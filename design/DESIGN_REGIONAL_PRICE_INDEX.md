# DESIGN #112 — regional import pricing: pay the paying zone's local_price (per-zone divergence), replacing reverted #50

**Status:** CORRECTIONS FOLDED, AWAITING CLEAN RE-REVIEW 2026-08-11 (NOT yet implementation-ready — review112b
returned SOUND-WITH-CORRECTIONS incl. a CRITICAL max/min floor bug; those fixes are now IN the doc but have NOT
themselves been reviewed. One more pass must return CLEAN before implementation).
The LEVER is a DIRECT SUBSTITUTION (NOT a "regional index" — see §WHY-DIRECT): at the payment site (:2468) pay
`zone.local_price / (0.5 + owner.national_penetration)` instead of `owner.country_unit_price`. Reads NO gbip.
- Both sink-risk checks PASS (review112 + review112b): ORDERING — the direct form reads only local_price
  (driver :37) + owner penetration (:50), both set before the payment site (:54); reads no gbip. PEG ISOLATION —
  country_unit_price (peg input) is NOT written; peg reads country_unit_price + reserve_ratio, the change touches
  neither → provably the correct side of the peg, unlike #50 (which scaled penetration, a peg INPUT).
- review112b findings folded: (1 CRITICAL) the floor is `min = 0.0001`, NOT `max` (max = ceiling in this engine —
  `max=0.01` would have capped all prices at 0.01 and destroyed the lever); (2) copy country_unit_price's own
  block verbatim, swap gbip→local_price — its `min=0.0001` IS the strict-positive floor, one guard, done;
  (3) boot-watch the §E zero-stockpile SILVER spike (structural for China's silver zones); (4) ORDERING rewritten
  for the direct form (no gbip).
- CLAMP REMOVED (user): the [0.25,4.0] band was MY OWN addition to this new term, not upstream. Only guard on
  the value = the `min=0.0001` strict-positive floor so a good never goes free ("only prevent goods from going to
  0"). NO ceiling. Metals stay IN (user: do not exempt gold).
- MINIMAL form. The fuller "both" model (per-zone TZ_penetration denominator) is #115, separate pipeline,
  mutually exclusive at :2468.
Delicate UPSTREAM code — cautious pattern. Clears AUDIT_CURRENCY_23 §F.2 (§H). See [[currency-swing-diagnosis]].

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

## SCOPE NOTE — #112 is the MINIMAL form; the "both" form is #115 (separate pipeline)
#112 (this doc) makes ONLY the price NUMERATOR regional: pay `zone.local_price / (0.5 + NATIONAL penetration)`.
The economically-fuller "both" model — where the DENOMINATOR is also per-zone (`/ (0.5 + owner.TZ_penetration_
<zone>)`, using the per-zone penetration layer Sobisonator already built) — is a SEPARATE task (#115) with its
own diagnosis→review→design→review pipeline, per user directive (do not conflate). The two are MUTUALLY EXCLUSIVE
at implementation (both rewrite the same payment line :2466-2469): if #115 clears its pipeline it likely
SUPERSEDES #112; otherwise #112 ships as the safe minimal version. Nothing below adopts the #115 denominator.

## The lever — pay the paying zone's local_price instead of the national average (DIRECT form)
The province pays for its imports at ITS OWN TRADE ZONE'S price, not the country-wide average. Stated directly
(no "index" abstraction — see §WHY-DIRECT below for why the earlier index framing was redundant):

```
TODAY:  wealth_owed = order_size × owner.country_unit_price × order_size_modifier × (1 − power_trade_bonus)
        where  owner.country_unit_price = gbip / (0.5 + owner.penetration)          # national avg, penetration-discounted

CHANGE: wealth_owed = order_size × [ zone.local_price / (0.5 + owner.penetration) ] × order_size_modifier × (1 − power_trade_bonus)
        i.e. substitute the paying zone's local_price for gbip in the price term, keeping the SAME
        (0.5 + penetration) access-discount divisor.
```

- **What changes:** the price a province pays is now its ZONE'S local_price (per-zone, geographic), not the
  world-average gbip. Canton (cheap-silk zone) pays less; London (dear-silk zone) pays more. A conquered London
  province still sits in the central_europe zone → still pays that zone's price regardless of owner → prices do
  NOT teleport on conquest. Exactly the user's test.
- **What is PRESERVED:** the `(0.5 + penetration)` divisor — the national access-discount (a high-penetration
  power still pays proportionally less). Only the numerator (gbip → zone local_price) changes.
- **What is UNTOUCHED:** the `country_unit_price` VARIABLE itself is not modified — we compute the payment from
  local_price directly at the payment site, leaving country_unit_price (:2734) exactly as-is. The currency peg
  reads country_unit_price (§H.1), so the peg is isolated by construction — no #50-style bleed (proven §H).
- **Magnitude (honest, review112 finding 2):** paying zone-price instead of the stockpile-share-weighted world
  average, under order-size weighting, does NOT preserve the total payment pool by construction — a country whose
  orders concentrate in systematically cheap (or dear) home zones shifts its total trade income. UNBOUNDED (no
  clamp, below). MEASURED on boot (§H.4) — the user tracks mod trade income → treasury in the UI.
- **NO CLAMP (user directive).** The zone price passes through in full: a cheap zone drives the payment far down,
  a starved/spiking zone far up, both unbounded — the user wants the true regional signal on the boot, not a
  guessed cap. The ONLY value-guard is a strict-positive FLOOR so a good never becomes literally FREE (below).

## §WHY-DIRECT — why this is NOT written as a "regional index" (the earlier framing was redundant)
An earlier draft layered a multiplier `regional_index = zone.local_price / gbip` ON TOP of the existing
`× country_unit_price` term. But country_unit_price already = gbip/(0.5+pen), so:
```
order_size × [gbip/(0.5+pen)] × [local_price/gbip] = order_size × local_price/(0.5+pen)
                    └── gbip ──┘   └── ÷gbip ──┘   →  the gbip CANCELS
```
The "÷ gbip" did nothing but cancel the gbip already present, and it read gbip for no reason. The index framing
also MISLEADINGLY suggested a normalized deviation-from-world-average; mechanically it is just "pay local_price."
The DIRECT form above is the same result, reads no gbip, and states plainly what it does. Implement the direct
substitution, not the index.

### Where it attaches — the EXACT block (review112b findings 1+2 folded)
GT_split_update_wealth_owed_for_tradegoods (:2459) runs in the PAYING governorship's scope with `$tradezone$`
from the :2319 dispatcher. At the price multiply (:2466-2469) replace `multiply = owner.var:country_unit_price_
$good$` with country_unit_price's OWN block (:2727-2741) verbatim, swapping gbip → the paying zone's local_price:
```
multiply = {
    value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
    min = 0.0001                                     # ← FLOOR (min = floor in this engine; see below). Doubles as the strict-positive guard.
    divide = { value = 0.5  add = owner.var:country_global_market_penetration_$tradegood$ }
}
```
That is the WHOLE change. No second guard, no gbip, no Div/0 (the `0.5 +` literal keeps the divisor ≥ 0.5).

### Guards — ONE guard, and it is already in the block above
- **`min = 0.0001` on local_price = BOTH the strict-positive floor AND all that's needed.** [review112b CRITICAL
  finding 1] In THIS engine **`min` = floor, `max` = CEILING** (confirmed CURRENCY_svalues.txt:373 `min=0.05`
  floor vs :700 `max=32000` cap). An earlier draft wrote the floor as `max = 0.01` — that would CAP every zone
  price at 0.01, pinning all import payments to ~0 and DESTROYING the lever. The floor MUST be `min`. [finding 2]
  country_unit_price's `min = 0.0001` floors the NUMERATOR (gbip today; local_price after the swap) — NOT the
  divisor — so copying its block verbatim ALREADY places the strict-positive floor exactly where the design
  wants it. A never-ordered zone (local_price = 0) → floored to 0.0001 → payment strictly positive, never free.
- **NO ceiling** (user directive): a starved/spiking zone's price passes through in full — the large one-quarter
  payment is the real signal, measured on boot. See §H.4 + the §E-spike watch note below (review112b finding 3).

## ORDERING — CONFIRMED SAFE (traced :28-56; corrected for the DIRECT form per review112b finding 4)
The DIRECT form reads only TWO inputs: the paying zone's local_price and the owner's penetration. It reads NO
gbip (the whole point of §WHY-DIRECT — do not re-introduce a gbip read here). Both inputs are set for the quarter
BEFORE the payment site, in the strict driver sequence:
1. :37 `GT_set_tradegood_price_all_TZs...` → writes local_price per zone (:5901), unconditionally for all 22 zones.
2. :50 penetration (`GT_split_get_country_global_market_penetration_all`) → writes owner.country_global_market_penetration.
3. :54 `GT_split_update_wealth_owed_for_all_TZs...` → the PAYMENT site (:2459) — where the substitution attaches.
So at step 3 both local_price (step 1) and penetration (step 2) are already written → the payment reads live
values, NO stale/unset read, NO "variable used but never set" flood; a never-ordered zone gives local_price = 0,
caught by the `min = 0.0001` floor. (gbip's :47 timing is IRRELEVANT to the direct form — it is not read.) The
currency peg is computed on the SEPARATE currency on_action from country_unit_price, entirely outside this loop —
never sees the payment-site price.

## §F.2 burden of proof — DISCHARGED (AUDIT_CURRENCY_23 §H)
- (a) WHAT: at the payment site (:2466-2469), pay `zone.local_price / (0.5 + owner.national_penetration)` instead
  of `owner.country_unit_price` (= gbip/(0.5+pen)). Numerator swapped gbip→zone.local_price; SAME divisor.
- (b) WHY regional: local_price is set PER-ZONE from that zone's own supply/demand (:5901); keyed to the PAYING
  province's zone (:2319 dispatch), so conquest-correct (a conquered London province pays central_europe's price).
- (c) NO bleed: country_unit_price (the peg input, §H.1) is NOT written — we compute the payment from local_price
  at the site, leaving the variable intact. wealth_owed's consumers (§H.3, CORRECTED) are: (1) the seller-income
  pool (:3559), (2) the state reserve-capture WEIGHT for gold/silver (:5415-:5510), (3) buyer queued expenses
  (:3530). None writes silver_reserve_size or country_unit_price, so none reaches the peg (reserve_ratio is
  written only by se_CURRENCY/se_QING_REVENUE/se_QING_CANTON/se_LAND). order_size_modifier reads DEMAND+penetration,
  not wealth_owed (§G.2). The change cannot reach the peg, order sizes, penetration, or #219's zeroed AI valuation.
- Residual (measured, not assumed): total-payment-pool magnitude (§H.4) — paying local_price vs the stockpile-
  weighted world average under order-size weighting does NOT preserve the total by construction — + the
  reserve-metal strata-income DISTRIBUTION shift (§H.3 consumer 2). Both MEASURED on boot, not blockers.

## Logging (ships with the change — overnight Rule 1a / error-logging rule)
Under the existing tzprobe / ECON_LOG harness (kept from #50), emit per boot for silk + tea + grain + silver:
- the paying zone's local_price + the resulting payment price local_price/(0.5+pen), vs the old country_unit_price,
- total global_payment_pool for the good WITH vs WITHOUT the change (the §H.4 delta),
- **[review112b finding 3 — the §E zero-stockpile SILVER spike, watch explicitly]** local_price for the zones
  whose stockpile persistently sits at 0 (§E.3: China's own upper_yangtzi + yellow_sea SILVER zones). When a
  zone's stockpile = 0, GT_set_tradegood_price (:5908-5917) SKIPS the `÷stockpile` (guarded `>0`) so local_price
  = order×0.6 UNDIVIDED — an order-magnitude (order²-scale) spike. The OLD code weighted that spike OUT of the
  consumed price (empty zone → global-stockpile share 0 → dropped from gbip); the DIRECT form pays local_price
  at the site and thus RE-EXPOSES the spike for those provinces. It does NOT reach the peg (isolation holds), but
  it is a STRUCTURAL/persistent treasury-side spike for silver (not the rare war-starved case). Boot-watch: log
  Chinese silver payments for the zero-stockpile zones specifically; if they blow up treasury, the fix is to the
  UNDERLYING zero-stockpile local_price bug (§E), NOT a ceiling the user removed.
Static label strings only (no macro $param$ / # in LOG strings — log-string-macro-rule). -debug_mode gated.

## Files
- common/scripted_effects/se_GLOBALTRADE_split.txt — replace the `multiply = owner.var:country_unit_price_$good$`
  at GT_split_update_wealth_owed_for_tradegoods (:2468) with the direct `zone.local_price / (0.5 + owner.pen)`
  computation = country_unit_price's own block (:2730-2739) copied verbatim with gbip→local_price; its
  `min = 0.0001` on the numerator (now local_price, :2734) IS the strict-positive floor — ONE guard, no separate
  epsilon, NO ceiling, NO economic band. Nothing else in the price chain changes.
- common/scripted_effects/se_ECON_LOG_TZPROBE.txt (or the ECON_LOG harness) — the price + pool-delta logging.
- NO change to country_unit_price (:2734), the peg (CURRENCY_svalues.txt), gbip (:2509), local_price (:5901),
  penetration (:1991), order_size_modifier (:2026), or the income distribution (:3559).

## Review must test (adversarial)
1. Is the payment price truly geographic + conquest-correct? Confirm the paying scope's $tradezone$ is the
   PROVINCE's zone (not the owner's) — trace the :2319 switch: it dispatches on `TZ_is_<zone>_tradezone`, a
   property of the governorship's LOCATION. So a conquered London province → central_europe zone → its price,
   not China's. Verify. (review112 confirmed via se_TRADE.txt:1399/:1677 — re-confirm.)
2. Div/0 + unset: (0.5+pen) divisor reuses country_unit_price's `min=0.0001` guard? zone.local_price unset
   (never-ordered zone) handled by the epsilon floor? No new "Variable used but never set" flood — confirm ORDER:
   GT_set_tradegood_price (:5901) runs (driver :37) BEFORE wealth_owed (:2459, driver :54). (review112 + this
   session CONFIRMED the order; re-verify.)
3. Peg isolation: re-confirm country_unit_price is not WRITTEN and the peg cannot see the payment price (§H.1).
4. Total-income magnitude (§H.4): with NO clamp (user directive), the payment price is UNBOUNDED above — a
   systematically-cheap-or-dear home zone, or a war-starved zone spiking, can shift CHI's total trade income
   materially / produce a large one-quarter payment. INTENTIONALLY unbounded, MEASURED on boot (user tracks mod
   trade income → treasury in UI). Only value-guard = the strict-positive epsilon floor. Flag a genuinely
   destabilizing single-quarter spike, but do NOT re-introduce a ceiling — explicitly removed.
5. #219: does a regional wealth_owed resurrect any goods-valuation signal the vanilla trade AI reads
   (memory vanilla-trade-request-flood-open, zeroed in e3f3c2e91)? Confirm no AI diplo factor reads wealth_owed.
6. Manufactured goods: local_price for manufactured goods factors ingredient costs (:5936+). Does paying the raw
   zone.local_price for a manufactured good compose correctly (it already includes the ingredient premium), or
   does anything downstream assume the good was priced at country_unit_price? Verify.
7. Is the direct local_price substitution the right minimal form, vs the #115 "both" model (per-zone denominator
   too)? Confirm #112 and #115 are mutually exclusive at :2468 and this doc does NOT adopt #115's denominator.
