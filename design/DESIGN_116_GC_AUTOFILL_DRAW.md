# DESIGN — #116 enforce create_character rule on GC autofill

> STATUS 2026-08-11: DIAGNOSIS ONLY. Not implemented, not reviewed. This is a pre-implementation
> design note recording a real risk found during diagnosis, so the next session (or a design-review
> pass) has the finding without re-deriving it.

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
