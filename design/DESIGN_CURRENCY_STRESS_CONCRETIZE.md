# DESIGN — Tighten `qing_currency_stress` onto the concrete reserve/inflation model (銀荒)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI (the Qing-flavoured meter).
**Sibling to:** the yamen/exam/corruption concretization docs. Same [[imp19c-concrete-over-abstract-rule]].

## 0. Why this is a target — and why it's the LEAST-bad of the accumulators

`qing_currency_stress` (0–100, the 銀荒 silver-famine gauge) is different from the other TARGET meters:
it is **already partially tied** to the concrete upstream currency model — but in the crudest possible way,
throwing away almost all of the concrete signal. Verified drivers:

- The base drift is `CURR_STRESS_update` (`se_CURRENCY_STRESS.txt:54-74`), shared with the generic (non-CHI)
  currency layer. It reads ONE concrete value — `CURRENCY_reserve_ratio_impact` (a 0–1 reserve-backing
  health signal, `CURRENCY_svalues.txt:376`) — but collapses it to a **binary threshold**:
  ```
  if reserve_ratio_impact < 0.5  → stress += 2      # one bit of a rich 0..1 number
  else                           → stress −= 1
  ```
- On top of that, ~19 scattered event/effect nudges write the same var (opium drain, revenue events,
  rebellion, canton, self-strengthening resets, etc. — full census §2).

So it reads the reserve ratio as a single on/off bit and otherwise accumulates. **The concrete referent
(the whole upstream reserve/backing/inflation model — the one this session mapped) already exists and is
already wired in — this task upgrades the transfer function from a 1-bit threshold to a real derivation,
and demotes the hand-nudges to a residual.** Lower risk than the other targets because we're tightening an
existing coupling, not building one.

## 1. Thesis — two-store, same shape as the corruption doc

`qing_currency_stress = clamp( CONCRETE_base + event_residual , 0, 100 )`, recomputed each pulse:

1. **`QING_currency_stress_base`** — derived from the concrete monetary state. ⚠️ **NOT the naive
   `(1−impact)×100` (review CRITICAL 1).** CHI is `silver_standard` and has NO `public_debt_administration`
   (that's set only on GBR/FRA/SPA/RUS, `se_CURRENCY.txt:958-967`), so `CURRENCY_reserve_ratio_impact`
   takes the **`else` branch = `reserve_ratio_total / 3`** (`CURRENCY_svalues.txt:390-396`) — it only
   reaches 1 (→ base 0) when the silver reserve is worth ≥3× all circulating cash, a very high bar. The
   naive map sends `impact 0.5 → base 50` = strain band, firing silver_drain at the High-Qing zenith.
   **Must be CALIBRATED, and calibrated against MEASURED 1763 values (below):**
   - **Reserve backing** (core 銀荒 signal): a *piecewise/scaled* transfer where the OLD 1-bit pivot
     (`impact ≈ 0.5`) maps to the OLD boundary (~30, calm/strain edge), and only a genuinely-drained reserve
     (`impact < ~0.2`) reaches crisis. e.g. `base_reserve = clamp((0.7 − impact) / 0.7 × 100, 0, 100)` (so
     impact 0.7→0, 0.5→~29, 0.2→~71, 0→100) — tune the 0.7 knee to the measured start.
   - **+ inflation/deflation term:** `CURRENCY_amt_circulated_inflation` (`:1134`) and/or `private_cash_ratio`
     (`:753`) deviation from 1.0 — modest weight.
   - **MANDATORY PRE-BUILD:** read live `CURRENCY_reserve_ratio_total` / `_impact` for CHI at the 1763 AND
     1815 starts and RECORD them; pick the knee so 1763 opens calm and 1815 opens strained. Do NOT assert
     "1763 opens calm" until measured — with the ÷3 branch it may not.
   `impact` is cleanly clamped 0..1 (final `max=1 min=0`), so base can't overshoot [0,100] — no extra clamp/div0 needed on it.
2. **`qing_currency_stress_residual`** — a NEW **SIGNED** stored var the ~19 event nudges retarget (the
   rewrite). ⚠️ **It MUST allow NEGATIVE values and decay toward 0 from BOTH sides (review CRITICAL 2).**
   The existing `QING_DECLINE_nudge`/`QING_opium_nudge` FLOOR at 0 (`se_QING_DECLINE.txt:8`), so a plain
   retarget would make every NEGATIVE nudge inert at residual 0 — and the High-Qing calm TODAY comes
   largely from the opium *surplus* (a big negative nudge) holding the meter at its 0 floor. Discarding
   that suppression would spike the opening. So: author a **dedicated signed nudge helper** (no 0-floor)
   for the residual; the level clamp `[0,100]` happens only on `base + residual`, not on the residual
   itself. The opium drain (§3) is the most important resident and is frequently negative (surplus years).
3. **The level** = `clamp(base + residual)`. The bands (`CURR_STRESS_classify` 30/60 → silver_drain /
   monetary_crisis modifiers) and every reader are UNCHANGED — they still read `qing_currency_stress`.

This is the corruption doc's two-store model, and it fits here for the same reason: too many writers (~19)
to leave on the live var while also anchoring it, so redirect them to a residual and derive the base.

## 2. Writer census (verified — ~19 sites, all files)
| File:line | Amount | Nature |
|---|---|---|
| `se_CURRENCY_STRESS.txt:54` (`CURR_STRESS_update`) | ±2/−1 on reserve-ratio bit | **the base drift → REPLACE with the §1 derivation** |
| `se_QING_OPIUM.txt:208` | `var:qing_opium_stressnudge_tmp` | opium trade-balance (§3) → residual |
| `se_QING_OPIUM.txt:327,339`, `qing_opium_events.txt:210` | +4/−6/−5 | opium beats → residual |
| `se_QING_REVENUE.txt:158,277`; `qing_revenue_events.txt:216,237,251,265` | ±1..−10 | fiscal events → residual |
| `qing_rebellion_events.txt:444` | +12 | rebellion shock → residual |
| `qing_canton_events.txt:81` | +4 | canton shock → residual |
| `qing_frontier_sea_events.txt:139` | +8 | coastal crisis → residual |
| `se_QING_MECHANICS.txt:532,556` | −25/−5 | reform/reset → residual (or leave as a residual reset) |
| `se_QING_SELFSTR.txt:765` | `set 0` | self-str full reset → reset BOTH base-cache and residual |
| `qing_roster_events.txt:159,531` | −6/−4 | minister quality → residual |
| `se_QING_DECLINE.txt:96` | seed 0 | seed → keep (or seed base) |

Note: some are `QING_opium_nudge` / `QING_DECLINE_nudge` wrappers — all ultimately `change_variable` the
same var, so all retarget to the residual uniformly.

## 3. The opium drain is ALREADY concrete — do NOT fold it into the reserve base
Verified: `qing_opium_stressnudge_tmp` (`se_QING_OPIUM.txt:160-208`) is itself **derived from real trade
goods** — `inflow = (GOODS_national_production_tea + silk + porcelain)/4` (capped 40) minus
`outflow = (DEMAND_country_opium − GOODS_national_production_opium)/8 + addicted_share/3` (capped 50). Net
inflow−outflow nudges stress DOWN (silver flowing in) or UP (opium draining it out). This is a genuinely
concrete balance-of-trade signal (#366) and must be PRESERVED as-is — it just lands in the **residual**,
not the reserve base (the reserve base captures the *stock* backing; opium captures the *flow*). The two
are complementary, not double-counting: stock (reserve ratio) + flow (opium trade balance) = the full 銀荒
picture. Keep the opium computation; only change where its output is added.

## 4. Interaction / what stays
- **Bands + modifiers** (`qing_curr_silver_drain` / `qing_curr_monetary_crisis`, thresholds 30/60): UNCHANGED
  — they read the level. But note the same reframe caveat as the other docs: the level is now dominantly
  reserve-derived, so "silver_drain" fires on a genuinely low reserve ratio rather than accumulated nudges.
  This is MORE historically correct (that's literally what 銀荒 was), so it's an improvement, not a
  regression — but disclose it.
- **`qing_reform_pressure`** sums `qing_currency_stress` (`se_QING_DECLINE.txt:351`) — the sum machinery is
  untouched, BUT its OPENING VALUE is only unchanged if the base opens near 0 (review #6, contingent on the
  CRITICAL-1 calibration). Today ≈ (12+0+20+10)/4 ≈ 10.5; if the base opens at ~50 it climbs to ~23+ and
  could arm the currency→ethnic crosswire (`:1037`, `stress≥70`) and treaty/roster gates (`stress≥40`)
  early. Re-validate reform_pressure's 1763 opening after calibrating the base.
- **Generic non-CHI layer** (`CURR_STRESS_pulse`, excludes CHI): the shared `CURR_STRESS_update` is used by
  both. If we replace it for CHI, either (a) branch inside `CURR_STRESS_update` (CHI → derivation, else →
  1-bit drift), or (b) give CHI its own `QING_currency_stress_recompute` and leave the generic helper alone.
  **(b) is cleaner** — keeps the generic layer byte-identical, no cross-contamination.

## 5. Feasibility / gotchas
- **Perf:** `CURRENCY_reserve_ratio_impact` / `_inflation` are country svalues (no province sweep) — cheap;
  fine to read live each pulse. No per-character hot path here (unlike the exam/censorate case). No cache needed.
- **The reserve base IS a function of the reserve size the Canton/Revenue feeds move** (review #3 —
  correcting §5's earlier "distinct, no double-count" phrasing, which was WRONG): `silver_reserve_size` →
  `backing_value` → `reserve_ratio_total` → `impact` → base. This is the **intended single channel** (Canton
  silver → stronger backing → lower stress), NOT a double-count. BUT a real **feedback-loop risk**: the
  Revenue 銀荒 drain (`se_QING_REVENUE.txt:125-127`) subtracts `silver_reserve_size` gated on
  `var:qing_currency_stress >= 40` (the LEVEL). With the level now reserve-derived, if the base opens high
  (CRITICAL 1) the drain fires turn 1 → lowers reserve → raises base → keeps draining. Today's seed-0 meter
  reaches 40 slowly, damping this. **Fix: after calibrating, re-check this drain — gate it on the RESIDUAL
  (event-driven crisis), not the reserve-derived level, or raise its threshold.**
- **Save migration:** MUST run after currency setup (`has_variable = official_currency`); if the base can't
  yet be read (e.g. at `on_game_initialized` before currency init, where impact=0→base=100), SKIP the seed
  and leave residual 0. Otherwise seed `residual = old level − fresh base` (signed — CRITICAL 2), decay both ways.
- **RHS-comparison rule:** any drift-toward compare needs the `_cmpsvalue` wrapper idiom.
- **Div/0:** `reserve_ratio_impact` is already clamped 0..1 upstream; no floor needed on the base.

## 6. Build checklist
0. **PRE-BUILD MEASUREMENT (blocking):** read live `CURRENCY_reserve_ratio_total`/`_impact` for CHI at the
   1763 and 1815 starts; record. Pick the transfer-function knee (§1.1) so 1763 opens calm / 1815 strained.
1. `QING_currency_stress_recompute` (CHI-only): `base` = the CALIBRATED reserve transfer (§1.1, NOT
   `(1−impact)×100`) + weighted inflation term; `level = clamp(base + qing_currency_stress_residual, 0, 100)`.
   Leave the generic `CURR_STRESS_update` untouched (§4b).
2. Add `qing_currency_stress_residual` (**SIGNED**, decays toward 0 from both sides) + a dedicated signed
   nudge helper (NO 0-floor — CRITICAL 2).
3. Retarget the 17 nudge-writers + 1 self-str reset (§2) to the residual via the signed helper (opium
   computation §3 preserved, only its add-target changes; NEGATIVE nudges must stay negative).
4. Wire the recompute into `QING_DECLINE_pulse` REPLACING the `QING_DECLINE_update_currency_stress` call
   (`se_QING_DECLINE.txt:963`); DELETE the now-orphaned `QING_DECLINE_update_currency_stress` wrapper
   (`:138-140`) so it can't be re-called.
5. Re-check the Revenue reserve-drain (`se_QING_REVENUE.txt:125-127`) for runaway (§4) — regate on residual
   or raise threshold. Re-validate reform_pressure opening (§4).
6. Verify bands/readers unchanged; MEASURED 1763 opening calm (not assumed).
7. **[review M1] Reconcile the SECOND reserve→stress channel** `se_QING_REVENUE.txt:146-158`
   (`silver_reserve_size < 10000 → currency_stress += 1`): once the base is reserve-derived, a near-empty
   reserve ALREADY raises the base via low impact, so this +1 backfeed is a partial DOUBLE-COUNT of the same
   low-reserve signal. Either retarget it to the residual AND accept redundancy, or DROP it. (This is the
   `:158` writer the §2 census mislabels as a "fiscal ±1..−10" event — L1.)
8. **[review M2] The inflation term must be DEFLATION-side, not `CURRENCY_amt_circulated_inflation`.** That
   svalue (`CURRENCY_svalues.txt:1134`) returns 0 unless `private_cash_ratio > 1` (monetary GLUT) — it fires
   nothing during 銀荒, which is a DEFLATIONARY silver-scarcity (`private_cash_ratio < 1`). Use the deflation
   side (`CURRENCY_amt_circulated_deflation:1119` / ratio-below-1 deviation), NOT the inflation svalue — else
   the term raises stress during inflation and contributes nothing during the actual silver famine.
9. **[review M3] Re-validate the LINEAR (non-threshold) consumer** `se_QING_MINISTRY.txt:848-854` — the Board
   of Revenue performance term subtracts `currency_stress / 6` LINEARLY from the minister's Grand Council
   standing. Unlike the threshold gates, this shifts proportionally with the opening value: if the calibrated
   base opens ~30-50 instead of ~0, the Board minister opens 5-8 pts weaker at game start. Add to the
   1763-opening re-validation (§4), plus the extra level-gates L2 flags: `se_QING_REVENUE.txt:275 (≥20)`,
   `:334 (≥30)`, `qing_revenue_events.txt:197 (≥30)`.
7. Review gates: two-store (base+SIGNED residual) not max(); reserve→base is the single channel (not a
   double-count) but drain-feedback checked; opium negative nudges preserved; generic layer untouched;
   migration guarded on currency-setup; brace/quote/BOM; boot-crash review.
