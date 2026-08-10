# DESIGN — Seed New World crops into their real 1763 American ranges (#64)

**Status:** implementation design, 2026-08-10. Grounded in research/RESEARCH_NWCROP_GEOGRAPHY_64.md (crop-geo agent, region keys verified vs common/province_setup.csv). Design-note-first → adversarial review → implement → verify boot. Do NOT implement until reviewed. freekumquats / merge-overnight.

## The defect (user, verified)
The 5 New World crops are seeded almost entirely in CHINA — their 18th-c. diffusion frontier — and barely in the AMERICAS, their actual origin. This is backwards from the real 1763 distribution (memory: 1763 seeding corrections; DESIGN_NWCROP_DEMAND_RECLASSIFY_62 H3 re-opened). Verified current state (grep province_setup.csv col4=TRADEGOOD):
- maize: 6 provinces, ALL China (Hunan/Jiangxi) — ZERO Americas.
- peanut: 5, ALL China (Guangdong/Fujian) — ZERO Americas.
- chili: 6, ALL China (Hunan) — ZERO Americas.
- sweet_potato: 6 (4 China + 2 Costa de Peru) — roughly right.
- potato: 5, ALL Americas but WRONG sub-region (New Mexico ×2, Atacama ×2, Potosí ×1).

This is an ECONOMIC-CORRECTNESS task (get the map right), NOT a pop-boom (that's #65). It also unblocks #62 (the per-crop food-vs-luxury demand decision can only be made on correct geography).

## Scope boundary (what #64 is / isn't)
- **IS:** correct WHERE each crop is grown — add American producers, fix potato's sub-region, keep the (correct) China sweet_potato + a defensible China minority for maize/chili/peanut.
- **IS NOT:** #65's boom mechanics (buildings/events/missions), #62's demand-basket edits, any trade_goods/00_imp19c.txt change (#66: that file is a closed door). Pure map-seeding: change which good a province grows.

## THE SEEDING PLAN (per RESEARCH_NWCROP_GEOGRAPHY_64.md)
Convert selected American provinces' TRADEGOOD to the appropriate NW crop. Prefer converting provinces currently growing GENERIC `grain`/`livestock`/`fur` (low-differentiation goods) in the target areas, so we're not destroying a differentiated good (sugar/silver/copper stay). Candidate pool already enumerated (grep of the target American areas):

- **MAIZE** (top priority — the great gap): seed across Mesoamerica + N.America + Andean valleys + Caribbean. Target areas: Eastern Mexico, Pacific Mexico, Central America (core), Northern Mexico, Antilles, Costa/Atacama de Peru (valley provinces), American Southwest, Appalachia, Argentina, Brazil ×5 (minor). Convert grain/livestock provinces there. KEEP Hunan/Jiangxi maize but it becomes a minority share.
- **POTATO** (fix sub-region): the 2 New Mexico potato provinces (548 Hobbs, 856 Cimarron) are geographically wrong (Pueblo agriculture was maize/beans/squash, never potato). **Reassign New Mexico potato → maize or livestock** (livestock already dominates New Mexico: 13 provinces), and **concentrate potato in Potosí + highland Atacama de Peru** (already has 1 Potosí + 2 Atacama — add 1-2 more highland provinces from the grain pool). Leave Old World thin (correct near-zero 1763 China potato).
- **PEANUT**: KEEP modest Guangdong/Fujian. ADD native range: Brazil (esp. Northeast/North), Costa de Peru, Antilles. Convert grain provinces. NOT export-tagged (the W.African groundnut export boom is 19th-c. — do NOT model it here).
- **CHILI**: ADD real American range: Eastern/Pacific Mexico, Central America (core), Costa/Atacama de Peru, Antilles, Brazil. KEEP Hunan modest (do NOT expand). A garden/kitchen crop, not a plantation export (validates #62's keep-chili-luxury-only).
- **SWEET_POTATO**: KEEP Fujian/Guangdong + 2 Costa de Peru (correct). ADD minor: Antilles, Central America/Eastern Mexico lowlands, Brazil. Minor rounding-out only.

Exact province IDs to convert are chosen at impl from the target-area grain/livestock pool (a concrete list, built + logged, not silently sampled — no-silent-cap rule). Target rough share: China maize/peanut/chili drop to a MINORITY of each crop's provinces; the Americas hold the majority.

## THE LOAD-BEARING MECHANICS QUESTION (BLOCKER — resolve before impl)
**Where is the source of truth for a province's trade good?** Two candidates, and they must not be edited in the wrong place:
- `common/province_setup.csv` (col4 = TRADEGOOD) — where ALL the current crop seeding lives (verified: maize/potato/etc. rows are here). The American target provinces (New Mexico, Peru areas) appear in the CSV.
- `setup/provinces/*.txt` (`trade_goods="..."` per province) — used by MANY provinces (Tannu Tuva, Angola, Sichuan-Kham, …). **Standing memory (imp19c-rifles-logistics-blocker): "edit setup/provinces/*.txt not csv"** — the CSV was found NOT to be the live source for at least some provinces.
- **MUST VERIFY at impl:** for each American target province, which file the engine actually reads (does a setup/provinces/*.txt entry exist and OVERRIDE the CSV? are the American provinces CSV-only?). Editing the CSV for a province whose good is set in setup/*.txt = a no-op (the #281 rifles trap). The impl must (a) locate each target province's real trade-good definition, (b) edit THAT, (c) confirm on boot the good actually changed. Grep both sources per province before editing.
- **BOM/EOL:** the setup/ reader REJECTS BOM (memory: setup-reader-rejects-bom) — CSV + setup/provinces/*.txt must stay BOM-free. Do NOT add a BOM. Preserve existing EOL.

## Downstream coupling to check (must-hold, verify at impl + boot)
- **#279 dynamic food basket**: `DEMAND_num_food_goods` = 6 + 1 per NW crop actually PRODUCED (se_DEMAND.txt). Adding American maize/peanut producers CHANGES how many food goods exist per governorship → the famine-metric divisor (memory #62 M2 dilution). Verify the count logic stays consistent across the new producer set.
- **se_QING_COLON.txt capacity lift / se_QING_POPULATION.txt pop-pressure** (#66 axis 4): `QING_COLON_apply_nwcrop_capacity` (se_QING_COLON.txt:276-325) is a **GLOBAL every_province sweep BY DESIGN** — it stamps `qing_nwcrop_abundance` (local_population_capacity) on EVERY province growing any of the 5 crops, worldwide, because "the lift is a property of the CROP, not the polity" (header :283-285) and CHI-gating was EXPLICITLY REJECTED as a behaviour change. **CONSEQUENCE for #64: seeding crops in American provinces WILL apply the capacity lift there too — this is INTENDED, not a bug.** The Qing boom "emerges naturally because the crop provinces are overwhelmingly Chinese" (:268-269). After #64, American provinces gain the lift too — a modest global capacity increase in the Americas is historically fine (NW crops did raise carrying capacity in their homelands). VERIFY it doesn't produce a runaway American pop explosion, but do NOT owner-gate the sweep (that contradicts its design). The narrative Qing BOOM events (qing_migration.20/.21/.22) + diffusion (QING_COLON_nwcrop_diffuse) ARE CHI-scoped (ROOT=CHI) — those stay Qing-only regardless of American seeding; only the capacity lift is global.
- **#62 demand fix**: this is #62's prerequisite. After #64, revisit #62's per-crop food-vs-luxury lever on the CORRECTED geography (maize/peanut now have American subsistence producers → their demand path can be decided per-region, not off the all-China artifact).
- **GOODS_national_production / area trade sums**: the caravan oasis-trade + Canton customs read GOODS_national_production_<good> for specific goods (tea/silk/silver/salt/etc.) — NONE of the 5 NW crops are in those lists, so re-seeding them does NOT perturb caravan/Canton revenue. Confirm (grep) no revenue svalue reads maize/potato/etc.

## Files (anticipated — confirm source-of-truth first)
- `common/province_setup.csv` AND/OR `setup/provinces/*.txt` (the American area files) — per the blocker above, edit whichever is the live source per province. NO trade_goods/00_imp19c.txt. NO demand svalues (that's #62). NO buildings (that's #65).
- Possibly loc if any province name/flavour references the old good (unlikely — trade goods aren't province-named).

## RISK
- **R1 [HIGH] — wrong-file edit = silent no-op** (the #281 rifles trap). Resolve the source-of-truth blocker per province BEFORE editing; boot-verify the good actually changed.
- **R2 [MED] — don't destroy differentiated goods.** Convert only generic grain/livestock/fur provinces; leave sugar/silver/copper/coal/cloth (the differentiated American goods) intact.
- **R3 [MED] — famine-metric divisor** (#279 / #62 M2): more producing NW-crop goods dilutes the famine metric in producing regions. Acceptable but must be flagged + verified, not silently shipped.
- **R4 [MED, CORRECTED] — the capacity lift is GLOBAL by design; American producers WILL gain it (intended).** Do NOT owner-gate `QING_COLON_apply_nwcrop_capacity` (that contradicts its explicit design, se_QING_COLON.txt:283-285). Instead VERIFY the resulting American capacity increase doesn't cause a runaway foreign pop explosion on boot. The narrative boom events + diffuse loop are already ROOT=CHI (Qing-only) — unaffected.

## Verify (boot)
- Grep the boot's live province goods (or in-game map): maize/peanut/chili now grow across the Americas (majority share) with a China minority; potato is on Potosí/Atacama highlands NOT New Mexico; sweet_potato unchanged in China + minor Americas additions.
- Each edited province's good ACTUALLY changed (not a wrong-file no-op) — R1.
- No differentiated American good was destroyed (R2). Famine metric sane (R3). Global capacity lift now applies to American producers (intended) without a runaway foreign pop explosion; narrative boom + diffuse loop still ROOT=CHI (R4). Caravan/Canton revenue unchanged (no NW crop in those sums).
- #62 can now proceed on corrected geography.

## Traps / rules
- Source-of-truth per province (R1) — the single make-or-break. No BOM in CSV/setup (setup reader rejects BOM). No EOL churn.
- Concrete province-ID list built + logged (no silent sampling).
- This is content seeding, NOT plumbing — no #219 flood risk (not editing good defs or country/province modifier blocks).
- Design-note-first → adversarial review → implement → verify boot.
