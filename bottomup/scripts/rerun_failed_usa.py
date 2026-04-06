#!/usr/bin/env python3
"""Re-run the USAspending queries that failed due to agency filter format."""
from __future__ import annotations
import json, os, sys, time, logging
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usaspending_client import (
    spending_over_time, spending_over_time_keywords,
    spending_by_recipient, spending_by_award,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

USA_DIR = Path(__file__).parent.parent / "bronze" / "usaspending"
USA_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "Department of the Navy"
CG = "United States Coast Guard"

def save(data, filepath, label):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    log.info(f"[{label}] Saved {filepath.name}")

def main():
    # --- Trends with agency filter ---
    trend_queries = [
        (["J998", "J999"], NAVY, "J998_J999_navy"),
        (["J998", "J999"], CG, "J998_J999_dhs"),
        (["J019", "J020"], NAVY, "J019_J020_navy"),
        (["R425", "R408"], NAVY, "R425_R408_navy"),
    ]
    for psc, agency, label in trend_queries:
        log.info(f"Trend: {label}")
        try:
            data = spending_over_time(psc, agency_id=agency, fy_start=2017, fy_end=2026)
            save(data, USA_DIR / f"trend_{label}.json", label)
        except Exception as e:
            log.error(f"FAILED {label}: {e}")
        time.sleep(0.3)

    # Keyword trends with agency
    kw_queries = [
        (["HUSBANDING"], NAVY, "kw_HUSBANDING_navy"),
        (["CMAV"], NAVY, "kw_CMAV_navy"),
    ]
    for kw, agency, label in kw_queries:
        log.info(f"Keyword trend: {label}")
        try:
            data = spending_over_time_keywords(kw, agency_id=agency, fy_start=2017, fy_end=2026)
            save(data, USA_DIR / f"trend_{label}.json", label)
        except Exception as e:
            log.error(f"FAILED {label}: {e}")
        time.sleep(0.3)

    # --- Vendors with agency filter ---
    vendor_queries = [
        (["J998"], NAVY, 2024, 2024, "vendors_J998_navy_fy24"),
        (["J998"], NAVY, 2023, 2023, "vendors_J998_navy_fy23"),
        (["J998", "J999"], NAVY, 2022, 2026, "vendors_J998_J999_navy_fy22-26"),
        (["J019", "J020"], NAVY, 2022, 2026, "vendors_J019_J020_navy_fy22-26"),
        (["K019", "K020", "N019", "N020"], NAVY, 2022, 2026, "vendors_mod_install_navy_fy22-26"),
        (["J998", "J999"], CG, 2022, 2026, "vendors_J998_J999_dhs_fy22-26"),
    ]
    for psc, agency, fy_s, fy_e, label in vendor_queries:
        log.info(f"Vendors: {label}")
        try:
            data = spending_by_recipient(psc, agency_id=agency, fy_start=fy_s, fy_end=fy_e, limit=50)
            save(data, USA_DIR / f"{label}.json", label)
        except Exception as e:
            log.error(f"FAILED {label}: {e}")
        time.sleep(0.3)

    # --- Top awards with agency filter ---
    award_queries = [
        (["J998"], None, NAVY, 2024, 2024, 3, "awards_J998_navy_fy24"),
        (["J998"], None, NAVY, 2023, 2023, 3, "awards_J998_navy_fy23"),
        (None, ["CMAV"], NAVY, 2022, 2026, 3, "awards_CMAV_navy_fy22-26"),
        (["J998", "J999"], None, CG, 2022, 2026, 3, "awards_J998_J999_dhs_fy22-26"),
    ]
    for psc, kw, agency, fy_s, fy_e, pages, label in award_queries:
        outfile = str(USA_DIR / f"{label}.json")
        if Path(outfile).exists() and Path(outfile).stat().st_size > 100:
            log.info(f"SKIP {label} — already exists")
            continue
        log.info(f"Awards: {label}")
        try:
            spending_by_award(
                psc_codes=psc, keywords=kw, agency_id=agency,
                fy_start=fy_s, fy_end=fy_e, max_pages=pages,
                output_file=outfile, query_batch=label,
            )
        except Exception as e:
            log.error(f"FAILED {label}: {e}")
        time.sleep(0.5)

    log.info("Re-run complete.")

if __name__ == "__main__":
    main()
