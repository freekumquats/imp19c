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

## ⚠️ REGRESSION FOUND + FIXED (read second)

- **REG1 (#356 clobbered the Edicts button strip — FIXED in the #351 commit):** The committed
  #356 (d837be39f) edit to gui/government_view.gui REPLACED the entire two-column Edicts button
  strip with just the new marriage-proposal button — silently DROPPING the emperor
  seclusion/resume-rule buttons, the four succession-law reform buttons + active-law indicator
  (#312), the Great Game panel button (#108), the Reports hub button (#314 B26), and the War
  (#349) / Lifan Yuan (#350) / Zongli Yamen (#354) ministry-panel open buttons. Those features
  were all live but had NO WAY TO OPEN in-game after #356. RESTORED the full strip verbatim from
  the be7e33888 baseline (col1 = seclusion/resume/succession, col2 = Great Game/Reports/War/
  Lifan/Zongli), re-inserted the marriage-proposal button in col2, and ADDED the new #351 Works
  button alongside. Brace balance verified 1868/1868 (baseline 1864 + one new button = +4). This
  is why a post-task GUI-diff sanity check matters — the marriage-play review (still running) did
  not have government_view.gui's pre-image to compare against; caught here by grep during #351.

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

### #356 Marriage-proposal diplomatic play (replaces Dynastic Match) — BUILT (pending review)
- **D25 (new play goal):** a NEW `play_goal = flag:marriage_proposal` (flag literals are ad-hoc,
  no declaration needed) with a new branch in DIPLOMACY_trigger_diplomatic_play_finale_event →
  MARRIAGE_PLAY_resolve. The two chosen chars are stored on the play provobj as
  marriage_play_groom/_bride; play_target_area = the proposer's capital (a play needs an area;
  the marriage has no land locus and the finale branch does NO land transfer, so it is never ceded).
- **D26 (reuse, not reinvent):** resolution REUSES the existing marriage machinery — marry_character
  + MARRIAGE_apply_marriage_bond if both adult (decisive → full state bond; partial → private
  match), or a betrothal via the existing betrothed_to_char / betrothed_children / marriage_betrothed
  bookkeeping (matured/dissolved by the existing MARRIAGE_check_betrothals pulse) if either is a minor.
- **D27 (success seeding + player levers):** opening success seeded from the EXISTING compatibility
  triggers (pair_compatible → 45 warm, power_parity → 30 moderate, else 15 cold). The Zongli-Yamen
  factor (#357) rides every pulse; MARRIAGE_PLAY_add_incentive (dowry/gifts, +10 success, -50 treasury)
  is the player lever; adverse events ride the generic play-event system.
- **D28 (two-step picker):** new marriage_play_window.gui — 3 columns (target realm → our unmarried
  char → their opposite-gender unmarried char), ruling family FIRST (two-pass add: from_ruler_family
  then the rest), MINORS INCLUDED (betrothal path). Backed by MARRIAGE_PLAY_actions.txt (pick_realm/
  pick_own/pick_their/launch) + list-builders in se_MARRIAGE_PLAY.txt. Opposite-gender fixed by our
  pick's sex (rebuilds their list on pick).
- **D29 (deletion):** DELETED gui/marriage_window.gui + common/scripted_guis/MARRIAGE_actions.txt
  (the old Dynastic Match window/builder — fixes the F5 empty-list bug by removal). Verified no
  live dependency: the AI marriage pulse (se_MARRIAGE.txt) uses none of the deleted GUI defs; the
  only remaining reference is a comment in MARRIAGE_svalues.txt (left in place — its svalues may be
  shared with se_MARRIAGE, deleting risks breakage; a dead comment is harmless). government_view
  button swapped to open the new picker.
- New files: se_MARRIAGE_PLAY.txt, MARRIAGE_PLAY_actions.txt, gui/marriage_play_window.gui,
  qing_marriage_play_l_english.yml; edited se_DIPLOMACY.txt (finale branch), government_view.gui.

### #357 Zongli-Yamen global play-success factor + #354 Zongli Yamen panel — BUILT
- **D22:** qing_min_perf_zongli = Director charisma (dev-7 x4) + DIPLOMAT-CORPS staffing
  (count vs a healthy ~4, x2; empty corps penalised). Rebuilds qing_zongli_diplomats (a
  courtier list flagged qing_zongli_diplomat) for the panel. Folds into the Director's
  council standing via the shared fold.
- **D23 (#357 the global factor):** QING_zongli_play_boost applies once per Qing pulse to
  EACH of the Qing's OWN live plays (spliced into QING_gp_scan_plays' (A) instigator=self
  branch, in the play-provobj scope): converts (perf-50)/25 into a ±success delta via
  DIPLOMACY_modify_play_success (clamped 0..100, idempotent-safe to re-apply). So a well-run
  Zongli advances every play, a poor one fumbles it — applies to ALL plays incl. the #356
  marriage play. Reads the Qing perf var via $home$.var: (proven se_AI.txt:1202).
- **D24 (#354 diplomats):** the "lower-ranked diplomats reporting to the Grand Director" are
  courtiers flagged qing_zongli_diplomat, appointed via qing_zongli_appoint_diplomat (a new
  row in the shared court picker keyed on qing_gc_picker_office='zongli_diplomat', capped at
  6) and recalled from the panel roster. Reuses the proven picker + refresh idiom.
- **REVIEW FIX (from #349 review, applied here too):** all scratch-var reads use `add =
  var:X` — the bare-name `add = X` bug the #349 review caught (bare name resolves as an
  undefined script_value = 0, pinning the meter at 50). Fixed the War + Lifan Yuan reads and
  wrote the Zongli reads correctly from the start.
- New files: QING_zongli_panel.txt, gui/qing_zongli.gui, qing_zongli_l_english.yml; edited
  se_QING_MINISTRY.txt (+zongli perf +play-boost +dispatcher), se_QING_DIPLO.txt (scan
  splice), imp19c_windows.gui (picker diplomat row), government_view.gui (button).

### #346 Frontier-garrison overlay + War↔Lifan-Yuan turf war — BUILT + REVIEWED (fixes applied)
- **REVIEW — 1 BLOCKER + 3 real findings fixed:**
  1. (BLOCKER) `QING_fgar_scan` iterated c:CHI's OWN `every_army` with `commander={employer=ROOT}`
     — but subject-soil frontier garrisons are RAISED IN THE SUBJECT'S SCOPE with a subject-employed
     commander (#338/B21), so CHI's own armies never see them: the scan could NEVER match. FIX:
     rewrote the scan to iterate `every_subject` (autonomous_governorship) and detect a garrison the
     SUBJECT itself fields on its own soil (`any_army { is_moving=no in_combat=no unit_size>=3 }`) —
     THAT is the frontier banner host. Dropped the `commander=employer=ROOT` filter + the dead
     commander-scope save. Proven idioms: `every_subject` (INCOME_svalues), `any_army` (agadir_crisis
     naval sibling `any_navy`), `is_subject_type=autonomous_governorship` (00_monthly_country).
  2. (major) occupation-modifier FLICKER — duration 200 under a `NOT has_country_modifier` add-guard +
     180-day throttle meant the modifier lapsed at T200 and wasn't re-added until T360 (~44% of every
     cycle the -10 loyalty_to_overlord vanished though the garrison stayed). FIX: unconditional
     remove-then-add each cycle (the #347 refresh idiom) → continuously present.
  3. (minor) opinion STACKING — `add_opinion` fired unconditionally every 180d, laying unbounded
     -10 instances. FIX: fire the opinion ONCE at occupation ONSET (guarded on the modifier being
     absent = garrison just arrived); the continuous drag is carried by the modifier itself. Avoided
     the review's suggested `has_opinion` guard (UNPROVEN in this codebase — used nowhere else).
  4. (minor) missing loc key `qing_amban_cooperation_opinion` (option B) + the parallel unlocalized
     amban opinions. FIX: added loc for cooperation/clash/capable/ineffective to qing_amban_l_english.yml
     (single home, no dup). Also wired the previously-dead `qing_frontier_garrisoned` var LIVE into the
     Lifan Yuan panel roster (a "#R Under imperial garrison#!" marker per dependency).
- Re-verified brace balance (se_QING_FRONTIER 41/41, qing_lifanyuan.gui 84/84, event 22/22).

### #346 Frontier-garrison overlay + War↔Lifan-Yuan turf war — original BUILD notes
- **D18 (overlay, not re-architecture):** the setup OOB deliberately raises subject-soil
  frontier garrisons UNDER the subject for engine placement-validity (#338/B21). #346 does
  NOT change that — it LAYERS on the #347 detection idiom: a Qing pulse (QING_fgar_scan, hooked
  into 00_monthly_country after QING_GOV_pulse) finds every settled army whose COMMANDER is
  c:CHI-employed sitting on an autonomous-governorship subject's province, and applies the
  occupation consequences to that dependency.
- **D19 (consequences):** per garrison, throttled ~180d/subject: (1) TIGHTEN integration
  (SUBJ_QING_advance_integration steps=1); (2) chafe — a subject-facing loyalty_to_overlord
  drag (qing_frontier_occupied modifier) + qing_frontier_occupation_opinion; (3) if the Lifan
  Yuan office is filled AND a resident Amban shares the ground AND a War Minister sits, roll a
  turf-war event (qing_frontier.1, ~1/yr): govern-by-army (integration presses, Lifan affronted)
  / govern-by-resident (dependency soothed, garrison reined) / divide authority.
- **D20 (prefix rename):** effects renamed QING_fgar_* to avoid confusion with the existing
  QING_frontier_flavour_roll decline dispatcher; vars/event/modifiers keep the clear
  qing_frontier_* namespace.
- **D21 (LESSON — same as the #347 blocker #2, applied here):** scripted EFFECTS must live in
  common/scripted_effects/ (se_QING_FRONTIER.txt), CALLED from the on_action; the on_action file
  holds only on_action blocks. Confirmed my new effect files obey this.
- New files: se_QING_FRONTIER.txt, qing_frontier_events.txt, qing_frontier_l_english.yml;
  edited qing_amban_modifiers.txt (+occupied modifier), imp19c_opinions.txt (+occupation
  opinion), 00_monthly_country.txt (scan hook). Panels #349/#350 surface it via the subject's
  qing_frontier_occupied modifier + qing_frontier_garrisoned var (visible on the amban roster).

### #351 Ministry of Works (工部) panel — BUILT (pending review)
- **D30 (perf):** qing_min_perf_works = Works minister's FINESSE (dev-7 x4, the same stat
  se_QING_WORKS gates its build effects on) + WORKS COVERAGE (count of standing dikes/canal-
  depots/wall-sections/state-manufactories vs a healthy ~8, x2) − CORRUPTION drag (河工 graft,
  corruption/10, 0..-10). Vacant office → 25. Rebuilds qing_works_provinces (every province
  holding a Board-of-Works building) + tallies qing_works_building_count for the panel. Folds
  into the Works minister's council standing via the shared fold (already wired at
  se_QING_COUNCIL.txt:1389 QING_council_perf_accumulate office=works — no council edit needed).
- **D31 (interactive panel, not just a dashboard):** unlike the read-only War/Lifan panels, the
  Works panel has COMMISSION BUTTONS (dike/canal-depot/Great-Wall) that call the EXISTING proven
  se_QING_WORKS build effects on the capable route (cheap=no), each is_valid-gated on a filled
  Works office of finesse≥7 + the treasury/stability the effect needs + a province lacking that
  building. Reuses se_QING_WORKS entirely — no new build logic. Province roster uses the proven
  Scope.GetProvince datamodel idiom (qing_province_reports.gui:50) with a goto_button.
- **D32 (icons):** finesse read-out via the proven `icon_civic` template; header icon =
  menu_trade.dds (menu_technology.dds does NOT ship — verified the menu_buttons set). 
- New files: QING_works_ministry_panel.txt, gui/qing_works_ministry.gui, qing_works_ministry_
  l_english.yml; edited se_QING_MINISTRY.txt (+perf +dispatcher) + government_view.gui (button,
  in the strip restored by REG1).

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

### #353 Ministry of Rites (禮部) panel — BUILT (pending review)
- **D33 (perf):** qing_min_perf_rites = Rites minister's ZEAL (dev-7 x4, the ceremony + the
  examinations are the Board's charge, so zeal is its governing skill) + TRIBUTARY COVERAGE
  (count of tributary subjects vs a healthy ~4 court, x2) + EXAM HEALTH ((qing_exam_pass_rate
  −50)/5, a bounded ±10 band, guarded on the exam system being initialised). Vacant office →
  25. Rebuilds qing_rites_tributaries (tributary-country list, via the proven
  QING_tribute_is_tributary_trigger) + tallies qing_rites_tributary_count for the panel.
  Folds into the Rites minister's council standing via the shared fold (office=rites already
  enumerated at se_QING_COUNCIL — no council edit needed).
- **D34 (read-only dashboard):** unlike the Works panel, Rites is a pure read-across — the
  tribute embassies + exams run on their own pulses (se_QING_TRIBUTE / se_QING_EXAM); this
  panel surfaces the minister card, perf meter, exam-pass-rate + tributary-count read-outs,
  and the tributary-country roster (Scope.GetCountry + new_country_flag, the qing_lifanyuan.gui
  idiom). No action buttons — nothing new to drive, so none invented.
- **D35 (icons):** zeal read-out via the proven `icon_religious` template; header icon =
  menu_religion.dds. Both verified in the shipped menu_buttons / shared_icons sets.
- New files: QING_rites_ministry_panel.txt, gui/qing_rites_ministry.gui, qing_rites_ministry_
  l_english.yml; edited se_QING_MINISTRY.txt (+perf +dispatcher) + government_view.gui (button,
  in the col2 strip after Works).

### #356 REVIEW — 4 confirmed findings fixed (post-commit, adversarial workflow wf_6c025264)
The #356 marriage-proposal play review confirmed 1 blocker + 2 major + 1 minor in the
already-committed code. All fixed on merge-overnight:
- **(BLOCKER) MARRIAGE_PLAY_build_their mixed `this` and ROOT scopes.** Called from two
  scripted-guis: pick_realm (GUI scope=country → ROOT==this) AND pick_own (GUI scope=character,
  SetRoot=Character; builder runs inside `scope:player={}` so `this`=country but ROOT=the clicked
  character). The `ROOT = { add_to_variable_list ... }` writes + `ROOT = { var:want_male }` reads
  therefore appended to the CHARACTER and read an unset var in the pick_own path → column 3 emptied
  after picking an own char + the sex filter always fell to female. FIX: `save_scope_as =
  mplay_home_country` (=`this`, the country in BOTH paths) at the top; replaced all 4 ROOT refs
  (2 want_male reads + 2 list writes) with scope:mplay_home_country. NOT scope:player (absent in
  the pick_realm path).
- **(MAJOR) No opposite-sex guard → same-sex pair could launch + silently no-op.** Columns are
  clickable in any order; a stale same-sex their_pick could survive a re-pick, and marry_character
  rejects same-sex → play consumed, begin-price paid, no marriage, false WED log. FIX: added an
  OR(opposite-sex) clause to marriage_play_launch.is_valid; and in marriage_play_pick_own, after
  the their-list rebuild, drop a now-invalid same-sex marriage_play_their_pick so the player
  re-chooses from the correctly-sexed column.
- **(MAJOR) Marriage play's monthly territorial-crisis dispatcher not goal-guarded.** play_target_
  area = the proposer's OWN capital, so DIPLOMACY_trigger_diplomatic_play_event fired send_settlers/
  agitator/Fashoda/Agadir AT the proposer's own capital (loyalty damage) and could escalate to a
  conquer-wargoal war on it. FIX: wrapped the whole early/middle/late event body in
  `if = { limit = { NOT = { var:play_goal = flag:marriage_proposal } } ... }`. A marriage play has
  no territorial locus; its progression is the seeded success + Zongli factor (#357) + the
  goal-guarded finale (MARRIAGE_PLAY_resolve).
- **(MINOR) Foreign spouse's marriage_origin_country never stamped.** The AI paths
  (se_MARRIAGE.txt:404/:956) tag the incoming consort so the Grand Council foreign-spouse lobby
  (qing_office.30) can fire; the play path didn't. FIX: in BOTH the marry branch and
  MARRIAGE_PLAY_betroth_pair, stamp scope:mplay_bride.marriage_origin_country = scope:play_target_
  country when she is female (mplay_bride is always the target-court char).
- Two findings correctly REJECTED by the verify pass (betrothal-overwrite self-heals via
  MARRIAGE_check_betrothals; MARRIAGE_PLAY_add_incentive is inert dead code, not a defect) — left
  as-is; add_incentive stays for a future mid-play incentive button.

---

## #355 — Ministry of Revenue panel (戶部)

Built the Board of Revenue as an INTERACTIVE Grand-Council-clone L4 panel (the Works pattern,
not the read-only Rites/War/Lifan pattern) — it owns the imperial fisc and gives the Revenue
minister two levers. All fiscal logic reuses existing se_QING_REVENUE.txt — no new fiscal code.

- **D36 — Perf spine (folds into the Grand Council).** `qing_min_perf_revenue` recomputed in
  `QING_ministry_recompute_perf_revenue`, registered in the `QING_ministry_recompute_all_perf`
  dispatcher (se_QING_MINISTRY.txt). Formula: base 50; filled → (finesse−7)×4 [finesse is the
  Board's governing skill] + (granary_count−5)×3 [ever-normal reserves vs a healthy establishment
  of ~5] + 10 if the salt gabelle is reformed − currency_stress/6 [the 銀荒 silver drag]
  − corruption/10; vacant floor = 25; clamp 0..100. The council fold needs NO edit — the office
  key `revenue` is already enumerated in QING_council_perf_accumulate.
- **D37 — Granary roster as concrete province links.** The compute effect rebuilds
  `qing_revenue_granaries` (every owned province holding `qing_granary_building`) +
  `qing_revenue_granary_count` each pulse, following the concrete-over-abstract rule. The panel
  scrolls this as a province roster with goto_buttons (the Works-panel datamodel idiom).
- **D38 — Two action levers, both reusing proven logic.**
  (1) STOCK A GRANARY (常平倉): `qing_revenue_ministry_stock_granary` — gated on a seated minister
  with finesse ≥ 7, treasury ≥ 60, and a Yellow-River city province (北京/天津/保定/開封/濟南);
  charges −60 treasury then calls the proven `QING_revenue_stock_granary`.
  (2) REFORM THE SALT GABELLE (鹽政): `qing_revenue_ministry_reform_salt` — gated on a seated
  minister + an unreformed gabelle; fires the proven `qing_revenue.1` event with its fitness-gated
  reform/milk/defer choices.
- **D39 — Read-outs.** Perf meter, granary count, silver-crisis (qing_currency_stress),
  salt-gabelle reformed/unreformed state (via the `qing_revenue_ministry_salt_reformed` indicator),
  finesse minister card (icon_civic/GetFinesse), and the shared council-contrib line.
- Header icon menu_trade.dds (fisc); window `qing_revenue_ministry_panel`; open button wired into
  the government_view col2 strip after Rites. All referenced vars/effects verified to exist.

### #355 adversarial review (wqa00aa7e) — 2 MAJOR fixed + 1 systemic MINOR ruled-on

- **R355-MAJOR-1 (granary treasury sink — FIXED).** `qing_revenue_ministry_stock_granary` charged
  −60 treasury on EVERY click but `QING_revenue_stock_granary` could re-target an already-granaried
  province (its `random_owned_province` limit lacked a NOT-has_building guard) → pure treasury sink
  for zero coverage gain once all 5 Yellow-River cities were stocked. Fixed BOTH ends: (a) added
  `NOT = { has_building = qing_granary_building }` to the panel button's any_owned_province is_valid
  (disables the button once all covered — matches the works-build siblings); (b) changed the effect
  to `ordered_owned_province` + `order_by = total_population` + `max = 1` + the same NOT-guard in the
  limit, so it stocks the largest uncovered city and never lands on a granaried one.
- **R355-MAJOR-2 (salt-reform money printer — FIXED).** The panel bypassed the AI pulse's 270-day
  `qing_revenue_event_cooldown`, so a below-fitness minister could re-click `reform_salt` every 1–3
  days and repeatedly take qing_revenue.1 Option B (+80 treasury, flag never set) — an unbounded coin
  printer. Fixed: is_valid gained `NOT = { has_variable = qing_revenue_event_cooldown }`; effect now
  stamps `set_variable = { name = qing_revenue_event_cooldown  days = 270 }`, mirroring the pulse gate.
- **R355-MINOR-systemic (finesse double-fold — RULED DELIBERATE, comment corrected).** The reviewer
  correctly noted the Revenue minister's finesse reaches `qing_council_eff_target` twice: once via
  `QING_council_score_office{ office=revenue skill=finesse }` (se_QING_COUNCIL.txt:158) and again via
  perf term (a) `(finesse−7)×4` folding through `QING_council_perf_accumulate`. This is the SHARED
  spine across all ministries #349–#354, so any change is systemic. **Decision: keep term (a), do NOT
  strip it.** Rationale: term (a) is what makes each panel's *performance bar* read sensibly (a skilled
  minister with average fiscal OUTPUT must not display a flat neutral 50); its second path into
  eff_target is negligible — `(finesse−7)×4` averaged across filled offices then /5 in the accumulate
  → **<±0.5 pts of eff_target**, a mild competence reinforcement, not a real double-weighting. The
  meter's true signal is the OUTPUT terms (b)–(e): granary coverage, salt reform, silver-crisis drag,
  corruption drag. **The actual bug was the misleading header comment** ("…not the man again"), which
  claimed the fold avoided re-scoring the skill — it doesn't. Corrected the comment (se_QING_MINISTRY.txt
  lines 439–442) to document the deliberate, bounded double-contribution rather than deny it.

---

## #358 — Hanlin Academy panel (翰林院)

Built the Hanlin Academy as an INTERACTIVE Grand-Council-clone L4 panel (the War/character-roster
pattern). All talent logic reuses the existing se_QING_EXAM.txt scholar-pool substrate — no new
appointment code.

- **D40 — Office mapping: Hanlin → grand_secretariat (NOT a 14th council seat).** Historically the
  Hanlin Academy is the scholar corps from which the Grand Secretaries (大學士) were drawn; the
  Academy's leader for Grand Council purposes IS the grand_secretariat office-holder. So #358 does
  NOT add a new council office (the locked GC spec is unchanged) — it builds the CANONICAL
  `QING_ministry_recompute_perf_grand_secretariat` compute and registers it in the ministry
  dispatcher. The council fold already enumerates the `grand_secretariat` office key, so the perf
  auto-folds with NO se_QING_COUNCIL edit.
- **D41 — Perf formula (folds into the Grand Council).** base 50; filled → (finesse−7)×4
  [大學士's drafting/administration skill] + (hanlin_scholar_count−4)×3 [waiting laureate bench vs
  a healthy ~4] + (exam_pass_rate−50)/5 [examination vigour net of 捐納/corruption drag]
  − corruption/10; vacant floor = 25; clamp 0..100. Scratch reads use var:X.
- **D42 — Concrete roster.** The compute rebuilds `qing_hanlin_scholars` + `qing_hanlin_scholar_count`
  each pulse from the live exam pool (qing_scholar_pool, living + employed) — the panel renders it
  as a character roster (finesse + charisma cards). Concrete-over-abstract: the bench IS the pool
  of real jinshi/juren characters se_QING_EXAM.txt already mints.
- **D43 — One action lever.** DRAW A LAUREATE (掄才): `qing_hanlin_draw_scholar` calls the proven
  `QING_exam_fill_first_vacant_from_pool` (seats the ablest waiting scholar in the first vacant
  great office; a no-op if every office is manned, leaving him in the pool). Gated on a non-empty,
  un-officed bench.
- **D44 — #361 SCOPE COLLAPSE.** #361 (Central Secretariat 內閣 = the grand_secretariat office
  bureaucracy) now overlaps almost entirely with #358: the perf var + council fold are done here.
  #361 will be re-scoped to a THIN follow-on (an 內閣-flavoured second view / edict-drafting lever)
  or folded into #358 outright — flagged for the deferrals section rather than duplicating the perf
  spine. Header icon menu_religion.dds (scholarship); window `qing_hanlin_panel`; open button wired
  into government_view after Revenue. All referenced vars/effects verified to exist.

---

## #359 — Imperial Household Department panel (內務府)

Built the Imperial Household as an INTERACTIVE Grand-Council-clone L4 panel over the EXISTING
se_QING_HOUSEHOLD.txt substrate (privy purse, eunuchs, workshops) + its 4 events
(qing_household_events.txt). No new household code — three action levers each fire a proven event.

- **D45 — Perf compute (chamberlain office).** Added `QING_ministry_recompute_perf_chamberlain`,
  registered in the dispatcher. Formula: base 50; filled → (charisma−7)×4 [內務府's governing
  skill] + (privy_purse−50)/4 [the emperor's private reserve health] − 20 if a eunuch faction
  leader stalks the court [the chamberlain's signal charge is checking the eunuchs] − corruption/10;
  vacant floor = 25; clamp 0..100. Council fold needs NO edit — the `chamberlain` office key is
  already enumerated.
- **D46 — No roster.** Unlike the roster panels, the household is the privy purse + the eunuch
  danger, not a set of on-map objects — the panel reads the purse var + the eunuch indicator
  directly (a read-out panel with action levers, not a dynamicgridbox).
- **D47 — Three action levers, all reusing proven events.**
  (1) MANAGE THE PRIVY PURSE (內帑): fires qing_household.1 (replenish/tap/drain), gated on the
  purse being tracked.
  (2) DEAL WITH THE EUNUCHS (太監): fires qing_household.2 (check/indulge/instrument), both
  is_shown AND is_valid gated on a live eunuch faction leader existing (button hidden otherwise).
  (3) COMMISSION THE WORKSHOPS (造辦處): fires qing_household.3, gated on a seated chamberlain
  with charisma ≥ 8 (matching the event's own gate, so button and event agree).
- **D48 — Loc appended, not overwritten.** qing_household_l_english.yml already held the 4 events'
  keys; the panel keys (QING_HOUSEHOLD_*) were APPENDED. Header icon menu_trade.dds (silver/fisc
  flavour for the privy purse); window `qing_household_panel`; open button wired into government_view
  after Hanlin. All referenced vars/effects/events verified to exist.
- **D49 — #360 (Harem 後宮) sits under this Neiwufu.** The harem mechanic will hook into the same
  chamberlain office / household substrate (consorts as household characters). Not built here.

---

## Review fixes — #351 & #353 (from adversarial-review workflows)

- **#351 fix (review whzuingvk, MAJOR).** `qing_works_building_count` in
  `QING_ministry_recompute_perf_works` added only +1 per province holding any works building, but
  the three commission routes (dike/canal/wall) all site into the single highest-population province
  (`ordered_owned_province order_by total_population max=1`), so several works stack in one province
  and read as 1 — depressing qing_min_perf_works below its true value. FIX: keep the province joining
  the roster once, but tally EACH of the 8 works-building types it holds via per-type guarded `if`
  increments. Commit 26d7acf49.
- **#353 fix (review w0i9921w4, minor, cross-cutting).** In qing_mechanics_on_actions.txt the
  game-start seed ran `QING_ministry_recompute_all_perf` BEFORE `QING_council_autofill`, so every
  ministry computed its vacant floor (25); the offices then autofilled and folded that stale vacant
  value into council effectiveness until the first quarterly pulse (~90d) self-healed it. FIX:
  reorder to `QING_council_autofill` → `QING_ministry_recompute_all_perf` → `QING_council_recompute`
  so the council reads real filled-office perf from game start. Affects ALL ministries, not just
  Rites. Commit 26d7acf49.
- **#351 fix (review whzuingvk, minor — wrap).** All 8 ministry panels' vacant-post and
  empty-roster notes used `size={460 26}` with no `multiline`, clipping their ~90-char loc strings
  to one line (violates the text-wrap standing rule). FIX: `multiline=yes` + `size={460 46}` on all
  15 such notes across qing_household/lifanyuan/hanlin/revenue/war/rites/zongli/works. Commit 15b45c7d5.
- **#353 review — BOM findings REJECTED (real=false).** The verify pass rejected the "loc file
  missing UTF-8 BOM breaks CJK rendering" finding: 5 sibling CJK panels already ship BOM-less on
  master (user-verified-in-game) and render fine; the loader decodes valid UTF-8 without a BOM. No
  action. (Recorded so the deferrals section doesn't re-surface it.)

---

## Review fix — #359 (review wo4tx38hv, MAJOR)

- **#359 privy-purse lever false affordance.** `qing_household_manage_purse`'s is_valid gated only
  on `has_variable = qing_privy_purse`, but the event it fires (qing_household.1) is
  is_triggered_only with trigger `var:qing_privy_purse < 35`, re-checked at fire time. Since
  QING_household_init seeds the purse to 50, the button was live at game start yet fired a silent
  no-op (the event dropped itself). The sibling eunuch + workshop levers correctly mirror their
  events' gates; only this one omitted it. FIX: add `var:qing_privy_purse < 35` to the lever's
  is_valid + update the tooltip to state the low-purse requirement. Commit 13e641cce. (All 3
  confirmed findings were the same bug, de-duplicated.)

## Review fix — #358 (review wru2g1xcn, minor)

- **#358 Draw-a-Laureate inert when council full.** `qing_hanlin_draw_scholar`'s is_valid gated
  only on a waiting un-officed scholar in qing_scholar_pool, not on an actual office vacancy. With
  all 13 offices manned the button stayed enabled, QING_exam_fill_first_vacant_from_pool no-op'd,
  yet the effect logged a false success — contradicting the lever's own comment/tooltip. FIX: add
  `has_variable = qing_council_vacancy` + `var:qing_council_vacancy > 0` (maintained by
  QING_council_recompute, exact 13-office scope). Commit a051ee49b. (All 3 confirmed findings were
  the same bug.)

---

## #360 — Harem (後宮) — imperial consorts under the Neiwufu

Built the imperial harem as a CONCRETE roster of on-map consort characters under the Imperial
Household Department (內務府), whose health folds into the chamberlain's Grand Council standing —
the throne's succession engine, not a new council seat. New se_QING_HAREM.txt + gui/qing_harem.gui
+ common/scripted_guis/QING_harem_panel.txt.

- **D46 — Concrete roster, not a counter (house rule).** `qing_harem_consorts` is a variable_list
  of REAL female characters (created via the proven create_character roster idiom, mirroring
  QING_exam_mint_scholar), each marked `qing_is_harem_consort`. `qing_harem_consort_count` is kept
  in step for the GUI + perf. Self-healing: `QING_harem_recompute_roster` rebuilds the list fresh
  from the live marked characters (prunes dead/departed) each quarterly perf recompute + on panel
  open; `QING_harem_remove_on_death` (hooked into on_character_death after the exam prune) keeps the
  count honest immediately.
- **D47 — Folds into the chamberlain (the HARD wire).** Added term (e) to
  `QING_ministry_recompute_perf_chamberlain` (se_QING_MINISTRY.txt): rebuild the roster, then score
  `(consort_count − 4) × 2` into qing_min_perf_chamberlain (a full court of 8 → +8, an empty one →
  −8), bounded so it stays a MINOR term next to the charisma/purse/eunuch/corruption terms. The
  chamberlain office key is already enumerated in the council perf fold, so NO se_QING_COUNCIL edit —
  the harem's health reaches the Grand Council through the chamberlain, per the standing requirement
  that every bureaucracy's performance determines its leader's council performance.
- **D48 — Heirs via make_pregnant, NOT create_character parentage.** FAVOUR A CONSORT (臨幸) gets a
  consort with child by the emperor via `make_pregnant = { father = <emperor scope>  known_bastard =
  no  number_of_children = 1 }` run on the WOMAN. RATIONALE: this session's oracle consultation
  verified make_pregnant with 3 verbatim Invictus examples (father can be ANY char scope, not just a
  spouse), whereas create_character with `father=`/`mother=` has ZERO proven usages I could point to.
  Per the proven-code rule I used the verified idiom. It is also more robust — the child is borne
  through the engine's own birth mechanic, so legitimacy / dynasty / the family graph (and thus the
  succession) are handled natively rather than hand-assembled. Guarded on a male reigning emperor +
  a living, `is_pregnant = no` consort (both effect and panel button), so a favouring never
  double-conceives an already-pregnant woman and the button is not a no-op affordance.
- **D49 — Init ordering gotcha (dedicated flag, not the count var).** The perf recompute runs at
  game-start (on_action line 48) BEFORE QING_harem_init (~line 110) and calls
  QING_harem_recompute_roster, which SETS qing_harem_consort_count. So QING_harem_init guards on a
  dedicated `qing_harem_initialized` flag — guarding on the count var would wrongly skip minting the
  opening inner court of 3. (This is the same class of ordering bug as #353's game-start fold order.)
- **D50 — AI-autonomous + panel levers.** QING_harem_pulse (governance pulse, after
  QING_household_pulse) rebuilds the roster, rolls a 20%/quarter favoured-consort birth (so the inner
  court does its dynastic work AI-side too), and drifts dynastic-harmony down a touch under a
  vacant/venal chamberlain. Two GUI levers (選秀 draft gated below a court of 8; 臨幸 favour) reuse the
  same proven effects. Draft nudges dynastic-harmony +2; a birth nudges it +4 and the consort +15
  prestige. Panel opened from a button in gui/qing_household.gui (the harem sits under the Household).
- All idioms verified proven: create_character roster + add_* + set_home_country (se_QING_EXAM);
  random_in_list + limit (se_EDU); is_pregnant (schemes/death); variable_list roster + on-death prune
  (se_QING_EXAM); make_pregnant (Invictus oracle, this session). Brace balance 76/76, 27/27, 83/83.

---

## #361 — Central Secretariat (內閣) — the working chancery

**Commit:** (pending) · Built on `merge-overnight`. Files: `common/scripted_effects/se_QING_SECRETARIAT.txt` (NEW), `common/scripted_guis/QING_secretariat_panel.txt` (NEW), `gui/qing_secretariat.gui` (NEW), `common/scripted_effects/se_QING_MINISTRY.txt` (term (e)), `gui/qing_hanlin.gui` (open button), `common/on_action/qing_mechanics_on_actions.txt` (init), `common/scripted_effects/se_QING_GOVERNANCE.txt` (pulse), `localization/english/qing_secretariat_l_english.yml` (panel loc).

- **D51 — Re-scoped to a THIN facet, NOT a second office/meter (the key call).** The design doc
  (overnight_design4.md:58/61) pairs #361 with #358: *"grand_secretariat | 內閣 | ... Central
  Secretariat — fed by Hanlin (#361/#358)"* and *"Hanlin Academy (#358) feeds #361."* Both target
  the SAME `grand_secretariat` office key. #358 already built the full perf meter
  (qing_min_perf_grand_secretariat), the Hanlin scholar roster, the draw-scholar lever, and the
  council fold. A second full panel with its OWN perf meter would double-count into the fold. So
  #361 is built as the WORKING-CHANCERY facet of that one office (exact mirror of the #360
  harem→household precedent, D46/D47): the Hanlin is the talent RESERVOIR, the 內閣 is where those
  men WORK. It reuses the existing meter — no new meter, NO council edit.
- **D52 — Concrete rescript backlog (票擬積壓), not an abstract score (house rule).**
  `qing_secretariat_backlog` (0..100) is the concrete measure of chancery throughput. Fresh
  rescripts accumulate +6/quarter (the throne's business never stops); a live Grand Secretary
  works it DOWN by his charisma (his drafting throughput — able hand charisma 10 clears ~10/qtr
  = net −4; weak hand charisma 5 clears ~5 = net +1 creep). A vacant chancery has no throughput,
  so it climbs untended. Clamp 0..100.
- **D53 — Folds into the EXISTING grand_secretariat meter (the HARD wire).** Added term (e) to
  QING_ministry_recompute_perf_grand_secretariat (se_QING_MINISTRY.txt): backlog deviation from a
  tolerable 30, /4 (bounded so it neither dominates the finesse/Hanlin terms nor is negligible),
  ADDED to the meter (a cleared backlog < 30 lifts it, a choked one > 30 drags it). Inside the
  office-FILLED branch (a vacant office already floors the meter at 25 — no backlog term needed
  there). So the chancery's health reaches the Grand Council through the Grand Secretary's own
  standing, satisfying the HARD requirement that every bureaucracy's performance determines its
  leader's council performance.
- **D54 — CONVENE THE CHANCERY (票擬) lever + AI-autonomous pulse.** The panel's single lever fires
  QING_secretariat_convene: clears 30 backlog + generates political influence scaled by the
  secretary's charisma (charisma/2, echoing the #273 qing_secretariat.1 Edict Mill), +2 loyalty,
  on a 270-day cooldown. `add_political_influence = var:X` is proven upstream (se_INCOME.txt:500).
  Button is_valid MIRRORS the effect's own guard (present secretary + backlog ≥ 20 + no cooldown)
  so it is never a live-but-no-op affordance. The quarterly QING_secretariat_pulse runs the drift
  AI-side too; the #273 events remain the flavour beats layered on top.
- **D55 — Opened from the Hanlin panel, not a new council button.** Since it is one office, the
  內閣 window opens from a button INSIDE gui/qing_hanlin.gui (Execute + createwidget idiom), not a
  new government_view.gui council-strip entry — reinforcing "one man, one office, two facets" and
  avoiding council-strip clutter. Init guards on a dedicated `qing_secretariat_initialized` flag
  (not the backlog var) per the #360 D49 ordering gotcha (perf recompute reads the backlog at
  game-start before init).

### D56–D60 — #362 Censorate panel (都察院) + a LATENT-BUG FIX

- **D56 — FIXES a never-computed council fold (latent bug).** The council fold
  (QING_council_fold_ministry_perf) has always enumerated `office = censor`, but NO effect ever
  SET `qing_min_perf_censor` — QING_council_perf_accumulate self-guards on
  `has_variable = qing_min_perf_censor` and silently DROPPED the Censor-in-Chief from the average.
  So the censor's charge contributed NOTHING to the Grand Council. #362 builds
  QING_ministry_recompute_perf_censor + registers it in the dispatcher, closing the gap so the
  Censorate now folds into its leader's standing like every other office (the HARD requirement).
- **D57 — Concrete Inspectors-General corps (御史), not an abstract counter (house rule).** The
  panel manages a real corps of investigating censors: courtiers flagged
  `qing_is_censor_inspector`, rebuilt into `qing_censor_inspectors` + tallied each pulse (exact
  mirror of the #354 Zongli diplomat-corps archetype). Commissioned via the SHARED court picker
  keyed `censor_inspector`; capped at 6 (a select service, not the whole court); per-inspector
  recall on the roster.
- **D58 — Perf-compute (fixes the meter).** base 50; office-filled adds (finesse−7)×4 + honest/just
  +6 each + (inspector_count−4)×2 − corruption/8; vacant floors at 25; clamp 0..100. Finesse is the
  censor's governing skill (matches se_QING_CENSORATE's own vigor formula). The corruption drag makes
  the meter a real signal of the court's cleanliness, not just the man.
- **D59 — Reuses the proven Censorate domain for the IMPEACH lever.** The panel's IMPEACH THE VENAL
  lever chains the existing QING_censorate_find_corrupt (ordered_character by corruption →
  scope:qing_censorate_target) + QING_censorate_impeach_uphold (cleanse + vacate office +
  corruption −6) — no new prosecution logic. is_valid MIRRORS find_corrupt's own limit (present
  Censor-in-Chief + a venal courtier exists via any_character) so the lever is dead when the court
  is clean — no live-but-no-op affordance.
- **D60 — Opened from a government_view council-strip button (its own great office).** Unlike the
  #361 內閣 facet, the Censorate IS its own distinct great office (censor holder), so it gets its
  own council-strip open button (after the 內務府 Household button), its own window
  (gui/qing_censorate.gui), and appoint routing through imp19c_windows.gui. Open button recomputes
  the meter so the panel is fresh on open.

### #361 adversarial review (wada9zxq1) — 2 confirmed fixes applied

- **#361-R1 (major/display) — `Player.MakeScope.GetPoliticalInfluence` → `Player.GetPoliticalInfluence`.**
  gui/qing_secretariat.gui:203 read the influence pool off a GuiScope; GetPoliticalInfluence is a
  Country accessor (MakeScope exposes only GetVariable/Var/GetList/GetCharacter). The lone such call
  in the repo — fixed to the bare-Country form the 5 other influence read-outs + the vanilla topbar use.
- **#361-R2 (minor) — `add_loyalty = 2` → `add_loyalty = loyalty_qing_commended`** in
  QING_secretariat_convene. The engine's add_loyalty takes a NAMED loyalty-modifier key, not a raw
  scalar (00_imp19c_loyalty.txt:35; verified: ZERO raw-integer add_loyalty anywhere in the repo or
  the Invictus/TI oracles — every working call uses a key). A bare `= 2` silently no-ops.
- **DEFERRED (tracked, NOT defer-for-size): mod-wide raw-integer add_loyalty audit.** The review
  flagged the same no-op anti-pattern pre-existing in se_QING_HOUSEHOLD.txt (#359), se_QING_DYNASTY.txt
  (#312) and se_QING_PERSONNEL.txt — 12 sites. These belong to already-committed OTHER features and a
  proper fix needs NEW small-value loyalty keys (the existing keys are all ±12..±40, too coarse for the
  ±1/±3/±5 personnel sites) + per-site semantic mapping — genuine design, not a mechanical swap, and
  each site wants its own review. Logged as a standalone cleanup task rather than smuggled into #363.

### #360 adversarial review (wt2gzn195) — 1 confirmed fix + 1 documented no-fix

- **#360-R1 (minor, x3 duplicate reports) — harem init moved BEFORE the game-start perf fold.**
  The chamberlain's HAREM term (e) is UNGATED (unlike the has_variable-guarded privy-purse term):
  it always runs QING_harem_recompute_roster which SETS qing_harem_consort_count. QING_harem_init
  used to mint the opening 3 consorts ~66 lines AFTER QING_ministry_recompute_all_perf, so the
  game-start fold counted 0 → booked (0−4)×2 = −8 instead of the correct (3−4)×2 = −2, leaving the
  chamberlain meter ~6 pts low until the first quarterly pulse self-healed it. FIX: moved
  `QING_harem_init = yes` to right after QING_council_autofill, before the perf fold (harem_init
  needs only current_ruler + culture/religion, all present at game start). Council-target impact
  was tiny (~0.1 pt after the /12-office average /5), but the 內務府 panel meter read wrong.
- **#360-R2 (minor perf, NO-FIX, documented) — the 3 QING_harem_recompute_roster sweeps/quarter.**
  The roster sweep (O(court), one country) runs up to 3× per quarterly pulse: once in the chamberlain
  perf term (e), once in QING_harem_pulse, once on the 20% favour roll. KEPT AS-IS: each sweep is
  deliberately self-healing/self-contained (favour_consort + the panel both call it defensively so
  they never operate on a stale roster regardless of call context), the cost is a few extra court
  iterations for ONE country per quarter (negligible), and removing them would trade that for a
  fragile hidden ordering dependency. Not worth the correctness risk.


---

## D61 — #363 Board of Punishments panel (刑部, justice office)

- **Concrete object = a DOCKET (待審) of accused officials** (marked qing_justice_accused), distinct
  from the Censorate's instant impeach (#362): the 刑部 is the high COURT, so it CHARGES first then
  TRIES. Panel levers: ACCUSE the most-corrupt courtier onto the docket → CONVICT (定罪) or ACQUIT (開釋)
  each. Concrete "slaves class" hook the design called for = PENAL SERVITUDE (籍沒): CONVICT reduces a
  pop in the capital province to the slave class via the proven `set_pop_type = slaves` at capital_scope
  (naval_raiding.txt:174; `create_state_pop = slaves` is NOT attested — only freemen/tribesmen — so it
  was avoided). Guarded against a no-eligible-pop capital.
- **LATENT COUNCIL-FOLD BUG CLOSED (same class as #362 censor):** qing_min_perf_justice was enumerated in
  QING_council_perf_accumulate (se_QING_COUNCIL.txt:1388) but NEVER SET, so the self-guarding fold silently
  DROPPED the Grand Minister of Justice from the council average. Added QING_ministry_recompute_perf_justice
  (holder zeal×4 + just/honest integrity +6 each − docket-backlog×3 − corruption/8, vacant floor 25,
  clamp 0..100; rebuilds qing_justice_docket roster) and registered it in QING_ministry_recompute_all_perf.
- Files: se_QING_MINISTRY.txt (compute + dispatcher), se_QING_JUSTICE.txt (docket domain verbs),
  QING_justice_panel.txt (scripted GUIs), gui/qing_justice.gui, government_view.gui (open button),
  qing_justice_l_english.yml (panel loc appended to the #125 events loc). Commit 5de45e714.

### #362 adversarial review (wubl4n68g / wf_3edbfa91) — 3 confirmed, ALL FIXED

- **#362-R1 (major) — Impeach-the-Venal lever was spam-clickable.** No cost/cooldown: each click ran
  QING_censorate_impeach_uphold (corruption −6 + a fresh disgrace) unthrottled, so a player could floor
  qing_corruption_level to 0 in a single day and re-hammer the same already-disgraced courtier (find_corrupt
  keeps re-selecting him — disgrace keeps loyalty < 40). FIX: added a ~1-quarter cooldown
  (qing_censorate_impeach_cooldown, days=90) — is_valid now gates on NOT has_variable, effect stamps it.
- **#362-R2 (major) — inspector double-count when an inspector is promoted to a great office.** The corps
  roster/count (every_character has_variable=qing_is_censor_inspector) didn't exclude office-holders, so an
  inspector later made Censor-in-Chief was scored as chief in term (a) AND tallied in corps term (c) (+2
  inflate) and rendered in both the summit card and the roster. FIX: added NOT={has_variable=qing_office_held}
  to the roster-rebuild limit — fixes both the count and the panel render at once.
- **#362-R3 (minor) — disgraced inspector kept his corps mark.** QING_censorate_impeach_uphold cleansed/
  vacated the target but never removed qing_is_censor_inspector, so a disgraced inspector stayed a ghost in
  the corps count. FIX: remove_variable = qing_is_censor_inspector in the uphold effect (guarded).
- **Preemptive carry-over to #363:** applied the R2 lesson to the fresh Board of Punishments — the sitting
  Minister of Justice is now EXCLUDED from QING_justice_find_accusable + the accuse-lever gate (proven
  `this = scope:X` char-equality), so he can never be charged onto his own docket (which would double-role
  him). Fixes committed together in the follow-up commit.
