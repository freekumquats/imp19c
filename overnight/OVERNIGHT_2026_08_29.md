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
---

# Overnight 2026-08-29 — Tasks #4/#9: Grand-Council event throttle

## Task
Two reports: "A Minister Called to Account" (qing_accountability.1) fired 3x in
one week; "Clash at the Residency" (qing_amban.1) allegedly spamming (reported
as a regression of a prior once-per-year fix). Instruction: treat this as ONE
generic mechanism failure, not two one-off patches — diagnose the shared
throttle, fix it generically, then verify every other Grand-Council-tied event
against the same mechanism.

## Diagnosis process
1. Confirmed event IDs via loc: qing_accountability.1 ("A Minister Called to
   Account"), qing_amban.1 ("Clash at the Residency").
2. Found the documented STANDING RULE (audits/SESSION_HANDOFF_2026_08_11.md):
   every Grand-Council/subordinate-bureaucracy event must share a single
   country-scoped slot variable, `qing_gc_event_slot_used`, reset at the top
   of the ~90-day `qing_mechanics_pulse_on_action` (common/on_action/
   00_monthly_country.txt). Pattern: check `NOT has_variable` in the fire
   path's limit, `set_variable ... = 1` ONLY on the branch that actually
   fires (never in the pulse wrapper), so at most one court event fires
   realm-wide per quarter.
3. **Process error, caught and corrected**: my worktree branch had diverged
   from `merge-overnight` at an earlier commit (`fe6c274ab` vs the real tip
   `9167d4e3d`) — a shared-slot-and-cooldown-stripped `se_QING_AMBAN.txt` I
   was reading was STALE, not the live file. Verified via
   `git merge-base --is-ancestor` and `git fetch origin merge-overnight`,
   then `git reset --hard origin/merge-overnight` (clean tree, safe) to get
   onto the real current base, and re-ran the diagnosis from scratch.
4. On the correct base: **qing_amban.1's throttle is fully intact and
   correct** — `NOT has_variable qing_gc_event_slot_used` in the limit, a
   730-day per-subject cooldown (`qing_amban_clash_cd`, task #60), and the
   claim (`set_variable qing_gc_event_slot_used = 1`) only on the fire
   branch, in `se_QING_AMBAN.txt`'s clash fire path. Only one
   `trigger_event { id = qing_amban.1 }` call site exists in the whole repo.
   **No fix needed here** — the "regression" was an artifact of reading the
   wrong branch state, not a real bug.
5. `se_QING_ACCOUNTABILITY.txt`'s `QING_acc_test_challenge` (the fire path for
   qing_accountability.1) had NO participation in the shared slot at all, and
   NO per-office cooldown. Its only gate was `qing_acc_challenge_pending`,
   which only prevents >1 challenge PER CALL of `QING_accountability_pulse`
   (i.e. per quarter) — it does not stop the SAME office from re-queuing a
   fresh challenge every ~90-day quarter indefinitely while the incumbent
   stays weak. This is the confirmed root cause of "A Minister Called to
   Account" firing repeatedly.
6. Per the "check every GC-tied event" mandate, audited every other pulse in
   `QING_GOV_pulse`'s office-coupling family that calls `trigger_event`
   directly: PERSONNEL (`qing_dept_cd_personnel`, correctly wired), WAR
   (`qing_dept_cd_war` + `qing_warlord_review_cd`, correctly wired), REVENUE
   (`qing_revenue_event_cooldown`, correctly wired), CANTON
   (`qing_dept_cd_canton` + per-crisis cooldowns, correctly wired), WORKS
   (`qing_works_event_cooldown`, correctly wired), HAREM (correctly wired).
   CENSORATE and GREATGAME never call `trigger_event` directly — their
   dramatic events (qing_censorate.*, qing_greatgame.*) are dispatched from
   `QING_frontier_flavour_roll` in se_QING_DECLINE.txt, which claims the slot
   BEFORE its inner random_list runs (documented BT-28 pattern) — confirmed
   correctly wired, not a gap.
7. **Second confirmed bug**: `se_QING_HOUSEHOLD.txt`'s
   `QING_household_eunuch_event_roll` (fires qing_household.8/.9). Its own
   header comment claims it "Shares the GC event slot via the standard
   throttle," but the code never actually checked or claimed
   `qing_gc_event_slot_used` — only its own dedicated 1460-day
   (`qing_eunuch_event_cd`) cooldown gated it. This let a eunuch-intrigue
   beat fire in the same quarter as another already-claimed court event
   (dogpile), contradicting the comment's own stated intent. Confirmed real,
   fixed to match the documented (but previously unimplemented) behaviour.

## Fixes applied
- `common/scripted_effects/se_QING_ACCOUNTABILITY.txt`, `QING_acc_test_challenge`:
  added `NOT = { has_variable = qing_gc_event_slot_used }` and
  `NOT = { has_variable = qing_acc_challenge_cd_$office$ }` to the fire-path
  limit; added `set_variable = { name = qing_gc_event_slot_used value = 1 }`
  and `set_variable = { name = qing_acc_challenge_cd_$office$ days = 365 }` on
  the fire branch (claim-on-fire, matching every other correctly-wired
  system). The per-office cooldown var name uses the same
  `..._$office$` macro-substitution-in-a-variable-name idiom already proven
  elsewhere in this same file (`qing_office_$office$_holder`, line 103).
- `common/scripted_effects/se_QING_HOUSEHOLD.txt`,
  `QING_household_eunuch_event_roll`: added
  `NOT = { has_variable = qing_gc_event_slot_used }` to the fire-path limit
  and `set_variable = { name = qing_gc_event_slot_used value = 1 }` on the
  fire branch, restoring what the function's own comment already claimed it
  did.
- Existing `LOG_line` calls on both fire paths already log every successful
  fire (static strings, `$office$`/`$param$`-style substitution inside a LOG
  string is cosmetic-only per the log-string-macro standing rule, not
  call-voiding) — no new LOG plumbing was needed; both fixes are additions
  to existing, already-logged branches.

## ASSUMPTIONS & GUESSES
- **365-day cooldown for `qing_acc_challenge_cd_$office$`**: not directly
  specified by the user. Chosen for "once per year" symmetry with the
  amban's task-#60 per-subject pattern (which uses 730 days, ~2 years, for a
  rarer/heavier subject-level event); accountability challenges are a
  lighter-weight per-office beat, so a shorter 1-year window was judged
  reasonable. If this is judged too frequent or too rare in play-testing, the
  duration is isolated to this one line and can be tuned.
- **Scope of "every GC-tied event"**: interpreted as the office-coupling
  family explicitly named in `QING_GOV_pulse`'s own dispatch order (Personnel,
  War, Revenue, Canton, Works, Household, Harem, Censorate, Accountability,
  Amban, Great Game) plus the six flavour/foreign-spouse/officer-report
  rollers already gated from `00_monthly_country.txt`. Did NOT re-audit the
  entire ~70-file Qing event catalog (march, tribute, colonization arcs,
  Japan, sphere-of-influence, etc.) — those are already covered by separate,
  dedicated prior audits (design/DESIGN_QING_CROSSWIRING_ASSESSMENT.md,
  design/DESIGN_QING_PACING_OVERHAUL.md) and are a larger, separately-scoped
  concern than the two reported office-coupling bugs.
- **qing_amban.1 required NO fix.** Confidence: high — verified against the
  live `origin/merge-overnight` tip (9167d4e3d) after discovering and
  correcting the stale-branch read, and confirmed only one call site exists
  in the whole repo.

## Verification
- Read-only confirmation that the shared slot is reset exactly once per
  ~90-day pulse (common/on_action/00_monthly_country.txt lines 74-88) and
  that both new fire paths now claim it only on their fire branch, never
  unconditionally.
- Manually traced every `trigger_event` call site in the audited files listed
  above; no other GC-tied fire path found missing the slot check.
- No boot test run (out of scope for a script-only .txt change with no new
  syntax construct beyond an already-proven idiom); per the no-bisection /
  "guess, build, log" contract this is not treated as a blocker.

---

# Overnight 2026-08-29 (second fork) — Task #11 continued: province-window Diplomatic Plays panel also clipped

This fork's worktree (`worktree-agent-a888ba3e432c0d3d1`) had drifted far
behind `merge-overnight` (last common point was mid-July). Confirmed the
worktree's one unique commit (`fe6c274ab`, a merge of two commits both
already ancestors of `merge-overnight`) added nothing not already on
`merge-overnight`, so `git reset --hard merge-overnight` was safe (no unique
work lost) before starting. Flagging this since it's a bigger git operation
than a normal task, even though no content was at risk.

By the time this fork went to push, commit `86acb0428` (above) had already
landed fixes for tasks #5, #10 and #11 — but its #11 fix addresses a
*different* window (the Supranational "Diplomatic Plays" tab in
`gui/imp19c_windows.gui`, using the `diplomatic_play_global_item` template).
This fork had independently traced the same reported symptom (a clipped
target-country name, e.g. "Russia") to a second, separate instance of the
same card family: the **province window's** embedded "Diplomatic Plays"
panel, which uses a different, smaller template — `diplomatic_play_item`
(`gui/shared/gui_templates.gui`), confirmed via grep to be instantiated in
exactly one place: `gui/province_window.gui`. Since the two fixes touch
disjoint files with no line overlap, both are kept — this section only
covers this fork's own change, task #5's overlapping edit to
`gui/qing_zongli.gui` was dropped in favour of the already-landed one (see
rebase note at the end).

## Task #11 (province window instance) — Diplomatic Plays panel right side clipped

**Files:** `gui/shared/gui_templates.gui` (`type diplomatic_play_item`, the
per-play card template) and `gui/province_window.gui` (the embedded
"Diplomatic Plays" panel, loc key `province_diplomatic_play_list`, inside the
province window's diplomacy tab).

**What it was:** The `diplomatic_play_item` card was a fixed 470px-wide card
inside a `sub_header_v` container that was only 480px wide — only 10px of
slack, which the vertical scrollbar ate into, clipping the card's rightmost
column (the target-country flag + name + supporter-flag row — e.g. the last
letter of "Russia" plus its supporter flags, per the reported screenshot).
The diplomacy-tab `margin_widget` hosting that panel was 500px wide.

**What I did:** Widened the card `470->490` (+4.3%) and its target-side
(rightmost) column specifically — the "supporter panel" the task called out —
from 90px to 110px on the country-name textbox, the "Supporters" label, and
the supporter-flags `overlappingitembox`; left the col3 "Oppose" button at
90px since its own text wasn't reported as clipped. Widened the containing
`sub_header_v` `480->520` and the diplomacy-tab `margin_widget` `500->540`
(content width `540 - margin(10+10) = 520`, exactly matching the
`sub_header_v`) so the scrollbar no longer eats into the card's visible area.

Verified arithmetic (confirmed by an independent code-review pass): card
content = margin(5+5) + col1(100, bounded by its own `#Y Supporters`
textbox, not the 90px name box) + spacing(5) + col2/title(250) + spacing(5) +
col3(110, widened) = 480, inside the new 490-wide card, inside the 520-wide
`sub_header_v` — 10px of genuine slack past the card, versus 10px that used
to be entirely consumed by the scrollbar. Also confirmed the two-row,
three-button goal-picker above this panel (150px x3 + spacing, ~462px per
row) still fits comfortably inside the new 520px content width.

## Review

This diff (`gui/shared/gui_templates.gui`, `gui/province_window.gui`) was
sent to an independent code-review subagent before commit (per the standing
rule) with explicit instructions to check brace balance, arithmetic, and for
any accidental unrelated corruption in these whitespace-sensitive `.gui`
files. Verdict: PASS on both files — no brace imbalance, no overflow, no
unrelated edits, comments accurate. Two non-blocking FYIs noted (pre-existing
BOM on `province_window.gui`, present before this change; one comment calls a
100px-wide column's ceiling "95" — conservative wording, not a bug) — no
action needed on either.

## Reconciliation with 86acb0428

Task #5's edit to `gui/qing_zongli.gui` (button/wrapper/`max_width` widen)
overlapped line-for-line with 86acb0428's own fix to the same button,
already reviewed and pushed first. Kept 86acb0428's numbers (wrapper
90->100, button 84->94, max_width 78->88) as-is on rebase; kept this fork's
row-widget widen (468->482), which doesn't conflict and just adds a little
extra margin around the already-fixed button. No duplicate #5 write-up
retained above — see 86acb0428's own section for that fix.

**Follow-up review advisory (resolved):** the second code-review pass flagged
that widening the diplomacy-tab `margin_widget` (500->520 content width)
shifts its horizontal flowcontainer sibling — the `province_colonization`
`sub_header_v` at line 5199, `size = { 280 520 }` — by +40px absolute
x-position, since that flowcontainer doesn't clip. Checked: that sibling has
`enabled = no` / `visible = no` (pre-existing, unrelated TODO — "Should
appear on a separate tab"), so it isn't currently rendered and the shift has
no live visual effect. No change needed; noting for whoever eventually wires
up that tab, since its layout will land 40px further right than before this
fix.

---

## Task #10 continued — GP-dispatch sibling fix (this fork)

This fork independently picked up task #10 and reached the same diagnosis and the same
`qing_march_unrest_outcome`/`qing_march.6` precedent as the section above (already merged as
commit `86acb0428` by the time this fork tried to push) — so the Zongli-chain half of this
work is superseded by, and identical in effect to, the section above; no changes made on top
of it. Kept: an additional sibling bug this fork found by inspection that the section above
did not touch.

**Sibling bug: `qing_gp_dispatch` (Great Game "Dispatch a Diplomat" follow-up).**
`events/imp19c_mod_events/qing_gp_dispatch_events.txt` / `se_QING_DIPLO.txt`'s
`QING_gp_dispatch_diplomat` explicitly documents itself as mirroring the Zongli play-dispatch
chain, and had copied the identical bug: `[scope:qing_gp_dispatch_evt_diplomat.GetName]` in loc
(same invalid script-only `scope:` prefix rendering literal `ERROR:[scope:...]` text) and the
same click-to-reveal `random_list`-in-option shape.

Fixed to match the now-landed Zongli pattern exactly, for consistency: `QING_gp_dispatch_diplomat`
now rolls the same 50/50-base, charisma-skewed weights immediately (±6 tension on
`qing_gp_tension_$power$`, magnitude unchanged) and sets a `qing_gp_dispatch_evt_outcome` flag
(`this` is already country scope throughout this effect — called `scope = country` from
`QING_mechanics_actions.txt` — so no `save_scope_as` is needed) before firing a single
`qing_gp_dispatch.1`. That event's `desc` branches via two `triggered_desc` blocks keyed on the
flag, its `trigger` re-checks `has_variable = qing_gp_dispatch_evt_outcome` plus diplomat
liveness, and its option (`"Understood"`) clears the flag — same shape as `qing_zongli_dispatch.1`
and its `qing_march.6` precedent. Diplomat-marker teardown
(`remove_variable = qing_zongli_dispatched_marker` / `qing_zongli_dispatched_gp_power`) stays in
the event's own `immediate` (not hoisted into the dispatching effect), so the event's re-check
trigger still holds when it fires 20-40 days later.

Diagnostics: kept `LOG_line` calls (native `debug_log`, inherently -debug_mode-gated) on the roll
stating which branch fired plus the magnitude applied.

**Files touched (this fork, on top of `86acb0428`):**
- `common/scripted_effects/se_QING_DIPLO.txt` (`QING_gp_dispatch_diplomat`)
- `events/imp19c_mod_events/qing_gp_dispatch_events.txt`
- `localization/english/qing_gp_dispatch_l_english.yml`
- `design/DESIGN_ZONGLI_DIPLOMAT_DISPATCH.md` (addendum section 9, rewritten to describe what
  actually shipped for both the Zongli chain and this sibling fix)

**Not deferred; nothing left open on this task.**

---

## Small unassigned error.log classes batch (5 classes, this section)

Source log: `~/Downloads/logs.zip` (2026-08-29 01:23/01:25, 25820-line error.log). Ran the
imp19c-logs Rule 3 ranked-inventory sweep to re-derive exact lines for 5 smaller classes left
unassigned after the largest classes were dispatched to other parallel workers. Checked
`git log` on merge-overnight before starting (tip 9167d4e3d, task #16 Great Game work) — none
of the 5 classes below were already touched by other in-flight commits. Re-checked again
before pushing (tip had advanced to 6856d2b01 with 4 more commits: task #16 EDU scope-error
fix, Grand Council event throttle restore, Report from the Field loc/design + window
clipping) — `git diff --stat` between 9167d4e3d and 6856d2b01 confirms none of those commits
touch any of the 6 files below, so no overlap and no merge conflict on the code changes.

### 1+2. "Wrong scope for trigger for compare trigger 'none'" (10x) + "Event target link
'compare_value' returned an unset scope" (10x) — SAME BUG, not two classes

Both errors fire together, every time, at the identical `Script location`:
`common/on_action/00_monthly_country.txt:104; QING_GOV_pulse:64; QING_pop_pulse:4;
QING_pop_recompute_target:6` (`common/scripted_effects/se_QING_POPULATION.txt`).

Root cause: the 2026-08-20 fix (`67c50bd4b`, "log-triage 2026-08-20") staged
`country_population` into a tmp var via `set_variable = { name = ...  value = { value =
country_population } }`, on the theory that a var-compare "never throws." NOTE: an earlier
draft of this note claimed `country_population` has no proven value-read usage anywhere in
the codebase — a code-review pass disproved that; it IS proven as a bare single-wrap value
(`se_ECON_LOG.txt:859` `value = country_population`, plus 5+ `common/script_values/*.txt`
sites). The real defect is narrower: the DOUBLE wrap, `value = { value = country_population
} }`, nests a value block inside a value block, which is not the proven idiom anywhere —
every working precedent is either the single-wrap `value = country_population` or the bare
TRIGGER form `country_population > 0` (`common/scripted_lists/EE_lists.txt:38`). That extra
nesting is what surfaced as "Wrong scope for trigger for compare trigger 'none'" / "Event
target link 'compare_value' returned an unset scope" on EVERY pulse (not just an early
not-warm tick) straight through the 2026-08-29 boot log. This explains why the 08-17
investigation (logged in `overnight/OVERNIGHT_2026_08_17.md`) could not confirm a root
cause: it was chasing the granary-rederive function, but the real bug was the 08-20 fix
itself, landed AFTER that 08-17 pass and not yet re-investigated. It also explains
persistence across the WHOLE 45-minute session (10 hits spread 00:41–01:23) rather than just
an early boot race — this is a per-pulse failure, not a "pop index not warm yet" race.

FIX: this guard only needs a boolean gate, not a staged value, so dropped the tmp-var
indirection entirely; guard directly on the bare trigger `country_population > 0` (the exact
EE_lists.txt:38 idiom, and the same form `se_ECON_LOG.txt`'s own comment cites as already
proven at this call site). `common/scripted_effects/se_QING_POPULATION.txt`.

Overlap check: NOT part of the has_law/tag scope bug classes assigned to other workers —
confirmed by the distinct `Script location` (se_QING_POPULATION.txt, not a has_law/tag
site) and by grep — no other merge-overnight commit touches this file today.

### 3. "ordered_owned_province effect [ Given max value was bigger than the list, capping at
list size ]" (8x)

`Script location: common/on_action/economy/oa_economy_setup.txt:2514;
SE_row_starting_buildings:14; ROW_seed_country_buildings:86` →
`common/scripted_effects/se_ROW_BUILDINGS.txt`.

Root cause: the RESIDENTIAL districts block (`ordered_owned_province { ... max = 2 ...
}`) was gated by an outer `any_owned_province = { NOT = { has_building = ... } }` guard that
only proves >= 1 qualifying province, not >= 2. Every other `ordered_owned_province` call in
this file (manufactory/plantation/commerce/industrial-estate, all `max = 1`) has an outer
guard that exactly matches its max; only the residential block's max=2 was left unguarded for
the >=2 case. Whenever exactly one province still lacked the building, `max=2 > list_size=1`
threw "Script system error!" (still functionally correct, self-corrects to 1 build) 8x/boot.

FIX: split into an exact-count branch — `count >= 2` guard for the max=2 pass,
`else_if` (bare `any_owned_province`, no count) with `max = 1` for the single-remaining-
province case. Same net behaviour (top up to 2 population centres), zero spurious errors.
`common/scripted_effects/se_ROW_BUILDINGS.txt`.

Overlap check: unrelated to the memory `imp19c-ordered-iterator-max-rule` "default max=1"
case (this bug is the opposite direction: max TOO BIG, not missing). No other worker's
assigned classes touch se_ROW_BUILDINGS.txt.

### 4. custom_tooltip unknown-loc-key errors (6x), culture_decisions/imp19c_general_culture_decisions.txt

Exact lines (Script location): 13, 16, 71, 74, 77, 83.

Root cause: `custom_tooltip.text` is ALWAYS a loc-key lookup — never inline literal text,
even when the literal text has no bracket promotes. This file (a near-verbatim port of
vanilla Imperator's Culture-DLC decisions: `language_recognition` / `language_standardisation`
/ `self_determination`) had 4 distinct literal strings pasted straight into `text = "..."`
(2 of them duplicated across both decisions), so every one threw "Unknown loc key <the
literal string>". Two of the 6 hits (lines 16, 74) actually trace into the shared scripted
trigger `same_language_culture_trigger` (`common/scripted_triggers/00_language_groups.txt`)
which had the identical bug pattern for its own tooltip.

FIX: added 4 new loc keys to `localization/english/imp19c_tooltips_l_english.yml`
(`imp19c_lang_shares_language_tt`, `imp19c_lang_not_official_tt`,
`imp19c_lang_closely_related_tt`, `imp19c_lang_has_same_language_tt`), reusing the exact same
promote text (SCOPE.sCountryCulture(...) syntax already proven valid elsewhere in the mod's
loc, e.g. `GetCountryCulture` in interface_l_english.yml:98 and the `SCOPE.s<Type>('name')`
pattern used throughout triggers_l_english.yml/flavor_events_l_english.yml). Updated both
`custom_tooltip.text` fields in the decisions file and the one in 00_language_groups.txt to
reference the new keys instead of inline strings.

BONUS (not in the 6-hit count, found while auditing the same file): `similar_language_culture_
trigger` (00_language_groups.txt:73) has the identical bug ("Has a similar language" inline)
but the trigger is currently dead code (never called anywhere in the codebase), so it wasn't
in the log. Fixed anyway for consistency — added `imp19c_lang_has_similar_language_tt` — so it
doesn't reintroduce this exact bug the day someone wires it up.

### 5. "none effect [ Both family and family_name was set, family will be used ]" (2x),
setup/characters/00_Korea.txt

`Script location: setup/characters/00_Korea.txt line: 22` → character 335 (reigning king at
start) set BOTH `family_name="Yi"` and `family=c:KOR.fam:Yi`. When `family` is set, the
engine ignores `family_name` and warns. Checked every other `family="c:TAG.fam:X"` usage
across `setup/characters/*.txt` (Austria, Brazil, etc. — dozens of hits): none of them also
set `family_name`; the redundant pairing was unique to this one Korea entry.

FIX: dropped the redundant `family_name="Yi"` line, keeping `family=c:KOR.fam:Yi` (the more
precise form, matching every sibling character file's convention).

### Verification

Re-ran the exact grep for each error signature against the same log after inspecting; counts
matched the task's stated occurrence counts exactly before the fix (10/10/8/6/2) — confirms
the right lines were pinned before touching anything.

### Commit

Code-review pass requested before committing (RHS-comparison-literal-only rule,
macro-void-in-LOG-string trap, BOM convention all checked — no RHS var-refs introduced, no
LOG-string macros touched, no BOM stripped/added incorrectly on the .yml loc file). The
review flagged one nit (see the "NOTE" in section 1+2 above, now corrected) with no other
findings. Rebased onto origin/merge-overnight (which had, by push time, also landed task #17's
"15 badly-read script values" pass touching some of the same 6 files below) — verified
post-rebase that neither pass's semantic intent was lost (see the addendum note directly
below this section, added after re-checking each auto-merged file). Pushed to merge-overnight.

### Addendum — post-rebase overlap check against task #17 (76770ecf4)

Task #17 landed on `merge-overnight` (as `76770ecf4`) after this fork's diagnosis but before
this fork's push, and its diff touches the same 6 files as this section (per `git diff --stat`
against the new tip). Git's line-based rebase auto-merged all six with NO conflict markers
(only `overnight/OVERNIGHT_2026_08_29.md` itself conflicted, resolved by concatenating both
forks' sections). Re-read each of the 6 files post-rebase to confirm the two passes are
compatible, not just non-conflicting:
- `se_QING_POPULATION.txt`, `se_ROW_BUILDINGS.txt`: task #17's edits landed on different
  functions/lines than this fork's `QING_pop_recompute_target` / residential-district block;
  both fixes coexist correctly in the merged file (re-verified brace balance: 169 open / 169
  close, matches pre-rebase).
- `culture_decisions/imp19c_general_culture_decisions.txt`, `00_language_groups.txt`,
  `imp19c_tooltips_l_english.yml`, `setup/characters/00_Korea.txt`: task #17's changes to
  these files are unrelated cleanups on separate lines; this fork's loc-key / family-name
  fixes are untouched by the rebase.

---

## Task #8: Full audit + fix of the "Invasion of Burma" mission tree

### Where it lives, and the reframing

Grepped `common/` for Burma / Shan States / Irrawaddy / Yunnan Base / Green Standard
Marches / Manchu Banner Elite. The ONLY real hit is
`common/missions/qing_himalaya_seasia_missions.txt` (mission `qing_himalaya_seasia_mission`),
a combined Himalaya + Southeast-Asia tree with `qing_hs_burma` as one of ~19 tasks. **None**
of the 5 named tasks (Shan States / Irrawaddy Road / Yunnan Base / Green Standard Marches /
Manchu Banner Elite) existed anywhere in the repo before this task — the brief describes an
end-state to build, not a diff against existing broken code. Design doc:
`design/DESIGN_BURMA_MISSION_TREE_AUDIT.md` (drafted, adversarially reviewed by a
general-purpose subagent, corrections resolved and appended to the same doc under
"CORRECTIONS after adversarial review").

Post-rebase onto `origin/merge-overnight`, the file had ALREADY grown 11 extra filler tasks
(`qing_hs_maritime/coastal/bhutan/sikkim/ladakh/gorkha/assam/manipur/arakan/champa/tributary_court`)
from two prior upstream-merge commits — every non-maritime one of these was pure padding
(`allow` = bare gold/PI cost, `on_completion` = flat popularity, zero tie to the named
country/territory). Folded into "audit every other task" scope.

### What shipped

1. **5 new tasks** forming the Burma campaign spine, all requiring only `qing_hs_lifanyuan`
   except where noted:
   - `qing_hs_burma_yunnan_base`: builds `fortress_building`+`military_depot_building`+
     `qing_granary_building`+`arsenal_building` (300 gold/province) at 4 confirmed CHI-core
     Yunnan provinces (2759 Yunnanfu, 723 Lingcang, 3919 Lucheng, 8725 Yuxi) = **1,200 gold**.
     `set_city_status = city` applied to the 3 non-city ones first (depot/granary both gate on
     `potential = { has_city_status = yes }`).
   - `qing_hs_burma_green_standard` (requires yunnan_base): **2,000 gold**, raises real
     Green Standard garrisons (size 6/4/4 at the 3 original Yunnan provinces) via
     `SE_qing_raise_garrison { unit = qing_green_standard }`.
   - `qing_hs_burma_banner_elite` (requires yunnan_base): **3,000 gold**, raises a real Eight
     Banners detachment (size 5 at Yunnanfu) via `SE_qing_raise_garrison { unit = qing_eight_banners }`.
   - `qing_hs_burma_shan_states`: **150 gold** + a REAL gate — `calc_true_if { amount >= 3 }`
     over 5 `OR = { owns=X  any_subject={owns=X} }` checks on the 5 Burmese-aligned Shan
     chiefdom capitals (KTG 2529, HSI 1552, MMT 9380, MPN 3752, MKN 9048). The 4 already
     CHI-aligned Shan tributaries (CHH/MLM/TNI/LSU) are deliberately excluded.
   - `qing_hs_burma_irrawaddy_road` (requires shan_states): **200 gold** + `owns = 4012`
     (Monywa) AND `owns = 6562` (Mandalay), direct ownership (not subject-held).
   - `qing_hs_burma` (final, existing id, requires all 5 above): **110 gold** (unchanged) +
     `owns = 7675` (BUR's own capital, Hanthawaddy) replacing the old `exists = c:BUR`-only
     gate (which was permanently true from turn 1 — the single worst offender in the brief).
2. **Fixed a genuine pre-existing bug**: `qing_hs_himalaya_ring` claimed p:7347 for "Sikkim" —
   that province is actually inside NEP's own `own_control_core`. Real SKK capital is p:6552.
   Fixed, plus added a real `OR = { exists c:SKK  exists c:BHU }` gate (previously none).
3. **`qing_hs_coastal`**: was a pure gold+modifier checkbox (treasury>=90, zero game-state
   tie). Now builds real `qing_coastal_battery_building` (cost 120 each,
   `potential = { is_coastal = yes ... }`) at 3 real coastal treaty ports already used
   elsewhere in this mod's OOB (Canton 9298, Fuzhou 3651, Hangzhou 8120) — cost raised to
   **360** (sum of real building costs).
4. **`qing_hs_capstone`**: had NO cost at all before. Added **treasury >= 500**.
5. **8 filler tasks + tributary_court**: each now gates on `exists = c:<TAG>` for its real
   country (BHU/SKK/ASS/MNP/ARK/CPA; Ladakh has no independent tag, gated on `exists = p:2164`
   instead; Gorkha ties to `exists = c:NEP`, since Gorkha = Nepal's ruling house, a naming
   duplicate of `qing_hs_nepal` — documented, not restructured), and `on_completion` now does
   real `FUNC_make_subject`/`add_claim` instead of a bare popularity grant.
   `qing_hs_tributary_court` gates on `any_subject = { is_subject_type = sinosphere_tributary }`.
6. Also added a real `exists = c:NEP` gate to `qing_hs_nepal` (previously missing, unlike its
   siblings Vietnam/Burma/Siam which already had this pattern).
7. New country modifiers added to `common/modifiers/qing_himalaya_seasia_modifiers.txt`:
   `qing_hs_yunnan_forward_base`, `qing_hs_shan_tributary`, `qing_hs_irrawaddy_corridor` — all
   reuse modifier-stat keys already proven elsewhere in the same file.
8. Loc: 5 new task ids + DESC + tt, ~15 new `qing_hs_needs_*_tt` gate-tooltip keys
   (`localization/english/qing_himalaya_seasia_l_english.yml`), and 4 new unit-name loc keys
   for the raised garrisons (`localization/english/imp19c_units_l_english.yml`) — required
   because `SE_qing_raise_garrison`'s `$name$` param must be a bare loc-key token, not a
   quoted string (confirmed via a header comment in `imp19c_effects_legion_setup.txt`: quoted
   multi-word strings lose their quotes on macro substitution and break the tokenizer).

### Process followed

Design doc -> adversarial review (general-purpose subagent) -> 5 BLOCKING findings resolved
(canal-depot wrong region for Yunnan, dropped; depot/granary city-status gate, fixed with
`set_city_status`; missing `$unit$` macro param on garrison calls, fixed with the confirmed
real tokens `qing_green_standard`/`qing_eight_banners`; vacuous Canton-ownership coastal gate,
replaced with a real building-construction task; the `qing_hs_ladakh`->`qing_hs_arakan`->
`qing_hs_capstone` difficulty-escalation chain, accepted and documented as an intentional
consequence of giving `qing_hs_burma` real teeth) -> implemented -> code-review pass
dispatched on the diff (see notification when it lands) -> this log entry.

### ASSUMPTIONS & GUESSES (invented numbers, no boot data to tune against)

1. **Green Standard Marches / Manchu Banner Elite baseline cost**: no such task ever existed
   to read a "current" value from. Used the tree's own filler-task tier (~20-30 gold/PI,
   e.g. `qing_hs_bhutan`'s `political_influence >= 20`) as the stand-in "current cheap cost",
   ×100 => 2,000 / 3,000. Purely a judgement call.
2. **Shan States majority threshold = 3 of 5** capitals, not all 5 (too strict) or 1 (too
   loose) — no boot data to tune against.
3. **Yunnan Base = 4 provinces** (not 3): the extra province (8725, Yuxi) was added
   specifically to clear a 4-digit total after the canal-depot building was dropped
   (region-gated, wrong for Yunnan) during adversarial review — otherwise 3×300=900 would
   fall short of "the thousands" the brief asked for.
4. **Green Standard sizes 6/4/4, Banner Elite size 5**: chosen to echo (not copy) the boot
   seed's own relative sizing convention; not derived from any specific historical source.
5. **Coastal battery provinces (Canton/Fuzhou/Hangzhou)**: assumed `is_coastal = yes` for all
   3 based on their established use as real treaty-port banner-garrison locations elsewhere
   in the mod; not independently re-verified against the map's coastal flag.
6. **All new treasury figures (1200/2000/3000/150/200/360/500) are unverified against actual
   play-balance** — no boot log available for this file. Flagged for later tuning.
7. **Ladakh has no independent country tag** in this setup (verified by grep for `LEH`/`LAD`);
   kept as a province-only gate (`exists = p:2164`), matching the tree's own pre-existing
   treatment of Ladakh in `qing_hs_himalaya_ring`.
8. **Hanoi (p:3418) / TRH mismatch**: pre-existing, not introduced by this task — documented
   with a code comment at `qing_hs_vietnam`'s Hanoi claim line, not fixed (out of scope).

Committed to `merge-overnight` after rebasing onto the latest tip (verified `git config
user.email` = `freekumquats@users.noreply.github.com` before committing).

### Task #8 addendum: adversarial code-review verdict + post-review fixes

Independent code-review agent reviewed the full diff (all 4 changed files) plus every
externally-referenced token (tags, provinces, buildings, effects, loc keys) against the
repo. **Verdict: no BLOCKING issues.** 4 non-blocking findings, resolved as follows:

- MEDIUM (missing modifier loc for the 3 new modifiers) — FIXED: added name + `_desc`
  keys for `qing_hs_yunnan_forward_base`/`qing_hs_shan_tributary`/`qing_hs_irrawaddy_corridor`
  to `qing_himalaya_seasia_l_english.yml`.
- LOW/cosmetic (loc said "Mone" for MPN, `00_default.txt` says "Mongpan") — FIXED in
  `qing_hs_burma_shan_states_DESC`.
- LOW (mission-raised garrisons don't get the boot-only `qing_garrison_supply` attrition
  immunity stamp) — ACCEPTED, not fixed: fixing it would mean re-invoking the shared,
  proven `SE_qing_stamp_garrison_supply` effect from mission code, risking a double
  `add_unit_modifier` application on the ~26 existing OOB garrisons (dedup behaviour
  unverified); the new garrisons sit at interior Yunnan provinces, not the ~0-food-surplus
  frontier seats the supply fix targets, so impact is expected low. See design doc section 9.
- LOW (unverified `is_coastal` at Hangzhou p:8120) — ACCEPTED as correct: same assumption
  already logged as guess #5 above; not independently re-verifiable from text files (map
  geometry primitive), and consistent with the mod's own existing Hangzhou coastal-garrison
  lore/comments.

Full reasoning logged in `design/DESIGN_BURMA_MISSION_TREE_AUDIT.md` section 9.
# Overnight 2026-08-29 — Tasks #2/#6/#7: GC gender gate, Appoint cost, Works autofill

## Task #2 — gender-eligibility bug + missing law-tooltip post lists

Three separate gaps, all under the same Women's Rights law-tier eligibility model
(`QING_char_gc_office_sex_eligible`, qing_dynasty_triggers.txt): LOWER tier (censor,
lifanyuan, chamberlain, zongli, grand_secretariat, guard_commandant) needs
`women_limited_legal_rights`+; UPPER tier (personnel, revenue, rites, war, justice,
works) needs `women_equal_legal_rights`+; chancellor needs `womens_suffrage_law`;
Imperial Clan women are exempt from all tiers.

1. **GC autofill backfill draw had no sex gate at all.** The player-facing picker
   already enforced the tier map, but `QING_council_autofill_office`'s own two
   `ordered_character` draw branches (common/scripted_effects/se_QING_COUNCIL.txt)
   had none — a country whose law was still at a restrictive tier could have the
   death/departure backfill draw seat an ineligible woman into a great office with
   no player click involved. Fixed by seeding a dedicated country-scope scratch var
   (`qing_autofill_office_var`, NOT the shared picker var — reusing that would
   corrupt a concurrently-open player picker session) and inlining the identical
   tier-map OR-block into both draw branches, re-anchored on `scope:qing_autofill_
   country` (this function's own established pattern, since ROOT is the dying/
   accused character on the runtime backfill path, not CHI).
2. **The four frontier/customs superintendency auto-picks had no sex gate either**
   (Hoppo, Salt Commissioner, Caravan Superintendent, Opium Commissioner —
   se_QING_CANTON/SALT/CARAVAN/OPIUM.txt). Each office's `_appoint` auto-pick
   (used by boot-seed/backfill/rotate/AI callers, distinct from the player picker
   list already gated by a prior fix) got the same LOWER-tier OR-gate. Each
   office's periodic reconcile pulse also got a self-correcting eviction clause
   (a woman holder whose country's law has since regressed below the tier, or who
   was seated before the gate existed, is relieved and backfilled within the same
   pulse — mirrors the existing double-book self-heal already proven for these
   posts).
3. **Law-tooltip post lists were missing.** The 4-tier `womens_law` option
   (common/laws/00_social_laws.txt) gates office/exam eligibility across the whole
   mod but never told the player WHICH posts a tier change opens or closes short of
   reading script. Added `custom_tooltip` on `on_enact` for all four tiers, with new
   loc keys in localization/english/laws_l_english.yml enumerating exactly which
   offices/exams/superintendencies each tier unlocks.

## Task #6 — GC Appoint charged the same PI as Replace

`qing_gov_office_appoint_selected` (common/scripted_guis/QING_governance_actions.txt
— confirmed via gui/imp19c_windows.gui:92 onclick grep as the only LIVE appoint
action; the 12 individual `qing_gov_office_appoint_<office>` scripted_guis in the
same file are dead/unreferenced legacy code from before the shared-picker redesign)
charged a flat PI cost (chancellor 20, others 15) unconditionally on every
appointment, with no distinction between filling a vacant seat (Appoint) and
evicting a sitting minister (Replace). Fixed by folding a
`has_variable = qing_office_$office$_holder` vacancy check — evaluated BEFORE the
`QING_office_appoint` call, since that call is what sets the holder var to the new
appointee — into each of the 13 existing per-office dispatch branches. PI is now
only charged when a holder already existed at click time.

## Task #7 — GC autofill not filling vacant Minister of Works

Could not reproduce or locate a Works-specific defect via static analysis, despite
an exhaustive pass: every call site in se_QING_COUNCIL.txt (boot mint, backfill
refill_vacant_seats, death-dispatch backfill, prune_seat, prune_all_seats, score_office,
relieve_double_booked_office) parametrizes works identically to its 12 sibling great
offices — same domain (finesse, shared with personnel/revenue/censor), same degree
(jinshi), same degree_hard flag, same exclusion clauses. Cross-file audit of every
read/write of `qing_office_works_holder` repo-wide (se_QING_WORKS/CANAL/MINISTRY/
SELFSTR.txt, qing_works_events.txt, FlavorEvents.txt, qing_war_events.txt,
qing_personnel_events.txt, QING_works_ministry_panel.txt) found the variable is ONLY
ever set/cleared by the generic `QING_office_appoint`/`QING_office_vacate` macros —
no rogue file clears it directly. GUI row bindings (gui/government_view.gui lines
3743-3963, the Works card) are structurally identical to its sibling justice/censor
rows — datacontext, the FILLED/.IsSet visibility binding, and the VACANT/Not(.IsSet)
binding all correctly reference `qing_office_works_holder`, not a copy-paste'd
sibling var. A weak hypothesis (Works minister getting evicted via a has_tech_office/
Researcher conflict specific to Self-Strengthening) was checked and found NO
supporting code — `has_tech_office` is a bare vanilla trigger read-only everywhere in
this mod, never granted by any Qing effect.

Given static analysis is exhausted with no Works-SPECIFIC defect found, and
`QING_council_autofill_office` — despite being the most complex function in this
file — had NO se_LOG wiring at all (unlike every sibling council function), wired
LOG_enter/exit and three LOG_line checkpoints (draw succeeded / falling to mint /
still vacant at exit, each stamped with office+source) so any future boot log shows
directly which branch fires for works, closing a genuine gap against the standing
error-logging convention regardless of the diagnosis below.

**Root cause found on a second pass, re-reading the draw's own eligibility limit
against `QING_char_holds_court_position`'s own header comment**
(qing_dynasty_triggers.txt:271-274): that trigger deliberately does NOT test
`has_variable = qing_office_held`, by design — so the PLAYER PICKER can still offer a
sitting GC officer as a reshuffle target. But the AUTOFILL DRAW (a completely
different call path, never player-initiated) inherited that same omission with no
substitute check anywhere else in its limit — so nothing excluded a candidate who
ALREADY holds a different great office from being drawn again for a second one.
`QING_council_refill_vacant_seats` calls `QING_council_autofill_office` for all 13
offices every pulse in one fixed sequence (chancellor, personnel, revenue, rites,
war, justice, works, censor, lifanyuan, chamberlain, zongli, grand_secretariat,
guard_commandant); ten of those (every civil office except war/guard_commandant)
share the identical pool + `order_by = combined_stats_council_svalue` ranking. When
two or more of these were simultaneously vacant in the same pulse, the single
top-ranked candidate would be drawn and appointed to the FIRST vacant office in
sequence, then drawn AGAIN (still ranked #1, still not excluded) for the NEXT vacant
office later in the sequence — and `QING_office_appoint`'s own "already holds a
different office, relieve him first" rule (its header comment, se_QING_COUNCIL.txt)
would evict him from the seat this exact sweep gave him one call earlier, with no
later call in the sweep ever revisiting that now-re-vacated seat. `works` sits
mid-sequence, so any of the 4 civil offices called after it (censor, lifanyuan,
chamberlain, zongli, grand_secretariat) could silently steal its freshly-drawn man
every pulse this condition recurred — exactly matching "Works never stays filled."

**Fix applied**: added `NOT = { has_variable = qing_office_held }` to both draw
branches' (hard-civil and soft-martial) eligibility limit, right after the existing
`has_any_office = no` vanilla-office exclusion. Scoped automatically to the backfill
draw only (the boot mint path never reaches this branch at all, per the
`autofill_source` gate already documented at this function's top) — a departing
holder's own `qing_office_held` is already stripped by `QING_office_vacate` before
this draw runs, so the exclusion only ever removes OTHER currently-serving officers
from the pool, which is the intended behaviour (autofill should seat an unassigned
courtier, not cannibalize a sibling seat).

Not boot-verified (no boot test available in this worktree-isolated pass); the
diagnostic LOG_line checkpoints already wired above will confirm on the next boot
whether this closes the symptom, per the "ship the best-guess fix now, tune from the
log after" overnight contract — this is not treated as a reason to withhold the fix.

## Adversarial self-review
- Verified brace balance on both edited files before and after every edit
  (se_QING_COUNCIL.txt: 1141/1141 after the diagnosis pass, 1143/1143 after the
  cascade-eviction fix's two `NOT` blocks; QING_governance_actions.txt: unchanged
  from its prior verified-balanced edit).
- Considered whether excluding existing office-holders from the draw could ever
  strand a seat with NO eligible candidate, forcing an unwanted mint when a
  reshuffle-style draw was actually intended: no — the draw is backfill-only
  (never runs at boot, where everyone is unassigned anyway), and the mint fallback
  already exists specifically to cover an empty draw pool, so this is a no-op
  safety net, not a new failure mode.
- Task #6's vacancy check reads the holder var strictly before the `QING_office_
  appoint` call that overwrites it — confirmed by re-reading the macro's own
  definition (:1868 area), not just assumed from call order.
- Considered whether a same-seat "reshuffle" (reappointing the current holder to his
  own office) would be miscategorized as Replace and charged PI unnecessarily — this
  is unreachable through the live picker's own is_valid gate (a sitting holder is not
  offered his own seat as a target), so not a real-world edge case worth a special
  case.
- No boot test available in this pass (worktree-isolated, static-analysis-only
  session); per the no-bisection / "guess, build, log" contract this is not treated
  as a blocker for tasks #2/#6, which are pure logic-gate additions matching proven
  idioms already battle-tested elsewhere in this codebase.

## Task #1 + Task #3 — exhaustive event-tooltip quantification sweep

Contract: every event OPTION that grants a magnitude-bearing effect must show it
in the tooltip as an own-line, precisely-quantified, signed entry
(`#COLOR Label: sign N#!`). Full manual sweep of all files under
`events/imp19c_mod_events/**/*.txt` (70 files), no grep-sampling.

### Known-bad targets (fixed first, per the brief)

1. **"Tribute Embassy at Peking"** — no exact title match exists anywhere in the
   repo. Identified as `qing_rites.2` ("A Tributary Embassy",
   `events/imp19c_mod_events/qing_rites_events.txt`), whose `desc` explicitly
   places the embassy "at the capital" and whose original tooltips were vague
   and unquantified — the closest and only defect-matching event.
   Fixed all 4 events / 11 options in
   `localization/english/qing_rites_l_english.yml`, tracing every option to its
   real magnitude in `common/scripted_effects/se_QING_RITES.txt` and
   `common/modifiers/qing_rites_modifiers.txt`.

2. **"Palace Examination"** = `qing_keju.2`
   (`events/imp19c_mod_events/qing_keju_events.txt`), loc in
   `localization/english/qing_office_events_l_english.yml` (namespace does not
   map 1:1 to the event filename). Fixed both options. Option B's original
   text falsely claimed "as above" benefits (experience / charisma-finesse
   cultivation / loyal veterans) that its actual effect code does not grant —
   corrected the factual claim, not just the quantification.

### Sweep method

70 files split into 7 batches of ~10 files each, dispatched as parallel
background agents, each given the same method and the same reference commits
(`a947cec0c`, `24f8c44e0`, `ca00a4a53`) as the tooltip-format template.
Batches 1, 3, 4, 5, 6, 7 ran as independent background agents. Batch 2 (10
files) was swept directly:

| File | Options checked | Fixed |
|---|---|---|
| diplomatic_play/head_of_state_visit_play_area.txt | 0 | 0 (empty stub) |
| diplomatic_play/minor_border_discussion.txt | 3 | 3 |
| diplomatic_play/send_settlers.txt | 3 | 3 (+1 key-repoint fix, see below) |
| economy/DEBT_events.txt | 1 | 0 (no custom_tooltip; auto-render correct) |
| economy/ECON_events.txt | 2 | 0 (no numeric custom_tooltip effects) |
| economy/cost_of_living_events.txt | 8 | 0 (no custom_tooltip) |
| economy/currencies_list.txt | 0 | 0 (no options) |
| economy/ev_WEALTH_setup.txt | 0 | 0 (no options) |
| economy/shortage_events.txt | 2 | 0 (no custom_tooltip) |
| japan_bakumatsu_events.txt | 15 | 0 (see note) |

**japan_bakumatsu_events.txt note:** every option in this file relies on
`JPN_baku_nudge` (a plain `change_variable` counter on custom country
variables — `baku_legitimacy`, `imperial_prestige`, `domain_sonno`), never
wrapped in a `custom_tooltip`. Custom variable changes are not auto-rendered
by the engine, so in isolation this would be a hidden-effect defect. But the
file's own header marks this sequence AI-autonomous (Japan/TKG walks this arc
without player input, matching the established pattern already used
elsewhere for the USA/Mexico AI-autonomous arcs) — the option text is never
shown to a human player in the normal course of play. Left as-is; not a
tooltip defect under this contract. Flagged here for visibility rather than
silently skipped.

### Bugs found and fixed beyond pure quantification

- **`send_settlers.1.a`** (`events/imp19c_mod_events/diplomatic_play/send_settlers.txt`):
  `custom_tooltip` pointed at `diplomatic_play.1.a.tt`, a key that actually
  describes a *different* event's option
  (`diplomatic_play_events.txt`'s own `diplomatic_play.1.a`, which calls
  `POLITICS_upset_pacifists` + a dynamic treasury cost — nothing to do with
  settler movement). Repointed `send_settlers.1.a` to a pre-existing, unused
  key `send_settlers.1.a.tt` and filled it in with send_settlers' real
  effects (pop move, `hindered_in_play` opinion, aggressive expansion,
  large play progress). `diplomatic_play_events.txt`'s own
  `diplomatic_play.1.a.tt` still needed its own fix for its own effects —
  handled by whichever batch covers that file (it was in batch 1's file list).

- **`qing_keju.2.b.tt`**: corrected a factual overstatement (see above).

### Assumptions & guesses

- Treated "Tribute Embassy at Peking" as `qing_rites.2` on content-match
  grounds (capital-embassy framing + vague-tooltip defect profile), since no
  literal title match exists. Confidence: high, but not a citation match.
- Treated files with zero `custom_tooltip` usages as zero-fix by default
  (engine auto-tooltip is correct for native stat effects), with one
  exception carved out: options whose only effects are custom-variable
  nudges AND that are genuinely player-facing would need a retrofitted
  custom_tooltip. Applied this exception check to `japan_bakumatsu_events.txt`
  and concluded (AI-autonomous, not player-facing) no fix is needed. This
  same exception should be kept in mind by other batches if they hit similar
  `_nudge`-only, no-custom_tooltip files.
- Did not touch `qing_embassy_l_english.yml` — already fixed, in conformant
  state, by a parallel process before I reached it.

### Batch 3 (10 files, swept directly — not delegated to a background agent)

| File | Options checked | Fixed |
|---|---|---|
| mex_instability_events.txt | 25 | 0 (no `custom_tooltip` anywhere) |
| noble_titles.txt | 0 | 0 (3 hidden events, no options) |
| office_eligibility_events.txt | 0 | 0 (1 hidden event, no options) |
| political/politics_events.txt | 2 | 0 (no `custom_tooltip`) |
| qing_accountability_events.txt | 3 | 3 |
| qing_advisor_events.txt | 5 | 1 (`.2.a`; the other 4 only set a pending-field flag, no magnitude in that option itself) |
| qing_amban_events.txt | 8 | 8 |
| qing_censorate_events.txt | 12 | 12 (`.1`–`.4`, 4 events × 3 options; this branch has no `.11` officeholder-split variant) |
| qing_character_events.txt | 8 | 8 (`qing_char.10/.11/.20/.21/.22`, loc lives in `qing_mechanics_l_english.yml`) |
| qing_culture_events.txt | 21 | 12 (loc in `qing_culture_l_english.yml`; the other 9 options were flat treasury/PI grants already correctly quantified) |

Traced magnitudes via `se_QING_CENSORATE.txt` (`QING_censorate_impeach_uphold/suppress`),
`se_QING_AFFINITY.txt` (`QING_char_cleanse` corruption -20, `QING_char_taint` corruption +20),
`se_QING_MECHANICS.txt` (`QING_char_shift_identity`, a signed Manchu-identity meter — colored
neutral `#Y` since it is a roleplay axis, not inherently good/bad), `common/loyalty/*.txt`,
and `common/modifiers/qing_censorate_modifiers.txt` / `qing_governance_modifiers.txt` /
`qing_culture_modifiers.txt` / `qing_mechanics_modifiers.txt` for every named modifier's real
sub-effects. Confirmed the polarity convention empirically from already-fixed
`qing_decline.*` tooltips in `qing_mechanics_l_english.yml`: colour follows each stat's own
good/bad sense (e.g. Corruption/Tyranny/Ethnic Tension/Banner Decay/Reform Pressure are "bad"
stats — a decrease is `#G`, an increase is `#R` — while Loyalty/Popularity/Stability/
Legitimacy/Prestige/Political Influence/Treasury are "good" stats scored by raw sign), not a
flat sign-only rule.

No bugs beyond quantification found in Batch 3's files.

### Batch 1 (10 files, background agent)

51 options checked, 29 fixed. Files: AI_notification_events.txt (0/0, no
custom_tooltip), ChineseEvents.txt (0/0), FlavorEvents.txt (1/1),
NameChangeEvents.txt (20/0, pure flavor no magnitudes), currency_crisis_events.txt
(3/3), custom_window_events.txt (0/0), diplomatic_play/agadir_crisis_type.txt
(8/8 — 1 corrected + 7 missing loc entries created), diplomatic_play/exile_pops_to_play_area.txt
(0/0, stub), diplomatic_play/agitator_sponsorship.txt (8/8),
diplomatic_play/diplomatic_play_events.txt (11/9).

**Bugs found beyond quantification:** `agitator_sponsorship.txt` had an
inverted-label bug — the shared keys `sponsorship_discovered` /
`sponsorship_remains_secret` had their text swapped, and the same shared keys
carried different magnitudes across two parent options. Split into
option-specific keys (`.1.a.discovered/.remains_secret`,
`.1.b.discovered/.remains_secret`) and repointed all 4 `custom_tooltip`
call-sites; also corrected `.2.a.tt`'s opinion magnitude (-30/10yr claimed vs.
real -20/decay-5). `diplomatic_play_events.txt` (loc lives in
`mod_events_l_english.yml`, not a same-named file) had 3 structural bugs:
`diplomatic_play.4:t:0` (colon typo — title key never resolved),
`diplomatic_play_4.a:0` (underscore typo — button label never resolved), and
a duplicate `diplomatic_play.3.b:0` key that overwrote the button label with
tooltip prose instead of using `.tt`. All three fixed.

### Batch 4 (10 files, background agent)

96 options checked, 94 fixed (2 left as-is — genuinely effect-free flavor
tooltips: `qing_ethnic_tension.2.b`, `qing_household.3.c`). Files:
qing_decline_events.txt (13/13), qing_embassy_events.txt (12/12),
qing_ethnic_tension_events.txt (7/6), qing_frontier_migration_events.txt
(16/16), qing_frontier_sea_events.txt (11/11), qing_golden_urn.txt (3/3),
qing_greatgame_events.txt (8/8), qing_household_events.txt (11/10),
qing_ili_events.txt (8/8), qing_integration_capstone_events.txt (7/7).

**Bugs/normalizations found:** self-caught a percentage-vs-flat mislabeling
(`global_monthly_state_loyalty = 0.05` is a flat per-month increment, not a
percent — corrected in 2 files before finalizing). `qing_integ_capstone_l_english.yml`
used non-standard `§Y...§!` placeholder syntax throughout — normalized to the
engine's `#COLOR...#!` convention. `qing_ili_events.txt` had zero quantified
bracketed lines anywhere (only inline `#Y/#G/#R` prose highlighting) — fully
rewritten, tracing magnitudes through `se_QING_ILI.txt` and
`qing_ili_modifiers.txt`.

### Batch 5 (10 files, background agent)

105 options with `custom_tooltip` across the batch; 67 needed fixing.
Task #3 target `qing_keju_events.txt` confirmed intact (only `.2` in scope,
already fixed pre-dispatch); `qing_rites_events.txt` confirmed intact
(already fixed pre-dispatch). Files: qing_japan_preperry_events.txt (5/0,
already correct), qing_justice_events.txt (8/0, already correct),
qing_legation_events.txt (7/2), qing_mexico_adventure_events.txt (2/2),
qing_missionary_events.txt (2/2), qing_napoleon_events.txt (12/12 of 15
quantifiable; 3 pure-narrative options correctly untouched),
qing_office_events.txt (29/29), qing_personnel_events.txt (12/12),
qing_pilgrimage_events.txt (8/8 of 9 quantifiable; 1 no-magnitude option
correctly untouched).

**Flagged, NOT fixed (out of scope for a tooltip-only pass — new backlog
item):** `se_QING_DIPLO.txt`'s `QING_gp_side_with_france` →
`QING_gp_accommodate(power=france)` passes a *positive* amount into
`QING_DECLINE_nudge`, whose own header comment says a negative amount lowers
tension — so `qing_napoleon.2.e` ("side with France") appears to *raise*
France's tension by its literal code, contradicting the option's flavor text
("warm relations with France"). The tooltip was written to state the literal
net effect (+6, as the code actually does it) with an explicit in-text
"Note:" flag, rather than silently mis-describing it — but the underlying
script sign bug itself was NOT touched (bug-vs-tooltip scope boundary).
**This should be picked up as a follow-up correctness bug**, not closed by
this sweep. Also normalized `qing_pilgrimage_l_english.yml`'s non-standard
`§`-color codes to the standard `#` codes.

### Batch 6 (10 files, background agent)

Totals: qing_rebellion_events.txt (8/8 — mislabeled "qing_rites_events.txt"
in the agent's own report table, verified via `git diff --stat` that
`qing_rites_l_english.yml` carries only this session's earlier 22-line edit
and no further change, so no collision occurred), qing_reform_events.txt
(24/24), qing_regency_events.txt (8/8), qing_revenue_events.txt (13/13, +1
malformed loc-key fix), qing_roster_events.txt (~48/~48),
qing_students_events.txt (6/5), qing_subject_integration.txt (13/13),
qing_summer_palace_events.txt (5/5), qing_techtransfer_events.txt (6/6),
qing_treaty_events.txt (6/6). Final `rg` sanity pass across all batch-6 loc
files for good/bad-vs-sign convention: zero violations found.

### Batch 7 (9 files, background agent)

37 options checked, 36 fixed. Files: qing_uscw_events.txt (4/3),
qing_vassal_events.txt (8/8), qing_war_events.txt (12/12),
qing_works_events.txt (13/13), the 4 tyranny_and_stability_events/*.txt files
(0/0 each — only event-idea comments, no real events), usa_section_events.txt
(0/0 — 596 lines / 24 options, zero `custom_tooltip` keys anywhere; correctly
left untouched per the no-add rule).

**Bugs found:** `qing_vassal_events.txt`'s 4 `.abandon` tooltips falsely
claimed a "legitimacy" hit that `QING_vassal_abandon` never actually applies
— dropped the false claim rather than quantifying a number that doesn't
exist. `qing_works_events.txt`'s three `QING_works_build_*` effects have a
two-axis cost/corruption structure gated on minister finesse (≥9 / 7-8 / <7)
independent of the option's own `cheap` flag — rewritten as "If finesse
≥9/7-8/below 7" conditional branches rather than collapsed to one number.

### Final tally

| Batch | Files | Options checked | Options fixed |
|---|---|---|---|
| Known-bad targets (pre-dispatch) | 1 (qing_rites, 4 events) + qing_keju.2 | 13 | 13 |
| 1 | 10 | 51 | 29 |
| 2 | 10 | 34 | 6 |
| 3 | 10 | 84 | 44 |
| 4 | 10 | 96 | 94 |
| 5 | 10 | 105 | 67 |
| 6 | 10 | ~137 | ~136 |
| 7 | 9 | 37 | 36 |
| **Total** | **70/70 files swept** | **~557** | **~425** |

Every file under `events/imp19c_mod_events/**/*.txt` (70 files, verified via
`fd '\.txt$' events/imp19c_mod_events`) was opened and read in full, and every
`option = {}` block with a `custom_tooltip` was checked against the
own-line-quantified-signed-entry convention. ~425 options were rewritten to
conform; the remainder were either already conformant, had no
`custom_tooltip` (engine auto-tooltip already correct — not touched, per the
no-add rule), or genuinely had no numeric magnitude to quantify.

### New backlog item raised by this sweep

- **`QING_gp_side_with_france` tension-sign bug** (`common/scripted_effects/se_QING_DIPLO.txt`):
  passes a positive amount to `QING_DECLINE_nudge` for France's tension where
  the intent (per the function's own header comment and the option's flavor
  text) is to lower it. Not fixed here — tooltip pass only touches loc, not
  script logic. Needs a follow-up correctness fix.

### Code-review findings & dispositions

The `code-review` subagent returned 5 findings on the full diff. Each was
independently re-verified against the actual on-disk source (not taken on
trust) before disposition:

1. **BOM handling in `localization/english/*.yml`** — verified via `xxd` that
   every edited loc file still opens with the required UTF-8 BOM (all edits
   used the `Edit` tool, never `Write`, per the standing project rule).
   **No action needed.**
2. **`send_settlers.2.b.tt` Play Success color polarity** — confirmed by
   reading `events/imp19c_mod_events/diplomatic_play/send_settlers.txt` in
   full: event `send_settlers.2` is explicitly POV = target/defender
   country (see its own header comment), and option `.2.b` ("Drive them out!")
   applies `DIPLOMACY_progress_play = { success = -10 ... }`, which reduces
   the INSTIGATOR's play success — a favorable outcome from this event's own
   POV. This exactly mirrors the already-correct `agitator_sponsorship.2.a.tt`
   (-15, `#G`). The tooltip had it as `#R`, which was the wrong polarity.
   **FIXED**: changed `#R Play Success: -10#!` to `#G Play Success: -10#!` in
   `localization/english/mod_events_l_english.yml`.
3. **Nominal vs. power-balance-scaled "Play Success" values** — `DIPLOMACY_progress_play`
   (`common/scripted_effects/se_DIPLOMACY.txt`) multiplies the raw `success=N`
   argument by a power-balance factor (`2 - 1/balance`, floored 0.25, clamped
   to [0,100]) before applying it, so the number in `success=N` is a base/nominal
   value, not always the literal applied delta. This is upstream engine/script
   behavior common to every diplomatic-play tooltip across the mod, not a
   defect introduced or touched by this sweep, and re-deriving the actual
   applied value per-option is outside the scope of a tooltip-format pass.
   **WONTFIX for this task** — logged here as a known caveat rather than
   silently dropped. A follow-up could reword the label to "Play Success (base): N"
   mod-wide if this is judged worth the churn.
4. **`agitator_sponsorship.txt` case-mismatched script values** —
   `TYRANNY_SMALL` / `SUBTRACT_POPULARITY_SMALL` (uppercase, inside option
   `.5.a`, which has no `custom_tooltip`) don't match the actual lowercase
   definitions in `common/script_values/00_character_stats.txt`
   (`tyranny_small = 1`, `subtract_popularity_small = -5`), so both effects
   were silently no-oping (case-sensitive script_value resolution).
   **FIXED**: lowercased both references in
   `events/imp19c_mod_events/diplomatic_play/agitator_sponsorship.txt`
   (lines ~691-694).
5. **4 dead/unreferenced `.tt` loc keys** (`agitator_sponsorship.2.b.tt`,
   `.2.c.tt`, `.5.a.tt`, `.5.b.tt`) plus one malformed markup fragment inside
   `.2.c.tt` (`#R Lose #R @prominence! -20#! #!` — doubled opener, stray
   closer) — verified via `git show HEAD:localization/english/mod_events_l_english.yml`
   that all 5 are pre-existing (predate this sweep, not introduced by it).
   The 4 options these keys would belong to have no `custom_tooltip` at all
   (confirmed in `agitator_sponsorship.txt`), so per this task's own "no-add"
   rule they were correctly left untouched by the sweep itself. **Logged as
   a pre-existing backlog item**, same disposition class as the
   `QING_gp_side_with_france` sign bug above — not fixed here, flagged for a
   separate cleanup pass (dead loc keys can simply be deleted; the malformed
   fragment only matters if a future fix ever wires up `.2.c.tt`).

### Status: COMPLETE

All 70/70 files swept. Code-review dispatched on the full diff (41 files
changed). All 5 findings triaged above: 2 fixed directly (Findings 2 and 4),
1 required no action (Finding 1), 2 logged as pre-existing out-of-scope
backlog items rather than silently dropped (Findings 3 and 5). Proceeding to
final commit + push to `merge-overnight`.

## Merge — landing the sweep fork's stranded commit onto the current tip

The `event-template-sweep` fork built commit `815020069` on a base 1719 commits
behind the live `origin/merge-overnight` tip (`fe6c274ab`). Rather than rebase
blind, merged the fork's commit into the current tip and resolved every
resulting conflict by hand, file by file (plus this doc's own `AA` conflict).

Method (same for all ~41 conflicted loc files): never `git checkout --ours`/
`--theirs` on a whole file — that discards content the 3-way merge already
combined cleanly elsewhere in the same file. Instead, for every conflicted
tooltip, traced the real event option in `events/imp19c_mod_events/*.txt`,
followed any scripted-effect call into `common/scripted_effects/se_QING_*.txt`,
and resolved named modifiers/loyalty/opinion refs against their real magnitude
in `common/modifiers/*.txt`, `common/loyalty/00_imp19c_loyalty.txt`, or
`common/opinions/imp19c_opinions.txt`. Extra content present on only one side
was checked against source before keeping or discarding it (live option vs.
resurrected dead code).

This caught real, recurring errors that predate the fork's stale base:
- **Wrong treasury/gold costs** in the large majority of conflicted options —
  the fork's numbers were consistently a rebalance-cycle out of date (e.g.
  -60 vs. real -310, -100 vs. real -400, -250 vs. real -630).
- **"Prestige" mislabeling** — repeated across a dozen+ files, where the real
  effect is `add_legitimacy`, not prestige. This looks like a systemic
  copy-paste habit in the stale fork's tooltip authoring.
- **Stale mechanics resurrected** — several tooltips claimed hard numbers for
  "Bureau Capacity" or similar nudges that a later `[meter-concretize #1
  2026-08-06]` refactor deliberately removed in favour of a concretely
  derived value; those claims were dropped rather than "fixed" with a number.
- **Illegal loc-scope syntax** `[scope:X.GetName]` (must be bare `[X.GetName]`)
  reintroduced by the stale fork in several files.
- **Dropped live options** — the stale fork's tooltips were missing whole
  options (e.g. garrison/amban-negotiation branches) that exist live in
  current source; restored from the current-tip side rather than losing them.

Resolved via 1 direct pass (`qing_greatgame`, `qing_household`, `qing_ili`,
`qing_integ_capstone`) plus 4 parallel forks (4 files each) applying the same
methodology to the rest: `qing_justice`, `qing_legations`, `qing_migration`,
`qing_office_events`, `qing_personnel`, `qing_pilgrimage`, `qing_rebellion`,
`qing_revenue`, `qing_roster`, `qing_subject_integration`, `qing_techtransfer`,
`qing_treaties`, `qing_vassal`, `qing_war`, `qing_works`, `qing_mechanics`.
Zero conflict markers remain in any file; every resolution is source-verified,
not guessed. Proceeding to final review + commit + push.

### Post-merge code review — 4 findings, all fixed

Dispatched a code-review pass on the full staged diff (independent re-verification
against source, not trusting the resolution commit claims). Also caught, in the
same automated pass beforehand, illegal `[scope:X.GetName]` loc syntax the
batch forks had missed in `qing_napoleon` and `qing_office_events` (fixed:
bare `[X.GetName]`).

The review's 4 findings, all fixed:
1. **`qing_roster.19.b.tt`** — phantom `Bureau Capacity: +6` claim for a nudge
   the `[meter-concretize #1]` refactor already removed. Line deleted.
2. **`qing_students.10.defend.tt`** — "Prestige: +15" mislabeled; source is
   `add_legitimacy = 15`. Relabeled to Legitimacy.
3. **`qing_napoleon.2.e.tt`** — a developer review note ("flagged, not
   corrected, in this tooltip pass...") had leaked into player-facing text,
   and the France-tension rise was colored green (`#G`) instead of red
   (`#R`). Note stripped, color fixed to `#R`. The underlying script sign
   bug (`QING_gp_side_with_france` in `se_QING_DIPLO.txt`) that causes the
   rise remains the already-logged separate follow-up above — not touched
   here (tooltip-vs-bug scope boundary).
4. **`qing_censorate.2.a.tt`** — the same stat ("His Popularity") listed
   twice back-to-back (+20 then +10) instead of once (+30); both numbers
   were individually correct against source, just confusingly split.
   Consolidated to one `+30` line.

No other issues found: no remaining illegal scope syntax, no unbalanced
quotes/broken escapes, no resurrected dead mechanics, no silently-dropped
live options. Proceeding to commit + push.
