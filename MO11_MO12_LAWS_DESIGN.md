# MO#11 Employment Laws & MO#12 Industrialization Laws — design (2026-07-29)

Branch: merge-overnight (worktree imp19c-mo). From merge-overnight boot-test findings #11/#12
("laws governing employment" / "laws governing industrialization"; MUST integrate with the
EXISTING building + manufactured-goods economy, not a standalone modifier layer).

## 1. How laws work here (verified)
- Law group = bare key `= { potential={} <opt1>={} <opt2>={} ... }`. See common/laws/00_economic_laws.txt
  (currency_law, non_tribal_land_law, labour_organisation_law, business_regulation_law) and
  00_qing_statutes_laws.txt (45+ groups).
- Each option may carry: `allow={}` (selectable gate: tech/date/var), `modifier={}` (standing country
  modifier while active — dominant safe pattern), `on_enact={}` (one-shot; fires on EVERY re-enact →
  any nudge is farmable → must be once-guarded per LAW_EXPANSION_DESIGN_DOC.md).
- `potential={}` at group level gates whole-group visibility (is_tribal=no worldwide; tag=CHI Qing-only).
- AI weighting: NO ai_will_do/ai= exists anywhere in this mod's laws (or vanilla stubs). Law desirability
  is the engine's built-in heuristic on standing modifiers. Cannot author custom AI weights → structural
  limit, flagged to user (risk 3).
- GUI registration is MANDATORY + manual: gui/government_view.gui hand-lists each group as a laws_widget
  in a laws_widget_area. Omission = console-only/invisible (the "succession_law" precedent). Empty vertical
  flowcontainer at :2455-2459 is the insertion point.
- Loc: localization/english/laws_l_english.yml flat keys group / group_desc / option / option_desc.

## 2. Economy hooks (verified file:line)
- Employment fill-ratio: JOBS_svalues.txt JOBS_buildings_cap (:402-415) = 0.5×(pop−tribesmen)×(1+civ/100)
  + depot cap, min=1. JOBS_available_slots (:433-435) = cap − used; read by sufficient_job_slots trigger
  (00_buildings_scripted_triggers.txt:1-6) which EVERY buildable building's allow= requires.
- Cottage vs mechanised: se_COTTAGEIND.txt 24 recipes at governorship scope; steel/chemicals/motors/
  electronics/rare_alloys/late_munitions/late_artillery/steel_ships/machine_parts/petrochemicals are
  factory-only. Throughput scale = TECH_cottage_industry_overall_bonus (TECH_svalues.txt:12-26) =
  1 + two invention-gated 0.1 adds. ← BIAS-A target.
- Factory capacity gate: every IND_/qing_industry_ building allow= requires
  INDUSTRY_province_industry_capacity > num_of_IND_industrial_estate.
  INDUSTRY_province_industry_capacity (INDUSTRY_svalues.txt:3-40) scales infra counts by
  owner.MODIFIER_industry_productivity = 1 + modifier:global_import_commerce_modifier
  (MODIFIER_svalues.txt:95-99). ← the single global industrial-capacity lever for MO#12.
- Proven law tokens (used in 00_economic_laws.txt/00_social_laws.txt):
  global_{upper,middle,lower,proletariat,indentured,slaves}_{output,happyness}, build_cost, build_time,
  global_commerce_modifier, global_tax_modifier, research_points_modifier, manpower_recovery_speed,
  population_growth, global_unrest, stability_monthly_change, monthly_corruption, global_capital_trade_routes,
  global_import_commerce_modifier.
- No settable "price" token (prices emergent from trade averaging) → no worldwide tariff law (risk 5).

## REVIEW AMENDMENTS (adversarial design review, folded in 2026-07-29)
1. **TOKEN FIX:** `population_growth` is NOT a country modifier here → use `global_population_growth`
   (proven in 00_social_laws.txt womens_law/healthcare_law). Applies to statutory_ten_hour_act +
   protective_labour_age + eight_hour_movement wherever this doc wrote population_growth.
2. **BIAS-VAR REVERT BUG:** empty `{}` default options never clear EMPLOY_tenure_bias / INDUS_cottage_bias
   → reverting from a non-default option leaves the bias stuck (silent restore failure). FIX per proven
   Qing bias-law idiom (00_qing_statutes_laws.txt qing_military_upkeep_law etc.): the DEFAULT option of
   workplace_safety_and_tenure_law and cottage_to_factory_transition_law MUST carry
   `on_enact = { set_variable = { name = <bias> value = 0 } }`, and every non-default option sets its
   explicit value. Keep the has_variable read-guard (value=0 makes both paths baseline-equivalent).
3. **STACK CHECK:** global_proletariat_happyness (working_hours + workplace_safety + existing
   labour_organisation_law) and build_cost (child_labour + capacity + cottage + existing non_tribal_land)
   can co-hold. Worst-case sums verified bounded below (each new delta sized <= existing land-law).

## 3. MO#11 — common/laws/00_employment_laws.txt (worldwide, potential={is_tribal=no}), 3 groups × 4 opts
### working_hours_law  (pure modifier-swap, no on_enact)
- unregulated_shifts (DEFAULT): {}
- sweatshop_hours: global_proletariat_output=0.08, global_lower_strata_output=0.04,
  global_proletariat_happyness=-0.15, global_lower_strata_happyness=-0.08, global_unrest=0.3
- statutory_ten_hour_act [invention=tech_manufactories]: global_proletariat_output=-0.02,
  global_lower_strata_output=-0.01, global_proletariat_happyness=0.05, manpower_recovery_speed=0.03
- eight_hour_movement [invention=tech_electricity]: global_proletariat_output=-0.05,
  global_lower_strata_output=-0.02, global_proletariat_happyness=0.12, global_middle_strata_happyness=0.03,
  population_growth=0.01, research_points_modifier=0.02
### child_and_bonded_labour_law  (sized BELOW non_tribal_land_law indentured_tenancy ±0.1 to bound stacking)
- customary_practice (DEFAULT): {}
- protective_labour_age [invention=tech_manufactories]: global_lower_strata_happyness=0.08,
  global_proletariat_happyness=0.05, global_lower_strata_output=-0.03, population_growth=0.01,
  research_points_modifier=0.02
- indentured_apprenticeship: global_indentured_output=0.15, global_indentured_happyness=-0.05,
  global_lower_strata_happyness=-0.03, build_cost=-0.03
- workhouse_system: global_indentured_output=0.25, global_proletariat_output=0.05,
  global_indentured_happyness=-0.15, global_proletariat_happyness=-0.10, global_unrest=0.4, build_cost=-0.05
### workplace_safety_and_tenure_law  (BIAS-B into JOBS_buildings_cap via var EMPLOY_tenure_bias)
- customary_hiring (DEFAULT): bias 0, {}
- flexible_hire_and_fire: bias +0.04, global_proletariat_happyness=-0.05, build_time=-0.05
- regulated_tenure [invention=tech_manufactories]: bias 0, global_proletariat_happyness=0.05,
  global_lower_strata_happyness=0.03, build_time=0.03
- protected_employment [civic_tech>=6]: bias -0.04, global_proletariat_happyness=0.12,
  global_lower_strata_happyness=0.06, global_unrest=-0.2, build_time=0.08, monthly_corruption=-0.02

JOBS_svalues.txt guarded hook (inside JOBS_buildings_cap, immediately before its `min = 1`):
    if = { limit = { owner = { has_variable = EMPLOY_tenure_bias } }
           multiply = { value = 1  add = owner.var:EMPLOY_tenure_bias } }
(unset var ⇒ untouched; multiplicative tilt keeps it proportional to province size)

Rejected MO#11 candidates: minimum-wage (wages emergent, not settable; overlaps labour_organisation_law);
unionisation (ALREADY shipped = labour_organisation_law). Not built to avoid double-count.

## 4. MO#12 — common/laws/00_industrialization_laws.txt, 3 groups × 4 opts
### industrial_capacity_policy_law  (worldwide, moves global_import_commerce_modifier = capacity ceiling)
- laissez_faire_pace (DEFAULT): {}
- state_subsidized_industrialisation [invention=tech_manufactories]: build_cost=-0.15,
  global_tax_modifier=-0.05, monthly_corruption=0.03, global_import_commerce_modifier=0.05
- forced_pace_industrialisation [invention=tech_mechanical_tools]: build_time=-0.20,
  global_import_commerce_modifier=0.10, global_proletariat_happyness=-0.10,
  global_middle_strata_happyness=-0.05, global_unrest=0.2
- cautious_gradualism [invention=tech_manufactories]: build_cost=0.05, global_upper_strata_happyness=0.05,
  stability_monthly_change=0.01, global_import_commerce_modifier=-0.02
### enterprise_ownership_model_law  (potential={is_tribal=no NOT={tag=CHI}} — mutually exclusive w/ Qing statute)
- mixed_enterprise (DEFAULT): {}
- state_directed_industry [invention=tech_manufactories]: research_points_modifier=0.05,
  global_commerce_modifier=-0.03, global_tax_modifier=-0.02
- private_capital_industry [invention=tech_manufactories]: global_commerce_modifier=0.05,
  global_middle_strata_output=0.05, global_upper_strata_output=0.05, research_points_modifier=-0.02
- free_incorporation [civic_tech>=6]: global_commerce_modifier=0.10, global_upper_strata_output=0.10,
  global_capital_trade_routes=1, global_proletariat_happyness=-0.10
### cottage_to_factory_transition_law  (BIAS-A into TECH_cottage_industry_overall_bonus via var INDUS_cottage_bias)
- unguided_transition (DEFAULT): bias 0, {}
- protect_cottage_industry: bias +0.10, global_import_commerce_modifier=-0.03,
  global_middle_strata_happyness=0.05, global_lower_strata_happyness=0.05
- promote_mechanisation [invention=tech_manufactories]: bias -0.05, global_import_commerce_modifier=0.05,
  global_proletariat_output=0.03, global_middle_strata_happyness=-0.03
- full_mechanisation_drive [invention=tech_mechanical_tools]: bias -0.10, global_import_commerce_modifier=0.10,
  global_proletariat_output=0.06, global_middle_strata_happyness=-0.08, global_lower_strata_happyness=-0.05,
  build_cost=-0.05

TECH_svalues.txt guarded hook (append inside TECH_cottage_industry_overall_bonus before closing brace):
    if = { limit = { owner = { has_variable = INDUS_cottage_bias } }
           add = owner.var:INDUS_cottage_bias }

Rejected MO#12 candidate: worldwide tariff (no generic real-goods trade hook outside Canton; would ship inert).

## 5. Build list
NEW: common/laws/00_employment_laws.txt, common/laws/00_industrialization_laws.txt (BOM per siblings).
EDIT: common/script_values/JOBS_svalues.txt (1 guarded if), common/script_values/TECH_svalues.txt (1 guarded if),
      gui/government_view.gui (2 laws_widget_area, 3 widgets each; slot into empty flowcontainer :2455-2459),
      localization/english/laws_l_english.yml (2 area headers + 6 group name/desc + 24 option name/desc = 48 keys).
NEW backing vars: EMPLOY_tenure_bias, INDUS_cottage_bias (country vars; set only via on_enact=set_variable;
      read guarded; never nudged → no toggle-farm).
ICONS: none new (all tokens have modifier icons except global_indentured_output which renders icon-less — cosmetic).

## 6. Risks
1. Double-count vs non_tribal_land_law (build_cost/lower-strata): sized below land-law, additive-bounded.
2. Undefined tokens: all grep-confirmed in existing law/building/invention/modifier_icon files; re-verify at build.
3. AI never picking: no ai_will_do capability in mod → engine default only. Structural, flag to user.
4. Save-compat: every default option no-op ({}, bias unset); both hooks has_variable-guarded → byte-identical default.
5. No worldwide tariff (fake-choice avoided).
6. GUI omission = silent invisibility (succession_law precedent): add areas in SAME commit as law files.
