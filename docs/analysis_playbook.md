# Naval Vessel TAM Analysis — Playbook & Lessons Learned

What we learned doing this analysis, organized for future reference.

---

## 1. Budget Book Structure — Where to Find What

### SCN (Shipbuilding & Conversion, Navy)
- **P-1 Detail Table** (near front of book, ~lines 210-660): Master table with every SCN line item, FY24/FY25/FY26 columns. This is the single best source for new construction TOA.
- **Format quirk:** Each program spans multiple lines — ship procurement, advance procurement (AP), subsequent full funding (SFF), completion of prior year (CTC). Must sum all related lines per program.
- **FY26 has a "Reconciliation" column** = OBBA / Working Families Tax Cut Act funding. Many ships funded entirely through reconciliation (DDG-51, LPD, LHA, MLS, T-AO). Use FY26 Total (Request + Reconcil) for TAM.
- **L49 "Completion of PY Shipbuilding Programs"** is a catch-all for cost growth on prior-year ships. Contains MEMO NON ADD breakout showing which programs. L49 is separate from individual program CTC lines — individual programs show CTC for FY24/FY25, while L49 consolidates FY26 CTC. No double-count.
- **Resource Summary tables** (deep in the book, per program): Show detailed TOA breakout including outfitting. The P-5c Ship Cost Analysis tables show cost category breakdown (basic construction, electronics, propulsion, HM&E, ordnance).
- **RCOH and LCAC SLEP are the only in-service items in SCN.** Everything else is new construction.

### OMN Vol2 — The Most Data-Rich Book
- **PB-61 Depot Maintenance Summary** (~lines 3442-4598 of source): Three OMN sections + one OPN section, all broken out by vessel class. This is the best source for per-class depot maintenance data.
  - **"Ship Maint"** section = scheduled depot maintenance (Bucket 2) by class
  - **"Continuous Maintenance"** section = continuous/emergent (Bucket 3) by class
  - **"Other"** section = additional depot-related work by class (mixed bucket assignment)
  - **OPN section** = OPN-funded depot material by class (additive to OMN, not overlapping)
- **OMN Total in PB-61 (~$17.5B)** is larger than 1B4B alone (~$13.8B) because PB-61 includes both SAG 1B4B and 1B5B.
- **OP-5A Shipyard Tables** (per shipyard): Hull-level availability records with budgeted costs. Format: "Bud: Mission Direct ($K) / Reimb ($K)". These are dollar amounts, not man-days. Covers public yards only — no private yard availability detail.
- **Availability type codes** in OP-5A: DSRA, EDSRA, DMP, DPIA, PIA, CIA, SRA, EOH, ERO, ERP, CMAV, IA (inactivation), SLA, RCD.

### OMN (Main Book)
- **SAG 1B4B** (~$13.8B): Ship Depot Maintenance. NME sub-elements in Performance Criteria table give per-category breakout (SMP, 2-Hatch, 4-Hatch, Sub Avail, etc.) but NOT per vessel class.
- **SAG 1B5B** (~$2.8B): Ship Depot Operations Support. Named sub-elements for sustainment engineering (DDG-1000 support, NMP, SUPSHIP, etc.).
- **CMMP and Expedited M&M** within 1B4B are the Bucket 3 (continuous/emergent) items.

### OPN BA1
- **L26 Ship Maintenance, Repair & Modernization** (~$2.4B): OPN material/equipment for depot availabilities. This is the material companion to OMN 1B4B labor.
- **Named per-class modernization BLIs**: DDG Mod ($997M), LCS Mod ($238M), LHA/LHD Midlife ($123M), etc. Excellent per-class data for Bucket 4.
- **BA8 spares** (BLI 9020, ~$884M): War reserve / initial spares. Can be broken out by class from the detail book.

### OPN BA2
- **In-service share requires judgment.** Most BA2 electronics lines serve both new construction and in-service fleet. We used program-level context to estimate shares (CANES 99%, SEWIP 100%, SSN Acoustic 80%, etc.).
- Multi-class systems (CANES, SEWIP) serve DDGs, carriers, amphibs — keep as "multi-class" unless detail book specifies platform quantities.

### USCG Congressional Budget Justification
- **PC&I Vessels PPA** has both new construction (OPC, FRC, PSC, WCC) and in-service (ISVS with SLEP/MMA sub-investments).
- **O&S Object Class 25.7** ($1.03B) is the maintenance line but NOT vessel-specific — includes aircraft and shore equipment. We estimated 60% vessel share (medium confidence).
- **ISVS sub-investments** give per-class SLEP/MMA data: MLB SLEP, WMEC SLEP, WLM MMA, Healy SLEP, WMSL MMA.
- **"Boats" line** mixes new boat procurement and RB-M SLEP — requires split.
- **FY24/FY25 for USCG** are shown as "Enacted" and "Full-Year CR" (continuing resolution), not actuals. Less precise than Navy data.

---

## 2. Key Analytical Decisions & Rationale

### What metric to use for new construction TAM
**Total Obligation Authority (TOA)** from the P-1 — includes net procurement, SFF, AP, and CTC. This represents the authority to obligate funds in each FY, which drives industry activity. Alternative (net P-1 only) would undercount because it excludes prior-year SFF and AP.

### How to handle multi-year ship funding
SCN uses incremental funding — a ship authorized in FY25 gets AP in FY23-24, full funding in FY25, SFF in FY26-27, and possibly CTC in FY28+. The P-1 TOA captures all flows per year. Don't confuse total ship cost with annual spend.

### In-service share of OPN BA2/BA4
Some lines are 100% in-service (SEWIP, SQQ-89, in-service radars). Others are split with new construction (CANES 99%, SSN Acoustic 80%, Tomahawk 70%, Strategic Missile 50%). Read the program descriptions in the detail book to determine share.

### USCG O&S vessel share
Budget books don't break out vessel vs. aircraft vs. shore within O&S. The 60% estimate for Object Class 25.7 is based on fleet size but is uncertain. This is the single largest source of medium-confidence uncertainty in the in-service TAM.

### Bucket 7 (Availability Support) undercount
Most availability support costs (scaffolding, cranes, shore power, environmental) are embedded in Bucket 2 depot availability contracts. The $228M identified is a floor. True figure is likely $1-2B but cannot be separated from budget books alone — would need contract-level (bottom-up) data.

---

## 3. Data Processing Pitfalls

### Budget book PDF-to-text conversion
- Always use `-layout` flag for PDF conversion. Without it, column alignment is lost and dollar figures become unreadable.
- SCN book is ~17,000 lines. Read strategically — find the P-1 summary table first (lines 200-660), then go to specific program sections only as needed.

### Double-counting traps
- **OMN vs OPN**: Different appropriations, always additive. OMN = labor, OPN = material/equipment. Both go to the same physical availabilities.
- **NWCF vs OMN**: NWCF is NOT additive for naval shipyard work. Public shipyards are funded through OMN direct, not NWCF. NWCF covers aviation and Marine Corps ground depot only. Exception: MSC M&R was in NWCF until FY26 transfer to OMN.
- **OMN Vol2 shipyard data vs OMN 1B4B**: Same dollars, different view. OP-5A is per-shipyard execution data. Use for performer split (public/private), not additive to TAM.
- **SCN L49 CTC vs individual program CTC**: Not double-counted. Individual programs show CTC for FY24/FY25; L49 consolidates FY26 CTC separately.

### Rounding and reconciliation deltas
- Sub-elements don't always sum exactly to parent totals. Multiple exhibit tables in the same book may show slightly different figures. Use the financial summary / SAG total as the controlling figure.
- Accept deltas under ~$1M as rounding. Flag anything larger.

---

## 4. Per-Class Data Availability

### What exists in budget books (no guessing needed)
| Data | Source | Class Granularity |
|------|--------|-------------------|
| New construction by program | SCN P-1 | Per program/class |
| Depot maintenance (OMN) by class | PB-61 "Ship Maint" section in OMN Vol2 | CV-CVN, DDG, SSN variants, LCS, AMPHIBS, LPD, LHD, LHA, LSD, etc. |
| Depot maintenance (OPN) by class | PB-61 OPN section in OMN Vol2 | DDG, LCS, LHD, AMPHIBS, CG, etc. |
| Continuous maintenance by class | PB-61 "Continuous Maint" section in OMN Vol2 | DDG, LCS, CG, DDG-1000, LCAC (partial — some in "Other") |
| Modernization by class | OPN BA1 named BLIs | DDG Mod, LCS Mod, LHA/LHD Midlife, Sub Support, etc. |
| RCOH by hull | SCN P-1 + Resource Summary | CVN 74, CVN 75 |
| SLEP/MMA by class | USCG ISVS sub-investments | WMEC, WLM, MLB, Healy, WMSL |
| Sustainment engineering by class | OMN 1B5B NMP + OPN BA8 | Partial — DDG, Sub, Carrier, Amphibs, LCS |
| Hull-level availabilities | OMN Vol2 OP-5A tables | Per hull (public yards only) |

### What does NOT exist by class (don't guess)
- Bucket 3 (continuous/emergent) for carriers, submarines, amphibs (lumped into "Other" in PB-61)
- Bucket 7 (availability support) — not class-specific, yard/fleet-wide
- USCG O&S maintenance by cutter class — budget books don't break it down
- OMN 1B4B NME sub-elements by vessel class (e.g., "2-Hatch Ships" and "4-Hatch Ships" are NOT per-class)

---

## 5. File & Directory Structure

```
topdown/
  sources/          # Raw PDF + text files from budget books
  bronze/           # First-pass extraction from each source
    scn.md          # SCN in-service items
    scn_newbuild.md # SCN new construction items
    omn.md          # OMN main book
    omn_vol2.md     # OMN Vol2 (PB-61, shipyard data)
    opn_ba1.md      # OPN Budget Activity 1
    opn_ba2.md      # OPN Budget Activity 2
    opn_ba4.md      # OPN Budget Activity 4
    opn_ba5_8.md    # OPN Budget Activities 5-8
    uscg.md         # USCG Congressional Budget Justification
  silver/           # Canonicalized, dispositioned, overlap-resolved
    canonical.md    # In-service items (uses old 6-bucket numbering)
    newbuild_canonical.md  # New construction items
  gold/             # Final TAM tables, summaries, reconciliation
    tam_table.md    # Master TAM table with all 7 buckets
    bucket1_newconstruction.md  # Detailed Bucket 1 line items
    summary.md      # Executive summary
    confidence_and_gaps.md  # Confidence tiers, known gaps
    reconciliation.md  # Internal consistency checks, benchmarks
```

---

## 6. Taxonomy Reference

| Bucket | Name | Primary Funding | Key Discriminator |
|--------|------|-----------------|-------------------|
| 1 | New Construction | SCN, USCG PC&I | Builds a new vessel |
| 2 | Scheduled Depot Maintenance | OMN 1B4B + OPN BA1 L26 | Restores existing condition during planned availability |
| 3 | Continuous/Intermediate/Emergent | OMN 1B4B (CMMP) | Shorter-duration work outside big depot event |
| 4 | Modernization & Alteration | OPN BA1/BA2/BA4 | Adds capability or changes configuration |
| 5 | Major Life-Cycle Events | SCN (RCOH), USCG PC&I (SLEP/MMA) | Named service-life-extension program |
| 6 | Sustainment Engineering | OMN 1B5B + OPN BA8 | Planning, DMSMS, spares, tech support |
| 7 | Availability Support | OMN 1B5B (partial) | Husbanding, port services, scaffolding |

See `docs/Seven_Bucket_TAM_Crosswalk.md` for the full taxonomy with PSC codes, keywords, and decision tree.

---

## 7. FY26 Headline Numbers

| | Amount | Note |
|--|--------|------|
| Full TAM (7 buckets) | ~$74.9B | |
| New Construction (Bucket 1) | ~$46.3B | Includes $24.5B OBBA reconciliation |
| In-Service (Buckets 2-7) | ~$28.6B | |
| Largest program (new construction) | Virginia Class $11.1B | |
| Largest program (in-service) | OMN 1B4B Depot Maintenance $13.8B | |
| Public yard workload | ~$7.8B (OMN direct) | 4 naval shipyards |
| Private industry addressable (in-service) | ~$18-22B | |
| USCG total | ~$2.1B ($1.3B new + $0.8B in-service) | |
