from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Milestone(BaseModel):
    name: str
    planned_start: str
    planned_end: str
    completion_req: float

class Material(BaseModel):
    name: str
    qty: str
    phase: str

class Obligation(BaseModel):
    clause: str
    meaning: str
    impact: str

class ContractBaselineResponse(BaseModel):
    project_id: str
    contract_value: float
    planned_start: str
    planned_end: str
    milestones: List[Milestone] = Field(default_factory=list)
    materials: List[Material] = Field(default_factory=list)
    obligations: List[Obligation] = Field(default_factory=list)
    contractual_risk_exposure: float = Field(0.0)
    risk_category: str = Field("Low")
    semantic_features: List[float] = Field(default_factory=list)
    kg_activations: List[str] = Field(default_factory=list)

class ContractPredictionRequest(BaseModel):
    project_cost_crores: float = Field(..., description="Project Cost in ₹ Crores")
    state: str = Field(..., description="Indian State")
    city: str = Field(..., description="City")
    contract_type: str = Field(..., description="EPC, HAM, BOT, etc.")
    terrain: str = Field(..., description="Plain, Coastal, Mountain, Forest, Urban")
    monsoon_impact: str = Field(..., description="Low, Medium, High")
    contractor_exp: str = Field(..., description="New, Medium, Experienced")
    environment_risk: str = Field(..., description="Low Risk, Moderate Risk, High Risk")
    contract_text: Optional[str] = Field(None, description="Extracted text from the contract PDF")

class RootCause(BaseModel):
    category: str
    evidence: str
    impact: str
    risk_contribution: str

class ContractPredictionResponse(BaseModel):
    risk_score: float = Field(..., description="Predicted risk probability (0-1)")
    risk_percentage: float = Field(..., description="Predicted risk percentage (0-100)")
    risk_category: str = Field(..., description="Risk category (Low, Medium, High, Critical)")
    
    # Transparency fields
    semantic_risks: Dict[str, float] = Field(default_factory=dict, description="Semantic risk components")
    extracted_clauses: List[str] = Field(default_factory=list, description="Key risky clauses extracted")
    
    # New Intelligence Fields
    root_cause_analysis: List[RootCause] = Field(default_factory=list)
    mitigation_steps: List[str] = Field(default_factory=list)
    kg_activated_nodes: List[str] = Field(default_factory=list)

class ProjectListResponse(BaseModel):
    id: str
    name: str
    status: str
    category: str
    created_at: str

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_cost_crores: float
    state: str
    city: str
    contract_type: str
    terrain: str
    monsoon_impact: str
    contractor_exp: str
    environment_risk: str
    contract_text: Optional[str] = None
    
class ProjectResponse(ProjectCreate):
    id: str
    risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    created_at: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

class MonthlyReportUpload(BaseModel):
    project_id: str
    reporting_month: str
    planned_progress: float
    actual_progress: float
    cost_spent: float
    revised_cost: Optional[float] = None
    delay_days: int
    issues_mentioned: List[str] = Field(default_factory=list)
    completed_activities: List[str] = Field(default_factory=list)
    pending_activities: List[str] = Field(default_factory=list)

class ProjectHealth(BaseModel):
    schedule_health: int
    cost_health: int
    quality_health: int
    contract_health: int

class DashboardData(BaseModel):
    contract_risk: float
    execution_risk: float
    overall_health: float
    delay_days: int
    budget_overrun: float
    ld_exposure: float
    s_curve: List[dict]
    cost_curve: List[dict]
    risk_evolution: List[dict]
    heat_map: List[dict]

class ControlRoomData(BaseModel):
    timeline: List[dict]
    status: List[dict]
    risk_chain: List[dict]
    ai_explanation: str
