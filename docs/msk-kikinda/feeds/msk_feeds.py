#!/usr/bin/env python3
"""
MSK Kikinda - Part 11: which feedstock is actually cheapest, September 2026.

Question put by the owner: what is the cheapest feedstock in the world for this
plant, with maximum reuse of the existing equipment and the 15 MW steam turbine,
that can be landed at Port of Bar and railed to Kikinda?

This part exists because Parts 3-10 never priced the one route that reuses the
most equipment: HEAVY LIQUID RESIDUE through the existing POX with a
conventional shift.  Part 3 modelled liquid residue only with electrolytic
hydrogen (route R4), which loaded it with 5.9 MWh/t of electrolysis and buried
it.  MSK's U-13 is natively a liquid-feed partial-oxidation gasifier, so that
was the wrong comparison to make.

It also re-prices everything at September 2026 levels.  Between the last part
and this one the US-Iran war roughly tripled European gas and pulled fuel oil
and coal up with it.  That changes the ranking, and it changes it in the
project's favour - for the wrong reason.

Basis of comparison: carbon, not tonnage and not energy.  The plant is a carbon
converter.  Every route must deliver the same carbon into the same product
slate that the operator's own 2026 projection describes.

  python3 msk_feeds.py            full comparison
  python3 msk_feeds.py switch     the gas-vs-petcoke switching price
  python3 msk_feeds.py volume     can you actually buy the tonnage?

Tags:  [FACT]  published/observed         [FACT-MSK] operator's own document
       [ENG]   engineering estimate       [ASSUM]   model assumption
       [RFQ]   requires a vendor quote    [LIST]    a listing, not a trade
"""
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional
import sys

# ===========================================================================
# 1. THE PRODUCT SLATE - from the operator's own 2026 projection  [FACT-MSK]
# ===========================================================================
MEOH_TOTAL = 186_390.0        # t/y methanol produced
MEOH_SALE  = 136_526.0        # t/y sold
ACOH       =  92_340.0        # t/y acetic acid
HOURS      =   7_920.0        # 330 days

# Carbon that must end up in product
C_MEOH      = 12/32.04
C_CO        = 12/28.01
CO_FOR_ACOH = ACOH * (28.01/60.05) / 0.94          # 94% CO selectivity [ENG]
C_NEEDED    = MEOH_TOTAL*C_MEOH + CO_FOR_ACOH*C_CO # t carbon/y into product

# Methanol-equivalent tonnes, used only to express costs per tonne of output
MEOH_EQ = MEOH_TOTAL + CO_FOR_ACOH

FX = 501.0/470.20             # USD per EUR, the rate implicit in the
                              # operator's own projection  [FACT-MSK]

# ===========================================================================
# 2. CARBON EFFICIENCY
# ===========================================================================
# Natural gas: MEASURED from the operator's projection, not assumed.
# 301,952,000 m3/y at 0.716 kg/m3 and 74.9% carbon by mass.
GAS_M3        = 301_952_000.0        # [FACT-MSK]
GAS_DENSITY   = 0.716                # kg/m3   [ENG]
GAS_C_FRAC    = 0.749                # CH4 carbon fraction
GAS_LHV_M3    = 0.0358               # GJ/m3   [ENG]
GAS_C_IN      = GAS_M3*GAS_DENSITY/1000.0*GAS_C_FRAC
GAS_C_EFF     = C_NEEDED/GAS_C_IN    # -> ~0.545, and it is a measurement

# Gasification, acid-rich slate: Part 9 corrected this to 41-46%.  Parts 5-7
# used 35.8%, carried over from a methanol-only coal case.  Acetic acid CO is
# never shifted, so an acid-rich slate runs 5-8 points above methanol-only.
GASIF_C_EFF   = 0.435                # [ENG] Part 9 mid-range
GASIF_C_EFF_LO, GASIF_C_EFF_HI = 0.41, 0.46

# ===========================================================================
# 3. COSTS THE PLANT CARRIES WHATEVER IT BURNS
# ===========================================================================
CASH_OPEX_EX_GAS = 33_402_806.0      # [FACT-MSK] labour, catalyst, maint, etc.
GROSS_LOAD_MW    = 36.0              # [ENG] plant + ASU + syngas compression
TURBINE_MW       = 15.0              # [FACT-MSK/owner] existing unit NAMEPLATE
# ...but nameplate is not output.  Part 9 caps recoverable HP steam at
# 60-75 t/h.  Let down to the process header at ~420 kJ/kg that is 7.0-8.8 MW
# of back-pressure work; a condensing tail on the surplus adds ~2-3 MW.  So
# the machine runs at roughly two thirds of its plate.  Earlier drafts of this
# part credited the full 15 MW - that was wrong and flattered the project by
# about EUR 6m/y.
TURBINE_OUTPUT_MW = 10.0             # [ENG] bounded by the Part 9 steam ceiling
POWER_EUR_MWH    = 160.0             # [FACT-anchored] Serbia SEEPEX baseload
                                     # traded EUR 109-183/MWh through Sep 2026;
                                     # an industrial buyer also pays network
                                     # and balancing on top, so 160 is if
                                     # anything generous to the project
IDC, WORKING_CAP = 22.0, 26.0        # EUR m  [ENG]

# Incremental cash opex of a gasification island, over the EUR 33.4m above
ISLAND_MAINT_PCT = 0.030             # [ENG]
ISLAND_FIXED     = 6.3               # EUR m/y: operators, AGR solvent,
                                     # shift/Claus catalyst, slag   [ENG]

# Product prices, FCA Kikinda, on the TRADED basis established in Part 8.
# NOT Methanex posted.  Part 8: posted EUR 915/t vs traded EUR 405/t on the
# same day; FCA Kikinda works out at EUR 461-481/t.
MEOH_FCA = 470.0                     # [FACT-derived, Part 8]
ACOH_FCA = 530.0                     # [FACT-derived, Part 8: EUR 610 Europe
                                     #  less ~EUR 80/t export freight]

# ===========================================================================
# 4. THE CANDIDATES
# ===========================================================================
@dataclass
class Feed:
    key: str
    name: str
    delivered: Tuple[float, float, float]   # EUR/t delivered Kikinda
    c_frac: float                            # carbon, as received
    lhv: float                               # GJ/t, as received
    c_eff: float
    capex: Tuple[float, float, float]        # EUR m installed
    available: Optional[float]               # t/y realistically sourceable
    route: str
    evidence: str
    kills: str = ""

FEEDS: List[Feed] = [
 Feed("petcoke", "Petroleum coke, fuel grade, US Gulf or Med -> Bar -> rail",
      (94.5, 115.0, 127.8), 0.867, 32.5, GASIF_C_EFF, (200.0, 225.0, 265.0),
      None, "new solid gasification island; POX shell, COSORB, MeOH loop, "
      "AcOH plant, ASU, tankage all reused",
      "[FACT] Q4-2025 Argus fob USGC 6.5% S non-calcined USD 54.90/t; "
      "delivered chain built up in Part 10",
      "the FOB print is from Q4 2025 and PRE-DATES the war - see the warning"),

 Feed("hsfo", "High-sulphur fuel oil 3.5%, Rotterdam -> Bar -> rail tanker",
      (520.0, 555.0, 600.0), 0.855, 40.2, GASIF_C_EFF, (110.0, 135.0, 175.0),
      None, "LIQUID feed straight into the existing U-13 POX: no mill, no "
      "slurry prep, no lock hoppers, no slag system",
      "[FACT] USD 529.00/mt fob Rotterdam barges, 7 Sep 2026; "
      "delivered leg [ENG]",
      "at USD 529/t the feedstock alone is dearer than the methanol"),

 Feed("vacresid", "Refinery vacuum residue / visbreaker tar, regional",
      (330.0, 400.0, 470.0), 0.855, 39.0, GASIF_C_EFF,
      (110.0, 135.0, 175.0), 400_000.0,
      "same liquid POX conversion as HSFO, but sourced from Pancevo, Brod, "
      "Rijeka, Burgas or Elefsina - no ship, no Port of Bar",
      "[ENG] 60-75% of HSFO, the usual residue discount; NO QUOTED PRICE",
      "no published index: every tonne is a bilateral refinery deal"),

 Feed("coal", "Imported steam coal 6,000 kcal NAR -> Bar -> rail",
      (150.0, 167.0, 190.0), 0.650, 25.1, GASIF_C_EFF,
      (215.0, 240.0, 282.0), None,
      "same solid gasification island as petcoke, plus ash handling",
      "[FACT] API2 cif ARA ~USD 145/t mid-Sep 2026; inland leg [ENG]",
      "more ash, more tonnage, and none of petcoke's grade discount"),

 Feed("husk", "Sunflower husk pellets, Vojvodina (Cantavir ~80 km)",
      (75.0, 82.0, 95.0), 0.460, 16.5, GASIF_C_EFF,
      (210.0, 250.0, 305.0), 100_000.0,
      "biomass gasifier + fuel yard; no torrefaction needed for pellets",
      "[LIST] EUR 67/t EXW bulk, Cantavir listing - a LISTING, not a trade",
      "Serbia's ENTIRE husk arising is ~100 kt/y against ~430 kt/y needed"),

 Feed("straw", "Torrefied cereal straw / corn stover, Vojvodina",
      (105.0, 130.0, 165.0), 0.520, 20.0, GASIF_C_EFF,
      (260.0, 310.0, 380.0), 1_500_000.0,
      "biomass gasifier + a torrefaction plant + a farm-contracting business "
      "MSK does not have",
      "[ENG] EUR 40-55/t baled delivered + torrefaction; UNVERIFIED",
      "the torrefaction plant is a second project bolted to the first"),

 Feed("rdf", "Refuse-derived fuel / SRF - the negative-price idea",
      (-25.0, -10.0, 15.0), 0.400, 16.0, 0.38,
      (240.0, 290.0, 360.0), 150_000.0,
      "biomass/waste gasifier plus a waste reception, shredding and metals "
      "removal plant, and a waste permit MSK does not hold",
      "[ENG] gate fee, not a commodity price; Serbian gate fees are "
      "EUR 10-25/t, EU gate fees EUR 80-150/t",
      "EU RDF cannot legally be shipped to Serbia for recovery after "
      "21 May 2027 unless Serbia is on the EU authorised-country list; "
      "chlorine also poisons a methanol synthesis catalyst"),

 Feed("gas", "Natural gas, pipeline, TTF-linked",
      (0.0, 0.0, 0.0),                       # priced separately, see below
      GAS_C_FRAC, GAS_LHV_M3/GAS_DENSITY*1000.0, GAS_C_EFF,
      (90.0, 115.0, 150.0), None,
      "REFURBISH ONLY - every existing unit stays, including the turbine",
      "[FACT] TTF EUR 79.52/MWh, 18 Sep 2026",
      "at TTF 79.52 the gas bill alone is ~EUR 239m/y"),
]

GAS_TTF_EUR_MWH = 79.52       # [FACT] 18 Sep 2026


def gas_price_per_t(ttf_eur_mwh: float) -> float:
    """EUR per tonne of natural gas at a given TTF price."""
    eur_per_gj = ttf_eur_mwh/3.6
    gj_per_t   = GAS_LHV_M3/GAS_DENSITY*1000.0     # ~50.0 GJ/t
    return eur_per_gj*gj_per_t


def ttf_from_eur_km3(eur_per_km3: float) -> float:
    """Inverse of gas_price_per_t: EUR/1,000 m3 -> the equivalent TTF EUR/MWh."""
    eur_per_gj = eur_per_km3/1000.0/GAS_LHV_M3
    return eur_per_gj*3.6


def annuity(r: float, n: int = 20) -> float:
    return r*(1+r)**n/((1+r)**n-1)


# ===========================================================================
# 5. THE MODEL
# ===========================================================================
def evaluate(f: Feed, band: str = "base", ttf: float = GAS_TTF_EUR_MWH,
             disc: float = 0.10, years: int = 20) -> Dict:
    i = {"low": 0, "base": 1, "high": 2}[band]

    tonnes = C_NEEDED/f.c_eff/f.c_frac                 # t/y of feedstock
    if f.key == "gas":
        price = gas_price_per_t(ttf)
    else:
        price = f.delivered[i]
    feed_cost = tonnes*price

    installed = f.capex[i]
    funding   = installed + IDC + WORKING_CAP

    # Power.  The 15 MW turbine is the asset here: on gas it already carries
    # the whole load (the plant buys only EUR 540k/y of electricity).  On a
    # gasification route the load rises with the ASU and the turbine has to be
    # fed from gasifier waste heat instead - Part 9 bounds that at ~13 MW of
    # shaft work, so the turbine covers less of a bigger load.
    if f.key == "gas":
        net_mw = 0.0
        island = 0.0
    else:
        net_mw = max(GROSS_LOAD_MW - TURBINE_OUTPUT_MW, 0.0)
        island = (installed*ISLAND_MAINT_PCT + ISLAND_FIXED)*1e6
    power = net_mw*HOURS*POWER_EUR_MWH

    rev  = MEOH_SALE*MEOH_FCA + ACOH*ACOH_FCA
    opex = CASH_OPEX_EX_GAS + feed_cost + power + island
    ebitda = rev - opex

    cap_charge = funding*1e6*annuity(disc, years)
    return dict(
        feed=f, band=band, tonnes=tonnes, price=price, feed_cost=feed_cost,
        gj=f.lhv and price/f.lhv, installed=installed, funding=funding,
        power=power, island=island, rev=rev, opex=opex, ebitda=ebitda,
        cap_charge=cap_charge, net=ebitda-cap_charge,
        eur_per_t_feed=feed_cost/MEOH_EQ,
        eur_per_t_cap=cap_charge/MEOH_EQ,
        eur_per_t_all=(opex+cap_charge)/MEOH_EQ,
        payback=funding*1e6/ebitda if ebitda > 0 else None)


def table():
    print("="*97)
    print("MSK KIKINDA - PART 11: WHICH FEEDSTOCK IS ACTUALLY CHEAPEST "
          "(September 2026)")
    print("="*97)
    print(f"\nCarbon that must reach product : {C_NEEDED:>11,.0f} t C/y")
    print(f"Methanol-equivalent output     : {MEOH_EQ:>11,.0f} t/y")
    print(f"Natural-gas carbon efficiency  : {GAS_C_EFF:>11.1%}   "
          "[MEASURED from the operator's own projection]")
    print(f"Gasification carbon efficiency : {GASIF_C_EFF:>11.1%}   "
          f"[ENG, Part 9 range {GASIF_C_EFF_LO:.0%}-{GASIF_C_EFF_HI:.0%}]")

    print("\n" + "-"*97)
    print("A.  DELIVERED COST OF ENERGY - the number that decides everything")
    print("-"*97)
    print(f"{'feedstock':<40}{'EUR/t':>10}{'GJ/t':>8}{'EUR/GJ':>9}"
          f"{'x petcoke':>11}")
    print("-"*97)
    rows = []
    for f in FEEDS:
        p = gas_price_per_t(GAS_TTF_EUR_MWH) if f.key == "gas" \
            else f.delivered[1]
        rows.append((f, p, p/f.lhv))
    base_gj = [r[2] for r in rows if r[0].key == "petcoke"][0]
    for f, p, gj in sorted(rows, key=lambda r: r[2]):
        print(f"{f.name[:39]:<40}{p:>10,.1f}{f.lhv:>8.1f}{gj:>9.2f}"
              f"{gj/base_gj:>10.2f}x")
    print("-"*97)
    print("Read this first: at Sep-2026 prices natural gas costs SIX TIMES")
    print("what petcoke costs per GJ, and fuel oil three and a half times.")

    print("\n" + "-"*97)
    print("B.  ALL-IN COST PER TONNE OF METHANOL-EQUIVALENT")
    print("    feedstock + every other cash cost + capital charge "
          "(20y, 10%)")
    print("-"*97)
    print(f"{'feedstock':<34}{'t/y feed':>11}{'feed':>8}{'other':>8}"
          f"{'capital':>9}{'ALL-IN':>9}{'EBITDA':>10}")
    print(f"{'':<34}{'':>11}{'EUR/t':>8}{'EUR/t':>8}{'EUR/t':>9}"
          f"{'EUR/t':>9}{'EUR m/y':>10}")
    print("-"*97)
    res = [evaluate(f) for f in FEEDS]
    for r in sorted(res, key=lambda x: x["eur_per_t_all"]):
        other = (r["opex"]-r["feed_cost"])/MEOH_EQ
        print(f"{r['feed'].name[:33]:<34}{r['tonnes']:>11,.0f}"
              f"{r['eur_per_t_feed']:>8,.0f}{other:>8,.0f}"
              f"{r['eur_per_t_cap']:>9,.0f}{r['eur_per_t_all']:>9,.0f}"
              f"{r['ebitda']/1e6:>10,.1f}")
    print("-"*97)
    rev_per_t = (MEOH_SALE*MEOH_FCA + ACOH*ACOH_FCA)/MEOH_EQ
    print(f"Revenue on the same basis: EUR {rev_per_t:,.0f}/t "
          f"(methanol {MEOH_FCA:.0f}, acetic acid {ACOH_FCA:.0f}, FCA Kikinda)")
    print("Anything whose ALL-IN exceeds that number destroys value.")

    print("\n" + "-"*97)
    print("C.  WHAT EACH ROUTE ACTUALLY REUSES, AND WHAT IT COSTS TO BUILD")
    print("-"*97)
    for r in sorted(res, key=lambda x: x["eur_per_t_all"]):
        f = r["feed"]
        print(f"\n{f.name}")
        print(f"   capex installed  EUR {f.capex[0]:.0f}-{f.capex[2]:.0f}m "
              f"(base {f.capex[1]:.0f}) + IDC {IDC:.0f} + WC {WORKING_CAP:.0f}"
              f"  ->  funding EUR {r['funding']:.0f}m")
        print(f"   reuse            {f.route}")
        print(f"   evidence         {f.evidence}")
        if f.kills:
            print(f"   >> WEAKNESS      {f.kills}")


def volume():
    print("="*97)
    print("CAN YOU ACTUALLY BUY THE TONNAGE?")
    print("="*97)
    print("A price you cannot buy 400,000 tonnes of every year is not a price.")
    print(f"\n{'feedstock':<40}{'needed t/y':>13}{'sourceable':>14}"
          f"{'cover':>9}")
    print("-"*97)
    for f in FEEDS:
        if f.key == "gas":
            continue
        need = C_NEEDED/f.c_eff/f.c_frac
        if f.available is None:
            print(f"{f.name[:39]:<40}{need:>13,.0f}{'world market':>14}"
                  f"{'ok':>9}")
        else:
            cov = f.available/need
            flag = "OK" if cov >= 1.5 else ("TIGHT" if cov >= 1.0 else "FAILS")
            print(f"{f.name[:39]:<40}{need:>13,.0f}{f.available:>14,.0f}"
                  f"{cov:>8.2f}x  {flag}")
    print("-"*97)
    print("Sunflower husk: Serbia's whole sunflower crop is ~454,000 t of seed")
    print("[FACT], husk is ~22% of that, so ~100,000 t/y EXISTS NATIONALLY -")
    print("and the oil mills already burn most of it for their own steam.")
    print("It is a CO-FEED at best, never the base load.  Do not plan on it.")


def switch(disc: float = 0.10):
    print("="*97)
    print("THE SWITCHING PRICE - what the owner actually asked for")
    print("="*97)
    print("The stated requirement is to keep feedstock optionality: burn gas")
    print("when gas is cheap, petcoke when it is not, with no long-term")
    print("binding offtake.  That requirement has a price, and here it is.\n")

    pk = [f for f in FEEDS if f.key == "petcoke"][0]
    gs = [f for f in FEEDS if f.key == "gas"][0]
    rp = evaluate(pk)

    # (a) Before FID: compare total cost including each route's own capital.
    # (b) After FID: the petcoke island is sunk, so compare CASH only - and
    #     gas has to beat petcoke's cash cost to justify idling a paid asset.
    def gas_total(ttf, cash_only=False):
        r = evaluate(gs, ttf=ttf, disc=disc)
        return r["opex"] if cash_only else r["opex"]+r["cap_charge"]

    def bisect(target, cash_only, lo=1.0, hi=400.0):
        for _ in range(80):
            mid = (lo+hi)/2
            if gas_total(mid, cash_only) > target:
                hi = mid
            else:
                lo = mid
        return (lo+hi)/2

    t_before = bisect(rp["opex"]+rp["cap_charge"], False)
    t_after  = bisect(rp["opex"], True)

    print(f"{'':<46}{'TTF EUR/MWh':>14}{'USD/1000 m3':>14}")
    print("-"*97)
    print(f"{'TODAY (18 Sep 2026)':<46}{GAS_TTF_EUR_MWH:>14.1f}"
          f"{gas_price_per_t(GAS_TTF_EUR_MWH)*GAS_DENSITY*FX:>14,.0f}")
    print(f"{'the operator own 2026 projection':<46}"
          f"{ttf_from_eur_km3(470.20):>14.1f}{501.0:>14,.0f}")
    print(f"{'BEFORE FID: gas beats petcoke below':<46}{t_before:>14.1f}"
          f"{gas_price_per_t(t_before)*GAS_DENSITY*FX:>14,.0f}")
    print(f"{'AFTER FID: gas beats petcoke CASH below':<46}{t_after:>14.1f}"
          f"{gas_price_per_t(t_after)*GAS_DENSITY*FX:>14,.0f}")
    print("-"*97)
    print(f"\nWhat this means in plain terms:")
    print(f"  Gas has to fall to about EUR {t_before:.0f}/MWh before building")
    print(f"  the petcoke island stops making sense.  That is roughly")
    print(f"  {t_before/GAS_TTF_EUR_MWH:.0%} of today's TTF.")
    print(f"\n  Once the island IS built, gas has to fall to about")
    print(f"  EUR {t_after:.0f}/MWh before it is worth idling it and burning")
    print(f"  gas instead.  Below that price dual-feed capability pays;")
    print(f"  above it, it is insurance you are unlikely to exercise.")
    print(f"\n  Keeping the gas train alive and connected is cheap - it is")
    print(f"  already there.  The honest case for dual-feed is NOT that you")
    print(f"  will switch often.  It is that it removes the single-supplier")
    print(f"  exposure that shut this plant down in the first place.")


# ===========================================================================
# 6. THE TURBINE, AND WHY IT IS NOT THE LEVER
# ===========================================================================
O2_PER_COKE   = 0.95      # t O2 per t petcoke  [ENG]
ASU_MWH_PER_T = 0.30      # MWh per t O2, large cryogenic unit incl. compression [ENG]
STEAM_CEILING_TH = (60.0, 75.0)   # t/h HP steam recoverable  [ENG, Part 9]
BACKPRESSURE_KJ  = 420.0          # 100 bar -> ~12 bar header  [ENG, Part 9]


def turbine():
    print("="*97)
    print("THE 15 MW STEAM TURBINE - refurbish it, do NOT try to uprate it")
    print("="*97)
    print("\nToday, on gas, this turbine carries the entire plant: MSK buys")
    print("only EUR 540,000/y of electricity [FACT-MSK].  That self-sufficiency")
    print("is the single most valuable thing the site owns after the reactors.")
    print("\nOn petcoke it stops being enough, for two reasons at once:")

    pk = [f for f in FEEDS if f.key == "petcoke"][0]
    coke = C_NEEDED/pk.c_eff/pk.c_frac
    o2   = coke*O2_PER_COKE
    asu_mwh = o2*ASU_MWH_PER_T
    asu_mw  = asu_mwh/HOURS

    lo_mw = STEAM_CEILING_TH[0]*1000/3600*BACKPRESSURE_KJ/1000
    hi_mw = STEAM_CEILING_TH[1]*1000/3600*BACKPRESSURE_KJ/1000

    print(f"\n  1. THE LOAD GOES UP.  An air separation unit appears that was")
    print(f"     never there before:")
    print(f"        petcoke feed        {coke:>12,.0f} t/y")
    print(f"        oxygen needed       {o2:>12,.0f} t/y   [ENG {O2_PER_COKE} t O2/t coke]")
    print(f"        ASU power           {asu_mwh:>12,.0f} MWh/y = {asu_mw:>5.1f} MW"
          f"   [ENG {ASU_MWH_PER_T} MWh/t O2]")
    print(f"        total plant load    {GROSS_LOAD_MW:>12,.1f} MW   [ENG]")

    print(f"\n  2. THE STEAM GOES DOWN.  Part 9 established that the gasifier")
    print(f"     can raise {STEAM_CEILING_TH[0]:.0f}-{STEAM_CEILING_TH[1]:.0f} t/h of HP steam, not the 110-125 t/h")
    print(f"     a supplied model booked.  Let down to the process header at")
    print(f"     ~{BACKPRESSURE_KJ:.0f} kJ/kg that is only {lo_mw:.1f}-{hi_mw:.1f} MW of shaft work.")

    net = GROSS_LOAD_MW - TURBINE_OUTPUT_MW
    bill = net*HOURS*POWER_EUR_MWH
    print(f"\n  >> So the existing 15 MW machine is ALREADY the right size.")
    print(f"     It is not undersized - it is fed by steam that tops out at")
    print(f"     about {hi_mw:.0f} MW of back-pressure work, plus 2-3 MW from a")
    print(f"     condensing tail on the surplus: call it {TURBINE_OUTPUT_MW:.0f} MW delivered")
    print(f"     against a 15 MW plate.  Uprating the turbine buys nothing,")
    print(f"     because the steam is the constraint, not the machine.")
    print(f"     REFURBISH IT.  DO NOT SPECIFY A BIGGER ONE.")

    print(f"\n  The residual import is then {net:.0f} MW:")
    print(f"        {net:.0f} MW x {HOURS:,.0f} h x EUR {POWER_EUR_MWH:.0f}/MWh"
          f" = EUR {bill/1e6:,.1f}m/y")
    print(f"        = EUR {bill/MEOH_EQ:,.0f} per tonne of product - the SECOND")
    print(f"          largest cost line after the feedstock itself.")

    print(f"\n" + "-"*97)
    print("THE LEVER IS THE LOAD, NOT THE GENERATION")
    print("-"*97)
    saved = asu_mw*HOURS*POWER_EUR_MWH
    print(f"About {asu_mw:.1f} MW of that {GROSS_LOAD_MW:.0f} MW load is the ASU alone,")
    print(f"worth EUR {saved/1e6:.1f}m/y of electricity and an estimated")
    print(f"EUR 60-80m of the capex [ENG/RFQ].")
    print("")
    print("Oxygen over the fence - Messer, Linde or Air Liquide build, own and")
    print("operate the ASU on MSK's site and sell oxygen by the tonne - removes")
    print("both from MSK's books.")
    print("")
    print("This is NOT the build-own-operate structure the owner rejected.")
    print("That rejection was about keeping control of the FEEDSTOCK, and an")
    print("oxygen contract does not touch the feedstock at all: the gasifier,")
    print("the feed system and every tonne of coke, coal, residue or gas that")
    print("goes into it stay wholly MSK's.  An industrial-gas contract locks a")
    print("UTILITY, not a feed.  It is worth a quote precisely because it is")
    print("the one thing that can be de-scoped without losing optionality.")


def warning():
    print("\n" + "!"*97)
    print("THE ONE NUMBER IN THIS PART THAT I DO NOT TRUST")
    print("!"*97)
    print("Every petcoke figure here descends from an Argus fob USGC print of")
    print("USD 54.90/t for Q4 2025.  Since then the US-Iran war has taken TTF")
    print("from roughly EUR 27 to EUR 79.52/MWh [FACT], API2 coal to about")
    print("USD 145/t [FACT] and 3.5% fuel oil to USD 529/t [FACT].")
    print("")
    print("Fuel-grade petcoke competes with coal in cement kilns and power")
    print("stations.  It will NOT have stayed at USD 55 while coal went to")
    print("USD 145.  I could not obtain a September-2026 petcoke assessment:")
    print("the Argus index is paywalled and the session cannot reach it.")
    print("")
    print("So: petcoke is still almost certainly the cheapest thing you can")
    print("put on a ship, because the RANKING is robust - it moves with coal,")
    print("and coal is still far below oil and gas per GJ.  But the MARGIN")
    print("in section B is overstated by an unknown amount.")
    print("")
    print("One phone call to a petcoke trader fixes this.  Ask for fob USGC")
    print("6.5% S 40 HGI, and separately for a high-sulphur shot-coke offer,")
    print("which is what a gasifier should actually be buying.")
    print("!"*97)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("all", "table"):
        table()
    if cmd in ("all", "volume"):
        print()
        volume()
    if cmd in ("all", "turbine"):
        print()
        turbine()
    if cmd in ("all", "switch"):
        print()
        switch()
    if cmd in ("all", "table"):
        warning()
