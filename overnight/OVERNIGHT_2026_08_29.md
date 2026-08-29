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
