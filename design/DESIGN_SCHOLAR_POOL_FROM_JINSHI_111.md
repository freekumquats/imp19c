# DESIGN #111 — populate the Hanlin scholar pool from real jinshi holders, not create_character spawns

**Status:** REVIEWED (SOUND-WITH-CORRECTIONS, 2026-08-11) — 5 corrections folded below (§CORRECTIONS).
Implementation-ready. The 3/6/9 cap edit is already staged and folds into THIS task's single review.

## §CORRECTIONS (from adversarial review — these SUPERSEDE any contradicting text below)
- **PREMISE CONFIRMED:** real office-less jinshi exist at the 1763.2.16 start — setup/characters/00_Qing.txt
  bakes `jinshi` on ~5-6 real Qianlong-court men (Yu Minzhong 563, Ji Yun 567, Qian Daxin 569, Zhao Yi 570,
  Sun Yuting 355, Dai Junyuan 344) via bare add_trait, NOT pool members. Draw is not circular. Restricted cap
  (3) fills easily; customary (6) ~1 short; broad (9) ~3-4 short at start — acceptable per design.
- **C1 (CRITICAL) — the cohort is IN SCOPE.** The aether-spawn is NOT only in QING_exam_seed_hanlin_pool.
  QING_exam_graduate_cohort (se_QING_EXAM.txt:298/310-319, fired triennially from qing_keju.2 both options,
  qing_keju_events.txt:220/:252 — first cycle ~1 month into a fresh game) ALSO calls QING_exam_mint_scholar
  (create_character → qing_is_pool_scholar → add_to_variable_list qing_scholar_pool). Rewriting only the seed
  relocates the bug to the cohort. FIX: convert QING_exam_graduate_cohort to CONFER jinshi/juren via add_trait
  onto real office-less adult non-degreed courtiers — exactly the laureate model (qing_keju_events.txt:150-159:
  pick ablest courtier not already jinshi, then confer) extended from 1 to the cohort size. This is the
  step-3(a) pipeline fix; it gives the seed-draw a renewable real-jinshi supply.
- **C2 (MEDIUM) — no `max = var` iterator exists in this repo.** Implement the draw as the seed's EXISTING
  per-law-branch shape: `while = { limit = { var:qing_scholar_pool_count < N }  count = N  <draw-one> }` with
  N the literal 3/6/9, and `<draw-one>` = `ordered_character = { limit = {…} order_by = finesse max = 1 … }`.
  The literal `count = N` hard-caps iterations (loop can't hang even when no eligible jinshi remain — the
  acceptable-shortfall case). Each draw stamps qing_is_pool_scholar so the next iteration excludes it. Count
  bumped once per add → stays in sync (integrity OK). (Alt: unrolled if-rungs, the QING_subpost_staff_corps
  pattern se_QING_SUBPOSTS.txt:126-131.)
- **C3 (MEDIUM) — new phantom-member surface from drawing REAL chars.** A drawn jinshi can later become a
  governor/general/admiral via engine/events; the pool tick only strips age≥55/dead, and
  QING_char_holds_court_position does NOT include qing_is_pool_scholar → he lingers as a phantom pool member.
  FIX: add a strip pass to QING_exam_pool_tick mirroring QING_subpost_strip_double_booked
  (se_QING_SUBPOSTS.txt:143-171): drop from the pool any member who is now is_governor/is_general/is_admiral
  (or QING_char_holds_court_position). Minted scholars never needed this; drawn real chars do.
- **C4 (MEDIUM) — scrub stale fallback text.** The "fallback mint" is REMOVED. Ignore/delete every
  fallback reference below (the old step-2 fallback framing, "Why keep the fallback", the #90 fallback bullet,
  "draw-then-fallback-mint" in Files, Review-test items about the fallback). Corrected intent = §CORRECTIONS.
- **C5 (LOW) — add `age < 55` to the draw limit** so near-retirement jinshi aren't drawn only to be retired
  next tick (drawn men are older than the old age-28 mints — Yu is 49).
- **DOWNSTREAM SAFE (confirmed):** under-full/empty pool breaks nothing — the 13 great offices are filled by
  QING_council_autofill_office which mints its OWN officials (does NOT read qing_scholar_pool); pickers +
  drop-member + GUI count all self-guard. Only qing_keju.6's opportunistic pool-raise no-ops. (Verify the
  se_QING_MINISTRY Hanlin roster panel tolerates an empty list — low risk.)

--- (original draft below; where it contradicts §CORRECTIONS, §CORRECTIONS wins) ---

## Problem (user)
The waiting-Hanlin scholar pool is fabricated from the aether. `QING_exam_mint_scholar` (se_QING_EXAM.txt:159)
`create_character`s a fresh han/confucianism age-28 courtier, stamps the degree trait + `qing_is_pool_scholar`
+ `qing_needs_bind`, and adds him to `qing_scholar_pool`. Scholars should instead be the empire's real top
exam graduates — specifically **the highest-finesse JINSHI (進士) holders who do NOT already hold an office**.

## Ground truth (traced in source, this session)
- `qing_scholar_pool` = variable_list on CHI; `qing_scholar_pool_count` = its GUI-read count.
- `qing_is_pool_scholar` (per-char var) = the ACTIVE Academy posting marker: drives the on-name "Hanlin
  Scholar" title (00_offices.txt:186) + death-cleanup + the on-seating drop (QING_exam_pool_drop_member,
  #77/#79) + the deferred-bind gate.
- Cap = law `qing_law_hanlin_cap` (0 customary / 1 broad / 2 restricted), now **6 / 9 / 3** (this task).
- `QING_exam_seed_hanlin_pool` (:342) tops the pool up to the cap via a `while` calling mint.
- `QING_exam_pool_tick` (monthly, 00_monthly_country.txt) retires age≥55/dead (keeps degree, drops marker),
  binds the `qing_needs_bind` scholars, then calls seed to top up.
- CONSUMERS that must keep working: the office-fill pickers (QING_exam_fill_first_vacant_from_pool etc.)
  which already `any_in_list = { variable=qing_scholar_pool  is_alive=yes employer=ROOT NOT={has_variable=qing_office_held} }`;
  QING_exam_pool_drop_member; the GUI count; the Hanlin roster in se_QING_MINISTRY.
- SEPARATE create_character sites NOT in scope (leave alone): se_QING_SUBPOSTS (subpost mint), se_QING_WENZHI,
  se_QING_AMBAN (fanyi_jinshi amban pool). #111 is scoped to the HANLIN scholar pool source only.

## Design — replace "mint" with "draw from office-less jinshi", keep create_character as bounded fallback
Rename intent of `QING_exam_seed_hanlin_pool`: instead of minting up to the cap, it should:
1. **DRAW existing candidates first.** Iterate CHI's characters who: hold the `jinshi` trait, are alive+adult,
   `employer = ROOT`, do NOT already hold an office/court post (`NOT = { has_variable = qing_office_held }`
   AND `NOT = { QING_char_holds_court_position = yes }`), and are NOT already pool members
   (`NOT = { has_variable = qing_is_pool_scholar }`). Select the **highest-finesse** first (`ordered_character
   order_by = finesse`), add up to (cap − current_count) of them: stamp `qing_is_pool_scholar` (+`qing_needs_bind`),
   add_to_variable_list qing_scholar_pool, bump count. NO create_character — these are real jinshi.
   - HANLIN = drawn from jinshi (user): the pool IS the Academy bench; membership drawn from top jinshi. (The
     `hanlin` posting trait, if still granted anywhere, is the "is/was an academician" style — keep separate
     from the pool marker per #77/#79; do not add/remove traits here.)
2. **NO create_character fallback (user correction).** Minting goes away entirely — the aether-spawn is the
   thing being removed; re-introducing it as a "fallback" is the same bug wearing a hat. If the draw can't
   fill the pool, the deficiency is UPSTREAM in the exam pipeline, addressed at (3), not papered over by a spawn.
3. **The exam pipeline MUST produce jinshi (user: "the exam process should 100% produce them, as it did
   historically").** For the draw to have candidates, the keju/examination pipeline (#114 Examinations Convene,
   se_QING_EXAM keju events) must grant the jinshi trait to REAL passers climbing shengyuan→juren→gongshi→
   jinshi, on an ongoing cadence — exactly as the historical triennial metropolitan exam produced a fresh
   jinshi cohort. Two cases the review must distinguish:
   - (a) exams produce NO jinshi at all → that is ITS OWN BUG in the exam pipeline; fix the pipeline to confer
     jinshi to graduates (the primary deliverable if so).
   - (b) exams produce SOME jinshi but not enough to keep the Hanlin pool (3/6/9) full → a SIMPLE TUNING TWEAK
     (raise the exam's jinshi yield / cadence, or widen the draw net), NOT a spawner. The Academy simply runs
     below establishment until enough jinshi exist — historically plausible and self-correcting as exams run.
   Either way the pool is fed ONLY by real graduates; an under-full Academy is acceptable and honest, a spawned
   one is not.

## Why keep the fallback (not a deferral — a graceful-degradation guarantee)
Removing minting outright would empty the pool whenever the realm has < cap office-less jinshi, starving the
GC office-fill pickers (a regression). The fallback makes drawn-jinshi PRIMARY and mint the exception, logged
so the shortfall is visible. If the user wants NO minting ever, that's a one-line removal of the fallback
branch once the exam pipeline reliably produces jinshi — call it out for the review.

## #90-safety / crash rules
- The draw is a pure marker-stamp on EXISTING characters (no create_character) → no #90 create-then-grant risk.
- The fallback keeps the proven QING_exam_mint_scholar create_character idiom UNCHANGED (age/culture/religion
  literals, deferred bind) — no new crash surface.
- Same-tick read-back: drawn EXISTING characters CAN be read same-tick (they're not created this tick), so the
  deferred-bind `qing_needs_bind` split is only needed for the fallback mints (unchanged) — drawn scholars
  could bind immediately, but for uniformity route both through the existing tick-deferred bind (safe).

## Files
- common/scripted_effects/se_QING_EXAM.txt — rewrite QING_exam_seed_hanlin_pool (draw-then-fallback-mint);
  the 3/6/9 cap already staged there.
- localization/english/laws_l_english.yml — 3/6/9 desc already staged.
- No change to QING_exam_pool_drop_member, the pickers, the GUI, or the other create_character sites.

## Review must test
1. Does the draw's `ordered_character` scope + trigger correctly find office-less jinshi (not double-add pool
   members, not steal seated officials)? Confirm `NOT=qing_office_held` + `NOT=QING_char_holds_court_position`
   + `NOT=qing_is_pool_scholar` covers all "already busy" cases.
2. Does the fallback fire ONLY on genuine shortfall (draw first, count-gate the mint)? No double-fill.
3. Pool-count integrity: count bumped exactly once per add (draw AND fallback), matches list length.
4. No regression to office-fill pickers / drop-member / roster.
5. #90: no create-then-grant; fallback create_character unchanged.
6. Is highest-finesse-first the right selection (user said "highest-finesse jinshi")? Confirm order_by=finesse.
