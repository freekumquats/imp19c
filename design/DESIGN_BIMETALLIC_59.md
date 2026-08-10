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

## HISTORY DIGEST LANDED (research/RESEARCH_BIMETALLIC_MONETARY.md, 2026-08-10) — reshapes the mechanic
The mandated history-first research returned. Key findings + how they change this design:
- **Regime at 1763 AND 1815:** bimetallism (fixed statutory MINT ratio) + silver-standard China are the NORM; the gold standard is the exception (only Britain, informally pre-1816). France 15.5:1, US 15:1, both bimetallic through both bookmarks. So the two metals were monetarily RELATED everywhere — the mod's fully-independent float has NO historical analogue anywhere in the period.
- **Ratio:** China ~1:8-10 (17th c.) → converged to ~1:14-15 by 1750-63 (matching the Western peg), driven by the Canton/Manila silver inflow + gold-out arbitrage. The ~1:15 anchor is the converged, stable pre-1873 reality for BOTH bookmarks.
- **Mechanism = Gresham's Law arbitrage** against a fixed ratio (confirmed the operative force in every historical bimetallic breakdown; Friedman/Flandreau vs Redish/Kindleberger debate its robustness but all agree the mechanism is arbitrage vs a fixed legal ratio). So the right mechanic is a SOFT BAND with mean-reversion, NOT a hard peg and NOT independence.
- *** THE CRUCIAL CORRECTION (Kuroda, Socio-Economic History 57:2 1991): *** China's REAL functioning "bimetallism" was **SILVER vs COPPER CASH**, and it FLOATED (Qing set NO fixed silver:copper ratio — unlike the West's fixed mint ratios). **GOLD was a COMMODITY / trade-arbitrage good in China, NOT a monetary reserve metal.** => the gold:silver mechanic must be scoped as an EXTERNAL / TRADE-VALUATION relationship (how bullion reserves are valued against the world ~1:15 ratio), NOT as China's domestic money system. China's domestic money question (silver:copper, floating) is SEPARATE and already partly modelled (backing_type = silver_standard, se_CURRENCY.txt) — do NOT conflate them. Modelling gold as a Qing reserve/monetary metal on par with silver would be historically WRONG.

CONSEQUENCE for the Tier decision below: Tier A (a ~1:15 VALUATION anchor for reserves) is historically correct AS AN EXTERNAL TRADE-VALUATION relationship. The research's "soft ratio-band + mean-reversion" is the fuller Tier-B-ish mechanic — historically the most faithful (Gresham arbitrage) but it's the world-economy-scale coupling the user gated. And for CHI specifically, gold is barely a monetary metal at all, so the CHI-facing benefit of ANY gold:silver mechanic is small — the CHI money story is silver-vs-copper, out of #59's scope.

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

## WHY #59 IS SAFE TO BUILD WHILE #60 STAYS CLOSED — the ADDITIVE distinction (user, 2026-08-10)
"Modifying the existing cash vs reserves (i.e. what was previously proposed for Qing copper and silver circulation, #60) is far more dangerous because it is not purely additive."
- **#59 (gold↔silver reserve coupling) is ADDITIVE.** It ADDS a relationship between two quantities that already exist as independent floats. No existing quantity's SEMANTICS change; the pull is layered ON TOP. Reversible, boundable, and Tier A (valuation-anchor-only) is a clean always-safe floor.
- **#60 (the copper-M1 ↔ silver-reserve rework) is NOT additive.** It would have REDEFINED what the existing cash/reserve buckets MEAN and REROUTED flows between them (silver into circulation). Mutating the meaning of a live, load-bearing quantity is categorically more dangerous than adding a new coupling beside it — which is why #60 was correctly ruled out.
- **DESIGN CONSTRAINT this imposes on Tier B:** the #59 mechanic must be strictly ADDITIVE — it may add a new pull/anchor svalue + a bounded per-pulse nudge, but it must NOT change the semantics of, or reroute flows between, silver_reserve_size / the cash/M1 buckets / backing_type. The nudge acts on the two metals' MARKET prices/demand (new coupling), never on what the existing reserve or circulation quantities represent. If a proposed implementation step would mutate an existing bucket's meaning (as #60 would have), it is out of scope — fall back to the additive-only path or Tier A.
- **GLOBAL SCOPE raises the stakes on additive-only (user, 2026-08-10):** gold/silver reserves are a GLOBAL construct — every country has them, so this coupling applies GLOBALLY, not just to CHI. That is precisely WHY additive-only is doubly essential here: an additive pull's worst case is "mistuned," which is dialable-down or cleanly revertible everywhere at once; a semantics-mutating change (like #60) applied to EVERY country's reserves would be near-impossible to unwind and could break economies country-by-country in ways no single verify boot catches. So: (a) additive-only is non-negotiable given the global reach; (b) the verify boot MUST sample MULTIPLE countries (gold-standard Britain, bimetallic France, silver-standard CHI), not just CHI — a mechanic that stabilizes CHI but breaks a gold-standard power is a fail; (c) prefer building the safe Tier-A floor (valuation anchor, zero market pull) FIRST and adding the market nudge as a separate gated increment, so the global market-coupling risk is isolated and independently revertible.

## THE FULL RISK TAXONOMY (why #59 is buildable and #60 is not) — two axes, user 2026-08-10
The two tasks differ on BOTH axes, and #60 is the worst corner of both:
| | #59 gold↔silver | #60 copper↔silver / M1 |
|---|---|---|
| Additive vs semantics-mutating | ADDITIVE (adds a coupling beside existing floats) | SEMANTICS-MUTATING (redefines/reroutes existing buckets) |
| Global-uniform vs per-country fork | GLOBAL-UNIFORM (one coupling, every country has metal reserves, same rule for all) | PER-COUNTRY FORK of a global system (copper-vs-silver circulation is CHINA-SPECIFIC → reach into the SHARED global cash/reserve machinery and carve out CHI-only behaviour) |
| Worst case | mistuned pull → dial down / revert everywhere | mutated a load-bearing global system AND forked it per-country → near-unwindable, breaks economies country-by-country |
=> #59 is additive-and-uniform (buildable, boundable, revertible). #60 is the worst combination — "changing global systems specifically for Qing" — mutating shared global machinery to special-case one country. That combination, not scale alone, is why #60 is out and #59 is in. The #59 build must STAY in the safe corner: additive + globally-uniform. Any step that special-cases the coupling for CHI (a per-country fork) is a red flag pushing toward the #60 danger zone — reject it; keep the mechanic uniform across all countries.

## CLASSIFICATION (user, 2026-08-10): MISSING FEATURE, not a bug ([[bug-vs-missing-feature-rule]]).
"Coupling gold and silver reserves is a missing feature." So the independent gold/silver float is NOT Sobisonator doing something wrong (a bug to fix) — it is a feature that was never built (design + ADD). #59 is correctly feature-addition work: design → review → implement → verify, adding the coupling that never existed. This is not a regression to revert or a defect to patch; it's net-new mechanic, which is why it goes through the full design pipeline + gets the world-economy-scale caution, rather than the bug-fix path.

## USER DECISION (2026-08-10): TIER B — the Gresham soft-band. GREEN-LIT (mechanic), still gated on impl review + verify boot.
The user chose the historically-faithful Tier B (arbitrage mean-reversion toward the ~1:15 ratio), accepting the world-economy scale. This is the green-light for the MECHANIC; implementation still runs adversarial review → verify boot (high risk, touches every country's metal prices). Tier A is SUBSUMED (the valuation anchor is the band's centre).

## TIER B MECHANIC SPEC (the locked design)
Model gold↔silver as a soft-pegged pair that arbitrage pulls toward the era ratio, per the research (Gresham vs a fixed ratio; Friedman/Flandreau arbitrage-absorber):
1. **Anchor ratio R = 15** (gold:silver by weight; the pre-1873 converged value, correct for BOTH bookmarks). A single global constant (bullion is fungible worldwide — METAL_RESERVE_PRICING §II.3 option a; a per-country ratio risks backing circularity, rejected).
2. **Realized market ratio** = the two metals' current traded prices (gold_price / silver_price) — the mod already computes these independently. Let `r = gold_price / silver_price`.
3. **Mean-reversion pull (the arbitrage)**: each pulse, nudge the two metal prices TOWARD r = R by a small fraction (a partial correction, NOT a snap — arbitrage takes time + is frictional). When gold is under-valued vs silver (r < 15, the CHI silver-standard case: silver dear), the pull raises gold demand / lowers silver's relative price a touch, and vice-versa — exactly Gresham arbitrage (the cheap metal gets bought/shipped toward parity). Implement as a bounded per-pulse adjustment to the demand or price of each metal proportional to (R − r), clamped so one pulse can't overshoot (mirror the #23 damping discipline — no undamped feedback; the no-restoring-drift-ratchet rule: band-gate so it only pulls when |r − R| exceeds a deadband, else it ratchets on noise).
4. **BAND, not peg**: supply/demand can still push r away from 15 within a band (a big silver inflow CAN make silver dearer transiently — historically true); the pull only fights SUSTAINED divergence, so the silver-standard character (#46, silver dear in China) is PRESERVED as a within-band lean, not erased.
5. **CHI caveat honoured**: gold is not a Qing monetary metal (research/Kuroda), so the CHI-facing effect is deliberately small — this mechanic is the WORLD bullion market pulling the two metals together; it does NOT touch China's domestic silver:copper money (backing_type=silver_standard, se_CURRENCY.txt) or M1 (#60). The band centre also feeds reserve VALUATION (the old Tier A benefit, now the band's anchor).

## Interaction constraints (must not break) — CRITICAL for Tier B
- **#23 currency chain**: Tier B DOES touch the metal market prices that feed the gbip blend → the sqrt loop. This is the top risk. The per-pulse pull MUST be damped + deadbanded like the #23 fix (no undamped feedback, no ratchet-on-noise); the verify boot MUST confirm gbip stays flat with the band active. If the pull perturbs the sqrt loop, shrink the correction fraction / widen the deadband.
- **#42/#54 reserve display**: reserve valuation now reads the band anchor; confirm the change-indicator still reads right.
- **#46 silver-standard (WAI)**: PRESERVE — silver dear in China is a within-band lean, not erased. The band must be wide enough that the silver-standard character survives; only absurd sustained divergence is corrected.
- **#60 (accepted limitation)**: do NOT reopen M1/circulation. Tier B touches metal MARKET prices + reserve valuation, NOT M1.
- **GLOBAL (the user's hard rule)**: this changes every country's metal prices. The verify boot MUST check multiple countries on the #51 logs (gold/silver series already logged), not just CHI. A mechanic that stabilizes CHI but breaks a gold-standard Britain is a fail.

## Files (TIER B)
- common/script_values/CURRENCY_svalues.txt — the ratio constant R, the realized-ratio svalue (gold_price/silver_price), the reserve-valuation anchor (subsumes Tier A's intrinsic_price).
- common/scripted_effects/se_CURRENCY.txt (or the currency pulse) — the per-pulse bounded mean-reversion nudge to the two metals' demand/price, deadbanded + damped. THE core mechanic + the highest-risk code.
- NO M1/circulation changes. NO province/country blocks. NO domestic silver:copper touch.

## Verify (TIER B) — the boot must confirm ALL of these
- The realized gold:silver ratio trends toward ~15 over quarters (not a snap; a gradual pull), visible in the #51 gold/silver price series.
- Silver stays dear-ish in China (within-band lean preserved, #46 intact) — the pull did NOT erase the silver standard.
- #23 gbip FLAT with the band active (the pull is damped, no oscillation reintroduced) — the load-bearing check.
- Multiple countries' economies stable on the logs (not just CHI) — the global rule.
- #42/#54 reserve display correct; #60 M1 untouched.
IF any fail (esp. gbip destabilizes): shrink the correction fraction, widen the deadband, or fall back to Tier A (valuation-anchor-only) — which is always the safe floor.

## RISK/REWARD verdict (user, 2026-08-10) — why #59 is worth building and #60 is not
- **#60 = HIGH risk, LOW reward.** High risk: semantics-mutating + per-country fork of global machinery (the worst corner of the taxonomy above). Low reward: it only corrects a MODEST M1 drain the user already accepted as a tolerable in-game-abstraction cost. Not worth it → stays closed.
- **#59 = LOWER risk, HIGHER reward.** Lower risk: additive + globally-uniform (dialable, revertible; Tier-A floor). Higher reward: fixes a mechanic with NO historical analogue anywhere in the period (independent metal floats), and the fix applies GLOBALLY across every country — a broad correctness gain for one bounded uniform coupling.
=> The effort ordering is settled: BUILD #59 (through the safe Tier-A-first path + adversarial review + multi-country verify boot), LEAVE #60 closed. The bigger-sounding task (#59, "the bimetallic economy") is the SAFER, more rewarding one; the smaller-sounding one (#60, an M1 tweak) is the dangerous, low-payoff one — intuition inverted, per the risk/reward + additive/uniform axes.
