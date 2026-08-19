# ANALYSIS — task #15: is the ±10% food-demand "ratchet" a defect, or a correct rate limiter?

**Status:** ANALYSIS → for adversarial review (NO boot needed; settle by derivation).
**Origin:** flagged during #14 as a "compounding ratchet" that latches vegetables demand near 0.
This doc RE-DERIVES the mechanism to decide whether to fix it, and reaches a different answer.

## The mechanism, derived from source

Per quarter, per governorship, per food good, in `DEMAND_set_demand_from_food` (se_DEMAND.txt):
1. **Bands set (`:128-149`)** from the SVALUE read `DEMAND_food_$good$`:
   `previous_tick_food_demand_$good$` = that read; `_110_percent` = ×1.1; `_90_percent` = ×0.9.
2. **Raw recomputed (`:155-218`)** into `var:DEMAND_food_$good$`: base = unfulfilled_food_need/6,
   then ÷ num_food_goods, then ÷ price-elasticity ratio. This is the RAW value; the var holds it
   UNCLAMPED (no clamp is ever written back to the var).
3. **Consumed on read**: the svalue `DEMAND_food_$good$` (`DEMAND_food_svalues_new.txt`) returns
   `clamp(var:DEMAND_food_$good$, [ _90_percent, _110_percent ])` — this clamped value is what
   `DEMAND_$good$` (→ order size) actually consumes.

Let `output_N` = the consumed (clamped) svalue at tick N, `raw_N` = the recomputed var at tick N.
- At tick N step 1, the svalue read = `clamp(raw_{N-1}, bands_{N-1})` = `output_{N-1}`.
  So `bands_N = [0.9·output_{N-1}, 1.1·output_{N-1}]`.
- Therefore **`output_N = clamp(raw_N, [0.9·output_{N-1}, 1.1·output_{N-1}])`**.

## Conclusion: this is a STANDARD multiplicative rate limiter, not a bug

`output_N = clamp(input_N, [0.9·output_{N-1}, 1.1·output_{N-1}])` is the textbook form of a ±10%/
tick multiplicative rate limiter. Its reference is the PREVIOUS OUTPUT — which is correct, not a
"self-referential compounding bug." Consequences that are INTENDED, not defects:
- Traversing a large gap (e.g. 10×) takes ~`log_1.1(10)`≈24 quarters. Slow recovery from a deep
  crush is the *definition* of rate limiting, and the code comment states the intent explicitly
  ("bound food demand at 10% either side of the previous value").
- The deep crush that made this visible for vegetables was the **supply shortage** (few veg
  provinces → price spike → elasticity divide crushes raw demand), addressed by the #5 reseed and
  the Site-A price div/0 fix. With supply restored, raw stops being crushed and the limiter simply
  damps gently around a stable demand.

**"Fixing" it by deriving the bands from the RAW var would make `output_N = clamp(raw_N, ±10% of
raw_{N-1})`; since the var jumps to the full raw each tick, output would reach the raw in ~1 tick —
i.e. it DISABLES the damping. That is a regression, not a fix.** So there is no structural change
to make.

## The 0-fixed-point concern — REFUTED by review (kept for the record)
I worried a multiplicative limiter has a fixed point at 0 (band `[0,0]` latching). The adversarial
review showed this reasoning is WRONG: the ceiling line is guarded `var:..._110_percent > 0`
(DEMAND_food_svalues_new.txt:19-20 + per-good siblings), so even a hypothetical `[0,0]` band releases
to raw in one tick — it cannot latch. Also the read-side `min` floor lifts a zeroed var back to
`0.9·output_{N-1} > 0`, so `DEMAND_scale_down_food_demand` writing var=0 (se_DEMAND.txt:507-515)
never zeros the band base, and the first-tick base is `DEMAND_food_base > 0`. So exact-0 is NOT
reachable in practice. No hardening needed.

## VERDICT (adversarial review, 2026-08-19): CONCLUSION SOUND — CLOSE #15, NOT A DEFECT
- The ±10% clamp is a correct multiplicative rate limiter keyed to the previous OUTPUT. No structural
  fix. "bands-from-raw" is confirmed a regression (collapses damping to a one-tick lag).
- Exact-0 latch not reachable (guards above). The vegetables collapse was SUPPLY (task #5), not this.
- Minor, non-blocking hygiene the reviewer noted (NOT fixed here — out of scope, avoid churn):
  `previous_tick_food_demand_$g$` (se_DEMAND.txt:128-131) is set-but-never-read (dead); the New-World
  crop else-branches (se_DEMAND.txt:99/104/109) remove the demand var but leave stale `_110/_90` band
  vars. Neither affects vegetables or correctness.

## Disposition
- **No correctness defect** → no structural fix; the `bands-from-raw` idea is rejected as a
  damping-disabling regression.
- **±10%/quarter aggressiveness is a TUNING choice**, not a bug. Widening it (e.g. ±20-25%/quarter)
  would speed recovery but increases food-demand volatility — the very thing the limiter exists to
  damp — so it is a two-sided change that should be made only with evidence, not speculatively.
- **Action:** submit this conclusion to adversarial review. If it survives, CLOSE #15 as
  not-a-defect. If the review finds the 0-fixed-point IS hit in practice, or an asymmetry/other
  real defect, fix that specific thing.
