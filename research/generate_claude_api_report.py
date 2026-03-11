from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import date

OUTPUT = "C:/users/25badmin/projects/accounts-payable-research/Claude_API_AP_Integration_Guide_2026.pdf"

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
    name="SubHead2",
    fontSize=11,
    leading=14,
    textColor=HexColor("#2d3748"),
    spaceBefore=8,
    spaceAfter=4,
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
    name="CodeBlock",
    fontSize=7.5,
    leading=10,
    fontName="Courier",
    leftIndent=12,
    rightIndent=12,
    spaceBefore=6,
    spaceAfter=6,
    backColor=HexColor("#f7fafc"),
    borderColor=HexColor("#e2e8f0"),
    borderWidth=0.5,
    borderPadding=6,
))
styles.add(ParagraphStyle(
    name="CodeComment",
    fontSize=7.5,
    leading=10,
    fontName="Courier",
    leftIndent=12,
    textColor=HexColor("#718096"),
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
    name="Footer",
    fontSize=8,
    leading=10,
    textColor=HexColor("#718096"),
    alignment=TA_CENTER,
))

story = []

# ========== COVER PAGE ==========
story.append(Spacer(1, 1.8 * inch))
story.append(Paragraph("Claude API Integration Guide<br/>for AP Automation", styles["CoverTitle"]))
story.append(Spacer(1, 0.3 * inch))
story.append(HRFlowable(width="60%", color=HexColor("#2b6cb0"), thickness=2))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("Technical Architecture, Prompt Engineering &amp; Cost Analysis", styles["CoverSubtitle"]))
story.append(Paragraph("Building a Commercial-Grade AI Accounts Payable Product", styles["CoverSubtitle"]))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph(f"Prepared: {date.today().strftime('%B %d, %Y')}", styles["CoverSubtitle"]))
story.append(Paragraph("Confidential - Internal Use Only", styles["CoverSubtitle"]))
story.append(PageBreak())

# ========== TABLE OF CONTENTS ==========
story.append(Paragraph("Table of Contents", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.15 * inch))
toc_items = [
    "1. How Claude Processes Invoices (End-to-End Flow)",
    "2. Claude Model Selection Strategy",
    "3. Pricing &amp; Cost-Per-Invoice Analysis",
    "4. Vision &amp; Multimodal Capabilities",
    "5. Structured Output &amp; Schema Design",
    "6. Professional Prompt Engineering for AP",
    "7. Prompt Caching &amp; Cost Optimization",
    "8. Batch Processing for High Volume",
    "9. Extended Thinking for Complex Cases",
    "10. Production Architecture &amp; Rate Limits",
    "11. Construction-Specific Prompt Examples",
    "12. Error Handling &amp; Validation Patterns",
    "13. Complete Code Examples",
    "14. Sources",
]
for item in toc_items:
    story.append(Paragraph(item, styles["Body"]))
story.append(PageBreak())

# ========== 1. HOW CLAUDE PROCESSES INVOICES ==========
story.append(Paragraph("1. How Claude Processes Invoices", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "When you send an invoice to the Claude API, the following happens under the hood:",
    styles["Body"]
))

flow_steps = [
    ("Step 1: Document Ingestion",
     "Your application converts the invoice (PDF, image, or scanned document) into a format Claude can read. "
     "For images, this means base64-encoding or uploading via the Files API. For PDFs, Claude can process them "
     "natively. The encoded document is sent as part of the API message payload."),
    ("Step 2: Visual Understanding",
     "Claude's vision model analyzes the document pixel by pixel. Unlike traditional OCR that just reads characters, "
     "Claude understands the spatial layout -- it knows that a number next to 'Total' is the total amount, that "
     "items in a table are line items, and that text in a header is the vendor name. This is semantic understanding, "
     "not pattern matching."),
    ("Step 3: Structured Extraction",
     "Using either Structured Outputs or Tool Use, Claude maps what it sees to your predefined schema. "
     "You define the exact JSON structure you need (invoice number, vendor, line items, amounts) and Claude "
     "populates it. With Structured Outputs, the response is guaranteed to match your schema -- no parsing errors."),
    ("Step 4: Confidence &amp; Validation",
     "Claude can flag fields it's uncertain about, identify missing information, and detect anomalies "
     "(duplicate invoice numbers, unusual amounts, mismatched totals). Your application then routes confident "
     "results to auto-posting and uncertain results to human review."),
]
for title, desc in flow_steps:
    story.append(Paragraph(title, styles["SubHead2"]))
    story.append(Paragraph(desc, styles["Body"]))

story.append(Paragraph(
    "The entire process takes 2-8 seconds per invoice depending on complexity and model choice. "
    "At scale with the Batch API, you can process thousands of invoices per hour at 50% reduced cost.",
    styles["Callout"]
))

# ========== 2. MODEL SELECTION ==========
story.append(Paragraph("2. Claude Model Selection Strategy", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Choosing the right Claude model for each task is critical to balancing cost and accuracy. "
    "A production AP system should use multiple models, routing invoices based on complexity.",
    styles["Body"]
))

model_data = [
    ["Model", "Best For", "Speed", "Accuracy", "Cost (Input/Output)"],
    ["Haiku 4.5", "Simple, standard invoices\n(80% of volume)", "Fastest", "Good", "$1 / $5 per MTok"],
    ["Sonnet 4.6", "Complex invoices,\nexception validation", "Fast", "Very High", "$3 / $15 per MTok"],
    ["Opus 4.6", "Multi-step reasoning,\napproval decisions", "Moderate", "Highest", "$5 / $25 per MTok"],
]
t = Table(model_data, colWidths=[1*inch, 1.6*inch, 0.8*inch, 0.8*inch, 1.5*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Recommended Routing Strategy", styles["SubHead"]))
routing = [
    "Tier 1 (Haiku 4.5): Standard invoices from known vendors with clean formatting -- ~80% of volume",
    "Tier 2 (Sonnet 4.6): New vendors, complex line items, multi-page invoices, or when Haiku confidence is low",
    "Tier 3 (Opus 4.6): Exception cases requiring reasoning -- PO discrepancies, approval rule evaluation, fraud flags",
    "Fallback: If any model returns low confidence, route to human review queue",
]
for r in routing:
    story.append(Paragraph(f"&bull; {r}", styles["BulletCustom"]))

# ========== 3. PRICING ANALYSIS ==========
story.append(PageBreak())
story.append(Paragraph("3. Pricing &amp; Cost-Per-Invoice Analysis", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Token Consumption Per Invoice", styles["SubHead"]))
story.append(Paragraph(
    "A typical invoice image (1000x1000px) consumes approximately 1,334 input tokens for the image alone. "
    "The system prompt adds 300-800 tokens, and the structured output response is typically 150-400 tokens. "
    "Token formula for images: tokens = (width x height) / 750.",
    styles["Body"]
))

cost_data = [
    ["Component", "Tokens", "Haiku Cost", "Sonnet Cost", "Opus Cost"],
    ["Invoice image (1000x1000)", "~1,334", "$0.0013", "$0.004", "$0.0067"],
    ["System prompt", "~500", "$0.0005", "$0.0015", "$0.0025"],
    ["Extraction schema", "~200", "$0.0002", "$0.0006", "$0.001"],
    ["Output (structured JSON)", "~300", "$0.0015", "$0.0045", "$0.0075"],
    ["TOTAL per invoice", "~2,334", "$0.0035", "$0.0106", "$0.0177"],
]
t2 = Table(cost_data, colWidths=[1.6*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.9*inch])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("BACKGROUND", (0, -1), (-1, -1), HexColor("#ebf8ff")),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t2)
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Monthly Cost Projections (Blended Model Strategy)", styles["SubHead"]))
story.append(Paragraph(
    "Using a tiered model strategy (80% Haiku, 15% Sonnet, 5% Opus) with prompt caching and batch processing:",
    styles["Body"]
))

monthly_data = [
    ["Monthly Invoices", "Standard Cost", "With Caching (30% savings)", "With Batch + Cache"],
    ["1,000", "$5.07", "$3.55", "$2.13"],
    ["5,000", "$25.35", "$17.75", "$10.65"],
    ["10,000", "$50.70", "$35.49", "$21.29"],
    ["50,000", "$253.50", "$177.45", "$106.47"],
    ["100,000", "$507.00", "$354.90", "$212.94"],
]
t3 = Table(monthly_data, colWidths=[1.3*inch, 1.3*inch, 1.6*inch, 1.5*inch])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t3)
story.append(Spacer(1, 0.05 * inch))

story.append(Paragraph(
    "Key insight: Even at 100,000 invoices/month, the AI API cost is only ~$213/month with full optimization. "
    "This is a fraction of the value delivered -- customers paying $0.50-$2.00 per invoice makes this extremely profitable.",
    styles["Callout"]
))

# ========== 4. VISION CAPABILITIES ==========
story.append(Paragraph("4. Vision &amp; Multimodal Capabilities", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Claude's vision is not OCR -- it is semantic document understanding. While OCR reads characters, "
    "Claude understands what the document means. It recognizes tables, headers, footers, logos, stamps, "
    "handwritten notes, and spatial relationships between elements.",
    styles["Body"]
))

story.append(Paragraph("Supported Formats &amp; Limits", styles["SubHead"]))
vision_specs = [
    "Image formats: JPEG, PNG, GIF, WebP",
    "PDF: Native support via document content blocks or Files API",
    "Max image size: 5MB per image via API",
    "Max resolution: 8000x8000 pixels (optimal: 1568px on longest edge)",
    "Max images per request: 100 (enables batch processing multiple invoices in one call)",
    "Token cost: (width x height) / 750 tokens per image",
]
for s in vision_specs:
    story.append(Paragraph(f"&bull; {s}", styles["BulletCustom"]))

story.append(Paragraph("What Claude Can Read on Invoices", styles["SubHead"]))
reads = [
    "Printed text in any font, size, or color",
    "Handwritten annotations and approval signatures",
    "Table structures with line items, quantities, prices",
    "Stamps (PAID, APPROVED, RECEIVED)",
    "Barcodes and QR codes (identifies presence, may extract data)",
    "Multi-language invoices (100+ languages)",
    "Poor quality scans, faxes, and photographs of documents",
    "Watermarks and background patterns (reads through them)",
]
for r in reads:
    story.append(Paragraph(f"&bull; {r}", styles["BulletCustom"]))

# ========== 5. STRUCTURED OUTPUT ==========
story.append(PageBreak())
story.append(Paragraph("5. Structured Output &amp; Schema Design", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Claude offers two methods for getting structured data back: Structured Outputs (recommended) and "
    "Tool Use. Structured Outputs guarantee that the response matches your JSON schema exactly -- "
    "no parsing errors, no malformed JSON, no missing required fields.",
    styles["Body"]
))

story.append(Paragraph("Recommended Invoice Schema (Pydantic)", styles["SubHead"]))
schema_code = """from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class LineItem(BaseModel):
    line_number: int = Field(description="Sequential line number")
    description: str = Field(description="Item or service description")
    quantity: Optional[float] = Field(description="Quantity if applicable")
    unit_price: Optional[float] = Field(description="Unit price if applicable")
    amount: float = Field(description="Line item total amount")
    cost_code: Optional[str] = Field(description="Job cost code if present")
    po_line_ref: Optional[str] = Field(description="PO line reference if present")

class InvoiceExtraction(BaseModel):
    # Core identifiers
    invoice_number: str = Field(description="Unique invoice identifier")
    invoice_date: str = Field(description="Invoice date in YYYY-MM-DD format")
    due_date: Optional[str] = Field(description="Payment due date in YYYY-MM-DD")
    po_number: Optional[str] = Field(description="Purchase order reference")

    # Vendor information
    vendor_name: str = Field(description="Vendor/supplier company name")
    vendor_address: Optional[str] = Field(description="Vendor mailing address")
    vendor_tax_id: Optional[str] = Field(description="Vendor EIN or tax ID")

    # Customer / bill-to
    bill_to_name: Optional[str] = Field(description="Bill-to company name")
    bill_to_address: Optional[str] = Field(description="Bill-to address")
    project_name: Optional[str] = Field(description="Project or job name")
    project_number: Optional[str] = Field(description="Project or job number")

    # Financial
    subtotal: Optional[float] = Field(description="Subtotal before tax")
    tax_amount: Optional[float] = Field(description="Tax amount")
    tax_rate: Optional[str] = Field(description="Tax rate percentage")
    total_amount: float = Field(description="Total invoice amount due")
    currency: str = Field(default="USD", description="Currency code")
    payment_terms: Optional[str] = Field(description="Payment terms e.g. Net 30")
    retention_amount: Optional[float] = Field(description="Retention/retainage held")
    retention_rate: Optional[str] = Field(description="Retention percentage")

    # Line items
    line_items: List[LineItem] = Field(description="All invoice line items")

    # Metadata
    confidence: ConfidenceLevel = Field(description="Overall extraction confidence")
    flags: List[str] = Field(default_factory=list,
        description="Any warnings: duplicate_suspected, total_mismatch, etc.")
    notes: Optional[str] = Field(description="Additional observations")"""

story.append(Preformatted(schema_code, styles["CodeBlock"]))

story.append(Paragraph(
    "Important: Structured Outputs guarantee format compliance, NOT accuracy. Always validate semantic "
    "correctness (e.g., do line items sum to subtotal? Is the date in the future?).",
    styles["Callout"]
))

# ========== 6. PROMPT ENGINEERING ==========
story.append(PageBreak())
story.append(Paragraph("6. Professional Prompt Engineering for AP", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "The quality of your prompts is the single biggest factor in extraction accuracy. "
    "Below are production-grade prompts refined through real-world invoice processing.",
    styles["Body"]
))

# --- PROMPT 1: Core Extraction ---
story.append(Paragraph("Prompt 1: Core Invoice Extraction (System Prompt)", styles["SubHead"]))
prompt1 = """SYSTEM PROMPT — Invoice Data Extraction Engine

You are an expert accounts payable processor with 15 years of experience
handling invoices across construction, manufacturing, and service industries.

YOUR TASK: Extract structured data from the provided invoice document with
the highest possible accuracy.

EXTRACTION RULES:
1. DATES: Always output in YYYY-MM-DD format. If only month/year given,
   use the first of the month. If ambiguous (e.g., 03/04/2026), prefer
   MM/DD/YYYY (US format) unless other context suggests otherwise.

2. AMOUNTS: Extract exact numeric values as shown. Do NOT round or
   recalculate. If a total appears inconsistent with line items, extract
   both the stated total and the calculated total, and flag the
   discrepancy in the flags array.

3. VENDOR: Extract the full legal entity name as printed. Do NOT
   abbreviate or normalize (e.g., keep "Smith & Sons Electrical, LLC"
   not "Smith and Sons Electrical").

4. LINE ITEMS: Extract every line item. For description, include the
   full text. If line items span multiple pages, combine them into a
   single list.

5. MISSING FIELDS: If a field is not present on the invoice, return
   null. Do NOT guess or infer values that aren't explicitly stated.

6. CONFIDENCE SCORING:
   - HIGH: All key fields clearly readable, amounts consistent
   - MEDIUM: Some fields unclear or minor inconsistencies
   - LOW: Significant fields unreadable or major discrepancies

7. FLAGS: Add relevant flags from this set:
   - "total_mismatch" — line items don't sum to stated total
   - "duplicate_suspected" — invoice number matches a common pattern
   - "future_dated" — invoice date is in the future
   - "missing_po" — no PO number found when one is expected
   - "handwritten_annotations" — handwritten notes detected
   - "poor_scan_quality" — document quality affects readability
   - "multi_currency" — multiple currencies detected
   - "retention_present" — retainage/retention line found"""

story.append(Preformatted(prompt1, styles["CodeBlock"]))

# --- PROMPT 2: GL Coding ---
story.append(Paragraph("Prompt 2: Autonomous GL Code Prediction", styles["SubHead"]))
prompt2 = """SYSTEM PROMPT — GL Code Prediction Engine

You are an expert construction accountant specializing in job costing
and general ledger classification.

CONTEXT: You will receive:
1. Extracted invoice data (vendor, line items, amounts, project)
2. The company's chart of accounts (provided below)
3. Historical coding patterns for this vendor (if available)

YOUR TASK: Predict the correct GL account, cost code, and job number
for each line item.

CHART OF ACCOUNTS (abbreviated):
  5000 - Direct Materials
    5010 - Electrical Materials
    5020 - Plumbing Materials
    5030 - Mechanical/HVAC Materials
    5040 - Underground/Civil Materials
  5100 - Subcontractor Costs
    5110 - Electrical Subcontractors
    5120 - Plumbing Subcontractors
    5130 - Mechanical Subcontractors
  5200 - Equipment Rental
  5300 - Tools & Supplies
  6000 - Overhead
    6010 - Office Supplies
    6020 - Utilities
    6030 - Insurance
    6040 - Vehicle Expenses

CODING RULES:
1. Match vendor type to the appropriate cost category
2. If a project/job number is on the invoice, use it
3. If the vendor has historical coding patterns provided, follow them
   unless the current invoice clearly differs
4. For ambiguous items, suggest the most likely code and set
   confidence to MEDIUM
5. Never leave a line item uncoded — always provide your best prediction

OUTPUT: For each line item, provide:
  - gl_account: The GL account number and name
  - cost_code: The job cost code (if applicable)
  - job_number: The project/job number
  - coding_confidence: HIGH, MEDIUM, or LOW
  - coding_rationale: Brief explanation of why this code was chosen"""

story.append(Preformatted(prompt2, styles["CodeBlock"]))

# --- PROMPT 3: Fraud Detection ---
story.append(PageBreak())
story.append(Paragraph("Prompt 3: Invoice Fraud &amp; Anomaly Detection", styles["SubHead"]))
prompt3 = """SYSTEM PROMPT — Fraud & Anomaly Detection Agent

You are a forensic accounting specialist analyzing invoices for fraud
indicators and anomalies.

You will receive:
1. The current invoice data (extracted)
2. Historical data for this vendor (avg invoice amount, frequency,
   typical items, payment history)
3. Company policy thresholds

ANALYZE FOR THESE RED FLAGS:

DUPLICATE DETECTION:
- Same invoice number from same vendor
- Same amount + same date from same vendor (different inv #)
- Sequential invoice numbers with identical amounts

AMOUNT ANOMALIES:
- Invoice amount > 2x vendor's historical average
- Round-number invoices (exactly $5,000, $10,000) — flag for review
- Amount just below approval thresholds (e.g., $4,999 when limit is
  $5,000)

VENDOR ANOMALIES:
- New vendor with no purchase order
- Vendor address matches an employee address
- Vendor bank details recently changed

TIMING ANOMALIES:
- Invoice dated on weekend or holiday
- Invoice dated before PO date
- Duplicate invoices submitted within 30-day window

CONSTRUCTION-SPECIFIC:
- Progress billing exceeds contract value
- Retainage release without completion certification
- Change order amounts without approved change order reference
- Lien waiver amount doesn't match payment amount

OUTPUT:
- risk_score: 0-100 (0=no risk, 100=definite fraud)
- risk_level: LOW (<25), MEDIUM (25-50), HIGH (50-75), CRITICAL (>75)
- findings: List of specific findings with evidence
- recommended_action: APPROVE, REVIEW, HOLD, or REJECT
- explanation: Human-readable summary for the AP reviewer"""

story.append(Preformatted(prompt3, styles["CodeBlock"]))

# --- PROMPT 4: AIA Billing ---
story.append(Paragraph("Prompt 4: AIA G702/G703 Progress Billing Extraction", styles["SubHead"]))
prompt4 = """SYSTEM PROMPT — AIA Progress Billing Specialist

You are an expert at reading AIA Document G702 (Application and
Certificate for Payment) and G703 (Continuation Sheet) forms used
in construction billing.

EXTRACTION REQUIREMENTS FOR G702:
- application_number: The application/draw number
- period_to: The billing period end date
- contract_date: Original contract date
- project_name: Project name from the form
- owner: Property owner name
- contractor: General contractor or subcontractor name
- original_contract_sum: Line 1 — original contract amount
- change_orders_add: Line 2 — net change by change orders (additions)
- change_orders_deduct: Line 3 — deductions from change orders
- contract_sum_to_date: Line 4 — current contract sum
- total_completed_to_date: Line 5 — total completed and stored
- retainage_on_completed: Line 5a — retainage on completed work
- retainage_on_stored: Line 5b — retainage on stored materials
- total_retainage: Line 5c — total retainage
- total_earned_less_retainage: Line 6
- less_previous_certificates: Line 7 — previously certified amounts
- current_payment_due: Line 8 — current amount due
- balance_to_finish: Line 9 — remaining balance plus retainage

EXTRACTION REQUIREMENTS FOR G703 (Continuation Sheet):
For each line item (schedule of values row):
- item_number: Line item number (A)
- description: Description of work (B)
- scheduled_value: Scheduled value (C)
- previous_applications: Work completed from previous applications (D)
- this_period: Work completed this period (E)
- materials_stored: Materials presently stored (F)
- total_completed: Total completed and stored to date (G)
- percent_complete: Percentage complete (G/C) (H)
- balance_to_finish: Balance to finish (C-G) (I)
- retainage: Retainage amount (J)

VALIDATION: After extraction, verify:
1. G703 line items sum to G702 totals
2. Percent complete is between 0-100% for each line
3. Balance to finish = Scheduled Value - Total Completed
4. Current payment = Total this period - retainage on this period
Flag any discrepancies."""

story.append(Preformatted(prompt4, styles["CodeBlock"]))

# ========== 7. PROMPT CACHING ==========
story.append(PageBreak())
story.append(Paragraph("7. Prompt Caching &amp; Cost Optimization", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Prompt caching is one of the most powerful cost optimization tools for AP automation. "
    "Since your system prompt and extraction schema stay the same across thousands of invoices, "
    "you can cache them and pay only 10% of the input token cost on subsequent requests.",
    styles["Body"]
))

story.append(Paragraph("How Caching Works for AP", styles["SubHead"]))
cache_items = [
    "First request: System prompt is cached (1.25x write cost for 5-min cache, 2x for 1-hour cache)",
    "Subsequent requests: Cached system prompt costs 0.1x (90% savings on input tokens)",
    "Cache is per-model and based on exact prefix match of the prompt content",
    "For AP: Your system prompt + schema = ~800 tokens cached. At $3/MTok (Sonnet), saves ~$0.002/invoice",
    "At 10,000 invoices/month: ~$20/month saved just from caching system prompts",
    "Vendor-specific context can also be cached when processing batches from the same vendor",
]
for c in cache_items:
    story.append(Paragraph(f"&bull; {c}", styles["BulletCustom"]))

story.append(Paragraph("Caching Implementation", styles["SubHead"]))
cache_code = """import anthropic

client = anthropic.Anthropic()

# The system prompt is cached after the first call.
# Subsequent calls with the same prefix reuse the cache.
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": INVOICE_EXTRACTION_SYSTEM_PROMPT,  # ~800 tokens
            "cache_control": {"type": "ephemeral"}     # 5-min TTL
        }
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image", "source": {...}},
                {"type": "text", "text": "Extract invoice data."}
            ]
        }
    ]
)

# Check cache performance
print(f"Cache write tokens: {response.usage.cache_creation_input_tokens}")
print(f"Cache read tokens:  {response.usage.cache_read_input_tokens}")
print(f"Fresh input tokens: {response.usage.input_tokens}")"""

story.append(Preformatted(cache_code, styles["CodeBlock"]))

# ========== 8. BATCH PROCESSING ==========
story.append(Paragraph("8. Batch Processing for High Volume", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "The Batch API processes requests asynchronously at 50% reduced cost. Most batches complete in "
    "under 1 hour. This is ideal for non-urgent invoice processing -- for example, processing a day's "
    "worth of invoices overnight, or handling bulk imports from new customers.",
    styles["Body"]
))

batch_code = """import anthropic
import json

client = anthropic.Anthropic()

# Prepare batch of invoices
invoices_to_process = load_pending_invoices()  # Your data source

batch_requests = []
for inv in invoices_to_process:
    batch_requests.append({
        "custom_id": f"invoice-{inv['id']}",
        "params": {
            "model": "claude-sonnet-4-6",
            "max_tokens": 2048,
            "system": INVOICE_EXTRACTION_SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": inv["mime_type"],
                                "data": inv["base64_data"]
                            }
                        },
                        {"type": "text", "text": "Extract invoice data."}
                    ]
                }
            ]
        }
    })

# Submit batch (up to 100,000 requests)
batch = client.messages.batches.create(requests=batch_requests)
print(f"Batch ID: {batch.id}, Status: {batch.processing_status}")

# Poll for completion (or use webhook)
result = client.messages.batches.retrieve(batch.id)
# Status: in_progress | ended

# Process results
for result in client.messages.batches.results(batch.id):
    invoice_id = result.custom_id
    extracted = json.loads(result.result.message.content[0].text)
    save_extraction(invoice_id, extracted)"""

story.append(Preformatted(batch_code, styles["CodeBlock"]))

# ========== 9. EXTENDED THINKING ==========
story.append(PageBreak())
story.append(Paragraph("9. Extended Thinking for Complex Cases", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Extended thinking gives Claude a 'scratchpad' to reason through complex scenarios before "
    "producing output. For AP, this is valuable for three-way matching, approval decisions, "
    "and fraud analysis where Claude needs to compare multiple data points.",
    styles["Body"]
))

thinking_code = """response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000  # Allow up to 8K tokens of reasoning
    },
    system=FRAUD_DETECTION_SYSTEM_PROMPT,
    messages=[
        {
            "role": "user",
            "content": f\"\"\"
            Analyze this invoice for fraud and anomalies:

            CURRENT INVOICE:
            {json.dumps(current_invoice)}

            VENDOR HISTORY (last 12 months):
            - Average invoice: $4,200
            - Frequency: 2x/month
            - Typical items: Electrical supplies
            {json.dumps(vendor_history)}

            MATCHING PO:
            {json.dumps(purchase_order)}

            Provide your risk assessment.
            \"\"\"
        }
    ]
)

# The thinking block shows Claude's reasoning process
for block in response.content:
    if block.type == "thinking":
        log_reasoning(block.thinking)  # Store for audit trail
    elif block.type == "text":
        risk_assessment = json.loads(block.text)"""

story.append(Preformatted(thinking_code, styles["CodeBlock"]))
story.append(Spacer(1, 0.05 * inch))

story.append(Paragraph(
    "Extended thinking tokens are billed as output tokens. Budget 5,000-10,000 thinking tokens for "
    "complex cases. At Opus pricing ($25/MTok output), this adds ~$0.13-$0.25 per complex invoice -- "
    "use only for flagged exceptions, not routine processing.",
    styles["Callout"]
))

# ========== 10. PRODUCTION ARCHITECTURE ==========
story.append(Paragraph("10. Production Architecture &amp; Rate Limits", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Rate Limits by Tier", styles["SubHead"]))

rate_data = [
    ["Tier", "Requests/Min", "Input Tokens/Min", "Output Tokens/Min", "Batch Queue"],
    ["Tier 1", "50", "30,000", "8,000", "10,000"],
    ["Tier 2", "1,000", "450,000", "90,000", "100,000"],
    ["Tier 3", "2,000", "800,000", "160,000", "200,000"],
    ["Tier 4", "4,000", "2,000,000", "400,000", "500,000"],
]
t4 = Table(rate_data, colWidths=[0.7*inch, 1.1*inch, 1.2*inch, 1.2*inch, 1*inch])
t4.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a365d")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f7fafc"), HexColor("#edf2f7")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t4)
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Production Architecture Pattern", styles["SubHead"]))
arch_items = [
    "API Gateway: Rate limiting, authentication, request routing per customer",
    "Invoice Queue: Redis/SQS queue for incoming invoices -- decouples ingestion from processing",
    "Worker Pool: Multiple workers consuming from queue, each calling Claude API",
    "Model Router: Routes invoices to Haiku/Sonnet/Opus based on vendor, complexity, customer tier",
    "Result Store: PostgreSQL for extracted data, S3 for original documents",
    "Retry Logic: Exponential backoff on 429 (rate limit) and 529 (overloaded) responses",
    "Webhook/Polling: Notify customer systems when extraction is complete",
    "Audit Log: Store every API call, response, and human override for compliance",
]
for a in arch_items:
    story.append(Paragraph(f"&bull; {a}", styles["BulletCustom"]))

# ========== 11. CONSTRUCTION-SPECIFIC PROMPTS ==========
story.append(PageBreak())
story.append(Paragraph("11. Construction-Specific Prompt Examples", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Prompt 5: Lien Waiver Processing", styles["SubHead"]))
lien_prompt = """SYSTEM PROMPT — Lien Waiver Extraction & Validation

You are a construction payment compliance specialist. Extract and
classify lien waivers from the provided document.

WAIVER TYPES (identify which type this is):
1. CONDITIONAL_PROGRESS — Conditional upon receipt of progress payment
2. UNCONDITIONAL_PROGRESS — Unconditional for progress payment received
3. CONDITIONAL_FINAL — Conditional upon receipt of final payment
4. UNCONDITIONAL_FINAL — Unconditional for final payment received

EXTRACT:
- waiver_type: One of the four types above
- claimant_name: The party waiving lien rights
- customer_name: The property owner or GC
- project_name: Project identification
- project_address: Job site address
- through_date: Period covered through this date
- payment_amount: The payment amount referenced
- exceptions: Any exceptions or exclusions listed
- signature_present: true/false — is the document signed?
- notarized: true/false — is there a notary acknowledgment?
- date_signed: Date of signature if visible
- state_compliant: Which state's statutory form this matches (if any)

VALIDATION:
- Verify waiver amount matches the expected payment amount
- Flag if conditional waiver is submitted where unconditional is required
- Flag if signature or notarization is missing
- Flag if through_date doesn't match the billing period"""

story.append(Preformatted(lien_prompt, styles["CodeBlock"]))

story.append(Paragraph("Prompt 6: Three-Way PO Matching", styles["SubHead"]))
match_prompt = """SYSTEM PROMPT — Intelligent Three-Way Match Engine

You are a procurement specialist performing three-way matching:
Invoice vs Purchase Order vs Receiving Report.

You will receive three data objects. Compare them and determine if
the invoice should be approved for payment.

MATCHING RULES:
1. VENDOR MATCH: Invoice vendor must match PO vendor (allow for minor
   name variations like "Corp" vs "Corporation")

2. QUANTITY MATCH: For each line item:
   - Invoice qty <= Received qty <= PO qty (allow partial shipments)
   - Flag if invoice qty > received qty (overbilling)
   - Flag if invoice qty > PO qty (exceeds PO)

3. PRICE MATCH: For each line item:
   - Invoice unit price should match PO unit price
   - Allow tolerance of +/- 2% for rounding
   - Flag price increases > 2% as PRICE_VARIANCE

4. AMOUNT MATCH:
   - Invoice total should match (qty x price) for all matched lines
   - Allow tolerance of +/- $0.05 for rounding on line items
   - Total tolerance: +/- $1.00

MATCH RESULTS (per line item):
  - FULL_MATCH: Qty, price, and amount all match within tolerance
  - PARTIAL_MATCH: Qty is partial shipment, price matches
  - PRICE_VARIANCE: Price differs beyond tolerance
  - QUANTITY_VARIANCE: Qty exceeds received or PO amount
  - NO_MATCH: Line item not found on PO

OVERALL DECISION:
  - AUTO_APPROVE: All lines FULL_MATCH or PARTIAL_MATCH
  - REVIEW: Any PRICE_VARIANCE within 10% — needs manager approval
  - HOLD: Any QUANTITY_VARIANCE or PRICE_VARIANCE > 10%
  - REJECT: NO_MATCH lines or vendor mismatch"""

story.append(Preformatted(match_prompt, styles["CodeBlock"]))

# ========== 12. ERROR HANDLING ==========
story.append(PageBreak())
story.append(Paragraph("12. Error Handling &amp; Validation Patterns", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph(
    "Structured Outputs guarantee format compliance but NOT accuracy. You must build a validation "
    "layer that catches semantic errors before data enters your accounting system.",
    styles["Body"]
))

story.append(Paragraph("Validation Pipeline", styles["SubHead"]))
validation_code = """class InvoiceValidator:
    def validate(self, extracted: InvoiceExtraction) -> ValidationResult:
        errors, warnings = [], []

        # 1. Math validation
        calc_total = sum(item.amount for item in extracted.line_items)
        if extracted.subtotal and abs(calc_total - extracted.subtotal) > 0.05:
            warnings.append(f"Line items sum ({calc_total}) != "
                          f"subtotal ({extracted.subtotal})")

        # 2. Date validation
        inv_date = parse_date(extracted.invoice_date)
        if inv_date > date.today():
            warnings.append("Invoice date is in the future")
        if inv_date < date.today() - timedelta(days=365):
            errors.append("Invoice date is over 1 year old")

        # 3. Required field validation
        if not extracted.invoice_number:
            errors.append("Missing invoice number")
        if extracted.total_amount <= 0:
            errors.append("Total amount must be positive")

        # 4. Duplicate check (against database)
        existing = db.find_invoice(
            vendor=extracted.vendor_name,
            number=extracted.invoice_number
        )
        if existing:
            errors.append(f"Duplicate: matches invoice {existing.id}")

        # 5. Confidence-based routing
        if extracted.confidence == "low":
            return ValidationResult(
                status="MANUAL_REVIEW",
                errors=errors, warnings=warnings
            )

        if errors:
            return ValidationResult(status="REJECTED", errors=errors)

        if warnings:
            return ValidationResult(status="REVIEW", warnings=warnings)

        return ValidationResult(status="AUTO_APPROVED")"""

story.append(Preformatted(validation_code, styles["CodeBlock"]))

story.append(Paragraph("API Error Handling", styles["SubHead"]))
api_errors = [
    "400 Bad Request: Invalid parameters — check image format, base64 encoding",
    "401 Unauthorized: Invalid API key — verify key and permissions",
    "429 Rate Limited: Too many requests — implement exponential backoff (start 1s, max 60s)",
    "500 Internal Error: Anthropic server issue — retry with backoff, switch to backup model",
    "529 Overloaded: API temporarily at capacity — retry with longer backoff (start 5s)",
    "Timeout: Large documents may take 10-30s — set appropriate timeout, consider chunking",
]
for e in api_errors:
    story.append(Paragraph(f"&bull; {e}", styles["BulletCustom"]))

# ========== 13. COMPLETE CODE EXAMPLE ==========
story.append(PageBreak())
story.append(Paragraph("13. Complete Code Examples", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("Full Invoice Processing Pipeline (Python)", styles["SubHead"]))
full_code = """import anthropic
import base64
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# --- Configuration ---
client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var
DEFAULT_MODEL = "claude-sonnet-4-6"
FALLBACK_MODEL = "claude-opus-4-6"

# --- Schema (as defined in Section 5) ---
class InvoiceExtraction(BaseModel):
    invoice_number: str
    invoice_date: str
    vendor_name: str
    total_amount: float
    line_items: List[LineItem]
    confidence: ConfidenceLevel
    flags: List[str] = []
    # ... (full schema from Section 5)

# --- System Prompt ---
SYSTEM_PROMPT = \"\"\"[Insert Prompt 1 from Section 6]\"\"\"

# --- Core Processing Function ---
def process_invoice(file_path: str) -> InvoiceExtraction:
    \"\"\"Process a single invoice file and return structured data.\"\"\"

    # 1. Load and encode the document
    path = Path(file_path)
    file_bytes = path.read_bytes()
    base64_data = base64.standard_b64encode(file_bytes).decode("utf-8")

    # Determine media type
    media_types = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".pdf": "application/pdf",
        ".webp": "image/webp"
    }
    media_type = media_types.get(path.suffix.lower(), "image/jpeg")

    # 2. Call Claude with structured output
    response = client.messages.parse(
        model=DEFAULT_MODEL,
        max_tokens=2048,
        output_format=InvoiceExtraction,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64_data
                    }
                },
                {
                    "type": "text",
                    "text": "Extract all invoice data from this document."
                }
            ]
        }]
    )

    extraction = response.parsed_output

    # 3. If low confidence, escalate to Opus
    if extraction.confidence == ConfidenceLevel.LOW:
        response = client.messages.parse(
            model=FALLBACK_MODEL,
            max_tokens=4096,
            output_format=InvoiceExtraction,
            thinking={"type": "enabled", "budget_tokens": 5000},
            system=[{"type": "text", "text": SYSTEM_PROMPT}],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64_data
                    }},
                    {"type": "text",
                     "text": "This invoice was difficult to read on "
                             "first pass. Please carefully extract all "
                             "data, using extended reasoning for any "
                             "ambiguous fields."}
                ]
            }]
        )
        extraction = response.parsed_output

    # 4. Validate
    validation = InvoiceValidator().validate(extraction)

    # 5. Store results
    save_to_database(extraction, validation)

    return extraction"""

story.append(Preformatted(full_code, styles["CodeBlock"]))

story.append(Paragraph("Multi-Tenant Customer Processing", styles["SubHead"]))
tenant_code = """class APProcessor:
    \"\"\"Multi-tenant invoice processor for SaaS deployment.\"\"\"

    def __init__(self):
        self.client = anthropic.Anthropic()

    def process_for_customer(self, customer_id: str, invoice_file):
        \"\"\"Process invoice with customer-specific configuration.\"\"\"

        # Load customer config (chart of accounts, vendors, rules)
        config = load_customer_config(customer_id)

        # Build customer-specific system prompt
        system_prompt = self._build_prompt(config)

        # Select model based on customer tier
        model = self._select_model(config["tier"], config["complexity"])

        # Process with customer context
        response = self.client.messages.parse(
            model=model,
            max_tokens=2048,
            output_format=InvoiceExtraction,
            system=[{
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            }],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64",
                        "media_type": invoice_file["type"],
                        "data": invoice_file["data"]
                    }},
                    {"type": "text",
                     "text": f"Extract invoice data. "
                             f"Customer: {config['company_name']}. "
                             f"Apply their chart of accounts."}
                ]
            }]
        )

        return response.parsed_output

    def _select_model(self, tier, complexity):
        if tier == "enterprise" or complexity == "high":
            return "claude-sonnet-4-6"
        return "claude-haiku-4-5"

    def _build_prompt(self, config):
        base = INVOICE_EXTRACTION_SYSTEM_PROMPT
        # Append customer-specific chart of accounts
        base += f"\\n\\nCHART OF ACCOUNTS:\\n{config['chart_of_accounts']}"
        # Append vendor patterns if available
        if config.get("vendor_patterns"):
            base += f"\\n\\nKNOWN VENDORS:\\n{config['vendor_patterns']}"
        return base"""

story.append(Preformatted(tenant_code, styles["CodeBlock"]))

# ========== 14. SOURCES ==========
story.append(PageBreak())
story.append(Paragraph("14. Sources", styles["SectionHead"]))
story.append(HRFlowable(width="100%", color=HexColor("#e2e8f0"), thickness=1))
story.append(Spacer(1, 0.1 * inch))

sources = [
    "Claude API Documentation — Vision (platform.claude.com/docs/en/build-with-claude/vision)",
    "Claude API Documentation — Structured Outputs (platform.claude.com/docs/en/build-with-claude/structured-outputs)",
    "Claude API Documentation — Batch Processing (platform.claude.com/docs/en/build-with-claude/batch-processing)",
    "Claude API Documentation — Prompt Caching (platform.claude.com/docs/en/build-with-claude/prompt-caching)",
    "Claude API Documentation — Extended Thinking (platform.claude.com/docs/en/build-with-claude/extended-thinking)",
    "Claude API Documentation — Pricing (platform.claude.com/docs/en/about-claude/pricing)",
    "Claude API Documentation — Rate Limits (platform.claude.com/docs/en/api/rate-limits)",
    "Claude API Documentation — Models Overview (platform.claude.com/docs/en/about-claude/models/overview)",
    "Claude Cookbook — Extracting Structured JSON with Tool Use (github.com/anthropics/anthropic-cookbook)",
    "Koncile — Claude vs GPT vs Gemini for Invoice Extraction (koncile.ai)",
    "Gennai — Claude AI vs ChatGPT for Invoice Processing (gennai.io)",
    "CallSphere — Claude Vision API: Analyzing Documents at Scale (callsphere.tech)",
    "Reruption — Use Claude to Speed Up Invoice & Receipt Processing (reruption.com)",
    "Anthropic Claude API Pricing Guide 2026 (devtk.ai)",
    "Claude API Pricing Calculator 2026 (invertedstone.com)",
    "Agenta — Guide to Structured Outputs and Function Calling with LLMs (agenta.ai)",
]
for s in sources:
    story.append(Paragraph(f"&bull; {s}", styles["BulletCustom"]))

# BUILD
doc.build(story)
print(f"PDF generated: {OUTPUT}")
