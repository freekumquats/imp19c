# DESIGN — Organic New World Crop Diffusion (task #384)

Status: SPEC ONLY (not yet built). Deferred behind finishing the known boot-test bugs.
Branch: 1763_bookmark. Author decision date: 2026-07-11.

## Why this exists
The #64/#78 New World crop system is a **static seed + colonization-arc conversion**, and
organic time-based diffusion was *explicitly decided against* (OVERNIGHT_DECISIONS.md:77 —
"#120 is JUST a map mode reading that state — NO new diffusion mechanic"). The user has now
**reversed that decision**: maize/sweet_potato/peanut/chili spread organically through the SW
China hill country across the 18th c. (Ho Ping-ti; Columbian Exchange via Manila galleon), so
the crop set should GROW over a playthrough, and the New World Crops report (#120) should
surface that live spread — not a frozen list.

## What already exists (reuse, don't rebuild)
- **Static seed**: 28 provinces in `common/province_setup.csv` → now also written into the
  loaded `setup/provinces/*.txt` (BT-23 fix — the CSV is only a generator INPUT; the game loads
  the .txt; 43% CSV↔txt drift means NO full regen). ~10 Qing-owned crop provinces at 1763.
- **`qing_migration.20`** (events/imp19c_mod_events/qing_frontier_migration_events.txt:157) —
  "New World Crops Arrive" Columbian-Exchange event. Sets `qing_newworld_crops = 1`. THE ARRIVAL GATE.
- **`QING_COLON_apply_nwcrop_capacity`** (se_QING_COLON.txt:269) — idempotent GLOBAL sweep:
  stamps/removes the `qing_nwcrop_abundance` (local_population_capacity=8) modifier on every
  province that grows one of {maize, sweet_potato, potato, peanut, chili}. Re-run after any spread.
- **`QING_COLON_spread_newworld_crops`** (se_QING_COLON.txt:336) — colonization-arc-gated
  conversion of ≤3 marginal (livestock/wood, NEVER grain) provinces to sweet_potato. Keep as-is.

## The model — REUSE the proven PULL/PUSH sphere diffusion (se_QING_SPHERE.txt)
The sphere pulse (#307/#165) is the template. Its two-pass idiom is PROVEN and exactly the
shape crop spread needs:
- **PASS 1 SNAPSHOT** (`QING_sphere_snapshot_state`): freeze each state's scores into `*_snap`
  vars BEFORE any mutation, so pass 2 reads stable, order-independent values.
- **PASS 2 BLEED** (`QING_sphere_bleed_one_power`): walk `every_state_province →
  every_neighbor_province → state`, accumulate a running max of neighbours' snapshots onto a
  PERSISTENT temp var on a SAVED source scope (persistent-var arithmetic is the proven idiom;
  local_var arithmetic with var: operands is NOT), then close a fraction of the gap.
- Self-throttled to ~yearly via own 365-day cooldown var; called from the quarterly pulse in
  `common/on_action/00_monthly_country.txt` right after `QING_sphere_pulse = yes`.

### Crop mapping (PUSH source + PULL neighbour)
- **PUSH source** = a province ALREADY growing a NW crop (trade_goods ∈ crop set).
- **PULL target** = a MARGINAL neighbour eligible to adopt: `owner = CHI` (or CHI subject —
  decide; sphere bleeds across borders, but crops should probably stay on Qing soil first),
  `is_sea = no`, `total_population > 0`, and trade_goods ∈ {livestock, wood, and other
  non-staple low-value goods} — **NEVER grain / rice / wheat** (preserve the breadbasket, same
  rule QING_COLON_spread_newworld_crops enforces).
- **Diffusion rule**: for each eligible target province, count adjacent crop-source provinces
  (walk neighbours, tally). Convert with a probability that scales with that count (more crop
  neighbours → faster adoption), gated behind `qing_newworld_crops = 1` (arrival). Adopt the
  MOST COMMON crop among its crop neighbours (mirrors the sphere "pull toward strongest adjacent"
  — here "adopt the dominant adjacent crop"). Use `random`/`random_list` with a chance for the
  probabilistic flip (VERIFY this is a proven idiom in se_QING_ETHNIC_TENSION / decline first —
  neither file currently uses `random =` inside these pulses, so confirm the idiom before use).
- After any conversions this pulse: call `QING_COLON_apply_nwcrop_capacity = yes` so newly-
  converted provinces get the capacity lift.
- **Conservative rate**: cap conversions per pulse (e.g. ≤2–3 nationwide per year) so the world
  food supply is not rebalanced — same caution as the existing accelerator.

### Two-pass to avoid mid-iteration feedback
Like the sphere: PASS 1 mark/snapshot which provinces are crop sources this pulse (freeze into a
per-province `nwcrop_source_snap` flag/var); PASS 2 evaluate each candidate against the FROZEN
sources, so a province converted this pulse does not immediately seed its own neighbours in the
same pass (order-independence).

## Surfacing in the report (#120 New World Crops report)
- The report already lists provinces growing a NW crop (BT-23 fixed the seed so the list is
  non-empty). ADD: a spread indicator — e.g. count of provinces that adopted a crop in the last
  pulse/year (a `qing_nwcrop_spread_last_year` counter set by the pulse), and/or a per-province
  "newly adopted" marker. Mirror the trend-arrow idiom being added to the tension/sinicization
  reports (snapshot prev → show delta). Keep read-only.

## Idioms / gotchas to respect
- se_LOG (LOG_enter/exit/line/fail) on every path; NO macro `$param$` or `#` inside LOG strings.
- `every_neighbor_province` is proven in an effect (se_QING_SPHERE.txt:105/349, se_AI.txt).
- Persistent-var arithmetic on a SAVED scope for cross-province accumulation; not local_var.
- se_QING_COLON.txt is UTF-8 (no BOM), LF, brace-balanced — preserve on edit.
- Oracle-check (TI + Invictus) the probabilistic-conversion idiom + any unproven accessor before building.

## Related
Task #384 (this). Report enhancement pairs with #385 (sinicization rate-of-change) and the
tension trend indicator (both use the snapshot-prev → delta pattern). Memory:
imp19c-sphere-idioms-oracle (the PULL neighbour-bleed idiom), imp19c-economy-mechanics.
