#!/usr/bin/env python3
"""
Phase 1: Bronze — FPDS Pull
Runs all three strata (PSC, keyword, vendor) and writes JSON to bronze/fpds/.
Generates bronze_fpds_summary.md at the end.
"""

import json
import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Ensure script dir is on path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fpds_client import pull_fpds
from shared_utils import load_json_records, matches_ship_work

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRONZE_DIR = Path(__file__).parent.parent / "bronze" / "fpds"
BRONZE_DIR.mkdir(parents=True, exist_ok=True)

# FY range — trimmed to FY22-FY26 (4 full years + YTD)
FY_RANGE = "SIGNED_DATE:[2021/10/01,2026/09/30]"  # FY22-FY26

# ---------------------------------------------------------------------------
# STRATUM 1: PSC-based pulls (primary — captures ~90% of target data)
# ---------------------------------------------------------------------------

STRATUM1_QUERIES = [
    # Navy core PSC pulls
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:J998 CONTRACTING_AGENCY_ID:1700 {FY_RANGE}",
        "batch": "psc_J998_navy_fy22-26",
        "file": "psc_J998_navy_fy22-26.json",
    },
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:J999 CONTRACTING_AGENCY_ID:1700 {FY_RANGE}",
        "batch": "psc_J999_navy_fy22-26",
        "file": "psc_J999_navy_fy22-26.json",
    },
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:J019 CONTRACTING_AGENCY_ID:1700 {FY_RANGE}",
        "batch": "psc_J019_navy_fy22-26",
        "file": "psc_J019_navy_fy22-26.json",
    },
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:J020 CONTRACTING_AGENCY_ID:1700 {FY_RANGE}",
        "batch": "psc_J020_navy_fy22-26",
        "file": "psc_J020_navy_fy22-26.json",
    },
    # Mod/install PSCs
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:K019 CONTRACTING_AGENCY_ID:1700 {FY_RANGE}",
        "batch": "psc_K019_navy_fy22-26",
        "file": "psc_K019_navy_fy22-26.json",
    },
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:N019 CONTRACTING_AGENCY_ID:1700 {FY_RANGE}",
        "batch": "psc_N019_navy_fy22-26",
        "file": "psc_N019_navy_fy22-26.json",
    },
    # Coast Guard
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:J998 CONTRACTING_AGENCY_ID:7000 {FY_RANGE}",
        "batch": "psc_J998_cg_fy22-26",
        "file": "psc_J998_cg_fy22-26.json",
    },
    {
        "query": f"PRODUCT_OR_SERVICE_CODE:J999 CONTRACTING_AGENCY_ID:7000 {FY_RANGE}",
        "batch": "psc_J999_cg_fy22-26",
        "file": "psc_J999_cg_fy22-26.json",
    },
]

# ---------------------------------------------------------------------------
# STRATUM 2: Keyword gap-fillers (targets buckets PSC codes miss)
# ---------------------------------------------------------------------------

STRATUM2_QUERIES = [
    {
        "query": f'DESCRIPTION_OF_REQUIREMENT:"RCOH" CONTRACTING_AGENCY_ID:1700 {FY_RANGE}',
        "batch": "kw_RCOH_navy_fy22-26",
        "file": "kw_RCOH_navy_fy22-26.json",
    },
    {
        "query": f'DESCRIPTION_OF_REQUIREMENT:"SLEP" CONTRACTING_AGENCY_ID:7000 {FY_RANGE}',
        "batch": "kw_SLEP_cg_fy22-26",
        "file": "kw_SLEP_cg_fy22-26.json",
    },
    {
        "query": f'DESCRIPTION_OF_REQUIREMENT:"HUSBANDING" CONTRACTING_AGENCY_ID:1700 {FY_RANGE}',
        "batch": "kw_HUSBANDING_navy_fy22-26",
        "file": "kw_HUSBANDING_navy_fy22-26.json",
    },
]

# Stratum 3 (vendor pulls) deferred — run after Silver gap analysis if needed.

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_stratum(name: str, queries: list[dict], all_stats: list):
    log.info(f"\n{'='*60}")
    log.info(f"STRATUM: {name} ({len(queries)} queries)")
    log.info(f"{'='*60}")
    for i, q in enumerate(queries, 1):
        outfile = str(BRONZE_DIR / q["file"])
        # Skip if file already exists and has data (resume support)
        if Path(outfile).exists() and Path(outfile).stat().st_size > 100:
            existing = load_json_records(outfile)
            log.info(f"[{i}/{len(queries)}] SKIP {q['batch']} — already has {len(existing)} records")
            all_stats.append({
                "query_batch": q["batch"],
                "records_fetched": len(existing),
                "skipped": True,
            })
            continue

        log.info(f"[{i}/{len(queries)}] Starting {q['batch']}")
        stats = pull_fpds(
            query=q["query"],
            output_file=outfile,
            query_batch=q["batch"],
        )
        all_stats.append(stats)
        # Small pause between queries
        time.sleep(1.0)


def generate_summary(all_stats: list):
    """Generate bronze_fpds_summary.md from collected stats."""
    summary_path = Path(__file__).parent.parent / "bronze_fpds_summary.md"

    total_records = sum(s.get("records_fetched", 0) for s in all_stats)
    total_pages = sum(s.get("pages_fetched", 0) for s in all_stats)
    all_errors = []
    for s in all_stats:
        for e in s.get("errors", []):
            all_errors.append(f"  - [{s.get('query_batch', '?')}] {e}")

    # Categorize by stratum
    psc_stats = [s for s in all_stats if s.get("query_batch", "").startswith("psc_")]
    kw_stats = [s for s in all_stats if s.get("query_batch", "").startswith("kw_")]
    # Count record types
    rt_totals = {"award": 0, "IDV": 0, "OtherTransactionAward": 0, "OtherTransactionIDV": 0}
    for s in all_stats:
        for rt, count in s.get("record_types", {}).items():
            rt_totals[rt] = rt_totals.get(rt, 0) + count

    lines = [
        "# Bronze FPDS Pull Summary",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Overview",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total queries executed | {len(all_stats)} |",
        f"| Total records fetched | {total_records:,} |",
        f"| Total pages fetched | {total_pages:,} |",
        f"| Errors | {len(all_errors)} |",
        "",
        "## Records by Stratum",
        "",
        f"| Stratum | Queries | Records |",
        f"|---------|---------|---------|",
        f"| PSC-based (Stratum 1) | {len(psc_stats)} | {sum(s.get('records_fetched', 0) for s in psc_stats):,} |",
        f"| Keyword gap-fillers (Stratum 2) | {len(kw_stats)} | {sum(s.get('records_fetched', 0) for s in kw_stats):,} |",
        "",
        "## Record Types",
        "",
        f"| Type | Count |",
        f"|------|-------|",
    ]
    for rt, count in rt_totals.items():
        lines.append(f"| {rt} | {count:,} |")

    lines += [
        "",
        "## Query-Level Detail",
        "",
        "| Query Batch | Est. Total | Fetched | Errors |",
        "|-------------|-----------|---------|--------|",
    ]
    for s in all_stats:
        est = s.get("total_estimated", "?")
        if est is not None:
            est = f"{est:,}" if isinstance(est, int) else str(est)
        else:
            est = "?"
        fetched = s.get("records_fetched", 0)
        errs = len(s.get("errors", []))
        skipped = " (skipped)" if s.get("skipped") else ""
        lines.append(f"| {s.get('query_batch', '?')}{skipped} | {est} | {fetched:,} | {errs} |")

    if all_errors:
        lines += ["", "## Errors", ""]
        lines.extend(all_errors)

    lines.append("")
    summary_path.write_text("\n".join(lines))
    log.info(f"Summary written to {summary_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    start_time = time.time()
    all_stats = []

    # Save stats to a JSON file for later analysis
    stats_file = BRONZE_DIR / "_pull_stats.json"

    run_stratum("PSC-based (Stratum 1)", STRATUM1_QUERIES, all_stats)
    run_stratum("Keyword gap-fillers (Stratum 2)", STRATUM2_QUERIES, all_stats)

    # Save raw stats
    with open(stats_file, "w") as f:
        json.dump(all_stats, f, indent=2, default=str)

    generate_summary(all_stats)

    elapsed = time.time() - start_time
    log.info(f"\nPhase 1 complete in {elapsed/60:.1f} minutes.")
    log.info(f"Total records: {sum(s.get('records_fetched', 0) for s in all_stats):,}")


if __name__ == "__main__":
    main()
