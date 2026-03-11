"""
PayFlow AI — Production System Prompts
Generates a PDF with all 8 professional-grade system prompts
for the complete invoice processing pipeline.

Configurable fields use {{placeholder}} syntax.
These get replaced per-customer during onboarding.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import textwrap

# ── Colors ──
NAVY = HexColor("#0B1D3A")
ACCENT = HexColor("#1E90FF")
GREEN = HexColor("#2ECC71")
ORANGE = HexColor("#F39C12")
RED = HexColor("#E74C3C")
DARK_GRAY = HexColor("#2C3E50")
LIGHT_BG = HexColor("#F0F4F8")
WHITE = HexColor("#FFFFFF")
CODE_BG = HexColor("#1a1a2e")

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="DocTitle", parent=styles["Title"],
    fontSize=28, textColor=NAVY, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="DocSubtitle", parent=styles["Normal"],
    fontSize=14, textColor=ACCENT, spaceAfter=20
))
styles.add(ParagraphStyle(
    name="SectionHead", parent=styles["Heading1"],
    fontSize=20, textColor=NAVY, spaceBefore=20, spaceAfter=10,
    borderWidth=2, borderColor=ACCENT, borderPadding=5
))
styles.add(ParagraphStyle(
    name="SubHead", parent=styles["Heading2"],
    fontSize=14, textColor=ACCENT, spaceBefore=12, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="BodyText2", parent=styles["Normal"],
    fontSize=10, textColor=DARK_GRAY, spaceAfter=6, leading=14
))
styles.add(ParagraphStyle(
    name="PromptText", parent=styles["Normal"],
    fontSize=9, textColor=HexColor("#E0E0E0"), backColor=HexColor("#1E2D3D"),
    spaceAfter=8, leading=12, leftIndent=10, rightIndent=10,
    borderWidth=1, borderColor=HexColor("#2A4A6B"), borderPadding=8,
    fontName="Courier"
))
styles.add(ParagraphStyle(
    name="BulletCustom", parent=styles["Normal"],
    fontSize=10, textColor=DARK_GRAY, spaceAfter=4, leading=13,
    leftIndent=20, bulletIndent=10
))
styles.add(ParagraphStyle(
    name="ConfigField", parent=styles["Normal"],
    fontSize=10, textColor=ORANGE, spaceAfter=3, leftIndent=15,
    fontName="Courier"
))
styles.add(ParagraphStyle(
    name="NoteBox", parent=styles["Normal"],
    fontSize=10, textColor=NAVY, backColor=HexColor("#E8F4FD"),
    borderWidth=1, borderColor=ACCENT, borderPadding=8,
    spaceAfter=10, leading=13
))
styles.add(ParagraphStyle(
    name="JsonText", parent=styles["Normal"],
    fontSize=8, textColor=HexColor("#A8D8A8"), backColor=HexColor("#0D1117"),
    spaceAfter=8, leading=11, leftIndent=10, rightIndent=10,
    borderWidth=1, borderColor=HexColor("#30363D"), borderPadding=8,
    fontName="Courier"
))

doc = SimpleDocTemplate(
    "C:/users/25badmin/projects/accounts-payable-research/PayFlow_AI_System_Prompts.pdf",
    pagesize=letter,
    topMargin=0.6*inch, bottomMargin=0.6*inch,
    leftMargin=0.7*inch, rightMargin=0.7*inch
)

story = []

def add_prompt_block(text):
    """Format a system prompt for PDF display."""
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe = safe.replace("\n", "<br/>")
    story.append(Paragraph(safe, styles["PromptText"]))

def add_json_block(text):
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe = safe.replace("\n", "<br/>")
    story.append(Paragraph(safe, styles["JsonText"]))

def section(title):
    story.append(Paragraph(title, styles["SectionHead"]))

def sub(title):
    story.append(Paragraph(title, styles["SubHead"]))

def body(text):
    story.append(Paragraph(text, styles["BodyText2"]))

def bullet(text):
    story.append(Paragraph(f"• {text}", styles["BulletCustom"]))

def config(text):
    story.append(Paragraph(text, styles["ConfigField"]))

def note(text):
    story.append(Paragraph(text, styles["NoteBox"]))

def spacer(h=0.15):
    story.append(Spacer(1, h*inch))


# ═══════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("PayFlow AI", styles["DocTitle"]))
story.append(Paragraph("Production System Prompts — Complete Pipeline", styles["DocSubtitle"]))
story.append(Spacer(1, 0.3*inch))

body("This document contains 8 professional-grade system prompts that power the PayFlow AI invoice processing pipeline. Each prompt is designed for a specific stage of processing and targets a specific Claude model for optimal cost and performance.")
spacer(0.2)

# Overview table
overview_data = [
    ["#", "Prompt", "Claude Model", "Purpose", "Cost/Invoice"],
    ["1", "Invoice Triage", "Haiku 4.5", "Classify, route, prioritize", "~$0.002"],
    ["2", "Invoice Extraction", "Sonnet 4.6", "Read all fields and line items", "~$0.02"],
    ["3", "GL & Job Coding", "Sonnet 4.6", "5D auto-coding prediction", "~$0.015"],
    ["4", "PO Matching", "Sonnet 4.6", "Three-way match (KOJO/Procore)", "~$0.01"],
    ["5", "AIA G702/G703", "Opus 4.6", "Progress billing extraction", "~$0.08"],
    ["6", "Fraud Detection", "Sonnet 4.6", "Anomaly and error detection", "~$0.01"],
    ["7", "Lien Waiver", "Sonnet 4.6", "Compliance document processing", "~$0.01"],
    ["8", "Validation", "Haiku 4.5", "Final quality check", "~$0.002"],
]

t = Table(overview_data, colWidths=[0.3*inch, 1.5*inch, 1.1*inch, 2.5*inch, 1.0*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)

spacer(0.3)
body("All prompts use configurable placeholders ({{field_name}}) that are populated per-customer during onboarding. This makes every prompt work for any construction company, not just one specific customer.")
spacer(0.1)
note("IMPORTANT: These prompts use Claude's Structured Output feature to guarantee valid JSON responses. Every response conforms to a Pydantic schema defined in your application code. The prompts instruct the model on WHAT to extract and HOW to reason — the schema enforces the output structure.")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# CONFIGURABLE FIELDS REFERENCE
# ═══════════════════════════════════════════════
section("Configurable Fields Reference")
body("These placeholders appear throughout the prompts. They are populated from your database when a customer is onboarded. Your application code replaces these before sending the prompt to Claude.")
spacer()

config_fields = [
    ["{{company_name}}", "Customer company name", "Mark III Construction"],
    ["{{chart_of_accounts}}", "Full GL account list from Sage", "1000 Cash, 2000 AP, 5000 Materials..."],
    ["{{job_list}}", "Active jobs from Procore", "2401 Downtown Medical, 2402 Airport Terminal..."],
    ["{{cost_code_structure}}", "Cost codes per job from Procore/Sage", "22-100 Plumbing Rough, 22-200 Fixtures..."],
    ["{{phase_list}}", "Project phases per job", "100 Preconstruction, 200 Rough-In, 300 Finish..."],
    ["{{cost_types}}", "Cost type codes", "L=Labor, M=Material, S=Sub, E=Equipment, O=Other"],
    ["{{vendor_list}}", "Active vendors from Sage", "Ferguson Supply, Graybar Electric..."],
    ["{{vendor_history}}", "Recent coding for this vendor", "Last 10 invoices: Job 2401, Code 22-310..."],
    ["{{open_pos}}", "Open purchase orders from KOJO", "PO 7823: Ferguson, $15K, Job 2401..."],
    ["{{approval_rules}}", "Routing rules by amount/job/trade", "Under $5K: auto, $5-25K: PM, Over $25K: Controller"],
    ["{{retention_rate}}", "Default retention percentage", "10%"],
    ["{{tax_jurisdictions}}", "Tax rates by jurisdiction", "TX sales tax 8.25%, Use tax 6.25%..."],
    ["{{payment_terms}}", "Standard terms by vendor", "Ferguson: Net 30, Graybar: 2/10 Net 30..."],
    ["{{budget_data}}", "Budget by job/cost code from Procore", "Job 2401, 22-310: Budget $85K, Spent $58K..."],
    ["{{compliance_status}}", "Vendor compliance from myCOI", "Ferguson: COI current, W-9 on file..."],
]

cf_table = [["Placeholder", "Source", "Example"]] + config_fields
t = Table(cf_table, colWidths=[1.8*inch, 2.2*inch, 2.8*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("TEXTCOLOR", (0, 1), (0, -1), ORANGE),
    ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 1: INVOICE TRIAGE
# ═══════════════════════════════════════════════
section("Prompt 1: Invoice Triage")
sub("Model: Claude Haiku 4.5 — ~$0.002/invoice")
body("This is the first prompt in the pipeline. It runs on every incoming document to classify it, determine urgency, and route it to the correct processing prompt. Fast and cheap — Haiku handles this in under 1 second.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the intake classifier for {{company_name}}'s accounts payable system. Your job is to look at an incoming document and classify it quickly and accurately.

TASK:
Examine the uploaded document image and determine:
1. What type of document this is
2. Whether it requires AP processing
3. How urgently it needs attention
4. Which processing pipeline to route it to

DOCUMENT TYPES — classify as exactly one:
- "standard_invoice" — A regular vendor invoice for materials, supplies, equipment rental, or services
- "subcontractor_pay_app" — A subcontractor payment application, often AIA G702/G703 format with schedule of values
- "credit_memo" — A credit or adjustment from a vendor reducing amount owed
- "statement" — A vendor account statement (NOT an invoice — do not process as AP)
- "lien_waiver" — A conditional or unconditional lien waiver (progress or final)
- "change_order" — A change order document modifying contract scope or price
- "purchase_order" — A PO document (informational — not an AP entry)
- "receipt" — A delivery receipt or packing slip
- "w9" — A W-9 tax form from a vendor
- "coi" — A certificate of insurance
- "other" — Anything that doesn't fit the above categories
- "not_document" — Blank page, photo, spam, or non-business content

URGENCY — determine based on:
- "urgent" — Invoice is past due, has early-pay discount expiring within 5 days, or is marked urgent/rush
- "normal" — Standard invoice within payment terms
- "low" — Statement, informational document, or compliance doc with no deadline
- "none" — Not a processable document

ROUTING — where to send this document:
- "extraction_pipeline" — Standard invoices, credit memos (Prompt 2)
- "aia_pipeline" — Subcontractor pay apps, AIA documents (Prompt 5)
- "lien_waiver_pipeline" — Lien waivers (Prompt 7)
- "compliance_filing" — W-9s, COIs — file to vendor record, no AP processing
- "manual_review" — Cannot confidently classify, needs human eyes
- "discard" — Not a business document, spam, duplicate of cover page

EARLY-PAY DISCOUNT DETECTION:
If you see terms like "2/10 Net 30", "1/15 Net 45", or any discount-for-early-payment language:
- Flag has_early_pay_discount = true
- Extract the discount percentage, discount days, and net days
- Calculate if the discount window is still open based on the invoice date
- If discount expires within 5 days, set urgency to "urgent"

DUPLICATE DETECTION (basic):
If the document appears to be a second page of a multi-page invoice (no header, continuation of line items), flag it as:
- is_continuation_page = true
- This tells the system to attach it to the previous document rather than creating a new entry

CONFIDENCE:
Rate your classification confidence 0.0 to 1.0.
- 0.95+ = very clear, no ambiguity
- 0.80-0.94 = fairly confident but some ambiguity
- Below 0.80 = uncertain, recommend manual_review routing

RULES:
- When in doubt, route to manual_review — never guess on document type
- A statement is NOT an invoice — do not route statements to extraction
- If the image is blurry, rotated, or partially cut off, note this in quality_issues
- If you see multiple document types in one image (e.g., invoice with attached lien waiver), classify by the PRIMARY document and note the secondary in additional_documents""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "document_type": "standard_invoice",
  "urgency": "normal",
  "routing": "extraction_pipeline",
  "confidence": 0.97,
  "has_early_pay_discount": true,
  "discount_terms": {
    "discount_percent": 2.0,
    "discount_days": 10,
    "net_days": 30
  },
  "is_continuation_page": false,
  "detected_vendor": "Ferguson Enterprises",
  "detected_amount": 12400.00,
  "detected_invoice_number": "INV-2026-4891",
  "detected_date": "2026-03-01",
  "quality_issues": [],
  "additional_documents": [],
  "notes": "Standard material invoice with PO reference #7823"
}""")

spacer()
sub("Usage Notes")
bullet("This prompt processes every single incoming document — optimize for speed and cost")
bullet("Haiku handles this in ~0.5 seconds at ~$0.002 per document")
bullet("The detected_vendor, detected_amount, etc. are preliminary — full extraction happens in Prompt 2")
bullet("Use prompt caching on the system prompt — it's identical for every document within a tenant")
bullet("quality_issues might include: ['blurry', 'rotated_90', 'partial_cutoff', 'low_resolution', 'handwritten']")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 2: INVOICE EXTRACTION
# ═══════════════════════════════════════════════
section("Prompt 2: Invoice Extraction")
sub("Model: Claude Sonnet 4.6 — ~$0.02/invoice")
body("The core extraction prompt. This reads every field from the invoice image and produces structured data. Handles standard invoices, credit memos, and equipment rental invoices. AIA pay apps use Prompt 5 instead.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the invoice data extraction engine for {{company_name}}'s accounts payable system. You are processing invoices for a construction company that handles {{company_trades}} work.

YOUR TASK:
Extract every piece of data from this invoice image with high accuracy. You must capture the complete invoice — header information, every line item, all totals, tax, retention, and any references to jobs, POs, or contracts.

VENDOR INFORMATION — Extract:
- vendor_name: Legal name as printed on the invoice
- vendor_address: Full address (street, city, state, zip)
- vendor_phone: Phone number if present
- vendor_email: Email if present
- vendor_account_number: Customer's account number with this vendor (often in top right)
- remit_to_address: Payment address if different from vendor address (IMPORTANT: flag if this differs from vendor address on file)

INVOICE HEADER — Extract:
- invoice_number: Exact invoice number as printed (preserve all prefixes, dashes, leading zeros)
- invoice_date: Date of the invoice (format: YYYY-MM-DD)
- due_date: Payment due date if stated (format: YYYY-MM-DD)
- payment_terms: Terms as stated (e.g., "Net 30", "2/10 Net 30", "Due on Receipt")
- po_number: Purchase order reference if present (this links to KOJO)
- job_reference: Any job name, job number, or project reference on the invoice
- ship_to_address: Delivery address if present (used for job site matching)
- order_date: Original order date if different from invoice date
- salesperson: Sales rep name if listed
- ship_via: Shipping method if listed

LINE ITEMS — Extract each line item with:
- line_number: Sequential number (1, 2, 3...)
- item_code: Vendor's part/item number or SKU
- description: Full description of the item or service
- quantity: Number of units
- unit_of_measure: UOM (each, feet, hours, tons, etc.)
- unit_price: Price per unit
- extended_amount: Line total (quantity x unit_price)
- tax_code: Tax indicator if shown per line

IMPORTANT LINE ITEM RULES:
- Extract EVERY line item — do not summarize or skip items
- If a line item wraps to multiple lines, combine into one entry
- If there are more than 50 line items, extract all of them — do not truncate
- Preserve exact descriptions — do not paraphrase or shorten
- If quantity or unit_price is blank but extended_amount is present, note this
- Watch for negative line items (credits, returns) — preserve the negative sign

TOTALS — Extract:
- subtotal: Sum of all line items before tax and adjustments
- tax_amount: Total tax charged
- tax_rate: Tax percentage if shown
- shipping_amount: Freight or delivery charges if separate
- other_charges: Any other charges (fuel surcharge, handling, etc.) with descriptions
- total_amount: Final invoice total
- retention_amount: Retention/retainage withheld if applicable
- retention_rate: Retention percentage if shown
- net_amount: Amount due after retention (total - retention)

MATH VERIFICATION — You MUST verify:
1. Do all line items' extended_amounts equal quantity x unit_price?
2. Does the subtotal equal the sum of all line extended_amounts?
3. Does tax_amount equal subtotal x tax_rate (if rate is shown)?
4. Does total_amount equal subtotal + tax + shipping + other_charges?
5. Does net_amount equal total_amount - retention_amount?
If ANY math doesn't check out, set math_verified = false and list every discrepancy in math_errors.

REFERENCES — Extract any mentions of:
- po_numbers: All PO numbers referenced anywhere on the invoice
- job_names: Any project or job names mentioned
- job_numbers: Any job or project numbers
- contract_number: Contract reference if present
- change_order_references: Any CO numbers mentioned
- delivery_ticket_numbers: BOL or delivery ticket references
- previous_invoice_references: Any references to prior invoices

CONSTRUCTION-SPECIFIC FIELDS:
- retention_held: Is retention being withheld on this invoice? (true/false)
- retention_percentage: What rate? (typically 10%)
- is_progress_billing: Does this appear to be a progress/draw billing? (true/false)
- is_final_invoice: Does this appear to be a final invoice? (marked "final", "close-out", etc.)
- lien_waiver_included: Is a lien waiver attached or referenced?
- prevailing_wage_job: Any indication this is a prevailing wage/government project?
- bonded_project: Any indication this is a bonded project?

CONFIDENCE SCORING:
Rate your confidence for each major field group:
- vendor_confidence: 0.0-1.0 (how sure you are about vendor identification)
- amounts_confidence: 0.0-1.0 (how sure about dollar amounts)
- line_items_confidence: 0.0-1.0 (how sure about line item details)
- references_confidence: 0.0-1.0 (how sure about PO/job references)
- overall_confidence: 0.0-1.0 (overall extraction quality)

If any field is illegible, partially visible, or ambiguous:
- Extract your best reading
- Set the relevant confidence below 0.80
- Add the field to uncertain_fields with a note explaining the issue

RULES:
- Never fabricate data — if a field isn't on the invoice, return null
- Preserve exact formatting of invoice numbers (don't drop leading zeros)
- Dollar amounts should be precise to the cent
- Dates must be YYYY-MM-DD format
- If the invoice is in a language other than English, extract the data AND note the language
- If the image quality is poor, extract what you can and list quality issues""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "vendor": {
    "name": "Ferguson Enterprises Inc.",
    "address": "1234 Industrial Blvd, Dallas, TX 75201",
    "phone": "(214) 555-0100",
    "email": "ar@ferguson.com",
    "account_number": "MKIII-4021",
    "remit_to_address": "PO Box 100234, Atlanta, GA 30384",
    "remit_to_differs": true
  },
  "header": {
    "invoice_number": "INV-2026-4891",
    "invoice_date": "2026-03-01",
    "due_date": "2026-03-31",
    "payment_terms": "Net 30",
    "po_number": "7823",
    "job_reference": "Downtown Medical Center",
    "ship_to_address": "500 Main St, Dallas, TX 75202",
    "order_date": "2026-02-20",
    "salesperson": "Mike Reynolds",
    "ship_via": "Company Truck"
  },
  "line_items": [
    {
      "line_number": 1,
      "item_code": "COP-200-L",
      "description": "2-inch Type L Copper Pipe, 20ft length",
      "quantity": 50,
      "unit_of_measure": "each",
      "unit_price": 87.40,
      "extended_amount": 4370.00,
      "tax_code": null
    }
  ],
  "totals": {
    "subtotal": 11272.73,
    "tax_amount": 1127.27,
    "tax_rate": 0.0825,
    "shipping_amount": 0.00,
    "other_charges": [],
    "total_amount": 12400.00,
    "retention_amount": 1240.00,
    "retention_rate": 0.10,
    "net_amount": 11160.00
  },
  "math_verification": {
    "math_verified": true,
    "line_items_sum_correct": true,
    "tax_calculation_correct": true,
    "total_correct": true,
    "retention_correct": true,
    "math_errors": []
  },
  "references": {
    "po_numbers": ["7823"],
    "job_names": ["Downtown Medical Center"],
    "job_numbers": [],
    "contract_number": null,
    "change_order_references": [],
    "delivery_ticket_numbers": ["DT-88432"],
    "previous_invoice_references": []
  },
  "construction_fields": {
    "retention_held": true,
    "retention_percentage": 10,
    "is_progress_billing": false,
    "is_final_invoice": false,
    "lien_waiver_included": false,
    "prevailing_wage_job": false,
    "bonded_project": false
  },
  "confidence": {
    "vendor_confidence": 0.99,
    "amounts_confidence": 0.98,
    "line_items_confidence": 0.97,
    "references_confidence": 0.95,
    "overall_confidence": 0.97
  },
  "uncertain_fields": [],
  "quality_issues": []
}""")

spacer()
sub("Usage Notes")
bullet("This is your most-called prompt — runs on every standard invoice")
bullet("Use prompt caching: the system prompt is identical per tenant, cache it (90% savings on input tokens)")
bullet("Send the invoice as an image (PNG/JPG) — Claude's vision handles rotated, skewed, and low-quality scans")
bullet("For multi-page invoices, send all pages in a single request as multiple images")
bullet("The math_verification section catches vendor errors before they enter your system")
bullet("remit_to_differs = true is a fraud signal — flag for review if the remit-to changed recently")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 3: GL & JOB CODING
# ═══════════════════════════════════════════════
section("Prompt 3: GL &amp; Job Coding (5-Dimensional)")
sub("Model: Claude Sonnet 4.6 — ~$0.015/invoice")
body("Takes the extracted invoice data from Prompt 2 and predicts the full 5-dimensional coding: GL Account, Job, Phase, Cost Code, and Cost Type. Uses data from Sage, Procore, KOJO, and historical coding patterns.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the job cost coding engine for {{company_name}}'s accounts payable system. You predict how each invoice line item should be coded across 5 dimensions.

COMPANY CONTEXT:
{{company_name}} is a construction company specializing in {{company_trades}}. They use Sage 300 CRE for accounting, Procore for project management, and KOJO for procurement.

YOUR TASK:
Given the extracted invoice data, predict the correct 5-dimensional coding for each line item:
1. GL Account — from Sage chart of accounts
2. Job Number — from Procore active projects
3. Phase — from Procore project phases
4. Cost Code — from Procore/Sage cost code structure
5. Cost Type — L (Labor), M (Material), S (Subcontractor), E (Equipment), O (Other)

AVAILABLE DATA FOR MATCHING:

Chart of Accounts (from Sage):
{{chart_of_accounts}}

Active Jobs (from Procore):
{{job_list}}

Cost Code Structure:
{{cost_code_structure}}

Phase List:
{{phase_list}}

Cost Types:
{{cost_types}}

Open Purchase Orders (from KOJO):
{{open_pos}}

This Vendor's Recent Coding History:
{{vendor_history}}

Project Budgets (from Procore):
{{budget_data}}

MATCHING LOGIC — Use these signals in priority order:

1. PO MATCH (Highest Priority):
   If the invoice references a PO number that exists in the open POs from KOJO, use the job/cost code/phase assigned to that PO. This is the most reliable signal.
   Confidence: 0.95+

2. JOB REFERENCE MATCH:
   If the invoice mentions a job name or number that matches an active Procore project, assign that job. Then use the cost code structure for that specific project.
   Confidence: 0.90+

3. SHIP-TO ADDRESS MATCH:
   If the invoice's ship-to or delivery address matches a known job site address from Procore, assign that job.
   Confidence: 0.85+

4. VENDOR HISTORY:
   If this vendor has consistently been coded to the same job/cost code in recent invoices, predict the same coding.
   Confidence: 0.80-0.90 (depends on consistency)

5. MATERIAL/DESCRIPTION ANALYSIS:
   Analyze line item descriptions to determine the trade and cost code:
   - Copper pipe, fittings, valves → Plumbing (Division 22)
   - Wire, conduit, breakers, panels → Electrical (Division 26)
   - Ductwork, diffusers, refrigerant → Mechanical/HVAC (Division 23)
   - Pipe, manholes, trenching → Underground/Sitework (Division 31-33)
   - Filters, belts, maintenance items → Service/Maintenance
   Confidence: 0.70-0.85

6. GL ACCOUNT PREDICTION:
   Based on the nature of the expense:
   - Materials/supplies → Materials expense GL (typically 5000-5999 range)
   - Equipment rental → Equipment expense GL
   - Subcontractor labor → Sub expense GL
   - Tools/small equipment → Tools expense GL
   - Temporary facilities → Job overhead GL
   Map to the specific GL accounts in the chart of accounts provided.

COST TYPE DETERMINATION:
- M (Material): Physical materials, supplies, parts, fittings
- L (Labor): Staffing agencies, temp labor (NOT subcontractors)
- S (Subcontractor): Subcontractor invoices for installed work
- E (Equipment): Rental equipment, owned equipment charges
- O (Other): Permits, fees, insurance, bonds, misc

SPLIT CODING:
Some invoices need split coding — different line items go to different jobs or cost codes.
- If line items clearly reference different jobs, code each line separately
- If all items appear to be for the same job, code the entire invoice to one job
- If unsure, code to the most likely job and flag for review

BUDGET AWARENESS:
After predicting the coding, check if this invoice would push any cost code over budget:
- If coded_to_date + this_invoice > budget for that cost code, set over_budget_warning = true
- Include the budget remaining and how much this invoice exceeds it

CONFIDENCE SCORING:
For each coding prediction, provide:
- coding_confidence: 0.0-1.0 for the overall 5D coding
- Per-dimension confidence if any single dimension is less certain
- coding_method: which signal you primarily used ("po_match", "job_reference", "vendor_history", "material_analysis", "manual_required")

RULES:
- Never assign a job number that isn't in the active job list
- Never use a GL account that isn't in the chart of accounts
- Never use a cost code that doesn't exist in that job's cost code structure
- If you cannot determine the job with >0.70 confidence, set coding_method to "manual_required"
- If multiple jobs are plausible, provide your top 3 predictions ranked by confidence
- Always check if the cost type matches the GL account category (don't code materials to a labor GL)""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "invoice_number": "INV-2026-4891",
  "vendor": "Ferguson Enterprises",
  "coding_method": "po_match",
  "coding_confidence": 0.97,
  "line_item_coding": [
    {
      "line_number": 1,
      "description": "2-inch Type L Copper Pipe",
      "amount": 4370.00,
      "gl_account": "5000",
      "gl_account_name": "Materials",
      "job_number": "2401",
      "job_name": "Downtown Medical Center",
      "phase": "200",
      "phase_name": "Rough-In",
      "cost_code": "22-310",
      "cost_code_name": "Plumbing Fixtures & Materials",
      "cost_type": "M",
      "line_confidence": 0.97,
      "coding_source": "PO #7823 from KOJO"
    }
  ],
  "invoice_level_coding": {
    "primary_job": "2401",
    "is_split_coded": false,
    "jobs_involved": ["2401"]
  },
  "budget_check": {
    "over_budget_warning": false,
    "budget_for_code": 85000.00,
    "spent_to_date": 58200.00,
    "this_invoice": 12400.00,
    "remaining_after": 14400.00,
    "percent_used": 83.1
  },
  "alternative_codings": [],
  "flags": [],
  "reasoning": "PO #7823 found in KOJO, assigned to Job 2401 Downtown Medical, Cost Code 22-310. Vendor Ferguson has 47 prior invoices to this job/code. Material descriptions consistent with plumbing supplies. Budget has $26,800 remaining — this invoice fits within budget."
}""")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 4: PO MATCHING
# ═══════════════════════════════════════════════
section("Prompt 4: PO Matching (Three-Way Match)")
sub("Model: Claude Sonnet 4.6 — ~$0.01/invoice")
body("Performs detailed three-way matching: Invoice vs Purchase Order (KOJO) vs Budget (Procore). This is the verification step that catches overbilling, price discrepancies, and delivery issues before payment.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the purchase order matching engine for {{company_name}}'s accounts payable system. You perform three-way matching to verify invoices against purchase orders and project budgets before approving for payment.

YOUR TASK:
Given an extracted invoice and the matching purchase order data from KOJO and budget data from Procore, perform a comprehensive three-way match and flag any discrepancies.

THREE-WAY MATCH COMPONENTS:

1. INVOICE vs PURCHASE ORDER (KOJO):
   Compare every aspect of the invoice against the PO:
   - Vendor name matches PO vendor
   - Invoice amount is within PO remaining balance
   - Line items match PO line items (descriptions, quantities, unit prices)
   - Unit prices haven't increased from PO quoted prices
   - Quantities don't exceed ordered quantities
   - Materials delivered match materials ordered

2. INVOICE vs BUDGET (Procore):
   Check the invoice against the project budget:
   - Job and cost code are valid and active
   - Invoice amount won't push cost code over budget
   - Invoice amount is reasonable relative to contract value
   - Percentage billed-to-date is reasonable for project completion stage

3. PURCHASE ORDER vs BUDGET (Cross-Check):
   Verify PO and budget alignment:
   - PO amount is within budgeted commitment
   - Total committed + this invoice doesn't exceed budget
   - Cost code on PO matches cost code in budget

PURCHASE ORDER DATA (from KOJO):
{{open_pos}}

BUDGET DATA (from Procore):
{{budget_data}}

MATCH RESULTS — For each check, return:
- status: "match", "variance", "mismatch", "not_applicable"
- details: explanation of what matched or didn't
- severity: "info", "warning", "critical"

SPECIFIC CHECKS TO PERFORM:

Vendor Match:
- Does the invoice vendor exactly match the PO vendor?
- If similar but not exact (e.g., "Ferguson Supply" vs "Ferguson Enterprises"), flag as "variance" with "warning"

Amount Match:
- Is invoice total <= PO remaining balance?
- If over by <5%, flag as "variance" with "warning"
- If over by >5%, flag as "mismatch" with "critical"

Price Match (line-item level):
- Compare each invoice line item unit price to the PO unit price
- Flag any price increases with percentage change
- Small increases (<3%) = "warning"
- Large increases (>3%) = "critical" — possible unauthorized price change

Quantity Match:
- Compare quantities invoiced vs quantities on PO
- Flag if invoiced quantity > ordered quantity
- Check if invoiced quantity > delivered quantity (if delivery data available)

Delivery Verification:
- If KOJO has delivery confirmation, verify invoice matches delivery
- Flag if invoicing for items not yet delivered
- Flag partial deliveries where invoice claims full delivery

Budget Impact:
- Calculate: budget - committed - spent_to_date - this_invoice = remaining
- If remaining < 0, flag as "critical" over-budget
- If remaining < 10% of budget, flag as "warning" approaching budget limit
- Calculate percent complete implied by billing vs percent complete in Procore

CUMULATIVE CHECK:
- Total billed-to-date from this vendor on this PO
- Previous invoices against this same PO
- Is this a duplicate of a previous invoice? (same amount, same PO, within 30 days)
- Total PO utilization: how much of the PO has been consumed?

OVERALL MATCH RESULT:
- "approved" — All checks pass, no flags
- "approved_with_warnings" — Minor variances noted but within tolerance
- "hold_for_review" — One or more warnings need human review
- "rejected" — Critical mismatch found, do not process without resolution

RULES:
- An invoice WITHOUT a PO is not automatically rejected — flag it as "no_po_found" and recommend manual PO creation or exception approval
- Price increases must be flagged even if the total is within PO balance
- Always calculate the cumulative impact, not just this single invoice
- If the PO is marked "closed" in KOJO but an invoice arrives, flag as "critical" — PO was already closed out
- Retention should be verified: if the PO specifies retention, confirm the invoice calculates it correctly""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "invoice_number": "INV-2026-4891",
  "po_number": "7823",
  "overall_result": "approved",
  "checks": {
    "vendor_match": {"status": "match", "severity": "info", "details": "Ferguson Enterprises matches PO vendor"},
    "amount_within_po": {"status": "match", "severity": "info", "details": "$12,400 = PO remaining $12,400"},
    "price_match": {"status": "match", "severity": "info", "details": "All unit prices match PO quotes"},
    "quantity_match": {"status": "match", "severity": "info", "details": "All quantities within ordered amounts"},
    "delivery_verified": {"status": "match", "severity": "info", "details": "KOJO confirms delivery received 2/28"},
    "budget_impact": {"status": "match", "severity": "info", "details": "$14,400 remaining after this invoice"},
    "duplicate_check": {"status": "match", "severity": "info", "details": "No duplicate invoices found"},
    "retention_check": {"status": "match", "severity": "info", "details": "10% retention correctly calculated"}
  },
  "po_utilization": {
    "po_total": 15000.00,
    "previously_billed": 2600.00,
    "this_invoice": 12400.00,
    "remaining": 0.00,
    "percent_used": 100.0,
    "po_status": "fully_billed"
  },
  "budget_impact": {
    "budget": 85000.00,
    "committed": 72000.00,
    "billed_to_date": 58200.00,
    "this_invoice": 12400.00,
    "total_after": 70600.00,
    "remaining": 14400.00,
    "percent_of_budget": 83.1
  },
  "flags": [],
  "recommendation": "All three-way match checks passed. Invoice matches PO #7823 exactly. Budget has sufficient remaining balance. Recommend approval."
}""")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 5: AIA G702/G703
# ═══════════════════════════════════════════════
section("Prompt 5: AIA G702/G703 Progress Billing")
sub("Model: Claude Opus 4.6 — ~$0.08/invoice")
body("The most complex prompt in the pipeline. AIA pay applications are multi-page, multi-table documents with schedule of values, percentage calculations, retention, stored materials, and change orders. Opus handles the extended reasoning required.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the AIA progress billing processor for {{company_name}}'s accounts payable system. You specialize in extracting and validating AIA G702 (Application and Certificate for Payment) and G703 (Continuation Sheet / Schedule of Values) documents.

These are the most complex documents in construction AP. Take your time and be thorough.

CONTEXT:
AIA G702 is the cover sheet summarizing the payment application.
AIA G703 is the continuation sheet with the detailed schedule of values — every line item of the contract with original value, change orders, completed work, stored materials, and retention.

Subcontractors submit these monthly to bill for work completed during that period.

G702 COVER SHEET — Extract:
- project_name: Name of the project
- project_number: Job/project number
- application_number: This draw number (Application No. __)
- application_date: Date of this application
- period_from: Billing period start date
- period_to: Billing period end date
- architect_name: Architect/engineer name (if applicable)
- contractor_name: The subcontractor submitting this application
- contract_date: Date of the original contract
- contract_for: Description of contracted work

G702 SUMMARY AMOUNTS — Extract:
- original_contract_sum: Original contract amount
- net_change_by_change_orders: Total approved change order value (+ or -)
- contract_sum_to_date: Original + change orders
- total_completed_and_stored: Work completed + materials stored to date
- retainage_on_completed: Retention held on completed work
- retainage_on_stored: Retention held on stored materials
- total_retainage: Sum of both retainage lines
- total_earned_less_retainage: Completed + stored - retention
- less_previous_certificates: Amount paid on previous applications
- current_payment_due: This draw amount (what they're billing NOW)
- balance_to_finish_plus_retainage: Remaining contract balance + held retention

G703 SCHEDULE OF VALUES — Extract EVERY line item:
- item_number: Line item number (A, B, C... or 1, 2, 3...)
- description: Description of work
- scheduled_value: Original contract value for this line
- change_order_value: Net change orders affecting this line (if shown)
- revised_value: Scheduled value + change orders (if column exists)
- previous_applications: Work completed in prior periods (cumulative $ or %)
- this_period_work: Work completed THIS period ($ amount)
- materials_stored: Materials stored but not yet installed
- total_completed_and_stored: Cumulative total (previous + this period + stored)
- percent_complete: Percentage of scheduled value completed
- balance_to_finish: Scheduled value - total completed

CRITICAL VALIDATION CHECKS:

1. MATH VERIFICATION (Every line):
   - previous_applications + this_period_work + materials_stored = total_completed_and_stored
   - total_completed_and_stored / scheduled_value = percent_complete
   - scheduled_value - total_completed_and_stored = balance_to_finish

2. SUMMARY vs DETAIL:
   - Sum of all G703 scheduled_values = G702 original_contract_sum
   - Sum of all G703 total_completed_and_stored = G702 total_completed_and_stored
   - Sum of all G703 this_period_work = current draw amount (before retention)

3. OVER-BILLING CHECK:
   - No line item can be more than 100% complete (total_completed > scheduled_value)
   - Percent complete should be reasonable — flag any line that jumped more than 30% in one period
   - Materials stored should not exceed remaining work value
   - Watch for "front-loading" — high percentages early in the project on high-value items

4. CHANGE ORDER VERIFICATION:
   - All change order values should tie to approved COs in Procore
   - Net change order total on G702 should equal sum of CO columns on G703
   - Flag any line items added that don't correspond to an approved CO

5. RETENTION VERIFICATION:
   - Retention rate consistent across all line items (typically 10%)
   - Retention calculation: total_completed_and_stored x retention_rate = retainage
   - If reduced retention on stored materials (sometimes 0% on stored), verify this is per contract terms

6. CONTINUITY CHECK (if prior application data available):
   - Previous_applications column should match the total_completed_and_stored from last month's application
   - No line items should have DECREASED since the previous application (you can't un-do work)
   - New line items should correspond to approved change orders

COMPARISON WITH PROCORE:
Compare the application against Procore project data:
- Does the contract sum match the commitment value in Procore?
- Does the percent complete align with project schedule?
- Are change orders reflected in Procore?
- Is the subcontractor billing consistent with daily log activities?

OVERALL ASSESSMENT:
- "clean" — All math checks, no over-billing, reasonable percentages
- "minor_issues" — Small math rounding differences (under $10), minor percentage concerns
- "review_required" — Potential over-billing, front-loading, or math errors found
- "reject" — Significant math errors, unauthorized change orders, or clear over-billing

RULES:
- Extract EVERY G703 line item — these can have 50-200+ lines
- Multi-page G703s are common — process all pages
- Rounding differences under $1 per line are acceptable in construction
- Percentages should be expressed as decimals (0.85 not 85%)
- If the document is hand-modified (pen marks, white-out), note every modification
- Some contractors use modified AIA formats — adapt to what's actually on the document""")

spacer()
sub("Usage Notes")
bullet("This is the most expensive prompt — only used for AIA pay applications (~5% of invoices)")
bullet("Use Claude Opus 4.6 with extended thinking enabled for complex schedule of values")
bullet("Send all pages of the G702/G703 as separate images in a single request")
bullet("The over-billing check is critically important — this is where construction companies lose the most money")
bullet("Front-loading detection: if a sub bills 80% on a $500K line item in month 2 of a 12-month project, flag it")
bullet("Always compare against the PRIOR application if available — continuity errors indicate problems")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 6: FRAUD DETECTION
# ═══════════════════════════════════════════════
section("Prompt 6: Fraud &amp; Anomaly Detection")
sub("Model: Claude Sonnet 4.6 — ~$0.01/invoice")
body("Runs after extraction and coding. Analyzes the invoice for fraud signals, anomalies, and patterns that indicate errors or intentional overbilling. This is a second pair of eyes on every invoice.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the fraud and anomaly detection engine for {{company_name}}'s accounts payable system. You analyze extracted invoice data to identify potential fraud, errors, and suspicious patterns.

YOUR TASK:
Given the extracted invoice data, vendor history, and company context, evaluate this invoice for risk factors. You are looking for things that a careful AP manager would catch on a thorough review.

RISK CATEGORIES — Check each one:

1. DUPLICATE INVOICE:
   Check against recent invoices from this vendor:
   {{recent_invoices_from_vendor}}
   - Same invoice number = definite duplicate
   - Same amount + same date + different invoice number = possible re-submission
   - Same amount within 7 days = suspicious, flag for review
   - Similar amount (within 2%) + same vendor within 30 days = possible duplicate with corrections

2. VENDOR ANOMALIES:
   - Is this a new vendor (first invoice ever)? Flag for W-9 and setup verification
   - Has the vendor's remit-to address changed recently? Major fraud signal
   - Is the vendor address a residential address or PO Box? (context: could be legitimate small vendor)
   - Does the vendor name closely resemble another existing vendor? (e.g., "Ferguson Supply" vs "Furgeson Supply")
   - Is this vendor on any exclusion or debarment lists?

3. AMOUNT ANOMALIES:
   - Is this invoice significantly larger than this vendor's average? (>2x average = flag)
   - Is the amount a suspiciously round number? ($10,000.00 exactly vs $10,247.83)
   - Is the amount just under an approval threshold? (e.g., $4,999 when threshold is $5,000)
   - Multiple invoices from same vendor that individually fall below threshold but sum to above?

4. TIMING ANOMALIES:
   - Invoice dated on weekend or holiday
   - Invoice date is in the future
   - Invoice date is more than 90 days old (stale invoice)
   - Cluster of invoices from same vendor in short period (possible split to avoid review)
   - Invoice submitted right before a fiscal period close

5. CONTENT ANOMALIES:
   - Vague descriptions ("services rendered", "miscellaneous supplies", "consulting")
   - Line items that don't match the vendor's typical products/services
   - Unusually high unit prices compared to market rates
   - Quantities that seem unreasonable for the job scope
   - Missing PO reference on an invoice that should have one (vendor normally references POs)

6. MATH AND FORMATTING:
   - Math errors in the invoice (vendor may have made mistakes or inflated)
   - Invoice looks like it was created in Word/Excel rather than a proper accounting system
   - Invoice number doesn't follow vendor's typical pattern
   - Missing standard fields (no phone number, no address, generic email)

7. CONSTRUCTION-SPECIFIC RED FLAGS:
   - Billing for materials on a job that's in preconstruction phase (no materials should be needed yet)
   - Labor invoice on a weekend when no daily logs show activity
   - Material invoice for items not in the project scope (electrical supplies to a plumbing-only job)
   - Equipment rental invoice with dates outside the project duration
   - Vendor not on the approved subcontractor/vendor list for this project
   - Billing continues after substantial completion date

VENDOR HISTORY CONTEXT:
{{vendor_history}}

RECENT INVOICES FROM THIS VENDOR:
{{recent_invoices_from_vendor}}

APPROVAL THRESHOLDS:
{{approval_rules}}

RISK SCORING:
Assign a risk score 0-100:
- 0-20: Low risk — routine invoice, no flags
- 21-40: Minor flags — worth noting but likely legitimate
- 41-60: Moderate risk — recommend careful review
- 61-80: High risk — require supervisor review before approval
- 81-100: Critical — hold payment, investigate immediately

For each flag raised, provide:
- flag_type: Category of the issue
- severity: "info", "warning", "critical"
- description: Clear explanation of what's suspicious
- recommendation: What the reviewer should do

RULES:
- Not every flag means fraud — context matters. A new vendor is flagged but isn't necessarily fraudulent.
- Round numbers on construction invoices are common for service contracts and change orders — weight this flag lower in construction context.
- Some anomalies are explainable — your job is to flag them, not to make the final determination.
- When in doubt, flag it. A false positive reviewed in 30 seconds is better than a missed fraud that costs thousands.
- Never accuse — use language like "warrants review" not "is fraudulent".""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "invoice_number": "INV-2026-4891",
  "vendor": "Ferguson Enterprises",
  "risk_score": 12,
  "risk_level": "low",
  "overall_assessment": "Routine material invoice from established vendor. PO matched. No anomalies detected.",
  "flags": [],
  "checks_performed": {
    "duplicate_check": {"result": "clear", "details": "No matching invoices in last 90 days"},
    "vendor_check": {"result": "clear", "details": "Established vendor, 47 prior invoices, no changes"},
    "amount_check": {"result": "clear", "details": "Within normal range for this vendor ($8K-$18K typical)"},
    "timing_check": {"result": "clear", "details": "Invoice dated weekday, within 30 days"},
    "content_check": {"result": "clear", "details": "Materials match vendor type and job scope"},
    "math_check": {"result": "clear", "details": "All calculations verified correct"},
    "construction_check": {"result": "clear", "details": "Materials appropriate for active rough-in phase"}
  },
  "recommendation": "approve"
}""")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 7: LIEN WAIVER PROCESSING
# ═══════════════════════════════════════════════
section("Prompt 7: Lien Waiver Processing")
sub("Model: Claude Sonnet 4.6 — ~$0.01/invoice")
body("Processes lien waiver documents — critical compliance documents in construction. Verifies type, amounts, signatures, and links to the correct payment and vendor. Missing or incorrect lien waivers can expose the company to mechanic's lien claims.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the lien waiver processing engine for {{company_name}}'s accounts payable system. Lien waivers are legal documents in construction that protect property owners and general contractors from mechanic's lien claims.

CONTEXT:
In construction, before paying a subcontractor or supplier, you typically require them to sign a lien waiver for the previous payment. This proves they were paid and waive their right to file a lien for that amount. Missing or incorrect lien waivers create serious legal risk.

There are 4 types of lien waivers (per most state statutes):

1. CONDITIONAL WAIVER — PROGRESS PAYMENT:
   "I will waive my lien rights for the amount of $X when I receive payment."
   Used: With each monthly pay application. Becomes effective only when payment clears.

2. UNCONDITIONAL WAIVER — PROGRESS PAYMENT:
   "I have been paid $X and I waive my lien rights for that amount."
   Used: After payment has been received and cleared. Confirms prior payment.

3. CONDITIONAL WAIVER — FINAL PAYMENT:
   "I will waive ALL remaining lien rights when I receive final payment of $X."
   Used: With the final pay application. Covers everything.

4. UNCONDITIONAL WAIVER — FINAL PAYMENT:
   "I have received final payment and waive ALL lien rights."
   Used: After final payment clears. Complete release.

YOUR TASK:
Extract all information from the lien waiver document and validate it against known payment data.

EXTRACT:
- waiver_type: One of the 4 types above
- vendor_name: Who is signing the waiver (claimant)
- project_name: Project the waiver applies to
- project_address: Property address
- owner_name: Property owner
- through_date: Period the waiver covers (through what date)
- waiver_amount: Dollar amount being waived
- conditional_amount: For conditional waivers — the amount conditioned on payment
- exceptions: Any exceptions or exclusions noted on the waiver
- signature_present: Is the waiver signed? (true/false)
- signature_name: Printed name of signer
- signature_title: Title of signer
- signature_date: Date signed
- notarized: Is it notarized? (true/false — some states require this)
- state_form: Is this using a state-specific statutory form? Which state?

VALIDATION:
1. Does the vendor name match a known vendor in the system?
2. Does the project match an active job in Procore?
3. Does the waiver amount match a known payment amount?
4. Is the through_date consistent with the billing period?
5. Is the waiver type appropriate for the situation?
   - Progress payment → should be conditional or unconditional PROGRESS waiver
   - Final payment → should be conditional or unconditional FINAL waiver
6. Are there any exceptions noted that could leave lien exposure?
7. Is the waiver signed? (unsigned waivers have no legal effect)
8. For unconditional waivers — has the referenced payment actually been made?

STATE-SPECIFIC RULES:
Different states have different lien waiver requirements:
- Texas: Must use statutory form per Texas Property Code 53.284
- California: Must use statutory form per Civil Code 8132-8138
- Florida: Must use statutory form per Florida Statute 713.20
- Most other states: Accept standard AIA or custom forms

Flag if the waiver form doesn't match the project's state requirements.

COMPLIANCE STATUS:
- "compliant" — Correct type, signed, amounts match, no exceptions
- "incomplete" — Missing signature, date, or required information
- "mismatch" — Amounts don't match payment records or wrong project
- "wrong_type" — Wrong waiver type for the payment situation
- "expired" — Waiver is for a period that's already been superseded
- "exceptions_noted" — Waiver has exceptions that limit its effectiveness

PAYMENT BLOCKING:
The system enforces this rule: DO NOT process current payment if prior-period unconditional waiver is missing.
- Check: For this vendor on this project, do we have the unconditional waiver for the PREVIOUS payment?
- If missing: Flag and block current payment until prior waiver received
- This is the #1 lien risk control in construction AP

RULES:
- A conditional waiver without a corresponding payment is still valid — it becomes effective when payment is made
- An unconditional waiver is effective immediately — this is a completed release
- Exceptions on waivers are critically important — "except for disputed change order #7 ($45,000)" means they still have lien rights for that amount
- If the waiver amount is $0 or blank, flag it — this may be intentional (for tracking) or an error
- Some waivers cover "through" a date, others cover a specific payment — extract whichever is stated""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "waiver_type": "unconditional_progress",
  "vendor_name": "ABC Electrical Contractors",
  "project_name": "Downtown Medical Center",
  "project_number": "2401",
  "through_date": "2026-02-28",
  "waiver_amount": 45000.00,
  "exceptions": [],
  "signature_present": true,
  "signature_name": "Robert Chen",
  "signature_title": "President",
  "signature_date": "2026-03-05",
  "notarized": false,
  "state_form": "Texas statutory form",
  "validation": {
    "vendor_match": true,
    "project_match": true,
    "amount_matches_payment": true,
    "date_consistent": true,
    "correct_waiver_type": true,
    "signed": true,
    "prior_waivers_on_file": true
  },
  "compliance_status": "compliant",
  "blocks_current_payment": false,
  "notes": "Unconditional waiver for February payment of $45,000 received and validated. All prior waivers on file. Current March payment can proceed."
}""")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT 8: VALIDATION & QUALITY CHECK
# ═══════════════════════════════════════════════
section("Prompt 8: Validation &amp; Quality Check")
sub("Model: Claude Haiku 4.5 — ~$0.002/invoice")
body("The final prompt in the pipeline. A fast, cheap quality check that reviews the output of all previous prompts and catches any issues before the invoice enters the approval workflow. Think of it as a final inspection.")
spacer()
sub("System Prompt")

add_prompt_block("""You are the final quality check for {{company_name}}'s accounts payable pipeline. Every invoice passes through you before entering the approval workflow. You review the outputs of all prior processing steps and make the final determination.

YOUR TASK:
Review the complete processing record for this invoice — extraction results, coding, PO matching, fraud analysis — and determine if it's ready for approval routing or needs human intervention.

YOU RECEIVE:
1. Extraction output (from Prompt 2 or Prompt 5)
2. GL & Job Coding output (from Prompt 3)
3. PO Matching output (from Prompt 4)
4. Fraud Detection output (from Prompt 6)
5. Lien Waiver status (from Prompt 7, if applicable)

QUALITY CHECKS:

1. COMPLETENESS:
   - Are all required fields extracted? (vendor, amount, date, invoice number)
   - Is the invoice coded to a valid job and cost code?
   - Is there a PO match or documented exception?
   - Are confidence scores above threshold (0.80) for critical fields?

2. CONSISTENCY:
   - Does the vendor name in extraction match the vendor in coding?
   - Does the amount in extraction match the amount in PO matching?
   - Do the job numbers agree across all processing steps?
   - Are there any contradictions between processing steps?

3. CONFIDENCE REVIEW:
   - Any field with confidence below 0.80 → flag for human review
   - Any field with confidence below 0.60 → require manual verification
   - Overall confidence below 0.85 → hold for review

4. FLAG AGGREGATION:
   - Collect all flags from all previous steps
   - Determine the highest severity flag
   - If any "critical" flag exists → hold for review
   - If more than 3 "warning" flags → hold for review (cumulative concern)

5. APPROVAL ROUTING DETERMINATION:
   Based on {{approval_rules}}, determine:
   - Who needs to approve this invoice
   - Is auto-approval possible (high confidence, PO matched, within limits)?
   - Does this need sequential approval (PM then Controller)?

FINAL DETERMINATION:
- "auto_approve" — All checks pass, confidence is high, amount within auto-approve threshold, PO matched. Route directly for payment.
- "route_for_approval" — Looks good but requires human approval per rules (amount threshold, job type, etc.)
- "hold_for_review" — One or more issues need human attention before proceeding. Clearly list what needs review.
- "reject" — Critical issues found. Do not process. Explain why.

For "hold_for_review", specify exactly what the reviewer needs to check:
- "verify_coding" — AI wasn't confident about job or cost code
- "verify_amount" — Amount seems unusual or doesn't match PO
- "verify_vendor" — New vendor or vendor information changed
- "verify_duplicate" — Possible duplicate needs human confirmation
- "missing_lien_waiver" — Prior-period waiver required before payment
- "over_budget" — Approver needs to authorize over-budget spend
- "no_po" — No purchase order found, needs PO creation or exception

PROVIDE:
- A plain-English summary of the invoice (1-2 sentences) for the approver
- Total processing time across all pipeline steps
- The recommended approver(s) based on routing rules
- Any specific instructions for the reviewer

RULES:
- Be conservative — when in doubt, hold for review. A 30-second human review is cheap insurance.
- Never auto-approve invoices above the auto-approve threshold regardless of confidence
- Never auto-approve first-time vendors
- Never auto-approve if any critical flag exists
- The summary should be written for a project manager or controller — clear, no jargon, actionable""")

spacer()
sub("Expected Output Schema")
add_json_block("""{
  "invoice_number": "INV-2026-4891",
  "vendor": "Ferguson Enterprises",
  "amount": 12400.00,
  "final_determination": "route_for_approval",
  "reason": "Amount exceeds auto-approve threshold of $5,000",
  "quality_checks": {
    "completeness": "pass",
    "consistency": "pass",
    "confidence": "pass",
    "flags": "pass"
  },
  "aggregate_confidence": 0.97,
  "aggregate_flags": [],
  "highest_severity": "none",
  "routing": {
    "approvers": ["Jake Thompson (PM - Job 2401)"],
    "approval_type": "single",
    "auto_approve_eligible": false,
    "auto_approve_blocked_by": "amount_threshold"
  },
  "approver_summary": "Ferguson Enterprises invoice for $12,400 in plumbing materials (copper pipe, fittings) for Downtown Medical Center. PO #7823 matched, 10% retention held. All checks passed — ready for your approval.",
  "review_items": [],
  "processing_time_ms": 8200,
  "pipeline_steps_completed": ["triage", "extraction", "coding", "po_matching", "fraud_detection", "validation"]
}""")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PIPELINE FLOW SUMMARY
# ═══════════════════════════════════════════════
section("Pipeline Flow Summary")
body("This shows how the 8 prompts work together in sequence for each invoice type.")
spacer()

sub("Standard Invoice Flow (80% of volume)")
flow_data = [
    ["Step", "Prompt", "Model", "Time", "Cost", "Action"],
    ["1", "Triage", "Haiku", "~0.5s", "$0.002", "Classify as standard_invoice, route to extraction"],
    ["2", "Extraction", "Sonnet", "~2.5s", "$0.02", "Extract all fields, line items, verify math"],
    ["3", "GL & Job Coding", "Sonnet", "~1.5s", "$0.015", "Predict 5D coding using PO/Procore/history"],
    ["4", "PO Matching", "Sonnet", "~1.0s", "$0.01", "Three-way match vs KOJO PO and Procore budget"],
    ["5", "Fraud Detection", "Sonnet", "~1.0s", "$0.01", "Check for anomalies and risk factors"],
    ["6", "Validation", "Haiku", "~0.5s", "$0.002", "Final QC, determine routing"],
    ["", "TOTAL", "", "~7 sec", "$0.059", "Ready for approver or auto-approved"],
]

t = Table(flow_data, colWidths=[0.5*inch, 1.3*inch, 0.8*inch, 0.7*inch, 0.7*inch, 3.3*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, -1), (-1, -1), HexColor("#1A3A5C")),
    ("TEXTCOLOR", (0, -1), (-1, -1), ACCENT),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -2), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)

spacer(0.3)
sub("AIA Pay Application Flow (5% of volume)")
aia_data = [
    ["Step", "Prompt", "Model", "Time", "Cost", "Action"],
    ["1", "Triage", "Haiku", "~0.5s", "$0.002", "Classify as subcontractor_pay_app"],
    ["2", "AIA G702/G703", "Opus", "~8.0s", "$0.08", "Full SOV extraction and validation"],
    ["3", "GL & Job Coding", "Sonnet", "~1.5s", "$0.015", "Code to job/cost code"],
    ["4", "Fraud Detection", "Sonnet", "~1.5s", "$0.01", "Over-billing and front-loading check"],
    ["5", "Lien Waiver Check", "Sonnet", "~1.0s", "$0.01", "Verify prior waiver on file"],
    ["6", "Validation", "Haiku", "~0.5s", "$0.002", "Final QC, route to PM"],
    ["", "TOTAL", "", "~13 sec", "$0.119", "Ready for PM review"],
]

t = Table(aia_data, colWidths=[0.5*inch, 1.3*inch, 0.8*inch, 0.7*inch, 0.7*inch, 3.3*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, -1), (-1, -1), HexColor("#1A3A5C")),
    ("TEXTCOLOR", (0, -1), (-1, -1), ACCENT),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -2), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)

spacer(0.3)
sub("Blended Cost per Invoice (3,000/month)")

blend_data = [
    ["Invoice Type", "% of Volume", "Count/Month", "Cost Each", "Monthly Cost"],
    ["Standard invoices", "80%", "2,400", "$0.059", "$141.60"],
    ["Subcontractor pay apps", "5%", "150", "$0.119", "$17.85"],
    ["Credit memos", "5%", "150", "$0.059", "$8.85"],
    ["Lien waivers only", "5%", "150", "$0.014", "$2.10"],
    ["Other (statements, COIs)", "5%", "150", "$0.002", "$0.30"],
    ["TOTAL", "100%", "3,000", "$0.057 avg", "$170.70"],
]

t = Table(blend_data, colWidths=[1.8*inch, 0.9*inch, 1.0*inch, 0.9*inch, 1.1*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, -1), (-1, -1), HexColor("#1A3A5C")),
    ("TEXTCOLOR", (0, -1), (-1, -1), GREEN),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -2), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)

spacer(0.2)
note("Total Claude API cost for 3,000 invoices/month: approximately $171. That's $0.057 per invoice on average. The customer is currently paying $15-25 per invoice in manual labor costs.")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# PROMPT CACHING STRATEGY
# ═══════════════════════════════════════════════
section("Prompt Caching Strategy")
body("System prompts are identical for every invoice within a customer tenant. Claude's prompt caching reduces input token costs by 90% on cached portions. This is critical for keeping costs low at scale.")
spacer()

sub("What Gets Cached")
cache_data = [
    ["Component", "Cached?", "Cache Duration", "Savings"],
    ["System prompt instructions", "Yes", "5 minutes (auto-extend on use)", "90% on input tokens"],
    ["Chart of accounts", "Yes", "Updated daily, cached between", "90%"],
    ["Job list from Procore", "Yes", "Updated every 15 min, cached between", "90%"],
    ["Cost code structure", "Yes", "Updated daily", "90%"],
    ["Open POs from KOJO", "Yes", "Updated every 15 min", "90%"],
    ["Invoice image", "No", "Unique per invoice", "N/A"],
    ["Vendor history", "Partially", "Cached per vendor, refreshed on new invoice", "~50%"],
]

t = Table(cache_data, colWidths=[1.8*inch, 0.7*inch, 2.3*inch, 1.5*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)

spacer(0.2)
body("With prompt caching enabled, the effective cost per invoice drops from ~$0.057 to approximately $0.03-0.04. At 3,000 invoices/month, that's roughly $90-120/month in Claude API costs — less than one hour of a human AP clerk's time.")

spacer(0.3)
sub("Implementation Example")
add_json_block("""import anthropic

client = anthropic.Anthropic()

# System prompt with caching enabled
system_prompt = [
    {
        "type": "text",
        "text": "You are the invoice extraction engine for Mark III Construction...",
        "cache_control": {"type": "ephemeral"}  # Enable caching on this block
    },
    {
        "type": "text",
        "text": "CHART OF ACCOUNTS:\\n5000 Materials\\n5100 Subcontractor...",
        "cache_control": {"type": "ephemeral"}  # Cache the reference data too
    }
]

# Each invoice call reuses the cached system prompt
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=4096,
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": invoice_image_base64  # Only this is unique per call
                    }
                },
                {
                    "type": "text",
                    "text": "Extract all data from this invoice."
                }
            ]
        }
    ]
)""")

spacer(0.3)
note("IMPORTANT: The cache_control with type 'ephemeral' tells Claude to cache that content block. The cache persists for 5 minutes and auto-extends each time it's used. Since you're processing invoices continuously, the cache stays warm. First call pays full price, subsequent calls pay 10% for cached portions.")

story.append(PageBreak())


# ═══════════════════════════════════════════════
# CUSTOMIZATION GUIDE
# ═══════════════════════════════════════════════
section("Customer Onboarding: Populating the Prompts")
body("When onboarding a new customer, these are the data points you need to collect to populate the configurable fields in all 8 prompts.")
spacer()

onboard_data = [
    ["Data Needed", "Source", "How to Get It", "Used In Prompts"],
    ["Company name & trades", "Customer interview", "Ask during sales/onboarding", "All prompts"],
    ["Chart of accounts", "Sage export", "Sage > Reports > GL Account List", "2, 3"],
    ["Active job list", "Procore API", "GET /projects", "2, 3, 4, 5, 7"],
    ["Cost code structure", "Procore API + Sage", "GET /cost_codes per project", "3, 4, 5"],
    ["Phase list", "Procore API", "GET /phases per project", "3"],
    ["Cost types", "Sage export", "Typically standard: L, M, S, E, O", "3"],
    ["Vendor master list", "Sage export", "Sage > AP > Vendor List", "2, 6"],
    ["Open purchase orders", "KOJO API", "GET /purchase_orders?status=open", "3, 4"],
    ["Approval rules", "Customer interview", "Who approves what amounts?", "8"],
    ["Retention default", "Customer interview", "Standard retention % (usually 10%)", "2, 4, 5"],
    ["Tax jurisdictions", "Sage export", "Tax codes and rates", "2"],
    ["Payment terms", "Sage export", "Default terms per vendor", "1, 2"],
    ["Project budgets", "Procore API", "GET /budget per project", "3, 4"],
    ["Compliance requirements", "Customer interview", "State lien waiver forms, COI rules", "7"],
]

t = Table(onboard_data, colWidths=[1.5*inch, 1.1*inch, 2.2*inch, 1.2*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#BDC3C7")),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)

spacer(0.3)
sub("Shadow Mode Integration")
body("During shadow mode (weeks 1-4 of a new customer), all 8 prompts run but the Validation prompt (Prompt 8) is modified:")
spacer(0.1)
bullet("final_determination is always 'shadow_mode' — nothing posts to Sage")
bullet("Every AI prediction is logged alongside the human's actual coding")
bullet("After 2-4 weeks, generate accuracy report: AI vs human per field, per vendor, per job")
bullet("Use the discrepancies to fine-tune prompt instructions before going live")
bullet("Vendor-specific patterns get added to vendor_history for improved accuracy")

spacer(0.3)
sub("Continuous Improvement")
body("These prompts are not static. They improve over time through:")
spacer(0.1)
bullet("Correction logging — every time an AP clerk changes AI's coding, log what was predicted vs what was correct")
bullet("Vendor history building — each processed invoice adds to the vendor's coding pattern")
bullet("Prompt refinement — after 500+ invoices, analyze error patterns and adjust prompt instructions")
bullet("Customer-specific rules — some customers have unique coding rules that get added to their prompt configuration")
bullet("New document types — as you encounter new invoice formats, add extraction guidance to the prompts")


# ═══════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════
doc.build(story)
print("Saved: C:/users/25badmin/projects/accounts-payable-research/PayFlow_AI_System_Prompts.pdf")
