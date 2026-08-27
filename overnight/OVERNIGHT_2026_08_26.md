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

**Status:** DONE.
