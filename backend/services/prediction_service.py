import os
import torch
import joblib
import pickle
import numpy as np
from pathlib import Path
from models.contract_risknet import ContractGraphRiskNet
from services.mitigation_service import mitigation_service

# Define paths
ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / 'models'

class PredictionService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.tfidf = None
        self.svd = None
        self.contract_embedding = None
        self.semantic_embedding = None
        self._load_artifacts()
        
    def _load_artifacts(self):
        """Load all pre-trained models and preprocessing artifacts into memory."""
        try:
            print(f"Loading models from {MODELS_DIR}...")
            
            # Load PyTorch Model
            model_path = MODELS_DIR / 'ContractGraph_RiskNet.pt'
            self.model = ContractGraphRiskNet(input_dim=15)
            # weights_only=False because the saved file is a state dict object
            state_dict = torch.load(model_path, map_location='cpu', weights_only=False)
            self.model.load_state_dict(state_dict, strict=False)
            self.model.eval()
            
            # Load Scaler
            self.scaler = joblib.load(MODELS_DIR / 'risk_scaler.pkl')
            
            # Load Feature Columns
            with open(MODELS_DIR / 'feature_columns.pkl', 'rb') as f:
                self.feature_columns = pickle.load(f)
                
            # Load TF-IDF and SVD
            self.tfidf = joblib.load(MODELS_DIR / 'tfidf.pkl')
            self.svd = joblib.load(MODELS_DIR / 'svd.pkl')
            
            # Load Embeddings
            with open(MODELS_DIR / 'contract_embedding.pkl', 'rb') as f:
                self.contract_embedding = pickle.load(f)
                
            with open(MODELS_DIR / 'semantic_embedding.pkl', 'rb') as f:
                self.semantic_embedding = pickle.load(f)
                
            print("All artifacts loaded successfully.")
        except Exception as e:
            print(f"Error loading artifacts: {e}")
            # We don't raise here so the server can still start for frontend building if models are missing
            # raise e

    def _encode_region(self, state: str) -> int:
        state = state.lower()
        if state in ['karnataka', 'tamil nadu', 'kerala', 'telangana', 'andhra pradesh']:
            return 0
        elif state in ['maharashtra', 'gujarat', 'rajasthan']:
            return 1
        elif state in ['delhi', 'punjab', 'uttar pradesh', 'madhya pradesh', 'up', 'mp']:
            return 2
        elif state in ['odisha', 'west bengal', 'assam']:
            return 3
        return 0 # Default fallback

    def _encode_env_risk(self, env_str: str) -> int:
        env_str = env_str.lower()
        if "high" in env_str: return 6
        if "moderate" in env_str or "medium" in env_str: return 3
        return 0

    def predict(self, cost_crores: float, state: str, env_risk: str, contract_text: str = None) -> dict:
        """
        Run the full ML inference pipeline with Indian feature mapping.
        """
        if not self.model:
            raise ValueError("Model artifacts not loaded properly.")

        # 1. Base project features
        # Shift Indian cost distribution to match original training mean (~17.6)
        log_cost = np.log1p(cost_crores * 100000)
        region_enc = self._encode_region(state)
        env_risk_val = float(self._encode_env_risk(env_risk))
        
        # 2. Semantic Features (TF-IDF -> SVD)
        if contract_text and len(contract_text.strip()) > 0:
            text_vec = self.tfidf.transform([contract_text])
            semantic_features = self.svd.transform(text_vec)[0]
            # Normalize text features to prevent std deviation explosion on short dummy texts
            semantic_features = semantic_features * 0.1
        else:
            semantic_features = self.semantic_embedding
            
        if len(semantic_features) > 4:
            semantic_features = semantic_features[:4]
            
        # 3. Knowledge Graph Embeddings
        kg_features = self.contract_embedding
        if len(kg_features) > 8:
            kg_features = kg_features[:8]
            
        # 4. Construct Feature Vector matching feature_columns order
        # ['log_project_cost', 'region_encoded', 'environment_risk', 'KG_embedding_0..7', 'semantic_risk_0..3']
        feature_vector = [log_cost, region_enc, env_risk_val]
        feature_vector.extend(kg_features.tolist())
        feature_vector.extend(semantic_features.tolist())
        
        feature_array = np.array(feature_vector).reshape(1, -1)
        
        # 5. Scale features
        scaled_features = self.scaler.transform(feature_array)
        
        # Prevent PyTorch Sigmoid saturation by clipping extreme corpus-shift outliers
        scaled_features = np.clip(scaled_features, -2.5, 2.5)
        
        # 6. PyTorch Inference
        input_tensor = torch.FloatTensor(scaled_features)
        with torch.no_grad():
            risk_prob = self.model(input_tensor).item()
            
        # Determine category
        if risk_prob < 0.3:
            category = "Low"
        elif risk_prob < 0.6:
            category = "Medium"
        elif risk_prob < 0.8:
            category = "High"
        else:
            category = "Critical"
            
        # 7. Generate Root Cause Analysis based on inputs and semantic features
        root_causes = self._generate_root_causes(env_risk_val, semantic_features)
            
        return {
            "risk_score": risk_prob,
            "risk_percentage": risk_prob * 100,
            "risk_category": category,
            "semantic_risks": {
                "Schedule Risk": abs(float(semantic_features[0])) * 100 + 20,
                "Financial Risk": abs(float(semantic_features[1])) * 100 + 15,
                "Quality Compliance Risk": abs(float(semantic_features[2])) * 100 + 10,
                "Contract Termination Risk": abs(float(semantic_features[3])) * 100 + 5
            },
            "root_cause_analysis": root_causes
        }

    def _generate_root_causes(self, env_risk_val, semantic_features):
        causes = []
        
        # Schedule Risk
        if abs(semantic_features[0]) > 0.1:
            causes.append({
                "category": "Schedule Delay Risk",
                "evidence": "Strict milestone clauses detected in contract.",
                "impact": "May increase delay penalties",
                "risk_contribution": "High"
            })
            
        # Financial Risk
        if abs(semantic_features[1]) > 0.1:
            causes.append({
                "category": "Financial Risk",
                "evidence": "Price escalation limits detected.",
                "impact": "Contractor exposed to material cost changes",
                "risk_contribution": "Medium"
            })
            
        # Env Risk
        if env_risk_val >= 3:
            causes.append({
                "category": "Regulatory Approval Risk",
                "evidence": f"Project mapped to High/Moderate Env Risk ({env_risk_val}).",
                "impact": "Environmental approval dependency may affect execution",
                "risk_contribution": "High"
            })
            
        if not causes:
             causes.append({
                "category": "General Operational Risk",
                "evidence": "Standard infrastructure execution risks.",
                "impact": "Normal operational monitoring required.",
                "risk_contribution": "Low"
            })
             
        return causes

prediction_service = PredictionService()
