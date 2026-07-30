# MG-3 Design — Distinct province/country modifiers per trade good

**Bug (user boot-test):** ALL trade goods give the SAME "Local Monthly Amenities" modifier.
**Root cause:** Every one of the 56 goods in `common/trade_goods/00_imp19c.txt` carries the
identical `province = { local_monthly_food = 0.07 }` and NO `country` block. So owning any
good confers the same tiny food bonus and nothing else — goods are mechanically
indistinguishable.

**Fix shape (proven upstream — TI `00_default.txt`, Invictus `00_default.txt`):** give each
good a DISTINCT pair — a `province = { <one local modifier> }` **and** a
`country = { <one-or-two global effects> }` — thematically matched to the good. Preserve every
existing `category`, `gold`, `color`, and `allow_unit_type` line unchanged.

## Vocabulary verified present in imp19c (do NOT invent tokens)
- svalues (`00_event_values.txt:1577-1589`): `happiness_small_svalue`=0.04, `happiness_large_svalue`=0.08,
  `output_small_svalue`=0.03, `output_large_svalue`=0.06 (+ negatives).
- Province modifiers (`00_from_events_province.txt`): `local_monthly_food`, `local_output_modifier`,
  `local_tax_modifier`, `local_manpower_modifier`, `local_monthly_civilization`,
  `local_<strata>_happyness`, `local_<strata>_output`. All 10 pop-types
  (upper_strata/middle_strata/lower_strata/proletariat/indentured + vanilla citizen/freemen/nobles/
  slaves/tribesmen) auto-generate local_ & global_ output+happyness tokens.
- Country modifiers (`00_from_events_country.txt` + military grep): `global_monthly_food_modifier`,
  `global_population_growth`, `global_population_capacity_modifier`, `global_pop_promotion_speed_modifier`,
  `global_commerce_modifier`, `global_export_commerce_modifier`, `global_monthly_civilization`,
  `research_points_modifier`, `monthly_legitimacy`, `ruler_popularity_gain`, `omen_power`,
  `build_cost`, `build_time`, `ship_cost`, `navy_maintenance_cost`, `army_maintenance_cost`,
  `global_supply_limit_modifier`, `global_manpower_modifier`, `heavy_infantry_discipline`,
  `heavy_cavalry_discipline`, `light_cavalry_discipline`, `light_cavalry_movement_speed`,
  `warelephant_discipline`, `regular_infantry_offensive`, `regular_infantry_discipline`,
  `artillery_offensive`, `heavy_infantry_defensive`, `global_<strata>_output`, `global_<strata>_happyness`,
  `global_population_happiness`, `diplomatic_reputation`.

## Scale discipline (IMPORTANT)
imp19c's food scale is tiny (existing file uses 0.07 everywhere) — TI's `local_monthly_food = 3..6`
is a DIFFERENT scale and must NOT be copied. Food goods keep `local_monthly_food` in the
**0.04–0.07** band. Province happiness/output use the named svalues (0.03–0.04). Country military
bonuses ~0.05–0.10, cost reductions ~ -0.03 to -0.05, matching TI/existing econ modifiers.

## Decision: drop the food byproduct from NON-food goods
TI/Invictus non-food goods carry ZERO food. The old universal `local_monthly_food = 0.07` on
worked/mineral goods is exactly the "same modifier everywhere" bug. Non-food goods therefore lose
the food line and gain their own thematic province modifier. Food/agricultural goods keep food as
their (now good-appropriate) province modifier. **Risk noted for review:** ~28 provinces were
re-mapped to porcelain/rifles/New-World crops via province_setup.csv; those producing a *non-food*
good (porcelain, rifles) lose 0.07 local food. This is negligible vs pop/building food and is
TI-consistent, but flagged for the adversarial reviewer.

## Per-good assignment (56 goods)

### Food (agricultural — keep food as province modifier)
| good | province | country |
|---|---|---|
| grain | local_monthly_food = 0.07 | global_monthly_food_modifier = 0.05 |
| fish | local_monthly_food = 0.05 | global_lower_strata_happyness = happiness_small_svalue |
| livestock | local_monthly_food = 0.05 | global_manpower_modifier = 0.02 |
| vegetables | local_monthly_food = 0.05 | global_population_growth = 0.03 |
| generic_fruit | local_monthly_food = 0.04 | global_population_happiness = 0.02 |
| tropical_fruit | local_monthly_food = 0.04 | global_lower_strata_happyness = happiness_small_svalue |
| mediterranean_fruit | local_monthly_food = 0.04 | global_middle_strata_happyness = happiness_small_svalue |
| temperate_fruit | local_monthly_food = 0.04 | global_population_happiness = 0.02 |
| sugar | local_monthly_food = 0.04 | global_population_happiness = 0.02 |
| salt | local_lower_strata_happyness = happiness_small_svalue | army_maintenance_cost = -0.05 |
| spices | local_middle_strata_happyness = happiness_small_svalue | global_commerce_modifier = 0.05 |
| chocolate | local_upper_strata_happyness = happiness_small_svalue | global_upper_strata_happyness = happiness_small_svalue |

### Cash crops (category 2)
| good | province | country |
|---|---|---|
| tea | local_middle_strata_happyness = happiness_small_svalue | global_monthly_civilization = 0.01 |
| coffee | local_middle_strata_happyness = happiness_small_svalue | research_points_modifier = 0.05 |
| opium | local_tax_modifier = 0.03 | global_commerce_modifier = 0.05 |
| tobacco | local_lower_strata_happyness = happiness_small_svalue | global_population_happiness = 0.02 |
| maize | local_monthly_food = 0.05 | global_population_growth = 0.03 |
| sweet_potato | local_monthly_food = 0.05 | global_population_capacity_modifier = 0.03 |
| potato | local_monthly_food = 0.05 | global_population_growth = 0.03 |
| peanut | local_monthly_food = 0.04 | global_lower_strata_output = output_small_svalue |
| chili | local_lower_strata_happyness = happiness_small_svalue | global_population_happiness = 0.01 |
| hardwood | local_output_modifier = 0.02 | ship_cost = -0.05 |
| rubber | local_output_modifier = 0.02 | global_commerce_modifier = 0.05 |
| dye | local_upper_strata_happyness = happiness_small_svalue | global_export_commerce_modifier = 0.05 |

### Raw textile fibres (category 3)
| good | province | country |
|---|---|---|
| fur | local_output_modifier = 0.01 | global_commerce_modifier = 0.05 |
| linen | local_lower_strata_happyness = happiness_small_svalue | global_commerce_modifier = 0.03 |
| hemp | local_output_modifier = 0.01 | navy_maintenance_cost = -0.05 |
| cotton | local_proletariat_output = output_small_svalue | global_export_commerce_modifier = 0.05 |
| textile_fibres | local_proletariat_output = output_small_svalue | global_middle_strata_output = output_small_svalue |
| industrial_fibres | local_output_modifier = 0.02 | build_cost = -0.03 |
| wool | local_lower_strata_happyness = happiness_small_svalue | global_commerce_modifier = 0.03 |

### Special animals (category 0 — keep allow_unit_type)
| good | province | country |
|---|---|---|
| horses | local_output_modifier = 0.01 | army_movement_speed = 0.05 |
| elephants | local_output_modifier = 0.03 | warelephant_discipline = 0.1 |
| camel | local_output_modifier = 0.01 | global_supply_limit_modifier = 0.05 |

### Industrial raw / minerals
| good | province | country |
|---|---|---|
| wood | local_manpower_modifier = 0.02 | regular_infantry_defensive = 0.05 |
| stone | local_lower_strata_happyness = happiness_small_svalue | build_cost = -0.05 |
| inorganic_compounds | local_output_modifier = 0.02 | build_cost = -0.03 |
| sulphur | local_output_modifier = 0.02 | artillery_offensive = 0.1 |
| whales | local_upper_strata_happyness = happiness_small_svalue | global_commerce_modifier = 0.03 |
| peat | local_output_modifier = 0.01 | build_time = -0.03 |
| coal | local_proletariat_output = output_small_svalue | global_middle_strata_output = output_small_svalue |
| oil | local_output_modifier = 0.02 | global_commerce_modifier = 0.05 |

### Precious / luxury minerals
| good | province | country |
|---|---|---|
| amber | local_upper_strata_happyness = happiness_small_svalue | ruler_popularity_gain = 0.05 |
| gems | local_upper_strata_happyness = happiness_small_svalue | global_upper_strata_happyness = happiness_small_svalue |
| incense | local_upper_strata_happyness = happiness_small_svalue | omen_power = 0.1 |
| palm | local_monthly_food = 0.04 | global_lower_strata_happyness = happiness_small_svalue |

### Metals (category 3 — keep allow_unit_type where present)
| good | province | country |
|---|---|---|
| tin | local_tax_modifier = 0.02 | global_manpower_modifier = 0.02 |
| copper | local_tax_modifier = 0.02 | navy_maintenance_cost = -0.05 |
| iron | local_tax_modifier = 0.02 | regular_infantry_discipline = 0.05 |
| gold | local_tax_modifier = 0.03 | monthly_legitimacy = 0.02 |
| silver | local_tax_modifier = 0.03 | global_commerce_modifier = 0.05 |
| lead | local_output_modifier = 0.02 | regular_infantry_offensive = 0.1 |

### Worked luxury / manufactured raw-style (category 4)
| good | province | country |
|---|---|---|
| cloth | local_middle_strata_happyness = happiness_small_svalue | global_commerce_modifier = 0.03 |
| silk | local_upper_strata_happyness = happiness_small_svalue | global_export_commerce_modifier = 0.05 |
| porcelain | local_upper_strata_happyness = happiness_small_svalue | global_export_commerce_modifier = 0.05 |
| rifles | local_tax_modifier = 0.02 | regular_infantry_offensive = 0.1 |

**Total: 56 goods, each a unique (province, country) pair** (a few country effects repeat across
thematically-similar goods — e.g. global_commerce_modifier on trade commodities — but no two goods
share the SAME province+country pair, and every good now has BOTH blocks, which is the fix).

## Out of scope
- The 24 manufactured goods (electronics/steel/chemicals/…) are NOT in this file (they are the
  variable-overlay MG goods) — untouched.
- Icons, loc (MG-1/MG-2 done separately), gold/category/color values — unchanged.

## Design-review resolutions (agent ad5dc10127c852f5c — MG-3 verdict: SOUND)
- **Flag 1 (MEDIUM) — inert stub-unit modifiers: FIXED.** The review found that
  `heavy_cavalry_discipline`, `light_cavalry_movement_speed`, and `heavy_infantry_defensive` target
  unit types whose `common/units/` files are 3-byte BOM-only STUBS (no unit defined) — engine-valid
  tokens but zero units to act on, so the bonus is cosmetic-only over an empty set. Confirmed: the
  only real land units are `regular_infantry`, `conscripts`, `artillery`, `warelephant`, `riflemen`,
  `qing_yongying`/`bayara`/`eight_banners`/`green_standard`/`ever_victorious`, `engineer_cohort`,
  `supply_train`. Retargeted to FUNCTIONAL, country-legal tokens:
  - horses `heavy_cavalry_discipline` → `army_movement_speed = 0.05` (proven country-scope,
    `qing_selfstrengthening_modifiers.txt:170,251`; cavalry-flavour = mobility).
  - camel `light_cavalry_movement_speed` → `global_supply_limit_modifier = 0.05`
    (`00_from_events_country.txt`; camels = desert logistics).
  - wood `heavy_infantry_defensive` → `regular_infantry_defensive = 0.05` (`qing_mechanics_modifiers.txt:631`).
  - iron `heavy_infantry_discipline + regular_infantry_discipline` → single
    `regular_infantry_discipline = 0.05` (dropped the inert heavy-inf half).
  `warelephant_discipline` (elephants), `artillery_offensive` (sulphur), `regular_infantry_offensive`
  (lead/rifles) were confirmed FUNCTIONAL and are kept.
- **Flag 2 (LOW–MEDIUM) — food-drop overrides an in-file comment: ACKNOWLEDGED, proceeding.** The
  drop of `local_monthly_food` from porcelain/rifles knowingly overrides the author note at
  `00_imp19c.txt:494-499`. The review confirmed 0.07 flat food is immaterial and found NO structural
  dependency (only a yield contribution, no crash). The implementer will replace that comment with a
  note explaining the deliberate override (goods now carry their own thematic modifier), not silently
  contradict it.
- **Flag 3 (LOW) — scale conservatism: endorsed by the review.** No change.

## Review gates
1. Adversarial DESIGN review (this doc) — token validity, scale, food-drop risk, thematic sanity.
2. Implement (pure edit of province/country blocks in 00_imp19c.txt).
3. Adversarial POST-IMPL review (diff) — brace balance, no token typo, no lost allow_unit_type,
   BOM/line-endings preserved.
