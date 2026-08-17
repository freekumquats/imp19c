# DESIGN (draft, pre-review) — a minimum import floor for geographically-concentrated goods

## Problem (fully confirmed, see `design/DESIGN_VEGETABLES_PERZONE_DISTRIBUTION_DIAGNOSIS.md`)

Vegetables, silk, and tea (all China-concentrated in this mod) show 12-19 of ~22 world trade
zones permanently stuck at stock=0 with real, persistent unmet demand — a stable trap, not
noise. Grain and livestock (produced in 1700+ provinces worldwide) never run dry anywhere.

**Confirmed mechanism** (independent review traced the full chain in
`common/scripted_effects/se_GLOBALTRADE_split.txt`):
1. `GT_split_get_country_global_market_penetration_tradegood` (:1824+) computes a country's
   access to a good as a weighted sum, across all 22 zones, of `(that zone's share of world
   production) × (this country's TZ_penetration in that zone)`.
2. `TZ_penetration_<zone>` (`common/script_values/SHIPPING_svalues.txt`) is BILATERAL — a
   country's own pre-built shipping/trade-agreement presence in that SPECIFIC zone, divided by
   everyone's combined presence there. It is not a function of the producing zone's province
   count.
3. For a good spread across most zones, step 1's weighted sum is dominated by each country's own
   home-zone term (always healthy). For a good concentrated in one zone, step 1 collapses to
   essentially one term: this country's bilateral presence SPECIFICALLY in the producing zone —
   which most of the world starts at zero in 1763, and which cannot grow on its own (a
   governorship needs the good to justify building the shipping that would let it get the good).
4. `GT_split_get_order_size_modifier_tradegood` (:2065-2133) turns this into
   `order_size_modifier_$tradegood$` — the fraction of every governorship's desired order that
   actually gets placed. When access is below national demand (the concentrated-good case for
   almost the whole world), this lands very close to 0, `GT_split_add_amount_imported_tradegood`
   (:3986-4002) then credits almost nothing to the governorship's own stockpile, forever.

**Confirmed NOT the mechanism**: no province-count-scaled capacity cap exists in this chain
(the diagnosis's other candidate). Not touching `TRADE_governorship_trade_capacity` or similar.

## Directly verified this session: every governorship DOES have a stockpile var, producer or not

`GOODS_setup_governorship_stockpiles` (`se_GOODS.txt:235-249` for vegetables, same shape for
every raw good) sets `$tradegood$_stockpile = 0` via an `else` branch for every governorship
that does NOT carry `has_variable = produces_$tradegood$`. So the earlier concern that
non-producers might never even have the stockpile var initialized (and so could never
order/import at all, independent of the penetration bottleneck) does not apply — every
governorship in the world has this var, defaulting to 0. The market-penetration chain above is
the ONLY real blocker, confirmed, not one of two candidates.

## Design: a minimum floor on `order_size_modifier_$tradegood$`

Add one new named constant and one guard, at the single point in the already-traced chain where
the "how much of my desired import actually arrives" fraction is finalized
(`GT_split_get_order_size_modifier_tradegood`, `se_GLOBALTRADE_split.txt:2065-2133`) — not
touching the penetration formula itself (§1-3 above), which is a real, working "well-connected
countries get proportionally more" gradient that should stay exactly as-is for every good that
isn't stuck at the floor.

New named constant (`common/script_values/TRADE_svalues.txt`, matching this codebase's own
convention of naming every tuning constant with its own derivation comment):
```
# [fix, per-zone distribution trap, design/DESIGN_PERZONE_IMPORT_FLOOR.md] a country with ZERO
# pre-built bilateral shipping presence in a good's producing zone gets order_size_modifier ~0
# forever (confirmed: no self-correcting mechanism exists -- a governorship needs the good to
# justify building the shipping that would let it get the good). This floor guarantees SOME
# informal/ad-hoc trade always reaches a deficit market, without changing the existing "more
# shipping presence = proportionally more access" gradient for every country already above it.
# [ASSUMPTION, boot-tune] 0.05 = 5% of national demand always gets through at minimum.
TRADE_minimum_order_size_modifier_floor = {
	value = 0.05
}
```

Edit to `GT_split_get_order_size_modifier_tradegood` — one `if` block added right after the
existing cap-at-1 check, inside the same "access below demand" branch (`se_GLOBALTRADE_split.
txt:2107-2115`), before that inner `if` closes:
```
			if = {
				limit = {
					var:order_size_modifier_$tradegood$ > 1
				}
				set_variable = {
					name = order_size_modifier_$tradegood$
					value = 1
				}
			}
			# [fix, see TRADE_minimum_order_size_modifier_floor's own comment]
			if = {
				limit = {
					var:order_size_modifier_$tradegood$ < TRADE_minimum_order_size_modifier_floor
				}
				set_variable = {
					name = order_size_modifier_$tradegood$
					value = TRADE_minimum_order_size_modifier_floor
				}
			}
```

### Why this is the minimal, correct edit point (not the penetration formula itself)

- Applying the floor to `country_global_market_penetration_$tradegood$` instead would also
  require reasoning about the weighted-sum-across-22-zones formula and its interaction with
  `global_stockpile_$tradegood$` (a second multiplicative term) — two things would need
  independent floors, and it's less clear a positive penetration score alone guarantees a
  nonzero import once multiplied through. Flooring the FINAL modifier (a 0..1 fraction, already
  the thing every governorship's order gets multiplied by) is a single, direct, easy-to-reason-
  about intervention exactly at the observed symptom.
- The floor only activates inside the branch that already means "my access can't cover my
  demand" (`se_GLOBALTRADE_split.txt:2080-2117`) — the two `else` branches (`access >= demand`,
  or `demand == 0`) are untouched, so a country that's already well-supplied is not affected at
  all by this change.
- Bounded, not a drift/ratchet mechanic: a fixed floor constant, not a growing state var — no
  runaway-accumulation risk (per this project's own standing caution against unbounded passive
  nudges).

### What this does NOT touch (explicitly out of scope)

- The `× 0.4545` constant in `GT_split_get_country_global_market_penetration_tradegood`
  (`se_GLOBALTRADE_split.txt` around :2033-2038) — flagged by the diagnosis review as
  apparently a 10x discrepancy against its own comment ("divide by 22" = `×0.04545`, not
  `×0.4545`). This scales EVERY good's penetration uniformly, so it doesn't affect the
  concentrated-vs-diffuse asymmetry this design targets, and touching it risks an unreviewed,
  hard-to-predict rebalance of the entire global trade economy. Left alone deliberately.
- `TZ_penetration_<zone>`'s own bilateral formula, `SHIPPING_svalues.txt` — unchanged. Countries
  that DO build real shipping presence into a producing zone still get proportionally more than
  the floor, exactly as before.
- Production formulas for vegetables/silk/tea — unchanged (the vegetables production multiplier
  already shipped this session was the right, separate fix for the GLOBAL stock question; this
  fix targets the PER-ZONE distribution question only).

## Open questions for review

- Is `0.05` (5% of national demand always gets through) the right order of magnitude, or should
  it be lower/higher? No existing figure in this codebase anchors this specific choice — flagged
  as a boot-tunable assumption, matching this project's own established convention for similar
  guesses (e.g. the vegetables production multiplier, the salt gabelle reform's treasury costs).
- Does a uniform floor (same for every tradegood) risk any unintended effect on a good this
  design didn't examine — e.g. a good that is INTENTIONALLY meant to be totally unavailable
  without real trade investment (a scarcity mechanic elsewhere depending on literal zero access)?
  Worth a grep for any `_stockpile` / `order_size_modifier` reader that assumes exact-zero is
  reachable and meaningful, before this ships.
- Should the floor apply to ALL 25 tracked goods uniformly, or only to raw/food goods (excluding
  luxury/manufactured goods, where zero access might be an intentional scarcity signal for a
  wholly different design reason)? The diagnosis only examined vegetables/silk/tea/grain/
  livestock — this design doesn't have direct evidence either way for luxury goods.

## Review outcome (adversarial review, 2026-08-17) — sound, no blockers

Reviewed independently. No HIGH/MEDIUM findings. Confirmed: the function's structure matches
the design's description exactly; no other reader of `order_size_modifier_$tradegood$` treats
literal 0 as a meaningful embargo/scarcity signal (checked against the file's OTHER deliberate
zero-guards, e.g. the #112 zero-stockpile price guard — none of them read this specific var);
the function runs exactly once per country per tradegood per quarter with no idempotency risk;
`TRADE_svalues.txt` already holds ~30 similarly-styled named constants, several already at the
same 0.05 order of magnitude elsewhere in this codebase; both stated out-of-scope exclusions
(the `0.4545` constant, the production multiplier) are genuinely orthogonal, not missing
dependencies. One informational note, not a design change: `$tradegood$_stockpile` has no
found ongoing decay/consumption subtraction anywhere in this chain (a pre-existing engine
property, not introduced by this fix) — so the floored import will accumulate quarter over
quarter rather than staying a flat trickle, which if anything makes the fix MORE visibly
effective, not less. Recommended a post-implementation `vegetables_trace.py` boot check to
confirm this empirically — noted as a follow-up, not a blocker.

## IMPLEMENTED (2026-08-17)

`TRADE_minimum_order_size_modifier_floor = { value = 0.05 }` added to `common/script_values/
TRADE_svalues.txt` (new `## IMPORT MODIFIERS` section). Floor guard added to
`GT_split_get_order_size_modifier_tradegood` (`se_GLOBALTRADE_split.txt`), inside the existing
"access below demand" branch, immediately after the pre-existing cap-at-1 check — exactly the
insertion point the design and its review confirmed. A second implementation-focused review
covers the actual diff before commit.

**Incidental bonus fix, disclosed**: staging the new constant tripped this repo's own
pre-commit brace-balance check on `TRADE_svalues.txt` with a pre-existing -2 imbalance,
unrelated to this change. Traced it (running brace-depth count, not a blind search) to a real,
copy-pasted structural bug in two functions, `TRADE_cash_balance_late_artillery` and
`TRADE_cash_balance_late_munitions` (both cosmetic tooltip-display script values, per their own
"Should be displayed... in tooltip" comments): each had one stray extra closing brace right
after their first `if` block, which prematurely closed the enclosing `every_governorships`
before the second `if` block (the income-due half of the same tooltip calculation) — pushing
that second `if` outside the per-governorship iteration entirely. Confirmed the sibling `early_
artillery`/`early_munitions` functions do NOT have this defect (correctly structured), so this
was a copy-paste-and-modify slip specific to the two "late" variants. Removed both stray braces;
file is now genuinely balanced (0, not just passing by coincidence). Unrelated to the per-zone
import floor itself — fixed because it was blocking the commit and was fully understood, not
guessed at.
