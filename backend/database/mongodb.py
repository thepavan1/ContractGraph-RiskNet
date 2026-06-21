import os
import uuid
from datetime import datetime
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from services.pdf_service import pdf_service

class DatabaseService:
    def __init__(self):
        self.db_url = os.getenv("MONGODB_URL")
        self.client = None
        self.db = None
        self.use_mock = False
        
        # Memory Mock Data
        self.mock_projects = []
        self.mock_baselines = {}
        self.mock_reports = {}
        self.mock_risk_history = {}
        
        if self.db_url:
            try:
                self.client = AsyncIOMotorClient(self.db_url)
                self.db = self.client.contractgraph
                print("Connected to MongoDB Atlas.")
            except Exception as e:
                print(f"MongoDB connection failed: {e}. Using Memory DB.")
                self.use_mock = True
        else:
            print("MONGODB_URL not found. Using Memory DB.")
            self.use_mock = True

    async def initialize_and_seed(self):
        """Seed DB with generated sample data if empty."""
        count = await self.db.projects.count_documents({}) if not self.use_mock else len(self.mock_projects)
        if count > 0:
            print(f"Database already contains {count} projects. Skipping seed.")
            return
            
        print("MongoDB is empty. Seeding deterministic dataset...")
        sample_dir = Path(__file__).resolve().parent.parent.parent / "sample_projects"
        if not sample_dir.exists():
            print("Sample projects directory not found.")
            return
            
        from services.prediction_service import prediction_service

        for proj_dir in sample_dir.iterdir():
            if not proj_dir.is_dir(): continue
            
            project_id = str(uuid.uuid4())
            
            # Extract baseline from contract PDF
            contract_pdf = next(proj_dir.glob("*_Contract.pdf"), None)
            if not contract_pdf: continue
            
            with open(contract_pdf, "rb") as f:
                baseline_data = pdf_service.extract_contract_data(f.read())
                
            project_name = baseline_data.get("project_name", proj_dir.name.replace("_", " "))
            
            # 1. Project
            project_data = {
                "id": project_id,
                "name": project_name,
                "status": "Active",
                "category": "Unknown",
                "created_at": datetime.now().isoformat()
            }
                
            # ML Inference on Baseline
            try:
                pred = prediction_service.predict(
                    cost_crores=baseline_data.get("contract_value", 1000.0),
                    state=baseline_data.get("state", "Delhi"),
                    env_risk="Moderate",
                    contract_text=baseline_data.get("raw_text", "")
                )
                project_data["risk_score"] = pred["risk_score"]
                project_data["category"] = pred["risk_category"]
                baseline_data["contractual_risk_exposure"] = pred["risk_score"] * 100
                baseline_data["risk_category"] = pred["risk_category"]
            except Exception as e:
                project_data["risk_score"] = 0.5
                project_data["category"] = "Medium"
                baseline_data["contractual_risk_exposure"] = 50.0
                baseline_data["risk_category"] = "Medium"

            if not self.use_mock:
                await self.db.projects.insert_one(project_data)
            
            # 2. Baseline
            baseline_data["project_id"] = project_id
            if "raw_text" in baseline_data:
                del baseline_data["raw_text"]
            
            if not self.use_mock:
                await self.db.contract_baselines.insert_one(baseline_data)
            
            # 3. Monthly Reports
            reports_dir = proj_dir / "monthly_reports"
            if reports_dir.exists():
                for pdf_path in sorted(reports_dir.glob("*.pdf")):
                    with open(pdf_path, "rb") as f:
                        dpr_data = pdf_service.extract_dpr_data(f.read())
                        
                    dpr_data["id"] = str(uuid.uuid4())
                    dpr_data["project_id"] = project_id
                    
                    if "raw_text" in dpr_data:
                        del dpr_data["raw_text"]
                        
                    # Calculate deviations to ensure accuracy from start
                    from services.deviation_engine import deviation_engine
                    from services.mitigation_service import mitigation_service
                    
                    deviations = deviation_engine.calculate_deviations(baseline_data, dpr_data)
                    dpr_data.update(deviations)
                    
                    # Generate mitigation steps
                    risk_cat = deviations.get("schedule_status", "LOW")
                    if "CRITICAL" in risk_cat: risk_cat = "Critical"
                    elif "HIGH" in risk_cat: risk_cat = "High"
                    else: risk_cat = "Low"
                    
                    clauses = [ob.get("clause", "") for ob in baseline_data.get("obligations", [])]
                    dpr_data["mitigation_steps"] = mitigation_service.generate_mitigation_steps(risk_cat, clauses)
                        
                    if not self.use_mock:
                        await self.db.monthly_reports.insert_one(dpr_data)
                    else:
                        if project_id not in self.mock_reports: self.mock_reports[project_id] = []
                        self.mock_reports[project_id].append(dpr_data)
                        
                    # Add risk history point
                    await self.save_risk_history(project_id, {
                        "event": f"DPR Month {dpr_data.get('report_month')}",
                        "execution_risk": deviations["execution_risk_score"],
                        "overall_health": deviations["overall_health_score"],
                        "delay_days": deviations["estimated_delay_days"]
                    })
                        
            # Save project to mock
            if self.use_mock:
                self.mock_projects.append(project_data)
                self.mock_baselines[project_id] = baseline_data
                        
        print("Database Seeding complete.")

    async def get_projects(self):
        if self.use_mock: return self.mock_projects
        return await self.db.projects.find({}, {"_id": 0}).to_list(length=100)
        
    async def get_project_baseline(self, project_id: str):
        if self.use_mock: return self.mock_baselines.get(project_id)
        return await self.db.contract_baselines.find_one({"project_id": project_id}, {"_id": 0})
        
    async def get_project_reports(self, project_id: str):
        if self.use_mock: return self.mock_reports.get(project_id, [])
        return await self.db.monthly_reports.find({"project_id": project_id}, {"_id": 0}).sort("report_month", 1).to_list(length=100)

    async def get_risk_history(self, project_id: str):
        if self.use_mock: return self.mock_risk_history.get(project_id, [])
        return await self.db.risk_history.find({"project_id": project_id}, {"_id": 0}).sort("timestamp", 1).to_list(length=100)

    async def save_risk_history(self, project_id: str, data: dict):
        data["project_id"] = project_id
        data["timestamp"] = datetime.now().isoformat()
        if not self.use_mock:
            await self.db.risk_history.insert_one(data)
        else:
            if project_id not in self.mock_risk_history: self.mock_risk_history[project_id] = []
            self.mock_risk_history[project_id].append(data)

db_service = DatabaseService()
