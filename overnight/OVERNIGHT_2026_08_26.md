# Overnight run — 2026-08-26

## ASSUMPTIONS & GUESSES
(none yet — Task #1 required no guessed values; the target tan color and layout
were both copied verbatim from an existing vanilla loc string, not invented.)

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

**Status:** DONE (confirmed fix shipped + pushed). `qing_pos_marker_ct`
cascade NOT independently fixed — see hypothesis above; recommend checking
its count on the next boot before deciding whether it needs its own task
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
