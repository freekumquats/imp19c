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
