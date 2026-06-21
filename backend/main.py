from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv
import os, json, uuid
from datetime import datetime

from models.schemas import ChatRequest, ChatResponse

load_dotenv()
from contextlib import asynccontextmanager

from services.prediction_service import prediction_service
from services.pdf_service import pdf_service
from services.kg_service import kg_service
from services.rag_service import rag_service
from services.deviation_engine import deviation_engine
from services.shap_service import shap_service
from services.report_service import report_service
from database.mongodb import db_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_service.initialize_and_seed()
    yield

app = FastAPI(title="ContractGraph-RiskNet API", version="2.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root():
    return {"message": "ContractGraph-RiskNet API running"}

# ─── PROJECT LIST ───
@app.get("/api/projects")
async def list_projects():
    projects = await db_service.get_projects()
    for p in projects:
        p.setdefault("status", "Active")
        p.setdefault("category", "Unknown")
        p.setdefault("name", p.get("title", "Unnamed"))
    return projects

# ─── COMPLETE PROFILE (Single Source of Truth) ───
@app.get("/api/projects/{project_id}/complete-profile")
async def get_complete_profile(project_id: str):
    projects = await db_service.get_projects()
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    baseline = await db_service.get_project_baseline(project_id)
    reports = await db_service.get_project_reports(project_id)
    risk_history = await db_service.get_risk_history(project_id)

    # Build deviation analysis from latest report
    latest = reports[-1] if reports else {}
    deviations = {}
    if latest and baseline:
        deviations = {
            "schedule_variance": latest.get("schedule_variance", 0),
            "cost_variance_crores": latest.get("cost_variance_crores", 0),
            "spi": latest.get("spi", 1.0),
            "cpi": latest.get("cpi", 1.0),
            "schedule_status": latest.get("schedule_status", "ON TRACK"),
            "estimated_delay_days": latest.get("estimated_delay_days", 0),
            "execution_risk_score": latest.get("execution_risk_score", 0),
            "overall_health_score": latest.get("overall_health_score", 100),
            "ld_penalty_exposure_crores": latest.get("ld_penalty_exposure_crores", 0),
            "delayed_activities": latest.get("delayed_activities", [])
        }

    # SHAP
    risk_score = baseline.get("contractual_risk_exposure", 50) / 100 if baseline else 0.5
    shap_values = shap_service.explain_prediction(
        {"cost_crores": baseline.get("contract_value", 1000) if baseline else 1000, "state": baseline.get("state", "Delhi") if baseline else "Delhi"},
        risk_score
    )
    risk_breakdown = shap_service.generate_risk_breakdown(baseline or {}, risk_score)

    # S-Curve and cost curve from all reports
    s_curve = []
    cost_curve = []
    risk_evolution = []
    contract_risk = baseline.get("contractual_risk_exposure", 0) if baseline else 0
    cv = baseline.get("contract_value", 1000) if baseline else 1000

    for r in reports:
        m = f"M{r.get('report_month', 1)}"
        pl = r.get("planned_progress", 0)
        ac = r.get("actual_progress", 0)
        s_curve.append({"month": m, "planned": pl, "actual": ac})
        budget = round((pl / 100) * cv, 2)
        spend = round((ac / 100) * cv, 2)
        cost_curve.append({"month": m, "budget": budget, "actual_spend": spend, "forecast": round(spend * 1.08, 2)})
        risk_evolution.append({
            "month": m,
            "contractRisk": contract_risk,
            "executionRisk": r.get("execution_risk_score", 0),
            "totalHealth": r.get("overall_health_score", 100)
        })

    # Recovery suggestion
    delay = deviations.get("estimated_delay_days", 0)
    recovery = {}
    if delay > 0:
        recovery = deviation_engine.simulate_recovery(delay, 50, 5, 2, 1.0)

    # Risk chain
    risk_chain = []
    if delay > 0:
        risk_chain.append({"node": "Schedule Deviation", "desc": f"{delay} days behind baseline"})
        risk_chain.append({"node": "Execution Risk", "desc": f"{deviations.get('execution_risk_score', 0):.0f}% elevated"})
        if delay > 15:
            risk_chain.append({"node": "LD Clause Activated", "desc": f"Rs.{deviations.get('ld_penalty_exposure_crores', 0):.2f} Cr penalty"})
        if delay > 45:
            risk_chain.append({"node": "Termination Warning", "desc": "Authority may invoke termination"})

    # Timeline
    timeline = []
    if baseline:
        for ms in baseline.get("milestones", []):
            timeline.append({"name": ms.get("name"), "planned_start": ms.get("planned_start"), "planned_end": ms.get("planned_end"), "weightage": ms.get("weightage", 0)})

    return {
        "project": project,
        "baseline": {
            "project_name": baseline.get("project_name", project.get("name", "")) if baseline else project.get("name", ""),
            "contract_type": baseline.get("contract_type", "") if baseline else "",
            "contract_value": baseline.get("contract_value", 0) if baseline else 0,
            "state": baseline.get("state", "") if baseline else "",
            "planned_start": baseline.get("planned_start", "") if baseline else "",
            "planned_end": baseline.get("planned_end", "") if baseline else "",
            "contractual_risk_exposure": baseline.get("contractual_risk_exposure", 0) if baseline else 0,
            "risk_category": baseline.get("risk_category", "Unknown") if baseline else "Unknown",
            "milestones": baseline.get("milestones", []) if baseline else [],
            "materials": baseline.get("materials", []) if baseline else [],
            "obligations": baseline.get("obligations", []) if baseline else [],
        },
        "dpr_reports": [{
            "month": r.get("report_month", 0),
            "planned_progress": r.get("planned_progress", 0),
            "actual_progress": r.get("actual_progress", 0),
            "schedule_variance": r.get("schedule_variance", 0),
            "execution_risk_score": r.get("execution_risk_score", 0),
            "overall_health_score": r.get("overall_health_score", 100),
            "estimated_delay_days": r.get("estimated_delay_days", 0),
            "ld_penalty_exposure_crores": r.get("ld_penalty_exposure_crores", 0),
            "issues": r.get("issues", []),
            "delayed_activities": r.get("delayed_activities", []),
            "mitigation_steps": r.get("mitigation_steps", [])
        } for r in reports],
        "risk": {
            "probability": round(risk_score * 100, 1),
            "category": baseline.get("risk_category", "Unknown") if baseline else "Unknown",
            "shap_values": shap_values,
            "risk_breakdown": risk_breakdown
        },
        "deviations": deviations,
        "recovery": recovery,
        "charts": {
            "s_curve": s_curve,
            "cost_curve": cost_curve,
            "risk_evolution": risk_evolution
        },
        "risk_chain": risk_chain,
        "timeline": timeline,
        "risk_history": risk_history
    }

# ─── CONTRACT BASELINE UPLOAD ───
@app.post("/api/extract/baseline")
async def extract_baseline(project_id: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    baseline = pdf_service.extract_contract_data(content)
    baseline["project_id"] = project_id

    pred = prediction_service.predict(
        cost_crores=baseline.get("contract_value", 1000),
        state=baseline.get("state", "Delhi"),
        env_risk="Moderate",
        contract_text=baseline.get("raw_text", "")
    )
    baseline["contractual_risk_exposure"] = pred["risk_score"] * 100
    baseline["risk_category"] = pred["risk_category"]
    if "raw_text" in baseline: del baseline["raw_text"]

    if not db_service.use_mock:
        await db_service.db.contract_baselines.update_one({"project_id": project_id}, {"$set": baseline}, upsert=True)
        await db_service.db.projects.update_one({"id": project_id}, {"$set": {"risk_score": pred["risk_score"], "category": pred["risk_category"]}})
    else:
        db_service.mock_baselines[project_id] = baseline
        for p in db_service.mock_projects:
            if p["id"] == project_id:
                p["risk_score"] = pred["risk_score"]
                p["category"] = pred["risk_category"]

    await db_service.save_risk_history(project_id, {"event": "Baseline Extraction", "risk_score": pred["risk_score"]*100, "source": "ContractGraph-RiskNet"})
    if "_id" in baseline: del baseline["_id"]

    # Return risk breakdown too
    risk_breakdown = shap_service.generate_risk_breakdown(baseline, pred["risk_score"])
    baseline["risk_breakdown"] = risk_breakdown
    return baseline

# ─── DPR UPLOAD ───
@app.post("/api/reports/upload")
async def upload_monthly_report(project_id: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    dpr_data = pdf_service.extract_dpr_data(content)
    dpr_data["id"] = str(uuid.uuid4())
    dpr_data["project_id"] = project_id
    if "raw_text" in dpr_data: del dpr_data["raw_text"]

    baseline = await db_service.get_project_baseline(project_id)
    if not baseline:
        raise HTTPException(status_code=400, detail="Contract Baseline not found. Upload contract first.")

    deviations = deviation_engine.calculate_deviations(baseline, dpr_data)
    dpr_data.update(deviations)
    
    from services.mitigation_service import mitigation_service
    risk_cat = deviations.get("schedule_status", "LOW")
    if "CRITICAL" in risk_cat: risk_cat = "Critical"
    elif "HIGH" in risk_cat: risk_cat = "High"
    else: risk_cat = "Low"
    clauses = [ob.get("clause", "") for ob in baseline.get("obligations", [])]
    dpr_data["mitigation_steps"] = mitigation_service.generate_mitigation_steps(risk_cat, clauses)

    if not db_service.use_mock:
        await db_service.db.monthly_reports.insert_one(dpr_data)
    else:
        if project_id not in db_service.mock_reports: db_service.mock_reports[project_id] = []
        db_service.mock_reports[project_id].append(dpr_data)

    await db_service.save_risk_history(project_id, {
        "event": f"DPR Month {dpr_data.get('report_month')}",
        "execution_risk": deviations["execution_risk_score"],
        "overall_health": deviations["overall_health_score"],
        "delay_days": deviations["estimated_delay_days"]
    })

    if "_id" in dpr_data: del dpr_data["_id"]
    return dpr_data

# ─── RECOVERY SIMULATOR ───
from pydantic import BaseModel
class SimulationRequest(BaseModel):
    workers: int
    excavators: int
    shifts: int
    budget: float

@app.post("/api/projects/{project_id}/simulate")
async def simulate_recovery(project_id: str, req: SimulationRequest):
    reports = await db_service.get_project_reports(project_id)
    latest = reports[-1] if reports else {}
    delay = latest.get("estimated_delay_days", 0)
    result = deviation_engine.simulate_recovery(delay, req.workers, req.excavators, req.shifts, req.budget)
    return result

# ─── KNOWLEDGE GRAPH ───
@app.get("/api/kg")
def get_knowledge_graph():
    return kg_service.get_graph_data()

# ─── AI CHAT ───
@app.post("/api/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest):
    response_text = rag_service.chat(request.message, request.context)
    return {"response": response_text}

# ─── PDF REPORT ───
@app.get("/api/projects/{project_id}/generate-report")
async def generate_ai_report(project_id: str):
    profile = await get_complete_profile(project_id)
    projects = await db_service.get_projects()
    project = next((p for p in projects if p["id"] == project_id), {})
    baseline = await db_service.get_project_baseline(project_id)
    reports = await db_service.get_project_reports(project_id)

    pdf_bytes = report_service.generate_pdf_report(project, baseline or {}, reports, {
        "ai_explanation": f"Risk Analysis based on {len(reports)} DPR reports. SHAP features: {', '.join(s['feature'] for s in profile['risk']['shap_values'])}.",
        "risk_chain": profile.get("risk_chain", [])
    })
    name = project.get("name", "Project").replace(" ", "_")
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="AI_Risk_Report_{name}.pdf"'})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
