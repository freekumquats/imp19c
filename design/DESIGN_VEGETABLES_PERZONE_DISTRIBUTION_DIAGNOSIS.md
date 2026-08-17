# DIAGNOSIS (draft, pre-review) — why most trade zones stay permanently out of vegetables

## Trigger

`tools/vegetables_trace.py` on the 2026-08-16 22:05 boot (after the `GOODS_vegetables_
production_multiplier=4` fix shipped this session) showed the GLOBAL vegetables stock no
longer collapsing to 0 — but 19 of 22 individual trade zones still hit stock=0 and stay there
permanently through the end of the trace, with real unmet demand (`order` stays nonzero)
persisting the whole time. Only baltic, central_europe, and india stabilize at nonzero stock.

## Scope check: is this vegetables-specific?

No. Re-ran the same zone-death classification (last 5 quarter-marks all stock=0) against 4
other goods from the SAME boot's debug.log:

| good | provinces (world) | zones dead / 23 tracked |
|---|---|---|
| grain | 1747 | 0 |
| livestock | 1885 | 0 |
| silk | (China-concentrated) | 12 |
| tea | (China-concentrated) | 13 |
| vegetables | 419 (China only) | 19 |

**Goods produced worldwide (grain, livestock) never die in any zone. Goods geographically
concentrated in one region (silk, tea, vegetables — all China-only in this mod) die in roughly
half to five-sixths of the world's zones.** This is a general limitation in how production
reaches a zone that doesn't produce a good locally, not something specific to vegetables' own
demand/production formulas (both of which were already audited and fixed this session).

## Traced mechanism (confirmed by direct code read)

- `GT_split_declare_sell_to_TZ_aggregate_stockpile` (`se_GLOBALTRADE_split.txt`, called once per
  governorship from `GT_split_do_global_trade_split`): each governorship sells only into its
  OWN geographic trade zone's aggregate stockpile. There is no step in this entry chain that
  moves a producing zone's surplus into a different zone's stockpile.
- `GT_split_create_order_tradegood` (`se_GLOBALTRADE_split.txt:2143-2200`): a governorship only
  submits a buy-order for a good if `has_variable = $tradegood$_stockpile` is already true for
  it. The function's OWN comment (`[logfix #19]`) explicitly flags this as a live, unresolved
  design question: *"Whether a non-producing governorship SHOULD raise a buy order is a separate
  design question, deliberately not changed here."* A governorship that never produced
  vegetables would only have this var at all if something else (a game-start seed) initialized
  it — meaning its capacity to even ASK for more vegetables going forward is contingent on that
  one-time seed, not a standing per-good demand right every governorship has by default.
- `GT_set_tradegood_price` (`se_GLOBALTRADE_split.txt:6210+`): price is computed PURELY from
  `global_var:$tradezone$_total_order_size_$tradegood$` divided by
  `global_var:$tradezone$_stockpile_$tradegood$` — both zone-LOCAL globals. The price formula
  itself has no cross-zone term at all; whatever a zone's local stock is (its own production
  plus whatever imports arrived from elsewhere) is all that formula ever sees.
- `TZ_penetration_<region>` (`SHIPPING_svalues.txt`, the function this session's log pass just
  patched for unguarded first-tick reads) feeds `TRADE_total_global_market_penetration` — a
  COUNTRY-level aggregate "how much global market access do I have" figure, consumed by
  `TRADE_svalues.txt` and `CURRENCY_svalues.txt`. Confirmed this exists and is real; **NOT yet
  traced to a specific line that actually moves a quantity of a good from a foreign zone's
  stockpile into a deficit zone's own stockpile** — that redistribution step (if it exists) is
  somewhere else in the trade-processing chain and was not located in this pass.

## Confidence-graded conclusion

**High confidence** (directly observed + directly read): the die-off correlates with
geographic production concentration, not with vegetables' own formulas; each zone's price is
computed from purely local order/stock; a governorship's ability to even order more of a good
depends on a stockpile var whose initialization for non-producers is explicitly flagged as an
open design question in the code's own comments.

**Not yet confirmed** (would need either a live boot probe or more tracing through the vanilla
trade engine, which runs considerably deeper than the entry points read here): the EXACT
mechanism (or absence of one) that is supposed to move a producing zone's surplus into a
deficit zone's stockpile, and why it isn't doing so adequately for China-concentrated goods
specifically. Two candidate explanations, not yet distinguished:
1. **No such redistribution step exists in a meaningful way** for this class of good — the mod/
   vanilla trade engine may rely on individual COUNTRIES importing via their own market
   penetration into a foreign zone, and a country with low penetration into China's trade zones
   (most of the world, starting cold in 1763) simply never accumulates enough access to buy any
   of China's vegetable surplus, regardless of how much of it exists.
2. **A redistribution step exists but is gated/capped low enough** (e.g. by
   `TRADE_governorship_trade_capacity`, a shipping-capacity cap referenced elsewhere in this
   session's log pass) that it can't move enough volume for a good with this few producing
   provinces, even though the same cap doesn't bottleneck a good produced in 1700+ provinces.

Both candidates point toward the SAME class of fix (raise effective shipping/import capacity or
penetration for geographically concentrated goods) but are different code paths to change, so
distinguishing them matters before proposing a specific fix.

## Mechanism CONFIRMED (adversarial review, 2026-08-17)

Review traced the exact missing step this diagnosis flagged as unlocated — it exists a few
dozen lines further into the SAME orchestrator (`GT_split_do_global_trade_split`,
`se_GLOBALTRADE_split.txt`) this diagnosis had already opened, and was findable without a live
boot probe (a calibration miss on this diagnosis's part, noted honestly — the review's own
critique, confirmed fair). Full chain, spot-checked directly against the file and confirmed
accurate at every cited line:

1. `GT_split_create_global_stockpile` (:1469-1519) sums each zone's local stockpile into a
   global total, then computes `<zone>_percentage_of_global_stockpile_$tradegood$` for all 22
   zones (each zone's SHARE of world production).
2. `GT_split_get_country_global_market_penetration_tradegood` (:1824+) computes, per country:
   `Σ_zones( <zone>'s share of world production × TZ_penetration_<zone> ) × 0.4545` (spot-check:
   the `× 0.4545` is a real, confirmed OFF constant — the adjacent comment says "divide by 22"
   which is `× 0.04545`, a 10x discrepancy, present in the code as-is; flagged, not touched).
3. `TZ_penetration_<zone>` (`SHIPPING_svalues.txt`) is a BILATERAL value — a country's own
   built-up shipping/trade-agreement presence in that SPECIFIC foreign zone, divided by
   everyone's combined presence there. Confirmed NOT a function of the producing zone's
   province count.
4. This penetration score becomes `order_size_modifier_$tradegood$`
   (`GT_split_get_order_size_modifier_tradegood`, :2065+), which scales down every governorship's
   import order before `GT_split_add_amount_imported_tradegood` (:3986-4002, spot-checked)
   credits it to the governorship's own local stockpile. **Confirmed this import step carries
   the SAME `has_variable = $tradegood$_stockpile` gate found earlier for order-creation** — a
   governorship that never produced the good (and was never game-start-seeded with the var)
   cannot receive an import at all, a second, independent choke point on top of the penetration
   score.

**Why this explains the province-count correlation without province count being the real
variable**: for a good produced across most of the 22 zones (grain, livestock), step 2's
weighted sum is dominated by each country's OWN home-zone term, and every country has
substantial shipping presence in its own zone by default — penetration stays healthy, imports
flow. For a good concentrated in ONE zone (silk/tea/vegetables — all China-only here), step 2
collapses to essentially one term: a country's bilateral shipping presence SPECIFICALLY in
China's zone. Most of the 1763 world starts cold there (no trade agreements/colonies in China's
zone yet), so penetration ≈ 0, `order_size_modifier` ≈ 0, and imports stay ≈ 0 — a stable trap
that doesn't self-correct (a governorship needs the resource to build the very shipping
infrastructure that would let it get the resource). The real causal variable is "number of trade
zones with a nonzero production share," not province count directly — they only correlate here
because every concentrated good in this mod happens to be confined to one region.

**Candidate 2 (a province-count-scaled capacity cap) is confirmed NOT the mechanism** — no such
cap was found in this chain. Drop it from consideration. Candidate 1 (import access gated on
pre-existing bilateral penetration) is confirmed correct, sharpened as above.

The 3 zones that stabilize (baltic, central_europe, india) are plausibly the ones with the
strongest historical head-start in China-zone shipping presence (era-appropriate for
India/EIC-style China trade, and the two European hubs) — consistent with, but not yet directly
confirmed against, live boot variable values.

## Recommendation

Diagnosis is now confirmed, not speculative — ready for a design phase. Any fix should target
step 2/3 above (making `country_global_market_penetration` for a geographically-concentrated
good reachable without requiring an ALREADY-existing bilateral shipping relationship — e.g. a
floor value, a different penetration curve for single-zone goods, or seeding a minimal
`shipping_<zone>` value at game start for major trade powers), not a capacity-cap fix (confirmed
wrong target) and not another production multiplier (already tried this session for vegetables,
confirmed insufficient for this specific per-zone problem). Not designing or implementing a fix
in this pass — flagging as ready for its own dedicated design/review/implement cycle when
picked up next, given the volume of other work already in flight this session.
