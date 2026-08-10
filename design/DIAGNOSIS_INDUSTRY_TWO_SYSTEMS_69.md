# DIAGNOSIS (Stage 0) — #69 Modern Industry buildings vs the goods sim

**Status:** Stage-0 diagnosis, 2026-08-10, source+git traced. Awaiting adversarial review before any design. This diagnosis **inverts the task's original premise** — read before designing.

TERMINOLOGY: "BOM" = byte-order-mark file header ONLY. Manufacturing recipe = "bill of materials", spelled out.

## The premise was WRONG (corrected here)

The task was written on the stale #133 memory ("manufactured-goods var-sim is ~30% live, gated OFF, produce driver commented out, MANUFACTURE_* undefined"). Tracing the CURRENT code shows that is **out of date**: the factory production sim is LIVE.

### What is actually live (traced)
- **`GOODS_governorship_produce_all` runs EVERY quarter** — oa_wealth_changes.txt:171 (right beside the cottage driver at :172), plus the game-start fill at oa_economy_setup.txt.
- It calls **`GOODS_governorship_produce_industry` for all 24 manufactured goods** (se_GOODS.txt:1378+): steel, chemicals, rare_alloys, processed_foods, motors, electronics, petrochemicals, naval_supplies, munitions/artillery, ships, etc.
- Each `produce_industry` (se_GOODS.txt body) adds `GOODS_governorship_<good>_produced_mechanised` to `<good>_stockpile`, **gated on `has_variable = INDUSTRY_factories_assigned_<good>`**.
- The mechanised-output term (`GOODS_governorship_<good>_produced_mechanised`, GOODS_svalues.txt:3044+ for clothing etc.) = `INDUSTRY_production_<good> × industrialisation-bonus × employment-ratio`, gated on the same `factories_assigned` var.
- The **bill of materials IS consumed**: `#133 I3` wired `INDUSTRY_demand_<good>_<input>` into the `DEMAND_<input>` aggregators (e.g. DEMAND_steel_iron/_coal, DEMAND_whales pharma branch) — the factory branches gated on `INDUSTRY_factories_assigned_<good>`.
- `INDUSTRY_factories_assigned_<good>` **IS incremented** (not stuck at 0): a game-start per-country seed (oa_economy_setup.txt:254-352, e.g. GBR clothing +3, bronze +1) AND the player GUI buttons (industrial_goods_buttons.txt — `add_<good>_button` pays a price + `INDUSTRY_assign_factory{ amount=1 }`, consuming an abstract industry slot).

### What is actually dead (and WHY — git-traced)
- `debug_demand.3/.4` + the `MANUFACTURE_*` effects: **deliberately DELETED in 2c69f9b83** ("MG Phase 3 I1: dead-code removal"). The commit message is explicit: `GOODS_governorship_produce_manufactured/_2` and `GOODS_consume_industrial_demand` were "**superseded by _produce_industry**" — i.e. the OLD driver was removed BECAUSE the NEW live `produce_industry` path replaced it, not because the feature failed. So "the produce driver is disabled" is FALSE for the current code; the OLD driver is gone, the NEW one is live.
- => The #133 memory is STALE (pre-#133-I2-I12). It should be updated: the var-sim is live, not 30%-stubbed.

## The REAL gap (the actual #69)

Factories in the live sim are an **ABSTRACT slot-counter** (`INDUSTRY_factories_assigned_<good>` + `INDUSTRY_governorship_industry_slots`), driven by GUI buttons + a game-start seed. This is a COMPLETE, working representation of industry.

The concrete **Modern Industry BUILDINGS** (IND_heavy_industry_buildings.txt: coal_mine/blast_furnace/steel_mill; qing_industry_buildings.txt: Hanyang/Jiangnan/Kaiping) are a **SEPARATE, PARALLEL representation**: they grant pop/output/civ via engine building modifiers + `show_model="factory"`, and are gated on the abstract `INDUSTRY_province_industry_capacity > num_of_IND_industrial_estate`. They **never increment `INDUSTRY_factories_assigned_<good>`**, so building a blast furnace does NOT add a steel factory to the production sim.

**So #69's real content is: two parallel, non-communicating factory representations.** Building an `IND_blast_furnace` gives pop/output/civ modifiers but produces no steel in the goods sim; adding a "steel factory" via the counter produces steel but places no building on the map. They model the same thing twice, disconnected.

### Root-cause classification (per the task's a-e)
Neither (a) perf disaster, (b) crash, nor (c) economy-destabilization. It is (d)+(e): the OLD var-sim driver was cleanly retired (superseded), the NEW slot-counter sim is live and working, and the concrete IND_ buildings were added later (buildings-research 2026-07-27) as a PARALLEL flavour/pop layer **without ever wiring them into the counter**. Not a regression — an unfinished join between two independently-built systems.

## Verdict + what the design must decide (NOT decided here — needs the research + design stage)
This is a genuine gap, buildable, but the design must choose the JOIN model, and it needs the Industrial-Revolution research (already Stage-1 of the task) to ground it:
- **Option A — buildings FEED the counter:** a live pulse sets/increments `INDUSTRY_factories_assigned_<good>` from `num_of_<IND building>` (blast_furnace → steel, coal_mine → coal-side, etc.). Smallest wire; makes the concrete building the driver of the abstract sim. Risk: double-count if a province has BOTH a counter-assigned factory (button) AND the building — the design must pick ONE source of truth per good.
- **Option B — unify:** make the buttons build the actual IND_ building (add_building_level) and derive the counter from building counts, retiring the abstract slot as the input. Bigger, cleaner, but touches the GUI + every good.
- **Option C — leave parallel, document:** if the two are intended as alternative flavours (abstract slots for non-China, concrete named works for the Self-Strengthening arcs), the "gap" is by design — but then the buildings should at least not imply production they don't deliver. Least work; may be the honest answer for some goods.

The design stage (gated on THIS diagnosis passing adversarial review + the Stage-1 IR research) picks among these per the history + the double-count risk. The honest outcome may be "unify only the China Self-Strengthening named works, leave the generic IND_ as pop/output flavour" — to be decided with evidence, not now.

## Corrections this diagnosis forces elsewhere
- Update memory imp19c-manufactured-goods-risk: the var-sim is LIVE (produce_industry, all 24 goods, quarterly), NOT 30%-stubbed. The dead MANUFACTURE_* path was superseded + deleted (2c69f9b83), not "gated off pending".
- #69 task text (premise "produce driver disabled / nothing increments factories_assigned") is WRONG — both are live. The real gap is the building↔counter disconnect. Rewrite before design.
