# Overnight Design 4 — Qing Bureaucracy Build-Out

**Branch:** `merge-overnight`
**Start:** 2026-07-11 04:46 PDT
**Author of record:** freekumquats (all commits)
**Scope:** Build out a full Qing central-government simulation: every Grand Council
office gains a concrete bureaucracy (a Grand-Council-clone L4 GUI panel + backing
mechanics), plus the marriage-as-diplomatic-play rework and its Zongli-Yamen
success hook, plus two standing-army substrate features that several panels depend on.

This document is the plan. `overnight_decisions4.md` is the running log of major
decisions + deferrals, written as the build proceeds.

---

## 0. Operating rules (self-imposed, from the standing memory rules)

- **Proven code only.** "Proven" = upstream Imperatrix (sobisonator) / Invictus /
  Terra-Indomita / vanilla, verified by git blame THAT turn showing a non-freekumquats
  author, cited file:line inline. My own `se_QING_*`/`QING_*`/`SE_*` files never count
  as proof of an engine capability.
- **Oracle before building** any unproven engine verb (TI + Invictus reference repos
  at `/Users/alan.chiang/github.com/{SnowletTV/Invictus,dementive/Terra-Indomita}`).
- **se_LOG everywhere** (enter/exit/line/fail), STATIC message strings only — never a
  macro `$param$` or `#` inside a LOG string.
- **GUI text wraps** (multiline=yes + fixed width, never autoresize).
- **Adversarial review after each task** (a Workflow fan-out of skeptics), fix
  confirmed findings before moving on.
- **Brace-balance check** every edited file (must be 0).
- **Minimize deferrals.** Size/complexity is NOT a reason to defer. Defer only for a
  hard external blocker (an unproven engine capability both oracles lack, or a
  dependency on an unbuilt feature). Every deferral is logged at the top of
  `overnight_decisions4.md` with the concrete blocker.
- **No push** until the user is back to test (merge-overnight is the test candidate).
  Commit in logical batches.

---

## 1. The office → bureaucracy map (the spine of the build)

The Grand Council IS the set of filled great offices (se_QING_COUNCIL.txt). Each
appointive office now gets a bureaucracy panel. Office keys + governing skill from
`QING_council_score_office` (se_QING_COUNCIL.txt:202-211):

| Office key | 中文 | Gov. skill | Bureaucracy (task) |
|---|---|---|---|
| chancellor | 領班軍機大臣 | all 4 | Grand Council hub (built: qing_greatgame) |
| war | 兵部 | martial | Ministry of War (#349) + frontier friction (#346) |
| personnel | 吏部 | finesse | Board of Personnel — governor corps (#365) |
| revenue | 戶部 | finesse | Ministry of Revenue — salt + Canton (#355) |
| rites | 禮部 | zeal | Ministry of Rites — tribute + exams (#353) |
| justice | 刑部 | zeal | Board of Punishments — slaves + trials (#363) |
| works | 工部 | finesse | Ministry of Works — buildings (#351) |
| censor | 都察院 | finesse | Censorate — Inspectors-General (#362) |
| lifanyuan | 理藩院 | charisma | Lifan Yuan Directorate — Ambans (#350) |
| chamberlain | 內務府 | charisma | Imperial Household — Upper Study + Harem (#359/#337/#360) |
| zongli | 總理衙門 | charisma | Zongli Yamen — plays + diplomats (#354/#357) |
| grand_secretariat | 內閣 | finesse | Central Secretariat — fed by Hanlin (#361/#358) |
| guard_commandant | 領侍衛內大臣 | martial | Imperial Guard — Bayara unit (#364) |

Cross-cutting: Hanlin Academy (#358) feeds #361; Southern Study (#336) is an
inner-court cabinet fed by the exam system (#321).

---

## 2. The shared "Ministry panel" pattern (clone of the Grand Council GUI)

Every office panel reuses ONE structural template (proven by the existing
qing_greatgame.gui / QING_greatgame_panel.txt pair, and the GC panel):

1. **Header** — `vbox using MainWindowHeaderBox`, title + menu icon + close button
   (the #352 F9 idiom: body NESTED inside the header vbox, layoutpolicy expanding).
2. **Summary bar** — office-holder portrait in the "summit card" slot; a
   `qing_<office>_perf` statesmanship progressbar (0..100); a filled/total count.
3. **Ministry-health meter list** — the sub-metrics that fold into perf.
4. **Managed-subordinate datamodel list** — the concrete roster this office runs
   (garrisons, Ambans, buildings, governors, inspectors, diplomats, scholars,
   consorts…). MUST be a `dynamicgridbox`/`fixedgridbox` (NOT vbox — #352 F2).
5. **Directives action strip** — scripted-GUI buttons (QING_*_actions.txt).

**Performance → Grand Council fold.** Each `qing_<office>_perf` feeds
`qing_council_eff_target` via the SAME fold the officer-corps coupling uses
(se_QING_COUNCIL.txt ~404-408), so a well/poorly-run ministry moves its Minister's
council standing. This is the unifying mechanic: the panels are not cosmetic — they
each drive one office's effectiveness.

Opening idiom: a button spliced into an existing view (government/diplomatic/religion),
`gui.createwidget` + window-name; close via `GUI.ClearWidgets` (imp19c-gui-panel-open-idiom).

---

## 3. Build order (dependency-driven)

**Wave 0 — standing-army substrate (moved to top by user):**
- **#347** generic standing-army province effects (unrest reduction, governor
  friction, food confirm). New shared files: army_effects_on_actions.txt,
  army_effects_modifiers.txt, army_governor_friction.txt, army_effects_l_english.yml.
  Detection idiom: `any_character_unit + is_moving=no + unit_location + unit_size`
  (Invictus internal_politics_republic.txt:563-633). Pulse hooks: monthly_province
  (empty now) + monthly_country.
- **#346** Qing frontier-garrison overlay: shift subject-soil frontier garrisons to
  direct CHI command + War-Ministry reporting + Lifan Yuan/Amban turf-war friction.
  Layers on #347's detection idiom (shared code, not duplicated).

**Wave 1 — diplomatic-play + marriage foundation:**
- **#357** Zongli Yamen global play-success factor. The Directorate (zongli office
  holder + charisma + new subordinate diplomats) seeds/modifies EVERY Qing play's
  success via `DIPLOMACY_seed_feature_play_success` / `DIPLOMACY_modify_play_success`.
- **#356** Marriage-proposal diplomatic play. DELETE Dynastic Match window/builder.
  New `play_goal = flag:marriage_proposal` branch in
  `DIPLOMACY_trigger_diplomatic_play_finale_event`; a two-step character picker
  (our unmarried char → their opposite-gender unmarried char, ruling family on top,
  minors allowed for betrothal). On success: MARRY if both adult, BETROTH if either
  minor (reuse MARRIAGE_form_pact payload / MARRIAGE_betroth). Success seeded by the
  existing compatibility triggers; player incentives (dowry/gifts, +success) and
  adverse events (rival suitor/scandal, -success) via DIPLOMACY_modify_play_success.

**Wave 2 — the office bureaucracies** (each = panel + backing mechanic + perf fold):
#349, #350, #351, #353, #354, #355, #361, #362, #363, #364, #365, #359.

**Wave 3 — inner-court + sub-mechanics:** #337, #360, #336, #358.

**Deferred follow-ons folded in where touched:** #334 (tributary), #335 (canal).

---

## 4. Per-feature design (filled in as each is built; see decisions log for choices)

### #347 Standing-army province effects (generic)
- A stationed army (is_moving=no) reduces province unrest (a pacification modifier),
  scaled to unit_size. Refreshed on a pulse; removed when the army leaves.
- Billeting/foraging friction with the province governor: a low-discipline or large
  garrison sitting on a governor's land breeds a friction event (governor loyalty /
  unrest tick), competence-gated.
- Food: confirmed engine-driven (unit food_consumption vs province capacity →
  attrition); documented, no new scripting.

### #346 Qing frontier garrison overlay
- Subject-soil frontier garrisons (Ili/Xinjiang/Mukden/Heilongjiang) → CHI-owned,
  CHI-commanded. Report to 兵部尚書 (office war); factor into qing_office.32 lifecycle.
- Presence on subject soil: tightens integration + drops subject loyalty (se_SUBJECT_QING).
- Turf war with 理藩院 (Ambans + Grand Director): a friction beat surfaced in BOTH
  the War panel (#349) and the Lifan Yuan panel (#350).

### #357 / #356 / Wave 2 / Wave 3
See per-task sections appended as built, and `overnight_decisions4.md`.

---

## 5. New units, characters, IDs

- **Bayara (巴牙喇)** — new elite infantry unit in common/units/bayara.txt (#364),
  modeled on regular_infantry.txt; strong combat weights, high upkeep, small.
- **Zongli Yamen diplomats + Censorate inspectors + Hanlin scholars + consorts** —
  new setup characters where a starting roster is wanted. Char-ID rule: recompute the
  global max across ALL setup/characters/*.txt every time, use contiguous max+1 (no gaps).

---

## 6. Risks / watch-items

- `play_goal = flag:marriage_proposal` is a NEW goal the finale switch must handle;
  the two chosen characters must survive from play-launch to resolution (store as
  play-provobj vars, re-validate is_alive at resolution).
- Multi-consort/harem modelling: engine marriage is monogamous; the harem is modelled
  with the existing spouse + concubine idiom if proven, else as ranked consort
  characters with a favour var (concrete-over-abstract). Oracle-gate before building.
- Every new panel's datamodel list must iterate via dynamicgridbox (the #352 F2 trap).
- Perf-fold into qing_council_eff_target must not double-count or destabilise the
  existing band applier — behavioural-equivalence scrutiny per the fix-traceability rule.
