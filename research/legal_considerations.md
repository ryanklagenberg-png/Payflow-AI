# Legal Considerations for Commercial AP AI Product
## Date: March 6, 2026

---

## 1. Data Security & Privacy

### SOC 2 Compliance
- Customers (especially mid-market and up) will require SOC 2 Type II before signing
- Covers security, availability, processing integrity, confidentiality, privacy
- Cost: $15-50K for initial audit, $10-25K annually to maintain
- Timeline: 6-12 months to get certified
- You can start selling without it, but enterprise deals will stall

### Data Encryption
- Encrypt data at rest (AES-256) and in transit (TLS 1.2+)
- This isn't optional — it's a legal liability if you don't

### State Privacy Laws
- CCPA (California), and similar laws in TX, VA, CO, CT, etc.
- If you ever handle data from EU companies: GDPR applies
- You need a published Privacy Policy that explains what data you collect, store, and process

---

## 2. Financial Data Regulations

### Handling Sensitive Financial Records
- Invoices contain vendor bank details, tax IDs (EIN/SSN), payment amounts
- If any of this leaks, you're liable
- Consider cyber liability insurance ($1-5K/year for a startup)

### Record Retention
- IRS requires businesses to keep financial records 3-7 years
- Your platform needs to support this — you can't just delete customer data
- Your contract must clarify who owns the data and what happens if they cancel

### Sarbanes-Oxley (SOX)
- If your customers are publicly traded companies, their AP processes fall under SOX
- Your system needs complete audit trails (who changed what, when)
- The AI audit trail on the invoice detail page addresses this

---

## 3. AI-Specific Legal Issues

### AI Accuracy & Liability
- If your AI miscodes an invoice and it causes a tax filing error, who's liable?
- Your Terms of Service MUST include disclaimers that the AI is assistive, not a replacement for human judgment
- Always keep a human-in-the-loop option — never position it as fully autonomous with zero oversight
- The "confidence score" in your product is legally important — it shows you're flagging uncertainty

### Sending Data to Anthropic
- Customer invoice data gets sent to Claude API for processing
- Anthropic's API terms state they don't train on API data — but your customers need to know this
- Your DPA (Data Processing Agreement) must disclose the use of third-party AI providers
- Some customers (government, defense) may prohibit sending data to third-party APIs

### AI Bias & Errors
- If the AI consistently miscategorizes invoices from certain vendors or in certain languages, that could create issues
- Document your accuracy rates and testing methodology

---

## 4. Contracts You Need

### Terms of Service (ToS)
- Limitation of liability (cap damages at the amount they've paid you)
- Indemnification clauses (mutual)
- Uptime SLA (99.9% is standard for SaaS)
- Data ownership (customer owns their data, you own the platform)

### Data Processing Agreement (DPA)
- Required by GDPR, increasingly expected in the US
- Defines how you process, store, and protect customer data
- Discloses sub-processors (Anthropic, AWS, etc.)

### Service Level Agreement (SLA)
- Uptime guarantees
- Response times for support
- What happens if you miss the SLA (service credits)

### Business Associate Agreement (BAA)
- Only if you ever handle healthcare-related invoices (HIPAA)
- Probably not relevant initially, but worth knowing

---

## 5. Business Formation

### LLC vs Corporation
- LLC is simpler and cheaper to start — protects personal assets from business liability
- If you plan to raise VC funding, you'll need a C-Corp (Delaware is standard)
- Minimum: form an LLC before your first customer

### Business Insurance
- General liability: $500-1,500/year
- Cyber liability / E&O (Errors & Omissions): $1-5K/year
- This protects you if a data breach or AI error causes a customer financial loss

---

## 6. Intellectual Property

### Your IP
- The system prompts, validation logic, and extraction schemas are your trade secrets
- Don't open-source your prompts — they're the core IP of the product
- Consider filing a provisional patent if your processing pipeline is novel ($2-5K)

### Using Claude API
- Anthropic's API terms allow commercial use — you're fine to build and sell a product on it
- You don't own Claude — you own the application you build around it
- If Anthropic changes pricing or terms, you need a fallback plan (abstract the AI layer)

### Customer Data
- You do NOT own customer data — make this explicit in your contracts
- You can use aggregated, anonymized metrics (e.g., "average processing time") for marketing

---

## 7. Priority Action List

| Priority | Action | Cost | When |
|----------|--------|------|------|
| 1 | Form an LLC | $100-500 | Before first customer |
| 2 | Terms of Service + Privacy Policy | $1-3K (lawyer) or template service | Before first customer |
| 3 | Cyber liability insurance | $1-3K/year | Before first customer |
| 4 | Data Processing Agreement template | $1-2K (lawyer) | Before first customer |
| 5 | SOC 2 preparation | $15-50K | When enterprise customers ask |
| 6 | IP protection (provisional patent) | $2-5K | When product is proven |

---

## 8. Critical Risk: Data Breach

A data breach is the single biggest threat. If customer financial data leaks:
- You're liable for damages
- You'll lose every customer overnight
- Potential regulatory fines

From day one: encrypt everything, use role-based access, log all access to data, never store credentials in code, and get cyber insurance.
