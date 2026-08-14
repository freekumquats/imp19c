# AUDIT — #23 currency period-2 oscillation, then persistent deflation (FINALIZED findings only)

**Purpose:** this file holds only what was CONFIRMED and survived adversarial review. The full working
history — every hypothesis tried, and why each was refuted — lives in `audits/SCRATCH_CURRENCY_23.md`
(not committed; local working notes). Do not re-propose anything from that file without new evidence.

## ACCEPTANCE CRITERIA (user, 2026-08-09) — the fix must produce PLAUSIBLE results, not just stop oscillating
The bug is NOT "fixed" merely when the period-2 oscillation stops. The corrected system must settle to
steady-state values that are HISTORICALLY PLAUSIBLE. Concretely, a `-debug_mode` boot must show:
- `CURRENCY_essentials_buying_power` (the Economy-tab "cost of living") settling to a stable value whose
  tael-equivalent is in the right ballpark vs the historical Qing peasant subsistence budget. YARDSTICK
  (research/QING_COST_OF_LIVING_1763.md): bare-bones subsistence ≈ **~5 taels/adult/yr**
  (Allen et al. 2011); **~15–22 taels/family/yr**; rice ≈ **1.0–1.5 taels/shih** (Wang Yeh-chien 1972);
  silver ≈ **700–1,000 wén/tael**.
- inflation/deflation % resting near 0 in a well-run economy (not pinned at a ±rail);
- private_cash_ratio near 1 (not 1.5 ⇄ 0.01);
- the other currency-chain outputs (ratio, need, circ, silver price) plausible and stable.

## FINDING 1 — CONFIRMED, FIXED (2026-08-09): the `sqrt` primitive was mathematically broken
**Root cause.** `sqrt` (`common/scripted_effects/se_ECON_functional.txt:56-111`, the shared Babylonian-
method primitive) had its recurrence inverted (`y = x/param`, should be `y = param/x`) AND a signed
(not absolute-value) convergence guard. Effect: for `base < 1`, the loop never ran and the input was
returned raw, unrooted; for `base > 1`, the recurrence decayed geometrically to ~0 instead of converging
to √base. `gbip = sqrt(Σ price×share)` (the ONE live caller, `se_GLOBALTRADE_split.txt:2701`) rail-slammed
between "≈base" and "≈0.005" every time the pre-sqrt base crossed 1.0 — a mundane, plausible ~0.7⇄1.3
wobble one quarter to the next, turned into a ~250× oscillation by the broken primitive. This produced the
original period-2 currency oscillation (inflation ⇄ deflation-floor every quarter).

Hand-traced against the exact-tick log and confirmed to match every observed high/low exactly (see
git history for the full trace). Two coupled defects, both required: the inverted recurrence, and the
signed guard that skips the loop entirely for `base < 1`.

**Fix implemented** (`se_ECON_functional.txt:56`): corrected Babylonian method, seed `x=param, y=1`,
recurrence `y = param/x` (was `x/param`), bounded `count = 12` (quadratic convergence reaches √N in ~7
iterations for any realistic base; idempotent once converged, so it cannot hang regardless of the
engine's fixed-point resolution — this replaced an epsilon-based guard that was shown to risk an infinite
loop at load under 3-decimal fixed-point). Blast radius: exactly one caller (gbip), zero collateral.

**Status: implemented, code-reviewed PASS, boot-confirmed by the user.** The old oscillation signature
(gbip toggling 0.003⇄0.88) does not recur in any log gathered after this fix.

## FINDING 2 — CONFIRMED, standing mechanism: a zero-stockpile zone contributes ZERO to the world price
`GT_split_get_global_import_unit_price_tradegood` (`se_GLOBALTRADE_split.txt:2585-2745`) blends all 22
trade zones' `local_price` into the world price `gbip`, each zone weighted by
`percentage_of_global_stockpile` — a ratio that is guarded to exactly 0 whenever that zone's own
stockpile is 0 (`:1467-1480`). So however extreme a zone's `local_price` gets while its stockpile is
empty, its contribution to the WORLD price (`gbip`) is `(spiked price) × 0 = 0`. This was the basis on
which an earlier "empty-stockpile spike reaches the currency peg" theory was refuted (the peg reads
`country_unit_price`, which is built from this same zero-weighted blend, never from a single zone's raw
`local_price`).

This fact remains true and load-bearing: it is WHY the world-price blend was never the vulnerable path,
and it is what threw the investigation onto the correct path — the trade-PAYMENT site, which (per
Finding 3) does not have this same protection.

## FINDING 3 — CONFIRMED mechanism, FIXED (2026-08-13): the trade-payment site paid a zero-stockpile
## zone's raw, un-normalized price directly, with no protective weighting
Commits `2b7142977` (#112, "regional import pricing") and `7663239b1` (#115, "both model") changed
`GT_split_update_wealth_owed_for_tradegoods` (`se_GLOBALTRADE_split.txt:2498-2577`) — the effect that
turns a governorship's import order into a real currency payment — from reading the zero-weighted
BLENDED price (`country_unit_price_$tradegood$`, the safe value per Finding 2) to reading a single
zone's raw `local_price_$tradegood$` directly, with `min = 0.0001` guarding only the low side.

`local_price_$tradegood$` (`GT_set_tradegood_price`, `:6000-6032`) is `order_size / stockpile × 0.6`,
guarded so the divide is SKIPPED (not the assignment) when a zone's stockpile is 0 or unset — in that
case the "price" is the raw, un-normalized order count, with no relationship to actual scarcity.
Confirmed directly in a real boot log: `upper_yangtzi` (silver) sat at `stock 0` for every one of 29
logged quarters; `yellow_sea` began at `stock 0` and, once stock recovered, its price band dropped by
more than an order of magnitude — exactly the undivided-vs-divided transition #112's own commit message
had flagged as an open risk.

This is the confirmed, line-level-isolated mechanism by which #112/#115 removed a real protection at
exactly one call site. Whether it was the DOMINANT driver of the reported persistent ~-10% deflation was
never conclusively measured (multiple analysis attempts against the existing log — see
`SCRATCH_CURRENCY_23.md` — could not settle this without a fresh boot), but per user instruction the
goal was to find and correct the single most-likely defective line, not to first prove its exact
magnitude.

**Fix implemented** (`se_GLOBALTRADE_split.txt`, `GT_split_update_wealth_owed_for_tradegoods`): the
payment multiply is now guarded on the SAME stockpile condition `GT_set_tradegood_price` already uses
(`has_global_variable = $tradezone$_stockpile_$tradegood$` + `> 0`) — a zone with no stockpile to sell
from contributes ZERO payment for that good this quarter, rather than being charged against the raw
order count. Regional pricing (#112/#115's actual feature) is completely unaffected for every zone that
has real stock, which is the common case. Reviewed through three design revisions (a first draft
substituting a fallback price was rejected on economic grounds — no sale occurred, so no price, even a
"safe" one, should be charged; a second draft's guard syntax and blast-radius analysis were both found
wrong by adversarial review) before landing on this minimal, zero-blast-radius shape. Passed adversarial
design review and a final boot-crash review.

**Status: implemented, reviewed, committed. Awaiting boot confirmation.** Diagnostic logging was added
alongside the fix (`natexp`, `wvuraw`, `poptick`, `wealthgen` exact-tick tags, a rescaled `need` past its
old display cap, and a hit-counter on the new guard) so the next boot can directly confirm the guard
fires and measure its effect on `TRADE_national_expenditure`.

## FINDING 4 — CONFIRMED reusable technique: recovering `need`'s true value past its own display cap
`CURRENCY_private_cash_needed` ("need")'s exact-tick log line hit its own display cap on many quarters
in a real boot, making its true magnitude unmeasurable directly. It can be recovered without a new boot:
`CURRENCY_private_cash_ratio = circ × 0.004 / max(need, 0.01)` (`CURRENCY_svalues.txt:753-766`, `circ` =
`CURRENCY_amt_circulated_scaled`) — both `circ` and `ratio` are independently exact-logged and, in the
boot checked, never approached their own caps. So `need_true = circ × 0.004 / ratio` recovers the real,
uncensored `need` for every quarter, using only already-logged data — verified correct by adversarial
review (the floor never binds in practice; the three values are read from one synchronous log call, so
there is no risk of reading them at different moments).

**This is a standing, reusable diagnostic technique for any future currency-chain question on this
system** — it does not need to be re-derived or re-reviewed each time. It does NOT by itself establish
which of `need`'s inputs drives a given swing (a separate causal question, addressed in Finding 3 above
by a different route) — it only removes the display-cap censoring so that question can be asked with
real numbers.

## FINDING 5 — DIAGNOSED (revised 2026-08-13 after adversarial review found the first draft aimed
## at the wrong function and the wrong "ruled out" list). Root mechanism unchanged; the real income
## conduit and the real dominant channel are corrected below.
**The core mechanism (unchanged, still correct).** `GT_set_tradegood_price`
(`se_GLOBALTRADE_split.txt`, ~6044-6127) computes `local_price_$tradegood$ = zone_total_order_size /
zone_stockpile × 0.6` (the divide is SKIPPED, not the whole calculation, when stockpile is 0/unset —
Finding 3's fix covers exactly this skipped-divide case, and ONLY this case).
`GT_split_update_wealth_owed_for_tradegoods` (~2498-2621) then sets
`wealth_owed_for_$tradegood$ = this_governorship's_own_order_size × local_price_$tradegood$`. For a
zone stockpile of exactly 1 unit, this gives a large number (own_order × zone_total_order × 0.6). But
at a normal, non-thin stockpile the term is much smaller and close to linear — the first draft's
"1,500,000" example only holds at stockpile = 1, an extreme case, not a typical one. **This finding
does NOT yet prove the effect is large at typical stockpile levels — that is still open (see
Confidence below).**

**CORRECTED: the treasury-income conduit is a DIFFERENT function than the first draft named.**
The first draft cited `GT_split_calculate_actual_share_of_expenses_category` (seller=the_state).
That function computes a COST (its value is sign-flipped negative, ~4207-4210) — it cannot explain
income being too high. The real income conduit is `GT_split_calculate_actual_share_of_income_category`
(~4083-4092), called for EVERY seller — the_state AND every pop stratum — inside
`GT_split_distribute_income_category` (~4094-4176). Each call reads the SAME `wealth_owed`-derived
`trade_income_due_$category$` and scales it by that seller's own share weight.

**CORRECTED: income tax and tariffs are NOT independent of this mechanism — withdrawn from the
"ruled out" list.** `INCOME_governorship_income_tax_upper_strata`
(`INCOME_svalues.txt:622-642`, confirmed by direct read) adds
`this_income_from_manufacturing_upper_strata` and `this_income_from_shipping_upper_strata` straight
into the income-tax base. These are the SAME `wealth_owed`-derived values as the_state's own share,
just read for a different seller. Property tax and the cost-of-living excise duty remain
independently clean (confirmed: they read population/housing counts and `WEALTH_cost_of_living_*`,
not `wealth_owed`).

**CORRECTED AGAIN (second review found the first correction cited a dead/parallel file with wrong
numbers): the state-vs-strata weight gap is real but its size is NOT yet proven.** The live weights
come from `GT_split_calculate_all_trade_shares` (`se_GLOBALTRADE_split.txt:3977-4021`), not from
`GT_svalues.txt` (that file's `GT_trade_share_*` values are dead/unread by the income split — wrong
citation, now withdrawn). For the manufacturing category, the live call sets `the_state = 0.001` and
`upper_strata = 0.6` (`:4013-4014`) — a ~600× gap in the RAW weight, before population scaling.

But `GT_split_calculate_trade_shares` (the function that actually applies these) then multiplies
`trade_share_$category$_the_state` by `governorship_population` (the WHOLE population) and
`trade_share_$category$_upper_strata` by `governorship_upper_strata` (only the upper stratum's own,
much smaller population) — `:5704-5711`. This narrows the effective gap by an unknown amount,
depending on what fraction of a governorship's population is upper strata (not looked up in this
pass). The income-tax channel is also discounted by `INCOME_taxrate_income_tax` (a tax rate,
`INCOME_svalues.txt:655-656`), while the state's own channel is not. **Whether income tax or the
state channel is the larger contributor in practice is still an open, unproven question** — this
finding does not pick a winner between them.

**Status: PARTIALLY DIAGNOSED, mechanism confirmed real, magnitude and dominant channel NOT yet
confirmed.** The order_size/stockpile-driven `wealth_owed` inflation is a real, unfixed gap in
Finding 3's guard (confirmed: the guard only fires on exact-zero/unset stockpile,
`se_GLOBALTRADE_split.txt` ~2549-2550) — but whether it is actually large at TYPICAL (not
worst-case) stockpile levels, and which channel (income tax vs. the state's own share) dominates in
practice, are both open questions. This finding does NOT yet meet the bar needed to move to a design
pass; it needs the fresh-boot step below first.

**Next step, before any design work.** Get one fresh boot with the Finding 3 fix's own diagnostic
tags populated (`ECON_LOG_curx_natexp`, `ECON_LOG_curx_zerostock_guard`), and read the actual
stockpile values for a few real goods/zones at that point — not the worst-case stockpile=1 example.
If typical stockpiles are close to order size (not near-zero), this mechanism is likely small and a
different, still-unfound cause may explain task #30. If typical stockpiles ARE thin, this mechanism
is likely real and large, and the design pass should target the income-tax channel first, not the
state's own tiny channel. Tracked as task #30 (existing) — this finding is a partial diagnosis for
that task, not a finished one, and not yet a fix.

**Confidence: medium on the mechanism being real** (the order_size/stockpile shape and the
uncovered-by-Finding-3 gap are both confirmed by direct code reading); **low on the mechanism being
the DOMINANT driver at typical (non-worst-case) stockpile levels** — this has not yet been checked
against real numbers, and the first draft's "1,500,000" example only holds at an extreme,
unrepresentative stockpile value. The only log available also predates the Finding 3 fix by ~7
hours, so it cannot show the post-fix state either.

## FINDING 6 — fresh boot (logs.zip Aug-14 02:10, 5 Dec 1763 → past 3 Jun 1766, 29 PRE/POST
## quarter-marks) — answers part of Finding 5's "next step", rules out 3 treasury-spike
## hypotheses, and surfaces one new instrumentation gap. NOT the currency-oscillation bug;
## this is the separate "treasury jumps ~2-3x more than the displayed quarterly income every
## other quarter" symptom the user reported live during this same boot.

**RULED OUT — quarterly pulse double-firing.** Grepped every `IMP19C CURX QUARTER-MARK
PRE/POST` line's wall-clock timestamp directly from debug.log: all 29 are evenly spaced
(30s-5min apart), no two ever land back-to-back. `INCOME_update_treasury_country` (the ONLY
`add_treasury` call reading the cached `INCOME_national_total_quarterly` var that the topbar
"Change" text also reads, `gui/ingame_topbar.gui:801`) is called from exactly one recurring
site (`oa_wealth_changes.txt:206`, inside `quarterly_trade_pulse`) plus two ONE-TIME sites
(`on_game_initialized`, `FUNC_setup_new_country`) that cannot produce a recurring alternating
pattern. The topbar "Change" number and the actual `add_treasury` amount read the exact same
variable — they cannot legitimately diverge from each other by construction.

**RULED OUT — reserve-selling / deficit mitigation.** `INCOME_mitigate_deficit` (which DOES
call `add_treasury` on its own, outside the cached-var path above) only fires when
`treasury < 0`. Zero occurrences of its LOG_enter, `DEBT_events.1`, or `negative_treasury`
anywhere in this boot's debug.log — CHI never went into deficit this run. Ruled out for this
boot; may still be worth re-checking under an actual deficit run.

**RULED OUT (as a double-count) — "Tariffs and shipping" vs "Tariffs" magnitude gap.**
The topbar tooltip's "Tariffs and shipping" (`INCOME_national_total_from_tariffs_and_shipping`,
`INCOME_svalues.txt:43-49`) sums `INCOME_governorship_tariffs_and_shipping` across EVERY
governorship via `every_governorships`. The Economy tab's "Tariffs +74.173 (7.5% rate)" line
is ONE governorship's own `INCOME_governorship_tariffs_total_positive` figure. An empire-wide
total being ~20-40x one governorship's figure, for Qing's dozen-plus governorships, is the
expected shape of a sum — not a double-count. **However, a real defect was found in the same
read:** `INCOME_governorship_tariffs_and_shipping = tariffs_total_positive + state_port_charges`
(`INCOME_svalues.txt:184-189`), and `INCOME_governorship_state_port_charges`
(`:829-843`) reads `this_income_from_shipping_the_state` / `this_expenses_from_shipping_the_state`
— grepped across all of `common/`, **these two vars are never `set_variable`'d anywhere**. The
"shipping" half of "Tariffs and shipping" is dead code, always contributing exactly 0; the line
is really just "Tariffs" (summed nationally) under a misleading label. Cosmetic, not a magnitude
bug, but worth a follow-up: either wire real shipping income into these vars or rename the line.

**STILL OPEN, but advanced with real data — Finding 5's thin/zero-stockpile `wealth_owed`
mechanism.** This boot is the "fresh boot" Finding 5 asked for. `tools/curx_analyze.py`'s
oscillation summary shows **16 of 22 trade zones TOGGLE stock band across the 29 quarters**,
and at least 9 zones (`east_europe`, `east_mediterranean`, `east_north_america`, `india`,
`indo_china`, `south_east_asia`, `upper_yangtzi`, `west_africa`, `western_steppe`,
`yellow_sea`) pass through an exact `stock=0` state at some point — the thin/zero condition
Finding 3's guard targets is the COMMON case for most zones, not a rare edge case. Order size
for most zones sits in a comparatively stable 10-100 band (100-1000 for `india`, consistently)
while stock swings far more widely (0 to 100-1000) — so when a zone's stock dips into
thin-but-NONZERO territory (1-10, 0.1-1), `order/stockpile` spikes, and Finding 3's guard
(which only fires at EXACT zero/unset stockpile, confirmed unchanged) does NOT catch it. This
corroborates Finding 5's open hypothesis that the thin-stock gap is live and frequent.

**But a genuine negative data point against it being the DOMINANT driver:** `natexp`
(`TRADE_national_expenditure`, the exact metric Finding 3's fix added specifically to measure
this channel) stayed NEGATIVE and near-zero (coarse band "abs 0-10k", exact tick = 0) across
ALL 29 quarters of this boot — confirmed genuinely SET every quarter (zero hits on its own
"= UNSET" log branch), not an unread/uninitialized var. If wealth_owed-driven expenditure were
spiking from the thin-stock local_price blowups, this expenditure-side metric should show it;
it doesn't, in this run. This does NOT clear the income side (tariffs/income-tax also read
wealth_owed, and natexp is expenditure-only) — so Finding 5 remains open, now narrowed: the
thin-stock gap is confirmed frequent, but its effect (if any) must be showing up on the
INCOME side, not the expenditure side measured by natexp.

**NEW — instrumentation gap found, not yet a claim about the economy.** `wealthgen`'s
exact-tick probe (`se_ECON_LOG.txt:829`, the `IMP19C CURXV LABEL wealthgen` line) has NO
matching coarse-band `IMP19C CURX wealthgen ...` call anywhere in the codebase (only `natexp`
got one, at `se_ECON_LOG.txt:652`) and reads exact 0 for all 29 quarters. Not yet distinguished
whether wealth-generation is genuinely near-zero this boot or this specific probe is unwired
to a live source — flagged for whoever picks up Finding 5 next, not investigated further here.

**Inflation (7%→22% reported by the user across this same boot) — separate mechanism, real
and structural, not a bug in the sense of a broken formula.** The CHI currency-chain exact
values show `ratio` and `gbip` making a PERMANENT step up between quarter-index 10 and 11
(ratio 1.26→2.00, gbip 0.996→1.002 crossing into the next display band) and then **staying
elevated for the remaining 18 quarter-marks** — a one-time regime shift, not a returning
oscillation (the #23 bug this doc otherwise tracks was periodic and was fixed in Finding 1).
`infl`'s coarse band moves in lockstep (settles at ">= 10pct" from the same index onward, per
the CHI CURRENCY CHAIN table). This is consistent with the reported 7%→22% climb: once `ratio`
(a trade-wealth/reserve valuation ratio) steps up, `infl` steps up with it and does not revert,
because nothing in this system currently pulls `ratio` back down once trade wealth outgrows
reserves — matching the standing `imp19c-no-restoring-drift-ratchet-rule` diagnosis for other
passive metrics in this codebase. Whether the step is a REALISTIC consequence of a genuinely
growing trade economy (more governorships/trade volume outpacing metal-reserve growth) or is
itself partly fed by the same thin-stock `local_price` inflation from Finding 5 was not
distinguished this pass — `ratio`'s own upstream inputs (`wvuraw`, agsilver) were not traced
back to `wealth_owed` in this session. Not escalated to a new numbered finding pending that trace.

## Related files
- `audits/SCRATCH_CURRENCY_23.md` — full working history: every hypothesis tried on this bug, and the
  adversarial review that refuted each one. Not committed to git; local reference only.
- `design/DESIGN_112_ZEROSTOCK_PRICE_GUARD.md` — the design document for Finding 3's fix, including its
  three revisions and the reasoning that rejected the first two.
- `tools/curx_analyze.py` — the log-analysis tool used throughout this investigation; reads the
  `IMP19C CURX`/`CURXV`/`TZP` debug-log tags and reconstructs the currency chain per quarter.
