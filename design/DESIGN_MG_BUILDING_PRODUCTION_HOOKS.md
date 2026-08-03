# Manufactured-Goods — Named-Building Production Hooks (Design)

**Branch:** to isolate off `merge-overnight` (follows the #133 MG isolation discipline).
**Relates to:** #133 (manufactured-goods system), [logistics P2] arsenal/depot munitions hook,
[[imp19c-manufactured-goods-build-rules]], [[imp19c-add-building-level-respects-potential]].
**Status:** Phase 2 (design). Running decision log; nothing implemented yet.
**User ruling (2026-08-02):** the current single-hook state is a **GAP to close** — thematic
manufacturing buildings SHOULD contribute a direct production term to their good, mirroring the
arsenal→munitions hook, across BOTH the generic and Qing building sets.

---

## 1. PROBLEM STATEMENT

The topbar "Military supplies" figure (`ingame_topbar.gui:817`, var `MILITARY_supplies_country`;
change = svalue `MILITARY_supplies_balance_country`, `INCOME_svalues.txt:1018`) is:

```
balance = MILITARY_supplies_income_country  +  consumed_quarterly (negative)
```

`MILITARY_supplies_income_country` (`INCOME_svalues.txt:909`) = the sum, over governorships, of the
**fulfilled** military base-demand for these goods, each docked by its shortage fraction:
`early_munitions`, `late_munitions`, `clothing`, `pharmaceuticals`, `construction_materials`
(and `early_artillery`/`late_artillery` on the consumption side). So the topbar number rises only
when the underlying #133 goods economy actually **produces** enough of those goods to fulfil military
demand.

### 1.1 The gap
Production of every #133 manufactured good flows through exactly TWO channels plus ONE exception:
- **Cottage** — `COTTAGEIND_produced_<good>` (pop/household, no named building).
- **Mechanised factory** — a generic `IND_industrial_estate` slot assigned to the good
  (`INDUSTRY_factories_assigned_<good>`).
- **Exception (the only named-building hook in the whole system):** the [logistics P2] arsenal/depot
  walk in `GOODS_governorship_munitions_infra_output_compute` (`GOODS_svalues.txt:2749`), which adds
  `num_of_arsenal_building × 2` + `num_of_military_depot_building × 1` munitions per governorship,
  gated on `owner = { invention = tech_firearms }`.

Confirmed by audit: across the entire `GOODS_svalues.txt`, the **only** `num_of_*_building` counters
referenced are `arsenal_building` and `military_depot_building`. **No other building — generic or
Qing — contributes to any manufactured good as itself.** Every thematic manufacturing building is a
pure *modifier-grant + industry-slot-gate*; it produces its themed good only if the province also
happens to hold a generic industrial estate (or cottage) assigned to it.

### 1.2 Two production models must NOT be conflated
1. **`base_resources = N`** — vanilla engine RAW-good province output (emits N of the province's
   `trade_goods`). Carried by raw-extraction buildings (blast furnace, coal mine, silk filature,
   salt yard, cotton workshop, ROW plantation/manufactory, resource-gathering op). This is the
   **raw** layer (iron, coal, silk, salt, cotton) and is **out of scope** — it is not a manufactured
   good and does not touch the topbar.
2. **The #133 scripted `GOODS_governorship_<good>_produced` walks** — the manufactured layer. THIS is
   where the hooks are missing. This design adds named-building production terms ONLY here.

---

## 1.3 WAS THIS NOT ALREADY CLOSED? (reconciliation with the merged #133 MG work)

The manufactured_goods branch WAS merged (`bea80a969 Merge manufactured_goods into merge-overnight`),
and it built a large, working system. It is important to state precisely what it did and did **not**
close, because `DESIGN_MANUFACTURED_GOODS.md` §D6 *reads* as if this gap were addressed.

**What #133 actually built (verified in current history):**
- The production MATH engine per good: `INDUSTRY_production_rate_X`, `_base`, `_multiplier`,
  employment scaling (I5), BOM/ingredient maluses (I3), prices (I7/D7), stockpiles, 24 goods
  un-gated (I6), 5 new goods (#144 I12), cottage paths (I10).
- The FACTORY path: goods are produced by **generic `IND_industrial_estate` slots**, assigned to a
  good by the player via `industrial_goods_buttons.txt` (writes `INDUSTRY_factories_assigned_X`).
  `INDUSTRY_governorship_total_industry_slots` (`INDUSTRY_svalues.txt:55`) counts **only**
  `num_of_IND_industrial_estate` as slots.
- The ONE named-building production hook: arsenal/depot → early_munitions ([logistics P2], a RIFLES
  design deliverable, `DESIGN_LOGISTICS_RIFLES.md:60-72`), added as a flat per-building infra term.

**What it did NOT close — the actual gap:**
- `DESIGN_MANUFACTURED_GOODS.md` §D6 (line 388) asserts "Qing … full per-good mechanised production
  through the Qing named works." That binding was **never implemented.** The three purely-manufacturing
  Qing works (`qing_machine_works`, `qing_textile_mill`, `qing_navy_yard`) are **modifier-only** —
  `local_output_modifier`, `local_proletariat_output`, etc. — which boost POP output, not the factory
  good. (`qing_steel_works` is the fourth candidate but is a RAW emitter, `base_resources = 2` on iron —
  see §3.2/OQ2, a distinct case.) The modifier-only works:
  - do NOT provide industry slots (only `IND_industrial_estate` does), and
  - do NOT add a production term to any good (only arsenal/depot do, for munitions).
- So a province with a Jiangnan Arsenal produces munitions **only** if it also holds a generic
  industrial estate assigned to munitions (or a cottage recipe). The named work itself contributes
  nothing to the good it thematically makes.

**Conclusion.** #133 closed production for the *goods* (the engine) but left the *building→good
binding* open for every named manufacturing building except arsenal/depot. §D6 is an unfulfilled
design intent, not a shipped feature. This document is the design to finally honour §D6 — generalising
the arsenal hook to the rest of the named manufacturing buildings.

## 1.4 HOW THIS DESIGN DIFFERS FROM THE EXISTING MG IMPLEMENTATION

| Dimension | Existing #133 (shipped) | This design (new) |
|---|---|---|
| Who produces a manufactured good | Generic `IND_industrial_estate` slots (player-assigned) + cottage; arsenal/depot for munitions only | ADDS: named manufacturing buildings emit their themed good directly |
| Named Qing works role | Modifier-only (pop output, civ, research); zero direct goods output | Gain a flat per-building production term in their good's `_produced_mechanised` |
| Building→good binding | Exists ONLY for arsenal/depot→munitions | Generalised to machine works→munitions/artillery, textile mill→clothing, navy yard→naval_supplies, etc. |
| §D6 "Qing granular via named works" | Aspirational, unwired | Actually implemented |
| Mechanism | — | Reuses the proven [logistics P2]/[perf #71] cached infra-walk idiom verbatim |
| Raw layer (`base_resources`) | Unchanged raw province output | UNCHANGED (explicitly out of scope, N1) |

This is **additive and orthogonal** to the factory-slot path: the new term keys off `num_of_<building>`,
the estate path off `INDUSTRY_factories_assigned_X`, cottage off `COTTAGEIND_produced_X` — three
disjoint variables, so no double-count (see R1).

## 2. GOALS / NON-GOALS

**Goals**
- G1. Give each thematic MANUFACTURING building a direct, scripted production term for the good it
  canonically makes, reusing the arsenal hook's IDIOM (a per-governorship building-count × output-rate
  term added into that good's `_produced_mechanised` svalue) — but with PURE-PRODUCER semantics (supply
  only, no demand entry on the finished good), which differs from the arsenal's consume+produce model
  (see G3/§4).
- G2. Cover BOTH sets: generic (`IND_*`, `arsenal`/`depot` already done) and Qing (Self-Strengthening
  works) — asymmetric fidelity preserved (Qing granular, ROW abstract) but no set left with a
  flavour-vs-output mismatch.
- G3. Topbar-balance honesty. The topbar income term `MILITARY_supplies_income_country`
  (`INCOME_svalues.txt:909`) sums **fulfilled** `DEMAND_<good>` per governorship, docked by the good's
  shortage fraction — i.e. it is **demand-capped**: producing more of a good can only drive its shortage
  fraction toward 0 (fulfilment toward 1.0), never push income above demand. So adding SUPPLY-only for a
  producing building does NOT inflate the balance — it does exactly the intended thing (fewer shortages).
  This RETIRES the earlier "must add matching demand or the topbar inflates" worry (see §4, R2). The one
  real rule that remains: a building must not be double-credited as producing the SAME good twice (R1),
  and must not be modeled as consuming what it makes.
  NOTE on the arsenal precedent: the arsenal is counted on BOTH sides — it consumes munitions/artillery/
  construction_materials (`DEMAND_svalues.txt:1586/1936/1961/1990`, beside `num_of_fortress_building`)
  AND produces munitions (supply, `GOODS_svalues.txt:2761`). It is a consume-and-net-produce building
  (a garrison that also manufactures). The new works here are modeled as **pure producers** (a factory
  consumes raw inputs via the BOM, not finished military goods), so they DEVIATE from the arsenal's
  two-sided pattern — this is a deliberate choice, not an exact mirror (see §4).
- G4. Performance: the arsenal walk is already cached (`munitions_infra_cached`, [logistics-perf #71]).
  Any new per-good building walk must use the SAME cache-or-compute idiom, never an uncached province
  re-walk (these svalues evaluate >1×/quarter).

**Non-goals**
- N1. NOT touching `base_resources` raw output (§1.2.1).
- N2. NOT converting named buildings into industrial-estate slots (they stay modifier buildings; the
  hook is an ADDITIVE flat term, orthogonal to the factory-assignment path — so no double-count with
  a co-located estate, because the estate path keys off `INDUSTRY_factories_assigned`, a different var).
- N3. NOT re-scoping employment/pop mechanics (a later #133 phase).

---

## 3. THE AUDIT — building → good it should produce

Legend: **RAW** = `base_resources` raw emitter (out of scope, N1). **MFG-HOOK** = candidate for a new
production term. **MODIFIER-ONLY** = grants modifiers, no goods (leave as-is unless flavour demands).

### 3.1 Generic set
| Building | File | Current | Themed manufactured good | Verdict |
|---|---|---|---|---|
| `arsenal_building` | 00_military | MFG-HOOK (done) | early_munitions | ✅ already hooked |
| `military_depot_building` | 00_military | MFG-HOOK (done) | early_munitions (warehousing) | ✅ already hooked |
| `IND_blast_furnace_building` | IND_heavy | RAW (base=2, cast iron) | **steel / construction_materials** | **HOOK CANDIDATE** — flavour "cast iron for rails, machinery, structures". Decide: is its base_resources=2 (on an iron province) the intended abstraction, or does it also warrant a `construction_materials`/`steel` mfg term? |
| `IND_coal_mine_building` | IND_heavy | RAW | coal (raw) | RAW — out of scope |
| `IND_electric_plant_building` | IND_heavy | MODIFIER-ONLY | (utility, electronics/motors enabler) | Review: likely modifier-only (infra), no direct good |
| `IND_gasworks_building` | IND_heavy | MODIFIER-ONLY | (utility) | modifier-only |
| `IND_industrial_estate` | 00_industrial | slot-provider | ALL (via assignment) | leave — this IS the generic factory path |
| `IND_resource_gathering_operation` | 00_industrial | RAW (base=1) | raw | out of scope |
| `row_manufactory_building` | row_production | RAW (base=2) | ROW abstraction | **REVIEW** — a "manufactory" emitting base_resources (raw) is itself suspect; but ROW is deliberately abstract (asymmetric fidelity). Likely leave; record rationale. |
| `row_plantation_building` | row_production | RAW (base=2) | raw crops | out of scope |

### 3.2 Qing set (Self-Strengthening + production)
| Building | File | Current | Themed manufactured good | Verdict |
|---|---|---|---|---|
| `qing_machine_works_building` (江南製造局 Jiangnan Arsenal) | qing_industry | MODIFIER-ONLY | **early_munitions + early_artillery + machine_parts** | **PRIMARY HOOK** — flagship arms works; "casting arms and machine tools". |
| `qing_textile_mill_building` (機器織布局) | qing_industry | MODIFIER-ONLY | **clothing** | **HOOK** — "cotton/silk into cloth at scale". |
| `qing_steel_works_building` | qing_industry | RAW (base=2) | **steel / construction_materials** | **HOOK CANDIDATE** — "steel for rails, ships, machinery, modern arms". Same base_resources-vs-mfg question as blast furnace. |
| `qing_navy_yard_building` (福州船政局) | qing_industry | MODIFIER-ONLY | **naval_supplies / wooden_ships / steel_ships** | **HOOK** — shipyard; but ships are a distinct sub-question (recruit-speed modifier already present). |
| `qing_coal_mine_building` | qing_industry | RAW (base=2) | coal (raw) | out of scope |
| `qing_cotton_workshop_building` | qing_production | RAW (base=2) | raw cotton / cloth? | **REVIEW** — "clothed the empire"; is it raw cotton (RAW) or proto-clothing? Probably RAW (raw layer beneath cloth), leave. |
| `qing_silk_filature_building` | qing_production | RAW (base=3) | raw silk vs silk_cloth | **REVIEW** — filature = reeling raw silk → RAW; silk_cloth would be the mfg step (a mill). Leave as RAW. |
| `qing_porcelain_kiln_building` | qing_production | RAW (base=2) | porcelain | porcelain is a trade good; treat as RAW province output (leave) |
| `qing_tea_workshop` / `salt_yard` / `opium_poppy_farm` | qing_production | RAW | tea/salt/opium | out of scope (raw) |
| `qing_selfstr_wonder_building` | qing_selfstr | MODIFIER-ONLY | (national wonder) | modifier-only |
| `qing_military_*` (banner_garrison, green_standard_post, coastal_battery, horse_pasture, military_colony) | qing_military | MODIFIER-ONLY | (garrison/defence; horse_pasture→horses raw?) | garrisons CONSUME supply — do NOT hook to production. `horse_pasture` may be RAW horses. |
| all `qing_agriculture/works/fiscal/foreign/religion/scholarship/governance/granary/customs` | — | MODIFIER-ONLY | none | out of scope |

### 3.3 Confirmed HOOK list (subject to review-round pruning)
1. `qing_machine_works_building` → early_munitions (+ possibly early_artillery, machine_parts).
2. `qing_textile_mill_building` → clothing.
3. `qing_navy_yard_building` → naval_supplies (ships handled separately).
4. `qing_steel_works_building` / `IND_blast_furnace_building` → steel/construction_materials **IF**
   the base_resources abstraction is judged insufficient (open question OQ2).

---

## 4. PROPOSED MECHANISM (reuse the arsenal hook's IDIOM; pure-producer semantics)

For each good `X` gaining named-building production, add a cached infra walk parallel to the
munitions one:

```
GOODS_governorship_<X>_infra_output = {          # cached wrapper
    if   = { limit = { has_variable = <X>_infra_cached }  value = var:<X>_infra_cached }
    else = { value = GOODS_governorship_<X>_infra_output_compute }
}
GOODS_governorship_<X>_infra_output_compute = {
    value = 0
    if = {
        limit = { owner = { <appropriate invention gate, e.g. tech_weapon_manufacturing> } }
        every_governorship_state = { every_state_province = {
            add = { value = num_of_qing_machine_works_building  multiply = GOODS_machine_works_<X>_output }
            # ... other buildings feeding X ...
        } }
    }
}
```
Then in `GOODS_governorship_<X>_produced_mechanised` add `add = GOODS_governorship_<X>_infra_output`
(exactly as early_munitions:2717 adds the munitions infra term). Per-building output rates live in
their own tunable svalues (mirror `GOODS_arsenal_munitions_output = 2`).

**Cache:** extend the [logistics-perf #71] cache writer that currently produces `munitions_infra_cached`
to also write each new `<X>_infra_cached` in the same pass (one province walk per quarter, not one per
good). This is a REQUIRED part of the build, not an optimization afterthought (G4).

**Demand handling (G3) — RESOLVED, not symmetric.** The topbar income term is demand-capped
(`INCOME_svalues.txt:909`, see G3), so pure-supply producers do NOT inflate the balance — the earlier
"must add matching demand" concern is retired. The new works are modeled as **pure producers**: they
add to good X's SUPPLY and add no demand for X. This deliberately differs from the arsenal (which both
consumes and produces munitions because it is also a garrison). A factory's *inputs* are handled by the
existing #133 BOM/ingredient system (e.g. clothing already consumes textile_fibres/dye/livestock via
`INDUSTRY_malus_clothing_production_*`), NOT by a demand entry on the finished good. The ONE invariant
to enforce per building: it must not be credited producing the same good through two channels (R1), and
must not consume the finished good it makes.

---

## 5. OPEN QUESTIONS (resolve in design review, before impl)
- **OQ1.** Invention gating per building. Munitions uses `tech_firearms`; the machine works `allow`
  uses `tech_weapon_manufacturing`, the textile mill `tech_manufactories`. The production term should
  gate on the SAME invention as the good's demand appears (so you can't produce before you can
  meaningfully demand) — confirm each good's demand invention gate.
- **OQ2.** `base_resources` buildings (steel works, blast furnace) — their `base_resources` emits the
  province's RAW good (both gate `trade_goods = iron`), i.e. iron. A manufactured `construction_materials`
  term would be a DIFFERENT good, so it is NOT double-counting the same good. The real questions are
  (a) whether iron→construction_materials conversion should be modeled by these buildings at all, and
  (b) whether "steel" even exists in the #133 good set — `construction_materials` does; a distinct
  `steel` good is UNCONFIRMED (verify against `is_manufactured_tradegood` before referencing it). LEANING:
  leave `base_resources` as the raw iron layer; add a manufactured hook ONLY where the building's good is
  purely manufactured (munitions, clothing, naval_supplies) and has no `base_resources` today — i.e.
  hook the three modifier-only works, and treat steel_works/blast_furnace as a separate, later question.
- **OQ3.** Ships (`naval_supplies`, `wooden_ships`, `steel_ships`) via the navy yard — the yard already
  grants `local_ship_recruit_speed`. Is a goods production term additive-correct or does it
  double-count with recruit-speed? Possibly defer ships to a sub-phase.
- **OQ4.** Output-rate magnitudes. Arsenal=2, depot=1. What relative scale for a machine works (a
  major arms complex) vs a bare arsenal? Must not swamp the cottage/factory economy or trivialise
  the topbar. Needs a back-of-envelope against typical governorship demand.
- **OQ5.** ROW abstraction (`row_manufactory_building`): a "manufactory" that emits base_resources
  (raw) is arguably itself mis-modelled, but asymmetric-fidelity says ROW stays abstract. Confirm we
  deliberately leave ROW alone.
- **OQ6.** `add_building_level` potential trap ([[imp19c-add-building-level-respects-potential]]):
  none of the new hooks force-add buildings, so N/A — but any event that spawns these works must
  respect the city/potential gate.

---

## 6. STAGING (per MG build rule: design → review → impl → review, small steps)
1. **This doc → adversarial design review** (round 1). ✅ DONE 2026-08-02. Verdict: **premise TRUE
   (gap real, not closed by #133), audit complete, proceed.** Findings folded in: F1 (steel_works is
   RAW not modifier-only — 3 modifier-only works, not 4); F2 (stale `DEMAND_svalues.txt:1448` citation
   → real lines 1586/1936/1961/1990, fixed in doc AND at source in `GOODS_svalues.txt:2709` +
   `00_military_buildings.txt:26`); D1 (demand-symmetry resolved — topbar income IS demand-capped,
   §4/R2 rewritten, R2 retired); D2 (arsenal is consume+produce, our works are pure producers — §4/G1
   own the deviation); D3 (OQ2 reworded — base_resources=raw iron, not same-good double-count; verify
   `steel` exists in good set); D4 (per-province producer stacking noted in R1/R6, feeds OQ4).
   Remaining to resolve IN-DESIGN before impl: OQ1, OQ3, OQ4, OQ5 (OQ2/OQ6 leanings recorded).
2. Impl step A: the cache-writer extension (one province walk writes all `<X>_infra_cached`). Review.
3. Impl step B: ONE good end-to-end (clothing via `qing_textile_mill`) as the reference vertical —
   svalues + cache + demand-symmetry check + se_LOG wiring. Review.
4. Impl step C: remaining confirmed hooks, one good per commit. Review each.
5. Perf pass: confirm the cache holds; measure quarterly tick (compare `timetest_quarterly_tick`).
6. Boot-test on the separate machine (PUSH first, [[imp19c-testing-on-other-machine]]).

---

## 7. RISKS
- R1. Double-counting production (building hook + co-located industrial estate + cottage all crediting
  the same good). Mitigation: hook keys off `num_of_<building>`, estate off
  `INDUSTRY_factories_assigned`, cottage off `COTTAGEIND_produced` — three disjoint vars (verified: no
  Qing named work is an `IND_industrial_estate` nor counts toward `total_industry_slots`).
  STACKING NOTE (feeds OQ4): because the works gate only on capacity
  (`INDUSTRY_province_industry_capacity > num_of_IND_industrial_estate`) and do NOT consume a slot, one
  province can hold e.g. a `qing_textile_mill` (new flat term) AND a co-located estate assigned to
  clothing AND cottage — all three credit clothing additively. Not a bug, but it raises the stakes on
  OQ4 output-rate calibration: producers stack per-province, so a modest per-building rate can compound.
- R2. ~~Topbar inflation from supply-without-demand.~~ RETIRED — the topbar income term is demand-capped
  (`INCOME_svalues.txt:909`); pure-supply cannot exceed demand, it only reduces shortage. See G3/§4.
- R3. Perf regression from uncached per-good walks (G4). Mitigation: single-pass cache writer, hard
  requirement.
- R4. Scope creep into `base_resources`/raw layer or employment. Mitigation: N1/N3 fences.
- R5. Asymmetric-fidelity violation (over-modelling ROW). Mitigation: OQ5 explicit leave.
- R6. Output-rate calibration (OQ4) compounded by R1 stacking — a machine works + estate + cottage in
  one province could swamp demand and trivialise the topbar. Mitigation: calibrate against typical
  governorship demand with the stacking case in mind; tune in the perf/calibration pass (§6.5).
