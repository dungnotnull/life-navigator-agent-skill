# Scripts Reference — Life Navigator Agent

## Script Index

| Script | Purpose | Phase |
|---|---|---|
| `utils.py` | Shared utilities | All |
| `classify_document.py` | Classify document type + urgency + modes | Phase 1 |
| `plain_language.py` | Rewrite complex text in plain English | Phase 2 |
| `action_plan.py` | Generate numbered action plan by document type | Phase 3 |
| `assemble_response.py` | Bundle all outputs into final response | Final |

## Full Pipeline

```bash
# Step 1 — Classify
python scripts/classify_document.py \
  --text "Pay or Quit Notice: You must pay $1,200 or vacate within 3 days..." \
  --json > /tmp/lna/classification.json

# Step 2 — Plain language
python scripts/plain_language.py \
  --text "Pay or Quit Notice: You must pay $1,200 or vacate within 3 days..." \
  --doc-name "Pay or Quit Notice" \
  --json > /tmp/lna/plain_summary.json

# Step 3 — Action plan
python scripts/action_plan.py \
  --classification /tmp/lna/classification.json \
  --json > /tmp/lna/action_plan.json

# Step 4 — Assemble
python scripts/assemble_response.py \
  --classification /tmp/lna/classification.json \
  --plain-summary /tmp/lna/plain_summary.json \
  --action-plan /tmp/lna/action_plan.json \
  --output /tmp/lna/response.md
```

## Individual Script Usage

```bash
# Just classify a document
python scripts/classify_document.py --text "Your EOB from Aetna..."

# Just get plain language summary
python scripts/plain_language.py --file letter.txt

# Just get action plan for a known document type
python scripts/action_plan.py --doc-type HSG-03 --modes crisis

# Scam check
python scripts/classify_document.py --text "Call immediately or be arrested..." --json | python -c "import json,sys; d=json.load(sys.stdin); print('SCAM' if d['potential_scam'] else 'Likely legitimate')"
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LNA_WORKSPACE` | `/tmp/lna` | Working directory for intermediate files |
