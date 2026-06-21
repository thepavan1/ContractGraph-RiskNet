class MitigationService:
    def generate_mitigation_steps(self, risk_category: str, clauses: list) -> list:
        """
        Generate Indian-context mitigation steps based on risk profile and flagged clauses.
        """
        steps = []
        
        # Determine primary focus based on overall risk category
        if risk_category in ["High", "Critical"]:
            steps.append("Immediate: Establish high-level steering committee with State/Central authorities.")
            
        # Analyze clauses to give specific recommendations
        clause_text = " ".join(clauses).lower()
        
        if "delay" in clause_text or "milestone" in clause_text:
            steps.extend([
                "Schedule: Increase resource allocation on critical path activities.",
                "Schedule: Implement weekly progress monitoring with drone surveillance.",
                "Schedule: Fast-track pending ROW (Right of Way) and utility shifting clearances."
            ])
            
        if "penalty" in clause_text or "liquidated" in clause_text or "cost" in clause_text:
            steps.extend([
                "Financial: Lock in material prices (cement/steel) with long-term supplier agreements.",
                "Financial: Maintain a minimum 10% contingency fund for cost escalation.",
                "Financial: Closely monitor cash-flow and ensure timely submission of RA bills."
            ])
            
        if "termination" in clause_text or "default" in clause_text:
            steps.extend([
                "Legal: Conduct immediate contract review to identify breach triggers.",
                "Legal: Ensure strict compliance with all environmental and local statutory clearances to prevent stop-work notices."
            ])
            
        if "quality" in clause_text or "defect" in clause_text:
            steps.extend([
                "Quality: Appoint independent Third-Party Quality Audit (TPQA) agency.",
                "Quality: Increase frequency of material testing at site laboratory."
            ])
            
        # Fallback if no specific clauses triggered
        if not steps:
            steps = [
                "General: Conduct monthly risk review meetings.",
                "General: Ensure all site engineers are trained on contract dispute mechanisms."
            ]
            
        return steps[:5] # Return top 5

mitigation_service = MitigationService()
