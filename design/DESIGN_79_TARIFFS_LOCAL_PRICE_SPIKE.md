# DESIGN — #79: tariffs income inflated by per-zone local-price spikes

## Status
Diagnosis: self-verified against both code and a real boot's logged numbers, adversarially
reviewed clean across 2 rounds (round 1 caught a real overclaim in the log evidence,
corrected; round 2 confirmed the corrected numbers independently). This doc now also
contains the FIX design (below) — not yet reviewed.

## The chain, precisely (all mod-authored, verified directly this session)

1. **Payment formula** (`common/scripted_effects/se_GLOBALTRADE_split.txt:2578-2594`,
   `GT_split_update_wealth_owed_for_tradegoods`):
   ```
   if = {
       limit = { has_global_variable = $tradezone$_stockpile_$tradegood$
                 global_var:$tradezone$_stockpile_$tradegood$ > 0 }
       change_variable = {
           name = wealth_owed_for_$tradegood$
           multiply = { value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
                        min = 0.0001
                        divide = { value = 0.5  add = owner.var:TZ_penetration_$tradezone$ } }
       }
   }
   else = { change_variable = { name = wealth_owed_for_$tradegood$  multiply = 0 } }
   ```
   `$tradezone$` = the PAYING governorship's own location zone. This is a deliberate #112
   (2026-08-11) change from the prior `multiply = owner.var:country_unit_price_$tradegood$`
   (the country's ONE stable, geography-blind national average) to this zone's own volatile
   `local_price_$tradegood$` — confirmed via the code's own changelog comment at the same
   location: *"Was multiply = owner.var:country_unit_price_$tradegood$ ... Instead pay the
   PAYING governorship's OWN trade-zone local_price."*

2. **`local_price_$tradegood$`'s own formula** (`GT_set_tradegood_price`, same file,
   setter body `:6093-6130`, formula at `:6099-6110`): `order_size / stockpile × 0.6`, with a
   documented (#107) Div/0 guard (`has_global_variable`-gated, `:6105-6108`) that
   skips the divide when stockpile is unset — leaving `local_price` as the RAW, un-normalized
   order count when a zone's stock is very low. The zero-stockpile PAYMENT guard added in
   #112/`DESIGN_112_ZEROSTOCK_PRICE_GUARD.md` only zeroes the payment when stockpile is
   **exactly 0** (`> 0` check above) — it does NOT protect a **low-but-nonzero** stock zone,
   whose `local_price` can still be a large raw order-count, unguarded, multiplied straight
   into the payment.

3. **Summation** (`:3697-3707`, `:3937-3947`): `wealth_owed_for_$tradegood$` for every good
   traded is summed into `queued_trade_expenses_due_resource_extraction`/`_manufacturing`,
   then merged into `trade_expenses_due_resource_extraction`/`_manufacturing`. Both are reset
   to 0 every quarter (`GT_reset_trade_transaction_totals`, `:4117/:4126`) — confirmed no
   cross-quarter double-counting.

4. **Strata split** (`GT_split_calculate_actual_share_of_expenses_category`, `:4240-4249`):
   ```
   set_variable    = { name = this_expenses_from_$category$_$seller$  value = var:trade_expenses_due_$category$ }
   change_variable = { name = this_expenses_from_$category$_$seller$  multiply = var:trade_share_$category$_$seller$ }
   ```
   called with `$category$` = resource_extraction/manufacturing and `$seller$` = every
   social stratum — producing the exact variable names `this_expenses_from_resource_
   extraction_upper_strata` etc. **This is the piece an earlier pass in this same
   investigation wrongly concluded was vanilla-engine-internal** — a literal-string grep for
   the fully-expanded variable name missed this macro-parametrized setter entirely. It is
   100% mod code, not vanilla.

5. **Tariffs income** (`common/script_values/INCOME_svalues.txt:757-890`, verified directly
   by me, not delegated): `INCOME_governorship_tariffs_<strata>` = (`this_expenses_from_
   resource_extraction_<strata>` + `this_expenses_from_manufacturing_<strata>`) ×
   `owner.var:INCOME_taxrate_tariffs`, summed over 5 strata into `INCOME_governorship_
   tariffs_total_positive` (`:748-754`), then over every governorship into the national
   total (`:108-114`). `INCOME_taxrate_tariffs` itself is confirmed correctly set (0-0.30,
   `EE_scripted_guis.txt:1003-1075`, `se_INCOME.txt:441-512`) — not the bug.

## Real log evidence (this exact boot, `~/Downloads/logs.zip`, debug.log Aug 14 16:49)

**Corrected after adversarial review round 1**, which caught that my first pass conflated two
different cases. Extracted directly from `IMP19C TZP BAND silver <zone> price <band>` /
`stock <band>` / `GLOBAL gbip <band>` across all 25 quarter-mark dumps in this boot:

- **GLOBAL gbip band is 0.1-1 in only 7/25 dumps; 1-10 in the other 18/25** — not the
  uniformly-low "0.1-1 consistently" my first pass claimed.
- The zones reading 100-1000 (india 7/25, yellow_sea 5/25, east_mediterranean 11/25, etc.)
  correlate with **stock = 0** for that zone/quarter in 29/33 (87.9%) of these readings (e.g.
  yellow_sea: 5/5 of its 100-1000 readings paired with stock=0). Stock=0 is the **exact-zero
  case the payment guard (step 2) DOES neutralize** (`change_variable = { multiply = 0 }`) —
  so most of these dramatic readings do NOT demonstrate an actual inflated payment; the guard
  is working as designed for them.
- The genuinely **unguarded** case — stock 1-10 (low but nonzero, passes the `> 0` guard) —
  pairs with local_price bands of **10-100** in the large majority of readings (east_europe
  18/18, baltic 8/8), while GLOBAL sits at 1-10 in the same dumps: a real, consistent **~10x
  divergence** between the zone-local price actually used for payment and the global average
  the pre-#112 formula would have used. A small unguarded tail (india, 2 readings) reaches
  local_price 100-1000 while its own stock is still nonzero (1-10) — i.e. genuinely unguarded
  cases as large as ~100x exist, just rare (2 of the 33 spike readings) compared to the
  dominant ~10x east_europe/baltic pattern.

Corrected conclusion: the mechanism is real and live today. The DOMINANT unguarded magnitude
is ~10x (one order of magnitude); a rare unguarded tail reaches ~100x. The much larger
100-1000x spikes seen in the raw zone data are mostly (87.9%) the guarded exact-zero case and
do not reach the payment.

## Corrections from adversarial review (round 1) incorporated

- No separate cross-quarter double-counting bug — reset confirmed real (step 3).
- The #112-era "boot-watch" note specifically worried about the EXACT-zero-stockpile case,
  which #115/the zero-stock guard now DOES protect — but the mechanism survives via the
  low-but-nonzero case, which is empirically confirmed still spiking in this boot's real data
  (see above). The diagnosis is not stale; the guard's protection is narrower than the spike
  vector actually observed.
- The `INCOME_svalues.txt` linkage (step 5) is now independently verified directly, not
  asserted from an unverified prior claim.

## Important tension: this may be a deliberate design directive, not a plain bug

The #112 comment (`se_GLOBALTRADE_split.txt:2536-2548`) states explicitly: *"NO ceiling (user
directive): a starved/spiking zone's price passes through in full."* This means a PRIOR
session was directly instructed to let a scarce zone's price spike uncapped, as part of the
"conquest-correct" regional-pricing intent (a conquered province pays its own zone's price,
not a national blend). The ~10x divergence this diagnosis found in the low-but-nonzero-stock
case is arguably the WORKING-AS-DIRECTED consequence of that choice, not a code defect —
a genuine local shortage (thin stock relative to heavy order demand) legitimately commands a
higher local price economically.

This reframes #79: the complaint ("tariffs income is too high relative to real treasury
growth") is a gameplay-balance objection to a previously-shipped, deliberately-undamped
design, not necessarily a "Sobisonator/AI did something wrong" bug. Per this project's
bug-vs-missing-feature convention, this is closest to a **balance revision of prior
mod-authored work**, which is in scope to adjust (it is not vanilla/upstream code) — but the
fix should explicitly preserve the "no ceiling" intent for the cases it was meant to cover
(a genuinely well-stocked zone with a real regional price difference), and narrow only the
specific noise vector this diagnosis identified (a thin-but-nonzero stock zone's price being
dominated by raw, unnormalized demand pressure rather than a meaningful scarcity signal).

## What this diagnosis does NOT yet establish

- The EXACT magnitude of the tariffs-income inflation itself (as opposed to the underlying
  local-price divergence) — the dedicated `ECON_LOG_curx_tariffs_expenses` probe
  (`se_ECON_LOG.txt`, shipped in commit `3db638045`) has zero data in this boot because this
  log predates that commit by ~2 hours. The local-price divergence shown above is real,
  large, and mechanically sufficient to explain an order-of-magnitude tariffs inflation, but
  the precise tariffs-income number itself needs a fresh boot with that probe active to
  pin down exactly.
- Whether ALL goods behave like silver, or whether silver (a currency-adjacent good with its
  own dedicated TZPROBE coverage) is unusually volatile compared to ordinary resource-
  extraction/manufacturing goods that actually drive the bulk of tariffs income. The
  `this_expenses_from_*` sums cover ALL traded goods, not just silver — the mechanism is
  generic (any good routed through step 1-2 is exposed to the same zone-price-spike vector),
  but this boot's probe coverage only lets a per-zone comparison for silver specifically.

## Proposed fix (revised after adversarial review round 1 on the fix — see corrections below)

**Goal: dampen the specific thin-stock noise vector, without reversing the "no ceiling"
directive for the case it was meant to serve** (a well-stocked zone with a genuine regional
price difference — the "conquest-correct" intent #112 documents).

At the payment site only (`GT_split_update_wealth_owed_for_tradegoods`,
`se_GLOBALTRADE_split.txt:2578-2594`), cap the LOCAL price used for THIS payment (not the
shared `local_price_$tradegood$` variable itself, which has ~24 other readers per the
existing code comment) — but ONLY when the paying zone's own stock is thin relative to
demand (the exact condition this diagnosis found driving the noise):

```
if = {
	limit = {
		has_global_variable = $tradezone$_stockpile_$tradegood$
		global_var:$tradezone$_stockpile_$tradegood$ > 0
	}
	# [task #79] precompute the thin-stock ratio as an EFFECT first, per the standing RHS-
	# comparison rule (a var-bearing expression may never sit on a trigger comparison's RHS) --
	# then compare the resulting plain var against a literal, matching every other threshold
	# check in this file. Guarded against total_order_size being unset/0 (the #107 Div/0 class,
	# 85x/boot when unguarded per this file's own history) -- a zone with stock but zero current
	# orders is a real, valid state (nothing being bought this quarter), not thin-stock.
	if = {
		limit = {
			has_global_variable = $tradezone$_total_order_size_$tradegood$
			global_var:$tradezone$_total_order_size_$tradegood$ > 0
		}
		set_variable = {
			name = GT_thinstock_ratio_tmp
			value = global_var:$tradezone$_stockpile_$tradegood$
			divide = global_var:$tradezone$_total_order_size_$tradegood$
		}
	}
	else = {
		# no current orders in this zone -- nothing being bought, so "thin stock relative to
		# demand" does not apply; treat as NOT thin (ratio >= the 0.1 threshold below).
		set_variable = { name = GT_thinstock_ratio_tmp  value = 1 }
	}
	if = {
		limit = {
			var:GT_thinstock_ratio_tmp < 0.1
			# [review round 3] also require gbip > 0 before capping -- gbip is 0 "for a good
			# with no global trade" (the sqrt setter's own >0 guard, :2852-2853). Capping
			# against a meaningless 0 baseline would zero the payment entirely instead of
			# capping it to 3x a real average -- fall through to the SAME uncapped multiply
			# the well-stocked branch uses whenever gbip isn't a usable baseline.
			has_global_variable = global_base_import_price_$tradegood$
			global_var:global_base_import_price_$tradegood$ > 0
		}
		# thin stock (< 10% of order demand) AND a usable global baseline: cap the LOCAL price
		# at 3x the pre-penetration-divide GLOBAL base price -- but
		# global_base_import_price_$tradegood$ is SQRT-TRANSFORMED at its own setter
		# (:2862-2868, sqrt of the raw weighted-sum-of-local-prices), while local_price is NOT
		# sqrt'd. Squaring gbip back before the 3x multiply recovers the same pre-sqrt scale as
		# local_price -- true apples-to-apples (per adversarial review: capping against gbip
		# directly, un-squared, would make "3x" mean something that swings with the price level
		# instead of a clean 3x of the real regional average). NOT
		# country_unit_price_$tradegood$ either -- that is ALREADY divided by
		# (0.5+country_penetration), a second, separate units mismatch also ruled out.
		change_variable = {
			name = wealth_owed_for_$tradegood$
			multiply = {
				value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
				min = 0.0001
				max = {
					value = global_var:global_base_import_price_$tradegood$
					multiply = global_var:global_base_import_price_$tradegood$
					multiply = 3
				}
				divide = { value = 0.5  add = owner.var:TZ_penetration_$tradezone$ }
			}
		}
	}
	else = {
		# well-stocked zone (>= 10% of order demand), OR thin stock but no usable gbip baseline:
		# UNCHANGED, full local-price pass-through -- honors the #112 "no ceiling" directive for
		# the case it was meant to serve, and safely avoids zeroing the payment when gbip=0.
		change_variable = {
			name = wealth_owed_for_$tradegood$
			multiply = {
				value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
				min = 0.0001
				divide = { value = 0.5  add = owner.var:TZ_penetration_$tradezone$ }
			}
		}
	}
	remove_variable = GT_thinstock_ratio_tmp
}
else = {
	# [IMPLEMENTATION NOTE, per adversarial review] this is NOT a no-op placeholder -- copy the
	# REAL existing else-branch verbatim from se_GLOBALTRADE_split.txt:2595-2620: the
	# `multiply = 0` zeroing AND the ECON_LOG_zerostock_guard_hits diagnostic counter (init-
	# guarded set_variable + change_variable, owner scope). Dropping the counter would silently
	# regress the #112-era boot-verification tooling for the exact-zero case.
}
```

**Corrections applied from adversarial review round 1 on this fix design:**
- **CRITICAL, fixed**: the original sketch nested an `if` inside a `max{}` sub-block — zero
  precedent anywhere in this codebase (every `min{}`/`max{}` sub-block in this file is pure
  arithmetic; every conditional in a script_value sits at the TOP level applying a running
  operator). Restructured into a top-level `if`/`else` computing the multiply value directly
  in each branch — the exact proven shape this file already uses at `:2578-2620` and the
  idiom confirmed elsewhere (`DEMAND_luxury_svalues.txt:34-52`).
- **MEDIUM, fixed**: the original cap compared `local_price` (pre-penetration-divide) against
  `country_unit_price` (already-divided) — a units mismatch that would make the effective
  ceiling swing with penetration instead of holding at a clean 3x. Now caps against
  `global_base_import_price_$tradegood$`, the true pre-divide apples-to-apples counterpart.
- **MEDIUM, fixed**: the original thin-stock test put a `global_var`-bearing value-block
  directly on a trigger comparison's RHS (`stockpile < { value = ... }`), violating the
  standing RHS-comparison rule. Now precomputed as a plain ratio via `set_variable` first,
  compared against the literal `0.1` afterward.

**Why 3x and 10%**: both are best-guess tuning constants, not derived from a formula — logged
plainly as guesses per the standing "guess and log" convention. 3x gives real regional
divergence room (matching the spirit of "no ceiling" for a meaningfully-stocked zone) while
still bounding the specific thin-stock spike this diagnosis measured at ~10x (rare ~100x) —
note this means the dominant ~10x case is only partly closed (capped to ~3x, not fully to
~1x); a fresh boot with the already-shipped `ECON_LOG_curx_tariffs_expenses` probe is needed
to confirm whether 3x is the right cap or should be tightened. 10% stock-to-order-size is a
round-number threshold for "thin."

**Why not cap `local_price_$tradegood$` itself at the source** (`GT_set_tradegood_price`):
per the existing code comment, that variable has ~24 other readers (the world-price blend,
the manufactured-goods raw-input pass in `se_PRICE.txt`, the purchase-spend path in
`se_PURCHASE.txt`) — capping it there would silently change behavior for all of them,
violating the delicate-fix principle. This fix touches only the tariffs-payment multiply.

**Why not revert #112/#115 to `country_unit_price` entirely**: that would undo the
"conquest-correct" regional-divergence intent wholesale (a deliberate, directed design
choice), not just the specific noise vector this diagnosis identified. The proposed fix is
narrower: preserve full local-price pass-through for well-stocked zones, cap it only where
the diagnosis found the number is actually unreliable (thin stock, order-count-dominated).

## Risks / open questions (resolved items removed after 4 review rounds)

- Is capping at 3x too aggressive/too lax given the measured ~10x dominant case (would clamp
  it) vs the rare ~100x tail (would also clamp it, more aggressively) — a boot's probe data
  is the only way to properly tune this, logged as a guess per above.
- This fix targets goods generically (works for any `$tradegood$`, not just silver) — the
  diagnosis's log evidence only covered silver's per-zone data; the fix's actual effect on
  the broader `this_expenses_from_*` totals (which sum ALL goods) still needs the dedicated
  `ECON_LOG_curx_tariffs_expenses` probe's data from a fresh boot to fully confirm.
