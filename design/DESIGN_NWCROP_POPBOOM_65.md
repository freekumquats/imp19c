# DESIGN — Flesh out the New World pop-boom: generic crop buildings + CHI boom reader + events/missions (#65)

**Status:** implementation design, 2026-08-10. Grounded in research/RESEARCH_TRADE_GOOD_DIFFERENTIATION_66.md (#66) + the existing se_QING_COLON.txt boom machinery. Depends on #64 (correct crop geography) + #62 (demand double-count). Design-note-first → adversarial review → implement → verify boot. freekumquats / merge-overnight.

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

## #66 verdict that shapes #65
- **maize / potato / sweet_potato ALREADY earn their keep** — food basket + colonization diffusion + capacity lift + pop-pressure. A genuine 4th differentiation axis (demographic/settlement) no other good has. #65 makes this VISIBLE (buildings + events), doesn't invent it.
- **peanut / chili are flat** — luxury-base demand ONLY, no building, no BOM, no food path. They ride the diffusion sweep but carry zero economic distinctiveness. #65 must EITHER give them a bespoke hookup (peanut→oil pressing; chili→processed_foods/pharma input) OR the user's stated alternative (retire from distinct-good status). Since the user's intent is "make them earn their keep," LEAN toward the hookup, not retirement.

## THE DESIGN — three concrete layers

### A. GENERIC New World crop processing building(s)
A generic building (available to ALL countries — Europe processed NW crops too) whose `allow` block gates on the province growing a NW crop, producing a processed output / capacity benefit. Mirror the existing generic production-building shape (common/buildings/) — NOT a Qing-specific building, NOT one of the ~2 Qing-excluded generics.

**Design choice — one building or per-crop?** LEAN: a SINGLE generic `new_world_farmstead` (or similar) building available where any of the 5 crops grows, giving a modest local food/capacity output — this is the concrete on-map object the CHI boom reader keys on (below), and it's the "buildings tied to the NW crops" the user asked for. It reinforces the capacity lift with a player-BUILT object (agency), rather than the purely-automatic province modifier.
- PLUS, to make peanut/chili earn their keep (the #66 gap): a generic **oil/condiment press** consuming peanut/chili as a BOM input into an existing manufactured good (peanut→oil; chili→processed_foods/pharma), per #66's recommendation. This gives the two flat crops a real BOM consumer role (#66 axis 3, the densest differentiation axis) — the thing they lack.
- **VERIFY at impl:** the exact generic-building schema (allow/trade_goods gate, production, potential), that a `trade_goods = <crop>` allow-gate works for a building, and which manufactured good peanut-oil/chili can feed (grep INDUSTRY_svalues.txt for oil / processed_foods / pharmaceuticals recipes). Do NOT invent a new manufactured good (perf cost, #66) — hook into an EXISTING recipe.

### B. CHI boom reader keyed on the generic building
The Qing-specific effect (user ruling 2): a CHI-scoped pulse/reader that counts the generic NW-crop buildings in Qing territory and drives a Qing pop-boom bonus — extending the EXISTING qing_migr_crop_boom / capacity machinery, NOT a parallel system. Concretely: fold a term into the existing boom driver that scales with the count of the generic building in CHI provinces (a "the more the empire invests in New World agriculture, the stronger the boom" coupling). Reuse the proven every_owned_province-count-into-a-scratch-var idiom (or the area-iterate idiom if subject-held). CHI-only; the generic building itself stays available to everyone, but only the Qing reads it for the boom (the proven pattern).

### C. Events + a mission beat (player-legible boom)
- **Event(s):** flesh out / add to the qing_migration.20-22 boom chain so the player SEES the New World crop boom as narrative beats tied to concrete triggers (e.g. crossing a threshold of NW-crop provinces or buildings). Court-slot / cooldown throttled per #55/#107. Percentages-N/A (deterministic). Loc, no macro-in-LOG.
- **Mission beat:** a mission-tree node (in the existing Qing colonization/population tree — DESIGN_COLONIZATION_SPLIT / the colonization arcs) rewarding the spread of NW-crop agriculture (build N farmsteads / reach N crop provinces → a capacity or growth reward). Reuse the proven mission-node idiom; do NOT build a whole new tree.

## Dependencies / ordering
- **#64 FIRST** (correct geography) — #65's buildings/reader key on crop provinces; building on the backwards geography would reinforce the error.
- **#62** (demand double-count) — independent but same crop-demand area; land #62 so the food-basket is correct before the boom reads it.
- Then #65.

## RISK
- **R1 [HIGH] — perf: no new manufactured good, no new full-map sweep.** #66 is explicit: adding a trade good has real perf cost. Peanut/chili BOM must hook an EXISTING recipe. Any new building-count sweep must be O(cheap) + throttled (reuse the existing boom pulse's cadence, don't add a new full-map every_province pass — the se_QING_COLON.txt:278 [#83 C1 perf] single-pass lesson).
- **R2 [HIGH] — generic building, NOT Qing-specific** (user ruling 1). It must be available to all; only the CHI READER is Qing-specific. Do NOT put it on the ~2-building Qing-exclude list. Verify against the building-availability architecture.
- **R3 [MED] — don't double-count the capacity boom.** The global qing_nwcrop_abundance lift already fires per crop province. A player-built farmstead adding MORE capacity on the same province must be a deliberate, bounded stack (or the building replaces the automatic modifier where built) — not an unbounded double-lift. Decide + bound at impl.
- **R4 [MED] — the boom stays a BOOM, not a runaway.** The CHI reader term must be bounded (the existing boom is already tuned); a building-count term must be capped so mass farmstead-building can't explode Qing population past the historical ~High-Qing boom. Tune + verify on the pop logs.
- **R5 [LOW] — peanut/chili retirement is the fallback, not the plan.** If the BOM hookup proves unbuildable (no suitable existing recipe), the documented alternative is retiring them per imp19c-defunct-trade-goods — but that's a LAST resort (the user wants them to earn their keep). Flag, don't silently pick.

## Files (anticipated — confirm at impl)
- `common/buildings/` — the generic NW-crop farmstead + (peanut/chili) press building(s).
- `common/script_values/INDUSTRY_svalues.txt` — the peanut-oil / chili BOM recipe hookup (into an existing mfg good).
- `common/scripted_effects/se_QING_COLON.txt` (or the boom pulse) — the CHI building-count boom-reader term.
- `events/imp19c_mod_events/qing_migration_events.txt` — flesh out the boom events.
- the Qing colonization/population mission tree file — the mission beat.
- `localization/english/` — building names, event/mission loc.
- NO trade_goods/00_imp19c.txt change (closed door, #66). NO new trade good (perf, R1).

## Verify (boot)
- The generic NW-crop building(s) exist + are buildable by the Qing AND a European power (generic, R2).
- Peanut/chili now feed a real BOM recipe (they have a consumer — #66 gap closed) OR (fallback, flagged) are retired.
- The Qing boom reads the building count + drives a BOUNDED boom (R4) — pop logs show a boom, not a runaway; a non-Qing builder gets the building but NOT the Qing boom (R2 reader-gating).
- No new full-map sweep / no new trade good (R1). Capacity not double-counted unbounded (R3).
- Events/mission beat fire + read correctly; court-slot throttled; loc present; no macro-in-LOG.

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
