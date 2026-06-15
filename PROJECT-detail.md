# PROJECT-detail.md — Life Navigator Agent

## Problem Definition

### The Document Comprehension Crisis

Every year, hundreds of millions of official documents are sent to everyday people
who cannot fully understand them:

- **67% of US adults** read at or below a 6th-grade level (NCES)
- **40% of medical bills** contain errors that most patients never catch
- **$10+ billion** in benefits go unclaimed annually because people don't understand
  eligibility notices or don't know how to appeal denials
- **Seniors lose $28.3 billion** per year to fraud, often through fake government letters
- **1 in 3 evictions** could be prevented with timely access to rental assistance information
- **Immigrants** face deportation partly due to missed USCIS deadlines from confusing notices

The people most affected — seniors, caregivers, new immigrants, low-income households —
are also the least likely to have access to lawyers, financial advisors, or educated
family members who can interpret documents for them.

**Current options:**
- **Lawyers** — expensive, not available on-demand, intimidating to contact
- **Legal Aid** — under-resourced, long wait times, limited to very low income
- **Government websites** — still too complex, still full of jargon
- **Family/friends** — often don't know either
- **Generic AI (ChatGPT/Claude without skill)** — too generic, misses emotional context,
  doesn't know which resources exist, can't detect scams

**The gap:** An on-demand, warm, simple, action-oriented AI that treats every confusing
document as a navigation problem — and provides the exact path forward.

---

## Solution Design

### Three-Phase Navigation

Every response has exactly three outputs — no more, no less:

```
PHASE 1: DECODE    What does this say? (Plain English)
PHASE 2: ASSESS    Should I be worried? (Honest calibration)
PHASE 3: ACT       What do I do? (Numbered steps + resources)
```

This structure works because:
- Non-tech users are overwhelmed by information dumps
- They need to know "is this an emergency?" before anything else
- Numbered steps are the most accessible format for action
- Free resources change the equation for low-income users

### The Reading Level Commitment

Every output targets 6th-8th grade reading level. This is enforced by:
1. `plain_language.py` — measures original grade level, simplifies
2. Jargon dictionary — 200+ direct replacement terms
3. Writing rules embedded in CLAUDE.md — sentence length limits, pronoun rules
4. Eval assertions specifically testing for plain language

### The Trust Architecture

Non-tech users need to trust the navigator before they'll act on it.
Three trust-builders embedded in every response:

1. **Honest worry calibration** — "This IS serious" when true, "This is routine" when true
   Never minimizing, never over-alarming. Users stop trusting AI that either panics them
   or dismisses real threats.

2. **Free resources always** — Many users assume help costs money they don't have.
   Showing free options (211, Legal Aid, SHIP, TAS) builds trust that the navigator
   understands their situation.

3. **Scam detection** — When a document is flagged as a possible scam, the user
   learns the navigator is protecting them, not just processing their request.

---

## Document Coverage Architecture

### 60+ Document Types, 6 Categories

```
MED (12 types)  — Medical bills, insurance EOBs, Medicare notices, denials
HSG (10 types)  — Leases, eviction notices, utility shutoffs, foreclosure
FIN (12 types)  — Debt collection, IRS notices, wage garnishment, student loans
GOV (15 types)  — Social Security, SNAP, court summons, immigration, CPS
EDU  (6 types)  — FAFSA, IEP, child support, school enrollment
EMP  (7 types)  — Job offers, COBRA, 401k, workers' comp, termination
```

### Urgency System

Four levels based on consequence + time pressure:

```
RED    → Respond TODAY: eviction, shutoff, IRS levy, court summons, NTA
YELLOW → Respond in 1-2 weeks: insurance denial, SS overpayment, COBRA
GREEN  → Respond as directed (usually 30 days): routine bills, statements
INFO   → No response needed: EOBs, annual notices, quarterly statements
```

The urgency system is the most important design choice:
- Under-urgency = user ignores something serious
- Over-urgency = user panics about a routine notice

Getting this right is what separates Life Navigator from generic AI.

---

## Special Mode System

Four modes with specific behavioral adjustments:

### Senior Mode
- Simpler vocabulary baseline (grade 5-6 vs 6-8)
- Extra skepticism about collection letters and "government" contacts (high fraud risk)
- SHIP, SMP, Eldercare Locator resources always included
- Acknowledgment of Medicare/Social Security system complexity
- Offer to write a letter instead of calling (many seniors prefer writing)

### Immigrant Mode
- Ultra-short sentence structure (ESL consideration)
- Explain American systems that don't exist in other countries (credit scores, SSN, at-will employment)
- Strong recommendation of DOJ-accredited representatives for immigration docs
- Community organization references
- No slang or idioms

### Caregiver Mode
- Acknowledge the emotional weight of managing someone else's paperwork
- HIPAA/Power of Attorney considerations included
- Resources for the caregiver, not just the patient
- Recognition that they may be managing multiple situations simultaneously

### Crisis Mode
- One-sentence emotional acknowledgment mandatory
- Emergency resources FIRST (not after the explanation)
- Compressed information — only the critical path
- Specific dates/deadlines called out prominently
- Follow-up offered ("want me to help with the next step?")

---

## Scam Detection System

Many of the documents this skill handles are targets for fraud.
The scam detection system checks for:

**Hard red flags** (very likely scam):
- Gift card payment request
- Wire transfer / cryptocurrency demand
- Immediate arrest threat
- Spoofed government caller ID
- No specific account number or name

**Soft yellow flags** (verify first):
- Unexpected collection letter
- Unexpected IRS contact
- Phone-only SSA/Medicare contact
- Mismatched amounts or details

When scam is detected:
- Scam warning appears BEFORE any document analysis
- Document analysis continues (in case it's legitimate)
- Verification steps for each agency provided
- FTC reporting link included

---

## The Phone Script System

One of the biggest barriers for non-tech users is calling official numbers.
They don't know what to say, how to ask, what rights they have, or what information
to have ready.

The phone script system provides:
- Word-for-word opening lines
- Specific questions to ask
- Rights to assert
- What to write down
- Warnings about what to watch out for

Eight standard scripts cover 80%+ of calling situations:
1. Medical billing
2. Insurance denial appeal
3. Medicare questions
4. Social Security (SSA)
5. IRS
6. Debt collectors (with FDCPA rights)
7. Landlords / Property managers
8. 211 (the universal emergency resource line)

---

## What This Skill Does NOT Do

- **Give legal advice** — explains documents and rights, not legal strategy
- **Give medical advice** — explains what documents say about care decisions, not what care to choose
- **Replace an attorney** — always flags situations requiring legal representation
- **Make financial decisions** — explains options, doesn't recommend
- **Process documents in other languages** — English only in v1.0; translation tools can assist
- **Verify documents are real** — explains how to verify; doesn't verify itself

---

## Future Roadmap

### v1.1 — Document Expansion
- [ ] Student loan-specific deep coverage (IDR, PSLF, rehabilitation)
- [ ] Small claims court preparation guide
- [ ] Veterans benefits documents (VA rating, C&P exams)
- [ ] HOA deep coverage (CC&Rs, assessment disputes)

### v1.2 — Language Support
- [ ] Spanish language output mode
- [ ] Portuguese (Brazilian) output mode
- [ ] Cantonese / Mandarin output mode

### v1.3 — Integration
- [ ] OCR integration — process actual document photos directly
- [ ] 211.org API — real-time local resource lookup
- [ ] State-specific legal aid directory integration

### v2.0 — Proactive Navigation
- [ ] Deadline tracker — import deadlines, get reminders
- [ ] Benefits eligibility checker — based on situation, find programs they qualify for
- [ ] Document bundle mode — process multiple related documents together
