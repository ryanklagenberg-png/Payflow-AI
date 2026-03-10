# Competitive Analysis - AP AI Market
## Date: March 6, 2026

---

## 1. Stampli (Billy the Bot)

**What they do:** Full procure-to-pay platform with an AI agent called "Billy" trained on 83 million hours of real AP workflow data and $90B+ in annual spend.

**What they do that we don't (yet):**
- **Built-in collaboration layer** — AP teams, approvers, and vendors chat directly on each invoice inside the platform. Eliminates email back-and-forth. We don't have vendor-facing communication.
- **Procurement + AP + Payments + Cards in one** — They've expanded beyond AP into purchasing, credit cards, and vendor management. We're AP-only.
- **83M hours of training data** — Billy's accuracy comes from massive proprietary data. We're starting from zero historical data and relying on Claude's general intelligence + our prompts.
- **200+ ERP integrations already built** — We'd have to build each integration from scratch.

**Their weakness:** Not construction-specific. No AIA billing, lien waivers, or job costing. Generic AP for all industries.

**Website:** https://www.stampli.com

---

## 2. Vic.ai

**What they do:** Pure AI-first AP platform. No templates, no rules — deep learning models trained on 535M+ invoices.

**What they do that we don't (yet):**
- **Proprietary ML models** — They trained their own deep learning models specifically for invoice processing. We're using Claude (general-purpose LLM). Their models are purpose-built; ours is adapted.
- **Autopilot mode** — True zero-touch processing. Invoices flow from receipt to payment with no human in the loop. 84% no-touch rate proven at customer sites.
- **VicInbox** — Dedicated AI that monitors vendor email inboxes, automatically identifies invoices vs. spam vs. other correspondence, and routes them. We have basic email ingestion planned.
- **VicAnalytics** — Real-time bottleneck identification in the AP process. Shows where invoices get stuck and why. We have basic reporting but not process intelligence.
- **355% capacity improvement per FTE** — They have proven ROI metrics from real deployments. We have projections.

**Their weakness:** No construction focus. No job costing, no AIA forms, no lien waivers. Also expensive — enterprise pricing only, no SMB tier.

**Website:** https://www.vic.ai

---

## 3. Adaptive

**What they do:** AI-native construction accounting. Backed by Andreessen Horowitz. The closest competitor to what we'd build.

**What they do that we don't (yet):**
- **Construction-first from day one** — Every feature designed for construction: job costing, cost codes, AIA billing, subcontractor payments. We'd be building these features; they already have them.
- **Accounting firm channel** — They sell through CPA firms (Pinion, CLA) who manage construction clients. This is a distribution strategy we haven't considered.
- **Real-time field reconciliation** — Connects financial data with field updates so costs match actual work progress. We don't have field integration.
- **10x accuracy claim** — They claim 10x better accuracy than general AP tools because they only focus on construction data patterns.
- **Already integrated with QuickBooks** — The most common accounting system for their market.

**Their weakness:** Limited AI sophistication compared to Stampli/Vic.ai. Only integrates with QuickBooks (not Sage, Viewpoint, or other construction ERPs). Small company, limited track record. Pricing starts at $575/mo which prices out smaller contractors.

**Website:** https://www.adaptive.build

---

## Comparison Matrix

| Capability | Stampli | Vic.ai | Adaptive | Us (PayFlow AI) |
|-----------|---------|--------|----------|-----------------|
| AI sophistication | High | Highest | Medium | High (Claude API) |
| Construction features | None | None | Strong | To be built |
| AIA billing / lien waivers | No | No | Yes | To be built |
| Proprietary ML models | Yes | Yes | Partial | No (use Claude) |
| ERP integrations | 200+ | 40+ | QuickBooks | To be built |
| Proven at scale | Yes | Yes | Growing | No |
| Pricing flexibility | Enterprise | Enterprise | $575/mo | We decide |

---

## Our Advantages

- Latest AI technology (Claude) vs. their models built 2-3 years ago
- Can undercut on price since our AI costs are pennies per invoice
- Construction-specific + best-in-class AI (nobody does both well today)
- Faster iteration — we're small, they have legacy code and processes

## Our Disadvantages

- Zero production data and proven accuracy metrics
- No integrations built
- No brand recognition or trust
- They have years of edge cases solved; we'd discover them the hard way

## The Opportunity

Adaptive is the closest competitor but they're early too (backed by a16z, still growing). The window to build a construction-focused AI AP product with superior AI is open right now — but it won't stay open long. Stampli or Vic.ai could add construction features, or Adaptive could upgrade their AI.

---

## Sources

- Stampli AP Automation Platform — https://www.stampli.com/ap-automation-platform/
- Stampli Edge Launch — https://www.cpapracticeadvisor.com/2025/08/07/stampli-launches-stampli-edge-ai-driven-ap-automation-built-for-smbs/166881/
- Vic.ai How It Works — https://www.vic.ai/how-it-works
- Vic.ai AP Automation — https://www.vic.ai/accounts-payable
- Adaptive Construction Accounting — https://www.adaptive.build/
- Adaptive AP Features — https://www.adaptive.build/features/accounts-payable
- Adaptive for Accounting Firms — https://www.adaptive.build/blog/adaptive-launches-industry-specific-ai-to-help-accounting-firms-scale-construction-services-without-adding-headcount
