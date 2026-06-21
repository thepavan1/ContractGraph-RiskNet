import os
import random
import shutil
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SAMPLE_DIR = ROOT_DIR / "sample_projects"

# ====================================================
# 15 REALISTIC INDIAN INFRASTRUCTURE PROJECTS
# 5 risk categories x 3 projects each
# ====================================================

PROJECTS = {
    "1_NO_RISK": [
        {
            "name": "NHAI Bengaluru-Mysuru Expressway Phase II",
            "type": "EPC Contract",
            "cost": 2450,
            "state": "Karnataka",
            "milestones": [
                ("Site Survey & Geotechnical Investigation", 1, 2, 15),
                ("Land Acquisition & ROW Clearance", 2, 4, 20),
                ("Earthwork & Embankment", 4, 8, 25),
                ("Pavement & Bituminous Layer", 8, 14, 25),
                ("Structures & Flyovers", 10, 18, 10),
                ("Finishing & Handover", 18, 20, 5),
            ],
            "materials": [("Cement OPC 53 Grade", "85,000 Tons"), ("Steel TMT Bars Fe-500D", "32,000 Tons"), ("Bitumen VG-30", "18,000 Tons"), ("Aggregate 20mm", "250,000 Cu.m")],
            "clauses": [
                "Liquidated Damages (LD): 0.05% of Contract Price per day of delay, maximum cap at 10% of total contract value.",
                "Force Majeure: Contractor exempt from delays caused by earthquakes, cyclones, or declared pandemics lasting more than 14 continuous days.",
                "Quality Compliance: All materials must conform to IRC SP:73 and MoRTH specifications. Non-compliance attracts 2% deduction.",
                "Payment Terms: Running Account bills processed within 30 days of certification by Independent Engineer."
            ],
            "dpr_trajectory": [2.0, 3.0, 2.5, 1.5, 3.0, 2.0],  # Ahead of schedule
        },
        {
            "name": "Bharatmala Rajasthan Desert Highway NH-15",
            "type": "HAM Contract",
            "cost": 1800,
            "state": "Rajasthan",
            "milestones": [
                ("Preliminary Survey & Design", 1, 2, 15),
                ("Utility Shifting & Land Handover", 2, 3, 15),
                ("Subgrade & Drainage Construction", 3, 7, 25),
                ("Base Course & WBM", 7, 12, 20),
                ("Surface Course & Marking", 12, 16, 15),
                ("Testing & Commissioning", 16, 18, 10),
            ],
            "materials": [("Cement PPC", "45,000 Tons"), ("Steel Reinforcement", "18,000 Tons"), ("WBM Aggregate", "180,000 Cu.m")],
            "clauses": [
                "LD Clause: Penalty of 0.04% per day for intermediate milestone failure, capped at 5%.",
                "Payment: 40% during construction, 60% as annuity over 15 years post-COD.",
                "Termination: Authority may terminate for persistent default exceeding 90 days continuous suspension.",
                "Escalation: Price adjustment formula applicable for cement and steel only, indexed to WPI."
            ],
            "dpr_trajectory": [1.5, 2.0, 1.0, 2.5, 1.5, 3.0],
        },
        {
            "name": "Smart City Pune Ring Road Corridor",
            "type": "PPP Agreement",
            "cost": 920,
            "state": "Maharashtra",
            "milestones": [
                ("Detailed Project Report", 1, 2, 10),
                ("Environmental & Forest Clearance", 2, 4, 15),
                ("Earthwork & Box Culverts", 4, 8, 30),
                ("Road Pavement & Signage", 8, 12, 25),
                ("Smart Infrastructure & ITS", 12, 15, 15),
                ("Handover & Defect Liability", 15, 16, 5),
            ],
            "materials": [("Cement", "22,000 Tons"), ("Steel", "8,500 Tons"), ("Bitumen", "5,200 Tons")],
            "clauses": [
                "LD: 0.05% per day, max 10%. Grace period of 30 days for monsoon months (June-September).",
                "Quality: Third-party audit every quarter. Failure attracts 1% penalty per non-compliance."
            ],
            "dpr_trajectory": [1.0, 1.5, 2.0, 1.0, 2.5, 1.5],
        },
    ],
    "2_LOW_RISK": [
        {
            "name": "Delhi Metro Phase IV Extension Line-8",
            "type": "EPC Contract",
            "cost": 5800,
            "state": "Delhi",
            "milestones": [
                ("Geotechnical Survey & Utility Mapping", 1, 3, 10),
                ("Station Box Excavation", 3, 8, 20),
                ("Tunnel Boring (TBM)", 6, 14, 30),
                ("Track Laying & OHE", 14, 18, 20),
                ("Station Finishing & MEP", 16, 22, 15),
                ("Testing & Commissioning", 22, 24, 5),
            ],
            "materials": [("Cement OPC 53", "180,000 Tons"), ("Steel TMT", "95,000 Tons"), ("Precast Segments", "45,000 Rings"), ("Copper OHE Wire", "2,500 Tons")],
            "clauses": [
                "LD: 0.05% per day delay, max 10% of contract value. Applicable from Scheduled Completion Date.",
                "Variation: No variation exceeding 15% of original scope without DMRC Board approval.",
                "Force Majeure: Includes bandhs, riots, and government-ordered lockdowns.",
                "Defect Liability: 24-month DLP from date of completion certificate."
            ],
            "dpr_trajectory": [-2.0, -3.0, -4.0, -3.5, -2.0, -1.5],
        },
        {
            "name": "Chennai Port-Maduravoyal Elevated Corridor",
            "type": "HAM Contract",
            "cost": 3200,
            "state": "Tamil Nadu",
            "milestones": [
                ("ROW & Utility Shifting", 1, 4, 15),
                ("Foundation & Pile Work", 4, 10, 25),
                ("Pier & Pier Cap", 10, 16, 25),
                ("Superstructure Erection", 14, 20, 20),
                ("Deck Finishing & Railing", 20, 23, 10),
                ("Load Testing & Handover", 23, 24, 5),
            ],
            "materials": [("Cement", "120,000 Tons"), ("Steel", "52,000 Tons"), ("Pre-stressed Cables", "3,200 Tons")],
            "clauses": [
                "LD: 0.05% per day, max 10%. Intermediate milestone LD: 0.02% per day.",
                "Coastal Zone Regulation: CRZ-III compliance mandatory. Violation attracts immediate stop-work order.",
                "Payment: Quarterly installments based on certified progress by IE."
            ],
            "dpr_trajectory": [-1.5, -2.5, -3.0, -4.0, -2.5, -1.0],
        },
        {
            "name": "PWD Jaipur Elevated Bridge Corridor",
            "type": "EPC Contract",
            "cost": 1400,
            "state": "Rajasthan",
            "milestones": [
                ("Site Clearance & Diversion", 1, 2, 10),
                ("Pile Foundation", 2, 6, 25),
                ("Pier & Abutment", 6, 10, 25),
                ("Girder Launching", 10, 14, 20),
                ("Deck Slab & Wearing Course", 14, 17, 15),
                ("Approach Road & Handover", 17, 18, 5),
            ],
            "materials": [("Cement", "38,000 Tons"), ("Steel", "16,000 Tons"), ("Bitumen", "3,500 Tons")],
            "clauses": [
                "LD: 0.04% per day. Total LD cap 8%.",
                "Termination: PWD may terminate if contractor abandons work for 15 consecutive days."
            ],
            "dpr_trajectory": [-1.0, -2.0, -3.5, -2.0, -1.5, -1.0],
        },
    ],
    "3_MEDIUM_RISK": [
        {
            "name": "Hyderabad Outer Ring Road Expansion BOT",
            "type": "BOT Toll Contract",
            "cost": 4200,
            "state": "Telangana",
            "milestones": [
                ("Design & Survey", 1, 3, 10),
                ("Land Acquisition (Forest)", 3, 8, 20),
                ("Earthwork & Drainage", 6, 12, 25),
                ("Pavement Construction", 12, 18, 25),
                ("Toll Plaza & ITS", 18, 22, 15),
                ("Commercial Operation Date", 22, 24, 5),
            ],
            "materials": [("Cement", "95,000 Tons"), ("Steel", "42,000 Tons"), ("Bitumen", "22,000 Tons"), ("Aggregate", "320,000 Cu.m")],
            "clauses": [
                "LD: 0.05% per day, max 10%. Applicable if COD delayed beyond Scheduled COD.",
                "Forest Clearance: Stage-I FC must be obtained before earthwork in notified forest patches. Delay in FC is NOT Force Majeure.",
                "Toll Collection: Concessionaire bears traffic risk. Minimum guaranteed annuity NOT applicable.",
                "Termination for Convenience: Authority may terminate with 90-day notice, compensation at 90% of outstanding debt."
            ],
            "dpr_trajectory": [-2.0, -5.0, -10.0, -12.0, -8.0, -6.0],
        },
        {
            "name": "Mumbai Coastal Road Tunnel Section",
            "type": "EPC Contract",
            "cost": 9500,
            "state": "Maharashtra",
            "milestones": [
                ("TBM Procurement & Assembly", 1, 4, 10),
                ("Cut & Cover Section", 3, 8, 15),
                ("Tunnel Boring (2.8 km)", 6, 16, 35),
                ("Internal Finishing & Ventilation", 14, 20, 20),
                ("Approach Roads & Interchanges", 18, 22, 15),
                ("Safety Audit & Handover", 22, 24, 5),
            ],
            "materials": [("Cement", "250,000 Tons"), ("Steel", "110,000 Tons"), ("Precast Segments", "65,000 Rings"), ("Shotcrete", "45,000 Cu.m")],
            "clauses": [
                "LD: 0.05% per day delay. Given Rs 9,500 Cr value, daily LD = Rs 4.75 Cr.",
                "Monsoon Clause: Strict monsoon delay penalties apply. No monsoon extension for tunnel works.",
                "CRZ Compliance: Mandatory CRZ-I clearance. Any violation triggers immediate suspension and penalty.",
                "Insurance: All-risk insurance of 110% contract value mandatory throughout construction."
            ],
            "dpr_trajectory": [-1.0, -4.0, -8.0, -14.0, -11.0, -9.0],
        },
        {
            "name": "Lucknow Metro Phase II Corridor",
            "type": "PPP Agreement",
            "cost": 6200,
            "state": "Uttar Pradesh",
            "milestones": [
                ("Utility Shifting & Traffic Diversion", 1, 4, 10),
                ("Station Excavation", 3, 8, 20),
                ("Viaduct Construction", 6, 14, 30),
                ("Track & Signaling", 14, 20, 20),
                ("Station Architecture & MEP", 18, 22, 15),
                ("Trial Runs & Safety Certification", 22, 24, 5),
            ],
            "materials": [("Cement", "160,000 Tons"), ("Steel", "72,000 Tons"), ("Pre-stressed Girders", "8,500 Units")],
            "clauses": [
                "LD: 0.05% per day, max 10%. Utility shifting delays by government agencies excluded.",
                "Payment: Monthly RA bills within 45 days of IE certification.",
                "Dispute Resolution: 3-tier mechanism - IE Decision, DRB, then Arbitration under Indian Arbitration Act."
            ],
            "dpr_trajectory": [-2.0, -6.0, -9.0, -12.0, -10.0, -7.0],
        },
    ],
    "4_HIGH_RISK": [
        {
            "name": "Kochi Metro Phase III Underground Extension",
            "type": "EPC Contract",
            "cost": 4500,
            "state": "Kerala",
            "milestones": [
                ("Utility Shifting", 1, 4, 10),
                ("Diaphragm Wall Construction", 3, 8, 20),
                ("Tunnel Boring", 6, 16, 30),
                ("Station Box & Track", 14, 20, 20),
                ("Systems Integration", 18, 22, 15),
                ("Commissioning", 22, 24, 5),
            ],
            "materials": [("Cement", "140,000 Tons"), ("Steel", "62,000 Tons"), ("TBM Segments", "35,000 Rings")],
            "clauses": [
                "Strict LD: 0.05% per day of delay. With Rs 4,500 Cr value, daily LD = Rs 2.25 Cr. Maximum cap 10%.",
                "No Price Escalation: Contract is FIXED PRICE. No escalation allowed for any material including steel and cement.",
                "Termination for Default: KMRL may terminate if work suspended for 30 continuous days without Force Majeure justification.",
                "Performance Security: 10% of contract value as Performance Bank Guarantee, valid until DLP completion."
            ],
            "dpr_trajectory": [-3.0, -8.0, -18.0, -25.0, -30.0, -28.0],
        },
        {
            "name": "NHAI Guwahati-Shillong Expressway Bridge Corridor",
            "type": "EPC Contract",
            "cost": 3200,
            "state": "Assam",
            "milestones": [
                ("Survey & Foundation Design", 1, 3, 10),
                ("Pile Foundation (River Crossing)", 3, 10, 25),
                ("Pier Construction", 8, 14, 25),
                ("Superstructure Erection", 12, 18, 20),
                ("Approach & Link Roads", 16, 20, 15),
                ("Load Testing & Handover", 20, 22, 5),
            ],
            "materials": [("Cement", "82,000 Tons"), ("Steel", "38,000 Tons"), ("Bitumen", "12,000 Tons")],
            "clauses": [
                "LD: 0.05% per day. No price escalation allowed for steel and cement despite NE remoteness.",
                "Monsoon Restriction: Work suspension mandatory during extreme flood events (above HFL). No time extension for seasonal floods.",
                "Authority Delay: Site handover delay by Authority will NOT waive the Scheduled Completion Date.",
                "Retention Money: 5% retention from each RA bill, released after successful DLP."
            ],
            "dpr_trajectory": [-5.0, -10.0, -20.0, -28.0, -32.0, -35.0],
        },
        {
            "name": "Kolkata East-West River Tunnel Metro",
            "type": "HAM Contract",
            "cost": 5100,
            "state": "West Bengal",
            "milestones": [
                ("TBM Procurement", 1, 4, 10),
                ("Launch Shaft Construction", 3, 8, 15),
                ("River Crossing Tunnel", 6, 16, 35),
                ("Station Construction", 12, 20, 20),
                ("Track & Systems", 18, 22, 15),
                ("Commissioning", 22, 24, 5),
            ],
            "materials": [("Cement", "165,000 Tons"), ("Steel", "75,000 Tons"), ("Bentonite Slurry", "8,000 Tons")],
            "clauses": [
                "LD: 0.05% per day, max 10%. River crossing section carries 2x LD multiplier.",
                "Safety: Zero fatality policy. Any fatality triggers mandatory 7-day safety audit suspension.",
                "Geological Risk: Contractor bears full geological risk. No additional payment for unforeseen ground conditions."
            ],
            "dpr_trajectory": [-4.0, -12.0, -22.0, -30.0, -35.0, -33.0],
        },
    ],
    "5_CRITICAL_RISK": [
        {
            "name": "Bengaluru-Chennai Expressway Phase III",
            "type": "EPC Contract",
            "cost": 18500,
            "state": "Karnataka",
            "milestones": [
                ("Mobilization & Survey", 1, 3, 5),
                ("Land Acquisition (12 Districts)", 2, 10, 20),
                ("Earthwork & Major Bridges", 6, 18, 30),
                ("Pavement & Structures", 14, 24, 25),
                ("ITS & Toll Systems", 22, 28, 15),
                ("Final Inspection & COD", 28, 30, 5),
            ],
            "materials": [("Cement", "450,000 Tons"), ("Steel", "200,000 Tons"), ("Bitumen", "95,000 Tons"), ("Aggregate", "1,200,000 Cu.m")],
            "clauses": [
                "LD: 0.05% per day. With Rs 18,500 Cr, daily LD = Rs 9.25 Cr. MAXIMUM EXPOSURE Rs 1,850 Cr.",
                "Contract Termination: NHAI may terminate upon 30 days continuous suspension of work without valid Force Majeure.",
                "Encashment: Performance BG of Rs 1,850 Cr to be encashed upon termination for Contractor Default.",
                "Blacklisting: Contractor and all associated entities blacklisted for 5 years upon termination for default.",
                "No Claim Certificate: Contractor must issue No Claim Certificate at each milestone. Future claims barred."
            ],
            "dpr_trajectory": [-5.0, -15.0, -30.0, -45.0, -55.0, -60.0],
        },
        {
            "name": "Patna Metro Rail Phase I",
            "type": "EPC Contract",
            "cost": 14200,
            "state": "Bihar",
            "milestones": [
                ("Utility Shifting & Traffic Management", 1, 4, 10),
                ("Depot Land Development", 3, 8, 15),
                ("Viaduct & Station Construction", 6, 18, 35),
                ("Track & Electrical Systems", 16, 22, 20),
                ("Rolling Stock Integration", 20, 26, 15),
                ("Safety Certification & Revenue Service", 26, 30, 5),
            ],
            "materials": [("Cement", "320,000 Tons"), ("Steel", "145,000 Tons"), ("Pre-stressed Girders", "12,000 Units"), ("Copper Cable", "4,500 Tons")],
            "clauses": [
                "LD: 0.05% per day. Daily penalty Rs 7.1 Cr.",
                "Severe Default Penalty: Safety or quality audit failure triggers immediate show-cause and potential termination.",
                "Subcontractor Liability: Main contractor liable for all subcontractor defaults. No pass-through of liability.",
                "Completion Guarantee: Unconditional, irrevocable Bank Guarantee of 15% contract value.",
                "Insurance: Comprehensive All-Risk policy of 120% contract value mandatory."
            ],
            "dpr_trajectory": [-8.0, -20.0, -35.0, -48.0, -58.0, -62.0],
        },
        {
            "name": "Bhopal Smart City Integrated Hub",
            "type": "Smart City PPP",
            "cost": 2200,
            "state": "Madhya Pradesh",
            "milestones": [
                ("DPR Finalization & Financial Closure", 1, 3, 15),
                ("Site Development & Services", 3, 6, 20),
                ("Building Construction", 6, 14, 30),
                ("Smart Infrastructure & IoT", 12, 18, 20),
                ("Testing & Commissioning", 18, 20, 10),
                ("Occupancy & Handover", 20, 22, 5),
            ],
            "materials": [("Cement", "55,000 Tons"), ("Steel", "24,000 Tons"), ("Smart Sensors", "15,000 Units"), ("Fiber Optic Cable", "250 Km")],
            "clauses": [
                "Financial Closure: Immediate cancellation if financial closure not achieved within 60 days of Agreement Date.",
                "LD: 0.05% per day. Applicable from Day 1 post milestone deadline.",
                "Technology Compliance: All IoT infrastructure must meet ISO 27001 and BIS standards.",
                "Termination: SPV Board may terminate with 15-day notice for any material default.",
                "Penalty Escalation: LD doubles to 0.10% per day if delay exceeds 90 days."
            ],
            "dpr_trajectory": [-10.0, -25.0, -40.0, -52.0, -60.0, -65.0],
        },
    ]
}


def generate_pdf(filepath, title, content_lines):
    c = canvas.Canvas(str(filepath), pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, title)
    c.setFont("Helvetica", 10)
    y = 710
    for line in content_lines:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 750
        # Truncate very long lines
        c.drawString(50, y, str(line)[:95])
        y -= 16
    c.save()


def create_dataset():
    if os.path.exists(SAMPLE_DIR):
        shutil.rmtree(SAMPLE_DIR)
    os.makedirs(SAMPLE_DIR)

    for category_id, projects in PROJECTS.items():
        cat_dir = SAMPLE_DIR / category_id
        os.makedirs(cat_dir)

        for proj in projects:
            folder = proj["name"].replace(" ", "_").replace("/", "_")
            proj_dir = cat_dir / folder
            os.makedirs(proj_dir)

            # ---- CONTRACT PDF ----
            contract_lines = [
                f"PROJECT: {proj['name']}",
                f"TYPE: {proj['type']}",
                f"VALUE: Rs. {proj['cost']} Crores",
                f"STATE: {proj['state']}",
                "",
                "=" * 60,
                "SECTION 1: OBLIGATIONS & MILESTONES",
                "=" * 60,
            ]
            for ms in proj["milestones"]:
                contract_lines.append(f"  - {ms[0]}: Month {ms[1]} to Month {ms[2]} (Weightage: {ms[3]}%)")

            contract_lines.extend(["", "=" * 60, "SECTION 2: MATERIAL REQUIREMENTS", "=" * 60])
            for mat in proj["materials"]:
                contract_lines.append(f"  - {mat[0]}: {mat[1]}")

            contract_lines.extend(["", "=" * 60, "SECTION 3: KEY CONTRACTUAL CLAUSES", "=" * 60])
            for cl in proj["clauses"]:
                contract_lines.append(f"  - {cl}")

            generate_pdf(proj_dir / f"{folder}_Contract.pdf", "EPC/HAM AGREEMENT DOCUMENT", contract_lines)

            # ---- 6 MONTHLY DPR PDFs ----
            reports_dir = proj_dir / "monthly_reports"
            os.makedirs(reports_dir)

            planned_prog = 0.0
            actual_prog = 0.0

            for month in range(1, 7):
                planned_prog += 16.6
                deviation = proj["dpr_trajectory"][month - 1]
                actual_prog = planned_prog + deviation
                actual_prog = max(0, min(100, actual_prog))

                # Generate realistic issues based on category
                if "NO_RISK" in category_id:
                    issues = [
                        "None. Progressing ahead of schedule.",
                        "Material supply stable. Quality checks passed."
                    ]
                elif "LOW_RISK" in category_id:
                    issues = [
                        f"Minor delay in equipment mobilization (Month {month}).",
                        "Recoverable by adding weekend shifts.",
                        "No penalty threshold breached."
                    ]
                elif "MEDIUM_RISK" in category_id:
                    if month >= 3:
                        issues = [
                            f"Environmental clearance pending for forest patch (Month {month}).",
                            f"Schedule deviation: {abs(deviation):.1f}% behind baseline.",
                            "Contractor requested time extension. Under review.",
                            "Material shortage: Cement delivery delayed by 12 days."
                        ]
                    else:
                        issues = ["Normal mobilization. Minor ROW issues in Sector B."]
                elif "HIGH_RISK" in category_id:
                    if month >= 3:
                        issues = [
                            f"MAJOR DELAY: {abs(deviation):.1f}% behind schedule.",
                            "Steel price escalation of 22% - no escalation clause in contract.",
                            f"Estimated {int(abs(deviation) * 1.5)} days behind completion target.",
                            "LD Penalty warning issued by Authority.",
                            "Subcontractor mobilization failure on pile foundation."
                        ]
                    else:
                        issues = [
                            "Initial delays in ROW handover by Authority.",
                            "Equipment procurement delayed due to import clearance."
                        ]
                else:  # CRITICAL
                    if month >= 3:
                        issues = [
                            f"CRITICAL CONTRACT BREACH: {abs(deviation):.1f}% behind schedule.",
                            "Earthwork halted for 30+ days due to land disputes.",
                            "Notice of Intention to Terminate issued by Authority.",
                            f"LD Exposure: Rs {proj['cost'] * 0.0005 * int(abs(deviation) * 1.5):.1f} Cr accumulated.",
                            "Performance Bank Guarantee encashment proceedings initiated.",
                            "Labour strike at 3 work fronts. Subcontractor abandoned site."
                        ]
                    else:
                        issues = [
                            "Significant delay in financial closure.",
                            "Land acquisition protests in 4 villages.",
                            "Slow mobilization. Equipment not deployed as per schedule."
                        ]

                report_lines = [
                    f"MONTHLY PROGRESS REPORT (DPR) - MONTH {month}",
                    f"Project: {proj['name']}",
                    f"Reporting Period: Month {month}",
                    "",
                    "=" * 60,
                    "PROGRESS SUMMARY",
                    "=" * 60,
                    f"Planned Progress: {planned_prog:.1f}%",
                    f"Actual Progress: {actual_prog:.1f}%",
                    f"Deviation: {deviation:.1f}%",
                    "",
                    "=" * 60,
                    "ISSUES & RISKS REPORTED",
                    "=" * 60,
                ]
                for iss in issues:
                    report_lines.append(f"- {iss}")

                generate_pdf(reports_dir / f"Month_{month}_Progress_Report.pdf",
                             f"DPR Month {month} - {proj['name'][:40]}", report_lines)

    print(f"Successfully generated 15-project dataset in {SAMPLE_DIR}")


if __name__ == "__main__":
    create_dataset()
