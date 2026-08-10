# DESIGN — peanut + chili industrial demand via the LIVE cottage path (#68)

**Status:** Stage-0 diagnosis complete + design, 2026-08-10. Source-traced this session. Awaiting adversarial review before implement.

TERMINOLOGY: "BOM" = byte-order-mark file header ONLY. The manufacturing recipe (input goods a manufactured good consumes) is written out **bill of materials**, never abbreviated.

## STAGE 0 — DIAGNOSIS (traced, with git evidence)

### Why the cottage stubs exist (the "why", not just the "what")
`COTTAGEIND_produce_processed_foods` (+ motors/machine_parts/electronics/chemicals/petrochemicals/rare_alloys/steel_ships/late_munitions/late_artillery/refined_sugar/dyes) are empty bodies whose comment reads "CANNOT BE PRODUCED BY COTTAGE INDUSTRY". Git-blamed to **31aacdf79** — the ORIGINAL creation of se_COTTAGEIND.txt by Sobisonator ("Implemented manufactured tradegood cottage industries"). They were written as deliberate stubs **from day one** — NOT a regression, NOT a later disable. It is an intentional design boundary: the 24 manufactured goods split into
- **artisanal goods a household/workshop CAN make by hand → LIVE cottage**, and
- **modern factory-only goods → deliberate cottage stub** (exactly the goods #69's factory var-sim was meant to cover).

Full live/stub map (awk-verified over se_COTTAGEIND.txt):
- **LIVE:** clothing, luxury_clothing, furniture, luxury_furniture, alcohol, glass, **pharmaceuticals**, paper, silk_cloth, bronze, steel, wooden_ships, construction_materials, naval_supplies, early_munitions, early_artillery, gunpowder.
- **DELIBERATE STUB (factory-only):** motors, machine_parts, electronics, chemicals, petrochemicals, rare_alloys, steel_ships, late_munitions, late_artillery, **processed_foods**, refined_sugar, dyes.

### The LIVE cottage input→output→demand mechanism (traced end-to-end)
1. **Raw input cache** (se_COTTAGEIND.txt:86-180): once/quarter, `COTTAGEIND_raw_<good> = GOODS_governorship_<good>_produced` for ~30 goods — a read-only capacity proxy. `vegetables` and `whales` are cached; **`chili` is NOT** (not in the list).
2. **Produce recipe** (se_COTTAGEIND.txt:600-614): `COTTAGEIND_produce_pharmaceuticals` sets `COTTAGEIND_produced_pharmaceuticals = raw_vegetables + raw_whales`, then `COTTAGEIND_scale_production{ output=pharmaceuticals efficiency=5 }` scales it by pops × efficiency × tech (se_COTTAGEIND.txt:183+).
3. **Output to consumers** (GOODS_svalues.txt:3254): `GOODS_governorship_pharmaceuticals_produced` = cottage produced + mechanised (dead) — summed for consumers.
4. **Input demand-back** (the live channel): `DEMAND_<rawinput>` adds `var:COTTAGEIND_produced_<manufactured>`. PROVEN for clothing: `DEMAND_wool` (DEMAND_svalues.txt:725), `DEMAND_dye` (:1358), `DEMAND_textile_fibres` (:662) all `add = var:COTTAGEIND_produced_clothing`. This is how producing a cottage good creates demand for its inputs.
5. **Driver** is live quarterly: `COTTAGEIND_produce_all = yes` (oa_wealth_changes.txt:172).

### What is DEAD vs DORMANT (corrected after adversarial review)
- `DEMAND_from_industry_<good>` — genuinely DEAD: set NOWHERE (grep-confirmed); the `has_variable = DEMAND_from_industry_*` branches never fire.
- `INDUSTRY_factories_assigned_<good>` — **NOT dead** (review correction): seeded to 0 for all goods, but INCREMENTED positive at world setup (`INDUSTRY_assign_factory { add=$amount$ }` in se_INDUSTRY_factory_assignment.txt, called from oa_economy_setup.txt:254-352 — clothing +3, early_munitions +4, alcohol +1, …) AND by the player add-factory GUI buttons. So the `has_variable = INDUSTRY_factories_assigned_pharmaceuticals` branch is TRUE everywhere; it is DORMANT (adds ~0 with no pharma factories + the mechanised production term being unfed), not structurally dead. What is actually stubbed is the PRODUCE DRIVER (debug_demand.3 / undefined MANUFACTURE_*) — that is #69's problem, and #69's task text must be corrected (it wrongly says nothing increments factories_assigned).
- **The only live pharma-input demand-back is the direct `DEMAND_<input> add var:COTTAGEIND_produced_pharmaceuticals` shape.** It is NOT wired for pharma's own inputs today (vegetables/whales have only the dormant factory branch), so the chili wiring INTRODUCES this pattern for pharma by copying the proven CLOTHING template (wool/dye/textile_fibres add var:COTTAGEIND_produced_clothing), not by mirroring the dormant whales branch.

### Verdict
- **CHILI → pharmaceuticals** is buildable on the LIVE path: chili as materia medica (辣椒, an 18thC Chinese pharmacopeia/condiment good). Buildable now.
- **PEANUT** splits by processing state (user directive):
  - **RAW peanut** = food/subsistence → **#62** (food-basket). Not a manufacturing hookup.
  - **PROCESSED peanut** = peanut oil 花生油 = the **processed_foods** good, which is deliberately factory-only → **#69** (factory var-sim revival). NOT cottage.
  - => #68 builds **nothing** for peanut; it is handed to #62 (raw) + #69 (oil). Stated plainly, not faked onto the factory-only stub.

## DESIGN (chili → cottage pharmaceuticals) — CORRECTED after adversarial review: ONE edit, demand-back only

The review established that chili DEMAND comes ENTIRELY from the demand-back term; adding chili as an in-recipe input (a raw cache + a produced-total add) would ALSO inflate pharmaceutical OUTPUT (the produced var is literally the sum of its input terms — construction_materials/clothing precedent) for no demand benefit. The wool precedent proves it: wool is demanded via `produced_clothing` WITHOUT wool being in the produce_clothing recipe. So the minimal, side-effect-free build is the demand-back term ALONE.

**ONE edit** — `common/script_values/DEMAND_luxury_svalues.txt`, `DEMAND_chili` (:532-576, NOT DEMAND_svalues.txt — chili is a LUXURY good defined there):
- chili's shape is `value = var:DEMAND_luxury_chili` (else `DEMAND_luxury_base_total`), a wealth/price-elasticity `multiply` block, then `multiply = DEMAND_elasticity_impact`, `min = 0`. It has NO `value = 0` baseline, so the wool `add`-onto-zero shape cannot be copied verbatim.
- Add the medicinal-demand term as an `add` on the good's own total, placed so it is NOT swallowed by the wealth/price-elasticity multiply (that multiply models discretionary luxury elasticity; medicinal/industrial demand for chili should be additive to it, not scaled by pop wealth). Concretely: add `if = { limit = { has_variable = COTTAGEIND_produced_pharmaceuticals } add = { value = var:COTTAGEIND_produced_pharmaceuticals  multiply = <modest coeff> } }` AFTER the elasticity multiply block and BEFORE `min = 0` (so it sits alongside `multiply = DEMAND_elasticity_impact` as a floor-additive medicinal term, mirroring how DEMAND_wool adds produced_clothing as a flat term — adapted to the luxury structure). Verify placement on the boot log.
- This makes producing cottage pharmaceuticals demand chili (materia medica) WITHOUT changing pharma output.

- **GLOBAL blast radius (corrected rationale):** chili demand tracks cottage-pharma OUTPUT (driven by raw_vegetables+raw_whales — near-universal), gated only on `has_variable = COTTAGEIND_produced_pharmaceuticals` (true wherever cottage pharma runs), so it arises GLOBALLY wherever cottage pharma runs — NOT only where chili is grown (the review corrected my wrong "only where grown" claim). This matches the existing global cottage demand-back behavior (wool is demanded everywhere clothing is made). Since chili is New-World-seeded (#64) into a NARROW supply, global pharma-demand pulls on that narrow supply → moves chili price/trade in producing regions (#50/#52 layer). The real safety lever is the COEFFICIENT (keep it modest), not geography. Verify no destabilization on the boot.
- **#62/#279 reconcile (corrected):** chili's "food role" is SUPPLY-side — GOODS_governorship_chili_produced is summed into DEMAND_fulfilled_food_need (DEMAND_food_svalues.txt:102, ÷2), i.e. production feeding fulfilled-need, NOT a food DEMAND on chili. Chili's only DEMAND today is the luxury sink DEMAND_chili; adding an industrial/medicinal term there is ADDITIVE, not a double-count. Still confirm #62 didn't already add an independent chili food-demand elsewhere before layering this third role.
- **-debug_mode logging:** emit chili's medicinal-demand contribution per quarter (staged-var band, static label) so the boot confirms it flows.

## ASSUMPTIONS / GUESSES (→ overnight ASSUMPTIONS section)
- chili's medicinal-demand coefficient (the `multiply` on the COTTAGEIND_produced_pharmaceuticals add) — best-guess modest (chili is a minor medicinal input, not a bulk one); start small, tune on the tzprobe chili demand band. Placement relative to the elasticity multiply is itself a call to verify on the boot.
- Peanut is ROUTED to #62 (raw food) + #69 (peanut oil = factory processed_foods) — NOT built here. Stated loudly, not a hidden cut: #68's deliverable is chili only. NOTE (review): pre-industrial peanut-oil pressing (榨油) WAS historically a cottage/workshop activity, so "processed_foods is factory-only" is an ENGINE constraint (the deliberate cottage stub), not a historical truth — logged so #69 knows the history if it ever adds a cottage processed_foods path.

## VERIFY
- tzprobe: chili demand band RISES where cottage pharmaceuticals are produced; scales with the coefficient. No double-count against chili's supply-side food role. Pharma OUTPUT unchanged (the one-edit design doesn't touch it). No global economy destabilization (#50/#52 caution).
