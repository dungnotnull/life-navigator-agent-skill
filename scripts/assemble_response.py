#!/usr/bin/env python3
"""
assemble_response.py — Assemble the full Life Navigator response from all components.

Combines: classification + plain language summary + action plan + phone scripts + resources

Usage:
    python scripts/assemble_response.py \
        --classification /tmp/lna/classification.json \
        --plain-summary /tmp/lna/plain_summary.json \
        --action-plan /tmp/lna/action_plan.json \
        --output /tmp/lna/response.md
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import save_text, now_date, LNA_VERSION, URGENCY_COLORS, MODE_LABELS


URGENCY_LABELS = {
    "RED":    "🔴 URGENT — Respond within 24–48 hours",
    "YELLOW": "🟡 TIME-SENSITIVE — Respond within 1–2 weeks",
    "GREEN":  "🟢 NORMAL — Respond as directed",
    "INFO":   "ℹ️  INFORMATIONAL — No action required",
}

SCAM_WARNING_TEXT = """
⚠️ THIS LOOKS LIKE IT MIGHT BE A SCAM

Based on what you shared, this document or message has warning signs of fraud.

What NOT to do:
• Do NOT call any number from this letter or message
• Do NOT send money, gift cards, or wire transfers
• Do NOT give your Social Security number, bank account, or credit card

What to do instead:
• If it claims to be from the IRS → Call IRS directly: 1-800-829-1040
• If it claims to be from SSA → Call SSA directly: 1-800-772-1213
• If it claims to be from Medicare → Call Medicare: 1-800-633-4227
• Report the scam at reportfraud.ftc.gov

Remember: Government agencies always send letters first. They do not demand
immediate payment by gift card, wire transfer, or cryptocurrency.
"""

SENIOR_INTRO = """
💡 Note for seniors and their families: This type of document is handled
differently — I've added extra resources specifically for seniors at the bottom.
"""

CAREGIVER_NOTE = """
💡 Caregiver note: If you're managing this for a family member, make sure you
have legal authority to act on their behalf (Power of Attorney or Health Care Proxy).
If you don't have this yet, a legal aid organization can help you get it.
"""

IMMIGRANT_NOTE = """
💡 Note: If English is not your first language, look for community organizations
in your area that offer free document translation and navigation help.
"""


def assemble(classification, plain_summary, action_plan, doc_text_snippet=None):
    """Assemble the full navigator response."""
    doc_type = classification.get("document_type", "UNKNOWN")
    doc_name = classification.get("document_name", "Official Document")
    urgency = classification.get("urgency_code", "GREEN")
    urgency_label = URGENCY_LABELS.get(urgency, urgency)
    modes = classification.get("special_modes", [])
    is_scam = classification.get("potential_scam", False)
    scam_flags = classification.get("scam_flags", [])
    amounts = classification.get("key_amounts", [])
    dates = classification.get("key_dates", [])
    refs = classification.get("reference_numbers", [])

    lines = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines.append(f"📄 {doc_name}")
    lines.append(f"   {urgency_label}")
    if modes:
        mode_str = " | ".join(MODE_LABELS.get(m, m) for m in modes)
        lines.append(f"   {mode_str}")
    lines.append("")

    # ── Scam warning (highest priority) ──────────────────────────────────────
    if is_scam:
        lines.append(SCAM_WARNING_TEXT)
        lines.append("─" * 50)
        lines.append("")
        lines.append("If you believe this IS a legitimate document (not a scam),")
        lines.append("please verify it through the official agency and continue reading.")
        lines.append("")

    # ── Mode-specific notes ───────────────────────────────────────────────────
    if "senior" in modes and not is_scam:
        lines.append(SENIOR_INTRO.strip())
        lines.append("")
    if "caregiver" in modes:
        lines.append(CAREGIVER_NOTE.strip())
        lines.append("")
    if "immigrant" in modes:
        lines.append(IMMIGRANT_NOTE.strip())
        lines.append("")

    # ── Crisis acknowledgment ─────────────────────────────────────────────────
    if urgency == "RED" and not is_scam:
        lines.append("I can see this is a stressful situation. Let's focus on")
        lines.append("the most important steps you can take right now.")
        lines.append("")

    # ── Plain language summary ────────────────────────────────────────────────
    lines.append("─" * 50)
    lines.append("WHAT THIS SAYS (IN PLAIN ENGLISH)")
    lines.append("─" * 50)
    lines.append("")

    bullets = plain_summary.get("plain_summary_bullets", "")
    if bullets:
        lines.append(bullets)
    else:
        lines.append("• This document requires your attention.")
        lines.append("• Please share the document text for a detailed explanation.")
    lines.append("")

    # ── Key facts ─────────────────────────────────────────────────────────────
    if amounts or dates or refs:
        lines.append("Key details from this document:")
        if amounts:
            lines.append(f"  💰 Amount(s) mentioned: {', '.join(amounts[:3])}")
        if dates:
            lines.append(f"  📅 Date(s) mentioned: {', '.join(dates[:3])}")
        if refs:
            lines.append(f"  🔢 Reference number(s): {', '.join(refs[:2])}")
        lines.append("")

    # ── Worry assessment ──────────────────────────────────────────────────────
    lines.append("─" * 50)
    lines.append("SHOULD YOU BE WORRIED?")
    lines.append("─" * 50)
    lines.append("")

    worry_text = {
        "RED":    "Yes — this document needs your attention very soon. But there ARE steps you can take, and help is available. Don't panic — take it one step at a time.",
        "YELLOW": "This document needs attention, but you have some time to act. Don't ignore it — address it within the next 1–2 weeks.",
        "GREEN":  "This is a normal document that most people receive. It needs a response, but it's not an emergency.",
        "INFO":   "No — this is an informational notice only. You don't need to do anything unless you spot an error.",
    }.get(urgency, "Review the document carefully and respond as directed.")

    lines.append(worry_text)
    lines.append("")

    # ── Action plan ───────────────────────────────────────────────────────────
    steps = action_plan.get("steps", [])
    deadline_note = action_plan.get("deadline_note")

    lines.append("─" * 50)
    lines.append("WHAT TO DO NEXT")
    lines.append("─" * 50)
    lines.append("")

    for i, step in enumerate(steps, 1):
        if isinstance(step, (list, tuple)) and len(step) == 2:
            title, detail = step
        elif isinstance(step, dict):
            title = step.get("title", "")
            detail = step.get("detail", "")
        else:
            title, detail = str(step), ""

        lines.append(f"{i}. {title}")
        if detail:
            lines.append(f"   → {detail}")
        lines.append("")

    # ── Deadline box ──────────────────────────────────────────────────────────
    if deadline_note:
        lines.append("")
        lines.append("─" * 50)
        lines.append(deadline_note)
        lines.append("─" * 50)
        lines.append("")

    # ── Resources ─────────────────────────────────────────────────────────────
    resources = action_plan.get("resources", [])
    if resources:
        lines.append("─" * 50)
        lines.append("🆘 WHERE TO GET MORE HELP")
        lines.append("─" * 50)
        lines.append("")
        for r in resources:
            lines.append(f"  • {r}")
        lines.append("")
        lines.append("  📞 For any local help: Call 2-1-1 (free, 24/7)")
        lines.append("")

    # ── Footer ────────────────────────────────────────────────────────────────
    lines.append("─" * 50)
    lines.append("💬 Questions? Describe what you don't understand and I'll")
    lines.append("   explain it further. You can also ask me to write a letter")
    lines.append("   or script for a specific call.")
    lines.append("─" * 50)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Assemble full navigator response")
    parser.add_argument("--classification", required=True)
    parser.add_argument("--plain-summary", required=True)
    parser.add_argument("--action-plan", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.classification) as f:
        classification = json.load(f)
    with open(args.plain_summary) as f:
        plain_summary = json.load(f)
    with open(args.action_plan) as f:
        action_plan = json.load(f)

    response = assemble(classification, plain_summary, action_plan)
    save_text(response, args.output)

    print(f"\n✅ Response assembled: {args.output}", file=sys.stderr)
    print(f"   Document: {classification.get('document_name')}", file=sys.stderr)
    print(f"   Urgency:  {classification.get('urgency_code')}", file=sys.stderr)
    print(f"   Modes:    {classification.get('special_modes', [])}", file=sys.stderr)


if __name__ == "__main__":
    main()
