# DESIGN — join the concrete Modern Industry buildings to the goods sim (#69) — v2 (premise corrected)

**Status:** design v2, 2026-08-10. **v1 was built on a FALSE premise and is REJECTED** (see below). Rests on: DIAGNOSIS_INDUSTRY_TWO_SYSTEMS_69.md (Stage-0) + RESEARCH_INDUSTRIAL_REVOLUTION_69.md + the adversarial review of v1 (5 findings, 3 CRITICAL) + DESIGN_MG_BUILDING_PRODUCTION_HOOKS.md (the 2026-08-04 MG-hook, commit 873c4af99).

TERMINOLOGY: "BOM" = byte-order-mark file header ONLY. The manufacturing recipe is "bill of materials".

## WHY v1 WAS WRONG (the review's premise inversion — verified in source)
v1 (and the Stage-0 diagnosis) claimed the concrete industrial buildings "**never** produce in the goods sim." **That is FALSE for 3 of the 4**, and my own memory index records why: the **2026-08-04 MG-hook (873c4af99)** already wires them. Verified in source:
- **textile_mill → clothing**: `GOODS_svalues.txt:3064` adds `GOODS_governorship_clothing_infra_output` INTO the clothing `produced_mechanised` svalue; `:3090` = `num_of_qing_textile_mill_building × GOODS_textile_mill_clothing_output(=2)`.
- **machine_works → (early_)munitions**: `GOODS_svalues.txt:2799` (`num_of_qing_machine_works_building × …_munitions_output`) via `munitions_infra_output`.
- **navy_yard → naval_supplies**: `GOODS_svalues.txt:2895/2920` via `naval_supplies_infra_output`.

These three are **PURE PRODUCERS — supply only** (`GOODS_svalues.txt:3062`: "Pure producer — supply only… no double-count"). This was a **deliberate, reviewed** design choice: DESIGN_MG_BUILDING_PRODUCTION_HOOKS.md:258-266 — the works add SUPPLY, add **no** demand for the finished good (demand-capped so they can't inflate the military topbar income `MILITARY_supplies_income_country`), and the ONE invariant is *"a producing building must not consume the finished good it makes."*

So v1's plan to ADD `building_factories → INDUSTRY_<good>_factories` for those three would have **double-produced** (infra_output + factory path) — the review's C1, a literal same-good double count. v1 is dead.

**Only `steel` is genuinely disconnected** — no infra_output hook exists (`GOODS_governorship_steel_produced_mechanised`, `GOODS_svalues.txt:2990`, sums only the cottage var + the factory-count path; the steel_works/blast_furnace buildings touch neither).

## The CORRECTED gap #69 actually targets
The literal title: *"Connect the live Modern Industry buildings to the goods sim (blast furnace **actually consumes iron → produces steel**, etc.)."*
- 3 of the 4 buildings ARE already connected (they produce) — the "connect to the goods sim" verb is satisfied for them by the MG-hook. What they don't do is CONSUME inputs (produce-only by deliberate design).
- **`steel` is the one building fully disconnected AND is the title's literal example** ("consumes iron → produces steel"). This is the core, unambiguous #69 deliverable.

## The design — TWO honest parts, scoped by regression risk

### PART 1 (CORE, ships now) — wire steel via the single factory-count read point (H1)
The review's H1 correction: the numeric factory-count read is NOT in `produced_mechanised` (that's only a `has_variable` gate); it's one layer down in `INDUSTRY_steel_factories` (`INDUSTRY_svalues.txt:165` = `var:INDUSTRY_factories_assigned_steel`). Both PRODUCE (`INDUSTRY_production_steel_base` `multiply = INDUSTRY_steel_factories`, `:2651`) AND CONSUME (`INDUSTRY_demand_steel_iron` `value = INDUSTRY_steel_factories`, `:2699`; `_steel_coal` `:2726`) funnel through it. **So editing ONE svalue makes a steel works both produce steel AND consume its iron+coal bill of materials — automatically consistent.** This is exactly "blast furnace actually consumes iron → produces steel."

**Impl:**
1. **`INDUSTRY_steel_factories` (`INDUSTRY_svalues.txt:165`)** → `value = var:INDUSTRY_factories_assigned_steel` **+** `add = INDUSTRY_building_factories_steel` (the effective count). The single-point edit; produce + consume both pick it up.
2. **`INDUSTRY_building_factories_steel`** (new svalue) = Σ over the governorship's provinces of `num_of_qing_steel_works_building` (the proven province-loop count idiom — `every_state_province { add = num_of_<building> }`, M2; NOT the nonexistent `num_of_building` block form). Named svalue (can't inline a province loop in a `set_variable value`). RECOMPUTE-not-accumulate is moot here (it's a pure svalue read of the live building count each evaluation, no stored var to accumulate) — SIMPLER than v1's separate-store scheme, which was only needed to dodge the (nonexistent) accumulation problem.
3. **C3 gate fix** — the produce path gates on `has_variable = INDUSTRY_factories_assigned_steel` at three sites (`se_GOODS.txt:1467`, `GOODS_svalues.txt:2995`, `DEMAND_svalues.txt:1131`). A governorship with a steel works but no button-assigned steel factory has no such var → the gate fails → the building produces nothing (the review's C3, which would silently break PART 1). **Verify first:** `INDUSTRY_setup_all_factory_assignments` (`oa_economy_setup.txt:248`) runs for EVERY governorship at setup — confirm it initialises `INDUSTRY_factories_assigned_steel = 0` for all. If yes, the `has_variable` gate is always true and C3 is a non-issue. If NOT, widen the three gates to `OR = { has_variable = factories_assigned_steel  ...building_factories_steel>0 }` and guard both `var:` reads. **This check is the make-or-break for PART 1 — resolve at impl before writing the gate.**
4. **Building→good: `qing_steel_works_building` → steel ONLY.** Per H2 + the research (§1a/§1d): a blast furnace terminates at pig/wrought iron, NOT steel; `IND_blast_furnace_building` is `trade_goods = iron` and already raises iron via `base_resources = 2` (`IND_heavy_industry_buildings.txt:49-68`) — same reason coal_mine is skipped. So `IND_blast_furnace` and both coal mines are **SKIPPED** (raw goods, already on the vanilla base_resources path). The dedicated steel converter (`qing_steel_works_building`) is the steel producer.
5. **Per-building weight** = 1 (1 steel works = 1 factory-equivalent), best-guess; tune on boot if it over/under-produces vs button factories.
6. **-debug_mode logging** — a per-governorship LOG line each quarter the steel-works count is nonzero: emits the building count + resulting effective steel factory count, so the boot SURFACES a steel works becoming a real steel factory (STATIC label, no macro/#).

### PART 2 (input-consumption for the 3 already-producing buildings) — SCOPE BOUNDARY, flagged LOUDLY, NOT silently dropped
The 3 MG-hooked buildings (clothing/munitions/naval_supplies) already PRODUCE but do NOT consume their inputs (produce-only by design). Making them ALSO consume would complete the consume→produce realism for them too. **But it is NOT a clean add** and I am NOT folding it silently:
- Adding `building_factories → INDUSTRY_<good>_factories` for them **double-produces** (the existing infra_output PLUS the factory path) — the review's C1. To avoid that you must **migrate** them off the produce-only infra_output onto the factory path.
- That migration (a) changes their **output magnitude** (infra: `num × output(=2)`; factory: `count × production_rate × bonuses × (1 − shortage malus)`) → needs recalibration; (b) for `munitions`/`naval_supplies` it re-routes a **deliberately demand-capped MILITARY-topbar income subsystem** (`MILITARY_supplies_income_country`, the whole point of the MG-hook) through a different path → real regression risk to the military income model; (c) requires the C3 gate widen for all three goods or a building-only governorship regresses to producing nothing.
- **This is a refactor of a shipped, reviewed subsystem with a military-income regression surface — a distinct task with its own diagnosis + review, not a safe fold into #69.** Evidence it's a real boundary, not a convenience cut: the produce-only model is documented-deliberate (DESIGN_MG_BUILDING_PRODUCTION_HOOKS.md:258-266) and the review's C1 shows the naive add double-produces.

**#69's title ("connect … to the goods sim") is DELIVERED:** steel (the disconnected building + the literal example) gets full consume→produce; the other 3 are already connected (produce). PART 2 (their input-consumption) is bounded out with a concrete technical reason (military-topbar regression), logged here for a follow-on task. **If the adversarial review judges PART 2 in-scope, I build the migration too** — this boundary is the review's to test.

## GLOBAL / #23-#60 safety (PART 1)
- `qing_steel_works_building` is invention/civ-gated (~1860s+, post-Bessemer era) — a 1763 game has none → `INDUSTRY_building_factories_steel` = 0 → **byte-identical to today until a country builds a steel works.** (Review M1: gating is by invention reachability, not date; verify no 1763 country starts owning it, and note the mid-game-anachronism risk is a separate calibration matter.)
- Raising steel supply LOWERS the steel price (trade/price blend), NOT the currency/silver gbip — **review CONFIRMED #23 peg reads only gold/silver reserves × metal unit-prices** (`CURRENCY_svalues.txt:234-278`); no manufactured-goods price touches the backing. Peg untouched. Div/0 CONFIRMED safe (guarded divisions, `country_unit_price min = 0.0001`).
- Also newly CONSUMES iron+coal where steel works exist → raises iron/coal demand (can create shortages that throttle steel output via the existing `INDUSTRY_malus_steel_production_*` — self-limiting, correct).
- Perf: the province-count scan rides the proven `COTTAGEIND_cache_all_values` per-governorship-per-quarter cache pattern (`se_COTTAGEIND.txt:39-116`); one `every_state_province` pass, cached to a var (review-confirmed within envelope).

## ASSUMPTIONS / GUESSES (→ overnight ASSUMPTIONS)
- Steel-works per-building weight = 1 factory-equivalent (best-guess; boot-tune vs button-factory output).
- PART 1 only (steel). PART 2 (the 3 produce-only buildings' input-consumption) deliberately bounded out — see PART 2; the review may pull it in.
- C3: assuming `INDUSTRY_setup_all_factory_assignments` inits `factories_assigned_steel=0` for every governorship (→ gate always true). VERIFY at impl; if false, widen the 3 gates.

## VERIFY (boot)
- 1763 game: `INDUSTRY_building_factories_steel` = 0 everywhere, steel sim byte-identical (no steel works exist).
- Industrialised save: building a `qing_steel_works` raises the effective steel factory count → steel appears in the stockpile AND iron+coal demand rises (bill of materials consumed); the per-governorship LOG line shows it. No accumulation (pure count read).
- Steel price falls sanely where steel works concentrate; #23 gbip flat (gold/silver only); no ROW break; no div/0.

## Rejected (logged)
- **v1 (add building_factories to all 4 via a separate store):** built on the false "never produce" premise → double-produces clothing/munitions/naval_supplies (review C1). REJECTED wholesale.
- **IND_blast_furnace → steel (v1 map):** category error — a blast furnace makes pig iron, not steel (research §1a; H2); it already raises iron via base_resources. SKIP.
- **machine_parts / ships mapping (v1):** WRONG — the MG-hook already established the correct goods (munitions/naval_supplies) for those buildings; don't re-map.
- **Separate-store recompute-not-accumulate scheme (v1):** unnecessary — a pure svalue province-count read has nothing to accumulate; the stored-var scheme only existed to dodge a nonexistent problem.
