# INTERIM FINDINGS — New World crops thread (#62/#64/#65) — PRE-COMPACT CAPTURE

**Status:** 2026-08-10 capture note written just before context compaction. Records the resolved
findings from a long investigation so they survive. TO BE OVERWRITTEN post-compact with proper
per-task design docs. Not itself a design doc — a findings ledger.

## The thread (what was investigated + every conclusion, some hard-won after wrong turns)

Started from #52 (luxury pricing) → surfaced the New World crops (maize/sweet_potato/potato/peanut/chili)
→ chain of investigation. Corrected premises (I was wrong repeatedly; user caught each):
1. NOT a category-field issue — the luxury/food split is driven by hardcoded call-lists in se_DEMAND.txt
   (DEMAND_set_demand_from_food_all + DEMAND_set_demand_from_luxury_all), NOT the trade_goods `category` field.
2. The crops are FORK-ADDED (commit f45c9ce7b/20db2dbd1), category=2 was an incidental tobacco-clone.
3. NOT a starvation bug — American pops eat via generic grain+livestock (food value identical).
4. NOT a missing-boom — the QING_COLON pop-boom is CHI-only, and HISTORICALLY there was NO New World
   population boom in the Americas (post-Columbian collapse; crops were millennia-old staples there, not
   a novel input). The boom is a Qing/Old-World phenomenon (novel crops → marginal-land farming → explosion).
5. Trade-good DEF differentiation: I claimed oracles differentiate via vanilla modifiers → WRONG for this
   mod. UPSTREAM = Sobisonator's imp19c ONLY (oracles = upstream + TI + Invictus; see
   [[imp19c-oracle-vs-upstream-terminology]]). Sobisonator DELIBERATELY STRIPPED vanilla trade-good
   modifiers (they interfere with the script trade system). Verified upstream/master trade_goods: 49 goods,
   almost all flat (category+gold+color+local_monthly_food+province); only allow_unit_type on 7, country on 1.
   So flat NW-crop defs are CORRECT-BY-LINEAGE, not a defect.
6. Perf cost correction: "defined = paying perf cost" is WRONG. Only TRADED (produced+flowing) goods pay
   the per-good/per-TZ/per-quarter loop cost. Dead defs (amber/hemp/incense/camel/palm/generic_fruit +
   the defunct-remap set) cost ~nothing. So no perf case for pruning dead defs; the cost question only
   applies to goods actually in the economy.
7. Where distinctness lives: NOT the def (flat by design) — the SCRIPT layer (demand-basket membership,
   building recipes, production, mod mechanics). A good "earns its keep" by distinct script-layer use.

## THE BUILDING ARCHITECTURE (corrected by user — my two-track model was WRONG)
- WRONG model I asserted: "Qing-only buildings vs everyone-except-Qing generic buildings."
- CORRECT (user + row_production_buildings.txt header): GENERIC buildings are available to EVERYONE
  INCLUDING THE QING. There are Qing-SPECIFIC buildings and generic buildings, both available to Qing.
  Only ~2 buildings are Qing-EXCLUDED (row_manufactory_building + row_plantation_building) — excluded
  ONLY because they are strictly-inferior generic versions of the Qing's own SPECIALITY works (the 5
  named: silk filature/porcelain kiln/tea works/cotton works/salt yard). Qing-SPECIFIC ≠ Qing-SPECIALITY.
- => a New World crop building is GENERIC (Europe ate New World crops too — potato etc.). No Qing exclusion,
  no Qing-specific version needed. Available to all whose provinces grow the crop.

## THE KEY DESIGN INSIGHT (user, the resolution)
The building is GENERIC; the QING-SPECIFICITY lives in the BOOM MECHANIC that READS it.
- Generic crop building = pure economic processing, same for everyone (Europe potato works = economic output).
- QING_COLON pop-boom = a CHI-SCOPED mechanic that keys off the presence/count of those generic crop
  buildings (or crop provinces) and fires the Qing demographic-explosion effects. The boom is the READER;
  the building is the DATA. Same generic object → "processing" everywhere, "demographic frontier" only to
  the Qing reader. No duplication, no Qing-specific building.

## THE THREE RESOLVED TASKS
- **#62** — REMOVE the luxury double-count (maize/potato/sweet_potato demanded as BOTH food + luxury;
  spurious tobacco-clone artifact). Fix in DEMAND_luxury_svalues.txt (rewrite Total svalue food-only, per
  the [#281] rifles precedent — NOT call-list-only, which falls back to DEMAND_luxury_base_total ≠ 0) +
  se_DEMAND.txt call-lists (both …_all + …_all_first_time). peanut needs a food path (no DEMAND_food_peanut
  exists); chili stays luxury-only. Reviewed (design/DESIGN_NWCROP_DEMAND_RECLASSIFY_62.md). UNBLOCKED.
- **#64** — SEED the crops in their real 1763 ranges (Americas: Mesoamerica/maize, Andes/potato,
  S.America+Caribbean/peanut+chili+sweet_potato; EUROPE potato; etc.). Food-neutral relabel of generic grain
  → real staple where the crop dominated; LEAVE grain where temperate wheat dominated. NOT a boom (no American
  boom) — baseline economic correctness so the GENERIC crop building + good-tied economy attach in the crops'
  real regions. PREREQUISITE for #65's generic building having provinces to sit on. Watch: #228(b) was a global
  trade-good pass I ran + stamped "reviewed" that edited the American files and STILL missed maize/potato in
  their homelands → #64 review must be a genuine per-region COMPLETENESS check; #228(b) ROW stamp untrustworthy.
- **#65** — GENERIC New World crop processing building(s) [available to all] + wire the CHI QING_COLON
  pop-boom to READ them for Qing-specific effects + flesh out the boom with CHI events/missions (land pressure,
  frontier migration, the demographic story). Build ON QING_COLON diffusion (#384) + #78 applicator. CHI-boom
  half is Qing-only; the building is generic. Needs #64 (crops in the ground).

DEPENDENCIES: #64 (crops seeded) → prereq for #65 (generic building attaches). #62 independent. #65 boom-half CHI-only.
