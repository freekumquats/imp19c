# DESIGN — #93: vegetables global-stockpile depletion to zero

## Status
Diagnosis adversarially reviewed. Core mechanism SURVIVES review; 3 supporting details
corrected below (province counts, livestock's true consumer count, the real protective
factor). FIX design round 1 (a dynamic shortage-throttle) FAILED review with a CRITICAL
same-tick circular-dependency defect (see "Rejected approach" below) — round 2 (this
version) adopts the review's own suggested simpler alternative instead. Not yet re-reviewed.

## The bug, precisely (corrected)

Vegetables' global stockpile (summed across all 22 trade zones) declines steadily through a
real boot and hits exactly 0 at quarter-mark 11, then stays at 0 for the rest of the run
(`tools/vegetables_trace.py`). Every comparable staple food good (grain, livestock, fish,
temperate_fruit) stayed healthy (10000-100000) the whole run.

**Production side** (`setup/provinces/*.txt`, `trade_goods=` field, recounted directly):
vegetables 419 provinces, temperate_fruit 661, fish 668, grain 1747, livestock 1885. Vegetables
has by far the smallest production base of any actively-produced staple.

**Demand side** (`common/script_values/DEMAND_food_svalues_new.txt`): vegetables is consumed by
**3** industrial chains — alcohol (`INDUSTRY_demand_alcohol_vegetables` = factories × 5,
`INDUSTRY_svalues.txt:1364-1387`), pharmaceuticals (× 6, `:2481-2489`), processed_foods (× 6,
`:3097-3105`). **Correction**: the original diagnosis claimed "every sibling has at most one
consumer" — false. Livestock has **4** consumers (clothing, luxury_clothing, early_artillery,
processed_foods, `DEMAND_food_svalues_new.txt:153-191`), with a HIGHER aggregate per-factory
demand (21) than vegetables' (17). Livestock does not collapse anyway, because its production
base (1885 provinces) is 4.5x vegetables'.

**The real protective factor is demand-pressure-per-producing-province, not consumer count**:
- vegetables: 17 demand / 419 provinces = **0.0406**
- temperate_fruit: 10 / 661 = 0.0151
- grain: 20 / 1747 = 0.0114
- livestock: 21 / 1885 = 0.0111
- fish: 4 / 668 = 0.0060

Vegetables' pressure is ~2.7x the next-worst good and ~3.6x livestock/grain. This is why
vegetables is the good that collapses, not "vegetables uniquely has industrial demand."

**The non-clearing mechanism** (confirmed, this part of the original diagnosis holds): the
malus formulas (`INDUSTRY_malus_alcohol_production_vegetables` etc., `INDUSTRY_svalues.txt:
1364-1373`) reduce factory OUTPUT once `shortage_vegetables` exists (a generic per-good
variable set by `se_CONSUME.txt`'s shared `$tradegood$`-parametrized shortage effect — not
vegetables-specific machinery). But `INDUSTRY_demand_alcohol_vegetables` etc. are unconditional
(`factories_assigned × flat base`) — they never reference `shortage_vegetables` at all. Once
stock hits 0, demand keeps drawing at full rate forever; there is no feedback loop to let the
stock recover. This is the actual bug: a missing shortage-responsive term on the demand side.

**Pop-level (non-industrial) base demand is NOT the differentiator.** `DEMAND_food_vegetables`
(`:230-249`) uses the same smoothing shape as every other food good (clamped to ±10% of the
previous tick via `previous_tick_food_demand_vegetables_110_percent`/`_90_percent`) — this is a
volatility damper, not a scarcity throttle, and it is IDENTICAL in shape across all five staples.
It is not what makes vegetables special, and changing it would deviate from a shared convention
used by every food good, not just vegetables.

**Verdict: genuine bug, not intentional scarcity.** Three independent #133 manufactured-goods
wiring passes each added a vegetables consumer without checking the aggregate draw against
vegetables' comparatively thin production base, and there is no demand-side shortage feedback
anywhere in the formula to self-correct once the deficit starts.

## Two fix options (per explicit request: assess both, decide feasibility)

### Option A — Supply side: increase vegetables' production base

Concretely: assign more provinces `trade_goods="vegetables"`, or boost the production formula
(`GOODS_governorship_vegetables_produced`, `GOODS_svalues.txt:1963-1974`) with an added
multiplier vegetables alone would get.

**Feasibility: LOW.** This mod's province trade-good assignment is the product of dedicated,
sourced historical-geography research (memory: `imp19c-nwcrop-geography-64` — "crops seeded
backwards... real ranges per-crop"; `imp19c-china-granularity-rule` — China fine-fidelity is a
standing project convention). Vegetables' 419-province assignment is very likely *correct*
historically (vegetables are not a broad-acreage staple crop the way grain/livestock are) — it is
not an oversight to "fix" by adding provinces arbitrarily. Doing so would fight the project's own
established research discipline for a balance patch, and touching many province files is a much
larger, harder-to-verify-safe change than the alternative. A vegetables-only production-formula
multiplier (not touching province assignment) is *slightly* more feasible, but still invents a
special-cased bonus with no historical grounding, purely to compensate for a demand-side defect
— treating the symptom's mirror image rather than the actual missing mechanism.

### Option B, REJECTED first attempt — dynamic shortage-throttle on demand

First design round proposed reading `shortage_vegetables` (the SAME variable the malus formulas
already consume) inside the 3 demand formulas, throttling demand as shortage rises. **Adversarial
review found this CRITICALLY broken**: `shortage_vegetables` is not an independent scarcity
signal — it is computed (`se_CONSUME.txt` `CONSUME_update_shortage`) by dividing the raw deficit
BY `DEMAND_vegetables` itself, the exact quantity the proposed fix throttles. Making demand read
its own divisor mid-computation is a same-tick circular dependency: on a collapse tick the
throttle degenerates to a binary "cut to the 10% floor," and — worse — since the malus formulas
read the SAME now-corrupted `shortage_vegetables`, the fix silently maxes out the production
malus too, despite the design's explicit claim that it wouldn't touch the malus at all. Rejected.

### Option B, REVISED — statically retune the 3 industrial base-demand constants

The root cause (see above) is that vegetables' aggregate industrial demand-per-producing-province
(0.0406) is ~2.7x the next-worst staple's. That ratio is set by three INVENTED mod coefficients —
not researched geography, not an engine default — with no shortage-feedback mechanism involved at
all:
- `INDUSTRY_base_demand_alcohol_vegetables = 5` (`INDUSTRY_svalues.txt:1380-1382`)
- `INDUSTRY_base_demand_pharmaceuticals_vegetables = 6` (`:2481-2484`)
- `INDUSTRY_base_demand_processed_foods_vegetables = 6` (`:3097-3100`)

Lowering these three flat constants attacks the actual measured imbalance directly, with:
- **No new mechanism, no feedback loop, no circular read** — plain constants, evaluated once per
  formula, same shape every other good's base-demand constant already uses.
- **Zero interaction with `shortage_vegetables` or the malus formulas** — those are untouched,
  fully honoring the delicate-fix principle this design already committed to.
- **Zero interaction with province geography** — no `setup/provinces/*.txt` edit, no conflict with
  this project's sourced crop-geography research.

Target: bring vegetables' demand-pressure-per-province down to roughly parity with the next-worst
staple (temperate_fruit, 0.0151) rather than to zero — this should still let vegetables run tight
(consistent with its real thin production base) without guaranteeing total, permanent collapse.
Current aggregate per-factory demand is 17 (5+6+6); target ballpark is 17 × (0.0151/0.0406) ≈ 6.3.
Best-guess allocation (proportional trim, preserving each consumer's relative weight):
- `alcohol`: 5 → 2 (was 0.15 importance weight, keep it the smallest of the three)
- `pharmaceuticals`: 6 → 2
- `processed_foods`: 6 → 2
This is a best-guess tuning split, not derived from a formula — logged plainly as a guess per the
overnight "guess and log" convention; a boot's `tools/vegetables_trace.py` output will show
whether the new aggregate (6) actually stops the collapse, and the exact 2/2/2 split can be
retuned in proportion if one industry still starves disproportionately.

### Option A — Supply side: increase vegetables' production base

Concretely: assign more provinces `trade_goods="vegetables"`, or boost the production formula
(`GOODS_governorship_vegetables_produced`, `GOODS_svalues.txt:1963-1974`) with an added
multiplier vegetables alone would get.

**Feasibility: LOW.** This mod's province trade-good assignment is the product of dedicated,
sourced historical-geography research (memory: `imp19c-nwcrop-geography-64` — "crops seeded
backwards... real ranges per-crop"; `imp19c-china-granularity-rule` — China fine-fidelity is a
standing project convention). Vegetables' 419-province assignment is very likely *correct*
historically (vegetables are not a broad-acreage staple crop the way grain/livestock are) — it is
not an oversight to "fix" by adding provinces arbitrarily. A vegetables-only production-formula
multiplier (not touching province assignment) is a real, viable secondary lever — unlike
province reassignment it does not fight the geography research — but the retuned base-demand
constants above already remove the deficit at its actual source (aggregate demand vs. production
base), so a production bonus on top is unnecessary unless a boot shows the demand retune alone is
insufficient.

### Recommendation

**Retuned Option B (static base-demand constants) alone, for the first pass.** It is simpler than
the rejected dynamic throttle, has no circular dependency, touches nothing shared with the malus
or #69's fix, and directly targets the measured imbalance. Keep Option A's production-multiplier
variant in reserve as a documented fallback if a boot shows the retune under- or over-corrects.

## Implementation sketch (for review, not final code)

1. `INDUSTRY_base_demand_alcohol_vegetables` (`INDUSTRY_svalues.txt:1380-1382`): `value = 5` ->
   `value = 2`.
2. `INDUSTRY_base_demand_pharmaceuticals_vegetables` (`:2481-2484`): `value = 6` -> `value = 2`.
3. `INDUSTRY_base_demand_processed_foods_vegetables` (`:3097-3100`): `value = 6` -> `value = 2`.
4. No change to the SCRIPT of `se_CONSUME.txt`, `shortage_vegetables`, the malus formulas,
   `DEMAND_food_vegetables` (pop-level base demand), or any other good's demand formula. Their
   RUNTIME VALUES will improve as a downstream consequence (lower base_demand -> lower
   DEMAND_vegetables -> smaller deficit -> lower shortage_vegetables -> lower malus -> recovered
   output) -- the fix works partly THROUGH the malus chain, not around it; "no change" means the
   formulas themselves are untouched, not that their behavior is unaffected.
5. The 2/2/2 split is a best-guess tuning constant, logged plainly as a guess (see above) — not a
   blocking unknown, matches the overnight "guess and log" convention.

## Risks / open questions for adversarial review

- Does trimming these three constants meaningfully reduce OTHER outputs downstream (alcohol/
  pharmaceuticals/processed_foods production itself, since their own BOM-consumption of
  vegetables is now capped lower per factory) in a way that creates a NEW shortage elsewhere
  (e.g. processed_foods itself, already noted as chronically at 0 for unrelated reasons)? Trace
  whether lowering vegetables' base-demand also lowers alcohol/pharma/processed_foods' own
  PRODUCTION formulas (i.e. is `INDUSTRY_base_demand_alcohol_vegetables` purely an input-cost
  term, or does it also gate output volume for that industry?).
- Is 2/2/2 the right split, or should the trim be non-uniform (e.g. keep alcohol closer to its
  original 5 since it has the lowest `INDUSTRY_demand_importance` weight of 0.15, meaning its
  malus impact per unit of shortage is already the smallest)? A real boot's trace is the only way
  to properly tune this — logged as a guess, not a blocking unknown.
- Interaction with #69 (already fixed): confirmed genuinely resolved — #69 writes
  `<good>_ess_last_nonzero_price` and reads `global_stockpile_<good>`/`country_unit_price_<good>`;
  this design reads/writes only the three base-demand constants, never touching any variable #69's
  fix reads or writes. Complementary (this fix reducing consumption makes #69's collapse branch
  fire less often), not conflicting.
