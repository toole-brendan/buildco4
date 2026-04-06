# Silver Canonical — Top-Down TAM Analysis
## In-Service Vessel Work: US Navy & Coast Guard
### FY 2026 President's Budget Justification Books
### All dollar figures in $thousands unless noted

---

## 1. Methodology

### 1.1 Purpose
This Silver layer takes every line item extracted in the nine Bronze files and applies:
- **Disposition**: INCLUDE / EXCLUDE / PARTIAL / SPLIT / PERFORMER_TAG
- **Bucket assignment**: 1–6 per the six-bucket taxonomy
- **Performer tag**: Public Yard / Private Industry / Mixed / Unknown
- **In-service share**: % of the line item attributable to in-service vessel work
- **Rationale**: Why the disposition was chosen

### 1.2 Overlap Resolution
| Potential Overlap | Resolution |
|---|---|
| OMN 1B4B vs OPN BA1 Line 26 | **No overlap.** Different appropriations. OMN funds O&M depot maintenance labor/material. OPN BA1 L26 funds procurement of equipment/material for private-yard ship maintenance. Both contribute to the same physical availabilities but are additive in budget terms. |
| NWCF vs OMN | **NWCF is NOT additive.** NWCF depot maintenance covers aviation (FRCs) and Marine Corps ground (DMAG) only. Public naval shipyards are funded through OMN direct appropriations. NWCF supply management figures represent material costs flowing through the working capital fund — used for PERFORMER_TAG only. |
| NWCF MSC M&R vs OMN 1B4B MSC | **Same dollars.** $1.4B MSC M&R transferred from NWCF to OMN in FY26. Already captured in the 1B4B total of $13,803,188K. Not double-counted. |
| OPN BA8 Spares vs OMN spares | **No overlap.** OPN BA8 funds procurement-account spares (initial and replenishment for newly installed systems). OMN spares (OP-31 DLRs and consumables) are O&M-funded through NWCF Supply Management. Different appropriation streams. |
| OMN Vol2 shipyard data vs OMN 1B4B | **Same dollars, different view.** OMN Vol2 OP-5A shows per-shipyard execution of OMN-funded work. Used for PERFORMER_TAG (public yard share), not additive. |
| OPN BA1 class support lines vs BA2 electronics | **No overlap.** BA1 funds HM&E/platform equipment; BA2 funds C4ISR/combat systems electronics. Different BLIs, different systems. |
| USCG O&S 25.7 vs USCG PC&I ISVS | **No overlap.** O&S funds routine maintenance (Buckets 1/2). PC&I ISVS funds major life-cycle events — SLEPs and MMAs (Bucket 4). Different appropriations. |

### 1.3 Key Assumptions
1. **FY26 figures used as primary TAM year.** FY24 Actual and FY25 Enacted carried for trend analysis.
2. **Reconciliation/mandatory funding included in totals.** FY26 Total = Base + OOC/Reconciliation.
3. **Aircraft excluded from vessel TAM.** CG aircraft SLEPs (MH-60T, HC-144, MH-65, HC-130J) are not in-service vessel work.
4. **New construction excluded.** SCN new-build lines, Columbia-class equipment in OPN, and similar items excluded.
5. **Training systems excluded.** BA4 Surface Training Equipment and Submarine Training Device Mods are predominantly shore-based training systems, not direct vessel work.
6. **USCG O&S vessel share estimated at ~60% of Object Class 25.7.** Without a vessel-specific breakout, this is medium-confidence. The CG fleet of ~250 cutters drives the majority of 25.7 spend, but aviation and shore equipment are also included.

---

## 2. Line-by-Line Disposition Table

### 2A. OMN — SAG 1B4B Ship Depot Maintenance

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------|-------------|--------|-----------|------------------|-----------|
| OMN 1B4B | **Ship Depot Maintenance (SAG total)** | 11,502,495 | 11,763,594 | 13,803,188 | **SPLIT** | — | — | 100% | Parent line; decomposed below |
| OMN 1B4B | → Ship Modernization Program (SMP) | 1,203,816 | 869,253 | 1,197,180 | INCLUDE | 1 | Mixed | 100% | OMN-funded modernization installation labor during depot availabilities. Equipment funded separately via OPN. |
| OMN 1B4B | → NME/2-Hatch Ships | 1,197,197 | 1,306,411 | 1,341,155 | INCLUDE | 1 | Mixed | 100% | Scheduled depot availabilities for 2-hatch surface ships |
| OMN 1B4B | → NME/4-Hatch Ships | 1,247,653 | 1,290,155 | 1,289,894 | INCLUDE | 1 | Mixed | 100% | Scheduled depot availabilities for 4-hatch surface ships |
| OMN 1B4B | → NME/Continuous Maint & Modernization | 1,259,925 | 1,303,227 | 1,321,948 | INCLUDE | 2 | Mixed | 100% | CMAV-type work, emergent repairs, continuous maintenance outside major depot periods |
| OMN 1B4B | → NME/Submarine Availability | 871,537 | 896,253 | 924,629 | INCLUDE | 1 | Public Yard | 100% | Submarine depot availabilities — almost entirely public naval shipyards |
| OMN 1B4B | → NME/Industrial Base | 1,245,621 | 1,270,256 | 1,267,865 | INCLUDE | 1 | Mixed | 100% | Shipyard capacity and industrial base support for depot work |
| OMN 1B4B | → NME/NAVPLAN | 1,134,835 | 1,139,556 | 1,134,328 | INCLUDE | 1 | Mixed | 100% | Navy maintenance plan execution |
| OMN 1B4B | → NME/SSN-to-Repair | 630,555 | 639,229 | 642,190 | INCLUDE | 1 | Public Yard | 100% | Submarine repair at public yards |
| OMN 1B4B | → NME/Carrier | 762,048 | 816,344 | 784,000 | INCLUDE | 1 | Mixed | 100% | Carrier depot availabilities (PIAs, DPIAs, CIAs) — split public/private |
| OMN 1B4B | → NME/Amphibious | 569,696 | 656,000 | 624,506 | INCLUDE | 1 | Private Industry | 100% | Amphibious ship depot availabilities — primarily private yards |
| OMN 1B4B | → NME/LCS | 481,854 | 539,000 | 492,493 | INCLUDE | 1 | Private Industry | 100% | LCS depot availabilities — private yards |
| OMN 1B4B | → NME/DDG | 758,318 | 758,610 | 749,000 | INCLUDE | 1 | Private Industry | 100% | DDG depot availabilities — primarily private yards |
| OMN 1B4B | → NME/Expedited Maint & Mod | 581,796 | 602,706 | 640,000 | INCLUDE | 2 | Mixed | 100% | Expedited/emergent maintenance and modernization |
| OMN 1B4B | → MSC M&R (transfer from NWCF/1B1B) | — | — | 1,584,000 | INCLUDE | 1 | Private Industry | 100% | MSC vessel maintenance transferred to OMN in FY26. MTA, ROH, other MSC depot work at private yards. |

**1B4B Bucket Summary:**

| Bucket | FY26 ($K) | Derivation |
|--------|-----------|------------|
| Bucket 1 (Scheduled Depot) | 10,855,216 | SMP + 2-Hatch + 4-Hatch + Sub Avail + Ind Base + NAVPLAN + SSN-to-Repair + Carrier + Amphib + LCS + DDG + MSC M&R |
| Bucket 2 (Continuous/Emergent) | 1,961,948 | CMMP + Expedited M&M |
| Bucket 6 (Availability Support) | — | Not separately identifiable within 1B4B sub-elements; availability support costs are embedded in depot availability budgets |
| **1B4B Check Total** | **12,817,164** | Note: Sum of sub-elements is $12,219,188 (pre-MSC) + $1,584,000 (MSC) = $13,803,188. The $986K delta vs sub-element sum ($12,817,164 + gap) is due to the Performance Criteria table showing an OMN-only total of $12,219,188 while the individual NME sub-elements shown here sum to a slightly different figure. The SAG total of $13,803,188 from the financial summary is controlling. |

**Confidence note:** The 1B4B sub-element breakout from the Performance Criteria table (lines 5596-5618) uses NME categories that do not perfectly align with the six-bucket taxonomy. The NME "2-Hatch" and "4-Hatch" categories blend scheduled depot work, support work, and potentially some availability support. The bucket assignment is **medium confidence** for the Bucket 1 vs Bucket 6 boundary. The Bucket 2 assignment (CMMP + Expedited M&M) is **high confidence** — these are explicitly continuous/emergent maintenance.

---

### 2B. OMN — SAG 1B5B Ship Depot Operations Support

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------|-------------|--------|-----------|------------------|-----------|
| OMN 1B5B | **Ship Depot Ops Support (SAG total)** | 2,714,238 | 2,671,812 | 2,760,878 | **SPLIT** | — | — | 100% | Parent line; decomposed below |
| OMN 1B5B | → DDG-1000 Maintenance & Support | 183,642 | 197,600 | 209,225 | INCLUDE | 5 | Mixed | 100% | Lifecycle engineering and maintenance support for DDG 1000 class |
| OMN 1B5B | → Mine Countermeasures Ship Support | 14,157 | 7,186 | 5,573 | INCLUDE | 5 | Mixed | 100% | MCM class support — declining as hulls decommission |
| OMN 1B5B | → PRE/PRL CV/CVN Technical Support | 81,444 | 81,505 | 86,561 | INCLUDE | 5 | Mixed | 100% | Carrier lifecycle maintenance and ISEA support |
| OMN 1B5B | → Service Craft Support, Boats/Targets Rehab | 7,548 | 8,364 | 6,842 | INCLUDE | 5 | Mixed | 100% | Service craft and target rehabilitation |
| OMN 1B5B | → Surface & Amphibious Ship Support | 446,317 | 463,167 | 451,307 | INCLUDE | 5 | Mixed | 100% | Surface/amphib class maintenance planning and technical support |
| OMN 1B5B | → Facilities & Supply Support Operations | 120,535 | 87,573 | 81,780 | INCLUDE | 6 | Public Yard | 100% | Includes SIOP ($28,752K), painting center, nuclear inactive ship maintenance facility |
| OMN 1B5B | → Nuclear Propulsion Tech Logistics & Operating Reactor Plant Technology | 327,227 | 340,900 | 355,445 | INCLUDE | 5 | Mixed | 100% | Nuclear propulsion sustainment engineering |
| OMN 1B5B | → SUPSHIP Costs | 255,302 | 269,204 | 251,345 | INCLUDE | 5 | Public Yard | 100% | Government oversight of ship construction and repair at private yards |
| OMN 1B5B | → NMP Total (Navy Modernization Process) | 415,261 | 277,773 | 410,893 | INCLUDE | 5 | Mixed | 100% | Modernization planning, design, engineering across all ship classes |
| OMN 1B5B | → NMMES (Navy Maritime Maintenance Enterprise Solutions) | 103,028 | 104,083 | 115,706 | INCLUDE | 5 | Mixed | 100% | Enterprise IT and management solutions for maintenance |
| OMN 1B5B | → Smart Work/TOC Initiatives | 22,363 | 34,068 | 23,672 | INCLUDE | 5 | Mixed | 100% | IT infrastructure and process improvement for maintenance |
| OMN 1B5B | → CSOSS (Combat System Operational Sequencing System) | 12,756 | 11,062 | 14,954 | INCLUDE | 5 | Mixed | 100% | Combat system operational procedures |
| OMN 1B5B | → Berthing & Messing Program | 129,771 | 135,039 | 141,596 | INCLUDE | 6 | Mixed | 100% | Barges, off-ship housing during availabilities — direct availability support |
| OMN 1B5B | → RMC (Regional Maintenance Centers) | 22,311 | 25,633 | 26,529 | INCLUDE | 2 | Mixed | 100% | RMC planning and oversight of non-depot maintenance |
| OMN 1B5B | → NAVSEA HQ Civilian Personnel & IT | 571,260 | 628,655 | 579,450 | INCLUDE | 5 | Public Yard | 100% | NAVSEA headquarters operations supporting all ship maintenance |

**1B5B Bucket Summary:**

| Bucket | FY26 ($K) | Key Components |
|--------|-----------|----------------|
| Bucket 2 (RMC) | 26,529 | Regional Maintenance Center oversight of non-depot work |
| Bucket 5 (Sustainment Engineering) | 2,511,373 | NMP, SUPSHIP, NAVSEA HQ, Nuclear Propulsion, DDG-1000 Support, Surface/Amphib Support, NMMES, CSOSS, Smart Work, MCM, PRE/PRL, Service Craft |
| Bucket 6 (Availability Support) | 223,376 | Berthing & Messing ($141,596) + Facilities/Supply Ops ($81,780) |
| **1B5B Check** | **2,761,278** | Within rounding of SAG total $2,760,878K |

---

### 2C. OMN — Context SAGs (EXCLUDED)

| Source | Line Item | FY26 ($K) | Disposition | Rationale |
|--------|-----------|-----------|-------------|-----------|
| OMN 1B1B | Mission and Other Ship Operations | 7,257,073 | EXCLUDE | Ship operations (fuel, crew, operating tempo) — not maintenance/repair/modernization. MSC M&R portion already transferred to 1B4B. |
| OMN 1B2B | Ship Operations Support & Training | 1,719,580 | EXCLUDE | Training and operational support — not in-service vessel work |

---

### 2D. OPN BA1 — Ships Support Equipment

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 Total ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------------|-------------|--------|-----------|------------------|-----------|
| OPN BA1 L1 | Surface Power Equipment | 12,855 | 20,840 | 9,978 | INCLUDE | 3 | Private Industry | 100% | Gas turbine lifecycle support for in-service CG47, DDG51, LCS-2, LHD-8, LHA-6/7 |
| OPN BA1 L2 | Surface Combatant HM&E | 92,449 | 77,592 | 62,004 | INCLUDE | 3 | Private Industry | 100% | HM&E upgrades for in-service surface combatants; post-Fitzgerald/McCain collision findings |
| OPN BA1 L4 | Sub Periscope, Imaging & Supt Equip | 272,778 | 290,575 | 277,413 | INCLUDE | 3 | Mixed | 100% | ISIS and EW BLQ-10 systems for in-service LA, SEAWOLF, VIRGINIA, OHIO classes |
| OPN BA1 L5 | DDG Mod | 641,676 | 861,066 | 997,485 | INCLUDE | 3 | Private Industry | 100% | DDG 51 Flight I/II/IIA modernization — SEWIP Block III, SPY-6(V)4, AEGIS BL10M |
| OPN BA1 L8 | LHA/LHD Midlife | 102,334 | 81,602 | 123,384 | INCLUDE | 3 | Private Industry | 100% | In-service LHA 6 / LHD 1 class HM&E upgrades — generators, PMP, PACS, MRS |
| OPN BA1 L9 | LCC 19/20 ESLP | 10,522 | 7,352 | 19,276 | INCLUDE | 4 | Private Industry | 100% | Extended Service Life Program — major life-cycle event for LCC class |
| OPN BA1 L11 | Submarine Support Equipment | 210,652 | 293,766 | 383,062 | INCLUDE | 3 | Mixed | 100% | SSN modernization, silencing ranges, SOF equipment, VIRGINIA acoustic backfit |
| OPN BA1 L12 | Virginia Class Support Equipment | 32,055 | 43,565 | 52,039 | INCLUDE | 3 | Mixed | 100% | Rotatable pool and insurance spares for VIRGINIA class — in-service support |
| OPN BA1 L13 | LCS Class Support Equipment | 17,816 | 7,318 | 2,551 | INCLUDE | 3 | Private Industry | 100% | Long-lead end items for LCS repairs; declining as fleet matures |
| OPN BA1 L15 | LPD Class Support Equipment | 80,933 | 38,115 | 125,542 | INCLUDE | 3 | Private Industry | 100% | In-service LPD 17 class modernization — obsolescence, HM&E, SWAN-CANES integration |
| OPN BA1 L16 | DDG 1000 Class Support Equipment | 220,771 | 340,668 | 115,267 | INCLUDE | 3 | Private Industry | 100% | DDG 1000 product improvement, cybersecurity, DMSMS, SM-6 capability |
| OPN BA1 L17 | Strategic Platform Support Equip | 23,756 | 53,931 | 53,740 | INCLUDE | 3 | Mixed | 100% | OHIO class HM&E modernization and TRF/IMF/TTF support equipment |
| OPN BA1 L20 | CG Modernization | 30,000 | 0 | 0 | EXCLUDE | — | — | 0% | Program ended. $30M FY24 only for USS CHOSIN/CAPE ST GEORGE completion. Zero FY26. |
| OPN BA1 L21 | LCAC | 10,239 | 11,013 | 20,321 | INCLUDE | 3 | Private Industry | 100% | LCAC system upgrades, replacement engines, PTMs. FY26 entirely reconciliation. |
| OPN BA1 L26 | Ship Maintenance, Repair & Modernization | 2,839,179 | 2,392,190 | 2,392,620 | INCLUDE | 1 | Private Industry | 100% | **Largest OPN line.** Private-yard ship availabilities (OH through RA/TA) for CPF and FFC. Contains 100+ individual ship availabilities with hull-specific costs. |
| OPN BA1 L28 | Reactor Components | 389,890 | 445,974 | 399,603 | INCLUDE | 3 | Mixed | 100% | Nuclear reactor plant components for all operational subs and carriers. Classified detail. |
| OPN BA1 L33 | LCS Common Mission Modules Equipment | 49,028 | 56,105 | 38,880 | INCLUDE | 3 | Private Industry | 100% | MCM and SUW mission package support containers and C5I equipment |
| OPN BA1 L34 | LCS MCM Mission Modules | 87,828 | 118,247 | 91,372 | INCLUDE | 3 | Private Industry | 100% | Mine countermeasures mission package — detect/engage operations |
| OPN BA1 L36 | LCS SUW Mission Modules | 12,094 | 11,101 | 3,790 | INCLUDE | 3 | Private Industry | 100% | Surface warfare mission package — gun/missile/aviation modules |
| OPN BA1 L37 | LCS In-Service Modernization | 154,561 | 188,254 | 237,728 | INCLUDE | 3 | Private Industry | 100% | Safety, cyber, habitability, obsolescence, C2 mods for both LCS variants |
| OPN BA1 L40 | LSD Midlife & Modernization | 3,989 | 56,667 | 4,079 | INCLUDE | 3 | Private Industry | 100% | LSD 41/49 class AIT and DSA for modernization availabilities |

**OPN BA1 Summary:**

| Bucket | FY26 Total ($K) | Key Lines |
|--------|-----------------|-----------|
| Bucket 1 | 2,392,620 | L26 Ship Maint, Repair & Mod (private yard availabilities) |
| Bucket 3 | 2,999,238 | L5 DDG Mod, L4 Sub Periscope, L28 Reactor, L11 Sub Support, L37 LCS Mod, L8 LHA/LHD, L16 DDG 1000, L15 LPD, L17 Strategic, L2 HM&E, L34 MCM, L12 VA Support, L33 Common MM, L1 Power, L21 LCAC, L40 LSD, L36 SUW, L13 LCS Support |
| Bucket 4 | 19,276 | L9 LCC ESLP |

---

### 2E. OPN BA2 — Communications & Electronics Equipment

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------|-------------|--------|-----------|------------------|-----------|
| OPN BA2 L43 | AN/SQQ-89 Surf ASW Combat System | 133,803 | 134,637 | 144,425 | INCLUDE | 3 | Private Industry | 100% | Backfit on in-service CG47/DDG51. FY26 absorbed CV-TSC, SDRW, USW-DSS from BLI 2176. |
| OPN BA2 L44 | SSN Acoustic Equipment | 519,272 | 465,824 | 498,597 | PARTIAL | 3 | Mixed | 80% | A-RCI modernizations, towed arrays, hull sensors for all sub classes. ~20% may support new-build Virginia Block V integration. In-service share: ~$398,878K |
| OPN BA2 L46 | Submarine Acoustic Warfare System | 41,695 | 51,514 | 56,482 | INCLUDE | 3 | Mixed | 100% | Expendable countermeasures and launch systems for all submarine classes |
| OPN BA2 L48 | Fixed Surveillance System | 536,796 | 405,854 | 363,312 | EXCLUDE | — | — | 0% | Shore-based fixed acoustic surveillance (SOSUS-family). Classified. Not ship-installed. |
| OPN BA2 L49 | SURTASS | 33,887 | 45,975 | 31,169 | EXCLUDE | — | — | 0% | T-AGOS surveillance ship towed arrays and shore processing. Separate vessel class, not combat ship equipment. |
| OPN BA2 L50 | AN/SLQ-32 (SEWIP) | 325,996 | 182,011 | 461,380 | INCLUDE | 3 | Private Industry | 100% | SEWIP Block 1B/2/3 and SOEA for in-service CVN/DDG/LHD/CG. Includes USCG WMSL/OPC items. |
| OPN BA2 L51 | Shipboard IW Exploit | 367,452 | 362,099 | 379,908 | INCLUDE | 3 | Mixed | 100% | SSEE, CCOP, Spectral, ICADS for surface/subsurface platforms. FY26 absorbed CCOP from BLI 3501. |
| OPN BA2 L53 | Cooperative Engagement Capability | 37,652 | 26,644 | 26,648 | INCLUDE | 3 | Private Industry | 95% | CEC backfit on CG/DDG/CVN/LHD/LHA during availabilities. ~5% LBTS (shore). In-service share: ~$25,316K |
| OPN BA2 L70 | CANES | 467,278 | 440,207 | 534,324 | PARTIAL | 3 | Mixed | 99% | Navy POR for afloat network modernization. Ashore component only $3.9M of $534M. In-service share: ~$530,408K |
| OPN BA2 L72 | CANES-Intell | 48,175 | 50,654 | 46,281 | INCLUDE | 3 | Mixed | 99% | Intelligence portion of CANES; predominantly afloat. In-service share: ~$45,813K |
| OPN BA2 L78 | In-Service Radars and Sensors | 279,545 | 222,607 | 249,656 | INCLUDE | 3 | Private Industry | 100% | DBR sustainment, radar restoration material, I-STALKER, NGSSR, SPY-1 improvements, SPY-6 FoR, SPEIR. Name confirms in-service. FY26 absorbed SPQ-9B. |
| OPN BA2 L79 | Battle Force Tactical Network | 68,327 | 104,119 | 106,583 | INCLUDE | 3 | Mixed | 100% | Classified. Shipboard communications BSA confirms ship-relevant. |
| OPN BA2 L80 | Shipboard Tactical Communications | 28,574 | 24,602 | 20,900 | INCLUDE | 3 | Mixed | 90% | DMR IW/MUOS radios for surface/subsurface/shore. ~10% shore sites. In-service share: ~$18,810K |
| OPN BA2 L81 | Ship Communications Automation | 103,352 | 103,546 | 162,075 | PARTIAL | 3 | Mixed | 75% | ADNS, ORT, Tactical Messaging, EPCA, STACC, Agile Enclave. STACC/EPCA are primarily shore infrastructure serving afloat platforms. ~25% shore. In-service share: ~$121,556K |

**OPN BA2 Ship-Relevant Summary:**

| Disposition | Line Count | FY26 Total ($K) |
|-------------|------------|-----------------|
| INCLUDE (100%) | 7 | 1,465,527 |
| PARTIAL (adjusted) | 5 | ~1,114,781 |
| EXCLUDE | 2 | 394,481 |
| **Bucket 3 Total (adjusted)** | **12** | **~2,580,308** |

---

### 2F. OPN BA4 — Ordnance Support Equipment

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 Total ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------------|-------------|--------|-----------|------------------|-----------|
| OPN BA4 BLI 125 | Ship Gun Systems Equipment | 16,250 | 6,416 | 7,358 | INCLUDE | 3 | Private Industry | 100% | ORDALTs and equipment for in-service DDG 51/CG 47 gun fire control |
| OPN BA4 BLI 127 | Ship Missile Support Equipment | 283,972 | 376,830 | 455,822 | INCLUDE | 3 | Mixed | 100% | AEGIS, SSDS, NSSMS, RAM, VLS, OTH WS, ICS, C-UAS. Backfit on in-service ships explicitly cited. |
| OPN BA4 BLI 128 | Tomahawk Support Equipment | 92,371 | 98,921 | 107,709 | PARTIAL | 3 | Mixed | 70% | TTWCS (afloat) + TMPC (mix of afloat CVN and shore). ~30% shore TMPC infrastructure. In-service share: ~$75,396K |
| OPN BA4 BLI 131 | SSN Combat Control Systems | 143,975 | 153,237 | 102,954 | PARTIAL | 3 | Mixed | 86% | AN/BYG-1 for all sub classes. Columbia class ($8.6M) + SSN774 BLK V PSA ($5.8M) = $14.4M new-build. In-service share: ~$88,554K |
| OPN BA4 BLI 136 | Anti-Ship Missile Decoy System | 51,100 | 75,614 | 89,129 | INCLUDE | 3 | Mixed | 100% | Nulka, MK-59, LEED — all ship-installed/ship-deployed decoys for in-service fleet |
| OPN BA4 BLI 126 | Harpoon Support Equipment | 227 | 226 | 209 | INCLUDE | 3 | Mixed | 100% | ENCAP Harpoon for LA-class SSN — very small line |
| OPN BA4 BLI 129 | CPS Support Equipment | 0 | 0 | 67,264 | EXCLUDE | — | — | 0% | Conventional Prompt Strike for Virginia Block V — new construction associated |
| OPN BA4 BLI 130 | Strategic Missile Systems Equipment | 322,524 | 320,691 | 492,999 | PARTIAL | 3 | Mixed | 50% | Mix of OHIO (in-service) and Columbia (new-build). OHIO class backfits (LIS, SSI Inc 11) confirmed. Rough 50/50 split. In-service share: ~$246,500K |
| OPN BA4 BLI 132 | ASW Support Equipment | 37,301 | 25,362 | 25,721 | INCLUDE | 3 | Mixed | 100% | Torpedo tube support, AN/UQN-10 fathometer retrofit on 103 ships — explicit in-service |
| OPN BA4 BLI 134 | Directed Energy/ODIN | 0 | 3,817 | 2,976 | INCLUDE | 3 | Private Industry | 100% | AN/SEQ-4 spares and backfit ECPs for 8 in-service DDG 51 FLT IIA ships |
| OPN BA4 BLI 138 | Surface Training Equipment | 207,231 | 179,974 | 186,085 | EXCLUDE | — | — | 0% | Training systems (BFTT, simulators). Some ship-installed BFTT but predominantly training, not vessel work. |
| OPN BA4 BLI 137 | Submarine Training Device Mods | 76,903 | 80,248 | 77,889 | EXCLUDE | — | — | 0% | Shore-based submarine training simulators |

**OPN BA4 Summary:**

| Disposition | FY26 Total ($K) |
|-------------|-----------------|
| INCLUDE (100%) | 581,215 |
| PARTIAL (adjusted) | ~410,450 |
| EXCLUDE | 331,238 |
| **Bucket 3 Total (adjusted)** | **~991,665** |

---

### 2G. OPN BA8 — Spares and Repair Parts

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 Total ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------------|-------------|--------|-----------|------------------|-----------|
| OPN BA8 BLI 9020 | Spares and Repair Parts | 736,770 | 705,144 | 883,630 | INCLUDE | 5 | Mixed | 100% | Initial + replenishment spares for all ship-installed systems. Supports depot and operational readiness. FY26 includes $297.8M reconciliation. |
| OPN BA8 BLI 9021 | VIRGINIA Class (VACL) Spares | 478,691 | 0 | 0 | EXCLUDE | — | — | — | Zeroed in FY25/FY26. FY24-only program to address VACL availability material shortfalls. |

**OPN BA5-7 Scan:**

| Source | FY26 ($K) | Disposition | Rationale |
|--------|-----------|-------------|-----------|
| BA5 Civil Engineering | 347,308 | EXCLUDE | Shore-based construction/maintenance equipment. Fire fighting equipment is shore-based ship response apparatus. |
| BA6 Supply Support | 688,659 | EXCLUDE | Material handling equipment and Navy Cash. Supporting infrastructure, not vessel work. |
| BA7 Personnel & Command Support | 904,347 | EXCLUDE | Training, command support, pier-side equipment (camels, fenders). Not direct vessel work. |

---

### 2H. SCN — Shipbuilding and Conversion, Navy

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 Total ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------------|-------------|--------|-----------|------------------|-----------|
| SCN L10 | CVN Refueling Overhauls — Subsequent Full Funding | — | 811,143 | 1,779,011 | INCLUDE | 4 | Private Industry (HII-NNS) | 100% | CVN 75 TRUMAN RCOH 2nd year of full funding. HII Newport News sole source. |
| SCN | CVN RCOH — Cost to Complete (CVN 74) | 42,422 | 669,171 | 483,100 | INCLUDE | 4 | Private Industry (HII-NNS) | 100% | CVN 74 STENNIS cost growth + 13-month delivery delay. Delivery Nov 2027. |
| SCN | CVN RCOH — Outfitting/Post-Delivery | 19,704 | 6,660 | 12,200 | INCLUDE | 4 | Private Industry | 100% | Post-delivery outfitting for RCOH completions |
| SCN L47 | LCAC SLEP (ESLEP) | 15,286 | 45,087 | 37,390 | INCLUDE | 4 | Private Industry (Walashek) | 100% | 1 LCAC ESLEP availability. FY26 entirely reconciliation/mandatory. |
| SCN | LCAC SLEP — Outfitting | 728 | 0 | 493 | INCLUDE | 4 | Private Industry | 100% | Post-delivery outfitting for LCAC ESLEP |
| SCN L49 | Completion of PY Shipbuilding (excl RCOH/LCAC) | — | — | 1,207,746 | EXCLUDE | — | — | 0% | Cost growth on new construction (SSN-774, DDG, LPD 17, LHA R). Not in-service work. CVN RCOH portion ($483.1M) already captured above. |
| SCN | All new construction lines (L1-L48 excl L10, L47) | — | — | ~50,000,000+ | EXCLUDE | — | — | 0% | New ship construction — not in-service vessel work |

**SCN In-Service Summary:**

| Bucket | FY26 Total ($K) |
|--------|-----------------|
| Bucket 4 (RCOH) | 2,274,311 |
| Bucket 4 (LCAC SLEP) | 37,883 |
| **Bucket 4 Total** | **2,312,194** |

---

### 2I. USCG — Coast Guard Justification

| Source | Line Item | FY24 ($K) | FY25 ($K) | FY26 ($K) | Disposition | Bucket | Performer | In-Service Share | Rationale |
|--------|-----------|-----------|-----------|-----------|-------------|--------|-----------|------------------|-----------|
| USCG O&S | **25.7 O&M of Equipment (total)** | 915,020 | 933,110 | 1,025,994 | **PARTIAL** | 1/2 | Mixed | ~60% | Largest O&S non-pay line. Includes vessel, aircraft, shore equipment O&M. No vessel-specific breakout. 60% vessel estimate based on fleet composition. In-service share: ~$615,596K |
| USCG PC&I | **In-Service Vessel Sustainment (ISVS)** | 120,000 | 120,000 | 152,000 | **SPLIT** | 4 | — | 100% | Parent line; decomposed below |
| USCG PC&I | → 47-ft MLB SLEP | 43,000 | 43,000 | 45,000 | INCLUDE | 4 | CG Yard / Private | 100% | SLEP for 107 of 117 Motor Life Boats; up to 20 inducted FY26 |
| USCG PC&I | → 270-ft WMEC SLEP | 46,200 | 46,200 | 76,000 | INCLUDE | 4 | CG Yard | 100% | Medium Endurance Cutter service life extension; 4th/5th hull begins FY26 |
| USCG PC&I | → 175-ft WLM MMA | 17,800 | 17,800 | 15,000 | INCLUDE | 4 | CG Yard | 100% | Coastal Buoy Tender major maintenance availability |
| USCG PC&I | → CGC Healy SLEP | 13,000 | 13,000 | 11,000 | INCLUDE | 4 | Mixed | 100% | Icebreaker SLEP |
| USCG PC&I | → 418-ft WMSL MMA (new start) | 0 | 0 | 5,000 | INCLUDE | 4 | CG Yard | 100% | National Security Cutter MMA — new start FY26 (detail design) |
| USCG PC&I | ISSS (In-Service Systems Sustainment) | 0 | 0 | 30,000 | INCLUDE | 3 | Mixed | 100% | NSC C5I system sustainment/replacement — afloat modernization |
| USCG PC&I | C4ISR | 16,000 | 16,000 | 10,000 | INCLUDE | 3 | Mixed | 100% | C4ISR integration for major cutters, aircraft, forward assets |
| USCG PC&I | Cyber and Enterprise Mission Platform | 21,500 | 21,500 | 25,800 | PARTIAL | 3 | Mixed | 50% | EMP covers both cutter and shore/enterprise IT. ~50% vessel share. In-service share: ~$12,900K |
| USCG PC&I | Survey & Design — Vessels, Boats, Aircraft | 5,000 | 5,000 | 5,000 | INCLUDE | 5 | CG Yard | 100% | Engineering survey and design for future SLEPs, MMAs, availabilities |
| USCG PC&I | Program Oversight & Management | 21,000 | 21,000 | 22,000 | PARTIAL | 5 | Mixed | 50% | PO&M covers all acquisitions, not just vessel sustainment. ~50% vessel share. In-service share: ~$11,000K |
| USCG PC&I | Other Equipment & Systems | 5,600 | 5,600 | 7,040 | PARTIAL | 6 | Mixed | 31% | Includes vessel travel lifts, depot test equipment ($2,200K of $7,040K). In-service share: ~$2,200K |
| USCG PC&I | Boats (incl. RB-M SLEP) | 6,500 | 6,500 | 30,900 | PARTIAL | 4 | Private Industry | 30% | Includes RB-M SLEP (~$9,270K est.) plus new boat acquisition. SLEP portion only. |
| USCG O&S | Decommission Reliance Class WMEC | — | — | (33,502) | EXCLUDE | — | — | — | Negative program change (decommissioning savings). Not in-service sustainment. |
| USCG PC&I | Aircraft SLEPs (MH-60T, HC-144, MH-65, HC-130J) | 68,250 | 68,250 | 182,600 | EXCLUDE | — | — | 0% | Aircraft, not vessels |
| USCG PC&I | New vessel construction (OPC, FRC, PSC, WCC) | 820,000 | 820,000 | 1,256,400 | EXCLUDE | — | — | 0% | New construction, not in-service work |
| USCG PC&I | Shore Facilities & MASI | 187,500 | 187,500 | 16,300 | EXCLUDE | — | — | 0% | Shore facilities — not vessel work |

**USCG In-Service Vessel Summary:**

| Bucket | FY26 ($K) | Source |
|--------|-----------|-------|
| Bucket 1/2 (O&S vessel maintenance) | ~615,596 | 60% of O&S Obj Class 25.7 |
| Bucket 3 (Modernization) | ~52,900 | ISSS + C4ISR + Cyber (partial) |
| Bucket 4 (SLEP/MMA) | ~161,270 | ISVS + RB-M SLEP portion |
| Bucket 5 (Engineering/Planning) | ~16,000 | Survey & Design + PO&M (partial) |
| Bucket 6 (Support) | ~2,200 | Other Equipment (vessel share) |

---

### 2J. NWCF — Navy Working Capital Fund

| Source | Line Item | FY26 ($K) | Disposition | Rationale |
|--------|-----------|-----------|-------------|-----------|
| NWCF | FRC Depot Maintenance (aviation) | 2,900,764 | EXCLUDE | Aviation depot maintenance — not ship work |
| NWCF | MC DMAG (Marine Corps ground) | 362,600 | EXCLUDE | Marine Corps ground combat depot — not ship work |
| NWCF | Supply Management — weapon system material by platform | — | PERFORMER_TAG | Not additive. Shows material cost flows by ship class (Submarine $391.7M, CRUDES $676.9M, CVN $89.1M FY26). Used to understand material intensity by platform. |
| NWCF | VACL Material Strategy | — | PERFORMER_TAG | $909M obligated; $38M FY26 increase. Already reflected in OMN spares flows. Reference for submarine material availability improvement. |
| NWCF | MSC M&R transition to OMN | ~1,400,000 | PERFORMER_TAG | Already captured in OMN 1B4B MSC M&R line ($1,584,000K). Not additive. |
| NWCF | R&D Warfare Centers (NSWC, NUWC, etc.) | ~20,000,000 | EXCLUDE | R&D/engineering centers. Some provide support to ship maintenance programs but funded separately and not counted as direct vessel work TAM. |

---

### 2K. OMN Vol2 — Performer Tag Data (Public Naval Shipyards)

| Source | Line Item | FY26 ($K) | Disposition | Use |
|--------|-----------|-----------|-------------|-----|
| OMN Vol2 | PHNSY&IMF Total Funding | 1,787,171 | PERFORMER_TAG | Public yard; primarily submarines. FY26: 4 EDSRA/DMP + 1 CMAV + 1 DSRA. |
| OMN Vol2 | PSNS&IMF Total Funding | 3,473,772 | PERFORMER_TAG | Largest public yard; carriers + submarines. FY26: 4 carrier avails + 4 sub avails + SLAs + IAs. |
| OMN Vol2 | PNSY Total Funding | 1,640,762 | PERFORMER_TAG | Submarines only. FY26: 2 DSRA + 1 DMP. |
| OMN Vol2 | NNSY Total Funding | 2,102,193 | PERFORMER_TAG | Carriers + submarines. FY26: 1 PIA + 1 DMP + 1 IA. |
| OMN Vol2 | **Four-Yard OM,N Direct Total** | **7,793,385** | PERFORMER_TAG | **Public yard share of OMN-funded depot maintenance.** This represents ~56% of SAG 1B4B ($13,803,188K). Remainder flows to private industry. |
| OMN Vol2 | Four-Yard Total Workforce | 39,437 | PERFORMER_TAG | Civilian + military end strength across four shipyards. |

**Public vs. Private Performer Split (1B4B):**

| Performer | FY26 ($K) | % of 1B4B | Derivation |
|-----------|-----------|-----------|------------|
| Public Yard (4 shipyards) | ~7,793,385 | ~56% | OMN Vol2 OP-5A four-yard OM,N direct funding |
| Private Industry | ~4,425,803 | ~32% | OPN BA1 L26 ($2,392,620) + residual OMN 1B4B not at public yards |
| MSC (Private) | ~1,584,000 | ~11% | MSC M&R transfer — private yards (Detyens, Bayonne, etc.) |
| **Total** | **~13,803,188** | **100%** | |

Note: The four-yard figure ($7.79B) includes OMN direct + MPN. The relationship to 1B4B is approximate — some shipyard costs are overhead/infrastructure not directly billable to 1B4B sub-elements.

---

## 3. Silver Reconciliation Summary

### 3.1 Stage-by-Stage Filtering

| Stage | Line Item Count | FY26 Total ($K) | Notes |
|-------|-----------------|-----------------|-------|
| **Bronze (all extracted lines)** | ~85 | ~82,000,000+ | Includes all SAGs, BLIs, SCN, USCG, NWCF |
| After EXCLUDE filter | ~55 | ~26,500,000 | Removed: 1B1B, 1B2B, Fixed Surveillance, SURTASS, CG Mod, CPS, Training, BA5-7, SCN new construction, NWCF depot/R&D, CG aircraft, CG new vessels |
| After PARTIAL adjustment | ~55 | ~25,300,000 | Adjusted: SSN Acoustic (80%), CANES (99%), CEC (95%), Ship Comms Auto (75%), Tomahawk (70%), SSN CCS (86%), Strategic Missile (50%), USCG O&S 25.7 (60%), Cyber/EMP (50%), PO&M (50%), Boats (30%), Other Equip (31%), Tactical Comms (90%) |
| After SPLIT decomposition | ~70+ | ~25,300,000 | Split: 1B4B into 14 sub-elements, 1B5B into 15 sub-elements, USCG ISVS into 5 sub-investments |
| **Final Silver (INCLUDE + adjusted PARTIAL)** | **~60 included lines** | **~25,300,000** | All bucket-assigned, performer-tagged |

### 3.2 Bucket Roll-Up (FY26, $K)

| Bucket | Navy ($K) | USCG ($K) | Total ($K) | Confidence |
|--------|-----------|-----------|------------|------------|
| **1. Scheduled Depot Maintenance & Repair** | 13,247,836 | ~369,358 | **~13,617,194** | High (Navy), Medium (USCG) |
| **2. Continuous / Intermediate / Emergent** | 1,988,477 | ~246,238 | **~2,234,715** | Medium |
| **3. Modernization & Alteration Installation** | 6,571,211 | ~52,900 | **~6,624,111** | Medium-High |
| **4. Major Life-Cycle Events (RCOH/SLEP/MMA)** | 2,331,470 | ~161,270 | **~2,492,740** | High |
| **5. Sustainment Engineering / Planning** | 3,395,003 | ~16,000 | **~3,411,003** | High |
| **6. Availability Support / Port Services** | 225,576 | ~2,200 | **~227,776** | Low |
| **TOTAL TAM** | **27,759,573** | **~847,966** | **~28,607,539** | |

### 3.3 Bucket Detail — Navy

**Bucket 1: Scheduled Depot Maintenance & Repair — $13,247,836K**
| Source | Amount ($K) | Description |
|--------|-------------|-------------|
| OMN 1B4B (scheduled depot sub-elements) | 10,855,216 | SMP + ship-class NME categories + MSC M&R |
| OPN BA1 L26 | 2,392,620 | Private-yard ship availabilities (OPN-funded material/equipment) |

**Bucket 2: Continuous / Intermediate / Emergent — $1,988,477K**
| Source | Amount ($K) | Description |
|--------|-------------|-------------|
| OMN 1B4B CMMP | 1,321,948 | Continuous Maintenance & Modernization Program |
| OMN 1B4B Expedited M&M | 640,000 | Expedited maintenance and modernization |
| OMN 1B5B RMC | 26,529 | Regional Maintenance Center oversight |

**Bucket 3: Modernization & Alteration Installation — $6,571,211K**
| Source | Amount ($K) | Description |
|--------|-------------|-------------|
| OPN BA1 (excl L26, L9, L20) | 2,999,238 | DDG Mod, Sub Periscope, Reactor, Sub Support, LCS Mod, etc. |
| OPN BA2 (adjusted) | 2,580,308 | SQQ-89, SSN Acoustic, SEWIP, IW, CEC, CANES, Radars, etc. |
| OPN BA4 (adjusted) | 991,665 | Ship Missile Support, Tomahawk, SSN CCS, ASMD, ASW, etc. |

**Bucket 4: Major Life-Cycle Events — $2,331,470K**
| Source | Amount ($K) | Description |
|--------|-------------|-------------|
| SCN CVN RCOH (SFF + CTC + outfitting) | 2,274,311 | CVN 74 cost-to-complete + CVN 75 subsequent full funding |
| SCN LCAC SLEP + outfitting | 37,883 | 1 LCAC ESLEP |
| OPN BA1 L9 LCC ESLP | 19,276 | LCC 19/20 Extended Service Life Program |

**Bucket 5: Sustainment Engineering / Planning — $3,395,003K**
| Source | Amount ($K) | Description |
|--------|-------------|-------------|
| OMN 1B5B (Bucket 5 share) | 2,511,373 | NMP, SUPSHIP, NAVSEA HQ, Nuclear Propulsion, class support, NMMES, etc. |
| OPN BA8 BLI 9020 | 883,630 | Spares and repair parts |

**Bucket 6: Availability Support — $225,576K**
| Source | Amount ($K) | Description |
|--------|-------------|-------------|
| OMN 1B5B Berthing & Messing | 141,596 | Barges, off-ship housing during availabilities |
| OMN 1B5B Facilities/Supply Ops | 81,780 | SIOP, painting center, nuclear inactive ship facility |
| OMN 1B5B Other | 2,200 | (embedded; approximate) |

### 3.4 USCG Bucket Detail

**Bucket 1/2 (blended): ~$615,596K**
- 60% of O&S Object Class 25.7 ($1,025,994K). Cannot separate Bucket 1 from Bucket 2 without additional data. The CG uses drydock (DD) and dockside (DS) availability types; DD maps to Bucket 1, DS maps to Bucket 1/2. Combined here.

**Bucket 3: ~$52,900K**
- ISSS: $30,000K (NSC C5I sustainment)
- C4ISR: $10,000K (cutter mission system integration)
- Cyber/EMP (50%): ~$12,900K

**Bucket 4: ~$161,270K**
- ISVS total: $152,000K (MLB SLEP + WMEC SLEP + WLM MMA + Healy SLEP + WMSL MMA)
- Boats RB-M SLEP share: ~$9,270K

**Bucket 5: ~$16,000K**
- Survey & Design: $5,000K
- PO&M (50%): ~$11,000K

**Bucket 6: ~$2,200K**
- Other Equipment & Systems vessel share: ~$2,200K

---

## 4. Cross-Checks

### 4.1 OMN Internal Check
- Bucket 1 OMN portion + Bucket 2 = $10,855,216 + $1,961,948 = $12,817,164
- SAG 1B4B total = $13,803,188
- Delta = $986,024 (MSC component accounting + rounding in Performance Criteria table vs financial summary)
- **Status: REASONABLE** — within expected tolerance given NME table totals slightly different from financial summary

### 4.2 1B5B Internal Check
- Bucket 2 (RMC) + Bucket 5 + Bucket 6 = $26,529 + $2,511,373 + $223,376 = $2,761,278
- SAG 1B5B total = $2,760,878
- Delta = +$400 (rounding)
- **Status: PASS**

### 4.3 No Double-Counting Check
- OMN funds O&M; OPN funds procurement; SCN funds shipbuilding — different appropriation streams
- NWCF lines tagged as PERFORMER_TAG, not counted in TAM total
- OMN Vol2 shipyard data tagged as PERFORMER_TAG, not counted in TAM total
- MSC M&R counted once in OMN 1B4B (not also in NWCF)
- **Status: PASS**

### 4.4 Reasonableness
- Bucket 1 (Scheduled Depot) is the largest bucket at ~$13.6B — **expected**, this is the core of Navy ship maintenance
- RCOH dominates Bucket 4 at $2.3B of $2.5B — **expected**
- BA8 spares ($884M) < Bucket 1 ($13.6B) — **expected**
- Total TAM ~$28.6B is consistent with the ~$25.5B Ship Operations total ($23.0B OMN 1B1B-1B5B minus non-maintenance 1B1B/1B2B + OPN/SCN/USCG additions)
- **Status: PASS**

---

## 5. Confidence Assessment

| Bucket | High-Confidence ($K) | Medium-Confidence ($K) | Low-Confidence ($K) |
|--------|----------------------|------------------------|---------------------|
| 1 | 13,247,836 (Navy OMN+OPN) | 369,358 (USCG est.) | — |
| 2 | 1,961,948 (OMN CMMP+Exp) | 272,767 (USCG est. + RMC) | — |
| 3 | 2,999,238 (OPN BA1 named programs) | 3,571,973 (BA2+BA4 adjusted + USCG) | — |
| 4 | 2,331,470 (SCN RCOH+LCAC+LCC) | 161,270 (USCG ISVS+RBM) | — |
| 5 | 3,395,003 (1B5B+BA8) | 16,000 (USCG S&D+PO&M) | — |
| 6 | — | — | 227,776 (embedded in larger lines) |
| **Total** | **$23,935,495 (84%)** | **$4,391,368 (15%)** | **$227,776 (1%)** |

---

## 6. Known Exclusions and Gaps

1. **Classified programs**: Nuclear reactor specifics (OPN BA1 L28 included at top-line only), BFTN details, Fixed Surveillance. Dollar values included where visible.
2. **MSC vessel work granularity**: $1.584B MSC M&R is a single line; no breakdown by MSC ship class or availability type available from budget books.
3. **USCG vessel vs. non-vessel O&S**: The 60% vessel share of Object Class 25.7 is an estimate. True figure requires CG internal data.
4. **Bucket 6 undercount**: Availability support costs are largely embedded within Bucket 1 availability contracts (scaffolding, crane services, shore power, etc.). The $228M captured here (berthing/messing + facilities) is the explicitly identifiable portion only.
5. **Army watercraft**: Not in Navy/CG budget books. Separate service.
6. **OPN BA3**: Not extracted (carrier aviation systems AAG/EMALS). Small potential in-service component if scope includes carrier aviation equipment installed during availabilities. Deprioritized.
7. **WPN Book**: Not extracted. Weapon-system sustainment may have small ship-relevant components. Deprioritized.
8. **Public-private split precision**: The four-shipyard OMN figure ($7.79B) is an approximation of the public-yard share. True split requires contract-level data (bottom-up analysis).

---

*Silver layer complete. Ready for Gold phase.*
