# Existing economy log-flood — investigation & fixes (task #19)

Branch `merge-overnight`. Mandate: fix what is low/med-risk in the economy trade-engine log flood
(`oa_wealth_changes` ~4000+ errors); **leave high-risk alone** (explicit operator instruction).
Static-verified only — no boot this session; every change is boot-pending. Commits authored freekumquats.

## Source of truth
Real logs extracted from `~/Downloads/logs.zip` → `/tmp/imp_logs/logs/error.log` (33,601 lines,
one boot session 02:50–02:57 on 2026-07-20). Per [[imp19c-stale-log-vs-git-rule]] I verify every
candidate against **git HEAD**, because parts of this log predate fixes already in the tree.

## Error census (normalized, top economy classes)
| count | error | verdict |
|------:|-------|---------|
| 2568 | `change_variable ... Variable not of the 'value' scope type. Type: empty` | mostly STALE (see A) + LIVE trade-split (see B) |
| 1866 | `oa_wealth_changes.txt:166; ECON_LOG_production_snapshot line: 8/9` | **STALE** — already fixed 2026-07-11 (6b2c4d9f6) |
| 644  | `Event target link 'var' returned an unset scope` | **LIVE** — trade-split unguarded stockpile read (B) |
| 444  | `Invalid left side during comparison 'var'` | **LIVE** — same root as B |
| ~1900| `GT_split_*` chains (declare_sell_amount / create_order_tradegood) | **LIVE** (B) |
| 417  | `Unexpected token: is_triggered_only` (event files) | **STALE** — event files brace-balanced at HEAD |
| ~270 | `Failed to read key reference octere/liburnian` + `Unexpected token: secondary` | pre-existing, OUT OF SCOPE (C) |

## A) ECON_LOG_production_snapshot flood (1866 lines) — REAL BUG, FIXED (my earlier "stale" call was WRONG)
**Correction.** I first dismissed this as stale (claiming the log predated the 2026-07-11 fix 6b2c4d9f6).
The operator corrected me: the log is from a **2026-07-19** build, which CONTAINS that fix — so the error
is genuinely still firing, and the July-11 fix was INCOMPLETE. Root cause found by reading the scope, not
the line numbers:
- `ECON_LOG_production_snapshot` runs inside `every_country` (oa_wealth_changes.txt:166), so `this` = the
  iterated country and `root` = the on_action origin — DIFFERENT scopes.
- The temp vars were INITIALISED with `set_variable` on bare `this` (relative lines 8-9) but INCREMENTED
  with `change_variable` inside `root = {}` (lines 21-22). change_variable on root hit a var that was only
  ever set on `this` → "Variable not of the 'value' scope type. Type: empty", ~1860 lines/session.
- The July-11 fix only corrected the READ idiom (`prev.var:` → `scope:x.var:`) on the increment line and
  never noticed init-scope ≠ modify-scope.
- Comment-stripped relative line 8/9 in the CURRENT file = the two `change_variable`s inside root — exactly
  what the 07-19 log points at. (My "line 8 is now a harmless set_variable" claim used un-stripped numbers;
  the engine reports comment-stripped positions. That error is what let me talk myself into "stale".)
**FIX:** stage ALL temp-var ops (init, increment, cleanup) on `root` consistently — mirroring the working
`ECON_LOG_country_snapshot` sibling. Verified the other 3 snapshot effects: `country`/`currency` are
consistent (all-root); `jobs_snapshot` uses correct two-scope staging (accumulate on `this`, COPY to root
temps, clean both) — NOT the same bug, left as-is.

## B) LIVE: GT_split unguarded stockpile reads (the real remaining flood) — FIX
`GT_split_declare_sell_to_TZ_aggregate_stockpile` runs `every_tradegood_$type$_complex` (ALL trade
goods) on every governorship, applying `GT_split_declare_sell_amount`. That effect (se_GLOBALTRADE_split.txt:756)
does `limit = { var:$tradegood$_stockpile > DEMAND_$tradegood$ }` with **no `has_variable` guard**.
But `GOODS_setup_governorship_stockpiles` sets `X_stockpile` for RAW goods ONLY behind
`has_variable = produces_X` — so a governorship that does not produce good X never has `var:X_stockpile`.
Reading it → "Event target link 'var' returned an unset scope" + "Invalid left side during comparison
'var'" + "Variable not of 'value' type: empty", once per (governorship × non-produced good) = the
~4000-line flood. Identical bug in `GT_split_create_order_tradegood:2087` (`var:X_stockpile < DEMAND_X`).

**FIX (low-risk, behaviour-preserving):** guard each `if` on `has_variable = $tradegood$_stockpile`.
When the var is unset the governorship produces none of that good, so there is nothing to declare-for-sale
(the `for_sale_X`/`order_size_X` default of 0 already set just above is the correct outcome) — the guard
only skips a block that was erroring, it does not change any value the sim would otherwise compute.
An unset stockpile means "produced 0", and 0 is never `> DEMAND` (sell path) so skipping is exact; on
the order/demand path, `var:X_stockpile < DEMAND_X` with stockpile treated as 0 means demand is unmet —
still handled because the country-level demand aggregation reads DEMAND directly, not via this per-gov
order when the gov produces nothing. Verified the `value=0` default is set BEFORE the guarded `if`.

## D) LIVE: DEMAND_luxury_svalues.txt unset per-good cache read (180 lines) — FIX
17 luxury-good total-demand svalues (alcohol, gems, opium, tobacco, maize, porcelain, sweet_potato,
potato, peanut, chili, chocolate, coffee, tea, spices, sugar, luxury_clothing, luxury_furniture) each do:
```
if = { limit = { has_global_variable = first_time_luxury_demand_updated }  value = var:DEMAND_luxury_X }
else = { value = DEMAND_luxury_base_total }
```
The guard is the GLOBAL flag "luxury system has run once", but `var:DEMAND_luxury_X` is a PER-GOVERNORSHIP
cache. A governorship that never wrote that per-good var (didn't exist / no luxury demand at first run)
reads it unset → "Failed to fetch variable 'DEMAND_luxury_X' due to not being set" + "Event target link
'var' returned an unset scope". **FIX:** add `has_variable = DEMAND_luxury_X` (LOCAL scope) to each
limit, so a missing cache falls to the existing `else = DEMAND_luxury_base_total` — the intended default.
Behaviour-preserving: an unset var read returns empty/0 + error today; the guard routes to base_total,
which is the correct "not yet cached" demand. 17 blocks, invariant-neutral, brace delta 0.

## E) STALE / already-fixed — verified, NO action
- `ECON_LOG_production_snapshot` (1866) — fixed 2026-07-11 (6b2c4d9f6); see A.
- `sqrt` "unknown arguments" compile error — fixed (R2 `input=` key present); the REMAINING sqrt error
  ("Illegal use of operator >", ~157 lines) is the empty-input case, fixed in C above.
- `Unexpected token: is_triggered_only` (417, event files) — event files brace-balance clean at HEAD.

## C) LIVE: sqrt fed empty global price (~157 lines) — FIX
`GT_split_get_global_import_unit_price_all` calls `sqrt{ input = global_var:global_base_import_price_X }`
for every tradegood. A good with no global trade has base price 0; Tobbzn's Newton-method sqrt then
iterates its while-loop on an empty/zero `condition`, throwing "Illegal use of operator >" at sqrt's
while-limit. **FIX:** wrap the sqrt call in `if = { limit = { global_var:...price_X > 0 } ... }`.
sqrt(0)=0 and the global already holds 0, so skipping is value-exact. Guarded at the CALL SITE (not
inside the shared sqrt primitive) to keep blast radius to this one caller. Brace delta 0.

## OUT OF SCOPE (recorded, not touched)
- (C-culture) `octere`/`liburnian`/`tetrere` ancient-galley navy keys in ~130 culture files — un-migrated
  vanilla I:R naval vocab; the game BOOTS with it (tolerated load warning, not the economy flood). A
  mod-wide 130-file cosmetic sweep, out of scope for the #19 economy task. Flagged for a separate pass.
- Industry-A2 / trade-cluster PERF backlog — explicitly HIGH-RISK (correctness trap: var:X_stockpile is
  consumed inventory, not gross production; see [[imp19c-economy-audit-backlog]]). NOT touched, per the
  "low-med risk only" instruction.

## Summary of #19 fixes (all low-risk, behaviour-preserving, static-verified, boot-pending)
1. `GT_split_declare_sell_amount` — guard `var:X_stockpile` read with `has_variable` (sell path).
2. `GT_split_create_order_tradegood` — same guard (order/buy path).
3. `GT_split_get_global_import_unit_price_tradegood` — guard sqrt call with price `> 0`.
4. `DEMAND_luxury_svalues.txt` ×17 — add local `has_variable` guard beside the global-flag guard.
Together these target the dominant LIVE economy flood families (~1900 GT_split + 180 DEMAND_luxury +
157 sqrt lines). The single largest raw count (1866 ECON_LOG lines) was already fixed 2026-07-11 (stale
in this log). No high-risk perf work touched.

## F) LIVE: INCOME_sell_largest_reserve unset reserve vars (84 lines) — FIX
`INCOME_mitigate_deficit` (se_INCOME.txt, fired from DEBT_events.txt) falls back to
`INCOME_sell_largest_reserve` when the currency is not clearly gold/silver-standard. That effect
computes `local_var:gold_reserve_value_greater_than_silver` from `var:gold_reserve_size`,
`var:silver_reserve_size` × the global metal prices. A country with **no reserves** has neither
reserve_size var set, so the value never computes → the local var is unset → line 612's `> 0`
comparison threw "Invalid left side during comparison 'local_var'" / "returned an unset scope"
("gold_reserve_value_greater_than_silver" / "silver_needed_for_deficit" not set).
**FIX:** wrap the whole body in `if = { limit = { OR = { has_variable gold_reserve_size, silver_reserve_size } } ... }`
(sell only when a reserve exists — else nothing to sell, deficit handled elsewhere next tick), and inside
treat a missing reserve as size 0 via `l_gold/l_silver_reserve_size` locals so the comparison is always
well-defined. Used the proven `if/OR/has_variable/local_var` idiom — NOT `return = yes` (that verb is
unused anywhere in this codebase / not an Imperator effect; introducing it would be a NEW error).
Brace delta 0.

## G) ASSESSED, DEFERRED — piechart_update 'none'-type (96 lines)
`events/piechart/piechart_update.txt:32` in `TRADE_order_consumers` reads a scriptvalue that resolves to
type 'none' for some tradegoods (a GUI pie-chart data feed). Display-only (chart rendering), low count,
and the fix would touch the piechart value path blind. Per the "low-med risk only" bound this is
DEFERRED — flagged, not fixed. Likely the same unset-trade-var family; may already be reduced once the
GT_split guards (B) stop the upstream unset-scope cascade. Re-measure after a boot.

## Fixes this session (final): 5 effect groups, all low-risk / behaviour-preserving / brace delta 0
1. GT_split_declare_sell_amount — has_variable guard on stockpile read.
2. GT_split_create_order_tradegood — same.
3. GT_split_get_global_import_unit_price_tradegood — sqrt only when price > 0.
4. DEMAND_luxury_svalues.txt ×17 — local has_variable guard.
5. INCOME_sell_largest_reserve — OR-guard on reserve existence + zero-default locals.
DEFERRED: piechart 'none' (display, low-risk-uncertain), the ~130-file ancient-galley navy keys
(cosmetic, out of scope), and the entire perf backlog (high-risk correctness trap).

## H) LIVE: CURRENCY_grant_country_wealth guard TOO WEAK (17+ lines, all grant callers) — FIX
Same class as the ECON_LOG miss: a July-15 `[playtest logfix]` guard was PRESENT in the July-19 log but
the error still fired (`wealth_to_grant` not set, via QING_sell_offices + every other grant caller). The
guard used `OR = { has_variable country_unit_price_silver, ...gold }` — "at least one metal price". But
`CURRENCY_wealth_value_1_unit` branches on the currency's `backing_type` and reads the price OF THAT
METAL. So a SILVER-standard currency with `country_unit_price_silver` unset but `...gold` set PASSED the
OR yet still read the unset silver price → svalue 'none' → `change_local_variable multiply` drops
`wealth_to_grant` → `add_treasury` reads it unset (relative line 19). **FIX:** require the price MATCHING
the backing type — gold/bimetallic → `country_unit_price_gold`; silver → `country_unit_price_silver`;
anything else → the existing LOG_fail skip. Verified the only 3 backing types are gold/silver/bimetallic
(se_CURRENCY.txt:1840), so no 4th type is wrongly skipped. flag-comparison-as-trigger idiom proven in
CURRENCY_wealth_value_1_unit. Brace delta 0.

## Remaining log classes — TRIAGE (what is NOT a script bug / out of scope)
- **gradient_black_flip.dds missing texture (7525)** — GUI asset not shipped; cosmetic, not script.
- **Map object locator too far outside bounding box — vfx/unit_stack/combat (756)** — map-data (locators),
  cosmetic; not a script/economy bug.
- **PURCHASE_order_external / _get_preferred_tradezone_internal "unknown arguments" (136)** — INTENTIONAL
  no-op STUBS (se_PURCHASE.txt:1156/636 block comments): the real external-trade feature was never
  written; empty body is engine-legal + proven; boot runs fine. Compile-warning on an unused-$param$
  stub, not a bug. Left as-is (silencing would add noise to a deliberately-minimal stub for pure cosmetics).
- **remove_country_modifier PostValidate false — INCOME_set_tax_modifier (80)** — the standard
  "remove all 9 tax-tier modifiers, add the current one" idiom; removing an absent modifier is a
  harmless no-op the engine merely warns about. Not a crash/behaviour bug. Left as-is (guarding all 9×N
  removes with has_country_modifier is pure log-cosmetics on a working effect).
- **WAR_scripted_guis "testing for exact value (=)" (804)** — engine STYLE warning (use <,>,<=,>=), not
  an error; PEACE warscore GUI reads. Cosmetic.
- **COHORT_NAME_jurchen ordinal / octere-liburnian navy keys / console.gui widget-not-destroyed** —
  loc + culture-vocab + dev-console cosmetics; out of scope (see the ~130-file navy-keys note above).
- **oa_economy_setup.txt sqrt "Illegal use of operator >" (61)** — SAME sqrt bug as (C), reached via the
  setup on_action instead of oa_wealth_changes; my fix C guards the sqrt call itself → covers both. ✓
- **DEBT_events local_var unset (79)** — INCOME_sell_largest_reserve/sell_reserves; addressed by (F). ✓

## I) PURCHASE_* stub "unknown arguments" (136 lines) — INVESTIGATED + noise silenced (NOT implemented)
Investigation (operator asked whether to implement real external/internal trade):
- The two stubs (`PURCHASE_get_preferred_tradezone_internal`, `PURCHASE_order_external`) sit on a
  **DEFUNCT** code path. Their driver is `trade.2` ("Quarterly internal trade simulation",
  events/economy/trade.txt), which is **commented out** of the live pulse: `oa_wealth_changes.txt:211
  "# trade.2 # Defunct"`. It never fires.
- The mod's LIVE trade engine is `GT_split_do_global_trade_split` (called 8×/quarter in oa_wealth_changes),
  which ALREADY models cross-tradezone trade (declare-sell-to-TZ, global/country import pricing, order
  summing, export-subtract / import-add). It SUPERSEDED trade.2.
- So the feature these stubs gesture at (internal-supplier ranking + external partner purchase) already
  exists via a different design. Implementing the stubs = zero gameplay effect unless you ALSO re-enable
  trade.2 and rip out GT_split — a full trade-engine swap, not a stub fill-in. `PURCHASE_order_external`'s
  body was never written; `..._internal` has only unverified WiP (wip_quicktraderank.txt, TODO-laden).
- **DECISION: do NOT implement** (duplicate of live GT_split, high risk of double-counting supply — the
  same consumed-vs-gross trap as the perf backlog). **Silence the cosmetic warning instead:** an empty
  stub body that never mentions its passed $params$ makes the arg-compiler emit "unknown arguments".
  Added a dead `if = { limit = { always = no } ... }` block referencing each param (proven idioms:
  `value = flag:$X$` ×83 in repo; `add = $order_size$` already at se_PURCHASE.txt:1023) → never runs,
  zero runtime cost/behaviour, 136 warnings gone. Confirmed the sibling
  `PURCHASE_get_preferred_tradezone_external` does NOT throw the warning precisely because it references
  `$tradegood$` in its body — validating the diagnosis. Brace delta 0.

## J) Trade-system PERF cluster — INVESTIGATED (2026-07-20), verdict: NO safe cheap win
Operator asked to investigate the se_GLOBALTRADE_split.txt perf items. Measured the actual cost of
`GT_split_do_global_trade_split` (called 8×/quarter, once per good-type — food/luxury/luxury_2/3/4/5/6):

1. **"Reset explosion"** — `GT_split_reset_global_TZ_variables` zeroes ~133 global vars/good (6 accumulator
   families × 22 tradezones + extras). Across 61 goods that is ~8,100 `set_global_variable`/quarter.
   BUT: it is called ONCE per type (NOT per country — it sits above the every_country block), and every
   one of those globals is an ACCUMULATOR (`change_global_variable add=` all tick), so it MUST be zeroed
   each quarter. **Not removable, not redundant** — it's inherent to an accumulator design. No safe win.

2. **"Repeated every_country{every_governorship{}} passes"** — there are 5 such passes per type-driver.
   They are separated by HARD DATA BARRIERS: each pass feeds a global aggregation (sum_all_TZ_stockpiles,
   get_global_import_unit_price, sum_all_TZ_orders, scale_order_size, do_shipping_costs) that needs ALL of
   the prior pass's per-gov output before the next pass can run. This is a genuine map→reduce→map→reduce
   pipeline; the passes CANNOT be naively fused (that is precisely why they are split). Fusing would be a
   correctness regression (reading a global mid-accumulation), the same class as the A2 trap. No safe win.

3. **"goods-vs-trade_goods drift"** — FALSE ALARM. A set-diff shows 23 injector goods (steel, clothing,
   chemicals, munitions, …) absent from common/trade_goods/, but those are MANUFACTURED goods handled by
   the DEMAND/GOODS machinery (DEMAND_svalues.txt et al.), not undefined-var drift. The reverse list
   (amber, cotton, whales, plus non-goods country/province/color) is regex noise / goods simply not
   globally traded. No consistency bug.

**VERDICT: the trade-cluster perf items are either inherent (reset accumulators), structurally necessary
(barrier-separated passes), or false alarms (manufactured-goods "drift").** There is no low/med-risk perf
win here — any real speedup (e.g. collapsing the per-good iteration, or a gross-production cache) is a
net-new caching layer with the SAME consumed-vs-gross correctness trap that closed A2, plus it touches
the live hot trade loop. Recommend NOT pursuing under the "low-med risk only" rule. The residual
manufactured-good `X_stockpile not set` log lines (e.g. luxury_clothing, 22 lines) are the SAME unset-
stockpile class already guarded by fixes B (GT_split) and D (DEMAND_luxury) this session.

## Industry A2 — CLOSED / WONTFIX (do not reopen)
Recorded here for completeness: A2 was investigated twice and BOTH framings proven counterproductive
(switch-binned rewrite = mis-framed; "point 255 sites at var:X_stockpile" = correctness regression, since
X_stockpile is consumed inventory not gross production, already tried+reverted for food goods). A2 is
closed; the only "fix" would be a net-new gross-production cache + per-site semantic audit — not worth it.
See memory [[imp19c-economy-audit-backlog]].
