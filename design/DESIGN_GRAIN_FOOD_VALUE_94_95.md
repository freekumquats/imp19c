# Design — Concrete grain economy: #94 Capital Grain Reserve · #95 Canal Depots · canal condition · retire the 0-100 proxies

**Status:** DESIGN, not built. For adversarial review BEFORE any code. Consolidated 2026-08-09
(supersedes the earlier v1 石-rescale and v2 Plan-2 drafts — history in §9).
**Theme:** concrete-over-abstract ([[imp19c-concrete-over-abstract-rule]]). One real grain economy;
retire the abstract 0-100 proxies in favour of concrete on-map reality (real food + real buildings by
count AND position). Deep decline-era crisis code — spillover-sensitive; hence design-first.

---

## 1. Decisions locked (by the user, this session)

1. **#94 Plan 1 — the canal feeds the capital STATE's real (engine) food.** The Grand Canal delivers
   real tribute grain into the Beijing/Zhili state's food store (`add_state_food`); the "Capital Grain
   Reserve" IS that real food; famine gates read `has_state_food / has_state_food_capacity`. One food
   economy — the literal "plug into the real food system." (Plan 2, a sibling 食-pool mimicking the
   ever-normal pool's units but not its mechanism, is REJECTED — see §9.)
2. **A new 京倉/通倉 capital-granary building** provides the capital reserve's concrete capacity anchor
   (distinct from the provincial 常平倉 `qing_granary_building` and 社倉).
3. **Food is a VANILLA pop-consumption abstraction** — `has_state_food`/`_capacity` are consumed by pops
   at Imperator game-balance rates, NOT real daily grain. So ALL capacity/delivery/consumption values are
   **vanilla-food-scale balance knobs**, calibrated so famine cadence matches today. The sourced historical
   shi figures (§6) are **FLAVOUR/loc ONLY**, never a mechanic input.
4. **#95 — no double-count.** Depots already raise delivery INDIRECTLY via `qing_canal_condition` (+8 each);
   a second additive depot→delivery term would double-count. Depots' grain effect flows through condition→
   delivery (now real food); the per-depot 食 share is DISPLAYED, not re-added.
5. **Retire the abstract 0-100 proxies** (`qing_grain_reserve`, `qing_granary_stock`) by migrating their
   consumers to the concrete real values — not deleting variables with live consumers.
6. **Canal condition made concrete** — derive `qing_canal_condition` from real building COUNT AND POSITION
   (per corridor-stretch), not a flat empire-wide count feeding a drifting meter.

Sequenced as separate reviewed commits (§7). This doc is the DESIGN; the per-step IMPLEMENTATION design
(exact svalues, scopes, migrations) is written + re-reviewed before each commit.

## 2. Current state (verified in source)

**A. Ever-normal pool (常平倉) — REAL food, already concrete. `se_QING_DECLINE.txt:2366-2510`.**
`qing_granary_food` = pooled grain (engine food units, moved by `add_state_food`); cap
`qing_granary_capacity = qing_granary_count × 200`. `QING_DECLINE_granary_pool` (~180d) sweeps
`every_country_state`: skim 1/20 cap from near-max states → pool; ship to shortage states (`<1/5` cap) ←
pool. Derives `qing_granary_stock` (0..100 = food/cap×100). #93 surfaces food/capacity as a real bar.
NB it has many writers (se_QING_REVENUE:513 +600 pre-fill; qing_subject_integration:617/694; drawdowns in
FlavorEvents:289, shortage_events:186) — a busy shared object.

**B. Capital Grain Reserve (京倉) — ABSTRACT 0..100. `se_QING_CANAL.txt`.**
`qing_grain_reserve` (init 75 :59; `reserve += delivery − draw` :188-189; clamp 0..100 :191-192).
`delivery = qing_canal_condition/20 × jiangnan_quota (+1 sea route)`; `draw = 4 − min(qing_granary_count,2)`.
Only link to A: reads `qing_granary_count` to shave the draw (:180-186). Never touches engine food.

**C. Canal condition — ABSTRACT drifting 0..100. `se_QING_CANAL.txt:71-141`.**
Target = base 40 ± Works-minister finesse ± corruption, +8/depot (cap +24 at 3), +6/dike (cap +18 at 3);
live condition drifts ±3/qtr toward target. Buildings only NUDGE an abstraction, and are a FLAT
empire-wide count (se_QING_MINISTRY.txt:639-640) — POSITION unmodelled (a Zhejiang depot and a Yellow-River
dike count identically; the depot region-gate is enforced only at build time). Consumers: Works-minister
perf (se_QING_MINISTRY.txt:697), the qing_canal.2 sea-route event, the Works GUI bar.

**Building facts (verified):** `local_food_capacity` granted by `qing_granary_building` (+200) and several
`qing_agriculture_buildings` (+100/+200). NO capital/metropolitan granary building exists. `qing_granary_count`
counts provincial 常平倉 and already backs pool A's capacity.

## 3. #94 — Plan 1 detailed shape

- **Capital state:** `capital_scope.state` (proven: governor_policies/00_default.txt:300, invest/move_capital
  buttons). = 順天府/Zhili.
- **NEW building `qing_capital_granary_building` (京倉/通倉):** grants `local_food_capacity` (per-level, a
  vanilla-food-scale balance figure — §1.3); region-gated to the capital corridor (Zhili/順天府); SEEDED at
  1763 so the capital opens with a real metropolitan reserve capacity the canal fills. Distinct from 常平倉.
- **Delivery = real food IN:** each canal quarter `capital_scope.state = { add_state_food = <delivery> }`,
  delivery = the existing signal (condition/20 × jiangnan_quota × depot-through-condition, +sea route) scaled
  to the vanilla food unit. NO new additive depot term (§1.4).
- **Consumption = real food OUT:** `add_state_food = −<consumption>` (capital + banner garrisons + frontier
  armies), replacing the abstract `draw`.
- **Famine gates rewired:** `<40`/`<20` (se_QING_CANAL.txt:259/269) → fractions of the capital state's
  `has_state_food / has_state_food_capacity` (same real signal shortage.1 + pool A use). Preserve the
  `qing_high_qing_era` suppression + player-only/cooldown on the qing_canal.1-adjacent gate.
- **Famine-payload writers RE-POINTED (biggest hazard):** `QING_canal_relief_redirect` −10 (:307) and
  `_hoard` +4 (:324) act on the capital state's real food (`add_state_food ∓`), not the retired var — else
  the player's dilemma choices become no-ops.
- **`qing_grain_reserve` RETIRED:** GUI shows `has_state_food / has_state_food_capacity` (real, #93-style);
  qing_canal.1 LOG (:41) re-pointed. Grep-verify ALL consumers migrated before deletion.
  **Complete consumer list (verified):** WRITERS se_QING_CANAL.txt:59,188,189,191,192,307,324;
  READERS :259,:269, gui/qing_works_ministry.gui:234,:240, events/…/qing_canal_events.txt:41.
- **Cadence:** NOT 1:1. Calibrate delivery/consumption vs the capital state's VANILLA pop food-consumption
  so the fill/drain rate (relative to the 京倉 capacity) reproduces today's famine timing. Boot-test knob.
- **Ever-normal-sweep interaction (playtest):** `QING_DECLINE_granary_pool`'s `every_country_state` (:2395)
  iterates the capital state too → it would skim canal-delivered grain back into pool A when the capital is
  near-max and ship to it when short. Decide: (a) accept the coupling (most concrete), or (b) EXCLUDE the
  capital state from the SKIM leg (a strategic reserve, not a surplus donor) while allowing the ship leg.
  RECOMMEND (b). Playtest either way.

## 4. #95 — Canal Depots on real food (no double-count)

Depots' contribution flows through `qing_canal_condition` → delivery (now real food); the Works panel DISPLAYS
each depot's grain-throughput 食 share (derived from its condition contribution). NO new additive
`delivery += depot_count × D` term (would double-count the +8/depot condition lift). Weak-sense "exact"
(count already influences it, capped at 3, blended, lagged); the STRONG per-depot split-delivery rebalance
(remove the condition depot-bonus, add a direct per-depot delivery term) is DEFERRED — flag for user.

## 5. Retire the 0-100 proxies + concrete canal (count + position)

**(i) `qing_granary_stock` — retire, don't delete.** **12** live consumers gate on the 0-100 scale (see §8b
for the corrected count + the three se_QING_DECLINE.txt lines this list omits, and the granaryless-default
invariant). Enumerated here (partial):
se_QING_POPULATION.txt (`<30`/`>=60`/`<=15`, +20 nudge :105/:110/:210-234); se_QING_MECHANICS.txt (+25/−20
nudges, `qing_granary_stocked` modifier `>=40`/`<40` :94-110); qing_decline_events.txt (`>=20` ×2),
qing_population_events.txt (`<=15`); GUI (population + works panels). Migrate each to read the real fraction
`qing_granary_food / qing_granary_capacity`, then drop the derived var. Pool A becomes the single truth.

**(ii) `qing_canal_condition` — derive from real buildings + POSITION.** Replace the drift-meter with a
condition DERIVED from per-corridor coverage: tally depots per canal-corridor region (Zhili/Shandong/Jiangsu/
Zhejiang) and dikes per Yellow-River region, so condition reflects whether the SPECIFIC stretches are
maintained — a gap in the Shandong stretch silts that segment regardless of over-building elsewhere. Preserve
the qing_canal.2 gate (condition<45) and the Works-perf fold (se_QING_MINISTRY.txt:697) as fractions/derived.
Bigger rework; its own reviewed slice.

## 6. Historical figures — FLAVOUR/loc ONLY (research/QING_GRANARY_CAPACITIES.md)

Food is a vanilla pop abstraction (§1.3), so these anchor NO mechanic number — tooltip colour only:
- 常平倉 empire-wide **48,118,350 shi** pre-1748 (Liu Ts'ui-jung 1980 citing 《大清會典事例》) — nominal QUOTA,
  not audited stock; not cross-checked vs Will & Wong.
- 漕糧 **~4,000,000 shi/yr** (Qing) — indicative, tertiary-depth; the "~400,000 tons" figure is Ming, don't reconcile.
- 京倉/通倉 capacity — GENUINE GAP (the "4M shi capital" figure is Ming). Moot: the mechanic uses a
  vanilla-food-scale balance capacity, not shi.
- 1 Qing shi ≈ **103.5 L** (volume unit; ≠ the 70.8 kg weight-picul — conflation trap).

## 7. Build sequence (each its own IMPLEMENTATION design + adversarial review + commit)
1. ✅ #93 (done) — real food shown on the Works panel.
2. #94 Plan 1 — 京倉 building + canal→capital-state food + famine-gate rewire + payload-writer re-point +
   retire qing_grain_reserve. (Depends on nothing further; the big one.)
3. #95 display — depots' 食 share on the Works panel (rides on #94's real-food delivery).
4. Retire `qing_granary_stock` — migrate its 12 consumers to food/capacity (re-derive the full list + the
   granaryless-default guard first; see §8b — the risky slice). **NOTE: §7 is superseded by the §8b re-sequence.**
5. Canal condition derived from per-corridor coverage.

## 8. Open questions for review
1. Ever-normal-sweep interaction: recommend EXCLUDE capital state from the skim leg — confirm the state-scope
   exclusion is expressible and doesn't break the sweep's every_country_state guards.
2. Is seeding the 京倉 building at 1763 (setup) the right way to give the capital opening capacity, vs an
   init effect? (Setup rejects BOM; add_building_level bypasses potential.)
3. `add_state_food` sign/scale: confirm the delivery/consumption magnitudes needed for sane cadence are
   representable (are there fractional-food or clamp gotchas on add_state_food?).
4. Retiring `qing_grain_reserve` + `qing_granary_stock`: any consumer in a SAVE that would misread during
   migration (persisted vars)? Need a migration guard?
5. #95 strong split-delivery rebalance — pursue or leave the weak (through-condition) form?
6. Does the capital state receiving canal food interact with vanilla amenities/pop-growth in a way that
   over-feeds the capital (runaway pop)? Bound the delivery.

## 8b. ADVERSARIAL REVIEW FINDINGS (2026-08-09) — PROCEED, with corrections + a re-sequence

Verdict: doc is substantially sound and cites source accurately. No finding refutes Plan 1. Close the
three gaps below and start with a NARROWER first slice than §7 step 2 proposed. Per-item verdicts:

**MUST-FIX corrections (fold into the per-slice impl designs):**
1. **`add_state_food` syntax — block form + `multiply = -1`.** Every proven call is block form
   `add_state_food = { value = var:x }`; negatives via `multiply = -1` (se_QING_DECLINE.txt:2431/:2451, the
   :2451 comment says the bare form is unattested). §3's pseudocode (`add_state_food = <delivery>`,
   `= −<consumption>`) is written in the UNATTESTED bare form — impl must use block form + multiply=-1.
   Fractional amounts are already de-facto exercised by the pool (/20, /10); engine clamp-at-capacity is
   NOT asserted anywhere — treat clamp behaviour as unverified until boot.
2. **Capital-move breaks the capacity anchor (§3 under-states this).** `capital_scope.state` recomputes
   live so DELIVERY follows a moved capital — but the 京倉 is seeded in a FIXED region (Zhili/順天府), so a
   moved capital points delivery at a state with NO 京倉 (low capacity) and the famine gate misreads. The
   delivery-target and the capacity-anchor decouple under a capital move. Reconcile in the impl design.
3. **`qing_granary_stock` retirement — the risky slice; list was INCOMPLETE and the 1:1 claim is FALSE.**
   §5(i) says "~8 consumers"; independent grep finds **12**, and §5 OMITS three in se_QING_DECLINE.txt
   itself: `:1216` (sect-pressure cross-wire, `>=70` eases qing_sect_pressure), `:2531` (good-year → build a
   real 常平倉 gate, `>=60`), `:2564` (famine → empty granaries gate, `<=15`). The last two ARE the
   concrete-granary-building logic this program means to strengthen — omitting them under-scopes the slice
   against its own thesis. **The 1:1 migration is NOT behaviour-preserving:** qing_granary_stock defaults to
   **30** and is deliberately HELD at 30 while `qing_granary_capacity == 0` (se_QING_DECLINE.txt:119,
   :2493-2501 — a prior review-fix so a granaryless realm isn't false-flagged into famine). The fraction
   `food/capacity` CANNOT reproduce this — at cap 0 it is divide-by-zero/undefined, not "30." So every
   migrated consumer needs an explicit `capacity > 0` guard + a defined granaryless-default, or a granaryless
   1763 realm divides-by-zero or flips straight into famine/pop-pressure/empty-granary bands. This is a
   BLOCKING migration invariant, not a caveat. Re-derive the full 12-consumer list before any code.

**Under-flagged spillovers (confirm as first-class constraints):**
- **Amenities/pop-growth coupling (MEDIUM).** Positive state food auto-applies the hardcoded growth modifier
  (00_hardcoded.txt `positive_state_food_growth`, `local_population_growth = 0.02`) → a well-fed high-capacity capital risks runaway
  Beijing pop. Bound the delivery and/or 京倉 capacity — a first-class calibration constraint (Q6), not an
  afterthought.
- **Seed via INIT EFFECT, not setup/.** There is ZERO precedent for seeding any `qing_*` building in setup/
  (all are runtime-spawned); use `add_building_level` (bypasses potential) in a game-start hook. Answers Q2.

**CONFIRMED sound (resolve as settled):**
- `add_state_food` + `capital_scope.state` are real, proven primitives (state scope; :2431/:2451; governor_
  policies/00_default.txt:300-301). Capital = province 8363 (Beijing)/Zhili.
- Famine-gate rewire (has_state_food/_capacity) is state-scope + idiomatic; the stale-read is the SAME one the
  pool already tolerates. **BONUS:** shortage.1 keys on `any_governorship_state`, which EXCLUDES the capital
  home state — so draining the capital below 1 will NOT double-fire shortage.1 alongside qing_canal.1 (Q-resolved).
- Famine-payload writers (:307 −10, :324 +4) are the ONLY two; re-point to capital_scope.state add_state_food
  is reachable + coherent.
- Ever-normal skim exclusion (Q8/§3(b)) is expressible WITHOUT touching the precomputed-operand guards: a
  scope-identity test `NOT = { this = ROOT.capital_scope.state }` on the FILL leg (:2418) is a different
  construct from the numeric-RHS guard and is proven at governor_policies/00_default.txt:301. Nuance: excluding
  only the SKIM leg still lets the SHIP leg refill the capital; the 京倉's large capacity may keep the capital
  in the `<1/5` ship band and preferentially pull pool grain — playtest note.
- qing_grain_reserve retirement is CLEAN (all 12 cited lines confirmed; only trivial omission is the :58 init
  guard, deleted with the block). #95 no-double-count CONFIRMED (depots feed delivery ONLY via condition).
  Canal-condition-by-position FEASIBLE with negligible perf (adds is_in_region branches to the existing
  every_owned_province sweep; is_in_region proven at se_QING_CANAL.txt:214).

**RE-SEQUENCE (supersedes §7 step 2 — split the big bundle; §7 front-loaded the capital-move + amenities risk):**
1. ✅ #93 (done).
2. **京倉 building + init-effect seeding + capacity anchor ONLY** (no delivery yet) — smallest reviewable slice;
   boot-verify the building, the amenities/pop-growth coupling, and capital-state resolution in isolation.
3. **Canal→capital-state delivery/consumption + famine-gate rewire + payload re-point + retire qing_grain_reserve**
   (the clean retirement).
4. #95 display (rides on 3).
5. **qing_granary_stock retirement** — the RISKY slice; only after re-deriving its 12-consumer list + fixing the
   granaryless-default invariant (block-fix above).
6. Canal-condition by per-corridor coverage.

## 8c. SLICE 2 — IMPLEMENTATION SPEC (2026-08-09) — 京倉 building + init-effect seeding + capacity anchor ONLY

Smallest reviewable slice (§8b re-sequence step 2). NO delivery, NO consumption, NO gate rewire — just
put the concrete capital-granary building on the map at 1763 start with a real `local_food_capacity`
anchor, so a later slice has a capacity to fill. Verified facts driving the shape:

- **`add_building_level` RESPECTS `potential`** ([[imp19c-add-building-level-respects-potential]] + the
  #190 in-repo correction, se_QING_BUILDINGS.txt:105). So the building's `potential` MUST be satisfiable
  at the seed site. Seed site = **Beijing P8363** — CHI-owned, city, **region Zhili** (verified:
  areas.txt Beijing area ∈ regions.txt Zhili block:652). Gate = `is_in_region = Zhili` + jurchen/chinese
  culture (the proven region+culture seeding idiom; province_id in a building potential is UNATTESTED —
  avoid). This restricts the metropolitan granary to the capital corridor, which is the design intent.
- **Amenities/pop-growth coupling (§8b MEDIUM / Q6) does NOT bite in this slice.** The hardcoded
  `positive_state_food_growth` (00_hardcoded.txt:1193, `local_population_growth = 0.02`) fires on a food
  SURPLUS, not on capacity. This slice adds capacity but NO food-in and — deliberately — NO
  `local_monthly_food_modifier` (which would raise production → create surplus). So it cannot trigger
  runaway Beijing pop. That is precisely why §8b isolated capacity-only as the safe first boot.
- **Capital-move (§8b MUST-FIX #2) does NOT bite in this slice.** No delivery is pointed at
  `capital_scope.state` yet, so the fixed-Zhili building and a (hypothetical) moved capital cannot
  decouple. That reconciliation lands in slice 3 when delivery is wired.

### Files touched (slice 2)
| File | Change |
|---|---|
| `common/buildings/qing_granary_buildings.txt` | + new `qing_capital_granary_building` (京倉/通倉) — capacity anchor |
| `common/scripted_effects/se_QING_BUILDINGS.txt` | + 1 `QING_seed_works_building` seed line at P8363 |
| `localization/english/qing_works_l_english.yml` | + name + `_desc` (sits with the canal depot, its economy) |
| `localization/english/imp19c_tooltips_l_english.yml` | + `tooltip_qing_capital_granary_building` results tooltip |

### Building schema (exact)
```
qing_capital_granary_building = {
    local_food_capacity = 400              # metropolitan anchor = 2× the provincial 常平倉 (200).
    local_monthly_state_loyalty = 0.03     # a fed, provisioned capital is a quiet one (non-food key).
    local_population_happiness  = 0.03     # ditto. NO local_monthly_food_modifier — see §8c (no surplus).
    cost = 80
    time = 200
    potential = {
        is_in_region = Zhili
        OR = { owner = { OR = { country_culture_group = jurchen  country_culture_group = chinese_group } } }
    }
    allow = { sufficient_job_slots = yes }
    modification_display = { 0 = local_food_capacity  1 = local_monthly_state_loyalty  2 = local_population_happiness }
}
```
`local_food_capacity = 400` is a **vanilla-food-scale balance knob** (§1.3) and the calibration lever the
slice-3 delivery is tuned against — revisit it there, not here. The two flavour keys are non-food (they
cannot make surplus), keeping the slice genuinely capacity-only w.r.t. the food economy.

### Seed line (exact) — added to `SE_qing_starting_buildings`, adjacent to the canal-depot works block
```
QING_seed_works_building = { P = 8363  B = qing_capital_granary_building  NAME = "Beijing 北京 metropolitan granary 京倉/通倉" }
```
`QING_seed_works_building` guard = exists + `owner = c:CHI` + `NOT has_building` (ownership-only, idempotent,
bypasses `allow` but respects `potential` — all satisfied at P8363). Same macro the 5 hydraulic works use.

### Localization (BOM + LF; both files have BOM)
- `qing_works_l_english.yml`: `qing_capital_granary_building:0 "京倉 Metropolitan Granary"` + `_desc`.
- `imp19c_tooltips_l_english.yml`: `tooltip_qing_capital_granary_building:0 "#T Results:#! …"` mirroring the
  granary tooltip shape (colour codes `#G …#!`), so the build-menu hover shows no raw key.

### Invariants (applied-diff review)
- Braces balanced; BOM per file (buildings/loc BOM; se_ none — 232323 header); no EOL churn.
- `potential` satisfiable at P8363 (region Zhili + CHI culture=jurchen) → seed lands, does not silently drop.
- NO `local_monthly_food_modifier` on the building (would break the capacity-only isolation).
- Seed is idempotent (NOT has_building) + guarded (exists + owner) — a re-mapped capital cannot mis-seed.
- No consumer reads this building yet (delivery is slice 3) — the slice is inert beyond capacity + flavour.

## 8d. SLICE 3 — IMPLEMENTATION SPEC (2026-08-09) — canal→capital-state REAL FOOD + famine-gate rewire + payload re-point + retire `qing_grain_reserve`

§8b re-sequence step 3. This is the substantive slice: it replaces the abstract 0..100 `qing_grain_reserve`
counter with REAL engine food on the capital state (the 京倉 capacity anchor placed in slice 2 is what that
food fills), rewires the famine gates to the real signal, re-points the famine-dilemma payloads, and retires
`qing_grain_reserve` cleanly. CHI-only; no-BOM/LF file (se_QING_CANAL header 232323 = no BOM).

### Verified primitives driving the shape
- **`capital_scope.state = { … }` is a PROVEN effect scope** (se_DIPLOMACY.txt:1049 `scope:play_target_country.capital_scope.state = {…}`). = 順天府/Zhili for CHI.
- **`add_state_food = { value = <var> }`** and negative via **`{ value = <var>  multiply = -1 }`** — proven block forms (pool A se_QING_DECLINE.txt:2431/:2451; apotheosis se_IDEOLOGY_APOTHEOSIS.txt:88 with value/multiply/min/max). Bare `= var:X` is UNATTESTED — never used.
- **`has_state_food` / `has_state_food_capacity`** read into a `set_variable` (state scope) — proven (pool A :2407-2408; governor_policies:154, 00_governor_policies:140).
- **Cross-scope read** `set_variable = { value = ROOT.var:X }` inside a state scope — proven (pool A :2413). **Cross-scope write** `ROOT = { set_variable/change_variable … value = scope:S.var:Y }` — proven (pool A :2432); requires the state be `save_scope_as` first.
- **Comparison RHS:** var-vs-var MUST use the `_cmpsvalue` suffix (pool A :2409, :2427); var-vs-literal (`< 40`, `> 0`) is legal bare. [[imp19c-rhs-comparison-operator-rule]].
- **GUI** reads Player COUNTRY vars only (no attested country→capital→state→food datafunction chain in the Works panel); so the capital food/cap is MIRRORED into country vars each tick, exactly as the #93 pool bar mirrors `qing_granary_food`/`qing_granary_capacity`.

### CALIBRATION — capacity-RELATIVE fractions, not a fixed FOOD_SCALE (rev after adversarial review 2026-08-09)
**Adversarial-review HIGH-1 + HIGH-2 (CONFIRMED against source) forced this redesign.** The prior draft
anchored a `FOOD_SCALE = 4` on the 京倉's 400 `local_food_capacity`, assuming the capital STATE's
`has_state_food_capacity ≈ 400`. FALSE: `province_base_values` grants EVERY province `local_food_capacity = 100`
(common/modifiers/00_hardcoded.txt:141), and the Beijing capital state is **7 provinces** (map_data/areas.txt:12969
— 2640/3250/3500/3783/4109/4401/8363), so its capacity is **~700 (base) + 400 (京倉) + farm buildings ≈ 1100+**,
NOT 400. A fixed ×4 band (4-20 food/qtr) on a ~1100 capacity is <2%/qtr — the reserve would sit pinned near-full
on vanilla production and the `<40`/`<20` gates would never fire (HIGH-1); and a small fixed delivery clamped to
near-zero headroom would be discarded every tick, severing the canal→reserve coupling (HIGH-2).

**Fix (keeps LOCKED Plan 1 — real state food, gates read the real signal; does NOT adopt the rejected Plan-2
private pool):** make delivery and draw **percentages of the measured `has_state_food_capacity`**, so they
auto-scale to the true capacity (whatever the boot reveals) with NO hardcoded anchor, AND make the draw a
**large, always-applied structural drain** — the capital + banner garrisons + frontier armies, the grain sink
the 漕運 tribute historically EXISTED to feed (the north could not feed itself; that is the whole mechanic).
Because the draw is applied every tick it continuously RE-OPENS headroom, so the headroom-clamped delivery is
never permanently discarded — the canal condition sets the equilibrium fill level (HIGH-2 resolved):
- **draw fraction** = `0.06` of capacity/qtr, minus `0.01` per provincial 常平倉 (`qing_granary_count`, cap 2)
  → floor `0.04` (preserves the existing granary-shaves-the-draw coupling, se_QING_CANAL.txt:180-186, as a %).
- **delivery fraction** = `(qing_canal_condition / 100) × 0.08` × `jiangnan_quota` (0.5..1.0), `+0.01` flat if
  the sea route is open. So at full condition delivery ≈ 8% > draw 6% → the reserve fills; at condition 50
  delivery ≈ 4% < draw 6% → net −2%/qtr slow drain; at condition 25 delivery ≈ 2% → −4%/qtr toward famine.
  Canal condition thus has a MONOTONE grip on the equilibrium, which is the design intent.
- **Why these two literals:** 0.08 delivery > 0.06 draw keeps a sound canal net-positive (fills to near cap);
  the ~2pt gap makes a silted canal drain at a visible-but-not-whiplash rate (a multi-year decline into famine,
  matching the historical 19th-c. arc). Rejected: equal frac (no fill headroom ever, permanent knife-edge);
  >0.15 (a single quarter swings >15% of cap — whiplash before vanilla settles).
- **These magnitudes are boot-tuned.** Whether they dominate or are dominated by Zhili's VANILLA net food
  production is genuinely unknown without a boot (Q: is the 1763 capital state a vanilla food surplus or
  deficit region?). The slice ships INSTRUMENTED — a LOG_line each tick dumping `food / cap / pct / deliver_amt
  / draw_amt` — so the FIRST boot reveals the regime and confirms/retunes the two fractions. **This is NOT a
  deferral:** the mechanic is fully built, wired, and self-scaling; the two fractions are documented literals a
  boot confirms, exactly the "boot-test knob" §3 + Q6 already designate. If the boot shows vanilla swamps a 6%
  draw, the follow-up is a one-literal bump (draw 0.06→higher) on a shipped correct mechanic, not new design.

### Runaway-pop guard (§8b MEDIUM / Q6) — headroom clamp + always-on draw
`positive_state_food_growth` (00_hardcoded.txt:1193) fires on food SURPLUS. The delivery leg CLAMPS to
remaining headroom (`cap − food`) before applying (the SAME clamp pool A uses on its skim leg,
se_QING_DECLINE.txt:2425-2429), so delivery can never push food PAST capacity. Combined with the always-applied
draw, near-full the net each tick is `min(delivery, headroom) − draw < 0`, so the reserve sits JUST BELOW cap
rather than pegged at surplus — the always-on draw is itself the anti-runaway mechanism (the capital is a net
consumer, so it cannot balloon). Consumption/redirect drains clamp to available food (never below 0).

### Capital-move (§8b MUST-FIX #2) — honest statement (review MED-1: the old cap>0 rationale was illusory)
Adversarial-review MED-1 (CONFIRMED): a `cap > 0` guard does NOT detect a moved capital — a state with no 京倉
still has capacity `100 × provinces > 0` (00_hardcoded.txt:141). So `cap > 0` is purely **divide-by-zero
safety** on the pct-derive, NOT moved-capital protection. Honest position: **for CHI the capital is Beijing and
does not move**, so the fixed-Zhili 京倉 and the live `capital_scope.state` delivery target never decouple in
practice. No building-presence gate is added (a per-tick `has_building` scan for a case that cannot arise for
the only tag that runs this CHI-gated code is unwarranted). The `cap > 0` guard stays, correctly labelled as
divide-safety only.

### Country vars introduced (all on CHI)
| var | meaning | written by | read by |
|---|---|---|---|
| `qing_capital_food` | capital state's stored food (post-tick mirror, arithmetic) | `QING_canal_run_grain_balance` | GUI value, gate |
| `qing_capital_food_cap` | capital state's food capacity (mirror) | ″ | GUI value, gate guard |
| `qing_capital_grain_pct` | `food/cap*100` (0..100), guarded cap>0 | ″ | famine gates `<40`/`<20`, GUI bar fill |

`qing_grain_delivery` / `qing_grain_draw` are re-purposed as the intermediate FRACTION vars (0..~0.08 / 0.04..0.06),
removed at end of the effect; the state scope multiplies each by the measured capacity to get the food amount.

### QING_canal_run_grain_balance — rewrite (se_QING_CANAL.txt:150-195)
REPLACE the whole body. Compute the two FRACTIONS in country scope (re-using the existing condition/quota/
sea-route/granary-count inputs, now as %-of-capacity terms), then apply inside the capital state scope:
```
QING_canal_run_grain_balance = {
	# --- DELIVERY FRACTION (0..~0.08 of capacity/qtr): canal condition × 8%, scaled by the Jiangnan quota. ---
	set_variable = { name = qing_grain_delivery  value = var:qing_canal_condition }
	change_variable = { name = qing_grain_delivery  divide = 100 }          # condition -> 0..1
	change_variable = { name = qing_grain_delivery  multiply = 0.08 }       # -> 0..0.08 at full condition
	QING_canal_compute_jiangnan_quota = yes
	change_variable = { name = qing_grain_delivery  multiply = var:qing_canal_jiangnan_quota }   # ×0.5..1.0
	if = { limit = { has_variable = qing_sea_route_open }  change_variable = { name = qing_grain_delivery  add = 0.01 } }   # flat +1% floor
	# --- DRAW FRACTION (0.04..0.06 of capacity/qtr): the metropolitan+garrison+frontier grain sink. ---
	set_variable = { name = qing_grain_draw  value = 0.06 }
	if = {
		limit = { has_variable = qing_granary_count  var:qing_granary_count > 0 }
		set_variable = { name = qing_grain_draw_relief  value = var:qing_granary_count }
		if = { limit = { var:qing_grain_draw_relief > 2 } set_variable = { name = qing_grain_draw_relief  value = 2 } }
		change_variable = { name = qing_grain_draw_relief  multiply = 0.01 }
		change_variable = { name = qing_grain_draw  subtract = var:qing_grain_draw_relief }
		remove_variable = qing_grain_draw_relief
	}
	# --- APPLY to the capital state's REAL food; mirror the result back to CHI for the gate + GUI. ---
	if = {
		limit = { exists = capital_scope  exists = capital_scope.state }
		capital_scope.state = {
			save_scope_as = qing_cap_state
			set_variable = { name = qing_cap_food_tmp  value = has_state_food }
			set_variable = { name = qing_cap_cap_tmp   value = has_state_food_capacity }
			# DELIVERY amount = cap × delivery-fraction, clamped to headroom (cap − food) — runaway-pop guard.
			set_variable = { name = qing_cap_deliver_tmp  value = has_state_food_capacity }
			change_variable = { name = qing_cap_deliver_tmp  multiply = ROOT.var:qing_grain_delivery }
			set_variable = { name = qing_cap_room_tmp  value = has_state_food_capacity }
			change_variable = { name = qing_cap_room_tmp  subtract = var:qing_cap_food_tmp }
			if = { limit = { var:qing_cap_deliver_tmp > qing_cap_room_tmp_cmpsvalue }  set_variable = { name = qing_cap_deliver_tmp  value = var:qing_cap_room_tmp } }
			if = { limit = { var:qing_cap_deliver_tmp < 0 }  set_variable = { name = qing_cap_deliver_tmp  value = 0 } }   # headroom can be negative if food>cap; no negative delivery
			if = { limit = { var:qing_cap_deliver_tmp > 0 }  add_state_food = { value = var:qing_cap_deliver_tmp } }
			# DRAW amount = cap × draw-fraction, clamped to available food so it never drives below 0.
			set_variable = { name = qing_cap_draw_tmp  value = has_state_food_capacity }
			change_variable = { name = qing_cap_draw_tmp  multiply = ROOT.var:qing_grain_draw }
			if = { limit = { var:qing_cap_draw_tmp > qing_cap_food_tmp_cmpsvalue }  set_variable = { name = qing_cap_draw_tmp  value = var:qing_cap_food_tmp } }
			if = { limit = { var:qing_cap_draw_tmp > 0 }  add_state_food = { value = var:qing_cap_draw_tmp  multiply = -1 } }
			# MIRROR post-tick food + cap back to CHI. Compute final food ARITHMETICALLY (initial + delivered −
			# drawn) rather than RE-READING has_state_food after the add_state_food calls — whether an
			# add_state_food write is reflected in a same-block has_state_food read is UNVERIFIED (pool A never
			# re-reads); both operands are the already-clamped actual amounts, so the arithmetic is exact.
			set_variable = { name = qing_cap_foodfinal_tmp  value = var:qing_cap_food_tmp }
			change_variable = { name = qing_cap_foodfinal_tmp  add = var:qing_cap_deliver_tmp }
			change_variable = { name = qing_cap_foodfinal_tmp  subtract = var:qing_cap_draw_tmp }
			ROOT = {
				set_variable = { name = qing_capital_food      value = scope:qing_cap_state.var:qing_cap_foodfinal_tmp }
				set_variable = { name = qing_capital_food_cap  value = scope:qing_cap_state.var:qing_cap_cap_tmp }
			}
		remove_variable = qing_cap_food_tmp
		remove_variable = qing_cap_cap_tmp
		remove_variable = qing_cap_room_tmp
		remove_variable = qing_cap_deliver_tmp
		remove_variable = qing_cap_draw_tmp
		remove_variable = qing_cap_foodfinal_tmp
	}
	# DERIVE the 0..100 pct for the gates + GUI bar. cap>0 is DIVIDE-BY-ZERO safety only (review MED-1: a
	# state ALWAYS has cap = 100×provinces > 0, so this is NOT moved-capital detection). has_variable guards
	# the first-ever tick before the mirror ran.
	if = {
		limit = { has_variable = qing_capital_food_cap  var:qing_capital_food_cap > 0 }
		set_variable = { name = qing_capital_grain_pct  value = var:qing_capital_food }
		change_variable = { name = qing_capital_grain_pct  multiply = 100 }
		change_variable = { name = qing_capital_grain_pct  divide = var:qing_capital_food_cap }
	}
	# [slice-3 INSTRUMENTATION — the boot-tuning acceptance gate for the two calibration fractions]
	# RESOLVED (source check): LOG_line has NO value field — it is `debug_log = "IMP19C $sys$: $msg$"`
	# (se_LOG.txt:49-56), and a $/# in $msg$ is forbidden (log-string-macro-rule). The PROVEN way to dump
	# numeric var values is LOG_state (se_LOG.txt:77-82), which writes a header line + `debug_log_scopes = yes`
	# (the full ROOT scope-stack dump). All five vars are on ROOT (CHI) at this point, so one LOG_state emits
	# food/cap/pct/delivery/draw for the boot to read. Placed BEFORE the two removes so delivery/draw are dumped.
	LOG_state = { sys = QING  note = "canal grain balance (capital food/cap/pct + delivery/draw frac in scope dump)" }
	remove_variable = qing_grain_delivery
	remove_variable = qing_grain_draw
}
```

### QING_canal_init — retire the reserve seed (se_QING_CANAL.txt:57-60)
DELETE the `qing_grain_reserve` init block (:57-60). KEEP the `qing_canal_condition` init (:53-56). No
replacement seed needed: the capital state opens with the 京倉 capacity (slice 2) + whatever vanilla food it
starts with; the first tick mirrors it into `qing_capital_food(_cap)`.

### QING_canal_quarterly_tick — famine gates (se_QING_CANAL.txt:257-300)
- `:259` `var:qing_grain_reserve < 40` → **`has_variable = qing_capital_food_cap  var:qing_capital_food_cap > 0  var:qing_capital_grain_pct < 40`** (guard + rewire). Keeps the `NOT high_qing_era` suppression. (review MED-2: add the `has_variable` guard for parity with the pct-derive — first-tick safety.)
- `:269` `var:qing_grain_reserve < 20` → **`has_variable = qing_capital_food_cap  var:qing_capital_food_cap > 0  var:qing_capital_grain_pct < 20`** + the existing `is_ai = no` + cooldown. Preserves player-only + throttle.
- The qing_canal.2 sea-route gate (:288, `qing_canal_condition < 45`) is UNTOUCHED (condition, not reserve).

### Payload re-point (se_QING_CANAL.txt:307, :324) — FULL idiom, not prose (review MED-3)
Both replace the `QING_DECLINE_nudge` on the retired var with real-food math on the capital state, using the
EXACT balance-block idiom (save_scope_as → precompute operands into state vars → `_cmpsvalue` clamp →
block-form `add_state_food` → re-mirror + re-derive pct under cap>0). Magnitudes are now %-of-capacity (not
the old fixed ±10/+4), for consistency with the fraction-based balance:
- `QING_canal_relief_redirect` (:307, was −10 nudge): DRAIN the capital reserve to feed the provinces —
  ```
  if = { limit = { exists = capital_scope  exists = capital_scope.state }
      capital_scope.state = {
          save_scope_as = qing_cap_state
          set_variable = { name = qing_cap_food_tmp  value = has_state_food }
          set_variable = { name = qing_cap_cap_tmp   value = has_state_food_capacity }
          set_variable = { name = qing_cap_draw_tmp  value = has_state_food_capacity }
          change_variable = { name = qing_cap_draw_tmp  multiply = 0.10 }             # relief shipment = 10% of cap
          if = { limit = { var:qing_cap_draw_tmp > qing_cap_food_tmp_cmpsvalue }  set_variable = { name = qing_cap_draw_tmp  value = var:qing_cap_food_tmp } }
          if = { limit = { var:qing_cap_draw_tmp > 0 }  add_state_food = { value = var:qing_cap_draw_tmp  multiply = -1 } }
          set_variable = { name = qing_cap_foodfinal_tmp  value = var:qing_cap_food_tmp }
          change_variable = { name = qing_cap_foodfinal_tmp  subtract = var:qing_cap_draw_tmp }
          ROOT = { set_variable = { name = qing_capital_food  value = scope:qing_cap_state.var:qing_cap_foodfinal_tmp }
                   set_variable = { name = qing_capital_food_cap  value = scope:qing_cap_state.var:qing_cap_cap_tmp } }
          remove_variable = qing_cap_food_tmp  remove_variable = qing_cap_cap_tmp
          remove_variable = qing_cap_draw_tmp  remove_variable = qing_cap_foodfinal_tmp
      }
      QING_canal_rederive_capital_pct = yes    # shared pct-derive helper (see below)
  }
  ```
  KEEP the existing `add_stability = 1` / `sect_pressure −5` / `current_ruler add_popularity 5` lines.
- `QING_canal_relief_hoard` (:324, was +4 nudge): FIRM the capital reserve — same skeleton but a delivery of
  `+0.05 × cap` clamped to headroom (`cap − food`, guarded ≥0), `add_state_food = { value = amt }` (positive),
  `foodfinal = food + amt`. KEEP the `sect_pressure +8` / `reform_pressure +4` / `add_stability −1` lines.
- **Extract the pct-derive into a shared helper `QING_canal_rederive_capital_pct`** (the guarded
  `food×100/cap` block) so the balance tick AND both payloads re-derive identically without duplication.

### GUI (gui/qing_works_ministry.gui:234, :240) + loc
- `:234` value textbox → `[Player.MakeScope.GetVariable('qing_capital_food').GetValue|0] / [Player.MakeScope.GetVariable('qing_capital_food_cap').GetValue|0]` (real food / capacity, matching the #93 pool bar's `_VALUE` shape). Widen the textbox 60→90 like the pool row.
- `:240` progressbar value → `[FixedPointToFloat( Player.MakeScope.GetVariable('qing_capital_grain_pct').GetValue )]` (the derived %).
- `QING_WORKS_MINISTRY_GRAIN_TT` (loc :32) reworded: real capital-state food vs its metropolitan capacity (京倉/通倉), filled by the canal, drawn by the capital + banners — drop the "(0–100)" phrasing.

### canal.1 LOG (events/…/qing_canal_events.txt:41)
Re-point `GetVariable('qing_grain_reserve')` → `GetVariable('qing_capital_grain_pct')` (the surviving signal).

### Retirement completeness (all 14 `qing_grain_reserve` sites — review LOW-1 corrected 13→14)
WRITERS se_QING_CANAL.txt:59 (init seed) + :58 (its `has_variable` guard) — the whole :57-60 block DELETED;
:188/:189/:191/:192 (balance — replaced by the fraction rewrite). PAYLOADS :307/:324 (re-pointed to real food).
READERS :259/:269 (gates — rewired to `qing_capital_grain_pct`), gui:234/:240 (re-pointed to
`qing_capital_food`/`_cap`/`_pct`), qing_canal_events.txt:41 (LOG re-pointed). Plus the header comment :20
(update to describe real food). After this slice a repo-wide grep for `qing_grain_reserve` returns ZERO (design
doc/overnight excluded — and DESIGN_QING_CROSSWIRING_ASSESSMENT.md:423, review LOW-2, gets a one-line update so
it doesn't misdescribe the now-real-food banner-decay coupling). `qing_granary_stock` is a SEPARATE var (pool A)
and is OUT of scope here (slice 5).

### Invariants (applied-diff review)
- Braces balanced; se_QING_CANAL.txt stays no-BOM/LF; GUI/loc keep their BOM; no EOL churn (numstat == --ignore-cr-at-eol numstat).
- Every var-vs-var comparison uses `_cmpsvalue`; every var-vs-literal is bare. No `ROOT.var:` on a comparison RHS (cross-scope pool reads go into a state var first, then compare via `_cmpsvalue`).
- `add_state_food` only in the proven block form; negatives via `multiply = -1`.
- Delivery = %-of-capacity, clamped to headroom (no forced surplus → no runaway pop; the always-on draw is the anti-runaway mechanism); draw/redirect clamped to available food (no sub-zero).
- Calibration is capacity-RELATIVE (no false fixed anchor); the two fractions (delivery 0.08, draw 0.06) are boot-tuned via the LOG_state dump — mechanic ships fully wired.
- Famine gates + pct-derive guarded on `has_variable + cap > 0` (divide-safety + first-tick safety; NOT moved-capital detection — labelled honestly per MED-1).
- Zero `qing_grain_reserve` references remain (grep-verified) before commit.
- `LOG_state` (not a `value=` LOG_line) carries the numeric instrumentation (se_LOG.txt:77-82); no `$`/`#` in any msg string.

## 8e. SLICE 4 — IMPLEMENTATION SPEC (2026-08-09) — #95 depots' 食-share DISPLAY on the Works panel

§8b re-sequence step 4, rides on slice 3's real-food delivery. **DISPLAY ONLY — no new mechanic number.**
The design's iron constraint (§4 + §8b CONFIRMED "no-double-count"): depots feed delivery ONLY through
`qing_canal_condition` (each 漕運倉 lifts the condition target +8, cap +24 at 3 depots —
`QING_canal_update_condition` se_QING_CANAL.txt:84-91). There is NO additive `delivery += depot×D` term and
this slice adds none — it merely *attributes* a share of the real-food tribute already delivered in slice 3.

### Derivation (honest attribution, weak-sense "exact")
- **`qing_canal_grain_shipped`** (ROOT/CHI) = the actual food delivered to the capital state this quarter =
  the headroom-clamped `qing_cap_deliver_tmp` (mirrored inside the existing `ROOT = { … }` block in
  `QING_canal_run_grain_balance`, alongside the food/cap mirror, BEFORE its `remove_variable`). A useful
  real-food number in its own right (this quarter's 漕糧 tribute).
- **`qing_canal_depot_grain`** (ROOT/CHI) = the portion of that tribute attributable to the depots =
  `shipped × (depot condition-points ÷ total condition)`, where depot condition-points = `min(depot_count×8, 24)`
  (the exact contribution `QING_canal_update_condition` credits them). Computed in ROOT scope AFTER the
  `capital_scope.state` block. Guards: only when `condition > 0` and `depot_count > 0` (else 0); the share
  fraction is clamped to `≤ 1.0` (corruption can drift condition below the depot points, which would
  otherwise attribute >100% — clamp keeps depot_grain ≤ shipped). All comparisons are var-vs-literal (bare
  legal); `divide = var:qing_canal_condition` / `multiply = var:…share…` are value-field var reads (legal,
  cf. :172). No new `_cmpsvalue` operand needed.

### Files touched (slice 4)
- `se_QING_CANAL.txt` — mirror `qing_canal_grain_shipped` in the ROOT block; add the depot-share compute block
  after the `capital_scope.state` if. Two new ROOT vars; two scratch temps (`_depotpts_tmp`, `_depotshare_tmp`)
  removed in-block.
- `gui/qing_works_ministry.gui` — one display row under the Capital Grain Reserve bar: label +
  `[…qing_canal_depot_grain…|0] / […qing_canal_grain_shipped…|0]` (depot food out of total tribute shipped).
- `localization/english/qing_works_ministry_l_english.yml` (BOM) — `QING_WORKS_MINISTRY_DEPOT_GRAIN_LABEL` + `_TT`.

### Invariants (applied-diff review)
- NO additive delivery term (grep the delivery block: unchanged); depot_grain is purely derived from
  already-shipped grain. Double-count impossible.
- Divide-by-zero guarded (`condition > 0`); depot_grain defaults 0 (no depots / never-ran); share clamped ≤ 1.0.
- Braces balanced; se_QING_CANAL no-BOM/LF, loc keeps BOM; no EOL churn.
- The STRONG per-depot split-delivery rebalance (remove condition depot-bonus, add direct per-depot delivery)
  remains DEFERRED with user-flag per §4 — this slice is the weak/through-condition form the design locked.

## 8f. SLICE 5 — IMPLEMENTATION SPEC (2026-08-09) — the abstract-granary lever concretization (design premise CORRECTED)

§8b re-sequence step 5 ("qing_granary_stock retirement — the risky slice"). **The literal premise is STALE and
NOT executed; the genuine concretization it was reaching for IS built whole.** Grounded byte-level + git (note:
`rg`'s rendered output corrupts `qing_granary_stock` → `n`, a display artifact — only Python/git reads trusted).

### Why "retire qing_granary_stock" is a stale no-op (source proof, NOT a deferral)
- `qing_granary_stock` is NOT an abstract counter like the retired `qing_grain_reserve`. Commit `51957efaf1`
  (2026-07-13) already converted it to a **derived real-food cache**: `qing_granary_food × 100 / capacity`
  when cap>0, held at the DECLINE_init baseline 30 while cap==0 (se_QING_DECLINE.txt:2493-2497; the block
  comment at :2352 states "KEPT: now DERIVED = qing_granary_food / cap * 100"). Pool A (`qing_granary_food` +
  `qing_granary_capacity`) is ALREADY the single source of truth; `qing_granary_stock` is its 0..100 projection.
- Deleting it and inlining `food/capacity` into the consumers is (a) **infeasible** in the boolean event
  `trigger = {}` blocks that read it (`qing_decline.11/.12` option-triggers `>= 20`; `qing_pop_press` event
  trigger `<= 15` — a trigger block has no precompute step for a divide), and (b) would force the granaryless
  cap==0→30 guard to be re-implemented at every one of the ~9 read sites, replacing ONE central guarded derive
  with nine scattered ones. That is de-refactoring, not concretization — it makes the code worse. NOT DONE.

### The real defect (this IS the concretization program — "concrete over abstract")
Three player levers write the DERIVED CACHE, not the underlying real food, so the 180-day pool sweep silently
reverts them — the player pays but no real grain is stored/spent:
- `QING_granary_invest` (¥360 button, se_QING_MECHANICS.txt:94) — `nudge qing_granary_stock +25`
- `QING_granary_release` (famine-relief option, :105) — `nudge qing_granary_stock -20`
- `QING_pop_relief_resettle` (¥310 lever, se_QING_POPULATION.txt:234) — `nudge qing_granary_stock +20`
The only correct real-food lever today is `se_QING_REVENUE.txt:512-513` (`change_variable qing_granary_food add`).

### Fix (whole, buildable now)
1. **Extract the pool's clamp+derive tail (se_QING_DECLINE.txt:2490-2506) into a shared, self-contained helper
   `QING_DECLINE_granary_rederive`** (recompute cap_tmp = count×200, clamp food [0,cap], derive stock if cap>0,
   set capacity, remove cap_tmp). Behaviour-identical to the inline it replaces. Called at the pool tail AND by
   each lever, so a lever's real-food change is reflected in the cache IMMEDIATELY (not lost until the next sweep).
2. **Convert the three nudges to real-food changes** via the proven REVENUE idiom (guard-init `qing_granary_food`
   then `change_variable add/subtract`), followed by `QING_DECLINE_granary_rederive = yes`:
   - invest: `+200` real food (a solid ¥360 stocking; cf. REVENUE seeds +600 across ~3 granaries)
   - release: `−150` real food (clamped ≥0 by the rederive)
   - relief: `+150` real food
   Magnitudes are boot-tunable knobs comparable to the old ±20-25 index points at a typical 2-3-granary cap
   (400-600). All other lever effects (sect-pressure nudges, stability, the qing_granary_stocked/famine_relief
   modifiers, the frontier pull) are PRESERVED unchanged — only the stock→food write is concretized.
3. **Granaryless honesty:** if cap==0 (no granaries) the rederive clamps stored food to 0 — you cannot stock an
   ever-normal reserve you have not built. The invest button's fuller market-price BUY rework is **task #18's**
   explicit domain (a separately-tracked task, NOT a deferral of this slice); slice 5 only stops the phantom-cache
   write. The stocked-modifier gate (`stock >= 40`) now reads the honestly-rederived value.

### Files touched (slice 5)
- `se_QING_DECLINE.txt` — new `QING_DECLINE_granary_rederive` helper; pool tail calls it (identical behaviour).
- `se_QING_MECHANICS.txt` — invest + release: real-food change + rederive (was a stock nudge).
- `se_QING_POPULATION.txt` — relief: real-food change + rederive.
- Loc: invest tooltip reworded from "builds granary stock" to real grain bought into the ever-normal reserve.

### Invariants (applied-diff review)
- `qing_granary_stock` is NOT deleted (it is the derived cache every reader + GUI uses); no reader changes.
- Helper is behaviour-identical to the pool tail it extracts (same clamp, same cap==0→baseline-30 hold, same
  `qing_granary_cap_tmp_cmpsvalue` RHS which already exists at 00_event_values.txt:1876).
- `add`/`subtract` on `qing_granary_food` are value-field ops (legal); no new comparison-RHS operands.
- Levers guard-init `qing_granary_food` before changing (a lever may fire before the first pool sweep).
- Braces balanced; se_ files no-BOM/LF; loc keeps BOM; no EOL churn.

## 8g. SLICE 6 — IMPLEMENTATION SPEC (2026-08-09) — canal condition DERIVED from per-corridor coverage

§8b re-sequence step 6 — the FINAL slice of Task #7 (#94/#95). §5(ii): replace the empire-wide
depot/dike *sum* feeding the condition target with PER-CORRIDOR coverage, so a gap in one stretch
silts that segment regardless of over-building elsewhere. This is the "bigger rework, its own reviewed
slice" §5(ii) named.

### The defect it fixes
`QING_canal_update_condition` (se_QING_CANAL.txt:84-99) derives the condition target from the
EMPIRE-WIDE tallies `qing_depot_count` / `qing_dike_count`: `+8 per depot (cap +24 at 3)`, `+6 per dike
(cap +18 at 3)`. Two flaws:
1. **Position-blind.** Three depots all in Jiangsu score identically to one depot in each of three
   different stretches — yet the canal is a SERIAL artery: grain that reaches Yangzhou still has to
   cross a silted Shandong stretch to reach Beijing. A gap anywhere throttles the whole line.
2. **The cap is unreachable by design.** Only TWO depots are seeded at 1763 (Yangzhou/Jiangsu +
   Tianjin/Zhili) and the depot building is seed-only (`potential = always no`; only the Works panel's
   build route adds more, into the single highest-pop province). So `qing_depot_count` is pinned at 2
   for most games → +16, never the +24 cap. The "diminishing 2nd/3rd depot" story (:81) is inert.

### The geography (VERIFIED — area→region join, this session)
Grand Canal corridor, south→north (the serial stretches grain transits):
| Region   | 1763 depot seed            | Yellow-River dike seed        |
|----------|----------------------------|-------------------------------|
| Zhejiang | — (Haining is a 海塘 seawall)| Haining seawall (NOT R. dike) |
| Jiangsu  | **Yangzhou 揚州** (P3208)   | —                             |
| Shandong | —                          | **Jinan 濟南** (P6485)         |
| Zhili    | **Tianjin 天津** (P3783)    | —                             |
| Henan    | (off the canal; feeds R.)  | **Kaifeng+Zhengzhou** (P4931/8622) |

- Canal-corridor coverage = the 4 stretches **Zhejiang, Jiangsu, Shandong, Zhili** — the provinces the
  tribute barges actually transit between the Yangtze delta and Beijing. (Anhui is a grain-QUOTA source,
  handled by `QING_canal_compute_jiangnan_quota`; it is NOT on the trunk canal, so it is NOT a corridor
  stretch here.)
- Yellow-River dike coverage = the crossing regions **Henan + Shandong** (where the river threatens the
  canal). Haining/Zhejiang is a coastal 海塘 seawall, so a Zhejiang dike does NOT count as river-crossing
  protection — the position-awareness the slice is *for*.

### The new derivation (replaces se_QING_CANAL.txt:84-99, term (canal depots) + term (dikes))
Two helper effects tally COVERED stretches, not raw buildings; each covered stretch is worth a fixed
band. All O(owned) `any_owned_province` short-circuit tests (proven idiom + scope:
qing_settle_frontier_missions.txt:277 `any_owned_province = { is_in_region = X NOT = has_building = Y }`;
`is_in_region` province-scope proven se_QING_CANAL.txt:214 / 00_tradezone_triggers.txt:388).

**Depot corridor coverage → target contribution (replaces the flat +8×count/cap+24):**
```
qing_canal_depot_corridors = 0
for each of { Zhejiang Jiangsu Shandong Zhili }:
    if any_owned_province in that region has_building qing_canal_depot_building:  += 1   # 0..4
target += qing_canal_depot_corridors × 6      # 0..24 — SAME +24 ceiling, but now needs SPREAD, not stacking
```
At 1763: Jiangsu ✔ + Zhili ✔ = 2 corridors → +12 (vs the old +16 for count=2). The player raising a
depot in the empty **Shandong** stretch now lifts the target where it matters; a 4th in already-covered
Jiangsu does nothing — exactly the position story §5(ii) asks for. Ceiling +24 preserved so the
Works-perf fold (term d) and the drift band are undisturbed at full coverage.

**Yellow-River dike coverage → target contribution (replaces the flat +6×count/cap+18):**
```
qing_canal_dike_regions = 0
for each of { Henan Shandong }:
    if any_owned_province in that region has_building qing_dike_building:  += 1           # 0..2
target += qing_canal_dike_regions × 9          # 0..18 — SAME +18 ceiling across the 2 crossing regions
```
At 1763: Henan ✔ + Shandong ✔ = 2 → +18 (the old count=3 cap). NOTE (design-review LOW): FOUR
`qing_dike_building` seeds actually exist — Kaifeng+Zhengzhou (Henan), Jinan (Shandong), AND Haining
(Zhejiang, se_QING_BUILDINGS.txt:332), so empire-wide `qing_dike_count` = 4 at start, not 3. The Haining
seed is a 海塘 SEAWALL modelled with the dike building; slice-6 condition correctly counts REGIONS (Henan +
Shandong), so it excludes Haining/Zhejiang from river-crossing protection — full protection at the 1763
zenith across the two crossing regions. A region breached and lost (Taiping-era Henan) drops the river
protection concretely. SEMANTIC-SPLIT note: the flood MTTH (se_QING_DECLINE.txt:2315) still reads the
empire-wide `qing_dike_count` (which includes the Haining seawall), so a Zhejiang seawall raises flood
protection there but not canal condition — pre-existing, #115's domain, deliberately NOT reconciled here.

### What is PRESERVED (unchanged — verified against every consumer)
- **`qing_depot_count` / `qing_dike_count` STILL tallied** empire-wide by the Works sweep
  (se_QING_MINISTRY.txt:639-640) — they have OTHER consumers this slice must NOT disturb:
  the Works panel GUI (`qing_works_ministry.gui:325/331`, the raw building counts shown) and the
  Yellow-River flood MTTH (`se_QING_DECLINE.txt:2315-2318`, `qing_dike_count >= 3 / = 2 / = 0`). Slice 6
  only changes how *condition* reads geography; it does not retire the counts. (A later, out-of-scope
  polish could make the flood MTTH per-region too — explicitly NOT this slice; the flood model is #115's
  domain and already shipped.)
- **The qing_canal.2 gate (`condition < 45`)** and the **Works-perf fold** (se_QING_MINISTRY.txt:697,
  `condition − 60 /4`) read `qing_canal_condition` unchanged — they see the same 0..100 meter, now driven
  by a position-aware target. No gate rewire.
- **Slice-4 depot 食-share DISPLAY** (se_QING_CANAL.txt:246-266) reads `min(qing_depot_count×8, 24)` to
  attribute the depots' share of shipped grain. THIS IS A SEAM: the display's "depot condition-points"
  term (`depot×8 cap 24`) was written to mirror the OLD condition credit. Slice 6 changes the credit to
  `corridors×6 cap 24`. **FIX (in-scope, not a deferral):** re-point the display's depot-points term to
  the new basis `qing_canal_depot_corridors × 6` (same 0..24 range) so the attribution stays honest and
  no-double-count holds (depots still feed delivery ONLY through condition). The share denominator
  (condition) is unchanged.

### Files touched (slice 6)
| File | Change |
|---|---|
| `se_QING_CANAL.txt` | replace the two flat count→target blocks (:84-99) with two per-corridor coverage tallies + fixed band; re-point the slice-4 display depot-points term to `corridors×6`; update the header comment |
| (no new operands) | all new vars are LHS or value-field reads; the drift compare still uses the existing `qing_canal_cond_target_cmpsvalue` (:1860) — unchanged |

### Invariants / traps checked
- **RHS-comparison rule:** the only var-vs-var comparison in the effect is the drift step
  (`var:qing_canal_condition < qing_canal_cond_target_cmpsvalue`, :135/139) — UNCHANGED, operand exists at
  00_event_values.txt:1860. The new `any_owned_province = { is_in_region = X has_building = Y }` are
  TRIGGERS (limit blocks), not comparisons; the `+= band` uses `change_variable add = <literal>`
  (value-field, legal). No new `_cmpsvalue` needed.
- **`is_in_region` scope:** province-scope trigger, used INSIDE `any_owned_province` (province scope) —
  correct (proven se_QING_CANAL.txt:214, :319-330 already do exactly this for the Jiangnan quota).
- **Ceilings preserved:** depot band ceiling +24 (4×6), dike band ceiling +18 (2×9) — identical to the
  old caps, so the target's full-coverage maximum and thus the Works-perf fold + drift band are
  unchanged at the healthy end. Only the PATH to the ceiling changes (spread, not stack).
- **Scratch var hygiene — CORRECTED (design-review CRITICAL, 2026-08-09):** `qing_canal_depot_corridors`
  MUST **PERSIST**, NOT be removed. The re-pointed slice-4 display (in `QING_canal_run_grain_balance`) reads
  it, and that effect runs AFTER `QING_canal_update_condition` in the same tick (`QING_canal_quarterly_tick`
  :353→:354). Removing it in update_condition would leave the display's `has_variable` guard false → the
  depot 食-share row reads 0 forever (silent failure). It is re-`set_variable`'d fresh at the top of
  update_condition every pulse, so it never goes stale — persisting is safe and correct. `qing_canal_dike_regions`
  has no cross-effect consumer, so it is added to the target then `remove_variable`'d at the tail (safe).
- **1763 zenith sanity:** depot 2 corridors (+12) + dike 2 regions (+18) + baseline 40 + filled office +
  minister finesse − corruption drift = a high-but-not-maxed condition, consistent with the current
  seed=80 and the "canal sound at the zenith" contract. The drift meter eases there over the first years.
- Braces balanced; se_QING_CANAL.txt stays no-BOM/LF; no loc/GUI change (the GUI still shows the raw
  `qing_depot_count`/`qing_dike_count`, which remain accurate empire-wide tallies).

### Rejected alternatives (logged per no-deferral rule)
- **Per-PROVINCE serial-bottleneck model** (multiply stretch conditions so the worst stretch dominates):
  truer to a serial artery, but needs per-stretch condition state + a product idiom with no precedent, and
  risks a zero-stretch zeroing the whole line (too punishing vs the current additive band). REJECTED as
  over-engineering for a 0..100 abstraction; the additive per-corridor band already delivers the
  position-awareness §5(ii) asks for.
- **Retire `qing_depot_count`/`qing_dike_count` entirely**, driving GUI + flood MTTH off the corridor
  tallies too: expands blast radius into #115's shipped flood model for no gain to THIS slice's goal.
  REJECTED — keep the empire-wide counts for their existing consumers; scope slice 6 to the condition
  derivation only.

## 9. Superseded (record)
- v1: rescale qing_grain_reserve to bespoke 石 — REJECTED (invents a parallel scale).
- v2 Plan 2: sibling 食-pool mirroring pool A's units but not its add_state_food mechanism — REJECTED by
  review + user (mimics units ≠ plugs into the mechanism; also no countable capacity anchor).

## 10. Evidence files
- `se_QING_DECLINE.txt:2366-2510` (pool A); `se_QING_CANAL.txt:51-62,71-141,150-195,257-340` (reserve+condition+
  famine consumers+payloads); `common/buildings/qing_granary_buildings.txt`, `qing_agriculture_buildings.txt`
  (food_capacity), `qing_works_buildings.txt:36-75` (depot); `se_QING_MINISTRY.txt:603-640,697` (tallies+perf);
  `gui/qing_works_ministry.gui`; `events/…/qing_canal_events.txt`; `research/QING_GRANARY_CAPACITIES.md`.
