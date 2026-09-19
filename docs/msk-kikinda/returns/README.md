# Part 6 — Full-ownership returns, petcoke via Port of Bar

Run: `python3 msk_returns.py`

## Owner's decisions recorded here

- **No BOO, no tolling.** MSK/SPV owns all equipment. No long-term binding
  syngas offtake, so feedstock can be switched to natural gas — or anything
  else — whenever that becomes cheaper. The optionality is the point.
- **Port of Bar** for US Gulf petcoke, then rail to Kikinda.
- **Methanol €450–500/t** as the planning price (not the current war spike).

## Two corrections this part makes to earlier work

Part 3 route R2 reported €165m capex, €312/t cash cost and a 3.6-year payback.
Both inputs were wrong and both errors were mine:

1. **Capex too low.** Revised to €235m installed / €283m funding after the
   China red-team (CE/PED compliance premium, AACE Class-4 contingency,
   Serbian erection priced as its own line).
2. **The €98/t "island opex" was never built up.** It does not survive a check
   against the power bill: net import alone is ~26 MW = 208 GWh/y ≈ **€100/t**
   at €85/MWh. Opex is rebuilt bottom-up here and lands at **€425/t**.

The 3.6-year payback also assumed €700/t methanol — the war spike, not a
planning price.

## Headline result at the owner's price band

Base petcoke (€116/t delivered), quench, funding €283m:

| MeOH | AcOH | Revenue | Opex | EBITDA | Payback |
|---|---|---|---|---|---|
| 450 | 500 | 92.5 | 75.3 | **17.2** | 16.4y |
| 475 | 550 | 98.8 | 75.3 | **23.5** | 12.0y |
| 500 | 620 | 106.0 | 75.3 | **30.7** | 9.2y |

**DSCR fails at the bottom of the band.** At MeOH 450 / AcOH 500 the project
cannot service even 55% senior debt (DSCR 0.98).

## Bar vs the alternative

Bar's sea leg is ~700–900 nm shorter than Constanța (no Dardanelles/Black
Sea), but the Bar–Belgrade mountain line costs ~€31/t against ~€23/t for
Danube/Tisa barge. Net, **Bar is ~€4/t more expensive** — close enough that
control and simplicity may justify it. Capacity check: 270 kt/y ≈ 3.5 trains
per week of 1,500 t. **Line capacity and axle load require confirmation.**

## The two levers that actually move this

1. **Steam integration.** Power is the largest opex line. Taking the turbine
   from 6 MW (quench) to 22–30 MW via a full WHB/RSC train costs €34–52m extra
   capex and moves payback from 12.0y to 9.6–8.8y. This is the opposite of the
   China red-team's "quench, skip the RSC" advice, and at €85/MWh the red-team
   is wrong on this point.
2. **Power price.** €55/MWh → 9.5y; €115/MWh → 16.4y. A power contract is
   worth as much negotiating effort as the petcoke contract.

## The risk that dwarfs everything

Vented CO₂ is **506 kt/y = 2.53 t per tonne of product sold** (European
methanol from natural gas is 0.7–0.9 t/t). Today Serbia charges €0/t on it —
its €4/t tax from 1 Jan 2026 covers cement, fertilizers, iron & steel,
aluminium and electricity, not methanol or acetic acid, and CBAM does not
cover them either.

**EBITDA reaches zero at €46/t CO₂.** Serbia is on an EU accession path and
will adopt an ETS. This is a change-in-law question, not an engineering one,
and it is the single largest threat to the investment.
