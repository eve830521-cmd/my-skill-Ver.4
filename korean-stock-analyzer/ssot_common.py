"""
Shared helpers for the Korean Stock Analyzer pipeline.

1) Path configuration  - every default equals the previously hard-coded value, so behaviour is
   unchanged unless an environment variable overrides it (portable across PCs / drives).
       KSA_STOCK_RESEARCH_ROOT : folder that holds one sub-folder per company
       KSA_MY_LIST_ROOT        : folder with my-list/cache.db and */Data.xlsx
       KSA_S_CURVE_REGISTRY    : path to korean cycle s_curve_registry.json
2) Warning registry     - replaces silent `except: pass`. Warnings are written into
   valuation_metrics.json -> "data_quality" so degraded runs are never invisible.
"""
import os
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent
_WORKSPACE = _SKILL_DIR.parent  # ...\my-skill

STOCK_RESEARCH_ROOT = os.environ.get(
    "KSA_STOCK_RESEARCH_ROOT", str(_WORKSPACE / "Stock_Research")
)
MY_LIST_ROOT = os.environ.get(
    "KSA_MY_LIST_ROOT", r"e:\antigravity-work\my-stock\my-list"
)
S_CURVE_REGISTRY_PATH = os.environ.get(
    "KSA_S_CURVE_REGISTRY",
    r"e:\antigravity-work\korean cycle\00_megatrend\docs\s_curve_registry.json",
)
REPORT_CSS_PATH = os.environ.get(
    "KSA_REPORT_CSS", str(_SKILL_DIR / "report_style.css")
)

_WARNINGS = []


def record_warning(stage, detail, severity="warn"):
    """Record a non-fatal problem. severity: 'warn' (informational) | 'degraded' (numbers may be affected)."""
    entry = {"stage": str(stage), "severity": severity, "detail": str(detail)}
    if entry not in _WARNINGS:
        _WARNINGS.append(entry)
    print(f"  [WARN:{severity}] {stage}: {detail}")


def get_warnings():
    return list(_WARNINGS)


def reset_warnings():
    _WARNINGS.clear()


def data_quality_summary():
    """Compact block stored in valuation_metrics.json."""
    status = "degraded" if any(w["severity"] == "degraded" for w in _WARNINGS) else (
        "warn" if _WARNINGS else "ok"
    )
    return {"status": status, "warnings": get_warnings()}
