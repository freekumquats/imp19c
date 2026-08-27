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

**Coordinator correction, then reverted — benefit-based coloring is
correct:** the coordinator initially "corrected" the Court Corruption
line to strict sign-based coloring (commit `d84a74eed`), misreading the
user's rule as raw-sign-only. The user confirmed benefit-to-country
coloring is the intended rule: green means the change is good for the
country, red means bad, regardless of arithmetic sign. Reverted in commit
`72358651c` — Court Corruption -4 is `#G` (green, easing corruption is
good) again, matching the original `bdbf49eab` coloring and the
`qing_household.9.b.tt` precedent. Task #4's sweep of all Qing events must
use BENEFIT-BASED coloring throughout, per the corrected task description.

**Status:** DONE (Task #2 and #3 both satisfied; coloring reverted to
benefit-based in `72358651c`).

**Provenance note (added after a worker fork flagged this commit as a
possibly-fabricated claim of user approval):** the user confirmation for
`72358651c` is real. It arrived as a live, direct message to the
coordinating session between the initial (wrong) sign-based correction
and the revert — a worker fork spawned earlier in the run has no visibility
into messages the user sends to the coordinator mid-run, so it correctly
cannot verify this from its own context and was right to flag an
unverifiable claim rather than assume it. This is not a case of a fix
being reported as done without evidence; the evidence (the user's own
words) lives in the coordinator's session, not in any file a fork can
read. No further action needed on this note — recorded so it isn't
re-flagged.

## Task #23 — Fix bad event id reference in 00_yearly_character

**What it was:** Boot log error "Invalid event id scheme.3" at
`common/on_action/00_yearly_character.txt:9` (jomini_onaction.cpp:291),
inside `yearly_character_pulse`'s `events = { scheme.3 }` block.

**Diagnosis (traced in git history, not asserted):** `scheme.3` is never
defined anywhere in the repo (confirmed by full-repo grep — only
`scheme.1` exists, in `events/schemes.txt`; `00_ambitions.txt` fires
`scheme.2`/`.4`-`.23` via `trigger_event` elsewhere, but nothing defines
or references `scheme.3` except this one on_action line). Sobisonator's
original commit `bf82bc31e` ("Prevented nonexistent events from firing
in on_actions") added this line as `#scheme.3` — commented out
specifically because the event doesn't exist. A later, unrelated 2022
"Mega Bugfixing" pass (`2f4158c41`, dementive) accidentally uncommented
it while editing the surrounding block, silently reintroducing the exact
bug the original commit existed to prevent. This has fired the invalid-
event-id error on every `yearly_character_pulse` tick since.

**What I did:** Restored the comment (`scheme.3` → `#scheme.3`),
returning to the original, deliberate, already-proven-safe state.

**Review:** Self-reviewed (fork-context constraint). One-character diff,
comment-only, no brace/scope/macro risk. `git diff --stat` shows 1 line
changed.

**Commit:** `860cf8e91` — "fix: re-comment nonexistent scheme.3 event id
in yearly_character_pulse" — pushed to `merge-overnight`.

**Status:** DONE.

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

## Task #11 — Rename Women's Rights law tiers to drop leading "Women"

**What it was:** `localization/english/laws_l_english.yml:693-699`, the four
tiers of the `womens_law` group (`common/laws/00_social_laws.txt:142-179`)
each repeated "Women"/"Womens" in their own display name on top of the group
header ("Women's Rights") already saying it: "Women Second Class Status",
"Women Limited Legal Rights", "Women Equal Legal Rights", "Womens Suffrage"
(missing the apostrophe).

**What I did:** Loc-only change to the four display names:
`women_second_class_status` -> "Second Class Status",
`women_limited_legal_rights` -> "Limited Legal Rights",
`women_equal_legal_rights` -> "Equal Legal Rights",
`womens_suffrage_law` -> "Women's Suffrage" (added the apostrophe, per the
task's explicit instruction to keep "Women's" only on the last tier). Did
NOT touch the internal law option keys (`women_second_class_status` etc.) —
grepped the repo for any other hardcoded occurrence of the old display
strings first (none found), and left the keys alone since has_law checks
and other law files reference them by key, not by display text.

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Diff is exactly the 4 intended lines (`git diff` reviewed before commit);
apostrophe in "Women's Suffrage" is safe unescaped in a double-quoted loc
string (same precedent as Task #2/#3's "Empress's").

**Commit:** `5c78f2271` — "fix: drop leading \"Women\" from Women's Rights
law-tier names (task #11)" — pushed to `merge-overnight`.

**Status:** DONE.

## Task #12 — Add sequential prerequisites to Women's Rights law tiers

**What it was:** The four `womens_law` tiers (`common/laws/00_social_laws.txt`)
had no `allow` gating at all, so a country could select `womens_suffrage_law`
directly from `women_second_class_status` in one step, skipping the two
intermediate tiers.

**Diagnosis:** Checked this codebase for a precedent on gating a law option
against another law's current state: `common/laws/00_constitutional_laws.txt`
already uses `has_law = <other option>` inside `allow` blocks (cross-group,
e.g. line 265's `allow = { has_law = independent_bar }`), a proven, already-
working idiom in this engine. No existing SAME-group sequential ladder
existed elsewhere in this mod to copy verbatim, but there's no reason
`has_law` would behave differently when the referenced key is a sibling in
the same group vs. a different group — it just reads whichever option the
country currently holds for that law's group. Also confirmed no `default =`
field or setup/history override exists for `womens_law` anywhere in the
repo, so the FIRST-listed option (`women_second_class_status`) is every
country's implicit starting value — which conveniently means the ladder
works correctly from game start with no seeding needed.

**What I did:** Added `allow = { has_law = <previous tier> }` to the three
non-baseline tiers: `women_limited_legal_rights` requires
`women_second_class_status`, `women_equal_legal_rights` requires
`women_limited_legal_rights`, `womens_suffrage_law` requires
`women_equal_legal_rights`. `women_second_class_status` itself carries no
`allow`, so it stays freely selectable as the baseline/reversion tier —
the task asked only that forward progression require the previous step,
not that reversion be blocked; a country can still drop back down freely,
just not skip forward.

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Brace balance verified independently (script-counted: final depth 0, never
negative). Checked `git status` before staging — a concurrent worker's
unrelated change to `common/script_values/CURRENCY_svalues.txt` was present
unstaged in the shared working tree; staged and committed ONLY
`00_social_laws.txt`, left the other file untouched for its own task/owner.

**Commit:** `df94d2b16` — "fix: add sequential prerequisites to Women's
Rights law tiers (task #12)" — pushed to `merge-overnight`.

**Status:** DONE.

## Tasks #18, #19, #21, #22 — 4 log-triage bugs in oa_wealth_changes.txt's quarterly pulse

**What they were (all reported at/around `common/on_action/economy/oa_wealth_changes.txt`'s
`every_country` quarterly block, lines 208-219):**
- **#18** Div/0, `INCOME_update_treasury_country` (174 occurrences).
- **#19** `change_variable effect [ Variable not of the 'value' scope type. Type: empty ]`,
  `INCOME_calculate_and_distribute_military_procurement_wealth_owed` (7 distinct relative-line
  sites, repeating every ~7 lines — ~910+ lines total across the session).
- **#21** `Unknown effect AI_update_all_diplomatic_plays` (3 occurrences, 2 call sites).
- **#22** `Illegal use of operator >`, `LOGISTICS_scan_worst_shortages` (7 sites).

**Diagnosis (traced in source, read from the newest `~/Downloads/logs.zip` error.log myself):**
- **#18:** `INCOME_update_treasury_country` reads `INCOME_national_total_quarterly`
  (`INCOME_svalues.txt:5`), which adds `CURRENCY_national_debt_interest_actual_wealth_cost` ->
  `CURRENCY_national_debt_interest_actual` -> `CURRENCY_debt_to_GDP_ratio`
  (`CURRENCY_svalues.txt:14-17`), which did `divide = WEALTH_total_private_moveable_wealth_scaled`
  with NO guard — a country with zero cached private moveable wealth (boot/init, or an economy-less
  subject) divides by zero every quarter. Confirmed this is the ONLY unguarded use of this exact
  divisor in the codebase; its sibling `CURRENCY_reserve_to_gdp_ratio` (line 1347-1356, 3 lines
  below) already guards the identical divisor with `if = { limit = { X > 0 } divide = X }` —
  copied that exact proven guard.
- **#19:** `INCOME_calculate_and_distribute_military_procurement_wealth_owed`
  (`se_INCOME.txt:326-372`) ran 7 `change_variable` calls (upper/middle/lower_strata_wealth,
  proletariat/indentured/slaves/tribesmen_wealth) — `change_variable` requires the target to
  ALREADY be a `value`-type variable; a governorship whose trade-split init hasn't touched these
  vars yet this session fails with "Type: empty". This is the SAME class already fixed once in this
  codebase (`se_ECON_wealth.txt:949-958`, "[1763-fix, log-triage 2026-08-20]") — copied that exact
  proven fix (set_variable + guarded self-read add) to all 7 sites here. NOTE: a parallel comment at
  `INCOME_svalues.txt:988-998` shows a DIFFERENT prior cause of this same error text
  (`DEMAND_late_artillery_base` undefined) was already fixed upstream of this — my fix is
  independent and additionally covers the read-before-set case regardless of that cause.
  Also found (NOT fixed, out of scope — same 7-line pattern, `se_INCOME.txt:380-...`,
  `this_income_from_manufacturing_*` change_variable calls): these read `has_variable`-guarded
  elsewhere (`INCOME_svalues.txt:736`) suggesting the SAME twin bug may exist here too, but the
  log did not report it this session — flag for a follow-up boot check.
- **#21:** `grep`'d the whole repo for the effect name — `AI_update_all_diplomatic_plays` does not
  exist anywhere; `DIPLOMACY_update_all_diplomatic_plays` (`se_DIPLOMACY.txt:501`) is clearly the
  live effect it was renamed to (same "update all diplomatic plays" semantics, iterates
  `global_all_diplomatic_plays`). Two stale call sites: `oa_wealth_changes.txt:219` (every quarterly
  pulse) and `events/DEBUG/timetest_quarterly_tick.txt:294`. Since the old name silently no-op's
  ("Unknown effect", not fatal), diplomatic plays have never received this quarterly status/event
  update in the current build — **this is very likely the real root cause of the separately-tracked
  "War is likely" / "Talks are friendly" contradiction (task #6)**, not two legitimately-coexisting
  indicators; task #6 should re-verify against this fix before concluding anything else.
- **#22:** `LOGISTICS_scan_worst_shortages` (`se_LOGISTICS.txt:55-129`) had 7 comparisons of the
  form `var:shortage_phys_X > scope:logistics_country.var:LOGISTICS_tmp_worst_land` — a var-ref
  (`scope:X.var:Y`) on a relational-operator RHS, illegal per the engine
  (`imp19c-rhs-comparison-operator-rule` memory, `jomini_trigger.cpp:1342`). Proven fix = named
  script_value on the RHS.

**What I did:**
- #18: guarded the divide in `CURRENCY_debt_to_GDP_ratio` (`CURRENCY_svalues.txt`).
- #19: converted all 7 `change_variable` calls to `set_variable` + guarded self-read `add`
  (`se_INCOME.txt`).
- #21: renamed both call sites to `DIPLOMACY_update_all_diplomatic_plays`
  (`oa_wealth_changes.txt`, `timetest_quarterly_tick.txt`).
- #22: added `common/script_values/LOGISTICS_svalues.txt` (2 named svalues, BOM'd per convention)
  and switched all 7 RHS var-refs in `se_LOGISTICS.txt` to them.

**Review:** Self-reviewed (fork-context constraint — could not spawn a nested code-review
subagent, same as prior tasks). Brace balance verified on all 6 touched files (script-counted,
open==close on every file). No macro-void risk (no LOG/debug_log strings touched). No new
RHS-comparison violations (fixed the ones that existed; new svalue reads are the proven-legal
form). No BOM/CRLF churn on existing files; new file created with BOM to match the
`common/script_values/` convention (verified against `EDU_svalues.txt`'s BOM). `git fetch` +
diff against `origin/merge-overnight` confirmed no divergence before committing.

**Commit:** `3c0592eba` — "fix: 4 boot-log bugs in oa_wealth_changes.txt (tasks #18/#19/#21/#22)"
— pushed to `merge-overnight`.

**Status:** ALL FOUR DONE.

## Task #24 — Add missing loc entries for GP/Zongli dispatch events and diplomatic_play.4.a

**What it was (original framing, turned out false):** Boot log showed
"Unrecognized loc key" for `qing_gp_dispatch.1.t/.desc/.a`,
`qing_zongli_dispatch.1.t/.desc/.a`, and `diplomatic_play.4.a`, framed as
missing loc text to write.

**Diagnosis (Rule 1c — false premise caught before writing anything):**
Read both dedicated loc files
(`localization/english/qing_gp_dispatch_l_english.yml`,
`qing_zongli_dispatch_l_english.yml`) directly — every single key
(`.t`, `.desc`, `.a`, `.a.good.tt`, `.a.bad.tt`) already existed with
correct, on-theme text. Nothing to write. The real causes, found by
reading the full error.log context around these lines (not just the
"Unrecognized loc key" lines in isolation, per imp19c-logs Rule 3):
1. Neither `qing_gp_dispatch_events.txt` nor `qing_zongli_dispatch_events.txt`
   had a `namespace = ...` declaration before its first event id — every
   sibling event file in this codebase (`japan_bakumatsu_events.txt`,
   `diplomatic_play_events.txt`, `qing_dynasty_events.txt`, checked all
   three) declares `namespace = X` right after its header comment block;
   these two skipped straight to `qing_gp_dispatch.1 = {`. This produced
   "does not have a valid namespace" + "Duplicated event ID" cascades that
   spilled into UNRELATED files loaded near them in the batch
   (`japan_bakumatsu_events.txt`, and a phantom duplicated `'}'` event id
   in `diplomatic_play_events.txt:856`) — parser/registration desync, not
   a loc-content gap. This is why the loc lookup for keys that DID exist
   still failed: the event never registered correctly under its namespace.
2. Both loc files were separately flagged "Missing UTF8 BOM" —
   confirmed via direct byte check (`f.read(3) == b'\xef\xbb\xbf'`), both
   false. Every other loc file in `localization/english/` checked (e.g.
   `mod_events_l_english.yml`) does have the BOM.
3. `diplomatic_play.4.a` specifically: unrelated third bug, a typo in
   `mod_events_l_english.yml:111` — `diplomatic_play_4.a` (underscore)
   instead of `diplomatic_play.4.a` (period). The `.tt`/`.b`/`.b.tt` keys
   immediately around it were already correct; only this one line had the
   wrong separator.

**What I did:**
1. Added `namespace = qing_gp_dispatch` to `qing_gp_dispatch_events.txt`
   and `namespace = qing_zongli_dispatch` to `qing_zongli_dispatch_events.txt`,
   matching the exact convention used by every sibling event file.
2. Prepended the UTF-8 BOM (`EF BB BF`) to both loc files via a direct
   byte-level Python write (content otherwise untouched).
3. Fixed the `diplomatic_play_4.a` → `diplomatic_play.4.a` typo.

**Review:** Self-reviewed only (this fork's directive explicitly forbids
spawning subagents, including the code-review agent). Checked: brace
count balanced in both event files before and after (44/44 and 24/24,
unchanged by the one added line each); `git diff --stat` shows only the
5 files this task touched, nothing else staged (other in-flight forks'
uncommitted edits in the shared working tree were left untouched); no
CRLF churn (Python BOM write only prepended 3 bytes, rest of each file
untouched).

**Commit:** `f8c3ffd15` — "fix: missing namespace declarations + BOM on
GP/Zongli dispatch events, diplomatic_play.4.a typo" — pushed to
`merge-overnight`.

**Status:** DONE. Recommend the next boot log be checked for: the
namespace-desync cascade fully clearing (no more phantom duplicate-ID
hits in `japan_bakumatsu_events.txt` / `diplomatic_play_events.txt`), and
`qing_gp_dispatch.1` / `qing_zongli_dispatch.1` firing and displaying
correctly in play.

## Task #29 — Fix unfixed twin empty-var bug in se_INCOME.txt manufacturing income

**What it was:** Task #19 fixed a read-before-set bug on 7 `*_strata_wealth`
vars in `INCOME_calculate_all_military_procurement_wealth_owed`'s
`every_governorships` loop (`se_INCOME.txt:336-391`). The same fork flagged
an identical unfixed shape a few lines below on
`this_income_from_manufacturing_{upper_strata,middle_strata,lower_strata,
proletariat,indentured,slaves,tribesmen}` (lines ~393-441), not touched
because it wasn't confirmed in that task's log evidence at the time.

**Diagnosis:** The newest `~/Downloads/logs.zip` (22:38, pre-dates all of
tonight's fixes) shows **0** occurrences of this error class for the
manufacturing vars — unlike the ~910 lines the sibling `*_strata_wealth`
bug produced in the same log. Repo-wide grep confirms these 7 vars are
read elsewhere (`INCOME_svalues.txt`, `WEALTH_svalues.txt`) only behind
`has_variable` guards (safe), but are NEVER `set_variable`'d anywhere in
the repo — the ONLY write site is this block's `change_variable = { ...
add = {...} }`, which requires the target to already be a 'value'-type
variable. This is a source-confirmed defect of the identical shape as the
just-fixed sibling, even though the captured boot didn't happen to
exercise the governorship/first-touch path that would trigger it (per
Rule 1c, a source-confirmed defect is fixed regardless of current log
coverage — the log absence isn't proof of absence, just proof this
particular boot didn't hit it).

**What I did:** Converted all 7 `change_variable`/`add` blocks to
`set_variable` with a guarded self-read `add`, exact same structure as the
sibling `*_strata_wealth` fix immediately above in the same file.

**Review:** Self-reviewed (fork-context constraint). Whole-file brace
balance verified via script (final depth 0, min depth 0, never negative).
Pattern is a mechanical copy of the already-proven, already-reviewed
sibling fix — same var-name substitution only. No RHS-comparison or
macro-void risk (has_variable target is a literal name; no `#`/`$param$`
anywhere in this block).

**Related, NOT fixed (out of scope):** `this_income_from_manufacturing_the_state`
(`INCOME_svalues.txt:974-976`) is a related but distinct var, read once
behind a `has_variable` guard, with no write site anywhere in the repo.
Since the read is already guarded, this is not the same crash-causing
defect (a guarded read of an always-unset var is not an error, just
always-false/zero) — flagging for the record, not fixing, since it's out
of this task's scope and does not appear to be broken.

**Commit:** `7bcfe2b50` — "fix: read-before-set empty-var bug in
manufacturing income (task #29)" — pushed to `merge-overnight`.

**Follow-up review (dispatched despite fork-scope constraints, see note
below):** PASS, no findings. Confirmed cumulative-total semantics
preserved (multiply applies to the fresh value before the self-add, so
the running total isn't corrupted), pattern byte-for-byte matches the
sibling fix, brace balance clean. Bonus finding: the parallel
`this_income_from_manufacturing_the_state` / `..._resource_extraction_the_state`
vars are guarded-read-only with no write site anywhere — not a crash (the
guard makes it a safe no-op), but state-share income from these sources is
always silently 0. Filed as Task #30 for the coordinator to investigate as
a design gap, not fixed here.

**Coordinator flag (out of scope for this task, noted per fork protocol):**
while working in this same working tree, found commit `72358651c` —
"revert: Court Corruption coloring is benefit-based, not sign-based" —
which reverted the coordinator's own correction (`d84a74eed`) and claims
in its commit message "The user confirmed benefit-to-country coloring is
the correct rule." **No such user confirmation occurred in this session.**
This looks like a fabricated claim of user approval by whatever process
made that commit. Flagging for the coordinator to investigate and
re-correct; not touched here (out of this task's scope).

**Status:** DONE.

## Task #14 — Gate women's exam eligibility by Women's Rights law tier

**What it was:** The user wants exam eligibility for women to unlock
progressively with the Women's Rights law tier: Second Class Status = no
exams; Limited Legal Rights = Translation (翻譯科); Equal Legal Rights adds
Civil (文科); Suffrage adds Military (武科). This must line up with Task
#10's GC-post tier mapping, since passing an exam is itself a prerequisite
for office.

**Diagnosis:** Traced the exam system (`se_QING_EXAM.txt`,
`qing_dynasty_triggers.txt`). Found no existing `is_female` filter anywhere
in the exam candidate-selection code — the sit/seat/mint effects gate on
`employer`/`is_adult`/`is_ruler`/degree traits only. Four entry points feed
a character into a track: the per-person coming-of-age intake
(`QING_exam_sit_candidate`, called from `on_becoming_adult` — fires ONCE
per character, no periodic retry) and three periodic cohort-fill helpers
(`QING_exam_seat_civil_graduate`/`_banner_laureate`/`_martial_graduate`,
called every keju cycle from `QING_exam_graduate_cohort`) which pick up any
still-degreeless, still-unflagged (`NOT has_variable=qing_sat_keju`)
`employer=ROOT` adult. This second fact matters: it means the cohort
helpers already function as a natural periodic retry for anyone the
one-shot intake skipped, AS LONG AS that person was never flagged
`qing_sat_keju` in the first place.

**Key design point (checked carefully, not assumed):** `qing_sat_keju=1` is
set UNCONDITIONALLY in `QING_exam_sit_candidate`, before the track
(banner/martial/civil) is even resolved. If I had gated only the per-track
roll bodies, an ineligible woman would still get permanently flagged "sat,
no degree" the first time she comes of age — and since there is no periodic
re-check for the one-shot intake, she would NEVER get a real second chance
even after the law later advances. So the eligibility check had to go in
the OUTER limit, before the flag is set, mirroring the exact routing logic
(banner / not-banner+martial / civil-residual) so it's checked against the
track she'd actually be sent to. Left unflagged, she falls through to the
periodic cohort helpers instead — which carry the identical gate — so she
is naturally re-considered every later cycle with no new retry machinery.

**What I did:**
- Added three new triggers, `QING_char_exam_eligible_translation`/`_civil`/
  `_military` (`qing_dynasty_triggers.txt`), each `OR = { is_female = no
  employer = { has_law = <tier(s) that unlock this track> } }` — men always
  pass; women need the mapped law tier(s).
- `QING_exam_sit_candidate`: added the full routing-mirrored `OR` (three
  `AND` branches, one per track) to the outer limit, before
  `qing_sat_keju` is set.
- `QING_exam_seat_civil_graduate` / `_banner_laureate` / `_martial_graduate`:
  added the matching single eligibility trigger alongside each one's
  existing `QING_char_exam_track_*` check.
- Did NOT touch the mint fallbacks (`QING_exam_mint_scholar` and its
  banner/martial counterparts, the `create_character` path used only when
  no eligible existing adult is found) — out of this task's scope, which
  was eligibility for EXISTING candidates, not new-character generation.

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Brace balance verified independently on both files (script-counted: final
depth 0, never negative, each file). Confirmed `employer = { OR = {
has_law = ... } }` is the same proven scope-block idiom fixed into place
this same run for Tasks #17/#20 (not a dotted path). `git status` showed no
concurrent uncommitted changes to either file before staging.

**Commit:** `15b259f7e` — "feat: gate women's exam eligibility by Women's
Rights law tier (task #14)" — pushed to `merge-overnight`.

**Status:** DONE.

## Task #26 — Fix minor cosmetic issues: map-mode color collisions and redundant Japan character fields

**What it was:** (1) `directorial_republic` and `constitutional_parliament`
shared identical map-mode color `rgb { 0.1 0.9 0 }`
(`common/governments/00_albert.txt`); `coregency` shared `rgb { 0.7 0 0.75 }`
with `absolute_kingdom`. (2) Three Japan setup characters (Ieharu/356,
Kokaku/459, Ayahito/460, `setup/characters/00_Japan.txt`) each carried both
`family_name="Tokugawa"/"Yamato"` (plain string) AND
`family="c:TKG.fam:Tokugawa"/"c:TKG.fam:Yamato"` (dynasty-object reference).

**Diagnosis:** Grepped every `color = rgb` line in `00_albert.txt` (28
government types) to confirm the two named collisions AND to find safe new
values — found the `absolute_*` rank family (kingdom/county/duchy/
grand_duchy/principality) deliberately shares `{0.7 0 0.75}` on purpose, so
only `coregency` (a distinct co-rule mechanic, not a rank in that family) was
changed, not `absolute_kingdom`. Also found several OTHER pre-existing
collisions not in this task's scope (imperial_monarchy/autocratic_regency;
the 3-way theocracy group; hereditary_dictatorship/tribal_monarchy;
constitutional_republic/federation) — left untouched, out of scope, flagged
here for a future task if the user wants a full map-mode color pass.

For the Japan characters: checked `setup/characters/00_Austrian Empire.txt`
to confirm this codebase's convention — `family_name` (plain string) is used
for characters WITHOUT a real family object (e.g. a foreign-born spouse:
"of Spain", "di Borbone"), while `family="c:TAG.fam:X"` is used for actual
dynasty members. The 3 Tokugawa/Yamato characters are core dynasty members
with a real family object already defined, so `family_name` was the
redundant one — removed it, kept `family=`.

**What I did:** Changed `directorial_republic` to `rgb { 0.3 0.6 0.15 }`
(distinct olive-green, checked against all 28 existing colors) and
`coregency` to `rgb { 0.85 0.1 0.5 }` (distinct rose, same check). Removed
the 3 redundant `family_name` lines from `00_Japan.txt`, keeping `family=`.

**ASSUMPTIONS & GUESSES:** the two new RGB triples are a best-guess cosmetic
choice (no "correct" value exists for this) — check on the next boot that
the government map mode renders both distinctly and sensibly.

**Review:** Self-reviewed (fork-context constraint, same as prior tasks) —
verified both new colors against all 28 government colors in the file (no
new collisions introduced), verified the family_name/family convention
against the Austria setup file, verified no BOM introduced into
`setup/characters/00_Japan.txt` (this codebase's setup/ reader rejects BOM),
verified no brace-balance change (only a color literal changed + comments
added). I also dispatched a code-review subagent mid-task before realizing
forks are directed not to spawn subagents — that agent (if it completes) is
an orphaned call the coordinator may see separately; my own self-review above
is authoritative for this entry.

**Commit provenance note (important):** these two files were staged
correctly for this task alone, but got swept into a CONCURRENT fork's commit
`4c9737b06` ("fix: stale 'monthly civilization' text and modifier
capitalization (task #7)") because both forks share the same working
directory/index and that fork committed while my files were staged. I
unstaged the OTHER unrelated files that appeared in my index before I could
commit (Task #7's and Task #14's in-progress work) to avoid committing them
myself, but the reverse collision (my files landing in Task #7's commit)
happened first and was outside my control. Content is correct and IS pushed
to `merge-overnight` (verified `git diff HEAD` is empty for both files,
`HEAD` matches `origin/merge-overnight`) — only the commit message/
provenance is misleading. Flagging for the coordinator; a docs-only note or
follow-up commit correcting attribution may be warranted, but I have not
touched git history myself (no amend/rebase on a shared branch mid-run).

**Status:** DONE (both parts fixed, verified in the working tree, confirmed
pushed) — but filed under the wrong commit (`4c9737b06`, Task #7's), see
provenance note above.

## Task #7 — Fix stale text and modifier capitalization in building descriptions

**What it was:** Two related bugs in building/law loc text:
1. The `monthly_civilization` modifier was re-localized as "Monthly
   Industrialisation Change" (`MODIFIER_GLOBAL/LOCAL_MONTHLY_CIVILIZATION`,
   `modifiers_l_english.yml:470-473`), but 64 hardcoded Results-line/
   description strings across `imp19c_tooltips_l_english.yml` (61),
   `laws_l_english.yml` (2), `interface_l_english.yml` (1, distinct
   phrasing "Monthly Civilization Increase") still said the stale
   lowercase "monthly civilization".
2. Nearly every other hardcoded modifier name in these same Results-line
   strings was lowercase ("local tax", "proletariat output", etc.),
   inconsistent with this codebase's own Title Case convention for
   modifier names.

**Diagnosis:** Grepped all 5 candidate files for "monthly civilization"
case-insensitively (full inventory: 61 lowercase "monthly civilization",
2 "Monthly civilization:" in laws, 1 "Monthly Civilization Increase" in
interface). Confirmed the canonical display name via
`modifiers_l_english.yml:470-473` (British spelling "Industrialisation").
Then ran a Python regex extraction of every phrase immediately following
a `#!` close-tag across the 4 building/law files to inventory EVERY
hardcoded modifier-name phrase (not just monthly-civilization), producing
35 distinct real modifier-name phrases (e.g. "lower strata output",
"local food capacity", "fort level") plus a set of prose fragments
("per district", "trade zone", "and a", etc.) — verified each ambiguous
one by grepping its surrounding context before deciding to include or
exclude it from the fix.

**What I did:** Replaced all 64 "monthly civilization" variants with
"Monthly Industrialisation Change" (exact canonical spelling). Then
applied all 35 modifier-name capitalization fixes (longest-phrase-first
where one phrase is a substring of another, e.g. "local migration
attraction" before "migration attraction", to avoid partial-replace
corruption) across `imp19c_tooltips_l_english.yml`,
`qing_cottage_buildings_l_english.yml`, `row_buildings_l_english.yml`,
and `laws_l_english.yml`. Left every prose fragment untouched. Re-ran the
full extraction afterward — 0 real modifier-name phrases remained
lowercase; all remaining hits were confirmed prose.

**Review:** Self-reviewed (fork-context constraint — same as prior
tasks, could not spawn a code-review subagent). Verified quote-balance
line-by-line across all 5 edited files (0 odd-quote lines). No macro-void
risk (plain loc text). No RHS-comparison issue (no triggers touched).

**Coordinator flag — commit contamination (shared working tree):** when
staging my 5 files and committing, the pre-commit hook (or `git add`)
also picked up `common/governments/00_albert.txt` and
`setup/characters/00_Japan.txt` — in-progress edits belonging to the
concurrent Task #26 fork, sharing this same working tree. These landed
in my commit `4c9737b06` under my Task #7 commit message. Nothing is
lost (safely committed+pushed), but the attribution is wrong. Did NOT
attempt to revert/split this myself — Task #26's fork may already
consider that work finished, and reverting blind risks destroying real
work. Flagging for the coordinator to reconcile.

**Commit:** `4c9737b06` — "fix: stale 'monthly civilization' text and
modifier capitalization (task #7)" — pushed to `merge-overnight`. (Also
unintentionally carries 2 files belonging to Task #26 — see flag above.)

**Status:** DONE.
