# DESIGN — #51 (4th piece): fold Maritime Customs revenue into the Revenue office's performance rollup

> STATUS 2026-08-13: REVIEW ROUND 2 — CLEAN, ready to implement. Round 1 found a HIGH-severity scale
> defect in the original fix (folding the REAL post-currency-conversion treasury delta would
> permanently pin the term at its +15 cap, ~1000x the siblings' scale) and a false precedent
> citation. Revised: the fix now publishes the pre-conversion `thousands` input directly instead of
> snapshotting the real delta — a much simpler change (one unconditional set_variable line, no
> before/after diff, no branching) that also fixes the scale problem. Round 2 independently confirmed
> the customs value (~0-20/quarter) sits in the same order of magnitude as its three siblings, the
> fix reads the tmp var at a safe, unmutated point, and the Ministry-side add is correct.

## Task text
`#51`: "Surface Customs IG on Canton card, own title, 1:1 rule, Revenue perf rollup." Three of four
pieces are DONE and committed (`54cdd52ed`): the Inspector-General (IG) has a character-card title,
appears on the Canton Trade card, and is counted in the 1:1-audit. This design covers the 4th piece.

## Diagnosis (per Rule 1c — why the current state is what it is, traced before changing it)

`se_QING_MINISTRY.txt:902-918`, term (g) of `QING_ministry_recompute_perf_revenue` (shipped as #431,
"TREASURY-INFLOW REWARD"), sums three published quarterly income streams into `qing_min_perf_revenue`
(the Revenue Ministry's own accountability score, read by `QING_acc_score_office = { office = revenue
metric = treasury }`, `se_QING_ACCOUNTABILITY.txt:70`):
```
qing_min_revenue_inflow = qing_salt_income_last + qing_canton_last_state + qing_caravan_income_last
                           (each has_variable-guarded, summed, /4, capped at +15)
```
This term exists SPECIFICALLY so a minister who books real money on ANY of the state's revenue
streams is not punished because a DIFFERENT stream underperformed (#431's own stated rationale,
`:902-905`). Maritime Customs (`se_QING_CUSTOMS.txt`, shipped after #431) is a fourth, genuinely
real, on-books treasury stream — `QING_customs_pulse` (`:173-216`) grants quarterly revenue via
`CURRENCY_grant_country_wealth` — but it was never added to this sum, because at the time of #431
the Customs Service did not yet exist as a mechanic. This is a missed-follow-up gap, not a
deliberate exclusion (confirmed: no design doc or comment anywhere argues customs should be
excluded from the Revenue rollup; `design/DESIGN_QING_CROSSWIRING_ASSESSMENT.md:399` independently
flags "Fiscal Agents → Customs Superintendent" as an unrelated MEDIUM cross-wiring miss, corroborating
that this subsystem was integrated late and incompletely).

**A genuine SCALE mismatch, discovered by adversarial review — not the unit-purity concern this
design first assumed.** Salt/Canton/caravan each call `add_treasury = var:<x>_income_tmp` directly
with small numbers (the sum at `:912-916` is tuned "~+1 per 4 taels of combined take, capped at
+15" — i.e. the THREE combined are expected in roughly the 0-60 range per quarter). Customs instead
grants revenue via `CURRENCY_grant_country_wealth = { thousands = var:qing_customs_revenue_tmp }`
(`se_QING_CUSTOMS.txt:202`). **Review found the ACTUAL treasury amount that call adds is NOT close to
the other three streams' scale — it is roughly 1000x larger**: `CURRENCY_grant_country_wealth`'s main
branch multiplies the `thousands` input by `CURRENCY_wealth_value_1_unit_scaled_by_reserve_ratio_x1k`,
which is itself `×1000` (`CURRENCY_svalues.txt:286-290`), and `QING_customs_pulse`'s own comment
confirms the intended scale: "thousands = efficiency / 5, so up to ~20k at full efficiency"
(`se_QING_CUSTOMS.txt:195-197`) — i.e. up to ~20,000 real treasury units per quarter, not ~20.

An earlier draft of this design proposed snapshotting the REAL post-conversion treasury delta
(before/after `treasury` reads around the grant call) on the theory that this was the "unit-correct"
figure to publish. **Review correctly rejected this**: folding a ~20,000-unit real delta into a sum
tuned for a combined 0-60 range does not make the term "more generous," it makes it PERMANENTLY
PINNED at the `+15` cap every quarter forever — the term stops discriminating between a good and bad
Revenue minister at all, the exact opposite of #431's stated intent. The review's own insight,
adopted here: the PRE-conversion `thousands` INPUT (`qing_customs_revenue_tmp`, ~8-20 per quarter,
since `efficiency` is 0-100 and `/5` caps it at 20) is actually MUCH CLOSER in scale to the other
three streams' 0-60 combined range than the "unit-correct" real delta is — even though it is
technically a different currency-scale number (a `CURRENCY`-interface input, not a literal tael
count), using it as the customs contribution keeps the whole sum in the range the existing `/4`/`+15`
tuning was built for, which matters more here than unit-label purity for what is fundamentally a
heuristic accountability SCORE, not a literal ledger reconciliation.

**Corrected precedent citation (review finding): the earlier draft cited `se_SUBJECT_QING.txt:1213`
as a proven "before/after treasury diff" idiom. This was WRONG and is withdrawn** — that line is
actually a min-clamp (`set_variable = { value = treasury }` guarded on `treasury < qing_trib_amt_
svalue`, used to cap a tribute payment at what the payer can afford), not a diff pattern at all. No
such precedent exists in this codebase, but none is needed — the fix below does not require one.

## The fix — publish the pre-conversion `thousands` input directly (ASSUMPTION, boot-tune)

```
# [#51 2026-08-13] publish qing_customs_income_last for the Revenue Ministry's performance rollup
# (se_QING_MINISTRY.txt term (g)). Deliberately uses the PRE-conversion `thousands` value passed to
# CURRENCY_grant_country_wealth, NOT the real post-peg-conversion treasury amount that call actually
# adds (~1000x larger, per CURRENCY_svalues.txt's own x1000 scaling comment) — folding the real
# delta into a sum tuned for a combined 0-60 range across 3 streams would permanently pin the term
# at its +15 cap, defeating the whole point of a discriminating score. This keeps customs in the
# same rough order of magnitude as its siblings. OVERNIGHT ASSUMPTION — boot-tune against pop/econ
# logs like every other magnitude in this suite; if customs still visibly dominates or is inert
# relative to salt/canton/caravan on a real boot, retune the scale here, not the shared /4 divisor.
set_variable = { name = qing_customs_income_last  value = var:qing_customs_revenue_tmp }
```
This is a single new line, added right after the existing `set_variable = { name = qing_customs_
revenue_tmp ... }` / `change_variable = { ... divide = 5 }` pair (`se_QING_CUSTOMS.txt:198-199`),
BEFORE the existing `if = { limit = { var:qing_customs_revenue_tmp >= 1 } ... }` grant block
(`:200-204`), so it publishes unconditionally every pulse — including the near-zero case (efficiency
near 0), matching `qing_caravan_income_last`'s own "published even at 0" precedent
(`se_QING_CARAVAN.txt:272`, an unconditional publish outside its own `>0` guard). No snapshot, no
before/after diff, no interaction with `CURRENCY_grant_country_wealth`'s internal branches (main vs.
fallback) at all — this reads a value already fully computed BEFORE that call runs, so it is
identical regardless of which branch inside `CURRENCY_grant_country_wealth` fires. The existing
grant block, the corruption/reform check, and `QING_customs_apply_band` (`:206-215`) are all
UNCHANGED — this design adds exactly one line, no branching, no replaced block.

Then, `se_QING_MINISTRY.txt:912-914` gains a fourth guarded add:
```
if = { limit = { has_variable = qing_customs_income_last } change_variable = { name = qing_min_revenue_inflow  add = var:qing_customs_income_last } }
```
No other line in the existing sum changes — the `/4`, the `+15` cap, and the three existing guarded
reads are untouched. (The divisor stays `/4` rather than becoming `/5` to average four inputs — the
existing divisor is a TUNING constant that converts combined taels to a 0-15 point scale, per #431's
own "~+1 per 4 taels" framing, not literally "divide by the count of streams." Changing it would
rebalance the WHOLE term, including the three already-shipped streams, which is out of this design's
scope — a fourth revenue stream landing here should make the term MORE generous on average, which is
the intended, not-a-defect direction: more real revenue streams should be able to lift the minister's
score, matching #431's own "must not be punished because a different stream fell short" rationale
extended to a fourth stream.)

## Why this is the correct fold point (mirrors #431's own precedent exactly)

`QING_ministry_recompute_perf_revenue` is already the established "sum every real on-books revenue
stream" chokepoint for the Revenue Ministry's own accountability score — adding a fourth guarded
`has_variable` read, in the identical shape as its three siblings, is the minimal, idiom-consistent
fix. No new function, no new meter, no change to the `qing_accountability.1` event chain — crediting
one more input to the existing sum requires no downstream change at all.

**Self-caught scoping note, confirmed by review (item 3): `QING_acc_score_office = { office =
revenue  metric = treasury }` reads `QING_acc_metric_treasury` (`se_QING_ACCOUNTABILITY.txt:157-167`),
which reads bare country `treasury`/`has_monthly_income` — NOT `qing_min_perf_revenue`.** These are
TWO SEPARATE Revenue-office judgment systems that happen to share the word "revenue":
`qing_min_perf_revenue` (`se_QING_MINISTRY.txt`, the Ministry-panel performance score, #431's own
target) versus the Accountability challenge's own `QING_acc_metric_treasury` (a DIFFERENT, simpler
bare-treasury check that triggers the `qing_accountability.1` "minister called to account" event).
#51's task text names "Revenue perf rollup" specifically — matching `qing_min_perf_revenue` (the
"perf" in the name), NOT the Accountability metric, which already reads bare treasury and would
need its own, separate design if customs-awareness there is also wanted. **This design targets
`qing_min_perf_revenue` only, per the task's own literal wording; the Accountability metric is
explicitly out of scope** (folding customs into a SECOND, unrelated metric under a design meant for
the Ministry panel's own rollup would silently expand scope).

## What this does NOT touch
- `QING_acc_metric_treasury` / `qing_accountability.1` (the Accountability challenge chain) — reads
  bare `treasury`, not `qing_min_perf_revenue`; genuinely a different metric, out of scope per above.
- The three existing streams' own `_last` vars, their own pulse functions, or the `/4`/`+15` tuning
  constants in the existing sum — untouched.
- `qing_customs_efficiency`/`qing_customs_foreign_control` and the IG's own stat-to-efficiency
  coupling (there currently isn't one, beyond a one-time appointment nudge) — a real, separate gap
  (an ongoing IG-skill-feeds-efficiency term, mirroring the Hoppo→Canton `qing_canton_hoppo_factor`
  idiom, `se_QING_CANTON.txt:130-166`) but NOT what task #51's own wording ("Revenue perf rollup")
  asks for — logged as a candidate follow-up, not built here (see below).
- `QING_customs_pulse`'s efficiency-drift math, its band application, or its corruption/reform-
  pressure side effects — all untouched; only the revenue-grant block and one new published var.

## Follow-up flagged, not built (per no-silent-omission)
The IG's own competence (finesse/corruption, like the Hoppo) does not currently shape ongoing
`qing_customs_efficiency` the way the Hoppo's stats shape Canton's yield — only a one-time
appointment nudge exists (`QING_customs_appoint_ig`, `se_QING_CUSTOMS.txt:126-127`). This is a
genuine gap in the "official's skill matters" pattern this suite otherwise follows consistently, but
it is a DIFFERENT piece of work than "roll customs revenue into the Ministry's performance sum" —
task #51's literal wording is about the rollup, not the IG's ongoing stat-coupling. Not built here;
worth a future task if the IG's skill should matter turn-to-turn, not just at appointment.

## Blast radius
Two files. `se_QING_CUSTOMS.txt`: one new unconditional `set_variable` line, added before the
existing revenue-grant `if` block; nothing else in the file changes (the grant block itself,
efficiency drift, band application, corruption/reform side effects all untouched). `se_QING_
MINISTRY.txt`: one new guarded `change_variable` line, identical shape to its three siblings; the
divisor/cap and the three existing lines are untouched. No GUI change needed (the Ministry panel
already displays whatever `qing_min_perf_revenue` computes to; crediting one more input requires no
panel change, matching #431's own "no panel change needed" precedent when it added the caravan
stream).

## Also confirmed by review (ordering, not a defect)
`QING_ministry_recompute_all_perf` runs at governance-pulse step 0 (`se_QING_GOVERNANCE.txt:218`);
`QING_customs_pulse` runs at step 6 (`:309-312`) — so the Ministry's recompute reads customs' PREVIOUS
quarter's value, a one-quarter lag. This is NOT a new problem this design introduces: salt
(`QING_revenue_pulse`, step 16), Canton (`QING_canton_pulse`, step 17d-iii), and caravan
(`QING_caravan_pulse`) all ALSO pulse after step 0, so all four streams already share this identical
one-quarter lag — customs behaves exactly like its three siblings, not differently. On the first
post-establishment tick the `has_variable = qing_customs_income_last` guard fails cleanly (contributes
0, no crash) until the var is first published.

## Open questions for review
1. Is `qing_customs_revenue_tmp` (~8-20 per quarter at typical efficiency) really the right scale
   to sum against `qing_salt_income_last`/`qing_canton_last_state`/`qing_caravan_income_last`
   (combined tuned for 0-60), or does it still under/over-weight customs in a way that needs its own
   scaling factor rather than a raw pass-through? This design's own "publish the CURRENCY-interface
   input value directly" choice is itself an ASSUMPTION (see the code comment) — a real boot's econ
   logs are the only way to confirm the four-stream sum lands where #431's "~+1 per 4 taels, capped
   at +15" intent expects, not a per-stream guess.
2. Should the `qing_customs_income_last` var also be surfaced on the Revenue Ministry panel as its
   own ledger line (mirroring how salt/Canton/caravan each have a visible panel line), or is feeding
   it silently into `qing_min_perf_revenue` sufficient for what #51 asks? Task #51's wording ("Revenue
   perf rollup") suggests the rollup itself is the ask, not a new panel line — this design does NOT
   add a panel line, treating that as a separate, smaller follow-up if wanted.
