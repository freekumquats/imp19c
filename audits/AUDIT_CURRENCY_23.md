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

### C.3 STATE after the Aug 9 producer-TZ probe (2026-08-09 pm) — LOOP CLOSED IN SOURCE, pending adversarial refutation

The producer-TZ probe the audit called for WAS built (se_ECON_LOG_TZPROBE.txt, tag `IMP19C TZP`) and its
output IS in the Aug 9 04:22 log (1,675,657 lines). Read in full via tools/curx_analyze.py (streams the
whole 1.48 GB debug.log). This is the data C.2 was blocked waiting on. Findings:

**Exact CHI chain (CURXV tick layer, 27 snapshots) — CHI is a VERIFIED PASSTHROUGH, exonerated:**
- `agsilver = gbip/(0.5+pen)`: q0 0.838/0.5755=1.456 ✓; q1 0.0025/0.6325=0.004 ✓ (exact).
- `ess` swing (8→2664) is ENTIRELY `wvuscaled` collapsing (0.385→0.001); the Σ12-price numerator is
  ~stable (~2.7–3.1). Cost-of-living is a downstream victim of the peg, confirmed with exact numbers.
- `ratio = circ×0.004/need` ✓. `circ` flat (125→117 slow monotone decline over 13q). NOT the driver.
- So NOTHING in CURRENCY_svalues.txt is the oscillator. It faithfully transmits `gbip`.

**gbip is the mover, and its algebra is now pinned (log ⟷ code exact):**
- `gbip² = Σ_TZ (local_price_TZ × share_TZ)` (se_GLOBALTRADE_split.txt:2659), `share_TZ =
  stock_TZ / global_stock` (:1458-1470), `local_price_TZ = (order_TZ/stock_TZ)×0.6` for stock>0 (:5898-5908).
- Substituting: **`gbip² = 0.6 × Σ_{stocked TZ}(order_TZ) / global_stock_silver`**. The stock_TZ cancels in
  price×share; a zone at stock=0 has share=0 and DROPS OUT of the sum (correction to any "stock-0 price
  spike drives gbip" idea — it does the opposite, it removes that zone's contribution).
- Log confirms the 1/global_stock relation: gbip collapses to 0-0.01 EXACTLY in the quarters global silver
  stock spikes to 1000-10000 (q11, q19, q25), and is 0.1-1 when global stock is 100-1000. Anti-correlated.

**The loop (each edge pinned in source):**
1. RESET: every quarter all `<tz>_stockpile_silver` and `<tz>_total_order_size_silver` globals are reset to
   0 (:152-248, :431+) and rebuilt from scratch.
2. REBUILD stock: `<tz>_stockpile += for_sale_silver` per selling governorship (:1020-1027), where
   `for_sale = governorship_stockpile − DEMAND_silver`, capped at infra (:752-804).
3. DEMAND→price return edge: `DEMAND_silver` (:1339) `multiply = DEMAND_elasticity_impact`
   (DEMAND_svalues.txt:11-33), which reads `WEALTH_percentage_change_governorship` — price-coupled. The devs
   REMOVED a second price multiplier here (`DEMAND_shortage_silver_inverse`, :1315) with the comment
   *"Removed because this causes major instability in prices"* — confirming this subsystem is known-oscillatory.
4. price recomputed FRESH from the rebuilt stock/order (:5898), gbip re-aggregated (:2659), sqrt-damped.

**DIAGNOSIS (hypothesis, pre-adversarial-review):** the silver trade-price layer is a **cobweb model**
`price ∝ Σorder/global_stock` whose supply (`for_sale`) and demand (`DEMAND_silver` via elasticity) react to
the PRIOR quarter's price/wealth with a one-quarter lag and loop gain ≥ 1, producing the phase-locked
period-2 limit cycle. The reset-to-0-and-rebuild each quarter (no smoothing/inertia on stock or price) is
what makes the gain undamped: nothing carries a fraction of last quarter's state forward, so the full
correction lands every quarter → bang-bang. This is a PRECISE-COMPUTATION defect (missing damping/inertia in
the order/stock→price recompute), consistent with the user's "model sound, computation buggy" framing —
NOT a redesign. STILL TO PROVE under adversarial review: that the loop gain is structurally ≥1 (vs the
elasticity coupling being too weak, as the CHI-side version was — C.2 killed CHI self-feedback at ~0.5%);
i.e. WHICH term supplies the ≥1 gain (the reset artifact, the /global_stock aggregation, or the elasticity).

### C.4 ADVERSARIAL REVIEW of §C.3 (cycle 1, 2026-08-09) — VERDICT: PARTIALLY. Cobweb-elasticity mechanism REFUTED; double-subtraction lead resurrected.

An independent reviewer (told to REFUTE) re-ran tools/curx_analyze.py on the same Aug 9 log and read every
cited file:line. Result: the LOCALIZATION survives, the specific MECHANISM does not.

**Survives (confirmed):**
- Code line-refs + algebra correct (minor: for_sale block runs to :819 incl. the CU-scope add, not :804;
  sqrt at :2697-2708). `gbip² = 0.6·Σ(order_TZ)/global_stock` shape confirmed (stock cancels in price×share).
- CHI-side exoneration stands (exact ticks: agsilver=gbip/(0.5+pen), ess swing = wvuscaled collapse).
- Not-CHI / not-any-graveyard-theory localization to producer/consumer-TZ dynamics stands.

**REFUTED in §C.3 (three errors — do not repeat):**
1. **"gbip collapses ⟺ global stock spikes to 1000-10000 (q11/19/25)" is only 3 of 8 collapse quarters.**
   The other 5 State-B quarters (idx 1,5,7,15,21) have global stock in the SAME 100-1000 band as healthy
   quarters. So in the majority of collapses the mover is the NUMERATOR (Σ order_TZ), not the denominator.
   My "global_stock is the mover" framing is empirically wrong for most quarters.
2. **It is NOT clean period-2.** Real POST sequence (from CURXV exact ticks): B,A,B,B,A,B,A,B,A,B,B,A,B —
   TWO runs of consecutive State-B quarters (idx 5&7, idx 19&21). §A's "flips every quarter, no third
   state" is overstated. Irregular runs argue for a THRESHOLD/STOCKOUT event (something crossing zero and
   staying near zero a variable number of quarters until refilled), NOT a smooth fixed-lag oscillator.
3. **Loop gain does not close via elasticity.** gbip swings ~280× (pre-sqrt Σ swings ~78,000×);
   DEMAND_elasticity_impact is clamped max=1/min=0.1 = a 10× ceiling. Elasticity CANNOT supply 4+ orders of
   magnitude — the exact fatal weakness that killed CHI self-feedback in C.2. §C.3 ended on an open question,
   not a proof of ≥1 gain. So the cobweb-VIA-ELASTICITY story is quantitatively dead as the primary driver.

**Resurrected (the better-fitting, still-UNTESTED lead — this is LEAD 1 from §C.1, shelved prematurely):**
**DEMAND double-subtraction at governorship scope.** A seller's `for_sale = stockpile − DEMAND`
(se_GLOBALTRADE_split.txt:772-781) already nets demand out before export. That same `for_sale`/export is
subtracted from the stockpile again on export application (:3656-3688, esp. :3680-3686), and THEN
`CONSUME_from_stockpile` (se_CONSUME.txt:44-58) subtracts `DEMAND_$tradegood$` a SECOND time from the same
governorship stockpile at end-of-quarter (oa_wealth_changes.txt:335-344). A thin-margin producer
(stockpile only modestly > DEMAND) is drained toward zero/negative every quarter it exports → next quarter
`for_sale=0` (guard :772 needs stockpile>DEMAND) → its contribution drops out of the TZ aggregate → TZ stock
crashes to floor → `local_price=order/stock` spikes → no export that quarter means no second drain →
production refills it above DEMAND → export resumes → stock recovers → price craters. A discrete
"did any seller have surplus this quarter" flip.

Why it fits the log BETTER than the cobweb: OSCILLATION SUMMARY shows the toggling TZs drive stock all the
way to band `0` (baltic, east_mediterranean, east_europe, indo_china, west_africa, india), while big
well-buffered producers (central_europe, west_south_america, atlantic_seaboard) NEVER hit 0 and stay flat —
exactly a thin-margin-stockout signature, not a smooth elasticity rail. Also explains the two-in-a-row
State-B runs, and why non-producing TZs still toggle (imports via :3690-3706 let a net-importer re-export,
spreading churn beyond true producers — undermining the "only producer TZs matter" premise).

**DECISION (cycle 1 close):** §C.3 does NOT graduate to "the diagnosis." Do NOT design a fix on the
elasticity mechanism. NEXT: trace the double-subtraction lead in source (the three subtraction sites above)
and confirm/refute with a per-GOVERNORSHIP (not per-TZ) silver-stockpile probe at 3 points in one quarter
(post-produce / post-export / post-consume) for a real silver producer feeding a toggling TZ (e.g. a Swedish
province → baltic). If (post-export)→(post-consume) shows a second ~DEMAND_silver subtraction stacked on the
export that already netted DEMAND, the double-draw is pinned. This lead was UNPROVEN in §C.1 and must itself
survive adversarial refutation before it becomes the diagnosis. Cobweb-elasticity → GRAVEYARD (theory 8).

### C.5 DIAGNOSIS cycle 2 (2026-08-09) — DOUBLE-SUBTRACTION traced + closed-form; LEADING diagnosis, pending its own adversarial review

Traced the resurrected double-subtraction lead directly in source. CONFIRMED: `DEMAND_$tradegood$` is
subtracted from a governorship's `$tradegood$_stockpile` TWICE per quarter:

1. **Reserved out of sellable surplus:** `for_sale_$tradegood$ = stockpile − DEMAND_$tradegood$`
   (se_GLOBALTRADE_split.txt:775-781; guard :772 requires stockpile > DEMAND).
2. **Export application:** `stockpile −= amount_exported`, where `amount_exported = for_sale`
   (se_GLOBALTRADE_split.txt:3663-3685). [imports then add order_size, :3701-3703]
3. **Consume, end of quarter:** `stockpile −= DEMAND_$tradegood$` AGAIN
   (se_CONSUME.txt:54-57, called from CONSUME_all_stockpiles at oa_wealth_changes.txt:340).

**Per-quarter operation order** (quarterly_apply_trade_changes_and_consume, oa_wealth_changes.txt:335-343):
produce → for_sale/export/import (the GT_split passes, earlier in quarter) → CONSUME_all_stockpiles.

**CLOSED FORM for a net-exporter governorship (stock S, demand D, S>D), ignoring imports:**
- after export: `S − for_sale = S − (S−D) = D`
- after consume: `D − D = 0`
⇒ **an exporting governorship's silver stockpile is driven to exactly 0 every quarter it exports.**
Next quarter the for_sale guard (stock > D, :772) FAILS → it exports nothing → that governorship's stock
drops OUT of its TZ `Σstock` aggregate → the TZ stockpile term craters toward its floor → `local_price =
order/stock` (:5901-5906) spikes → gbip climbs. The following quarter, with no export there is no second
drain, production refills stock above D, export resumes, TZ stock recovers, price craters. This is the
period-2 engine (with the stockout-RUN irregularity the review noted: a producer can sit at 0 for >1
quarter if production is slow to lift it back above D). Thin-margin producers hit 0; well-buffered ones
(central_europe, west_south_america, atlantic_seaboard) stay above D every quarter → FLAT — exactly the log's
OSCILLATION SUMMARY split. And the double-drain can push a low-margin gov NEGATIVE, consistent with the
"Failed to fetch / Invalid comparison" econ-var noise classes.

**Why this beats the cobweb-elasticity story (C.3/graveyard #8):** it needs NO ≥1 elasticity gain (the
quantitative wall). The gain is structural bang-bang from a boolean guard (exported? → stock=0 → guard fails
→ no export), not a smooth elastic response. It predicts the zero-touching toggles, the flat big producers,
and the irregular multi-quarter B-runs — all three of which the cobweb story failed.

**STATUS: leading diagnosis, NOT yet graduated.** Must survive its OWN adversarial review before any fix
design. Open questions for that review: (a) is DEMAND_silver actually >0 for the toggling producer govs
(if DEMAND≈0 the double-subtract of ~0 is harmless and this is refuted)? (b) do imports (:3701) refill
enough to blunt the drain, changing the period? (c) is the "subtract DEMAND in for_sale" AND "subtract DEMAND
in consume" genuinely double-counting the same physical consumption, or are they two DIFFERENT sinks
(export-reserve vs domestic-consumption) that are both legitimate? — this is the crux: if for_sale's
`−DEMAND` is meant as "hold back D for domestic use" and consume's `−D` is "domestic use actually happens,"
then subtracting in for_sale is the BUG (it reserves D, but the reservation is never returned to stock — it
just vanishes because consume takes ANOTHER D). The fix hinges on which subtraction is the phantom.

### C.6 ADVERSARIAL REVIEW of §C.5 (cycle 2, 2026-08-09) — VERDICT: REFUTED. Double-subtraction is an accounting identity, not a bug. Two sharper leads + the central paradox.

Independent reviewer traced every `$tradegood$_stockpile` mutation in one quarter, in execution order:
1. `GT_split_declare_sell_amount` (:775-781): `for_sale = stockpile − DEMAND` writes to **for_sale_ (a local
   var)**, NOT to the stockpile. Stockpile UNTOUCHED here. (grep confirms for_sale is never assigned back to
   stockpile.) — this is the load-bearing correction: nothing is "reserved out of stock" that could "vanish."
2. Export (:3663-3685): `stockpile −= amount_exported`, amount_exported = for_sale = (S−D). Removes the SURPLUS.
3. Consume (se_CONSUME.txt:54-57): `stockpile −= DEMAND`. Removes D.
Total removed = (S−D) + D = **S, the whole production, removed exactly once.** DEMAND appears in two FORMULAS
but is subtracted from the stockpile VARIABLE only once (step 3); step 2 removes D's complement. §C.5's
"subtracted twice / reservation vanishes" is factually wrong. The S→D→0 arithmetic is right but the causal
label was wrong: it's the identity export + domestic-use = production. Removing either subtraction would BREAK
correctness (remove for_sale's −D ⇒ export whole stock then consume drives negative; remove consume's −D ⇒
domestic use never happens). NEITHER site is a phantom. → DOUBLE-SUBTRACTION to GRAVEYARD (theory 9).

Supporting: consume runs once/quarter strictly after export (oa_wealth_changes.txt:335-343) ✓; imports do NOT
refill an exporter same-quarter (order_size>0 only when stock<DEMAND, mutually exclusive with the stock>DEMAND
export branch; :2095-2124) ✓.

**THE CENTRAL PARADOX (now the thing to explain):** in the Aug 9 log the real silver-producer TZs
(central_europe=Austria/Saxony/Silesia, west_south_america=Peru/Chile, atlantic_seaboard=Portugal,
west_mediterranean=Andalusia) are the FLATTEST series — stock pinned in one band all 13 quarters, never 0.
Only baltic (Sweden) toggles among producers; the other zero-touching zones (india, indo_china, east_europe,
etc.) produce NO silver. **Yet gbip swings ~280× every quarter.** If gbip² = 0.6·Σ(order_TZ)/global_stock and
the producers' price & stock are flat, WHAT supplies the swing? Candidates to chase next:
- The `global_stock` DENOMINATOR rescaling ALL shares (even flat producers') when non-producer zones toggle.
- A single high-weight zone (or the sqrt guard at :2697 behaving oddly when the summed base = 0/unset).
- A SET-BUT-EMPTY per-TZ operand (local_price or share) entering the Σ every other quarter (the classic
  imp19c read-before-set / reset-before-rebuild hazard) → sum collapses → gbip craters.

**Two sharper structural leads the reviewer raised (both real, both need checking):**
- LEAD A — `DEMAND_silver` is a live svalue re-evaluated UNCACHED at two times: declare-pass (:773/779, early
  quarter) and consume-pass (se_CONSUME.txt:56, end quarter, after wealth/price updates). If it moves between
  them, the S→0 identity breaks → over/under-drain. (elasticity-coupled via WEALTH_percentage_change.)
- LEAD B — the boolean guard `stockpile > DEMAND` (:772) makes a governorship's export contribution BINARY
  (all S−D, or exactly 0) rather than a smooth ramp as production approaches demand → a real bang-bang source
  for the zero-touching toggles this audit keeps seeing.

**DECISION (cycle 2 close):** §C.5 does NOT graduate. NEXT (cycle 3): resolve the CENTRAL PARADOX first —
compute per-TZ price×share (=gbip contributors) from the EXISTING log (analyzer already captures pct) to see
which zone(s) actually move gbip, and check the sqrt/empty-operand behavior at :2659-2708. That tells us
whether to chase Lead A, Lead B, the denominator, or the empty-operand. No fix design until the mover is pinned.

### C.7 DIAGNOSIS cycle 3 (2026-08-09) — BREAKTHROUGH: inputs CANNOT produce the output ⇒ gbip is a STALE/ORDERING read, not a magnitude swing.

Extended tools/curx_analyze.py to reconstruct gbip from its OWN inputs, per quarter (POST). Two facts kill the
"aggregate magnitude swings" family of hypotheses:

1. **Per-zone stock CANCELS in gbip.** gbip² = Σ(local_price_TZ × share_TZ), local_price = order/stock,
   share = stock/global_stock ⇒ price×share = order/global_stock. Individual producer stock/price moves
   cannot drive gbip; only Σorder and global_stock (two aggregates) can. (Confirms the flat-producers paradox
   is expected, not anomalous.)
2. **The aggregates are ~FLAT at band resolution AND cannot yield the logged gbip.** Reconstructed
   Σ(price×share) ≈ 11 on q0; sqrt(0.6×11) ≈ 2.6. Σorder≈1507 / global_stock≈550 ⇒ 0.6·ratio ≈ 1.64,
   sqrt ≈ 1.28 — and this is ~constant across quarters. **Yet the actual gbip the CHI chain reads toggles
   0.0025 ⇄ ~0.7–0.88** (exact CURXV ticks). On the collapse quarters the per-TZ prices/shares in the dump are
   NONZERO and steady (india 2.75, central_europe 3.03, west_med 3.03 contribution) — they do NOT collapse —
   yet gbip = 0.0025, ~1000× below what those same-quarter inputs imply.

**INESCAPABLE CONCLUSION:** the `global_base_import_price_silver` value CONSUMED by the currency chain does
NOT equal sqrt(0.6·Σ(price×share)) computed from the same-quarter per-TZ values the TZP dump shows. The inputs
are steady; the consumed gbip toggles ~250×. Therefore the oscillator is a **TIMING / STALE-READ / ORDERING**
defect: on alternate quarters the chain reads gbip at a moment when it holds a freshly-RESET (near-zero) or
not-yet-reaggregated value — the reset-before-rebuild hazard. It is NOT a magnitude swing in any trade input,
NOT elasticity, NOT double-subtraction, NOT the denominator. (GLOBAL gbip band and CHI-chain gbip agree, so
the two are the same variable — the staleness is in WHEN that one variable is written vs read, not two vars
disagreeing.)

**NEXT (cycle 3 → trace):** pin the exact per-quarter ORDER of (a) the reset of per-TZ globals
(GT_split_reset_global_TZ_variables, :152-248), (b) the rebuild of local_price/stockpile/order, (c) the gbip
aggregation + sqrt (:2659-2708), and (d) WHERE in oa_wealth_changes the CURRENCY chain READS
global_base_import_price_silver (CURRENCY_svalues.txt:1091) relative to a-c. The period-2 signature =
something that recomputes/reads on a 2-phase cadence: e.g. gbip written every quarter but the sqrt-skip guard
(:2697 "only sqrt if base>0") leaving a stale/near-zero global when the summed base is 0 on alternate passes;
or the CHI read landing between reset and rebuild every other quarter; or trade running on a subset of goods
per quarter. Trace this; do not design until the write/read cadence is pinned and the near-zero value's origin
is identified in source.

### C.7-RESOLVED (2026-08-09) — cadence PINNED in source; oscillator is a SUB-BAND period-2 collapse of the gbip aggregation operands, invisible to the post-settle probe.

Traced the full quarter cadence in source (no boot needed):
- Silver ∈ trade category **6** (zz_tradegood_6_injector.txt:41) → processed on the LAST trade pass
  (`GT_split_do_global_trade_split { type=6 }`, oa_wealth_changes.txt, day 54 of the quarter).
- gbip has **exactly ONE writer** (se_GLOBALTRADE_split.txt:2659 sum, :2705 sqrt-in-place), called once
  per quarter inside that pass-6 via GT_split_get_global_import_unit_price_all (:38). It is a **deterministic,
  memoryless-w.r.t-itself** function: base = Σ_TZ(local_price_silver × pct_silver); if base>0, gbip=sqrt(base).
  local_price (:5898) and pct (:1458) do NOT read prior gbip, so there is NO self-referential period-2 here.
- The reset (:152) is scoped `every_tradegood_$type$_complex` → zeroes ONLY silver's own globals, on silver's
  own pass. No cross-pass/cross-good reset-before-rebuild staleness. **(kills the C.7 reset-ordering candidate.)**
- The TZP/POST probe fires in `quarterly_apply_trade_changes_and_consume` (day 61+), AFTER the pass-6
  aggregation AND after `GT_split_scale_order_size_and_payment_pools` (:55) + order_size_modifier mutate the
  order globals. So the probe records **settled end-of-quarter** per-TZ state, NEVER the aggregation-time
  operands that produced gbip.

**Exact-tick arithmetic (decisive, from CURXV not bands):** gbip lows are 0.0025/0.0030/0.0035/0.0060… =
sqrt(~1e-5); highs 0.62–0.88 = sqrt(0.39–0.77). ⇒ the pre-sqrt **base toggles ~0.77 ⇄ ~9e-6 period-2 (10⁵×)**.
A 22-term sum collapsing to 9e-6 requires **essentially EVERY term → ~0 simultaneously** on alternate quarters.
Prices are O(1) at band resolution and stocks/orders are FLAT decade-bands in the POST probe (india steady
100-1000 all 13 q; global_stock 550 on both a lo-q and a hi-q — so global_stock is NOT the driver). Therefore
the collapsing operand is **sub-band** (a within-decade swing that band logging cannot resolve) and lives at
**aggregation time (day 54)**, not at the settled snapshot (day 61) the probe captures.

**DIAGNOSIS (cycle 3, pending adversarial review):** the oscillation is a period-2 collapse of the gbip
aggregation inputs — either all `local_price_silver` (order/stock at price-compute time) or all
`pct = stock/global_stock` go to ≈0 every other quarter — occurring INSIDE pass-6 and thus INVISIBLE to the
post-settle TZP probe. This is a **BLOCKED-ON-DATA** state per imp19c-sobisonator-upstream-caution: I cannot
change shared upstream trade logic without the exact-tick operand values AT the aggregation site. The mandated,
non-optional response is to SHIP a targeted exact-value probe of the 44 gbip operands (local_price_silver +
pct_silver × 22 TZ) captured at :2659 (silver only, once/quarter — cheap), then re-boot. This supersedes the
"trace the cadence" NEXT above (cadence now pinned) and is NOT elasticity/double-subtraction/denominator (all
in graveyard).

---

## C.8 ROOT CAUSE — CONFIRMED (2026-08-09). The `sqrt` scripted effect is mathematically broken; gbip's "collapse" is a sqrt discontinuity at base=1.0, NOT a trade-input swing.

Cycle-3's adversarial review REFUTED the "10⁵× sub-band operand collapse / BLOCKED-ON-DATA" conclusion, and I
independently verified the refutation by HAND-TRACING the primitive (no boot needed — pure arithmetic against
the exact-tick log). The §C.7 base=gbip² inference was an artifact of ASSUMING sqrt works. It does not.

**The primitive** (`sqrt`, common/scripted_effects/se_ECON_functional.txt:56-111, "Tobbzn's method"):
```
param = $input$ ; x = param ; y = 1 ; e = 0.001 ; condition = x - y      # = param - 1
while ( condition > e ):
    x = (x + y) / 2
    y = x / param            # <-- LINE 96: BUG. Babylonian needs y = param / x
    condition = x - y
result = x
```
Correct Babylonian keeps x·y = param (so x,y bracket √param) via **y = param/x**; the code computes **y = x/param**.

**Hand-trace matches the log EXACTLY (this is the proof):**
- base < 1 (e.g. 0.882): condition₀ = 0.882 − 1 = −0.118, NOT > e ⇒ **loop never runs**, result = param = 0.882.
  → gbip HIGHS in log: 0.761, 0.654, 0.870, 0.882, 0.625 = the base returned raw (true √ would be ~0.79–0.94).
- base > 1 (e.g. 1.2): recurrence collapses to xₙ₊₁ = xₙ·(1+1/param)/2 (ratio<1) ⇒ **x decays geometrically to
  ~0**; halts when x·(1−1/param) ≤ e ⇒ result ≈ e/(1−1/param) ≈ 0.003–0.006.
  → gbip LOWS in log: 0.003, 0.004, 0.006 = the geometric-decay floor (base those quarters ≈ 1.2–1.4).

So the REAL pre-sqrt base wobbles gently ~0.7 ⇄ ~1.3 (≈2×) ACROSS THE DISCONTINUITY AT base=1.0, and the broken
sqrt rail-slams gbip between "≈base" (base<1 branch, loop skipped) and "≈0.005" (base>1 branch, decay-to-zero).
That single discontinuity IS the entire ~250× gbip oscillation and the inflation/deflation sawtooth downstream.

**Two coupled defects, both required to reproduce the symptom:**
1. **Recurrence inverted** (line 96): `y = x/param` should be `y = param/x`. Without this, base>1 decays to ~0.
2. **Guard not absolute** (line 74/82): `condition = x − y`; `while condition > e`. For base<1 the initial
   x−y = param−1 is NEGATIVE, so the loop is skipped and param is returned raw. Even AFTER fixing line 96 this
   guard still short-circuits base<1. The guard must test **|x − y| > e**. (The reviewer's one-line "flip line
   96" fix is therefore INSUFFICIENT — verified by re-trace: base<1 still returns param unchanged.)

**Blast radius: exactly ONE caller** — se_GLOBALTRADE_split.txt:2701 (the gbip write; guarded `if base>0`).
`rg "sqrt = \{"` finds no other invocation. So repairing the shared primitive changes only gbip. (The
FUNC_sqrt at :9-54 is an abandoned empty-while stub, never called — leave it.)

**Secondary (mild) oscillator, per review — NOT the primary cause:** a one-quarter-LAGGED elasticity/wealth loop
(country_unit_price_silver→reserve_ratio→essentials_buying_power→private_cash_ratio→inflation malus→
WEALTH_percentage_change_governorship→DEMAND_change_elasticity_impact cache (oa_wealth_changes.txt:293)→
DEMAND_elasticity_impact ×DEMAND_silver, DEMAND_svalues.txt:1286) makes base drift across 1.0 each quarter. It is
clamped max=1/min=0.1 (10× ceiling) and multiplies EVERY good, so it can only supply the mild ~2× base wobble —
which a CORRECT sqrt compresses to a ~1.14× gbip wobble (harmless). Address ONLY if oscillation survives the
sqrt fix (a deadband on DEMAND_change_elasticity_impact — see design/DIAGNOSIS_CURRENCY_INFLATION_SWINGS.md — is
the second-order lever). Watch-only thread: CURRENCY_reserve_accumulation_rate_from_inflation_or_deflation
(se_CURRENCY.txt:1188-1225) — but silver_reserve_size is FLAT in §A, so not currently a driver.

**STATUS: diagnosis COMPLETE and confirmed in source + arithmetic. Proceed to DESIGN (fix sqrt: correct
recurrence + absolute-value guard), adversarial-review the design, implement, adversarial-review the code.**

---

## D-FIX. DESIGN (2026-08-09) — repair the shared `sqrt` primitive in place.

**Goal:** make `sqrt = { input = N }` return a true √N (result = local_var:result) for all N > 0, converging
from either side of 1.0, so gbip = sqrt(base) is continuous and the rail-swing disappears.

**Scope / blast radius:** the primitive has ONE live caller (se_GLOBALTRADE_split.txt:2701, gbip, guarded
base>0). Repairing it in place fixes gbip with zero collateral. The abandoned FUNC_sqrt stub (:9-54) stays.

**Chosen approach — corrected Babylonian/Newton (minimal, proven method):**
```
sqrt = {                                   # input = $input$  (caller guarantees > 0)
    set_local_variable = { name = param  value = $input$ }
    set_local_variable = { name = x      value = local_var:param }   # seed x = N
    set_local_variable = { name = y      value = local_var:param  divide = ??? }  # y = N/x  (see below)
    set_local_variable = { name = e      value = 0.0001 }
    set_local_variable = { name = diff   value = { value = local_var:x  subtract = local_var:y } }
    if = { limit = { local_var:diff < 0 }  change_local_variable = { name = diff  multiply = -1 } }  # |x-y|
    while = {
        limit = { local_var:diff > local_var:e }
        set_local_variable = { name = x  value = { value = local_var:x  add = local_var:y  divide = 2 } }
        set_local_variable = { name = y  value = { value = local_var:param  divide = local_var:x } }  # FIX: N/x
        set_local_variable = { name = diff value = { value = local_var:x  subtract = local_var:y } }
        if = { limit = { local_var:diff < 0 } change_local_variable = { name = diff multiply = -1 } } # |x-y|
    }
    set_local_variable = { name = result  value = local_var:x }
}
```
Two corrections vs the shipped code, BOTH required (proven necessary by the C.8 hand-trace):
1. **Recurrence** — inside the loop `y = param / x` (was `x / param`). This is the Babylonian invariant x·y=N.
2. **Guard is |x − y|** — compute diff then negate-if-negative (proven abs idiom, se_ECON_LOG.txt:416). The
   original `condition = x − y` is signed, so for N<1 (x=N<1, y=N) the initial diff is negative and the loop
   is skipped, returning N raw. Absolute value makes the loop run for N<1 too. Also seed `y` = param (so the
   pre-loop diff is meaningful) — the very first loop iteration recomputes y = param/x properly.
3. **Tighten e to 0.0001** (was 0.001): at gbip magnitudes ~1, 0.001 tolerance is ~0.1% — fine — but 0.0001
   costs only ~1-2 extra iterations and removes any visible quantisation on the peg. (Minor; keep 0.001 if the
   reviewer prefers fewer iterations. Convergence is quadratic so iteration count stays ~5-8 either way.)

**Termination / safety:** for any seed x>0 and N>0, Newton's method converges monotonically after the first
step (x stays ≥ √N, decreasing; y ≤ √N, increasing), so |x−y| strictly decreases to 0 — the loop always
terminates. The caller's `if base>0` guard (se_GLOBALTRADE_split.txt:2697) already excludes N=0 (which would
divide-by-zero at y=N/x once x→0; cannot happen for N>0). No new div/0 risk. N is never negative (sum of
price×share, all ≥0).

**Rejected alternatives:**
- *Flip line 96 only* (reviewer's one-liner): INSUFFICIENT — re-trace shows N<1 still returns N raw because the
  signed guard skips the loop. Would fix the lows-collapse but leave gbip = base (un-rooted) for base<1, i.e.
  still wrong, just not rail-slamming. Rejected.
- *Route caller to a different/new sqrt effect*: no working sqrt exists elsewhere (se_FUNC.txt has only
  modifier-stack helpers). Building a second primitive duplicates code; repairing the one live primitive is
  smaller and lower-risk given the single caller. Rejected.
- *Damp the elasticity loop instead*: that loop is only the mild ~2× base wobble; it is HARMLESS once sqrt is
  continuous (a correct √ maps 0.7⇄1.3 to 0.84⇄1.14). Damping it would mask, not fix, and the audit already
  established (graveyard) it lacks the gain to be the primary cause. Deferred to "only if symptom survives".

**Acceptance (per ACCEPTANCE CRITERIA above):** post-fix -debug_mode boot must show gbip stable (no
0.003⇄0.88 toggle), private_cash_ratio ~1, inflation ~0, essentials_buying_power settling to a plausible
tael-equivalent (~5 taels/adult/yr yardstick). Re-run tools/curx_analyze.py on the new debug.log: the "gbip
actual (exact)" row should be flat, not toggling.

**NEXT: adversarial-review THIS design (attack the math + termination + the N<1 guard + e change), resolve,
then implement + code-review.**

### D-FIX.REVIEW (2026-08-09) — design review verdict: SOUND-WITH-CORRECTIONS. Two regressions in my draft caught + fixed.

The adversarial review confirmed the §C.8 root cause and the two named corrections (recurrence y=param/x;
absolute-value guard) but caught TWO regressions I introduced in the draft code, both verified by re-trace:
1. **SEED BUG (critical):** my draft seeded `y = param`. Then pre-loop diff = x−y = 0, |0| is not > e, the loop
   NEVER runs, and sqrt returns N unchanged for ALL N — worse than the original. The correct seed is the
   ORIGINAL `y = 1` (= param/x at x=param). The original seed was never the bug; only the recurrence + guard.
2. **EPSILON BUG (critical):** my draft tightened e to 0.0001. Under 3-decimal fixed-point the diff ULP is
   0.001, a near-root 2-cycle can pin diff at 0.001, and `0.001 > 0.0001` is ALWAYS true → INFINITE LOOP AT
   GAME LOAD, for zero perceptible benefit. KEEP e = 0.001 (terminates at 3 AND 5 decimals).
Everything else (Jomini syntax, single caller, sqrt-is-load-bearing-not-spurious) validated against source.

**FINAL APPROVED APPROACH — corrected Babylonian with a BOUNDED iteration count (maximally load-safe).**
Rather than the epsilon guard (whose safety depends on the engine's fixed-point resolution), use `count = 12`:
quadratic convergence reaches √N in ~7 iters for any realistic base (gbip base ~0.7–1.3; safe to N~10⁶), the
body is idempotent once converged (x=y=√N ⇒ x'=(x+x)/2=x), so it CANNOT hang under any resolution. Cost: 12
fixed iters once/quarter for one good — negligible. This sidesteps the entire e-vs-ULP question.
```
sqrt = { # Babylonian/Newton — repaired for #23 (recurrence y=param/x; bounded 12-iter for load-safety)
    set_local_variable = { name = param  value = $input$ }        # caller guarantees > 0 (se_GLOBALTRADE_split.txt:2697)
    set_local_variable = { name = x      value = local_var:param }   # seed x = N
    set_local_variable = { name = y      value = 1 }                 # seed y = 1 (= param/x; NOT param, which stalls)
    while = {
        count = 12                                                   # quadratic convergence: ~7 iters for N<=100; idempotent after
        set_local_variable = { name = x  value = { value = local_var:x  add = local_var:y  divide = 2 } }
        set_local_variable = { name = y  value = { value = local_var:param  divide = local_var:x } }   # FIX: N/x (was x/param)
    }
    set_local_variable = { name = result  value = local_var:x }
}
```
Verified traces (seed x=N, y=1): N=0.77 → 0.8775 (√=0.8775) by it3; N=1.3 → 1.1402 (√=1.1402) by it2; N=100 →
10.0 by ~it7; N=0.01 → 0.1 by ~it6. All then idempotent to count 12. Caller `if base>0` (:2697) excludes N=0
(the only div/0 site, y=N/x); N never negative. No new failure mode.

**STATUS: design APPROVED. Proceed to IMPLEMENT (edit se_ECON_functional.txt:56-111), then code-review, commit+push.**

### D-FIX.IMPL (2026-08-09) — IMPLEMENTED + code-reviewed PASS.
- Edited common/scripted_effects/se_ECON_functional.txt:56 — replaced the broken `sqrt` body with corrected
  Babylonian (seed x=param, y=1; loop `count=12`; recurrence y=param/x; result=x). Header comment documents
  the two original defects + why count=12 over epsilon.
- Refreshed the now-obsolete caller comment at se_GLOBALTRADE_split.txt:2688-2697 (the old epsilon-guard
  "Illegal use of operator >" rationale no longer applies; the `if base>0` guard stays — value-exact, cheap).
- Checks: BOM present both files; uniform CRLF, no bare-LF churn; braces balanced (21/21); no macro-void;
  no LOG-string `$`/`#`; no RHS-comparison violation (count loop has no comparison).
- Code-review verdict: **PASS, no defects, no nits.** Reviewer independently re-traced N=0.77→0.8775,
  N=1.3→1.1402, N=100→10.0 (iter7), N=0.001→iter8 — all converge inside count=12; loop cannot hang. Noted
  (non-blocking) that temp locals param/x/y persist in caller scope after return — harmless (overwritten next
  call, never read elsewhere), matches pre-existing pattern.
- Acceptance is BOOT-GATED: the user boot-tests on a separate machine. Post-boot, re-run
  tools/curx_analyze.py on the new debug.log — the "gbip actual (exact)" row must be FLAT (no 0.003⇄0.88
  toggle), inflation~0, private_cash_ratio~1, essentials_buying_power settling to a plausible tael-equivalent
  (~5 taels/adult/yr yardstick). If any residual wobble survives, the secondary elasticity loop (deadband on
  DEMAND_change_elasticity_impact) is the next lever — but the primary discontinuity is now removed.

**STATUS: #23 fix IMPLEMENTED, reviewed PASS, committed. Awaiting user boot-test for acceptance verification.**
- Log: `~/Downloads/logs.zip` (Aug 8 22:11) → `logs/debug.log`, grep `CURX`.
- `common/script_values/CURRENCY_svalues.txt` — ratio L753, need L719, ess L673, wvuraw L234,
  reserve_ratio_impact L376 (dead end #3), gbip_silver read L1091.
- `common/scripted_effects/se_GLOBALTRADE_split.txt` — gbip write L2659 (=sqrt(Σ TZ price×share)),
  per-TZ contributor L2500+, country_unit_price=gbip/(0.5+pen) L2717.
- `common/script_values/DEMAND_svalues.txt` — silver reserve demand (the `agsilver>0` gate suspicion).
- `common/scripted_effects/se_ECON_LOG.txt` — CURX dump emitter (~L700+).

---

## E. SECOND-ORDER BUG (2026-08-11) — post-#23-fix HIGH-INFLATION PLATEAU: silver price pinned high via empty-stockpile price spike (UPSTREAM)

Surfaced by the Aug-10 boot test (tracked as task #110). The #23 sqrt fix (§C.8/§D-FIX) killed the
OSCILLATION — confirmed by the boot cross-reference below — but a SEPARATE, pre-existing bug leaves the
currency on a HIGH-INFLATION PLATEAU (~16% vs the intended ~3%).

### E.1 MEASURED — boot cross-reference (5 logs × git timeline; #23 sqrt fix = 14c9ed899 @ 08-09 06:58)
Ran tools/curx_analyze.py on every -debug_mode log on disk; mapped each to code state by commit timestamp:
| boot log | code state | ratio (private_cash_ratio) | verdict |
|---|---|---|---|
| Aug 8 22:11 (`logs 4.21.57 AM.zip`) | M1=125M; PRE-#23-fix | 0.01↔7.76 | WILD OSCILLATION |
| Aug 9 04:22 (`logs 8.06.25 PM.zip`) | PRE-#23-fix | 1.46↔0.004 | WILD OSCILLATION |
| Aug 9 20:06 | post-fix, NOT -debug_mode (0 IMP19C) | — | — |
| Aug 9 22:42 (`logs 7.36.46 PM.zip`) | #23-fix + #111a ONLY | 1.59→2.18 | SETTLED, HIGH ~16% |
| Aug 10 23:18 (`logs.zip`) | ALL overnight econ commits | 1.49→2.67 | SETTLED, HIGH ~16% |
Conclusions: (1) #23 sqrt fix WORKED — oscillation gone across the pre/post boundary. (2) The overnight econ
layer (#50/#52/#59/#62/#67/#111a) is EXONERATED for the plateau — the Aug-9-22:42 boot already shows ~16%
and predates almost all of them; #111a exonerated specifically (only rescaled the Canton yield factor
×0.7→[0.5,1.3], a bounded reserve-QUANTITY effect, wrong channel + too small). (3) `agsilver`
(country_unit_price_silver) is pinned at the logger's 1.6 ceiling in EVERY post-fix boot.

### E.2 CODE CHAIN (all UPSTREAM — git-blamed, predates the fork's currency work)
1. `GT_set_tradegood_price` (se_GLOBALTRADE_split.txt ~L5818): `local_price = total_order_size` then
   `if stockpile>0 { divide = stockpile }` × 0.6. **The ÷stockpile is GUARDED on stockpile>0 — when a zone's
   silver stockpile = 0, the divide is SKIPPED and local_price = order_size × 0.6 UNDIVIDED**, spiking price to
   the order-size magnitude (hundreds).
2. `gbip_silver` = Σ(zone local_price_silver × zone stockpile-share)  (se_GLOBALTRADE_split.txt gbip build).
3. `country_unit_price_silver = gbip_silver / (0.5 + penetration_silver)` (GT_split_get_country_import_unit_price
   _tradegood). Blamed to upstream 172a2097a (2024-05-04). pen~0.1 ⇒ divisor ~0.6 ⇒ country price ~1.6× gbip.
4. `CURRENCY_wealth_value_from_silver = country_unit_price_silver × 16` (CURRENCY_svalues.txt). Blamed to
   upstream f20026af7 (2024-08-18). Feeds wealth_value_1_unit → the cost-of-living divisor
   (CURRENCY_essentials_buying_power ÷ wealth_value_1_unit_scaled_by_reserve_ratio) → private_cash_needed →
   private_cash_ratio (the logged `ratio`, inflation = (ratio−1)/10).

### E.3 LOG EVIDENCE (tzprobe silver-by-zone, current boot — price|stock|order bands)
China's own silver zones sit at **stockpile = 0 persistently**, with price railed to the top band exactly when
stock=0 — the §E.2-step-1 signature:
- `upper_yangtzi`: every quarter `10-100 | 0 | 1-10..10-100` (stock 0 throughout).
- `yellow_sea`: `100-1000 | 0` q0-q2, then `1-10..10-100 | 10-100`.
- `baltic`, `east_europe`: `100-1000 | 0` recurring.
So silver stockpiles are chronically ~0 → the price formula's ÷stockpile term is skipped → silver price spikes
structurally → drags gbip_silver and country_unit_price_silver to the high pin → collapses cost-of-living →
~16% inflation plateau. Consistent with the user's read: turns back to upstream; likely NEVER worked properly
for a silver-standard economy.

### E.4 STILL UNPROVEN (do NOT fix yet — Sobisonator-caution: upstream logic on an as-yet-unreviewed diagnosis)
- WHY silver stockpile is ~0: under-produced / over-consumed in the sim, or never seeded a stockpile? (supply
  side — could be mod seeding or upstream). Need to trace silver production/demand + initial stockpile seed.
- WHICH fix is right: upstream (the `stockpile>0` guard should FLOOR the price, not skip the divide — an
  upstream logic change needing explicit user sign-off) vs mod-side (seed a silver stockpile floor). Undecided.
- NEXT: prove the ~0-stockpile root (production vs demand vs seed) from code+log, THEN adversarial-review this
  §E diagnosis before proposing any fix. This is the LEADING diagnosis, NOT yet reviewed.

**STATUS §E: LEADING diagnosis, pending (a) proof of ~0-stockpile root + (b) adversarial review. #110 = this.**

### E.5 ADVERSARIAL REVIEW of §E (2026-08-11) — VERDICT: **REFUTED**. Empty-stockpile spike is weighted OUT of gbip.
The §E step-1→step-2 link is broken. Source-decisive (se_GLOBALTRADE_split.txt):
- **Share is stockpile>0-guarded (L1467-1480):** `zone_percentage_of_global_stockpile = zone_stockpile ÷ global_stock`
  ONLY `if zone_stockpile > 0`. A stockpile=0 zone has share = **exactly 0**.
- **gbip build (L2516-2701):** each zone contributes `local_price_TZ × percentage_of_global_stockpile_TZ`. Empty
  zone → (spiked price) × 0 = **0 contribution**. For a stocked zone the stock CANCELS:
  `(order/stock × 0.6) × (stock/global_stock) = 0.6·order/global_stock`. So NO per-zone price spike — empty or
  thin — can enter gbip; gbip depends only on Σorder and global_stock (two aggregates). This is the SAME
  correction the audit already recorded in §C.3/§C.7; §E re-proposed a buried theory (a regression).
- China's empty silver zones (share 0) are irrelevant to the GLOBAL sum; the real silver producers
  (central_europe, west_south_america, atlantic_seaboard, west_mediterranean) hold stock and dominate global_stock
  (§C.6). Denominator does NOT collapse.
- `agsilver 1.6!CAPPED` is the emitter top-banding `country_unit_price_silver ≥ 1` — NOT a spike. gbip ~1.3,
  /(0.5+pen~0.1) ≈ 2.1: the formula's INTRINSIC level, not a stockpile artifact.

WHAT §E GOT RIGHT (kept): the DOWNSTREAM direction — higher country_unit_price_silver ×16 → bigger ess divisor
→ lower ess → lower need → higher private_cash_ratio → higher inflation. And that country_unit_price_silver ≈1.6+
in every post-fix boot. The ARITHMETIC is sound; the SUPPLY-SIDE cause (empty stockpiles) is wrong.

### E.6 REAL LEADING CANDIDATE (post-refutation) — SCALE/CALIBRATION of the peg→ratio mapping, NOT a supply artifact
Given circ flat (~125) and ess a STEADY plateau (~13-20, not "collapsing" — §E overstated that), the ~2.7 ratio
(→ ~17% infl) is the level the calibrated chain settles to on plausible flat inputs:
`gbip (~1.3) → ÷(0.5+pen) → ×16 → ÷3 reserve-ratio` peg vs `amt_circulated×0.004`, then `inflation=(ratio−1)/10`.
i.e. a MIS-CALIBRATED peg/ratio SCALE (the acceptance-criteria concern at the top of this audit), not the
`stockpile>0` guard. A fix touching GT_set_tradegood_price's guard would edit a value that never reaches the peg
and would NOT move the plateau. NEXT (when resumed): trace the peg→ratio scale constants (×16, ÷3, ×0.004,
/(0.5+pen), the (ratio−1)/10 map) against the ~3% target; that is the calibration lever. This is the #110 lead now.

**STATUS §E: REFUTED (theory #10 → graveyard). Plateau cause re-scoped to peg/ratio SCALE calibration (§E.6),
not empty-stockpile supply. No fix attempted; #110 remains open on the §E.6 calibration lead.**

### E.7 (2026-08-11) — §E.6 "wealth_value_1_unit is ~2× too strong" PREMISE RETRACTED by user ("your premise is all fucked")
I derived "wealth_value_1_unit (silver×16/8) runs 2× too strong → need should be ~0.37 not ~0.18" from log
bands + back-of-envelope arithmetic and presented it as diagnosis. It is NOT verified.
TWO fabrications in that reasoning, both retracted:
  1. I invented a TARGET. There is NO intended/design ratio value and NO intended ~3% inflation. The "~3%"
     is ONLY a past-boot OBSERVATION (task #56, an older run) — a measured fact from one boot, NOT a target
     anyone set. I turned an observation into a calibration goal ("land the intended ~3% → ratio ~1.3") to
     justify a fix. There is no "intended anything" to calibrate toward. Delete that framing.
  2. I asserted the "2×" from assumed values of essentials_buying_power, country_population, the /4000/2000
     scaling — none read from the log; all assumed.
Same failure mode (plausible arithmetic + a fabricated target, asserted as a proven cause) as the four earlier
refuted theories. RETRACTED. Do NOT edit any peg/ratio constant (×16, units_to_the_lb, /(0.5+pen), ×0.004,
(ratio−1)/10) on this basis, and do NOT treat any inflation number as a "target."
#110 = OPEN, NO verified cause, NO defined target. IF revisited: (a) establish from the user/design what the
economy is even SUPPOSED to do (is high inflation wrong at all? what behaviour is desired?) BEFORE calling
anything a defect, then (b) add a targeted debug line (wealth_value_1_unit + essentials_buying_power +
private_cash_needed + country_population per quarter), boot, read ACTUAL values. No arithmetic-from-bands.

### E.8 (2026-08-11) — silver-zone "flap" observation: NOT a proven bug; stood down
Observed in the banded TZP data (both instrumented boots): several zones (yellow_sea, baltic, east_europe,
east_mediterranean, indo_china, eastern_steppe) show silver STOCK oscillating 0↔(10-100/100-1000) on a
~1-quarter period, price tracking inversely. I flagged this as a possible causeless numerical instability.
STOOD DOWN as a bug claim: (1) both prior deep audits AND Sobisonator judge the economy broadly SOUND —
a high bar a banded-log pattern does not clear; (2) per §E.5, an empty zone contributes ZERO to gbip
(stockpile>0-guarded share = 0), so this flapping is likely economically INERT — it does not reach the
currency peg; (3) I have not traced a mechanism, only read bands. Recorded as an UNPROVEN OBSERVATION for a
future targeted look IF ever warranted, NOT a defect. No fix. Do not treat as confirmed.

### F. TWO-BOOT DIFF (2026-08-11) — CAUSE ISOLATED TO MY #50 penetration change (NOT upstream)
Method: ran curx_analyze on BOTH instrumented boots, matched POST quarters term-by-term.
- EARLY = Aug 9 22:42 (`logs 7.36.46 PM.zip`): code = #23-fix + #111a only.
- LATE  = Aug 10 23:18 (`logs.zip`): code = + all overnight econ commits (#62/#44/#59/#50/#52/#67/#68/#69/#71cap).
FINDING — exactly ONE term shifted systematically between the boots:
  pen (market_penetration): EARLY 0.07–0.12  →  LATE 0.12–0.20  (uniform ~1.5–1.7× lift, EVERY matched quarter).
  ess falls / ratio rises in lockstep in LATE; agsilver bounces in BOTH (not the mover).
That ~1.54× is PRECISELY my #50 commit 2c52ed96a: penetration shrink 0.4545 → 0.7 (0.7/0.4545 = 1.54). It is
MY code, this run — not upstream (the /(0.5+pen) peg + the shrink line predate me, but the 0.4545→0.7 EDIT is mine).
MECHANISM: penetration feeds country_unit_price_silver = gbip/(0.5+pen) (GT_split_get_country_import_unit_price
_tradegood). Raising pen ~1.5× changes the peg divisor → shifts wealth_value/ess → raises private_cash_ratio →
higher inflation. #50 raised a term that feeds TWO systems (the intended regional-price-gap widening AND the
currency peg); I reasoned only about the first. The #50 commit's OWN warning ("confirm silver stays damped")
is exactly what the diff shows FAILED.
VERDICT: cause = #50 (mine), UNINTENDED currency side-effect of an intended gap-widening change. Upstream is
sound (both prior audits + Sobisonator concur); the divergence is entirely in my overnight edit.
NEXT: adversarial-review this diagnosis (is #50 the sole systematic mover, or do #52/#59 co-contribute to the
ratio climb?), THEN design the fix (revert 0.4545, or decouple the gap-widening from the peg), THEN review it.

### F.1 (2026-08-11) — USER: #50 was INTENTIONAL and fixed a real problem → fix = DECOUPLE, do NOT revert
The 0.4545→0.7 penetration lift is a legitimate, wanted change (widens the inter-country same-good price gap:
Canton silk vs London silk — the #50 regional-divergence goal). Reverting to 0.4545 is OFF THE TABLE; it would
undo a real improvement. The DEFECT is that penetration feeds TWO consumers and #50 moved both:
  (a) INTENDED: the regional price-gap ceiling (0.5+pen_max)/0.5 — keep the widened value here.
  (b) UNINTENDED: the currency peg country_unit_price_silver = gbip/(0.5+pen) — this got dragged along and
      shifted the inflation ratio (§F).
FIX DIRECTION (locked): DECOUPLE (b) from (a). Options for the design to weigh (post-review): the peg's
country_unit_price could read a penetration term pinned to the pre-#50 shrink (0.4545) or a separately-tuned
constant, while the regional-gap path keeps 0.7; OR damp the peg's sensitivity to pen; OR compute the peg from
a pen value that excludes the #50 widening. The regional-gap widening MUST survive; only its bleed into the
currency peg is corrected. NOT a revert.

### F.2 (2026-08-11) — the fix's BURDEN OF PROOF (user), before any lever change
"Penetration is the wrong lever" is PLAUSIBLE, NOT proven. Reverting #50 remains a legitimate option. The
design phase (after the review's mechanism map) must NOT just name an alternative lever — whichever lever the
fix proposes, the design must establish ALL THREE at the source level, or the lever is only a "candidate,
needs its own design+proof":
  (a) WHAT exactly the lever is (the precise var/term, where set + read);
  (b) WHY it produces the desired REGIONAL per-trade-zone divergence (Canton silk ≠ London silk), shown in the
      code path — not asserted;
  (c) WHY it has NO unintended side effects — enumerate the lever's OWN consumer graph (every svalue/effect
      that reads it) and show the regional change does NOT bleed into the currency peg / order sizes / trade
      income / shortages / #219 trade-AI. i.e. prove we are NOT relocating the penetration→peg bleed to a new
      term.
Decision rule: switch levers ONLY if the new lever is PROVEN regional AND PROVEN side-effect-clean. If an
alternative can't clear that bar in-analysis, prefer the option whose side-effect surface is already KNOWN
(revert to 0.4545 = known-good pre-#50 state; or decouple with a bounded, enumerated peg term) over an
unproven alternative. Rank options by PROVEN-clean side-effect surface, not by elegance.

### F.3 (2026-08-11) — #50 REVERTED (user directive), superseding F.1
User: "revert 50 and start scanning the codebase for entry points for a regional price index." F.1's
"decouple, do not revert" is SUPERSEDED. Rationale the user affirmed via the conquest test — "if China
conquers London, does cheap silk suddenly teleport there?" YES it does, because penetration feeds
country_unit_price which is per-COUNTRY (§G below), so #50 never produced true regional divergence in the
first place; it only lifted the country-wide price ceiling AND dragged the currency peg (§F). Wrong lever.
Committed 54673a6af: se_GLOBALTRADE_split.txt penetration block restored BYTE-FOR-BYTE to pre-#50 vanilla
(multiply 0.7 → 0.4545, terse "# Divide by 22" comment restored). The #52 tzprobe tooling extended in the
same #50 commit (se_ECON_LOG_TZPROBE.txt, gen_econ_tzprobe.py) is KEPT — it remains useful for measuring the
genuine regional-price work. Regional divergence is now a SEPARATE task on a geographic (per-zone) lever — §G.

## §G (2026-08-11) — REGIONAL PRICE-INDEX ENTRY-POINT SCAN (read-only; traced this session)
Goal: represent that the SAME good costs differently in different regions (Canton silk ≠ London silk) WITHOUT
dragging the currency peg or re-triggering #219. Below is the full price chain traced in
common/scripted_effects/se_GLOBALTRADE_split.txt, tagged PER-ZONE (already regional) vs PER-COUNTRY
(geography-blind — the reason #50 failed).

### G.1 — the chain, node by node (file:line)
1. **local_price_$good$  — PER-ZONE (already regional). GT_set_tradegood_price (:5901).**
   Scope: tradezone province. `local_price_$good$ = ($zone$_total_order_size / $zone$_stockpile) × 0.6`
   (food ÷ DEMAND_num_food_tradegoods). THIS IS THE REGIONAL PRICE — it already differs per trade zone by
   that zone's own order/stockpile ratio. Silk in the india TZ genuinely differs from silk in the
   central_europe TZ here. THIS IS THE LEVER a regional index must key off.
2. **global_base_import_price_$good$ (gbip) — GLOBAL scalar. GT_split_get_global_import_unit_price_tradegood
   (:2509).** gbip = Σ over 22 zones of (zone.local_price × zone_percentage_of_global_stockpile). A single
   stockpile-share-weighted world average. Collapses the per-zone spread into ONE number. Empty zones have
   share 0 so weight out.
3. **country_unit_price_$good$ — PER-COUNTRY, GEOGRAPHY-BLIND. GT_split_get_country_import_unit_price_tradegood
   (:2734).** `= gbip / (0.5 + country_global_market_penetration_$good$)`. Keyed on the COUNTRY's penetration,
   NOT on where its provinces sit. Every province a country owns pays this one price. ← this is why #50
   (which scaled penetration) could not make Canton ≠ London: both are CHI, both read CHI's country price.
   This term ALSO feeds the currency peg (essentials_buying_power → CURRENCY_private_cash_ratio) → the §F bleed.
4. **wealth_owed_for_$good$ — the payment. GT_split_update_wealth_owed_for_tradegoods (:2459), dispatched
   PER-TRADEZONE by GT_split_update_wealth_owed_for_all_TZs_tradegood (:2319).** KEY FINDING: the dispatcher
   (:2319) runs a `switch` on which TZ the governorship physically sits in and passes `$tradezone$` as a macro
   param — so at the payment site THE ZONE IS KNOWN. Yet line 2468 multiplies order_size × **owner.var:
   country_unit_price_$good$** (the global per-country price), discarding the zone. The regional signal exists
   one scope away and is thrown out here.

### G.2 — candidate entry points (for the design phase; NOT yet chosen — must clear §F.2 (a)(b)(c))
- **CANDIDATE A — regional price at the PAYMENT site (:2468).** Replace/blend
  `owner.var:country_unit_price_$good$` with a term that reads the paying governorship's OWN trade zone's
  `local_price_$good$` (available: the dispatcher already knows `$tradezone$`; the value is
  `global_var:global_$tradezone$_tradezone.var:local_price_$good$`). This makes wealth_owed genuinely regional
  (Canton province pays india/yellow_sea-TZ silk price; a London province pays central_europe-TZ price) —
  survives conquest correctly (price follows the province's ZONE, not its owner). Side-effect surface to prove
  per §F.2(c): wealth_owed feeds the $tradezone$_payment_pool + global_payment_pool (trade income
  distribution) — must confirm a regional price here does NOT feed back into country_unit_price / the currency
  peg (it should not: peg reads country_unit_price at :2734, a SEPARATE term). This is the MOST PROMISING
  entry — it is exactly where the geography is discarded, and it is downstream of the peg (no bleed by
  construction). NEEDS: full trace of every reader of wealth_owed_for_$good$ and the payment pools.
- **CANDIDATE B — a derived regional_price_index var (read-only display/tax lever).** Compute per-zone
  local_price ÷ gbip as an index (1.0 = world avg) and expose it WITHOUT touching wealth_owed — a pure
  reporting/flavour or a small regional tax/tariff modifier. Zero risk to peg/orders/#219 (adds nothing to the
  existing feedback loops), but also does NOT make provinces actually pay regional prices — weaker on the
  "Canton silk really is cheaper" goal. Fallback if A's side-effect surface proves entangled.
- **REJECTED — penetration (the #50 lever).** Per-country, geography-blind, feeds the peg. Proven wrong (§F/§G.1.3).

### G.3 — open questions the design must answer (before any edit — delicate upstream code)
- Does making wealth_owed regional (Cand. A) change TOTAL trade income materially, or just its DISTRIBUTION
  across a country's provinces? (order_size × local_price vs × country_unit_price — need the magnitude compare;
  the tzprobe kept from #50 can measure zone local_price vs gbip.)
- Do order SIZES read country_unit_price anywhere that would now diverge from the price actually paid
  (order_size_modifier at :2026 reads DEMAND + penetration, not country_unit_price — likely clean, confirm)?
- #219 trade-AI: the vanilla trade-request flood was tied to goods-VALUATION diplo factors (memory
  vanilla-trade-request-flood-open, zeroed in e3f3c2e91). Confirm a regional wealth_owed does not resurrect a
  valuation signal the AI reads.
- Manufactured goods: local_price for manufactured goods factors ingredient costs (:5936+, global_mean_price
  path) — confirm a regional payment term composes correctly with that (raw vs manufactured ordering).
NEXT: this scan feeds a DESIGN doc (design/DESIGN_REGIONAL_PRICE_INDEX.md) → adversarial review → the §F.2
three-part burden of proof, before any implementation. Cautious pattern, delicate upstream code.

## §H (2026-08-11) — §F.2(c) PROOF for Candidate A (the payment-site regional price) — traced, not asserted
The regional-price task (#112) picks up §G. §F.2(c) requires proving a lever change does NOT bleed into the
currency peg / orders / #219. For Candidate A (make wealth_owed at :2468 read the paying zone's local_price
instead of owner.country_unit_price), traced this session:

### H.1 — the currency peg reads country_unit_price DIRECTLY, never wealth_owed/local_price
CURRENCY_essentials_buying_power (CURRENCY_svalues.txt:673-701) = Σ of twelve `var:country_unit_price_<good>`
(grain, livestock, fish, vegetables, temperate_fruit, processed_foods, clothing, furniture, pharmaceuticals,
alcohol, luxury_clothing, luxury_furniture) ÷ CURRENCY_wealth_value_1_unit_scaled_by_reserve_ratio, cap 32000.
It feeds CURRENCY_private_cash_needed (:719) → the CURRENCY_private_cash_ratio → inflation. The peg's ONLY
price input is country_unit_price. It does NOT read wealth_owed, the payment pools, or local_price.
=> CONCLUSION: Candidate A leaves country_unit_price (:2734) UNTOUCHED, so the peg is disjoint from the payment
path BY CONSTRUCTION. No bleed possible. This is the structural reason #50 broke the peg (it scaled a peg
INPUT, penetration→country_unit_price) and Candidate A does not (it changes only what buyers PAY, downstream).

### H.2 — TWO DISTINCT CONCEPTS #50 wrongly conflated (the core insight)
(1) country_unit_price = the NATIONAL cost-of-living / currency anchor. CORRECTLY per-country — a currency's
    buying power is one national number. Must stay per-country; this is the peg input.
(2) what a PROVINCE actually pays for an import = SHOULD be regional (Canton silk ≠ London silk).
#50 tried to make (2) regional by scaling penetration, but penetration only moves (1) — so it dragged the peg
and never made provinces pay regional prices. Candidate A separates them: keep (1), regionalize (2).

### H.3 — the index's consumers, enumerated (CORRECTED per review112 finding 1 — my first pass was WRONG)
CORRECTION: an earlier draft claimed "wealth_owed feeds ONLY the payment pool → seller income." That is FALSE.
The full consumer set of wealth_owed_for_$good$ / the payment pool (traced grep):
  1. global_payment_pool + $tz$_payment_pool (:2495-2499) → GT_split_get_governorship_income_due (:3559-3585),
     the buyer→seller income redistribution. (the one I had.)
  2. **var:wealth_owed_for_gold / _silver read DIRECTLY** by GT_split_calculate_trade_shares (:5415, :5451,
     :5467, :5510) to build trade_share_$category$_the_state_{gold,silver}_reserves — the STATE reserve-capture
     income WEIGHT. Silver+gold are type-6 goods routed through :2462, so the index DOES reach this for the
     reserve metals.
  3. buyer-side queued_trade_expenses (:3530, :3536).
WHY §F.2(c) STILL HOLDS (the conclusion survives, the proof is now correct): consumer (2) feeds only strata
INCOME NORMALIZATION (:5597) and the state's own income application is COMMENTED OUT (:3984-3986); crucially it
NEVER writes silver_reserve_size (that is written only by se_CURRENCY / se_QING_REVENUE / se_QING_CANTON /
se_LAND — never the trade path, confirmed by review112), so it never reaches the peg's reserve_ratio input.
None of (1)(2)(3) feed country_unit_price, essentials_buying_power, order_size_modifier (:2026 = DEMAND+pen
only, §G.2), or penetration. => §F.2(c) SATISFIED — but the index measurably shifts strata income DISTRIBUTION
for the reserve metals (real, bounded by the clamp; add to the boot-measurement checklist alongside H.4).

### H.4 — the ONE real magnitude effect (not a bleed — a total-income shift, to be MEASURED not assumed)
Because buyers would pay regional local_price instead of the national country_unit_price average, the TOTAL
payment pool size changes (Σ regional prices ≠ Σ national-average price × quantities). That changes total trade
INCOME (redistributed to sellers), and its DISTRIBUTION across a buyer's provinces. This is the legitimate
economic consequence of regional prices, NOT a defect — but its magnitude must be measured on a boot (the #52
tzprobe kept from #50 already logs zone local_price vs gbip, so the ratio is observable). DESIGN must: (a) log
the pre/post total-pool delta, (b) confirm it doesn't swing trade income so hard it destabilizes treasuries.
This is the §F.2 "measure, don't assume" residual — a boot-tunable, not a blocker.

### H.5 — VERDICT: Candidate A clears §F.2 (a)+(b)+(c). Proceed to design.
(a) WHAT: wealth_owed_for_$good$ (:2468) multiply by the paying governorship's zone local_price
    (global_var:global_$tradezone$_tradezone.var:local_price_$good$; the dispatcher :2319 already knows
    $tradezone$) instead of owner.var:country_unit_price_$good$.
(b) WHY regional: local_price is set PER-ZONE from that zone's own order/stockpile ratio (:5901) — genuinely
    geographic; survives conquest correctly (a province's price follows its ZONE, not its owner's nationality).
(c) NO bleed: proven H.1+H.3 — peg reads country_unit_price (untouched); pool feeds only seller income.
Residual: H.4 total-income magnitude (measure on boot). Design doc = design/DESIGN_REGIONAL_PRICE_INDEX.md next.

## I. (2026-08-12) — NEW BUG, post-#112/#115: economy PINNED at flat -10% deflation (not oscillating)

Boot-test finding (fresh session). NOT the old §A/§C period-2 oscillation (that stays fixed — the #23 sqrt
repair is confirmed intact, se_ECON_functional.txt:56-102, recurrence y=param/x, count=12, unchanged). This is
a DIFFERENT, NEW symptom: `CURRENCY_amt_circulated_deflation` sits flat near its own formula ceiling every
quarter, no flip back to inflation.

### I.1 — REFRAME (the -10% number itself is not informative)
`CURRENCY_amt_circulated_deflation` = `(1 - ratio)` floored at 0.001, then `÷10` (CURRENCY_svalues.txt:1157-
1171). This expression only APPROACHES 0.10 as `ratio -> 0`. A flat reading near -10% means
`CURRENCY_private_cash_ratio` is pinned NEAR ZERO, not merely below 1. The real question is why the ratio
collapsed to ~0 and stayed there — not "why -10%."

### I.2 — FIRST HYPOTHESIS (mine), WRONG — killed by user-corrected timeline + math, kept here as a graveyard entry
I proposed: commit 75f25152a ("Revert 50 penetration cap-lift 0.7 -> 0.4545") pushed the system into deflation,
since it landed after the user's last-known-good boot and inside the same commit range separating the two
sessions.
**REFUTED, two ways:**
- **Timeline:** `0.4545` is the long-standing PRE-#50 vanilla value (§F/§F.3) — it was already active during
  the OLD, since-fixed oscillation era, long before this session. A value that predates the symptom's first
  appearance cannot be what newly caused it. Restoring an old baseline is not a new perturbation.
- **Magnitude:** even taking the mechanism at face value, `pen` only ranges ~0.07-0.20 (§F). Reverting
  0.7->0.4545 moves `(0.5+pen)` by at most a few percent. That cannot drag `ratio` from its healthy range down
  to ~0. The effect is real in DIRECTION (smaller pen -> smaller divisor -> higher price -> more deflationary
  pressure, confirmed by a second independent read) but three orders of magnitude too small to be the driver.
**Do not re-propose #50/penetration-shrink as the cause of THIS bug.** Add to the graveyard (§B).

### I.3 — LEADING CANDIDATE (unconfirmed, needs the check §H.4 already called for and never ran)
§H already proved (H.1-H.3) that #112/#115's payment-site change (`wealth_owed_for_$good$` now multiplies by
the paying zone's `local_price` instead of the national `country_unit_price`) does NOT bleed into the peg's
PRICE anchor (`country_unit_price`/`essentials_buying_power` are untouched, confirmed by direct consumer
enumeration). §H.4 explicitly flagged a SEPARATE, NOT-YET-MEASURED consequence: because buyers now pay
per-zone prices instead of one national average, **the TOTAL size of the payment pool changes** — and that
total, unlike the price anchor, DOES reach the currency ratio through a path §H never traced:
- `TRADE_national_expenditure` (TRADE_svalues.txt:4412) sums, over every governorship,
  `final_quarterly_trade_expenses_due_resource_extraction` + `final_quarterly_trade_expenses_due_manufacturing`
  — the SNAPSHOTTED totals of the exact `wealth_owed_for_$good$` values #112/#115 changed the formula for.
- `TRADE_national_expenditure` feeds `CURRENCY_private_cash_needed` (CURRENCY_svalues.txt:727-728, subtracted)
  AND `CURRENCY_trade_wealth_outgoing_currency_value` (:949-968), which feeds `CURRENCY_amt_circulated_balance`
  (:973-993) — the MONTHLY update to the circulating-cash stock itself (`CURRENCY_amt_circulated_thousands`,
  se_CURRENCY.txt:1408-1416).
So a shift in total trade-expenditure size from #112/#115 has TWO live paths into the ratio: it can shrink the
numerator (circulating cash, via the monthly balance update) AND grow the denominator (private_cash_needed)
simultaneously — either alone would depress the ratio; together they compound. This is exactly the "total-
income magnitude" effect §H.4 named as a residual and said must be MEASURED, not assumed, before this design
could be called fully clear. That measurement was never done.
**NOT YET CONFIRMED.** No boot-instrumented numbers exist for `TRADE_national_expenditure`,
`CURRENCY_private_cash_needed`, or `CURRENCY_amt_circulated_thousands` pre/post #112/#115 to prove the size or
even the sign of this effect. This is the leading lead, not a diagnosis.

### I.4 — SECOND CANDIDATE (unconfirmed, lower confidence) — MONSTD_reconcile
Commit 821b9b73e (#75, Monetary Standard law group) added a NEW recurring monthly effect, `MONSTD_reconcile`
(se_MONSTD.txt), which can flip a country's currency `backing_type` (gold/silver/bimetallic) when it diverges
from the held law. A flip changes which metal's `country_unit_price` feeds `CURRENCY_essentials_buying_power`
(cost of living) via `CURRENCY_update_backing_value` (se_CURRENCY.txt:1956+). This is a genuinely NEW,
currency-touching, monthly-recurring mechanism absent from the last-known-good boot's code state — structurally
capable of sustaining a persistent shift if a country's backing flips (or keeps flipping) into a metal whose
price basis is unfavorable. NOT traced in depth; not ruled in or out. Lower priority than §I.3 pending that
measurement, since #75 fires only on an actual law/backing MISMATCH (one-time correction per mismatch), while
§I.3's path runs every quarter unconditionally.

### I.5 — NEXT STEP (not yet done)
Add targeted se_ECON_LOG lines for `TRADE_national_expenditure`, `CURRENCY_private_cash_needed`,
`CURRENCY_amt_circulated_thousands`, and `CURRENCY_private_cash_ratio` (none of these are currently traced by
any existing probe — confirmed by grep, zero hits in either boot's debug.log for `private_cash` or
`circulated_deflation`), then boot and read actual values. Until then §I.3/§I.4 remain candidates, not a cause.
No fix attempted.

### I.6 (2026-08-12) — NEW DIAGNOSIS, run against the fresh Aug-12 log with `tools/curx_analyze.py`

The tool this audit already built (`tools/curx_analyze.py`) reads the CURX/CURXV/TZP tags. It still works.
Ran it against the fresh boot log (Aug 12, 18:43, 4.79M lines, 522 CURX ticks, 29 quarter-marks). This is
the first time in Section I that a real trace, not a guess, was checked. No fix made. Facts only, below.

**FACT 1 — the ratio never crosses back to a high state.** The CHI CURRENCY CHAIN table (all 29 PRE/POST
snapshots) shows `ratio` at `0.01-0.10` on 22 of 29 rows, dips to `< 0.01` on 3 rows, and rises only to
`0.25-0.50` on 2 rows (idx 6-7). It NEVER reaches the old bug's State A band (`>= 1.50`, per §A). `infl`
reads `= 0` on EVERY row. This confirms the user's report exactly: the system is not oscillating, it sits
in one low band, with two small dips even lower and one small partial recovery that still falls short of
inflation territory.

**FACT 2 — `gbip` (the value the #23 sqrt fix targets) is STABLE, not swinging.** The gbip-reconstruction
table shows `gbip actual (exact)` at 0.76 on quarter 0, then 0.35-0.41 for all 13 remaining quarters — a
tight, flat band. Compare this to the OLD bug (§C.7/§C.8): a ~250x rail-to-rail swing every quarter
(0.003 to 0.88). This log shows NO such swing. **This proves the #23 sqrt fix is still working.** The old
mechanism is not back. This matches the user's own correction: this is a new bug, not the old one returning.

**FACT 3 — `agsilver` (country_unit_price_silver) also settles low and stays there.** It reads `>= 1` only
on the first 2 rows, then drops to `0.5-1` and stays there for the remaining 26 rows. It does not recover.
Per §A's own consistency check (`agsilver` follows `gbip`), a lower stable `gbip` naturally gives a lower
stable `agsilver` — consistent, not a new anomaly on its own.

**FACT 4 — `pen` (penetration) sits inside the range §F already measured, RULING OUT §I.2 again by direct
observation, not just by the earlier math argument.** `pen` moves from `0-0.1` to `0.1-0.5` at snapshot 3
and stays there. §F's own two-boot diff measured `pen` at 0.07-0.20 in both of ITS boots (before and after
the #50 lift). This fresh log's `pen` band overlaps that same range. It is not spiking, not collapsing, and
not behaving differently from prior boots. §I.2's refutation stands, now confirmed by a THIRD boot's data,
not just arithmetic.

**WHAT THIS MEANS:** the low, flat `gbip`/`agsilver` band is not an active oscillation, and it is not being
pushed low by `pen`. The remaining candidates from §I.3/§I.4 (the #112/#115 total-trade-expenditure path,
and the #75 MONSTD_reconcile backing-flip path) are UNCHANGED by this pass — this log does not carry the
`TRADE_national_expenditure` / `private_cash_needed` / `amt_circulated_thousands` tags (confirmed again by
direct grep on this log, zero hits, matching §I.5's earlier finding on the other two logs). So this pass
answers "is the OLD bug back" (NO) and "is the #50 revert the cause" (NO, confirmed a third way), but does
NOT yet answer "what is holding gbip/agsilver at this new, lower flat level instead of the old flat level."

**STATUS: §I.2 REFUTED a third time (timeline, math, AND now direct log observation — safe to fully retire).
§I.3/§I.4 remain the live candidates, still unconfirmed. The missing piece is exactly what §I.5 already
named: log `TRADE_national_expenditure`, `CURRENCY_private_cash_needed`, `CURRENCY_amt_circulated_thousands`
directly — the existing CURX/TZP tags do not cover them. No fix attempted.**

### I.7 — SELF-REVIEW of §I.6 (2026-08-12) — attacking my own new facts before calling them a diagnosis

This diagnosis is NOT yet complete. It only rules two things OUT (the old oscillation, the #50 revert). It
does not name a confirmed cause for the new flat floor. Checking my own work before handing it forward:

1. **Did I mistake "gbip is flat" for "gbip is fine"?** No — I did not claim the CURRENT flat gbip level is
   correct or healthy. §A's own acceptance criteria (top of this doc) says `private_cash_ratio` should rest
   NEAR 1 in a well-run economy. This log's ratio sits at 0.01-0.10 nearly the whole game. That is still a
   bug by the doc's own stated bar — I am only saying it is a DIFFERENT bug shape (flat-low, not
   oscillating) than the one §C-§D fixed.
2. **Is my "gbip stable -> old bug not back" claim actually solid?** Yes, on this data: the old bug's own
   signature (§C.7, exact ticks) was gbip toggling between ~0.003 and ~0.88 EVERY quarter. This log shows
   13 of 14 quarters within 0.35-0.41 of each other — far tighter than the old swing, and never touching the
   old bug's near-zero rail (lowest gbip value in this log is 0.35, not 0.003). This is a real, checkable
   difference, not a band-resolution illusion — the tool prints exact CURXV values, not just bands, for gbip.
3. **Could the low-but-flat gbip level itself just be the correct, INTENDED level, and the real bug live
   entirely downstream (in `need`/`private_cash_needed`, matching §I.3's trade-expenditure lead)?** This is
   the honest open question. I have NOT measured `private_cash_needed` or `TRADE_national_expenditure`
   directly in this pass — I only confirmed gbip/agsilver/pen are NOT the movers. §I.3's candidate is
   therefore still standing, unweakened and unconfirmed, exactly as before this pass. I am not overclaiming
   it as proven.
4. **Did I check enough of the log, or just the CHI-scope tags?** The CHI CURX tags are CHI-scoped by design
   (§C.1's own caveat). This pass does not add producer-side or non-CHI evidence. That caveat from the OLD
   bug still applies in principle, but it is less relevant here because FACT 2 already shows the mechanism
   the old bug needed (a swinging gbip) is simply absent now — there is no swing left to localize to a
   producer zone. I am not claiming the caveat is resolved, only that it does not block THIS pass's narrower
   conclusion (ruling out the OLD bug's return).

**VERDICT of self-review: FACTS 1-4 hold up. The two negative conclusions (not the old bug; not the #50
revert) are now confirmed by direct log data, not just prior arithmetic. The positive cause (§I.3's
trade-expenditure path, or something else entirely feeding `private_cash_needed`) is still unconfirmed and
requires the targeted log lines §I.5 already specified. This is the honest state of the diagnosis. No fix
attempted, per standing instruction to hold until the mechanism is proven.**

### I.8 (2026-08-12) — tool widened to all 22 zones x 16 goods; new finding + a real, named BLIND SPOT

User asked for full per-good, per-zone logging. Checked what exists: `common/scripted_effects/
se_ECON_LOG_TZPROBE.txt` (generated by `tools/gen_econ_tzprobe.py`) already logs 22 zones x 16 goods
(silver, gold, grain, salt, fish, tea, silk, silk_cloth, porcelain, gems, opium, coffee, sugar, spices,
tobacco, chili) — full coverage already exists in the LOG. The gap was in `tools/curx_analyze.py`, which
hard-coded a silver-only regex and silently read only 1 of the 16 goods present. Added `--good <name>`
(default silver, old behaviour unchanged) so any tracked good can be read the same way. Saved as memory
`imp19c-curx-analyze-tool`.

**Checked every good the widened tool can reach against §H.1's exact list of the 12 goods that actually
feed `CURRENCY_essentials_buying_power`** (grain, livestock, fish, vegetables, temperate_fruit,
processed_foods, clothing, furniture, pharmaceuticals, alcohol, luxury_clothing, luxury_furniture — the
cost-of-living sum that drives `CURRENCY_private_cash_needed` -> the ratio). Result: **the probe's 16
tracked goods overlap the peg's 12 goods in only 2 places: `grain` and `fish`.** The other 10 goods that
directly set cost of living (`livestock`, `vegetables`, `temperate_fruit`, `processed_foods`, `clothing`,
`furniture`, `pharmaceuticals`, `alcohol`, `luxury_clothing`, `luxury_furniture`) have **zero** per-zone
visibility in any existing log or tool. This is a real, confirmed blind spot, not a guess.

**Checked the 2 goods that ARE both tracked and peg-relevant:** `grain` is cheap and stable in every zone,
including China's own (yellow_sea, upper_yangtzi) — not a driver. `fish` is small, stable, and contributes
almost nothing to its own world-price sum (Σ price×share ~0.1-0.6, far below spices' ~1-9) — not a driver.
**Both peg-relevant goods I can actually see are healthy.** This weakens (does not disprove) any theory
that blames the everyday cost-of-living basket broadly, and sharpens the open question to: is the driver
hiding in one of the 10 UNCHECKED peg goods, or genuinely in the trade-expenditure path (§I.3), or in
`MONSTD_reconcile` (§I.4)?

**A real, checkable side-finding while widening the tool (kept for the record, NOT claimed as the cause of
THIS bug since spices is not a peg input): `spices` in `yellow_sea` (a China-adjacent zone) shows a
genuine, non-band-resolution price spike** — price climbs from band `0.1-1` (q0) through `10-100` (q7),
`100-1000` (q9), to `1000-10000` (q13) while stock collapses `10-100` -> `0-0.01` over the same window.
Unlike silver's §E.5 refutation (where an empty zone's SHARE also collapses to ~0, weighting the spike
OUT of the world sum), yellow_sea's spice CONTRIBUTION (price_mid x pct_mid) does NOT collapse — it
actually PEAKS at 2.75 (the single highest value anywhere in the whole 22-zone table) at q9-11, meaning
its share did NOT fall proportionally as its stock fell. This shows the §E.5 mechanism ("empty zones
always weight themselves out") is NOT universal across goods — it can fail for a good/zone pair where
that zone holds a large enough fraction of a small enough global pool. Real, but spices does not feed
the currency peg, so this is a candidate MECHANISM (worth remembering if any of the 10 unchecked peg
goods shows the same shape), not a proven cause of the current deflation floor.

**STATUS: blind spot named and now on record. To close it, `tools/gen_econ_tzprobe.py`'s GOODS list would
need the 10 missing peg goods added (a real, mechanical extension of an existing generator — not new
design) and a fresh boot taken. That boot has not been requested or taken. No fix attempted on any game
file. §I.3/§I.4 remain the standing candidates; this pass narrows but does not close the question.**

### I.9 (2026-08-12) — SELF-REVIEW CORRECTIONS, three real errors found and fixed. `need` was ALREADY measured.

An adversarial review of I.6-I.8 found three real problems. All three checked and confirmed true by
re-reading the same log directly. Corrections below; nothing in I.6-I.8 is deleted, this section fixes it.

**ERROR 1 (the important one) — I said `CURRENCY_private_cash_needed` was unmeasured. IT IS ALREADY
MEASURED.** I.5/I.6/I.8 all say "no boot-instrumented numbers exist for `CURRENCY_private_cash_needed`,"
confirmed by "grep, zero hits for `private_cash`." The grep was for the wrong STRING. The tool's own
EXACT VALUES table already prints a `need` column every quarter, and `need` IS
`CURRENCY_private_cash_needed` (§A's own naming; confirmed numerically: `ratio = circ×0.004/need`, e.g.
idx0: 125×0.004/5.796 = 0.086, matching the printed ratio exactly). I searched for a STRING
(`private_cash`) instead of recognizing the TAG (`need`) already carries the value. This is exactly the
project's own standing "hypothesis-grep, not full read" trap.

**What the recovered `need` values actually show (from the same log, re-read directly):**
```
idx | need        | ess (cost-of-living)
  0 | 5.796       | 20
  1 | 6.978       | 32
  6 | 1.76        | 64
  7 | 1.914       | 76
 10 | 12.64       | 87
 11 | 11.99       | 40
 20 | 10.99       | 34
```
and roughly HALF the quarters print `16!CAPPED` (the tool's exact-tick counter saturates at 16 — the true
value is higher, not exactly 16). `ess` stays inside a 20-87 band the WHOLE game (~4x spread at most).
`need` swings from ~2 up through a repeatedly-capped 16+ — a much bigger swing than `ess` alone can cause.
**`need`'s own formula (CURRENCY_svalues.txt:719-731) is:**
`need = ((ess × country_population) / 4000 − CURRENCY_trade_wealth_outgoing_currency_value +
CURRENCY_wealth_generated_country_as_currency_value) / 2000`
Since `ess` only moves ~4x and `need` moves far more than that (and repeatedly saturates the logger),
**the mover is one of the OTHER three terms** — `country_population`, `CURRENCY_trade_wealth_outgoing_
currency_value` (the exact term §I.3 already named, sourced from `TRADE_national_expenditure`), or
`CURRENCY_wealth_generated_country_as_currency_value`. This is now a narrowed, three-way question with
real numbers behind it, not a guess. **This directly strengthens §I.3** (the trade-expenditure path was
already the leading candidate; it is now the correct explanation for a number I can show is actually
moving, not just a plausible story).

**ERROR 2 — miscounted rows in Fact 1.** I said ratio dips to `&lt;0.01` on 3 rows. Re-checked against the
exact-tick table above: idx 4 (0.006), 5 (0.006), 26 (0.009), 27 (0.009), 28 (0.002) — that is **5** rows,
not 3. (22+5+2=29, matching the total; my original 22+3+2=27 did not even sum to 29 — a check I should
have run at the time and didn't.) Corrected here; does not change the conclusion, only the count.

**ERROR 3 — the spices/yellow_sea "share does not collapse" claim in I.8 does NOT survive.** The 2.75
contribution figure is `midband("100-1000") × midband("0-0.01") = 550 × 0.005`, an arithmetic product of
two BAND MIDPOINTS, not a real reading — spices has no exact-tick layer at all (metals-only, confirmed in
`gen_econ_tzprobe.py`). The share band `0-0.01` is consistent with a true share anywhere from ~0.0001
(genuinely near-zero, matching §E.5) to ~0.0099 (not near-zero) — the midpoint approximation cannot tell
these apart, and asserting a mechanism from it is exactly this document's own catalogued Section-B
mistake ("assert from bands where exact numbers were needed"). Also: by q13, when stock fully collapses,
the contribution DOES drop to `0.00` — i.e. the share eventually DOES hit zero, which is §E.5's mechanism
working, not failing. **RETRACTED. §E.5 (empty zones weight themselves out of the world sum) stands,
un-contradicted, for every good including spices.** The remaining, correctly-hedged part of I.8 (the
2-of-12 peg-good coverage gap) is unaffected by this retraction and still stands — it did not depend on
the spices claim.

**Also corrected: Fact 2's "gbip is stable → proves the sqrt fix is working" overstated what flatness can
prove.** A flat gbip only rules out the OLD symptom (rail-to-rail oscillation); it cannot, by itself,
distinguish "correct sqrt on a stable input" from "still-broken sqrt on an input that happens to sit
below 1.0 every quarter this game" (the broken sqrt returns its input UNCHANGED, not rooted, whenever
that input is below 1 — see §C.8). The stronger, correct basis for "the old bug is not back" is that the
sqrt SOURCE is unchanged (`se_ECON_functional.txt:56-102`, checked directly, matches the D-FIX.IMPL text)
combined with the flat log — source-plus-log together, not the log alone. Restating: "the old bug is not
back" still holds; "this proves the fix is working" was overclaimed and is corrected to "consistent with
the fix still working, corroborated by the log."

**STATUS: §I.3 (TRADE_national_expenditure path) is now the STRONGEST standing candidate, not merely the
"leading, unconfirmed" one — `need`'s own already-measured swing (not merely `ess`) is consistent with a
term other than cost-of-living driving it, and `TRADE_national_expenditure` is the only one of the three
remaining candidate terms this document has already traced end-to-end (§I.3). §I.4 (MONSTD_reconcile)
remains a live but untraced second candidate. NEXT: log `CURRENCY_trade_wealth_outgoing_currency_value`,
`country_population`, and `CURRENCY_wealth_generated_country_as_currency_value` directly (the three
un-decomposed terms of `need`) to see which of the three actually moves — `need` itself no longer needs
a new probe, it is already in hand. No fix attempted on any game file.

### I.10 (2026-08-12) — DIAGNOSIS: §I.4 (MONSTD) ruled out by log; #112/#115's regional-price rewrite is the
### confirmed cause. Root: a per-zone `local_price` floored at 0.0001 lets an empty-stockpile zone's price
### spike by orders of magnitude, and that spike now feeds the trade-expenditure term inside `need`.

**Method, per direct instruction:** narrow the commit search to ONLY files that can touch `need`'s three
formula terms (`CURRENCY_svalues.txt`, `se_CURRENCY.txt`, `WEALTH_svalues.txt`,
`on_action/economy/*.txt`), read every one of the resulting commits, rule each in/out on the CODE, then
cross-check the survivor against the real log. Five commits touched that narrow file set:

```
821b9b73e 75: implement Monetary Standard law group (59 Tier C) + reconciler
80c0a4c83 Revert "106: seed shipping_<zone> vars to 0 ..."
434ee3841 106: seed shipping_<zone> vars to 0 ...
a62300015 74: sell-degrees (捐納) yields silver — fallback grant in CURRENCY_grant_country_wealth
2de48741e 102: raise treasury cap 99999 -> 9999999
```

**#74 (a62300015) — RULED OUT.** Diff only touches `CURRENCY_grant_country_wealth`'s rare one-time
fallback-grant else-branch. Does not touch `need`'s formula at all.

**#102 (2de48741e) — RULED OUT.** Diff raises `MAXIMUM_GOLD` and the paper-money-law branch of
`CURRENCY_minting_rate_cap`, plus 4 unrelated debt-issue GUI gates. Does not touch `need`'s formula.

**#106 (434ee3841) and its revert (80c0a4c83) — RULED OUT.** Both versions only add/remove
`SHIPPING_seed_zone_defaults` (seeds 22 `shipping_<zone>` vars to 0 to kill unset-var log noise). Grepped
the whole repo for `shipping_<zone>`'s only consumer, `SHIPPING_svalues.txt` — it is not read by
`TRADE_national_expenditure`, `WEALTH_total_new_generated_governorship`, or any term of `need`. No path in.

**#75 (821b9b73e, Monetary Standard law group) — RULED OUT BY THE LOG, not just by code.** This was §I.4's
long-standing "second candidate," on the theory that `MONSTD_reconcile` flipping a country's
`backing_type` changes `CURRENCY_wealth_value_1_unit`, which is the divisor of BOTH remaining `need` terms
— a real mechanism, worth checking directly rather than dismissing on priors. The log resolves it: grepped
`logs/debug.log` for `MONSTD_reconcile`'s own LOG_enter/LOG_exit pair — it fires every month, every
country, exactly as designed (confirmed running). But grepped for its OWN callee's log line,
`MONSTD_switch_backing`'s `LOG_line = "monetary standard: switching..."` — **zero hits in the entire
boot.** The reconciler ran every month and never once found a mismatch to act on (every country's held law
already matches its seeded `backing_type` the whole game, exactly as `MONSTD_seed_starting_law` intends).
The mechanism is real but **inert this boot** — `backing_type` never changes, so `CURRENCY_wealth_value_1_unit`
never changes for this reason. #75 is not the cause of THIS symptom.

**All 5 commits in the narrow file set are now ruled out.** Per the same instruction ("most of the changes
did not touch this specific part of the code"), this means the driver is not a change to `need`'s own
formula — it is a change to one of `need`'s two DOWNSTREAM input terms:
`CURRENCY_trade_wealth_outgoing_currency_value` (reads `TRADE_national_expenditure`) or
`CURRENCY_wealth_generated_country_as_currency_value`. Traced `TRADE_national_expenditure`
(`TRADE_svalues.txt:4412`) down to its real source: it sums, per governorship,
`final_quarterly_trade_expenses_due_resource_extraction` + `..._due_manufacturing`, which in turn are
quarterly snapshots of `trade_expenses_due_$category$` — the running total that
`GT_split_scale_wealth_owed_and_order_size_tradegood` feeds from `wealth_owed_for_$tradegood$`.
**`wealth_owed_for_$tradegood$` is set by `GT_split_update_wealth_owed_for_tradegoods`
(`se_GLOBALTRADE_split.txt:2498`) — exactly the effect two commits outside the narrow file set rewrote:**

```
2b7142977 112: regional import pricing — pay the paying zone's local_price, not the national average
7663239b1 115: regional import price "both" model -- per-zone penetration denominator
```

**#112 replaced** `multiply = owner.var:country_unit_price_$tradegood$` (one national price per country,
computed by `country_unit_price`'s own formula, `min = 0.0001` on the WORLD-AGGREGATE `global_base_import_
price`) **with** `multiply = { value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$
min = 0.0001 divide = { 0.5 + penetration } }` — a PER-ZONE `local_price`, `min`-floored at 0.0001
INDIVIDUALLY per zone rather than after a 22-zone blend. #112's own commit message explicitly names the
mechanism and flags it as unresolved: *"the §E zero-stockpile SILVER zones (upper_yangtzi/yellow_sea)
price undivided → order-scale spike re-exposed here; measured on boot."* #115 layered a per-zone
penetration denominator on top (same shape, same floor behavior), not a new mechanism.

**`local_price_$tradegood$` (`se_GLOBALTRADE_split.txt:6000-6032`, `GT_set_tradegood_price`) is**
`order_size / stockpile` (guarded `has_global_variable` + `>0`, ELSE the divide is skipped and price =
raw order size — i.e. UNDIVIDED) `× 0.6`. **A zone with zero stockpile and nonzero orders never divides —
its price is the raw order count itself, not a normalized ratio.** Confirmed directly in the log
(`unzip -p logs.zip logs/debug.log`, `IMP19C TZP BAND silver upper_yangtzi/yellow_sea`):

- `upper_yangtzi`: `stock 0`, `order 1-10` at q0 (price then `10-100`, i.e. price ≈ raw order, undivided) —
  the exact zero-stockpile state #112 flagged.
- `yellow_sea`: `stock 0`, `order 10-100` at q0 (price `10-100`); after stock recovers (`100-1000`+),
  order stays `10-100`+ but price DROPS to `0.01-0.1` — an order-of-magnitude-plus swing between the
  undivided (zero-stock) state and the divided (stocked) state, for the exact reason #112's own comment
  predicted.

This is the concrete mechanism reaching `need`: a zone briefly at zero stockpile prices at its raw,
undivided order count (can be 10-1000+×), gets paid at that price by `GT_split_update_wealth_owed_for_
tradegoods` (multiplying `wealth_owed_for_$tradegood$` by this spiked `local_price`), which feeds
`trade_expenses_due_resource_extraction/manufacturing` → `TRADE_national_expenditure` →
`CURRENCY_trade_wealth_outgoing_currency_value` → `need`. `trout` (the log tag for this term) is measured
NEGATIVE (inflow-signed) every single one of 29 quarters with a magnitude band that itself swings across
three orders of magnitude (`0-10k` / `10-100k` / `100-500k`) over the game — consistent with a spike-driven
term, though `trout`'s own band resolution (no exact-tick layer exists for it) cannot pin the swing to
THIS mechanism to the same certainty as the ruled-out commits were ruled out. This is presented as the
strongest traced mechanism given what's measurable, not as visually confirmed exact-value proof.

**Why this produces persistent (not oscillating) ~-10% deflation specifically:** `CURRENCY_amt_circulated_
deflation = (1 - private_cash_ratio)`, floored `min=0.001`, `divide=10` — structurally capped at ~10%
regardless of how far below 1 the ratio falls. §I.6/§I.9 already established `ratio` is pinned near-zero
most quarters (`ratio` exact values: 0.086, 0.071, 0.03, 0.013, 0.006, 0.006, ...0.024, 0.038 — never once
recovering near 1 after q0). A `need` inflated by episodic zero-stockpile price spikes (rather than
oscillating, since #112/#115 apply every quarter, not periodically) pins the ratio persistently low —
matching the reported symptom exactly (persistent -10%, not the old rail-to-rail oscillation).

**STATUS (superseded by I.11 below): #112/#115 named as leading suspect, pending adversarial review.**
§I.3/§I.4 are resolved: §I.3's `TRADE_national_expenditure` path was correct as the channel; §I.4's
`MONSTD_reconcile` mechanism is real but inert this boot (ruled out by direct log evidence, not by
priors). No fix attempted on any game file.

### I.11 (2026-08-12) — ADVERSARIAL REVIEW of I.10: mechanism CONFIRMED, "confirmed cause" label
### RETRACTED. Numerator-vs-divisor question unresolved; magnitude never measured.

An adversarial code-review agent checked I.10 point-by-point against the code, git history, and log.
**Everything mechanical in I.10 held up**: the full formula chain (payment → expenses →
`TRADE_national_expenditure` → `trade_wealth_outgoing` → `need` → `ratio` → deflation cap) is real and
file:line-verified; the #112/#115 diffs match; the zero-stockpile undivided-price behavior in
`GT_set_tradegood_price` is exactly as described; #75/MONSTD is correctly ruled out by log (0 hits on
`MONSTD_switch_backing`'s own log line against 61,400 `MONSTD_reconcile` entries); the file-set search for
alternative `need`-term movers was complete (`WEALTH_svalues.txt` had zero commits in range;
`country_population` is engine-provided, not moddable). The review also confirmed I.10 does NOT repeat the
§I.9 band-midpoint-multiplication mistake — it reads the price and stock bands separately, not as a
fabricated product.

**But three real gaps mean "confirmed cause" overclaimed what was shown:**

1. **(Highest) Numerator vs. divisor never separated.** `CURRENCY_trade_wealth_outgoing_currency_value =
   TRADE_national_expenditure / CURRENCY_wealth_value_1_unit` (CURRENCY_svalues.txt:965,967). I.10 blames
   the NUMERATOR (#112's per-zone price spike). It never ruled out the DIVISOR
   (`wealth_value_1_unit = country_unit_price_silver × units_to_the_lb`, `:234-278`), which #112/#115 do
   NOT touch and which §I.6 Fact 3 already showed settled to a persistently LOWER band this boot. A
   persistently low divisor inflates `need` every quarter by itself, with no spike required — and would
   look identical in the exact-tick data gathered so far, since `need` was measured but its two RHS terms
   (`TRADE_national_expenditure` and `wealth_value_1_unit` in this specific ratio) were not logged
   separately. This also matters because the SAME divisor scales `wealth_generated_country_as_currency_
   value` (`:739`), so a low divisor would inflate `need` through two terms at once, independent of #112.
2. **(High) Dominance/magnitude never measured.** No measurement shows silver expenses from 1-2 spiking CHI
   zones (upper_yangtzi/yellow_sea) are large enough, relative to the FULL national expenditure sum (16
   goods × every governorship), to swing the national `ratio`. `trout` (the log tag for this term) has no
   exact-tick layer — only a 3-decade-wide band — so this was always "consistent with," never demonstrated,
   and I.10 said so itself but still used the word "confirmed" in its status line.
3. **(Medium) An undiscussed damping mechanism.** `GT_split_scale_wealth_owed_and_order_size_tradegood`
   (se_GLOBALTRADE_split.txt:3542-3554) multiplies `wealth_owed_for_$tradegood$` by
   `global_supply_as_percentage_of_order_$tradegood$` when that fraction is `<1` — BEFORE it reaches
   expenses. Silver scarcity (the same condition causing the zero-stockpile spike) tends to make this
   fraction small, which would partly cancel the very spike I.10 relies on. Not addressed in I.10.

**STATUS: #112/#115 remain the leading, mechanism-verified suspect for the CHANNEL (the payment-price path
into `need`), but are NOT a proven cause of the specific persistent-low-ratio symptom.** The decisive
missing measurement, per the reviewer's recommendation: log `TRADE_national_expenditure`,
`CURRENCY_wealth_value_1_unit`, and `CURRENCY_private_cash_needed` as THREE SEPARATE tags for one boot. If
`TRADE_national_expenditure` is flat/small while `wealth_value_1_unit` sits low, gap #1 (the divisor, a
mechanism unrelated to #112/#115) is the real cause. If `TRADE_national_expenditure` swings in step with
the silver zero-stock quarters, #112/#115 graduates from suspect to confirmed. No fix attempted on any game
file; next step is this additional logging, not a fix.

### I.12 (2026-08-12) — LINE-LEVEL NARROWING of #112/#115 to ONE substitution; new EXACT logging added
### for `TRADE_national_expenditure` and `CURRENCY_wealth_value_1_unit` to close I.11's numerator-vs-
### divisor gap on the next boot.

**Line-level diff, read directly (not from commit-message prose).** Diffed the exact payment-site code
before #112, after #112, and after #115 (`se_GLOBALTRADE_split.txt`, `GT_split_update_wealth_owed_for_
tradegoods`):

- **Pre-#112 (baseline):** `multiply = owner.var:country_unit_price_$tradegood$`. `country_unit_price`
  (`:2803-2817`) reads `global_base_import_price_$tradegood$`, which is a WEIGHTED BLEND across all 22
  zones (`GT_split_get_global_import_unit_price_tradegood`, `:2585-2745`): each zone's `local_price` is
  multiplied by that zone's `percentage_of_global_stockpile` before summing. A zero-stockpile zone has
  `pct=0` (guarded `>0` at the percentage setter, e.g. `:1507-1518`), so its `local_price` — however
  spiked — contributes exactly 0 to the blend. This is the SAME dilution mechanism §E.5 already proved
  protects `gbip`; pre-#112 it protected the trade-payment price too.
- **#112's actual change (the incriminating line):** replaces the above with
  `value = global_var:global_$tradezone$_tradezone.var:local_price_$tradegood$  min = 0.0001  divide =
  {0.5 + owner.var:country_global_market_penetration_$tradegood$}`. This reads ONE zone's raw `local_price`
  DIRECTLY, with NO stockpile-share weighting at all — the dilution that protected the pre-#112 price is
  gone at this call site. The carried-over `min=0.0001` floor still guards the LOW side (a good is never
  free) but does nothing on the HIGH side, which is exactly where a zero-stock zone's price sits
  (`GT_set_tradegood_price`, `:6000-6032`, skips its divide-by-stockpile when stock is unset/≤0, so
  `local_price` = raw order count × 0.6, undivided). #112's own commit message says so: *"NO ceiling (user
  directive): a starved/spiking zone's price passes through in full."*
- **#115's change (divisor only, NOT implicated):** swaps only the divisor's `add` term from the national
  aggregate `country_global_market_penetration_$tradegood$` to the per-zone cached `TZ_penetration_
  $tradezone$`. Worst case `TZ_penetration=0` → divisor floors at `0.5` → price at most DOUBLES. No
  removal of a protection, no spike mechanism — #115's own text agrees ("floors gracefully... at most
  doubles the price — no spike, unlike the numerator's zero-stockpile case").

**Conclusion: `2b7142977` (#112) is the incriminating commit, specifically the single substitution of
undiluted per-zone `local_price` for the stockpile-weighted `country_unit_price` at this one call site.**
`7663239b1` (#115) rides on the same code but cannot independently produce an order-of-magnitude spike.

**This narrows the CHANNEL (§I.10/§I.11's #112/#115 mechanism) to one line, but does not resolve §I.11's
still-open numerator-vs-divisor question** — whether `trout`'s swing is actually driven by this channel's
spikes (the numerator, `TRADE_national_expenditure`) versus `CURRENCY_wealth_value_1_unit` (the unrelated
divisor, driven by `country_unit_price_silver × units_to_the_lb`). An interim read of the EXISTING coarse
band for the divisor (`wvuraw`, tag for `CURRENCY_wealth_value_1_unit`) shows it pinned at `>= 1` (an
unbounded-top band) for all 29 quarters of the current log — flat, suggestive that the divisor is NOT the
mover, but the band is too coarse to distinguish "flat at 1" from "swinging between 5 and 80," so this is
not decisive.

**New logging added (se_ECON_LOG.txt) to settle this on the next boot, not a game-file fix:**
- `ECON_LOG_curx_natexp` (new emitter, `:435-457`) — bands `TRADE_national_expenditure` directly (was
  previously unlogged; only its already-divided derivative `trout` existed). Wired into
  `ECON_LOG_curx_chain` immediately after `ECON_LOG_curx_trout`.
- `ECON_LOG_curx_wvu_raw`'s band ladder (`:810-826`) widened: the old top band ("`>= 1`", unbounded) could
  not tell 1 from 50 apart. Added `1-10`/`10-100`/`>=100` bands so a real swing at the high end is now
  visible even at band resolution.
- Exact-tick layer (`ECON_LOG_curx_exact`, `:725-782`) gained two new metrics: `wvuraw` (scale /500) and
  `natexp` (scale ×0.0002, since it runs into the millions — scaled DOWN, not up, to stay under the
  8000-tick cap). Both follow the existing proven `LABEL` → stage-value → `ECON_LOG_curx_tick_emit`
  pattern; no new idiom introduced.
- `tools/curx_analyze.py` updated to match: `natexp` added to `CHAIN` and given the same dual-line
  SIGN/abs handling `trout` already needed (confirmed `natexp` has the identical two-line-per-quarter
  shape); a `natexp(sign|abs)` column added to the CHI CURRENCY CHAIN table; `wvuraw`/`natexp` added to
  the EXACT VALUES table's `SCALE` dict and `exact_cols`. Verified: brace count in se_ECON_LOG.txt
  balanced (652/652), `curx_analyze.py` syntax-checked, tool re-run against the EXISTING (pre-dating this
  change) log — new columns correctly show `?`/`UNSET` with no crash, confirming the change is additive
  and non-regressive.

**STATUS: mechanism narrowed to one line in #112; magnitude/dominance question from §I.11 still open,
pending a fresh boot with the new `natexp`/`wvuraw` exact logging.** No fix attempted on any game file —
this section is logging + line-level analysis only.

### I.13 (2026-08-12) — REFUTED attempt to close §I.11 by reconstructing `wvuraw` from the EXISTING
### log without a fresh boot. An adversarial review killed the inference; genuinely unresolved.

Before waiting for a fresh boot with the new `natexp`/`wvuraw` logging (§I.12), tried to close §I.11's
numerator-vs-divisor question retroactively: `CURRENCY_wealth_value_1_unit` ("wvuraw") is algebraically
`country_unit_price_silver × 16 / units_to_the_lb`, and `country_unit_price_silver` ("agsilver") is
ALREADY exact-logged. CHI is `silver_standard` with `units_to_the_lb = 8` (`se_CURRENCY.txt:223`), so
`wvuraw = agsilver × 2`. Reconstructed across all 29 quarters of the existing log: `agsilver` ranges
0.548–1.590 (ratio 2.90×), so `wvuraw` ranges 1.095–3.180 (same ratio). Verified the reconstruction
formula (`agsilver = gbip/(0.5+pen)`) against already-logged `gbip`/`pen` — matched to within 0.0006 every
quarter, and confirmed `#112`/`#115` never touch this formula (they edit a different function entirely,
`GT_split_update_wealth_owed_for_tradegoods`, not `country_unit_price_silver`'s setter at
`se_GLOBALTRADE_split.txt:2803-2817`). From a 2.9× divisor swing being smaller than `need`'s ≥9.1× swing,
concluded the residual was better explained by the numerator (`#112`'s channel, `TRADE_national_
expenditure`) — i.e., that this strengthened rather than refuted the #112 diagnosis.

**An adversarial review (dispatched per standing practice before writing this into the audit) REFUTED
this inference, on grounds independent of the algebra (which the review confirmed correct):**

1. **The "2.9× is too small" comparison used the wrong model.** `need`'s formula has THREE terms, and
   TWO of them divide by `wvuraw`-derived quantities, not one: `trout` divides by `wvuraw` directly
   (`:967`); `wealth_generated` divides by `wvuraw` directly (`:739`); and `ess` — almost certainly the
   DOMINANT term — divides by `wvuscaled = wvuraw × reserve_ratio_impact` (`:692-694`, `:280-283`), where
   `reserve_ratio_impact` is itself a separate swinging, capped quantity. Treating `need` as if only
   `trout` carries a `1/wvuraw` factor understates the divisor side's real reach.
2. **The 16.0 display cap makes the whole residual argument unfalsifiable.** `need` sits AT the tool's
   display cap in 17 of 29 quarters (re-verified directly: `need` min 1.76, max 16.0, 17/29 capped). The
   TRUE maximum is unknown — could be 16, could be 1600. Computing "≥9.1×, therefore too big for a 2.9×
   divisor, therefore numerator" from a value whose true size is censored is circular: no divisor claim
   can be falsified against an unmeasured ceiling, and no numerator claim can be confirmed by it either.
3. **The simplest remaining explanation was sitting in the SAME probe output, unread.** `ess` and
   `wvuscaled` are BOTH already exact-logged by the identical CURXV layer used to reconstruct `wvuraw` —
   no algebra or reconstruction was needed to read them directly. Re-read directly (not reconstructed):
   `ess` ranges 20–87 (ratio **4.35×**, larger than §I.9's earlier ~4× estimate and than `wvuraw`'s 2.9×,
   though still short of `need`'s censored ≥9.1×); `wvuscaled` ranges 0.170–0.421 (ratio 2.48×). Neither
   alone closes the gap to `need`'s true (unknown) swing, but both were available all along and were not
   checked before reaching for the unmeasured numerator as the explanation. `CURRENCY_wealth_generated_
   country_as_currency_value` (`:734-739`, its own numerator `WEALTH_total_new_generated_governorship`)
   remains completely unmeasured and was not ruled out either.

**Self-correction on re-attempting the ess/wvuscaled read**: an initial pass divided `ess` by `wvuscaled`
AGAIN, double-counting the division `ess`'s own formula already performs (`CURRENCY_svalues.txt:690-694`:
`ess` = Σ12 prices ÷ `wvuscaled`, capped 32000 — `ess` IS the already-divided value, not a numerator still
awaiting division). Caught and corrected before writing this section; the 4.35×/2.48× figures above are
from `ess` and `wvuscaled` read independently, not combined incorrectly.

**RETRACTED: the claim that this reconstruction "strengthens" #112/#115.** It does not — it is neither
confirmed nor refuted by this analysis. What actually changed: the divisor's magnitude (2.9×, `wvuraw`)
and the dominant term's own magnitude (4.35×, `ess`) are now both known exactly from the EXISTING log
without a fresh boot; `need`'s true swing remains unmeasured past its 16.0 display cap; and `#112`'s own
channel (`natexp`) is STILL completely unmeasured, exactly as it was before this section. Nothing here
moves #112/#115 from "leading, mechanism-verified suspect" (§I.11's standing status) to anything stronger
or weaker.

**STATUS unchanged from §I.11/§I.12: no cause confirmed.** The decisive missing measurements remain (a) a
fresh boot exercising the new `natexp` exact logging, and (b) — newly identified by this section — raising
`ECON_LOG_curx_exact`'s hard tick cap (currently 8000, `se_ECON_LOG.txt`) or otherwise removing `need`'s
own display-cap censoring, since 17 of 29 quarters in the CURRENT log already can't be read past 16.0 and
a fresh boot would hit the identical cap on `need` again without that fix. No game file has been touched
in any diagnosis section to date.

### I.14 (2026-08-12) — NEW DIAGNOSIS: `need` swings at CONSTANT `ess` (a real control, not a
### reconstruction) in lockstep with `trout`'s band — AND a genuine, code-verified ordering bug found
### in the process. Pending adversarial review.

Per instruction, kept digging past §I.13's dead end. Two findings, one promoted, one demoted to scratch:

**Finding A (the diagnosis): a natural control the log already contains.** Instead of reconstructing an
unlogged quantity, searched the EXISTING exact-tick data for adjacent quarter-snapshot pairs where `ess`'s
tick count is IDENTICAL — i.e., cost-of-living genuinely did not move between the two reads, a real
zero-variance control, not an assumption. Found 13 such pairs across the 29-quarter log. In every one,
`need` still swings, and the swing tracks `trout`'s magnitude band moving, not `ess`. Sharpest example:

```
q5 POST: ess=64  need=16.000 (CAPPED, true value ≥16)  trout_abs_band=100-500k
q6 PRE:  ess=64  need=1.760  (EXACT, uncapped)          trout_abs_band=0-10k
```

`ess` is bit-for-bit unchanged (both read back exactly 64 ticks); `need` collapses from a censored ≥16
down to an exact 1.76 exactly as `trout`'s band drops two tiers. Since `ess` cannot be the mover here by
construction (it didn't move), and `need`'s other unmeasured term (`wealth_generated`) is a slow-moving
production/services quantity with no mechanism to flip this sharply between adjacent snapshots, `trout` —
i.e., `TRADE_national_expenditure` — is the best-supported mover for THIS pair, on direct log evidence,
not reconstruction. The same pattern (trout-band change ⇒ need swings; trout-band flat ⇒ need also moves
less, though not perfectly, since ess itself still varies in most other pairs) holds across all 13
constant-ess pairs (full table in `audits/SCRATCH_CURRENCY_23.md`).

**What this does NOT establish (checked before writing this up):** does not pin the swing to #112/#115's
specific mechanism (zero-stockpile zones). Tried to tie `trout`'s swings to `upper_yangtzi`/`yellow_sea`
silver order/stock bands directly and the correlation did NOT hold cleanly — `trout` sums across ALL
governorships and ~16 tracked goods, not just silver in two zones, so a single-good/single-zone story is
too narrow and was NOT forced into this section. This section establishes that `TRADE_national_expenditure`
genuinely drives `need`'s swing (confirmed, not reconstructed) — it does NOT yet re-confirm #112/#115
specifically as the source of THAT term's own swing (that still needs the fresh-boot `natexp` exact data
per §I.12, or a broader per-good/per-zone trace than attempted here).

**Finding B (structural, found while checking Finding A, NOT yet a proven cause of THIS symptom — logged
to scratch, not promoted): a real read-before-write ordering issue.** `quarterly_apply_trade_changes_and_
consume` (`oa_wealth_changes.txt:339-371`) calls `CURRENCY_update_amt_circulated` (`:355`, which reads
`CURRENCY_amt_circulated_balance` → `CURRENCY_trade_wealth_outgoing_currency_value` → `var:TRADE_national_
expenditure`) BEFORE the country-scope cache-write `set_variable { name = TRADE_national_expenditure
value = TRADE_national_expenditure }` (`:368-371`) that refreshes it for the quarter. So the currency
update at `:355` reads LAST quarter's cached `TRADE_national_expenditure`, not this quarter's freshly
computed value — a one-quarter lag. Checked via `git log -p` whether this ordering is NEW (a candidate
regression) or long-standing: it is long-standing, present across many historical revisions of this file
(oldest checked diffs already show `CURRENCY_update_amt_circulated` preceding the cache-write). A
long-standing lag cannot by itself explain a symptom that only appeared recently — same reasoning that
killed the earlier #50-revert hypothesis (§I.2) — so this is NOT promoted as a cause of the CURRENT
deflation symptom. Recorded because it is a real, independently-checkable defect regardless: it means
`CURRENCY_amt_circulated_balance` is always one quarter stale relative to trade, which could matter for a
FUTURE oscillation-timing question even if it isn't this bug.

**STATUS (superseded by I.15 below): "confirmed driver" claim RETRACTED after adversarial review.** No
fix attempted on any game file.

### I.15 (2026-08-12) — ADVERSARIAL REVIEW of I.14: REFUTED. The 13 "supporting" pairs mostly don't
### support it; two new confounds found (population, shared wvuraw divisor with wealth_generated); logging
### gaps closed for the next boot, no cause confirmed.

An adversarial review re-derived the full pair list independently and found the "confirmed" claim does not
survive:
- **Re-tally of all 14 constant-ess pairs** (13 promoted + 1 the review found, a within-quarter idx26→27
  pair — explains the 13-vs-14 discrepancy): only **2 of 14** (the headlined q5/q6 pair, plus one other)
  show a judgeable trout-band change moving with a judgeable need change. **5 pairs are CAP-CAP** (need
  reads the display-cap on BOTH sides) — zero evidence either way, yet were counted as "support." **6
  pairs have trout's band completely FLAT while need still swings by a large, uncapped amount** — by this
  section's own logic, a flat trout cannot be the mover there, which directly contradicts the "confirmed"
  claim in the majority of the dataset it was built from.
- **New confound found, not addressed in I.14:** `need`'s dominant term is `ess * country_population /
  4000` — TWO factors. `country_population` was never logged anywhere in this whole investigation (§I.6
  through §I.14). A population change between two snapshots is structurally indistinguishable, in the
  existing log, from the swing this section attributed to `trout`.
- **New confound found, a repeat of I.13's exact refutation:** `CURRENCY_wealth_generated_country_as_
  currency_value` (`need`'s third, ADDED term) divides by the SAME `CURRENCY_wealth_value_1_unit` divisor
  that `trout` divides by (`CURRENCY_svalues.txt:739` vs `:967`). A swing in that shared divisor moves both
  terms at once — exactly the confound I.13 was refuted for, re-imported here under a different name.
- **The "confirmed" language itself repeats a pattern already retracted four times in this document**
  (§E.7, §I.10→I.11, §I.13, now this section) — asserting a cause from a partial/self-selected read of the
  log rather than from a clean, closed measurement.

**Genuinely new, useful output despite the refutation: two real logging gaps identified and closed.**
`need`'s exact-tick scale (`se_ECON_LOG.txt`) was hitting its display cap (`need >= 16.0`) on 17 of 29
quarters, making its true magnitude unmeasurable — rescaled 500→50 (10x headroom) so the next boot can
read it. `country_population` (`poptick`) and `CURRENCY_wealth_generated_country_as_currency_value`
(`wealthgen`) added to the exact-tick layer, closing both confounds above for the next boot. `tools/
curx_analyze.py` updated to match (new `poptick`/`wealthgen` columns in the EXACT VALUES table).
**IMPORTANT:** `need`'s exact value from any log PREDATING this change will be mis-scaled 10x if read with
the current tool version — only trust `need`'s exact reading from a boot taken after this change.

Per user instruction (2026-08-12): the AUDIT doc should preserve the confirmed cause once found, not every
wrong guess along the way. §I.13's and this section's (§I.14) refuted reconstructions/inferences, and the
disproven #50/#74/#102/#106/#75 hypotheses, are recorded in full in `audits/SCRATCH_CURRENCY_23.md` — this
document keeps the chain of reasoning that is still LIVE plus a pointer to scratch, not a duplicate of it.

**STATUS: no cause confirmed. `need`'s true dominant driver remains genuinely unknown.** The decisive
missing measurement is now a fresh boot exercising ALL of: `natexp` (§I.12), `wvuraw` exact (§I.12),
`poptick`, and `wealthgen` (both §I.15) — the four quantities whose separate, simultaneous exact values are
required to attribute `need`'s swing to any one of its inputs without a confound. No fix attempted on any
game file.

### I.16 (2026-08-12) — DIAGNOSIS: `need`'s CENSORING REMOVED via algebraic back-solve from two
### ALREADY-uncapped exact-logged quantities (not a new probe, not a reconstruction of an unlogged
### quantity — arithmetic inversion of a formula already confirmed correct). Pending adversarial review.

§I.11/§I.13/§I.15 all hit the same wall: `need`'s exact-tick reading was CAPPED at 16.0 on 17 of 29
quarters in the existing log, and every argument built on "need's swing is >=Nx" was flagged as circular
against that censored ceiling. §I.15 fixed this for FUTURE boots (rescaled the probe 500->50), but that
doesn't recover the CURRENT log's censored quarters.

**The censoring is avoidable without a new boot.** `CURRENCY_private_cash_ratio` (`CURRENCY_svalues.txt:
753-765`) is `value = CURRENCY_amt_circulated_scaled  multiply = 0.004  divide = { value =
CURRENCY_private_cash_needed  min = 0.01 }` — i.e. `ratio = circ * 0.004 / max(need, 0.01)`. Both `circ`
(`CURRENCY_amt_circulated_scaled`) and `ratio` (`CURRENCY_private_cash_ratio`) are ALREADY exact-tick
logged (tags `circ` /10, `ratio` /1000) and NEITHER ever approaches its own tick-cap in this log (`circ`
max ~125 of an 8000-tick/10-scale = 800 ceiling; `ratio` max ~0.28 of an 8000/1000 = 8.0 ceiling — both
comfortably inside range every quarter). So `need = circ * 0.004 / ratio` recovers the TRUE, uncensored
`need` for every quarter, including all 17 previously-capped ones, using only already-logged, already-
uncapped numbers and the SAME formula CURRENCY_svalues.txt already defines (an algebraic inversion, not a
new assumption). Sanity check against the 12 quarters where the direct `need` reading was NOT capped: the
back-solved value matches within band/rounding noise every time (e.g. q0: direct 5.796, back-solved
5.814; q6: direct 1.760, back-solved 1.762) — confirming the inversion is correct, not merely plausible.

**Re-running the §I.14/§I.15 constant-`ess` comparison with the TRUE (uncensored) `need`, all 14 pairs
consistent, ZERO contradictions** (vs. 6 contradictions when §I.14 used the censored direct reading):

```
ess=61  q3P->q4P   need  37.85-> 82.00 (+44.15)  trout 10-100k ->100-500k (+1 band)  AGREE
ess=64  q5P->q6P   need  81.33->  1.76 (-79.57)  trout 100-500k->0-10k    (-2 band)  AGREE
ess=76  q7P->q8P   need   1.91-> 20.17 (+18.25)  trout 0-10k   ->10-100k  (+1 band)  AGREE
ess=87  q9P->q10P  need  20.00-> 12.63 ( -7.37)  trout flat                          AGREE (need still moves)
... (10 more pairs, all trout-flat, need moves in both directions — see below)
ess=35  q27P->q28P need  49.33->222.00(+172.67)  trout 10-100k ->100-500k (+1 band)  AGREE
```

**What this DOES establish (high confidence, arithmetic not statistical):** in every one of the 4 pairs
where `trout`'s band actually changes, `need`'s TRUE value moves in the same direction, including the two
biggest true-`need` swings in the whole log (+172.67 at q27->q28, -79.57 at q5->q6) — both trout-band-change
quarters. This is consistent with `trout` (i.e. `TRADE_national_expenditure`) being a real, correctly-
signed contributor to `need`, now checked against uncensored numbers.

**What this does NOT establish (the honest limit, stated up front so this isn't the same overclaim §I.14
made):** in the OTHER 10 constant-`ess` pairs, `trout`'s coarse band is flat while `need`'s true value
still swings substantially (e.g. q25->q26: trout flat, need 17.23->49.78, a +32.5 swing with NO trout-band
change to attribute it to). Since `trout` only has a coarse 6-tier band in this log (no exact tick existed
for it before §I.12), a flat BAND does not mean a flat trout VALUE — the swing in these 10 pairs could
still be `trout` moving within one band, or could be the two confounds §I.15 identified and just added
logging for (`country_population`, `wealth_generated`, which shares `trout`'s exact divisor). This section
cannot distinguish those possibilities from the CURRENT log — that requires the fresh boot with `natexp`
(trout's own exact numerator), `poptick`, and `wealthgen` all logged, exactly as §I.15 already concluded.

**STATUS: `trout`/`TRADE_national_expenditure` is a real, correctly-signed, arithmetically-confirmed
(not merely correlated) contributor to `need`'s swing in the 4 pairs where it's observable at all — this
is now demonstrated on true, uncensored numbers, a stronger basis than any prior section reached.** It is
NOT shown to be the DOMINANT or ONLY driver — 10 of 14 pairs show unexplained `need` movement with no
observable trout-band change, consistent with `natexp`/`population`/`wealth_generated` (or sub-band trout
moves) doing real work too. No fix attempted on any game file. Pending adversarial review before any
further conclusion.

### I.17 (2026-08-12) — ADVERSARIAL REVIEW of I.16: back-solve MATH confirmed sound (a genuine, kept
### methodological result); the CAUSAL claim about trout REFUTED as near-tautological. Also found: the
### pair construction itself is an artifact of the Finding-B cache-lag ordering, not independent evidence.

**Math verdict: SOUND, KEPT.** An adversarial review independently re-derived `need_true = circ*0.004/
ratio` from the source formula, re-parsed the log, and confirmed: the `divide = { min = 0.01 }` floor
never binds (true `need` never drops below 1.76, far above 0.01); `circ`/`ratio` never hit their own
tick-caps on any of the 29 quarters (verified directly — no `CAPPED` flag on either tag, ever); `ratio`,
`need`, `circ` are read from one synchronous, uninterrupted call (`ECON_LOG_curx_exact`) — no risk of
reading three different moments. All cited numbers reproduced independently. **This back-solve is a real,
useful, KEPT result: it recovers uncensored `need` for all 29 quarters, including the 17 that were capped,
using only already-logged data, and is immune to the /500-vs-/50 rescale confusion because it never reads
`need`'s own (rescaled) tick count at all.**

**Causal verdict: REFUTED.** Two independent problems, found by two independent routes:

1. **(Review) The "4-of-4 direction match" is close to tautological, not confirmatory.** `need` SUBTRACTS
   `trout`, and `trout` arrives ALREADY NEGATIVE (the documented double-negative, `CURRENCY_svalues.txt:
   952-960`, confirmed by `trout SIGN = NEGATIVE` on literally all 29 quarters). Subtracting a bigger
   negative number is mechanically `+|trout|` — so "trout's band grows ⇒ need grows" is close to a formula
   identity, not new evidence, whenever nothing else swamps it. With only 4 trout-band-change events in
   the whole log and a sign fixed by construction, "matches in 4/4" is a weak, small-sample result, not
   independent confirmation of causation or dominance.
2. **(This section, found while re-checking the ordering) The pair construction is itself an artifact of
   Finding B (§I.14), not an independent natural experiment.** `ECON_LOG_curx_dump_post` fires at
   `oa_wealth_changes.txt:365` — BEFORE the `TRADE_national_expenditure` cache-refresh at `:368-371` in
   the SAME on_action block. So every POST(N) reading of `trout` is stale (reflects quarter N-1's trade);
   the cache refreshes moments later; PRE(N+1) is the first read AFTER that refresh. Every one of the
   constant-`ess` pairs is a POST(N)→PRE(N+1) transition — i.e. every single pair straddles exactly one
   guaranteed cache-refresh landing, by construction of where the log markers sit relative to the
   cache-write, not because of any independent economic event. This means the "trout-band-changed" pairs
   are not 4 independently-arising coincidences to weigh against 10 independently-arising non-events; the
   whole 14-pair set was pre-selected to sit at the one moment `trout` is GUARANTEED to have a chance to
   change. This does not make the back-solve wrong, but it removes the "independent natural control"
   framing entirely — the control was measuring the mechanism Finding B already named, not testing it.

**STATUS: the back-solve (`need_true = circ*0.004/ratio`) is a confirmed, reusable diagnostic technique —
recorded and kept for future use on this or any future currency-chain question, no adversarial review
needed to re-derive it each time.** The causal question — which of `need`'s inputs (`trout`/`natexp`,
`country_population`, `wealth_generated`) actually drives the swing — remains UNRESOLVED after four
consecutive analysis attempts on this ONE existing log (§I.10/§I.13/§I.14/§I.16, all either refuted or
downgraded to "consistent with, not proof of"). **This is the actual, final finding of this analysis
phase: the existing log's temporal/aggregation structure — one dump before the trade cache-refresh, one
after, `ess`/`trout` visible only as coarse bands or a single per-quarter aggregate — cannot resolve this
question no matter how the existing numbers are recombined.** The only way forward that doesn't repeat
this cycle is the fresh boot already specified in §I.12/§I.15: `natexp`, `wvuraw`, `poptick`, `wealthgen`,
and the rescaled `need` (/50), ALL logged simultaneously in one boot, read with the back-solve technique
available as a cross-check. No fix attempted on any game file. No cause confirmed.
