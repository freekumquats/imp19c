# Upstream Bug U4 — Re-diagnosis + Fix (branch upstream_bugs, off pristine upstream/master b78ccc1f6)

Full re-diagnosis of the four prior "upstream bug" claims (U1–U4) from scratch on a PRISTINE upstream/master
tree (no fork code), 2026-07-24, followed by an adversarial reconciliation and a behaviour-preserving fix of the
one real bug (U4). The fork has a history of misdiagnosed upstream bugs, so every claim was re-derived against
pristine code + the actual fork error.log line-counts, cross-checked by an independent agent, and adversarially
reviewed by a workflow before any code was touched.

## Method
1. Branch `upstream_bugs` created from `upstream/master` (github sobisonator/imp19c) — pristine, no fork edits.
2. Confirmed all four bug SITES exist verbatim on pristine upstream → genuinely Sobisonator's code.
3. Re-diagnosed each claim from scratch (me) + an independent agent (blind, from raw log symptoms).
4. Adversarial workflow (8 refuters + synthesis, LOG = arbiter) reconciled the diagnoses.
5. Only after 100% confidence: fixed U4 (me) + independent agent (blind) → reconciled → deep adversarial review.

## DECISIVE LOG EVIDENCE (fork error.log per-line flood counts)
```
22638  DIPLOMACY_svalues.txt line: 100
18767  CURRENCY_svalues.txt  line: 653
18228  CURRENCY_svalues.txt  line: 505/510/514/527/532/536/560  (each)
13230  CURRENCY_svalues.txt  line: 910
 5733  CURRENCY_svalues.txt  line: 381
  843  pdx_persistent_reader
   ... WEALTH_svalues.txt: ZERO occurrences
```

## FINAL RECONCILED VERDICTS (adversarial workflow wf_7f955d04-6a1)
- **U1 — WITHDRAWN / NON-BUG.** Prior notes claimed WEALTH_cost_of_living was the "127,778-error / 99.8%" flood.
  FLAT WRONG: WEALTH_svalues.txt has ZERO lines in the flood. The else-branch (12 unguarded country_unit_price_*
  reads) is unreachable dead code — its only evaluator (WEALTH_cache_national_cost_of_living, se_ECON_wealth.txt:
  1021) runs only inside `every_country { limit = { has_variable = official_currency } }` (:958-964), so the
  svalue's own line-1240 currency check always takes the if-branch; every downstream reader hits the guarded
  modifier (WEALTH_svalues.txt:1222-1234, default -0.0002). No fix. (A guard would fix nothing real.)
- **U2 — REAL upstream defect, COSMETIC no-op, NOT in the flood.** se_INCOME.txt:402-410 removes 4 undefined
  step-modifiers per category (00_economy_modifiers.txt defines only 5, disjoint sets). Failed remove = no-op;
  absent from the flood counts. No fix warranted.
- **U3 — ENGINE ARTIFACT.** 843 counts, no script file:line locator; benign engine cross-read of event grammar.
  A ~28-line BOM-reject subset is trivially fixable but yields no gameplay benefit here. No fix warranted.
- **U4 — REAL UPSTREAM BUG, the actual ~99.4% flood. FIXED.** DIPLOMACY:100 (22,638) + CURRENCY cluster
  (653/505-560/910/381). CURRENCY_svalues.txt is byte-identical fork-vs-upstream (0 diff-lines); DIPLOMACY:100 +
  its currency gate are unchanged (the 56 DIPLOMACY diff-lines are additive elsewhere) → both Sobisonator's code.
  **CORRECTED MECHANISM (both prior diagnoses had it wrong):** NOT "ungated reads on non-currency countries."
  DIPLOMACY:100 is double-gated (has_variable=official_currency + THIS=originator_country); the CURRENCY sites
  fire inside `every_in_list=currency_adopted_countries`. The real cause is currency-PARTICIPATING countries
  reading var:official_currency sub-vars (CURRENCY_national_debt_*, amt_circulated_*, gold/silver_reserve_size,
  reserve_actual_change, minting) that are UNSET / PRE-CACHE at read time = READ-BEFORE-SET on the currency scope
  (the identical 18,228 counts across 7 lines confirm a shared iteration driver). Failed reads resolve to
  engine-default 0 → no economy corruption, but the ~189k-line flood is the problem.

---

## THE FIX (common/script_values/CURRENCY_svalues.txt)
Guarded every read-before-set leaf `var:` read of an unset-able currency var with the proven idiom
`if = { limit = { has_variable = X }  <op> = var:X }` so an unset var leaves the svalue at engine-default 0
(== the value the failed read already resolved to → numerically behaviour-preserving on BOTH set and unset
paths). Sites guarded:
 - national_debt_{thousands,millions,billions}_scaled; amt_circulated_{thousands,millions,billions}_scaled
 - reserve_value_in_cash_scaled (gold/silver branches); wealth_bimetallic_both_reserves_size (gold+silver)
 - wealth_bimetallic_{gold,silver}_as_percentage; wealth_value_bimetallic_from_{gold,silver}
 - national_debt_scaled_wealth_value_millions (national_debt master)
 - reserve_value_in_cash_scaled_{silver,gold}; reserve_value_in_wealth_{silver,gold}
 - reserve_change_currency_value; {gold,silver}_reserve_actual_change_with_cashout
 - completeness: added the missing `has_variable = TZ_penetration_eastern_steppe` to the CURRENCY_power TZ guard
   (was 21/22; latent because all 22 TZ vars are co-set atomically, added for correctness)
CRLF line endings + UTF-8 BOM preserved (upstream file is CRLF; an interim scripted edit flipped to LF and was
corrected — the committed diff is purely the semantic guards, verified with git diff --ignore-all-space).

## VERIFICATION
- Two independent fixes (mine + an independent agent's) converged on the identical guard idiom; the agent's was a
  superset (caught the bimetallic both_reserves site) → adopted.
- Deep adversarial review (workflow wf_d7d5ac87-bda, 5 attack angles + judge): SHIP-WITH-MINOR-FOLLOWUP. No
  set-path regression; unset-path returns exactly 0; the conditional-only-body-defaults-to-0 idiom is proven
  against pristine siblings (CURRENCY_base_starting_reserve_gold/silver); scope correct (all country-scope vars).
  The flagged residual same-class sites were then ALSO guarded (this fix) → flood fully, not ~99%, eliminated.
- Braces 405/405. Behaviour-preserving. This is Sobisonator's upstream code; the fix belongs upstream (PR-able).
