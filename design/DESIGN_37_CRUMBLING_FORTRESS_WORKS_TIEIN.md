# DESIGN — #37 tie the Crumbling Fortress event (flavor_eve.8) into the Ministry of Works

> STATUS 2026-08-13: REVIEW ROUND 3 — CLEAN, ready to implement. Round 1 found 2 CRITICAL defects:
> (1) a static `right_portrait = scope:works_minister` field on a generic, all-nations event with no
> `tag = CHI` gate would dangle for every non-Qing firing; (2) the cited `QING_works_build_dike`
> "finesse-discount factor" doesn't exist — that function is a two-way branch between two dike-count-
> scaled script-values, not a reusable multiplier, so the original design gave no real number. Round
> 2's fix dropped the portrait field and derived a real cost number from the dike-cost RATIO, but
> introduced a NEW defect of the same class: its effect bodies acted on `scope:works_minister`, a
> scope this event never saves (it only guards on the VARIABLE `qing_office_works_holder`) — the
> exact dangling-scope failure mode reintroduced one layer down. Round 3 fixes this by acting
> directly on `var:qing_office_works_holder = { ... }` (no scope save at all, matching the real
> `var:qing_office_chamberlain_holder = { add_loyalty = ... }` precedent at
> `qing_household_events.txt:356`), and corrects a false precedent citation (round 2 pointed at
> `qing_works.1.a`/`.3.a`, which contain no `add_loyalty` at all — the real precedent for
> add-loyalty-on-a-named-officeholder is `qing_faction_events.txt`, adapted here to act on the var
> directly instead of a saved scope).

## Task text
Task #37: "Tie Crumbling Fortress event (flavor_eve.8) into the Ministry of Works."

## Diagnosis (per Rule 1c — the existing event, traced before extending it)

`flavor_eve.8` (`events/imp19c_mod_events/FlavorEvents.txt:475-526`) is a generic, upstream-style
country event with **no `tag = CHI` gate anywhere in its trigger** — it fires for any nation with a
fortress and no active cooldown. A random owned province with `num_of_fortress_building >= 1` takes
earthquake damage; the player chooses (a) unaided repair (`-10 state loyalty` + a 2-year
`local_unrest_harsh` province modifier) or (b) a paid repair (`-50 treasury`, `+5 ruler popularity`).
`left_portrait = current_ruler` only; no `right_portrait` field exists on the base event at all.

**Corrected precedent (round 2): the proven pattern for tying a Qing institution into a SHARED,
ungated event is NOT a static portrait field — it is CHI-gated logic entirely inside the option
body, with a generic fallback for every other nation.** `flavor_eve.7.a`'s own comment states this
explicitly: "for the Qing with a seated Zongli Yamen (總理衙門) director — route the exchange through
a REAL envoy... mirrors the #22 flavor_eve.18 Yamen tie-in" (`FlavorEvents.txt:405-410`), and the
actual code is `if = { limit = { tag = CHI  exists = scope:...  has_variable = qing_office_*_holder
...} ... } else = { <generic fallback> }` inside the OPTION, never a change to the event's own
`left_portrait`/`right_portrait`/`trigger` fields. This design follows that exact shape.

## The fold — CHI-gated option-body logic, generic event body and portraits untouched

No change to `flavor_eve.8`'s `trigger`, `fire_only_once`, `picture`, or portraits. Both options gain
an `if = { limit = { tag = CHI  <Works-seat-filled guard> } ... }` block; every non-CHI nation (and a
CHI game with a vacant Works seat) falls through unchanged to the exact original flat effects.

**Guard (round 2 fix, still correct): use the FULL proven idiom, not a bare `has_variable`.**
Every place in this suite that actually ACTS on `qing_office_works_holder` also checks `is_alive =
yes  employer = ROOT` (`qing_works_events.txt:74,226`; `se_QING_WORKS.txt:175`) — a bare
`has_variable` guard would let a dead or defected ex-minister be loyalty-banded and finesse-read.
```
tag = CHI
has_variable = qing_office_works_holder
var:qing_office_works_holder = { is_alive = yes  employer = ROOT }
```

**No scope is saved — round 3 fix (round 2's own regression).** Round 2 wrote its option-body
effects against `scope:works_minister`, a scope this event never saves anywhere (it only guards on
the VARIABLE `qing_office_works_holder`) — the exact dangling-scope bug round 1 killed in the
portrait field, reappearing one layer down in the effect body. `flavor_eve.8` gets NO `immediate`
scope-save added (that would require touching the event's own `immediate` block, which "What this
does NOT touch" below still refuses, correctly, since a scope-save is unnecessary machinery for a
one-shot loyalty/cost effect). Instead, act DIRECTLY on the variable, matching the proven
no-scope-save idiom `var:qing_office_chamberlain_holder = { add_loyalty = loyalty_qing_delta_p20 }`
(`qing_household_events.txt:356`) and `var:qing_office_crownprince_holder = { add_loyalty = ... }`
(`se_QING_DYNASTY.txt:319,322`):

1. **Option `.a` (unaided repair)**: inside the guard above, `var:qing_office_works_holder = {
   add_loyalty = loyalty_qing_estranged }` (his own office looked weak while a fortress crumbled
   unaided) and `QING_DECLINE_nudge = { var = qing_reform_pressure  amount = 2 }` (the central
   government visibly failed to respond to frontier infrastructure decay). Both fire ONLY when a
   living, employed Works Minister exists — see "corrected semantics" below for why this is right,
   not backwards.
2. **Option `.b` (paid repair)**: inside the SAME guard, scale the treasury cost by the Works
   Minister's own finesse, using a REAL number derived from this suite's own proven dike-cost ratio
   (see "the actual cost number" below). Add `var:qing_office_works_holder = { add_loyalty =
   loyalty_qing_commended }` (credited for a well-funded repair under his watch) — mirroring the
   SHAPE of `qing_faction_events.txt`'s `scope:X = { add_loyalty = loyalty_qing_commended }` pattern
   (:75,89,236-237), adapted here to act on the variable directly since no scope is saved.

## The actual cost number (round 2 fix — round 1 gave none)

Round 1 claimed `QING_works_build_dike`'s cost carries a reusable "finesse-discount factor." It does
not — `QING_dike_cost_expert_svalue`/`_standard_svalue` (`QING_governance_svalues.txt:410-423`) are
both `QING_dike_count × 40 + <175|220>`, clamped `[175,700]`/`[220,760]` — a dike-COUNT-scaled cost
with no standalone multiplier. But the RATIO between the two tiers' base terms (`175` vs `220`) is a
real, proven number this suite already uses to express "an able Works Minister gets the job done for
~20% less" (`175/220 ≈ 0.795`). Apply that SAME ratio to the flat `-50` base, rather than inventing an
unrelated new constant:
```
if = {
    limit = { var:qing_office_works_holder = { finesse >= 9 } }
    add_treasury = -40   # round(50 x 0.795) — the expert-tier discount, same ratio as the dike cost
}
else = {
    add_treasury = -50   # standard tier, byte-identical to the original flat cost
}
```
The `finesse >= 9` threshold matches `QING_works_build_dike`'s own expert-tier cutoff exactly
(`se_QING_WORKS.txt:194`), so this is genuinely the SAME idiom transplanted with a derived, not
invented, number — not the empty "reuse by reference" round 1 asserted. OVERNIGHT ASSUMPTION on the
exact discount amount (the -40 vs -50 split); boot-tune if it reads as too small to matter.

## Corrected semantics (round 2 fix — round 1's "vacant seat pays no penalty" was backwards)

Round 1 gated the reform-pressure malus on a Works Minister EXISTING, which review correctly flagged
as backwards ("a vacant Works seat pays NO neglect penalty — the opposite of the 'central government
failed to respond' narrative"). **Decision (made here, not deferred): keep the malus scoped to a
FILLED seat, but for the OPPOSITE, corrected reason — this is not a "vacant seat should also be
penalized" case.** A vacant Ministry of Works cannot be blamed for a specific minister's neglect; the
reform-pressure term here specifically represents "a NAMED minister was on watch and did nothing,"
not "infrastructure decayed in general" (a different, broader mechanic this design does not build).
Rejected alternative: apply the malus regardless of whether the seat is filled. Not chosen because
that would require a SEPARATE reform-pressure term with no character to attribute it to, which is a
different, larger design (a general "state neglects its infrastructure" mechanic) than what task #37
asks for (tying ONE event into the Works MINISTER specifically). The narrower, minister-attributed
version is what this design builds; the broader one is out of scope, not silently dropped — noted
here explicitly rather than left as an unexamined gap.

## Loc requirement (round 2 fix — round 1 said "none required," review flagged the gap)

Every sibling event that scales a cost by a minister's finesse pairs the option with a
`custom_tooltip` naming the variance (`qing_works.1.a.tt`, `.5.a.tt`). `flavor_eve.8.b` currently has
no tooltip at all. Add one, matching the sibling pattern:
```
flavor_eve.8.b.tt:0 "Spend treasury to fund the repairs. #Y A capable Works Minister gets it done for
less#!."
```
Localized generically (no specific number, since the two-tier cost is a minor flavor detail, matching
how `qing_works.1.a.tt` itself stays generic — "Costs [...GetVariable(...)]" pattern, not literal
numbers baked into static text). Guard the tooltip's OWN visibility the same way the effect is
guarded — `custom_tooltip` on a non-CHI/vacant-seat option renders the SAME string but describes
behavior that doesn't apply; acceptable, since the fallback behavior (flat -50) is still "spend
treasury to fund the repairs," just without the variance — the tooltip's claim ("a capable minister
gets it done for less") is simply inert rather than wrong when no minister exists to read.

## What this does NOT touch

- The event's `trigger`, `fire_only_once`, `picture`, `left_portrait`, or firing cadence — unrelated
  to "tie into the Ministry of Works," which is about the event's own CONSEQUENCES for CHI
  specifically, not when/whether/for-whom it fires. NO `right_portrait` field is added (round 1's
  CRITICAL error) — the event keeps its current single-portrait shape for every nation.
- `QING_works_build_dike`/`_build_canal_depot`/`_build_wall_section`/`_graft_scandal` themselves —
  read by DERIVED RATIO only (the 175/220 tier split), not modified or called.
- Any general "state neglects infrastructure" mechanic independent of a specific minister — see
  "Corrected semantics" above; explicitly out of scope for this design.

## Blast radius
Two files. `events/imp19c_mod_events/FlavorEvents.txt`: one event (`flavor_eve.8`), both of its
existing options — each gains one CHI-gated `if`/`else` block, acting directly on `var:qing_office_
works_holder` (no scope save); the event's own trigger/portraits/picture/fire_only_once are
untouched. `localization/english/flavor_events_l_english.yml`: one new loc key (`flavor_eve.8.b.tt`)
— confirmed the correct file (where `flavor_eve.8.t`/`.desc`/`.a`/`.b` already live, lines 40-43).

## Open questions for review
1. Is the derived `-40` (the 175/220 ratio applied to the flat `-50` base) the right way to size the
   expert-tier discount, or should it instead just mirror the ABSOLUTE dike-tier gap (175 to 220 is a
   45-treasury difference, not a ratio) scaled down for a smaller one-shot repair? This design chose
   the RATIO reading (relative discount) over the absolute-gap reading because the dike costs scale
   with `QING_dike_count` (irrelevant to a single fortress) while the ratio between tiers is the part
   that IS transplantable context-independently — but this is a judgment call, not a proven identity.
2. Should the reform-pressure malus (option `.a`, filled seat) also scale by the minister's finesse
   (a WEAK minister looks worse than a strong one caught off guard), or is a flat `+2` sufficient for
   a one-shot flavor beat? Kept flat for simplicity — not derived from a deeper judgment that scaling
   would be wrong, just not built here.
