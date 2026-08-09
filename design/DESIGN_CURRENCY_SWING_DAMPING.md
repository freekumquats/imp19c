# Design — Damp the CHI currency oscillation (#14 / #23 fix)

**Status: REFUTED 2026-08-08 by adversarial review — DO NOT BUILD Option 1. The mechanism this
doc pins the swing on is UNREACHABLE for CHI, and the proposed fix targets terms too small to
matter. Kept for the record + the corrected diagnosis below. See §0.**

## 0. REFUTATION (adversarial review, 2026-08-08) — read first

Option 1 is SAFE (provably non-CHI no-op, correct wiring) but WRONG (aimed at the wrong terms). Two
load-bearing errors:

**C1 — the "~5× amplifier" is unreachable for CHI.** `CURRENCY_reserve_ratio_impact` (CURRENCY_svalues.txt:376-397)
returns `ratio×(5−ratio)` ONLY inside an `if` requiring BOTH `has_variable = public_debt_administration`
AND `reserve_ratio_total < 1`. CHI has NEITHER: PDA is hard-coded to GBR/FRA/SPA/RUS only
(se_CURRENCY.txt:954-969), and CHI's reserve_ratio ≈ 1.4 (>1). CHI ALWAYS takes the `else` = `÷3`
(gain 1/3 < 1, low-gain). The repo already recorded this (overnight_abstract_meters.md:332); this doc's
§1/§4.0 amplifier claim CONTRADICTS an established finding. My re-trace added the amplifier without
checking CHI can reach the branch — it can't.

**C2 — the swing is DENOMINATOR-driven; the damping factor touches none of it.** The ratio =
`circ×0.004 / private_cash_needed`. The numerator (circulation ~46M) barely moves — the two correction
amounts are ~0.6% nudges (`deflation×3000` ≤ ~300 on ~46,140; reserve moves ~0.4%). The ratio craters
1.5→<0.1 because `private_cash_needed` EXPLODES: `essentials_buying_power` (L673-701) = Σ~12
`country_unit_price_*` ÷ `wealth_value_1_unit_scaled_by_reserve_ratio`, CAPPED at 32000, and
`private_cash_needed`'s divisor floored at min=0.01 (L762). When `country_unit_price_silver` (→
`wealth_value_1_unit`) dips on a trade pass, essentials slams the 32000 cap → `needed` blows up → ratio
hits the deflation floor; next pass it snaps back. This is a **trade-price / cost-of-living CAP
nonlinearity**, NOT the currency-correction feedback loop. Option 1's factor multiplies only
`selloff_amt`/`money_demand_amt` — it does NOT touch `country_unit_price_*`, `essentials_buying_power`,
the 32000 cap, or `wealth_value_1_unit`. Expected effect on the swing: **negligible.** No factor value
(0.25/0.1/0.01) helps — don't ship-and-iterate; it would burn boots chasing the wrong term.

**Also:** §4.0's mint-gate argument is faulty (balance is DERIVED from the amounts, so damping them
shifts the gate identically — M1); "exactly four consumers" undercounts (the raw amounts are also read
by inflation_tooltip/deflation_tooltip ×1000 — M2). And PDA IS reachable for CHI mid-game
(se_QING_NAPOLEON.txt:268 unlocks the tech; establish_public_debt_administration decision) — if CHI ever
gets PDA and circulation grows so reserve_ratio<1, it enters the REAL amplifier and the swing could
worsen (L2).

**NEXT (correct path):** re-diagnose with a boot-trace that DECOMPOSES `private_cash_needed` — is
`essentials_buying_power` pinned at the 32000 cap? is `country_unit_price_silver` the swinging input? —
and logs `selloff_amt`/`money_demand_amt` vs `amt_circulated_scaled` to confirm the correction terms are
tiny. Let THAT data pick the fix site (essentials/wealth_value_1_unit/cap side, or trade-price
stability), not the refuted amplifier theory. ALSO ties to #71: if M1 (46M) is ~14× too high vs the ~3.2M
chuan the historical 3.2bn wén implies, the ratio scale itself is off and may interact with the cap.
Extend the CURX probe to log essentials_buying_power (+ whether it's at cap) and country_unit_price_silver.

The original (now-refuted) design follows unchanged below for the record.

---

**Status:** DESIGN, not built. For adversarial review BEFORE any code. 2026-08-07.
**Diagnosis basis:** design/DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md (#14, the real mechanism);
design/DIAGNOSIS_CURRENCY_ANNUAL_SNAP.md (#23, my read-ordering theory REFUTED — #23 is a duplicate of
#14). This design implements #14's "Option 1: damp the correction amounts."

---

## 1. Problem (confirmed, not hypothesis)

CHI currency oscillates quarter-to-quarter: modest inflation → snap to the −10% deflation floor → back.
It is an **undamped full-gap feedback loop** in the upstream quarterly currency system, NOT user error,
NOT the minting amount, NOT a read-ordering bug.

**[PROBE-CONFIRMED 2026-08-08 boot 01:19]** The rewritten literal-band CURX probe (the digit-decomposition
version was broken; this one works) captured the ratio time-series directly. It oscillates between the
EXTREMES with almost no middle band:
`ratio 1.20-1.50 → <0.01 (floor) → 1.20-1.50 → >=1.50 → <0.01 ×4 → >=1.50 ×2 → 0.01-0.10 (defl FLOOR ~-10%) ×4 → >=1.50 ×2 → <0.01 ×2 → >=1.50 ×2 …`
i.e. STRONG INFLATION (≥1.5) ⇄ DEFLATION FLOOR (<0.1), quarter to quarter, essentially never resting in
the healthy 0.75–1.05 band. Both `CURX defl 8-10pct` and `CURX infl ≥10pct(cap)` appear in the same run =
both rails are being hit. This is the reported symptom, now MEASURED — the undamped-overshoot diagnosis
below is no longer inference. (Also confirmed: the trade term `trout` is a small NEGATIVE inflow band here,
so #53's display bug is NOT the swing driver — the swing is the reserve/cost-of-living loop below.)

**Amplifier identified (this session's re-trace):** `CURRENCY_reserve_ratio_impact` (L376-388) returns
`ratio × (5 − ratio)` when `reserve_ratio < 1` — a gain up to ~5× at small ratios — and it is the term that
divides cost-of-living (`essentials_buying_power`, L694). So a modest quarterly reserve change is amplified
into an EXTREME cost-of-living swing → extreme `private_cash_needed` swing → the ratio craters/spikes. This
steep gain is why the correction overshoots to the opposite rail rather than converging. The damping factor
(§4.1) throttles the correction feeding this amplifier; the amplifier itself is upstream/shared and is left
intact (Sobisonator-caution), which is why the factor may need to be well below 0.25 (see §4.1 caveat).

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
