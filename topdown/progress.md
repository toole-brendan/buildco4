# Top-Down TAM Analysis — Progress Tracker

---

## Phase 0: Convert Supporting Exhibits PDF to Text
**Status: COMPLETE**
- `Supp_Book.txt` already existed when work began (converted 2025-04-05)

## Phase 1: Read the Map (Supporting Exhibits)
**Status: COMPLETE**
- O-1 and P-1 exhibit tables fully extracted and documented in `topdown_implementation_plan.md`
- All SAG codes (1B1B, 1B2B, 1B4B, 1B5B) and OPN BLIs identified with FY24/25/26 figures
- SCN RCOH and LCAC SLEP lines identified
- BA8 spares line identified

## Phase 2: Extract Navy O&M Data (Buckets 1, 2, 5, 6)
**Status: COMPLETE**

### Step 2A: OMN_Book.txt — Decompose SAG 1B4B
**Output:** `topdown/bronze/omn.md`
- SAG 1B4B ($13,803,188K FY26) fully decomposed
- Availability-type breakdown captured: OH, SRA, SIA, PIA, CIA, SCO, ERATA, ORATA, CM, Non-depot/IL
- Naval shipyard workload by yard: NNSY, PNSY, PSNSY, PHNSY
- MSC sub-elements captured (new FY26 transfer): MTA-17, ROH-34, Other MSC M&R ($1,584,000K total)
- OP-32 object class breakdown captured
- All program increases/decreases itemized

### Step 2B: OMN_Book.txt — Extract SAG 1B5B
**Output:** `topdown/bronze/omn.md`
- SAG 1B5B ($2,760,878K FY26) fully decomposed
- Sub-elements: NAVSEA HQ, NMP (with ship-class sub-breakdown), Nuclear Propulsion, Surface/Amphib Ship Support, SUPSHIP, Berthing & Messing, NMMES, Facilities/Supply Ops, PRE/PRL CV/CVN Tech Support, RMC, Smart Work/TOC, CSOSS, DDG-1000, MCM Support, Service Craft/Boats
- SIOP ($28,752K FY26) identified within 1B5B

### Step 2C: OMN_Vol2_Book.txt — Fine-grain detail
**Status: COMPLETE**
**Output:** `topdown/bronze/omn_vol2.md`
- OP-31 Spares and Repair Parts: Ship DLRs ($751M/$750M/$1.307B FY24-26), Ship Consumables ($2.345B/$2.283B/$3.013B FY24-26)
- OP-5A Naval Shipyards 8% Capital Investment Plan — revenue averages and appropriated funding
- Four individual shipyard sections (PHNSY&IMF, PSNS&IMF, PNSY, NNSY) with funding, performance metrics, workload resource days, workforce end strength, full availability tables with hull numbers/dates/types
- PB-61 Depot Maintenance Summary by ship class: CV-CVN $2.72B, SSN-MTS-SSGN $2.43B, SSN-SSGN $1.41B FY26 funded
- OPN ship depot items: DDG $1.28B, AMPHIBS $237M, LHD $395M, LCS $383M FY26
- Note: Book does NOT contain SAG 1B4B/1B5B identifiers directly — provides shipyard-level and PB-61 weapon-system-level breakdowns underlying those SAG totals

## Phase 3: Extract Navy Procurement Data (Bucket 3, parts of 4 and 5)

### Step 3A: OPN_BA1_Book.txt — Decompose the big lines
**Status: COMPLETE**
**Output:** `topdown/bronze/opn_ba1.md`
- Line 26 Ship Maintenance, Repair and Modernization ($2,392,620K FY26) — full detail with CPF/FFC split and individual ship availabilities
- DDG Mod ($997,485K FY26 total incl. reconciliation)
- LCS In-Service Modernization ($237,728K total)
- LHA/LHD Midlife ($123,384K total)
- LCC ESLP ($19,276K)
- LCAC ($20,321K — entirely reconciliation)
- Reactor Components ($399,603K — details classified)
- All 21 target BLIs identified and cross-referenced

### Step 3B: OPN_BA2_Book.txt — Ship-installed electronics
**Status: COMPLETE**
**Output:** `topdown/bronze/opn_ba2.md`
- 12 ship-relevant BA2 lines captured with full dollar figures and descriptions
- Key items: AN/SQQ-89 ($144K), SSN Acoustic ($499K), AN/SLQ-32 ($461K), CANES ($534K), In-Service Radars ($250K), Shipboard IW ($380K)
- Exclusions noted: Fixed Surveillance System (shore-based), SURTASS (not combat ship equipment)
- FY26 scope changes flagged (program mergers affecting comparability)

### Step 3C: OPN_BA4_Book.txt — Ship weapon systems
**Status: COMPLETE**
**Output:** `topdown/bronze/opn_ba4.md`
- 5 target BLIs fully extracted: Ship Gun Systems ($7,358K), Ship Missile Support ($455,822K), Tomahawk Support ($107,709K), SSN Combat Control ($102,954K), Anti-Ship Missile Decoy ($89,129K)
- 6 additional BLIs flagged with ship-relevance: Harpoon ($209K), CPS ($67,264K), Strategic Missile ($492,999K), ASW Support ($25,721K), Directed Energy/ODIN ($2,976K), Surface Training ($186,085K)
- Extensive in-service/backfit/retrofit language captured; new-build vs. in-service splits noted where available
- DMSMS/obsolescence references captured (especially Anti-Ship Missile Decoy)

### Step 3D: OPN_BA5-8_Book.txt — BA8 Spares
**Status: COMPLETE**
**Output:** `topdown/bronze/opn_ba5_8.md`
- BLI 9020 (Spares and Repair Parts, Line 176): $585,865K FY26 request / $883,630K with reconciliation
- BLI 9021 (Virginia Class Spares, Line 177): $478,691K FY24, zeroed FY25/FY26
- Sub-line structure: Initial Spares, COSAL Outfitting, Lay-In Spares, Vendor-Direct/Replenishment
- Full P-18 Initial vs. Replenishment breakdown: 70+ end items, Initial $522.594M / Replenishment $46.109M FY26
- Ship-class-specific items: DDG 51 mod spares ($13.6M+$14M), LHA/LHD midlife ($3.3M), submarine spares, LCS mission modules
- Reconciliation: $297.8M mandatory funding (Shipbuilding + Readiness sections)
- BA5-7 scan: No in-service vessel work found; only shore-based/pier-side support items

### Step 3E: OPN_BA3_Book.txt — Low priority
**Status: NOT STARTED** (deprioritized unless gap surfaces)

## Phase 4: Extract Major Life-Cycle Events (Bucket 4)

### Step 4A: SCN_Book.txt — RCOH detail
**Status: COMPLETE**
**Output:** `topdown/bronze/scn.md`
- CVN 74 STENNIS: In RCOH at HII-NNS since 2021, delivery Nov 2027; $483.1M cost-to-complete in FY26
- CVN 75 TRUMAN: RCOH starts Jun 2026, delivery Jan 2031; $1,779.011M subsequent full funding FY26
- FY26 total obligation authority: $2,262.111M
- Full cost breakdowns for both hulls: Basic Construction ($5,479.9M/$4,736.1M), Electronics ($402.8M/$476.9M), Propulsion ($615.2M/$691.9M), HM&E ($218.1M/$198.6M), Ordnance ($264.6M/$456.8M), Other ($144.8M/$172.5M)
- Detailed electronics P-8a breakdown with all 14 systems

### Step 4B: SCN_Book.txt — LCAC SLEP
**Status: COMPLETE**
**Output:** `topdown/bronze/scn.md`
- FY26: 1 unit at $37,390K (entirely mandatory/reconciliation, $0 discretionary)
- Original SLEP program completed March 2022; current work is ESLEP (Extended SLEP)
- Unit cost ~$15.3M-$22.5M; Contractor: Walashek; 4 ESLEP craft in production (hulls 81, 76, 73, 79)

### Step 4C: OPN_BA1_Book.txt — Other life-cycle events
**Status: COMPLETE** (captured in Step 3A: LCC ESLP, LHA/LHD Midlife, LSD Midlife, LCAC)

### Step 4D: Cross-reference with USCG
**Status: COMPLETE** (CG SLEP/MMA data captured in Phase 5)

## Phase 5: Extract Coast Guard Data (All Buckets)

### Step 5A: USCG_Justification.txt
**Status: COMPLETE**
**Output:** `topdown/bronze/uscg.md`
- ISVS total: $152,000K FY26 (47-ft MLB SLEP, 270-ft WMEC SLEP, 175-ft WLM MMA, CGC Healy SLEP, 418-ft WMSL MMA new start)
- O&S vessel maintenance via Object Class 25.7: $1,025,994K FY26
- Modernization: ISSS $30,000K (NSC C5I), C4ISR $10,000K, Cyber/EMP $25,800K
- Survey and Design: $5,000K/yr
- MH-60T SLEP: $164,600K FY26
- HC-144 SLEP: $12,000K FY26

## Phase 6: Public-Yard Decomposition and Context

### Step 6A: NWCF_Book.txt — Public-yard share
**Status: COMPLETE**
**Output:** `topdown/bronze/nwcf.md`
- KEY FINDING: NWCF book does NOT contain public naval shipyard data — the four shipyards are funded via OMN direct appropriations, not NWCF revolving fund
- NWCF "Depot Maintenance" = aviation (FRC ~$2.9B) + Marine Corps ground (DMAG ~$345M) only
- Useful data captured: Supply Management weapon system material by platform (Submarine $391.7M, CVN $89.1M, CRUDES $676.9M FY26)
- VACL submarine material strategy: $909M obligated; $38M FY26 increase for "Submarine Wholeness (Shipyards)"
- MSC M&R realignment: $1.4B moving from NWCF to OMN in FY26
- For performer-split analysis: OMN Vol2 book (`bronze_omn_vol2.md`) is the correct source — contains per-shipyard workload and availability data

### ~~Step 6B: president_budget_fy2027.txt~~
**REMOVED** — FY27 document; FY27 justification books not released. Using FY26 books only.

### Step 6B: WPN_Book.txt (if needed)
**Status: NOT STARTED** (deprioritized)

---

## Bronze Output Files

| File | Status | Size |
|------|--------|------|
| `topdown/bronze/omn.md` | Complete | 33KB |
| `topdown/bronze/opn_ba1.md` | Complete | 33KB |
| `topdown/bronze/opn_ba2.md` | Complete | 36KB |
| `topdown/bronze/uscg.md` | Complete | 30KB |
| `topdown/bronze/opn_ba4.md` | Complete | 30KB |
| `topdown/bronze/opn_ba5_8.md` | Complete | 31KB |
| `topdown/bronze/scn.md` | Complete | 25KB |
| `topdown/bronze/nwcf.md` | Complete | 19KB |
| `topdown/bronze/omn_vol2.md` | Complete | 48KB |

## Remaining Bronze Work

**ALL BRONZE EXTRACTION COMPLETE.** All 9 source books have been processed.

---

## Phase 7: Silver Canonicalization
**Status: COMPLETE**

### Output: `topdown/silver/canonical.md`
- All ~85 Bronze line items dispositioned (INCLUDE/EXCLUDE/PARTIAL/SPLIT/PERFORMER_TAG)
- Overlap resolution documented (OMN vs OPN vs NWCF vs OMN Vol2)
- 1B4B ($13.8B) split into Bucket 1 (~$10.9B scheduled depot) and Bucket 2 (~$2.0B continuous/emergent)
- 1B5B ($2.76B) split into Bucket 5 (~$2.5B sustainment engineering), Bucket 6 (~$223M support), Bucket 2 ($27M RMC)
- OPN BA1/BA2/BA4 lines assigned to Bucket 3 with in-service share adjustments for PARTIAL items
- SCN RCOH + LCAC SLEP assigned to Bucket 4
- USCG lines assigned across all 6 buckets with vessel-share estimates
- NWCF and OMN Vol2 shipyard data tagged as PERFORMER_TAG (not additive)
- Public-yard performer split derived: ~56% of 1B4B is public yard ($7.79B)
- Stage-by-stage reconciliation summary included
- Confidence assessment: 84% high-confidence, 15% medium, 1% low

### Silver TAM Roll-Up (FY26, $K)

| Bucket | Total ($K) |
|--------|------------|
| 1. Scheduled Depot Maintenance | ~$13,617,194 |
| 2. Continuous / Intermediate / Emergent | ~$2,234,715 |
| 3. Modernization & Alteration Installation | ~$6,624,111 |
| 4. Major Life-Cycle Events (RCOH/SLEP/MMA) | ~$2,492,740 |
| 5. Sustainment Engineering / Planning | ~$3,411,003 |
| 6. Availability Support / Port Services | ~$227,776 |
| **TOTAL TAM** | **~$28,607,539** |

---

## Phase 8: Gold Classification & Analysis-Ready Output
**Status: COMPLETE**

### Output Files

| File | Size | Contents |
|------|------|----------|
| `topdown/gold/tam_table.md` | 18KB | All 6 buckets with every contributing line item (60+ lines), FY24/FY25/FY26, performer tags, confidence levels. Roll-up summary, performer split, funding source breakdown. |
| `topdown/gold/confidence_and_gaps.md` | 6KB | Confidence tiers by bucket (84% High / 15% Medium / 1% Low), known exclusions, 7 data gaps, sensitivity analysis. |
| `topdown/gold/reconciliation.md` | 6KB | 5 internal consistency checks (all PASS/REASONABLE), 4 external benchmarks, FY24→FY26 trend analysis, methodology transparency. |
| `topdown/gold/summary.md` | 7KB | Executive summary — total market size, by-bucket/customer/funding-source/performer breakdowns, 8 key findings, confidence assessment, methodology. |

### Gold TAM Roll-Up (FY26, $K)

| Bucket | Total ($K) | % of TAM |
|--------|------------|----------|
| 1. Scheduled Depot Maintenance & Repair | ~$13,617,194 | 47.6% |
| 2. Continuous / Intermediate / Emergent | ~$2,234,715 | 7.8% |
| 3. Modernization & Alteration Installation | ~$6,624,111 | 23.2% |
| 4. Major Life-Cycle Events (RCOH/SLEP/MMA) | ~$2,492,740 | 8.7% |
| 5. Sustainment Engineering / Planning | ~$3,411,003 | 11.9% |
| 6. Availability Support / Port Services | ~$227,776 | 0.8% |
| **TOTAL TAM** | **~$28,607,539** | **100%** |

### Key Metrics
- Private-industry addressable TAM: **~$18-22B**
- High-confidence portion: **$23.9B (84%)**
- Underlying growth (excl MSC transfer + RCOH cycle): **~5-7% CAGR**

---

## Remaining Work

**TOP-DOWN ANALYSIS COMPLETE.** All phases (Bronze → Silver → Gold) finished. Ready for bottom-up analysis and triangulation.
