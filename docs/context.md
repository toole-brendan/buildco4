TRANSCRIPT BETWEEN ME AND LLM ABOUT HOW TO PROPERLY CATEGORIZE DATA

ME: how are MRO contract awards described by the US DoD/ DoW ? like in budget books or in awards? what about things like setting up combat systems integration, or adding some type of module to a vehicle. how is that described too?

LLM: Taking “DoW” as **Defense-Wide**: in the DoD budget and contracting documents I checked, the Department usually does **not** use the single commercial shorthand **“MRO”** as the formal label. It usually breaks that work out as **maintenance**, **depot maintenance and repairs**, **repair**, **overhaul**, **rebuild**, **modernization**, **sustainment**, or **modification**, depending on what the work actually does. DoD’s current financial guidance defines **depot maintenance and repairs** as maintenance/repair requiring **overhaul, upgrade, or rebuild** plus testing/reclamation, but it **excludes procurement of major modifications or upgrades designed to improve performance**; those are treated separately as modification/upgrade efforts. ([Office of the Under Secretary of Defense][1])

In **budget books**, the O&M side usually shows up in **OP-5** exhibits as plain **maintenance/depot maintenance**. A current Defense-Wide example is SOCOM’s OP-5, which says maintenance includes **installation of modification and conversion kits**, **contractor logistics support (CLS)**, **field service representatives (FSRs)**, and depot-maintenance reimbursements. On the **procurement** side, the standard exhibits are things like **P-1**, **P-1M**, **P-3a (Individual Modification)**, and **P-40**. The key mod exhibit is usually **P-3a**: DoD says it should explain **what additional capability the modification adds** and why it is needed. It also breaks installs into **Group A installation kits** (for example, cables, brackets, interfaces) and **Group B equipment** to be installed (for example, radar, ECM, engine), and it records the **method of implementation** such as contractor, depot field team, or depot modification line. ([Office of the Under Secretary of Defense][2])

That is why something like **“setting up combat systems integration”** is usually **not** written as MRO. In DoD language it tends to become **system integration**, **combat systems engineering**, **ship integration and test engineering**, **installation testing and evaluation**, **design-agent engineering**, or **engineering and technical services**. Funding logic follows that split too: if the effort requires **engineering design, integration, test, or evaluation**, the FMR says it belongs in **RDT&E**; **fully developed and tested modification kits** and their installation move to **Procurement**; and improvements to an **out-of-production but still operational** item can be **O&M** if they stay within the current performance envelope and do not require DT/OT&E. The same FMR also says **land- or sea-based combat system test installations** are RDT&E. ([Office of the Under Secretary of Defense][3])

In **award announcements**, sustainment-type work is described much more directly. Recent DoD announcements use phrases like **“depot level repair, maintenance and modifications”** for sonar systems, and **“ship repair, maintenance and modernization”** for scheduled ship availabilities, including the ability to **complete, coordinate, and integrate** multiple maintenance areas. That is very typical DoD award prose for what a commercial reader might call MRO. ([U.S. Department of War][4])

For **combat-systems integration** specifically, the public award language is usually along the lines of **in-service combat systems engineering**, **ship integration and test engineering**, or integration support covering **design**, **system integration**, **production**, **installation testing and evaluation**, **logistics**, **repair**, and **validation**. Aegis awards, for example, use exactly that family of terms. ([U.S. Department of War][5])

For **adding some kind of module to a vehicle**, the common DoD nouns are **modification**, **retrofit**, **integration**, **engineering change proposal (ECP)**, **modification kits**, **A-kits/B-kits**, **ordnance alteration**, and sometimes **fielding**. Current official examples include Army budget language about **integrating and first fielding the 30mm cannon** on the Stryker DVHA1, an Army award to **integrate** HMS equipment with **Bradley Fighting Vehicles**, a Marine Corps award to **procure, produce, and integrate** a suspension-upgrade **ECP solution** onto M870A2 transporters, an F-35 award for **material modification kits** supporting **retrofit and modification efforts**, and a Navy weapon-system example described as an **ordnance alteration** that, once installed, adds new capability. ([Army Financial Management][6])

So, as a practical translation table: **MRO/sustainment** becomes “**depot-level repair, maintenance, and modification support**” or “**ship repair, maintenance, and modernization**”; **combat systems integration** becomes “**in-service combat systems engineering, ship integration and test engineering, and installation testing/evaluation**”; and **add a module to a vehicle** becomes “**procure, produce, integrate, install, and field [capability] onto [vehicle] via modification kits / retrofit / ECP**.” ([U.S. Department of War][7])

Paste a plain-English requirement and I’ll rewrite it in both **budget-book language** and **award-announcement language**.

[1]: https://comptroller.defense.gov/portals/45/documents/fmr/volume_11b.pdf "https://comptroller.defense.gov/portals/45/documents/fmr/volume_11b.pdf"
[2]: https://comptroller.defense.gov/Portals/45/documents/fmr/current/02b/02b_04.pdf "https://comptroller.defense.gov/Portals/45/documents/fmr/current/02b/02b_04.pdf"
[3]: https://comptroller.defense.gov/Portals/45/documents/fmr/current/02a/02a_01.pdf "https://comptroller.defense.gov/Portals/45/documents/fmr/current/02a/02a_01.pdf"
[4]: https://www.defense.gov/News/Contracts/Contract/Article/3685947/ "https://www.defense.gov/News/Contracts/Contract/Article/3685947/"
[5]: https://www.defense.gov/News/Contracts/Contract/Article/2225212/ "https://www.defense.gov/News/Contracts/Contract/Article/2225212/"
[6]: https://www.asafm.army.mil/Portals/72/Documents/BudgetMaterial/2025/pbr/Army%20FY%202025-Budget%20Highlights.pdf "https://www.asafm.army.mil/Portals/72/Documents/BudgetMaterial/2025/pbr/Army%20FY%202025-Budget%20Highlights.pdf"
[7]: https://www.defense.gov/News/Contracts/Contract/Article/2086591/1000/ "https://www.defense.gov/News/Contracts/Contract/Article/2086591/1000/"

ME: 
PASTED TEXT FROM ME - 


3 agents finished (ctrl+o to expand)
   ├─ Search OMN justification books · 16 tool uses · 43.1k tokens
   │  ⎿  Done
   ├─ Search OPN justification books · 18 tool uses · 30.0k tokens
   │  ⎿  Done
   └─ Search NWCF, SCN, WPN, USCG books · 22 tool uses · 44.8k tokens
      ⎿  Done

⏺ Now I have the full picture. Here's my synthesis.

  ---
  Recommended Taxonomy: Work on In-Service Vessels

  Your categorization needs to be defensible, meaning it should be traceable to
  how the customer (DoD/DHS) actually defines, funds, and contracts this work —
  not invented from scratch. Here's the framework I'd recommend, with the
  reasoning for each category.

  The Core Insight

  Neither the Navy nor the Coast Guard uses "MRO" as a category. The Navy draws
  a hard line between Maintenance and Modernization (separate programs, separate
   budgets, separate governance). The Coast Guard folds everything under three
  "types of maintenance" (corrective, preventive, alterative). The budget
  justification books reinforce this split — maintenance flows through OMN/NWCF,
   while modernization/upgrades flow through OPN/SCN. Contracts in FPDS reflect
  these distinctions through different PSC codes, NAICS codes, and funding
  offices.

  Your taxonomy should respect this structure because your eventual market
  sizing will need to map to traceable funding lines and contract data.

  ---
  The Six Categories

  1. Depot Maintenance (Scheduled Repair & Overhaul)
  - What it is: The core of what people mean by "MRO" — planned, depot-level
  work to restore/sustain a ship's material condition. Executed during
  CNO-scheduled availabilities (SRAs, DSRAs, PMAs, PIAs, overhauls) and CG
  drydock/dockside availabilities.
  - Why it's defensible: This is the single largest line item in OMN (~$13.8B in
   FY26 under SAG 1B4B). The NWCF defines it as "time-critical depot-level
  maintenance, repair, overhaul." The Navy tracks it by availability type with
  explicit counts and dollars. FPDS contracts use PSC codes like J998 (Ship
  Repair) and NAICS 336611.
  - Includes: Overhauls (ROH, COH, EOH), SRAs/DSRAs, PIAs/DPIAs, CIAs, phased
  maintenance, drydocking, hull/mechanical/electrical repair, Class A-D overhaul
   work, MSC Mid-Term Availabilities and ROHs.

  2. Intermediate & Continuous Maintenance (Non-Depot Repair)
  - What it is: Ship repair and maintenance performed outside of major depot
  availabilities — by RMCs, IMAs, tenders, MATs, ASSIST teams, or cutter crews
  with contractor augmentation. Includes continuous maintenance availabilities
  (CMAVs), emergent repairs (ERATA), and voyage repairs.
  - Why it's defensible: OMN separately budgets "Non-depot / Intermediate
  Maintenance" at ~$1.53B/yr. The Navy's tri-level maintenance framework
  (Organizational / Intermediate / Depot) is codified in OPNAVINST 4700.7N. The
  CG's NEM mirrors this with its tri-level structure. Emergent repair (ERATA
  ~$139M) and miscellaneous RA/TA (ORATA ~$1.07B) are separately tracked line
  items.
  - Includes: RMC work, continuous maintenance, emergent/casualty repair, voyage
   repair, IMA support, CASREP-driven work, contractor maintenance augmentation.

  3. Modernization & Capability Upgrades
  - What it is: Work that changes the ship — adds new capability, upgrades
  combat systems, installs new equipment beyond original design. Funded
  primarily through OPN, not OMN.
  - Why it's defensible: The Navy explicitly separates this: "The ship
  modernization program is designed to either add new capability or improve
  reliability" (OPNAVINST 4700.7N). OPN has dedicated BLIs: DDG Mod
  (~$687M-$997M/yr), CG Mod, LCS In-Service Mod, LHA/LHD Midlife. The CG calls
  this "alterative maintenance" and funds it through PC&I. Alteration types
  (SHIPALT, MACHALT, ORDALT, SPALT) are formally tracked. Contract descriptions
  reference "capability insertion," "objective configuration upgrades,"
  "Advanced Capability Build."
  - Includes: Program-funded alterations, tech insertion/tech refresh kits,
  combat system upgrades, backfits/retrofits of new equipment, cybersecurity
  upgrades (TFCA), AIT installation work.

  4. Sustainment Engineering & Obsolescence Management
  - What it is: The engineering, logistics, and procurement work that keeps
  existing systems viable over time — without adding new capability or
  performing physical repair. This is the "keep it from becoming unsupportable"
  work.
  - Why it's defensible: OMN SAG 1B5B ("Ship Depot Operations Support,"
  ~$2.76B/yr) is entirely this — planning, technical support, lifecycle
  maintenance, class maintenance support, Navy Modernization Process design
  services. OPN separately funds DMSMS management with explicit strategies:
  "bridge-buys, life-of-type buys, modernization through replacement,
  modification/redesign, and reclamation." SUPSHIPs, ship lifecycle support
  offices, and engineering services all sit here. The CG funds "Survey and
  Design" for future availabilities separately.
  - Includes: Life cycle engineering, obsolescence/DMSMS management,
  life-of-type buys, spares & repair parts procurement (OPN BA08,
  ~$586M-$884M/yr), SUPSHIP oversight, class maintenance plan development,
  technical manual maintenance, configuration management.

  5. Major Life-Cycle Events (RCOH, SLEP, MMA)
  - What it is: Multi-year, ship-class-level programs that blur the
  maintenance/modernization line — refueling overhauls, service life extensions,
   and major maintenance availabilities that are so large they get their own
  budget line items.
  - Why it's defensible: These have dedicated appropriation-level funding. CVN
  RCOH is funded under SCN (not OMN or OPN) as a multi-billion-dollar line item
  with detailed cost breakdowns (basic construction, electronics, HM&E,
  ordnance, outfitting). The CG's PC&I funds SLEP and MMA as named
  sub-investments under "In-Service Vessel Sustainment." These are categorically
   different from routine depot maintenance in scale, duration, and funding
  mechanism. The Navy's D5 Life Extension and SSBN weapon system work similarly
  sits here.
  - Includes: RCOH, ERO, SLEP, FRAM, MMA, Major Renovation, Depot Modernization
  Periods, midlife overhauls.

  6. Availability Support Services
  - What it is: The overhead and support tasks that enable
  maintenance/modernization but aren't themselves repair or upgrade work — force
   protection, berthing ashore, crane services, scaffolding, shore power, dry
  dock services, environmental compliance.
  - Why it's defensible: The Navy's CSMP formally recognizes "Services" as one
  of four work item categories alongside Condition-Based Maintenance, Engineered
   Maintenance, and Modernization (JFMM Rev D). The CG's SFLC Standard
  Specifications have dedicated specs for docking/undocking (0342), shore power
  (8635), and contractor support infrastructure. OMN tracks berthing and messing
   as a separate sub-element. These show up in FPDS as distinct contract line
  items.
  - Includes: Drydock/berthing services, crane/rigging, scaffolding, shore
  power, environmental remediation, force protection during availabilities,
  test/trials support.

  ---
  Why This Taxonomy Works for Market Sizing

  ┌───────────────────┬─────────────────┬───────────────────────────────────┐
  │     Category      │ Primary Funding │      Traceable In Contracts?      │
  │                   │       Line      │                                   │
  ├───────────────────┼─────────────────┼───────────────────────────────────┤
  │ 1. Depot          │ OMN (1B4B),     │ Yes — PSC J998, NAICS 336611,     │
  │ Maintenance       │ NWCF, CG O&S    │ description keywords              │
  ├───────────────────┼─────────────────┼───────────────────────────────────┤
  │ 2. Intermediate & │ OMN (1B4B       │ Yes — different contracting       │
  │  Continuous       │ sub-elements)   │ offices (RMCs vs. NAVSEA)         │
  │ Maintenance       │                 │                                   │
  ├───────────────────┼─────────────────┼───────────────────────────────────┤
  │ 3. Modernization  │ OPN (multiple   │ Yes — distinct PSC codes,         │
  │ & Capability      │ BLIs), CG PC&I  │ "alteration"/"modernization"      │
  │ Upgrades          │                 │ descriptions                      │
  ├───────────────────┼─────────────────┼───────────────────────────────────┤
  │ 4. Sustainment    │ OMN (1B5B), OPN │ Yes — engineering services PSCs,  │
  │ Engineering &     │  (BA08 spares)  │ DMSMS keywords                    │
  │ Obsolescence      │                 │                                   │
  ├───────────────────┼─────────────────┼───────────────────────────────────┤
  │ 5. Major          │ SCN (RCOH), CG  │ Yes — named programs, distinct    │
  │ Life-Cycle Events │ PC&I (SLEP/MMA) │ appropriations                    │
  ├───────────────────┼─────────────────┼───────────────────────────────────┤
  │ 6. Availability   │ OMN (within     │ Yes — services PSCs, support      │
  │ Support Services  │ 1B4B)           │ CLINs                             │
  └───────────────────┴─────────────────┴───────────────────────────────────┘

  Each category maps to at least one distinct appropriation or budget line item,
   meaning you can size it top-down from PB justification books. Each is also
  findable bottom-up in FPDS/USAspending through a combination of PSC codes,
  NAICS codes, funding agency codes, and description keywords. The two
  approaches cross-check each other.

  What to Call It

  Don't call the overall market "MRO." Call it "In-Service Vessel Work" or
  "Post-Delivery Ship Sustainment & Modernization." This matches how the
  customer thinks about it and avoids the definitional trap of "MRO" which
  neither service actually uses as a category.

✻ Baked for 3m 51s

❯ did you look through FPDS/USAspending?                                        

⏺ No, I only read the guide on how to query those systems — I didn't actually
  pull any data from the APIs. Let me do that now.

  Before I start hitting endpoints, let me think about what would be most
  useful: I should search FPDS for ship repair/maintenance/modernization
  contracts to see how the actual contract descriptions categorize this work —
  that's the ground truth for how the market labels itself.

  Let me pull a sample across a few angles: PSC codes (J998 = ship repair),
  NAICS 336611 (shipbuilding/repair), and keyword searches for key terms.

⏺ 2 agents finished (ctrl+o to expand)
   ├─ FPDS ship repair queries · 29 tool uses · 30.6k tokens
   │  ⎿  Done
   └─ USAspending ship work queries · 13 tool uses · 61.7k tokens
      ⎿  Done

⏺ Good call — the contract data reveals some important things that change my
  earlier recommendation. Here's what I found and how it should reshape the
  taxonomy.

  ---
  What the Contract Data Tells Us

  The single most important finding: Contracting officers don't use the words
  "MRO," "depot maintenance," or "ship overhaul." They use availability type
  abbreviations — DSRA, DMP, SRA, CMAV, EDSRA, etc. The standard contract
  description is just [Ship Name] (Hull #) FY[XX] [Availability Type]. That's
  it. The descriptive richness is in the type of availability, not in prose
  about the work.

  Key data points from the pulls:
  - PSC J998 (Ship Repair) tracks ~$1.6B-$2.3B/yr in DoD obligations — this is
  the best single structured filter
  - PSC J999 (Ship Repair NEC) has ~18,480 records — even larger
  - NAICS 336611 is useless for MRO isolation — it lumps $34.7B submarine
  construction with $15K pump overhauls
  - "Ship maintenance" as a keyword catches management/support contracts, NOT
  hands-on work
  - "Ship overhaul" returns zero results — the Navy doesn't use this phrase
  - The Navy's umbrella IDIQ language explicitly says "Repair, Maintenance and
  Modernization Requirements" — that three-part phrase is the closest thing to a
   contracting officer's version of "MRO"
  - The Coast Guard uses much simpler terminology: DD (Dry Dock), DS (Dockside),
   SLEP
  - The Army uses "Modifications, Modernization and OCCM" and "Master Ship
  Repair Agreement"
  - MSC uses ROH (Regular Overhaul) and MTA (Midterm Availability)

  ---
  Revised Taxonomy — Grounded in All Three Sources

  Based on (1) how the services define work, (2) how they budget it, and (3) how
   they contract it, here are the categories you should use. Each one is
  defensible because it maps to a distinct combination of funding line +
  contract vehicle + PSC code + description language.

  1. Scheduled Depot Availabilities (The Core)

  What it is: CNO-scheduled maintenance periods at private or public shipyards —
   the big-ticket items that dominate PSC J998/J999 spending.

  How it appears in contracts: USS [Name] ([Hull]) FY[XX]
  [DSRA/DMP/SRA/EDSRA/DPMA/PMA]

  How it's budgeted: OMN SAG 1B4B (~$13.8B total, of which depot availabilities
  are the largest share)

  Contract evidence: The top 50 USAspending "ship repair" results are almost
  entirely this — $100M-$600M contracts per ship per availability. BAE Systems,
  NASSCO, Metro Machine, Vigor Marine, HII, Continental Maritime, Marine
  Hydraulics are the dominant vendors.

  Sub-types by availability (from both contract descriptions and Navy taxonomy):

  ┌──────────────┬────────────────────────────────────────┬─────────────────┐
  │ Availability │               What It Is               │ Typical Value   │
  │              │                                        │      Range      │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ DSRA / EDSRA │ Docking Selected Restricted            │ $100M-$350M     │
  │              │ Availability                           │                 │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ DMP / MODPRD │ Depot Modernization Period             │ $100M-$270M     │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ SRA          │ Selected Restricted Availability       │ $100M-$200M     │
  │              │ (non-docking)                          │                 │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ DPMA / EDPMA │ Docking Phased Maintenance             │ $100M-$250M     │
  │              │ Availability                           │                 │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ PIA / DPIA   │ Planned/Drydocking Incremental         │ $150M-$200M     │
  │              │ Availability (carriers)                │                 │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ CIA          │ Carrier Incremental Availability       │ Large           │
  ├──────────────┼────────────────────────────────────────┼─────────────────┤
  │ PSA          │ Post Shakedown Availability            │ Varies          │
  └──────────────┴────────────────────────────────────────┴─────────────────┘

  2. Continuous & Emergent Maintenance (Non-Depot Ship Repair)

  What it is: Shorter-duration maintenance outside major depot availabilities —
  CMAVs, emergent repairs, voyage repairs, intermediate-level work by RMCs/IMAs.

  How it appears in contracts: ACCOMPLISH [Hull] FY[XX] CMAV or ERATA or ORATA
  line items. Also "TYCOM BASE WORK ITEMS."

  How it's budgeted: OMN sub-elements: CMAV (~$651M), ERATA (~$139M), ORATA
  (~$1.07B), Non-depot/IL (~$1.53B)

  Contract evidence: FPDS shows ~1,800 records for CMAV alone, dominated by
  Metro Machine for carrier work in Norfolk. The verbs are "ACCOMPLISH" and
  "DEFINITIZE."

  3. Refueling & Major Life-Cycle Overhauls

  What it is: Multi-year, multi-billion-dollar events — nuclear refueling
  overhauls (RCOH, ERO), submarine engineered overhauls (EOH), and CG
  SLEPs/MMAs. These are categorically different in scale and funding.

  How it appears in contracts: FY[XX] RCOH ACCOMPLISHMENT, USS [Name] EOH
  PLANNING, USCGC [Name] SLEP FY[XX] DRY-DOCK

  How it's budgeted: CVN RCOH is funded under SCN (not OMN) — $2-3B per ship. CG
   SLEPs and MMAs are under PC&I (not O&S). Submarine EOHs are in the public
  naval shipyard workload.

  Contract evidence: HII Newport News holds $3.0-$3.4B RCOH contracts. CG SLEP
  work appears at Mare Island Dry Dock, Vigor Marine. MSC ROHs ($18-27M each) at
   Detyens Shipyards, Subic Drydock, Bayonne Drydock.

  4. Modernization & Alteration Installation

  What it is: Work that changes the ship — installing new combat systems, tech
  insertion kits, backfits, SHIPALTs/ORDALTs. Procurement is through OPN;
  installation happens during availabilities.

  How it appears in contracts: The physical modernization work is embedded
  within availability contracts (the DMP literally stands for "Depot
  Modernization Period"). Separate contracts exist for equipment procurement and
   AIT (Alteration Installation Team) work. The umbrella IDIQ language is
  "Repair, Maintenance and Modernization Requirements."

  How it's budgeted: OPN BLIs: DDG Mod (~$687M-$997M/yr), CG Mod, LCS In-Service
   Mod, LHA/LHD Midlife, HM&E. Total OPN for in-service ship modernization is
  several billion/yr.

  Contract evidence: The "Depot Modernization Period" availability type
  explicitly blends maintenance and modernization. The NASSCO contract for "USS
  Chung-Hoon/USS James E. Williams Depot Modernization Period Availabilities"
  ($435M) is modernization-plus-repair. Army uses "Modifications, Modernization
  and OCCM" as a compound phrase in their watercraft IDIQs.

  5. Sustainment Engineering, Planning & Lifecycle Support

  What it is: The technical workforce that plans, oversees, and supports
  physical work — SUPSHIP offices, lifecycle engineering, class maintenance plan
   development, DMSMS/obsolescence management, and the "Ship Maintenance
  Improvement Program" type contracts.

  How it appears in contracts: "SCIENTIFIC, ENGINEERING, TECHNICAL, AND
  ANALYTICAL (SETA) SUPPORT," "SHIP MAINTENANCE IMPROVEMENT SERVICES," "LIFE
  CYCLE MAINTENANCE," "PLANNING AND TECHNICAL SUPPORT." These use services PSC
  codes (R-series), not J998/J999.

  How it's budgeted: OMN SAG 1B5B (~$2.76B/yr) is entirely this category. Also
  OPN BA08 for spares (~$586M-$884M/yr).

  Contract evidence: CACI ($107M), Antech Systems ($22.8M), Noblis ($28.9M),
  ORBIS SIBRO ($15.8M) — these are the engineering/management support firms,
  distinct from the shipyards doing physical work.

  6. Availability Support Services

  What it is: The infrastructure and overhead that enables availabilities —
  drydock services, crane/rigging, berthing/messing, shore power, scaffolding,
  environmental compliance.

  How it appears in contracts: "DRY DOCK 12 CAPEX," "BERTHING AND MESSING,"
  "SHORE POWER." Also the CG's SFLC Std Spec 0342 (Docking/Undocking) and 8635
  (Shore Power) are standalone CLINs.

  How it's budgeted: Within OMN 1B4B and 1B5B sub-elements. Drydock
  infrastructure itself is a major capital category — the $245M "Multi-Mission
  Drydock" contract and SIOP (Shipyard Infrastructure Optimization Program) are
  here.

  Contract evidence: The FPDS "dry dock" search shows $245M for new drydock
  construction, plus Sasebo/Pearl Harbor drydock infrastructure work. These are
  separable from the ship repair itself.

  ---
  How to Use This for Market Sizing

  ┌──────────────────┬──────────────────────┬───────────────────────────────┐
  │     Category     │   Top-Down Sizing    │   Bottom-Up Contract Filter   │
  │                  │        Source        │                               │
  ├──────────────────┼──────────────────────┼───────────────────────────────┤
  │ 1. Scheduled     │ OMN 1B4B             │ PSC J998 + J999, NAICS        │
  │ Depot            │ availability counts  │ 336611, keywords: hull        │
  │ Availabilities   │ × avg cost           │ designations + availability   │
  │                  │                      │ types                         │
  ├──────────────────┼──────────────────────┼───────────────────────────────┤
  │ 2. Continuous &  │ OMN                  │ FPDS keyword "CMAV" or        │
  │ Emergent         │ CMAV/ERATA/ORATA/IL  │ "ERATA", RMC contracting      │
  │ Maintenance      │ line items           │ offices                       │
  ├──────────────────┼──────────────────────┼───────────────────────────────┤
  │ 3. Refueling &   │ SCN (RCOH), CG PC&I  │ FPDS keywords "RCOH", "EOH",  │
  │ Major Life-Cycle │ (SLEP/MMA)           │ "SLEP", specific PIID         │
  │  Overhauls       │                      │ prefixes                      │
  ├──────────────────┼──────────────────────┼───────────────────────────────┤
  │ 4. Modernization │                      │ PSC J998 where description    │
  │  & Alteration    │ OPN BLIs (DDG Mod,   │ includes "DMP" or "MODPRD";   │
  │ Installation     │ etc.)                │ OPN-funded CLINs within       │
  │                  │                      │ availability contracts        │
  ├──────────────────┼──────────────────────┼───────────────────────────────┤
  │ 5. Sustainment   │                      │ PSC R-series, keywords        │
  │ Engineering &    │ OMN 1B5B             │ "SETA", "lifecycle",          │
  │ Lifecycle        │                      │ "planning", SUPSHIP offices   │
  │ Support          │                      │                               │
  ├──────────────────┼──────────────────────┼───────────────────────────────┤
  │                  │                      │ PSC codes for                 │
  │ 6. Availability  │ OMN sub-elements,    │ crane/berthing/facilities     │
  │ Support Services │ SIOP                 │ services, drydock             │
  │                  │                      │ infrastructure contracts      │
  └──────────────────┴──────────────────────┴───────────────────────────────┘

  The hard part is that categories 1 and 4 overlap in practice — a DMP contract 
  bundles maintenance and modernization into one award. You'll need to decide
  whether to split by funding source (OMN vs. OPN within the same contract) or
  accept that "Depot Availability" contracts are a blended category. For market 
  sizing purposes, I'd recommend keeping them separate top-down (the budget
  books split them cleanly) but acknowledging the overlap bottom-up (the
  contracts don't).

  What to call the overall market: Based on how the Navy's own umbrella IDIQ    
  contracts describe it, the most defensible label is "Ship Repair, Maintenance,
   and Modernization" — that's the exact phrase BAE Systems Hawaii uses for
  their multi-hundred-million-dollar IDIQ, and HII uses a near-identical        
  formulation. It's what the customer calls it.

MY MESSAGE - DoW is department of war.... but i have a problem that i think you can help me with. im a market sizing analyst for a shipbuilder and i need to size the market / the TAM of the MRO and MRO-adjacent market. As in work on already-constructed vessels. but i dont know how to categorize the TYPES of work. i need a defensible reasoning of how I "come up" and categorize the types of work. like should i use how the navy and coast guard define the types of work in official documents, should i use how its described or categorized in justification books, should i use how its awarded in USAspending / FPDS/ SAM.gov? Should I use "Availability"? should i use NAICS or PSC codes? maybe that is the cleanest? idk maybe it should be "availability"? here are notes from a transcript of a conversation between me and an AI agent that might be useful to read - so read that attachment - but don't be overly swayed by it if you don't agree....


LLM: Got it. I read the transcript, and I mostly agree with where it landed, with two tweaks: do not let Navy availability acronyms become the **top-level** taxonomy for the whole TAM, and keep husbanding / availability-support work explicitly **adjacent** unless your yard actually competes there. 

The cleanest defensible answer is a **hybrid hierarchy**:

1. Use **official Navy / Coast Guard program-and-funding logic** to define the market buckets.
2. Use **availability type** as a second-level tag, especially for Navy depot work.
3. Use **PSC codes + keywords + funding office** to pull and assign contracts.
4. Use **NAICS only as a loose universe filter**, not as the taxonomy itself.

That structure is defensible because DoD financial rules separate depot maintenance/repair from major performance-improving modifications, Navy O&M separately budgets **Ship Depot Maintenance** and **Ship Depot Operations Support**, Coast Guard PC&I has a named **In-Service Vessel Sustainment** investment for repair availabilities/MMAs/SLEPs, and PSC is the FPDS field intended to record **what was bought**, using the **predominant** product/service on mixed awards. By contrast, NAICS 336611 is too broad because it includes ship **construction, repair, conversion, alteration, and specialized services**. ([Office of the Under Secretary of Defense][1])

Why not use “availability” as the whole taxonomy? Because it is an **execution construct**, not a complete work-type framework. Navy doctrine has a rich availability vocabulary — overhaul, RCOH/EOH, DMP, PIA/DPIA, SRA/DSRA, PMA/DPMA, CMAV, emergent availabilities — while Coast Guard uses a simpler set such as **dry-dock**, **dockside**, **MMA**, and **SLEP**. And in awards, Navy often names a contract with little more than the ship and the availability type, even when the actual scope blends maintenance, repair, and modernization. That makes availability extremely useful for bottom-up retrieval, but not ideal as your top-level TAM logic. ([NAVSEA][2])

My recommendation would be to use these **six work-type buckets**.

**1. Scheduled depot maintenance and repair.**
This is the core “MRO” bucket: planned shipyard work meant to restore or sustain the ship’s existing condition and readiness. Navy evidence is the JFMM availability structure and the O&M **Ship Depot Maintenance** budget line; Coast Guard analogs are dry-dock and dockside repair availabilities. ([Office of the Under Secretary of Defense][3])

**2. Continuous / intermediate / emergent maintenance.**
This is non-depot repair outside the big yard periods: CMAV-type work, casualty repair, emergent work, short dockside repair, and similar sustainment activity. Navy doctrine explicitly distinguishes CMAV and emergent maintenance from the larger CNO-scheduled availabilities. ([NAVSEA][2])

**3. Modernization and alteration installation.**
This is the “add or change capability” bucket: combat-system upgrades, tech refresh, retrofits, new module installs, SHIPALT-like work, and other configuration changes. This is where I would put “setting up combat-systems integration” or “adding a module” **when it adds capability or changes configuration**, because DoD financial rules exclude major performance-improving modifications from depot maintenance/repair, and the P-3a modification exhibit is explicitly about what additional capability a modification adds and how it will be installed. ([Office of the Under Secretary of Defense][1])

**4. Major life-extension / recapitalization events.**
This is for unusually large in-service events that are not routine repair: RCOH/EOH on the Navy side, and Coast Guard **MMA** and **SLEP** on the USCG side. Coast Guard’s current budget is very explicit that ISVS funds vessel repair availabilities including MMAs and SLEPs, and it even distinguishes SLEP as extending service life **without significantly modifying capabilities**. ([NAVSEA][2])

**5. Sustainment engineering, planning, and obsolescence support.**
This is engineering and lifecycle support around in-service vessels: technical planning, survey/design, class support, program support, configuration/obsolescence work, and related technical services. It is adjacent to MRO, not hands-on repair. Navy budget structure includes **Ship Depot Operations Support** as a separate line, PSC has **R425 Engineering/Technical** and **R408 Program Management/Support**, and Coast Guard funds survey/design work to plan future MMAs, SLEPs, and recapitalization efforts. ([Office of the Under Secretary of Defense][3])

**6. Availability support / husbanding / port services.**
This is the enablement layer: force protection, waste removal, material handling, berthing, cranes, forklifts, tug/pilot/port services, and integrated husbanding support. I would keep this as **MRO-adjacent** unless your firm directly sells into it. PSC now has dedicated ship-husbanding codes for exactly these services. ([Acquisition.gov][4])

For the **coding spine**, PSC is the best primary choice. The reason is simple: PSC is the federal field meant to describe what was purchased, and for mixed contracts it uses the **predominant** product/service. For ship work, whole-ship repair often lands in **J998/J999**, equipment-level repair can show up in **J019/J020**, modifications in **K019/K020**, installation in **N019/N020**, engineering support in **R425** or **R408**, and husbanding/port services in **M2AA–M2CA**. That is much more analytically useful than NAICS, which blurs new construction and in-service work. ([Acquisition.gov][4])

A practical classification rule is:

* **Restore existing capability / condition** → maintenance & repair.
* **Add capability or change configuration** → modernization / alteration.
* **Extend service life at platform scale** → life-extension / recapitalization.
* **Plan, engineer, analyze, or manage the work without doing the repair/install itself** → sustainment engineering/support.
* **Enable the availability with shore/port/support services** → availability support.

That rule is consistent with the DoD FMR distinction between maintenance and major upgrades, Coast Guard’s separation of MMA/SLEP, and the PSC structure. ([Office of the Under Secretary of Defense][5])

The big complication is that **contracts are often blended**. A DMP or DSRA award can include maintenance, repair, and modernization in one package, and Navy award language says exactly that. One current DMP award for USS *Kidd* was explicitly described as **repair, maintenance, and modernization**, and it carried both O&M and Other Procurement funding. So at the contract level, I would not force false precision. Use a **primary bucket + secondary tag** system, and only split dollars further if you have CLIN-level visibility or clear funding separation. That approach also matches the PSC manual’s “predominant product/service” rule for mixed awards. ([U.S. Department of War][6])

So the short answer to your specific “what should I use?” question is:

* **Official definitions + budget books:** yes, this should anchor the taxonomy.
* **USAspending / FPDS / SAM descriptions:** yes, but as the retrieval and validation layer, not the conceptual source of truth.
* **Availability:** yes, but one level down, mainly for Navy depot work.
* **PSC:** yes, this is the cleanest contract-data backbone.
* **NAICS:** no, not as the main categorization method. ([Office of the Under Secretary of Defense][1])

For the market name itself, I would call it **“in-service vessel sustainment, repair, and modernization”** or, if you want language closer to the contract market, **“ship repair, maintenance, and modernization.”** That matches Navy award language much better than plain “MRO.” ([U.S. Department of War][7])

A useful next artifact would be a one-page crosswalk with columns for **bucket / official definition / budget source / PSCs / availability keywords / include-exclude rules**.

[1]: https://comptroller.defense.gov/portals/45/documents/fmr/volume_11b.pdf "https://comptroller.defense.gov/portals/45/documents/fmr/volume_11b.pdf"
[2]: https://www.navsea.navy.mil/Portals/103/Documents/SUBMEPP/JFMM/Volume_II.pdf "https://www.navsea.navy.mil/Portals/103/Documents/SUBMEPP/JFMM/Volume_II.pdf"
[3]: https://comptroller.defense.gov/Portals/45/Documents/defbudget/FY2026/FY2026_o1.pdf "https://comptroller.defense.gov/Portals/45/Documents/defbudget/FY2026/FY2026_o1.pdf"
[4]: https://www.acquisition.gov/sites/default/files/manual/PSC%20Manual%20April%202024.pdf "https://www.acquisition.gov/sites/default/files/manual/PSC%20Manual%20April%202024.pdf"
[5]: https://comptroller.defense.gov/Portals/45/documents/fmr/current/02a/02a_01.pdf "https://comptroller.defense.gov/Portals/45/documents/fmr/current/02a/02a_01.pdf"
[6]: https://www.defense.gov/News/Contracts/Contract/Article/3946889/ "https://www.defense.gov/News/Contracts/Contract/Article/3946889/"
[7]: https://www.defense.gov/News/Contracts/Contract/Article/2086591/1000/ "https://www.defense.gov/News/Contracts/Contract/Article/2086591/1000/"


ME: Final Answer: How to Categorize the In-Service Vessel Work Market

  After looking at all three layers — (1) how the Navy/CG officially define work
   types, (2) how the budget justification books fund them, and (3) how
  contracts are actually awarded and coded in FPDS — here's the taxonomy I'd
  defend:

  ---
  The Framework: Two Axes

  You need two axes, not one, because the government itself uses two systems
  that don't perfectly align:

  Axis 1 — What gets contracted (bottom-up, from FPDS):
  This is what you can actually measure with contract data.

  Axis 2 — What gets budgeted (top-down, from PB justification books):
  This is how the customer thinks about and plans the work.

  The market sizing works by triangulating between the two.

  ---
  Axis 1: Contract-Traceable Categories

  #: 1
  Category: Non-Nuclear Ship Availabilities
  PSC Codes: J998, J999
  ~Annual Spend: $4-5B/yr
  What It Actually Is: The core market. Every DSRA, DMP, SRA, CMAV, EDSRA, DPMA,

    PIA — all bundled into single contracts that include repair + maintenance +
    modernization. This is the number.
  ────────────────────────────────────────
  #: 2
  Category: Ship & Marine Equipment Maintenance
  PSC Codes: J019, J020
  ~Annual Spend: $700M-1B/yr
  What It Actually Is: Component-level repair, smaller vessel work, work outside

    major availabilities. Trending upward.
  ────────────────────────────────────────
  #: 3
  Category: Nuclear Overhauls (RCOH/ERO/EOH)
  PSC Codes: Not J998/J999 (excluded by definition)
  ~Annual Spend: $2-4B/yr
  What It Actually Is: Funded under SCN. HII Newport News monopoly for carriers;

    public shipyards for subs. Entirely separate contracting and funding.
  ────────────────────────────────────────
  #: 4
  Category: Engineering, Planning & Technical Support
  PSC Codes: R425, R408, L019, L020
  ~Annual Spend: $2-3B/yr (needs filtering to ship-specific)
  What It Actually Is: SETA contracts, SUPSHIP oversight, lifecycle engineering,

    class maintenance planning, DMSMS management. The brains behind the
    wrench-turning. OMN SAG 1B5B (~$2.76B) is the budget proxy.
  ────────────────────────────────────────
  #: 5
  Category: Equipment Procurement for Backfit/Modernization
  PSC Codes: Product codes (FSC 19xx, 20xx, etc.)
  ~Annual Spend: Several $B/yr
  What It Actually Is: The OPN-funded combat systems, tech insertion kits, HM&E
    equipment, and spares that get installed during availabilities but are
  bought
     separately. DDG Mod alone is ~$700M-1B/yr.
  ────────────────────────────────────────
  #: 6
  Category: Ship Modification & Installation (standalone)
  PSC Codes: K019, N019
  ~Annual Spend: $130-230M/yr
  What It Actually Is: Standalone mod/install contracts not bundled into
    availabilities. K019 is collapsing as work gets absorbed into availability
    contracts; N019 is growing.
  ────────────────────────────────────────
  #: 7
  Category: Testing, Inspection & QC
  PSC Codes: H119, H120, H219, H319
  ~Annual Spend: Needs pull
  What It Actually Is: Standalone testing/inspection contracts. Much of this is
    embedded in availability contracts, but some is separate.
  ────────────────────────────────────────
  #: 8
  Category: Port Services & Husbanding
  PSC Codes: M2xx series
  ~Annual Spend: Needs pull
  What It Actually Is: Berthing, force protection, tugs, pilots, cranes, waste
    removal. Activated as PSC codes in 2020.
  ────────────────────────────────────────
  #: 9
  Category: CG In-Service Vessel Sustainment
  PSC Codes: J998/J999 + CG-specific
  ~Annual Spend: $400M-1B/yr (growing)
  What It Actually Is: CG drydocks, dockside avails, SLEPs, MMAs. Funded under
    PC&I and O&S. Smaller contracts, different vendor base (Mare Island,
    Colonna's, Vigor, Birdon).

  ---
  Axis 2: Budget-Traceable Categories (How the Customer Thinks About It)

  ┌─────┬─────────────────────────┬───────────────────┬─────────────────────┐
  │  #  │        Category         │   Appropriation   │   ~Annual Budget    │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │     │ Depot Maintenance       │                   │ ~$8-10B of the      │
  │ A   │ (scheduled              │ OMN (1B4B)        │ $13.8B SAG          │
  │     │ availabilities)         │                   │                     │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │ B   │ Intermediate &          │ OMN (1B4B         │ ~$3-4B (CMAV,       │
  │     │ Continuous Maintenance  │ sub-elements)     │ ERATA, ORATA, IL)   │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │     │ Ship Modernization      │ OPN (DDG Mod, CG  │                     │
  │ C   │ (equipment +            │ Mod, LCS Mod,     │ ~$2-3B across BLIs  │
  │     │ installation)           │ etc.)             │                     │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │ D   │ Sustainment Engineering │ OMN (1B5B)        │ ~$2.76B             │
  │     │  & Planning             │                   │                     │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │     │ Nuclear                 │                   │ ~$2-4B per year     │
  │ E   │ Refueling/Overhaul      │ SCN               │ depending on RCOH   │
  │     │                         │                   │ cycle               │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │ F   │ Spares & Repair Parts   │ OPN (BA08)        │ ~$600M-900M/yr      │
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │ G   │ CG In-Service Vessel    │ CG PC&I + O&S     │ ~$400M-1B/yr        │
  │     │ Sustainment             │                   │                     │   
  ├─────┼─────────────────────────┼───────────────────┼─────────────────────┤
  │     │                         │ OMN (SIOP) +      │ ~$1-2B/yr           │   
  │ H   │ Shipyard Infrastructure │ MILCON            │ (enabling, not      │   
  │     │                         │                   │ vessel work itself) │
  └─────┴─────────────────────────┴───────────────────┴─────────────────────┘   
                  
  ---
  The Total Market Size
                                                                                
  If your TAM is "all work on already-constructed vessels," then summing the
  non-overlapping contract categories:                                          
                  
  ┌───────────────────────────────────────────────────────────┬──────────────┐  
  │                         Component                         │ Annual Spend │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Non-nuclear ship availabilities (J998+J999)               │ $4-5B        │
  ├───────────────────────────────────────────────────────────┼──────────────┤
  │ Ship/marine equipment maintenance (J019+J020)             │ $0.7-1B      │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Nuclear overhauls (RCOH/ERO/EOH)                          │ $2-4B        │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Engineering & technical support (ship-specific R/L codes) │ $2-3B        │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Equipment procurement for backfit (OPN)                   │ $2-3B        │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Standalone mod/install (K019+N019)                        │ $0.1-0.2B    │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ CG in-service sustainment                                 │ $0.4-1B      │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Spares & repair parts                                     │ $0.6-0.9B    │
  ├───────────────────────────────────────────────────────────┼──────────────┤  
  │ Total                                                     │ ~$12-18B/yr  │
  └───────────────────────────────────────────────────────────┴──────────────┘  
                  
  Add port services, testing/inspection, and shipyard infrastructure enabling   
  costs and you're pushing toward $15-21B/yr as the broadest defensible TAM for
  the U.S. federal in-service vessel work market.                               
                  
  ---                                                                           
  What to Call It
                                                                                
  Don't call it "MRO" — neither service uses that term, and it understates the
  scope (it misses modernization, which is a huge chunk). Don't call it "ship   
  repair" — that understates it too (it's just J998/J999).
                                                                                
  Call it "In-Service Vessel Sustainment & Modernization" or, if you want the   
  language contracting officers actually use: "Ship Repair, Maintenance, and 
  Modernization."                                                               
                  
  ---
  Why This Is Defensible
                                                                                
  Every number traces to one of three authoritative sources:
  1. FPDS contract data — PSC-coded, publicly queryable, deduplicated by PIID   
  2. PB justification books — appropriation-level, submitted to Congress,       
  line-item detail                                                       
  3. Official policy documents — OPNAVINST 4700.7N, JFMM, NEM define the        
  taxonomy the services themselves use                                  
                                                                                
  You didn't invent categories. You mapped the categories the customer already
  uses across their three systems (policy → budget → contract) and showed where 
  they align and where they don't.
                                                                                
✻ Baked for 44s                 


MY MESSAGE TO LLM - well what do you think about this? or do you still prefer the categorization that you said in your latest response? - 


LLM: I’m comparing your framework against the one I recommended, focusing on the real choice: top-level market buckets versus retrieval tags, and whether either better fits official funding/contracting structure.

I’ve narrowed it down: your draft looks stronger for measurement, mainly because the two-axis model is useful, but I wouldn’t adopt it wholesale as the leadership version. I’m validating where it aligns with official Navy/USCG structures and where it risks double counting modernization, engineering support, spares, and public-yard work.

Thought for 8m 17s

I’d split the difference:

I like this better as a market-sizing method, but not as the final category list.
The strongest improvement in the note is the two-axis idea: one view for what you can actually pull from contracts, and another for how the customer budgets and thinks about the work. That is a real upgrade over a single flat taxonomy. I also agree with the note’s instinct to center PSC + availability language + budget lines, and to demote NAICS to a supporting filter.

Where I would not adopt it exactly is the category design. Several of the listed “categories” are not the same kind of thing:

Non-nuclear ship availabilities is a work package / execution form.
Nuclear overhauls is a program/funding segment.
CG in-service vessel sustainment is a customer segment.
Equipment procurement for backfit and spares are product/content buckets.
Port services/husbanding is an enabling-support layer.
That makes the list very useful for data pulls, but less clean as the category set you present as a mutually exclusive TAM framework.

So I still prefer my earlier functional categorization for the presentation layer, but I would combine it with this note’s two-axis logic for the model layer.

My practical recommendation would be:

Use one primary taxonomy for the TAM

These should be your headline buckets.

Scheduled depot repair & maintenance availabilities
Intermediate / continuous / emergent repair
Modernization / alteration installation
Major life-cycle events
RCOH / EOH / SLEP / MMA type work
Sustainment engineering / planning / lifecycle support
Availability support services
husbanding, docking support, cranes, shore power, etc.
Optional adjacent bucket: in-service equipment / kits / spares content
only include this if you intentionally want a broader ecosystem TAM, not just shipyard-addressable work
Then tag every record with overlays

These are not top-level TAM buckets; they are slicing dimensions:

Availability type: DSRA, DMP, SRA, CMAV, etc.
Customer/service: Navy, Coast Guard, MSC, Army, etc.
Funding: OMN, OPN, SCN, PC&I, O&S
PSC family
Nuclear vs non-nuclear
Core vs adjacent vs non-addressable

That structure gives you the best of both worlds:

a clean, defensible story for executives
a traceable extraction logic for FPDS/USAspending and budget books

The biggest thing I’d change from the uploaded note is this:

Do not make these top-level categories

Coast Guard, nuclear, and equipment procurement should not sit at the same level as “repair” or “engineering.”
They should be treated as:

customer overlays: Coast Guard
program overlays: nuclear
content overlays: equipment / spares

Otherwise you risk double counting and category confusion.

A few specific judgments:

“Availability” is still not the whole taxonomy. It is a very good contract-language tag, but not the best top-level market logic.
Testing / inspection / QC is probably too small and too embedded to stand alone unless your data pull proves otherwise. I would usually fold it into engineering/support or availability support.
Shipyard infrastructure / SIOP / drydock capex should be outside your vessel-work TAM unless you deliberately want an “enabling ecosystem” view.
The note’s TAM sum is directionally useful, but I would trust the framework more than the summed number until you tighten overlap rules.

So the cleanest final answer is:

Yes, I would adopt the uploaded note’s two-axis approach.
No, I would not use its raw category list unchanged.
I would keep my earlier work-type buckets as the main taxonomy, and use the uploaded note’s contract/budget structure as the measurement backbone.

If I were naming the three layers in a deck, I’d use:

Core yard-work TAM
Adjacent sustainment-services TAM
Broader in-service vessel ecosystem TAM

That framing is especially useful for a shipbuilder, because it separates:

what a yard can realistically capture,
what is adjacent but winnable,
and what is technically in the market but mostly belongs to OEMs, public yards, or infrastructure programs.

Paste your current draft category tree and I’ll turn it into a MECE-style version with include/exclude rules and sample PSC/keyword mapping.

**WORKBOOK FROM LLM** IN OTHER FILE (In_Service_Vessel_TAM_Crosswalk (1).xlsx)



ME: where would cls / contractor logistics support be in the crosswalk? just answer in chat about that. but then can you make an artifact that is specifically centered on the defensibility of the 6 buckets that you arrived at in column A of the artifact that you made in your last response? (so - 

1. Scheduled depot maintenance & repair
2. Continuous / intermediate / emergent maintenance
3. Modernization & alteration installation
4. Major life-cycle events / service-life extension
5. Sustainment engineering / planning / obsolescence support
6. Availability support / husbanding / port services 

-- WHICH I AGREE WITH)

I agree with those buckets, but i just want a one pager centered on the defensibility of those categories, centered on WHY we chose those buckets, which center on explaining in plain-speak, simple terms, that these are the most appropriate categorizations and buckets because of..... (language used in budget books, language use in contract awards, language used in internal official navy / coast guard documents...)


LLM: CLS should usually be treated as a **secondary tag / delivery construct**, not as a seventh top-level bucket.

My rule would be:

* **Default home: Bucket 5** when the scope is mostly lifecycle support, planning, technical support, materiel management, or sustainment support.
* **Bucket 1** when the CLS scope is predominantly contractor-performed depot work during a scheduled availability.
* **Bucket 2** when it is predominantly recurring / intermediate / emergent hands-on maintenance.
* **Bucket 3** when it is mainly tied to installing upgrades or capability-adding modifications.
* **Bucket 6** only when it is really availability-enablement or service support around the work.

That is the cleanest defensible approach because DoD’s depot-maintenance definition explicitly says depot maintenance can include **interim contractor support / contractor logistics support** to the extent it is for services, but it **does not include major performance-improving modifications or upgrades**; and PSC guidance says to classify a contract by the **predominant** product or service being bought. So for TAM purposes, I would code **CLS by the underlying work type**, then keep a **CLS = yes/no** tag on top of that. ([Office of the Under Secretary of Defense][1]) ([Acquisition.GOV][2])

I also made the one-pager centered on **why the six buckets are defensible** in plain language, using the same logic you agreed with: they line up with named budget lines like **Ship Depot Maintenance** and **Ship Depot Operations Support**, with JFMM’s split between scheduled availabilities and CMAV/emergent work, with procurement modification exhibits for capability-adding installs, with Coast Guard ISVS naming **MMA** and **SLEP**, with Coast Guard WISS separating **maintenance actions** from **service actions**, and with award language that explicitly says **ship repair, maintenance and modernization**.    ([Office of the Under Secretary of Defense][3]) ([Office of the Under Secretary of Defense][4])  ([USCG Mission Support][5]) ([U.S. Department of War][6])

Artifacts:

* [Editable DOCX](sandbox:/mnt/data/Six_Bucket_Defensibility_OnePager.docx)
* [PDF version](sandbox:/mnt/data/Six_Bucket_Defensibility_OnePager.pdf)

[1]: https://comptroller.defense.gov/portals/45/documents/fmr/volume_11b.pdf#:~:text=L2439%40P84%3A%20%201,performance%2C%20the%20nuclear%20refueling%20or "VOLUME 11B"
[2]: https://www.acquisition.gov/sites/default/files/manual/PSC%20Manual%20April%202024.pdf#:~:text=L230%40P6%3A%20%E2%97%8F%20How%20do%20I,captured%20in%20and%20reported%20from "Microsoft Word - PSC Manual April 2024.docx"
[3]: https://comptroller.defense.gov/Portals/45/documents/fmr/current/02b/02b_04.pdf#:~:text=L497%40P19%3A%20Classification,Identify%20the%20operational "VOLUME 2B, CHAPTER 4"
[4]: https://comptroller.defense.gov/Portals/45/documents/fmr/current/02b/02b_04.pdf#:~:text=L531%40P20%3A%20,radar%2C%20ECM%2C%20engine%20etc "VOLUME 2B, CHAPTER 4"
[5]: https://www.dcms.uscg.mil/Portals/10/CG-4/documents/SFLC/WISS.pdf?ver=o_W4XjEHRMoVw4Ym6MzGWQ%3D%3D#:~:text=L53%40P4%3A%20Generic%20Maintenance%20Actions%20These,General%20Requirements%20Items%20Item%E2%80%9D%20herein "Process Guide Template"
[6]: https://www.defense.gov/News/Contracts/Contract/Article/2086591/1000/ "
	Contracts For Feb. 18, 2020 > U.S. Department of War > Contract | U.S. Department of War
"

See other artifacts - 
Six_Bucket_Defensibility_OnePager.docx
Six_Bucket_Defensibility_OnePager.pdf