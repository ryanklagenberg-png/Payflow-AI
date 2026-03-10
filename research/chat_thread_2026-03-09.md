# PayFlow AI — Q&A Thread
## Date: March 9, 2026

---

## Topics Covered

### 1. Accounts Payable vs Accounts Receivable
- AP = money you owe to others (liability). AR = money owed to you (asset).
- In construction: AP is paying subs/suppliers, AR is billing project owners.
- PayFlow AI focuses on the AP side.

### 2. How PayFlow AI Knows How to Code Invoices
- Pulls job list, cost codes, and phases from Procore and Sage
- Uses invoice clues: PO numbers (links to KOJO), job references, vendor history, material type, delivery address, contract matching
- Learns from AP clerk corrections over time
- Confidence scoring: 95%+ auto-route, 80-94% clerk reviews, <80% flagged for manual coding
- 5-dimensional coding: GL Account + Job + Phase + Cost Code + Cost Type
- Expected results: ~80% auto-coded correctly, ~15% need quick review, ~5% manual

### 3. KOJO Integration
- Mark III uses KOJO for issuing purchase orders
- Decision: Integrate with KOJO, do NOT build our own PO system (scope creep)
- KOJO provides: PO numbers, materials, delivery status, vendor quotes, change orders, order history, buyout tracking
- Enables: instant PO matching, price verification, delivery confirmation, remaining balance tracking, auto-coding from PO data
- Creates the procurement-to-payment triangle: KOJO (procurement) → PayFlow AI (AP) → Sage (accounting), with Procore (project mgmt) feeding data
- Need to verify KOJO has a public API (likely yes, modern SaaS platform)
- This is a competitive advantage — generic AP tools don't integrate with construction procurement platforms

### 4. How It Works PowerPoint (18 slides generated)
- File: PayFlow_AI_How_It_Works.pptx
- Generator: generate_how_it_works.py
- Covers the complete 7-step invoice lifecycle:
  1. Invoice Intake (email, upload, scanner, KOJO)
  2. AI Extraction (Claude reads every field)
  3. Intelligent Job Coding (5D auto-coding)
  4. Three-Way Matching (invoice vs KOJO PO vs Procore budget)
  5. Validation & Fraud Detection
  6. Approval Routing (9 configurable rules)
  7. Sage 300 CRE Posting
- Deep dives: KOJO integration, Procore integration
- Other integrations slide: Textura, Viewpoint, CMiC, DocuSign, myCOI, QuickBooks, Microsoft 365, PlanGrid, LevelSet, Banking APIs (Plaid)
- Construction-specific features: AIA G702/G703, lien waivers, retention, certified payroll, compliance dashboard, change order workflow
- Real example: Ferguson Supply invoice traced from 9:02 AM to 9:15 AM (13 min, 0 manual entry)
- Shadow mode explanation
- Data flow architecture diagram
- Security & compliance slide

### 5. Will PayFlow Make Payments?
- Not initially — payment execution is a banking function with heavy regulatory requirements
- Money transmitter licenses, PCI compliance, fraud liability, positive pay files
- Sage already handles payment runs — deeply embedded workflow
- PayFlow AI stops at "approved and posted to Sage"
- Phase 2: Payment intelligence (discount alerts, cash flow timing, payment prioritization, retention release scheduling)
- Phase 3 (future): Optional payment execution via banking APIs (Plaid/Dwolla) with proper licensing
- Smart sequence: get AP automation right first, then add payment intelligence, then optional payment execution

### 6. How PayFlow Communicates with Procore, KOJO, and Sage
- **Procore**: REST API, OAuth 2.0 authentication, well-documented at developers.procore.com, JSON data format, 3,600 requests/hour, 15-minute sync cycle
- **KOJO**: Needs verification — likely REST API or webhooks (modern SaaS platform). Fallback options: CSV export, browser automation. First action: contact KOJO team about API availability.
- **Sage 300 CRE**: Hardest integration. On-premise system, no clean cloud API. Options: ODBC/SDK direct connection, Sage Intacct API (if cloud), Ryvit middleware, CSV import/export. Likely approach: small connector agent installed on customer's network, connects to Sage locally, syncs to PayFlow cloud over HTTPS. This is Phase 4 (weeks 11-14) and the most development time.
- All three sync on 15-minute cycles, with immediate push for approved invoices to Sage
- Fault tolerance: each system can be down independently without losing invoices

### 7. Code Security / Locking Down
- Private GitHub repo, branch protection, access control
- Secrets management (#1 mistake): never hardcode API keys, use AWS Secrets Manager or environment variables
- Code obfuscation not needed for cloud SaaS — customers never see backend code
- Real IP is in AI prompts, matching algorithms, and training data
- What to protect: AI system prompts (server-side only), integration credentials (secrets manager, rotate 90 days), customer data (AES-256, TLS 1.3, per-tenant isolation), source code (private repo), Sage connector (signed binary, certificate pinning), database (private network, encrypted), API endpoints (auth required, rate limiting)
- Legal IP protection: copyright (automatic), trade secrets (NDAs), trademark ("PayFlow AI" — file with USPTO), patent (possibly — 5D coding, shadow mode), Terms of Service
- Employee/contractor security: NDAs, IP assignment, least-privilege, revoke on departure, code review
- Priority order: secrets management → encryption → access control → SOC 2 → trademark → patent

### 8. AWS Hosting Decision
- Do NOT host on Mark III's servers — not scalable, lose control, update nightmare, security liability
- Host on AWS (same as Procore)
- Architecture: ECS Fargate (app), RDS PostgreSQL (database), S3 (invoice files), ElastiCache Redis (queues/cache), ALB (load balancer), CloudFront (CDN), SES (email intake), all in private subnets
- Multi-tenant architecture — all customers share one deployment, data isolated by tenant_id
- Only the Sage connector agent sits on customer's network
- Monthly costs: Stage 1 (1 customer) ~$440-640, Stage 2 (5 customers) ~$1,230-1,590, Stage 3 (20 customers) ~$3,840-4,810
- Profitable at 1 customer paying $1,500/month
- Development cost: ~$50/month (local Docker, small Claude API testing)
- URLs: app.payflowai.com, api.payflowai.com, invoices@{company}.payflowai.com

### 9. AWS Security (Layer by Layer)
- Layer 1: Network — private subnets, database never publicly accessible, only port 443 open
- Layer 2: IAM — MFA required, least-privilege policies, root account locked
- Layer 3: Encryption — TLS 1.3 in transit, AES-256 at rest (RDS, S3, backups, secrets)
- Layer 4: Application — bcrypt passwords, MFA for admin, JWT sessions, parameterized queries (no SQL injection), CSRF protection, rate limiting, input validation, file upload validation
- Layer 5: Multi-tenant isolation — every query scoped by tenant_id
- Layer 6: Monitoring — CloudTrail, GuardDuty, CloudWatch, WAF, VPC Flow Logs, application audit logs
- Layer 7: Backup — daily snapshots (30-day retention), point-in-time recovery, S3 versioning, cross-region backup, infrastructure as code
- Layer 8: Compliance — SOC 2, audit trails, 7-year data retention, right to delete, annual pentest
- Layer 9: Sage connector — TLS 1.3, certificate pinning, signed binary, minimal permissions, encrypted credentials
- Security services cost: ~$30-75/month on AWS
- Priority checklist: pre-launch must-haves, 3-month should-haves, first-year nice-to-haves

### 10. Monthly AWS Cost Breakdown
- Stage 1 (Mark III only, 3,000 invoices): AWS ~$260-455 + Claude API ~$180 = $440-640/month total
- Stage 2 (5 customers, 12,000 invoices): ~$1,230-1,590/month
- Stage 3 (20 customers, 50,000 invoices): ~$3,840-4,810/month
- Non-AWS costs: GitHub $4, business insurance $100-200, LLC fees ~$50 amortized, accounting software $30-60, SOC 2 $400-800 amortized, pentest $200-400 amortized
- Margins improve with scale — infrastructure costs don't double per customer
- During development: $0-50/month (local Docker, small API testing)
- Breakeven: 1 customer at $1,500/month

### 11. Professional-Grade System Prompts (8 prompts created)
- File: PayFlow_AI_System_Prompts.pdf
- Generator: system_prompts.py
- Questions asked for better prompts (user will get answers in next few days):
  - Cost code format (CSI MasterFormat or custom?)
  - GL account numbering range
  - Standard retention percentage
  - Approval thresholds by dollar amount
  - Tax jurisdiction details
  - Common invoice types and volume split
  - Common vendors
  - Payment terms
  - Current AP workflow (who touches invoices, how many clerks)
  - How invoices arrive today
- All prompts built with configurable {{placeholder}} fields for any customer

#### The 8 Prompts:
1. **Invoice Triage** (Haiku 4.5, ~$0.002) — Classifies document type (11 types), determines urgency, routes to correct pipeline, detects early-pay discounts, catches continuation pages
2. **Invoice Extraction** (Sonnet 4.6, ~$0.02) — Extracts vendor info, header, all line items, totals, tax, retention, references. Built-in math verification. Confidence scoring per field group. Construction-specific fields (retention, progress billing, lien waiver, prevailing wage, bonded project)
3. **GL & Job Coding** (Sonnet 4.6, ~$0.015) — 5D prediction using 6 matching signals in priority order: PO match (highest), job reference, ship-to address, vendor history, material analysis, GL prediction. Budget awareness. Split coding support. Top-3 alternatives when uncertain.
4. **PO Matching** (Sonnet 4.6, ~$0.01) — Three-way match: invoice vs KOJO PO vs Procore budget. Checks: vendor, amount, price per line, quantity, delivery verification, budget impact, duplicate, retention. Cumulative PO utilization tracking.
5. **AIA G702/G703** (Opus 4.6, ~$0.08) — Full G702 cover sheet + G703 schedule of values extraction. Math verification per line. Over-billing and front-loading detection. Change order verification. Retention verification. Continuity check against prior applications.
6. **Fraud Detection** (Sonnet 4.6, ~$0.01) — 7 risk categories: duplicate, vendor anomalies, amount anomalies, timing, content, math/formatting, construction-specific red flags. Risk score 0-100. Construction context (job phase vs material type, daily log cross-reference).
7. **Lien Waiver** (Sonnet 4.6, ~$0.01) — All 4 waiver types. State-specific statutory form validation (TX, CA, FL). Payment blocking rule: no current payment without prior unconditional waiver. Exception tracking.
8. **Validation** (Haiku 4.5, ~$0.002) — Final QC across all pipeline outputs. Completeness, consistency, confidence review, flag aggregation. Determines: auto_approve, route_for_approval, hold_for_review, or reject. Plain-English summary for approvers.

#### Also in the PDF:
- Configurable fields reference (15 placeholders)
- Pipeline flow for standard invoices (7 sec, $0.059) vs AIA pay apps (13 sec, $0.119)
- Blended cost: $0.057/invoice average, ~$171/month for 3,000 invoices
- Prompt caching strategy (40-50% additional savings)
- Implementation code example with cache_control
- Customer onboarding data collection guide
- Shadow mode integration notes
- Continuous improvement process

---

## Files Generated This Session
- `PayFlow_AI_How_It_Works.pptx` — 18-slide step-by-step presentation
- `generate_how_it_works.py` — Generator script for How It Works deck
- `PayFlow_AI_System_Prompts.pdf` — All 8 production system prompts
- `system_prompts.py` — Generator script for prompts PDF
- `PayFlow_AI_Sales_Deck_v3.pptx` — 16-slide CFO sales deck (generated from prior session's script)
- `chat_thread_2026-03-09.md` — This file

---

## Pending / Next Steps
- Get answers from Mark III about: cost code format, GL numbering, retention %, approval thresholds, tax jurisdictions, common invoice types, common vendors, payment terms, current AP workflow, how invoices arrive
- Verify KOJO has a public API
- Populate prompt {{placeholders}} with Mark III's actual data
- Begin Phase 1 development: project scaffolding, invoice upload, Claude API integration
- Register payflowai.com domain
- File LLC
- Secure trademark for "PayFlow AI"

---

## All Files in Project (Cumulative)
1. `AP_AI_Software_Research_2026.pdf` — Market research document
2. `generate_report.py` — Market research PDF generator
3. `Claude_API_AP_Integration_Guide_2026.pdf` — Claude API technical guide
4. `generate_claude_api_report.py` — Claude API guide generator
5. `prototype/index.html` — Clickable HTML/CSS/JS prototype (8 pages)
6. `chat_thread_2026-03-06.md` — First conversation log
7. `legal_considerations.md` — Legal issues and compliance
8. `competitive_analysis.md` — Stampli, Vic.ai, Adaptive analysis
9. `Competitive_Analysis_2026.pdf` — Competitive analysis PDF
10. `generate_competitive_analysis_report.py` — Competitive analysis generator
11. `mark_iii_pilot_customer.md` — Pilot customer profile
12. `development_timeline.md` — 7-phase development timeline
13. `procore_marketplace_strategy.md` — Procore App Marketplace strategy
14. `PayFlow_AI_Sales_Deck.pptx` — V1 sales deck (12 slides)
15. `generate_sales_deck.py` — V1 sales deck generator
16. `PayFlow_AI_Sales_Deck_v2.pptx` — V2 sales deck with charts (13 slides)
17. `generate_sales_deck_v2.py` — V2 sales deck generator
18. `PayFlow_AI_Sales_Deck_v3.pptx` — V3 CFO-focused deck (16 slides)
19. `generate_sales_deck_v3.py` — V3 sales deck generator
20. `PayFlow_AI_How_It_Works.pptx` — How It Works deck (18 slides)
21. `generate_how_it_works.py` — How It Works generator
22. `PayFlow_AI_System_Prompts.pdf` — 8 production system prompts
23. `system_prompts.py` — System prompts PDF generator
24. `chat_thread_2026-03-09.md` — This conversation log
