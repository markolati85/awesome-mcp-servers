# MSK Kikinda — Founder-Controlled Industrial Investment Structuring Study

**Prepared for:** Marko Latinovic / Trade Unique
**Subject:** Optimal capital structure for the acquisition and modernisation of MSK a.d. Kikinda, and a reusable structure for subsequent industrial projects
**Date:** September 2026
**Status:** Structuring study for negotiation preparation. Not investment advice, not a financing commitment, and not a substitute for Serbian corporate/tax counsel.

---

## How to read this document

Every number below comes from an explicit model in `model/msk_model.py`, whose outputs are reproduced in [`MODEL-OUTPUTS.md`](./MODEL-OUTPUTS.md). Run `python3 model/build_outputs.py` to regenerate.

Three labels are used throughout and never mixed:

- **[FACT]** — documented in a cited primary or reputable secondary source.
- **[INFERENCE]** — a reasonable deduction, clearly not established fact.
- **[RECOMMENDATION]** — my judgement.

**The operating assumptions are placeholders.** Full-ramp EBITDA of €46m and capex of €200m are the modelling assumptions this study was asked to use. Neither has been validated by an engineering study. Section 23 shows what happens when they are wrong, and that analysis, rather than the base case, is what should drive behaviour.

---

## A. Executive conclusion

### A.1 The structure I would pursue first

A **HoldCo / ProjectCo structure with founder 60% economics and 60% votes, funded by ECA-backed senior debt at ~65% of the funding need, with the investor's €82m split between a 9% shareholder loan and ordinary equity, no founder personal guarantee, and a MOIC-capped founder call from Year 10.**

| Term | Value |
|---|---|
| Total funding need | €233m (capex €200m + fees €5m + working capital €18m + DSRA €10m) |
| Senior / ECA-backed debt | €152m (65%) |
| Investor shareholder loan | €47m at 9%, cash-pay from operating Year 2, repaid by Year 8 |
| Investor ordinary equity | €34m |
| Founder cash | €0 |
| Founder economics / votes | 60% / 60% |
| Investor economics / votes | 40% / 40%, with reserved matters |
| Acquisition price (€40m illustrative) | HoldCo-level seller credit from the State, **outside** ProjectCo |
| Investor IRR (hold to Y15) | 11.7%, MOIC 2.9x |
| Investor IRR (call at Y10, 2.10x cap) | 11.4%, MOIC 2.10x |
| Founder wealth Y15 | €210m holding, €224m with the call exercised |
| Minimum DSCR | 1.57x |
| Founder personal guarantee | None |

### A.2 The three things this study concluded that contradict the brief

**1. The binding constraint is not the ownership split. It is whether €200m buys €46m of EBITDA.**

Table 9 shows that moving capex from €150m to €300m swings founder terminal wealth from €259m to €110m — and at €300m the debt has to shrink to stay within DSCR, so the investor's cheque balloons to €181m for a 4.5% IRR, which no investor on earth funds. Moving the founder's share from 51% to 60% moves founder wealth by €39m (Table 11). The capex/EBITDA question is worth roughly **four times** more than the entire ownership negotiation. Every week spent negotiating percentages before the Chinese EPC feasibility study lands is a week spent optimising the wrong variable — which is precisely what Section 21 of the brief warned against, and the brief itself then does by making the split the central question.

**2. No serious private-equity investor will take this deal at any split, and that is not a control problem.**

Table 14 is the important one. Hold-to-exit investor IRR on this asset tops out in the low-to-mid teens across *all ten* structures, at *every* founder percentage from 51% to 75%, at *every* shareholder-loan coupon from 6% to 12%, and at leverage up to the DSCR limit. Apollo, KKR, Oaktree, Advent and Lone Star target 18–22%+. [FACT: mid-market PE commonly targets 15–25% net IRR, large-cap 12–18%.](https://www.opalecapital.com/en/blog/private-equity-returns-2026) The gap is 6–10 points and **no amount of founder generosity closes it**, because the cash simply is not there.

The reverse-analysis exercise in Section 17 of the brief assumes the deal gets rejected because the founder asked for too much. It gets rejected because the asset earns too little. The correct response is not to concede equity — it is to **change the investor universe**: infrastructure/value-add funds, family offices, strategics with an offtake motive, and Chinese industrial groups with ECA support. Conceding 51% to an investor who was never going to clear their hurdle is the worst possible outcome: the founder loses control *and* still gets no deal.

**3. The founder call option, as conceived in the brief, is a trap.**

This is the most important single finding, and it is the opposite of what the brief assumes. Table 6:

- An **IRR-ratchet call gets more expensive every year** (€106m at Y8 → €127m at Y12) because the clock compounds.
- A **MOIC-based call gets cheaper every year** (€59m → €48m) because interim cash reduces the top-up.
- A pure IRR call at 14% prices the investor's stake at a **60–75% premium to its fair market value**, and is **not fundable by refinancing at any point in the fifteen-year model**.
- Exercising an IRR-ratchet call **destroys** founder wealth: €189m versus €210m for simply holding.

The brief says: *"I want to prevent a situation where the factory becomes extremely valuable and the investor can later demand an arbitrary enormous price."* An IRR-ratchet call does not prevent that. **It is that.** It hands the investor a contractual right to an arbitrary, ever-growing price, agreed in advance by the founder, and the founder cannot even borrow enough to pay it.

The founder's protection is a **cap on the investor's money multiple**, not a floor on their IRR. Negotiate the ceiling, not the ratchet.

---

## B. The best three structures

Ranked for the founder, with investor acceptance scored separately. Full detail in Table 1.

| Rank | Structure | Founder econ | Founder wealth Y15 | Investor IRR | Probability of closing | Verdict |
|---|---|---:|---:|---:|---|---|
| **1** | **Recommended: 60/40, ECA-led 65% senior, €47m SHL at 9%, MOIC-capped call** | 60% | €210–224m | 11.7% | **Medium-high** with infra/family-office/strategic capital; near-zero with PE | Best risk-adjusted outcome |
| 2 | **G — maximum ECA/project debt (70%), small institutional cheque** | 65% | €224m | 10.4% | Medium — depends entirely on ECA appetite for Serbian brownfield chemicals | Higher founder %, but a 1.43x minimum DSCR leaves no room for a trough |
| 3 | **J — family office / permanent capital, 62/38, low coupon** | 62% | €217m | 10.0% | Medium — small but genuinely compatible investor universe | Simplest structure; lowest investor return, so it needs exactly the right counterparty |

Note the ranking tension the brief asked for. **The recommended structure is ranked first even though two others give the founder a higher percentage**, because it is the only one that simultaneously delivers a defensible minimum DSCR (1.57x), an investor return at the very top of what this asset can pay (11.7%), and a capped exit. Structure G gives the founder 65% but at a 1.43x minimum DSCR, which is thin for a cyclical commodity chemical and does not survive the stress in Table 12.

Structure F deserves a specific note, because the brief is drawn to it. On paper, 82% founder ownership funded by subordinated debt and warrants looks ideal. The model gives the investor **8.9%** for taking €89m of junior risk in a construction project. No one funds that. It is the most attractive structure the founder cannot have.

Structures rejected outright:

- **A (all-equity, founder 51%)** — gives the founder the *highest* terminal wealth of all ten (€313m, because there is no debt and no coupon) alongside an investor IRR of **4.2%**. It is the perfect illustration of the brief's own Section 21 warning: maximal founder wealth on paper, completely unfinanceable in practice. It will never be signed.
- **D (founder 51% votes, investor 49% economics + preference)** — founder wealth €170m, the lowest of any viable structure. Splitting votes from economics *in the investor's favour* is the single most expensive thing the founder could agree to.
- **E (investor preferred equity, 8% PIK)** — PIK compounds into an exit obligation the founder cannot refinance. See Section F.

---

## C. The €200m financing model

See Table 2 for the full stack. Three points that are not in the brief's framing:

**The funding need is not €200m. It is €233m.** Fees (~2.5%), initial working capital (€18m for a chemical plant turning ~€110–130m of revenue) and a six-month debt service reserve are not optional. A term sheet negotiated against "€200m" will be €33m short on day one, and the overrun mechanism (Section I) will then be triggered *by an error in the term sheet rather than by anything going wrong.* [RECOMMENDATION] Negotiate against total funding need, never against capex.

**Leverage above ~70% does not clear a 1.30x minimum DSCR** on base-case EBITDA (Table 10), and that is before stress. For a **cyclical commodity chemical** — where the brief itself correctly flags the danger — the right test is not what a lender signs at close but what survives a trough. Table 12, with the debt quantum held fixed, shows the structure survives EBITDA −25% (minimum DSCR 1.13x, five years of locked distributions, no default) and **breaks at −40%** (DSCR 0.79x). Since methanol and acetic acid margins can move more than 40% peak-to-trough, **65% is the right answer and 70%+ is founder vanity.**

**On ECA financing.** [FACT] China Exim commonly finances ~85% of contract value against a 15% down payment, with tenors up to ~15 years, Sinosure-insured; medium/long-term Sinosure cover above US$300m requires State Council approval. [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/723180e6/accessing-chinese-solutions-for-mining-energy-and-resource-infrastructure-clients), [Sinosure](https://xm.sinosure.com.cn/en/Insurance/meci/index.shtml). [INFERENCE] A €200m programme sits below the State Council threshold, which materially shortens the approval path.

**But** — and the brief flags this correctly in Section 20 — *Chinese EPC groups doing free technical work is not evidence that Chinese financing exists.* Free feasibility work is a business-development cost of a few hundred thousand euros and is offered routinely. Sinosure cover for a Serbian brownfield chemical restart, with merchant commodity exposure and no sovereign guarantee, is a genuinely different decision. [RECOMMENDATION] Obtain a written indicative Sinosure/Exim interest letter **before** signing anything with an equity investor that is priced off the assumption that cheap ECA debt exists. If the ECA debt does not materialise, the structure defaults to ~50–55% commercial leverage, the investor's cheque grows by ~€35m, and the founder's defensible share falls by roughly 8–10 points.

---

## D. Investor return model

Full detail Table 4. Recommended structure, hold to Year 15:

| Component | Cash to investor |
|---|---:|
| Shareholder loan interest and principal | €65m |
| Ordinary dividends (40% share) | €51m |
| Terminal equity value (40% of Y15 equity) | €122m |
| **Total in** | **€238m** |
| Total invested | €82m |
| **IRR / MOIC** | **11.7% / 2.9x** |

**On the brief's "do not allow double counting" instruction.** The concern is well-placed and the answer is structural, not arithmetic: the shareholder loan is repaid in full by Year 8 and **its outstanding balance is deducted from equity value at every valuation date**. Loan repayment and equity upside are therefore disjoint claims on the same cash, not two bites. Where double counting actually creeps into deals like this is via (a) PIK that is *not* deducted from equity value at exit, and (b) liquidation preferences that are *participating* rather than *non-participating*. [RECOMMENDATION] Insist on **non-participating** preference. A 1.0x non-participating preference costs the founder almost nothing in the base case and is a normal investor protection; a participating preference is double counting written into the SHA.

**The brief's test structures** (8% / 10% / 12% coupon alongside 40% equity) are answered in Table 11, and the result is worth stating precisely. From the recommended 40% / 9% cell:

- Raising the coupon 9% → 12% gives the investor **+0.4 points** of IRR and costs the founder **€4m**.
- Raising investor equity 40% → 45% gives the investor **+0.8 points** and costs the founder **€22m**.

Per point of IRR delivered, **equity costs the founder roughly three times what coupon does.** [RECOMMENDATION] In negotiation, pay up to 10–11% on the shareholder loan without hesitation in order to hold the equity line at 40%. Founders instinctively do the reverse, because the coupon is visible annual cash and the equity is abstract future value. That instinct costs roughly €25–30m of terminal wealth per 5 points of equity conceded.

**When do the total economics become excessive?** At an investor IRR above ~14% on this asset, the founder's Y15 wealth falls below ~€190m and the call option becomes unfundable in every year of the model. [RECOMMENDATION] **14% is the walk-away line on blended investor economics**, not 20%.

---

## E. Founder return model

Table 5. Recommended structure:

| Case | Wealth Y5 | Wealth Y10 | Wealth Y15 |
|---|---:|---:|---:|
| Hold 60%, no call | €3m | €93m | €210m |
| Call at Y10, 2.10x cap | €3m | €50m | €224m |

**The Year 5 number is the one to stare at.** Founder net worth from this project at Year 5 is approximately zero, in *every* structure, because the asset is still levered, the acquisition obligation is outstanding and distributions are locked up behind senior debt and shareholder-loan amortisation.

Two consequences the brief does not anticipate:

1. **The founder must have independent income for at least eight years.** Any structure, lifestyle or parallel obligation that requires cash out of MSK before Year 8 will break the deal or force the founder to sell equity cheaply at the worst moment. This is the most common way founders in exactly this position lose control — not through a veto right, but through personal liquidity pressure.

2. **The model shows the acquisition obligation stalling.** In the base case the €40m seller credit cannot be serviced out of founder distributions in Years 5–8 — the balance stops amortising at €32.9m (Table 8) because there are no distributions to service it from. [RECOMMENDATION] Negotiate the seller credit with a **principal grace period to Year 8** and amortisation thereafter, explicitly matched to the ProjectCo distribution profile. A seller credit with a Year 3 start is a default waiting to happen, and defaulting to the *State* on the acquisition price is a catastrophic, politically visible failure.

---

## F. Call-option model

Tables 6, 7, 7b. This section reverses the brief's premise; the reasoning is in Section A.2 point 3.

### The four formulas, worked

At Year 10, recommended structure, investor has €82m in:

| Formula | Price | FMV of the position | Premium | Fundable? | Founder wealth Y15 |
|---|---:|---:|---:|:--:|---:|
| IRR ratchet, 14% | €127m | €77m | +64% | **No** | €180m |
| Greater of 14% IRR / 1.6x MOIC | €127m | €77m | +64% | **No** | €180m |
| **Greater of, capped at 2.10x MOIC** | **€89m** | €77m | +16% | **Yes** | **€224m** |
| Fair market value (independent valuation) | €77m | €77m | 0% | Yes | €238m |
| 1.6x MOIC only | €49m | €77m | −37% | Yes | €271m |

### What sophisticated investors will actually accept

[INFERENCE, from market practice rather than a documented comparable] A 1.6x-MOIC-only call will be rejected — it caps the investor below their hurdle while leaving them the full downside. A pure FMV call will usually be rejected too, because it gives the founder a free option on their own information advantage.

The realistic landing zone is a **collar**: the investor gets a floor (the greater of a defined IRR and a minimum multiple) and the founder gets a ceiling (a maximum multiple). [RECOMMENDATION] Open at *lesser of 12% IRR / 1.5x*; target **greater of 12% IRR / 1.6x MOIC, capped at 2.10x**; fall back to a 2.25x cap; walk away above 2.5x, at which point the call is worthless because it can never be exercised profitably.

### Three mechanical points that matter more than the formula

**PIK is the founder's enemy, not friend.** With a four-year PIK the Year 6 call price is €161m and is unfundable until Year 8. With a one-year PIK it is €128m and fundable from Year 6. PIK feels founder-friendly because it preserves early cash; it is in fact a compounding short position against the founder's own future ownership. [RECOMMENDATION] Accept PIK only through construction and the first ramp year, then hard-switch to cash-pay subject to a 1.20x DSCR lock-up test.

**Exercise late, not early.** Under a MOIC cap, every year of waiting lowers the price (interim cash counts toward the multiple) *and* raises refinancing capacity (senior debt amortises). Years 10–12 are the window. A Year 5 or Year 6 call is unfundable in every variant tested.

**The call must be fundable, and "fundable" means something specific.** At Year 6 the ProjectCo carries €142m of senior plus €21m of shareholder loan against €47m of EBITDA — 3.5x already. There is no refinancing headroom. [RECOMMENDATION] Write a **financing condition** into the call: the founder may exercise within a 24-month window opening at Year 10, and the exercise is conditional on refinancing availability, with no penalty for non-exercise. An unconditional call the founder cannot fund is a liability, not an asset.

### When the call is genuinely valuable

Table 7b. Because the MOIC-capped price is fixed by the *investor's* cash flows and not by plant performance, all outperformance accrues to the founder:

| Actual EBITDA | Call price (2.10x, Y10) | Founder gain from exercising |
|---:|---:|---:|
| €30m | €215m | not exercised |
| €40m | €102m | not exercised |
| €46m (base) | €89m | +€14m |
| €55m | €68m | +€61m |
| €65m | €45m | +€114m |
| €80m | €0m | +€204m |

This is the honest case for the call: **a cheap option on the founder's own execution.** It is an option, not an obligation — in the €30m and €40m rows the founder simply does not exercise and loses nothing but the negotiating capital spent obtaining it. Price it on MOIC, cap it, exercise late, and treat it as upside rather than as the ownership plan.

---

## G. Governance term sheet

The brief asks for founder operational control with genuine but non-paralysing minority protection. That is achievable at 60/40. It is *not* achievable at 51/49 with a standard reserved-matters list, for the reason set out below.

### Board

[RECOMMENDATION] **Five seats: founder 3, investor 2.** Chair appointed by the founder, no casting vote (a casting vote invites a deadlock clause that is worse than the problem it solves).

Reject the 7-seat model with an independent director. In a two-shareholder company an "independent" director is in practice appointed by whoever wins the fight over their identity, and that fight will recur at every contentious decision. Five seats with a clear majority is more honest and more stable.

### Management

Founder appoints and removes the CEO, CFO and all other officers, subject to one carve-out: **the investor may require the removal of the CFO for cause** (fraud, material misstatement, failure to deliver reporting). [RECOMMENDATION] Concede this early and cheaply. It is the protection most investors actually care about and it costs the founder nothing operationally.

The founder controls: pricing, customers, offtake within policy, procurement within budget, hiring below the officer level, production planning, execution of the approved annual budget, and all ordinary commercial contracts.

### Reserved matters — the list to accept

Investor consent (or their 2 board votes) required for:

1. Issuing new shares or instruments convertible into shares
2. Changing the constitution in a way that affects investor rights
3. Related-party transactions above €250k (**the single most important protection in the whole SHA, and the founder should propose it first, unprompted**)
4. Incurring debt above an agreed ratio (say net debt / EBITDA > 3.5x)
5. Granting security over material assets outside the agreed financing
6. Disposing of assets above €5m
7. Winding up, insolvency filing, or material change of business
8. Approving the annual budget — **with a deemed-approval mechanic** (see below)
9. Distributions outside the agreed waterfall
10. Appointing or removing the auditor

### Reserved matters — the list to refuse, and why

The brief asks to "red-team every investor veto" and identify which create de facto control at 51–60%. These are the ones:

| Veto demanded | Why it is de facto control |
|---|---|
| **Annual budget approval with no fallback** | The most dangerous clause in minority-protection practice. If the investor can withhold budget approval with no consequence, they control the company every January. **Always pair with: if no budget is approved by the start of the financial year, the prior year's budget applies uplifted by CPI.** This single mechanic is worth more than five points of equity. |
| Any capex above a low threshold (€1–2m) | In a chemical plant this is routine maintenance and turnaround spend. Converts an operational necessity into an annual hostage negotiation. Set the threshold outside the approved budget only, and at €5m+. |
| Hiring/firing any senior manager | Control of management is control of the company. Concede the CFO-for-cause carve-out only. |
| Entering contracts above a low threshold | Offtake and feedstock contracts *are* the business. Anything that lets the investor veto a methanol sales contract is total control. |
| **Veto over refinancing** | Lethal in combination with a founder call: the investor can block the very refinancing needed to buy them out, then demand a higher price. **Refuse absolutely, or make it fall away once senior debt is below an agreed threshold.** |
| Veto over the business plan (as distinct from the budget) | Open-ended and unmeasurable. |
| Investor consent to exercise of the founder call | Defeats the entire purpose. The brief is right to flag this. |

At **51/49** this list becomes unmanageable: with a near-equal stake the investor will demand more of it, deadlock is structurally likely, and the founder's "control" is nominal. **60/40 with a disciplined reserved-matters list gives more real control than 51/49 with a fought-over one.** This is the concrete answer to the brief's question about whether 51% ordinary equity is optimal: it is not, and the reason is governance dynamics rather than arithmetic.

---

## H. Cash waterfall

[RECOMMENDATION] The order below is the most founder-favourable one that senior lenders and a minority investor will realistically accept. The brief's proposed ordering is close; three changes matter.

1. Operating costs and maintenance capex
2. Taxes
3. Senior debt interest
4. Senior debt scheduled principal
5. Debt service reserve top-up to 6 months
6. Maintenance reserve top-up
7. **Shareholder loan interest** (cash-pay, subject to DSCR ≥ 1.20x; PIK below that)
8. **Shareholder loan principal** (target full repayment by Year 8)
9. Ordinary distributions, pro rata to all shareholders (10% cash cushion retained)
10. **Out of the founder's distribution share only: service of the acquisition obligation**

### The three changes from the brief's draft

**The founder acquisition obligation moves from step 8 to step 10, and out of the company entirely.** In the brief it sits above ordinary distributions, which means ProjectCo pays it — i.e. the investor funds 40% of the founder's purchase of the founder's own stake. No investor will agree, and the founder should not want it: it converts a personal obligation into a shared one at a 40% cost. It belongs at HoldCo, serviced from the founder's distributions after they leave ProjectCo. See Section 10 / Table 8.

**There is no "preferred investor return" step.** The brief lists one after shareholder-loan amortisation. Adding a preferred return *on top of* a 9% shareholder loan *and* 40% of the equity is the double counting the brief elsewhere warns against. Pick one: a shareholder loan with a coupon, or preferred equity with a preferred return. [RECOMMENDATION] Choose the shareholder loan — it is senior to equity, tax-efficient at 15% Serbian CIT within the deductibility limits, and repayable without a shareholder vote.

**A cash-sweep clause must be resisted.** Lenders will ask for 50–75% of excess cash to sweep to senior prepayment. Every euro swept is a euro that does not reduce the shareholder loan, which is the expensive money. [RECOMMENDATION] Offer a sweep that is *conditional on leverage*: 50% sweep above 3.0x net debt/EBITDA, zero below. This is common and lenders accept it.

### Serbian tax constraint on the shareholder loan

[FACT] Serbia applies a 15% flat corporate income tax; exceeding borrowing costs are deductible only up to **30% of EBITDA or €3m, whichever is higher**, with a three-year carry-forward; related-party interest above a **4:1 debt-to-equity ratio** is disallowed under thin-capitalisation rules; the domestic dividend withholding rate for non-residents is 20%, commonly reduced to 5% or 10% by treaty. ([Serbia tax guide 2026](https://www.taxadvisorserbia.com/insights/doing-business-in-serbia-2026-tax-guide), [PwC — Serbia withholding taxes](https://taxsummaries.pwc.com/serbia/corporate/withholding-taxes))

[INFERENCE] These rules bind this structure in two places. First, total interest (senior + shareholder loan) is ~€14m against €46m of EBITDA, or 30.4% — **right at the deductibility cap**. Any increase in the shareholder-loan coupon above ~9% starts producing non-deductible interest, which makes expensive money more expensive still. This is a second, independent reason to cap the shareholder loan around 9–10%. Second, the investor's jurisdiction materially changes their net return via dividend withholding. [RECOMMENDATION] Have Serbian tax counsel confirm both points before the term sheet, and expect a sophisticated investor to hold their stake through a treaty jurisdiction — which is normal and should not be resisted.

---

## I. Cost-overrun mechanism

Table 13. This is where the founder is most likely to lose the company, and the brief is right to single it out.

A 20% overrun on €200m is €40m. If the investor funds it as new equity at the original valuation, the founder falls from 60% to **41.5%** — losing control outright. At a punitive 30% discount, to **34.1%**. The brief's worry that "a €20m cost overrun turns a 45% investor into a 60% shareholder" understates the problem.

### The recommended overrun waterfall

Each layer is exhausted before the next is touched:

| Layer | Source | Size | Dilution |
|---|---|---:|:--:|
| 1 | **Contingency inside the budget** — 10% of capex, funded pro rata at close | €20m | none |
| 2 | **EPC lump-sum turnkey wrap** — fixed price on the ~70% of scope that can be wrapped, with liquidated damages and a performance bond at 10% of contract value | ~€140m of scope | none |
| 3 | **Standby senior / ECA tranche** — committed at close, undrawn, priced as a commitment fee | €20m | none |
| 4 | **Pro-rata subordinated overrun loan** at the shareholder-loan coupon + 200bp, offered to *both* shareholders pro rata | uncapped | none |
| 5 | **Non-pro-rata subordinated loan** — if the founder cannot fund their share, the investor funds 100% and receives a preferential return on that tranche only | uncapped | none |
| 6 | **Equity issue at fair market value** determined by an independent valuer — last resort, and never at a contractual discount | uncapped | dilution at fair value only |

### The clauses to refuse

- **Any automatic equity conversion of overrun funding.** This is the mechanism that takes the company.
- **Any "equity cure at a discount to the last round."** A punitive ratchet at exactly the moment of maximum weakness.
- **Any sponsor completion guarantee backed by the founder personally or by Trade Unique assets.** The brief is right to insist on this and the founder should treat it as a walk-away. A completion guarantee limited to **ProjectCo resources and the founder's ProjectCo shares** is acceptable; recourse beyond that is not.
- **Cross-default to other Trade Unique entities.** Destroys the ring-fence that is the entire point of the SPV.

[RECOMMENDATION] Layers 1–3 should be **negotiated into the base case before the equity term sheet is signed**, because after signing the investor has no reason to fund contingency they can instead convert into ownership. This is the highest-leverage single item in the entire negotiation and it is not the ownership split.

---

## J. Investor red team — why an institution rejects this

Written from the other side of the table.

**"The asset is sub-scale and structurally disadvantaged."** 200kt/yr of methanol is small — world-scale plants are 1.7–2.5 Mt/yr. [INFERENCE] Unit costs at this scale are materially above global marginal producers. Worse, European gas-based methanol competes against US Gulf and Middle East producers with structurally cheaper feedstock. [FACT] MSK has been repeatedly idled — a 12-month halt to 2009, an extended turnaround to December 2016 ([SeeNews](https://seenews.com/news/serbian-methanolacetic-acid-complex-msk-kikinda-restarts-production-after-12-mo-halt-935742), [ICIS](https://www.icis.com/explore/resources/news/2016/12/01/10059750/serbia-msk-s-kikinda-plant-comes-out-of-shutdown/)) — and accumulated large gas debts to Srbijagas, which converted them to equity. **An asset that has failed repeatedly under two owners needs an explanation of what is different now, and "new management and €200m" is not sufficient.**

**"The €46m EBITDA is unsupported, and our own arithmetic does not reach it."** On roughly 145kt of merchant methanol plus 100kt of acetic acid, revenue is of the order of €105–125m. Natural gas at ~33 GJ/t of methanol is the dominant cost and at recent European gas prices it consumes most of the gross margin. [INFERENCE] A gas-fed refurbishment plausibly earns €10–20m of EBITDA and is negative in a gas spike. **The €46m case is not a refurbishment case — it implicitly requires the waste/biomass feedstock route.** But a 600kt/yr RDF gasification and syngas cleanup train is itself a €400m+ project. So: €200m is simultaneously too much to spend on a gas refurbishment that cannot earn it back and too little to build the waste conversion that would justify it. **Resolve this before anything else.** This is the single most important sentence in the study.

**"We are being asked to fund 100% of the cash for 40% of the company."** The founder's contribution is real but its market value is not 60%. [INFERENCE] Development work of the type described — origination, government negotiation, EPC organisation, permitting, team — is typically compensated at 10–25% of a project's equity, occasionally more where the originator holds genuinely exclusive access. The founder's 60% claim needs to rest on **exclusivity**: if any investor could negotiate with the Serbian state directly, the promote collapses.

**"There is no offtake, no feedstock contract, and no permit."** At the stage described, this is a concept, not a project. Institutions fund projects.

**"Serbia, chemicals, brownfield, restart, merchant commodity exposure, minority stake, founder control, no personal guarantee, and a call option capping our upside."** Each is individually financeable. The combination is a very small universe.

### The efficient frontier — what to concede, in order

The brief asks where one additional concession disproportionately raises the probability of closing. From the model and from market practice:

| Rank | Concession | Cost to founder | Effect on closing probability |
|---|---|---|---|
| **1** | **Independent technical and market due diligence, founder-funded, before approach** | €0.3–0.8m | **Largest single improvement.** Converts the asset from a story into a project. |
| **2** | A signed offtake or tolling arrangement for ≥50% of output | Margin concession | Very large — transforms the risk profile and the debt capacity |
| **3** | Raise the shareholder-loan coupon to 10–11% | ~€2–4m of terminal wealth | Large — visible annual cash is what credit committees underwrite |
| **4** | 1.0x non-participating liquidation preference | Small in base case | Large — standard, expected, cheap |
| **5** | CFO appointed jointly / removable by investor for cause | ~zero | Moderate — high comfort, no operational cost |
| **6** | Move the founder call from Y6 to Y10 with a 2.25x cap | €10–15m | Moderate |
| **7** | Drop founder economics 60% → 55% | ~€22m | **Small** — moves investor IRR by only ~0.8 points |

**Items 1 and 2 are worth more than items 3 through 7 combined, and neither is a concession of ownership.** The founder's instinct will be to reach for item 7 first. That is backwards.

---

## K. Founder red team — where the founder gives away value

**Giving away equity to fix a returns problem that equity cannot fix.** The central trap. When an investor says "the returns don't work", the founder will hear "give me more equity". Table 11 shows 5 points of equity buys the investor ~0.8 points of IRR. The founder can concede all the way to 40% and still not reach an 18% hurdle. [RECOMMENDATION] When an investor says the returns do not work, the correct response is *"then you are the wrong investor"*, not *"how much do you need?"*

**Accepting an IRR-ratchet call and believing it is a protection.** Covered in Section F. The founder asked for this specifically and it is the most expensive thing in the brief.

**Underwriting the acquisition price out of distributions that do not exist.** Table 8: the obligation stalls in Years 5–8. A seller credit that starts amortising at Year 3 defaults.

**Believing free Chinese EPC work implies Chinese financing.** Covered in Section C. The brief already flags this; the model quantifies it: without ECA debt the investor's cheque rises ~€35m and the founder's defensible share falls 8–10 points.

**Personal liquidity.** Year 5 founder wealth from this project is approximately zero in every structure.

**Assuming the state is a passive seller.** [FACT] Serbia's recent industrial transactions have carried heavy non-price obligations: HBIS bought Železara Smederevo for €46m in 2016 with investment commitments reported between $300m and $980m and a commitment to retain ~5,000 workers ([bne IntelliNews](https://www.intellinews.com/serbia-to-sell-zelezara-smederevo-to-china-s-hbis-94453/), [Gecić Law](https://www.geciclaw.com/zelezara-smederevo/)); NIS took HIP-Petrohemija from ~21% to 90% in December 2021 for €150m with a €150m capitalisation commitment and a new polypropylene complex ([Interfax](https://interfax.com/newsroom/top-stories/73471/)). [INFERENCE] **The headline price is the least important term.** Employment guarantees, investment milestones, clawbacks and reversion rights will dominate, and a low price bought with a heavy investment commitment can be far more expensive than a high price with a light one. Budget for the obligations, not the price.

**Underestimating environmental liability.** A 1987-vintage chemical complex that has operated intermittently will have soil and groundwater issues. [RECOMMENDATION] A Phase II environmental assessment and an explicit statutory carve-out for pre-closing contamination are non-negotiable. In several CEE privatisations legacy environmental liability has exceeded the purchase price. Without the carve-out, no serious investor will sign regardless of the equity split.

**Working capital.** A plant with ~€110–130m of revenue and volatile feedstock needs €18–25m of working capital, plus letters of credit for gas or feedstock purchases that a counterparty will only extend against cash collateral or a guarantee until a track record exists. [RECOMMENDATION] Size the WC facility at close; do not assume it appears at COD.

---

## L. Historical precedents

The brief asks for documented transaction mechanics rather than mythology, with clear labelling where disclosure is unavailable.

### INEOS — what actually happened, and what transfers

**The 1998 founding transaction.** [FACT] Ratcliffe, then a director of Inspec, formed Ineos to buy Inspec's ethylene oxide facility at Antwerp. The £84m purchase was funded by Murray Johnstone (£10m), Ineos management (£1.5m), and BT Alex Brown (£72.5m raised through high-yield bonds). ([Wikipedia — Ineos](https://en.wikipedia.org/wiki/Ineos), [Business Sale](https://www.business-sale.com/insights/for-buyers/how-sir-jim-ratcliffe-built-ineos-into-the-uks-biggest-private-company-225465))

Read the ratios, because they are the whole lesson:

| | Amount | % |
|---|---:|---:|
| High-yield debt | £72.5m | **86%** |
| Financial sponsor equity | £10m | 12% |
| **Management equity** | **£1.5m** | **1.8%** |

**Ratcliffe's control did not come from contributing 51% of the capital. It came from contributing 1.8% of the capital and using debt, not equity, for the rest.** The equity cheque he had to share was tiny because the debt market carried the transaction. This is the single most transferable lesson, and it argues directly for the recommended structure: **maximise senior/ECA debt, minimise the equity cheque, and only then argue about the split of a small equity pool.** A founder who raises €233m as equity is negotiating over a large pie; a founder who raises €152m of debt is negotiating over an €82m pie, and the same percentage costs the investor far less to concede.

**The 2005 Innovene acquisition.** [FACT] Ineos agreed to buy BP's Innovene for $9bn in October 2005, completing 14 December 2005; the combined group had turnover above $30bn, making it the fourth-largest independent petrochemicals company. ([INEOS](https://www.ineos.com/news/ineos-group/ineos-completes-purchase-of-bps-innovene-business-for-9bn/), [C&EN](https://cen.acs.org/articles/83/i42/Ineos-Buying-BPs-Innovene.html)) [FACT] INEOS's own account states the $9bn was raised in 30 days. The detailed tranching of the 2005 facilities is **not established in the sources reviewed here** — I could not verify the senior/second-lien split or the arrangers, and I am not going to state figures I have not seen. Treat any specific 2005 tranche numbers as unverified.

**Ownership evolution.** [FACT] INEOS Ltd shareholders are reported as Ratcliffe ~61.8%, Currie ~19.2%, Reece ~19%. ([Adam Crafton / reporting](https://x.com/AdamCrafton_/status/1738967849186562368), [WikiCorporates](https://www.wikicorporates.org/wiki/INEOS_Group_Holdings_SA)) [INFERENCE] The founding sponsor (Murray Johnstone) is not among them, so the financial investor was bought out or exited at some point — **exactly the trajectory the brief wants.** The terms are not publicly disclosed and I will not invent them.

**What does not transfer.** [FACT] INEOS has recently carried debt above €10bn and cancelled its dividend amid pressure in European chemicals ([AOL/Telegraph](https://www.aol.com/news/jim-ratcliffe-ineos-cancels-dividend-111518406.html)). The leveraged model works when acquiring **cash-generative assets at a discount to replacement cost**. MSK is not cash-generative — it needs €200m before it generates anything. Ratcliffe bought businesses that were already producing EBITDA and cut costs; this is a construction and restart project with commissioning risk. **Applying INEOS-style leverage to a pre-revenue restart is the fastest way to lose it.** The 86% gearing in the 1998 deal must not be copied.

### Mittal / ArcelorMittal

[FACT] Ispat acquired Kazakhstan's Karmet in 1995 for a reported $400–450m, and a 2001 investment agreement with Kazakhstan covered ~$580m of capital expenditure. Sidex (Romania) followed in 2001. ([Qarmet — Wikipedia](https://en.wikipedia.org/wiki/Qarmet), [steelonthenet](https://www.steelonthenet.com/history/karmet.html), [Mittal Steel Company](https://en.wikipedia.org/wiki/Mittal_Steel_Company))

[INFERENCE] The pattern is directly analogous to MSK: distressed state-owned heavy industry, low headline price, heavy investment obligation, sponsor supplying management and access rather than the bulk of the cash. The transferable lesson is the **sequencing**: acquire cheap with obligations, restore cash generation, then refinance against the restored asset rather than against the projections. Detailed equity/debt splits of the 1995 Karmet financing are **not publicly disclosed** in the sources reviewed.

### Serbian precedents — the most directly relevant comparables

| Deal | Price | Obligations | Relevance |
|---|---|---|---|
| **Železara Smederevo → HBIS (2016)** [FACT] | €46m | Investment commitments reported from $300m to $980m; retain ~5,000 workers | Nearly identical template: low price, heavy investment and employment commitments, Chinese industrial buyer. **The state's price expectation for MSK is likely low; its obligation expectation is likely high.** |
| **HIP-Petrohemija → NIS (2021)** [FACT] | €150m for 21%→90% | €150m capitalisation, new 140kt polypropylene complex | The state will accept a strategic partner taking majority control of a petrochemical asset in exchange for committed capital |
| **HIP-Petrohemija debt restructuring** [FACT] | — | €254m of NIS debt: 52.3% converted to equity, 47.7% written off | **Precedent for writing off and converting legacy debt before a strategic entry.** MSK's Srbijagas gas debt should be dealt with the same way — as a precondition, not inherited |
| **MSK itself** [FACT] | — | Srbijagas became majority owner via debt conversion; the government has publicly framed restructuring as preparation for new strategic partners | The counterparty is Srbijagas/the state and the stated policy direction already favours a partner |

Sources: [bne IntelliNews](https://www.intellinews.com/serbia-to-sell-zelezara-smederevo-to-china-s-hbis-94453/), [Interfax](https://interfax.com/newsroom/top-stories/73471/), [SeeNews — Petrohemija restructuring](https://seenews.com/news/serbian-court-approves-hip-petrohemija-debt-restructuring-plan-report-1113468), [SeeNews — MSK restructuring prior to partial sale](https://seenews.com/news/serbia-analyses-restructuring-of-msk-kikinda-prior-to-partial-sale-pm-1123049).

**The most actionable precedent in this entire section:** HIP-Petrohemija's €254m of debt was restructured — half converted, half written off — *before* NIS took 90%. [RECOMMENDATION] Make an equivalent treatment of MSK's legacy gas debt a **condition precedent** to the transaction. Inheriting it would consume the equity value the founder is negotiating over.

---

## M. Investor-type matrix

Derived from Table 14 — achievable IRR on this asset is ~11.7% hold / ~11.4% under a capped call.

| Investor type | Target IRR | Cheque | Accepts minority? | Accepts founder control? | Serbia? | Brownfield chem? | Founder call? | **Verdict** |
|---|---:|---|:--:|:--:|:--:|:--:|:--:|---|
| Large-cap buyout PE (Apollo, KKR, Carlyle, Advent) | 18–22% | ✓ | rarely | no | some | some | no | **Do not approach** |
| Distressed / opportunistic (Oaktree, Lone Star) | 20–25% | ✓ | sometimes | no | yes | yes | no | **Do not approach** |
| Industrial turnaround specialists | 20%+ | ✓ | no | no | yes | yes | no | **Do not approach** |
| Mezzanine / private credit | 12–15% coupon-led | ✓ | n/a | **yes** | yes | cautious | n/a | **Approach** — for the junior tranche only, not the whole cheque |
| **Infrastructure / value-add funds** | 12–14% | ✓ | **yes** | **yes** | yes, via CEE mandates | **only if contracted** | possibly | **Primary target — conditional on offtake** |
| **Family offices / permanent capital** | 10–13% | €30–80m | **yes** | **yes** | yes | yes | **yes** | **Primary target** |
| **Strategic industrial / chemical** | strategic, ~12% | ✓ | **yes** | negotiable | yes | **yes** | yes | **Primary target** |
| **Chinese state / industrial groups** | strategic | ✓ | yes | often demands control | **yes** | **yes** | rarely | **Approach with care** — see below |
| Commodity traders (Vitol, Trafigura, Glencore) | 15–20% on capital, but motivated by flow | ✓ | **yes** | **yes** | yes | yes | **yes** | **Strong fit, under-considered** |
| Sovereign wealth (Gulf, Azerbaijan) | 10–12% | ✓ | yes | yes | yes | yes | possibly | **Approach** — slow |
| EBRD / IFC / DFIs | 8–12% + development mandate | €20–50m | **yes** | **yes** | **yes — core mandate** | yes, with ESG conditions | yes | **Approach early** — see below |

### Four observations the brief does not anticipate

**Commodity traders are the most structurally compatible counterparty and are missing from the brief.** A trader's return does not come only from the equity — it comes from the offtake flow. They will therefore accept a lower equity IRR than any fund, routinely take minority positions, do not want operational control, and are comfortable with a founder call because the offtake agreement survives it. They also solve the offtake problem (item 2 on the efficient frontier) *in the same transaction*. [RECOMMENDATION] Approach a trader early, structured as equity + a long-term offtake.

**DFIs are missing from the brief and are unusually well-matched.** EBRD and IFC lend into exactly this profile, accept minority positions, do not seek control, and their presence is the strongest available signal to commercial lenders. Their conditions are ESG and governance discipline, not ownership. The cost is time and process.

**On Chinese industrial groups.** They bring EPC, ECA-backed financing and genuine appetite for Serbian industry — the Smederevo precedent is real. But the Smederevo template was an **outright acquisition with the Chinese party in control**, not a minority investment behind a Serbian founder. [INFERENCE] The likeliest Chinese proposal is one where they take majority control and the founder becomes a local partner with a modest stake. That may still be the highest-probability route to the plant actually restarting, but it is not the structure the brief asks for. **Be clear which objective ranks higher before entering that room.**

**The right approach order:** (1) commodity trader with offtake, (2) family office / permanent capital, (3) EBRD/IFC alongside, (4) infrastructure fund once offtake is contracted, (5) strategic chemical, (6) Chinese industrial as fallback. Do not approach PE at all.

---

## N. Negotiation strategy

| Term | **Opening** | **Target** | **Fallback** | **Walk-away** |
|---|---|---|---|---|
| Founder economics | 70% | **60%** | 55% | **Below 51%** |
| Founder votes | 70% | **60%** | 51% | Below 51% |
| Investor cash | €82m | €82m | €100m | — |
| Investor instrument | 80% SHL / 20% equity | **58% SHL / 42% equity** | 50/50 | All-equity |
| SHL coupon | 7% | **9%** | 11% | Above 12% (non-deductible above ~30% of EBITDA) |
| PIK | none | **construction + 1 ramp year** | +2 ramp years | Any PIK beyond Year 5 |
| Blended investor IRR | 11% | **12–13%** | 14% | **Above 14%** |
| Investor MOIC cap | 1.8x | **2.10x** | 2.25x | Above 2.5x |
| Board | 4 / 1 | **3 / 2 of 5** | 3 / 2 with CFO carve-out | Any structure without a founder majority |
| Budget veto | none | **deemed approval, prior year + CPI** | approval with expert determination | Unqualified investor budget veto |
| Refinancing veto | none | **none** | falls away below 2.5x leverage | Any permanent refinancing veto |
| Liquidation preference | none | **1.0x non-participating** | 1.25x non-participating | **Any participating preference** |
| Founder call | lesser of 12% IRR / 1.5x, from Y8 | **greater of 12% IRR / 1.6x, capped 2.10x, Y10–12 window** | cap 2.25x | Uncapped, or IRR-ratchet only |
| Investor put | none | **Y12, at FMV, subject to financing availability** | Y10 FMV | Put at a fixed premium, or unconditional |
| Cost overrun | contingency + LSTK + standby | **layers 1–4 of Section I** | layer 5 | **Any automatic equity conversion or discounted cure** |
| Personal guarantee | none | **none** | none | **Any recourse beyond ProjectCo shares** |
| Transfer restrictions | full veto | **ROFR + tag + no transfers to a named competitor list** | ROFO + tag | Free transferability to any party |

**Two negotiating notes.** First, the walk-away lines that matter are the *personal guarantee*, the *overrun mechanism* and the *uncapped call* — not the percentage. A founder at 55% with no personal guarantee and a clean overrun waterfall is in a far stronger position than a founder at 60% with a completion guarantee and a discounted equity cure. Second, concede in the order set out in Section J: technical diligence and offtake first, coupon and preference second, governance detail third, and equity percentage last.

---

## O. Draft indicative term sheet

See [`TERM-SHEET.md`](./TERM-SHEET.md) — a two-page non-binding indicative term sheet drafted to be shown to a serious investor.

---

## Section 19 — Multiple-project strategy

The brief's instinct here is correct and it is the most valuable structural idea in the whole document.

```
                    Founder HoldCo (Trade Unique Industrial)
                    100% founder-owned. No investor ever.
                             |
        +--------------------+--------------------+-------------------+
        |                    |                    |                   |
   MSK ProjectCo        Project 2 SPV        Project 3 SPV      Services Co
   Founder 60%          Founder 70%          Founder 65%       100% founder
   Investor 40%         Investor B 30%       Investor C 35%
```

**Rules for keeping this clean:**

1. **Investors invest at SPV level only.** Never at HoldCo. The moment an investor holds HoldCo equity they participate in every future project.
2. **No cross-collateralisation and no cross-default between SPVs.** A failure at MSK must not reach Project 2. This is the single clause that preserves the platform.
3. **Beware the "right of first refusal on future projects" clause.** Investors ask for it routinely and it sounds harmless. It is the mechanism by which a single-project investor becomes a permanent partner. [RECOMMENDATION] Offer at most a **time-limited right to be shown** the next project (90 days, no matching right, expiring after 3 years), and never a right to participate on agreed terms.
4. **The Services Co is where the platform value accrues.** A 100%-founder-owned entity providing management, technical and procurement services to each SPV under an arm's-length agreement approved as a related-party transaction gives the founder (a) cash flow from Year 1, independent of distributions, which directly solves the Year 5 liquidity problem in Section E, and (b) a growing asset no project investor owns. [RECOMMENDATION] **Set this up at the same time as ProjectCo, not later** — introducing it after an investor is in requires their consent as a related-party transaction, and they will price it.
5. **When HoldCo-level capital does make sense:** only after 2–3 assets are operating and generating distributions, when a HoldCo facility secured on the portfolio is cheaper than project-level equity. That is a Year 8–12 decision, not a Year 1 one.

[INFERENCE] This is essentially how INEOS was built: a small management-controlled holding vehicle, with acquisition-level financing raised separately against each acquired business.

---

## Section 25 — The final decision

The brief asks me to sit simultaneously as the founder, as the investment committee of a €10bn private-capital firm, and as the senior lender, and find the one structure all three can rationally sign.

### The structure

| Term | Value |
|---|---|
| **Founder ownership** | **60%** economics, **60%** votes |
| **Investor ownership** | **40%** economics, **40%** votes |
| **Senior / project debt** | **€152m** (65% of a €233m funding need), ECA-backed where obtainable |
| **Investor equity** | **€34m** |
| **Investor shareholder loan** | **€47m** |
| **Loan coupon** | **9%**, cash-pay subject to a 1.20x DSCR test |
| **PIK period** | **Construction plus the first ramp year only** (~4 years from close) |
| **Expected investor IRR** | **11.4–11.7%** |
| **Expected investor MOIC** | **2.10x** (capped) **to 2.9x** (hold to Y15) |
| **Founder board seats** | **3 of 5** |
| **Investor board seats** | **2 of 5** |
| **Founder call begins** | **Year 10**, 24-month window |
| **Call price formula** | **Greater of (a) the amount giving the investor a 12% gross IRR on all cash invested, net of all cash previously received, and (b) 1.6x total invested capital less all cash previously received — the whole capped at 2.10x total invested capital.** Conditional on refinancing availability; no penalty for non-exercise. |
| **Investor fallback exit** | Put at Year 12 at independent fair market value, subject to financing availability; plus tag-along, ROFR, and drag only above an agreed minimum price with a 2.10x floor to the investor |
| **Personal founder guarantee** | **None.** Recourse limited to ProjectCo assets and the founder's ProjectCo shares |
| **Cost-overrun mechanism** | Layers 1–4 of Section I: 10% contingency, LSTK wrap with a 10% performance bond, committed standby senior tranche, then pro-rata subordinated overrun loans. Equity issuance only at independently determined fair value, as a last resort |
| **Who controls management** | **The founder.** CEO and all officers appointed by the founder; the investor may require removal of the CFO for cause only |

### Maximum terms the founder should concede before walking away

- Economics to 51%, **never below**
- Votes to 51%, **never below**
- Blended investor IRR to 14%; MOIC cap to 2.25x
- Coupon to 11%; PIK to Year 5
- 1.25x **non-participating** preference; never participating
- Board 3/2 with an investor-appointed chair having **no** casting vote
- Call deferred to Year 12

**Absolute walk-aways:** any personal guarantee or recourse to Trade Unique assets; any automatic or discounted equity cure on cost overrun; any participating liquidation preference; any permanent investor veto over refinancing; any unqualified budget veto without deemed approval; any investor consent requirement on exercise of the founder call.

### Would I sign this as founder?

**Yes — but conditionally, and the conditions are not financial.**

On the terms above the founder builds a €200m+ net worth over fifteen years having contributed no cash, retains operational control throughout, risks no personal assets, and holds a capped option to reach 100%. That is an excellent outcome for a development contribution.

I would **not** sign it today, because three conditions precedent are unmet, and signing before they are met converts a good structure into a bad deal:

1. **An independent engineering study confirming that €200m delivers €40m+ of sustainable EBITDA.** The model says the structure works at €46m, survives at €35m, and is worthless below €30m. The investor red team (Section J) argues a gas-fed refurbishment plausibly earns €10–20m. **This is not a detail — it is the whole question**, and nothing else in this study matters if the answer is €18m.
2. **Legacy gas debt to Srbijagas written off or converted before entry**, on the HIP-Petrohemija precedent.
3. **A Phase II environmental assessment and a statutory carve-out for pre-closing contamination.**

### Would I invest in it as the investor?

**Yes — if I am the right kind of investor, and no otherwise.**

As an infrastructure fund, a family office, a commodity trader with an offtake motive, a strategic chemical group, or a DFI: 11.4–11.7% IRR at 2.1x with a 9% cash-pay coupon, a 1.57x minimum DSCR, ECA-backed senior debt, a 1.0x preference and a capped exit is a rational risk-adjusted return, **provided** the offtake is contracted and the technical case is independently verified.

As a private-equity fund with an 18%+ hurdle: **no, at any ownership split.** And I would not spend six months discovering that.

Both answers are yes within their intended universe, so I am not redesigning further. The remaining work is not structuring — it is the engineering study, the offtake, and the legacy-liability cleanup. **Those three items are worth more than every percentage point in this document.**

---

## Sourcing note and limitations

Market return benchmarks are drawn from: [PwC Private Credit Survey 2026](https://www.pwc.com/gx/en/industries/private-equity/private-credit-survey.html), [With Intelligence Private Credit Outlook 2026](https://www.withintelligence.com/insights/private-credit-outlook-2026/), [MetLife Investment Management on infrastructure debt](https://investments.metlife.com/insights/private-capital/infrastructure-debt-a-compelling-private-credit-portfolio-addition/), and [Opale Capital on 2026 PE returns](https://www.opalecapital.com/en/blog/private-equity-returns-2026). Infrastructure debt spreads in 2026 were reported at roughly +200–250bp for investment grade, +325–400bp for BB, and +425–650bp for low-BB/single-B; mezzanine blended IRR targets at 15–20%.

**What I could not verify, and did not invent:**

- The detailed tranching of the INEOS 2005 Innovene facilities, and the arrangers' roles.
- The terms on which Murray Johnstone exited its 1998 Ineos stake.
- The 1995 Karmet acquisition financing split.
- MSK Kikinda's current operating status, order book, balance sheet, headcount, legacy debt quantum and environmental position as at 2026. **The €40m acquisition price is an illustration derived from the Smederevo and Petrohemija comparables, not a valuation.**
- Whether Sinosure or China Exim have any appetite for this specific asset.
- Any current Serbian government policy or timetable for a sale of MSK.

**The largest single limitation:** the base-case EBITDA of €46m is an input this study was asked to use, not an output it derived. Section J sets out why it may be materially optimistic for a gas-fed refurbishment, and Table 12 shows the structure's behaviour when it is wrong. Commission the engineering study before using any number in this document in a negotiation.
