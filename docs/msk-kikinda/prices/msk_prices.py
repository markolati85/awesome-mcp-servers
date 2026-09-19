#!/usr/bin/env python3
"""
MSK Kikinda - Part 8: HARD-EVIDENCE PRICE COLLECTOR for methanol and acetic acid.

WHY THIS INSTEAD OF A SUBSCRIPTION
----------------------------------
A price assessment (IHS / S&P / ICIS / Argus) is a judgement about where a
market is. Customs data is a record of what was actually paid, declared to a
government, by the importer, under penalty. For a business plan and for a
lender's diligence, the second is stronger evidence than the first - and a
lender can verify it independently, for free, forever.

It is also the right shape for THIS project. Part 4 turned on "Central Europe
delivered parity": what an imported tonne actually costs at the buyer's gate in
Budapest, Vienna, Bratislava, Zagreb or northern Italy. Eurostat reports exactly
that - monthly, by CN8 product, by reporter AND partner country. No assessment
service publishes that pairing.

Note also: MSK's own 2026 projection used IHS forecasts of EUR 340-350/t for
methanol. The spike ran to EUR 830-915/t. The forecast was not the valuable
part. Hard transaction data is, and it is free.

WHAT THIS IS NOT
----------------
This does not touch any paywalled or subscription service. Every source below
publishes openly. Nothing here circumvents an access control or a login.

SOURCES
-------
  Eurostat Comext  EU trade by CN8, monthly, reporter x partner. PRIMARY.
                   methanol CN 29051100, acetic acid CN 29152100
  UN Comtrade      global HS6 (290511 / 291521), free preview tier.
                   Needed for Serbia, Turkey, UK, China - non-EU reporters.
  Methanex posted  public regional reference price. NOT a transaction price;
                   carried only to measure the posted-to-actual gap.

CAVEATS - read before quoting any number this produces
------------------------------------------------------
  * Unit value = declared value / declared mass. It is an AVERAGE over a month
    and a country pair, mixing contract and spot, grades, and package sizes.
  * EU import values are at the EU border (CIF-type); export values are FOB-type.
    A unit value is therefore NOT comparable to FOB Rotterdam without adjustment.
  * Thin flows give wild unit values. --min-tonnes filters them; default 200 t.
  * Trade data lags roughly 2-3 months.
  * Re-exports and transit can distort a partner pairing.

STATUS: the network policy in the session that wrote this blocked
ec.europa.eu, comtradeapi.un.org and www.methanex.com, so the live calls below
are UNTESTED. Every request prints the exact URL it uses and dumps the raw
payload on a parse failure, so a mismatch is quick to find and fix. Run with
--probe first.

Stdlib only.  python3 msk_prices.py --help
"""

from __future__ import annotations
import argparse, csv, json, os, sys, time, urllib.parse, urllib.request
from datetime import date

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
UA = "Mozilla/5.0 (compatible; MSK-price-research/1.0)"

# --- product codes ---------------------------------------------------------
CN = {"methanol": "29051100", "acetic_acid": "29152100"}
HS6 = {"methanol": "290511",  "acetic_acid": "291521"}

# --- markets --------------------------------------------------------------
# Eurostat uses 2-letter codes; Comtrade uses UN M49 numeric.
EU_MARKETS = {
    "HU": ("Hungary", 348), "AT": ("Austria", 40),   "IT": ("Italy", 380),
    "HR": ("Croatia", 191), "SK": ("Slovakia", 703), "CZ": ("Czechia", 203),
    "PL": ("Poland", 616),  "SI": ("Slovenia", 705), "RO": ("Romania", 642),
    "BG": ("Bulgaria", 100),"DE": ("Germany", 276),  "NL": ("Netherlands", 528),
}
NON_EU = {"RS": ("Serbia", 688), "BA": ("Bosnia and Herzegovina", 70),
          "MK": ("North Macedonia", 807), "TR": ("Turkiye", 792)}

EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-045409"
COMTRADE = "https://comtradeapi.un.org/public/v1/preview/C/M/HS"


# ===========================================================================
def fetch(url: str, params: dict, tag: str, ttl_hours: int = 24) -> dict | None:
    """GET JSON with an on-disk cache. Prints the URL. Never raises."""
    os.makedirs(CACHE, exist_ok=True)
    qs = urllib.parse.urlencode(params, doseq=True)
    full = f"{url}?{qs}"
    key = os.path.join(CACHE, f"{tag}_{abs(hash(full))}.json")
    if os.path.exists(key) and time.time() - os.path.getmtime(key) < ttl_hours*3600:
        with open(key) as f:
            return json.load(f)
    print(f"  GET {full}", file=sys.stderr)
    req = urllib.request.Request(full, headers={"User-Agent": UA,
                                                "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode("utf-8", "replace")
    except Exception as e:
        print(f"  !! {type(e).__name__}: {e}", file=sys.stderr)
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        dump = key.replace(".json", ".raw.txt")
        with open(dump, "w") as f:
            f.write(raw)
        print(f"  !! not JSON. First 400 chars saved to {dump}:\n{raw[:400]}",
              file=sys.stderr)
        return None
    with open(key, "w") as f:
        json.dump(data, f)
    return data


# ===========================================================================
def jsonstat_rows(d: dict):
    """
    Flatten a JSON-stat v2 response (Eurostat's format) into dicts.
    Eurostat returns `dimension` with an `id` order and `category.index`,
    plus a sparse `value` map keyed by flat index.
    """
    if not d or "value" not in d or "dimension" not in d:
        return
    dim = d["dimension"]
    ids = d.get("id") or list(dim.keys())
    sizes = d.get("size") or [len(dim[i]["category"]["index"]) for i in ids]
    labels = []
    for i in ids:
        idx = dim[i]["category"]["index"]
        if isinstance(idx, dict):
            inv = {v: k for k, v in idx.items()}
            labels.append([inv[n] for n in range(len(inv))])
        else:
            labels.append(list(idx))
    for flat, val in d["value"].items():
        n = int(flat); coord = {}
        for pos in range(len(ids) - 1, -1, -1):
            n, r = divmod(n, sizes[pos]) if pos else (0, n)
            coord[ids[pos]] = labels[pos][r]
        coord["value"] = val
        yield coord


def eurostat_trade(product_cn, reporter, partner, year, flow=1):
    """
    flow 1 = import, 2 = export.
    Returns list of {period, indicator, value}.
    """
    p = {"format": "JSON", "lang": "EN", "product": product_cn,
         "reporter": reporter, "partner": partner, "flow": str(flow),
         "indicators": ["VALUE_EUR", "QUANTITY_KG"], "time": str(year)}
    d = fetch(EUROSTAT, p, f"es_{product_cn}_{reporter}_{partner}_{year}_{flow}")
    return list(jsonstat_rows(d)) if d else []


def comtrade_trade(hs6, reporter_m49, period, flow="M"):
    p = {"reporterCode": str(reporter_m49), "period": str(period),
         "cmdCode": hs6, "flowCode": flow}
    d = fetch(COMTRADE, p, f"ct_{hs6}_{reporter_m49}_{period}_{flow}")
    if not d:
        return []
    return d.get("data", []) if isinstance(d, dict) else []


# ===========================================================================
def unit_values(rows, min_tonnes):
    """Pair VALUE_EUR with QUANTITY_KG per period and return EUR/tonne."""
    by = {}
    for r in rows:
        per = r.get("time") or r.get("TIME_PERIOD") or r.get("period")
        ind = r.get("indicators") or r.get("indicator")
        if per is None or ind is None:
            continue
        by.setdefault(per, {})[ind] = r["value"]
    out = []
    for per, v in sorted(by.items()):
        val, kg = v.get("VALUE_EUR"), v.get("QUANTITY_KG")
        if not val or not kg:
            continue
        t = kg / 1000.0
        if t < min_tonnes:
            continue
        out.append({"period": per, "tonnes": round(t, 1),
                    "value_eur": round(val, 0), "eur_per_t": round(val / t, 2)})
    return out


def comtrade_unit_values(rows, min_tonnes):
    out = []
    for r in rows:
        kg = r.get("netWgt") or r.get("NetWgt") or 0
        usd = r.get("primaryValue") or r.get("PrimaryValue") or 0
        if not kg or not usd:
            continue
        t = kg / 1000.0
        if t < min_tonnes:
            continue
        out.append({"period": r.get("period"), "partner": r.get("partnerDesc"),
                    "tonnes": round(t, 1), "usd_per_t": round(usd / t, 2)})
    return out


# ===========================================================================
def cmd_probe(a):
    print("Probing each source with one minimal request.\n")
    ok = {}
    print("[1] Eurostat Comext")
    r = eurostat_trade(CN["methanol"], "HU", "EXT_EU27_2020", a.year)
    ok["eurostat"] = bool(r)
    print(f"    -> {len(r)} cells\n")
    print("[2] UN Comtrade")
    r2 = comtrade_trade(HS6["methanol"], 348, f"{a.year}01")
    ok["comtrade"] = bool(r2)
    print(f"    -> {len(r2)} records\n")
    for k, v in ok.items():
        print(f"  {k:<12} {'OK' if v else 'FAILED - see the URL and error above'}")
    if not any(ok.values()):
        print("\nBoth failed. Most likely: network policy, or a changed API "
              "parameter set.\nThe exact URLs are printed above - open one in a "
              "browser to see what the\nservice expects, then adjust "
              "eurostat_trade()/comtrade_trade().")
    return 0


def cmd_collect(a):
    prod = a.product
    rows_out = []
    print(f"Collecting {prod} (CN {CN[prod]} / HS {HS6[prod]}), year {a.year}\n")

    for rep, (name, m49) in EU_MARKETS.items():
        if a.markets and rep not in a.markets:
            continue
        for partner, plabel in (("EXT_EU27_2020", "extra-EU"), ("EU27_2020", "intra-EU")):
            uv = unit_values(eurostat_trade(CN[prod], rep, partner, a.year),
                             a.min_tonnes)
            for u in uv:
                rows_out.append({"source": "eurostat", "product": prod,
                                 "reporter": rep, "reporter_name": name,
                                 "partner": plabel, **u})
            if uv:
                avg = sum(x["eur_per_t"]*x["tonnes"] for x in uv)/sum(x["tonnes"] for x in uv)
                tot = sum(x["tonnes"] for x in uv)
                print(f"  {name:<16} {plabel:<10} {tot:>9,.0f} t  "
                      f"vol-wtd EUR {avg:>8,.2f}/t")

    if not rows_out:
        print("\nNo data. Run --probe to see which source failed and why.")
        return 1

    os.makedirs(a.outdir, exist_ok=True)
    path = os.path.join(a.outdir, f"{prod}_{a.year}_unit_values.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader(); w.writerows(rows_out)
    print(f"\nWrote {len(rows_out)} rows -> {path}")

    tot = sum(r["tonnes"] for r in rows_out)
    wavg = sum(r["eur_per_t"]*r["tonnes"] for r in rows_out)/tot
    print(f"\nVolume-weighted mean across all collected flows: EUR {wavg:,.2f}/t")
    print(f"Total tonnage observed: {tot:,.0f} t")
    print("\nThis is a BORDER unit value, not FOB Rotterdam. Read the caveats "
          "at the top\nof this file before putting it in a business plan.")
    return 0


def cmd_netback(a):
    """FCA Kikinda netback implied by an observed delivered unit value."""
    print("FCA Kikinda netback from an observed delivered unit value\n")
    print(f"  delivered unit value   EUR {a.delivered:,.2f}/t")
    print(f"  inland freight to buyer EUR {a.freight:,.2f}/t")
    print(f"  switching incentive     EUR {a.incentive:,.2f}/t")
    nb = a.delivered - a.freight - a.incentive
    print(f"  ---------------------------------------------")
    print(f"  implied FCA Kikinda    EUR {nb:,.2f}/t")
    print("\n  Compare against Part 7 cash cost before calling this a margin.")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("probe", help="test each source with one request")
    pr.add_argument("--year", type=int, default=date.today().year - 1)
    pr.set_defaults(fn=cmd_probe)

    co = sub.add_parser("collect", help="collect customs unit values")
    co.add_argument("--product", choices=list(CN), default="methanol")
    co.add_argument("--year", type=int, default=date.today().year - 1)
    co.add_argument("--markets", nargs="*", help="e.g. HU AT IT HR SK")
    co.add_argument("--min-tonnes", type=float, default=200.0)
    co.add_argument("--outdir", default="out")
    co.set_defaults(fn=cmd_collect)

    nb = sub.add_parser("netback", help="delivered price -> FCA Kikinda")
    nb.add_argument("--delivered", type=float, required=True)
    nb.add_argument("--freight", type=float, default=45.0)
    nb.add_argument("--incentive", type=float, default=15.0)
    nb.set_defaults(fn=cmd_netback)

    a = p.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
