# Bottom-Up TAM Analysis — Implementation Plan

## Objective

Size each of the six in-service vessel work buckets from the bottom up using federal contract and award data. The output is a bucket-by-bucket obligated-spend table with FY columns, vendor breakdowns, and confidence notes.

---

## The Six Buckets (same taxonomy as top-down)

| # | Bucket | Primary Contract Signals |
|---|--------|--------------------------|
| 1 | Scheduled Depot Maintenance & Repair | PSC J998/J999, availability types (DSRA, DMP, SRA, PIA, DPIA, etc.), hull designations |
| 2 | Continuous / Intermediate / Emergent | CMAV, ERATA, ORATA, emergent repair, voyage repair, RMC contracts |
| 3 | Modernization & Alteration Installation | PSC K019/K020/N019/N020, "modernization", "alteration", "backfit", "retrofit", DDG Mod, SEWIP, CANES |
| 4 | Major Life-Cycle Events (RCOH/SLEP/MMA) | RCOH, EOH, SLEP, MMA, SCN-funded, CG ISVS programs |
| 5 | Sustainment Engineering / Planning | PSC R425/R408/L019/L020, SETA, lifecycle support, planning, DMSMS, SUPSHIP |
| 6 | Availability Support / Port Services | PSC M2xx, berthing, crane, tug, pilot, husbanding, shore power, scaffolding |

---

## Data Sources

| Priority | Source | Auth | Role |
|----------|--------|------|------|
| 1 | FPDS Atom Feed | None (public) | Primary. Most complete, authoritative, has OT records, description-level search. |
| 2 | USAspending API | None (public) | Supplementary. Aggregated views, FY trends, recipient rollups. |

---

## API Findings from Probe Testing

### FPDS Atom Feed

| Finding | Detail |
|---------|--------|
| **Speed** | Excellent — 0.07-0.14s per page (10 records/page) |
| **CRITICAL GOTCHA** | `AGENCY_CODE:"1700"` silently returns zero when combined with `SIGNED_DATE` ranges. **Must use `CONTRACTING_AGENCY_ID:1700`** for Navy filtering with dates. |
| **J998 volume** | ~4,000 records for Navy in FY24 alone. Full FY20-FY26 pull = ~25,000+ records. |
| **Description quality** | Rich — references specific ship names, hull numbers, availability types. High value for bucket classification. |
| **Record types** | All standard `award` in Navy FY24 probes. No OT records surfaced for ship repair (expected — ship repair uses traditional contracting). |
| **CMAV volume** | ~700 records in FY24 — good coverage of Bucket 2 |
| **Husbanding (M2AA)** | Only 6 Navy results in FY24. Most M2AA is non-Navy. Bucket 6 may need keyword search instead of PSC. |
| **Vendor search** | `VENDOR_NAME:"BAE SYSTEMS"` works. ~2,690 Navy results in FY24 (need post-filtering to ship work). |
| **Correct query template** | `PRODUCT_OR_SERVICE_CODE:{code} CONTRACTING_AGENCY_ID:1700 SIGNED_DATE:[2023/10/01,2024/09/30]` |

### USAspending API

| Finding | Detail |
|---------|--------|
| **Speed** | 0.4-0.6s for simple queries, 4-5s for aggregations |
| **PSC filter syntax** | Must use plain array `["J998"]`, NOT `{"require": ["J998"]}` — latter returns 422 |
| **PSC Code in results** | Always returns `None` at award level — PSC is transaction-level, lost in award aggregation |
| **IDV dollar amounts** | Always $0. Dollars live on delivery orders. Query contracts (A/B/C/D) for dollar analysis. |
| **J998+J999 trend** | FY18: $4.2B, FY19: $3.5B, FY20: $4.1B, FY21: $3.9B, FY22: $3.5B, FY23: $4.0B, FY24: $4.1B |
| **Keyword "DSRA"** | Near-zero false positives — highly precise filter |
| **Keyword "ship repair"** | Good relevance but broader; needs post-filtering |
| **Top recipients (J998 FY24)** | Metro Machine $387M, NASSCO $385M, Marine Hydraulics $151M, Detyens $111M, BAE Norfolk $109M — all correct |
| **Vendor name dedup** | "Metro Machine Corp." vs "Metro Machine Corp" appear as separate entries. Must normalize. |

---

## Medallion Architecture (mirrors top-down)

| Layer | What Happens | Output |
|-------|-------------|--------|
| **Bronze** | Raw contract data pulled from APIs, stored as JSON (handles messy descriptions, variable OT fields). No filtering, no bucket assignment. | `bottomup/bronze/` (JSON files) + summary .md files |
| **Silver** | Post-filter by description regex, deduplicate (PIID + mod), normalize vendors, assign bucket + confidence. Output as CSV — data is now flat and clean. | `bottomup/silver_canonical.csv` + `bottomup/silver_summary.md` |
| **Gold** | Aggregate by bucket/FY/vendor/performer. Produce TAM table, vendor landscape. | `bottomup/gold_tam_table.md`, `bottomup/gold_vendor_landscape.md`, `bottomup/gold_confidence_and_gaps.md`, `bottomup/tam_bottomup_summary.md` |

---

## Bronze JSON Schema

All FPDS and USAspending records are stored as JSON in Bronze. JSON is the right format here because FPDS descriptions contain commas/quotes/newlines that make CSV fragile, OT records have extra fields that standard awards lack, and modification histories are variable-depth. The Silver layer converts to CSV once the data is clean and flat.

Each Bronze JSON file is a JSON array of record objects. One file per query batch.

### FPDS record fields

| Column | Source Field | Notes |
|--------|-------------|-------|
| `source` | — | Always "FPDS" |
| `piid` | `awardContractID/PIID` (or OT equivalent) | Primary key for dedup |
| `mod_number` | `modNumber` | For dedup: keep latest mod per PIID |
| `parent_idv_piid` | `referencedIDVID/PIID` | Parent IDIQ/BOA if delivery order |
| `vendor_name` | `vendorName` | Raw; normalized in Silver |
| `vendor_uei` | `vendorAlternateName` or UEI field | For vendor dedup |
| `description` | `descriptionOfContractRequirement` | The key field for bucket classification |
| `psc_code` | `productOrServiceCode` | PSC code (e.g., J998) |
| `psc_description` | `productOrServiceCode/@description` | PSC text label |
| `naics_code` | `principalNAICSCode` | 6-digit NAICS |
| `naics_description` | `principalNAICSCode/@description` | NAICS text label |
| `obligated_amount` | `obligatedAmount` | This action only ($) |
| `total_obligated` | `totalObligatedAmount` | Cumulative to date ($) — use this for dollar analysis |
| `base_exercised_options` | `totalBaseAndExercisedOptionsValue` | Cumulative exercised ($) |
| `base_all_options` | `totalBaseAndAllOptionsValue` | Cumulative ceiling ($) |
| `contract_action_type` | `contractActionType` | Code: A=BPA Call, B=PO, C=DO, D=Definitive |
| `contract_action_desc` | `contractActionType/@description` | Text label |
| `contract_pricing_type` | `typeOfContractPricing` | Code (e.g., J=FFP, S=Cost Plus) |
| `contract_pricing_desc` | `typeOfContractPricing/@description` | Text label (e.g., "Firm Fixed Price") |
| `extent_competed` | `extentCompeted` | Code |
| `extent_competed_desc` | `extentCompeted/@description` | Text (e.g., "Full and Open Competition", "Not Competed") |
| `signed_date` | `signedDate` | YYYY-MM-DD |
| `effective_date` | `effectiveDate` | Period of performance start |
| `completion_date` | `currentCompletionDate` | Period of performance end |
| `ultimate_completion_date` | `ultimateCompletionDate` | Including all options |
| `fiscal_year` | `fiscalYear` | FY of this action |
| `contracting_agency_id` | `contractingOfficeAgencyID` | 4-digit code |
| `contracting_agency_name` | `contractingOfficeAgencyID/@name` | Agency name |
| `contracting_office_name` | `contractingOfficeID/@name` | Office name |
| `funding_agency_name` | `fundingRequestingAgencyID/@name` | Who pays |
| `funding_office_name` | `fundingRequestingOfficeID/@name` | Funding office |
| `record_type` | — | "award", "OtherTransactionAward", or "OtherTransactionIDV" |
| `ot_agreement_type` | `typeOfAgreement` (OT only) | "PROTOTYPE" or "PRODUCTION" |
| `query_batch` | — | Which query produced this record (for audit trail) |

### USAspending record fields

| Column | Source Field | Notes |
|--------|-------------|-------|
| `source` | — | Always "USASPENDING" |
| `award_id` | `Award ID` | Primary key |
| `vendor_name` | `Recipient Name` | Raw |
| `description` | `Description` | Key field for classification |
| `award_amount` | `Award Amount` | Total award value ($) |
| `total_outlays` | `Total Outlays` | Actual spending ($) |
| `contract_award_type` | `Contract Award Type` | e.g., "DELIVERY ORDER", "DEFINITIVE CONTRACT", "IDV_B_A" |
| `start_date` | `Start Date` | |
| `end_date` | `End Date` | |
| `awarding_agency` | `Awarding Agency` | Top-tier agency |
| `awarding_sub_agency` | `Awarding Sub Agency` | Sub-tier (e.g., "Department of the Navy") |
| `naics_code` | `NAICS Code` | |
| `psc_code` | `PSC Code` | Note: often returns None at award level |
| `query_batch` | — | Audit trail |

Bronze stores these as JSON objects. In Silver, after dedup and cleaning, the data flattens to CSV via `pd.json_normalize()` → `df.to_csv()`.

---

## Phase 0: Setup

### Step 0A: Create project structure

```
bottomup/
  scripts/           # Python scripts for API pulls and processing
  bronze/            # Raw API responses as JSON
    fpds/            # FPDS JSON files per query batch
    usaspending/     # USAspending JSON files per query batch
  silver/            # Filtered, deduped, bucket-assigned CSV + summary
  gold/              # Final analysis outputs
```

### Step 0B: Build the Python tooling

Create a lightweight pull framework with:

**FPDS client:**
- XML parsing with namespace handling (`ns1="https://www.fpds.gov/FPDS"`, `a="http://www.w3.org/2005/Atom"`)
- Pagination: parse `<link rel="last">` for total count, increment `start` by 10
- Rate politeness: 0.3-0.5s delay between pages, brief pause every 5 pages
- Parse all three record types: `<ns1:award>`, `<ns1:OtherTransactionAward>`, `<ns1:OtherTransactionIDV>`
- Extract all fields from the Bronze CSV schema above, including contract_action_type, contract_pricing_type, extent_competed
- **Always use `CONTRACTING_AGENCY_ID:1700`** for Navy, never `AGENCY_CODE:"1700"` with date ranges
- No space after comma in date ranges: `[2023/10/01,2024/09/30]`
- Write JSON records to disk after every page (crash resilience) — append to JSON array file

**USAspending client:**
- JSON REST client
- PSC filter as plain array: `"psc_codes": ["J998"]`
- Request `Contract Award Type` field in all spending_by_award queries
- Separate calls per award_type_code group (contracts vs IDVs vs grants vs other)
- Skip IDV queries for dollar analysis (always $0)
- Retry with exponential backoff on 5xx
- Write JSON records incrementally per page

**Shared utilities:**
- Description regex filter (see Step 0C)
- Vendor name normalizer (strip suffixes, uppercase, alias map)
- Deduplication: latest mod per PIID for FPDS, Award ID for USAspending
- JSON-to-CSV converter for Silver output (`pd.json_normalize()` → `df.to_csv()`)

### Step 0C: Build the master description regex

```python
import re

SHIP_WORK_PATTERN = re.compile(
    r"\b("
    # Availability types (Bucket 1)
    r"DSRA|EDSRA|DOCKING SELECTED RESTRICTED|"
    r"DMP|DEPOT MODERNIZATION PERIOD|"
    r"SRA|SELECTED RESTRICTED AVAILABILITY|"
    r"D?PIA|PLANNED INCREMENTAL AVAILABILITY|"
    r"D?PMA|PHASED MAINTENANCE AVAILABILITY|"
    r"EDPMA|CIA|"
    # Continuous/emergent (Bucket 2)
    r"CMAV|CONTINUOUS MAINTENANCE|"
    r"ERATA|EMERGENT REPAIR|ORATA|VOYAGE REPAIR|"
    # Modernization (Bucket 3)
    r"SHIPALT|ORDALT|MACHALT|ALTERATION INSTALLATION|"
    r"BACKFIT|RETROFIT|TECH INSERTION|"
    r"DDG.?MOD|LCS.?MOD|IN.?SERVICE MODERNIZATION|"
    r"SEWIP|CANES|AN.SQQ.89|AN.SLQ.32|"
    # Major life-cycle (Bucket 4)
    r"RCOH|REFUELING.{0,10}OVERHAUL|"
    r"EOH|ENGINEERED OVERHAUL|"
    r"SLEP|SERVICE LIFE EXTENSION|"
    r"MMA|MAJOR MAINTENANCE AVAILABILITY|"
    # Sustainment (Bucket 5)
    r"LIFECYCLE SUPPORT|LIFE CYCLE|DMSMS|OBSOLESCENCE|"
    r"SETA|SUPSHIP|SHIP MAINTENANCE IMPROVEMENT|"
    # Support (Bucket 6)
    r"HUSBANDING|SHORE POWER|DRYDOCK SERVICE|"
    r"SCAFFOLDING|CRANE SERVICE|"
    # General ship repair
    r"SHIP REPAIR|VESSEL REPAIR|SHIP MAINTENANCE|"
    r"AVAILABILIT(?:Y|IES)"
    r")\b",
    re.IGNORECASE,
)
```

This regex is used for post-filtering. Records matching PSC J998/J999 are auto-included regardless of regex match (PSC is sufficient signal).

### Step 0D: Build the keyword and query plan

#### FPDS Query Plan

> **Design rationale — trimmed plan.** The original plan had three strata (PSC, keyword, vendor) totaling ~32 queries and ~80K records (~90 min of API time). Testing revealed that strata overlap heavily: DSRA/DMP/CMAV keyword records are already coded to J998/J999; vendor-name records are already captured by PSC pulls. The trimmed plan below keeps the high-value PSC pulls, narrows to FY22-FY26 (4 full years + YTD), and limits keyword pulls to gap-fillers that target buckets PSC codes miss. Vendor pulls are deferred to a later pass if gap analysis shows missing data.
>
> **FPDS pagination note.** The Atom Feed returns four record types: `<ns1:award>`, `<ns1:IDV>`, `<ns1:OtherTransactionAward>`, `<ns1:OtherTransactionIDV>`. All four must be parsed or pagination appears to "stop early" when IDV-only pages are encountered. The `<link rel="last">` start value overestimates true count (includes deleted/inactive records) but pagination does reach the end if all record types are handled.

**Stratum 1: PSC-based pulls (primary — captures ~90% of target data)**

| PSC Code(s) | Agency Filter | Date Range | Expected Volume | Target Bucket |
|-------------|---------------|------------|-----------------|---------------|
| J998 | CONTRACTING_AGENCY_ID:1700 | FY22-FY26 | ~15,000-20,000 | 1, 2 |
| J999 | CONTRACTING_AGENCY_ID:1700 | FY22-FY26 | ~10,000-15,000 | 1, 2 |
| J019 | CONTRACTING_AGENCY_ID:1700 | FY22-FY26 | ~3,000-4,000 | 1, 2 |
| J020 | CONTRACTING_AGENCY_ID:1700 | FY22-FY26 | ~1,000-1,500 | 1, 2 |
| K019 | CONTRACTING_AGENCY_ID:1700 | FY22-FY26 | ~500-700 | 3 |
| N019 | CONTRACTING_AGENCY_ID:1700 | FY22-FY26 | ~500-700 | 3 |
| J998 | CONTRACTING_AGENCY_ID:7000 | FY22-FY26 | ~500-1,000 | 1, 2 (CG) |
| J999 | CONTRACTING_AGENCY_ID:7000 | FY22-FY26 | ~300-500 | 1, 2 (CG) |

**Stratum 2: Keyword gap-fillers (targets buckets that PSC codes miss)**

| Keyword | Agency | Date Range | Notes |
|---------|--------|------------|-------|
| "RCOH" | 1700 | FY22-FY26 | Bucket 4 — RCOH may be coded outside J998/J999 (SCN-funded). Small volume, high value. |
| "SLEP" | 7000 | FY22-FY26 | Bucket 4 — CG service life extensions. Different contracting patterns. |
| "HUSBANDING" | 1700 | FY22-FY26 | Bucket 6 — PSC M2AA was too sparse (only 6 Navy results in FY24). Keyword is the only reliable retrieval method. |

**Stratum 3: Vendor-specific pulls — DEFERRED**

> Deferred to a later pass. Rationale: the major ship repair vendors (BAE, HII, NASSCO, GD, Vigor, Metro Machine, etc.) overwhelmingly contract under PSC J998/J999, so Stratum 1 already captures their work. Vendor pulls are useful for catching vague-description records coded to generic PSCs, but this is a marginal-return exercise best done after Silver analysis reveals specific gaps. If needed, the vendor list and query templates from the original plan remain valid.

#### USAspending Query Plan

| Query Type | Filter | Purpose |
|-----------|--------|---------|
| spending_over_time | J998+J999, FY17-FY26 | Already done in probe — $3.5-4.2B/yr trend |
| spending_over_time | J019+J020, FY17-FY26 | Component-level repair trend |
| spending_over_time | K019+N019, FY17-FY26 | Standalone mod/install trend |
| spending_by_award | J998, Navy, FY24, sorted by amount desc | Top contracts for Bucket 1 detail |
| spending_by_award | "RCOH", all agencies, FY22-FY26 | Bucket 4 contracts |
| spending_by_category/recipient | J998, FY24 | Already done — vendor landscape validation |
| spending_by_category/recipient | J998+J999, FY22-FY26 | Multi-year vendor landscape |

---

## Phase 1: Bronze — FPDS Pull

### Step 1A: PSC-based pulls (Stratum 1)

Run all 8 PSC queries from the plan above. For each:
1. Fetch page 0, parse `<link rel="last">` for estimated total
2. Paginate through all pages (start=0, 10, 20, ...), parsing all four record types (`award`, `IDV`, `OtherTransactionAward`, `OtherTransactionIDV`)
3. Extract all Bronze schema fields (including contract_action_type, contract_pricing_type, extent_competed)
4. Write JSON records to `bottomup/bronze/fpds/{psc}_{agency}_{fy_range}.json` incrementally (crash resilience)
5. Log: query string, total records, pages fetched, any errors

**Estimated pagination budget:**
- ~25,000-30,000 total records across 8 PSC queries
- ~2,500-3,000 pages at 0.35s delay = ~15-18 minutes
- With processing overhead and batch pauses: ~25-30 minutes total

### Step 1B: Keyword gap-filler pulls (Stratum 2)

Run the 3 keyword queries (RCOH, SLEP, HUSBANDING). Same parsing and JSON storage approach.
- ~1,000-2,000 total records
- ~3-5 minutes

### Step 1C: Vendor-specific pulls — DEFERRED

Not run in Phase 1. Will be triggered after Silver gap analysis if needed.

### Step 1D: Flag OT and IDV records

While parsing, `OtherTransactionAward`, `OtherTransactionIDV`, and `IDV` records are tagged in the `record_type` field and logged separately. IDV records (indefinite-delivery vehicles like IDIQs and BOAs) are expected to appear alongside awards — they represent the umbrella contract, while delivery orders (contract_action_type "C") represent the actual funded work. OT records are not expected to be a major component of ship repair but are captured for completeness.

### Bronze Output

- `bottomup/bronze/fpds/*.json` — one JSON file per query batch
- `bottomup/bronze_fpds_summary.md`:
  - Total records by query stratum (PSC / keyword)
  - Record count by PSC code
  - Record count by contract_action_type (BPA Call / PO / DO / Definitive)
  - Record count by contract_pricing_type (FFP / Cost-Plus / T&M / etc.)
  - Record count by extent_competed
  - Record count by record type (award / IDV / OT)
  - Date range coverage
  - Any errors or gaps

---

## Phase 2: Bronze — USAspending Pull

### Step 2A: Spending trends (spending_over_time)

Run for each PSC group:
- J998+J999 (done in probe: $3.5-4.2B/yr)
- J019+J020
- K019+N019
- R425+R408 (will be noisy — includes non-ship)

### Step 2B: Top contracts (spending_by_award)

Run for:
- PSC J998, Navy, FY24 — full pagination (top 100-200 by amount)
- PSC J998, Navy, FY23 — same
- Keywords "RCOH" — all agencies, FY20-FY26
- Keywords "SLEP" — all agencies, FY20-FY26

Request `Contract Award Type` field in all queries. Post-filter every result by description regex. Write to JSON.

### Step 2C: Vendor landscape (spending_by_category/recipient)

- J998, all agencies, FY22-FY24 (3 separate year queries)
- J019+J020, all agencies, FY24

### Bronze Output

- `bottomup/bronze/usaspending/*.json`
- `bottomup/bronze_usaspending_summary.md`

---

## Phase 3: Silver — Post-Filter, Deduplicate, Classify

### Step 3A: Merge FPDS and USAspending

- Load all Bronze JSON files into a single dataframe (`pd.json_normalize()`)
- FPDS is authoritative when records conflict
- Match on PIID where possible
- USAspending may surface awards FPDS keyword searches missed
- Keep FPDS record when duplicated; supplement with USAspending-only finds

### Step 3B: Post-filter by description

Apply the master regex (Step 0C) to every record's description. Rules:
- PSC J998/J999 records: **auto-include** regardless of regex match (PSC is sufficient signal)
- PSC J019/J020/K019/N019 records: include if regex matches OR description references a ship/hull
- PSC R425/R408 records: include ONLY if regex matches (these PSCs are too broad without filtering)
- PSC M2xx records: include if description references ship/vessel/port/husbanding
- Keyword-sourced and vendor-sourced records: include only if regex matches
- All excluded records retained with EXCLUDE disposition for audit

### Step 3C: Deduplicate

1. Group all records by PIID
2. For each PIID, sort by mod_number descending
3. Keep ONLY the record with the highest mod_number
4. Use `total_obligated` and `base_all_options` from this latest mod
5. **NEVER sum totals across mods** — this inflates by 5-10x

Count unique PIIDs for contract counts. Use latest-mod totals for dollar analysis.

### Step 3D: Normalize vendors

- Strip suffixes: INC, LLC, CORP, CORPORATION, CO, LTD, LP, L.P.
- Remove trailing punctuation
- Uppercase for comparison
- Apply alias map for known mergers/variants:
  - "METRO MACHINE" → "HII" (acquired)
  - "VIGOR MARINE" / "VIGOR INDUSTRIAL" → "VIGOR"
  - "GENERAL DYNAMICS NASSCO" → "GD NASSCO"
  - etc.

### Step 3E: Assign buckets

Classification priority order:

**1. Description keywords (highest priority):**

| Pattern in Description | Bucket | Confidence |
|----------------------|--------|------------|
| DSRA, EDSRA, SRA, DMP, PIA, DPIA, PMA, DPMA, EDPMA, CIA, "AVAILABILITY" + hull designation | 1 | High |
| CMAV, ERATA, ORATA, "EMERGENT", "VOYAGE REPAIR", "CONTINUOUS MAINTENANCE" | 2 | High |
| RCOH, EOH, "REFUELING OVERHAUL" | 4 | High |
| SLEP, MMA, "SERVICE LIFE EXTENSION", "MAJOR MAINTENANCE AVAILABILITY" | 4 | High |
| SHIPALT, ORDALT, MACHALT, "MODERNIZATION", "BACKFIT", "RETROFIT", "DDG MOD", "ALTERATION" | 3 | High |
| SETA, SUPSHIP, "LIFECYCLE", "PLANNING AND TECHNICAL", "DMSMS", "OBSOLESCENCE" | 5 | High |
| "HUSBANDING", "BERTHING", "SHORE POWER", "CRANE", "TUG", "PILOT SERVICE" | 6 | High |

**2. PSC code (for records with vague descriptions):**

| PSC | Default Bucket | Confidence |
|-----|---------------|------------|
| J998/J999 | 1 | Medium |
| J019/J020 | 1 | Medium |
| K019/K020 | 3 | Medium |
| N019/N020 | 3 | Medium |
| R425/R408 | 5 | Medium |
| M2xx | 6 | Medium |

**3. "Blended contract" rule:** Large availability contracts (e.g., a DMP at $300M) bundle depot repair + modernization + support. Assign full value to **Bucket 1** as primary. Tag Bucket 3 as secondary. This mirrors how contracting officers code the predominant PSC.

### Step 3F: Add Silver-specific columns

Add these columns to the Silver CSV:

| Column | Values |
|--------|--------|
| `disposition` | INCLUDE / EXCLUDE |
| `bucket_primary` | 1-6 |
| `bucket_secondary` | 1-6 or blank |
| `confidence` | High / Medium / Low |
| `vendor_normalized` | Cleaned vendor name |
| `classification_reason` | Why this bucket was assigned (e.g., "description contains DSRA", "PSC J998 default") |

### Silver Output

- `bottomup/silver_canonical.csv` — full dataset with disposition, bucket, confidence columns
- `bottomup/silver_summary.md`:
  - Disposition summary: INCLUDE / EXCLUDE counts
  - Records by bucket
  - Records by confidence tier
  - Records by contract_action_type and contract_pricing_type
  - Records by extent_competed
  - Known classification ambiguities

---

## Phase 4: Gold — Aggregate and Produce Analysis

### Step 4A: Bucket-by-bucket TAM table

Aggregate Silver INCLUDE data by bucket and fiscal year:

```
| # | Bucket | FY20 ($M) | FY21 ($M) | FY22 ($M) | FY23 ($M) | FY24 ($M) | FY25 ($M) | FY26 YTD ($M) | Trend |
```

### Step 4B: Vendor landscape

For each bucket, top-10 vendors:

```
## Bucket 1: Scheduled Depot Maintenance
| Rank | Vendor | FY24 Obligated ($M) | FY23 ($M) | Key Programs | Market Share |
```

Also produce cross-bucket vendor summary showing which companies span multiple buckets.

### Step 4C: Public vs. Private performer

Using vendor identity:
- Known public entities (if any appear — naval shipyard work is organic, not contracted) → Public
- All contract recipients → Private
- **Document that public yard work (~$7.8B per top-down) will NOT appear in contract data. This is a known and expected gap.**

### Step 4D: Contract vehicle analysis

Characterize the market by:
- Contract action type (Definitive Contract, Delivery Order, BPA Call, Purchase Order)
- Contract pricing type (FFP, Cost-Plus, T&M, etc.)
- Competition level (sole source vs. full & open vs. limited competition)
- Contract size distribution (histogram of award values)
- Geographic concentration (place of performance if available)

### Step 4E: Confidence and gaps

Document:
- What the contract data covers vs. what it misses
- Known blind spots: public yards, classified, subcontractors, vague descriptions, OPN equipment procurement coded as products
- The blended-contract allocation problem
- OTA visibility findings

### Gold Output Files

| File | Contents |
|------|----------|
| `bottomup/gold_tam_table.md` | Bucket-by-bucket bottom-up spend with FY columns |
| `bottomup/gold_vendor_landscape.md` | Top vendors by bucket, market share, program associations |
| `bottomup/gold_confidence_and_gaps.md` | Confidence tiers, blind spots, methodology notes |
| `bottomup/tam_bottomup_summary.md` | Executive summary of bottom-up findings |

---

## Execution Sequencing

| Phase | Dependency | Est. Time | Notes |
|-------|-----------|-----------|-------|
| 0: Setup | None | 1-2 hrs | Script writing + keyword/regex design |
| 1: FPDS Bronze | Phase 0 | ~30 min (API time) | Trimmed to 11 queries / ~25-30K records |
| 2: USAspending Bronze | Phase 0 | 30-60 min | Can run in parallel with Phase 1 |
| 3: Silver | Phases 1-2 | 2-3 hrs | Hardest intellectual work — classification and dedup |
| 4: Gold | Phase 3 | 1-2 hrs | Aggregation and analysis |

**Phases 1 and 2 can run in parallel.**

---

## Key Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Public yard work invisible in FPDS | Misses ~$7-8B of Bucket 1 | Document as known gap; bottom-up covers private industry only |
| Blended contracts inflate Bucket 1 / deflate Bucket 3 | Bucket-level precision suffers | Primary + secondary bucket tags; document the blending |
| FPDS description vagueness | Misses awards with generic descriptions | Vendor-specific pulls deferred; run after Silver gap analysis if needed |
| FPDS pagination — IDV record type | Parser stops early if IDV records not handled | Must parse all 4 record types: award, IDV, OtherTransactionAward, OtherTransactionIDV |
| OPN equipment procurement coded as products | Bucket 3 understated | Note that equipment procurement is better sized from budget books |
| Deduplication errors (mod handling) | Dollar values inflated 5-10x | Strict latest-mod-per-PIID rule |
| FPDS `AGENCY_CODE` gotcha | Zero results with wrong field | Always use `CONTRACTING_AGENCY_ID` with date ranges |
| USAspending PSC filter syntax | 422 errors | Plain array format, not require/exclude |

---

## What Bottom-Up Will and Won't Tell Us

**Will tell us:**
- Which private companies perform in-service vessel work and how much they receive
- Contract vehicle types (definitive, delivery order, BPA, OT) by work type
- Contract pricing types (FFP, cost-plus, T&M) by bucket
- Competition levels (sole source vs. competed)
- Geographic distribution (place of performance)
- Contracted spending trends FY22-FY26
- Vendor concentration and competitive dynamics

**Won't tell us:**
- Public naval shipyard workload (~$7.8B) — organic, not contracted
- Precise bucket splits within blended availability contracts
- Subcontractor spending (only primes visible)
- Classified program details
- How much OPN equipment procurement is for in-service vs. new-build
