# DESIGN — a zero-stockpile trade zone has no valid local price; skip its contribution to payment instead
# of substituting a fabricated or borrowed price. Preserves #112/#115's regional pricing unconditionally.
# REV 3: guard the STOCKPILE condition directly at the ONE payment site; leave `local_price_$tradegood$`
# itself completely untouched everywhere else (zero blast radius on its ~24 other readers).

## Task
Persistent ~-10% deflation (tracked in `audits/AUDIT_CURRENCY_23.md`, §I.10-I.17). Commit `2b7142977`
(#112) isolated at the LINE level (§I.12) as removing a stockpile-weighting protection at one call site.
Per user instruction: identify the single most-likely line and change it conservatively, preserving
#112/#115's regional-pricing feature, then let a boot confirm/refute empirically — exact magnitude proof
is not required first.

## Revision history (why this is REV 3, not REV 1)
- **REV 1** proposed falling back to the pre-#112 national blended price when a zone's stockpile is
  empty. REJECTED by the user on economic grounds: a zone with zero stockpile made NO sale, so there is
  no real transaction to price at all — substituting any price (even a safe national average) bills for
  a sale that didn't happen.
- **REV 2** proposed leaving `local_price_$tradegood$` UNSET when stockpile is empty, plus a
  `has_global_variable` guard at the payment site to skip an unset price. An adversarial review found TWO
  blocking defects: (1) the guard's proposed syntax (`has_global_variable = OBJECT.INNER`, a dotted form)
  does not exist anywhere in this codebase and would either fail to parse or silently evaluate false on
  every call, zeroing ALL trade-expenditure — worse than the bug it fixes; (2) leaving `local_price` unset
  has a MUCH wider blast radius than assumed: it is read, unguarded, by the manufactured-goods raw-input-
  cost pass (`PRICE_factor_raw_input_costs_$tradegood$`, `se_PRICE.txt`, a `change_variable` with no
  existence guard — would hit the exact unset-var class `#107` was written to prevent) AND by the
  purchase-spend path (`se_PURCHASE.txt:1267,1279,1284`), neither of which the design accounted for.
- **REV 3 (this document)** eliminates both defects by not touching `local_price_$tradegood$`'s setter or
  existence AT ALL. Every other reader (the 22-zone world-price blend, the manufactured-goods pass, the
  purchase-spend path) is completely unaffected — `local_price` is always set exactly as it is today. The
  ONLY change is at the ONE payment site (`GT_split_update_wealth_owed_for_tradegoods`), which is guarded
  on the SAME stockpile condition `GT_set_tradegood_price` already uses for the identical purpose one
  function away, using the SAME proven, bare `has_global_variable = NAME` syntax already shipped there —
  not a new or invented trigger form.

## Root cause (unchanged from REV 1/2, restated for a stable reference)

`GT_set_tradegood_price` (`common/scripted_effects/se_GLOBALTRADE_split.txt:6000-6032`) sets a tradezone's
`local_price_$tradegood$` as `order_size / stockpile × 0.6` (plus a food-goods divisor), guarded so the
divide is SKIPPED when `$tradezone$_stockpile_$tradegood$` is unset or `<=0` (`:6011-6014`, the `#107`
Div/0 fix). When skipped, the variable is STILL written — to the raw, un-normalized order count. This
design does not change that function at all (see "Revision history" above for why REV 2's attempt to
change it was wrong).

The one place this raw number becomes a real currency drain is `GT_split_update_wealth_owed_for_
tradegoods` (`:2498-2577`), `#112`/`#115`'s payment-site rewrite:

```
change_variable = {
    name = wealth_owed_for_$tradegood$
    multiply = {
        value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
        min = 0.0001
        divide = { value = 0.5  add = owner.var:TZ_penetration_$tradezone$ }
    }
}
```
(`:2535-2545`.) `min = 0.0001` only guards the LOW side. This flows into `wealth_owed_for_$tradegood$` →
`trade_expenses_due_*` → `TRADE_national_expenditure` → `CURRENCY_trade_wealth_outgoing_currency_value` →
`CURRENCY_private_cash_needed`, draining circulation against a transaction that, per the user's economic
argument, never happened.

## Fix — ONE change, at ONE site, reusing a proven guard verbatim

`GT_split_update_wealth_owed_for_tradegoods` (`:2498-2577`) — wrap the existing price-multiply in the
SAME stockpile check `GT_set_tradegood_price` already uses (`:6011-6014`), using the bare
`has_global_variable = NAME` form actually proven at that site (NOT a dotted/object-scoped form — REV 2's
mistake):

```
if = {
    limit = {
        has_global_variable = $tradezone$_stockpile_$tradegood$
        global_var:$tradezone$_stockpile_$tradegood$ > 0
    }
    change_variable = {
        name = wealth_owed_for_$tradegood$
        multiply = {
            value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
            min = 0.0001
            divide = { value = 0.5  add = owner.var:TZ_penetration_$tradezone$ }
        }
    }
}
else = {
    # [fix] the paying zone has no stockpile to sell from this quarter -- no sale occurred, so no expense
    # is recorded for it (mirrors GT_set_tradegood_price's own #107 guard at :6011-6014, same condition,
    # same tradezone/tradegood pairing). Zeroed, not skipped: the order_size_modifier/power_trade_bonus
    # multiplies below and the payment-pool adds still run on a correctly-zeroed wealth_owed, exactly like
    # every other tradegood's code path -- no special-cased skip of downstream effects.
    change_variable = {
        name = wealth_owed_for_$tradegood$
        multiply = 0
    }
}
```

This is the literal condition already proven at `:6011-6014` — same two clauses (`has_global_variable` +
`> 0`), same variable name pattern (`$tradezone$_stockpile_$tradegood$`), copied verbatim, not invented.
`local_price_$tradegood$` itself is read EXACTLY as it is today when the guard passes; nothing about its
value, its existence, or any other reader of it changes in any way.

**`order_size_$tradegood$` asymmetry — corrected per adversarial review.** `wealth_owed_for_$tradegood$`
starts as a copy of `order_size_$tradegood$` (`:2501-2504`), and this fix only changes `wealth_owed`'s
later multiply, not `order_size` itself — so a zone can still show a nonzero `order_size` while paying
zero import cost for it. An earlier draft of this doc claimed `global_supply_as_percentage_of_order_
$tradegood$` (`:3542-3554`) damps a zero-stockpile zone's OWN `order_size` toward 0, making this "not a
new asymmetry." **That claim is WRONG and is retracted:** `global_supply_as_percentage_of_order_
$tradegood$` (set at `:2922-2939`) is a single WORLD-AGGREGATE ratio (`global_stockpile_$tradegood$` ÷
`global_order_total_$tradegood$`), applied uniformly to every zone — one zone's own zero stockpile does
NOT drive this term toward 0 by itself; the whole world's supply would have to run short. So a zone can
retain a fully nonzero `order_size` even after `:3542-3554`, and (confirmed by the review) `order_size`
also feeds a SEPARATE expense channel, `queued_trade_expenses_due_shipping` (`:5262`), which this fix does
NOT zero. **The honest statement: this fix zeros only the IMPORT-payment path (`wealth_owed_for_
$tradegood$`) for a zone with no stockpile to sell from; the shipping-expense path from the same zone's
`order_size` is untouched and pre-existing, not introduced by this fix.** Low severity (not part of the
deflation mechanism traced in §I.10-§I.17, and not a crash risk), but the reasoning above corrects the
prior draft's false damping claim so it is not relied on in any future change.

## What this does NOT change (now genuinely zero blast radius elsewhere)
- `GT_set_tradegood_price` — UNCHANGED. `local_price_$tradegood$` is written exactly as today, always a
  number, never unset, for every zone/good/quarter. REV 2's manufactured-goods and purchase-path risks
  (found by review) do not apply because nothing about this variable's existence changes.
- The 22-zone world-price blend (`GT_split_get_global_import_unit_price_tradegood`, `:2585-2745`),
  the manufactured-goods raw-input-cost pass (`PRICE_factor_raw_input_costs_$tradegood$`, `se_PRICE.txt`),
  and the purchase-spend path (`se_PURCHASE.txt:1267,1279,1284`) — all read `local_price` exactly as they
  do today. None of these are touched, guarded, or affected by this fix in any way.
- Every zone WITH stock (the common case, and the case #112/#115 were built for) is completely unaffected
  — the `if` branch, unchanged from #112/#115's shipped code, is what runs for them.
- #115's per-zone `TZ_penetration` denominator is untouched in both branches.
- The currency peg (`CURRENCY_essentials_buying_power`/`country_unit_price`) never reads `local_price`
  directly, unaffected either way (peg isolation, already established by #112/#115, unchanged).
- No new variable, no new svalue, no new cache, no fallback price of any kind.

## What this does not resolve
Four analysis cycles on the existing log (§I.10-§I.17) could not conclusively attribute `need`'s full
swing to this mechanism alone versus `country_population`/`wealth_generated`/other inputs — not required
before this change per user instruction. Separately open (noted, not resolved by this fix): whether
`upper_yangtzi`'s PERMANENT zero-silver-stock across all 29 logged quarters is itself downstream of a
different, upstream production/seeding defect, or is simply a zone that legitimately never stocks silver
— this fix correctly stops mis-pricing that state either way, but does not diagnose why the state exists.
Measure the result on the next boot via the exact-tick logging already added (`natexp`, `wvuraw`,
`poptick`, `wealthgen`, rescaled `need` — §I.12/§I.15) plus the back-solve cross-check (§I.16/§I.17).

## Boot-crash checklist
- The guard is a bare `has_global_variable = NAME` + `NAME > 0` — the EXACT proven form already shipped
  one function away (`:6011-6014`) for the identical variable-name pattern. Not a new trigger form (unlike
  REV 2's rejected dotted syntax).
- The `else` branch's `multiply = 0` always produces a valid number; `wealth_owed_for_$tradegood$` is never
  left unset or wrong-typed, so no downstream reader (`GT_split_scale_wealth_owed_and_order_size_
  tradegood`, `:3526-3616`) can hit an unset-var or Div/0 from this change.
- None of the 4 established imp19c boot-crash pattern classes (create_character grant-to-self,
  scripted_gui compile-inline recursion, ownerless capital, schema-invalid law-option field) apply.
- No dotted/object-scoped existence-check syntax anywhere in this design (REV 2's blocking defect) — the
  only existence check used is the literal, already-proven bare form.
