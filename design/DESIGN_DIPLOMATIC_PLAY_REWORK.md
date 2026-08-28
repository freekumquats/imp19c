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
  manpower-reserve term: `manpower × (0.2 + military_tech × 0.02)` — i.e.
  manpower matters, scaled up by military tech. [fix, review-flagged: the
  first draft had a spurious extra `× 0.2` in this paraphrase.]
- The CURRENT `war_assessment` formula already walks this specific play's
  supporters via `every_in_list { variable = play_observers_support_target /
  play_observers_support_instigator }` (`se_AI.txt:1391-1410`, corrected from
  an earlier "~1375-1395" citation) — but only
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
    add   = treasury   # UNCAPPED, no min/max/multiply -- confirmed by user
                        # decision after the parity-case tension was raised
                        # (see "RESOLVED by user decision" below this block).
}
var:play_target_country = {
    add = { value = has_war_exhaustion  multiply = 60  max = 100000 }
    subtract = stability
}
# truce veto unchanged from the current formula (subtract 100000 if a truce exists).
# [fix, review-flagged] the CURRENT formula's observer-support tail
# (se_AI.txt:1391-1410, every_in_list over play_observers_support_target/
# _instigator, subtracting THIS.DIPLOMACY_power x 0.01/0.005) is REMOVED, not
# kept -- it double-counted the same supporters the PRIMARY block above now
# folds in directly (with real military weight, not a generic power
# fraction), and with the OPPOSITE sign for the instigator's own supporters
# (added as strength above vs. subtracted as a cost in the old tail). Keeping
# both was a genuine bug in the first draft of this section, not a real
# design choice -- the primary block's supporter-inclusion replaces this
# tail entirely.
```

**Flaw found on re-review — RESOLVED by user decision (2026-08-28): leave
treasury literally uncapped, no coefficient.** "Military strength is
primary" and "treasury is secondary but uncapped" are in tension at military
parity (instigator strength ≈ target strength): the primary block's
difference collapses toward 0 regardless of its weight, leaving an
unbounded treasury term to decide `war_assessment`'s sign alone — the same
shape as the "any evenly-matched solvent instigator reads war-willing"
symptom this doc's root-cause section (and the sibling
`DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md`) diagnosed as the original bug. A
`× 0.02`-style coefficient was proposed as a middle ground (in the spirit of
`AI_svalues.txt:2069`'s own treasury-scaling idiom) but explicitly declined
— the user's call is that an extremely wealthy country tipping a close
military parity case is acceptable, intentional behavior, not a bug to
guard against. Implement `add = treasury` with no `min`/`max`/`multiply`,
exactly as originally directed.

**What happens to the attitude term:** the directive's factor list (military
strength, war exhaustion, treasury, stability) does not mention attitude.
Judgment call, flagged for confirmation: **removing `AI_play_attitude` from
`war_assessment` entirely**, rather than keeping it as a demoted secondary
term. This is not just an omission — it resolves the SHARED-INPUT-DILUTION
half of task #15's contradiction (the treasury-parity tension noted above
in the military-strength section was a SEPARATE half of the same original
bug, not covered by removing attitude — now resolved by user decision:
uncapped treasury at parity is accepted as intentional, not a bug):
`war_assessment`
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

## USER DIRECTIVE (2026-08-28): AI_play_attitude rearchitected around relations

Same pattern, second target. Current `AI_diplomatic_play_evaluate_attitude`
(`se_AI.txt:1233-1295`) computes `AI_play_attitude` = `AI_friendly` (culture
match +50, religion match +50) minus `AI_hostile` (power-balance ratio +
ideological distance×10 + core-province-claim overlap×20). **There is no
`opinion` term anywhere in this formula** — an "attitude" score with zero
input from the actual bilateral relationship history is exactly the kind of
bizarre gap task #16 exists to fix. Directive: relations (opinion) becomes
the **PRIMARY** term; diplomatic reputation and aggressive expansion are
added as further primary-tier inputs; the existing culture/religion/
ideology/power/core-claims terms are **confirmed to remain real, just
demoted to secondary** (same principle as the war_assessment rework above).

**Proven building blocks:**
- `opinion = { target = X  value > N }` is a proven TRIGGER (boolean
  threshold), used 6x in this codebase (`AI_svalues.txt:1723-1857`) — but
  there is no proven way to read opinion as a raw numeric value inside a
  script_value sum (checked this mod and both oracles — none found). This
  looks like a genuine engine limitation (opinion is trigger-only), not a
  mod gap. Same class of unprovable-from-script primitive as
  `num_goods_produced` ([[imp19c-num-goods-produced-engine-internal]]).
- Workaround: this mod's OWN `AI_svalues.txt:1723-1735` already builds a
  numeric proxy from layered opinion thresholds (`if opinion>30 / else_if
  opinion<0 / else_if opinion<-50`, applied as multipliers there). Reused
  below as ADD amounts instead, to turn the boolean primitive into a banded
  numeric contribution — the same proven idiom, different arithmetic role.
- `has_aggressive_expansion` is proven as a bare numeric value inside a sum
  (`WARSCORE_svalues.txt:96`, `subtract = has_aggressive_expansion`).
- `diplomatic_reputation` is a real country stat (used mod-wide as a
  MODIFIER key, e.g. `qing_governance_modifiers.txt`) — by the same pattern
  as `stability`/`tyranny`/`legitimacy` (all proven usable bare in a sum
  elsewhere in this exact formula family), it should be usable bare too,
  though this specific stat's bare-value use is not independently confirmed
  in this codebase — flag for a differential check before relying on it,
  same discipline as any other unconfirmed-but-analogous primitive.

**Proposed new formula shape** ([fix, review-flagged] `opinion = {}` is a
country-to-country trigger, and this whole formula runs in
`scope:diplomatic_play`, a PROVINCE scope (`se_AI.txt:1243`, confirmed by
reading the current live formula) — bare `opinion = {}` here would not
resolve. Every opinion check below is now wrapped in
`var:play_instigator = { opinion = {...} }`, matching how the rest of this
same formula already reaches country scope, e.g. `var:play_target_country.religion`):
```
set_local_variable = {
    name = AI_friendly
    value = {
        value = 0
        # PRIMARY -- relations (opinion of instigator toward target),
        # banded proxy using this codebase's own proven if/else_if-on-opinion
        # STRUCTURE (AI_svalues.txt:1723-1735 uses >30/<0/<-50 as multiplier
        # tiers) -- the THRESHOLDS and ADD magnitudes below are this
        # section's own first guess, not the cited bands verbatim; only the
        # if/else_if-on-opinion shape is reused, not those exact numbers.
        var:play_instigator = {
            if      = { limit = { opinion = { target = var:play_target_country  value > 100 } }  add = 80 }
            else_if = { limit = { opinion = { target = var:play_target_country  value > 30  } }  add = 50 }
            else_if = { limit = { opinion = { target = var:play_target_country  value > 0   } }  add = 20 }
        }
        # PRIMARY -- diplomatic reputation (instigator's own standing).
        add = { value = var:play_instigator.diplomatic_reputation  multiply = 2 }
        # SECONDARY -- existing terms, still real, demoted:
        if = { limit = { var:play_target_country.religion = var:play_instigator.religion }  add = 50 }
        if = { limit = { var:play_target_country.culture  = var:play_instigator.culture  }  add = 50 }
    }
}
set_local_variable = {
    name = AI_hostile
    value = {
        value = 0
        # PRIMARY -- relations, hostile side of the same banded proxy.
        var:play_instigator = {
            if      = { limit = { opinion = { target = var:play_target_country  value < -100 } }  add = 80 }
            else_if = { limit = { opinion = { target = var:play_target_country  value < -30  } }  add = 50 }
            else_if = { limit = { opinion = { target = var:play_target_country  value < 0    } }  add = 20 }
        }
        # PRIMARY -- aggressive expansion (instigator's own AE makes it
        # MORE willing to act hostile -- consistent with AE already being
        # a "spent, might as well keep spending" infamy-adjacent signal
        # elsewhere in this mod's AI logic; bare-value proof is
        # WARSCORE_svalues.txt:96, `subtract = has_aggressive_expansion` --
        # corrected from an earlier, wrong self-citation to AI_svalues.txt:96).
        add = { value = var:play_instigator.has_aggressive_expansion  multiply = 0.5 }
        # SECONDARY -- existing terms, still real, demoted:
        add = { value = var:AI_play_power_balance_instigator_root }
        add = {
            value = var:play_instigator.SPIRIT_traditionalism
            subtract = var:play_target_country.SPIRIT_traditionalism
            multiply = 10
        }
        var:play_target_area.area = {
            every_area_province = {
                limit = { is_core_of = var:play_instigator }
                add = 20
            }
        }
    }
}
set_variable = { name = AI_play_attitude  value = { add = local_var:AI_friendly  subtract = local_var:AI_hostile } }
```

**Judgment calls flagged for confirmation** (band thresholds/weights and
whose stats to read):
- Opinion bands (>100/>30/>0 and <-100/<-30/<0, magnitudes 80/50/20) are a
  first guess at "primary-tier" scale, matching the war_assessment section's
  own admission that dominant-term weighting needs a boot to confirm, not a
  derived number.
- Read as the INSTIGATOR's opinion of the TARGET (not the reverse) and the
  INSTIGATOR's own diplomatic_reputation/aggressive_expansion (not the
  target's) — matches the existing formula's convention that AI_hostile's
  ideology and core-claims terms are already about the instigator's own
  situation. Flag if the target's reputation/AE should matter instead or as
  well.

## USER DIRECTIVE (2026-08-28): war/back-down consequences scaled by attitude

A third directive, changing what attitude actually DOES in the reworked
system. It is not a term inside `war_assessment` or a display-only signal —
it sets the CONSEQUENCE of the choice the player/AI makes once war is
already assessed as likely:
- **Declaring war** costs stability + aggressive expansion. That cost is
  **higher against a friendly target** (betraying goodwill is more costly
  than attacking a rival you were already hostile toward).
- **Backing down** costs legitimacy. That cost is **higher against a
  hostile target** (caving to a rival you were already at odds with is a
  bigger loss of face than standing down from a friend, where it reads as
  restraint rather than weakness).

**Current state (confirmed by reading every Declare-war/Back-down option
across all three event files):** costs are inconsistent, and mostly but not
entirely absent. `diplomatic_play.4.b` (Declare war: `add_political_influence
= -5`, `add_aggressive_expansion = 5`) and `diplomatic_play.4.a` /
`send_settlers.3.a` (Back down: `add_stability = -1/-2`, `send_settlers.3.a`
also `add_political_influence = -2`, `add_aggressive_expansion = -1`) carry
a cost. `agadir_crisis_type.6.a`/`.7.a` (Declare war) genuinely carry none.
**Correction: `agadir_crisis_type.6.b` (Back down) is NOT cost-free** — the
first draft of this doc claimed it was, which the adversarial review
disproved by reading the actual option body: it carries `add_stability = -5`,
`add_political_influence = -25`, and `POLITICS_upset_militarists = { level =
major }` — one of the LARGEST existing costs in any of these options, not
the smallest. None of the existing costs are attitude-scaled.

**This changes the "replaces each event's own ad-hoc costs" plan below**:
naively swapping `agadir_crisis_type.6.b`'s body for the shared
`DIPLOMACY_play_back_down_cost` effect (legitimacy -3, or -7 vs. a hostile
target) would silently delete a `-25` political-influence penalty and a
`POLITICS_upset_militarists` effect this doc never accounted for — a real
regression, not a wash. `agadir_crisis_type.6.b`'s existing cost should be
KEPT alongside the new shared legitimacy cost, not replaced by it, unless a
follow-up confirms the militarist-upset effect is meant to be superseded
too.

**Proposed shared effects** (one pair, called from every event's
Declare-war/Back-down option, instead of duplicating per-event — matches
this mod's own convention of shared `DIPLOMACY_*`/`QING_*` effects called
from many events rather than copy-pasted logic):
```
DIPLOMACY_play_declare_war_cost = {
    # Scope: diplomatic_play. Call from every "Declare war" option.
    var:play_instigator = {
        add_stability = -1
        add_aggressive_expansion = 3
        if = {
            limit = { DIPLOMACY_play_attitude_friendly_trigger = yes }
            add_stability = -2       # additional penalty, on top of the -1 above
            add_aggressive_expansion = 3   # additional penalty, on top of the 3 above
        }
        else_if = {
            limit = { DIPLOMACY_play_attitude_hostile_trigger = yes }
            # no additional penalty -- attacking an already-hostile rival
            # costs nothing beyond the baseline.
        }
    }
}

DIPLOMACY_play_back_down_cost = {
    # Scope: diplomatic_play. Call from every "Back down" option.
    var:play_instigator = {
        add_legitimacy = -3
        if = {
            limit = { DIPLOMACY_play_attitude_hostile_trigger = yes }
            add_legitimacy = -4      # additional penalty, on top of the -3 above
        }
        else_if = {
            limit = { DIPLOMACY_play_attitude_friendly_trigger = yes }
            # no additional penalty -- standing down from a friend reads as
            # restraint, not a loss of face.
        }
    }
}
```
Both reuse the already-proven `add_stability`/`add_aggressive_expansion`/
`add_legitimacy` idioms (all confirmed usable with literal negative values
elsewhere this session — tasks #4/#10/#11) and the already-proven
`DIPLOMACY_play_attitude_friendly_trigger`/`_hostile_trigger` booleans (no
new primitives needed here, unlike the opinion-as-value gap above).

**Judgment calls flagged for confirmation:**
- Baseline magnitudes (stability -1, AE +3 for declaring war; legitimacy -3
  for backing down) and the size of the attitude-scaled surcharge (stability
  -2, AE +3, legitimacy -4) are first guesses, not derived — same tunable-
  magnitude caveat as every other number in this doc.
- This REPLACES each event's own ad-hoc costs (where any exist) rather than
  stacking on top of them — e.g. `diplomatic_play.4.b`'s existing
  `add_aggressive_expansion = 5` and `send_settlers.3.a`'s existing
  `add_stability = -1` would be removed in favor of calling the shared
  effect, not left in place alongside it. **Exception, review-flagged:**
  `agadir_crisis_type.6.b`'s existing cost (`add_stability = -5`,
  `add_political_influence = -25`, `POLITICS_upset_militarists`) is
  substantially larger than anything this replace-all rule was designed
  for and was wrongly believed not to exist when this rule was written —
  KEEP it alongside the new shared cost rather than deleting it, pending
  confirmation. Flag if any OTHER event's existing cost was similarly a
  deliberate, event-specific number that should survive as an addition
  rather than being replaced.
- `send_settlers.1.b`'s existing `add_tyranny = 1` (a "Forbid and arrest
  settlers" option, not a literal Declare-war/Back-down) is NOT touched by
  this directive as written — it's a different kind of choice (refuse a
  request, not fight-or-yield). Flag if it should be folded into this same
  pattern.

## USER DIRECTIVE (2026-08-28): the "war unlikely" branch

When war is assessed as unlikely, the instigator gets a choice between
**completing the play** (achieve the play's goal without war) or **aborting
the play** (give up the demand entirely). Attitude sets a diplomatic-
relations + reputation penalty, **higher against unfriendly countries**.

**Current state:** as documented above under "war unlikely," no such choice
exists today — `war_not_willing_trigger` is only ever an `ai_chance` booster
on an event's existing "Back down"-shaped option; there is no distinct
"complete the play peacefully" option anywhere, and no relations/reputation
cost tied to this branch at all.

**Proven building block for relations/reputation:** `add_opinion = { modifier
= X  target = Y }` (proven, e.g. `send_settlers.1.a` →
`add_opinion = { modifier = hindered_in_play  target = ... }`,
`agitator_sponsorship.txt:334-337`). This mod's own `common/opinions/
imp19c_opinions.txt` already defines exactly the right pair of magnitudes for
this: `hindered_in_play` (`value = -10`, `common/opinions/
imp19c_opinions.txt:31-34`) and `betrayed_in_play` (`value = -100`, `:36-39`)
— a mild vs. severe opinion hit, already built for "a diplomatic play did
something to this country." No new opinion key needed.

`add_diplomatic_reputation` was NOT found as a proven effect in this mod or
either oracle — flagged as unconfirmed, same caution as `diplomatic_reputation`'s
bare-value read above. May need a temporary `add_country_modifier` granting a
`diplomatic_reputation` modifier instead of a direct effect, if no direct
effect exists in this engine version — needs a differential check before
implementing.

**Proposed shared effect:**
```
DIPLOMACY_play_complete_peacefully_cost = {
    # Scope: diplomatic_play. Call from every "Complete the play" option.
    add_opinion = { modifier = hindered_in_play  target = var:play_target_country }
    if = {
        limit = { DIPLOMACY_play_attitude_hostile_trigger = yes }
        add_opinion = { modifier = betrayed_in_play  target = var:play_target_country }
    }
    # add_diplomatic_reputation -- UNCONFIRMED effect, needs a check before use.
}
```

**Judgment call flagged for confirmation:** the directive names one penalty
(relations + reputation) without saying which of the two options it attaches
to. Assumed here: **completing the play** carries the cost (it's the action
that actually imposes an outcome on the target, parallel to how "declare
war" carries the attitude-scaled cost in the war-likely branch), while
**aborting the play** carries no new cost (parallel to "back down" being the
zero-surcharge default against a friendly target). Flag if this is backwards,
or if "abort the play" should instead get its own scaled cost (e.g.
legitimacy, mirroring the war-likely branch's back-down cost).

## USER DIRECTIVE (2026-08-28): the "war undecided" branch borrows the other two

When war is undecided, there is no third choice-structure. Attitude decides
which of the other two branches' choice-pair the instigator is given:
- **Friendly** → the war-unlikely branch's choice (complete the play /
  abort the play).
- **Unfriendly (hostile)** → the war-likely branch's choice (declare war /
  back down).

This means the real decision tree has only two distinct SHAPES of choice,
not three — "undecided" is resolved entirely by attitude rather than getting
its own UI/options. Reuses the already-proven `DIPLOMACY_play_attitude_
friendly_trigger`/`_hostile_trigger` to pick the branch; no new primitive.

**Resolved by a further directive — the neutral case gets its own third
choice, not a default branch:** when war AND attitude are both undecided,
the instigator gets to spend treasury + political influence to try to tip
attitude into the friendly bucket (or decline and let it stand).

**Proposed shared effect:**
```
DIPLOMACY_play_court_favour_option = {
    # Scope: diplomatic_play. Offered only when BOTH war_considering_trigger
    # and attitude_neutral_trigger are true.
    var:play_instigator = {
        add_treasury = -200
        add_political_influence = -10
    }
    add_opinion = { modifier = helped_in_play  target = var:play_target_country }
    # helped_in_play (value = 10, common/opinions/imp19c_opinions.txt:21-24)
    # is the proven, already-defined "a diplomatic play went well" bump --
    # reused rather than inventing a new opinion key. Whether +10 opinion is
    # ENOUGH to actually cross AI_play_attitude into the friendly band
    # depends on the banded thresholds proposed in the AI_play_attitude
    # section above (>30/>0 etc.) and the target's starting opinion -- not
    # guaranteed to succeed, which is consistent with "tip the scales," not
    # "force the outcome."
}
```

**Judgment calls flagged for confirmation:**
- Cost (200 treasury, 10 political influence) is a first guess, not derived
  — same tunable-magnitude caveat as every other number in this doc.
- Whether declining this option should have any consequence of its own
  (e.g. does the play simply stay in the neutral/undecided state
  indefinitely, re-offering this choice next quarter when
  `AI_diplomatic_play_evaluate_attitude` re-runs, or does it eventually
  force a default branch after some time limit) is unresolved — flagging
  rather than assuming a specific fallback.
- This only resolves the war-undecided × attitude-neutral cell. The other
  three "undecided" combinations (war-undecided × friendly, war-undecided ×
  hostile) are already covered by the branch-borrowing rule above; war-likely
  × neutral and war-unlikely × neutral are covered by their respective
  branches already (attitude only changes the SURCHARGE in those cases, per
  the earlier two directives — neutral attitude there means baseline cost,
  no special new option).

## USER DIRECTIVE (2026-08-28): nine discrete events, not one shared/dynamic effect

3 war buckets × 3 attitude buckets = 9 permutations, and each gets its OWN
event with its own localization, following this mod's existing quantified-
tooltip template (own-line `#COLOR Name: sign N#!`, per tasks #4/#5/#8) —
not one shared effect with a live if/else surcharge computed at trigger
time. This means every cost below is now a STATIC number baked into that
one event's tooltip — no conditional text, no "if attitude is X" branching
inside the tooltip itself, because each event only ever fires under its own
exact war×attitude combination.

Proposed namespace: `diplomatic_play_outcome`, events `.1`-`.9`, one per row:

| # | War bucket | Attitude bucket | Choice pair | Option A cost | Option B cost |
|---|---|---|---|---|---|
| 1 | Likely | Friendly | Declare war / Back down | Declare: Stability −3, AE +6 | Back down: Legitimacy −3 |
| 2 | Likely | Neutral | Declare war / Back down | Declare: Stability −1, AE +3 | Back down: Legitimacy −3 |
| 3 | Likely | Hostile | Declare war / Back down | Declare: Stability −1, AE +3 | Back down: Legitimacy −7 |
| 4 | Unlikely | Friendly | Complete play / Abort play | Complete: Opinion −10 (hindered_in_play) | Abort: no cost |
| 5 | Unlikely | Neutral | Complete play / Abort play | Complete: Opinion −10 (hindered_in_play) | Abort: no cost |
| 6 | Unlikely | Hostile | Complete play / Abort play | Complete: Opinion −110 (hindered_in_play + betrayed_in_play) | Abort: no cost |
| 7 | Undecided | Friendly | Complete play / Abort play (borrows row 4's costs) | Complete: Opinion −10 | Abort: no cost |
| 8 | Undecided | Neutral | Court favour / Do nothing | Favour: Treasury −200, PI −10, Opinion +10 (helped_in_play) | Do nothing: no cost |
| 9 | Undecided | Hostile | Declare war / Back down (borrows row 3's costs) | Declare: Stability −1, AE +3 | Back down: Legitimacy −7 |

Rows 1-3 and 4-6 derive directly from the two earlier attitude-scaled-
consequence directives, now made static per-permutation instead of
conditional. Row 7 and row 9 are literally rows 4 and 3 respectively, under
a different trigger condition and their own event id/title/desc — the
CHOICE and COSTS are identical, only the framing text differs (since the
underlying situation, war undecided vs. war unlikely/likely, is genuinely
different even when the mechanical outcome is the same). Row 8 is the new
court-favour event from the directive immediately above.

**What this replaces:** the `DIPLOMACY_play_declare_war_cost` /
`DIPLOMACY_play_back_down_cost` / `DIPLOMACY_play_complete_peacefully_cost`
shared effects proposed earlier (with `if = { limit = {
DIPLOMACY_play_attitude_*_trigger = yes } }` surcharge logic) are now
UNNECESSARY as shared/dynamic effects — each of the 9 events simply writes
its own fixed numbers directly, no trigger-time branching needed. The
shared-effect versions above are superseded by this table, not run alongside
it.

**Judgment calls flagged for confirmation:**
- Each event still needs to be written against ONE of the existing three
  event files' structure (`diplomatic_play_events.txt` pattern, `send_
  settlers.txt` pattern, or `agadir_crisis_type.txt` pattern) or a NEW
  dedicated file — not decided yet. Given this is a generic outcome (not
  colonial-expedition-specific like `send_settlers` or crisis-specific like
  `agadir_crisis_type`), a new file (`diplomatic_play_outcome_events.txt`)
  is the more consistent choice, but flagging rather than deciding
  unilaterally.
- This 9-event structure does not by itself replace the CALL SITES that
  currently trigger `diplomatic_play.4`/`.7`, `send_settlers.3`,
  `agadir_crisis_type.2`/`.6` — those trigger_event calls would need
  repointing to pick one of the 9 new events based on the live war/attitude
  bucket at that moment, which is a real code change beyond this design doc,
  not just new event text.

## USER DIRECTIVE (2026-08-28): AI behavior for rows 1-3/9 and 4-6/7

**Declare-war rows (1, 2, 3, 9):** the AI picks war when it thinks it will
win, backs down otherwise. Since `war_assessment` is now primarily military
strength (per the rearchitecture above), this is no longer "a grab-bag of
~6 loosely-related `ai_chance` modifiers plus one `×100` boolean" (the
current implementation in every Declare-war option checked earlier) — the
AI's choice should track `war_assessment`'s own sign/magnitude directly,
continuously, not as one more boolean tier among several.

**Proven capability check — CORRECTED after adversarial review:** the first
draft of this section claimed a continuous `factor = { value = ... }` block
was "proven possible," citing Invictus `common/buildings/00_default.txt:55`
and `senate_objectives_roman_events.txt:771`. Both citations were WRONG:
the first is inside a `chance = {}` block (building appearance odds), the
second inside a `weight = {}` block (random-character selection) — neither
is an `ai_chance` block. An exhaustive brace-matched scan of every
`ai_chance = {}` block in both oracles (1,971 in Invictus, 1,298 in
Terra-Indomita) found `factor =` is a **plain numeric literal in 100% of
cases** — zero bare script_value references, zero nested blocks. This
construct is UNPROVEN for `ai_chance` specifically, and the available
evidence leans against it parsing there at all. Retracting the "proven
possible" claim entirely.

**Corrected approach — reuse the proven if/else_if literal-factor tier
pattern instead** (the same shape already used for the opinion bands
elsewhere in this doc, and for the existing Declare-war/Back-down options'
own `×5`/`×10`/`×50`/`×100` tiers today): approximate continuous scaling
with several discrete, literal-factor tiers keyed on `war_assessment`'s
magnitude, rather than one continuous expression:
```
ai_chance = {
    modifier = { factor = 1 }
    modifier = { factor = 10   scope:diplomatic_play = { var:war_assessment > 0    } }
    modifier = { factor = 50   scope:diplomatic_play = { var:war_assessment > 200  } }
    modifier = { factor = 200  scope:diplomatic_play = { var:war_assessment > 500  } }
    modifier = { factor = 1000 scope:diplomatic_play = { var:war_assessment > 1000 } }
}
```
(mirrored, inverse tiers on Back down, keyed on how negative
`war_assessment` is). This is entirely literal-factor, matching 100% of the
proven `ai_chance` corpus in both oracles — no unproven construct needed.
Note: the lowest tier here (`war_assessment > 0`) can fire on treasury-driven
positivity at military parity, not genuine military confidence — this is the
accepted, intentional consequence of the resolved treasury-parity decision
above (uncapped treasury, no coefficient), not a defect in this tier ladder.
[fix, review-flagged: also corrected the scope path — `scope:diplomatic_play
= { var:war_assessment > N }` matches the proven wrapper form used by every
existing reader (e.g. `send_settlers.txt:135-137`); the first draft's
unwrapped `scope:diplomatic_play.var:war_assessment` chain was not the
proven form.] The tier boundaries are a first guess, same tunable-magnitude
caveat as the rest of this doc — needs a boot to see what `war_assessment`'s
real range looks like once military strength dominates it, then re-tune the
tier cutoffs to match.

This replaces the current pattern's `×100` willing/not-willing boolean plus
the ~6 secondary `×5`-tier modifiers (opinion, minister martial, raw
power-balance thresholds) — those secondary factors were already flagged
as "demoted to secondary" for the SCORE itself above; this extends the same
demotion to how the AI WEIGHS its own choice, not just what the number
means.

**Unlikely rows (4, 5, 6, 7): the AI should complete the play, not abort
it.** Default AI behavior for this branch is Complete, not a 50/50 or
opinion-driven toss-up — matches the intuition that giving up on a demand
you were never going to fight for anyway should be the exception, not the
default.

**Judgment calls flagged for confirmation:**
- The tier boundaries and factor values in the corrected if/else_if approach
  above are first guesses — same tunable-magnitude caveat as every other
  number in this doc. Needs a boot to confirm the resulting war frequency
  feels right once military strength actually dominates the underlying
  score, then a re-tune of the cutoffs.
- "The AI should complete the play" for rows 4-7 — proposed as a strong
  `ai_chance` weight favoring Complete (e.g. `factor = 10` vs `factor = 1`
  on Abort), not an unconditional/`ai_will_do`-style guarantee, so a
  genuinely bad situation (e.g. the target has crushing observer support)
  can still tip an individual case toward Abort. Flag if "should complete
  the play" was meant as a hard rule instead of a strong default.

## USER DIRECTIVE (2026-08-28): success/failure feeds the Great Game sphere system — CORRECTED, larger lift than first scoped

Scoped, not universal: **only** when a Great Power is involved and the
target is in one of the sphere system's designated contested regions.
Successful plays raise the instigator's sphere influence there; failed
plays lower it. When BOTH instigator and target are Great Powers, the
effect is doubled.

**The first draft of this section was architecturally wrong, not just
missing a scope-bridge detail — adversarial review caught this. Corrected
facts, from actually reading `se_QING_SPHERE.txt` end to end this time:**

1. **`qing_sphere_states` is a variable list OWNED BY CHI, not a free-
   floating list checkable from any scope.** `QING_sphere_build_ring`
   (`:99-159`) opens with `save_scope_as = sphere_owner` on whatever scope
   called it (CHI, in every existing call site), and every add is
   `scope:sphere_owner = { add_to_variable_list = { name = qing_sphere_states
   ... } }`. The first draft's `is_target_in_variable_list = { name =
   qing_sphere_states  target = var:play_target_area }`, run bare inside
   `scope:diplomatic_play`, checks a list that does not exist on that scope
   — it needs to run on CHI's own scope specifically, not a generic
   country/play scope.
2. **There is no instigator-tag → `$power$` mapping anywhere in this
   system, and it is not a missing detail — it's a different model
   entirely.** Power identity is assigned by GEOGRAPHY of the STATE, not by
   who is acting: `QING_gp_sphere_is_france` (`imp19c_diplomacy_triggers.txt:86`),
   `QING_gp_sphere_is_britain` (`:106`), `QING_gp_sphere_is_russia` (`:133`)
   [fix, re-review-flagged: name↔line pairing was swapped for Britain/France
   in the prior pass] are pure `is_in_region` checks (Southeast
   Asia/Indochina for France, Burma/British-India for Britain, Central
   Asia/Siberia/Far East for Russia), and `QING_sphere_gp_push`
   is always called with a hardcoded literal (`power = britain`, `:499-500`;
   `power = france`, `:503-504`; `power = russia`, `:507-508`) gated on that
   state's geography, not on any country's tag. This system models "which
   power's historical sphere does this region sit in," passively, over
   time — it has no concept of "an instigator's own tracked influence" to
   hook a diplomatic play's outcome into.
3. **The subsystem's own header comment says CHI-player-only** (`:55`,
   read for this correction). Generalizing it to "any Great Power
   instigator" is a materially bigger change than adding one effect call —
   it means teaching the system a second kind of actor it was never
   designed to represent.

**What IS still proven and reusable:**
- The 4 influence variables, their clamp range, and the
  `change_variable = { name = $power$_influence  add/subtract = N }`
  adjustment idiom (`:209-219`, `:456-459`, `:536-547` — corrected citation,
  the `$power$` macro itself lives in `QING_sphere_gp_push`, not the flat
  decay lines).
- `rank = great_power` (`se_SUCCESSION.txt:70/80`, `se_MARRIAGE.txt:234-235`).

**Revised, honest proposal — reusing the GEOGRAPHY-based power identity
instead of inventing an instigator-tag mapping:**
```
DIPLOMACY_play_sphere_outcome_success = {
    # Scope: diplomatic_play. Call ONLY from an outcome that is
    # unambiguously a success (Complete-the-play resolving; a war's actual
    # end via victory -- see the mapping gap flagged below, this is NOT the
    # same moment as the 9 outcome events firing). Split success/failure
    # into two separately-named effects instead of one with a $result$
    # macro parameter compared via trigger -- `limit = { $result$ = success }`
    # is not a valid trigger shape (a macro param expands to a literal
    # token, not something comparable with `=` against another literal).
    var:play_target_area = {
        # GEOGRAPHY, not instigator identity, decides which power's
        # influence this state's outcome affects -- matches how this
        # subsystem already assigns power identity everywhere else.
        if      = { limit = { any_area_province = { QING_gp_sphere_is_britain = yes } } }  # power = britain
        else_if = { limit = { any_area_province = { QING_gp_sphere_is_france  = yes } } }  # power = france
        else_if = { limit = { any_area_province = { QING_gp_sphere_is_russia  = yes } } }  # power = russia
        else    = { }                                                                       # power = china (default)
    }
    # NOTE: this pseudo-code cannot actually branch a bare $power$ macro
    # value at runtime from an if/else_if -- Jomini macros are textual
    # substitution at PARSE time, not a runtime variable. The real
    # implementation needs 4 separate concrete effect bodies (one per
    # power, each with change_variable hardcoded to that power's own
    # _influence key), called from 4 parallel if/else_if branches, mirroring
    # how QING_sphere_gp_push itself is called 3 times with 3 literal
    # `power=` values rather than a single parameterized call driven by a
    # runtime branch. This is GENUINELY NEW structure, not a reuse of an
    # existing multi-branch caller -- flagging plainly rather than
    # dressing it up as proven.
}
```

**This directive is NOT fully closed by this design doc.** Two real gaps
remain that need a decision, not a guess:
- **Whether CHI should even be a "great power" in this system's own terms**
  for the purposes of raising `china_influence` on ITS OWN successful
  plays — the sphere system already treats China as the default/home power
  (the "else" case above), so a CHI success might mean "raise
  china_influence" OR "lower whichever of Britain/France/Russia currently
  dominates that region" OR both. The directive says "raise the
  instigator's own influence," which reads cleanly for Britain/France/
  Russia instigators (geography-matched) but is ambiguous for CHI (the
  system's default/home actor, not one it tracks as competing FOR
  influence against itself).
- **The success/failure call-site problem (independent finding, applies
  regardless of the above):** the 9 outcome events (table above) fire at
  the DECISION point, not at resolution. Declare-war rows (1/2/3/9) don't
  know whether the war was WON until it actually ends — a separate, later
  event/effect (the war's peace-deal resolution, not one of the 9). Complete-
  the-play rows (4/5/6/7) DO resolve at the event itself (success = clean).
  Back-down/Abort rows are failures at the event itself (clean). Row 8
  (court favour / do nothing) resolves NEITHER a success nor a failure —
  it should not call this effect at all. So: 4 of 9 rows can call this
  effect directly at their own event; declare-war rows need a hook into
  war-resolution instead, which is outside this design doc's scope (a
  separate investigation into how this mod's war-resolution effects work);
  row 8 is excluded entirely.

**Judgment calls flagged for confirmation:**
- Magnitude (7 per success/failure, doubled to 14 when both sides are Great
  Powers) is anchored to the proven `3/7/11/12` range already used in
  `se_QING_SPHERE.txt` for comparable pushes, not independently derived —
  same tunable caveat as every other number in this doc.
- Doubling is applied by literally repeating the add/subtract line rather
  than a `multiply = 2` on the whole thing, since `change_variable`'s
  `add`/`subtract` fields take literal magnitudes, not a scalable block —
  flag if a cleaner single-call-with-multiplier idiom exists elsewhere in
  this codebase that should be used instead.
- Whether this directive should be pulled out into its own, separate design
  task rather than staying folded into #16 — it touches a CHI-only
  subsystem that was never built to represent other actors, which is a
  bigger and more independent piece of work than everything else in this
  doc. Flagging the option, not deciding it.

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
