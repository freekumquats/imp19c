# Overnight run — 2026-08-18

Autonomous backlog run on branch `merge-overnight`. Log-error cleanup pass:
the boot log's top error classes, worst-first. All commits as freekumquats,
pushed after each task (user boot-tests on a separate machine).

## ASSUMPTIONS & GUESSES (scan this first)

Every value/decision made WITHOUT boot data, with the log line that confirms it:

- **#11 root cause is NOT boot-proven.** Two theories were refuted in review
  (zeal-gap arithmetic; then whole-body wrap). The applied fix (guard the
  `this`-stat block behind `is_alive = yes`) is a can't-hurt hardening of
  exactly the statements that can throw on a dead-but-existing scope. The
  newest log is pre-#8, so the exact flood path (canton.2.a) no longer exists
  in HEAD and cannot be re-validated against that log.
  - **CONFIRM ON BOOT:** absence of the three `QING_char_affinity` error
    messages ("Failed to fetch qing_char_affinity", unset-scope, invalid-left)
    in error.log. They were 4,566 each (13,698 total) — the #1 class.
- **#9 has no tunable guesses** — a mechanical strip of dead tokens. Confirm on
  boot = the "Could not find data system function 'GetTag'" class drops to zero.
- **#12 has no tunable guesses** — a `has_variable` pre-guard. Confirm on boot =
  the `var:CPI_annual` fetch-unset class (~893/boot) drops to zero.

## Tasks

### #8 — Censorate two-event split (DONE, `043acc1dd`, pre-this-session)
Split the courtier-censure path from the corrupt-officeholder path; re-gated
`qing_canton.2` to the non-censure branch. Retired the `canton.2.a` impeach
option (moved to `qing_censorate.11`). Recorded here for the run's audit trail.

### #12 — CPI tooltip unguarded `var:CPI_annual` read (DONE, `bee69f60c`)
- **What:** the `cpi_value_text` customizable_localization deflation branch read
  `var:CPI_annual < 0` with no existence guard. `CPI_annual` is set only on a
  country's first quarterly CPI pulse (se_CURRENCY.txt bootstrap), so the strict
  `var:` accessor threw ~893/boot before that pulse.
- **Fix:** prepend `has_variable = CPI_annual` to the trigger. A false trigger
  falls through to the default `cpi_info` key (GUI `GetVariable` renders 0
  harmlessly). No behaviour change once the var is set.
- **Review:** CLEAN.

### #13 — Art Patronage invalid culture keys (DONE, `5b52c6302`)
- **What:** the Suppress-the-Jesuits visibility gate matched `culture = italian`,
  but `italian` is a culture GROUP, not a culture — 30 errors/boot, and it
  cascade-flagged the valid `portuguese` on the same line.
- **Fix:** match the group via `culture.culture_group = culture_group:italian`;
  keep `culture = portuguese`. Comment records the distinction.
- **Review:** CLEAN.

### #9 — Strip non-rendering `[X.GetTag]` LOG tokens (DONE, `2be51d084`)
- **What:** ~330 `[ROOT.GetTag]` / `[scope:target.GetTag]` tokens sat in
  diagnostic LOG strings. `debug_log` in effect context does NOT evaluate
  `[...]`; the engine tooltip-preview localizer then fails on the unknown
  `GetTag` function and floods error.log.
- **Key decision — STRIP, not replace.** First plan was `GetTag → GetDebugTag`.
  Reading se_ECON_LOG.txt:664-708 + se_LOG.txt:49-64 + the qing_integ.42
  precedent proved `debug_log` does not render `[...]` in effect context at all,
  so `GetDebugTag` would fail identically. A uniform strip (over a literal `CHI`)
  is correct because some callers are generic (ROOT ≠ always CHI, e.g.
  currency_crisis.1). This matches the established convention (1511 sites already
  stripped; the 2026-08-06 logfix used a literal).
- **Scope kept tight:** only the two GetTag tokens removed. Valid brackets
  (`MakeScope.GetVariable().GetValue`, `current_ruler.GetName`) left intact.
  Comment lines discussing the tokens preserved.
- **Verified:** 52 files, exactly 304 insertions / 304 deletions (pure
  replacements); zero live GetTag left in any LOG string; all 52 files
  brace-balanced; no trailing/double spaces, no dangling labels, no empty parens;
  no EOL/BOM churn; the 5 comment anchors intact.
- **Review:** dispatched code-review + independent full mechanical verification;
  all check points pass.

### #11 — `QING_char_affinity` Script-system-error flood (DONE, `4b99dd44e`)
- **What:** the #1 log-error class — 13,698/boot (three message types, 4,566
  each). `QING_char_affinity` scores the CURRENT character (`this`) and reads
  its attributes. On a dead-but-existing `this` (a saved/derived scope whose
  character died between save and use), those stat reads threw all three types
  per call. The old `exists = root.current_ruler` guard covered the WRONG scope.
- **Fix (endorsed Required #1):** add `is_alive = yes` to that limit so a
  dead/stale `this` skips the stat block cleanly (`is_alive` is a native trigger;
  returns false, no throw). The neutral default (`set 50`, line 47) and the
  0-100 clamp stay UNCONDITIONAL and outside the guard.
- **Why no caller guards (Required #2 rejected):** `set_variable` persists on a
  dead-but-existing char, so line 47 always sets the default; the ~13 unguarded
  caller reads of `var:qing_char_affinity` therefore always see 50, never
  fetch-unset. Review confirmed `set_variable` on the just-dead ROOT is proven
  (on_character_death runs `add_gold`/`remove_variable` on it).
- **Review:** CLEAN — fix is COMPLETE as-is; all 6 verify points PASS; 41 call
  sites across 18 files all open a CHARACTER scope, so `is_alive` never runs
  off-scope; live-`this` behaviour identical to before; braces balanced.
- **Diagnosis trail:** design/DESIGN_11_AFFINITY_ZEALGAP_FLOOD.md (two refuted
  theories + final resolution).

## Adjacent items found, logged for the backlog (NOT fixed here)
- `QING_censorate_impeach_uphold` is also called from `qing_censorate.7`, a
  CHARACTER event where ROOT = the accused, not CHI. On that path
  `root.current_ruler` is invalid, so the ruler-relative scoring is skipped and
  affinity stays a flat 50 — a silent SCORING inaccuracy, not an error. Separate
  concern; not the flood.
