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

## Re-running with real numbers

When the Tianchen / Hualu engineering work lands, re-run the recommended structure against
the actual capex and EBITDA instead of the placeholders:

```bash
python3 docs/msk-kikinda/model/msk_model.py --capex 260 --ebitda 38 --senior-pct 0.55
```

It prints the capital stack, minimum DSCR, investor IRR/MOIC, the call price and whether it
can be funded, founder wealth at Y5/Y10/Y15, and — most usefully — **the maximum economic
share the founder can defend at that leverage for each investor hurdle rate**:

```
      investor needs 10%  ->  founder can hold 69%
      investor needs 12%  ->  founder can hold 58%
      investor needs 14%  ->  founder can hold 45%
```

`--help` lists every input. This is the tool that replaces arguing about percentages with
computing them.

## The three conclusions

1. **The binding constraint is not the ownership split — it is whether €200m of capex buys €40m+ of EBITDA.** Capex uncertainty is worth roughly four times the entire ownership negotiation.

2. **No private-equity investor will take this at any split.** Achievable investor IRR is ~11.7%; PE hurdles are 18–22%. The compatible universe is infrastructure funds, family offices, commodity traders with an offtake motive, strategics, DFIs and ECA-backed Chinese industrial capital.

3. **An IRR-ratchet founder call option is a trap.** It gets more expensive every year, prices the investor's stake at a 60–75% premium to fair value, is never fundable by refinancing, and *destroys* founder wealth. The protection the founder actually wants is a **cap on the investor's money multiple**, exercised late.

## Corrections log

Claims withdrawn or materially revised after review, and why:

| Withdrawn | Replaced with |
|---|---|
| "No private-equity investor will take this at any split" | Too categorical. There is no universal hurdle per investor category; managers price deal by deal. Reframed as a conditional statement about *this risk profile*, which changes if the engineering de-risks the project. |
| DFIs listed against a "10% IRR" hurdle | EBRD and IFC publish no such tariff. EBRD takes minority equity for an "appropriate return", structured project by project; IFC typically takes 5–20% of project equity. They are a slice of the stack, not an €80m silent partner. |
| "The founder must have independent income for eight years" | Conflated distributions with compensation. ProjectCo should pay benchmarked market-rate executive compensation as ordinary opex, agreed in the SHA at signing. Only the *equity value* is near zero at Year 5. |
| Stress tests that re-sized debt to the stressed cash flow | Fixed: the capital structure is now held constant across all stress scenarios, which is what a stress test means. |

## Health warning

The operating assumptions — €200m capex, €46m full-ramp EBITDA — are the modelling inputs the study was asked to use. **Neither has been validated by any engineering study.** Section J sets out why a gas-fed refurbishment may earn materially less, and Table 12 shows how the structure behaves when the assumption is wrong. Commission the engineering study before using any number here in a negotiation.
