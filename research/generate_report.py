from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import date

OUTPUT = "C:/users/25badmin/projects/accounts-payable-research/AP_AI_Software_Research_2026.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    topMargin=0.75 * inch,
    bottomMargin=0.75 * inch,
    leftMargin=0.85 * inch,
    rightMargin=0.85 * inch,
)

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(
    name="CoverTitle",
    fontSize=28,
    leading=34,
    alignment=TA_CENTER,
    textColor=HexColor("#1a365d"),
    spaceAfter=12,
    fontName="Helvetica-Bold",
))
styles.add(ParagraphStyle(
    name="CoverSubtitle",
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    textColor=HexColor("#4a5568"),
    spaceAfter=6,
    fontName="Helvetica",
))
styles.add(ParagraphStyle(
    name="SectionHead",
    fontSize=18,
    leading=22,
    textColor=HexColor("#1a365d"),
    spaceBefore=18,
    spaceAfter=10,
    fontName="Helvetica-Bold",
))
styles.add(ParagraphStyle(
    name="SubHead",
    fontSize=13,
    leading=16,
    textColor=HexColor("#2b6cb0"),
    spaceBefore=12,
    spaceAfter=6,
    fontName="Helvetica-Bold",
))
styles.add(ParagraphStyle(
    name="BodyText2",
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=6,
    fontName="Helvetica",
))
styles.add(ParagraphStyle(
    name="BulletCustom",
    fontSize=10,
    leading=14,
    leftIndent=20,
    spaceAfter=4,
    fontName="Helvetica",
    bulletIndent=8,
))
styles.add(ParagraphStyle(
    name="TableHeader",
    fontSize=9,
    leading=12,
    textColor=HexColor("#ffffff"),
    fontName="Helvetica-Bold",
    alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="TableCell",
    fontSize=8.5,
    leading=11,
    fontName="Helvetica",
    alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="Footer",
    fontSize=8,
    leading=10,
    textColor=HexColor("#718096"),
    alignment=TA_CENTER,
))

story = []

# ---------- COVER PAGE ----------
story.append(Spacer(1, 2 * inch))
story.append(Paragraph("AI-Based Accounts Payable<br/>Software Research Report", styles["CoverTitle"]))
story.append(Spacer(1, 0.3 * inch))
story.append(HRFlowable(width="60%", color=HexColor("#2b6cb0"), thickness=2))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("Market Analysis &amp; Competitive Landscape", styles["CoverSubtitle"]))
story.append(Paragraph("Construction Industry Focus", styles["CoverSubtitle"]))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph(f"Prepared: {date.today().strftime('%B %d, %Y')}", styles["CoverSubtitle"]))
story.append(Paragraph("Confidential - Internal Use Only", styles["CoverSubtitle"]))
story.append(PageBreak())

# ---------- TABLE OF CONTENTS ----------
story.append(Paragraph("Table of Contents", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.15 * inch))
toc_items = [
    "1. Executive Summary",
    "2. Market Overview &amp; Trends",
    "3. Leading AI AP Software Vendors",
    "4. Construction-Specific Solutions",
    "5. Vendor Comparison Matrix",
    "6. Pricing Analysis",
    "7. Key AI Capabilities Breakdown",
    "8. Opportunities for Custom Development",
    "9. Recommendations",
    "10. Sources",
]
for item in toc_items:
    story.append(Paragraph(item, styles["BodyText2"]))
story.append(PageBreak())

# ---------- 1. EXECUTIVE SUMMARY ----------
story.append(Paragraph("1. Executive Summary", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))
story.append(Paragraph(
    "The accounts payable automation market is experiencing rapid growth, projected to reach $1.9 billion "
    "by 2025 with a compound annual growth rate (CAGR) of 17%. In 2024, Gartner reported that 58% of "
    "finance functions were already using AI -- a significant leap from prior years. The shift from basic "
    "OCR to true cognitive automation with AI agents represents the next frontier, with platforms now "
    "capable of understanding invoices rather than just reading them, detecting fraud patterns, predicting "
    "GL codes, and managing complex approval workflows autonomously.",
    styles["BodyText2"]
))
story.append(Paragraph(
    "For a 500-employee multi-trade construction company, AP automation is particularly impactful due to the "
    "volume and complexity of invoices from subcontractors, material suppliers, and service vendors across "
    "mechanical, electrical, plumbing, service, underground, and manufacturing divisions. Construction-specific "
    "challenges include AIA billing formats (G702/G703), lien waiver tracking, retention management, "
    "job costing across projects, and certified payroll compliance.",
    styles["BodyText2"]
))
story.append(Paragraph(
    "This report surveys 15+ AI-based AP automation vendors, with special attention to construction industry "
    "applicability, AI agent capabilities, pricing models, and integration options. The goal is to inform "
    "a build-vs-buy decision for a custom AI AP solution.",
    styles["BodyText2"]
))

# ---------- 2. MARKET OVERVIEW ----------
story.append(Paragraph("2. Market Overview &amp; Trends", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Market Size &amp; Growth", styles["SubHead"]))
story.append(Paragraph(
    "The AP automation market is valued at approximately $1.9B (2025) with 17% CAGR. "
    "Key drivers include labor cost reduction, error elimination, and regulatory compliance demands. "
    "AI-first solutions are displacing traditional OCR+rules-based systems.",
    styles["BodyText2"]
))

story.append(Paragraph("The Shift to Agentic AI", styles["SubHead"]))
story.append(Paragraph(
    "The 2025-2026 period marks a shift from assistive AI (suggestions, auto-fill) to agentic AI -- "
    "autonomous agents that process invoices end-to-end with minimal human intervention. "
    "Companies report an average 80% ROI on agentic AP deployments. Leading vendors like Ramp now deploy "
    "four distinct AI agents: invoice coding, fraud monitoring, approval documentation, and payment execution.",
    styles["BodyText2"]
))

story.append(Paragraph("Key Industry Metrics", styles["SubHead"]))
metrics = [
    ["Metric", "Manual Process", "AI Automated"],
    ["Cost per invoice", "$10-$30", "$1-$4"],
    ["Processing time per invoice", "15-25 minutes", "1-3 minutes"],
    ["Error rate", "3-5%", "<1%"],
    ["First-time match rate", "~50%", "97%+"],
    ["Straight-through processing", "<20%", "85%+"],
]
t = Table(metrics, colWidths=[2.2 * inch, 2 * inch, 2 * inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f7fafc")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.15 * inch))

# ---------- 3. LEADING VENDORS ----------
story.append(Paragraph("3. Leading AI AP Software Vendors", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

vendors = [
    {
        "name": "Stampli",
        "tagline": "AP Automation Built by AP Professionals",
        "desc": (
            "Stampli is powered by Billy the Bot, an agentic AI assistant trained on over $90 billion "
            "in annual spend and 83 million hours of P2P workflow experience. Billy delivers 97-100% "
            "accuracy in PO matching by replicating human judgment in complex matching scenarios. The "
            "platform provides automated invoice capture via advanced OCR, intelligent GL coding based "
            "on historical patterns, configurable multi-level approval workflows, duplicate invoice "
            "detection, and automated exception handling. Stampli recently expanded to global payments "
            "supporting 150+ countries."
        ),
        "ai": "Agentic AI (Billy the Bot), ML-based GL coding, anomaly detection",
        "best_for": "Mid-market to enterprise; companies needing invoice-centric AP with strong AI",
        "rating": "4.6/5 (G2)",
    },
    {
        "name": "Ramp",
        "tagline": "#1 Easiest AP Software (G2)",
        "desc": (
            "Ramp runs on autonomous technology with four AI agents managing invoice coding, fraud "
            "monitoring, approval documentation, and card payment execution. OCR achieves 99% accuracy "
            "capturing line-item details, processing invoices 2.4x faster than traditional AP platforms. "
            "Supports ACH, card, check, and wire payments with deep integrations into NetSuite, "
            "QuickBooks, and Xero."
        ),
        "ai": "4 autonomous AI agents, 99% OCR accuracy, real-time fraud detection",
        "best_for": "Tech-savvy mid-market companies wanting unified AP, cards, and expense management",
        "rating": "4.8/5 (G2)",
    },
    {
        "name": "Vic.ai",
        "tagline": "AI-First Invoice Processing",
        "desc": (
            "Vic.ai is a pure AI-first AP platform that achieves 5X efficiency gains, 99% accuracy, "
            "and 85% no-touch (straight-through) invoice processing. Unlike competitors relying on "
            "templates, Vic.ai eliminates templating entirely through deep learning. The platform "
            "includes VicInbox for email invoice capture and VicCard for virtual card payments. "
            "Strong focus on autonomous processing with human-in-the-loop for exceptions only."
        ),
        "ai": "Deep learning (no templates), autonomous coding, PO matching, anomaly detection",
        "best_for": "Organizations seeking highest automation rates with minimal human intervention",
        "rating": "4.5/5 (G2)",
    },
    {
        "name": "Tipalti",
        "tagline": "End-to-End Global Payables Platform",
        "desc": (
            "Tipalti is a fintech unicorn (valued at ~$8.3B) specializing in global payables automation "
            "for companies managing hundreds or thousands of suppliers across multiple countries. Combines "
            "supplier onboarding, invoice processing, tax compliance (1099, W-8/W-9), and mass payment "
            "execution. Supports 196 countries and 120 currencies. OCR and ML for invoice data extraction "
            "and coding."
        ),
        "ai": "OCR/ML invoice extraction, automated tax compliance, payment optimization",
        "best_for": "Companies with large international vendor networks and complex tax compliance needs",
        "rating": "4.5/5 (G2)",
    },
    {
        "name": "BILL (Bill.com)",
        "tagline": "Cloud-Based AP/AR Automation",
        "desc": (
            "BILL is a widely adopted cloud-based AP and AR automation platform, primarily targeting "
            "small to mid-sized businesses. AI automates data capture and bill pay to reduce manual work "
            "and errors. The platform added a Procurement module in Q1 2025. Strong integrations with "
            "QuickBooks, Xero, and NetSuite. Over 400,000 businesses use BILL."
        ),
        "ai": "AI data capture, automated bill pay, smart approval routing",
        "best_for": "Small to mid-sized businesses wanting simple, affordable AP automation",
        "rating": "4.3/5 (G2)",
    },
    {
        "name": "Basware",
        "tagline": "Enterprise-Grade AP Automation",
        "desc": (
            "Basware is an enterprise AP automation platform with AI trained on over 2 billion invoices "
            "globally. Handles invoice capture, workflow automation, payment processing, and supplier "
            "management at scale. Strong compliance and audit trail capabilities. Recognized as a "
            "leader in multiple analyst reports."
        ),
        "ai": "AI trained on 2B+ invoices, predictive coding, automated matching, compliance AI",
        "best_for": "Large enterprises with complex global AP operations",
        "rating": "4.2/5 (G2)",
    },
    {
        "name": "Yooz",
        "tagline": "AI-Powered Fraud Detection in AP",
        "desc": (
            "Yooz specializes in AI-driven fraud detection, flagging suspicious invoices, detecting "
            "anomalies, identifying irregular vendor payments, and using ML to analyze invoice metadata "
            "for inconsistencies. Strong purchase-to-pay automation with cloud-based deployment. "
            "Over 200 ERP integrations available."
        ),
        "ai": "AI fraud detection, ML anomaly analysis, automated metadata validation",
        "best_for": "Organizations prioritizing fraud prevention and compliance",
        "rating": "4.4/5 (G2), 8.6/10 (TrustRadius)",
    },
    {
        "name": "Medius",
        "tagline": "Gartner Magic Quadrant Leader for AP",
        "desc": (
            "Medius is positioned as a Leader in Gartner's Magic Quadrant for Accounts Payable "
            "Applications. Provides end-to-end AP automation with AI-powered invoice processing, "
            "spend management, and payment solutions. Strong analytics and reporting capabilities."
        ),
        "ai": "AI invoice processing, predictive analytics, automated spend categorization",
        "best_for": "Enterprise organizations seeking a Gartner-validated AP leader",
        "rating": "4.3/5 (G2)",
    },
    {
        "name": "Hypatos",
        "tagline": "AI Agents for Document Processing",
        "desc": (
            "Hypatos automates invoices, POs, and payments using dedicated AI Agents, cutting DPO "
            "and manual effort with end-to-end AP document processing. Recognized as a Representative "
            "Vendor in Gartner's Market Guide for AP Invoice Automation. Strong focus on SAP integration "
            "with generative AI capabilities for auto-posting."
        ),
        "ai": "Agentic AI for document processing, generative AI for SAP auto-posting",
        "best_for": "SAP-centric enterprises needing intelligent document automation",
        "rating": "4.4/5 (G2)",
    },
    {
        "name": "Coupa",
        "tagline": "Procure-to-Pay Suite",
        "desc": (
            "Coupa is a comprehensive procure-to-pay suite where top-performing companies achieve a "
            "97.1% first-time invoice match rate. Provides AI-powered invoice processing, supplier "
            "management, procurement, and treasury management in a unified platform. Strong enterprise "
            "adoption with Fortune 500 clients."
        ),
        "ai": "AI matching (97.1% first-time rate), community intelligence, spend analytics",
        "best_for": "Large enterprises wanting unified procurement and AP in one platform",
        "rating": "4.2/5 (G2)",
    },
    {
        "name": "HighRadius",
        "tagline": "AI-Powered Financial Operations",
        "desc": (
            "HighRadius offers electronic invoice capture, automated invoice matching, workflow "
            "management, and deep ERP integration. Part of a broader autonomous finance platform "
            "covering AR, treasury, and AP. Uses AI to predict and automate financial close processes."
        ),
        "ai": "AI invoice capture, predictive matching, autonomous workflow management",
        "best_for": "Large enterprises seeking a unified order-to-cash and procure-to-pay platform",
        "rating": "4.3/5 (G2)",
    },
]

for v in vendors:
    story.append(Paragraph(f'{v["name"]} -- {v["tagline"]}', styles["SubHead"]))
    story.append(Paragraph(v["desc"], styles["BodyText2"]))
    story.append(Paragraph(f'<b>AI Capabilities:</b> {v["ai"]}', styles["BulletCustom"]))
    story.append(Paragraph(f'<b>Best For:</b> {v["best_for"]}', styles["BulletCustom"]))
    story.append(Paragraph(f'<b>Rating:</b> {v["rating"]}', styles["BulletCustom"]))
    story.append(Spacer(1, 0.08 * inch))

# ---------- 4. CONSTRUCTION-SPECIFIC ----------
story.append(PageBreak())
story.append(Paragraph("4. Construction-Specific Solutions", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Adaptive -- AI Native Construction Accounting", styles["SubHead"]))
story.append(Paragraph(
    "Adaptive is purpose-built for construction accounting with a team of AI agents that automate manual "
    "accounting work, reconcile financials with field updates, and deliver real-time financial control. "
    "The platform identifies overbilling, missing waivers, and unapproved scope in subcontractor invoices. "
    "Key features include AP management with AI-powered invoice processing and job costing, payment "
    "processing for vendors and subcontractors, AR/draw management for streamlined payment applications, "
    "and automated expense tracking with categorization and allocation.",
    styles["BodyText2"]
))
story.append(Paragraph(
    "Pricing starts at $575-$599/month based on annual revenue, with unlimited projects, users, payments, "
    "support, and training. Integrates with QuickBooks, banking systems, email platforms, and project "
    "management software.",
    styles["BodyText2"]
))

story.append(Paragraph("AvidXchange -- Middle Market AP Powerhouse", styles["SubHead"]))
story.append(Paragraph(
    "AvidXchange is a dominant player in middle-market AP automation, especially in real estate and "
    "construction. Features include lien waiver management for compliance, over 200 ERP integrations, "
    "and TimberScan/TimberScan Titanium -- purpose-built AP automation for Sage 300 Construction and "
    "Real Estate with PO matching, cost coding, and job-level visibility. Supports virtual credit card, "
    "ACH, and check payments.",
    styles["BodyText2"]
))
story.append(Paragraph(
    "Pricing starts at approximately $440/month with annual costs up to $13,000 depending on volume "
    "and modules selected. Uses a flexible modular pricing model.",
    styles["BodyText2"]
))

story.append(Paragraph("Itemize -- Agentic AI for Construction AP", styles["SubHead"]))
story.append(Paragraph(
    "Itemize focuses on how agentic AI reinvents accounts payable for construction firms, addressing "
    "pain points like multiple invoice sources and formats (paper, email, PDF, fax, EDI) from numerous "
    "subcontractors and suppliers. The platform emphasizes autonomous processing with construction-aware "
    "document understanding.",
    styles["BodyText2"]
))

story.append(Paragraph("Payra -- Construction Payment Acceleration", styles["SubHead"]))
story.append(Paragraph(
    "Payra assists construction and building materials suppliers in accepting digital payments (cards, "
    "ACH) and automates reconciliation inside legacy finance systems via AI-enabled technology. "
    "Focused specifically on getting construction firms paid faster.",
    styles["BodyText2"]
))

story.append(Paragraph("Construction-Specific AP Challenges", styles["SubHead"]))
construction_challenges = [
    "Multiple invoice formats: paper, email, PDF, fax, EDI from diverse subcontractors/suppliers",
    "AIA billing (G702/G703): standard progress billing format requiring specific field extraction",
    "Lien waiver tracking: conditional and unconditional waivers must be collected before payment",
    "Retention/retainage: typically 5-10% held until project completion or milestones",
    "Job costing: every expense must be coded to the correct project, phase, and cost code",
    "Change order management: tracking approved changes that affect original contract amounts",
    "Certified payroll and prevailing wage compliance on government projects",
    "Insurance certificate and W-9 tracking for subcontractor compliance",
    "Progress billing verification against actual work completed in the field",
]
for c in construction_challenges:
    story.append(Paragraph(f"&bull; {c}", styles["BulletCustom"]))

# ---------- 5. COMPARISON MATRIX ----------
story.append(PageBreak())
story.append(Paragraph("5. Vendor Comparison Matrix", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

hdr_style = ParagraphStyle("hdr", fontSize=7, leading=9, textColor=HexColor("#ffffff"), fontName="Helvetica-Bold")
cell_style = ParagraphStyle("cel", fontSize=7, leading=9, fontName="Helvetica")

comp_data = [
    [Paragraph("Vendor", hdr_style), Paragraph("AI Agents", hdr_style), Paragraph("OCR Accuracy", hdr_style),
     Paragraph("Construction Focus", hdr_style), Paragraph("ERP Integration", hdr_style),
     Paragraph("Global Pay", hdr_style), Paragraph("Starting Price", hdr_style)],
    [Paragraph("Stampli", cell_style), Paragraph("Yes (Billy)", cell_style), Paragraph("97-100%", cell_style),
     Paragraph("Partial", cell_style), Paragraph("Strong", cell_style),
     Paragraph("150+ countries", cell_style), Paragraph("Custom quote", cell_style)],
    [Paragraph("Ramp", cell_style), Paragraph("Yes (4 agents)", cell_style), Paragraph("99%", cell_style),
     Paragraph("No", cell_style), Paragraph("Strong", cell_style),
     Paragraph("Limited", cell_style), Paragraph("Free tier avail.", cell_style)],
    [Paragraph("Vic.ai", cell_style), Paragraph("Yes", cell_style), Paragraph("99%", cell_style),
     Paragraph("No", cell_style), Paragraph("Moderate", cell_style),
     Paragraph("Limited", cell_style), Paragraph("Custom quote", cell_style)],
    [Paragraph("Tipalti", cell_style), Paragraph("Partial", cell_style), Paragraph("High", cell_style),
     Paragraph("No", cell_style), Paragraph("Strong", cell_style),
     Paragraph("196 countries", cell_style), Paragraph("Custom quote", cell_style)],
    [Paragraph("BILL", cell_style), Paragraph("Basic", cell_style), Paragraph("Good", cell_style),
     Paragraph("No", cell_style), Paragraph("Good", cell_style),
     Paragraph("Limited", cell_style), Paragraph("~$45/mo", cell_style)],
    [Paragraph("Adaptive", cell_style), Paragraph("Yes", cell_style), Paragraph("High", cell_style),
     Paragraph("YES - Built for it", cell_style), Paragraph("QuickBooks", cell_style),
     Paragraph("No", cell_style), Paragraph("$575/mo", cell_style)],
    [Paragraph("AvidXchange", cell_style), Paragraph("Partial", cell_style), Paragraph("High", cell_style),
     Paragraph("YES - Strong", cell_style), Paragraph("200+ integrations", cell_style),
     Paragraph("Limited", cell_style), Paragraph("~$440/mo", cell_style)],
    [Paragraph("Basware", cell_style), Paragraph("Yes", cell_style), Paragraph("High", cell_style),
     Paragraph("No", cell_style), Paragraph("Enterprise", cell_style),
     Paragraph("Strong", cell_style), Paragraph("Custom quote", cell_style)],
    [Paragraph("Yooz", cell_style), Paragraph("Partial", cell_style), Paragraph("High", cell_style),
     Paragraph("No", cell_style), Paragraph("200+ integrations", cell_style),
     Paragraph("Limited", cell_style), Paragraph("Custom quote", cell_style)],
    [Paragraph("Hypatos", cell_style), Paragraph("Yes", cell_style), Paragraph("High", cell_style),
     Paragraph("No", cell_style), Paragraph("SAP focus", cell_style),
     Paragraph("Limited", cell_style), Paragraph("Custom quote", cell_style)],
    [Paragraph("Coupa", cell_style), Paragraph("Partial", cell_style), Paragraph("97%", cell_style),
     Paragraph("No", cell_style), Paragraph("Enterprise", cell_style),
     Paragraph("Strong", cell_style), Paragraph("$$$", cell_style)],
]

col_w = [0.85*inch, 0.85*inch, 0.75*inch, 1.05*inch, 0.95*inch, 0.85*inch, 0.9*inch]
t2 = Table(comp_data, colWidths=col_w)
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(t2)

# ---------- 6. PRICING ANALYSIS ----------
story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("6. Pricing Analysis", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Cost of Manual vs Automated AP Processing", styles["SubHead"]))
story.append(Paragraph(
    "Manual invoice processing costs $10-$30 per invoice (average ~$16), while automated processing "
    "reduces this to $1-$4 per invoice. For a 500-employee construction company processing an estimated "
    "2,000-5,000 invoices per month across all trades, the savings are substantial:",
    styles["BodyText2"]
))

pricing_data = [
    ["Scenario", "Monthly Invoices", "Cost/Invoice", "Monthly Cost", "Annual Cost"],
    ["Manual (current est.)", "3,500", "$16", "$56,000", "$672,000"],
    ["AI Automated", "3,500", "$3", "$10,500", "$126,000"],
    ["Annual Savings", "", "", "", "$546,000"],
]
t3 = Table(pricing_data, colWidths=[1.5*inch, 1.1*inch, 1*inch, 1.1*inch, 1.1*inch])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("BACKGROUND", (0, -1), (-1, -1), HexColor("#c6f6d5")),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -2), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t3)
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Software Licensing Cost Ranges", styles["SubHead"]))
story.append(Paragraph(
    "Annual software costs typically range from $2,000 to $50,000+ for mid-market solutions, with large "
    "enterprise AI-heavy deployments exceeding $100,000+/year. Construction-specific solutions like "
    "Adaptive start at ~$7,000/year, while AvidXchange ranges from ~$5,300 to $13,000/year. "
    "Even at the high end, software costs are a fraction of the labor savings.",
    styles["BodyText2"]
))

# ---------- 7. AI CAPABILITIES ----------
story.append(Paragraph("7. Key AI Capabilities Breakdown", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

capabilities = [
    ("Intelligent Document Processing (IDP)",
     "Advanced OCR combined with NLP and computer vision to extract data from invoices regardless of "
     "format -- paper scans, PDFs, photos, emails. Modern systems achieve 97-99% accuracy without "
     "templates, learning from each processed document."),
    ("Autonomous GL Coding",
     "AI predicts the correct general ledger account, cost code, job number, and cost category based "
     "on historical patterns, vendor history, and invoice content. Accuracy improves over time through "
     "reinforcement learning from user corrections."),
    ("Three-Way Matching",
     "Automated matching of invoices to purchase orders and receiving reports. AI handles fuzzy matching "
     "for partial shipments, price variances, and quantity discrepancies, flagging only true exceptions "
     "for human review."),
    ("Fraud Detection &amp; Anomaly Identification",
     "ML models trained on millions of transactions detect duplicate invoices, unusual vendor patterns, "
     "price anomalies, suspicious timing, and potential billing fraud. Real-time alerts prevent "
     "fraudulent payments before they occur."),
    ("Agentic Workflow Automation",
     "AI agents autonomously route invoices for approval based on amount, vendor, project, and cost type. "
     "Agents can send reminders, escalate overdue approvals, and even execute payments within authorized "
     "parameters without human intervention."),
    ("Predictive Analytics &amp; Cash Flow",
     "AI forecasts payment obligations, identifies early-pay discount opportunities, and optimizes "
     "payment timing for cash flow management. Predictive models help CFOs plan cash needs weeks in advance."),
]

for title, desc in capabilities:
    story.append(Paragraph(title, styles["SubHead"]))
    story.append(Paragraph(desc, styles["BodyText2"]))

# ---------- 8. CUSTOM DEVELOPMENT OPPORTUNITY ----------
story.append(PageBreak())
story.append(Paragraph("8. Opportunities for Custom Development", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "While commercial solutions cover broad AP automation needs, a custom-built AI AP system offers "
    "significant advantages for a multi-trade construction company:",
    styles["BodyText2"]
))

story.append(Paragraph("Gaps in Existing Solutions", styles["SubHead"]))
gaps = [
    "Most general AP platforms lack deep construction-specific features (AIA billing, lien waivers, retainage)",
    "Construction-specific platforms (Adaptive, AvidXchange) have good features but limited AI sophistication",
    "No vendor combines best-in-class agentic AI with comprehensive construction AP workflows",
    "Integration with existing field/project management tools is often limited or expensive",
    "Vendor lock-in and per-invoice pricing creates escalating costs as the company grows",
]
for g in gaps:
    story.append(Paragraph(f"&bull; {g}", styles["BulletCustom"]))

story.append(Paragraph("Custom Build Advantages", styles["SubHead"]))
advantages = [
    "Tailored to exact multi-trade workflows (mechanical, electrical, plumbing, service, underground, manufacturing)",
    "Deep integration with existing accounting system (QuickBooks, Sage, Viewpoint, etc.)",
    "AI models trained specifically on the company's invoice patterns and vendor relationships",
    "Full control over data, security, and compliance requirements",
    "No per-invoice fees -- fixed infrastructure costs that don't scale with volume",
    "Construction-native features: AIA billing, lien waivers, retention, job costing, certified payroll",
    "Can leverage latest AI models (Claude, GPT-4) for superior document understanding",
    "Competitive advantage -- the system becomes a proprietary asset",
]
for a in advantages:
    story.append(Paragraph(f"&bull; {a}", styles["BulletCustom"]))

story.append(Paragraph("Recommended Custom Build Architecture", styles["SubHead"]))
arch_items = [
    "Backend: NestJS (TypeScript) for robust API development",
    "Database: PostgreSQL with Prisma ORM for financial data integrity",
    "AI Engine: Claude API for document understanding, extraction, and GL coding",
    "File Storage: S3-compatible storage for invoice documents and attachments",
    "Frontend: React/Next.js dashboard for AP team, PMs, and CFO views",
    "Authentication: Role-based access (AP clerk, project manager, superintendent, CFO)",
    "Integrations: API connectors to accounting software (QuickBooks, Sage, Viewpoint)",
    "Deployment: Cloud-hosted (AWS/Azure) with SOC 2 compliance considerations",
]
for a in arch_items:
    story.append(Paragraph(f"&bull; {a}", styles["BulletCustom"]))

# ---------- 9. RECOMMENDATIONS ----------
story.append(Paragraph("9. Recommendations", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Based on this research, we recommend a phased approach combining immediate commercial evaluation "
    "with parallel custom development:",
    styles["BodyText2"]
))

recs = [
    ("Short-term (Evaluate)",
     "Request demos from Adaptive and AvidXchange as construction-specific benchmarks. "
     "Also evaluate Stampli and Vic.ai for best-in-class AI capabilities. "
     "Understand current invoice volumes, processing costs, and pain points."),
    ("Medium-term (Build Phase 1)",
     "Develop a custom AI invoice ingestion and extraction pipeline using Claude API. "
     "This is the highest-value component and creates the foundation for full automation. "
     "Target: process invoices from all trades with 95%+ accuracy in data extraction."),
    ("Medium-term (Build Phase 2)",
     "Add construction-specific features: AIA billing support, lien waiver tracking, "
     "retention management, job costing with multi-trade cost code structures, and "
     "three-way PO matching."),
    ("Long-term (Build Phase 3)",
     "Complete approval workflows, payment scheduling, ERP integration, reporting dashboards, "
     "and predictive cash flow analytics. Target: 80%+ straight-through processing rate."),
]

for title, desc in recs:
    story.append(Paragraph(f"<b>{title}:</b> {desc}", styles["BodyText2"]))

story.append(Paragraph(
    "The custom build path is recommended because no existing solution adequately combines "
    "construction-grade AP features with state-of-the-art agentic AI. The estimated annual savings "
    "of $500,000+ in AP labor costs justify a significant development investment, and the resulting "
    "system becomes a proprietary competitive advantage.",
    styles["BodyText2"]
))

# ---------- 10. SOURCES ----------
story.append(PageBreak())
story.append(Paragraph("10. Sources", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

sources = [
    "Rillion - 8 Best AI Accounts Payable Automation Software (rillion.com)",
    "Gartner Peer Insights - Best Accounts Payable Applications Reviews 2026 (gartner.com)",
    "Ramp - AP Automation Software Comparison: Top-Rated Providers (ramp.com)",
    "HighRadius - 13 Top Accounts Payable Automation Software for 2026 (highradius.com)",
    "Zone & Co - Top 16 AP Automation Software Solutions for 2026 (zoneandco.com)",
    "Stampli - Tipalti vs BILL vs Stampli Comparison (stampli.com)",
    "Vic.ai - AI-First Invoice Processing (vic.ai)",
    "Hypatos - AI Agents for Accounts Payable (hypatos.ai)",
    "Adaptive - AI Native Construction Accounting (adaptive.build)",
    "AvidXchange - AP Automation for Construction (avidxchange.com)",
    "Itemize - Agentic AI for Construction Firms (itemize.com)",
    "Construction Dive - Startup Aims to Get Construction Firms Paid Faster (constructiondive.com)",
    "SafeBooks AI - AI Agents for AP: Controller's Guide (safebooks.ai)",
    "ChatFin - Top 10 Best AI Tools for AP Teams in 2026 (chatfin.ai)",
    "Quadient - Accounts Payable Automation Cost in 2025 (quadient.com)",
    "Parseur - AI Invoice Processing Benchmarks 2026 (parseur.com)",
    "CoreIntegrator - How Much Does AP Automation Cost (coreintegrator.com)",
    "Tipalti - The Impact of AI in Accounts Payable (tipalti.com)",
    "Genpact - Streamline AP with Agentic AI (genpact.com)",
    "EverWorker - Top AI Vendors for Accounts Payable (everworker.ai)",
    "AIMultiple Research - AP AI Applications & Tools (aimultiple.com)",
    "NetSuite - AI in Accounts Payable: Benefits & Impact (netsuite.com)",
]
for s in sources:
    story.append(Paragraph(f"&bull; {s}", styles["BulletCustom"]))

# BUILD
doc.build(story)
print(f"PDF generated: {OUTPUT}")
