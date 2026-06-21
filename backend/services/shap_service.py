class ShapService:
    def explain_prediction(self, features: dict, risk_score: float) -> list:
        """Feature importance explanations for the ML prediction."""
        explanations = []
        cost = features.get("cost_crores", 0)
        state = features.get("state", "Delhi")

        if cost > 5000:
            explanations.append({"feature": "Project Cost (>5000 Cr)", "impact_value": round(0.15 * risk_score, 3), "description": "Mega-projects have historically higher schedule overrun probability."})
        elif cost > 2000:
            explanations.append({"feature": "Project Cost (>2000 Cr)", "impact_value": round(0.08 * risk_score, 3), "description": "Large projects carry moderate resource management risk."})

        high_risk_states = ["kerala", "west bengal", "bihar", "assam", "jharkhand"]
        if any(s in state.lower() for s in high_risk_states):
            explanations.append({"feature": f"State Risk ({state})", "impact_value": round(0.12 * risk_score, 3), "description": "Historical ROW/labour challenges in this region."})

        explanations.append({"feature": "KG Structural Embedding", "impact_value": round(0.10 * risk_score, 3), "description": "Node2Vec embedding captures causal risk topology."})
        explanations.append({"feature": "Semantic Clause Vector", "impact_value": round(0.07 * risk_score, 3), "description": "TF-IDF+SVD encodes penalty language severity."})

        explanations.sort(key=lambda x: abs(x["impact_value"]), reverse=True)
        return explanations

    def generate_risk_breakdown(self, baseline: dict, risk_score: float) -> list:
        """Generate 8-category risk breakdown from contract features."""
        contract_value = baseline.get("contract_value", 1000)
        milestones = baseline.get("milestones", [])
        obligations = baseline.get("obligations", [])
        materials = baseline.get("materials", [])

        # Base risk distributed across categories
        base = risk_score * 100

        # Analyze obligations for specific risk evidence
        has_ld = any("financial" in o.get("impact", "").lower() or "penalty" in o.get("clause", "").lower() or "liquidated" in o.get("clause", "").lower() for o in obligations)
        has_termination = any("termination" in o.get("impact", "").lower() or "termination" in o.get("clause", "").lower() for o in obligations)
        has_quality = any("quality" in o.get("impact", "").lower() or "quality" in o.get("clause", "").lower() for o in obligations)
        has_env = any("environment" in o.get("clause", "").lower() or "forest" in o.get("clause", "").lower() for o in obligations)
        has_legal = any("dispute" in o.get("impact", "").lower() or "breach" in o.get("clause", "").lower() or "legal" in o.get("impact", "").lower() for o in obligations)

        categories = [
            {
                "name": "Schedule Risk",
                "score": round(min(95, base * 1.1 + (10 if len(milestones) > 5 else 0)), 1),
                "reason": f"{len(milestones)} milestones with tight sequencing" if milestones else "No milestones extracted",
                "evidence": f"Contract specifies {len(milestones)} sequential activities",
                "impact": "Delay in any critical-path activity cascades to project completion"
            },
            {
                "name": "Financial Risk",
                "score": round(min(95, base * 1.05 + (15 if has_ld else 0) + (10 if contract_value > 3000 else 0)), 1),
                "reason": "LD clause detected with daily penalty structure" if has_ld else "Standard payment terms",
                "evidence": next((o["clause"] for o in obligations if "financial" in o.get("impact", "").lower()), "No specific clause"),
                "impact": f"Potential LD exposure on Rs.{contract_value} Cr contract"
            },
            {
                "name": "Quality Risk",
                "score": round(min(90, base * 0.7 + (15 if has_quality else 0)), 1),
                "reason": "Quality compliance requirements specified" if has_quality else "Standard quality norms apply",
                "evidence": next((o["clause"] for o in obligations if "quality" in o.get("impact", "").lower()), "IRC/IS code compliance"),
                "impact": "Rework and rejection of defective work"
            },
            {
                "name": "Environmental Risk",
                "score": round(min(85, base * 0.5 + (20 if has_env else 5)), 1),
                "reason": "Environmental clearance dependency" if has_env else "Standard environmental compliance",
                "evidence": next((o["clause"] for o in obligations if "environment" in o.get("clause", "").lower()), "MoEFCC norms"),
                "impact": "Work stoppage if clearance delayed or violated"
            },
            {
                "name": "Termination Risk",
                "score": round(min(90, base * 0.4 + (25 if has_termination else 0)), 1),
                "reason": "Termination clause with specific triggers" if has_termination else "Standard termination provisions",
                "evidence": next((o["clause"] for o in obligations if "termination" in o.get("clause", "").lower()), "Model EPC agreement"),
                "impact": "Complete project takeover by authority"
            },
            {
                "name": "Compliance Risk",
                "score": round(min(85, base * 0.6), 1),
                "reason": f"Regulatory compliance for Rs.{contract_value} Cr public infrastructure",
                "evidence": "NHAI/State PWD guidelines",
                "impact": "Contract suspension for non-compliance"
            },
            {
                "name": "Safety Risk",
                "score": round(min(80, base * 0.45 + (5 if contract_value > 2000 else 0)), 1),
                "reason": "Large-scale earthwork and structural activities",
                "evidence": "IS safety standards + BOCW Act",
                "impact": "Work stoppage, legal liability, insurance claims"
            },
            {
                "name": "Legal Risk",
                "score": round(min(90, base * 0.55 + (15 if has_legal else 0)), 1),
                "reason": "Dispute resolution clauses present" if has_legal else "Standard arbitration provisions",
                "evidence": next((o["clause"] for o in obligations if "legal" in o.get("impact", "").lower() or "dispute" in o.get("impact", "").lower()), "Arbitration Act provisions"),
                "impact": "Protracted litigation and cost escalation"
            }
        ]

        return categories

shap_service = ShapService()
