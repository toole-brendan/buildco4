# Bottom-Up TAM Analysis — Attempt Log & Roadblocks

## What We Tried

We attempted to execute Phase 0 (setup) and Phase 1 (FPDS Bronze data pull) of the bottom-up implementation plan. The goal was to pull contract-level data from the FPDS Atom Feed for all six in-service vessel work buckets, starting with PSC-code-based queries for Navy and Coast Guard.

## What We Built

All tooling was built and is functional in `bottomup/scripts/`:

- **`fpds_client.py`** — Full FPDS Atom Feed client with XML parsing, pagination, retry logic, and support for all four record types (award, IDV, OtherTransactionAward, OtherTransactionIDV).
- **`shared_utils.py`** — Master description regex for ship work classification, vendor name normalizer, JSON file helpers, fiscal year utilities.
- **`run_phase1_fpds.py`** — Query runner with resume support, stats collection, and automatic summary generation.

The scripts work correctly. We validated them with probe queries and a full FY24 J998 pull (3,991 records).

## The Data Volume Problem

The FPDS Atom Feed returns 10 records per page with no bulk download option. Here's what we discovered about actual volumes:

| Query | FY Range | Estimated Records | Time to Pull |
|-------|----------|-------------------|--------------|
| J998 Navy | FY22-26 | ~17,000 | ~26 min |
| J999 Navy | FY22-26 | ~26,500 | ~40 min |
| J019 Navy | FY22-26 | ~5,000 | ~8 min |
| J020 Navy | FY22-26 | ~4,000 | ~6 min |
| K019 Navy | FY22-26 | ~700 | ~1 min |
| N019 Navy | FY22-26 | ~700 | ~1 min |
| J998 CG | FY22-26 | ~500-1,000 | ~2 min |
| J999 CG | FY22-26 | ~300-500 | ~1 min |
| **Stratum 1 subtotal** | | **~55,000** | **~85 min** |
| 3 keyword gap-fillers | FY22-26 | ~1,000-2,000 | ~5 min |
| **Total** | | **~57,000** | **~90 min** |

We had already trimmed the original plan substantially:
- Narrowed from FY20-FY26 to FY22-FY26 (dropped 2 years)
- Cut from 32 queries to 11
- Deferred all vendor-specific pulls (Stratum 3)
- Dropped R425, R408, M2AA (noisy PSCs needing heavy post-filtering)

Even after trimming, the pull takes ~90 minutes of continuous API requests at 10 records/page with 0.35s politeness delays. The original uncut plan would have been 2+ hours.

## What We Successfully Captured

Before halting, we did complete two pulls:

| File | Records | Status |
|------|---------|--------|
| `psc_J998_navy_fy22-26.json` | 17,025 | Complete |
| `psc_J999_navy_fy22-26.json` | 6,950 | Partial (killed mid-pull; estimated ~26,500 total) |

These are stored in `bottomup/bronze/fpds/` and contain full Bronze schema fields (PIID, vendor, description, dollar amounts, PSC, NAICS, contract type, pricing, competition level, dates, etc.).

## Technical Issues Discovered & Solved

### 1. FPDS IDV record type (critical bug, fixed)

The FPDS Atom Feed returns four XML record types, not three:
- `<ns1:award>` — standard FAR contract actions
- `<ns1:IDV>` — indefinite-delivery vehicles (IDIQs, BOAs, BPAs)
- `<ns1:OtherTransactionAward>` — OT awards
- `<ns1:OtherTransactionIDV>` — OT umbrella agreements

The implementation plan and federal procurement guide only documented three types (missing `IDV`). Our initial parser only handled `award` + two OT types, causing it to skip IDV pages and falsely detect "empty pages" mid-pagination. For J998 FY24, this made us capture only 338 of ~4,000 actual records.

**Fix:** Added `IDV` detection with its own PIID xpath (`.//ns1:IDVID/ns1:PIID`). After the fix, pagination runs cleanly to the end.

### 2. FPDS "last" link over-reports total count

The `<link rel="last">` element in FPDS Atom responses reports a `start=` value that overestimates actual record count (likely includes deleted/inactive records). For J998 FY24, "last" said ~4,000 but actual content was 3,991. For multi-year ranges, the overestimate can be larger. This is cosmetic — the parser correctly stops when no more entries are returned.

### 3. Python 3.9 type hint compatibility

The `str | None` union syntax requires Python 3.10+. Fixed with `from __future__ import annotations`.

## Options for Moving Forward

### Option A: Let it run (simplest)
Run the full Phase 1 script as-is. It takes ~90 min but is fully automated with resume support (skips already-completed files). Walk away and come back.

### Option B: Use FPDS bulk data instead
Download the full FPDS database XML dump from data.gov. Multi-gigabyte files but eliminates the pagination bottleneck entirely. Requires building a different parser but gives access to the complete dataset. Better for truly comprehensive analysis.

### Option C: Use USAspending bulk download
download.usaspending.gov provides full database dumps by agency and fiscal year. Monthly updates. More efficient than API pagination for large-scale analysis. Downside: USAspending loses some FPDS fidelity (no OT record types, PSC often null at award level).

### Option D: Hybrid — USAspending API for trends, FPDS for targeted pulls
Use USAspending `spending_over_time` endpoint (fast, ~1 call per PSC group) for FY-level trend data and market sizing. Use USAspending `spending_by_award` for top-contract detail. Only use FPDS for targeted pulls where description-level precision matters (RCOH, SLEP, etc.). This gives 80% of the analytical value in 10% of the time.

### Option E: Skip bottom-up record-level pulls entirely
Size the bottom-up TAM using only USAspending aggregation endpoints (`spending_over_time` by PSC code), which are fast (seconds per call). Accept that you get FY-level totals and top-vendor lists but not record-level classification into the six buckets. Cross-reference against top-down budget numbers for validation.

## Recommendation

**Option D is probably the sweet spot.** The six-bucket classification is most defensible when done top-down from budget books anyway (the budget structure maps cleanly to the buckets). Bottom-up's main value is (1) vendor landscape, (2) competition analysis, and (3) validating top-down totals — all of which USAspending aggregate endpoints handle well. Reserve FPDS record-level pulls for the small-volume, high-value queries (RCOH, SLEP, specific vendor deep-dives) where description parsing actually matters.
