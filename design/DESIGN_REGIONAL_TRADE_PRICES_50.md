# DESIGN — regional trade-good price divergence in the script market (#50)

**Status:** design/feasibility note from the #50 code investigation (2026-08-09). No tree edits yet. Feeds off #49 (China-anchored base values) but does NOT depend on it — the base `gold = N` value is not read by the price sim at all, so #50 and #49 are independent.

## The question
In 1763 the same good had very different prices by region (silk/tea cheap at Canton, dear in London; silver dearer in China). The engine's single `gold = N` base-value field can't express that. Where does the divergence live? The mod's parallel **script market**.

## What exists today (investigation, file:line confirmed)
Two layers, answering different questions:

1. **`local_price_<good>` — genuinely per-tradezone.** `GT_set_tradegood_price` (se_GLOBALTRADE_split.txt:5893-5975) is scoped to a TZ province, called once per TZ (22×) by `GT_set_tradegood_price_all_TZs` (5799-5891). Each reads THAT TZ's own `<tz>_total_order_size_<good>` / `<tz>_stockpile_<good>`. So `local_price` genuinely differs by region today, driven by each TZ's own supply/demand ratio. Formula: order/stockpile × 0.6 (flat) [÷ food-basket if food] [+ manufactured-input-cost terms built from the flat WORLD `global_mean_price` of inputs]. No distance/shipping/origin term; no elasticity clamp (placeholder comment only). Base `gold=N` is NOT an input.

2. **`country_unit_price_<good>` — a global blend that ERASES the divergence.** `GT_split_get_global_import_unit_price_tradegood` (2500-2710) sums each TZ's `local_price` weighted by that TZ's **share of global stockpile** (not geography), then sqrt-compresses (line 2702 — the #23-fixed Babylonian primitive). `GT_split_get_country_import_unit_price_tradegood` (2718-2732) divides by (0.5 + the country's market penetration). So what a country PAYS is a stockpile-share-weighted average of all 22 TZ prices, adjusted only by its own access — **no region-of-origin/destination term**. Real per-TZ signals exist but nothing routes "cheap in source, dear in destination" into what anyone pays.

`global_mean_price_<good>` (se_PRICE.txt) is a plain arithmetic mean of `local_price` over all 22 TZs, quarterly-refreshed (#145 fix); it feeds manufactured-goods input costs (flat world average).

## Tradezones (22, hardcoded — TRADE_svalues.txt num_of_TZs=22)
China-adjacent: **yellow_sea, upper_yangtzi**. Europe/Atlantic: **atlantic_seaboard, central_europe, west_mediterranean, baltic, east_europe, east_mediterranean** (6). Plus india, the SE-Asia/Indochina zones, the Americas, Africa, steppes, middle_east. **The China-vs-Europe granularity needed for the arbitrage already exists.** `neighbouring_tradezones` adjacency graph is built (se_TRADE.txt:962-1300+) but its reader wasn't found — possibly unused by pricing.

## Three levers — and why the multiplier is the WEAKEST (user challenge, 2026-08-09)
`local_price_<good>` IS the regional price — it is not flat; it is `order_size / stockpile × 0.6`, i.e. pure regional supply/demand. So a per-(good, TZ) multiplier is a hardcoded fudge on an already-emergent price, not "adjusting a flat price." Reframed, there are three distinct levers:

1. **The regional price's INPUTS — the honest fix.** `local_price` diverges by region only as much as regional SUPPLY and DEMAND diverge. If Canton silk isn't cheap enough / European silk not dear enough, the real cause is unrealistic per-region production/stockpile + demand seeding (China should be silk-abundant → low price; Europe silk-scarce + high-demand → high price). Fix the seeding and divergence emerges for the RIGHT reason, no hardcoded table. This is "adjust the regional price directly," done properly.

2. **The regional price's FORMULA — the multiplier (WEAKEST).** The `× 0.6` is a flat global scale; a per-(good, TZ) multiplier just makes that scale regional (silk ×0.7 in yellow_sea, ×1.4 in Europe). It works and is surgical/downstream-safe/flood-safe, BUT it hardcodes the answer instead of letting supply/demand produce it — brittle, and it misrepresents WHY Canton silk is cheap. Downgraded from "recommended" to "fallback / quick-and-dirty only."

3. **What the country PAYS — the blend (the actual blocker).** THE CRITICAL CATCH: even a perfectly-diverged `local_price` never reaches the player, because `country_unit_price` (GT_split_get_global_import_unit_price_tradegood, 2500-2710) averages all 22 TZs by stockpile share. So you can get regional prices exactly right and a Chinese player STILL pays the world-average for silk. Any regional realism the player is meant to FEEL must come through the blend — either distance/adjacency-weight it (using the built `neighbouring_tradezones` graph as a hop proxy) or let a country buy at its own region's `local_price` rather than the global average. Bigger change, touches the #23-fixed sqrt at 2702 → higher review burden + must be verified against #23 regression on the #35 boot.

**RECOMMENDATION (reversed from the initial "Hook 1" lean):** the right build is **(1) realistic per-region supply/demand seeding** so `local_price` diverges for real reasons, **PLUS (3) fixing the blend** so a country pays closer to its own region's price than a flat world average. The multiplier (2) is a lie the blend dilutes anyway — use it only as a stopgap if (1)+(3) are out of scope for a slice. All three are script-market-only, so all flood-safe ([[two-trade-systems]]); (3) is the one that touches #23.

### ADVERSARIAL RE-READ (2026-08-09, code verified directly, NOT via the subagent summary)
I read `GT_set_tradegood_price` (5893), `GT_split_get_global_import_unit_price_tradegood` (2500-2710), the `<TZ>_percentage_of_global_stockpile` computation (1458-1470), and `GT_split_get_country_import_unit_price_tradegood` (2718-2732) directly. The three structural claims HOLD: per-TZ local_price ✓; the country price is a stockpile-share-weighted average of all 22 TZs' local_price, sqrt'd, then ÷ (0.5 + the country's market penetration) ✓; base gold=N absent from the formula ✓. The weights ARE normalized shares (`<TZ>_stockpile / global_stockpile`, summing to 1), so "weighted average" is accurate.

**BUT the weighting has a consequence that BREAKS the naive "seeding alone" fix:** the weight is SHARE OF WORLD STOCKPILE, so a region that produces most of the world's supply of a good DOMINATES the blend. If China holds most of the world's silk/tea stockpile, the `global_base_import_price` for silk is already pulled toward China's LOCAL price — so the world price ≈ China's price, and China and Britain end up paying NEARLY THE SAME LOW price. Lever (1) alone (make Canton silk cheap via seeding) would drag the WORLD price down too, helping Britain as much as China — the OPPOSITE of the arbitrage. So:
- **Lever (3), the blend, is LOAD-BEARING, not optional.** Only breaking the single-world-price blend (weight NEARBY TZs more per importing country, or let a country buy at its own region's local_price) makes Canton silk cheap for China yet dear for Britain. Seeding makes the source cheap; without the blend fix, "cheap at source" leaks to everyone through the shared world price.
- **`country_global_market_penetration_<good>` (÷ 0.5 + pen, line 2728) is a bigger lever than the summary credited** — it is the ONE existing per-country differentiator of what's actually paid. Before designing (3), MUST read GT_split_get_country_global_market_penetration_tradegood (1776) + TZ_penetration_<zone> (SHIPPING_svalues) to determine whether penetration is already REGIONALLY structured (does China have high penetration in yellow_sea?). If it is, the geography hook may belong THERE (bias penetration by proximity) rather than in the blend sum — smaller and it AVOIDS the #23 sqrt. This is the key unknown; do not design (3) until it's traced. (Subagent flagged Q6c provisional; I have NOT resolved it either.)

Corrected bottom line: the seeding+blend direction is right, but SEEDING ALONE CANNOT produce the arbitrage (the stockpile-weighted blend makes the dominant producer's price ≈ world price). The blend/penetration path is essential and under-investigated — resolve the penetration question first; it may move the cleanest hook off the #23-touching sum entirely.

## Interactions to respect
- **#23 currency:** the blend path holds the #23-fixed sqrt (2702). Hook 1 avoids it entirely; Hook 2 must be reviewed against #23 regression. Verify either on the #35 econ boot.
- **DEMAND:** `local_price` numerator is built from governorship DEMAND (one hop up) — a TZ multiplier composes cleanly.
- **Trade Agreement / TZ-penetration:** per-country ACCESS multiplier (divides the blended price), not a per-good price term. se_DIP_TRADE.txt not read this pass — read before finalizing in case it already carries TZ-scoped state.

## Scope recommendation
Hook 1 is a **worthwhile, low-risk** enrichment: it makes Canton-sourced luxuries genuinely cheap at source and dear in Europe, which is the historically-right texture and reinforces the China-trade arbitrage. Ship it as its own reviewed slice AFTER the #49 price research lands (to pick the per-region multipliers from real ratios). Hook 2 is optional depth — only if the blend's averaging proves to wash Hook 1 out in play. Neither needs #49's base-value edit; neither risks the #219 flood.

## Open / unverified (flagged by the investigation)
- `TZ_is_<zone>_tradezone` trigger bodies not located (only usage).
- `neighbouring_tradezones` adjacency reader not found — unverified consumer.
- se_DIP_TRADE.txt / trade_diplo_buttons.txt / MODIFIER_GLOBAL_STATE_TRADE_ROUTES not read — Q6(c) provisional.
- Whether trade_goods base `gold=N` is read anywhere outside the price sim (vanilla AI, events) — only confirmed absent from the two price files (feeds #49's flood-safety verdict; a full-repo negative still owed there).

---

## Historical anchors (from research/RESEARCH_TRADE_GOOD_PRICES_1763.md, 2026-08-09) — and two corrections they force

The China-anchored 1763 price research (memory [[trade-good-prices-1763-research]]) lands two results that directly reshape this design and the sibling tickets:

1. **gold ≈ 14-15× silver by 1763 — the "China cheap gold" arbitrage is a 17th-c. phenomenon, OVER by the bookmark.** Cantillon/von Glahn/Melitz/Peng Xinwei agree the China (~1:10) vs Europe (~1:15) gap had converged to near parity (~1:14.5-15, both in China and internationally) by 1750-1763. So: (a) there is NO 1763 reason to model a China-specific gold discount (that would fit a 1600-1700 start, not this one); (b) the #46 "oddity" (silver trading ABOVE gold, both off an identical 0.2 base) is **backwards from history at every point in the Qing** — gold should always be several × silver by weight. This is a base-value ordering fact, and per #49 it only matters if a live system reads `gold = N` (still to be traced) — but it is NOT a regional-divergence problem and should NOT be chased through #50's script-market hooks.

2. **luxury tier ≈ 10-20× staple tier.** Bohea tea ~17.8 taels/picul (1766, no-advance spot) vs rice ~1-1.5 taels/shih (~1 tael/picul) ⇒ tea ≈ 12-18× grain per comparable weight; silk sits a further multiple above cotton, cotton above grain. Cross-checked independently via wages (one picul of tea ≈ ~200 days' unskilled Canton wage vs ~3-4 kg rice/day). The mod's flat 0.2-for-everything collapses this whole order-of-magnitude spread to 1:1.

**Salt (the #44 priority) — a TAX MARK-UP, not a base-value bump.** Raw salt 1-2 wen/catty (場灶 production cost) vs Changlu retail 13-16 wen/catty (Kangxi) ⇒ **~7-14× markup** for the 1763 window, from 清史稿·食貨志·鹽法 read directly + the 1740 Hankou salt-price case (revised DOWN from an earlier weak-sourced 30-50× min.news figure, which may describe a later Qing period). DESIGN CONSEQUENCE (unchanged, strengthened): the salt price gap is a POLICY artifact (Lianghuai monopoly), not an intrinsic commodity value — so #44 must model it as a tax/mark-up layered on a MODEST raw base, NOT by raising salt's `local_price`/base everywhere salt is produced. This is consistent with routing salt revenue through the Salt Commissioner office + output (#44 R7), not through a bespoke high salt price.

**Metals UNRESOLVED (research gap, flagged):** no 1763 comparative iron/copper/tin/lead ratio found — the mod's existing lead=0.4 could be neither corroborated nor refuted. Do NOT touch metal values on this pass; a library/JSTOR follow-up (Donald Wagner; 滇銅京運 copper records) is owed.

### How the anchors interact with the levers (the load-bearing point, restated)
The 10-20× luxury:staple spread is what #50 wants players to FEEL regionally (Canton tea cheap, London tea dear). But per the adversarial re-read above, the stockpile-share-weighted blend means: if China dominates world tea/silk stockpile, the WORLD price ≈ China's price, so widening China's local_price down (via seeding to the real ratios) drags the world price down for EVERYONE — it does not by itself create the Canton-cheap/London-dear split. The historical ratios tell us WHAT the divergence should be; they do NOT change the finding that the **blend/penetration path is the load-bearing lever**. Sequence unchanged: (i) resolve whether country_global_market_penetration is regionally structured; (ii) if yes, bias it by proximity (small, avoids the #23 sqrt); (iii) seed per-region supply/demand to the researched ratios so the now-regional prices land at historical multiples; (iv) the per-(good,TZ) multiplier remains a stopgap-only lie.

## ADVERSARIAL-REVIEW STATUS
The three structural code claims (per-TZ local_price; stockpile-share-weighted blend; base gold=N unread) were re-verified DIRECTLY against se_GLOBALTRADE_split.txt (5893, 2500-2732, 1458-1470) on 2026-08-09 — they hold. The design's remaining risk is entirely in the UNTRACED `country_global_market_penetration` / `TZ_penetration` path (whether geography already lives there). This doc is dispatched for adversarial code-review before ANY implementation; no tree edits until the penetration question is resolved and a slice is scoped + user-cleared.

---

## PENETRATION PATH — TRACED (2026-08-09, resolves the load-bearing unknown)

Read directly: `GT_split_get_country_global_market_penetration_tradegood` (se_GLOBALTRADE_split.txt:1776-1980) and `TZ_penetration_yellow_sea` (SHIPPING_svalues.txt:2181+).

**FINDING: the geography hook the design hypothesized ALREADY EXISTS.** `country_global_market_penetration_<good>` is NOT a flat access scalar — it is built per-TZ as `Σ over 22 TZs of ( <TZ>_percentage_of_global_stockpile_<good> × var:TZ_penetration_<TZ> )` (1802-1980). And `TZ_penetration_<TZ>` is **already geographically structured**: it is driven by `var:shipping_<TZ>` — the country's own trade/shipping power INTO that specific tradezone (2200-2207) — plus its subjects' and trade-partners' shipping into that zone (2212-2248). A country present in / trading heavily with yellow_sea has high `TZ_penetration_yellow_sea`; a distant country has ~0 there. (AI-minor shortcut: 0.5 if it owns a province in the zone, else 0.1, 2182-2199.)

**So how the two stockpile-weighted sums combine (the crux):**
- Price blend: `global_base_import_price = Σ( stockpile_share × local_price )` → sqrt → ONE world price. Composition is stockpile-share-weighted, SAME for every country.
- Country pays: `country_unit_price = world_price ÷ (0.5 + Σ( stockpile_share × TZ_penetration ))`.

The world price's COMPOSITION is fixed (no country pays a differently-composed basket). What differs per country is the DIVISOR: a country with high shipping into the high-stockpile zones of a good gets a bigger penetration sum → pays LESS. **Therefore the arbitrage the user wants is ALREADY PARTLY MODELLED, via a different mechanism than "regional prices":** if China dominates yellow_sea silk stockpile AND has high `shipping_yellow_sea`, its penetration for silk is large → it divides the world price down → **China pays less for silk than a low-shipping distant Britain.** "Source region pays less" emerges today as a market-ACCESS discount, not a per-TZ price.

### What this means for the design (REVISED conclusion, supersedes the earlier lever ranking)
1. **Do NOT build a new blend-side distance term, and do NOT touch the #23 sqrt.** The per-country differentiation already lives in the penetration divisor, cleanly separated from the sqrt'd world-price blend. This removes the highest-risk lever entirely.
2. **The real questions become empirical, not structural:** (a) does the Qing actually HAVE high `shipping_yellow_sea` / `shipping_upper_yangtzi` at the 1763 seed (i.e. is its silk/tea penetration already high)? (b) is the resulting China-vs-Britain price gap large enough to FEEL, or does the sqrt-compression + the flat 0.5 floor wash it out? Both are BOOT-MEASURABLE (dump `country_unit_price_silk` for CHI vs GBR on the #35 econ boot) — the honest next step is to MEASURE the existing gap before building anything.
3. **If the existing gap is too weak,** the smallest lever is to boost the Qing's `shipping_<China-TZ>` seed (or the `MODIFIER_tradezone_penetration_from_own_trade_power` scale), NOT a new price term — amplifying a mechanism that already works, near-zero blast radius, nowhere near #23.
4. **Seeding realistic per-region SUPPLY** (China silk/tea-abundant) still matters — it drives both `local_price` divergence AND the stockpile shares that weight penetration — but it is a TUNING/seed input, not new machinery.
5. The per-(good,TZ) `local_price` multiplier is now firmly REJECTED (not even a stopgap): it fights the stockpile-weighted blend and misrepresents cause.

### Residual unknowns (smaller now, still flagged)
- Whether CHI's 1763 `shipping_<China-TZ>` seed is actually high (measure on boot).
- Magnitude: does sqrt-compression + the `0.5 +` floor leave a perceptible CHI-vs-GBR gap? (measure on boot).
- `TZ_penetration` also folds in trade-agreement partners' shipping (2238-2248) — a Qing trade agreement with a European power would raise the EUROPEAN side's China-TZ penetration too; confirm this doesn't erase the gap the wrong way.

**BOTTOM LINE (design complete):** regional price divergence that the player FEELS is already implemented as a market-penetration discount keyed on per-TZ shipping power — the mechanism is sound and avoids the #23 sqrt. The correct #50 work is (i) MEASURE the existing CHI-vs-ROW price gap for China goods on a boot; (ii) if weak, amplify the EXISTING penetration/shipping seed; (iii) seed realistic per-region supply so shares/prices are historical. No new blend machinery, no #23 risk, no trade_goods base edit, flood-safe throughout. This doc is now ready for adversarial code-review.

---

## ADVERSARIAL CODE-REVIEW CORRECTIONS (2026-08-09) — magnitude, not structure

An adversarial review verified all five structural claims + the core inference against source, but found the design's MAGNITUDE reasoning wrong in three ways. Corrections, superseding the relevant text above:

**The inter-country same-good gap is HARD-CAPPED at ~1.9-3× — this is the decisive fact the design missed.** The per-country price is `world_price ÷ (0.5 + penetration)`, and for two countries the world price CANCELS exactly:
  `price_CHI / price_GBR = (0.5 + pen_GBR) / (0.5 + pen_CHI)`.
Penetration ∈ [0,1] (capped, se_GLOBALTRADE_split.txt:1999-2007) AND is shrunk by `× 0.4545` after the 22-TZ sum (1987-1990 — a factor the earlier design math OMITTED; note the code comment says "divide by 22" but the constant is 1/2.2, a latent mismatch worth flagging to whoever tunes here). So via the shipping path alone penetration ≤ ~0.4545 → divisor ∈ [0.5, ~0.95] → **max same-good CHI-vs-ROW gap ≈ 1.9×**; the absolute ceiling with the customs-union term is **3×**. Worked example (silk, yellow_sea = 90% of world stockpile): China pays ~38% less than Britain — real and perceptible, but that ~1.9× is the CEILING, not a tunable starting point.

**Consequences (correcting the "PENETRATION PATH TRACED" and "Historical anchors" sections above):**
1. The regional arbitrage the player feels for a same good is structurally bounded at ≈1.9-3×. NO amount of shipping-seed or `MODIFIER_tradezone_penetration_from_own_trade_power` amplification can exceed it (they only push penetration toward the cap). So "measure on boot, amplify if weak" is REPLACED BY: **the ceiling is ~1.9-3× by construction — decide NOW whether that ceiling is the intended feel. If the desired regional gap exceeds ~2-3×, penetration is the WRONG lever and seeding cannot fix it.**
2. The earlier "does the sqrt-compression wash the gap out? — measure on boot" worry is WRONG: the world price and its sqrt CANCEL in the inter-country ratio; the gap depends only on the two penetration terms. Strikes the sqrt-washout concern; reinforces "no #23 risk" (the gap never touches the sqrt).
3. The 10-20× luxury:staple figure from the price research is a CROSS-GOOD tier spread (tea vs rice), driven by each good's own local_price order/stockpile ratio — deliverable and NOT penetration-capped. It is a DIFFERENT AXIS from #50's regional same-good gap (Canton silk vs London silk), which IS penetration-capped at ≤~1.9×. Do not use the 10-20× number to set the regional-feel expectation — the regional mechanism cannot produce it. (The cross-good spread is arguably the more impactful and more achievable lever, and lives in local_price seeding, not penetration.)
4. Trade-agreement erosion is FIRST-ORDER, not residual: a Qing–European trade agreement raises the European side's China-TZ penetration (minimal_shipping ×0.75 + ADDITIVE_from_trade_agreements, SHIPPING_svalues.txt:2246-2247); against a ≤~1.9× ceiling that can erode a large fraction of an already-small gap.

**REVISED BOTTOM LINE:** structure is sound and #50 carries NO #23 risk (world price cancels). But the regional same-good divergence is hard-capped at ~1.9-3× and ALREADY EXISTS at whatever the current shipping seeds produce — so #50's real decision is a DESIGN judgment made now, not a boot measurement: is a ≤~1.9-3× Canton-vs-London gap the intended feel? If YES → #50 is essentially already satisfied (maybe a small shipping-seed nudge); if a BIGGER divergence is wanted → penetration cannot deliver it and the honest lever is the CROSS-GOOD local_price spread (tier realism: tea/silk dear everywhere, grain cheap everywhere), which is uncapped and lives in seeding — a different, arguably better feature than same-good regional arbitrage. Either way: no new blend machinery, no #23 risk, no base-value edit. This is a scope/intent decision for the user, not a build-now item.

---

## USER DIRECTIVE (2026-08-10) — the ~1.9-3× cap CAN be lifted, with great caution

The user has authorized lifting the penetration hard-cap **if necessary** to achieve a larger regional gap — BUT with an explicit caution flag: **"great caution is advised for both lifting AND the rest of the implementation because this touches deep trade logic."**

So the #50 decision tree is now:
1. **Default / low-risk:** if a ≤~1.9-3× Canton-vs-London gap is acceptable, #50 is essentially already satisfied by the existing penetration mechanism — at most a small shipping-seed nudge. PREFER this.
2. **If a larger same-good regional gap is genuinely wanted:** the cap-lift is now permitted. The levers are the penetration clamp (se_GLOBALTRADE_split.txt:1999-2007) and/or the `× 0.4545` post-sum shrink (1987-1990, the latent "divide by 22" vs 1/2.2 mismatch noted above). Lifting either widens the achievable gap.
   - *** DEEP-TRADE-LOGIC CAUTION (load-bearing): *** the penetration term feeds the per-country price divisor `world_price ÷ (0.5 + penetration)` which feeds EVERY country's unit price, trade income, and the price blend that the #23 sqrt stabilizes. Raising the penetration ceiling changes prices GLOBALLY, not just the CHI-vs-ROW gap. Before lifting: (a) trace every consumer of the penetration svalue + the 0.4545 constant; (b) confirm the #23 currency chain stays stable (the world price cancels in the inter-country RATIO, but the per-country ABSOLUTE price does move with penetration → the gbip blend + the sqrt could be perturbed); (c) verify on the #51 logs across MULTIPLE countries (the user's global-not-just-CHI rule). This is the single riskiest trade change in the batch — the adversarial review must scrutinize the cap-lift's blast radius specifically, and the verify boot must confirm no country's currency/price destabilized.
   - Resolve the latent "divide by 22" comment vs 1/2.2 constant mismatch FIRST (it's either a bug or a mislabel — know which before tuning on top of it).
3. **Alternative that sidesteps the cap entirely:** the CROSS-GOOD tier spread (#52) is uncapped and delivers a dear-tea/cheap-grain feel without touching the penetration math — often the better lever if the goal is "prices feel varied" rather than "the SAME good costs 5× more in London than Canton."

RECOMMENDATION: attempt the low-risk path (1) first; only lift the cap (2) if the user, seeing the measured ≤1.9-3× gap on a boot, judges it too small — and then treat the cap-lift as its own carefully-reviewed sub-change, not folded into a broader #50 pass.

---

## USER DECISION (2026-08-10): LIFT THE CAP + IMPLEMENT + LOG. Concrete build spec.

The user directed path (2): lift the penetration cap to widen the regional same-good gap, implement it, and log the result. This is the single riskiest trade change in the batch (penetration feeds EVERY country's price divisor). Build spec, grounded in source:

### The "divide by 22" mismatch — RESOLVED (do this first, per the design's own instruction)
The comment at se_GLOBALTRADE_split.txt:~1994 says "Divide by 22, the number of tradezones" but the constant is `multiply = 0.4545` (= 1/2.2). VERIFIED which is correct by tracing the sum: each of the 22 per-TZ terms = `<TZ>_percentage_of_global_stockpile × TZ_penetration` (se_GLOBALTRADE_split.txt:1811+); the stockpile PERCENTAGES across the 22 TZs sum to ~1 (they are shares of the global stockpile), and TZ_penetration ∈ [0,1], so the raw Σ is a stockpile-weighted AVERAGE of TZ_penetration, already bounded ~[0,1] — NOT ~22. => dividing by 22 would wrongly crush penetration ~10×; the `×0.4545` (÷2.2) is the DELIBERATE constant and the **"Divide by 22" COMMENT is the mislabel**. FIX: correct the comment to "× 0.4545 (≈ 1/2.2): a headroom shrink so penetration rarely saturates the [0,1] cap; NOT 1/22 — the per-TZ terms are stockpile-share-weighted, summing to ~1" — do NOT change the constant (changing it IS the lever, below, done deliberately).

### The cap-lift lever (widens the ≤~1.9× ceiling)
The inter-country same-good gap ceiling = (0.5 + pen_max) / 0.5. Today pen_max ≈ 0.4545 (the shrink) → ceiling ≈ 1.9×. Two knobs, lift the SHRINK (least-bad):
- **Raise the 0.4545 shrink toward 1.0** (se_GLOBALTRADE_split.txt:~1996): at 0.4545 → ceiling 1.9×; at ~0.9 → divisor ∈ [0.5,1.4] → ceiling ~2.8×; at 1.0 (no shrink, rely on the [0,1] cap) → ceiling 3.0×. This is the cleanest lever — it just lets penetration use more of its existing [0,1] range; the [0,1] cap still bounds it, so no unbounded runaway. [#50 ASSUMPTION best-guess: set the shrink to **0.9** — a perceptible ~2.8× Canton-vs-London ceiling without removing the cap entirely; boot-tune.]
- Do NOT raise the [0,1] `>1` cap itself (line ~2000) — that removes the structural bound and is the genuinely dangerous knob; keep penetration ∈ [0,1].

### CAUTION — global blast radius (the load-bearing risk)
Penetration feeds `country_unit_price = world_price ÷ (0.5 + penetration)` for EVERY country (se_GLOBALTRADE_split.txt:2035/2735), which feeds trade income + the price blend the #23 sqrt stabilizes. Raising the shrink lowers the ABSOLUTE price every high-penetration country pays (bigger divisor) — a GLOBAL deflationary nudge on high-access goods, not just the CHI-vs-ROW gap. So:
- The inter-country RATIO is safe (world price cancels — no #23 risk in the gap itself), BUT the per-country ABSOLUTE price moves → the gbip blend + downstream currency/reserve could shift. MUST verify #23 stability + multiple countries' prices on the boot (the global-not-just-CHI rule).
- LOG the effect: emit country_unit_price for a China good (silk/tea) for CHI vs GBR vs a low-access country, before/after, so the widened gap + the absolute-price shift are both measurable. The extended #52/#50 tzprobe already logs CHIPAID (CHI paid price + penetration per good) + REGIONGAP; ADD a GBR/low-access comparator if the tzprobe doesn't already cover non-CHI paid price (it's CHI-only — so #50 needs a small non-CHI paid-price + penetration emit, like #59's regime roster).

### Files
- se_GLOBALTRADE_split.txt: the 0.4545 → 0.9 shrink constant (the lever) + the comment fix. CRLF+BOM — preserve.
- a non-CHI paid-price/penetration log emit (new small effect or extend the tzprobe) for the GBR/low-access comparator.
- NO new blend machinery, NO #23 sqrt edit, NO trade_goods base edit.

### Verify (boot)
- CHI pays perceptibly less than GBR for a China good (silk/tea) — gap widened toward ~2.8× (was ~1.9×).
- #23 currency chain STABLE across CHI + GBR + a bimetallic power (no oscillation, no runaway); the absolute-price shift is modest, no country destabilized.
- The 0.4545→0.9 magnitude is best-guess (OVERNIGHT ASSUMPTIONS) — tune on the logged before/after.
## CAP-LIFT SPEC REVIEW (2026-08-10) — PROCEED-WITH-CORRECTIONS (folded)
The make-or-break (÷2.2 deliberate, "divide by 22" comment is the mislabel) CONFIRMED correct: the 22 <TZ>_percentage_of_global_stockpile values sum to exactly 1 (each = TZ_stock/global_stock, se_GLOBALTRADE_split.txt:1466-1477; global = Σ TZ :1439-1461), so the penetration sum is a convex combination ∈[0,1] — ÷22 would wrongly crush it ~10×; create_lookup.py:154 sweeps penetration over [0,1], corroborating. Gap-ceiling math confirmed (0.4545→1.9×, 0.7→2.4×, 0.9→2.8×). No direct #23-sqrt risk (penetration is downstream of gbip/sqrt — the shrink changes nothing the sqrt sees). THREE corrections, folded:

**C1 [must fix — blast radius incomplete] — the shrink feeds a SECOND consumer: order_size_modifier.** Line 2035 is NOT the price divisor — it's `order_size_modifier_$tradegood$ = penetration × global_stockpile` (the access-QUANTITY cap), which multiplies trade volume at wealth_owed :2465-2472. So raising the shrink does TWO things: (1) lowers country_unit_price (bigger 0.5+pen divisor — deflationary), AND (2) raises order_size_modifier → high-access countries ORDER MORE (capped at 1, :2067-2075, so bounded). Net trade-wealth = price↓ × quantity↑. => the VERIFY must watch TRADE INCOME / country WEALTH across CHI+GBR+bimetallic, not just unit prices. (The full consumer set of country_global_market_penetration: price divisor :2736, order_size_modifier :2035, the >1 cap :2009, read-only logging — no GUI/event consumer, so runtime blast = those two functional paths.)

**C2 [must fix — the comparator log is a generated-file trap] — route the GBR/low-access emit through the GENERATOR.** se_ECON_LOG_TZPROBE.txt is `# GENERATED — DO NOT HAND-EDIT`, and its chipaid probe (country_unit_price + penetration) is CHI-only (tag=CHI guards se_ECON_LOG.txt:551/569). To log a GBR/low-access comparator, EDIT tools/gen_econ_tzprobe.py + regenerate (add a small non-CHI paid-price/penetration emit), OR add the emit in a hand-editable se_ file — NOT a hand-edit of the generated .txt.

**C3 [magnitude] — start at shrink 0.7, NOT 0.9.** 0.7 → ~21% max price drop + ceiling 2.4× (clearly perceptible) at ~2/3 the price shock of 0.9 (~32% drop). Honors the user's "great caution" flag + the newly-surfaced compound (price+volume) blast radius. Tune toward 0.9 only after the boot confirms currency/wealth stability on the logged before/after. [#50 ASSUMPTION revised: shrink = 0.7 first pass.]

REVISED FILES: se_GLOBALTRADE_split.txt (0.4545→0.7 constant :1997 + comment fix :1993, CRLF+BOM preserve); tools/gen_econ_tzprobe.py + regenerated se_ECON_LOG_TZPROBE.txt (GBR/low-access paid-price + penetration comparator — C2). Verify watches price AND trade-wealth across regimes (C1). This spec is now review-clean; implement.

## IMPL-REVIEW (2026-08-10) — CLEAN, with one #23 watch-note carried to the verify boot
Impl reviewed CLEAN: constant isolated + correct (only the one 0.4545→0.7; comment fixed), gap math right (2.4× non-CU, 3× CU unchanged), blast radius bounded (both consumers — price divisor + order_size_modifier — saturate; penetration caps at 1), comparator probe well-formed (exists-guarded GBR/USA scope-hop, silk/tea, literal labels), integrity preserved.
**WATCH-NOTE for the verify boot (LOW, carried):** penetration does NOT feed the sqrt WITHIN a tick, but it DOES re-enter ACROSS quarters — penetration → order_size_modifier → order_size → next-quarter total_order_size → next-quarter local_price → next-quarter gbip=sqrt(...). So 0.4545→0.7 raises the (bounded, saturating — modifier caps at 1, sqrt compresses) gain of the cross-quarter order→price feedback loop the #23 sqrt sits inside, by up to ~1.54× where the modifier isn't saturated. Not a structural re-opening, but the #23 boot check MUST specifically confirm the SILVER oscillation stays damped (the tzprobe's silver GLOBAL-gbip bands + exact ticks cover it — the new GBR/USA comparator is silk/tea only and won't reveal a silver sawtooth). If silver oscillation returns → lower the shrink back toward 0.4545.
