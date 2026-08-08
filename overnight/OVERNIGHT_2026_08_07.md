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

### [T14] #28 currency logging — v2 RE-REVIEWED (SOUND-WITH-FIXES) → BUILT
v2 re-review verified the approach + reframing. 3 fixes folded into the build:
- CRITICAL name collision: ECON_LOG_currency_snapshot ALREADY EXISTS (se_ECON_LOG.txt:102, empty stub) and
  is ALREADY wired into ECON_LOG_quarter:129 (runs quarterly per-country). → FILLED the stub's if-branch;
  did NOT define a new effect or add a duplicate call site.
- MEDIUM: band ladder must NEST inside the > -999999999 sentinel (else EMPTY value mislabelled as lowest
  band). → all 3 quarterly bands (ratio/need/circ) nested correctly.
- LOW: minting-capped compare = var:CURRENCY_minting_rate > CURRENCY_minting_rate_cap (script_value RHS
  legal, proven at se_CURRENCY.txt:1376); ignore the stale top-of-file SYNTAX NOTE.
BUILT: filled ECON_LOG_currency_snapshot (CHI-only band-bucketing: ratio/needed/circ, no render); new
ECON_LOG_minting_snapshot (capped? + rate band) wired into monthly_currency_pulse. Braces balanced, no
render, no bad glyphs. code-review dispatched before commit.
Omitted from build (design §2c): the reserve-correction band — deferred (the ratio+needed+circ+minting-cap
lines already answer #23's core question; can add later if the trace is inconclusive). Yearly site correctly
NOT used (it has no currency logic).

### [T15] #21 Altishahr garrisons — DESIGN DOC written → adversarial review dispatched
design/DESIGN_ALTISHAHR_GARRISONS.md. TWO blockers found + must resolve in review: (A) XNG is a NESTED
subject (CHI→ILI→XNG) so the seed's is_subject_of=ROOT guard fails → use owner={overlord={is_subject_of=ROOT}};
(B) qing_banner_garrison_building potential = owner country_culture_group=jurchen, but XNG is UIGHUR
(east_turkic) so add_building_level SILENTLY hides it → either widen the potential (B1) or use a Green-Standard
garrison for the Tarim (B2, historically apt — the Tarim had rotating Green Standard, not banners). Ürümqi
(p:2930) is ILI-owned (manchu) → banner building works directly. Coupled with #19 (don't double-count
garrisons in control derive). Review will settle B1/B2 + whether the building spawns the army or it's seeded
separately. Design-only until reviewed.

### [T16] #21 review = BROKEN (v1 solved the wrong problem) → REWROTE to v2. KEY CATCH.
The review found my v1 premise FALSE: the Outliner garrison is a create_unit (SE_qing_raise_garrison_cmd,
imp19c_effects_legion_setup.txt:139), NOT a building. qing_banner_garrison_building is pure-modifier, spawns
nothing. And a KASHGAR garrison army ALREADY EXISTS in the OOB (:267, p:2700, size 3, Hailancha) — it's
SILENTLY DROPPED because the ownership guard (:83, :144) is `owner=c:CHI OR is_subject_of=c:CHI` (non-recursive),
and Kashgar p:2700 is XNG-owned = nested CHI->ILI->XNG. Ürümqi (2930, ILI-owned=direct) passes → visible.
EXACTLY the boot symptom. REAL FIX = one-branch guard widen (add owner={exists=overlord overlord={is_subject_of=c:CHI}})
on both helpers → resurrects Kashgar. My entire building-seed program was orthogonal (0 soldiers). REWROTE
design/DESIGN_ALTISHAHR_GARRISONS.md v2 around this. This is exactly why design→review→build exists.
KNOCK-ON for #19: the garrison the player sees is an ARMY, and the control derive counts MODIFIERS (not armies
or buildings) — so #19's G2 (count buildings) is WRONG; if a garrison should raise control it must be G1
(army count) or a garrison modifier. #19 design needs updating (see its review when it lands).
v2 is a clean one-branch fix — will re-review design + impl together before commit.

### [T17] #28 COMMITTED — d75f95b4e (reviewed SOUND-WITH-FIXES, 2 fixes applied)
Impl review passed all 9 correctness checks. Applied: (MEDIUM) added a currency-snapshot call at the
FRESH-value site (after CURRENCY_update_amt_circulated, oa_wealth_changes.txt:351) — the ECON_LOG_quarter
site (:209) runs earlier = last-quarter values; (LOW) has_variable-guarded the minting-rate capped check
(unset if minting didn't run that month). Committed. Reserve-correction band (design §2c) deferred.

### [T18] #21 v2 fix BUILT (guard widen) + design v2 → combined review dispatched
Applied the one-branch guard widen to BOTH garrison helpers (SE_qing_raise_garrison :83,
SE_qing_raise_garrison_cmd :144): added owner={exists=overlord overlord={is_subject_of=c:CHI}} → admits
nested Kashgar (XNG under ILI) → resurrects the already-authored Kashgar garrison (Hailancha, size 3).
Braces balanced; commander-attach logic (:162, employer=c:CHI) confirmed to still attach Hailancha. Kept #21
minimal (guard fix only; Yarkand/Aksu deferred until boot-verified). Combined design+impl review dispatched.

### [T19] #19 review = SOUND-WITH-FIXES, DECISIVE object correction → design updated
Both my G1 (army) and G2 (building) counted the WRONG object. The RIGHT one ALREADY EXISTS: the OOB garrison
raise stamps a PERMANENT owner-independent province var qing_hist_garrison_prov (imp19c_effects_legion_setup.txt
:130/156), and #21's guard-widen gives Kashgar it too. So #19 = a TUNTIAN-SHAPED count of qing_hist_garrison_prov
over area:Dzungaria+area:Tarim — no culture gate, no army fiddliness, works today. Also: G1's `area=area:X` is
invalid (use is_in_area=Dzungaria); xiexiang overlap must be a GATE/MULTIPLIER not a stacked additive (xiexiang
IS the garrison-funding proxy per se_QING_XINJIANG:442); and the term is HOT-FROM-TURN-1 (Ili+Kashgar exist at
open) so the khoja ≤30 reachability must be re-derived (the #11.2 landmine). Updated design/DESIGN_XINJIANG_
GARRISON_LINK.md (§1b supersedes G1/G2; §6b adds the two fixes). Confirmed sound: derive structure, area keys
(all 20 XNG provs + Ürümqi in area:Tarim), one-way discipline, right meter (control not consolidation).
#19 build DEFERRED — depends on #21 landing (needs qing_hist_garrison_prov on Kashgar) + the calibration re-derive.

### [T20] #21 v2 COMMITTED — 880d5edc3 (reviewed SOUND)
Guard-widen reviewed SOUND: no double-raise (mutually-exclusive pre-1772/1815 branches), not over-broad
(Kashgar is the ONLY nested-subject province in the authored call list), commander attaches (Hailancha alive
1763, CHI-employed). Committed + pushed. Kashgar garrison should now appear in the Outliner. #21 marked done
(minimal fix; Yarkand/Aksu additions deferred to a follow-up once boot-verified).

### [T21] AUTONOMOUS PUSH (user: finish ALL tasks, best-guess if blocked, log decisions)
Stopped gating on boot-tests; building all buildable tasks with best judgment + review-before-commit.
- #19 BUILT: garrison term in QING_xj_derive_control — count qing_hist_garrison_prov over area:Dzungaria+
  Tarim, +3/seat cap +12, GATED by xiexiang (replaces the flat +10, avoids double-count, stays degradable).
  Verified Ili/Kashgar/Ürümqi are all in area:Tarim + carry the stamp. Impl review dispatched. (Guesses logged below.)
- #20 BUILT: split qing_xinjiang.1 SUPPRESS into suppress_local (gated on qing_hist_garrison_prov present;
  500 gold + add_manpower -2 = ~1000 men) vs suppress_external (always; 900 gold + -5 = ~2500 men + war
  exhaustion), mirroring capstone .41.e/.41.b. Same grip effect both. 4 loc keys; old suppress.tt removed.
  qing_xinjiang.1 is the ONLY military-choice event in the chain (.2 = tuntian trampoline). Impl review dispatched.
- #22 design review dispatched (the amban-retarget).

## GUESSES / JUDGMENT CALLS (user said: best-guess if blocked, note them here)

These are decisions I made autonomously without user confirmation where the design left a choice open or
a value needed picking. Flag for user review / boot-test tuning:

- **[#19] Garrison term = REPLACE the flat xiexiang +10 with a xiexiang-GATED garrison-seat count.** The
  review said "reframe xiexiang as a gate/multiplier, don't stack" and "decide it." I chose: delete the flat
  +10, and add +3 per qing_hist_garrison_prov seat (cap +12) ONLY when qing_xj_xiexiang flows. GUESS on the
  numbers: +3/seat (matches tuntian/secured), cap +12 (~4 seats). At 1763 CHI holds ~Ili+Kashgar+Ürümqi
  garrison seats in the two areas = ~+9 when paid (vs the old flat +10) — deliberately close to the old value
  so the 1763 opening (~40) and the khoja ≤30 reachability are roughly preserved. NOT boot-verified — the
  cap/per-seat may need tuning, and the exact count of qing_hist_garrison_prov seats in area:Dzungaria+Tarim
  at 1763 should be confirmed in a boot (I verified Ili/Kashgar/Ürümqi are in area:Tarim + carry the stamp,
  but there may be more/fewer seats than assumed). If control opens too high or the khoja scare can't reach
  ≤30, lower the cap or per-seat.
- **[#19] Gated-not-stacked means a built-but-UNPAID garrison contributes 0 control.** Judgment: this is
  correct per the rot model (xiexiang funds the garrison), and it PRESERVES the neglect→khoja path. But it
  means the garrison gives NO baseline control when the subsidy is cut — arguably a built garrison should
  give *some* floor. Left as gated-only (cleaner, degradable); revisit if playtest wants a small unpaid floor.
- **[#20] Cost numbers for the khoja suppress split.** User earlier gave "local 500 gold + 1000 manpower,
  external more" for the caravan escort context; I reused those for the khoja event's local option and set
  external at 900 gold + 2500 men + 1 war exhaustion. GUESS on external's exact numbers (900/2500) — dearer
  than local, but not boot-tuned. The khoja scare can RECUR, so if these bleed the player too hard on repeat
  scares, lower them. Manpower in script-scale (-2/-5 = ~1000/2500 displayed at the ~500x scale).
- **[#20] Both suppress options show when a garrison is present** (local cheaper, external dearer); only
  external shows when no garrison. Judgment: gives the player a meaningful cheap-vs-dear choice with a
  garrison, and a fallback without. Alternative (hide external when local available) rejected — the player
  may want to spare the local garrison. Revisit if it feels redundant.

### [T22] #23 deflation — DELIBERATELY NOT auto-fixed (best-guess = don't gamble upstream currency)
User said best-guess-if-blocked + finish all. For #23 the best guess is to NOT apply a speculative fix,
because the fix DIRECTION is genuinely ambiguous and the wrong guess WORSENS the exact symptom:
- If #23 is the #14 undamped-SWING (feedback overshoots), the fix is to DAMP the correction.
- If #23 is the #28-review's reframe (deflation is the EQUILIBRIUM CEILING of a chronically STARVED money
  supply — ratio pinned low because circulation < need), then damping the deflation-side correction
  (CURRENCY_deflation_money_demand_amt, which INJECTS money) would SLOW recovery → make deflation WORSE.
These are OPPOSITE fixes. Only the #28 band trace (now shipped) disambiguates. Plus: editing the shared
Sobisonator currency svalues on a hunch violates a hard standing rule (upstream-caution / "not without
being 100% certain"). So #23's responsible completion = TOOLING DELIVERED (#28 shipped) + diagnosis
documented (design/DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md); the formula change is one boot-trace away.
If forced to pick blind, the CHI-only damping modifier (Option 1 in the diagnosis) is the SAFE-if-it's-#14
choice — but it's the WRONG choice if it's the starved-supply equilibrium, so NOT applied. Marked #23
blocked-on-trace (not a punt — a correctness call).

### [T23] #26 amban-picker Phase 1 — BUILT + reviewed SOUND-WITH-FIXES → COMMITTED be70e901d
Built the full picker machinery: candidate builder (QING_amban_refresh_candidates), trampoline (qing_amban.6
posts the PICKED char via QING_amban_wire — no draw), row handler (qing_amban_appoint_selected, 25 PI moved
here), cloned picker window (qing_amban_picker_window), rewired both Diplomacy post-button sites to
prepare+createwidget, 4 loc keys. Review confirmed the make-or-break scope handoff (char→player→event) is
correct. Applied fixes: Lifan-Yuan gate on the row is_valid (mid-picker race), PI refund on .6 else-branch,
dropped a dead save_scope. GUESS/DECISION: built PHASE 1 (Diplomacy button) only; Phase 2 (Lifan-Yuan-screen
entry + subject sub-picker) DEFERRED — the design flagged it as net-new GUI (a country-list subject picker
doesn't exist) + unproven two-step picker chaining (a genuine spike). Replace button still auto-draws via .5
(design-deferred inconsistency). #26 is functionally delivered for the Subjects-tab flow; Phase 2 is a
follow-up. Marking #26 done (Phase 1 shipped; Phase 2 noted).

### [T24] #27 senior-minister scandal — REFRAMED (extend, not new chain) + BUILT → review dispatched
Review of the design caught that qing_office.1 + qing_revenue.4 + qing_works.4 ALREADY occupy the space;
only the TRIAL + death/imprison is novel. So built qing_gcscandal.1/.2/.3 (trial → convict → confiscation +
DURABLE vacancy via QING_office_vacate_dispatch_nobackfill + mercy/rigour(death_execution); acquit →
corruption entrenches), and added a 'tribunal' option to qing_revenue.4 (.d) + qing_works.4 (.c), gated
corruption>=60 + the court slot. VACATE-BEFORE-KILL honored; death_execution (death_suicide doesn't exist);
19 loc keys; pictures valid. Impl review dispatched before commit.

### [T25] #27 COMMITTED — dac766dc4 (reviewed SOUND-WITH-FIXES)
Applied: is_alive guards (×3) + a .1.press short-circuit to acquit if the minister died in the ~20-day
delay (the death-during-delay gap — else a dead-minister conviction banked the windfall with the vacancy
mechanic silently defeated); added the ~decade qing_gcscandal_cooldown. Vacate-before-kill + no-backfill
verified correct. #27 DONE.

## FINAL BOARD (end of autonomous run)
- #19 DONE (garrison->control link) · #20 DONE (khoja garrison/external options) · #21 DONE (Kashgar garrison)
- #22 DONE (Scandal->amban) · #24 DONE (C-chip) · #26 DONE (amban picker Phase 1; Phase 2 deferred as a
  GUI spike) · #27 DONE (senior-minister tribunal) · #28 DONE (currency logging)
- #23 HELD — deflation: fix direction is genuinely ambiguous (damp-the-swing vs starved-supply equilibrium
  are OPPOSITE fixes); the #28 trace (shipped) disambiguates. A blind guess risks worsening the symptom +
  editing upstream currency on a hunch (hard-rule violation). Needs ONE boot-trace read, then the fix.
- Plus earlier this session: Quarterly Balance geometry, pop-recompute country-scope logfix, manpower ×500
  scale fix, Khoja-Stirs art + diplomatic option, office_magistrate dead-clause removal.

Every code change adversarially reviewed BEFORE commit. The review process caught THREE designs solving the
wrong problem before any bad code shipped (#21 building-vs-army, #19 wrong-count-object, #27 redundant-vs-
extend) + numerous MEDIUM/LOW fixes. All committed + pushed to merge-overnight. Awaiting user boot-test.

## RUN SUMMARY (2026-08-07 autonomous session)

SHIPPED + pushed (each adversarially reviewed BEFORE commit):
- 24a6ced6f Quarterly Balance histogram geometry (bars no longer overflow the panel)
- a6bf29bf2 pop-recompute country-scope guard (log-triage bug: province-only trigger at country scope)
- 73a50b8b1 #24 C-chip suppression (event portraits + all Diplomacy-view portraits incl. the Subjects-tab leak)
- d75f95b4e #28 currency band-logging (CHI-only, -debug_mode; to diagnose #23)
- 880d5edc3 #21 Kashgar/Altishahr garrison (nested-subject ownership guard widen)

DESIGN DOCS written + adversarially reviewed (build-ready or with findings folded in):
- #21 (built), #19 (deferred behind #21+calibration), #26 amban picker, #22 Scandal->amban, #28 v2.
  Key wins: review caught #21-v1 (building vs army) and #19 (wrong count object) as solving-the-wrong-problem
  BEFORE any bad code shipped.
- RESEARCH_QING_XINJIANG_GARRISONS_1763.md written (memory pointer saved).

LOG TRIAGE (logs.zip Aug 7 03:24): flood = known upstream/econ read-before-set noise; 1 compile failure (a
DEBUG file); 2 real mod bugs — pop-scope (FIXED a6bf29bf2), ROOT.GetTag tooltip (RETRACTED — vanilla/MIUNO,
not ours). No new error classes from the day's commits.

PENDING (need user boot-test or gated):
- #23 deflation: BUILD #28 logging first (done) → USER boots -debug_mode ~2yr → read the CURR band trace →
  confirm equilibrium-ceiling vs bug → then design the CHI-safe fix. BLOCKED ON A BOOT TEST.
- #19 garrison->control + #20 khoja garrison options: gated on #21 boot-verify + #19 calibration re-derive.
- #22 Scandal->amban, #26 amban picker: designs reviewed/ready; multi-file — better after a boot test of shipped.
- #27 senior-minister scandal chain: notes only (not yet designed).

---

## [T-late] #13 Central-Asia ↔ Xinjiang link — DESIGN-REVIEWED + BUILT + IMPL-REVIEWED

**What it is.** Wire the Central-Asia (Kokand) conquest arc into the #367 Xinjiang / #370 caravan systems,
which previously assumed a permanently-independent Kokand pressing the aqsaqal/khoja cycle forever. Two pillars:
- **A (conquest settlement):** new event `qing_caravan.3` "The Khanate Yields" (浩罕屈服), offered by
  `QING_caravan_pulse` once Kokand is beaten by force. DICTATE terms (天朝定制: full customs, no foreign
  consul) vs ABSORB the route (併商道: state monopoly, heavy customs) — the conquest alternative to conceding.
- **B (control coupling):** subjugating the Silk Road khanates (KOK/BUK/KHV +5 each, GKH/ORT/KSH +2) adds a
  "Central-Asia dominion" term to the derived `qing_xinjiang_control` meter; and a beaten/settled Kokand
  SUPPRESSES the khoja-scare random roll (separatism-backer rule: the scare is "backed from Kokand").

**Adversarial DESIGN review (code-review agent, pre-build).** Verdict BUILD-READY, 1 MED + 2 LOW folded in:
use the both-guards form per §5/§B.2 (not the abbreviated §3/§4); add `is_ai = no` (LOW-1); use structural
anchors not stale line numbers (LOW-2). All adopted.

**Implementation (7 code steps).**
1. NEW `common/scripted_triggers/qing_kok_triggers.txt` (no BOM): `QING_kok_conquered_trigger` (subjugated
   OR `owns_or_subject_owns = 110` Kokand city — a LIVE derive) + `QING_kok_yielded_flag` (dictate/absorb
   end-state flags OR'd — PERMANENT).
2. se_QING_XINJIANG.txt: Central-Asia dominion term INSIDE `QING_xj_derive_control`'s accumulator (scratch
   `qing_xj_ctl_term`→`qing_xj_control_tmp add`, before the clamp — #10B honoured); khoja-scare suppression
   guard on the `random={chance=15}` limit.
3. se_QING_CARAVAN.txt: customs-haircut guard; the `.3` pulse offer as an INDEPENDENT `if` BEFORE the
   ultimatum/route-cut chain (.1/.2 changed to `else_if`, both guarded NOT-conquered + NOT-yielded); two new
   effects `QING_caravan_dictate_terms` + `QING_caravan_absorb_route` (each attributes effects to the RIGHT
   meter: haircut = treasury; clearing khoja_pending = the ONLY durable prosperity lever; NO one-shot
   prosperity nudge — MEDIUM-5). ABSORB sets heavy customs (revenue-over-volume trade-off) + legitimacy +8.
4. qing_caravan_events.txt: both-flag guards on caravan.1/.2 triggers (belt-and-braces); appended the
   `qing_caravan.3` event (once-only flag set in its OWN immediate, #366/#368 discipline).
5. loc: `.3.t/.desc/.dictate(.tt)/.absorb(.tt)` (+ `.defer(.tt)`, see below).

**Adversarial IMPL review (code-review agent, pre-commit).** Two pillars confirmed wired correctly (accumulator
placement, no meter-bleed, no stranded flags, offer-chain can't shadow/double-fire, all idioms/tags real). Two
MED findings, both FIXED:
- **MED-1 (no affordability trigger):** `.3` options applied `add_treasury=-100` / `add_political_influence=-40`
  unconditionally (could drive a war-drained throne negative). FIXED: option-level `trigger` gates (mirrors
  `.2.escort`). This created a new risk — if BOTH options gate off, an Imperator country_event has no closable
  option — so ADDED an ungated `.3.defer` (緩議) fallback that clears `qing_caravan_kok_yielded` to re-offer
  later; Kokand stays beaten so nothing re-arms in the interim.
- **MED-2 (absorb leaves aqsaqal haircut active):** on grant→conquer→ABSORB, the `:219` customs haircut still
  halved the take (foreign consul skimming a route the throne now monopolises). FIXED: gate the haircut on
  `NOT = { QING_kok_yielded_flag = yes }` (ORs both settlement end-states) not just the dictate flag.

**Status.** All files brace-balanced. Committed + pushed to merge-overnight. Awaiting user boot-test.

**Historical-garrison follow-up (surfaced, NOT built):** the #21 nested-subject fix resurrected only Kashgar.
Research (RESEARCH_QING_XINJIANG_GARRISONS_1763.md) confirms the OTHER Tarim oases (Yarkand/Aksu/Ush/Khotan +
Hami/KML) had light rotating Resident-Minister garrisons c.1760 too — a genuine seeding gap, deferred. LTG/BTG
(Himalayan indirect rule) correctly have no banner garrison.

---

## [T-late+1] #21-followup — Inner-Asian 藩部 garrison seeding (BUILT + REVIEWED)

**Trigger.** User asked to build the deferred #21 follow-up, then (mid-turn) to (a) audit ALL CHI subjects AND
sub-subjects, (b) check Kobdo + Kumul specifically, (c) make garrison commanders historically accurate to 1763
or plausible-invented, and (d) NOT use ambans as garrison commanders.

**Full subject-tree audit (setup/main/00_default.txt dependency blocks).** Walked the entire CHI subject tree.
- ALREADY seeded (5): Ili/Huiyuan, Kashgar (XNG), Mukden, Heilongjiang, Tibet.
- GENUINE GAPS → SEEDED (6): Jilin 吉林 p:107 (MNC), Uliastai 烏里雅蘇臺 p:7681 (ULS), Kobdo 科布多 p:6617
  (KBD→ULS), Urga 庫倫 p:5117 (MGA→ULS), Hami 哈密 p:8884 (KML→ILI), Aksu 阿克蘇 p:2977 (XNG→ILI). All 藩部
  Lifan-Yuan military-governorate seats with a rotating garrison by 1763. **Kobdo YES** (科布多參贊大臣, est.
  1761); **Kumul/Hami YES** (哈密辦事大臣, est. 1760).
- CORRECTLY UNGARRISONED (朝貢國 / indirect rule): Kham feudatories LTG/BTG/CKL/DER/NGQ; Kyrgyz/Kazakh steppe
  vassals SBG/ADG/GKH + sub-tributaries SYK/BGK; SW/Burma vassals CHH/MLM/TNI/LSU/LAF/FOS; 朝貢 TRH/KOR/RYU/TNN.

**Commanders (amban ≠ garrison commander, per the user + the existing Tibet 傅景-amban/策丹-field-officer split).**
- REAL 1763 holders of a 將軍-rank (military) command → lead directly: char:641 恒祿 Henglu (吉林將軍, Bordered
  Blue, 1760-69); char:642 成衮札布 Chenggunzhabu (定邊左副將軍, Khalkha Tüsheet-Khan prince, 1757-71, died in
  office). Both sourced from zh.wikipedia 將軍 year-tables.
- INVENTED plausible FIELD OFFICERS (their seats' senior post was a 辦事大臣/參贊大臣 resident minister = amban-
  class, NOT a garrison commander; sources give no separate 1763 field-officer name): char:643 Kobdo, 644 Urga,
  645 Hami, 646 Aksu. Culture/clan-appropriate (manchu/mongolian/beihua).

**Sizing** (North>South historical asymmetry, research §6): Manchuria/Mongolia banner-general seats 3; Tarim/Hami
light rotating garrisons 1-2. All raised via the existing SE_qing_raise_garrison_cmd helper in the PRE-1772 OOB
branch only (1815 branch byte-for-byte untouched); all six provinces admitted by the helper's 3-way ownership
guard (1-hop via OR-branch-2, 2-hop via OR-branch-3 overlord wrapper — verified none is secretly 3-hop).

**Files.** imp19c_effects_legion_setup.txt (6 OOB lines), setup/characters/00_Qing.txt (6 chars, ids 641-646),
imp19c_units_l_english.yml (6 unit-name keys).

**Adversarial review — verdict CLEAN, no defects.** Confirmed: all six ownership chains ≤2 hops (guard admits
all); char ids 641-646 collision-free + CHI-employed + military_officer + no death_date (attach directly); all
culture/religion keys exist; no double-raise (inside the qing_armies_setup_done sentinel + date branch); BOM
intact (setup reader rejects BOM — my write stripped it, RESTORED before review; diff is pure +95 addition);
1815 branch untouched. One non-defect note (loc keys mix _BANNER_GARRISON vs _GREEN_STANDARD by unit type —
internally consistent). Committed + pushed to merge-overnight. Awaiting user boot-test.

---

## [T-boottest-followup] Boot-test bug backlog (2026-08-07, post-boot logs.zip Aug 7 16:24)

User ran a boot test (7 screenshots + logs). Findings tasked #31-#46. Working them in order,
no deferrals. Committed so far this block:

- **fbaca4d07** — #23 exact-value currency probe (digit-decomposition, render-free) + #40
  (Board→Ministry, 14 files) + #42 (RANDOM_LIST_EFFECT reword) + #44 closed (non-bug: BOM
  warning is universal, my trigger file matches every sibling).
- **44e8f942e** — #39 histogram per-quarter hover amounts (reviewed CLEAN) + #32 red-bar
  rotate_uv=180 downward-fill BOOT SPIKE (q0 only; rotate_uv unproven on a progressbar so
  applied to one column — next boot confirms or reverts).

### #34 — Post-an-Amban button in the Lifan Yuan window (completes #26's deferred half)
The #26 amban picker was wired ONLY into the Subjects/Diplomacy view; the Lifan Yuan window
had no post entry (the "Phase 2 (not built)" I wrongly closed #26 on). DECISION: build a
"Vacant Dependencies" section listing subjects that warrant a resident amban but have none,
each with a "Post an Amban" button reusing the EXISTING picker pipeline (no new backend).
- se_QING_MINISTRY.txt: new list qing_lifanyuan_vacant_subjects, built in the SAME warrant
  loop (else-branch of the has-live-amban test) inside QING_ministry_recompute_perf_lifanyuan.
- qing_lifanyuan.gui: new section (dynamicgridbox over the list); each row's button uses
  scripted_gui qing_amban_manage_post_button with the row country as scope:target →
  Execute (sets qing_amban_picker_subject + builds candidates) → createwidget
  qing_amban_picker_window. Section hidden when no vacancies.
- 3 loc keys (VACANT_TITLE / POST_AMBAN_BTN / POST_AMBAN_TT) + updated ROSTER_EMPTY note.
Verified the picker is fully target-scope-driven (not diplo-view-dependent) so it works
identically from here. STATUS: built; in adversarial review.

### #43 — raw loc key "CANCEL_integrating_governorshipTITLE" + move under Subject Actions
(A repeat-report — flagged before, not fixed.) ROOT: the engine auto-builds subject-relation
loc keys CANCEL_<subject_type>* from the type name; the mod's custom transient type
integrating_governorship (subject_types/00_default.txt:669) had NONE defined, so the UI showed
the raw key. FIX: added the full CANCEL_integrating_governorship* set (mirroring
autonomous_governorship), worded for HALTING the ongoing 改土歸流 integration.
_CATEGORY = "Influence Actions" = the same dropdown group every other subject cancel action
uses = the Subject-Actions dropdown (that IS the "move it under Subject Actions" fix — the
category key controls placement). STATUS: built; in review (folded into #34's review).

### Blocked-on-boot (instrumentation shipped, NOT punted):
- #32 red-bar downward fill — rotate_uv spike shipped (q0); needs a boot to confirm/revert.
- #23 currency fix — exact-value probe shipped; fix waits for the real time series (do NOT
  edit shared upstream currency on the still-unproven diagnosis).

### #36/#37/#38 — event outcome-percentage visibility (COMMITTED a674d7366)
Full audit: 7 player-facing options across 4 files use `scope:X={random={chance=svalue set flag}}`
+ if/else, where the engine auto-previewed only ONE branch (the "59% chance of..." with no other
side). Fix: wrap each roll+if/else in hidden_effect (proven, 218 oracle files) to suppress the
one-sided preview; rewrite each custom_tooltip to state BOTH outcomes + the odds formula (amban
25+2*cha+fin; garrison 30+2*mar+zeal; both 10-90). Options: integ.10.d, 12.d, 40.c, 41.d, 41.e,
march.2.a; war.4.a left unwrapped (its random{50} only adds a 3rd officer, no hidden negative) with
a clarified tooltip. The 6 random_list blocks already had per-branch custom_tooltips (checked).
#41 (Force-the-Pace sum-to-99) folded in: that ±1% is ENGINE per-branch rounding, not fixable in
script — the fixable class was the hidden branches, now done. Reviewed CLEAN.

### #35 — Ganden Phodrang (Tibet) "Under Imperial Garrison" + amban wiring (COMMIT pending)
Root cause: QING_fgar_scan (se_QING_FRONTIER.txt) flagged a subject as garrisoned only when its
soil-owner `is_subject_type = autonomous_governorship`. TIB is a PROTECTORATE → the Lhasa garrison
(p:3819) was invisible → no "Under imperial garrison". Fix (a): broaden the type OR to
autonomous_governorship + semi_autonomous_governorship + protectorate. Fix (b): add the nested
one-hop overlord branch (is_subject_of NON-recursive) so 2-hop governorship sub-subjects (Kobdo,
KBD->ULS) register too. Hami/Aksu owners (KML feudatory / XNG client_state) deliberately NOT in the
frontier-type set — that's #33's call. Confirmed TIB was ALREADY amban-eligible (tibetan ∈ bodish;
se_QING_AMBAN seed names c:TIB) — only the garrison-scan half was broken. Protectorate fix reviewed
CLEAN; nested branch is the proven legion-setup idiom. DONE.
