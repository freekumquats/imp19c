# DIAGNOSIS — task #14: vegetables trade-zone collapse is an UNDAMPED demand-elasticity bug, not seeding

**Status:** DIAGNOSIS (pre-adversarial-review). Independently traced in source this session.
A parallel deep-trace agent (diag-veg-collapse) is confirming the cross-quarter feedback and
pinning the exact Div/0 divide line; its findings merge into §5/§6 before this goes to review.

## Symptom (live -debug_mode boot, 2026-08-18 11:50)
- `vegetables` (a FOOD good) collapses: all 13 producing zones' zone stockpile hits 0 by
  ~1.5 in-game years (after quarter ~5) and never recovers through quarter 9.
- **ORDER (demand/attempted purchases) also drops to 0 in all 22 zones** — not just stock.
- CHI national vegetables PRODUCTION stays stable. A forensic seed-probe shows vegetables
  seed/produce healthy (REAL 10,968-11,098 / 11,098 — same ratio as every other good).
- Separately: Div/0 attributed to `oa_wealth_changes.txt:445/462/479/535` — the call sites of
  `GT_split_do_global_trade_split = { type = luxury / luxury_2 / 3 / 6 }`. The `food` pass
  (type=food, :421) is NOT in the Div/0 list.

## CORRECTION (2026-08-18, after adversarial review) — the "ORDER→0" inference is REFUTED
My first draft argued: "order→0 proves the collapse is demand-side, not supply, so the reseed
(task #5) is the wrong cause." **That inference is WRONG, and this correction supersedes it.**
- The probe's logged `order` = `global_var:$tz$_total_order_size_$good$`
  (`se_ECON_LOG_TZPROBE.txt:94-96`). That variable is **supply-scaled AFTER it is summed**:
  `GT_split_modify_fulfillable_order_sizes` (`se_GLOBALTRADE_split.txt:3390-3486`, verified this
  session) multiplies EVERY zone's `total_order_size_$good$` by
  `global_supply_as_percentage_of_order_$good$` whenever supply < 1, and that percentage =
  `global_stockpile / global_order_total` (`:3159-3176`). So when global vegetables stockpile
  collapses, the logged `order` is scaled to 0 across ALL zones **mechanically, with demand fully
  intact.** `order→0` therefore does NOT adjudicate supply-vs-demand — it is a downstream
  consequence of the stock collapse.
- **Internal inconsistency that settles it:** if demand had truly collapsed, production would
  exceed the (collapsed) demand and the stockpile SURPLUS would GROW — yet the boot shows
  stock→0. A demand collapse cannot produce stock→0. A SUPPLY shortfall produces both stock→0
  (no surplus) and logged-order→0 (via the fulfilment scaling). So the PRIMARY driver is a
  supply shortfall, consistent with H-RESEED.

## Corrected verdict — SUPPLY is primary; the demand-loop bugs are a real SECONDARY amplifier
- **H-RESEED (task #5) is a valid, primary supply-side fix and is NOT superseded.** More
  vegetable provinces → higher zone stockpile → lower price (`price = (order/stock)·0.6/num_food`,
  `se_GLOBALTRADE_split.txt:6244-6252`) → smaller elasticity divisor AND a higher supply% so the
  fulfilment scaling stops zeroing the logged order. Supply and the demand loop are COUPLED.
- **The demand-loop defects below are real and confirmed, but secondary** — they aggravate the
  price spike and add error spam; they are not the root of stock→0. They ship as complementary
  hardening under task #14, alongside the #5 reseed.

The remaining sections (undamped elasticity, dead clamp, div/0) survive the review as CONFIRMED
code defects — only their CAUSAL WEIGHT is downgraded from "the cause" to "an amplifier."

## Root cause (traced in source)

### 1. Vegetables demand is NOT vegetables-specific at its base
`se_DEMAND.txt`:
- `DEMAND_set_demand_from_food_all` (:36) sets
  `var_DEMAND_unfulfilled_food_need_governorship = DEMAND_unfulfilled_food_need_governorship`
  (:40-43) — the WHOLE governorship's residual food need — then calls
  `DEMAND_set_demand_from_food` once per food good (:68-85), vegetables at :77-79.
- `DEMAND_set_demand_from_food` (:114) sets each good's base demand to that same
  whole-governorship unfulfilled need (:155-158) then `divide = DEMAND_num_food_goods` (:175,
  = 6 baseline). So vegetables' BASE demand = `unfulfilled_food_need / 6`, re-seeded EVERY tick.
- CONSEQUENCE: vegetables' base demand cannot latch to 0 from thin veg production — it tracks
  the governorship's total food need, which is positive as long as pops are hungry. **Thin veg
  seeding does not starve veg demand.** H-RESEED's premise is structurally false here.

### 2. The price-elasticity divide is UNBOUNDED
`se_DEMAND.txt:179-218`:
- `l_DEMAND_<good>_price_diff_to_food_mean = local_price_<good> / PRICE_food_mean_normalised`
  (:179-194) — this good's price relative to the food-basket mean.
- `DEMAND_food_<good> divide = l_DEMAND_<good>_price_diff_to_food_mean` (:213-216) — the
  elasticity brake: an expensive good's demand is divided down.
- There is NO cap on the divisor. When vegetables is even modestly under-produced in a zone its
  price rises above the food mean, so the divisor > 1 and demand is cut. With `price = order /
  stock` (`GT_set_tradegood_price`), a shrinking for-sale surplus spikes price, which cuts
  demand further next tick — a feedback with no bound.

### 3. The ±10% damping clamp that WOULD bound it is dead — and it died by ACCIDENT
`se_DEMAND.txt:128-149` still COMPUTES `previous_tick_food_demand_<good>_110_percent` /
`_90_percent`, but the code that APPLIES them (:220-263) is entirely commented out.
- **Git blame (`dd43d5419`, Sobisonator, 2023-08-23, "WiP dynamic food demand"):** the working
  clamp was `FUNC_clamp_variable{ variable=DEMAND_food_<good> max=..._110_percent min=..._90_percent }`.
  The commit message states it was removed because it "was failing to compare a variable to 0
  (try making this 0.0 or an svalue?)" — i.e. the **RHS-variable-comparison bug**
  (`imp19c-rhs-comparison-operator-rule`: a var on a comparison RHS is illegal). It was replaced
  by commented-out inline code that was never finished.
- So the ±10% damping was lost to a fixable scripting error in a 2023 WiP, NOT to a design
  decision. Food demand has run UNDAMPED ever since. The author's aside ("the order size
  effectively does this job by subtracting the local amount available before making an order")
  addresses only the UPPER bound (over-demand); it does nothing for the LOWER bound, which is
  exactly the collapse direction here.

### 4. Net mechanism
Undamped elasticity divide (2) with the intended damping missing (3), over a base that is not
veg-specific (1): once a zone's vegetables price sits above the food mean, demand is divided
down hard, `order = demand − local stockpile` falls to ~0, and with no floor the market reads
DEAD (stock=0 AND order=0) even though pops' real food need is met by grain/livestock. This is
a SIM artifact of a missing damping bound, not a true vegetable shortage.

## Verdict (CORRECTED): supply-primary + demand-loop amplifier — BOTH #5 and #14 ship.
- Task #5 (province reseed) is the PRIMARY fix and stays live. The ×4 revert already shipped
  (9085ba9c1) and stays.
- Task #14 ships the two confirmed demand-loop defects below as complementary hardening.
- **This corrected verdict incorporates the 2026-08-18 adversarial review, which was accepted
  after independently re-verifying its decisive claim (`GT_split_modify_fulfillable_order_sizes`
  supply-scaling) in source.**

## Div/0 — RESOLVED to the real site (my earlier :3340 guess was WRONG)
The error.log stack traces (authoritative, boot 2026-08-18 11:47, post-#107) name TWO innermost
frames — NEITHER is :3340 (my guess) nor the luxury-demand site (the deep-trace agent's guess):
- **SITE A (fixed): `GT_set_tradegood_price` price divide** (se_GLOBALTRADE_split.txt ~6252),
  269× at setup (oa_economy_setup:2493) + runtime. The `#107` guard used an `if/limit` AROUND the
  divide, NESTED inside the scriptvalue `value = { }` block — and that does NOT reliably skip the
  divide in this engine (proven: it still fires post-#107). The codebase's working idiom floors the
  DIVISOR directly (EDU_svalues.txt:607-610, ADMIN/AI). **FIX APPLIED:** `divide = { value =
  global_var:$tradezone$_stockpile_$tradegood$  min = 1 }`. min=1 (not 0.0001) reproduces #107's
  "price = raw order size at stockpile 0" default and damps the #79 thin-stock explosion.
- **SITE B (likely a DOWNSTREAM CASCADE of Site A — no separate fix): `GT_split_update_wealth_owed_
  for_tradegoods`**, 257× Div/0 (line 12) + 3,828× "failed to read divide for set_variable"
  (line 34, the bigger class). The deep-trace agent read this macro in full and found ALL its own
  divides properly guarded (effect-level if/limit or 0.5-floor) — the real cause is an UPSTREAM
  EMPTY operand (a scriptvalue that Div/0s yields EMPTY, per se_ECON_LOG.txt:1412), fed into
  `total_order_size` / `TZ_penetration`. **Hypothesis (boot-testable): Site A is the root.** Site A's
  Div/0 makes `local_price` EMPTY; `local_price` feeds the demand elasticity divide (se_DEMAND.txt:
  179-216) → EMPTY `DEMAND_food` → EMPTY `order_size` → EMPTY `total_order_size` → Site B's readers
  "fail to read divide". So the Site A floor should CLEAR Site B's 4,085 combined errors too.
  **CONFIRM ON BOOT:** if Site B's line-12/line-34 classes survive after the Site A fix, trace the
  upstream `total_order_size`/`TZ_penetration` setter directly (next round) — do NOT pre-guess it.

## (superseded) earlier div/0 note — kept for the record
The below (:3340) was my first guess; the error.log does not implicate it. Left for the trail.
- The price divide in `GT_set_tradegood_price` (~:6237) is already `#107`-guarded
  (`has_global_variable` + `> 0`), and the global-stockpile percentage divides
  (`GT_split_create_global_stockpile`, :1520-1553+) are guarded (`stockpile>0 && global>0`).
- **PINNED (traced this session): the unguarded divide is `se_GLOBALTRADE_split.txt:3340`**, in
  `GT_split_get_order_as_percentage_of_TZ_total_tradegood`:
  ```
  set_variable = { name = order_as_percentage_of_TZ_total_$tradegood$  value = var:order_size_$tradegood$ }
  change_variable = { name = order_as_percentage_of_TZ_total_$tradegood$
      divide = global_var:$tradezone$_total_order_size_$tradegood$ }   # <-- NO guard
  ```
  Every sibling divide by `total_order_size` / `global_order_total` / `global_supply_as_percentage`
  IS guarded — 2558 (`has_global_variable` + `> 0`), 3174 (`trigger_if` + `> 0`), 3376/3996
  (`> 1`). Only :3340 divides unconditionally. When a good's `$tradezone$_total_order_size_$tradegood$`
  is 0 (a luxury nobody orders in that zone), it div/0s. Food is exempt because food goods always
  carry positive total order in every zone.
- Fix = mirror the accepted pattern: guard the :3340 divide with `has_global_variable` +
  `> 0`, skipping it (leaving `order_as_percentage_of_TZ_total_$tradegood$` = the raw order size,
  the correct default when the zone total is 0) when the divisor is 0.

## Fix shape (task #14 — NOT yet implemented; for the design phase)
Two minimal, independent changes. (The reseed itself is task #5, tracked separately.)
1. **Restore the ±10% per-tick food-demand clamp** (`se_DEMAND.txt:221-263`). The intended clamp
   already exists as commented-out inline code that IS RHS-legal (it compares
   `var:l_comparison_diff < 0` against the literal 0, never a var-to-var comparison — precisely
   avoiding the 2023 `FUNC_clamp_variable` failure). Implementation = uncomment both blocks
   (upper bound 221-240, lower bound 244-263) and fix the ONE latent bug they carry: the
   `set_variable` target is written `name = var:DEMAND_food_$tradegood$` (:236, :259) — the
   `var:` prefix is illegal in a `name` field and must be `name = DEMAND_food_$tradegood$`.
   This bounds each tick's demand to ±10% of the previous tick, exactly the abandoned intent.
   - **DROPPED the earlier "cap the elasticity divisor `[0.5,2.0]`" idea** — with the ±10% clamp
     restored, per-tick demand change is already bounded, so a divisor cap is redundant and would
     be an unproven new constant (over-engineering). Faithful clamp restoration only.
2. **Guard the `se_GLOBALTRADE_split.txt:3340` Div/0** — mirror the accepted `#107` pattern:
   wrap the `divide` in `limit = { has_global_variable = $tradezone$_total_order_size_$tradegood$
   global_var:$tradezone$_total_order_size_$tradegood$ > 0 }`, leaving
   `order_as_percentage_of_TZ_total_$tradegood$` = the raw order size when the zone total is 0.

## Safety / caution (imp19c-sobisonator-upstream-caution)
- Change #1 touches the shared FOOD demand loop (all 6 food goods, not just vegetables). It is
  justified because git blame (`dd43d5419`) proves the damping was INTENDED and lost to a fixable
  scripting bug, not removed by design — restoring it completes the original intent. It is a
  faithful uncomment of the author's own replacement code, not a new mechanism. Still routed
  through design → adversarial review → code-review, and it ships with the existing TZP band
  logging so the next boot confirms behaviour across ALL food goods (watch grain/livestock do not
  regress).
- Change #2 is a pure defensive guard (mirror of an existing accepted pattern), no behaviour
  change except removing the Div/0 error spam.

## Boot-confirmation plan (guess-and-log, not a deferral)
- #14 ships the clamp restore + div/0 guard; #5 ships the reseed (primary supply fix).
- Next -debug_mode boot: `tools/curx_analyze.py --good vegetables` over debug.log — expect the
  ~19 collapsing zones' stock to STOP hitting 0 and price to stay in low bands; Div/0 count for
  the luxury/3/6 passes to drop to zero; grain/livestock demand bands to stay stable (clamp did
  not distort them). If a zone still collapses, it is a residual SUPPLY gap → raise that zone's
  reseed margin (#5), not the clamp.
