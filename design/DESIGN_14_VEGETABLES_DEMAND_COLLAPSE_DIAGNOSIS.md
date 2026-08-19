# DIAGNOSIS — task #14: vegetables trade-zone collapse is an UNDAMPED demand-elasticity bug, not seeding

**Status:** DIAGNOSIS (pre-adversarial-review). Independently traced in source this session.
A parallel deep-trace agent (diag-veg-collapse) is confirming the cross-quarter feedback and
pinning the exact Div/0 divide line; its findings merge into §5/§6 before this goes to review.

## Symptom (live -debug_mode boot, 2026-08-18 11:50)
- `vegetables` (a FOOD good) collapses: all 13 producing zones' zone stockpile hits 0 by
  ~1.5 in-game years (after quarter ~5) and never recovers through quarter 9.
- **ORDER (demand/attempted purchases) also drops to 0 in all 22 zones** — not just stock.
- CHI national vegetables PRODUCTION stays stable. A forensic seed-probe shows vegetables
  seed/produce healthy (REAL 10,968-11,098 / 11,098 — same ratio as every other good).
- Separately: Div/0 attributed to `oa_wealth_changes.txt:445/462/479/535` — the call sites of
  `GT_split_do_global_trade_split = { type = luxury / luxury_2 / 3 / 6 }`. The `food` pass
  (type=food, :421) is NOT in the Div/0 list.

## CORRECTION (2026-08-18, after adversarial review) — the "ORDER→0" inference is REFUTED
My first draft argued: "order→0 proves the collapse is demand-side, not supply, so the reseed
(task #5) is the wrong cause." **That inference is WRONG, and this correction supersedes it.**
- The probe's logged `order` = `global_var:$tz$_total_order_size_$good$`
  (`se_ECON_LOG_TZPROBE.txt:94-96`). That variable is **supply-scaled AFTER it is summed**:
  `GT_split_modify_fulfillable_order_sizes` (`se_GLOBALTRADE_split.txt:3390-3486`, verified this
  session) multiplies EVERY zone's `total_order_size_$good$` by
  `global_supply_as_percentage_of_order_$good$` whenever supply < 1, and that percentage =
  `global_stockpile / global_order_total` (`:3159-3176`). So when global vegetables stockpile
  collapses, the logged `order` is scaled to 0 across ALL zones **mechanically, with demand fully
  intact.** `order→0` therefore does NOT adjudicate supply-vs-demand — it is a downstream
  consequence of the stock collapse.
- **Internal inconsistency that settles it:** if demand had truly collapsed, production would
  exceed the (collapsed) demand and the stockpile SURPLUS would GROW — yet the boot shows
  stock→0. A demand collapse cannot produce stock→0. A SUPPLY shortfall produces both stock→0
  (no surplus) and logged-order→0 (via the fulfilment scaling). So the PRIMARY driver is a
  supply shortfall, consistent with H-RESEED.

## Corrected verdict — SUPPLY is primary; the demand-loop bugs are a real SECONDARY amplifier
- **H-RESEED (task #5) is a valid, primary supply-side fix and is NOT superseded.** More
  vegetable provinces → higher zone stockpile → lower price (`price = (order/stock)·0.6/num_food`,
  `se_GLOBALTRADE_split.txt:6244-6252`) → smaller elasticity divisor AND a higher supply% so the
  fulfilment scaling stops zeroing the logged order. Supply and the demand loop are COUPLED.
- **The demand-loop defects below are real and confirmed, but secondary** — they aggravate the
  price spike and add error spam; they are not the root of stock→0. They ship as complementary
  hardening under task #14, alongside the #5 reseed.

The remaining sections (undamped elasticity, dead clamp, div/0) survive the review as CONFIRMED
code defects — only their CAUSAL WEIGHT is downgraded from "the cause" to "an amplifier."

## Root cause (traced in source)

### 1. Vegetables demand is NOT vegetables-specific at its base
`se_DEMAND.txt`:
- `DEMAND_set_demand_from_food_all` (:36) sets
  `var_DEMAND_unfulfilled_food_need_governorship = DEMAND_unfulfilled_food_need_governorship`
  (:40-43) — the WHOLE governorship's residual food need — then calls
  `DEMAND_set_demand_from_food` once per food good (:68-85), vegetables at :77-79.
- `DEMAND_set_demand_from_food` (:114) sets each good's base demand to that same
  whole-governorship unfulfilled need (:155-158) then `divide = DEMAND_num_food_goods` (:175,
  = 6 baseline). So vegetables' BASE demand = `unfulfilled_food_need / 6`, re-seeded EVERY tick.
- CONSEQUENCE: vegetables' base demand cannot latch to 0 from thin veg production — it tracks
  the governorship's total food need, which is positive as long as pops are hungry. **Thin veg
  seeding does not starve veg demand.** H-RESEED's premise is structurally false here.

### 2. The price-elasticity divide is UNBOUNDED
`se_DEMAND.txt:179-218`:
- `l_DEMAND_<good>_price_diff_to_food_mean = local_price_<good> / PRICE_food_mean_normalised`
  (:179-194) — this good's price relative to the food-basket mean.
- `DEMAND_food_<good> divide = l_DEMAND_<good>_price_diff_to_food_mean` (:213-216) — the
  elasticity brake: an expensive good's demand is divided down.
- There is NO cap on the divisor. When vegetables is even modestly under-produced in a zone its
  price rises above the food mean, so the divisor > 1 and demand is cut. With `price = order /
  stock` (`GT_set_tradegood_price`), a shrinking for-sale surplus spikes price, which cuts
  demand further next tick — a feedback with no bound.

### 3. The ±10% damping clamp that WOULD bound it is dead — and it died by ACCIDENT
`se_DEMAND.txt:128-149` still COMPUTES `previous_tick_food_demand_<good>_110_percent` /
`_90_percent`, but the code that APPLIES them (:220-263) is entirely commented out.
- **Git blame (`dd43d5419`, Sobisonator, 2023-08-23, "WiP dynamic food demand"):** the working
  clamp was `FUNC_clamp_variable{ variable=DEMAND_food_<good> max=..._110_percent min=..._90_percent }`.
  The commit message states it was removed because it "was failing to compare a variable to 0
  (try making this 0.0 or an svalue?)" — i.e. the **RHS-variable-comparison bug**
  (`imp19c-rhs-comparison-operator-rule`: a var on a comparison RHS is illegal). It was replaced
  by commented-out inline code that was never finished.
- So the ±10% damping was lost to a fixable scripting error in a 2023 WiP, NOT to a design
  decision. Food demand has run UNDAMPED ever since. The author's aside ("the order size
  effectively does this job by subtracting the local amount available before making an order")
  addresses only the UPPER bound (over-demand); it does nothing for the LOWER bound, which is
  exactly the collapse direction here.

### 4. Net mechanism
Undamped elasticity divide (2) with the intended damping missing (3), over a base that is not
veg-specific (1): once a zone's vegetables price sits above the food mean, demand is divided
down hard, `order = demand − local stockpile` falls to ~0, and with no floor the market reads
DEAD (stock=0 AND order=0) even though pops' real food need is met by grain/livestock. This is
a SIM artifact of a missing damping bound, not a true vegetable shortage.

## ============================================================================
## INVESTIGATION LOG — post-fix boot (Aug 18 20:11), task #20. READ THIS FIRST to avoid circling.
## ============================================================================
## Rule (user): a diagnosis must PASS adversarial review before any design/fix. If refuted,
## investigate deeper, produce a NEW diagnosis, review again. Iterate until CLEAN.

### SETTLED FACTS (verified in source + log — do NOT re-litigate)
- **Only vegetables collapses among raw food staples.** Boot Aug 18 20:11, TZP BAND GLOBAL stock:
  vegetables 10000-100000 → declines → 10-100 (per-zone → 0 in 20/23 zones). grain, livestock,
  fish, temperate_fruit all FLAT at 10000-100000. processed_foods = 0 (manufactured, collapsed).
- **Stock is a per-quarter FLOW, not a reservoir.** local `vegetables_stockpile` is SET to that
  quarter's production (se_GOODS.txt:237-247); zone stock is reset to 0 then rebuilt from for_sale
  each quarter (se_GLOBALTRADE_split.txt:169-175, 1029-1035). for_sale = local_stockpile − DEMAND
  (se_GLOBALTRADE_split.txt:782-791), floored 0. NO cross-quarter accumulator.
- **NOT production count:** veg (1224 provinces) drains; fish (660) is stable. So more provinces ≠ safe.
- **Per-factory industrial base_demand is SMALL:** alcohol/pharma/processed_foods _vegetables = 2 each;
  grain alcohol = 20; fish processed_foods = 4.
- **Supply-side fixes proven insufficient:** the ×4 multiplier (reverted) and the 419→1224 reseed
  BOTH failed to stop the collapse; more supply → bigger glut → still drains (boom-bust).
- **Div/0 Site A (GT_set_tradegood_price) is FIXED** (0 occurrences post-fix). Separate: 3828×
  "failed to read divide" at GT_split_update_wealth_owed_for_tradegoods:34 (empty total_order_size) = task #21.

### DIAGNOSIS ATTEMPTS
- **v1 — stockpile-share redistribution runaway** (DEMAND_subtract_excess_food_demand_from_tradegood
  concentrates residual food demand on the thinnest-stock food → self-reinforcing drain).
  **REFUTED** (review-veg20): requires a cross-quarter reservoir; everything is a per-quarter flow,
  so no runaway is possible. The redistribution is within-quarter, food-component-only, per-governorship.
  DEAD END — do not revisit.
- **v2 — unclamped 3-chain industrial-demand balance** (DEMAND_vegetables = clamped food + alcohol +
  pharma + processed_foods, each factory_count×2, no ±10% clamp; that pull exceeds veg output where
  factories are; veg is the only food feeding 3 chains). **UNDER REVIEW (review-veg20b).**
  STRONGEST COUNTER-EVIDENCE to resolve: a prior pass cut those 3 constants 5/6/6→2 (~65%) and it did
  NOT move the collapse (DESIGN_93_FOLLOWUP); AND at 1763 (~9 quarters, pre-industrial) there may be
  too few factories for industrial demand to dominate. If either holds, v2 is REFUTED.

- **v2 REFUTED (review-veg20b, VERIFIED):** factory counts at 1763 = 4 alcohol (all non-Chinese,
  amount=1), 0 pharmaceuticals, 0 processed_foods worldwide (oa_economy_setup.txt:296-351; no other
  live seeder). So all 3 industrial adds = 0 in every Chinese governorship → DEMAND_vegetables ==
  DEMAND_food_vegetables there. Industrial pull is the ZERO term, not the dominant one. Also explains
  why the prior 65% constant cut did nothing (terms already 0). DEAD END.
- **v3 — price-elasticity amplifies the cheapest food's demand into collapse** (DEMAND_food /=
  price_diff_to_food_mean; reseed makes veg cheap → demand amplified → drains). **REFUTED by price
  data (boot Aug 18 20:11):** GRAIN is the CHEAPEST food almost everywhere (price 0-0.01, extreme
  glut) yet is ROCK-STABLE; FISH is EXPENSIVE (10-100 in upper_yangtzi) yet STABLE. If cheapness drove
  demand into collapse, grain would go first. Veg's price SPIKE is a symptom of draining, not the
  cause. DEAD END.

### CROSS-FOOD MEASUREMENTS (boot Aug 18 20:11) — the constraints any v4 must satisfy
- CHI demand: grain/livestock/fish/temperate/vegetables ALL flat at band 1000-10000 (equal split,
  confirmed — DEMAND_num_food_goods=6). GLOBAL stock: grain/livestock/fish/temperate FLAT at
  10000-100000; vegetables 10000-100000 → 10-100 (only veg drains).
- Prices (per-zone): grain ~0-0.01 (massive glut), livestock cheap, fish higher/tighter, veg starts
  cheap then spikes. => grain TOTAL output >>> its demand; veg output starts as a glut then is overtaken.
- Production formula veg == fish (byte-identical, GOODS_svalues.txt:1963-1974 vs 2002-2013);
  no veg multiplier (the ×4 was REVERTED, 9085ba9c1); num_goods_produced is province-intrinsic.

### v4 (SURVIVING hypothesis by ELIMINATION — NOT yet confirmed, do NOT design on it yet)
Demand target = unfulfilled_food_need/6, EQUAL per food, population-driven. Only veg drains =>
veg TOTAL production < that target, while grain/fish TOTAL production exceeds it. Veg has 1224
provinces (> stable fish's 660) yet grain is ~10x more glutted (price 0-0.01 vs veg 0.01-0.1) on
only 1.4x the provinces => grain per-province OUTPUT >> veg per-province output. So the collapse is a
per-province YIELD/OUTPUT shortfall, not province count — the reseed added COUNT but not OUTPUT. The
universal ±10% demand ramp then overtakes veg's thinner surplus while grain's huge surplus is never
overtaken. LEVER THIS IMPLIES: per-province veg OUTPUT (a production multiplier — the reverted ×4),
NOT more provinces. TENSION: user rejected the ×4 as boom-bust; a MODERATE output lift (not ×4) may
be the answer, or the yield gap has a fixable cause.
- **v4 is NOT confirmed** — it rests on elimination + coarse log-magnitude bands that cannot
  distinguish "production shortfall" from "demand excess" numerically, and script cannot reveal
  per-province num_goods_produced. BEFORE proposing v4 as the diagnosis, INSTRUMENT: add a
  -debug_mode probe logging per-zone RAW numbers for GOODS_governorship_vegetables_produced vs
  DEMAND_vegetables (and grain/fish for comparison). Next boot proves/quantifies the gap. THEN review, THEN fix.

### PIVOTAL FINDING (offline production computation) — SUPPLY IS REFUTED AS THE CAUSE
Computed each food good's production-vs-demand balance from setup pops (production proxy
1+lower_strata/20 per province, per SLAVE_POPS_TO_PRODUCE_EXTRA=20; demand = 1/6 of total pop):
  vegetables 1.71 (HIGHEST surplus) — COLLAPSES;  livestock 1.52 stable;  grain 1.41 stable;
  fish 0.70 (DEFICIT) STABLE;  temperate_fruit 0.67 (DEFICIT) STABLE.
=> The good with the MOST supply collapses; goods with supply DEFICITS are stable. Supply is
NOT the driver — this refutes count/yield/reseed/×4 (all supply levers). CAVEAT: the proxy is
crude (contradicts observed prices — grain is cheaper in-game than veg despite lower proxy-surplus),
because num_goods_produced is ENGINE-computed (pop-driven) and not reproducible from static files.
The ORDINAL conclusion survives regardless: veg is not the supply-short food; fish is, and fish is fine.
Also: debug.log carries only BANDS + REAL/PRESENT flags, NOT raw numbers, so faithful per-good
production/effective-demand figures would require a numeric probe.

### v4/v5 (per-province yield / per-capita distribution shortfall) — REFUTED
Same pivotal finding kills these: veg is not supply/yield-short (highest proxy-surplus; more
provinces than stable fish). DEAD END.

### v6 (CURRENT candidate — DEMAND-side, code-grounded — UNDER adversarial review)
Price-elasticity amplification of a cheap, non-ubiquitously-distributed food. The food-demand
elasticity divide DEMAND_food_<g> /= (local_price_<g> / PRICE_food_mean_normalised)
(se_DEMAND.txt:213-215) amplifies demand for any food priced BELOW the basket mean. The mean is
inflated by EXPENSIVE fish (log: fish 10-100 vs grain/livestock/veg ~0.01-0.1), so cheap foods get
amplified demand and fish gets reduced. Grain/livestock survive because they're produced UBIQUITOUSLY
(~every governorship ∝ population) so amplified demand is met locally; vegetables — well-supplied
GLOBALLY but NOT ubiquitously co-located with population — can't meet its amplified demand in
high-pop zones → for_sale→0 → drains. Fish survives by being expensive (demand reduced). Explains
why supply fixes fail + boom-bust (constraint = amplified demand vs LOCAL distribution, not global
supply). Candidate fixes: bound/cap price_diff in the divide; or fix the fish-price distortion of
the food mean; or distribute veg ∝ population. STATUS: under adversarial review (review-veg-v6).
OPEN sub-question the review must probe: why veg drains but livestock (also cheap+amplified, similar
global supply) is stable — is livestock genuinely more ubiquitous across governorships than veg?

### v6 REFUTED — food mean is MAD-filtered (outlier-resistant)
PRICE_set_food_mean_normalised_price (se_PRICE.txt:487+) computes each food's deviation from the raw
mean, a MAD, and averages ONLY goods within the MAD (EXCLUDES outliers). So expensive fish is
filtered OUT, NOT inflating the mean; cheap foods sit near the mean → no differential veg
amplification; the elasticity is self-correcting (a spiking good is excluded → its demand crushed).
v6's premise is false. DEAD END.

### v7 REFUTED — per-zone supply balance does NOT predict collapse
Computed per-zone veg producing-pop share ×6 (self-sufficiency index) vs actual post-reseed outcome:
yellow_sea SURVIVES at 1.49 (highest) while upper_yangtzi COLLAPSES at 1.44; central_europe SURVIVES
at 0.69 while west_mediterranean COLLAPSES at 0.39. Overlapping ranges, no separation. NO supply or
distribution metric (global or per-zone) predicts the collapse. (Same non-monotonicity DESIGN_93's
review hit.) DEAD END for all supply/distribution framings.

### EXHAUSTION CONCLUSION (2026-08-19) — offline analysis cannot settle this; instrument it
Refuted: v1 (flow), v2 (0 factories), v3/v6 (MAD-filtered mean), v4/v5/v7 (supply/yield/distribution).
The decisive quantity — REAL per-good, per-zone PRODUCTION — is NOT faithfully computable offline:
the pop proxy (1+lower_strata/20) contradicts BOTH observed prices (grain cheaper than veg despite
lower proxy-surplus) AND the collapse pattern, because num_goods_produced is engine-computed from
pop TYPE (which stratum works the RGO), a formula not in the mod files. debug.log has only BANDS +
REAL/PRESENT flags, no raw numbers. => A PROVEN diagnosis requires a NUMERIC probe. NEXT STEP: add a
-debug_mode probe emitting RAW GOODS_governorship_<food>_produced, DEMAND_<food>, DEMAND_food_<food>,
local_price, PRICE_food_mean_normalised per food good (CHI, per quarter). The boot then shows whether
veg real production is short (mis-targeted reseed onto high-civ/urban low-RGO provinces) or effective
demand is anomalous. THEN diagnose from data, THEN review, THEN fix. Building the probe now.

### v6 REFUTED by independent adversarial review (review-veg-v6) — CONVERGED with my analysis
Confirmed: (a) food mean is MAD-filtered → fish is TRIMMED, not inflating it (v6 premise false);
(b) vegetables is MORE ubiquitous than grain (1224 vs 1024 provinces) — v6's "veg less widespread"
is backwards; (c) grain is cheapest → gets the LARGEST elasticity amplification yet is stable, so
the elasticity divide cannot be a veg-specific driver; (d) in the log, veg is as cheap/abundant as
grain in high-pop China zones. The reviewer independently reached the SAME remaining candidate:
per-governorship veg PRODUCTION (num_goods_produced × ag-prod over veg provinces) falling below veg's
~1/6 food-demand share in specific governorships, hitting the for_sale = stockpile − DEMAND clamp
(se_GLOBALTRADE_split.txt:761-813, CLAMPED to 0 when DEMAND ≥ stockpile). It also independently
recommends a NUMERIC per-governorship stockpile-vs-DEMAND dump before any fix — no such value exists
in the log (only bands + REAL/PRESENT flags).

### DECISION: probe the for_sale clamp (validated by two independent analyses)
Added a -debug_mode CHI probe in GT_split_declare_sell_amount: per governorship, for vegetables and
grain, log SURPLUS (stockpile > DEMAND) vs CLAMPED0 (stockpile ≤ DEMAND → for_sale 0 → zone drains).
Boot then shows whether veg is CLAMPED0 in far more CHI governorships than grain (⇒ per-governorship
production shortfall = the mechanism) or about the same (⇒ NOT supply-distribution; look elsewhere).
Cheap flag-logging (no while-loop), engine-silent outside -debug_mode. THEN diagnose from the counts,
THEN review, THEN fix. NOTE: veg is more ubiquitous than grain, so a clean "veg CLAMPED0 >> grain"
result is NOT guaranteed — if they're similar, the mechanism is still unknown and needs another angle.

### IF v2 IS REFUTED — deeper questions to answer BEFORE proposing v3 (don't guess)
- Measure the actual DEMAND_vegetables split from the boot: food component vs Σ industrial. How many
  alcohol/pharma/processed_foods factories exist in 1763? (If few → industrial is negligible → the
  drain is the FOOD component or yield.)
- Does for_sale subtract DEMAND_vegetables (food+industrial) or DEMAND_food_vegetables (food only)?
  (se_GLOBALTRADE_split.txt:782-791.) Decides whether industrial demand even reaches the balance.
- Per-province YIELD: is a vegetable province's num_goods_produced lower than a fish/grain province's?
  (Formulas are identical — GOODS_svalues.txt:1963-1974 vs 2002-2013 — but per-province throughput
  unverified.) If veg output per province is lower, 1224 veg may be < 660 fish in real output.
- Why the glut→gradual-decline shape (starts 10000-100000, declines over ~7q)? A flow that's demand-
  bound would hit equilibrium fast; the gradual glide implies demand RISING over quarters — the ±10%
  food-demand clamp (DEMAND_food_svalues_new.txt:240-252) converging toward a target that exceeds
  output. Whose target rises, and why only veg's above output?
- Is vegetables' price_diff_to_food_mean systematically < 1 (cheap glut) → its FOOD demand amplified
  vs other foods (se_DEMAND.txt:213-215 divides food demand by price_diff)?

## Verdict (CORRECTED): supply-primary + demand-loop amplifier — BOTH #5 and #14 ship.
- Task #5 (province reseed) is the PRIMARY fix and stays live. The ×4 revert already shipped
  (9085ba9c1) and stays.
- Task #14 ships the two confirmed demand-loop defects below as complementary hardening.
- **This corrected verdict incorporates the 2026-08-18 adversarial review, which was accepted
  after independently re-verifying its decisive claim (`GT_split_modify_fulfillable_order_sizes`
  supply-scaling) in source.**

## Div/0 — RESOLVED to the real site (my earlier :3340 guess was WRONG)
The error.log stack traces (authoritative, boot 2026-08-18 11:47, post-#107) name TWO innermost
frames — NEITHER is :3340 (my guess) nor the luxury-demand site (the deep-trace agent's guess):
- **SITE A (fixed): `GT_set_tradegood_price` price divide** (se_GLOBALTRADE_split.txt ~6252),
  269× at setup (oa_economy_setup:2493) + runtime. The `#107` guard used an `if/limit` AROUND the
  divide, NESTED inside the scriptvalue `value = { }` block — and that does NOT reliably skip the
  divide in this engine (proven: it still fires post-#107). The codebase's working idiom floors the
  DIVISOR directly (EDU_svalues.txt:607-610, ADMIN/AI). **FIX APPLIED:** `divide = { value =
  global_var:$tradezone$_stockpile_$tradegood$  min = 1 }`. min=1 (not 0.0001) reproduces #107's
  "price = raw order size at stockpile 0" default and damps the #79 thin-stock explosion.
- **SITE B (likely a DOWNSTREAM CASCADE of Site A — no separate fix): `GT_split_update_wealth_owed_
  for_tradegoods`**, 257× Div/0 (line 12) + 3,828× "failed to read divide for set_variable"
  (line 34, the bigger class). The deep-trace agent read this macro in full and found ALL its own
  divides properly guarded (effect-level if/limit or 0.5-floor) — the real cause is an UPSTREAM
  EMPTY operand (a scriptvalue that Div/0s yields EMPTY, per se_ECON_LOG.txt:1412), fed into
  `total_order_size` / `TZ_penetration`. **Hypothesis (boot-testable): Site A is the root.** Site A's
  Div/0 makes `local_price` EMPTY; `local_price` feeds the demand elasticity divide (se_DEMAND.txt:
  179-216) → EMPTY `DEMAND_food` → EMPTY `order_size` → EMPTY `total_order_size` → Site B's readers
  "fail to read divide". So the Site A floor should CLEAR Site B's 4,085 combined errors too.
  **CONFIRM ON BOOT:** if Site B's line-12/line-34 classes survive after the Site A fix, trace the
  upstream `total_order_size`/`TZ_penetration` setter directly (next round) — do NOT pre-guess it.

## (superseded) earlier div/0 note — kept for the record
The below (:3340) was my first guess; the error.log does not implicate it. Left for the trail.
- The price divide in `GT_set_tradegood_price` (~:6237) is already `#107`-guarded
  (`has_global_variable` + `> 0`), and the global-stockpile percentage divides
  (`GT_split_create_global_stockpile`, :1520-1553+) are guarded (`stockpile>0 && global>0`).
- **PINNED (traced this session): the unguarded divide is `se_GLOBALTRADE_split.txt:3340`**, in
  `GT_split_get_order_as_percentage_of_TZ_total_tradegood`:
  ```
  set_variable = { name = order_as_percentage_of_TZ_total_$tradegood$  value = var:order_size_$tradegood$ }
  change_variable = { name = order_as_percentage_of_TZ_total_$tradegood$
      divide = global_var:$tradezone$_total_order_size_$tradegood$ }   # <-- NO guard
  ```
  Every sibling divide by `total_order_size` / `global_order_total` / `global_supply_as_percentage`
  IS guarded — 2558 (`has_global_variable` + `> 0`), 3174 (`trigger_if` + `> 0`), 3376/3996
  (`> 1`). Only :3340 divides unconditionally. When a good's `$tradezone$_total_order_size_$tradegood$`
  is 0 (a luxury nobody orders in that zone), it div/0s. Food is exempt because food goods always
  carry positive total order in every zone.
- Fix = mirror the accepted pattern: guard the :3340 divide with `has_global_variable` +
  `> 0`, skipping it (leaving `order_as_percentage_of_TZ_total_$tradegood$` = the raw order size,
  the correct default when the zone total is 0) when the divisor is 0.

## Fix shape (task #14 — NOT yet implemented; for the design phase)
Two minimal, independent changes. (The reseed itself is task #5, tracked separately.)
1. **Restore the ±10% per-tick food-demand clamp** (`se_DEMAND.txt:221-263`). The intended clamp
   already exists as commented-out inline code that IS RHS-legal (it compares
   `var:l_comparison_diff < 0` against the literal 0, never a var-to-var comparison — precisely
   avoiding the 2023 `FUNC_clamp_variable` failure). Implementation = uncomment both blocks
   (upper bound 221-240, lower bound 244-263) and fix the ONE latent bug they carry: the
   `set_variable` target is written `name = var:DEMAND_food_$tradegood$` (:236, :259) — the
   `var:` prefix is illegal in a `name` field and must be `name = DEMAND_food_$tradegood$`.
   This bounds each tick's demand to ±10% of the previous tick, exactly the abandoned intent.
   - **DROPPED the earlier "cap the elasticity divisor `[0.5,2.0]`" idea** — with the ±10% clamp
     restored, per-tick demand change is already bounded, so a divisor cap is redundant and would
     be an unproven new constant (over-engineering). Faithful clamp restoration only.
2. **Guard the `se_GLOBALTRADE_split.txt:3340` Div/0** — mirror the accepted `#107` pattern:
   wrap the `divide` in `limit = { has_global_variable = $tradezone$_total_order_size_$tradegood$
   global_var:$tradezone$_total_order_size_$tradegood$ > 0 }`, leaving
   `order_as_percentage_of_TZ_total_$tradegood$` = the raw order size when the zone total is 0.

## Safety / caution (imp19c-sobisonator-upstream-caution)
- Change #1 touches the shared FOOD demand loop (all 6 food goods, not just vegetables). It is
  justified because git blame (`dd43d5419`) proves the damping was INTENDED and lost to a fixable
  scripting bug, not removed by design — restoring it completes the original intent. It is a
  faithful uncomment of the author's own replacement code, not a new mechanism. Still routed
  through design → adversarial review → code-review, and it ships with the existing TZP band
  logging so the next boot confirms behaviour across ALL food goods (watch grain/livestock do not
  regress).
- Change #2 is a pure defensive guard (mirror of an existing accepted pattern), no behaviour
  change except removing the Div/0 error spam.

## Boot-confirmation plan (guess-and-log, not a deferral)
- #14 ships the clamp restore + div/0 guard; #5 ships the reseed (primary supply fix).
- Next -debug_mode boot: `tools/curx_analyze.py --good vegetables` over debug.log — expect the
  ~19 collapsing zones' stock to STOP hitting 0 and price to stay in low bands; Div/0 count for
  the luxury/3/6 passes to drop to zero; grain/livestock demand bands to stay stable (clamp did
  not distort them). If a zone still collapses, it is a residual SUPPLY gap → raise that zone's
  reseed margin (#5), not the clamp.
