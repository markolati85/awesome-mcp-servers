# -*- coding: utf-8 -*-
"""
MSK Kikinda — methanol & acetic acid market / delivered-parity / netback model.

Core question: NOT "what is Rotterdam", but "what does imported product cost when
it physically arrives at a buyer in Budapest / Vienna / Bratislava / Zagreb /
northern Italy, and what FCA Kikinda netback can MSK take underneath it".

Tags: FACT (sourced) / EST (estimate) / PROXY (older datapoint extrapolated).
No number here is a quotation. Stdlib only.
"""
from dataclasses import dataclass
from typing import Dict, List

USD_EUR = 0.92          # EST, Sep 2026

# ---------------------------------------------------------------------------
# PRICE BENCHMARKS
# ---------------------------------------------------------------------------
# [FACT] Methanex European Posted Contract Price 2026 (GROSS, non-discounted):
#          Q1 EUR 535/t | Q2 EUR 850/t | Q3 EUR 915/t
# [FACT] Q2 2026 realised fixed at EUR 827/t FOB Rotterdam (~3% below posted).
# [FACT] Platts launched a monthly NET contract price (MTFRE03), EUR/mt FOB
#        Rotterdam, from 3 Nov 2025, averaging daily month-ahead FOB Rotterdam
#        spot assessments; and in May 2026 proposed to DISCONTINUE the
#        industry-settled European quarterly GROSS contract price.
#        -> the market itself is abandoning the posted benchmark.
MEOH_POSTED_2026 = dict(Q1=535.0, Q2=850.0, Q3=915.0)
MEOH_Q2_REALISED_FOB_ROT = 827.0

# [FACT] Acetic acid Europe: USD 0.61/kg Sep 2026 (~USD 610/t); USD 589/t Nov 2025.
ACOH_EUR_SEP26 = 610.0 * USD_EUR
ACOH_EUR_NOV25 = 589.0 * USD_EUR

# WHY PRICES ARE WHERE THEY ARE  [FACT]
# Europe imported ~6.3 Mt of methanol in 2025 (ex-Turkey): US 38%, Trinidad 25%,
# Middle East 4%. In 2026 the US-Iran war and the near-total closure of the
# Strait of Hormuz from late Feb cut tanker traffic 40-70%; Jan-May 2026 EU
# imports fell 76.4% from Saudi Arabia and 92.7% from Oman, and 14.2% / 8.6%
# from the US and Trinidad. The Q1->Q3 move from 535 to 915 is a WAR-DRIVEN
# SUPPLY SHOCK, not a structural repricing.
EU_MEOH_IMPORTS_MT = 6.3
EU_MEOH_SHARE = dict(US=0.38, Trinidad=0.25, MiddleEast=0.04, Other=0.33)

# PRICE SCENARIOS, FOB Rotterdam equivalent, 2026 real EUR/t   [EST]
# Built from: Q1 2026 pre-war 535; Nov-2025-era levels; the 5-year range; and
# the fact that ~63% of European supply is US/Trinidad gas-based.
MEOH_SCEN = {
    "Severe downcycle": 300.0,
    "Conservative":     380.0,
    "Base / mid-cycle": 450.0,
    "Strong market":    600.0,
    "Current Sep 2026 (war spike)": 830.0,
}
ACOH_SCEN = {
    "Severe downcycle": 400.0,
    "Conservative":     470.0,
    "Base / mid-cycle": 520.0,
    "Strong market":    580.0,
    "Current Sep 2026 (war spike)": 561.0,
}

# ---------------------------------------------------------------------------
# INLAND LOGISTICS  [EST — no published tariff; must be replaced by quotations]
# ---------------------------------------------------------------------------
# Chemical movements price as a fixed terminal/handling element plus a
# distance element. Rail tank car and inland barge bracket the range.
FIX_ARA = (22.0, 28.0)        # ARA terminal in/out, storage, survey, clearance
FIX_MSK = (12.0, 18.0)        # loading at MSK's own siding - no port, no terminal
VAR_LO, VAR_HI = 0.040, 0.065 # EUR/t-km, chemical tank car / barge blend


# Mediterranean / Adriatic import terminals (Trieste, Ravenna, Koper, Constanta,
# Thessaloniki) are the RELEVANT competitor route for the southern markets.
# Ignoring them overstates MSK's moat, so the model takes the CHEAPER of the two.
MED_PREMIUM = 10.0        # EST: Med CFR vs FOB Rotterdam
SWITCH_INCENTIVE = 15.0   # EST: EUR/t saving a buyer needs to change supplier


@dataclass
class Market:
    name: str
    km_from_ara: int          # ARA import terminal -> buyer
    km_from_msk: int          # Kikinda -> buyer
    size_kt: float            # EST addressable methanol demand, kt/y
    note: str = ""
    km_from_med: int = 0      # nearest Med/Adriatic terminal -> buyer (0 = n/a)


MARKETS = [
    Market("Serbia (domestic)",      1750,  130,  40, "home market, no border", 500),
    Market("Hungary (Budapest)",     1500,  250, 120, "Kronospan, MOL, resins", 500),
    Market("Croatia (Zagreb)",       1400,  400,  60, "wood panels, chemicals", 180),
    Market("Romania (west/Bucharest)",1900, 600, 110, "chemicals, resins", 230),
    Market("Slovenia (Ljubljana)",   1250,  530,  35, "wood panels, coatings", 110),
    Market("Austria (Vienna/Linz)",  1200,  450, 150, "large chemical demand", 500),
    Market("Slovakia (Bratislava)",  1250,  470,  70, "", 600),
    Market("Bulgaria (Sofia)",       2000,  500,  45, "", 380),
    Market("Czechia (Moravia)",      1100,  750,  90, "closer to ARA than to MSK", 700),
    Market("S. Poland (Katowice)",   1150,  750, 130, "closer to ARA", 900),
    Market("N. Italy (Milan/Veneto)",1100,  950, 220, "Med-supplied - moat is thin", 300),
    Market("Greece (Thessaloniki)",  2300,  700,  35, "own port - no moat", 50),
]


def freight(km: int, fixed: tuple, lo=VAR_LO, hi=VAR_HI) -> tuple:
    return (fixed[0] + km * lo, fixed[1] + km * hi)


def mid(t): return (t[0] + t[1]) / 2.0


def parity(m: Market, rotterdam: float) -> Dict:
    """Delivered parity and the FCA Kikinda netback it implies.

    The competitor benchmark is the CHEAPER of an ARA import and a
    Mediterranean/Adriatic import. Using ARA alone overstates MSK's advantage in
    the southern markets, where Trieste, Koper, Constanta and Thessaloniki are
    far closer than Rotterdam.
    """
    f_ara = freight(m.km_from_ara, FIX_ARA)
    f_msk = freight(m.km_from_msk, FIX_MSK)
    via_ara = rotterdam + mid(f_ara)
    if m.km_from_med:
        f_med = freight(m.km_from_med, FIX_ARA)
        via_med = rotterdam + MED_PREMIUM + mid(f_med)
        comp_del = min(via_ara, via_med)
        route = "Med" if via_med < via_ara else "ARA"
    else:
        comp_del = via_ara
        route = "ARA"
    msk_frt = mid(f_msk)
    # MSK must give the buyer a visible reason to switch supplier. Procurement
    # responds to an absolute saving, not a percentage, so a flat EUR 15/t is
    # used [EST]. A percentage would wrongly inflate the incentive at high prices.
    switch = SWITCH_INCENTIVE
    msk_del = comp_del - switch
    fca = msk_del - msk_frt
    return dict(market=m.name, size=m.size_kt, route=route,
                ara_frt=comp_del - rotterdam, msk_frt=msk_frt,
                comp_delivered=comp_del, msk_delivered=msk_del,
                fca_netback=fca, moat=fca - rotterdam,
                km_ara=m.km_from_ara, km_msk=m.km_from_msk, note=m.note)


def all_markets(rotterdam: float) -> List[Dict]:
    return [parity(m, rotterdam) for m in MARKETS]


def weighted_netback(rotterdam: float, take_share=0.35) -> Dict:
    """Volume-weighted achievable FCA netback across markets where MSK has a moat."""
    rows = [r for r in all_markets(rotterdam) if r["moat"] > 0]
    rows.sort(key=lambda r: -r["moat"])
    vol = 0.0
    wsum = 0.0
    picked = []
    for r in rows:
        v = r["size"] * take_share
        if vol + v > 150.0:
            v = max(0.0, 150.0 - vol)
        if v <= 0:
            break
        vol += v
        wsum += v * r["fca_netback"]
        picked.append((r["market"], v, r["fca_netback"], r["moat"]))
    return dict(volume_kt=vol, netback=wsum / vol if vol else 0.0, picked=picked)


# ---------------------------------------------------------------------------
# PROFITABILITY
# ---------------------------------------------------------------------------
MERCH_MEOH = 150_000.0
MERCH_ACOH = 50_000.0
# MSK cash costs from the syngas study (petcoke at EUR 105/t delivered).
# Treated here as SCENARIO INPUTS to be challenged, not as fact.
MEOH_COST_CASES = [280, 300, 320, 340, 360, 400]
ACOH_COST_CASES = [330, 350, 370, 400, 430, 470]
MEOH_COST_BASE = 312.0
ACOH_COST_BASE = 336.0


def contribution(meoh_px, acoh_px, meoh_cost=MEOH_COST_BASE, acoh_cost=ACOH_COST_BASE,
                 commercial_eur_t=14.0):
    m = (meoh_px - meoh_cost - commercial_eur_t) * MERCH_MEOH / 1e6
    a = (acoh_px - acoh_cost - commercial_eur_t) * MERCH_ACOH / 1e6
    return dict(meoh=m, acoh=a, total=m + a)


def breakeven_rotterdam(meoh_cost=MEOH_COST_BASE, take_share=0.35) -> float:
    """Rotterdam price at which MSK's weighted netback equals its cash cost."""
    lo, hi = 100.0, 900.0
    for _ in range(80):
        mid_ = (lo + hi) / 2
        if weighted_netback(mid_, take_share)["netback"] < meoh_cost:
            lo = mid_
        else:
            hi = mid_
    return (lo + hi) / 2
