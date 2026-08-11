# DESIGN — regional price index (per-zone import price divergence), replacing the reverted #50

**Status:** DRAFT 2026-08-11. Replaces the reverted #50 penetration cap-lift. Needs adversarial review before
implementation. Delicate UPSTREAM code (se_GLOBALTRADE_split.txt) — cautious pattern, must clear the
AUDIT_CURRENCY_23 §F.2 three-part burden of proof (§H proves it for the chosen lever). See [[currency-swing-diagnosis]].

## Goal (user)
The SAME good should cost differently in different regions — Canton silk cheaper than London silk — and this
must survive conquest correctly ("if China conquers London, cheap silk must NOT teleport there"). #50 tried to
do this by scaling country market penetration; that FAILED because penetration is a per-COUNTRY lever that
also feeds the currency peg (it dragged inflation) and could never make two provinces of the same owner pay
different prices. #50 is reverted (54673a6af). This builds the divergence on a genuinely geographic lever.

## Ground truth — the price chain (traced, AUDIT_CURRENCY_23 §G/§H)
- **local_price_$good$** (GT_set_tradegood_price, :5901) — PER-ZONE, from that zone's own
  order/stockpile ratio × 0.6. Already geographic (india-TZ silk ≠ central_europe-TZ silk). THE regional signal.
- **gbip = global_base_import_price_$good$** (:2509) — the stockpile-share-weighted WORLD AVERAGE of the 22
  zones' local_price. One global scalar.
- **country_unit_price_$good$** (:2734) = gbip / (0.5 + country_penetration) — PER-COUNTRY. Carries the
  penetration ACCESS DISCOUNT (a high-penetration power pays below world average). ALSO the currency peg's sole
  price input (CURRENCY_essentials_buying_power, CURRENCY_svalues.txt:673 — §H.1). MUST stay per-country.
- **wealth_owed** (GT_split_update_wealth_owed_for_tradegoods, :2459) = order_size × owner.country_unit_price ×
  owner.order_size_modifier × (1 − power_trade_bonus). Dispatched PER-TRADEZONE (:2319 knows $tradezone$) — the
  zone is KNOWN here but currently discarded in favor of the owner's national price.

## The lever — a regional INDEX multiplier on the payment (NOT a raw price swap)
Do NOT replace country_unit_price with local_price (that would discard the penetration discount + peg
consistency). Instead layer a **regional index** onto wealth_owed:

```
regional_index_$good$(zone) = zone.local_price_$good$ / gbip_$good$        # 1.0 = world average; <1 cheap zone, >1 dear zone
wealth_owed = order_size × owner.country_unit_price × order_size_modifier × (1 − power_trade_bonus) × regional_index(paying zone)
```

- **country_unit_price stays the national anchor** → the currency peg (which reads country_unit_price, §H.1) is
  UNTOUCHED → no #50-style bleed (proven §H). The penetration access-discount is preserved.
- **regional_index is purely geographic**: it is (this zone's price ÷ world average). Canton's cheap-silk zone
  → index <1 → Canton pays below the national price; London's dear-silk zone → index >1. A conquered London
  province sits in the central_europe zone, so it reads THAT zone's index regardless of owner → prices do NOT
  teleport. Exactly the user's test.
- The multiplier is DIMENSIONLESS and centered on 1.0, so on a globally-average zone it is a no-op — meaning
  the WORLD-AGGREGATE payment pool is approximately preserved (Σ over zones of price×qty ≈ national-avg×qty when
  the index averages to 1 weighted by trade). This bounds §H.4's total-income magnitude effect: it REDISTRIBUTES
  payment across zones far more than it changes the total. (Still logged + measured on boot — see below.)

### Where it attaches
GT_split_update_wealth_owed_for_tradegoods (:2459) already runs in the PAYING governorship's scope and receives
`$tradezone$` (from the :2319 switch dispatcher). Add ONE change_variable after the country_unit_price multiply
(:2468): multiply wealth_owed by `regional_index_$good$` computed from
`global_var:global_$tradezone$_tradezone.var:local_price_$good$` ÷ `global_var:global_base_import_price_$good$`.
Guard gbip>0 (Div/0 — the #23 discipline) and clamp the index to a sane band (see below).

### Clamp / safety band (best-guess, log-and-tune)
- **gbip = 0 or unset** → index = 1 (no-op; never Div/0). Same guard style as :5908 stockpile>0.
- **local_price = 0** (empty zone, no orders) → index would be 0, zeroing the payment. Floor the index at a
  minimum (e.g. 0.25) so an under-supplied zone still pays SOMETHING; cap at a maximum (e.g. 4.0) so a
  momentarily-starved zone doesn't 10× a payment. Band [0.25, 4.0] is a best-guess — logged, tuned on boot.
  (Historical regional price spreads for a staple were rarely beyond ~3-4×; luxuries wider but the cap protects
  the sim, not realism.)

## §F.2 burden of proof — DISCHARGED (AUDIT_CURRENCY_23 §H)
- (a) WHAT: a dimensionless regional_index = zone local_price ÷ gbip, multiplied into wealth_owed at :2468-ish.
- (b) WHY regional: local_price is set per-zone from that zone's own supply/demand (:5901); the index is a pure
  geographic deviation from the world average; keyed to the PAYING zone, so conquest-correct.
- (c) NO bleed: country_unit_price (the peg input, §H.1) is untouched; the payment pool feeds ONLY seller income
  distribution (§H.3, GT_split_get_governorship_income_due:3559); order_size_modifier reads DEMAND+penetration,
  not wealth_owed (§G.2). The index cannot reach the peg, order sizes, penetration, or #219's AI valuation.
- Residual (§H.4): the total-payment-pool magnitude shift. Bounded by the index centering on 1.0; MEASURED on
  boot via logging, not assumed. This is a tunable, not a blocker.

## Logging (ships with the change — overnight Rule 1a / error-logging rule)
Under the existing tzprobe / ECON_LOG harness (kept from #50), emit per boot for silk + tea + grain + silver:
- gbip, a sample zone's local_price, the computed regional_index (min/max/mean across zones),
- total global_payment_pool for the good WITH vs WITHOUT the index (the §H.4 delta),
so the boot confirms the index band is sane and the total-income shift is bounded. Static label strings only
(no macro $param$ / # in LOG strings — log-string-macro-rule). -debug_mode gated.

## Files
- common/scripted_effects/se_GLOBALTRADE_split.txt — ONE added change_variable block in
  GT_split_update_wealth_owed_for_tradegoods (~:2468), computing + applying regional_index with the gbip>0 guard
  and the [0.25,4.0] clamp. Nothing else in the price chain changes.
- common/scripted_effects/se_ECON_LOG_TZPROBE.txt (or the ECON_LOG harness) — the index + pool-delta logging.
- NO change to country_unit_price (:2734), the peg (CURRENCY_svalues.txt), gbip (:2509), local_price (:5901),
  penetration (:1991), order_size_modifier (:2026), or the income distribution (:3559).

## Review must test (adversarial)
1. Is regional_index truly geographic + conquest-correct? Confirm the paying scope's $tradezone$ is the
   PROVINCE's zone (not the owner's) — trace the :2319 switch: it dispatches on `TZ_is_<zone>_tradezone` which
   is a property of the governorship's LOCATION. So a conquered London province → central_europe zone → its
   index, not China's. Verify.
2. Div/0 + unset: gbip>0 guard present? local_price unset (never-ordered zone) handled by the floor? No new
   "Variable used but never set" flood (the zone local_price + gbip are set earlier in the same quarterly pass —
   confirm ORDER: GT_set_tradegood_price (:5901) and gbip (:2509) both run BEFORE wealth_owed (:2459)? If
   wealth_owed runs before local_price is set for the quarter, the index reads a stale/unset value — CRITICAL
   ordering check).
3. Peg isolation: re-confirm country_unit_price is not touched and the peg cannot see the index (§H.1).
4. Total-income magnitude (§H.4): does the index centering on 1.0 actually bound the pool delta, or can a
   systematically-cheap-home-zone (e.g. all of China's silk in cheap zones) shift CHI's total trade income
   materially? Is the [0.25,4.0] clamp the right band? (Boot-tunable, but flag if the design under-bounds it.)
5. #219: does a regional wealth_owed resurrect any goods-valuation signal the vanilla trade AI reads
   (memory vanilla-trade-request-flood-open, zeroed in e3f3c2e91)? wealth_owed feeds only the payment pool →
   seller income; confirm no AI diplo factor reads it.
6. Manufactured goods: local_price for manufactured goods factors ingredient costs (:5936+, global_mean_price
   path). Does the index (local_price/gbip) compose correctly for a manufactured good, or double-count the
   ingredient premium? (gbip is ALSO built from the same local_prices, so the ratio should be clean — verify.)
7. Is a multiplicative index the right model vs an additive/blended one? (An index preserves the national
   structure exactly and is conquest-clean; alternatives should be argued down or up.)
