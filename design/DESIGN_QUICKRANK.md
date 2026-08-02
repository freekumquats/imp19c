# Quickrank — wiring the internal-supplier ranking into the live trade path (#393)

Branch: **trade_fix**. High-caution task — this changes the live quarterly trade simulation
(runs every governorship × every tradegood). All major decisions, risks, and estimated in-game
effects are logged here as work proceeds.

## The situation (as found)

The mod's internal trade uses a **supplier-ranking** scheme: for each governorship + tradegood,
rank the accessible internal trade-zones (TZs) as suppliers, awarding
`1st_rank_internal_supplier_<good>` … `6th_rank_internal_supplier_<good>` vars on the ranking
governorship. The live purchase loop then walks those ranks and pulls stock from each in turn.

**The gap (documented by #340):** the live path
`PURCHASE_make_internal_shopping_list → PURCHASE_check_shopping_internal` (wired at
events/economy/trade.txt:175) calls `PURCHASE_get_preferred_tradezone_internal` (se_PURCHASE.txt:655)
to produce those rank vars — but that effect is a **behaviour-preserving empty no-op STUB**
(#340 defined it empty to kill ~68 "Unknown effect" load errors after upstream reverted its WiP
trade framework, commit b60906d1). Because the stub sets no rank vars, `PURCHASE_order_internal`
finds no ranked supplier → **no internal order is ever placed**. That is the current live economy:
internal inter-TZ trade is effectively OFF; provinces rely on their own stockpile + external orders.

The **working ranking logic still exists** but is unwired: `wip_quicktraderank.txt:500`
`PURCHASE_get_preferred_tradezone_internal_quickrank` (governorship scope; args `$tradegood$`,
`$order_size$`). It scores every accessible TZ by `order_size × local_price + route.connection_time`
(negated → cheaper+closer = higher), sorts via `ordered_in_list … order_by … max=3`, and awards
`1st..6th_rank_internal_supplier_<good>` on `scope:ranking_governorship`. Single-TZ fast path:
awards 1st = own trade_center.

**#393 = replace the stub body with (a call to) the proven quickrank logic**, making internal
supplier ranking actually fire. This is a deliberate ECONOMY BEHAVIOUR CHANGE, exactly the
follow-on #340's own comment (se_PURCHASE.txt:645-650) points to.

## Open questions being verified before ANY edit
- Q1. Does the quickrank effect's scope/args EXACTLY match the live call site (governorship scope,
  `tradegood` + `order_size`)? — the stub is called at check_shopping_internal:399 with exactly
  `{ tradegood = $tradegood$  order_size = scope:purchaser_governorship.var:l_order_size }`. ✅ matches.
- Q2. Does the quickrank logic depend on route/TZ setup that is actually initialized in the live
  game? It reads `global_routes_list`, `var:origin_TZ.connection_time`, `internal_trade_scope`,
  `num_TZ_in_ITS`, `list_of_tradezones_in_internal_trade_scope`. `TRADE_setup_routes` IS called at
  oa_economy_setup.txt:112. — VERIFYING these are all populated at runtime.
- Q3. Does `PURCHASE_order_internal` (the consumer) correctly read the rank vars the quickrank sets,
  and does its loop terminate? (check_shopping_internal_pre_ranked wraps it in a
  `while TZs_tried < num_TZ_in_ITS` — the live check_shopping_internal calls it once.)
- Q4. Cost/perf: quickrank does `every_trade_center` + `ordered_in_list` per (governorship,good).
  Estimate the added cost vs today's no-op.

## VERIFIED FINDINGS (exploration + hand-checked against on_actions)

**F1 — The entire internal-purchase chain is DEAD at runtime.** The stub #393 targets
(`PURCHASE_get_preferred_tradezone_internal`) is reached only via
`PURCHASE_make_internal_shopping_list → PURCHASE_check_shopping_internal`, whose ONLY caller is
event **`trade.2`**, which is commented `# trade.2 # Defunct` at its sole on_action site
(oa_wealth_changes.txt:211). Confirmed: `trade.2` fires nowhere uncommented; the stub's only
"callers" are comment lines. The LIVE `quarterly_trade_pulse` (oa_wealth_changes.txt:138) instead
chains the **GLOBALTRADE split** path (`quarterly_global_trade_food/luxury/3..6 → GT_split_*`,
se_GLOBALTRADE_split.txt), which never touches the PURCHASE internal chain or the
`*_rank_internal_supplier_*` vars at all. → Swapping the stub for quickrank changes NOTHING
observable unless `trade.2` (or an equivalent) is also re-enabled into the live pulse.

**F2 — quickrank IS scope/dep-compatible** (if the chain were live): it awards
`Nth_rank_internal_supplier_<good>` on `scope:ranking_governorship`, exactly what the consumer
`PURCHASE_order_internal` reads; and its runtime deps (`internal_trade_scope`, ITS TZ list,
`global_routes_list`+`connection_time` from `TRADE_setup_routes` @ oa_economy_setup:112,
`trade_center`, `local_price_<good>`) are all genuinely set up at game start.

**F3 — Latent bugs that would bite the moment the chain went live:**
- Rank-var RESET (`TRADE_reset_TZ_internal_rankings`, se_TRADE.txt:469) clears only ranks **1–3**
  (nested-if, comment "purely concept at the moment") and is NOT called from the live pulse.
  quickrank awards up to **6th** → ranks 4–6 leak across quarters (stale suppliers).
- `PURCHASE_try_supplier_quickrank` (wip:706) hardcodes `tradezone = india` (author TODO
  "Can we improve this somehow?") — WiP, and NOT the one the live consumer uses anyway
  (`PURCHASE_order_internal` calls `PURCHASE_try_supplier`, not the _quickrank twin).
- `global_routes_list` is built once at game start, never rebuilt on territory change (only
  connection_time refreshes) — new trade centers may lack routes.
- quickrank `connection_time` scoring carries unfinished author TODOs (scale "Make 0.01",
  "Check if this is what it's called").

## DECISION — STOP AND SURFACE (do not bulldoze)

The one-line task "wire quickrank into the live trade path" is, on inspection, NOT a one-effect
swap. The live trade path is the GLOBALTRADE-split architecture; the whole
PURCHASE-internal/supplier-rank subsystem (quickrank included) was reverted to dormancy by upstream
(commit b60906d1 "Reverted to original trade ranking method") and is dead code. Genuinely "wiring
it into the live path" would mean either (a) re-enabling defunct `trade.2` and running the old
per-governorship internal-purchase loop ALONGSIDE the live GLOBALTRADE split — i.e. resurrecting a
whole parallel, upstream-abandoned trade engine — or (b) porting supplier-ranking INTO the
GLOBALTRADE split. Both are large, economy-reshaping, and would ship known-WiP code (F3) into the
live sim. That is a scope + risk call the user must make, per the "great caution" directive — not
something to commit autonomously. **No code changed. Surfaced to user with options (below).**

## Does the LIVE GLOBALTRADE-split already do what quickrank would? — YES, and more

Read se_GLOBALTRADE_split.txt (5900 lines; orchestrator GT_split_do_global_trade_split:1). The live
system does the SAME JOB quickrank was reaching for — matching demand to supply across trade zones —
but by a fundamentally different, superior method:

- **quickrank (dead):** a per-(governorship × good) SEARCH. For each buyer it scores every reachable
  TZ (price + route connection_time), ranks the top ~6 suppliers, then pulls stock rank-by-rank.
  A greedy nearest-cheapest-supplier picker. O(buyers × TZs) each quarter.
- **GLOBALTRADE-split (live):** a POOL-and-DISTRIBUTE market clearing. Every governorship declares its
  sell-stockpile into its TZ (GT_split_declare_sell_to_TZ_aggregate_stockpile) and its buy-orders
  (GT_split_create_order); the system sums a global/customs-union stockpile, computes global + per-
  country import unit prices and market-penetration + order-size modifiers, then SCALES all orders and
  payment pools to what's actually fulfillable, distributes income/expenses, applies shipping costs,
  and books amount-exported/imported per good. It clears the whole market simultaneously with real
  price formation, shipping, tariffs/customs unions, and proportional fulfilment.

So GLOBALTRADE-split SUPERSEDES quickrank: it already moves goods between zones to meet demand (the
thing quickrank+PURCHASE_order_internal was built to do), and additionally models price discovery,
customs unions, market penetration, shipping traffic/costs, and pro-rata order scaling — none of which
the quickrank/PURCHASE path had. This is why upstream reverted the PURCHASE-internal path to dormancy
(commit b60906d1): it was replaced, not merely paused. Re-activating quickrank alongside the split
would DOUBLE-COUNT internal trade (goods bought twice) or fight the split's clearing — a regression.

CONCLUSION: quickrank is not a missing feature — it is superseded dead code. "Wiring it into the live
path" as a real activation would REGRESS the economy. The only non-harmful reading of #393 is Option 1
(un-stub for code-completeness, behaviour-inert) or Option 3 (defer/leave dead).

## Options put to the user
1. **Swap the stub only** (populate `PURCHASE_get_preferred_tradezone_internal` with the quickrank
   body). Behaviour-inert TODAY (chain is dead), but readies it + removes the "reverted" gap.
   Lowest risk; also fix the F3 rank-reset (extend to 6) so it's correct if ever activated.
2. **Swap + re-enable `trade.2`** into the live quarterly pulse (make internal supplier trade
   actually run). Real economy change; must first fix F3 (reset 4-6, route-rebuild) and validate
   perf (every governorship × every good, per quarter). Needs a boot/perf test.
3. **Defer** — record findings, leave dead code dead (upstream deliberately reverted it).

## FINAL DECISION (user-approved): OPTION 3 — DEFER, leave dead code dormant

Rationale (confirmed with user): enabling quickrank delivers NO meaningful gameplay benefit and is a
net negative. Its entire payoff (deficit provinces supplied from surplus zones) is ALREADY delivered
by the live GLOBALTRADE-split, which additionally models price formation, customs unions, shipping,
and pro-rata fulfilment. Running quickrank alongside the split would DOUBLE-COUNT internal trade
(inflated stockpiles, mispriced markets, double-spent wealth) and would ship known-WiP code into the
hot per-(gov×good) quarterly loop (rank-reset covers only 1-3; routes never rebuilt; india hardcode;
unfinished scoring TODOs). Upstream already replaced this path deliberately (b60906d1). Upside ~0,
downside real → do not activate.

ACTION TAKEN: no code changed. The stub PURCHASE_get_preferred_tradezone_internal stays an inert no-op
(as #340 left it, load-error-clean). #393 closed as "won't-do / superseded" — documented here.

## Estimated in-game effects (per option)
- **Option 1:** zero runtime change now (dead chain). Removes the dormant-code gap; safe.
- **Option 2 (if activated):** provinces short of a good would pull from the cheapest+closest
  internal trade-zone with stock, instead of only their own stockpile + external market. Likely
  effects: fuller stockpiles inland, less reliance on external imports, lower prices in
  well-connected core zones, redistribution toward deficit provinces. RISKS: perf cost of the
  per-(gov×good) scoring loop each quarter; stale ranks 4-6 (F3) could route to a drained/wrong TZ;
  double-counting if it runs alongside the GLOBALTRADE split rather than replacing part of it.
  Magnitude un-estimable without a boot test — this is why it needs one.
- **Option 3:** no change.

---

# Employment & Wages — gap analysis + fix (follow-on, same branch)

Branch: **trade_fix**. Same "great caution" + record-decisions directive. The task:
"explore the existing gaps with employment and wages and implement the fix / build out
the feature." Analysis below, then the implemented fix.

## What is LIVE and working (do not touch)

- **Wages are paid every quarter.** `oa_wealth_changes.txt:171 WEALTH_pay_wages_all_countries`
  → per governorship: `WEALTH_calculate_all_wages` sets `WEALTH_wages_due_<category>` =
  (filled building job slots in that category) × `WEALTH_average_wage_wealth_value`, then
  `WEALTH_pay_wages` credits `proletariat_wealth` / `middle_strata_wealth` /
  `upper_strata_wealth` pools. Categories: administrators, educators, infrastructure_workers,
  military, resource_gatherer, industrial_workers, commercial (JOBS_svalues.txt).
- **Cost of living is booked** as an expense in `WEALTH_expenses_total_<strata>`
  (WEALTH_svalues.txt) so the wage income nets against living costs in the per-capita
  wealth pools. (Note: `WEALTH_subtract_cost_of_living_all_governorships` in
  se_ECON_wealth.txt is NOT called from any on_action — but COL is instead captured via
  the expenses svalues, so this is redundant/dead, not a missing deduction. Left as-is.)
- **Unemployment already drives migration.** `MIGRATION_push_province` adds
  `JOBS_unemployed_pops_province`; `MIGRATION_pull_province` adds `JOBS_available_slots`
  (JOBS_svalues.txt:355/:406, read at MIGRATION_svalues.txt:39/:95). So joblessness →
  people leave, spare slots → people arrive. This coupling is real and functioning.
- **Building construction gates on spare slots** via `sufficient_job_slots`
  (00_buildings_scripted_triggers.txt:4 → `JOBS_available_slots > 0`).

## The GAPS found

**G1 — `JOBS_set_employment_slots` is an ORPHAN (github issue #37, half-built).**
`se_ECON_employment.txt` defines exactly one effect, `JOBS_set_employment_slots`, which
computes `JOBS_slots_subsistence = total_population × (1 − civilization_value×0.01)`
(i.e. `total_population × inverse_industrialisation`). It is **called from nowhere**, and
its output variable `JOBS_slots_subsistence` is **read by nothing**. Dead code — the
subsistence-employment half of the model was scaffolded and never wired.

**G2 — Consequence of G1: unemployment is WILDLY overstated in agrarian provinces.**
`JOBS_num_used_slots = JOBS_non_subsistence` counts **only building jobs** (arsenals,
industrial estates, districts, depots…). So
`JOBS_unemployed_pops_province = total_population×0.5 − building_jobs`. In a pre-industrial
province with few buildings — i.e. essentially the entire Qing heartland — this reads
almost the whole workforce as "unemployed," even though those people are farming
subsistence land. `JOBS_svalues.txt:337` even flags the fix-value `JOBS_subsistence_worker`
as "# NOT IN USE". Because unemployment feeds `MIGRATION_push_province` (×1, min 0), this
phantom joblessness inflates out-migration push everywhere in agrarian China — a
structural bias, not intended behaviour. The engine already ships `inverse_industrialisation`
(ECON_svalues.txt:140) to express subsistence absorption; it was simply never applied to
the unemployment count.

**G3 — Wage/wealth ADEQUACY has no welfare feedback (noted, NOT fixed here).**
Strata wealth pools receive wages and pay cost-of-living, but nothing reads pop/per-capita
wealth to affect happiness, unrest, or pop promotion/demotion. Only luxury *demand*
(DEMAND_luxury_svalues.txt) reads `WEALTH_governorship_per_capita`. Wiring wealth→contentment
is a larger, balance-affecting design change (touches every country's unrest) and is out of
scope for a caution-first pass; recorded as a future item.

## FIX IMPLEMENTED — G1+G2: count subsistence employment in the unemployment calc

Decision: the correct, minimal, defensible fix is to stop counting subsistence farmers as
unemployed — exactly the intent of the orphan issue-#37 code. Rather than resurrect the
un-wired `JOBS_set_employment_slots` (a per-governorship yearly variable write with a
TODO-riddled temp-var dance), fold subsistence absorption **directly into the read-time
script value** `JOBS_unemployed_pops_province`, so it stays a cheap cached read with no new
pulse and no stored state — matching how the rest of the JOBS svalues work.

Formula (province scope):
```
JOBS_unemployed_pops_province =
    total_population × 0.5            # workforce (unchanged model assumption)
  − JOBS_num_used_slots              # building jobs (unchanged)
  − subsistence_jobs                 # NEW: land-absorbed labour
  , min 0
where subsistence_jobs = max( 0 , total_population × inverse_industrialisation − JOBS_non_subsistence )
```
`inverse_industrialisation = (100 − civilization_value)/100`. The `− JOBS_non_subsistence`
inside prevents double-counting the building jobs already subtracted above (net subsistence
labour beyond what buildings employ), and `min 0` keeps a highly-built province from going
negative there.

Effect by civ level (workforce = pop×0.5):
- **civ 0** (inv_ind 1.0): subsistence absorbs ~all pop → unemployed floors at 0. Correct:
  a pure subsistence economy has no wage-unemployment.
- **civ ~30–40** (Qing heartland, inv_ind ~0.6–0.7): subsistence ≥ workforce → unemployed ≈ 0.
  Removes the phantom migration over-push from agrarian provinces.
- **civ 100** (inv_ind 0): subsistence_jobs = 0 → `unemployed = pop×0.5 − building_jobs`,
  i.e. the ORIGINAL behaviour. A fully industrial province still shows real joblessness when
  buildings can't absorb the workforce. So the fix only *relaxes* the agrarian phantom and
  leaves the industrial case identical.

What this touches: ONLY `JOBS_unemployed_pops_province` (JOBS_svalues.txt). Consumers:
`MIGRATION_push_province` (migration push falls in agrarian provinces — the intended
correction) and `ECON_LOG_jobs_snapshot` (debug log total). It does NOT touch
`JOBS_num_used_slots` / `JOBS_available_slots`, so building-construction gating and the
DEMAND/wage chains are byte-for-byte unchanged. `inverse_industrialisation` and
`JOBS_non_subsistence` are both already-proven cached svalues used across the econ engine.

Estimated in-game effect: internal migration in Qing (and any low-civ nation) stops being
driven by a false "half the peasantry is unemployed" signal; people now leave provinces for
genuine reasons (unrest, famine, war, real overcrowding above subsistence capacity) rather
than everywhere-at-once. Industrialised nations are unaffected. No treasury/wage numbers move.

## FIX IMPLEMENTED — G3: wage/wealth adequacy as a migration signal (the missing feedback)

Decision: the genuinely MISSING feature is that wages/wealth had no downstream behaviour.
Rather than bolt global unrest onto every nation's pops (large, balance-affecting, touches
every country), the idiomatic build-out — consistent with the mod's FIRM bottom-up-migration
philosophy — is to make wealth adequacy a MIGRATION signal: the wage engine already pays
proletariat wealth every quarter and nets cost-of-living against it, so let that wealth pool
decide where people want to be. Poor provinces shed people; prosperous ones draw them. This
closes the wage -> welfare -> behaviour loop using only cached reads and the existing decade
migration pulse (no new on_action, no stored state).

New helper `MIGRATION_wealth_relative_province` (MIGRATION_svalues.txt, province scope):
```
= governorship.WEALTH_governorship_proletariat_per_capita
  / (owner.var:WEALTH_total_private_moveable_wealth / owner.country_population)
  - 1                       # deviation from the NATIONAL per-capita average
  , clamped to [-1, 1]
```
SCALE-FREE by construction: it is a ratio against the country's own average, so it never
depends on the absolute magnitude of the currency (which varies wildly by nation/era and
would be dangerous to read raw). Guarded on `wealth_setup_done` + the cached moveable-wealth
var, so it is a clean 0 before the wealth system inits and costs nothing when unset. The
`WEALTH_governorship_proletariat_per_capita` operand carries its own div-by-0 floor; the
denominator is floored at 0.0001.

Wired into the two migration scores (MIGRATION_svalues.txt):
- **PUSH** += `max(0, -deviation) * 6` — only the BELOW-average (poorer-than-national) leg
  pushes; scaled to 6 at the destitute floor (deviation -1), comparable to the war term.
- **PULL** += `max(0, +deviation) * 6` — only the ABOVE-average leg attracts; symmetric weight.
Splitting the legs (max 0 / min 0) keeps prosperity from creating negative push and poverty
from creating spurious pull — poverty pushes, wealth pulls, and neither double-signs.

Both operands are proven cross-scope reads: `governorship.<svalue>` from province scope is
the exact idiom already used for `governorship.ECON_governorship_food_shortage`
(MIGRATION_svalues.txt:52/:112), and `WEALTH_national_per_capita` reads the same
`WEALTH_total_private_moveable_wealth`/`country_population` pair (WEALTH_svalues.txt:632,
also read at DIPLOMACY_svalues.txt:64).

What this touches: ONLY MIGRATION_svalues.txt (the two decade-pulse scores + one helper).
No wage/treasury/wealth number changes; the wealth pools are read, never written. Perf: two
extra cached reads per province per DECADE pulse (migration is not a per-tick system).

Estimated in-game effect: wages finally MATTER for population. A province the wage engine
keeps poor (few jobs, high cost of living, heavy taxation eating the proletariat pool) slowly
loses people to richer provinces; booming industrial/commercial provinces draw labour in.
Combined with the G2 fix, migration now tracks REAL economic conditions — jobs, hunger,
unrest, war, AND relative prosperity — instead of a phantom-unemployment constant. Effect is
gradual (decade pulse, one grievance-weighted pop per province per pulse) and self-limiting
(as people leave a poor province its per-capita rises; as they crowd a rich one its slots
fill and pull falls), so it nudges the distribution without runaway depopulation.

## Orphan cleanup (G1)
`JOBS_set_employment_slots` (se_ECON_employment.txt) left in place as the issue-#37 scaffold,
with a STATUS NOTE added pointing to the read-time fold in JOBS_unemployed_pops_province and
warning against wiring it (would double-count subsistence). Not deleted — deleting a named
effect risks a future reference; the note is the lower-risk choice.

## Files changed (employment & wages)
- common/script_values/JOBS_svalues.txt — G1/G2: subsistence absorption folded into
  JOBS_unemployed_pops_province.
- common/script_values/MIGRATION_svalues.txt — G3: MIGRATION_wealth_relative_province helper
  + wealth-adequacy leg in MIGRATION_push_province and MIGRATION_pull_province.
- common/scripted_effects/se_ECON_employment.txt — G1: STATUS NOTE on the orphan effect.
All brace-balanced (verified). Next: deep adversarial review workflow, then commit + push.

## DEEP ADVERSARIAL REVIEW — 3 confirmed defects, all FIXED before commit

Ran a 3-dimension find -> adversarial-verify workflow (correctness/scope, proven-idiom,
balance-regression), 12 agents. All idioms verified PROVEN (governorship.<svalue> cross-scope
read, owner.var:, country_population divide, nested-block divisor, min/max clamps) — no
unproven-idiom flags survived. But it caught **three real correctness/balance defects**, all
confirmed against the actual files. Fixed:

**R1 (was HIGH) — G3 per-capita BASE MISMATCH.** The helper divided a PROLETARIAT-only
governorship per-capita (`WEALTH_governorship_proletariat_per_capita`) by the ALL-STRATA
national per-capita (`WEALTH_total_private_moveable_wealth / country_population`). Proletariat
is a poorer-than-average stratum, so the ratio was < 1 nearly everywhere -> deviation negative
everywhere -> the PUSH leg (max 0) fired empire-wide and the PULL leg (min 0) was DEAD. The
"symmetric ±6" signal I documented never existed; it was a one-sided everywhere-push — exactly
the bias the G2 fix set out to remove.
FIX: compare LIKE-FOR-LIKE — numerator now `governorship.WEALTH_governorship_per_capita`
(all-strata, WEALTH_svalues.txt:447) against the all-strata national per-capita. Now genuinely
symmetric around 0: a governorship richer than the national average draws people, poorer sheds
them.

**R2 (was HIGH) — G3 zero-proletariat spike.** A governorship with no proletariat made
`WEALTH_governorship_proletariat_per_capita` return 0 (no top-level value=, inner else fires)
-> ratio 0 -> deviation floored at -1 -> phantom full +6 push on ~half the 1763 map's tags
(tribal/steppe/colonial nations with no urban proletariat), enough to trip the emigrate gate
(push > 5) on its own.
FIX: dissolved by the SAME R1 change — `WEALTH_governorship_per_capita` is all-strata, floored
at 0.001, and populated for every governorship, so there is no zero-stratum edge. A no-
proletariat governorship now reads its real all-strata wealth, not 0.

**R3 (was MEDIUM) — G2 building-job cancellation.** My inner `subtract = JOBS_non_subsistence`
double-removed the building jobs (already subtracted via JOBS_num_used_slots), so in the
agrarian regime the metric algebraically collapsed to `(0.5 - inverse_industrialisation)*pop`
— the building-job count CANCELLED, making unemployment a pure civ function blind to actual
job-slot scarcity, and a hard 0 for all civ <= 50.
FIX: dropped the inner `subtract = JOBS_non_subsistence`. Now
`unemployed = max(0, 0.5*pop - building_jobs - inverse_industrialisation*pop)`: building jobs
are subtracted exactly once, subsistence capacity exactly once, so the metric stays responsive
to job slots at every civ level (subsistence floors it at 0 in poor provinces; reduces to the
old building-only calc at civ 100).

Non-surviving items (REFUTED on verify): 3 "reassurance/no-defect" notes and the
"governorship-uniform wealth signal" concern (refuted — the picker ranks provinces and the
signal still varies country-to-country and over time as wages diverge wealth). No runaway-
depopulation risk (migration is hard-capped to one pop per province per decade pulse).

Post-fix: both files re-verified brace-balanced. The migration wealth signal is now symmetric
and scale-free on a like-for-like all-strata basis; unemployment is subsistence-aware AND
job-slot-responsive. Committing.
