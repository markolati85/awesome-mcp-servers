# Part 11 — Which feedstock is actually cheapest (September 2026)

**Question:** what is the cheapest feedstock in the world for MSK, reusing as much
of the existing plant and the 15 MW steam turbine as possible, landed at Port of
Bar and railed to Kikinda?

Run it:

```
python3 msk_feeds.py            # full comparison
python3 msk_feeds.py volume     # can you actually buy the tonnage?
python3 msk_feeds.py turbine    # the turbine question, answered
python3 msk_feeds.py switch     # the gas-vs-petcoke switching price
```

No dependencies. Stdlib only.

---

## The answer

**Petroleum coke, and it is not close** — on the metric that decides it, delivered
cost of energy:

| Feedstock | €/t delivered | GJ/t | **€/GJ** | × petcoke |
|---|---:|---:|---:|---:|
| RDF / SRF (a gate fee, not a price) | −10 | 16.0 | **−0.62** | — |
| **Petroleum coke, fuel grade, via Bar** | **115** | **32.5** | **3.54** | **1.00×** |
| Sunflower husk pellets, Vojvodina | 82 | 16.5 | 4.97 | 1.40× |
| Torrefied straw / corn stover, Vojvodina | 130 | 20.0 | 6.50 | 1.84× |
| Imported steam coal 6,000 kcal, via Bar | 167 | 25.1 | 6.65 | 1.88× |
| Refinery vacuum residue, regional | 400 | 39.0 | 10.26 | 2.90× |
| High-sulphur fuel oil 3.5% | 555 | 40.2 | 13.81 | 3.90× |
| **Natural gas (TTF €79.52/MWh)** | 1,104 | 50.0 | **22.09** | **6.24×** |

Natural gas now costs **six times** what petcoke costs per gigajoule. That single
ratio is the whole case for converting this plant.

---

## But every route still destroys value

Same carbon requirement, same product slate, each route carrying its own capital:

| Feedstock | t/y feed | feed €/t | other €/t | capital €/t | **ALL-IN €/t** | EBITDA €m/y |
|---|---:|---:|---:|---:|---:|---:|
| RDF / SRF | 588,417 | −25 | 350 | 171 | **496** | 37.6 |
| **Petcoke** | **237,149** | 117 | 342 | 138 | **597** | **6.4** |
| Sunflower husk | 446,974 | 158 | 345 | 151 | 654 | −3.7 |
| Steam coal | 316,320 | 227 | 344 | 146 | 717 | −19.6 |
| Torrefied straw | 395,400 | 221 | 353 | 181 | 755 | −20.2 |
| Vacuum residue | 240,477 | 414 | 330 | 93 | 837 | −59.8 |
| HSFO | 240,477 | 575 | 330 | 93 | 998 | −97.1 |
| Natural gas | 216,198 | 1,028 | 144 | 82 | 1,255 | −159.1 |

**Revenue on the same basis is €487/t** (methanol €470, acetic acid €530, FCA
Kikinda, Part 8 traded basis).

Nothing clears it. The best purchasable feedstock on earth lands at **€597/t
against €487/t of revenue**. Petcoke turns EBITDA positive — €6.4m/y — and then
a €273m funding requirement takes €32.1m/y of capital charge out of it.
**Net −€25.6m/y.**

The only row that comes close is the one with a *negative* feedstock price, and
you cannot buy 588,000 t/y of it.

---

## What Part 11 corrects in Parts 3–10

1. **Liquid residue through the existing POX was never priced properly.** Part 3
   modelled heavy residue only with electrolytic hydrogen (route R4), which loaded
   it with 5.9 MWh/t of electrolysis and buried it. MSK's U-13 is natively a
   liquid-feed gasifier, so that was the wrong comparison. Priced correctly here —
   **and it still loses**, not on capital but on the feedstock: HSFO is
   **$529/t fob Rotterdam** (7 Sep 2026). The cheapest conversion in the study
   feeds the most expensive solid-or-liquid carbon in the study.

2. **The turbine was credited at nameplate.** Earlier drafts of this part took the
   full 15 MW. Part 9 caps recoverable HP steam at 60–75 t/h, which is 7.0–8.8 MW
   of back-pressure work plus 2–3 MW from a condensing tail on the surplus.
   Corrected to **10 MW delivered against a 15 MW plate** — this flattered the
   project by about €6m/y.

3. **Power was priced at €85/MWh (Part 6) and €140/MWh (this part's first pass).**
   Serbia's SEEPEX baseload traded **€109–183/MWh** through September 2026.
   Corrected to €160/MWh. Power is now **€142/t of product — the second largest
   cost line after the feedstock itself.**

---

## The turbine question, answered

**Refurbish it. Do not specify a bigger one.**

On gas the turbine carries the entire plant — MSK buys only €540,000/y of
electricity [FACT-MSK]. On petcoke that breaks, for two reasons at once:

- **The load goes up.** An air separation unit appears that was never there:
  225,291 t/y of oxygen at 0.30 MWh/t is **8.5 MW**, inside a ~36 MW total load.
- **The steam goes down.** The gasifier raises 60–75 t/h of HP steam, not the
  110–125 t/h a supplied model booked (Part 9).

So the 15 MW machine is **already big enough** — it is fed by steam that tops out
at about 10 MW of work. **Uprating it buys nothing, because the steam is the
constraint, not the machine.**

**The lever is the load, not the generation.** About 8.5 MW of the 36 MW load is
the ASU alone: €10.8m/y of electricity and an estimated €60–80m of capex
[ENG/RFQ]. Oxygen over the fence — Messer, Linde or Air Liquide build, own and
operate the ASU on site and sell oxygen by the tonne — takes both off MSK's books.

**This is not the build-own-operate structure the owner rejected.** That rejection
was about keeping control of the *feedstock*. An oxygen contract does not touch
the feedstock: the gasifier, the feed system and every tonne of coke, coal,
residue or gas going into it stay wholly MSK's. It locks a **utility**, not a
feed — which is exactly why it is the one thing that can be de-scoped without
losing optionality.

---

## The switching price — what feedstock optionality is actually worth

| | TTF €/MWh | USD/1,000 m³ |
|---|---:|---:|
| Today (18 Sep 2026) | 79.5 | 843 |
| The operator's own 2026 projection | 47.3 | 501 |
| **Before FID: gas beats petcoke below** | **28.7** | **304** |
| **After FID: gas beats petcoke on cash below** | **24.4** | **259** |

Gas must fall to about **36% of today's price** before building the petcoke island
stops making sense. Once it is built, gas must fall to about €24/MWh before it is
worth idling a paid-for asset.

**Cross-check:** that $259/1,000 m³ is derived here from first principles.
MSK's own projection states a cash break-even of **$253.74**. Two independent
routes, 2% apart.

The honest case for dual-feed is therefore **not** that you will switch often.
It is that keeping the gas train alive costs almost nothing — it is already
there — and it removes the single-supplier exposure that shut this plant down.

---

## Volume: a price you cannot buy 400,000 t/y of is not a price

| Feedstock | needed t/y | sourceable t/y | cover | |
|---|---:|---:|---:|---|
| Petcoke / HSFO / coal | 237–316k | world market | — | ok |
| Vacuum residue, regional refineries | 240,477 | 400,000 | 1.66× | OK |
| Torrefied straw / corn stover | 395,400 | 1,500,000 | 3.79× | OK |
| **Sunflower husk pellets** | 446,974 | 100,000 | **0.22×** | **FAILS** |
| **RDF / SRF** | 588,417 | 150,000 | **0.25×** | **FAILS** |

**Sunflower husk looks cheap and is not available.** Serbia's entire sunflower
crop is ~454,000 t of seed [FACT]; husk is ~22% of that, so ~100,000 t/y exists
*nationally* — and the oil mills already burn most of it for their own steam.
It is a **co-feed at best, never the base load.**

**RDF is blocked twice over.** EU waste cannot legally be shipped to Serbia for
recovery after **21 May 2027** unless Serbia is added to the EU authorised-country
list (first list due 21 Nov 2026) — so the feedstock's legality would rest on an
administrative decision MSK does not control, which is the opposite of
optionality. Chlorine in RDF also poisons methanol synthesis catalyst.

---

## The one number here I do not trust

Every petcoke figure descends from an Argus fob USGC print of **$54.90/t for
Q4 2025**. Since then the US–Iran war has taken TTF from roughly €27 to
€79.52/MWh, API2 coal to about $145/t and 3.5% fuel oil to $529/t — all [FACT].

Fuel-grade petcoke competes with coal in cement kilns and power stations. **It
will not have stayed at $55 while coal went to $145.** The September-2026 Argus
assessment is paywalled and this session cannot reach it.

So the **ranking** is robust — petcoke moves with coal, and coal is still far
below oil and gas per GJ. But the **margin** in the all-in table is overstated by
an unknown amount, and the all-in number is already €110/t underwater.

**One phone call to a petcoke trader fixes this.** Ask for fob USGC 6.5% S
40 HGI, and separately for a high-sulphur **shot coke** offer — which is what a
gasifier should actually be buying, and what nobody else can use.

---

## Provenance

| Tag | Meaning |
|---|---|
| `[FACT]` | published or observed |
| `[FACT-MSK]` | the operator's own document |
| `[ENG]` | engineering estimate |
| `[ASSUM]` | model assumption |
| `[RFQ]` | requires a vendor quote |
| `[LIST]` | a listing, not a transaction |

Observed inputs, September 2026:

- TTF natural gas **€79.52/MWh**, 18 Sep 2026
- HSFO 3.5% fob Rotterdam barges **$529.00/mt**, 7 Sep 2026
- API2 steam coal cif ARA **~$145/t**, mid-Sep 2026
- Serbia SEEPEX baseload **€109–183/MWh** through Sep 2026
- Serbian sunflower seed crop **454,282 t**
- Sunflower husk pellets **€67/t EXW bulk**, Čantavir — `[LIST]`, a listing
- Petcoke fob USGC 6.5% S **$54.90/t, Q4 2025** — **pre-war, see above**

No price in this model is a quotation.
