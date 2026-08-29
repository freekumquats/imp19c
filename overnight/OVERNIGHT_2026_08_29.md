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
