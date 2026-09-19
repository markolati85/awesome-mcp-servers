#!/usr/bin/env python3
"""
MSK Kikinda - Part 5: CAPEX benchmarking (China) and OWN vs BUILD-OWN-OPERATE (BOO).

Basis: the R2 route from Part 3 (petcoke through the existing Texaco POX island),
slate 150,000 t/y merchant methanol + 50,000 t/y acetic acid, i.e. 177,085 t/y
total methanol-equivalent plus 24,810 t/y CO. All per-tonne figures below are per
tonne of TOTAL methanol-equivalent (177,085 t/y) so they tie to Part 3.

Tagging convention (user's sourcing standard):
  [FACT]  published, attributable
  [EST]   engineering estimate by this model
  [ASSUM] model assumption, chosen, not derived

NOTHING here is a vendor quotation. Every equipment number requires vendor RFQ.

Stdlib only.  Run: python3 msk_capex.py
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 0. Constants
# ---------------------------------------------------------------------------

TOTAL_MEOH_T = 177_085.0      # [FACT-internal] from Part 3 mass balance
CNY_PER_EUR  = 7.69           # [ASSUM] mid-Sep 2026 working rate

# ---------------------------------------------------------------------------
# 1. Chinese CAPEX benchmarks
#
# Sourcing note: Chinese vendor listing prices (Alibaba / Made-in-China / broker
# pages) are excluded by the user's own sourcing standard and are useless for a
# gasification island anyway - they price components, not installed complexes.
# The only reliable Chinese data at this scale is the PUBLISHED TOTAL INVESTMENT
# of announced projects. Those are [FACT] but they are TOTAL project investment
# (greenfield, incl. owner's cost and infrastructure), NOT EPC-installed cost,
# and NOT comparable one-for-one to a brownfield conversion.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ChinaProject:
    name: str
    cny_bn: float          # [FACT] announced total investment
    kt_per_year: float     # [FACT] nameplate methanol
    note: str

    @property
    def eur_m(self) -> float:
        return self.cny_bn * 1000.0 / CNY_PER_EUR

    @property
    def eur_per_annual_t(self) -> float:
        return self.eur_m * 1e6 / (self.kt_per_year * 1000.0)


CHINA = [
    ChinaProject("Xinjiang Zhongtai (Tianchen EPC)", 5.990, 1000.0,
                 "coal->MeOH, 1 Mt/y; world-scale, best case for scale economics"),
    ChinaProject("Lishu biomass gasification->MeOH", 2.557, 200.0,
                 "CLOSEST COMPARABLE: same scale band, same plant shape"),
    ChinaProject("CSSC Tongliao wind-H2->MeOH", 4.300, 320.0,
                 "green route; carries electrolyser + wind, not comparable"),
    ChinaProject("LONGi Urad Houqi green MeOH", 6.974, 400.0,
                 "green route; carries electrolyser + wind, not comparable"),
]

# Scaling to MSK size from the closest comparable.
SCALE_EXPONENT = 0.70         # [ASSUM] classic six-tenths/seven-tenths rule
BROWNFIELD_REUSE_LO = 0.30    # [EST] low end of reuse credit
BROWNFIELD_REUSE_HI = 0.45    # [EST] high end of reuse credit
# Reuse credit rationale [EST]: MSK already owns site, siding, river/rail access,
# power intake, cooling water, tankage, methanol synthesis loop, distillation,
# COSORB, acetic acid unit, ASU building and permits. What must be built or
# rebuilt is the petcoke handling/grinding/slurry train, the gasifier internals
# and refractory, AGR/SRU, and the syngas conditioning. Requires site survey.


def scaled_capex(ref: ChinaProject, target_kt: float) -> float:
    """Greenfield-equivalent EUR m at target scale, per the scaling rule."""
    return ref.eur_m * (target_kt / ref.kt_per_year) ** SCALE_EXPONENT


# ---------------------------------------------------------------------------
# 2. Chinese steel - checked, and it does not move the answer
# ---------------------------------------------------------------------------
# [FACT] China NBS, mid-September 2026: 20mm HRB400E rebar averaged
#        RMB 3,182.7/t nationally = USD ~470/t = EUR ~414/t.
# [FACT] Chinese steelmakers and CISA have been curbing output on weak
#        profitability -> this is a cyclical trough, not a structural floor.
REBAR_CNY_T = 3182.7
REBAR_EUR_T = REBAR_CNY_T / CNY_PER_EUR

# Why cheap steel does not rescue the CAPEX [EST]:
STEEL_SHARE_OF_EPC = 0.12     # [EST] bulk carbon steel as share of installed EPC
# A gasification island's cost sits in alloy pressure vessels, refractory,
# high-pressure piping, rotating equipment, instrumentation and - above all -
# erection hours, not in bulk mild steel.


# ---------------------------------------------------------------------------
# 3. MSK funding build-up (own case), from Part 3 / GPT reconciliation
# ---------------------------------------------------------------------------

EPC_INSTALLED = 176.0         # [EST] base-case EPC installed cost, EUR m
OWNERS_COST   = 18.0          # [EST] owner's team, EPCM, permits, insurance
IDC           = 22.0          # [EST] interest during construction
WORKING_CAP   = 26.0          # [EST] feedstock + product inventory + receivables
CONTINGENCY   = 18.0          # [EST] ~10% of EPC, AACE Class 4 lower bound

TOTAL_FUNDING_OWN = EPC_INSTALLED + OWNERS_COST + IDC + WORKING_CAP + CONTINGENCY

# ---------------------------------------------------------------------------
# 4. Scope split under a "Sale of Gas" / build-own-operate structure
#
# [FACT] Air Products Syngas Solutions markets turnkey gasification complexes
#        under a "Sale of Gas" model in which Air Products builds, finances,
#        owns and operates the syngas facility so that the customer can focus
#        its capital, management and personnel on its own primary value-added
#        products. >230 gasifiers installed worldwide; coal gasification since
#        the early 1970s.
# [FACT] Precedents: a contract to build, own and operate a coal-to-syngas
#        plant for Jiutai New Material, Hohhot, China; and the Lu'an project,
#        the first plant 100% owned by Air Products (~USD 650m, Shell
#        gasification technology).
# ---------------------------------------------------------------------------

BOO_PARTNER_EPC = 134.0       # [EST] gasification island: petcoke handling,
                              #       grinding/slurry, gasifier, syngas cooling,
                              #       AGR, SRU, ASU, island utilities
MSK_EPC_BOO     = EPC_INSTALLED - BOO_PARTNER_EPC   # = 42.0 [EST]
                              #       MSK keeps: synthesis loop refurb,
                              #       distillation, COSORB, acetic acid unit,
                              #       tankage, tie-ins

_scope = MSK_EPC_BOO / EPC_INSTALLED

TOTAL_FUNDING_BOO = (
    MSK_EPC_BOO
    + OWNERS_COST * _scope     # owner's team scales with scope
    + IDC * _scope             # IDC scales with what MSK actually funds
    + WORKING_CAP              # [ASSUM] unchanged - MSK still carries feedstock
                               #         and product inventory; under a pass-
                               #         through tolling deal it may RISE
    + CONTINGENCY * _scope
)

# ---------------------------------------------------------------------------
# 5. Operating cost stack (Part 3, route R2)
# ---------------------------------------------------------------------------

FEEDSTOCK_EUR_T   = 155.0     # [EST] petcoke delivered Kikinda, per t MeOH-eq
ISLAND_OPEX_EUR_T = 98.0      # [EST] island non-feedstock opex (power, O2,
                              #       catalyst, maintenance, island labour)
DOWNSTREAM_EUR_T  = 60.0      # [EST] MSK synthesis/distillation/AcOH opex
CASH_COST_OWN     = FEEDSTOCK_EUR_T + ISLAND_OPEX_EUR_T + DOWNSTREAM_EUR_T  # 313

CONTRACT_YEARS = 20           # [ASSUM] typical Sale-of-Gas tenor


def annuity(rate: float, years: int = CONTRACT_YEARS) -> float:
    """Capital recovery factor."""
    return rate * (1 + rate) ** years / ((1 + rate) ** years - 1)


def capital_charge_eur_t(capital_eur_m: float, rate: float) -> float:
    return capital_eur_m * 1e6 * annuity(rate) / TOTAL_MEOH_T


def tolling_fee_eur_t(partner_rate: float, opex_margin: float = 0.05) -> float:
    """
    What the BOO partner must charge per tonne of MeOH-equivalent to recover
    its island capital at `partner_rate` plus the island opex it now carries,
    with a small margin on the pass-through opex.  [EST]
    """
    cap = capital_charge_eur_t(BOO_PARTNER_EPC, partner_rate)
    return cap + ISLAND_OPEX_EUR_T * (1 + opex_margin)


def compare(msk_rate: float, partner_rate: float) -> dict:
    own_cash  = CASH_COST_OWN
    own_cap   = capital_charge_eur_t(TOTAL_FUNDING_OWN, msk_rate)
    own_full  = own_cash + own_cap

    toll      = tolling_fee_eur_t(partner_rate)
    boo_cash  = FEEDSTOCK_EUR_T + toll + DOWNSTREAM_EUR_T
    boo_cap   = capital_charge_eur_t(TOTAL_FUNDING_BOO, msk_rate)
    boo_full  = boo_cash + boo_cap

    return dict(toll=toll, own_cash=own_cash, own_cap=own_cap, own_full=own_full,
                boo_cash=boo_cash, boo_cap=boo_cap, boo_full=boo_full,
                delta=boo_full - own_full)


def indifference_partner_rate(msk_rate: float) -> float:
    """Partner return at which BOO and owning cost the same, fully loaded."""
    lo, hi = 0.01, 0.60
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if compare(msk_rate, mid)["delta"] > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


# ---------------------------------------------------------------------------
# 6. Report
# ---------------------------------------------------------------------------

def main() -> None:
    w = 78
    print("=" * w)
    print("PART 5 - CHINA CAPEX BENCHMARKS AND OWN-vs-BOO".center(w))
    print("=" * w)

    print("\n1. PUBLISHED CHINESE PROJECT INVESTMENTS  [FACT]")
    print("   (total investment, greenfield - NOT EPC-installed, NOT brownfield)")
    print(f"   {'Project':<38}{'CNY bn':>8}{'EUR m':>8}{'kt/y':>7}{'EUR/t/y':>9}")
    for p in CHINA:
        print(f"   {p.name:<38}{p.cny_bn:>8.3f}{p.eur_m:>8.0f}"
              f"{p.kt_per_year:>7.0f}{p.eur_per_annual_t:>9.0f}")
    for p in CHINA:
        print(f"     - {p.name.split(' (')[0]}: {p.note}")

    ref = CHINA[1]
    greenfield = scaled_capex(ref, TOTAL_MEOH_T / 1000.0)
    lo = greenfield * (1 - BROWNFIELD_REUSE_HI)
    hi = greenfield * (1 - BROWNFIELD_REUSE_LO)
    print(f"\n2. SCALED TO MSK ({TOTAL_MEOH_T/1000:.0f} kt/y MeOH-eq)")
    print(f"   Reference: {ref.name}  [FACT]")
    print(f"   Greenfield-equivalent at MSK scale (n={SCALE_EXPONENT}): "
          f"EUR {greenfield:.0f}m  [EST]")
    print(f"   Less brownfield reuse {BROWNFIELD_REUSE_LO:.0%}-{BROWNFIELD_REUSE_HI:.0%}: "
          f"EUR {lo:.0f}m - {hi:.0f}m  [EST]")
    print(f"   => independently brackets the EUR 175-195m EPC figure. It does NOT")
    print(f"      validate it as a FUNDING need: that is EUR {TOTAL_FUNDING_OWN:.0f}m.")

    print(f"\n3. CHINESE STEEL  [FACT]")
    print(f"   HRB400E 20mm rebar, NBS mid-Sep 2026: CNY {REBAR_CNY_T:,.1f}/t "
          f"= EUR {REBAR_EUR_T:.0f}/t")
    print(f"   Bulk carbon steel is ~{STEEL_SHARE_OF_EPC:.0%} of installed EPC  [EST].")
    print(f"   A 20% swing in steel moves EPC by "
          f"EUR {EPC_INSTALLED*STEEL_SHARE_OF_EPC*0.20:.1f}m "
          f"({EPC_INSTALLED*STEEL_SHARE_OF_EPC*0.20/EPC_INSTALLED:.1%}).")
    print( "   Cheap steel is real but it is not the lever. Cyclical trough:")
    print( "   Chinese mills and CISA are curbing output on weak profitability.")

    print("\n4. FUNDING NEED")
    print(f"   {'':<28}{'OWN':>10}{'BOO':>10}")
    print(f"   {'EPC installed':<28}{EPC_INSTALLED:>10.1f}{MSK_EPC_BOO:>10.1f}")
    print(f"   {'Owner cost / EPCM':<28}{OWNERS_COST:>10.1f}{OWNERS_COST*_scope:>10.1f}")
    print(f"   {'IDC':<28}{IDC:>10.1f}{IDC*_scope:>10.1f}")
    print(f"   {'Working capital':<28}{WORKING_CAP:>10.1f}{WORKING_CAP:>10.1f}")
    print(f"   {'Contingency':<28}{CONTINGENCY:>10.1f}{CONTINGENCY*_scope:>10.1f}")
    print(f"   {'TOTAL (EUR m)':<28}{TOTAL_FUNDING_OWN:>10.1f}{TOTAL_FUNDING_BOO:>10.1f}")
    print(f"   Capital at risk removed from MSK: "
          f"EUR {TOTAL_FUNDING_OWN - TOTAL_FUNDING_BOO:.0f}m "
          f"({1 - TOTAL_FUNDING_BOO/TOTAL_FUNDING_OWN:.0%})")

    print("\n5. FULLY LOADED COST, EUR per t MeOH-equivalent")
    print("   (annuity capital charge over "
          f"{CONTRACT_YEARS} years - NOT a cash P&L line)")
    for msk_rate in (0.10, 0.12, 0.14):
        print(f"\n   MSK cost of capital {msk_rate:.0%}"
              f"   | own cash {CASH_COST_OWN:.0f} + capital "
              f"{capital_charge_eur_t(TOTAL_FUNDING_OWN, msk_rate):.0f}"
              f" = {CASH_COST_OWN + capital_charge_eur_t(TOTAL_FUNDING_OWN, msk_rate):.0f}/t")
        print(f"   {'partner ret.':<14}{'toll':>8}{'BOO cash':>10}"
              f"{'BOO full':>10}{'vs own':>9}")
        for pr in (0.10, 0.12, 0.14):
            r = compare(msk_rate, pr)
            print(f"   {pr:<14.0%}{r['toll']:>8.0f}{r['boo_cash']:>10.0f}"
                  f"{r['boo_full']:>10.0f}{r['delta']:>+9.0f}")
        ind = indifference_partner_rate(msk_rate)
        print(f"   Indifference: BOO wins while the partner's required return "
              f"is below {ind:.1%}")

    print("\n6. WHAT THIS ACTUALLY SAYS")
    print("   - BOO is NOT primarily a cost saving. Per tonne it is roughly")
    print("     neutral when MSK's own cost of capital is ~10%.")
    print("   - BOO wins on two things that are not per-tonne:")
    print(f"     (a) capital at risk EUR {TOTAL_FUNDING_OWN:.0f}m -> "
          f"EUR {TOTAL_FUNDING_BOO:.0f}m;")
    print("     (b) gasifier availability risk sits with the party that has")
    print("         built 230+ of them, not with a first-time owner.")
    print("   - The per-tonne case turns positive exactly to the extent MSK's")
    print("     true cost of capital exceeds the partner's. For a Serbian")
    print("     brownfield restart with no operating track record, it does.")
    print("   - REQUIRES VENDOR RFQ: the tolling fee is the whole deal and")
    print("     cannot be estimated. It must be bid.")
    print("=" * w)


if __name__ == "__main__":
    main()
