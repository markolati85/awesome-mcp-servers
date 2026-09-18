# MSK Kikinda — Founder-Controlled Industrial Investment Structuring Study

Structuring study for the acquisition and modernisation of MSK a.d. Kikinda (methanol / acetic acid complex, Serbia), and for a reusable capital structure for subsequent industrial projects.

## Contents

| File | What it is |
|---|---|
| [`STUDY.md`](./STUDY.md) | The study. Sections A–O plus the multi-project structure and the final decision exercise |
| [`MODEL-OUTPUTS.md`](./MODEL-OUTPUTS.md) | All 15 model tables. Every number in the study traces here |
| [`TERM-SHEET.md`](./TERM-SHEET.md) | Two-page non-binding indicative term sheet |
| [`model/msk_model.py`](./model/msk_model.py) | The model: project cash flows, debt sizing, waterfall, call-option pricing |
| [`model/build_outputs.py`](./model/build_outputs.py) | Generates `MODEL-OUTPUTS.md` |

## Reproducing the numbers

```bash
python3 docs/msk-kikinda/model/build_outputs.py
```

No dependencies beyond the Python 3 standard library.

## The three conclusions

1. **The binding constraint is not the ownership split — it is whether €200m of capex buys €40m+ of EBITDA.** Capex uncertainty is worth roughly four times the entire ownership negotiation.

2. **No private-equity investor will take this at any split.** Achievable investor IRR is ~11.7%; PE hurdles are 18–22%. The compatible universe is infrastructure funds, family offices, commodity traders with an offtake motive, strategics, DFIs and ECA-backed Chinese industrial capital.

3. **An IRR-ratchet founder call option is a trap.** It gets more expensive every year, prices the investor's stake at a 60–75% premium to fair value, is never fundable by refinancing, and *destroys* founder wealth. The protection the founder actually wants is a **cap on the investor's money multiple**, exercised late.

## Health warning

The operating assumptions — €200m capex, €46m full-ramp EBITDA — are the modelling inputs the study was asked to use. **Neither has been validated by any engineering study.** Section J sets out why a gas-fed refurbishment may earn materially less, and Table 12 shows how the structure behaves when the assumption is wrong. Commission the engineering study before using any number here in a negotiation.
