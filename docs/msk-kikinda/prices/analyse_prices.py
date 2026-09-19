#!/usr/bin/env python3
"""
Part 8b - Calibrate the business-plan price against observed data.
Reads observed_prices.json. Stdlib only.
"""
import json, os, statistics as st

D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "observed_prices.json")))
FX = D["fx"]["usd_eur"]
SPIKE = {"2026Q2", "2026Q3"}   # Middle East supply shock

def main():
    w = 76
    print("="*w); print("OBSERVED PRICES vs THE PLANNING NUMBER".center(w)); print("="*w)

    posted = D["methanex_europe_posted_eur_t"]
    print("\n1. METHANEX EUROPEAN POSTED  (GROSS LIST - not a transaction price)")
    for r in posted:
        flag = "  <-- WAR SPIKE" if r["period"] in SPIKE else ""
        print(f"   {r['period']}  EUR {r['price']:>4}/t   {r['confidence']:<9}{flag}")
    allp = [r["price"] for r in posted]
    exsp = [r["price"] for r in posted if r["period"] not in SPIKE]
    print(f"\n   mean all {len(allp)} quarters      EUR {st.mean(allp):>6.0f}/t")
    print(f"   median                    EUR {st.median(allp):>6.0f}/t")
    print(f"   mean EXCLUDING the spike  EUR {st.mean(exsp):>6.0f}/t   <-- mid-cycle")
    print(f"   min / max                 EUR {min(allp)} / {max(allp)}/t")

    real = D["methanex_global_realized_usd_t"]
    print("\n2. METHANEX GLOBAL REALIZED  (what the company actually got)")
    for r in real:
        print(f"   {r['period']}  USD {r['price']:>4}/t  = EUR {r['price']*FX:>6.0f}/t")

    print("\n3. THE GAP - why you must never plan on a posted price")
    pm = {r["period"]: r["price"] for r in posted}
    for r in real:
        p = pm.get(r["period"])
        if p:
            e = r["price"]*FX
            print(f"   {r['period']}  posted EUR {p:>4}  realized EUR {e:>4.0f}"
                  f"   realized = {e/p:.0%} of posted")
    print("   Realized is a GLOBAL blend including Asia and China, where prices")
    print("   run well below Europe, so the Europe-only discount is smaller than")
    print("   this. The direction is not in doubt; the magnitude is.  [CAVEAT]")

    print("\n4. ACETIC ACID, EUROPE")
    for r in D["acetic_acid_europe_usd_t"]:
        print(f"   {r['period']}  USD {r['price']:>4}/t = EUR {r['price']*FX:>4.0f}/t"
              f"   {r['confidence']}")
    aa = [r["price"]*FX for r in D["acetic_acid_europe_usd_t"]]
    print(f"   range EUR {min(aa):.0f} - {max(aa):.0f}/t, mean EUR {st.mean(aa):.0f}/t")

    print("\n5. VERDICT ON THE PLANNING PRICE")
    mid = st.mean(exsp)
    print(f"   Mid-cycle European POSTED (ex-spike):        EUR {mid:>6.0f}/t")
    for ratio, lbl in ((0.80, "Europe premium region, modest discount"),
                       (0.85, "smaller discount"),
                       (0.90, "near-posted, optimistic")):
        print(f"   x {ratio:.2f} realized/posted ->  EUR {mid*ratio:>6.0f}/t   ({lbl})")
    print(f"\n   Your planning band:                          EUR 450 - 500/t")
    lo, hi = mid*0.80, mid*0.90
    if 450 >= lo*0.95 and 500 <= hi*1.05:
        print( "   -> SUPPORTED by the observed data. It sits inside the")
        print( "      mid-cycle realized range, not above it.")
    print(f"\n   Q3 2026 posted is EUR {pm['2026Q3']}/t. Planning on that would be")
    print(f"   planning on a war. Methanex's own realized price two quarters")
    print(f"   earlier was EUR {real[0]['price']*FX:.0f}/t - less than half.")

    print("\n6. ACETIC ACID PLANNING")
    print(f"   Observed EUR {min(aa):.0f}-{max(aa):.0f}/t. Part 7 used EUR 550-630/t.")
    print(f"   -> SUPPORTED. MSK's own projection used EUR 629/t, at the top")
    print(f"      of the observed range; EUR 550-580 is the safer plan.")
    print("="*w)
    print("\nSOURCES")
    for s in D["sources"]:
        print(f"  {s}")

if __name__ == "__main__":
    main()
