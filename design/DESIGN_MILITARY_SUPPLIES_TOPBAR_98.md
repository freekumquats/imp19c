# DESIGN — #98 Arsenal production not contributing to Military Supplies (topbar attribution)

Status: DRAFT for adversarial review. Author: overnight run 2026-08-11. Root cause traced by audit99 (#99),
confirmed in source here.

## Diagnosis (source-verified)
Boot test: "Arsenal buildings not contributing to Military Supplies despite building many." The production is
NOT missing — audit99 + this pass confirm the named-building production terms are live (machine_works→munitions
GOODS_svalues.txt:2792, →artillery :2867, textile_mill→clothing :3121, navy_yard→naval_supplies :2951; arsenal/
depot→munitions the original hook), all folded into the quarterly stockpile write. The bug is UPSTREAM in the
TOPBAR figure:

`MILITARY_supplies_income_country` (INCOME_svalues.txt:1063-1170) = Σ over governorships of, per military good:
  `DEMAND_<good> × (1 − shortage_<good>)`  [when the shortage var exists; else just DEMAND_<good>]

This is **fulfilled DEMAND**, not production. Its ceiling is total military demand. Mechanism (audit99):
- `se_CONSUME.txt:64-113` DELETES `shortage_<good>` once the governorship's stockpile is non-negative (no
  shortage). With the var absent, the term is the flat `DEMAND_<good>` (the demand ceiling).
- So once a good is fully supplied (shortage cleared), building MORE arsenals raises the stockpile but the
  topbar term is already pinned at the demand ceiling — the extra output is silently absorbed, invisible.
- Result the player sees: "I built many arsenals, Military Supplies didn't move." Correct per the formula,
  surprising per the expectation the #71/#103 work set ("arsenal → more supplies").

## SEPARATE CONFIRMED BUG (narrow, unambiguous) — late_munitions reads the wrong shortage var
INCOME_svalues.txt:1095: inside the **late_munitions** add block, the shortage subtraction reads
`var:shortage_early_munitions` — a copy-paste from the early_munitions block just above (:1080). It should read
`var:shortage_late_munitions`. Also its outer `has_variable` guard (:1088) correctly tests shortage_late_munitions,
but the inner subtract (:1095) tests+subtracts shortage_early_munitions — so late_munitions fulfilment is docked
by the EARLY munitions shortage, not its own. Pre-existing upstream defect, distinct from the demand-cap design
question. This is a direct fix (one var name), NOT a design change.

## THE DESIGN QUESTION (#98 proper) — should the topbar reflect production above demand?
Two honest framings, and the choice changes what the number MEANS:

**Option A — LEAVE the income term as fulfilled-demand; fix only the attribution/visibility.** The topbar
"Military supplies" is an INCOME line (fulfilled military demand feeding the budget), and demand-capping is
correct for an income line: you don't earn income on supplies nobody demands. The player's real question —
"is my arsenal doing anything?" — is answered by SHOWING PRODUCTION somewhere, not by inflating the income line.
Fix = add a separate read-out (a "Military goods produced" / surplus line, or a building-tooltip term) that
surfaces `GOODS_governorship_<good>_produced` so the player sees arsenals raising output even when the income
line is demand-pinned. Keeps the income/budget math untouched (no Sobisonator-shared-logic risk).

**Option B — CHANGE the income term to credit production over demand.** Make the topbar rise with production
past the demand ceiling. This REDEFINES the line from "fulfilled demand" to "production value," inflates the
budget, and perturbs the shared income/balance math (MILITARY_supplies_balance_country:1172 feeds the topbar
change indicator + the treasury). High blast radius on Sobisonator-shared economy logic — exactly the
[[imp19c-sobisonator-upstream-caution]] trap. NOT recommended without boot data proving the income line is
where the player expects the signal.

## ⟪v2 — REVISED per dr98 (SOUND-WITH-CORRECTIONS). Supersedes the recommendation below.⟫
dr98 confirmed the demand-cap diagnosis + the line-1095 bug (both :1095 AND :1097 read shortage_early_munitions;
must be shortage_late_munitions; shortage_late_munitions IS live, so the fix is behavior-correcting, not dead),
but caught that Option A as written is WRONG:
- **C1/C2 (blocking):** a "Production by good" section ALREADY EXISTS in the topbar tooltip (MILITARY_SUPPLIES_TT,
  imp19c_tooltips_l_english.yml:237) reading MILITARY_supplies_prod_* (INCOME_svalues.txt:975-1019). But those
  svalues are the SAME `DEMAND × (1−shortage)` fulfilled-demand formula — CAPPED — and their own comment admits
  it. So the tooltip already claims to show "Production" while showing fulfilled-demand. THAT MISLABEL is the real
  #98 defect. Surfacing MILITARY_supplies_prod_* (my Option A) would just re-commit the capped number.
- **C3:** the #98 filer looked at the TOPBAR. The fix must land on the topbar tooltip, not a per-state ledger.
- The values that actually RISE with arsenals are GOODS_national_production_<good> (uncapped true production,
  GOODS_svalues.txt:638+ — confirmed to exist for all 5 military goods + artillery).

### v2 FIX (three parts, all topbar-tooltip / income-svalue local; no budget/treasury perturbation):
1. **Line-1095/1097 bug:** change both `shortage_early_munitions` reads in the late_munitions income block
   (INCOME_svalues.txt:1095, :1097) to `shortage_late_munitions`. Behavior-correcting (late_munitions fulfilment
   was docked by the EARLY shortage). dr98 C5: this shifts balance_country accumulation slightly, in the correct
   direction; only se_TEST MILITARY_update_supplies:363 reads balance_country (mutates the supplies STOCKPILE, not
   cash — dr98 C4 corrects my "budget/treasury" wording).
2. **Relabel the capped tooltip section:** "Production by good (quarterly, supplied)" → "Supplied by good
   (quarterly)" — the MILITARY_supplies_prod_* numbers ARE fulfilled-demand, so name them honestly. (Keep them —
   "how much of demand did we meet" is a legitimate legibility line.)
3. **Add a real UNCAPPED "Produced by good" section** to the same tooltip, sourced from
   GOODS_national_production_<good> (early_munitions/late_munitions/early_artillery/clothing/pharmaceuticals/
   construction_materials) — the values that rise when you build arsenals. Now a player who built arsenals and
   checked the topbar sees a number move (closes #98's actual symptom). dr98 C6: label it distinctly from the
   supplied line; GOODS_national_production_ is the mechanised+cottage total (true output), which is exactly what
   we want to show. No income-total change (Option B rejected — the income LINE stays fulfilled-demand, correct
   per its own "gains/consumes" tooltip framing).

### v2 blast radius (dr98 C4, corrected): touching MILITARY_supplies_income_country's :1095/:1097 flows to
MILITARY_supplies_balance_country (:1172) → se_TEST MILITARY_update_supplies:363, which mutates the military-
supplies STOCKPILE + the topbar change indicator (topbar.gui:818). NOT cash treasury / AI budget. Small, correct-
direction. The new "Produced" tooltip line is read-only (svalue in loc), zero sim effect.

## (superseded) RECOMMENDATION: Option A + the line-1095 bug fix.
- The line-1095 wrong-shortage-var is a clear defect → direct fix (behavior-correcting, tiny).
- For the "arsenal does nothing visible" symptom → surface PRODUCTION (not inflate income): add a read-out of
  the produced military goods so the arsenal's effect is visible, leaving the income/budget line semantically
  correct. This honours #98's user intent ("see my arsenals contribute") without the Option-B budget-inflation
  risk. The exact surface (topbar sub-line vs the building tooltip vs the Military panel) is the impl choice —
  the building tooltip is the lowest-risk, most-local home and matches #103's tech-gate-tooltip precedent.

## Adversarial-review asks
1. Is line 1095 really a bug (should be shortage_late_munitions), or is late_munitions deliberately docked by
   the early shortage for some supply-chain reason? Check whether shortage_late_munitions is even set anywhere
   (se_CONSUME) — if late_munitions never gets a shortage var, the whole late block may be dead/degenerate.
2. Option A vs B: is demand-capping actually correct for this line, or does the topbar genuinely purport to show
   production (in which case B is right despite the risk)? What does the topbar LABEL/tooltip claim it shows?
3. If Option A: where should the "produced" read-out live so it's actually seen by a player who built arsenals
   and checked the topbar? Is a building tooltip enough, or does it need a Military-panel line?
4. Blast radius of touching MILITARY_supplies_income_country at all (even the 1095 one-var fix): does anything
   else read this svalue in a way the fix would shift? (balance_country, treasury, AI budget.)
5. Any double-count risk if a "produced" read-out sums GOODS_governorship_<good>_produced (which already
   includes the building-hook infra terms)?
