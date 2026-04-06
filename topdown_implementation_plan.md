# Top-Down TAM Analysis — Implementation Plan

## Objective

Extract dollar figures from Navy and Coast Guard budget/justification books to size each of the six in-service vessel work buckets from the top down. The output is a bucket-by-bucket spend table with FY columns, traceable page references, and notes on what is included/excluded.

---

## The Six Buckets

| # | Bucket | Primary Budget Source(s) |
|---|--------|--------------------------|
| 1 | Scheduled depot maintenance & repair | OMN (SAG 1B4B), NWCF, USCG O&S |
| 2 | Continuous / intermediate / emergent maintenance | OMN (1B4B sub-elements: CMAV, ERATA, ORATA, IL) |
| 3 | Modernization & alteration installation | OPN BA1, OPN BA2, OPN BA4 (selective), USCG PC&I |
| 4 | Major life-cycle events / service-life extension | SCN (RCOH), OPN BA1 (LCC ESLP, LCAC SLEP), USCG PC&I (SLEP/MMA) |
| 5 | Sustainment engineering / planning / obsolescence support | OMN (SAG 1B5B), OPN BA8 (spares) |
| 6 | Availability support / husbanding / port services | OMN (within 1B4B/1B5B sub-elements), USCG O&S |

---

## Source Files

All located in `topdown/sources/`.

| Priority | File | Format | Status | Used For |
|----------|------|--------|--------|----------|
| 0 | `Supp_Book.pdf` → `Supp_Book.txt` | PDF → Text | **Needs conversion via `pdftotext -layout`** | O-1 and P-1 supporting exhibits — the map for everything else |
| 1 | `OMN_Book.txt` | Text | Ready | Buckets 1, 2, 5, 6 (core) |
| 2 | `OMN_Vol2_Book.txt` | Text | Ready | Fine-grain detail under OMN lines |
| 3 | `OPN_BA1_Book.txt` | Text | Ready | Bucket 3 (DDG Mod, LCS Mod, LHA/LHD Midlife, etc.) and Bucket 4 (LCC ESLP) |
| 4 | `OPN_BA2_Book.txt` | Text | Ready | Bucket 3 (combat systems, sensors, electronics backfit) |
| 5 | `OPN_BA5-8_Book.txt` | Text | Ready | Bucket 5 (BA8 spares and repair parts only) |
| 6 | `OPN_BA4_Book.txt` | Text | Ready | Bucket 3 (weapon-system backfit — selective, only if in scope) |
| 7 | `SCN_Book.txt` | Text | Ready | Bucket 4 (RCOH, LCAC SLEP, major life-cycle events) |
| 8 | `USCG_Justification.txt` | Text | Ready | All buckets, Coast Guard side (SLEP, MMA, dry-dock, dockside, survey & design) |
| 9 | `NWCF_Book.txt` | Text | Ready | Public-yard depot work — used to identify the public-yard share of OMN-funded maintenance (not additive to OMN; decomposes the same dollars by performer) |
| ~~10~~ | ~~`president_budget_fy2027.txt`~~ | ~~Text~~ | ~~Ready~~ | ~~Removed — FY27 book; using FY26 justification books only~~ |
| — | `OPN_BA3_Book.txt` | Text | Ready | Low priority — carrier aviation systems (AAG, EMALS) edge case |
| — | `WPN_Book.txt` | Text | Ready | Deprioritized unless weapon-system sustainment is in scope |

---

## Phase 0: Convert Supporting Exhibits PDF to Text

The `Supp_Book.pdf` has not been converted to text yet. This must happen first — it is the map that tells us where to look in every other book.

```bash
pdftotext -layout topdown/sources/Supp_Book.pdf topdown/sources/Supp_Book.txt
```

Verify the output is readable and the tabular structure (SAG numbers, BLI numbers, dollar columns) survived the conversion. The `-layout` flag is critical — without it, the columnar budget tables become unreadable.

---

## Phase 1: Read the Map (Supporting Exhibits)

**Source:** `Supp_Book.txt`

The Supp Book contains both the O-1 (O&M summary) and P-1 (Procurement summary) exhibits. Below is the complete extraction target list derived from the actual Supp Book content.

### O-1 Exhibit: Navy O&M Lines (all $ in thousands)

The Ship Operations section of O-1 contains four SAGs. All are relevant:

| SAG | Title | FY24 Actual | FY25 Enacted | FY26 Request | Buckets |
|-----|-------|-------------|--------------|--------------|---------|
| 1B1B | Mission and Other Ship Operations | $7,460,169 | $7,258,014 | $7,257,073 | Context (not directly a bucket, but may contain enabling spend) |
| 1B2B | Ship Operations Support & Training | $1,372,331 | $1,536,668 | $1,719,580 | Context |
| **1B4B** | **Ship Depot Maintenance** | **$11,502,495** | **$11,763,594** | **$13,803,188** | **Buckets 1, 2, 6** (need to decompose sub-elements) |
| **1B5B** | **Ship Depot Operations Support** | **$2,714,238** | **$2,671,812** | **$2,760,878** | **Bucket 5** (and possibly part of 6) |
| | Total Ship Operations | $23,049,233 | $23,230,088 | $25,540,719 | |

**Key insight:** 1B4B ($13.8B) is the single largest line and must be decomposed into Bucket 1 (scheduled depot), Bucket 2 (continuous/intermediate/emergent), and Bucket 6 (availability support). The OMN detail book (OMN_Book.txt and OMN_Vol2_Book.txt) will show the sub-element breakdown.

### P-1 Exhibit: OPN Budget Activity Summary

| BA | Title | FY24 Actual | FY25 Enacted | FY26 Request | FY26 Total (w/ Reconcil) | Buckets |
|----|-------|-------------|--------------|--------------|--------------------------|---------|
| **01** | **Ships support equipment** | **$6,113,468** | **$6,390,236** | **$5,378,816** | **$8,021,677** | **Buckets 3, 4** |
| **02** | **Communications and electronics equipment** | **$4,152,244** | **$3,927,280** | **$4,508,845** | **$4,519,845** | **Bucket 3** (selective — ship-installed only) |
| 03 | Aviation support equipment | $906,795 | $889,155 | $814,932 | $894,932 | Low priority edge case |
| **04** | **Ordnance support equipment** | **$1,262,194** | **$1,351,254** | **$1,572,752** | **$1,644,572** | **Bucket 3** (selective — ship weapon systems only) |
| 05 | Civil engineering support equipment | $186,641 | $260,583 | $347,308 | $347,308 | Skip |
| 06 | Supply support equipment | $698,653 | $1,063,444 | $688,659 | $688,659 | Skip |
| 07 | Personnel and command support equipment | $600,986 | $555,677 | $672,347 | $904,347 | Skip |
| **08** | **Spares and repair parts** | **$1,215,461** | **$705,144** | **$585,865** | **$883,630** | **Bucket 5** |
| | **Total OPN** | **$15,136,442** | **$15,142,773** | **$14,569,524** | **$17,904,970** | |

### P-1 Exhibit: OPN BA1 Line Items Relevant to In-Service Vessel Work

These are the specific BLIs within BA1 "Ships support equipment" that map to the six buckets:

| Line # | Item | FY24 Actual | FY25 Enacted | FY26 Request | FY26 Total | Bucket |
|--------|------|-------------|--------------|--------------|------------|--------|
| 1 | Surface Power Equipment | $12,855 | $20,840 | $9,978 | $9,978 | 3 |
| 2 | Surface Combatant HM&E | $92,449 | $77,592 | $62,004 | $62,004 | 3 |
| 4 | Sub Periscope, Imaging and Supt Equip Prog | $272,778 | $290,575 | $135,863 | $277,413 | 3 |
| **5** | **DDG Mod** | **$641,676** | **$861,066** | **$686,787** | **$997,485** | **3** |
| **8** | **LHA/LHD Midlife** | **$102,334** | **$81,602** | **$86,884** | **$123,384** | **3 or 4** |
| **9** | **LCC 19/20 Extended Service Life Program** | **$10,522** | **$7,352** | **$19,276** | **$19,276** | **4** |
| 11 | Submarine Support Equipment | $210,652 | $293,766 | $383,062 | $383,062 | 3 (sub-specific) |
| 12 | Virginia Class Support Equipment | $32,055 | $43,565 | $52,039 | $52,039 | 3 (sub-specific) |
| 13 | LCS Class Support Equipment | $17,816 | $7,318 | $2,551 | $2,551 | 3 |
| 15 | LPD Class Support Equipment | $80,933 | $38,115 | $101,042 | $125,542 | 3 |
| 16 | DDG 1000 Class Support Equipment | $220,771 | $340,668 | $115,267 | $115,267 | 3 |
| 17 | Strategic Platform Support Equip | $23,756 | $53,931 | $38,039 | $53,740 | 3 |
| 20 | CG Modernization | $30,000 | — | — | — | 3 (ended?) |
| 21 | LCAC | $10,239 | $11,013 | — | $20,321 | 3 or 4 |
| **26** | **Ship Maintenance, Repair and Modernization** | **$2,839,179** | **$2,392,190** | **$2,392,620** | **$2,392,620** | **3** (largest single line — needs detail book decomposition) |
| 28 | Reactor Components | $389,890 | $445,974 | $399,603 | $399,603 | 3 (nuclear-specific) |
| 33 | LCS Common Mission Modules Equipment | $49,028 | $56,105 | $38,880 | $38,880 | 3 |
| 34 | LCS MCM Mission Modules | $87,828 | $118,247 | $91,372 | $91,372 | 3 |
| 36 | LCS SUW Mission Modules | $12,094 | $11,101 | $3,790 | $3,790 | 3 |
| **37** | **LCS In-Service Modernization** | **$154,561** | **$188,254** | **$203,442** | **$237,728** | **3** |
| 40 | LSD Midlife & Modernization | $3,989 | $56,667 | $4,079 | $4,079 | 3 or 4 |

**Key insight:** Line 26 "Ship Maintenance, Repair and Modernization" at **$2.4B** is the single largest BA1 line. The detail book (OPN_BA1_Book.txt) must be opened to understand what this actually funds and how it splits across buckets.

### P-1 Exhibit: OPN BA2 Ship-Relevant Line Items

Not everything in BA2 is ship-installed. The following are the ship-relevant lines:

| Line # | Item | FY24 Actual | FY25 Enacted | FY26 Request | Bucket |
|--------|------|-------------|--------------|--------------|--------|
| 43 | AN/SQQ-89 Surf ASW Combat System | $133,803 | $134,637 | $144,425 | 3 |
| 44 | SSN Acoustic Equipment | $519,272 | $465,824 | $498,597 | 3 |
| 46 | Submarine Acoustic Warfare System | $41,695 | $51,514 | $56,482 | 3 |
| 50 | AN/SLQ-32 (EW) | $325,996 | $182,011 | $461,380 | 3 |
| 51 | Shipboard IW Exploit | $367,452 | $362,099 | $379,908 | 3 |
| 53 | Cooperative Engagement Capability | $37,652 | $26,644 | $26,648 | 3 |
| 70 | CANES | $467,278 | $440,207 | $534,324 | 3 |
| 72 | CANES-Intell | $48,175 | $50,654 | $46,281 | 3 |
| 78 | In-Service Radars and Sensors | $279,545 | $222,607 | $249,656 | 3 |
| 79 | Battle Force Tactical Network | $68,327 | $104,119 | $106,583 | 3 |
| 80 | Shipboard Tactical Communications | $28,574 | $24,602 | $20,900 | 3 |
| 81 | Ship Communications Automation | $103,352 | $103,546 | $162,075 | 3 |

**Important filter:** Many BA2 lines (e.g., Fixed Surveillance System $352M, SURTASS $31M, ashore ATC, shore electronics) are NOT ship-installed and must be excluded. Only include items that are physically installed or backfit onto in-service vessels. The detail book will help distinguish — look for descriptions mentioning "ship-installed", "backfit", "fleet upgrade", or specific hull designations.

### P-1 Exhibit: OPN BA4 Ship-Relevant Line Items

| Line # | Item | FY24 Actual | FY25 Enacted | FY26 Request | Bucket |
|--------|------|-------------|--------------|--------------|--------|
| 125 | Ship Gun Systems Equipment | $16,250 | $6,416 | $7,358 | 3 |
| 127 | Ship Missile Support Equipment | $283,972 | $376,830 | $455,822 | 3 |
| 128 | Tomahawk Support Equipment | $92,371 | $98,921 | $107,709 | 3 |
| 131 | SSN Combat Control Systems | $143,975 | $153,237 | $102,954 | 3 |
| 136 | Anti-Ship Missile Decoy System | $51,100 | $75,614 | $89,129 | 3 |
| | Total BA4 Ordnance support equipment | $1,262,194 | $1,351,254 | $1,644,572 | |

**Decision needed:** BA4 totals $1.6B but not all of it is ship-backfit on in-service vessels. The detail book must be checked to separate ship-installed ordnance support from munitions procurement, new-build equipment, and shore-based systems. The lines above are the most likely ship-relevant candidates.

### P-1 Exhibit: SCN (Shipbuilding and Conversion, Navy)

| Line # | Item | FY24 Actual | FY25 Enacted | FY26 Total | Bucket |
|--------|------|-------------|--------------|------------|--------|
| **10** | **CVN Refueling Overhauls** | — | **$6,271,049** (full program) | **$1,779,011** (subsequent full funding) | **4** |
| **47** | **LCAC SLEP** | **$15,286** (1 unit) | **$45,087** (2 units) | **$37,390** (1 unit) | **4** |
| | CVN RCOH (MEMO NON ADD) | | | ($483,100) | 4 (annualized reference) |

**Key insight:** CVN RCOH is the dominant Bucket 4 item. The $6.3B figure is the full program cost for one RCOH, not annual spend. The $1.78B FY26 figure is the incremental funding obligation. The detail book (SCN_Book.txt) has the cost breakdown (basic construction, electronics, HM&E, ordnance, outfitting). Most of the rest of SCN is new construction and should be excluded.

### P-1 Exhibit: OPN BA8 Spares

| Line # | Item | FY24 Actual | FY25 Enacted | FY26 Request | FY26 Total | Bucket |
|--------|------|-------------|--------------|--------------|------------|--------|
| 176 | Spares and Repair Parts | $736,770 | $705,144 | $585,865 | $883,630 | 5 |

Note: BA8 spares is a single line at the P-1 level. The detail book may break this down by ship class or system type.

---

## Phase 2: Extract Navy O&M Data (Buckets 1, 2, 5, 6)

### Step 2A: OMN_Book.txt — Decompose SAG 1B4B ($13.8B)

This is the highest-priority extraction. SAG 1B4B "Ship Depot Maintenance" is a $13.8B line that contains Buckets 1, 2, and parts of 6 blended together. The detail book must show sub-element breakdowns.

Search for these codes and keywords in order:
1. `1B4B` — find the SAG summary and all sub-element lines beneath it
2. `CMAV` — continuous maintenance availability dollars (→ Bucket 2)
3. `ERATA` — emergent repair dollars (→ Bucket 2)
4. `ORATA` — other repair/technical assistance dollars (→ Bucket 2)
5. `intermediate` or `non-depot` — intermediate-level maintenance (→ Bucket 2)
6. `availability` — count tables showing number of scheduled availabilities by type
7. `SRA`, `DSRA`, `DMP`, `PIA` — scheduled depot availability sub-elements (→ Bucket 1)
8. `berthing`, `messing`, `drydock services`, `shore power` — availability support (→ Bucket 6)

**Goal:** Separate 1B4B into:
- Bucket 1: Scheduled depot availabilities (the residual after subtracting Buckets 2 and 6)
- Bucket 2: CMAV + ERATA + ORATA + intermediate/non-depot maintenance
- Bucket 6: Availability support services (if separately identifiable)

### Step 2B: OMN_Book.txt — Extract SAG 1B5B ($2.76B)

Search for `1B5B` and its sub-elements. This maps cleanly to Bucket 5. Look for:
- Planning and technical support
- Lifecycle maintenance / class maintenance support
- Navy Modernization Process design services
- DMSMS / obsolescence management
- SUPSHIP oversight

### Step 2C: OMN_Vol2_Book.txt — Fine-grain detail

Use this immediately after OMN_Book for:
- Sub-element breakdowns under 1B4B and 1B5B that the main book may only show at summary level
- Availability-type-level spending if available
- Any reconciliation tables

---

## Phase 3: Extract Navy Procurement Data (Bucket 3, parts of 4 and 5)

### Step 3A: OPN_BA1_Book.txt — Decompose the big lines

**Priority 1 — Line 26: Ship Maintenance, Repair and Modernization ($2.4B)**
This is the single most important OPN line to decompose. Search for this line's detail section. Need to understand:
- What does this actually fund? Equipment? Installation? Both?
- How does it split between maintenance/repair vs. modernization?
- Is there a ship-class or program-level breakdown?

**Priority 2 — Named modernization programs:**
- Line 5: DDG Mod ($687M-$997M) — extract detail section
- Line 37: LCS In-Service Modernization ($203M-$238M) — extract detail section
- Line 8: LHA/LHD Midlife ($87M-$123M) — extract detail section
- Line 9: LCC 19/20 ESLP ($19M) — extract detail section (→ Bucket 4)

**Priority 3 — Class support equipment lines:**
- Lines 2, 4, 11, 12, 13, 15, 16, 17 — these may be equipment procurement for in-service vessels, or they may include new-build support. The detail book will clarify.

**Priority 4 — Mission modules:**
- Lines 33, 34, 36 (LCS mission modules) — are these for in-service vessels or new-build? Detail book needed.

### Step 3B: OPN_BA2_Book.txt — Ship-installed electronics

For each of the ship-relevant BA2 lines identified above, open the detail section and verify:
- Is this equipment installed on in-service vessels (backfit/retrofit)?
- Or is it for new construction integration?
- Or both?

Only include the in-service portion in Bucket 3. If the detail book doesn't split new-build vs. in-service, note as a medium-confidence estimate.

### Step 3C: OPN_BA4_Book.txt — Ship weapon systems (selective)

Same filter as BA2: only include items that are backfit onto in-service vessels. The five ship-relevant BA4 lines total ~$763M in FY26 but the actual in-service portion may be smaller.

### Step 3D: OPN_BA5-8_Book.txt — BA8 Spares ($586M-$884M)

Go directly to the BA8 section. Extract:
- Total BA8
- Any ship-specific vs. non-ship breakdown
- Map to Bucket 5

Skip BA5-7 entirely unless a gap surfaces.

### Step 3E: OPN_BA3_Book.txt — Low priority

Only check if carrier aviation support systems (AAG, EMALS) installed on in-service carriers are deemed in scope. Otherwise skip.

---

## Phase 4: Extract Major Life-Cycle Events (Bucket 4)

### Step 4A: SCN_Book.txt — RCOH detail

- Search for `RCOH`, `Refueling Overhaul`, `CVN 73`, `CVN 74`, `CVN 75` (whichever hull is in RCOH)
- Extract the cost breakdown: basic construction, electronics, HM&E, ordnance, outfitting
- Record both the full program cost and the FY26 incremental funding ($1.78B)
- Note: for annual TAM purposes, use the incremental annual funding, not the full program cost

### Step 4B: SCN_Book.txt — LCAC SLEP

- Search for `LCAC SLEP`
- FY26: $37.4M for 1 unit
- Small relative to RCOH but a clean Bucket 4 item

### Step 4C: OPN_BA1_Book.txt — Other life-cycle events

- LCC 19/20 ESLP ($19M) — already identified
- LHA/LHD Midlife ($87-123M) — could be Bucket 3 or 4; detail book will clarify whether this is a "major life-cycle event" scale program or routine modernization
- LSD Midlife & Modernization ($4M) — small, probably Bucket 3

### Step 4D: Cross-reference with USCG (Phase 5)

Coast Guard SLEP and MMA are the CG Bucket 4 items — extracted in Phase 5.

---

## Phase 5: Extract Coast Guard Data (All Buckets)

### Step 5A: USCG_Justification.txt

The Coast Guard justification book covers all CG buckets in one document. The Supp Book does NOT contain CG detail — only a "Coast Guard Support" line ($22M) within Navy O&M, and a "Coast Guard Weapons" line ($55M) and "Coast Guard Equipment" line ($62M) in OPN.

The CG's own justification book is the primary source. Search for:

**Bucket 1 & 2:** "dry-dock", "dockside", "cutter maintenance", "depot-level", "vessel repair", "corrective maintenance", "preventive maintenance"

**Bucket 3:** "alterative maintenance", "capability upgrade", "mission system", "modernization"

**Bucket 4:** "SLEP", "MMA", "Major Maintenance Availability", "Service Life Extension", "In-Service Vessel Sustainment", "ISVS"

**Bucket 5:** "survey and design", "lifecycle support", "planning", "engineering support"

**Bucket 6:** "service actions", "port services", "husbanding", "docking/undocking"

**Key CG funding lines to find:**
- PC&I (Procurement, Construction & Improvements) — Buckets 3, 4
- O&S (Operating & Support) — Buckets 1, 2, 5, 6
- AC&I (Acquisition, Construction & Improvements) — may appear as alternate name for PC&I

---

## Phase 6: Public-Yard Decomposition and Context

### Step 6A: NWCF_Book.txt — Public-yard share of depot maintenance

**This is NOT additive to OMN.** OMN 1B4B funds depot maintenance; some of that money flows to private yards via contracts (visible in FPDS) and some flows to public naval shipyards via NWCF working capital fund transfers. The NWCF book shows the public-yard execution side of the same dollars.

**Goal:** For every OMN-funded line item already extracted in Phase 2 (especially Bucket 1 and Bucket 4), determine what share is executed by public yards vs. private industry.

Search for:
- Public shipyard workload data (Norfolk Naval Shipyard, Puget Sound Naval Shipyard, Pearl Harbor Naval Shipyard, Portsmouth Naval Shipyard)
- Depot maintenance execution tables showing public vs. private split
- Submarine depot maintenance (almost entirely public yard)
- Carrier depot maintenance (split between public and private)
- Surface combatant depot maintenance (mostly private yard)
- CG yard (Coast Guard Yard, Curtis Bay) if present

**What to extract:**
- Total public-yard depot maintenance workload in dollars and/or direct labor hours
- Any breakdown by ship class or availability type showing public vs. private performer
- Any explicit statements about what percentage of depot maintenance is performed organically vs. contracted

**How this flows through the medallion layers:**
- **Bronze:** Extract the NWCF figures as their own line items, clearly tagged as `Source: NWCF`
- **Silver:** These lines get disposition `PERFORMER_TAG` — they are not new TAM dollars, they are used to populate the Performer column on existing OMN-sourced line items. Document the mapping (e.g., "NWCF shows $X in submarine depot maintenance → this tags the OMN 1B4B submarine depot sub-element as Performer: Public Yard")
- **Gold:** Every line item in the TAM table carries a Performer column. The TAM total is unchanged — the Performer column just tells you who does the work.

### ~~Step 6B: president_budget_fy2027.txt~~ — REMOVED
> Removed from plan. This is an FY27 document but the FY27 budget justification books have not been released yet. All analysis uses FY26 justification books only.

### Step 6B: WPN_Book.txt (if needed)
- Only consult if weapon-system sustainment on ships surfaces as a gap.

---

## Medallion Architecture: How It Maps to This Plan

This plan follows the Bronze / Silver / Gold medallion method described in `medallion-architecture-generalized.md.pdf`. Each layer produces a concrete output file.

### Bronze (Raw Ingestion) — Phases 0–5

**What happens:** Extract every potentially relevant figure from each budget book exactly as it appears — no filtering, no judgment about which bucket it belongs to. Record the raw dollar values, line item names, SAG/BLI codes, page references, and source file.

**Output file:** `topdown/bronze_extractions.md`

Structure per book:
```
## Source: OMN_Book.txt
### SAG 1B4B — Ship Depot Maintenance
- [line XXX] Sub-element: [name] | FY24: $X | FY25: $X | FY26: $X
- [line XXX] Sub-element: [name] | FY24: $X | FY25: $X | FY26: $X
...
### SAG 1B5B — Ship Depot Operations Support
...

## Source: OPN_BA1_Book.txt
### Line 5: DDG Mod
- [line XXX] FY24: $641,676 | FY25: $861,066 | FY26: $997,485
- Detail: [raw description excerpt]
...
```

**Rules:**
- Pull broadly — if a line item might be relevant, extract it. Filtering comes in Silver.
- One source is the system of record per fact type: OMN owns O&M dollars, OPN owns procurement dollars, SCN owns shipbuilding dollars. Do not mix.
- NWCF figures are extracted separately and tagged as `Source: NWCF`. They represent the public-yard execution share of OMN-funded work — they are **not additive** to OMN dollars. Their role is to inform the Performer column in Silver/Gold.
- Do not interpret, classify, or exclude anything at this stage.

### Silver (Canonicalization & Enrichment) — Phase 6 + new Silver step

**What happens:** Take the bronze extractions and apply filtering, normalization, and bucket assignment — while preserving every individual line item. The Silver output is the same list of line items as Bronze, but each one now has a disposition, a bucket assignment, and adjusted dollar values where needed.

Steps:
1. **Resolve overlaps** — verify no line item is counted in two places (e.g., does Line 26 "Ship Maintenance, Repair and Modernization" overlap with OMN depot maintenance? It shouldn't — different appropriations — but verify and document).
2. **Apply include/exclude rules** — for each extracted line, determine: is this in-service vessel work? Mark each line as INCLUDE, EXCLUDE, or PARTIAL with rationale.
3. **Split blended lines** — where a line item spans multiple buckets (e.g., 1B4B contains depot, continuous, and support spend), break it into sub-lines with the split logic documented. The sub-lines each get their own row.
4. **Normalize units** — all figures in thousands, all fiscal years aligned.
5. **Flag new-build vs. in-service ambiguity** — for OPN lines where the detail book doesn't cleanly separate new-build from in-service, tag as PARTIAL and note the assumed in-service share.
6. **Assign bucket** — every INCLUDE and PARTIAL line gets a bucket number. This is the bucket assignment that Gold will use directly.

**Output file:** `topdown/silver_canonical.md`

**Key rule: every line item from Bronze appears in Silver.** Nothing is silently dropped. EXCLUDE items stay in the table with their disposition and rationale — they are just not counted in totals. This preserves full continuity from Bronze → Silver → Gold.

Structure:
```
## Line-by-Line Disposition

| Source | Line Item | Bronze FY26 ($K) | Disposition | Bucket | Performer | Adjusted FY24 ($K) | Adjusted FY25 ($K) | Adjusted FY26 ($K) | In-Service Share | Rationale |
|--------|-----------|-------------------|-------------|--------|-----------|---------------------|---------------------|---------------------|------------------|-----------|
| OMN 1B4B | Ship Depot Maintenance (total) | 13,803,188 | SPLIT | — | — | — | — | — | 100% | Parent line; see sub-elements below |
| OMN 1B4B | → Scheduled depot avails (surface) | XXX | INCLUDE | 1 | Private Industry | $X | $X | $X | 100% | Mostly private yards per NWCF |
| OMN 1B4B | → Scheduled depot avails (submarine) | XXX | INCLUDE | 1 | Public Yard | $X | $X | $X | 100% | Public naval shipyards per NWCF |
| OMN 1B4B | → CMAV | XXX | INCLUDE | 2 | Mixed | $X | $X | $X | 100% | Continuous maintenance |
| OMN 1B4B | → ERATA | XXX | INCLUDE | 2 | Mixed | $X | $X | $X | 100% | Emergent repair |
| OMN 1B4B | → ORATA | XXX | INCLUDE | 2 | Mixed | $X | $X | $X | 100% | Other repair |
| OMN 1B5B | Ship Depot Ops Support | 2,760,878 | INCLUDE | 5 | Mixed | $2,714,238 | $2,671,812 | $2,760,878 | 100% | Direct budget line |
| OPN BA1 L5 | DDG Mod | 997,485 | INCLUDE | 3 | Private Industry | $641,676 | $861,066 | $997,485 | 100% | In-service modernization |
| OPN BA2 L48 | Fixed Surveillance System | 363,312 | EXCLUDE | — | — | — | — | — | 0% | Shore-based, not ship-installed |
| OPN BA2 L44 | SSN Acoustic Equipment | 498,597 | PARTIAL | 3 | Mixed | $X | $X | $X | ~50%? | Includes new-build and in-service |
| NWCF | Public yard depot workload | X | PERFORMER_TAG | — | — | — | — | — | — | Not TAM dollars; used to tag OMN lines above |
...
```

**Performer column values:**
- **Public Yard** — work performed by federal civilian employees at government-owned naval shipyards (Norfolk, Puget Sound, Pearl Harbor, Portsmouth) or CG Yard (Curtis Bay)
- **Private Industry** — work contracted to private shipyards and companies
- **Mixed** — line item contains both public and private execution, or the split is not determinable from budget books alone
- **Unknown** — insufficient data to determine performer

**Reconciliation artifact** (required by medallion method):
```
## Silver Reconciliation Summary

| Stage | Line Item Count | Total FY26 ($K) |
|-------|-----------------|-----------------|
| Bronze (all extracted lines) | XX | $XX,XXX,XXX |
| After EXCLUDE filter | XX | $XX,XXX,XXX |
| After PARTIAL adjustment | XX | $XX,XXX,XXX |
| After SPLIT decomposition | XX | $XX,XXX,XXX |
| Final Silver (INCLUDE + adjusted PARTIAL) | XX | $XX,XXX,XXX |
```

### Gold (Classification & Analysis-Ready Output) — Phase 7

**What happens:** Apply the six-bucket taxonomy to the Silver-canonical data to produce the final TAM table. Classification uses the pre-defined bucket definitions — not invented during this step. The Gold layer preserves individual line items within each bucket — it does not collapse them into opaque totals.

**Output files:**

**1. `topdown/gold_tam_table.md` — The primary deliverable**

The bucket-by-bucket TAM table with every contributing line item visible. Structure per bucket (all $ in thousands):

```
## Bucket 1: Scheduled Depot Maintenance & Repair

| Source | Line Item | Performer | FY24 Actual | FY25 Enacted | FY26 Request | Confidence | Notes |
|--------|-----------|-----------|-------------|--------------|--------------|------------|-------|
| OMN 1B4B | Scheduled depot avails (surface) | Private Industry | $X | $X | $X | High | Direct budget line |
| OMN 1B4B | Scheduled depot avails (submarine) | Public Yard | $X | $X | $X | High | Naval shipyards per NWCF |
| OMN 1B4B | Scheduled depot avails (carrier) | Mixed | $X | $X | $X | High | Split public/private |
| USCG O&S | Dry-dock availabilities | Private Industry | $X | $X | $X | Medium | CG contracts to private yards |
| **Bucket 1 Total** | | | **$X** | **$X** | **$X** | | |
| → of which Public Yard | | Public Yard | $X | $X | $X | | |
| → of which Private Industry | | Private Industry | $X | $X | $X | | |

## Bucket 3: Modernization & Alteration Installation

| Source | Line Item | Performer | FY24 Actual | FY25 Enacted | FY26 Request | Confidence | Notes |
|--------|-----------|-----------|-------------|--------------|--------------|------------|-------|
| OPN BA1 L5 | DDG Mod | Private Industry | $641,676 | $861,066 | $997,485 | High | Named program |
| OPN BA1 L37 | LCS In-Service Modernization | Private Industry | $154,561 | $188,254 | $237,728 | High | Named program |
| OPN BA1 L26 | Ship Maint, Repair & Mod (in-service share) | Mixed | $X | $X | $X | Medium | Apportioned from $2.4B total |
| OPN BA2 L43 | AN/SQQ-89 Surf ASW Combat System | Private Industry | $133,803 | $134,637 | $144,425 | Medium | Assumed 100% in-service backfit |
| OPN BA2 L78 | In-Service Radars and Sensors | Private Industry | $279,545 | $222,607 | $249,656 | High | Name confirms in-service |
| OPN BA4 L127 | Ship Missile Support Equipment | Mixed | $283,972 | $376,830 | $455,822 | Medium | In-service share TBD |
| ...
| **Bucket 3 Total** | | | **$X** | **$X** | **$X** | | |
```

Then a **roll-up summary table** at the end:

| Bucket | FY24 Actual | FY25 Enacted | FY26 Request | Public Yard | Private Industry | Mixed/Unknown | Confidence |
|--------|-------------|--------------|--------------|-------------|------------------|---------------|------------|
| 1. Scheduled depot maintenance & repair | | | | | | | |
| 2. Continuous / intermediate / emergent | | | | | | | |
| 3. Modernization & alteration installation | | | | | | | |
| 4. Major life-cycle events / SLEP | | | | | | | |
| 5. Sustainment engineering / planning | | | | | | | |
| 6. Availability support / port services | | | | | | | |
| **Total TAM** | | | | | | | |

The Public Yard / Private Industry / Mixed columns show the FY26 split by performer. This allows reading the table two ways: total market (FY26 Request) and addressable market for a private shipbuilder (Private Industry + share of Mixed).

**2. `topdown/gold_confidence_and_gaps.md` — Confidence tiers and known gaps**

For each bucket:
- **High confidence** — dollar figure comes directly from a named budget line with a clear boundary.
- **Medium confidence** — figure is derived by subtracting known sub-elements, apportioning a broader line, or filtering new-build from in-service within a BLI.
- **Low confidence / gap** — line item is not separately broken out; estimate is inferred or the detail book didn't provide the needed split.

Known exclusions:
- Classified programs (not in public budget books)
- MSC vessel work (may be in different appropriations — check if OMN or SCN has MSC-specific lines)
- Army watercraft (separate service budget, not in Navy books)

**3. `topdown/gold_reconciliation.md` — Cross-checks**

1. **OMN internal check:** Sum of Bucket 1 + 2 + (OMN portion of 6) should ≈ SAG 1B4B ($13.8B). Bucket 5 should ≈ SAG 1B5B ($2.76B).
2. **Cross-source check:** Sum of all buckets should be in the neighborhood of the $16.2B ship maintenance figure (acknowledging that figure may use a different boundary and likely excludes OPN modernization).
3. **Reasonableness:** Bucket 1 (depot) should be the largest single bucket. RCOH should dominate Bucket 4. BA8 spares should be smaller than Bucket 1.
4. **No double-counting:** OPN modernization lines should not overlap with OMN depot maintenance lines (budget books split these cleanly by appropriation, so this should hold).

**4. `topdown/tam_topdown_summary.md` — Executive summary**

A concise, presentation-ready document that synthesizes the entire top-down analysis. Structure:

```
# In-Service Vessel Work — Top-Down TAM Summary

## Total Market Size
- FY24 Actual: $X.XB
- FY25 Enacted: $X.XB
- FY26 Request: $X.XB
- FY trend: [growing / flat / declining] at ~X% CAGR

## By Bucket
[The roll-up table from gold_tam_table.md]

## By Funding Source
| Funding Source | FY26 ($B) | % of Total | Buckets Served |
|...

## By Performer (Public vs. Private)
| Performer | FY26 ($B) | % of Total | Notes |
|-----------|-----------|------------|-------|
| Public Yard | $X.XB | X% | Naval shipyards (Norfolk, Puget Sound, Pearl Harbor, Portsmouth) + CG Yard |
| Private Industry | $X.XB | X% | Addressable market for private shipbuilders |
| Mixed / Unknown | $X.XB | X% | Blended lines; actual split TBD from contract data |

## Key Findings
- [Top 3-5 takeaways, e.g., "Depot maintenance (Bucket 1) is Xx% of the total market at $X.XB"]
- [Fastest-growing bucket]
- [Largest single line item]
- [CG vs. Navy split]
- [Public vs. private yard split — what % of the TAM is addressable by private industry]

## Confidence Assessment
- High-confidence portion: $X.XB (X% of total)
- Medium-confidence portion: $X.XB (X%)
- Low-confidence / gap: $X.XB (X%)

## Known Exclusions
- [Classified, MSC, Army watercraft — brief summary with estimated impact if possible]

## Methodology
- Source: FY2026 President's Budget justification books (Navy + Coast Guard)
- Taxonomy: Six work-type buckets derived from official Navy/CG definitions, budget structure, and contract language
- Approach: Medallion architecture (Bronze raw extraction → Silver canonicalization → Gold classification)
- All figures in then-year dollars as presented in budget books
```

This is the document you'd hand to someone who wants the answer without the working.

---

## Precautions for AI Agent Execution

These books are large (OMN_Book.txt is 3MB, OPN books are 1-4MB each). The following rules apply:

1. **Never read an entire book into context.** Always use targeted searches (grep/search for SAG codes, BLI codes, keywords) to find the relevant sections, then read only those sections.
2. **Use the Supp Book extraction tables above as the map.** Do not open detail books without first knowing which SAG/BLI codes and line numbers to look for.
3. **Search by code first, keywords second.** SAG "1B4B" is more precise than "ship maintenance" which will match hundreds of lines.
4. **When a search returns too many results, narrow with additional terms** (ship class, fiscal year, availability type).
5. **Record page references / line numbers** for every extracted figure so the work is auditable.
6. **Write intermediate results to disk after each phase.** Do not accumulate everything in memory.
7. **The Supp_Book.pdf must be converted to text before any other work begins.** Run: `pdftotext -layout topdown/sources/Supp_Book.pdf topdown/sources/Supp_Book.txt`
8. **Write Bronze output after each book is processed** — do not wait until all books are done. Append to `topdown/bronze_extractions.md` incrementally.
9. **Write Silver output only after all Bronze extraction is complete** — Silver needs the full picture to resolve overlaps and apply include/exclude rules.
10. **Write Gold output only after Silver is complete** — Gold is mechanical application of the bucket taxonomy to Silver-canonical data.

---

## Output Files Summary

| File | Layer | What It Contains | When Written |
|------|-------|------------------|--------------|
| `topdown/bronze_extractions.md` | Bronze | Every extracted line item from every book, raw, with source/line references | Incrementally during Phases 1–5 |
| `topdown/silver_canonical.md` | Silver | Line-by-line disposition (INCLUDE/EXCLUDE/PARTIAL), overlap resolution, split logic, reconciliation summary | After all Bronze extraction is complete |
| `topdown/gold_tam_table.md` | Gold | The 6-bucket TAM table with every contributing line item visible, plus roll-up summary | After Silver is complete |
| `topdown/gold_confidence_and_gaps.md` | Gold | Confidence tiers per bucket, known exclusions, data gaps | After Silver is complete |
| `topdown/gold_reconciliation.md` | Gold | Cross-checks against known benchmarks and internal consistency tests | After Gold table is assembled |
| `topdown/tam_topdown_summary.md` | Final | Executive summary — total market size, by-bucket and by-source breakdowns, key findings, methodology | After all Gold files are complete |

---

## Reading Order Summary

| Order | Book | What to Extract | Est. Effort |
|-------|------|-----------------|-------------|
| 1 | Supp_Book (O-1 + P-1) | ✅ Done — see tables above | Complete |
| 2 | OMN_Book | Decompose 1B4B into Buckets 1/2/6; extract 1B5B for Bucket 5 | Heavy — largest extraction |
| 3 | OMN_Vol2_Book | Fine-grain sub-elements under 1B4B and 1B5B | Medium |
| 4 | OPN_BA1_Book | Decompose Line 26 ($2.4B); detail on DDG Mod, LCS Mod, LHA/LHD Midlife, LCC ESLP | Heavy |
| 5 | OPN_BA2_Book | Filter ship-installed electronics for Bucket 3 | Medium — selective |
| 6 | OPN_BA5-8_Book | BA8 spares for Bucket 5 | Light — one section |
| 7 | OPN_BA4_Book | Ship weapon system backfit for Bucket 3 (if in scope) | Light — selective |
| 8 | SCN_Book | RCOH detail and LCAC SLEP for Bucket 4 | Light — targeted |
| 9 | USCG_Justification | All CG buckets | Medium |
| 10 | NWCF_Book | Public-yard workload — used to tag Performer column on OMN lines (not additive) | Medium |
| ~~11~~ | ~~president_budget_fy2027~~ | ~~Removed — FY27; not applicable~~ | ~~N/A~~ |
