#!/usr/bin/env python3
"""
Option D Bronze: Hybrid approach.
  - USAspending aggregate endpoints for FY-level trends and vendor landscapes (fast)
  - Targeted FPDS pulls for description-level precision (RCOH, SLEP, HUSBANDING)
  - Remaining small-volume FPDS PSC pulls (J019, J020, K019, N019, CG)
  - Uses already-pulled J998/J999 Navy FPDS data
"""
from __future__ import annotations

import json
import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from usaspending_client import (
    spending_over_time,
    spending_over_time_keywords,
    spending_by_recipient,
    spending_by_award,
)
from fpds_client import pull_fpds
from shared_utils import load_json_records

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRONZE_DIR = Path(__file__).parent.parent / "bronze"
FPDS_DIR = BRONZE_DIR / "fpds"
USA_DIR = BRONZE_DIR / "usaspending"
FPDS_DIR.mkdir(parents=True, exist_ok=True)
USA_DIR.mkdir(parents=True, exist_ok=True)

# USAspending agency names (subtier level)
NAVY_CODE = "Department of the Navy"
DHS_CODE = "United States Coast Guard"
FY_RANGE_FPDS = "SIGNED_DATE:[2021/10/01,2026/09/30]"  # FY22-FY26


def save_json(data: any, filepath: Path, label: str):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    log.info(f"[{label}] Saved to {filepath}")


# ===================================================================
# PART 1: USAspending Aggregate Calls (fast — seconds each)
# ===================================================================

def run_usaspending_trends():
    """FY-level spending trends by PSC group — the core market sizing data."""
    log.info("\n" + "=" * 60)
    log.info("USASPENDING: Spending Trends (spending_over_time)")
    log.info("=" * 60)

    queries = [
        # Bucket 1+2: Ship repair (the big number)
        {"psc": ["J998", "J999"], "label": "J998_J999_all", "agency": None},
        {"psc": ["J998", "J999"], "label": "J998_J999_navy", "agency": NAVY_CODE},
        {"psc": ["J998", "J999"], "label": "J998_J999_dhs", "agency": DHS_CODE},
        # Bucket 1+2: Component-level repair
        {"psc": ["J019", "J020"], "label": "J019_J020_all", "agency": None},
        {"psc": ["J019", "J020"], "label": "J019_J020_navy", "agency": NAVY_CODE},
        # Bucket 3: Standalone mod/install
        {"psc": ["K019", "K020"], "label": "K019_K020_all", "agency": None},
        {"psc": ["N019", "N020"], "label": "N019_N020_all", "agency": None},
        # Bucket 5: Engineering/technical (noisy — needs context)
        {"psc": ["R425", "R408"], "label": "R425_R408_navy", "agency": NAVY_CODE},
    ]

    results = {}
    for q in queries:
        label = q["label"]
        log.info(f"  Querying spending_over_time: {label}")
        try:
            data = spending_over_time(
                psc_codes=q["psc"],
                agency_id=q["agency"],
                fy_start=2017,
                fy_end=2026,
            )
            results[label] = data
            save_json(data, USA_DIR / f"trend_{label}.json", label)
            time.sleep(0.3)
        except Exception as e:
            log.error(f"  FAILED {label}: {e}")
            results[label] = {"error": str(e)}

    # Keyword-based trends for buckets PSC codes miss
    kw_queries = [
        {"kw": ["RCOH"], "label": "kw_RCOH_all", "agency": None},
        {"kw": ["SLEP"], "label": "kw_SLEP_all", "agency": None},
        {"kw": ["HUSBANDING"], "label": "kw_HUSBANDING_navy", "agency": NAVY_CODE},
        {"kw": ["CMAV"], "label": "kw_CMAV_navy", "agency": NAVY_CODE},
    ]

    for q in kw_queries:
        label = q["label"]
        log.info(f"  Querying spending_over_time (keyword): {label}")
        try:
            data = spending_over_time_keywords(
                keywords=q["kw"],
                agency_id=q["agency"],
                fy_start=2017,
                fy_end=2026,
            )
            results[label] = data
            save_json(data, USA_DIR / f"trend_{label}.json", label)
            time.sleep(0.3)
        except Exception as e:
            log.error(f"  FAILED {label}: {e}")
            results[label] = {"error": str(e)}

    return results


def run_usaspending_vendors():
    """Top vendors by PSC group — vendor landscape data."""
    log.info("\n" + "=" * 60)
    log.info("USASPENDING: Vendor Landscapes (spending_by_category/recipient)")
    log.info("=" * 60)

    queries = [
        # Bucket 1+2: Ship repair vendors
        {"psc": ["J998"], "label": "vendors_J998_navy_fy24", "agency": NAVY_CODE, "fy_start": 2024, "fy_end": 2024},
        {"psc": ["J998"], "label": "vendors_J998_navy_fy23", "agency": NAVY_CODE, "fy_start": 2023, "fy_end": 2023},
        {"psc": ["J998", "J999"], "label": "vendors_J998_J999_navy_fy22-26", "agency": NAVY_CODE, "fy_start": 2022, "fy_end": 2026},
        {"psc": ["J998", "J999"], "label": "vendors_J998_J999_all_fy22-26", "agency": None, "fy_start": 2022, "fy_end": 2026},
        # Bucket 1+2: Component repair vendors
        {"psc": ["J019", "J020"], "label": "vendors_J019_J020_navy_fy22-26", "agency": NAVY_CODE, "fy_start": 2022, "fy_end": 2026},
        # Bucket 3: Mod/install vendors
        {"psc": ["K019", "K020", "N019", "N020"], "label": "vendors_mod_install_navy_fy22-26", "agency": NAVY_CODE, "fy_start": 2022, "fy_end": 2026},
        # CG vendors
        {"psc": ["J998", "J999"], "label": "vendors_J998_J999_dhs_fy22-26", "agency": DHS_CODE, "fy_start": 2022, "fy_end": 2026},
    ]

    results = {}
    for q in queries:
        label = q["label"]
        log.info(f"  Querying vendor landscape: {label}")
        try:
            data = spending_by_recipient(
                psc_codes=q["psc"],
                agency_id=q["agency"],
                fy_start=q["fy_start"],
                fy_end=q["fy_end"],
                limit=50,
            )
            results[label] = data
            save_json(data, USA_DIR / f"{label}.json", label)
            time.sleep(0.3)
        except Exception as e:
            log.error(f"  FAILED {label}: {e}")
            results[label] = {"error": str(e)}

    return results


def run_usaspending_top_awards():
    """Top individual awards for detail and validation."""
    log.info("\n" + "=" * 60)
    log.info("USASPENDING: Top Awards (spending_by_award)")
    log.info("=" * 60)

    queries = [
        # Top ship repair contracts FY24
        {
            "psc": ["J998"], "kw": None, "label": "awards_J998_navy_fy24",
            "agency": NAVY_CODE, "fy_start": 2024, "fy_end": 2024, "pages": 3,
        },
        # Top ship repair contracts FY23
        {
            "psc": ["J998"], "kw": None, "label": "awards_J998_navy_fy23",
            "agency": NAVY_CODE, "fy_start": 2023, "fy_end": 2023, "pages": 3,
        },
        # RCOH awards (Bucket 4)
        {
            "psc": None, "kw": ["RCOH"], "label": "awards_RCOH_all_fy22-26",
            "agency": None, "fy_start": 2022, "fy_end": 2026, "pages": 3,
        },
        # SLEP awards (Bucket 4)
        {
            "psc": None, "kw": ["SLEP"], "label": "awards_SLEP_all_fy22-26",
            "agency": None, "fy_start": 2022, "fy_end": 2026, "pages": 3,
        },
        # CMAV awards (Bucket 2 detail)
        {
            "psc": None, "kw": ["CMAV"], "label": "awards_CMAV_navy_fy22-26",
            "agency": NAVY_CODE, "fy_start": 2022, "fy_end": 2026, "pages": 3,
        },
        # CG top awards
        {
            "psc": ["J998", "J999"], "kw": None, "label": "awards_J998_J999_dhs_fy22-26",
            "agency": DHS_CODE, "fy_start": 2022, "fy_end": 2026, "pages": 3,
        },
    ]

    results = {}
    for q in queries:
        label = q["label"]
        outfile = str(USA_DIR / f"{label}.json")
        # Skip if already pulled
        if Path(outfile).exists() and Path(outfile).stat().st_size > 100:
            log.info(f"  SKIP {label} — already exists")
            results[label] = load_json_records(outfile)
            continue

        log.info(f"  Querying top awards: {label}")
        try:
            data = spending_by_award(
                psc_codes=q["psc"],
                keywords=q["kw"],
                agency_id=q["agency"],
                fy_start=q["fy_start"],
                fy_end=q["fy_end"],
                max_pages=q["pages"],
                output_file=outfile,
                query_batch=label,
            )
            results[label] = data
            time.sleep(0.5)
        except Exception as e:
            log.error(f"  FAILED {label}: {e}")
            results[label] = {"error": str(e)}

    return results


# ===================================================================
# PART 2: Targeted FPDS Pulls (small volume, high value)
# ===================================================================

def run_fpds_targeted():
    """
    Run remaining FPDS pulls that Option D still needs:
    - Small-volume PSC pulls: J019, J020, K019, N019, CG J998, CG J999
    - Keyword pulls: RCOH, SLEP, HUSBANDING
    J998/J999 Navy are already done (17K + 7K partial).
    """
    log.info("\n" + "=" * 60)
    log.info("FPDS: Targeted Pulls (small-volume PSC + keywords)")
    log.info("=" * 60)

    queries = [
        # Remaining PSC pulls (small volume, ~15K total, ~25 min)
        {
            "query": f"PRODUCT_OR_SERVICE_CODE:J019 CONTRACTING_AGENCY_ID:1700 {FY_RANGE_FPDS}",
            "batch": "psc_J019_navy_fy22-26",
            "file": "psc_J019_navy_fy22-26.json",
        },
        {
            "query": f"PRODUCT_OR_SERVICE_CODE:J020 CONTRACTING_AGENCY_ID:1700 {FY_RANGE_FPDS}",
            "batch": "psc_J020_navy_fy22-26",
            "file": "psc_J020_navy_fy22-26.json",
        },
        {
            "query": f"PRODUCT_OR_SERVICE_CODE:K019 CONTRACTING_AGENCY_ID:1700 {FY_RANGE_FPDS}",
            "batch": "psc_K019_navy_fy22-26",
            "file": "psc_K019_navy_fy22-26.json",
        },
        {
            "query": f"PRODUCT_OR_SERVICE_CODE:N019 CONTRACTING_AGENCY_ID:1700 {FY_RANGE_FPDS}",
            "batch": "psc_N019_navy_fy22-26",
            "file": "psc_N019_navy_fy22-26.json",
        },
        # Coast Guard
        {
            "query": f"PRODUCT_OR_SERVICE_CODE:J998 CONTRACTING_AGENCY_ID:7000 {FY_RANGE_FPDS}",
            "batch": "psc_J998_cg_fy22-26",
            "file": "psc_J998_cg_fy22-26.json",
        },
        {
            "query": f"PRODUCT_OR_SERVICE_CODE:J999 CONTRACTING_AGENCY_ID:7000 {FY_RANGE_FPDS}",
            "batch": "psc_J999_cg_fy22-26",
            "file": "psc_J999_cg_fy22-26.json",
        },
        # Keyword gap-fillers (Bucket 4 + Bucket 6)
        {
            "query": f'DESCRIPTION_OF_REQUIREMENT:"RCOH" CONTRACTING_AGENCY_ID:1700 {FY_RANGE_FPDS}',
            "batch": "kw_RCOH_navy_fy22-26",
            "file": "kw_RCOH_navy_fy22-26.json",
        },
        {
            "query": f'DESCRIPTION_OF_REQUIREMENT:"SLEP" CONTRACTING_AGENCY_ID:7000 {FY_RANGE_FPDS}',
            "batch": "kw_SLEP_cg_fy22-26",
            "file": "kw_SLEP_cg_fy22-26.json",
        },
        {
            "query": f'DESCRIPTION_OF_REQUIREMENT:"HUSBANDING" CONTRACTING_AGENCY_ID:1700 {FY_RANGE_FPDS}',
            "batch": "kw_HUSBANDING_navy_fy22-26",
            "file": "kw_HUSBANDING_navy_fy22-26.json",
        },
    ]

    all_stats = []
    for i, q in enumerate(queries, 1):
        outfile = str(FPDS_DIR / q["file"])
        # Resume support
        if Path(outfile).exists() and Path(outfile).stat().st_size > 100:
            existing = load_json_records(outfile)
            log.info(f"  [{i}/{len(queries)}] SKIP {q['batch']} — already has {len(existing)} records")
            all_stats.append({"query_batch": q["batch"], "records_fetched": len(existing), "skipped": True})
            continue

        log.info(f"  [{i}/{len(queries)}] Starting {q['batch']}")
        stats = pull_fpds(query=q["query"], output_file=outfile, query_batch=q["batch"])
        all_stats.append(stats)
        time.sleep(1.0)

    return all_stats


# ===================================================================
# PART 3: Summary Generation
# ===================================================================

def generate_bronze_summary(trend_results, vendor_results, award_results, fpds_stats):
    summary_path = Path(__file__).parent.parent / "bronze" / "option_d_summary.md"

    lines = [
        "# Option D Bronze Summary",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Approach",
        "",
        "Option D (Hybrid): USAspending aggregate endpoints for FY-level trends and vendor",
        "landscapes + targeted FPDS pulls for description-level precision.",
        "",
        "---",
        "",
        "## USAspending Spending Trends",
        "",
        "### Ship Repair (J998+J999) — All Agencies",
        "",
    ]

    # Format trend data
    for label, data in trend_results.items():
        if isinstance(data, dict) and "error" in data:
            lines.append(f"**{label}**: ERROR — {data['error']}")
            lines.append("")
            continue
        if not isinstance(data, list):
            continue
        lines.append(f"### {label}")
        lines.append("")
        lines.append("| Fiscal Year | Obligations ($M) |")
        lines.append("|-------------|-----------------|")
        for row in sorted(data, key=lambda x: x.get("fiscal_year", 0)):
            fy = row.get("fiscal_year", "?")
            amt = row.get("aggregated_amount", 0)
            if amt is not None:
                lines.append(f"| FY{fy} | ${amt / 1e6:,.0f}M |")
            else:
                lines.append(f"| FY{fy} | N/A |")
        lines.append("")

    # Vendor summaries
    lines.extend(["---", "", "## Vendor Landscapes", ""])
    for label, data in vendor_results.items():
        if isinstance(data, dict) and "error" in data:
            lines.append(f"**{label}**: ERROR — {data['error']}")
            lines.append("")
            continue
        if not isinstance(data, list):
            continue
        lines.append(f"### {label}")
        lines.append("")
        lines.append("| Rank | Vendor | Amount ($M) |")
        lines.append("|------|--------|------------|")
        for i, v in enumerate(data[:20], 1):
            name = v.get("name", "?")
            amt = v.get("amount", 0)
            if amt is not None:
                lines.append(f"| {i} | {name} | ${amt / 1e6:,.1f}M |")
        lines.append("")

    # FPDS stats
    lines.extend(["---", "", "## FPDS Targeted Pulls", ""])
    lines.append("| Query | Records | Status |")
    lines.append("|-------|---------|--------|")
    # Include pre-existing J998/J999 Navy
    j998_path = FPDS_DIR / "psc_J998_navy_fy22-26.json"
    j999_path = FPDS_DIR / "psc_J999_navy_fy22-26.json"
    if j998_path.exists():
        n = len(load_json_records(str(j998_path)))
        lines.append(f"| psc_J998_navy_fy22-26 | {n:,} | Pre-existing |")
    if j999_path.exists():
        n = len(load_json_records(str(j999_path)))
        lines.append(f"| psc_J999_navy_fy22-26 | {n:,} | Pre-existing (partial) |")
    for s in fpds_stats:
        batch = s.get("query_batch", "?")
        fetched = s.get("records_fetched", 0)
        status = "Skipped (resume)" if s.get("skipped") else "Complete"
        errs = len(s.get("errors", []))
        if errs > 0:
            status += f" ({errs} errors)"
        lines.append(f"| {batch} | {fetched:,} | {status} |")

    lines.append("")
    summary_path.write_text("\n".join(lines))
    log.info(f"Summary written to {summary_path}")


# ===================================================================
# Main
# ===================================================================

def main():
    start_time = time.time()

    # Part 1: USAspending (fast — should take < 2 min total)
    trend_results = run_usaspending_trends()
    vendor_results = run_usaspending_vendors()
    award_results = run_usaspending_top_awards()

    # Part 2: Targeted FPDS pulls (slower — ~15-25 min for remaining queries)
    fpds_stats = run_fpds_targeted()

    # Part 3: Summary
    generate_bronze_summary(trend_results, vendor_results, award_results, fpds_stats)

    elapsed = time.time() - start_time
    log.info(f"\nOption D Bronze complete in {elapsed / 60:.1f} minutes.")


if __name__ == "__main__":
    main()
