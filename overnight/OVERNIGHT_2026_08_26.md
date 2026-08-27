# Overnight run — 2026-08-26

## ASSUMPTIONS & GUESSES
- Task #1 required no guessed values; the target tan color and layout were
  both copied verbatim from an existing vanilla loc string, not invented.
- Task #2/#3 (Consort Clan): the user's instruction was "positive number
  changes in green text and negative in red." For Court Corruption, a
  literal reading of that rule would color a -4 change (corruption easing,
  good for the country) RED, since -4 is a negative number. I instead
  colored it GREEN, matching this codebase's own existing precedent
  (`qing_household.9.b.tt`, which colors a corruption decrease `#G`) —
  i.e. colored by whether the change benefits the country, not by raw
  arithmetic sign. If the user actually wants strict sign-based coloring
  (so a corruption DECREASE always shows red because -4 is negative),
  this specific line needs flipping back — flag for confirmation.

## Task #1 — Fix GC "Titles Unassigned" notification style

**What it was:** In the Qing Grand Council's "Titles Unassigned" alert/tooltip
(`QING_GC_TITLES_UNASSIGNED_TT` and `QING_GC_TITLES_UNASSIGNED_ALERT_TT`,
`localization/english/qing_governance_l_english.yml`), the "Titles Unassigned"
header rendered with the `#Y` tag (not tan) and ran inline with the rest of the
sentence on one line, instead of matching the vanilla vacant-office notification
pattern (`ALERT_EMPTY_OFFICE:0 "#T Titles Unassigned#!"`, `alerts_l_english.yml`,
`#T` = tan, `color:{0.98,0.85,0.588}` per `gui/textformatting.gui:4-12`) and the
mod's own standard tooltip template (`"#T <Header>#!\n<body>"`, confirmed against
dozens of existing entries in `core_l_english.yml`, e.g. `TRAIT_TOOLTIP`,
`IS_PREGNANT_DETAILED_TT`).

**What I did:** Changed both loc strings from
`"#Y Titles unassigned#! (虛位待補). #R [...]"` to
`"#T Titles Unassigned#!\n(虛位待補). #R [...]"` — tan tag, capitalized
"Unassigned" to match vanilla exactly, and the header now sits on its own line
with the vacancy count and per-office detail below, same as vanilla.

**Key decision:** Fixed BOTH the in-panel tooltip (`QING_GC_TITLES_UNASSIGNED_TT`,
shown on the government-view badge) and the top-bar alert tooltip
(`QING_GC_TITLES_UNASSIGNED_ALERT_TT`), since they carried the identical bug in
identical text — fixing only one would have left the other inconsistent.

**Mid-task correction (false-alarm check, not a false premise):** A parallel
log/screenshot triage flagged screenshot `20260826220204_1.jpg` as showing
"Titles Unassigned" already correct (own line, tan) before this fix landed,
appearing to contradict the bug. Verified directly: that screenshot's tooltip
lists "Minister of Foreign Affairs / Minister of Development / Minister of
Culture" — vanilla ministerial titles, none of which are among the Qing GC's 13
great offices (Grand Chancellor, Grand Minister of Personnel/Revenue/Rites/War/
Justice/Works, Censorate, Lifan Yuan, Chamberlain, Zongli Yamen, Grand
Secretariat, Guard Commandant). The screenshot is the **vanilla `empty_office`
alert** (the correct reference pattern the task pointed at), not the Qing-
specific alert that had the bug — the two alerts coexist in
`gui/alertmanager.gui` and share the same dismiss token. The bug and the fix
are both real; the screenshot depicted the reference, not the defect. No revert
needed.

**Review:** Self-reviewed the diff (fork context did not permit spawning a
code-review subagent). Checked: no brace imbalance (loc string only, quote
count balanced), no macro-void risk (plain loc text, not a LOG/debug_log
string), no RHS-comparison issue (no triggers touched), no BOM/CRLF churn
(`git diff --stat` shows exactly 2 lines changed, file BOM preserved).

**Commit:** `89cddaf54` — "fix: GC Titles Unassigned notification color+layout
to match vanilla vacant-office pattern" — pushed to `merge-overnight`.

**Follow-up code-review (dispatched by the coordinator, since the fork could
not spawn its own):** Confirmed `#T` is a real tan color alias
(`gui/textformatting.gui`) and the `\n`-after-header convention is correct and
matches ~10 other keys in the same file, plus vanilla `ALERT_EMPTY_OFFICE`. One
nit: the CJK gloss `(虛位待補)` was left orphaned at the start of the body line
instead of inside the header span, unlike the file's own convention (e.g.
`#T Dynastic Harmony (皇室和睦): ...#!`). Fixed in commit `5366fa703` — moved
the gloss inside the `#T ... #!` header on both strings. No other findings.

**Status:** DONE.

## Task #16 — Fix office-appointment var-scope failure cascade (qing_accountability_events)

**What it was:** The single largest error class in the latest boot log
(`error.log`, ~38,000 occurrences), reported at
`events/imp19c_mod_events/qing_accountability_events.txt:107` (via
`QING_office_appoint`) and `:120`/`:121` (via `QING_council_recompute`):
"Failed to fetch variable for 'qing_office_held' due to not being set" /
"Event target link 'var' returned an unset scope" / "Invalid left side during
comparison 'var'" — three log lines per occurrence, all describing the same
one failed evaluation of a variable-holding-a-flag comparison against an
unset variable.

**Diagnosis (traced in source, not asserted):**
- `QING_office_appoint` (`common/scripted_effects/se_QING_COUNCIL.txt:1759-1763`,
  pre-fix) used a single flat `limit` block:
  `limit = { has_variable = qing_office_held  NOT = { var:qing_office_held = flag:$office$ } }`.
  For any appointee who has never held a great office before (the common case
  — every autofill-seeded scholar, every fresh keju laureate), `has_variable`
  is correctly false, but the engine still evaluates the sibling
  `NOT = { var:qing_office_held = flag:$office$ }` leaf, which fails to fetch
  the unset variable and logs the three-line error — even though the overall
  boolean AND outcome (correctly "false, don't vacate anything") is
  unaffected. This is the exact "read-before-set" class documented in memory
  (`local_var scope boundary`). Confirmed this is the ONLY site in the whole
  effect (1744-1914) where `qing_office_held` is read before its own
  unconditional `set_variable` at line 1800.
- `QING_council_recompute`'s parallel error for `qing_pos_marker_ct`
  (`se_QING_COUNCIL.txt:685-722`) I could **not** pin to a defect after
  exhaustive tracing: full-repo grep confirms `qing_pos_marker_ct` is used
  ONLY inside this one `every_character` block; it is unconditionally
  `set_variable`'d to 0 at line 699 before every read/increment/removal in
  the same iteration; brace depth across the block is verified balanced
  (0 in, 0 out, never negative); the `ROOT = { ... }` re-scope at 687-690 is
  an idiom used 20+ times elsewhere in this codebase without issue and
  correctly returns to character scope at its closing brace. I also checked
  the specific call site the log attributes this to
  (`qing_accountability_events.txt` option `.1.b`, `QING_council_recompute = yes`
  at line 121) — the event is `type = country_event` with `ROOT = CHI`
  throughout, so the `employer = ROOT` guards inside the recompute walk are
  correctly scoped there too (ruling out the sibling "ROOT = the appointee,
  not CHI" bug class that `QING_office_appoint`'s own #373 comment documents
  as a real, previously-fixed instance of this exact mistake elsewhere).
  **Left as-is** — no changes made to this block. Hypothesis, not fact: this
  may be downstream fallout from the `qing_office_held` failure in the same
  call chain (the two errors are adjacent event options), in which case
  fixing #16's confirmed bug may reduce or eliminate this count too; or it
  may be a benign engine self-logging artifact of the same "leaf-still-
  evaluated" class on some OTHER of `QING_council_recompute`'s 21 callers
  (per its own comment) that error.log's line attribution didn't let me
  localize further. **Check the next boot's error.log for the
  `qing_pos_marker_ct` count** — if it drops to zero or near-zero, this fix
  alone resolved it; if the count is materially unchanged, it needs its own
  follow-up task with the other 20 call sites audited for the ROOT-vs-
  employer mismatch.

**What I did:** Restructured `QING_office_appoint`'s guard (`se_QING_COUNCIL.txt`,
~line 1759) from a flat two-leaf `limit` into a nested `if`: the outer `if`
gates on `has_variable = qing_office_held` alone; only its inner `if` (run
only when the outer already passed) evaluates
`NOT = { var:qing_office_held = flag:$office$ }`. Same net effect
(`QING_office_vacate_dispatch_nobackfill` still fires under the identical
combined condition), but the var-flag compare is now structurally
unreachable while the variable is unset.

**Review:** Self-reviewed (fork context did not permit spawning a
code-review subagent — same constraint as Task #1). Checked: brace balance
verified across the whole file (script-counted, net 0, never negative);
no macro-void risk (plain comment, no LOG/debug_log string touched); no
RHS-comparison-rule violation (unchanged — `flag:$office$` is a literal
RHS, same as before); `git diff --stat` shows 17 insertions / 9 deletions,
no EOL/BOM churn (file has no BOM before or after, consistent).

**Commit:** `ccb2dca00` — "fix: read-before-set var-flag error in
QING_office_appoint (~38k boot-log lines)" — pushed to `merge-overnight`.

**Bonus finding (out of this task's scope, logged for Task #9):** while
tracing `QING_char_holds_court_position`'s OR-set
(`common/scripted_triggers/qing_dynasty_triggers.txt:299-320`) against
`QING_office_appoint`'s own "strip every other court marker on seating"
block (`se_QING_COUNCIL.txt:1811-1865`), found the strip block is MISSING
`qing_court_artist` (Court Painter), `qing_caravan_super_marker`,
`qing_salt_commissioner_marker`, `qing_is_xj_beg`,
`qing_opium_commissioner_marker`, and `qing_customs_ig_marker` — six markers
that the candidate-exclusion trigger and the 1:1-audit walk both know
about, but that a man keeps if he is promoted INTO a great office while
holding one of them. This is very likely the exact mechanism behind Task
#9's screenshot repro (Court Painter + Minister of Culture held at once).
Left untouched here (out of scope for #16) — Task #9 should extend the
strip block at lines 1811-1865 with these six markers, following the exact
pattern already used there for `qing_hoppo_marker`.

**Follow-up code-review (dispatched by the coordinator, same as Task #1):**
Confirmed correctness — before/after truth tables identical for all three
cases (never held office, holds this office, holds a different office);
brace balance clean (2 opens, 2 closes, enclosing effect closes correctly
at line 1922); nested-if-under-has_variable is the dominant idiom in this
file (35 other occurrences), not a novel form; no RHS-comparison violation.
Verdict: ship as-is, no findings to fix. Reviewer also spotted two more
sites with the same flat-AND anti-pattern — `se_QING_AFFINITY.txt:225-226`
and `se_ECON_LOG.txt:743` (both already comment-flagged as the same class)
— out of scope for this commit, filed as Task #28.

**Status:** DONE (confirmed fix shipped + pushed, reviewed clean).
`qing_pos_marker_ct` cascade NOT independently fixed — see hypothesis
above; recommend checking its count on the next boot before deciding
whether it needs its own task
(tracked as Task #27).

## Task #9 — Add Court Painter to 1:1 court-position restriction

**What it was:** Task #16's investigation found the root cause already:
`QING_office_appoint`'s "strip every other court marker on seating" block
(`se_QING_COUNCIL.txt`, ~1811-1865) stripped guard/censor/zongli/study/
eunuch/amban/hoppo/march_gg/consort markers on great-office promotion, but
missed six: `qing_court_artist` (Court Painter), `qing_caravan_super_marker`,
`qing_salt_commissioner_marker`, `qing_is_xj_beg`,
`qing_opium_commissioner_marker`, `qing_customs_ig_marker`. Screenshot
`20260826222001_1.jpg` confirmed the live repro (Court Painter + Minister of
Culture held at once). Task #9's scope was widened to all six, not just
Court Painter, since it's the same bug under six names.

**Diagnosis verification (traced independently, not taken on trust):**
Read the strip block directly, then traced each of the six markers to its own
grant/vacate/rotate site to classify it:
- **Four single-holder posts** (caravan superintendent, salt commissioner,
  opium commissioner, customs Inspector-General) each carry the same
  three-part state as Hoppo: a per-char marker, a salary `character_modifier`,
  and a COUNTRY-side holder var. Confirmed exact names against each office's
  own vacate/rotate code: `qing_caravan_super_office`/`qing_caravan_super_holder`
  (`se_QING_CARAVAN.txt:945-949`), `qing_salt_commissioner_office`/
  `qing_salt_commissioner_holder` (`se_QING_SALT.txt:82-87`),
  `qing_opium_commissioner_office`/`qing_opium_commissioner_holder`
  (`se_QING_OPIUM.txt:434-451` — confirmed `qing_lin_zexu_appointed`, a
  separate one-time-ever flag, must NOT be touched by the strip), and
  `qing_customs_inspector_general`/`qing_customs_ig_holder`
  (`se_QING_CUSTOMS.txt:116-152`, cross-checked against the modifier name
  used by its own vacate-previous-IG block at lines 126/175 — NOT
  `qing_customs_ig_office`, which doesn't exist).
- **Two many-seat corps markers** (`qing_court_artist`, `qing_is_xj_beg`) have
  NO character_modifier and NO country holder var — confirmed by reading
  their grant sites (`se_QING_WENZHI.txt`, `se_QING_XINJIANG.txt`): both are
  capped corps whose counts (`qing_court_artist_count`, `qing_xj_beg_count`)
  are rebuilt from a live `every_character` scan on demand, never
  incrementally tracked, matching the existing bare-`remove_variable` pattern
  already used in this same block for the guard/censor/study marks.

**What I did:** Added four three-part strip blocks (marker + modifier +
employer-wrapped holder-var clear) for the single-holder posts, matching the
proven Hoppo pattern exactly, plus two bare `remove_variable` strips for the
corps markers, matching the guard/censor/study pattern exactly. All six
inserted into the same scope (`this` = the appointee, confirmed unchanged
from `QING_office_appoint`'s own header comment; `employer` resolves to CHI
identically to the adjacent, already-proven Hoppo block — no scope-changing
effect sits between them).

**Review:** Self-reviewed (same fork-context constraint noted in Task #16 —
could not spawn a nested code-review subagent). Verified independently:
brace balance of the whole file after edit (script-counted: final depth 0,
never negative); all six modifier/var names cross-checked against their own
files' vacate/rotate code rather than assumed; confirmed `qing_lin_zexu_appointed`
is untouched; confirmed no scope-changing effect between the proven Hoppo
block and the new blocks.

**Commit:** `f63d58628` — "fix: close 1:1 court-position strip gap for 6
markers (task #9)" — pushed to `merge-overnight`.

**Status:** DONE — all six markers fixed, not just Court Painter.

**Post-hoc code review (dispatched by the coordinator against commit
f63d58628):** PASS, no bugs. All six modifier/holder-var names independently
verified against source (confirmed `qing_customs_inspector_general` is
correct, `qing_customs_ig_office` does not exist anywhere in `common/`).
Confirmed `qing_lin_zexu_appointed` untouched. Confirmed the `employer={}`
wrap is necessary and correct at this scope. Two non-blocking observations:
(1) the `qing_is_xj_beg` strip is effectively unreachable in practice, like
the pre-existing `qing_march_gg`/`qing_is_harem_consort` defensive strips —
harmless to include for list completeness; (2) the `qing_court_artist` strip
also fixes a second, previously-unreported bug: `qing_court_artist_count`'s
rebuild didn't exclude office-holders, so a promoted painter was silently
inflating the atelier's cap-5 count and could block new appointments — this
fix closes that too, as a side effect of removing the marker on seating.

## Task #28 — Fix flat-AND read-before-set anti-pattern in se_QING_AFFINITY and se_ECON_LOG

**What it was:** A code review of Task #16's fix flagged two more sites with
the identical flat-AND read-before-set shape: a `limit` block combining
`has_variable = X` with a sibling leaf that reads/compares `X`, which the
engine still evaluates even when `has_variable` already fails, logging a
spurious error for every case where `X` was never set.
- `common/scripted_effects/se_QING_AFFINITY.txt:225-226` (`QING_char_affinity`'s
  0..100 clamp): `has_variable = qing_char_affinity  var:qing_char_affinity > 100`
  (and the mirror `< 0` line). Both already carried a 2026-08-19 comment
  documenting 1160x "Failed to fetch variable" hits at exactly these lines.
- `common/scripted_effects/se_ECON_LOG.txt:743` (`ECON_LOG_curx_tick_emit`'s
  sentinel check): `has_variable = ECON_LOG_tickval  var:ECON_LOG_tickval >
  -999999999`. Already carried a 2026-08-16 comment documenting 3652 hits.

**What I did:**
- AFFINITY: merged the two independent flat-AND ifs into one outer
  `if = { limit = { has_variable = qing_char_affinity } ... }` with the two
  compares nested inside as separate inner `if`s — one shared guard instead
  of two duplicated flat leaves, same net effect (both clamps still fire
  under the identical combined condition as before).
  ) — no behavior change, only the spurious "not set" log removed.
- ECON_LOG: nested the sentinel compare inside its own `if`, gated on
  `has_variable`. **Key correctness point, checked carefully:** the ORIGINAL
  code had a single `else = { debug_log = "IMP19C CURXV flag EMPTY" }` on the
  flat if, which fired for BOTH failure reasons (never-set, or set-but-
  sentinel). A naive nest would only route the never-set case to that else,
  silently dropping the set-but-sentinel case with no flag emitted at all —
  a real behavior change, not just a log-noise fix. Preserved the original
  combined semantics by duplicating the identical `else = { debug_log =
  "IMP19C CURXV flag EMPTY" }` one level in (on the new inner if), so both
  failure reasons still emit the same flag, exactly as before.

**Review:** Self-reviewed (fork-context constraint, as with Tasks #16/#9).
Brace balance verified independently on both files after the edit
(script-counted: final depth 0, never negative, for each file). Re-read the
full original ECON_LOG if-block (through its own nested caps/while/else at
line ~770) before restructuring, specifically to catch the else-semantics
issue above rather than assume a bare copy of the AFFINITY pattern would be
safe.

**Commit:** `0682c6941` — "fix: nest 2 more flat-AND read-before-set sites
(task #28)" — pushed to `merge-overnight`.

**Status:** DONE — both sites fixed, ECON_LOG else-semantics preserved.

## Task #2 & #3 — Consort Clan modifier display format + named corruption stat

**What it was:** "The Consort Clan" event (`qing_dynasty.7`,
`localization/english/qing_dynasty_l_english.yml`) buried its modifier
changes inline inside parentheses ("dynastic harmony +2, corruption
eased" / "corruption up, dynastic harmony -4"), with no modifier list at
the bottom, no capitalization, no color, and — Task #3's specific ask —
no naming of which corruption stat "eased"/"rose" or by how much.

**Diagnosis:** Traced `qing_dynasty.7`'s two options
(`events/imp19c_mod_events/qing_dynasty_events.txt:308-319`) to their
effects, `QING_dynasty_consort_clan_curb` / `_indulge`
(`common/scripted_effects/se_QING_DYNASTY.txt:545-566`):
- Curb: `QING_dynasty_harmony_nudge{amount=2}`,
  `QING_DECLINE_nudge{var=qing_corruption_level amount=-4}`,
  empress `add_loyalty = loyalty_qing_delta_n8` (confirmed -8 base,
  `common/loyalty/00_imp19c_loyalty.txt:176`).
- Indulge: harmony `amount=-4`, `qing_corruption_level amount=5`,
  empress `add_loyalty = loyalty_qing_delta_p12` (+12 base).
- `qing_corruption_level` is a COUNTRY-scope administrative-corruption
  meter (0-100, clamped by `QING_DECLINE_nudge`,
  `se_QING_DECLINE.txt:19,33-42`) — used across ministries, censorate,
  canal, customs, self-strengthening. It is NOT a character stat. Its
  already-established display name in this codebase is "Court
  Corruption" (`QING_HEALTH_CORRUPTION_FMT`,
  `qing_governance_l_english.yml:395`).
- Found the proven own-line template already in THIS SAME FILE for THIS
  SAME MODIFIER: `qing_dynasty.1.a.tt` / `.1.b.tt` use
  `"...\n#G Dynastic Harmony: +8#!"` / `"...\n#R Dynastic Harmony: -6#!"`.
  Copied this exact syntax rather than inventing new formatting.

**What I did:** Rewrote both `.tt` strings — stripped the inline
parenthetical stat mentions from the prose, and appended each modifier on
its own line at the bottom in the proven `\n#COLOR Name: sign N#!`
format, Capitalized: Dynastic Harmony, Court Corruption, Empress's
Loyalty. Colored by benefit-to-country, not raw sign — see ASSUMPTIONS &
GUESSES above for the one place this matters (Court Corruption's -4/+5).

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Checked: quote balance (2 per line, both edited lines), no BOM/CRLF churn
(file BOM preserved, diff is exactly 2 lines), no macro-void risk (plain
loc text), apostrophes in "Empress's"/"Empress's family" don't need
escaping in a double-quoted loc string (only `"` does).

**Commit:** `bdbf49eab` — "fix: Consort Clan modifier display — own-line
list, named corruption stat" — pushed to `merge-overnight`.

**Status:** DONE (Task #2 and #3 both satisfied by this one commit).

## Task #17 / Task #20 — University T2 national-bonus scope mismatch

**What it was:** Log triage found the SAME error at two call sites, so both
tasks share one root cause and one fix:
- `common/on_action/economy/oa_economy_setup.txt:2721` chain
  (`EDU_set_t2_national_bonus_from_universities`, `se_EDU.txt:206`) — 1,234
  occurrences.
- `common/script_values/EDU_svalues.txt:78` (`EDU_university_national_bonus`'s
  own `has_law`, reached via `EDU_university_national_bonus_here`,
  `EDU_svalues.txt:109-113`) — 50 occurrences.

Both errors are "has_law trigger: Wrong scope for trigger: province,
expected country." A prior 2026-08-25 fix attempt (already present in the
code, with its own comment) diagnosed the scope leak correctly — a nested
`every_governorships -> every_governorship_state -> every_state_province`
iterator inside `EDU_set_t2_national_bonus_from_universities`'s value block
leaves the block's "current scope" at PROVINCE for everything after the
iterator closes, not the country scope the enclosing `set_variable` assumes
— but its chosen fix (a dotted `owner.EDU_university_national_bonus`
reference) did not actually work: the newest boot log still shows all
1,234 + 50 occurrences.

**Diagnosis (traced, not assumed):** `EDU_university_national_bonus` is
documented "Scope: Country" and contains a BARE `has_law = ...` trigger
inside its own `if.limit` (`EDU_svalues.txt:73-82`), correct only when the
whole script value is invoked with `this` already = country. A dotted
scope-prefix on a script-value NAME (`owner.SomeScriptValue`) rescopes
direct field/value access, but does NOT push a new root for TRIGGERS nested
inside that value's own blocks — so the bare `has_law` inside stayed
evaluated at the STALE province scope regardless of the `owner.` prefix on
the outer call. Confirmed this codebase already has a WORKING alternative
idiom for exactly this situation: `DEMAND_svalues.txt`'s `DEMAND_steel_ships`
uses an explicit `owner = { value = num_of_ships ... }` scope-change BLOCK
(not a dotted path) to correctly re-root a nested computation, and this same
file's `EDU_university_bonus_total_province` uses the block form
`owner = { has_law = ... }` directly for a trigger check — both proven,
neither erroring in the log.

**What I did:** Replaced the dotted `owner.EDU_university_national_bonus`
reference at both call sites with the proven `owner = { value =
EDU_university_national_bonus }` scope-change block:
- `se_EDU.txt:206` (`EDU_set_t2_national_bonus_from_universities`'s
  `multiply` field).
- `EDU_svalues.txt:109-113` (`EDU_university_national_bonus_here`'s `value`
  field) — this is Task #20's exact site, fixed by the same change since
  it's the same root cause.

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Brace balance verified independently on both files after the edit
(script-counted: final depth 0, never negative, both files). Checked
`git status` before committing — no concurrent uncommitted changes to
either file from other in-flight tasks.

**Commit:** `7afd1b097` — "fix: rescope EDU_university_national_bonus calls
via owner={} block (tasks #17, #20)" — pushed to `merge-overnight`.

**Status:** DONE — both tasks closed by this one commit. Recommend checking
the next boot log for both error counts (EDU_svalues.txt:78 and the
oa_economy_setup.txt:2721 chain) dropping to zero.
