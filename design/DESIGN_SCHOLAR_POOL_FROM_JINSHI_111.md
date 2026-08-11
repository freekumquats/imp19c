# DESIGN #111 — refill the Hanlin pool by DRAWING office-less jinshi (kill only the quarterly aether-spawn)

**Status:** REVIEWED CLEAN-WITH-FIXES-FOLDED 2026-08-11. Rewritten to the user's corrected scope (the two prior
passes — §CORRECTIONS/§CORRECTIONS-2, DELETED — were false-premised, treating the exam cohort's create_character
as the bug; discarded). A fresh adversarial pass on THIS scope returned SOUND-WITH-CORRECTIONS; its 4 findings
are folded inline (marked [REVIEW-FIX N]): (1 HIGH) draw gate must add is_governor/is_general/is_admiral = no —
QING_char_holds_court_position does NOT cover the march-GG roles, so a founding jinshi governor would be stamped
a pool scholar while governing (#77/#79 1:1 violation); (2 MED) same three roles folded into the retire-pass
phantom-strip (a governorship is a drawn scholar's likeliest exit, uncaught by pool_drop_member); (3 LOW) dropped
the redundant NOT=qing_office_held; (4 LOW) commented that count=N is the sole loop terminator in the under-full
refill. IMPLEMENTATION-READY.

## The two rules the user fixed the scope with (authoritative — everything below serves these)
1. **`create_character` with an exam degree is permitted in EXACTLY TWO places, nowhere else:**
   - (a) the **game-start boot seed** — fills the Hanlin Academy to its cap ONCE at start, exactly as the rest
     of the Grand Council is seeded. The one-and-only-one-time exception.
   - (b) the **exam itself** (`QING_exam_graduate_cohort`, surfaced as "The Examinations Convene") — the sole
     ongoing character factory after game start.
2. **After game start, the ONLY place characters with exam degrees are created is the exam.** No other effect
   may spawn a degree-holder post-boot.

## The bug (narrow)
`QING_exam_seed_hanlin_pool` is called from BOTH:
- the **boot event** (`qing_force_setup.12`, day-32 deferred — qing_force_setup_events.txt) → legitimate per
  rule 1(a); and
- the **quarterly pool tick** (`QING_exam_pool_tick`, se_QING_EXAM.txt:496) → this re-runs the SAME
  `create_character` mint every quarter to refill the drained bench. THIS violates rule 2 — it fabricates
  fresh jinshi from the aether instead of drawing from the jinshi the exam has since produced. **This tick
  top-up is the entire bug.**

## The fix — a CALLER SPLIT (not a rewrite of the seed guts, and NOTHING in the exam cohort changes)
Split `QING_exam_seed_hanlin_pool` (se_QING_EXAM.txt:341-378) into two effects:

- **`QING_exam_seed_hanlin_pool_boot`** = today's body VERBATIM (the three law-branch `while` loops that call
  `QING_exam_mint_scholar = { degree = jinshi }` up to the 3/6/9 cap). Called ONLY from the boot event.
  Preserves rule 1(a) — the Academy starts FULL via create_character, the sanctioned one-time seed.
- **`QING_exam_refill_hanlin_pool`** = NEW. NO create_character. Called ONLY from `QING_exam_pool_tick`.
  For each law-branch target N (broad 9 / restricted 3 / customary 6, resolved as a literal per the
  RHS-comparison rule — same branch shape the boot seed uses today), DRAW office-less jinshi up to N:
  ```
  while = {
      limit = { var:qing_scholar_pool_count < N }
      count = N                                   # literal hard-cap. [REVIEW-FIX 4] In the refill (unlike the boot
                                                  # seed, where every iteration mints and the var-limit terminates),
                                                  # when eligible jinshi run out the body no-ops, count never rises,
                                                  # and the var-limit never flips false — so count=N is the SOLE
                                                  # loop terminator here. Safe (N ≥ max possible adds from empty).
      ordered_character = {
          limit = {
              employer = ROOT
              is_alive = yes
              is_adult = yes
              age < 55                            # don't draw a man the retire pass will drop next tick
              has_trait = jinshi
              NOT = { has_variable = qing_is_pool_scholar }        # not already on the bench
              # [REVIEW-FIX 1 HIGH] the "already busy" test MUST mirror the canonical eligible-candidate
              # picker se_QING_COUNCIL.txt:1149-1151, which lists is_governor/is_general/is_admiral
              # SEPARATELY. QING_char_holds_court_position (qing_dynasty_triggers.txt:241-257) is a fixed
              # OR-set of COURT-POST variable markers only and does NOT include the march-GG roles — so a
              # founding jinshi serving as GOVERNOR (e.g. Liu Tongxun 562, #34) would otherwise pass every
              # gate and be stamped a pool scholar WHILE GOVERNING = the exact #77/#79 1:1 violation.
              is_governor = no
              is_general = no
              is_admiral = no
              NOT = { QING_char_holds_court_position = yes }       # not seated in a GC/court post
              # NOTE: QING_char_holds_court_position already ORs has_variable=qing_office_held (:243), so a
              # separate NOT={has_variable=qing_office_held} is redundant — dropped (review finding 3).
          }
          order_by = finesse                      # user: the highest-finesse jinshi
          check_range_bounds = no
          max = 1
          save_scope_as = drawn_scholar
      }
      # stamp + enlist him EXACTLY as the mint's post-create block does (minus create_character):
      scope:drawn_scholar = {
          set_variable = { name = qing_is_pool_scholar  value = 1 }   # excludes him next iteration
          # NO qing_needs_bind deferral needed — he is an EXISTING char (not made this tick), so his
          # affinity vars read back same-tick. But route the bind through the tick's existing deferred
          # pass anyway (stamp qing_needs_bind) for uniformity with boot-seeded scholars — safe (write-only).
          set_variable = { name = qing_needs_bind  value = 1 }
      }
      add_to_variable_list = { name = qing_scholar_pool  target = scope:drawn_scholar }
      change_variable = { name = qing_scholar_pool_count  add = 1 }
  }
  ```
  If fewer than N office-less jinshi exist, the `ordered_character` finds nobody, the iteration no-ops, and the
  Academy runs UNDER-FULL — honest and self-correcting as the exam produces more jinshi. NO spawn to paper it.

## Candidate supply (why the draw is not circular — traced this session)
- **Founding jinshi (rule: valid candidates):** setup/characters/00_Qing.txt bakes `jinshi` on real
  Qianlong-court men (Yu Minzhong 563, Ji Yun 567, Qian Daxin 569, Zhao Yi 570, Sun Yuting 355, Dai Junyuan
  344) via bare add_trait — office-less at start, so drawable. All are <55 at 1763.2.16 (Yu 49 … Dai 17) → the
  age<55 gate excludes none of them initially.
- **Exam-produced jinshi (rule 2):** `QING_exam_graduate_cohort` seats a jinshi lead each triennial when the
  pass-rate band is healthy (>=30), plus juren extras. Over time this is the renewable supply. Yield is thin
  (~1 jinshi/triennial from the cohort; juren extras don't count) → the pool will often run under-full. That
  is ACCEPTED (rule: under-full is honest). Raising exam jinshi yield/cadence is a SEPARATE tuning task
  (#114 / #2), explicitly NOT in #111.
- **Re-eligibility (user-confirmed):** the gate is "has no job RIGHT NOW," not "never had one." A jinshi who
  held an office and left it (retired/dismissed/rotated out) drops `qing_office_held` and becomes drawable
  again — the draw's `NOT={has_variable=qing_office_held}` + `NOT={QING_char_holds_court_position}` already
  captures this.

## One real correction that SURVIVES from the old passes (re-scoped)
- **Strip a drawn scholar who later takes a job (the phantom-member risk).** A drawn REAL char can later become
  a governor/general/admiral or seat a court post; the retire tick (se_QING_EXAM.txt:463-477) currently drops
  only age>=55/dead, so he would linger as a listed-but-employed phantom. FIX: extend that EXISTING retire
  pass's `limit` OR-block with **BOTH** `QING_char_holds_court_position = yes` **AND** `is_governor = yes` /
  `is_general = yes` / `is_admiral = yes` — [REVIEW-FIX 2 MEDIUM] the march-GG roles must be listed SEPARATELY
  because a drawn civil jinshi's LIKELIEST exit is a GOVERNORSHIP, which QING_char_holds_court_position does NOT
  cover (:241-257 is court-post vars only) AND which QING_exam_pool_drop_member does NOT catch (that fires only
  from the office/canton/salt/amban/caravan appoint tails, se_QING_COUNCIL.txt:1606 etc. — nothing routes a
  governor/general assignment through it). Reuse the retire pass's own `remove_list_variable target=prev` +
  count-decrement + `remove_variable qing_is_pool_scholar` body (:472-476).
  SAFETY (review-confirmed): folding QING_char_holds_court_position never strips a legit WAITING scholar — a
  waiting scholar has qing_is_pool_scholar but NOT qing_office_held, and the trigger does not include the pool
  marker; and no double-decrement with pool_drop_member (that delists at SEATING, this at the tick — a seated
  man is already off the list by the time the tick runs). (The old note said "mirror
  QING_subpost_strip_double_booked" — WRONG idiom: that strips a scalar; the pool needs the list-removal the
  retire pass already does. Fold into the retire pass, don't add a new helper.)
  NOTE: the boot-seeded (minted) scholars never needed this because minting made purpose-built unemployed men;
  drawing real chars introduces the need.

## Explicitly NOT in scope (the false-premise fixes from the deleted passes)
- **NO change to `QING_exam_graduate_cohort`** — the exam creating characters is rule 1(b), intended.
- **NO "confer degrees on existing courtiers"** — that was the false-premise fix. Discarded.
- **NO "non-degreed vs not-already-jinshi" reconciliation** — moot; the cohort is untouched.
- **NO laureate/cohort collision concern** — that only arose from converting the cohort; not happening.
- **NO deletion of `QING_exam_mint_banner_laureate`** — untouched (it feeds the amban bench, #40); it was only
  ever "at risk" under the discarded cohort-conversion.
- **`QING_exam_mint_scholar` is KEPT unchanged** — still the body of the BOOT seed (rule 1(a)).

## Files
- common/scripted_effects/se_QING_EXAM.txt — split the seed into `_boot` (verbatim) + `_refill` (new draw);
  point the pool tick (:496) at `_refill`; extend the retire pass (:463-477) with the took-a-job strip. The
  3/6/9 cap literals are already in the boot branches (staged).
- events/imp19c_mod_events/qing_force_setup_events.txt — point the boot call at `QING_exam_seed_hanlin_pool_boot`.
- localization/english/laws_l_english.yml — 3/6/9 desc already staged (customary six / broad nine / restricted three).
- No change to QING_exam_pool_drop_member, the office-fill pickers, the GUI count, the Hanlin roster, or ANY
  create_character site other than renaming the boot seed.

## Review must test (against THIS scope)
1. Caller split is correct: boot event → `_boot` (create_character kept); pool tick → `_refill` (draw only, no
   create_character). No third caller mints post-boot (rule 2 upheld).
2. The draw's `ordered_character` limit finds office-less jinshi and excludes: already-pool, seated-in-office,
   court-position-holders, age>=55. No double-add; each draw's marker excludes it next iteration.
3. `count = N` literal hard-caps the while (can't hang when eligible jinshi are exhausted — the under-full case).
4. Pool-count integrity: +1 per add, matches list length; retire pass -1 per removal.
5. Retire-pass strip of a drawn scholar who took a job (phantom-member) works via the list-removal idiom.
6. Downstream unaffected: office-fill pickers (already gate on employer=ROOT + NOT qing_office_held), drop-member,
   GUI count, roster all tolerate an under-full/empty pool (13 great offices autofill via
   QING_council_autofill_office, which does NOT read qing_scholar_pool — confirmed).
7. #90: the draw is a marker-stamp on EXISTING chars → no create-then-grant. The boot seed's create_character
   is unchanged and still runs from the DEFERRED day-32 event, not construction.
