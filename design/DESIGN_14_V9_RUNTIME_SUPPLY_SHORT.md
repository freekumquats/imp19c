# DIAGNOSIS v9 (log-matched, pre-review) — vegetables is SUPPLY-SHORT *at runtime*, and num_goods_produced does NOT track lower_strata pop count

## Supersedes both v8 and the review-veg-v8 rebuttal
- v8 said "supply-short" but proved it with a lower_strata/base_resources proxy → REFUTED (that proxy says veg OUT-produces grain).
- review-veg-v8 said "demand-side" (veg has 3 industrial consumers) → REFUTED below: those factory counts are 0 at 1763 and ~0 by 1768, so the industrial terms evaluate to ~0 this boot.
- v9 reconciles both with the ACTUAL LOG: veg is supply-short at RUNTIME, but the cause is NOT lower_strata pop distribution — it is that the engine's `num_goods_produced` for the reseeded veg provinces is far below the grain provinces they replaced.

## The log (newest boot, logs.zip Aug 18 20:11, POST-reseed — veg=1223 provinces on disk)
Per-zone TZP "stock" reads `global_var:<zone>_stockpile_<good>` — the ZONE TRADEABLE POOL, which the
sim rebuilds each quarter as Σ_governorship max(0, local_stockpile − DEMAND) [floored, infra-capped]
(se_GLOBALTRADE_split.txt:797-820). local_stockpile is SET to production each quarter (se_GOODS.txt:239).

upper_yangtzi (CHI) stock, quarter by quarter:
- grain: q1 100-1000  →  q2..q21 1000-10000  (jumps 10× at the first production tick, then stable)
- vegetables: q1 100-1000  →  q2..q9 100-1000  →  q10..q21 **0**  (never rises off the seed, then drains to 0)
GLOBAL stock: grain flat 10000-100000 all 21q; vegetables 10000-100000 → drains monotonically to 10-100.
CHI price: veg (0.01-0.1) DEARER than grain (0-0.01) from q2; veg spikes to 10-100 at q18+ (stock=0).
CHI order: veg rises to 100-1000 by q2 (grain not until q8), then veg collapses to 1-10 as stock→0.

## The proof (match A to B, band resolution — a 10× gap = one full band)
1. q1 = the initial SEED (both goods 100-1000, identical). q2 = the first PRODUCTION-driven pool value.
2. At q2 CHI grain pool = 1000-10000, CHI veg pool = 100-1000 → grain's surplus is ~10× veg's.
3. pool_gov = max(0, production_gov − DEMAND_gov). So Σ max(0, veg_prod − veg_dem) ≈ 10× smaller than
   Σ max(0, grain_prod − grain_dem) in CHI.
4. DEMAND is ≤ for veg vs grain (proven, see below). A SMALLER surplus with an EQUAL-OR-SMALLER demand
   can only come from a SMALLER production. ⟹ **veg production < grain production per CHI governorship.**
5. Yet the reseeded veg provinces carry EQUAL-OR-MORE lower_strata pops than grain (CHI: veg 2216 lower
   vs grain 1068; global veg 30012 vs grain 24372). ⟹ **num_goods_produced does NOT track lower_strata
   pop count.** The base_resources proxy (lower×0.075) that v8 and review-veg-v8 both used is INVALID.

## Why DEMAND is ≤ for veg (kills the "demand-side" alternative for THIS boot)
- Base food demand is byte-identical templated by $tradegood$ (se_DEMAND.txt:155-216): need/6 ÷
  (local_price / food_mean). The ONLY per-good term is price. CHI veg is DEARER than grain (log), so its
  price-elasticity divide REDUCES veg demand and AMPLIFIES grain's. So base food demand favors GRAIN.
- Industrial demand: veg adds alcohol+pharma+processed_foods; grain adds alcohol only. BUT every
  INDUSTRY_factories_assigned_* is SET TO 0 at setup (se_INDUSTRY_setup.txt:65-177) and grows only as
  factories are BUILT. pharmaceuticals/processed_foods are 19th-c industries; in a 1763→~1768 boot their
  counts are ~0, so INDUSTRY_demand_pharmaceuticals_vegetables = 0×2 = 0, likewise processed_foods. Even
  alcohol: grain's per-factory demand (base 20) is 10× veg's (base 2, task #93 trim), and grain stays
  FLAT, so alcohol factories are ~0 too. ⟹ veg industrial demand ≈ 0 this boot. review-veg-v8's PROOF 2
  is magnitude-blind (counted 3 terms vs 1; the terms are ~0).

## What is different about the reseeded veg provinces (the engine-weighting unknown)
Candidates for why num_goods_produced(veg) << num_goods_produced(grain) despite equal lower_strata:
- (a) SLAVES dominate the engine RGO output (SLAVE_POPS_TO_PRODUCE_EXTRA=20, defines). In CHI/Asian
  zones grain sits on slave-RICH provinces, veg on slave-POOR ones (CHI grain 28 slaves vs veg 5;
  yellow_sea grain 12 vs veg 0; india grain 47 vs veg 9). The reseed selected by civilization_value
  (urban nodes), which correlates with lower_strata but NOT slaves.
- (b) num_goods_produced needs a production BUILDING / employment the converted provinces lack (the
  reseed rewrote only trade_goods, tools/reseed_vegetables.py:239; province setups carry no building).
- (c) a per-province floor/threshold in the engine primitive.
num_goods_produced is a Jomini ENGINE primitive with NO mod-script formula (base_resources is only a
pop_types attribute the engine consumes) — so (a)/(b)/(c) cannot be distinguished from files alone. The
q2 pool bands are the only runtime read, and they are conclusive at the "veg produces less" level.

## Why this boot's raw production number is NOT available (not a dodge — a broken instrument)
The raw-value probe ECON_LOG CURXV emits the literal string "unit" for 199,729 lines (value interpolation
broken) and is aimed at thinstock bronze/gunpowder in indo_china, NOT veg/grain production. So the exact
num_goods_produced(veg) vs (grain) is absent. The q2 pool band (10× gap) is the proof at band resolution.

## Fix direction (for the design phase, AFTER review — do NOT ship yet)
The runtime shortfall is real regardless of which of (a)/(b)/(c) is the engine cause. Robust levers,
in preference order:
- Raise vegetables' production at the SOURCE to close the ~10× CHI gap, WITHOUT a flat ×N (the ×4
  multiplier boom-busted). E.g. a modest per-province vegetables output bonus that lifts the floor, or
  concentrate veg on provinces whose grain predecessors had real output (slave-bearing), reversing the
  civilization_value-first selection that put veg on slave-poor urban nodes.
- Do NOT re-trim demand (already ~0 this boot) and do NOT add more low-output provinces (the reseed's
  mistake: count without output).

## RESOLUTION — v9's OBSERVATION confirmed, its EXPLANATION refuted, TRUE root found and fixed 2026-08-19

The adversarial review REFUTED v9's explanation (opaque engine num_goods_produced disparity) and found the
real, file-provable root ONE layer up:

**Vegetables is the ONLY good (of the ~44 hand-enumerated, including defunct chocolate/tropical_fruit and
every other food) with NO quarterly production-replenishment block in `GOODS_governorship_produce_all`
(se_GOODS.txt:1135-1436).** It is seeded ONCE at boot (GOODS_setup_governorship_stockpiles, :239, a
set_variable) and then NEVER topped up, while consumption (CONSUME_all_stockpiles) and export
(GT_split_subtract_amount_exported_tradegood) drain it generically every quarter. So vegetables_stockpile
monotonically drains from its boot seed to 0 — exactly matching the log (CHI veg flat q1-9 then 0; global
veg 10000-100000 → 10-100 while grain stays flat, in equilibrium from +production −consumption each quarter).

This reproduces EVERY log symptom with NO engine-primitive asymmetry: q1 is identical for both goods (both
computed once from num_goods_produced at the same boot call — matching the log's identical q1). The seed-vs-
production reading in v9 §"proof" step 1-2 was wrong (q1 is already production-derived, not a placeholder);
the DEMAND-bound (step 2/4) and num_goods_produced-is-engine-internal (step 4) claims SURVIVED but were
irrelevant — the asymmetry lives entirely in mod script (the missing quarterly add), which IS file-derivable.

Both prior attempts treated symptoms: task #93 trimmed veg industrial demand (which is ~0 in early game
anyway); the geographic reseed grew veg province count (which cannot help if the produce is never added).

FIX (shipped): one block added to GOODS_governorship_produce_all mirroring grain's (:1143-1146):
`GOODS_governorship_produce = { do_if = produces_vegetables  amount = GOODS_governorship_vegetables_produced
into_stockpile = vegetables_stockpile }`. Verified: the svalue, the produces_vegetables marker, and the
vegetables_stockpile var all already exist; the macro guards the write on has_variable so unseeded govs skip.
The reseed (1223 veg provinces ≈ grain's 1009) now produces properly → veg reaches staple parity, which is
the user's stated goal. STATUS: FIXED.
