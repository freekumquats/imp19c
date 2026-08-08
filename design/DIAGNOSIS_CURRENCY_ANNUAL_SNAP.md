# Diagnosis — Currency snaps from modest inflation to severe deflation (boot-test #23)

**Status:** ⚠️ **INITIAL DIAGNOSIS REFUTED by adversarial review (2026-08-07).** The read-ordering /
stale-accumulator root cause below (§4, struck through) is **WRONG** — disproven against source on three
independent load-bearing points. The corrected conclusion is in §0. Kept as a record of the false trail
so it is not re-attempted. Boot log: `~/Downloads/logs.zip`, Aug 7 16:24 (`-debug_mode`, #28 currency
band-logging present).

---

## 0. CORRECTED CONCLUSION (what is actually true)

The symptom (currency snaps modest-inflation → −10% floor → back, cyclically) is **the same
undamped-feedback oscillation already diagnosed in [DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md] (#14)** —
NOT a new read-ordering bug. My #23 root cause was a mis-attribution. Three source facts (all
re-verified by me after the review) break the #23 chain:

1. **The quarterly reset does NOT zero the denominator's trade term.**
   `GT_reset_trade_transaction_totals` (`se_GLOBALTRADE_split.txt:3919-3951`) sets to 0 only six
   per-governorship vars: `trade_income_due_shipping` / `_expenses_due_shipping` /
   `_income_due_resource_extraction` / `_expenses_due_resource_extraction` /
   `_income_due_manufacturing` / `_expenses_due_manufacturing`. The denominator's subtracted term,
   `CURRENCY_trade_wealth_outgoing_currency_value`, reads `var:TRADE_national_expenditure` (a
   **country-scope stored var**) — which the reset **never touches**. It is *overwritten* (not zeroed)
   once per quarter at `oa_wealth_changes.txt:359`. **There is no zeroed window.** (Verified: grep of
   the reset body shows no `national_expenditure`; the only writer is oa_wealth_changes.txt:359.)

2. **No monthly consumer reads the denominator.** `monthly_currency_pulse`
   (`oa_wealth_changes.txt:111-133`) calls only `CURRENCY_mint_currency` (reads `CURRENCY_minting_rate`
   vs its cap — NOT `private_cash_needed`/`ratio`), `ECON_LOG_minting_snapshot`, `CURR_STRESS_pulse`.
   The deflation term (`CURRENCY_amt_circulated_deflation`) is consumed **only on quarterly paths**
   (`DEMAND_consumer_multiplier`, `se_CONSUME.txt`, via `quarterly_apply_trade_changes_and_consume`).
   So the "a per-month consumer samples the zeroed quarterly window" premise is false — there is no
   monthly read. (Verified: read of `monthly_currency_pulse` body.)

3. **The trace snapshots are themselves quarterly** and are taken when both trade terms are populated
   (`ECON_LOG_currency_snapshot` at `oa_wealth_changes.txt:209` and `:356`, after
   `WEALTH_generate_new_all_countries` and while `TRADE_national_expenditure` holds its value). So the
   §2 bands show genuine **quarter-to-quarter** denominator movement — not a sub-quarter sawtooth.

**Why the denominator genuinely swings quarter-to-quarter (the real mechanism = #14):**
`private_cash_needed` is recomputed each quarter from (a) `TRADE_national_expenditure` and
`WEALTH_total_new_generated_governorship` — outputs of the trade economy that #14 showed oscillates
under undamped full-gap correction — and (b) `CURRENCY_essentials_buying_power` (cost-of-living), which
divides by `CURRENCY_wealth_value_1_unit_scaled_by_reserve_ratio` (`CURRENCY_svalues.txt:690-694`),
a term the reserve buy/sell feedback moves every quarter. So the cost-of-living numerator of `needed`
*also* swings with the same #14 loop. The denominator steps quarter-to-quarter because **the whole
monetary system oscillates quarterly** — exactly #14. (Verified: `essentials_buying_power` divides by
the reserve-ratio-scaled unit.)

**The one salvageable #23 observation:** the denominator swing is **larger** than #14's original
"1–5%/quarter" estimate (the trace shows `needed` band 0-10 ↔ 25-50, a ~5× move). This is a **magnitude
correction to #14**, not a new mechanism — partly explained by the reserve-ratio scaling of
cost-of-living compounding with the trade-term swing.

## 0.1 CORRECTED FIX DIRECTION

Do **NOT** pursue the §5 Option A below (cache `private_cash_needed`) — the review showed it is
ineffective (nothing to suppress at monthly cadence; the swing is quarterly), phase-incorrect at the
proposed call site (would blend this-quarter wealth-generated with last-quarter outgoing), and NOT
economics-neutral (the ratio it caches also feeds the reserve buy/sell feedback, so caching perturbs
the #14 loop).

**Correct fix = #14's Option 1: damp the feedback AMOUNTS** (`CURRENCY_inflation_cash_selloff_amt` /
`CURRENCY_deflation_money_demand_amt`), scaling the per-quarter correction to a fraction of the gap so
it converges instead of overshooting. Prefer the CHI-only-modifier form (upstream-caution rule). Fold
the magnitude correction (denominator swings up to ~5×, not 1–5%) into #14 and pursue the fix THERE.
This #23 doc is closed; **#23 is a duplicate of #14**.

---

## 1. Symptom (sharpened player report, boot test)

Not "there is deflation." The complaint is the **discontinuity**: currency sits at *modest inflation*,
then **snaps to severe deflation (≈ −10%, the floor)** periodically, then recovers — a sawtooth. The
player's framing: *"a calculation being reset suddenly somewhere."* That intuition pointed at a reset;
the reset exists (quarterly trade reset) but does NOT feed the denominator (§0.1), so the intuition,
though reasonable, does not localise the cause. The cause is the quarterly feedback oscillation (#14).

## 2. The boot trace (what it actually shows — quarterly, not sub-quarterly)

#28 `ECON_LOG_currency_snapshot` bands, chronological from `debug.log`:

| time (wall) | ratio band | needed band | circ band |
|---|---|---|---|
| 16:02:45 | ≥ 1.0 (inflation) | 0-10 | 25-50 |
| 16:06:31 | < 0.1 (defl FLOOR) | 25-50 | 25-50 |
| 16:13:22 | ≥ 1.0 (inflation) | 0-10 | 25-50 |
| 16:14:52 | < 0.1 (defl FLOOR) | 25-50 | 25-50 |
| 16:18:04 | ≥ 1.0 (inflation) | 0-10 | 25-50 |

Correct reading: `circ` (the snapshot logs `CURRENCY_amt_circulated_scaled`, not raw circulation) is
stable; `ratio` moves inversely with `needed`. **This is the #14 signature** (denominator oscillating
quarter-to-quarter under the feedback loop), NOT evidence of an intra-quarter transient. My original
inference that the inverse correlation implied a read-ordering reset bug was the error.

## 3. The formula chain (`common/script_values/CURRENCY_svalues.txt`) — quoted correctly, conclusion wrong

```
deflation%           = (1 − ratio) / 10                    (L1111-1124)
ratio                = circ_scaled × 0.004 / private_cash_needed   [needed min 0.01]  (L753-765)
private_cash_needed  = [ essentials_buying_power × pop / 4000
                         − trade_wealth_outgoing   (reads var:TRADE_national_expenditure, L911-924)
                         + wealth_generated ] / 2000        (L719-732)
```
The formulas are quoted correctly. The error was the claim about what MOVES the terms (§4, struck).

## 4. ~~Root cause (stale-accumulator read-ordering)~~ — ❌ REFUTED, DO NOT USE

> ~~At quarter start, `quarterly_reset_trade_transaction_totals` zeroes the accumulators feeding
> `− trade_wealth_outgoing`; the subtraction vanishes → `needed` snaps up → ratio collapses to the
> clamp → deflation floor; a monthly consumer samples this zeroed window → step.~~

**Every clause of this is false in source** — see §0 breaks 1–3. The reset zeroes different vars than
the denominator reads; `TRADE_national_expenditure` is never zeroed; no monthly consumer reads the
denominator; the snapshots are quarterly. Retained only to mark the dead end.

## 5. ~~Proposed fix (Option A: cache private_cash_needed)~~ — ❌ REJECTED by review

See §0.1. Ineffective (nothing to suppress at monthly cadence), phase-incorrect at the proposed site,
and not economics-neutral (the cached ratio also drives the reserve feedback). Superseded by #14 Option 1.

## 6. Lessons (why the initial diagnosis was wrong)

1. **Asserted a causal link as VERIFIED without tracing the variable identity.** §4 stated the reset
   "zeroes the accumulators that feed `trade_wealth_outgoing`" as fact. I never confirmed the reset's
   target vars are the SAME vars the denominator reads — they are not (`trade_*_due_*` ≠
   `TRADE_national_expenditure`). A variable-name lineage check would have caught it immediately.
2. **Assumed cadence instead of reading the consumer.** I called deflation "a per-month consumer"
   without checking that `monthly_currency_pulse` reads it. It does not; deflation is quarterly-only.
3. **A stable-numerator + inverse-correlation trace is the #14 signature too** — it does not
   distinguish a read-ordering bug from feedback oscillation. I over-read the trace.
4. The adversarial review was decisive precisely because it was told to REFUTE, not confirm. This is
   the value of the review-before-build rule catching a bad diagnosis before any code shipped.

## 7. Evidence files (verified)
- `common/scripted_effects/se_GLOBALTRADE_split.txt:3919-3951` — reset zeroes only `trade_*_due_*`.
- `common/script_values/CURRENCY_svalues.txt` — L690-694 (essentials÷reserve-ratio-scaled unit),
  L719-732 (needed), L753-765 (ratio), L911-924 (outgoing reads `var:TRADE_national_expenditure`),
  L1111-1124 (deflation).
- `common/on_action/economy/oa_wealth_changes.txt` — L111-133 (monthly pulse: no denominator read),
  L209/L356 (quarterly snapshot sites), L340 (quarterly deflation consume), L359 (sole
  `TRADE_national_expenditure` write).
- `common/scripted_effects/se_CONSUME.txt`, `common/script_values/DEMAND_svalues.txt:210` — quarterly
  deflation application.
- `design/DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md` (#14) — the mechanism that actually explains the trace.
