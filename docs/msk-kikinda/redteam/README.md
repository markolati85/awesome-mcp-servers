# Part 9 — Independent red-team of the integrated investment case

Reviews `MSK_Final_Business_Model_2026.xlsx`, `MSK_Final_Investment_Case_2026.pdf`
and two prior power-island studies. The Excel was **not** treated as source of
truth; every load-bearing number was recomputed from first principles.

## Four findings, in order of size

### 1. The HP steam recovery is physically impossible — **fatal to architectures D and E**

The model books 110 t/h (arch. D) and 125 t/h (arch. E) of recovered HP steam.

Heat balance, 277 kt/y petcoke at 30 MJ/kg = **288 MWth** input. At 73% cold-gas
efficiency the syngas carries 210 MWth away as chemical energy, leaving **78 MWth**,
of which ~7 MWth is ambient loss and slag. Making 1 t/h of 100 bar/540 °C steam
from 105 °C BFW needs 0.84 MWth.

| | MWth needed | available |
|---|---|---|
| 110 t/h | **93** | ~71 |
| 125 t/h | **105** | ~71 |

**The physical ceiling is ~60–75 t/h with full RSC+CSC.** Architectures D and E
do not exist. Everything downstream of them — the new extraction turbine, the
5 MW export, the near-zero utility gas bill — falls with them.

### 2. Net grid import of 2 MW is wrong by ~18 MW — **€19m/y**

Even granting the model its own 110 t/h, the shaft work is bounded by the
enthalpy drop. 104 t/h through a back-pressure/extraction let-down from 100 bar
to the ~12 bar process header at ~420 kJ/kg gives **~13 MW**, not the ~30 MW
implied. Against a 32 MW load the net import is **~19 MW**, not 2 MW.

At €130/MWh that is **€19m/y of electricity the model does not pay for** — most
of the gap between its €28.3m EBITDA and a defensible number.

*This also corrects my own first pass, which counted only surplus steam as
generating power. Steam does work on its way to the process header whether it
turns a generator or a compressor.*

### 3. Carbon utilization of 40% is **too low** — this one favours the project

Acetic acid takes its CO **directly**; that carbon is never shifted. Methanol
carbon must be, and every mole of H₂ made by shift destroys a mole of CO.

From first principles on 88% C petcoke:

| slate | ideal | with ~7% losses |
|---|---|---|
| methanol only | 37–43% | 35–40% |
| **acid-max (132/100)** | **44–50%** | **41–46%** |

**40% is conservative for an acid-rich slate.** My own Parts 5–7 used 35.8% —
carried over from a methanol-only coal case — and that was wrong here. Correcting
it cuts petcoke from 277 to ~241 kt/y and adds ~€5m/y.

### 4. The 70 MW gas-turbine study is unusable

A 50 MW gas turbine on syngas at 33% efficiency needs **152 MWth = 72% of all the
syngas the gasifier makes**. The same document says its 200 kt/y petcoke is
"sufficient for the existing methanol/acetic acid capacity". It cannot be both.
Burning ~70% of the syngas leaves ~56 kt/y methanol instead of 186 kt/y —
destroying ~€91m/y of chemical revenue to earn €57m/y of electricity.

It then cuts its CO₂ bill from €42.5m/y to €4.25m/y with 90% carbon capture and
adds **zero CAPEX** for the capture plant (realistically €150–300m+). Its
2.3-year payback is an artefact of that omission.

## Rebuilt result

| Scenario | Petcoke kt/y | EBITDA €m | IRR | NPV@12% €m |
|---|---|---|---|---|
| Excel arch. D as published | 277 | 28.3 | 3.5%* | −145* |
| turbine physics corrected | 277 | **10.9** | −5.1% | −236 |
| + steam capped at 75 t/h | 277 | 1.1 | −18.4% | −290 |
| + C-util 46% | 241 | 7.2 | −8.3% | −256 |
| + Part 8 traded prices (471/561) | 241 | 18.7 | −0.2% | −193 |
| + petcoke via Bar €116/t | 241 | 27.0 | 3.1% | −154 |
| + CAPEX €240m | 241 | 27.0 | 4.8% | −110 |
| **best defensible: CAPEX 225, petcoke 110** | 241 | **28.4** | **6.0%** | **−90** |
| downside (405/480, petcoke 143) | 264 | −3.1 | −34.0% | −268 |

\* the Excel's own figures

**The best case I can defend is ~6% unlevered, NPV −€90m at a 12% discount rate.**
The Excel's 12.0% "optimized FID target" requires simultaneously: CAPEX €225m,
45% carbon utilization, €130/t petcoke, **and** a steam recovery that the heat
balance does not permit. Remove only the last and the case does not clear its
cost of capital.

Note the Excel says this itself: **NPV@12% is negative in every published
scenario** including the optimized one (−€0.57m).

## What was not done

Live research was impossible — the session's egress policy blocks every external
host. No Chinese tender prices, no SEEPEX verification, no Eurostat. The turbine
and gasifier CAPEX in the Excel remain unverified in either direction, and the
figures above inherit them.
