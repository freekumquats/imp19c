# Design — Damp the CHI currency oscillation (#14 / #23 fix)

**Status:** DESIGN, not built. For adversarial review BEFORE any code. 2026-08-07.
**Diagnosis basis:** design/DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md (#14, the real mechanism);
design/DIAGNOSIS_CURRENCY_ANNUAL_SNAP.md (#23, my read-ordering theory REFUTED — #23 is a duplicate of
#14). This design implements #14's "Option 1: damp the correction amounts."

---

## 1. Problem (confirmed, not hypothesis)

CHI currency oscillates quarter-to-quarter: modest inflation → snap to the −10% deflation floor → back.
It is an **undamped full-gap feedback loop** in the upstream quarterly currency system, NOT user error,
NOT the minting amount, NOT a read-ordering bug.

**The loop (all verified in source this session):**
- `CURRENCY_private_cash_ratio` = `circ_scaled × 0.004 / private_cash_needed` (CURRENCY_svalues.txt:753).
- `deflation% = (1−ratio)/10` (L1111); `inflation% = (ratio−1)/10` (L1134). Deflation clamps at −10%
  (ratio floored at 0.01).
- Each quarter (`quarterly_apply_trade_changes_and_consume`, oa_wealth_changes.txt:335+) the system
  auto-corrects via `CURRENCY_amt_circulated_balance` (L927-948):
  - inflation branch: `subtract = CURRENCY_inflation_cash_selloff_amt` = `inflation × circ_scaled / 5`
    (L1177-1183) — pops sell inflated cash for reserve metal, REMOVING circulation.
  - deflation branch: `add = CURRENCY_deflation_money_demand_amt` = `deflation × 3000` (L1205-1210) —
    pops mint private cash, ADDING circulation.
- That balance is applied to circulation monthly by `CURRENCY_update_amt_circulated`
  (se_CURRENCY.txt:1391 → `CURRENCY_alter_amt_circulated`, writes `CURRENCY_amt_circulated_thousands`).

**Why it oscillates (both terms of the ratio move under the same loop — verified):**
1. NUMERATOR: the correction directly adds/removes circulation.
2. DENOMINATOR: circulation feeds `CURRENCY_reserve_ratio_total` (= reserve_value / total_country_cash,
   L643-658) → `CURRENCY_reserve_ratio_impact` (L376) → `CURRENCY_wealth_value_1_unit_scaled_by_reserve_ratio`
   (L280-284) → `CURRENCY_essentials_buying_power` (cost-of-living, L673-694, divides by that scaled
   unit) → `private_cash_needed` (L719-732). So a correction that moves circulation ALSO moves the
   denominator, in the same direction as the ratio it was trying to fix → over-correction → sign flip.
3. FULL-GAP, NO DAMPING: neither `selloff` nor `money_demand` closes a fraction of the gap; each tries
   to correct the entire deviation in one quarter. Correction magnitude (≈227k–300k/qtr on CHI per #14)
   ≫ the player's minting lever (50–100k), so the player cannot stabilise it and it reads as random.

The #23 magnitude finding (folded into #14): the denominator swings up to ~5× (trace bands 0-10 ↔
25-50), so the correction overshoots hard — damping must be strong, not cosmetic.

## 2. Goal

Make CHI currency **converge** to ratio≈1 over a few quarters instead of overshooting into a sawtooth.
Preserve the *direction* of the correction (still self-stabilising) and the steady-state (ratio→1 is
still the attractor); only reduce the per-quarter STEP so it stops overshooting.

**Non-goals:** do not eliminate the business cycle entirely; do not change minting, reserves policy, or
any non-CHI tag's behaviour.

## 3. Constraint & the CHI-only reality (important — read before choosing the lever)

Standing rule (`imp19c-sobisonator-upstream-caution`, `imp19c-proven-code-rule`): do NOT edit the shared
upstream currency formula on a hunch. This is no longer a hunch (reviewed diagnosis), but the rule still
demands the smallest, most isolated change.

**There is NO modifier key that scales circulation / deflation / minting** (grepped common/modifiers +
MODIFIER_svalues — none exists). So a pure "add a CHI country_modifier" fix is NOT possible; a modifier
cannot intercept these script_values. Any real fix must touch script logic. The question is WHERE, with
the least blast radius and strictest CHI-gating.

## 4. Options

> **[REVISED 2026-08-07 after adversarial review — see §4.0]** The first draft of Option 1 damped the
> factor inside `CURRENCY_amt_circulated_balance` (the circulation channel) ONLY. That was REFUTED: the
> correction has TWO parallel channels each quarter, and the balance is only one of them. The corrected
> Option 1 (§4.1) damps at the shared *amount* svalues, which feed both channels. §4.0 explains why.

### 4.0 Why the first-draft insertion point (`amt_circulated_balance`) was WRONG
Verified against source: each quarter's correction signal drives **two** state updates, both invoked
from `quarterly_apply_trade_changes_and_consume`:
- **Circulation channel** — `CURRENCY_update_amt_circulated` (oa_wealth_changes.txt:351) reads
  `CURRENCY_amt_circulated_balance` (CURRENCY_svalues.txt:927-948), which sums the two correction terms.
- **Reserve buy/sell channel** — `CURRENCY_private_purchase_or_sell_reserves` (oa_wealth_changes.txt:349,
  runs FIRST) changes gold/silver reserve size via `CURRENCY_reserve_accumulation_rate_from_inflation_or_deflation`
  (CURRENCY_svalues.txt:1230), which reads `CURRENCY_inflation_precious_metal_reserve_bought` (L1197→L1200)
  and `CURRENCY_deflation_money_bought_precious_metal_sold` (L1222→L1225) — both built from the **raw**
  `CURRENCY_inflation_cash_selloff_amt` / `CURRENCY_deflation_money_demand_amt`, NOT from
  `amt_circulated_balance`.

The reserve channel is a **primary denominator driver**: reserve size is the numerator of
`CURRENCY_reserve_ratio_total` (L643) → `reserve_ratio_impact` (L376) →
`wealth_value_1_unit_scaled_by_reserve_ratio` (L280) → `essentials_buying_power` divides by it (L694) →
`private_cash_needed` (L719, the deflation/inflation denominator). So damping only the balance leaves the
reserve leg swinging the denominator at full magnitude — the fix would not stop the −10% snap.

Also (verified): the balance is applied **quarterly** (L351, inside the quarterly pulse), NOT monthly —
the "monthly" in the earlier draft and the `# Called: Monthly` comment at se_CURRENCY.txt:1393 are stale.
And `amt_circulated_balance` is ALSO read by the monthly mint gate (oa_wealth_changes.txt:115-118,
`balance > 0.5 | <= -0.5`) — a further reason NOT to damp it there (it would shift when minting fires).

### 4.1 Option 1 (CORRECTED, RECOMMENDED) — damp inside the two shared AMOUNT svalues
Bake the CHI-only factor into `CURRENCY_inflation_cash_selloff_amt` (L1177) and
`CURRENCY_deflation_money_demand_amt` (L1205) themselves. These two svalues have exactly four consumers —
verified by grep: the circulation balance (L937/946), the reserve buy/sell (L1200/1225), and the two
`_display` svalues (L1188/1213). Damping at the definition propagates to **all four coherently**: both
channels throttle together, AND the player-facing display honestly shows the damped number.

```
CURRENCY_inflation_cash_selloff_amt = {
    value = CURRENCY_amt_circulated_inflation
    divide = 5
    multiply = CURRENCY_amt_circulated_scaled
    multiply = CURRENCY_swing_damping_factor      # NEW: 1.0 for all tags, 0.25 for CHI
}
CURRENCY_deflation_money_demand_amt = {
    value = CURRENCY_amt_circulated_deflation
    multiply = 3000
    multiply = CURRENCY_swing_damping_factor      # NEW
}
CURRENCY_swing_damping_factor = {                 # NEW svalue in a MOD-owned file, default 1 = global no-op
    value = 1
    if = { limit = { tag = CHI }  value = 0.25 }  # CHI closes ¼ of the gap/quarter
}
```
- **Blast radius:** non-CHI tags multiply by 1.0 → byte-identical output on ALL four consumers → zero
  behaviour change for any other tag. (`tag = CHI` in a script_value limit is valid — precedent
  DIPLOMACY_svalues.txt:368.)
- **Why it damps the whole loop:** it throttles the correction at the single point upstream of BOTH the
  circulation and reserve channels, so both the ratio numerator (circulation) and the reserve-driven
  denominator (`private_cash_needed` via reserve_ratio) are damped together — the actual root, not a
  symptom.
- **Steady state preserved:** at ratio=1 both amounts are 0, so the factor is irrelevant there; ratio=1
  remains the fixed point. The factor only shrinks the per-quarter step.
- **Display honesty:** because the `_display` svalues read the (now-damped) amount, the tooltip shows the
  true damped flow — no desync between what the player sees and what happens.
- **Risk:** still an edit to shared-file svalues, but the change is one `multiply =` line in each of two
  defs plus one new MOD-owned svalue; provably no-op for every non-CHI tag.

### Option 2 — deadband (only correct when |ratio−1| > ~0.03)
Gate the correction so small deviations don't fire. Kills trade-noise nudging but NOT the large
overshoot that produces the −10% snap (the snap is a big deviation, which a deadband still lets through
at full magnitude). Weaker for THIS symptom. Could layer on top of Option 1 but not alone.

### Option 3 — per-quarter cap (correction ≤ X% of circulation)
Simple bound, but doesn't fix full-gap targeting; a cap set low enough to stop the snap also cripples
legitimate correction. Inferior to Option 1's proportional damping.

### Option 4 — CHI-only reversal/smoothing effect in a Qing pulse
Add a Qing-only monthly effect that partially reverses the applied correction. Hacky (fights the shared
system after the fact), double-bookkeeping, and easy to desync. Rejected.

**Recommendation: Option 1 (§4.1, corrected)** — damp both amount svalues by a CHI-only factor.

**Convergence caveat (from review — do NOT overstate).** "Closes 25%/quarter → converges in ~4 quarters"
is loose: geometric decay leaves 0.75⁴≈32% of the gap after a year. More importantly, the loop has the
built-in overshoot mechanism (more circulation → higher `private_cash_needed` → lower ratio) PLUS the
reserve channel, so the effective loop gain is not analytically proven < 1 even at 0.25. Treat 0.25 as a
STARTING factor to boot-test, not a proven convergent value. If the trace still oscillates, lower the
factor (0.15, 0.1); if it converges too sluggishly (persistent mild deflation), raise it. The fix is
correct in FORM (throttle both channels at the shared amount); the exact factor is empirical.

## 5. Open questions for review
1. **Is `tag = CHI` valid in a script_value `limit`** in this engine/scope (country scope)? (Believe yes
   — used widely — but confirm; if not, use `has_variable = <CHI-only flag>` set at game start.)
2. **Does damping the deflation `money_demand` term risk leaving CHI in *persistent* mild deflation**
   (under-correcting)? At factor 0.25 it still corrects fully over ~4 quarters; verify it converges, not
   just oscillates slower. Consider asymmetric factors (damp inflation-selloff and deflation-demand
   differently) only if boot-test shows a residual bias.
3. **Interaction with `reserves_frozen`:** the correction is already skipped when reserves are frozen
   (L933/943). Damping composes cleanly (factor only applies when the branch fires). Confirm no
   double-gate issue.
4. **Is `CURRENCY_amt_circulated_balance` read anywhere else** besides the monthly apply
   (se_CURRENCY.txt:1396)? If it feeds a display or another consumer, damping changes what they show —
   grep before building.
5. **Numerator vs denominator sufficiency:** §1 argues damping circulation tames both terms. Confirm the
   denominator's cost-of-living swing is genuinely circulation-driven (via reserve ratio) and not
   dominated by an independent trade-wealth term that damping won't touch — if the latter, Option 1
   reduces but may not eliminate the swing, and we'd add a denominator-smoothing follow-up.

## 6. Test plan
- Build Option 1 (factor 0.25), boot CHI `-debug_mode` ~3 in-game years.
- Read #28 CURR trace: ratio should approach 1 and STAY in a narrow band (no more 0-10 ↔ 25-50 needed
  swing forcing the floor); deflation/inflation % should be small and non-oscillating.
- Confirm non-CHI tags unchanged (spot-check one AI monetary tag's trace = identical to pre-fix).

## 7. Evidence files
- `common/script_values/CURRENCY_svalues.txt` — L280-284, L643-658, L673-694 (denominator coupling),
  L753-765 (ratio), L927-948 (balance = the edit site), L1111-1146 (defl/infl %), L1177-1210 (the two
  correction amounts = the damping targets).
- `common/scripted_effects/se_CURRENCY.txt` — L1371-1400 (mint + apply balance to circulation).
- `common/on_action/economy/oa_wealth_changes.txt` — L111-133 (monthly), L335+ (quarterly apply).
- Diagnosis: DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md (#14) + DIAGNOSIS_CURRENCY_ANNUAL_SNAP.md (#23, refuted).
