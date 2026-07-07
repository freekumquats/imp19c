# Overnight Autonomous Build — Major Decisions Log

Started 2026-07-07. Author of all commits: **freekumquats** (repo-local identity, per standing rule).
This file records the major decisions taken while implementing the pending task queue
autonomously ("implement everything without stopping"). One line per non-obvious call,
with the *why*. Companion to SESSION_REPORT.md (which gets the per-feature detail).

## Scope & review base
- **Review base = `origin/fix-usa-roster-create-character` @ `5a79ddcd`** — the latest version
  confirmed to work (per user). Everything in `5a79ddcd..HEAD` is in-scope for the final
  adversarial review. This is exactly "back from the Grand Council rework" (b12e1219 is the
  first commit after 5a79ddcd).
- Already committed on top of the base this session: `b12e1219` (Grand Council rework:
  council-is-offices + accountability), `919eddfd` (amban→grand_secretary rename + Dynastic
  Health panel #110).

## Cross-cutting architectural decisions
1. **The coupling-family pattern.** Each of the great offices OWNS its natural charges, turning
   a static office modifier into a live character relationship. Uniform spine for #108/#113/#117/
   #118/#121/#122/#123/#124/#125/#126: (a) the office-holder's skill/loyalty gates outcomes+costs
   of the domain's events; (b) the domain's charges (residents/governors/commanders/etc.) join the
   character-affinity chart against the holder via `QING_char_affinity`/`QING_pair_friction`
   (se_QING_AFFINITY.txt) — agree→effective+loyal, clash→dysfunction/recall events; (c) a VACANT
   office = that domain drifts. Each coupling stays CONSISTENT with the accountability metric that
   already judges its office (se_QING_ACCOUNTABILITY.txt) and must NOT double-count.
   - Personnel 吏部 ↔ governors (#117) | War 兵部 ↔ army/navy commanders (#118) |
     Works 工部 ↔ dikes/canal/wall + buildings (#121) | Rites 禮部 ↔ ceremonies/tribute (#122) |
     Lifan Yuan 理藩院 ↔ ambans/residents (#113) | Zongli 總理衙門 ↔ embassies/Great Game (#108) |
     Censorate 都察院 ↔ impeachment/remonstrance (#123) | Revenue 戶部 ↔ salt/granaries/silver (#124) |
     Justice 刑部 ↔ autumn assizes/penal code (#125) | Grand Secretary 內務府 ↔ privy purse/eunuchs (#126).
2. **Permanent vs appointable seats.** Emperor 皇帝 + Crown Prince 皇太子 (#115) and Grand Regent /
   Empress Dowager (#116) are a DISTINCT seat class — non-appointable, non-vacatable, excluded from
   the 11-office accountability loop, the appoint targets, the challenger search, and the vacate verb.
   They coexist with the existing Emperor Emeritus 太上皇 seat (Napoleon arc).
3. **Secret succession (秘密立儲) is the RESOLUTION mechanic, not flavour (#119).** Sealing the
   tablet damps prince-jockeying friction and yields a smooth transition; refusing/leaking reignites
   it — re-enacting Yongzheng's historical fix for the 九子奪嫡.
4. **Empress Dowager leads the regency (#116).** The living `current_ruler.mother` is styled 皇太后
   and is the FIRST-priority regent candidate (the 垂簾聽政 default), above prince/grand-councillor
   archetypes; carries the sharpest cling-to-power (Cixi) risk. Matches Invictus's own mother-first
   regency pick (oracle-verified).
5. **Concrete over abstract** ([[imp19c-concrete-over-abstract-rule]]) throughout: operate on real
   characters, real posts, real provinces, real buildings + `add_building_level`, and reuse existing
   counters (qing_corruption_level, qing_currency_stress, unrest, legitimacy, GP-tension) rather than
   inventing new abstract meters.

## Engine-capability decisions (oracle-verified; per standing oracle rule)
- **var-holds-character-reference is SAFE** (#113): verified in Invictus/Terra-Indomita AND our own
  se_QING_NAPOLEON.txt:124 / se_QING_CUSTOMS.txt:159. Post a resident with create_character at CHI →
  `move_country` to subject → mark with a `duration=-1` role modifier GRANTED OUTSIDE the
  create_character block (the #90 boot-crash gotcha). Store the link on the OVERLORD keyed by subject
  tag. Teardown = `death`/`move_country` + `remove_variable` (NO `remove_character`/`banish` in
  Imperator). Guard every deref with `has_variable` + `is_alive`.
- **Regency/seat idioms (#115/#116):** child = `current_ruler = { is_adult = no }` (adulthood = AGE
  16). Incapacity = `has_trait = incapable` (only first-class marker; PARTIAL — pair with `age >= 70`
  proxy). Succession hook = `on_ruler_change` (+ monarchy variant). No on_coming_of_age/on_trait_removed
  → auto-clear via a HIDDEN MTTH triggered event (Invictus ip_monarchy.52 pattern). Heir =
  `primary_heir` scope + `has_primary_heir` gate (monarchy-only). Mother = `current_ruler.mother`
  scope (guard exists+is_alive; `is_female` confirms) — Invictus regency literally saves it as regent.
- **Map modes (#109/#120) — RESOLVED by oracle 2026-07-07 (ad983280c6f671ecc):** VERDICT = NO. True
  custom, selectable map modes with new `color_mode` values are NOT scriptable in Imperator 2.0.5 —
  map modes are engine-enumerated via `SelectMapModesView.GetMapModes` (gui/select_map_modes.gui:57)
  and the 32 `color_mode` values in gfx/map/map_modes/map_modes.txt are C++-hardcoded; there is no
  `common/map_modes/` registration dir. Neither Terra-Indomita nor Invictus adds a custom map mode
  (TI's "performance_mm" just reuses color_mode=political). **DECISION: build a scripted-GUI province
  query panel instead** — PROVEN via common/scripted_guis/sell_provinces.txt (iterate
  every_governorships → every_governorship_state, filter on script conditions, render a scrollable
  list with per-province tooltips). This is more data-rich than a colour overlay anyway (categorical
  crop types / tension breakdown + backing powers). #109 ethnic-tension report and #120 crop-distribution
  report SHARE this scaffolding. Optional visual aid = a temporary civ-value modifier pulse to dim/
  highlight provinces in an existing map mode, but the LIST is primary. No silent scope-cut — the
  panel replaces the map-mode ask and the limitation is logged here.

## Existing-state reuse decisions
- New World crops (#120) already modelled as trade goods (maize/sweet_potato/potato) with province
  vars `produces_*` (se_GOODS.txt) + spread effect `QING_COLON_spread_newworld_crops` (se_QING_COLON.txt).
  #120 is JUST a map mode reading that state — NO new diffusion mechanic.
- Revenue (#124) reuses common/buildings/qing_granary_buildings.txt (extend, don't duplicate) and the
  qing_currency_stress counter shown on the #110 Dynastic Health panel.
- Works (#121) defines NEW buildings in common/buildings/qing_works_buildings.txt matching the
  qing_governance_buildings.txt schema (河堤 / 漕運倉 / 長城).

## Byte & process conventions (enforced on every file)
- se_*.txt + events .txt: no-BOM, LF, final newline. loc .yml: BOM, LF, final newline. .gui: TAB indent.
- Every net-new effect wired to se_LOG (LOG_enter/exit/line, sys=QING) per standing rule.
- Every fix/feature: task-tagged in-code comment + se_LOG marker + SESSION_REPORT entry.
- Brace-balance + byte-convention check after each edit. Mandatory post-implementation review
  (the final adversarial workflow covers 5a79ddcd..HEAD).

## Per-feature decisions

### #110 Dynastic Health (finish + review) — DONE, committed 1c0e5365
- Code review found ONE real bug: QING_HEALTH_CURRENCY_TT cited a silver-drain threshold of 40; the
  real classifier bands at 30 (silver drain) / 60 (crisis). Fixed the tooltip to name both true
  breakpoints. Cosmetic GUI indent nit left as-is (whitespace-insensitive, review confirmed no impact;
  a re-tab of the block is riskier than the nit).

### #115 Emperor + Crown Prince permanent seats & #116 Grand Regent — DONE (trunk)
- NEW file `se_QING_SEATS.txt` holds the whole dynastic-seat class, DELIBERATELY separate from the
  appointable-office backend (se_QING_COUNCIL.txt) so the autofill sweep / accountability pulse /
  effectiveness recompute / appoint-vacate GUIs / challenger search stay UNTOUCHED. The seats reuse the
  same `qing_office_<key>_holder` var shape (emperor/crownprince/regent) purely so the GUI roster renders
  them with the existing card idiom — but they never enter any appointable loop.
- Emperor seat = mirror of current_ruler; Crown Prince = mirror of primary_heir (monarchy-gated,
  hidden when secret succession sealed); refreshed every quarter (QING_GOV_pulse) + on_ruler_change +
  game start.
- Regency (#116): QING_seat_evaluate_regency fires qing_regency.1 when warranted (child is_adult=no /
  incapable trait / age>=70 dotage proxy) and no regent sits; fires qing_regency.3 to DISSOLVE when no
  longer warranted (quarterly re-eval stands in for the missing on_coming_of_age hook — Invictus
  ip_monarchy.52 pattern). Regent PICK priority = Empress Dowager (current_ruler.mother, living) FIRST,
  then imperial prince (close relative), then ablest grand councillor. qing_regency.3 branch on outgoing
  regent's affinity models the Cixi cling-to-power danger (regency persists, does NOT clear).
- Seat modifiers added to qing_governance_modifiers.txt: qing_regency_active (country; legitimacy/PI drain +
  unrest — a regency is workable but never as sure as majority rule), qing_regent_authority (character;
  prominence/popularity/loyalty — the lightning-rod regent).
- GUI: new "The Throne (大統)" seat row (3 read-only cards, no appoint/vacate buttons) inserted above the
  Dynastic Health panel in government_view.gui. Braces balanced 1595/1595.

### #119 九子奪嫡 + 秘密立儲 (secret succession as resolution) — DONE (trunk)
- In the SAME qing_regency_events.txt (namespace qing_succession). qing_succession.1 (princes intrigue,
  offered by flavour roll when ≥2 adult imperial sons + no sealed succession) RESOLVES via option .a
  "Institute secret succession" — sets qing_secret_succession_sealed, clears jockeying, legitimacy
  dividend, hides the crown-prince seat (the Yongzheng 正大光明-tablet fix). Open designation (.b) or
  aloofness (.c) leave the qing_succession_faction_strife modifier biting.
- qing_succession.2 fires on_ruler_change: SEALED → smooth accession (legitimacy+12); UNSEALED amid
  jockeying → disputed accession (legitimacy-10 + strife modifier). Sealed flag consumed each reign.
- Dispatcher: added weight-7 qing_succession.1 entry to QING_frontier_flavour_roll (se_QING_DECLINE.txt),
  self-guarded on the trigger. on_ruler_change hook added to qing_mechanics_on_actions.txt (CHI, AI+player).

## Parallel content-agent wave — orchestration + splice-scrutiny decisions (2026-07-07)
Each office-coupling / content feature (#107,#108,#111/#112,#113,#114,#117,#118,#121,#122,#123,#124,
#125,#126,#109/#120) was built by a background agent AGAINST BUILD_BRIEF_OVERNIGHT.md, writing ONLY new
files (se_/event/modifier/loc/scripted_gui/.gui) and RETURNING splices. I (orchestrator) own the trunk +
all shared-file edits (the flavour-roll dispatcher se_QING_DECLINE.txt, the quarterly QING_GOV_pulse in
se_QING_GOVERNANCE.txt, on_actions, government/diplomatic .gui open-buttons) — spliced in ONE consolidated
pass to avoid write-collisions. Insertion points confirmed: dispatcher random_list = se_QING_DECLINE.txt
after line ~997 (inside the `chance = 30` random_list, weights kept 5–12); pulse calls appended in
QING_GOV_pulse before LOG_exit (line 433).

**Splice bugs found in returned payloads — to CORRECT at integration, not paste verbatim:**
- **#117 Personnel** triennial-guard splice put EFFECTS (`subtract_variable`/`check_variable`) INSIDE a
  `trigger = { }` block — invalid (a trigger evaluates conditions, cannot mutate). CORRECTION: drop the
  in-trigger mutation; gate the 大計 purely on a stored `qing_personnel_daji_last_year` compared with a
  read-only condition, and do the year-stamp in the EVENT's immediate/option, not the roll trigger.
  Also its `QING_personnel_evaluate_governors` pulse call must land in QING_GOV_pulse.
- **#118 War** references a `qing_military_strain` counter that does NOT exist in QING_DECLINE_init.
  CORRECTION: redirect that nudge to an existing counter (`qing_greenstandard_decay` — the closest fit
  for warlordism/regional-army strain) rather than adding an unseeded var. Also flagged: commander
  iteration uses an `every_character martial>=8 power_base>=1` proxy (no direct commander iterator in
  Imperator) — ACCEPTED as the loyal-cohorts proxy already used in se_QING_COUNCIL. Naval sub_unit
  `trireme` kept (matches se_QING_SELFSTR fleets). Pulse call `QING_war_review_commanders` → QING_GOV_pulse.
- **#122 Rites** dispatcher entries use `trigger = { always = yes }` on weights 8/6/6 — these would
  over-fire (every roll, no state gate) and spam. CORRECTION: gate .1/.3/.4 on `has_variable =
  qing_office_rites_holder` (parallel to the other office entries) so they only roll when the office is
  live; keep .2 gated on `any_subject`. Events self-re-check, but the dispatcher gate prevents dead rolls.
- **#123 Censorate** returned a `QING_censorate_pulse` (nudges corruption from the Censor's stats) PLUS
  four dispatcher entries. RISK: the pulse must NOT double-count the accountability metric (Censor already
  judged on qing_corruption_level). DECISION: keep the pulse (it MOVES corruption, accountability GRADES
  the office on it — distinct), but verify at review it only nudges, never re-grades. Dispatcher entries
  accepted (all properly gated on censor holder + corruption bands).
- **#124 Revenue / #126 Household / #123 / #108** all add quarterly pulse calls
  (`QING_revenue_pulse`, `QING_household_pulse`, `QING_censorate_pulse`, `QING_greatgame_pulse`). All land
  in QING_GOV_pulse before LOG_exit, EACH self-guarded/O(1). #126 adds ONE new counter `qing_privy_purse`
  (內帑, init 50) — justified (a private imperial treasury distinct from the state 戶部 treasury; no existing
  counter fits) — its `QING_household_init` goes in the on_game_initialized block.
- **#125 Justice** dispatcher entries gate on `is_ai = no` — ACCEPTED (justice ceremonies are a
  player-facing flavour layer; AI need not be prompted). Seasonal 秋審 gate on current_month 8–10 kept.
- **Map modes (#109/#120)** built as scripted-GUI province-query PANELS per the oracle verdict above (NO
  custom map mode). #107 OWNS the province var `qing_prov_ethnic_tension`; #109's panel READS it — name
  locked so the two agents agree. Open-buttons into shared .gui returned as splices, wired centrally.
- **#113 Amban — UNPROVEN idiom found & MUST FIX at integration.** se_QING_AMBAN.txt:76 stores residents
  via `set_variable = { name = "qing_amban_$subject$.GetTag" … }` — constructing a variable NAME from a
  dynamic tag interpolation. Grep confirms NOTHING else in the repo does this (the `$nick$` cases are
  `add_nickname` on a value, a different mechanism); it is NOT a proven Imperator capability and may
  silently no-op or fail. CORRECTION: rewrite the amban storage to the PROVEN `variable_list` idiom
  (add_to_variable_list / every_in_list / remove_list_variable — used in se_QING_COUNCIL.txt) holding
  resident CHARACTER references on CHI, and iterate with every_in_list in QING_amban_evaluate/recall.
  The resident character already carries the `qing_amban_resident` duration=-1 modifier (applied outside
  create_character per #90), so the subject link can also be read from the character's location. Agent
  self-flagged this as its open question #2 — resolved DECISION: variable_list, not tag-interpolated names.
  Also: #113 posting is event-driven; the optional init-seeding of residents to Tibet/Mongol subjects is
  DEFERRED (guard on subjects actually existing at 1815; not wired this pass to avoid a bad deref).
- **#109/#120 province-query panels — GUI-idiom scrutiny (lowest-confidence deliverable of the batch).**
  Agent flagged 3 open GUI questions; dispositions:
  (1) window-open via `gui.CreateWidget` — RESOLVED: mechanism proven (console.gui:214, wars_overview.gui:12,
      imp19c_windows.gui:1) BUT the agent's splice used the WRONG syntax `gui.CreateWidget <window>` (missing
      file path). CORRECT form is `gui.createwidget gui/qing_province_reports.gui <window>` — FIX the two
      onclick lines in the open-button splice before wiring.
  (2) province-scope `Var('qing_prov_ethnic_tension')` read inside a GUI datamodel item — UNVERIFIED (not
      exercised by sell_provinces, which only reads list membership). RISK: a bad datamodel deref.
  (3) `trade_goods = maize` province filter inside a scripted_gui limit — UNVERIFIED in a scripted_gui context.
  DECISION: the panels are net-new auto-loaded files (zero risk while UNREFERENCED). The ONLY shared-file
  touch is the government_view.gui open-button. To honour the "don't ship unproven capability that can crash"
  rule while still delivering: wire the open-button ONLY after (2)+(3) are confirmed by the adversarial review
  or a quick oracle; if unconfirmed at commit time, COMMIT THE PANEL FILES (dormant, no open-button) and leave
  the button splice as a documented TODO in SESSION_REPORT rather than risk a GUI hard-crash. The fix to (1)
  is applied regardless.
- **#114 Pilgrimage — dispatcher trigger fix.** Culture keys VERIFIED (mongolian/oirat/buryat/dagur all real
  in common/cultures/00_mongolic.txt; group = mongolic). BUT the any_subject branch uses
  `dominant_province_culture_group = mongolic`, and only `dominant_province_culture` (not the _group form)
  is proven in-repo (governor_policies/00_default.txt, on_action). CORRECTION: at integration, replace that
  branch with a proven check — subject's ruler `culture_group = mongolic` — or keep the well-proven
  any_character mongol-culture gate as the sole trigger (a Mongol courtier is the pilgrim anyway).
- **#118 War — counter redirect VERIFIED.** `qing_greenstandard_decay` IS seeded in QING_DECLINE_init
  (se_QING_DECLINE.txt:53, init value 15), so redirecting the phantom `qing_military_strain` nudge onto it
  is safe and semantically apt (Green Standard/regional-army warlordism).
- **#111/#112 Integration capstone — timing DECISION = SOLUTION A.** VERIFIED the capstone binds to the REAL
  existing meter `SUBJ_integration_progress` (se_SUBJECT_QING.txt), not a fork — good. Agent flagged that
  `SUBJ_QING_advance_integration` auto-absorbs at progress>=5, which would pre-empt the qing_integ.30
  capstone CHOICE. DECISION: SOLUTION A — at integration, edit the shared se_SUBJECT_QING.txt so that on
  reaching the threshold it fires qing_integ.30 (the manner-of-改土歸流 choice: solemn/bureaucratic/coercive)
  INSTEAD of silently calling SUBJ_QING_absorb_subject; each capstone option then calls absorb itself. This
  makes the capstone the absorption MOMENT (concrete, player-chosen manner) rather than a hollow
  post-hoc ceremony (Solution B). Decree (.40) hook = pulse splice in 00_monthly_country.txt after
  SUBJ_QING_integration_pulse; resistance (.41) fired by .40 (no separate hook). All player-only (is_ai=no),
  matching the existing integration subsystem.
- **#107 Ethnic tension — TWO fixes required at integration.** (1) The agent's `QING_ethnic_tension_init`
  effect was NEVER written into se_QING_ETHNIC_TENSION.txt (only the pulse is in the file); it was
  returned as splice-text prose. I must AUTHOR it. (2) Its frontier-seed region names are WRONG: it used
  invented lowercase keys `tarim_region / dzungaria_region / tibet_region / inner_mongolia_region /
  outer_mongolia_region`, but the real region keys in map_data/regions.txt are CAPITALIZED and different:
  `Turkestan` (Xinjiang), `Tibet`, `Mongolia`, `Qinghai`, `Sichuan_Kham`, `Gansu`. CORRECTION: author
  QING_ethnic_tension_init using the REAL keys (Turkestan=20, Tibet=15, Mongolia=10, Qinghai/Sichuan_Kham=10)
  and verify province-scope `region = <Key>` is the right trigger form (regions are groups-of-areas here;
  if `region =` doesn't match on province scope, fall back to iterating and gating on culture instead).
  Province var name `qing_prov_ethnic_tension` CONFIRMED matching #109's panel read. Pulse hook =
  qing_mechanics_pulse_on_action in 00_monthly_country.txt; province-scope idioms (every_owned_province,
  set_variable on province, dominant_province_culture, province_unrest, every_neighbor_province) all
  VERIFIED by the agent against in-repo occurrences.
- **#108 Great Game — pulse+events clean, GUI button HELD (same class as #109/#120).** Pulse splice
  (QING_greatgame_pulse after QING_accountability_pulse in QING_GOV_pulse) and the 3 flavour-roll event
  entries are well-gated (Zongli holder + GP-tension thresholds; reuse qing_gp_tension_* seeded by
  QING_gp_init) — INTEGRATE. But the diplomatic-view open-button relies on UNVERIFIED `ToggleGameViewWindow`
  + `GetCountryByTag` GUI datafunctions (agent's open Qs #1/#2). SAME DECISION as #109/#120: commit the
  panel + scripted_gui + .gui files (dormant, harmless unreferenced) and the pulse/events LIVE; HOLD the
  diplomatic-view button splice until the GUI idioms are confirmed, else a blank-window/crash risk. Note:
  #108 event splice uses `calc_true_if` — verify that's a valid trigger in this engine version at review.
