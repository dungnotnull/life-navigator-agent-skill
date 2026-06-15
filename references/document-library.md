# Document Library — Classification & Key Signals

## Document Type Codes

### MED — Medical & Health Documents

| Code | Document | Key Signals | Urgency Default |
|---|---|---|---|
| MED-01 | Medical / Hospital Bill | "Amount Due", "Patient Responsibility", "Balance After Insurance" | 🟢 Normal |
| MED-02 | Insurance EOB (Explanation of Benefits) | "Explanation of Benefits", "This is not a bill", "Allowed Amount", "Deductible" | ℹ️ Info |
| MED-03 | Medicare Notice (MSN) | "Medicare Summary Notice", "Medicare", "Part A/B/D" | ℹ️ Info |
| MED-04 | Medicaid Notice | "Medicaid", "CHIP", "eligibility", "redetermination" | 🟡 Time-sensitive |
| MED-05 | Insurance Denial / Prior Auth Denial | "not covered", "denied", "not medically necessary", "appeal rights" | 🟡 Time-sensitive |
| MED-06 | Discharge Instructions | "discharge", "follow-up", "restrictions", "medications" | 🟢 Normal |
| MED-07 | Prescription Label | drug name, dosage, "Take [X] times", refills | ℹ️ Info |
| MED-08 | Medical Records / Test Results | lab values, "normal range", diagnosis codes (ICD-10) | 🟢 Normal |
| MED-09 | Medicare Advantage / Part D Notice | "plan", "formulary", "premium change", "Annual Notice of Change" | 🟡 Time-sensitive |
| MED-10 | Appeals / Grievance Letter | "appeal", "grievance", "IRO", "External Review" | 🟡 Time-sensitive |
| MED-11 | Surprise Medical Bill / Balance Bill | unexpected high amount, out-of-network provider | 🟡 Time-sensitive |
| MED-12 | Medical Debt Collection | collection agency, "final notice", "credit reporting" | 🟡 Time-sensitive |

### HSG — Housing Documents

| Code | Document | Key Signals | Urgency Default |
|---|---|---|---|
| HSG-01 | Lease Agreement | "Tenant", "Landlord", "Rent", "Security Deposit", "Term" | 🟢 Normal |
| HSG-02 | Rent Increase Notice | "rent increase", "new rent", "effective date" | 🟢 Normal |
| HSG-03 | Pay or Quit Notice | "Pay or Quit", "3-day notice", "vacate", "unlawful detainer" | 🔴 URGENT |
| HSG-04 | Eviction / Unlawful Detainer | court filing, "summons", "eviction" | 🔴 URGENT |
| HSG-05 | Utility Shutoff Warning | "disconnect", "shutoff", "past due", utility company | 🔴 URGENT |
| HSG-06 | HOA Notice / Fine | "HOA", "Association", "violation", "fine", "assessment" | 🟢 Normal |
| HSG-07 | Mortgage Statement | "principal", "escrow", "interest", "payment due" | 🟢 Normal |
| HSG-08 | Foreclosure Notice | "Notice of Default", "foreclosure", "trustee sale" | 🔴 URGENT |
| HSG-09 | Security Deposit Dispute | itemized deduction, "normal wear and tear" | 🟢 Normal |
| HSG-10 | Section 8 / HCV Notice | "Housing Choice Voucher", "HUD", "inspection", "HAP" | 🟡 Time-sensitive |

### FIN — Financial & Debt Documents

| Code | Document | Key Signals | Urgency Default |
|---|---|---|---|
| FIN-01 | Debt Collection Letter | "collection", "Collector", "FDCPA", "validation of debt" | 🟡 Time-sensitive |
| FIN-02 | IRS CP2000 (Proposed Change) | "CP2000", "Underreported Income", "proposed changes" | 🟡 Time-sensitive |
| FIN-03 | IRS Balance Due Notice | "CP14", "CP501", "CP503", "CP504", "Amount Due" | 🟡 Time-sensitive |
| FIN-04 | IRS Final Notice (Intent to Levy) | "CP90", "LT11", "final notice", "levy", "seize" | 🔴 URGENT |
| FIN-05 | Wage Garnishment Notice | "garnish", "withhold from wages", "judgment" | 🔴 URGENT |
| FIN-06 | Bank Account Closure / Freeze | "account closed", "restricted", "suspicious activity" | 🔴 URGENT |
| FIN-07 | Student Loan Default Warning | "default", "rehabilitation", "collections", Department of Education | 🟡 Time-sensitive |
| FIN-08 | Credit Card / Loan Statement | APR, minimum payment, balance, due date | 🟢 Normal |
| FIN-09 | Credit Report Dispute | credit bureau, "dispute", FCRA | 🟡 Time-sensitive |
| FIN-10 | Bankruptcy Notice | "Chapter 7", "Chapter 13", "discharge", "trustee" | 🟡 Time-sensitive |
| FIN-11 | Car Repossession Warning | "repossess", "right to cure", "voluntary surrender" | 🔴 URGENT |
| FIN-12 | Payday / Predatory Loan Notice | extremely high APR, short repayment, balloon payment | 🟡 Time-sensitive |

### GOV — Government & Legal Documents

| Code | Document | Key Signals | Urgency Default |
|---|---|---|---|
| GOV-01 | Social Security Award / Change | "SSA", "benefit amount", "COLA", "overpayment" | 🟢 Normal |
| GOV-02 | Social Security Overpayment | "overpayment", "waiver", "repayment plan" | 🟡 Time-sensitive |
| GOV-03 | SSDI / SSI Review Notice | "Continuing Disability Review", "CDR", "medical review" | 🟡 Time-sensitive |
| GOV-04 | Unemployment Benefits Notice | "UI", "claim", "determination", "disqualification" | 🟡 Time-sensitive |
| GOV-05 | SNAP / Food Stamp Notice | "SNAP", "EBT", "eligibility", "renewal", "reduction" | 🟡 Time-sensitive |
| GOV-06 | Medicaid Renewal / Termination | "Medicaid", "renewal", "eligibility review" | 🟡 Time-sensitive |
| GOV-07 | Court Summons (Civil) | "SUMMONS", "plaintiff", "defendant", "appear", "respond" | 🔴 URGENT |
| GOV-08 | Court Summons (Criminal) | "criminal", "arraignment", "plea", "charges" | 🔴 URGENT |
| GOV-09 | Traffic Violation / Fine | "violation", "citation", "fine", "DMV", "license" | 🟢 Normal |
| GOV-10 | Jury Duty Notice | "juror", "report", "service" | 🟢 Normal |
| GOV-11 | Property Tax Notice | "assessment", "property tax", "millage", "appeal deadline" | 🟢 Normal |
| GOV-12 | Immigration Notice (USCIS) | "USCIS", "I-", "Notice to Appear", "RFE", "NOA" | 🟡 Time-sensitive |
| GOV-13 | Immigration – NTA / Removal | "Notice to Appear", "removal", "deportation" | 🔴 URGENT |
| GOV-14 | Child Protective Services Notice | "CPS", "DCFS", "investigation", "child welfare" | 🔴 URGENT |
| GOV-15 | Workers' Compensation Notice | "workers' comp", "claim", "disability rating", "IME" | 🟡 Time-sensitive |

### EDU — Education & Family Documents

| Code | Document | Key Signals | Urgency Default |
|---|---|---|---|
| EDU-01 | FAFSA / Financial Aid Award | "Expected Family Contribution", "EFC", "SAI", "grant", "loan" | 🟡 Time-sensitive |
| EDU-02 | Student Loan Statement | servicer, "repayment plan", "IDR", "forbearance" | 🟢 Normal |
| EDU-03 | IEP / Special Education | "Individualized Education Program", "IEP", "504" | 🟢 Normal |
| EDU-04 | School Enrollment / Transfer | "enrollment", "registration", "immunization", "district" | 🟢 Normal |
| EDU-05 | Child Support Order | "support order", "garnishment", "arrears", "modification" | 🟡 Time-sensitive |
| EDU-06 | Divorce / Separation Basics | "dissolution", "petition", "respondent", "marital assets" | 🟡 Time-sensitive |

### EMP — Employment & Benefits

| Code | Document | Key Signals | Urgency Default |
|---|---|---|---|
| EMP-01 | Job Offer Letter | "offer", "salary", "start date", "at-will", "contingent" | 🟢 Normal |
| EMP-02 | Non-Compete / NDA Agreement | "non-compete", "non-solicitation", "confidential" | 🟢 Normal |
| EMP-03 | Employee Benefits Enrollment | "open enrollment", "premium", "deductible", "HSA", "FSA" | 🟡 Time-sensitive |
| EMP-04 | 401k / Retirement Statement | "vested", "contribution", "match", "fund allocation" | ℹ️ Info |
| EMP-05 | COBRA Notice | "COBRA", "continuation coverage", "election period" | 🟡 Time-sensitive |
| EMP-06 | Termination / Layoff Letter | "termination", "laid off", "severance", "WARN Act" | 🟡 Time-sensitive |
| EMP-07 | Workers' Comp Claim Denial | "denied", "not work-related", "independent medical exam" | 🟡 Time-sensitive |

---

## Document Classification Scoring

When classifying, check for these signal categories in order:

1. **Letterhead / Sender** — Who sent it? (IRS, SSA, hospital, court, collection agency)
2. **Action required** — Does it say to pay, respond, appear, or appeal?
3. **Deadline phrases** — "by [date]", "within [N] days", "final notice"
4. **Legal terms** — "judgment", "garnish", "levy", "summons", "eviction"
5. **Money amounts** — positive (benefit), negative (owed), neutral (statement)
6. **Code numbers** — IRS notice codes (CP14, CP2000), USCIS form numbers (I-485)

---

## Scam Detection Fast-Check

Before processing, check for scam signals (see `references/scam-patterns.md`):
- Requests for gift card or wire transfer payment
- Threatens arrest for not paying immediately
- Grammar / spelling errors throughout
- Unfamiliar "IRS", "SSA", or "Medicare" sender email/address
- Asks for SSN, credit card, or bank info by phone/email
- No return address or P.O. Box only
- Very generic (no account number, no specific amount)
