# Manufactured-Goods System — Design & Decision Log

**Branch:** `manufactured_goods` (isolated off `merge-overnight` @ `0c56dfb2b`, incl. #122–#132 + #129).
**Task:** #133 (re-scoped from a risk report to a full implementation).
**Status:** Phase 2 (design). This document is the RUNNING DECISION LOG — every design decision,
trade-off, upstream finding, and review outcome is recorded here as work proceeds.

> Governing directives (from the user, recorded in memory `imp19c-manufactured-goods-build-rules`):
> move slowly & carefully; research every change against upstream; review every step adversarially;
> never defer for difficulty OR risk (the branch IS the risk isolation); tie into raw goods,
> buildings, the rest of the economy, and **especially employment**; **asymmetric fidelity** — Qing
> granular, rest-of-world abstracted; then research 18c-appropriate goods & implement them; then a
> performance assessment + optimizations trading small accuracy for large perf. Autonomy is absolute:
> best-guess-and-record when a decision would otherwise need the user.

---

## 1. CURRENT STATE (Phase-1 research, verified against the tree)

The manufactured-goods layer is **not a greenfield build** — it is ~30% live plumbing / ~70% stub,
with TWO independent production paths and a fully-live consumption path. The precise state:

### 1.1 Definitions
- `is_manufactured_tradegood` (`common/scripted_triggers/00_trade_scripted_triggers.txt:97`): **24
  goods** — clothing, luxury_clothing, furniture, luxury_furniture, alcohol, glass, chemicals,
  rare_alloys, construction_materials, early_munitions, late_munitions, naval_supplies, steel_ships,
  wooden_ships, steel, bronze, machine_parts, early_artillery, late_artillery, electronics,
  pharmaceuticals, motors, processed_foods, petrochemicals.
- Per-good variables (governorship scope): `INDUSTRY_factories_assigned_X` (factory count),
  `X_stockpile`, `COTTAGEIND_produced_X`, `INDUSTRY_production_X` (mechanised output rate),
  `local_price_X`/`global_mean_price_X`, `shortage_X`, `DEMAND_X`.

### 1.2 Production — TWO paths
**(a) Mechanised (factory) path.** `IND_industrial_estate` buildings provide generic slots; a slot's
good is chosen by `INDUSTRY_assign_factory` (`se_INDUSTRY_factory_assignment.txt:1`) writing
`INDUSTRY_factories_assigned_X`. Output rate `INDUSTRY_production_X` exists for **9 goods only**
(clothing, luxury_clothing, bronze, machine_parts, naval_supplies, alcohol, glass, early_munitions,
early_artillery — `INDUSTRY_svalues.txt`). `GOODS_governorship_produce_all` (`se_GOODS.txt:1037`)
adds output to stockpiles for **only 4** of them (clothing, luxury_clothing, machine_parts, bronze).

**(b) Cottage path — LIVE, and it already integrates pops + raw goods.** `COTTAGEIND_produce_all`
(`se_COTTAGEIND.txt:4`), called quarterly from `oa_wealth_changes.txt:163`, has real raw-good recipes
for **15 goods**. Each recipe (e.g. `COTTAGEIND_produce_clothing`) sums `COTTAGEIND_raw_<input>` vars
then calls `COTTAGEIND_scale_production`, which multiplies by **`COTTAGEIND_pops_output`** (a pop-count
scalar: `governorship_middle_strata` + `_lower_strata`, summing `num_of_*_strata` across provinces —
`ECON_svalues.txt`) and by `TECH_cottage_industry_overall_bonus`, then adds to `X_stockpile`. **This is
the template for the whole integration story** (pops → output → raw-input consumption → stockpile).

**(c) The generalized macro nobody calls.** `GOODS_governorship_produce_industry` (`se_GOODS.txt:1361`)
is a clean, already-written generic effect: `if has_variable INDUSTRY_factories_assigned_$tradegood$ →
change_variable X_stockpile add GOODS_governorship_$tradegood$_produced`. It is defined and correct but
called nowhere. **This is the un-gate path** — not the undefined `MANUFACTURE_*`.

### 1.3 Consumption — LIVE for 23 of 24
`CONSUME_all_stockpiles` (`se_CONSUME.txt:19`), called quarterly (`oa_wealth_changes.txt:298`),
iterates `every_tradegood_complex` and does `X_stockpile -= DEMAND_X`, then computes `shortage_X`.
This runs for **23 of the 24 manufactured goods already**. So the imbalance is production-side: stubbed
goods are consumed but never produced → their stockpiles sit at/below 0 permanently.
**[REVIEW CORRECTION — was "all 24"]** `rare_alloys` is **absent** from the `every_tradegood_complex`
key list (the `tradegood_hypercomplex` block in `zz_tradegood_injector.txt`), so
`rare_alloys_stockpile` is **never decremented** even though `DEMAND_rare_alloys` exists. Un-gating
`rare_alloys` production without a consumption sink would grow its stockpile UNBOUNDED and crash its
price. See D10.

### 1.4 The GATE
- `oa_wealth_changes.txt:212`: `# debug_demand.3` (commented out).
- `oa_economy_setup.txt:2580-2581`: `#debug_demand.4`, `#debug_demand.5` (commented out).
- `debug_demand.3/.4` call `MANUFACTURE_get_all_input_availability` + `MANUFACTURE_all`, which are
  **defined nowhere** (`rg MANUFACTURE_` → only these dead call sites + 2 stale comments). `.5` calls
  `COTTAGEIND_produce_all`, which is ALSO called live elsewhere — so `.5` is redundant, not missing.

### 1.5 Price
`PRICE_factor_raw_input_costs_X` has real BOM-weighted bodies for the **same 9 goods**; the other 15
are empty stubs (`= {}`). Caller `se_GLOBALTRADE_split.txt:5866` gates on an explicit 9-good OR list
(the `is_manufactured_tradegood` call is commented out there). Dead commented duplicate stub lines at
`se_PRICE.txt:935,940,956,958,985,987,992,994`.

### 1.6 Tech gating
`INDUSTRY_unlocked_svalues.txt`: 7 goods have a placeholder `civic_tech >= 0` gate; **17 are hardcoded
`value = 0 # TODO`** (permanently locked). BUT the **real** per-good invention gates already exist in
`industrial_goods_buttons.txt` `is_valid` blocks (e.g. steel → tech_manufactories + tech_blast_furnace;
electronics/motors/petrochemicals → none yet). All referenced inventions exist in `common/inventions/`.
This mapping is the ground truth for real tech gating.

### 1.7 Employment / JOBS (verified — this EXISTS)
- `JOBS_svalues.txt`: `JOBS_industrial_workers = num_of_IND_industrial_estate`;
  `JOBS_industrial_workers_governorship` rolls it up; `JOBS_non_subsistence` sums all job categories;
  `JOBS_unemployed_pops_province = max(0, 0.5*pop − building_jobs − inverse_industrialisation*pop)`;
  `JOBS_available_slots = JOBS_buildings_cap − JOBS_num_used_slots`.
- Buildings gate on `sufficient_job_slots` (need educated pops) in their `allow`.
- **Live wage path**: `WEALTH_calculate_wages` = `JOBS_<cat>_governorship × WEALTH_average_wage_value`;
  split to `middle_strata`/`proletariat` by population share (`JOBS_wages_due_*`).
- **Dead scaffolding** (DO NOT wire — Phase-1 confirmed unwired + would double-count):
  `JOBS_set_employment_slots`, `WAGE_pay_pop_wage`, `JOBS_*_employed_*` svalues (don't exist).

### 1.8 Pop wealth + manufacturing-income distribution (the employment payoff)
- 7 governorship×stratum wealth vars (`upper_strata_wealth`…`slaves_wealth`), full quarterly
  income/expense/cost-of-living ledger + pending-change accumulator (`se_ECON_wealth.txt`).
- `trade_income_due_manufacturing` (governorship var) already flows quarterly and is distributed by
  `GT_split_distribute_income_category { category = manufacturing }`. **Current share weights**
  (`se_GLOBALTRADE_split.txt:3834`): `the_state 0.001, upper 1, middle 0.2, lower 0, proletariat 0`…
  → manufacturing wealth today goes almost entirely to the bourgeoisie, **nothing to the industrial
  proletariat**. This weight table is the single hook that routes factory income to factory workers.

### 1.9 Qing / ROW asymmetry (already the house style)
Realized in the BUILDINGS layer, culture-gated, with identical economy math underneath:
- `qing_production_buildings.txt` (silk filature, porcelain kiln, tea workshop, cotton works, salt
  yard — `country_culture_group = chinese_group`), `qing_industry_buildings.txt` (Self-Strengthening
  heavy works, e.g. Hanyang steel works).
- `row_production_buildings.txt` — TWO deliberately coarse generic buildings (`row_manufactory_building`
  + plantation) for `NOT chinese_group/jurchen`, same output/labour hooks, no per-good variants.
- No Qing-only branch inside the core wealth/jobs math; the asymmetry is purely which buildings a
  culture may raise + Qing flavor events.

---

## 2. DESIGN GOALS (restating the mandate as testable criteria)

1. **All 24 goods actually produce, consume, and price** — no permanently-dead goods (subject to tech).
2. **Raw-goods integration**: manufactured output consumes raw-good inputs (a real bill-of-materials),
   so raw and manufactured markets are coupled.
3. **Buildings integration**: production capacity is tied to on-map factory buildings (Qing named works
   + ROW generic manufactory + generic `IND_industrial_estate`), not free-floating vars.
4. **Employment integration (ESPECIALLY)**: factory output scales with EMPLOYED pops (industrial
   workforce filling factory job slots), wages/wealth flow to those worker strata, and unemployment
   responds — closing the loop pops→jobs→output→wages→wealth→consumption.
5. **Economy integration**: stockpiles/prices/wealth move REAL money and pop needs through the existing
   quarterly trade sim — one var space, not a parallel silo.
6. **Asymmetric fidelity**: Qing granular (per-good, per-province-ish, employment-linked); ROW
   abstracted (coarser, cheaper, aggregated) — for BOTH performance and integration.
7. **No new crash traps**: reuse proven idioms; every increment adversarially reviewed & boot-safe.

---

## 3. KEY DESIGN DECISIONS (the decision log proper)

### D1 — Un-gate via `GOODS_governorship_produce_industry`, NOT by reviving `MANUFACTURE_*`
**Decision.** Delete the dead `debug_demand.3/.4` events and the undefined `MANUFACTURE_*` calls.
Extend `GOODS_governorship_produce_all` to call the existing generalized macro
`GOODS_governorship_produce_industry` for every manufactured good (all 24), instead of the 4 hand-coded
blocks. This is the un-gate. **The macro adds the MECHANISED-ONLY output, not the cottage+mechanised
sum — see D1a, which is the single most important decision in this doc.**
**Why.** `MANUFACTURE_*` is defined nowhere; reviving it means inventing an entire entrypoint from a
comment. `GOODS_governorship_produce_industry` already exists, is correct, is the author's own
"new, better, less verbose" replacement (its own comment says so). Lower risk, less new code.
**Alternatives considered.** (a) Implement `MANUFACTURE_*` — rejected: more novel code, higher crash
surface, duplicates the produce loop. (b) Keep the 4 hand-coded blocks and add 20 more — rejected:
verbose, error-prone, and the macro exists precisely to avoid that.

### D1a — [REVIEW-DRIVEN, CRITICAL] Split the writers: cottage writes its own stockpile, the produce loop adds mechanised-only
**Problem the adversarial design review surfaced.** The produce loop's macro is gated on
`has_variable INDUSTRY_factories_assigned_$tradegood$` (fires ONLY where a factory is assigned) and, as
originally written, would add `GOODS_governorship_X_produced` = *(cottage + mechanised)*. But cottage
output is **already written directly to `X_stockpile`** by `COTTAGEIND_scale_production`
(`se_COTTAGEIND.txt:166-169`), which runs for the no-factory case. So routing the SUM through the
factory-gated loop would:
- **double-count cottage output** wherever a factory IS assigned (this bug is ALREADY LIVE today for the
  4 hand-wired goods clothing/luxury_clothing/machine_parts/bronze), OR
- if we "fixed" it by deleting cottage's direct write, **zero out all cottage-only (non-industrialised)
  production**.
So D1+the original D2 were mutually contradictory. This must be settled in the DESIGN, not deferred.
**Decision (chosen resolution — split the writers):**
1. **Cottage keeps its own direct stockpile write** in `COTTAGEIND_scale_production` (unchanged). It is
   the correct owner of the non-factory path and already integrates pops + raw inputs.
2. **The `produce_all`/`produce_industry` loop adds MECHANISED-ONLY output** — i.e. it adds
   `INDUSTRY_production_X` (factory rate × employment ratio, §D4a), NOT the cottage+mechanised sum. I
   will change `GOODS_governorship_produce_industry` to add a new mechanised-only svalue
   `GOODS_governorship_X_produced_mechanised` (= just the `INDUSTRY_production_X` chain), leaving the
   existing summed `GOODS_governorship_X_produced` for GUI/DEMAND read-out display only (where a single
   "total produced" figure is wanted), so no external reader breaks.
3. **Fix the pre-existing 4-good double-count as part of I2**, not later: the 4 hand-coded blocks at
   `se_GOODS.txt:1263-1283` today add the summed svalue on top of cottage's direct write. Replacing them
   with the mechanised-only macro removes that live bug.
**Result:** every governorship gets cottage output once (direct write) + mechanised output once (loop),
never twice, and cottage-only governorships keep producing. A factory-less good adds 0 via the loop
(macro's `has_variable` gate) but still produces via cottage — correct.
**Ordering fix (also review-surfaced):** `oa_wealth_changes.txt:162-163` runs `produce_all` BEFORE
`COTTAGEIND_produce_all`. With split writers this is harmless (the loop no longer reads the cottage
var). Confirmed no stale-read remains under this resolution.

### D2 — Every manufactured good gets a real mechanised produced svalue (+ keep the summed display svalue)
**Decision.** For the 15 stub/partial goods, define `GOODS_governorship_X_produced_mechanised` reading
the real `INDUSTRY_factories_assigned_X` + `INDUSTRY_production_X` chain (this is what the loop adds per
D1a), and keep/repair the summed `GOODS_governorship_X_produced = COTTAGEIND_produced_X +
INDUSTRY_production_X` for display. Fix the `industry_production_X` (lowercase, never-set) reads to the
real uppercase `INDUSTRY_production_X`. Fill the missing `INDUSTRY_production_X` rate svalues for the
mechanised goods; give cottage-eligible goods real `COTTAGEIND_produce_X` recipes (§D5).
**Why.** A good with no produced svalue is consumed but never made — a permanent shortage. Matching the
proven 9-good pattern keeps every good on one code path.
**Also fixes** (all review-confirmed):
- `naval_supplies` copy-paste bug — `GOODS_governorship_naval_supplies_produced` reads
  `INDUSTRY_factories_assigned_bronze`, should be `_naval_supplies` (`GOODS_svalues.txt:2693`).
- `glass` case-mismatch — its `limit` checks lowercase `industry_production_glass` but `add` uses
  uppercase `INDUSTRY_production_glass`, so its mechanised branch never fires (`GOODS_svalues.txt:2854`).
- **Duplicate definitions** — `GOODS_governorship_chemicals_produced` is defined twice
  (`GOODS_svalues.txt:2534` and `:2932`; last wins) and `GOODS_governorship_electronics_produced` twice
  (`:2728`, `:2910`). Delete the earlier duplicates as part of I1/I2 so each good has ONE definition,
  else D2 edits to the first copy are silently overridden. (Added to D9's dead-code list.)

### D3 — Real tech gating from the invention map that already exists
**Decision.** Replace the 16 `INDUSTRY_unlocked_X = value = 0 # TODO` and the 7 `civic_tech >= 0`
placeholders with the real per-good invention gates already encoded in `industrial_goods_buttons.txt`
`is_valid` (e.g. `INDUSTRY_unlocked_steel = { if owner has tech_manufactories AND tech_blast_furnace →
1 else 0 }`). For the 3 goods with no invention gate yet (electronics, motors, petrochemicals — all
late-industrial, out of the 1763–1900 window anyway), gate on a late civic_tech floor so they stay
locked until very late / effectively off, rather than inventing anachronistic tech.
**[REVIEW CORRECTION]** count is 16 `value = 0 # TODO` (not 17); `wooden_ships` has a gated GUI button
but NO `INDUSTRY_unlocked_wooden_ships` entry at all — D3 must ADD its unlock svalue (from the button's
`[manufactories, warships, technical_drawings]` gate), not just replace an existing stub.
**Why.** Single source of truth; the buttons and the unlock svalue must agree or the GUI lets you build
a factory that produces nothing. Uses only inventions confirmed to exist.
**Decision (recorded, best-guess):** electronics/motors/petrochemicals stay effectively out-of-era for
the 1763 start — they will be locked behind a high civic_tech floor, not deleted, so a very-late game
can still reach them. Rationale: the mod's window is 18th–19th c.; these are 20th-c. goods.

**I4 invention-gate map (extracted from `industrial_goods_buttons.txt` `is_valid`; all 15 inventions
confirmed present in `common/inventions/`):**
| good | required inventions (owner must have ALL) |
|---|---|
| clothing | tech_manufactories, tech_cotton_gin |
| luxury_clothing | tech_manufactories, tech_cotton_gin |
| furniture | tech_manufactories |
| luxury_furniture | tech_manufactories |
| construction_materials | tech_manufactories |
| machine_parts | tech_manufactories |
| alcohol | tech_manufactories, tech_bottling_and_canning |
| glass | tech_manufactories, tech_bloomery |
| bronze | tech_manufactories, tech_bloomery |
| steel | tech_manufactories, tech_blast_furnace |
| chemicals | tech_manufactories, tech_electrochemistry |
| rare_alloys | tech_manufactories, tech_electrochemistry |
| early_munitions | tech_manufactories, tech_replaceable_weapon_parts |
| late_munitions | tech_manufactories, tech_late_small_arms_manufacturing |
| naval_supplies | tech_manufactories, tech_non_food_canneries |
| steel_ships | tech_manufactories, tech_steam_powered_ships, tech_blast_furnace, tech_technical_drawings |
| wooden_ships | tech_manufactories, tech_warships, tech_technical_drawings |
| early_artillery | tech_manufactories, tech_cannons |
| late_artillery | tech_manufactories, tech_quick_firing_gun |
| pharmaceuticals | tech_manufactories, tech_antiseptic_principle |
| processed_foods | tech_manufactories, tech_bottling_and_canning, tech_antiseptic_principle |
| electronics / motors / petrochemicals | (button `always = no # TODO`) → gate on high civic_tech floor per D3 |

**I3 cottage-recipe state (from `se_COTTAGEIND.txt`):** REAL cottage recipes today = clothing,
luxury_clothing, furniture, luxury_furniture, alcohol, glass, pharmaceuticals, construction_materials,
bronze, early_munitions, naval_supplies, wooden_ships, early_artillery (13). CANNOT-BE-PRODUCED stubs =
processed_foods, motors, electronics, rare_alloys, steel, machine_parts, chemicals, late_munitions,
steel_ships, late_artillery, petrochemicals (11). I3 will add mechanised `INDUSTRY_production_X` rate
svalues for the goods that lack them, keeping heavy-industrial goods mechanised-only (cottage stub
retained, matching convention).

### D4 — Employment: factory output scales with employed industrial workforce; manufacturing wealth
reaches the workers
**Decision (two parts).**
- **4a Output ← employment.** Introduce an employment fill-ratio for the mechanised path:
  factory output is scaled by how many of the province/governorship's factory job-slots are actually
  manned by industrial-worker pops. Reuse the JOBS layer: `JOBS_industrial_workers_governorship`
  (slots) vs the industrial workforce available (proletariat + lower_strata pops, capped by slots).
  Concretely, a new svalue `INDUSTRY_employment_ratio` (governorship) = clamp( available industrial
  workforce / assigned factory slots, 0..1 ), multiplied into `INDUSTRY_production_X`. This mirrors
  how the cottage path already multiplies by `COTTAGEIND_pops_output`.
  **[REVIEW NOTE]** the numerator (proletariat+lower_strata pop counts, `ECON_svalues.txt:74-96`) and
  denominator (`JOBS_industrial_workers_governorship`, `JOBS_svalues.txt:139`) both exist — this is NOT
  hand-waved. MUST guard divide-by-zero: when assigned slots = 0 the good produces via cottage only
  (loop skipped by the `has_variable` gate), but the svalue itself must return 0 (or 1, unused) rather
  than divide — wrap in `if has_variable INDUSTRY_factories_assigned` / slots>0 check.
- **4b Wealth → workers.** Change the manufacturing income share weights
  (`se_GLOBALTRADE_split.txt:3834`) so the industrial proletariat/lower strata receive a real slice of
  `trade_income_due_manufacturing` (currently 0). Best-guess starting weights (to be tuned/reviewed):
  `upper 0.6, middle 0.25, proletariat 0.12, lower 0.03` (was upper 1 / middle 0.2 / rest 0). Keeps the
  bourgeoisie dominant (owners) but pays the workforce — the closed loop the user asked for.
  **[REVIEW NOTE — asymmetry caveat]** this weight table is the GLOBAL manufacturing share (applied in
  the country-scope share calc), so 4b reweights ROW as well as Qing. That is acceptable (it's a wealth
  DISTRIBUTION ratio, cheap, not a per-province computation) and does not violate D6's cadence
  asymmetry — but note it in the D6 review: the *distribution* rule is uniform; the *granularity* of the
  production/employment that FEEDS it is what differs Qing vs ROW.
**Why.** This is THE integration the user emphasised most ("especially employment"). It reuses the live
JOBS + wealth-distribution machinery rather than a parallel system.
**Decision (recorded, best-guess):** exact weights + the employment-ratio curve are judgement calls;
recorded here, tunable, and flagged for the adversarial review. Guardrail: never let the ratio ratchet
a 0..100 meter (see memory `no-restoring-drift-ratchet-rule`) — it's a clamp, not an accumulator.

**### D4a-concrete — [I5 IMPLEMENTATION-LOCKED] the employment-ratio formula, verified terms.**
All terms below were read on-disk before locking:
- **Denominator (labour DEMAND)** = `INDUSTRY_governorship_used_industry_slots` (INDUSTRY_svalues.txt) —
  already sums `var:INDUSTRY_factories_assigned_<good>` across ALL 24 goods, so it is the whole mechanised
  sector's factory count for this governorship. × a tunable `INDUSTRY_workers_per_factory` (NEW svalue,
  best-guess = 5) to convert factories → job slots.
- **Numerator (labour SUPPLY)** = `governorship_proletariat + governorship_lower_strata` (ECON_svalues.txt) —
  the industrial workforce pops in this governorship.
- **`INDUSTRY_employment_ratio_compute`** (governorship): if `used_industry_slots > 0` → value =
  supply ÷ (used_slots × workers_per_factory), `min = 0 max = 1`; else value = 1 (safe default; the
  `has_variable INDUSTRY_factories_assigned_X` gate on each writer means a 0-factory good never reads it,
  but the svalue must not divide by zero). It is a CLAMP, never an accumulator (guardrail above).
- **`INDUSTRY_employment_ratio`** (governorship): reads `var:industry_employment_ratio_cached` if present,
  else `INDUSTRY_employment_ratio_compute` — the exact #71 cache idiom used by
  `GOODS_governorship_bonus_to_industrial_production_from_industrialisation`.
- **Cache effect** `INDUSTRY_cache_employment_ratio` sets `industry_employment_ratio_cached` ONCE per
  governorship per quarter, called from `GOODS_governorship_produce_all` alongside the two existing caches.
- **Wiring**: append `multiply = INDUSTRY_employment_ratio` as the LAST line INSIDE each
  `GOODS_governorship_X_produced_mechanised` `if` block (all 24). By the Jomini multiply rule this scales
  the whole factory-output accumulator built up in that `if` — and CRUCIALLY stays contained to the `if`,
  so early_munitions' out-of-`if` `add = GOODS_governorship_munitions_infra_output` (supply-infra, not
  factory labour) is NOT scaled by employment. Mirrors how cottage output ×`COTTAGEIND_pops_output`.
- **D6 asymmetry**: the ratio is per-GOVERNORSHIP (identical for every good that quarter) and cached once —
  there is NO per-good employment fan-out, so ROW pays one cache write, not 24. Qing granularity comes from
  its many named-works governorships each computing their own ratio, not from a forked formula. So a single
  uniform svalue satisfies D6 (branch-free) — recorded as the best-guess resolution of "ROW coarse".
- **Best-guess constants (tunable, flagged for review + boot-test):** `workers_per_factory = 5`; linear
  clamp 0..1 (no curve). Rationale: keeps a fully-staffed sector at ratio 1 (no output change vs today) and
  only bites when pops are too few to man the assigned factories — the intended "employment gates output"
  behaviour without a magic curve.

### D5 — Raw-goods BOM: extend the cottage recipe system, don't invent a new table
**Decision.** For every manufactured good that lacks a recipe, add a `COTTAGEIND_produce_X` body (raw
inputs → output) in the existing idiom, and for the mechanised goods fill the `INDUSTRY_demand_X_<input>`
recipe svalues. Do NOT build a new data-driven BOM registry (the mod has none and two hand-coded systems
already). Recipes researched against period production (iron+coal→steel, saltpetre+charcoal+sulphur→
munitions, copper+tin→bronze, etc.).
**Why.** Consistency with the existing two systems; a refactor to a unified BOM table is out of scope
and higher-risk. Difficulty/volume is not a reason to punt (per mandate) — but reinventing the
architecture is a different, unmandated risk.
**Decision (recorded):** the 9 late-industrial goods with no sensible 18th-c. cottage recipe
(steel_ships, electronics, motors, petrochemicals, late_*) get a mechanised-only recipe gated by late
tech (per D3), with a `# CANNOT BE PRODUCED BY COTTAGE INDUSTRY` stub kept — matching the existing
convention, not a gap.

#### D5a — [I3 CONCRETE RECIPE TABLE] rates + BOM for the 15 goods that lack a mechanised chain
Every good below gets the full proven chain (`INDUSTRY_production_rate_X`, `production_bonus_X`,
`_base`, `INDUSTRY_production_X`, `_multiplier`, `_efficiency`) plus one ingredient quad
(`INDUSTRY_malus_X_<ing>` / `_demand_importance_X_<ing>` / `_base_demand_X_<ing>` /
`INDUSTRY_demand_X_<ing>`) per input, exactly mirroring the 9 built goods. The `_produced` split-writer
pair (I2 idiom) is added for each. `rate` = per-factory max output (calibrated against the built goods:
bulk/cheap goods high, big-ticket/high-tech low). `base_demand` = raw units consumed per factory;
`importance` = 0..1 malus weight (primary input 1.0, secondary lower). Inputs use ONLY confirmed
tradegood keys (raw list of 58 + manufactured intermediates steel/bronze/chemicals/glass/machine_parts/
rare_alloys). Each `INDUSTRY_demand_X_<ing>` is wired into the raw good's `DEMAND_svalues.txt`
aggregator under an `if has_variable INDUSTRY_factories_assigned_X` guard (BOM consumption integration).

**Cottage-capable (5)** — already have a `COTTAGEIND_produce_X` recipe; I3 adds the mechanised chain +
summed/mechanised split. Mechanised inputs mirror the cottage BOM (so both paths draw the same raws):

| good | rate | mechanised BOM (ing: base_demand, importance) | tech gate |
|---|---|---|---|
| construction_materials | 120 | wood:8,1.0 · stone:6,0.6 · iron:2,0.3 | tech_manufactories |
| furniture | 90 | wood:10,1.0 | tech_manufactories |
| luxury_furniture | 55 | wood:6,1.0 · silk:2,0.4 · gold:0.5,0.3 · gems:0.5,0.3 · dye:1,0.2 | tech_manufactories |
| pharmaceuticals | 40 | vegetables:6,1.0 · whales:2,0.4 | tech_manufactories, tech_antiseptic_principle |
| wooden_ships | 30 | wood:20,1.0 · copper:3,0.4 · industrial_fibres:4,0.5 | tech_manufactories, tech_warships, tech_technical_drawings |

**Mechanised-only (10)** — keep the `# CANNOT BE PRODUCED BY COTTAGE INDUSTRY` stub; add mechanised
chain + split (summed == mechanised, no cottage term). Intermediates (steel, chemicals, rare_alloys)
are built as inputs to the others, so they carry raw inputs only:

| good | rate | mechanised BOM (ing: base_demand, importance) | tech gate |
|---|---|---|---|
| steel | 90 | iron:10,1.0 · coal:6,0.7 | tech_manufactories, tech_blast_furnace |
| chemicals | 70 | sulphur:6,1.0 · coal:4,0.5 · salt:3,0.4 | tech_manufactories, tech_electrochemistry |
| rare_alloys | 35 | steel:4,1.0 · tin:2,0.4 · lead:2,0.3 · copper:2,0.3 | tech_manufactories, tech_electrochemistry |
| processed_foods | 110 | livestock:6,0.6 · vegetables:6,0.6 · fish:4,0.4 · salt:3,0.5 · glass:2,0.3 | tech_manufactories, tech_bottling_and_canning, tech_antiseptic_principle |
| late_munitions | 70 | steel:5,0.7 · chemicals:4,1.0 · lead:3,0.4 | tech_manufactories, tech_late_small_arms_manufacturing |
| late_artillery | 45 | steel:8,1.0 · machine_parts:3,0.6 · chemicals:2,0.4 | tech_manufactories, tech_quick_firing_gun |
| steel_ships | 25 | steel:20,1.0 · machine_parts:5,0.6 · coal:6,0.4 | tech_manufactories, tech_steam_powered_ships, tech_blast_furnace, tech_technical_drawings |
| motors | 30 | steel:6,0.7 · machine_parts:5,1.0 · oil:4,0.5 | HIGH civic_tech floor (out-of-era, D3) |
| electronics | 30 | rare_alloys:4,1.0 · chemicals:3,0.5 · copper:3,0.5 | HIGH civic_tech floor (out-of-era, D3) |
| petrochemicals | 60 | oil:10,1.0 · chemicals:4,0.6 | HIGH civic_tech floor (out-of-era, D3) |

**BOM ordering constraint (recorded):** steel and chemicals are inputs to several later goods
(machine_parts already demands steel/rare_alloys; late_munitions/late_artillery/steel_ships demand steel;
electronics demands rare_alloys+chemicals). Their `INDUSTRY_demand_<good>_steel` etc. wire into steel's
DEMAND aggregator — so steel/chemicals/rare_alloys must exist as producible goods FIRST. Hence the I3
implementation batching below (I3a cottage-5, then I3b intermediates steel/chemicals/rare_alloys, then
I3c the goods that consume them). Every batch is a full chain + split + demand wiring, reviewed on its own.

**Tech-gate note:** the mechanised chain does NOT itself gate on tech — the factory can only be built
where `INDUSTRY_unlocked_X` (I4) is true, and production is gated by `has_variable
INDUSTRY_factories_assigned_X`, which only exists where a factory was assigned. So I3 defines the chain;
I4 supplies the real unlock gate. The tech-gate column above is the I4 target (kept here so the two stay
in sync), not an I3 edit.

**Decision (recorded, best-guess):** all rates, base_demands, and importances are period-plausible
judgement calls, tunable in Phase 6/7 and flagged for the I3 adversarial review. They follow the built-
good calibration (clothing 150 bulk → early_artillery 60 → machine_parts 45 big-ticket) and Imperator/
Invictus convention (primary input importance 1.0). No new engine keys are invented.

### D6 — Asymmetric fidelity: Qing granular path, ROW abstracted path
**Decision.** The asymmetry lives where it already lives — the buildings + cadence, not a forked math
engine:
- **Qing (chinese_group / jurchen):** full per-good mechanised production through the Qing named works
  (`qing_production_buildings.txt` / `qing_industry_buildings.txt`), employment-scaled (D4), per-good
  prices (D7), per-governorship stockpiles. This is the granular path.
- **ROW (everyone else):** production flows through the coarse `row_manufactory_building` at
  aggregated fidelity — fewer per-good distinctions, cheaper cadence (see D-perf in Phase 7), enough to
  feed the trade/price signals Qing interacts with. No per-good employment fan-out for ROW; use a
  simpler workforce approximation.
**Why.** Matches the documented house style and is the primary performance lever. The user tied
performance AND integration to this asymmetry explicitly.
**Decision (recorded):** the split is by `country_culture_group`, reusing the existing building
`potential` gates, so no new tag-list maintenance. Where a shared svalue must branch, it branches on
culture group (the proven idiom), never on a hardcoded CHI/QNG tag.

### D7 — Prices for all producible goods
**Decision.** Write `PRICE_factor_raw_input_costs_X` bodies for every good that now has a real BOM
(from D5), and add those goods to the price-factoring OR list at `se_GLOBALTRADE_split.txt:5866`. Remove
the dead commented duplicate stub lines in `se_PRICE.txt`.
**Why.** A produced good with no input-cost price factor gets a meaningless price; the price sim must
see raw-input costs for the coupling to matter.

### D8 — Loc + GUI + comment hygiene (finish the surface)
**Decision.** Add the missing `rare_alloys` display name; replace the 17 "not yet implemented" tooltip
placeholders + the `NONE DESC` strings with real ingredient tooltips for now-producible goods; fix the
stale `#### NOT YET IMPLEMENTED ####` banner over `GT_save_final_quarterly_wealth_values` (it IS live)
and the stale `MANUFACTURE_` comment in `se_DEMAND.txt`. The 24 GUI factory buttons already render and
work at the factory-count level; verify each now shows real output once D2 lands.
**Why.** The feature is user-facing; blank/placeholder tooltips read as broken even when the math works.

### D9 — Delete dead code rather than leave it as a trap
**Decision.** Remove: `debug_demand.3/.4` (undefined calls), `GOODS_consume_industrial_demand`
(uncalled — consumption is done by the live `CONSUME_*` path), the duplicate `COTTAGEIND_produce_*`
blocks (`se_COTTAGEIND.txt` ~542-563), `GOODS_governorship_produce_manufactured`/`_manufactured_2`
(superseded by `_produce_industry`), and **the duplicate svalue definitions** (review-found):
`GOODS_governorship_chemicals_produced` at `GOODS_svalues.txt:2534` (keep `:2932`) and
`GOODS_governorship_electronics_produced` at `:2728` (keep `:2910`). Keep `debug_demand.1/.2` and `.5`
behaviour intact (`.5`'s `COTTAGEIND_produce_all` runs live already).
**Why.** Dead effects that reference undefined names are exactly the #133 crash-risk trap; removing them
shrinks the crash surface. Duplicate svalues silently override edits (D2). (Cross-checked against memory
`create_character-crash-gotcha` etc. — these are plain scripted-effect deletions, not construction-time
hazards.)

### D10 — [REVIEW-DRIVEN] Close the `rare_alloys` consumption gap
**Problem the review surfaced.** `rare_alloys` is absent from the `every_tradegood_complex` key list
(`tradegood_hypercomplex` in `zz_tradegood_injector.txt`), so `CONSUME_all_stockpiles` never decrements
`rare_alloys_stockpile`. `DEMAND_rare_alloys` exists but is never applied. Un-gating rare_alloys
production without a consumption sink → unbounded stockpile → price crash.
**Decision.** Add `rare_alloys` to the `tradegood_hypercomplex` injector list, so consumption runs for a
true all-24. **IMPLEMENTED (I5.5).**
**Regeneration hazard (discovered during I5.5).** The injector `common/scripted_effects/
zz_tradegood_injector.txt` IS machine-generated by `zz_injectormaker/`, BUT the source template
(`zz_injectormaker/tradegood_injector.txt`) does NOT contain the 24 manufactured goods at all -- not even
`steel`. All 24 MG keys were hand-added directly to the generated file. Therefore REGENERATING the
injector would DROP all 24 MG goods (destructive). The correct path is the hand-edit to the generated
`common/` file (which is what I5.5 does); a future regen is a known destructive hazard to guard against
(the MG keys must be re-added, or added to the source template + injectormaker RECIPES first). The 24 MG
goods are NOT engine tradegoods (absent from `common/trade_goods/`) -- they are variable-name keys
(`X_stockpile`), so the hand-maintained hypercomplex list IS the authoritative iteration set for them.
**Why.** Production without consumption is the exact imbalance §1 warns about, inverted; a good must have
both sides live before un-gating.

---

## 4. PHASED IMPLEMENTATION PLAN (small, reviewable increments — each gets its own adversarial review)

Each increment is independently boot-safe (produces 0 rather than crashing if a later increment is
missing) and committed only after review. **[REVIEW CORRECTION]** the original "everything inert until
I6" framing is FALSE for the 4 pre-wired goods (clothing/luxury_clothing/machine_parts/bronze), which
`GOODS_governorship_produce_all` already feeds live. So I2/I5 have LIVE effects on those 4 and must be
boot-tested there — the un-gate is a single moment only for the OTHER 20 goods. Handled by folding the
4-good migration into I2/I6 (D1a).

- **I1 — Dead-code removal + comment hygiene (D9, D8-comments) + duplicate-svalue deletion.** No
  behaviour change; shrinks crash surface first. Boot-safe by construction.
- **I2 — Split-writer for the 9 already-built goods (D1a/D2).** [CORRECTION — the earlier "refined I2"
  note here was WRONG and has been reverted. It claimed "nothing external reads the summed
  `GOODS_governorship_X_produced` svalue, so make it mechanised-only in place." That premise was a
  grep artifact: my search `GOODS_governorship_[a-z_]+_produced` silently failed to match the MACRO
  form `GOODS_governorship_$tradegood$_produced` (the `$` delimiters aren't `[a-z_]`). Re-grepping
  `GOODS_governorship_\$[a-z_]+\$_produced` CONFIRMED the summed svalue IS read by consumers:
  se_TRADE.txt (world price / global_supply), se_ECON_wealth.txt (WEALTH_generate_from_production),
  se_FUNC.txt, DEMAND_svalues.txt (DEMAND_difference_X = produced − demand), the province-window GUI
  Production tooltip, and GOODS_national_production_X. Making `_produced` mechanised-only would
  UNDERCOUNT total production for all of them — worst at the pre-industrial 1763 start where nearly
  all output is cottage. So I2 follows the design doc's original D1a exactly.]
  I2 = for the 9 built goods (clothing, luxury_clothing, bronze, machine_parts, naval_supplies,
  alcohol, glass, early_munitions, early_artillery): (a) add a new
  `GOODS_governorship_X_produced_mechanised` svalue = the factory chain only (gate on
  `has_variable INDUSTRY_factories_assigned_<good>`, `add INDUSTRY_production_<good>` × industrialisation
  bonus, plus early_munitions' arsenal/depot infra term); (b) restore `GOODS_governorship_X_produced`
  as the SUMMED total = cottage term (`add = var:COTTAGEIND_produced_X`) + the `_mechanised` svalue,
  for consumers; (c) repoint the 4 pre-wired produce-loop blocks (clothing/luxury_clothing/
  machine_parts/bronze) AND the generic `GOODS_governorship_produce_industry` macro to add the
  `_mechanised` term, fixing the live cottage double-count. Bug fixes folded in: naval_supplies gate
  (bronze→naval_supplies), glass limit (lowercase var→uppercase `INDUSTRY_factories_assigned_glass`),
  early_artillery missing mechanised branch (was cottage-only, and its cottage term was wrongly scaled
  by the industrialisation bonus — now added unscaled). **LIVE change for the 4 pre-wired goods → boot-test.**
- **I3 — Build the other 15 goods (D5): create `INDUSTRY_production_X` rate svalues + cottage recipes,
  and give each the same split-writer pair as I2 (`_produced_mechanised` = factory chain; `_produced`
  = summed cottage + mechanised)** so no good is left half-transformed. Raw-goods BOM. New goods still
  gated OFF (not in produce loop until I6). **STATUS: DONE (I3a cottage-5 + I3b intermediates-3 + I3c
  consumers-7 = all 15), each adversarially reviewed clean and committed. See REVIEW LOG.**
- **I4 — Real tech gating (D3).** `INDUSTRY_unlocked_X` from the invention map (+ add wooden_ships);
  GUI buttons already agree. **STATUS: DONE — reviewed clean, committed. See REVIEW LOG.**
- **I5 — Employment scaling (D4a): `INDUSTRY_employment_ratio` into mechanised output.** Qing granular
  / ROW coarse (D6). LIVE for the 4 pre-wired goods → boot-test their output delta.
  **STATUS: DONE — reviewed clean (all 7 criteria), committed. See REVIEW LOG.**
- **I5.5 — Close rare_alloys consumption sink (D10)** BEFORE any un-gate that could produce it.
  **STATUS: DONE — reviewed (1 CRITICAL found + fixed in same increment), committed. See REVIEW LOG.**
- **I6 — UN-GATE (D1) for the remaining 20 goods: extend `GOODS_governorship_produce_all` to all 24 via
  the mechanised-only macro.** The switch-on for the new goods. Heavily reviewed + boot-tested.
  **STATUS: DONE — reviewed CLEAN (all 7 criteria), committed. See REVIEW LOG. Boot-test owed (live economic change).**
- **I7 — Prices for all producible goods (D7).**
  **STATUS: DONE — reviewed CLEAN (all 7 criteria), committed. See REVIEW LOG. Surfaced a pre-existing
  never-refreshed-global-mean-price balance item (logged, non-blocking).**
- **I8 — Manufacturing wealth → workers (D4b): reweight manufacturing income shares.** Closes the
  employment loop.
  **STATUS: DONE — reviewed (adversarial code-review found 2 REAL latent distributor bugs + 1 doc bug,
  ALL activated — not introduced — by the reweight; all 3 fixed in-increment). See REVIEW LOG I8.**
- **I9 — Loc + GUI tooltips (D8).**
  **STATUS: DONE — reviewed adversarially (PASS, 1 LOW cosmetic finding fixed). See REVIEW LOG I9.**
- **I10 — Steel becomes cottage-capable (Phase 5 #1, D5 reversal for steel only).**
  **STATUS: DONE — design review SOUND + post-impl review CLEAN (all 7 criteria); committed. Boot-test owed.
  See REVIEW LOG I10 and §8.**
- **I11 — BOM spot-audit DEMAND-layer correctness fixes (§7.2 #3; widened to 4 edits).**
  **STATUS: DONE — design review SOUND (found the gap is systemic, added FIX C, deferred 13 to #146) +
  post-impl review CLEAN (all 6 checks); committed. Boot-test owed. See REVIEW LOG I11 and §8.**

(Order rationale: everything that only DEFINES capability lands before I6 flips on the 20 new goods;
the 4 pre-wired goods change behaviour at I2/I5 and are boot-tested there. rare_alloys' sink (I5.5)
precedes any un-gate that could produce it.)

---

## 5. RISK REGISTER (carried through review)
- **R1 quarterly perf**: adding 20 goods × per-governorship reads to the produce loop multiplies the hot
  path. Mitigation = D6 asymmetry (ROW coarse) + Phase-7 optimizations (skip near-zero stockpiles,
  cache invariants). Measured in Phase 7.
- **R2 double production**: RESOLVED in design by D1a (split writers). Cottage owns its direct
  `X_stockpile` write; the produce loop adds MECHANISED-ONLY output. A good is never added twice, and
  cottage-only governorships keep producing. This also removes the pre-existing 4-good live double-count.
  Verify in I2 review that the summed display svalue is read ONLY by GUI/DEMAND, never by a stockpile
  write.
- **R3 shortage feedback**: goods now produced but with mis-scaled DEMAND could swing prices/wealth
  wildly. Mitigation: conservative starting rates; review price/wealth deltas.
- **R4 boot crash**: any undefined var/effect reference. Mitigation: static scan each increment; the
  branch is the isolation.

---

## 6. REVIEW LOG
- **Phase 1 (research):** complete — two agents mapped production/consumption/price/tech/loc/GUI and
  employment/pops/wealth/Qing-ROW; findings folded into §1. Core code paths independently re-verified
  by direct read (produce loop, cottage recipe, JOBS svalues, manufacturing income weights).
- **Phase 2 (design):** adversarial design review COMPLETE (code-review agent, verified all 8 crux
  claims against the tree). Outcome — 1 CRITICAL + 1 HIGH + 3 MEDIUM + verified-clean foundations:
  - **CRITICAL:** D1+original-D2 contradictory (factory-gated macro can't carry a cottage+mechanised
    sum without double-count or zeroing cottage-only). → RESOLVED by new **D1a (split writers)**; R2
    downgraded to resolved.
  - **HIGH:** `rare_alloys` never consumed (absent from injector list) → unbounded stockpile on un-gate.
    → RESOLVED by new **D10** + new increment **I5.5** (close sink before any un-gate).
  - **MEDIUM:** duplicate `chemicals`/`electronics` produced svalues (last wins, silently override D2
    edits) → added to **D9** deletion list. `glass` case-mismatch never fires → added to **D2** fixes.
    "single un-gate moment" false for 4 pre-wired goods → **§4** corrected (I2/I5 live for those 4).
  - **Verified CLEAN (foundations sound):** `GOODS_governorship_produce_industry` exists+correct+uncalled;
    `CONSUME_all_stockpiles` live (23/24); manufacturing weight table at `:3834` as claimed (global — D4b
    note added); JOBS layer real (D4a buildable, div-0 guard noted); invention gates + inventions exist
    (D3 buildable, +wooden_ships gap); `MANUFACTURE_*` undefined everywhere (D9 safe); naval_supplies bug
    confirmed.
  Design updated to incorporate ALL findings. Design is now internally consistent → cleared for Phase 3.
- **Phase 3 / I1 (dead-code removal + comment hygiene):** IMPLEMENTED + adversarially reviewed CLEAN
  (no-behaviour-change verified). Changes: deleted 3 duplicate `GOODS_governorship_X_produced` svalues
  (rare_alloys/chemicals/electronics — kept the effective later copies, PDX last-wins); deleted
  `debug_demand.3/.4` (undefined `MANUFACTURE_*`, call-sites already commented); deleted uncalled
  `GOODS_consume_industrial_demand` + `GOODS_governorship_produce_manufactured`/`_2` (also empty-`if`
  buggy); deleted 3 duplicate empty `COTTAGEIND_produce_*` stubs; refreshed stale MANUFACTURE_/NOT-YET-
  IMPLEMENTED comments. Brace-balanced, zero dangling refs. Review confirmed all 5 no-op; one LOW
  advisory (rare_alloys/chemicals dropped copies carried an already-shadowed cottage contribution —
  moot, both are mechanised-only per D5 and their cottage recipes are CANNOT-BE-PRODUCED stubs).
- **Phase 3 / I2 (split-writer for the 9 built goods, D1a + 3 bugfixes):** IMPLEMENTED + adversarially
  reviewed CLEAN (all 8 criteria). Reversed the earlier flawed "mechanised-only in place" approach —
  its premise ("nothing external reads the summed svalue") was a grep artifact that missed the
  `GOODS_governorship_$tradegood$_produced` MACRO form. For each of the 9 built goods added a
  `_produced_mechanised` (factory chain only; early_munitions keeps its arsenal/depot infra term) and
  restored `_produced` as the SUMMED total (cottage + mechanised) read by consumers (se_TRADE world
  price, se_ECON_wealth, se_FUNC, DEMAND_difference, province GUI, GOODS_national_production). Repointed
  the 4 pre-wired produce-loop blocks + the generic `produce_industry` macro to add the `_mechanised`
  term (fixes live cottage double-count). Bugfixes: naval_supplies gate (bronze→naval_supplies), glass
  case-mismatch limit, early_artillery cottage term now added UNSCALED (was wrongly ×industrialisation).
  Committed `2a1860181`, pushed. **LIVE for those 4 pre-wired goods → boot-test owed.**
- **Phase 3 / I3a (5 cottage-capable goods — full chains + BOM):** IMPLEMENTED + adversarially reviewed
  CLEAN (all 8 criteria). Built mechanised chains + I2 split-writer pairs + raw-goods BOM for
  construction_materials, furniture, luxury_furniture, pharmaceuticals, wooden_ships (whose mechanised
  branch was previously dead — read never-set lowercase `var:industry_production_X`). Introduced
  `tools/gen_mg_chains.py` as the CANONICAL data-driven MG-chain generator (RECIPES = doc D5a); extend
  RECIPES, never hand-copy a chain. Goods defined but still gated OFF (produce loop deferred to I6).
  Committed `4b64225d4`, pushed.
- **Phase 3 / I3b (3 mechanised-only intermediates — steel/chemicals/rare_alloys):** IMPLEMENTED +
  adversarially reviewed CLEAN (all 8 criteria). Generated full chains (gen_mg_chains.py i3b) + split-
  writer pairs (`_produced` = `value = X_produced_mechanised` wrapper, no cottage term — these have no
  cottage recipe) + 9 BOM consumption adds: steel→{iron,coal}, chemicals→{sulphur,coal,salt},
  rare_alloys→{steel,tin,lead,copper}. DEMAND_coal gains TWO adds (steel+chemicals); DEMAND_steel gains
  rare_alloys as an intermediate-input consumer. Static-verified: braces balanced on all 5 touched files,
  all 9 `INDUSTRY_demand_*` refs defined, each split-pair defined once, no live dead lowercase var refs.
  **Whitespace incident (fixed):** a Python whole-file rewrite of DEMAND_svalues.txt normalized CRLF→LF,
  producing an 8k-line phantom diff; reconverted to CRLF (repo convention) → clean 62-line insert.
  Review MEDIUM/PLAUSIBLE finding: I3b ships the CONSUMPTION half while PRODUCTION (produce-loop stockpile
  write) + factory-assignment are deferred to I6 — so the DEMAND adds evaluate to 0 today (factories=0,
  inert) and the steel-shortage-throttles-rare_alloys coupling can't bite until I6/I5.5. This is the
  §4 ordering boundary by design; **DEPENDENCY logged: I5.5 (close rare_alloys sink) + I6 (un-gate =
  produce-loop wiring) MUST land together so supply and demand ship as one — do NOT un-gate any of these
  3 without their produce-loop output.** Committed + pushed.
- **Phase 3 / I3c (7 mechanised-only consumer goods — full chains + BOM):** IMPLEMENTED + adversarially
  reviewed CLEAN (all 7 criteria, no defects). Built mechanised chains + split-writer pairs + raw-goods
  BOM for processed_foods, late_munitions, late_artillery, steel_ships, motors, electronics,
  petrochemicals (each previously a DEAD `_produced` stub reading never-set lowercase
  `var:industry_production_X`; late_artillery also carried a cottage term whose recipe is a
  CANNOT-BE-PRODUCED stub — dropped as a no-op). All 7 `_produced` = `value = X_produced_mechanised`
  wrappers (no cottage). 22 BOM adds wired across 13 aggregators (chemicals+4, steel+4, machine_parts+3,
  oil+2, singles elsewhere) — several ingredients are themselves MG intermediates (steel, chemicals,
  rare_alloys, machine_parts, glass); the full MG dependency graph is a verified DAG (no cycles) and
  demand depends on factory COUNTS not instantaneous production, so no circular script_value eval.
  Food-ingredient aggregators (livestock/vegetables/fish) have no elasticity multiply → adds anchored
  before `min = 0` instead. All edits CRLF-preserving. Static: braces balanced on 4 files, all 22 refs
  defined+wired once, split-pairs once each, no live dead-var reads. Review non-findings (both
  pre-existing/cosmetic, not introduced): DEMAND_chemicals lacks a trailing `min = 0`; I3b rare_alloys→
  steel add has extra leading tabs (whitespace-insensitive). Goods defined but still gated OFF (produce
  loop → I6). Committed + pushed.
- **Phase 3 / I4 (real tech gating, D3):** IMPLEMENTED + adversarially reviewed CLEAN (all 5 criteria,
  no defects). Rewrote `INDUSTRY_unlocked_svalues.txt` so each `INDUSTRY_unlocked_X` MIRRORS its
  `industrial_goods_buttons.txt` `is_valid` invention AND-gate exactly (single source of truth; the
  svalue was previously DEAD — no consumer repo-wide — as 7 `civic_tech >= 0` always-true + 16
  `value = 0 # TODO` always-locked placeholders). 21 goods → bare `invention = tech_X` AND-gates at
  country scope (button's `owner={}` wrapper dropped since the svalue is already country-scoped); ADDED
  the missing `INDUSTRY_unlocked_wooden_ships` (23→24 defs). electronics/motors/petrochemicals kept as
  `value = 0` mirroring their buttons' `always = no` (20th-c., out of the 1763-1900 window — locked, not
  deleted). Buttons NOT touched (they already gate correctly; the province GUI enables via each button's
  own `IsValid`). Verified: all 24 defs unique, every good↔invention pairing correct (no swaps — glass/
  bronze/steel/steel_ships/wooden_ships/processed_foods stress-checked), all 15 inventions exist, braces
  balanced, UTF-8-BOM+CRLF preserved (`file` confirmed). Inert until I6 reads it as the un-gate authority.
  **Best-guess decision recorded:** D3 floated a "high civic_tech floor" for the 3 out-of-era goods, but
  the mod has NO established civic_tech scale to anchor a floor against (no invention gates on civic_tech
  anywhere), and un-`always=no`-ing their buttons is a balance call better made with boot-test in the
  loop — so they stay hard-locked (`value = 0`) for now; revisit if a late-game reach is wanted.
  Committed + pushed.
- **Phase 3 / I5 (employment scaling, D4a):** IMPLEMENTED + adversarially reviewed CLEAN (all 7 criteria,
  0 defects). Factory output now scales by an employment fill-ratio = clamp( (governorship_proletariat +
  governorship_lower_strata) / (INDUSTRY_governorship_used_industry_slots x INDUSTRY_workers_per_factory),
  0, 1 ), mirroring how the cottage path scales output by pop counts. Added 3 svalues to
  INDUSTRY_svalues.txt (`INDUSTRY_workers_per_factory = 5` best-guess; `INDUSTRY_employment_ratio_compute`
  = the clamped ratio, div-0-guarded by `if limit = { used_industry_slots > 0 }`, default `value = 1` when
  no factories; `INDUSTRY_employment_ratio` = #71 cache wrapper reading `var:industry_employment_ratio_cached`
  else recomputing inline -> missing cache degrades to correctness never zero). Added
  `INDUSTRY_cache_employment_ratio` effect to se_GOODS.txt + its call in `GOODS_governorship_produce_all`
  BEFORE the produce loop (after the 2 sibling caches). Wired `multiply = INDUSTRY_employment_ratio` as the
  LAST line INSIDE all 24 `GOODS_governorship_X_produced_mechanised` if-blocks -- verified contained: for
  early_munitions the arsenal/depot `add = ...munitions_infra_output` sits OUTSIDE the if and is correctly
  NOT employment-scaled. Review confirmed: (1) accumulator-containment correct incl. early_munitions;
  (2) div-0 impossible (guard + workers_per_factory=5 constant); (3) fresh clamp not ratchet
  (no-restoring-drift rule); (4) cache set-before-read, per-governorship scope, overwritten each quarter,
  same one-quarter-stale lifecycle as the 2 existing caches (no new staleness class); (5) `value =`-inside-if
  reset idiom verified against ~30 codebase precedents (WEALTH/INCOME/MIGRATION/CURRENCY/etc.); (6) all
  referenced terms exist + governorship-scoped; (7) braces balanced, no duplicate defs, BOM/CRLF preserved
  (line-1 BOM on GOODS_svalues.txt restored -- HEAD had it). **1 LOW design-consistency note (recorded, no
  action): ingredient DEMAND (`INDUSTRY_demand_X_<ing>` = factory COUNT x base) is NOT employment-scaled
  while OUTPUT is -- an under-manned sector draws full inputs but yields reduced output, a latent balance
  quirk (may drive ingredient shortages a symmetric model wouldn't). Defer symmetric input-scaling to a
  balance pass / Phase 6; noted here so it is not lost.** Committed + pushed. LIVE for the 4 pre-wired goods
  -> boot-test their output delta.
- **Phase 3 / I5.5 (close rare_alloys consumption sink, D10):** IMPLEMENTED + adversarially reviewed;
  review found **1 CRITICAL prerequisite, FIXED IN THE SAME INCREMENT** before commit. The core edit adds
  `rare_alloys` to the `tradegood_hypercomplex` list in `zz_tradegood_injector.txt` (it was the ONLY one
  of 24 MG goods missing) -- that list is the expansion set for `every_tradegood_complex`, so
  `CONSUME_all_stockpiles` now decrements `rare_alloys_stockpile` by `DEMAND_rare_alloys` each quarter
  (sink closed). Verified: block byte-identical in shape to the 23 siblings; rare_alloys appears exactly
  once; `DEMAND_rare_alloys` (DEMAND_svalues.txt:1821, min=0, non-negative) + `rare_alloys_stockpile`
  init (se_GOODS.txt:87) both exist; the shortage `divide` is min=0.001-guarded (no div-0). **CRITICAL the
  review surfaced:** `every_tradegood_complex` has ~40 callers (not just CONSUME); the QUARTERLY WEALTH
  loop `WEALTH_generate_from_production` reads `WEALTH_$tradegood$_durability` templated, but
  `WEALTH_rare_alloys_durability` was UNDEFINED (rare_alloys was the sole MG good missing it) -> once
  rare_alloys entered the shared iterator, every governorship would log an undefined-svalue error each
  quarter + zero rare_alloys wealth (a NEW flood -- exactly the bug-class I5.5 exists to fix, in a
  different iterated set). FIX: added `WEALTH_rare_alloys_durability = { value = 0.95 }` (mirrors durable
  metal siblings steel/machine_parts/bronze) to WEALTH_svalues.txt in the same commit. Also verified the
  reviewer's secondary flag: `global_base_import_price_rare_alloys` is auto-seeded by the SAME
  `every_tradegood_complex` loop (se_GLOBALTRADE_split.txt:5915 / GT_split price effect), so it is
  consistent (not zero); rare_alloys appended LAST preserves the "raw goods before manufactured" ordering
  assumption (se_GLOBALTRADE_split.txt:5864) and it is correctly absent from the I7-scope
  `PRICE_factor_raw_input_costs` list. **Regeneration hazard confirmed + recorded in D10:** the injector
  is machine-generated but its source template lacks all 24 MG goods, so a regen would drop them -- the
  hand-edit to the generated `common/` file is the correct path. Static: injector braces 150/150 (+2),
  WEALTH braces 406/406 (+3), both BOM+CRLF preserved. Committed + pushed. Sink + wealth-parity closed;
  rare_alloys is now safe to un-gate at I6.
- **Phase 3 / I6 (UN-GATE the remaining 20 manufactured goods, D1):** IMPLEMENTED + adversarially
  reviewed CLEAN (all 7 criteria, no defects). Added 20 `GOODS_governorship_produce_industry =
  { tradegood = X }` calls to `GOODS_governorship_produce_all` (se_GOODS.txt), immediately after the 4
  pre-wired blocks, for: steel, chemicals, rare_alloys (intermediates I3b); construction_materials,
  furniture, luxury_furniture, pharmaceuticals, wooden_ships (cottage-capable I3a); alcohol, glass,
  processed_foods, naval_supplies, early_munitions, late_munitions, early_artillery, late_artillery,
  steel_ships, motors, electronics, petrochemicals (consumers/other I2+I3c). The generic macro
  (defined but previously UNCALLED) adds the MECHANISED-ONLY term to `X_stockpile`, gated on
  `has_variable = INDUSTRY_factories_assigned_X` — the split-writer (D1a) so cottage output
  (written directly by COTTAGEIND_scale_production) is never double-counted. Ships together with I5.5
  (rare_alloys sink) so supply + demand arrive as one increment (the I3b DEPENDENCY note is satisfied).
  Prerequisites verified per good before wiring: `_produced_mechanised` svalue defined (24/24 in
  GOODS_svalues), factory-assign var + GUI assign button (24/24 in industrial_goods_buttons.txt),
  I4 tech gate (INDUSTRY_unlocked_X), I3 raw-goods BOM (DEMAND aggregators), and a consumption sink
  (CONSUME_all_stockpiles, 24/24 after I5.5). **Inert-at-0-factories confirmed by review** — the
  genuine guarantee is that `INDUSTRY_production_X` (and hence `_produced_mechanised`) evaluates to 0
  when no factory is assigned, NOT merely the `has_variable` gate; so even where the assign-var is
  seeded to 0 at setup, the add is 0. No div-by-zero. Macro equivalence to the 4 pre-wired
  `GOODS_governorship_produce` blocks verified (same gate semantics, same mechanised svalue, same
  scope). Static: braces 395/395 (+20), BOM+CRLF preserved, clean +35 insert diff.
  **Review-surfaced BACKLOG (pre-existing, NOT introduced by I6, non-blocking):** newly-spawned
  countries (revolts/colonies/new tags via `FUNC_setup_new_country`) double-seed governorship
  stockpiles at t=0 — `GOODS_setup_governorship_stockpiles` (se_FUNC.txt:492) and
  `FUNC_every_governorship_update_tradegood_stockpiles` (se_FUNC.txt:522) fire back-to-back. Game-start
  countries seed via the mutually-exclusive global-flag path (oa_economy_setup.txt:381) and are
  single-seeded (unaffected). It is a one-time t=0 value error, not a recurring quarterly double-count.
  Also noted: `setup_main_effect` (se_setup.txt) is dead/orphaned (zero callers). Both logged for a
  later increment; neither touches I6's correctness. **LIVE economic change → boot-test owed.** Committed + pushed.
- **Phase 3 / I7 (prices for all producible goods, D7):** IMPLEMENTED + adversarially reviewed CLEAN
  (all 7 criteria, no defects). Filled the 15 empty `PRICE_factor_raw_input_costs_X = {}` stubs with real
  BOM-weighted bodies (construction_materials, furniture, luxury_furniture, pharmaceuticals, wooden_ships,
  steel, chemicals, rare_alloys, processed_foods, late_munitions, late_artillery, steel_ships, motors,
  electronics, petrochemicals) and added those 15 to the OR gate at se_GLOBALTRADE_split.txt:5871 that
  guards `PRICE_factor_raw_input_costs_$tradegood$ = yes` (was a hardcoded 9-good list; the
  `is_manufactured_tradegood` call there stays commented). All 24 MG goods now price their inputs.
  **Canonical-generator path:** extended `tools/gen_mg_chains.py` with `price_body()` + a `price` mode
  emitting bodies from the SAME RECIPES dict that drives the production chains and the
  `INDUSTRY_demand_importance_<good>_<input>` weights — no hand-copy. rare_alloys had NO prior stub (a
  post-hoc good), so its body was appended before the raw-goods stub block; the other 14 replaced their
  stubs in place. Deleted 9 dead commented-out duplicate stub lines (the goods that already had bodies).
  Bodies are shape-identical to the 9 hand-built ones: `add = { value = global_mean_price_<input>
  min = 0.001 multiply = INDUSTRY_demand_importance_<good>_<input> }` per input, `multiply =
  PRICE_input_goods_scale_factor` (=0.1) last. **Ordering/circularity CLEARED (independently traced +
  review-confirmed):** bodies read `global_mean_price_<input>` — a persistent GLOBAL var computed for
  ALL tradegoods (incl. manufactured, via the every_tradegood_complex injector list) in a SEPARATE
  averaging pass (`PRICE_update_all_global_mean_prices`), NOT the in-progress `local_price`. So MG-
  consuming-MG chains (electronics->rare_alloys, motors/steel_ships/late_*->steel/machine_parts/chemicals,
  petrochemicals->chemicals) read a stable prior snapshot; intra-loop good ordering is moot and the
  "raw first" comment is over-cautious for the global-mean approach. Cold-start safe: on the day-0 setup
  tick, `PRICE_update_TZ_prices` (oa_economy_setup.txt:2360) zero-inits + computes every mean BEFORE the
  first `GT_split_do_global_trade_split` (:2449) reads it — writer-before-reader, same tick; `min=0.001`
  prevents div-0/negative. No `INDUSTRY_demand_importance` ref undefined (all built in I3), no double-
  application (single call per good per loop via the gate), generated bodies free of the original
  luxury_clothing copy-paste bug (each input multiplies its OWN weight). Static: se_PRICE braces 303->370
  (+376/-23), se_GLOBALTRADE_split 1613/1613 (+19), both BOM+CRLF preserved.
  **BACKLOG (pre-existing, NOT introduced by I7, non-blocking, balance not correctness):** `global_mean_price_*`
  is written ONCE at day 0 and never refreshed — `PRICE_update_TZ_prices` has only the one-time
  `done_trade_startup`-gated setup call plus two dead event call-sites (trade.1/trade.2, unreferenced).
  So every quarter's input-cost factoring reads the frozen day-0 mean forever. Affects all 24 MG goods
  identically (the 9 originals too) — a property of the existing price subsystem, flagged for a later
  refresh/balance decision. **LIVE economic change → boot-test owed.** Committed + pushed.
- **Phase 3 / I8 (manufacturing wealth → workers, D4b):** IMPLEMENTED + adversarially reviewed.
  **Change:** reweighted the `GT_split_calculate_trade_shares category = manufacturing` per-capita share
  table (se_GLOBALTRADE_split.txt:3834) from `the_state 0.001, upper 1, middle 0.2, lower 0, proletariat 0`
  to `the_state 0.001, upper 0.6, middle 0.25, lower 0.03, proletariat 0.12` (rest 0). These are per-capita
  relative weights (each × stratum pop, summed, normalised to shares totalling 1 PER category), so
  resource_extraction/shipping are untouched; the ratios give factory owners the dominant per-capita cut
  while routing a real slice to the industrial workforce (proletariat + lower_strata) whose pop count also
  scales output via `INDUSTRY_employment_ratio` (I5) — this closes the employment→output→wages loop end to end.
  **Adversarial review (code-review agent) REFUTED my pre-review claim** that "there is no separate
  proletariat_wealth var; proletariat income folds into lower_strata_wealth harmlessly." It found — and I
  independently re-verified on disk — that `proletariat_wealth` is a LIVE, load-bearing var (credited by
  `JOBS_wages_due_proletariat` at se_ECON_wealth.txt:1098, generated production/services :910, growth :114,
  setup floor :56; read by WEALTH_svalues.txt:270-272/437, province_window.gui, cost_of_living_events.txt,
  DEMAND_luxury_svalues.txt). Turning the proletariat weight from 0→0.12 ACTIVATED two latent distributor
  bugs (both pre-existing copy-paste errors that were inert only because every category's proletariat share
  was 0):
    - **FINDING 1 (HIGH) — income mis-credit:** `GT_split_distribute_income_category`'s proletariat block
      (~3971) wrote `name = lower_strata_wealth` (copied from the lower_strata block) instead of
      `proletariat_wealth`. FIXED → `proletariat_wealth`.
    - **FINDING 2 (MEDIUM/HIGH) — expense-floor clobber:** `GT_split_distribute_expenses_category`'s
      proletariat floor guard (~4116) tests `var:proletariat_wealth < WEALTH_starting_proletariat_half` but
      its corrective `set_variable` wrote `name = lower_strata_wealth`. FIXED → `proletariat_wealth`.
      (The expense DEBIT just above, 4113, already correctly targets proletariat_wealth; only the floor was wrong.)
    - **FINDING 3 (LOW) — my false doc comment:** the NOTE I'd added at the weight table asserting "no separate
      proletariat_wealth var" was wrong. CORRECTED to state each stratum's income routes to its own wealth var.
  **Decision (Option A, best-guess per autonomy mandate):** make proletariat income + expense + floor all
  target `proletariat_wealth`, symmetric with every sibling stratum AND with the wages path — rather than
  Option B (fold proletariat into lower_strata everywhere), which would have contradicted the wages-side
  crediting and the GUI reads. This is a self-consistent single-var-per-stratum model. Because
  resource_extraction/shipping keep `proletariat = 0`, all three fixes are provable no-ops there; they take
  effect only under I8's nonzero manufacturing share. **This is a validation of the mandated adversarial-review
  pipeline — a plausible-sounding pre-review assumption was refuted before commit and prevented shipping a
  silent proletariat_wealth drain.** Static: braces 1613/1613, BOM+CRLF preserved, clean +29/-7 diff.
  **LIVE economic change → boot-test owed.**
- **Phase 3 / I9 (loc + GUI factory tooltips, D8):** IMPLEMENTED + adversarially reviewed CLEAN
  (code-review agent, PASS; 1 LOW cosmetic finding found + fixed). Two loc files:
  **(1) localization/english/industry_l_english.yml** — the province-window factory tooltip is a
  macro-assembled string; each producible good needs one `PROVWINDOW_GOV_<GOOD>_PRODUCED_TT` body plus
  one `ind_<good>_ingredient_<ing>` submacro per ingredient. 7 goods were hand-built (clothing,
  luxury_clothing, bronze, machine_parts, naval_supplies, alcohol, early_munitions); the other 17 were
  stubbed as `"...This industry is not yet implemented"` placeholders. Replaced all 17 placeholders with
  real macro tooltips (furniture, luxury_furniture, glass, pharmaceuticals, processed_foods, motors,
  electronics, rare_alloys, construction_materials, steel, chemicals, late_munitions, steel_ships,
  wooden_ships, early_artillery, late_artillery, petrochemicals), byte-identical in shape to the 7
  hand-built ones. **Canonical-generator path:** new `tools/gen_industry_tooltips.py` (GOODS dict:
  good -> title + ordered ingredient list). The ingredient lists were derived from the ground-truth
  `INDUSTRY_base_demand_<good>_<ing>` svalues (so they never drift from the production chains), then the
  generator was validated to confirm every one of the 3 svalue families it references
  (`INDUSTRY_base_demand`/`INDUSTRY_malus_*_production`/`INDUSTRY_demand_importance`) plus the frame reads
  (`GOODS_governorship_<good>_produced`, `INDUSTRY_production_<good>[_efficiency]`,
  `INDUSTRY_production_rate_<good>`, `INDUSTRY_<good>_factories`) and the `add_<good>_button` scripted GUIs
  all resolve on disk — ALL 17 goods clean, no dangling refs. Note glass + early_artillery are PRE-EXISTING
  goods (not in gen_mg_chains.py RECIPES); their ingredient sets (glass=coal/stone/lead;
  early_artillery=sulphur/wood/stone/lead/textile_fibres/iron/steel/bronze/livestock) were read from their
  own svalues, not assumed. **(2) localization/english/imp19c_tradegoods_l_english.yml** — filled the 7
  `NONE DESC` placeholder descriptions (steel_ships, wooden_ships, petrochemicals, early_munitions,
  late_munitions, early_artillery, late_artillery) with period-appropriate house-style text, and added the
  missing `rare_alloys` NAME + DESC (it had neither). All 24 MG goods now have NAME + DESC.
  **Review finding (LOW, fixed):** wooden_ships DESC used a `\'` backslash-escaped apostrophe — the ONLY
  one in the whole loc dir; Paradox loc renders `\'` as a literal backslash, so changed to a bare `'`
  (matching the 1430 other possessives). Static: industry_l_english.yml 24 PRODUCED_TT (was 7 real + 17
  placeholder), 0 placeholders left, 0 dangling `$macro$` refs, 0 duplicate keys, CRLF preserved;
  imp19c_tradegoods 0 `NONE DESC` left (bar 2 commented fallback lines), LF preserved; both BOMs intact
  (one double-encode slip caught + repaired before review). **Cosmetic/GUI-only change — no economic
  behaviour; boot-safe. Boot-test owed (visual verify tooltips render).**
- **Phase 5 / I10 (steel becomes cottage-capable — crucible/blister artisan path, D5 reversal for steel
  ONLY):** IMPLEMENTED + adversarially reviewed at BOTH stages. **Design review (code-review agent) verdict
  SOUND** — ship the 3-edit plan as designed; efficiency 0.35 is defensible/conservative (cottage steel is
  ~4 orders of magnitude below one factory's output, so it never rivals the Bessemer volume path); it flagged
  1 MEDIUM implementation trap (a substring comment-fix on "No cottage recipe for steel" would ALSO hit the
  `steel_ships` comment at GOODS_svalues.txt:2753), which I avoided by editing via an exact multi-line anchor.
  **Change (3 edits):** (1) `se_COTTAGEIND.txt` — cached `COTTAGEIND_raw_coal = GOODS_governorship_coal_produced`
  in `COTTAGEIND_cache_all_values` right after `COTTAGEIND_raw_iron` (coal had no prior COTTAGEIND reader; a
  read-only capacity proxy like every sibling raw var); (2) same file — replaced the `COTTAGEIND_produce_steel`
  "CANNOT BE PRODUCED" stub with a real recipe (`set COTTAGEIND_produced_steel = var:COTTAGEIND_raw_iron`,
  `add var:COTTAGEIND_raw_coal`, `COTTAGEIND_scale_production = { output = steel efficiency = 0.35 }`) —
  structurally identical to the bronze / construction_materials idiom; (3) `GOODS_svalues.txt` — the
  `GOODS_governorship_steel_produced` summed writer gained the D1a cottage branch (`value = 0; if has_variable
  = COTTAGEIND_produced_steel { add = var:COTTAGEIND_produced_steel }; add = _mechanised`), byte-identical in
  shape to construction_materials, and the stale "No cottage recipe for steel" comment was rewritten.
  **Post-impl review (code-review agent) CLEAN** — all 7 criteria pass, no CRITICAL/HIGH/MEDIUM: (A) recipe
  structurally identical to bronze/construction_materials, `output = steel` correct, scale writes
  `COTTAGEIND_produced_steel` + `steel_stockpile`; (B) no double-count — `steel_stockpile` gets exactly the
  cottage direct write + the `_mechanised`-only produce-loop add (gated on `INDUSTRY_factories_assigned_steel`);
  the summed `GOODS_governorship_steel_produced` is read only by price/demand/wealth/GUI + the one-time init
  seed, never a quarterly stockpile add; (C) summed-writer edit shape-identical to construction_materials, no
  typo; (D) the `steel_ships` comment at :2753 confirmed UNTOUCHED (trap avoided); (E) `GOODS_governorship_coal_produced`
  exists (GOODS_svalues.txt:1525), coal cached FIRST in produce_all (cache runs before produce_steel), no
  duplicate `COTTAGEIND_raw_coal` set; (F) braces balanced (se_COTTAGEIND 137/137, GOODS_svalues 909/909),
  BOM+CRLF intact, both raw vars cached before use; (G) efficiency 0.35 present, recipe reachable
  (`COTTAGEIND_produce_steel = yes` in produce_all line 18). **1 LOW (pre-existing, out of scope, NOT a
  regression):** the `steel` trade_goods engine key is absent from `common/trade_goods/` — true of ALL
  manufactured goods (bronze/clothing/etc.); the whole MG path is variable-based (`steel_stockpile`,
  svalue names) and never calls `trade_goods = steel` / `set_trade_goods`, so this is the known half-wired
  condition tracked in memory `imp19c-manufactured-goods-risk`, not introduced here. **LIVE economic change
  → boot-test owed (verify artisan steel is a trickle, does not flood pre-Bessemer, does not trivialise the
  factory unlock).** Committed + pushed.
- **Phase 5 / I11 (BOM spot-audit — DEMAND-layer correctness fixes; §7.2 #3):** IMPLEMENTED + adversarially
  reviewed at BOTH stages. **Design review** verified the plan CORRECT but INCOMPLETE — the glass-demand gap
  is not unique, it is SYSTEMIC. A five-layer BOM audit (cottage / mechanised svalue / INDUSTRY factory
  demand / DEMAND aggregator / price / tooltip) of chemicals/glass/naval_supplies showed the INDUSTRY, price,
  and tooltip layers AGREE per good, but the DEMAND-aggregator layer had two defect classes; a completeness
  sweep across ALL goods found their full extent. **4 edits, all in `DEMAND_svalues.txt`:**
  - **FIX A (CLASS A — dangling ref, unique repo-wide):** `DEMAND_bronze` added `INDUSTRY_naval_supplies_parts_bronze`,
    a name defined NOWHERE (undefined-svalue log flood + zero bronze demand for naval yards, the I5.5 bug-class).
    Renamed to `INDUSTRY_demand_naval_supplies_bronze` (INDUSTRY_svalues.txt:1113), matching the 3 sibling
    naval_supplies ingredient adds. This is the ONLY CLASS-A instance in the file (all 79 other `add = INDUSTRY_*`
    tokens resolve).
  - **FIX B1/B2 (CLASS B — defined-but-unconsumed, target aggregator exists):** `INDUSTRY_demand_glass_coal`
    (INDUSTRY_svalues.txt:1439) and `_glass_stone` (:1466) were defined + well-formed + real inputs (production
    malus present) but consumed by ZERO aggregator — only glass_lead was wired. Added the standard
    `if has_variable = INDUSTRY_factories_assigned_glass { add = INDUSTRY_demand_glass_<coal|stone> }` branches to
    `DEMAND_coal` (after steel_ships, after the mid-block ×0.3/×3 partial multiplies so it's unscaled like every
    factory sibling) and `DEMAND_stone` (no mid-block multiply; before the elasticity tail).
  - **FIX C (CLASS B, folded in by the design review):** `INDUSTRY_demand_early_artillery_textile_fibres`
    (INDUSTRY_svalues.txt:1905) — same class, target `DEMAND_textile_fibres` exists. Added as a flat factory
    sibling after the early_munitions branch (NOT swept into the luxury_clothing/clothing cottage branches'
    ×2/×3 multiplies). **Pre-existing systemic bug noted in-code + out of scope:** the entire early_artillery
    demand block drives off `INDUSTRY_early_munitions_factories` (copy-paste from the early_munitions chain),
    not the early_artillery factory count; FIX C's gate (`assigned_early_artillery`) vs scaling driver
    (early_munitions) is mismatched exactly like its 7 already-wired siblings, so it introduces NO new behaviour
    vs baseline. Logged for a later dedicated fix.
  **Scope decision (best-guess, per autonomy mandate):** I11 fixes ONLY proven WIRING defects, not ingredient
  COMPOSITION. The §7.1/§7.6 historical mismatches (chemicals wants saltpetre; glass wants silica sand/soda/lime;
  naval_supplies wants timber/tar/pitch/hemp/canvas) reference raw goods ABSENT from the live good set
  (`common/trade_goods/00_imp19c.txt`, 58 keys — design review independently confirmed saltpetre/silica/soda/
  lime/tar/pitch/hemp/canvas/flax all absent, not a naming miss); adding them is the I12+ new-goods program.
  Also DEFERRED to backlog #146: 13 more CLASS-B svalues whose ingredient (livestock/gems/temperate_fruit/grain/
  sugar/vegetables/fish) has NO `DEMAND_<ing>` aggregator — they feed the separate food-demand
  (`DEMAND_country_*`/stockpile) architecture and alcohol/grain touches an existing `DEMAND_grain_from_industry_alcohol`
  path, so wiring is a DESIGN question (double-count risk), not a mechanical fold. **Post-impl review CLEAN** —
  all 6 checks: (1) all 4 targets defined+well-formed (leaf svalues = factories×constant), each add once, old
  dangling name gone from live code (survives only in FIX A comment); (2) insertion positions verified unscaled
  by mid-block multiplies for B1+C, stone/B2 has none; (3) no double-count (`assigned_glass` now exactly 3×,
  `assigned_early_artillery` 1× in textile_fibres); (4) braces 1279/1279, BOM present, 4278 CRLF / 0 bare-LF,
  clean +38/-1 localized insert; (5) all adds `if`-gated → 0 when factory absent, no div-0, no circular eval
  (leaf targets); (6) correct aggregators, no typos, tail intact. 1 LOW (the pre-existing early_artillery
  mis-key, not introduced, already scoped out). **LIVE economic change → boot-test owed (bites once glass /
  naval_supplies / early_artillery factories exist).** Committed + pushed.
- **BOOT-TEST FLOOD FIX (manufactured_goods box, 2026-07-29 logs.zip; error.log 296,979 lines):**
  IMPLEMENTED + adversarially reviewed. Two MG-caused floods diagnosed from the log and fixed; they
  drove the bulk of the 80,537 "Script system error!" + 35,380 "unset scope" wrapper lines.
  - **Flood #1 (`trade_share_manufacturing_*`, 29,488 hits):** the manufacturing
    `GT_split_calculate_trade_shares` call in `GT_split_calculate_all_trade_shares`
    (se_GLOBALTRADE_split.txt ~3853) was MISSING `category = manufacturing` (present on the
    resource_extraction/shipping siblings) → `$category$` expanded empty, wrote `trade_share__*`,
    distributor read `trade_share_manufacturing_*` unset. Also made I8 (mfg income→workers) a silent
    no-op. FIX: added `category = manufacturing`. Now the block sets all 8 strata vars the distributor
    reads. (Verified against the trade_shares definition @5350 + distributor @3935.)
  - **Flood #2 (`rare_alloys` asymmetry, ~10,850 hits):** I5.5 registered rare_alloys in the SINGULAR
    master `tradegood` injector only — missing from PLURAL `tradegoods` + CATEGORY `tradegood_3`
    lists (per-category setters skipped it while master-list readers hit it: `global_base_import_price`
    2,769, `wealth_owed_for` 1,843, `income_due` 1,843), AND missing 14 hand-defined per-good svalues
    (2 country aggregators `DEMAND_country_rare_alloys` + `GOODS_national_production_rare_alloys`, and
    the 12 cat-3-sibling `electronics`-parity stems: `TRADE_governorship_for_export[_internal]`,
    `TRADE_governorship_export_cap/threshold`, `TRADE_cash_balance`, `TRADE_total_revenue/expenditure`,
    `DEMAND_shortage_country`, `DEMAND_difference_infrastructure_capped`, `GOODS_country_total_sold`,
    `PRICE_global_mean`, `AI_root_scope_unit_price_sqrt`). FIX: added rare_alloys to both injector lists
    (matching `electronics` exactly) + cloned all 14 svalues. Verified: FULL electronics/rare_alloys
    stem parity (0 gaps), every dep resolves, no `electronics` copy-paste leak in any clone body, all
    touched files brace-balanced (pre-existing HEAD 2196/2198 quirk in TRADE_svalues.txt is NOT mine —
    my adds net 21/21), pure additions (0 code-line deletions besides the 1-line category insert).
  - **Systematic asymmetry sweep:** confirmed master↔category injector lists now perfectly symmetric
    (every good in exactly one category list ⇄ master); no other good would flood the per-category setters.
  - **Linear read** of se_GLOBALTRADE_split.txt 1–5984 (user-mandated) COMPLETE — no further MG bugs.
  - **Out of scope (pre-existing, noted only):** uniform 18× `INDUSTRY_factories_assigned_*` unset for
    ALL 24 goods (setup-order, flag-only guard); `cattle`/`livestock` flag mismatch (split 3491 vs 3600);
    bimetallic `_silver_reserves`→`_gold_reserves` multiply typo (5437); merge-overnight baseline floods
    #13-17. Touches 8 files; see BOOT_TEST_NOTES_MANUFACTURED_GOODS_2026-07-29.md. Commit pending review.
- (Phase 3+ increments logged here as they land.)

---

## 7. PHASE 5 RESEARCH — 18c/19c period-appropriateness of goods (drives #138 implementation)

Academic research deliverable (sources: Robert Allen, *The British Industrial Revolution in Global
Perspective* 2009; Joel Mokyr, *The Lever of Riches* 1990; Kenneth Pomeranz, *The Great Divergence*
2000; William Rowe, *China's Last Empire* 2009; plus Wikipedia-verified invention/process dates cited
below). Both start dates matter: **1763** (Qianlong, post-Seven-Years-War) and **1815** (post-Napoleonic).

### 7.1 Per-good period-appropriateness, mechanisation decade, cottage/factory flag, realistic BOM

| Good | 1763 | 1815 | Mechanisation decade | Cottage/Factory | Realistic BOM (raw + intermediate) |
|---|---|---|---|---|---|
| construction_materials | yes (timber/stone/brick/lime) | yes; Portland cement 1824 | brickworks/limekilns already factory-organised pre-1763; cement scales 1850s-70s | both (cottage timber/stone + factory brick/lime) | timber, stone, clay, limestone |
| early_munitions | yes (powder mills water-powered) | yes | powder milling already mechanised pre-1763; arms assembly artisan until armory system 1815-1850s | factory (powder) + cottage (arms assembly) | saltpetre, sulphur, charcoal, lead, iron |
| late_munitions | ANACHRONISTIC | ~anachronistic (percussion caps emerging 1820s-40s) | 1860s-1890s (metallic cartridge 1860s-70s; smokeless powder 1884-1891) | factory-only | steel/brass case, lead, mercury fulminate, nitrocellulose (from chemicals) |
| early_artillery | yes (mature craft) | yes | no mechanisation moment (foundry craft continuous) | factory-organised foundry, craft-skill | bronze OR cast iron, gunpowder |
| late_artillery | ANACHRONISTIC | ANACHRONISTIC | 1850s-60s (Armstrong 1855, Krupp steel breech-loaders 1860s) | factory-only (needs Bessemer/crucible steel + machining) | steel, propellant chemicals, machine_parts |
| naval_supplies | yes (continuous) | yes | not mechanised (dockyard craft) | craft/factory hybrid | timber, tar, pitch, hemp, flax/canvas |
| steel_ships | ANACHRONISTIC | ANACHRONISTIC | iron hulls 1830s-50s; steel hulls ~1870s, dominant 1880s | factory-only | steel, timber, machine_parts (engines) |
| wooden_ships | yes (dominant) | yes (still dominant) | never mechanised (shipwright craft) | craft | timber, tar, pitch, hemp, canvas, iron fittings |
| **steel** | artisan ONLY (crucible/blister, Huntsman 1740s) | STILL artisan/small-batch | **factory mass-steel only from Bessemer 1856-58 / Siemens-Martin 1860s, dominant post-1890** | **cottage/artisan at BOTH 1763 & 1815**; factory ~1856+ | iron ore, coal/coke, limestone flux |
| bronze | yes (ancient craft) | yes | no mechanisation moment | craft/foundry | copper + tin |
| clothing | cottage (hand spin+weave) | TRANSITIONAL (spinning=factory post jenny 1764/water-frame/mule 1779; weaving still cottage) | spinning 1780s-1800s; weaving 1820s-30s | cottage 1763; mixed 1815; factory ~1830s | wool, cotton, flax, silk, dyes |
| luxury_clothing | artisan | artisan | never fully mechanised this period | cottage/artisan both | fine wool/silk, dyes, lace, fur, leather |
| furniture | artisan cabinetmaker | artisan | factory furniture 1850s-70s | cottage/artisan both | hardwood timber, textiles/leather, glue |
| luxury_furniture | high-end artisan | artisan | never mechanised this period | cottage/artisan both | fine hardwoods, veneers, gilding, silk/velvet |
| alcohol | both (farm + commercial breweries) | both | no sharp break; steam in breweries from 1780s | mixed both | grain, fruit, sugar/molasses, hops |
| glass | factory-organised works, hand-blown | same | plant=factory throughout; automatic forming only 1880s-1900s | factory-organised, craft labour | silica sand, soda/potash, lime, lead |
| pharmaceuticals | apothecary craft | apothecary craft | modern pharma industry ~1880s-90s (aspirin 1899) | cottage/artisan both; factory ~1880s+ | botanical/herbal extracts, minerals, later synth from chemicals |
| processed_foods | preservation (salting/smoking/curing) | canning invented 1810, not yet mass | canning industrialises 1820s-60s; factory 1860s-80s | cottage-dominant both; factory late-19c | livestock, fish, vegetables, grain, salt, sugar |
| motors | ANACHRONISTIC | ANACHRONISTIC | 1860s-80s (Lenoir 1860, Otto 1876, Benz 1885-86) | factory-only ~1860s+ | steel, machine_parts, later petrochemicals |
| electronics | ANACHRONISTIC | ANACHRONISTIC | 1900s-1910s (De Forest triode 1906) | factory-only ~1900s+ | copper wire, glass (tubes), rare minerals, rubber |
| rare_alloys | ANACHRONISTIC | ANACHRONISTIC | 1880s-90s (nickel/tungsten/chrome/manganese steels) | factory-only ~1880s+ | steel + nickel/chromium/tungsten/manganese ores |
| chemicals | factory (sulphuric acid, Roebuck 1749) | factory, expanding (Leblanc soda 1791, UK works 1816) | already factory-organised 1763-1815; expands 1790s-1870s | **factory-dominant BOTH dates** (earliest factory good) | sulphur, saltpetre, salt, coal |
| machine_parts | ~anachronistic as traded good | marginal (Maudslay lathe 1800) | real industry 1820s-50s; explodes with steel 1860s+ | factory-only | steel/iron, bronze/brass |
| petrochemicals | ANACHRONISTIC | ANACHRONISTIC | 1859 crude (Drake well) / ~1910s true petrochem | factory-only | crude petroleum |

### 7.2 Key findings for implementation

1. **Current zero-output gating (motors/electronics/petrochemicals + I4's locks) is historically CORRECT.**
   Recommended explicit unlock decades if a date-gate layer is added: motors ~1860-1880s; electronics
   ~1900-1910s; petrochemicals ~1859 crude / ~1910s true; rare_alloys ~1880-1890s; late_artillery
   ~1850-1860s; late_munitions ~1860-1890s (optional transitional percussion-cap tier 1820s-40s);
   steel_ships ~1870-1880s. Our 1763-1900 window means motors/electronics/petrochemicals correctly stay
   `always = no` (I4); the rest unlock via invention gates already wired.

2. **BIGGEST ACCURACY GAP = steel treated as factory-only from start.** Historically steel is a
   cottage/artisan good (crucible/blister, small-batch, expensive) at BOTH 1763 and 1815; factory
   mass-steel only from Bessemer 1856-58 / Siemens-Martin 1860s (dominant post-1890). ACTION CANDIDATE
   (Phase 5 impl): allow steel a cottage-capable path at low volume/high cost with factory steel
   unlocking mid-century, rather than mechanised-only. FLAGGED as a design decision for I-series follow-up
   (currently steel is I3b mechanised-only). NOTE: this reverses the D5 mechanised-only classification for
   steel specifically -- record as a best-guess decision to revisit with the user / boot-test.

3. **BOM corrections vs current wiring** worth auditing in Phase 5 impl: several current BOMs are broadly
   right; verify chemicals inputs (sulphur/saltpetre/salt/coal), glass (silica sand/soda/lime/lead),
   naval_supplies (timber/tar/pitch/hemp/canvas).

### 7.3 Missing significant 18c/early-19c goods (candidates, ranked)

Top additions (all double as Qing-fidelity hooks): **refined sugar** (factory refineries, earliest true
factory industry), **silk textiles** (split from clothing; Lombe's silk mill Derby 1721 = one of
Britain's earliest factories; China/Jiangnan world-leader), **porcelain** (Jingdezhen proto-factory;
Wedgwood factory-organises Europe 1760s), **salt** (universal, huge fiscal base -- Chinese salt monopoly
since 119 BC, >half of some dynasties' tax revenue). Secondary: **paper** (Fourdrinier machine 1799/1801/
operational 1803-04; relevant to Qing print culture), **tea processing** (dominant EIC import from Qing,
central to Canton trade -- highest Qing-export significance even if light manufacturing), gunpowder/
saltpetre (strategic, EIC Bengal), tools/hardware/nails (cottage putting-out -> factory 1830s-60s), soap,
dyes/indigo (synthetic only post-1856), books/printing (steam press Koenig 1814), leather goods, tobacco
(Bonsack cigarette machine 1880).

### 7.4 Qing-specific manufacturing (asymmetric-fidelity granularity targets)

Ranked Qing-specific mechanic candidates: (1) **Salt / Lianghuai monopoly** -- fiscal/monopoly mechanic,
highest revenue significance (state-licensed merchant monopoly near Yangzhou); (2) **Porcelain /
Jingdezhen** -- production-bonus building, highest export/prestige (world's largest porcelain centre since
14c, fine division-of-labour proto-factory); (3) **Silk / Jiangnan** -- cottage-production bonus
(household sericulture + imperial Three Weaving Bureaus 江南三織造; Pomeranz's proto-industrialisation
comparison); (4) **Tea / Fujian-Anhui-Guangdong** -- export/trade-good mechanic (茶號 tea-hong workshops;
dominant EIC import); (5) **Cotton textiles / Songjiang-Jiangnan** -- reinforces clothing cottage-capable
flag (Songjiang cloth exported to SE Asia/Japan). Also: **iron / Foshan** (one of the "four great towns",
ironware cluster); **paper** (Jiangxi/Fujian bamboo paper, feeds bureaucratic print culture).

### 7.5 Source-verification notes

Wikipedia-verified: Bessemer 1856-58, Siemens-Martin 1860s/dominant post-1890; spinning jenny 1764-65 /
water frame / mule 1779; Leblanc soda 1791 / UK works 1816; Fourdrinier 1799/1801/1803-04; Lenoir 1860 /
Otto 1876 / Benz 1885-86; Drake well 1859; Jingdezhen; salt-tax fiscal significance. [domain-consensus]
(Allen/Mokyr/Pomeranz, uncontested but not live-fetched this session): crucible steel 1740s Huntsman,
Roebuck sulphuric acid 1749, London porter breweries 1720s-50s, Lombe silk mill 1721, McKay shoe stitcher
1858, Bonsack 1880, Pomeranz Jiangnan proto-industry. Spot-check before treating as verbatim citations.

### 7.6 Cross-check from parallel research passes (5 independent angle agents) -- additive detail

Five independent research passes (mechanisation timeline / BOM / cottage-vs-factory / missing-goods /
Qing) corroborated §7.1-7.5 and added the following:

- **STRONG multi-agent CONSENSUS: steel is cottage/artisan (crucible/blister) at BOTH 1763 AND 1815.**
  Three separate passes independently reached this. Crucible steel (Huntsman 1740) was explicitly
  small-batch (~15 kg/crucible, ~12 crucibles); Bessemer 1856 (commercial 1858) collapsed cost
  £40->£6-7/ton and dominated by the 1890s. This reinforces §7.2 finding #2 -- steel should be
  cottage-capable at game-start with a mid-late-19c tech/event flip to mechanised-only, NOT mechanised-
  only from start. HIGHEST-PRIORITY accuracy correction for the goods layer.

- **DESIGN INSIGHT -- a THIRD production category ("factory-capital, hand-craft process"):** glass and
  wooden_ships are neither cottage-capable (both need furnace/dockyard capital) NOR machine-mechanised in
  the 1763-1900 window (glass hand-blowing until Owens automatic bottle machine ~1903; wooden shipbuilding
  stays shipwright-craft throughout -- "ships of the Napoleonic Wars still built to the same basic plan as
  the Spanish Armada"). Our binary cottage/mechanised model buckets these as mechanised-only, which is a
  reasonable approximation; flagged so a future fidelity pass can consider a distinct middle tier.

- **alcohol is DUAL from game-start:** cottage (farm/home brewing) AND already large commercial breweries
  pre-1763 (London porter breweries substantial from the 1720s-50s); Coffey continuous still 1830 marks
  the industrial-distilling step. So alcohol = cottage-capable AND factory-capable at 1763 (no wait for an
  IR trigger) -- fine spirits stay pot-still/craft as a luxury variant.

- **wool lags cotton by decades:** wool cottage-dominant at BOTH 1763 and 1815 (spinning mechanises
  ~1800-1820s, weaving mid-19c). Cotton spinning factory-dominant ~1800; cotton WEAVING cottage-majority
  through ~1830 (power-loom crossover 1830). Relevant if clothing BOM is ever split by fibre.

- **NEW Qing hook not in §7.4 -- Yunnan copper / cash-coin minting (well-sourced, hard numbers):** 1725
  Yunnan ran 47 coin-casting furnaces; Ortai's reforms made it profitable enough to export coin to other
  provinces. Annual quotas scaled from 400,000 strings (Shunzhi) to 2,586,000 strings (Jiaqing). Minting
  primarily funded Bannermen salaries + government-construction wages -- i.e. a STATE fiscal/military-
  payroll tool, not commercial coinage. Strong candidate for a state-controlled strategic-resource mechanic
  distinct from market goods. (Source: Qing dynasty coinage, Wikipedia.)
- **Qing silk political-risk hook:** the Cao family held the Jiangning (Nanjing) Imperial Textile
  Commissioner post 3 generations (1684-1727) via a Kangxi personal tie, then was purged/stripped under
  Yongzheng 1727 -- a ready template for a "prestigious but politically risky imperial-monopoly
  appointment" character/event mechanic. Porcelain two-stage chain (Jingdezhen blanks -> Canton painting
  at the Thirteen Factories) maps cleanly to a "regional building + processing chain" mechanic; VOC+EIC+
  others shipped ~100M+ pieces over ~80 years (export-scale data point).

- **Missing-goods TOP-5 consensus (both missing-goods passes agreed):** paper, gunpowder/saltpetre,
  refined sugar, silk (split from clothing), dyes (indigo/cochineal/madder). Deprioritised (cottage/
  artisan the ENTIRE window, no in-window mechanisation event -> no clean two-tier BOM): tobacco (Bonsack
  1880), tea (never mechanised in-period in China), leather (McKay 1858, edge), salt (a taxation/monopoly
  mechanic, not a manufacture). Sugar carries a ready event hook: cane->beet BOM shift forced by the
  Napoleonic Continental blockade (~1800s-1810s).

- **Sourcing caveat (all passes):** live web access was degraded/WebFetch-only in several passes; claims
  rest on Wikipedia tertiary sources + uncontested economic-history consensus, NOT the named
  Allen/Mokyr/Pomeranz/Rowe primary texts (not fetchable this session). Thin/unverified-this-session:
  furniture factory-mechanisation exact decade (~1856 Thonet Koryčany factory is the anchor found),
  glass hand->machine transition (~1903 Owens, outside window), EIC-Bengal saltpetre volumes, Qing
  yanzheng licensing detail, tea-region processing. Spot-check before any of these become load-bearing.

---

## 8. PHASE 5 IMPLEMENTATION PLAN (research-driven goods changes — #144)

The Phase 5 research (§7) produced a ranked action list. Implementing the whole list (new goods
sugar/silk/paper/dyes/gunpowder + full BOM audit + date-gates) is a feature-scale program; per the
build rules each piece gets design → adversarial review → implement → adversarial review, in small
increments. Ordered by research-stated priority and by blast radius (smallest, best-sourced first):

- **I10 — Steel becomes cottage-capable (crucible/blister artisan path).** §7.2 finding #2 + §7.6 (STRONG
  multi-agent consensus, "HIGHEST-PRIORITY accuracy correction"). Today steel is I3b mechanised-only
  (`COTTAGEIND_produce_steel` = explicit "CANNOT BE PRODUCED" stub; summed writer notes "No cottage recipe
  for steel"). Historically steel is artisan/small-batch (Huntsman crucible 1740, blister) at BOTH 1763 and
  1815; factory mass-steel only from Bessemer 1856. **Decision (best-guess, per autonomy mandate; reverses
  D5 mechanised-only for steel ONLY):** give steel a cottage recipe with a DELIBERATELY LOW efficiency (so
  artisan steel is a trickle at high effective cost, not a free substitute for factories), consuming iron +
  coal (its real BOM). Factory steel stays invention-gated (tech_manufactories + tech_blast_furnace on
  `add_steel_button`) and is the volume path once unlocked — matching the "artisan game-start → factory
  mid-century" arc without needing a new date-gate (the invention gate already IS the mid-century flip).
  **Files:** (1) `se_COTTAGEIND.txt` — replace the steel stub with a real recipe (iron + coal, low
  efficiency); requires caching `COTTAGEIND_raw_coal` (coal is NOT currently in `COTTAGEIND_cache_all_values`
  — the recipe references only cached vars, so coal must be added to the cache the same way as iron/stone;
  `GOODS_governorship_coal_produced` exists at GOODS_svalues.txt:1525). (2) `GOODS_svalues.txt` — steel
  summed writer already adds `_mechanised`; add the `if has_variable = COTTAGEIND_produced_steel { add =
  var:COTTAGEIND_produced_steel }` branch (D1a split-writer, identical to construction_materials) and fix
  the two stale "No cottage recipe for steel" comments. (3) `industry_l_english.yml` — steel tooltip already
  shows the cottage line (`industry_TT_p2` reads `COTTAGEIND_produced_steel`), so no loc change needed.
  **Efficiency calibration:** cottage efficiencies today span 0.5 (bronze) … 10 (two outliers). Steel
  artisan should sit at/below bronze (0.5) — best-guess **0.35** — reflecting crucible steel's tiny batch
  size + high cost. Flag for balance/boot-test. **Risk:** if efficiency too high, artisan steel floods the
  market pre-industrialisation and trivialises the Bessemer unlock; low starting value + boot-test mitigates.
  **STATUS: DONE — design review PASS (SOUND; 0.35 defensible/conservative, ~4 orders of magnitude below one
  factory; 1 MEDIUM comment-fix trap flagged), implemented as designed, post-impl review CLEAN (all 7 criteria,
  no CRITICAL/HIGH/MEDIUM), committed. Boot-test owed (live economic change). See REVIEW LOG I10.**
- **I11 — BOM spot-audit fixes (§7.2 #3): two DEMAND-layer correctness defects.** A five-layer BOM audit of
  chemicals/glass/naval_supplies (cottage / mechanised svalue / INDUSTRY factory demand / DEMAND aggregator /
  price / tooltip) found the INDUSTRY, price, and tooltip layers all AGREE per good, but the DEMAND-aggregator
  layer has two genuine wiring defects (both the I5.5 bug-class — an undefined-svalue reference floods the log
  and evaluates to 0, and a missing aggregator branch silently drops real factory demand). **Both verified on
  disk:**
  - **Defect A (naval_supplies bronze — dangling reference):** `DEMAND_bronze` at DEMAND_svalues.txt:1488 adds
    `INDUSTRY_naval_supplies_parts_bronze`, a name defined NOWHERE (sole repo occurrence). The correct svalue is
    `INDUSTRY_demand_naval_supplies_bronze` (INDUSTRY_svalues.txt:1113, well-formed, mirrors the other 3
    naval_supplies ingredient demands). Fix = rename that one token. Effect: naval_supplies factories will now
    correctly draw bronze demand (and stop logging an undefined-svalue error each quarter once naval_supplies
    factories exist).
  - **Defect B (glass coal + stone — missing aggregator branches):** `INDUSTRY_demand_glass_coal`
    (INDUSTRY_svalues.txt:1439) and `INDUSTRY_demand_glass_stone` (1466) are defined + well-formed but consumed
    NOWHERE; only `INDUSTRY_demand_glass_lead` is wired (into `DEMAND_lead` at :1220). So glass factories draw
    lead demand but not coal/stone. Fix = add the two standard `if has_variable = INDUSTRY_factories_assigned_glass
    { add = INDUSTRY_demand_glass_<coal|stone> }` branches to `DEMAND_coal` (~:390, alongside steel/chemicals/
    steel_ships) and `DEMAND_stone` (~:706, alongside construction_materials), mirroring the existing glass_lead
    branch and every sibling factory branch exactly. Both adds land BEFORE the block's `multiply =
    DEMAND_elasticity_impact` / `min = 0` tail (same anchoring as every neighbour).
  **Scope decision (best-guess, per autonomy mandate):** I11 fixes ONLY these two proven wiring defects — it does
  NOT change ingredient COMPOSITION. The remaining §7.1/§7.6 historical mismatches (chemicals wants saltpetre;
  glass wants silica sand/soda/lime not stone; naval_supplies wants timber/tar/pitch/hemp/canvas) all reference
  raw goods that DO NOT EXIST in the mod's palette (verified: saltpetre/silica/soda/lime/tar/pitch/hemp/canvas/
  flax/charcoal all ABSENT). Adding raw goods is high-blast-radius (new tradegood defs + injector list D10 regen
  hazard + DEMAND/price/GUI) and belongs with the I12+ new-goods program, NOT a "spot-audit fix." The current
  stone/coal/metals proxies are a defensible abstraction and stay. **Files:** DEMAND_svalues.txt ONLY (3 edits:
  1 rename + 2 branch inserts). No new svalues, no injector touch, no loc. **Risk:** minimal — all three refer to
  already-defined, already-verified INDUSTRY svalues; the fix makes demand match the production/price/tooltip
  layers that already ship these ingredients. **Design review WIDENED the scope:** the glass gap is not
  unique — it is SYSTEMIC. A completeness sweep found the two defect classes across all goods: CLASS A
  (dangling refs) has exactly ONE instance repo-wide (the bronze one FIX A targets); CLASS B (defined-but-
  unconsumed demand svalue whose target `DEMAND_<ing>` aggregator exists) has a 4th mechanical instance —
  **FIX C: `INDUSTRY_demand_early_artillery_textile_fibres` (INDUSTRY_svalues.txt:1905) → add to
  `DEMAND_textile_fibres`** (a real input per its production malus, consumed nowhere). Folded into I11. A
  further 13 CLASS-B svalues were found whose ingredient (livestock/gems/temperate_fruit/grain/sugar/
  vegetables/fish) has NO `DEMAND_<ing>` aggregator at all — those feed the separate food-demand
  (`DEMAND_country_*`/stockpile) architecture and at least alcohol/grain touches an existing
  `DEMAND_grain_from_industry_alcohol` path, so wiring them is a DESIGN question (double-count risk), NOT a
  mechanical fold → deferred to backlog #146, explicitly logged not dropped. Review also noted the whole
  early_artillery demand block is mis-keyed to `INDUSTRY_early_munitions_factories` (pre-existing systemic
  bug, out of I11 scope; FIX C stays consistent with its 7 already-wired siblings). **STATUS: DONE — design
  review SOUND (widened +FIX C), implemented as 4 edits in DEMAND_svalues.txt, post-impl review CLEAN (all 6
  checks, no CRITICAL/HIGH/MEDIUM), committed. Boot-test owed (live economic change once these factories
  exist). See REVIEW LOG I11.**
- **I12+ — New goods (deferred within Phase 5).** sugar (factory refineries + cane→beet Napoleonic event hook),
  silk (split from clothing), paper, dyes, gunpowder/saltpetre. Each is a full mini-build (new tradegood defs,
  injector list D10 regen hazard, DEMAND/prices, cottage+mechanised chains, GUI buttons, loc); scoped after I11
  lands and is boot-confirmed. Adding saltpetre here would also let a later pass correct the chemicals/gunpowder
  BOM that I11 deliberately left as a proxy.

---

## Boot-test 2026-07-29 findings MG-1 .. MG-5 + residual floods

Source: `BOOT_TEST_NOTES_MANUFACTURED_GOODS_2026-07-29.md`. Five reported bugs; all addressed.

- **MG-1 / MG-2 — loc + capitalization.** 8 loaded goods (linen/cotton/wool/inorganic_compounds/whales/
  peat/palm/chocolate) had NO name/DESC and rendered as raw lowercase keys → added `#T #L` sibling loc.
  Capitalization tail: 9 building-name loc keys were sentence-case ("Industrial estate") → Title Case per
  user rule; 2 trade-good DESC tooltip headers lowercase (Processed foods / Naval supplies) → fixed.
  **STATUS: DONE — committed a45b0b71b (cap tail) + 7478ca515 (loc). Boot-test owed.**
- **MG-3 — every good felt identical.** All 56 goods carried the same placeholder province block
  (`local_monthly_food = 0.07`, no country block). Reworked each to a DISTINCT province modifier + a
  role-matched country modifier (iron→regular_infantry_discipline, silk→export-commerce, grain keeps food,
  etc.). 4 goods retargeted off inert stub unit-type tokens onto functional country-legal ones.
  porcelain/rifles drop the flat-food byproduct (worked, not agricultural). category/gold/color/
  allow_unit_type + BOM + LF all preserved; braces 224/224. **STATUS: DONE — design review + post-impl
  adversarial review both CLEAN (all tokens legal, no dupes). Committed 94df025d3. Boot-test owed.**
- **MG-4 — loyal-cohorts grant was a no-op.** `QING_regional_army_bind_commander` only bumped the abstract
  `num_loyal_veterans` pool (`add_loyal_veterans`) → no visible cohorts. Rewired to trampoline through
  hidden `qing_office.42` (dodges the scripted_gui compile-inline AV, per `qing_guard.10` precedent), which
  picks the weightiest sitting Han governor and — on his FIRST sanction only (fire-once guard via
  `qing_had_yongying_already`) — raises a REAL `qing_yongying` legion (`QING_regional_army_raise_yongying`,
  clone of the proven grandee-legion idiom) and binds him as commander with loyal sub_units. Create↔destroy
  symmetry: `QING_reassert_strip_magnate` now destroys the legion (`every_character_unit = destroy_unit`)
  when the veteran tally fully draws down. LOG wording split so "physical legion raised" logs only on the
  actual raise. **STATUS: DONE — design review (fabricated-citation + unbounded-legion flags folded in) +
  post-impl adversarial review both CLEAN (scope chain, fire-once ordering, refs, braces). Committed
  35ba9099f. Boot-test owed.**
- **MG-5 — personnel-dispute recall didn't remove governor.** (Fixed prior session.) **STATUS: DONE —
  committed 7478ca515.**

### Residual correctness fixes (folded in at user request 2026-07-29) — IN PROGRESS
Two "residual" items from the boot-test notes, promoted to full fixes (design → adversarial review →
implement → adversarial review → commit). Design in `MG_RESIDUAL_FLOODS_DESIGN.md`.
- **Bimetallic silver multiply typo** (`se_GLOBALTRADE_split.txt` bimetallic branch): silver reserve is
  set+divided on `_silver_reserves` but the demand-ratio multiply names `_gold_reserves` → silver never
  multiplied, gold multiplied twice. Fix = one `_gold_reserves`→`_silver_reserves`. Sibling gold/silver-only
  branches prove the "multiply the reserve you set" pattern.
- **cattle/livestock classifier mismatch**: `livestock` is the only loaded good; `cattle` is a defunct
  vanilla name absent from the goods file, so `flag:$tradegood$ = flag:cattle` never matches. Raw-goods
  classifier copy-pasted; expenses side (split:3491) + canonical `is_raw_tradegood` (scripted_triggers:74)
  use dead `flag:cattle` while income side (split:3600) uses correct `flag:livestock` → livestock import
  expenses mis-booked to manufacturing bucket vs its income booked to resource-extraction. Fix = both
  `flag:cattle`→`flag:livestock`. **STATUS: DONE — design review CONFIRMED (no missed 4th list; is_raw_tradegood
  unused so latent, fixed anyway), implemented as 3 single-token edits, post-impl review CONFIRMED (diff is
  exactly the 3 fixes + comments, braces/BOM/CRLF intact, zero live flag:cattle). Committed 049d2acfa,
  pushed. Boot-test owed (economic accounting change).**


## 9. VANILLA vs MOD TRADE SYSTEMS — architecture + the "Request Trade Route" flood (BT 2026-07-29/30)

**imp19c runs TWO trade systems in parallel over the same trade-good keys.** Understanding the
split is essential before touching anything trade-related.

### Vanilla engine trade (C++, still LIVE underneath)
- Each province produces one trade good. A country with a *surplus* of a good receives that good's
  `country = { }` block (the "trade-surplus bonus", e.g. salt -> `army_maintenance_cost = -0.05`).
  The `province = { }` block is the local bonus for producing it.
- Countries import goods they lack via **engine trade routes**. AI desire to import good X is driven
  largely by how valuable X's `country = { }` bonus is. Route economics live in
  `common/defines/00_defines.txt -> NTrade` (`ROUTE_BASE_INTERNAL/EXPORTING/IMPORTING_COMMERCE`);
  these are STOCK values (0.2 / 1 / 0.35) — imp19c never zeroed them, so the vanilla commerce layer
  and its `country{}` bonuses ARE live and reach the player.
- The AI's propensity to *ask* for a route is `common/ai_diplochance/00_default.txt -> trade_access`
  (loc `ASKTRADEACCTITLE` = "Request Trade Route"), scaled by define `TRADE_REQUEST_ACCEPTANCE`.

### Mod script trade (imp19c, the system the mod actually wants players to use)
- A parallel quarterly market sim in `se_GLOBALTRADE_split.txt`. Its own tradezone (TZ) / stockpile /
  price economy, all stored in VARIABLES — it does **not** use engine trade routes at all.
- **What a good "is" to the mod:** per-governorship, per-good production (cottage + mechanised
  factories) adds to a `<good>_stockpile` var; pop/industry DEMAND (`se_DEMAND`) draws it down; the
  leftover is offered to the TZ market at a computed PRICE (`PRICE_svalues`, supply vs
  `global_var:global_mean_price_<good>`), capped by infrastructure/shipping capacity. Goods are
  handled by category (food_goods + manufactured/raw tiers) and cottage-vs-mechanised chains.
- **What "surplus" means in mod terms:** a positive `<good>_stockpile` after local demand is met,
  which the governorship SELLS into the tradezone. It is a continuous priced quantity, NOT vanilla's
  binary count-based surplus.

### Trade Agreement (mod-invented; NO vanilla equivalent) — the mod's replacement for trade routes
- `se_DIP_TRADE.txt` + `common/scripted_guis/trade_diplo_buttons.txt`. Pure variable lists
  (`list_of_trade_partners_<category>`; categories: food_goods + all_categories scaffold).
- Effect: it DIVIDES a country's exports and import demand among its agreed partners
  (`TRADE_number_of_trade_partners_<category>` = the divisor) and grants tradezone PENETRATION
  (`MODIFIER_GLOBAL_STATE_TRADE_ROUTES`), scaled against tariffs (higher tariffs = less penetration
  from partners' agreements, more from your own shipping). No goods move via engine routes — it is
  all the script market. This is how two countries formally open their script-market tradezones to
  each other, i.e. the on-design substitute for vanilla "request/accept trade route".
- The mod market + Trade Agreement layer reads STOCKPILE VARS and the trade-partner LISTS. It never
  reads a good's `country{}` bonus.

### The regression: "Request Trade Route" flood at game start
- imp19c meant to suppress the vanilla trade-route AI, but `trade_access` only had `base offset = 0`
  and LEFT `opinion scale = 0.25` — so positive opinion still pushed the request over threshold.
- It stayed quiet ONLY because pre-MG just ONE good (tobacco) carried a `country{}` bonus, so the
  vanilla import AI had essentially nothing worth importing.
- **MG-3 (#148)** gave all 56 goods a distinct `country{}` bonus (to make each good feel different).
  That handed the vanilla import AI 56 desirable import targets -> it woke up and flooded the player
  with "Request Trade Route" from turn 1. Seen first on the manufactured_goods boot test, then on
  merge-overnight after the merge. `country{}` bonuses feed ONLY the vanilla layer — the mod's own
  market/Trade-Agreement system is indifferent to them.

### Fix chosen (2026-07-30, committed 803d7d3fa)
- **Harden `trade_access` only.** base offset 0 -> **-1000** (swamps any positive term), opinion
  scale 0.25 -> **0** (removes the term still driving it). `scale = 0` is the file's documented
  disable idiom (header: "Hardcoded factors can be removed by scaling by 0"; already used elsewhere).
- The 56 `country{}` surplus bonuses are LEFT INTACT: with the vanilla commerce layer still live they
  are real player-facing modifiers (several mirror stock vanilla, e.g. grain food / salt maintenance).
  Only the AI's propensity to ASK for a route is disabled. Trade Agreement diplomacy untouched.
- REJECTED alternative: stripping the `country{}` bonuses. Rejected because they are live gameplay
  rewards under the still-active vanilla layer, not vestigial — removing them would delete real
  surplus modifiers. If imp19c ever fully zeroes the vanilla commerce layer (NTrade ROUTE_BASE_* = 0),
  revisit: then the `country{}` bonuses WOULD be vestigial and could be stripped.

### STANDING RULE for future trade-good work
Adding/enlarging a good's `country{}` bonus re-arms the vanilla import AI. That is now hard-suppressed
via `trade_access`, so it will not re-flood — but any future change that touches NTrade route commerce,
`trade_access`, or re-enables vanilla trade diplomacy must re-check this interaction. The mod's own
distinctiveness for a good belongs in its `province{}` block + the script market (stockpile/price/
Trade Agreement), NOT in `country{}`.

---

## 10. #201 — Bespoke apotheosis effects for the 48 ideology thinker-deities (2026-07-30)

### Problem
The 48 ideology thinker-deities (`common/deities/04_ideology_pantheons.txt`) each cloned one of only
EIGHT generic category base effects (`military_apotheosis_capital_freemen_effect`, `economy_income_effect`,
`culture_apotheosis_characters_effect`, `fertility_apotheosis_capital_effect`, and their `_2` counterparts).
Because the 6 ideologies × 8 slots reuse the same 8 effects, a Liberalism war-deity (Montesquieu) and a
Communism war-deity (Marx) fired an **identical** apotheosis. Mechanically the 48 collapsed to 8.

### Design chosen — layered flourish (NOT full bespoke rewrite)
Following the upstream wrapper idiom in `common/scripted_effects/00_apotheosis.txt`
(`tur_apotheosis_effect` = base + `add_trait`; `midas_apotheosis_effect` = base + `add_treasury`;
`pylaemenes_apotheosis_effect` = base + `add_popularity`/`add_legitimacy`), each deity KEEPS its working
category base effect and gains ONE ideology-specific flourish appended to `on_activate`:
`on_activate = { <base>_effect = yes ideology_apotheosis_<ideology>_effect = yes }`.
Result: all 48 are now unique — distinct across ideologies (flourish differs) AND within an ideology
(base differs). New effects live in `common/scripted_effects/se_IDEOLOGY_APOTHEOSIS.txt`.

Six flourishes, each a different lever so no two ideologies overlap:
| Ideology | Flourish | Primitive (all proven in 00_apotheosis.txt) |
|----------|----------|----------------------------------------------|
| Liberalism   | +10 political influence (the open forum)        | `add_political_influence` (glycon) |
| Conservatism | +5 stability (the settled order)                | `add_stability` (add_stab_apotheosis) |
| Monarchism   | +10 legitimacy (if monarchy) + ruler popularity | `add_legitimacy`/`add_popularity` (pylaemenes) |
| Nationalism  | manpower scaled by Martial, else military exp   | `add_manpower`/`add_military_experience` (military_apotheosis_manpower) |
| Socialism    | state food to every state, scaled by Charisma   | `every_country_state add_state_food` (fertility_apotheosis_food) |
| Communism    | +15 civic-tech research (scientific vanguard)    | `add_research civic_tech` (culture_apotheosis_civic_tech) |

### Why NOT a full bespoke effect per deity
48 hand-written effects would (a) require 48 new `_tt_description` loc keys and 48 tooltip audits, (b)
risk unproven primitives per author whim, (c) not actually improve differentiation over "6 ideology
signatures × 8 category bases = 48 unique pairs". The layered flourish delivers full uniqueness while
reusing the already-shipped, already-localized 8 base tooltips. Every primitive is one the vanilla
apotheosis file already uses at country scope (`on_activate` runs in country scope — confirmed: the
base `economy_income_effect` uses `add_treasury`).

### Loc
Each deity `_desc` now ends `... $<base>_tt_description$ $ideology_apotheosis_<ideology>_tt$` — the base
tooltip line plus the flourish line. Six `ideology_apotheosis_<ideology>_tt` keys added to
`localization/english/qing_ideology_deities_l_english.yml`.

### Verification
48 `on_activate` rewrites (8 per ideology, verified by count); brace-balanced (deities 288/288,
effects 29/29); all 6 effects defined, all 6 tt keys defined; each ideology block carries only its own
flourish (cross-checked). No unproven engine capability introduced.

---

## 11. #145 — never-refreshed global_mean_price + new-country double-seed (2026-07-30)

Two independent pre-existing balance/correctness bugs flagged during I6/I7 review, both fixed. Adversarial
code-review (code-review agent) returned CLEAN on both parts.

### Part A — quarterly refresh of `global_mean_price_<good>`
**Bug:** `global_mean_price_<good>` (global var, the tradezone-averaged price read by I7's input-cost
factoring `PRICE_factor_raw_input_costs_X`) was computed ONCE at day-0 setup
(`PRICE_update_TZ_prices` -> `PRICE_update_all_global_mean_prices`, oa_economy_setup.txt:2360) and never
refreshed. But `local_price_<good>` (which the mean averages) IS recomputed every quarter by
`GT_set_tradegood_price` (se_GLOBALTRADE_split.txt) on the trade-center provinces. So every quarter's
manufactured-good input-cost factoring read a frozen day-0 mean forever — affecting all 24 MG goods and
the 9 originals identically.
**Fix:** added `PRICE_update_all_global_mean_prices = yes` to `quarterly_reset_trade_transaction_totals`
(oa_wealth_changes.txt), the FIRST on_action in the quarterly trade pulse (globally gated to fire once per
quarter). Called ONLY the averaging pass — NOT the full `PRICE_update_TZ_prices`, which would also re-run
`PRICE_update_price_TZ`/`PRICE_normalise_price` and double-recompute `local_price` via the defunct SELL
formula. Because it runs at quarter-start it reads the PRIOR quarter's final local prices (the same stable-
prior-snapshot ordering I7 documented), then the day-9..61 splits consume the freshly-refreshed mean — no
read-after-write circularity. Scope-safe at the on_action root (`every_trade_center`/`every_tradegood_complex`
are global-list iterators; siblings `GT_split_setup_global_shipping_costs_pool` etc. run at the same scope).
`num_of_TZs = 22` (static svalue) so the divide can't div-0.

### Part B — new-country stockpile double-seed
**Bug:** `FUNC_setup_new_country` (se_FUNC.txt) seeded newly-spawned-country governorship stockpiles TWICE
at t=0: `GOODS_setup_governorship_stockpiles` (:492, `set_variable { value = <good>_produced }`) then
`FUNC_every_governorship_update_tradegood_stockpiles` (:522, `change_variable { add = <good>_produced }`).
Both firing = 2x one quarter's production seeded at t=0. The game-start path (oa_economy_setup.txt:381)
calls ONLY `GOODS_setup_governorship_stockpiles`, so game-start countries are single-seeded; revolts/
colonies/new tags were double-seeded.
**Fix:** commented out the second call. Review confirmed: (1) it was the sole caller (definition now
harmless dead code); (2) `GOODS_setup_governorship_stockpiles` hand-enumerates a STRICT SUPERSET of the
goods the removed `every_tradegood_complex` loop covered, so NO good is left unseeded (the under-seed
risk does not trigger); (3) the removed call wrote the same `<good>_stockpile` var from the same
`GOODS_governorship_<good>_produced` source — genuinely redundant. New countries now match game-start.

### Incidental (NOT fixed here — separate backlog)
Review noted `every_tradegood_complex` omits 7 defined goods (chocolate, inorganic_compounds,
mediterranean_fruit, peat, tropical_fruit, whales, wool) that `GOODS_setup_governorship_stockpiles` covers.
A pre-existing gap in the shared iterator affecting the whole price/demand pipeline, unrelated to #145.
Logged for a future decision on whether those 7 goods are meant to be live in the script market.

---

## 12. #146 — wire deferred factory food-ingredient demand svalues (2026-07-30)

### Finding: 12 of the 13 were already wired by I3; only ONE genuine gap remained
The #146 backlog note (written at I7 time) flagged 13 CLASS-B leaf demand svalues
(`INDUSTRY_demand_<good>_<ingredient>` for the 7 food ingredients livestock/gems/temperate_fruit/grain/
sugar/vegetables/fish) as needing to be wired into the food/luxury-demand model. A fresh audit
(grep for `add = <leaf>` across common/) found the incremental I3 wiring had since consumed 12 of them:
- **food model** (`DEMAND_food_svalues_new.txt` `DEMAND_<ing>` svalues, each gated on
  `has_variable = INDUSTRY_factories_assigned_<good>`, `add = INDUSTRY_demand_<good>_<ing>`):
  clothing/early_artillery/processed_foods → livestock; alcohol/pharmaceuticals/processed_foods →
  vegetables; alcohol → grain; alcohol → temperate_fruit; processed_foods → fish.
- **luxury model** (`DEMAND_luxury_svalues.txt`): luxury_clothing/luxury_furniture → gems; alcohol → sugar.

### The one genuine gap fixed
`INDUSTRY_demand_luxury_clothing_livestock` (INDUSTRY_svalues.txt:535; gate
`INDUSTRY_factories_assigned_luxury_clothing`; base 5 units/factory) was defined AND already read by the
price input-cost factoring (`se_PRICE.txt:617-637`, `PRICE_factor_raw_input_costs_luxury_clothing`), but
never added to `DEMAND_livestock`. So luxury_clothing factories PRICED livestock as an input yet never
ORDERED it — a supply/price asymmetry (the input cost showed up in the good's price but generated no
actual livestock demand, understating livestock consumption wherever luxury_clothing factories exist).
**Fix:** added the standard gated `add = INDUSTRY_demand_luxury_clothing_livestock` block to
`DEMAND_livestock` (DEMAND_food_svalues_new.txt), matching the three existing siblings there
(clothing/early_artillery/processed_foods) exactly. No double-count — verified this is the sole
luxury_clothing→livestock consumer. Braces 117/117, BOM+CRLF preserved. **LIVE economic change (bites
once a country runs luxury_clothing factories) → boot-test owed.**

---

## 13. #139 — MG Phase 6 performance assessment + optimizations (2026-07-30)

Assessment (general-purpose analysis agent, read-only) of the quarterly economic hot loops
(~200 countries × N governorships × ~62 tradegoods × quarterly). Conclusion: the per-tradegood hot
paths are ALREADY close to fully optimized by prior work (perf #71 caches, #139-E food-mean relocation,
produce-loop `produces_<good>` gating, CONSUME loop-invariant hoisting). Two genuine remaining
opportunities found — both about caching GRANULARITY, not missing caches. Both implemented; Finding 1
reviewed CLEAN, Finding 2 reviewed with a correctness refinement (below).

### Finding 1 (implemented, CLEAN) — infrastructure-capacity cached at wrong granularity
`GT_split_cache_governorship_infrastructure_capacity` (writes `var:governorship_infrastructure_capacity`
= `TRADE_governorship_infrastructure_capacity_svalue`, a 7-addend all-state-province walk +
shipping-power branch) was called inside `GT_split_do_global_trade_split` (se_GLOBALTRADE_split.txt:12) —
once per governorship PER CATEGORY PASS = **7×/quarter** — although it changes only when a building
finishes construction. **Fix:** relocated to the once-per-quarter loop in
`quarterly_reset_trade_transaction_totals` (oa_wealth_changes.txt), beside the sibling once/quarter caches
(WEALTH_cache_shipping_trade_values, DEMAND_cache_and_update_elasticity_impact). All 4 readers use the
cached var (se_GLOBALTRADE_split.txt:787/802/2137/2152), so transparent. Added a cold-start seed to the
game-setup path (oa_economy_setup.txt, in the `GT_reset_trade_transaction_totals` loop) because that path
runs the 7 splits directly at day 0 — same cold-start reasoning as the #139-E food-mean re-seed. Collapses
7 multi-province walks/governorship/quarter to 1 (~85% cut, the perf #71 shape). **Accepted temporal
caveat:** a building completed mid-quarter now takes effect next quarter's trade rather than the next
category pass — identical once/quarter semantics to the sibling caches; review confirmed this is the ONLY
behavioural change.

### Finding 2 (implemented, refined) — WEALTH generation loop not gated like its sibling produce loop
`WEALTH_generate_from_production` (se_ECON_wealth.txt) runs the ungated `every_tradegood_complex` (~62
goods)/governorship/quarter; for the 45 raw goods `GOODS_governorship_<good>_produced` is a full
province walk returning 0 where the good isn't local. **Fix:** wrapped the wealth `add` in a 3-marker OR
gate — `produces_<good>` (45 raw) ∪ `INDUSTRY_factories_assigned_<good>` (24 factory, always present at
setup) ∪ `COTTAGEIND_produced_<good>` (14 cottage). Verified the union covers all 62 iterated goods with
ZERO gaps, and factory+cottage are both OR'd so cottage-only goods aren't wrongly zeroed.
**Adversarial review refinement:** the change is NOT strictly byte-neutral. `produces_<good>` is written
only at setup + FUNC_setup_new_country, NOT on ownership change (`GOODS_update_governorship_local_goods`
is documented-unwired for transfers at se_GOODS.txt:838). A raw good gained by an existing country via
conquest/peace-transfer has a stale-absent `produces_` marker → OLD code generated wealth for it. BUT the
production-into-stockpile loop gates on the SAME stale marker, so that good produced into NO stockpile
either way. OLD wealth was therefore PHANTOM (wealth with no matching stockpile output); the gate removes
it, making wealth consistent with actual production — more correct, not a drain. Comment corrected to state
this accurately rather than "provably neutral".

### Backlog surfaced (NOT fixed — pre-existing, affects both loops)
- **#139-C:** `produces_<good>` staleness on ownership change — `GOODS_update_governorship_local_goods`
  never runs on conquest/peace-transfer (only setup + new-country). Affects BOTH the produce loop and
  (now) the wealth loop identically; wiring it into an ownership-change on_action would fix the underlying
  phantom-wealth/no-production mismatch for the whole economy. Logged, not addressed here.
- Cottage markers `COTTAGEIND_produced_{alcohol,naval_supplies,wooden_ships}` are set inside an `if` and
  never cleared → a governorship that loses the enabling condition keeps a stale cottage value that both
  old and new `GOODS_governorship_<good>_produced` read via `has_variable`. Pre-existing, unrelated to #139.

### 13.1 — #139-C RESOLVED (2026-07-30, commits d2e60db7d + 5fe7a5d91) — both adversarially reviewed
All three surfaced items above are now closed:
1. **produces_<good> ownership-change refresh (FIXED, d2e60db7d).** Wired
   `governorship ?= { GOODS_update_governorship_local_goods = yes }` into `on_ownership_change`
   (00_specific_from_code.txt:891). At fire time the province is in its NEW-owner state (verified: all
   sibling hooks CLAIM_HOSTILITY/DEJURE/MIGRATION read `owner` as the taker), so this refreshes the
   GAINING governorship — exactly the one carrying the stale-ABSENT marker (the substantive defect). The
   losing governorship's stale-TRUE marker is benign (its produced-svalue province-scan sums ~0). Universal
   hook: LAND_transfer_province → FUNC_set_conquered_by → engine `set_conquered_by` fires it, as do AI peace
   deals and event cedes — no per-flow wiring needed. Review: SOUND; only a LOW optional perf note (the hook
   rescans the gaining governorship once per transferred province with no dedup — a one-time
   O(provinces×45goods) spike at peace, matching the accepted tolerance of the sibling hooks; a
   `governorship_vars_updated`-style dedup list would be nice-to-have, not required).
2. **Cottage-marker clear (FIXED, d2e60db7d).** Added `else = { remove_variable = COTTAGEIND_produced_<good> }`
   to the 3 gated cottage recipes (naval_supplies/wooden_ships coastal gate, alcohol restriction gate) in
   se_COTTAGEIND.txt. Without it, a governorship that lost the enabling condition kept a stale-TRUE marker +
   last value, which readers (GOODS_svalues.txt:2756/2802/2993, DEMAND_svalues.txt:506/647/1347) re-added as
   phantom output every quarter (they gate on has_variable). `remove_variable` makes the branch a clean no-op.
   Review: SOUND; confirmed these 3 are the ONLY conditionally-gated cottage recipes (all others do an
   unconditional per-quarter set_variable, self-refreshing, no staleness).
3. **7-good every_tradegood_complex omission = NOT A BUG / WAI (5fe7a5d91, comment-only).** git-blame found
   the smoking gun: upstream commit 584ac791c (2024-04-20) DELIBERATELY removed wool/whales/peat/
   inorganic_compounds/tropical_fruit/mediterranean_fruit/chocolate from the iterator AND added the boot-time
   `defunct_tradegoods_replaced` remap (oa_economy_setup.txt:130-215) that converts every province carrying
   them to a live substitute (wool→textile_fibres, whales→fish, chocolate→coffee, peat→sulphur,
   inorganic_compounds→stone, {tropical,mediterranean}_fruit→temperate_fruit) BEFORE any sim tick. So no
   province ever carries them past boot; their defs + supporting svalues survive as unreachable dead code.
   Adding them back to the iterator would be WRONG. Fix = add DEFUNCT comments to their trade_goods defs
   (mirroring the existing cloth/hemp/camel `# to be removed` style) so future audits don't re-flag them.
   **Boot-test owed for items 1+2 (live economic changes).**

### What is already well-optimized (no action)
All `owner.var:X` reads inside the 7 category passes are already cached var reads, not live svalue
recomputes. PRICE_update_TZ_prices / se_PURCHASE / FUNC_every_governorship_update_tradegood_stockpiles are
setup-only or dead code, not in the quarterly tick. **LIVE economic change (Finding 1 timing + Finding 2
phantom-wealth removal) → boot-test owed.**
