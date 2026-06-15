#!/usr/bin/env python3
"""
action_plan.py — Generate a numbered action plan for a classified document.

Usage:
    python scripts/action_plan.py --doc-type HSG-03 --urgency RED
    python scripts/action_plan.py --classification /tmp/lna/classification.json
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import LNA_VERSION, now_date

# ─── Action Plans by Document Type ───────────────────────────────────────────

ACTION_PLANS = {

    # ── Medical ───────────────────────────────────────────────────────────────
    "MED-01": {
        "title": "Medical / Hospital Bill",
        "steps": [
            ("Request an itemized bill",
             "Call the billing department and say: 'I'd like an itemized bill showing every individual charge.' You have the right to this."),
            ("Check it against your EOB",
             "Compare the bill to your Explanation of Benefits (EOB) from your insurance company. The amounts should match."),
            ("Ask about financial assistance",
             "Ask the billing department: 'Do you have a charity care or financial hardship program?' Many hospitals will reduce or forgive bills for qualifying patients."),
            ("Set up a payment plan if needed",
             "Ask: 'Can I set up a monthly payment plan?' Most hospitals offer this — often interest-free."),
            ("Dispute any errors",
             "If you see charges for services you didn't receive, call the billing department to dispute them in writing."),
        ],
        "resources": ["Hospital billing department", "Patient Advocate Foundation: 1-800-532-5274", "NeedyMeds.org for prescription help"],
        "deadline_note": None,
        "phone_script_key": "SCRIPT-01",
    },

    "MED-02": {
        "title": "Insurance EOB (Explanation of Benefits)",
        "steps": [
            ("Remember: this is NOT a bill",
             "An EOB is just a summary of what insurance paid. You don't owe money from this document alone — wait for the actual bill."),
            ("Review for accuracy",
             "Check that the service, date, and provider listed are correct. If something looks wrong, call your insurance company."),
            ("Note your deductible and out-of-pocket progress",
             "EOBs show how much of your annual deductible you've used. Keep these to track your progress."),
            ("File it for your records",
             "Keep this EOB with your medical records in case you're billed separately later."),
        ],
        "resources": ["Your insurance member services number (on your insurance card)"],
        "deadline_note": None,
        "phone_script_key": "SCRIPT-02",
    },

    "MED-05": {
        "title": "Insurance Denial / Prior Authorization Denial",
        "steps": [
            ("Read the denial reason carefully",
             "The letter must explain why it was denied. Write down the reason code and the exact reason."),
            ("Note your appeal deadline immediately",
             "Appeal deadlines are strict — usually 30–180 days. Missing this deadline may end your right to appeal."),
            ("Ask your doctor to write a letter",
             "Your doctor can write a 'letter of medical necessity' explaining why this treatment is required. This is often all you need to win an appeal."),
            ("File a formal appeal in writing",
             "Call your insurance company and ask for the appeal process. Submit in writing by certified mail so you have proof."),
            ("Request an External Review if appeal is denied",
             "If internal appeal fails, you have the right to an independent External Review — it's free and often successful."),
            ("Contact your State Insurance Commissioner if needed",
             "If the insurance company is unresponsive, file a complaint at your state's insurance commissioner office."),
        ],
        "resources": [
            "Your insurance appeal address (in the denial letter)",
            "State Insurance Commissioner: naic.org/state_web_map.htm",
            "Medicare Rights Center: 1-800-333-4114 (for Medicare denials)",
        ],
        "deadline_note": "⚠️ Check the denial letter for your appeal deadline — missing it may forfeit your rights.",
        "phone_script_key": "SCRIPT-02",
    },

    "HSG-03": {
        "title": "Pay or Quit Notice (Eviction Warning)",
        "steps": [
            ("Do NOT ignore this notice",
             "This is a legal document. Ignoring it will lead to a court case being filed against you."),
            ("Check the exact deadline",
             "The notice will say how many days you have (usually 3–5 days). Count carefully from the date on the notice."),
            ("Try to pay or contact your landlord immediately",
             "If you can pay, do so right away and get written confirmation. If you can't pay the full amount, contact your landlord — they may accept a payment plan."),
            ("Call 211 for emergency rental assistance",
             "Dial 2-1-1 from any phone. There may be emergency funds available in your area that can help pay the rent."),
            ("Contact a legal aid organization today",
             "Call your local legal aid office (find at lsc.gov/find-legal-aid). They provide free legal help for eviction cases. Do this even if you think you owe the money."),
            ("Gather your documents",
             "Collect your lease, any receipts of rent paid, and any communication with your landlord. You may need these."),
        ],
        "resources": [
            "211 (dial 2-1-1) — emergency rental assistance",
            "Legal Aid: lsc.gov/find-legal-aid",
            "HUD Housing Counselors: 1-800-569-4287",
            "National Low Income Housing Coalition: nlihc.org",
        ],
        "deadline_note": "🔴 URGENT: Count the days from the notice date. Missing this deadline leads to court filing.",
        "phone_script_key": "SCRIPT-07",
    },

    "HSG-05": {
        "title": "Utility Shutoff Warning",
        "steps": [
            ("Call the utility company today",
             "Ask about payment plans and assistance programs. Say: 'I received a shutoff notice. Do you have a payment plan or assistance program I can apply for?'"),
            ("Ask about LIHEAP",
             "Ask the utility company: 'Do you participate in LIHEAP?' — this is a federal program that can pay part of your bill."),
            ("Call 211 for emergency energy assistance",
             "Dial 2-1-1. They can connect you to local programs that help pay utility bills quickly."),
            ("Tell them about medical needs",
             "If anyone in your home has a medical condition requiring electricity or heat, tell the utility company. Most states have special protections for medical necessity."),
            ("Note any shutoff protection periods",
             "Many states ban shutoffs during extreme cold or heat — ask if a protection period applies."),
        ],
        "resources": [
            "211 (dial 2-1-1)",
            "LIHEAP: liheap.acf.hhs.gov",
            "Your utility company's assistance program",
        ],
        "deadline_note": "🔴 URGENT: Call today — shutoff can happen quickly after the notice date.",
        "phone_script_key": "SCRIPT-07",
    },

    "FIN-01": {
        "title": "Debt Collection Letter",
        "steps": [
            ("Don't panic — verify the debt first",
             "You have the right to ask the collector to prove this debt is real and that they have the right to collect it."),
            ("Send a debt validation request within 30 days",
             "Write a letter (certified mail, return receipt) requesting: the original creditor's name, amount owed and how calculated, proof they own the debt. Once you send this, they must stop collection until they verify."),
            ("Check if the debt is too old to sue you",
             "Every state has a 'statute of limitations' — a deadline for suing over a debt. An old debt may still exist but they may not be able to take you to court. Ask a legal aid attorney."),
            ("Do not ignore a real debt",
             "If the debt is verified and valid, contact the collector to negotiate. Many will accept less than the full amount. Get any agreement in writing before paying."),
            ("File a complaint for illegal tactics",
             "Debt collectors cannot threaten, harass, or lie to you. If they do, file a complaint at consumerfinance.gov or ftc.gov."),
        ],
        "resources": [
            "CFPB Consumer Complaint: consumerfinance.gov/complaint",
            "FTC: ftc.gov/complaint",
            "National Foundation for Credit Counseling: 1-800-388-2227",
        ],
        "deadline_note": "⚠️ You have 30 days from receiving this letter to send a debt validation request.",
        "phone_script_key": "SCRIPT-06",
    },

    "FIN-04": {
        "title": "IRS Final Notice — Intent to Levy",
        "steps": [
            ("Act immediately — this is urgent",
             "You have 30 days from the notice date to request a Collection Due Process (CDP) hearing. Doing this STOPS the levy while your case is reviewed."),
            ("Call the Taxpayer Advocate Service (TAS) today",
             "TAS is a free, independent IRS helper. Call 1-877-777-4778. They specialize in situations like yours."),
            ("Call the IRS directly if you can",
             "Call 1-800-829-1040. Ask about an installment agreement (payment plan) or 'Currently Not Collectible' status if you truly cannot pay."),
            ("Do NOT ignore this notice",
             "Ignoring a levy notice can result in your bank account or wages being seized with no further warning."),
            ("Consider free legal help",
             "Low Income Taxpayer Clinics (LITC) provide free legal representation against the IRS. Find one at taxpayeradvocate.irs.gov/litc"),
        ],
        "resources": [
            "Taxpayer Advocate Service: 1-877-777-4778 (FREE)",
            "IRS: 1-800-829-1040",
            "Low Income Taxpayer Clinics: taxpayeradvocate.irs.gov/litc",
            "IRS Payment Plan: irs.gov/payments",
        ],
        "deadline_note": "🔴 URGENT: You have 30 days from the notice date to file a CDP hearing request to stop the levy.",
        "phone_script_key": "SCRIPT-05",
    },

    "GOV-02": {
        "title": "Social Security Overpayment Notice",
        "steps": [
            ("Read the notice carefully",
             "The letter says how much SSA believes they overpaid you and asks you to pay it back. You have options — you don't have to pay it all back immediately."),
            ("You can request a waiver",
             "If paying it back would cause financial hardship, OR if it wasn't your fault, you can ask SSA to waive (forgive) the overpayment. File SSA Form 632-BK."),
            ("You can appeal if you disagree",
             "If you think SSA made a mistake, you can appeal within 60 days. File SSA Form 561."),
            ("Request a payment plan",
             "If you must repay it, ask SSA for a monthly payment plan you can afford. They generally accept plans that work for your budget."),
            ("Keep getting your benefits while you appeal",
             "Ask SSA to keep paying your current benefits while your appeal or waiver is being reviewed — they usually will."),
        ],
        "resources": [
            "SSA: 1-800-772-1213",
            "SSA Form 632-BK (Waiver Request): ssa.gov/forms/ssa-632.pdf",
            "National Organization of Social Security Claimants' Representatives: nosscr.org",
        ],
        "deadline_note": "⚠️ You have 60 days from the notice date to appeal. You have no hard deadline for a waiver request, but file it quickly.",
        "phone_script_key": "SCRIPT-04",
    },

    "GOV-07": {
        "title": "Civil Court Summons",
        "steps": [
            ("Do NOT ignore this — respond by the deadline",
             "If you don't respond to a civil summons, the court will automatically rule against you (a 'default judgment'). This is one of the worst outcomes."),
            ("Note the response deadline immediately",
             "The summons will say how many days you have to respond — usually 20–30 days. Write this date down now."),
            ("Get legal help immediately",
             "Contact legal aid (lsc.gov/find-legal-aid) or a private attorney. Many offer free consultations. The summons will explain what you're being sued for."),
            ("Visit the court's self-help center",
             "Most courthouses have a free self-help center where staff can explain the paperwork and help you file a response."),
            ("File an 'Answer' to respond formally",
             "You respond to a summons by filing an 'Answer' — a document explaining your side. Legal aid or the court self-help center can help you prepare this."),
        ],
        "resources": [
            "Legal Aid: lsc.gov/find-legal-aid",
            "Court Self-Help Center (at your local courthouse)",
            "LawHelp.org — free legal help in your state",
        ],
        "deadline_note": "🔴 URGENT: Respond before the deadline in the summons. Missing it results in automatic judgment against you.",
        "phone_script_key": None,
    },

    "GOV-13": {
        "title": "Immigration Notice to Appear (NTA)",
        "steps": [
            ("Do NOT miss the court date — this is critical",
             "Missing your immigration court date results in an automatic removal order. No matter what, show up to court."),
            ("Hire an immigration attorney immediately",
             "This is too serious to handle without legal help. Contact an immigration attorney or accredited representative today."),
            ("Find free/low-cost immigration legal help",
             "Go to immigrationadvocates.org to find free or low-cost immigration legal aid in your area."),
            ("Do not sign anything you don't understand",
             "Never sign documents related to your immigration case without having them explained by an attorney."),
            ("Prepare your documents",
             "Gather all your immigration documents: passport, visa, I-94, any USCIS notices, employment records, family ties in the US."),
        ],
        "resources": [
            "Immigration Advocates Network: immigrationadvocates.org",
            "USCIS: 1-800-375-5283",
            "National Immigration Law Center: nilc.org",
            "DOJ Accredited Representatives list: justice.gov/eoir",
        ],
        "deadline_note": "🔴 CRITICAL: Your court date is on the notice. Do NOT miss it under any circumstances.",
        "phone_script_key": None,
    },

    "EMP-05": {
        "title": "COBRA Continuation Coverage Notice",
        "steps": [
            ("Understand your deadline",
             "You have exactly 60 days from the date of this notice to elect COBRA coverage. After that, your option expires permanently."),
            ("Compare costs and alternatives",
             "COBRA lets you keep your current insurance but you pay the full premium (often $400–$700+/month for one person). Compare to Healthcare.gov marketplace plans, which may be cheaper."),
            ("Check if you qualify for Medicaid",
             "If your income dropped after losing your job, you may qualify for free or low-cost Medicaid. Apply at healthcare.gov or your state Medicaid office."),
            ("If you have ongoing medical needs, elect COBRA first",
             "COBRA keeps your exact same doctors and coverage. If you're in treatment or have upcoming procedures, COBRA may be worth the higher cost."),
            ("Elect coverage in writing",
             "To elect COBRA, complete the election form in the notice and send it back by the deadline. Keep a copy."),
        ],
        "resources": [
            "Healthcare.gov — compare marketplace plans",
            "Your state Medicaid office: medicaid.gov",
            "DOL COBRA info: dol.gov/general/topic/health-plans/cobra",
        ],
        "deadline_note": "⚠️ You have exactly 60 days from this notice to elect COBRA. This deadline cannot be extended.",
        "phone_script_key": None,
    },
}

# Fallback action plan for unrecognized document types
DEFAULT_PLAN = {
    "title": "Official Document",
    "steps": [
        ("Read the entire document carefully",
         "Look for: who sent it, what they're asking you to do, and any deadlines."),
        ("Note any deadlines",
         "Write down any dates mentioned. Missing a deadline can affect your rights."),
        ("Gather any reference or account numbers",
         "These will be needed if you call to ask questions."),
        ("Contact the sender if anything is unclear",
         "Use the phone number or address printed on the document itself — not a number from a web search, in case of scams."),
        ("Get help if you're unsure",
         "Call 211 (dial 2-1-1) to find local help resources, or contact a legal aid organization."),
    ],
    "resources": ["211 (dial 2-1-1)", "LawHelp.org — free legal help"],
    "deadline_note": "⚠️ Check the document for any response deadlines.",
    "phone_script_key": None,
}


def get_action_plan(doc_type, modes=None):
    plan = ACTION_PLANS.get(doc_type, DEFAULT_PLAN)
    steps = plan["steps"]
    resources = plan["resources"]

    # Adjust for special modes
    modes = modes or []
    if "senior" in modes:
        resources = resources + [
            "SHIP (free Medicare counseling): shiphelp.org",
            "Eldercare Locator: 1-800-677-1116",
            "BenefitsCheckUp: benefitscheckup.org",
        ]
    if "immigrant" in modes:
        resources = resources + [
            "Immigration Advocates Network: immigrationadvocates.org",
            "Local community organizations for immigrants",
        ]
    if "caregiver" in modes:
        resources = resources + [
            "Caregiver Action Network: 1-855-227-3640",
            "Eldercare Locator: 1-800-677-1116",
        ]
    if "crisis" in modes:
        # In crisis: put emergency resources FIRST
        resources = ["211 (dial 2-1-1) — Emergency help NOW"] + resources

    return {
        "title": plan["title"],
        "steps": steps,
        "resources": list(dict.fromkeys(resources))[:8],
        "deadline_note": plan.get("deadline_note"),
        "phone_script_key": plan.get("phone_script_key"),
    }


def format_action_plan(plan, crisis=False):
    lines = []
    lines.append("─" * 50)
    lines.append("WHAT TO DO NEXT")
    lines.append("─" * 50)
    lines.append("")

    if crisis:
        lines.append("⚠️  This situation needs attention TODAY.")
        lines.append("")

    for i, (title, detail) in enumerate(plan["steps"], 1):
        lines.append(f"{i}. {title}")
        lines.append(f"   → {detail}")
        lines.append("")

    if plan.get("deadline_note"):
        lines.append("")
        lines.append(plan["deadline_note"])
        lines.append("")

    if plan["resources"]:
        lines.append("─" * 50)
        lines.append("🆘 WHERE TO GET MORE HELP")
        lines.append("─" * 50)
        for r in plan["resources"]:
            lines.append(f"• {r}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate action plan for document type")
    parser.add_argument("--doc-type", help="Document type code (e.g. HSG-03)")
    parser.add_argument("--modes", nargs="*", default=[], help="Special modes: senior immigrant caregiver crisis")
    parser.add_argument("--classification", help="Path to classification JSON from classify_document.py")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.classification:
        with open(args.classification) as f:
            data = json.load(f)
        doc_type = data.get("document_type", "UNKNOWN")
        modes = data.get("special_modes", [])
        crisis = data.get("urgency_code") == "RED"
    else:
        doc_type = args.doc_type or "UNKNOWN"
        modes = args.modes
        crisis = "crisis" in modes

    plan = get_action_plan(doc_type, modes)

    if args.json:
        print(json.dumps(plan, indent=2))
    else:
        print(format_action_plan(plan, crisis))


if __name__ == "__main__":
    main()
