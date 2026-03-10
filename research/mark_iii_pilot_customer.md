# Pilot Customer: Mark III Construction
## Date: March 6, 2026

---

## Company Profile

| Detail | Info |
|--------|------|
| Company | Mark III Construction |
| Trades | Mechanical, Electrical, Plumbing, Underground, Service |
| Accounting System | Sage (specific version TBD) |
| Project Management | Procore |
| Relationship | Direct (wife's company) |

---

## Why Mark III Is the Ideal Pilot

- **Multi-trade**: Invoices come from every type of vendor (material suppliers, subcontractors, equipment rentals, service calls)
- **Sage**: Adaptive only integrates with QuickBooks. If we build Sage integration first, we immediately have something Adaptive can't offer
- **Procore**: Procore has an open API. Integrating with Procore for job data, cost codes, and change orders would be a massive differentiator
- **Real data**: We can get actual invoices, their chart of accounts, their cost code structure, and their AP workflow
- **Insider access**: Direct relationship means fast feedback loops and real-world testing

---

## Questions for Mark III AP Team

### Current Process
1. How many invoices do they process per month?
2. How many AP staff handle it?
3. What does their workflow look like today? (Invoice arrives > who touches it > how does it get into Sage?)
4. What's the biggest time waste in their current AP process?
5. Which Sage product exactly? (Sage 300 CRE, Sage Intacct, Sage 100 Contractor?)

### Pain Points
6. Do they deal with AIA billing from subcontractors?
7. How do they track lien waivers today? (Spreadsheet? Paper files? Procore?)
8. How do they handle retention tracking?
9. What's their cost code structure look like? (How many levels deep?)
10. Do they do prevailing wage / government work?

### Technology
11. Which Procore modules do they use? (PM, Financials, both?)
12. Does Procore already sync with Sage, or are they separate?
13. Do invoices come in via email, paper mail, or vendor portals?
14. Who approves invoices? (By amount? By job? By trade?)

---

## Build Decisions Based on Mark III

| Decision | Answer |
|----------|--------|
| First ERP integration | Sage (whichever version they use) |
| First PM integration | Procore |
| Cost code structure | Match Mark III's exact structure |
| Invoice types to support first | Whatever their vendors actually send |
| Approval workflow | Mirror their current approval chain |
| Test dataset | Real Mark III invoices (with sensitive data redacted) |

---

## The Pitch

"What if every invoice that hits your inbox was automatically read by AI, coded to the right job and cost code, matched against the PO in Procore, checked for retention and lien waivers, and routed to the right person for approval — in under 5 seconds? And the ones the AI is confident about just flow straight through."

### ROI Estimate (Needs Validation)
- If they process 2,000 invoices/month at $16 each manually = $32,000/month in labor
- AI processing cost: ~$20/month (API) + software subscription
- Even at 50% automation on day one, that's $16,000/month saved

---

## Next Steps

1. Get answers to the 14 questions above from the AP team
2. Collect 50-100 sample invoices (redact sensitive data if needed)
3. Get a copy of their chart of accounts and cost code structure from Sage
4. Understand their Procore setup and what data is available via API
5. Start building the MVP tailored to their exact workflow
