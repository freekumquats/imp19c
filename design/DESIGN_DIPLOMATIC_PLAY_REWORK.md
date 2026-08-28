# Design: rework diplomatic play war/attitude decision logic

Supersedes/extends `design/DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md`, which
covers only the treasury-term bounding history (±300 → ±400, and the
"SECOND CORRECTION" noting ±400 was never actually derived against the
real decision boundary). This doc covers the full pipeline end-to-end:
what feeds `war_assessment` and `AI_play_attitude`, how they gate both
the player-facing text AND the AI's actual event-option choices, and why
"War is likely" + "Talks are friendly" can display together with no
error anywhere in the code (task #15, confirmed live in-game).

## Pipeline map

1. **Play begins** → `AI_diplomatic_play_evaluate_attitude` (`se_AI.txt:1233`)
   sets `AI_play_attitude` = `AI_friendly` (religion/culture match, +50
   each) minus `AI_hostile` (power-balance term + ideological distance×10
   + core-province claims×20). Unbounded on either side; no cap.
2. **Same tick** → `AI_diplomatic_play_evaluate_war` (`se_AI.txt:1302`)
   computes `AI_play_war_assessment`, copied verbatim into `war_assessment`
   (`se_AI.txt:1422`). This formula is NOT independent of attitude — it
   re-reads `AI_play_attitude` at `se_AI.txt:1328-1332`:
   ```
   subtract = { value = var:AI_play_attitude
                multiply = scope:diplomatic_play.var:AI_play_power_balance_instigator_root
                max = 100000 }
   ```
   `AI_play_power_balance_instigator_root` (`se_AI.txt:1181-1196`) is
   `(instigator_power/100) / (target_power/100)`, capped at 90.01. So
   attitude's effect on the war decision is **attitude × power-ratio**,
   not raw attitude — the SAME input the display trigger reads raw.
3. **Display triggers** (`imp19c_diplomacy_triggers.txt`) bucket the two
   RAW variables independently: `war_assessment > 0` → "War is likely"
   (`:1-10`); `AI_play_attitude > 20` → "Talks are friendly" (`:25-31`).
   Both thresholds are named script_value constants
   (`DIPLOMACY_play_war_willing`, `DIPLOMACY_play_attitude_friendly`),
   defined in `DIPLOMACY_svalues.txt:503` and `:495` as 0 and 20
   respectively — cited here as literals for readability, but a future
   re-tune of either constant would need this doc's numbers re-checked.
   Neither trigger looks at the other's variable, the power-ratio term,
   or any of war_assessment's other terms.
4. **Same triggers gate real AI choices.** `diplomatic_play_events.txt`,
   `send_settlers.txt`, `agadir_crisis_type.txt` use these exact triggers
   inside `ai_chance = { modifier = { factor = N ... } }` blocks on
   "Declare war" / "Back down" / "Allow settlers" / "Drive them out"
   options. Confirmed 16 occurrences of the two triggers across the three
   files (9 war_willing + 7 attitude_friendly). `ai_chance` modifiers in
   this engine are **multiplicative**, not additive — this matches
   established Jomini/Imperator `ai_chance` semantics (factor multiplies
   the running weight), but is asserted here as engine behavior, not
   independently re-derived from this codebase. E.g. `send_settlers.1.b`
   (`:121-154`) stacks `factor=30` (opinion>0) × `factor=30`
   (attitude_friendly) × `factor=30` (war_willing=no) × `factor=100`
   (attitude_friendly AGAIN, a duplicate of the second modifier — likely
   an authoring mistake, not an intentional double-weight) =
   30×30×30×100 = **2,700,000**× the base weight. Any single
   `factor=100` trigger (the common pattern for
   `war_willing_trigger`/`attitude_friendly_trigger`) already dwarfs the
   base factors (1-30 range) other considerations use (foreign-minister
   stats, opinion, power balance) by 3-4 orders of magnitude. The
   war/attitude triggers aren't "a factor among several" for the AI's
   actual choice — they are overwhelmingly the deciding factor.

## Root cause of the contradiction (task #15)

Both display texts read from the *same underlying signal* (attitude),
but through two different transforms:
- **"Talks are friendly"** reads `AI_play_attitude` raw, uncapped,
  unscaled.
- **"War is likely"** reads `war_assessment`, in which attitude's
  contribution is `attitude × power_ratio` (capped 100000) — one term
  among ~11, alongside treasury (±400, per the existing but *unvalidated*
  bound — see the "SECOND CORRECTION" in the superseded doc), infamy/
  stability cost (squared; infamy base 100² = 10,000, stability base
  50² = 2,500 before adjustments — confirmed by reading
  `play_infamy_cost_war` at `se_AI.txt:499-560` and
  `play_stability_cost_war` starting at `:561` — both well below the
  100000 cap in normal play, but infamy in particular is NOT "hundreds,"
  it's five figures before adjustment), instigator/target war exhaustion
  and stability, a truce check, and observer-support subtraction.
  **Correction:** the infamy/stability terms are SUBTRACTED from
  `war_assessment`, not added — they only ever push the score DOWN, never
  up. For `war_assessment > 0`, the positive contributors must dominate:
  treasury (+400 max), instigator `add = stability` (`se_AI.txt:1352`),
  and target war-exhaustion (`×60`, `:1373`). The infamy/stability
  *cost* terms only matter here in that they must be SMALL for the
  positive terms to win — and what makes them small is specific, not
  generic: their definitions reduce cost by
  `civilization_value × 2` per province in the target area and by `+75`
  per instigator core already in that area, while core overlap
  separately RAISES `AI_hostile` (`+20` each) and thus LOWERS attitude.
  So the contradiction requires a configuration where cost-suppressing
  conditions hold (industrialized target, no core overlap) WITHOUT the
  attitude-suppressing ones (no core overlap) also firing — e.g. two
  peer industrial nations with no territorial claim on each other. This
  is a real, reachable configuration, but it is a **specific** one, not
  the "any evenly-matched solvent instigator" framing below might
  suggest.

At power_ratio ≈ 1 (evenly matched instigator/target), attitude's
contribution to `war_assessment` shrinks to roughly its raw value
(±20-ish typical range), which is then weighed against treasury (±400)
and the (small, in this configuration) cost terms. A friendly,
evenly-matched, moderately-solvent instigator with no core claim on the
target and an industrialized target area can score `war_assessment > 0`
mostly from treasury while `AI_play_attitude` independently reads `> 20`
(friendly) — no error in either individual computation, but a specific,
reachable configuration, not a universal one.

This is NOT primarily a "treasury is too big" problem (that's the
already-tracked, still-unvalidated `DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md`
issue). It is a **missing reconciliation** problem: nothing checks
whether the war-willingness conclusion and the attitude conclusion agree
before either is shown or acted on.

## USER DIRECTIVE (2026-08-28): war_assessment rearchitected around military strength

**This supersedes the "Proposed fix" section below** — the user's own diagnosis
of the deeper problem: `war_assessment` currently has no direct term for "can
I actually win this war." The only place relative strength appears at all is
as a multiplier on the attitude term (`AI_play_power_balance_instigator_root`,
itself diluted by economy/tech/subjects, not a military-only measure) — never
a standalone assessment of comparative military strength. Directive: rebuild
`war_assessment` so relative military strength is the **PRIMARY, dominant**
term, with war exhaustion, treasury (**uncapped** — the ±400 bound from
`DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md` is explicitly overridden here, not
reused), and stability as **secondary** terms.

**User confirmation received:** the existing terms (infamy/stability cost, war
exhaustion, treasury, stability) are not being discarded — they remain real
factors, just demoted to secondary. And relative military strength must
include **supporters**, not just each side's own standing forces: both
permanent allies AND this specific play's backers (the play can attract
support from countries with no formal alliance at all).

**Proven building blocks already in this codebase** (per the standing rule to
reuse proven idioms, not invent new ones):
- `AI_svalues.txt`'s peace-suing score (~line 2100-2115) already builds a
  military-strength figure from `num_of_cohorts` (army) + `num_of_ships × 0.1`
  (navy, weighted down — ships are pricier/rarer than cohorts) +
  `every_allied_country { add = num_of_cohorts }` (allied strength counts).
- `DIPLOMACY_power_from_military` (`DIPLOMACY_svalues.txt:106-119`) adds a
  manpower-reserve term: `manpower × (0.2 + military_tech × 0.02 × 0.2)`
  roughly — i.e. manpower matters, scaled up by military tech.
- The CURRENT `war_assessment` formula already walks this specific play's
  supporters via `every_in_list { variable = play_observers_support_target /
  play_observers_support_instigator }` (`se_AI.txt` ~1375-1395) — but only
  weighs each supporter by `THIS.DIPLOMACY_power × 0.01/0.005`, a token
  fraction of a broad (non-military-only) power index. The rework reuses
  this SAME proven list/iterator, but replaces that weak weighting with each
  supporter's actual `num_of_cohorts`/`num_of_ships` — consistent with how
  the ally term treats permanent allies.
- Note: `every_allied_country` is the proven mod-wide iterator name (confirmed
  6 uses, `se_AI.txt:1056`, `AI_svalues.txt:1741/1871/2114`, etc.) — there is
  no proven `every_ally`; do not introduce it.

**Proposed new formula shape** (military strength — own forces + permanent
allies + this play's supporters, on both sides — as one dominant add/subtract
pair, weighted well above every secondary term — exact weight is a tunable
judgment call, flagged below):
```
value = 0
add = {
    # PRIMARY — relative military strength, instigator side vs. target side.
    # "Side" = own forces + permanent allies + THIS PLAY's supporters.
    value = {
        value = 0
        add = var:play_instigator.num_of_cohorts
        add = { value = var:play_instigator.num_of_ships  multiply = 0.1 }
        add = { value = var:play_instigator.manpower       multiply = 0.05 }
        var:play_instigator = {
            every_allied_country = { add = num_of_cohorts }
        }
        # this play's supporters on the instigator's side (not just formal allies)
        every_in_list = {
            variable = play_observers_support_instigator
            add = { value = THIS.num_of_cohorts }
            add = { value = THIS.num_of_ships  multiply = 0.1 }
        }
    }
    subtract = {
        value = 0
        add = var:play_target_country.num_of_cohorts
        add = { value = var:play_target_country.num_of_ships  multiply = 0.1 }
        add = { value = var:play_target_country.manpower       multiply = 0.05 }
        var:play_target_country = {
            every_allied_country = { add = num_of_cohorts }
        }
        # this play's supporters on the target's side
        every_in_list = {
            variable = play_observers_support_target
            add = { value = THIS.num_of_cohorts }
            add = { value = THIS.num_of_ships  multiply = 0.1 }
        }
    }
    multiply = <WEIGHT — tunable, needs to dominate the secondary terms below;
                start high (e.g. 10-20x) and confirm via boot that war
                frequency now tracks actual military balance, not treasury>
}
# SECONDARY terms — still real, still applied, but no longer able to
# outweigh the primary military term on their own (per user confirmation):
subtract = { value = var:play_infamy_cost_war     multiply = var:play_infamy_cost_war     max = 100000 }
subtract = { value = var:play_stability_cost_war  multiply = var:play_stability_cost_war  max = 100000 }
var:play_instigator = {
    subtract = { value = has_war_exhaustion  multiply = 120  multiply = has_war_exhaustion  max = 100000 }
    if    = { limit = { stability < 50 }  subtract = { value = 50  subtract = stability  multiply = 500  max = 100000 } }
    else  = { add = stability }
    add   = treasury   # UNCAPPED per this directive -- no min/max
}
var:play_target_country = {
    add = { value = has_war_exhaustion  multiply = 60  max = 100000 }
    subtract = stability
}
# truce veto and observer-support terms unchanged from the current formula.
```

**What happens to the attitude term:** the directive's factor list (military
strength, war exhaustion, treasury, stability) does not mention attitude.
Judgment call, flagged for confirmation: **removing `AI_play_attitude` from
`war_assessment` entirely**, rather than keeping it as a demoted secondary
term. This is not just an omission — it directly resolves task #15's original
contradiction at its root, rather than just rebalancing it: `war_assessment`
becomes purely "can I win, and can I afford to fight" (military + economic),
while `AI_play_attitude` remains its own, fully independent "do I like them"
signal. The two no longer read overlapping inputs through different
transforms, so "War is likely" and "Talks are friendly" can still co-occur,
but it stops being an artifact of shared-input dilution — it becomes two
genuinely orthogonal questions, which is a coherent thing for two different
texts to say. If this reading is wrong and attitude should stay in as a
(smaller) secondary term instead, flag it and it can be re-added as one more
`subtract` line without changing the rest of the shape.

**Does not fix on its own:** the event-level `ai_chance` weighting problem
found while tracing "what happens when both fire" (`send_settlers.1`/`.3`
stacking attitude-friendly modifiers, including the likely copy-paste
duplicate at `send_settlers.txt:145-150`, up to `×3000`/`×100` against a
war-willing signal that only gets `×10`). Rebuilding `war_assessment` changes
*what the war-willing trigger means*, but every event option's own `ai_chance`
weights are separate numbers, set independently per event, and still need
their own pass to reflect the new formula's intent (e.g. if military strength
now dominates war_assessment, an event's "Declare war" option arguably
deserves a bigger factor than the flat `×10`/`×100` patterns used today,
proportional to how lopsided the military balance is — not just a boolean
willing/not-willing switch). Flagging as the next step once the formula
itself is confirmed, not bundled into this change.

## Proposed fix (SUPERSEDED — kept for record, see directive above)

1. **Add an explicit reconciliation trigger**, e.g.
   `DIPLOMACY_play_war_attitude_conflict_trigger` = "war_assessment
   crosses war-willing while AI_play_attitude simultaneously crosses
   friendly." Use it in one of two ways (needs user decision, this is a
   game-feel choice, not purely technical):
   - **(a) Suppress the war-willing display/ai_chance boost** when
     attitude is friendly, on the theory that goodwill should be able to
     override a marginal treasury-driven war score. This changes AI
     behavior (fewer wars against friendly targets), not just text.
   - **(b) Show both, but change the wording** ("despite friendly talks,
     war looms" style text) so the player understands the game means it,
     rather than reading it as a bug. Zero behavior change, pure
     UX/loc fix.
   Recommend **(b)** as the low-risk default, with **(a)** as a
   follow-up only if the user decides the AI should actually behave
   differently, not just describe itself more honestly.
   **Tension flagged by independent review:** (b) sits awkwardly next to
   this doc's own finding that `war_assessment` is behavior-authoritative,
   not display-only — rewording the text leaves the AI still declaring
   the war. An unconsidered middle option exists between full (a)
   suppression and text-only (b): give attitude a LARGER (or uncapped)
   weight inside `war_assessment` itself, or gate the war-willing
   trigger's `ai_chance` factor (not just its display text) on attitude,
   without a fully separate reconciliation trigger. This is lighter than
   (a) but still a real behavior change, so it still needs the user's
   game-feel call, not a default recommendation.
2. **Separately, and regardless of (a)/(b):** the duplicate
   `DIPLOMACY_play_attitude_friendly_trigger = yes` modifier in
   `send_settlers.txt:133-138` and `:145-150` (identical trigger, two
   separate `modifier` blocks, factors 30 and 100) looks like a
   copy-paste error, not an intentional double-weight. Flagging for a
   differential check against the other options in the same event to
   confirm before touching it — do not "fix" without checking whether
   this was deliberate escalation.
3. **Do not touch the ±400 treasury bound as part of this rework** —
   that's `DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md`'s open item (still
   flagged there as needing live boot telemetry against the `war_assessment
   > 0` boundary, not a static-analysis fix). Keep the two docs separate;
   this rework's fix should not silently re-derive that number as a side
   effect.
4. **Consider whether `ai_chance factor=100` on a single boolean trigger
   is too blunt a lever** given the multiplicative-stacking finding
   above — a single trigger currently outweighs every other
   consideration by 3-4 orders of magnitude. This is a bigger, riskier
   change (touches real AI event-choice weighting mod-wide, not just
   this one contradiction) — flagging as a candidate for a SEPARATE
   follow-up task, not bundled into this fix.

## Alternatives considered and rejected

- **Merge `war_assessment` and `AI_play_attitude` into one unified
  score.** Rejected: they answer different questions (should I go to
  war vs. how do I feel about this country) and vanilla-style AI
  scoring in this mod's own precedent (`AI_svalues.txt`) keeps
  war-desire and attitude as separate concerns everywhere else observed.
  A merge would be a much larger, riskier change than the actual
  reported symptom needs.
- **Delete one of the two display texts.** Rejected: both are
  legitimate, independently-meaningful signals to the player; the bug
  is the lack of reconciliation, not that either signal individually is
  wrong.

## Adversarial self-review

- **Could recommendation (b) alone leave the AI still "behaving badly"
  even if the text stops looking contradictory?** Yes — (b) is
  explicitly a text-only fix. If the user wants the AI to actually be
  less war-happy toward friendly targets, (a) is required, and that is
  a real behavior change needing its own careful review (per this
  session's AI-logic-change standing caution), not a mechanical
  follow-on.
- **Is the "duplicate trigger" finding in send_settlers.txt definitely a
  bug?** Not confirmed — flagged as a candidate, not asserted as fact,
  specifically because this session's standing rule is to treat
  suspected authoring mistakes with the same differential-proof
  discipline as suspected Sobisonator bugs. Needs a check against
  sibling options before any edit.
- **Did this investigation touch any script file?** No — read-only.
  Only this design doc was written.

## Independent adversarial review (2026-08-28)

A separate reviewer re-checked every citation and claim against current
source, trying to refute rather than confirm. Result: **the core thesis
survives** (both display triggers are independent scalar reads of
different transforms of overlapping inputs; the duplicate-trigger and
multiplicative-`ai_chance` findings both hold). Issues found and folded
into this doc above:
- The original root-cause section had the cost terms' sign backwards
  (they subtract, not add) and overstated how common the contradiction
  configuration is — corrected in "Root cause" above with the actual
  civilization_value/core-overlap coupling that governs it.
- An arithmetic error (2,430,000 → corrected to 2,700,000) — fixed in
  the pipeline section above.
- Minor citation drift (trigger line ranges off by 1-2; the stability
  cost citation started 1 line past the cited range; call-site count
  was 15, actually 16) — corrected inline above.
- The multiplicative-`ai_chance` claim was asserted without an in-repo
  citation — now flagged as an engine-behavior assertion rather than a
  proven-from-this-codebase fact.
- Flagged a real tension between recommendation (b)'s "low-risk
  default" framing and this doc's own behavior-authoritative finding —
  folded into the proposed-fix section above, including a previously
  unconsidered middle option between (a) and (b).
