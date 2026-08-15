# DESIGN — #59 Revenue Minister performance should reflect subordinate-office squeeze, plus Opium

> STATUS 2026-08-13: DRAFT v3 — round-2 adversarial review complete, VERDICT: READY FOR
> IMPLEMENTATION. Round 2 independently hand-traced the sketch's arithmetic (confirmed 3 offices
> maxed at squeeze=100 correctly lands at exactly -10, matching sibling (e)'s rail), confirmed the
> Canton 0.7x weighting is applied at the right point (before the final divide), and stress-tested
> `K=27` against REALISTIC squeeze ranges (not just the theoretical max) — confirmed sensible,
> sibling-proportionate magnitudes at the seed baseline (30/30/30 -> -3.0) and moderate corruption
> (40-50 range -> -4.0 to -5.0), not just at the max. Two small MECHANICAL fixes required during
> implementation (not requiring another design round): (1) add a band-ladder `debug_log` on the
> new drag value before it's removed, since the doc's own ASSUMPTION constants (K=27, Canton 0.7x)
> need a boot-observable trace per this project's standing rule, and the sketch currently has none;
> (2) nest term (h) correctly INSIDE the "office FILLED" branch (immediately after (g)'s
> `remove_variable`, before that branch's closing brace) — the sketch's flush-left formatting
> doesn't show this, risking an implementer applying the drag even when the ministry is vacant.
> Both folded into the implementation sketch below. Round 2 also endorsed keeping Customs/Opium
> out of this task's scope (open question #4 resolved: 2a, not 2b — matching #51's own prior
> scoping precedent and this project's anti-scope-creep discipline).
>
> **Cross-reference, added after #62's round-3 review, SKETCH UPDATED after #62's round-4
> review**: `design/DESIGN_62_CUSTOMS_SQUEEZE_METER.md` (the Customs Inspector-General squeeze
> meter) depends on term (h) EXISTING before it can add its own `if` block — #62's round 3 found
> that a naive fixed-divisor retune (27→a larger constant) to accommodate a 4th office would
> silently weaken THIS doc's own already-verified 3-office magnitudes in the common case (Customs
> rarely/never appointed). #62's round 4 found that a PROSE-ONLY cross-reference note here (as
> this doc had until this fix) is not enough — an implementer who skims the note and copies this
> doc's own code sketch verbatim would still ship the flat `/27` and have to rework it later. **The
> sketch below is now updated to show the running-average scaffold directly** — the
> `qing_min_oversight_count` variable (seeded 0, incremented alongside each existing `if` block's
> drag accumulation, guarded divide via a scratch-var multiply, and removed at the end alongside
> its siblings `qing_min_oversight_drag`/`_scratch`) — so #59 ships the count scaffold for the
> original 3 offices, and #62's OWN implementation step only needs to add ONE more `if` block for
> Customs, not touch the divide/count machinery at all.
>
> **FINAL, after #62's round 5+6**: round 5 found one more precision bug in the running-average
> scaffold shown above — the count→scratch copy step used `change_variable` where every sibling
> reset line in the same block uses `set_variable` (zero precedent anywhere for `change_variable`
> paired with a bare `value =` key). Fixed in the sketch below. Round 6 confirmed the fix landed
> correctly and did a final fresh read of the whole document — **VERDICT: READY FOR
> IMPLEMENTATION**, no further rounds needed.

> Round-1 summary (superseded detail retained for history): round 1 independently
> re-verified every source citation (all confirmed accurate) and found one HIGH issue that
> reshapes the recommended implementation: `se_QING_CANTON.txt:137` documents that `#111a`
> explicitly RETIRED a `squeeze>=60 -> x0.7` CLIFF on this exact variable in favor of a
> continuous factor, specifically because a hard threshold was judged the wrong shape for
> grading office-holder graft. v1's Option B/C sketch proposed a NEW cliff at the SAME
> threshold, on the SAME variable, for a related purpose — reintroducing a pattern this
> codebase already tried and rejected. Fixed below by switching to a continuous shape. Round 1
> also found a MEDIUM asymmetry (Canton's squeeze already reaches the Minister's score through
> a second, indirect path via `qing_corruption_level` -> term (e), which Salt/Caravan lack) —
> resolved below with an explicit reduced weight for Canton rather than an unstated imbalance.
> Two open questions (independent-quantities framing, "same pulse" wording) were downgraded
> from open to resolved-as-accepted-tradeoff per round 1's judgment.

## Task text

User (this session, following #51's Customs rollup): "the squeeze on each of those 4 streams
should also reflect (negatively) on the Minister of Revenue's performance, and so should the
revenue/squeeze from the newly added opium commissioner."

## Ground truth (confirmed by a dedicated research pass, all citations verified in source)

### Term (g) today — `se_QING_MINISTRY.txt:902-922` (`QING_ministry_recompute_perf_revenue`)

```
902  # (g) [#431] TREASURY-INFLOW REWARD ...
911  set_variable = { name = qing_min_revenue_inflow  value = 0 }
912  if = { limit = { has_variable = qing_salt_income_last }    change_variable = { name = qing_min_revenue_inflow  add = var:qing_salt_income_last } }
913  if = { limit = { has_variable = qing_canton_last_state }   change_variable = { name = qing_min_revenue_inflow  add = var:qing_canton_last_state } }
914  if = { limit = { has_variable = qing_caravan_income_last } change_variable = { name = qing_min_revenue_inflow  add = var:qing_caravan_income_last } }
918  if = { limit = { has_variable = qing_customs_income_last } change_variable = { name = qing_min_revenue_inflow  add = var:qing_customs_income_last } }
919  change_variable = { name = qing_min_revenue_inflow  divide = 4 }
920  if = { limit = { var:qing_min_revenue_inflow > 15 } set_variable = { name = qing_min_revenue_inflow  value = 15 } }
921  change_variable = { name = qing_min_perf_revenue  add = var:qing_min_revenue_inflow }
922  remove_variable = qing_min_revenue_inflow
```

Reward-only, capped +15. No penalty side exists yet.

### Per-stream squeeze/corruption state (confirmed, NOT assumed)

| Stream | Squeeze var | Range | Mirrored from | Already reads/eases |
|---|---|---|---|---|
| Salt | `qing_salt_squeeze` | 0..100 | `qing_salt_seated.corruption` (`se_QING_SALT.txt:236`) | Yield-shave on `qing_salt_income_last` itself (`:152-153`); `QING_frontier_office_ease_squeeze` on rotate/picker (`:261`, `se_QING_FRONTIER_PICKER.txt:76`) |
| Canton | `qing_hoppo_squeeze` | 0..100 | `qing_hoppo_seated.corruption` (`se_QING_CANTON.txt:343`) | Yield-shave + siphon on Canton revenue (`:137-166`, `:326-337`); leaks into realm `qing_corruption_level` at `>=55` (`:360-367`); gates 3 Canton events (`:372-426`); eased on rotate/picker (`:529`, `se_QING_FRONTIER_PICKER.txt:104`) |
| Caravan | `qing_caravan_super_squeeze` | 0..100 | `qing_caravan_super_seated.corruption` (`se_QING_CARAVAN.txt:332`) | Yield-shave via lagged tmp (`:226-244`); siphon (`:317-326`); eased on rotate/picker (`:933`, `se_QING_FRONTIER_PICKER.txt:90`) |
| Customs | **NONE** | — | — | `se_QING_CUSTOMS.txt` tracks `qing_customs_efficiency`/`qing_customs_foreign_control` (institutional, not personal-corruption) with INVERSE polarity (higher foreign control -> LOWER realm corruption, `:217-221`). #51's own design doc already flagged this exact gap under "Follow-up, not built." |
| Opium | **NONE**, and no revenue stream either | — | — | Only `add_treasury = 40` exists (`se_QING_OPIUM.txt:424`), a ONE-SHOT treaty-legalization effect, not tied to the Commissioner and not a recurring published var. The file's own comments (`:308`, `:345`) state twice, explicitly, "this office carries no squeeze/graft meter." Opium's fiscal effect reaches the Ministry TRANSITIVELY today, through `qing_currency_stress` -> term (d) (`se_QING_MINISTRY.txt:875-881`), a completely different pathway than term (g). |

### The double-count risk (the key design hazard, confirmed via full grep of `qing_salt_squeeze`)

Squeeze is NOT currently read anywhere inside `se_QING_MINISTRY.txt` (zero hits). But it IS
already read inside each stream's OWN revenue computation, as a yield-shave BEFORE that
stream's income is published to the `_income_last` var that term (g) sums. Concretely: a high
`qing_salt_squeeze` already produces a SMALLER `qing_salt_income_last`, which already produces a
smaller reward in term (g), automatically. If a new penalty term ALSO subtracts directly from
`qing_min_perf_revenue` based on the same `qing_salt_squeeze` reading, the minister is punished
TWICE for the same graft: once via a smaller reward (correct, already happening), once via a
fresh, separate subtraction (new, and redundant with the first).

This must be resolved explicitly, not glossed over — see Design Decision 1 below.

### Coexistence with the existing squeeze-relief event (`qing_revenue.1`, se #46 this session)

`qing_revenue.1`'s Option A (reform) and Option B (milk it) both act on
`scope:salt_commissioner`'s real `corruption` character stat (via `QING_char_corruption`), NOT on
`qing_salt_squeeze` directly — specifically because a direct edit to the squeeze var would be
overwritten by `QING_salt_reconcile`'s quarterly mirror. This means any new penalty term built on
`qing_salt_squeeze` (etc.) automatically reflects `qing_revenue.1`'s outcome one quarter later, for
free, with no separate reconciliation code needed — the relief event and this task's new penalty
term already share the same upstream source and lag path.

## Design goals

1. Penalize the Revenue Minister for graft under his nominal purview, without double-counting
   graft that's already shrinking his reward via a smaller income figure.
2. Treat this as a DIFFERENT judgment than the office-holder's own consequences (the Salt
   Commissioner already suffers his own squeeze-gated crisis events; this is about whether the
   MINISTER is seen as failing to rein in his subordinates — a supervisory failure, not a restatement
   of the subordinate's own problem).
3. Don't invent state for Customs/Opium that doesn't exist — either build the missing meters
   properly (their own task-sized addition) or explicitly scope them out of THIS penalty term and
   log why, rather than silently reading a nonexistent var (which `has_variable` guards would make
   inert/silent anyway, but "silently does nothing" for 2 of 4 named targets is a bad shipped
   result if unflagged).

## Design Decision 1 — how to avoid double-counting (the central call)

**Option A (rejected)**: subtract `squeeze/K` directly for each of the 3 existing meters,
stacked alongside the existing yield-shave. Rejected: this is the double-count described above —
mathematically punishes the same graft number twice through two different channels feeding the
same score.

**Option B — flat cliff at squeeze>=60 (REJECTED, round-1 review, HIGH).** The original draft
proposed a flat `-3` per office whose squeeze crosses `>= 60`. Round-1 review found this
reintroduces a pattern this exact codebase already tried and explicitly retired:
`se_QING_CANTON.txt:137` (`#111a`) replaced "the old squeeze>=60 -> x0.7 CLIFF" with a continuous
factor specifically because a hard threshold was judged the wrong shape for grading office-holder
graft on this same variable. Proposing a NEW cliff at the SAME threshold for a related purpose
(Ministry-level judgment vs. yield-grading judgment) needs a stated reason to diverge from the
mod's own most recent design direction on this exact meter — none exists, so the cliff is
rejected.

**Option C (RECOMMENDED, revised) — a new term (h), continuous and NOT proportional to income.**
Keep term (g) exactly as-is (it already reflects lost REVENUE, correctly, via the post-shave
income figures). Add a separate, labeled term (h), "SUBORDINATE OVERSIGHT DRAG," matching this
function's existing one-term-per-concern convention (a)-(g). Term (h) is continuous like (d)/(e)/
(f) (`subtract meter/K`), NOT a cliff — but still deliberately NOT derived from the same income
figures (g) sums, so it remains a conceptually distinct quantity (lost REPUTATION/oversight-
failure) rather than a second read of the same lost-revenue signal. Shape, mirroring the existing
`/6`/`/10`/`/8` sibling drags in the same function:
```
subtract (squeeze_office_1 + squeeze_office_2 + squeeze_office_3_weighted) / K
```
where `K` is tuned so 3 offices simultaneously maxed at squeeze=100 lands in the same -10..-16
range as the existing (d)/(e)/(f) drags (proportionate magnitude, not the outlier the old flat
-3/-9 sketch was).

**Canton's asymmetric weight (round-1 review, MEDIUM, resolved).** Round 1 found Canton's squeeze
already reaches the Minister's score through a SECOND, indirect path today: `qing_hoppo_squeeze
>= 55` nudges the realm-wide `qing_corruption_level` (`se_QING_CANTON.txt:360-367`), which term
(e) of this SAME function already drags on (`corruption_level/10`). Salt and Caravan have no such
leak — they reach the score through term (g) only. Weighting all three offices identically in
term (h), as the original draft did, would make Canton triple-touched (g, e-via-leak, h) while
Salt/Caravan become double-touched (g, h) — an unstated imbalance. Resolved by giving Canton's
contribution to term (h) a reduced weight (e.g. Canton's squeeze term counts at ~0.7x vs Salt/
Caravan's 1.0x — best-guess, log under ASSUMPTIONS, boot-tune), rather than leaving the asymmetry
silent. This is a small correction in absolute terms (the corruption_level leak is diluted among
many other contributors to that counter) but should be stated, not glossed over.

**Accepted tradeoff, no longer an open question (round-1 review, LOW, resolved):** term (g)'s
lost-revenue reward and term (h)'s lost-reputation drag are not mathematically the same read (g
reads `_income_last`, h reads squeeze directly — different formulas, no shared variable read
twice with the same math), but both are still ultimately driven by the SAME root cause (the
office-holder's corruption stat). This is best understood as an intentional AMPLIFICATION of one
underlying signal viewed through two distinct lenses, not a coincidental double-count — accepted
as a deliberate design choice given the magnitudes stay proportionate to existing sibling terms
(checked: (d)/(e)/(f) max out at -16/-10/-12; term (h)'s tuned `K` should land in the same range,
not exceed it).

## Design Decision 2 — Customs and Opium

**Customs**: has NO squeeze meter to reuse. Two sub-options:
- **2a (recommended for THIS task's scope)**: exclude Customs from the new penalty term entirely,
  log this explicitly (not silently), and file it as its own follow-up ("build a
  `qing_customs_ig_squeeze` meter, mirroring the Salt/Canton/Caravan pattern") — matching how
  #51's own design doc already flagged the IG's-competence-doesn't-shape-`qing_customs_efficiency`
  gap as "a genuine gap... not built here."
- **2b**: build the Customs squeeze meter as part of this task, mirroring the proven 3-line
  pattern (seed at 30, mirror from holder's `corruption` on reconcile, ease on rotate) exactly as
  Salt/Canton/Caravan already do it. This is NOT large — the pattern is fully proven and would
  take roughly the same shape as the other three's ~3 call sites. Recommend 2b if the review finds
  reviewer bandwidth allows it in the same pass, since it closes the exact gap #51 already flagged
  and keeps all 4 streams symmetric — but do not let it block shipping the penalty term for the 3
  streams that already have the state.

**Opium**: has NEITHER a squeeze meter NOR a treasury-linked revenue stream comparable to the
other 4 — building both from scratch is a materially bigger lift than Customs (which only needs
the squeeze meter; its revenue stream already exists). Recommend: OUT of this task's scope
entirely. The user's own framing ("the revenue/squeeze from the newly added opium commissioner")
assumed parity with the other 4 that the research pass disproves — opium's fiscal effect already
has its own, different pathway into the Ministry score (term (d), via currency stress), which
arguably already IS "opium's effect on the minister's performance," just not through term (g)'s
mechanism. Recommend logging this finding back to the user rather than building new opium-revenue
plumbing under this task's umbrella — that would be a much larger, separately-scoped mechanic
(giving the Opium Commissioner his own direct treasury stream and corruption meter) than "add a
penalty term," and risks exactly the kind of scope-creep-disguised-as-a-quick-fix this project's
own rules warn against.

## Proposed implementation sketch (revised, round-2 review — arithmetic + calibration verified)

New term (h) in `QING_ministry_recompute_perf_revenue`, placed after (g), INSIDE the office-FILLED
branch (`se_QING_MINISTRY.txt:847-853`'s `if` block, same 3-tab depth as terms (a)-(g) — this
placement is load-bearing, not cosmetic: round-2 review flagged that a flush-left/un-nested sketch
risks an implementer applying the drag even when the ministry is VACANT, double-penalizing a state
that already floors to 25 with no minister to hold accountable). Continuous, not a cliff — mirrors
the existing (d)/(e)/(f) `subtract meter/K` shape. Canton weighted at 0.7x per the asymmetry
correction above. Round 2 hand-traced this exact sketch at squeeze=100/100/100 and confirmed it
lands at exactly -10 (matching sibling (e)'s rail), and at the real seed baseline (30/30/30)
lands at -3.0, and at moderate corruption (40-50 range) lands at -4.0 to -5.0 — proportionate to
siblings (d)/(e)/(f) at their own typical (non-maxed) magnitudes, not just at the theoretical rail.
Adds a band-ladder `debug_log` (round-2 review, MEDIUM: the sketch had none, leaving the two
ASSUMPTION constants unobservable on a boot — per this project's standing rule every best-guess
constant needs a boot-log line):

```
			# (h) [#59] SUBORDINATE OVERSIGHT DRAG — a minister who lets graft run unchecked under his
			# own purview pays a reputational cost distinct from the lost-revenue reward already
			# reflected in (g) (squeeze already shaves the raw income figures (g) sums; this is a
			# DIFFERENT quantity — oversight failure, not revenue loss — deliberately continuous like
			# siblings (d)/(e)/(f), NOT a cliff: #111a (se_QING_CANTON.txt:137) already retired a
			# squeeze>=60 CLIFF on this same meter for yield-grading, for the same reason a cliff is
			# the wrong shape here. Canton weighted at 0.7x since its squeeze ALSO leaks into
			# qing_corruption_level (term (e) above already drags on that), so an unweighted 1.0x
			# would triple-touch Canton relative to Salt/Caravan's double-touch. Customs and Opium are
			# deliberately EXCLUDED here — neither has a squeeze meter today (Customs) or a real
			# revenue stream at all (Opium); see design/DESIGN_59_REVENUE_SQUEEZE_PENALTY.md Decision 2
			# for the follow-up scoping. [ASSUMPTION 2026-08-13] K=27 and Canton's 0.7x weight are
			# best-guess, boot-tune-checked via the band log below.)
			set_variable = { name = qing_min_oversight_drag  value = 0 }
			# [DESIGN_62 dependency, sketch updated after #62's round-4 review] count scaffold
			# for the running-average divisor -- #59 ships this count var for the 3 offices below;
			# #62's OWN implementation step only adds ONE more "if" block for Customs (see
			# design/DESIGN_62_CUSTOMS_SQUEEZE_METER.md), touching neither this seed nor the divide.
			set_variable = { name = qing_min_oversight_count  value = 0 }
			if = { limit = { has_variable = qing_salt_squeeze }
				set_variable = { name = qing_min_oversight_scratch  value = var:qing_salt_squeeze }
				change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
				change_variable = { name = qing_min_oversight_count  add = 1 }
			}
			if = { limit = { has_variable = qing_hoppo_squeeze }
				set_variable = { name = qing_min_oversight_scratch  value = var:qing_hoppo_squeeze }
				change_variable = { name = qing_min_oversight_scratch  multiply = 0.7 }
				change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
				change_variable = { name = qing_min_oversight_count  add = 1 }
			}
			if = { limit = { has_variable = qing_caravan_super_squeeze }
				set_variable = { name = qing_min_oversight_scratch  value = var:qing_caravan_super_squeeze }
				change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
				change_variable = { name = qing_min_oversight_count  add = 1 }
			}
			# [DESIGN_62's Customs "if" block is added HERE by #62's own implementation step]
			if = { limit = { var:qing_min_oversight_count > 0 }
				# running average, not a fixed divisor -- [round-4 fix, DESIGN_62] the scratch-
				# var-then-divide form is doubly-proven in this codebase (se_QING_MINISTRY.txt:374
				# precedent); a nested "divide = { value=X multiply=Y }" form has no exact
				# precedent anywhere and was rejected for that reason.
				set_variable = { name = qing_min_oversight_scratch  value = var:qing_min_oversight_count }   # [round-5 fix] was change_variable; zero precedent anywhere for change_variable+value, every sibling reset line here uses set_variable
				change_variable = { name = qing_min_oversight_scratch  multiply = 9 }   # [ASSUMPTION] reproduces the original /27 at count=3 exactly (27/3=9); tuned so 3 offices maxed (100+70+100=270) lands at -10, matching sibling (e)'s -10 rail; boot-tune
				change_variable = { name = qing_min_oversight_drag  divide = var:qing_min_oversight_scratch }
			}
			change_variable = { name = qing_min_perf_revenue  add = var:qing_min_oversight_drag }
			# [round-2 review] boot-observable band ladder for the ASSUMPTION constants (×9 scale factor, Canton 0.7x)
			if = { limit = { var:qing_min_oversight_drag >= -2 }                                        debug_log = "IMP19C REVENUE oversight_drag >= -2 (low graft)" }
			else_if = { limit = { var:qing_min_oversight_drag >= -5 }                                    debug_log = "IMP19C REVENUE oversight_drag -2..-5 (moderate)" }
			else_if = { limit = { var:qing_min_oversight_drag >= -10 }                                   debug_log = "IMP19C REVENUE oversight_drag -5..-10 (high)" }
			else = { debug_log = "IMP19C REVENUE oversight_drag < -10 (severe)" }
			remove_variable = qing_min_oversight_drag
			remove_variable = qing_min_oversight_count   # [round-4 fix, DESIGN_62] third transient var, cleaned up like its siblings
			remove_variable = qing_min_oversight_scratch
```

(Customs term added only if Decision 2 picks 2b and the meter is built; Opium term omitted per
Decision 2's recommendation.)

## Open questions for round 2

1. **[RESOLVED, round 1]** Threshold shape — was flat cliff, now continuous per Decision 1's
   revision. `K=27` is a best-guess divisor (log under ASSUMPTIONS, boot-tune); round 2 should
   sanity-check the tuning math (3 offices maxed = -10, matching sibling (e)'s rail) rather than
   the shape question, which is settled.
2. **Player-experience redundancy (round-1 judgment: acceptable, but confirm in round 2).** Round
   1 found the Ministry-level drag and each office's own crisis-event gates are one-quarter
   LAGGED relative to each other (not literally simultaneous), and judged the redundancy
   acceptable — comparable to how term (e)'s corruption drag already coexists with other
   corruption-driving events elsewhere in the codebase without being treated as a problem. Round 2
   should confirm this judgment holds rather than re-opening it from scratch.
3. **[RESOLVED, round 1]** Independent-quantities framing — accepted as an intentional
   amplification of one root cause through two distinct lenses (revenue vs. reputation), not a
   coincidental double-count, given magnitudes stay proportionate to sibling terms.
4. Should 2b (build the Customs meter) actually be pulled into ITS OWN follow-up task rather than
   this one, given #51's own design doc already logged it as a separate, deliberately-deferred gap?
   Recommend keeping this task scoped to the penalty-term MECHANISM and NOT expanding it to also
   build new state for Customs — but log that recommendation for round 2 to override if it
   disagrees. (Round 1 did not weigh in on this question — still open.)
5. **New from round 1:** verify the `K=27` divisor and Canton's `0.7x` weight are the right
   calibration once round 2 has fresh eyes on it — these are the two new best-guess constants
   introduced by this revision and haven't been independently checked yet.
