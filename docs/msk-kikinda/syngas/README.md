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

## Results (cash cost €/t methanol)

| Route | Bucket | €80/MWh grid | €20/MWh PPA | New capex |
|---|---|---:|---:|---:|
| R1 Natural gas POX ($505/1,000 Nm³) | A | 647 | — | €115m |
| **R2 Petcoke via existing POX** | **A** | **386** | — | **€165m** |
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
