# Part 5 — CAPEX benchmarking (China) and Own vs Build-Own-Operate

Run: `python3 msk_capex.py`

## What this part answers

Two questions:

1. **"Is there something smarter?"** — yes, and it is a *structure*, not a price:
   buying syngas over the fence from a build-own-operate (BOO) partner instead
   of MSK building and owning the gasification island.
2. **"Research Chinese prices."** — done, with a sourcing caveat that matters.

## Sourcing caveat on Chinese prices

Chinese **vendor listing prices** (Alibaba, Made-in-China, broker pages) are
excluded by the standing sourcing standard in this study, and they would be
useless here regardless: they price components, not installed complexes, and a
gasification island's cost is in alloy vessels, refractory, HP piping, rotating
equipment, instrumentation and erection hours — not in catalogue items.

The reliable Chinese data at this scale is the **published total investment of
announced projects**. Those are facts, but they are *greenfield total
investment*, not EPC-installed cost and not brownfield.

| Project | CNY bn | €m | kt/y | €/annual t |
|---|---|---|---|---|
| Xinjiang Zhongtai (Tianchen EPC) | 5.990 | 779 | 1,000 | 779 |
| **Lishu biomass gasification→MeOH** | **2.557** | **333** | **200** | **1,663** |
| CSSC Tongliao wind-H₂→MeOH | 4.300 | 559 | 320 | 1,748 |
| LONGi Urad Houqi green MeOH | 6.974 | 907 | 400 | 2,268 |

Lishu is the closest comparable (same scale band, same plant shape). Scaled to
177 kt/y at n=0.7 → €305m greenfield-equivalent; less 30–45% brownfield reuse →
**€168–214m**, which brackets the €175–195m EPC figure independently.

It does **not** validate €175–195m as a *funding need*. That remains **€260m**.

## Chinese steel

NBS, mid-September 2026: 20mm HRB400E rebar averaged **CNY 3,182.7/t = €414/t**
— genuinely cheap, and a cyclical trough (mills and CISA curbing output on weak
profitability), not a structural floor. But bulk carbon steel is ~12% of
installed EPC, so a 20% steel swing moves EPC by ~€4m (2.4%). Cheap steel is
real; it is not the lever.

## Own vs BOO

Precedent is established, not speculative: Air Products Syngas Solutions markets
turnkey gasification complexes under a **"Sale of Gas"** model in which it
builds, finances, owns and operates the syngas facility so the customer can
focus its capital and people on its own value-added products (>230 gasifiers
installed; coal gasification since the early 1970s). Precedents include a
build-own-operate coal-to-syngas plant for Jiutai New Material (Hohhot, China)
and the Lu'an project, the first plant 100% owned by Air Products (~US$650m,
Shell gasification technology).

Funding need, MSK side: **€260m → €82m** (€178m, 69%, of capital at risk
removed).

Fully loaded cost per tonne of methanol-equivalent, 20-year annuity basis:

| MSK cost of capital | Own | BOO @10% partner | BOO @12% | BOO @14% |
|---|---|---|---|---|
| 10% | €485/t | €461 (−24) | €473 (−12) | €486 (+1) |
| 12% | €510/t | €469 (−41) | €481 (−28) | €494 (−16) |
| 14% | €535/t | €477 (−58) | €489 (−46) | €502 (−33) |

## Correction

An earlier working version of this comparison reported the BOO advantage on an
unstated capital-charge basis and printed a closing line that contradicted its
own table. This part re-derives everything on one stated basis (annuity capital
charge, 20 years, per tonne of total methanol-equivalent) and supersedes it.

The honest conclusion is narrower than the earlier one: **BOO is not primarily a
cost saving.** At a 10% MSK cost of capital it is roughly neutral per tonne. It
wins on capital at risk and on who carries gasifier availability risk — and the
per-tonne case turns positive exactly to the extent MSK's true cost of capital
exceeds the partner's, which for a first-time Serbian brownfield owner it does.

**The tolling fee is the whole deal and cannot be estimated. It must be bid.**
