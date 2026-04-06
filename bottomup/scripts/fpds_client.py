"""
FPDS Atom Feed client.
Handles XML parsing, pagination, and all three record types.
"""
from __future__ import annotations

import time
import json
import logging
from urllib.request import urlopen, Request
from urllib import parse
from xml.etree.ElementTree import ElementTree, fromstring
from pathlib import Path

from shared_utils import append_records_to_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BASE_URL = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}

PAGE_DELAY = 0.35          # seconds between pages
BATCH_PAUSE_EVERY = 5      # extra pause every N pages
BATCH_PAUSE_SECS = 1.5
USER_AGENT = "BuildCo-TAM-Analyzer/1.0"
MAX_RETRIES = 3


# ---------------------------------------------------------------------------
# XML parsing
# ---------------------------------------------------------------------------

def _text(elem, xpath: str) -> str | None:
    node = elem.find(xpath, NS)
    return node.text.strip() if node is not None and node.text else None


def _attr(elem, xpath: str, attr: str) -> str | None:
    node = elem.find(xpath, NS)
    return node.get(attr) if node is not None else None


def _float(elem, xpath: str) -> float | None:
    val = _text(elem, xpath)
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _detect_record_type(content_elem):
    """Return (record_element, record_type_string)."""
    award = content_elem.find(".//ns1:award", NS)
    if award is not None:
        return award, "award"
    idv = content_elem.find(".//ns1:IDV", NS)
    if idv is not None:
        return idv, "IDV"
    ot_award = content_elem.find(".//ns1:OtherTransactionAward", NS)
    if ot_award is not None:
        return ot_award, "OtherTransactionAward"
    ot_idv = content_elem.find(".//ns1:OtherTransactionIDV", NS)
    if ot_idv is not None:
        return ot_idv, "OtherTransactionIDV"
    return None, None


def _piid_xpath(record_type: str) -> str:
    if record_type == "OtherTransactionAward":
        return ".//ns1:OtherTransactionAwardContractID/ns1:PIID"
    if record_type == "OtherTransactionIDV":
        return ".//ns1:OtherTransactionIDVContractID/ns1:PIID"
    if record_type == "IDV":
        return ".//ns1:IDVID/ns1:PIID"
    return ".//ns1:awardContractID/ns1:PIID"


def parse_record(elem, record_type: str, query_batch: str) -> dict:
    piid_path = _piid_xpath(record_type)
    rec = {
        "source": "FPDS",
        "piid": _text(elem, piid_path),
        "mod_number": _text(elem, ".//ns1:modNumber"),
        "parent_idv_piid": _text(elem, ".//ns1:referencedIDVID/ns1:PIID"),
        "vendor_name": _text(elem, ".//ns1:vendorName"),
        "vendor_uei": _text(elem, ".//ns1:vendorAlternateName"),
        "description": _text(elem, ".//ns1:descriptionOfContractRequirement"),
        "psc_code": _text(elem, ".//ns1:productOrServiceCode"),
        "psc_description": _attr(elem, ".//ns1:productOrServiceCode", "description"),
        "naics_code": _text(elem, ".//ns1:principalNAICSCode"),
        "naics_description": _attr(elem, ".//ns1:principalNAICSCode", "description"),
        "obligated_amount": _float(elem, ".//ns1:obligatedAmount"),
        "total_obligated": _float(elem, ".//ns1:totalObligatedAmount"),
        "base_exercised_options": _float(elem, ".//ns1:totalBaseAndExercisedOptionsValue"),
        "base_all_options": _float(elem, ".//ns1:totalBaseAndAllOptionsValue"),
        "contract_action_type": _text(elem, ".//ns1:contractActionType"),
        "contract_action_desc": _attr(elem, ".//ns1:contractActionType", "description"),
        "contract_pricing_type": _text(elem, ".//ns1:typeOfContractPricing"),
        "contract_pricing_desc": _attr(elem, ".//ns1:typeOfContractPricing", "description"),
        "extent_competed": _text(elem, ".//ns1:extentCompeted"),
        "extent_competed_desc": _attr(elem, ".//ns1:extentCompeted", "description"),
        "signed_date": _text(elem, ".//ns1:signedDate"),
        "effective_date": _text(elem, ".//ns1:effectiveDate"),
        "completion_date": _text(elem, ".//ns1:currentCompletionDate"),
        "ultimate_completion_date": _text(elem, ".//ns1:ultimateCompletionDate"),
        "fiscal_year": _text(elem, ".//ns1:fiscalYear"),
        "contracting_agency_id": _text(elem, ".//ns1:contractingOfficeAgencyID"),
        "contracting_agency_name": _attr(elem, ".//ns1:contractingOfficeAgencyID", "name"),
        "contracting_office_name": _attr(elem, ".//ns1:contractingOfficeID", "name"),
        "funding_agency_name": _attr(elem, ".//ns1:fundingRequestingAgencyID", "name"),
        "funding_office_name": _attr(elem, ".//ns1:fundingRequestingOfficeID", "name"),
        "record_type": record_type,
        "query_batch": query_batch,
    }
    # OT-specific fields
    if record_type.startswith("OtherTransaction"):
        rec["ot_agreement_type"] = _text(elem, ".//ns1:typeOfAgreement")
    else:
        rec["ot_agreement_type"] = None
    return rec


# ---------------------------------------------------------------------------
# Pagination helpers
# ---------------------------------------------------------------------------

def _get_total_from_last_link(root) -> int | None:
    """Parse <link rel='last'> to estimate total records."""
    for link in root.findall("a:link", NS):
        if link.get("rel") == "last":
            href = link.get("href", "")
            for part in href.split("&"):
                if part.startswith("start="):
                    try:
                        return int(part.split("=")[1]) + 10
                    except ValueError:
                        pass
    return None


def _fetch_page(query: str, start: int) -> ElementTree:
    """Fetch a single FPDS page with retry."""
    encoded = parse.urlencode({"q": query})
    url = f"{BASE_URL}&{encoded}&start={start}"
    for attempt in range(MAX_RETRIES):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
            return fromstring(data)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)
                log.warning(f"Retry {attempt+1} for start={start}: {e}. Waiting {wait}s")
                time.sleep(wait)
            else:
                raise


# ---------------------------------------------------------------------------
# Main pull function
# ---------------------------------------------------------------------------

def pull_fpds(query: str, output_file: str, query_batch: str,
              max_records: int | None = None) -> dict:
    """
    Pull all records matching `query` from FPDS Atom Feed.
    Writes JSON incrementally to `output_file`.
    Returns stats dict.
    """
    stats = {
        "query": query,
        "query_batch": query_batch,
        "output_file": output_file,
        "total_estimated": None,
        "records_fetched": 0,
        "pages_fetched": 0,
        "record_types": {"award": 0, "IDV": 0, "OtherTransactionAward": 0, "OtherTransactionIDV": 0},
        "errors": [],
    }

    # First page — get total count
    try:
        root = _fetch_page(query, 0)
    except Exception as e:
        stats["errors"].append(f"Failed first page: {e}")
        log.error(f"[{query_batch}] Failed first page: {e}")
        return stats

    total = _get_total_from_last_link(root)
    stats["total_estimated"] = total
    log.info(f"[{query_batch}] Estimated total: {total}")

    if total is not None and total == 0:
        log.info(f"[{query_batch}] Zero results, skipping.")
        return stats

    # Process first page
    page_records = _parse_entries(root, query_batch)
    if page_records:
        append_records_to_json(output_file, page_records)
    stats["records_fetched"] += len(page_records)
    stats["pages_fetched"] += 1
    for r in page_records:
        rt = r.get("record_type", "award")
        if rt in stats["record_types"]:
            stats["record_types"][rt] += 1

    if total is None or total <= 10:
        log.info(f"[{query_batch}] Done. {stats['records_fetched']} records.")
        return stats

    # Determine upper bound
    upper = total
    if max_records is not None:
        upper = min(total, max_records)

    # Paginate
    start = 10
    while start < upper:
        if stats["pages_fetched"] % BATCH_PAUSE_EVERY == 0:
            time.sleep(BATCH_PAUSE_SECS)
        else:
            time.sleep(PAGE_DELAY)

        try:
            root = _fetch_page(query, start)
            page_records = _parse_entries(root, query_batch)
            if page_records:
                append_records_to_json(output_file, page_records)
            stats["records_fetched"] += len(page_records)
            stats["pages_fetched"] += 1
            for r in page_records:
                rt = r.get("record_type", "award")
                if rt in stats["record_types"]:
                    stats["record_types"][rt] += 1

            if stats["pages_fetched"] % 50 == 0:
                log.info(f"[{query_batch}] Progress: {stats['records_fetched']}/{upper} records, page {stats['pages_fetched']}")

            # If page returned zero entries, we're done
            if len(page_records) == 0:
                log.info(f"[{query_batch}] Empty page at start={start}, stopping.")
                break

        except Exception as e:
            stats["errors"].append(f"Page start={start}: {e}")
            log.error(f"[{query_batch}] Error at start={start}: {e}")

        start += 10

    log.info(f"[{query_batch}] Complete. {stats['records_fetched']} records in {stats['pages_fetched']} pages.")
    return stats


def _parse_entries(root, query_batch: str) -> list[dict]:
    records = []
    for entry in root.findall("a:entry", NS):
        content = entry.find("a:content", NS)
        if content is None:
            continue
        elem, record_type = _detect_record_type(content)
        if elem is None:
            continue
        rec = parse_record(elem, record_type, query_batch)
        records.append(rec)
    return records
