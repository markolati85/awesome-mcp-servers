# Part 8 — Hard-evidence price collector

```bash
python3 msk_prices.py probe --year 2025          # test the sources first
python3 msk_prices.py collect --product methanol --year 2025 --markets HU AT IT HR SK
python3 msk_prices.py collect --product acetic_acid --year 2025
python3 msk_prices.py netback --delivered 520 --freight 45
```

## Why this instead of a subscription

A price assessment (IHS / S&P / ICIS / Argus) is a **judgement** about where a
market is. Customs data is a **record of what was actually paid** — declared to a
government by the importer, under penalty for misdeclaration.

For a business plan and for a lender's diligence the second is the stronger
evidence, and it has one property no subscription has: **the lender can verify it
themselves, for free, forever.** A number you can hand someone with "here is the
query, run it yourself" survives diligence differently from a number whose source
you are contractually forbidden to redistribute.

It is also the right *shape* for this project. Part 4 turned on **Central Europe
delivered parity** — what an imported tonne costs at the buyer's gate in
Budapest, Vienna, Bratislava, Zagreb or northern Italy. Eurostat reports exactly
that: monthly, by CN8 product, **by reporter and partner country**. No assessment
service publishes that pairing.

And note what MSK's own projection shows: it used **IHS forecasts of €340–350/t**
methanol for 2026. The spike ran to €830–915/t. The forecast was not the valuable
part of that subscription. Hard transaction data is — and it is free.

## What this does not do

It does not touch any paywalled or subscription service. Every source publishes
openly; nothing here circumvents a login or an access control. Scraping S&P or
IHS was considered and rejected — besides the terms-of-use problem, a business
plan resting on data you are not licensed to redistribute fails diligence at the
first question about provenance.

## Sources

| Source | What it gives | Role |
|---|---|---|
| **Eurostat Comext** | EU trade by CN8, monthly, reporter × partner | **primary** |
| **UN Comtrade** | global HS6, free preview tier | non-EU reporters (Serbia, Türkiye) |
| Methanex posted | public regional reference price | measures the posted-to-actual gap |

Product codes: methanol **CN 2905 11 00 / HS 290511**; acetic acid
**CN 2915 21 00 / HS 291521**.

## Caveats — read before quoting any number this produces

- A unit value is `declared value / declared mass`: an **average** over a month
  and a country pair, mixing contract and spot, grades and package sizes.
- EU **import** values are at the border (CIF-type); **export** values are
  FOB-type. **A unit value is not comparable to FOB Rotterdam without
  adjustment.** This is the mistake most likely to produce a wrong business plan.
- Thin flows produce wild unit values. `--min-tonnes` filters them, default 200 t.
- Trade data lags roughly 2–3 months.
- Re-exports and transit distort a partner pairing — Rotterdam especially.

## Status: the live calls are untested

The session that wrote this had `ec.europa.eu`, `comtradeapi.un.org` and
`www.methanex.com` blocked by its network egress policy, so **the HTTP paths have
never executed successfully**. The offline logic (JSON-stat flattening, unit-value
pairing, netback) is exercised and works.

The code is built for this: every request prints the exact URL it calls, and a
non-JSON response is written to `.cache/*.raw.txt` with the first 400 characters
shown. `probe` tests each source with one minimal request and tells you which
failed. If a parameter name has changed, open the printed URL in a browser — the
service will say what it expects — then adjust `eurostat_trade()` or
`comtrade_trade()`.

Run `probe` first. Do not trust a `collect` run that you have not probed.
