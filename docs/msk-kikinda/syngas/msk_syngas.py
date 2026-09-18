# -*- coding: utf-8 -*-
"""
MSK Kikinda — zero-feed / ultra-low-cost syngas screening model.

Integrated carbon + hydrogen + oxygen balance for the CORRECT production slate:
    150,000 t/y MERCHANT methanol
     50,000 t/y acetic acid  (which internally consumes methanol and CO)

Stdlib only. Tags: FACT / VENDOR / ENG / ASSUM. No price here is a quotation.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional

# ---- exact chemistry [FACT] -------------------------------------------------
M_C, M_H2, M_O2, M_CO, M_CO2 = 12.011, 2.016, 31.998, 28.010, 44.009
M_MEOH, M_ACOH, M_CH4 = 32.042, 60.052, 16.043

# ---- INTEGRATED PRODUCTION BALANCE -----------------------------------------
MERCHANT_MEOH = 150_000.0
ACOH          =  50_000.0
SEL_MEOH      = 0.985      # methanol selectivity in carbonylation [VENDOR]
UTIL_CO       = 0.94       # CO utilisation, Cativa-class [VENDOR]

MEOH_FOR_ACOH = ACOH * (M_MEOH / M_ACOH) / SEL_MEOH      # t/y
CO_FOR_ACOH   = ACOH * (M_CO   / M_ACOH) / UTIL_CO       # t/y
TOTAL_MEOH    = MERCHANT_MEOH + MEOH_FOR_ACOH            # t/y

# per tonne of methanol [FACT, stoichiometry]
C_PER_T_MEOH  = M_C  / M_MEOH * 1000.0    # 374.8 kg C
H2_PER_T_MEOH = 2*M_H2 / M_MEOH * 1000.0  # 125.8 kg H2 (CO + 2H2 -> CH3OH)
H2_LOSS       = 1.03                      # purge/loss factor [ENG]

# CO for acetic acid carries its own carbon
C_PER_T_CO    = M_C / M_CO * 1000.0       # 428.8 kg C per t CO

# ---- existing MSK assets [FACT — MSK site + user brief] --------------------
ASU_NM3_H       = 19_000.0        # existing oxygen plant
ASU_HOURS       = 8_000.0         # [ASSUM]
O2_KG_PER_NM3   = 1.429
ASU_T_PER_YEAR  = ASU_NM3_H * O2_KG_PER_NM3 * ASU_HOURS / 1000.0
COSORB_T_PER_Y  = 55_000.0        # existing CO separation capacity

# ---- natural gas reference [FACT — user-supplied delivered price] ----------
USD_PER_1000NM3 = 505.0
USD_EUR         = 0.92            # [ASSUM]
GJ_PER_1000NM3  = 32.3            # LHV of pipeline gas [ENG]
GAS_EUR_PER_GJ  = USD_PER_1000NM3 * USD_EUR / GJ_PER_1000NM3
GAS_TARGET_LOW  = 200.0 * USD_EUR / GJ_PER_1000NM3   # the $200/1000Nm3 the plant wants
GAS_TARGET_HIGH = 230.0 * USD_EUR / GJ_PER_1000NM3


@dataclass
class Route:
    key: str
    name: str
    bucket: str                    # A bankable / B emerging / C breakthrough
    carbon_source: str
    c_eff: float                   # feed carbon -> product carbon
    # carbon carrier
    feed_c_frac: float = 0.0       # kg C per kg feed (0 for CO2/electro routes)
    feed_h_frac: float = 0.0       # kg H per kg feed
    feed_eur_t: tuple = (0, 0, 0)  # LOW/BASE/HIGH delivered EUR/t
    feed_unit: str = "t"
    # hydrogen
    ext_h2_frac: float = 0.0       # fraction of required H2 supplied by electrolysis
    h2_kwh_per_kg: float = 52.0    # [FACT-anchored: SOEC <36 core, ~40 system;
                                   #  alkaline/PEM system 50-55]
    # other power (gasifier aux, compression, ASU if used)
    aux_mwh_per_t: float = 0.45
    uses_asu: bool = True
    # capex
    capex_low: float = 0.0         # EUR m, NEW capex only
    capex_base: float = 0.0
    capex_high: float = 0.0
    availability: float = 0.90
    heads: int = 200
    reuse: str = ""
    killer: str = ""


def annuity(r, n):
    return r / (1 - (1 + r) ** -n)


def run(rt: Route, elec: float, feed_level="base", capex_level="base",
        capital_rate=0.08, capital_years=15) -> Dict:
    """Cost of ONE TONNE of methanol, on the integrated slate."""
    o = dict(route=rt.name, key=rt.key, bucket=rt.bucket)

    # ---------- carbon ----------
    # total carbon the site must import = carbon in all methanol + carbon in the
    # CO that goes to acetic acid, both divided by the route's carbon efficiency.
    c_total_kg = (TOTAL_MEOH * C_PER_T_MEOH + CO_FOR_ACOH * C_PER_T_CO) / rt.c_eff
    c_per_t_meoh = c_total_kg / TOTAL_MEOH
    o["c_per_t"] = c_per_t_meoh

    if rt.feed_c_frac > 0:
        feed_t = c_per_t_meoh / 1000.0 / rt.feed_c_frac
        px = dict(low=rt.feed_eur_t[0], base=rt.feed_eur_t[1], high=rt.feed_eur_t[2])[feed_level]
        o["feed_t_per_t"] = feed_t
        o["feed_eur_t"] = px
        o["feed_cost"] = feed_t * px
        h_from_feed = feed_t * 1000.0 * rt.feed_h_frac      # kg H
    else:
        # CO2-based route: carbon arrives as CO2
        co2_t = c_per_t_meoh / 1000.0 * (M_CO2 / M_C)
        px = dict(low=rt.feed_eur_t[0], base=rt.feed_eur_t[1], high=rt.feed_eur_t[2])[feed_level]
        o["feed_t_per_t"] = co2_t
        o["feed_eur_t"] = px
        o["feed_cost"] = co2_t * px
        h_from_feed = 0.0

    # ---------- hydrogen ----------
    h2_need = H2_PER_T_MEOH * H2_LOSS
    # CO for acetic acid needs no hydrogen, but the shift-free design must still
    # balance the whole syngas stream; charge H2 only against methanol.
    h2_ext = max(0.0, h2_need - h_from_feed) * rt.ext_h2_frac
    o["h2_kg_per_t"] = h2_ext
    o["h2_mwh_per_t"] = h2_ext * rt.h2_kwh_per_kg / 1000.0

    # ---------- oxygen ----------
    # electrolysis yields 8 kg O2 per kg H2 [FACT, stoichiometry]
    o2_from_electro = h2_ext * 8.0
    # POX / gasification oxygen demand ~1.33 kg O2 per kg C to CO, plus heat [ENG]
    o2_need = c_per_t_meoh * 1.45 / 1000.0 * 1000.0 if rt.feed_c_frac > 0 else 0.0
    o["o2_need_kg"] = o2_need
    o["o2_electro_kg"] = o2_from_electro
    o["o2_from_asu_kg"] = max(0.0, o2_need - o2_from_electro)
    o["o2_surplus_kg"] = max(0.0, o2_from_electro - o2_need)
    o["asu_t_per_y"] = o["o2_from_asu_kg"] * TOTAL_MEOH / 1000.0
    o["asu_ok"] = o["asu_t_per_y"] <= ASU_T_PER_YEAR
    o["asu_headroom_pct"] = (1 - o["asu_t_per_y"] / ASU_T_PER_YEAR) * 100 if ASU_T_PER_YEAR else 0

    # ---------- power ----------
    aux = rt.aux_mwh_per_t
    if not o["asu_ok"] and rt.uses_asu:
        aux += 0.15          # extra ASU capacity would be needed [ENG]
    o["aux_mwh_per_t"] = aux
    o["mwh_per_t"] = o["h2_mwh_per_t"] + aux
    o["power_cost"] = o["mwh_per_t"] * elec
    o["mw_continuous"] = o["mwh_per_t"] * TOTAL_MEOH / ASU_HOURS
    o["twh_per_y"] = o["mwh_per_t"] * TOTAL_MEOH / 1e6

    # ---------- other opex ----------
    capex = dict(low=rt.capex_low, base=rt.capex_base, high=rt.capex_high)[capex_level]
    o["capex"] = capex
    prod = TOTAL_MEOH * rt.availability / 0.90
    o["maint"] = capex * 1e6 * 0.035 / prod
    o["labour"] = rt.heads * 22_000.0 / prod
    o["other"] = 34.0                   # catalyst, chemicals, water, waste [ENG]
    o["cash"] = (o["feed_cost"] + o["power_cost"] + o["maint"] +
                 o["labour"] + o["other"])
    o["capchg"] = capex * 1e6 * annuity(capital_rate, capital_years) / prod
    o["full"] = o["cash"] + o["capchg"]

    # ---------- acetic acid ----------
    meoh_in = (M_MEOH / M_ACOH) / SEL_MEOH
    co_in = (M_CO / M_ACOH) / UTIL_CO
    # CO is a co-product of the same syngas; charge it at the marginal carbon +
    # separation cost rather than at the methanol price [ENG]
    co_cost = 0.42 * o["cash"] if rt.feed_c_frac > 0 else 0.55 * o["cash"]
    o["acoh_marginal"] = meoh_in * o["cash"] + co_in * co_cost + 46.0
    o["acoh_full"] = meoh_in * o["full"] + co_in * co_cost + 74.0

    # ---------- CO2 ----------
    c_vent = c_per_t_meoh - C_PER_T_MEOH
    o["co2_process"] = max(0.0, c_vent) * (M_CO2 / M_C) / 1000.0
    o["co2_power"] = o["mwh_per_t"] * 0.65
    o["co2_total"] = o["co2_process"] + o["co2_power"]
    return o


def breakeven_power(rt: Route, target_cash: float, feed_level="base") -> Optional[float]:
    """Electricity price at which this route's cash cost equals target."""
    lo, hi = 0.0, 400.0
    if run(rt, lo, feed_level)["cash"] > target_cash:
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        if run(rt, mid, feed_level)["cash"] <= target_cash:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ============================ THE ROUTES ====================================
# Petcoke: fuel grade 6.5% S benchmark quoted at USD 104.50/t FOB US Gulf [FACT];
# delivered Kikinda adds ocean freight, Constanta handling and Danube/rail [ENG].
PETCOKE_DELIVERED = (120.0, 155.0, 200.0)

ROUTES: List[Route] = [
 Route("R1","Natural gas POX (status quo, $505/1,000 Nm3)","A","pipeline gas",
       c_eff=0.72, feed_c_frac=0.749, feed_h_frac=0.251,
       feed_eur_t=(GAS_EUR_PER_GJ*50.0,)*3,   # placeholder, overridden below
       ext_h2_frac=0.0, aux_mwh_per_t=0.25, capex_low=90, capex_base=115,
       capex_high=150, heads=190,
       reuse="everything", killer="feedstock price alone is EUR 546/t methanol"),

 Route("R2","Petcoke via existing POX, conventional shift","A","imported petcoke",
       c_eff=0.335, feed_c_frac=0.88, feed_h_frac=0.035, feed_eur_t=PETCOKE_DELIVERED,
       ext_h2_frac=0.0, aux_mwh_per_t=0.55, capex_low=120, capex_base=165,
       capex_high=230, heads=280,
       reuse="ASU, COSORB, syngas compression, MeOH loop, AcOH plant, utilities",
       killer="5-6.5% sulphur: large AGR and sulphur recovery, permitting"),

 Route("R3","Petcoke + electrolytic H2 (shift-free, electrolyser O2)","B","imported petcoke",
       c_eff=0.90, feed_c_frac=0.88, feed_h_frac=0.035, feed_eur_t=PETCOKE_DELIVERED,
       ext_h2_frac=1.0, aux_mwh_per_t=0.40, capex_low=230, capex_base=310,
       capex_high=430, heads=270,
       reuse="POX shell, COSORB, MeOH loop, AcOH plant; ASU becomes redundant",
       killer="5.9 MWh/t of electrolysis: only works on dedicated cheap power"),

 Route("R4","Refinery vacuum residue + electrolytic H2","B","heavy residue",
       c_eff=0.90, feed_c_frac=0.855, feed_h_frac=0.105, feed_eur_t=(150,210,280),
       ext_h2_frac=1.0, aux_mwh_per_t=0.40, capex_low=210, capex_base=285,
       capex_high=395, heads=260,
       reuse="POX is natively a liquid-feed gasifier - best mechanical fit",
       killer="residue is a traded fuel; price tracks crude, less discount than petcoke"),

 Route("R5","Torrefied biomass / biochar hubs + electrolytic H2","B","regional biochar",
       c_eff=0.88, feed_c_frac=0.72, feed_h_frac=0.04, feed_eur_t=(120,165,220),
       ext_h2_frac=1.0, aux_mwh_per_t=0.45, capex_low=280, capex_base=380,
       capex_high=520, heads=320,
       reuse="POX, COSORB, MeOH loop, AcOH plant; plus 5-8 regional hubs",
       killer="hub CAPEX and a farm-contracting business MSK does not have"),

 Route("R6","Point-source CO2 + electrolytic H2 (direct hydrogenation)","B","captured CO2",
       c_eff=0.93, feed_c_frac=0.0, feed_eur_t=(25,55,95),
       ext_h2_frac=1.0, h2_kwh_per_kg=52.0, aux_mwh_per_t=0.30,
       capex_low=250, capex_base=340, capex_high=470, heads=210, uses_asu=False,
       reuse="MeOH distillation, tankage, utilities; POX and ASU redundant",
       killer="CO2 hydrogenation needs 3 H2 per CO2, not 2: 189 kg H2/t methanol"),

 Route("R7","DAC CO2 + electrolytic H2 ('methanol from air')","C","direct air capture",
       c_eff=0.93, feed_c_frac=0.0, feed_eur_t=(280,420,600),
       ext_h2_frac=1.0, h2_kwh_per_kg=52.0, aux_mwh_per_t=0.30,
       capex_low=400, capex_base=600, capex_high=900, heads=230, uses_asu=False,
       reuse="MeOH distillation and tankage only",
       killer="DAC at USD 300-600/t CO2 is 15-40x the cost of point-source CO2"),

 Route("R8","SOEC co-electrolysis (CO2 + H2O -> syngas)","C","captured CO2 + water",
       c_eff=0.93, feed_c_frac=0.0, feed_eur_t=(25,55,95),
       ext_h2_frac=1.0, h2_kwh_per_kg=40.0, aux_mwh_per_t=0.25,
       capex_low=330, capex_base=460, capex_high=650, heads=210, uses_asu=False,
       reuse="MeOH loop and distillation",
       killer="SOEC stack life ~5 years; 4-5 stack replacements over plant life"),

 Route("R9","Biogas / biomethane dry reforming via existing POX","B","regional biogas",
       c_eff=0.80, feed_c_frac=0.60, feed_h_frac=0.16, feed_eur_t=(320,430,560),
       ext_h2_frac=0.0, aux_mwh_per_t=0.30, capex_low=140, capex_base=195,
       capex_high=270, heads=220,
       reuse="POX, COSORB, MeOH loop, AcOH plant",
       killer="aggregating 180+ MNm3/y of biomethane across three countries"),

 Route("R10","Petcoke + biomass char co-feed + H2 (hybrid)","B","petcoke + biochar",
       c_eff=0.89, feed_c_frac=0.82, feed_h_frac=0.037, feed_eur_t=(135,178,240),
       ext_h2_frac=1.0, aux_mwh_per_t=0.42, capex_low=255, capex_base=345,
       capex_high=470, heads=300,
       reuse="POX, COSORB, MeOH loop, AcOH plant",
       killer="two feed systems, two supply chains, one gasifier"),
]

# R1 natural gas is priced per GJ, handled specially
GAS_GJ_PER_T_MEOH = 38.0    # POX route, feed + fuel [ENG]


def run_gas(elec: float, eur_per_gj: float = None) -> Dict:
    rt = ROUTES[0]
    gj = eur_per_gj if eur_per_gj is not None else GAS_EUR_PER_GJ
    o = run(rt, elec)
    o["feed_t_per_t"] = None
    o["feed_cost"] = GAS_GJ_PER_T_MEOH * gj
    o["feed_eur_gj"] = gj
    o["cash"] = o["feed_cost"] + o["power_cost"] + o["maint"] + o["labour"] + o["other"]
    o["full"] = o["cash"] + o["capchg"]
    meoh_in = (M_MEOH / M_ACOH) / SEL_MEOH
    co_in = (M_CO / M_ACOH) / UTIL_CO
    o["acoh_marginal"] = meoh_in * o["cash"] + co_in * 0.55 * o["cash"] + 46.0
    o["acoh_full"] = meoh_in * o["full"] + co_in * 0.55 * o["cash"] + 74.0
    return o
