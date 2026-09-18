# MSK Kikinda — zero-feed / ultra-low-cost syngas screen

Open technology screen: ten architectures for supplying MSK with CO + H2 without
expensive pipeline natural gas. Stdlib only.

```bash
python3 -c "import sys;sys.path.insert(0,'docs/msk-kikinda/syngas');from msk_syngas import *;print(run(ROUTES[1],80)['cash'])"
```

## Correction to the earlier feedstock study

That study modelled MSK as a **steam reforming** plant at 200 kt/y methanol + 100 kt/y
acetic acid. Both were wrong. MSK's own technical description confirms a
**partial-oxidation (POX)** unit with COSORB stripping CO from the POX syngas. A POX
gasifier is natively a heavy-feed machine — the same family that gasifies petroleum
coke and refinery residue — so the economics of switching feedstock are materially
better than previously reported.

## Integrated production balance

| Stream | t/y |
|---|---:|
| Merchant methanol | 150,000 |
| Methanol consumed making acetic acid | 27,085 |
| **Total methanol** | **177,085** |
| Acetic acid | 50,000 |
| CO required | 24,810 |

Per tonne of methanol: 374.8 kg carbon and 125.8 kg H2 (CO + 2H2 → CH3OH).

## Corrections (September 2026) — three material errors, all in the project's favour

| Withdrawn | Replaced with |
|---|---|
| Petcoke at €155/t delivered (base) | **€105/t**. Built up from a real logistics chain: FOB USG **$65.49/t Q3 2026** (Argus fell below $80 on 3 Jun), *less a high-S / low-HGI / high-metal discount a gasifier can uniquely accept*, plus a Supramax COA to the Adriatic, direct ship-to-wagon and a unit train to MSK's own siding. Four errors were found: FOB anchored on April not current, the off-spec discount missed entirely, rail over-priced, and a handling step plus a road leg double-counted. |
| CBAM at €75/tCO₂ applied to MSK | **€0/t for these products today.** Serbia's CO₂ tax applies from 1 Jan 2026 at €4/t but the obligated parties are cement, fertilizers, iron & steel, aluminium and electricity — **methanol and acetic acid are not covered** — and EU CBAM does not cover them either. EU ETS *does* cover acids and bulk organic chemicals, so the same plant inside the EU would pay. This made the petcoke route look ~€290/t worse than it is. |
| Methanol at €350/t | **€827–915/t.** Methanex European Posted Contract Price 2026: Q1 €535, Q2 €850, Q3 €915; Q2 realised at €827/t FOB Rotterdam, only ~3% below posted. Every margin in the earlier work was understated. |

**Net effect:** methanol cash cost falls from €386/t to **€312/t**, and against a market at €827/t the merchant margin is ~€515/t, not the ~€0 the earlier numbers implied.

## Two structural points added since

- **Petcoke is a long position on European gas.** European methanol is priced off gas-fed marginal supply while a petcoke cost base is flat. Margin on 150 kt/y merchant methanol: ~€84m at today's prices, ~€43m if gas normalises to €40/MWh, ~€10m if gas falls to €18/MWh. Downside bounded, upside currently extraordinary.
- **This is a payback-window play, not a permanent cost advantage.** At €118/tCO₂ the petcoke advantage over gas reaches zero; the EU is already at ~€86. You need roughly six years at Serbia's current treatment to cover €250m of capex. The bypassable shift and pre-flanged H₂/O₂ tie-ins are the exit, not a nicety.

## Results (cash cost €/t methanol)

| Route | Bucket | €80/MWh grid | €20/MWh PPA | New capex |
|---|---|---:|---:|---:|
| R1 Natural gas POX ($505/1,000 Nm³) | A | 647 | — | €115m |
| **R2 Petcoke via existing POX** | **A** | **312** | — | **€165m** |
| R3 Petcoke + electrolytic H2 | B | 705 | 337 | €310m |
| R4 Refinery residue + H2 | B | 566 | 322 | €285m |
| R6 Point-source CO2 + H2 | B | 785 | 362 | €340m |
| R7 DAC CO2 + H2 ("from air") | C | 1,464 | 1,042 | €600m |
| R8 SOEC co-electrolysis | C | 680 | 354 | €460m |

## Findings

- **R2 is the bankable answer**: €386/t cash vs €647/t on gas — €46m/y saving on
  €165m capex, **3.6-year payback**, no power project required.
- **Acetic acid on gas is loss-making** at $505/1,000 Nm³ (€573/t marginal vs €560
  market). On petcoke it earns +€224/t. That is the real urgency.
- **Electrolysis converts a feedstock problem into a power-price problem.** R2 moves
  only €63/t across €10–100/MWh; every H2 route moves €400–600/t. R3 beats R2 only
  below ~€25/MWh, and needs 136 MW continuous / 1.09 TWh/y — 2.7% of Serbia's
  electricity consumption.
- **"Methanol from air" is dead**: DAC feedstock alone costs €720/t of methanol.
  With point-source CO2 instead of air the same chemistry reaches €300/t at €11/MWh.
- **On the Serbian grid, electrolytic H2 raises emissions** (4.4 t CO2/t vs 3.8 for
  plain petcoke) because grid power is lignite-heavy. The power contract *is* the
  architecture.
- **Gas beats petcoke again below ~$260/1,000 Nm³** — and $200–230 is exactly what
  the company says it needs. Exhaust the gas negotiation before spending capital.
