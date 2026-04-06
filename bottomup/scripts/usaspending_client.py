"""
USAspending API client for bottom-up TAM analysis.
Handles spending_over_time, spending_by_award, and spending_by_category endpoints.
"""
from __future__ import annotations

import json
import time
import logging
from urllib.request import urlopen, Request
from pathlib import Path

from shared_utils import append_records_to_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BASE_URL = "https://api.usaspending.gov/api/v2"
MAX_RETRIES = 3
RETRY_DELAY = 2.0
PAGE_DELAY = 0.5


def _post(endpoint: str, payload: dict) -> dict:
    """POST JSON to USAspending API with retry."""
    url = f"{BASE_URL}/{endpoint}"
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(MAX_RETRIES):
        try:
            req = Request(url, data=body, headers={
                "Content-Type": "application/json",
                "User-Agent": "BuildCo-TAM-Analyzer/1.0",
            })
            with urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_DELAY * (2 ** attempt)
                log.warning(f"Retry {attempt+1} for {endpoint}: {e}. Waiting {wait}s")
                time.sleep(wait)
            else:
                raise


# ---------------------------------------------------------------------------
# spending_over_time — FY-level obligation totals by PSC group
# ---------------------------------------------------------------------------

def spending_over_time(
    psc_codes: list[str],
    agency_id: str | None = None,
    fy_start: int = 2017,
    fy_end: int = 2026,
    group: str = "fiscal_year",
) -> list[dict]:
    """
    Get FY-level spending totals for given PSC codes.
    Returns list of {fiscal_year, aggregated_amount} dicts.
    """
    filters = {
        "psc_codes": psc_codes,
        "time_period": [
            {"start_date": f"{fy - 1}-10-01", "end_date": f"{fy}-09-30"}
            for fy in range(fy_start, fy_end + 1)
        ],
    }
    if agency_id:
        filters["agencies"] = [
            {"type": "awarding", "tier": "subtier", "name": agency_id}
        ]

    payload = {"group": group, "filters": filters}
    resp = _post("search/spending_over_time/", payload)
    results = resp.get("results", [])
    return [
        {
            "fiscal_year": r.get("time_period", {}).get("fiscal_year"),
            "aggregated_amount": r.get("aggregated_amount"),
        }
        for r in results
    ]


# ---------------------------------------------------------------------------
# spending_by_category/recipient — vendor breakdowns
# ---------------------------------------------------------------------------

def spending_by_recipient(
    psc_codes: list[str],
    agency_id: str | None = None,
    fy_start: int = 2022,
    fy_end: int = 2026,
    limit: int = 50,
) -> list[dict]:
    """
    Get top recipients (vendors) for given PSC codes.
    Returns list of {name, amount, id} dicts.
    """
    filters = {
        "psc_codes": psc_codes,
        "time_period": [
            {"start_date": f"{fy - 1}-10-01", "end_date": f"{fy}-09-30"}
            for fy in range(fy_start, fy_end + 1)
        ],
    }
    if agency_id:
        filters["agencies"] = [
            {"type": "awarding", "tier": "subtier", "name": agency_id}
        ]

    payload = {
        "category": "recipient",
        "filters": filters,
        "limit": limit,
        "page": 1,
    }
    resp = _post("search/spending_by_category/recipient/", payload)
    results = resp.get("results", [])
    return [
        {
            "name": r.get("name"),
            "amount": r.get("amount"),
            "recipient_id": r.get("id"),
        }
        for r in results
    ]


# ---------------------------------------------------------------------------
# spending_by_award — individual award detail
# ---------------------------------------------------------------------------

def spending_by_award(
    psc_codes: list[str] | None = None,
    keywords: list[str] | None = None,
    agency_id: str | None = None,
    fy_start: int = 2022,
    fy_end: int = 2026,
    award_type_codes: list[str] | None = None,
    limit: int = 100,
    max_pages: int = 5,
    output_file: str | None = None,
    query_batch: str = "",
) -> list[dict]:
    """
    Get individual awards. Paginates up to max_pages.
    award_type_codes: ["A","B","C","D"] for contracts (not IDVs which show $0).
    """
    if award_type_codes is None:
        award_type_codes = ["A", "B", "C", "D"]

    filters = {
        "award_type_codes": award_type_codes,
        "time_period": [
            {"start_date": f"{fy - 1}-10-01", "end_date": f"{fy}-09-30"}
            for fy in range(fy_start, fy_end + 1)
        ],
    }
    if psc_codes:
        filters["psc_codes"] = psc_codes
    if keywords:
        filters["keywords"] = keywords
    if agency_id:
        filters["agencies"] = [
            {"type": "awarding", "tier": "subtier", "name": agency_id}
        ]

    fields = [
        "Award ID", "Recipient Name", "Description", "Award Amount",
        "Total Outlays", "Contract Award Type", "Start Date", "End Date",
        "Awarding Agency", "Awarding Sub Agency", "NAICS Code", "PSC Code",
    ]

    all_records = []
    for page in range(1, max_pages + 1):
        payload = {
            "filters": filters,
            "fields": fields,
            "limit": limit,
            "page": page,
            "sort": "Award Amount",
            "order": "desc",
        }
        resp = _post("search/spending_by_award/", payload)
        results = resp.get("results", [])
        if not results:
            break

        records = []
        for r in results:
            records.append({
                "source": "USASPENDING",
                "award_id": r.get("Award ID"),
                "vendor_name": r.get("Recipient Name"),
                "description": r.get("Description"),
                "award_amount": r.get("Award Amount"),
                "total_outlays": r.get("Total Outlays"),
                "contract_award_type": r.get("Contract Award Type"),
                "start_date": r.get("Start Date"),
                "end_date": r.get("End Date"),
                "awarding_agency": r.get("Awarding Agency"),
                "awarding_sub_agency": r.get("Awarding Sub Agency"),
                "naics_code": r.get("NAICS Code"),
                "psc_code": r.get("PSC Code"),
                "query_batch": query_batch,
            })
        all_records.extend(records)

        if output_file:
            append_records_to_json(output_file, records)

        has_next = resp.get("page_metadata", {}).get("hasNext", False)
        if not has_next:
            break
        time.sleep(PAGE_DELAY)

    log.info(f"[{query_batch}] spending_by_award: {len(all_records)} records")
    return all_records


# ---------------------------------------------------------------------------
# spending_over_time with keywords (for RCOH/SLEP trending)
# ---------------------------------------------------------------------------

def spending_over_time_keywords(
    keywords: list[str],
    agency_id: str | None = None,
    fy_start: int = 2017,
    fy_end: int = 2026,
    award_type_codes: list[str] | None = None,
) -> list[dict]:
    """
    Get FY-level spending totals for keyword searches.
    """
    if award_type_codes is None:
        award_type_codes = ["A", "B", "C", "D"]

    filters = {
        "keywords": keywords,
        "award_type_codes": award_type_codes,
        "time_period": [
            {"start_date": f"{fy - 1}-10-01", "end_date": f"{fy}-09-30"}
            for fy in range(fy_start, fy_end + 1)
        ],
    }
    if agency_id:
        filters["agencies"] = [
            {"type": "awarding", "tier": "subtier", "name": agency_id}
        ]

    payload = {"group": "fiscal_year", "filters": filters}
    resp = _post("search/spending_over_time/", payload)
    results = resp.get("results", [])
    return [
        {
            "fiscal_year": r.get("time_period", {}).get("fiscal_year"),
            "aggregated_amount": r.get("aggregated_amount"),
        }
        for r in results
    ]
