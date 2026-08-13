# DESIGN #49 — REV 2: route the accountability event's defender through the NO-BACKFILL vacate
# dispatcher (established idiom), instead of adding a new exclusion marker to the general path

> REV 2 — REV 1 proposed a new transient marker (`qing_vacate_backfill_exclude`) added to `QING_
> council_autofill_office`'s candidate gate. Adversarial review confirmed REV 1's engine-scope
> mechanics were all correct, but found it does not actually fix option `.c`'s stated intent (the
> office should end up VACANT; the marker only stops the DEFENDER being redrawn, not the backfill
> from seating a DIFFERENT courtier or a freshly-minted official) and found a simpler, already-
> established fix. This document replaces REV 1 with that simpler fix, kept ONLY for the general
> vacate-dispatch case's own record (see "Deferred, not built" below).

## Task
Same as REV 1: "A Minister Called to Account" (qing_accountability.1) options `.b` and `.c` route
their defender through `QING_office_vacate_dispatch` — the BACKFILLING dispatcher — even though
NEITHER option wants an automatic replacement: `.b` immediately seats the challenger in the same
office; `.c` explicitly wants the office to fall vacant (its own code comment: "the office falls
vacant, straining its domain"). The backfill's candidate gate has no exclusion for "the office's own
just-vacated holder," so the defender can be redrawn into his own seat moments after being relieved
of it — and `.b`'s own subsequent `QING_office_appoint` call for the challenger then finds him
re-seated and strips him a second, genuine time (the visible double-strip in the screenshot).

## The simpler fix — use the proven no-backfill twin, exactly as `QING_office_appoint`'s own #175
## reshuffle path already does

`QING_office_vacate_dispatch_nobackfill` (`se_QING_COUNCIL.txt:1849-1876`) is the SAME 13-office
dispatch table as `QING_office_vacate_dispatch`, minus the trailing `QING_council_autofill_office`
call — it tears the seat down and leaves it EMPTY for the caller to fill (or not) by hand. This is
not a new idiom: `QING_office_appoint` ITSELF already calls this exact twin (`:1646`) when a manual
reshuffle relieves an appointee's PRIOR office, with the header comment explicitly stating the
reasoning that applies here too: "a MANUAL RESHUFFLE is different... the user's rule is 'when the
player clicks Appoint, NO characters are created.' Auto-backfilling the relieved seat there would
spawn a fresh official off a manual appoint."

The accountability event's `.b` and `.c` are exactly this same class of manual, player-driven
office action — swap `QING_office_vacate_dispatch = yes` for `QING_office_vacate_dispatch_nobackfill
= yes` in BOTH options' `scope:qing_acc_defender` block:

```
# qing_accountability_events.txt:86-90 (option .b)
scope:qing_acc_defender = {
    QING_office_vacate_dispatch_nobackfill = yes
    add_loyalty = loyalty_qing_disgraced
    add_popularity = -15
}
```
```
# qing_accountability_events.txt:124-127 (option .c)
scope:qing_acc_defender = {
    QING_office_vacate_dispatch_nobackfill = yes
    add_loyalty = loyalty_qing_estranged
}
```
No other line in either option changes.

## Why this fixes all three problems in one move (corrected per adversarial review — claim 3 softened)
1. **The double-strip is gone**: no backfill call means no race to redraw the defender — the office
   is simply empty until `.b`'s own subsequent `QING_office_appoint` fills it with the challenger.
2. **`.b`'s wasted-official churn is gone**: without this fix, a backfill could mint or draw a THIRD
   character into the office for zero game-time, only to be stripped again a moment later when the
   challenger is appointed — pure waste. With the fix, only the challenger is ever seated.
3. **`.c`'s strain now persists at the moment of dismissal, though not necessarily forever** —
   corrected claim (review finding 2): `qing_office_vacancy_strain` is a single global modifier,
   removed BY NAME on any later appointment ANYWHERE (`se_QING_COUNCIL.txt:1668`), not gated on
   every office being filled. Without this fix, the backfill could silently refill the seat and clear
   the strain within the SAME tick as the dismissal — defeating the option's stated intent
   immediately. With the fix, the seat genuinely stays empty and the strain genuinely applies at
   dismissal; it may still be cleared later by an unrelated appointment elsewhere, which is
   pre-existing behavior this design does not change or claim to fix.

## Blast radius
Two one-word changes, both inside `qing_accountability_events.txt`, both already-scoped to
`scope:qing_acc_defender`. `QING_office_vacate_dispatch_nobackfill` is an existing, already-shipped,
already-proven function (used by `QING_office_appoint`'s own #175 reshuffle path) — no new function,
no new variable, no change to `QING_council_autofill_office` or `QING_office_vacate_dispatch` at all.
Zero risk to any OTHER caller of either dispatcher, since neither dispatcher's own body changes.

## NOT deferred silently: the general vacate-dispatch race affects ~14 OTHER live callers
## (adversarial review finding — corrects REV 1's unverified "no evidence elsewhere" claim)
REV 1's diagnosis correctly identified a GENERAL defect: `QING_office_vacate_dispatch`'s own backfill
call has no identity exclusion for the man it just vacated. REV 1 claimed "no evidence... showed the
general case actually firing elsewhere" — the REV 2 adversarial review found this claim rested on an
absence of looking, not an absence of the bug: **at least ~14 other callers of the BACKFILLING
dispatch relieve a LIVING minister on a player-driven purge** (`qing_censorate.1`/`.2`/`.4`,
`qing_faction.3`, `qing_office.1`/`.9`/`.10`, `se_QING_CENSORATE.txt:245`, and others not yet
individually confirmed) and share the IDENTICAL redraw hole this design fixes for the accountability
event. Only two callers are provably SAFE by construction: `QING_justice_strip_for_trial` (stamps
`qing_pending_trial` before vacating, which the backfill gate already excludes) and
`on_character_death`'s own natural-death backfill (the vacated holder is dead, so `is_alive = yes`
in the candidate gate already excludes him).

**This design does NOT fix those ~14 other callers** — fixing them is genuinely out of scope for
THIS design (each would need its own check for whether a backfill is actually wanted there, unlike
the accountability event where routing around it is clearly correct for both options). But per this
project's own "no fabrication / no silent deferral" rule, this finding is logged here loudly, not
buried: **a new task should be opened to audit and fix the other ~14 confirmed-exposed callers**,
using either the nobackfill-twin swap (where no replacement is wanted) or REV 1's marker-based
exclusion (verified mechanically sound by adversarial review, aside from its `.c`-specific overclaim
— where a backfill genuinely IS wanted but must exclude the just-vacated man specifically).

## Open questions for review
1. Does `QING_office_vacate_dispatch_nobackfill`'s dispatch table exactly mirror `QING_office_
   vacate_dispatch`'s own 13 offices + emeritus/regent branches (confirmed once already in REV 1's
   review, re-stating here since this design now depends on it directly, not just tangentially)?
2. Is there any effect inside `QING_office_vacate` (called by BOTH dispatchers identically) that
   specifically depends on `QING_council_autofill_office` running afterward, in a way that skipping
   the backfill here could leave some other piece of state inconsistent (e.g. a modifier that
   assumes the office is never empty for more than an instant)? Not found in this pass, but not
   exhaustively ruled out either.
