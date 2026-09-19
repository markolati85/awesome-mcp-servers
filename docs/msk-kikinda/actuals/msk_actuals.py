#!/usr/bin/env python3
"""
MSK Kikinda - Part 7: REBUILT ON THE PLANT'S OWN NUMBERS.

Source: "Projekcija za 2026 23.04.2024.xlsx", sent by Mirko Latinovic,
acting General Manager of MSK a.d. Kikinda, 23.04.2024, and the covering
e-mail "Prirodni gas" of 09.04.2024.  [FACT - operator's own document]

Everything earlier in this study used an assumed slate of 150 kt merchant
methanol + 50 kt acetic acid. The plant's own projection says otherwise, and
the differences are large enough to change conclusions. This part rebuilds
on the operator's figures.

Tags: [FACT-MSK] from the operator's own projection
      [FACT] other published/attributable
      [EST] engineering estimate   [ASSUM] chosen assumption   [RFQ] must be bid
"""

# ===========================================================================
# 1. WHAT THE PLANT ACTUALLY IS                          [ALL FACT-MSK]
# ===========================================================================
NAMEPLATE_MEOH   = 200_000.0   # t/y over 330 operating days
NAMEPLATE_ACOH   = 100_000.0   # t/y over 330 operating days
UTIL_MEOH, UTIL_ACOH = 0.93, 0.92

MEOH_TOTAL    = 186_390.0      # t/y produced
MEOH_OWN_USE  =  49_864.0      # t/y consumed making acetic acid
MEOH_SALE     = 136_526.0      # t/y sold
ACOH          =  92_340.0      # t/y
MEOH_PER_ACOH = 0.54           # operator's own stated ratio

GAS_KM3       = 301_952.0      # thousand m3/y  (= 302 million m3/y)
GAS_EUR_KM3   = 470.20         # EUR per 1,000 m3 in the projection
GAS_USD_KM3   = 501.0

# Full-year P&L in the projection
REVENUE       = 105_311_883.0
OPEX_TOTAL    = 177_437_060.0
RESULT        = -72_125_178.0

# The operator's own decomposition (ties out exactly):
GAS_COST      = 141_978_286.0  # = GAS_KM3 * GAS_EUR_KM3
DEPRECIATION  =   2_055_968.0
CASH_OPEX_EX_GAS = 33_402_806.0

# The operator's own break-even gas prices
BE_LIQUIDITY_USD  = 253.74     # cash break-even
BE_PROFIT_USD     = 246.48     # profitability

# Product prices used in the projection (IHS forecast basis for 2026)
MEOH_PROJ = 341.23             # EUR/t gross
ACOH_PROJ = 629.27             # EUR/t gross
FREIGHT_MEOH = 25.0            # EUR/t export freight  [FACT-MSK]
FREIGHT_ACOH = 80.0            # EUR/t export freight  [FACT-MSK]

# Acetic acid catalyst: RHODIUM + iodide promoter -> this is the MONSANTO
# process, not Cativa/iridium. Earlier parts of this study said Cativa. Wrong.
RH_G_PER_T   = 1.163           # g rhodium per t acetic acid  [FACT-MSK]
RH_EUR_PER_G = 7.444           # EUR/g  [FACT-MSK]
I2_G_PER_T   = 80.337          # g iodine per t acetic acid   [FACT-MSK]

# ===========================================================================
# 2. PETCOKE CASE REBUILT ON THE REAL SLATE
# ===========================================================================
C_MEOH, C_CO = 0.3748, 12/28
CARBON_EFF   = 0.358           # [EST] entrained-flow petcoke, from Part 5
PETCOKE_C    = 0.867
MOISTURE     = 0.08

CO_FOR_ACOH  = ACOH * (28/60.05) / 0.94
C_NEEDED     = MEOH_TOTAL*C_MEOH + CO_FOR_ACOH*C_CO
PETCOKE_DRY  = C_NEEDED / CARBON_EFF / PETCOKE_C
PETCOKE_AR   = PETCOKE_DRY / (1-MOISTURE)
CO2_VENT     = (PETCOKE_DRY*PETCOKE_C - C_NEEDED) * 44/12

# Delivered petcoke via Port of Bar (Part 6)
PETCOKE_DELIVERED = {"low": 97.2, "base": 115.8, "high": 143.3}

# Capex (Part 5, after the China red-team)
INSTALLED_BASE = 235.0
IDC, WORKING_CAP = 22.0, 26.0

# --- The power question, which is what the 15 MW turbine is about ----------
# TODAY: the plant buys only EUR 540,000/y of electricity, because the
# existing steam turbine covers the load off gas-fired process steam.
# [FACT-MSK]  That self-sufficiency is an ASSET, and it is the single biggest
# thing earlier parts of this study got wrong (Part 6 assumed EUR 17.7m/y of
# imported power).
#
# On petcoke the steam must come from gasifier waste heat instead. That makes
# the waste-heat boiler MANDATORY, not optional - the opposite of the China
# red-team's "quench, skip the RSC" advice.
GROSS_LOAD_MW = 36.0           # [EST] existing plant + ASU + compression
TURBINE_MW    = 15.0           # [FACT-MSK/owner] existing unit, refurbished
POWER_EUR_MWH = 85.0           # [ASSUM]
HOURS         = 7_920.0        # [FACT-MSK] 330 days

STEAM_CASES = {
    #  name            : (turbine MW, extra capex EUR m)
    "quench (no WHB)"   : (4.0,  0.0),
    "existing turbine"  : (15.0, 20.0),   # WHB sized to feed the 15 MW unit
    "turbine uprated"   : (26.0, 42.0),   # WHB + larger/uprated turbine
    "full self-suff."   : (36.0, 62.0),
}

# Incremental cash opex of the gasification island, over and above the
# EUR 33.4m the plant already spends ex-gas.  [EST]
ISLAND_MAINT_PCT = 0.030
ISLAND_LABOUR    = 2.2         # EUR m/y, added operators for the island
ISLAND_CHEM      = 3.5         # EUR m/y, AGR solvent, shift/Claus catalyst
ISLAND_SLAG      = 0.6         # EUR m/y
SULFUR_KT, SULFUR_EUR = 18.0, 100.0   # [EST] scales with the bigger feed

def annuity(r, n=15):
    return r*(1+r)**n/((1+r)**n-1)

def petcoke_case(meoh_eur, acoh_eur, feed_key="base", steam="existing turbine"):
    tmw, extra = STEAM_CASES[steam]
    installed  = INSTALLED_BASE + extra
    funding    = installed + IDC + WORKING_CAP
    net_mw     = max(GROSS_LOAD_MW - tmw, 0.0)

    rev = MEOH_SALE*meoh_eur + ACOH*acoh_eur
    feed = PETCOKE_AR * PETCOKE_DELIVERED[feed_key]
    power = net_mw * HOURS * POWER_EUR_MWH
    island = (installed*ISLAND_MAINT_PCT + ISLAND_LABOUR + ISLAND_CHEM
              + ISLAND_SLAG)*1e6
    sulfur = -SULFUR_KT*1000*SULFUR_EUR
    opex = CASH_OPEX_EX_GAS + feed + power + island + sulfur
    eb = rev - opex
    return dict(rev=rev, feed=feed, power=power, island=island, opex=opex,
                ebitda=eb, funding=funding, installed=installed,
                net_mw=net_mw, payback=funding*1e6/eb if eb > 0 else None)

# ===========================================================================
def main():
    w = 80
    print("="*w); print("PART 7 - REBUILT ON MSK'S OWN PROJECTION".center(w)); print("="*w)

    print("\n1. WHAT THE PLANT ACTUALLY IS   [FACT-MSK]")
    print(f"   Nameplate          {NAMEPLATE_MEOH:>10,.0f} t/y methanol  "
          f"{NAMEPLATE_ACOH:>9,.0f} t/y acetic acid  (330 days)")
    print(f"   Utilisation        {UTIL_MEOH:>10.0%}              {UTIL_ACOH:>9.0%}")
    print(f"   Methanol produced  {MEOH_TOTAL:>10,.0f} t/y")
    print(f"     of which own use {MEOH_OWN_USE:>10,.0f} t/y  ({MEOH_PER_ACOH} t per t AcOH)")
    print(f"     of which sold    {MEOH_SALE:>10,.0f} t/y")
    print(f"   Acetic acid        {ACOH:>10,.0f} t/y")
    print(f"   Natural gas        {GAS_KM3*1000:>10,.0f} m3/y  "
          f"= {GAS_KM3*1000/MEOH_TOTAL:,.0f} m3 per t methanol")
    print(f"\n   *** This study had been assuming 150,000 t methanol + 50,000 t AcOH.")
    print(f"   *** Acetic acid is actually {ACOH/50_000-1:+.0%} - it is the high-value product.")

    print("\n2. WHY IT IS SHUT   [FACT-MSK]")
    print(f"   Revenue          {REVENUE:>15,.0f}")
    print(f"   Operating costs  {OPEX_TOTAL:>15,.0f}")
    print(f"   RESULT           {RESULT:>15,.0f}")
    print(f"   of which gas     {GAS_COST:>15,.0f}   "
          f"= {GAS_COST/OPEX_TOTAL:.0%} of ALL operating cost")
    print(f"   cash opex ex-gas {CASH_OPEX_EX_GAS:>15,.0f}")
    print(f"   depreciation     {DEPRECIATION:>15,.0f}")
    print(f"   (ties out exactly: {GAS_COST+CASH_OPEX_EX_GAS+DEPRECIATION:,.0f})")
    print(f"\n   Operator's own break-even gas price:")
    print(f"     liquidity      USD {BE_LIQUIDITY_USD:.2f}/1000 m3")
    print(f"     profitability  USD {BE_PROFIT_USD:.2f}/1000 m3")
    print(f"     projected      USD {GAS_USD_KM3:.2f}/1000 m3"
          f"  -> needs gas at {BE_LIQUIDITY_USD/GAS_USD_KM3-1:+.0%}")
    print( "   The thesis that gas is why this plant does not run is now")
    print( "   arithmetic, not opinion.")

    print("\n3. THE ELECTRICITY FINDING  -  THE 15 MW TURBINE")
    print(f"   The plant buys only EUR 540,000/y of electricity [FACT-MSK]:")
    print(f"   the existing steam turbine covers the load off process steam.")
    print(f"   Part 6 of this study assumed EUR 17.7m/y of imported power.")
    print(f"   That was the single biggest error in it.")
    print(f"\n   On petcoke the steam must come from gasifier waste heat, so the")
    print(f"   waste-heat boiler becomes MANDATORY - the opposite of the China")
    print(f"   red-team's 'quench, skip the RSC' recommendation.")

    print("\n4. PETCOKE REQUIREMENT ON THE REAL SLATE")
    print(f"   CO for acetic acid      {CO_FOR_ACOH:>10,.0f} t/y")
    print(f"   carbon into product     {C_NEEDED:>10,.0f} t/y")
    print(f"   petcoke as received     {PETCOKE_AR:>10,.0f} t/y  "
          f"(Part 6 assumed 270,000)")
    print(f"   vented CO2              {CO2_VENT:>10,.0f} t/y  "
          f"= {CO2_VENT/(MEOH_SALE+ACOH):.2f} t per t sold")

    print("\n5. EBITDA AND PAYBACK, REAL SLATE, PETCOKE VIA BAR")
    print("   (base petcoke EUR 115.8/t delivered)")
    for steam in STEAM_CASES:
        r0 = petcoke_case(475., 600., "base", steam)
        print(f"\n   --- {steam}: turbine {STEAM_CASES[steam][0]:.0f} MW, "
              f"net import {r0['net_mw']:.0f} MW, installed "
              f"{r0['installed']:.0f}, funding {r0['funding']:.0f} ---")
        print(f"   {'MeOH':>6}{'AcOH':>7}{'revenue':>11}{'opex':>11}"
              f"{'EBITDA':>11}{'payback':>10}")
        for meoh in (450., 500.):
            for acoh in (550., 600., 630.):
                r = petcoke_case(meoh, acoh, "base", steam)
                pb = f"{r['payback']:.1f}y" if r['payback'] else "never"
                print(f"   {meoh:>6.0f}{acoh:>7.0f}{r['rev']/1e6:>11.1f}"
                      f"{r['opex']/1e6:>11.1f}{r['ebitda']/1e6:>11.1f}{pb:>10}")

    print("\n6. FEEDSTOCK SENSITIVITY (MeOH 475, AcOH 600, existing turbine)")
    for k in PETCOKE_DELIVERED:
        r = petcoke_case(475., 600., k, "existing turbine")
        pb = f"{r['payback']:.1f}y" if r['payback'] else "never"
        print(f"   petcoke {k:<6} EUR {PETCOKE_DELIVERED[k]:>6.1f}/t  "
              f"feed cost {r['feed']/1e6:>6.1f}m  EBITDA {r['ebitda']/1e6:>6.1f}m  {pb}")

    print("\n7. THE COMPARISON THAT MATTERS: PETCOKE vs STAYING ON GAS")
    r = petcoke_case(475., 600., "base", "existing turbine")
    gas_rev = MEOH_SALE*475. + ACOH*600.
    print(f"   {'':<28}{'gas today':>14}{'petcoke':>14}")
    print(f"   {'revenue (same prices)':<28}{gas_rev/1e6:>14.1f}{r['rev']/1e6:>14.1f}")
    print(f"   {'feedstock':<28}{GAS_COST/1e6:>14.1f}{r['feed']/1e6:>14.1f}")
    print(f"   {'other cash opex':<28}"
          f"{CASH_OPEX_EX_GAS/1e6:>14.1f}{(r['opex']-r['feed'])/1e6:>14.1f}")
    gas_eb = gas_rev - GAS_COST - CASH_OPEX_EX_GAS
    print(f"   {'EBITDA':<28}{gas_eb/1e6:>14.1f}{r['ebitda']/1e6:>14.1f}")
    print(f"\n   Feedstock bill falls from EUR {GAS_COST/1e6:.0f}m to "
          f"EUR {r['feed']/1e6:.0f}m - a EUR {(GAS_COST-r['feed'])/1e6:.0f}m/y swing.")
    print( "   THAT is the investment case. Not the price of methanol.")

    print("\n8. CORRECTION: THE ACETIC ACID CATALYST")
    rh_kg = RH_G_PER_T*ACOH/1000
    print(f"   The projection lists rhodium {RH_G_PER_T} g/t at EUR {RH_EUR_PER_G}/g")
    print(f"   plus iodide promoter {I2_G_PER_T} g/t -> this is the MONSANTO")
    print(f"   process, NOT Cativa/iridium as stated earlier in this study.")
    print(f"   Rhodium make-up {rh_kg:.0f} kg/y = EUR {rh_kg*RH_EUR_PER_G*1000/1e6:.2f}m/y;")
    print(f"   the reactor INVENTORY is a separate working-capital item.  [RFQ]")
    print("="*w)

if __name__ == "__main__":
    main()
