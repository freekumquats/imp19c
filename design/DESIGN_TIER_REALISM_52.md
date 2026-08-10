# DESIGN — cross-good tier realism (#52): luxuries should price above staples

**Status:** implementation design, 2026-08-10. Grounded in the Aug-9 22:42 econ-log read + RESEARCH_TRADE_GOOD_PRICES_1763.md. Part of the trade-economy program (DESIGN_TRADE_ECONOMY_PROGRAM.md). Full pipeline: this design → adversarial review → implement → GATE-2 log-check → verify boot. Do NOT implement until reviewed (batch with #44/#50/#59).

## The finding (from the logs, not a hypothesis)
The Aug-9 22:42 debug.log (#51-extended, curx_analyze full pass, 21 quarters) showed CHI PAID PRICE per good:
- grain 0.01-0.1 | tea 0.01-0.1 | silk 0.01-0.1 | salt 0.1-1 | gold 0.1-1→1-10 | silver 1-10

**tea and silk (luxuries) price in the SAME cheapest band as grain** — a tier INVERSION. Historically luxuries were the DEAREST goods (RESEARCH_TRADE_GOOD_PRICES_1763.md: tea ~12-18× grain; silk a further multiple; gems/porcelain dearer still). ROOT visible in the CHI DEMAND column: **tea demand = 10-100, the LOWEST of all six goods**, vs grain 1000-10000, silk 100-1000. The sim treats tea/silk as abundant + barely-demanded → cheap.

## Why the fix is SEEDING, not the price engine or base_value (settled by #49/#50)
- **base_value (`gold=N`) is INERT** for the mod economy (#49, verified): absent from local_price, the blend, global_mean_price, AND the stockpile seed. Touching it does nothing (and risks the #219 vanilla-trade-request flood). NOT the lever.
- **Price is emergent** from stockpile-vs-demand in se_GLOBALTRADE_split.txt. The two inputs are: (a) the DEMAND svalues (`ln<good>` in DEMAND_svalues.txt / DEMAND_luxury_svalues.txt, aggregated to DEMAND_country_<good>) and (b) the game-start STOCKPILE seed (GOODS_setup_governorship_stockpiles, se_GOODS.txt:69, seeded from physical `_produced` counts). Tier realism = make luxuries SCARCE (low stockpile relative to demand) and DEMANDED (higher ln<good>) vs staples. This is the only real lever, and it's UNCAPPED (unlike the #50 same-good regional gap, hard-capped ~1.9-3×).

## The mechanism (price ≈ f(demand / stockpile)) — and WHY the lever is SUPPLY, not demand
Emergent price rises with demand and falls with stockpile. There are two ways to lift a luxury's price band; **only one is correct**, because a luxury is NOT a necessity:

*** DESIGN CONSTRAINT (user, 2026-08-10): "luxuries are, well, luxuries. people did not starve just to drink tea." ***
Luxury demand is DISCRETIONARY and ELASTIC — a luxury is dear because it is SCARCE and bought at the margin by the wealthy, NOT because everyone needs a large quantity of it. So the fix must come from the SUPPLY/SCARCITY side, NOT by cranking demand.

WHY raising demand is WRONG here:
- Modelling tea demand at grain levels makes tea a NECESSITY — historically false (a High-Qing peasant did not consume tea in grain-like volume).
- Worse, if the engine's pop-consumption/shortage logic reads these demand svalues, inflating luxury demand could make pops prioritise a luxury over food — the exact "starve to drink tea" pathology the user is warning against. A staple shortfall must always bite before a luxury shortfall.
- High MODELLED demand for a discretionary good is a category error even setting the pathology aside.

So the tea/silk price premium must be **scarcity-driven** (supply-constrained), matching reality: tea/silk were dear because they were labour-intensive, regionally concentrated, and export-competed — a small dear supply, not a huge demanded one. Grain is cheap because it is ABUNDANT (high stockpile), not because it is un-demanded. Tea should be cheap-to-make-but-dear-to-buy via LOW STOCKPILE, keeping its demand MODEST (discretionary), so the demand/stockpile RATIO lands it above grain WITHOUT modelling it as a necessity.

## What "alter luxury supply" means — TWO sub-levers (user, 2026-08-10)
Altering luxury supply = EITHER (a) altering luxury BUILDING OUTPUTS [totally fine], OR (b) altering the TRADE GOODS themselves [maybe fine, depends on historical context]. Prefer (a); use (b) only where historically justified and with caution:
- **(a) Building output (PREFERRED, safe).** The luxury-producing buildings (tea works, silk/sericulture, porcelain kilns, etc.) set `base_resources` / output. Trimming a luxury building's output makes the good scarcer at source — a clean, contained, historically-legible lever (luxuries WERE labour-intensive, low-yield-per-unit-effort). This is the qing_salt_yard_building / production-building surface, well within the concrete-object program.
- **(b) Trade-good property (CAUTION, context-dependent).** Altering the trade good's own supply/stockpile seeding is broader-reaching and touches the shared trade layer. Only where the history supports it (e.g. a good that was genuinely export-constrained), and only after (a) is shown insufficient. This is closer to the deep-trade-logic caution the user flags for #50.

## Proposed change (minimal, supply-scarcity-first, global-safe)
1. **Luxury BUILDING OUTPUT scarcity (the PRIMARY lever — sub-lever a).** Trim the per-unit output of the luxury-producing buildings (tea/silk/porcelain/etc. works — the production-building surface, common/buildings/qing_production_buildings.txt + the vanilla luxury buildings) so the standing luxury supply is TIGHT relative to even modest discretionary demand → the demand/stockpile ratio lifts the price band. Models scarce, labour-intensive luxury production, NOT necessity. Do NOT zero output (breaks the physical economy) — trim toward historical scarcity.
   - Secondary (sub-lever b, only if a is insufficient + historically justified): constrain the SEEDED luxury stockpile in GOODS_setup_governorship_stockpiles (se_GOODS.txt, stockpile ← `_produced`). This touches the shared trade layer — treat with the #50-level caution.

### How the two supply levers COMPOSE (they are NOT mutually exclusive — user, 2026-08-10)
The seed maps `stockpile ← _produced` (se_GOODS.txt:69+): the standing stockpile is INITIALIZED FROM the production count. So building-output and stockpile-seed act on the SAME physical supply quantity at different points in its lifecycle:
- **Building output = the FLOW (upstream, durable).** Trimming a luxury building's per-unit output reduces how much is produced each cycle. Because the seed reads `_produced`, this AUTOMATICALLY trims the seeded stockpile too, AND keeps it trimmed every subsequent cycle. It sets the equilibrium scarcity — scarce production → scarce stockpile → dear price, permanently + physically coherent. This is the BACKBONE of the fix.
- **Stockpile seed = the OPENING POSITION (one-time).** Trimming only the game-start standing stockpile, WITHOUT touching production, is a one-shot scarcity that the ongoing flow refills within a few cycles (the flow overwrites the trimmed seed) — so ALONE it DECAYS. WITH the output trim behind it, it simply brings the dear price forward to turn 1 instead of waiting for the constrained flow to draw the stockpile down over several quarters.
- **Therefore they COMPOSE:** (1) building-output trim = the durable lever that sets equilibrium scarcity [PRIMARY]; (2) stockpile-seed trim = an optional OPENING-POSITION ACCELERANT layered ON TOP (not instead) to make the good dear from game start. Reach for the pure-stockpile route as the FAITHFUL surface only for a good whose historical scarcity was DISTRIBUTIONAL (produced in volume but hoarded / export-restricted / market-bottlenecked — the salt-monopoly-wedge or #50-penetration story), NOT productive — that is the "depends on historical context" trade-good case, and where the deep-trade-logic caution applies. For classic labour-intensive luxuries (tea/silk/porcelain), the scarcity is PRODUCTIVE → building-output is both the safer AND the more faithful lever.
2. **Luxury demand stays MODEST + DISCRETIONARY (guardrail, not a lever).** Do NOT raise luxury demand toward staple levels. If anything, CONFIRM luxury demand is elastic/capped so a shortage of it never outranks a food shortage in the engine's consumption/shortage priority. The goal is "small dear supply meets modest discretionary demand," not "everyone needs tea." Leave grain/staple demand alone (correctly high).
3. **Verify the pathology is absent.** Before/after the change, confirm on the logs that a LUXURY shortage does NOT trigger the food-shortage / famine path (DEMAND_shortage_country, the qing_pop/famine linkage) — i.e. tea scarcity raises tea PRICE but never starves pops. This is the load-bearing check the user's note demands.
4. **Tune to bands, verify on logs.** The #51 tea/silk/salt price series is already logged. Set the stockpile-scarcity constants, boot, read the log: target tea/silk to move from 0.01-0.1 up to ≥0.1-1 (salt's band) or 1-10 (a clear luxury premium over grain's 0.01-0.1) — achieved by scarce SUPPLY, with demand held modest. Iterate the constant, don't guess.

## GLOBAL constraint (the user's hard rule)
"It does no good to have a global system which functions fine for CHI but breaks for other countries." The stockpile seed + demand svalues are GLOBAL (every country's economy reads them). So:
- The luxury-scarcity change must be a GENERAL good-property change (tea/silk are scarce-and-dear EVERYWHERE, historically correct — tea was a dear import in 1763 Europe too), NOT a CHI-only override.
- Watch the knock-on: tightening luxury supply raises luxury PRICES globally, which feeds every country's trade income + the price blend. Verify on the logs that no country's economy destabilizes (the #51 logs cover gold/salt/tea/silk; the curx chain covers CHI currency — confirm gbip stays flat, #23 holds). If a global scarcity change perturbs the currency chain, shrink the trim.
- Do NOT touch province{}/country{} blocks (the #219 flood trigger) — this is svalue + seed-var work only ([[two-trade-systems]], [[vanilla-trade-request-flood-open]]).

## Files
- common/buildings/qing_production_buildings.txt (+ the vanilla luxury buildings) — trim the luxury-producing buildings' per-unit output / base_resources (the PRIMARY lever, sub-lever a — safe, contained, historically legible). Identify the tea/silk/porcelain/etc. producers first.
- common/scripted_effects/se_GOODS.txt — GOODS_setup_governorship_stockpiles: constrain the seeded luxury stockpile ONLY as sub-lever b, if building-output alone is insufficient AND history supports it (touches the shared trade layer — #50-level caution).
- common/script_values/DEMAND_luxury_svalues.txt — READ to confirm luxury demand is modest/elastic; adjust ONLY as a guardrail (ensure luxury shortage never outranks food shortage), NOT to raise demand toward staple levels.
- common/script_values/DEMAND_svalues.txt — leave staple (grain/fish) demand alone (correctly high); read DEMAND_shortage_country to confirm the food-shortage path is staple-gated, not luxury-triggerable.
- No base_value edits. No province/country blocks. se_ no-BOM/LF; buildings files check their own BOM/EOL convention before editing.

## Traps / rules
- RHS-comparison rule: no var: on a comparison RHS in the demand svalues.
- Measure-then-tune: the constant is a tuning knob verified on the #51 logs (GATE-2), NOT guessed. Don't ship without the log-check confirming the band moved AND no country broke.
- Global blast radius: this is the highest-blast-radius trade change (every country, every luxury). Adversarial review must scrutinize the cross-country knock-on before implement, and the verify boot must confirm ROW didn't break.
- Keep it MINIMAL: the demand lift is the one lever; only add the stockpile trim if the log shows demand alone didn't move the band. Resist re-architecting the price engine.

## Verify (GATE-2 log-check + boot)
- #51 log: tea/silk CHI paid-price band rises from 0.01-0.1 to ≥0.1-1 (ideally 1-10, a clear luxury premium over grain's 0.01-0.1); tea demand no longer the table floor.
- curx chain: CHI gbip stays flat (~0.97), #23 holds — the luxury lift didn't perturb the currency loop.
- ROW: spot-check a non-CHI country's economy in the logs isn't destabilized by the global luxury-demand rise.

---

## ADVERSARIAL DESIGN-REVIEW CORRECTIONS (2026-08-10) — "do NOT implement as written"; the premise needs rework

The review found the design's two load-bearing justifications wrong on the facts. The finding (tea/silk in the grain band) is real, but the mechanism + even the framing need rework. This SUPERSEDES the "scarcity-first / building-output primary" plan above.

**H1 [HIGH] — the building-output lever is CHI-ONLY, violating the design's own global rule.** qing_tea_workshop/silk_filature/porcelain_kiln are hard-gated to jurchen/chinese_group + placed only by the c:CHI seed — a European silk producer can never hold them. So the "primary" lever is exactly the CHI-only override the design forbids. Making it global means also trimming ROW luxury buildings (row_manufactory/row_plantation), landing the trim on non-CHI economies (Italian/French silk, Caribbean sugar). The genuinely-global luxury lever is the DEMAND_luxury_* svalue system — the one the design rejected.

**H2 [HIGH] — building-output trim is too WEAK + the stockpile ACCUMULATES.** Price ≈ (order/stockpile)×0.6. (a) base_resources=2 is a marginal INCREMENT to a province's inherent tea production, not the bulk — trimming 2→1 can't deliver a 10-100× band move. (b) <good>_stockpile is an ACCUMULATING running balance (produce adds, consume subtracts); if production persistently > (tiny discretionary) luxury consumption, the stockpile grows unbounded → price floors. That accumulation is the LIKELY real root cause of tea sitting in the grain band. An output trim that still leaves production>consumption doesn't change the steady state. => the design's "output=durable equilibrium, seed=accelerant" model is WRONG for an accumulating good; the real question is production-rate vs consumption-rate. [Reviewer flags this is inferred from seed/produce/consume structure, NOT read off the logged stockpile trajectory — CONFIRM against the #51 tea-stockpile series before committing to any lever.]

**H3 [HIGH] — WRONG SCARCITY TYPE per our own research.** The design calls tea/silk PRODUCTIVE scarcity (trim output). RESEARCH_TRADE_GOOD_PRICES_1763.md says the opposite for these exact goods: tea/silk/porcelain were CHEAP IN CHINA, dear in Europe — dearness was DISTRIBUTIONAL/EXPORT (voyage risk, Cape-route margin, European retail), NOT productive. The log measures CHI PAID PRICE — tea being cheap DOMESTICALLY IN CHINA is closer to HISTORICALLY CORRECT than the "inversion" framing admits. The research explicitly warns a Canton-export anchor "would systematically overprice every domestic-only good." => the faithful lever is the EXPORT-PREMIUM / tradezone / penetration layer (#50 territory), NOT trimming China's tea production (which pushes China-domestic tea toward the ahistorical Europe frame). Caveat: the engine computes ONE world price ÷ penetration, inter-country gap hard-capped ~1.9-3× — it literally cannot represent "cheap in China, dear in Europe" beyond ~2× without the #50 cap-lift.

**M1 [MEDIUM] — the "starve to drink tea" pathology is ARCHITECTURALLY IMPOSSIBLE; the demand-lever safety objection is FALSE.** Traced: the famine/kill_pop path (shortage.1) keys ONLY on has_state_food / has_state_food_capacity, written ONLY by grain/food sources. Tea/silk can NEVER add to or drain the state food pool. The per-good shortage_<good> ledger was DELIBERATELY severed from famine in change #47 and never touches kill_pop/unrest/migration. => raising DEMAND_tea CANNOT starve pops. The design's chief safety rationale for rejecting demand COLLAPSES. Demand is in fact a SAFE, GLOBAL, directly-powerful lever (numerator of the price formula; DEMAND_luxury_* is already global + wealth-elastic/discretionary). The residual objection ("category error — modelling tea as a necessity") is a modelling-AESTHETICS preference, legitimate but NOT the safety hazard the design claimed. => demand is back on the table, at minimum as a co-lever, since building-output alone won't hit the target.
   NOTE (user's original concern stands as TASTE, not safety): the user's "people did not starve to drink tea" is still a valid design PREFERENCE against modelling luxury demand at necessity levels — but it's a modelling choice, not a starvation risk. A MODEST discretionary-demand bump (not to grain levels) is both safe AND respects the preference.

**M2 [MEDIUM] — the good list is muddled. Fix it FIRST.** IN SCOPE: tea, silk_cloth, porcelain (the actual pop luxuries showing the inversion). DROP: opium (own se_QING_OPIUM model + ANACHRONISTIC as a dear luxury at 1763 — pre-loads the later crisis), rare_alloys (industrial intermediate, NOT a consumer luxury — category error), gems (raw-mined, NO building lever), luxury_clothing/luxury_furniture (script-only manufactured, no building; price folds in raw-input costs). CLARIFY: raw silk (DEMAND_silk value=0 + industrial BOM only — an intermediate, CORRECTLY cheap) vs silk_cloth (the consumer luxury). If the log's cheap "silk" is RAW silk, that's EXPECTED, not an inversion — must confirm which the log measures.

**LOW (verified sound):** currency-chain safety claim CORRECT — CURRENCY_svalues reads gbip for silver+gold ONLY, so lifting tea/silk price does NOT feed the #23 blend. base_resources trim (vs strata-output modifiers) leaves pop jobs intact.

## REVISED DIRECTION (pre-implementation — needs a user call)
1. **This may not be a bug at all for CHI.** Tea cheap in China domestically is ~historically right (research H3). The "inversion" is really "the mod shows the China-domestic price, which is correctly low." So #52 as 'make tea dear everywhere' partly fights the history.
2. **The faithful feature is an EXPORT PREMIUM (#50 territory):** tea/silk cheap in China, dear as an export / in Europe — which needs the penetration/tradezone layer (and likely the #50 cap-lift the user conditionally authorized), NOT trimming Chinese production.
3. **If a cross-good tier spread IS still wanted globally, the lever is DEMAND (safe, global, powerful), not building output (CHI-only, too weak)** — with a MODEST discretionary bump respecting the user's "not a necessity" preference.
4. **First DIAGNOSE the stockpile trajectory** on the #51 logs (accumulating unbounded vs flow-equilibrium) — that determines whether ANY supply lever can move the steady state.
=> #52 goes back to DIAGNOSIS: confirm raw-silk-vs-silk_cloth + the stockpile trajectory on the logs, and get the user's call on export-premium (#50-ish) vs global-demand-bump vs "it's actually correct for CHI, close it." Do NOT implement the building-output plan.

---

## DIAGNOSIS RESULTS + USER DIRECTION (2026-08-10)

**Diagnostics run on the Aug-9 22:42 #51 logs (the "diagnose first" step):**
- **Q2 — tea stockpile does NOT accumulate unbounded (reviewer's H2b hypothesis REFUTED).** Tea CHI stockpile sits FLAT at the 1000-10000 band all 21 quarters — a stable flow-equilibrium, not a runaway climb. So the low price is an EQUILIBRIUM demand/stockpile ratio (big stable stockpile, modest demand), NOT accumulation. A supply lever COULD move the steady state, but the mechanism is equilibrium-pricing.
- **Q1 — the log's "silk" is RAW SILK, not silk_cloth (reviewer's M2 caveat CONFIRMED).** The tzprobe generator reads the good keyed `silk` (tools/gen_econ_tzprobe.py:47), which in this engine is the RAW trade good — an intermediate that is CORRECTLY cheap. silk_cloth (the manufactured consumer luxury) is NOT what the log measured. => the "silk in the grain band" signal is EXPECTED (cheap raw intermediate), NOT a luxury mispricing. Only TEA (a consumer good) is a genuine signal.

**USER DIRECTION (2026-08-10): EXPORT-PREMIUM is the DEFAULT PATH, research to confirm/disprove.**
The faithful mechanism (per the review + RESEARCH_TRADE_GOOD_PRICES_1763.md): tea/silk were CHEAP IN CHINA, DEAR as an EXPORT / in Europe — dearness was DISTRIBUTIONAL (voyage risk, Cape-route margin, European retail), NOT productive/domestic. So #52 defaults to modelling an EXPORT PREMIUM (China-domestic price stays low = correct; the good becomes dear when exported / in European tradezones), NOT trimming Chinese production (which would wrongly raise the China-domestic price). This is #50 penetration/tradezone territory and likely needs the conditionally-authorized #50 cap-lift.
- Research task dispatched to CONFIRM or DISPROVE the export-premium framing: was the China-domestic price of tea/silk genuinely low (making the mod's current CHI-cheap correct), and was the dearness genuinely export/distributional (not a domestic luxury premium)? If research CONFIRMS → build the export premium (merge with #50). If research DISPROVES (e.g. there WAS a domestic luxury premium for fine tea/silk within China) → reconsider a domestic lever.
- REVISED SCOPE: raw silk is OUT (correctly cheap intermediate); silk_cloth + tea are the consumer luxuries; the mechanism is EXPORT-side, not domestic-production-side.

## SILK_CLOTH PRICE BEHAVIOR — NOT MEASURED (probe gap found, user Q 2026-08-10)
Asked how silk_cloth (the actual consumer luxury) priced: it was NEVER MEASURED this boot. The #51 TZP probe's GOODS list is silver/gold/grain/salt/tea/silk — the "silk" is RAW silk (intermediate, correctly cheap), NOT silk_cloth. silk_cloth appears 33k× in debug.log but ONLY as a boot-time FORENSIC var-type classification ("stockpilesilk_cloth = REAL"), NOT runtime price/stockpile/demand values. So there is ZERO runtime price-behavior data for silk_cloth (or porcelain) in this boot.

What the CODE says about silk_cloth structure (not behavior):
- It IS a consumer luxury (full wealth/price-responsive demand model, like refined_sugar/DEMAND_refined_sugar) — so it SHOULD carry a real luxury price, unlike raw silk.
- It's a MANUFACTURED/script-only good (cottage + factory, from raw silk) → its price folds in the RAW-SILK input cost, which is cheap → the finished luxury likely INHERITS a low base (the review's M2 concern).

CONSEQUENCE: the #51 diagnostic measured the WRONG good for #52. To actually diagnose consumer-luxury tier pricing, the econ probe must track silk_cloth + porcelain (the consumer luxuries), NOT raw silk. => PRE-REQUISITE for #52: extend gen_econ_tzprobe.py GOODS to add silk_cloth + porcelain (+ tea already there), reboot, and read THEIR price/stockpile/demand before choosing any #52 lever. Without this the export-premium-vs-domestic question can't be answered on real data for the finished luxuries. (Coordinates with #35: this is exactly the kind of temporary probe-extension that stays until #52 is verified, then strips with the rest.)

## PROBE SCOPE CORRECTED — track the WHOLE luxury tier, not a hand-picked few (user, 2026-08-10)
Scoping the probe extension to silk_cloth+porcelain repeats the "measured the wrong good" mistake in miniature: #52 is about the TIER (the luxury class vs staples), so the diagnostic must cover the whole tier or it risks another cherry-picked miss.

FULL luxury roster (every DEMAND_luxury_<good>, common/script_values/DEMAND_luxury_svalues.txt):
alcohol, chili, chocolate, clothing, coffee, furniture, gems, luxury_clothing, luxury_furniture, maize, opium, peanut, porcelain, potato, spices, sugar, sweet_potato, tea, tobacco (+ silk_cloth, the finished-silk luxury).

TWO refinements so "track everything" doesn't become noisy overkill:
1. NOT all of these are 1763 LUXURIES. maize/potato/sweet_potato/peanut/chili are NEW WORLD CROPS becoming STAPLES/subsistence in Qing China (the #384 diffusion mechanic), NOT dear luxuries. The #52 TIER comparison is TRUE luxuries (tea, silk_cloth, porcelain, coffee, chocolate, spices, gems, luxury_clothing, luxury_furniture, alcohol, tobacco, sugar) vs STAPLES (grain, fish, + the New World food crops). Track the New World crops too (completeness), but classify them staple-side in the tier read.
2. PROBE COST: each good ≈180 generated log-block lines; the full tier + staples is a big log-volume bump. Acceptable for a TEMPORARY diagnostic boot (strips with #35), but do it deliberately — this is a measure-then-strip probe, not a permanent log.

REVISED #52 PREREQUISITE: extend gen_econ_tzprobe.py GOODS to the full luxury tier (all DEMAND_luxury_* goods + silk_cloth) PLUS the staple baseline (grain/fish already partly there), reboot, and read the whole tier's price/stockpile/demand — so #52 measures luxuries-as-a-CLASS vs staples, and the export-premium-vs-domestic question is answered on the complete tier, not tea alone. Classify New-World-crops staple-side. Then choose the lever.

## CORRECTION — WHY the New World crops are classed as luxuries (user challenge, 2026-08-10)
I earlier asserted maize/potato/etc "aren't 1763 luxuries" then noted the engine classes them as luxuries WITHOUT reconciling it. Checked the actual trade-good defs (common/trade_goods/00_imp19c.txt) — I was WRONG per the engine:
- grain / salt / fish = `category = 1` (staples)
- maize / sweet_potato / potato / peanut / tea / coffee / opium / sugar = `category = 2` (SAME category — New World food crops sit in the EXACT same engine category as tea/coffee/sugar/opium)
- porcelain = `category = 4` (manufactured)
The `DEMAND_luxury_*` system is keyed off category-2 membership, so maize IS a "luxury" to the engine BECAUSE it shares category 2 with tea/coffee. This is inherited vanilla-Imperator categorization (colonial/cash-crop goods lumped as category 2), with NO 1763-China-aware sense that a New World food crop had become peasant subsistence in Qing China.

CONSEQUENCE — this REFRAMES #52:
- The tier "inversion" is not only supply/demand magnitudes; the engine's GOOD-CATEGORY SCHEME itself is not 1763-China-historical (New World food crops lumped with tea/silk luxuries). maize being luxury-demand-driven is a CATEGORY artifact, not a tuning bug.
- My "classify New World crops staple-side" is therefore a RECLASSIFICATION (move maize/potato/sweet_potato/peanut from category 2 → 1), NOT just a probe-labelling choice. Reclassifying goods touches the shared category scheme that drives the whole demand/luxury system for EVERY country — a bigger, deep-shared-layer change (the #219/two-trade-systems caution zone), and globally it may be WRONG (maize in the Americas/Europe was arguably more cash-crop than subsistence). So reclassification is NOT obviously correct and NOT in the minimal #52 slice.
- For the PROBE: still track the whole category-2 set (that IS the engine's luxury tier), but LABEL in the read which are true-luxury (tea/coffee/sugar/spices/tobacco/chocolate + porcelain[cat4] + silk_cloth + gems + luxury_clothing/furniture) vs New-World-food-crop (maize/potato/sweet_potato/peanut/chili) — the latter are category-2 in the engine but subsistence-in-Qing historically. The DIVERGENCE between engine-category and 1763-China-reality is itself a #52 finding to surface, not silently "fix" by reclassifying.
- OPEN QUESTION for the user (do NOT assume): should #52 (a) leave the category scheme alone and only tune supply/demand within it, or (b) also RECLASSIFY the New World food crops to staples for the Qing? (b) is historically tempting for China but globally dubious + touches the shared category layer — recommend (a) unless the user wants the deeper reclassification.

## CORRECTION #2 — the New World crops are FORK-ADDED by us, category=2 was a CLONE ARTIFACT (user challenge, 2026-08-10)
I said "inherited vanilla-Imperator categorization." WRONG — checked git: the 5 New World crops (maize/sweet_potato/potato/peanut/chili) were FORK-ADDED by us in commit f45c9ce7b (freekumquats, 2026-07-05, "New World crops (#64-fix)"). The commit message is explicit: they were "cloned from the TOBACCO cash-crop archetype (category 2, food byproduct)" purely to fix a #64 blocking defect (28 provinces referenced goods the engine never loaded → parse error / zero food). The `category = 2` was INCIDENTAL — copied wholesale from the tobacco template to unblock the crash, NOT a considered "these are luxuries" decision. Their 1763-China role (subsistence crops) was never weighed.

CONSEQUENCE — reclassification is LOWER-risk than CORRECTION #1 framed it:
- Moving maize/potato/sweet_potato/peanut (the FOOD crops) from category 2 → 1 (staples, with grain) is CORRECTING OUR OWN INCIDENTAL CLONE, NOT fighting the engine or an inherited upstream layer. Much more defensible than "reclassify a shared scheme."
- It IS still globally-scoped (category drives the demand system for every country) — so it's not zero-risk, and must be verified across countries — but it's fixing a fork shortcut, not touching load-bearing inherited machinery.
- chili is a genuine flavour/condiment good (arguably stays category-2-ish, or its own thing); the clear staples-by-history are maize/potato/sweet_potato/peanut (bulk subsistence calories in Qing China). tea/coffee/sugar/tobacco/opium legitimately stay category 2 (real cash-crop luxuries).
- This SUPERSEDES CORRECTION #1's "recommend (a) leave categories alone": reclassifying the 4 food crops is now a reasonable, low-ish-risk option because we're fixing our own clone, not a shared inheritance. Still the user's call, but the risk framing was wrong — it's not the deep-inherited-layer change I described.

REVISED OPTIONS for #52's category question:
(a) leave categories, tune supply/demand only [minimal];
(b) reclassify the 4 New World FOOD crops (maize/potato/sweet_potato/peanut) 2→1 to fix our own incidental tobacco-clone [corrects a fork shortcut; globally-scoped but defensible; verify cross-country];
Recommend (b) is now viable (was wrongly framed as too-risky). Still gate on the export-premium research + the full-tier probe before finalizing.

## DECOUPLING — the reclassification is NOT gated on the luxury probe/research (user, 2026-08-10)
I wrongly wrote the New-World-food-crop reclassification (maize/potato/sweet_potato/peanut, category 2→1) as "gated on the export-premium research + full-tier probe." That conflates two INDEPENDENT things:
- **The reclassification** is a STANDALONE CORRECTNESS FIX: we accidentally cloned tobacco's category=2 onto four subsistence food crops (f45c9ce7b, a #64 parse-crash unblock). maize/potato/sweet_potato/peanut are bulk subsistence calories in Qing China → they belong in category 1 (staples) with grain. This is justified on its OWN terms and needs NOTHING from the luxury investigation.
- **The export-premium research + full-tier probe** gate the LUXURY-PRICING question (are tea/silk/porcelain dear enough; export-vs-domestic). Different question, different goods.
=> The reclassification has its OWN (and only) gate: a CROSS-COUNTRY verification that moving the 4 crops 2→1 doesn't break another country's demand (category is global — every country's demand system reads it). That is the correct + sufficient gate. It does NOT wait on the tea/silk export research or the luxury-tier probe.
=> Split #52 into two independent workstreams: (1) NEW-WORLD-CROP RECLASSIFICATION — a self-contained correctness fix (maize/potato/sweet_potato/peanut 2→1; chili TBD), gated only on its own cross-country verify boot; can proceed independently. (2) LUXURY TIER PRICING (tea/silk_cloth/porcelain export-premium) — gated on the export-premium research + full-tier probe. These are NOT sequenced; (1) can ship first.
