# AUDIT — #23 currency period-2 oscillation (LIVE working doc)


> **[#16 2026-08-09] Tooling removed post-solve.** The forensic instrumentation this audit references — `tools/curx_analyze.py`, `tools/gen_econ_tzprobe.py`, `common/scripted_effects/se_ECON_LOG_TZPROBE.txt`, and the `ECON_LOG_curx_*` chain in `se_ECON_LOG.txt` — was STRIPPED once #23 landed (14c9ed899). Those file references below are historical; the code no longer exists. Regenerate from git history (this commit's parent) if the probe is ever needed again.


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
