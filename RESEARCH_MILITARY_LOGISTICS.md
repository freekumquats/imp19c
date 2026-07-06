# Military Logistics — Mechanics Research & Expansion Options

*Imperatrix: Victoria (Imperator: Rome engine). Research date: 2026-07-05. Read-only investigation + feasibility-graded expansion proposals.*

> **Oracle-check correction (added by parent after the research pass):** the research agent reported it
> consulted *zero* oracle mods because it could not find the Terra-Indomita / Invictus paths, and therefore
> graded every feasibility question from this codebase + engine assumptions alone. Both oracle repos DO exist
> (`/Users/alan.chiang/github.com/dementive/Terra-Indomita`, `/Users/alan.chiang/github.com/SnowletTV/Invictus`).
> A follow-up oracle grep resolved the two central unknowns — see **§F1 (RESOLVED)** at the bottom. Net effect:
> Proposals 3 & 4 no longer need to degrade to total-cohort proxies (`num_of_unit_type` is proven), and the
> goods-gate-plus-scripted-shortage design (not custom unit attributes) is confirmed as the correct approach.

---

## A. Current logistics mechanics

### A1. Vanilla supply & attrition baseline
- **Supply limit** (`common/defines/00_defines.txt:697-703`): `SUPPLY_LIMIT_OWNER = 0.25`, `_ACCESS/_ALLY/_CONTROLLER = 0.1`; `BaseSupplyLimit() * (1.0 + efficiency)`. Modifier keys: `supply_limit` (flat), `supply_limit_modifier` (%), `global_supply_limit_modifier`.
- **Attrition**: units carry `attrition_weight` / `attrition_loss`; provinces/terrain impose `attrition` (flat) and `max_attrition` (ceiling); navies use `naval_unit_attrition`.
- **Unit food** (`common/units/*.txt`): every unit defines `food_consumption` (e.g. regular_infantry `0.20`, artillery `0.50`) and `food_storage` (supply_train `50`, regular_infantry `2.8`). Supply train is a mandatory support cohort (`common/units/army_supply_train.txt:1-2`). Food is the engine's supply currency; there is **no scripted subtraction of food stockpiles by armies** — the engine handles the consumption tick.

### A2. Mod overrides
- Provinces have `local_food_capacity` (buildings raise it, e.g. `qing_granary_buildings.txt:23 = 200`), `local_monthly_food` / `local_monthly_food_modifier`. `DEFAULT_FOOD_CAPACITY = 0` (defines:709) — capacity is building-driven.
- `arsenal_building` (`common/buildings/00_military_buildings.txt:20`) exists, gated on `tech_firearms`, **counted in demand but has no output modifiers / no supply-production hook** — the biggest single gap.
- `INF_railway_upgrade` grants `army_movement_speed = 0.1` (not supply); `INF_depot` grants a build slot (not a supply depot).

## B. Goods system inventory
- Trade goods live in `common/trade_goods/00_imp19c.txt` (48 goods). Military-relevant: `horses`, `elephants`, `camel`, `wood`, `iron`, `tin`, `coal`, plus manufactured `early_munitions`, `late_munitions`, `early_artillery`, `late_artillery`, `naval_supplies`, `steel_ships`, `wooden_ships` (`zz_injectormaker/military_goods.txt`, `se_GOODS.txt:71-80`).
- **`allow_unit_type = <unit>`** inside a trade-good definition gates recruitment on that good (`00_imp19c.txt:118` horses→cavalry, `:297` iron→heavy_infantry). PROVEN idiom in this codebase.
- Quarterly flow (`on_action` `quarterly_trade_pulse`, `oa_economy_setup.txt`): production (raw per-governorship `GOODS_governorship_X_produced`; industrial via `COTTAGEIND_produce_X` + `INDUSTRY_production_X`) → demand (`DEMAND_svalues.txt`, military demand at `:1436-1573` = `num_of_cohorts * pop_ratio * 0.01 + fortresses + arsenals + military jobs`) → consumption (`se_CONSUME.txt:19` `CONSUME_all_stockpiles`, wired at `oa_economy_setup.txt:2339`) → shortage tracking (`CONSUME_update_shortage`, per-good `var:shortage_X` as a 0..1 ratio) → trade split.
- **CRITICAL GAP:** military goods are produced, demanded, and their shortages computed — but **no scripted effect reads `shortage_early_munitions` etc. to penalise armies.** The engine's unit `food_consumption` loop is entirely parallel to the quarterly trade sim.

## C. The food supply link
- Food goods carry `local_monthly_food = 0.07`; engine accumulates into province food capacity. `se_GOODS.txt:125+` records `grain_stockpile` etc. as variables.
- `ECON_governorship_food_shortage` (`ECON_svalues.txt:377-422`) = average shortage fraction across the 6 food goods, ×2.
- **Only concrete consequence of food shortage in the codebase:** migration push (`MIGRATION_svalues.txt:49-54` adds `food_shortage × 8` to emigration pressure). **Zero** effects read food shortage to impose attrition/morale/movement penalties on armies.

## D. Available hooks
- **Units**: `food_consumption`, `food_storage`, `attrition_weight`, `attrition_loss`; `allow = { ... }` can gate on `invention` and (per oracle) on triggers like `trade_good_surplus`.
- **Buildings**: `arsenal_building` (no output yet — extend it); `qing_granary_building` is the stockpile-building template; modifier keys `supply_limit`, `supply_limit_modifier`, `local_monthly_food_modifier`, `local_food_capacity`, `army_movement_speed` available. `add_building_level` spawns buildings from events. `num_of_arsenal_building` counter is proven (used in demand at `DEMAND_svalues.txt:1448`).
- **Pulses**: monthly (`00_monthly_country.txt`), quarterly (`oa_economy_setup.txt` `quarterly_trade_pulse`). Best insertion point: after `CONSUME_all_stockpiles` (`oa_economy_setup.txt:2339`).
- **se_LOG**: every new effect must carry `LOG_enter`/`LOG_line`/`LOG_exit` with `sys = LOGISTICS` (zero cost outside `-debug_mode`).

## E. Ranked expansion proposals

All follow the standing **concrete-over-abstract** rule and are **additive** (coexist with, do not replace, food-based supply).

1. **[LOW risk, HIGH impact — START HERE] Munitions/artillery shortage → attrition & morale penalty.**
   Read the *already-computed* `shortage_early/late_munitions/artillery` variables in a new quarterly effect
   (after `CONSUME_all_stockpiles`), and stamp tiered country modifiers (`country_munitions_shortage_minor/severe`)
   carrying `land_unit_attrition` + `army_morale_recovery` (+ `army_movement_speed` at the severe tier). **All
   primitives verified in this codebase — no oracle needed.** New files: `se_LOGISTICS.txt`, `logistics_modifiers.txt`,
   + one hook line.
2. **[MEDIUM] Arsenal/depot buildings → local munitions production.** Give `arsenal_building` real output modifiers
   and add a `military_depot_building` (cloned from the granary schema); extend `GOODS_governorship_early_munitions_produced`
   to add `num_of_arsenal_building × rate` + depot term. Creates a concrete on-map supply-infrastructure layer; pairs with #1
   (depots reduce shortage risk). Custom `local_munitions_production` key is display-only — the real accumulation is the scripted
   building-count term (the arsenal is already counted this way in demand). Needs a `tech_logistics` invention or reuse an existing gate.
3. **[MEDIUM-HIGH] Coal / naval supplies for steamers → movement/attrition penalty.** Gate steam units on
   `allow = { trade_good_surplus = coal }`; add `DEMAND_coal_from_navy` (now filterable to steam hulls via the proven
   `num_of_unit_type`); a `country_coal_shortage` modifier penalises naval attrition. Introduces industry-vs-navy coal
   competition. Sailing ships unaffected.
4. **[HIGH, future] `rifles`/`small_arms` trade good + infantry gating.** New manufactured good produced by arsenals + factories,
   demanded by infantry (`num_of_unit_type = { type = regular_infantry ... }`), gating recruitment via `allow = { trade_good_surplus = rifles }`.
   Most invasive (6-file touch: trade_goods, COTTAGEIND, INDUSTRY, GOODS, DEMAND, unit defs + loc) and most aligned with concrete-over-abstract.
   Save until #1–2 are proven stable.

Full per-proposal code sketches, exact insertion points, and file:line citations are in the session transcript
(this file is the durable digest).

## F1. Oracle feasibility checks — **RESOLVED** (parent follow-up)

- ✅ **`num_of_unit_type` — PROVEN.** Real syntax: `num_of_unit_type = { type = <unit> value >= N }` (Terra-Indomita
  mission triggers, e.g. `num_of_unit_type = { type = trireme value >= 8 }`). Proposals 3 & 4 can do genuine
  per-unit-type demand/gating; **no need to degrade to total-`num_of_cohorts` proxies.**
- ✅ **`allow_unit_type` in a trade good — PROVEN** (`allow_unit_type = octere` in Terra-Indomita, matching this mod's
  horses/iron pattern).
- ⚠️ **`trade_good_surplus` inside a *unit's* `allow` block — STILL UNPROVEN.** Oracle hits for `trade_good_surplus`
  are all in missions/decisions, none in unit `allow` gates. Whether it's a hard recruit-block or soft penalty needs
  an in-game test; the goods-gate design should ship with a scripted-fallback pulse in case enforcement is soft.
- ✅ **No custom per-unit resource attributes.** Neither oracle's unit files declare any `*_consumption` / `*_storage`
  beyond food, confirming the report's design: gate via goods surplus + scripted shortage modifiers, **do not** invent a
  `coal_consumption` unit attribute the engine won't read.

## F2. Open design decisions for the human
- Shortage penalty severity / curve (linear vs shortage²).
- Depot cost/output tuning (chokepoint vs background).
- Coal abundance (force industry-vs-navy trade-off, or not).
- Rifles as hard recruitment gate vs soft attrition penalty.
- Roll out generic (all countries) or Qing-first.
- Keep food as baseline "soldiers must eat" layer with military goods as the equipment layer (recommended: parallel systems, quarterly cadence).
