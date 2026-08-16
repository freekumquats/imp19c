# DESIGN — Art Patronage / Court Painter narrative events (task #15)

## Goal
User: "does the Art Patronage have events (including but not limited to those involving the Court
Painter)? if not it should." Confirmed gap: `se_QING_WENZHI.txt` has a real, live Court Painter
mechanic (`qing_court_artist` marker, 5-painter atelier cap, Castiglione seeded by name at game
start, commission/suppress player levers) and a dedicated panel
(`QING_household_panel.txt:263`, `qing_art_patronage_open_panel_button`), but the ONLY two events
in `qing_wenzhi_events.txt` (`.1` zenith milestone, `.2` a hidden UI trampoline for the suppress-
Jesuits button) are not painter-specific. Two new, additive events proposed.

## Event 1 — ambient painter-flavour beat (recurring, low-frequency)
A small, recurring "the atelier presents a finished work" beat while at least one court painter is
in residence — the missing ambient payoff for maintaining the mechanic at all (today, painters sit
silently once commissioned; nothing ever happens to/because of them again).
**Trigger site**: new `if` block inside `QING_wenzhi_pulse` (`se_QING_WENZHI.txt:117-150`), added
as a NEW block (no existing line touched), modelled directly on the zenith-milestone block already
there (`:138-148`):
```
# [round 1 review fix] rebuild the count HERE too, not just trust the button-maintained var --
# it otherwise goes stale after a natural death with no button click in between (same rescan
# idiom QING_wenzhi_commission_painting/QING_wenzhi_suppress_jesuits already each pay once).
set_variable = { name = qing_court_artist_count  value = 0 }
every_character = {
	limit = { has_variable = qing_court_artist  is_alive = yes  employer = ROOT }
	ROOT = { change_variable = { name = qing_court_artist_count  add = 1 } }
}
if = {
	limit = {
		var:qing_court_artist_count > 0
		NOT = { has_variable = qing_dept_cd_wenzhi_painter }
		NOT = { has_variable = qing_gc_event_slot_used }
	}
	random = {
		chance = 15
		set_variable = { name = qing_dept_cd_wenzhi_painter  days = 1095 }   # ~3y, "once every few years"
		set_variable = { name = qing_gc_event_slot_used  value = 1 }
		trigger_event = { id = qing_wenzhi_painter.1  days = { 5 20 } }
	}
}
```
Matches the established shared-slot + `qing_dept_cd_<name>`-style cooldown convention used
throughout the codebase (Canton/Caravan/Revenue/etc. — see `design/DESIGN_QING_PACING_OVERHAUL.md`
section 6 for the fuller survey of this exact idiom). 15% chance × ≥1 eligible painter, gated by a
3-year department cooldown, lands comfortably in "once every few years," consistent with every
other niche flavour beat in this doc's sibling systems — and deliberately modest so it doesn't add
a new dominant contender to the shared-slot contention `DESIGN_QING_PACING_OVERHAUL.md` is
separately trying to fix.
**Event body** (`qing_wenzhi_painter.1`, new file `events/imp19c_mod_events/qing_wenzhi_painter_
events.txt`, namespace `qing_wenzhi_painter`): flavour text about a finished commission presented
to the throne (a court still life, a hunting scene, an imperial portrait), small payoff — one
option: `current_ruler = { add_popularity = 4 }` + `QING_wenzhi_advance = { amount = 3 }` (a modest
top-up, well below the deliberate initiative buttons' 10-15). No `add_prestige` per this file's own
documented BT-5/6 rule.

## Event 2 — a court painter's death (one-shot per painter, reactive not rolled)
The mechanic already seeds ONE named historical figure (Castiglione, age 75 in 1763, documented in
`se_QING_WENZHI.txt:66-70` as expected to die of natural aging "within a few years") with zero
narrative acknowledgement planned for that death — today he just quietly disappears from the
roster like any unmarked character. A reactive, not rolled, one-shot beat closes this.
**Trigger site**: `on_character_death` is ALREADY a multi-file merged on_action in this codebase
(confirmed: `common/on_action/00_specific_from_code.txt:234` and `common/on_action/qing_mechanics_
on_actions.txt:385` are two SEPARATE, already-coexisting `on_character_death` blocks — Imperator
on_actions merge across files, unlike events). Add ONE new line to the existing fork-owned block at
`qing_mechanics_on_actions.txt:385-...` (alongside `QING_caravan_aqsaqal_teardown = yes`), calling
a new effect:
```
QING_wenzhi_painter_death_check = yes
```
New effect (`se_QING_WENZHI.txt`, new function, appended at end of file):
```
QING_wenzhi_painter_death_check = {
	# Scope: ROOT = the dying character (on_character_death convention).
	if = {
		limit = { has_variable = qing_court_artist  exists = employer  employer = { tag = CHI } }
		save_scope_as = qing_dead_painter
		employer = {
			if = {
				limit = { NOT = { has_variable = qing_gc_event_slot_used } }
				set_variable = { name = qing_gc_event_slot_used  value = 1 }
				trigger_event = { id = qing_wenzhi_painter.2  days = { 3 8 } }
			}
		}
	}
}
```
Still gated on the shared slot (a death is a real event, but not urgent enough to preempt a
simultaneous bigger court crisis — consistent with every other beat in this doc). No department
cooldown needed — a specific painter can only die once.
**Event body** (`qing_wenzhi_painter.2`): reads `scope:qing_dead_painter` (captured via
`save_scope_as` before the death fully resolves the character out of scope).
**[Implementation-review correction]** `betroth_dead_partner` (cited above) is NOT actually a
matching precedent — it uses `save_temporary_scope_as` and is consumed synchronously, same-tick,
never across a delay; every other in-repo dead-character scope read is likewise synchronous. The
only real precedent for a PERMANENT `save_scope_as` read after a scope change on a just-died
character, with no crash risk if wrong, is vanilla `00_ambitions.txt:1085/1124`
(`save_scope_as` + `employer = { trigger_event = ... }`) — which uses NO delay. Implemented
accordingly: `trigger_event = { id = qing_wenzhi_painter.2 }` with no `days=` param (not the
originally-drafted 3-8 day delay), to match the one proven shape exactly and minimize exposure to
an otherwise-unverified engine behavior. Failure mode if wrong is graceful either way — the
event's own `exists = scope:qing_dead_painter` trigger guard means a stale/invalid scope just
means the beat silently doesn't fire, never a crash.
Two flavour variants inside the SAME event, selected by trigger: if the dead painter is Castiglione
specifically (`scope:qing_dead_painter = { has_variable = qing_castiglione_char }` — reuse the
existing `qing_castiglione_char` var already set at seed time, `se_QING_WENZHI.txt:93`, comparing
identity, not nickname string-matching), a unique, historically-anchored text (his four decades at
three reigns' courts, the Sino-European style he leaves behind); otherwise a generic "a court
painter has passed" text. Small payoff either branch: `QING_wenzhi_advance = { amount = -4 }` (the
atelier loses a hand) is enough — no stability/legitimacy hit, this is a much smaller beat than the
Jesuit-suppression lever, not a policy choice.

## Round 1 review — Event 2 UNBLOCKED (task #19 resolved: no bug, both blocks are live)
Task #19's dedicated research pass found direct existence proof in an oracle repo (Terra Indomita:
`on_ruler_change_inv_.txt` and `on_ruler_change_CFT.txt`, two separate files each defining a bare
`on_ruler_change` block, both containing real load-bearing logic in a mature, actively-played mod)
that recurring on_actions DO merge bare inline blocks across files. The `#254` comment is correctly
scoped to `on_game_initialized` specifically (a one-time boot hook, plausibly special-cased), not a
general rule — resolving the apparent contradiction with the OTHER comment in the same file
(`:344-346`, "on_ruler_change ... is merged across files"), which was the accurate one. Neither
existing `on_character_death` nor `on_ruler_change` block is dead code. Event 2 proceeds exactly as
originally planned below (superseding the "BLOCKED" framing above, kept for the record).

## Round 1 review — Event 2 BLOCKED pending a separate, higher-priority investigation (task #19)
### [SUPERSEDED — see the "UNBLOCKED" note directly above; kept for the record, not acted on further]
Round 1 found Event 2's trigger-site plan rests on a claim ("on_character_death merges across
files") that a comment in the SAME target file directly disputes (`qing_mechanics_on_actions.txt:
5-11`, "[develop #254]": bare inline effect blocks do NOT merge across files) — while a DIFFERENT
comment in that same file (`:344-346`) asserts the opposite for `on_ruler_change` specifically.
This contradiction is bigger than this design: if bare blocks genuinely don't merge for recurring
on_actions, either `00_specific_from_code.txt`'s or `qing_mechanics_on_actions.txt`'s existing
`on_character_death`/`on_ruler_change` content (QING_post_release, betrothal dissolution, aqsaqal
teardown, succession contest — real, load-bearing logic, not this design's content) is silently
dead code today, independent of anything in this doc. Tracked as its own task (#19); a dedicated
research pass is resolving the merge-behavior question via oracle repos/vanilla precedent.
**Event 2 will be re-sequenced to hook in via whatever safe, list-registered form task #19 lands
on**, rather than adding a third bare block to an already-ambiguous pair. **Event 1 has no such
dependency** (it hooks into `QING_wenzhi_pulse`, an ordinary called-by-name function, not a raw
on_action) and can proceed independently once its own round-1 finding (below) is addressed.

## Round 1 review — Event 1 real gap: `qing_court_artist_count` can go stale
`qing_court_artist_count` is only rebuilt (rescanned via `every_character`) inside `QING_wenzhi_
commission_painting` and `QING_wenzhi_suppress_jesuits` — i.e. only when the player clicks one of
the two initiative buttons. It is never rebuilt when a painter dies naturally (of old age, e.g.
Castiglione). So after a painter's death, if the player doesn't immediately click a button, the
count stays stale at its last-known value, and Event 1's gate (`var:qing_court_artist_count > 0`)
could keep passing — and firing "the atelier presents a finished work" — with zero living painters
in residence. **Fix: rebuild the count directly inside a small guard at Event 1's own roll site**
(the same `set_variable = 0` + `every_character` rescan idiom already used twice in `se_QING_
WENZHI.txt`, just called a third time, here, before checking `> 0`) rather than trusting the
button-maintained var. This makes Event 1 self-sufficient regardless of whether task #19 ever
touches the death hook, and costs nothing (the rescan is O(living characters), same as the
existing two call sites already pay on every button click).

## Implementation review — Event 1 CONFIRMED CLEAN, Event 2 review in progress
Event 1's implementation review found zero defects (brace-balanced, pure addition, correct
nesting inside the patronage wrapper, correct priority vs the zenith block, loc keys exact). One
LOW informational note accepted as a conscious trade-off: the count-rescan now runs every quarter
unconditionally (previously only on a button click) — O(living characters) for one country, the
price of making Event 1 immune to the stale-count bug. Not a defect.

## What this does NOT do
- Does not touch `QING_wenzhi_commission_painting`, `QING_wenzhi_suppress_jesuits`, or any existing
  line in `se_QING_WENZHI.txt` — both new effects are wholly new functions/blocks.
- Does not add a THIRD painter-mint path — Event 1 and 2 only move the patronage meter and
  popularity, never `create_character`. The atelier's headcount still only changes via the two
  existing player-initiated buttons, keeping the 5-painter cap logic in exactly one place.
- Does not compete for player attention with a policy decision (unlike the Jesuit-suppression
  lever) — both events are flavour-only, no meaningful choice, consistent with "ambient beat" not
  "new mechanic."
