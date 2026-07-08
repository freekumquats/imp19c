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

### #139 Economy perf pass (trade / industry / production) — DONE, adversarially reviewed
Base task: 7 candidate perf fixes (A–G) surfaced by the economy audits ([[imp19c-economy-audit-backlog]]).
Overriding mandate: "extreme caution, functionality must not break" → every fix behaviour-PRESERVING
(cache-once hoist of an invariant, never a semantic change), then a deep adversarial review.
- **Implemented 4 (B/C/E/F), all byte-behaviour-identical:**
  - **B** (se_CONSUME.txt) — cache-once the deflation + elasticity factors that were recomputed per
    good inside the consume loop; both are good-invariant within the pass.
  - **C** (se_DEMAND.txt) — cache-once wealth-per-capita in the luxury-demand path (province-invariant
    across the goods it was recomputed for).
  - **E** (se_GLOBALTRADE_split.txt) — hoisted 7 category-invariant recomputes out of the per-category
    loop. THIS is the one that bit back (see review).
  - **F** (se_COTTAGEIND.txt) — cache-once cottage-industry raw-goods GROSS production; reads a NEW
    dedicated gross var, NOT the mutable/consumed `var:X_stockpile` (see rejection of the naive
    migration in the backlog note — substituting stockpile for gross output is a correctness regression).
- **REJECTED 2 as unsafe (A, D):**
  - **A** (fuse the dual currency-province sweep) — the two sweeps are NOT equivalent passes; fusing
    them would reorder currency mutation vs read. Not worth the correctness risk for the saving.
  - **D** (finish the half-done food/wealth cache migration) — same trap as the backlog's #76 analysis:
    the "cached alternative" reads a consumed inventory var, not gross production. Left the migration
    half-done ON PURPOSE (the earlier revert was deliberate).
- **SKIPPED G** (TZ-score matrix + numeric dispatch) — highest-risk, a structural rewrite not a hoist;
  out of scope for a "don't break anything" pass. Dead-code path anyway.
- **Adversarial review (6-agent Workflow) — cleared B/C/F + integrity; found ONE real regression in E.**
  DECISION on the E regression: relocating `PRICE_set_food_mean_normalised_price` out of
  `GT_split_do_global_trade_split` overlooked GT_split's SECOND caller — the game-SETUP path
  (oa_economy_setup.txt) runs the 7 splits synchronously at day 0 and had relied on the removed block to
  seed `PRICE_food_mean_normalised` before the first quarterly pulse (~day 20). In that gap a land
  transfer would read the unset var and diverge. FIX = re-seed the food mean in the setup path right
  after the food split (byte-identical to the original setup end-state; passes 2–7 never touch food
  prices). This validated the "extreme-caution + adversarial-review" mandate — the one escape was a
  hoist's other-callers blind spot, not a caching error.
- Net rule reaffirmed: a perf "fix" that MOVES a statement must enumerate ALL callers of both the source
  and destination scope. Caching an invariant in place is safe; relocating across a shared helper is not.

### #147 Player-initiated diplomatic plays via GUI — DONE, adversarially reviewed
Request: let the player START plays for many reasons via GUI (none existed — the only entry point was one
toggle that always fired get_territory) + a full plays-management window. User picked ALL goals and the
full-window scope.
- **GUI-shape DECISION: 6 thin per-goal scripted GUIs, NOT one popup with datacontext plumbing.** Each
  `DIPLO_begin_play_<goal>` clones the PROVEN `DIPLO_begin_or_end_play` two-scope shape
  (`GuiScope.SetRoot(province).AddScope('player', Player)`) and reads the SAME `scope:player.var:selected_province`
  the existing button already relies on — zero new plumbing, each button independently verifiable. A single
  popup with per-goal datacontext branching was rejected as fragile/unverifiable.
- **Backend DECISION: reuse proven wrappers, clone the proven resolver.** The 4 new resolvers
  (annex/purchase/liberate/colonise) are state-scoped clones of the known-good `DIPLOMACY_resolve_get_territory`,
  reusing `LAND_transfer_provinces` / `LAND_release_from_list` / `FUNC_make_subject` (all oracle-verified in
  #148 BEFORE building, per the standing oracle rule) — never raw `set_owned_by` (which would skip the
  governorship wealth/stockpile economy layer). Decisive/partial split mirrors get_territory throughout.
- **Purchase-state = consensual land, NO opinion penalty** (the whole point vs annex): buyer PAYS the seller
  a treasury sum scaled to ceded-land `DIPLOMACY_province_wealth_value`, capped at the buyer's treasury so it
  can never drive the buyer negative. `play_purchase_price` lives on the play PROVOBJ and is read back as
  `scope:diplomatic_play.var:play_purchase_price` inside the country-scoped payment blocks (a bare `var:` would
  resolve against the wrong scope — self-caught during build).
- **Liberate: decisive = fully independent nation; partial = your client_state** (release flag:dynamic then
  re-bind via FUNC_make_subject — the flag:dynamic-binds-to-releaser quirk compensated). Releaser = the owner
  being liberated FROM, matching the send_settlers precedent.
- **Colonise works on frontier AND sparse foreign land**; normalises play_target_country = instigator so the
  engine's c:BAR unclaimed-land fallback fires.
- **Support action wired** (both previously-dead list-template buttons) → `DIPLO_player_support_play`, 10 PI for
  `DIPLOMACY_modify_play_success += 10`.
- **Post-implementation adversarial review (code-review agent) — risky treasury/scope code CLEARED; 4 gating
  edges found & ALL fixed:**
  1. Support self-harm (MEDIUM) — button shows on every play, and backing always raises the INSTIGATOR's
     success, so a player could pay to boost a play AGAINST themselves. FIX: bar `var:play_target_country =
     scope:player` (a third party helping an ally stays legal) + skip a play already at 100.
  2. Purchase partial free-acquisition (LOW) — pricing play_target_area up front floored the price to 0 when
     that province was no longer cedable, yet a real province still transferred. FIX: select the transferred
     province FIRST, then price the province actually ceded.
  3. PI gate vs cost mismatch (LOW) — buttons gated `political_influence > 0` but the play costs 30 PI. FIX:
     gate raised to `>= 30` on all 6; tooltips corrected.
  4. Colonise third-party seizure (LOW) — foreign land taken with no grievance. FIX: `bitter_over_occupation`
     applied once per distinct displaced owner (`every_country`) before the release, matching the annex path.
- All new effects se_LOG-wired; 13 touched files brace-balanced + byte-conventions preserved; SESSION_REPORT
  #147 + #139 sections written. Not yet committed (awaiting user go / freekumquats identity).

## Scan-and-implement pass: unfinished / shallow features (2026-07-07)
User directive: "deep scan on what features are currently unfinished or lacking depth, make a list,
then start implementing with extreme caution to ensure nothing breaks" + "add all major decisions
to OVERNIGHT_DECISIONS".
- **METHOD DECISION: 3 parallel recon agents before any edit** — (1) code-level incompleteness markers
  (TODO/FIXME, dead GUI, uncalled effects, loc placeholders); (2) decision-doc mining of
  SESSION_REPORT + OVERNIGHT_DECISIONS + BUILD_BRIEF for everything explicitly DEFERRED/HELD/dormant;
  (3) depth assessment of the major subsystems (shallow-but-working mechanics). Synthesize into ONE
  prioritized list, present to user, THEN implement highest value/lowest risk first. Rationale: the
  "extreme caution / nothing breaks" mandate + the standing post-implementation-review rule mean the
  scope must be enumerated and triaged before touching code, not discovered mid-edit.
- Ordering principle for the list: dormant player-facing GUI the player literally cannot open ranks
  highest (a shipped-but-unreachable feature); internal accepted-staleness ranks lowest.
- Each implemented item will follow the standing rules: oracle-verify any unproven idiom FIRST,
  task-tag + se_LOG + SESSION_REPORT entry, brace/byte-convention check, post-implementation review,
  and a decision line appended here.

### Consolidated scan result + triage (2026-07-07)
Three recon agents (code-markers / decision-doc mining / depth assessment) returned. Triaged by
value/risk under the "nothing breaks" mandate:
- **Tier A (implement first — additive, cannot affect running sim):** (1) empty social-law modifier
  bodies womens_law/healthcare_law/religious_law (00_social_laws.txt) — selectable laws that confer
  nothing; (2) loc placeholders (11 PLACEHOLDER govt descs, 12 TBD mil-tradition strings, "9/10"
  score, MONARCH_HOW_PRES2 "Hello").
- **Tier B (needs oracle verification first):** held dormant GUI panels #108 Great Game + #109/#120
  province reports (unverified ToggleGameViewWindow/GetCountryByTag/createwidget + datamodel Var reads);
  balance_history hidden panel (economy_view.gui:1463).
- **Tier C (depth, additive, larger):** diplomatic-play join/oppose + AI-play crises + cancellation;
  subject agency (rebellion/drift/requests); Grand Council mid-tenure events; economy emergency levers.
- **Tier D — DELIBERATELY NOT TOUCHED (touching them risks breakage, violating the mandate):**
  monthly_administration_pulse / monthly_job_pulse (commented out BECAUSE they caused "unacceptable
  monthly slowdowns" — reviving = perf regression); migration/pop-policy verbs (deep pop-engine tie-in,
  balance risk); common/WIP/ (deliberately unloaded parked content); owed Qing correctness audit
  (a review effort, not a build).
- **GUARDRAIL for Tier A laws:** every modifier key must be validated against existing in-repo usage
  before insertion — an invalid country/character modifier key hard-throws at boot. No key goes in
  unverified.

### Tier A implemented (2026-07-07) — additive completions, zero running-sim risk
- **Empty social laws filled (common/laws/00_social_laws.txt).** womens_law (4 tiers) and healthcare_law
  (4 tiers) were selectable laws with EMPTY `modifier = { }` bodies (conferred nothing). Filled with a
  graded progression using ONLY modifier keys already proven to load in-repo (global_*_strata_happyness/
  output — note the codebase's `happyness` spelling — global_population_growth, manpower_recovery_speed,
  research_points_modifier, happiness_for_same_culture_modifier). Magnitudes kept inside the ranges the
  neighbouring cultural_protections_law / university_law already use.
  - KEY DECISION on healthcare "admin demand": the original comments said each tier raises "national/
    local administration demand", but admin demand is an SVALUE system (ADMIN_svalues.txt, a repurposed
    modifier hook), NOT a plain law modifier. Per the no-hot-path guardrail I did NOT wire into it —
    modelled the cost instead as upper-strata discontent + the growth/manpower benefit, which is
    behaviour-equivalent to the design intent without touching a shared quarterly svalue.
  - Dropped the stale `# WiP` tag on religious_law (it was already fully populated — false positive).
  - Wrote real player-facing loc descriptions for all 9 law options (were "...desc" placeholders) in
    laws_l_english.yml; renamed womens_law title "Womens law" → "Women's Rights".
- **Loc placeholders filled:** 10 government descriptions ("PLACEHOLDER" → real flavour text) in
  mod_governments_l_english.yml; 12 military-tradition titles ("TBD" → names matching each tradition's
  actual modifier/path theme) in military_traditions_l_english.yml. These are display-only strings
  (titles/descriptions), zero mechanical effect.
- **LEFT deliberately:** province_current_score "9/10" + MONARCH_HOW_PRES2 "Hello" — the former belongs
  to the dead province-colonization MOCKUP panel (a Tier C concern, not worth dressing a non-functional
  panel); the latter is referenced NOWHERE (harmless dead loc). japanese_imperial_ambitions_path_3 loc
  is orphaned (no tradition block uses it) — named anyway for tidiness, harmless.
- **Two PRE-EXISTING loc parse bugs fixed opportunistically** (genuine defects, render blank in-game):
  emigration_commerce_only `""Commerce Only"` (3 quotes) in laws_l_english.yml; and an UNTERMINATED
  string `secretary_r_interior_british_group:0 "$home_secretary$` (missing closing quote) in
  mod_governments_l_english.yml.
- Integrity: 00_social_laws.txt braces 84/84 (BOM+CRLF); all 3 loc files 0 bad-quote lines, BOM intact.

### Tier B — balance_history panel: LEFT HIDDEN (decision, 2026-07-07)
economy_view.gui:1461 `balance_history` flowcontainer is `visible = no # WiP`. Investigated whether it
could simply be un-hidden. VERDICT: NO — it has no real backing data. The panel is two progressbars with
hardcoded `value = "100"`, an in-code comment that the Y-position "needs to be dynamic", a name implying
8 quarters but only ONE bar-pair, and its only backing svalue `INCOME_negative_8q_ago` (INCOME_svalues.txt:
1102) is itself a stub returning a literal `value = 50` — there is NO positive counterpart, no other-quarter
svalues, and no quarterly income-history RECORDER anywhere in the sim. Un-hiding it would display fake static
bars. Finishing it properly = build an 8-quarter rolling income-history variable set (new quarterly recorder
on the economy pulse) + dynamic progressbar binding — a real feature, not a hidden-flag flip. DEFERRED as a
genuine build, not shipped fake. Kept hidden.

### Tier B — dormant player-facing panels WIRED (decision, 2026-07-07)
Three fully-built but unreachable panels (#108 Great Game dashboard, #120 New World crop report,
#109 province ethnic-tension report) were shipped in prior sessions with NO open-button — the player
could not open them. Added open-buttons in the Grand Council action strip (government_view.gui, CHI-only
tab), reusing the proven `icon_button_square` + `GetScriptedGui` idiom already used by the war-council /
court-a-power buttons in that same strip.

- **OPEN IDIOM (verified in-repo + both oracles):** `[ExecuteConsoleCommand('gui.createwidget gui/<file> <window>')]`
  is the proven way to open a custom window (settings_window, debug_menus in-repo; sell_provinces, ages_window
  in Terra-Indomita/Invictus). Window name arg must match the top-level `name =` in the .gui — verified all three.
- **REPORT BUTTONS chain TWO onclick lines:** first `ScriptedGui.Execute` (runs every_governorships to populate
  the variable-list), THEN createwidget (opens the window whose datamodel reads that list). Multiple onclick
  lines in one blockoverride run top-to-bottom (proven diplomatic_view.gui:59-62), so the list is populated
  before the window reads it. The Great Game panel is stateless/read-only so its button just createwidgets.
- **ORACLE VERDICT caught a latent CRASH:** the Great Game panel used `GetCountryByTag('GBR')` — NOT a valid
  engine datafunction (zero occurrences in either oracle mod). The correct form is `GetCountry('GBR')` (proven
  new_element_test.gui:18, Terra-Indomita chinese_unification.gui:44). Fixed all 6 sites. The panel would have
  hard-crashed on open. Also `GetOpinionOf(Player)` -> `GetOpinionOf(Player.GetCountry)` (3 sites) to match the
  reference-proven resolved-country argument form.
- **FIXED a dead close button:** the Great Game panel's close called `qing_greatgame_close_panel.Execute`, a
  scripted_gui with an EMPTY effect — clicking it did nothing. Replaced with `GUI.ClearWidgets qing_greatgame_panel`
  (proven imp19c_windows.gui:20). The two report windows already used the correct ClearWidgets close idiom.
- **Backing data all confirmed present** before wiring: qing_prov_ethnic_tension set by se_QING_ETHNIC_TENSION.txt;
  qing_gp_tension_* set by se_QING_GREATGAME.txt et al; qing_office_zongli_holder set by se_QING_COUNCIL/ROSTER;
  maize/sweet_potato/potato all defined in common/trade_goods/00_imp19c.txt:428+; every loc key the panels read
  already exists. Icons chosen from confirmed-existing shared_icons (oratory/essential_category/pop_type) — the
  pre-existing strip's diplomacy.dds is actually MISSING but that is a pre-existing cosmetic issue, left alone.
- se_LOG markers (sys = QING) added to the two report open-effects per the error-logging standing rule.
- Integrity: qing_greatgame.gui 104/104, qing_province_reports.gui 64/64, government_view.gui 1608/1608 braces;
  both panel loc files 0 bad-quote lines; all files no-BOM/LF preserved; no lingering GetCountryByTag.


### Tier C — diplomatic-play OPPOSE + CANCEL (decision, 2026-07-07)
First Tier-C depth item. The diplomatic-play data model, resolution (#58 DIPLOMACY_complete_play),
and player Support button (#147) already existed; the play display had a labeled-but-DEAD target-side
button and no way to withdraw your own play. Added both missing verbs, mirroring Support.

- **OPPOSE = back the TARGET.** Rather than add a redundant "Oppose" button next to Support on the
  instigator side, wired the pre-existing dead target-side stub (its onclick was commented out, enabled
  hardcoded) to a new `DIPLO_player_oppose_play` scripted_gui. Semantics: backing the play's target IS
  opposing the instigator's play — so the target-side button is the natural, already-labeled home for it.
  Renamed that button `support_play_side` -> `support_target_play_side` to disambiguate from the
  instigator-side Support. Done in BOTH templates (diplomatic_play_item + diplomatic_play_global_item).
- **OPPOSE effect mirrors Support:** pay `oppose_diplomatic_play_price` (political_influence = 10, symmetric
  to support's cost), then `DIPLOMACY_modify_play_success = { amt = -10 }`. The negative-amt path runs the
  divide branch of DIPLOMACY_modify_play_success; the multiplier is floored at 0.25 (#79), so amt=-10 is at
  worst -40, clamped to 0 — no blow-up, no crash.
- **OPPOSE is_valid:** has_variable=is_diplomatic_play; player has >=10 PI; NOT instigator (opposing your own
  play is nonsense — that's Cancel); diplomatic_play_success > 0 (no point paying once already collapsed).
  The target OR any third party may oppose; only the instigator is barred.
- **CANCEL = withdraw your own play,** on the instigator side next to Support. New `DIPLO_player_cancel_play`
  scripted_gui, gated on has_variable=is_diplomatic_play + has_variable=manual_play + var:play_instigator =
  scope:player — only the instigator of a MANUAL (player-started) play may cancel; AI/automatic plays are
  excluded. Reuses the proven `AI_remove_diplomatic_play` teardown (de-indexes + strips every play_* var), so
  the next update pass finds nothing to resolve. Influence already spent to begin the play is NOT refunded
  (matches existing end-play semantics; deliberately no cost/refund on Cancel itself).
- **VERIFIED before building:** play_type=manual sets the `manual_play` variable (se_AI.txt:451
  `set_variable = $play_type$_play`); AI_remove_diplomatic_play is a complete/safe teardown; the negative
  branch of DIPLOMACY_modify_play_success cannot underflow. GUI scope idiom reused verbatim from the Support
  button: root = play provobj (`Scope.GetProvince.MakeScope`) + AddScope('player', Player.MakeScope).
- se_LOG markers (sys = DIPLO) added to BOTH new effects per the error-logging standing rule.
- Integrity: gui_templates.gui 1204/1204, EE_scripted_guis.txt 497/497, 00_diplomacy_prices.txt 4/4 braces;
  4 new loc keys quote-clean (exactly 2 quotes each); all files byte-convention preserved
  (gui/scripted_gui/prices no-BOM/LF, loc BOM+LF). Post-implementation code review dispatched.


### Imperial family dynamics → Grand Council (#157, decision, 2026-07-07)
User request: positive AND negative events for the family dynamics between the Emperor, Crown Prince,
and Empress Dowager that affect Grand Council operations. Built on `develop` (unverified branch).

- **Coupling via an EXISTING lever, not a parallel system.** The events move ONE meter,
  `qing_dynastic_harmony` (0..100, init 50), which is folded into the EXISTING
  `qing_council_eff_target` inside QING_council_recompute (se_QING_COUNCIL.txt): (harmony-50)/5,
  a +/-10 effectiveness band. A united house lifts council effectiveness; a court split between
  the heir's faction and the dowager's clique drags it down. This is additive conversion of an
  existing counter (concrete-over-abstract house rule), NOT a new bookkeeping layer — the harmony
  meter is just the shared thermometer + the coupling term. Scaled /5 so it never dominates the
  skill base or the dyarchy +15 bonus.
- **Events act on CONCRETE characters.** Emperor = current_ruler; Crown Prince =
  var:qing_office_crownprince_holder (the SEATS seat var, refreshed each quarter); Empress Dowager
  = current_ruler.mother (guarded is_alive + is_female, the se_QING_SEATS.txt:244 precedent). Every
  option grants real add_prestige / add_loyalty to the character involved, per the house rule — the
  harmony meter is a side effect, not the payload.
- **Five events, 2 positive / 3 negative** (qing_dynasty.1-.5): .1 Dowager's Counsel (heed=+8/overrule=-6),
  .2 Crown Prince Proves Himself (+8/+3), .3 The House Divided (mediate=+10/let-burn=-12), .4 Behind the
  Screen 垂簾聽政 (yield=-10/send-back=-6), .5 The Wayward Heir (indulge=-5/rein-in=+3). Each re-checks
  its own trigger (dowager/crownprince presence) so a stale flavour-roll pick is a harmless no-op.
- **Dispatch:** a low-chance (25%) QING_dynasty_flavour_roll added to the quarterly Qing pulse
  (qing_mechanics_pulse_on_action, CHI-only + is_ai=no + 90-day cooldown) AFTER the governance pulse,
  so the harmony it moves is read fresh next quarter. Kept OUT of the already-huge frontier flavour_roll
  to avoid bloating that random_list.
- **Scoping decision:** QING_dynasty_has_dowager / _has_crownprince written as trigger-body blocks used
  with `= yes` — the proven QING_seat_regency_warranted pattern from the sibling SEATS file (a scripted
  trigger living in a scripted_effects file, resolved by the engine regardless of directory).
- se_LOG (sys=QING) on every effect + event immediate. Task-tagged [#157] comments throughout.
- Integrity: se_QING_DYNASTY.txt 84/84, se_QING_COUNCIL.txt 346/346, qing_dynasty_events.txt 36/36,
  on_action files balanced; loc BOM+LF, 0 bad-quote lines; all refs defined. Post-implementation review dispatched.
- Fixed one self-introduced bug pre-review: dropped a bogus `add_loyalty_to_regime` verb (zero repo
  occurrences) and the unproven `add_loyalty = { value = N }` form → bare `add_loyalty = N` (the proven idiom).

## #158 — Grand Council faction layer + character-driven family events (three linked enhancements to #157)

User's three requests (2026-07-07), built as one coherent Guangxu-vs-Cixi system:
1. "the events should tie into the actual character skills and traits, just like the existing affinity chart"
2. "the existing council events and the new family dynamics events should be interrelated and reference each other"
3. "add a conservative faction vs reformist faction layer covering everyone on the grand council"

- **Two LOCKED design decisions (AskUserQuestion, 2026-07-07):**
  - Faction lean **FEEDS** the existing country-level `qing_reform_faction_balance` (the #14 reform
    end-state meter): QING_faction_feed_reform_balance nudges it ±1..2/quarter toward the council lean.
    Chosen over a standalone meter so WHO sits on the council drives the realm's reform trajectory.
    Kept small so it complements — never clobbers — the mission-tree nudges (+5..+10 per reform task).
  - Polarization = a **DEADLOCK penalty** (not a conservative-drag): a court split 50/50 governs worse
    regardless of side; a united council (reformist OR conservative) functions. polar_pen = 5×(smaller
    bloc), capped 20, docked from qing_council_eff_target beside the #157 harmony coupling.
- **Per-character stance (QING_char_stance, -100..+100):** modelled as the sister of QING_char_affinity —
  reformer/traditionalist traits (±45, the primary poles), zeal (orthodoxy), finesse (reform-minded
  administrator), age (young reform / aged grandee), culture (Han reformist-leaning vs Manchu anchor),
  corruption (status-quo interest), integrity. Scored on every seated office-holder + the 3 figureheads.
- **Figureheads ARE the faction anchors:** Emperor weight 3, Dowager 2, Crown Prince 2 — they sit on the
  council, so their stance dominates the lean (the 光緒-reformer / 慈禧-conservative dynamic given teeth).
- **Ask #1 — family events read real characters:** QING_dynasty_assess runs QING_char_affinity +
  QING_char_stance on the figureheads in each event immediate; every dynasty effect helper now scales its
  deltas by the figurehead's actual skills (finesse/charisma/martial) and affinity with the throne.
- **Ask #2 — cross-linking both ways:** dynasty helpers now move qing_council_effectiveness (a house at
  war paralyses the council; an able heir given a role strengthens it) and, via QING_dynasty_reform_echo,
  tilt qing_reform_faction_balance toward whoever gained sway (dowager-behind-the-screen = the strongest
  echo, scale 3 — the canonical Cixi reform-block). The 3 new faction events pick councillors BY the same
  qing_char_stance the family layer reads, and turn on the figureheads — bridging the two families.
- **Ask #3 — the faction layer itself:** 3 events (Reform Memorial / Behind the Screen / Deadlock) let the
  player adjudicate the split; each moves reform balance + effectiveness + harmony and acts on concrete
  characters (loyalty/prestige, office-vacate purge).
- **Concrete-over-abstract:** the meters are thermometers; every payload is real character prestige/
  loyalty/office changes and the existing effectiveness/reform counters (additive conversion, no new
  parallel bookkeeping layer). Feeds the EXISTING reform meter rather than inventing a second one.
- **Oracle rule N/A:** every idiom used (prev.var: value reads, order_by var:, any_in_list element
  conditions, has_trait reformer/traditionalist, QING_char_affinity) is already proven in-repo; no
  unproven engine capability introduced.
- se_LOG (sys=QING) on every new effect + event immediate; task-tagged [#158] comments throughout.

## Grand Council tab flavour text (user request, 2026-07-07)
- Expanded GOV_VIEW_GRAND_COUNCIL_TOOLTIP (interface_l_english.yml) from a one-line placeholder into
  hover flavour: the vanilla Six Boards / Grand Secretariat / ministries (the Government + Offices tabs)
  have hardened into ceremonial husks that keep the forms but govern nothing, while real power has drained
  inward to the Grand Council — the true centre of political gravity. Header + #TF click-hint formatting.
