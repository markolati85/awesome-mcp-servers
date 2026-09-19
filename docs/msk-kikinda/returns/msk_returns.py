#!/usr/bin/env python3
"""
MSK Kikinda - Part 6: FULL-OWNERSHIP RETURNS
Petcoke via PORT OF BAR. Methanol EUR 450-500/t. No BOO, no tolling.

Owner's decision, recorded: MSK/SPV owns all equipment. No long-term binding
syngas offtake, so that feedstock can be switched to natural gas (or anything
else) whenever that becomes cheaper. Everything below is built on that basis.

Slate (Part 3): 150,000 t/y merchant methanol + 50,000 t/y acetic acid,
177,085 t/y total methanol-equivalent, 24,810 t/y CO for the AcOH unit.

Tags: [FACT] published/attributable  [EST] engineering estimate
      [ASSUM] chosen assumption  [RFQ] must be bid, cannot be estimated

Stdlib only.  python3 msk_returns.py
"""

# ===========================================================================
# 0. PHYSICAL BASIS  (Part 3, cross-checked in Part 5 against carbon balance)
# ===========================================================================
MERCHANT_MEOH = 150_000.0
ACOH          =  50_000.0
TOTAL_MEOH    = 177_085.0      # incl. 27,085 t consumed making AcOH
PETCOKE_AR    = 270_000.0      # t/y as-received, 8% moisture
PETCOKE_DRY   = 248_000.0
OP_HOURS      = 8_000.0

# carbon balance -> vented CO2  [EST]
C_IN      = PETCOKE_DRY * 0.867
C_PRODUCT = TOTAL_MEOH * 0.3748 + 24_810 * (12/28)
CO2_VENT  = (C_IN - C_PRODUCT) * 44/12

USD_EUR = 0.92   # [ASSUM]

# ===========================================================================
# 1. PETCOKE DELIVERED, US GULF -> PORT OF BAR -> RAIL -> KIKINDA
#
# Route as instructed by the owner. Sea leg to Bar is ~700-900 nm SHORTER
# than to Constanta (no Dardanelles/Black Sea). The inland leg is the
# problem: Bar-Belgrade is a mountain line (grades, tunnels, axle-load and
# capacity limits), so its per-tonne-km cost is well above a flat unit train.
# ===========================================================================
RAIL_BAR_KIKINDA_KM = 600.0    # [EST] Bar-Belgrade ~450 + Belgrade-Kikinda ~130

class Route:
    def __init__(self, name, fob_usd, sea_usd, port_eur, rail_eur_tkm, km):
        self.name, self.fob_usd, self.sea_usd = name, fob_usd, sea_usd
        self.port_eur, self.rail_eur_tkm, self.km = port_eur, rail_eur_tkm, km
    @property
    def fob(self):  return self.fob_usd * USD_EUR
    @property
    def sea(self):  return self.sea_usd * USD_EUR
    @property
    def rail(self): return self.rail_eur_tkm * self.km
    @property
    def delivered(self): return self.fob + self.sea + self.port_eur + self.rail

# FOB [EST]: high-sulfur, high-metal, low-HGI fuel-grade petcoke. A gasifier
# with AGR+SRU is indifferent to sulphur and slurry-grinds anyway, so MSK buys
# the DISCOUNTED grade, not the benchmark grade.  Benchmark Q3 2026 was
# USD 65.49/t; the discounted grade sits under it.   [RFQ - term contract]
BAR = {
 "low":  Route("Bar - low",  52.0, 20.0, 4.0, 0.045, RAIL_BAR_KIKINDA_KM),
 "base": Route("Bar - base", 60.0, 26.0, 5.5, 0.052, RAIL_BAR_KIKINDA_KM),
 "high": Route("Bar - high", 75.0, 34.0, 7.0, 0.060, RAIL_BAR_KIKINDA_KM),
}
# Reference only - the owner has chosen Bar. Constanta + Danube/Tisa barge:
CONSTANTA_BASE = Route("Constanta+barge", 60.0, 30.0, 6.0, 0.021, 1_100.0)

# ===========================================================================
# 2. CAPEX  (Part 5, revised up after the China red-team)
# ===========================================================================
INSTALLED   = 235.0   # [EST] EUR m, 1x100% quench train, max brownfield reuse,
                      #       Chinese package + Serbian erection, incl. CE/PED
                      #       compliance premium and AACE Class-4 contingency
IDC         = 22.0
WORKING_CAP = 26.0
FUNDING     = INSTALLED + IDC + WORKING_CAP     # = 283

ISLAND_SHARE = 0.60   # [EST] share of installed cost that is the syngas island

# ===========================================================================
# 3. OPEX, BUILT BOTTOM-UP  (the EUR 98/t island figure in Part 3 was never
#    built up and does not survive a check against the power bill)
# ===========================================================================
POWER_MW_LOAD   = 32.0    # [EST] ASU + O2 boost + syngas/CO compression + mills
TURBINE_MW = {"quench": 6.0, "whb": 13.5}   # [EST] 55GT01 off process steam
POWER_EUR_MWH   = 85.0    # [ASSUM] large Serbian industrial consumer
WHB_EXTRA_CAPEX = 18.0    # [EST] EUR m to get the turbine to full output

MAINT_PCT   = 0.030       # [EST] of installed capex
INSURANCE   = 0.005       # [EST] of installed capex
HEADCOUNT   = 450         # [EST]
LABOUR_EUR  = 14_500.0    # [EST] fully loaded, RSD 80-90k/month + contributions
CATALYST_M  = 7.0         # [EST] MeOH + shift + AGR solvent + Claus + Cativa Ir
WATER_M     = 1.5         # [EST] demin, cooling, wastewater treatment
SLAG_M      = 0.5         # [EST] filter cake disposal (V/Ni recovery may offset)
SGA_M       = 4.0         # [EST]

SULFUR_KT   = 14.5        # [EST] t/y elemental sulphur from Claus
SULFUR_EUR  = 100.0       # [ASSUM] volatile; EUR 50-150/t

def opex(delivered_petcoke, steam_case="quench"):
    net_mw   = POWER_MW_LOAD - TURBINE_MW[steam_case]
    power_m  = net_mw * OP_HOURS * POWER_EUR_MWH / 1e6
    capex    = INSTALLED + (WHB_EXTRA_CAPEX if steam_case == "whb" else 0.0)
    return {
        "feedstock": PETCOKE_AR * delivered_petcoke / 1e6,
        "power":     power_m,
        "maint":     capex * MAINT_PCT,
        "labour":    HEADCOUNT * LABOUR_EUR / 1e6,
        "catalyst":  CATALYST_M,
        "water":     WATER_M,
        "slag":      SLAG_M,
        "insurance": capex * INSURANCE,
        "sga":       SGA_M,
        "sulfur_credit": -SULFUR_KT * 1000 * SULFUR_EUR / 1e6,
    }, capex, net_mw

def revenue(meoh_eur, acoh_eur):
    return MERCHANT_MEOH*meoh_eur/1e6 + ACOH*acoh_eur/1e6

def annuity(r, n=15):
    return r*(1+r)**n/((1+r)**n - 1)

# ===========================================================================
def main():
    w = 78
    print("=" * w)
    print("PART 6 - FULL OWNERSHIP, PETCOKE VIA PORT OF BAR".center(w))
    print("=" * w)

    print("\n1. PETCOKE DELIVERED KIKINDA VIA BAR  (EUR/t)")
    print(f"   {'':<10}{'FOB':>8}{'sea':>8}{'port':>8}{'rail':>8}{'DELIVERED':>11}")
    for k, r in BAR.items():
        print(f"   {k:<10}{r.fob:>8.1f}{r.sea:>8.1f}{r.port_eur:>8.1f}"
              f"{r.rail:>8.1f}{r.delivered:>11.1f}")
    c = CONSTANTA_BASE
    print(f"   {'[ref] Constanta + Danube/Tisa barge, base':<52}{c.delivered:>11.1f}")
    print(f"   -> Bar's shorter sea leg is given back on the mountain railway:")
    print(f"      rail Bar EUR {BAR['base'].rail:.0f}/t vs barge EUR {c.rail:.0f}/t."
          f"  Bar costs EUR {BAR['base'].delivered-c.delivered:+.0f}/t more.")
    print(f"      Volume check: {PETCOKE_AR/1000:.0f} kt/y = ~{PETCOKE_AR/52/1500:.1f} "
          f"trains/week of 1,500 t on the Bar-Belgrade line.  [capacity: RFQ]")

    print("\n2. CAPEX AND FUNDING  (EUR m)")
    print(f"   installed {INSTALLED:.0f} + IDC {IDC:.0f} + working capital "
          f"{WORKING_CAP:.0f} = FUNDING NEED {FUNDING:.0f}")

    print("\n3. OPEX BUILT BOTTOM-UP, base petcoke, quench case  (EUR m/y)")
    ox, cap, netmw = opex(BAR["base"].delivered, "quench")
    for k, v in ox.items():
        print(f"   {k:<18}{v:>9.1f}   ({v*1e6/TOTAL_MEOH:>6.1f} EUR/t MeOH-eq)")
    tot = sum(ox.values())
    print(f"   {'TOTAL':<18}{tot:>9.1f}   ({tot*1e6/TOTAL_MEOH:>6.1f} EUR/t MeOH-eq)")
    print(f"   net power import {netmw:.1f} MW = "
          f"{netmw*OP_HOURS/1000:.0f} GWh/y  <- single biggest opex line")

    print("\n4. EBITDA AND PAYBACK  (EUR m/y; payback = funding / EBITDA)")
    for steam in ("quench", "whb"):
        ox, cap, netmw = opex(BAR["base"].delivered, steam)
        fund = cap + IDC + WORKING_CAP
        tot  = sum(ox.values())
        print(f"\n   --- {steam.upper()} case: installed {cap:.0f}, funding {fund:.0f},"
              f" net import {netmw:.0f} MW ---")
        print(f"   {'MeOH':>6}{'AcOH':>7}{'revenue':>10}{'opex':>8}"
              f"{'EBITDA':>9}{'margin':>8}{'payback':>9}")
        for meoh in (450.0, 475.0, 500.0):
            for acoh in (500.0, 550.0, 620.0):
                rev = revenue(meoh, acoh)
                eb  = rev - tot
                pb  = fund/eb if eb > 0 else float("inf")
                pbs = f"{pb:.1f}y" if eb > 0 else "never"
                print(f"   {meoh:>6.0f}{acoh:>7.0f}{rev:>10.1f}{tot:>8.1f}"
                      f"{eb:>9.1f}{eb/rev:>8.1%}{pbs:>9}")

    print("\n5. FEEDSTOCK-PRICE SENSITIVITY (MeOH 475, AcOH 550, quench)")
    print(f"   {'petcoke':<10}{'delivered':>11}{'EBITDA':>9}{'payback':>9}")
    for k, r in BAR.items():
        ox, cap, _ = opex(r.delivered, "quench")
        eb = revenue(475.0, 550.0) - sum(ox.values())
        fund = cap + IDC + WORKING_CAP
        print(f"   {k:<10}{r.delivered:>11.1f}{eb:>9.1f}"
              f"{fund/eb if eb>0 else 0:>8.1f}y")

    print("\n6. DEBT SERVICE CHECK (Part 1 discipline, not just payback)")
    ox, cap, _ = opex(BAR["base"].delivered, "quench")
    fund = cap + IDC + WORKING_CAP
    for meoh, acoh in ((450.0, 500.0), (475.0, 550.0), (500.0, 620.0)):
        eb = revenue(meoh, acoh) - sum(ox.values())
        for senior_pct in (0.55, 0.65):
            debt = fund * senior_pct
            ds   = debt * annuity(0.075, 15)
            print(f"   MeOH {meoh:.0f} AcOH {acoh:.0f} | senior {senior_pct:.0%} "
                  f"= {debt:.0f}m, service {ds:.1f}m/y, EBITDA {eb:.1f}m "
                  f"-> DSCR {eb/ds:.2f}"
                  f"{'  <-- FAILS' if eb/ds < 1.30 else ''}")

    print("\n7. THE RISK THAT DWARFS EVERYTHING ELSE: CO2")
    print(f"   Vented CO2: {CO2_VENT/1000:,.0f} kt/y  [EST from carbon balance]")
    print(f"   = {CO2_VENT/(MERCHANT_MEOH+ACOH):.2f} t CO2 per t of product sold")
    print( "   (European methanol from natural gas is ~0.7-0.9 t/t)")
    print(f"   Today Serbia charges EUR 0/t on this: its EUR 4/t tax from")
    print( "   1 Jan 2026 covers cement, fertilizers, iron & steel, aluminium")
    print( "   and electricity - NOT methanol or acetic acid. CBAM does not")
    print( "   cover them either.  [FACT]")
    ox, cap, _ = opex(BAR["base"].delivered, "quench")
    eb_base = revenue(475.0, 550.0) - sum(ox.values())
    print(f"   {'CO2 price':<12}{'cost':>10}{'EBITDA':>10}{'payback':>10}")
    for p in (0.0, 4.0, 30.0, 60.0, 86.0):
        cost = CO2_VENT * p / 1e6
        eb = eb_base - cost
        pb = f"{(cap+IDC+WORKING_CAP)/eb:.1f}y" if eb > 0 else "never"
        print(f"   EUR {p:>5.0f}/t{cost:>10.1f}{eb:>10.1f}{pb:>10}")
    be = eb_base*1e6/CO2_VENT
    print(f"   EBITDA reaches zero at EUR {be:.0f}/t CO2.")
    print( "   Serbia is on an EU accession path and will adopt an ETS.")
    print( "   This is a change-in-law question, not an engineering one.")
    print("=" * w)

if __name__ == "__main__":
    main()
