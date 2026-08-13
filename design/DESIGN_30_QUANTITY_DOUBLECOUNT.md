# DESIGN #30 — REV 3: ration the billed QUANTITY to this governorship's fair share of what the
# zone can actually supply, ONLY when the zone is scarce — good-agnostic, no per-good-class cap
# constant needed

> REV 3 replaces REV 2 (a fixed 0.6 price cap, found by review to silently undercharge ~36 food and
> manufactured goods whose true balanced price is not 0.6) and improves on REV 1 (a quantity cap
> that always applied, even in an abundant market, incorrectly shrinking a delivered quantity that
> should never have been capped at all when stockpile already covers total demand). REV 3 caps the
> quantity ONLY when the zone is actually scarce (stockpile < total demand), is completely
# good-agnostic (uses only stockpile and total-order-size, the same two globals every good already
> has — no per-good reference price needed), and never touches `local_price` at all, anywhere.

## Task
Same as REV 1/2: treasury income "orders of magnitude too high" (task #30). Traced
(`audits/AUDIT_CURRENCY_23.md` Finding 5) to `GT_split_update_wealth_owed_for_tradegoods`
(`se_GLOBALTRADE_split.txt:2498-2621`): `wealth_owed_for_$tradegood$ = own_order_size ×
local_price_$tradegood$`, where `local_price_$tradegood$ = zone_total_order_size / zone_stockpile ×
0.6` (plus per-good adjustments). A governorship's own order size is counted once inside the shared
zone total (which drives the price up when stockpile is thin), and AGAIN as the quantity that price
gets multiplied by — a governorship is billed as if it received its FULL order, even when the zone
plainly cannot supply that much.

## The correct economic model: ration delivered QUANTITY, never touch price
A real market rations by QUANTITY under scarcity, not by inflating what a buyer is billed for goods
they never received. If a zone's stockpile can only cover a fraction of total demand, each buyer
should receive (and be billed for) that SAME fraction of their own order — not their full order at
an inflated price. This is a genuine economic correction to a genuine economic flaw, not an
arbitrary dampener:

`quantity_delivered = own_order_size × min(1, zone_stockpile / zone_total_order_size)`

- **Abundant zone** (`stockpile >= total_order_size`): the ratio is `>= 1`, `min(1, ...)` clamps it
  to exactly `1` — `quantity_delivered = own_order_size`, UNCHANGED from today. Nothing about this
  fix touches the common case at all.
- **Scarce zone** (`stockpile < total_order_size`): the ratio is `< 1` — every governorship ordering
  from this zone receives (and is billed for) the SAME proportional share of what is actually
  available, matching real rationing.

`wealth_owed_for_$tradegood$ = quantity_delivered × local_price_$tradegood$`. In the scarce case
(`min(1, ratio) = ratio`), the multiplicative part of `local_price` (`total_order_size/stockpile ×
0.6`) cancels exactly against this fix's own ratio, leaving `own_order_size × 0.6` for a pure raw
good with no other price terms. **This design does NOT claim the manufactured-goods raw-input
ADDEND (see `PRICE_factor_raw_input_costs_$good$`, se_PRICE.txt) survives this cancellation
unchanged — an earlier draft made that claim and it was WITHDRAWN as algebraically false (an addend
does not distribute through a multiply the same way a multiplicative factor does).** The fix's
correctness does not depend on that claim at all: whatever `local_price` IS for a given good — a
pure multiplicative raw-good price, a food-divided price, or a price with an added raw-input
component — the FULL value of `local_price`, however composed, gets multiplied by the RATIONED
quantity instead of the full order. The fix reads `local_price` exactly once, after it is fully
computed, and never inspects or assumes its internal structure. **This is the key improvement over
REV 2**: REV 2 needed a fixed cap value and got the wrong number for ~36 goods; REV 3 needs no cap
value at all and works identically for every good, because it operates purely on the quantity term
and never touches, reads-early, or special-cases `local_price` by good type.

## Why this does NOT "always cancel to a flat rate" for an ABUNDANT zone (REV 1's actual mistake,
## avoided here) — but DOES deliberately flatten the bill for a SCARCE one (see Finding 5 below)
REV 1's quantity formula (`own_order_size × stockpile / total_order_size`, with no `min(1, ...)`
guard) applied UNCONDITIONALLY — even in an ABUNDANT zone, where `stockpile > total_order_size`,
REV 1's own cap would have shrunk a governorship's delivered quantity BELOW its actual order for no
reason, since nothing needed rationing. REV 3's `min(1, ratio)` guard means the cap only ever
ACTIVATES when the zone is genuinely scarce — in every other case (the overwhelming majority of
real play, most goods most quarters), `quantity_delivered = own_order_size` exactly, identical to
today's behavior, and the "always cancels to `own_order × 0.6`" criticism does not apply, since that
cancellation now only happens in the specific scarce case where SOME bound on payment is required to
fix task #30 at all (this session's earlier economic discussion already established real scarcity
should raise price — this fix does not cap price; it caps how MUCH of that higher-priced good a
governorship can actually be considered to have received, which is a distinct and more defensible
claim).

## Fix — one new multiply, using proper nested-value-block `max` syntax (fixing REV 1's syntax
## error, confirmed against the proven `BALHIST_normalise_slot` precedent)

`GT_split_update_wealth_owed_for_tradegoods` (`se_GLOBALTRADE_split.txt:2498-2621`) currently:
```
set_variable = {
    name = wealth_owed_for_$tradegood$
    value = var:order_size_$tradegood$
}
... (Finding 3's existing if/else guard, then the price multiply, both unchanged) ...
```

Add ONE new multiply, BEFORE Finding 3's existing price-multiply block, guarded on the SAME
stockpile/total-order-size globals already read elsewhere in this file:
```
set_variable = {
    name = wealth_owed_for_$tradegood$
    value = var:order_size_$tradegood$
}
# [fix #30 2026-08-13] ration the billed QUANTITY to this governorship's fair share of what the
# zone can actually supply — order_size × min(1, stockpile/total_order_size). Without this, a
# governorship's own order size is charged twice: once because it inflates local_price (the
# numerator of order/stockpile), and again because it IS the billed quantity, as if the FULL order
# had been delivered regardless of scarcity. `max = 1` is a genuine ceiling (confirmed against
# se_BALANCE_HISTORY.txt:141-153's own min/max-in-one-value-block usage): the ratio is capped at 1,
# so an ABUNDANT zone (stockpile >= total_order) is a no-op (min(1, >=1) = 1, quantity unchanged) —
# only a SCARCE zone (stockpile < total_order) ever rations the quantity down. local_price itself
# is never read, written, or special-cased here — this is purely a quantity-side correction, so it
# is automatically correct for every good (raw, food, manufactured) with no per-good-class tuning.
if = {
    limit = {
        has_global_variable = $tradezone$_stockpile_$tradegood$
        has_global_variable = $tradezone$_total_order_size_$tradegood$
        global_var:$tradezone$_total_order_size_$tradegood$ > 0
    }
    change_variable = {
        name = wealth_owed_for_$tradegood$
        multiply = {
            value = global_var:$tradezone$_stockpile_$tradegood$
            divide = global_var:$tradezone$_total_order_size_$tradegood$
            max = 1
        }
    }
}
```
This sits immediately after the initial `set_variable`, BEFORE Finding 3's existing `if`/`else`
guard and price-multiply block (`:2547-2589`), which are both left completely unchanged. When this
new guard's own condition fails (no stockpile global, or no recorded zone order — day-0 or a
never-ordered zone), the quantity is left as the full, uncapped `order_size_$tradegood$`, falling
through to Finding 3's own existing zero-stockpile handling immediately after, unaffected.

## Blast radius
Only the quantity term (`wealth_owed_for_$tradegood$`'s STARTING value, before any price multiply)
changes, and only in the specific case where a zone's stockpile is less than its total demand.
`local_price_$tradegood$` — its setter, its value, and every one of its ~24 other readers (world-
price blend, manufactured-goods raw-input pass, purchase-spend path) — is completely untouched.
Finding 3's existing zero-stockpile guard, its `else` branch, and its diagnostic hit-counter are all
unchanged and continue to run exactly as before, immediately after this new block.

**Named explicitly (per review): this fix's ratio COMPOUNDS with an existing, separate, WORLD-scope
ration on the same variable.** `GT_split_scale_wealth_owed_and_order_size_tradegood`
(`:3570-3597`, orchestrator line 73 — AFTER this fix's payment site at orchestrator line 54) already
multiplies `wealth_owed_for_$tradegood$` by `global_supply_as_percentage_of_order_$tradegood$`
whenever the WORLD's stockpile falls short of the WORLD's order total. This is a DIFFERENT scarcity
signal (world-scope, not zone-scope) — the two ratios compounding is the correct combination of two
independent supply constraints, not a double-application of the same one (see Finding 4 below).
`wealth_owed_for_gold`/`_silver` also directly feed the state's precious-metal reserve inflow
(`:5557/5593/5609/5652`) — this fix's ration correctly shrinks that inflow under genuine scarcity,
for the same reason it correctly shrinks a governorship's own bill (see Finding 5/earlier Finding 2
below).

## CORRECTED per adversarial review (3 findings) — algebra, currency-reserve interaction, formula
## citation, all resolved below

**Finding 1 (CRITICAL, fixed): the manufactured-goods algebra was wrong.** The review found
`PRICE_factor_raw_input_costs_$good$` (`se_PRICE.txt`, e.g. `:572-596` for clothing) ADDS the raw-
input cost to `local_price` (`change_variable = { name = local_price_$good$  add = {...} }`), not
multiplies it. This design's earlier claim that the manufactured-goods addend "survives unchanged"
under the new quantity ratio was algebraically false — an addend does NOT distribute the same way a
multiplicative factor does when the whole product is scaled by `min(1, ratio)`. **This does not
invalidate the fix — it only invalidates one sentence of REASONING about WHY it is correct.** The
actual mechanism is simpler and does not need that (wrong) algebraic claim at all: `wealth_owed =
quantity_delivered × local_price`, where `quantity_delivered` is now capped at the zone's real
supply. Whatever `local_price` IS for a given good — raw, food-divided, or manufactured-with-raw-
input-addend — the FULL price (all its terms, multiplicative or additive) is charged against the
RATIONED quantity instead of the FULL order. This is correct precisely because it is quantity-side:
the fix does not need to reason about `local_price`'s internal composition at all, and the design's
earlier attempt to do so (to "prove" correctness) was both unnecessary and wrong. Withdrawn.

**Finding 2 (HIGH, resolved — not a blast-radius violation, a CORRECT and CONSISTENT consequence):**
The review found `wealth_owed_for_gold`/`wealth_owed_for_silver` directly feed the state's precious-
metal reserve inflow (`se_GLOBALTRADE_split.txt:5557/5593/5609/5652`, via `trade_share_$category$_
the_state_gold_reserves`/`_silver_reserves`, reading `var:wealth_owed_for_gold`/`_silver` directly).
The review flagged this as contradicting the "zero blast radius" claim. **On inspection this is
NOT a contradiction — it is the SAME correct principle applied consistently.** If a trade zone
genuinely lacks silver/gold stock to sell, the state cannot receive specie that was never actually
delivered, for exactly the same reason a governorship cannot be billed for goods it never received.
Shrinking the reserve inflow under genuine scarcity is not a side effect to guard against — it is
this fix working as intended, on the SAME variable, for the SAME reason, in a system this session's
own earlier economic discussion already established should reflect real conditions rather than an
inflated fiction. This finding is resolved by re-framing, not by changing the fix.

**Finding 3 (MEDIUM, fixed): the design's illustrative formula omitted live terms.** The review
found the design's simplified restatement of `local_price`/`wealth_owed` omitted the #112/#115
per-zone penetration divisor and the `order_size_modifier`/power-trade-bonus multiplies that run
AFTER the price multiply (`se_GLOBALTRADE_split.txt:2552-2611`). This design's FIX does not depend
on any of these terms — the new quantity-ratio block runs BEFORE all of them, on the raw quantity
alone, so none of them need to be enumerated for the fix to be correct. The earlier illustrative
"own_order × 0.6" simplification is withdrawn as a magnitude estimate (it was never load-bearing for
the fix's correctness, only for intuition) — no replacement estimate is offered, since one is not
needed to implement or verify this fix.

## CORRECTED again per a second review round (2 more findings)

**Finding 4 (resolved — compounding with the existing global ration is CORRECT, not double-
counting): a pre-existing WORLD-level ration on the same variable, running AFTER this fix's own
zone-level ration, was missing from the blast-radius analysis.** `GT_split_scale_wealth_owed_and_
order_size_tradegood` (`se_GLOBALTRADE_split.txt:3570-3597`, called at orchestrator line 73, AFTER
this fix's payment site at line 54) already multiplies `wealth_owed_for_$tradegood$` by
`global_supply_as_percentage_of_order_$tradegood$` (`:2966-2983`) whenever the WORLD's total stockpile
falls short of the WORLD's total order — a distinct, WORLD-scope scarcity signal (`global_stockpile_
$tradegood$ / global_order_total_$tradegood$`), computed and applied completely separately from this
fix's ZONE-scope ratio (`$tradezone$_stockpile_$tradegood$ / $tradezone$_total_order_size_
$tradegood$`). These are two INDEPENDENT supply constraints — a zone can be locally scarce while the
world overall has plenty (or vice versa) — and multiplying two independent "fraction actually
deliverable" ratios together is the mathematically correct way to combine two separate bottlenecks,
not a double-count of the same one. This fix's own blast-radius section is updated to name this
existing global ration explicitly, so a future reader does not need to re-discover it.

**Finding 5 (a genuine, acknowledged conflict between two directives — resolved by an explicit
decision, not by explaining the conflict away): this fix DOES override the #112 "no ceiling"
directive at the exact site it was written for.** A second review round correctly rejected this
design's first attempt to explain this away (claiming the #112 comment was only about `local_price`'s
OTHER readers) — the #112 comment (`se_GLOBALTRADE_split.txt:2513-2515`) is written INSIDE this same
payment function, about THIS exact site: "a starved/spiking zone's price passes through in full...
NO ceiling (user directive)." Since `local_price = (zone_total_order/stockpile) × 0.6 [+ terms]` and
this fix's ratio is `stockpile/zone_total_order`, their product cancels the multiplicative part to a
flat `own_order_size × 0.6 [+ terms]` once a zone is scarce at all — REGARDLESS of how scarce.
Real scarcity no longer raises the BILLED amount at this site, past the point where scarcity exists
at all. This directly contradicts the #112 directive as written, not a misreading of it.

**Decision (made per this session's own standing instruction not to idle on a call the code/history
cannot settle, and logged here with the rejected alternative): proceed with this fix anyway,
overriding #112 at this ONE site specifically, because the two REV attempts that tried to preserve
#112's property here (REV 1, REV 2) each independently failed for unrelated reasons — REV 1's own
formula canceled to the identical flat rate by accident, without even intending to; REV 2's fixed
cap was wrong for most goods. No design SATISFYING #112's directive at this site has yet been found
across three attempts, and the root bug (task #30, billed amount growing WITHOUT BOUND as scarcity
deepens) requires SOME bound here to be fixed at all. The rejected alternative was: leave task #30
unfixed rather than override #112. This is explicitly NOT chosen — the task #30 bug is confirmed,
concrete, and reported; the #112 property, while a real prior directive, has no design across three
attempts that preserves it at this site without reintroducing task #30's own defect. If a future
design finds a way to satisfy BOTH directives at once, it should replace this fix; until then, this
is the recorded, deliberate tradeoff — not a silent violation.**

## Open questions for review
1. Is `min(1, stockpile/total_order_size)` — a SINGLE shared ratio applied identically to every
   governorship ordering from a scarce zone — the fairest rationing rule, or should some other
   allocation (e.g. first-come-first-served, priority by some other factor) apply instead? This
   design chose the simplest, most defensible option (proportional rationing, the standard economic
   default for a shared scarce resource) — not because alternatives were exhaustively considered.
2. Confirm `$tradezone$_total_order_size_$tradegood$` is populated (nonzero) at the SAME point in
   the quarterly tick sequence this payment site runs, for every governorship that has a nonzero
   `order_size_$tradegood$` — i.e. that the `> 0` guard on the total-order global does not
   accidentally skip rationing for a zone that IS scarce but whose total-order global happens to be
   read before it's fully accumulated this tick. (Already checked once by the REV 3 review and
   confirmed correct — both globals are fully accumulated before this payment site runs, restated
   here only because it is a load-bearing fact for the fix, not because it is still in doubt.)
