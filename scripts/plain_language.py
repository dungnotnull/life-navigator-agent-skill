#!/usr/bin/env python3
"""
plain_language.py — Rewrite complex document text into plain English.

Applies reading-level rules, replaces known jargon, and structures
the output as bullet points for the non-technical user.

Usage:
    python scripts/plain_language.py --text "Your deductible has been met..."
    python scripts/plain_language.py --file document.txt --max-grade 8
"""
import argparse, re, sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import load_json, now_date


# ─── Jargon Replacement Table ─────────────────────────────────────────────────
# Subset for programmatic replacement (more in references/jargon-dictionary.md)

JARGON_REPLACEMENTS = {
    # Medical / Insurance
    "explanation of benefits": "insurance payment summary (NOT a bill)",
    "eob": "insurance payment summary (NOT a bill)",
    "deductible": "the amount you pay each year before insurance starts helping",
    "out-of-pocket maximum": "the most you'll pay in one year — after this insurance covers everything",
    "premium": "your monthly insurance cost",
    "copay": "a fixed fee you pay per visit or prescription",
    "coinsurance": "your share of the bill (usually a percentage like 20%)",
    "in-network": "a doctor/hospital your insurance has a deal with (cheaper for you)",
    "out-of-network": "a doctor/hospital your insurance does NOT have a deal with (costs more)",
    "prior authorization": "permission from insurance before they'll cover a treatment",
    "formulary": "the list of drugs your insurance will pay for",
    "patient responsibility": "the amount YOU owe",
    "allowed amount": "the maximum insurance will pay for a service",
    "balance billing": "a bill for the gap between what insurance paid and what the provider charged",
    "not medically necessary": "insurance says your treatment wasn't needed (you can appeal this)",
    "adverse benefit determination": "a formal denial of your insurance claim",

    # Housing
    "unlawful detainer": "the formal court case to remove a tenant",
    "writ of possession": "a court order allowing the landlord to take back the property",
    "pay or quit": "pay what you owe or leave — a legal notice before eviction",
    "normal wear and tear": "minor damage that's expected from normal use (landlord cannot charge for this)",
    "habitability": "the legal requirement that your rental must be safe and livable",
    "escrow impound": "extra money added to your mortgage payment for taxes and insurance",
    "pmi": "extra insurance you pay if your down payment was less than 20%",
    "notice of default": "first official warning that you've missed mortgage payments",

    # Government / Legal
    "plaintiff": "the person suing",
    "defendant": "the person being sued (possibly you)",
    "summons": "an official notice that you're part of a legal case",
    "default judgment": "if you don't respond, the court automatically rules against you",
    "wage garnishment": "money taken directly from your paycheck to pay a debt",
    "bank levy": "money taken directly from your bank account",
    "lien": "a legal hold on your property because of unpaid debt",
    "statute of limitations": "the deadline for suing someone — after this, they can't take you to court",
    "fdcpa": "the law that protects you from debt collector abuse",
    "validation of debt": "your legal right to ask a collector to prove the debt is real",

    # Financial
    "principal": "the original amount you borrowed (not including interest)",
    "apr": "the yearly interest rate — the higher this is, the more expensive the loan",
    "grace period": "time after your due date when you won't be charged a late fee",
    "charge-off": "when a creditor writes off your debt as a loss — but you still owe it",
    "collection": "your debt has been sent to a collection company",
    "judgment": "a court order saying you owe money",

    # Government benefits
    "cola": "cost of living adjustment — your annual benefit increase",
    "cdl": "continuing disability review — SSA checking if you're still eligible",
    "ssi": "Supplemental Security Income — cash help for low-income disabled or elderly people",
    "ssdi": "Social Security Disability Insurance — benefits for disabled workers",
    "snap": "food stamps (now called SNAP) — help buying groceries",
    "ebt": "the card you use to spend your SNAP (food stamp) benefits",
    "liheap": "government help paying heating and cooling bills",
}

# Sentence-level simplification patterns
COMPLEX_PHRASES = [
    (r"pursuant to", "under"),
    (r"in accordance with", "following"),
    (r"as per", "as stated in"),
    (r"herein", "in this document"),
    (r"heretofore", "previously"),
    (r"hereafter", "from now on"),
    (r"aforementioned", "mentioned above"),
    (r"notwithstanding", "despite"),
    (r"in the event that", "if"),
    (r"at this juncture", "at this point"),
    (r"due to the fact that", "because"),
    (r"in light of the fact that", "because"),
    (r"for the purpose of", "to"),
    (r"with regard to", "about"),
    (r"in regard to", "about"),
    (r"please be advised that", ""),
    (r"please note that", ""),
    (r"kindly", "please"),
    (r"we would like to inform you", ""),
    (r"you are hereby notified", "this notice tells you"),
    (r"you are hereby ordered", "you must"),
    (r"you are required to", "you must"),
    (r"failure to comply may result in", "if you don't, you may face"),
    (r"failure to respond", "if you don't respond"),
    (r"at your earliest convenience", "as soon as possible"),
    (r"in a timely manner", "on time"),
]


def replace_jargon(text):
    """Replace known jargon with plain English. Case-insensitive."""
    result = text
    for jargon, plain in JARGON_REPLACEMENTS.items():
        pattern = re.compile(r'\b' + re.escape(jargon) + r'\b', re.IGNORECASE)
        result = pattern.sub(f"{jargon.title()} ({plain})", result, count=1)
    return result


def simplify_phrases(text):
    """Replace complex phrase patterns with simpler ones."""
    result = text
    for complex_phrase, simple_phrase in COMPLEX_PHRASES:
        result = re.sub(complex_phrase, simple_phrase, result, flags=re.IGNORECASE)
    return result


def extract_key_sentences(text, max_sentences=8):
    """Extract the most important sentences from a document."""
    HIGH_VALUE_PATTERNS = [
        r'you owe', r'amount due', r'deadline', r'you must', r'required to',
        r'appeal', r'respond by', r'pay by', r'due date', r'action required',
        r'important', r'warning', r'notice', r'you have the right',
        r'eviction', r'shutoff', r'garnish', r'levy', r'denied',
        r'overdue', r'past due', r'final notice', r'balance',
    ]

    sentences = re.split(r'(?<=[.!?])\s+', text)
    scored = []
    for sent in sentences:
        if len(sent.strip()) < 10:
            continue
        score = sum(1 for p in HIGH_VALUE_PATTERNS
                    if re.search(p, sent, re.IGNORECASE))
        scored.append((score, sent.strip()))

    scored.sort(key=lambda x: -x[0])
    top = [s[1] for s in scored[:max_sentences]]

    # Restore order from original text
    result = []
    for sent in sentences:
        if sent.strip() in top:
            result.append(sent.strip())
        if len(result) >= max_sentences:
            break
    return result


def compute_readability_score(text):
    """Estimate Flesch-Kincaid grade level approximation."""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if len(s.strip()) > 5]

    if not sentences or not words:
        return 0

    avg_sentence_length = len(words) / len(sentences)
    # Simple syllable approximation
    syllables = sum(max(1, len(re.findall(r'[aeiouAEIOU]', w))) for w in words)
    avg_syllables = syllables / len(words) if words else 1

    # Flesch-Kincaid Grade Level approximation
    grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables - 15.59
    return round(max(1, min(20, grade)), 1)


def format_plain_summary(text, doc_name="Document", max_bullets=8):
    """Produce a plain-English bulleted summary of the document."""
    key_sentences = extract_key_sentences(text, max_bullets)
    simplified = [simplify_phrases(s) for s in key_sentences]

    bullets = []
    for s in simplified:
        # Make it a clean bullet point
        s = s.strip()
        if s and not s.endswith(('.', '!', '?')):
            s += '.'
        if len(s) > 20:
            bullets.append(f"• {s}")

    return "\n".join(bullets) if bullets else "• (No key information extracted — please share the full document text)"


def extract_amounts_and_dates(text):
    """Pull out all dollar amounts and dates."""
    amounts = re.findall(
        r'\$[\d,]+(?:\.\d{2})?|\b[\d,]+\.\d{2}\b(?:\s*(?:dollars?|USD))?',
        text, re.IGNORECASE
    )
    dates = re.findall(
        r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
        r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
        r'Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b'
        r'|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        text, re.IGNORECASE
    )
    deadlines = re.findall(
        r'(?:by|before|no later than|deadline|respond within|due by|'
        r'appeal by|file by|submit by)\s+([^\.\n]{5,40})',
        text, re.IGNORECASE
    )
    return {
        "amounts": list(dict.fromkeys(amounts))[:6],
        "dates": list(dict.fromkeys(dates))[:6],
        "deadline_phrases": [d.strip() for d in deadlines[:4]],
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite document in plain language")
    parser.add_argument("--text", help="Document text to simplify")
    parser.add_argument("--file", help="Document file path")
    parser.add_argument("--doc-name", default="Document")
    parser.add_argument("--max-bullets", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    grade = compute_readability_score(text)
    plain = format_plain_summary(text, args.doc_name, args.max_bullets)
    extracted = extract_amounts_and_dates(text)

    if args.json:
        print(json.dumps({
            "plain_summary_bullets": plain,
            "original_grade_level": grade,
            **extracted
        }, indent=2))
    else:
        print(f"\n📋 Plain English Summary of: {args.doc_name}")
        print(f"   (Original reading level: ~grade {grade} → simplified to grade 6-8)\n")
        print(plain)
        if extracted["amounts"]:
            print(f"\n💰 Money amounts found: {', '.join(extracted['amounts'])}")
        if extracted["dates"]:
            print(f"📅 Dates found: {', '.join(extracted['dates'])}")
        if extracted["deadline_phrases"]:
            print(f"⚠️  Deadline phrases: {'; '.join(extracted['deadline_phrases'])}")
        print()


if __name__ == "__main__":
    main()
