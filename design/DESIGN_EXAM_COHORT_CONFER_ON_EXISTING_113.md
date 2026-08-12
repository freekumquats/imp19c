# DESIGN #113 — the triennial exam cohort confers degrees on existing degreeless court adults (all 3 tracks), create_character ONLY as fallback

**Status:** SHIPPED (commit 9f2365c94) but IMPLEMENTED WITHOUT the adversarial design review this doc
calls for below — a process gap. Four rounds of POST-IMPLEMENTATION code review were needed to reach a
behaviorally-correct state (3 rounds each caught a real cross-track leak bug; round 4 confirmed CLEAN).
A RETROACTIVE adversarial design review (2026-08-11, after the fact) then examined the shipped design
approach itself and returned NOT CLEAN — see "## RETROACTIVE REVIEW FINDINGS" appended at the bottom of
this file. That review's Finding 1 (shared-trigger extraction) is a real, actionable follow-up fix,
distinct from and not fixing any remaining behavioral bug in the shipped code. Treat this doc as
historical record of what was PLANNED plus what a review found AFTER THE FACT; the planned design below
was never itself adversarially reviewed before implementation began. Distinct from #111 (Hanlin POOL
caller-split); this is the EXAM COHORT itself.

## The rule this serves (user-authoritative — see [[imp19c-character-creation-rule]])
`create_character` with an exam degree is permitted in EXACTLY two places: (a) the game-start boot seed, and
(b) the exam itself. This task keeps the exam as the sole ongoing factory but makes it **prefer conferring the
degree onto a real existing person**, creating a body only when no eligible candidate exists.

## Diagnosis (traced in source this session — se_QING_EXAM.txt)
Two exam mechanisms exist, and they embody graduates oppositely:
- **Per-person path — `QING_exam_sit_candidate` (:534), fired on_becoming_adult.** Tests an EXISTING court
  character and `add_trait`s the degree onto him. It ALREADY confers on real people, and already routes three
  tracks by profile (all inside the one effect):
  - **BANNER 翻譯科** (:566-589): gate `culture_group = jurchen OR mongolic` → `fanyi_jinshi` / `shengyuan`.
  - **MILITARY 武科** (:598-641): gate `martial > finesse` (see §ROUTING-FIX) → `wu_zhuangyuan/wu_jinshi/
    wu_juren/wu_shengyuan` by pass-rate band.
  - **CIVIL 文科** (:642-694): else → `hanlin/jinshi/gongshi/juren/shengyuan/jiansheng` by pass-rate band.
  This path never needs create_character — the sitter IS the existing character. UNTOUCHED by this task except
  the shared §ROUTING-FIX.
- **Cohort batch — `QING_exam_graduate_cohort` (:298), triennial.** Calls `QING_exam_mint_scholar` (:159) for
  every graduate slot, which UNCONDITIONALLY `create_character`s a fresh body (age 28 / han / confucianism /
  add_trait $degree$). **CIVIL ONLY today**, always spawns. THIS is what #113 reworks.

## Desired behavior (user, locked)
1. For each cohort graduate slot: FIRST try to confer the degree (`add_trait`) onto the **ablest** existing
   degreeless adult CHI-court character of the slot's track profile; `create_character` ONLY as fallback when
   none is eligible.
2. **Extend the cohort to all THREE tracks** (user: "extend the cohort to all 3 tracks"). Today only civil
   graduates come out of the batch; banner + martial graduates only trickle from the coming-of-age path. Give
   the cohort banner + martial slots too, so the amban bench (banner) and the Green Standard officer pool
   (martial) get a renewable triennial batch supply — the starvation #40 patched with a one-off banner mint;
   this absorbs that need.
3. The create_character **fallback applies to banner + martial too** (user: "add the create_character fallback
   to the banner and martial exam track"): when no eligible existing candidate of the track profile exists,
   create one with that track's profile.

## Design

### §ROUTING-FIX (shared, user directive)
Drop `martial > charisma` from the military-track routing gate; keep ONLY `martial > finesse`
(se_QING_EXAM.txt:600-601). Charisma is not a keju axis, so a martial+charismatic man still belongs on the
military ladder. Apply to BOTH the per-person path (:600) AND the new cohort track-selection so routing stays
consistent. This is the ONLY edit to the per-person `QING_exam_sit_candidate`.

### The cohort rework — a per-track "confer-else-create" helper
Replace each `QING_exam_mint_scholar = { degree = X }` call in `QING_exam_graduate_cohort` with a new
`QING_exam_seat_graduate = { track = <civil|banner|martial>  degree = X }` that does:

```
QING_exam_seat_graduate = {
    # Try to CONFER on the ablest eligible existing degreeless court adult of this track's profile.
    if = {
        limit = { any_character = { <track candidate gate> } }
        ordered_character = {
            limit = { <track candidate gate> }
            order_by = <track ability metric>     # civil: finesse; martial: martial; banner: charisma (amban stock)
            check_range_bounds = no
            max = 1
            save_scope_as = seated_graduate
        }
        scope:seated_graduate = {
            add_trait = $degree$
            set_variable = { name = qing_sat_keju  value = 1 }   # excludes him from the per-person path + next cohort slot
        }
    }
    # FALLBACK: no eligible existing candidate → create one with this track's profile (the sanctioned factory).
    else = {
        <track create_character>       # civil = existing QING_exam_mint_scholar body; banner/martial = new profiles below
    }
}
```

**Track candidate gate** = the per-person gate (QING_exam_sit_candidate:536-557) MINUS `NOT=has_variable
qing_sat_keju`? — NO: KEEP `qing_sat_keju` in the gate so a man who already sat (per-person) is not re-graded,
AND stamp `qing_sat_keju` on each conferred pick so the cohort's own multiple slots don't double-confer the
same man. Common gate: `exists=employer  employer={tag=CHI}  is_ruler=no  prisoner=no  is_adult=yes  NOT={has_
variable=qing_sat_keju}` + degreeless (NONE of jiansheng/shengyuan/juren/gongshi/jinshi/hanlin/fanyi_jinshi/
wu_shengyuan/wu_juren/wu_jinshi/wu_zhuangyuan). PLUS the per-track profile:
- **civil:** (no culture/martial constraint — the residual track). order_by = finesse.
- **banner:** `OR={ culture.culture_group=culture_group:jurchen  culture.culture_group=culture_group:mongolic }`.
  order_by = charisma (amban-broker profile, matches qing_amban_rank_svalue).
- **martial:** `martial > finesse`. order_by = martial.

NOTE the profiles are MUTUALLY the same routing as the per-person path, so a court adult is a candidate for
exactly one track — no cross-track poaching if the cohort is careful to run them in a fixed order and each
conferral stamps qing_sat_keju.

### Track fallbacks (create_character — the last resort)
- **civil:** the EXISTING `QING_exam_mint_scholar = { degree = $degree$ }` (age 28 / han / confucianism), UNCHANGED
  — already #90-safe, deferred-bind split intact. It also add_to_variable_list's the scholar pool + bind; for a
  cohort graduate that is fine (matches today's behavior).
  - OPEN Q for review: today EVERY civil graduate mint goes into qing_scholar_pool via mint_scholar. When we
    CONFER on an existing man instead, should he ALSO be added to the pool? Probably NOT automatically — pool
    membership is #111's draw-from-office-less-jinshi concern; a fresh jinshi graduate becomes pool-eligible
    naturally via #111's tick draw. Recommend: the conferred path adds the degree ONLY (no pool insert); the
    fallback-create path keeps today's pool insert (so behavior for created bodies is unchanged). Review to confirm.
- **banner:** new fallback mirroring `QING_exam_mint_banner_laureate` (:218): create manchu / vajrayana /
  charisma-lead body + add_trait fanyi_jinshi. (For lower banner outcome, shengyuan on a created body is odd —
  keep the fallback at the fanyi_jinshi tier the cohort slot represents.) #90-safe: no modifiers in
  create_character, runs from the deferred triennial path.
- **martial:** new fallback: create a martial-lead body (culture han — the wuju was the HAN path to the Green
  Standard, per :597) + add_trait $wu_degree$. Mirror QING_exam_mint_scholar's shape (age 28, add_martial lead,
  finesse/charisma spread) with the wu_* trait instead. #90-safe, deferred path.

### Cohort structure (all 3 tracks)
`QING_exam_graduate_cohort` currently: 1 civil lead (jinshi/juren by pass-rate) + hall-count civil extras +
1 banner-laureate mint (:326). Reshape to seat graduates across the three tracks:
- CIVIL lead + extras: KEEP the existing count/tier logic (jinshi if pass_rate>=30 else juren; +1 juren at >=16
  halls, +2 at >=28), routed through QING_exam_seat_graduate track=civil.
- BANNER: the existing 1 banner-laureate per cycle (:326, gated >=16 halls) → route through
  QING_exam_seat_graduate track=banner degree=fanyi_jinshi (confer on an eligible bannerman first, else create —
  this is a strict improvement over the current always-create QING_exam_mint_banner_laureate).
- MARTIAL: NEW — add martial graduate slot(s) scaled by hall count, tier by pass-rate band (wu_jinshi/wu_juren/
  wu_shengyuan mirroring the per-person martial ladder), routed through QING_exam_seat_graduate track=martial.
  MAGNITUDE (best-guess, log-and-tune per overnight Rule 1a): 1 martial graduate per cycle at >=16 halls, tier
  wu_jinshi if pass_rate>=30 else wu_juren. Logged so the boot confirms/tunes.

## #90 / crash safety
- Conferral is `add_trait` on an EXISTING adult (no create-then-grant) → #90-safe.
- All three fallback create_characters run only from the triennial cohort (a deferred/runtime path, never
  construction) with NO modifiers inside create_character — the proven idiom (QING_exam_mint_scholar,
  QING_exam_mint_banner_laureate). Deferred-bind split preserved for the civil pool insert.
- add_trait on the trait/opposite machinery must be RUNTIME only (QING_grant_martial_degree:735 note:
  access-violates at construction) — the cohort is triennial runtime, safe.

## Files
- common/scripted_effects/se_QING_EXAM.txt — §ROUTING-FIX at :600-601; new QING_exam_seat_graduate helper +
  banner/martial fallback creators; reshape QING_exam_graduate_cohort (:298) to seat across 3 tracks. Keep
  QING_exam_mint_scholar (civil fallback) + QING_exam_mint_banner_laureate (or fold into the banner fallback).
- No change to QING_exam_sit_candidate except §ROUTING-FIX. No change to #111's pool machinery.

## Review must test
1. §ROUTING-FIX applied to BOTH the per-person path and the cohort track-selection; no other per-person change.
2. Each cohort slot confers on the ablest eligible existing degreeless court adult of the RIGHT track profile;
   the profiles partition court adults into exactly one track (no cross-track double-eligibility given the
   culture/martial routing) — confirm a bannerman can't be pulled onto the civil slot and vice versa.
3. qing_sat_keju stamping prevents double-conferral across the cohort's multiple slots AND against the
   per-person path. Confirm a man who already sat (per-person) is excluded from the cohort.
4. Fallback create_character fires ONLY when no eligible candidate exists (the `else` of an `any_character`
   existence check) — not in addition. No double-graduation per slot.
5. Banner fallback = manchu/vajrayana/fanyi_jinshi; martial fallback = han/martial-lead/wu_*; civil = unchanged
   mint. All #90-safe (deferred path, no modifiers in create_character).
6. Degree-TIER logic preserved (civil jinshi>=30 else juren + hall extras; martial wu_jinshi>=30 else wu_juren;
   banner fanyi_jinshi). Magnitudes logged for boot tuning.
7. Pool interaction: conferred civil graduates should NOT be auto-inserted into qing_scholar_pool (that's #111's
   draw); confirm the fallback-create civil path's pool insert is preserved and the conferred path omits it — or
   justify a different choice. No regression to #111.
8. QING_exam_mint_banner_laureate: if the banner cohort slot now routes through the confer-else-create helper,
   is the standalone mint still called anywhere (QING_amban_seed_spare_laureates boot backfill)? Don't break #40.

## RETROACTIVE REVIEW FINDINGS (2026-08-11, post-implementation design audit)

The shipped code (`common/scripted_effects/se_QING_EXAM.txt`, commit `9f2365c94`) is behaviorally
correct — the fourth code-review round confirmed the three tracks are mutually exclusive and jointly
exhaustive, matching `QING_exam_sit_candidate`'s own partition token-for-token, including the
`martial == finesse → civil` boundary. No remaining behavioral bug was found. But a retroactive
adversarial review of the DESIGN APPROACH (not just the final code) returned **NOT CLEAN** on
structural grounds:

**Finding 1 (primary, actionable) — the partition is copy-pasted across four sites with nothing
forcing lockstep.** The civil/banner/martial track partition lives independently in
`QING_exam_sit_candidate` (as ordered if/else_if branches) AND in the three cohort helpers
(`QING_exam_seat_civil_graduate`/`_banner_laureate`/`_martial_graduate`, each as a flat predicate that
hand-negates the earlier branches). Hand-negating branches into flat predicate form is exactly the step
that produced all three review-round bugs. Worse, the 11-trait "degreeless" NOT-list is ALSO duplicated
verbatim in all four sites — a second lockstep hazard that happened to stay consistent by luck, not by
any review. Nothing today forces a future edit to `QING_exam_sit_candidate` (a new track, a changed
`martial > finesse` threshold, an added degree trait) to propagate to the three cohort copies — the next
change could silently reintroduce a cross-track leak with zero compile error and zero failing gate.
**Recommended fix (not yet implemented, needs its own review before landing):** extract shared
scripted_triggers — `QING_char_exam_degreeless` (the 11-trait list) and
`QING_char_exam_track_civil`/`_banner`/`_martial` (the partition) — called from BOTH
`QING_exam_sit_candidate`'s branch conditions and the three cohort helpers' `ordered_character` limits.
This pattern is already proven in the same file (`QING_exam_pool_draw_one` already calls a shared
scripted_trigger, `QING_char_holds_court_position`, inside an `ordered_character` limit), so it is not a
novel idiom — it converts "verified consistent today" into "cannot diverge by construction."

**Finding 2 (low) — the stale-scope guard is correct but heavier than the call shape needs.** The civil
helper's guard (borrowed from #111's while-loop draw) is genuinely necessary GIVEN the design chosen
(one `max=1` save-scope name reused across up to 3 calls per cohort). But the call count here is a
fixed, small, literal-gated 1+2 (lead + hall-band extras), not an unbounded loop. A single lead
`ordered_character max=1` followed by one `ordered_character max=2` for the extras would pick 2 DISTINCT
characters in one call (the lead's `qing_sat_keju` stamp already excludes him), needing NO stale-scope
guard at all. Caveat: a fully dynamic `max = var:slot_count` is likely unproven in this codebase (same
class of concern as the `days = var:X` unproven-idiom note elsewhere), so the literal-max-2 split is the
feasible form, not a dynamic one.

**Finding 3 (low, undocumented tradeoff) — the confer path is a transient early-game backlog drain, not
a permanent behavior, and this was never stated explicitly.** The cohort's `NOT has_variable
qing_sat_keju` gate means confer can only ever match characters who never passed through
`on_becoming_adult` — i.e., the game-start adult backlog. Every NEW adult gets stamped by the per-person
intake before the cohort ever sees him. So mid-to-late game, the confer path finds nobody and the cohort
degrades to minting exactly as it did before #113. Likely the intended scope (mirrors the amban-bench
rationale that the pre-existing generation can't be reached any other way), but a design review would
have pinned down this lifetime expectation explicitly rather than leaving it implicit.

**Finding 4 (low, consistency gap) — the cohort confer gate doesn't exclude office-holders or the
primary heir, unlike its sibling pool-draw.** `QING_exam_pool_draw_one` excludes
`QING_char_holds_court_position` and the primary heir; the three cohort confer helpers exclude neither.
Harmless in practice (just stamps a prestige trait onto an incumbent), and matches
`QING_exam_sit_candidate`'s own laxity, but the cohort's purpose is producing NEW talent, not decorating
incumbents — worth asking whether office-less should gate here too, for consistency with the sibling
draw path.

**Finding 5 (root-cause, process) — the original task diagnosis (this doc) named the WHAT
("confer-else-create") but not the CENTRAL RISK ("keep three new gates in lockstep with a fourth
pre-existing one").** This doc inherited #111's draw-first/mint-fallback shape and treated #113 as a
mechanical extension. That framing hid that the real hard problem was a mutually-exclusive,
jointly-exhaustive population partition maintained in FOUR parallel copies. Had this doc's own review
(called for above, never actually dispatched before implementation) run BEFORE code was written, it
would very likely have surfaced Finding 1 up front and converted three rounds of post-hoc whack-a-mole
into one structural decision made once. Bundling a brand-new martial track (no cohort precedent to copy
from) into the same task as the confer refactor compounded this — the martial helper's missing culture
exclusion (round 1's bug) had no existing cohort code to pattern-match against carefully.

**Disposition:** Finding 1's shared-trigger extraction is a genuine follow-up fix, not yet implemented.
It must go through its own design review (per the standing gate) before any code changes — do not
implement directly from this retroactive finding alone.
