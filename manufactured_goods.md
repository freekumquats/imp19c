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
**Decision.** Add `rare_alloys` to the `tradegood_hypercomplex` injector list and regenerate, so
consumption runs for a true all-24. If regeneration proves risky (the injector is a generated file),
FALLBACK: keep rare_alloys tech-locked (D3) so it never produces, and record the gap — never un-gate a
good that has no consumption sink. Preferred path is closing the sink, not locking the good.
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
- **I2 — Split-writer svalues (D1a/D2): mechanised-only `GOODS_governorship_X_produced_mechanised` for
  all 24 + repair summed display svalue + naval_supplies/glass/dup fixes + migrate the 4 hand-coded
  blocks onto the mechanised-only macro (removes the live double-count).** LIVE change for the 4
  pre-wired goods → boot-test. Other 20 still gated OFF.
- **I3 — Missing `INDUSTRY_production_X` rate svalues + cottage recipes (D5).** Raw-goods BOM. New goods
  still gated OFF.
- **I4 — Real tech gating (D3).** `INDUSTRY_unlocked_X` from the invention map (+ add wooden_ships);
  GUI buttons already agree.
- **I5 — Employment scaling (D4a): `INDUSTRY_employment_ratio` into mechanised output.** Qing granular
  / ROW coarse (D6). LIVE for the 4 pre-wired goods → boot-test their output delta.
- **I5.5 — Close rare_alloys consumption sink (D10)** BEFORE any un-gate that could produce it.
- **I6 — UN-GATE (D1) for the remaining 20 goods: extend `GOODS_governorship_produce_all` to all 24 via
  the mechanised-only macro.** The switch-on for the new goods. Heavily reviewed + boot-tested.
- **I7 — Prices for all producible goods (D7).**
- **I8 — Manufacturing wealth → workers (D4b): reweight manufacturing income shares.** Closes the
  employment loop.
- **I9 — Loc + GUI tooltips (D8).**

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
- (Phase 3+ increments logged here as they land.)
