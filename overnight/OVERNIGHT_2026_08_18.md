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
- **#5 vegetables reseed sizing = GUESS.** Target each collapsing zone to veg-province count
  ≈ 0.15 × its food-province count + 25% margin, breadth-first across governorships. The
  earlier probe-first sizing is blocked because raw demand is obscured by supply-scaling
  (#14), so this reverts to a survivor-ratio target with margin (glut self-damps, so erring
  high is safe). CONFIRM ON BOOT: the ~19 collapsing zones' vegetables `stock` band stops
  hitting 0 and `price` stays low; if a zone still collapses, raise that zone's margin.
- **#14 demand ratchet (task #15) is a PROVEN mechanism but its fix is NOT shipped** — correct
  fix form unclear + impact unproven vs supply. Gated on the #5 reseed boot. Called out loud,
  not deferred silently.
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

### #10 — Over-skilled character stat distribution (VERIFIED ALREADY-SHIPPED)
- **What:** minted GC officeholders / garrison courtiers were too skilled on
  average; target profile = per character ONE low (1-3), TWO mid (4-6), ONE
  domain-keyed peak (7-12), with natural exceptions from ranged rolls.
- **State found this run:** designed + implemented + code-reviewed + committed
  in the prior session (Task 3, 2026-08-17; design doc
  DESIGN_CHARACTER_STAT_DISTRIBUTION.md, incl. a resolved MEDIUM finding that
  moved the council peak from the degree trait to the office GOVERNING SKILL).
- **Verified in current code (working tree clean):**
  - `qing_war_events.txt` war.5/.6 — peak `add_martial {8 12}`, mids at 5, one
    genuine low per block (zeal=2 / charisma=2 / finesse=3, varied).
  - `se_QING_COUNCIL.txt` `QING_council_autofill_office` — uniform base
    `martial {1 3}` / `finesse {1 3}` / `charisma {4 6}` / `zeal {4 6}` plus a
    `add_$domain$ {3 6}` booster keyed to `QING_council_score_office`.
  - `se_QING_SUBPOSTS.txt`, `se_QING_EXAM.txt` — peak / low / two-mid bands.
  - Probe in `QING_council_apply_officer_buffs` (debug-gated) logs each seated
    member's 4 attributes.
- **CONFIRM ON BOOT (documented assumption):** engine base ≈ 0. If the officer-
  buff probe shows systematic overshoot past 12, the degree-trait bonuses
  (jinshi +3 fin, wu_jinshi +3 mar, etc.) are the first tuning lever. Shipped
  best-guess, tune next round — not a deferral.

### #14 — Vegetables trade-zone collapse (IN PROGRESS; diagnosis CORRECTED mid-task)
Full diagnosis: design/DESIGN_14_VEGETABLES_DEMAND_COLLAPSE_DIAGNOSIS.md.
- **First inference (WRONG, corrected):** I argued "order→0 proves demand-side, so the #5
  reseed is the wrong cause" and started two fixes on that basis — (a) re-enable the ±10%
  food-demand clamp in se_DEMAND.txt, (b) guard a div/0 at se_GLOBALTRADE_split.txt:3340.
- **Adversarial review REFUTED the inference, and I verified the refutation in source:**
  `GT_split_modify_fulfillable_order_sizes` (se_GLOBALTRADE_split.txt:3390-3486) multiplies every
  zone's `total_order_size` by `global_supply%/order`, so the logged `order` is supply-scaled →
  `order→0` is a mechanical consequence of a STOCK collapse, not proof of demand collapse. And a
  demand collapse would make stock GROW, but stock→0 is observed. **PRIMARY cause = SUPPLY
  shortfall → #5 reseed is valid and NOT superseded.**
- **Both my first fixes were WRONG and are REVERTED (git stash `wf14-speculative...`):**
  - The ±10% clamp is NOT dead-by-accident. It was MOVED to the svalue read-side in the Aug 6
    `_new` refactor: `DEMAND_food_svalues_new.txt` clamps each food svalue on read to
    [previous_90pct, previous_110pct]. Re-adding the effect-side clamp is redundant/harmful.
  - The div/0 is NOT at :3340. The error.log stack traces (authoritative) point to
    `GT_set_tradegood_price line 3` and `GT_split_update_wealth_owed_for_tradegoods line 12` —
    scriptvalue divides whose source line I could not map by inspection (all obvious divides look
    guarded). I did NOT ship a third guess; delegated a strict log-driven pinpoint (agent diag-div0).
  - LESSON: two fixes reasoned from plausible mechanism, both contradicted by the actual log.
    Reverted to strictly log-driven per imp19c-logs.
- **Demand ratchet (task #15, split out):** the svalue read-clamp + bands-set-from-clamped-read
  compound into a ratchet (floor decays 10%/tick, recovery capped +10%/tick). PROVEN mechanism,
  but the correct FIX form is unclear (naive "bands from raw" may just disable the rate-limiter)
  and its IMPACT vs supply is unproven in a 9-quarter boot. Shared food-demand logic, un-boot-
  testable → own design pass, gated on the #5 reseed boot. Tracked openly as #15, not buried.
- **#5 reseed (primary supply fix):** implementation delegated (agent impl-veg-reseed, worktree);
  I code-review the diff+manifest before commit.

## Adjacent items found, logged for the backlog (NOT fixed here)
- `QING_censorate_impeach_uphold` is also called from `qing_censorate.7`, a
  CHARACTER event where ROOT = the accused, not CHI. On that path
  `root.current_ruler` is invalid, so the ruler-relative scoring is skipped and
  affinity stays a flat 50 — a silent SCORING inaccuracy, not an error. Separate
  concern; not the flood.
