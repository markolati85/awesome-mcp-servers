"""
MSK Kikinda — founder-side capital structure model.

Deterministic project-finance / waterfall model used to generate every number in
STUDY.md. No external dependencies (stdlib only) so it runs anywhere.

Conventions
-----------
* All amounts in EUR millions, all rates as decimals.
* Year 0 = financial close. Construction runs Y0..Y2, COD at start of Y3.
* Cash flows are annual, end-of-year, except construction draws (mid-year).
* "Investor" = the third-party financial investor. "Founder" = Marko Latinovic /
  Trade Unique HoldCo, contributing development rather than cash.

IMPORTANT: operating assumptions (EBITDA, gate fees, prices) are ILLUSTRATIVE
placeholders for structuring purposes. They are labelled as such in STUDY.md and
must be replaced with the Chinese EPC / feedstock studies before any term sheet
is signed. The STRUCTURAL conclusions are tested for robustness across the full
sensitivity grid rather than resting on the base case.
"""

from dataclasses import dataclass, field, replace
from typing import List, Dict, Optional

# ----------------------------------------------------------------------------
# generic finance helpers
# ----------------------------------------------------------------------------

def npv(rate: float, cfs: List[float]) -> float:
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs: List[float], lo: float = -0.95, hi: float = 5.0) -> Optional[float]:
    """Bisection IRR. Returns None if no sign change (no meaningful IRR)."""
    if all(c <= 0 for c in cfs) or all(c >= 0 for c in cfs):
        return None
    f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    if f_lo * f_hi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cfs)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def moic(cfs: List[float]) -> Optional[float]:
    """Total inflows / total outflows on an investor cash-flow vector."""
    out = -sum(c for c in cfs if c < 0)
    inn = sum(c for c in cfs if c > 0)
    return inn / out if out > 0 else None


def annuity_payment(principal: float, rate: float, n: int) -> float:
    if n <= 0:
        return 0.0
    if abs(rate) < 1e-12:
        return principal / n
    return principal * rate / (1.0 - (1.0 + rate) ** -n)


# ----------------------------------------------------------------------------
# project (asset-level) assumptions
# ----------------------------------------------------------------------------

@dataclass
class Project:
    # capex and timing
    capex: float = 200.0                 # EUR m, modernisation/restart programme
    capex_profile: tuple = (0.25, 0.45, 0.30)   # Y0, Y1, Y2
    delay_years: int = 0                 # construction delay (COD pushed back)
    capex_overrun: float = 0.0           # fraction, e.g. 0.20 = +20%

    # acquisition of the shares/assets of MSK from the state / Srbijagas
    acquisition_price: float = 40.0      # EUR m, ILLUSTRATIVE
    acq_deferred_years: int = 7          # seller-financed instalments
    acq_rate: float = 0.03               # seller credit coupon

    # operations
    ebitda_full: float = 46.0            # EUR m at full ramp, hybrid feedstock case
    ebitda_stress: float = 0.0           # fractional haircut, e.g. -0.25
    ramp: tuple = (0.55, 0.85, 1.00)     # first three operating years
    ebitda_growth: float = 0.015         # nominal, post-ramp
    maint_capex_pct: float = 0.035       # of gross capex, per operating year
    working_capital: float = 18.0        # EUR m, funded by a separate WC facility

    # tax (Serbia)
    tax_rate: float = 0.15
    tax_depr_life: int = 15
    interest_cap_pct_ebitda: float = 0.30   # ATAD-style exceeding borrowing cost cap
    loss_carryforward_years: int = 5

    # valuation
    exit_multiple: float = 5.5           # EV / EBITDA
    horizon: int = 15

    @property
    def total_capex(self) -> float:
        return self.capex * (1.0 + self.capex_overrun)

    @property
    def cod(self) -> int:
        return len(self.capex_profile) + self.delay_years

    def ebitda_series(self) -> List[float]:
        """EBITDA by year index, 0 through horizon."""
        out = [0.0] * (self.horizon + 1)
        full = self.ebitda_full * (1.0 + self.ebitda_stress)
        for y in range(self.cod, self.horizon + 1):
            k = y - self.cod
            if k < len(self.ramp):
                f = self.ramp[k]
            else:
                f = self.ramp[-1] * (1.0 + self.ebitda_growth) ** (k - len(self.ramp) + 1)
            out[y] = full * f
        return out

    def capex_series(self) -> List[float]:
        out = [0.0] * (self.horizon + 1)
        tc = self.total_capex
        # delay stretches the construction period, spreading the last tranche
        prof = list(self.capex_profile)
        if self.delay_years > 0:
            # delay adds years of slow spend at the tail (idle-time cost ~2%/yr of capex)
            prof = prof + [0.0] * self.delay_years
        for y, f in enumerate(prof):
            out[y] = tc * f
        if self.delay_years > 0:
            # standing costs during delay, charged to capex
            for y in range(len(self.capex_profile), self.cod):
                out[y] += 0.02 * self.capex
        return out

    def maint_capex_series(self) -> List[float]:
        out = [0.0] * (self.horizon + 1)
        for y in range(self.cod, self.horizon + 1):
            out[y] = self.maint_capex_pct * self.capex
        return out


# ----------------------------------------------------------------------------
# capital structure
# ----------------------------------------------------------------------------

@dataclass
class Structure:
    name: str
    label: str = ""
    # gearing
    senior_pct: float = 0.60             # senior/ECA debt as % of funding need
    fixed_senior: Optional[float] = None  # if set, use this debt quantum instead of
                                          # re-sizing (REQUIRED for stress testing:
                                          # a stress must hold the structure constant)
    senior_rate: float = 0.065           # all-in incl. ECA premium amortised
    senior_tenor: int = 12               # years post-COD
    senior_grace: int = 2                # interest-only years through ramp
    dsra_months: int = 6                 # debt service reserve, pre-funded
    dscr_floor: float = 1.30             # sizing test: MINIMUM DSCR across ops life
    # investor junior capital
    investor_equity: float = 0.0         # EUR m of the funding need taken as equity
    investor_shl: float = 0.0            # EUR m of shareholder loan / pref
    shl_rate: float = 0.09
    shl_pik_years: int = 4               # PIK through construction + first ramp year
    shl_bullet_year: int = 10            # final maturity (year index)
    pref_return: float = 0.0             # additional preferred accretion on equity
    # ownership
    founder_econ: float = 0.51           # founder share of ordinary equity
    founder_votes: float = 0.51
    # founder cash contribution (usually zero — sweat + deferred acquisition price)
    founder_cash: float = 0.0
    # founder call option
    call_year: int = 6
    call_target_irr: float = 0.15
    call_moic_floor: float = 1.6
    call_moic_cap: float = 2.0           # ceiling on total investor money multiple
    call_formula: str = "greater"        # greater | lesser | irr | moic | capped | fmv
    # cost overrun funding split (investor share of any overrun equity)
    overrun_investor_share: float = 1.0

    @property
    def investor_junior(self) -> float:
        return self.investor_equity + self.investor_shl


# ----------------------------------------------------------------------------
# the engine
# ----------------------------------------------------------------------------

def run(p: Project, s: Structure) -> Dict:
    H = p.horizon
    ebitda = p.ebitda_series()
    capex = p.capex_series()
    maint = p.maint_capex_series()

    # ---- funding need -------------------------------------------------------
    # capex + interest during construction (approximated) + fees + initial WC
    fees = 0.025 * p.total_capex
    funding_need_ex_dsra = p.total_capex + fees + p.working_capital

    # ---- senior debt sizing -------------------------------------------------
    # Sized on the BINDING (minimum) DSCR across the whole operating life, with an
    # interest-only grace period through ramp-up. Solved by bisection because the
    # DSRA makes the funding need a function of the debt size.
    def debt_service_profile(D: float) -> List[float]:
        out = [0.0] * (H + 1)
        bal = D
        amort_years = max(1, s.senior_tenor - s.senior_grace)
        pay = annuity_payment(D, s.senior_rate, amort_years)
        for y in range(p.cod, min(p.cod + s.senior_tenor, H + 1)):
            k = y - p.cod
            i = bal * s.senior_rate
            if k < s.senior_grace:
                out[y] = i
            else:
                pr = min(bal, max(0.0, pay - i))
                out[y] = i + pr
                bal -= pr
        return out

    def min_dscr_for(D: float) -> float:
        ds = debt_service_profile(D)
        worst = 1e9
        for y in range(p.cod, min(p.cod + s.senior_tenor, H + 1)):
            cf = ebitda[y] * (1 - p.tax_rate * 0.6) - maint[y]
            if ds[y] > 1e-9:
                worst = min(worst, cf / ds[y])
        return worst

    lo_d, hi_d = 0.0, 1000.0
    for _ in range(200):
        mid = (lo_d + hi_d) / 2.0
        if min_dscr_for(mid) >= s.dscr_floor:
            lo_d = mid
        else:
            hi_d = mid
    dscr_size = lo_d

    # gearing-based size, solved jointly with the DSRA it requires
    senior = 0.0
    for _ in range(60):
        ds = debt_service_profile(senior)
        peak = max(ds) if any(ds) else 0.0
        dsra = peak * s.dsra_months / 12.0
        need = funding_need_ex_dsra + dsra
        senior = min(s.senior_pct * need, dscr_size)
    if s.fixed_senior is not None:
        senior = s.fixed_senior
    ds = debt_service_profile(senior)
    dsra = (max(ds) if any(ds) else 0.0) * s.dsra_months / 12.0
    funding_need = funding_need_ex_dsra + dsra
    if s.fixed_senior is not None:
        senior_binding = "fixed (stress test)"
    else:
        senior_binding = "DSCR" if dscr_size < s.senior_pct * funding_need - 0.01 else "gearing"

    junior_need = funding_need - senior
    # scale investor junior to fill the gap, preserving the equity/SHL mix
    if s.investor_junior > 0:
        scale = junior_need / s.investor_junior
        inv_eq = s.investor_equity * scale
        inv_shl = s.investor_shl * scale
    else:
        inv_eq, inv_shl = junior_need, 0.0
    inv_eq = max(0.0, inv_eq - s.founder_cash)
    investor_cash_total = inv_eq + inv_shl

    # ---- construction-period balances --------------------------------------
    senior_bal = 0.0
    shl_bal = 0.0
    idc = 0.0
    draw_years = max(len(p.capex_profile), p.cod)
    for y in range(draw_years):
        share = capex[y] / p.total_capex if p.total_capex else 0.0
        senior_bal += senior * share
        shl_bal += inv_shl * share
        idc += senior_bal * s.senior_rate
        senior_bal += senior_bal * s.senior_rate          # IDC capitalised
        shl_bal += shl_bal * s.shl_rate                   # PIK
    senior_bal = senior * (1 + s.senior_rate) ** 1.5      # normalise IDC treatment
    shl_bal = inv_shl

    # ---- operating phase ----------------------------------------------------
    rows = []
    senior_bal = senior
    # capitalise IDC into the senior balance at COD
    senior_bal = senior * (1.0 + s.senior_rate) ** (p.cod * 0.55)
    shl_bal = inv_shl
    pref_bal = inv_eq if s.pref_return > 0 else 0.0

    tax_base_capex = p.total_capex
    losses = 0.0
    loss_age: List[tuple] = []

    inv_cf = [0.0] * (H + 1)
    fdr_cf = [0.0] * (H + 1)

    # investor outflows during construction
    for y in range(draw_years):
        share = capex[y] / p.total_capex if p.total_capex else 0.0
        inv_cf[y] -= investor_cash_total * share
        fdr_cf[y] -= s.founder_cash * share

    amort_years = max(1, s.senior_tenor - s.senior_grace)
    sched = annuity_payment(senior_bal, s.senior_rate, amort_years)

    # founder acquisition obligation (seller credit), serviced from founder cash
    acq_bal = p.acquisition_price
    acq_pmt = annuity_payment(acq_bal, p.acq_rate, p.acq_deferred_years)

    cum_div_founder = 0.0
    cum_div_investor = 0.0

    for y in range(p.cod, H + 1):
        e = ebitda[y]
        m = maint[y]

        s_int = senior_bal * s.senior_rate
        k_sen = y - p.cod
        if k_sen < s.senior_grace:
            s_prin = 0.0                                  # interest-only through ramp
        elif y >= p.cod + s.senior_tenor:
            s_prin = senior_bal
        else:
            s_prin = min(senior_bal, max(0.0, sched - s_int)) if senior_bal > 0 else 0.0

        # ---- tax -----------------------------------------------------------
        depr = tax_base_capex / p.tax_depr_life if y < p.cod + p.tax_depr_life else 0.0
        shl_int_accr = shl_bal * s.shl_rate
        gross_int = s_int + shl_int_accr
        deductible_int = min(gross_int, max(p.interest_cap_pct_ebitda * e, 3.0))
        taxable = e - depr - deductible_int
        # loss carryforward
        loss_age = [(amt, age + 1) for amt, age in loss_age if age + 1 <= p.loss_carryforward_years]
        if taxable < 0:
            loss_age.append((-taxable, 0))
            tax = 0.0
        else:
            avail = sum(a for a, _ in loss_age)
            used = min(avail, taxable)
            rem = used
            new_ages = []
            for amt, age in loss_age:
                take = min(amt, rem)
                rem -= take
                if amt - take > 1e-9:
                    new_ages.append((amt - take, age))
            loss_age = new_ages
            tax = (taxable - used) * p.tax_rate
        cfads = e - tax - m

        dscr = cfads / (s_int + s_prin) if (s_int + s_prin) > 0.01 else None
        senior_bal = max(0.0, senior_bal - s_prin)
        avail_junior = cfads - s_int - s_prin

        # ---- junior waterfall ----------------------------------------------
        lockup = (dscr is not None and dscr < 1.20)
        shl_int_paid = 0.0
        shl_prin_paid = 0.0
        k = y - p.cod
        if shl_bal > 0:
            if k < s.shl_pik_years or lockup or avail_junior <= 0:
                shl_bal += shl_int_accr           # PIK
            else:
                shl_int_paid = min(avail_junior, shl_int_accr)
                shl_bal += (shl_int_accr - shl_int_paid)
                avail_junior -= shl_int_paid
                # amortise toward the bullet
                yrs_left = max(1, s.shl_bullet_year - y)
                target = shl_bal / yrs_left
                shl_prin_paid = max(0.0, min(avail_junior, target, shl_bal))
                shl_bal -= shl_prin_paid
                avail_junior -= shl_prin_paid
            if y >= s.shl_bullet_year and shl_bal > 0 and avail_junior > 0:
                extra = min(avail_junior, shl_bal)
                shl_prin_paid += extra
                shl_bal -= extra
                avail_junior -= extra

        # preferred accretion (structures using pref equity)
        pref_paid = 0.0
        if pref_bal > 0:
            pref_bal *= (1.0 + s.pref_return)
            if not lockup and avail_junior > 0 and k >= 2:
                due = pref_bal - inv_eq
                pref_paid = max(0.0, min(avail_junior, due))
                pref_bal -= pref_paid
                avail_junior -= pref_paid

        # ordinary distributions (retain a 10% cash cushion)
        div_total = max(0.0, avail_junior * 0.90) if not lockup else 0.0
        div_founder = div_total * s.founder_econ
        div_investor = div_total * (1.0 - s.founder_econ)
        cum_div_founder += div_founder
        cum_div_investor += div_investor

        # founder services the acquisition obligation out of its own distributions
        acq_service = 0.0
        if acq_bal > 0 and y < p.cod + p.acq_deferred_years:
            acq_service = min(acq_pmt, div_founder + max(0.0, 0.0))
            interest = acq_bal * p.acq_rate
            acq_bal = max(0.0, acq_bal + interest - acq_service)

        inv_cf[y] += shl_int_paid + shl_prin_paid + pref_paid + div_investor
        fdr_cf[y] += div_founder - acq_service

        rows.append(dict(year=y, ebitda=e, tax=tax, cfads=cfads, s_int=s_int,
                         s_prin=s_prin, s_bal=senior_bal, dscr=dscr,
                         shl_bal=shl_bal, shl_int=shl_int_paid, shl_prin=shl_prin_paid,
                         div_total=div_total, div_founder=div_founder,
                         div_investor=div_investor, acq_bal=acq_bal,
                         acq_service=acq_service, lockup=lockup))

    # ---- terminal value and the founder call --------------------------------
    def equity_value(year: int) -> float:
        r = next((x for x in rows if x["year"] == year), None)
        if r is None:
            return 0.0
        ev = r["ebitda"] * p.exit_multiple
        return ev - r["s_bal"] - r["shl_bal"]

    def call_price(year: int) -> Dict:
        """Price the founder pays the investor for its whole position at `year`,
        computed so the investor hits its agreed IRR / MOIC floor."""
        pre = inv_cf[:year + 1]
        # IRR-based: solve for the top-up X at `year` giving target IRR
        lo, hi = 0.0, 3000.0
        for _ in range(200):
            mid = (lo + hi) / 2.0
            test = list(pre)
            test[year] += mid
            v = npv(s.call_target_irr, test)
            if v < 0:
                lo = mid
            else:
                hi = mid
        p_irr = (lo + hi) / 2.0
        # MOIC-based
        outflow = -sum(c for c in inv_cf[:year + 1] if c < 0)
        inflow = sum(c for c in inv_cf[:year + 1] if c > 0)
        p_moic = max(0.0, s.call_moic_floor * outflow - inflow)
        p_cap = max(0.0, s.call_moic_cap * outflow - inflow)
        ev_share = max(0.0, equity_value(year)) * (1.0 - s.founder_econ)
        r = next((x for x in rows if x["year"] == year), None)
        shl_out = r["shl_bal"] if r else 0.0
        fmv = ev_share + shl_out
        chosen = dict(greater=max(p_irr, p_moic), lesser=min(p_irr, p_moic),
                      irr=p_irr, moic=p_moic, fmv=fmv,
                      capped=min(max(p_irr, p_moic), p_cap))[s.call_formula]
        return dict(irr_price=p_irr, moic_price=p_moic, cap_price=p_cap,
                    chosen=chosen,
                    greater=max(p_irr, p_moic), fmv_share=fmv,
                    ebitda=r["ebitda"] if r else 0.0, s_bal=r["s_bal"] if r else 0.0,
                    shl_bal=shl_out)

    # can the founder actually FUND the call by refinancing?
    def call_fundable(year: int, price: float, max_leverage: float = 3.5) -> Dict:
        r = next((x for x in rows if x["year"] == year), None)
        if r is None:
            return dict(ok=False, headroom=0.0, capacity=0.0)
        capacity = max_leverage * r["ebitda"]
        existing = r["s_bal"] + r["shl_bal"]
        headroom = capacity - existing
        return dict(ok=headroom >= price, headroom=headroom, capacity=capacity,
                    existing=existing, gap=price - headroom)

    # ---- outputs ------------------------------------------------------------
    res = dict(
        name=s.name, label=s.label,
        funding_need=funding_need, dsra=dsra, senior=senior,
        senior_binding=senior_binding, dscr_max_debt=dscr_size,
        investor_equity=inv_eq, investor_shl=inv_shl,
        investor_cash=investor_cash_total,
        founder_econ=s.founder_econ, founder_votes=s.founder_votes,
        gearing=senior / funding_need if funding_need else 0.0,
        rows=rows, inv_cf=inv_cf, fdr_cf=fdr_cf,
        min_dscr=min([r["dscr"] for r in rows if r["dscr"]], default=None),
        avg_dscr=(sum(r["dscr"] for r in rows if r["dscr"]) /
                  max(1, len([r for r in rows if r["dscr"] is not None]))),
        lockup_years=sum(1 for r in rows if r["lockup"]),
        equity_value=equity_value,
        call_price=call_price, call_fundable=call_fundable,
    )

    # hold-to-exit case: investor sells at horizon at fair value
    inv_exit = list(inv_cf)
    inv_exit[H] += max(0.0, equity_value(H)) * (1.0 - s.founder_econ)
    res["inv_irr_hold"] = irr(inv_exit)
    res["inv_moic_hold"] = moic(inv_exit)

    # call-option case
    cy = s.call_year
    cp = call_price(cy)
    inv_call = inv_cf[:cy + 1]
    inv_call = list(inv_call)
    inv_call[cy] += cp["chosen"]
    res["call"] = cp
    res["call_fund"] = call_fundable(cy, cp["chosen"])
    res["inv_irr_call"] = irr(inv_call)
    res["inv_moic_call"] = moic(inv_call)

    # founder wealth at 5 / 10 / 15 (post-call, founder owns 100%)
    def founder_wealth(year: int, exercised: bool) -> float:
        cash = sum(fdr_cf[:year + 1])
        share = 1.0 if (exercised and year >= cy) else s.founder_econ
        ev = max(0.0, equity_value(year))
        acq_left = next((r["acq_bal"] for r in rows if r["year"] == year), 0.0)
        debt_for_call = 0.0
        if exercised and year >= cy:
            debt_for_call = cp["chosen"] * (1.03 ** (year - cy))  # carried at 3% real
        return ev * share + cash - acq_left - debt_for_call

    res["founder_wealth"] = founder_wealth
    return res


# ----------------------------------------------------------------------------
# the ten structures
# ----------------------------------------------------------------------------

def structures() -> List[Structure]:
    return [
        Structure("A", "Founder 51 / Investor 49, all-equity investor cheque",
                  senior_pct=0.0, investor_equity=100.0, investor_shl=0.0,
                  founder_econ=0.51, founder_votes=0.51),
        Structure("B", "Founder 55 / Investor 45, equity + shareholder loan",
                  senior_pct=0.0, investor_equity=40.0, investor_shl=60.0,
                  shl_rate=0.10, founder_econ=0.55, founder_votes=0.55),
        Structure("C", "Founder 60 / Investor 40, senior+ECA debt 60% + minority equity",
                  senior_pct=0.60, investor_equity=60.0, investor_shl=40.0,
                  shl_rate=0.09, founder_econ=0.60, founder_votes=0.60),
        Structure("D", "Founder 51% votes, investor 49% econ with 1.3x liq pref",
                  senior_pct=0.55, investor_equity=50.0, investor_shl=50.0,
                  shl_rate=0.09, founder_econ=0.51, founder_votes=0.51,
                  pref_return=0.02),
        Structure("E", "Founder majority common, investor preferred equity 8% PIK",
                  senior_pct=0.55, investor_equity=100.0, investor_shl=0.0,
                  pref_return=0.08, founder_econ=0.70, founder_votes=0.70),
        Structure("F", "Investor subordinated debt + warrants (no permanent 49%)",
                  senior_pct=0.55, investor_equity=15.0, investor_shl=85.0,
                  shl_rate=0.12, founder_econ=0.82, founder_votes=0.85,
                  call_target_irr=0.17),
        Structure("G", "Max ECA/project debt 70% + small institutional equity",
                  senior_pct=0.70, investor_equity=55.0, investor_shl=45.0,
                  shl_rate=0.09, founder_econ=0.65, founder_votes=0.65),
        Structure("H", "Strategic industrial investor (offtake-linked, 45%)",
                  senior_pct=0.55, investor_equity=80.0, investor_shl=20.0,
                  shl_rate=0.07, founder_econ=0.55, founder_votes=0.51,
                  call_target_irr=0.13),
        Structure("I", "Infrastructure / private-capital investor, contracted cashflow",
                  senior_pct=0.65, investor_equity=55.0, investor_shl=45.0,
                  shl_rate=0.08, founder_econ=0.58, founder_votes=0.58,
                  call_target_irr=0.14),
        Structure("J", "Family office / permanent capital, long hold, low coupon",
                  senior_pct=0.60, investor_equity=45.0, investor_shl=55.0,
                  shl_rate=0.08, founder_econ=0.62, founder_votes=0.62,
                  call_target_irr=0.15, call_year=7),
        Structure("K", "RECOMMENDED — 60/40 econ+votes, ECA-led 65%, SHL 9% cash-pay, capped call",
                  senior_pct=0.65, senior_rate=0.062, investor_equity=42.0,
                  investor_shl=58.0, shl_rate=0.09, shl_pik_years=1,
                  shl_bullet_year=9, founder_econ=0.60, founder_votes=0.60,
                  call_year=10, call_target_irr=0.14, call_moic_floor=1.60,
                  call_moic_cap=2.10, call_formula="capped"),
    ]
