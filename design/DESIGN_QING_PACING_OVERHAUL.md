# DESIGN — Qing pacing overhaul: integration speed, event cadence, GC-slot fairness

## Scope (6 user requests, one session)
1. Subject integration takes far too little time — should take decades, per history.
2. Subject-integration events should fire far less often — once every few years.
3. Caravan trade events should fire once every few years.
4. Canton trade events should fire once every few years — user has never seen one fire.
5. If Canton events don't touch the silver-reserve contribution, they should.
6. Salt monopoly events should fire once every few years.
Plus, found while diagnosing #2-6: the shared Grand-Council event slot always seems to hand the
turn to the same few systems ("I keep seeing the same few GC events over and over"). Which event
fires should be random; repeats should be avoided. (Task #17.)

All findings below come from a dedicated read-only diagnosis pass (file:line cited throughout,
not re-verified a second time in this doc — see the diagnosis report for the full citations).

## 1. Integration speed — real, single dominant cause, simple fix

`SUBJ_integration_progress` on the subject needs to reach 5 (`se_SUBJECT_QING.txt:339`). The
dominant driver is `QING_fgar_apply_occupation` (`se_QING_FRONTIER.txt:99-139`): for ANY garrisoned
on-ladder subject, it advances +1 UNCONDITIONALLY every 180 days (`qing_frontier_occupation_cd`,
`:103-105`, advance at `:128-138`), with no cap, no shared-slot gating, no probability roll. 5
steps x 180 days = 900 days ~ 2.5 years to fully absorb a garrisoned subject with zero player
input. Historically gaitu guiliu (改土歸流) took decades. This is the only unthrottled, uncapped,
fully-automatic driver among the ~5 total (the rest are treasury-gated, cooldown-gated to 1/year,
or capped by colony counts) — so it dominates the real timeline whenever a subject is garrisoned.

**Fix:** `se_QING_FRONTIER.txt:105`. Two changes to the SAME site, both needed:
- Lengthen `qing_frontier_occupation_cd` from `days = 180` to `days = 1825` (5 years/step x 5
  steps = 25 years total for a garrisoned subject with no other driver — squarely "decades").
- Make the advance itself NOT unconditional: wrap the existing `SUBJ_QING_advance_integration =
  { steps = 1 }` call (`:128`, inside the on-ladder `if`) in a `random = { chance = 60 ... }` — so
  even on the 5-year tick, occupation alone doesn't guarantee forward progress every time (a
  garrison chafes, but "improves administration" is not automatic just because troops are present).
  60% chosen to keep the EXPECTED time in the same "decades" band (expected ~8.3 years/step x 5 =
  ~42 years) without making it feel broken/stalled at the player's table.
- **Not touched**: the manual push-button (`qing_subject_integrate_button`, already 1/year,
  365-day cooldown, 50 influence — a deliberate player lever, not part of the "too fast" complaint),
  and the treasury-gated ILI-only advances (`QING_xj_plant_tuntian`, `QING_caravan_invest_market`)
  — both already cost real resources and are capped, not the runaway driver.
- The threshold (5 steps) is left unchanged — raising it would also lengthen the OTHER, already
  slow/gated drivers (button, treasury-gated ones), overcorrecting things that aren't the problem.

**[Round 1 review, citation fix]** The `SUBJ_QING_advance_integration = { steps = 1 }` call itself
is at `se_QING_FRONTIER.txt:138`, not `:128` — `:128` is the opening `if =` of the on-ladder gate
that wraps it. Wrap the call at `:138` in `random = { chance = 60 ... }`; the gate structure at
`:128` is unchanged. **Round 1 review confirmed this section otherwise sound**: `QING_fgar_apply_
occupation`'s 180-day/unconditional/no-cap shape verified exactly as described; every other caller
of `SUBJ_QING_advance_integration` (`se_QING_CARAVAN.txt:553`, `se_QING_XINJIANG.txt:337/677`,
`SUB_QING_subject_interactions.txt:231`, `se_SUBJECT_QING.txt:448`) is independently gated, so
wrapping only this one call site breaks no shared assumption.

## 2. Subject-integration event pulse — REDESIGNED after round 1 review found the diagnosis wrong

**Round 1 review correction (CRITICAL, accepted):** the original diagnosis missed that `SUBJ_QING_
integration_pulse`'s caller, `qing_integration_pulse_on_action`, already self-throttles to ~twice a
year at the COUNTRY level (`00_monthly_country.txt:43` trigger `NOT = { has_variable = qing_
integration_pulse_cooldown }`, claimed at `:52` with `days = 180`, BEFORE the pulse call at `:53`)
— it does not fire every month. Real per-SUBJECT rate is already ≈ 2 firings/year × 40% roll ×
~71% non-quiet ≈ roughly one real event per subject per ~2 years — already close to "once every
few years," not the 3-4/year originally claimed.
**The real complaint is very likely multi-subject stacking**: `SUBJ_QING_integration_pulse` loops
`every_subject` (`se_SUBJECT_QING.txt:628`) and rolls independently for EACH active subject on the
SAME twice-yearly country pulse — so a player integrating 3-4 subjects at once sees several of
these fire in the same window even though any ONE subject's own rate is already reasonable. This
also matches the complaint's flavour (a general "too many of these" sense, not "this exact one
subject spams me").
**Redesigned fix:** rather than inventing a new per-subject cooldown variable (round 1 flagged a
real problem with that approach: `SUBJ_QING_roll_reaction` is shared with the manual push-button
path, `SUB_QING_subject_interactions.txt:234`, so claiming a cooldown INSIDE that shared function,
as originally proposed, would silently also suppress a subject's future ambient reactions after a
manual button-push — an undiscussed side effect), gate the loop itself on the SAME shared court
slot every other system in this doc uses:
```
every_subject = {
	limit = {
		has_variable = SUBJ_integration_active
		NOT = { has_variable = SUBJ_integration_suspended }
		is_subject_type = autonomous_governorship
	}
	save_scope_as = target
	root = {
		if = {
			limit = { NOT = { has_variable = qing_gc_event_slot_used } }   # NEW
			random = {
				chance = 40
				SUBJ_QING_roll_reaction = { ambient = yes }
				set_variable = { name = qing_gc_event_slot_used  value = 1 }   # NEW, claim-on-roll-success
			}
		}
	}
}
```
**[Round 2 review correction]** the `NOT = { has_variable = qing_gc_event_slot_used }` check moved
OUT of the loop's own governing `limit=` and into a body-level `if=` after entering `root`, matching
the ONLY placement pattern proven at any of the 49 existing claim sites (e.g. `se_QING_AMBAN.txt:
436-455`'s and `se_QING_MARCH.txt:585-687`'s own `every_subject` rolls both check `has_variable`
inside the loop body, never in the outer `limit=`). Behaviourally identical either way (round 2
found supporting evidence — `se_SUBJECT_QING.txt:707`'s own comment on live/sequential iteration —
that the original placement would likely have worked too), but this costs nothing and removes any
doubt by matching established precedent exactly instead of introducing a new, unprecedented shape.
This does not touch `SUBJ_QING_roll_reaction` at all (so the manual button, which calls that same
function directly, is completely unaffected), and does not need a new cooldown variable. Effect:
within one `every_subject` pass, only the FIRST subject (in iteration order) whose 40% roll
succeeds can claim the slot; every subsequent subject in the SAME pass sees the slot already
claimed and is skipped — directly fixing the stacking complaint. Claiming on roll-success (not on
"a real reaction resulted") slightly over-suppresses in the rare case the inner random_list's
"quiet" branch wins (74/104 weight is non-quiet, so this is the minority case) — the SAME accepted
tradeoff `QING_frontier_flavour_roll` already uses for the identical reason (its own comment:
"the safe direction for an anti-spam throttle"), not a new risk pattern.
**Secondary effect worth flagging, not a defect:** integration events now also compete with all
~49 OTHER systems already sharing `qing_gc_event_slot_used` (see section 6) for the same quarter's
single slot — this could push the per-subject rate down FURTHER than the already-reasonable ~1/2yr
baseline. Given the user's complaint was "too frequent," this is the correct direction to err.

## 3-4. Caravan and Canton trade events

**Caravan — largely already correct, no bug.** The 3 Kokand-arc events (caravan.1/.2/.3) are
one-shot, date/state-gated narrative beats, not a recurring loop — nothing to throttle. The one
RECURRING event, caravan.4 (阿奇木 friction), already uses the shared-slot + `qing_dept_cd_caravan`
270-day standdown pattern (`se_QING_CARAVAN.txt:438-457`) — the SAME idiom Canton uses. 270 days
(~9 months) is shorter than "a few years"; **optional tune**: raise it to `days = 1095` (~3 years)
to literally match the user's ask. Low-risk, single-line change, no architectural issue here.

**Canton — the user's "never fires" report has a real, diagnosed cause, distinct from cadence.**
`qing_hoppo_squeeze` is re-derived every quarter directly from the seated Hoppo's fixed `corruption`
stat (`se_QING_CANTON.txt:348`), not a slow drift. Combined with 3 mutually-exclusive, fairly
narrow stat-band branches (commendation/exposure/crisis — see diagnosis) AND Canton's position
deep in a long fixed dispatch chain sharing ONE slot with ~15-20 other systems (see item 6 below),
a seeded Hoppo whose corruption sits outside all three live bands can go the entire game without
ever satisfying — not an impossible trigger, but a real, structural rarity. **This is the SAME root
cause as task #17 (item 6 below), not a separate Canton-specific bug** — fixing the shared-slot
fairness problem is very likely what makes Canton visible at all. No Canton-specific code change
is proposed here beyond that shared fix (adding a NEW score band or loosening the trigger would be
solving a symptom the diagnosis didn't actually confirm is the bottleneck).

**Canton silver-reserve linkage (item 5 in scope) — already true, no gap.** `QING_canton_pulse`
already adds specie to `silver_reserve_size` every quarter (`se_QING_CANTON.txt:233-238`),
UNCONDITIONALLY — regardless of whether any qing_canton.* narrative event ever fires. The
narrative events and the silver-reserve inflow are (correctly) two separate concerns: the pulse's
quarterly production feeds the reserve every quarter; the rare narrative events are flavour on top,
triggered by extremes in the Hoppo's corruption. **No fix needed here — reporting this back to the
user as already-satisfied, not implementing a duplicate hook.**

## 5 (scope item 6). Salt monopoly events — already on the established pattern, mostly already fine

`qing_revenue.1` (salt gabelle reform) is ALREADY on the shared-slot + `qing_dept_cd`-style pattern:
own 270-day cooldown (`qing_revenue_event_cooldown`, `se_QING_REVENUE.txt:289/292`) AND the shared
`qing_gc_event_slot_used` gate (`:290`), then a 40%-chance/quarter roll into a pool where salt
gabelle is weight 20/~70 (`:294-317`) — net ≈ 40% x (20/70) ≈ 11-12%/quarter ≈ once every ~2 years
while unreformed. **This already roughly matches "once every few years."** Contrary to task #16's
original framing, salt does NOT need new throttle wiring — it already has it.
**One real distinction to flag, not fix without confirmation:** this is a single-fire "reform or
not" DECISION event — once `qing_salt_gabelle_reformed` is set, the trigger's own OR-gate
(`:304-307`) blocks re-offering permanently. If the user wants a RECURRING salt-monopoly flavour
event (not just the one-time reform decision) that keeps firing every few years indefinitely, that
is new content to design, not a cadence bug in the existing one. Flagging this distinction for the
user rather than assuming which one they meant.

## 6. GC event-slot fairness (task #17) — the real architectural fix

**Diagnosis, precise:** the ONE shared `qing_gc_event_slot_used` var (cleared monthly at
`00_monthly_country.txt:80`, inside the quarterly-self-throttled `qing_mechanics_pulse_on_action`)
is contested by a long, FIXED, sequential list of ~20 independent systems each quarter: first,
`QING_GOV_pulse`'s own internal chain (`se_QING_GOVERNANCE.txt:212-553` — customs, students,
treaty, techtransfer, vassal, missionary, mission_stations, ili, xj, caravan, censorate, revenue,
works, household, harem, secretariat, southernstudy, wenzhi, canton, treasure_return_voyage,
upperstudy, princes, delib, pop, greatgame, ethnic_tension, integ_capstone — called from
`qing_mechanics_pulse_on_action:98`, BEFORE the rest); then, still inside the same effect, frontier_
flavour_roll (30%, `:118-121`), dynasty (25%, `:127-133`), faction (25%, `:139-146`), foreign_spouse
(20%, `:178-184`), officer_report (12%, `:190-197`). Each checks `NOT has_variable
qing_gc_event_slot_used` before rolling; the FIRST one in this fixed sequence whose own chance
happens to hit claims the slot, and every later check in the SAME quarter then sees it already
claimed and skips. This is strict first-past-post over a fixed priority order, not a random draw
over all eligible candidates — so whichever early, frequently-eligible system tends to win most
quarters, and systems positioned late (Canton) or needing narrow conditions rarely get a turn at
all, regardless of their own chance value.

**What the user explicitly wants:** "which event fires should be random, but repeats should be
avoided." Two distinct properties: (a) true randomness among ELIGIBLE candidates each quarter
(not fixed-order priority), (b) avoid the SAME one firing twice in a row.

**Why a full rewrite (collect all ~20 systems' eligibility into one list, draw once) is NOT
proposed:** it would require touching the internals of ~15-20 separate files to decouple each
system's "administrative pulse work" (which must still run every quarter, unconditionally) from
its "shared-slot event roll" (which must NOT run unconditionally) — a large, high-risk refactor
for a pacing/variety complaint, disproportionate to the ask, and hard to review as one unit.

**Round 1 review verdict on the original "rotating priority window" proposal: REJECTED, redesigned
from scratch.** Two fatal problems, both confirmed by re-reading the actual code:
1. **Blast radius was undercounted by ~7x, not the "3-4x" round 1 estimated.** A full enumeration
   (`rg -n "set_variable = { name = qing_gc_event_slot_used"`) finds **49 separate claim sites
   across 17 files** (se_QING_DYNASTY×8, se_QING_WAR×4, se_QING_FRONTIER×1, se_QING_FACTION×4,
   se_QING_COUNCIL×2, se_QING_MARCH×5, se_QING_CANTON×3, se_QING_PRINCES×2, se_QING_HAREM×2,
   se_QING_DECLINE×5, se_QING_PERSONNEL×2, se_QING_WENZHI×1, se_QING_WORKS×2, se_QING_MARCH_
   PULSE×1, se_QING_CARAVAN×1, se_QING_REVENUE×5, se_QING_AMBAN×1). There is no single place
   "group 1" (or any group) claims the slot as a unit — "group-level" tagging would mean touching
   all 49 sites individually anyway, which is not meaningfully cheaper than a per-site fix and is
   far too large a blast radius to review as one change for a pacing/variety complaint.
2. **The rotation mechanism as specified does not deliver its own claimed property.** Hand-
   simulated: since `qing_gc_slot_check_order` advances independently of who actually won, a
   dominant group (e.g. the GOV_pulse chain, checked first, with by far the most independently-
   eligible sub-rollers) is only in the "protected" pair 2 of every 6 quarters — it can and would
   win the other 4 of 6 quarters uninterrupted, reproducing the exact repeat behaviour the user
   complained about. The mechanism was underspecified (no code ever reads the rotation var to
   compute "the first 2 groups due") and, once made concrete, does not work.

**Redesigned fix — target the two CONFIRMED structural causes directly, not a general-purpose
fairness layer.** This is deliberately smaller than "true uniform randomness over all 49 sites"
(disproportionate — see above) and instead fixes the two specific, diagnosed problems:

**(A) `QING_frontier_flavour_roll` is the single largest structural offender — weaken it.**
It is checked FIRST every quarter (`qing_mechanics_pulse_on_action`, before dynasty/faction/spouse/
officer, and its own `QING_GOV_pulse` call happens even earlier still), at a flat 30% chance
(`se_QING_DECLINE.txt:1496-1497`), and claims the slot the instant that 30% passes — even in the
rare case its own inner `random_list` finds no eligible branch (`:1498-1502`, an explicitly-accepted
over-suppression tradeoff). Fix: lower `chance = 30` to `chance = 15` at that one site
(`se_QING_DECLINE.txt:1497`). A single-line, low-risk change that halves this roller's structural
head start, giving dynasty/faction/spouse/officer (and, once section 2's fix lands, integration)
comparatively more room within the SAME quarter.

**(B) Canton/Revenue(salt) are checked too late inside `QING_GOV_pulse`'s own fixed chain —
reorder, don't rearchitect.** `QING_GOV_pulse` (`se_QING_GOVERNANCE.txt:212-553`) calls ~20
sub-pulses in a fixed sequence; Canton (`:479`) and Revenue (`:439`) are checked after ~10 earlier
systems (customs/students/treaty/techtransfer/vassal/missionary/mission_stations/ili/xj/caravan/
censorate), several of which also claim the SAME shared slot. Fix: move the two existing call
lines — `QING_revenue_pulse = yes` (`:439`) and `QING_canton_pulse = yes` (`:479`) — to immediately
after `QING_accountability_pulse = yes` (`:286`), ahead of caravan/customs/etc. This is a pure
reordering of two independent `= yes` lines, zero logic changed in either function.
**Safety check performed (not just asserted):** read both functions' bodies —
`QING_revenue_pulse` (`se_QING_REVENUE.txt:240+`) starts by reading/writing its OWN reserve-drift
state, no reference to secretariat/southernstudy/wenzhi/household/harem (the systems currently
ahead of it that would move BEHIND it). `QING_canton_pulse` (`se_QING_CANTON.txt:90+`) only checks
`qing_canton_regime` and Guangzhou ownership — also self-contained. The systems that explicitly
document a same-quarter ordering DEPENDENCY (`QING_southernstudy_pulse` "runs after secretariat";
`QING_secretariat_pulse` "runs after household/harem"; `QING_caravan_pulse` "runs after QING_xj_
pulse") all depend on something EARLIER, and none of them are things Canton/Revenue currently
precede and would stop preceding — so nothing downstream should break. **Flagging for round 2
review to double-check independently** — this reordering touches real gameplay sequencing and
deserves a second look, not just this session's own read.

**What this does NOT deliver, stated plainly (sharpened per round 2 review):** true uniform
randomness over all 49 claim sites, or a hard guarantee against any repeat anywhere in the system.
`QING_GOV_pulse`'s own ~20-system internal chain still runs FIRST every quarter, entirely unchanged
by (A) or (B) — (A) only weakens `frontier_flavour_roll` (which is checked AFTER that whole chain
already had its turn); (B) only reorders 2 systems WITHIN that chain, ahead of the 11 that used to
precede them, not ahead of the chain's role relative to frontier/dynasty/faction/spouse/officer.
**Concretely: Canton and Revenue should visibly win the slot more often than before (real,
targeted improvement), but the GOV_pulse chain AS A WHOLE is still likely to keep beating
dynasty/faction/frontier/spouse/officer most quarters — the "same few events" complaint may
resurface in a milder form (now more often "whichever GOV_pulse sub-system wins" rather than
"whichever of the previous first 11"), not fully resolved.** A true fix for that residual would
still require the disproportionate 49-site rewrite already rejected above. (A) and (B) are the two
mechanisms this session's diagnosis actually confirmed as structurally dominant; fixing those two
is expected to visibly improve Canton's odds specifically, without the risk of a 49-site rewrite —
but this is a partial, not complete, fix to the general variety complaint, and the user should
expect that going in, not discover it after the fact. If repetition (in this milder, GOV-pulse-
internal form) still bothers the user after this lands, that is the signal to revisit scope for a
genuine candidate-collection rewrite, not a reason to over-build now.

## 7. Art Patronage / Court Painter events (task #15, separate/smaller — not yet designed in detail)
Real gap: `se_QING_WENZHI.txt` has a live Court Painter mechanic (Castiglione seed, `QING_wenzhi_
commission_painting`, Jesuit-suppression) and a dedicated panel (`QING_household_panel.txt:263`),
but zero dedicated narrative events — only 2 generic wenzhi events (qing_wenzhi.1/.2), neither
painter-specific. Proposed for a FOLLOW-UP design (not detailed here to keep this doc reviewable):
2-3 new events in a new or existing wenzhi-adjacent event file, triggered from `QING_wenzhi_
commission_painting` (a completed commission) and/or a low-chance ambient roll inside `QING_wenzhi_
pulse` — using the SAME shared-slot + dept-cooldown convention as every other system in this doc,
so it doesn't reintroduce the exact fairness problem section 6 just diagnosed.

## Summary of what actually needs code changes (post round-1 review corrections)
- **Real fixes**: #1 (integration speed, 2 edits at `se_QING_FRONTIER.txt:105` + wrap the call at
  `:138`), #2 (integration pulse, 2 new lines inside `SUBJ_QING_integration_pulse`'s `every_subject`
  loop, `se_SUBJECT_QING.txt:628-640` — no new variable, no shared-function touch), #6 (GC-slot
  variety, 2 edits: `se_QING_DECLINE.txt:1497` chance 30->15, plus moving 2 existing lines —
  `QING_revenue_pulse`/`QING_canton_pulse` — earlier in `se_QING_GOVERNANCE.txt`'s call order).
- **Optional tune, not a bug**: caravan.4's 270-day cooldown -> 1095, if the user wants it literal.
- **Already correct, no action**: Canton silver-reserve linkage (already unconditional every
  quarter); salt's existing throttle — user confirmed the existing one-time reform cadence is fine,
  no recurring flavour event wanted.
- **Deferred, separate follow-up**: Art Patronage/Court Painter events (#7/task #15).
- **Explicitly out of scope, not attempted**: a full 49-site rewrite for mathematically-uniform
  event-slot randomness (see section 6) — rejected as disproportionate; (A)+(B) above target the
  two mechanisms actually confirmed dominant.
