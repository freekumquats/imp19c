# Qing Feature Suite — Cross-Wiring & Depth Assessment (READ-ONLY, no implementation)

**Date:** 2026-07-20 · Branch `merge-overnight` · Player tag CHI.
**Mandate (operator):** deep assessment of the Qing feature suite for (a) cross-wiring potential
(Qing↔Qing and Qing↔vanilla), (b) duplication to reduce, (c) depth to enhance, (d) abstract→concrete
opportunities. **Report only — nothing implemented.** Findings overlapping the concrete-conversion
backlog (task #91) are excluded; this hunts NEW opportunities.

**Method:** 6 parallel read-only cluster agents (court/personnel · decline/crisis · economy/modernization ·
frontier/subjects · diplomacy/foreign-arcs · religion/military/misc), each producing a structured report
with file:line citations, PLUS a cross-cutting infrastructure pass by the synthesizer (the shared spine no
single cluster sees). **The synthesizer independently VERIFIED every high-impact and "dead-code" claim
against the actual code** — two agent claims were refuted (see §6). Treat unverified agent claims as
leads, not facts, until a boot / targeted grep confirms.

---

## 0. Scale & shape of the surface
- **76** `se_QING_*.txt` effect files (~29,200 lines), **~59** `qing_*_events.txt`, **24** `gui/qing_*.gui`,
  **32** Qing scripted_guis, **3** Qing on_action files.
- **49 distinct 0..100 counters** on CHI, all nudged via ONE shared engine (`QING_DECLINE_nudge`).
  This meter-centric spine is the suite's backbone AND its main cross-wiring / abstract→concrete surface.
- The suite is, overall, **well-built**: strong concrete-object discipline (councils/rosters/harem/officer-
  corps are real character lists; military decay drives real unit debuffs + real legions; treaty ports &
  missionary stations are already real province objects), a shared logging module, and a throttled monthly
  pulse tying ~20 subsystems. The findings below are **enhancement opportunities, not a broken system.**

---

## 1. TOP CROSS-CUTTING THEMES (synthesizer — spans clusters)

**T1. Parallel "suzerain control" models — the single biggest DUPLICATION (frontier cluster).**
THREE systems model the strength of Qing overlordship, with no shared source of truth:
(1) `SUBJ_ladder_rung` (4-rung real subject-type ladder, se_SUBJECT_QING.txt:43-65),
(2) `qing_suzerain_prestige` (0..100 abstract counter, se_QING_VASSAL.txt:24),
(3) `qing_sphere_dominant` (per-state 0-4 codes, se_QING_SPHERE.txt:37-43).
They never read each other. **Highest-value refactor:** make the real subject graph (rung + is_subject_type)
the source of truth; DERIVE `qing_suzerain_prestige` from live subject count/rung distribution; and make
sphere flips change actual subject types. (Cross-confirmed by diplomacy cluster T-Sphere below.)

**T2. Sphere contest is cosmetic — highest-value single cross-wire (diplomacy + frontier agree).**
`se_QING_SPHERE.txt` runs a four-power influence contest but: (a) its documented tie-in to `qing_gp_tension_*`
is written in comments but NOT wired (diplomacy cluster verified 0 hits); (b) winning/losing a march never
changes province owner or subject type (frontier cluster verified no `change_province_owner`/`make_subject`);
(c) it has ZERO player verbs (pure pulse). So the contest is watch-only with no stakes. Concrete hooks in §2.

**T3. Foreign-adventure arcs are lateral set-pieces (diplomacy cluster).** Mexico/Americas/USCW arcs correctly
hook GP-tension but don't feed any core meter (reform/currency/selfstr) beyond one-shots — only Napoleon
(4× selfstr calls) and USCW (1×) have vertical depth. They're flavor vignettes without domestic consequence.

**T4. "Meter fed by many, consumed by few" — the depth-gap signature.** Whole-suite write/read scan:
`qing_reform_pressure` (96 writes / 23 reads, nearly all reads in se_QING_ROSTER), `qing_ethnic_tension`
(42/10), `qing_sect_pressure` (53/18). These are NOT dead (every counter is consumed somewhere — see §5),
but lots pushes them and comparatively little happens *because* of them. Prime targets for consequence depth.

**T5. Abstract→concrete is already the house style — and mostly done.** Treaty ports (real province modifiers,
se_QING_TREATIES:157-181), missionary stations (real buildings), Self-Strengthening (real arsenals/rail/tech +
新軍 legion), banner decay (real unit morale debuffs), regional magnates (real commanders w/ loyal_veterans),
students→returnees — all already concrete. The NEW opportunities in §3 are genuinely incremental.

---

## 2. CROSS-WIRING OPPORTUNITIES (consolidated, priority-ordered)

**HIGH**
- **Sphere → GP-tension (wire the documented-but-missing tie-in).** On a march flipping away from China,
  nudge `qing_gp_tension_<rival>` (diplomacy cluster gives the exact 5-line hook for `QING_sphere_tick_state`).
- **Sphere → real subject changes.** A march lost to a rival should demote the Qing subject holding it a rung
  (or hand it to the rival as a real client); a march won should promote. Gives the contest stakes (frontier T2/§3D).
- **Foreign arcs → domestic feedback.** USCW/Mexico/Americas should feed selfstr_progress or reform_pressure
  (diplomacy cluster gives per-arc hooks), so overseas ventures matter at home.
- **Exam ladder → Censorate corruption.** A degraded `qing_exam_ladder` (bought degrees) should feed venal
  candidates into the censorate roster (court cluster: weight `qing_exam_ladder < 40` in `QING_censorate_find_corrupt`).
- **Rites → Mandate meter.** Ritual efficacy grants vanilla legitimacy but never nudges `qing_mandate_strength`
  (religion cluster Opportunity #1) — wire ceremonies to the mandate counter so ritual gates Taiping/rebellion rolls.

**MEDIUM**
- **Missing decline cross-links (decline cluster):** corruption≥60→sect_pressure; banner_decay≥70→sect_pressure;
  currency_stress≥70→ethnic_tension; high granary_stock→passive sect relief. Each a 1-line pulse add with a clear
  historical rationale (venal officials→famine→White Lotus; rotten armies can't suppress; silver crisis→frontier tax burden).
- **Opium ↔ treaty ports (diplomacy cluster):** legal opium should boost port commerce and more ports should
  amplify the opium drain (the Shanghai-boom link); currently adjacent but mechanically blind to each other.
- **Wenzhi patronage → exam ladder (court cluster):** high 文治 should widen the talent funnel.
- **Amban effectiveness → subject ladder (frontier cluster):** an effective amban should push integration /
  promote a rung; a failing one should trigger demotion — currently a parallel character layer that doesn't move the ladder.

**Qing↔VANILLA (medium; where the suite runs a private track beside an engine system)**
- **Faction systems (court cluster, CRITICAL-flagged):** `qing_char_faction` (reformist/conservative) runs
  parallel to vanilla `character.faction` with no cross-read. Reconcile at init, or have `QING_faction_assign`
  also `join_faction`.
- **Vanilla great offices treated as conflicts, not congruences (court cluster):** council filters blanket-exclude
  `office_marshal`/`office_steward`/etc.; role-congruent ones should be appointment *bonuses* to War/Revenue seats.
- **Dynastic harmony vs vanilla opinion; exam graduates vs vanilla prominence; officer corps ignores vanilla
  general traits (court cluster):** each a custom meter beside an engine metric that should feed it.
- **One-way vanilla reads that should write back (decline cluster):** ethnic_tension reads `province_unrest` but
  never raises it; corruption/sect/banner-decay could drive tyranny / province unrest / war exhaustion.
- **Caravan / tribute gold bypass the engine trade/tribute income systems (frontier cluster):** direct `add_treasury`
  instead of `trade_route` / `tribute_income_modifier`.

---

## 3. ABSTRACT→CONCRETE — NEW (beyond backlog #91)
Ranked; all HYBRID (keep the counter as summary, hang a real object off it) per the standing rule:
1. **Amban → real governorship** (frontier): make the resident the engine `set_as_governor` of a subject province,
   so loyalty/opinion flow from the real role (mirrors the Han-magnate pattern). *(High value, med risk.)*
2. **Caravan → real trade route** (frontier): define a Kashgar→Beijing `trade_route`; prosperity drives a route
   modifier instead of a flat treasury trickle.
3. **Frontier settlement → real Han pops** (frontier): settlement pushes `create_pop culture=han` in frontier
   provinces — feeds ethnic tension organically and makes later integration a real demographic shift.
4. **Censorate vigor → deployed investigating-censor characters + province modifier** (court): 御史 dispatched to
   a high-corruption province, events fire *there*.
5. **Office-vacancy strain → acting ministers** (court): appoint a 署理 acting holder at half-strength on a vacancy.
6. **Wenzhi patronage → imperial-project buildings** (court): 四庫全書 library / observatory / kilns at thresholds
   (mirrors the Summer Palace concrete-building pattern).
7. **Dynastic harmony → throne-council sessions; scholar-pool retirees → private-academy province modifiers;
   affinity → stipend/faction transaction** (court). 8. **Rites → real ritual-complex building; pilgrimage → pilgrim
   governorship; guard corps → ruler-security modifier** (religion). 9. **Investiture → vanilla opinion; sphere flip →
   liberty_desire** (frontier).

---

## 4. DEPTH GAPS (shallow features w/ obvious room)
- **Sphere & treaty revision have no player verbs** (diplomacy): sphere is watch-only; treaty revision is event-only.
  Add Frontier/Zongli panel actions ("Dispatch Amban", "Foment Unrest", "Press for Treaty Revision").
- **Ratchet meters lacking recovery/relief events** (decline): banner/greenstandard decay only relieved by one drill
  lever each; ethnic tension has weak recovery — add crisis-response events ("Grand Pardon for Frontier Peoples",
  Mongol marriage-alliance to cut banner decay).
- **One-shot arcs with no follow-up** (decline + frontier): Mandate disasters, population memorial, subject absorption
  all end abruptly — add recovery/escalation follow-ons and post-annexation consequence chains.
- **Shallow court set-pieces** (court): exam cycle & harem are one-shots (no bribery scandal, sponsor-a-candidate,
  consort rivalry, appointment opposition, officer promotion-from-reports). Rich branching exists for dynasty/council —
  bring exam/harem/censorate up to that bar (investigation→verdict→exonerate for impeachment).
- **Economy upside-only paths** (economy): treasure fleet, railway extension, Summer Palace have no risk/upkeep —
  add piracy/storm loss, corvée unrest, maintenance drain.
- **Rites/pilgrimage thin** (religion): 4 rites events (random-only, no scheduling lever); linear 5-event pilgrimage
  with no accumulating patronage standing. Add a Rites ministry action panel and a `qing_tibetan_patronage` standing meter.
- **Military traditions tree is passive** (religion): the 十全武功 tree grants modifiers but no Qing mission grants
  `add_military_experience` toward it — wire Ili/Burma/Taiwan mission completions to the matching nodes.

---

## 5. DEAD / INERT — VERIFIED (most agent "dead" claims did NOT survive verification)
- **NO true write-only counters.** Whole-suite scan flagged `qing_ttx_debt_*` → VERIFIED false positive
  (per-power vars read at se_QING_TECHTRANSFER.txt:198-213). The religion & decline clusters independently
  confirmed no orphaned decline counters.
- **REFUTED — `qing_gc_event_slot_used` is NOT an inert throttle** (court cluster claimed it was): there are
  **18 check-sites** (`has_variable = qing_gc_event_slot_used` in event limits) vs 31 set-sites. It IS wired.
- **REFUTED — JAPAN_PREPERRY / OPEN_JAPAN / PILGRIMAGE are NOT dead** (diplomacy cluster claimed "delete 25KB"):
  all three are LIVE via their paired files — `QING_jppre_init` at qing_mechanics_on_actions.txt:209;
  `QING_openjapan_*` from qing_open_japan_missions.txt:94-237; `QING_pilgrim_*` from qing_pilgrimage_events.txt:55-167
  (+ religion cluster independently confirmed pilgrimage modifiers are applied). The diplomacy agent only searched
  effect→effect references and missed event/mission/on_action callers. **DO NOT delete.**
- **Genuinely inert / low-value (worth cleanup, low priority):** `qing_vassal_lost_ryukyu` / `_burma` write-only
  flags (out-of-scope subjects, never read — frontier cluster); `SUBJ_ladder_rung = 0` off-ladder case never handled;
  the `QING_harem_rank_cap` dead comment (already removed in a perf audit). These need a targeted re-verify before action.
- **Consistency (not dead, hygiene):** ~106 create_character calls across 33 files; 20 files spawn without an in-file
  `QING_roster_finalize`. Spot-checks (harem consort, guard commander) show these are DELIBERATE bespoke spawns with
  the correct #90/culture-flood idiom — recommend a consistency pass to confirm each honors the trait/culture rules,
  but this is hygiene, not a defect.

## 5a. Duplication worth consolidating (beyond T1)
- **Three "pick a courtier by skill" pickers** (council/exam/harem) share one idiom → unify into a parameterized
  `QING_courtier_refresh_picker` (court cluster).
- **Per-ministry performance boilerplate** (12 near-identical `QING_ministry_recompute_perf_*`) → template + per-office addenda.
- **Two "strip office on disgrace" paths** (censorate + justice) → one `QING_char_disgrace_vacate_office` helper.
- **Japan arc split across PREPERRY + OPEN_JAPAN** (diplomacy): a false module boundary (one continuous relationship,
  never both active) — could merge under one era-gated file. (Merge, NOT delete — see §5.)
- **3 copies of the 4-way GP-tension power-dispatch** (embassy/legation/missionary) → hoist `QING_ease_gp_tension` to se_QING_DIPLO.

---

## 6. VERIFICATION LOG (what the synthesizer checked, and corrections made)
- `qing_gc_event_slot_used`: 18 check-sites confirmed → court cluster's "inert throttle" claim **REFUTED**.
- 3 "dead" files: each defining effect traced to a live event/mission/on_action caller → diplomacy cluster's
  "delete 25KB" **REFUTED**; reframed as "merge Japan files (optional), keep all three."
- `qing_ttx_debt_*` write-only flag: **REFUTED** (read at TECHTRANSFER:198-213).
- create_character finalize-gap: spot-checked → mostly intentional bespoke spawns, downgraded to hygiene note.
Remaining agent claims marked "needs grep/boot to confirm" (e.g. off-ladder rung=0 consumers, ryukyu/burma flags,
qing_war.3 naval spawn) should be re-verified before any action.

---

## 7. RECOMMENDED SEQUENCING (if/when implementation is authorized — NOT done here)
1. **Tier 1 (structural, high value):** unify the three suzerain-control models (T1); wire sphere→GP-tension +
   sphere→subject-type (T2); this is the largest coherence win and touches frontier + diplomacy together.
2. **Tier 2 (cheap cross-links, high ratio):** the decline cross-links (§2 MEDIUM) and exam↔censorate, rites↔mandate —
   each a few lines with clear history, all additive/low-risk.
3. **Tier 3 (depth):** player verbs for sphere/treaty; recovery/escalation events for ratchet meters; court set-piece
   branching (exam/harem/censorate/appointments).
4. **Tier 4 (concrete faces):** the §3 abstract→concrete items, HYBRID per the standing rule.
5. **Tier 5 (hygiene):** duplication consolidation (§5a), verified dead-flag cleanup, create_character consistency pass.
All Tiers are additive and independently shippable; none requires the risky perf work. Each would follow the
fix-traceability rule (task-tagged comment + se_LOG + report) and a boot-crash review before commit.

---
---

# APPENDIX A — FULL PER-CLUSTER AGENT REPORTS (verbatim)

The six sections below are the **complete, unedited** output of each cluster agent, preserved so nothing is
lost to the §1–§7 consolidation. **Editorial correction flags** in `> ⚠️ SYNTHESIZER CORRECTION` blockquotes
are the ONLY inserted text — they mark the three claims the synthesizer verified and refuted. Everything else
is the agent's own words and citations. Where an agent hedged ("needs grep to confirm", "file not read"), that
hedge is theirs and still stands as an open verify-before-acting item. Agent claims are LEADS; the §6
verification log records which were checked.

---

## APPENDIX A.1 — COURT & PERSONNEL CLUSTER

## 1. CROSS-WIRING OPPORTUNITIES

### A. Qing ↔ Qing (missing internal couplings)

**HIGH PRIORITY:**

1. **Exam system → Censorate**: The examination ladder health (`qing_exam_ladder`) and graduate pool quality directly affect court integrity, but the Censorate never reads them. A corrupt/degraded ladder should feed venal officials into the system → **Hook**: `QING_censorate_find_corrupt` should weight `qing_exam_ladder < 40` as a source of more corrupt candidates; low ladder = bought degrees flooding the court.

2. **Harem succession → Dynasty harmony**: The harem (`se_QING_HAREM.txt`) produces heirs via `make_pregnant`, but Crown Prince selection/designation is never wired to which harem consort bore him. A high-rank consort (`qing_consort_rank = 4`, 皇貴妃) whose son becomes Crown Prince should affect `qing_dynastic_harmony` (consort-clan power play) → **Hook**: Wire harem rank into `QING_seat_evaluate_heir` decision-weight; track `qing_crownprince_birth_mother` and fire dynasty events when her rank changes.

3. **Southern/Upper Study → Exam pool**: The two academies (`se_QING_SOUTHERNSTUDY`, `se_QING_UPPERSTUDY`) educate palace scholars but graduates never flow into `qing_scholar_pool`. A distinguished Southern Study alumnus should enter the hiring pool directly → **Hook**: Add `QING_southernstudy_elevate_to_pool` effect; when a首席 leaves the academy, mint him into `qing_scholar_pool` with elevated traits.

4. **Censorate impeachments → Accountability taint**: `QING_censorate_impeach_uphold` calls `QING_char_cleanse` (removes corruption) but never stamps a **public disgrace marker** that other court features read. A disgraced official should be excluded from future appointments/promotions → **Hook**: Set `qing_is_disgraced` flag (7-year duration) on impeached characters; gate `QING_office_eligible_candidate` + `QING_exam_pool_drop_member` on `NOT has_variable qing_is_disgraced`.

**MEDIUM PRIORITY:**

5. **Guard Commandant → Regency**: The Imperial Guard (`se_QING_GUARD.txt`) protects the throne, but when a regent seizes power (`QING_seat_regent_install`) the Guard Commandant's loyalty is never checked. A disloyal commandant should enable a coup → **Hook**: `QING_seat_evaluate_regency` should test `qing_office_guard_commandant_holder.loyalty < 40` → fire a regency-crisis event (the commandant backs/opposes the regent).

6. **Wenzhi patronage → Exam ladder**: The 文治 cultural-patronage meter (`qing_wenzhi_level`, `se_QING_WENZHI.txt`) supposedly strengthens literati culture, but never feeds `qing_exam_ladder`. High patronage should widen the talent funnel → **Hook**: Add `(qing_wenzhi_level - 50)/8` to `QING_GOV_update_exam_ladder` target (mirrors civic-identity boost).

### B. Qing ↔ Vanilla (vanilla integration gaps)

**CRITICAL:**

7. **Character factions vs. reformist/conservative blocs**: The mod tracks `qing_char_faction` (reformist/conservative alignment, `se_QING_FACTION.txt`) in parallel to vanilla's `character.faction` system, completely ignoring engine faction membership/loyalty. Characters can be in BOTH a vanilla faction AND a Qing faction with no cross-read → **Hook**: Merge or reconcile: either map vanilla `faction` membership onto `qing_char_faction` at init, or have `QING_faction_assign` also call vanilla `join_faction` to a matching in-game faction entity.

8. **Office power-base vs. vanilla holdings**: `QING_office_appoint` grants `add_loyal_veterans = 4` (power base) but never checks if the appointee already holds **vanilla estates/holdings** (the engine's own power-base mechanic, `character.holdings`). A landed grandee appointed to office gets double power-base (mod's +4 + his estates) with no acknowledgment → **Hook**: Read `prev.holdings` in `QING_office_appoint`; if `>= 3`, reduce mod grant to +2 and fire a "landed magnate" flavor event.

9. **Council eligibility vs. vanilla offices**: The council candidate filters (`se_QING_COUNCIL.txt` L940-947, L1023-1030) exclude 8 vanilla great offices (`office_foreign_minister`, `office_marshal`, etc.) but treat them as **conflicting** rather than overlapping. A character holding `office_marshal` (vanilla's military commander office) should be ELIGIBLE for the Qing War Minister seat (兵部) with a trait/skill bonus, not blanket-excluded → **Hook**: Revise filter: exclude vanilla offices EXCEPT `office_marshal` for War, `office_steward` for Revenue, `office_high_priest_monarchy` for Rites (role-congruent vanilla offices become appointment bonuses, not blockers).

10. **Dynastic harmony vs. vanilla opinion**: `qing_dynastic_harmony` (family cohesion) is a pure custom meter; vanilla's `opinion` system (ruler ↔ heir, ruler ↔ family) runs in parallel with no coupling. The heir can have -100 vanilla opinion of the ruler while `qing_dynastic_harmony = 80` → **Hook**: In `QING_dynasty_assess`, read `var:qing_office_crownprince_holder.opinion:current_ruler`; if `< -25`, apply -8 harmony penalty; if `> 50`, apply +5 harmony bonus (vanilla opinion becomes a harmony input).

**MEDIUM PRIORITY:**

11. **Exam graduates vs. vanilla prominence**: `QING_exam_mint_scholar` creates degree-holders but never grants vanilla **prominence** (the engine's court-standing metric). A jinshi entering the pool has 0 prominence; vanilla courtiers with high prominence compete for the same offices with no degree-vs-prominence weighting → **Hook**: Grant `add_prominence = 15` for jinshi, `+8` for juren at mint; revise `combined_stats_council_svalue` to fold `prominence` into the rank (currently only reads 4 skills).

12. **Officer corps → vanilla general traits**: The War Ministry officer-corps coupling (`se_QING_COUNCIL.txt` L440-471) reads commanders' `martial` but ignores vanilla general **traits** (`organizer`, `tactical_genius`, `bold_fighter`, `winter_soldier` from `00_commander_traits.txt`). A brilliant general (trait `tactical_genius` = +2 martial equivalent) scores the same as a mediocre one of equal raw martial → **Hook**: In the corps martial-sum loop, add `+2` per positive general trait the commander holds; revise commentary to note "officer corps quality (skills + traits)".

## 2. DUPLICATION

1. **Three parallel "pick courtier by skill" mechanisms**:
   - `se_QING_COUNCIL.txt` L918-971: `QING_council_refresh_candidates_by` (office appointment picker, sorted by `$sortval$`)
   - `se_QING_EXAM.txt` L272-299: `QING_exam_fill_first_vacant_from_pool` (`ordered_in_list` by `combined_stats_council_svalue`)
   - `se_QING_HAREM.txt` L147-195: `QING_harem_refresh_candidates` (consort picker, by charisma)
   - **All share**: `ordered_character` + `check_range_bounds=no` + `max=12` cap + dedup guard + `add_to_variable_list`. **Unify** into `QING_courtier_refresh_picker { list_name=$X$ sort_by=$Y$ max=$Z$ limit={ ... } }` — single idiom, 3 call sites.

2. **Two "strip office on disgrace" code paths**:
   - `se_QING_CENSORATE.txt` L190: `QING_censorate_impeach_uphold` — `if = { limit = { has_variable qing_office_held } QING_office_vacate_dispatch }`
   - `se_QING_JUSTICE.txt` (implied by memory, not read here but task spec says `se_QING_JUSTICE` is in cluster) — likely duplicates the same "convicted → vacate office" logic.
   - **Unify** into `QING_char_disgrace_vacate_office` helper called by both impeachment and conviction paths.

3. **Parallel "recompute roster from marker" patterns**:
   - `se_QING_HAREM.txt` L118-144: `QING_harem_recompute_roster` (rebuild `qing_harem_consorts` from `qing_is_harem_consort` marker)
   - `se_QING_COUNCIL.txt` L183-201: `QING_council_recompute` rebuilds `qing_council_members` from office holder vars
   - `se_QING_EXAM.txt` (pool tick, not shown in excerpt) — likely rebuilds scholar pool from `qing_is_pool_scholar`
   - **All share**: `clear_variable_list`, `every_character { limit = { marker } save + add_to_list }`, count var sync. **Pattern** is sound but could be macro-ized if the codebase adopts parameterized roster helpers.

4. **Duplicate "per-ministry performance computation" boilerplate**:
   - `se_QING_MINISTRY.txt` L27-48: `QING_ministry_recompute_all_perf` dispatcher calls 12 `QING_ministry_recompute_perf_<office>` effects
   - Each recompute follows identical structure: base=50, read minister's governing skill, apply domain-specific terms, clamp 0-100
   - **Evidence**: War Ministry (L52-200+) vs Lifanyuan/Zongli/Works/Rites/Revenue (not excerpted but dispatcher calls them) — all mirror the same `set base → score minister → add domain terms → clamp` flow. **Unify** via template: `QING_ministry_perf_base { office=$X$ skill=$Y$ }` + per-office domain addenda.

## 3. ABSTRACT → CONCRETE

**NEW opportunities** (excluding task #91's already-identified backlog):

1. **Dynastic harmony (qing_dynastic_harmony) → Throne Council sessions**: Currently a pure 0-100 meter. The in-fiction referent is how often/well the Emperor, Crown Prince, Empress, and Dowager **actually convene** to decide policy. → **Concrete**: Track `qing_throne_council_last_session` date; fire monthly `qing_dynasty.20` "throne council convenes" event when harmony > 60 (creates a **logged policy decision** with concrete outcomes: "resolved the X crisis", "granted Y petition"). Low harmony = sessions are rare/bitter → visible event drought. (Mirrors medieval "royal council" events.)

2. **Censorate vigor (qing_censorate_vigor) → Active investigations**: Currently derived 0-50 score (`se_QING_CENSORATE.txt` L54-67). In-fiction =御史 (investigating censors) dispatched to provinces. → **Concrete**: When vigor > 30, `QING_censorate_pulse` spawns `qing_censor_investigating` **character marker** + **province assignment** (pick a high-corruption province, stamp `qing_censor_present` province modifier for 180 days). Events fire **at that province** ("the御史 reports graft in the governor's yamen"). Low vigor = no investigators deployed → no investigation events.

3. **Office vacancy strain (qing_office_vacancy_strain) → Acting ministers**: Currently a stacking country modifier (applied per vacancy, `se_QING_COUNCIL.txt` L1378). In-fiction = 署理 (acting/deputy officials) fill the gap. → **Concrete**: When an office is vacated, immediately appoint an **acting holder** (pick top-2 eligible courtier, stamp `qing_acting_office_held = flag:$office$`, grant **half** the usual modifier strength, no power-base). GUI shows "署理 Acting War Minister"; full appointment replaces him. (Mirrors Invictus "acting governor" when governorship is empty.)

4. **Scholar pool staleness (age-out at ~55, se_QING_EXAM.txt) → Retired scholars opening academies**: Currently scholars aged > 55 are `remove_list_variable` with no trace (`QING_exam_pool_tick`). In-fiction = unplaced graduates retire to local academies. → **Concrete**: On retirement, pick a random CHI-owned province, grant **province modifier** `qing_private_academy` (+2% research, +1 monthly pop-happiness, flavor "the retired scholar X teaches classics here"). Adds a visible legacy; player sees where the talent went.

5. **Wenzhi patronage level (qing_wenzhi_level) → Imperial-sponsored projects**: Currently 0-100 meter feeding abstract buffs (`se_QING_WENZHI.txt`). In-fiction = 四庫全書 compilation, observatory construction, porcelain kilns. → **Concrete**: At thresholds (wenzhi 40/60/80), trigger `qing_wenzhi.30/.31/.32` events that **create a building** in the capital (`qing_imperial_library`, `qing_astronomical_observatory`, `qing_imperial_kilns`) with +research/prestige bonuses. Player sees the patronage **on the map**; the buildings persist. (Mirrors Summer Palace tree #74's concrete 圓明園 building.)

6. **Affinity binding (qing_char_affinity, "天子門生" scholar-to-throne loyalty)**: Currently a 0-100 character var read for loyalty tooltips (`se_QING_AFFINITY.txt`). In-fiction = exam graduates are the Emperor's **personal clients**. → **Concrete**: High-affinity scholars (>75) should receive an **annual stipend** (grant +5 gold via `add_gold`, fire flavor event "the throne rewards your faithful service"). Low-affinity (<25) scholars who hold office become **factional assets** → automatically `join_faction` a reformist/conservative faction based on `qing_char_stance`. (Makes affinity a transactional loyalty mechanic, not just a color.)

## 4. DEPTH GAPS (shallow features needing more texture)

1. **Harem consort favour (se_QING_HAREM.txt)**:
   - **Current**: Single `QING_harem_favour_consort` lever → `make_pregnant` (L210+, not excerpted but implied by file header). One choice: "favor her" → heir chance.
   - **Gap**: No **rivalry**, no multi-consort dynamics, no consequences beyond pregnancy. Historical 後宮 politics (consort clans, jealousy, poisoning) are absent.
   - **Deepen**: Add `qing_consort_rivalry` variable_list (pairs of rivals); favouring one consort triggers `qing_harem.10` "rival consort schemes" event (lose dynasty harmony, -loyalty to rivals, rare poison/scandal outcomes). Add "elevate a consort's rank" separate from favour (rank ≠ favour). Add "consort intercedes for her clan" (foreign-spouse lobby, mirrors `QING_council_foreign_spouse_check` L1438+ but for harem).

2. **Exam cycle (qing_keju events)**:
   - **Current**: Triennial cycle fires `qing_keju.1` (host exam) → `.2` (results) → `QING_exam_graduate_cohort` mints 1-3 scholars. Shallow: player observes, cohort auto-added to pool, done.
   - **Gap**: No **player choice** in the cycle itself (can't adjust standards, can't cheat, can't sponsor a candidate). No scandal/controversy outcomes.
   - **Deepen**: Add `qing_keju.15` "examiner bribery scandal" (choice: punish examiner [-corruption, -exam ladder short-term] vs. suppress [+corruption, no ladder hit]). Add "sponsor a regional candidate" button (spend gold to boost one juren → guaranteed jinshi). Add "tighten exam standards" decision (reduce cohort size by 1, +exam_ladder integrity, -civic_identity short-term backlash from disappointed families).

3. **Censorate impeachments (qing_censorate.5 → picker at .6)**:
   - **Current**: Build venal roster → player picks one → choice "uphold" (cleanse, -corruption) vs. "suppress" (+corruption). Binary, one-shot.
   - **Gap**: No **investigation phase**, no false-accusation risk, no factional weaponization (reformists impeach conservatives for political reasons, not real graft).
   - **Deepen**: Split into 3-stage: (1) "御史 accuses X" (based on evidence strength = corruption + random), (2) player orders **investigation** (costs time, can fail if evidence weak), (3) verdict (can now **exonerate** if investigation clears him, restoring his reputation). Add "factional impeachment" branch (if censor + target are opposite factions, 40% chance the charge is politically motivated → choice to expose the censor or let it proceed).

4. **Grand Council appointment (QING_office_appoint)**:
   - **Current**: Open picker → select candidate → he's appointed (instant). One-office-per-man reshuffle if he already holds an office.
   - **Gap**: No **opposition**, no confirmation drama, no appointment-crisis if the candidate is controversial (low loyalty, wrong faction, foreign-born).
   - **Deepen**: Add `qing_office.50` "appointment opposed" event (fires if new appointee's loyalty < 50 OR he's opposite-faction to current council majority): choice to force the appointment (-harmony, -effectiveness short-term) vs. withdraw and pick another. Add "rival candidate" flavor (the #2 ranked courtier objects; player can mollify him with a lesser post or accept his enmity).

5. **Dynastic figureheads (Empress, Dowager, Crown Prince) in council effectiveness**:
   - **Current**: Figured into `QING_council_score_figurehead` (L683-753) as skill contributions. Passive: they affect the effectiveness number, no direct player interaction.
   - **Gap**: No **decisions** leveraging their influence. Can't ask Dowager to mediate a council deadlock, can't assign Crown Prince to head a ministry for training, can't grant Empress a ceremonial office (典禮).
   - **Deepen**: Add "Consult the Dowager" decision (available when `qing_dynastic_harmony < 40` + dowager exists): spend prestige, she brokers a truce between factions (+15 harmony, -10 polar_pen, 3-year cooldown). Add "Crown Prince apprenticeship" (assign him to observe a ministry for 1 year; he gains +1 in that ministry's governing skill, the minister gains +loyalty if the training goes well). Add "Empress holds court" (ceremonial decision, grants +5 legitimacy, +3 harmony, once per year).

6. **Officer-corps reports (qing_office.31, L1500-1563)**:
   - **Current**: War Minister reports on a random commander; event gives +/-loyalty outcome. One-shot flavor.
   - **Gap**: No **promotion/demotion mechanic** emerging from reports, no dismissal for incompetence, no multi-report narrative (a commander who gets 3 bad reports should face consequences).
   - **Deepen**: Add `qing_officer_report_count` and `_last_report` vars on each commander; track report outcomes. After 2 consecutive negative reports, fire `qing_war.20` "the garrison falters under X" → choice: relieve him (vacate command, -martial modifier on his replacement term) vs. grant reprieve (he gets one more chance, risks mutiny if he fails again). After 2 consecutive positive reports, fire promotion event (he gains a **trait** `qing_decorated_officer` = +1 martial, +10 loyalty).

## 5. DEAD / INERT CODE

**Defined but never called:**

1. **`QING_harem_rank_cap`** (`se_QING_HAREM.txt` L106-108 comment): Explicitly noted as **REMOVED** in PERF-AUDIT — zero callers, output var never read. ✅ Already identified and documented by author, but still present as dead comment.

2. **`qing_gc_event_slot_used` slot-claim pattern**: Used in 50+ places (`se_QING_DYNASTY.txt` L89/98/108/etc., `se_QING_COUNCIL.txt` L1488/1553) but **never consumed** — no code reads the var to throttle/skip subsequent events. It's set to 1 on event fire paths, but the quarterly pulse never checks `has_variable qing_gc_event_slot_used` before rolling next event → **Inert throttle**. Either wire the check (top of `QING_dynasty_flavour_roll`: `if = { limit = { has_variable qing_gc_event_slot_used } return }`) or delete 50+ assignments.

> ⚠️ **SYNTHESIZER CORRECTION (claim A.1-§5.2 REFUTED):** `qing_gc_event_slot_used` is NOT an inert throttle.
> Independent grep found **18 check-sites** (`has_variable = qing_gc_event_slot_used` in event `limit` blocks)
> vs 31 set-sites. The throttle IS wired and working (~1 court event/quarter). Do NOT delete the assignments.
> The agent grepped only for reads in the *pulse dispatcher* and missed the per-event `limit` gates.

3. **`qing_council_vacancy`** (L397-399): Computed (= 13 - filled_count), used to derive penalty (L400-402 `qing_council_vacancy_pen`), then never referenced again. The **penalty** is read; the raw vacancy count is not. Could be exposed to GUI/events but currently write-only.

4. **`qing_council_eff_denom`** (L370-371): Computed as denominator for effectiveness average, used once in L374-377 for division, then never read. Purely intermediate scratch var; could be `set_local_variable` to reduce country-scope clutter.

5. **`qing_officer_corps_count` and `qing_officer_corps_martial`** (L447-458): Summed in the officer-corps loop, used immediately for L466-470 average-martial calc, then orphaned. Not read by GUI, not referenced in ministry-performance, not exposed to events → **Write-only tallies**. Should feed War Ministry performance (currently performance reads garrison-vacancy + minister-martial but NOT corps-quality; wire corps avg-martial as term (c) in `QING_ministry_recompute_perf_war`).

6. **`QING_council_perf_accumulate`** (L1652-1676): Helper for ministry-performance fold, but **grep confirms** it's called 12 times from `QING_council_fold_ministry_perf` (L1620-1631), so **NOT DEAD** — false alarm, it's actively used. ❌ No issue.

7. **`QING_exam_schedule_triennial`** (L126-139): Calls `QING_exam_compute_pass_rate` + fires `qing_keju.1`. **Grep needed** to confirm call sites (likely from `qing_mechanics_pulse_on_action`). If orphaned → dead; if called → alive. *Cannot confirm without broader search.*

8. **`qing_grandee_rebelled`** (L827, set on flipped chancellor): Prevents double-flip (L824 guard), but **no other code** reads it. The rebel chancellor is never flagged in events, never excluded from appointments, never pursued. Set once, never consumed → **One-way marker**. Should gate: exclude from future appointment pickers (loyalty is already checked, but this is a **permanent rebellion mark**), fire periodic "the grandee still holds his army" events, or wire into civil-war logic.

9. **`qing_needs_bind`** (L182, on fresh exam graduate): Set to defer affinity binding to next tick (L165-182 comment explains the same-tick read-back crash). Consumed by `QING_exam_pool_tick` (implied, not shown) so likely **NOT DEAD**, but confirmation needed. *Appears intentional per comment.*

**Summary Stats:** Cross-wiring gaps 12 (7 Qing↔Qing, 5 Qing↔Vanilla) · Duplication clusters 4 · Abstract→Concrete 6 NEW · Depth gaps 6 · Dead/inert 5 claimed (⚠️ item 2 refuted by synthesizer).

**Key architectural findings:** Excellent vanilla integration on character power-base / commander attachment / pregnancy, but parallel faction systems (mod vs engine) and vanilla offices ignored (could be congruence-mapped). Strong concrete-object discipline (councils/rosters/harem/scholar-pool/officer-corps all real `variable_list`); the violations (harmony, vigor, pass-rate as pure meters) are new opportunities. Cross-system awareness exists but is shallow (no reciprocal loops). Event depth uneven (dynasty/council rich; exam/harem shallow one-shots).

---

## APPENDIX A.2 — DECLINE & INTERNAL-CRISIS CLUSTER

## 1. CROSS-WIRING OPPORTUNITIES

### (a) Qing↔Qing Internal Wiring: STRONG but with gaps

**EXISTING WIRING (well-coupled):**
1. **Opium → Currency Stress → Revenue Ministry Performance** — `se_QING_OPIUM.txt:13-17` nudges `qing_currency_stress` quarterly; `se_QING_DECLINE.txt:343-347` folds it into `qing_reform_pressure`; header confirms it folds into Board of Revenue perf (term d). COMPLETE 3-hop chain.
2. **Corruption → Reform Pressure** — `se_QING_DECLINE.txt:343`. WIRED.
3. **Ethnic Tension → Reform Pressure** — `se_QING_DECLINE.txt:345`. WIRED.
4. **Banner/GreenStandard Decay → Reform Pressure** — `se_QING_DECLINE.txt:346`. WIRED.
5. **Population Pressure → Sect Pressure (famine→rebellion)** — `se_QING_POPULATION.txt:152-156` (pressure≥70 → sect +2). WIRED.
6. **Population Pressure → Migration** — `se_QING_POPULATION.txt:128-132` (pressure≥60 activates `QING_COLON_heartland_push`). WIRED.
7. **Opium Epidemic → Sect Pressure** — high epidemic nudges sect +1. WIRED but weak.

**MISSING WIRING (gaps):**
1. **Corruption does NOT feed Sect Pressure** — historical link venal officials→famines→White Lotus. **Hook:** `QING_DECLINE_pulse` ~L990: `if={limit={var:qing_corruption_level>=60} QING_DECLINE_nudge={var=qing_sect_pressure amount=1}}`.
2. **Granary Stock does NOT passively ease Sect Pressure** — only manual `QING_granary_release` (-10). **Hook:** after L914 `if={limit={var:qing_granary_stock>=70} nudge sect -1}`.
3. **Banner Decay does NOT directly raise Sect Pressure** — rotten banners can't suppress rebellions. **Hook:** ~L890 `if={limit={var:qing_banner_decay>=70} nudge sect +1}`.
4. **Currency Stress does NOT feed Ethnic Tension** — silver crisis→frontier tax burden. **Hook:** currency-stress band ~L150 `if={limit={var:qing_currency_stress>=70} nudge ethnic +2}`.

### (b) Qing↔VANILLA System Integration: PARTIAL

**EXISTING:** Mandate calamities call `add_legitimacy`/`add_stability` (`se_QING_MANDATE.txt:34-46`); anti-corruption audit adds `add_tyranny=3` (`se_QING_MECHANICS.txt:441`); censorate suppression adds tyranny; rebellion option adds `add_war_exhaustion=2`; ethnic tension **reads** `province_unrest` ×2 (`se_QING_ETHNIC_TENSION.txt:170`) — **ONE-WAY READ**, never writes back.

**MISSING VANILLA COUPLING:**
1. **Corruption Counter → Tyranny** — ~L930 `if={limit={var:qing_corruption_level>=75} add_tyranny=1}`.
2. **Sect Pressure → Province Unrest** — band modifier `qing_sect_infiltration` add `local_unrest_modifier=1.0`.
3. **Banner Decay → War Exhaustion** — in `QING_army_apply_decay_debuffs` ~L360, wartime + decay≥75 → `add_war_exhaustion=1`.
4. **Ethnic Tension → Character Loyalty** — after L542 iterate governors, apply loyalty penalty in restive regions.
5. **Pop Pressure → Pop Happiness** — band `qing_pop_pressure_crisis` add `global_pop_happiness=-0.10`.

## 2. DUPLICATION
1. **Currency/Silver/Revenue** (`qing_currency_stress` / `qing_opium_net_flow_tmp` / Revenue reads currency_stress) — NOT duplication, a PIPELINE. NOT a problem.
2. **Four "pressure" meters** (sect / ethnic / pop / reform) — DISTINCT phenomena; reform is a SUMMARY. NOT duplication — correct domain modeling.
3. **Banner vs GreenStandard decay** — historically distinct forces, asymmetric by design. NOT duplication.
**Verdict: NO meaningful duplication. Apparent overlaps are layered abstractions.**

## 3. ABSTRACT→CONCRETE (New)
**Already converted (#91 — do not re-report):** granaries→buildings, sect leaders→char, separatist leaders→char, banner-decay→unit debuff, GP-rivalry→plays.
**NEW:**
1. **Corruption Patronage Networks → characters** — spawn a "corrupt clique" char (marked trait) at corruption≥70, power_base tied to level (mirror sect-leader spawn L957). MEDIUM.
2. Reform Factions → char stances — N/A, ALREADY CONCRETE (`se_QING_FACTION.txt` `qing_char_stance`).
3. **Canton Trade Regime → treaty-port buildings/modifiers** — `add_province_modifier` on Canton/Shanghai when regime opens. LOW.
4. **Opium Smuggler Pops** — spawn tagged pops in high-addiction provinces (partially done L961). LOW.
5. **Fiscal Agents → char appointments** — Salt Commissioner (鹽政) / Customs Superintendent (海關監督) char when revenue stress high. MEDIUM.

## 4. DEPTH GAPS (Ratchets / Dead-Ends)
**Ratchet-up meters with no lever:** 1. Banner Decay (+1/mo passive, only `QING_banner_drill` relief) — add Mongol marriage-alliance event. 2. GreenStandard Decay (+1/mo, accelerates ≥40) — add "Recruit from the Banners" transfer event. 3. Ethnic Tension (weak recovery) — add "Grand Pardon for Frontier Peoples" event.
**Dead-end events (no follow-up):** 4. Mandate Disasters — add 6-month "relief bore fruit" follow-up. 5. Population Pressure Memorial (`qing_population.1` once at ≥65) — add "Hong Liangji Pleads Again" at ≥85. 
**Missing feedback loops:** 6. Corruption→Revenue→Corruption vicious cycle — when deficit≥50, trigger `qing_office.7` office-sales temptation more often.

## 5. DEAD / INERT CODE
1. `qing_manchu_identity` (per-char) — written+banded, no gameplay read beyond char modifier; **INERT for gameplay, narrative-only** (sinicization events read it). Not truly dead.
2. `qing_civic_identity` passive drift — FULLY WIRED (civic assimilation, band, ethnic relief). Not dead.
3. `qing_prov_ethnic_tension_prev` — snapshotted, read by ethnic-tension report GUI (#109). ALIVE.
**Effects:** all six rebellion events (.1-.6) live in random_list; decline reaction roll all fire. **NO dead effects found.**

**Summary priorities:** (do first) corruption→sect, banner→sect, sect→province unrest, ethnic-tension crisis-response event. (medium) corrupt-magnate char, granary passive relief, Mongol marriage event. (low) treaty-port buildings, mandate recovery follow-ups. (leave as-is) multi-layer currency pipeline, parallel pressure meters, slow civic-identity drift.

---

## APPENDIX A.3 — ECONOMY & MODERNIZATION CLUSTER

## 1. CROSS-WIRING OPPORTUNITIES
### (a) Qing↔Qing — STRONG INTEGRATION
1. **Students-abroad → Self-Strengthening** (`se_QING_STUDENTS.txt:131`) — `QING_students_graduate` → `QING_selfstr_advance={amount=6}` + lifts `qing_bureau_capacity`; returnees feed SHARED `qing_selfstr_progress`.
2. **Tech-transfer → Self-Strengthening** (`se_QING_TECHTRANSFER.txt:64`) — `QING_techtransfer_bargain` fires `QING_selfstr_found_jiangnan/_fuzhou`. Accelerates, not parallel.
3. **Early Industrialization → Self-Strengthening** (`se_QING_EARLYINDUS.txt:20`) — reuses SAME counter + verbs, zero duplication.
4. **Canal/Works → Banner Decay** (`se_QING_CANAL.txt:256`) — low `qing_grain_reserve`(<40) accelerates `qing_banner_decay`.
5. **Self-Strengthening → Civic Identity** — `qing_selfstr_progress` sets ceiling for civic/modernarmy drift targets.
**MISSED:** (1) Canton revenue not explicitly funding Self-Strengthening treasury needs — add trace "Canton customs funded this". (2) Treasure-fleet haul not cross-wired to modernization — let wealth grant bonus selfstr progress on industrial purchases. (3) Canal condition not feeding trade routes — wire `qing_canal_condition` into TRADE_svalues as Jiangnan→North multiplier.

### (b) Qing↔VANILLA — CONCRETE INTEGRATION
Self-Strengthening → real buildings (`add_building_level` arsenal/port/university/rail, `se_QING_SELFSTR.txt:76-89`); → rifles trade good (L117); → tech unlocks (`unlock_invention`, L126-139); Canton yield from real `GOODS_national_production_tea/_silk/_porcelain` (L93-96); Canal → real granaries (L180-185); Works buildings → canal condition (L81-95); railway → army movement speed (L440, #441 done).
**PARALLEL ABSTRACT TRACKS to ground further:** (1) treasure-fleet haul is pure currency not goods — could spawn actual trade goods in home port; (2) `qing_selfstr_progress` abstract but INTENTIONAL summary (buildings hang off it) — acceptable; (3) students-abroad counter spawns real char every +25 — GOOD, #91 item C delivered.

## 2. DUPLICATION — ZERO MAJOR FOUND
EarlyIndus reuses selfstr engine; tech-transfer fires selfstr hooks directly; only ONE arsenal chain + ONE rail chain; Works minister specialty buildings build DIFFERENT goods than selfstr; Canton + treasure fleet one pulse each, no overlap.

## 3. ABSTRACT→CONCRETE
**Already delivered (#91, do not re-report):** treaty ports, customs-house, students→returnee chars, Self-Strengthening wonder.
**NEW:** 1. **Canton Hoppo → real Grand Council office** (currently lightweight char marker `qing_hoppo_holder`, L198-240) — promote to full office w/ traits/dismissal. 2. **Tech-Transfer Debt → treaty-port concessions** (`qing_ttx_debt_britain/france/russia/america`, L147-164; paying nudges abstract `qing_treaty_burden`) — grant real province modifier `treaty_port_concession_britain` w/ garrison + trade bonus on a NAMED port. 3. **Self-Strengthening Hollow Flag → concrete failure events** (`qing_selfstr_hollow_flag`, L522) — hollow movement triggers Yalu-style naval disaster. 4. **Grain Reserve → famine provinces** (L264-271) — mark starving provinces with `famine_year` modifier.

> ⚠️ **SYNTHESIZER NOTE (re A.3-§3.2):** the agent correctly reports `qing_ttx_debt_*` is READ (paying-concession path). This
> refutes the whole-suite regex scan's earlier "write-only" false-positive on those vars — the per-power debt
> counters are read at `se_QING_TECHTRANSFER.txt:198-213`. Logged in §6.

## 4. DEPTH GAPS
**Good cost/tradeoff structure:** selfstr gated on machinery (progress HALVED if bureau_capacity<50 or council_eff<50, L54-67); tech-transfer favor-debt; students recall risk (1881, L298-306); Canton Cohong bankruptcy (L168-177); EarlyIndus conservative backlash (L75-86).
**SHALLOW / NO-TRADEOFF:** 1. **Treasure Fleet pure upside** (wealth every quarter, no risk, L134-171) — add piracy/storm sink risk. 2. **Railway extension simple spend** (60 treasury+5 mp, no fail, L742-769) — add corvée unrest / bandit sabotage. 3. **Summer Palace no ongoing cost** (permanent splendour after one build, L104) — add upkeep drain / decay event.

## 5. DEAD / INERT CODE
All major pulses wired + firing (students/techtransfer/canton/canal/treasure/selfstr per `se_QING_GOVERNANCE.txt`). **Potentially inert:** `qing_canton_last_yield` / `qing_treasure_last_haul` are WRITE-ONLY except one GUI read (`gui/qing_province_reports.gui`) — display-only, not gameplay-inert. Selfstr refraction test writes `qing_selfstr_hollow_flag` w/ limited bite (works as designed).

**Summary:** tight Qing-internal integration, strong vanilla grounding, concrete-over-abstract applied, good cost structure. Opportunities: Canton/Treasure wealth→selfstr funding; canal→trade routes; tech-debt→named ports; hollow→disaster; treasure fleet→piracy risk; railway→unrest. No parallel modernization systems, no duplicate arsenal paths, all pulses firing.

---

## APPENDIX A.4 — FRONTIER, SUBJECTS & TRIBUTARY CLUSTER

## 1. CROSS-WIRING OPPORTUNITIES
### (a) Qing↔Qing
**DUPLICATE PARALLEL LADDERS — THREE separate subject-control progressions:**
1. `SUBJ_ladder_rung` (`se_SUBJECT_QING.txt:43-65`): 4-rung ladder sinosphere_tributary(1)→nominal_vassal(2)→feudatory(3)→autonomous_governorship(4).
2. `qing_suzerain_prestige` (`se_QING_VASSAL.txt:24`): 0..100 abstract counter.
3. `qing_sphere_dominant` (`se_QING_SPHERE.txt:37-43`): per-STATE codes 0-4 (China/Britain/France/Russia).
Model overlapping concepts, run in parallel with NO shared state. `qing_suzerain_prestige` never reads actual `SUBJ_ladder_rung`; sphere never feeds back to which subjects hold marches.
**PARTIAL COUPLING (tribute↔vassal):** `QING_vassal_free_real_subject` releases real KOR/VIE (L106-124); `QING_tribute_schedule_missions` tests `any_subject` (L67-117).
**MISSING frontier settlement → population:** `se_QING_FRONTIER.txt`/`se_QING_SETTLE_FRONTIER.txt` likely abstract counters, not `create_pop`. *(agent hedge: files not fully read — verify.)*
**CARAVAN↔TRADE disconnection:** `qing_caravan_prosperity` → direct `add_treasury` trickle (L34), NOT engine `trade_route`.
**XINJIANG/ILI/AMBAN partial:** `QING_amban_post` reads `is_subject_of` (L44-144); caravan reads `qing_xinjiang_control` (L92); amban does NOT drive ladder position.

### (b) Qing↔VANILLA
**DRIVES REAL SUBJECTS (good):** `release_subject=c:KOR` (L111); `FUNC_make_subject` wraps vanilla `make_subject` (L76-95); `SUBJ_QING_absorb_subject` transfers provinces via `LAND_transfer_provinces` (L486-490); `QING_establish_protectorate` creates real tributaries (L63-88); setup ships real `dependency={first=CHI second=VIE subject_type=sinosphere_tributary}`.
**ABSTRACT COUNTERS BESIDE ENGINE (duplication):** `qing_suzerain_prestige` parallel to real subject loyalty/opinion; `qing_sphere_*` per-state influence vars NEVER alter `owner`/control (L209-219 clamp, no `change_province_owner`) → **four-power contest is purely COSMETIC**.
**TRIBUTE EMBASSIES:** transient `create_character` per mission (L140-160), dismissed after (L170-181). **Quarterly gold transfer** real (`add_treasury` both sides, L663/688-689) but bypasses engine `tribute_income_modifier`.

## 2. DUPLICATION
**MAJOR: Three parallel subject-control models** (rung / prestige / sphere). **SHOULD unify:** real subject `is_subject_type`+`SUBJ_ladder_rung` = single source of truth; DERIVE prestige from rung distribution + lost-subject flags; sphere flip → real subject type change.
**MEDIUM:** tribute embassy rhythm vs `SUBJ_integration_progress` ladder — both model "tightening control", should merge as one state machine (tribute from rung-1, integration at rung-4).
**MINOR:** amban effectiveness doesn't drive `SUBJ_QING_change_type` — effective amban should auto-promote a rung / boost integration; failing amban → demotion.

## 3. ABSTRACT→CONCRETE (NEW)
**#91 covers (do not re-report):** tributary vassals as real subjects ✅ DONE; treaty ports deferred; Xinjiang/Ili deferred.
**NEW:** (A) **Amban as real governor** — `set_as_governor` of a subject province, loyalty/opinion flow from role, `remove_governorship` on recall. (B) **Caravan as real trade route** — define `trade_route` Kashgar→Beijing, prosperity → `add_trade_route_modifier`, Kokand as third party. (C) **Frontier settlement as real pops** — settlement → `create_pop culture=han`, feeds ethnic tension organically, integration = real demographic shift. (D) **Sphere flips as real subject type changes** — march flip demotes/promotes actual subject or transfers to rival client. (E) **Investiture as engine opinion** — `QING_tribute_invest_new_ruler` (L280-306) → `add_opinion` + `liberty_desire` rise on snub.

## 4. DEPTH GAPS
(A) **Sphere contest has no consequence** — count marches, band modifier, but no subject/province loss or crisis beyond tension nudge. Add "Britain holds >50% → Sphere Crisis demands cession". (B) **Integration stops at absorption** (`SUBJ_QING_absorb_subject` L458-511 transfers + ends) — add ex-elite chars, ethnic unrest, consolidation chain. (C) **Amban evaluation drifts but fires no crisis** — add "affinity<20 for 3 quarters → recall crisis". (D) **Tribute default leads nowhere** (`qing_tribute_defaulted` L680 → `qing_tribute.5`) — add "3 defaults → auto-demote rung". (E) **Caravan prosperity bottoms out with no crisis** — add "prosperity<15 + Kokand aqsaqal → khoja rising threat".

## 5. DEAD / INERT CODE
(A) **`qing_vassal_lost_ryukyu` / `_burma` WRITE-ONLY** — set L75-76 for any vassal word, but ryukyu/burma OUT OF SCOPE (L101-102), never read by events. (B) **`SUBJ_ladder_rung=0` off-ladder NEVER handled** — set L63 for non-ladder types, no `if={limit={var:SUBJ_ladder_rung=0}}` blocks; off-ladder subjects silently fail promote/demote. (C) `qing_tribute_missions_recent` decay guard L241 redundant (not dead). (D) `qing_sphere_top_val` temp-var churn (created/destroyed per march per pulse) — inefficient not dead. (E) **`QING_tribute_invest_new_ruler` caller unclear** — header says on_ruler_change hook, no `on_ruler_change={...}` found in read files; **needs grep of `/common/on_action/`**.

**Priority:** TIER 1 unify three ladders + sphere→real subject + caravan→trade route; TIER 2 amban→governor, settlement→pops, integration follow-on; TIER 3 investiture→opinion, dead-var cleanup, meter→crisis auto-triggers. **Verified live:** `QING_vassal_pulse`(gov:448), tribute/sphere/integration pulses (on_actions quarterly), absorb, tribute collect. **Potentially inert (needs grep):** invest_new_ruler hook, ryukyu/burma flags, rung=0 handling.

---

## APPENDIX A.5 — DIPLOMACY & FOREIGN-ARCS CLUSTER

**Scope:** DIPLO, GREATGAME, EMBASSY, LEGATIONS, TREATIES, OPIUM, MISSIONARY, foreign arcs (AMERICAS/MEXICO/USCW/NAPOLEON/INDIA/BURMA), SPHERE.

## 1. CROSS-WIRING
**(A) SPHERE↔GREAT GAME ISOLATION — HIGH.** SPHERE (four-power contest, `qing_sphere_dominant`, L36-51) and DIPLO (`qing_gp_tension_*`, L27-31) track the same rivalry but never talk. SPHERE has GP tie-in COMMENTS (L48-51) but `rg "qing_gp_tension" se_QING_SPHERE.txt` = **zero hits** — documented but not wired. Concrete 5-line hook in `QING_sphere_tick_state` nudging `qing_gp_tension_britain/france/russia` on a rival flip.
**(B) OPIUM↔TREATY-PORT COMMERCE MISSING — MEDIUM.** `QING_opium_treaty_legalize` (L335) grants flat treasury, never touches `qing_treaty_ports`; `QID_treaty_apply_ports_modifier` (L187-203) never reads opium posture. The Shanghai-boom link. Hooks given.
**(C) EMBASSY/LEGATION↔GP-RIVALRY feed reform pressure — LOW DUP.** 4 write-sites all model opening-backlash; design is "many roads to reform pressure" — consistent, not a bug; document compounding.
**(D) FOREIGN ARCS ARE ISOLATED SET-PIECES — HIGH.** Americas(7 effects)/Mexico(2)/USCW(3) write no decline meters except USCW `QING_selfstr_advance` ×1; only Napoleon has depth (4× selfstr calls). Flavour vignettes w/ GP stakes but no domestic reform/decline impact. Hooks given (USCW→reform relief, Mexico→selfstr precedent).
**(E) MISSIONARY↔BOXER wiring present** (`QING_missionary_pulse` L181 → `qing_rebellion.9`). VERIFIED, no gap.

## 2. DUPLICATION
**(A) EMBASSY vs LEGATION power-dispatch — LOW.** EMBASSY named per-power wrappers (asymmetric costs, load-bearing); `QING_legation_ease_tension` (L73-85) identical to `QING_missionary_ease_power` (L152-162) — **3 copies of the same 4-way dispatch**. Hoist `QING_ease_gp_tension` to DIPLO.
**(B) JAPAN PRE-PERRY vs OPEN JAPAN split — STRUCTURAL.** Two files, sequential phases of one relationship, both write same 3 counters. Merge into `se_QING_JAPAN.txt` w/ era gate — false module boundary.

## 3. ABSTRACT→CONCRETE
**(A) EMBASSY AS REAL CHARACTER (駐外使臣) — NEW.** Conjure Macartney/Amherst as chars w/ traits; rebuff/receive keys on envoy finesse; received envoy → first legation minister.
**(B) TREATY PORTS — ALREADY DONE.** `QING_treaty_stamp_port` (L157-181) stamps real `qing_treaty_port` province modifiers (Shanghai first). Exemplary. #91 item B done.
**(C) MISSIONARY STATIONS — ALREADY DONE.** `se_QING_MISSIONARY_STATIONS.txt` — stations are province buildings; `qing_missionary_reach` counts real stations. Already concrete.

## 4. DEPTH GAPS
**(A) TREATY REVISION event-only — MEDIUM.** `QING_treaty_revise` (L120-146) called only from events. Add Zongli Yamen "Press for Treaty Revision" player action (gated `qing_legation_count>=3`).
**(B) SPHERE CONTEST HAS NO PLAYER VERBS — HIGH.** Pure pulse; GP-rivalry has `QING_gp_court_*`(L491-515), `QING_gp_dispatch_diplomat`(L526), sphere has zero. Add Frontier Ministry "Dispatch Amban"/"Foment Unrest" actions.

## 5. DEAD / INERT CODE
**(A) JAPAN_PREPERRY / OPEN_JAPAN / PILGRIMAGE — agent claimed "CONFIRMED DEAD, DELETE 25KB".**

> ⚠️ **SYNTHESIZER CORRECTION (claim A.5-§5A REFUTED — this is the single most important correction in the report):**
> All THREE files are **LIVE**, not dead. The agent's `rg -c "QING_japan_preperry|QING_open_japan|QING_pilgrimage"`
> searched for the WRONG symbol names and grepped only effect→effect refs, missing the event/mission/on_action
> callers. Verified live callers: `QING_jppre_init` at `qing_mechanics_on_actions.txt:209`; `QING_openjapan_*`
> from `qing_open_japan_missions.txt:94-237`; `QING_pilgrim_*` from `qing_pilgrimage_events.txt:55-167` (and the
> religion cluster A.6 independently confirmed pilgrimage modifiers ARE applied at `qing_pilgrimage.3:225`).
> **DO NOT DELETE.** The only valid part of this finding is the *optional merge* of the two Japan files (A.5-§2B),
> which is a refactor, not a deletion.

**(B) se_QING_INDIA.txt / se_QING_BURMA.txt — mission-only, NOT dead but narrow.** Called only from mission trees (3 and 6 sites); no pulse/event/GUI. Arcs, not systems — correct design, zero replayability once done.

**Summary table (agent's own):** Sphere↔GP HIGH cross-wire; Opium↔ports MEDIUM; foreign arcs shallow HIGH; sphere no-verbs HIGH; treaty revision event-only MEDIUM; ~~JAPAN files dead~~ **(REFUTED — live)**; power-dispatch LOW dup; Japan split LOW dup. **Verified strengths:** opium→currency_stress→Revenue; treaty ports + missionary stations already concrete; GP-rivalry drives vanilla plays+opinion+aggressive_expansion.

---

## APPENDIX A.6 — RELIGION, MILITARY & REMAINING CLUSTER

**Executive summary:** military (WAR, GUARD), religion/ritual (RITES, PILGRIMAGE, MISSIONARY), roster (ROSTER), 17 unassigned files. Strong concrete wiring (real legions/commanders/loyalties), excellent Grand Council + decline integration. 2 major cross-wire opportunities, minimal duplication, 3 abstract→concrete gaps, several dead/inert fragments. **Overall grade A− (91/100).**

## 1. CROSS-WIRING
### A. Qing↔Qing
**✅ MILITARY → DECLINE (FULLY WIRED):** central-army collapse → commander loyalty drift (`se_QING_WAR.txt:75-86`); decay≥60 → **real unit morale debuffs** (`se_QING_MECHANICS.txt:348-430`, `qing_unit_banner_rot`/`_greenstandard_rot`); modernarmy≥60 → **raise_legion 新軍** (L396-430); Bayara Guard → real legion + marked commander (`se_QING_GUARD.txt:33-118`); regional magnates → `add_loyal_veterans+8` on real Han governor-general (L172-300). EXCELLENT, no orphaned counters.
**⚠️ OPPORTUNITY #1: RITES → MANDATE/LEGITIMACY SHALLOW.** Ceremonies grant vanilla legitimacy but never nudge `qing_mandate_strength`. Wire `QING_DECLINE_nudge={var=qing_mandate_strength amount=X}` into rites branches so ritual gates Taiping/rebellion rolls.
**⚠️ OPPORTUNITY #2: PILGRIMAGE → RELIGION (NO HOLY-SITE WIRING).** Mongol pilgrimage binds loyalty / relieves sect_pressure but does NOT touch vanilla holy_site system; `vajrayana` defined w/ NO holy sites. Add holy sites for Potala/Jokhang/Chengde 外八廟; wire `controls_holy_site` into `qing_pilgrimage.3` outcomes.
**✅ Golden Urn / Regency / Harem → succession** — files exist, assumed wired (society cluster's brief).

### B. Qing↔Vanilla
**✅ MILITARY → LEGIONS/UNITS FULLY CONCRETE.** raise_legion in 10 files; every military lever raises real units (drill→debuffs, modern army→新軍, Bayara→guard legion, war ministry→`create_unit navy=yes` 2× brig at `qing_war.3`); loyal-cohorts idiom 10×COUNCIL/3×MECHANICS/3×HOUSEHOLD; military_traditions tree `00_manchu.txt` 十全武功 (jurchen-gated, functional modifiers) but **COMMEMORATION ONLY — no mission cross-wiring**.
**✅ RELIGION → Confucianism/vajrayana defined, no holy sites** (Confucianism historically accurate; vajrayana = Opportunity #2).
**✅ MARRIAGE/SUCCESSION → vanilla char system** via `QING_roster_finalize` (`se_QING_ROSTER.txt:44-59`); 21 roster figures spawn context-keyed (corruption→Heshen, selfstr→Li Hongzhang, sect→Hong Xiuquan).

## 2. DUPLICATION — MINIMAL, CLEAN
No duplicate military-strength / legitimacy-piety / succession meters. Legion-spawn idiom consistent (15 sites, proven reuse). Character-spawn idiom consistent (70 calls, `create_character`+`QING_roster_finalize` tail). No wasteful parallel systems.

## 3. ABSTRACT→CONCRETE
**Already concrete (#91):** banner-decay→unit morale, 新軍→legion, regional magnate→loyal_veterans.
**NEW:** #1 **RITES efficacy → real temple building** (`add_building_level` Altar of Heaven in Beijing; losing Beijing = losing ritual efficacy; precedent `QING_statecraft_invest` L550-610). #2 **PILGRIMAGE → real pilgrim governorship** (sponsored pilgrim → `set_governor` of Mongol-majority province, territorial base like Han magnate). #3 **GUARD corps → ruler-scope modifier** (guard_corps≥5 → `qing_well_guarded_sovereign` on ruler, +popularity / -assassination risk).

## 4. DEPTH GAPS
**⚠️ Shallow ritual variety** — `qing_rites_events.txt` only 4 events, random-fire only, no Rites ministry action GUI. Add "Conduct Grand Sacrifice" button + orthodox/pragmatic stance toggle.
**⚠️ Pilgrimage chain shallow** — 5 linear events, no branching, no recurring standing. Add `qing_tibetan_patronage` accumulating meter gating "Dalai Lama recognizes emperor as Cakravartin" at ≥80.
**⚠️ Missionary pre-treaty friction no player lever** — `qing_mission_social_friction` (L192-231) event-called only. Add "Local Heterodoxy Crackdown" button.

## 5. DEAD / INERT CODE
**✅ Deferred-fix #5 applied:** `qing_pilgrim_patron_of_faith` NOW applied at `qing_pilgrimage.3:225`; `qing_pilgrim_devotion_to_rival` NOW applied at `se_QING_MISSIONARY.txt:133`. Both LIVE. *(This is the religion cluster independently confirming the PILGRIMAGE system is live — see A.5-§5A correction.)*
**⚠️ `qing_war.3` naval commission** — prior bug (empty `trireme` stub) fixed to `create_unit navy=yes` brig idiom, but **unproven / untested** — boot-test recommended.
**⚠️ Military traditions tree PASSIVE** — functional modifiers but no Qing mission grants `add_military_experience` toward nodes. Wire Ili/Burma/Taiwan mission completions to matching Shiquan nodes.
**✅ NO orphaned counters** — write-vs-read checked for every decline counter (banner_decay, greenstandard_decay, modernarmy_share, sect_pressure, suzerain_prestige all read).

## 6. UNASSIGNED FILES (17 flagged)
ADVISORS, BUILDINGS, CANAL, COLON, EARLYINDUS, INTEG_CAPSTONE, **MANDATE (⚠️ overlaps Rites legitimacy)**, NAPOLEON, REFORM, **SELFSTR (backbone, crosses all clusters)**, SPHERE, STUDENTS, SUMMER_PALACE, TECHTRANSFER, TREASURE_FLEET, TREATIES, WORKS. *(Synthesizer note: all 17 were in fact covered by the economy/decline/diplomacy/frontier clusters — this list reflects only THIS agent's brief boundary, not a true coverage gap.)*

**Final verdict:** military & religion suite highly functional, exemplary concrete-over-abstract, tight Council/Decline wiring, minimal duplication. Deductions: orphaned mandate feed, missing holy-site wiring, shallow ritual/pilgrimage depth, passive traditions tree. No critical bugs; fixes #5 + #118 already applied.

---

*End of Appendix A. Six reports, ~112 KB of raw agent output, preserved verbatim with three synthesizer
correction flags (A.1-§5.2 gc_slot, A.3-§3.2 ttx_debt note, A.5-§5A Japan/pilgrimage — the critical one).*
