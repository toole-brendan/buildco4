#!/usr/bin/env python3
"""
Newbuild / New Construction — Taxonomy Discovery Script

Pulls new-construction contract award data from USAspending API to understand
how ship construction work is described, categorized, and coded in federal
procurement data. This is a DISCOVERY exercise — the goal is to learn the
taxonomy, not to produce final TAM numbers.

Searches:
  - Navy ship program keywords (DDG-51, Virginia, Columbia, FFG, LPD, CVN, T-AO, etc.)
  - Coast Guard cutter programs (NSC, OPC, FRC, PSC/icebreaker)
  - General construction terms ("detail design and construction", "ship construction")
  - PSC product codes in the 19xx range (combat ships, transports, patrol craft, etc.)

Outputs:
  - Raw award JSON files in bottomup/bronze/newbuild/usaspending/
  - CSV of all deduplicated awards
  - Markdown discovery report analyzing descriptions, PSC codes, vendors, etc.
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
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from usaspending_client import spending_by_award, spending_over_time_keywords
from shared_utils import normalize_vendor

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BRONZE_DIR = Path(__file__).parent.parent / "bronze" / "newbuild" / "usaspending"
OUTPUT_CSV = Path(__file__).parent.parent / "newbuild" / "discovery.csv"
REPORT_MD = Path(__file__).parent.parent / "newbuild" / "discovery_report.md"

FY_START = 2017
FY_END = 2026
MAX_PAGES = 10          # up to 1,000 records per query
RECORDS_PER_PAGE = 100
CALL_DELAY = 0.5        # seconds between API calls

# ---------------------------------------------------------------------------
# Keyword groups
# ---------------------------------------------------------------------------

# Trimmed for taxonomy discovery — just enough to see how construction is described
NAVY_KEYWORD_GROUPS = [
    {"keywords": ["detail design and construction"], "label": "kw_dd_and_c"},
    {"keywords": ["ship construction"], "label": "kw_ship_construction"},
    {"keywords": ["advance procurement"], "label": "kw_advance_procurement", "agency": True},
]

CG_KEYWORD_GROUPS = [
    {"keywords": ["offshore patrol cutter"], "label": "kw_opc", "agency_name": "United States Coast Guard"},
    {"keywords": ["cutter construction"], "label": "kw_cutter_construction", "agency_name": "United States Coast Guard"},
]

# Just the main construction PSC code
PSC_CODE_GROUPS = [
    {"psc": ["1905"], "label": "psc_1905_combat"},
]

# Award type groups — contracts and IDVs only (construction is never grants/other)
AWARD_TYPE_GROUPS = {
    "contracts": ["A", "B", "C", "D"],
    "idvs": ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"],
}

NAVY_AGENCY = "Department of the Navy"

# ---------------------------------------------------------------------------
# Pull logic
# ---------------------------------------------------------------------------

def pull_keyword_awards(keyword_groups: list[dict], default_agency: str | None = None) -> list[dict]:
    """Pull awards for all keyword groups across contract + IDV award types."""
    all_records = []
    total = len(keyword_groups) * len(AWARD_TYPE_GROUPS)
    call_count = 0

    for kg in keyword_groups:
        keywords = kg["keywords"]
        label = kg["label"]
        # Agency: explicit agency_name > default if agency=True > None
        agency = kg.get("agency_name") or (default_agency if kg.get("agency", False) else None)

        for atg_name, atg_codes in AWARD_TYPE_GROUPS.items():
            batch_label = f"{label}_{atg_name}"
            call_count += 1
            agency_short = agency.split()[-1] if agency else "any"
            print(f"  [{call_count}/{total}] {keywords} | {atg_name} | agency={agency_short}")

            outfile = str(BRONZE_DIR / f"awards_{batch_label}.json")
            try:
                records = spending_by_award(
                    keywords=keywords,
                    agency_id=agency,
                    fy_start=FY_START,
                    fy_end=FY_END,
                    award_type_codes=atg_codes,
                    limit=RECORDS_PER_PAGE,
                    max_pages=MAX_PAGES,
                    output_file=outfile,
                    query_batch=batch_label,
                )
                print(f"           -> {len(records)} records")
                all_records.extend(records)
            except Exception as e:
                log.error(f"  ERROR on {batch_label}: {e}")
                print(f"           -> ERROR: {e}")

            time.sleep(CALL_DELAY)

    return all_records


def pull_psc_awards() -> list[dict]:
    """Pull awards for PSC 19xx product codes."""
    all_records = []
    total = len(PSC_CODE_GROUPS) * len(AWARD_TYPE_GROUPS)
    call_count = 0

    for pg in PSC_CODE_GROUPS:
        psc = pg["psc"]
        label = pg["label"]

        for atg_name, atg_codes in AWARD_TYPE_GROUPS.items():
            batch_label = f"{label}_{atg_name}"
            call_count += 1
            print(f"  [{call_count}/{total}] PSC={psc} | {atg_name}")

            outfile = str(BRONZE_DIR / f"awards_{batch_label}.json")
            try:
                records = spending_by_award(
                    psc_codes=psc,
                    fy_start=FY_START,
                    fy_end=FY_END,
                    award_type_codes=atg_codes,
                    limit=RECORDS_PER_PAGE,
                    max_pages=MAX_PAGES,
                    output_file=outfile,
                    query_batch=batch_label,
                )
                print(f"           -> {len(records)} records")
                all_records.extend(records)
            except Exception as e:
                log.error(f"  ERROR on {batch_label}: {e}")
                print(f"           -> ERROR: {e}")

            time.sleep(CALL_DELAY)

    return all_records


def pull_spending_trends() -> dict[str, list[dict]]:
    """Pull spending_over_time for key construction keyword groups."""
    trend_groups = [
        {"keywords": ["ship construction"], "label": "ship_construction"},
        {"keywords": ["submarine construction"], "label": "sub_construction"},
        {"keywords": ["DDG 51", "DDG-51", "Arleigh Burke"], "label": "ddg"},
        {"keywords": ["Virginia class"], "label": "virginia"},
        {"keywords": ["Columbia class"], "label": "columbia"},
        {"keywords": ["FFG 62", "Constellation class"], "label": "ffg"},
        {"keywords": ["national security cutter", "offshore patrol cutter", "fast response cutter"], "label": "cg_cutters"},
        {"keywords": ["advance procurement"], "label": "advance_procurement", "agency": NAVY_AGENCY},
        {"keywords": ["detail design and construction"], "label": "dd_and_c"},
    ]

    all_trends = {}
    for tg in trend_groups:
        label = tg["label"]
        kw = tg["keywords"]
        agency = tg.get("agency")
        print(f"  Trend: {label} ({kw})")

        try:
            results = spending_over_time_keywords(
                keywords=kw,
                agency_id=agency,
                fy_start=FY_START,
                fy_end=FY_END,
                award_type_codes=["A", "B", "C", "D"],
            )
            all_trends[label] = results

            outfile = BRONZE_DIR / f"trend_{label}.json"
            outfile.parent.mkdir(parents=True, exist_ok=True)
            with open(outfile, "w") as f:
                json.dump(results, f, indent=2, default=str)

            print(f"           -> {len(results)} FY rows")
        except Exception as e:
            log.error(f"  Trend ERROR {label}: {e}")
            print(f"           -> ERROR: {e}")

        time.sleep(CALL_DELAY)

    return all_trends


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def dedup_by_award_id(records: list[dict]) -> list[dict]:
    """Deduplicate by Award ID, keeping highest award_amount."""
    # Records come sorted by award_amount desc within each batch,
    # so first occurrence per award_id is typically the largest
    seen = set()
    deduped = []
    for r in records:
        aid = r.get("award_id")
        if aid and aid not in seen:
            seen.add(aid)
            deduped.append(r)
    return deduped


# ---------------------------------------------------------------------------
# Discovery report generation
# ---------------------------------------------------------------------------

def generate_report(records: list[dict], trends: dict[str, list[dict]]):
    """Generate markdown discovery report analyzing the pulled data."""
    lines = []
    lines.append("# Newbuild / New Construction — Discovery Report\n")
    lines.append(f"**Generated from USAspending data, FY{FY_START}–FY{FY_END}**\n")
    lines.append(f"**Total unique awards analyzed: {len(records)}**\n")

    # --- 1. Description Samples ---
    lines.append("\n## 1. Sample Contract Descriptions (Top 50 by Award Amount)\n")
    lines.append("These are the actual descriptions contracting officers used:\n")
    sorted_by_amount = sorted(records, key=lambda r: r.get("award_amount") or 0, reverse=True)
    for i, r in enumerate(sorted_by_amount[:50]):
        amt = r.get("award_amount") or 0
        desc = (r.get("description") or "NO DESCRIPTION")[:150]
        vendor = r.get("vendor_name") or "UNKNOWN"
        psc = r.get("psc_code") or "N/A"
        lines.append(f"{i+1}. **${amt:,.0f}** | {vendor} | PSC: {psc}")
        lines.append(f"   > {desc}\n")

    # --- 2. PSC Code Distribution ---
    lines.append("\n## 2. PSC Code Distribution\n")
    psc_counter = Counter()
    psc_dollars = {}
    for r in records:
        psc = r.get("psc_code") or "NULL"
        amt = r.get("award_amount") or 0
        psc_counter[psc] += 1
        psc_dollars[psc] = psc_dollars.get(psc, 0) + amt

    lines.append(f"| PSC Code | Count | Total Award Amount |")
    lines.append(f"|----------|------:|-------------------:|")
    for psc, count in psc_counter.most_common(30):
        dollars = psc_dollars.get(psc, 0)
        lines.append(f"| {psc} | {count} | ${dollars:,.0f} |")

    # --- 3. NAICS Code Distribution ---
    lines.append("\n\n## 3. NAICS Code Distribution\n")
    naics_counter = Counter()
    naics_dollars = {}
    for r in records:
        naics = r.get("naics_code") or "NULL"
        amt = r.get("award_amount") or 0
        naics_counter[naics] += 1
        naics_dollars[naics] = naics_dollars.get(naics, 0) + amt

    lines.append(f"| NAICS Code | Count | Total Award Amount |")
    lines.append(f"|------------|------:|-------------------:|")
    for naics, count in naics_counter.most_common(20):
        dollars = naics_dollars.get(naics, 0)
        lines.append(f"| {naics} | {count} | ${dollars:,.0f} |")

    # --- 4. Top Vendors ---
    lines.append("\n\n## 4. Top Vendors by Total Award Amount\n")
    vendor_dollars = {}
    vendor_count = Counter()
    for r in records:
        v = normalize_vendor(r.get("vendor_name") or "UNKNOWN")
        amt = r.get("award_amount") or 0
        vendor_dollars[v] = vendor_dollars.get(v, 0) + amt
        vendor_count[v] += 1

    vendor_sorted = sorted(vendor_dollars.items(), key=lambda x: x[1], reverse=True)
    lines.append(f"| Vendor | Award Count | Total Award Amount |")
    lines.append(f"|--------|----------:|-------------------:|")
    for vendor, dollars in vendor_sorted[:30]:
        count = vendor_count[vendor]
        lines.append(f"| {vendor} | {count} | ${dollars:,.0f} |")

    # --- 5. Award Type Distribution ---
    lines.append("\n\n## 5. Award Type Distribution\n")
    type_counter = Counter()
    type_dollars = {}
    for r in records:
        atype = r.get("contract_award_type") or "UNKNOWN"
        amt = r.get("award_amount") or 0
        type_counter[atype] += 1
        type_dollars[atype] = type_dollars.get(atype, 0) + amt

    lines.append(f"| Award Type | Count | Total Award Amount |")
    lines.append(f"|------------|------:|-------------------:|")
    for atype, count in type_counter.most_common():
        dollars = type_dollars.get(atype, 0)
        lines.append(f"| {atype} | {count} | ${dollars:,.0f} |")

    # --- 6. Awarding Sub-Agency Distribution ---
    lines.append("\n\n## 6. Awarding Sub-Agency Distribution\n")
    agency_counter = Counter()
    agency_dollars = {}
    for r in records:
        ag = r.get("awarding_sub_agency") or "UNKNOWN"
        amt = r.get("award_amount") or 0
        agency_counter[ag] += 1
        agency_dollars[ag] = agency_dollars.get(ag, 0) + amt

    lines.append(f"| Sub-Agency | Count | Total Award Amount |")
    lines.append(f"|------------|------:|-------------------:|")
    for ag, count in agency_counter.most_common(20):
        dollars = agency_dollars.get(ag, 0)
        lines.append(f"| {ag} | {count} | ${dollars:,.0f} |")

    # --- 7. Query Batch Hit Distribution ---
    lines.append("\n\n## 7. Which Query Batches Produced Results\n")
    batch_counter = Counter()
    for r in records:
        batch = r.get("query_batch") or "UNKNOWN"
        batch_counter[batch] += 1

    lines.append(f"| Query Batch | Unique Awards |")
    lines.append(f"|-------------|-------------:|")
    for batch, count in batch_counter.most_common():
        lines.append(f"| {batch} | {count} |")

    # --- 8. Spending Trends ---
    lines.append("\n\n## 8. Spending Trends (FY-Level)\n")
    for label, trend_data in trends.items():
        lines.append(f"\n### {label}\n")
        lines.append(f"| FY | Obligated |")
        lines.append(f"|---:|----------:|")
        for row in sorted(trend_data, key=lambda x: x.get("fiscal_year", 0)):
            fy = row.get("fiscal_year", "?")
            amt = row.get("aggregated_amount", 0) or 0
            lines.append(f"| {fy} | ${amt:,.0f} |")

    # --- 9. Description Keyword Frequency ---
    lines.append("\n\n## 9. Common Words/Phrases in Descriptions\n")
    lines.append("Frequency of key terms across all award descriptions:\n")

    term_patterns = [
        ("CONSTRUCTION", r"\bCONSTRUCTION\b"),
        ("DETAIL DESIGN", r"\bDETAIL DESIGN\b"),
        ("ADVANCE PROCUREMENT", r"\bADVANCE PROCUREMENT\b"),
        ("LONG LEAD", r"\bLONG[- ]LEAD\b"),
        ("FABRICAT", r"\bFABRICAT"),
        ("BUILD", r"\bBUILD"),
        ("DDG", r"\bDDG\b"),
        ("SSN / VIRGINIA", r"\b(SSN|VIRGINIA)\b"),
        ("SSBN / COLUMBIA", r"\b(SSBN|COLUMBIA)\b"),
        ("CVN / CARRIER", r"\b(CVN|CARRIER)\b"),
        ("FFG / FRIGATE / CONSTELLATION", r"\b(FFG|FRIGATE|CONSTELLATION)\b"),
        ("LPD", r"\bLPD\b"),
        ("LHA", r"\bLHA\b"),
        ("SUBMARINE", r"\bSUBMARINE\b"),
        ("DESTROYER", r"\bDESTROYER\b"),
        ("CUTTER", r"\bCUTTER\b"),
        ("OILER / T-AO", r"\b(OILER|T-AO|TAO)\b"),
        ("REPAIR", r"\bREPAIR\b"),
        ("MAINTENANCE", r"\bMAINTENANCE\b"),
        ("MODERNIZATION", r"\bMODERNIZATION\b"),
        ("OVERHAUL", r"\bOVERHAUL\b"),
        ("MODIFICATION", r"\bMODIFICATION\b"),
        ("ENGINEERING", r"\bENGINEERING\b"),
        ("INTEGRATION", r"\bINTEGRATION\b"),
        ("COMBAT SYSTEM", r"\bCOMBAT SYSTEM\b"),
        ("GFE", r"\bGFE\b"),
        ("GOVERNMENT FURNISHED", r"\bGOVERNMENT FURNISHED\b"),
        ("COMPLETION", r"\bCOMPLETION\b"),
    ]

    lines.append(f"| Term | Count | % of Awards |")
    lines.append(f"|------|------:|------------:|")
    total_records = len(records)
    for term_name, pattern in term_patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        count = sum(1 for r in records if r.get("description") and regex.search(r["description"]))
        pct = (count / total_records * 100) if total_records > 0 else 0
        lines.append(f"| {term_name} | {count} | {pct:.1f}% |")

    # --- 10. All Unique Descriptions (for manual taxonomy review) ---
    lines.append("\n\n## 10. All Unique Descriptions (for manual review)\n")
    lines.append("Sorted by award amount descending. Use this to identify natural groupings.\n")

    seen_descs = set()
    unique_desc_records = []
    for r in sorted_by_amount:
        desc = (r.get("description") or "").strip().upper()
        if desc and desc not in seen_descs:
            seen_descs.add(desc)
            unique_desc_records.append(r)

    lines.append(f"**{len(unique_desc_records)} unique descriptions found.**\n")

    for i, r in enumerate(unique_desc_records[:200]):
        amt = r.get("award_amount") or 0
        desc = (r.get("description") or "NO DESCRIPTION")[:200]
        vendor = r.get("vendor_name") or "UNKNOWN"
        psc = r.get("psc_code") or "N/A"
        naics = r.get("naics_code") or "N/A"
        lines.append(f"{i+1}. **${amt:,.0f}** | {vendor} | PSC={psc} | NAICS={naics}")
        lines.append(f"   > {desc}\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("Newbuild / New Construction — Taxonomy Discovery")
    print("USAspending Award Pull")
    print("=" * 70)

    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Pull Navy keyword awards
    print(f"\n--- Step 1: Navy Program Keywords ({len(NAVY_KEYWORD_GROUPS)} groups) ---")
    navy_records = pull_keyword_awards(NAVY_KEYWORD_GROUPS, default_agency=NAVY_AGENCY)
    print(f"  Navy keyword total: {len(navy_records)} raw records\n")

    # Step 2: Pull CG keyword awards
    print(f"--- Step 2: Coast Guard Program Keywords ({len(CG_KEYWORD_GROUPS)} groups) ---")
    cg_records = pull_keyword_awards(CG_KEYWORD_GROUPS)
    print(f"  CG keyword total: {len(cg_records)} raw records\n")

    # Step 3: Pull PSC 19xx code awards
    print(f"--- Step 3: PSC 19xx Product Code Awards ({len(PSC_CODE_GROUPS)} groups) ---")
    psc_records = pull_psc_awards()
    print(f"  PSC total: {len(psc_records)} raw records\n")

    # Step 4: Combine and dedup
    all_raw = navy_records + cg_records + psc_records
    print(f"--- Step 4: Deduplication ---")
    print(f"  Raw total: {len(all_raw)} records")
    all_deduped = dedup_by_award_id(all_raw)
    print(f"  After dedup: {len(all_deduped)} unique awards\n")

    # Step 5: Write CSV
    print(f"--- Step 5: Writing CSV ---")
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "award_id", "vendor_name", "description", "award_amount",
        "total_outlays", "contract_award_type", "start_date", "end_date",
        "awarding_agency", "awarding_sub_agency", "naics_code", "psc_code",
        "query_batch",
    ]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in sorted(all_deduped, key=lambda x: x.get("award_amount") or 0, reverse=True):
            writer.writerow(r)
    print(f"  Wrote {len(all_deduped)} records to {OUTPUT_CSV}\n")

    # Step 6: Spending trends — SKIPPED for taxonomy discovery
    trends = {}
    print(f"--- Step 6: Spending Trends — SKIPPED (taxonomy only) ---\n")

    # Step 7: Generate discovery report
    print(f"--- Step 7: Generating Discovery Report ---")
    report = generate_report(all_deduped, trends)
    with open(REPORT_MD, "w") as f:
        f.write(report)
    print(f"  Wrote report to {REPORT_MD}")

    print("\n" + "=" * 70)
    print("Newbuild Discovery complete.")
    print(f"  Awards CSV:  {OUTPUT_CSV}")
    print(f"  Report:      {REPORT_MD}")
    print(f"  Bronze data: {BRONZE_DIR}/")
    print("=" * 70)
