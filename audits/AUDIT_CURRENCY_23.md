# AUDIT — #23 currency period-2 oscillation (LIVE working doc)

**Purpose:** stop the circling. This doc records (a) what the LOGS MEASURE (fact, not theory),
(b) the GRAVEYARD of theories already disproven — with WHAT disproved each, so none is ever
re-proposed, and (c) the single open question. No fix is designed until a cause is proven AND
survives adversarial scrutiny. This is deep shared/upstream currency code; spillover cost is high.

## ACCEPTANCE CRITERIA (user, 2026-08-09) — the fix must produce PLAUSIBLE results, not just stop oscillating
The bug is NOT "fixed" merely when the period-2 oscillation stops. The corrected system must settle to
steady-state values that are HISTORICALLY PLAUSIBLE — cost of living AMONG them, but not limited to it.
Concretely, post-fix a `-debug_mode` boot must show:
- `CURRENCY_essentials_buying_power` (the Economy-tab "cost of living") settling to a stable value whose
  tael-equivalent is in the right ballpark vs the historical Qing peasant subsistence budget. YARDSTICK
  (landed — research/QING_COST_OF_LIVING_1763.md): bare-bones subsistence ≈ **~5 taels/adult/yr**
  (Allen et al. 2011, Beijing 182.6 g silver ÷ 37 = 4.9 tael) / **~15–22 taels/family/yr** (Beijing ~15.5
  vs Yangzi-Delta 22.59, a sourced regional spread); rice ≈ **1.0–1.5 taels/shih** (Wang Yeh-chien 1972);
  silver ≈ **700–1,000 wén/tael**. Compare the DERIVATION (Σ12 prices ÷ silver-backed peg, capped 32000)
  to that: numerator = a basket price, denominator = the currency peg; a steady-state cost of living orders
  of magnitude off ~5 tael/adult (a peasant "spending" hundreds of taels/yr, or a fraction of a tael) means
  the trade-price/peg SCALE is mis-calibrated — part of what #23 must correct, not just the oscillation.
- inflation/deflation % resting near 0 in a well-run economy (not pinned at a ±rail);
- private_cash_ratio near 1 (not 1.5 ⇄ 0.01);
- the other currency-chain outputs (ratio, need, circ, silver price) plausible and stable.
So the fix's design + its adversarial review must include a PLAUSIBILITY pass: re-measure the steady state
after the fix and check each output against history/sanity. The measured pre-fix numbers (§A) are readings
off the BROKEN oscillator (two rails of the bug) — they are BOUNDS, not the game's cost of living, and must
not be treated as a settled value (per the standing "don't conclude off the bug's rail" caution). A clean
steady-state reading only exists post-fix. Ties to #75 (inflation tuning) and #57 (deflation semantics).

Log source: `~/Downloads/logs.zip`, **Aug 8 22:11** (today), `-debug_mode` (2.26M IMP19C lines),
CURX forensic dump present (231,864 lines; 17 quarterly PRE/POST snapshots). Newer than any code.

---

## INPUTS-ARE-PLAUSIBLE COROLLARY (user, 2026-08-09) — the fault is in the MACHINERY, not the seeds
Logical constraint that narrows the diagnosis: the silver reserve is plausible, and M1 is plausible — so
if the machinery (the transformation from those inputs to the currency outputs) is CORRECT, it must produce
plausible outputs. It doesn't → the fault is in the MACHINERY, not the input seeds.
- CORROBORATED by the measured facts (§A): `circ` (≈M1) is FLAT + plausible across the flip; `silver_reserve_size`
  is FLAT ~62k + plausible. Both load-bearing inputs are steady and sane, yet essentials/ratio/need swing ~100×.
  So the oscillator is DOWNSTREAM in the transformation (trade-price → peg → cost-of-living), exactly where the
  traces localized it — NOT in the seeds.
- CONSEQUENCE for the fix: do NOT re-tune the seeds (the M1 46M/125M, the reserve size) — they are plausible.
  The correction belongs in the calculation chain.
- CONSEQUENCE for acceptance: "plausible cost of living" is not a separate goal bolted on — it is the TEST that
  the machinery is right. Correct machinery on plausible inputs ⇒ plausible outputs by construction. If the
  fixed machinery still yields an implausible cost of living from plausible M1 + reserve, it is NOT fixed.
- AND IF IT IS NOT PLAUSIBLE, IT MUST BE FIXED (user, 2026-08-09). Implausible output from plausible inputs is
  itself the defect — the scope of #23 is not merely "stop the period-2 oscillation" but "the machinery yields
  plausible outputs." A fix that damps the swing but leaves the cost of living (or any chain output) implausible
  is INCOMPLETE and does not close #23. This may mean correcting the transformation's SCALE/formula (the
  trade-price→peg→cost-of-living chain), not just its stability. Keep pursuing until the outputs are plausible.

## FRAMING (user, 2026-08-09) — the MODEL is sound; the bug is in the precise COMPUTATION
The existing currency machinery is conceptually sound AS AN ECONOMIC REPRESENTATION (money supply vs
silver-backed peg → cost-of-living → money-need → inflation/deflation is a reasonable model). The defect is
a BUG IN THE PRECISE COMPUTATIONS — a specific arithmetic/operand/order-of-operations error in the chain,
NOT a flaw in the conceptual design. So the fix is SURGICAL, not a redesign:
- Do NOT rework the economic representation or invent a new model — the concept stays.
- Do NOT re-tune the plausible seeds (M1, reserve — see corollary above).
- FIND the exact computation that turns flat, plausible inputs into a ~100× oscillating output: a mis-scaled
  divide/multiply, a unit mismatch, a sign/clamp error, a stale/wrong operand, an order-of-operations flaw in
  the trade-price → gbip → peg → essentials_buying_power → private_cash_needed chain. The period-2 signature +
  flat inputs point to a computation whose own output feeds back into its next input with a bad coefficient.
- This is consistent with everything measured: plausible flat inputs, sound concept, one transformation
  misbehaving. The producer-TZ probe is meant to expose WHICH computation (per-TZ local_price = order/stockpile,
  the sqrt, the /(0.5+pen), etc.) carries the fault. The fix corrects THAT computation so the sound model
  yields plausible, stable outputs.

## A. MEASURED FACTS (from the CURX ordered time series — not inferred)

The dump emits, per quarter, a PRE (last-quarter carried state) and POST (fresh recompute)
band-snapshot of the whole chain. Read in order, the system is a **phase-locked period-2 limit
cycle**: it flips between exactly two states every quarter, and next-tick PRE == this-tick POST
(state carries cleanly; no third state, no drift).

| var | STATE A ("inflation") | STATE B ("deflation floor") |
|---|---|---|
| `ratio` | ≥ 1.50 | 0.01–0.10 (−10% floor) |
| `circ` (amt_circulated_scaled) | 0–100k | 0–100k  **← FLAT** |
| `need` (private_cash_needed) | 0–100k | 0–100k (band coarse; algebra ⇒ it swings ~100×) |
| `ess` (essentials/cost-of-living) | 0–100 | 100–4000 |
| `gbip` (global_base_import_price_silver) | 0.5–1 | **0–0.01** |
| `wvuraw` (wealth_value_1_unit) | ≥ 1 | **0–0.01** |
| `wvuscaled` (…×reserve_ratio_impact) | 0.1–0.5 | 0–0.01 |
| `agsilver` (= **country_unit_price_silver**, NOT accum rate — corrected) | ≥ 1 | **0–0.01** |
| `pen` (market_penetration_silver) | 0–0.1 | **0.1–0.5**  ← ANTI-PHASE to gbip |
| `rratio` (reserve_ratio_total) | 0.1–0.5 | 0.1–0.5  **← FLAT** |
| `agreserve` (= **silver_reserve_size**) | ~60–62k | ≥ 62k  **← FLAT (stock stable)** |
| `agdemand` (= **DEMAND_country_silver**) | > 0 | > 0  **← never hits penetration-zero flip** |

**CURX label corrections (verified in se_ECON_LOG.txt:479-547):** `agsilver`=country_unit_price_silver,
`agreserve`=silver_reserve_size, `agdemand`=DEMAND_country_silver, `rratio`=CURRENCY_reserve_ratio_total.
Consistency check passes: country_unit_price = gbip.min(0.0001)/(0.5+pen). State A: 0.75/0.55≈1.4 (≥1 ✓);
State B: 0.005/0.6≈0.008 (0-0.01 ✓). So `agsilver` FOLLOWS gbip; gbip is the upstream mover, pen amplifies.

**Locked conclusions from the data (do not re-litigate):**
1. **Numerator is NOT the driver.** `circ` is flat across the flip. The ratio swings because its
   denominator `private_cash_needed` swings.
2. **The trade-price layer is what oscillates.** `gbip`, `wvuraw`, `wvuscaled`, `agsilver` all
   collapse ~50–100× in State B and recover in State A, in lockstep. `ess` (hence `need`) is the
   *downstream victim*: prices ÷ a near-zero peg → cost-of-living spikes → need spikes → ratio floors.
3. **`pen` is anti-phase to `gbip`.** When gbip collapses, market penetration rises, and vice-versa.
4. **Reserve SIZE is stable** (`agreserve` ~flat); the reserve ACCUMULATION RATE (`agsilver`) is what
   toggles on/off.

---

## B. GRAVEYARD — theories DISPROVEN (with the disproof). NEVER RE-PROPOSE THESE.

1. **"Unfloored `local_price = order_size/stockpile` divide is the root" (Claim B, orig #23).**
   ✗ REFUTED (adversarial review, this session): the divide is zero-GUARDED (`if stockpile>0`),
   sqrt-DAMPED downstream, and followed by a divisor floored at 0.5. Flooring it changes nothing.
   ALSO it's the deepest node of the same symptom chain — naming it "the cause" is relabeling.

2. **"essentials_buying_power slams the 32000 cap."**
   ✗ REFUTED by the log: `ess` peaks 1000–4000 in State B, never near 32000. The `max = 32000`
   never binds. Cap is OFF THE TABLE.

3. **"CURRENCY_reserve_ratio_impact parabola (`ratio×(5−ratio)`) is the ~5× amplifier."**
   ✗ REFUTED twice: (a) CHI can't reach that branch (needs `public_debt_administration` +
   reserve_ratio<1; CHI has neither → always takes `else`=÷3); (b) the log shows `rratio` FLAT
   (0.1–0.5) across the flip — it does not move, so it cannot be the oscillator.

4. **"#14: damp the correction amounts (`selloff_amt`/`money_demand_amt`)."**
   ✗ EXCLUDED by the log: those amounts move circulation/reserves; `circ` and `agreserve` are FLAT
   across the flip, and they do NOT feed `gbip_silver`. Damping them cannot touch the trade-price
   collapse that is the actual swing. (This was the standing "recommended" fix — the data kills it.)

5. **"Read-ordering / quarterly-reset zeroes the denominator term."**
   ✗ REFUTED earlier (DIAGNOSIS_CURRENCY_ANNUAL_SNAP §0): the reset zeroes `trade_*_due_*`, not
   `TRADE_national_expenditure`; no monthly consumer reads the denominator.

6. **"silver_accumulation_rate>0 gate closes the loop (price → next-quarter accumulation → demand → price)."**
   ✗ REFUTED (deep-trace, 2026-08-09): `silver_accumulation_rate` is written in the ENTIRE repo ONLY by
   the one-time seed `CURRENCY_country_setup_reserves` (se_CURRENCY.txt:2034-2055) and the manual ±1/±10
   player/AI GUI buttons (EE_scripted_guis.txt:164-237). `gbip_silver` / `country_unit_price_silver` /
   `pen` NEVER feed back into it. The demand→price edge is real (DEMAND_silver gated on accum_rate>0 →
   order_size → local_price), but the RETURN edge price→accum_rate DOES NOT EXIST. It is a one-way input,
   not a loop. This was the audit's OWN leading Section-C candidate — now dead.

**Meta-lesson (why I kept circling):** I repeatedly drilled DOWN the data-dependency chain
(ratio→need→ess→wvuraw→gbip→local_price) and presented each next node as "the cause." That only
relabels the symptom one level lower. A period-2 cycle's cause is a FEEDBACK LOOP with a one-quarter
lag and gain>1 — a loop, not a node. The open question must be posed as "what closes the loop," not
"which variable is lowest."

---

## C. THE OPEN QUESTION (the only thing left to prove)

**Why is the silver trade-price layer bistable with period 2?** Specifically, what feedback couples
`gbip_silver` (and `agsilver`, `pen`) such that a high-price quarter forces a near-zero-price quarter
and back, every quarter, phase-locked?

Candidate loop to TEST IN SOURCE (NOT yet proven — must be traced + adversarially refuted before it
graduates from hypothesis):
- Suspicion from the data: `agsilver` (accumulation rate) toggles on/off, and `pen` is anti-phase to
  `gbip`. If silver reserve DEMAND is gated on `agsilver>0`, and that demand feeds `order_size` →
  `local_price` → `gbip`, while `gbip`/valuation in turn decides next quarter's `agsilver`, that is a
  lagged on/off feedback = period-2. **Unverified.** Trace: what writes `silver_accumulation_rate`;
  what gates DEMAND_silver's reserve term on it; how `market_penetration_silver` is computed and why
  it's anti-phase; whether the loop gain is structurally ≥1 (bang-bang) rather than damped.

**Gate before any fix:** the loop must be pinned in source with the log values consistent at every
step, then handed to an adversarial reviewer instructed to REFUTE it. Only a hypothesis that survives
that becomes the diagnosis. Then — separately — a fix is designed and itself adversarially reviewed.

### C.1 STATE after deep-trace #1 (2026-08-09) — loop NOT yet closed; two live leads

The confirmed price chain (gbip → country_unit_price_silver → ratio) recomputes FRESH each quarter
inside `quarterly_global_trade_6` (oa_wealth_changes.txt:495-511, day 61), right before the apply pulse.
That is *when* the flip lands, but the RETURN EDGE that makes it a phase-locked period-2 cycle (vs. just
"recomputed fresh") is NOT yet found. Two structurally-plausible, EMPIRICALLY-UNCONFIRMED leads:

- **LEAD 1 — stockpile double-draw (LOW-MED confidence).** In one quarter the silver stockpile appears
  drained by `DEMAND_silver` TWICE: once as the trade-6 export (`GT_split_declare_sell_amount`,
  se_GLOBALTRADE_split.txt:752-819) and again in `CONSUME_from_stockpile` (se_CONSUME.txt:44-62,
  `subtract = DEMAND_$tradegood$`). If a governorship is a net silver exporter this could drive the
  physical stockpile toward 0 every other quarter → `local_price = order/stockpile` blows toward a rail.
  Structurally capable of period-2. UNPROVEN: no governorship/TZ-level `silver_stockpile` value is logged.

- **LEAD 2 — wealth/elasticity round-trip (UNCONFIRMED either way).** `DEMAND_elasticity_impact`
  (DEMAND_svalues.txt:11-33) → `DEMAND_silver` depends on `WEALTH_percentage_change_governorship`, which
  is price-coupled via the inflation-wealth-malus (se_CURRENCY.txt:2128-2155, fires when ratio>1 = State
  A). MAY cancel algebraically (malus hits numerator and denominator of the wealth-change). Not logged.

- **CRITICAL SCOPE CAVEAT:** `gbip_silver` is a WORLD AGGREGATE (sqrt of Σ over 23 trade zones). The CURX
  dump is CHI-ONLY, and CHI may not even be the dominant silver producer. So the current logs cannot pin
  *where* the oscillator physically lives. Any confirming probe must log governorship/TZ-level silver
  stockpile+order for the actual silver-producing zone(s), identified from setup/ map data — NOT CHI.

**Decision:** do NOT design a fix. The loop is not closed. Awaiting independent trace #2; if it also
fails to close the loop, the honest next step is a TARGETED probe (governorship/TZ silver stockpile+order
PRE/POST trade-6 for the real producer) — read-only — NOT a fix. No conclusion is drawn until a return
edge is pinned in source AND matched by logged values AND survives adversarial refutation.

### C.2 STATE after TWO independent deep-traces (2026-08-09) — CONVERGENT; loop still not closed

Two ~210k-token independent traces (one framed on the cobweb hypothesis, one told to disagree freely)
reached the SAME conclusions:

**Both confirmed (HIGH):**
- Chain verified with EXACT numbers (not bands): `country_unit_price_silver = gbip_silver.min(0.0001)/(0.5+pen)`.
  gbip=0.85,pen=0.081→1.463 ✓ ; gbip=0.004→0.0068 ✓. `circ` + `silver_reserve_size` flat every flip.
- **CHI PRODUCES ZERO SILVER** (setup/provinces/*.txt: silver = Andalusia, Austria/Saxony/Silesia,
  Peru/Chile, Mexico, Sweden, Portugal … no China province). CHI is a pure price-TAKER — the OBSERVER
  of the swing, NOT its source. `gbip_silver` is a WORLD aggregate (`se_GLOBALTRADE_split.txt:2659` =
  sqrt(Σ 22 TZ of local_price_TZ × TZ_%_of_global_stockpile)); each `local_price_TZ` =
  `(TZ_total_order_size / TZ_stockpile) × 0.6`, recomputed FRESH each quarter (`:5898-5923`), zero-guarded.

**Both KILLED (add to graveyard):**
- 7. **CHI-currency-ratio self-feedback.** Quantitatively refuted: gbip swings ~200× post-sqrt ⇒ the
  pre-sqrt weighted sum swings **~45,000×**. The only CHI price→demand channel (inflation wealth malus,
  se_CURRENCY.txt:2128-2155) is a ~0.5% effect at the measured ratios — ~200× too weak to be the driver.
- (LEAD 2 wealth/elasticity from C.1 is thus also effectively dead as the PRIMARY driver — too weak.)

**Both hit the SAME wall (the honest result):** the oscillator lives in the **producer-side TZ
order/stockpile dynamics** (the silver-producing zones), and the CURX dump is **CHI-scoped** — it cannot
see per-TZ `local_price_silver`, TZ stockpile, or TZ order size. The "cobweb in producer TZs" is the
LEADING HYPOTHESIS, explicitly **NOT PROVEN** — neither trace would promote it without producer-TZ data.
Trace-1's stockpile-double-draw (se_CONSUME.txt:44-62 vs GT export declaration) is a specific, testable
sub-lead within this.

**NEXT (decided): a minimal READ-ONLY probe.** The per-TZ silver aggregates are GLOBAL variables
(`global_var:<tz>_tradezone.var:local_price_silver`, `global_var:<tz>_stockpile_silver`,
`global_var:<tz>_total_order_size_silver`, `global_var:<tz>_percentage_of_global_stockpile_silver`), so
they are readable from CHI's existing dump WITHOUT iterating producer countries and WITHOUT touching any
currency logic. Extend the CURX dump to log these for the ~5 silver-producing TZs, PRE and POST of
`quarterly_global_trade_6`. That data will show whether a producer TZ's stockpile/order ratio does a
period-2 sawtooth (confirms cobweb) or not (kills it). Requires a boot on the user's machine. NO fix
until this pins the return edge AND it survives adversarial refutation.

**Refined facts (this pass, correct labels):** silver_reserve_size is FLAT and DEMAND_country_silver
is >0 in BOTH states — so the swing is NOT reserve-stock depletion and NOT demand hitting zero. The
mover is **gbip_silver itself** (the global base import price, se_GLOBALTRADE_split.txt:2659 =
sqrt(Σ over 23 TZ of local_price_silver × stockpile-share)), which halves-to-near-zero and recovers
every quarter. `country_unit_price_silver` and `pen` are downstream/coupled, not the source.

**Strong tell (not yet a proof):** DEMAND_svalues.txt:1315 carries a devs' comment on a REMOVED
multiplier — *"Removed because this causes major instability in prices."* The trade-price subsystem
is known-oscillatory. The shape (price ∝ 1/stockpile; next-quarter supply/demand react to this
quarter's price) is the classic **cobweb model** — with elasticity/gain ≥ 1 it produces exactly this
divergent period-2 cycle. HYPOTHESIS ONLY. Must trace: (1) what writes each TZ `local_price_silver`
and its stockpile each quarter; (2) whether the quarter-to-quarter response gain is structurally ≥1;
(3) why it pins to the two RAILS (near-0 / high) rather than a decaying oscillation — a bang-bang gate
somewhere. Do NOT design until this loop is pinned in source AND survives adversarial refutation.

---

## D. Evidence pointers
- Log: `~/Downloads/logs.zip` (Aug 8 22:11) → `logs/debug.log`, grep `CURX`.
- `common/script_values/CURRENCY_svalues.txt` — ratio L753, need L719, ess L673, wvuraw L234,
  reserve_ratio_impact L376 (dead end #3), gbip_silver read L1091.
- `common/scripted_effects/se_GLOBALTRADE_split.txt` — gbip write L2659 (=sqrt(Σ TZ price×share)),
  per-TZ contributor L2500+, country_unit_price=gbip/(0.5+pen) L2717.
- `common/script_values/DEMAND_svalues.txt` — silver reserve demand (the `agsilver>0` gate suspicion).
- `common/scripted_effects/se_ECON_LOG.txt` — CURX dump emitter (~L700+).
