# Overnight run — 2026-08-29

Multiple forks are working this backlog in parallel worktrees; each appends its own
section here before merging. This section covers tasks #5, #10, #11.

## Task #10 — "A Report from the Field" (qing_zongli_dispatch.1): loc bug + redesign

Diagnosis: the event rendered the literal broken string
`ERROR:[scope:qing_dispatch_evt_diplomat.GetName]` (screenshot-confirmed,
`~/Downloads/20260829011005_1.jpg`). Root cause per the standing loc-scope-syntax rule:
saved scopes are read bare as `[x.GetName]`, never as `[scope:x.GetName]`.

Separately, the event's single "Hear the report" option ran a charisma-weighted
`random_list` with `custom_tooltip` lines per branch — those are preview-only text and
never displayed after the pick fired, so the player learned nothing about which outcome
happened. User's explicit instruction: cut the "useless" first click, resolve the chance
directly, and tell the player the concrete result.

Fix: moved the `random_list` roll from the event's option into
`QING_zongli_dispatch_pulse` (common/scripted_effects/se_QING_ZONGLI_DISPATCH.txt) —
it now resolves immediately, applies `DIPLOMACY_modify_play_success`, and sets a
country-scope flag `qing_zongli_dispatch_evt_outcome` (`flag:success`/`flag:failure`)
before `trigger_event`. `qing_zongli_dispatch.1` (events/imp19c_mod_events/qing_zongli_dispatch_events.txt)
is now a pure outcome notification: trigger requires `has_variable = qing_zongli_dispatch_evt_outcome`,
`desc` branches via two `triggered_desc` blocks, option just `remove_variable`s it. This
mirrors the existing proven idiom `qing_march_unrest_outcome` / `qing_march.6` (task #91)
— same codebase, same shape, already battle-tested. Loc file updated: fixed the scope
syntax, replaced the single `.desc` + two `.tt` keys with `.desc_success` / `.desc_failure`,
renamed the option label "Hear the report" -> "Understood" (there's no longer a two-stage
report to "hear").

Adversarial code-review ran clean: random_list-in-scripted-effect is a proven pattern
elsewhere in this codebase (se_QING_DECLINE.txt, se_QING_WAR.txt etc.), the country-scope
write/read for the outcome var is correct and mirrors se_QING_MINISTRY.txt's root-capture
idiom, and the per-tick slot guard still prevents two diplomats' rolls from colliding.
One low-severity, non-blocking note: if the play ends or the diplomat dies during the
event's 5-15 day delay, the outcome var can linger uncleared on the country (harmless —
same accepted property as the qing_march precedent). Not fixed, since it's precedented
and not a regression.

## Task #5 — Zongli Yamen "Dispatched" button clipping

gui/qing_zongli.gui: the Recall/Dispatched button was 84px wide (`max_width = 78` on the
text) — "Dispatched" (10 chars) didn't reliably fit. Widened the containing widget
90->100, the button 84->94, and the text max_width 78->88. Minimal increase per the
user's "just a little bit."

## Task #11 — Diplomatic Plays (Supranational) window right-side clipping

Traced the window: `type supranational` (gui/imp19c_windows.gui, `size = { 1300 @window_height }`)
hosts the "diplomatic_plays" tab, a scrollarea (`size = { 930 615 }`) listing
`diplomatic_play_global_item` rows (gui/shared/gui_templates.gui:4093). Summed that
template's row-content width (instigator flag+name column, supporters+action-buttons
column, title/details column, balance/progress/success icon column, target
supporters+oppose column, target flag+name column, plus inter-column spacing) — comes to
~975px, exceeding both the 930px scrollarea and effectively the window's own available
right-side budget (1300 total minus the ~342px left-hand global-power panel). This is
why the rightmost element (target-country name, e.g. "Russia") clips its last
character(s) at the row's right edge.

Fix: widened the window 1300->1360 and the scrollarea 930->980 (gui/imp19c_windows.gui).
Did not touch gui_templates.gui's row-content template itself — the row's own column
widths are unchanged, they just now have room to render inside their container.

## ASSUMPTIONS & GUESSES

- Task #11's exact widen amounts (60px window, 50px scrollarea) are a best-guess sized
  to the row's summed content width, not boot-verified pixel-for-pixel (no boot test
  available in this pass). If still tight in practice, the fix direction (widen window +
  scrollarea together, proportional to the left global-power panel's fixed 335+7px) is
  correct; only the exact px amount might need a follow-up nudge.
- Tasks #12, #13, #14 (diplomatic-range limit, Balance of Power/success/progress tooltip
  text, and the deterministic-vs-probabilistic outcome architecture question) are
  explicitly NOT touched in this section — they're assigned to a separate concurrent
  fork ("fix-diplomatic-play-scope-regression") to avoid duplicate/conflicting edits to
  the same gui_templates.gui file region.

## Task #16 — EDU_set_t2_national_bonus_from_universities has_law/owner scope errors (~1853x each)

This was already "fixed" once, by commit 7afd1b097 (tasks #17/#20, landed 2026-08-26):
it wrapped the national-bonus multiply in `owner = { value = EDU_university_national_bonus }`,
on the theory that the preceding `every_governorships -> every_governorship_state ->
every_state_province` iterator left the value={} block's scope at PROVINCE for that sibling
multiply term.

The 2026-08-29 01:23 error.log (the newest log at the time of this run, boot AFTER
7afd1b097 was live) still showed ~1853 occurrences of both errors, unchanged in count.
Root-caused by reading the exact error text literally instead of trusting the prior
diagnosis: the owner-link error reports `[...] Expected 'province, state, governorship,
legion', but got 'country'` — i.e. scope at that call was already COUNTRY, not leaked to
province. Wrapping an already-country scope in `owner={}` is itself invalid (owner has no
valid source when already at country), and everything nested inside that failing owner
block — including `EDU_university_national_bonus`'s own `has_law` check
(EDU_svalues.txt:78) — then evaluated in the resulting invalid/"none" scope. One mistake,
both error signatures.

Fix (common/scripted_effects/se_EDU.txt, EDU_set_t2_national_bonus_from_universities):
removed the owner={} wrap; moved the multiply out of the set_variable's nested value={}
block entirely into its own top-level `change_variable` statement, a sibling to
set_variable rather than an arithmetic term inside it. This runs unambiguously at the
effect's own Country scope (entered correctly via `every_country` in
EDU_startup_effect/EDU_update_effect) regardless of whether the value-block sibling-leak
theory from 7afd1b097 was ever actually correct — sidesteps the question rather than
re-litigating it.

Self-reviewed (adversarial pass done solo, in-worktree — this fork's own code-review
subagent call is unavailable from inside a forked worker): verified brace balance before
and after the edit, confirmed no other call sites reference the removed structure, and
confirmed EDU_svalues.txt itself needed no change (EDU_university_national_bonus and
EDU_university_national_bonus_here, the two existing correct usages at province/country
scope, are untouched).

Commit: ab4474f78 (rebased onto 86acb0428 after a non-fast-forward push race with the
tasks #5/#10/#11 fork).

### Note on this fork's own diagnosis process
This fork's worktree was branched from a stale point in history (predating
tools/precommit_checks.py and the entire 7afd1b097 fix) — its own first diagnosis pass
(before discovering this) independently arrived at the same "sibling-arithmetic-term
scope leak" theory and drafted a fix against the STALE pre-7afd1b097 code. That draft was
discarded (never pushed) once `git fetch`+rebase surfaced the merge conflict revealing
7afd1b097 already existed and had already failed. The final fix above was derived fresh
against the current (post-7afd1b097) code and the actual current error text, not by
reapplying the stale draft.

### ASSUMPTIONS & GUESSES (task #16)
- Not boot-verified (no boot test available in this pass). The fix is derived directly
  from the literal error text ("got country") rather than from re-deriving engine scope
  semantics from first principles, so confidence is high but not certain. If ~1853 errors
  persist in the next boot log at this exact call site, the next step should be to check
  whether `every_governorships` as a value-block sibling to `multiply=` really does leak
  scope for OTHER similar constructs in this codebase (search for other
  `value={ every_governorships = {...} multiply = ... }` shapes) — that would mean this
  particular error's true cause is elsewhere in the chain (e.g. a corrupted/failed limit=
  evaluation on some governorship), not the multiply's rescoping at all.
