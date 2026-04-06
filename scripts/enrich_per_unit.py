"""
Enrich DDG top-down and bottom-up CSVs with per-unit cost columns.

Top-down: uses qty from budget exhibits (P-1, P-5c)
Bottom-up: maps MYP contracts to known ship counts from budget books
"""
import csv
import re
from pathlib import Path

# ── Top-down enrichment ──────────────────────────────────────────────────────

# Known quantities from SCN P-1 and P-5c exhibits
# Format: (program, fiscal_year) -> qty
TOPDOWN_QTY = {
    # DDG-51 P-5c Total Ship Estimates
    ("DDG 51", "FY2016"): 3,
    ("DDG 51", "FY2017"): 2,
    ("DDG 51", "FY2018"): 2,
    ("DDG 51", "FY2019"): 3,
    ("DDG 51", "FY2020"): 3,
    ("DDG 51", "FY2021"): 2,
    ("DDG 51", "FY2022"): 2,
    ("DDG 51", "FY2023"): 3,
    # DDG-51 P-1 Gross Construction Cost
    ("DDG 51", "FY2024"): 2,
    ("DDG 51", "FY2025"): 3,
    ("DDG 51", "FY2026"): 2,  # reconciliation ships
    # DDG 1000 - 3 ships total (class is complete)
    ("DDG 1000", "Prior Years"): 3,
    # DDG 1000 CPS APMs
}

# Descriptions that are per-ship-class totals (eligible for per-unit calc)
TOPDOWN_UNIT_ELIGIBLE = [
    "Construction Gross Cost",
    "Construction Total",
    "Construction Mandatory",
    "Total Ship Estimate",
    "Unit Cost",  # already per-unit, just tag it
    "Gross Weapon System Cost",  # DDG 1000
    "Cumulative Prior Years",
]

# DDG MOD: installation quantities from budget book (FY2026 schedule)
# HM&E Mod: 1, DDG MOD 1.0: 1, DDG MOD 1.5: 2, DDG MOD DMP2: 1
# Total ships receiving DDG MOD work in FY2026: ~5 (overlapping work packages)
DDG_MOD_SHIPS_FY26 = 5  # approximate from install schedule

# CPS APMs have explicit quantities
CPS_APM_QTY = {
    "FY2024": 3,
    "FY2025": 3,
    "FY2026": 2,
}

def enrich_topdown():
    inpath = Path("topdown/ddg_topdown.csv")
    rows = []
    with open(inpath) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Add new columns
    new_fields = fieldnames + ["qty_units", "cost_per_unit_thousands", "cost_per_unit_millions", "unit_basis"]

    outpath = Path("topdown/ddg_topdown.csv")
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fields)
        writer.writeheader()

        for row in rows:
            prog = row["program_name"]
            fy = row["fiscal_year"]
            desc = row["description"]
            amt_str = row["amount_thousands"]
            amt = float(amt_str) if amt_str and amt_str != "0" else 0

            qty = None
            unit_basis = ""

            # Already-stated unit costs (just pass through)
            if "Unit Cost" in desc:
                row["qty_units"] = "1"
                row["cost_per_unit_thousands"] = amt_str
                row["cost_per_unit_millions"] = f"{amt / 1000:.3f}" if amt else ""
                row["unit_basis"] = "Budget exhibit stated unit cost"
                writer.writerow(row)
                continue

            # DDG-51 construction / ship estimates
            if prog == "DDG 51" and any(k in desc for k in ["Construction Gross Cost", "Construction Total", "Construction Mandatory", "Total Ship Estimate"]):
                key = (prog, fy)
                qty = TOPDOWN_QTY.get(key)
                unit_basis = "Ship qty from SCN P-1/P-5c exhibit"

            # DDG-51 construction gross cost - FY2026 disc has 0 new ships
            if "Construction Gross Cost (Disc)" in desc and fy == "FY2026":
                qty = None  # discretionary portion isn't for new ships
                unit_basis = ""

            # DDG 1000 class-level totals (3 ships)
            if prog == "DDG 1000" and "Cumulative Prior Years" in desc:
                qty = 3
                unit_basis = "DDG 1000 class = 3 ships (DDG 1000/1001/1002)"

            # DDG 1000 support equipment - per class (3 ships)
            if prog == "DDG 1000" and "Support Equipment - Total" in desc:
                qty = 3
                unit_basis = "DDG 1000 class = 3 ships"

            # DDG 1000 CPS totals - being installed on all 3 ships
            if prog == "DDG 1000" and "Conventional Prompt Strike (CPS) - Total" in desc:
                qty = 3
                unit_basis = "CPS integration across 3 DDG 1000 ships"

            # CPS APMs have explicit quantities
            if "Advanced Payload Modules" in desc:
                qty = CPS_APM_QTY.get(fy)
                unit_basis = "APM qty from P-3a exhibit"

            # DDG MOD total line items
            if "DDG Modernization - Total" in desc and fy == "FY2026":
                qty = DDG_MOD_SHIPS_FY26
                unit_basis = f"~{DDG_MOD_SHIPS_FY26} ships receiving DDG MOD work in FY26 (approx from install schedule)"

            # DDG MOD totals for FY24/25 - harder to know exact ship count
            if "DDG Modernization - Total (Disc Base)" in desc:
                # We don't have exact FY24/FY25 install counts, skip
                pass

            # SPY-6(V)4 radar - the biggest DDG MOD sub-element
            if "SPY-6(V)4" in desc:
                # DDG MOD 2.0 starts with 0 installs in FY26 per schedule
                # but procurement is for future installs (2 ships in FY30/31)
                qty = 2
                unit_basis = "SPY-6(V)4 procurement for 2 future DDG MOD 2.0 ships"

            # Write enriched row
            if qty and amt:
                per_unit = amt / qty
                row["qty_units"] = str(qty)
                row["cost_per_unit_thousands"] = f"{per_unit:.0f}"
                row["cost_per_unit_millions"] = f"{per_unit / 1000:.3f}"
                row["unit_basis"] = unit_basis
            else:
                row["qty_units"] = str(qty) if qty else ""
                row["cost_per_unit_thousands"] = ""
                row["cost_per_unit_millions"] = ""
                row["unit_basis"] = unit_basis

            writer.writerow(row)

    print(f"Top-down enriched: {outpath}")


# ── Bottom-up enrichment ─────────────────────────────────────────────────────

# Known MYP contract -> ship count mappings from SCN P-5c production status
# Contract award dates and hull numbers from budget exhibit:
#   MYP I (FY13-17): awarded Jun 2013 / Sep 2017
#     BIW (N0002413C2305 approx): DDG 124, 126, ... ~5 ships
#     HII  (N0002413C2307 approx): ~5 ships
#   MYP II (FY18-22): awarded Sep 2018
#     BIW (N0002418C2305): DDG 129, 133, 134, 136, 138 = 5 ships
#     HII  (N0002418C2307): DDG 128, 130, 131, 132, 135, 137, 139 = 7 ships
#   MYP III (FY23-27): awarded Aug 2023
#     BIW (N0002423C2305): DDG 141, 143, 145, 147 = ~4 ships
#     HII  (N0002423C2307): DDG 140, 142, 144, 146 = ~4 ships + options

CONTRACT_SHIP_MAP = {
    # FY23-27 MYP II contracts
    "N0002423C2307": {"vendor": "HII", "ships": 5, "hulls": "DDG 140,142,144,146 + options", "program": "DDG-51 MYP III FY23-27"},
    "N0002423C2305": {"vendor": "BIW", "ships": 4, "hulls": "DDG 141,143,145,147", "program": "DDG-51 MYP III FY23-27"},
    # FY18-22 MYP I contracts
    "N0002418C2307": {"vendor": "HII", "ships": 7, "hulls": "DDG 128,130,131,132,135,137,139", "program": "DDG-51 MYP II FY18-22"},
    "N0002418C2305": {"vendor": "BIW", "ships": 5, "hulls": "DDG 129,133,134,136,138", "program": "DDG-51 MYP II FY18-22"},
    # FY13-17 MYP contracts
    "N0002413C2305": {"vendor": "BIW", "ships": 5, "hulls": "DDG 117,119,121,123,125 (approx)", "program": "DDG-51 MYP I FY13-17"},
    "N0002413C2307": {"vendor": "HII", "ships": 5, "hulls": "DDG 118,120,122,124,127 (approx)", "program": "DDG-51 MYP I FY13-17"},
    # DDG 1000 class contracts
    "N0002402C2303": {"vendor": "BIW", "ships": 3, "hulls": "DDG 1000,1001,1002 (detail design + lead ship)", "program": "DDG 1000 Detail Design/Construction"},
    "N0002408C2309": {"vendor": "BIW", "ships": 2, "hulls": "DDG 1001,1002 (construction)", "program": "DDG 1001/1002 Construction"},
}

# For single-ship contracts, try to detect from description
SINGLE_SHIP_PATTERN = re.compile(r"DDG[- ]?(\d{2,4})\b")

def enrich_bottomup():
    inpath = Path("bottomup/ddg_bottomup.csv")
    rows = []
    with open(inpath) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    new_fields = fieldnames + ["qty_ships", "cost_per_ship", "cost_per_ship_millions", "hull_numbers", "unit_basis"]

    outpath = Path("bottomup/ddg_bottomup.csv")
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fields)
        writer.writeheader()

        mapped = 0
        for row in rows:
            award_id = row["award_id"]
            desc = (row["description"] or "").upper()
            amt_str = row["award_amount"]
            amt = float(amt_str) if amt_str else 0

            qty = None
            hulls = ""
            unit_basis = ""

            # Check known contract map
            if award_id in CONTRACT_SHIP_MAP:
                info = CONTRACT_SHIP_MAP[award_id]
                qty = info["ships"]
                hulls = info["hulls"]
                unit_basis = f"Known MYP mapping: {info['program']}"

            # Single-ship contracts: description references exactly one DDG hull
            elif not qty:
                hull_matches = SINGLE_SHIP_PATTERN.findall(desc)
                unique_hulls = set(hull_matches)
                # Filter out hull numbers that are clearly not ship references
                # (e.g., "DDG 51 CLASS" shouldn't count 51 as a hull)
                real_hulls = set()
                for h in unique_hulls:
                    num = int(h)
                    # DDG 51-150 are Arleigh Burke, DDG 1000-1002 are Zumwalt
                    if (51 <= num <= 150) or (1000 <= num <= 1002):
                        # Make sure it's not just "DDG 51 CLASS" pattern
                        if f"DDG {h} CLASS" not in desc and f"DDG-{h} CLASS" not in desc and f"DDG{h} CLASS" not in desc:
                            real_hulls.add(h)

                if len(real_hulls) == 1:
                    qty = 1
                    hulls = f"DDG {list(real_hulls)[0]}"
                    unit_basis = "Single hull number in description"
                elif len(real_hulls) > 1:
                    qty = len(real_hulls)
                    hulls = ", ".join(f"DDG {h}" for h in sorted(real_hulls, key=int))
                    unit_basis = f"{qty} hull numbers identified in description"

            # Construction-type detection for unmapped multi-ship
            if not qty and "CONSTRUCTION" in desc and "DDG 51" in desc:
                # Can't determine ship count, flag it
                unit_basis = "Multi-ship construction contract; qty unknown"

            if qty and amt:
                per_ship = amt / qty
                row["qty_ships"] = str(qty)
                row["cost_per_ship"] = f"{per_ship:.2f}"
                row["cost_per_ship_millions"] = f"{per_ship / 1e6:.1f}"
                row["hull_numbers"] = hulls
                row["unit_basis"] = unit_basis
                mapped += 1
            else:
                row["qty_ships"] = str(qty) if qty else ""
                row["cost_per_ship"] = ""
                row["cost_per_ship_millions"] = ""
                row["hull_numbers"] = hulls
                row["unit_basis"] = unit_basis

            writer.writerow(row)

    print(f"Bottom-up enriched: {outpath}")
    print(f"  {mapped} of {len(rows)} awards have per-unit cost ({mapped/len(rows)*100:.0f}%)")


if __name__ == "__main__":
    enrich_topdown()
    enrich_bottomup()
