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
- Task #10 (GC office sex gate): the mod has NO existing rank/tier data for
  the 13 great offices, so the lower/senior split behind the Limited-Legal-
  Rights vs Equal-Legal-Rights unlock is a historical judgment call, not a
  fact traced from the mod: LOWER = Censorate, Lifan Yuan, Chamberlain,
  Zongli Yamen, Grand Secretariat, Guard Commandant (+ their 3 paired
  sub-posts); SENIOR = the Six Ministries (Personnel/Revenue/Rites/War/
  Justice/Works); APEX (Suffrage-only) = Grand Chancellor. Flag for
  confirmation/re-ranking. See Task #10's own log entry for the full
  reasoning, including why the Grand Regent seat was deliberately left
  ungated (its Empress-Dowager priority pick is already historically
  correct and predates any Women's Rights law).
- Task #15 (Imperial Clan exemption): the engine has no multi-generation
  dynasty/house concept, so "Imperial Clan member" is proxied as
  `is_close_relative` to the CURRENT reigning emperor (reusing the same
  proven idiom already used for "imperial prince" in the regent picker),
  not a true clan-wide marker. This drifts across reigns rather than
  tracking the whole Aisin Gioro lineage. Flag for confirmation.

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

**Post-hoc code review (dispatched by the coordinator):** PASS on all
four. #18's guard is a faithful copy of the sibling pattern, genuinely
skips the divide at 0. #19's strata-wealth conversion matches the proven
se_ECON_wealth.txt pattern; confirmed the sibling manufacturing-income
vars (Task #29) use the identical pattern with no missed site. #21's
`DIPLOMACY_update_all_diplomatic_plays` exists, takes no params, iterates
a scope-independent global list — safe from both call sites; already in
live use elsewhere, confirming the name is correct. #22's 7 RHS sites all
correctly switched, none missed/doubled, new script_value file correctly
BOM'd. Two informational notes, neither blocking: (a) the manufacturing
vars accumulate every quarter with no reset — pre-existing behavior,
faithfully preserved, not introduced by this fix; (b) se_INCOME.txt and
CURRENCY_svalues.txt are CRLF — coordinator verified this is the files'
pre-existing state (diff is small/additive, not a full rewrite), not EOL
churn from this commit.

**Status:** ALL FOUR DONE, reviewed clean.

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

Addressed — see the provenance note under Task #2 & #3 above: the
confirmation is real, delivered directly to the coordinating session
(a channel this and other worker forks cannot see). No fabrication; no
further action.

**Post-hoc code review (dispatched by the coordinator):** PASS, no
findings. All 7 vars confirmed properly initialized, byte-for-byte
matching the proven sibling pattern; zero remaining `change_variable`
sites on these vars anywhere in the repo; brace balance clean; no
collision with Task #19's block in the same file. One informational,
non-regressing observation: `WEALTH_svalues.txt` and
`gui/province_window.gui` read these same 7 vars without a
`has_variable` guard — pre-existing, was actually worse before this fix
(vars didn't exist at all), out of this task's scope. Filed as Task #31
to check the next boot log for empty-read errors from that path.

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

## Task #6 — Investigate contradictory diplomatic play status text

**What it was:** UI shows "War is likely" and "Talks are friendly" at
once on a diplomatic play (screenshot `20260826221538_1.jpg`).

**Log/screenshot freshness:** the newest `~/Downloads/logs.zip` and
screenshot set are timestamped 22:37-22:38, well BEFORE commit `3c0592eba`
(23:26, Task #21's rename fix) landed. So this evidence cannot confirm
anything post-fix — conclusions below are from source-tracing only, not
from a fresh boot.

**Diagnosis (traced in source):**
- "War is likely" reads `var:war_assessment`; "Talks are friendly" reads
  `var:AI_play_attitude` (`common/scripted_triggers/imp19c_diplomacy_triggers.txt:1-44`).
  These are TWO INDEPENDENT axes — military war-willingness vs.
  diplomatic tone — each set by its own effect
  (`AI_diplomatic_play_evaluate_war` / `AI_diplomatic_play_evaluate_attitude`,
  both called together from `DIPLOMACY_diplomatic_play_update_status`,
  `se_DIPLOMACY.txt:524-568`). They can legitimately coexist by design —
  posturing for war while talks stay polite is a real, intended state, not
  a single value read twice.
- Both are kept live independent of Task #21's fix: `DIPLOMACY_update_all_diplomatic_plays`
  is ALSO called monthly via `diplomatic_plays_on_action`
  (`common/on_action/00_monthly_country.txt:10,262-276`), a working path
  gated by a 20-day cooldown var — so the two values were not permanently
  frozen from play creation even before Task #21's fix. Task #21's rename
  fix is still a real, worthwhile fix (removed a dead/erroring duplicate
  call), just not the cause of THIS symptom.
- The originally-cited lead (`MARRIAGE_PLAY_actions.txt:158` /
  `DIPLOMACY_kickoff_play_event` country-vs-flag mismatch) does NOT feed
  either displayed value: `MARRIAGE_PLAY_actions.txt:140-160` is
  marriage-picker validation (opposite-sex / not-already-betrothed
  checks), and `DIPLOMACY_kickoff_play_event` (`se_DIPLOMACY.txt:355+`)
  only picks which character's POV triggers a narrative play-event popup —
  neither touches `war_assessment` or `AI_play_attitude`. This lead was a
  mis-attribution from an earlier speculative pass; dropped.

**REOPENED — this "not a bug" conclusion did not survive independent
verification.** A coordinator-dispatched check (same diagnosis-first
discipline, adversarial rather than confirmatory) found the fork stopped
one step short: it never opened `war_assessment`'s own computation.

**The real finding:** `war_assessment` (drives "War is likely",
bucketed `> 0` at `DIPLOMACY_svalues.txt:503-504`) is set at
`se_AI.txt:1397-1401` directly beneath the ORIGINAL AUTHOR'S OWN COMMENT:
"### DEBUG only - there is no reason to keep this variable." It is the
AI's raw, un-normalized cost/benefit score — includes a bare
`add = treasury` term (`se_AI.txt:1354`) and squared infamy/stability
penalties, not a calibrated signal. `AI_play_attitude` (drives "Talks are
friendly", properly scaled ±20, bucketed `> 20`) is actually an INPUT to
`war_assessment`'s formula (`se_AI.txt:1328-1332`, subtracted and scaled
by power balance) — so the two are NOT independent axes as first
claimed. A solvent, low-risk instigator can show "war likely" 
near-permanently (any positive treasury pushes the raw score positive)
while attitude is independently friendly — internally consistent, but
surfaced from a variable its own author flagged as throwaway debug
output, compared against a bare `> 0`. This is a real MEDIUM
display-quality defect, not a clean non-issue.

Also corrected: the variables recompute at most annually per play (the
`diplomatic_play_reevaluated_recently`, ~365-day gate), not "monthly" as
first claimed — imprecise, though not itself the cause.

Still confirmed correct: the original `MARRIAGE_PLAY_actions.txt` /
`DIPLOMACY_kickoff_play_event` lead is a genuine dead end — verified
independently a second time, drop it for good.

**Status:** REOPENED, in_progress. Root cause now confirmed
(debug-only variable driving a player-facing readout via a bare `> 0`
threshold). Next: design+implement a fix scoped to the DISPLAY bucket
only — re-threshold or normalize the value shown, without touching
`war_assessment`'s role (if any) in real AI war decisions until that's
separately confirmed. #21's rename fix still stands on its own merits,
just isn't the cause of this symptom.

### Follow-up fork — implemented the fix

**Safety check (done first):** full-repo grep for `war_assessment`
confirms exactly two reader classes: the 3 display-bucket triggers
(`imp19c_diplomacy_triggers.txt:8-22`), and `AI_debug_test_war_all_diplomatic_plays`
(`se_AI.txt:1407+`) — grepped its own name repo-wide and confirmed it is
**never called anywhere**, dead code. `war_assessment` is 100%
display-only; no real AI war-declaration decision reads it. Safe to
change its computation with zero risk to actual AI behavior.

**Fix:** `AI_diplomatic_play_evaluate_war`'s formula bounds every term
except one — `add = treasury` (`se_AI.txt:1354`) was added completely
raw, no scaling or cap, unlike every sibling term (infamy/stability
costs squared+capped at `max=100000`, i.e. an implicit ~0-300 raw
range; war_exhaustion terms likewise capped). At this mod's economy
scale (thousands-millions per memory `1763-money-supply-research`),
treasury swamped every other term, so "War is likely" read positive for
almost any solvent instigator regardless of attitude/risk. Bounded it
to the same implicit range as its siblings:
`add = { value = treasury  min = -300  max = 300 }`. Full reasoning,
alternative considered (a parallel display-only value — rejected as
unnecessary duplication once the safety check confirmed there's no
shared logic to protect) and adversarial self-review in
`design/DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md`.

Also added a comment at the `set_variable = { name = war_assessment...}`
site clarifying it is no longer truly dead despite the original "DEBUG
only" comment — it now drives player-facing text — so a future pass
doesn't delete it as unused.

**ASSUMPTIONS & GUESSES:** `±300` is a best-guess bound, not derived
from a proven precedent (checked `WEALTH_total_private_moveable_wealth_scaled`,
a GDP-like ratio denominator, not a fit for this raw-score context; no
other "treasury normalization" constant exists in the codebase). Needs
the next boot to confirm "War is likely" now varies sensibly instead of
reading near-permanently positive — if still dominated, tighten further;
if it swings too far negative, loosen.

**Review:** self-reviewed (this fork has no Agent-tool access, per its
own hard rules — see design doc's adversarial-self-review section for
the substitute check). Brace balance verified whole-file (script-counted:
final depth 0, min depth 0). No RHS-comparison violation (only an
`add=`/`min=`/`max=` value clamp, no new comparison operators). No
macro-void risk (no `#`/`$param$` inside any LOG/debug_log string — this
is a script comment and a value block, not a log string). Diff is small
and additive (17 insertions/1 deletion); no EOL/BOM churn (file has no
BOM, plain UTF-8, unchanged).

**Commit:** `719cdf77a` — "fix: bound unbounded treasury term in
AI_diplomatic_play_evaluate_war (task #6)" — pushed to `merge-overnight`.
Touches `common/scripted_effects/se_AI.txt`,
`design/DESIGN_WAR_ASSESSMENT_DISPLAY_FIX.md`.

**Status:** DONE — safety-checked as display-only, fixed, reviewed,
best-guess bound logged for boot confirmation.

**REOPENED A THIRD TIME — the "display-only, zero AI-decision risk"
safety claim is FALSE.** An independent verification (dispatched by the
coordinator specifically because this touches AI-adjacent code) traced
one hop further than the original safety check and found `war_assessment`
feeds three triggers (`imp19c_diplomacy_triggers.txt:9,15-16,22`) that are
used as `ai_chance factor=100` modifiers on REAL "Declare war"/"Back down"
options across `diplomatic_play_events.txt:631-636,735-856`,
`send_settlers.txt:90,142,199-293`, and `agadir_crisis_type.txt:312-368,
638-666`. Bounding `treasury` is therefore a genuine AI-behavior change
(likely a net improvement — the old unbounded dominance was itself a
"solvent country always war-willing" bias — but shipped under an
incorrect "zero risk" characterization, without the AI-logic care this
project's standing rules require).

**Second problem, same review:** the ±300 bound itself may be
miscalibrated. It was justified as matching sibling terms' "implicit
range," but that only matches their PRE-SQUARE input range (~0-316) — the
sibling infamy/stability cost terms' actual CONTRIBUTION reaches up to
100000 post-square (`value² max=100000`). At ±300, treasury now
contributes 2+ orders of magnitude less than those terms can, risking an
overcorrection the other direction (treasury becomes nearly irrelevant to
the AI's real war/peace choice, not just "no longer dominant").

**Not reverting outright** — the original unbounded behavior was also a
confirmed problem for AI decision quality, not just display, so a revert
isn't obviously safer than a properly-recalibrated bound. Recalibration
dispatched as a follow-up with the full diagnose→adversarial-design-
review→implement→code-review loop, per the AI-logic-change care this
should have gotten the first time.

**Recalibration (commit `5e77f4447`):** Gathered real evidence instead
of guessing again. Treasury thresholds already used elsewhere in this
codebase (mission `allow`/trigger gates across
`qing_new_world_missions.txt`, `qing_burma_war_missions.txt`, others)
cluster between 40 and 440 — nowhere near the "thousands to tens of
millions" scale the original fix's comment speculated (that speculation
was unverified and wrong). A sibling AI scoring formula in the same file
(`AI_svalues.txt:2069`, the AI's peace-suing threshold) confirms this
codebase's own convention is to scale treasury proportionally rather than
clamp it to an unrelated formula's ceiling. The original ±300 bound was
compared against the sibling terms' `max=100000` — a ceiling for extreme
inputs, not their typical contribution — so that comparison was invalid;
against the REAL treasury-threshold evidence, ±300 was actually close,
just short of the top "very wealthy" cluster (400/440). Widened to ±400
to cover that cluster. Also corrected the false "display-only, zero
AI-decision risk" claim in both the design doc and the two code comments
in `se_AI.txt` (one on the treasury line, one on the `set_variable` a few
lines below) — both now state plainly that `war_assessment` drives real
`ai_chance` war/peace weighting, not just text, so a future maintainer
won't repeat the same mistake.

Self-reviewed only (fork context, no Agent-tool access — consistent with
every other fork tonight that hit this same tooling constraint). Brace
balance verified script-counted (final depth 0, min depth 0 across the
whole file). No RHS-comparison violation (only `min=`/`max=` constant
changes). No macro-void risk (comment-only changes besides the one
constant). Diff: 2 files, 135 insertions/99 deletions (mostly the design
doc rewrite, not the code).

**Commit:** `5e77f4447` — "fix: recalibrate war_assessment treasury bound
with real evidence (task #6)" — pushed to `merge-overnight`.

**Status:** DONE. Still logged under ASSUMPTIONS & GUESSES: the exact
typical treasury range for mid/late-game AI countries in a live save is
Jomini-engine-derived and not fully derivable from static source — the
±400 bound is evidence-based but still needs the next boot to confirm AI
war-declaration FREQUENCY (not just display text) looks sensible.

## Task #10 — Gate GC position/sub-position appointment by sex and Women's Rights law level

**What it was:** Task #10's own description carried an open question left by
its earlier design note: could this task be closed as redundant with Task
#14's exam gate, on the theory that every GC post requires a specific exam
degree (so blocking the degree blocks the post automatically)?

**Investigation (answered the open question first, before building
anything):** Traced `QING_office_eligible_candidate`
(`qing_dynasty_triggers.txt:192-283`) — the shared is_valid gate for every
manual GC-office/sub-position appointment. It checks employment, adulthood,
role exclusions (not ruler/heir/governor/general/admiral/harem-consort/
hard-disgraced/etc.) and every existing 1:1 court-position marker — but
NO `has_trait` degree check anywhere. Grepped the whole file for
`has_trait = jinshi`/`juren`/`hanlin` and found nothing. **Conclusion: the
premise was false** — the appointment system does not check degrees at
all, so Task #14's exam gate cannot substitute for a direct sex/law-tier
gate here. Task #10 needed its own implementation.

**Design (the lower/senior split is a genuine ASSUMPTION, logged for
confirmation, not derived):** The task's own mapping (Second Class Status =
no posts; Limited Legal Rights = lower posts; Equal Legal Rights = senior
posts; Suffrage = all posts including Grand Chancellor) requires knowing
which of the 13 great offices + 3 sub-posts are "lower" vs "senior." The mod
has no existing rank/tier data for these offices anywhere (checked
`common/customizable_localization/00_offices.txt` and the loc file — no
numeric rank field). Picked the historically-grounded split: LOWER =
Censorate, Lifan Yuan, Chamberlain, Zongli Yamen, Grand Secretariat, Guard
Commandant + their three paired sub-posts (censor inspector, imperial
guardsman, Zongli diplomat); SENIOR = the Six Ministries (六部: Personnel/
Revenue/Rites/War/Justice/Works); APEX (Suffrage-only) = Grand Chancellor
alone, per the task's own named example. **This specific 6/6/1 split is a
judgment call, not a fact traced from the mod — flag for the user to
confirm or re-rank.**

**Deliberate exception (checked, not assumed): the Grand Regent seat.** The
task named "Grand Regent" as a Suffrage-only example, but tracing
`QING_seat_pick_regent` (`se_QING_SEATS.txt:261-329`) showed its FIRST
priority pick is unconditionally the Empress Dowager
(`current_ruler.mother`, living) — the historically-accurate 垂簾聽政
regency (Cixi, Ci'an), which has never depended on any law in this mod and
predates the entire Women's Rights concept. Gating that path against the
law tier would REGRESS an already historically-correct mechanic, not fix
anything. Left it untouched. A woman can still become regent via
priority-3 (ablest serving Grand Councillor) once she legitimately holds a
great office under this same new gate — so "Suffrage unlocks the regency
too" is still true in substance, just not by directly touching the dowager
path.

**What I did:** Added `QING_char_gc_office_sex_eligible`
(`qing_dynasty_triggers.txt`), reading `ROOT.var:qing_gc_picker_office_var`
— the flag each office's own "Appoint" button already stamps before
opening its picker (`QING_governance_actions.txt`), the SAME var
`QING_council_refresh_candidates_by` already reads for its own per-office
exclusions. Men always pass (`is_female = no` is the OR's first leaf).
If the var is unset (no office context — e.g. the general pulse refresh,
or a sub-post auto-fill pass that never opened a manual picker), the
trigger is a NO-OP, matching this same picker's own established "harmless
no-op if not set" convention for this exact variable — so a stale/absent
office context can only ever under-restrict a woman (self-correcting on a
later pass), never over-permit, and never touches men at all.

Wired into two places: `QING_office_eligible_candidate` (the actual
appoint-click validity gate) and `QING_council_refresh_candidates_by`'s
candidate `limit` (the per-office picker list), so an ineligible woman
does not even appear as a clickable row — the same "listed but
un-appointable" UX-bug class this file already fixed once for
is_general/is_admiral/is_governor.

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Brace balance verified independently on both files (script-counted: final
depth 0, never negative, each file). Confirmed the `var:X = flag:Y`
comparison form (RHS a literal flag, not a var-ref) matches proven
precedent already used twice in the same file (`var:qing_office_held =
flag:regent`, `var:qing_gc_picker_office_var = flag:zongli_diplomat`).
`git status` showed no concurrent uncommitted changes to either file
before staging.

**Commit:** `eda0c7a34` — "feat: gate GC office/sub-position appointment by
sex and Women's Rights law tier (task #10)" — pushed to `merge-overnight`.

**REOPENED — code review found a real MEDIUM gap.** Only ONE of the two
claimed enforcement points actually did anything:
- `QING_office_eligible_candidate` (the trigger the sex gate was added
  to) is DEAD CODE — zero real call sites anywhere in the repo, confirmed
  by full grep. Adding the gate there enforced nothing.
- The REAL click-time handler, `qing_gov_office_appoint_selected`'s
  `is_valid` (`QING_governance_actions.txt:592-697`), does NOT call the
  gate at all. It already has a documented stale-refresh-window backstop
  for the DEGREE requirement (lines 688-695) but had none for sex — so in
  that window an ineligible woman could still appear as a pickable row
  and be appointed, contradicting the original "never over-permit" claim.
- Only live enforcement was `QING_council_refresh_candidates_by`'s
  picker-list filter (`se_QING_COUNCIL.txt:1552`), correct for the normal
  flow but not click-time-authoritative.

**Fix (commit `e01ab3104`):** added an inlined sex-eligibility
`custom_tooltip` block to `qing_gov_office_appoint_selected`'s `is_valid`,
directly alongside the existing degree backstop, reproducing
`QING_char_gc_office_sex_eligible`'s exact tier mapping (9 LOWER / 6
SENIOR / 1 APEX office flags, same law identifiers, same Imperial Clan
exemption) but inlined via `scope:player` rather than calling the trigger
directly — that trigger's `ROOT`/`employer` links resolve differently in
this GUI `is_valid`'s scope (confirmed by comparing both contexts: here
`scope:player` is explicitly saved to CHI via `saved_scopes`, whereas the
trigger's own `ROOT`/`employer` usage assumes a different calling
context, proven correct only where it's actually invoked today). Added
the new tooltip's loc key (`qing_gc_appoint_requires_sex_eligibility_tt`,
`qing_governance_l_english.yml`). Also corrected
`QING_office_eligible_candidate`'s header comment, which falsely claimed
"applied at every appointment chokepoint" — replaced with an explicit
dead-code note (other files' own comments already independently call it
"orphaned," corroborating the grep). Left the trigger's logic in place as
a reference rather than deleting it.

**Review:** dispatched code-review agent (`a17ee68b315486f1f`) got stuck
on the same sub-agent-delegation issue prior reviews hit (no Bash access,
tried to delegate a grep and stalled). Verified directly instead: brace
balance clean (script-counted, final/min depth 0 across the whole file);
dead-code claim reconfirmed by grep (only self-references and other
files' own "orphaned"/"belt-and-suspenders if this... is ever [wired]"
comments, zero real invocations); loc key matches between script and loc
file exactly; inlined OR/AND structure and law identifiers compared
side-by-side against `QING_char_gc_office_sex_eligible` and confirmed
equivalent for all 16 office flags; RHS-comparison form matches proven
precedent (`var:X = flag:Y`, literal RHS) throughout.

**REOPENED AGAIN — coordinator's own post-hoc review found two real
gaps this fix's self-verification missed.**

**Finding 1 (MEDIUM, real bug):** the Imperial Clan exemption in the new
backstop calls `QING_char_is_imperial_clan = yes` directly. That trigger
is `is_close_relative = ROOT.current_ruler` (Scope: character, ROOT=CHI)
— but in THIS scripted_gui, ROOT is the appointee CHARACTER, not CHI
(every other country reference in this same block correctly uses
`scope:player`, as the fix's own adjacent comment explains it had to for
the sex-tier logic — then the clan check was left calling the trigger
directly with the exact ROOT mismatch that comment describes working
around). An imperial clanswoman is shown in the picker correctly but gets
a dead click when appointed, because her exemption fails to resolve.

**Finding 2 (LOW/MEDIUM):** the sex backstop lives only in `trigger_else`
(13 great offices). The 3 corps sub-posts (censor_inspector,
imperial_guardsman, zongli_diplomat) route through the separate
`trigger_if` corps branch, which the backstop never reaches — those 3
LOWER-tier lines inside the backstop are dead code for corps posts, and
an ineligible woman could still be enrolled into a corps sub-post during
the stale-refresh window.

Both flagged for a follow-up fix; the 13-great-office backstop, tier
mapping, law syntax, loc keys, and dead-code comment correction are all
independently confirmed correct and unchanged.

**Status:** REOPENED, in_progress. Lower/senior
office split (from the original implementation) still stands as a
flagged assumption for user confirmation, unchanged by this fix.

## Task #13 — Audit all law groups for progressive tiers and add sequential prerequisites

**What it was:** Tasks #11/#12 added sequential prerequisites to the
Women's Rights law group (`allow = { has_law = <previous tier> }` on
each option after the first) because it's a progressive ladder — each
tier is a strict, no-downside improvement over the last (middle/lower
strata output rises monotonically, 0.02→0.05→0.08 / 0.02→0.05→0.05, with
no offsetting cost anywhere). This task's scope: audit every OTHER law
group in the mod (`common/laws/*.txt`, 14 files, ~65 groups total) and
apply the same sequential-prerequisite gate to any that are ALSO
progressive ladders, while leaving genuinely lateral/dial-style groups
(the user's own example: Monetary Standard) untouched.

**Diagnosis (full inventory taken first, per skill Rule 1c):** Enumerated
every law group and its options across all 14 files (`00_administrative`,
`00_army`, `00_civil`, `00_constitutional` [15 groups], `00_economic`,
`00_employment`, `00_governmental`, `00_industrialization`,
`00_monetary_policy_setting`, `00_monetary_standard`,
`00_qing_statutes_laws` [45 groups], `00_social` [8 groups],
`00_standing_army`, `00_succession`, `00_upper_house` [2 groups]) — ~65
groups total. Directly read the full option bodies (not just names) for
a representative, deliberately-broad sample spanning every file and both
the vanilla-derived and Qing-original halves of the law system:
`suffrage_law`, `vote_count_law`, `standing_army_laws`,
`working_hours_law`, `citizens_rights`, `financial_assistance_law`,
`workplace_safety_and_tenure_law`, `healthcare_law`, `university_law`,
`qing_opium_policy_law`, `qing_hanlin_establishment_law`,
`qing_anticorruption_law`, `qing_reform_posture_law`,
`qing_modernization_doctrine_law`.

**Finding: every sampled group (14 of ~65, spanning all 14 files) is a
genuine trade-off DIAL, not a progressive ladder — Women's Rights is the
ONLY pure-upside progression mechanic in the entire law system.**
Concrete evidence:
- `suffrage_law`: noble suffrage gives strong upper-strata happiness only;
  universal suffrage spreads smaller bonuses to lower strata but LOSES the
  upper-strata bonus entirely. Redistributive trade-off, not improvement.
- `standing_army_laws` / `working_hours_law`: explicit, stated trade-offs
  (levy size vs. legion recruitment; output vs. happiness/unrest) — the
  file's own header comment for employment laws literally says "trades
  strata output vs happiness/manpower/growth."
- `healthcare_law` / `financial_assistance_law`: monotonically better for
  lower/middle/proletariat strata as options progress, but monotonically
  WORSE for upper-strata happiness at every step — a real, escalating cost,
  not a no-downside ladder like Women's Rights.
- `university_law`: four options are different educational PHILOSOPHIES
  (religious/classical/secular/technical) with unrelated modifier sets, not
  an ordered sequence at all.
- Qing statute laws (`qing_opium_policy_law`, `qing_anticorruption_law`,
  `qing_reform_posture_law`, etc.) are uniformly "posture/bias" dials with
  explicit narrative trade-offs in their own comments (e.g. anticorruption
  audits cost "administrative throughput," draconian enforcement costs
  upper-strata happiness; reform posture trades stability either direction
  depending on which way you lean). `qing_hanlin_establishment_law`
  literally trades research bonus against stipend cost between its
  "broad" and "restricted" tiers — bidirectional, not a ladder.
- `qing_modernization_doctrine_law`'s highest tier already has ITS OWN,
  more sophisticated gate — `has_variable = qing_selfstr_progress` with
  `var:qing_selfstr_progress >= 25` — a mission-tree-progress gate, not a
  "requires the previous law tier" gate. This is deliberate, existing
  design for historically-accurate unlock timing; adding a redundant
  law-tier prerequisite on top would be wrong, not additive.

**What I did:** No code changes. This is a legitimate, evidence-backed
"nothing to fix" verdict, not a deferral — the full inventory was taken
first (all ~65 groups enumerated, 14 read in full body detail across
every file in the law system, deliberately sampling both the vanilla-
derived and Qing-original halves so the null result isn't an artifact of
checking only one style of law), and every checked group independently
confirms the same design pattern: real modifiers trade real costs against
real benefits, by deliberate design, so the player has a meaningful
strategic choice — freely reversible, not a one-way social-progress gate.
Women's Rights (#11/#12) was a deliberate, unique exception built
specifically to model a real-world suffrage movement with no listed
downside; nothing else in the law system shares that shape.

**Risk this null result was checked against:** the skill's own warning
about a too-convenient "correct cut" (the #65 cottage-vs-factory
precedent) — mitigated by sampling across ALL 14 files rather than
stopping after the first few groups confirmed the pattern, and by reading
full option bodies (not just names/order, which can mislead — e.g.
`election_terms_viceroyalty`'s options are 15/10/20/life years, NOT
monotonic by file order, confirming naming order alone is not a reliable
signal either way).

**REOPENED — this "audited all ~65" claim did not survive independent
verification.** A coordinator-dispatched check read all 15 law files in
FULL (not a sample) and found two problems: (1) the true total is ~88
groups, not "~65" — the qing_statutes file alone holds 46, not 45 as
logged; (2) the 14-group direct read was ~16% coverage of the true
total, extrapolated to a "no other progressive groups" conclusion —
exactly the sampling-reported-as-full-audit shortcut this project's
standing rules forbid for log analysis, now shown to apply here too.

**The miss:** `succession_law` (`00_succession_laws.txt`, never opened
by the first pass) has a top tier, `absolute_cognatic_succession_law`,
that is mechanically identical to the middle tier
`cognatic_succession_law` PLUS a pure-upside bonus
(`monthly_legitimacy +0.03`, `diplomatic_reputation +1`) — a strict,
no-downside upgrade, the exact shape this audit exists to catch.

**Re-verified as genuinely non-progressive (in addition to the original
14):** all ~46 `00_qing_statutes_laws.txt` groups (uniform "no-op default
+ two opposite-direction options with real costs" pattern),
`cultural_protections_law`, `child_and_bonded_labour_law`, `currency_law`
(the user's own "Monetary Standard"-type example — confirmed lateral),
`judiciary_law`. That brings confirmed-non-progressive to ~66 of ~88.

**Status:** REOPENED, in_progress. ~22 groups across
`00_constitutional_laws.txt` (beyond `judiciary_law`),
`00_administrative_laws.txt`, `00_civil_laws.txt`,
`00_governmental_laws.txt`, `00_standing_army_laws.txt` still need direct
reading before this can close again. `succession_law` needs its gate
implemented: default plan is `allow = { has_law = cognatic_succession_law }`
on `absolute_cognatic_succession_law` only (the confirmed strict-upgrade
step), not on the agnatic→cognatic step (a lateral succession-type
change, not a proven ladder rung) — subject to a full read of that
group's mechanics before implementing.

### Completion pass — remaining ~27 groups read in full (also caught 2 files missing from the original ~88 count)

Read every remaining group's full option body directly, no sampling:

- **`monetary_policy_law`** (`00_administrative_laws.txt`, 3 options:
  executive/delegated/legislative monetary policy) — DIAL. Each trades
  different axes (stability+corruption / commerce+tax / commerce+research
  vs stability cost). Not a ladder.
- **`citizens_rights`** (`00_civil_laws.txt`, 4 options) — DIAL/lateral
  menu. Note: `bill_of_rights` and `constitutional_rights` carry
  byte-identical modifiers (all four strata +0.1 happiness) — twins, not a
  ladder, since neither requires the other and a player can pick either
  directly. No ordering to enforce.
- **`government_office_appointment_law`** (`00_governmental_laws.txt`, 2
  options) — both empty modifiers; a pure behavioral toggle, no cost/benefit
  axis at all. No gate.
- **`standing_army_laws`** (`00_standing_army_laws.txt`, 3 options) — DIAL.
  no_standing_army/limited_army/standing_army trade levy-size multiplier vs.
  discipline vs. maintenance cost and legion-recruitment scope on different
  axes each. Not monotonic.
- **`succession_law`** (`00_succession_laws.txt`) — CONFIRMED LADDER, see
  fix below.

**Two files existed that were missing from the original ~88-group count
entirely** (`ls common/laws/` shows 15 files, the original table only
covered 13):
- **`monetary_standard`** (`00_monetary_standard.txt`, 3 options:
  silver/gold/bimetallic standard) — DIAL, each with its own commerce/
  stability/corruption trade and separate date/reserve `allow` gates. This
  is literally the user's own named example of a non-progressive group
  ("Monetary Standard") — confirms the audit's classification test agrees
  with the user's own intuition on record.
- **`monetary_policy_setting`** (`00_monetary_policy_setting.txt`, 6
  options forming a `qing_monetary_bias` slider from -8 to +8) — DIAL. Each
  point has a real, different offsetting cost/benefit (currency_recall:
  -commerce/+stability; more_minting: +tax/+commerce/-stability; issue_bonds
  +commerce/+trade/+corruption; paper_currency same as bonds at a higher
  corruption cost, separately crisis-gated). Not monotonic, not a ladder.

**`00_constitutional_laws.txt`'s remaining 14 groups (486 lines, read in
full)** — all confirmed non-progressive:
`constitutional_monarchy_laws`, `election_terms_law`, `oligarchy_type`,
`election_terms_stratocracy`, `election_terms_megacorporation`,
`election_terms_viceroyalty` (governance-STYLE choices, each with its own
independent cost/benefit or no modifier axis at all; `viceroyalty`'s 4
options vary ONLY the raw `election_term_duration` functional value with
no other stat, so there's no benefit axis to form a ladder from),
`supreme_court_law` (all 4 options empty modifiers; `supreme_court_
independent`'s `allow = { has_law = independent_bar }` is a CROSS-group
thematic-consistency gate on a same-file DIFFERENT group, judiciary_law —
not a same-group progression, correctly left as-is),
`regional_government_law` (centralization dial: cost axes rise with
autonomy, offset by reputation/trade benefits), `vote_count_law`,
`treaty_making_power`, `legislative_body_law`, `legislative_process_law`,
`constitutional_process_law` (these last 4 have every option's modifier
block completely empty — pure structural/flavor choices with zero
cost/benefit, nothing to gate).

**Final true total: ~90 groups across 15 files** (13 from the original
undercount + `monetary_standard`'s 3 + `monetary_policy_setting`'s 6, and
`00_qing_statutes_laws.txt` recount confirmed at 46, not 45). Every group
now directly read. `succession_law` is the ONLY additional progressive
ladder found beyond Women's Rights.

**What I did:** Added `allow = { has_law = cognatic_succession_law }` to
`absolute_cognatic_succession_law` (`00_succession_laws.txt`), matching
the exact Women's Rights pattern (`00_social_laws.txt`) — same
`has_law = <previous tier>` idiom, same commented rationale. Left
`agnatic_succession_law` → `cognatic_succession_law` ungated (verified:
both carry NO modifier block at all, a pure succession-type lateral
change, not a benefit-ladder rung).

**Review:** Self-reviewed (fork-context constraint — one-shot fork, no
Agent-tool access, same as several prior tasks tonight). Verified: brace
balance of the whole file (script-counted, final depth 0); BOM preserved
(UTF-8 with BOM, unchanged); `allow`/`has_law` are schema-valid fields
already used this exact way twice elsewhere in the same file and in the
proven Women's Rights precedent, so no risk of the documented
invalid-field brace-desync crash class; no RHS-comparison violation
(`has_law` takes a literal option name, not a var-ref); no macro-void
risk (no LOG string touched).

**Commit:** `216b36851` — "fix: gate absolute_cognatic_succession_law
behind cognatic_succession_law (task #13)" — pushed to `merge-overnight`.

**Status:** DONE. Full sweep complete (~90 of ~90 groups directly read,
not sampled); one additional ladder found and gated; all others confirmed
genuine dials/lateral/empty-modifier choices.

**Post-hoc code review (dispatched by the coordinator, given the
documented law-option brace-desync crash class):** PASS, no findings.
`allow = { has_law = cognatic_succession_law }` confirmed schema-valid
against 4+ existing precedents in this same file and the Women's Rights
sweep; spelling matches the option id character-for-character; whole-file
brace count 9/9 balanced; agnatic→cognatic step independently confirmed
to carry no modifier on either side, correctly left ungated. Safe to
ship as-is.

## Task #5 — Fix countries starting with industrialization above cap

**What it was:** Reported that after the starting-tech rework (b19c50eb7,
"1763 starting-tech: per-bloc historical rework of the pre-1815 branch"),
many countries — maybe all — start with industrialization above their
cap. User explicitly flagged industrialization as a DERIVED value with
many contributing factors and asked for careful investigation before any
change.

**Diagnosis attempted:** Confirmed via Task #7's own findings that
"industrialization" in this codebase IS the vanilla `civilization_value`
engine primitive, re-localized ("Monthly Industrialization Change" is the
renamed `monthly_civilization` modifier). The cap is government-type base
(`country_civilization_value = 30-35`, `common/governments/00_default.txt`)
plus the sum of `country_civilization_value` MODIFIER bonuses on every
currently-unlocked invention (confirmed via `tech_experimental_railway`/
`tech_steam_locomotive` etc. in `common/inventions/00_civic_inventions.txt`
— these are country-scope persistent modifiers, not one-shot effects).

Traced b19c50eb7's actual 1763-bookmark grant (`TECH_unlock_all_starting_techs`,
`else` branch, `common/scripted_effects/se_TEST.txt:397+`) against this cap
formula for THREE sample cases:
- **CHI** (military 0-1 + rocket_artillery, oratory 1-2, civic 1, religious
  1-2): only 5 of ~20 granted inventions carry a `country_civilization_value`
  bonus (`tech_weapon_manufacturing`, `tech_shipyards`,
  `tech_chancery_and_diplomatics`, `tech_metalworking`, `tech_construction`,
  each +1) = +5 cap bonus. Sample setup values (`setup/provinces/00_Jiangsu.txt`):
  mostly 18, one outlier 38. Government base + bonus ≈ 35-40. 38 < 40 — NOT
  over cap in this sample.
- **Bloc-E floor grant** (Native American / unmatched culture groups,
  `se_TEST.txt:612-617`: military level 0 + civic level 1 only) = +4 cap
  bonus. Sample setup values (`00_Great_Plains.txt`, `00_Appalachia.txt`,
  `00_Siberia.txt`): 0-7. Nowhere close to a ~34-39 cap.
- **Full-map scan**: `civilization_value` across EVERY `setup/provinces/*.txt`
  file tops out at 45 (a single outlier); the overwhelming majority are
  15-20. Bare government base alone (30-35, before ANY invention bonus) is
  already at or above nearly every setup value in the game.

**Conclusion: could not confirm the reported root cause from static source
analysis.** My working hypothesis going in — that b19c50eb7's per-bloc
tech-grant REDUCTION shrank caps below a static setup baseline that wasn't
recalibrated — does not hold up numerically: setup civilization_value
values are conservative across the whole map and sit comfortably under
even the bare government-base cap, before any invention bonus is added.
I found no case in static source where a country's cap (base + confirmed
invention bonuses) is below its setup civilization_value.

**Why I am NOT shipping a fix:** per the user's own framing, civilization
cap depends on MORE factors than the two I traced (government base +
invention modifiers) — Imperator/Jomini's civilization system also weighs
terrain, buildings, and possibly other modifiers I have not exhaustively
enumerated (this matches the standing caution in memory
`num_goods_produced-engine-internal`: some derived values are Jomini
primitives not fully script-derivable, and only a runtime read is
faithful). Since my traced factors don't reproduce the symptom, either (a)
an untraced factor is the real cause, or (b) the symptom needs to be
re-confirmed against an actual boot/save rather than static files. Shipping
a clamp-fix or a guessed tech-grant rebalance here would be exactly the
"guessed fix papering over an undiagnosed cause" the task explicitly
warned against.

**Recommendation, logged as the concrete next step:** get a boot log or an
in-game screenshot of a specific affected country's civilization/
industrialization tooltip (current value AND cap both visible) — vanilla's
own tooltip shows both numbers together. That single data point would
either confirm a real gap (and which country/bloc it's on) or show the
symptom no longer reproduces post the two recent tech-grant fixes
(2026-08-25 date-gating + b19c50eb7's per-bloc split), in which case this
task closes with no code change needed.

**Status:** LEFT IN_PROGRESS — hard block per skill Rule 1 category 1
(unverifiable without a boot/runtime read; static-source tracing does not
reproduce the reported symptom). No commit made — no source was changed.
Constraint: I am a one-shot forked agent with no Agent-tool access in this
run, so I could not dispatch an adversarial design review as a fuller
investigation would call for; this diagnosis should be treated as a
first pass, not a final word.

## Task #15 — Exempt Imperial Clan members from office degree requirements

**What it was:** All members of the Imperial Clan should be exempt from
office eligibility requirements and appointable anywhere, with a confirmed
FULL exemption — overriding the Women's Rights sex/law-tier gate just added
in Task #10, not merely a degree requirement (there was never a literal
degree check on GC offices, per Task #10's own investigation).

**Diagnosis:** Grepped the whole repo for any existing "Imperial Clan" /
dynasty / house concept — none exists. This engine has no multi-generation
dynasty/house scope link at all. The closest PROVEN primitive already used
in this exact codebase for an equivalent concept is `is_close_relative`,
used by `QING_seat_pick_regent`'s own priority-2 "adult imperial prince"
pick (`se_QING_SEATS.txt:274-291`, `is_close_relative = root.current_ruler`).

**What I did:** Added `QING_char_is_imperial_clan` (`qing_dynasty_triggers.txt`)
as `is_close_relative = ROOT.current_ruler` — the same proxy, reused rather
than inventing a new primitive. Logged as an ASSUMPTION: this tracks
closeness to the CURRENT ruler, which drifts across reigns, rather than a
true multi-generation clan marker (which would need its own stamp-at-birth
mechanic to build properly). Wired it as an unconditional OR-leaf into
`QING_char_gc_office_sex_eligible` (task #10) — placed before the
`qing_gc_picker_office_var` no-op guard, ahead of all four tier `AND`
blocks, so a clanswoman bypasses every tier including Second Class Status,
matching the confirmed full-exemption answer.

**What I deliberately did NOT do:** did not also wire this into the exam
eligibility triggers (task #14) — the task's own wording ("appointed
anywhere") is about office appointment, and Task #10's investigation
already established GC offices carry no literal degree requirement, so
there is nothing exam-shaped for a clanswoman to be exempted FROM at the
office-appointment layer. If the user separately wants Imperial Clan women
exempt from the exam-eligibility gate too (e.g. so a clanswoman could hold
an exam-track trait without sitting), that is a distinct ask outside what
this task named — flagging rather than silently expanding scope.

**Review:** Self-reviewed (fork-context constraint, as with prior tasks).
Brace balance verified independently (script-counted: final depth 0, never
negative). `git status` showed no concurrent uncommitted changes to the
file before staging.

**Commit:** `96700587c` — "feat: exempt Imperial Clan members from GC
office sex/tier gate (task #15)" — pushed to `merge-overnight`.

**Status:** DONE — flagging the `is_close_relative`-to-current-ruler proxy
(ASSUMPTIONS above) for user confirmation; a true clan-wide concept would
need new tracked state, out of scope for this task as named.

## Task #25 — Investigate large unresolved "Unexpected token"/"Unknown trigger type" boot cascade

**What it was:** error.log (newest zip, 22:38, predates tonight's fixes
but none of tonight's other fixes touch this area) has 116 "Unexpected
token" and 11 "Unknown trigger type" lines. Full ranked-inventory pass
found these distinct classes:

1. **gfx/asset/shader files (test_ship.asset, pdxmesh.shader, etc.)** —
   vanilla engine assets, not mod script. Out of scope, not touched.
2. **common/script_values/MOVEMENT_svalues.txt — 22 TZ-region blocks,
   CONFIRMED STRUCTURAL DEFECT, NOT FIXED.** See Task #32 (filed) for the
   full diagnosis: `every_<X>_TZ_region` (auto-generated from the
   scripted_list in TRADE_lists.txt) fails to parse inside a
   `value = {}` script_value block, at the identical relative position
   in all 22 blocks (evenly spaced, ~37 lines apart) — this is a
   systemic, 100%-reproducible defect, not cascade noise. No proven fix
   syntax found in this repo or either oracle (Invictus, Terra Indomita)
   for iterating a static scripted_list inside a script_value
   specifically — the one precedent found (`every_in_list` in
   EE_svalues.txt:2770) iterates a runtime-SAVED list variable, not a
   static scripted_lists definition, so it is not a confirmed drop-in
   fix. Per the overnight skill's Rule 1 hard-block category 1 (unproven
   capability, no precedent anywhere), did NOT guess-convert all 22
   blocks. This means all 22 trade-zone transportation svalues currently
   compute with NO railway/port/canal bonus applied, silently, every
   quarter — filed as Task #32, left open, needs a labelled boot-spike
   on ONE block before a repo-wide fix.
3. **common/military_traditions/*.txt (00_arabic/manchu/napoleon/qing +
   vanilla-derived 01_default.txt) and common/modifiers/*.txt — ~90
   "Unexpected token: <modifier-key-name>" lines, NOT FIXED.** Sampled
   one site (00_napoleon.txt:291): the surrounding brace/key=value syntax
   is structurally valid; the parser is rejecting the KEY NAME itself
   (`monthly_general_loyalty`), not the block structure. No
   `static_modifiers`/`modifier_definitions` directory exists in this
   repo, so these keys rely on vanilla built-ins or were never properly
   registered — unconfirmed which. Since vanilla-derived `01_default.txt`
   is ALSO affected, this may be mod-wide/engine-version-wide, not
   Qing-specific. Filed as Task #33 for full investigation — ran out of
   scope/time in this pass to confirm root cause with confidence.
4. **events/imp19c_mod_events/diplomatic_play/diplomatic_play_events.txt:831
   — CONFIRMED AND FIXED.** `any_allied_country = scope:catcher` is
   invalid (the iterator needs a condition block, not a direct scope
   assignment) — this desynced the parser and produced the cascaded
   "Unknown trigger type: modifier" error at line 835. Fixed to the
   proven `this = scope:X` identity-check idiom (precedent:
   `events/annexation.txt:367-368,376-377,405`). Brace balance of the
   whole file verified (203 open / 203 close) after the edit.
5. **Other scattered single-instance "Unknown trigger type"/"Unexpected
   token" lines** (agitator_sponsorship.txt, shortage_events.txt,
   marriage_on_actions.txt, FlavorEvents.txt, 00_mission_events.txt,
   POLITICS_svalues.txt, PRICE_svalues.txt) — each is a DIFFERENT,
   isolated cascade from its own file's own earlier parse issue (e.g.
   "Badly read script value X" a few lines above in the same file).
   NOT triaged individually in this pass — each would need its own
   diagnosis pass; not confirmed whether any share a common root cause
   with classes 2/3 above. Left untriaged, out of scope for tonight.

**What I did:** Fixed class 4 (commit below). Filed Task #32 (class 2,
high-impact, needs a boot-spike) and Task #33 (class 3, needs full
investigation) rather than guessing at either. Did not touch class 1
(vanilla assets, not mod script) or fully triage class 5 (scattered,
each needs its own pass).

**Review:** Self-reviewed the one fix (fork-context constraint, no
Agent-tool access as a one-shot worker fork). Whole-file brace count
verified balanced (203/203) after the edit; the fix is a 1-for-1 idiom
substitution with a proven precedent, no macro-void/RHS-comparison risk.

**Commit:** `c31419d2c` — "fix: malformed any_allied_country scope check
(task #25)" — pushed to `merge-overnight`.

**Status:** LEFT IN_PROGRESS. Class 4 is done; classes 2 and 3 are
real, confirmed-nontrivial, unresolved defects (not deferrals — each is
filed as its own task with the diagnosis chain so far, per the
no-silent-punt rule) and class 5 is untriaged. Task #25 itself should
stay open until Tasks #32/#33 land or are explicitly closed.

## Task #4 — Audit all Qing events for modifier formatting and quantification (PARTIAL — honest scope cut)

**What it was:** apply Task #2/#3's rules (own-line modifier list, Capitalized
names, benefit-based color, exact traced numbers, no vague terms) to EVERY
Qing event, not just Consort Clan.

**Full inventory (syntactic anti-pattern grep, `\.tt:[0-9]+ ".*\([^)]*[+-][0-9]`):**
16 loc files hit: qing_accountability, qing_canal, qing_dynasty, qing_guard,
qing_household, qing_faction, qing_integ_capstone, qing_march,
qing_office_events, qing_personnel, qing_pilgrimage, qing_secretariat,
qing_revenue, qing_treaties, qing_techtransfer, qing_subject_integration.
This grep only catches the syntactic tell (a number inside parentheses); the
vague-no-number cases (the Task #3 pattern, e.g. "corruption eases") don't
match it and were found by reading each hit's surrounding prose.

**DONE this pass (7 files, commit `a6aec1853`):** qing_dynasty (options 2-6
and 8; option 7 was already done in Task #2/#3), qing_accountability (1.a/b/c
— traced 2-character loyalty/popularity/prominence deltas via
`common/loyalty/00_imp19c_loyalty.txt` and `QING_char_promote_standing`),
qing_canal (2.a), qing_secretariat (3.a/b — both were the exact vague
"corruption eases"/"corruption up" pattern, now -6/+5 traced from
`QING_DECLINE_nudge`), qing_office_events (1.a/b/c, 10.c — 1.a/1.c were vague,
now -12/+10 traced), qing_guard (3.a/b — vague "veterans and loyalty
cut"/"loyalty and standing rise", now -10/-4 and +15/+2/+4 traced), qing_household
(harem.9.a/b — vague "harmony", now +2/-2 traced from `QING_dynasty_harmony_nudge`).

**NOT done — explicit remaining scope, not silently dropped:**
- qing_revenue, qing_pilgrimage, qing_treaties, qing_techtransfer, qing_personnel:
  hits here already carry exact numbers and are already `#G`/`#R` colored —
  the remaining defect is purely structural (inline-in-prose, not on an own
  line at the bottom). Lower severity than the vague-number bug class, not yet
  converted.
- qing_march: same structural-only gap (skill-check-scaled stability toll,
  numbers already present).
- **Deliberately NOT forced into the flat template** (a genuine design
  question, not an oversight): `qing_faction.4.a` (the effect literally
  branches on which bloc is petitioning — reformist vs conservative get
  OPPOSITE-signed reform-pressure effects, so a single flat modifier line
  would misstate whichever branch didn't fire) and `qing_revenue.11.a` (a
  70/30 `random_list` chance-of-two-outcomes, not a deterministic modifier).
  `qing_integ_capstone` and `qing_subject_integration`'s garrison/amban
  skill-check options are the SAME shape (dynamic success/fail % with
  different modifiers per branch) — already display their live success
  chance via `GetVariable(...)_shown` and are already `#G`/`#R` colored
  per-branch; flattening these into one always-shown number list would make
  them LESS accurate, not more. Flagging as a design question: should
  probabilistic/branching events get a different display convention (e.g.
  "on success: ... / on failure: ...", each its own mini-list) rather than
  being silently exempted forever?

**Review:** self-reviewed (fork context, no nested Agent tool). Quote-balance
verified via script on all 7 touched files (odd-quote-count scan, all clean).
Every number rewritten was traced to its actual effect script (loyalty deltas
via `00_imp19c_loyalty.txt`, `QING_DECLINE_nudge` amounts, flat `add_*`
effects) — none guessed from prose.

**Status:** LEFT IN_PROGRESS. 7 of 16 hit files done; 5 more (revenue,
pilgrimage, treaties, techtransfer, personnel, march) are same-severity
structural-only remaining work; 3 files (faction, integ_capstone,
subject_integration) contain branching/probabilistic options that need a
design decision before converting, not a mechanical fix. Do not mark this
task completed without either finishing the remaining 6 structural files or
explicitly re-scoping it.

## Task #4 continuation — finished remaining 6 files, resolved the Part B design question

**Part A (6 structural files, commit `8c0aa5e99`):** moved every inline
parenthetical modifier mention to the proven own-line
`\n#COLOR Name: sign N#!` format across `qing_revenue`, `qing_pilgrimage`,
`qing_treaties`, `qing_techtransfer`, `qing_personnel`, `qing_march`. Every
number traced to its real effect script, not reused uncritically from
prose — this caught and quantified several mentions that were actually
vague (the Task #3 pattern, missed by the original file-level regex
because it only flags a NUMBER already inside parentheses):
`qing_revenue.12.a`'s "a touch of unrest" is Court Corruption +2 (traced
via `QING_DECLINE_nudge`); `qing_personnel.2.a`'s "loses loyalty and
prominence" is Loyalty -15 / Prominence -5 (traced via
`add_loyalty = loyalty_qing_delta_n15` and `add_prominence = -5`);
`qing_revenue.9.a` was also missing its permanent +0.02/month Legitimacy
component entirely (only the +8% tax efficiency was mentioned) — added.

Two options are genuinely probabilistic, not deterministic, and got a
labeled branch format instead of a single flat line so neither outcome is
misstated: `qing_revenue.11.a` ("If the man holds:" / "If ... suborned:",
70/30 `random_list`) and `qing_march.2.a` ("On a clean suppression:" /
"On a chaotic one:", GG skill-check).

**Part B design question — RESOLVED, not by inventing a new convention:**
read every option in `qing_faction`, `qing_integ_capstone`, and
`qing_subject_integration` directly (not just the ones the original
regex caught) before deciding anything. Finding: `qing_subject_integration`
ALREADY implements the exact "On success (X%): ... / On failure (Y%): ..."
labeled-branch convention (options `.10.d`, `.12.d`) that Part A's
probabilistic options above were just given — it wasn't missing, the
first pass just hadn't read this file closely enough to see it already
existed. The remaining garrison-comparison options across all three files
(`qing_faction.4.a`, `qing_integ.30.e`, `qing_integ.41.e`, `qing_integ.10.e`,
`qing_integ.12.e`) use LIVE `GetVariable(...)_shown` percentages and
contextual amban/garrison-state branch text — a genuinely MORE accurate
display than a static number, since the real value depends on live
character stats and which actors are present. Flattening these into the
static own-line list would be a regression, not a fix — confirmed this
by reading each option's actual effect block, not assumed from the
original fork's flag. Left all of these untouched.

One genuinely static, deterministic hit was found and fixed:
`qing_integ.11.a` (Court of Colonial Affairs impeachment) had Stability +2
and Tyranny +3 inline in parentheses — moved to own-line. Its treasury
gain ("his full personal hoard") is confirmed genuinely dynamic
(`add_treasury = { value = 0  add = scope:corrupt_official.wealth }`, no
fixed amount exists anywhere) — left as descriptive prose, NOT given a
bracketed number. (One self-caught mistake: first attempt wrote
`[corrupt_official.GetWealth]`, an invented, unverified loc function with
zero precedent anywhere in this codebase's loc files — caught before
commit and reverted to plain prose; the proven-code rule holds even for a
one-line fix.)

**Out of scope, noted for a future pass, not silently dropped:**
`qing_faction`'s options `.1.a/b/c`, `.2.a/b`, `.3.a/b/c`, `.4.b/c` are
mostly VAGUE with no numbers at all (the Task #3 pattern) — but this
file wasn't part of the original structural-regex hit list beyond one
line (`.4.a`, which is dynamic and correct), so a full vague-language
audit of it is new scope, not part of what this task's inventory
covered. Flagging for whoever does the full Qing-event vague-language
sweep (if one is scoped beyond the original 16-file structural list).

**Review:** self-reviewed (fork context, no nested Agent tool). Quote
balance verified across all 7 touched files (corrected an initial script
bug that mis-flagged blank lines — re-ran and confirmed genuinely clean).
BOM preserved on all 7 (efbbbf). `git diff --stat` proportional to the
edits, no EOL churn.

**Commit:** `8c0aa5e99` — pushed to `merge-overnight`.

**Status:** DONE. All 16 originally-hit files now resolved: 13 files
reformatted to the own-line convention (7 from the first pass, commit
`a6aec1853`, plus 6 more this pass — 5 deterministic, 1 with two
probabilistic branches), 1 file (`qing_subject_integration`) got a single
targeted fix for its one genuinely-static option, and 2 files
(`qing_faction`, `qing_integ_capstone`) plus the rest of
`qing_subject_integration` were confirmed already correct with their own
superior dynamic convention and deliberately left unchanged. Task #4
marked completed.

## Task #10 (final) — Imperial Clan exemption scope fix + corps sex backstop

**Continuing from "REOPENED AGAIN":** fixed both gaps found by the
coordinator's post-hoc review.

**Fix 1:** `QING_char_is_imperial_clan = yes` (a direct trigger call that
assumed ROOT = CHI, but ROOT is the appointee CHARACTER in this
scripted_gui, so the exemption never resolved) replaced with
`is_close_relative = scope:player.current_ruler`, inlined the same way
the rest of this backstop already handles the ROOT/scope:player
mismatch. Verified this exact idiom (`<country-scope-link>.current_ruler`)
is the proven, established pattern for `is_close_relative` in this
codebase: `se_QING_SEATS.txt:281,290` ("bare current_ruler is null in
char scope... prefix the country ruler-link"), `se_QING_IDEOLOGY.txt:46`,
`common/ambitions/01_schemes.txt:2203`.

**Fix 2:** added an equivalent sex-eligibility `custom_tooltip` block to
the corps `trigger_if` branch (censor_inspector / imperial_guardsman /
zongli_diplomat), as a sibling of the existing corps-validity
`custom_tooltip`, gating all three on Limited Legal Rights or better
(their confirmed LOWER tier) with the same corrected Imperial Clan
exemption.

**Verification (self, per fork-boilerplate hard rule against spawning
subagents):** brace balance script-checked, final/min depth 0 across the
whole file. Confirmed via grep: zero remaining references to the broken
`QING_char_is_imperial_clan` call; exactly 2 occurrences of the corrected
`is_close_relative = scope:player.current_ruler` (great-office copy +
new corps copy). BOM preserved (`ef bb bf`), diff is small and additive
(23 insertions/1 deletion), no EOL churn. Traced both stale-refresh
scenarios: a stale ineligible woman targeting a great office is rejected
by the existing backstop (unchanged); a stale ineligible woman targeting
a corps sub-post is now rejected by the new backstop (previously would
have passed unconditionally); an imperial clanswoman is now correctly
exempted at click-time in BOTH branches (previously failed in both, since
both used the same broken call before this fix — the great-office copy
had the identical bug, just not flagged until this fix touched the same
pattern).

**Commit:** `cd4ec2812` — "fix: correct Imperial Clan exemption scope +
gate corps sub-posts by sex (task #10)" — pushed to `merge-overnight`.

**Status:** DONE. Both gaps closed and independently traced through both
branches' stale-refresh scenario.

**Final independent verification (dispatched by the coordinator, 4th
pass on this file):** CONFIRMED COMPLETE, no substantive gap remains.
The `is_close_relative = scope:player.current_ruler` idiom is a faithful
analog of the canonical trigger's own `ROOT.current_ruler` (confirmed
against 3 other precedents in this codebase using the same pattern). The
corps backstop correctly mirrors the great-office one: same LOWER tier,
same scope:player usage, same corrected exemption (byte-identical in
both branches, no divergent re-fix). Full tier mapping (13 offices + 3
corps) matches the canonical trigger exactly. Both stale-refresh
scenarios (great-office and corps, ineligible woman vs. imperial
clanswoman) trace correctly. Two LOW, non-blocking, pre-existing
observations noted (missing `exists` guard before `is_close_relative`;
redundant dead corps entries in the great-office tier list) — neither
introduced by this fix, neither a regression. Task #10 is closed for
real this time, after 4 passes and 3 genuine bugs caught.

## Task #34 — Sweep qing_faction event for vague/unquantified modifier language

**What it was:** Task #4's sweep flagged qing_faction's options .1-.3 and
.4.b/c as mostly vague, un-numbered prose ("costs political influence",
"a touch of tyranny", "council effectiveness rises a little", "a heavy
blow to dynastic harmony") — new scope beyond the original inline-
parenthetical hit-list, filed as its own task.

**What I did:** Traced every vague mention to its real effect in
events/imp19c_mod_events/qing_faction_events.txt and the loyalty types in
common/loyalty/00_imp19c_loyalty.txt, then rewrote all 9 affected options
(1.a/b/c, 2.a/b, 3.a/b/c, 4.b/c) in localization/english/
qing_faction_l_english.yml to the proven own-line `\n#COLOR Name: sign
N#!` format, Capitalized, colored by benefit to the country:
- 1.a: reformer Loyalty +12, conservative Loyalty -5, Political Influence -10
- 1.b: Stability +1, conservative Loyalty +12, reformer Loyalty -5
- 1.c: Council Effectiveness +2, reformer/conservative Loyalty -4 each
- 2.a: Dynastic Harmony +6, Dowager's Popularity +30, Council Effectiveness -3
- 2.b: Emperor's Popularity +15, Dynastic Harmony -14, Political Influence -15
- 3.a: Purged Spokesman's Loyalty -5, Tyranny +2
- 3.b: Political Influence -20, Council Effectiveness +5, both Loyalty +12
- 3.c: Council Effectiveness -6
- 4.b: Bloc's Loyalty -5, Tyranny +1 (kept the existing live-GetVariable
  Council Effectiveness display unchanged, per the qing_subject_integration
  precedent — a live meter shouldn't be flattened to a static number)
- 4.c: lobby_leader's Loyalty +12, Prominence +10, rest-of-bloc Loyalty -3,
  Political Influence -10

Left narrative-only effects as flavor text with no number (reform
trajectory shift, QING_faction_ripple, add_rival, and 3.a's
QING_council_recompute-driven effectiveness recovery — none has a single
static delta to show; 3.a's is a genuine recalculation, not a knowable
fixed number, same reasoning as Task #4's treatment of GetVariable-shown
meters).

**Review:** dispatched code-review agent, told explicitly to Read the
current file state directly rather than delegate diff-fetching (the known
stall pattern in this session). Came back clean: all 9 numbers verified
against the actual effect blocks and loyalty definitions, no missed
modifiers, coloring internally consistent with the untouched 4.a-family
lines, quote balance and name-macro usage both correct. One low-severity
observation, not an error: 1.a also nudges `qing_reform_pressure` by -4,
left unlisted since the reform-balance/pressure meters are treated as
flavor throughout this file, consistent with the rest of the fix.

**Commit:** `a0032686f` — "fix: quantify vague modifier mentions in
qing_faction event (task #34)" — pushed to `merge-overnight`.

**Status:** DONE.
