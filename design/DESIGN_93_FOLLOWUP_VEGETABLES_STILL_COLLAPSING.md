# DIAGNOSIS (draft, pre-review) — vegetables still collapsing after the #93 demand trim

> **SUPERSEDED (2026-08-18):** a live-boot re-investigation, then an adversarial review,
> overturned this doc's conclusions. The ×4 multiplier here rests on a province miscount
> ("419 CHI provinces" — 418 active provinces are worldwide, Russia-dominant; CHI ~50) and a
> non-causal ratio. The real cause is a GEOGRAPHY-GATED DEMAND RATCHET: vegetables are grown
> thin/locally in ~20/22 trade zones, and the shared ±10%-clamp + price-elasticity divide
> ratchets governorship demand past that thin local production each quarter (zone stock is a
> per-quarter FLOW, reset+rebuilt every pass — NOT a reservoir, and the infra export cap does
> NOT bind). The ×4 does not "keep it, merely inert" — it may ACCELERATE the ratchet by
> cheapening the early price. See `DESIGN_93_VEGETABLES_BOOMBUST_DIAGNOSIS.md` (§4, §5).

## Prior fix, and what it actually achieved

`design/DESIGN_93_VEGETABLES_SHORTAGE.md` (commit `4ee1f5412`, already live in current code
— verified `INDUSTRY_base_demand_alcohol_vegetables`/`_pharmaceuticals_vegetables`/
`_processed_foods_vegetables` all read `value = 2`, down from 5/6/6) diagnosed vegetables'
industrial demand-per-producing-province (0.0406) as ~2.7x the next-worst staple's, and cut
the three industrial base-demand constants by ~65% (aggregate per-factory demand 17 -> 6) to
compensate. Explicitly rejected a demand-side dynamic throttle (circular-dependency defect)
and deprioritized supply-side fixes (province reassignment: fights sourced crop-geography
research; a production-formula multiplier: kept "in reserve... if a boot shows the retune
under- or over-corrects").

## Fresh evidence: the retune measurably did not move the collapse

A live boot this session (`~/Downloads/logs.zip`, Aug 16 17:30, 17 quarter-marks), analyzed
with the project's own `tools/vegetables_trace.py`:

- **Global vegetables stock hits exactly 0 at quarter-mark 11** — the identical quarter the
  ORIGINAL pre-fix diagnosis reported ("hits exactly 0 at quarter-mark 11"). A 65% cut to
  industrial demand produced **no measurable change in the collapse quarter**.
- Every one of the 22 trade zones individually shows the same shape: real starting stock
  (100-10,000), price climbing steadily, stock draining to 0 by quarters 3-9 depending on
  zone, and by quarter 11 essentially all zones are pinned at stock=0/order=0 through the end
  of the trace (quarter 16) — a total, permanent market death, not "runs tight."
- Price and order data confirm this isn't a logging artifact: price rises 10-100x as stock
  drains (correct market-mechanic behavior), and order (attempted purchases) itself drops to 0
  once stock is exhausted — the market has nothing left to sell, not "nobody wants to buy."

**This is strong evidence the three trimmed industrial constants were never the dominant
consumption term.** If they had been, cutting them 65% should have shifted the collapse point
meaningfully later, or reduced the number of permanently-dead zones. Neither happened.

## Root cause of the actual dominant term, found

`DEMAND_food_base` (`common/script_values/DEMAND_food_svalues.txt:32-39`):
```
value = governorship_population
multiply = DEMAND_need_life_goods
divide = DEMAND_num_food_goods
...
```
Pop-level food demand is **population-scaled and split EQUALLY across however many food
goods exist** (`DEMAND_num_food_goods` — grain, vegetables, fish, livestock, temperate_fruit).
Every governorship's pops are modeled as wanting an equal per-capita share of EACH food good,
with no adjustment for that good's own production capacity.

But production capacity is wildly uneven (`setup/provinces/*.txt`, `trade_goods=` field,
recounted): vegetables 419 provinces, temperate_fruit 661, fish 668, grain 1747, livestock
1885. Vegetables' production base is **4.2x smaller than grain's and 4.5x smaller than
livestock's**, yet under `DEMAND_food_base`'s equal-split formula it is asked to satisfy the
exact same per-capita demand share as goods with 4-4.5x the growing capacity.

The original #93 diagnosis's "demand-pressure-per-producing-province" metric only measured the
**3 industrial consumers** (17 units/factory) — it never computed the equivalent ratio for
**pop-level demand**, which scales with national population (a vastly larger absolute number
than "units per factory") and is structurally identical in per-capita terms across all 5
staples regardless of production base. The industrial trim targeted a real but comparatively
minor term; the equal-split pop-level formula, untouched, is the actual dominant driver, and it
was explicitly and only screened on SHAPE ("same smoothing curve as every other food good" —
true, but irrelevant to magnitude) not on relative MAGNITUDE against production capacity.

## Why this reopens Option A (supply side)

The #93 design doc rejected broad province reassignment (fights sourced crop-geography
research — correct, still holds) but explicitly kept "a vegetables-only production-formula
multiplier (not touching province assignment)" in reserve, calling it "a real, viable
secondary lever," to be used "if a boot shows the retune alone is insufficient." That
condition is now met, with quantified evidence, not just a hunch. Per direct user
instruction, revisiting the supply-side option is now the right next step: further
demand-side trims of the *industrial* constants have no basis (they weren't the dominant
term to begin with — cutting them further from a shown-ineffective baseline is unlikely to
help either), and geography reassignment stays out of scope for the reason already
established.

## Review outcome (adversarial review, 2026-08-17)

Reviewed independently. The actionable direction (attack the supply side) survives; three
real problems in the reasoning/evidence were found and are corrected here.

**Lever 2 (adjusting `DEMAND_food_base`/`DEMAND_num_food_goods`) is DROPPED — not
implementable as described.** `DEMAND_food_base` is never read in the live pass — real
per-governorship food demand is set every tick by `DEMAND_set_demand_from_food`
(`se_DEMAND.txt:114-176`) into `var:DEMAND_food_vegetables`, and `DEMAND_food_vegetables`
(the svalue) only falls through to `DEMAND_food_base` in an `else` branch that never fires
once that var exists (i.e. always, after the first tick). Worse, `DEMAND_num_food_goods` is
ONE shared divisor across all 6 food goods per governorship — lowering it to help vegetables
would RAISE demand for every food good simultaneously (dividing by a smaller number), the
wrong direction entirely, and there is no existing per-good weight inside this formula to
target vegetables alone. This lever needs a genuinely new mechanism to exist at all; it is
not a tuning-constant edit like Lever 1. Dropped from consideration.

**The "identical collapse point, therefore zero effect" claim is weaker than stated.**
`tools/vegetables_trace.py` records a row for BOTH the PRE and POST half of each quarter, so
"17 quarter-marks" is actually ~8-9 real quarters, and "quarter-mark 11" is real quarter
~5-6, not literally the 11th quarter. Resolution is roughly half a quarter. A partial
improvement from the #93 industrial-demand trim (say a 20-40% drain reduction) could easily
fail to shift this coarse a marker while still being real. The conclusion "industrial demand
was never the dominant term" still holds (a truly dominant 65% cut should have shown SOME
visible shift — count of permanently-dead zones, peak price, per-zone onset spread — and it
didn't move any of those either), but it's confirmed by elimination and lack of any visible
shift across several signals, not by one precise quarter-number match.

**The "no demand-side feedback, draws at full rate forever" premise was factually wrong** —
there IS a real feedback term already live: `se_DEMAND.txt:197-218` divides pop-level food
demand by `price_diff_to_food_mean`, so as vegetables' price spikes 10-100x during a shortage
(confirmed in the trace data), pop demand for it DOES get throttled down, damped by a ±10%
previous-tick rubberband. This doesn't change the recommended fix, but it changes WHY it's
needed: persistent stock=0 despite a real, live price-elasticity brake is stronger evidence
that production is structurally below even the ALREADY-THROTTLED residual demand, not that
demand runs unchecked. Supply-side is still the right lever, now for the correct reason.

**Confirmed to survive independently**: no missed 4th/5th vegetables consumer (only the pop
term + the 3 industrial adds reach `CONSUME_from_stockpile`'s draw; other `DEMAND_*vegetables*`
references are export/legacy, not read by the live consume path); no hidden production gate
on `GOODS_governorship_vegetables_produced` (byte-identical shape to grain/livestock: sum
`num_goods_produced` over vegetables-tagged provinces × `agriculture_productivity`); province
count is a fair, if not exact, production proxy (ignores per-province yield variance, but no
better proxy is available without new instrumentation).

## Lever 1 (supply side) — the surviving fix, moving to design below

A vegetables-specific multiplier on `GOODS_governorship_vegetables_produced`
(`GOODS_svalues.txt:1963-1974`), unchanged from the original proposal, is confirmed
well-formed and is now the sole recommended lever. Design follows in a implementation-ready
form below.

## Open question for review (SUPERSEDED by the review outcome above — kept for the record)

Two distinct levers now look viable and are NOT mutually exclusive with the existing #93 fix
(which stays in place — it modestly reduced ONE real, if minor, contributor and should not be
reverted):
1. **Supply side**: a vegetables-specific multiplier on `GOODS_governorship_vegetables_produced`
   (`GOODS_svalues.txt:1963-1974`), the exact lever #93 kept in reserve.
2. **Demand side, but the RIGHT term this time**: `DEMAND_num_food_goods` or an equivalent
   per-good weighting inside `DEMAND_food_base`, so vegetables' equal-per-capita SHARE of pop
   food demand is reduced to reflect its genuinely smaller production base, instead of leaving
   the divisor uniform across all 5 foods and trimming an unrelated industrial side-channel.

Sending this diagnosis for adversarial review before proposing which lever (or combination) to
implement, and before touching any code.

## DESIGN (draft, pre-review) — vegetables-specific production multiplier

### Change

`common/script_values/GOODS_svalues.txt:1963-1974`, current body:
```
GOODS_governorship_vegetables_produced = {
	value = 0
	every_governorship_state = {
		every_state_province = {
			limit = { trade_goods = vegetables }
			add = num_goods_produced
		}
	}
	multiply = owner.MODIFIER_agriculture_productivity
}
```
Add one line: `multiply = GOODS_vegetables_production_multiplier` (a new named constant, not
an inline literal, matching this codebase's convention of naming every tuning constant so
it's independently discoverable/greppable and carries its own derivation comment — e.g.
`GOODS_cottage_military_goods_output`).

```
GOODS_vegetables_production_multiplier = {
	# [fix, task #93-followup 2026-08-17] vegetables' production base (419 CHI provinces
	# tagged trade_goods=vegetables) is 4.17x smaller than grain's (1747) and 4.5x smaller
	# than livestock's (1885), per design/DESIGN_93_VEGETABLES_SHORTAGE.md's own province
	# recount. Pop-level food demand (se_DEMAND.txt's DEMAND_set_demand_from_food) treats
	# all food goods structurally equally per governorship -- vegetables is asked to supply
	# the same per-capita share as grain/livestock from a base ~1/4 their size. Confirmed
	# via a live boot (tools/vegetables_trace.py) that vegetables' national stock collapses
	# to permanent 0 in the majority of trade zones despite an already-live price-elasticity
	# demand brake (se_DEMAND.txt:197-218) -- production is structurally short of even the
	# throttled residual demand, not a runaway/unthrottled draw.
	# Rate: 4, matching grain's production-base advantage ratio (1747/419 = 4.17, rounded to
	# a clean 4) -- brings vegetables' effective per-province-equivalent output to rough
	# parity with its "fair share" burden under the equal-per-good pop demand split, without
	# assuming per-province yield is identical across goods (it may not be -- boot-tunable).
	# [ASSUMPTION, boot-tune per the overnight guess-and-log convention] -- a real boot's
	# vegetables_trace.py output is the only way to confirm whether 4 clears the deficit,
	# over-corrects into a vegetables glut, or needs further adjustment.
	value = 4
}
```

### What this does NOT touch (honest scope)

- No change to `setup/provinces/*.txt` trade_goods assignment (stays out of scope: fights the
  project's sourced crop-geography research, per the original #93 doc's Option-A rejection of
  broad reassignment -- this design only ever proposed the "production-formula multiplier"
  variant, never touching province files).
- No change to the #93 industrial-demand trim (already live, stays as-is -- it's a real,
  independently-justified cut regardless of whether it moved the collapse marker; reverting it
  would not help and isn't proposed).
- No change to `DEMAND_set_demand_from_food`, `DEMAND_num_food_goods`, or any other consumer
  of vegetables -- Lever 2 is dropped per the review outcome above; this design touches
  production only.
- No change to `MODIFIER_agriculture_productivity` (the existing owner-level multiplier this
  formula already applies) -- the new multiplier is vegetables-specific and additive to that,
  not a replacement.

### Risk / open questions for design review

- Is 4 the right value, or should it be more conservative (e.g. 2-3, given province count is
  an imperfect proxy per the review's own note that it "ignores per-province yield variance")?
  A boot's `vegetables_trace.py` is the only way to properly tune this -- flagged as a guess,
  not a blocking unknown, matching the project's standing convention.
- Does this new script value need its own scope declaration, or does inheriting the calling
  scope (governorship, via `GOODS_governorship_vegetables_produced`) work correctly for a
  bare `value = 4` constant with no scope-dependent reads? (It should -- it's a pure literal,
  same shape as `GOODS_cottage_military_goods_output` -- but flagging for the review pass to
  confirm rather than assuming.)
- Should this also feed `GOODS_national_production_vegetables` (the topbar/tooltip "Produced
  by good" figure) automatically, or does that already sum from the per-governorship value
  (meaning it inherits the fix for free)? Check before implementing, not after.

## Design review outcome (adversarial review, 2026-08-17) — BUILD IT, one disclosure required

Reviewed independently. Verdict: proceed. Core change is well-formed, will not crash, composes
correctly (result = `sum(num_goods_produced) x owner.MODIFIER_agriculture_productivity x 4`).
Snippet quoted in the design was byte-accurate; scope composition (bare `value = 4`, no
scope-dependent reads) confirmed safe at governorship scope; the `GOODS_cottage_military_
goods_output` precedent claim confirmed accurate (identical shape). `GOODS_national_
production_vegetables` inherits the fix for free (no separate edit needed).

**One real gap, now disclosed (was MEDIUM):** the design's downstream-consumer audit missed
that `GOODS_governorship_vegetables_produced` also feeds `COTTAGEIND_raw_vegetables`
(`se_COTTAGEIND.txt:170`), which is the dominant input to the cottage PHARMACEUTICALS recipe
(`se_COTTAGEIND.txt:600-604`, alongside a whales term that's effectively zero since whales is
a defunct remapped good). So this fix will also raise cottage pharmaceuticals output by
roughly the same factor. This is disclosed, not mitigated -- pharmaceuticals is a good that
(per this session's own earlier log analysis) is chronically under-supplied relative to
military demand, so more pharma output is very likely a second beneficial side effect, not a
new problem. Flagged for a post-boot check, not blocking.

**Glut risk confirmed real but self-damped, not blocking**: the price formula (`se_
GLOBALTRADE_split.txt:6216-6242`, price ~ order_size/stockpile) means a permanent 4x stockpile
surplus would push price toward zero, but the SAME price-elasticity brake that throttles
demand during a shortage (`se_DEMAND.txt:197-218`) works symmetrically in reverse as price
falls -- demand rises to eat the surplus. Export is also hard-capped by
`TRADE_governorship_trade_capacity` (`DEMAND_svalues.txt:2099-2109`), so a glut cannot blow up
trade either. No additional guard needed.

**Sizing note**: because demand rises as price falls, 4x production will NOT translate to 4x
stock headroom -- demand partially absorbs the gain. This means 4 is more likely to
under-correct than over-correct from the current permanent stock=0 baseline, which argues
against the design's own fallback of a more conservative 2-3. Proceeding with 4 as the
first-pass value; a real boot's `vegetables_trace.py` output remains the actual tuning
instrument, as already planned.

**Deferred refinement (not blocking implementation)**: the review noted `GOODS_national_
production_grain`/`GOODS_national_production_vegetables` could be logged from a live boot to
get a measured output-VOLUME ratio instead of the 419-vs-1747 province-COUNT proxy this design
uses. Worth doing on a future boot pass to refine the constant further; not required to ship
the first-pass fix now.

## IMPLEMENTED (2026-08-17)

`GOODS_vegetables_production_multiplier = { value = 4 }` added to `common/script_values/
GOODS_svalues.txt`, referenced via `multiply = GOODS_vegetables_production_multiplier` inside
`GOODS_governorship_vegetables_produced`. Pharmaceuticals cross-good effect and glut-risk
self-damping both documented inline at the point of change, matching this doc's disclosures
above.
