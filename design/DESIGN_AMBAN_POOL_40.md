# DESIGN — feed the amban candidate pool (#40)

**Status:** design note, 2026-08-09. Small, self-contained (exam/character machinery — NOT economy). Design-note-first per the overnight rule, then implement + review.

## The bug (user, boot-tested)
The amban appointment PICKER is always empty; a sacked/recalled amban is immediately re-appointed because no other eligible candidate exists. Ambans hold the Translation Laureate trait `fanyi_jinshi` (繙譯進士), but nobody else does.

## Root cause (confirmed in source)
The ONLY producer of new `fanyi_jinshi` is `QING_exam_sit_candidate` (se_QING_EXAM.txt:480), the banner-track pass — and it is hooked ONLY to `on_becoming_adult` (00_specific_from_code.txt:719). So:
1. **No boot generation.** Every bannerman ALREADY ADULT at the 1763/1815 start (the whole opening generation of potential ambans) never sits the exam → never gets the degree. Verified: `grep fanyi_jinshi setup/` = 0 hits (no seeded laureates).
2. **The keju cohort mint is civil-only.** `QING_exam_graduate_cohort` (se_QING_EXAM.txt:251) mints only `jinshi`/`juren` via `QING_exam_mint_scholar` (which hardcodes `culture = han`) — it never produces banner `fanyi_jinshi`. So the triennial exam does NOT refill the amban bench.
3. **The picker has no fallback.** `QING_amban_refresh_candidates` (se_QING_AMBAN.txt:231) draws only existing eligible court laureates. While the seeded ambans are all posted (excluded via `qing_amban_marker`/`QING_char_holds_court_position`), the list is empty. A recalled amban drops his marker → becomes the sole `fanyi_jinshi` holder → re-picked. The auto-sweep `QING_amban_post` (:44) has a create-fallback (:132) but it only fires when the eligibility gate finds NOBODY — a just-recalled amban IS somebody, so the fallback never triggers.

## Fix (three parts; A+B are the substance, C is polish)

### A. BOOT BACKFILL — seed a bench of spare banner laureates at game start
The `on_becoming_adult` intake can't reach the pre-existing adult generation, so front-load it. In the CHI `on_game_initialized` block (qing_mechanics_on_actions.txt, after `QING_exam_init`), mint a handful (~4-5) of spare `fanyi_jinshi` bannermen into the CHI court, UNPOSTED, so the manual picker always has real alternatives from turn 1.
- Reuse a NEW mint helper `QING_exam_mint_banner_laureate` (parallel to `QING_exam_mint_scholar`) — `create_character` culture = manchu (or mongol for variety), religion = vajrayana, broker stat weights (add_charisma lead + add_finesse, low martial — matches the amban rank svalue #61 charisma×2+finesse), `add_trait = fanyi_jinshi`. Follow the mint template's deferred-bind pattern (set `qing_needs_bind`, no same-tick affinity read — the #61 flood lesson) and the #90 gotcha (no modifiers inside create_character).
- Do NOT add them to `qing_scholar_pool` (that list is the CIVIL office pool with its own retirement tick); they are free court characters the amban picker finds via its existing `employer=ROOT + fanyi_jinshi + not-holding-a-post` gate. Mark them (e.g. `qing_is_banner_laureate`) only if needed for later bookkeeping — likely not.
- Guard idempotent (a global one-shot flag) so a re-init can't double-seed.
- Count: enough that the picker has 2-3 alternatives beyond the seeded ambans. The 1763 amban roster is ~5-6 posts; seed ~5 spares.

### B. KEJU FEEDS BANNER LAUREATES — ongoing supply
Extend `QING_exam_graduate_cohort` so the triennial cohort ALSO mints an occasional banner-track laureate (not just civil), so the bench refills over time from the exam the design says feeds it. One banner laureate per cycle (scaled by hall count / pass-rate like the civil leads) via `QING_exam_mint_banner_laureate`. This makes the amban pipeline self-sustaining after the boot backfill drains.

### C. RECALL COOLDOWN / RANK PENALTY — don't instantly re-pick a just-recalled amban
So replacement is preferred when alternatives exist: stamp a timed marker (e.g. `qing_amban_recalled_recently`, ~2-3 years) on a recalled amban and either (i) exclude him from `QING_amban_refresh_candidates` for its duration, or (ii) rank him last via the order_by. Prefer (ii) rank penalty (he stays eligible as a last resort, but the fresh bench outranks him) — mirrors the #47 lesser-taint "ranked last, not barred" pattern. This is the direct fix for the reported "sacked amban immediately re-appointed."

## Files
- NEW helper `QING_exam_mint_banner_laureate` in se_QING_EXAM.txt (parallel to QING_exam_mint_scholar).
- Boot backfill call in common/on_action/qing_mechanics_on_actions.txt (CHI on_game_initialized).
- Cohort extension in se_QING_EXAM.txt (QING_exam_graduate_cohort).
- Recall cooldown/penalty: se_QING_AMBAN.txt (QING_amban_recall stamps the marker; QING_amban_refresh_candidates order_by/limit reads it) + possibly qing_amban_rank_svalue (QING_governance_svalues) for the rank penalty.

## Traps / rules
- create_character at on_game_initialized IS the #90 no-log-boot-crash class ONLY when granting to a just-made char / health trait on a boot char — the beg/amban seeds already create characters at boot safely by NOT doing modifiers inline + deferring bind. Mirror that exactly. Actually SAFER: consider running the backfill in the first quarterly pulse (like the aqsaqal spike / #112a caravan super) rather than at construction, if any doubt — but the amban SEED (QING_amban_seed_one) already creates at boot, so construction is proven for this class.
- Deferred bind (qing_needs_bind), no same-tick affinity read (#61 flood).
- fanyi_jinshi is the real trait key (rg corrupts CJK to "n").
- se_/events no-BOM/LF.
- Code-review before commit; freekumquats@users.noreply.github.com, merge-overnight.

## Verify
- Boot: the amban picker (Lifan Yuan panel appoint) shows multiple candidates at 1763 start, not just the posted ambans.
- Recall an amban → the picker offers OTHER laureates ranked above him → replacement, not re-appointment.
- debug.log: the boot backfill mint lines + the cohort banner-laureate line.

---

## ADVERSARIAL REVIEW CORRECTIONS (2026-08-09) — apply BEFORE implementing

Core plan CONFIRMED sound (a bare minted manchu+fanyi_jinshi+employer=CHI free char passes the picker gate AND the manual row-handler, and floats to top via qing_degree_prestige_svalue=25 — no hidden requirement, catch (a) does not exist). Two mechanics corrected + LOWs:

1. **[HIGH] PLACEMENT — do NOT create at on_game_initialized construction.** The exact create_character+add_trait pattern was DELIBERATELY deferred off construction into the day-32 event `qing_force_setup.12` (events/imp19c_mod_events/qing_force_setup_events.txt:164-165, "create_character + add_trait at on_game_initialized (construction) is a known boot-crash class"); it defers QING_council_autofill / QING_subpost_seed_gamestart / QING_exam_seed_hanlin_pool for this reason. The QING_amban_seed_one precedent I cited creates at construction but is the ONE path violating the convention (weak proof, and the OPEN #90 no-log-crash note is unresolved). => MINT THE BACKFILL INSIDE `qing_force_setup.12`, right next to QING_exam_seed_hanlin_pool (qing_force_setup_events.txt:185). Identical proven-safe pattern, runs after council/OOB seating, sidesteps the construction gamble. (Adds a NEW effect e.g. QING_amban_seed_spare_laureates called from qing_force_setup.12, NOT from qing_mechanics_on_actions.txt on_game_initialized.)

2. **[MEDIUM] DROP the deferred-bind marker — it's a dead no-op.** qing_needs_bind is consumed ONLY by QING_exam_pool_tick's loop over `qing_scholar_pool` (se_QING_EXAM.txt:430-438); a laureate NOT in that list is never bound and the marker lingers as dead state. It is NOT a flood/crash risk (setting a write-only var is safe; the picker svalues qing_amban_rank_svalue + combined_stats_council_svalue read only charisma/finesse/degree/disgraced — NO qing_char_affinity — QING_governance_svalues.txt:198-201 documents "flood-free"). => Mirror QING_amban_seed_one EXACTLY: create + add_trait fanyi_jinshi, NO qing_needs_bind, NO bind, NOT added to qing_scholar_pool. (Existing amban chars are never QING_char_bind'd either — scored via QING_char_affinity at post/evaluate time only.)

3. **[LOW] Reword root cause:** there are FOUR add_trait=fanyi_jinshi sites (se_QING_EXAM.txt:524/530 intake; se_QING_AMBAN.txt:144 post-fallback + :612 seed; se_QING_MARCH.txt:284 GG) — but only the intake yields a FREE, UNPOSTED, CHI-court laureate (the others move_country to a subject or set_as_ruler of a march). So say "only producer of a free court-held pickable laureate," not "only producer."

4. **[LOW] Part A is load-bearing; Part C is cosmetic without it.** qing_amban_rank_svalue is the order_by for BOTH the picker AND the QING_amban_post auto-draw, so the recall rank-penalty (C) deprioritizes a recalled man in both — GOOD. BUT the auto-draw's ELIGIBILITY if-gate ignores the svalue, so if the recalled man is the SOLE candidate the auto-path still re-posts him (create-fallback only on an empty bench). => C only fixes the reported bug BECAUSE A supplies alternatives. Also: stamping in the shared QING_amban_recall penalizes EVERY recall incl. benign turnover — acceptable, conscious choice.
   - Recall stamp site CONFIRMED: QING_amban_recall (se_QING_AMBAN.txt:276-314) is the single chokepoint all recall routes funnel through; save the man ~:287-298 and stamp qing_amban_recalled_recently (timed days=~730, the proven qing_amban_clash_cd idiom at :441). Rank penalty in qing_amban_rank_svalue: add `if = { limit = { has_variable = qing_amban_recalled_recently } subtract = 100 }` (mirrors the existing disgraced -100 at :165-168).

5. **[LOW] Count:** 1763 seeds up to 6 posted ambans (TIB/ILI/ULS/MKD/MNC/HLJ, se_QING_AMBAN.txt:643-741), all excluded from the picker while posted. ~5 spares gives 5 alternatives at boot — adequate to fix the reported bug. But long-term the bench drains (6 posts + post-sweep + turnover vs Part B's 1/triennium). Seed 6-8 spares and/or a healthier Part-B cadence. No soft-lock (QING_amban_post create-fallback covers an empty bench).

REVISED IMPLEMENTATION SHAPE:
- NEW QING_exam_mint_banner_laureate (se_QING_EXAM.txt): clone QING_exam_mint_scholar but culture=manchu, religion=vajrayana, charisma-lead+finesse stats, add_trait=fanyi_jinshi, NO pool-add, NO qing_needs_bind, NO bind (= QING_amban_seed_one shape).
- NEW QING_amban_seed_spare_laureates (mint 6-8 via the helper), called from qing_force_setup.12 next to QING_exam_seed_hanlin_pool. Idempotent one-shot flag.
- Part B: QING_exam_graduate_cohort also calls QING_exam_mint_banner_laureate ~1/cycle (scaled by hall count/pass-rate).
- Part C: QING_amban_recall stamps qing_amban_recalled_recently (days=730); qing_amban_rank_svalue subtracts a penalty when set.
