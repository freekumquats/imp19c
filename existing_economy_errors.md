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

## A) ECON_LOG_production_snapshot flood (1866 lines) — STALE, no action
Log points at `ECON_LOG_production_snapshot line: 8/9` doing `change_variable` on an empty var. In the
CURRENT `se_ECON_LOG.txt` (fixed by commit 6b2c4d9f6, `logfix #371`, 2026-07-11) lines 8/9 are the
harmless `set_variable ... value = 0` initialisers; the `change_variable` calls moved to lines 21/22
and now read the governorship via `save_scope_as` + `scope:x.var:` (the prev-across-`root=` empty-scope
bug is already fixed, with a `[logfix]` comment documenting it). The log is an older build than HEAD.
**No action** — verifying-only per the stale-log rule.

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
