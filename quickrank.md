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
