# Overnight autonomous run — 2026-07-15

User directive (2026-07-15, user away, work without stopping):
1. Drop #7 from pending tasks. **[DONE]**
2. Finish #4 (reformat ALL ministry panel read-outs into neat tables) → review → commit → push.
3. Switch to `merge-overnight`, pull all `1763_bookmark` branch changes into it.
4. Implement #28 (convert Grand Council offices + Amban into engine positions), oracle-gated.
5. Implement ALL mission trees in `pending_mission_trees.md` (#447/#448/#449/#451 + dropped ideas as feasible).
6. Document every decision here; review + commit + push throughout.

Standing rules in force: commits authored by freekumquats; independent code-review agent before every commit;
preserve each file's existing per-file BOM state (.gui = no-BOM upstream, but PRESERVE actual state); BOM is
NOT a crash cause; scripted_gui compile-recursion crash class (route sorting iterators / create_character /
imprison through hidden trigger_event trampolines); user boot-tests on a SEPARATE machine so MUST push;
oracle-gate any unproven engine capability (consult TI + Invictus).

---

## Task #4 — Reformat ALL ministry panel read-outs into neat tables

**Problem (playtest):** ministry L4 panels' label:value read-out rows don't align — the first ("performance")
row uses a 180px label, later rows use 240px or 300px, and value cells vary 40/60/80/120px, so numbers never
form a column.

**Design decision (user-approved via AskUserQuestion 2026-07-15):**
- Uniform label column = **300px**, value cell = **60px**, both `size = { W 20 }`, row `spacing = 8`.
- Performance row: keep label:value on the aligned row, **move the progress bar to its own full-width line
  below** (option "Bar on its own line"). Bar `size = { 300 12 }`.
- Rows with a conditional two-textbox value (reformed/unreformed, raised/unraised, danger/checked) keep BOTH
  value textboxes but normalize them to the value-column width so whichever is visible lands in the column.
- Roster/dynamicgridbox rows and section-title textboxes (`size = { 460 28 }`) are NOT touched — only the
  label:value read-out `flowcontainer` rows inside the standing/summary sections.

**Panels touched (24, extended beyond the initial 14 for visual consistency — "ALL"):** revenue_ministry,
household, zongli, secretariat, censorate, rites_ministry, war_ministry, works_ministry, lifanyuan, hanlin,
guard, personnel, harem, justice, southern_study, upper_study, caravan, greatgame, opium, population, princes,
province_reports, religion, xinjiang.

**Method:** wrote a brace-aware Python transformer (deleted after use) that recognized a read-out row as a
`flowcontainer` whose direct children are all `textbox`/`progressbar` AND whose first textbox `text` ends in
`_LABEL`; regenerated each in canonical form. Everything else (section titles size {460 28}, character-card
flowcontainers, dynamicgridbox rosters) untouched. All 24 files: braces balanced, no-BOM preserved.

**Code review (code-review agent) — 1 real regression + 4 cosmetic, ALL FIXED:**
- REGRESSION: `qing_province_reports.gui` Canton revenue-split row had a *container-level* `visible` guard
  (#426: shown only while the hoppo-rotation system is open). The transformer dropped container-level
  attributes (it only migrated child-textbox `visible`s). Restored the guard on the flowcontainer.
- CLIPPING (value cells narrowed to 60px but hold descriptive strings, not numbers): widened back —
  harem rank line (皇貴妃…/貴妃…/妃…) → 210; revenue salt reformed/unreformed → 200 each; household eunuch
  danger/checked → 200 each; works hydraulic VALUE → 180. Numeric value cells stay at 60 (they align).
- The two ratio rows (lifanyuan amban/warrant, personnel gov_clean/gov_count) manually kept at 120.

**Progress:** DONE — committed a1d9b5675, pushed to origin/1763_bookmark.

---

## Step 3 — switch to merge-overnight, pull 1763_bookmark

merge-overnight was 41 commits behind 1763_bookmark and 0 ahead → clean **fast-forward** merge (no
conflicts). Now merge-overnight == 1763_bookmark (a1d9b5675). Pushed to origin/merge-overnight.
**All remaining work (#28 + mission trees) proceeds on merge-overnight.**

---

## Task #28 — Convert Grand Council offices + Amban into engine positions

**Directive:** convert the Grand Council offices AND the Amban into engine positions (like governor /
researcher — https://imperator.paradoxwikis.com/Position), removing the now-redundant office-exclusion logic.
Oracle-gated: engine `Position` (office_type / job) is an UNPROVEN capability in this mod, so per the
standing oracle rule I must verify against upstream TI + Invictus before building.

**Progress:** BLOCKED — infeasible as specified. Full analysis below. Deferred; night's effort redirected
to the mission trees (concrete, proven-idiom content).

### Oracle finding (Explore agent + my own verification)

The engine's real "custom office" surface is `common/offices/` (vanilla Imperator office defs carried in the
mod). Two hard blockers make a 1:1 "offices → engine positions" conversion impossible:

1. **Fixed slot count.** Monarchy exposes exactly **8** office slots (verified: `office_foreign_minister,
   office_royal_tutor, office_marshal, office_master_of_the_guard, office_high_priest_monarchy,
   office_philosopher, office_steward, office_physician` in `common/offices/00_monarchy.txt`). You define
   what each of the fixed slots does, but you cannot declare a 9th+ arbitrary office. The Grand Council needs
   **13 appointable seats** (chancellor/personnel/revenue/rites/war/justice/works/censor/lifanyuan/chamberlain/
   zongli/grand_secretariat/guard_commandant) **plus 5 special seats** (emperor/empress/crown-prince/regent/
   emeritus) **plus the Amban** — far more than 8.

2. **No scriptable appoint effect.** Grep across `common/` + `events/` for `set_office / appoint_office /
   set_office_holder / assign_office / set_as_researcher / set_as_governor / add_office` returns **nothing**.
   The engine offers only READ (`has_office`, `has_any_office`, `is_governor`, `has_tech_office`) and STRIP
   (`remove_all_offices`, `remove_as_researcher`, `remove_as_governor`). Native office appointment is
   player/AI-driven through the vanilla government UI — it cannot be scripted. The mod's variable-based system
   (`se_QING_COUNCIL.txt` `QING_office_appoint`/`_vacate`/`_vacate_dispatch`) exists **precisely because** the
   engine provides no scripted seat effect (see the design header at se_QING_COUNCIL.txt:1-52 and
   qing_dynasty_triggers.txt:144 "invisible to the engine's native office system").

Governors bind to regions/subjects, researchers to tech slots — neither maps to a named council office. No
vendored TI/Invictus offices framework exists in the repo to borrow from.

### Decision (user away, cannot ask; documented per directive)

Do NOT attempt the conversion. A partial mapping onto the 8 vanilla monarchy slots would cover <half the
seats, could not stay synced with the variable system (no scripted appoint), and risks breaking vanilla AI
government behaviour — a high-regression change I cannot boot-verify on this machine. Per the standing
oracle-consultation rule ("do NOT build on an unproven/absent engine capability"), #28 is **deferred as
engine-blocked**. The variable-based office system stays; the office-exclusion logic stays (it is load-bearing,
not redundant — it is the ONLY thing making the seats mutually exclusive, since the engine can't).

If the user still wants the *feel* of engine positions later, the achievable scope is cosmetic only:
surface council seats in the government view via customizable_localization title-renames on the 8 real slots,
without wiring appointment. That is a separate, smaller task to scope with the user — not attempted tonight.

---

## Mission trees (pending_mission_trees.md: #447/#448/#449/#451)

Shared method: cloned the proven Qing conquest/enterprise idiom (qing_burma_war + qing_treasure_fleet trees).
PLAYER does the work — task goals gate on real province CONTROL (`p:ID = { controller = ROOT }` /
`any_owned_province = { count >= N  is_in_region = X }`) or on a subject tie (`c:TAG = { is_subject_of =
ROOT }`); scripted effects only add texture (self-expiring province modifiers, claims, make-subject-by-fiat
via FUNC_make_subject). Each tree: CHI-only + player-only (`potential = { tag=CHI  is_ai=no }`,
`ai_chance = { factor = 0 }`), `abort = { NOT = { tag = CHI } }`, tasks chained by `requires`, costs in
`on_start`, gates wrapped in `custom_tooltip`, capstone grants a permanent (`duration = -1`) dominion modifier.
All new files no-BOM (matches every sibling qing mission/effect/modifier/loc file). Loc format `key:0 "..."`
(single-space indent); the editor's YAML diagnostics on loc files are FALSE POSITIVES (Paradox loc isn't
standard YAML; sibling files trip the same linter).

Verified on-map keys before building (Explore agent + spot-checks): TKG=Tokugawa (Edo p:3684), AIN=Ainu
(Ezo), MAE=Matsumae; EIC=East India Company (Calcutta p:6219, subject of GBR), BNG=Nawab of Bengal (sovereign,
at war w/ Company 1763), MUG=Mughals; regions Kyushu/Honshu/Ezo, Bengal_region/Bahar, Turkestan/Bukhara/
Fergana/Khwarezm, Mongolia/Liaoning/Far_East all exist in map_data/regions.txt; CHI subjects in Mongolia/
Manchuria = ULS(Uliastai)/MGA(Urga)/KBD(Kobdo)/MNC(Manchuria)/MKD(Mukden)/HLJ(Heilongjiang)/TNN(Tannu).
sinosphere_tributary is a real subject type; FUNC_make_subject{overlord,target,type} is the proven idiom.

### #447 — Open the Closed Country (叩關破鎖國) — DONE
Anachronistic naval opening of Sakoku Japan ~a century before Perry. **Gated on the Treasure Fleet (#439)**
via `potential = { ... has_country_modifier = qing_treasure_fleet_glory }` (the permanent modifier its 下西洋
capstone grants) + `exists = c:TKG`. Forks: ARC S (南路: hold Kyushu → grant Edo claim → take Edo p:3684) and
ARC N (北路: embrace the Ainu as tributary via FUNC_make_subject → hold Ezo). Capstone requires BOTH Edo held
AND Ezo held → permanent qing_japan_opened modifier + lifts the coastal-pressure texture. 4 files:
qing_open_japan_missions.txt, se_QING_OPEN_JAPAN.txt, qing_open_japan_modifiers.txt, loc. Braces balanced.

### #448 — The Western Regions (經略西域) — DONE
Carries the Qing PAST the Xinjiang consolidation (#422) into Central Asia proper: the Kazakh steppe (three
Juz — GKH/ORT/KSH) and the Silk Road khanates (Kokand KOK, Bukhara BUK, Khiva KHV). `potential` requires
CHI + at least one of those six tags to exist. Tasks: qing_ca_beyond_pass (root, pay treasury+PI), two
parallel embrace branches — qing_ca_kazakh (gate `OR = { exists c:GKH/ORT/KSH }`, embrace via
QING_ca_embrace_kazakh) and qing_ca_khanates (gate `OR = { exists c:KOK/BUK/KHV }`, embrace via
QING_ca_embrace_khanates) — then qing_ca_ferghana (hold ground: `any_owned_province count>=1 is_in_region =
Fergana`). Capstone requires kazakh+ferghana, gate = `any_subject count>=2` among the six tags AND Fergana
ground → permanent qing_western_regions modifier. The two embrace effects use the proven himalaya_seasia
FUNC_make_subject idiom (guarded per tag on exists + not-already-subject). 4 files:
qing_central_asia_missions.txt (55/55), se_QING_CENTRAL_ASIA.txt (38/38), qing_central_asia_modifiers.txt
(1/1), loc (0 bad lines). All no-BOM.

**Design note (embrace vs. control gate):** first draft gated qing_ca_kazakh/khanates on `any_subject`
(already-a-subject) — UNREACHABLE, since the player has no control-goal that force-makes a subject. Fixed to
gate on `exists = c:TAG` + pay cost, embracing via the scripted effect on completion (matches the proven
qing_hs_nepal idiom). Region key is `Fergana` (verified in map_data/regions.txt).

### #449 — Contest the Company (逐夷復印) — DONE
Qing bid to contest the British East India Company (EIC) for the paramountcy of Hindustan. 1763 board
(verified in 00_default.txt): EIC = megacorp seated at Calcutta (p:6219, Bengal_region), a GBR client_colony
holding a web of Indian client_states incl. MUG (Mughal emperor, Delhi p:8805); BNG = Nawab of Bengal,
SOVEREIGN + at war with the Company in 1763 (natural anti-Company ally). `potential` requires CHI + `exists =
c:EIC`. ROOT qing_india_descent (pay treasury+PI, stamp company-pressure on EIC Bengal/Bihar ports) →
ARC W: qing_india_nawab (embrace BNG tributary + claim Calcutta) → qing_india_calcutta (control p:6219);
ARC E: qing_india_mughal (free MUG from Company → tributary) → qing_india_heartland (hold 2 provinces in
East_India, or freed Mughal holds ground there). Capstone requires calcutta+heartland, gate = Calcutta held +
BNG AND MUG both is_subject_of ROOT → permanent qing_india_paramountcy modifier + lifts pressure. Embrace
effects use the guarded FUNC_make_subject idiom (MUG guard is only NOT-subject-of-ROOT, so a Company vassal
still qualifies — that's the liberation). 4 files: qing_india_missions.txt (68/68), se_QING_INDIA.txt (48/48),
qing_india_modifiers.txt (2/2), loc (0 bad). All no-BOM. Verified keys: blockade_efficiency, global_tax_modifier.

### #451 — Settle the Nomads (定牧墾邊) — DONE
Consolidation of the Mongol steppe + Manchurian homeland from autonomous banner-governorships into settled,
directly-held imperial ground. UNLIKE the other three trees this integrates EXISTING CHI subjects, not
foreign conquest: 1763 board has ULS/KBD/MGA (Mongol governorships, MGA nested under ULS) + MNC/MKD/HLJ
(Manchurian governorships) + TNN (Tannu tributary), all already CHI subjects. `potential` = CHI only (no
foreign-tag gate needed). ROOT qing_settle_policy (pay, embrace-Tannu safety net) → ARC N qing_settle_mongolia
(own ≥8 in Mongolia, stamp reclamation) + ARC E qing_settle_manchuria (own ≥8 in Liaoning/Far_East, stamp
reclamation) → capstone (own ≥12 Mongolia AND ≥12 Liaoning/Far_East → permanent qing_frontier_settled). Goals
gate on OWNERSHIP (reached by integrating the governorships that hold the ground), not is_subject_of. Region
sizes verified via areas.txt: Mongolia ~178, Liaoning ~36, Far_East ~221, so 8/12 thresholds are reachable
fractions. Reclamation modifier self-expires (10yr). 4 files: qing_settle_frontier_missions.txt (46/46),
se_QING_SETTLE_FRONTIER.txt (26/26), qing_settle_frontier_modifiers.txt (2/2), loc (0 bad). All no-BOM.
Verified keys: every_owned_province, local_tax_modifier, local_population_growth, land_morale_modifier.

---

## Step 6 — code review + commit + push

All four mission trees (#447/#448/#449/#451) built. Independent code-review agent ran over all 16 files.

**Review verdict: NO critical or medium issues.** All 8 checklist items PASS — tooltip↔loc parity, effect
call↔def parity, modifier ref↔def, acyclic reachable task DAGs, proven scope idioms (incl. `controller = {
... }` and `any_subject` both confirmed proven elsewhere), LOG macro signatures + no #/$param$ in msg strings,
region keys all exist, ownership-count gates all well under region sizes.

**Two LOW design caveats flagged (capstone soft-lock if the player ANNEXES a tributary instead of holding it):**
- #449 India capstone (required c:BNG + c:MUG both is_subject_of ROOT): **FIXED** — conquering Indian states
  outright is a natural playstyle, so relaxed each throne gate to `OR = { NOT = { exists = c:TAG }  c:TAG = {
  is_subject_of = ROOT } }` (held as tributary OR absorbed out of existence). Tooltip reworded to match
  ("held as a tributary or absorbed into the empire outright"). Mission file rebalanced 72/72 braces, loc 0 bad.
- #448 Central Asia capstone (`any_subject count>=2`): **left as-is** — reviewer explicitly cleared it ("Fine
  as-is"); steppe hordes are unlikely to be fully annexed, and over-relaxing any_subject would be less clean.

Ready to commit.

---

## Task #34 — The keju as the source of all civil characters

**User directive:** "enhance and connect the keju system to become the source of character creation.
all civil officials (non-commanders) in all ministries must come from the keju. there should be several
new character traits representing the degrees granted by the keju. ambans for example should not be spawned
from nowhere but come out of the keju. the same system should also provide diplomats and governors and
researchers and so forth" + "all children should be sent to the keju when they get old enough".

**Approved design (AskUserQuestion, 3 answers):**
- **Coverage = "Population-source."** The verified engine limit: governors / researchers / engine-diplomats and
  the 8 fixed monarchy office slots are NOT script-appointable (no set_as_governor / set_as_researcher /
  create_diplomat / appoint_office anywhere — this is why #28 is engine-blocked). So the keju cannot appoint
  each SEAT; instead it gates the whole civil-character POPULATION. Every court character sits the exam on
  coming of age → carries a degree for life → the candidate benches the council / ambanate / legations already
  pick from are graduates by construction.
- **Eligibility = "Soft preference."** Degree-holders score far higher and are picked first, but a degreeless
  character can still be seated when no graduate is free — no soft-lock for want of a laureate.
- **Ambans = "Banner-exam track."** A Manchu/Mongol translation examination (翻譯科 → fanyi_jinshi) feeds the
  amban / resident posts; the civil track (文科) feeds the metropolitan offices.

**As built (7 files):**
1. **Degree traits** (`common/traits/00_imp19c.txt`): expanded the ladder to seven mutually-exclusive `status`
   degrees — 監生 jiansheng (new, purchased/academy floor) < 生員 shengyuan < 舉人 juren < 貢士 gongshi < 進士
   jinshi < 翰林 hanlin (new, Academy apex); plus 繙譯進士 fanyi_jinshi (new, banner track). **Bugfix:** the old
   opposites lists named `jiansheng` (never declared) and `gongsheng` (a typo for the declared `gongshi`) —
   `jiansheng` is now defined and every list rebuilt to reference all six others, so the ladder is genuinely
   exclusive. Holding-income scales with rank (0.01→0.125).
2. **Soft preference** (`common/script_values/QING_governance_svalues.txt`): new `qing_degree_prestige_svalue`
   (character scope, conditional add-by-trait, the proven religionator_svalue idiom) adds 5→30 by degree; folded
   into `combined_stats_council_svalue` AND all four `council_sort_<skill>` pickers, so a graduate outscores an
   equally-skilled commoner wherever the council / office / amban picker sorts. Deliberately large vs the 0..~9
   skill axis so a degree is the dominant sort key.
3. **Coming-of-age intake** (`se_QING_EXAM.txt` `QING_exam_sit_candidate` + on_becoming_adult hook in
   `00_specific_from_code.txt`): every Qing court character sits the keju on maturity. Bannermen (jurchen /
   mongolic culture groups) sit the translation track → fanyi_jinshi/shengyuan; Han + general court sit the
   civil track → degree tier by the realm's pass-rate band (mirrors QING_exam_graduate_cohort). Pass chance =
   `qing_keju_pass_chance_svalue` (finesse+charisma + a pass-rate floor band, bounded 5..90). A failer takes no
   merit degree (joins the fallback commoner pool), save a 15% 捐監-purchase of the 監生 floor. Marks
   qing_sat_keju so a man sits once. Self-guards on employer=CHI so it is a global no-op elsewhere.
   NOTE (scope): runs at CHARACTER root, so it does NOT call QING_char_init_identity / QING_char_bind (both read
   root.current_ruler = a COUNTRY link, invalid at char root) — conferring the degree is the whole job; identity
   + affinity are set by the office/council machinery when the graduate is drawn.
4. **Ambans from the keju** (`se_QING_AMBAN.txt` `QING_amban_post`): now DRAWS the ablest free banner-track
   graduate the court holds (fanyi_jinshi, or any degreed bannerman) and posts him, dropping him from the
   scholar pool if he was in it; conjures a fresh resident (now stamped fanyi_jinshi so he too is a keju man)
   ONLY when no banner graduate is free (the soft-preference fallback). Game-start historical residents
   (QING_amban_seed_one) also get fanyi_jinshi.
5. **Historical roster degrees** (`qing_roster_events.txt`): the real civil officials get their real degrees —
   Lin Zexu/Kang Youwei = jinshi; Li Hongzhang/Zeng Guofan/Zhang Zhidong/Guo Songtao = hanlin (all Hanlin
   compilers); Zuo Zongtang/Zeng Jize = juren; Sheng Xuanhuai = jiansheng (purchased rank). Correctly LEFT
   degreeless: Prince Gong (imperial prince), Yung Wing/Sun Yat-sen (Western-educated), Yuan Shikai (failed the
   exams for a military career), Heshen (banner favourite).
6. **Loc** (`imp19traits_l_english.yml`): full trait loc for all seven degrees — the pre-existing degree traits
   had NO loc entries at all (would have rendered as raw keys), so this fixes a latent display bug too.

**Self-caught bug during build:** first draft used `random = { chance=… } else = { … }` for the civil
pass/fail split — but `else` is a sibling of `if`/`else_if` ONLY, never of `random` (a silent parse break).
Rewrote to roll the pass into a one-shot `qing_keju_passed` marker, then branch with a proper if/else.

**Idioms verified before building:** conditional add-by-trait in a script_value (religionator_svalue); nested
script_value in `add =` (combined_stats_olympics precedent); `else_if`/`min`/`max`/`divide` in script values;
guarded `employer = { var:X >= N }` band read (bare `add = employer.var:X` NOT attested); culture_group keys
(manchu∈jurchen, mongolian∈mongolic, han∈chinese_group); `any_character { employer = ROOT }` + `ordered_character
order_by = combined_stats_council_svalue` (the exact council-picker idiom); on_becoming_adult = character scope.

All 6 .txt files brace-balanced; every file's per-file BOM state preserved (traits/on_action/roster = BOM,
exam/amban/svalues = no-BOM; loc = BOM). Loc YAML diagnostics are the documented false positives.

**Code review (independent agent) — 3 findings, all resolved:**
- MEDIUM (real bug, FIXED): the shared `QING_amban_wire` tail ran `set_as_minor_character = THIS`, correct
  only for a freshly-CREATED resident — but the #34 draw-path feeds it a real full court bannerman, so the
  ablest drawn graduate was PERMANENTLY demoted to minor standing (recall never restores it). Moved the
  demotion to the two CREATE sites only (fallback `else` + `QING_amban_seed_one`); a drawn court graduate now
  keeps major standing and rejoins the office pool on recall.
- MEDIUM (design, KEPT + documented): degree prestige (+5..30) folded into the single-skill `council_sort_*`
  keys. Assessed working-as-intended and historically correct — the Six Boards (incl. 兵部) were headed by
  civil-exam graduates, not field generals, and generals/admirals are already excluded from office eligibility
  (`QING_office_eligible_candidate`), so a "brilliant degreeless general loses the War seat" scenario cannot
  arise: he is not a candidate. Degree tiers are 5 apart vs a ~0–15 skill span, so skill still separates men
  within and across a tier — a genuine soft preference, not a collapse.
- LOW (pre-existing, FIXED opportunistically): `QING_exam_mint_scholar`'s LOG line interpolated a macro
  `$degree$` into the message string (violates the standing no-`$param$`-in-LOG rule). Replaced with a static
  "minted a degreed graduate" line.

All 6 .txt files re-verified brace-balanced after the fixes (amban 210/210, exam 184/184); no stale `gongsheng`
in live code (only the two bugfix-note comments). Committed. Ready for boot test on the user's machine.
