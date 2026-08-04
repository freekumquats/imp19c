# Metal (Gold/Silver) Reserve-Sale Pricing — Analysis

**Status:** ANALYSIS (no code change proposed for adoption yet). **Reclassified 2026-08-04.**

**⚠ This doc's original thesis was WRONG and has been retracted.** The first draft classified the
gold/silver reserve-price errors as a *missing feature* (metal pricing "never built"). An adversarial
code review refuted that with direct evidence (below). The actual cause is an **intra-quarter ordering /
cold-start defect** in the existing, working metal-pricing path. Keeping the retraction visible so the
wrong framing is not repeated. Per [[imp19c-bug-vs-missing-feature-rule]], note this is a **bug in
Sobisonator-authored economy code**, which is the higher-risk category to claim — so nothing here is
"proven" or fit to raise upstream; it is an internal analysis pending in-game verification.

---

## 1. What is actually true (verified from code)

Gold and silver ARE fully-modelled traded goods, priced by the same generic machinery as every good:
- **Iterated:** `gold`/`silver` are members of `every_tradegood_6_complex` (`zz_tradegood_6_injector.txt`).
- **Produced into stockpiles:** `se_GOODS.txt:451-476` — `gold_stockpile = GOODS_governorship_gold_produced`
  (guarded on `produces_gold`), same for silver; ~66 gold / ~19 silver producing provinces in setup.
- **Demanded:** `DEMAND_svalues.txt:1136` (`DEMAND_gold` = luxury + cottage luxury_clothing/furniture +
  factory + reserve accumulation), `:1249` (`DEMAND_silver`).
- **Priced:** `GT_split_get_global_import_unit_price_tradegood` (se_GLOBALTRADE_split.txt) writes
  `global_base_import_price_$tradegood$` UNCONDITIONALLY at line 2659, then sqrt-refines when `>0` at 2704.

So `global_base_import_price_gold/silver` IS produced — there is no missing price feature. Reserves are
seeded (`CURRENCY_base_starting_reserve_gold/silver`), accumulate/decay, back the currency (via the
`units_to_the_lb` cash-scaled path, which works), and are sold to cover deficits.

## 2. The actual defect — intra-quarter ordering (the errors' real cause)

In `oa_wealth_changes.txt` the quarterly pulse sequences the trade passes with day-delays:

```
day 0   quarterly_reset_trade_transaction_totals + quarterly_global_trade_food
day 1   quarterly_deficit_check          ← reserve-sale fires HERE
day 9   quarterly_global_trade_luxury
day 18  ...luxury_2   day 27 ...type 3   day 36 ...type 4   day 45 ...type 5
day 54  quarterly_global_trade_6         ← gold/silver repriced HERE (53 days LATER)
day 61  quarterly_apply_trade_changes_and_consume
```

`quarterly_deficit_check` (day 1) → `DEBT_events.1` → `INCOME_mitigate_deficit` → reserve-sale branches
divide `treasury ÷ global_base_import_price_gold/silver` (se_INCOME.txt:580/599/659/673, +708). But
gold/silver are only repriced at **day 54**. So:
- **First quarter:** the boot type-6 pass (oa_economy_setup) computes price 0 (day-0 production is ~0
  because `GOODS_governorship_produce_all` first runs mid-quarter, not at setup) → deficit check at day 1
  divides by 0 → empty `local_var` → the ~104-line `Failed to fetch 'silver_needed_for_deficit'` /
  `unset scope` / `Invalid comparison` cluster + the `CURRENCY_private_purchase_or_sell_reserves` Div/0.
- **Later quarters:** the check reads the *previous* quarter's price (53 days stale), which is at least
  nonzero once trade has run — so the flood is heaviest at game start and for AI/`auto_fund_deficit`
  countries that hit a deficit in the early window.

This is a **cold-start + stale-read ordering bug**, not an absent feature and not a wrong price formula.

## 3. Candidate fixes (NOT adopted — for discussion only)

Two directions, both small:
- **Guard the divide.** In the reserve-sale, skip when `global_base_import_price_$metal$ <= 0` (can't
  sell at an unknown price; deficit falls through to next quarter — mirrors the existing logfix #19 guard
  at se_INCOME.txt:621-683). Kills the flood + the Div/0. Smallest blast radius. Does NOT fix the
  53-day-stale read in later quarters (cosmetically fine — price is nonzero then — but the sale is priced
  off last quarter's value).
- **Reorder.** Move `quarterly_deficit_check` to AFTER the type-6 trade pass (or seed a first-quarter
  metal price at setup). Fixes staleness too, but touches the pulse ordering, which has other consumers —
  higher risk of unintended interaction with the day-delay sequencing that the perf work (#139) tuned.

## 4. Why NOT to act yet

1. **It is a bug in Sobisonator's economy code** ([[imp19c-bug-vs-missing-feature-rule]] +
   [[imp19c-sobisonator-upstream-caution]]): the higher-risk category to touch. The guard is defensible
   (it only adds a skip on a genuinely-undefined divide, doesn't change his intended math when the price
   is valid), but the reorder is a real behavioural change to his pulse and should not be done
   speculatively.
2. **Unverified in-game.** The day-delay reconstruction is from static reading of oa_wealth_changes.txt;
   confirm against a `-debug_mode` boot (does the flood concentrate in Q1 / AI deficit countries as
   predicted?) before committing anything.
3. The original "missing feature" framing was wrong; do not over-correct into a confident bug-fix without
   the boot evidence.

## 5. Files
- `common/on_action/economy/oa_wealth_changes.txt:222-243` — the pulse day-delay ordering (root).
- `common/scripted_effects/se_INCOME.txt:536-708` — reserve-sale divides (where the guard would go).
- `common/scripted_effects/se_GLOBALTRADE_split.txt:2659/2697/2720` — the (working) metal-price setter.
- `common/on_action/economy/oa_economy_setup.txt` — boot trade pass + reserve seeding (cold-start).

## Appendix — corrections to the retracted draft (from the adversarial review)
- "SET NOWHERE" → WRONG: set unconditionally at se_GLOBALTRADE_split.txt:2659 (→ 0 for gold/silver in the
  zero window, not unset).
- "gold/silver not traded / not in stockpile system" → WRONG: they are tradegood_6, produced, demanded.
- se_INCOME read count: **7**, not 6 (missed the macro read at :708).
- `CURRENCY_reserve_value_in_wealth_gold/silver/_total` + `_reserve_to_gdp_ratio` cited as blast radius
  are **dead code** (only consumer is commented out at CURRENCY_svalues.txt:372).
- "metallic backing inert" → OVERSTATED: the live reserve-ratio/minting path runs off `units_to_the_lb`
  and works; only the `country_unit_price_*`-coupled minting base collapses during the zero window.
- Options B/C/D (fixed price / mint-parity derivation / make-it-a-traded-good) are all MOOT — they solve a
  non-existent missing-producer problem.

---

# Part II — What a reasonable metal-reserve pricing mechanic looks like, vs. the current one

Added 2026-08-04 after tracing the full price path. This part is DESIGN THINKING, not a patch —
it exists to answer "what SHOULD this look like" and "what would change." Still subject to the
Sobisonator-code caution: nothing here is adopted.

## II.1 The core conceptual error (the thing to fix)

The mechanic conflates two prices that should be distinct:

- **Market-clearing price** = "what did metal TRADE at this quarter" = `order_size ÷ stockpile × 0.6`,
  summed over zones and sqrt-dampened. Legitimately **0 when nothing traded**, and legitimately
  **noisy** when volume is thin (see Part I volatility analysis). Correct for deciding import costs.
- **Reserve/backing valuation** = "what is the metal I HOLD worth" = should be a **stable, always-defined
  intrinsic value**. A central bank's gold is worth ~its mint parity whether or not anyone traded gold
  this week.

The current code uses the FIRST for the SECOND. Both `backing_value` (se_CURRENCY.txt:1938) and the
deficit reserve-sale (se_INCOME.txt) price the reserve off the market-clearing price
(`country_unit_price_*` / `global_base_import_price_*`). That is why: reserves can't be sold in a
no-trade quarter (price 0 → divide error), backing whipsaws with thin-market noise, and the sale is
gated on an unrelated condition (did anyone else trade metal this quarter).

## II.2 What a reasonable mechanic would use: the mint parity as the intrinsic anchor

The mod ALREADY has the right primitive: **`units_to_the_lb`** (se_CURRENCY.txt:1842) — a static,
per-currency mint parity (currency units per pound of backing metal: £=62, tael=194 ["23.3856g"],
franc=1720, …). It is:
- **Always defined** (set once at currency instantiation, never 0),
- **Stable** (doesn't move with quarterly trade noise),
- **Already the metal↔currency conversion** the mint uses — i.e. literally "how much currency a pound of
  this metal is worth," which IS an intrinsic metal price expressed in currency units.

A reasonable **reserve valuation price** = a function of `units_to_the_lb` (metal→currency), converted
to the internal wealth/price scale. Reserve value = `reserve_size × intrinsic_metal_price`. This is
stable, never zero, and needs no same-quarter trade. The gold:silver relationship is the era-stable
~1:15 ratio (fixed is fine for 1815 scope).

Keep the market-clearing price for what it's actually for (import cost of buying metal), but do NOT let
the reserve/backing/sale paths depend on it.

## II.3 Design sketch (the mechanic)

1. **Intrinsic metal price** (new, stable): derive a world metal valuation from parity. Two clean
   options for the "global vs per-country" problem (Part I open-Q2):
   - **(a) Fixed world numéraire:** pick silver as the base, `intrinsic_price_silver = K` (a scale
     constant calibrated once against a mid-range good's `global_base_import_price` so reserves sit at a
     sane fraction of GDP), `intrinsic_price_gold = K × 15`. Simplest; no circularity; metal value is
     globally uniform (defensible — bullion is fungible worldwide).
   - **(b) Parity-derived per country:** value each country's reserve via ITS OWN currency's
     `units_to_the_lb` (a country on a debased standard values its metal in more of its own units).
     Richer, but reserve VALUE then can't feed currency BACKING without circularity — so (a) is the safe
     recommendation and (b) only if backing is decoupled.
2. **Reserve valuation** reads the intrinsic price (never the market price): `reserve_value =
   reserve_size × intrinsic_price_metal`. Feeds backing_value + the deficit sale amount.
3. **Market-clearing price** unchanged — still governs the cost of IMPORTING metal (if any AI/country
   buys bullion), still allowed to be 0/noisy, because nothing structural now depends on it being
   nonzero.
4. **Optional (only if metal is meant to have a market at all):** if gold/silver should trade, add
   price smoothing (an EMA / prior-quarter blend) so thin-market swings damp — but this is secondary;
   the primary fix is decoupling valuation from the market price.

## II.4 Concrete diff vs current implementation (what actually changes)

| Aspect | Current | Reasonable mechanic | Change size |
|---|---|---|---|
| Reserve/backing price source | market-clearing `country_unit_price_*` / raw `global_base_import_price_*` | new stable `intrinsic_price_metal` from `units_to_the_lb` | **new svalue(s)** + repoint ~a dozen reads |
| Price when no trade | 0 (→ divide error in sale; near-0 backing) | intrinsic parity value (never 0) | eliminates the error class + the whipsaw |
| Sale gated on same-quarter trade | yes (bug) | no | removes the unrelated coupling you flagged |
| Market-clearing price for imports | as-is | as-is (unchanged) | none |
| Scale calibration | implicit/broken for metals | one calibrated constant `K` | needs a -debug_mode price probe |

**Files that change:**
- `common/script_values/CURRENCY_svalues.txt` — add `CURRENCY_intrinsic_price_gold/silver` (from
  `units_to_the_lb` × scale); repoint the ~10 reserve/backing read sites from
  `global_base_import_price_*` / `country_unit_price_*` to the new svalue. This is the bulk of the work.
- `common/scripted_effects/se_CURRENCY.txt` — `CURRENCY_update_backing_value` (1938) reads the intrinsic
  price instead of `country_unit_price_gold/silver`.
- `common/scripted_effects/se_INCOME.txt` — the deficit reserve-sale (536-708) divides by the intrinsic
  price (never 0 → no guard needed, the error class disappears structurally rather than being silenced).
- NO change to `se_GLOBALTRADE_split.txt` metal pricing — the market price keeps doing its (real) job.

**Scope verdict:** medium. It's not a one-line guard and it's not a from-scratch feature — it's
"introduce one stable intrinsic-price svalue and repoint the ~dozen reserve reads at it." The market
machinery is untouched. The single hard prerequisite is the scale constant `K`, which needs one
runtime price probe to calibrate (so reserves are a sane fraction of the economy, not dust or a
juggernaut).

## II.5 Relationship to the quick fix

The Part-I "guard the divide" is a strict SUBSET of this: it stops the crash but leaves backing noisy
and reserves near-worthless in no-trade quarters. The Part-II mechanic is the actual fix — it removes
the crash AS A CONSEQUENCE of giving reserves a real, stable value. If we only want the errors gone,
guard. If we want reserves to MEAN something (the point of a metallic-standard currency sim), do II.
Either way, it's a change to Sobisonator's economy — hold for the boot-evidence + an explicit decision.

## II.6 Still-unverified before building
- The scale constant `K` (needs a real good's `global_base_import_price` at mid-game as the anchor).
- Whether ANY current consumer WANTS the noisy market metal price (grep before repointing — don't break
  an intended import-cost read).
- Whether Sobisonator intends metal to be tradable at all (affects II.3.4).
- Runtime confirmation that the market price is in fact frequently 0/noisy for metals (the whole premise).

_Related: [[imp19c-bug-vs-missing-feature-rule]], [[imp19c-sobisonator-upstream-caution]],
[[imp19c-economy-mechanics]]._
