# P4 — `rifles` trade good + infantry gating (DRAFT, not yet applied)

*Companion to RESEARCH_MILITARY_LOGISTICS.md proposal #4. Military-logistics suite: `sys = LOGISTICS`.*

**Status: DRAFT ONLY — deliberately NOT wired into live files.** P4 is the HIGH-risk,
6-file member of the suite and carries the one primitive the oracle pass could *not* prove
(`trade_good_surplus` inside a *unit's* `allow` block — RESEARCH §F1). Registering a new
manufactured good means it enters the quarterly CONSUME loop immediately on load; if any one
of the six registration points is missing, the good has demand with no production (or a
stockpile that never initialises) and every country runs a **permanent phantom
`shortage_rifles`** that P1's penalty layer would then punish. So P4 ships as this exact,
ready-to-apply spec and is applied only after P1–P2 are confirmed stable in-game and the
`trade_good_surplus`-in-unit-`allow` behaviour is verified (hard block vs soft) with a live test.

All six edits below follow the same idioms the existing `early_munitions` good already uses,
so P4 is a mechanical clone once green-lit. Preserve each target file's byte convention
(all six are **BOM + UTF-8**; CRLF where the sibling lines are CRLF).

---

## Edit 1 — trade-good definition
`common/trade_goods/00_imp19c.txt` (BOM, LF). Add alongside the other manufactured/military
goods. `allow_unit_type` gates recruitment on the good (PROVEN idiom — `iron → heavy_infantry`
at `:297`). Category 4 (manufactured).

```
rifles = {
	category = 4

	allow_unit_type = regular_infantry

	gold = 0.2

	color = { 0.35 0.25 0.15 }
}
```

## Edit 2 — cottage-industry production
`common/scripted_effects/se_COTTAGEIND.txt` (probe convention). Clone the
`COTTAGEIND_produce_early_munitions` block (`:111`). Add the dispatch call next to its sibling
(`:22`) and the effect body:

```
COTTAGEIND_produce_rifles = {
	# Scope: governorship. Mirrors COTTAGEIND_produce_early_munitions.
	set_variable = { name = COTTAGEIND_produced_rifles  value = 0 }
	# ... same accumulation shape as early_munitions, output = rifles ...
	output = rifles
}
```

## Edit 3 — factory / industrial production
`common/scripted_effects/se_INDUSTRY_setup.txt` + the `INDUSTRY_production_rifles` script value.
Clone `INDUSTRY_setup_factories_early_munitions` (`:88`) and register
`INDUSTRY_factories_assigned_rifles`.

## Edit 4 — governorship production roll-up
`common/script_values/GOODS_svalues.txt` (BOM). Clone
`GOODS_governorship_early_munitions_produced` → `GOODS_governorship_rifles_produced`, summing
the cottage + industry terms **and** (for symmetry with P2) an arsenal building-count term:

```
GOODS_governorship_rifles_produced = {
	value = 0
	if = { limit = { has_variable = COTTAGEIND_produced_rifles }
		add = var:COTTAGEIND_produced_rifles }
	if = { limit = { has_variable = INDUSTRY_factories_assigned_rifles }
		add = INDUSTRY_production_rifles
		multiply = GOODS_governorship_bonus_to_industrial_production_from_industrialisation }
	if = { limit = { owner = { invention = tech_firearms } }
		every_governorship_state = { every_state_province = {
			add = { value = num_of_arsenal_building  multiply = GOODS_arsenal_munitions_output } } } }
}
```
Also wire it into the produce-all path in `se_GOODS.txt` beside the `early_munitions` line
(`:64`) and add its stockpile init in `GOODS_setup_governorship_stockpiles` (`se_GOODS.txt:24`,
mirroring `naval_supplies_stockpile` at `:71`): `rifles_stockpile`.

## Edit 5 — demand
`common/script_values/DEMAND_svalues.txt` (BOM). Clone `DEMAND_early_munitions_base` (`:1436`),
but drive the army term off the **proven** per-type counter instead of total cohorts:

```
DEMAND_rifles_base = {
	value = 0
	if = {
		limit = { owner = { invention = tech_firearms } }
		add = { value = num_of_unit_type = { type = regular_infantry }  min = 0 }   # per-type, not num_of_cohorts
		multiply = DEMAND_army_ratio_rifles
	}
	multiply = owner.MODIFIER_military_supply_consumption
}
DEMAND_rifles = { value = DEMAND_rifles_base  multiply = DEMAND_elasticity_impact  min = 0 }
```
(Confirm the exact `num_of_unit_type` value-read form in a script-value context during the
apply step; the trigger form `num_of_unit_type = { type = X value >= N }` is proven, the bare
value-read needs a quick check.)

## Edit 6 — unit recruitment gate
`common/units/regular_infantry.txt` (BOM, CRLF). Add an `allow` block:

```
allow = {
	trade_good_surplus = rifles      # UNPROVEN in unit allow — verify hard-block vs soft
}
```
**Fallback if soft/ignored:** drop the unit-`allow` gate and instead let P1's
`shortage_rifles` feed the existing munitions penalty tier (add `shortage_rifles` to
`LOGISTICS_scan_worst_land_shortage` in se_LOGISTICS.txt). This degrades P4 gracefully to a
pure attrition-pressure good with no new engine dependency.

---

## Apply checklist (when green-lit)
1. Apply Edits 1–5 **first and together** (production + stockpile + demand all present) so the
   good never has demand without supply. Load once, confirm no phantom `shortage_rifles` on a
   supplied country via the ECON/LOGISTICS debug trace.
2. Then add Edit 6's gate and test recruit-block behaviour.
3. Extend `LOGISTICS_scan_worst_land_shortage` (se_LOGISTICS.txt) to include `shortage_rifles`
   so the P1 penalty covers rifles too.
4. Add loc keys for `rifles` (name + the two new buildings if not already present).
5. se_LOG: the production/demand clones inherit tracing via ECON_LOG; no new effect needs its
   own LOG wiring beyond what the cloned siblings already carry.
