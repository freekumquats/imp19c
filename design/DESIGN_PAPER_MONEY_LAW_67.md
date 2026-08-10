# DESIGN — Paper-money law regime (#67)

**Status:** design, 2026-08-10. Rests on: DIAGNOSIS_MINTING_MACHINERY_67.md (Stage-0, committed) + RESEARCH_QING_PAPER_MONEY_67.md. Awaiting adversarial review before implement.

SOURCING CAVEAT (carried from the research, not hidden): the digest is Wikipedia-mediated (primary monographs — von Glahn, King, Peng — were inaccessible). The load-bearing numbers (backing ratio 80/20→50/50, the ~3-5%-of-face-in-8-years collapse) rest on single citation chains (Yang Duanliu 1962, via Wikipedia). They are used as SHAPE (a generous starting backing that erodes to a floor, then a non-linear collapse), not as precise balance constants — every one is a best-guess in the ASSUMPTIONS section, tuned on the boot.

## What the research fixes (design anchors)
1. **1763 = NO government paper.** Real gap 1661 (Shunzhi withdrawal) → 1853 (Xianfeng reintroduction); Jiaqing explicitly rejected it in 1814. So the regime is UNAVAILABLE at the 1763 start and unlocks only on FISCAL CRISIS (war-finance under treasury stress), NOT on a date/tech timer.
2. **The failure mode is a confidence cliff + doom-loop, not linear inflation.** Notes held value while backed; once the convertibility promise broke, they fell to ~3-5% of face within ~8 years, and depreciation ACCELERATED printing (denominations 500→100,000 wén in 6 years). Terminal state = forced abolition, not worthless limbo.
3. **Do NOT share a trust meter with private notes** (qianzhuang/piaohao) — out of scope here; a state fiat regime is its own mechanic.

## The lever — CORRECTED after adversarial review (DO-NOT-IMPLEMENT verdict on v1)

**v1 was inert — a fatal misread of the #63 machinery, caught by review.** v1 claimed `qing_monetary_bias=+12` → `qing_mint_ceiling = 1.45×cap` → more minting. FALSE against source: the #63 mint-ceiling block (se_QING_DECLINE.txt) is guarded `bias < 0` and only clamps the rate DOWN (sound-money discipline); it never runs for positive bias and never RAISES minting. And `CURRENCY_mint_currency` (se_CURRENCY.txt:1381) clamps the rate to the RAW `CURRENCY_minting_rate_cap` monthly — NO code path lets CHI mint above that raw cap (the #63 comments say so verbatim: "loose minting cannot exceed the shared cap"). So a +12 bias would mint NOTHING extra and add only stress — pure downside, a dead lever. Rejected.

### The REAL lever (review option (a)): add a CHI-gated, BOUNDED paper term to the cap's BOUNDED branch
`CURRENCY_minting_rate_cap` (CURRENCY_svalues.txt:835-844) is the actual monthly upper bound, and its bounded (paper-money-NOT-legal) branch is ADDITIVE: `reserve_change + 1%-circulation + trade_wealth + sisters`. The paper regime adds ONE more CHI-gated additive term to THAT branch — a finite paper allowance — so the cap genuinely rises and the player's mint slider can use the headroom. Stays on the bounded branch (never the 99999 else); `paper_money_allowed` stays FALSE. CHI-gated so it is 0 for every other country and 0 for CHI when the regime is off (the #63 "keep it on the Qing side of the fence" approach; the shared-svalue R2 caution is respected because the added term is tag=CHI + regime-gated).

The paper allowance term (in the bounded branch):
```
if = { limit = { tag = CHI  has_variable = qing_paper_regime_active }
       add = qing_paper_mint_allowance_svalue }   # finite: a bounded % of circulation, SHRUNK by depreciation
```
`qing_paper_mint_allowance_svalue` = `base_paper_allowance × (1 − qing_paper_depreciation/100)` — starts as real headroom (deficit-finance upside), and as depreciation climbs the allowance SHRINKS toward 0 (the doom-loop: the more you debase, the less the paper buys, per the research). Bounded by construction, never 99999.

**base_paper_allowance references the SILVER RESERVE, not live circulation (review-2 MED-2b fix).** v2-first-cut based it on % of circulation — but the cap recomputes monthly while depreciation only pulses quarterly, so a %-of-circulation term compounds (mint → more circulation → bigger term → more mint) ~4× the existing 1% term for up to a quarter before the brake catches up. REJECTED. Instead `base_paper_allowance = paper_pct × var:silver_reserve_size` (a STABLE reference the act of minting does NOT inflate — it removes the self-reference entirely, review option (a)), PLUS an absolute `min`/cap so it can never exceed a hard ceiling regardless. The regime is thus "you may print against your silver reserve, and the more you over-print the less it's worth" — historically apt (the 80/20→50/50 backing ratio IS a reserve ratio) and structurally non-compounding.

### Layer 1 — a new law option `paper_currency` in monetary_policy_setting (00_monetary_policy_setting.txt)
- A 6th option in the #63 law group (standard/currency_recall/limited/more/bonds/**paper_currency**).
- **Availability gate (corrected): per-option `allow = { has_variable = qing_paper_money_unlocked }`** — Imperator law OPTIONS do NOT support a per-option `potential` (review-confirmed against the mod + oracles; only group-level potential exists). `allow` is the proven per-option gate (00_qing_statutes_laws.txt precedent: qing_penal_revised/qing_opium_legalize gate one option while siblings stay open). CAVEAT: `allow` GREYS OUT the option (locked + tooltip), it does not HIDE it. If strict invisibility at 1763 is required, use a SEPARATE law group whose GROUP potential is the unlock gate instead. DECISION: greyed-out-until-unlocked is acceptable + simpler (the tooltip explains the crisis prerequisite) — go with `allow`; log the alternative.
- `on_enact`: `set_variable = qing_paper_regime_active = 1` (drives the allowance term + the depreciation pulse) + `set_variable = qing_monetary_bias = 8` (feeds the EXISTING stress term — paper adds monetary stress, same as issue_bonds; NOT relied on for the mint lever, which is the allowance term above). modifier: a modest commerce/deficit-finance boon (issue_bonds shape) — the visible upside.
- **Reversion:** enacting ANY of the 5 sibling options must clear `qing_paper_regime_active` (set 0 / remove) in their on_enact — the review caught that today they only set qing_monetary_bias, so without this the depreciation pulse keeps running after leaving the regime. Add the clear to ALL five.
- **Reversion-reset semantics (review-2 LOW-3, DECIDED):** voluntary reversion clears `qing_paper_regime_active` (freezes the depreciation pulse) but does NOT reset `qing_paper_depreciation` — it DECAYS back toward 0 over time (a slow recovery term in the pulse, active whether or not the regime is on, so trust rebuilds gradually). This models real scarring: re-entering the regime while trust is still damaged starts with a pre-shrunk allowance. `qing_paper_money_unlocked` stays set once earned (the crisis happened; the OPTION remains available), but the abolition end-state (Layer 3) sets a re-lock cooldown. So: leave-and-return = scarred-but-usable; abolition = locked-out for the cooldown.
- **Stress stacking (review-2 LOW-3, CONFIRMED intended):** the regime contributes qing_monetary_bias +8 (the standard over-mint stress, same as issue_bonds) PLUS the depreciation term (capped ≤+15) → up to ~+23 to qing_currency_stress, clamped 0..100. Intended: paper money is MORE stressful than bonds (the +8 base) AND worsens as it depreciates (the ≤+15). The clamp keeps it from pegging alone; the two together can approach the top band under heavy abuse, which is correct (that's the crisis).

### Layer 2 — the depreciation doom-loop (se_QING_DECLINE.txt, in the existing stress pulse)
The load-bearing part — the confidence cliff. A DEDICATED `qing_paper_depreciation` meter (0..100), pulsed only while `qing_paper_regime_active`:
- Rises each pulse by an amount that GROWS with real over-issue. **The concrete over-issue signal (review-2 MED, must be wired — an unwired signal = a functional-but-UNBRAKED lever):** in the pulse, compute how far the actual minted rate sits ABOVE the non-paper baseline cap — `over_issue = CURRENCY_minting_rate − (CURRENCY_minting_rate_cap − qing_paper_mint_allowance_svalue)` (i.e. how much of the paper headroom the player actually used), clamped ≥0. Feed `over_issue` (relative to the reserve, so it's a ratio) into the depreciation rise. While paper minting stays modest, depreciation barely moves (notes hold); as the player leans on the allowance, depreciation rises NON-LINEARLY (accelerating), per the research's "value stays ~1 then falls sharply past threshold." If over_issue is ~0 (regime enacted but barely used) depreciation does NOT climb — notes hold their value, historically apt.
- Feeds back TWO ways (the doom-loop): (a) it SHRINKS the mint allowance itself (`allowance = base × (1 − depreciation/100)`, Layer-1 lever) — so the deeper the debasement, the less headroom the paper buys, forcing the player to either pull back or print into ever-less-valuable notes; (b) a MODEST, BOUNDED contribution to `qing_currency_stress` — **NOT a big additive term** (review MED: the stress meter is clamped 0..100 and consumed widely — reform pressure, ethnic tension ≥70, treaty-system ≥40 — so a large paper term would peg it at 100 and swamp the opium/reserve signals). Cap the paper contribution to a small band (e.g. ≤ +15) so it colours the meter without drowning its other terms. The PRIMARY feedback is the allowance-shrink (its own meter), NOT the shared stress meter.
- Backing ratio: starts generous (~0.8, the Hubu 80/20) and pressure pushes it toward a 0.5 floor (the historical 50/50); past the floor the cliff steepens. ASSUMPTION-flagged constants.

### Layer 3 — terminal abolition (a real end-state, not limbo)
When `qing_paper_depreciation` sits above a high floor (e.g. >90) for N consecutive pulses, fire `qing_paper_abolition` event: forcibly revert the law to `standard_minting` (bias 0), clear the regime, apply a one-time legitimacy/stability hit (the 1861-68 collapse), and a cooldown before it can be re-unlocked. Mirrors the historical 1859 (tax-refusal) → 1861 (circulation end) → 1868 (formal abolition) sequence.

### Layer 0 — the crisis unlock (the gate)
A `qing_paper_crisis` event that sets `qing_paper_money_unlocked` when the Qing is in acute fiscal stress: gate on the existing `qing_currency_stress` in its top band AND a treasury/silver-reserve depletion threshold (the research's "desperate band," analogous to the pre-1853 drain) AND a late date (the Taiping-era window, ≥~1850, so it can't fire in a quiet High-Qing). Offers the regime as the desperate option it historically was.

## Files
- common/laws/00_monetary_policy_setting.txt (BOM+CRLF) — the `paper_currency` option.
- common/scripted_effects/se_QING_DECLINE.txt (BOM? verify — it's a scripted_effects file, check its own convention) — the depreciation meter + doom-loop + the abolition-trigger poll, in the existing stress pulse.
- events/imp19c_mod_events/ (no-BOM/LF) — qing_paper_crisis (unlock) + qing_paper_abolition (terminal) events.
- localization/english/ (BOM) — law option + events loc.
- All new levers ship with -debug_mode se_LOG bands (depreciation, effective mint ceiling, stress contribution) so the boot shows the doom-loop; STATIC labels, no macro/# in LOG.

## ASSUMPTIONS / GUESSES (→ overnight ASSUMPTIONS section) — all best-guess, tune on boot
- `base_paper_allowance = paper_pct × var:silver_reserve_size` + an absolute `min`/hard-cap. GUESS: paper_pct ~0.2-0.5 (print up to ~20-50% of the silver reserve as paper headroom) + a hard ceiling. References the RESERVE not circulation (review-2 MED-2b) so it does NOT compound with minting. Genuinely raises the cap (unlike v1's inert ceiling), finite, non-self-referential. Tune vs deficit-finance wanted; boot-verify the effective cap rises but M1 growth stays bounded (#60) with NO monthly compounding.
- paper_currency `qing_monetary_bias = +8` — feeds the EXISTING stress term only (same as issue_bonds); the mint lever is the allowance term, NOT the bias. (v1's +12→1.45×-ceiling claim was INERT — corrected.)
- backing ratio start 0.8, floor 0.5 (Hubu 80/20→50/50, single-chain-sourced — SHAPE not gospel).
- depreciation cliff curve (near-flat under light use, accelerating with over-issue; ~reaches high band a few years past heavy over-issue, per the ~8yr-to-3-5%-of-face outcome) — per-pulse rise + non-linear exponent are guesses; the depreciation band + the allowance-shrink confirm the shape on the boot.
- paper contribution to qing_currency_stress capped ≤ +15 (bounded, doesn't swamp the shared meter — review MED). Guessed cap.
- abolition trigger: depreciation >90 for N pulses (N ~4 quarters). Legitimacy/stability hit magnitude guessed.
- crisis-unlock gate: stress top-band + reserve-depletion threshold + date ≥1850. Thresholds guessed off the existing meters.

## VERIFY (boot)
- Regime UNAVAILABLE at 1763 (option hidden until qing_paper_crisis fires). 
- On enact: mint ceiling rises to ~1.45× (bounded, NOT 99999); paper_money_allowed stays false; #23 gbip + #60 M1 NOT destabilized by an uncap (the whole point).
- Depreciation doom-loop visible on the log: sustained over-issue → accelerating depreciation → rising currency_stress → (player pulls back OR) terminal abolition fires.
- Reversion to specie works (enact another option → bias/regime cleared).

## Rejected alternatives (logged)
- Raw `paper_money_allowed=true` flag flip → the 99999 uncap → runaway M1 → re-breaks #23/#60. REJECTED (Stage-0).
- A brand-new parallel mint system → duplicates #63's ceiling machinery. REJECTED (reuse #63).
- Date/tech-only unlock → ahistorical (it was crisis-driven, not steady growth). REJECTED (crisis-gated).
- Sharing a trust meter with private qianzhuang/piaohao notes → misrepresents history (private notes outperformed state fiat). REJECTED (separate mechanic, out of scope).
