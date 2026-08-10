# DESIGN — bimetallic economy: how gold + silver should relate (#59)

**Status:** RESEARCH/DESIGN note, 2026-08-10. Design-only; **gated on user green-light before implementation** (world-economy-scale, same family as the out-of-scope #60). Full pipeline: RESEARCH (history first) → this design → adversarial review → (user go) → implement → review. Batch with #44/#50/#52 for the DESIGN review; do NOT implement any of it yet.

*** STEP 0 — HISTORY FIRST (user, 2026-08-10): "the first step here is to consult history. what do academic sources say about the monetary interaction of gold/silver reserves." ***
Before the mechanic is designed, the historical monetary economics must be grounded from academic sources. A research task is dispatched to answer: how did gold and silver interact monetarily in the 18th-19th c. — bimetallism vs the silver standard (Qing) vs the emerging gold standard (West); Gresham's Law (bad money drives out good under a fixed legal ratio); the market vs mint ratio and arbitrage; the gold:silver ratio's actual path (China ~1:8-10 → converging to the Western ~1:14-15, and the silver-drain arbitrage that drove it); whether "reserves" of the two metals interacted at all or were valued independently; the classic bimetallism debates (e.g. Friedman on the "crime of 1873", Flandreau on 19th-c. bimetallism, Irigoin/von Glahn on Chinese silver). The RESEARCH DIGEST lands in research/RESEARCH_BIMETALLIC_MONETARY.md (per the research-digest-location rule); the TIER A/B decision below is PROVISIONAL pending that digest — the history may reveal the right mechanic is neither a fixed anchor nor active coupling but something the sources point to (e.g. a market-vs-mint-ratio arbitrage à la Gresham). Do NOT lock the mechanic until the research lands.

## The finding (from the Aug-9 22:42 logs)
The mod prices gold and silver as **two INDEPENDENT floats**, each on its own trade-zone supply/demand, with **NO ratio peg and NO substitution** between them. CHI demand: gold 100-1000 vs silver 10-100; yet silver PAID-PRICE 1-10 > gold 0.1-1→1-10 — because silver stock is scarcer relative to its demand (the silver-standard money-metal, #46 WAI). Result: silver runs dear, gold cheap, and nothing links the two.

Historically the two metals were coupled by an **exchange ratio** (~1:14-15 gold:silver by 1763 in the West; China ran nearer 1:8-10 earlier, converging over the century — an arbitrage the silver inflow to China exploited). The mod has no such coupling.

## What already exists (do NOT rebuild)
DESIGN_METAL_RESERVE_PRICING.md already established the right primitive: **`units_to_the_lb`** (se_CURRENCY.txt:1842) — a static per-currency mint parity, always-defined, stable, = the intrinsic metal↔currency conversion. It proposes an `intrinsic_price_metal` svalue with `intrinsic_price_gold = intrinsic_price_silver × 15` (the era-stable ratio), used for RESERVE VALUATION (decoupled from the noisy market-clearing price). #59 should BUILD ON that, not duplicate it — the ratio anchor is half-designed there already.

## The #59 question, sharpened
Given the market prices the two metals independently, should there be:
1. **A ratio ANCHOR** — gold and silver prices tethered to a ~1:15 band, so they can't drift arbitrarily apart? AND/OR
2. **SUBSTITUTION** — when the ratio diverges (e.g. silver becomes very dear relative to gold), agents/economy shift toward the cheaper metal, pulling the ratio back?

## Scope decision (the load-bearing call) — RECOMMEND the SMALL version
The user ruled the **M1/circulation bimetallic rework (#60) OUT OF SCOPE** ("would significantly alter the world economy"). #59 must stay on the RIGHT side of that line. Two tiers:

**TIER A (RECOMMENDED, small, safe): valuation-ratio anchor only — no market coupling.**
- Adopt the METAL_RESERVE_PRICING intrinsic-price approach: reserve VALUATION uses a stable parity-derived price with gold = silver × ~15. This gives the two metals a correct RELATIVE value for RESERVES (戶部銀庫 valuation, sell-reserve price) WITHOUT touching the market-clearing float or M1.
- The market-clearing price (import cost of buying metal) stays independent + noisy — nothing structural depends on it.
- This makes the Sell-Reserves screen and reserve valuation reflect the historical ~1:15 relationship (fixes the "gold cheaper than silver in a way that looks wrong for reserves" perception) WITHOUT the world-economy-scale rework the user vetoed. It is essentially a scoping of the already-designed METAL_RESERVE_PRICING work to also serve #59's ratio concern.

**TIER B (LARGER, needs explicit green-light): active bimetallic market coupling.**
- Add substitution: when the traded gold:silver ratio diverges from the peg, nudge demand/supply toward the cheaper metal so the ratio mean-reverts. This DOES touch the market floats + trade income for all countries → world-economy-scale → the #60 veto zone. Only if the user explicitly wants it.

**RECOMMENDATION: implement TIER A (fold into / alongside METAL_RESERVE_PRICING), leave TIER B parked behind the green-light.** Tier A satisfies the historical-ratio concern at reserve-valuation level (the visible "silver > gold looks off" surface) without destabilizing the currency model the #23 sqrt fix stabilized or the M1 model #60 left as an accepted limitation.

## Interaction constraints (must not break)
- **#23 currency chain**: the sqrt-stabilized gbip loop must stay flat — a valuation-only ratio anchor doesn't touch gbip, but confirm.
- **#42/#54 reserve display**: the reserve-change display (qing_silver_reserve_change_last) reads silver_reserve_size directly; a valuation-price change affects the DISPLAYED VALUE, not the size — confirm the change-indicator still reads right.
- **#46 silver-standard (WAI)**: silver being demanded/dear is CORRECT High-Qing behaviour; the ratio anchor must not erase the silver-standard character (CHI-specific), only stop gold/silver drifting to absurd relative values.
- **#60 (accepted limitation)**: do NOT reopen the M1/circulation bimetallic question — Tier A is reserve-valuation only.
- **Global**: silver-standard is CHI-specific; the West was moving toward gold. A fixed ~1:15 anchor is a reasonable global numéraire (bullion is fungible worldwide, per METAL_RESERVE_PRICING §II.3 option a); a per-country ratio is richer but risks circularity in backing — use the fixed anchor.

## Files (TIER A, if greenlit)
- common/script_values/CURRENCY_svalues.txt — the intrinsic_price_gold/silver svalues (per METAL_RESERVE_PRICING); repoint reserve-valuation/sell-reserve reads to them.
- (No M1/circulation changes. No market-float changes. No province/country blocks.)

## Verify (TIER A)
- Sell-Reserves / reserve valuation shows gold ≈ 15× silver per unit weight (the historical ratio), stable across quarters (not the noisy market float).
- #23 gbip flat; #42/#54 reserve-change display still correct; #46 silver-standard character intact; no ROW destabilization.

## OPEN for the user (before ANY #59 implementation)
- Confirm TIER A (valuation-ratio anchor, small) vs TIER B (active market coupling, world-economy-scale). Default recommendation: TIER A.
- Confirm #59 Tier A should be MERGED with the METAL_RESERVE_PRICING work (they're the same svalue) rather than a separate change.
