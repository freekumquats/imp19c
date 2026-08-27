# Design: fix "War is likely" display driven by unbounded treasury term

## CORRECTION (2026-08-27) — the original safety claim below is FALSE

An independent review traced one hop further than the grep below and found
`war_assessment`'s three display-bucket triggers
(`common/scripted_triggers/imp19c_diplomacy_triggers.txt:8-22`) are
themselves read as `ai_chance factor=100` modifiers on real "Declare
war"/"Back down" event options in
`events/imp19c_mod_events/diplomatic_play/diplomatic_play_events.txt:631-636,735-856`,
`send_settlers.txt:90,142,199-293`, and `agadir_crisis_type.txt:312-368,
638-666`. **This is a real AI-behavior change, not a display-only fix.**
The "Finding" section immediately below is preserved for its accurate
grep work (the two reader CLASSES it found are correct) but its
conclusion ("100% display-only... safe to change without any risk to
actual AI behavior") does not hold — the display triggers are dual-use.

The original fix (bounding `treasury`) is NOT being reverted: the old
unbounded dominance was itself a real AI-decision-quality problem (any
solvent instigator became almost automatically war-willing regardless of
every other factor — a bug, not a feature). See "Recalibration" section
near the end for the corrected magnitude and reasoning.

## Finding (safety check, done before the original code change — CONCLUSION CORRECTED ABOVE)

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
   "War is undecided" / "War is unlikely" loc text **AND** (per the
   correction above) real `ai_chance` war/peace weighting.
2. `AI_debug_test_war_all_diplomatic_plays` (`se_AI.txt:1407-1450+`) — a
   standalone debug utility effect. Grepped its own name repo-wide: it is
   **never called anywhere**. Dead code — this part of the original
   finding still holds.

## Root cause

`AI_diplomatic_play_evaluate_war`'s formula sums several terms. Every
term except one is deliberately bounded:
- infamy cost and stability cost are each squared then capped at
  `max = 100000` (`se_AI.txt:1318-1327`) — this cap is a CEILING/backstop
  for pathological inputs, not evidence of the terms' typical real
  contribution (see Recalibration below — this distinction is exactly
  what the original fix's magnitude reasoning got wrong).
- war-exhaustion terms are likewise multiplied and capped at
  `max = 100000` (`se_AI.txt:1334-1339`, `1356-1361`).
- the observer-support adjustments are small fractions of
  `DIPLOMACY_power` (`×0.01` / `×0.005`, `se_AI.txt:1376-1395`).

The one exception: `add = treasury` (`se_AI.txt:1354`), added completely
raw — no scaling, no cap. Any country with a positive treasury (the
normal case) pushed the whole score positive almost regardless of the
other terms — this was the real symptom, and remains a real symptom for
both the display AND the `ai_chance` war-declaration weighting.

## Recalibration (2026-08-27) — replacing the ±300 guess with evidence

The original ±300 bound was justified by comparing treasury to the
sibling cost terms' `max = 100000` cap. That comparison is invalid: the
cap is a ceiling for extreme/pathological raw inputs (reached only if the
underlying infamy/stability cost value exceeds ~316), not a statement
about what those terms typically contribute for a normal AI country. No
conclusion should have been drawn from it about "matching" treasury's
scale to theirs.

Better evidence, gathered directly from this codebase:
- **Treasury thresholds already used elsewhere in this mod** (mission
  `allow`/trigger gates in `qing_new_world_missions.txt`,
  `qing_burma_war_missions.txt`, and others) cluster between 40 and 440,
  with common values at 55, 60, 70, 80, 100, 120, 150, 220, 255, 285, 310,
  360, 400, 440. These are the mod's own de facto definition of
  "meaningful" treasury magnitudes for gating AI/player behavior — nowhere
  near the "thousands to tens of millions" scale the original fix's
  comment speculated (that speculation was unverified and appears to have
  been wrong).
- **A sibling AI scoring formula in the same file family**
  (`AI_svalues.txt:2069`, the AI's peace-suing threshold score) treats
  treasury with `value = treasury, multiply = 0.02` against a base-50
  scale, when treasury is negative — a proportional-scaling idiom, not a
  hard clamp. Its base scale (50) is much smaller than
  `AI_diplomatic_play_evaluate_war`'s (implicit 0-100000 per term), so its
  exact multiplier doesn't transfer directly, but it confirms this
  codebase's convention is "scale treasury down to be proportional to the
  formula it's entering," which a hard min/max clamp also achieves, just
  more bluntly.

Given this evidence, ±300 was not badly wrong — it sits within the mod's
own observed range of "meaningful" treasury magnitudes, just below the
top of the "very wealthy" cluster (400/440). Adjusted to **±400** to
cover that top end without reopening the original runaway-dominance
problem: a treasury of 10,000+ (if that scale ever occurs — unconfirmed
without a boot) still contributes no more than any other single term's
typical range, while a treasury of 40-440 (the mod's own common gate
range) now contributes close to its full raw value, proportional and
comparable to the other terms instead of dominating or being negligible.

```
add = { value = treasury  min = -400  max = 400 }
```

**Still a best-guess magnitude** — the exact typical treasury range for
mid/late-game AI countries in a live save is Jomini-engine-derived and
not fully derivable from static source. Logged under ASSUMPTIONS &
GUESSES for the next boot to confirm AI war-declaration FREQUENCY (not
just the display text) looks sensible — if AI countries still seem to
declare war almost regardless of attitude/stability, tighten further; if
AI countries with strong treasuries now seem under-weighted toward war
even when otherwise justified, loosen toward the observed 440 ceiling or
beyond.

## Alternative considered and rejected

Building a wholly separate, parallel "display-only" normalized score was
considered and is now DEFINITELELY rejected, not just for the original
reason (no separate concern to protect) but because it's now known the
real display triggers are dual-use — a parallel value would fail to fix
the actual AI-decision-weighting problem, only cosmetics, which was never
the actual complete symptom.

## Adversarial self-review (no Agent-tool access in this fork context — self-review substitutes, per this session's repeated fork-tooling constraint)

- **Could bounding treasury at ±400 instead of ±300 meaningfully change
  AI behavior versus the already-shipped ±300?** Only for instigators
  with treasury in the 300-400 (or -300 to -400) range, where the score
  contribution grows by at most 100 magnitude — small relative to the
  other terms' working range, not a dramatic behavior swing versus what
  already shipped.
- **Is there a risk the ±400 bound is still wrong in the OTHER
  direction (too generous, restoring dominance)?** No — the "very
  wealthy" mission-threshold ceiling observed in this codebase is 440;
  countries far above that (if such extreme treasuries occur) are capped
  the same way instigators just past today's 400/440 threshold are,
  matching the mod's own established idea of "very wealthy" as a ceiling,
  not an unbounded ramp.
- **Did the recalibration touch anything besides the treasury bound?**
  No — same single `add = { value = treasury ... }` line, only the
  min/max constants changed (300→400); no other term, no other effect.
