# BOOKMARK_PROCESS.md — Re-targeting the game-start year

**Purpose.** A reusable, mechanical checklist for moving the Imperatrix: Victoria game
start to an arbitrary historical year. Written for the `early_bookmark` peak-Qing task
(#194–#197) but deliberately generic: the user will re-run it for other years, so every
step names *which files* define the game start and *why* they must change.

> **Golden rule:** the game start is defined in MANY files, not just `setup/main/00_default.txt`.
> Changing only the setup file leaves dated events, treasury seeds, OOB spawns, and the
> `START_DATE` define pointing at the old year — the game will boot into an inconsistent
> world (events that already fired, armies raised for the wrong decade, a treasury sized
> for the wrong economy). Walk the whole list every time.

---

## 0. Branch & logging discipline (STANDING RULES — never skip)

- Work on a dedicated branch (e.g. `early_bookmark`); never contaminate `develop`.
- All commits authored **and** committed by `freekumquats` (repo-local git identity is
  already set — verify with `git config user.name`). NEVER the alan-chiang/Salesforce id.
- Every change gets: a task-tagged in-code comment (`# [bookmark-YYYY task #NNN] …`), an
  `se_LOG` marker where a scripted effect is touched, and a `SESSION_REPORT.md` entry.
- Log every *big decision* (chosen year, which borders move, which characters are cut/added,
  treasury figure, laws changed) to the task's decision doc (this run: `early_bookmark_decisions.md`).
- Post-implementation deep adversarial-review workflow is MANDATORY before the final commit.

---

## 1. THE ANCHOR — `START_DATE`

**File:** `common/defines/00_defines.txt:3` → `START_DATE = "1815.7.1"`

This is the single source of truth for the calendar. Change it first; everything dated
downstream is relative to it. `END_DATE` (line 4) usually stays.

---

## 2. DATED EVENTS / ON-ACTIONS / SCRIPTED EFFECTS (the silent breakers)

Any hardcoded early-19c date must be re-based to the new start year, or the content will
either fire in the past (already-happened, so it never triggers or fires instantly at boot)
or in the far future. Find them ALL with:

```
grep -rnoE "18[0-3][0-9]\.[0-9]{1,2}(\.[0-9]{1,2})?" common/ events/ setup/
```

Known date-bearing files (verified 2026-07-08 for the 1815 baseline — re-grep each run,
the list drifts as features are added):

| File | Date(s) | Meaning / action on year-swap |
|---|---|---|
| `common/defines/00_defines.txt` | `1815.7.1` START_DATE | **the anchor (§1)** |
| `common/on_action/00_specific_from_code.txt` | `1815.7.1/.2/.3` | mobilization guard (`current_date > 1815.7.2`) — re-base to `START+1day` |
| `common/on_action/japan_bakumatsu_on_actions.txt` | `1815.7.1` | Japan arc start gate |
| `common/on_action/mex_instability_on_actions.txt` | `1815.7.1` | Mexico arc start gate |
| `common/on_action/usa_section_on_actions.txt` | `1815.7.1` | US arc start gate |
| `common/on_action/qing_mechanics_on_actions.txt` | `1815.7.1`, `1821.5.5` | Qing mechanics boot + a dated event |
| `common/on_action/economy/oa_economy_setup.txt` | `1815` (comments + treasury seed) | **§4 treasury** + `SE_qing_*` seeds (§5) |
| `common/scripted_effects/se_QING_NAPOLEON.txt` | `1821.5.5` | alt-history chain date |
| `common/scripted_effects/se_MEXICO.txt` | `1830.1.1` | Mexico arc dated beat |
| `common/scripted_effects/se_QING_DIPLO.txt` | `1826.1.1` | diplo dated beat |
| `events/imp19c_mod_events/ChineseEvents.txt` | `1815.10.15` | dated Chinese event |
| `events/imp19c_mod_events/qing_napoleon_events.txt` | `1821.5.5` | Napoleon chain |
| `events/imp19c_mod_events/qing_rebellion_events.txt` | early-19c | rebellion timeline |
| `events/imp19c_mod_events/qing_roster_events.txt` | early-19c | anachronistic-spawn roster |

**Decision each time:** for arc/event dates that are *relative offsets from the start*
(e.g. "10 years into the game"), convert to `START + offset`. For dates tied to a *real
historical event* (First Opium War, Boshin War), decide per-year whether that event is
still in the future (keep its real date) or now in the past (cut the arc or re-scope it).
Log the call in the decisions doc.

> **CRITICAL — `on_game_initialized` day-offset arcs.** The US/Japan/Mexico/Qing arcs
> (`*_on_actions.txt`) fire beats via `trigger_event = { id=… days = { A B } }`, where the
> offset A is baked so the beat lands on its **real historical date measured from the OLD
> START_DATE**. If you move the start, these offsets DO NOT auto-shift — a beat calibrated to
> "day 13835 from 1815" fires 13835 days after the *new* start, i.e. ~25 yrs too early if you
> moved back to 1790. **For every real-event beat, add the start delta:
> `new_offset = old_offset + (OLD_START − NEW_START in days)`.** Drop beats whose real date now
> precedes the new start. Grep `days = {` in each `*_on_actions.txt`.

> **CRITICAL — `START_DATE` is GLOBAL.** Moving it also invalidates every *other* country's
> ruler and border for that year. Check with a script: how many `set_as_ruler=char:N`
> characters have `birth_date` after the new start (unborn/infant → no valid ruler at boot).
> Decide scope up front: a **Qing-focused** bookmark leaves the rest of the world at its old
> config (documented anachronism, patch only load-breaking rulers); a **full-world** re-target
> is a much larger effort (every country's ruler + borders for the year). Record which.

---

## 3. BORDERS — `own_control_core`

**File:** `setup/main/00_default.txt`. Each country block has
`own_control_core = { <space-separated province-id list> }`.

- CHI block ≈ line 35640; its `own_control_core` ≈ 35705 (large multi-line list).
- FRA block ≈ line 34418; its list ≈ 34465.
- To move a province at game start: **cut the id from the losing country's list and paste
  it into the gaining country's list.** Province ids are stable; there is no owner data in
  `setup/provinces/` (those files hold only pops/terrain).

**Method for a territorial-extent change:**
1. From research, list the regions that differ from the 1815 baseline (gained or lost).
2. Map each region to its province ids (grep `setup/provinces/` region files, or the
   in-repo province name → id references; cross-check on the map).
3. Move ids between the relevant countries' `own_control_core` blocks.
4. **Neighbours matter:** a province added to CHI must be *removed* from whoever held it
   in the baseline, or the engine will hand it to the first-listed owner and the other
   country keeps a dangling core. Always edit both sides.
5. For a *runtime* transfer instead (rare at game start) use `LAND_transfer_province` /
   `LAND_transfer_provinces` (`se_LAND.txt`) — NOT raw `set_conquered_by` — because the
   mod's economy sim needs the governorship/wealth/education bookkeeping migrated too.

Verify total id count before/after and check no id appears in two countries' lists.

---

## 4. TREASURY / ECONOMY SEED

**File:** `common/on_action/economy/oa_economy_setup.txt` → `QING_seed_starting_treasury`
(effect defined in `se_QING_*`; invoked inside the `every_country` game-init loop ≈ line 2397).

The 1815 baseline seeds CHI to ~one year of its own costs (sourced 1815–25 reserves,
tasks #172/#174). A different year needs a different figure: a peak-Qing year opens with a
large surplus (research: ~70–80 M tael Qianlong-era reserve), a late-decline year with a
strained treasury. Re-derive the number from the research package and update the seed.
Also revisit any per-country starting-wealth or reserve calibration keyed to 1815.

---

## 5. STARTING BUILDINGS / OOB (concrete on-map objects)

- **Buildings seed:** `common/scripted_effects/se_QING_BUILDINGS.txt` →
  `SE_qing_starting_buildings` (12 buildings via the `QING_seed_building` macro, guarded by
  `owner=c:CHI` + `trade_goods` match + `NOT has_building`, sentinel `chi_starting_buildings_done`).
  Invoked at `oa_economy_setup.txt:2188`. If the year's economy or territory differs, adjust
  which buildings seed where (a peak year may warrant more/greater works; a province lost to
  CHI can't hold a CHI seed).
- **Army/navy OOB:** `common/scripted_effects/imp19c_effects_legion_setup.txt`
  (`SE_qing_armies`, `SE_qing_navy`) + `common/scripted_effects/se_MOBILIZATION.txt`.
  The OOB is sourced to a specific decade (1815: Eight Banners + Green Standard strength,
  coastal 水師). A different year changes garrison sizes and which forces exist. Re-derive
  from research; keep the idempotency guard (`qing_armies_setup_done`).

---

## 6. STARTING CHARACTERS

**File:** `setup/characters/00_Qing.txt` (≈2066 lines; historical Aisin Gioro line +
court). Also per-tag files for neighbours whose rulers change with the year
(`00_British Empire.txt`, `00_Ottoman Empire.txt`, `00_India.txt`, etc. — all appear in the
dated-file grep).

Each character block: `first_name`, `family_name`, `birth_date`, `death_date`,
`culture`, `religion`, traits, optional `dna`, `father`/`mother` links (`char:NNN`).

**Year-swap character work:**
1. **Reigning monarch** — the ruler alive and on the throne in the target year (peak-Qing =
   the Qianlong Emperor, not the 1815 Jiaqing/Daoguang line). Set/confirm the ruler
   assignment in the CHI setup block (`setup/main/00_default.txt` character section) and
   ensure the person has a live character with correct birth/death dates bracketing the year.
2. **Court roster** — ~15–30 court/empire figures alive in the target year, with correct
   ages (birth_date before start, death_date after), roles, and stats. Add the ones who
   belong to that era, and ensure those who died before the target year are NOT the
   game-start office-holders (they can still exist historically if born earlier).
3. **DNA / portraits** — reuse existing dna strings for continuity; a new character can
   borrow a plausible existing dna block.
4. **Office/Grand-Council seeding** — the court-bench seed (#166/#177) and Grand Council
   holders must reference characters alive in the target year. Check `se_QING_*` seeds that
   save named characters into office variables.

Cross-check every `char:NNN` reference still resolves and no office is seeded to a
pre-dead character.

---

## 7. LAWS / GOVERNMENT / INSTITUTIONS

**File:** `setup/main/00_default.txt`, CHI block (≈35644): `government`, `primary_culture`,
`religion`, and the law list (`citizens_rights`, `regional_government_law`, `judiciary_law`,
`cultural_protections_law`, `religious_law`, `non_tribal_land_law`, `labour_organisation_law`,
`business_regulation_law`, `army_supply_law`, `army_recruitment_law`) plus `poptype_rights`.

A different era may warrant different laws (a peak-Qing high-competence bureaucracy vs a
declining one). Change only what the research justifies; log each change.

---

## 8. BOOKMARK METADATA (cosmetic, if present)

`grep -rln bookmark common/ gui/ game/` — the 1815 baseline references a bookmark in
`oa_economy_setup.txt` (comments) and `gui/shared/portraits.gui`. If a formal bookmark
definition exists, update its date/title/description and the shownd characters. (For the
current build the "bookmark" is effectively just START_DATE + setup; no separate dated
bookmark entry drives gameplay.)

---

## 9. VERIFY → REVIEW → COMMIT

1. **Brace-balance** every edited `.txt` (Python brace counter; remember braces inside
   strings/comments trip the naive counter — diff against `git show HEAD:` to prove a
   pre-existing imbalance isn't your regression).
2. **BOM check** each file matches its directory convention (se_*/modifiers = NO BOM;
   on_action/trade_goods/localization/buildings = UTF-8 BOM). Wrong BOM → engine rejects.
3. **Grep sweep** for any residual old-year date you missed (repeat §2's grep).
4. **Deep adversarial-review workflow** (dimensions → per-finding refutation → synthesis).
5. **Commit as freekumquats**, SESSION_REPORT entry, decisions doc updated.

---

## Quick checklist (copy per run)

- [ ] `START_DATE` in `00_defines.txt`
- [ ] All dated events/on-actions/scripted-effects re-based (§2 grep clean)
- [ ] Borders: `own_control_core` moved on BOTH sides for every changed province
- [ ] Treasury seed re-derived (`QING_seed_starting_treasury`)
- [ ] Buildings seed adjusted (`SE_qing_starting_buildings`)
- [ ] Army/navy OOB re-derived (`SE_qing_armies`/`SE_qing_navy`)
- [ ] Reigning monarch + court roster alive & correct (`00_Qing.txt`, setup ruler)
- [ ] Neighbour rulers for the year (per-tag character files)
- [ ] Laws/government reviewed
- [ ] Bookmark metadata (if any)
- [ ] Brace + BOM + residual-date verify
- [ ] Adversarial review passed
- [ ] Committed as freekumquats + SESSION_REPORT + decisions doc
