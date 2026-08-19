# DIAGNOSIS v8 (data-derived, pre-review) — vegetables is genuinely SUPPLY-SHORT per province

## This supersedes the "supply refuted" claim (that rested on a WRONG proxy)
Earlier I computed a production proxy (1+lower_strata/20, then lower×0.075+mid×0.01 "base_resources")
that said veg OUT-produces grain. That proxy is REFUTED: it contradicts the log. `base_resources` is
not the trade-good output driver (num_goods_produced is engine-internal and pop/RGO-driven). The LOG
is ground truth.

## The proof (match code ↔ log, no boot)
1. DEMAND is symmetric grain vs veg: DEMAND_grain and DEMAND_vegetables svalues are byte-identical in
   structure (DEMAND_food_svalues_new.txt); DEMAND_food_grain / DEMAND_food_vegetables are identical;
   the industrial adds on veg (alcohol/pharma/processed_foods) are 0 in CHI (0 factories). The ONLY
   asymmetric term is the price-elasticity divide, and it favors GRAIN amplification (grain is the
   cheapest food, price 0-0.01, so its demand is amplified MORE than veg's, 0.01-0.1). So veg effective
   demand ≤ grain effective demand — never higher.
2. LOG: CHI per-good demand band is EQUAL (grain and veg both 1000-10000). GLOBAL stock band is grain
   10000-100000 (flat) vs vegetables 10000-100000 → 10-100 (draining). Per-zone (upper_yangtzi POST):
   grain stock 1000-10000 flat, veg 100-1000 → 0.
3. stock = for_sale = production − demand (per gov, floored 0; se_GLOBALTRADE_split.txt:761-813).
   With demand equal-or-grain-favored and grain stock ~10× veg stock, PRODUCTION_grain >> PRODUCTION_veg
   (~10×). So vegetables is SUPPLY-SHORT: it produces far less than grain, GLOBALLY and per-zone.
4. Yet veg has MORE provinces than grain (1224 vs 1024; upper_yangtzi veg 34 prov vs grain 21). So the
   shortfall is per-PROVINCE OUTPUT: a veg province produces ~1/10–1/16 the goods a grain province does.

## Why veg per-province output is so low (the mechanism + why the reseed failed)
num_goods_produced is engine-computed from the province's goods-producing pops (RGO workers; vanilla:
slaves, SLAVE_POPS_TO_PRODUCE_EXTRA=20, terrain-modified by local_goods_from_slaves). The #5 reseed
selected provinces by HIGHEST civilization_value (near-urban) and flipped grain/livestock→vegetables.
High-civ/urban provinces have few goods-producing (agricultural/slave) pops, so they produce little of
ANY RGO good. So the 805 reseeded veg provinces contribute almost no vegetable output — the reseed
added province COUNT but not OUTPUT. Grain sits on the high-output rural provinces. Net: veg total/
per-zone output stays far below grain, its per-zone for_sale surplus is thin, and the universal ±10%
food-demand ramp overtakes the thin surplus → for_sale→0 → zone stock→0 → collapse. Grain's fat
surplus is never overtaken. This is why the reseed (count) and the ×4 multiplier (which over-corrected
into a glut→boom-bust) both failed: neither put durable OUTPUT where the demand is.

## Predictions this diagnosis makes (falsifiable, checkable offline/next boot)
- The reseeded veg provinces have markedly lower goods-producing pops than grain provinces. (Check the
  producing-pop counts of high-civ reseeded provinces vs rural grain provinces.)
- Zones where veg was reseeded onto genuinely high-output rural provinces (or already had rural veg)
  survive (central_europe, yellow_sea); zones reseeded onto urban/low-output provinces collapse.

## Fix lever (for the design phase, AFTER review)
Put veg OUTPUT where the demand is: reseed veg onto HIGH-OUTPUT (rural, high-producing-pop) provinces
rather than high-civ urban ones (re-target the tool's selection from civilization_value-desc to
producing-pop/output-desc), OR raise veg per-province output at the source. NOT more urban provinces,
NOT a flat ×N multiplier (boom-bust). Confirm the producing-pop gap first.

## UPDATE — v8's MECHANISM (low-output urban reseed) is REFUTED; core contradiction stands
Checked producing pops: vegetables provinces avg lower_strata 21.9 (slaves 399); grain provinces avg
lower_strata 21.6 (slaves 382); veg avg civ 8.6 vs grain 6.7. So veg provinces have EQUAL producing
pops (NOT fewer) and veg has MORE provinces (1223 vs 1009). If num_goods_produced is pop-driven, veg
should produce >= grain — so "reseed onto low-pop provinces" is FALSE.

IRREDUCIBLE CONTRADICTION (all three are evidenced, can't all be true):
  (A) veg provinces: equal pops + more count  => veg production >= grain production (if pop-driven).
  (B) demand code symmetric grain vs veg (industrial 0 in CHI; elasticity favors grain) => veg demand <= grain demand.
  (C) log: grain stock ~10x veg stock, veg collapses => needs veg produce << grain OR veg demand >> grain.
(A)+(B) contradict (C). One premise is wrong:
  - num_goods_produced NOT simply pop-driven (terrain local_goods_from_slaves / a modifier differs veg vs grain), OR
  - a hidden veg-vs-grain DEMAND asymmetry in the ~800-line se_DEMAND chain (not the svalue level), OR
  - the TZP "stock" band is not production−demand (transformed/supply-scaled like "order" is).
RESOLUTION REQUIRES the exact engine num_goods_produced formula + the true stock-band semantics —
being determined by review-veg-v8. Do NOT ship any fix until this contradiction is resolved and the
resulting diagnosis passes review.

## STATUS: v8 mechanism refuted; core question OPEN pending review-veg-v8 (production formula + stock semantics).
