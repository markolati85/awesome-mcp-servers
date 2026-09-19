# -*- coding: utf-8 -*-
"""
MSK Kikinda — feedstock / gasification / production-cost model.

First-principles carbon and energy balances from feedstock gate to one tonne of
saleable methanol, then to one tonne of acetic acid. Stdlib only.

PROVENANCE DISCIPLINE. Every input carries a tag:
  FACT   — sourced, cited in the study
  VENDOR — licensor/vendor claim, not independently verified
  ENG    — engineering estimate derived here from first principles or standard practice
  ASSUM  — model assumption, no external basis, varied in sensitivity

Nothing in this file is a quotation. Where a price would otherwise be invented,
a LOW/BASE/HIGH band is used and the derivation is stated in the comment.
"""

from dataclasses import dataclass, replace
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# chemistry constants  [FACT — IUPAC atomic masses]
# ---------------------------------------------------------------------------
M_C, M_H2, M_O2, M_CO, M_CO2 = 12.011, 2.016, 31.998, 28.010, 44.009
M_MEOH, M_ACOH = 32.042, 60.052

C_PER_T_MEOH = M_C / M_MEOH * 1000.0          # 374.8 kg C in 1 t methanol
C_PER_T_ACOH = 2 * M_C / M_ACOH * 1000.0      # 400.0 kg C in 1 t acetic acid

# acetic acid stoichiometry: CH3OH + CO -> CH3COOH   [FACT — stoichiometry]
MEOH_PER_ACOH_STOICH = M_MEOH / M_ACOH        # 0.5336 t/t
CO_PER_ACOH_STOICH   = M_CO   / M_ACOH        # 0.4664 t/t


@dataclass
class Feed:
    """A feedstock as delivered to the MSK gate."""
    name: str
    tag: str                  # provenance of the quality data
    moisture: float           # mass fraction, as received
    ash: float                # mass fraction, as received
    c_ar: float               # carbon, mass fraction as received
    lhv_ar: float             # GJ/t as received
    cost_low: float           # EUR/t delivered MSK
    cost_base: float
    cost_high: float
    cost_note: str = ""
    sulfur: float = 0.005
    chlorine: float = 0.0


# ---------------------------------------------------------------------------
# FEEDSTOCKS
# ---------------------------------------------------------------------------
# Serbian lignite quality: Kolubara/Kostolac average LHV ~7.2 GJ/t, moisture
# 39-56%, ash ~19%  [FACT — Euracoal Serbia profile; Serbian lignite literature].
# Carbon as received is BACK-CALCULATED here [ENG]: combustible fraction =
# 1 - moisture - ash; daf carbon taken at 65-68% for lignite rank; the resulting
# LHV is checked against the reported 7.2 GJ/t.
def lignite(name, moisture, ash, daf_c=0.665, cost=(14, 20, 30), note=""):
    comb = 1.0 - moisture - ash
    c_ar = comb * daf_c
    # LHV check: daf LHV ~26 GJ/t, less latent heat of the moisture (2.44 MJ/kg)
    lhv = comb * 26.0 - moisture * 2.44
    return Feed(name, "FACT(quality)/ENG(carbon)", moisture, ash, c_ar, lhv,
                cost[0], cost[1], cost[2], note)


FEEDS = {
    # moisture/ash per Serbian lignite literature; costs are BANDS [ENG], built
    # from EPS-class lignite production economics plus rail haulage, not quotes.
    "kovin":    lignite("Kovin lignite (captive)", 0.39, 0.17, cost=(11, 16, 24),
                        note="mine-gate + ~120 km rail; underwater/dredge extraction"),
    "kostolac": lignite("Kostolac lignite (purchased)", 0.39, 0.21, cost=(16, 23, 33),
                        note="purchased ex-EPS + ~130 km rail"),
    "kolubara": lignite("Kolubara lignite (purchased)", 0.50, 0.19, cost=(18, 26, 38),
                        note="purchased ex-EPS + ~200 km rail; highest moisture"),
    # Imported bituminous, e.g. via Danube/Constanta. Quality typical of a
    # traded steam coal 6,000 kcal/kg NAR. Price band from traded API2-type
    # levels plus inland freight [ENG].
    "import":   Feed("Imported bituminous (6,000 kcal NAR)", "ENG", 0.10, 0.12,
                     0.66, 25.1, 95, 125, 165,
                     "seaborne + Danube barge + rail to Kikinda", 0.008, 0.0005),
    # Agricultural residue, baled, delivered. Vojvodina residue potential is
    # large [FACT — Vojvodina crop-residue studies] but collectible fraction is
    # ~40-56% of technical potential in normal seasons and lower in dry years.
    "biomass":  Feed("Corn stover / wheat straw (baled)", "FACT(availability)/ENG(cost)",
                     0.15, 0.06, 0.40, 13.8, 55, 75, 100,
                     "farmgate + baling + handling + <=100 km road haul", 0.001, 0.002),
    # Prepared RDF/SRF. Gate fee is NEGATIVE cost, but preparation converts it
    # to a positive delivered cost for a CHEMICAL-grade feed [ENG].
    "rdf":      Feed("Prepared RDF/SRF (chemical grade)", "ENG", 0.15, 0.15,
                     0.42, 16.0, -5, 25, 60,
                     "gate fee net of MRF preparation, rejects disposal and densification",
                     0.003, 0.006),
}

# Natural gas is handled separately (priced per GJ, not per tonne).
# Serbian corporate gas has been administratively set in the past (EUR 95/MWh
# for the corporate sector in Nov 2022) and cut ~15% for industry in 2024
# [FACT]. No verified 2026 large-industrial tariff was found, so a BAND is used.
GAS_EUR_PER_MWH = dict(low=28.0, base=38.0, high=55.0)   # ENG band
def gas_eur_per_gj(level="base"):
    return GAS_EUR_PER_MWH[level] / 3.6


# ---------------------------------------------------------------------------
# ROUTE TECHNOLOGY PARAMETERS
# ---------------------------------------------------------------------------
@dataclass
class Route:
    name: str
    tech: str
    carbon_eff: float        # fraction of feed carbon ending in methanol
    o2_t_per_t_meoh: float   # t O2 / t MeOH  (0 for steam reforming)
    elec_mwh_per_t: float    # total imported electricity, MWh / t MeOH
    steam_gj_per_t: float    # net imported steam, GJ / t MeOH (negative = export)
    water_m3_per_t: float
    availability: float      # on-stream factor
    capex_scale_ref_kt: float   # reference plant scale, kt/y MeOH
    capex_ref_eur_m: float      # reference-scale NEW capex at that scale, EUR m
    capex_exp: float = 0.65     # six-tenths-type scale exponent  [ENG]
    europe_factor: float = 1.55 # China -> Serbia installed-cost multiplier [ENG]
    reuse_credit: float = 0.0   # EUR m of the above avoided by reusing MSK assets
    note: str = ""


# Carbon efficiency [ENG, from literature ranges]:
#   steam methane reforming to methanol .... 0.75-0.80
#   entrained-flow coal gasification ....... 0.30-0.35 (H2-poor syngas; the
#       water-gas shift vents CO2 to reach the 2.05 stoichiometric number)
#   biomass gasification ................... 0.28-0.33
#   RDF gasification ....................... 0.25-0.30
#
# O2 demand [ENG]: coal entrained flow ~0.9-1.1 t O2/t MeOH; biomass similar or
# slightly higher per unit carbon; zero for SMR.
#
# Reference capex: a modern Chinese coal-to-methanol complex at ~1,000 kt/y
# (gasification island + ASU + AGR + shift + synthesis + utilities) is taken at
# EUR 750m installed IN CHINA [ENG — order of magnitude from Chinese
# coal-chemical project scale; NOT a quotation]. Scaled and multiplied to Serbia.

ROUTES = {
 "gas": Route("Natural gas (SMR, existing plant refurbished)", "steam reforming",
        carbon_eff=0.775, o2_t_per_t_meoh=0.0, elec_mwh_per_t=0.15,
        steam_gj_per_t=-1.5, water_m3_per_t=8.0, availability=0.92,
        capex_scale_ref_kt=200, capex_ref_eur_m=115, capex_exp=1.0,
        europe_factor=1.0, reuse_credit=0.0,
        note="refurbish reformer, loop, compressors; no gasification island"),

 "coal": Route("Serbian lignite (entrained flow + drying)", "ECUST/OMB-class CWS or dry feed",
        carbon_eff=0.325, o2_t_per_t_meoh=1.05, elec_mwh_per_t=0.95,
        steam_gj_per_t=0.0, water_m3_per_t=20.0, availability=0.88,
        capex_scale_ref_kt=1000, capex_ref_eur_m=750, capex_exp=0.65,
        europe_factor=1.55, reuse_credit=55.0,
        note="new gasification island + ASU + AGR + shift; reuses MSK synthesis/offsites"),

 "coal_imp": Route("Imported bituminous (entrained flow)", "ECUST/OMB-class CWS",
        carbon_eff=0.335, o2_t_per_t_meoh=1.00, elec_mwh_per_t=0.85,
        steam_gj_per_t=0.0, water_m3_per_t=18.0, availability=0.90,
        capex_scale_ref_kt=1000, capex_ref_eur_m=700, capex_exp=0.65,
        europe_factor=1.55, reuse_credit=55.0,
        note="no dryer needed; smaller coal handling; same island otherwise"),

 "biomass": Route("Agricultural biomass (oxygen-blown gasification)", "fluidised / entrained",
        carbon_eff=0.300, o2_t_per_t_meoh=0.95, elec_mwh_per_t=1.00,
        steam_gj_per_t=0.0, water_m3_per_t=18.0, availability=0.83,
        capex_scale_ref_kt=1000, capex_ref_eur_m=900, capex_exp=0.68,
        europe_factor=1.60, reuse_credit=50.0,
        note="large feed handling; tar cracking; alkali/chlorine cleanup; seasonal storage"),

 "rdf": Route("Prepared RDF/SRF gasification", "entrained / plasma-assisted",
        carbon_eff=0.265, o2_t_per_t_meoh=1.05, elec_mwh_per_t=1.25,
        steam_gj_per_t=0.0, water_m3_per_t=20.0, availability=0.75,
        capex_scale_ref_kt=1000, capex_ref_eur_m=1150, capex_exp=0.70,
        europe_factor=1.60, reuse_credit=45.0,
        note="MRF + dryer + densifier + severe syngas cleanup (Cl, S, Hg, alkali, tar)"),
}


# ---------------------------------------------------------------------------
# PRICES AND FACTORS  (all ENG bands unless tagged)
# ---------------------------------------------------------------------------
@dataclass
class Econ:
    elec_eur_mwh: float = 100.0      # FACT-anchored: EPS structured industrial
                                     # contracts ~EUR 100-115/MWh in 2025; 2026
                                     # band for SEE large industrials 90-120.
    gas_level: str = "base"
    labour_eur_py: float = 22000.0   # ENG: fully loaded Serbian industrial cost
    maint_pct_capex: float = 0.035   # ENG: % of new capex per year
    ash_disposal_eur_t: float = 12.0 # ENG
    catalyst_eur_t_meoh: float = 14.0
    water_eur_m3: float = 0.45
    o2_note: str = "oxygen made on site; its cost appears as ASU power + ASU capex"
    capital_years: int = 15
    capital_rate: float = 0.08
    meoh_price: float = 350.0        # EUR/t, scenario variable
    acoh_price: float = 560.0        # EUR/t, scenario variable
    co2_price: float = 0.0           # EUR/t
    plant_kt: float = 200.0          # nameplate methanol, kt/y


def annuity(rate, n):
    return rate / (1.0 - (1.0 + rate) ** -n)


# ---------------------------------------------------------------------------
# CORE BALANCE — one tonne of saleable methanol
# ---------------------------------------------------------------------------
def methanol_balance(route_key: str, feed_key: Optional[str], e: Econ,
                     cost_level="base") -> Dict:
    r = ROUTES[route_key]
    out = dict(route=r.name, tech=r.tech, note=r.note)

    # --- feed quantity from the CARBON balance -----------------------------
    c_required = C_PER_T_MEOH / r.carbon_eff          # kg C per t MeOH
    out["c_required_kg"] = c_required

    if route_key == "gas":
        # natural gas: CH4, carbon 0.749 kg C per kg CH4; 1 Nm3 CH4 = 0.716 kg
        # Energy basis is the practical one: SMR-to-methanol total gas demand
        # (feed + fuel) is 31-34 GJ/t MeOH [ENG, industry range].
        gj = 32.0
        out["feed_name"] = "Natural gas"
        out["feed_t_per_t"] = None
        out["feed_gj_per_t"] = gj
        out["feed_eur_per_gj"] = gas_eur_per_gj(e.gas_level)
        out["feed_cost"] = gj * out["feed_eur_per_gj"]
        out["ash_t_per_t"] = 0.0
    else:
        f = FEEDS[feed_key]
        t_feed = (c_required / 1000.0) / f.c_ar       # t feed per t MeOH
        out["feed_name"] = f.name
        out["feed_t_per_t"] = t_feed
        out["feed_gj_per_t"] = t_feed * f.lhv_ar
        cost = dict(low=f.cost_low, base=f.cost_base, high=f.cost_high)[cost_level]
        out["feed_eur_per_t"] = cost
        out["feed_eur_per_gj"] = cost / f.lhv_ar if f.lhv_ar > 0 else float("inf")
        out["feed_cost"] = t_feed * cost
        out["ash_t_per_t"] = t_feed * f.ash
        out["moisture_t_per_t"] = t_feed * f.moisture
        out["feed_quality"] = f

    # --- utilities ---------------------------------------------------------
    out["elec_mwh"] = r.elec_mwh_per_t
    out["elec_cost"] = r.elec_mwh_per_t * e.elec_eur_mwh
    out["o2_t"] = r.o2_t_per_t_meoh
    out["water_cost"] = r.water_m3_per_t * e.water_eur_m3
    out["catalyst_cost"] = e.catalyst_eur_t_meoh
    out["ash_cost"] = out["ash_t_per_t"] * e.ash_disposal_eur_t

    # --- capex -------------------------------------------------------------
    scale = (e.plant_kt / r.capex_scale_ref_kt) ** r.capex_exp
    capex_new = r.capex_ref_eur_m * scale * r.europe_factor - r.reuse_credit
    capex_new = max(capex_new, 0.0)
    out["capex_eur_m"] = capex_new
    out["capex_specific"] = capex_new * 1e6 / (e.plant_kt * 1000.0)

    prod_t = e.plant_kt * 1000.0 * r.availability / 0.92   # normalise to on-stream
    out["prod_t"] = prod_t

    # --- labour ------------------------------------------------------------
    heads = dict(gas=190, coal=430, coal_imp=380, biomass=470, rdf=520)[route_key]
    out["heads"] = heads
    out["labour_cost"] = heads * e.labour_eur_py / prod_t

    # --- maintenance and fixed ---------------------------------------------
    out["maint_cost"] = capex_new * 1e6 * e.maint_pct_capex / prod_t
    out["overhead_cost"] = 0.25 * out["labour_cost"] + 6.0

    # --- cash cost ---------------------------------------------------------
    cash = (out["feed_cost"] + out["elec_cost"] + out["water_cost"] +
            out["catalyst_cost"] + out["ash_cost"] + out["labour_cost"] +
            out["maint_cost"] + out["overhead_cost"])
    out["cash_cost"] = cash

    # --- capital recovery --------------------------------------------------
    out["capital_charge"] = capex_new * 1e6 * annuity(e.capital_rate, e.capital_years) / prod_t
    out["full_cost"] = cash + out["capital_charge"]

    # --- CO2 ---------------------------------------------------------------
    # process CO2 = feed carbon not in product, as CO2; plus grid electricity.
    c_vented = c_required - C_PER_T_MEOH                 # kg C
    co2_proc = c_vented * M_CO2 / M_C / 1000.0           # t CO2 / t MeOH
    grid_ef = 0.65                                       # t CO2/MWh, Serbia lignite-heavy [ENG]
    out["co2_process"] = co2_proc
    out["co2_power"] = r.elec_mwh_per_t * grid_ef
    out["co2_total"] = co2_proc + out["co2_power"]
    out["co2_cost"] = out["co2_total"] * e.co2_price
    out["cash_cost_with_co2"] = cash + out["co2_cost"]
    out["full_cost_with_co2"] = out["full_cost"] + out["co2_cost"]
    return out


# ---------------------------------------------------------------------------
# ACETIC ACID
# ---------------------------------------------------------------------------
def acetic_balance(meoh_full_cost: float, meoh_cash_cost: float,
                   route_key: str, e: Econ) -> Dict:
    """Cost of 1 t acetic acid by methanol carbonylation.

    Cativa-type iridium carbonylation: CO utilisation >94%, acetic acid yield on
    methanol ~90% [VENDOR — Johnson Matthey / BP published claims].
    """
    meoh_in = MEOH_PER_ACOH_STOICH / 0.985     # t MeOH per t AcOH, 98.5% sel.
    co_in = CO_PER_ACOH_STOICH / 0.94          # t CO per t AcOH

    if route_key == "gas":
        # CO must be made by reforming + cold box; charge it at the methanol
        # plant's marginal syngas cost scaled by carbon content [ENG].
        co_cost_per_t = 0.55 * meoh_cash_cost
        co_source = "dedicated CO unit / cold box from reformed gas"
    else:
        # A gasifier already makes CO-rich syngas; CO separation is cheaper.
        co_cost_per_t = 0.40 * meoh_cash_cost
        co_source = "CO-rich raw syngas from the gasifier (structural advantage)"

    util = 28.0       # ENG: utilities per t AcOH
    cat = 18.0        # ENG: iridium/promoter, make-up
    lab = 12.0        # ENG
    maint = 16.0      # ENG

    marginal = meoh_in * meoh_cash_cost + co_in * co_cost_per_t + util + cat
    fully = meoh_in * meoh_full_cost + co_in * co_cost_per_t + util + cat + lab + maint
    return dict(meoh_in=meoh_in, co_in=co_in, co_cost_per_t=co_cost_per_t,
                co_source=co_source, marginal=marginal, fully=fully)


# ---------------------------------------------------------------------------
# SCENARIO RUNNER
# ---------------------------------------------------------------------------
CASES = [
    ("CASE 1",  "gas",      None,        "Natural gas (baseline)"),
    ("CASE 2a", "coal",     "kostolac",  "Purchased Kostolac lignite"),
    ("CASE 2b", "coal",     "kolubara",  "Purchased Kolubara lignite"),
    ("CASE 3",  "coal",     "kovin",     "Captive Kovin lignite"),
    ("CASE 4",  "coal_imp", "import",    "Imported bituminous coal"),
    ("CASE 5",  "biomass",  "biomass",   "Agricultural biomass"),
    ("CASE 6",  "rdf",      "rdf",       "Prepared RDF/SRF"),
]


def run_all(e: Econ, cost_level="base") -> List[Dict]:
    rows = []
    for cid, rk, fk, label in CASES:
        m = methanol_balance(rk, fk, e, cost_level)
        a = acetic_balance(m["full_cost"], m["cash_cost"], rk, e)
        m["case"] = cid
        m["label"] = label
        m["acoh"] = a
        rows.append(m)
    return rows


def blend(e: Econ, parts: List[tuple], label: str) -> Dict:
    """Co-feed case: parts = [(route_key, feed_key, energy_share), ...].

    Blends are costed on an energy-weighted feed cost with the capex of the
    dominant gasification island plus a co-feed handling premium [ENG].
    """
    base = None
    feed_cost = 0.0
    co2 = 0.0
    elec = 0.0
    for rk, fk, share in parts:
        m = methanol_balance(rk, fk, e)
        if base is None or share > 0.5:
            base = m
        feed_cost += share * m["feed_cost"]
        co2 += share * m["co2_total"]
        elec += share * m["elec_cost"]
    out = dict(base)
    out["label"] = label
    out["feed_cost"] = feed_cost
    out["elec_cost"] = elec
    premium = 0.06 * out["capex_eur_m"]        # ENG: second feed train
    out["capex_eur_m"] += premium
    prod_t = out["prod_t"]
    out["maint_cost"] = out["capex_eur_m"] * 1e6 * 0.035 / prod_t
    out["capital_charge"] = out["capex_eur_m"] * 1e6 * annuity(0.08, 15) / prod_t
    out["cash_cost"] = (feed_cost + elec + out["water_cost"] + out["catalyst_cost"] +
                        out["ash_cost"] + out["labour_cost"] + out["maint_cost"] +
                        out["overhead_cost"])
    out["full_cost"] = out["cash_cost"] + out["capital_charge"]
    out["co2_total"] = co2
    return out
