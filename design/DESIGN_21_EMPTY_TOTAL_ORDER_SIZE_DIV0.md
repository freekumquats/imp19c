# DIAGNOSIS (v1, pre-review) — #21 empty total_order_size Div/0 + "failed to read divide"

## Symptom (post-fix boot Aug 18 20:11, error.log)
- 3,828× `Failed to read 'divide' for 'set_variable'` at GT_split_update_wealth_owed_for_tradegoods
  line 34 (food + luxury passes), via oa_wealth_changes.txt:445/462/479/535.
- 526× `Div/0 near` (other, non-price sites — GT_set_tradegood_price is now 0 after the Site-A fix).
- "Failed to read 'divide'" = the divisor OPERAND is EMPTY (set-but-empty), not merely 0 or unset.

## Mechanism (traced)
1. `$tz$_total_order_size_$good$` is RESET to 0 each quarter (GT_split_reset_global_TZ_variables_tradegood,
   se_GLOBALTRADE_split.txt:437-524), then ACCUMULATED by `add = var:order_size_$good$`
   (GT_split_update_TZ_order_amount_apply_change, :2402).
2. Jomini arithmetic: `empty + number = empty`. If ANY governorship's `order_size_$good$` is EMPTY,
   the running `$tz$_total_order_size_$good$` becomes EMPTY for that zone+good.
3. `order_size_$good$` is EMPTY when its source `DEMAND_$good$` scriptvalue evaluates empty (a scriptvalue
   that Div/0s or reads an unset operand yields EMPTY when staged — se_ECON_LOG.txt:1412).
4. Downstream, GT_split_update_wealth_owed_for_tradegoods divides by `$tz$_total_order_size_$good$`
   (the thinstock ratio set_variable, ~:2626-2630, and the #30 change_variable ~:2558). Their guard is
   `has_global_variable = X  AND  global_var:X > 0`. has_global_variable is TRUE for a set-but-EMPTY
   global, and `> 0` does NOT reliably evaluate FALSE on EMPTY → the guard PASSES → divide by empty →
   "Failed to read 'divide'". The 526 Div/0 are the same empty/zero total_order_size at sibling divides.

## Candidate fixes (for the design phase, after review)
- **Guard at the SOURCE (preferred):** in GT_split_update_TZ_order_amount_apply_change (:2402), only
  `add` order_size when it is a real number (set-but-empty sentinel: `has_variable = order_size_$good$
  AND var:order_size_$good$ > -999999999`), else add 0. Stops the empty from ever entering the zone total.
- **OR guard the READERS:** add the set-but-empty sentinel (`> -999999999`) to the divide guards at
  :2558 and :2626 (and any sibling), skipping the divide when total_order_size is empty.
- **OR fix the UPSTREAM emptiness:** find why `DEMAND_$good$` / `order_size_$good$` evaluates empty for
  some governorship (likely an unset-var read in the DEMAND chain) and guard THAT — the true root.

## OPEN for review (verify before fixing)
- Confirm `order_size_$good$` can actually be EMPTY (not just 0): trace GT_split_create_order_tradegood
  (~:2170) — does it set order_size from a DEMAND svalue that can evaluate empty, and is there an
  unguarded path? Which DEMAND read goes empty (first-tick unset? a Div/0 in a demand svalue)?
- Confirm `> 0` does NOT catch set-but-empty in this engine (the premise). The imp19c-logs "set-but-empty"
  note + the existing `> -999999999` sentinel idiom (se_ECON_LOG.txt) strongly imply it, but verify.
- Is #21 the same root as #20 (empty demand) or independent? If the same upstream empty demand, one
  source-guard may fix both classes.

## RESOLUTION — reader-guard shipped (reviewed CLEAN), 2026-08-19

Diagnosis PASSED adversarial review (SOUND-WITH-CORRECTIONS): the `global_var:X > 0` guard does NOT
reject a set-but-empty global, so both divides in GT_split_update_wealth_owed_for_tradegoods fired on an
empty total_order_size → 3828× "failed to read divide" + 526× Div/0.

Chose the READER-guard (candidate 2), using the PROVEN staged-scope-var idiom instead of the `> -999999999`
sentinel (which is unproven on a GLOBAL comparison — the very failure mode here):
- Stage once at the top of the effect: `set_variable GT_wo_total_order_size_tmp = 0`, then overwrite from
  the global only if `has_global_variable` (avoids reading an unset global).
- Both divide sites (the #30 change_variable ~:2597 and the thinstock ratio set_variable ~:2669) now gate
  on `var:GT_wo_total_order_size_tmp > 0` (a SCOPE-var comparison DOES reject empty) and divide by
  `var:GT_wo_total_order_size_tmp`. Removed the staging var at the effect's top-level end (all paths).

Code-review verdict: all 6 risks SOUND (no stale read — reset-to-0 every call; empty-store rejected;
site-1 numerator un-regressed; site-2 else-branch reachable; both error classes closed because Jomini
evaluates `limit` fully before the body; brace/RHS/BOM clean; trivial per-call cost). No blocking findings.

NOT the root cause: WHY total_order_size goes empty upstream (an empty `order_size_$good$` from an empty
`DEMAND_$good$`) is the same empty-demand family as #20 and is tracked there. This reader-guard stops the
flood safely and bills a correct 0 when a zone has no real orders; the upstream empty is a separate fix.
