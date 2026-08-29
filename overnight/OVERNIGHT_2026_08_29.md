# Overnight log — 2026-08-29

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
