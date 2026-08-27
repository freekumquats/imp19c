# Design: fix "War is likely" display driven by unbounded treasury term

## Finding (safety check, done before any code change)

`war_assessment` (country-scope var) is written ONLY by
`AI_diplomatic_play_evaluate_war` (`se_AI.txt:1302-1405`), which copies a
local var `AI_play_war_assessment` into it under a comment literally
reading `### DEBUG only - there is no reason to keep this variable`
(`se_AI.txt:1397`).

Full repo grep for `war_assessment` finds exactly two classes of reader:
1. Three display-bucket triggers in
   `common/scripted_triggers/imp19c_diplomacy_triggers.txt:8-22`
   (`DIPLOMACY_play_war_willing_trigger` / `_undecided_trigger` /
   `_reluctant_trigger`) — these drive the "War is likely" /
   "War is undecided" / "War is unlikely" loc text.
2. `AI_debug_test_war_all_diplomatic_plays` (`se_AI.txt:1407-1450+`) — a
   standalone debug utility effect. Grepped its own name repo-wide: it is
   **never called anywhere**. Dead code.

**Conclusion: `war_assessment` is 100% display-only.** No real AI
war-declaration decision reads it. It is therefore safe to change its
computation without any risk to actual AI behavior — the only consumer
is the player-facing text this task is fixing.

## Root cause

`AI_diplomatic_play_evaluate_war`'s formula sums several terms. Every
term except one is deliberately bounded:
- infamy cost and stability cost are each squared then capped at
  `max = 100000` (`se_AI.txt:1318-1327`) — since squaring a value over
  ~316 already exceeds that cap, these terms are implicitly designed
  for small (roughly 0-300) raw inputs.
- war-exhaustion terms are likewise multiplied and capped at
  `max = 100000` (`se_AI.txt:1334-1339`, `1356-1361`).
- the observer-support adjustments are small fractions of
  `DIPLOMACY_power` (`×0.01` / `×0.005`, `se_AI.txt:1376-1395`).

The one exception: `add = treasury` (`se_AI.txt:1354`), added completely
raw — no scaling, no cap. Treasury is a currency magnitude (this mod's
1763 economy runs on taels/wén at scales of thousands to tens of
millions per memory `1763-money-supply-research` /
`silver-reserve-figures`), several orders of magnitude larger than every
other term's ~0-300 working range. Any country with a positive treasury
(the normal case) pushes the whole score positive almost regardless of
the other terms, which is exactly the reported symptom: "War is likely"
reads positive near-permanently for a solvent instigator, independent of
`AI_play_attitude` (which is separately, properly scaled to ±20 and
bucketed at >20 — hence "Talks are friendly" can show at the same time
with no actual contradiction in the underlying math, just a broken
display term on one side).

This is consistent with the term being disowned by its own author as a
debug leftover — it was written once, never calibrated, and left in a
state where one term dominates the rest by construction.

## Fix

Bound the treasury term into the same rough order of magnitude as the
formula's other raw (pre-square) inputs, using `min`/`max` the same way
this formula already bounds every other term — this is the formula's
own established idiom, not a new pattern:

```
add = { value = treasury  min = -300  max = 300 }
```

This is a **best-guess magnitude**, not derived from a proven precedent
(no existing "treasury_scaled" or comparable normalization constant was
found elsewhere in the codebase — checked `WEALTH_total_private_moveable_wealth_scaled`,
which is a GDP-like denominator for ratios, not a fit for this raw-score
context). ±300 is chosen to match the implicit ~0-300 range the squared
cost terms operate in before their own cap, so treasury becomes a
comparable-weight input instead of a dominating one. **Logged under
ASSUMPTIONS & GUESSES for the next boot to confirm** — if "War is
likely" still reads as near-permanent after this, the bound needs
tightening further; if it now varies sensibly with the other inputs,
±300 was a reasonable first guess.

## Alternative considered and rejected

Building a wholly separate, parallel "display-only" normalized score
(distinct script_value/effect, leaving `AI_diplomatic_play_evaluate_war`
untouched) was considered, per the directive's stated preference for
touching shared logic as little as possible. Rejected because:
`war_assessment`'s ONLY consumers are display + dead debug code — there
is no "shared" AI logic here to protect. A parallel value would
duplicate ~50 lines of the same formula for no safety benefit, and would
still need the exact same guess for the treasury bound to be
meaningful — it just moves the guess to a second place instead of fixing
it in the one place the value is actually computed.

## Adversarial self-review (this fork has no Agent-tool access — see
hard rule; self-review substitutes)

- **Could this break the real AI's war decisions?** No — confirmed by
  the full-repo grep above; nothing else reads `war_assessment`, and
  this change does not touch `AI_play_war_assessment`'s local-var value
  in any way `AI_diplomatic_play_evaluate_war`'s CALLERS could observe
  (the local var itself is unaffected in scope/lifetime; only the raw
  `treasury` term feeding it is bounded).
- **Could ±300 be so wrong it makes the display WORSE (e.g. everything
  reads negative now)?** Possible if this mod's typical treasury values
  are, say, always in the low hundreds (then ±300 barely changes
  anything) or if the OTHER terms' real typical magnitudes are far
  larger than their ~300 implicit design range (then even a bounded
  treasury term still gets dwarfed the other way). This is exactly the
  kind of magnitude question that needs a boot to confirm, per skill
  Rule 1a — implementing the best guess now, not blocking on it.
- **Is there a less invasive fix?** Considered leaving `treasury`
  unbounded but flipping the display bucket's threshold from `> 0` to a
  larger constant (e.g. `> 5000`) to compensate. Rejected: this still
  leaves ANY two countries' comparison dominated by whichever has more
  money, for a metric that's supposed to reflect strategic risk
  calculus, not wealth ranking. Bounding the outlier term is more
  faithful to the formula's own evident intent (a bounded multi-factor
  score) than moving the goalposts on the threshold.
