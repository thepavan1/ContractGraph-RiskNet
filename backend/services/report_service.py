import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ReportService:
    def generate_pdf_report(self, project: dict, baseline: dict, reports: list, control_room_data: dict) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=20,
            alignment=1 # Center
        )
        h2_style = ParagraphStyle(
            'Heading2Custom',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=15,
            spaceAfter=10,
            borderPadding=5,
        )
        normal_style = styles['Normal']
        
        elements = []

        # 1. Header
        elements.append(Paragraph(f"AI Project Risk & Execution Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        elements.append(Spacer(1, 20))
        
        # 2. Project Details
        elements.append(Paragraph("1. Project Details", h2_style))
        proj_data = [
            ["Project Name", project.get("name", "N/A")],
            ["Contract Type", project.get("category", "N/A")],
            ["State", baseline.get("state", "N/A")],
            ["Contract Value", f"Rs. {baseline.get('contract_value', 0)} Cr"],
            ["Duration", f"{baseline.get('duration_days', 'N/A')} Days"]
        ]
        t = Table(proj_data, colWidths=[150, 350])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
        ]))
        elements.append(t)
        
        # 3. ContractGraph-RiskNet Prediction
        elements.append(Paragraph("2. Baseline Contractual Risk", h2_style))
        risk_score = baseline.get("contractual_risk_exposure", 0)
        risk_cat = baseline.get("risk_category", "Unknown")
        elements.append(Paragraph(f"<b>Base Risk Exposure:</b> {risk_score:.1f}% ({risk_cat})", normal_style))
        elements.append(Spacer(1, 10))

        # 4. SHAP Feature Explanations
        elements.append(Paragraph("3. SHAP Intelligence (Risk Drivers)", h2_style))
        if "ai_explanation" in control_room_data:
            elements.append(Paragraph(control_room_data["ai_explanation"], normal_style))
        else:
            elements.append(Paragraph("SHAP explanations not available.", normal_style))
            
        # 5. DPR Deviation Analysis & 6. Timeline Status
        elements.append(Paragraph("4. Execution Deviation Analysis", h2_style))
        latest_report = reports[-1] if reports else {}
        if latest_report:
            dev_data = [
                ["Reporting Month", f"Month {latest_report.get('report_month', 'N/A')}"],
                ["Planned Progress", f"{latest_report.get('planned_progress', 0):.1f}%"],
                ["Actual Progress", f"{latest_report.get('actual_progress', 0):.1f}%"],
                ["Schedule Variance", f"{latest_report.get('schedule_variance', 0):.1f}%"],
                ["Estimated Delay", f"{latest_report.get('estimated_delay_days', 0)} Days"],
                ["Execution Risk Score", f"{latest_report.get('execution_risk_score', 0):.1f}%"]
            ]
            t2 = Table(dev_data, colWidths=[200, 300])
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            elements.append(t2)
            
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("<b>Reported Issues:</b>", normal_style))
            for issue in latest_report.get("issues", []):
                elements.append(Paragraph(f"• {issue}", normal_style))
        else:
            elements.append(Paragraph("No monthly reports uploaded yet.", normal_style))

        # 7. Contract Violation Warnings
        elements.append(Paragraph("5. Contract Violation Warnings", h2_style))
        ld_exp = latest_report.get("ld_penalty_exposure_crores", 0) if latest_report else 0
        if ld_exp > 0:
            warn_style = ParagraphStyle('Warn', parent=normal_style, textColor=colors.red)
            elements.append(Paragraph(f"<b>CRITICAL WARNING:</b> Liquidated Damages (LD) clause triggered.", warn_style))
            elements.append(Paragraph(f"<b>Estimated Penalty Exposure:</b> Rs. {ld_exp:.2f} Crores", warn_style))
        else:
            elements.append(Paragraph("No active financial penalties detected based on current deviation.", normal_style))
            
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<b>Risk Cascade Chain:</b>", normal_style))
        for chain in control_room_data.get("risk_chain", []):
            elements.append(Paragraph(f"• {chain.get('node')}: {chain.get('desc')}", normal_style))

        # 8. Mitigation Recommendations
        elements.append(Paragraph("6. AI Mitigation Recommendations", h2_style))
        elements.append(Paragraph("Based on the Neuro-Symbolic analysis and current schedule delay, the following recovery actions are recommended:", normal_style))
        elements.append(Spacer(1, 5))
        
        delay = latest_report.get("estimated_delay_days", 0) if latest_report else 0
        if delay > 30:
            elements.append(Paragraph("• Immediate mobilization of 3-shift continuous working (24/7).", normal_style))
            elements.append(Paragraph("• Deploy additional heavy machinery (min. 15% fleet increase) to earthwork/foundation fronts.", normal_style))
            elements.append(Paragraph("• Issue formal Force Majeure / Extension of Time (EoT) notices to the Authority to freeze LD accumulation.", normal_style))
        elif delay > 10:
            elements.append(Paragraph("• Implement 2-shift extended working hours.", normal_style))
            elements.append(Paragraph("• Increase skilled workforce by 20% on critical path activities.", normal_style))
            elements.append(Paragraph("• Expedite pending material procurements.", normal_style))
        else:
            elements.append(Paragraph("• Maintain current resource allocation.", normal_style))
            elements.append(Paragraph("• Monitor quality compliance closely to prevent rework.", normal_style))

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes

report_service = ReportService()
