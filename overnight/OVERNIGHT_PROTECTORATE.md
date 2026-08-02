# OVERNIGHT_PROTECTORATE.md — build log & decisions for the #27 colonization/protectorate rework

**Branch:** `merge-overnight`. **Task tag:** `#27`. Commits authored by `freekumquats`.
Companion to `design/DESIGN_PROTECTORATES_GENERAL.md` + `design/DESIGN_COLONIZATION_SPLIT.md`.
Autonomous overnight build (user directive 2026-08-02): implement both design docs, review each
chunk as it finishes, commit after successful review, do not defer tasks.

This doc records every non-obvious decision taken during the build — especially the places where a
design-doc primitive was UNPROVEN and I chose a proven fallback rather than ship an untestable path
(I cannot run the boot-test spikes the doc calls for; the user boot-tests on a separate machine).

---

## KEY RESOLUTIONS (taken before writing code)

### R1 — `QING_establish_protectorate` is KEPT for Lanfang + Mexican Empire; marches get a NEW effect.
`rg` shows `QING_establish_protectorate` is called by NINE sites: the 7 march tasks PLUS
`qing_col_lanfang` (a client republic release) and `qing_col_mexican_empire` (a client imperial-monarchy
release). Lanfang and the Mexican Empire are **legitimate** releases of conquered/held land as ordinary
sinosphere-tributary client states — they are NOT the EIC-style frontier marches, and the design doc's
scope excludes them. **Therefore: leave `QING_establish_protectorate` intact (Lanfang/Mexico keep using
it verbatim), and write a NEW effect `QING_found_march` for the seven 都護府.** This avoids breaking the
two correct releases and keeps the two mechanics cleanly separate.

### R2 — Marches are founded via the PROVEN `LAND_release_from_list`, NOT the unproven mint path.
`DESIGN_PROTECTORATES_GENERAL §5/§8.0` flags `create_country → change_country_tag`-to-a-predefined-code
as UNPROVEN (no repo precedent as a unit) and offers "a dynamic tag with a scripted custom name" as the
explicit fallback. Since I cannot run the isolation spike, I take the fallback as the primary path:
- `QING_found_march` uses `LAND_release_from_list` (the SAME proven verb Lanfang/Mexico/the old effect
  use) to spin the march off a province list, binding it as `frontier_protectorate`, government
  `megacorporation`, with a scripted `country_name`/`country_adj` loc key.
- **No predefined tags are minted.** This removes the entire tag-mint + `create_country` +
  `change_country_tag` boot-safety surface. The march is a dynamic tag (loses the fixed 3-letter code +
  predefined COA — the doc accepts this as the fallback cost).
- **The province list is the theatre's CONQUERED-LOCAL land, region-gated** (per DESIGN §4.1 the seven
  theatres are RETARGETED so their regions contain conquerable local land, NOT CHI home core — Kazakh
  steppe / fragmented Japan / oasis khanates / independent SE-Asia / the overseas coasts). The OLD bug
  was releasing CHI *core* (Mongolia/Liaoning/Vietnam regions that ARE Qing heartland); the retargeted
  regions are frontier conquest, so a region-gated owned-province list captures only conquered land.
  Guard: `is_capital = no` (never release CHI's capital) + the theatre regions are non-core by construction.

### R3 — The Vietnam fidelity fix (§4.3) is already committed (44fc08111). Task #33 DONE.

### R4 — Build order = the two docs' own phasing. Split FIRST (pure relocation, boot-safe), then marches.
Per `DESIGN_COLONIZATION_SPLIT §5` + `DESIGN_PROTECTORATES_GENERAL §8.0` Phase 1:
each chunk below is independently boot-safe, independently reviewable, committed after its own
adversarial `code-review` passes (+ re-review of fixes). No chunk is committed unreviewed.

---

## CHUNK LEDGER (status updated as each lands)

### Split (DESIGN_COLONIZATION_SPLIT)
- **C1** Lift Africa arc → `qing_africa_missions.txt` (+ loc). — _pending_
- **C2** Lift Mexico arc → `qing_mexico_missions.txt` (+ loc). — _pending_
- **C3** Lift New-World arc (amur/alaska/canada/california + daoguang) → `qing_new_world_missions.txt`
  (+ loc); re-root on Oceania `bureau`. Oceania tree keeps bureau/taiwan/pacific/new_holland/new_guinea/
  lanfang. — _pending_
- **C4** Salvage-check then DELETE `qing_col_xinjiang` + `qing_col_central_asia` (confirm the dedicated
  `qing_xinjiang_missions.txt` / `qing_central_asia_missions.txt` cover their content). — _pending_

### Marches (DESIGN_PROTECTORATES_GENERAL), Phase 1 proven core
- **P1** `QING_found_march` effect (release-from-conquered-local, bind frontier_protectorate, megacorp
  govt, GG install, subordinate other locals, seed army). Keep `QING_establish_protectorate` for
  Lanfang/Mexico. — _pending_
- **P3** Found the marches from their conquering trees (Anxi/Anbei → CA tree; Annan → Burma tree;
  Andong → Japan tree; Anhai/Anxin/Anfei → colonization branch capstones); retire old `qing_col_an*`
  march tasks. — _pending_
- **P4** `QING_march_pay_subsidy` quarterly (money reverse-tribute clamped to CHI treasury; army
  maintained to tier target; manpower docked from CHI only on raise, per H3). — _pending_
- **P5** `QING_march_expand_check` yearly (low-chance conquest gated on peace + colonize unowned). — _pending_
- **P6** subsidy low/med/high toggle GUI + `QING_march_set_subsidy`. — _pending_

### Marches Phase 3 (documented fallbacks where a primitive is unproven)
- **P7** `QING_march_integrate_pulse` (march-specific direct-absorb, per H1). — _pending_
- **P8** march war-relief event (relief-army-as-target-bump per H4; join-war option). — _pending_
- **P9** maritime navies (H2 — proven fallback = raise in CHI scope + transfer, since subject-scope
  navy raise is unproven). — _pending_

---

## DECISION LOG (appended as taken)

### C1 — Africa lift (DONE, pre-review)
- NEW `common/missions/qing_africa_missions.txt` (group `qing_africa_mission`) + NEW
  `localization/english/qing_africa_l_english.yml` (BOM). Tasks: zheng_he (re-rooted: dropped
  `requires = qing_col_bureau`, now the tree's own root on the shared self-str/High-Qing gate), cape,
  suez, congo, anfei. VERBATIM relocation (anfei still calls `QING_establish_protectorate` — the march
  rewire is deferred to chunk P3, keeping this lift a pure boot-safe relocation).
- Art REUSE: `icon = qing_treasure_fleet_mission` / `header = mission_image_qing_treasure_fleet` (both
  DDS exist; an ocean-going treasure fleet fits the African voyages). No generator run needed.
- Removed the Africa section (219 lines) from `qing_colonization_missions.txt` + its 43-line loc block
  from `qing_colonization_l_english.yml`. Braces balanced (541/541); no dangling `requires`; no dup loc keys.
- **DEVIATION (intended, documented):** `qing_col_zheng_he`'s fleet-gate OR gained a 4th arm
  `has_variable = qing_high_qing_era`. NOT in the original. REQUIRED: zheng_he is now the tree ROOT and
  the three original fleet modifiers are all 19th-c. Self-Strengthening grants absent at a 1763 start, so
  without the era escape the tree would open (its `potential` admits High-Qing) but its root task could
  never complete at the 1763 bookmark it exists for. Mirrors the identical #315 escape already on
  `qing_col_pacific_isles`/`_new_holland` and the parent root `qing_col_bureau`. Never set at 1815.
- **Review (adversarial code-review agent):** PASS. Verified brace balance, verbatim relocation fidelity
  (all province ids/modifiers/severities/LOG strings identical to git HEAD), loc completeness, BOM
  conventions (txt no-BOM, yml BOM), CJK integrity (鄭 not 鄧). Only flag = the era-escape deviation
  above (confirmed correct + necessary; comment sharpened, no functional change → no re-review needed).
