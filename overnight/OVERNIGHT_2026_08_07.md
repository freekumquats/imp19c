# Overnight Autonomous Run — 2026-08-07

**Branch:** merge-overnight. **Author:** freekumquats. **Mode:** autonomous.
**Rules honoured:** review-before-commit (adversarial review on every change); major tasks get a
design doc + adversarial design review before implementation; push after commit (user boot-tests
on a separate machine); log every decision here.

Started from the boot-test log triage (logs.zip Aug 7 03:24) + the standing task list #19–#28.

---

## Decision log

### [T0] Log triage (logs.zip Aug 7 03:24) — verdict
Ran the full imp19c-logs triage. error.log 343k lines / debug.log 500MB — flood is almost entirely
KNOWN upstream/econ read-before-set noise (EDU_svalues 88k, var-unset 45k, governorship_population
21k, shipping/stockpile warm-up). Only **1** compile failure and it's in a DEBUG file
(events/DEBUG/timetest_quarterly_tick.txt) — not shipped. No new error classes from today's commits.
Two genuine low-count MOD bugs surfaced → fixing:
- **BUG A** `QING_pop_recompute_target` (se_QING_POPULATION.txt:79): `limit = { total_population > 0 }`
  is a PROVINCE-only trigger used in a COUNTRY-scope effect → "Wrong scope for trigger" ×8. The
  crowding term of the Malthusian pop-pressure meter may skip.
- **BUG B** `ROOT.GetTag` data-function fails feeding loc key PROVINCE_TOOLTIP
  (map_tooltips_l_english.yml:3) ×23 — a loc-scope-syntax issue in a mod province tooltip (cosmetic).

### [T1] BUG A fix — pop_recompute country-scope trigger
Changed the guard `total_population > 0` → `country_population > 0` (the proven country-scope pop
trigger, EE_lists.txt:38). Kept the calibrated `total_population`/1200 VALUE on the next line (the
engine coerces total_population as a value at country scope; only the TRIGGER form errored).
Minimal, scale-preserving. Pending code-review before commit.

### [T2] BUG B — RETRACTED (not ours to fix)
`ROOT.GetTag` failure feeds loc key PROVINCE_TOOLTIP (map_tooltips_l_english.yml:3). Investigated:
`$OWNERSHIP$` is an ENGINE-INJECTED tooltip parameter (not defined in mod loc/custom-loc anywhere),
and the failing `ROOT.GetTag` originates inside the engine's `$OWNERSHIP$` expansion where ROOT is
not a country. The `PROVINCE_TOOLTIP:4` line was authored by MIUNO (base mod, 2025-03-20), NOT by
freekumquats; the mod's only edit is the trade-zone tail (Sobisonator). Per the vanilla/upstream-
caution rule + proven-code rule, do NOT edit a stock tooltip key on a hunch — cosmetic (23x hover
artifact over 2 in-game years), and touching it risks breaking the standard province tooltip.
DECISION: leave as-is; not a mod bug. No change.

### [T3] Autonomous plan for the task list
User directive: work autonomously; for MAJOR tasks draft a design doc + adversarial design review
BEFORE implementing; review ALL changes with code-review before committing; log decisions here.
Task triage by size:
- MAJOR (design doc → adversarial review → build → code-review): #19 (concrete garrison link),
  #26 (amban picker), #27 (senior-minister scandal chain), #22 (Scandal redesign), #23 (deflation
  diagnosis → fix), #28 (currency logging), #20 (khoja-chain garrison options — depends on #19/#21).
- MECHANICAL (build → code-review): #21 (seed Altishahr garrisons — once research lands), #24
  (C-chip suppression — proven idiom exists).
- Ordering: #23+#28 are coupled (logging enables the deflation diagnosis). #19→#20→#21 garrison
  chain is coupled and blocked on the re-dispatched Xinjiang garrison research. #24 is independent
  and quick. Start with the currency-logging design (#28) since it unblocks #23, and #24 in parallel.
Re-dispatching the failed Xinjiang garrison research agent (died mid-write on an API error).
