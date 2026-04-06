# U.S. Naval Vessel TAM Crosswalk — Seven Buckets

**Scope:** All U.S. Navy, Coast Guard, MSC, and Army watercraft work — from new construction through in-service sustainment.

**Recommended use:** Top-level bucket from official funding/program logic; second-level tags from availability type, customer, PSC, and nuclear/non-nuclear status. Practical rule: if the work **builds a new vessel**, it is Bucket 1; if it **restores existing condition**, it is maintenance (Buckets 2–3); if it **adds capability or changes configuration**, it is modernization (Bucket 4); if it **extends platform life at class scale**, it is a major life-cycle event (Bucket 5); if it is **planning/engineering support**, it is Bucket 6; if it **enables the availability but is not wrench-turning**, it is Bucket 7.

**Mixed-contract rule:** DMP/DSRA and other availabilities often bundle maintenance, repair, and modernization in one award. Keep top-down budgets split by appropriation (OMN vs OPN vs SCN); bottom-up, tag the contract by its predominant PSC code and flag the overlap.

---

## Bucket 1. New Construction

| Field | Detail |
|-------|--------|
| **Market segment** | Newbuild |
| **Definition / logic** | Design, construction, and delivery of new vessels — from detail design through sea trials and delivery. Includes long-lead material procurement and advance procurement that funds construction before the main DD&C contract. This is the shipbuilding market proper. |
| **Primary budget anchors** | Navy: SCN (Shipbuilding & Conversion, Navy) — e.g., DDG-51 construction, Virginia/Columbia-class subs, CVN-78 class carriers, FFG-62, LPD Flight II, T-AO, LHA, LCS, SSC. USCG: PC&I (Procurement, Construction & Improvements) — OPC, FRC, PSC (icebreaker), NSC. |
| **Primary PSCs** | Product codes 1905 (combat ships), 1910 (transport), 1915 (patrol craft), 1920 (service craft), 1925 (special purpose), 1940 (small craft). Note: PSC codes often come back NULL on the largest construction IDVs in USAspending — keyword/program matching is more reliable than PSC for newbuild. |
| **Award language / keyword tags** | "Detail design and construction" (DD&C), "[class] ship construction", "long lead time material" (LLTM), "advance procurement", "detailed design and production" (DD&P — CG variant), "construction of [hull designation]", "lead yard support/services", "planning yard" |
| **Include** | Full ship DD&C contracts, multi-ship block buys, advance procurement / LLTM, construction engineering and planning yard services, post-delivery trials, shipbuilder's guarantee work, foreign military sales construction (e.g., MMSC, Egyptian FMC). |
| **Exclude / boundary** | Post-Shakedown Availability (PSA) is the boundary — PSA and everything after is in-service (Buckets 2–7). RCOH/EOH are life-cycle events (Bucket 5), not newbuild. Shipyard infrastructure CAPEX (drydock construction, SIOP) is not vessel work. RDT&E test articles and prototypes are typically excluded unless they result in delivered hulls. |
| **Bottom-up retrieval rule** | Keyword-first approach: search for hull designations + "construction", "DD&C", "LLTM", "advance procurement." PSC 19xx codes catch some delivery orders but miss the large prime contracts (which often lack PSC in USAspending). Cross-reference against SCN P-1 budget exhibit program names. Filter out RCOH/EOH/SLEP and in-service repair keywords. |
| **Key vendors** | GD Electric Boat (subs), HII Newport News (carriers, subs, amphibs), HII Ingalls (DDG, LPD, LHA), GD Bath Iron Works (DDG), GD NASSCO (T-AO, ESB), Marinette Marine/Fincantieri (FFG-62), Austal USA (LCS, OPC), Bollinger (FRC, PSC), Eastern Shipbuilding (OPC), Textron (SSC/LCAC) |
| **Source IDs** | SCN P-1 exhibits, USCG PC&I Congressional Justification |

### Sub-categories within Bucket 1

| Sub-category | Award language pattern | Examples |
|---|---|---|
| Full ship DD&C | "detail design and construction", "[class] ship construction" | DDG-51, FFG(X), CVN-79, LPD, LHA, T-AO, OPC, FRC, PSC |
| Advance procurement / LLTM | "long lead time material", "advance procurement", "LLTM" | Pre-construction material buys, funded 1–2 years ahead of DD&C |
| Construction engineering / planning yard | "lead yard support", "planning yard", "design completion" | EB submarine planning yard, Columbia design completion |
| GFE / combat systems for newbuild | Separate from hull construction — funded through OPN or RDT&E | Combat systems procured by government, furnished to shipbuilder |

---

## Bucket 2. Scheduled Depot Maintenance & Repair

| Field | Detail |
|-------|--------|
| **Market segment** | Core MRO |
| **Definition / logic** | Planned depot-level work to restore or sustain existing ship material condition during CNO-scheduled availabilities (Navy) and scheduled drydock/dockside availabilities (CG). This is the core of what people call "MRO" — the largest recurring in-service vessel work market. |
| **Primary budget anchors** | Navy: O&M,N SAG 1B4B Ship Depot Maintenance (~$13.8B FY26). NWCF depot maintenance reimbursements for public-yard work. USCG: O&S (operating & support) maintenance funding for cutter availabilities. |
| **Primary PSCs** | J998, J999; sometimes J019 / J020 for equipment-level marine repair inside a larger availability. |
| **Availability / keyword tags** | DSRA, SRA, DPMA, PMA, PIA, DPIA, ROH, overhaul, drydock |
| **Include** | Hull/HM&E repair, inspections, drydocking, overhauls, corrosion control, renewal work, tank/void preservation, propulsion system repair, electrical plant repair, Class A–D overhaul work, MSC Mid-Term Availabilities and ROHs. |
| **Exclude / boundary** | Capability-adding mods (Bucket 4), class-scale SLEP/MMA (Bucket 5), engineering-only support (Bucket 6), husbanding / port services (Bucket 7). |
| **Bottom-up retrieval rule** | Filter PSC first (J998/J999); then agency, hull designation, and availability acronym. Treat DMP / MODPRD as mixed (split between Bucket 2 and Bucket 4 at the CLIN level or tag as blended). |
| **Source IDs** | S1, S4, S6, S11 |

---

## Bucket 3. Continuous / Intermediate / Emergent Maintenance

| Field | Detail |
|-------|--------|
| **Market segment** | Core MRO |
| **Definition / logic** | Repair outside the big depot event: shorter-duration, intermediate-level, continuous, and emergent/casualty work performed by RMCs, IMAs, tenders, MATs, ASSIST teams, or cutter crews with contractor augmentation. Same sustainment mission as Bucket 2 but different rhythm and urgency. |
| **Primary budget anchors** | Navy: non-depot / intermediate maintenance and CMAV / ERATA-type work within ship maintenance budgets. CMAV (~$651M), ERATA (~$139M), ORATA (~$1.07B), Non-depot/IL (~$1.53B). USCG: O&S intermediate maintenance and emergent repair. |
| **Primary PSCs** | J998, J999; selected J-codes for equipment repair. Contracting office filters are often more useful than PSC for separating this from Bucket 2. |
| **Availability / keyword tags** | CMAV, WOO, EM, emergent, casualty repair, voyage repair, dockside |
| **Include** | Continuous maintenance, voyage repairs, repair augmentation, short dockside work, CASREP-driven emergency repair, IMA/RMC-executed work, contractor maintenance augmentation. |
| **Exclude / boundary** | Named class-scale life-extension events (Bucket 5) and pure modernization procure/install efforts (Bucket 4). |
| **Bottom-up retrieval rule** | Use keywords + RMC / FDRMC / SRF contracting offices; PSC alone may under-separate this bucket from Bucket 2. |
| **Source IDs** | S4, S6, S11, S13 |

---

## Bucket 4. Modernization & Alteration Installation

| Field | Detail |
|-------|--------|
| **Market segment** | MRO-adjacent |
| **Definition / logic** | Work that changes configuration or adds capability/reliability beyond restore-only repair. Funded primarily through procurement, not O&M. DoD FMR explicitly separates major performance-improving modifications from depot maintenance/repair. |
| **Primary budget anchors** | Navy: procurement mods in P-1 / P-3a / P-40 — DDG Mod (~$687M–$997M/yr), CG Mod, LCS In-Service Mod, LHA/LHD Midlife. USCG: PC&I and ISVS mission-effectiveness upgrades. |
| **Primary PSCs** | K019, K020; N019, N020; sometimes J998 / J999 when embedded inside a ship availability that blends repair + modernization. |
| **Availability / keyword tags** | DMP, MODPRD, SHIPALT, ORDALT, MACHALT, tech refresh, capability insertion, AIT, backfit, retrofit, A-kit/B-kit |
| **Include** | Retrofits, A/B kits, new module installs, combat-system / mission-system upgrades, cybersecurity upgrades (TFCA), tech insertion kits, Advanced Capability Build, alteration installation team work. |
| **Exclude / boundary** | Restore-only repair (Buckets 2–3), RDT&E test installations, planning-only engineering (Bucket 6). |
| **Bottom-up retrieval rule** | Start with K / N PSCs. For J998 / J999 awards, require modernization keywords or DMP/MODPRD availability type to flag overlap with Bucket 2. OPN funding line is the cleanest top-down discriminator. |
| **Source IDs** | S2, S3, S5, S7, S11 |

---

## Bucket 5. Major Life-Cycle Events / Service-Life Extension

| Field | Detail |
|-------|--------|
| **Market segment** | MRO-adjacent |
| **Definition / logic** | Multi-year, platform- or class-scale recapitalization / service-life-extension work that is too large and special to treat as routine repair. Gets its own budget line items, own program offices, and own contracting vehicles. |
| **Primary budget anchors** | Navy: named overhaul/refueling or shipbuilding lines — CVN RCOH funded under SCN ($2–3B per ship). Sub EOH in public shipyard workload. USCG: PC&I In-Service Vessel Sustainment — SLEP and MMA as named sub-investments. |
| **Primary PSCs** | Often still J998 / J999 at execution level; use named program + funding line more than PSC for classification. |
| **Availability / keyword tags** | RCOH, EOH, ERO, SLEP, MMA, midlife, FRAM, major renovation |
| **Include** | Nuclear refueling overhauls (RCOH), engineered overhauls (EOH), Polar Star / WMEC / MLB SLEP, buoy-tender MMA, major midlife renovations, D5 life extension, SSBN weapon system life extension. |
| **Exclude / boundary** | Ordinary SRA / DSRA / CMAV work unless it is clearly part of a named life-extension program. Regular depot maintenance is Bucket 2. |
| **Bottom-up retrieval rule** | Retrieve by named program keywords (RCOH, EOH, SLEP, MMA) and appropriation first; do not rely on PSC alone. |
| **Source IDs** | S5, S8, S9, S10 |

---

## Bucket 6. Sustainment Engineering / Planning / Obsolescence Support

| Field | Detail |
|-------|--------|
| **Market segment** | MRO-adjacent |
| **Definition / logic** | Engineering, planning, lifecycle, DMSMS/obsolescence, and program-support work for in-service vessels. The "brains behind the wrench-turning" — the customer pays separately for this technical work that keeps ships supportable. |
| **Primary budget anchors** | Navy: O&M,N SAG 1B5B Ship Depot Operations Support (~$2.76B FY26). OPN spares & repair parts (BA08, ~$586M–$884M/yr). USCG: Survey & Design for future availabilities. |
| **Primary PSCs** | R425 (Engineering/Technical), R408 (Program Management/Support); selected supply/spares codes only if you intentionally include material procurement in the TAM. |
| **Availability / keyword tags** | SETA, lifecycle support, DMSMS, obsolescence, class maintenance plan, survey & design, technical authority, configuration management |
| **Include** | Availability planning, technical authority support, class support, configuration management, obsolescence/DMSMS management, life-of-type buys, SUPSHIP oversight, technical manual maintenance, spares procurement (if included in TAM scope). |
| **Exclude / boundary** | Physical repair labor (Buckets 2–3), install labor (Bucket 4), husbanding / port services (Bucket 7). |
| **Bottom-up retrieval rule** | Use R425 / R408 first; decide separately whether spares/material procurement belongs in this bucket or as a tagged overlay. Engineering services firms (CACI, Noblis, Antech, ORBIS SIBRO) are distinct from shipyards. |
| **Source IDs** | S4, S10, S11 |

---

## Bucket 7. Availability Support / Husbanding / Port Services

| Field | Detail |
|-------|--------|
| **Market segment** | Adjacent only |
| **Definition / logic** | Services that enable repair/modernization but are not themselves repair or upgrade work. These are the overhead and infrastructure services that make availabilities possible. |
| **Primary budget anchors** | Budgeted inside broader O&M support structures rather than as ship repair itself. Drydock infrastructure is a separate major capital category (SIOP). |
| **Primary PSCs** | M2AA–M2BZ, M2CA; selected facilities/support codes only if your TAM includes yard infrastructure. |
| **Availability / keyword tags** | Husbanding, pilot, tug, berthing, crane, forklift, shore power, scaffolding, force protection, waste removal, environmental |
| **Include** | Integrated port services, force protection, berthing/messing, cranes/rigging, shore power, scaffolding, environmental remediation, drydock services, test/trials support. |
| **Exclude / boundary** | Actual ship repair/install work (Buckets 2–4); shipyard infrastructure CAPEX unless you intentionally include it. |
| **Bottom-up retrieval rule** | Keep separate from core MRO unless your yard directly competes in these services. M2 PSC codes activated in 2020 are the cleanest filter. |
| **Source IDs** | S4, S8, S11 |

---

## Decision Tree for Classifying a Work Item

| Question | If yes → Bucket | Typical signals | Core MRO? |
|----------|----------------|-----------------|-----------|
| Is it construction of a new vessel? | 1. New Construction | DD&C, LLTM, advance procurement, SCN/PC&I funding | No (separate) |
| Does it restore existing condition during a planned major availability? | 2. Scheduled Depot Maintenance & Repair | DSRA / SRA / DPMA / PMA / PIA; repair, overhaul, drydock | Yes |
| Is it shorter-duration, emergent, or intermediate work outside the big depot event? | 3. Continuous / Intermediate / Emergent Maintenance | CMAV, WOO, EM, casualty, voyage repair, dockside | Yes |
| Does it add capability, improve reliability via retrofit, or change configuration? | 4. Modernization & Alteration Installation | SHIPALT, ORDALT, K/N PSCs, DMP, combat systems integration | No (adjacent) |
| Is it a named service-life-extension or recapitalization event? | 5. Major Life-Cycle Event / SLEP / MMA / RCOH | SLEP, MMA, RCOH, EOH, midlife, named class program | No (adjacent) |
| Is it planning, engineering, obsolescence, or program support? | 6. Sustainment Engineering / Planning / Obsolescence Support | R425, R408, SETA, DMSMS, survey & design, lifecycle | No (adjacent) |
| Is it port/husbanding/enabling support? | 7. Availability Support / Husbanding / Port Services | M2 codes, pilot, tug, berthing, crane, shore power | No (adjacent) |

---

## CLS (Contractor Logistics Support) Rule

CLS is a **delivery construct**, not a seventh (now eighth) bucket. Classify CLS by the underlying work type:

- **Default: Bucket 6** when scope is mostly lifecycle support, planning, technical support, materiel management.
- **Bucket 2** when CLS is predominantly contractor-performed depot work during a scheduled availability.
- **Bucket 3** when it is predominantly recurring / intermediate / emergent hands-on maintenance.
- **Bucket 4** when it is mainly tied to installing upgrades or capability-adding modifications.
- **Bucket 7** only when it is really availability-enablement or service support.

Tag CLS = yes/no as an overlay; do not create a separate bucket for it.

---

## PSC Cheat Sheet

| PSC | Official Description | TAM Bucket | Boundary Note |
|-----|---------------------|------------|---------------|
| 1905 | Combat Ships | 1 | New construction product code — but often NULL on large IDVs |
| 1910 | Transport Vessels | 1 | New construction / conversion |
| 1915 | Patrol Craft | 1 | New construction |
| J998 | Non-Nuclear Ship Repair (East) | 2, 3 | Core ship repair; best single structured filter for in-service work |
| J999 | Non-Nuclear Ship Repair (West) | 2, 3 | Pair with J998 for national view |
| J019 | Maint/Repair/Rebuild—Ships & Small Craft | 2, 3 | Equipment-level ship repair |
| J020 | Maint/Repair/Rebuild—Ship & Marine Equipment | 2, 3 | Marine-equipment repair |
| K019 | Modification—Ships & Small Craft | 4 | Platform-level post-delivery mods |
| K020 | Modification—Ship & Marine Equipment | 4 | System/equipment mods |
| N019 | Installation—Ships & Small Craft | 4 | Platform-level install labor |
| N020 | Installation—Ship & Marine Equipment | 4 | System/equipment install labor |
| R408 | Program Management/Support | 6 | Not hands-on repair |
| R425 | Engineering/Technical | 6 | Lifecycle engineering, DMSMS, technical support |
| M2AA–M2BZ | Husbanding Services sub-codes | 7 | Port/availability support |
| M2CA | Ship Husbanding—Management/Integration | 7 | Integrated port-service management |

---

## Hierarchy of Evidence

| Rank | Evidence Type | Use It For | Why It Works | Main Weakness |
|------|-------------|------------|--------------|---------------|
| 1 | Budget / program line / appropriation | Top-level TAM taxonomy + top-down sizing | Matches how the customer actually funds and governs the work | Less retrieval-friendly for pulling contract data |
| 2 | Official work-type definitions | Boundary rules between construction, maintenance, modernization, life extension, and support | Gives the defensible logic behind "what counts where" | Different services phrase work differently |
| 3 | PSC (predominant product/service) | Primary bottom-up coding spine in FPDS / USAspending | PSC is designed to say what was bought | Mixed awards collapse to a single predominant code; large construction IDVs often lack PSC |
| 4 | Availability acronym + contract keywords | Second-level Navy/USCG tagging and retrieval hints | How ship work is commonly named in contract text | Availability is an execution construct, not a complete work-type taxonomy |
| 5 | NAICS | Broad universe filter / vendor screen only | Useful for finding shipyards and broad maritime suppliers | Too broad: mixes new construction, repair, conversion, and alteration |

---

## Source Index

| ID | Document | Organization | URL |
|----|----------|-------------|-----|
| S1 | DoD FMR Volume 11B (Depot maintenance definition / funding logic) | DoD Comptroller | https://comptroller.defense.gov/portals/45/documents/fmr/volume_11b.pdf |
| S2 | DoD FMR Volume 2A, Ch. 1 (Appropriation boundary rules) | DoD Comptroller | https://comptroller.defense.gov/Portals/45/documents/fmr/current/02a/02a_01.pdf |
| S3 | DoD FMR Volume 2B, Ch. 4 (Procurement exhibits P-3a / P-40) | DoD Comptroller | https://comptroller.defense.gov/Portals/45/documents/fmr/current/02b/02b_04.pdf |
| S4 | FY2026 O-1 Operation and Maintenance Programs | DoD Comptroller | https://comptroller.defense.gov/Portals/45/Documents/defbudget/FY2026/FY2026_o1.pdf |
| S5 | FY2026 P-1 Procurement Programs | DoD Comptroller | https://comptroller.defense.gov/Portals/45/Documents/defbudget/FY2026/FY2026_p1.pdf |
| S6 | Joint Fleet Maintenance Manual (JFMM), Volume II | NAVSEA | https://www.navsea.navy.mil/Portals/103/Documents/SUBMEPP/JFMM/Volume_II.pdf |
| S7 | OPNAVINST 4700.7N Maintenance Policy | Department of the Navy | https://www.secnav.navy.mil/doni/Directives/04000%20Logistical%20Support%20and%20Services/04-700%20G |
| S8 | USCG In-Service Vessel Sustainment (ISVS) Program page | U.S. Coast Guard | https://www.dcms.uscg.mil/Our-Organization/Assistant-Commandant-for-Acquisitions-CG-9/Programs/Surface-Assets-Logistics-Center/In-Service-Vessel-Sustainment/ |
| S9 | USCG FY2026 Congressional Budget Justification | U.S. Coast Guard / DHS | https://www.dhs.gov/sites/default/files/2025-06/25_0613_uscg_fy26-congressional-budget-justificatin.pdf |
| S10 | USCG FY2025 Congressional Justification | U.S. Coast Guard | https://www.uscg.mil/Portals/0/documents/budget/2025/USCG%20FY%202025%20Congressional%20Justification.pdf |
| S11 | PSC Manual April 2024 | Acquisition.gov / GSA | https://www.acquisition.gov/sites/default/files/manual/PSC%20Manual%20April%202024.pdf |
| S12 | NAICS 2022 Manual | U.S. Census / OMB | https://www.census.gov/naics/reference_files_tools/2022_NAICS_Manual.pdf |
| S13 | CNRMC Master Ship Repair Agreement | NAVSEA | https://www.navsea.navy.mil/LinkClick.aspx?fileticket=h5HjhNwz3Zo%3D&mid=36784&portalid=103&tabid=15 |
| S14 | SCN P-1 Budget Exhibits (Shipbuilding & Conversion, Navy) | DoD Comptroller | https://comptroller.defense.gov/Budget-Materials/ |
| S15 | USAspending newbuild discovery pull (this project) | BuildCo analysis | Local: bottomup/newbuild_discovery_report.md |
