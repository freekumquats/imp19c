# Overnight Decisions 4 — running log

**Branch:** `merge-overnight` · **Start:** 2026-07-11 04:46 PDT · **Commits:** freekumquats

This is the decision log for the overnight bureaucracy build-out (`overnight_design4.md`).
Review this file when you're back. **Deferrals are called out at the very top.**

---

## ⚠️ DEFERRALS (read first)

> Goal is ZERO avoidable deferrals. Size/complexity is NOT a reason to defer — only a
> hard external blocker is (an unproven engine capability both oracles lack, or a
> dependency on an unbuilt feature). Anything deferred is listed here with its concrete
> blocker and what would unblock it.

- *(none yet — updated as the build proceeds)*

---

## Cross-cutting decisions

- **D0 (priority reorder, user):** #347 then #346 moved to the TOP of the queue ahead
  of Wave 1. Correct dependency order anyway — #347's army-detection idiom is the
  substrate #346 layers onto.
- **D0b (deps, user):** #349 (War panel) + #350 (Lifan Yuan panel) are PREREQUISITES
  of #346 — the frontier-garrison turf-war friction surfaces in BOTH panels, so they
  must exist first. Revised order: #347 → #349 → #350 → #346 → Wave 1 (#357/#356) →
  rest of Wave 2 → Wave 3.
- **D1 (office→bureaucracy completeness):** every one of the 13 appointive Grand
  Council offices gets a bureaucracy panel, so the Grand Council becomes a hub of 13
  sub-governments rather than a flat seat list. Map in overnight_design4.md §1.
- **D2 (shared panel pattern):** all office panels clone ONE structural template
  (qing_greatgame.gui pair), differing only in the managed roster + directives. Keeps
  13 panels consistent and cheap to review. §2.
- **D3 (the unifying mechanic — HARD REQUIREMENT, reaffirmed by user):** EVERY Grand
  Council bureaucracy is wired into its LEADER — the bureaucracy's performance
  DETERMINES that office-holder's performance on the Grand Council. Each panel drives a
  `qing_<office>_perf` 0..100 meter that folds into `qing_council_eff_target` (same fold
  as the officer-corps coupling, se_QING_COUNCIL.txt ~404-408). A well-run ministry
  raises its Minister's council standing/effectiveness; a poorly-run or vacant one drags
  it down. No panel ships without this fold wired + logged. Panels are functional, not
  cosmetic. This is checked in each task's adversarial review.
- **D6 (research landed):** English sources → RESEARCH_QING_OFFICES_EN.md; Chinese
  sources → RESEARCH_QING_INSTITUTIONS_CHINESE_SOURCES.md. Both are feasibility/flavour
  references only (no copyrighted text copied into game files). Key gap flagged by the
  ZH agent: **巴牙喇 Bayara** has minimal dedicated Chinese scholarship — for #364 lean
  on the banner-guard sources (Porter, *Slaves of the Emperor*; Crossley, *Orphan
  Warriors*; Chang, *A Court on Horseback*) + the 護軍營/侍衛處 literature and treat the
  Bayara as the elite 護軍 vanguard, which IS well-attested.
- **D4 (research):** English + Chinese academic-source agents dispatched for all
  offices; findings fold into per-feature flavour + this log. History agents dispatched
  ad hoc as features need grounding.
- **D5 (review cadence):** an adversarial-review Workflow runs after each task; only
  CONFIRMED findings are fixed before moving on. Verdicts summarised here per task.

---

## Per-task decisions

### Shared infrastructure — ministry-performance fold (the D3 spine)
- **D7 (canonical perf var):** each ministry panel sets ONE country var `qing_min_perf_<office>`
  (0..100, 50 = neutral/adequate), where `<office>` is the Grand Council office key
  (war/personnel/revenue/rites/justice/works/censor/lifanyuan/chamberlain/zongli/
  grand_secretariat/guard_commandant). The task-named `qing_war_ministry_perf` maps to
  `qing_min_perf_war`.
- **D8 (single fold, not 13 edits):** a new shared effect `QING_council_fold_ministry_perf`
  in se_QING_COUNCIL.txt is spliced ONCE into QING_council_recompute (right after the
  officer-corps fold, ~line 409). It averages `(qing_min_perf_<office> − 50)` across only
  those offices that BOTH have a perf var set AND a live filled holder, then adds
  `avg/5` (bounded ~±10) to `qing_council_eff_target`. Averaging keeps the term bounded no
  matter how many ministries report, so panels can be added incrementally without
  destabilising the effectiveness band. A well-run ministry raises the council target; a
  poorly-run one drags it. Behaviour when NO ministry has reported yet: the fold is a clean
  no-op (n=0 guard), so existing saves/behaviour are unchanged until a panel sets a perf var.
- **D9 (per-office contribution surfaced):** the fold also stores `qing_min_perf_council_mod`
  (the net ±term applied) so the Grand Council tooltip + each ministry panel can show "this
  ministry's contribution to the council". Concrete, not hidden.

### #347 Standing-army province effects (generic) — DONE (review: 1 blocker fixed)
- **REVIEW — 3 real findings fixed (2 blocker, 1 major):**
  1. (blocker) used `army_size` as a unit trigger — WRONG; proven key is `unit_size`
     (blemmia_missions:974; unit_abilities/*.txt; `army_size` is only ever a var NAME).
     Silently no-opped the whole pulse. Replaced all 5.
  2. (blocker) army→province deref via `location = { }` and country via `owner` — UNPROVEN
     from an army/unit scope. The PROVEN unit-scope links are `unit_location = { }`
     (naval_raiding.txt:29, a unit_ability = unit scope) and `unit_owner`. Fixed the
     scope-push (unit_location) + both friction-guard country reads (unit_owner). `commander`
     stays (army→char, read at army scope) and `<prov>.governor` stays (proven,
     egypt_mission_3:664).
  3. (major) modifier-refresh FLICKER — `NOT has_province_modifier` guard + duration=40 +
     ~30-day pulse meant the modifier expired at day 40 and wasn't re-added until day 60
     (a ~20-day unrest flicker every cycle), and two same-owner armies on one province
     conflicted. FIX: unconditional remove-then-add each pulse (proven refresh idiom) →
     exactly one instance, fresh timer, no flicker, no stack.
  - (minor, NOT fixed — accepted) friction cooldown is one-per-owner-per-200-days: at most
     one billeting dispute per realm per window even if several hosts quarrel. Deliberate
     anti-spam cap (D12), logged, not a defect.
  - Lesson: verify a scope-link/trigger key repo-wide against the REAL unit-scope refs
    (unit_abilities), not from a single mission-file grep hit that may be a different scope.
- **D10:** army detection uses the PROVEN `every_army` (country scope) + army-scope triggers
  (is_moving/army_size/in_combat/exists=commander, Invictus blemmia_missions:974) + the
  `<prov>.governor` scope-link (Invictus egypt_mission_3:664, guarded exists). Army strength
  carried into the province scope via `set_local_variable` (se_DIPLOMACY:105 pattern) — NOT a
  persistent var on the transient army object.
- **D11:** province modifiers (pacified / pacified_heavy / billeting_strain) are RE-STAMPED
  each monthly pulse with duration=40 (> the ~30-day cadence) + a has_province_modifier guard,
  so they refresh while the army stays and lapse on their own ~40 days after it leaves — no
  explicit teardown, no stacking.
- **D12:** governor-friction event throttled ONE per owner-country per 200 days
  (`army_gov_friction_cd`). Accepted limitation: at most one billeting dispute surfaces per
  realm per window even if several hosts quarrel — a deliberate anti-spam cap, logged here (NOT
  a deferral; the mechanic is complete, just rate-limited).
- **D13 (food):** confirmed engine-driven (unit food_consumption vs province capacity →
  attrition); documented in the on-action header, no new scripting. NOT a deferral — nothing to
  build.
- New files: common/on_action/army_effects_on_actions.txt, common/modifiers/
  army_effects_modifiers.txt, events/imp19c_mod_events/army_governor_friction.txt,
  localization/english/army_effects_l_english.yml. Adversarial review dispatched (wf run).

### #349 Ministry of War panel (兵部) — BUILT (pending review)
- **D14 (panel template locked):** #349 is the REFERENCE panel every other ministry panel
  clones. Structure = gui/qing_greatgame.gui's PROVEN working layout (fixed-size header +
  body siblings in a vertical flowcontainer, console createwidget open + GUI.ClearWidgets
  close), NOT the #352-F9 nested-expanding layout — greatgame is verified working in-game
  with fixed sizes, so that is the safer clone base. Roster list uses the PROVEN
  dynamicgridbox + `datamodel = [Player.MakeScope.GetList('<list>')]` idiom
  (imp19c_windows.gui:71) — never a vbox (#352 F2).
- **D15 (perf backbone):** new se_QING_MINISTRY.txt holds the dispatcher
  QING_ministry_recompute_all_perf (called at TOP of QING_GOV_pulse, before the council
  recompute) + per-office perf computes. War perf (qing_min_perf_war) = minister's martial
  (dev-from-7 ×3) + officer-corps average martial (dev-from-7 ×2); vacant office floors to 25.
  It also rebuilds qing_war_officer_roster (deduped character list) for the panel datamodel.
- **D16 (attribute icons):** use the PROVEN `icon_military` template (government_view.gui
  throughout) for martial, NOT a shared_icons/martial.dds (that file does NOT exist; only
  civic/oratory/religious.dds ship in shared_icons — a #352-F13-adjacent trap avoided).
- New files: common/scripted_effects/se_QING_MINISTRY.txt,
  common/scripted_guis/QING_war_ministry_panel.txt, gui/qing_war_ministry.gui,
  localization/english/qing_war_ministry_l_english.yml. Edited: se_QING_COUNCIL.txt (fold
  helper + splice), se_QING_GOVERNANCE.txt (dispatcher call), government_view.gui (open button).
- **REVIEW — findings addressed:**
  1. (major, PRE-EMPTED before review even returned) double-count: qing_min_perf_war
     originally re-scored officer-corps AVERAGE MARTIAL, which se_QING_COUNCIL already folds
     (~404-408). Changed to officer-corps COVERAGE (count vs establishment) — orthogonal,
     not double-counted.
  2. (minor) stale-by-one-pulse: read the council's qing_officer_corps_count (recomputed
     LATER same pulse). FIX: tally qing_war_roster_count as we build the roster this pulse +
     read that fresh value.
  3. (minor) perf vars unseeded at game-init → panels blank until first pulse. FIX: call
     QING_ministry_recompute_all_perf at CHI on_game_initialized before autofill.
  4. (minor) panel label "Contribution to the Grand Council" was ambiguous (it's the
     realm-wide aggregate, not this ministry's own). FIX: relabelled "Ministries' net effect
     on the Grand Council" + tooltip clarifies it's the combined figure.

### #350 Lifan Yuan Directorate panel (理藩院) — BUILT
- **D17:** clones the #349 reference panel. Perf qing_min_perf_lifanyuan = Director's charisma
  (dev-from-7 x4) + AMBAN COVERAGE (fraction of autonomous-governorship subjects that warrant
  a resident which actually have a live qing_amban_here, scaled 0..-25). Vacant office → 25.
  Rebuilds qing_lifanyuan_amban_subjects (subject-country list) for the panel datamodel;
  coverage counts qing_lifan_amban_count / qing_lifan_warrant_count shown in-panel. Folds into
  the Lifan Yuan Director's council standing via the shared fold. Per-subject amban management
  stays on the diplomatic Subject tab (SUB_QING_amban); this panel is the central read-across.
  New files: QING_lifanyuan_panel.txt, gui/qing_lifanyuan.gui, qing_lifanyuan_l_english.yml;
  edited se_QING_MINISTRY.txt (+ perf + dispatcher call) + government_view.gui (button).
