# Part 7 — Rebuilt on MSK's own projection

Run: `python3 msk_actuals.py`

**Source:** `Projekcija za 2026 23.04.2024.xlsx`, sent by Mirko Latinović, acting
General Manager of MSK a.d. Kikinda, 23.04.2024, plus the covering e-mail
"Prirodni gas" of 09.04.2024. This is the operator's own document, tagged
`[FACT-MSK]` throughout.

## What the plant actually is

| | Value |
|---|---|
| Nameplate | **200,000 t/y methanol, 100,000 t/y acetic acid** (330 days) |
| Utilisation in plan | 93% / 92% |
| Methanol produced | 186,390 t/y |
| — own use into AcOH | 49,864 t/y (0.54 t per t AcOH, operator's own ratio) |
| — **sold** | **136,526 t/y** |
| **Acetic acid** | **92,340 t/y** |
| Natural gas | **301,952,000 m³/y** = 1,620 m³ per t methanol |

Parts 3–6 of this study assumed 150,000 t merchant methanol + 50,000 t acetic
acid. **Acetic acid is actually +85% larger than assumed** — and at €629/t
against methanol's €341/t it is the high-value product. Every earlier revenue
figure understated the plant.

## Why it is shut — the operator's own arithmetic

| | € |
|---|---|
| Revenue | 105,311,883 |
| Operating costs | 177,437,060 |
| **Result** | **−72,125,178** |
| of which natural gas | 141,978,286 — **80% of all operating cost** |
| cash opex ex-gas | 33,402,806 |
| depreciation | 2,055,968 |

MSK's own stated break-even: liquidity at **$253.74/1000 m³**, profitability at
**$246.48/1000 m³**, against **$501/1000 m³** in the projection. The plant needs
gas at roughly **half** the price it can buy it for.

The thesis that gas is why this plant does not run is now arithmetic, not opinion.

## The 15 MW turbine

The plant buys only **€540,000/y of electricity** — the existing steam turbine
carries the load off process steam. **Part 6 of this study assumed €17.7m/y of
imported power. That was its single biggest error.**

On petcoke the steam must come from gasifier waste heat instead, which makes the
waste-heat boiler **mandatory**, not optional — the opposite of the China
red-team's "quench, skip the RSC" advice. Sizing the WHB and turbine is now the
highest-value engineering decision in the project:

| Steam case | Turbine | Net import | Installed | EBITDA @475/600 | Payback |
|---|---|---|---|---|---|
| quench, no WHB | 4 MW | 32 MW | €235m | €17.5m | 16.2y |
| **existing turbine** | **15 MW** | **21 MW** | **€255m** | **€24.3m** | **12.5y** |
| turbine uprated | 26 MW | 10 MW | €277m | €31.1m | 10.4y |
| full self-sufficiency | 36 MW | 0 MW | €297m | €37.2m | 9.3y |

Every euro spent on steam integration pays back faster than the plant as a whole.

## The comparison that matters

At identical product prices (MeOH €475, AcOH €600):

| | Gas today | Petcoke |
|---|---|---|
| Revenue | €120.3m | €120.3m |
| Feedstock | €142.0m | €36.3m |
| Other cash opex | €33.4m | €59.7m |
| **EBITDA** | **−€55.1m** | **€24.3m** |

**The feedstock bill falls from €142m to €36m — a €106m/y swing.** That is the
investment case. It was never the price of methanol.

## Corrections this part forces

1. **The acetic acid catalyst is rhodium, not iridium.** The projection lists
   rhodium 1.163 g/t at €7.444/g plus an iodide promoter — this is the
   **Monsanto** process. Earlier parts of this study said Cativa/iridium. Wrong.
   Rhodium make-up is ~107 kg/y ≈ €0.8m/y; the reactor inventory is a separate
   working-capital item that has not yet been sized.
2. **Part 6's power cost was wrong** (see above).
3. **The slate was wrong** in Parts 3–6 (see above).
4. Petcoke requirement rises from 270 kt/y to **313 kt/y** on the real slate,
   and vented CO₂ to **588 kt/y** — which makes the CO₂ change-in-law exposure
   from Part 6 larger, not smaller.

## Still outstanding

The attachments `msk-sc-2113-0001.pdf` (gas technical specification) and
`Pregled cena gasa MART 2020 – FEBRUAR 2024.pdf` (five years of actual purchase
prices) could not be read — this session has no Gmail attachment download tool
and they are not in Drive. The five-year price history in particular would let
the gas-vs-petcoke switching option be valued properly rather than assumed.
