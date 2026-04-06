#!/usr/bin/env python3
"""
Silver Layer: Post-filter, deduplicate, classify, and normalize all Bronze data.
Produces silver_canonical.csv and silver_summary.md.
"""
from __future__ import annotations

import json
import os
import re
import sys
import csv
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared_utils import (
    SHIP_WORK_PATTERN,
    matches_ship_work,
    normalize_vendor,
    load_json_records,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRONZE_FPDS_DIR = Path(__file__).parent.parent / "bronze" / "fpds"
BRONZE_USA_DIR = Path(__file__).parent.parent / "bronze" / "usaspending"
SILVER_DIR = Path(__file__).parent.parent / "silver"
SILVER_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Bucket classification patterns
# ---------------------------------------------------------------------------

# Priority 1: Description-based classification (high confidence)
BUCKET_PATTERNS = [
    # Bucket 4: Major life-cycle events (check FIRST — RCOH/SLEP are specific)
    (4, "High", re.compile(
        r"\b(RCOH|REFUELING.{0,10}OVERHAUL|ERO|EOH|ENGINEERED OVERHAUL|"
        r"SLEP|SERVICE LIFE EXTENSION|"
        r"MMA|MAJOR MAINTENANCE AVAILABILITY|"
        r"MIDLIFE)\b", re.IGNORECASE),
     "description keyword (Bucket 4: major life-cycle)"),

    # Bucket 2: Continuous/emergent (check before Bucket 1 — CMAV is specific)
    (2, "High", re.compile(
        r"\b(CMAV|CONTINUOUS MAINTENANCE AVAILABILITY|"
        r"ERATA|EMERGENT REPAIR|EMERGENT MAINTENANCE|"
        r"ORATA|VOYAGE REPAIR|CASUALTY REPAIR|CASREP|"
        r"CONTINUOUS MAINTENANCE)\b", re.IGNORECASE),
     "description keyword (Bucket 2: continuous/emergent)"),

    # Bucket 1: Scheduled depot (the big bucket)
    (1, "High", re.compile(
        r"\b(DSRA|EDSRA|DOCKING SELECTED RESTRICTED|"
        r"DMP|DEPOT MODERNIZATION|MODPRD|"
        r"SRA|SELECTED RESTRICTED AVAILABILITY|"
        r"D?PIA|PLANNED INCREMENTAL AVAILABILITY|"
        r"D?PMA|PHASED MAINTENANCE AVAILABILITY|"
        r"EDPMA|CIA|CARRIER INCREMENTAL|"
        r"PSA|POST SHAKEDOWN)\b", re.IGNORECASE),
     "description keyword (Bucket 1: scheduled depot availability)"),

    # Bucket 3: Modernization & alteration installation
    (3, "High", re.compile(
        r"\b(SHIPALT|ORDALT|MACHALT|SPALT|"
        r"ALTERATION INSTALLATION|TECH INSERTION|TECH REFRESH|"
        r"BACKFIT|RETROFIT|"
        r"DDG.?MOD|LCS.?MOD|IN.?SERVICE MODERNIZATION|"
        r"SEWIP|CANES|AN.SQQ.89|AN.SLQ.32|"
        r"CAPABILITY INSERTION|OBJECTIVE CONFIGURATION|"
        r"ADVANCED CAPABILITY BUILD|"
        r"COMBAT SYSTEM.{0,10}UPGRADE)\b", re.IGNORECASE),
     "description keyword (Bucket 3: modernization/alteration)"),

    # Bucket 5: Sustainment engineering/planning
    (5, "High", re.compile(
        r"\b(SETA|SUPSHIP|SHIP MAINTENANCE IMPROVEMENT|"
        r"LIFECYCLE SUPPORT|LIFE CYCLE SUPPORT|"
        r"PLANNING AND TECHNICAL|"
        r"DMSMS|OBSOLESCENCE MANAGEMENT|"
        r"CONFIGURATION MANAGEMENT|CLASS MAINTENANCE PLAN|"
        r"ENGINEERING.{0,10}TECHNICAL.{0,10}SUPPORT)\b", re.IGNORECASE),
     "description keyword (Bucket 5: sustainment engineering)"),

    # Bucket 6: Availability support/port services
    (6, "High", re.compile(
        r"\b(HUSBANDING|SHORE POWER|"
        r"BERTHING.{0,5}MESSING|"
        r"DRYDOCK SERVICE|DRY DOCK SERVICE|"
        r"SCAFFOLDING|CRANE SERVICE|"
        r"TUG SERVICE|PILOT SERVICE|"
        r"FORCE PROTECTION.{0,10}AVAIL|"
        r"PORT SERVICE)\b", re.IGNORECASE),
     "description keyword (Bucket 6: availability support)"),
]

# Priority 2: PSC-based default bucket (medium confidence)
PSC_DEFAULT_BUCKET = {
    "J998": (1, "Medium", "PSC J998 default (ship repair)"),
    "J999": (1, "Medium", "PSC J999 default (ship repair NEC)"),
    "J019": (1, "Medium", "PSC J019 default (equipment maintenance)"),
    "J020": (1, "Medium", "PSC J020 default (equipment repair)"),
    "K019": (3, "Medium", "PSC K019 default (modification of equipment)"),
    "K020": (3, "Medium", "PSC K020 default (modification of equipment)"),
    "N019": (3, "Medium", "PSC N019 default (installation of equipment)"),
    "N020": (3, "Medium", "PSC N020 default (installation of equipment)"),
    "R425": (5, "Medium", "PSC R425 default (engineering/technical)"),
    "R408": (5, "Medium", "PSC R408 default (program management/support)"),
    "L019": (5, "Medium", "PSC L019 default (technical representative)"),
    "L020": (5, "Medium", "PSC L020 default (technical representative)"),
}


def classify_bucket(record: dict) -> tuple[int | None, int | None, str, str]:
    """
    Classify a record into one of the 6 buckets.
    Returns (primary_bucket, secondary_bucket, confidence, reason).
    """
    desc = (record.get("description") or "").upper()
    psc = (record.get("psc_code") or "").upper().strip()

    # Priority 1: Description keywords
    for bucket, confidence, pattern, reason in BUCKET_PATTERNS:
        if pattern.search(desc):
            # Check for secondary bucket (blended contracts)
            secondary = None
            # DMP contracts blend maintenance (B1) + modernization (B3)
            if bucket == 1 and re.search(r"\b(DMP|DEPOT MODERNIZATION|MODPRD)\b", desc, re.IGNORECASE):
                secondary = 3
            # Large depot avails often include mod work
            elif bucket == 1 and re.search(r"\b(MODERNIZATION|ALTERATION|UPGRADE)\b", desc, re.IGNORECASE):
                secondary = 3
            return bucket, secondary, confidence, reason

    # Priority 2: PSC-based default
    if psc in PSC_DEFAULT_BUCKET:
        bucket, confidence, reason = PSC_DEFAULT_BUCKET[psc]
        # Check description for secondary signals
        secondary = None
        if bucket == 1 and re.search(r"\b(MODERNIZATION|ALTERATION|UPGRADE)\b", desc, re.IGNORECASE):
            secondary = 3
        return bucket, secondary, confidence, reason

    # Priority 3: General ship work regex match → Bucket 1 default (low confidence)
    if matches_ship_work(desc):
        return 1, None, "Low", "general ship work regex match"

    # No match
    return None, None, "None", "no match"


def should_include(record: dict) -> tuple[bool, str]:
    """
    Determine if a record should be INCLUDED in the analysis.
    Returns (include: bool, reason: str).
    """
    desc = (record.get("description") or "").upper()
    psc = (record.get("psc_code") or "").upper().strip()
    query_batch = record.get("query_batch", "")

    # PSC J998/J999: auto-include (PSC is sufficient signal)
    if psc in ("J998", "J999"):
        return True, "PSC J998/J999 auto-include"

    # PSC J019/J020: include if regex matches or references ship/hull
    if psc in ("J019", "J020"):
        if matches_ship_work(desc):
            return True, f"PSC {psc} + ship work regex match"
        if re.search(r"\b(USS |USCGC |DDG|FFG|LCS|LPD|LHA|LHD|CVN|SSN|SSBN|CG |MCM|MHC)\b", desc, re.IGNORECASE):
            return True, f"PSC {psc} + hull designation in description"
        return False, f"PSC {psc} but no ship work signal in description"

    # PSC K019/N019: include if mod/install related to ships
    if psc in ("K019", "K020", "N019", "N020"):
        if matches_ship_work(desc):
            return True, f"PSC {psc} + ship work regex match"
        if re.search(r"\b(SHIP|VESSEL|HULL|USS |DDG|FFG|LCS|LPD|CVN|SSN)\b", desc, re.IGNORECASE):
            return True, f"PSC {psc} + ship reference in description"
        return False, f"PSC {psc} but no ship reference"

    # PSC R425/R408: include ONLY if regex matches (too broad otherwise)
    if psc in ("R425", "R408", "L019", "L020"):
        if matches_ship_work(desc):
            return True, f"PSC {psc} + ship work regex match"
        return False, f"PSC {psc} but no ship work signal"

    # Keyword-sourced records: include only if regex matches
    if query_batch.startswith("kw_"):
        if matches_ship_work(desc):
            return True, f"keyword query + ship work regex match"
        # RCOH/SLEP/HUSBANDING keywords are specific enough to auto-include
        if any(kw in query_batch.upper() for kw in ["RCOH", "SLEP", "HUSBANDING"]):
            return True, f"keyword query ({query_batch}) — high-specificity keyword"
        return False, f"keyword query but no ship work signal"

    # USAspending records: include if ship work
    if record.get("source") == "USASPENDING":
        if matches_ship_work(desc):
            return True, "USAspending + ship work regex match"
        return False, "USAspending but no ship work signal"

    # Default: include if matches ship work
    if matches_ship_work(desc):
        return True, "general ship work regex match"
    return False, "no qualifying signal"


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def dedup_fpds_records(records: list[dict]) -> list[dict]:
    """
    Deduplicate FPDS records: keep latest mod per PIID.
    NEVER sum totals across mods.
    """
    by_piid = {}
    for r in records:
        piid = r.get("piid")
        if not piid:
            continue
        mod = r.get("mod_number", "0") or "0"
        key = piid
        if key not in by_piid or _mod_sort_key(mod) > _mod_sort_key(by_piid[key].get("mod_number", "0") or "0"):
            by_piid[key] = r
    return list(by_piid.values())


def _mod_sort_key(mod: str) -> tuple:
    """Sort mod numbers: numeric mods > alpha mods > '0'."""
    if not mod:
        return (0, 0, "")
    try:
        return (1, int(mod), "")
    except ValueError:
        return (0, 0, mod)


def dedup_usaspending_records(records: list[dict]) -> list[dict]:
    """Deduplicate USAspending records by award_id."""
    seen = {}
    for r in records:
        aid = r.get("award_id")
        if aid and aid not in seen:
            seen[aid] = r
    return list(seen.values())


# ---------------------------------------------------------------------------
# Main Silver processing
# ---------------------------------------------------------------------------

def load_all_fpds_bronze() -> list[dict]:
    """Load all FPDS Bronze JSON files."""
    records = []
    if not BRONZE_FPDS_DIR.exists():
        return records
    for f in sorted(BRONZE_FPDS_DIR.glob("*.json")):
        if f.name.startswith("_"):
            continue
        data = load_json_records(str(f))
        log.info(f"  Loaded {len(data):,} records from {f.name}")
        records.extend(data)
    return records


def load_all_usaspending_bronze() -> list[dict]:
    """Load USAspending award-level Bronze JSON files (spending_by_award output)."""
    records = []
    if not BRONZE_USA_DIR.exists():
        return records
    for f in sorted(BRONZE_USA_DIR.glob("awards_*.json")):
        data = load_json_records(str(f))
        log.info(f"  Loaded {len(data):,} records from {f.name}")
        records.extend(data)
    return records


def process_silver():
    log.info("=" * 60)
    log.info("SILVER LAYER: Post-filter, Deduplicate, Classify")
    log.info("=" * 60)

    # Step 1: Load all Bronze data
    log.info("\nStep 1: Loading Bronze data...")
    fpds_raw = load_all_fpds_bronze()
    usa_raw = load_all_usaspending_bronze()
    log.info(f"  FPDS raw: {len(fpds_raw):,} records")
    log.info(f"  USAspending raw: {len(usa_raw):,} records")

    # Step 2: Deduplicate
    log.info("\nStep 2: Deduplicating...")
    fpds_deduped = dedup_fpds_records(fpds_raw)
    usa_deduped = dedup_usaspending_records(usa_raw)
    log.info(f"  FPDS after dedup: {len(fpds_deduped):,} (removed {len(fpds_raw) - len(fpds_deduped):,} dups)")
    log.info(f"  USAspending after dedup: {len(usa_deduped):,} (removed {len(usa_raw) - len(usa_deduped):,} dups)")

    # Step 3: Post-filter and classify each record
    log.info("\nStep 3: Filtering and classifying...")
    silver_records = []

    for r in fpds_deduped:
        include, include_reason = should_include(r)
        bucket_primary, bucket_secondary, confidence, class_reason = classify_bucket(r)

        silver_rec = {
            **r,
            "disposition": "INCLUDE" if include else "EXCLUDE",
            "include_reason": include_reason,
            "bucket_primary": bucket_primary,
            "bucket_secondary": bucket_secondary,
            "confidence": confidence,
            "classification_reason": class_reason,
            "vendor_normalized": normalize_vendor(r.get("vendor_name", "")),
        }
        silver_records.append(silver_rec)

    for r in usa_deduped:
        include, include_reason = should_include(r)
        bucket_primary, bucket_secondary, confidence, class_reason = classify_bucket(r)

        silver_rec = {
            "source": "USASPENDING",
            "piid": r.get("award_id"),
            "mod_number": None,
            "parent_idv_piid": None,
            "vendor_name": r.get("vendor_name"),
            "vendor_uei": None,
            "description": r.get("description"),
            "psc_code": r.get("psc_code"),
            "psc_description": None,
            "naics_code": r.get("naics_code"),
            "naics_description": None,
            "obligated_amount": None,
            "total_obligated": r.get("award_amount"),
            "base_exercised_options": None,
            "base_all_options": None,
            "contract_action_type": None,
            "contract_action_desc": r.get("contract_award_type"),
            "contract_pricing_type": None,
            "contract_pricing_desc": None,
            "extent_competed": None,
            "extent_competed_desc": None,
            "signed_date": r.get("start_date"),
            "effective_date": r.get("start_date"),
            "completion_date": r.get("end_date"),
            "ultimate_completion_date": None,
            "fiscal_year": None,
            "contracting_agency_id": None,
            "contracting_agency_name": r.get("awarding_sub_agency"),
            "contracting_office_name": None,
            "funding_agency_name": r.get("awarding_agency"),
            "funding_office_name": None,
            "record_type": "usaspending_award",
            "ot_agreement_type": None,
            "query_batch": r.get("query_batch"),
            "disposition": "INCLUDE" if include else "EXCLUDE",
            "include_reason": include_reason,
            "bucket_primary": bucket_primary,
            "bucket_secondary": bucket_secondary,
            "confidence": confidence,
            "classification_reason": class_reason,
            "vendor_normalized": normalize_vendor(r.get("vendor_name", "")),
        }
        silver_records.append(silver_rec)

    # Step 4: Write CSV
    log.info("\nStep 4: Writing silver_canonical.csv...")
    included = [r for r in silver_records if r["disposition"] == "INCLUDE"]
    excluded = [r for r in silver_records if r["disposition"] == "EXCLUDE"]
    log.info(f"  INCLUDE: {len(included):,} | EXCLUDE: {len(excluded):,}")

    csv_path = SILVER_DIR / "silver_canonical.csv"
    if silver_records:
        fieldnames = list(silver_records[0].keys())
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(silver_records)
        log.info(f"  Written to {csv_path}")

    # Step 5: Generate summary
    log.info("\nStep 5: Generating silver_summary.md...")
    generate_silver_summary(silver_records, included, excluded)

    return silver_records


def generate_silver_summary(all_records, included, excluded):
    summary_path = SILVER_DIR / "silver_summary.md"

    # Count by bucket
    bucket_counts = Counter(r["bucket_primary"] for r in included if r["bucket_primary"])
    bucket_names = {
        1: "Scheduled Depot Maintenance & Repair",
        2: "Continuous / Intermediate / Emergent",
        3: "Modernization & Alteration Installation",
        4: "Major Life-Cycle Events (RCOH/SLEP/MMA)",
        5: "Sustainment Engineering / Planning",
        6: "Availability Support / Port Services",
    }

    # Count by confidence
    conf_counts = Counter(r["confidence"] for r in included)

    # Count by source
    source_counts = Counter(r["source"] for r in included)

    # Count by PSC
    psc_counts = Counter(r.get("psc_code", "?") for r in included)

    # Dollar totals by bucket (using total_obligated from latest mod)
    bucket_dollars = {}
    for r in included:
        b = r.get("bucket_primary")
        if b is None:
            continue
        amt = r.get("total_obligated") or 0
        try:
            amt = float(amt)
        except (ValueError, TypeError):
            amt = 0
        bucket_dollars[b] = bucket_dollars.get(b, 0) + amt

    # Top vendors
    vendor_dollars = {}
    for r in included:
        v = r.get("vendor_normalized", "")
        if not v:
            continue
        amt = r.get("total_obligated") or 0
        try:
            amt = float(amt)
        except (ValueError, TypeError):
            amt = 0
        vendor_dollars[v] = vendor_dollars.get(v, 0) + amt
    top_vendors = sorted(vendor_dollars.items(), key=lambda x: x[1], reverse=True)[:25]

    # Contract pricing
    pricing_counts = Counter(
        r.get("contract_pricing_desc") or r.get("contract_pricing_type") or "Unknown"
        for r in included if r["source"] == "FPDS"
    )

    # Competition
    compete_counts = Counter(
        r.get("extent_competed_desc") or r.get("extent_competed") or "Unknown"
        for r in included if r["source"] == "FPDS"
    )

    lines = [
        "# Silver Layer Summary",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Disposition Summary",
        "",
        f"| Disposition | Count |",
        f"|-------------|-------|",
        f"| INCLUDE | {len(included):,} |",
        f"| EXCLUDE | {len(excluded):,} |",
        f"| Total | {len(all_records):,} |",
        "",
        "## Records by Source",
        "",
        "| Source | Count |",
        "|--------|-------|",
    ]
    for src, cnt in source_counts.most_common():
        lines.append(f"| {src} | {cnt:,} |")

    lines.extend([
        "",
        "## Records by Bucket",
        "",
        "| # | Bucket | Records | Total Obligated ($M) | Confidence Notes |",
        "|---|--------|---------|---------------------|-----------------|",
    ])
    for b in range(1, 7):
        name = bucket_names.get(b, "?")
        cnt = bucket_counts.get(b, 0)
        dollars = bucket_dollars.get(b, 0)
        lines.append(f"| {b} | {name} | {cnt:,} | ${dollars / 1e6:,.0f}M | |")

    lines.extend([
        "",
        "## Records by Confidence",
        "",
        "| Confidence | Count |",
        "|-----------|-------|",
    ])
    for conf in ["High", "Medium", "Low"]:
        lines.append(f"| {conf} | {conf_counts.get(conf, 0):,} |")

    lines.extend([
        "",
        "## Records by PSC Code (top 15)",
        "",
        "| PSC | Count |",
        "|-----|-------|",
    ])
    for psc, cnt in psc_counts.most_common(15):
        lines.append(f"| {psc} | {cnt:,} |")

    lines.extend([
        "",
        "## Top 25 Vendors (by total obligated — FPDS records)",
        "",
        "| Rank | Vendor | Total Obligated ($M) |",
        "|------|--------|---------------------|",
    ])
    for i, (v, amt) in enumerate(top_vendors, 1):
        lines.append(f"| {i} | {v} | ${amt / 1e6:,.1f}M |")

    lines.extend([
        "",
        "## Contract Pricing Type (FPDS records)",
        "",
        "| Pricing Type | Count |",
        "|-------------|-------|",
    ])
    for pt, cnt in pricing_counts.most_common(10):
        lines.append(f"| {pt} | {cnt:,} |")

    lines.extend([
        "",
        "## Competition Level (FPDS records)",
        "",
        "| Competition | Count |",
        "|------------|-------|",
    ])
    for comp, cnt in compete_counts.most_common(10):
        lines.append(f"| {comp} | {cnt:,} |")

    lines.extend([
        "",
        "## Known Classification Ambiguities",
        "",
        "- **Blended contracts**: DMP/DSRA awards bundle maintenance + modernization. ",
        "  Primary bucket = 1 (depot maintenance), secondary = 3 (modernization).",
        "- **J998/J999 auto-include**: These PSC codes are sufficient signal for ship repair,",
        "  but some records may have vague descriptions that make bucket sub-classification difficult.",
        "- **USAspending PSC gaps**: PSC is often null at award level in USAspending.",
        "  Classification relies on description keywords alone for these records.",
        "- **J999 Navy partial**: Only ~7K of estimated ~26K records were pulled (run interrupted).",
        "  This understates the bottom-up totals.",
        "",
    ])

    summary_path.write_text("\n".join(lines))
    log.info(f"  Summary written to {summary_path}")


if __name__ == "__main__":
    process_silver()
