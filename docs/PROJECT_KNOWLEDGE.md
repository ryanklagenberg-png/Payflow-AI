# PayFlow AI - Project Knowledge Base

## Overview
AI-powered Accounts Payable automation SaaS, purpose-built for the construction industry.

**Target customer:** Construction companies (mechanical, electrical, plumbing, service, underground, manufacturing) processing high invoice volumes.

**Founder:** Ryan Klagenberg

---

## Business Case

### Problem
- Manual AP processing costs $15-20 per invoice
- Construction AP is uniquely complex (job costing, AIA billing, retention, lien waivers)
- No existing vendor combines best-in-class agentic AI with comprehensive construction AP workflows

### Solution
PayFlow AI uses Claude API to automate invoice ingestion, extraction, GL/job coding, PO matching, and approval routing — with construction-specific features no competitor offers.

### ROI (Mark III example — 3,000 invoices/mo)
- Current cost: $576K/year ($16/invoice)
- With PayFlow AI: $114K/year
- **Savings: $462K/year**
- PayFlow revenue: $18K/year ($1,500/mo Professional tier)
- PayFlow cost: $1,020/year (AI + infra)
- **94% gross margin**

---

## Pricing Model

| Tier | Price/mo |
|------|----------|
| Starter | $500 |
| Professional | $1,500 |
| Enterprise | Custom |

**Unit economics:** ~$0.06/invoice cost, $15-20/invoice customer savings. At 30+ customers: ~$0.012/invoice.

---

## Competitive Landscape

| Competitor | Strength | Weakness |
|-----------|----------|----------|
| **Stampli** (Billy the Bot) | 83M hrs training, 200+ ERP integrations | Not construction-specific |
| **Vic.ai** | 535M+ invoices, 84% no-touch rate | No construction focus, enterprise-only |
| **Adaptive** | Construction-first, a16z-backed | Limited AI, QuickBooks only, $575/mo min |

**PayFlow AI positioning:** Latest AI (Claude) + construction-specific + flexible pricing. Gap: zero production data, no integrations built yet, no brand recognition.

---

## Technical Architecture

### Tech Stack
- **Backend:** Python (FastAPI or NestJS — TBD)
- **Database:** PostgreSQL
- **AI:** Claude API (Anthropic)
- **Storage:** AWS S3 (invoices/documents)
- **Frontend:** React/Next.js
- **Infrastructure:** AWS (ECS Fargate, RDS, S3, ElastiCache Redis, ALB, CloudFront)
- **Containerization:** Docker

### AI Model Strategy (Tiered)

| Model | Use Case | % of Invoices | Cost/Invoice |
|-------|----------|---------------|-------------|
| Haiku 4.5 | Clean, standard invoices | 80% | $0.0035 |
| Sonnet 4.6 | Complex, multi-page | 15% | $0.0106 |
| Opus 4.6 | Exceptions, fraud analysis | 5% | $0.0177 |

**Blended cost: ~$0.005/invoice** (half a penny). With prompt caching: ~$0.003/invoice.

### 8 AI System Prompts Designed

| # | Prompt | Model | Cost/Invoice |
|---|--------|-------|-------------|
| 1 | Invoice Triage | Haiku 4.5 | $0.002 |
| 2 | Invoice Extraction | Sonnet 4.6 | $0.02 |
| 3 | GL & Job Coding | Sonnet 4.6 | $0.015 |
| 4 | PO Matching | Sonnet 4.6 | $0.01 |
| 5 | AIA G702/G703 Processing | Opus 4.6 | $0.08 |
| 6 | Fraud Detection | Sonnet 4.6 | $0.01 |
| 7 | Lien Waiver Processing | Sonnet 4.6 | $0.01 |
| 8 | Final Validation | Haiku 4.5 | $0.002 |

Full prompts documented in `research/PayFlow_AI_System_Prompts.pdf`.

### AWS Cost Estimates

| Stage | Customers | Monthly Cost |
|-------|-----------|-------------|
| Stage 1 | 1 | $440-640 |
| Stage 2 | 5 | $1,230-1,590 |
| Stage 3 | 20 | $3,840-4,810 |

### Security (9 Layers)
1. Network Security (VPC, private subnets, ALB only)
2. Identity & Access (IAM, MFA)
3. Data Encryption (AES-256 at rest, TLS 1.3 in transit)
4. Application Security (bcrypt, JWT, parameterized queries, CSRF, rate limiting)
5. Multi-Tenant Isolation (tenant_id on every query)
6. Monitoring (CloudTrail, GuardDuty, WAF, CloudWatch)
7. Backup & Recovery (daily snapshots, cross-region)
8. Compliance (SOC 2, audit trails)
9. Sage Connector Security (TLS 1.3, certificate pinning)

---

## Construction-Specific Features (Key Differentiator)

1. **AIA Progress Billing** (G702/G703 forms)
2. **Retention/Retainage tracking** (5-10% withheld per invoice)
3. **Lien Waiver Management** (4 types, state-specific)
4. **5-Dimensional Job Costing** (GL + Job + Phase + Cost Code + Cost Type)
5. **Change Order Tracking** (evolving contract values)
6. **Compliance Documents** (COIs, W-9s, safety certs)
7. **Prevailing Wage / Certified Payroll**
8. **Multi-Entity / Multi-Job splitting**
9. **Material vs. Labor vs. Equipment breakdown** (tax implications)
10. **Back-Charge Detection**

---

## Integrations

### Three-System Integration (Core)
- **KOJO** (Procurement): POs, materials, vendors
- **Procore** (Project Mgmt): Jobs, budgets, contracts — REST API, OAuth 2.0
- **Sage 300 CRE** (Accounting): GL, payments — requires on-premise connector agent (ODBC/SDK)

### Additional Planned
Textura, Viewpoint, CMiC, DocuSign, myCOI, LevelSet, Plaid, PlanGrid, QuickBooks

### Procore Marketplace Strategy
- Join Developer Program (free)
- Build integration via REST API + OAuth 2.0
- **Critical rule:** Cannot use Procore data to train AI models (fine — we process invoice docs)
- Target listing: ~Month 7-8

---

## CFO Value-Add Features

1. Cash Flow Forecasting
2. Early Payment Discount Optimization ($50-100K/yr potential)
3. Vendor Spend Analytics
4. Over/Under Billing Report (WIP reporting)
5. Bonding Capacity Impact
6. AP Aging Dashboard
7. Job Profitability Alerts
8. Tax Optimization (sales tax exemptions)
9. Audit-Ready Package (one-click)
10. Vendor Scorecard

---

## Pilot Customer: Mark III Construction

- **Trades:** Mechanical, Electrical, Plumbing, Underground, Service
- **Systems:** Sage (likely 300 CRE), Procore, KOJO
- **Volume:** ~3,000 invoices/month
- **Connection:** Ryan's wife works there

### 14 Discovery Questions (Pending)
1. What version of Sage? (100, 300 CRE, Intacct?)
2. How are cost codes formatted? (XX-XXXX-XX?)
3. How many active jobs at a time?
4. Who approves invoices and what's the routing?
5. What types of invoices? (material, subcontractor, equipment rental, AIA?)
6. How do they handle retention currently?
7. What's their lien waiver process?
8. How do invoices arrive? (email, mail, portal?)
9. Do they use KOJO POs for all purchases?
10. What reports does the CFO rely on most?
11. How many AP staff?
12. What's their average processing time per invoice?
13. Biggest AP pain points?
14. Any compliance/audit requirements?

---

## Development Timeline (7 Phases)

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| 1. Foundation | 1-3 | Working extraction pipeline |
| 2. Core AI | 4-6 | Accurate AI coding with Mark III invoices |
| 3. Dashboard | 7-10 | Usable web app |
| 4. Sage Integration | 11-14 | Data flows into accounting |
| 5. Procore Integration | 15-17 | PO matching works |
| 6. Construction Features | 18-22 | AIA, lien waivers, retention |
| 7. Polish & Pilot | 23-26 | Production-ready |

**Total: ~6 months** (best case 4-5, worst case 9-12)

---

## Legal Checklist (Before First Customer)

- [ ] Form LLC ($100-500)
- [ ] Terms of Service + Privacy Policy ($1-3K)
- [ ] Cyber liability insurance ($1-3K/yr)
- [ ] DPA template ($1-2K)
- [ ] SOC 2 compliance ($15-50K — can defer)
- [ ] Trademark "PayFlow AI"
- [ ] AI liability disclaimers (human-in-the-loop required)

---

## Future SaaS Opportunities

1. AI Contract Review for Construction (same customers — next priority)
2. AI Permit Expediting (first-mover opportunity)
3. AI Insurance Claims Processing
4. AI Lien & Notice Management (PayFlow add-on)
5. AI Compliance Document Manager (PayFlow add-on)
6. AI Property Management AP (same engine, different prompts)

---

## Pending Action Items

1. Get answers to 14 discovery questions from Mark III AP team
2. Verify KOJO has an API
3. Register payflowai.com domain
4. **Regenerate Claude API key** (old one was exposed in chat)
5. Scaffold project (folder structure, dependencies, Docker, first endpoint)
6. Begin Phase 1: invoice upload + Claude API extraction pipeline

---

## Research Files Index
All in `research/` directory:
- `AP_AI_Software_Research_2026.pdf` — Market research (11 vendors analyzed)
- `Claude_API_AP_Integration_Guide_2026.pdf` — Integration guide with code examples
- `Competitive_Analysis_2026.pdf` — Stampli vs Vic.ai vs Adaptive deep dive
- `PayFlow_AI_System_Prompts.pdf` — 8 production-grade AI prompts
- `PayFlow_AI_Sales_Deck.pptx` (v1, v2, v3) — CFO sales presentations
- `PayFlow_AI_How_It_Works.pptx` — 18-slide technical walkthrough
- `AI_SaaS_Opportunities_CEO.pptx` — Portfolio view for investors
- `competitive_analysis.md` — Markdown version
- `legal_considerations.md` — Legal deep dive
- `mark_iii_pilot_customer.md` — Pilot details
- `development_timeline.md` — Phase breakdown
- `procore_marketplace_strategy.md` — Marketplace listing plan
- `chat_thread_2026-03-06.md` — Session 1 conversation log
- `chat_thread_2026-03-09.md` — Session 2 conversation log
- `prototype/index.html` — 8-page clickable UI prototype
