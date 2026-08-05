# DESIGN — Amban + Garrison as full actors across the subject-integration chain

Consolidates the user's accumulated requirements (this session) into one buildable spec, so the
multi-event implementation is systematic and reviewable rather than option-by-option.

## Requirements (verbatim intent)
1. EVERY subject-integration event must involve the local amban AND garrison — not just .41.
2. Both the amban AND the garrison must be a **dedicated actor OPTION** in every event (not just a
   cost modifier or a flavour line) — mirroring the .41.d (amban) / .41.e (garrison) template.
3. The crush/force options cost **stability + legitimacy, never gold** (done for .41.b/.41.e).
4. Garrison-vs-subject strength: garrison cohorts vs subject **manpower ÷ 500** (1 cohort = 500 mp);
   levy strength is not script-readable, manpower is the chosen proxy (done in the resolver).
5. Garrison "marches out" is its OWN option (.41.e); the from-scratch war (.41.b) is separate and
   declares a real war (done).
6. War-declaration observer news must NOT fire at the declarer (done — se_FUNC exclusion).
7. **NEW:** the amban's performance/failure folds into the **Lifan Yuan (理藩院)** minister's Grand
   Council standing; the garrison's into the **Ministry of War (兵部)**. So using these actors well
   (or badly) in these events must move the relevant ministry-performance meter.
8. Amban behaviour is loyalty-banded: >70 staunch (negotiates), 40-70 steady, <40 / absent (flees).

## The resolver (SUBJ_QING_resolve_integ_actors) — already built, unchanged
Sets, per scope:target: integ_amban_present, scope:integ_amban, integ_amban_band (0/1/2),
integ_garrison_size (Σ CHI garrison cohorts on subject soil), integ_subject_size (subject manpower÷500),
integ_garrison_edge (0 subject-outweighs / 1 parity / 2 garrison-dominant). Every event calls it in
immediate; cleared at each option tail.

## Per-event options to ADD (gap map)
Template: amban option gated `integ_amban_present + band >= N`; garrison option gated
`integ_garrison_edge >= 1`. Each event keeps its existing base options; we ADD the two actor options
where missing, tuned to the event's situation.

| Event | amban option | garrison option |
|---|---|---|
| .10 unrest      | HAS (.10.d)        | ADD .10.e — garrison overawes the rising |
| .11 scandal     | ADD .11.d — amban investigates/arbitrates the graft locally | ADD .11.e — garrison seizes the corrupt official's assets by force |
| .12 strife      | HAS (.12.d)        | ADD .12.e — garrison separates the communities by force |
| .20 harvest     | ADD .20.d — amban channels the surplus into the local administration | ADD .20.e — garrison escorts/secures the grain (tuntian colony) |
| .21 festival    | ADD .21.d — amban hosts the investiture in the throne's name | ADD .21.e — garrison provides the ceremonial guard / show of force |
| .30 capstone    | ADD .30.d — amban oversees the bureaucratic handover | ADD .30.e — garrison enforces the incorporation on the ground |
| .40 decree      | HAS (.40.c)        | ADD .40.e — garrison backs the decree with a show of force |
| .41 resistance  | HAS (.41.d)        | HAS (.41.e) |

NOTE: for the POSITIVE events (.20/.21) the "garrison" and "amban" options are constructive, not
coercive (escort/ceremony/administration), so they cost little/nothing — the actor is still a real
choice, but the flavour fits a harvest/festival rather than a crush.

## Requirement 7 — actor performance folds into the GC ministries
- Each amban actor-option, on use, calls a small helper that nudges the **Lifan Yuan** perf meter
  (qing_min_perf_lifanyuan, se_QING_MINISTRY.txt) up (success) — and the "amban flees" branch nudges
  it DOWN. The amban IS a Lifan Yuan charge (理藩院 runs the ambans), so this is the natural coupling.
- Each garrison actor-option nudges the **Ministry of War** perf meter (qing_min_perf_war) — success
  up, a failed/bloody suppression down. The garrison is a 兵部 asset.
- VERIFY the exact perf-var names + the sanctioned nudge helper (QING_DECLINE_nudge or a ministry-
  specific setter) before wiring — do NOT invent a var. If a clean per-ministry nudge verb doesn't
  exist, this couples via the existing ministry recompute inputs instead.

## Build order (design → review → implement, small steps)
1. This note → your OK on the option matrix + the .20/.21 constructive framing.
2. Verify the Lifan Yuan / War perf-meter var names + nudge idiom (req 7) against se_QING_MINISTRY.
3. Implement the missing garrison options (.10.e/.11.e/.12.e/.20.e/.21.e/.30.e/.40.e) + missing amban
   options (.11.d/.20.d/.21.d/.30.d), each with loc, mirroring .41's proven shape.
4. Wire req-7 perf nudges into every actor option (amban→Lifan, garrison→War) + the flee branches.
5. Amban flee/negotiate consistency across all crush/force options.
6. Adversarial review of the whole batch BEFORE commit; stage only the named files.

## Open verification (before impl)
- OQ-A: **RESOLVED.** The meters exist and are the right hooks:
  - War 兵部 = `qing_min_perf_war` (se_QING_MINISTRY.txt:190, 0..100, 50=adequate), rebuilt by
    `QING_ministry_recompute_perf_war`; clamped 0..100 (lines 242-243).
  - Lifan Yuan 理藩院 = `qing_min_perf_lifanyuan` (:248+, 0..100), rebuilt by
    `QING_ministry_recompute_perf_lifanyuan` — and it ALREADY derives from amban coverage (how many
    Inner-Asian dependencies have a live amban posted, :254-263). So the amban→Lifan coupling is
    thematically pre-established; our event outcomes reinforce it.
  - CAVEAT: both meters are RE-COMPUTED wholesale each quarterly pulse from concrete state (roster
    coverage, garrison counts), not accumulated. So a raw `change_variable` nudge from an event would
    be OVERWRITTEN at the next recompute. Req-7 must therefore be wired as a PERSISTENT input the
    recompute reads — e.g. a decaying "recent amban success/failure" modifier var the perf-compute
    folds in — NOT a one-shot change_variable on the meter. Design the coupling as an input term, not
    a direct meter poke. (Confirm the recompute's fold structure at impl time and add the term there.)
- OQ-B: for the positive events, the garrison/amban options are framed CONSTRUCTIVELY (escort/ceremony/
  administration), so they read as fitting, not forced. User confirmed "every event".

## Requirement 9 (NEW) — amban negotiation is a SKILL CHECK, not auto-success
Loyalty gates whether the amban is WILLING to negotiate (band >= threshold → the option appears), but
his loyalty does NOT guarantee the negotiation SUCCEEDS. The outcome is a skill check on his
CHARISMA / FINESSE (the diplomatic skills): a skilled amban likely talks the chieftain down; an
unskilled one likely fails. **On FAILURE, the amban is EXECUTED** (death) — the negotiate option is a
genuine gamble, not a free de-escalation. Implement via a scored roll (e.g. weight success by
charisma+finesse vs a threshold, or a random_list whose success weight scales with the two skills);
apply the peace/rollback on success, and on failure kill the amban (death effect) + the rising
proceeds (fall through to the crisis continuing / a worse position). This replaces the current
auto-success .41.d / .10.d / .12.d amban options. Applies to the amban negotiate/mediate options in
EVERY event, not just .41. NOTE the coupling to req 7: a failed negotiation (dead amban) should hit
the Lifan Yuan perf meter harder than a mere non-attempt.

## Requirement 9b (NEW) — on amban-negotiation FAILURE, loop back to the SAME event minus the amban
When the negotiation skill-check (req 9) FAILS and the amban is executed, the event chain must
RE-FIRE the same event (re-trigger the same qing_integ.NN on scope:target) rather than resolving the
crisis. On the re-fire, the immediate re-runs SUBJ_QING_resolve_integ_actors — the amban is now dead,
so integ_amban_present is false and scope:integ_amban is gone, so the amban option(s) do NOT appear.
The player is returned to the same dilemma with the negotiation path removed (he gambled the amban and
lost him). Implementation: the failure branch of the amban option does `trigger_event = { id =
qing_integ.NN }` (re-fire self) after killing the amban, guarded against an infinite loop (the amban is
dead so the amban option can't be re-picked → no re-loop through the same failure; but confirm the
re-fire trigger still passes — the crisis is unresolved so it should). Applies to every event's amban
option, not just .41. NOTE: the re-fire must NOT re-run any one-time immediate side effects that would
double-apply (e.g. re-saving resistance_province is fine/idempotent; but any add_modifier in the
immediate would double — audit each event's immediate for re-entrancy before wiring the self-re-fire).

## Requirement 10 (NEW) — garrison march-out outcome is a COMMANDER SKILL CHECK
Parallel to req 9 (amban). When the garrison marches out (.41.e and the new garrison options in the
other events), the garrison strength/edge gates whether the option is AVAILABLE and how likely it is,
but whether the rising is crushed CLEANLY vs CHAOTICALLY depends on the GARRISON COMMANDER's MARTIAL
and ZEAL (the two military-leadership skills). A capable commander (high martial+zeal) breaks the
rising cleanly (small stability/legitimacy toll); a poor one wins but chaotically (larger toll, heavier
unrest, more war exhaustion, possibly the commander discredited). Implement via a scored roll on the
garrison commander's martial+zeal (find the commander from the garrison army on the subject's soil —
the resolver can save scope:integ_garrison_cmd alongside integ_garrison_size). This REPLACES the
current flat edge=2-vs-edge=1 clean/bloody split in .41.e (which used only relative strength) — keep
edge for AVAILABILITY/likelihood, use commander martial+zeal for the CLEAN-vs-CHAOTIC OUTCOME. Couples
to req 7: a chaotic suppression hits the War Ministry perf meter harder than a clean one.
NOTE the resolver must additionally save the garrison COMMANDER scope (not just the summed size) — add
scope:integ_garrison_cmd (the commander of the largest / a representative garrison army on the subject's
soil) so the outcome roll and the perf coupling can read his martial+zeal.

## ADVERSARIAL DESIGN REVIEW (2026-08-04) — VERDICT: NOT ready to implement as written
Six must-fix items before any of the ~11 options are built (review agent, high confidence):
1. **Base "force" options are ALREADY garrison-aware** (#task-8 pass): .10.a, .12.a, .30.c, .40.a
   already branch on integ_garrison_edge. So the proposed dedicated .10.e/.12.e/.30.e/.40.e would
   DUPLICATE them. Reconcile per event: either PROMOTE the garrison branch out of the base option into
   the dedicated option and STRIP it from the base, OR drop the dedicated option where the base carries
   it. Do NOT add on top.
2. **Manpower ÷500 proxy is miscalibrated → garrison options nearly never appear.** It compares a
   manpower STOCK (can be thousands) to a small garrison COHORT count with bands tuned for small
   numbers (delta≥4 dominant). Any subject with ~8000 manpower → subject_size 16 → needs ≥20 garrison
   cohorts for dominant → real banner garrisons never reach it → options hide. Yili "works" only
   because its 500-manpower rising → size 1; does NOT generalize. Recalibrate against the actual 1763
   subject-manpower distribution, or use a floored/capped measure or province-count instead.
3. **Req-7 fold must be self-expiring or explicitly decayed** (no unbounded accumulation — the
   no-restoring-drift ratchet rule). Use a `set_variable { days = N }` self-expiring flag folded as a
   fixed ± while present (idiom: qing_integ_coercive_absorption_flag days=730), NOT a bare
   change_variable add. ALSO note: the fold slots live inside the office-FILLED branch, so the coupling
   is INERT when the Ministry of War / Lifan Yuan seat is vacant (acceptable, but state it). Watch
   double-count vs the Lifan meter's existing amban-coverage (b) + amban-affinity (e) terms.
4. **Split "absent" from "wavering" for the flee flavor.** The resolver collapses both into band 0, so
   ".41.b: the resident flees his post" prints even when there was NEVER an amban. Gate flee on
   `integ_amban_present AND band 0`; genuinely-absent prints nothing/different. Also FIX the per-event
   band threshold inconsistency (.10.d/.12.d accept band≥1; .40.c/.41.d require band 2) with a stated
   rationale, or the "steady" band (40-70) is a hole (calms unrest but can't act on a rising, doesn't flee).
5. **Drop/re-scope .11.e** (the corrupt_official is a CHI COURT character, not on the subject's frontier
   soil — a garrison can't reach him; also duplicates .11.a's confiscation). **Downgrade .20/.21 actor
   options** from full dedicated options to flavor/cost-modifiers — the "constructive" framing is a
   rationalization (.20.e ≈ .20.a the harvest IS a tuntian; .21.e "show of force" is tonally opposite
   to a rou-yuan goodwill festival). This COLLIDES with req-2 ("dedicated option, not a modifier") —
   surface that collision to the user rather than ship hollow options.
6. Carry the .41 template invariants into every new option: `exists = scope:integ_amban` guard on any
   option touching that scope; keep one always-available ungated fallback per event; NO new option
   declares war / frees the subject (only .41.b does, via SUBJ_QING_crush_revolt_war + the se_FUNC
   observer-news exclusion) — new garrison options HOLD the subject.

Reqs 9 (amban skill-check + execution on fail) and 10 (garrison commander martial/zeal → clean vs
chaotic) were added AFTER this review and are NOT yet review-covered — re-review the revised design
(incl. saving scope:integ_garrison_cmd) before building.

## RESOLVED DECISIONS (2026-08-04, user-confirmed) — ready to build
The two forks that needed the user's call, plus the framing steer, are settled; the remaining
review must-fixes are resolved with the calls below.

- **R1 (garrison scope — was MF#1). User: "explicit garrison option (if the garrison exists) on
  ALL events, but it does not literally have to be marching out and killing people," and "a clear
  distinction between 'local garrison does X' (cheaper/more beneficial) and 'imperial troops are
  brought in to do X' (dearer)."** So the model per event is: the coercive/active action exists in
  TWO forms — the DEDICATED local-garrison option (gated `integ_garrison_edge >= 1`, cheaper /
  milder / more beneficial because the banner troops are already there) and the base "bring in
  imperial troops" option (always available, dearer). This IS review-MF#1's fix: PROMOTE the
  garrison branch OUT of each base force option into its own dedicated option, and STRIP the
  garrison discount from the base (the base becomes the pure "imperial troops brought in" path). For
  the POSITIVE events the local-garrison option is CONSTRUCTIVE, not martial: .20 = the garrison
  works/guards the tuntian (屯田 — the banner colonies literally farmed), .21 = the garrison provides
  the ceremonial guard of honour at the investiture. Per-event map:
  | Event | base "imperial troops brought in" | dedicated "local garrison does it" (edge>=1, cheaper) |
  |---|---|---|
  | .10 unrest   | .10.a bring in troops to crush (−5 stab)      | .10.e local garrison restores order (−3 stab, less resentment) |
  | .12 strife   | .12.a bring in Green Standard (+5 AE)          | .12.e local garrison separates communities (+3 AE, less blood) |
  | .30 capstone | .30.c bring in Green Standard to enforce (−5) | .30.e local garrison enforces incorporation (−3, milder) |
  | .40 decree   | .40.a force decree, resistance roll           | .40.e local garrison stands behind the decree → resistance far less likely |
  | .20 harvest  | (n/a)                                          | .20.e local garrison works/guards the tuntian (constructive: extra granary food) |
  | .21 festival | (n/a)                                          | .21.e local garrison provides the guard of honour (constructive: prestige/legitimacy) |
  | .41 revolt   | .41.b bring in a from-scratch expedition (independence war) | .41.e local garrison marches out, breaks it in the field (no war) |

- **R2 (execution scope — was req 9). User picked "Execute only in .41."** So: the amban
  negotiation in .41 (.41.d) is a charisma/finesse SKILL-CHECK and on FAILURE the amban is EXECUTED
  (death) + the event LOOPS BACK to itself minus the amban option (req 9/9b) — the loop-back is
  self-limiting because the death-cleanup hook (on_character_death clears qing_amban_here off the
  subject, se_QING_AMBAN.txt) means the re-fired resolver finds no amban, so the option cannot
  re-appear. In .10/.12/.40 the amban options are LIGHTER skill-checks: on failure the amban is
  DISCREDITED (loyalty + prominence hit, option spent) but NOT killed — execution for failing to
  calm routine unrest / smooth a decree is disproportionate; only facing down an armed rebel chieftain
  (.41) is mortal. .40's amban-smooth failure simply falls through to the ordinary decree resistance roll.

- **R3 (req 10 — garrison commander skill-check).** The resolver also saves scope:integ_garrison_cmd
  (commander of the largest garrison army on the subject's soil, via ordered_army order_by unit_size
  max 1). In .41.e (and only there — the other garrison options are single-outcome), the clean-vs-
  chaotic OUTCOME rolls on the commander's MARTIAL + ZEAL (garrison_clean_crush_chance_svalue): a
  capable commander breaks it cleanly (small toll), a poor one wins chaotically (larger toll). edge
  still gates AVAILABILITY; commander skill drives the OUTCOME (replaces the flat edge2-vs-edge1 split).

- **R4 (edge recalibration — was MF#2).** Keep manpower÷500 as the subject proxy (user: "just use
  manpower, 1 cohort = 500 manpower"), but recalibrate the bands to be SCALE-ROBUST via two scratch
  deltas compared to a literal 0 (RHS-literal rule): dominant (edge 2) iff garrison_cohorts ≥
  subject_size (delta = g − s ≥ 0); parity (edge 1) iff garrison_cohorts×2 ≥ subject_size
  (delta2 = 2g − s ≥ 0); else 0. So a garrison at least HALF the subject's manpower-pool-in-cohorts
  reads as parity and one matching it reads dominant — robust across the real 1763 manpower range,
  not tuned to Yili's 500-man special case.

- **R5 (req 7 — perf fold, was MF#3).** ONE self-expiring signed var per ministry, folded once in the
  office-FILLED branch of each recompute (inert when the seat is vacant — acceptable, stated):
  qing_lifan_recent_amban_outcome (amban success + / failure or death −−) and
  qing_war_recent_garrison_outcome (clean crush + / chaotic or failed −). Stamped via a small helper
  with set_variable { days = 730 } (self-expiring, the coercive-absorption-flag idiom), folded as a
  bounded fixed ±; NOT a change_variable poke on the meter (which the wholesale recompute would
  overwrite). No double-count vs the Lifan meter's existing coverage (b) + affinity (e) terms — this
  is a distinct "recent event outcome" term.

- **R6 (flee flavour split — was MF#4) + invariants (MF#6).** .41.b flee line: present+band0 = "the
  resident flees his post"; genuinely absent = no amban line. Every option touching scope:integ_amban
  guards `exists = scope:integ_amban`; every event keeps one always-available ungated fallback; no new
  option declares war or frees the subject (only .41.b, via SUBJ_QING_crush_revolt_war).

## STATUS: design RESOLVED and greenlit by the user — BUILDING now (task #27). Adversarial review of
## the finished batch BEFORE commit; stage only the named files.
