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

## 9. Superseded (record)
- v1: rescale qing_grain_reserve to bespoke 石 — REJECTED (invents a parallel scale).
- v2 Plan 2: sibling 食-pool mirroring pool A's units but not its add_state_food mechanism — REJECTED by
  review + user (mimics units ≠ plugs into the mechanism; also no countable capacity anchor).

## 10. Evidence files
- `se_QING_DECLINE.txt:2366-2510` (pool A); `se_QING_CANAL.txt:51-62,71-141,150-195,257-340` (reserve+condition+
  famine consumers+payloads); `common/buildings/qing_granary_buildings.txt`, `qing_agriculture_buildings.txt`
  (food_capacity), `qing_works_buildings.txt:36-75` (depot); `se_QING_MINISTRY.txt:603-640,697` (tallies+perf);
  `gui/qing_works_ministry.gui`; `events/…/qing_canal_events.txt`; `research/QING_GRANARY_CAPACITIES.md`.
