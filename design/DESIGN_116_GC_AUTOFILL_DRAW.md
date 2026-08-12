# DESIGN — #116 enforce create_character rule on GC autofill

> STATUS 2026-08-11: FIRST PROPOSAL REVIEWED — NOT CLEAN. See "## REVIEW FINDINGS (2026-08-11)" appended
> at the bottom for the full verdict. One CRITICAL finding (the draw must anchor on
> `scope:qing_autofill_country`, not `ROOT` — the proposal as originally written is inert or
> crash-adjacent on the exact runtime-backfill path #116 targets) plus several HIGH/MEDIUM
> underspecifications. Do not implement the "## Proposed resolution" section below as originally
> written — it needs the corrections listed in the review findings first, then a re-review.

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:61`: "#116 enforce create_character rule across GC positions
(only exams may create_character to fill seats)."

## Scope
The ONLY site under "GC positions" that is both (a) a create_character mint and (b) a **deliberate**
reversal away from draw-first is `QING_council_autofill_office` (`se_QING_COUNCIL.txt:168-215`), called
13 times per autofill pass (once per office, `:80-92`) and again on runtime vacancy backfill
(`QING_office_vacate_dispatch`, `:1741-1753`). Every OTHER create_character site surveyed
(se_QING_DELIBERATIVE/HOUSEHOLD/GUARD/SUBPOSTS/SOUTHERNSTUDY/UPPERSTUDY) already carries its own
dated, deliberate mint rationale unrelated to this task — not in scope.

## Why this is not a simple #111/#113/#114-pattern re-application

Commit `578ea7f89` ("Qing appointment redesign", 2026-07-22) deliberately reverted
`QING_council_autofill_office` FROM a draw (`ordered_character` + `limit = { QING_office_eligible_candidate
= yes }`) TO create_character, because the draw caused a "double-booking mess (autofill running more than
once, or grabbing minted/court characters, seated men who were or later became diplomats/censors/
commanders)."

`QING_office_eligible_candidate` (`qing_dynasty_triggers.txt:168-225`) has accumulated real hardening
since then (BT-50 army/navy exclusion, BT-7 officer-marker exclusion, BT-L harem exclusion, #47
hard-disgraced exclusion) — but its comment at `:172-176` says explicitly: **"AUTOFILL no longer uses
this gate... a current office-holder REMAINS an eligible candidate here"** — deliberately, because this
trigger now also feeds the MANUAL reshuffle pickers, where offering a sitting minister as a candidate for
a DIFFERENT seat is the intended "Replace" behavior (`QING_office_appoint`'s one-office-per-man logic
relieves his prior seat automatically, `:1493-1504`).

**#118 (`qing_current_post`, shipped this session, `6454a50cf`) does not close this gap.** It is a
structural cleanup/dispatch var (stamped by `QING_post_stamp`, read by `QING_post_dispatch_vacate`'s
11-branch chain) that guarantees a man relieved of post A has post A's teardown correctly dispatched when
he takes post B — it does NOT add any NEW eligibility exclusion. It does not appear anywhere in
`QING_office_eligible_candidate` or in `QING_char_holds_court_position`'s marker OR-set (only
`qing_is_xj_beg` was newly added there, for an unrelated reason).

**The concrete failure mode if `QING_council_autofill_office` is naively converted to draw-first using the
existing `QING_office_eligible_candidate` trigger:** `QING_council_autofill` calls the office-filler 13
times in strict sequence in one pass (`:80-92`). Each call's `ordered_character` ranks the WHOLE eligible
court by `combined_stats_council_svalue`. Since the trigger deliberately does not exclude current
GC-office holders, the single ablest man in the realm could be selected AGAIN by office #2's draw, even
though office #1 already appointed him one call earlier in the same pass — `QING_office_appoint`'s
one-office-per-man relief would then silently vacate office #1 to fill office #2, and office #1's autofill
call (already run, already returned) never re-fires to notice or backfill. Net effect after the 13-call
pass: fewer than 13 offices filled, with no error, no log flood, nothing indicating the shortfall — exactly
the "double-booking mess" `578ea7f89`'s commit message names, just re-introduced via the more-inclusive
eligibility gate that came later for a different purpose.

## What would need to be resolved before implementation

An autofill-SPECIFIC eligibility gate, distinct from `QING_office_eligible_candidate` (which must keep
including current holders for the manual-reshuffle callers), that additionally excludes anyone who
ALREADY carries `qing_office_held` (or, now that it exists, `qing_current_post`) — i.e. "eligible for
autofill" = "eligible for manual reshuffle" MINUS "already holds any post right now." This is a new
predicate, not a reuse of an existing one, and needs its own review before being wired into 13 sequential
calls in one pass.

Whether the confer-else-create fallback shape (mint only when the narrowed draw finds nobody) is still
correct for autofill given that early game start has ~13 seats and a much smaller court than the exam
pool ever assumes — i.e. whether the draw would realistically find 13 DISTINCT eligible men at day-32
autofill, or whether the fallback mint would fire for most/all of them anyway (in which case the "enforce
create_character rule" task may reduce to "add a draw attempt that usually no-ops," which is honest but
worth stating up front rather than discovering after implementation).

## Recommendation
Do not implement #116 against the existing `QING_office_eligible_candidate` trigger. Design the
autofill-specific exclusion first, run it through an adversarial design review (per the project's
diagnosis → design-review → implement → code-review gate sequence used for #111/#113/#114), THEN
implement.

## Proposed resolution (candidate — NOT reviewed, do not implement yet)

`QING_council_autofill_office`'s 13 calls within one `QING_council_autofill` pass run strictly
sequentially, not concurrently, and `QING_office_appoint` (called at the end of a successful draw)
stamps `qing_office_held` and, per #118, `qing_current_post` SYNCHRONOUSLY before returning. So a
candidate draw for office N+1 that queries the court AFTER office N's `QING_office_appoint` has
returned should already see office N's man as marked — there is no genuine same-tick race between
separate calls, provided the exclusion check reads a marker `QING_office_appoint` actually sets.

Candidate design:
1. Add a new `ordered_character` draw inside `QING_council_autofill_office`'s vacant-seat branch,
   BEFORE the existing `create_character` fallback, using a gate built from
   `QING_office_eligible_candidate`'s exclusions PLUS an additional
   `NOT = { QING_char_holds_court_position = yes }` (the canonical "already holds ANY court post"
   trigger, which includes `qing_office_held` in its OR-set) — NOT reusing
   `QING_office_eligible_candidate` unmodified, since that trigger deliberately keeps current
   office-holders eligible for the manual-reshuffle callers.
2. Require `has_trait = $degree$` on the draw (the same degree the create_character fallback already
   grants), so office/degree congruence holds on both the draw and the mint path.
3. Guard the draw's result with the same stale-scope idiom #111/#113/#114 use
   (`exists = scope:X` AND `scope:X = { NOT = { QING_char_holds_court_position = yes } }`) before
   calling `QING_office_appoint` on it, since this effect is called 13 times per pass and the saved
   scope is not reset between calls — a barren round must not re-read an earlier office's already-
   appointed man out of a stale scope.
4. Fall back to the existing `create_character` mint only when the guarded draw does not yield a
   fresh match.

Open questions this candidate does NOT yet resolve and a reviewer should probe:
- Does `QING_office_appoint`'s marker-stamp genuinely commit before the NEXT `QING_council_autofill_office`
  call's `ordered_character` runs, or could Imperator's effect-execution model defer/batch state
  changes within one country_event's `immediate` block in some way that reopens the race? (Diagnosis
  so far has ASSUMED strict sequential commit; this must be verified, not assumed.)
- Realistic draw-pool size at day-32 autofill: is `has_trait = $degree$` (jinshi for 11 offices,
  wu_jinshi for 2) ever satisfiable by more than a handful of seeded characters before the exam
  cohort/pool-refill mechanics (#111) have run even once? If the draw realistically never fires at
  boot, is a permanently-no-op draw+fallback still "enforcing the rule," or does it need a different
  shape for the boot-autofill case specifically vs. the later runtime-backfill case
  (`QING_office_vacate_dispatch`, which runs much later in a game with a populated exam pool)?
- Interaction with #117 (GC eligibility should check exam degrees) if that ships first: a degree
  filter on the picker would shrink the same-tick draw pool further — does that help or hurt this
  design's soundness?
- Does the `combined_stats_council_svalue` ranking on the draw need the same `qing_degree_prestige_svalue`
  weighting the exam-drawn sites use, or is a hard `has_trait` filter sufficient without a soft
  preference term (this doc leans hard-filter; #117's own diagnosis leaned soft-preference for its
  analogous case — reconcile or justify the difference)?

## REVIEW FINDINGS (2026-08-11)

Adversarial design review of the "## Proposed resolution" section above returned **NOT CLEAN**. The core
safety claim (point 1's precondition — `QING_char_holds_court_position` really does include
`qing_office_held`) was CONFIRMED correct. Everything else below needs fixing before re-review.

**Finding 1 (CRITICAL) — the draw must anchor on `scope:qing_autofill_country`, never bare `ROOT`.**
`QING_council_autofill_office` runs in TWO scope contexts: the day-32 boot autofill (ROOT = CHI) AND
`QING_office_vacate_dispatch`'s runtime backfill (reached from `on_character_death` /
`QING_justice_strip_for_trial`, where **ROOT = the dying/accused character, not CHI** — the existing
code already warns about this at `se_QING_COUNCIL.txt:169-176` and saves `this` to
`scope:qing_autofill_country` specifically to avoid it). The proposed resolution's step 1 says to build
the gate from `QING_office_eligible_candidate`'s exclusions — but that trigger is hardcoded to bare
`ROOT` (`employer = ROOT`, `ROOT.current_ruler`, `ROOT.primary_heir`) and cannot be reused verbatim; an
implementer copying it by habit gets a draw anchored on a dead character on the backfill path. This is
the SAME class of bug that shipped inert on the sibling #80/#82/#84 picker task this session
(`overnight/SESSION_HANDOFF_2026_08_11.md:28-29`, "CRITICAL ROOT-vs-employer scope bug that would've
shipped the picker inert"). **Fix:** every country-relative check in the draw's gate must read
`scope:qing_autofill_country` (`employer = scope:qing_autofill_country`,
`scope:qing_autofill_country.current_ruler`, `scope:qing_autofill_country.primary_heir`), never `ROOT`.

**Finding 2 (HIGH, consequence of Finding 1) — unfixed, the draw is inert on the exact path #116 targets.**
If the draw is anchored on `ROOT` and ROOT is the dead minister on the backfill path, `employer = ROOT`
matches nobody (no living CHI courtier is employed by a corpse) — the draw always falls through to
create_character, i.e. the mint fires on every death-backfill exactly as it does today. The boot-pass
mint may not even be a rule violation (see Finding 4); the backfill mint is the actual violation #116
exists to close, and Finding 1 left unfixed defeats it entirely on that path.

**Finding 3 (HIGH) — the gate composition ("PLUS `NOT = QING_char_holds_court_position`") is ambiguous
and, read as a substitution rather than an addition, reopens BT-50.** `QING_char_holds_court_position` is
a fixed OR-set of court-post MARKER VARS only — it does NOT include `is_governor`/`is_general`/
`is_admiral` (confirmed: #111's own review added those three separately for exactly this reason). If an
implementer reads step 1 as "use `QING_char_holds_court_position` instead of the eligible-candidate
exclusions" rather than "in addition to them," the draw could pull a serving army/navy commander or
governor into a Grand Council seat — the precise symptom `QING_office_eligible_candidate` was built to
close. **Fix:** the design must enumerate the full gate concretely rather than describing it by
reference: `is_ruler = no`, `is_general = no`, `is_admiral = no`, `is_governor = no`, not-primary-heir,
harem/officer-marker/hard-disgraced/vanilla-office exclusions, PLUS `NOT = QING_char_holds_court_position`,
PLUS `has_trait = $degree$` — all re-anchored per Finding 1.

**Finding 4 (MEDIUM) — the martial-seat draw (war, guard_commandant) is a near-permanent no-op; this
must be an explicit, acknowledged limitation, not a silent outcome.** Verified counts: the setup seed
(`setup/characters/00_Qing.txt`) has 23 `jinshi` characters and ZERO `wu_jinshi` at boot; the only
boot-time wu_jinshi grant targets serving generals/admirals and the sitting War/Guard holders — men the
draw's own `is_general`/`is_admiral = no` gate excludes, or the very seats being filled. A hard
`has_trait = wu_jinshi` filter finds essentially nobody for these 2 seats for a long stretch of the
game. **Fix:** state this plainly before implementation and decide deliberately — accept the near-no-op
(document it) or use a soft-preference weight instead of a hard filter for the 2 martial seats
specifically, and reconcile with #117 (which independently reached the same hard-vs-soft tension).

**Finding 5 (MEDIUM) — the design conflates the boot-pass and backfill call contexts and aims its
heaviest machinery (the stale-scope guard) at the context that least needs it.** The elaborate
stale-scope guard is justified by "13 calls per boot pass, scope not reset between them" — but (a) the
boot-pass mint is plausibly the SANCTIONED boot seed under the existing character-creation rule (create
is permitted at "the game-start boot seed"), so it may not be a violation requiring a draw at all; and
(b) the backfill call (the actual violation) runs ONCE, where the 13-in-a-row stale-scope hazard never
arises (the guard is harmless-but-inert there). **Fix:** state explicitly which call context is in
scope. If the boot mint is sanctioned, scope #116 to the backfill path only and drop/simplify the
stale-scope guard accordingly; if not, justify draw-first for the full 13-seat boot pass too.

**Finding 6 (LOW) — the "same proven stale-scope guard idiom as #111/#113" claim is inaccurate (though
the variant used happens to be correct).** The cited idiom keys its guard on the effect's OWN
just-stamped marker, set by a direct `set_variable` inside the same effect body. This design instead
keys the guard on `QING_char_holds_court_position`, stamped INDIRECTLY via `qing_office_held`, set
inline by `QING_office_appoint` at the end of a successful branch — a different (and still-correct, per
the review's independent confirmation of same-frame commit ordering) shape. **Fix:** describe the guard
accurately and record its dependency on `QING_office_appoint`'s synchronous `qing_office_held` stamp,
rather than claiming verbatim reuse of the cited precedent.

**Finding 7 (LOW) — `QING_exam_fill_first_vacant_from_pool` (`se_QING_EXAM.txt:807-834`) is an existing,
unmentioned "fill a vacant office from existing men" path** (pool-scoped, degree-agnostic, wired only to
`qing_keju.6` and a Hanlin GUI button). Not redundant with this design's proposed draw, but the design
should acknowledge it so the mod doesn't end up with two divergent fill-from-existing behaviors.

**Confirmed sound (no fix needed):** the same-execution-frame commit assumption (point 2's open
question) — three shipped, reviewed-clean precedents establish that a character-scope `set_variable`
from one sequential sub-call is visible to a later sequential sub-call's `ordered_character` limit in
the same execution frame, for DRAWN pre-existing characters (does not apply to a same-tick
create_character'd character, which this design doesn't need).

**Disposition:** revise per Findings 1-5 (the LOW findings are polish), then dispatch a fresh design
review before implementation.

## CORRECTED PROPOSAL (2026-08-11) — resolves Findings 1-5

**Scope decision (Finding 5):** #116 is scoped to the RUNTIME BACKFILL path only
(`QING_office_vacate_dispatch` → `QING_council_autofill_office`, reached from `on_character_death` /
`QING_justice_strip_for_trial`). The day-32 BOOT autofill pass is treated as the sanctioned boot seed
under the existing character-creation rule ("create_character permitted at the game-start boot seed")
and is left untouched — it keeps minting unconditionally, exactly as it does today. This means the
elaborate 13-calls-in-one-pass stale-scope guard from the original proposal is UNNECESSARY: the backfill
path calls `QING_council_autofill_office` once per vacancy, never 13 times in a row, so there is no
same-pass staleness to guard against.

**Corrected design:**
1. Add a NEW parameter to `QING_council_autofill_office`, `$autofill_source$` (values: `boot` |
   `backfill`), set by each caller (`QING_council_autofill` passes `boot`;
   `QING_office_vacate_dispatch` passes `backfill`).
2. Inside the vacant-seat branch, gate the NEW draw attempt on `$autofill_source$ = backfill` — the boot
   path skips straight to the existing create_character mint, unchanged.
3. On the backfill path, attempt an `ordered_character` draw BEFORE the mint, with this gate (Finding 3
   — fully enumerated, not described by reference):
   ```
   employer = scope:qing_autofill_country          # Finding 1 — NEVER bare ROOT
   is_adult = yes
   is_alive = yes
   is_ruler = no
   is_general = no
   is_admiral = no
   is_governor = no
   NOT = { AND = { exists = scope:qing_autofill_country.current_ruler
                    this = scope:qing_autofill_country.current_ruler } }
   NOT = { AND = { exists = scope:qing_autofill_country.primary_heir
                    this = scope:qing_autofill_country.primary_heir } }
   NOT = { has_variable = qing_is_harem_consort }
   NOT = { has_variable = qing_officer_marker }
   NOT = { QING_char_hard_disgraced = yes }
   NOT = { has_office = office_foreign_minister }
   NOT = { has_office = office_royal_tutor }
   NOT = { has_office = office_marshal }
   NOT = { has_office = office_master_of_the_guard }
   NOT = { has_office = office_high_priest_monarchy }
   NOT = { has_office = office_philosopher }
   NOT = { has_office = office_steward }
   NOT = { has_office = office_physician }
   NOT = { QING_char_holds_court_position = yes }    # Finding 3 — ADDITIVE, not a substitute for the above
   has_trait = $degree$                              # office/degree congruence with the mint fallback
   ```
   (This is `QING_office_eligible_candidate`'s exclusion set, re-anchored per Finding 1, PLUS
   `QING_char_holds_court_position` and `has_trait = $degree$` — not a reuse of the trigger itself, since
   it is hardcoded to bare `ROOT`.)
4. `order_by = combined_stats_council_svalue`, `max = 1`, `save_scope_as = qing_autofill_draw`.
5. NO stale-scope guard needed (see scope decision above — single call per vacancy on this path). If
   the draw matched: `scope:qing_autofill_draw = { QING_office_appoint = { office = $office$ } }`. Else:
   fall through to the existing create_character mint, unchanged.
6. **Finding 4 (martial-seat near-permanent no-op) — explicit decision, not left open:** the martial
   offices (war, guard_commandant) use a SOFT preference instead of the hard `has_trait = $degree$`
   filter used for the 11 civil offices. Rationale: the setup seed has ZERO wu_jinshi holders and the
   only accrual paths (day-30/31 grant, triennial exam) are slow — a hard filter would make the martial
   backfill draw permanently dead weight, which is honest but delivers nothing. A soft preference (add
   `qing_wu_degree_prestige_svalue` to the martial draw's `order_by` instead of gating on `has_trait`)
   lets a wu_jinshi-holder win the draw when one exists, without making the draw a guaranteed no-op when
   none does. This reconciles the hard-vs-soft tension #117 independently flagged — #117's design should
   adopt the SAME civil-hard/martial-soft split rather than making an independent, possibly divergent
   choice (see Finding 7 / cross-task note below).
7. **Finding 7 acknowledgment:** `QING_exam_fill_first_vacant_from_pool` (pool-scoped, degree-agnostic,
   wired to `qing_keju.6`/a GUI button) remains a distinct, intentionally-separate fill-from-existing
   path — this design does not unify with it. Noted so the two are not mistaken for redundant or
   conflicting.

**Cross-task note for whoever implements #117 next:** if #117 builds a canonical degree→post predicate
(per #117's own Finding 5), THIS design's draw gate (step 3's `has_trait = $degree$` / step 6's soft
martial preference) should consume that same predicate rather than hardcoding its own — implement #117's
predicate first if both land in the same session, or leave a TODO cross-reference if #116 lands first.

## REVIEW FINDINGS ROUND 2 (2026-08-11) — NOT CLEAN

A design review of the corrected proposal above confirmed Findings 1/2/3 fully resolved (re-anchoring
correct and verified against the actual code; gate composition verified line-by-line against
`QING_office_eligible_candidate` with nothing missing; 3-param macro syntax proven elsewhere in this
file), but found ONE CRITICAL regression and one HIGH spec contradiction, plus a medium gap:

**Finding A (CRITICAL) — the draw re-seats the accused on the `QING_justice_strip_for_trial` backfill
path, defeating the justice mechanic.** Traced `QING_justice_strip_for_trial`
(`se_QING_JUSTICE.txt:315-325`): it calls `QING_office_vacate_dispatch` (which backfills) BEFORE
stripping `is_general`/`is_admiral`/`is_governor` status, and applies NO disgrace at all (hard disgrace
only happens later, on conviction). At the moment the backfill draw runs, the accused is: alive,
CHI-employed, his own `qing_office_held` just removed (so `QING_char_holds_court_position` no longer
excludes him), not yet hard-disgraced, not yet imprisoned. If he holds the office's required degree, he
is a valid — often the TOP-ranked — candidate for the draw's own vacant seat, and the draw silently
re-appoints him to the seat he was just stripped from FOR TRIAL, undoing the strip instantly. The
CURRENT unconditional create_character mint does not have this defect (it mints a stranger, so the
accused stays out) — this design would REGRESS a working mechanic. (The Censorate impeach-uphold path is
NOT affected — it applies hard disgrace before its own vacate/backfill call, so the existing
`NOT = { QING_char_hard_disgraced = yes }` clause correctly excludes that accused.)
**Fix required:** exclude the specific character currently being stripped-for-trial from the draw. Two
options: (a) stamp a `qing_pending_trial` marker on the accused BEFORE `QING_office_vacate_dispatch` runs
in `QING_justice_strip_for_trial`, and add `NOT = { has_variable = qing_pending_trial }` to the draw
gate (clear the marker at trial resolution, win or lose); or (b) reorder `QING_justice_strip_for_trial`
so the general/admiral/governor strips (and, if a disgrace-on-accusation policy is acceptable, a light
taint) run BEFORE the office vacate/backfill, so the accused is already excluded by existing gate clauses
by the time the draw runs. Option (a) is more surgical (no behavior change to command/governor timing);
recommend it unless a reviewer prefers (b).

**Finding B (HIGH) — the martial soft-preference (step 6) is stated in prose but CONTRADICTED by the
concrete gate (step 3) and has no implementation mechanism.** Step 3 lists `has_trait = $degree$` as an
UNCONDITIONAL gate line for ALL offices; step 4 hardcodes `order_by = combined_stats_council_svalue`
with no per-office variation. `QING_office_vacate_dispatch` still passes `degree = wu_jinshi` for war/
guard_commandant. An implementer following steps 3-4 literally, as written, ships a HARD wu_jinshi
filter for the 2 martial offices — reintroducing Finding 4's near-permanent-no-op exactly as before,
despite step 6's prose claiming the opposite. **Fix required:** specify the actual mechanism, not just
the intent. Concretely: gate step 3's `has_trait = $degree$` line itself on a NEW parameter (e.g.
`$degree_hard_gate$ = yes|no`, set to `no` for war/guard_commandant, `yes` for the 11 civil offices at
each of the 26 call sites), and make step 4's `order_by` conditional:
`order_by = combined_stats_council_svalue` when `$degree_hard_gate$ = yes`, else
`order_by = combined_stats_council_svalue` with `qing_wu_degree_prestige_svalue` ADDED for the 2 martial
offices (mirroring `council_sort_martial`'s existing shape, `QING_governance_svalues.txt:229`). This is
buildable (the svalue already exists) but MUST be spelled out as concretely as this, not left as prose
intent contradicted by a literal spec.

**Finding C (MEDIUM) — the "no stale-scope guard needed" justification only covers same-EXECUTION
staleness, not same-TICK-different-death staleness, and step 5's match-detection is unspecified.** The
"single call per vacancy" justification is correct for the ORIGINAL same-pass (13-in-a-row) concern, but
does not address two ministers dying in the SAME tick, each independently triggering
`on_character_death` → a SEPARATE `QING_office_vacate_dispatch` → a separate backfill call — could a
barren second draw read a STALE `scope:qing_autofill_draw` left by the first death's successful draw and
wrongly re-appoint that already-seated man to the second vacancy? The gate's
`NOT = { QING_char_holds_court_position = yes }` protects against this IF the stale scope is re-checked
before use (a successfully-drawn man from death #1 already carries `qing_office_held` by the time death
#2's draw would read him) — but step 5 never specifies HOW "did the draw match" is detected (presumably
`exists = scope:qing_autofill_draw`, but this must be stated, and the re-check on the stale scope, not
just on the fresh `ordered_character` limit, needs to happen before the `QING_office_appoint` call).
**Fix required:** specify step 5 as: `if = { limit = { exists = scope:qing_autofill_draw
scope:qing_autofill_draw = { NOT = { QING_char_holds_court_position = yes } } } ... }` — the SAME
stale-scope-guard idiom used elsewhere this session (#111/#113), reinstated here not for the
13-in-a-row case (correctly ruled out) but for the cross-death-same-tick case (not previously considered).
This is cheap insurance, not the original elaborate guard.

**Finding D (LOW) — blast radius understated.** Threading `$autofill_source$` (and now, per Finding B's
fix, `$degree_hard_gate$`) through all 26 existing call sites (13 boot + 13 backfill) is an all-26-or-
nothing edit — every site must be updated in the same pass or the macro reference breaks. State this
explicitly as a single-PR-sized edit, not something that can be partially rolled out.

**Disposition:** fix Findings A and B (both real defects, not documentation gaps), specify Finding C's
concrete guard, then re-review. Findings 1/2/3 need no further work.

## CORRECTED PROPOSAL ROUND 3 (2026-08-11) — resolves Findings A, B, C

**Fix for Finding A (justice-strip re-seating):** stamp a marker on the accused BEFORE
`QING_office_vacate_dispatch` runs, exclude it in the draw gate, clear it at trial resolution.
- `QING_justice_strip_for_trial` (`se_QING_JUSTICE.txt:315-325`): add
  `set_variable = { name = qing_pending_trial  value = 1 }` as the FIRST line, before the existing
  `if = { limit = { has_variable = qing_office_held } ... }` vacate-dispatch call.
- Add `NOT = { has_variable = qing_pending_trial }` to the draw gate (round-2's enumerated list, this
  doc's earlier section).
- Clear the marker at BOTH trial outcomes: `QING_justice_convict_accused` (`se_QING_JUSTICE.txt:335+`)
  and whatever effect handles acquittal/dismissal of the charge (locate and add
  `remove_variable = qing_pending_trial` to both, so the marker never outlives the trial it was stamped
  for). This is a narrow, surgical fix — no change to the existing general/admiral/governor strip timing
  or to the Censorate impeach-uphold path (which is already correctly excluded via hard-disgrace).

**Fix for Finding B (martial soft-preference mechanism):** thread a second boolean parameter,
`$degree_hard$` (yes|no), alongside the existing `$degree$` param, through all 26 call sites.
- `QING_council_autofill` (boot, 13 calls, `se_QING_COUNCIL.txt:80-92`): every call passes
  `degree_hard = yes` (irrelevant on this path per the scope decision — boot never reaches the draw
  branch — but the parameter must still be supplied at every call site or the macro reference breaks;
  pass `yes` uniformly for boot-path calls as a harmless placeholder).
- `QING_office_vacate_dispatch` (backfill, 13 `else_if` branches, `:1741-1753`): the 11 civil branches
  pass `degree_hard = yes`; the war (`:1745`) and guard_commandant (`:1753`) branches pass
  `degree_hard = no`.
- Inside `QING_council_autofill_office`'s backfill draw gate: make the `has_trait = $degree$` line
  CONDITIONAL — `if = { limit = { $degree_hard$ = yes }  has_trait = $degree$ }` (only gate on it when
  hard). When `$degree_hard$ = no`, no trait gate is applied to the draw's `ordered_character.limit` at
  all (any otherwise-eligible man may be drawn); ranking does the work instead.
- Make `order_by` conditional too: `order_by = combined_stats_council_svalue` when `$degree_hard$ = yes`;
  when `$degree_hard$ = no`, use a `order_by` script value that ADDS `qing_wu_degree_prestige_svalue` on
  top of `combined_stats_council_svalue` (mirroring `council_sort_martial`'s existing shape at
  `QING_governance_svalues.txt:229` — reuse that EXACT svalue rather than inventing a new one, or define
  a trivial new svalue `combined_stats_council_svalue_martial = { value = 0  add =
  combined_stats_council_svalue  add = qing_wu_degree_prestige_svalue }` if `ordered_character.order_by`
  cannot take an inline `add =` expression directly — confirm which form is syntactically legal when this
  is reviewed).

**Fix for Finding C (cross-death same-tick staleness):** reinstate a minimal stale-scope guard —
NOT the original 13-in-a-row rationale (correctly ruled out), but for two separate `on_character_death`
events firing in the same tick, each independently calling this effect:
```
if = {
    limit = {
        exists = scope:qing_autofill_draw
        scope:qing_autofill_draw = { NOT = { QING_char_holds_court_position = yes } }
    }
    scope:qing_autofill_draw = { QING_office_appoint = { office = $office$ } }
}
else = {
    <existing create_character mint, unchanged>
}
```
This is the same idiom used elsewhere this session (#111/#113) — cheap, and correctly scoped to the
narrower cross-death case Finding C identified rather than the same-pass case Finding 5 (round 1)
originally (and correctly) ruled out.

**Blast radius (Finding D, acknowledged, not fixed — informational):** this is now a two-parameter
thread (`$autofill_source$` from round 2, PLUS `$degree_hard$` from this round) across all 26 call
sites, an all-26-or-nothing edit. Treat as a single implementation pass, not incremental.

This round-3 proposal needs its own design review before implementation — dispatching now.
