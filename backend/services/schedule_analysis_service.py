class ScheduleAnalysisService:
    def analyze_monthly_report(self, planned: float, actual: float, cost_spent: float, total_cost: float) -> dict:
        """
        Calculate deviations and health scores for a monthly report.
        """
        schedule_variance = actual - planned
        
        # Determine status
        if schedule_variance >= 0:
            status = "On Track"
        elif schedule_variance > -10:
            status = "Slightly Behind"
        else:
            status = "Severely Delayed"
            
        # Basic cost analysis (assuming linear progression for simple mock)
        # If we spent 50% of budget but only did 20% work, that's bad.
        expected_cost_spent = total_cost * (actual / 100.0) if actual > 0 else 0
        cost_deviation = cost_spent - expected_cost_spent
        
        # Calculate Health Scores out of 100
        # Schedule Health
        schedule_health = 100 + (schedule_variance * 2)
        schedule_health = max(0, min(100, schedule_health))
        
        # Cost Health
        cost_ratio = (expected_cost_spent / cost_spent) if cost_spent > 0 else 1.0
        cost_health = int(100 * cost_ratio)
        cost_health = max(0, min(100, cost_health))
        
        # Quality/Contract Health (mock based on variance for demo)
        quality_health = max(50, 100 - abs(schedule_variance))
        contract_health = max(40, schedule_health - 10)

        return {
            "schedule_variance": schedule_variance,
            "status": status,
            "cost_deviation": cost_deviation,
            "health": {
                "schedule_health": int(schedule_health),
                "cost_health": int(cost_health),
                "quality_health": int(quality_health),
                "contract_health": int(contract_health)
            }
        }

schedule_service = ScheduleAnalysisService()
