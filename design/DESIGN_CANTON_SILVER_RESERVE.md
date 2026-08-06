# DESIGN — Canton trade feeds the silver reserve (粵海關白銀入庫)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI only.

## 1. Thesis — close the one gap the money model leaves open

The pre-Opium-War silver inflow (Western traders paying **specie** for tea/silk/porcelain through the
single Canton port) is the single most important fact of 18th-c. Qing monetary history, and it is the
one thing the current model does **not** put where it belongs. Today:

- `QING_canton_pulse` (`se_QING_CANTON.txt:70`) computes a real-goods customs yield and routes it to
  the **treasury** (`add_treasury`, :154) and the emperor's **privy purse** (`current_ruler add_gold`,
  :148). It never touches the currency-backing reserve.
- The tea/silk/porcelain **silver inflow** is modelled only abstractly, in the opium module
  (`se_QING_OPIUM.txt` → `QING_opium_assess_trade_balance`): net exports nudge the abstract
  `qing_currency_stress` meter (`QING_DECLINE_nudge`, `:208`). Stress relief, never reserve tonnage.
- The **only** writer of CHI's `silver_reserve_size` is `QING_revenue_reserve_drift`
  (`se_QING_REVENUE.txt:71`) — an administrative/era drift keyed to the 戶部 minister, deliberately
  **not** market-driven.

So the reserve that actually backs the currency (`silver_reserve_size` → `backing_value`,
`se_CURRENCY.txt:1964-1980`) moves on ministerial competence and era, but **not** on whether the Canton
trade is booming and drawing foreign silver in. This doc adds that missing feed: **a fraction of each
quarter's Canton yield accrues to `silver_reserve_size` as physical specie inflow.**

This is the **layer-don't-duplicate** archetype (same as the opium module layering on the stress meter):
we add **no** new reserve variable, **no** new pulse, **no** new backing machinery. We add one guarded
`change_variable` inside the existing `QING_canton_pulse`, clamped by the existing peak, composing with
the four existing writers under the existing ratchet rule.

## 2. Historical grounding (why a *fraction*, and why silver specifically)

- Western buyers (chiefly the EIC and country traders) had almost nothing the Qing wanted to import, so
  they settled the trade deficit in **silver bullion** — the classic specie drain *from* Europe *into*
  China, 1700s–~1820. The Canton customs (粵海關) sat astride exactly that flow.
- The customs **yield** the pulse already computes is an ad-valorem **levy** on the trade, not the trade
  itself. The silver that flowed in was the **payment for the goods**, far larger than the levy. So the
  reserve feed is modelled as a **multiple of the levy** (a proxy for gross trade volume), not the levy
  itself — the levy already goes to treasury/purse and must not be double-counted.
- The flow must **stop when the port closes** (閉關 = "the silver stops", the pulse's own words at :68)
  and **shrink under a low treaty tariff / venal Hoppo**, because those already scale the yield the feed
  is derived from — we get that coupling for free by deriving from `qing_canton_yield_tmp`.

## 3. Mechanic — one feed, derived from the yield already computed

Inject **after the emperor/state split completes** (after `se_QING_CANTON.txt:158`, where
`qing_canton_state_tmp` is added to treasury) and **before the scratch-var removal at :205**. The read
of `qing_canton_yield_tmp` is valid anywhere in `[132, 205)` and the split does not mutate it, but place
the leg post-split so the specie inflow reads as conceptually separate from the levy routing.

```
# --- [Canton silver inflow] the specie the Western traders paid IN for the tea/silk/porcelain
# they shipped OUT. The customs YIELD above is only the ad-valorem levy; the silver that actually
# entered the empire was the payment for the goods — modelled as a multiple of that levy (a proxy
# for gross trade volume) and credited to the engine's currency-backing reserve. Only runs while the
# port is OPEN (this whole block sits inside QING_canton_pulse's open-regime conditional), so a closed
# regime (閉關) yields NO inflow.
# NO upper cap: [2026-08-06] the hard peak clamp was removed from QING_revenue_reserve_drift — the
# historic 1777 peak is a MILESTONE EVENT (qing_revenue.5), not an in-game ceiling. Canton is a
# data-driven MARKET writer (like the governorship silver-send and deflation-buying), so real trade
# specie may legitimately carry the reserve ABOVE the historic peak. It is therefore NOT band-gated
# < peak (that gate is only for the passive administrative drift, which must not self-ratchet) and NOT
# re-clamped. The only guard is that the engine reserve var exists.
# NOTE: this deliberately moves silver_reserve_size ONLY — it does NOT write
# silver_reserve_actual_change (that var is a LIVE minting/currency-power input, not a display line —
# see §6/§4-FN1), mirroring QING_revenue_reserve_drift's deliberate abstention (se_QING_REVENUE.txt:129).
if = {
    limit = { has_variable = silver_reserve_size }
    set_variable = { name = qing_canton_silver_in_tmp  value = var:qing_canton_yield_tmp }
    change_variable = { name = qing_canton_silver_in_tmp  multiply = 10 }   # 萬兩 → 千兩 unit conversion (fixed; see §5)
    change_variable = { name = qing_canton_silver_in_tmp  multiply = 1.5 }  # trade-specie multiple (the tunable knob — see §5)
    change_variable = { name = silver_reserve_size            add = var:qing_canton_silver_in_tmp }
    set_variable    = { name = qing_canton_last_silver_in     value = var:qing_canton_silver_in_tmp }  # panel readout
    remove_variable = qing_canton_silver_in_tmp
}
else = {
    # reserve unseeded (should never happen for CHI — seeded in CURRENCY_setup_all_reserves): honest 0.
    set_variable = { name = qing_canton_last_silver_in  value = 0 }
}
```

Units — **read this before touching the factor:** `silver_reserve_size` is in **千兩** (per
`se_QING_REVENUE.txt:45-46`: "×10 vs the retired [萬兩] counter"). `qing_canton_yield_tmp` is in **萬兩**
(the pulse's scale). **These differ by 10×** (1 萬兩 = 10 千兩). The factor must convert 萬兩→千兩 (×10)
explicitly — see §5. (The unit note at `se_QING_CANTON.txt:30` used to be stale and imply the two shared a
scale; it was **corrected [2026-08-06]** to state the 10× gap and point here, so the source no longer
misleads — but keep the ×10 conversion explicit in the code regardless.)

### Why fold into the existing pulse rather than a new effect
- The open-port / port-level / Hoppo-squeeze / tariff-law gating and multipliers are all already applied
  to `qing_canton_yield_tmp` at that point. Deriving from it inherits every one of those couplings with
  zero duplication: close the port → yield 0 → inflow 0; low treaty tariff → thinner yield → thinner
  inflow; venal Hoppo → same.
- One new temp var (`qing_canton_silver_in_tmp`, removed same-frame) and one new panel var
  (`qing_canton_last_silver_in`). No new pulse, no new on_action wiring.

## 4. Composition with the four existing `silver_reserve_size` writers

Per the `#425` audit already in `se_QING_REVENUE.txt:72-88`, silver_reserve_size has these writers; the
new feed composes safely with all:

| Writer | Direction | Interaction with Canton feed |
|---|---|---|
| `QING_revenue_reserve_drift` (`se_QING_REVENUE.txt:71`) | ±, minister/era | Runs FIRST, same pulse — `QING_revenue_pulse` (`se_QING_GOVERNANCE.txt:537`) precedes `QING_canton_pulse` (:577). **Now genuinely additive** (was FN2): since the hard peak clamp was removed [2026-08-06], the revenue drift no longer eats all headroom to the ceiling, so Canton's contribution is no longer subordinated. Revenue's OWN accumulation still self-gates `< peak` (line 108), but that does not cap the reserve — Canton adds on top. |
| `CURRENCY_all_governorships_send_to_reserves` | + (and resets `actual_change=0`) | ~nil silver for CHI, **but** it resets `silver_reserve_actual_change=0` (`se_CURRENCY.txt:1151`) on a *separate quarterly on_action chain* (`oa_wealth_changes.txt:340`) — see FN1. |
| `CURRENCY_private_purchase_or_sell_reserves` (`se_CURRENCY.txt:1204`, monthly) | ± inflation/deflation | The Canton inflow **backs** the currency → lowers stress → less inflation drain. Correct historical loop, but note it compounds with the opium path — see §7. |
| `INCOME_sell_reserves` (deficit auto-fund) | − | Independent; Canton feed just refills faster in boom years. |

**FN1 — `silver_reserve_actual_change` is a LIVE minting input, not a display line (was CRITICAL in
review).** It is read by `CURRENCY_ideal_reserve_ratio_multiplier_silver` (`CURRENCY_svalues.txt:326-328`)
→ the minting-value multiplier, and by `CURRENCY_reserve_change_currency_value` (`:807`) →
`..._for_minting` (`:813`) → **mintable currency**. So writing it pumps the money supply that quarter.
`QING_revenue_reserve_drift` deliberately does NOT write it (`se_QING_REVENUE.txt:129-135`). This doc
**follows that precedent** — the §3 leg moves `silver_reserve_size` only. Consequence: the Economy
window's vanilla "silver accumulation rate" line will **not** attribute the Canton inflow (same as the
revenue drift); the Revenue-panel read-out (§6) from `qing_canton_last_silver_in` is the surfacing
instead. Do **not** re-add the `actual_change` write without explicitly modelling and calibrating the
minting side-effect.

**FN2 — RESOLVED by the [2026-08-06] cap removal.** The original concern was that the revenue drift (first
in the pulse) would clamp the reserve to the peak and Canton's `< peak` gate would then zero it out —
making Canton a subordinate below-ceiling feed. That is no longer true: the hard peak clamp was removed
from `QING_revenue_reserve_drift`, and the Canton feed itself is **not** band-gated `< peak` (§3). So
Canton is now a genuine independent adder that composes additively with the drift, and real trade specie
can carry the reserve above the historic peak. The peak survives only as the `qing_revenue.5` milestone
event and as the self-gate on the drift's *own* passive accumulation.

**Ratchet-rule compliance** (`imp19c-no-restoring-drift-ratchet-rule`): the rule targets *passive
restoring drifts* that would ratchet a value toward a target with no opposing force. The Canton feed is
**not** such a drift — it is a data-driven market inflow gated on real, losable conditions (port open,
export production, tariff/Hoppo state); when those fall, the inflow falls or stops (close the port → 0).
It is therefore correctly **uncapped** (like the governorship silver-send and deflation-buying market
writers). The revenue drift's *own* passive accumulation remains self-gated `< peak` per the rule; the
drain legs (revenue decline, silver-crisis bleed, deficit sell-off) remain ungated, so 銀荒 downward
dynamics are never neutered. The zero floor (`se_QING_REVENUE.txt:138`) still bounds the reserve below.

## 5. Calibration — `SILVER_INFLOW_FACTOR` (pinned to the sourced figures)

**The Canton contribution must MIRROR the real net silver inflow** (per the calibration mandate and
`research/1763_CANTON_SILVER_INFLOW.md`), not a made-up proxy. Unit bridge:
- 1 tael ≈ 37.3 g → **1 千兩 (1000 taels) ≈ 37.3 kg → 1 metric ton ≈ 26.8 千兩.**

Sourced real inflow targets (research §1):
- **Canton-specific:** ~3,000 tons landed 1800–1830 = **100 tons/yr** (Deng 2008) → 100 × 26.8 ÷ 4
  ≈ **~670 千兩/quarter**.
- **Broader China money-supply inflow:** ~190 tons/yr (Von Glahn 2013) → ≈ **~1,270 千兩/quarter**
  (an upper bound — not all of it entered through Canton or reached the state reserve).

So the reserve feed should land around **~500–700 千兩/quarter at the 1763 zenith** to mirror the
Canton-specific figure — notably LARGER than the revenue drift's ~250–350, which is correct: booming
Canton trade was the *dominant* specie source in the High-Qing surplus era, and (post cap-removal, §3/§4)
it is now allowed to be. The factor must include the **×10 萬兩→千兩 unit conversion** (§3), then a
trade-multiple knob tuned to hit that band:

```
change_variable = { name = qing_canton_silver_in_tmp  multiply = 10 }    # 萬兩 → 千兩 (unit conversion, fixed)
change_variable = { name = qing_canton_silver_in_tmp  multiply = 1.5 }   # trade-specie multiple (tuned to the sourced inflow)
```

Worked example (mirrors the Deng ~100 tons/yr Canton figure):
- Zenith yield ≈ 45 **萬兩**/quarter → **×10 = 450 千兩** → **×1.5 = 675 千兩/quarter** ≈ **~25 tons/quarter
  = ~100 tons/yr** ✓ (matches the Canton-specific inflow).
- A closed or treaty-tariff-pinned Canton (yield floored ~6–8 萬兩 after ×0.8) → ~90–120 千兩/quarter —
  the inflow collapses when the port shuts, exactly as history has it (the 1826-27 reversal / 閉關).
- ⚠️ Two traps: (a) never fold away the ×10 conversion (a bare `×15` reads as arbitrary and invites the
  10× under-credit bug); (b) `1.5` is the **tunable knob** — if the §7 combined stress-relief loop
  (Canton-backing + opium-inflow) over-stabilises a boom in playtest, dampen `1.5` here, not the ×10.
- Note the mod's yield cap (45 萬兩, `se_QING_CANTON.txt`) ceilings the feed at ~675 千兩/quarter; if a
  richer target is wanted, raise the yield cap rather than the factor (keeps the levy and the specie
  feed proportional).

## 6. Player-facing surfacing

- **Revenue panel (戶部):** add a "Canton Silver Inflow (粵海關銀入)" read-out from
  `qing_canton_last_silver_in`, beside the existing "Canton Contribution" (`qing_canton_last_state`).
  This is the **primary** surfacing (see FN1).
- **Economy window:** the vanilla silver-accumulation-rate line will **NOT** show the Canton inflow —
  the feed deliberately does not write `silver_reserve_actual_change` (a live minting input, FN1). This
  matches the revenue drift's behaviour and is intentional. The reserve *size* still moves, so the
  Economy panel's reserve total and the currency backing update correctly; only the per-tick "rate" line
  omits it. (Earlier draft wrongly claimed the opposite.)
- **Loc:** one key `qing_canton_silver_in_tt` explaining the specie-for-goods flow and that closing the
  port stops it.

## 7. Non-goals / explicitly out of scope

- **No** change to the metal *price* (`country_unit_price_silver`) — price stays a pure trade-engine
  output (`se_GLOBALTRADE_split.txt:2717`); this feed only moves reserve **quantity**, exactly like
  every other reserve writer. (This is the invariant that kept #37 a false positive; do not break it.)
- **No** *money* double-count: the customs *levy* still goes to treasury/purse; the *inflow* is the
  separate gross-trade specie proxy. They are different money and must stay separate.
- **Acknowledged production-base overlap (was a review MEDIUM):** the Canton yield derives from
  `GOODS_national_production_{tea,silk,porcelain}` (`se_QING_CANTON.txt:94-96`), and the opium module's
  `QING_opium_assess_trade_balance` reads the **same three aggregates** (`se_QING_OPIUM.txt:164-166`) to
  nudge `qing_currency_stress` **down** directly. So a tea/silk/porcelain boom now relieves currency
  stress via **two paths keyed to the same signal**: opium's direct export-inflow nudge, and Canton's
  reserve → `backing_value` (`se_CURRENCY.txt:1972`) → reserve-ratio → stress-drift (transitive). This is
  not *money* double-counting (one moves the stress meter, the other moves the reserve), and it is not
  ahistorical (both really did track the same specie flow), but it is a **compounding stress-relief loop**
  the builder must be aware of. **Calibration guard:** tune the §5 `1.5` multiple so the *combined* stress
  relief in a boom is not overpowered; if it is, dampen here rather than in the opium module (opium owns
  the stress meter). Do NOT add a *new* stress nudge from Canton — the transitive path is the only one.
- **No** new stress meter or band machinery; the currency-stress relief happens transitively via the
  reserve → `backing_value` → reserve-ratio → stress-drift path that already exists.

## 8. Build checklist

1. `se_QING_CANTON.txt`: add the specie-inflow leg + `else`-zero + clamp in `QING_canton_pulse`,
   injected **after :158 (post-split), before :205 (scratch removal)** (§3), with the two-step factor
   form (§5). Move `silver_reserve_size` ONLY — do **not** write `silver_reserve_actual_change` (FN1).
2. `se_QING_CANTON.txt` `QING_canton_init`: seed `qing_canton_last_silver_in = 0` (panel-safe first read;
   the `else`-zero in §3 keeps it honest thereafter).
3. Revenue/Canton panel GUI + one loc key (§6). Do NOT wire it to the vanilla Economy accumulation-rate
   line (it won't be attributed there — FN1).
4. `se_LOG` line in the pulse (`LOG_line sys=QING msg="canton silver inflow ... for"`) per the
   error-logging standing rule.
5. **Calibrate the §5 `1.5` multiple against the COMBINED stress relief** (Canton reserve-backing path +
   opium export-inflow path, §7) — verify a boom isn't over-stabilising; dampen the `1.5` if so.
6. Review gates: ratchet-rule (band-gate + clamp), **no `actual_change` write (FN1)**, revenue-drift
   ordering/subordination acknowledged (FN2), no price write, no *money* double-count, opium
   production-base overlap noted (§7), unit factor legibility, brace/quote/BOM integrity, boot-crash
   independent review.
