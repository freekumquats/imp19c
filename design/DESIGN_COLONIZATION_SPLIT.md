# DESIGN_COLONIZATION_SPLIT.md — decomposing the 1470-line colonization mega-tree

**Branch:** `manufactured_goods`. **Status:** DESIGN (draft 2026-08-02, awaiting sign-off). Task tag `#27`.
Companion to `DESIGN_PROTECTORATES_GENERAL.md` (the march rework this split enables) and
`QING_FEATURES.md §13`. Commits authored by `freekumquats`.

> **Why:** `common/missions/qing_colonization_missions.txt` is **29 tasks / 1470 lines** bundling ~6
> distinct campaigns into one mission group. It also **duplicates** the dedicated Central-Asia and
> Xinjiang trees. The "each march is founded by the tree that conquers its theatre" ruling
> (DESIGN_PROTECTORATES_GENERAL §4.2) exposed this: several theatres already have proper homes, so the
> mega-tree is redundant in places. This doc plans the decomposition. **Build only after sign-off.**

---

## 1. CURRENT STATE — the 29 tasks + dependency graph

Shared mission-group gate (inherited by all tasks): `tag = CHI`, `is_ai = no`,
`OR { var:qing_selfstr_progress >= 40 ; has_variable = qing_high_qing_era }`. Loc =
`qing_colonization_l_english.yml`; modifiers = `qing_colonization_modifiers.txt`.

Dependency edges (`requires =`; root = `bureau`, the Maritime Bureau):

```
bureau ─┬─ taiwan ── pacific_isles ─┬─ new_holland ── new_guinea
        │                           ├─ anhai        (PROTECTORATE)
        │                           └─ lanfang
        ├─ amur ─┬─ alaska ─┬─ canada
        │        │          └─ california ── anxin   (PROTECTORATE)
        │        ├─ anbei   (PROTECTORATE)
        │        └─ andong  (PROTECTORATE)
        ├─ xinjiang ─┬─ central_asia
        │            └─ anxi    (PROTECTORATE)
        ├─ annan     (PROTECTORATE)
        ├─ daoguang_doctrine
        ├─ zheng_he ─┬─ cape ─┬─ congo
        │            │        └─ anfei  (PROTECTORATE)
        │            └─ suez
        └─ galleon ── veracruz ── maximilian ── mexican_empire
```

## 2. THE SPLIT (user ruling 2026-08-02 — "full split")

Four destinations. Each new tree gets its own mission-group wrapper (clone the shared gate + a fitting
`header`/`icon`), its own loc file, and its share of the modifiers.

### (A) SPLIT the maritime core into TWO trees — Oceania and the New World (user ruling 2026-08-02)
The kept "maritime core" is really two distinct campaigns; the dependency graph already separates them
(shared only at `bureau` + the basin-wide `daoguang_doctrine`). Split accordingly:

**(A1) OCEANIA — `qing_colonization_missions.txt` kept + renamed (大洋洲事業, the Pacific/South-Seas enterprise).**
Keeps: `bureau` (the Maritime Bureau root — the shared springboard), `taiwan`, `pacific_isles`,
`new_holland`, `new_guinea`, `lanfang`. MARCH capstone: **`anhai`** (Pacific march, off `pacific_isles`/
`new_holland`).

**(A2) NEW WORLD — new `qing_new_world_missions.txt` (新大陸事業, the trans-Pacific American enterprise).**
Moves: `amur`, `alaska`, `canada`, `california`, **`daoguang_doctrine`** (the entente with the American
republic — it is the North-American diplomacy task, so it belongs here, not in Oceania). MARCH capstone:
**`anxin`** (New-World, off `california`/`alaska`). NOTE: `andong` is NO LONGER founded here — it retargets
to fragmented JAPAN and is founded from `qing_open_japan_missions.txt` (DESIGN_PROTECTORATES §4.1/§4.2),
NOT from the Amur branch. `amur` stays as an ordinary New-World claim task with no march capstone. Its own
root task gates on the maritime springboard (mirror the `bureau` gate, or `requires` a shared
prerequisite — see §4 re-rooting).

> The two share only `bureau` (Maritime Bureau). `bureau` stays in the Oceania tree as the shared
> springboard; the New-World tree's root re-roots on the Oceania `bureau` prerequisite (or a cloned gate)
> so it still requires the maritime turn outward. NOTE `daoguang_doctrine` currently `requires = bureau`
> AND its provocation-guards are referenced by the New-World tasks (canada/california check
> `NOT has_country_modifier = qing_daoguang_doctrine`) — moving it INTO the New-World tree keeps that
> cross-reference intra-tree, which is cleaner. (`anfei` → Africa tree, `anxi`/`anbei` → Central Asia,
> `annan` → Burma — below.)

### (B) LIFT OUT — the Scramble for Africa → new `qing_africa_missions.txt`
Self-contained arc (`zheng_he` → `cape`/`suez` → `congo` → `anfei`), roots only at `bureau`. Move all 5
tasks to a new tree `qing_africa_mission` (非洲事業 / the Zheng-He-reborn arc). `anfei` (African march) is
its capstone. New loc file `qing_africa_l_english.yml`; its modifiers move from
`qing_colonization_modifiers.txt`. Re-root the arc's first task on the new tree's own root/gate instead
of `requires = bureau`.

### (C) LIFT OUT — the Mexican Adventure → new `qing_mexico_missions.txt`
Self-contained arc (`galleon` → `veracruz` → `maximilian` → `mexican_empire`), roots at `bureau`. Move
to `qing_mexico_mission` (墨西哥事業). NOTE the existing `DESIGN_MEXICO.md` + `se_MEXICO.txt` already own
the Mexican-empire RELEASE machinery — this tree is the mission-front for it; keep the se_ effects as-is,
only the mission tasks relocate. New loc `qing_mexico_l_english.yml`.

### (D) DELETE — the duplicate land-west tasks
`xinjiang` and `central_asia` in the colonization tree **duplicate** the dedicated
`qing_xinjiang_missions.txt` (#422, Dzungaria+Tarim) and `qing_central_asia_missions.txt` (#448, the Juz
+ khanates). Remove both colonization tasks. Their downstream dependents re-root:
- `alaska` currently `requires = amur` (fine — stays); nothing hangs off colonization-`xinjiang` except
  `central_asia` + `anxi`, both leaving. So deletion is clean once `anxi` relocates.
- The Anxi + Anbei marches are founded in `qing_central_asia_missions.txt` (per DESIGN_PROTECTORATES §4.2):
  Anxi as capstone of the khanate-conquest chain, Anbei off `qing_ca_kazakh`.
- **Salvage check:** anything `qing_col_xinjiang`/`_central_asia` did that the dedicated trees DON'T
  (e.g. the Urumqi fort+colony seed in `qing_col_xinjiang`, the Tashkent/Alma-Ata claims + Bukhara
  tributary in `qing_col_central_asia`) must be confirmed present in the dedicated trees or ported there
  before deletion — do NOT lose content. (`qing_central_asia` tree already has `qing_ca_khanates`,
  `_ferghana`, `_tuntian`, `_border` — likely covers it; verify at build.)

### (E) RELOCATE — Annan → the Burma war tree
`annan` (SE-Asia march) → capstone/branch of `qing_burma_war_missions.txt` (per DESIGN_PROTECTORATES §4.2).

## 3. RESULT

| Tree (file) | Contents | March founded |
|---|---|---|
| `qing_colonization_missions.txt` (kept = OCEANIA) | bureau/taiwan/pacific_isles/new_holland/new_guinea/lanfang | Anhai |
| `qing_new_world_missions.txt` (NEW) | amur/alaska/canada/california/daoguang | Anxin (Andong → Japan tree) |
| `qing_open_japan_missions.txt` (existing) | + Andong capstone | Andong |
| `qing_africa_missions.txt` (NEW) | zheng_he/cape/suez/congo | Anfei |
| `qing_mexico_missions.txt` (NEW) | galleon/veracruz/maximilian/mexican_empire | — |
| `qing_central_asia_missions.txt` (existing) | + Anxi, Anbei capstones | Anxi, Anbei |
| `qing_burma_war_missions.txt` (existing) | + Annan capstone | Annan |
| ~~col_xinjiang, col_central_asia~~ | DELETED (duplicate; salvage first) | — |

Colonization/Oceania tree drops from 29 → 6 tasks; three focused new trees (New-World 5, Africa 5,
Mexico 4); three marches founded in existing dedicated trees; no theatre covered twice.

## 4. MECHANICAL NOTES / RISKS
- **Mission-group wrapper per new tree:** clone the `qing_colonization_mission = { icon header repeatable
  chance ai_chance potential abort on_start on_completion <tasks> }` shell. `header` = a
  `mission_image_*` (may reuse an existing one or need a new one — see the icon note in the file header;
  cosmetic, not boot-critical).
- **Loc:** each relocated task keeps its keys; move the key blocks to the new tree's loc file so the old
  file doesn't carry dead keys (harmless if left, but tidy). Loc files keep BOM.
- **Modifiers:** `qing_col_*` country modifiers referenced by moved tasks must live somewhere the engine
  loads (all of `common/modifiers/` loads regardless of file) — so modifiers can stay in
  `qing_colonization_modifiers.txt` or split; no functional dependency on filename. Lowest-risk: leave
  modifiers where they are.
- **`requires =` re-rooting:** every moved arc's FIRST task must drop `requires = qing_col_bureau` and
  instead hang off its new tree's root task. Verify no task keeps a `requires` pointing into a tree it no
  longer shares (a cross-tree `requires` silently never unlocks).
- **Byte conventions:** mission files = no-BOM/LF; loc = BOM/LF; modifiers = no-BOM/LF (memory
  `imp19c-colonization-mission-arcs`).
- **No boot-crash surface** in a pure task-relocation (no new tags/provinces) EXCEPT the march-founding
  effect work (covered by DESIGN_PROTECTORATES_GENERAL). Split + protectorate rework interleave: do the
  split FIRST (pure relocation, low risk), THEN found the marches in their new homes.

## 5. BUILD ORDER (after sign-off)
1. Lift Africa arc → `qing_africa_missions.txt` (+ loc). Verify boots (arc self-contained). Review, commit.
2. Lift Mexico arc → `qing_mexico_missions.txt` (+ loc). Review, commit.
3. Lift New-World arc (amur/alaska/canada/california + daoguang_doctrine) → `qing_new_world_missions.txt`
   (+ loc); re-root on the Oceania `bureau` prerequisite. The Oceania tree keeps bureau/taiwan/pacific/
   new_holland/new_guinea/lanfang. Review, commit.
4. Salvage-check then DELETE col_xinjiang + col_central_asia (confirm dedicated trees cover their content).
   Review, commit.
5. (Then, per DESIGN_PROTECTORATES_GENERAL) found the 7 marches in their trees + rewrite the effect.
Each step is independently boot-safe and reviewable.
