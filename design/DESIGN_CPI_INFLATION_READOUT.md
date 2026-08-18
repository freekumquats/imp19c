# DESIGN (draft, pre-review) — display-only correct-inflation readout (CPI)

**Status:** DRAFT, pre-adversarial-review.
**Author:** freekumquats, 2026-08-17.
**Scope class:** touches EXISTING shared upstream currency code (display side only) — so
diagnosis-first + adversarial review per the overnight design-first rule and
`imp19c-sobisonator-upstream-caution`.

---

## 1. Problem

The top-bar "Inflation %" does not mean what a player expects. It is **not** a price index.
It is a **money-overhang ratio**: how much private cash is circulating relative to how much
cash the current cost of living needs.

Confirmed formula (`common/script_values/CURRENCY_svalues.txt`):

```
CURRENCY_private_cash_ratio        (L885) = amt_circulated_scaled × 0.004 / private_cash_needed
CURRENCY_amt_circulated_inflation  (L1312) = (private_cash_ratio − 1) / 10   [only when ratio > 1]
```

`private_cash_needed` (L851) is proportional to `essentials_buying_power` (the summed unit
prices of 10 essential goods, L835-849) × population. So essential-goods prices sit in the
**denominator**. Consequence, measured this session from a live boot: the number moves
**opposite** to real prices. Cheap essentials → small denominator → high ratio → high
"inflation" reading. The live boot showed a stable ratio ~2.5 → ~15% "inflation" with FLAT
money supply and LOW cost of living — i.e. the number was high **because** essentials were
cheap, not because prices rose.

This is a defensible upstream modelling simplification (a quantity-theory money-pressure
gauge), NOT a bug. But the LABEL is misleading. This design adds a **real** inflation
readout — a price-index (CPI) — **for display only**, without changing any behaviour.

## 2. Current state — what reads the inflation value (the map that governs risk)

**BEHAVIOURAL consumers (MUST NOT CHANGE — these are the economy):**
- `CURRENCY_amt_circulated_inflation_demand_multiplier` (= 1 + inflation), read by:
  - `DEMAND_food_svalues.txt:38`, `DEMAND_svalues.txt:211`, `DEMAND_luxury_svalues.txt`
    (many lines) — the main gameplay effect: extra consumer-goods demand.
- `CURRENCY_amt_circulated_inflation_wealth_multiplier`, read by
  `se_CURRENCY.txt:2159-2192` — pop-wealth malus.
- The overhang ratio also self-regulates the money supply (pops create/recall private cash;
  see the comment at `CURRENCY_private_cash_ratio`, L887-889).

**DISPLAY consumers (LEFT UNTOUCHED — the design is now ADDITIVE, see §3.3; listed only to
prove the new CPI readout does not collide with them):**
- Loc `inflation_info` (`localization/english/economic_enchancement_l_english.yml:1129`)
  renders `CURRENCY_amt_circulated_inflation |%` and labels it "consumer goods demand".
- `deflation_info` (L1131) is the mirror for the deflation branch.
- `inflation_deflation_text` / `inflation_deflation_tooltip`
  (`common/customizable_localization/000_ECON_loc.txt:2893 / 2909`) pick the inflation vs
  deflation loc key on `CURRENCY_amt_circulated_inflation > 0` (L2904 / L2920).
- `gui/economy_view.gui` (L1081/1085/1105/1109) calls those two custom-loc functions.

**Quarterly pulse (where new per-quarter state is stored):** `se_CURRENCY.txt` is the main
per-quarter currency update; the CURX probe already stores per-quarter vars here via
`se_ECON_LOG.txt`.

## 3. Proposed design — a display-only CPI, additive and reversible

### 3.1 The basket (nominal price level)
Define a NEW script value `CPI_basket_price` = the **sum of the raw nominal unit prices** of
the same 10 essential goods that `essentials_buying_power` uses:

```
grain, livestock, fish, vegetables, temperate_fruit,
processed_foods, clothing, furniture, pharmaceuticals, alcohol
```

DECISION — use the RAW `country_unit_price_<good>` vars (set in
`se_GLOBALTRADE_split.txt:3006-3016` from `global_base_import_price/(0.5+market_penetration)`;
CONFIRMED nominal by the review — the wealth-value division is a separate step applied only
inside `essentials_buying_power`, not baked into the base var). Do **NOT** divide by
`CURRENCY_wealth_value_1_unit`. Rationale: a CPI must measure the **nominal price level**;
the wealth-value division (a moving silver numeraire) would turn the CPI into a real-relative
series, wrong for a price index.
- Alternative rejected: reuse `essentials_buying_power` directly. Rejected because its
  wealth-value division makes it a real, not nominal, series — wrong for a CPI.

**Fallback source — CORRECTED per review (F2/F3):** the "hold last non-zero price" fallback
lives inside `CURRENCY_essentials_buying_power` at `CURRENCY_svalues.txt:689-820` (the real,
fallback-protected svalue consumed by `CURRENCY_private_cash_needed`). Do NOT copy from
`CURRENCY_essentials_buying_power_unweighted` (`:835-849`) — that sibling has NO fallback, and
using it would resurrect the task #69 bug (a simultaneous global-stockpile-zero craters the raw
price to ~0 and reads as "the good became free", per the comment at `:677-687`). The held-price
DATA (`$tradegood$_ess_last_nonzero_price`) is set generically for all goods in
`GT_split_get_country_import_unit_price_tradegood` (`se_GLOBALTRADE_split.txt:3003-3034`), so it
is reusable — BUT the per-good "if stockpile>0 use live else use held" SELECTION logic is inlined
per good with no shared call. So `CPI_basket_price` must DUPLICATE that ~10-branch if/else_if
chain. MAINTENANCE FLAG: two copies of the fallback chain now exist; if the essential-goods list
changes, both must change together. A shared helper is out of scope here but noted.

### 3.2 The rate (period-over-period change, smoothed, annualised)
**Wiring point — CORRECTED per review (F1, CRITICAL):** `se_CURRENCY.txt` is a pure effect
LIBRARY with no cadence of its own — defining the CPI-update effect there without CALLING it
ships dead code. The quarterly per-country cadence lives in
`common/on_action/economy/oa_wealth_changes.txt`. Wire the new `CPI_update` effect call into
`quarterly_apply_trade_changes_and_consume`, immediately after
`CURRENCY_update_amt_circulated = yes` (`oa_wealth_changes.txt:375`), inside the same
`if = { limit = { has_variable = official_currency } ... }` block (that site is documented to
run once PER COUNTRY per quarter, `:355-356`). Do NOT also wire it into the
`quarterly_trade_pulse` site (`:190`) — that runs once GLOBALLY per quarter and a double call
would break the `alpha=0.25` / `×4` math. One call site only.

Each quarter, in that per-country effect:
1. Read `CPI_basket_price` now.
2. Compare to the stored `CPI_basket_last` (a country variable set last quarter).
3. Quarter-over-quarter change = `(now − last) / last`.
4. Smooth it: exponential moving average, `CPI_smoothed = CPI_smoothed_prev + alpha × (QoQ − CPI_smoothed_prev)`,
   DECISION `alpha = 0.25` (≈ a 4-quarter memory). Rationale: raw prices swing across whole
   order-of-magnitude bands quarter to quarter (seen in the TZP probe); an unsmoothed CPI
   would sawtooth worse than today's number.
   - Alternative rejected: 4-quarter simple moving average. Equivalent memory but needs 4
     stored vars; EMA needs 1. EMA chosen for lower state.
5. Annualise for display: `CPI_annual = CPI_smoothed × 4`. Rationale: players read inflation
   as an annual rate; the current metric has no time dimension at all.
   - Alternative rejected: raw QoQ. Rejected as unintuitive on a top bar.
6. Store `CPI_basket_last = CPI_basket_price` for next quarter.

Guards:
- First quarter (no `CPI_basket_last`): CPI = 0 (bootstrap; nothing to compare to). Use the
  proven `has_variable`-else-initialize idiom (`se_DEMAND.txt:17-31`).
- `CPI_basket_last <= 0` (denominator): skip the division, hold the previous `CPI_smoothed`.
- **`CPI_basket_price <= 0` (numerator) — ADDED per review (F4):** ALSO skip the update and
  hold the previous `CPI_smoothed`. Without this, a quarter where all 10 essentials transiently
  read a first-ever zero gives `now=0, last>0` → `QoQ = -1` (a real −100% shock, no crash) that
  the EMA takes 4+ quarters to wash out, corrupting `CPI_annual` for over a year off an
  artifact (the day-0 zero edge is documented at `CURRENCY_svalues.txt:686-687`). Guard both
  ends symmetrically.
- Negative change → deflation, rendered as a negative `CPI_annual`.
  **Negative-render risk — per review (F5):** every in-repo `|%` usage formats a non-negative
  value, and the mod's OWN deflation display (`economic_enchancement_l_english.yml:1131/1135`)
  deliberately prepends a literal `-` and feeds a POSITIVE magnitude through `|%` rather than
  trust `|%` with a signed input. So a signed `|%` is UNPROVEN here. RESOLUTION: the Phase-0
  probe (§4) MUST force a negative `CPI_annual` and confirm `|%` renders it correctly BEFORE
  Phase 1 ships. If `|%` mis-renders a negative, fall back to the codebase's proven pattern —
  a twin loc key that prepends `-` and feeds `abs(CPI_annual)` — chosen on the boot evidence.

### 3.3 The display — a NEW, ADDITIVE readout (upstream inflation UNTOUCHED)
**LOCKED USER DIRECTIVE (2026-08-18):** do NOT modify the upstream inflation localization.
Leave loc `inflation_info` / `deflation_info`, the custom-loc functions
`inflation_deflation_text` / `_tooltip`, and the value `CURRENCY_amt_circulated_inflation`
EXACTLY as they are. The real price index is added as a SEPARATE readout, named to
distinguish it, so the player sees both: the upstream "Inflation" (money-overhang) figure AND
the new "Consumer Price Index".

- **New loc key `cpi_info`** in `localization/english/imp19c_interface_l_english.yml` (per
  review F7 — the mod's own topbar/interface loc file, where keys like
  `SHIPPING_CONTROLLED_TT_topbar` already live; NOT `economic_enchancement_l_english.yml`, which
  stays untouched). Renders as `Consumer Price Index: [value]%` — `[value]` = `CPI_annual`
  (§3.2), via `|%`. LOCKED: a percentage rate, NOT an index level.
- **Explanation ON HOVER ONLY** via a NEW `cpi_tooltip` key (same file). It explains the
  calculation: built from the current prices of a basket of the essential goods (grain,
  livestock, fish, vegetables, temperate_fruit, processed_foods, clothing, furniture,
  pharmaceuticals, alcohol), period-over-period change, smoothed and annualised, and that it is
  a genuine price-change rate — distinct from the money-overhang "Inflation" figure shown
  separately. **Bare-key tooltip, NO `Custom()` function (review F8):** the CPI tooltip is a
  single fixed explanation with no conditional branch, so `tooltip = "cpi_tooltip"` (the plain
  bare-key idiom, as `AUTO_FUND_DEFICIT_TT` at `economy_view.gui:1129`) suffices — no new
  `customizable_localization` function is needed. (Doc §6 Q2/Q5 are thereby moot.)
- **`gui/economy_view.gui` — additive, with the tab-growth risk resolved (review F6):** the
  currency section's enclosing vbox is a NON-scrolling flowcontainer (documented at
  `economy_view.gui:255` / the comment at `:1465-1469`), and stacking a new section pushes the
  Deficit/Expenses sections below it down in an already vertically-tight tab. RESOLUTION: add
  the CPI as a sibling textbox INSIDE the existing currency flowcontainer (`:1027-1088`),
  immediately after the inflation textbox — a minimal in-section addition, not a new stacked
  section — and the Phase-1 boot MUST screenshot-verify nothing clips at the tab bottom. The
  existing inflation widget and its two custom-loc calls are NOT altered.

**Display quantity — LOCKED (2026-08-18):** the headline value is a PERCENTAGE — the smoothed,
annualised price-change rate (`CPI_annual`, §3.2), rendered with the `|%` formatter. It is NOT
an index level. So the readout reads e.g. `Consumer Price Index: +4%`. A negative value renders
as deflation naturally (§3.2 guard). The `CPI_basket_price` level is an internal intermediate
only; it is not shown.

### 3.4 What is explicitly NOT touched (the safety contract)
- `CURRENCY_amt_circulated_inflation`, `_demand_multiplier`, `_wealth_multiplier`,
  `private_cash_ratio`, `private_cash_needed` — all UNCHANGED.
- Every behavioural consumer in §2 keeps reading the untouched overhang value. Pop demand,
  pop-wealth malus, and money-supply self-regulation behave EXACTLY as today.
- The upstream inflation display (loc `inflation_info`/`deflation_info`, the custom-loc
  functions, and the value they show) is ALSO unchanged — the CPI is a NEW, separate readout
  (§3.3), not a swap.
- Therefore the change **cannot** alter the economy's dynamics. It is a new read-only svalue
  family + a new loc key + a new GUI widget. Fully reversible by deleting the added widget.

## 4. Phasing (probe-first, per Sobisonator-caution)

**Phase 0 — PROBE (ships first, verified on a boot BEFORE any display change).**
Add `-debug_mode`-gated logging in the SAME per-country effect that hosts the CPI update
(called from `quarterly_apply_trade_changes_and_consume`, `oa_wealth_changes.txt:375` — see
§3.2 F1), STATIC label strings with no bare `#` (the real hazard per the corrected
`imp19c-log-string-macro-rule`; `$param$` is cosmetic-only and the design's labels avoid it
anyway). Emit, per quarter, side by side: `CPI_basket_price`, `CPI_basket_last`, raw QoQ,
`CPI_smoothed`, `CPI_annual`, and the existing `CURRENCY_amt_circulated_inflation`. Also force
a NEGATIVE `CPI_annual` at least once (per F5) to confirm `|%` renders deflation correctly
before Phase 1. This lets us SEE whether the CPI is stable and sensible across a real boot
before it reaches the UI. This is the mandated instrumentation step; it is not optional.

**Phase 1 — ADD THE READOUT (only after the probe boot confirms a stable CPI).**
Ship the CPI svalue family, the NEW `cpi_info` / `cpi_tooltip` loc keys, and the NEW additive
GUI widget per §3.3. The upstream inflation display is left as-is. Leave the probe in until a
second boot confirms the on-screen CPI matches the logged value, then strip the probe with the
standard verify-then-strip task.

## 4b. IMPLEMENTED (2026-08-18) — awaiting code review + boot

Shipped both phases together (the user boot-tests on a separate machine, so Phase 0's
"boot before Phase 1" is a verification gate, not a build gate — per the guess-and-log
convention). Files:
- `common/script_values/CURRENCY_svalues.txt` — `CPI_basket_price` (10-essential nominal
  basket, fallback chain duplicated from `CURRENCY_essentials_buying_power`, NO wealth-value
  divide, NO cap) + `CPI_ema_alpha = { value = 0.25 }`.
- `common/scripted_effects/se_CURRENCY.txt` — `CPI_update` effect (bootstrap / HOLD-both-ends /
  QoQ+EMA+annualise branches; stores `CPI_annual` signed + `CPI_annual_abs`) with the Phase-0
  CHI-only, `-debug_mode`-gated band-bucketed probe folded in (no bare `#`).
- `common/on_action/economy/oa_wealth_changes.txt` — `CPI_update = yes` once, per-country,
  right after `CURRENCY_update_amt_circulated` inside the `official_currency` block.
- `common/customizable_localization/000_ECON_loc.txt` — `cpi_value_text` sign-split custom-loc.
- `localization/english/imp19c_interface_l_english.yml` — `cpi_info` / `cpi_info_deflation` /
  `cpi_tooltip`.
- `gui/economy_view.gui` — additive CPI textbox inside the currency flowcontainer, after the
  inflation textbox.
Sign handling uses the PROVEN upstream deflation pattern (positive magnitude + literal `-`,
via the sign-split custom-loc), so signed-`|%` is never relied on (resolves F5 without a boot).
All 5 script files brace-balanced. Boot must screenshot-verify no bottom clip (F6) and confirm
the on-screen CPI matches the logged band; then strip the probe (verify-then-strip).

## 5. Risk assessment

- **Behavioural risk: NONE by construction** — no behavioural consumer is re-pointed (§3.4).
- **Display risk: LOW** — worst case the shown number is noisy or wrong; it changes no game
  state and reverts by undoing the loc edit.
- **Smoothing/annualisation are guesses** (`alpha = 0.25`, ×4). They are display-only and
  the Phase-0 probe logs them for tuning. Listed here so they are not buried.
- **Numeraire choice** (nominal raw prices vs wealth-normalised) is the one substantive
  modelling call; §3.1 argues nominal. The probe will show whether the raw basket is
  well-behaved.

## 6. Open questions for the adversarial reviewer
1. Are the 10 `country_unit_price_<good>` vars actually NOMINAL (silver) prices, or are they
   already normalised somewhere upstream? If already normalised, §3.1's "raw = nominal"
   premise is wrong and the CPI would be a relative-price index.
2. Does the "hold last non-zero price" fallback exist as a reusable value, or is it inlined
   inside `essentials_buying_power` such that the CPI basket must re-implement it?
3. Is `se_CURRENCY.txt` guaranteed to run once per quarter per country for CHI, and does the
   store-last-value ordering avoid reading `CPI_basket_last` after it is overwritten?
4. (RESOLVED — F9.) This question is void. The design is now ADDITIVE-ONLY (§3.3): the
   upstream `inflation_info` loc key is NOT re-pointed and NOT touched. The CPI ships as a
   NEW sibling readout with NEW loc keys (`cpi_info`/`cpi_tooltip`). No existing reader of
   `inflation_info` is affected. Kept here so the resolved question is visible, not buried.
5. Is a negative `CPI_annual` rendered correctly by the `|%` formatter, or does the deflation
   branch need its own key? (F5 — the Phase-0 probe forces a negative `CPI_annual` and
   confirms `|%` renders the sign; fallback = a twin loc key prepending `-` with abs value.)
