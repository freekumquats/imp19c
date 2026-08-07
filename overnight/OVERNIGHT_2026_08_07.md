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

### [T4] BUG A committed — a6bf29bf2
Pop-scope fix reviewed CLEAN (country_population is a proven country-scope trigger; calibration
untouched; line-59 seed neutralizes the one theoretical co-warming residual). Committed.

### [T5] #28 currency-logging DESIGN DOC drafted → adversarial review dispatched
Wrote design/DESIGN_CURRENCY_LOGGING.md. CRUX finding baked into the design: value-rendering into
debug.log is a KNOWN TRAP — both prior ECON_LOG snapshot bodies were REMOVED because
[ROOT.MakeScope.GetVariable(...).GetValue] emits "Could not find promote for 'MakeScope'" and logs
nothing. Design mandates a PROBE-FIRST approach (verify a real number lands before wiring sites).
Adversarial design review running. Will NOT build until the review + a working render form is confirmed.

### [T6] #24 C-chip suppression — BUILT, review dispatched
Root-caused: the shared PartyIcons block (gui_base.gui:5775, inside cpt_button 5648) has a govt-type
exclusion, but it still leaks on event portraits + Diplomacy view. Applied the PROVEN flat
blockoverride "PartyIcons" {} (same as characters_view.gui:1312 / qing_lifanyuan.gui) at:
  - gui/eventwindow.gui: the event_portrait template's cpt_button (1 site).
  - gui/diplomatic_view.gui: all 4 ruler/character cpt_buttons (ruler/horde/monarch/secondary-heir);
    a 5th pre-existing #86 override at :2852 is unrelated.
Braces balanced both files. code-review dispatched — flagged the deliberate tradeoff (this also hides
a REAL republic's party chip in these views, consistent with directive #47 "nobody shows C" + the 3
prior global fixes). Awaiting review before commit.

### Agents in flight (as of T6)
- garrison research (redo) → research/RESEARCH_QING_XINJIANG_GARRISONS_1763.md (for #21)
- #28 design review
- #24 code-review
Next once these land: commit #24 if clean; act on #28 review (probe or redesign); build #21 from the
research; then tackle the MAJOR design docs (#19, #26, #27, #22, #23).

### [T7] #23 deflation — LEADING HYPOTHESIS formed, BLOCKED on #28
Code trace: the annual reset is likely the DENOMINATOR private_cash_needed (CURRENCY_svalues.txt:719)
swinging once a year — it has `subtract = CURRENCY_trade_wealth_outgoing_currency_value` and there's a
`quarterly_reset_trade_transaction_totals` on_action (oa_wealth_changes.txt:268). If trade totals
accumulate then reset on a yearly boundary, private_cash_needed jumps → ratio drops → deflation FLOOR
(-10%), swamping the numerator (minting). Same undamped-feedback family as #14. CANNOT confirm which
term resets without the #28 per-cycle trace → #23 is sequenced BEHIND #28. Do NOT touch the shared
upstream currency formula on a hunch (upstream-caution + proven-code rules); CHI-safe damping/deadband
is the likely fix once confirmed. Recorded in task #23.

### [T8] #26 (amban character-picker) DESIGN DOC drafted → adversarial review dispatched
Wrote design/DESIGN_AMBAN_PICKER.md, grounded in the PROVEN Censorate "Commission an Inspector" picker
(4-onclick button → set picker var → refresh candidates → createwidget picker window; row-click handler
dispatches). Key risks flagged: R2 (is qing_office_picker_window reusable or must build a parallel window),
#34 crash rule (post via trampoline, never inline the sorting iterator), feeding a PICKED char through
QING_amban_wire (which currently DRAWS its own). Review running.

### [T9] #28 currency-logging — DESIGN v1 REVIEWED (SOUND-WITH-FIXES, central deliverable INFEASIBLE) → REWROTE to v2
The v1 review was decisive: (1) NO working numeric-value render exists in the repo — every .GetValue/
ScriptValue is a comment-documenting-failure or a GUI/loc display string; the MakeScope promote fails in
script debug_log. My cited "proof" (WAR_scripted_effects.txt:24) is a .GetName STRING with a commented-out
call site. (2) #23 is likely MISDIAGNOSED: there is NO annual reset — the -10% is the deflation formula's
EQUILIBRIUM CEILING (deflation=(1-ratio)/10, ratio floored, recomputed quarterly). My "yearly site" has NO
currency logic (red herring). (3) The PROVEN idiom is already in se_ECON_LOG.txt:300-486 — band-bucketing
(stage script_value into temp → classify with sentinel comparisons → emit a band LABEL, no render).
REWROTE design/DESIGN_CURRENCY_LOGGING.md to v2: band-bucketing (no render), retargeted to MONTHLY (minting
+ minting-cap-hit) and QUARTERLY (ratio band, denominator band, reserve-correction band) sites, yearly site
DROPPED. #23 reframed: the trace will distinguish "equilibrium under a starved money supply (balance issue)"
from "a bug" — do NOT assume annual reset. v2 re-review dispatched before building.

### [T11] #21 UNBLOCKED — garrison research landed + mod mechanics traced
research/RESEARCH_QING_XINJIANG_GARRISONS_1763.md written (memory pointer saved). Mechanics for the build:
- Existing garrisons seeded by imp19c_setup.12 as the BUILDING qing_banner_garrison_building (+ tuntian) on
  named subject-capital province IDs, guarded exists + owner=is_subject_of ROOT + not-present. NOT create_unit.
- XNG (Kashgaria/Altishahr), capital Kashgar p:2700, owns the Tarim belt (Aksu 2977 + 19 more). XNG is
  client_state of ILI → NESTED CHI→ILI→XNG. So the seed guard `owner = { is_subject_of = ROOT }` FAILS for XNG
  (non-recursive) — #21 MUST use `owner = { overlord = { is_subject_of = ROOT } }`. Urumqi p:2930 is ILI's, not
  XNG's (owner varies per province — verify each before seeding).
- Building potential gate: owner country_culture_group=jurchen + is_in_region Turkestan/etc. XNG is uighur-
  culture → the garrison building's jurchen-owner potential may REJECT it on XNG soil (like the amban gate #234
  had to widen). Must verify the building potential admits XNG, or widen it (#234 precedent).
- ANACHRONISM: Tarbagatai 1764 / Huiyuan finished 1766 / Sibe 1764 — do NOT seed as 1763-extant.
→ #21 is now a MAJOR task needing a short design doc (province-ID + owner-guard + potential-gate map, N-heavy/
  S-light sizes) before build. Deferred to next; not blindly seeding.

### [T12] #24 COMMITTED — 73a50b8b1 (reviewed, incl. the missed 2735 site)
Review found #24 INCOMPLETE — I'd missed diplomatic_view.gui:2735 (the Subjects-tab SELECTED-subject ruler
portrait = the exact Anhua/Sahaliyan Ula leak). Also confirmed: HLJ=stratocracy(republic-typed); the shared
block's stratocracy string-exclusion does NOT fire at runtime, so the flat blockoverride is the ROBUST fix
(not a fragile targeted exclusion). Patched 2735 + committed all 6 cpt_button sites. Pushed. DEFERRED (out of
scope, flagged): cpt_button_large (gui_base.gui:5907) renders the chip inline with NO block wrapper — no
override escape hatch if ever used for a Qing march ruler.

### [T13] #26 amban-picker DESIGN reviewed (SOUND-WITH-FIXES) → doc corrected
Key corrections folded in: (1) QING_amban_wire does NOT draw (the iterator is in QING_amban_post) — it's
ALREADY the pre-chosen-char entry point, so no wire adaptation needed; new trampoline qing_amban.6 presets
scope:qing_amban_new then calls the wire unchanged. R1 down-graded to LOW. (2) BIGGEST risk is R5 (narrow/empty
candidate pool + loss of the auto-path's create-a-resident fallback) → picker needs a "raise a new resident"
row, not gate-only. (3) R2 parallel window is routine (6 clones exist). (4) R3 up-graded: 2b-A subject sub-
picker is net-new GUI + unproven two-step chaining — treat as a spike; Phase 1 (Diplomacy button) doesn't need
it. (5) PI charge + qing_amban_manual must MOVE to the row handler (else charged on cancel). (6) Replace button
also auto-draws — decide if it becomes a picker too. Design-only; multi-phase GUI feature, not built tonight.

### [T10] #23 reframed by the #28 review — NOT an annual reset (likely equilibrium ceiling)
Updated understanding: the -10% is the deflation script_value's ceiling recomputed quarterly when
private_cash_ratio is pinned low, not a yearly event. The v2 currency log (#28) will confirm whether the
ratio is simply floored by a chronically tight money supply (→ #23 becomes a BALANCE question: is the
money-supply model too tight for CHI's scale?) vs an actual reset. Task #23 note to be updated after #28 lands.
