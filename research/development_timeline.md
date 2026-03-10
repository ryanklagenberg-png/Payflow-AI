# Development Timeline: PayFlow AI
## Date: March 7, 2026

---

## Overview

Building for Mark III Construction as pilot customer, with Sage + Procore integration. Solo developer with Claude Code as development partner.

**Total Estimated Timeline: ~6 months**

---

## Phase 1: Foundation (Weeks 1-3)
- Project scaffolding (backend API, database, auth)
- Invoice upload and file storage
- Claude API integration for invoice extraction
- Basic extraction pipeline (upload > AI reads > structured JSON out)
- **Deliverable:** You can upload an invoice and see extracted data

## Phase 2: Core AI Engine (Weeks 4-6)
- Refine extraction prompts using real Mark III invoices
- GL coding + job costing prediction (5-dimensional: GL, job, phase, cost code, cost type)
- Confidence scoring and flag system
- Validation pipeline (math checks, duplicate detection)
- **Deliverable:** AI accurately extracts and codes Mark III invoices

## Phase 3: Dashboard & Workflow (Weeks 7-10)
- Build the web UI (based on prototype)
- Invoice list, detail view, editing extracted fields
- Approval routing (by amount, job, trade)
- User roles (AP clerk, PM, controller)
- **Deliverable:** Mark III AP team can log in and use it

## Phase 4: Sage Integration (Weeks 11-14)
- Connect to Sage API (hardest integration)
- Sync chart of accounts, vendors, jobs, cost codes
- Push approved invoices into Sage
- Two-way sync for payment status
- **Deliverable:** Approved invoices flow into Sage automatically

## Phase 5: Procore Integration (Weeks 15-17)
- Pull job data, POs, change orders, cost codes from Procore
- Three-way matching (invoice vs PO vs budget)
- Contract value tracking
- **Deliverable:** AI matches invoices against Procore POs

## Phase 6: Construction Features (Weeks 18-22)
- AIA G702/G703 progress billing extraction
- Lien waiver processing and tracking
- Retention tracking per vendor per job
- Compliance dashboard (COIs, W-9s)
- **Deliverable:** Full construction-specific AP system

## Phase 7: Polish & Pilot (Weeks 23-26)
- Bug fixes from Mark III feedback
- Accuracy tuning (prompt refinement based on real corrections)
- Reporting and analytics
- Email ingestion (forward invoices to a dedicated inbox)
- Security hardening, audit trails
- **Deliverable:** Production-ready for Mark III

---

## Summary Table

| Phase | Weeks | What You Have |
|-------|-------|---------------|
| Foundation | 1-3 | Working extraction pipeline |
| Core AI | 4-6 | Accurate AI coding Mark III invoices |
| Dashboard | 7-10 | Usable web app |
| Sage | 11-14 | Data flows into accounting system |
| Procore | 15-17 | PO matching works |
| Construction | 18-22 | AIA, lien waivers, retention |
| Polish | 23-26 | Ready for daily use at Mark III |

---

## Realistic Ranges

- **Best case** (full-time, things go smoothly): 4-5 months
- **Expected** (consistent effort, normal setbacks): 6-7 months
- **Worst case** (part-time, Sage integration is painful): 9-12 months

---

## What Speeds This Up

- Working on it full-time vs. nights/weekends
- Getting sample invoices and Sage/Procore access early
- Mark III AP team giving fast feedback

## What Slows This Down

- Sage integration — API documentation can be painful, especially Sage 300 CRE
- Scope creep — every conversation with AP team reveals new requirements
- Edge cases — first 80% of invoices work fast, last 20% take 80% of the time

---

## Early Value

Mark III can start getting value at Phase 3 (week 10) — uploading invoices, reviewing AI extractions, and approving through the dashboard. Sage push would still be manual until Phase 4, but AI extraction and coding saves time immediately.
