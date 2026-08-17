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

## Recommendation

Do NOT propose an implementation from this diagnosis alone — the exact mechanism is not fully
traced, and guessing at a fix without finding the real redistribution step (or confirming there
isn't one) risks the same category of premature-fix mistake this project has been burned by
before (memory: reviews catching inert-lever fixes). Recommend:
1. Send this diagnosis for adversarial review first (per standing process) — an independent
   pass may trace further into the vanilla trade engine than this one did, or find the actual
   redistribution mechanism this pass missed.
2. If review confirms the mechanism is genuinely this shallow (no meaningful redistribution, or
   a capacity cap that scales badly with province count), the design phase should propose a fix
   targeted at whichever of the two candidates above turns out to be real — not a blanket
   production multiplier (already tried, already shown insufficient for the per-zone problem
   specifically) and not a guess at the shipping formula without confirming it's the actual
   bottleneck.
