# DESIGN #115 — regional import pricing "both" model: per-zone denominator, superseding #112's divisor

> STATUS 2026-08-12: REVIEWED — SOUND, one fix applied. Adversarial review confirmed the mechanism
> works (macro substitution into a chained scripted-value/var name is proven live elsewhere in this
> codebase, `se_CURRENCY.txt:1271`), confirmed ordering/peg-isolation/#106-interaction all hold, and
> found ONE real defect: the doc's own headline code sample showed the live svalue call
> (`owner.TZ_penetration_$tradezone$`, option (b)) while the analysis below it recommended the
> cached-var form (option (a)) — an implementer copy-pasting the sample would have shipped the
> unrecommended, hot-loop-reintroducing form. Fixed: the code sample now shows the cached-var form
> throughout, with an explicit warning against the bareword svalue-call form. Ready to implement.
> Scoped explicitly against #112's own scope note (`design/DESIGN_REGIONAL_PRICE_INDEX.md:22-23,
> 45-51`), which reserves exactly this task and flags it MUTUALLY EXCLUSIVE with #112's shipped
> divisor at the same site.

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:66`: "regional price = local_price / (0.5 +
per-zone TZ_penetration) — the 'both' landed-cost model (own pipeline)."

## Ground truth (confirmed by diagnosis, cross-checked against #112's own doc)

`GT_split_update_wealth_owed_for_tradegoods` (`common/scripted_effects/se_GLOBALTRADE_split.txt:
2459-2522`, scope: governorship, dispatched per-tradezone via the `:2319` dispatcher which already
knows `$tradezone$` from the paying governorship's location) currently computes, as of #112
(committed, shipped `fb8021418`):

```
wealth_owed_for_$tradegood$ =
    order_size_$tradegood$
    × ( global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$  [min = 0.0001]
        / (0.5 + owner.var:country_global_market_penetration_$tradegood$) )   # <- NATIONAL, aggregate-per-good
    × owner.var:order_size_modifier_$tradegood$
    × (1 - power_trade_bonus)
```

- `local_price_$good$` (`se_GLOBALTRADE_split.txt:5951`, set by `GT_set_tradegood_price`): per-zone,
  from that zone's own order/stockpile ratio × 0.6 (+ manufactured-input premium), stored on the
  tradezone's own global var object. Already geographic — #112's contribution.
- `owner.var:country_global_market_penetration_$tradegood$` (`GT_split_get_global_import_unit_
  price_tradegood`, ~`:2530+`): a COUNTRY-scope aggregate = Σ over all 22 zones of
  `(<zone>_stockpile_share × TZ_penetration_<zone>)` for that good — ONE number per country per good,
  blind to which zone is actually paying. This is the divisor #112 left untouched, explicitly
  reserving its replacement for this task (#112's doc, line 22-23: "the fuller 'both' model... is
  #115, separate pipeline... mutually exclusive at implementation").
- `TZ_penetration_$zone$` (`common/script_values/SHIPPING_svalues.txt:1317`+, one svalue per zone,
  e.g. `TZ_penetration_india`, `TZ_penetration_east_mediterranean`): COUNTRY scope, 0..1, "how much
  shipping presence does THIS country have in THIS zone" — driven by `var:shipping_<zone>` (the
  country's own shipping power into that zone, itself seeded/updated by `SHIPPING_update_TZ_
  overview_piecharts` and, as of #106 this session, at country-creation too) × `MODIFIER_tradezone_
  penetration_from_own_trade_power`, plus subjects'/trade-partners' contributions, with an AI-minor
  shortcut. This is the per-zone signal `country_global_market_penetration_$good$` collapses away.

## The gap and the fix

The "both" model makes BOTH the numerator (already done, #112) AND the denominator regional: divide
by THIS zone's own penetration, not the country's blended-across-22-zones aggregate. A country with
strong shipping in one zone but weak presence in another should pay the access-discount that matches
where the good is actually landing, not a national blend that over-discounts weak zones and
under-discounts strong ones.

Concretely, at the SAME site #112 edited (`se_GLOBALTRADE_split.txt:2459-2522`, the `multiply`
block within it), replace the divisor with the CACHED var form (option (a) below — not the live
svalue call; see "Why this doesn't need the aggregate" for why the cached form is the one to ship):

```
change_variable = {
    name = wealth_owed_for_$tradegood$
    multiply = {
        value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
        min = 0.0001
        divide = {
            value = 0.5
            add = owner.var:TZ_penetration_$tradezone$
        }
    }
}
```

The ONLY change from #112's shipped line: `owner.var:country_global_market_penetration_$tradegood$`
→ `owner.var:TZ_penetration_$tradezone$` (the cached per-zone COUNTRY var, written once per quarter
by `GT_split_cache_TZ_penetration_values`, NOT a live call to the `TZ_penetration_$tradezone$`
script value itself — copy this exact form, not a bareword `owner.TZ_penetration_$tradezone$`
svalue call, which would reintroduce a per-payment-call cost class this file's own `#139`
optimization elsewhere was written to eliminate). Both the numerator's zone and the denominator's
zone are now the SAME `$tradezone$` — the paying governorship's own trade zone, already known at
this call site (the `:2319` dispatcher passes it in). No new scope-bridging machinery is needed: the
governorship scope already carries both `$tradezone$` (as a macro param) and `owner` (for the
country-scope var read) — this is the exact same shape #112 already proved works at this site, just
swapping which penetration term is read.

## Why this doesn't need the `country_global_market_penetration` aggregate at all

`TZ_penetration_$tradezone$` is a plain script value (not a stored var) — callable directly as
`owner.TZ_penetration_$tradezone$` since it's scoped to Country and takes no macro parameter itself
(the zone is baked into its own name, one svalue per zone, matching the existing 22-svalue family
already used elsewhere in this file — e.g. `GT_split_cache_TZ_penetration_values`,
`se_GLOBALTRADE_split.txt:1038`+, which caches all 22 into `var:TZ_penetration_<zone>` country vars
once per quarter for OTHER readers). Two implementation options, both valid:

**(a) Read the cached var** (`owner.var:TZ_penetration_$tradezone$`) — reuses the existing
once-per-quarter cache from `GT_split_cache_TZ_penetration_values`, which already runs before this
payment site in the same on_action chain (confirmed: `GT_split_cache_TZ_penetration_values` is
called from `quarterly_reset_trade_transaction_totals`/`oa_economy_setup.txt`, both of which
precede the `quarterly_global_trade_*` category passes that eventually reach this payment function —
same ordering guarantee #112's own doc already established for `local_price`/penetration reads at
this site). Cheapest: zero extra computation, one var read.

**(b) Call the svalue directly** (`owner.TZ_penetration_$tradezone$`) — always fresh, no cache
staleness risk, but recomputes the full svalue (a walk over subjects + trade partners +
influenced-states + provinces, per `SHIPPING_svalues.txt:3585`+) on every payment call instead of
once per quarter.

**Recommendation: (a), the cached var — confirmed by review, stronger reason than staleness alone.**
#112's own numerator read (`local_price`) is likewise a cached global var, not a live svalue call,
at this exact site — using the cached penetration var matches that precedent. More importantly
(a review finding, not just staleness-avoidance): this file has direct prior art for the cost of
getting this wrong — `GT_split_cache_governorship_infrastructure_capacity`
(`se_GLOBALTRADE_split.txt:12-17`) was hoisted OUT of this exact hot per-category-pass loop (`#139`)
specifically because re-evaluating an expensive province-walking script value once per category pass
(7x/quarter) instead of once per quarter was the single most expensive recompute in the pipeline.
`TZ_penetration_$tradezone$`'s live body is the same shape of expense (`every_subject` + trade-
partner + influenced-state + province walks, `SHIPPING_svalues.txt:3585`+) — calling it live at THIS
payment site (per governorship, per good, per tradezone — a much hotter call frequency than even the
`#139` case) would reintroduce the exact class of regression `#139` was written to eliminate. The
cache is refreshed quarterly, the same cadence the rest of this payment pipeline already operates on
(order sizes, stockpile shares, etc.) — no new staleness class, and no new perf regression.

**Confirmed safe against the #106 shipping-seed flood** (a review cross-check): `TZ_penetration_
<zone>`'s live body has an unguarded `var:shipping_<zone> > 0` read inside its `every_subject` walk
(a subject's own shipping var) — structurally the SAME unset-var class #106 (`734de2ac1`) fixed for
the OWNER's own zone vars. This design does NOT reopen that risk: it only ever reads the ALREADY-
CACHED `var:TZ_penetration_<zone>`, never invoking the live svalue body itself. That live body is
invoked once per quarter regardless of this design (by the pre-existing `GT_split_cache_TZ_
penetration_values` call, which already feeds `CURRENCY_power` today) — this design adds a reader of
an existing cache, not a new evaluation path, so it carries none of the live body's own risk surface.

## Peg isolation (carried forward from #112's own proof, still holds)

`country_unit_price_$good$` (the currency peg's sole price input, `CURRENCY_svalues.txt:673`) is
STILL not written by this change — this fix only ever touches `wealth_owed_for_$tradegood$`, exactly
as #112 did. `TZ_penetration_$tradezone$` is read-only here (never written), so no new peg-input
mutation is introduced. The ordering guarantee #112 established (both `local_price` and the
penetration term are set before this payment site runs, every quarter) extends unchanged to the
per-zone penetration var, which is cached in the SAME quarterly pass as the aggregate one it replaces
(`GT_split_cache_TZ_penetration_values` computes all 22 `TZ_penetration_<zone>` vars in one call,
immediately alongside — same function — as far upstream of this payment site as the aggregate).

## Floor/ceiling (mirrors #112, no new policy decision needed)

Keep `min = 0.0001` on the numerator exactly as #112 shipped it (a good is never literally free) and
NO ceiling on the result (per #112's own user directive, unchanged: a starved/spiking zone's price
passes through in full). This fix changes ONLY which penetration figure divides the price, not the
floor/ceiling policy around it.

## Mutual exclusivity with #112 (explicit, per #112's own doc)

This design REPLACES #112's divisor inside the `multiply = { ... }` block of `GT_split_update_
wealth_owed_for_tradegoods` (`se_GLOBALTRADE_split.txt:2459-2522`) in place — it does not
stack alongside it. #112's numerator change (pay the paying zone's own `local_price`, not the global
`gbip`) is KEPT UNCHANGED; only the denominator term changes. Implementation is a single-line
substitution inside the SAME `change_variable` block #112 already shipped, not a parallel pipeline
bolted on beside it — "own pipeline" in the task's phrasing refers to this being #115's OWN
diagnosis/design/review track (distinct from #112's), not a request for a structurally separate code
path; the two formulas are algebraically substitutable at the identical call site, and #112's doc
itself anticipated exactly this outcome ("if #115 clears its pipeline it likely SUPERSEDES #112").

## What this design does NOT touch

- `local_price_$good$`'s own computation (`GT_set_tradegood_price`) — unchanged, #112's numerator
  fix stands as-is.
- `country_global_market_penetration_$good$` itself — left in place as a script value (other readers
  may still use the national aggregate for other purposes; grep confirms no other caller of THIS
  payment function needs it removed as dead code — it remains a legitimate general-purpose national
  metric, just no longer consumed at this one payment site).
- Any GUI/tooltip surface — this is a pure formula change in the trade-payment pipeline; no player-
  facing text currently displays this divisor's value, so no loc/GUI follow-up is implied.

## Open questions for review
- Confirm option (a) vs (b) above (cached var vs live svalue call) — is there a reader of
  `var:TZ_penetration_<zone>` elsewhere in the codebase whose cache-invalidation assumptions this
  change could interact with, or is it purely additive read-only consumption?
- Confirm the ordering claim: does `GT_split_cache_TZ_penetration_values` genuinely run, every
  quarter, strictly before `GT_split_update_wealth_owed_for_tradegoods` is reached for every
  governorship (not just "usually" — trace the actual on_action call chain, not inferred from #112's
  analogous claim about `local_price`).
- Any boot-watch concern analogous to #112's flagged zero-stockpile silver-zone spike (upper_yangtzi/
  yellow_sea) — does a zone where the OWNER has near-zero shipping presence (`TZ_penetration_<zone>`
  near 0) produce a similarly extreme divisor-near-0.5 spike, and if so is that economically
  sensible (a country poorly represented in a zone pays close to full local price there — arguably
  MORE correct than the national blend, since it's the "no access discount" case) or does it need
  the same boot-watch flag #112 carries?
