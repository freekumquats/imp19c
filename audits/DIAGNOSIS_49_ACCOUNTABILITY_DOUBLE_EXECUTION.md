# DIAGNOSIS #49 — "A Minister Called to Account" (qing_accountability.1) option .b re-strips the
# same defender twice, within one single execution (REVISED — the first draft self-contradicted a
# "preview pass commits gamestate" theory disproven by adversarial review; this is the corrected,
# non-contradictory root cause, confirmed by a focused trace agent + real debug.log corroboration)

## Evidence
Screenshot `20260812180918_1.jpg` (Aug 12 18:09), read directly. The event's built-in "Has happened"
outcome panel shows the full effect chain for option `qing_accountability.1.b` twice, verbatim, back
to back, for the SAME character (Cao Xiulong, ID 25280): loses "Holder of High State Office," loses
`qing_personnel_cultivated_minor`/`_major`, loses `qing_censorate_oversight_minor`/`_major`, loses 4
Loyal Veterans, "Great Qing loses Grand Minister of Rites Appointed," "Great Qing gains Vacant
Ministry," loses 40 Loyalty, loses 15 Popularity — then the entire sequence repeats.

## Root cause (traced step by step, confirmed against a real debug.log line for this exact event)
Option `qing_accountability.1.b` ("Elevate the challenger"):
```
scope:qing_acc_defender = {
    QING_office_vacate_dispatch = yes
    add_loyalty = loyalty_qing_disgraced
    add_popularity = -15
}
scope:qing_acc_challenger = {
    ... -> QING_office_appoint = { office = rites }   # (or whichever office was contested)
    add_loyalty = loyalty_qing_elevated
    QING_char_bind = yes
}
QING_council_recompute = yes
add_political_influence = -15
```
(`events/imp19c_mod_events/qing_accountability_events.txt:80-116`.)

**Step 1 — the first, correct strip.** `QING_office_vacate_dispatch` (`se_QING_COUNCIL.txt:1881-
1926`) branches on the defender's `qing_office_held` flag (here, `rites`) and calls
`QING_office_vacate = { office = rites }` (`:1801-1834`), which correctly strips the defender:
`remove_character_modifier = qing_officeholder`, `qing_personnel_cultivated_minor/major`,
`qing_censorate_oversight_minor/major`, `remove_variable = qing_office_held` (the CHARACTER var,
line 1814), `add_loyal_veterans = -4`, `remove_variable = qing_office_$office$_holder` (the COUNTRY
var, line 1819), then `remove_country_modifier = qing_office_$office$_active`,
`add_country_modifier = qing_office_vacancy_strain`. Both the character-scope and country-scope
tracking vars are correctly cleared here — this function itself is NOT the bug.

**Step 2 — the real gap: the backfill draw is not identity-excluded from re-picking the man who was
JUST vacated.** `QING_office_vacate_dispatch`'s SAME branch immediately also calls
`QING_council_autofill_office = { office = rites  degree = jinshi  autofill_source = backfill
degree_hard = yes }` (`:1892`) — the runtime backfill draw that fills the now-vacant seat. Its
candidate gate excludes by role/marker (`is_ruler`, `is_governor`, `qing_is_harem_consort`,
`qing_officer_marker`, `QING_char_hard_disgraced` = `has_trait = completely_disgraced`,
`qing_pending_trial`, and — critically — `NOT = { QING_char_holds_court_position = yes }`, which
tests `has_variable = qing_office_held` among other markers). But `qing_office_held` was JUST
removed from the defender in Step 1, ONE LINE EARLIER, in the SAME dispatcher. `QING_char_holds_
court_position` (`qing_dynasty_triggers.txt:241-263`) therefore flips to FALSE for the defender the
instant he is vacated — nothing in the backfill's candidate gate excludes "this office's own
just-departed holder" BY IDENTITY. A minister deposed for disloyalty/unpopularity/corruption (the
accountability trigger's own conditions — not incompetence) can still carry a real exam degree and a
strong `combined_stats_council_svalue` (martial+finesse+charisma+degree prestige), ranking at or near
the top of the very `ordered_character` draw that fires immediately after he is vacated. If drawn,
`QING_office_appoint = { office = rites }` reseats the SAME defender: `add_loyal_veterans = 4`,
`add_character_modifier = qing_officeholder`, `set_variable = qing_office_held = flag:rites`, and
`set_variable = { name = qing_office_$office$_holder  value = prev }` — re-populating the COUNTRY
holder var with his own ID again.

**Step 3 — the second, spurious strip.** The event's own, separate, deliberate
`scope:qing_acc_challenger = { ... QING_office_appoint = { office = rites } ... }` runs right after.
That call's internal "vacate the previous holder of this office" block (`se_QING_COUNCIL.txt:1648-
1667`) checks `has_variable = qing_office_$office$_holder` — and finds the country var pointing at
the defender AGAIN (re-set by the errant backfill in Step 2, moments earlier). It strips him a
SECOND, GENUINE time: the exact same modifier/var set (`qing_officeholder`, `qing_personnel_
cultivated_minor/major`, `qing_censorate_oversight_minor/major`, `remove_variable = qing_office_
held`, `add_loyal_veterans = -4`) — reproducing Step 1's chain verbatim, which is exactly what the
screenshot shows.

## Log corroboration (real boot, not inferred)
`~/Downloads/logs.zip` -> `logs/debug.log`, a live `qing_accountability.1` option `.b` resolution for
office `rites`, shows TWO independent `QING_office_appoint` calls into the SAME office within ONE
resolution of the option: one from `QING_council_autofill_office`'s own backfill draw (fired by
`QING_office_vacate_dispatch`), and one from the event's own explicit challenger appoint. This is
real, observed engine behavior confirming the mechanism above — not a preview-pass artifact (that
theory, present in this diagnosis's first draft, was DISPROVEN by adversarial review, which showed it
self-contradicted the very precedent it cited (task #25/`qing_roster.8.a`), where the confirmed
engine behavior is that a preview pass does NOT commit effects — an unset-var READ error, not a
visible duplicate).

## Scope of the bug
- **Option `.b`** ("Elevate the challenger") — confirmed affected; this is the exact chain traced
  above, corroborated by the screenshot and the log.
- **Option `.c`** ("Dismiss them both") — ALSO calls `scope:qing_acc_defender = { QING_office_
  vacate_dispatch = yes  ... }` (`qing_accountability_events.txt:124-127`), the SAME stateful call
  traced above. It does NOT then call a second `QING_office_appoint` into the same office (no
  challenger is seated in `.c`), so Step 3's re-strip cannot happen — but Step 2's errant backfill
  (reseating the defender into the very office he was just relieved of) is a SEPARATE, real defect
  in its own right: after choosing "Dismiss them both," the office should end up VACANT (the event's
  own stated intent — `qing_office_vacancy_strain`, "the office falls vacant, straining its domain")
  but may instead silently re-seat the disgraced defender via the backfill race, contradicting the
  option's own description and mechanical intent.
- **Option `.a`** ("Stand by the incumbent") — calls NO office-vacate machinery at all (`:63-77`,
  only `add_loyalty`/`add_popularity`/`QING_char_promote_standing`/`add_political_influence`) — NOT
  affected.

## Root cause, restated precisely
`QING_council_autofill_office`'s backfill candidate gate (`se_QING_COUNCIL.txt:216-281`, both the
hard-degree and soft-martial branches) has no exclusion for "this office's own just-vacated holder"
BY IDENTITY — only by role/marker/other-office categories, none of which name the specific man the
dispatcher relieved one line of script earlier. This is a general defect in `QING_office_vacate_
dispatch`'s own backfill call, not something specific to the accountability event — ANY caller of
`QING_office_vacate_dispatch` (the runtime backfill path) is exposed to the same race whenever the
vacated holder himself would otherwise qualify as an eligible backfill candidate.

## Not yet done
This is a DIAGNOSIS only. Per the standing workflow, the next step is a design document for the fix
— most likely: save the defender's scope BEFORE calling `QING_office_vacate` inside `QING_office_
vacate_dispatch`, then add an identity exclusion (`NOT = { this = scope:<saved> }`) to both
`QING_council_autofill_office` candidate-gate `ordered_character` calls — before any code changes.
