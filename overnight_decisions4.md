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

- **NONE.** All planned build tasks (#333–#371, the deferred exam/tributary/canal follow-ons, the
  8 candidate deep-sims, and the 13 ministry panels) were built in full — no feature was deferred for
  size or complexity, and no hard external blocker (an unproven engine capability both oracles lack,
  or a dependency on an unbuilt feature) was hit. The two remaining items are NOT build deferrals:
  (1) the develop / develop-mech-port merge PLAN (a post-build deliverable the user explicitly asked
  to draw up *after* all tasks finish, covering both the 1763 branch and merge-overnight); and
  (2) #319 in-game verification (B21/B22 unit placement, B12 marriage table, B14 Supranational) —
  owed to the USER at the game client, not codeable here.

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
  1. (BLOCKER) `QING_fgar_scan` — **SUPERSEDED; this entry's rationale was WRONG** (corrected commit
     47f06e69b, user-flagged 2026-07-12). It claimed frontier garrisons are raised in the SUBJECT'S scope
     (subject-owned/commanded) and rewrote the scan to `every_subject { any_army }`. But BT-15 (later)
     changed SE_qing_raise_garrison[_cmd] to raise them as **CHI-OWNED, CHI-COMMANDED** armies (bare
     create_unit in c:CHI scope) standing on subject soil — so `every_subject { any_army }` looked for a
     subject-fielded garrison that does NOT exist and could never match (overlay dead). CORRECTED: reverted
     to the proven `every_army` / `unit_location = { owner = { is_subject_of=ROOT  is_subject_type=
     autonomous_governorship } }` idiom (se_ARMY.txt) — iterate CHI's OWN settled armies, occupy the subject
     whose province the host stands on. Frontier garrisons ARE Qing-owned and Qing-commanded.
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


---

## D62 — #364 Imperial Guard panel (領侍衛內大臣, guard_commandant office)

- **Two concrete objects for the guard_commandant office** (whose Grand Council office was already
  fully wired — emperor-power-base reconcile + sovereign-vitality modifiers in se_QING_COUNCIL.txt,
  UNCHANGED):
  1. a **CORPS of 侍衛 guardsmen** — real courtiers enrolled into the guard (marked
     qing_is_imperial_guardsman, capped at 6), rebuilt into the qing_guard_corps variable_list each
     pulse by QING_ministry_recompute_perf_guard_commandant. Enrol via the SHARED court picker
     (qing_gc_picker_office = 'imperial_guardsman' → new picker row in imp19c_windows.gui), discharge
     per-row from the panel. The corps-roster archetype (Censorate #362 / Justice #363).
  2. the **BAYARA GUARD (巴牙喇)** — a raise-once elite legion the player musters at the capital.
- **DEVIATION FROM THE DESIGN DOC (recorded per directive):** overnight_design4.md:152 called for a
  brand-new elite unit *type* in common/units/bayara.txt modeled on regular_infantry.txt. I DELIBERATELY
  did NOT create a new unit type — a new unit type needs GFX (model/sprite/icon), tech-gating, and AI
  build-weights that cannot be tested headless (placeholder-icon risk, per the standing GFX rule). Instead
  the Bayara Guard is a **real raised legion** via the PROVEN raise_legion / capital_scope.state.governorship
  idiom (se_QING_ILI.txt:430, se_QING_SELFSTR.txt:340): 4× regular_infantry + 1 artillery, named "Bayara
  Guard". This delivers the "elite bodyguard corps under arms" concretely, on the map, at ZERO GFX risk.
  Readiness flag qing_bayara_guard_raised gates the muster (raise-once, no dead-affordance).
- **LATENT COUNCIL-FOLD BUG CLOSED (3rd of the class — after censor #362, justice #363):**
  qing_min_perf_guard_commandant was enumerated in QING_council_perf_accumulate (se_QING_COUNCIL.txt:1395)
  but NEVER SET, so the self-guarding fold silently DROPPED the Commandant from the council average. Added
  QING_ministry_recompute_perf_guard_commandant (base 50 + (martial−7)×4 + loyalty≥50 ? +6 + (corps−4)×2 +
  bayara-raised ? +10; vacant floor 25; clamp 0..100; rebuilds qing_guard_corps EXCLUDING great-office
  holders per the #362-R2 double-count fix) and registered it in QING_ministry_recompute_all_perf.
- **Enrol exclusion (baked-in #362-R2):** a great-office holder cannot also serve as a guardsman — the
  enrol verb + roster rebuild both exclude qing_office_held, so no double-role / double-count.
- Files: se_QING_GUARD.txt (new — muster verbs), QING_guard_panel.txt (new — scripted GUIs),
  gui/qing_guard.gui (new — the window), se_QING_MINISTRY.txt (perf-compute + dispatcher registration),
  government_view.gui (open button after the Justice button), imp19c_windows.gui (imperial_guardsman
  picker row), qing_guard_l_english.yml (panel loc appended to the #273 events loc). Commit 8538087c.


---

## D63 — #365 Board of Personnel panel (吏部, personnel office)

- **Concrete object = the GOVERNOR CORPS** — the provincial officialdom, real is_governor=yes engine
  characters (NOT a marked-var pseudo-object): the same corps QING_personnel_evaluate_governors and the
  大計 (Great Reckoning) review already iterate. The panel is the CENTRAL read-across-all-governors
  dashboard, mirroring the Lifan-Yuan roster-over-engine-objects archetype (#350) but with character
  items (Scope.GetCharacter) rather than country items.
- **No player governor-appointment lever** — governor assignment in this mod is AI/automatic (no proven
  player verb exists; searched common/ + setup/, only AI governor_policies + the trade governorship-tax
  plumbing). So the panel's levers act on the EXISTING corps rather than staffing it:
  1. **CONVENE THE 大計 (Great Reckoning)** — reuses the PROVEN QING_personnel_daji_review (the exact effect
     qing_personnel.1 calls), gated on the shared qing_personnel_daji_cooldown (days=1095) so the panel lever
     and the flavour event share ONE ~3-year throttle (no double-reckoning, no spam);
  2. **per-governor CULTIVATE (培養)** — a capable Minister (finesse>=9, the same threshold the 大計 rewards
     use) rewards an able governor: add_loyalty=loyalty_qing_commended (NAMED modifier) + standing lift, 1/yr;
  3. **per-governor DISCIPLINE (懲處)** — cashiers a venal/disloyal governor (corrupt|corruption>=40|loyalty<40):
     add_loyalty=loyalty_qing_disgraced + prominence cut, 1/yr.
- **PREEMPTIVE #362-R1 SPAM GUARD:** both per-governor levers carry a 365-day cooldown var
  (qing_personnel_cultivate_cooldown / _discipline_cooldown). Without it the DISCIPLINE lever would be
  infinitely re-clickable — a venal governor stays venal, so corruption>=40 keeps qualifying and the
  loyalty/prominence penalties would pile up unbounded. (The #362-R1 impeach-spam lesson, applied at build.)
- **NAMED loyalty modifiers, not raw scalars** — add_loyalty uses loyalty_qing_commended / _disgraced
  (defined in common/loyalty/00_imp19c_loyalty.txt), NOT raw integers (the #361-review no-op lesson). NOTE:
  the pre-existing se_QING_PERSONNEL.txt / qing_personnel_events.txt still use raw add_loyalty = 5/-10/-1 —
  those are the #371 mod-wide raw-integer audit's territory, deliberately left untouched here.
- **LATENT COUNCIL-FOLD BUG CLOSED (4th of the class — after censor #362, justice #363, guard #364):**
  qing_min_perf_personnel was enumerated in QING_council_perf_accumulate (se_QING_COUNCIL.txt:1385) but
  NEVER SET, silently dropping the Grand Minister of Personnel from the council average. Added
  QING_ministry_recompute_perf_personnel (finesse×4 + governor-corps-integrity term: clean% deviation from
  fully-clean, scaled 0..-25; vacant floor 25; clamp 0..100; rebuilds qing_personnel_governor_corps) and
  registered it in QING_ministry_recompute_all_perf.
- Files: QING_personnel_panel.txt (new), qing_personnel.gui (new), se_QING_MINISTRY.txt (compute +
  dispatcher), government_view.gui (open button after the Guard button), qing_personnel_panel_l_english.yml
  (new loc). Commit 1641dc32.

---

## D64 — #364 review-fix (adversarial review wf_0afce0ec-c63)

- **Bug (major, both review agents concurring):** the Bayara-Guard readiness read-out in
  gui/qing_guard.gui:195/202 gated its "Under arms" / "Not mustered" textboxes on
  `Player.MakeScope.Exists( ...GetVariable('qing_bayara_guard_raised') )`. `.Exists` is NOT a scope
  accessor — a country Scope exposes only GetVariable/Var/GetList/GetCharacter/ScriptValue; the only
  `.Exists` in the engine is `GetVariableSystem.Exists('literal_key')`. The datafunction failed to
  resolve, leaving the Bayara line permanently blank regardless of muster state.
- **Fix:** replaced with the mod's proven idiom `.GetVariable('qing_bayara_guard_raised').IsSet` (used
  30× in gui/province_window.gui shortage read-outs). Swept gui/ for the same invalid `.Exists(` pattern
  in Qing panels — no other leaks. Braces 110/110. Commit f4fc3db6.
- **Lesson (added to the GUI-accessor rule):** `Player.MakeScope` value-presence tests use
  `.GetVariable('x').IsSet`, never `.Exists(...)`; reserve `.Exists('literal')` for GetVariableSystem.

---

## D65 — #363 review-fix (adversarial review wf_7b9c40c7-9ff)

- **Bug (major):** QING_ministry_recompute_perf_justice's docket-roster rebuild (se_QING_MINISTRY.txt:840)
  omitted the `NOT = { has_variable = qing_office_held }` exclusion the sibling censor (#362-R2) and guard
  (#364) rosters carry. Failure path: an accused courtier (qing_justice_accused) who is later autofilled
  into a great office — QING_council_autofill_office excludes only sitting office-holders, not accused men —
  would be double-counted: scored as the sitting Minister of Justice's zeal AND tallied in
  qing_justice_docket_count (hit by the term-(c) backlog drag), and rendered as a Convict/Acquit row against
  himself in the panel. This is the exact double-role find_accusable's sitting-minister exclusion prevents.
- **Fix:** added `NOT = { has_variable = qing_office_held }` to the docket-sweep limit, matching censor/guard.
  Braces 525/525. Commit follows.
- **Pattern note:** this is the 3rd roster-rebuild to need the office-held exclusion (censor #362-R2, guard
  #364, now justice #363). The corps-roster archetype MUST carry `NOT={has_variable=qing_office_held}` in its
  every_character limit — folded into the archetype checklist for #336 and all future roster panels.

---

## D66 — #363/#364 SECOND-round review-fixes (adversarial verify passes)

The full review workflows (which run a find pass THEN an adversarial verify pass) surfaced findings the
first partial reads had not; my earlier D64/D65 fixes were confirmed, and these NEW confirmed findings
were actioned in commit ed4bcb10:

**#363 Board of Punishments (wf_7b9c40c7-9ff):**
- MAJOR — ACCUSE could charge a courtier who holds a DIFFERENT great office, but the docket rebuild (which
  I had just guarded with NOT={qing_office_held} in D65) excludes office-holders. So charging one produced
  an accused man who NEVER appeared on the docket: the lever visibly no-op'd and left a permanent, un-triable
  qing_justice_accused mark (a phantom docket entry once he later lost office). FIX: widened both
  QING_justice_find_accusable's limit AND the accuse is_valid gate to NOT={has_variable=qing_office_held}
  (subsumes the old sitting-Justice-minister-only exclusion). Now the accuse filters + docket rebuild agree.
- MINOR — ACQUIT required no seated Minister while CONVICT did → a headless Board could dispense clemency
  (+ free loyalty_qing_commended) during a vacancy. FIX: mirrored the seated-minister gate onto acquit.

**#364 Imperial Guard (wf_0afce0ec-c63):**
- MAJOR — qing_bayara_guard_raised was set once and NEVER cleared, fully decoupled from the legion's
  existence: a Bayara wiped in battle kept its +10 readiness (term d) forever AND left the raise-once muster
  permanently spent (dead affordance). FIX: re-coupled the flag to the concrete legion's lifetime. The muster
  now creates a MARKED founding commander (qing_is_bayara_commander) and attaches him via the proven
  create_character + add_to_legion=PREV + random_legion_unit set_as_commander idiom
  (se_QING_SELFSTR.txt:364); QING_ministry_recompute_perf_guard_commandant then AUTHORITATIVELY re-derives
  the flag each pulse from any_legion_commander{has_variable=qing_is_bayara_commander} — set while the marked
  commander still leads a legion, cleared once the Bayara is destroyed/disbanded. This simultaneously stops
  the +10 leak and reopens the muster.
  - REJECTED the reviewer's suggested fix (mark the legion + clear via on_legion_dissolved): NO variable is
    ever held on a legion scope in vanilla, Invictus, Terra-Indomita, Tianxia, or our own mod, and
    on_legion_dissolved is used nowhere — an UNPROVEN engine capability. Per the proven-idioms-only +
    oracle-before-unproven standing rules, I re-derived from the PROVEN any_legion_commander country iterator
    instead. New loc key NICKNAME_QING_BAYARA_COMMANDER.
- MINOR — the cap-6 guardsman corps could be exceeded via an office round-trip: a guardsman's
  qing_is_imperial_guardsman mark was not cleared when he took a great office, and the corps recompute
  excludes office-holders, so a returning ex-officer silently rejoined the corps as a hidden 7th without
  passing the enrol gate. FIX: QING_office_appoint now strips all three inner-court corps marks
  (qing_is_imperial_guardsman / qing_is_censor_inspector / qing_zongli_diplomat) on seating — the guard has
  the only hard cap, but batching all three keeps every enrol cap exact and forestalls the same latent leak
  in the Censorate + Zongli corps.
- **New pattern rule:** a man seated in a great office must LEAVE any inner-court corps he served in (the
  corps rosters all exclude office-holders); strip his corps mark(s) in QING_office_appoint. Folded into the
  roster-panel archetype checklist alongside the office-held-exclusion rule from D65.


---

## D67 — #362 review COMPLETED (wf_3edbfa91-10b) — 1 CONFIRMED systemic fix (supersedes the D at line 709)

The #362 adversarial review's **verify pass** completed (2026-07-11) and OVERTURNED its own find-pass:
the three find-pass findings recorded earlier (R1 spam-click cooldown, R2 inspector double-count, R3
disgraced-inspector ghost) were ALL ruled `real:false` — the code on disk already carries those fixes
(the cooldown at QING_censorate_panel.txt:130/153, the `NOT={has_variable=qing_office_held}` at
se_QING_MINISTRY.txt:764, the mark-strip at se_QING_CENSORATE.txt:147). Those were stale re-reports.

**What the verify pass CONFIRMED instead (both verifier agents, `real:true`) — a genuine SYSTEMIC bug:**
- The char-scoped appoint/recall panels (censor **and** zongli, guard, justice, personnel) run their
  immediate refresh as `scope:player = { QING_ministry_recompute_perf_X = yes }`. In a `scope = character`
  scripted_gui the execution ROOT is the appointed COURTIER; `scope:player = {}` changes THIS to the country
  but **leaves ROOT = the character** (ROOT is immutable across an effect; a scope-nav block never re-roots —
  proven by Invictus `bribe_mercenary_button` / `invest_in_state_button_effect`).
- Inside the recompute every `employer = ROOT` then compared a courtier's employer (a country) to a
  character → matched nobody. So on every appoint/recall: the corps roster rebuilt **EMPTY**, the count reset
  to **0**, the office-filled gate failed → office read **VACANT** → `qing_min_perf_X` floored to **25** — the
  exact opposite of the refresh's purpose. Self-healed only at the next monthly QING_GOV_pulse (ROOT=CHI).
  Side effect: the `< 6` corps cap in is_valid was bypassable between pulses (count kept resetting to 0), and
  an over-6 corps then inflated the corps-depth term after the pulse.
- Severity: the second verifier rated it **major** (wrong roster + vacant-floored meter until next pulse,
  cap bypass); the first rated the same root cause **minor** (transient, self-healing, the wrong meter never
  reaches the council fold because the fold recomputes only at pulse time after a fresh ROOT=CHI recompute).
  Either way it is a real runtime defect and shared across all 5 char-scoped panels.

**FIX (the root-independent option both verifiers endorsed over the delete-the-refresh stopgap):** at the
top of each of the 5 affected recomputes (`_zongli`, `_censor`, `_justice`, `_guard_commandant`,
`_personnel`) capture `save_scope_as = qing_min_recompute_ctry` — THIS is the country in ALL THREE call
contexts (pulse dispatcher, country-scoped open-button, and the `scope:player` wrapper) — then reference
`scope:qing_min_recompute_ctry` in place of every `employer = ROOT` and every `ROOT = { ... }` write. The
recompute is now root-independent, so the immediate panel refresh is correct regardless of the caller's ROOT
and the pulse-path behaviour (ROOT=CHI) is unchanged. The war/works/rites/revenue/grand_secretariat/
chamberlain/lifanyuan recomputes were left as-is — they have NO char-scoped callers (pulse + country open
buttons only), so their `employer = ROOT` always resolves to CHI. Secretariat + harem panels are all
`scope = country`. Commit on se_QING_MINISTRY.txt (braces 538/538).

**New standing rule (folded into the roster-panel archetype checklist):** a corps recompute that a
char-scoped panel refreshes MUST be root-independent — never rely on ROOT inside it. Capture the country
via `save_scope_as` at the top and reference the saved scope, because a `scope:player = {}` wrapper around a
scripted-effect call sets THIS but NOT ROOT.

## D68 — #336 Southern Study (南書房): exam-fed inner-court literary cabinet [BUILT]

The emperor's private cabinet of letters, built as a full Grand-Council-clone L4 panel. Files:
`se_QING_SOUTHERNSTUDY.txt` (124/124), `QING_southernstudy_panel.txt` (40/40),
`qing_southernstudy_modifiers.txt` (2/2), `gui/qing_southern_study.gui` (102/102),
`qing_southern_study_l_english.yml`, + open-button in `government_view.gui` and wiring in the
death hook / init on_action / governance pulse. Committed as freekumquats.

**Key design decision — the Study is NOT a Grand Council office; it FEEDS the council.** So unlike
every ministry panel (#349-#365) there is deliberately NO perf-fold into an office-holder and NO
`qing_min_perf_*` term — the #358+ ministry-perf spine is untouched. The Study's benefit is instead
COURT LUSTER (the `qing_southernstudy_luster_minor/major` country modifier: prestige + legitimacy,
and at the major tier a small assimilation-speed bump), scaled to the corps' literary depth, plus a
PROMOTION PIPELINE (the ELEVATE lever seats the chief in the first vacant great office).

**Concrete-over-abstract:** the corps is real 南書房行走 characters, not a counter. Intake is either
DRAW (掄才入直 — pull the ablest waiting exam-pool 天子門生, weighted by council-fitness svalue) or a
WILDCARD mint (高士奇 precedent — Kangxi's commoner prodigy). 1763 opens with two real laureates:
梁詩正 (探花 1730) and 于敏中 (狀元 1737); both `degree = jinshi` (探花/狀元 are palace-exam placements,
NOT traits — carried in the loc nicknames instead). Lead seat = 首席南書房行走 / "Grand Preceptor of
the Southern Study".

**Idioms reused (all proven):** the exam-pool draw + pool-exit (se_QING_EXAM.txt), the marked-courtier
roster rebuild EXCLUDING office-holders (#362-R2 double-count lesson — a promoted attendant leaves the
corps), the create_character named-roster mint (#90 rule: no modifiers inside; culture=han;
religion=root.religion; finalize in the saved scope), `QING_office_appoint_first_vacant`, and the
`qing_council_vacancy > 0` dead-affordance gate (#358). All LOG msgs static (#253). Cap = 8 attendants;
pulse self-replenishes at 25% when corps < 6 and the pool has talent.

Adversarial review launched next.

## D69 — #365 review COMPLETED (wf_983aaaac-0ff) — 1 CONFIRMED fix, 1 already-fixed

The #365 (Board of Personnel 吏部) adversarial review raised two findings:

- **R1 (major, ROOT-rebinding on the per-governor recompute-refresh):** ALREADY FIXED. The
  personnel recompute was made root-independent by the #362-R2 systemic pass — it captures
  `save_scope_as = qing_min_recompute_ctry` and references `scope:qing_min_recompute_ctry` in place
  of every `employer = ROOT` / `ROOT = {}` write (se_QING_MINISTRY.txt:1047+). So the char-scoped
  CULTIVATE/DISCIPLINE levers calling `scope:player = { QING_ministry_recompute_perf_personnel }`
  rebuild the corps correctly regardless of the caller's ROOT. Finding refuted (stale).

- **R2 (minor→CONFIRMED, DISCIPLINE no-op for its own meter):** REAL. The DISCIPLINE lever's
  tooltip promised to "purge the rot", but the effect only applied `loyalty_qing_disgraced` +
  `add_prominence = -5` — it never touched the `corrupt` trait or the `corruption` stat that SOLELY
  define the clean-count (NOT corrupt AND corruption<40). So the integrity read-out,
  qing_min_perf_personnel, and the Grand Council fold never moved on discipline. **FIX:** discipline
  now `remove_trait = corrupt` + `add_corruption = -25` (a punitive clean — deliberately NOT
  QING_char_cleanse, which would bump affinity upward; a disgraced governor is not brought closer to
  the throne). The recompute call that follows now sees a cleaner corps and lifts the meter as
  promised. Committed on QING_personnel_panel.txt (braces 59/59).

NOTE: the #365 review run appeared to stall (started 6 agents, journal recorded only 2 results, no
progress after ~09:53) — I read the journal find-pass findings directly and self-verified both
against the on-disk code rather than waiting on the orphaned run.

## D70 — #337 Upper Study (上書房): palace school tutoring the imperial princes [BUILT]

The Yongzheng-founded (1725) palace school, built as a full Grand-Council-clone L4 panel — the
TWIN of the Southern Study (#336). Files: `se_QING_UPPERSTUDY.txt` (147/147),
`QING_upperstudy_panel.txt` (57/57), `gui/qing_upper_study.gui` (131/131),
`qing_upper_study_l_english.yml`, + open-button in `government_view.gui` and wiring in the
death hook / init on_action / governance pulse (17e). Committed as freekumquats.

**Key design decision — like the Southern Study it is NOT a Grand Council office (no perf-fold),
but its benefit differs.** Where the Southern Study serves the EMPEROR (court luster modifier), the
Upper Study serves the HEIRS: its benefit is DYNASTIC. The corps of 師傅 tutors has a teaching
strength (qing_upperstudy_quality = summed finesse+martial+charisma); each pulse the schooling
progress (qing_upperstudy_schooling, 0..100) drifts toward it and nudges the EXISTING
qing_dynastic_harmony meter (>=70 → +2, <30 → −1 per pulse; a well-schooled house is secure).

**Concrete on-map coupling (concrete-over-abstract):** ties to the existing crown-prince seat
(qing_office_crownprince_holder, se_QING_SEATS.txt) — the INTENSIVE SCHOOLING (勤學不輟) lever
sharpens the reigning 皇太子's finesse (classics) + martial (國語騎射) toward a ceiling of 12,
+15 prestige, +4 harmony, once/year, gated on teaching-strength>=24. It is HIDDEN while a 密建
secret succession seals the heir (var:qing_office_crownprince_holder is cleared when
qing_secret_succession_sealed — QING_seat_refresh_crownprince) — so the lever mirrors that
(qing_upperstudy_no_crownprince inverse scripted_gui shows a "heir hidden" note instead).

**1763 masters (the two halves of a Qing prince's education):** 蔡新 (Cai Xin, 進士 1736, Han
classics master — rose from the schoolroom to Grand Secretary, the tutor-to-council arc the
ELEVATE lever models) + 觀保 (Guanbao, Manchu, the 國語騎射 master). Both degree=jinshi.

**Idioms reused (all proven):** the exam-pool draw + pool-exit, the roster rebuild EXCLUDING
office-holders (#362-R2), the create_character named-roster mint (#90), QING_office_appoint_first_vacant,
the qing_council_vacancy>0 dead-affordance gate (#358), the clamped QING_dynasty_harmony_nudge /
QING_DECLINE_nudge, and add_finesse/add_martial on live chars (proven Invictus
00_character_traits_effects.txt). Corrected 2 GUI issues pre-commit: icon_martial (nonexistent)
→ icon_military; IsFalse() wrap (unproven) → a dedicated qing_upperstudy_no_crownprince inverse
scripted_gui (the proven negation idiom). All LOG msgs static (#253). Cap = 6 masters.

Adversarial review launched next.

## D71 — CANDIDATE REORDER: #366 (Silver/Opium monetary) DEFERRED past #367 (Xinjiang) [COLLISION, not size]

Reordering the remaining candidate builds: **#367 Xinjiang Consolidation Arc is built before #366
Silver/Opium Monetary Model.** This is a COLLISION reason, not a size deferral (the standing rule
is: don't defer for size/complexity alone):

- **#366 collides with in-flight currency work.** The five most-recent master commits are ALL
  currency-layer refactors (2cc43112 foreign-influence listing, 65bf36c7 global-currency tooltip,
  d40c5c2b currency-power tooltip, plus se_CURRENCY / CURRENCY_svalues / se_CURRENCY_STRESS actively
  extended). A Qing silver/opium balance-of-trade model layered on top of a framework the user is
  currently rewriting risks immediate rework + merge conflict. There is ALSO already a
  qing_currency_stress silver-drain band mechanic (se_QING_DECLINE.txt) + a concrete smuggler-pod
  spawn (#91 item O) — #366 would need to reconcile with both. Better built once the currency
  refactor settles + with the user's input on the framework's final shape. NOT abandoned — sequenced.

- **#367 fits the 1763 zenith perfectly + is low-collision.** The Dzungar genocide + Altishahr
  (回部) conquest concluded 1759; in 1763 consolidation of the new 新疆 ("New Frontier") is THE live
  issue. It is concrete (real ILI/XNG subjects, frontier garrisons, provinces) and the existing
  se_QING_FRONTIER.txt overlay + amban/subject machinery give proven hooks to LAYER on (tuntian
  military colonies, the beg 伯克 system, Han settler inflow, khoja-revolt risk) rather than
  duplicate. Building #367 next.

(#368 Court Intrigue, #369 Population/Famine, #370 Silk Road caravan remain after; #371 add_loyalty
audit is independent and can slot in any time.)

## D72 — #336 + #337 ADVERSARIAL REVIEWS actioned (3 fixes committed)

Both study-panel reviews ran (#336 completed cleanly via workflow; #337's workflow infra stalled at
"started" with no results a second time, so I relaunched it fresh — wf_615d2605-aae). The #336
verify-pass produced ONE refuted major + TWO confirmed minors; I fixed all real findings, and
carried the structural ones across to #337 (identical idiom) proactively. Committed together:

- **[MAJOR, confirmed→fixed] Elevate cap-bypass (se_QING_COUNCIL.txt QING_office_appoint).** The
  appoint strip block cleared qing_is_imperial_guardsman/censor/zongli but NOT qing_is_southernstudy
  or qing_is_upperstudy. So a 首席/總師傅 promoted out via the 擢用 Elevate lever kept his study
  mark; when his great office was later vacated (QING_office_vacate drops qing_office_held only), the
  next recompute re-added him — count → 9/7, past the hard cap of 8/6, since the enrol gate is only
  checked on draw/mint. This is the exact #364-R2 pattern. FIX: strip both study marks in the same
  block. (NB the #336 find-pass flagged this as unstripped; the verify-pass correctly noted my fix
  was already in the working tree — real bug, now remediated + committed.)

- **[minor, confirmed→fixed] monthly_prestige is a CK3 token, not Imperator.** grep of the reference
  repos (Invictus vanilla_keys dump ~69k keys + Terra-Indomita) shows NO monthly_prestige country
  modifier — only monthly_character_fam_prestige + the confirmed-valid monthly_legitimacy. Imperator
  silently ignores unknown modifier tokens, so the Southern Study luster's prestige component was a
  NO-OP (never accrued). Swapped monthly_prestige → ruler_popularity_gain (the proven Imperator
  country-scope standing token, ~80 uses) in qing_southernstudy_modifiers.txt AND the two OTHER
  pre-existing files carrying the same latent no-op (qing_household_modifiers.txt:9,
  qing_pilgrimage_modifiers.txt:23 — both fixed too rather than left known-broken). CORRECTS the
  stale [[imp19c summer palace tree]] note that had cited monthly_prestige as "proven."

- **[minor, confirmed→fixed] init did not recompute → stale luster/quality at game start.** Both
  inits seed the 1763 cabinet (count → 2) but never called recompute, so literary/quality stayed 0
  and the luster/harmony effects did not apply until the first monthly pulse (unlike the harem, which
  folds into a game-start QING_ministry_recompute_all_perf). FIX: both inits now call their
  recompute at seed time (verified recompute does NOT call init back — no loop).

- **[tidiness] chief-on-death.** remove_on_death now clears qing_southernstudy_chief /
  qing_upperstudy_chief if the serving lead himself dies (every read-site already re-checks is_alive,
  so this was transient staleness, not a crash — fixed for cleanliness).

## D73 — #367 XINJIANG CONSOLIDATION ARC: design (1763 consolidation layer, NOT the late-Qing crisis)

Research agent returned a sourced digest (Perdue/Millward/Newby via Wikipedia). KEY SCOPING FINDING:
two Xinjiang systems ALREADY exist and #367 must LAYER, not duplicate:
  1. **se_QING_ILI.txt** = the LATE-QING (1874-81) Ili *crisis* set-piece (海防塞防之爭 debate →
     Yaqub-Beg reconquest → Chonghou/Zeng-Jize Ili diplomacy). It OWNS the qing_xinjiang_control
     meter (0..100) + the Dzungaria/Tarim province bands (qing_xinjiang_prov_secured/contested) +
     grip country-modifiers. Gated on qing_rebel_dungan (fires only after the 1860s Dungan revolt).
  2. **se_QING_AMBAN.txt** = the 駐紮大臣 resident lifecycle (post/recall/evaluate, Lifan-Yuan
     supervision, clash/gone-native events) on Inner-Asian subjects.
  3. **se_QING_FRONTIER.txt** = the #346 frontier-garrison overlay (將軍 banner garrisons on
     ILI/XNG/MKD/HLJ autonomous_governorship subjects, War-Ministry↔Lifan-Yuan turf war).

DESIGN: #367 is the **1763 CONSOLIDATION** layer that FEEDS the same qing_xinjiang_control meter in
the decades BEFORE the crisis — the historical "held it right → peaceful for 60 years, or bungled it
→ Jahangir 1826" arc. It is the player-emperor's set of consolidation LEVERS, surfaced as a panel,
that RAISE or ERODE qing_xinjiang_control and the province bands the Ili set-piece already reads. It
does NOT touch se_QING_ILI's stage machinery (that is a discrete 1874 set-piece keyed off a rebellion
flag that will not have fired in a well-run 1763 game). Concrete-over-abstract: real 屯田 tuntian
colonies (buildings/pops), real begs (伯克, minted characters on the XNG/ILI subjects), the existing
amban residents, real khoja-revolt risk. Levers historically: post tuntian colonies, appoint/discipline
begs, subsidize with 協餉 xiexiang silver stipends, settle banner garrisons. Full build detail in the
build commit + follow-on decision entry.

## D74 — #367 XINJIANG CONSOLIDATION ARC: BUILT (per D73 design)

Built the 1763 consolidation layer exactly as scoped in D73. Files (all brace-balanced 0):
- **common/scripted_effects/se_QING_XINJIANG.txt** (NEW) — init (seeds state + the 1763 opening
  beg corps 額敏和卓 Emin Khoja + 鄂對 Odui on XNG, recomputes at seed time per the #336 lesson);
  seed/mint beg (create_character #90 rule, culture=uighur religion=sunni, move_country=c:XNG,
  set_as_minor_character, QING_char_bind — mirrors QING_amban_post); recompute (rebuilds corps
  excluding office-holders per #362-R2; composite score = qing_xinjiang_control + 4/loyal-beg +
  3/tuntian capped +18 + 8 xiexiang − 6/venal-beg, clamped 0..100); FOUR levers — plant tuntian
  (spend 30, +5 grip, stamp a Dzungaria province, advance ILI integration 1 step), appoint beg
  (mint, +4 grip, cap 5), discipline beg (cashier ablest venal, +3 grip), xiexiang on/off
  (±6 grip + the drain modifier); pulse (maintenance +1 / neglect −1 drift, khoja-scare roll at
  grip≤30 & empty/venal corps); turn-a-beg (fester payoff); remove_on_death (drops beg from the
  CHI corps list — reaches CHI via c:CHI since the beg's employer is XNG).
- **common/modifiers/qing_xinjiang_consol_modifiers.txt** (NEW) — qing_xj_xiexiang (COUNTRY:
  army_maintenance_cost +0.08 drain, global_unrest −0.5, land_morale +0.02) + qing_xj_tuntian_colony
  (PROVINCE: local_tax +0.10, food +0.15, pop-cap +0.10, civilization +0.02). All tokens grep-proven.
- **common/scripted_guis/QING_xinjiang_panel.txt** (NEW) — open button + 4 lever GUIs (plant/appoint/
  discipline + xiexiang begin/cut, the two toggles mutually exclusive by has_country_modifier state);
  every is_valid mirrors the effect guard (no dead clicks); ai_is_valid=no, is_shown tag=CHI.
- **gui/qing_xinjiang.gui** (NEW) — Grand-Council-clone L4 window: grip + consolidation + beg-count +
  tuntian read-outs, 4 lever buttons (xiexiang begin/cut swap by visible=IsShown), beg roster
  (dynamicgridbox, martial+charisma icons). Mirrors qing_southern_study.gui.
- **localization/english/qing_xinjiang_l_english.yml** (NEW) — all panel/tooltip/event loc + the beg
  nickname keys (Emin Khoja / Odui / generic beg).
- **events/imp19c_mod_events/qing_xinjiang_events.txt** (NEW) — qing_xinjiang.1 khoja revolt-scare:
  suppress (spend 50, +12 grip) vs fester (−10 grip, +6 ethnic tension, turn a beg, sour KOK opinion).
  Backer = KOK Kokand ONLY (neighbouring Turkic power, per the separatism-backer standing rule).
- **common/opinions/imp19c_opinions.txt** (EDIT) — added qing_xj_kokand_emboldened (−20, decay 3).

THE FOLD (the standing directive — every bureaucracy's performance drives its Grand Council leader):
folds into the **Lifan Yuan Grand Director** (理藩院, qing_min_perf_lifanyuan) — the office that
historically governed Xinjiang. Implemented as an ADDITIVE term (c) INSIDE
QING_ministry_recompute_perf_lifanyuan (se_QING_MINISTRY.txt), NOT a post-hoc nudge — because that
recompute SETS the meter fresh each pulse and would clobber a nudge. Term = (qing_xj_consolidation −
50) / 3 → ±16 at the extremes. This is COMPLEMENTARY to the existing amban-coverage term (b): (b)
scores STAFFING, (c) scores the frontier's HEALTH — not double-counted. One-pulse lag (harmless).

WIRING: init after QING_ili_init (on_action, so the qing_xinjiang_control meter it reads is seeded
first); QING_xj_pulse after QING_ili_pulse in QING_GOV_pulse (so the ILI control-band — which runs
EVERY pulse unconditionally — has already banded this pulse's grip onto map + country); remove_on_death
after the study hooks; open button in government_view.gui after the Upper Study button.

KEY DECISIONS:
- **Layer, don't duplicate (D73 confirmed in code):** #367 only NUDGES qing_xinjiang_control (owned by
  se_QING_ILI) via the shared QING_DECLINE_nudge helper; ILI's per-pulse QING_ili_apply_control_band
  then bands it onto the map for free. #367 never touches ILI's stage machinery / Dungan gate.
- **Begs employed by XNG, corps list on CHI:** the beg's employer is the Kashgaria subject (the setup's
  "Beg appointed from Uighur nobles by a Qing amban"), but the roster variable_list lives on CHI (the
  player). remove_on_death therefore reaches the list via c:CHI, not employer (which is XNG).
- **monthly_wage_expense_add was UNPROVEN** (only my own draft used it) → swapped to army_maintenance_cost
  (80+ proven uses; xiexiang literally funded the western garrison, so semantically right too).
- All create_character honour the #90 rule (no modifiers inside; set_as_minor_character + move_country +
  QING_char_bind in the saved scope). All LOG msgs STATIC (#253). GUI text wraps (multiline+fixed width).

---

## D75 — #367 XINJIANG review-fix (adversarial review wf_2531bd20-358, 3× CONFIRMED = 1 bug)

The #367 adversarial review returned three CONFIRMED-major findings that are all the SAME defect: the
`qing_xj_khoja_pending` guard flag leaks. It is set in `QING_xj_pulse` before queuing `qing_xinjiang.1`
(days 10–40) and is cleared ONLY in that event's `immediate`. But the event re-checks its own trigger
(`qing_xinjiang_control <= 30`) at fire time; if the player pushes grip back above 30 during the delay
(via the panel's own xiexiang +6 / appoint-beg +4 levers — the *intended* response to the low-grip
warning), the engine silently cancels the event, its immediate never runs, and the flag sticks at 1
forever — permanently disabling every future khoja scare via the `NOT={has_variable}` re-queue guard.

**FIX (se_QING_XINJIANG.txt, `QING_xj_pulse`, tagged [#367-R2 review-fix]):** added a defensive clear
at the top of the pulse — if `qing_xj_khoja_pending` is set but grip has recovered above 30 (or the
control var is gone), `remove_variable` it. Mirrors the proven `qing_amban_here` defensive-clear
pattern (se_QING_AMBAN.txt). On the next quarterly pulse after grip recovers, the stale flag drops and
future scares can queue again; while grip stays <=30 the flag persists correctly until the event fires.
Braces 187/187.

**#337 review (wf_c5982a4e-a56): 0 confirmed** — both findings refuted. The ratchet concern was already
resolved by the D72 review-fix (the `var:qing_dynastic_harmony < 66` ceiling gate is present); the
missing-LOG finding is style-only (the pulse wrapper QING_upperstudy_pulse already brackets it with
LOG_enter/exit). No change.

---

## D76 — #366 SILVER/OPIUM BALANCE-OF-TRADE MONETARY MODEL (白銀外流 / 鴉片貿易): BUILT

The collision that forced the D71 deferral (a live currency refactor) is resolved (git tree clean), so
#366 is built. Full design + probe verdicts in **DESIGN_OPIUM_SILVER.md**.

**THESIS — layer, don't duplicate (same archetype as #367).** The mod already models the SYMPTOM: a
`qing_currency_stress` 0..100 meter (se_QING_DECLINE.txt term A) that drifts off the reserve ratio,
bands onto the country, and fires the decline/treaty events. #366 supplies the CAUSE — a quarterly
balance-of-trade assessment computing net silver flow (tea/silk/porcelain export INFLOW minus an
opium-import OUTFLOW) and nudging that EXISTING meter. No new stress meter, no new band machinery.

**THE GRAND-COUNCIL FOLD IS ALREADY WIRED (D3 satisfied transitively — NO new fold added).**
`QING_ministry_recompute_perf_revenue` (se_QING_MINISTRY.txt term d) already subtracts
`qing_currency_stress/6` from the Board of Revenue (戶部) minister's performance, which folds into his
Grand Council standing. So: opium net-drain → qing_currency_stress → qing_min_perf_revenue (d) →
qing_council_eff_target. The 戶部 is the historically correct office (it owned the 19thC silver-crisis
response, 銀荒/銀貴錢賤).

**BOTH ORACLE PROBES RETURNED NOT-PROVEN → both took the low-risk path:**
- **Cross-country trade-flow matrix does not exist** → opium-import intensity is a historical TIME RAMP
  (`qing_opium_import_index`, climbing toward a date-keyed ceiling: ~trickle 1763 → flood 1838; British
  Bengal country-trade grew external to the Qing frontier spheres), MODULATED by posture / commissioner
  / treaty / domestic-production. Export inflow uses the PROVEN, REAL country svalues
  `GOODS_national_production_{tea,silk,porcelain}`. (Rejected `britain_influence` as a proxy: that sphere
  ring is the Inner-Asian LAND frontier, geographically wrong for maritime Canton opium.)
- **Per-pop variables do not exist** → addiction is an AGGREGATE counter `qing_opium_addicted_share`
  (0..100) + country-modifier epidemic bands (proven corruption-band pattern), feeding qing_sect_pressure
  (White Lotus/Taiping among the ruined) + a productivity/unrest drag.

**FORMULA (calibrated Dermigny/Hsü):** net_flow = export_inflow (Σ tea+silk+porcelain ÷4, cap 40) −
opium_outflow (import_index÷2 + addicted_share÷3). Stress nudge = net_flow ÷5 × −1 (a +20 surplus →
−4 stress/quarter, a −20 drain → +4/quarter). 1763 zenith surplus bleeds stress DOWN; 1830s opium drain
drives it UP.

**POLICY LEVERS (L4 panel + events):** PROHIBIT (嚴禁) / TOLERATE-FOR-REVENUE (弛禁, +treasury +corruption)
posture toggle; APPOINT AN IMPERIAL COMMISSIONER (欽差大臣, Lin Zexu — suppresses the ramp, +legitimacy);
the Humen crackdown event DESTROY (−25 index, +8 legitimacy, GBR fury via QING_gp_react britain sev=20 +
grip-grace soft=1830 hard=1842) vs RELEASE (−5 legitimacy, +4 stress); treaty LEGALIZE (posture=2,
+40 treasury, −6 stress, epidemic worsens); UNLOCK DOMESTIC (以土抵洋, Yunnan/Sichuan — pulls import index
down, deepens epidemic).

**FILES:** NEW se_QING_OPIUM.txt (engine, 185/185 braces), qing_opium_events.txt (.1 memorial / .2 Humen /
.3 treaty legalization / .4 epidemic, 39/39), QING_opium_panel.txt (6 scripted-guis, 41/41), qing_opium.gui
(L4 clone, 74/74), qing_opium_modifiers.txt (2 epidemic bands, all tokens grep-proven), qing_opium_l_english.yml.
WIRING: QING_opium_init in qing_mechanics_on_actions.txt (after QING_xj_init); QING_opium_assess_trade_balance
in QING_DECLINE_pulse BEFORE update_currency_stress (so the trade nudge + reserve-ratio drift compound);
QING_opium_pulse after the concrete-object hangers; open button in government_view.gui (menu_trade.dds icon
— menu_economy.dds does not exist).

**KEY DECISIONS:**
- No se_DEMAND.txt edit needed — opium demand is modelled by the import-index ramp, not a trade-goods
  demand term (avoids re-touching the #279 crop-demand code that already carried unfixed bugs).
- Events .3/.4 exist in the events file but were NOT initially queued by the pulse; added two separate
  offer-blocks to QING_opium_pulse (treaty-legalize gated on qing_treaty_system_imposed; epidemic gated
  on addicted_share>=55) so no authored event is orphaned/dead.
- posture=2 (treaty-legalized) is IRREVERSIBLE by the panel (the treaty binds) — the PROHIBIT/TOLERATE
  buttons hide once legalized; every is_valid mirrors its effect guard (no dead clicks).
- All LOG msgs STATIC (#253). GUI text wraps (multiline + fixed width, #text-wrap rule). All modifier
  tokens grep-verified proven. QING_gp_react/QING_gp_grip_grace param names verified against se_QING_DIPLO.

---

## D77 — #368 Court Intrigue + Succession Deep Sim (宮闈鬥爭 / 立儲之爭) — BUILT + #366-R fix (commit c2eedf450)

**GOAL:** the concrete-over-abstract layer over the mod's EXISTING abstract succession. The mod already
models the succession *contest* (qing_succession.1 九子奪嫡 raises qing_succession_jockeying + a strife
modifier; qing_succession.2 resolves smooth-vs-disputed at accession off qing_secret_succession_sealed).
What it LACKED = the PRINCES themselves. #368 supplies a live roster of the reigning emperor's adult sons,
each with a court-backing score, and the teeth to seal the tablet on a SPECIFIC prince (秘密立儲).

**ENGINE (se_QING_PRINCES.txt, 132/132 braces):** QING_princes_init (idempotent), QING_princes_recompute_roster
(ordered_child over current_ruler's is_male/is_adult/is_alive sons → qing_princes variable_list on CHI +
qing_prince_count; each prince self-inits qing_prince_backing = combined_stats_council_svalue + 20, one-time),
QING_princes_compute_spread (top-minus-bottom backing = the factional-strife signal), QING_princes_pulse
(quarterly: rebuild, drift the front-runner's backing up +3 while unsealed & ≥2 princes → DIVERGENCE, couple
spread≥50 into qing_dynastic_harmony −1, offer events), + 4 levers.

**LEVERS:** 培植 FAVOUR (ablest by combined stats: +20 prestige, +12 backing, −2 harmony while unsealed),
秘密立儲 SEAL (nominated_heir_modifier + recalc_succession on the front-runner by backing + set
qing_secret_succession_sealed + strip prior nominee + +8 legit +1 stab +6 harmony + QING_seat_refresh_all),
查辦 INVESTIGATE (highest-backing prince: −15 prestige, −35 backing, −3 harmony; gated ≥70),
廢儲 REOPEN (strip nominee + recalc + clear seal + set jockeying + −10 legit −8 harmony; gated on sealed).

**FOLD (D3 satisfied transitively — no new fold):** the succession belongs to the EMPEROR, not an office, so
it nudges the shared qing_dynastic_harmony meter (QING_council_recompute additively converts harmony into
qing_council_eff_target — the SAME precedent as Harem #360 / Upper Study #337). A house at war over its
succession drags every Grand Council office; a sealed house lets them work.

**EVENTS (qing_princes_events.txt, 30/30):** .1 奪嫡之爭 THE PRINCES CONTEND (spread≥40, unsealed, ≥2 princes:
SEAL / GROOM / STAND ALOOF); .2 儲位太盛 AN OVER-MIGHTY PRINCE (a prince ≥85 backing: CURB 查辦 / ELEVATE seal /
WATCH). Both right_portrait = the saved front-runner/over-mighty prince.

**PANEL:** QING_princes_panel.txt (7 scripted-guis, 39/39) + gui/qing_princes.gui (104/104, menu_trade.dds icon
— menu_government.dds does not exist) — prince roster (dynamicgridbox, per-prince martial/finesse/charisma +
backing bar), harmony read-out, sealed banner, 4 lever buttons (each is_valid mirrors its effect guard — no dead
clicks). Open button in government_view.gui after the opium button.

**KEY DECISIONS / PROVEN-CODE:**
- NO create_character — princes are native family-graph children (born via the harem's make_pregnant #360),
  sidesteps the #90 boot-crash rule entirely. All primitives grep-verified proven in-repo (no oracle needed).
- ordered_child (NOT every_child) is the demonstrated effect iterator here (se_MARRIAGE.txt); every_child is
  only named in comments → switched the roster rebuild to ordered_child order_by=age.
- nominated_heir_modifier = a base-game vanilla triggered_character_modifier (used by anoint_heir_button.txt),
  carries support_for_character_as_heir=50 → makes the named prince primary_heir. Only ONE nominee at a time
  (strip prior before adding, mirrors the vanilla button).
- #368-R (prophylactic, same class as #366-R below): the once-only offered flags
  (qing_princes_contest_seen/_overmighty_seen) are set in the EVENT's own immediate, NOT the pulse — so a
  re-check failure during the trigger delay never strands them.

**#366-R (adversarial-review fix from wf_570e8e1f-9c8, MINOR — 1 confirmed):** QING_opium_pulse set the once-only
offered flags (qing_opium_warning_seen/_legalize_offered/_epidemic_offered) BEFORE trigger_event, so if the
event's own re-check trigger failed during the 5-20 day delay (e.g. the player switched posture), the flag stayed
set and the one-time event never re-offered. FIXED by moving each set_variable into the event's own immediate
(qing_opium.1/.3/.4 — fires only when the event actually fires). Same flag-leak class as the #367 khoja fix.

**#368 adversarial review:** launched wf_e71fa6e0-64e (running).

---

## D78 — #369 Population / Migration / Famine Deep Model (人口壓力 / 人地矛盾 / 饑荒) — BUILT (commit ca52862fc)

**GOAL:** the concrete-over-abstract standing driver over the mod's EXISTING one-shot demographic fragments.
The suite already modelled the story in pieces — the New World crop boom fires ONCE and forks ONCE
(qing_migration.20-.23), qing_granary_stock drifts as a famine reserve, and se_MIGRATION.txt is a full
bottom-up migration engine with migr_gov_push/pull government levers — but NOTHING continuously drove them
off the realm's crowding. #369 supplies that missing engine: a live qing_pop_pressure meter (0..100, 人口壓力)
that MOUNTS with the population boom + involution (內卷) and RELAXES with New World crops / frontier
resettlement / granary relief, continuously coupling the existing pieces. This is Hong Liangji 洪亮吉's 治平篇
(c.1793) thesis — "China's Malthus", five years before Malthus — made into a live meter.

**ENGINE (se_QING_POPULATION.txt, 91/91 braces):**
- QING_pop_recompute_target — target = total_population/12000 (floored), +18 involution (crops fired, not
  golden), +15 granary<30, −8 granary>=60, −12 frontier_resettlement flag, −10 golden crop; clamped 0..100.
- QING_pop_pulse (quarterly, from QING_GOV_pulse after QING_princes_pulse) — recompute target; EASE the meter
  1/4 toward it (hysteresis, matches the currency-stress design) via qing_pop_ease_tmp then remove it; couple
  into migration (>=60 → QING_COLON_heartland_push count=3; <35 → clear); couple into sects (>=70 → nudge
  qing_sect_pressure +2, the famine→rebellion linkage); offer .1 / .2.
- 3 levers: QING_pop_relief_resettle (賑濟移墾, treasury>=60), QING_pop_tax_remission (蠲免, treasury>=30),
  QING_pop_promote_resettlement (移民實邊, standing policy set-once). QING_pop_open_frontier_valve sets
  migr_gov_pull=12 on owned provinces in Turkestan/Yunnan/Guizhou/Sichuan_Kham/Gansu/Qinghai.

**FOLD (D3 — a REAL per-office drag, NOT the transitive harmony fold):** population pressure is a matter of
STATE ADMINISTRATION, so it folds into the Board of Revenue (戶部), historically the keeper of the 黃冊 census
and 常平倉 ever-normal granaries. Added ONE drag term (f) to QING_ministry_recompute_perf_revenue inside the
office-FILLED branch (qing_pop_pressure/8 subtracted from qing_min_perf_revenue) — the SAME shape as the
currency-stress (d) and corruption (e) drags. So a realm buckling under 人地矛盾 IS a Revenue-Minister failure
on the Grand Council.

**LAYER-DON'T-DUPLICATE:** qing_pop_pressure joins the EXISTING shared counter family (se_QING_DECLINE.txt:
corruption/sect/currency/granary) — same clamped-nudge idiom (QING_DECLINE_nudge, amount=var: proven), same
band-swap (QING_DECLINE_apply_pop_pressure_band: remove both, add current), same init (=20 if absent). Two
bands (qing_population_modifiers.txt): strain>=45, crisis>=75. No new meter machinery.

**EVENTS (qing_population_events.txt, 28/28):** .1 治平之憂 THE MEMORIAL ON POPULATION (pressure>=65: RELIEVE
賑濟移墾 / REMIT 蠲免 / RESETTLE 移民實邊 / LET-NATURE 聽其自然 which nudges reform_pressure+3 & re-offers);
.2 歲饑 FAMINE IN THE PROVINCES (pressure>=60 AND granary<=15: OPEN-GRANARIES 賑災 +add_legitimacy 4 /
WORK-RELIEF 以工代賑 / CANNOT-RESPOND which nudges sect+12 pressure+6 stability−2 & re-offers). Once-only
offered flags (qing_population_memorial_seen/_famine_seen) set in each event's OWN immediate, NOT the pulse —
the #366/#368 flag-leak fix.

**PANEL:** QING_population_panel.txt (6 scripted-guis, 31/31) + gui/qing_population.gui (67/67, menu_trade.dds
icon) — pressure / granary / sect read-outs, resettlement banner gated on qing_population_is_resettling, 3
lever buttons (each is_valid mirrors its effect's treasury/state guard — no dead clicks). Open button in
government_view.gui after the court-intrigue (#368) button.

**KEY DECISIONS / PROVEN-CODE:**
- ALL primitives grep-verified proven in-repo (no oracle needed): total_population at country scope, the
  clamped counter idiom (amount=var: reference), banded country modifiers, the migration levers
  (QING_COLON_heartland_push count param, migr_gov_pull/push read by MIGRATION_push/pull_province), all 6
  region keys (map_data/regions.txt), all 5 modifier tokens.
- FRONTIER VALVE routes to the historically-OPEN valves only — Xinjiang 屯田 (Turkestan), the southwest
  改土歸流 (Yunnan/Guizhou/Sichuan_Kham), Gansu/Qinghai — NOT Manchuria, which the 柳條邊 Willow Palisade kept
  legally closed to Han settlement until ~1860 (research-flagged).
- HYSTERESIS: the meter eases 1/4 toward a recomputed target rather than snapping, so a shock (bad harvest,
  crop-boom fork) doesn't jump the band — matches the currency-stress design.
- All LOG msgs STATIC. GUI text wraps. No create_character (no #90 risk — this is a pure counter model).

**#369 adversarial review:** launched wf_9371b193-50a (running).

**#368 adversarial review (wf_e71fa6e0-64e) result:** found the #368-R2 bare-order_by bug + #368-R3 per-reign
flag bug — BOTH already fixed (commits cefe2f99e, 6e713560f) before this session resumed.

## D79 — #370 Silk Road / Central Asian Caravan Trade-Node System (絲路商道 / 回疆貿易) — BUILT (commit 871322c4e)

**What:** the ECONOMIC twin of the #367 Xinjiang consolidation arc. Where #367 models the GRIP on the New
Dominion (garrisons, begs, tuntian, the 協餉 subsidy), #370 models the COMMERCE that ran alongside it: the
Kashgar–Yarkand caravan trade with the Central Asian khanates (tea/rhubarb/silk/silver west; horses/jade/
cotton/dried-fruit east), funnelled through the oasis entrepôts. The great historical crisis was commercial
— the Khanate of Kokand's escalating demands for the aqsaqal (阿奇木伯克) consul + its own customs, culminating
in the 1832 settlement (the first "unequal treaty" the Qing granted, a decade before Nanking; Kokand
weaponised the White-Mountain khoja pretenders when rebuffed).

**Layer-don't-duplicate:** owns ONE meter `qing_caravan_prosperity` (0..100, 商道繁榮) joining the shared
se_QING_DECLINE.txt counter family (QING_DECLINE_nudge clamped-nudge; band-swap `QING_DECLINE_apply_caravan_band`,
boom >=70 / depression <=25). Eases 1/4 toward a recomputed target (hysteresis, per #369/#367/currency).
COUPLES bidirectionally to #367 (does not duplicate): the target reads qing_xinjiang_control (grip /4, up to
+25) and qing_xj_khoja_pending (route-cut −15); prosperity nudges the grip back (>=70 → +1, <30 → −1). The
Kokand-concession lever reuses the SAME qing_xj_kokand_emboldened opinion + khoja-scare #367 owns
(separatism-backer rule satisfied — KOK is the neighbouring Turkic power).

**Grand-Council fold (the wiring rule):** term (d) inside `QING_ministry_recompute_perf_lifanyuan`
(se_QING_MINISTRY.txt) — additive-inside, deviation-from-50 /5 (~±10), alongside the #367 grip term (c)
which folds qing_xj_consolidation /3. Cloned term (c)'s template exactly. Verified the onward path: the term
writes qing_min_perf_lifanyuan (clamped 0..100 at recompute end), which se_QING_COUNCIL.txt's generic
qing_min_perf_$office$ loop folds (dev-from-50 /5) into qing_council_eff_target — so caravan prosperity
flows into the Lifan Yuan Director's Grand Council standing. c scores the GRIP, d the COMMERCE — complementary,
not double-counted.

**Levers (se_QING_CARAVAN.txt):** set_customs{0/1/2} (heavy sours KOK via add_opinion, unguarded-refresh);
invest_market (treasury −40, +8 prosperity, +1 XNG integration via SUBJ_QING_advance_integration steps=1 with
save_scope_as=target — the commercial mirror of the tuntian lever); grant_aqsaqal (set-once: +10 prosperity,
clear KOK emboldened + goodwill, defuse khoja, add_legitimacy −6 COUNTRY-scope, ruler add_prestige −15
CHAR-scope, + a permanent customs haircut the pulse applies by halving the take); revoke_aqsaqal (add_legitimacy
+3, re-arm KOK, grip −6); military_escort (treasury −30, +8 prosperity, +4 grip, defuse khoja).

**Revenue:** quarterly customs trickle = prosperity × rate-factor[light 1 / mod 2 / heavy 3] / 40, HALVED if
the aqsaqal is granted (Kokand skims third-party duties); add_treasury=var: guarded on >0 (so integer-floor to
0 no-ops cleanly, never a negative/zero add).

**Events (qing_caravan.1/.2):** .1 浩罕之求 the Kokand ultimatum (grant the 1832 settlement / refuse & garrison /
temporise) offered when prosperity >=55, aqsaqal not granted, KOK opinion value<0 (the PROVEN opinion value-test,
NOT the unavailable has_opinion); .2 商道斷絕 route cut (escort / negotiate / lapse) offered when a khoja scare is
pending. Once-only flags qing_caravan_ultimatum_seen / _routecut_seen set in each event's OWN immediate
(#366/#368 flag-leak fix); "temporise"/"lapse" clear their flag so the crisis can recur.

**Panel:** gui/qing_caravan.gui + QING_caravan_panel.txt (3 customs setters each valid-when-not-current-rate;
invest gated treasury>=40 & market<4; grant shown-when-not-granted / revoke shown-when-granted, mutually
exclusive; aqsaqal_active shown-indicator drives a banner) + government_view.gui open button after the #369
population button. menu_trade.dds icon (verified present). qing_caravan_modifiers.txt = boom/depression bands.
picture=trade_port (the undefined `trade` was swapped out). All LOG msgs STATIC. GUI text wraps. No
create_character (no #90 risk — pure counter/lever model). All files brace-balanced (+0).

**#370 adversarial review:** first run (wf_d3352c2a-a5c) result was lost when the tmp task dir
rolled over at the date change; re-run fresh as wf_9e226c8e-904 (running).

**#369 adversarial review (wf_9371b193-50a) — DONE, 2 real bugs found + fixed (commit 253f63f2):**
- **BLOCKER** — `QING_pop_recompute_target` scaled `total_population` by `/12000`. At country
  scope `total_population` is the COUNT of pop objects (~40k for CHI at 1763), so the crowding
  base pinned to ~4; the meter (seeded 20) eased DOWN to ~4 and NEVER crossed the strain(45) /
  crisis(75) / event(60/65) bands — the whole Malthusian dynamic was inert. **Fix:** divisor
  `/12000 → /1200` (base crowding ~34, a sane High-Qing baseline the +18 involution / +15
  thin-granary offsets push into the strain/crisis/event bands). se_QING_POPULATION.txt:62.
- **MAJOR** — `QING_pop_pulse`'s `pressure < 35` branch called `QING_COLON_clear_heartland_push`
  UNCONDITIONALLY, stripping `migr_gov_push` from every owned province each quarter and wiping
  the crop-boom events' (qing_migration.20/.23.b) own push within one quarter — silently
  defeating the boom's frontier out-migration. **Fix:** guarded the clear with
  `NOR = { has_country_modifier = qing_migr_crop_boom  has_country_modifier = qing_migr_overpopulation }`.
  se_QING_POPULATION.txt:129-144.
- A verifier also flagged one MINOR (same clear-strips-boom-push class) — subsumed by the MAJOR
  fix's NOR guard. One claim (integer-truncation on `divide = 4`) was correctly REFUTED: Imperator
  script vars are floating-point, so the 1/4 hysteresis ease is fractional as intended.

## D80 — #371 mod-wide raw-integer add_loyalty audit (DONE, commit ecc4b9b6)

**Thesis:** `add_loyalty` takes a NAMED loyalty modifier, never a raw integer — a raw-int call
silently no-ops (verified: 0 raw-int uses across 1,918 reference usages in Invictus + Terra
Indomita; self-documented at 00_imp19c_loyalty.txt:35). A prior sweep left 54 raw-int
`add_loyalty = <n>` sites across the Qing feature code, every one of which was doing NOTHING.

**Fix:** appended a graduated loyalty-delta ladder to common/loyalty/00_imp19c_loyalty.txt —
`loyalty_qing_delta_p1/p2/p3/p5/p10/p12/p15/p20` and `_n1…_n20` (18 rungs; each `value = <signed>`,
`yearly_decay 1` if |v|≤5 else 2, `min = v*2` on negatives) — and converted all 54 sites across 13
files (`add_loyalty = <int>` → `add_loyalty = loyalty_qing_delta_[pn]<abs>`). Now the loyalty
nudges these events/effects always intended actually land.

## D81 — #370 caravan review actioned (adversarial review; 1 CONFIRMED MAJOR, commit d07b8c0d)

**Review verdict:** the #370 adversarial review raised 3 claims; 1 confirmed MAJOR, 2 refuted.
- **CONFIRMED (MAJOR, flag-leak of the #366/#368 class):** `qing_caravan_routecut_seen` is set in
  `qing_caravan.2`'s immediate but was cleared ONLY on the 'lapse' option. The 'escort' and
  'negotiate' options resolved the route-cut crisis WITHOUT clearing it, so once the player
  resolved it non-destructively the first time, a FUTURE khoja scare (se_QING_XINJIANG re-raises
  `qing_xj_khoja_pending`) could never re-fire `.2` — the recurring crisis was permanently
  suppressed, and its prosperity drag stuck with no player recourse.
- **FIX (commit d07b8c0d):** both 'escort' and 'negotiate' now clear the flag on resolution
  (`if = { limit = { has_variable = qing_caravan_routecut_seen } remove_variable = ... }`),
  mirroring 'lapse'. The crisis can now recur whenever a fresh scare pends.
- **REFUTED:** (a) an `add_opinion` claimed to stack — refuted; `add_opinion` REFRESHES an existing
  (modifier,target) pair. (b) an "unbounded feedback loop" between prosperity and grip — refuted;
  both counters are `QING_DECLINE_nudge` clamped 0..100, so the coupling is bounded.

## D82 — #334 Deferred Tributary follow-ons (朝貢體系): wire the tributary/amban order into the Lifan Yuan leader (commit 4f551c14)

**Thesis (D3 completeness):** the tributary system (#322) and the Amban corps had NO fold into the
Grand Council — `qing_suzerain_prestige` (se_QING_VASSAL.txt) fed NO office at all, and the resident
Ambans' individual quality (`qing_char_affinity`) drove nothing central. Per the "wire every
bureaucracy into its leader" rule, the Lifan Yuan office-holder (理藩院尚書) is the natural leader
whose Grand Council standing the whole tributary order should determine.

**Built (per concrete-over-abstract):**
- **se_QING_MINISTRY.txt / `QING_ministry_recompute_perf_lifanyuan`:** a new
  `qing_lifan_amban_affinity_sum` accumulator (reset 0 each recompute) sums the REAL resident
  characters' `qing_char_affinity` over every autonomous-governorship subject with a live
  `qing_amban_here` (scope-saved + ROOT-scoped add, guarded on the var existing). Two new folds
  inside the office-FILLED branch:
  - **(e) AMBAN CORPS QUALITY:** average amban affinity (`sum / count`, guarded count>0 so
    no divide-by-zero), deviation from neutral 50, /5 (~+/-10). Complements existing term (b) which
    scores STAFFING count — (e) scores the quality of the concrete resident characters.
  - **(f) SUZERAIN PRESTIGE:** `qing_suzerain_prestige` deviation from 50, /5 (~+/-10) — the piece
    that made the tributary-order meter answer to a Grand Council seat for the first time.
- **gui/qing_lifanyuan.gui:** a suzerain-prestige progressbar, and a central "Tributary Order
  (朝貢體系)" dashboard — a dynamicgridbox over `qing_rites_tributaries` using the proven
  `new_country_flag { blockoverride "Size" {30 30} }` + `[Country.GetName]` idiom. Per-subject
  interactions stay in the Diplomatic View — this rosters the whole order in one place, no dup.
- **localization:** 5 keys (SUZERAIN_LABEL/_TT, TRIBUTE_TITLE/_NOTE/_EMPTY).

**Verified pre-commit:** braces balanced on all 3 files; 5 loc keys present; source vars confirmed
populated (`qing_char_affinity` base 50 at se_QING_AFFINITY.txt:47, `qing_suzerain_prestige` base 70
at se_QING_VASSAL.txt:43); scope-save + read within one effect block; div-by-zero guarded; perf
clamped 0..100. Adversarial review launched (wf_062c9da0-88d) — outcome to be actioned.

## D83 — #335 Deferred Grand Canal follow-ons (漕運): concrete building tallies drive canal + fold into Works leader (commit 7b870a35)

**Thesis (concrete-over-abstract + D3):** the Grand Canal condition/grain model (#323) drifted off
binary building presence and folded nothing into the Works office-holder. #335 makes it answer to
CONCRETE per-type building counts and folds canal health into the Works Minister's Grand Council
standing.

**Built:**
- **se_QING_MINISTRY.txt / `QING_ministry_recompute_perf_works`:** the owned-province sweep now
  resets + tallies `qing_dike_count` / `qing_depot_count` / `qing_granary_count` (added
  `has_building = qing_granary_building` to the OR limit). New fold **(d):** guarded
  `has_variable = qing_canal_condition`, `(condition - 60)/4` added to `qing_min_perf_works`.
- **se_QING_CANAL.txt / `QING_canal_update_condition`:** the canal target now scales off
  `qing_depot_count` (x8 cap 24) + `qing_dike_count` (x6 cap 18); filled Works office adds
  `+10 + (finesse - 7)`, vacant drags -12; minus corruption/4; drifts +/-3 toward target; all
  scratch vars removed on every path. `QING_canal_run_grain_balance` shaves `qing_grain_draw` by
  `min(qing_granary_count, 2)` — the granaries now buffer the reserve.
- **gui/qing_works_ministry.gui + loc:** canal-condition + grain-reserve progressbars + a
  dike/depot/granary tally readout.

**Verified pre-commit:** braces balanced; 7 works loc keys present. Adversarial review launched
(wf_18966771-a79) — outcome to be actioned.

## D84 — #335 canal review actioned (adversarial review wf_18966771; 1 CONFIRMED minor, commit 316a7fb4)

**Review verdict:** 4 findings raised, 1 confirmed (minor), 3 refuted.
- **CONFIRMED (minor, attribution mismatch):** adding `qing_granary_building` to the works sweep's
  `every_owned_province` OR-limit made granary-ONLY provinces join `qing_works_provinces`, so the Works
  panel's "Public Works of the Realm" roster listed ever-normal granaries (the decline-engine's building,
  deliberately kept OUT of `qing_works_building_count`) as Board-of-Works commissions — roster non-empty
  while the works count reads 0.
  - **FIX (commit 316a7fb4):** gated the `add_to_variable_list` on the province holding a genuine
    (non-granary) Works building. The granary still passes the outer OR-limit, so `qing_granary_count`
    is still tallied for the canal grain balance — only the panel roster is gated, not the loop entry.
    (The finding split 2-real / 1-refuted among the three verifiers — two argued the panel deliberately
    frames granaries as hydraulic works via the HYDRAULIC line; the fix is trivial + safe either way, so
    applied.)
- **REFUTED (MAJOR downgraded to non-issue):** the claim that `value = var:qing_office_works_holder.finesse`
  (se_QING_CANAL.txt:109) is an unproven dotted-read that reads 0/errors — refuted; the `var:X.attr` read
  in a `set_variable` value context is proven in the mod's trade code (se_DEMAND.txt:178
  `var:trade_center.var:local_price_*`, +4 more), and `.finesse` off a live char scope is proven in the
  sibling recompute. Behaviour is identical to the save_scope_as form; the minister's canal boost lands.
- **REFUTED (×2 minor):** two further framings of the same granary-roster observation — one arguing the
  inclusion is by-design (the panel's HYDRAULIC line counts granaries), one that the count!=roster-length
  invariant never existed. Both correct that it is non-load-breaking; fix applied anyway for clean
  attribution.

## D85 — #370-R2: caravan once-only flag-leaks (adversarial review wf_9e226c8e)
The #370 review confirmed 2 MAJOR flag-leaks (the #366/#368 class, siblings of #370-R):
- **qing_caravan.2 NEGOTIATE** granted the aqsaqal but never cleared `qing_caravan_routecut_seen`,
  so after a later revoke the route-cut crisis could never re-fire (road silently stays cut).
- **qing_caravan.1 GRANT** never cleared `qing_caravan_ultimatum_seen`, so grant-then-revoke left the
  Kokand ultimatum permanently suppressed despite the revoke re-provoking Kokand.
Both now clear their `_seen` flag on resolution (mirroring escort/lapse). **REFUSE deliberately KEEPS
`ultimatum_seen` set** — it sets the khoja scare and does not drop prosperity, so clearing it would
re-fire .1 next quarter and preempt the .2 route-cut the refusal is meant to provoke. Commit 5499fe3ca.

## D86 — Merge-plan audit: 2 gaps in DEVELOP_MERGE_PLAN_2.md (Layer A)
Answering "does the plan cover all mechanics added to the 1763 branch?", I audited the plan against the
FULL 6a31f077..fbd1c073 range (62 commits), not just the ee44b72a9-onward slice it enumerated:
- **GAP (real): #291 (1921f3b06) ROW specialty buildings** — `row_production_buildings.txt`,
  `se_ROW_BUILDINGS.txt`, `row_buildings_l_english.yml` are ABSENT on develop-mech-port and were NOT
  carried by batch 1 (which took only the Qing companion se_QING_BUILDINGS). Branch-agnostic [MECH].
  **Added to A-MECH.**
- **GAP (doc): #283/#302/#303** six-power 1763→1815 AI-catch-up arcs + dated-war scheduler + setup-events
  were only an "open decision". All START_DATE-offset [DATE] → firm **skip**; now named in A-DATE, §4.3
  RESOLVED. Commit ef0adf352.
All other absent-from-dmp files in the range = world-surgery (skip) or process/research docs (§4.2).

## D87 — merge-overnight 8-task batch (2026-07-12): major decisions + deferrals
The user-approved smallest-first batch on `merge-overnight` (all committed as freekumquats, each
independently code-reviewed pre-commit; boot-test-owed, NOT promoted to master). Commits f1bc120f7,
caf55db04, 3f6731fbe, 23fee8be6, e68354aa1, 2ccf6696e, edb703ee3, ee6cd56da.

### Decisions made
- **#392 amban game-start seed** — post historical 1763 residents (TIB 輔鼐 Funai / ILI 明瑞 Mingrui /
  ULS 成衮札布 Chenggünjab). DECISION: seed only the 3 DIRECT CHI frontier subjects (nested XNG-under-ILI,
  MGA-under-ULS are unreachable by every_subject → seeding them = invisible chars). Extracted a SHARED
  `QING_office`... no — `QING_amban_warrants_resident_trigger` (union: ruler mongolic/bodish OR
  is_subject_type=autonomous_governorship) so the Lifan Yuan panel roster == the auto-post-sweep gate
  (broadened to include the Manchu-ruled 將軍 governorates ILI/ULS the culture-only test missed).
- **#388 BT-11 tributary default** — there is NO literal vanilla "cannot afford tribute" event; the
  mod's realization is the affordability clamp in QING_subject_collect_tribute. DECISION: detect a
  MEANINGFUL shortfall (owed ≥5), route through the Lifan Yuan (suzerain-prestige ding + mark
  supervising amban ineffective), fire qing_tribute.5 PUNISH/FORGIVE. Defaulter PERSISTED as a CHI var
  (qing_trib5_defaulter) re-saved in the event immediate (BT-7 stale-scope idiom). BT-28 external slot.
- **#372 戶部銀庫 silver reserve** — concrete balance in 萬兩, seeded 6200 at 1763 (3100 at an 1815 start),
  climbs to the documented 8182 peak (乾隆42/1777) then drains. DECISION (review fix): base accumulation
  gates ONLY on the office being FILLED (not finesse≥6) so the peak milestone reliably fires — council
  autofill sorts by combined stats, so a low-finesse general can hold Revenue; +10 finesse bonus kept as
  reward. Distinct from the abstract qing_currency_stress meter. Figures → memory imp19c-silver-reserve-figures.
- **#384 NW-crop diffusion** — two-pass snapshot→adopt (sphere idiom), staple-safe (livestock/wood only,
  never grain), ≤3 adoptions/yr, gated on qing_newworld_crops=1. DECISION: adoption chance wrapped in a
  script_value (qing_nwcrop_flip_chance_svalue) — oracle-confirmed `chance = <svalue>` is proven,
  `chance = var:X` / `chance = scope:X.var:Y` is NOT. Always adopts sweet_potato (spec's "dominant adjacent
  crop" simplified, matching the existing accelerator).
- **#390 文治 cultural patronage** — NEW player-agency spine (qing_wenzhi_patronage meter + 4 launchable
  initiatives in the 內務府 panel: 造辦處 workshops / 如意館 painting / 四庫全書 / 南巡) on TOP of the
  pre-existing random qing_culture.* flavour events (reused, not rebuilt). Payoffs = legitimacy /
  ruler popularity / stability, NEVER add_prestige. Siku lever guarded by qing_wenzhi_siku_pending
  (cleared by all 3 qing_culture.5 options) to kill a free-patronage spam exploit.
- **#389 Canton System 粵海關** — DECISION (the historical hook): Canton customs are the EMPEROR'S money.
  Quarterly QING_canton_pulse splits the yield 70% to the privy purse (內帑, bypassing the 戶部) + 30%
  state quota (add_treasury); yield scales with Guangzhou (p:9298) port_building + Hoppo competence + the
  regime being open AND CHI holding Guangzhou. Hoppo = a Neiwufu-appointee marker (QING_canton_rotate_hoppo,
  the player's proactive squeeze lever) — NOT a Grand Council office. Did NOT rewrite the region-trade
  balance loop (reads the sim, doesn't mutate it). Cohong debt crisis qing_canton.1 at high squeeze.
- **#396 BT-50 GC exclusivity** — user picked MINIMAL exclusion guards (NOT a full engine-office
  migration). Shared QING_office_eligible_candidate trigger (excludes ruler/heir/governor/is_general/
  is_admiral/vanilla-monarchy-office-holder + existing GC-seat) applied at autofill + the row-click picker;
  prune_seat now also relieves a councillor who BECAME a commander/governor; qing_force_setup.1 (day-30
  OOB attach) runs a prune+autofill reconcile so the game-start overlap self-heals. Heir/ruler refs
  exists-guarded. Dead per-office appoint verbs left as harmless orphans.
- **#397 BT-60/61 borders** — user picked "leave stripped provinces UNOWNED". Full 1763 border AUDIT run
  first (see D88 below): world already largely correct. USA trimmed 236→172 Atlantic-seaboard provs (10
  subject tags MIC/ILL/MSI/MSP/IND + CHT/CHC/CHE/MSG/MIA emptied + their deps removed; 64 western + 21
  RUA Alaska provs → unowned). Freed tags left INERT via the proven QNG empty-core+capital pattern.

### DEFERRED / explicitly NOT done in this batch
- **#397 USA western provinces: a dedicated GBR "Crown Reserve" tag was REJECTED** in favour of leaving
  the trans-Appalachian interior UNOWNED (the user's pick) — the more-precise Crown-Reserve tag +
  province transfers was the deferred alternative.
- **Full world border rebase DEFERRED / closed as unneeded (#394)** — the audit found only USA + Alaska
  genuinely wrong; Poland-Lithuania-as-RUS-protectorate (18mo early, Poniatowski 1764) ACCEPTED as an
  already-documented defensible simplification, NOT changed. No country-by-country rebase warranted for a
  Qing-focused mod.
- **#393 quickrank trade wire-in — DEFERRED to the trade_fix branch** (not merge-overnight); still pending.
- **#391 BT-25→BT-46 boot-test findings — DEFERRED to 1763_bookmark** (still pending); this batch was
  the merge-overnight-scoped features + BT-11/50/60/61, not the 1763_bookmark bug list.
- **#389 Canton did NOT wire into the region-trade balance sim** — the task's "wire into se_TRADE_income"
  option was deferred as high-risk; the pulse reads the sim (port level) but routes its own yield, so the
  deeper trade-loop integration remains open if ever wanted.
- **BT-53 religion-panel empty body** — instrumented with a diagnostic sentinel on 1763_bookmark, awaiting
  the user's next boot-test read; NOT resolved.

## D88 — 1763 border audit verdict (2026-07-12): world largely correct
Full country-by-country audit (read-only agent) for #397/#394. FINDING: the #289/#296/#297/#298
territorial-accuracy batch MOSTLY SURVIVED on merge-overnight (the earlier "a later merge clobbered #289"
fear was WRONG): SPA→LSA + LSA's 14-province core intact (incl. New Orleans 3967), SFB New Granada
hierarchy intact, Crimea-under-Ottoman / Persia-Zand / Bengal-Nawab / Mexico-as-New-Spain / Florida-to-GBR
/ Haiti-French / New-France-ceded all correct. ONLY genuine anachronisms = USA-at-1815-extent (BT-60) +
Russian-Alaska (BT-61), both fixed under #397. Validation idiom for the setup edit: Python scan of every
own_control_core block for a province appearing in >1 owner = double-ownership = load error (confirmed 0).
Detail → memory imp19c-1763-border-audit-done.

## D89 — Deep-adversarial-review fix batch (23 confirmed findings, merge-overnight)

After the 72-agent adversarial review of the whole merge-overnight branch (verdict: "do NOT merge as-is"),
the user said "fix all bugs". All 23 confirmed findings fixed in one batch; 9 review false-positives were
correctly left alone (single-token $macro$ in LOG is fine; ordered_subject defaults descending; global
every_character heir-strip can't manifest; setup char-ID contiguity OK).

TIER 1 (block-merge):
- **A. Ministry corps picker dispatch** (QING_governance_actions.txt + 3 .gui). The 3 corps panels
  (Censorate 御史 / Imperial Guard 侍衛 / Zongli 駐外使臣) set only the GUI string var, never the SCRIPT var
  the shared row-click handler dispatches off → dead button OR stale-flag mis-appointment charging PI.
  Fix: 3 bridge GUIs (qing_gc_set_picker_office_{censor_inspector,imperial_guardsman,zongli_diplomat}) +
  corps branches in qing_gov_office_appoint_selected (NO PI, cap<6, stamp corps flag + recompute) +
  wired bridge Execute calls into the panel buttons. Office path kept byte-identical. New loc key
  qing_gov_corps_valid_tt.
- **B. Sphere illegal operator** (se_QING_SPHERE.txt). `var:X > local_var:top_val` engine-rejected —
  four-power Great Game silently dead. Ported the ALREADY-COMMITTED BT-64 fix (02ce33b78, which lived on
  another branch, NOT merge-overnight) verbatim: promote top_val to persistent qing_sphere_top_val,
  remove at end.
- **C. Tribute income read** (se_SUBJECT_QING.txt:657). `set_variable value = has_monthly_income` parsed
  as a nonexistent variable name → 0 + "Failed to fetch variable" flood, tribute-gold transfer dead. Fix:
  read via new script_value three_months_income_svalue (00_event_values.txt); dropped the now-redundant x3.

TIER 2:
- Liberate double-overlord (se_DIPLOMACY.txt:~1406): the flag:dynamic-released nation is already the
  releaser's subject; added release_subject-first before FUNC_make_subject (proven idiom from the
  subjugate-transfer path at 1085).
- Investiture dead else_if (qing_mechanics_on_actions.txt): on_character_death ROOT = dying char, so
  is_subject_type/overlord (country triggers) never fired; hop through `employer` like the first branch.
- Tribute .2/.3/.4 stale-scope: persisted qing_trib2_vassal/qing_trib3_restless/qing_trib4_meddled at
  dispatch sites + guard-on-var/re-save-in-immediate in the events, matching the BT-7 idiom .1/.5 use.
- Siku free-patronage farm (se_QING_WENZHI.txt): option-c decline cleared pending WITHOUT setting _done,
  so relaunch banked +15 patronage each cycle. Gated the +15 on a NEVER-cleared one-shot
  qing_wenzhi_siku_patronised; pending stays the dilemma-open guard.

TIER 3:
- add_prestige no-op sweep: converted 9 CHARACTER-scope add_prestige (POPULATION/CARAVAN/HAREM/MARRIAGE/
  UPPERSTUDY/PRINCES + tribute/caravan events) to add_popularity per BT-5/6. DELIBERATELY LEFT: the GP-arc
  events (aus/pru/gbr/fra/rus/spa) use COUNTRY-scope add_prestige (a valid country stat), and
  se_QING_AFFINITY's `family = { add_prestige }` is a deliberate family-honours grant.
- Zand double family_name+family (00_Persian Empire.txt:185, R2-18 anti-pattern): dropped family_name,
  kept the fam: object (matches his household 599/600/601).
- Cherokee province 89 trade_goods rifles→tobacco (stray industrial good on a 1763 tribesmen settlement).
- Sticky pending_play_goal (EE_scripted_guis.txt): cleared after a play begins so the next play doesn't
  inherit the stale goal.

DEFERRED / not fixed: nothing from the confirmed list. The recommended grep gate `grep -rn add_prestige
common/ events/` was run — only the intentional country-scope + family-scope sites remain. Independent
code-review agent run on the Tier-1-A picker rewrite BEFORE commit (STRICT PRE-COMMIT REVIEW rule).

## D90 — Qing feature-suite enhancement pass (merge-overnight, autonomous)

User directed a deep assessment of merge-overnight Qing features + autonomous implementation of
improvements. A general-purpose agent produced a ranked 15-item value/risk backlog; I implemented the
low-risk coupling + content items as reviewed additive changes. An independent code-review of the first
5 confirmed "all correct, ship it — no runaway, bounded loops". Implemented:

SYSTEM COUPLINGS (additive nudges via the clamped QING_DECLINE_nudge wrapper, quarterly pulse):
- **Opium addiction -> pop pressure** (#5, se_QING_OPIUM): addiction >=50 adds +1/qtr to
  qing_pop_pressure — the Malthusian multiplier beyond the silver drain. One-way (verified no feedback).
- **Silver reserve -> currency stress backfeed** (se_QING_REVENUE): a near-empty 戶部銀庫 (<1000萬兩,
  ~1799 level) adds +1/qtr to currency_stress, completing the bidirectional loop (stress already bled
  the reserve). Reviewer confirmed it converges to a BOUNDED, recoverable fiscal-collapse attractor,
  not a runaway — High-Qing accumulation (+25/35) overpowers it and switches it off above 1000.
- **Civic identity -> exam pass-rate** (#6, se_QING_EXAM): civic >=50 boosts the metropolitan pass-rate
  by (civic-50)/4 (0..12.5) — modern schools widening the talent pool. Was ignored by the formula.
- **Harem depth -> dynastic harmony** (#3, se_QING_HAREM pulse): consort_count >=4 => harmony +1;
  <=1 => -1 (succession security/anxiety). Stacks with the existing chamberlain-neglect term (max
  -2/qtr at count==1, intended + bounded).

CONTENT FILLS:
- **Boxer dual ignition** (#9, se_QING_DECLINE): the 義和團 trigger now fires on reform_pressure>=35
  AND (currency_stress>=40 OR qing_antichristian_sentiment>=50) — the historical dual cause (fiscal/
  foreign crisis OR anti-Christian fury). Formerly ignored the sentiment meter. Only BROADENS ignition;
  one-shot flag intact.
- **Green Standard decay asymmetry** (#12, se_QING_DECLINE): implemented the "rots slightly faster"
  the comment had long PROMISED but never coded — an extra +1/qtr once greenstandard_decay >=40, so
  the 綠營 collapse accelerates in the late decline (the 勇營->湘軍/淮軍 arc). Lockstep early (no
  premature warlord spike); divergence only bites once hollow.
- **Cultural zenith milestone event** (#13, NEW qing_wenzhi_events.txt + se_QING_WENZHI pulse +
  loc): patronage first >=80 fires a one-shot qing_wenzhi.1 capstone (endow-institutions vs
  personal-glory), mirroring the proven silver-peak qing_revenue.5. Court-slot + one-shot gated.

ASSESSMENT CORRECTION: the backlog's "surface hidden state" items (#1 silver reserve, #4 wenzhi, #11
opium net-flow) were found ALREADY displayed in their panels; #15 hollow-modernization is already an
outliner modifier (qing_selfstr_hollow, loc'd). So those were skipped as redundant — verify-before-build
paid off. DEFERRED (medium-risk / larger): #8 selfstr-velocity->civic drift rate, #10 harem->succession
event frequency, #2 exam-pool cross-panel display, #7 ethnic-tension province map, #14 accountability
trait grants. All additive; brace balance 0; BOM/CRLF preserved; se_LOG wired on the new event.

## D91 — Qing enhancement pass WAVE 2 (merge-overnight, autonomous)

Continued the deep-assessment enhancement pass with the deferred-but-viable wave-2 items.
Independent code-review confirmed both changes correct, bounded, and ready to ship (no defects).

- **Harem depth -> succession event frequency** (#10, se_QING_DECLINE ~1262): the succession-edict
  weight (the `8 =` random_list entry firing qing_char.20) now carries two weight modifiers keyed on
  the harem roster — `factor = 2` when qing_harem_consort_count >= 5 (a deep harem seethes with
  candidates), `factor = 0.5` when <= 1 (a thin line is a quiet matter). Multiplicative on the existing
  weight; the event's own age/health trigger + one-shot qing_secret_succession flag still gate the fire.
  `modifier = { factor N <trigger> }` verified as a proven in-file random_list idiom (lines 1362/1388/1843).

- **Sustained excellence -> a durable character mark** (#14, se_QING_ACCOUNTABILITY QING_acc_reward):
  transient standing (pop/prom) fades as the accountability pulse re-scores each quarter, so a minister
  who runs a THRIVING domain year after year now leaves a permanent stamp. Concrete-over-abstract: a
  per-character streak counter (qing_acc_streak, incremented each thriving verdict) and, on the 4th
  such verdict (~a full year of good government), a ONE-TIME grant of the `just` personality trait
  (賢能之臣). Guarded: fires once (qing_acc_lauded flag) and only if the man holds neither `just` nor
  its opposite `arbitrary` (never fights the trait system). add_trait=just on an employed char is a
  proven idiom (se_QING_STUDENTS, se_QING_JAPAN_PREPERRY). Vars are per-CHARACTER (inside
  scope:qing_acc_holder), no country-scope collision.

SKIPPED as redundant: #2 (exam scholar-pool cross-panel display) — the Hanlin Academy panel ALREADY
shows qing_hanlin_scholar_count PLUS a full scrolling scholar roster; that is the semantically correct
home for the exam-fed corps, so a duplicate count on the Rites panel would be clutter (verify-before-build).

STILL DEFERRED (needs prev-value state / medium-risk, not shipped unreviewed): #8 selfstr-velocity ->
civic drift-rate coupling (would need per-pulse delta tracking; reviewer flagged oscillation risk),
#7 ethnic-tension province map (large GUI effort). Brace balance 0 on both files; BOM/CRLF preserved.

## D92 — Qing enhancement pass WAVE 3 (merge-overnight, autonomous)

A fresh deep-assessment agent produced 6 new candidate couplings; verify-before-build pruned two
(assessment error: #1 "Council -> Exam ladder" is ALREADY wired — qing_council_effectiveness is
literally a 50% weight in QING_GOV_update_exam_ladder at se_QING_GOVERNANCE:162-163; #5 caravan ->
Xinjiang loyalty overlaps the existing caravan -> qing_xinjiang_control grip coupling AND would need
two new opinion_modifier defs, so deferred). Shipped the three clean high/med-value items; independent
code-review confirmed all correct, bounded, no defects.

- **Dynastic harmony <-> harem fertility** (#2, se_QING_HAREM QING_harem_pulse): the quarterly
  conception roll was a flat 20%; it now branches on qing_dynastic_harmony — 30% when the house is
  united (>= 60), 10% when split (<= 40), else 20%. Closes the loop with the wave-1 succession-security
  term (consort_count -> harmony): harmony now ALSO feeds back into how readily the line is got. Uses
  the proven `random = { chance = N  <effect> }` idiom in explicit branches (a `modifier` block inside
  `random` is used NOWHERE in the mod, so avoided).

- **Central-army collapse -> commander loyalty drift** (#3, se_QING_WAR QING_war_review_commanders):
  when BOTH central hosts rot (qing_banner_decay >= 60 AND qing_greenstandard_decay >= 60) each
  provincial commander takes an extra add_loyalty = loyalty_qing_estranged, in BOTH the War-office-filled
  and vacant iterators. Concretizes the abstract decay counters onto real on-map commanders (the
  湘軍/淮軍 regionalism seed). Bounded by the ladder's min=-35; compounds the existing friction/affinity
  drift; the warlord-event roll still gates the actual crisis.

- **Civic identity -> cultural-flowering frequency** (#4, se_QING_DECLINE culture roll weight ~1403):
  the `12 = { QING_culture_roll }` random_list entry gained two weight modifiers on qing_civic_identity —
  factor 1.5 in [50,85), factor 2 at >= 85, kept MUTUALLY EXCLUSIVE (upper-bound guard on the first) so
  they don't stack to 3x. Gives the wave-1 civic meter a visible qualitative payoff (more Kangxi
  Dictionary / Red Chamber / jubilee beats when the nation is united). Proven random_list modifier idiom.

Brace balance 0 on all three files; BOM/CRLF preserved. No new vars, events, GUI, or loc — pure
couplings between existing systems.

## D93 — Qing enhancement pass WAVE 4 (merge-overnight, autonomous)

A focused assessment of the tributary/canton/missionary/diplomacy/caravan subsystems (deliberately
steered AWAY from the heavily-mined decline-meter cluster) produced 5 candidates. Verify-before-build
pruned three: #2 tribute -> silver reserve (UNIT MISMATCH — qing_trib_amt is treasury gold, single
digits/qtr, while qing_silver_reserve is in 萬兩 ~6200-8182; adding raw would be ~inert/nonsensical),
#3 missionary friction -> integration (would need a NEW event = more risk than a pure coupling),
#5 legation -> techtransfer discount (low value, optimization-only). Shipped the two clean CONCRETE
on-map couplings; independent code-review confirmed both correct (directions/scopes right, matches the
proven amban/kokand opinion idioms), no defects.

- **Treaty burden -> tributary restiveness** (#4, se_QING_TREATIES QING_treaty_pulse): a heavy burden
  (qing_treaty_burden >= 65) is the court kowtowing to the barbarian powers; each sinosphere_tributary
  (Korea/Vietnam/Ryukyu) now takes a decaying qing_overlord_weakness_opinion (-6, yearly_decay 4)
  toward the overlord — the 1882 Korea / 1884 Sino-French strain, radiating the humiliation out to the
  朝貢 order. every_subject + add_opinion{target=ROOT} is the proven se_QING_AMBAN idiom.

- **Caravan health -> Kokand's disposition** (#1, se_QING_CARAVAN QING_caravan_pulse): a booming Yarkand
  trade (prosperity >= 70) warms c:KOK (qing_caravan_thriving_opinion +8) — a concrete diplomatic reward
  for investing in the oasis market; a collapsed route (< 30) chafes it (qing_caravan_disrupted_opinion
  -8), feeding the emboldened-grievance the Kokand ultimatum already runs on. Reuses the c:KOK on-map
  actor + add_opinion idiom ALREADY in this file (line 243). Previously the caravan meter only touched
  internal grip/prosperity/revenue — no subject/neighbour-facing consequence.

Three new opinion_modifier defs added to common/opinions/imp19c_opinions.txt (qing_overlord_weakness_
opinion, qing_caravan_thriving_opinion, qing_caravan_disrupted_opinion), matching the existing value +
yearly_decay format. Opinions refresh each pulse while the extreme holds, bounded by yearly_decay (same
assumption the existing amban/kokand code relies on). Brace balance 0 on all three files; BOM/CRLF kept.

## D94 — Cross-wave emergent-interaction audit + fixes (merge-overnight, autonomous)

After shipping four enhancement waves, ran a holistic audit for emergent problems that per-diff reviews
(each blind to the others) could miss — meters now written by 2+ new couplings in the same pulse,
feedback loops, stacked estrangement. The audit confirmed everything is numerically BOUNDED (all Qing
0..100 meters mutate through the QING_DECLINE_nudge [0,100] clamp; loyalty via the modifier's min=-35;
the harem fertility<->harmony loop does NOT close because make_pregnant produces an heir, never a new
consort, and the draft self-caps at 8). It surfaced ONE genuine regression I had introduced + one tidy-up:

- **FIX (real regression): harem harmony ratchet** (se_QING_HAREM ~255). My wave-1 `consort_count>=4 ->
  dynastic_harmony +1/qtr` term LACKED the `< 66` guard that the Upper Study schooling term
  (se_QING_UPPERSTUDY:234) was DELIBERATELY given in the #337 review-fix. Since qing_dynastic_harmony has
  NO restoring drift and count>=4 is the normal state (the draft fills to 6-8), the ungated +1/qtr was a
  one-way ratchet pinning harmony at 100 — permanently maxing the council harmony fold and neutering the
  -6/-12 dynasty-crisis nudges (the exact anti-pattern #337 documented). Added the matching
  `var:qing_dynastic_harmony < 66` guard to the positive leg; the negative leg stays ungated (a strain
  should always bite). Now schooling+harem both raise harmony only toward the "secure house" band, leaving
  crisis events their downward headroom.

- **TIDY-UP: redundant vacant-branch commander term** (se_QING_WAR). My wave-3 "both central armies
  rotting -> extra loyalty_qing_estranged" was added to BOTH the War-office-filled and vacant iterators.
  In the vacant branch the commander is ALREADY estranged unconditionally the line above, so the second
  identical modifier was redundant (floored by min=-35 regardless). Removed it from the vacant branch;
  kept it in the filled branch where it has real bite (compounds the friction/affinity scoring).

ACCEPTED AS-IS (bounded, intended): harmony worst-case -3/qtr (chamberlain -1 + thin-court -1 + Upper
Study -1, all requiring count==1 + vacant chamberlain + low schooling); currency_stress +2/qtr same-pulse
(reserve<1000 backfeed + vacant-office arm) — strongly asymmetric vs the -10/qtr stress->reserve drain,
self-corrects in the High Qing era; greenstandard_decay +2/qtr (base +1 + MO-ENH >=40 +1), single-file
clamped. Brace balance 0 on both edited files.
