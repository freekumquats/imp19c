# DESIGN — trade-economy realism program (#44 / #46 / #49 / #50 / #51 / #52)

**Status:** program design + process record, 2026-08-09. Captures the reasoning + user-set process so it survives context compaction. No behavioral tree edits from this doc; it governs the build sequence.

## Origin
Started from a boot observation (#46: silver sometimes sells for more than gold in the reserve-sell action). Investigating led to a chain of findings about the whole trade-price layer. The user's throughline: **a globalized economic system must be verified GLOBALLY, and the logs are the instrument that proves whether it is well-designed.**

## What the code actually does (verified directly in source, not summaries)
- **`local_price_<good>` is per-tradezone** (`GT_set_tradegood_price`, se_GLOBALTRADE_split.txt:5893): `order/stockpile × 0.6` [÷ food-basket for food] [+ manufactured input costs]. Base `gold=N` is NOT an input.
- **The country import price is a global blend** (`GT_split_get_global_import_unit_price_tradegood`, :2500-2710): `Σ over 22 TZ ( local_price × <TZ>_pct_of_global_stockpile )`, sqrt'd (line 2702 = the #23-fixed Babylonian primitive) → ONE world price, same composition for all countries.
- **Weights are normalized stockpile shares** (`<TZ>_stockpile / global_stockpile`, :1458-1470), sum ≈ 1.
- **Country pays** `country_unit_price = world_price ÷ (0.5 + country_global_market_penetration)` (:2718-2732).
- **Penetration is per-TZ + geographic** (`GT_split_get_country_global_market_penetration_tradegood`, :1776-2009): `Σ over 22 TZ ( <TZ>_stockpile_share × TZ_penetration_<TZ> )`, then `× 0.4545`, capped at 1. `TZ_penetration_<TZ>` (SHIPPING_svalues.txt:2181+) is driven by `var:shipping_<TZ>` — the country's own shipping power INTO that zone — plus subjects'/trade-partners' shipping.
- **The metal SELL-RESERVE price** (INCOME_sell_reserves, se_INCOME.txt:705-739, called by the economy-view sell buttons EE_scripted_guis.txt:545-620): treasury income = `global_base_import_price_<metal> × amount`. So the gold/silver sell value IS the blended world price, recomputed each quarter.
- **Base `gold=N` is INERT for the mod economy** — traced absent from local_price, the blend, global_mean_price, AND the game-start stockpile seed (GOODS_setup_governorship_stockpiles, se_GOODS.txt:69, seeds from `_produced` physical counts). Only OPEN question: does the vanilla ENGINE read it (province trade value / commerce / AI)? — a cheap boot probe (#49).

## Key inference (adversarially reviewed, math-checked)
`price_CHI / price_GBR = (0.5 + pen_GBR) / (0.5 + pen_CHI)` — **the world price CANCELS.** So the same-good inter-country gap depends ONLY on the two penetration terms (not local_price seeding, not the sqrt → #50 carries NO #23 risk). BUT penetration ∈ [0,1] and is shrunk `× 0.4545`, so the **same-good inter-country gap is HARD-CAPPED at ~1.9× (3× absolute)**. Worked example (silk, yellow_sea=90% of world stockpile): China pays ~38% less than Britain — real but that ~1.9× is the ceiling. The cross-good tier spread (tea vs grain) is a DIFFERENT axis, lives in local_price, and is NOT capped.

## Findings → tickets
- **#46 (metal sell price):** silver occasionally > gold because both share the flat 0.2 base → nothing anchors gold above silver; the sell price floats on the volatile blend. USER DIAL-BACK: this is INVESTIGATE, not assumed-bug — a transient inversion is historically plausible; only a frequent/large/non-reverting swing (the #23 undamped-feedback class on the metal ratio) is broken. MEASURE on the verify boot, then judge. Base-value fix DISCARDED (inert, verified).
- **#49 (base-value table):** flat 0.2 is INERT for the mod economy — differentiating is a no-op unless the vanilla engine reads it (boot probe). Likely CLOSE as no-op; route price realism through #44/#50/#52.
- **#50 (regional divergence):** the geographic mechanism ALREADY EXISTS (per-TZ shipping-driven penetration) and carries no #23 risk — but is hard-capped at ~1.9-3×. DECISION for the user: is ≤~2-3× Canton-vs-London enough (already ~satisfied) or is a bigger divergence wanted (penetration cannot deliver it — would need lifting the cap / 0.4545 shrink)? History says the real gap was larger, so the cap is itself a candidate design limitation to lift.
- **#52 (cross-good tier realism):** luxuries should price ~10-20× staples (research); currently flat. Uncapped, lives in supply/demand seeding — the more impactful, more achievable lever than same-good regional arbitrage.
- **#44 (salt revenue):** salt gabelle income too low (flat ~27/quarter constant). REWORK: revenue = **output × market price × gabelle mark-up**. The mark-up BRIDGES commodity price → taxed retail value (historically ~30-50× cost, a POLICY artifact of the Lianghuai monopoly, NOT intrinsic value — so NOT a base/market-value edit). Graded by the 兩淮鹽政 Salt Commissioner. See #44 for the full window/office build.

## Historical anchors (research/RESEARCH_TRADE_GOOD_PRICES_1763.md, [[trade-good-prices-1763-research]])
- Gold ≈ 14-15× silver by 1763 (China 1:10 arbitrage was OVER by the bookmark; gold > silver at every Qing point). Silver-above-gold is ahistorical.
- Luxury ≈ 10-20× staple (tea ~12-18× grain; silk a further multiple above cotton).
- Salt gabelle ~30-50× retail-over-cost markup (WEAK source, order-of-magnitude).
- Metals (iron/copper/tin/lead) UNRESOLVED — research gap; do not touch metal values.

## PROCESS the user established (governs the whole program)
1. **Design the logs FIRST** — "the logs will confirm whether the system is properly designed or not, so long as you design the logs properly." Instrument before building.
2. **Verify GLOBALLY, not just CHI** — the sim couples all countries through the shared world blend + stockpile shares, so a break in GBR/India propagates back into CHI within quarters. Logs MUST sample multiple countries (CHI + GBR/FRA/NED). "A global system that works for CHI but breaks elsewhere will pollute the correct functionality soon enough."
3. **Log broadly** — err toward more goods/countries than necessary (it's a removed diagnostic; volume has cost but coverage matters more here).
4. **TWO-GATE log-check per feature:**
   - GATE 1 (now, #51): extend logs to capture the CURRENT baseline across all axes + broadly, so a global side-effect is visible pre-change.
   - GATE 2 (after each feature): after it's implemented AND passes adversarial code-review, RE-CHECK the logs — confirm the feature's NEW vars/effects emit (so the verify boot captures it) AND that no FOREIGN economy broke.
   - Pipeline per feature: implement → adversarial code-review (correct?) → log-capture check (will the boot show it?) → user verify boot (behaves right, globally?).
5. **Base value is inert / flat table left alone** — realism goes through the script market (local_price seeding, penetration) + the salt mark-up, never the base `gold=N` table (flood-safe: never touch province{}/country{} — [[two-trade-systems]], [[vanilla-trade-request-flood-open]]).
6. **#23 safety** — the world-price sqrt is load-bearing for currency stability; #50's penetration path avoids it (world price cancels), but any blend-side change must be verified against #23 on the econ boot ([[currency-sqrt-root-cause]], #35 tooling restored).

## Build sequence (gated)
#51 (logs, GATE 1) → BLOCKS → #44 / #46 / #50 / #52, each through the per-feature pipeline (implement → review → GATE-2 log-check → verify boot). #49 = a cheap vanilla-reader boot probe, likely closes as no-op. Companion doc: design/DESIGN_REGIONAL_TRADE_PRICES_50.md (the #50 penetration analysis + adversarial-review corrections).
