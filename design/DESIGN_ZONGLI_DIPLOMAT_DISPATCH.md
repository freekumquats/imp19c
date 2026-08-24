# DESIGN: Dispatch a Zongli Yamen Diplomat to a Diplomatic Play

Status: READY TO IMPLEMENT. Two adversarial review rounds complete (resolution logs in
sections 7 and 8); all findings from both rounds folded in.

## 1. User request (verbatim, across the turn)

1. "diplomatic plays should have a button under Support and above Cancel to dispatch a
   diplomat character from the Zongli Yamen"
2. "a dispatched diplomat should be clearly labelled as such on the Zongli Yamen window"
3. "only one diplomat can be dispatched to one play at a time"
4. "it should increase the chances of success and also trigger some events (based on the
   diplomat's skills) which either increase or decrease chances of success"

## 2. What already exists (read from disk, not assumed)

- **Diplomatic play provobj** (province scope): `is_diplomatic_play`, `play_instigator`,
  `play_target_country`, `play_target_area`, `play_goal`, `diplomatic_play_success` (0-100),
  `diplomatic_play_progression`. Torn down through exactly one chokepoint,
  `AI_remove_diplomatic_play` (se_AI.txt:887), called from every path a play can end
  (se_DIPLOMACY.txt:257/719/1554 resolve/collapse/timeout, EE_scripted_guis.txt:1377/1652
  manual actions incl. Cancel, diplomatic_play_events.txt:649 event-driven end).
- **Support/Cancel buttons** (gui/shared/gui_templates.gui: Support at :3821/:4139, Cancel at
  :3837/:4155 — two identical blocks, one per play side) call `DIPLO_player_support_play` /
  `DIPLO_player_cancel_play` (EE_scripted_guis.txt:1586-1654), each a scripted_gui scoped to
  the play provobj with `scope:player` = the acting country. [REVIEW-FIX] corrected: `Oppose`
  (`DIPLO_player_oppose_play`) is NOT wired into this GUI block at all — it exists as a
  scripted_gui (EE_scripted_guis.txt:1613) but has no button here; only Support and Cancel are
  adjacent in this template. Support bottoms out in `DIPLOMACY_modify_play_success` (se_DIPLOMACY.txt:574),
  which takes `$amt$` (a literal OR a `var:X` — proven at se_QING_MINISTRY.txt:1023,
  `DIPLOMACY_modify_play_success = { amt = var:qing_zongli_play_delta }`), scales it by the
  instigator/target power balance, and clamps 0-100.
- **An existing PASSIVE Zongli mechanic already touches play success**:
  `QING_zongli_play_boost` (se_QING_MINISTRY.txt:1017-1025) applies +/-2 success per pulse to
  every CHI-instigated play, driven by the ministry's ambient performance
  (`qing_min_perf_zongli`), not by any specific character. This is a SEPARATE, ambient effect
  the new feature does not touch or duplicate — the new feature is a discrete, player-issued,
  per-character action.
- **The corps itself**: `qing_zongli_diplomat` (character var, marker), `qing_zongli_diplomats`
  (COUNTRY variable-list of corps members, rebuilt each pulse by
  `QING_ministry_recompute_perf_zongli`, se_QING_MINISTRY.txt:493-556),
  `qing_zongli_diplomat_count`. Auto-staffed/refilled by
  `QING_subpost_staff_corps_minted` / `QING_subpost_refill_sweep`
  (se_QING_SUBPOSTS.txt) and, as of the 2026-08-23 fix, protected from double-booking by
  `QING_subpost_strip_double_booked` (evicts a corps member who takes a vanilla role).
  `combined_stats_council_svalue` (martial+finesse+charisma+zeal+degree_prestige, minus a
  disgrace penalty; QING_governance_svalues.txt:185) is the PROVEN "ablest official" ranking
  score, already used to pick a Zongli envoy for a flavor payoff
  (`qing_legation.3`, events/imp19c_mod_events/qing_legation_events.txt:179-184:
  `ordered_in_list = { variable = qing_zongli_diplomats  order_by = combined_stats_council_svalue
  max = 1 }`).
- **Zongli Yamen panel roster** (gui/qing_zongli.gui:233-285): a `dynamicgridbox` over
  `Player.MakeScope.GetList('qing_zongli_diplomats')`, each row showing portrait, name, a
  charisma icon+value (`Character.GetCharisma`, `icon_oratory`), and a Recall button. This is
  where requirement 2's "clearly labelled" status must render.
- **Shared court-event throttle**: `qing_gc_event_slot_used` (monthly-reset flag) + a
  per-target timed cooldown variable is the PROVEN pattern for gating a recurring
  chance-of-firing court event so several instances don't dogpile in one pulse
  (se_QING_AMBAN.txt QING_amban_evaluate ~480-499 clash-event gate; se_QING_CARAVAN.txt:452-478;
  se_QING_CANTON.txt:399-415 — all three independently use this exact shape).
- **GUI `.IsSet` quirk** (memory `imp19c-gui-isset-character-var-quirk`): `.IsSet` renders
  correctly only for a FLAG/INT-valued variable, not a character-valued one. Any GUI visibility
  check must test an INT marker, never the character-reference var directly.

## 3. Data model (new)

[REVIEW-FIX round 2, finding #3] Updated count: THREE new character variables and TWO new
country/province-scope variables (the round-1 revision added `qing_zongli_dispatch_event_cd`
and `qing_zongli_dispatch_event_slot_used` in section 5.3, which the original count here
missed) — no new lists, reusing the existing `qing_zongli_diplomats` roster:

- `qing_zongli_dispatched_marker` (character var, value=1) — set on the diplomat while he is
  away on a mission. Mirrors the shape of every other corps "busy" marker in this codebase
  (`qing_officer_marker`, `qing_amban_marker`). Cleared on return (success/failure/play torn
  down by ANY path).
- `qing_zongli_dispatched_play` (character var, a saved PROVINCE scope reference to the play
  provobj he is working) — lets the periodic event effect (section 5.3) find "the play this
  diplomat is on" without a reverse search, and lets the Zongli panel label read back which
  play he's on (for tooltip/flavor text, not required for the base label).
- `qing_zongli_dispatch_event_cd` (character var, timed) — per-diplomat cooldown so the same
  dispatched man can't roll the section 5.3 event back-to-back.
- `qing_zongli_dispatched_diplomat` (province var on the play provobj, a saved CHARACTER scope
  reference) — the single source of truth for requirement 3 ("only one diplomat per play"):
  its mere presence (`has_variable`) is the gate that disables/hides the Dispatch button once
  a play already has a diplomat working it.
- `qing_zongli_dispatch_event_slot_used` (country var, monthly-reset flag) — the dedicated
  event-throttle slot from section 5.3, cleared alongside `qing_gc_event_slot_used` /
  `qing_ext_event_slot_used`.

This mirrors the amban pattern exactly (character-side marker + a pointer on each side back to
the other), which is the proven precedent for a two-sided "who is posted where" link in this
codebase (se_QING_AMBAN.txt: `qing_amban_marker` on the character, `qing_amban_here` on the
subject).

## 4. GUI changes

### 4.1 Play window — new button between Support and Cancel

In BOTH instances of the play-side block (gui/shared/gui_templates.gui:3822-3848 and the
duplicate at :4140-4166), insert a new `text_button_square` immediately after the existing
`support_play_side` block and before `cancel_play_side`:

- `name = "dispatch_diplomat_play_side"`, label key `play_dispatch_diplomat_button`
  ("Dispatch Diplomat").
- `enabled` routes to a new scripted_gui `DIPLO_player_dispatch_diplomat` (section 5.1),
  identical `GuiScope.SetRoot(Scope.GetProvince.MakeScope).AddScope('player', Player.MakeScope).End`
  wiring as the two existing buttons (proven idiom, copy exactly).
- `visible` (NOT `enabled`, so the button doesn't clutter every non-Qing player's play window):
  `scope:player` is tag CHI. Everyone else's play window shows only Support/Cancel exactly as
  today — this is a Qing-flavor addition, not a base-game feature, matching the "China
  fine-fidelity, ROW abstraction" standing rule.
- tooltip: new loc key stating what it does AND its skill-scaled, non-fixed nature (matches the
  precedent this session already set for `SUPPORT_DIPLOMATIC_PLAY_BUTTON_TT` stating Support's
  hidden cost) — "Dispatch the ablest available Zongli Yamen diplomat to personally manage this
  play. Raises its chance of success now, and may trigger further events (good or bad) based on
  his skill while he remains dispatched."

### 4.2 Zongli Yamen panel — dispatched-diplomat label (requirement 2)

[REVIEW-FIX] Reviewer flagged two problems with the original draft: `Yellow_FontColor` does
not exist anywhere in gui/ (the proven "active status" token is `Highlight_FontColor`, 28
uses), and adding a THIRD row to the roster item's fixed `{ 290 24 }` name column (which
already holds the name row + the charisma row inside an 84px-tall widget, gui/qing_zongli.gui:
238/250-265) risks vertical overflow. Revised approach: append the label INLINE in the
EXISTING name row (line 251-256, the `flowcontainer { spacing = 4 ... }` that already holds
the name tag + `qing_heir_favor_square`) instead of adding a new row — this changes row WIDTH
usage, not height, so the fixed 84px item height is never at risk:

```
flowcontainer = {
    spacing = 4
    tag = { text = "[Character.GetName]"  maximumsize = { 190 24 }  using = BaseFontM  using = Default_FontColor }
    qing_heir_favor_square = { }
    tag = {
        text = "QING_ZONGLI_DIPLOMAT_DISPATCHED_LABEL"
        maximumsize = { 60 24 }
        using = BaseFontS
        using = Highlight_FontColor
        visible = "[Character.MakeScope.GetVariable('qing_zongli_dispatched_marker').IsSet]"
        tooltip = "QING_ZONGLI_DIPLOMAT_DISPATCHED_TT"
    }
}
```
The name's `maximumsize` shrinks from 232 to 190 to make room (still well above typical name
render width; verify against the longest seeded name at implementation time). The tooltip
carries the "which play" detail so the visible label itself can stay a short fixed-width word
("Dispatched") rather than needing to fit a variable-length country name.

[REVIEW-FIX, was open question 7.4 — now DECIDED] Recall must be disabled while dispatched, not
left as an early-abort lever. The panel's Recall gui, `qing_zongli_recall_diplomat`
(common/scripted_guis/QING_zongli_panel.txt:118-137), removes only `qing_zongli_diplomat` +
the wage modifier — it does NOT know about `qing_zongli_dispatched_marker` /
`qing_zongli_dispatched_play` / the play's `qing_zongli_dispatched_diplomat`, and the section
5.4 teardown fires only on PLAY-end, not on recall. Left as-is, recalling a dispatched man
would orphan all three: the play stays flagged occupied forever (Dispatch button disabled with
no way to clear it short of the play ending on its own), the ex-diplomat keeps the marker and
is no longer even on the panel/roster, yet the section 5.3 pulse keeps rolling events for him.
Fix: add `NOT = { has_variable = qing_zongli_dispatched_marker }` to
`qing_zongli_recall_diplomat`'s `is_valid`, NOT `is_shown`. [REVIEW-FIX round 2, finding #2]
This is not a free choice: the panel button (gui/qing_zongli.gui:269-280) gates `visible` by
`ScriptedGui.IsShown` and `enabled` by `ScriptedGui.IsValid`. Putting the new guard in
`is_shown` would HIDE the Recall button entirely while dispatched — leaving nothing to carry a
"why disabled" tooltip. `is_valid` keeps the button visible but greyed, which is the intended
UX. Since the button's own tooltip is a static loc key (`QING_ZONGLI_RECALL_TT`), it will not
automatically explain a failed `is_valid` — add a `custom_tooltip` inside
`qing_zongli_recall_diplomat`'s `is_valid` block (the proven way this codebase surfaces a
conditional "why disabled" reason) stating the dispatched man cannot be recalled early; the
mission ends when the play resolves.

## 5. Effects

### 5.1 `DIPLO_player_dispatch_diplomat` (new scripted_gui, EE_scripted_guis.txt, beside
`DIPLO_player_support_play`)

```
scope = province
ai_is_valid = { always = no }
is_valid = {
    has_variable = is_diplomatic_play
    scope:player = { tag = CHI }
    NOT = { has_variable = qing_zongli_dispatched_diplomat }        # requirement 3, half A
    scope:player = {
        any_in_list = {
            variable = qing_zongli_diplomats
            NOT = { has_variable = qing_zongli_dispatched_marker }  # requirement 3, half B
        }
    }
    var:diplomatic_play_success < 100
}
effect = {
    QING_zongli_dispatch_diplomat = yes   # this = the play provobj; scope:player set by GUI
}
```

[REVIEW-FIX, was open question 7.1 — CONFIRMED PROVEN] `any_in_list` as an existence check
inside a trigger is a real, proven idiom in this codebase — se_QING_FACTION.txt:1025-1026 and
qing_faction_events.txt:43-44 use the exact `variable=… + has_variable=… + var:…` shape. 5.1 is
fine as drafted.

### 5.2 `QING_zongli_dispatch_diplomat` (new effect, se_QING_MINISTRY.txt or a new
se_QING_LEGATION_DISPATCH.txt beside the other Zongli-adjacent files — reviewer's call)

Province scope (`this` = the play provobj), `scope:player` = CHI (set by the GUI wiring).

[REVIEW-FIX, was open question 7.2 — CONFIRMED CORRECT, revised for clarity anyway] The
reviewer confirmed `PREV` as originally drafted IS correct here: `scope:player = {...}` and
`scope:qing_zongli_dispatch_pick = {...}` are sequential siblings, not nested, so `PREV` inside
the pick block correctly resolves to the block's structural parent — the play provobj — not to
`scope:player`. Proven precedent for storing a scope ref via `value = prev`:
se_QING_CUSTOMS.txt:130, se_QING_HOUSEHOLD.txt:356, se_QING_COUNCIL.txt:1722,
se_PURCHASE.txt:1964. Kept anyway as an explicit `save_scope_as` BEFORE the first scope switch
— matching the amban precedent (QING_amban_evaluate: `save_scope_as = qing_amban_subject`
before switching into `ROOT`) and this codebase's convention of not relying on implicit `PREV`
depth across a multi-step scope chain, even when technically safe:

```
save_scope_as = qing_zongli_dispatch_play_scope   # explicit capture, before any scope switch
scope:player = {
    ordered_in_list = {
        variable = qing_zongli_diplomats
        limit = { NOT = { has_variable = qing_zongli_dispatched_marker } }
        order_by = combined_stats_council_svalue
        check_range_bounds = no
        max = 1
        save_scope_as = qing_zongli_dispatch_pick
    }
}
scope:qing_zongli_dispatch_pick = {
    set_variable = { name = qing_zongli_dispatched_marker  value = 1 }
    set_variable = { name = qing_zongli_dispatched_play  value = scope:qing_zongli_dispatch_play_scope }
}
set_variable = { name = qing_zongli_dispatched_diplomat  value = scope:qing_zongli_dispatch_pick }
set_variable = {
    name = qing_zongli_dispatch_amt_tmp
    value = { value = scope:qing_zongli_dispatch_pick.combined_stats_council_svalue  divide = 2  min = 5  max = 20 }
}
DIPLOMACY_modify_play_success = { amt = var:qing_zongli_dispatch_amt_tmp }
remove_variable = qing_zongli_dispatch_amt_tmp
LOG_line = { sys = QING  msg = "zongli: diplomat dispatched to a play, success raised" }
```

Satisfies requirement 4's first half (raises success on dispatch, scaled by the diplomat's
combined skill, not a flat number — thematically distinct from Support's flat +10).

### 5.3 Ongoing skill-weighted events (requirement 4's second half)

New quarterly pulse function `QING_zongli_dispatch_pulse`. [REVIEW-FIX, was open question 7.3
— now DECIDED] `QING_zongli_play_boost`'s actual caller is `QING_gp_scan_plays`
(se_QING_DIPLO.txt:701), which runs the boost's body INSIDE a per-play
`every_in_global_list` (province/play scope) — placing a standalone `every_character`
function "beside" that would run it once per live play (redundant N×, wrong scope). Do NOT
place it there. Instead call `QING_zongli_dispatch_pulse = yes` as its own line inside
`QING_GOV_pulse` (se_QING_GOVERNANCE.txt:212), which runs QUARTERLY in CHI country scope
(dispatched from 00_monthly_country.txt:98) — giving ROOT = CHI and the quarterly cadence the
function needs.

[REVIEW-FIX round 2, finding #1] The original draft cited se_QING_MINISTRY.txt:514 as "proven"
for filtering `every_character` on `employer = ROOT`. That citation is FALSE: that sibling
function does NOT use ROOT — it uses `employer = scope:qing_min_recompute_ctry`, and the
comment directly above it (lines 501-507) explains why: `ROOT` inside a `scope:player = {}`
wrapper resolves to the CHARACTER the picker just scoped into, not CHI — a confirmed bug class
that rebuilt a roster empty. `QING_GOV_pulse` itself has no such wrapper (a plain per-country
`on_action` effect, ROOT genuinely = CHI throughout), so `employer = ROOT` would likely still
work here — but the design must not cite a disproven idiom as its proof, and should follow the
same defensive convention section 5.2 already adopted (explicit capture over reliance on
implicit scope). Fix: `save_scope_as = qing_zongli_dispatch_home` at the top of
`QING_zongli_dispatch_pulse` (before the `every_character` call), then filter on
`employer = scope:qing_zongli_dispatch_home` — matching the real proven sibling shape at
se_QING_MINISTRY.txt:501-514, not the disproven one. For every character carrying
`qing_zongli_dispatched_marker` (a small set — at most one per play, plays are rare), roll a
charisma-weighted chance of a further event:

```
QING_zongli_dispatch_pulse = {
    save_scope_as = qing_zongli_dispatch_home
    every_character = {
        limit = {
            employer = scope:qing_zongli_dispatch_home
            is_alive = yes
            has_variable = qing_zongli_dispatched_marker
            has_variable = qing_zongli_dispatched_play
            var:qing_zongli_dispatched_play = { has_variable = is_diplomatic_play }   # play still live; else clean up (7.5)
            NOT = { has_variable = qing_zongli_dispatch_event_cd }   # per-diplomat cooldown, mirrors qing_amban_clash_cd
        }
        save_scope_as = qing_dispatch_evt_diplomat
        var:qing_zongli_dispatched_play = { save_scope_as = qing_dispatch_evt_play }
        if = {
            limit = { NOT = { has_variable = qing_zongli_dispatch_event_slot_used } }   # [REVIEW-FIX] dedicated slot, see below
            set_variable = { name = qing_zongli_dispatch_event_slot_used  value = 1 }
            set_variable = { name = qing_zongli_dispatch_event_cd  days = 180 }   # per-diplomat, stops back-to-back rolls
            trigger_event = { id = qing_zongli_dispatch.1  days = { 5 15 } }
        }
    }
}
```

[REVIEW-FIX, was open question 7.4-adjacent, now DECIDED — reviewer finding #4] The shared
`qing_gc_event_slot_used` throttle is a single per-quarter slot already contended by SIX other
rollers inside the same pulse (dynasty, faction, justice-via-frontier, industry-via-works,
foreign-spouse, officer — per the "TWO-SLOT EVENT BUDGET" comment at
00_monthly_country.txt:80-81) plus a second `qing_ext_event_slot_used` slot for tribute.
Adding dispatch as a SEVENTH competitor for the already-scarce court slot would make
requirement 4's periodic events near-inert — violating the "fixes must be visible" standing
rule (a feature that almost never fires is not a delivered feature). Fix: give dispatch its
OWN dedicated slot, `qing_zongli_dispatch_event_slot_used`, cleared at the SAME top-of-pulse
location as the other two slots (00_monthly_country.txt, alongside the existing
`remove_variable = qing_gc_event_slot_used` / `remove_variable = qing_ext_event_slot_used`
lines) — a THIRD budget line, not a share of an existing one. Since at most one diplomat is
ever dispatched per play and plays are rare, this dedicated slot only ever protects against
the edge case of two-or-more diplomats rolling in the exact same pulse, without competing
against the six unrelated rollers.

The event `qing_zongli_dispatch.1` (new, events/imp19c_mod_events/qing_legation_events.txt or a
new file) resolves good/bad on a charisma-weighted roll — e.g. two options gated by
`scope:qing_dispatch_evt_diplomat.GetCharisma` bands (a high-charisma man's "clever gambit"
option succeeds more often; this can be a `random_list` weighted by charisma, or two
mutually-exclusive triggered options the way `qing_amban.1`'s clash/cooperate branches already
work) — each branch calls `scope:qing_dispatch_evt_play = { DIPLOMACY_modify_play_success =
{ amt = <+N or -N> } }`. Exact weighting formula and flavor text are an implementation-time
detail once the review confirms the pulse/event shape.

### 5.4 Teardown — single chokepoint

Add to `AI_remove_diplomatic_play` (se_AI.txt:887), inside the existing `if = { limit = {
has_variable = play_instigator } ... }`-style guarded block (or a sibling one, guarded on
`has_variable = qing_zongli_dispatched_diplomat`):

```
if = {
    limit = { has_variable = qing_zongli_dispatched_diplomat }
    var:qing_zongli_dispatched_diplomat = {
        remove_variable = qing_zongli_dispatched_marker
        remove_variable = qing_zongli_dispatched_play
        remove_variable = qing_zongli_dispatch_event_cd
    }
}
```

Because every play-end path already funnels through this one function (section 2), this single
addition releases the diplomat regardless of how the play ends (success, failure, cancel,
timeout, war-triggered removal) — no need to touch any of the 7 call sites individually. This
is the same "single source of truth chokepoint" shape already proven for the #118 post system.

## 6. Requirement-by-requirement mapping

1. Button between Support/Cancel — section 4.1.
2. Dispatched label on the Zongli panel — section 4.2.
3. One diplomat per play (both directions: a play can't get two diplomats, a diplomat can't
   serve two plays) — the `qing_zongli_dispatched_diplomat` / `qing_zongli_dispatched_marker`
   pair in section 3, enforced in the `is_valid` gates in 5.1.
4. Immediate success boost scaled by skill (5.2) + ongoing skill-weighted swing events (5.3).

## 7. Review round 1 — resolution log

All 8 original open questions were answered by an independent adversarial review against
on-disk code. Four required a design change (folded into sections 4.2, 5.2, 5.3 above, marked
[REVIEW-FIX]); four confirmed the original draft correct with no change needed.

- 7.1 `any_in_list` existence check — CONFIRMED proven (se_QING_FACTION.txt:1025-1026,
  qing_faction_events.txt:43-44). No change.
- 7.2 `PREV` scope capture — CONFIRMED correct as drafted (sequential siblings, not nested);
  revised anyway to an explicit `save_scope_as` for clarity (section 5.2).
- 7.3 `QING_zongli_dispatch_pulse` placement — WRONG as drafted; moved out of
  `QING_gp_scan_plays`'s per-play iterator into a standalone call in `QING_GOV_pulse`
  (section 5.3).
- 7.4 Recall-while-dispatched — DECIDED: disable Recall while dispatched, add the marker guard
  to `qing_zongli_recall_diplomat`'s validity check (section 4.2). Real orphan-state bug if left
  unresolved (dispatched diplomat could be recalled from the panel while the play he was
  working stays permanently flagged occupied).
- 7.5 dead-code guard — CONFIRMED `AI_remove_diplomatic_play` is the sole teardown chokepoint
  (`remove_variable = is_diplomatic_play` appears nowhere else); the 5.3 liveness guard is
  cheap defensive code, kept as-is.
- 7.6 corps headcount during dispatch — CONFIRMED no exploit; a dispatched man still counts
  toward `qing_zongli_diplomat_count` and `QING_subpost_refill_sweep` reads the live marker
  dispatch never touches. No change.
- 7.7 font-color token — WRONG (`Yellow_FontColor` does not exist); corrected to
  `Highlight_FontColor` (section 4.2).
- 7.8 interaction with the 1:1 double-booking sweep — CONFIRMED no interaction; dispatch sets
  none of `is_general`/`is_admiral`/`is_governor`/`qing_officer_marker`/`has_tech_office`, so
  `QING_subpost_strip_double_booked` never evicts a dispatched-only diplomat. No change.

Remaining implementation-time details (not blockers, to settle while writing the code): the
exact charisma-band thresholds and flavor text for `qing_zongli_dispatch.1`; the three new
localization keys (`play_dispatch_diplomat_button` + its tooltip,
`QING_ZONGLI_DIPLOMAT_DISPATCHED_LABEL` + its tooltip); verifying the shrunk 190px name
`maximumsize` (section 4.2) doesn't clip the longest seeded diplomat name in practice.

## 8. Review round 2 — confirmation pass, resolution log

A second independent review verified the round-1 fixes themselves. Two required a further
correction; two were confirmed as documentation-only fixes with no code-shape change.

- Finding #1 (MEDIUM) — the section 5.3 citation for filtering `every_character` on
  `employer = ROOT` pointed at se_QING_MINISTRY.txt:514, which actually filters on
  `employer = scope:qing_min_recompute_ctry` specifically BECAUSE bare `ROOT` inside a
  `scope:player = {}` wrapper resolves to the wrong scope (a confirmed prior bug class). Fixed:
  `QING_zongli_dispatch_pulse` now opens with `save_scope_as = qing_zongli_dispatch_home` and
  filters on `employer = scope:qing_zongli_dispatch_home`, matching the REAL proven sibling
  shape rather than a disproven one (section 5.3, code block updated).
- Finding #2 (MEDIUM/LOW) — section 4.2 left the Recall guard's location ambiguous ("is_valid
  or is_shown"). Committed to `is_valid`: the panel button (gui/qing_zongli.gui:269-280) gates
  `visible` via `IsShown` and `enabled` via `IsValid`, so an `is_shown` guard would hide the
  button entirely, leaving no surface for the "why disabled" tooltip. Added: a `custom_tooltip`
  inside the `is_valid` block stating the reason (section 4.2, updated).
- Finding #3 (LOW) — section 3's data-model count was stale (said "two character vars, one
  province var"; the round-1 revision had already added a third character var and a country
  var). Corrected to five variables total, each listed (section 3, updated).
- Finding #4 (LOW) — line-citation drift, `00_monthly_country.txt` slot-clear location cited as
  "~78-80," actually 80-81. Corrected (section 5.3).

Everything else — `Highlight_FontColor`'s existence, the inline-label row-width fit (282px
within budget), `QING_GOV_pulse`'s host/cadence, the dedicated event-slot mechanics, and the
section 5.2 scope chain (no leftover `PREV`, `this` correctly reverts to the play provobj after
both scope switches close) — was independently re-verified against on-disk code and confirmed
correct with no further change.

**Verdict: READY TO IMPLEMENT**, pending the user's go-ahead.
