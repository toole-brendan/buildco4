"""
Shared utilities for bottom-up TAM analysis.
Vendor normalizer, description regex, dedup, JSON helpers.
"""

import re
import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Master description regex (Step 0C)
# ---------------------------------------------------------------------------

SHIP_WORK_PATTERN = re.compile(
    r"\b("
    # Availability types (Bucket 1)
    r"DSRA|EDSRA|DOCKING SELECTED RESTRICTED|"
    r"DMP|DEPOT MODERNIZATION PERIOD|"
    r"SRA|SELECTED RESTRICTED AVAILABILITY|"
    r"D?PIA|PLANNED INCREMENTAL AVAILABILITY|"
    r"D?PMA|PHASED MAINTENANCE AVAILABILITY|"
    r"EDPMA|CIA|"
    # Continuous/emergent (Bucket 2)
    r"CMAV|CONTINUOUS MAINTENANCE|"
    r"ERATA|EMERGENT REPAIR|ORATA|VOYAGE REPAIR|"
    # Modernization (Bucket 3)
    r"SHIPALT|ORDALT|MACHALT|ALTERATION INSTALLATION|"
    r"BACKFIT|RETROFIT|TECH INSERTION|"
    r"DDG.?MOD|LCS.?MOD|IN.?SERVICE MODERNIZATION|"
    r"SEWIP|CANES|AN.SQQ.89|AN.SLQ.32|"
    # Major life-cycle (Bucket 4)
    r"RCOH|REFUELING.{0,10}OVERHAUL|"
    r"EOH|ENGINEERED OVERHAUL|"
    r"SLEP|SERVICE LIFE EXTENSION|"
    r"MMA|MAJOR MAINTENANCE AVAILABILITY|"
    # Sustainment (Bucket 5)
    r"LIFECYCLE SUPPORT|LIFE CYCLE|DMSMS|OBSOLESCENCE|"
    r"SETA|SUPSHIP|SHIP MAINTENANCE IMPROVEMENT|"
    # Support (Bucket 6)
    r"HUSBANDING|SHORE POWER|DRYDOCK SERVICE|"
    r"SCAFFOLDING|CRANE SERVICE|"
    # General ship repair
    r"SHIP REPAIR|VESSEL REPAIR|SHIP MAINTENANCE|"
    r"AVAILABILIT(?:Y|IES)"
    r")\b",
    re.IGNORECASE,
)


def matches_ship_work(description: str) -> bool:
    if not description:
        return False
    return bool(SHIP_WORK_PATTERN.search(description))


# ---------------------------------------------------------------------------
# Vendor name normalizer
# ---------------------------------------------------------------------------

_SUFFIX_RE = re.compile(
    r",?\s*\b(INC|LLC|CORP|CORPORATION|CO|LTD|LP|L\.?P\.?|LLP|"
    r"INCORPORATED|LIMITED|COMPANY)\b\.?",
    re.IGNORECASE,
)

VENDOR_ALIASES = {
    "METRO MACHINE": "HII",
    "METRO MACHINE CORP": "HII",
    "HUNTINGTON INGALLS INDUSTRIES": "HII",
    "VIGOR MARINE": "VIGOR",
    "VIGOR INDUSTRIAL": "VIGOR",
    "VIGOR WORKS": "VIGOR",
    "GENERAL DYNAMICS NASSCO": "GD NASSCO",
    "NASSCO": "GD NASSCO",
    "NATIONAL STEEL AND SHIPBUILDING": "GD NASSCO",
    "GENERAL DYNAMICS BATH IRON WORKS": "GD BIW",
    "BATH IRON WORKS": "GD BIW",
    "GENERAL DYNAMICS ELECTRIC BOAT": "GD EB",
    "ELECTRIC BOAT": "GD EB",
    "BAE SYSTEMS NORFOLK SHIP REPAIR": "BAE SYSTEMS",
    "BAE SYSTEMS SAN DIEGO SHIP REPAIR": "BAE SYSTEMS",
    "BAE SYSTEMS HAWAII SHIPYARD": "BAE SYSTEMS",
    "BAE SYSTEMS JACKSONVILLE SHIP REPAIR": "BAE SYSTEMS",
    "BAE SYSTEMS SOUTHEAST SHIPYARDS": "BAE SYSTEMS",
    "COLONNAS SHIPYARD": "COLONNA",
    "COLONNA'S SHIPYARD": "COLONNA",
}


def normalize_vendor(name: str) -> str:
    if not name:
        return ""
    n = name.strip().upper()
    n = _SUFFIX_RE.sub("", n).strip().rstrip(",. ")
    for alias, canonical in VENDOR_ALIASES.items():
        if alias in n:
            return canonical
    return n


# ---------------------------------------------------------------------------
# JSON file helpers — append-friendly
# ---------------------------------------------------------------------------

def append_records_to_json(filepath: str, records: list[dict]):
    """Append records to a JSON array file. Creates if doesn't exist."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if path.exists() and path.stat().st_size > 0:
        with open(path, "r") as f:
            existing = json.load(f)
    existing.extend(records)
    with open(path, "w") as f:
        json.dump(existing, f, indent=2, default=str)


def load_json_records(filepath: str) -> list[dict]:
    path = Path(filepath)
    if not path.exists() or path.stat().st_size == 0:
        return []
    with open(path, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Fiscal year helpers
# ---------------------------------------------------------------------------

def fy_date_range(fy: int) -> tuple[str, str]:
    """Return (start, end) date strings for a fiscal year in FPDS format."""
    return (f"{fy - 1}/10/01", f"{fy}/09/30")


def fy_date_range_iso(fy: int) -> tuple[str, str]:
    """Return (start, end) in ISO format for USAspending."""
    return (f"{fy - 1}-10-01", f"{fy}-09-30")
