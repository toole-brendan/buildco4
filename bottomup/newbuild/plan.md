# Plan: Newbuilds / New Construction TAM Channel — Taxonomy Discovery

## Context
Expanding the TAM analysis to include **new vessel construction** (Navy + Coast Guard). Before sizing this market, need to understand how construction contracts are actually described, categorized, and coded in federal procurement data. Taxonomy discovery first, market sizing second.

## The Core Question
How does DoD/DHS describe and categorize new ship construction in awards? What are the natural sub-categories? How should this channel sit alongside the existing 6 in-service buckets?

## Approach: USAspending-Only Discovery Pulls

USAspending only — FPDS is too slow (10 records/page) for a discovery phase. USAspending gives us descriptions, PSC codes, NAICS codes, award amounts, and vendor names, which is enough to understand the taxonomy. Can always follow up with targeted FPDS pulls later if needed.

### Phase 1: Discovery Pulls (understand the language)

**Goal:** Pull a representative sample of new construction awards and study how they're described, what PSC/NAICS codes appear, and what natural groupings emerge.

#### 1A. USAspending Keyword Searches — Navy Programs
Run `spending_by_award` for each keyword group (contracts `["A","B","C","D"]` + IDVs separately):

| Keyword Group | Rationale |
|---------------|-----------|
| `["construction of DDG"]` | DDG-51 Arleigh Burke construction |
| `["DDG 51"]` | Broader DDG-51 catch (includes mods, but we'll see descriptions) |
| `["Virginia class submarine"]` | SSN construction |
| `["Columbia class submarine"]` | SSBN construction |
| `["FFG 62"]` | Constellation-class frigate |
| `["Constellation class"]` | Frigate alternate name |
| `["LPD flight II"]` | San Antonio-class amphibious |
| `["LHA replacement"]` | America-class amphibious |
| `["detail design and construction"]` | Standard DD&C contract phrasing |
| `["ship construction"]` | Broad construction catch |
| `["advance procurement"]` (with Navy agency filter) | Long-lead materials |
| `["CVN 78"]` | Ford-class carrier |
| `["CVN 79"]` | Kennedy carrier |
| `["CVN 80"]` | Enterprise carrier |
| `["T-AO"]` | Fleet oiler |

#### 1B. USAspending Keyword Searches — Coast Guard Programs
| Keyword Group | Rationale |
|---------------|-----------|
| `["national security cutter"]` | NSC program |
| `["offshore patrol cutter"]` | OPC program |
| `["fast response cutter"]` | FRC program |
| `["polar security cutter"]` | Icebreaker program |
| `["cutter construction"]` | Broad CG construction catch |

#### 1C. USAspending PSC Code Searches
Run `spending_by_award` filtered by PSC codes in the 19xx range (ships/small craft) with Navy/DHS agency filter:
- PSC `1905` — Combat ships
- PSC `1910` — Transport vessels
- PSC `1915` — Patrol craft
- PSC `1920` — Service craft
- PSC `1925` — Special purpose vessels
- PSC `1930` — Barges
- PSC `1940` — Small craft
- PSC `1950` — Floating dry docks

Also run `spending_over_time` for PSC 19xx codes to get FY trend data.

#### 1D. USAspending Spending Trends
Run `spending_over_time` with keyword groups for FY-level trend data:
- `["ship construction"]`, `["submarine construction"]`, `["DDG construction"]`
- `["advance procurement"]` (Navy filter)

### Phase 2: Analyze the Results

After pulling data, analyze:
1. **Description patterns** — What verbs/nouns do contracting officers use? (e.g., "CONSTRUCTION OF DDG 51 CLASS SHIPS", "DETAIL DESIGN AND CONSTRUCTION", "ADVANCE PROCUREMENT FOR...")
2. **PSC code distribution** — Which PSC codes dominate? Is it product codes (19xx) or service codes?
3. **Contract structure** — Are construction contracts structured as definitive contracts (D), IDVs, or something else?
4. **Sub-categories that emerge naturally** from the data:
   - Full ship DD&C (detail design & construction)
   - Advance procurement / long-lead materials
   - Government-furnished equipment (GFE) / combat systems
   - Change orders / engineering change proposals on construction contracts
   - Completion of prior-year shipbuilding
   - Conversion (different from newbuild?)
5. **Vendor landscape** — Who holds the prime contracts?
6. **Dollar magnitudes** — What's the scale per program?

### Phase 3: Propose Taxonomy Integration

Based on findings, propose:
- Sub-categories within a "New Construction" bucket
- How it sits alongside the existing 6 in-service buckets (Bucket 0? Separate axis?)
- Where the boundaries are (e.g., post-shakedown availability — construction or in-service?)
- Crosswalk to SCN budget book line items

## Implementation

### Script: `run_newbuild_discovery.py`
New script in `bottomup/scripts/` that:
1. Uses existing `fpds_client.py` and `usaspending_client.py`
2. Runs the discovery queries above
3. Saves raw results to `bottomup/bronze/newbuild/`
4. Produces a summary report showing:
   - Sample descriptions (first 50-100 unique descriptions)
   - PSC code frequency distribution
   - NAICS code frequency distribution
   - Award type distribution
   - Top vendors
   - FY trend data
   - Suggested sub-categories based on description clustering

### Output Files
```
bottomup/bronze/newbuild/
  usaspending/
    awards_kw_*.json          (keyword search results)
    awards_psc_*.json         (PSC code search results)
    trend_*.json              (FY spending trends)
  newbuild_discovery_report.md   <-- the key output
```

### Estimated API Budget
- USAspending: ~80-100 API calls total (20 keyword groups x 2 award type groups + PSC queries + trends). ~10-15 min.
- FPDS: Skipped for discovery. Can do targeted FPDS follow-ups later.
- SAM.gov: Not needed (construction programs are well-established, not pipeline).

### Key Precautions
- USAspending keyword matching is noisy — post-filter every result by description regex.
- Award type codes cannot be mixed across groups (contracts vs IDVs are separate calls).
- "Advance procurement" is extremely broad without agency filter — always filter to Navy/DHS.
- Nuclear programs (Columbia, Virginia) may have limited visibility in public data.
- Some results will include in-service work (mods, repairs) mixed with construction — the point is to see what shows up and learn to separate them.

## Verification
- Cross-reference PSC codes found against the PSC manual
- Compare total dollar values against SCN budget book P-1 exhibit ($20.8B FY26 request)
- Confirm known programs (DDG-51, Virginia, Columbia, FFG-62, LPD, CVN, T-AO) all appear
- Spot-check that post-filtering removes in-service/repair awards from construction results
