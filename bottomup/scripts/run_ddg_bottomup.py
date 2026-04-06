#!/usr/bin/env python3
"""
DDG (Destroyer) Bottom-Up Analysis
Pulls DDG contract award data from USAspending API and produces ddg_bottomup.csv.

Keyword groups searched:
  DDG 51, DDG-51, Arleigh Burke, DDG 1000, DDG-1000, Zumwalt, DDG(X), DDGX,
  destroyer (with Navy agency filter)

Award type code groups (separate API calls per group):
  Contracts: A/B/C/D
  IDVs: IDV_A through IDV_E
  Grants: 02-05
  Other: 06-11, -1

Post-filters with DDG-specific regex, deduplicates by Award ID, and writes CSV.
Also runs spending_over_time for FY-level trend data.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import logging
from pathlib import Path

# Allow imports from the scripts directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from usaspending_client import spending_by_award, spending_over_time_keywords

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_CSV = Path(__file__).parent.parent / "ddg_bottomup.csv"
SUMMARY_CSV = Path(__file__).parent.parent / "ddg_spending_over_time.csv"

FY_START = 2017
FY_END = 2026
MAX_PAGES = 10
RECORDS_PER_PAGE = 100
CALL_DELAY = 0.5  # seconds between API calls

# Keyword groups — each is a separate API call
KEYWORD_GROUPS = [
    {"keywords": ["DDG 51"], "label": "DDG_51"},
    {"keywords": ["DDG-51"], "label": "DDG-51"},
    {"keywords": ["Arleigh Burke"], "label": "Arleigh_Burke"},
    {"keywords": ["DDG 1000"], "label": "DDG_1000"},
    {"keywords": ["DDG-1000"], "label": "DDG-1000"},
    {"keywords": ["Zumwalt"], "label": "Zumwalt"},
    {"keywords": ["DDG(X)"], "label": "DDGX_paren"},
    {"keywords": ["DDGX"], "label": "DDGX"},
    {"keywords": ["destroyer"], "label": "destroyer_navy", "agency": True},
]

# Award type code groups — cannot mix across groups
AWARD_TYPE_GROUPS = {
    "contracts": ["A", "B", "C", "D"],
    "idvs": ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"],
    "grants": ["02", "03", "04", "05"],
    "other": ["06", "07", "08", "09", "10", "11", "-1"],
}

# Navy agency filter for the "destroyer" keyword
NAVY_AGENCY_FILTER = "Department of the Navy"

# ---------------------------------------------------------------------------
# DDG post-filter regex
# ---------------------------------------------------------------------------

DDG_FILTER_PATTERN = re.compile(
    r"\b("
    r"DDG"                              # DDG (covers DDG-51, DDG 51, DDG-1000, DDG(X), DDGX)
    r"|ARLEIGH\s*BURKE"                 # Arleigh Burke class
    r"|ZUMWALT"                         # Zumwalt class
    r"|DESTROYER\s*(CLASS|PROGRAM|SHIP|VESSEL|ESCORT|SQUADRON|MODERNIZATION|CONSTRUCTION|COMBAT)"
    r"|GUIDED\s*MISSILE\s*DESTROYER"    # Guided Missile Destroyer
    r"|NAVAL\s*DESTROYER"               # Naval destroyer
    r")\b",
    re.IGNORECASE,
)


def passes_ddg_filter(description: str | None) -> bool:
    """Return True if description matches DDG-related terms."""
    if not description:
        return False
    return bool(DDG_FILTER_PATTERN.search(description))


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def pull_ddg_awards() -> list[dict]:
    """Pull all DDG awards from USAspending, across all keyword and award type groups."""
    all_records = []
    call_count = 0

    total_calls = len(KEYWORD_GROUPS) * len(AWARD_TYPE_GROUPS)
    print(f"=== DDG Bottom-Up: {total_calls} API query batches ({len(KEYWORD_GROUPS)} keyword groups x {len(AWARD_TYPE_GROUPS)} award type groups) ===")
    print(f"=== FY{FY_START}-FY{FY_END}, up to {MAX_PAGES} pages per query ===\n")

    for kg in KEYWORD_GROUPS:
        keywords = kg["keywords"]
        label = kg["label"]
        use_agency = kg.get("agency", False)
        agency_id = NAVY_AGENCY_FILTER if use_agency else None

        for atg_name, atg_codes in AWARD_TYPE_GROUPS.items():
            batch_label = f"{label}_{atg_name}"
            call_count += 1
            print(f"[{call_count}/{total_calls}] Querying: keywords={keywords}, award_types={atg_name}, agency={'Navy' if use_agency else 'any'}")

            try:
                records = spending_by_award(
                    keywords=keywords,
                    agency_id=agency_id,
                    fy_start=FY_START,
                    fy_end=FY_END,
                    award_type_codes=atg_codes,
                    limit=RECORDS_PER_PAGE,
                    max_pages=MAX_PAGES,
                    query_batch=batch_label,
                )
                print(f"         -> {len(records)} records returned")
                all_records.extend(records)
            except Exception as e:
                log.error(f"  ERROR on {batch_label}: {e}")
                print(f"         -> ERROR: {e}")

            time.sleep(CALL_DELAY)

    print(f"\n=== Total raw records: {len(all_records)} ===")
    return all_records


def apply_filter_and_dedup(records: list[dict]) -> list[dict]:
    """Apply DDG regex post-filter and deduplicate by Award ID."""
    # Tag each record with filter result
    for r in records:
        r["passed_filter"] = passes_ddg_filter(r.get("description"))

    # Keep only records that pass the filter
    filtered = [r for r in records if r["passed_filter"]]
    print(f"=== After DDG post-filter: {len(filtered)} records (from {len(records)} raw) ===")

    # Deduplicate by award_id — keep the first occurrence (highest award_amount due to sort)
    seen = set()
    deduped = []
    for r in filtered:
        aid = r.get("award_id")
        if aid and aid not in seen:
            seen.add(aid)
            deduped.append(r)

    print(f"=== After dedup by Award ID: {len(deduped)} unique awards ===")
    return deduped


def write_csv(records: list[dict], output_path: Path):
    """Write records to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "award_id", "vendor_name", "description", "award_amount",
        "total_outlays", "contract_award_type", "start_date", "end_date",
        "awarding_agency", "awarding_sub_agency", "naics_code", "psc_code",
        "query_batch", "passed_filter",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r)

    print(f"=== Wrote {len(records)} records to {output_path} ===")


def pull_spending_over_time_trends():
    """Run spending_over_time with DDG keywords for FY-level trend data."""
    print("\n=== Pulling spending_over_time FY trends ===")

    keywords = ["DDG 51", "DDG-51", "Arleigh Burke", "DDG 1000", "DDG(X)", "destroyer"]

    # Only contracts for spending_over_time (most meaningful)
    try:
        results = spending_over_time_keywords(
            keywords=keywords,
            fy_start=FY_START,
            fy_end=FY_END,
            award_type_codes=["A", "B", "C", "D"],
        )
        print(f"=== spending_over_time returned {len(results)} fiscal year rows ===")

        if results:
            SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
            with open(SUMMARY_CSV, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["fiscal_year", "aggregated_amount"])
                writer.writeheader()
                for r in results:
                    writer.writerow(r)
            print(f"=== Wrote spending_over_time summary to {SUMMARY_CSV} ===")

            # Print summary table
            print("\nFY-Level DDG Spending (Contracts):")
            print(f"{'FY':<8} {'Obligated':>20}")
            print("-" * 30)
            for r in sorted(results, key=lambda x: x.get("fiscal_year", 0)):
                fy = r.get("fiscal_year", "?")
                amt = r.get("aggregated_amount", 0) or 0
                print(f"FY{fy:<6} ${amt:>18,.0f}")

    except Exception as e:
        log.error(f"spending_over_time failed: {e}")
        print(f"ERROR in spending_over_time: {e}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("DDG (Destroyer) Bottom-Up — USAspending Award Pull")
    print("=" * 70)

    # Step 1: Pull awards
    raw_records = pull_ddg_awards()

    # Step 2: Filter and deduplicate
    final_records = apply_filter_and_dedup(raw_records)

    # Step 3: Write CSV
    write_csv(final_records, OUTPUT_CSV)

    # Step 4: Spending over time trends
    pull_spending_over_time_trends()

    print("\n=== DDG Bottom-Up complete ===")
