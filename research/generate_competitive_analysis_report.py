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

OUTPUT = "C:/users/25badmin/projects/accounts-payable-research/Competitive_Analysis_2026.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    topMargin=0.75 * inch,
    bottomMargin=0.75 * inch,
    leftMargin=0.85 * inch,
    rightMargin=0.85 * inch,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle",
    fontSize=26,
    leading=32,
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
    name="Body",
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
    name="Callout",
    fontSize=10,
    leading=14,
    fontName="Helvetica-Bold",
    textColor=HexColor("#2b6cb0"),
    leftIndent=12,
    borderColor=HexColor("#2b6cb0"),
    borderWidth=1,
    borderPadding=8,
    spaceBefore=8,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="WeaknessCallout",
    fontSize=10,
    leading=14,
    fontName="Helvetica-Bold",
    textColor=HexColor("#c53030"),
    leftIndent=12,
    borderColor=HexColor("#c53030"),
    borderWidth=1,
    borderPadding=8,
    spaceBefore=8,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="StrengthCallout",
    fontSize=10,
    leading=14,
    fontName="Helvetica-Bold",
    textColor=HexColor("#276749"),
    leftIndent=12,
    borderColor=HexColor("#276749"),
    borderWidth=1,
    borderPadding=8,
    spaceBefore=8,
    spaceAfter=8,
))

story = []

# ========== COVER PAGE ==========
story.append(Spacer(1, 1.8 * inch))
story.append(Paragraph("Competitive Analysis<br/>AP AI Market 2026", styles["CoverTitle"]))
story.append(Spacer(1, 0.3 * inch))
story.append(HRFlowable(width="60%", color=HexColor("#2b6cb0"), thickness=2))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("Stampli vs Vic.ai vs Adaptive vs PayFlow AI", styles["CoverSubtitle"]))
story.append(Paragraph("Strengths, Weaknesses &amp; Market Positioning", styles["CoverSubtitle"]))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph(f"Prepared: {date.today().strftime('%B %d, %Y')}", styles["CoverSubtitle"]))
story.append(Paragraph("Confidential - Internal Use Only", styles["CoverSubtitle"]))
story.append(PageBreak())

# ========== TOC ==========
story.append(Paragraph("Table of Contents", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.15 * inch))
toc = [
    "1. Competitive Landscape Overview",
    "2. Stampli - Full Procure-to-Pay with Agentic AI",
    "3. Vic.ai - AI-First Invoice Processing",
    "4. Adaptive - Construction-Native Accounting",
    "5. Head-to-Head Comparison Matrix",
    "6. Our Advantages",
    "7. Our Disadvantages",
    "8. The Market Opportunity",
    "9. Strategic Recommendations",
    "10. Sources",
]
for item in toc:
    story.append(Paragraph(item, styles["Body"]))
story.append(PageBreak())

# ========== 1. OVERVIEW ==========
story.append(Paragraph("1. Competitive Landscape Overview", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "The AP automation market has three tiers of competitors relevant to a construction-focused "
    "AI AP product. General-purpose AI leaders (Stampli, Vic.ai) dominate with sophisticated AI "
    "but lack construction expertise. Construction-specific players (Adaptive) understand the "
    "vertical but have less advanced AI. No company currently combines best-in-class agentic AI "
    "with deep construction AP workflows — this is the gap PayFlow AI would target.",
    styles["Body"]
))

story.append(Paragraph(
    "This analysis examines the three most relevant competitors: Stampli (strongest agentic AI), "
    "Vic.ai (highest automation rates), and Adaptive (closest to our target market).",
    styles["Body"]
))

overview_data = [
    ["", "Stampli", "Vic.ai", "Adaptive", "PayFlow AI (Ours)"],
    ["Founded", "2015", "2017", "2022", "2026"],
    ["Funding", "$90M+", "$100M+", "a16z backed", "Bootstrapped"],
    ["Focus", "General P2P", "General AP", "Construction", "Construction + AI"],
    ["AI Type", "Agentic (Billy)", "Proprietary DL", "Task-specific AI", "Claude API (LLM)"],
    ["Customers", "Thousands", "Hundreds", "Growing", "Pre-launch"],
    ["Invoices Processed", "Billions", "535M+", "Not disclosed", "0"],
    ["Rating", "4.6/5 G2", "4.5/5 G2", "4.7/5 Capterra", "N/A"],
]
t = Table(overview_data, colWidths=[1.1*inch, 1.15*inch, 1.15*inch, 1.15*inch, 1.15*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("BACKGROUND", (4, 0), (4, -1), HexColor("#ebf8ff")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)

# ========== 2. STAMPLI ==========
story.append(PageBreak())
story.append(Paragraph("2. Stampli - Full Procure-to-Pay with Agentic AI", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Company Overview", styles["SubHead"]))
story.append(Paragraph(
    "Stampli is a leading procure-to-pay platform powered by Billy the Bot, an agentic AI assistant "
    "trained on over 83 million hours of real P2P workflow experience and $90 billion in annual spend. "
    "Billy operates across the entire procure-to-pay lifecycle: extracting data, routing approvals, "
    "matching invoices, coding transactions, and managing vendor compliance. The platform is the only "
    "solution that is complete and seamless across accounts payable, procurement, payments, vendor "
    "management, and credit cards.",
    styles["Body"]
))

story.append(Paragraph("What They Do That We Don't (Yet)", styles["SubHead"]))
stampli_advantages = [
    "Built-in collaboration layer: AP teams, approvers, and vendors chat directly on each invoice "
    "inside the platform. Eliminates email back-and-forth entirely.",
    "Procurement + AP + Payments + Cards in one: They've expanded well beyond AP into a full "
    "procure-to-pay suite including credit cards and vendor management.",
    "83 million hours of training data: Billy's accuracy comes from massive proprietary workflow data. "
    "We start from zero historical data, relying on Claude's general intelligence plus our prompts.",
    "200+ ERP integrations already built: Including NetSuite, QuickBooks, Sage Intacct, SAP, "
    "Microsoft Dynamics, and many more. We'd build each integration from scratch.",
    "PO matching at 97%+ accuracy: Handles complex scenarios like inconsistent item descriptions, "
    "quantity mismatches, and split deliveries — proven at scale.",
    "Stampli Edge for SMBs: Recently launched a lighter product for small/mid businesses, "
    "showing they're expanding downmarket into our potential customer base.",
]
for a in stampli_advantages:
    story.append(Paragraph(f"&bull; {a}", styles["BulletCustom"]))

story.append(Paragraph(
    "Their Weakness: Not construction-specific. No AIA billing (G702/G703), no lien waiver tracking, "
    "no retention management, no job costing across trades. Generic AP for all industries.",
    styles["WeaknessCallout"]
))

# ========== 3. VIC.AI ==========
story.append(Paragraph("3. Vic.ai - AI-First Invoice Processing", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Company Overview", styles["SubHead"]))
story.append(Paragraph(
    "Vic.ai is a pure AI-first AP platform built with proprietary deep-learning models designed "
    "specifically for accounting workflows. Unlike rule-based or template-based automation, Vic.ai's "
    "AI continuously learns from over 535 million processed invoices to improve accuracy, detect "
    "anomalies, and minimize human intervention. The platform achieves 97-99% AI accuracy, surpassing "
    "human-level performance, and customers report up to 355% improved invoice processing capacity "
    "per full-time employee.",
    styles["Body"]
))

story.append(Paragraph("What They Do That We Don't (Yet)", styles["SubHead"]))
vicai_advantages = [
    "Proprietary deep learning models: Purpose-built ML models trained specifically for invoice "
    "processing. We use Claude (a general-purpose LLM adapted via prompts). Their models are "
    "specialized; ours is general but more flexible.",
    "Autopilot mode (true zero-touch): Invoices flow from receipt to payment with no human in "
    "the loop. 84% no-touch processing rate proven at customer sites. This is the gold standard.",
    "VicInbox: Dedicated AI that monitors vendor email inboxes, automatically identifies invoices "
    "vs. spam vs. other correspondence, categorizes them, and routes for processing.",
    "VicPay: Automated B2B payment execution with vendor payment optimization and rebate maximization. "
    "We have no payment execution capability planned for MVP.",
    "VicAnalytics: Real-time bottleneck identification showing where invoices get stuck, why, "
    "and how to fix process inefficiencies. We have basic reporting but not process intelligence.",
    "535M+ invoices processed: Massive training dataset that continuously improves their models. "
    "Each invoice makes the system smarter. We rely on Claude's pre-trained knowledge.",
    "Proven ROI metrics: 355% capacity improvement per FTE, 5.8M hours saved across all customers. "
    "Real numbers from real deployments vs. our projections.",
]
for a in vicai_advantages:
    story.append(Paragraph(f"&bull; {a}", styles["BulletCustom"]))

story.append(Paragraph(
    "Their Weakness: No construction focus whatsoever. No job costing, no AIA forms, no lien waivers, "
    "no retention tracking. Enterprise pricing only — no SMB or mid-market tier. Expensive to implement.",
    styles["WeaknessCallout"]
))

# ========== 4. ADAPTIVE ==========
story.append(PageBreak())
story.append(Paragraph("4. Adaptive - Construction-Native Accounting", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Company Overview", styles["SubHead"]))
story.append(Paragraph(
    "Adaptive is an AI-native construction accounting platform backed by Andreessen Horowitz (a16z). "
    "The platform provides a team of AI agents that automate manual accounting work, reconcile "
    "financials with field updates, and deliver real-time financial control. Adaptive claims 10x "
    "better accuracy than general AP tools by focusing exclusively on construction's unique data "
    "sources and processes. They recently launched a solution for accounting firms to scale their "
    "construction services without adding headcount.",
    styles["Body"]
))

story.append(Paragraph("What They Do That We Don't (Yet)", styles["SubHead"]))
adaptive_advantages = [
    "Construction-first from day one: Every feature designed for construction — job costing, "
    "cost codes, AIA billing, subcontractor payments. We'd be building these; they already have them.",
    "Accounting firm distribution channel: They sell through CPA firms (Pinion, CLA) who manage "
    "construction clients. This is a go-to-market strategy we haven't explored.",
    "Real-time field reconciliation: Connects financial data with field updates so costs match "
    "actual work progress. We have no field integration planned.",
    "10x accuracy claim: They claim 10x better accuracy than general AP tools because they focus "
    "exclusively on construction data patterns and workflows.",
    "QuickBooks integration already built: Seamless sync for invoices, vendors, GL codes, and "
    "job cost data — the most common accounting system for their target market.",
    "Continuous cost capture: Automatically captures and codes every cost (bills, receipts, "
    "cards, payments) to the correct job and cost code as work happens in real-time.",
    "Approval routing by job: Bills routed based on job, cost code, or amount to the correct "
    "approvers — construction-aware workflow, not generic thresholds.",
]
for a in adaptive_advantages:
    story.append(Paragraph(f"&bull; {a}", styles["BulletCustom"]))

story.append(Paragraph(
    "Their Weakness: Limited AI sophistication compared to Stampli/Vic.ai. Only integrates with "
    "QuickBooks (not Sage 300 CRE, Viewpoint Vista, or other construction ERPs). Small company with "
    "limited track record. Pricing at $575/mo may price out smaller contractors.",
    styles["WeaknessCallout"]
))

# ========== 5. COMPARISON MATRIX ==========
story.append(Paragraph("5. Head-to-Head Comparison Matrix", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

hdr = ParagraphStyle("cmphdr", fontSize=7.5, leading=10, textColor=HexColor("#ffffff"), fontName="Helvetica-Bold", alignment=TA_CENTER)
cel = ParagraphStyle("cmpcel", fontSize=7.5, leading=10, fontName="Helvetica", alignment=TA_CENTER)
celb = ParagraphStyle("cmpcelb", fontSize=7.5, leading=10, fontName="Helvetica-Bold", alignment=TA_CENTER)

comp_data = [
    [Paragraph("Capability", hdr), Paragraph("Stampli", hdr), Paragraph("Vic.ai", hdr),
     Paragraph("Adaptive", hdr), Paragraph("PayFlow AI", hdr)],
    [Paragraph("AI Sophistication", celb), Paragraph("High", cel), Paragraph("Highest", cel),
     Paragraph("Medium", cel), Paragraph("High (Claude)", cel)],
    [Paragraph("Construction Features", celb), Paragraph("None", cel), Paragraph("None", cel),
     Paragraph("Strong", cel), Paragraph("To Be Built", cel)],
    [Paragraph("AIA Billing G702/G703", celb), Paragraph("No", cel), Paragraph("No", cel),
     Paragraph("Yes", cel), Paragraph("Planned", cel)],
    [Paragraph("Lien Waiver Tracking", celb), Paragraph("No", cel), Paragraph("No", cel),
     Paragraph("Yes", cel), Paragraph("Planned", cel)],
    [Paragraph("Retention Management", celb), Paragraph("No", cel), Paragraph("No", cel),
     Paragraph("Yes", cel), Paragraph("Planned", cel)],
    [Paragraph("Job Costing", celb), Paragraph("No", cel), Paragraph("No", cel),
     Paragraph("Yes", cel), Paragraph("Planned", cel)],
    [Paragraph("Proprietary ML Models", celb), Paragraph("Yes", cel), Paragraph("Yes", cel),
     Paragraph("Partial", cel), Paragraph("No (LLM)", cel)],
    [Paragraph("No-Touch Processing", celb), Paragraph("High", cel), Paragraph("84%", cel),
     Paragraph("Moderate", cel), Paragraph("Target 80%+", cel)],
    [Paragraph("ERP Integrations", celb), Paragraph("200+", cel), Paragraph("40+", cel),
     Paragraph("QuickBooks", cel), Paragraph("To Be Built", cel)],
    [Paragraph("Vendor Collaboration", celb), Paragraph("Yes (built-in)", cel), Paragraph("No", cel),
     Paragraph("No", cel), Paragraph("Planned", cel)],
    [Paragraph("Payment Execution", celb), Paragraph("Yes", cel), Paragraph("Yes (VicPay)", cel),
     Paragraph("Yes", cel), Paragraph("Not in MVP", cel)],
    [Paragraph("Fraud Detection", celb), Paragraph("Yes", cel), Paragraph("Yes", cel),
     Paragraph("Basic", cel), Paragraph("Yes (AI)", cel)],
    [Paragraph("Analytics/Reporting", celb), Paragraph("Strong", cel), Paragraph("VicAnalytics", cel),
     Paragraph("Basic", cel), Paragraph("Planned", cel)],
    [Paragraph("Proven at Scale", celb), Paragraph("Yes", cel), Paragraph("Yes", cel),
     Paragraph("Growing", cel), Paragraph("No", cel)],
    [Paragraph("Pricing", celb), Paragraph("Enterprise", cel), Paragraph("Enterprise", cel),
     Paragraph("$575/mo", cel), Paragraph("Flexible", cel)],
]

col_w = [1.2*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch]
t2 = Table(comp_data, colWidths=col_w)
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("BACKGROUND", (4, 0), (4, -1), HexColor("#ebf8ff")),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(t2)

# ========== 6. OUR ADVANTAGES ==========
story.append(PageBreak())
story.append(Paragraph("6. Our Advantages", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

advantages = [
    ("Latest AI Technology",
     "Claude API represents the cutting edge of large language models. While competitors built their "
     "AI 2-3 years ago, we leverage models that are continuously improving. Claude's multimodal "
     "vision, structured outputs, and extended thinking capabilities are more advanced than any "
     "custom ML model these competitors trained years ago. When Anthropic improves Claude, our "
     "product automatically gets better — no retraining required."),
    ("Cost Structure Advantage",
     "Our AI costs are pennies per invoice ($0.003-$0.02 depending on model). Competitors who built "
     "proprietary ML models carry massive infrastructure costs for training, hosting, and maintaining "
     "those models. We can undercut on price while maintaining high margins because Anthropic bears "
     "the AI infrastructure cost. This lets us offer flexible pricing that opens up the SMB market "
     "that Stampli and Vic.ai ignore."),
    ("The Niche Nobody Owns",
     "Construction-specific AP with best-in-class AI. Stampli and Vic.ai have great AI but zero "
     "construction knowledge. Adaptive has construction knowledge but moderate AI. We can be first "
     "to combine both. In a $1.9B market, owning a niche is more valuable than competing broadly."),
    ("Speed of Iteration",
     "We're small. We can ship features in days, not quarters. We can update prompts instantly — "
     "no model retraining, no deployment cycles. If a customer needs a new invoice format supported, "
     "we update a prompt and it's live. Competitors need engineering sprints for what we do with "
     "a text change."),
    ("No Legacy Technical Debt",
     "We're building from scratch with 2026 technology. No legacy code, no deprecated APIs, no "
     "migration headaches. We choose the best tools available today, not what was best in 2017."),
]

for title, desc in advantages:
    story.append(Paragraph(title, styles["SubHead"]))
    story.append(Paragraph(desc, styles["Body"]))

# ========== 7. OUR DISADVANTAGES ==========
story.append(Paragraph("7. Our Disadvantages (Honest Assessment)", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

disadvantages = [
    ("Zero Production Data",
     "Competitors have processed hundreds of millions of invoices. We have zero. Their AI has seen "
     "every edge case; we'll discover them as customers report them. Mitigation: Collect 200-500 "
     "test invoices before launch and run thorough accuracy testing."),
    ("No Integrations Built",
     "Stampli has 200+ ERP integrations. We have none. Each integration takes 2-6 weeks to build "
     "and test. Mitigation: Build the one integration our first customer needs (likely QuickBooks "
     "or Sage), then expand based on demand."),
    ("No Brand Recognition",
     "Construction companies are conservative buyers. They trust established vendors. We're unknown. "
     "Mitigation: Start with a pilot customer who can become a case study. Offer free or discounted "
     "trial periods. Leverage the accounting firm channel (like Adaptive does)."),
    ("AI Provider Dependency",
     "We depend on Anthropic's Claude API. If they raise prices, have outages, or change terms, "
     "we're affected. Competitors with proprietary models control their destiny. Mitigation: "
     "Abstract the AI layer so we can swap providers. Keep prompts provider-agnostic where possible."),
    ("Edge Cases Will Hurt",
     "Competitors have spent years solving edge cases: invoices in 50+ languages, every conceivable "
     "format, every ERP quirk. We'll hit these one by one and need to fix them fast. Mitigation: "
     "Robust error handling, human fallback for every AI decision, fast feedback loop from users."),
]

for title, desc in disadvantages:
    story.append(Paragraph(title, styles["SubHead"]))
    story.append(Paragraph(desc, styles["Body"]))

# ========== 8. OPPORTUNITY ==========
story.append(PageBreak())
story.append(Paragraph("8. The Market Opportunity", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "The construction industry represents a $2 trillion annual market in the US alone, with over "
    "900,000 construction firms. Most still process invoices manually or with basic tools. The "
    "intersection of construction AP and AI automation is a greenfield opportunity.",
    styles["Body"]
))

story.append(Paragraph("Why Now?", styles["SubHead"]))
why_now = [
    "AI technology (LLMs with vision) just reached the accuracy threshold needed for financial documents",
    "Construction companies are under increasing margin pressure and need to cut overhead costs",
    "Labor shortages in back-office roles make automation essential, not optional",
    "Adaptive (our closest competitor) just raised funding — proving VCs see this market",
    "The gap between general AI AP tools and construction needs remains wide open",
    "Regulatory complexity (lien laws, prevailing wage, certified payroll) creates a moat for "
    "construction-specific solutions that general tools can't easily replicate",
]
for w in why_now:
    story.append(Paragraph(f"&bull; {w}", styles["BulletCustom"]))

story.append(Paragraph("Market Size Estimate", styles["SubHead"]))
market_data = [
    ["Segment", "Number of Firms", "Avg Monthly AP Volume", "Potential Revenue/Firm", "TAM"],
    ["Large (500+ employees)", "~5,000", "3,000-10,000 invoices", "$1,000-$3,000/mo", "$60-180M/yr"],
    ["Mid (50-499 employees)", "~35,000", "500-3,000 invoices", "$500-$1,500/mo", "$210-630M/yr"],
    ["Small (10-49 employees)", "~200,000", "50-500 invoices", "$100-$500/mo", "$240M-1.2B/yr"],
]
t3 = Table(market_data, colWidths=[1.1*inch, 1*inch, 1.2*inch, 1.2*inch, 1.2*inch])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t3)

story.append(Paragraph(
    "Even capturing 0.1% of the mid-market segment (35 customers) at $1,000/month = $420,000 ARR. "
    "This is achievable within 12-18 months of launch with a focused sales effort.",
    styles["StrengthCallout"]
))

# ========== 9. STRATEGIC RECOMMENDATIONS ==========
story.append(Paragraph("9. Strategic Recommendations", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Positioning Strategy", styles["SubHead"]))
story.append(Paragraph(
    "Do NOT compete with Stampli or Vic.ai head-on. They have more funding, more data, and more "
    "integrations. Instead, own the construction niche. Position PayFlow AI as: 'The only AP "
    "automation built by construction people, for construction people, powered by the latest AI.' "
    "Construction companies don't want generic tools — they want someone who understands AIA billing, "
    "retention, lien waivers, and job costing.",
    styles["Body"]
))

story.append(Paragraph("Go-to-Market Priority", styles["SubHead"]))
gtm = [
    "Step 1: Land one pilot customer (ideally a multi-trade contractor you have a relationship with)",
    "Step 2: Build the MVP around their exact workflow and accounting system",
    "Step 3: Achieve 90%+ accuracy on their real invoices — document everything",
    "Step 4: Turn them into a case study with real ROI numbers",
    "Step 5: Approach 5-10 similar contractors in the same region",
    "Step 6: Explore the accounting firm channel (CPA firms serving construction clients)",
    "Step 7: Expand to adjacent construction segments (GCs, specialty contractors, suppliers)",
]
for g in gtm:
    story.append(Paragraph(f"&bull; {g}", styles["BulletCustom"]))

story.append(Paragraph("Features to Prioritize (Beat Each Competitor)", styles["SubHead"]))
priority_data = [
    ["To Beat...", "We Need...", "Priority"],
    ["Stampli", "Superior construction features they'll never build", "HIGH"],
    ["Vic.ai", "Comparable accuracy at a fraction of the price", "HIGH"],
    ["Adaptive", "Better AI + more ERP integrations (Sage, Viewpoint)", "MEDIUM"],
    ["All three", "A pilot customer with documented ROI", "CRITICAL"],
]
t4 = Table(priority_data, colWidths=[1.5*inch, 3*inch, 1.2*inch])
t4.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (2, 0), (2, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("BACKGROUND", (0, -1), (-1, -1), HexColor("#c6f6d5")),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t4)

# ========== 10. SOURCES ==========
story.append(PageBreak())
story.append(Paragraph("10. Sources", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

sources = [
    "Stampli AP Automation Platform (stampli.com/ap-automation-platform)",
    "Stampli Edge Launch for SMBs (cpapracticeadvisor.com, August 2025)",
    "Stampli Software Reviews &amp; Pricing 2026 (softwareadvice.com)",
    "Stampli Top 6 AP Automation Features (stampli.com/blog)",
    "Vic.ai How It Works (vic.ai/how-it-works)",
    "Vic.ai AP Automation &amp; AI Accounting Software (vic.ai/accounts-payable)",
    "Vic.ai Reviews 2026 (g2.com)",
    "Vic.ai AP Autonomy Explained (vic.ai/blog)",
    "Adaptive AI Native Construction Accounting (adaptive.build)",
    "Adaptive Automated Accounts Payable (adaptive.build/features/accounts-payable)",
    "Adaptive Launch for Accounting Firms (cpapracticeadvisor.com, May 2025)",
    "Adaptive Software Reviews 2026 (softwareadvice.com)",
    "Adaptive Reviews 2026 (capterra.com)",
    "Rillion - 11 Best Stampli Alternatives 2026 (rillion.com)",
]
for s in sources:
    story.append(Paragraph(f"&bull; {s}", styles["BulletCustom"]))

# BUILD
doc.build(story)
print(f"PDF generated: {OUTPUT}")
