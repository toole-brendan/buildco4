#!/usr/bin/env python3
"""
Gold Layer: Aggregate Silver data into final TAM analysis outputs.
Produces:
  - gold_tam_table.md — bucket-by-bucket spend with FY columns
  - gold_vendor_landscape.md — top vendors by bucket, market share
  - gold_confidence_and_gaps.md — methodology, blind spots, confidence notes
  - tam_bottomup_summary.md — executive summary
Also incorporates USAspending aggregate trend data for market-level sizing.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared_utils import normalize_vendor, load_json_records

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

SILVER_DIR = Path(__file__).parent.parent / "silver"
BRONZE_USA_DIR = Path(__file__).parent.parent / "bronze" / "usaspending"
GOLD_DIR = Path(__file__).parent.parent / "gold"
GOLD_DIR.mkdir(parents=True, exist_ok=True)

BUCKET_NAMES = {
    1: "Scheduled Depot Maintenance & Repair",
    2: "Continuous / Intermediate / Emergent",
    3: "Modernization & Alteration Installation",
    4: "Major Life-Cycle Events (RCOH/SLEP/MMA)",
    5: "Sustainment Engineering / Planning",
    6: "Availability Support / Port Services",
}


def load_silver() -> list[dict]:
    csv_path = SILVER_DIR / "silver_canonical.csv"
    if not csv_path.exists():
        log.error(f"Silver CSV not found: {csv_path}")
        return []
    records = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    log.info(f"Loaded {len(records):,} records from Silver CSV")
    return records


def load_usaspending_trends() -> dict:
    """Load all USAspending trend JSON files."""
    trends = {}
    if not BRONZE_USA_DIR.exists():
        return trends
    for f in sorted(BRONZE_USA_DIR.glob("trend_*.json")):
        label = f.stem.replace("trend_", "")
        trends[label] = load_json_records(str(f))
    return trends


def load_usaspending_vendors() -> dict:
    """Load all USAspending vendor landscape JSON files."""
    vendors = {}
    if not BRONZE_USA_DIR.exists():
        return vendors
    for f in sorted(BRONZE_USA_DIR.glob("vendors_*.json")):
        label = f.stem
        vendors[label] = load_json_records(str(f))
    return vendors


def _fiscal_year(record: dict) -> str | None:
    """Extract fiscal year from a record."""
    fy = record.get("fiscal_year")
    if fy:
        return str(fy)
    # Try to derive from signed_date
    sd = record.get("signed_date", "")
    if sd and len(sd) >= 7:
        try:
            year = int(sd[:4])
            month = int(sd[5:7])
            return str(year + 1) if month >= 10 else str(year)
        except (ValueError, IndexError):
            pass
    return None


def _safe_float(val) -> float:
    if val is None or val == "" or val == "None":
        return 0.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


# ===================================================================
# Gold Output 1: TAM Table
# ===================================================================

def generate_tam_table(included: list[dict], trends: dict):
    """Bucket-by-bucket TAM table combining FPDS record-level data and USAspending trends."""
    path = GOLD_DIR / "gold_tam_table.md"

    # --- Section A: USAspending aggregate trends (the authoritative FY totals) ---
    lines = [
        "# Bottom-Up TAM Table: In-Service Vessel Work",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Section A: Market-Level Spending Trends (USAspending Aggregates)",
        "",
        "These are authoritative FY-level obligation totals from USAspending `spending_over_time`.",
        "They represent the most reliable top-line numbers because they cover the full dataset",
        "without pagination limits.",
        "",
    ]

    # Format each trend
    trend_groups = [
        ("J998_J999_all", "Ship Repair (J998+J999) — All Agencies", "Buckets 1+2 core"),
        ("J998_J999_navy", "Ship Repair (J998+J999) — Navy Only", ""),
        ("J998_J999_dhs", "Ship Repair (J998+J999) — DHS/Coast Guard", ""),
        ("J019_J020_all", "Equipment Maintenance/Repair (J019+J020) — All", "Buckets 1+2 component-level"),
        ("J019_J020_navy", "Equipment Maintenance/Repair (J019+J020) — Navy", ""),
        ("K019_K020_all", "Modification of Equipment (K019+K020) — All", "Bucket 3"),
        ("N019_N020_all", "Installation of Equipment (N019+N020) — All", "Bucket 3"),
        ("R425_R408_navy", "Engineering/Technical (R425+R408) — Navy", "Bucket 5 (noisy)"),
        ("kw_RCOH_all", "RCOH Keyword — All Agencies", "Bucket 4"),
        ("kw_SLEP_all", "SLEP Keyword — All Agencies", "Bucket 4"),
        ("kw_CMAV_navy", "CMAV Keyword — Navy", "Bucket 2"),
        ("kw_HUSBANDING_navy", "Husbanding Keyword — Navy", "Bucket 6"),
    ]

    for key, title, note in trend_groups:
        data = trends.get(key, [])
        if not data:
            continue
        lines.append(f"### {title}")
        if note:
            lines.append(f"*{note}*")
        lines.append("")
        lines.append("| FY | Obligations ($M) |")
        lines.append("|-----|-----------------|")
        for row in sorted(data, key=lambda x: x.get("fiscal_year", 0)):
            fy = row.get("fiscal_year", "?")
            amt = row.get("aggregated_amount", 0)
            if amt is not None:
                lines.append(f"| {fy} | ${amt / 1e6:,.0f}M |")
        lines.append("")

    # --- Section B: FPDS record-level bucket breakdown ---
    lines.extend([
        "---",
        "",
        "## Section B: Bucket-by-Bucket Breakdown (FPDS Record-Level Data)",
        "",
        "Based on FPDS contract-level records classified into the six buckets.",
        "**Note**: J999 Navy data is partial (~7K of ~26K records). These numbers",
        "understate the true totals. Use Section A USAspending trends for market-level sizing.",
        "",
    ])

    # Aggregate by bucket x FY
    bucket_fy_dollars = defaultdict(lambda: defaultdict(float))
    bucket_fy_counts = defaultdict(lambda: defaultdict(int))
    for r in included:
        b = r.get("bucket_primary")
        if not b or b == "None":
            continue
        b = int(b)
        fy = _fiscal_year(r)
        if not fy:
            continue
        amt = _safe_float(r.get("total_obligated"))
        bucket_fy_dollars[b][fy] += amt
        bucket_fy_counts[b][fy] += 1

    all_fys = sorted(set(
        fy for bdata in bucket_fy_dollars.values() for fy in bdata.keys()
    ))
    # Filter to FY22-FY26
    all_fys = [fy for fy in all_fys if fy >= "2022" and fy <= "2026"]

    fy_headers = " | ".join(f"FY{fy[2:]}" for fy in all_fys)
    fy_dashes = " | ".join("---:" for _ in all_fys)

    lines.append(f"| # | Bucket | {fy_headers} | Total |")
    lines.append(f"|---|--------|{fy_dashes} | ---: |")

    for b in range(1, 7):
        name = BUCKET_NAMES.get(b, "?")
        fy_vals = []
        total = 0
        for fy in all_fys:
            amt = bucket_fy_dollars[b].get(fy, 0)
            total += amt
            fy_vals.append(f"${amt / 1e6:,.0f}M")
        lines.append(f"| {b} | {name} | {' | '.join(fy_vals)} | ${total / 1e6:,.0f}M |")

    # Grand total row
    grand_vals = []
    grand_total = 0
    for fy in all_fys:
        fy_sum = sum(bucket_fy_dollars[b].get(fy, 0) for b in range(1, 7))
        grand_total += fy_sum
        grand_vals.append(f"${fy_sum / 1e6:,.0f}M")
    lines.append(f"| | **Total** | {' | '.join(grand_vals)} | **${grand_total / 1e6:,.0f}M** |")

    lines.extend([
        "",
        "### Record Counts by Bucket x FY",
        "",
        f"| # | Bucket | {fy_headers} | Total |",
        f"|---|--------|{fy_dashes} | ---: |",
    ])
    for b in range(1, 7):
        name = BUCKET_NAMES.get(b, "?")
        fy_vals = []
        total = 0
        for fy in all_fys:
            cnt = bucket_fy_counts[b].get(fy, 0)
            total += cnt
            fy_vals.append(f"{cnt:,}")
        lines.append(f"| {b} | {name} | {' | '.join(fy_vals)} | {total:,} |")

    lines.append("")
    path.write_text("\n".join(lines))
    log.info(f"TAM table written to {path}")


# ===================================================================
# Gold Output 2: Vendor Landscape
# ===================================================================

def generate_vendor_landscape(included: list[dict], usa_vendors: dict):
    path = GOLD_DIR / "gold_vendor_landscape.md"

    lines = [
        "# Bottom-Up Vendor Landscape: In-Service Vessel Work",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    # --- Section A: USAspending vendor rankings (authoritative) ---
    lines.extend([
        "## Section A: USAspending Vendor Rankings (Authoritative)",
        "",
        "These come from `spending_by_category/recipient` — covers the full dataset.",
        "",
    ])

    vendor_labels = [
        ("vendors_J998_J999_navy_fy22-26", "Ship Repair (J998+J999) Navy FY22-26"),
        ("vendors_J998_J999_all_fy22-26", "Ship Repair (J998+J999) All Agencies FY22-26"),
        ("vendors_J998_navy_fy24", "Ship Repair (J998) Navy FY24"),
        ("vendors_J998_navy_fy23", "Ship Repair (J998) Navy FY23"),
        ("vendors_J019_J020_navy_fy22-26", "Equipment Repair (J019+J020) Navy FY22-26"),
        ("vendors_mod_install_navy_fy22-26", "Mod/Install (K019/K020/N019/N020) Navy FY22-26"),
        ("vendors_J998_J999_dhs_fy22-26", "Ship Repair (J998+J999) DHS/CG FY22-26"),
    ]

    for key, title in vendor_labels:
        data = usa_vendors.get(key, [])
        if not data:
            continue
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| Rank | Vendor | Obligations ($M) |")
        lines.append("|------|--------|-----------------|")
        for i, v in enumerate(data[:20], 1):
            name = v.get("name", "?")
            amt = v.get("amount", 0)
            if amt is not None:
                lines.append(f"| {i} | {name} | ${amt / 1e6:,.1f}M |")
        lines.append("")

    # --- Section B: FPDS record-level vendor analysis by bucket ---
    lines.extend([
        "---",
        "",
        "## Section B: Vendors by Bucket (FPDS Record-Level)",
        "",
        "Based on vendor_normalized from FPDS records. Uses total_obligated from latest mod per PIID.",
        "",
    ])

    for b in range(1, 7):
        bucket_name = BUCKET_NAMES.get(b, "?")
        bucket_records = [r for r in included if r.get("bucket_primary") == str(b)]

        vendor_totals = defaultdict(float)
        for r in bucket_records:
            v = r.get("vendor_normalized", "")
            if not v:
                continue
            vendor_totals[v] += _safe_float(r.get("total_obligated"))

        top = sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True)[:15]
        total_bucket = sum(vendor_totals.values())

        lines.append(f"### Bucket {b}: {bucket_name}")
        lines.append("")
        if not top:
            lines.append("*No FPDS records classified into this bucket.*")
            lines.append("")
            continue
        lines.append(f"Total obligated: ${total_bucket / 1e6:,.0f}M across {len(vendor_totals)} vendors")
        lines.append("")
        lines.append("| Rank | Vendor | Obligated ($M) | Share |")
        lines.append("|------|--------|---------------|-------|")
        for i, (v, amt) in enumerate(top, 1):
            share = amt / total_bucket * 100 if total_bucket > 0 else 0
            lines.append(f"| {i} | {v} | ${amt / 1e6:,.1f}M | {share:.1f}% |")
        lines.append("")

    # --- Cross-bucket vendor presence ---
    lines.extend([
        "---",
        "",
        "## Cross-Bucket Vendor Presence",
        "",
        "Which companies span multiple buckets?",
        "",
    ])

    vendor_buckets = defaultdict(set)
    vendor_total_all = defaultdict(float)
    for r in included:
        v = r.get("vendor_normalized", "")
        b = r.get("bucket_primary")
        if v and b and b != "None":
            vendor_buckets[v].add(int(b))
            vendor_total_all[v] += _safe_float(r.get("total_obligated"))

    multi_bucket = {v: bs for v, bs in vendor_buckets.items() if len(bs) > 1}
    multi_sorted = sorted(multi_bucket.items(), key=lambda x: vendor_total_all[x[0]], reverse=True)[:20]

    lines.append("| Vendor | Buckets | Total Obligated ($M) |")
    lines.append("|--------|---------|---------------------|")
    for v, bs in multi_sorted:
        bucket_str = ", ".join(str(b) for b in sorted(bs))
        lines.append(f"| {v} | {bucket_str} | ${vendor_total_all[v] / 1e6:,.1f}M |")

    lines.append("")
    path.write_text("\n".join(lines))
    log.info(f"Vendor landscape written to {path}")


# ===================================================================
# Gold Output 3: Confidence and Gaps
# ===================================================================

def generate_confidence_and_gaps(included: list[dict]):
    path = GOLD_DIR / "gold_confidence_and_gaps.md"

    # Confidence breakdown
    conf_counts = Counter(r.get("confidence") for r in included)
    source_counts = Counter(r.get("source") for r in included)

    lines = [
        "# Bottom-Up Analysis: Confidence Assessment & Known Gaps",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Methodology",
        "",
        "This bottom-up analysis uses a hybrid approach (Option D):",
        "",
        "1. **USAspending aggregate endpoints** for authoritative FY-level spending trends",
        "   and vendor rankings. These cover the complete dataset without pagination limits.",
        "2. **FPDS Atom Feed record-level pulls** for description-level analysis — bucket",
        "   classification, contract vehicle characterization, and competition analysis.",
        "3. **Six-bucket classification** based on description keywords (high confidence),",
        "   PSC code defaults (medium confidence), or general ship work regex (low confidence).",
        "",
        "## Data Coverage",
        "",
        "### USAspending Aggregates",
        "- `spending_over_time`: Complete FY17-FY26 trends for all PSC groups + keywords",
        "- `spending_by_category/recipient`: Complete vendor rankings",
        "- `spending_by_award`: Top 300 awards per query for detail/validation",
        "",
        "### FPDS Record-Level",
        "",
        "| Source | Records |",
        "|--------|---------|",
    ]
    for src, cnt in source_counts.most_common():
        lines.append(f"| {src} | {cnt:,} |")

    lines.extend([
        "",
        "## Classification Confidence",
        "",
        "| Confidence | Records | Description |",
        "|-----------|---------|-------------|",
        f"| High | {conf_counts.get('High', 0):,} | Classified by specific description keyword (DSRA, CMAV, RCOH, etc.) |",
        f"| Medium | {conf_counts.get('Medium', 0):,} | Classified by PSC code default (J998→Bucket 1, K019→Bucket 3, etc.) |",
        f"| Low | {conf_counts.get('Low', 0):,} | General ship work regex match, assigned to Bucket 1 by default |",
        "",
        "## Known Gaps and Blind Spots",
        "",
        "### 1. Public Naval Shipyard Work (~$7-8B/yr)",
        "Organic work performed at the four public naval shipyards (Norfolk, Puget Sound,",
        "Pearl Harbor, Portsmouth) does **not** appear in FPDS or USAspending because it is",
        "not contracted. This is the single largest gap. The top-down budget analysis sizes",
        "this from NWCF depot maintenance data.",
        "",
        "### 2. J999 Navy Data Incomplete",
        "The FPDS pull for J999 Navy FY22-26 was interrupted (~7K of estimated ~26K records).",
        "This means FPDS record-level analysis (bucket classification, pricing, competition)",
        "understates the J999 contribution. USAspending aggregate trends are unaffected.",
        "",
        "### 3. Blended Contracts (Bucket 1 vs. Bucket 3)",
        "Large availability contracts (DMP, DSRA) typically bundle maintenance + modernization",
        "into a single award. Contracting officers assign PSC based on the **predominant**",
        "product/service. We assign these to Bucket 1 (primary) with Bucket 3 (secondary).",
        "The true Bucket 3 (modernization) dollar volume is understated in bottom-up data",
        "because the modernization component is absorbed into Bucket 1 awards. The top-down",
        "OPN budget analysis provides a better Bucket 3 estimate.",
        "",
        "### 4. OPN Equipment Procurement",
        "Equipment procurement for in-service modifications (DDG Mod ~$700M-1B/yr, combat",
        "system upgrades, etc.) is coded under product PSC codes, not service codes. This",
        "means it doesn't appear in J998/J999/K019/N019 pulls. Bucket 3 bottom-up totals",
        "capture **installation labor** but miss the **equipment procurement** component.",
        "Top-down OPN analysis is the only way to size this.",
        "",
        "### 5. Sustainment Engineering (Bucket 5) is Noisy",
        "PSC R425/R408 cover all engineering/technical services, not just ship-related.",
        "We apply strict description filtering, but this likely excludes legitimate ship",
        "sustainment contracts with generic descriptions. The top-down OMN SAG 1B5B",
        "(~$2.76B/yr) is a better sizing source for this bucket.",
        "",
        "### 6. Availability Support (Bucket 6) is Sparse",
        "Ship husbanding PSC codes (M2AA-M2CA) were only activated in 2020 and are still",
        "underused by contracting officers. Keyword search ('HUSBANDING') captures some",
        "but not all support services. This bucket is better sized from OMN sub-elements.",
        "",
        "### 7. Subcontractor Spending Invisible",
        "Only prime contractor awards appear in FPDS. Subcontractor spending (which can be",
        "30-50% of a large availability contract) is invisible. This doesn't affect TAM",
        "sizing (the prime award captures the full value) but it does affect vendor landscape",
        "analysis — subcontractors like MHI, Epsilon Systems, etc. don't show up.",
        "",
        "### 8. Classified Program Details",
        "Some submarine and carrier work details are classified. FPDS records exist but",
        "descriptions may be redacted or generic. These records fall into 'Medium' or 'Low'",
        "confidence classification.",
        "",
        "## Triangulation with Top-Down Analysis",
        "",
        "The bottom-up contract data should be cross-referenced with the top-down budget",
        "analysis. Key validation checks:",
        "",
        "| Check | Bottom-Up Source | Top-Down Source | Expected Agreement |",
        "|-------|-----------------|----------------|-------------------|",
        "| Total private ship repair | J998+J999 trend | OMN 1B4B minus public yards | Within 20% |",
        "| RCOH spending | RCOH keyword trend | SCN RCOH line item | Close match |",
        "| CG vessel sustainment | J998+J999 DHS trend | CG PC&I ISVS | Within 30% |",
        "| Modernization | K019+N019 + DMP secondary | OPN mod BLIs | Bottom-up << top-down (expected) |",
        "| Engineering support | R425+R408 filtered | OMN 1B5B | Bottom-up < top-down (expected) |",
        "",
    ]

    path.write_text("\n".join(lines))
    log.info(f"Confidence and gaps written to {path}")


# ===================================================================
# Gold Output 4: Executive Summary
# ===================================================================

def generate_executive_summary(included: list[dict], trends: dict, usa_vendors: dict):
    path = GOLD_DIR / "tam_bottomup_summary.md"

    # Pull key numbers from trends
    j998_j999_all = trends.get("J998_J999_all", [])
    latest_fy_total = None
    for row in j998_j999_all:
        if row.get("fiscal_year") == 2024:
            latest_fy_total = row.get("aggregated_amount")

    j998_j999_navy = trends.get("J998_J999_navy", [])
    navy_fy24 = None
    for row in j998_j999_navy:
        if row.get("fiscal_year") == 2024:
            navy_fy24 = row.get("aggregated_amount")

    j019_j020 = trends.get("J019_J020_all", [])
    j019_fy24 = None
    for row in j019_j020:
        if row.get("fiscal_year") == 2024:
            j019_fy24 = row.get("aggregated_amount")

    # CG
    cg_trend = trends.get("J998_J999_dhs", [])
    cg_fy24 = None
    for row in cg_trend:
        if row.get("fiscal_year") == 2024:
            cg_fy24 = row.get("aggregated_amount")

    # RCOH
    rcoh_trend = trends.get("kw_RCOH_all", [])
    rcoh_fy24 = None
    for row in rcoh_trend:
        if row.get("fiscal_year") == 2024:
            rcoh_fy24 = row.get("aggregated_amount")

    def fmt(val):
        if val is None:
            return "N/A"
        return f"${val / 1e9:,.1f}B" if abs(val) >= 1e9 else f"${val / 1e6:,.0f}M"

    lines = [
        "# Bottom-Up TAM Summary: In-Service Vessel Work",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Executive Summary",
        "",
        "This bottom-up analysis sizes the U.S. federal in-service vessel work market",
        "using contract obligation data from USAspending and FPDS. The analysis covers",
        "FY17-FY26 trends and classifies contracted work into six defensible buckets.",
        "",
        "### Key Findings",
        "",
        f"- **Ship repair contracts (J998+J999) totaled {fmt(latest_fy_total)} in FY24** across all agencies",
        f"  - Navy: {fmt(navy_fy24)}",
        f"  - Coast Guard/DHS: {fmt(cg_fy24)}",
        f"- **Equipment-level repair (J019+J020): {fmt(j019_fy24)} in FY24**",
        f"- **RCOH-related contracts: {fmt(rcoh_fy24)} in FY24** (keyword search)",
        "- The contracted market has been **stable at $4-5B/yr** for ship repair (J998+J999)",
        "  over FY17-FY24, with modest growth in component-level work",
        "",
        "### What This Covers vs. What It Misses",
        "",
        "| Component | Covered? | Source |",
        "|-----------|----------|--------|",
        "| Private shipyard depot work | Yes | J998+J999 |",
        "| Component/equipment repair | Yes | J019+J020 |",
        "| Standalone mod/install | Yes | K019+N019 |",
        "| RCOH/SLEP/MMA | Partially | Keyword search |",
        "| Sustainment engineering | Partially | R425+R408 (noisy) |",
        "| Port services/husbanding | Partially | Keyword + M2xx |",
        "| **Public naval shipyard work** | **No** | **~$7-8B/yr invisible** |",
        "| **OPN equipment procurement** | **No** | **$2-3B/yr in product codes** |",
        "",
        "### Bottom-Up Contracted Market Size (FY24)",
        "",
        "| Component | FY24 Obligations | Notes |",
        "|-----------|-----------------|-------|",
        f"| Ship repair (J998+J999) | {fmt(latest_fy_total)} | Core market — all agencies |",
        f"| Equipment repair (J019+J020) | {fmt(j019_fy24)} | Component-level |",
        "| Standalone mod/install (K019+N019) | ~$130-230M | Small, declining |",
        f"| RCOH/major overhauls | {fmt(rcoh_fy24)} | Keyword-based, may undercount |",
        "| Engineering/planning (R425+R408 filtered) | ~$1-2B est. | Ship-specific subset |",
        "| Port services/husbanding | <$100M | Sparse data |",
        f"| **Total contracted (visible)** | **~$6-8B/yr** | |",
        "| + Public yards (invisible) | ~$7-8B | From top-down budget data |",
        "| + OPN equipment procurement | ~$2-3B | From top-down budget data |",
        "| **= Total in-service vessel work** | **~$15-19B/yr** | **Triangulated estimate** |",
        "",
    ]

    # Top vendors section
    navy_vendors = usa_vendors.get("vendors_J998_J999_navy_fy22-26", [])
    if navy_vendors:
        lines.extend([
            "### Top Ship Repair Vendors (Navy J998+J999, FY22-26)",
            "",
            "| Rank | Vendor | Obligations ($M) |",
            "|------|--------|-----------------|",
        ])
        for i, v in enumerate(navy_vendors[:10], 1):
            lines.append(f"| {i} | {v.get('name', '?')} | {fmt(v.get('amount', 0))} |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Methodology",
        "",
        "**Option D Hybrid Approach:**",
        "1. USAspending `spending_over_time` for FY-level obligation trends by PSC group",
        "2. USAspending `spending_by_category/recipient` for vendor rankings",
        "3. USAspending `spending_by_award` for top-contract detail",
        "4. FPDS Atom Feed for record-level description analysis, bucket classification,",
        "   contract pricing, and competition characterization",
        "",
        "**Six-bucket classification** based on:",
        "- Priority 1: Description keywords (DSRA, CMAV, RCOH, etc.) → High confidence",
        "- Priority 2: PSC code defaults (J998→B1, K019→B3, etc.) → Medium confidence",
        "- Priority 3: General ship work regex → Low confidence",
        "",
        "**Deduplication:** Latest modification per PIID (FPDS), unique Award ID (USAspending).",
        "Dollar amounts use `total_obligated` from the latest mod — never summed across mods.",
        "",
        "See `gold_confidence_and_gaps.md` for full methodology notes and known limitations.",
        "",
    ])

    path.write_text("\n".join(lines))
    log.info(f"Executive summary written to {path}")


# ===================================================================
# Main
# ===================================================================

def main():
    log.info("=" * 60)
    log.info("GOLD LAYER: Aggregate and Produce Analysis")
    log.info("=" * 60)

    # Load data
    silver = load_silver()
    included = [r for r in silver if r.get("disposition") == "INCLUDE"]
    log.info(f"Silver INCLUDE records: {len(included):,}")

    trends = load_usaspending_trends()
    log.info(f"USAspending trends loaded: {len(trends)} datasets")

    usa_vendors = load_usaspending_vendors()
    log.info(f"USAspending vendor datasets loaded: {len(usa_vendors)}")

    # Generate outputs
    generate_tam_table(included, trends)
    generate_vendor_landscape(included, usa_vendors)
    generate_confidence_and_gaps(included)
    generate_executive_summary(included, trends, usa_vendors)

    log.info("\nGold layer complete.")


if __name__ == "__main__":
    main()
