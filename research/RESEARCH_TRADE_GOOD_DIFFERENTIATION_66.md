# RESEARCH #66 — How imp19c (upstream = Sobisonator) differentiates trade goods

**Date:** 2026-08-10. Grounded across common/trade_goods, common/script_values/DEMAND_*/INDUSTRY_*/GOODS_*, common/buildings, and a script-wide reference grep. Feeds #65 (make the NW crops earn their keep) + #62 (per-crop demand). "upstream" = Sobisonator's imp19c ONLY (see memory imp19c-oracle-vs-upstream-terminology).

## Bottom line
This mod's differentiation budget is spent on THREE axes only. The trade-good DEFINITION file is a permanently closed door for differentiation (by #219 design). The NW crops are differentiated by a rare FOURTH axis (a demographic/settlement mechanic) that no other good has — but only 3 of the 5 participate.

## Axis 1 — trade_goods/00_imp19c.txt fields: CLOSED (do not use)
57 goods, all identical shape: `category` (0-4), `gold` (flat 0.2; only exceptions saltpetre=0.25, lead=0.4), `province = { local_monthly_food = 0.07 }` (uniform; porcelain/rifles deliberately drop it, 00_imp19c.txt:509-513), `color`. Only 9/57 carry `allow_unit_type` (horses/elephants/camel/wood/tin/iron — military unit-gating, not economic).

This flatness is the second half of a documented revert, NOT an oversight:
- `94df025d3` (MG-3, 2026-07-29) added real per-good province/country modifiers (iron→regular_infantry_discipline, silk→global_export_commerce_modifier, …).
- `afbf558b5` (2026-07-30, "#219 FIX real root cause") REVERTED ALL of it: a good's province{}/country{} blocks ARE the vanilla import-AI's route-desirability input, so any attractive modifier reopens the #219 trade-request flood. Master's flat/"worthless" baseline is intentional so the vanilla AI never asks; the mod runs its own parallel script-trade economy.
- **CONCLUSION: goods will never be differentiated via 00_imp19c.txt. That axis is permanently closed by #219.** (Confirms memory imp19c-oracle-vs-upstream-terminology: re-adding vanilla modifiers "like the oracles" is the trap.)

## Axis 2 — Demand svalues: bucketed, mostly SHARED base, a few genuinely bespoke
- Luxury goods all fall back to `DEMAND_luxury_base_total` (strata wealth × elasticity × currency mult, DEMAND_luxury_svalues.txt:88-100). Each luxury good has a `DEMAND_<good>` wrapper but they're near-identical boilerplate (has_variable cache → else base_total → wealth-elasticity → elasticity_impact). Same shape, different var name = NOT meaningfully bespoke.
- Genuinely bespoke: `DEMAND_gems` (adds luxury_clothing/furniture BOM), `DEMAND_sugar` (adds alcohol+refined_sugar BOM), `DEMAND_rifles` (wholly distinct MILITARY svalue: army size + arsenals + tech_rifles gate, not pop-luxury at all).
- Food: `DEMAND_food_base` is the shared default for the 6-good basket (grain/livestock/vegetables/fish/temperate_fruit/processed_foods) + maize/potato/sweet_potato (DEMAND_food_svalues_new.txt). Basket size is DYNAMIC: `DEMAND_num_food_goods` = 6 + 1 per NW crop actually produced (se_DEMAND.txt:36-112, from #279).
- peanut + chili: luxury-base ONLY, no food-basket hookup (absent from DEMAND_set_demand_from_food_all).

## Axis 3 — Production buildings + BOM recipes: the REAL differentiation (densest axis)
- `trade_goods = <good>` in a building `allow` block gates WHERE it can be built (matches province good) AND drives supply via GOODS_governorship_<good>_produced. Only ~15/57 goods have a DEDICATED production building: silk, porcelain, tea, opium(×2), textile_fibres(×2), salt, coal(×2), iron(×2), cloth, wool, dye, sugar, spices, tobacco, coffee. The rest (grain, fish, livestock, most metals, ALL 5 NW crops) produce via generic base_resources farm/mine buildings.
- ~40 goods are consumed as BOM inputs into manufactured goods (INDUSTRY_demand_importance_<mfg>_<input> in INDUSTRY_svalues.txt): iron→steel; sulphur+wood+saltpetre→gunpowder; textile_fibres+dye→silk_cloth; silk+gold+gems→luxury_clothing/furniture; etc. ~20 mfg recipes each pull 3-9 named inputs. THE densest, most load-bearing axis.

## Reference-count tiers (grep across scripted_effects/script_values/buildings/events/decisions)
| tier | goods |
|---|---|
| heavily wired (currency/granary/canal/salt anchors) | silk, gold, silver, tea, grain, salt |
| well-differentiated (bespoke bldg + BOM + demand) | porcelain, opium, iron, coal, textile_fibres, sugar, dye, wool |
| BOM-only (real recipe input, no dedicated bldg) | copper, tin, lead, stone, wood, sulphur, saltpetre, gems, vegetables, livestock, fish, temperate_fruit, whales, rubber |
| flat/traded-but-undifferentiated | cotton, horses, elephants, camel, oil, spices(despite bldg), coffee, tobacco, hardwood, tropical_fruit, mediterranean_fruit, chocolate, inorganic_compounds, peat, rifles(supply-only) |
| defined-but-dead / DEFUNCT (remapped at boot 584ac791c; see memory imp19c-defunct-trade-goods) | linen, hemp, amber, incense, palm (+ several remapped-away) |

## Axis 4 (NW-crop-specific) — the demographic/settlement mechanic
- **maize, sweet_potato, potato**: food-basket member (DEMAND_food_<crop> + dynamic basket-size coupling #279) + luxury-base fallback + "fulfilled food need" (DEMAND_food_svalues.txt:98-102) + DRIVE the qing_migration/colonization diffusion (se_QING_COLON.txt organic spread) + the involution population-pressure penalty (se_QING_POPULATION.txt:92-100). This is a genuine 4th differentiation axis NO OTHER GOOD has. Real, distinct participation — not flat filler. (No dedicated production building, no BOM consumer role.)
- **peanut, chili**: luxury-base fallback ONLY — no food basket, no building, no BOM. They ride the SAME se_QING_COLON.txt diffusion as the other 3 (the colonization mechanic treats all 5 identically) but carry ZERO economic differentiation beyond generic luxury demand. These two are the closest to dead weight among the 5.

## Verdict feeding #65 / #62
- maize/potato/sweet_potato already earn their keep (food basket + colonization diffusion + population-pressure) — leave as distinct goods.
- peanut + chili sit at the flat-tradeable tier. To make them earn their keep (#65), EITHER (a) give them a bespoke BOM/building hookup — historically plausible: **peanut → oil pressing** (a processed_food / oil input), **chili → a processed_foods / medicinal (pharma) input** (chili was used medicinally) — OR (b) retire them from "distinct good" status if #65's pop-boom design doesn't need them individually. (Retirement path = memory imp19c-defunct-trade-goods precedent.)
- #62's per-crop demand choice should track this: maize/potato/sweet_potato are food-basket goods; peanut/chili are currently luxury-only with no food path.
