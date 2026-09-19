# MSK Kikinda — feedstock, gasification and production-cost model

Gate-to-tonne engineering economics for methanol and acetic acid at MSK Kikinda.
Companion to the capital structuring study in the parent directory.

```bash
python3 docs/msk-kikinda/feedstock/msk_feedstock.py   # importable; see run_all()
```

Stdlib only. Every number in the study PDF is produced here.

## What it does

Builds a first-principles **carbon balance** from feedstock gate to one tonne of
saleable methanol, then to one tonne of acetic acid:

- 1 t methanol contains 374.8 kg carbon; 1 t acetic acid contains 400.0 kg
- Carbon efficiency: ~77.5% for steam reforming, ~32.5% for entrained-flow coal
  gasification (H2-poor syngas forces a shift that vents CO2), ~30% biomass, ~26.5% RDF
- Feed quantity therefore falls out of the balance rather than being assumed

Then layers utilities, oxygen, labour, maintenance, ash disposal, capital recovery
and CO2, and reports cash cost and fully loaded cost per tonne.

## Provenance discipline

Every input carries a tag and the code says which:

| Tag | Meaning |
|---|---|
| `FACT` | sourced and cited |
| `VENDOR` | licensor/supplier claim, not independently verified |
| `ENG` | engineering estimate derived here from first principles or standard practice |
| `ASSUM` | model assumption, no external basis, varied in sensitivity |

**No price in this model is a quotation.** Where a firm price was unavailable a
LOW/BASE/HIGH band is used and its derivation is stated in a comment.

## Headline results (200 kt/y, €100/MWh power, €38/MWh gas, BASE feed band)

| Route | t feed / t MeOH | €/GJ | New capex | Cash €/t | Full €/t | t CO2/t |
|---|---:|---:|---:|---:|---:|---:|
| Natural gas | — | 10.56 | €115m | 423 | 490 | 0.50 |
| Captive Kovin lignite | 3.94 | 1.53 | €353m | **322** | 537 | 3.47 |
| Purchased Kostolac | 4.34 | 2.43 | €353m | 361 | 577 | 3.47 |
| Imported bituminous | 1.70 | 4.98 | €326m | 439 | 634 | 3.28 |
| Agricultural biomass | 3.12 | 5.43 | €432m | 520 | 800 | 3.85 |
| Prepared RDF/SRF | 3.37 | 1.56 | €551m | 450 | 845 | 4.62 |

## The finding

Serbian lignite is genuinely cheap energy (€1.53/GJ against €10.56/GJ for gas) and
gives the lowest cash cost of any route. It still loses, because converting MSK to
solid feed costs ~€353m against a 200 kt/y plant — **€1,767 of new capital per
annual tonne**, adding €216/t of capital charge to save €101/t of cash cost.
Simple payback 17.5 years. At 1,500 kt/y the full cost is still €358/t.

Coal gasification at MSK fails on **scale and capital intensity**, not on gasifier
performance — so modern Chinese technology, however good, does not change the
answer. Entrained-flow gasifiers also need <5% moisture feed or a pumpable slurry;
Serbian lignite at 39–50% moisture provides neither.

At €100/t CO2 the lignite route moves from cheapest (€322) to €669/t.
