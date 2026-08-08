# Diagnosis — Currency Inflation/Deflation Wild Swings (boot-test #14)

**Status:** DIAGNOSED, no fix applied (awaiting decision). Investigated 2026-08-07.

## Symptom (player report, boot test)

Wild non-monotonic currency swings within ~1 year: ~10% deflation → printed 100k money →
6% inflation → stopped printing → 10% deflation again; then printing 50k → 9% inflation
immediately. The player asked whether this is user error (printing too much/fast).

**Answer: NOT user error, NOT the print amount, NOT a mod bug.** It is an *undamped
full-gap feedback loop* in the **upstream Sobisonator** quarterly currency system.

## The calculation & cadence

Core (`common/script_values/CURRENCY_svalues.txt`):
- `private_cash_ratio = (amt_circulated_scaled × 0.004) / private_cash_needed` [min 0.01] (~L753-765)
- `inflation%  = (ratio − 1) / 10`   when ratio > 1 (~L1143-1145)
- `deflation% = (1 − ratio) / 10`   when ratio < 1 (~L1120-1123)

Screenshot check (19 Feb 1763, CHI): private_cash 46.13M, ratio 124.64%, inflation +2.46%
→ (1.2464−1)/10 = 2.464% ✓. Implied `private_cash_needed` ≈ 37M.

Quarterly feedback correction (every 91 days, via `quarterly_trade_pulse` →
`quarterly_apply_trade_changes_and_consume`, `common/on_action/economy/oa_wealth_changes.txt:345`):
- **Inflation branch (ratio>1):** `cash_selloff_amt = (inflation × amt_circulated_scaled) / 5`
  → at 2.46% infl on 46.13M ≈ **227k withdrawn/quarter** (subtracted from circulation).
- **Deflation branch (ratio<1):** `money_demand_amt = deflation × 3000`
  → at 10% defl ≈ **300k injected/quarter** (added to circulation).

## Root cause: undamped full-gap correction

1. **Step size ≫ perturbation.** Player print = 50–100k/action; quarterly auto-correction =
   227k–300k. The feedback is **3–6× larger** than the player's lever per quarter.
2. **Full-gap, no partial adjustment.** Neither formula includes a fractional gap-closing
   term ("close 20% of the gap per quarter"); each tries to correct the FULL gap in one step.
3. **Moving target.** `private_cash_needed` (~L719-732) recomputes every quarter off trade
   wealth + population, so the target shifts 1–5%/quarter while the correction is in flight →
   overshoot into the opposite sign → sawtooth.
4. **No deadband.** Corrections fire whenever ratio ≠ 1.0; trade noise keeps nudging.
5. **Non-monotonic player experience** (50k→9% but 100k→6%): the 100k print landed in a
   quarter with a higher `private_cash_needed` denominator, the 50k in a lower one — so the
   ratio response felt random.

Cadence is QUARTERLY; the ~1-year sawtooth = 4 quarters of over-correction.

**[#23 magnitude correction, 2026-08-07]** Boot-test #23 ("snaps from modest inflation to severe
deflation") is the SAME mechanism as this doc — confirmed after a #23-specific diagnosis was written
and then REFUTED by adversarial review (see design/DIAGNOSIS_CURRENCY_ANNUAL_SNAP.md §0 for the full
refutation of the read-ordering theory). The one salvageable finding: the `private_cash_needed`
denominator swings **larger** than the "1–5%/quarter" estimated in point 3 above — the #28 boot trace
shows it moving across bands 0-10 ↔ 25-50 (a ~5× quarter-to-quarter step), which drives `ratio` all the
way to the 0.01 clamp and pins deflation at the −10% floor. WHY it's that large: besides the trade-wealth
terms, `private_cash_needed`'s cost-of-living input `CURRENCY_essentials_buying_power` divides by
`CURRENCY_wealth_value_1_unit_scaled_by_reserve_ratio` (CURRENCY_svalues.txt:690-694), which the reserve
buy/sell feedback moves every quarter — so cost-of-living AND the trade terms both swing with this loop,
compounding. This does not change the fix (still Option 1 below — damp the correction amounts); it means
the damping must be strong enough to tame a denominator that can step several-fold, not just a few %.

## Provenance (why we don't just edit it)

The oscillation mechanism is **100% upstream Sobisonator** (git authorship on the feedback
formulas + the quarterly apply). Mod's only currency touches: read-before-set guards, the
£→¥ glyph swap, and `#425` silver-reserve rewiring — NONE alter the feedback formula. Per
standing rules (`imp19c-sobisonator-upstream-caution`, never touch Sobisonator currency on a
hunch; `imp19c-proven-code-rule`), we do NOT edit the shared formula unilaterally.

CHI is not special: no CHI file writes `amt_circulated`/`private_cash_needed`. The swing is
generic to any monetary tag; CHI just has large reserves+circulation so the absolute numbers
are eye-catching.

## Options (NOT yet applied — pick one)

1. **CHI-only damping modifier (SAFEST, recommended).** A country modifier that scales the
   per-quarter correction to ~25% of the gap (converge over ~1 year, no overshoot). Leaves
   upstream untouched; only affects CHI. Preferred given the upstream-caution rule.
2. **Partial-adjustment multiply = 0.25** on `CURRENCY_inflation_cash_selloff_amt` /
   `CURRENCY_deflation_money_demand_amt` — fixes it globally but touches shared upstream code
   used by every monetary tag/regime (silver/gold/bimetallic/paper); would need testing
   across all of them. Consider proposing UPSTREAM to Sobisonator rather than forking.
3. **Deadband** (only correct if |ratio−1| > ~0.02) — kills trade-noise nudging, weaker vs
   large swings.
4. **Per-quarter cap** (e.g. ≤2% of circulation) — simple, but doesn't fix the full-gap targeting.

**Player short-term workaround:** the swings are driven by the auto-correction, not the print
amount, so "print less" won't stop the sawtooth — it only reduces player control. Accept it
as a business cycle, or apply option 1.

## Evidence files
- `common/script_values/CURRENCY_svalues.txt` — L719-732 (needed), L753-765 (ratio),
  L927-948 (balance apply), L1119-1146 (infl/defl %), L1177-1228 (feedback amounts)
- `common/scripted_effects/se_CURRENCY.txt` — L1178-1215 (reserve buy/sell), L1391-1400 (update circ)
- `common/on_action/economy/oa_wealth_changes.txt` — L111-121 (monthly minting), L138-359 (quarterly pulse)
- `common/scripted_guis/EE_scripted_guis.txt` — L449-535 (minting-rate buttons)
