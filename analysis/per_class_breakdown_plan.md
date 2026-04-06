# Per-Vessel-Class Spending Breakdown — Plan

## Objective

Produce a workbook and summary document showing how much annual spending is allocated to each vessel class (DDG, CVN, SSN, LCS, LPD, LHA/LHD, FFG, CG cutters, etc.), segmented by the 7-bucket taxonomy, with FY24/FY25/FY26 columns. The workbook also incorporates the existing top-down TAM data.

---

## What Data Already Exists (From Bronze Extractions)

### High per-class visibility (can build now)

| Bucket | Source | What exists | Class granularity |
|--------|--------|-------------|-------------------|
| **Bucket 1 (New Construction)** | `topdown/bronze/scn.md` | SCN P-1 has every new-build program by hull class with full FY24-26 funding | DDG-51, CVN-78, Columbia, FFG-62, LPD Flight II, T-AO, LHA, LCS, LCAC, ESB — excellent |
| **Bucket 3 (Modernization)** | `topdown/bronze/opn_ba1.md` | OPN BA1 has named per-class modernization BLIs | DDG Mod ($997M), LCS In-Service Mod ($238M), LHA/LHD Midlife ($123M), LPD Support ($126M), DDG-1000 ($115M), Sub Support ($383M), Virginia Support ($52M) — excellent |
| **Bucket 3 (Modernization)** | `topdown/bronze/opn_ba1.md` | OPN ship maintenance by class table | DDG $1.28B, LCS $383M, LHD $395M, LHA $12M, LPD $12M, CV-CVN varies — excellent |
| **Bucket 5 (Major Life-Cycle)** | `topdown/bronze/scn.md` | RCOH is per-hull (CVN 74, CVN 75); LCAC SLEP is per-unit | CVN, LCAC — excellent |
| **Bucket 5 (Major Life-Cycle)** | `topdown/bronze/uscg.md` | USCG SLEP/MMA by cutter class | WMEC ($76M), MLB ($45M), WLM ($15M), WMSL ($5M), Healy ($11M) — excellent |
| **Bucket 6 (Sustainment Eng.)** | `topdown/bronze/omn_vol2.md` | 1B5B NMP performance criteria by class | DDG ($95M), Subs ($58M), Carriers ($51M), Amphibs ($178M), LCS ($2M), DDG-1000 ($209M) — good |
| **Bucket 6 (Sustainment Eng.)** | `topdown/bronze/opn_ba1.md` | BA8 spares by class | DDG ($124M), CV-CVN ($364M), LCS ($70M), SSN ($75M), SSN-MTS-SSGN ($260M), LHA ($16M), LHD ($16M), LPD ($44M) — excellent |

### Low per-class visibility (harder to decompose)

| Bucket | Source | Problem | What to do |
|--------|--------|---------|------------|
| **Bucket 2 (Scheduled Depot)** | `topdown/bronze/omn.md` | 1B4B ($13.8B) is organized by availability type and shipyard, not by class. Individual availabilities are listed per-hull but not aggregated by class. | **Option A:** Manually aggregate from hull-level availability listings in omn.md/omn_vol2.md. **Option B:** Use PB-61 depot maintenance summary by weapon system from omn_vol2.md (CV-CVN $2.72B, SSN $2.43B, DDG $1.28B, Amphibs $237M, LHD $395M, LCS $383M). **Option C:** Bottom-up pull from USAspending J998/J999 by hull designation keyword. |
| **Bucket 3 (Continuous/Emerg.)** | `topdown/bronze/omn.md` | CMAV/ERATA/ORATA are budgeted as aggregate pools, not by class | **Option A:** Bottom-up USAspending pull filtering CMAV contracts by hull designation. **Option B:** Allocate proportionally based on fleet size or depot maintenance share. **Option C:** Leave blank with note. |
| **Bucket 7 (Availability Support)** | various | Port services, husbanding, scaffolding are not class-specific — they're availability-level or yard-level | Not decomposable by class. Leave as fleet-wide total. |

---

## Research Steps

### Phase 1: Compile existing per-class data from bronze (no new research)

**Effort: Low — data already extracted, just needs assembly**

1. **Bucket 1 (New Construction):** Pull per-program figures from `topdown/bronze/scn.md` (Navy) and `topdown/bronze/uscg.md` (CG: OPC, FRC, PSC). Map each program to a vessel class.

2. **Bucket 3 (Modernization):** Combine three data sources already in bronze:
   - Named OPN BA1 modernization BLIs (DDG Mod, LCS Mod, etc.)
   - OPN BA1 "Ship Maintenance by Class" table (DDG, LCS, LHD, etc.)
   - OPN BA2 ship-installed electronics — allocate by primary platform where detail book specifies (e.g., AN/SQQ-89 → DDG/CG, CANES → fleet-wide)

3. **Bucket 5 (Major Life-Cycle Events):** Pull directly:
   - CVN RCOH from `topdown/bronze/scn.md` → CVN class
   - LCAC SLEP from `topdown/bronze/scn.md` → LCAC class
   - CG SLEPs/MMAs from `topdown/bronze/uscg.md` → per cutter class

4. **Bucket 6 (Sustainment Engineering):** Combine:
   - 1B5B NMP class breakdown from `topdown/bronze/omn_vol2.md`
   - BA8 spares by class from `topdown/bronze/opn_ba1.md`
   - DDG-1000 Maintenance & Support ($209M) from `topdown/bronze/omn_vol2.md`
   - Surface & Amphib Ship Support ($451M) — allocate or tag as "surface fleet-wide"

### Phase 2: Decompose Bucket 2 (Scheduled Depot) by class

**Effort: Medium — requires aggregation from existing data + one judgment call**

Two options (pick one or do both for triangulation):

**Option A — PB-61 top-down (recommended start)**

The PB-61 Depot Maintenance Summary in `topdown/bronze/omn_vol2.md` already has per-weapon-system depot maintenance figures. These are the cleanest top-down per-class numbers:
- CV-CVN: $2.72B FY26
- SSN-MTS-SSGN: $2.43B FY26
- SSN-SSGN: $1.41B FY26
- DDG: $1.28B FY26
- LHD: $395M FY26
- LCS: $383M FY26
- Amphibs: $237M FY26

**Caveat:** PB-61 is OPN depot maintenance funding, which is a different appropriation from the OMN 1B4B depot maintenance labor. The PB-61 weapon system figures may represent the OPN material component of depot work, not the full OMN labor + OPN material cost. Need to verify whether these are additive to or overlapping with 1B4B. Read the PB-61 section header in `topdown/bronze/omn_vol2.md` carefully.

**Action:** Read the PB-61 section in `topdown/bronze/omn_vol2.md` (around lines 5500-6000) to confirm what these figures represent and whether they're the OMN depot maintenance figures broken out by class or OPN depot material.

**Option B — Aggregate from hull-level availabilities**

The OMN Vol2 bronze file contains individual availability records with per-hull budgets (e.g., CVN 72 DPIA $527M, SSN 789 EDSRA $417M). Aggregate these by class:
- Sum all CVN availability budgets → CVN depot total
- Sum all SSN availability budgets → SSN depot total
- Sum all DDG availability budgets → DDG depot total
- etc.

**Caveat:** This only captures the availabilities listed for FY26. There may be ongoing availabilities funded in prior years that still consume FY26 dollars.

**Option C — Bottom-up USAspending pull (future validation)**

Query USAspending API for J998/J999 awards, filter by hull designation in description text (e.g., "DDG", "CVN", "SSN"), aggregate by class. This would give actual contract dollars flowing to each class. Best used as a cross-check against Options A/B.

### Phase 3: Assess Bucket 3 (Continuous/Emergent) by class

**Effort: Medium-High — limited top-down data, may need bottom-up**

CMAV/ERATA/ORATA totals are known ($651M / $139M / $1.07B) but not broken out by class in budget books.

**Option A — Proportional allocation**

Allocate CMAV/ERATA/ORATA proportionally based on each class's share of depot maintenance (Bucket 2). Rationale: classes with more depot work likely generate more emergent/continuous work.

**Option B — Bottom-up USAspending pull**

Query USAspending for awards containing "CMAV" + hull designation. The bronze data already has some CMAV award data in `bottomup/bronze/usaspending/awards_CMAV_navy_fy22-26.json`. Parse this by hull class.

**Option C — Leave blank**

Note "not separately budgeted by class" and leave the per-class column empty for Bucket 3. This is honest and defensible.

### Phase 4: Handle Bucket 7 (Availability Support) and cross-class items

**Effort: Minimal**

Bucket 7 is not decomposable by vessel class. Port services, husbanding, scaffolding, etc. are facility-level or fleet-wide. Mark as "Fleet-wide / not class-specific" in the workbook.

For OPN BA2 items that serve multiple classes (e.g., CANES installs on DDGs, carriers, and amphibs), either:
- Allocate proportionally by fleet size
- Tag as "multi-class" with a note listing which classes benefit
- If the BA2 detail book specifies quantities by platform, use those

---

## Workbook Design

### Tab 1: "TAM Summary"

The existing top-down TAM roll-up table — total market by bucket, FY24/FY25/FY26, with funding source and performer splits. Pulled from `topdown/gold/summary.md`.

```
                           FY24 ($K)    FY25 ($K)    FY26 ($K)    % of TAM
Bucket 1: New Construction      —            —            —           —
Bucket 2: Sched Depot Maint  13,271,718  12,909,097  13,617,194    47.6%
Bucket 3: Continuous/Emerg    2,083,638   2,155,459   2,234,715     7.8%
Bucket 4: Modernization       ...          ...          ...         23.2%
Bucket 5: Life-Cycle Events    ...          ...          ...          8.7%
Bucket 6: Sustain Eng          ...          ...          ...         11.9%
Bucket 7: Avail Support        ...          ...          ...          0.8%
TOTAL                          ...          ...          ...        100%
```

### Tab 2: "By Vessel Class"

The main deliverable — a matrix of vessel class (rows) x bucket (columns) for FY26.

```
                    Bucket 1   Bucket 2   Bucket 3   Bucket 4   Bucket 5   Bucket 6   Bucket 7   TOTAL
                    New Const  Depot M&R  Cont/Emrg  Mod/Alt    Life-Cyc   Sust Eng   Avail Sup
DDG-51              $X         $X         —          $997M      —          $X         —          $X
DDG-1000            —          $X         —          $115M      —          $209M      —          $X
CVN (Nimitz/Ford)   $X         $X         —          $X         $2,262M    $X         —          $X
SSN (688/Seawolf)   —          $X         —          $X         —          $X         —          $X
SSN (Virginia)      $X         $X         —          $X         —          $X         —          $X
SSBN (Ohio)         —          $X         —          $X         —          $X         —          $X
SSBN (Columbia)     $X         —          —          —          —          —          —          $X
FFG-62              $X         —          —          —          —          —          —          $X
LCS                 —          $X         —          $238M      —          $X         —          $X
LPD                 —          $X         —          $126M      —          $X         —          $X
LHA                 —          $X         —          $X         —          $X         —          $X
LHD                 —          $X         —          $X         —          $X         —          $X
LSD                 —          $X         —          $4M        —          —          —          $X
T-AO                $X         —          —          —          —          —          —          $X
ESB/ESD             —          $X         —          —          —          —          —          $X
LCAC                —          —          —          —          $37M       —          —          $X
MSC Fleet           —          $1,584M    —          —          —          —          —          $X
CG: NSC (WMSL)      —          $X         —          $X         $5M        —          —          $X
CG: OPC             $X         —          —          —          —          —          —          $X
CG: FRC (WPC)       $X         $X         —          —          —          —          —          $X
CG: WMEC-270        —          $X         —          —          $76M       —          —          $X
CG: WLM-175         —          $X         —          —          $15M       —          —          $X
CG: MLB-47          —          —          —          —          $45M       —          —          $X
CG: Healy           —          —          —          —          $11M       —          —          $X
Multi-class / TBD   —          —          —          $X         —          $X         $228M      $X
TOTAL               $X         $13.6B     $2.2B      $6.6B      $2.5B      $3.4B      $228M      $28.6B
```

**Column rules:**
- Cells with data show the FY26 figure in $K
- `—` means either zero or "not separately budgeted by class" (distinguished by cell color or footnote)
- "Multi-class / TBD" row catches BA2/BA4 systems serving multiple classes and Bucket 7 fleet-wide items
- Column totals must reconcile to Tab 1 TAM totals (cross-check formula)

### Tab 3: "FY Trend by Class"

For the top 5-6 vessel classes by total spend, show FY24/FY25/FY26 trend across all applicable buckets. One section per class:

```
DDG-51 Class
                    FY24 ($K)    FY25 ($K)    FY26 ($K)    CAGR
Bucket 2: Depot      $X           $X           $X           X%
Bucket 4: DDG Mod    $641,676     $861,066     $997,485     25%
Bucket 6: NMP-DDG    $127,935     $75,364      $95,494      ...
Bucket 6: Spares     $106,432     $100,690     $123,497     ...
TOTAL DDG-51         $X           $X           $X           X%
```

### Tab 4: "Sources & Methodology"

- Source file for each cell (which bronze file, which line/page)
- Confidence level (High/Medium/Low) per cell
- Allocation methodology notes (e.g., "CMAV allocated proportionally by depot share")
- List of buckets/classes left blank and why

### Tab 5: "Calculations"

Working sheet with:
- Raw data inputs (blue text per styling guide)
- Formulas linking to Tab 1 and Tab 2
- Reconciliation checks: each column total in Tab 2 = corresponding bucket total in Tab 1
- Any proportional allocation formulas used for Bucket 3

---

## Summary Document

A markdown file (`analysis/per_class_summary.md`) containing:

1. **Headline finding** — e.g., "DDG-51 is the single largest vessel class by in-service spending at ~$X.XB/yr (X% of the TAM), driven by..."
2. **Top 5 classes by total in-service spend** — ranked table
3. **Per-class highlights** — 2-3 sentences each on the top classes
4. **Data coverage assessment** — which buckets have clean per-class data vs. which are estimated or blank
5. **Methodology notes** — how allocations were made, what was excluded

---

## Execution Sequence

| Step | What | Input | Output | Effort |
|------|------|-------|--------|--------|
| 1 | Re-read PB-61 section of `topdown/bronze/omn_vol2.md` to confirm per-class depot maintenance figures | omn_vol2.md | Confirmed Bucket 2 per-class figures | Low |
| 2 | Compile all per-class data from bronze files into a working table | All bronze files | `analysis/per_class_working_data.md` | Medium |
| 3 | Decide which Bucket 3 approach to use (proportional, bottom-up, or blank) | Judgment call | Decision documented | Low |
| 4 | If using bottom-up for Bucket 3: parse CMAV awards JSON by hull class | `bottomup/bronze/usaspending/awards_CMAV_navy_fy22-26.json` | CMAV by class | Medium |
| 5 | Build workbook with all tabs | Working data | `output/tam_per_class_workbook.xlsx` | Medium |
| 6 | Write summary document | Workbook data | `analysis/per_class_summary.md` | Low |
| 7 | Cross-check: Tab 2 column totals = Tab 1 bucket totals | Workbook | Reconciliation pass | Low |

---

## Key Decisions Needed Before Starting

1. **Bucket 3 (Continuous/Emergent) — allocate proportionally, pull bottom-up, or leave blank?**
   - Recommendation: Leave blank for now, note as "not separately budgeted by class." Can add later with bottom-up data.

2. **OPN BA2/BA4 multi-class systems — allocate to primary platform or keep as "multi-class"?**
   - Recommendation: Keep the clearly class-specific ones (AN/SQQ-89 → DDG/CG) allocated. Keep the rest as "multi-class" to avoid false precision.

3. **Submarine class granularity — combine all subs or split 688/Seawolf/Virginia/Ohio?**
   - Recommendation: Split where data allows (Virginia has its own OPN line), combine where it doesn't (depot maintenance is usually "SSN" or "SSBN" without sub-class detail).

4. **CG vessel O&S — use the 60/40 Bucket 2/3 analyst allocation from gold table, or attempt a finer split?**
   - Recommendation: Keep the 60/40 split from gold table. CG O&S detail doesn't break down by maintenance type at the cutter-class level anyway.
