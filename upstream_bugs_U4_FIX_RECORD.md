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
  **CORRECTED MECHANISM (re-investigated 2026-07-24 — supersedes the earlier "read-before-set" label, which was
  WRONG):** The reader `CURRENCY_total_country_cash_scaled_for_reserve_ratio` (CURRENCY_svalues.txt:660) does
  `var:official_currency = { every_in_list = currency_adopted_countries { add = CURRENCY_total_country_cash_scaled } }`
  — it iterates ALL members of the currency's `currency_adopted_countries` list (125 tags added at setup,
  se_CURRENCY.txt:7-212) with NO `has_variable` re-gate on each member, and reads that member's
  CURRENCY_national_debt_*/amt_circulated_*/gold_reserve_size (CURRENCY_total_country_cash_scaled →
  national_debt_scaled + amt_circulated_scaled; the reserve branch reads gold/silver_reserve_size). The SEEDERS
  (CURRENCY_create_starting_currencies amount-sweep se_CURRENCY.txt:932, CURRENCY_setup_all_reserves reserve-sweep)
  seed via `every_country { has_variable = official_currency }`. So any adopter-list member that `every_country`
  does NOT enumerate (a stale list entry / landless / dead-but-still-listed country) is never seeded, yet is
  still iterated by the reader → the read fails.
  DECISIVE EVIDENCE this is a COVERAGE/STALENESS gap, NOT a timing race: (a) setup ORDER puts both seeders
  (setup lines 260 + 2254) BEFORE the CURRENCY_power/reserve reads (line 2280+), so seeded countries already have
  their vars when read; (b) all 7 vars (6 debt/circulation + gold_reserve_size) error at an IDENTICAL 9,114 count,
  and at BOTH 01:31 (setup) AND 01:41 (monthly CURRENCY_update_amt_circulated tick) — a timing race would give
  varying per-var counts, whereas an identical fixed count = the same deterministic set of unseeded/stale list
  members hit every pass. Failed reads resolve to engine-default 0 → no economy corruption; the ~189k-line flood
  is the only harm. (DIPLOMACY:100 is a downstream reader of the same chain via CURRENCY_power.)
  The has_variable guard fix is correct REGARDLESS of exactly why a member is unseeded: an unseeded member now
  contributes 0 (== what the failed read already yielded). A deeper alternative fix — re-gate the reader's
  every_in_list on has_variable, or prune stale adopters — is upstream-structural and out of scope for a
  minimal flood-fix; noted for a possible upstream PR discussion.

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

---

# AREA TO INVESTIGATE (not yet fixed): U-trade — b78ccc1f6 wealth_owed multiply typo

## STATUS
OPEN — flagged 2026-07-25 during the 1763-branch upstream review. Present on THIS branch (upstream_bugs
is built on upstream/master, so b78ccc1f6 is an ancestor). The 1763 branch (merge-overnight) does NOT
have it — its GT_split_update_wealth_owed_for_tradegoods still uses the correct two-multiply form.

## THE COMMIT
b78ccc1f6 "Condense multiplication calls for wealth_owed_for_$ ... from 2 to 1"
Author/committer: Sobisonator <chombasew@gmail.com>, Thu 23 Jul 2026 19:41:42 +0100 (direct commit, not a PR).

## THE BUG
In GT_split_update_wealth_owed_for_tradegoods (common/scripted_effects/se_GLOBALTRADE_split.txt) the
author meant to condense two sequential multiplies into one block. Intended (behaviour-preserving) form:
    multiply = { value = owner.var:country_unit_price_$tradegood$  multiply = owner.var:order_size_modifier_$tradegood$ }   # = price * modifier
What was committed instead:
    multiply = { value = owner.var:country_unit_price_$tradegood$  add      = owner.var:order_size_modifier_$tradegood$ }   # = price + modifier
i.e. an `add` where `multiply` was meant. The engine block computes the inner expression then multiplies
the target by it, so wealth_owed changed from
    order_size * price * modifier   (correct)  ->  order_size * (price + modifier)   (wrong).

## WHY IT'S WRONG (both trees)
order_size_modifier_$tradegood$ is a <=1 FULFILMENT FRACTION (share of demand the market can supply;
GT_split_get_order_size_modifier_tradegood sets it to a fraction, clamps >1 to 1, else 1). It must MULTIPLY
the owed wealth (scale unfulfilled orders DOWN). Adding a ~0..1 fraction to a (much larger) unit price both
fails to scale down shortfalls AND spuriously inflates the price term. Not context-dependent — the
order_size_modifier function is shared, un-forked code, so the semantics are the same upstream.

## PROVEN ENGINE SEMANTICS (verified in-file)
- `multiply = { value = 1  subtract = X }` -> multiply by (1 - X)  [se_GLOBALTRADE_split.txt:2472, 5094]
- correct two-multiply condense: `multiply = { value = A  multiply = B }` -> A*B  [se_ECON_wealth.txt:525-527]

## FIX (when we act)
Change the committed `add =` back to `multiply =` in that one block. One-line semantic fix. PR-able upstream
(same class as the U4 guards — Sobisonator's own code). Verify order_size_modifier is still a fraction at
the time of merge, then re-check trade-wealth figures against a pre-b78ccc1f6 baseline.
