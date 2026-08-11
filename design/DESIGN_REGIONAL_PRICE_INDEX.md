# DESIGN — regional price index (per-zone import price divergence), replacing the reverted #50

**Status:** REVIEWED SOUND-WITH-CORRECTIONS 2026-08-11 (review112). Both sink-risk checks PASS: ORDERING
(:37→47→52→54, index reads live local_price+gbip) and PEG ISOLATION (peg reads country_unit_price + reserve_ratio;
neither touched — provably the correct side of the peg, unlike #50). Two proof errors CORRECTED (not design
changes): §H.3 re-enumerated wealth_owed's real consumers (it also feeds the gold/silver reserve-capture WEIGHT
+ buyer queued expenses, NOT "only the pool" — but none reaches silver_reserve_size/the peg, so the conclusion
holds); and the "total pool preserved by construction" claim is downgraded to "measured on boot" (index averages
to 1 under stockpile-weighting but is applied under order-weighting). IMPLEMENTATION-READY; boot-measurement
checklist = total-pool delta + reserve-metal strata-income shift. Delicate UPSTREAM code — cautious pattern.
Clears AUDIT_CURRENCY_23 §F.2 (§H). See [[currency-swing-diagnosis]].
CLAMP REMOVED (user directive 2026-08-11): the [0.25,4.0] clamp was NOT upstream — it was MY OWN addition to the
NEW regional_index term I'm introducing. Removing it touches nothing upstream and does NOT reopen the review112
safety story (ordering + peg-isolation are independent of the clamp; the clamp only bounded the new term's
magnitude). The index is now UNBOUNDED except for a strict-positive epsilon floor so a good never goes free
(user: "it should only prevent goods from going to 0"). Metals stay IN the index (user: do not exempt gold).

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

### Where it attaches
GT_split_update_wealth_owed_for_tradegoods (:2459) already runs in the PAYING governorship's scope and receives
`$tradezone$` (from the :2319 switch dispatcher). At the price multiply (:2466-2469), replace the
`multiply = owner.var:country_unit_price_$good$` with the direct computation:
`zone.local_price ÷ (0.5 + owner.penetration)`, where zone.local_price =
`global_var:global_$tradezone$_tradezone.var:local_price_$good$` and owner.penetration =
`owner.var:country_global_market_penetration_$good$`. This keeps the exact divisor country_unit_price used
(:2740-2746, `0.5 + penetration`, min 0.0001), just with local_price as the numerator instead of gbip.
Guard against Div/0 on the (0.5+pen) divisor exactly as country_unit_price does (min 0.0001). NO clamp on the
resulting price — only the strict-positive floor below.

### Guards (ONLY these two — no tuning band)
- **(0.5 + penetration) divisor** → reuse country_unit_price's own `min = 0.0001` guard (:2741) so the divisor is
  never 0 — CRASH protection, not a tuning band; stays regardless.
- **strict-positive FLOOR so a good is never literally FREE (user directive: "it should only prevent goods
  from going to 0").** If the paying zone's local_price = 0 (empty/never-ordered zone) the payment price would be
  0, which would zero the payment (a free import). Floor the zone price just above 0 with a tiny epsilon (e.g.
  `max = 0.01` on the local_price read) — NOT an economic floor. The point is only to keep the payment strictly
  positive, not to bound how cheap a real cheap zone gets. NO ceiling: a starved/spiking zone's price passes
  through in full (that large one-quarter payment is the real signal, measured on boot).

## ORDERING — CONFIRMED SAFE (the finding most likely to sink this; traced :28-56)
The quarterly driver GT_split_do_global_trade_split runs a STRICT sequence, so every input the payment reads is
set for the quarter BEFORE the payment site:
1. :37 `GT_set_tradegood_price_all_TZs...` → writes local_price per zone (:5901).
2. :47 `GT_split_get_global_import_unit_price_all` → writes gbip (:2509).
3. :50-52 penetration → order_size_modifier → country_unit_price (:2734).
4. :53-55 `GT_split_update_wealth_owed_for_all_TZs...` → the PAYMENT site (:2459) — WHERE THE INDEX ATTACHES.
So at step 4 both local_price (step 1) and gbip (step 2) are already written → the index (local_price÷gbip)
reads live values, NO stale/unset read, NO "variable used but never set" flood. (The bimetallic metals-pass
QING_BIMET_pull at :46 also runs between local_price and gbip — the index reads the post-pull local_price, which
is correct.) The currency peg is computed on the SEPARATE currency on_action from country_unit_price, entirely
outside this loop — never sees the payment-site price.

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
so the boot confirms the regional spread is sane and the total-income shift is bounded. Static label strings only
(no macro $param$ / # in LOG strings — log-string-macro-rule). -debug_mode gated.

## Files
- common/scripted_effects/se_GLOBALTRADE_split.txt — replace the `multiply = owner.var:country_unit_price_$good$`
  at GT_split_update_wealth_owed_for_tradegoods (:2468) with the direct `zone.local_price / (0.5 + owner.pen)`
  computation (reuse country_unit_price's own `min = 0.0001` divisor guard, :2741) + the strict-positive floor
  (epsilon, e.g. max=0.01 on the local_price read) — NO ceiling, NO economic band. Nothing else in the price chain changes.
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
