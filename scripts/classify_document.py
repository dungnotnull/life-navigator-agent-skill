#!/usr/bin/env python3
"""
classify_document.py — Classify a document into type, urgency, and mode.

Usage:
    python scripts/classify_document.py --text "I got a pay or quit notice..."
    python scripts/classify_document.py --file document.txt
    python scripts/classify_document.py --text "..." --json

Output: document type code, urgency level, special modes, key signals found
"""
import argparse, re, sys, json
from pathlib import Path


# ─── Urgency Levels ───────────────────────────────────────────────────────────

URGENCY = {
    "RED":    "🔴 URGENT — Respond within 24–48 hours",
    "YELLOW": "🟡 TIME-SENSITIVE — Respond within 1–2 weeks",
    "GREEN":  "🟢 NORMAL — Respond as directed (usually within 30 days)",
    "INFO":   "ℹ️  INFORMATIONAL — No action required",
}

URGENCY_SHORT = {
    "RED": "URGENT", "YELLOW": "TIME-SENSITIVE",
    "GREEN": "NORMAL", "INFO": "INFORMATIONAL"
}

# ─── Document Classification Signals ─────────────────────────────────────────

DOC_SIGNALS = {
    # ── Medical ──────────────────────────────────────────────────────────────
    "MED-01": {
        "signals": ["patient responsibility", "amount due", "balance after insurance",
                    "hospital bill", "medical bill", "please pay", "statement date",
                    "your share", "patient balance", "amount you owe"],
        "urgency": "GREEN", "name": "Medical / Hospital Bill"
    },
    "MED-02": {
        "signals": ["explanation of benefits", "this is not a bill", "eob",
                    "allowed amount", "your deductible", "plan paid", "member responsibility"],
        "urgency": "INFO", "name": "Insurance Explanation of Benefits (EOB)"
    },
    "MED-03": {
        "signals": ["medicare summary notice", "msn", "medicare paid", "part a", "part b",
                    "medicare advantage", "supplemental"],
        "urgency": "INFO", "name": "Medicare Notice"
    },
    "MED-04": {
        "signals": ["medicaid", "chip", "medi-cal", "redetermination", "renewal notice",
                    "eligibility determination", "benefits will end"],
        "urgency": "YELLOW", "name": "Medicaid / State Health Benefits Notice"
    },
    "MED-05": {
        "signals": ["not covered", "claim denied", "denial of benefits", "not medically necessary",
                    "prior authorization denied", "appeal rights", "your right to appeal",
                    "adverse benefit determination"],
        "urgency": "YELLOW", "name": "Insurance Denial / Prior Authorization Denial"
    },
    "MED-09": {
        "signals": ["annual notice of change", "anoc", "part d", "formulary change",
                    "premium change", "plan benefit change", "medicare advantage plan"],
        "urgency": "YELLOW", "name": "Medicare Advantage / Part D Annual Notice"
    },
    "MED-11": {
        "signals": ["balance bill", "surprise bill", "out-of-network provider",
                    "no surprise act", "unexpected bill"],
        "urgency": "YELLOW", "name": "Surprise / Balance Bill"
    },
    "MED-12": {
        "signals": ["final notice", "collection agency", "sent to collections",
                    "credit reporting", "credit bureau", "past due account"],
        "urgency": "YELLOW", "name": "Medical Debt Collection Notice"
    },

    # ── Housing ───────────────────────────────────────────────────────────────
    "HSG-01": {
        "signals": ["lease agreement", "rental agreement", "tenant", "landlord",
                    "security deposit", "monthly rent", "term of lease"],
        "urgency": "GREEN", "name": "Lease / Rental Agreement"
    },
    "HSG-02": {
        "signals": ["rent increase", "new rental rate", "increase in rent",
                    "effective date", "new monthly rent"],
        "urgency": "GREEN", "name": "Rent Increase Notice"
    },
    "HSG-03": {
        "signals": ["pay or quit", "3-day notice", "3 day notice", "pay rent or vacate",
                    "notice to pay", "cure or quit", "pay or vacate"],
        "urgency": "RED", "name": "Pay or Quit Notice (Eviction Warning)"
    },
    "HSG-04": {
        "signals": ["unlawful detainer", "eviction summons", "eviction complaint",
                    "writ of possession", "notice to appear in court", "forcible detainer"],
        "urgency": "RED", "name": "Eviction / Unlawful Detainer"
    },
    "HSG-05": {
        "signals": ["disconnect notice", "shutoff notice", "termination of service",
                    "past due balance", "service will be disconnected",
                    "restoration fee", "final notice before disconnection"],
        "urgency": "RED", "name": "Utility Shutoff Warning"
    },
    "HSG-07": {
        "signals": ["mortgage statement", "principal balance", "escrow",
                    "loan servicer", "payment due", "interest charged"],
        "urgency": "GREEN", "name": "Mortgage Statement"
    },
    "HSG-08": {
        "signals": ["notice of default", "foreclosure", "trustee sale",
                    "right to reinstate", "notice of trustee sale", "lis pendens"],
        "urgency": "RED", "name": "Foreclosure Notice"
    },
    "HSG-10": {
        "signals": ["housing choice voucher", "section 8", "hcv", "hud",
                    "housing authority", "annual inspection", "hap payment"],
        "urgency": "YELLOW", "name": "Section 8 / HCV Notice"
    },

    # ── Financial ─────────────────────────────────────────────────────────────
    "FIN-01": {
        "signals": ["collection", "debt collector", "fdcpa", "fair debt collection",
                    "original creditor", "amount owed", "validation of debt",
                    "this communication is from a debt collector"],
        "urgency": "YELLOW", "name": "Debt Collection Letter"
    },
    "FIN-02": {
        "signals": ["cp2000", "underreported income", "proposed changes to your",
                    "information we received", "we believe you may owe"],
        "urgency": "YELLOW", "name": "IRS CP2000 — Proposed Tax Change"
    },
    "FIN-03": {
        "signals": ["cp14", "cp501", "cp503", "balance due", "amount you owe",
                    "unpaid tax", "internal revenue service", "department of treasury"],
        "urgency": "YELLOW", "name": "IRS Balance Due Notice"
    },
    "FIN-04": {
        "signals": ["cp90", "lt11", "final notice", "intent to levy",
                    "seize your property", "lien on your property", "last warning"],
        "urgency": "RED", "name": "IRS Final Notice — Intent to Levy"
    },
    "FIN-05": {
        "signals": ["wage garnishment", "garnish your wages", "withhold from earnings",
                    "judgment against you", "creditor's garnishment", "order to withhold"],
        "urgency": "RED", "name": "Wage Garnishment Notice"
    },
    "FIN-07": {
        "signals": ["student loan", "default", "department of education",
                    "federal student aid", "loan rehabilitation",
                    "your loans are in default", "treasury offset"],
        "urgency": "YELLOW", "name": "Student Loan Default Warning"
    },
    "FIN-11": {
        "signals": ["repossession", "right to cure", "voluntary surrender",
                    "repossess your vehicle", "cure the default", "deficiency balance"],
        "urgency": "RED", "name": "Car Repossession Warning"
    },

    # ── Government / Legal ────────────────────────────────────────────────────
    "GOV-01": {
        "signals": ["social security", "ssa", "benefit amount", "cola",
                    "cost of living adjustment", "your monthly benefit"],
        "urgency": "GREEN", "name": "Social Security Notice"
    },
    "GOV-02": {
        "signals": ["overpayment", "you were overpaid", "repayment", "waiver request",
                    "overpayment recovery", "we paid you too much"],
        "urgency": "YELLOW", "name": "Social Security Overpayment Notice"
    },
    "GOV-03": {
        "signals": ["continuing disability review", "cdr", "medical review",
                    "your disability benefits", "still disabled"],
        "urgency": "YELLOW", "name": "Social Security Disability Review"
    },
    "GOV-04": {
        "signals": ["unemployment", "unemployment insurance", "ui claim",
                    "disqualified", "claim determination", "benefit year"],
        "urgency": "YELLOW", "name": "Unemployment Benefits Notice"
    },
    "GOV-05": {
        "signals": ["snap", "food stamps", "ebt", "supplemental nutrition",
                    "benefit amount", "food assistance", "case number"],
        "urgency": "YELLOW", "name": "SNAP / Food Stamp Notice"
    },
    "GOV-07": {
        "signals": ["summons", "plaintiff", "defendant", "you are hereby summoned",
                    "respond within", "civil action", "complaint filed"],
        "urgency": "RED", "name": "Civil Court Summons"
    },
    "GOV-08": {
        "signals": ["criminal summons", "arraignment", "misdemeanor", "felony",
                    "charges against you", "appear before", "criminal complaint"],
        "urgency": "RED", "name": "Criminal Court Summons"
    },
    "GOV-10": {
        "signals": ["jury duty", "juror", "report for jury service",
                    "petit jury", "grand jury", "summons for jury"],
        "urgency": "GREEN", "name": "Jury Duty Notice"
    },
    "GOV-12": {
        "signals": ["uscis", "department of homeland security", "i-485", "i-130",
                    "request for evidence", "rfe", "notice of action", "receipt number"],
        "urgency": "YELLOW", "name": "USCIS / Immigration Notice"
    },
    "GOV-13": {
        "signals": ["notice to appear", "nta", "removal proceedings",
                    "immigration court", "deportation", "order of removal"],
        "urgency": "RED", "name": "Immigration Notice to Appear (NTA)"
    },

    # ── Education ─────────────────────────────────────────────────────────────
    "EDU-01": {
        "signals": ["fafsa", "financial aid", "expected family contribution", "efc",
                    "student aid index", "sai", "award letter", "federal grant"],
        "urgency": "YELLOW", "name": "FAFSA / Financial Aid Notice"
    },
    "EDU-03": {
        "signals": ["iep", "individualized education program", "504 plan",
                    "special education", "learning disability", "related services"],
        "urgency": "GREEN", "name": "IEP / Special Education Document"
    },

    # ── Employment ────────────────────────────────────────────────────────────
    "EMP-03": {
        "signals": ["open enrollment", "benefits enrollment", "health plan selection",
                    "deadline to enroll", "dependent coverage", "hsa", "fsa contribution"],
        "urgency": "YELLOW", "name": "Employee Benefits Enrollment"
    },
    "EMP-05": {
        "signals": ["cobra", "continuation coverage", "election period",
                    "qualified beneficiary", "coverage continuation"],
        "urgency": "YELLOW", "name": "COBRA Notice"
    },
    "EMP-06": {
        "signals": ["termination", "laid off", "separation agreement", "severance",
                    "last day of employment", "workforce reduction"],
        "urgency": "YELLOW", "name": "Termination / Layoff Letter"
    },
}

# ─── Special Mode Detection ───────────────────────────────────────────────────

SENIOR_SIGNALS = [
    "medicare", "medicaid", "social security", "pension", "retirement",
    "senior", "elderly", "aging", "65", "over 65", "my mother", "my father",
    "my parent", "mom", "dad", "grandma", "grandpa", "nursing home",
    "assisted living", "memory care", "cola notice"
]

IMMIGRANT_SIGNALS = [
    "uscis", "immigration", "visa", "green card", "i-485", "i-130",
    "citizenship", "naturalization", "english is not", "my english",
    "translate", "spanish", "mandarin", "vietnamese", "haitian",
    "work authorization", "ead", "employment authorization"
]

CAREGIVER_SIGNALS = [
    "my mother", "my father", "my parent", "caring for", "caregiver",
    "power of attorney", "taking care of", "on behalf of",
    "my elderly", "my disabled", "her medical", "his medical"
]

CRISIS_SIGNALS = [
    "pay or quit", "eviction", "shutoff", "garnishment", "levy",
    "notice to appear", "removal proceedings", "final notice before",
    "right to cure", "repossession", "foreclosure", "writ of possession",
    "unlawful detainer", "cps", "child protective"
]

SCAM_SIGNALS = [
    "gift card", "wire transfer", "bitcoin", "cryptocurrency", "western union",
    "moneygram", "arrested", "police on their way", "suspended",
    "warrant for your arrest", "deportation warrant", "your ssa number",
    "your social security number has been"
]


# ─── Classification Engine ────────────────────────────────────────────────────

def classify(text):
    text_lower = text.lower()
    scores = {}

    for doc_id, config in DOC_SIGNALS.items():
        score = sum(1 for s in config["signals"] if s in text_lower)
        if score > 0:
            scores[doc_id] = score

    if scores:
        best_id = max(scores, key=scores.get)
        best_config = DOC_SIGNALS[best_id]
    else:
        best_id = "UNKNOWN"
        best_config = {"name": "Unknown Document", "urgency": "GREEN"}

    # Detect special modes
    modes = []
    if any(s in text_lower for s in SENIOR_SIGNALS):
        modes.append("senior")
    if any(s in text_lower for s in IMMIGRANT_SIGNALS):
        modes.append("immigrant")
    if any(s in text_lower for s in CAREGIVER_SIGNALS):
        modes.append("caregiver")
    if any(s in text_lower for s in CRISIS_SIGNALS):
        modes.append("crisis")

    # Scam check
    scam_flags = [s for s in SCAM_SIGNALS if s in text_lower]
    is_potential_scam = len(scam_flags) >= 1

    # Crisis override — if crisis signals found, escalate urgency
    urgency = best_config.get("urgency", "GREEN")
    if "crisis" in modes:
        urgency = "RED"

    # Extract key numbers and dates
    amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?|\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars?|USD)', text, re.IGNORECASE)
    dates = re.findall(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text, re.IGNORECASE)
    ref_numbers = re.findall(r'(?:case|claim|account|reference|notice|member|invoice|confirmation)\s*(?:number|#|no\.?)?\s*:?\s*([A-Z0-9-]{4,20})', text, re.IGNORECASE)

    signals_found = [s for s in DOC_SIGNALS.get(best_id, {}).get("signals", []) if s in text_lower]

    return {
        "document_type": best_id,
        "document_name": best_config.get("name", "Unknown"),
        "urgency_code": urgency,
        "urgency_label": URGENCY.get(urgency, urgency),
        "urgency_short": URGENCY_SHORT.get(urgency, urgency),
        "special_modes": modes,
        "potential_scam": is_potential_scam,
        "scam_flags": scam_flags,
        "key_amounts": amounts[:5],
        "key_dates": dates[:5],
        "reference_numbers": [r[0] if isinstance(r, tuple) else r for r in ref_numbers[:3]],
        "signals_matched": signals_found,
        "confidence": min(scores.get(best_id, 0), 5),
    }


def print_result(result):
    print(f"\n📄 Document: {result['document_name']} ({result['document_type']})")
    print(f"   {result['urgency_label']}")

    if result["potential_scam"]:
        print(f"\n⚠️  POSSIBLE SCAM — Red flags detected: {', '.join(result['scam_flags'])}")

    if result["special_modes"]:
        modes_str = ", ".join(result["special_modes"])
        print(f"   Special modes: {modes_str}")

    if result["key_amounts"]:
        print(f"\n   💰 Amounts found: {', '.join(result['key_amounts'])}")
    if result["key_dates"]:
        print(f"   📅 Dates found: {', '.join(result['key_dates'])}")
    if result["reference_numbers"]:
        print(f"   🔢 Reference numbers: {', '.join(result['reference_numbers'])}")

    print(f"\n   Confidence: {result['confidence']}/5")
    if result["signals_matched"]:
        print(f"   Signals: {', '.join(result['signals_matched'][:4])}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Classify a life document")
    parser.add_argument("--text", help="Document text")
    parser.add_argument("--file", help="Document text file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    result = classify(text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)


if __name__ == "__main__":
    main()
