class DeviationEngine:
    def calculate_deviations(self, baseline: dict, report: dict):
        """Compare DPR actuals against contract baseline — activity-level."""
        planned = report.get("planned_progress", 0)
        actual = report.get("actual_progress", 0)
        
        # 1. Schedule Variance & SPI
        variance = actual - planned
        spi = round((actual / planned) if planned > 0 else 1.0, 2)
        
        # 2. Cost Variance & CPI
        financial = report.get("financial_progress", actual)
        cpi = round((actual / financial) if financial > 0 else 1.0, 2)
        contract_value = baseline.get("contract_value", 1000)
        earned_value = (actual / 100) * contract_value
        actual_cost = (financial / 100) * contract_value
        cost_variance = round(earned_value - actual_cost, 2)

        # 3. Delay classification (engineering-based)
        schedule_status = "ON TRACK"
        delay_days = 0
        execution_risk = 0.0
        total_duration = baseline.get("duration_days", 730)

        if variance < -20:
            schedule_status = "CRITICAL DELAY"
            delay_days = int(abs(variance) / 100 * total_duration)
            execution_risk = min(95, 50 + abs(variance) * 1.5)
        elif variance < -10:
            schedule_status = "HIGH DELAY"
            delay_days = int(abs(variance) / 100 * total_duration)
            execution_risk = min(80, 30 + abs(variance) * 1.8)
        elif variance < -5:
            schedule_status = "MODERATE DELAY"
            delay_days = int(abs(variance) / 100 * total_duration)
            execution_risk = min(60, 15 + abs(variance) * 1.5)
        elif variance < 0:
            schedule_status = "MINOR DELAY"
            delay_days = int(abs(variance) / 100 * total_duration)
            execution_risk = max(5, abs(variance) * 2)

        # 4. Activity-level deviation
        delayed_activities = []
        milestones = baseline.get("milestones", [])
        report_month = report.get("report_month", 1)
        for ms in milestones:
            ms_weight = ms.get("weightage", 10)
            # Estimate expected completion by this month
            ms_expected = min(100, (report_month / max(len(milestones), 1)) * 100)
            # Actual is proportional to overall actual with some spread
            ms_actual = max(0, actual * (ms_weight / (100 / max(len(milestones), 1))))
            ms_actual = min(100, ms_actual)
            ms_variance = round(ms_actual - ms_expected, 1)
            if ms_variance < -5:
                delayed_activities.append({
                    "activity": ms.get("name", "Unknown"),
                    "expected": round(ms_expected, 1),
                    "actual": round(ms_actual, 1),
                    "variance": ms_variance
                })

        # 5. LD penalty from contract obligations
        ld_penalty_exposure = 0
        if delay_days > 15:
            obligations = baseline.get("obligations", [])
            for ob in obligations:
                if "Financial" in ob.get("impact", "") or "penalty" in ob.get("clause", "").lower() or "liquidated" in ob.get("clause", "").lower():
                    ld_penalty_exposure = contract_value * 0.0005 * delay_days
                    break
            if ld_penalty_exposure == 0:
                ld_penalty_exposure = contract_value * 0.0003 * delay_days

        # 6. Overall Health (40% Contract, 60% Execution)
        contractual_risk = baseline.get("contractual_risk_exposure", 50)
        overall_health = 100 - ((contractual_risk * 0.4) + (execution_risk * 0.6))
        overall_health = max(0, min(100, overall_health))

        return {
            "schedule_variance": round(variance, 1),
            "spi": spi,
            "cpi": cpi,
            "cost_variance_crores": cost_variance,
            "schedule_status": schedule_status,
            "estimated_delay_days": delay_days,
            "ld_penalty_exposure_crores": round(ld_penalty_exposure, 2),
            "execution_risk_score": round(execution_risk, 1),
            "overall_health_score": round(overall_health, 1),
            "delayed_activities": delayed_activities
        }

    def simulate_recovery(self, delay_days: int, workers: int, excavators: int, shifts: int, budget: float):
        """Engineering-grade recovery simulation."""
        if delay_days <= 0:
            return {
                "recovered_days": 0,
                "remaining_delay_days": 0,
                "recovery_cost_crores": 0,
                "productivity_increase_percent": 0,
                "new_risk_category": "LOW",
                "risk_before": "LOW",
                "risk_after": "LOW"
            }

        # Engineering productivity rates
        # 1 worker = ~0.08 days recovered per day of deployment (avg across trades)
        # 1 excavator = ~0.35 days recovered per day
        # Budget: 1 Cr can accelerate ~1.5 days through procurement/logistics
        worker_output = workers * 0.08
        machine_output = excavators * 0.35
        budget_output = budget * 1.5

        base_daily_recovery = worker_output + machine_output + budget_output

        # Shift multiplier (diminishing returns)
        if shifts == 2:
            base_daily_recovery *= 1.45
        elif shifts >= 3:
            base_daily_recovery *= 1.75

        # Max recovery is capped at 70% of delay (can't recover everything)
        max_recoverable = int(delay_days * 0.7)
        recovered_days = min(max_recoverable, int(base_daily_recovery))
        remaining_delay = delay_days - recovered_days

        # Cost estimate
        recovery_cost = round((workers * 0.002) + (excavators * 0.08) + budget, 2)
        if shifts > 1:
            recovery_cost *= (1 + (shifts - 1) * 0.3)
        recovery_cost = round(recovery_cost, 2)

        # Productivity increase
        prod_increase = round((recovered_days / delay_days) * 100, 1) if delay_days > 0 else 0

        # Risk category transition
        def get_risk_cat(delay):
            if delay > 90: return "CRITICAL"
            if delay > 45: return "HIGH"
            if delay > 15: return "MEDIUM"
            if delay > 0: return "LOW"
            return "NO RISK"

        risk_before = get_risk_cat(delay_days)
        risk_after = get_risk_cat(remaining_delay)

        return {
            "recovered_days": recovered_days,
            "remaining_delay_days": remaining_delay,
            "recovery_cost_crores": recovery_cost,
            "productivity_increase_percent": prod_increase,
            "risk_before": risk_before,
            "risk_after": risk_after
        }

deviation_engine = DeviationEngine()
