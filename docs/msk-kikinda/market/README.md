# MSK Kikinda — market intelligence and realizable price model

Answers the commercial question the engineering studies could not: **what price can
MSK actually get, from whom, and how much money does that make?**

The axis is **Central Europe delivered parity** — not "what is Rotterdam", but what an
imported tonne costs *delivered to a buyer's gate* in Budapest, Vienna, Bratislava or
Zagreb, and what FCA Kikinda netback MSK can take underneath it.

```bash
python3 -c "import sys;sys.path.insert(0,'docs/msk-kikinda/market');from msk_market import *;print(weighted_netback(450.0))"
```

Tags: `FACT` (sourced) / `EST` (estimate) / `PROXY`. **No price here is a quotation.**

## Two findings that change the commercial case

**1. Today's price is a war, not a market.** European methanol went €535/t (Q1 2026) →
€850 (Q2) → €915 (Q3). [FACT] That is the Strait of Hormuz closure and the US–Iran
conflict: EU imports fell 76.4% from Saudi Arabia and 92.7% from Oman in Jan–May 2026.
**Do not set a 10-year contract price, or an FID, against €830–915/t.**

**2. The freight moat is ~€14/t, not ~€60/t.** Price the competitor's import through the
*Mediterranean* (Trieste, Koper, Constanța, Thessaloniki) rather than Rotterdam and the
advantage collapses. Worth ~€2.2m/y against a production-cost advantage of €20.7m/y at
mid-cycle. **The geography is worth about one tenth of the chemistry.**

## Delivered parity, Rotterdam €450/t mid-cycle

| Market | Competitor delivered | MSK FCA netback | Moat |
|---|---:|---:|---:|
| Serbia | 511 | 474 | **+24** |
| Hungary | 511 | 468 | **+18** |
| S. Poland | 532 | 463 | **+13** |
| Slovakia | 516 | 462 | **+12** |
| Austria | 511 | 458 | +8 |
| Czechia | 522 | 452 | +2 |
| Bulgaria / Croatia / Romania / Slovenia | — | — | −1 to −17 |
| N. Italy / Greece | 501 / 488 | 421 | **−29** |

Six markets carry a positive moat; six do not. **Do not chase northern Italy or Greece.**

## Scenarios (EBITDA contribution, 150 kt methanol + 50 kt acetic acid)

| Scenario | Rotterdam | MSK FCA | Acetic acid | Total |
|---|---:|---:|---:|---:|
| Severe downcycle | 300 | 314 | 400 | €0.8m |
| Conservative | 380 | 394 | 470 | €16.3m |
| **Base / mid-cycle** | **450** | **464** | **520** | **€29.3m** |
| Strong market | 600 | 614 | 580 | €54.8m |
| Current Sep 2026 (war spike) | 830 | 844 | 561 | €88.3m |

**Plan on €29.3m. Stress at €0.8m.** Breakeven Rotterdam price: **€298/t**.

## Benchmark to index to

[FACT] Platts launched a monthly **net** contract price for European methanol
(**MTFRE03**, €/mt FOB Rotterdam) on 3 Nov 2025, averaging daily month-ahead FOB
Rotterdam spot, because of market concern over contract/spot divergence — and in May
2026 proposed discontinuing the industry-settled quarterly **gross** ECP.

**Index to MTFRE03 or Platts FOB Rotterdam spot. Never to Methanex posted**, which is a
list price set by one producer, carries undisclosed discounts, and is being abandoned as
a settlement reference.

## Largest sources of error

Inland chemical freight, market sizes and the €15/t switching incentive are all `EST`.
The moat is only €14/t, so a €10/t freight error halves it. Rail tank-car tariffs from
Kikinda are the single most valuable number still missing.
