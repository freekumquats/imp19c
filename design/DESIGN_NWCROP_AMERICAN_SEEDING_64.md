# DESIGN — Seed New World crops into their real 1763 American ranges (#64)

**Status:** implementation design, 2026-08-10, **REVISED post-review (rev-64 corrections folded into the body; round-2 review pending).** Grounded in research/RESEARCH_NWCROP_GEOGRAPHY_64.md. Design-note-first → adversarial review → implement → verify boot. Do NOT implement until a CLEAN review passes. freekumquats / merge-overnight.

**Round-1 review (rev-64) verdict: PROCEED-WITH-CORRECTIONS.** Corrections integrated into the body below (the source-of-truth blocker is resolved, counts re-baselined from the engine .txt, numeric floors committed). Round-1 findings preserved verbatim at the bottom as an audit trail.

## The defect (user, verified — counts re-baselined from the ENGINE source setup/provinces/*.txt)
The 5 New World crops are seeded almost entirely in CHINA — their 18th-c. diffusion frontier — and barely in the AMERICAS, their actual origin. This is backwards from the real 1763 distribution (memory: 1763 seeding corrections; DESIGN_NWCROP_DEMAND_RECLASSIFY_62 H3 re-opened). **The engine reads `setup/provinces/*.txt`, NOT `common/province_setup.csv`** (the CSV is generator input only, diverges from the .txt, and must not be used as the baseline — see §Source of truth). True current state from the .txt:
- maize: 6 provinces, ALL China (Hunan/Jiangxi) — ZERO Americas.
- peanut: **3**, ALL China (Guangdong) — ZERO Americas.
- chili: **3**, ALL China (Hunan) — ZERO Americas.
- sweet_potato: 6 (4 China Fujian/Guangdong + 2 Costa de Peru) — roughly right.
- potato: 5, ALL Americas but WRONG sub-region (New Mexico ×2, Peru ×3).

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

**Numeric per-crop American FLOORS (committed — supply is abundant, so under-seeding is the real risk):** maize ≥12–15 American (vs 6 China → China becomes the minority); peanut ≥6 American (vs 3 China); chili ≥6 American (vs 3 China); sweet_potato +3–4 minor American; potato: move the 2 New Mexico → Andes, net Andean ≥4. Impl tunes WITHIN these floors and builds + logs the concrete province-ID list (no-silent-cap rule governs HOW it's logged; the floors govern HOW MANY). China maize/peanut/chili become a minority of each crop's provinces; the Americas hold the majority.

## Source of truth — RESOLVED: edit `setup/provinces/*.txt`, NOT the CSV
`common/province_setup.csv` is **NOT read by the engine** — it is only input to the modding scripts (buildings_generator.py / old_to_new_setup_*.py), and it DIVERGES from the live .txt (e.g. Wuyishan 3317 = `tea` in `00_Fujian.txt:131` but `peanut` in the CSV). Recorded decision: `overnight/OVERNIGHT_DECISIONS2.md:207-218` ("CRITICAL SOURCE DECISION, 2026-07-08"); confirmed by rg (no engine loader for province_setup). **Directive: edit `setup/provinces/00_<Region>.txt` only** (optionally sync the CSV for generator hygiene, never as the live edit). There is NO #281 rifles trap here — that trap only bites if you edit the CSV.
- Concrete live-good locations (verified): New Mexico 548/856 = `00_American_Southwest.txt:45,91` (potato, to reassign); Peru potato = `00_Peru.txt` (Moquegua 1587, Azángaro 2080) + `00_Lower_Peru.txt` (Uyuni 2128); Mexico targets = `00_Eastern_Mexico.txt`/`00_Pacific_Mexico.txt`/`00_Northern_Mexico.txt`/`00_Central_America.txt`; also `00_Antilles.txt`, `00_Appalachia.txt`, `00_Argentina.txt`, the 5 Brazil files; current maize seed = `00_Hunan.txt:27`.
- **Each conversion SUBTRACTS a grain/livestock producer as well as adding a NW-crop one — accepted** (rev-64 C-M1): grain→maize is food-basket-neutral (no famine risk), and the convert-only-generic rule (R2) keeps differentiated goods intact; the grain/livestock loss to building-eligibility/pop-composition is low-consequence and deliberate.
- **BOM/EOL (rev64b-round2 MED — the directive was INVERTED; corrected):** the `setup/provinces/*.txt` history files DO carry a UTF-8 BOM (verified `ef bb bf` on 00_Hunan/00_Peru/00_American_Southwest/00_Eastern_Mexico) and boot fine — the "setup-reader-rejects-bom" memory applies to a DIFFERENT setup reader (country/main setup), NOT these province-history files. Directive: **PRESERVE the existing BOM AND EOL — do not add, strip, or convert either.** A BOM-stripping edit path would churn every edited file (the file-editing-path rule's exact hazard).

## Downstream coupling to check (must-hold, verify at impl + boot)
- **#279 dynamic food basket**: `DEMAND_num_food_goods` = 6 + 1 per NW crop actually PRODUCED (se_DEMAND.txt). Adding American maize/peanut producers CHANGES how many food goods exist per governorship → the famine-metric divisor (memory #62 M2 dilution). Verify the count logic stays consistent across the new producer set.
- **se_QING_COLON.txt capacity lift / se_QING_POPULATION.txt pop-pressure** (#66 axis 4): `QING_COLON_apply_nwcrop_capacity` (se_QING_COLON.txt:276-325) is a **GLOBAL every_province sweep BY DESIGN** — it stamps `qing_nwcrop_abundance` (local_population_capacity) on EVERY province growing any of the 5 crops, worldwide, because "the lift is a property of the CROP, not the polity" (header :283-285) and CHI-gating was EXPLICITLY REJECTED as a behaviour change. **CONSEQUENCE for #64: seeding crops in American provinces WILL apply the capacity lift there too — this is INTENDED, not a bug.** The Qing boom "emerges naturally because the crop provinces are overwhelmingly Chinese" (:268-269). After #64, American provinces gain the lift too — a modest global capacity increase in the Americas is historically fine (NW crops did raise carrying capacity in their homelands). VERIFY it doesn't produce a runaway American pop explosion, but do NOT owner-gate the sweep (that contradicts its design). The narrative Qing BOOM events (qing_migration.20/.21/.22) + diffusion (QING_COLON_nwcrop_diffuse) ARE CHI-scoped (ROOT=CHI) — those stay Qing-only regardless of American seeding; only the capacity lift is global.
- **#62 demand fix**: this is #62's prerequisite. After #64, revisit #62's per-crop food-vs-luxury lever on the CORRECTED geography (maize/peanut now have American subsistence producers → their demand path can be decided per-region, not off the all-China artifact).
- **GOODS_national_production / area trade sums**: the caravan oasis-trade + Canton customs read GOODS_national_production_<good> for specific goods (tea/silk/silver/salt/etc.) — NONE of the 5 NW crops are in those lists, so re-seeding them does NOT perturb caravan/Canton revenue. Confirm (grep) no revenue svalue reads maize/potato/etc.

## Files (confirmed post-review)
- `setup/provinces/00_<Region>.txt` (the American area files listed above + `00_Hunan.txt`/`00_Fujian.txt` etc. only if trimming a China entry) — the LIVE source. NOT the CSV. NO trade_goods/00_imp19c.txt. NO demand svalues (that's #62). NO buildings (that's #65).
- Optionally re-sync `common/province_setup.csv` for generator hygiene (never as the live edit).
- Loc: unlikely (trade goods aren't province-named).

## RISK
- **R1 [RESOLVED] — edit setup/provinces/*.txt (the engine source), NOT the CSV.** The wrong-file no-op (#281 trap) only occurs if you edit the CSV. Boot-verify the good actually changed regardless.
- **R2 [MED] — don't destroy differentiated goods.** Convert only generic grain/livestock/fur provinces; leave sugar/silver/copper/coal/cloth (the differentiated American goods) intact.
- **R3 [MED] — famine-metric divisor** (#279 / #62 M2): more producing NW-crop goods dilutes the famine metric in producing regions. Acceptable but must be flagged + verified, not silently shipped.
- **R4 [MED, CORRECTED] — the capacity lift is GLOBAL by design; American producers WILL gain it (intended).** Do NOT owner-gate `QING_COLON_apply_nwcrop_capacity` (that contradicts its explicit design, se_QING_COLON.txt:283-285). Instead VERIFY the resulting American capacity increase doesn't cause a runaway foreign pop explosion on boot. The narrative boom events + diffuse loop are already ROOT=CHI (Qing-only) — unaffected.

## Verify (boot)
- Grep the boot's live province goods (or in-game map): maize/peanut/chili now grow across the Americas (majority share) with a China minority; potato is on Potosí/Atacama highlands NOT New Mexico; sweet_potato unchanged in China + minor Americas additions.
- Each edited province's good ACTUALLY changed (not a wrong-file no-op) — R1.
- No differentiated American good was destroyed (R2). Famine metric sane (R3). Global capacity lift now applies to American producers (intended) without a runaway foreign pop explosion; narrative boom + diffuse loop still ROOT=CHI (R4). Caravan/Canton revenue unchanged (no NW crop in those sums).
- #62 can now proceed on corrected geography.

## Traps / rules
- Source-of-truth = setup/provinces/*.txt (see §CORRECTIONS C1 — resolved, NOT open). PRESERVE the existing UTF-8 BOM + EOL on these history files (they HAVE a BOM and boot fine — do not add/strip/convert; the "setup-reader-rejects-bom" memory is a DIFFERENT reader). No churn.
- Concrete province-ID list built + logged (no silent sampling); numeric per-crop American floors (C-H1).
- This is content seeding, NOT plumbing — no #219 flood risk (not editing good defs or country/province modifier blocks).
- Design-note-first → adversarial review → implement → verify boot.

---

## ADVERSARIAL DESIGN-REVIEW CORRECTIONS (rev-64, 2026-08-10) — PROCEED-WITH-CORRECTIONS
Verdict: seeding plan + the two hardest calls (R4 global-capacity, #62 ordering) are SOUND. Two corrections are mandatory before impl; they supersede the conflicting text above.

**C1 [CRITICAL] — the source-of-truth blocker is ALREADY RESOLVED; edit `setup/provinces/*.txt`, NOT the CSV.** `common/province_setup.csv` is NOT read by the engine — it is only input to the modding scripts (buildings_generator.py / old_to_new_setup_*.py). Recorded decision: `overnight/OVERNIGHT_DECISIONS2.md:207-218` ("CRITICAL SOURCE DECISION, 2026-07-08"); confirmed by rg (no engine loader for province_setup, only doc/script refs). => the "LOAD-BEARING MECHANICS QUESTION" section + R1's "grep both / verify per province" language is STRUCK. Flat directive to impl: **edit `setup/provinces/00_<Region>.txt` only** (sync the CSV optionally for generator hygiene, never as the live edit). There is NO #281 rifles trap here — that trap only bites if you edit the CSV. Concrete live-good locations (verified): New Mexico 548/856 = `00_American_Southwest.txt:45,91` (potato); Peru potato = `00_Peru.txt` (Moquegua 1587, Azángaro 2080) + `00_Lower_Peru.txt` (Uyuni 2128); Mexico targets = `00_Eastern_Mexico.txt`/`00_Pacific_Mexico.txt`/`00_Northern_Mexico.txt`/`00_Central_America.txt`; also `00_Antilles.txt`, `00_Appalachia.txt`, `00_Argentina.txt`, the 5 Brazil files; current maize seed = `00_Hunan.txt:27`.

**C2 [CRITICAL] — the current-state counts above (and in the research doc) are STALE (from the CSV) and materially wrong.** The CSV diverges from the authoritative .txt (e.g. Wuyishan 3317 = `tea` in `00_Fujian.txt:131` but `peanut` in the CSV). Re-baselined from the engine .txt:
| crop | (stale CSV) | ACTUAL engine .txt | Americas |
|---|---|---|---|
| maize | 6 | 6 (Hunan/Jiangxi) | 0 |
| peanut | 5 | **3** (all Guangdong) | 0 |
| chili | 6 | **3** (all Hunan) | 0 |
| sweet_potato | 6 | 6 (4 Fujian/Guangdong + 2 Peru) | 2 |
| potato | 5 | 5 (New Mexico ×2 + Peru ×3) | 5 |
The qualitative defect (maize/peanut/chili = ZERO Americas) HOLDS — the task is real — but peanut/chili China baselines are already HALF what this design assumed, so any "China → minority" math off the CSV is wrong. => impl re-baselines current-state + all share targets from `setup/provinces/*.txt`.

**C-H1 [HIGH] — commit to numeric per-crop American FLOORS (don't leave "chosen at impl" vague).** Supply is abundant (under-seeding is the real risk, not the pool). Floors so majority-American is guaranteed: **maize ≥12–15 American** (vs 6 China); **peanut ≥6 American**; **chili ≥6 American**; **sweet_potato +3–4 minor American**; **potato: move the 2 New Mexico → Andes, net Andean ≥4**. Impl tunes within these; the no-silent-cap rule governs HOW the list is logged, these floors govern HOW MANY.

**C-M1 [MED] — state that each conversion SUBTRACTS a grain/livestock producer, accepted.** grain→maize is food-basket-neutral (no famine risk), but grain/livestock also feed building eligibility + pop composition; the convert-only-generic rule (R2) mitigates. Low consequence — say explicitly the removal is accepted.

**CONFIRMED SOUND (keep as written):** R4 global-capacity (if anything the runaway worry is OVER-stated — American provinces gain only the capacity CEILING, not the ROOT=CHI growth PUSH; verify-on-boot is cheap insurance, do NOT owner-gate); #62 ordering (#64 first, then #62 re-derives on corrected geography — no broken intermediate, no #62 edit needed first); L2 revenue coupling NONE; L4 content-only, no #219 risk; L3 setup files BOM-free.
