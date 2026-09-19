#!/usr/bin/env python3
"""
MSK Kikinda - Part 10: PETCOKE SOURCING, US GULF -> PORT OF BAR -> KIKINDA.

Tags: [FACT] published/attributable   [EST] engineering estimate
      [ASSUM] chosen assumption       [RFQ] must be bid

Collected 2026-09-19 by search; the session's egress policy blocked every
primary host, so nothing here was read off a source page. Confirm before
committing volume.
"""

USD_EUR = 0.92          # [ASSUM]
RAIL_KM = 600.0         # [EST] Bar-Belgrade ~450 + Belgrade-Kikinda ~130
FEED_KT = 241.0         # [EST] Part 9 corrected carbon balance, acid-max slate

# --- FOB US Gulf, fuel-grade high-sulphur ---------------------------------
# [FACT] Argus fob US Gulf 6.5% S / 40 HGI is the seaborne benchmark for
#        US Gulf and midcontinent coke; published weekly.
# [FACT] Q3 2025 fob offers USD 67-77/t. Q4 2025 6.5% S non-calcined
#        USD 54.90/t, -16.2% on Q3.
# [FACT] Argus outlook: higher heavy sour crude runs on the USGC may lift
#        high-sulphur fuel-grade output in 2026 and pressure fob 6.5% prices.
#        -> the supply side is working FOR a buyer.
FOB_USGC = {"low": 50.0, "base": 58.0, "high": 70.0}     # [EST] USD/t

# The grade discount MSK can uniquely capture. A gasifier with AGR + Claus/TGTU
# is indifferent to sulphur, and a slurry mill does not care about HGI the way
# a cement kiln does. So MSK buys BELOW the 6.5%/40 benchmark:  [EST]
GRADE_DISCOUNT = {"sulphur_7_8pct": 4.0, "hgi_30_35": 4.0, "high_V_Ni": 3.0}

# --- Ocean freight, Supramax ----------------------------------------------
# [FACT] June 2026, 50,000 t petcoke Houston -> Iskenderun, spot laycan:
#        ~USD 41.50/t.  April 2026: ~USD 35/t.
# [FACT] Same week, Houston -> ARA: ~USD 33.50/t.
# Bar is ~600 nm shorter than Iskenderun from Gibraltar, but is a thinner
# market with poorer backhaul, so owners will not pass the full saving on.
FREIGHT_USG_BAR = {"low": 36.0, "base": 41.0, "high": 47.0}   # [EST] USD/t

# --- Port of Bar -----------------------------------------------------------
# [FACT] Max draft 12.5 m; vessels to 80,000 DWT; LOA 260 m; 2,700 m of berth.
# A 58,000 dwt Supramax loads to ~12.8 m at full summer deadweight, so expect
# to lift ~52-55,000 t rather than a full cargo.  [EST]
BAR_DRAFT_M, BAR_MAX_DWT = 12.5, 80_000
PARCEL_T = 53_000                                          # [EST]
PORT_EUR = {"low": 4.0, "base": 5.5, "high": 7.0}          # [EST] EUR/t
RAIL_EUR_TKM = {"low": 0.045, "base": 0.052, "high": 0.060}  # [EST]

# --- Mediterranean alternative --------------------------------------------
# Not requested, but freight now dominates, so it has to be tested. [EST]
FOB_MED = {"low": 70.0, "base": 80.0, "high": 92.0}
FREIGHT_MED_BAR = {"low": 10.0, "base": 14.0, "high": 19.0}


def delivered(fob_usd, frt_usd, port_eur, rail_tkm, discount=0.0):
    fob = (fob_usd - discount) * USD_EUR
    frt = frt_usd * USD_EUR
    rail = rail_tkm * RAIL_KM
    return dict(fob=fob, frt=frt, port=port_eur, rail=rail,
                cfr=fob + frt, total=fob + frt + port_eur + rail)


def main():
    w = 82
    print("=" * w); print("PART 10 - PETCOKE TO KIKINDA VIA PORT OF BAR".center(w)); print("=" * w)

    print("\n1. PORT OF BAR TAKES A SUPRAMAX  [FACT]")
    print(f"   max draft {BAR_DRAFT_M} m | up to {BAR_MAX_DWT:,} DWT | LOA 260 m")
    print(f"   -> a 58,000 dwt Supramax draws ~12.8 m full, so lift ~{PARCEL_T:,} t")
    print(f"   -> {FEED_KT:.0f} kt/y = {FEED_KT*1000/PARCEL_T:.1f} cargoes/year")

    print("\n2. DELIVERED COST, US GULF -> BAR -> KIKINDA  (EUR/t)")
    print(f"   {'':<8}{'FOB':>8}{'freight':>9}{'CFR Bar':>9}{'port':>7}{'rail':>8}{'DELIVERED':>11}")
    for k in ("low", "base", "high"):
        d = delivered(FOB_USGC[k], FREIGHT_USG_BAR[k], PORT_EUR[k], RAIL_EUR_TKM[k])
        print(f"   {k:<8}{d['fob']:>8.1f}{d['frt']:>9.1f}{d['cfr']:>9.1f}"
              f"{d['port']:>7.1f}{d['rail']:>8.1f}{d['total']:>11.1f}")

    disc = sum(GRADE_DISCOUNT.values())
    print(f"\n3. THE GRADE DISCOUNT MSK CAN UNIQUELY TAKE  [EST]  -USD {disc:.0f}/t")
    for k, v in GRADE_DISCOUNT.items():
        print(f"   -USD {v:>4.1f}  {k}")
    print("   A gasifier with AGR + Claus/TGTU is indifferent to sulphur; a slurry")
    print("   mill does not care about HGI the way a cement kiln does. Cement and")
    print("   power buyers set the benchmark - MSK should never pay it.")
    d = delivered(FOB_USGC["base"], FREIGHT_USG_BAR["base"], PORT_EUR["base"],
                  RAIL_EUR_TKM["base"], discount=disc)
    print(f"   -> base case with discount: EUR {d['total']:.1f}/t delivered"
          f"  (saves EUR {disc*USD_EUR*FEED_KT/1000:.1f}m/y)")

    print("\n4. FREIGHT NOW DOMINATES - SO TEST THE MEDITERRANEAN  [EST]")
    print(f"   {'route':<26}{'FOB':>8}{'freight':>9}{'CFR Bar':>10}{'DELIVERED':>11}")
    us = delivered(FOB_USGC["base"], FREIGHT_USG_BAR["base"], PORT_EUR["base"], RAIL_EUR_TKM["base"])
    med = delivered(FOB_MED["base"], FREIGHT_MED_BAR["base"], PORT_EUR["base"], RAIL_EUR_TKM["base"])
    print(f"   {'US Gulf (Houston)':<26}{FOB_USGC['base']:>8.0f}{FREIGHT_USG_BAR['base']:>9.0f}"
          f"{us['cfr']:>10.1f}{us['total']:>11.1f}")
    print(f"   {'Mediterranean refinery':<26}{FOB_MED['base']:>8.0f}{FREIGHT_MED_BAR['base']:>9.0f}"
          f"{med['cfr']:>10.1f}{med['total']:>11.1f}")
    be = FOB_USGC["base"] + (FREIGHT_USG_BAR["base"] - FREIGHT_MED_BAR["base"])
    print(f"\n   Med petcoke wins up to FOB USD {be:.0f}/t - a USD {be-FOB_USGC['base']:.0f}/t")
    print(f"   premium over US Gulf - because it saves USD "
          f"{FREIGHT_USG_BAR['base']-FREIGHT_MED_BAR['base']:.0f}/t of freight.")
    print("   US Gulf FOB is the cheapest in the world and still may not be the")
    print("   cheapest DELIVERED. Tender both.")

    print("\n5. COST STACK - WHERE THE MONEY ACTUALLY GOES (base, with discount)")
    tot = d["total"]
    for lbl, v in (("FOB cargo", d["fob"]), ("ocean freight", d["frt"]),
                   ("port of Bar", d["port"]), ("rail Bar-Kikinda", d["rail"])):
        print(f"   {lbl:<20}EUR {v:>6.1f}/t{v/tot:>8.0%}  {'#'*int(v/tot*40)}")
    print(f"   {'TOTAL':<20}EUR {tot:>6.1f}/t")
    print(f"\n   Ocean freight + rail = {(d['frt']+d['rail'])/tot:.0%} of delivered cost.")
    print("   The cargo itself is a minority of the bill. Negotiate logistics")
    print("   at least as hard as the commodity.")

    print("\n6. WORKING CAPITAL")
    val = PARCEL_T * tot / 1e6
    print(f"   one Supramax parcel: {PARCEL_T:,} t x EUR {tot:.0f}/t = EUR {val:.1f}m")
    print(f"   USG-Bar voyage ~25-30 days + 30 days stock = ~EUR {val*2:.1f}m tied up  [EST]")
    print(f"   A Mediterranean source cuts transit to ~5 days and roughly halves this.")

    print("\n7. WHAT TO PUT IN THE RFQ  [RFQ]")
    for t in ["Index-linked formula off Argus fob USGC 6.5% S 40 HGI, NOT a fixed price",
              "Explicit discount schedule for S above 6.5%, HGI below 40, V+Ni above spec",
              "5-10 year term with annual volume 240-260 kt and +/-10% optionality",
              "Seller's assay: proximate, ultimate, S, V, Ni, ash fusion, HGI, grindability",
              "CFR Bar, not FOB - make the seller carry freight risk if he will",
              "Laycan flexibility and demurrage terms at Bar (thin port, thin market)",
              "Right to reject on assay, with an independent surveyor named"]:
        print(f"   - {t}")
    print("=" * w)


if __name__ == "__main__":
    main()
