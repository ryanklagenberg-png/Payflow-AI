# Procore App Marketplace Strategy
## Date: March 7, 2026

---

## Why Integrate With Procore (Not Compete)

- Procore took 20 years and $1B+ to build. 16,000+ customers, 2,000+ employees.
- Mark III already uses Procore — asking them to switch PM tools is a dealbreaker.
- Procore has an open API and active App Marketplace with 500+ partner apps.
- Being listed is a free distribution channel to 16,000 construction companies.

---

## How to Get Listed on Procore's App Marketplace

### Step 1: Join the Procore Developer Program
- Sign up at developers.procore.com/partner (free)
- Get access to API documentation, sandbox environment, developer support

### Step 2: Build the Integration
- Use Procore's REST API
- Must use OAuth 2.0 for authentication
- Must be installable in a customer's Procore account

**What we'd pull from Procore:**
- Projects, jobs, cost codes
- Purchase orders, commitments, change orders
- Budgets and contract values
- Vendor/subcontractor list

### Step 3: Meet Technical Requirements

| Requirement | What It Means |
|------------|---------------|
| Use only public APIs | No private or undocumented endpoints |
| OAuth 2.0 authentication | Secure customer authorization flow |
| No AI training on Procore data | Cannot use Procore data to train AI/ML models including LLMs |
| No ads or push notifications | Clean user experience |
| No malicious behavior | Standard security compliance |
| Proper error handling | Handle API rate limits, downtime gracefully |
| Data security | Follow Procore's data handling policies |

### Step 4: Beta Test with a Real Customer
- Need a beta customer using the integration in a real Procore account
- Mark III is perfect for this
- Gather feedback, fix issues, document the setup process
- Procore wants onboarding to be simple and intuitive

### Step 5: Prepare Marketplace Listing

| Content | Details |
|---------|---------|
| App name and logo | PayFlow AI branding |
| Description | What the app does, who it's for |
| Screenshots | UI showing the Procore integration |
| Categories | Accounts Payable, Financial Management |
| Support contact | Email, help docs, onboarding guide |
| Pricing info | How customers pay |
| Installation guide | Step-by-step setup documentation |
| Privacy policy | How we handle Procore data |

### Step 6: Submit for Review
- Submit app and listing through developer portal
- Procore reviews for technical compliance, content quality, policy adherence
- May request changes or additional information
- Procore can decline any listing at their discretion

### Step 7: Get Listed
- Appear in Procore App Marketplace
- 16,000+ customers can discover and install the app

---

## Critical AI Rule

**"You must not use Procore data to train AI/ML models (including LLMs)"**

What this means for us:
- CAN pull project data from Procore to match invoices against POs
- CAN display Procore job/cost code info in our UI
- CANNOT send Procore project data to Claude as training data
- CANNOT use their data to fine-tune models

This is fine — we use Claude API for invoice extraction, not training. We pull Procore data for matching and coding. The AI processes the invoice document itself, not Procore's data.

---

## Timeline for Marketplace Listing

| Step | When |
|------|------|
| Join developer program | Week 1 of development |
| Build Procore integration | Weeks 15-17 (Phase 5) |
| Beta test with Mark III | Weeks 18-22 |
| Prepare listing content | Week 23 |
| Submit for review | Week 24 |
| Approval (estimated) | 2-6 weeks after submission |
| **Listed on marketplace** | **~Month 7-8** |

---

## What Being Listed Gets Us

- **Free discovery** — construction companies browsing for AP tools find us
- **Credibility** — "Procore Partner" badge builds trust
- **Warm leads** — customers already use Procore, understand integrations
- **Co-marketing** — Procore sometimes features partner apps in newsletters and events
- **Sales team referrals** — Procore reps can point customers to us when asked about AP

---

## What We Pull From Procore (Integration Scope)

| Procore Data | How We Use It |
|-------------|---------------|
| Jobs/projects | Auto-code invoices to the right job |
| Cost codes | AI predicts cost code using Procore's structure |
| Purchase orders | Three-way match invoices against POs |
| Change orders | Verify billing doesn't exceed contract + changes |
| Budgets | Flag invoices that push a cost code over budget |
| Vendors/subs | Pre-populated vendor list, compliance docs |
| Commitments | Track contracted amounts vs. billed-to-date |
| Daily logs | Verify labor invoices match field activity |

---

## Sources

- Procore Partner Program — https://developers.procore.com/partner
- Become a Technology Partner — https://developers.procore.com/documentation/listing-your-app
- App Marketplace Overview — https://developers.procore.com/documentation/partner-overview
- Marketplace Requirements — https://developers.procore.com/documentation/partner-content-reqs
- Technical Requirements — https://procore.github.io/documentation/partner-tech-reqs
- Build & Prepare Your App — https://procore.github.io/documentation/marketplace-requirements
- Marketplace Listing Guidelines — https://developers.procore.com/documentation/marketplace-listing-guidelines
