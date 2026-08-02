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

### C2 — Mexico lift (DONE, pre-review)
- NEW `common/missions/qing_mexico_missions.txt` (group `qing_mexico_mission`) + NEW
  `localization/english/qing_mexico_l_english.yml` (BOM). Tasks: galleon (re-rooted: dropped
  `requires = qing_col_bureau`), veracruz, maximilian, mexican_empire — VERBATIM (mexican_empire keeps
  its LEGITIMATE `QING_establish_protectorate` client-Empire release + its se_QING_MEXICO.txt arc hooks).
- Moved with the arc: the consumer-event loc keys `qing_mexico_adventure.1.*` (namespace confirmed
  `qing_mexico_adventure`, keys `.1.t/.desc/.a/.a.tt/.b/.b.tt` — verified against the event file, NOT the
  misleading `ln` display artifact). Also `qing_col_needs_pacific_reach/acapulco/mexico_land_tt` + the
  silver_road/gulf_gate/mexican_crown/mexican_empire_mod modifier names + `qing_protectorate_mexico_name/adj`.
- Art REUSE: `icon = qing_colonization_mission` / `header = mission_image_qing_colonization` (this arc is
  the Pacific enterprise's American terminus; both DDS exist).
- Removed the Mexico section (280 lines) from the colonization tree + its loc block. Colonization braces
  417/417; mexico braces 135/135; capstone `requires` references only kept Oceania tasks; no dup loc keys.
- **Review (code-review agent):** PASS with one MEDIUM finding — the new tree's mission-group loc keys
  (`qing_mexico_mission:0` + the 4 `_DESCRIPTION/_CRITERIA/_REWARD/_BUTTON` suffixes) were absent (the
  verbatim loc extraction never included them, since the arc rendered under the parent
  `qing_colonization_mission` title pre-split). FIXED: added the 5 group keys matching the verified
  sibling convention (all 19 other mission-group loc files carry the identical suffix set). Re-verified
  directly (5 keys present, BOM intact) — pure loc addition on a proven pattern, no re-review agent needed.


### C3 — New-World lift (plan)
Moving amur/alaska/canada/california/daoguang + anxin (the New-World MARCH, travels with its arc like
anfei did in C1) to NEW `qing_new_world_missions.txt`. This ORPHANS three `requires` in the Oceania tree:
- **capstone** requires canada+california (leaving) → re-root to kept Oceania tasks (pacific_isles +
  new_guinea). Its `allow` (holdings/modifier checks incl. California 1493/golden_shore) is UNCHANGED, so
  it still demands real far-flung conquest.
- **anbei** + **andong** require amur (leaving) → re-root onto `qing_col_bureau` (kept root) as a
  BOOT-SAFETY BRIDGE. These two marches relocate to their proper homes (CA tree / Japan tree) in P3; the
  bridge just keeps them reachable in the interim so C3 is independently boot-safe.
Re-roots inside the New-World tree: amur drops `requires=bureau` → tree root; daoguang drops
`requires=bureau` → second root (independent US-entente diplomacy, gated on tree potential + exists c:USA).
alaska→amur, canada→alaska, california→alaska, anxin→california all stay intra-tree.

### C3 — New-World lift (DONE, pre-review)
- NEW `common/missions/qing_new_world_missions.txt` (group `qing_new_world_mission`) + NEW
  `localization/english/qing_new_world_l_english.yml` (BOM). Moved: amur/alaska/canada/california/
  daoguang + the anxin MARCH (travels with its arc, like anfei in C1). amur+daoguang re-rooted (both
  dropped `requires=bureau` → two independent roots); alaska→amur, canada→alaska, california→alaska,
  anxin→california stay intra-tree. All New-World internal `requires` resolve; no cross-tree requires.
- **Orphan re-roots in the KEPT Oceania tree (boot-safety):** capstone dropped canada+california (gone)
  from its `requires`, now requires pacific_isles+new_guinea (its `allow` still demands a real New-World
  holding, so it stays an all-oceans capstone); anbei+andong re-rooted amur→bureau as interim bridges
  (they relocate to CA/Japan trees in P3). All three annotated in-code with [#27 split] comments.
- Moved 28 loc keys (task title/DESC/tt + needs_usa/newworld tooltips + anxin name/adj + fur_coast/
  pacific_trade/golden_shore/daoguang modifier display names). Shared `qing_col_needs_strong_fleet_tt`
  KEPT in colonization loc (still used by 2 kept Oceania tasks). No dup keys across all 4 loc files.
- Braces: colonization 296/296, new-world 134/134.
- **DEFERRED (cosmetic):** Oceania group English title still "The Great Pacific Enterprise" — its final
  contents aren't settled until C4 (delete xinjiang/central_asia) + P3 (relocate land marches), so the
  rename to the Oceania/South-Seas enterprise is deferred to end-of-split to avoid churn. Chinese
  (大洋洲事業 = Oceania Enterprise) already correct.
- **Review (code-review agent):** PASS, no defects. Verified all requires resolve in-file (no dangling
  cross-tree requires — the chunk's #1 risk), byte-identical relocation vs 073e2cb62, loc completeness,
  no dup keys across all 4 loc files, BOM/CJK. One harmless non-defect noted: `qing_col_amur_frontier:0`
  modifier display was left in the colonization loc though its granting task (amur) moved. FIXED for
  locality — moved it to the New-World loc (pure organization, no behavior change; re-verified no dup).

### C4 — delete duplicate xinjiang/central_asia (DONE, pre-review)
- SALVAGE-CHECK FIRST (DESIGN §D): confirmed the dedicated trees fully cover the deleted content —
  `qing_central_asia_missions.txt` embraces KOK/BUK/KHV as sinosphere_tributary (via
  `se_QING_CENTRAL_ASIA.txt QING_ca_embrace_khanates`), claims every Turkestan province (qing_ca_begs),
  seeds military colonies + frontier forts region-wide, revives the Silk Road; `qing_xinjiang_missions.txt`
  has a dedicated Urumqi task + region-wide forts/colonies/karez. The two colonization tasks' specific
  point-claims (Alma-Ata 8238 / Bishkek 7038 / Tashkent 9370 / Kokand 110) fold into the Anxi/Anbei march
  founding in P3 per DESIGN §4.1; nothing unique is lost.
- Deleted `qing_col_xinjiang` + `qing_col_central_asia` tasks (96 lines) + their dead task-facing loc keys
  (titles/DESC/tt + needs_xinjiang_tt/needs_strong_army_tt). Left the modifier DEFINITIONS + their display
  names (qing_col_xinjiang_province/silk_road) intact per DESIGN §4 (lowest-risk; modifiers load globally).
- Re-rooted orphaned `qing_col_anxi` (required deleted xinjiang) → bureau bridge (relocates to CA tree in P3).
- Cleaned stray empty loc comment-headers left by C3/C4 migrations.
- FINAL SPLIT VALIDATION: all 11 live `requires` in the Oceania tree resolve in-file; africa/mexico/
  new_world all resolve; braces balanced (coloniz 240/240, africa 105/105, mexico 135/135, nw 134/134);
  no dup loc keys across all 5 loc files.
- **Review (code-review agent):** PASS on boot-safety + loc integrity. One MEDIUM content-loss finding:
  the deleted qing_col_central_asia granted claims on Tashkent (9370) + Kokand (110), both region
  **Fergana** — but qing_ca_begs only sweeps **Turkestan**, so those 2 Fergana claims had no home
  (Alma-Ata 8238 + Bishkek 7038 ARE Turkestan → already re-homed by qing_ca_begs). FIXED per DESIGN §4.1
  (oasis claims belong to the Anxi/khanate theatre): added a guarded `every_province is_in_region=Fergana
  add_claim` sweep to `qing_ca_khanates` (the task that overawes KOK/BUK/KHV) — re-homing the lost claims
  into the tree that conquers that ground, using the proven idiom already shipped at CA tree lines
  172/304/342. Reviewer's Urumqi-2930 note = acceptable per the region-wide good-enough abstraction rule
  (forts/colonies still seeded region-wide; qing_xj_fortify gates on a Tarim-area fortress). CA braces balanced.

### P1+P4 — march subsystem core (se_QING_MARCH.txt) (DONE, pre-review)
NEW `common/scripted_effects/se_QING_MARCH.txt`:
- **QING_found_march** (P1): LAND_release_from_list (proven fallback per R2 — dynamic tag, NOT the
  unproven mint) spins the conquered-local land into the march; change_government=megacorporation;
  FUNC_make_subject type=frontier_protectorate under CHI; QING_march_appoint_gg; subordinate the
  theatre's OTHER locals as the march's OWN subjects (overlord=march, type=protectorate); seed the army.
- **QING_march_appoint_gg**: creates the Manchu GG IN THE MARCH SCOPE + set_as_ruler there (the proven
  MEX_install_empire idiom, se_MEXICO.txt:398) — this deliberately AVOIDS the unproven cross-country
  create-in-CHI-then-set_ruler primitive (design M5). Gated on a seated Lifan Yuan holder; graceful no-op
  otherwise (#90 gotcha honoured: set_as_ruler is a separate statement outside create_character).
- **QING_march_size_army** (P4/H3): reconciles the march's host to its tier target (small/med/high =
  10/20/30 cohorts @ COHORT_SIZE 500 = 5k/10k/15k men, + relief bonus). Raises shortfall in the MARCH
  scope (its own troops); CHI pays manpower ONLY for the raised cohorts (add_manpower {value multiply -500}
  on ROOT=CHI) — a march at target costs 0 manpower/quarter (H3 corrected). Over-target (tier lowered):
  destroy_unit all + re-raise to lower target (proven verb; ordered_army/disband_unit NOT attested here),
  guarded is_at_war=no so a march is never stripped mid-campaign.
- **QING_march_pay_subsidy** (P4): quarterly on ROOT=CHI (wired into qing_mechanics_pulse_on_action after
  QING_subject_collect_tribute). every_subject{ frontier_protectorate + subsidy tier }: gold stipend
  15/30/45 CHI->march, CLAMPED to CHI treasury (tribute-model clamp); then QING_march_size_army. Mirror
  of QING_subject_collect_tribute, flow reversed — proven inline-transfer forms, not invented svalues.
- **QING_march_set_subsidy** (P6-effect): S/M/L exclusive modifier swap + tier var + immediate army resize.
- Supporting: 2 svalues (qing_march_ncohorts_svalue, chi_treasury_svalue — RHS-operator rule), 3 modifiers
  (qing_subsidy_small/medium/high in subject_rework_mods.txt). Braces 130/130.
- Verified proven: LAND_release_from_list, FUNC_make_subject any-overlord, create_unit-in-country-scope
  (Konbaung rally), set_as_ruler-in-target (MEX), change_government (Mexico/old protectorate), add_manpower
  deduct, ncohorts, destroy_unit, female=no, count=var:X. NOT-yet-called by missions (P3 wires it).
- **Review (code-review agent, 2 passes):** Pass 1 found HIGH create_unit off-by-one (base sub_unit +
  `while count=N` raises N+1, so the army overshot by 1, never converged, and thrashed destroy+rebuild
  every peacetime quarter) + MEDIUM subject-guard (would yank a polity from its existing overlord).
  FIXED: raise_count = shortfall-1 (total = raise_count+1 = shortfall); positive branch gated shortfall>=1;
  down-step gated shortfall<=-1 (rounding never trips it → a march at target sits STABLE); manpower bills
  the true raised count; local-subordination guard → `NOT is_subject=yes` (only free polities taken).
  Pass 2 (re-review): BOTH fixes CONFIRMED correct — convergence verified, count=0 while-loop safe (mints
  just the base cohort), target=0 disbands to nothing without a negative count reaching create_unit,
  manpower never double-docked, is_subject attested. No new defects. Braces 135/135.

### P3a — rewire the three OVERSEAS marches to QING_found_march (DONE, pre-review)
Anhai (colonization/Oceania), Anxin (New-World), Anfei (Africa) swapped from the old
QING_establish_protectorate to the new QING_found_march (se_QING_MARCH.txt). These three needed ONLY the
effect swap — their region lists already gather the player's COLONIZED overseas holdings (Pacific isles /
Alaska-BC-California / African coast), which are legitimately non-core frontier land (the old backwards
bug was the LAND marches carving CHI HEARTLAND — Mongolia/Liaoning/Vietnam). All three: maritime = yes
(they get navies, DESIGN §3.3); locallist = qing_march_locals_list (empty for now — they found from the
colonized land + grow via the P5 expansion pulse; per-theatre island/coastal polity tags are follow-up).
QING_establish_protectorate is UNTOUCHED for its legitimate callers (Lanfang republic + Mexican Empire).
Braces balanced (coloniz 240, nw 134, africa 105). REMAINING for P3b: the four LAND marches
(anbei/andong/anxi/annan) still call the old effect on CHI-CORE regions — they need region-retargeting +
relocation to their conquering trees (CA/Burma/Japan) per DESIGN §4.1/§4.2.
- **Review (code-review agent):** PASS, no defects. Confirmed: arg-contract match (all 6 macro args,
  government= correctly dropped since the effect hardcodes megacorporation); empty locallist is SAFE (an
  unpopulated list name = empty list; the any_in_list guard skips subordination, every_in_list cleanup
  no-ops); the `maritime = yes` → `$maritime$ = yes` → `yes = yes` trigger is a PROVEN shipping idiom
  (qing_works_events cheap=yes, se_MOBILIZATION floor=yes); overseas-only regions (no CHI core carved);
  both working lists cleaned at the effect tail (no carryover). Braces balanced.

### P3b-1 — Anxi relocated to the Central Asia tree + retargeted (DONE, pre-review)
- NEW task `qing_ca_anxi_march` in `qing_central_asia_missions.txt` (requires qing_ca_ferghana — holding
  conquered oasis ground). RETARGETED per DESIGN §4.1: carves from Fergana/Bukhara/Khwarezm (the OASIS
  khanates) — NOT "Turkestan" (the Kazakh steppe, the old task's mis-target) and NOT already-Qing Tarim.
  Subordinates the conquered KOK/BUK/KHV (which the CA tree makes CHI tributaries) as the MARCH's own
  princely states via QING_found_march. Land march (maritime=no). icon reuses qing_ca_ferghana.
- **Effect fix (subordination guard):** QING_found_march's local-guard changed from `NOT is_subject=yes`
  to `OR { is_subject=no  is_subject_of=ROOT }` — the LAND marches' theatre polities are ALREADY CHI
  subjects when founded (conquered into the sinosphere by the CA/Burma/Japan trees), so the march must be
  able to REPARENT CHI's own subjects down to itself (CHI→march→khanate nesting, viable per memory), while
  still never yanking a FOREIGN overlord's subject. This is the branch that actually populates land-march
  princely states (P3a's overseas marches pass an empty locallist; this is the first real use).
- Removed the OLD backwards `qing_col_anxi` (carved Turkestan as a fake tributary) from colonization;
  moved its loc to CA loc + added retargeted text + 2 new tooltip keys (qing_ca_anxi_march_tt,
  qing_ca_needs_oasis_land_tt). Braces: CA 215/215, coloniz 224/224. No dup loc keys; no dangling requires.
- **Review (code-review, 2 passes):** Pass 1 PASS on mechanics + found MEDIUM (founding Anxi soft-locks the
  CA capstone — carving CHI's Fergana land + reparenting the khanates breaks the capstone's allow, and both
  branched independently off qing_ca_ferghana) + PLAUSIBLE (FUNC_make_subject may not cleanly reparent an
  already-bound subject; se_FUNC releases first). FIXED: (1) qing_ca_anxi_march now requires the CAPSTONE
  (founded after the region is pacified — no soft-lock, acyclic, narratively right); (2) release-then-rebind
  in QING_found_march (release_subject from CHI before make_subject to the march, proven se_FUNC idiom).
  Pass 2 (re-review): BOTH fixes CONFIRMED correct, no new defects. This validates the reusable pattern
  (capstone-gate + release-then-rebind) for the remaining land marches Annan/Andong/Anbei.
