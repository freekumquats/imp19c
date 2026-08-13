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

## Related files
- `audits/SCRATCH_CURRENCY_23.md` — full working history: every hypothesis tried on this bug, and the
  adversarial review that refuted each one. Not committed to git; local reference only.
- `design/DESIGN_112_ZEROSTOCK_PRICE_GUARD.md` — the design document for Finding 3's fix, including its
  three revisions and the reasoning that rejected the first two.
- `tools/curx_analyze.py` — the log-analysis tool used throughout this investigation; reads the
  `IMP19C CURX`/`CURXV`/`TZP` debug-log tags and reconstructs the currency chain per quarter.
