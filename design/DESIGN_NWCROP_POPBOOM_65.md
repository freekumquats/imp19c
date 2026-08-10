# DESIGN — Flesh out the New World pop-boom: ONE generic farmstead + ONE mission beat (#65)

**Status:** implementation design, 2026-08-10, **REVISED post-review (rev-65 corrections folded into the body; round-2 review pending). The design was materially over-scoped on two wrong premises and is now cut to the minimal slice.** Grounded in research/RESEARCH_TRADE_GOOD_DIFFERENTIATION_66.md (#66) + the existing se_QING_COLON.txt boom machinery. Depends on #64 (correct crop geography) + #62 (demand double-count). Design-note-first → adversarial review → implement → verify boot. Do NOT implement until a CLEAN review passes. freekumquats / merge-overnight.

**Round-1 review (rev-65) verdict: PROCEED-WITH-CORRECTIONS (large).** The boom spine is nearly complete already; two load-bearing assumptions in the original three-layer plan were wrong (the BOM hookup targets a DORMANT subsystem; the "boom reader" targets a driver that doesn't exist). The body below is the corrected MINIMAL SLICE. Round-1 findings preserved verbatim at the bottom as an audit trail.

## What the user asked
"Flesh out the New World pop-boom with buildings/events/missions specifically tied to the New World trade goods, to make the crop goods earn their keep." Plus the two architecture rulings (user, this session):
1. **NW-crop buildings must be GENERIC** — "obviously Europe ate crops from the New World too." NOT Qing-specific. (memory: building-availability-architecture — generic buildings ARE available to Qing; only ~2 are Qing-excluded.)
2. **The Qing difference is a POP-BOOM MECHANIC that READS those same generic buildings** and triggers Qing-specific effects. (The proven pattern: generic building + CHI reader mechanic = Qing effects without a Qing-specific building.)

## What already exists (do NOT rebuild — verified)
- `qing_nwcrop_abundance` province modifier + `QING_COLON_apply_nwcrop_capacity` (se_QING_COLON.txt:276-325): a GLOBAL every_province sweep stamping a `local_population_capacity` lift on every province growing any of the 5 crops. This IS the structural crop→capacity coupling. Global by design (the lift is a property of the crop, not the polity).
- The narrative boom: `qing_migration.20/.21/.22` + `qing_migr_crop_boom` (empire-wide Qing growth), `QING_COLON_spread_newworld_crops` (#78, milestone spread), `QING_COLON_nwcrop_diffuse` (#384, organic time-based diffusion). All ROOT=CHI.
- The pop-pressure / involution penalty: se_QING_POPULATION.txt:92-100.
- Demand: maize/potato/sweet_potato in the dynamic food basket (#279); peanut/chili luxury-only.

**So the "pop-boom" spine EXISTS.** #65 is FLESHING IT OUT with the concrete objects the user named (buildings/events/missions) so the boom is player-legible + the crops (esp. the two flat ones) earn their keep.

## #66 verdict that shapes #65 (corrected)
- **maize / potato / sweet_potato ALREADY earn their keep** — food basket + colonization diffusion + capacity lift + pop-pressure. A genuine 4th differentiation axis (demographic/settlement) no other good has. #65 makes this VISIBLE (a player-buildable object), doesn't invent it.
- **peanut / chili are LOWER-differentiation, but NOT flat dead-weight** (rev-65 C2 corrected the stale #66 claim): they DO feed fulfilled_food_need (DEMAND_food_svalues.txt:101-102) and ride the diffusion sweep (se_QING_COLON.txt:296-297). Their only gap vs the other 3 is DYNAMIC-food-BASKET membership (DEMAND_num_food_goods, #279 divisor) — a narrow **#62 demand-svalue decision, NOT a #65 building/BOM**.
- **The BOM hookup idea is DROPPED (rev-65 C1):** peanut→processed_foods / chili→pharmaceuticals is buildable, but the industrial-BOM demand path is DISABLED (se_DEMAND.txt:6-9; only food+luxury demand live) and gated on debug-only `INDUSTRY_factories_assigned_*` vars (#133) — it delivers ZERO demand in the 1763 agrarian-boom era and needs industrial-era factories that don't exist then. It does NOT make them earn their keep in any era the mod exercises. Route peanut/chili individual differentiation to #62 if wanted.

## THE DESIGN — MINIMAL SLICE (rev-65: the boom spine is nearly complete; #65 = one building + one mission beat)
The pop-boom is NOT thin. Already live + player-legible: the arrival→reckoning→blessing/crisis chain (qing_migration.20/.21/.22/.23), golden/overpopulation branching, the global capacity sweep, organic diffusion, involution+famine+relief coupling (se_QING_POPULATION.txt:92-119), heartland→frontier migration. The one concrete object the user named that's genuinely MISSING is the BUILDING (player agency vs the purely-automatic modifier). So #65 = two objects:

### A. ONE generic "new world farmstead" building (Layers A+B of the old plan COLLAPSED into this)
- **Generic, available to all** (user ruling 1; Europe grew NW crops too). Authored in a GENERIC building file (e.g. 00_infrastructure or a new generic file) — **NOT** `row_production_buildings.txt` (its two ROW buildings are Qing-EXCLUDED via `potential { owner NOT chinese_group/jurchen }` :47-51 — copying that gate would invert the ruling), and **NOT** `qing_*_buildings.txt` (culture-gated the opposite way). OMIT any culture exclusion.
- **`potential` OR-gated on the 5 crops' trade_goods** (the proven shape: row_production_buildings.txt:28,80 uses a `trade_goods=X` gate).
- **Gives a SMALL, explicitly-bounded local benefit ON THE BUILDING** — a few points of `local_population_capacity` + minor local food / lower-strata output. This is the crop→pop coupling made PLAYER-DRIVEN, and it is the same lever the old "Layer B CHI reader" wanted — so **there is NO separate boom reader** (rev-65 C3: the boom is a flat event-applied country modifier, qing_migration_modifiers.txt:38-57, with NO continuous per-pulse driver to "fold a term into"; the honest lever is a local modifier on the building that reads naturally). Layers A and B collapse into this one object.
- **Capacity double-count is a deliberate, bounded STACK, not avoided** (rev-65 C4): the global `qing_nwcrop_abundance` already stamps `local_population_capacity=8` on every crop province, idempotent + self-correcting (se_QING_COLON.txt:286-323) — "the building replaces the modifier" is NOT viable (the sweep re-adds it :313-315). So the farmstead adds a SMALL extra on top (state the number at impl, same tier as the 6-10 band at modifier :69), tuned on pop logs so it doesn't push the Qing past the historical High-Qing boom.

### B. ONE mission-task beat (reuse the existing tree)
- A task in the EXISTING `qing_colonization_missions.txt` (task shape :88-119: allow/on_start/on_completion, custom_tooltip, add_country_modifier): "spread New World agriculture."
- **allow-gated on the cheap counter idiom** `any_owned_province = { has_building = new_world_farmstead count >= N }` (proven se_QING_SELFSTR.txt:141) — evaluated where the tree already evaluates, NO new on_action, NO new every_province sweep (rev-65 C6).
- completion grants a modest ONE-SHOT capacity/growth country modifier. Reuse the tree; build no new tree.

### C. Events — the chain ALREADY IS the boom narrative (rev-65 C7#4)
Do NOT rebuild the qing_migration.20-23 chain. At MOST one optional new beat, court-slot throttled via `qing_gc_event_slot_used` (00_monthly_country.txt:80). Likely NONE — the narrative is complete. (This is a scope trim the review licensed, not a deferral.)

## Dependencies / ordering
- **#64 FIRST** (correct geography) — the farmstead's `potential` reads crop provinces; building on the backwards geography would reinforce the error.
- **#62** (demand double-count + the peanut/chili basket decision) — land it so the food-basket is correct first.
- Then #65.

## RISK
- **R1 [HIGH] — perf: no new manufactured good, no new full-map sweep, no new on_action.** The mission counter uses the cheap `any_owned_province count>=N` idiom in the existing tree eval (C6). No BOM hookup (dropped, C1). No new trade good.
- **R2 [HIGH] — generic building, NOT Qing-specific** (user ruling 1). Author in a generic file, OMIT the culture exclusion (C5). The building is available to all; the Qing-ness is that the boom machinery + mission are CHI-scoped — but the farmstead's local capacity benefits ANY owner (as NW crops did historically).
- **R3 [MED] — capacity stack is bounded + deliberate** (C4): the farmstead's extra capacity stacks on the automatic qing_nwcrop_abundance=8; state the small number at impl, tune on pop logs. Not an unbounded double-lift.
- **R4 [MED] — boom stays a BOOM, not a runaway.** The farmstead's local capacity + the one-shot mission reward must be small enough that mass farmstead-building can't explode Qing pop past the historical High-Qing boom. Tune + verify on pop logs.
- **R5 [DROPPED] — peanut/chili "earn their keep" via BOM is not the plan** (C1): the subsystem is dormant. Their (narrow) differentiation gap is a #62 basket decision. NOT retirement (they have a real food role, C2), NOT a #65 building.

## Files (confirmed post-review)
- a GENERIC `common/buildings/` file (00_infrastructure or a new generic file — NOT row_production_buildings.txt, NOT qing_*_buildings.txt) — the ONE generic farmstead. **BOM/UTF-8** (row_production_buildings.txt:20 header).
- `qing_colonization_missions.txt` — ONE mission-task beat (existing tree).
- `localization/english/` — building name + mission loc. BOM.
- At most: the boom-events file (the chain is `qing_frontier_migration_events.txt`, NOT `qing_migration_events.txt` — that file doesn't exist) for ONE optional beat; likely untouched.
- NO INDUSTRY_svalues.txt BOM hookup (dropped). NO se_QING_COLON.txt boom-reader term (collapsed into the building). NO trade_goods/00_imp19c.txt. NO new trade good.

## Verify (boot)
- The generic farmstead exists + is buildable by the Qing AND a European power (generic, R2), `potential`-gated on the 5 crops.
- Its local capacity/output applies; the STACK on qing_nwcrop_abundance is bounded (R3/R4) — pop logs show a boom, not a runaway.
- The mission-task beat's allow-gate reads the farmstead count (cheap idiom) + completion grants its one-shot reward.
- No new full-map sweep / no new on_action / no new trade good / no BOM edit (R1). peanut/chili unchanged here (their basket question is #62).
- Loc present; any optional event court-slot throttled; no macro-in-LOG.

## Traps / rules
- Generic building (user ruling). No Qing-specific building. See §CORRECTIONS for the collapsed A/B + dropped BOM.
- No new trade good. No new full-map every_province sweep / no new on_action.
- common/buildings BOM/UTF-8; loc BOM; missions no-BOM/LF — verify per file. Brace balance. RHS var-vs-literal. No macro/# in LOG.
- Reuse existing boom/mission machinery; don't parallel-build.
- #64 + #62 land first. Design-note-first → adversarial review → implement → verify boot.

---

## ADVERSARIAL DESIGN-REVIEW CORRECTIONS (rev-65, 2026-08-10) — PROCEED-WITH-CORRECTIONS (large; design was over-scoped on two wrong premises)
The boom spine is nearly COMPLETE already; #65's real deliverable is ONE generic building + ONE mission beat. Two load-bearing assumptions were wrong. These corrections SUPERSEDE Layers A/B/C above.

**C1 [CRITICAL] — DROP the peanut/chili BOM hookup.** It IS buildable (processed_foods INDUSTRY_svalues.txt:3021 / pharmaceuticals :2441 have full recipe families; adding an ingredient = proven 4-svalue + 2-line shape) — but the whole industrial-BOM demand path is HALF-WIRED and OFF: `DEMAND_set_demand_from_industry_all` is DISABLED (se_DEMAND.txt:6-9; only food+luxury demand is live), and the `INDUSTRY_factories_assigned_*` gates are set only by the DEBUG path (memory imp19c-manufactured-goods-risk / #133). So a peanut→processed_foods hookup delivers ZERO demand in the era #65 cares about (the 1763 agrarian boom), and requires industrial-era factories that don't exist then. => do NOT use BOM as the differentiation answer. peanut/chili stay flat luxuries riding the diffusion sweep (which they already do). If they must be individually differentiated, that's a #62 food-BASKET decision, NOT a #65 building (see C2).

**C2 [HIGH] — #66's "peanut/chili have NO food path" is STALE; they already have a food role.** DEMAND_food_svalues.txt:101-102 already ADDS GOODS_governorship_peanut_produced + _chili_produced to DEMAND_fulfilled_food_need_governorship (the "quarter-food" tier, divide=2 :108); both are in the capacity sweep (se_QING_COLON.txt:296-297) + diffusion snapshot (:418-419) identically to the other three. The ONLY gap vs maize/potato/sweet_potato is membership in the DYNAMIC food basket / DEMAND_num_food_goods (#279 divisor) — a narrow #62 demand-svalue decision, NOT a #65 building. Re-verify + correct the #66 digest's "luxury-only" claim.

**C3 [HIGH] — Layer B's "fold a term into the boom driver" is architecturally IMPOSSIBLE; collapse A+B into the building.** There is NO continuous boom driver to fold into — the boom is a FLAT event-applied permanent country modifier (qing_migr_crop_boom/_golden/_overpopulation, qing_migration_modifiers.txt:38-57, added once by qing_migration.20 a/b at qing_frontier_migration_events.txt:179,205, swapped by .22/.23; global_population_growth is a fixed 0.10/0.25). To "scale the boom with building count" you'd invent a new graduated per-pulse modifier band (over-scope, R4 runaway) OR — the honest cheap answer — put a small local_population_growth/capacity ON THE BUILDING and let it read naturally. That's the SAME lever as Layer A's farmstead → **Layers A and B collapse into one object; drop the CHI reader entirely** (it implies a mechanism that doesn't exist).

**C4 [MED] — R3 capacity double-count: state the number, don't defer.** qing_nwcrop_abundance already stamps local_population_capacity=8 on every crop province, idempotent + self-correcting (se_QING_COLON.txt:286-323; modifier qing_migration_modifiers.txt:70-72). "Building replaces the modifier" is NOT viable (the sweep re-adds it next call, :313-315). => the farmstead adds a SMALL explicitly-bounded EXTRA capacity/output (a few points, same tier as the 6-10 band at modifier :69), accepted as a deliberate stack, tuned on pop logs. Design must NAME the number at impl, not defer.

**C5 [MED] — generic-building file landmine.** The proven generic shape (row_manufactory/row_plantation, row_production_buildings.txt:28,80) with a `trade_goods=X` OR-gate in `potential` is confirmed buildable — BUT those two are Qing-EXCLUDED via `potential { owner NOT chinese_group/jurchen }` (:47-51). If the farmstead is authored in that file or copies that gate it becomes Qing-excluded (inverts user ruling 1). => author it in a GENERIC file (e.g. 00_infrastructure / a new generic file), NOT row_production_buildings.txt, and NOT qing_*_buildings.txt (culture-gated the opposite way). OMIT the culture exclusion.

**C6 [MED] — perf: no reader, cheap counter idiom if any.** Per C3 the building-count reader shouldn't exist. If a CHI counter is still wanted for the mission task, use `any_owned_province = { has_building=X count>=N }` (proven se_QING_SELFSTR.txt:141) inside the EXISTING qing_mechanics pulse (00_monthly_country.txt:67, quarterly, court-slot throttled :80-81) — NO new on_action, NO new every_province pass.

**C7 [HIGH] — over-scope: buildings+BOM+reader+events+mission ≈ 4× the ask. RECOMMENDED MINIMAL SLICE:**
1. **ONE generic "new world farmstead"** building in a generic file, `potential` OR-gated on the 5 crops, NO culture exclusion, giving a SMALL bounded local capacity + minor food/lower-strata output (C4 number stated; C5 file stated). Its local capacity IS the crop→pop coupling made player-driven. Layers A+B collapse here — no separate reader.
2. **ONE mission-task beat** in the EXISTING qing_colonization_missions.txt (task shape :88-119): "spread New World agriculture," allow-gated on the cheap building-count idiom (C6), completion grants a modest one-shot capacity/growth country modifier. Reuse the tree; build no new tree.
3. **DROP the peanut/chili BOM hookup** (C1). Route peanut/chili individual differentiation to #62 (food-basket membership, C2) if the user insists.
4. **Events: the qing_migration.20-23 chain IS already the boom narrative** — do NOT rebuild it. At most ONE optional beat, court-slot throttled (qing_gc_event_slot_used, 00_monthly_country.txt:80).

**PROCESS FIX:** the Files section cites `events/imp19c_mod_events/qing_migration_events.txt` — that file does NOT exist; the boom chain is `qing_frontier_migration_events.txt`. Correct the path (and per the minimal slice, the events edit is at-most-one-beat / likely none).

**CONFIRMED SOUND:** no new trade good needed; the generic-building shape + OR-gate is proven; #64 + #62 land first (the farmstead potential reads crop provinces).
