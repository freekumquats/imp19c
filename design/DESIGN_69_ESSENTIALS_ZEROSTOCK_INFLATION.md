# DESIGN — #69: essentials cost-of-living collapses to ~0 on total goods depletion, causing permanent inflation

## Status
Diagnosis: adversarially reviewed CLEAN, twice (round 1 refuted the reserve-ratio-rail as the
trigger and found the numerator collapse instead; round 2 confirmed the exact mechanism and
ruled out every other candidate). This doc is the design for the FIX — not yet reviewed.

## The bug, precisely

`CURRENCY_essentials_buying_power` ("ess", `common/script_values/CURRENCY_svalues.txt:673-701`)
computes cost-of-living as:

```
ess = (Σ country_unit_price_<good> for 12 goods) / CURRENCY_wealth_value_1_unit_scaled_by_reserve_ratio
```

`country_unit_price_<good>` is fed by `global_base_import_price_$tradegood$`
(`common/scripted_effects/se_GLOBALTRADE_split.txt`, `GT_split_get_global_import_unit_price_tradegood`),
which is itself:

```
global_base_import_price_<good> = Σ over 22 trade zones of (local_price_zone × zone_percentage_of_global_stockpile)
```

`zone_percentage_of_global_stockpile` (`se_GLOBALTRADE_split.txt:1505-1519`, repeated per zone) is
initialized to the RAW zone stockpile, then converted to a true 0-1 percentage only
`if zone_stockpile > 0 AND global_stockpile > 0`. **When a good's GLOBAL stockpile is 0 (every
zone simultaneously out of stock), every zone's stockpile is 0 too, so every zone's "percentage"
term is left at 0 (not stale — genuinely 0, since the raw value was already 0).** The weighted
sum therefore collapses to exactly 0 regardless of what each zone's `local_price` actually is.

Confirmed for `vegetables` specifically in the Aug 14 boot: global stock hits exactly 0 in every
one of 22 zones by quarter-mark 11 (`tools/vegetables_trace.py`), and at that exact quarter-mark
`country_unit_price_vegetables` crosses from the "1-10" price band to "0-0.01"
(`tools/ess_price_trace.py`) — the ONLY one of the 12 `ess`-formula goods to cross a band at that
mark. The resulting ess numerator drop (16.9 → 9.1, exact-tick data via `curx_analyze.py`) is
large enough to explain the whole move ON ITS OWN **provided vegetables' pre-crash contribution
was near the top of its stated "1-10" band (~7-8), not mid-band** — the band data alone doesn't
pin the exact pre-crash value, so this is a bound consistent with the observed drop, not an
unconditional proof that vegetables is the sole contributor.

**Why this causes inflation, not deflation (the counterintuitive part):** `ess` feeds
`CURRENCY_private_cash_needed` positively (:719-732); `private_cash_needed` feeds
`CURRENCY_private_cash_ratio` as its divisor (:753-766); `CURRENCY_amt_circulated_inflation`
(:1180-1193) goes positive and STAYS positive once that ratio crosses 1. A LOWER ess means a
LOWER cash_needed means a HIGHER ratio means MORE inflation. So the bug makes a good becoming
totally unavailable register as free, which is read by the formula as "less cash is needed to
cover cost of living," which triggers the *opposite* of the economically sound outcome (a
genuine scarcity price spike would raise `ess`, which this formula's own comment says should
cause deflation pressure, not inflation, if cash supply doesn't keep pace).

## Provenance (git blame, per explicit request)

The zero-guard pattern (`value = raw_stockpile`, then conditionally divide) was introduced by
**Sobisonator** (`bomchasew@gmail.com`) on **23 April 2024**, commit `73ad408253` — *"Added a
method to split global trade out between 4 effects, reducing the wait time for the player."* A
pure performance-optimization commit (splitting one heavy calculation across 4 ticks to reduce
lag); the zero-stock edge case was almost certainly never in scope for that change. This is
upstream code, not a recent regression in this fork, and not something this session's
add_treasury/LOG_line sweeps touched. It has been live for over a year; it only manifests when a
good's stock hits *total, simultaneous, every-zone* depletion, which is why it hasn't surfaced
before now — vegetables' thin province-assignment base (419 provinces vs 1700+ for grain/
livestock) is apparently the first good to actually hit that condition in a long enough boot.

## Consumers of the shared value (why the fix must NOT touch `global_base_import_price` itself)

`global_base_import_price_$tradegood$` is read by, at minimum:
- `se_ECON_wealth.txt:556` (a wealth multiplier, all goods)
- `se_INCOME.txt` (metal minting/reserve income, gold and silver specifically) — **already
  guards every division with `global_var:global_base_import_price_<metal> > 0` before dividing**
  (lines 612, 634, 706, 724) — i.e. this codebase already has a PROVEN pattern for "this might be
  zero, branch around it" at the consumer site, not at the shared value's own computation.
- `se_QING_BIMETALLIC.txt:55-63` (the Gresham gold:silver pull) — same `> 0` guard pattern.
- `CURRENCY_svalues.txt` (silver/gold wealth-value-per-unit formulas)
- Multiple `ECON_LOG`/`TZPROBE` read-only diagnostic probes.
- `WEALTH_svalues.txt:1387/1393` (`WEALTH_cost_of_living`, which also reads `ess`) →
  `WEALTH_cost_of_living_modifier` → `WEALTH_subtract_cost_of_living` (a pop-wealth-drain
  effect). **Confirmed DEAD/inert, not a live consumer**: the cache write
  (`se_ECON_wealth.txt:1051-1059`, `WEALTH_cache_national_cost_of_living`) is only called at
  `on_game_initialized`, never quarterly, and the drain effect itself
  (`se_ECON_wealth.txt:1017-1023`, `:1084-1103`) is never invoked by any on_action/event/effect
  anywhere in the codebase. Named here explicitly so a future reviver of that chain knows it
  will inherit whatever `ess` does — including this fix — without re-diagnosing it.

Given how widely shared and upstream this value is, and the standing fix-must-be-delicate rule
(don't touch the underlying trade/pricing system, only the specific broken consumption of it):
**the fix targets `CURRENCY_essentials_buying_power`'s per-good term, not
`global_base_import_price` or the zone-percentage computation.** Changing the shared value's
core math risks silently altering gold/silver minting income and the bimetallic pull, which are
tuned against its CURRENT behavior (including its existing zero-guards, which already treat 0 as
a valid, expected state for metals). This bug is specific to how `ess` interprets that 0, not to
the shared value's computation being wrong in general.

## Proposed fix

In `CURRENCY_essentials_buying_power` (`CURRENCY_svalues.txt:673-701`), for each of the 12 goods,
detect the good's GLOBAL stockpile reading 0 (`global_var:global_stockpile_<good>` — the same
condition the bug's own root cause hinges on; the stockpile check alone is sufficient and simpler
than also re-checking `country_unit_price_<good>`'s value, since on a collapse tick that price is
already known to be pinned near its floor) and, for that term ONLY, hold forward the last known
genuine (nonzero-stockpile) price instead of adding the collapsed value.

Mechanism: a `<good>_ess_last_nonzero_price` per-country variable (see Implementation sketch for
the exact naming/insertion point), updated every time `global_var:global_stockpile_<good> > 0`
(i.e. every normal tick), left untouched when stockpile is 0. `CURRENCY_essentials_buying_power`'s
sum then reads, per good: `global_var:global_stockpile_<good> > 0 ? country_unit_price_<good> :
var:<good>_ess_last_nonzero_price`.

Why hold-last-value over the alternatives:
- **Not "skip the term from the sum"**: omitting it changes the sum's scale/units for every OTHER
  quarter comparison and is itself a silent behavior change to a widely-read index; also doesn't
  correct the direction (still short of what a true scarcity premium should add).
- **Not "substitute a fixed high ceiling"**: inventing a magic ceiling number is an unverified
  guess with no source-grounded justification, and risks overcorrecting into artificial deflation
  if the ceiling is picked wrong. Held-last-value is the only option that's both grounded in a
  REAL, previously-observed price (not invented) and requires no new tuning constant.
- **Not "fix the shared zone-percentage math"**: per the consumers section above, too wide a
  blast radius for a fix that's supposed to be delicate.
- This mirrors an EXISTING convention already used elsewhere in this codebase for cached
  "_last"-suffixed values bridging a tick where fresh data isn't available (per this session's
  own #79 visibility work, which found and used the exact same hold-last-value shape for the
  one-shot-grant accumulator).

## Implementation sketch (for the review, not final code)

**Correction from round-1 review**: the original sketch below proposed 12 hand-written snapshot
blocks inserted into `common/on_action/economy/oa_wealth_changes.txt`. That is the WRONG
location — `country_unit_price_<good>` is not set there at all. It is set by a single generic
macro, `GT_split_get_country_import_unit_price_tradegood`
(`se_GLOBALTRADE_split.txt:2878-2892`), invoked for every good via
`GT_split_get_country_import_unit_price_all` (:2872-2876,
`every_tradegood_$type$_complex` + `APPLY`):

```
GT_split_get_country_import_unit_price_all = {
	every_tradegood_$type$_complex = {
		APPLY = GT_split_get_country_import_unit_price_tradegood
	}
}

GT_split_get_country_import_unit_price_tradegood = {
	# Scope: Country
	set_variable = {
		name = country_unit_price_$tradegood$
		value = {
			value = global_var:global_base_import_price_$tradegood$
			min = 0.0001
			divide = {
				value = 0.5
				add = var:country_global_market_penetration_$tradegood$
			}
		}
	}
}
```

The fix now targets this macro directly — ONE insertion, parametrized by the existing
`$tradegood$` substitution, covers every good for free (not 12 hand-written blocks):

1. No new per-country variables list to hand-maintain. Add ONE snapshot `set_variable` inside
   `GT_split_get_country_import_unit_price_tradegood`, immediately after the existing
   `set_variable = { name = country_unit_price_$tradegood$ ... }` block, guarded with the
   PROVEN two-clause form already used at `se_GLOBALTRADE_split.txt:6086-6089` (from the prior
   `#107` day-0-unset-global fix, for the identical class of problem — a bare `> 0` on a global
   that may not exist yet is not safe inside a `value{}` script_value at day 0):

   ```
   if = {
   	limit = {
   		has_global_variable = global_stockpile_$tradegood$
   		global_var:global_stockpile_$tradegood$ > 0
   	}
   	set_variable = {
   		name = $tradegood$_ess_last_nonzero_price
   		value = var:country_unit_price_$tradegood$
   	}
   }
   ```

   This runs for every good on every tick `GT_split_get_country_import_unit_price_all` fires
   (i.e. every good gets a `_ess_last_nonzero_price` snapshot, not just the 12 `ess`-formula
   goods — a side effect of piggybacking on the shared macro rather than hand-picking 12 sites;
   harmless, since the extra snapshots are simply unread by anything outside `ess`).

2. In `CURRENCY_essentials_buying_power`, replace each flat `add = var:country_unit_price_<good>`
   term (for the 12 `ess`-formula goods specifically) with an `if/else_if/else`:
   - `if = { limit = { has_global_variable = global_stockpile_<good>  global_var:global_stockpile_<good> > 0 } }` → add the live `var:country_unit_price_<good>` (today's behavior, unchanged
     for the normal case).
   - `else_if = { limit = { has_variable = <good>_ess_last_nonzero_price } }` → add the held
     `var:<good>_ess_last_nonzero_price` instead of the collapsed live value.
   - `else` (stockpile never had a nonzero tick yet — genuine day-0 edge case, not the
     depleted-later case this bug is about) → add 0, i.e. today's behavior is preserved for
     that one edge case only.
3. No change to `global_base_import_price`, the zone-percentage computation, `se_INCOME.txt`,
   `se_QING_BIMETALLIC.txt`, `WEALTH_cost_of_living` (confirmed dead above), or any
   metal-specific consumer — the snapshot and the `ess`-side substitution are the only edits.

## Risks / open questions for adversarial review

- Does `global_var:global_stockpile_<good>` exist/read correctly at the exact point
  `CURRENCY_essentials_buying_power` is evaluated (scope/timing check needed)?
- Are there OTHER goods (beyond the 12 in ess) that could hit the same total-depletion state and
  would benefit from the identical treatment, or is this fix deliberately scoped to only the 12
  ess-formula goods per the delicate-fix principle?
- Does holding the last-known price forever (no decay, no re-scarcity premium) risk UNDER-pricing
  a good that stays depleted for a very long time (multiple years), versus a real economy where
  sustained unavailability should keep pushing perceived cost up, not flatline it? Is a flat hold
  an acceptable simplification for this mod's scope, or does it need a slow decay/creep back
  toward a ceiling the longer stockpile stays at 0?
- Interaction with #79 (tariffs magnitude): this fix does NOT address #79, which was found to
  depend on engine-internal `this_expenses_from_manufacturing_<strata>` vars decoupled from both
  `country_unit_price` and `local_price` — #79 remains a separate, still-open investigation.
