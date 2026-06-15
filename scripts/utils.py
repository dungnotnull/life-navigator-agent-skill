#!/usr/bin/env python3
"""utils.py — Shared utilities for Life Navigator Agent scripts"""
import json, sys, os
from pathlib import Path
from datetime import datetime, timezone

LNA_VERSION = "1.0"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path, pretty=True):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2 if pretty else None, default=str)
    print(f"  → Saved: {path}", file=sys.stderr)

def save_text(text, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  → Saved: {path}", file=sys.stderr)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def now_date():
    return datetime.now().strftime("%Y-%m-%d")

def ensure_workspace(workspace=None):
    ws = workspace or os.environ.get("LNA_WORKSPACE", "/tmp/lna")
    Path(ws).mkdir(parents=True, exist_ok=True)
    return ws

URGENCY_COLORS = {
    "RED":    "🔴",
    "YELLOW": "🟡",
    "GREEN":  "🟢",
    "INFO":   "ℹ️",
}

MODE_LABELS = {
    "senior":    "👴 Senior/Elder Mode",
    "immigrant": "🌍 New Immigrant Mode",
    "caregiver": "💊 Caregiver Mode",
    "crisis":    "🚨 Crisis Mode",
}
