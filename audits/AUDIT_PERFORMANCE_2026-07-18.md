# Performance & Correctness Audit — 2026-07-18

Branch: `merge-overnight` (== `1763_bookmark` @ 516677513 after tonight's merge).
Scope: deep scan of the Qing player-experience suite for performance optimizations,
bugs, dangling references, and dead code — with special focus on the **Grand Council**
(the centerpiece for most new features).

Method: 9 parallel read-only scan agents over ~29k lines of `common/scripted_effects/`,
68 `scripted_guis`, 64 Qing event files, 132 GUIs, plus on_actions and setup. Findings
verified by grep across the whole repo before inclusion. **No files were edited for this
audit — this is diagnosis only.**

---

## 0. Performance model (governs every recommendation)

**Cost = frequency × per-call cost.** The hot path is the quarterly pulse
`qing_mechanics_pulse_on_action` (`common/on_action/00_monthly_country.txt:66`), which is:
- gated `tag = CHI  is_ai = no` (human Qing only), and
- throttled to 90 days via `qing_mechanics_pulse_cooldown`.

It fans into: `QING_DECLINE_pulse` → `QING_sphere_pulse` → `QING_GOV_pulse` →
`QING_fgar_scan` → `QING_sinic_pulse` → `QING_COLON_nwcrop_diffuse` → event rollers.

Consequences that shape the whole audit:
- **Gated/inert content costs ~zero runtime CPU.** Deleting CHI-gated or trigger-blocked
  content saves load-time, memory, and save-file size — *not* per-tick CPU.
- **Real per-tick CPU** lives in: (a) work that runs every pulse regardless of outcome,
  (b) ungated MTTH events evaluated for many countries, (c) global (non-CHI) on_actions,
  and (d) extra AI-simulated setup countries.
- The heaviest confirmed hot cost is the **Grand Council / ministry recompute** (§1).

---

## 1. HEADLINE FINDING — Grand Council recompute does many full-world character scans every pulse

**Status: CONFIRMED by direct inspection (not yet agent-corroborated — deep-dive agent in flight).**

Every quarterly pulse, `QING_GOV_pulse` (`se_QING_GOVERNANCE.txt`) runs **both**:
- `QING_ministry_recompute_all_perf` (`:9`), and
- `QING_council_recompute` (`:12`),
then `QING_council_apply_band` (`:33`) and `QING_council_apply_officer_buffs` (`:45`).

`QING_ministry_recompute_all_perf` (`se_QING_MINISTRY.txt`) dispatches to **13 per-office
recomputes** (censor, chamberlain, grand_secretariat, guard_commandant, justice, lifanyuan,
personnel, revenue, rites, war, works, zongli + guard bayara readiness).

Confirmed scan counts (grep):
- `se_QING_MINISTRY.txt`: **5 `every_character`** full-world scans
- `se_QING_COUNCIL.txt`: **1 `every_character`**
- `se_QING_GOVERNANCE.txt`: an `every_owned_province` sweep at `:274`

So the council layer performs on the order of **half a dozen+ full character-table scans
plus province sweeps every 90 in-game days, for the entire game**, with several per-office
recomputes independently re-scanning the same court to tally their own corps counts and the
Manchu/Han split.

**Prime optimization (likely the single biggest CPU win in the mod):** collapse the repeated
per-office `every_character` passes into **one shared character sweep** that classifies each
courtier once (which office/corps he holds, his culture) and writes all the per-ministry
tallies + the council Manchu/Han split in a single iteration. Deep-dive agent (§8) is
quantifying the exact collapsible count and confirming feasibility.

*(This section will be expanded with the Grand Council deep-dive agent's precise scan count,
candidate-builder sync check, vacate-symmetry check, and dead-code list when it reports.)*

---

## 2. Hot-path core (DECLINE / GOVERNANCE / COUNCIL / MINISTRY / FACTION) — DONE

**Execution model confirmed:** `QING_GOV_pulse` calls `QING_ministry_recompute_all_perf` (`se_QING_GOVERNANCE.txt:333`)
then `QING_council_recompute` (`:336`), every ~90 days for one country forever. All 19 `_cmpsvalue`
refs defined; **no dead effects, no dangling refs, no illegal RHS** in this cluster.
`QING_DECLINE_scan_ethnic_target` + `QING_DECLINE_civic_assimilation` are correctly ANNUAL
(`00_yearly_country.txt:88,92`), not on the quarterly path — good.

**PERFORMANCE — ~12 unbounded iterators run back-to-back per `recompute_all_perf` call. Ranked:**

- **P1 (HIGHEST — the headline): SIX full-world `every_character` walks per quarter.**
  `se_QING_MINISTRY.txt:431` (zongli), `:1127` (censor), `:1219` (justice), `:1353` (guard), `:1441`
  (personnel) + `QING_harem_recompute_roster` (`se_QING_HAREM.txt:127`, called from chamberlain perf
  `se_QING_MINISTRY.txt:1032`). `every_character` is the **global** iterator (no scoped
  `every_employed_character` exists in this codebase — confirmed 0 uses), so each visits *every living
  character in the world* and filters `employer=ROOT`. Six independent global walks per dispatcher call.
  **Fix:** collapse into ONE `every_character { limit = { employer=ROOT is_alive=yes } }` pass that per
  character tests each marker (qing_zongli_diplomat / qing_is_censor_inspector / qing_justice_accused /
  qing_is_imperial_guardsman / qing_is_harem_consort / is_governor) and appends to the matching roster+count.
- **P2 (HIGH): two full `every_owned_province` sweeps, one redundant.** Works
  (`se_QING_MINISTRY.txt:510`) and Revenue (`:736`). Revenue only tallies `qing_granary_building` —
  which the Works sweep **already counts** (`:555`). **Fix:** build the granary roster inside the Works
  sweep, delete Revenue's independent `every_owned_province`. Cuts one full province sweep/quarter.
- **P3 (MEDIUM): army/unit DB walked ~5× per quarter.** Council officer fold `every_unit`
  (`se_QING_COUNCIL.txt:449`) + War `every_army`(`:91`) `every_unit`(`:104`) `every_navy`(`:124`)
  `every_army`(`:135`). Council's `every_unit` and War's `every_unit` are the **same population**
  computing overlapping aggregates. **Fix:** compute officer count/martial in War's existing `every_unit`
  (War runs first in GOV_pulse, so cache-then-read is stale-safe); fold the two `every_army` passes into one.
- **P4 (structural): gather-once pre-pass.** `recompute_all_perf` also does `every_subject` in lifanyuan
  (`:268`) and rites (`:652`). Combined with P1/P2/P3 that's ~12 unbounded iterators back-to-back. The
  clean end-state: one pass each over court / provinces / subjects / units, classify into all rosters,
  feed every per-office compute. (This is the big refactor — HIGH risk, see fixes list.)
- **P5 (MEDIUM): `QING_council_refresh_candidates` called on the pulse** (`se_QING_GOVERNANCE.txt:348`) —
  a top-12 `ordered_character` global sort every quarter purely to warm a GUI cache the player may not
  open. Its OWN header (`se_QING_COUNCIL.txt:884-893`) says it should refresh **lazily, never on the hot
  path**. The pulse call contradicts the design. **Fix:** drop the pulse call (tab-open scripted_gui +
  `_by` already refresh on click), or dirty-flag it. **Low-risk, high-value.**

**CORRECTNESS**
- **C1 (low): `se_QING_DECLINE.txt:831,837,838`** — `var:qing_ethnic_stance_active` read with no
  `has_variable` guard (every sibling meter read guards). Seeded at boot (`qing_mechanics_on_actions.txt:86-87`),
  so errors only on a pre-init save. Fix: add the guard for consistency.

**DEAD CODE:** none in this cluster.

## 3. Spatial & subject-graph (SPHERE / FRONTIER / DIPLO / TRIBUTE / AMBAN / SUBJECT_QING) — DONE

**All cross-file refs / script_values / triggers grep-verified as DEFINED — no dangling references.**

**PERFORMANCE**
- **P1 (HIGHEST — cross-confirmed with §10 #1): `se_QING_SINICIZATION.txt:54-88`** — `QING_sinic_pulse`
  runs `every_governorships { every_governorship_state { every_state_province { … } } }` (hundreds of
  provinces) on **every 90-day pulse**, with 1-2 var writes per Han province. Only STEP 2 (annual
  baseline roll, `:111-153`) is throttled by `qing_sinic_year_cd`; the **count walk is ungated by
  design**. Largest uncached province walk in the cluster. Fix: gate the count walk behind a ~180d
  self-throttle (or recompute lazily on report-open via the already-shared `QING_sinic_recompute_delta`);
  at minimum skip the per-province `set_variable = qing_prov_sinicized` write when unchanged.
- **P2 (MEDIUM — yearly-throttled): `se_QING_SPHERE.txt:354-391`** — `QING_sphere_bleed_state` calls
  `QING_sphere_bleed_one_power` **4×** (china/britain/france/russia), each independently walking
  `every_state_province { every_neighbor_province { state } }` — the province→neighbor graph walked 4
  identical times, differing only in which `$power$_influence_snap` is compared. **Mitigated:** whole
  sphere pulse is gated `qing_sphere_cooldown days=365` (`:400-402`) — runs ~yearly, not per-pulse
  (the "build_ring every pulse" worry is correctly throttled). Fix (since yearly, medium): collapse
  the 4 power-walks into ONE neighbor pass raising all four maxes, then apply 4 pulls. ~4× cut.
- **P3 (acceptable): `se_QING_SPHERE.txt:103-157`** — `build_ring` province×neighbor walk + nested
  double `every_subject` (O(subjects²) sub-vassal walk) + O(ring²) dedup via `is_target_in_variable_list`.
  Yearly-throttled (P2 cooldown) so acceptable; no fix beyond keeping the cooldown.
- **Verified CLEAN (no action):** `QING_gp_scan_plays` (`se_QING_DIPLO.txt:667`, already merged to one
  pass #86), `QING_fgar_scan` (`every_army`, bounded), `QING_amban_evaluate` + `QING_subject_collect_tribute`
  (single non-nested `every_subject`).

**CORRECTNESS**
- **C1 (low live risk): `se_QING_DIPLO.txt:411`** — `QING_gp_partition` does `current_ruler = { add_popularity = -10 }`
  with no `exists` guard (the documented boot-crash context-switch class). Only reached from player
  GUI/mission in CHI scope where a ruler exists, so it won't fire at boot — but it's the one unguarded
  ruler context-switch in the cluster. Fix: wrap in `if = { limit = { exists = current_ruler } … }`.
- **C2 (defensive): `se_QING_TRIBUTE.txt:357-359, 391-397`** — GP-tension `var:qing_gp_tension_*` reads
  with no `has_variable` guard; safe *only* because `QING_gp_init` seeds them earlier same-pulse. Fix:
  call `QING_gp_init = yes` at the top of `QING_tribute_gp_interference_check` so a future pulse reorder
  can't break it.
- Verified clean: no illegal RHS comparisons (only comment lines), no unset-var reads, snapshot ordering correct.

**DEAD CODE**
- **D1: `se_QING_DIPLO.txt:438, 472, 475`** — `QING_gp_side_with_britain`, `QING_gp_side_with_russia`,
  `QING_gp_partition_russia` have **zero call sites** repo-wide, while their France/Britain siblings are
  live. Asymmetry looks like an authoring omission — the player-facing 以夷制夷 lever is incomplete
  without them. Recommend **wiring** them into the GUI/mission choices rather than deleting.
- D2 (not dead): `QING_tribute_expire_cooldowns` is an intentional doc-only stub (timer auto-expires).
- D3: all sphere/sinic/tribute/amban counters have live readers — no set-but-never-read vars.

## 4. Character-mint / roster (HAREM / EXAM / HOUSEHOLD / studies / SUBPOSTS / STUDENTS) — DONE

All OUR code; all quarterly/CHI-human. Redundant-scan multipliers are the story here.

**PERFORMANCE**
- **P1 (top offender): `se_QING_SUBPOSTS.txt:107,117`** — `QING_subpost_staff_corps` does **two** full
  `every_character` passes (strip-double-booked, then recount) and is called **3×/quarter**
  (`:169,177,185` diplomats/censors/guards) = **6 full global scans/pulse** + per-fill `any_character`
  (`:48`) + `ordered_character` (`:50`). **Fix:** merge strip+recount into ONE pass (strip if
  double-booked else count) → saves 3 scans immediately. **Low-risk, high-value.**
- **P2: double-recompute on harem/SS/US pulse paths** — each pulse recomputes the roster, then on a
  throttled roll calls a draw/favour effect that recomputes **again** (a 2nd full `every_character` same
  pulse): HAREM `:515`+`:371`, SS `:351`+`:285`, US `:395`+`:294`. **Fix:** drop the sub-effect's internal
  `QING_*_recompute_roster` when reached from the pulse. **Low-risk.**
- **P3 (larger refactor): ~7 independent full-world roster passes** (HAREM `:127`, HOUSEHOLD `:117`,
  SS `:160`, US `:159`, SUBPOSTS ×3) are logically ONE court-roster rebuild split across subsystems — a
  single shared bucketed `every_character` pass would collapse them. Same family as §1/§2/§12-#1 — this is
  the big **medium/high-risk** structural win.
- P4/P5 (no action): accountability + household-danger scans are `any_character` early-out + rarely-reached (gated).

**CORRECTNESS / BOOT-CRASH class**
- **C1 (verify, low risk): boot-reachable `create_character` + inline `add_trait` (status degree)** —
  SS `:103`, US `:105`, EXAM `:159` (jinshi/juren) all reachable at `on_game_initialized`. **Within the
  safe envelope** (type=status, and a fresh char holds no opposite → no opposite-resolution at
  construction — unlike the #5 crash we fixed, which added a degree to an EXISTING char who held `jinshi`).
  But these are the only boot-reachable create+add_trait sites left, so first suspects if boot AV recurs.
  Optional hardening: move the `add_trait` into the follow-up saved-scope block.
- **C2 (confirmed clean):** the `castrated` (health) eunuch grant is correctly removed from boot path.
- **C3 (low, runtime): `se_QING_HOUSEHOLD.txt:251`** — `add_trait = ambitious` on a seeded eunuch with no
  opposite guard. Runtime (not construction) so not the boot-AV class, but inconsistent. **Fix:** add
  `NOT = { has_trait = ambitious }` to the `ordered_character` limit. Low-risk.
- **C5 (fragile): `se_QING_STUDENTS.txt:119`** — `QING_students_graduate` reads `qing_students_graduate_mag`
  set only by its sole caller immediately prior. Safe today; fragile. **Fix:** pass as `$mag$` macro param.

**DEAD CODE**
- **D1: `se_QING_HAREM.txt:104-109`** — `QING_harem_rank_cap` has **zero callers** and its var
  `qing_harem_rank_cap_tmp` is **never read** (cap logic was inlined as literals). Fully dead. **Delete.**
- D2: `QING_harem_promote_consort` (`:419`) unused but **intentionally retained** (documented) — no action.

## 5. Economy & arcs (REVENUE / WORKS / COLON / OPIUM / SELFSTR / XINJIANG / ILI / MISSIONARY / …) — DONE

Cluster in good shape: cooldown guards present on heavy pulses, all script_values resolve, retired
`qing_mission_station` modifier survives only in comments (buildings via `QING_prov_has_mission` — clean).

- **DEAD CODE — D1 (MEDIUM): `QING_justice_pulse` (`se_QING_JUSTICE.txt:30`) has ZERO callers.** The Justice
  (刑部) domain is driven instead through `QING_accountability_pulse` (`QING_acc_score_office = { office=justice
  metric=unrest }`). So the whole per-quarter justice block — including an `add_stability = 5`/`-3` drift and a
  `qing_justice_arbitrary` province-modifier stamp — **never runs**. **Decision needed:** wire it into
  `QING_GOV_pulse` (it's a latent gameplay effect — that `add_stability` would matter) OR delete it if
  accountability fully supersedes it. This is a design call → **defer to user** (not auto-implemented).
- **PERF P1/P2 (throttled, acceptable):** `QING_COLON_nwcrop_diffuse` (3 global `every_province` + neighbor
  walk) and `QING_mission_stations_pulse` (province×pop + province×neighbor) — both **verified correctly
  365d self-throttled** + dormant/inert until crops arrive / treaty opens. Watch if province counts grow; no fix.
- **C1 (LOW): `se_QING_OPIUM.txt:198-199`** — scratch `qing_opium_net_flow_tmp` is set each pulse but never
  `remove_variable`'d (its 3 siblings are). Not a logic bug (re-set fresh each pulse) but leaks a stale scratch
  value into every save. **Fix:** add `remove_variable`. Low-risk.
- **C2 (LOW, design-confirm): one-way `qing_sect_pressure` nudges** — `se_QING_OPIUM.txt:247` (+1) and
  `se_QING_MISSIONARY.txt:229` (+1) both push `qing_sect_pressure` up when their band holds, and it has **no
  passive counter-drift** (relieved only by discrete events). Band-gated + clamped so not a guaranteed peg-to-100,
  but two systems feeding an un-drifting meter is the ratchet-rule pattern. **Confirm with design** whether
  event-only relief is intended → defer.
- Verified NON-issues: currency-stress ordering compounds correctly (additive nudge, not clobbered), granary
  region-selection fixed, affinity religion reads use proven scope-link form, nwcrop flip uses svalue idiom.

## 6. Scripted GUIs (all 68) — DONE. (OUR QING panels vs UPSTREAM — flagged separately.)

Cluster is built with the #443 fix in mind — QING panels route heavy buttons through `trigger_event`
trampolines. No duplicate definitions. No illegal RHS. Findings split by ownership:

### OURS (QING — in scope for fixes)
- **Cat 1 — per-frame `is_shown`/`is_valid` iterators (HIGH):**
  - `QING_works_ministry_panel.txt:117,130,151` (`any_owned_province` in **is_shown** — full province
    scan every frame the panel is visible) + `:64,80,97,158` (is_valid). **Fix:** cache a bool var on
    panel-open, read `has_variable`/`var:` in is_shown. Medium-risk.
  - `QING_household_panel.txt:45,78,109,112` (`any_character` full-court scan per frame).
  - `QING_censorate_panel.txt:138`, `QING_justice_panel.txt:78`, `QING_personnel_panel.txt:75`,
    `QING_mechanics_actions.txt:151,282`, `QING_revenue_ministry_panel.txt:82` (`any_character`/`any_owned_province` in is_valid).
  - `any_in_list` in is_valid (hanlin/SS/US/harem/princes/deliberative/xinjiang panels) — cheaper
    (materialized list), lower priority.
- **Cat 4 — unguarded `var:` reads in is_shown/is_valid (bug — mis-gates/frame errors):**
  - **`QING_mechanics_actions.txt:166`** — `var:qing_han_provincial_power >= 20` with no `has_variable`;
    var only seeded by a reform effect (`se_QING_SELFSTR.txt:583`), unset before then. **Fix:** add guard. Low-risk.
  - **`QING_mechanics_actions.txt:596,603,610`** — `var:qing_canton_purse_share` seeded only lazily in
    the canton pulse; unset if regime opens first. **Fix:** guard or seed at regime-flag time. Low-risk.
  - (`:17,26,35,258,267,278` read stance/regime vars that ARE startup-seeded — lower risk, confirm ordering.)
- **Cat 8 — dead QING panel buttons (0 refs; windows open via `gui.createwidget`/close via `GUI.ClearWidgets`,
  NOT these):** ~11 `*_open_panel_button` + ~23 `*_close_panel` scripted_guis. Also dead:
  `qing_gov_office_appoint_*` (13 variants), `qing_gov_office_vacate`, `qing_censorate_appoint_inspector`,
  `qing_guard_enrol_guardsman`, `qing_zongli_appoint_diplomat`, `qing_action_promote_civic`,
  `qing_action_customs_establish/sinicize`, `qing_harem_populated`, etc. **NOTE:** some (`qing_gov_office_appoint_*`,
  styling helpers) look like partially-migrated features, not removed code — **human check before deleting**
  (the appoint picker now routes through `qing_gov_office_appoint_selected`, so the per-office variants may
  be genuinely superseded). Dead-code deletion is parse/memory-only; low urgency; I will NOT bulk-delete
  ambiguous ones without confirmation.

### UPSTREAM (sobisonator — HIGH-RISK, FLAG ONLY, not edited)
- **Cat 3 — boot-inline `create_character`/sorting iterator in button effect (the #443 AV class):**
  `hoa_league_city_button.txt:77`, `mg_syr_merc_subject_button.txt:88`, `release_subject_button.txt:79,87`
  (inline `create_country`+`create_character`), `SUB_open_view.txt:21` (`ordered_subject` inline). These
  are a genuine boot-crash class but they're **upstream** files → flagged for review, not auto-fixed. (They
  evidently boot today, so either the path isn't hit at construction or the class is milder than #443; worth
  a targeted look but out of our low/medium batch.)
- Cat 1 upstream: `decentralize_realm_button.txt:24-71` (depth-3 nested iterator, twice/frame — worst per-frame
  cost in the mod), WAR/assemble/summon/subject-focus guis — all upstream, flag only.
- **Cat 6 — dangling `GetScriptedGui`:** `republic_party_button` (definition 100% commented out → fully
  dangling), `select_attacker_country`/`select_defender_country` (no definition). Upstream gui; flag.

## 7. Events / on_actions / GUIs + repo-wide dangling-reference sweep — DONE

**Headline: this cluster is in very good shape.** Repo-wide sets built (36,631 effects, 306 triggers,
4,284 script_values, 798 scripted_guis, 627 event ids) and every reference in scope diffed against them.

- **Perf CLEAN:** both pulse schedulers correctly gated `tag=CHI is_ai=no` + cooldown
  (`00_monthly_country.txt:67-72` quarterly/90d, `:39-49` integration/180d). Sibling USA/MEX pulses
  are single-tag O(1) rejects for other countries. **Zero `mean_time_to_happen`, zero
  `is_triggered_only=no`** across all 64 Qing event files — nothing engine-polled. GUI datamodels are
  rebuilt on button-open (not per-frame); no `every_`/`any_` iterator inside any `visible`/`enabled`.
- **Correctness CLEAN:** no dangling `trigger_event` ids; all 149 `GetScriptedGui('…')` refs resolve;
  **the `current_ruler.mother` boot-crash class is fully guarded** everywhere (dynasty/faction/princes/
  emeritus events all gate on `QING_dynasty_has_dowager` / `exists = mother` / `exists = primary_heir`).
  No illegal RHS. No undefined effect/trigger/scope refs. **Zero unresolved references repo-wide.**
- **DEAD CODE (low impact — bloat only, nothing fires them):**
  - `qing_censorate.5` (`qing_censorate_events.txt:357`) — superseded impeach trampoline (panel now fires `.6`).
  - `qing_justice.5` (`qing_justice_events.txt:345`) — superseded accuse trampoline (panel now fires `.6/.7/.8`).
  - `qing_war.3` (`qing_war_events.txt:275`) — a complete "Military Commission" event (trigger + 3 options +
    loc, naval option already fixed off the trireme stub) with **no caller**. Decision needed: **wire** it
    into the War Ministry panel/pulse (siblings `.1/.2/.4` are wired from `se_QING_WAR.txt`) or **delete** it + its loc.
  - Inert-but-harmless: `trade_calculation_on_action` + `random_microflavour_event_on_action`
    (`00_monthly_country.txt:217-244, 282-286`) — commented-out bodies, unregistered. Doc stubs.

## 8. Grand Council DEEP-DIVE (centerpiece) — DONE

**Headline count: ~20 full-world iterations every quarterly pulse** in the council layer — ~10 character-table
walks + ~6 army/navy walks + 4 province/subject walks.

**PERFORMANCE (ranked)**
- **P1 (CRITICAL — biggest win): shared character pass.** 6 `every_character` + 3 `any_character` walks
  each iterate the whole character table filtering `employer=ROOT` + one marker. ONE
  `QING_council_shared_char_pass` at the top of `QING_ministry_recompute_all_perf` can rebuild all rosters
  (zongli/censor/guard/justice/personnel/harem) + stamp eunuch booleans in a single walk; each per-office
  compute keeps its scoring but reads the pre-built list/count. **~10 char walks → 1** (~80-90% cut of the
  council layer's char-scan cost/quarter). **MEDIUM/HIGH risk** (structural; touches the just-fixed recompute path).
- **P2 (HIGH): war-ministry does 4 army/unit walks** (`MINISTRY:91,104,124,135`) — the two `every_army`
  passes iterate the identical set; the council `every_unit` (`COUNCIL:449`) re-walks commanders the war
  roster just built. **Fix:** merge the two `every_army`; have COUNCIL:449 sum over the already-built
  `qing_war_officer_roster`. 6 walks → ~3. Medium risk.
- **P3 (HIGH — boot): recompute storm at game start.** `QING_office_appoint` tail-fires `qing_office.40`
  (recompute + refresh_candidates) via `employer={trigger_event}` (`COUNCIL:1305`); autofill calls appoint
  13× → **~15 council recomputes + 13 candidate rebuilds at boot**, plus a redundant on_action recompute
  (`mechanics:123`). **Fix:** set a `qing_council_bulk_fill` flag during autofill to suppress the per-appoint
  office.40, do ONE recompute at the end; drop the redundant on_action recompute. Boot work ~15× → ~2×. Medium risk.
- **P4 (MEDIUM): reshuffle fires TWO office.40 recomputes** (vacate-dispatch + appoint). Suppress the
  vacate-dispatch's office.40 when called from inside appoint.
- **P5 (LOW): `QING_council_refresh_candidates` runs every pulse** (`GOVERNANCE:348`) though its header says
  "lazy, tab-open only". Drop the pulse call (tab-open + office.40 already refresh). **Low-risk.** (= §2-P5)
- P6 (info): household panel's 4 `any_character` is_shown probes → read the P1 eunuch booleans instead.

**CORRECTNESS — our recent edits verified SOUND:**
- **C1 (#6): the two candidate builders are IN SYNC** — identical limit blocks (harem exclusion,
  conflicting-role cuts, regent/emeritus); only divergence is the intentional/documented BT-12 target-holder
  filter in `_by`. No drift.
- **C3 (#5): NO `add_trait` remains on the boot autofill path** — the `wu_jinshi` grant is gone from
  `QING_office_appoint`, relocated to the day-30 runtime event. Boot appoint does only safe
  `add_character_modifier`/`add_loyal_veterans`. Our crashfix is confirmed clean.
- **C4 (#9): all figurehead derefs guarded** — `current_ruler`/`.mother`/`.spouse`/regent/heir all behind
  `exists`/`QING_dynasty_has_dowager`/alive guards. No unguarded boot-reachable figurehead read.
- **C2 (#10, minor): vacate symmetry** — chamberlain/guard ruler-buffs are strip-then-reapply each pulse, so
  a vacated holder leaves the ruler buff live up to one quarter (cosmetic lag, no permanent leak). Optional:
  add immediate strips to `QING_office_vacate`. Low priority.
- **C5 (correctness hygiene): `COUNCIL:548` reads `var:qing_corruption_level >= 45` with no `has_variable`
  guard** (every sibling guards it). Seeded at boot so effectively safe, but technically an unguarded read.
  **Fix:** add the guard. Low-risk.

**DEAD CODE:** no dead council/ministry effects (all 13 recomputes + all `QING_council_*` trace to live
callers; no unmatched `qing_office_*_holder`). D2 (verify): `QING_office_appoint_first_vacant` (`COUNCIL:1314`)
has no `= yes` caller found — likely reserved for a laureate/keju path; confirm before touching.

---

## 9. Event-throttle short-circuit ordering — RESOLVED (agent-verified)

**Verdict: the two-slot throttle is implemented CORRECTLY. No meaningful evaluate-then-discard waste.**

Every heavy court roller is gated behind the O(1) `NOT = { has_variable = qing_gc_event_slot_used }`
check **before** its expensive work runs — either wrapped at the pulse call site
(`00_monthly_country.txt:118, 127, 140, 169, 182`) or with the slot check as the first clause of
its own internal `limit` AND (`QING_tribute_schedule_missions` `se_QING_TRIBUTE.txt:73`,
`QING_tribute_default_check:425`, `QING_DECLINE_roll_reaction` `se_QING_DECLINE.txt:990`). In every
case the O(1) slot read short-circuits before the `any_character` / `any_in_list` / `random_list` /
`random_subject` scans. Once `QING_frontier_flavour_roll` claims the slot, the four later court
blocks all fall out on the cheap `has_variable` check — no heavy work leaks past a claimed slot.

- The heaviest event-selection block is `QING_frontier_flavour_roll`'s ~20-branch `random_list`
  with per-branch triggers (`war_with`, `exists=c:XXX`, date checks) at `se_QING_DECLINE.txt:1020-1220`.
  It runs first, so its slot is always free — the `random{chance=30}` + `random_list` evaluates on
  ~30% of pulses. This is *necessary* work (you must evaluate to pick a branch), not wasted-post-throttle.
- **Only optimization available (LOW priority):** collapse the five separate court-event
  `if { limit { NOT slot } random{...} }` blocks into a single `random_list` dispatch so the engine
  rolls once instead of five independent draws each re-reading the slot var. CPU saved is marginal
  (five `has_variable` reads + up to five RNG draws/pulse).

## 10. Pulse-cadence downgrades — RESOLVED (agent-verified). 3 real wins, ranked by CPU saved.

**AI-rejection confirmed clean:** the single `tag=CHI is_ai=no` gate at `00_monthly_country.txt:68-71`
wraps the entire pulse effect; no heavy sub-effect escapes it. Cost is human-CHI-only.

### Recommended downgrades

| # | Effect | Site | Now | Fix | Precision lost | CPU saved |
|---|---|---|---|---|---|---|
| **1** | `QING_sinic_pulse` STEP 1 recount | `se_QING_SINICIZATION.txt:53-89` | **Quarterly, UNCAPPED** | Wrap STEP 1 in the existing `qing_sinic_year_cd` (365d) gate that already throttles STEP 2 | None meaningful — sinicization is glacial; delta only changes on a province flip, which the annual roll already catches | **HIGHEST** — the only uncapped **triple-nested** `every_governorships > every_governorship_state > every_state_province` walk on the pulse |
| **2** | `QING_DECLINE_granary_pool` | `se_QING_DECLINE.txt:1988+` | **Quarterly, UNCAPPED** | Add `qing_granary_pool_cd days=180` (biyearly) | Granary relief cadence 90d→180d; historically fine (ever-normal granaries were seasonal) | **HIGH** — uncapped `every_country_state` food sweep w/ ~10 var writes + `add_state_food` per state |
| **3** | `QING_fgar_scan` | `se_QING_FRONTIER.txt:31-67` | **Quarterly, UNCAPPED scan** | Add `qing_fgar_scan_cd days=180` to match its already-180d downstream consequence | Garrison-on-subject-soil is slow-changing; consequence already throttled 180d | **MEDIUM** — `every_army` sweep (small pool) |

### Already fine (verified self-throttles — NO action)
`QING_sphere_pulse` (365d cooldown, `se_QING_SPHERE.txt:402`), `QING_COLON_nwcrop_diffuse`
(365d + inert pre-crop-arrival, `se_QING_COLON.txt:408`), `QING_mission_stations_pulse`
(365d + dormant pre-treaty, `se_QING_MISSIONARY_STATIONS.txt:290`), `SEPARATISM_qing_pulse`
(~3yr + double-gated), `QING_exam_schedule_triennial` (1095d).

### Must stay quarterly (player-facing / event-driving)
`QING_GOV_pulse` council+ministry recompute (feeds faction/dynasty/officer rollers + reform drift —
but see §1: the *internal* scans are the real cost, not the cadence), `QING_DECLINE_pulse` band
applies (O(1) modifier swaps gating player meters), `QING_subject_collect_tribute` (quarterly
treasury flow the player sees), `QING_gp_scan_plays` (feeds fresh GP tension consumed same-pulse).

## 11. Deleting 1815 content from the 1763 branch — DONE. Premise stale; near-zero to gain.

**Key correction:** `merge-overnight` and `1763_bookmark` are the **identical commit** (516677513);
`git diff` between them is empty. **Both** define `START_DATE = "1763.2.16"` (`00_defines.txt:3`). There
is no live 1815 start — the 1815 line survives only as authoring-comment baselines. So there is no
"delete 1815 content" operation; the 1763 rebase already happened in place.

- **The dated arcs were REBASED (+19127 days), not orphaned.** USCW (`usa_section_*`, fires ~1820-1861),
  Mexico, Japan Bakumatsu (`tag=TKG`), Opium/treaty, Self-Strengthening, Taiping, Summer Palace all fire
  at their true historical dates *inside the 1763 campaign's future*. Deleting them removes intended content.
- **Setup-object audit — the real-CPU target is already clean.** No phantom 1815 AI countries
  (ITA/GER/COL/ARG/GRE… absent from the 632 gamestate country blocks). USA/MEX/BRZ present but reworked
  to 1763 polities (USA = Thirteen Colonies, MEX = viceroyalty). No dead AI nations ticking forever.
- **No ungated MTTH anywhere** in the dated arcs — all `is_triggered_only` + tag-gated + cooldowns.
- Only defensible deletion on merit: the **Napoleon-in-China arc** (`qing_napoleon_events.txt`) uses small
  offsets (`days={120 300}`) so it fires ~1763 — anachronistic — but it's `is_triggered_only tag=CHI`
  once-only, so **zero runtime CPU**; a lore/plausibility call, not a perf one.
- **Bottom line: deleting 1815 content saves ~zero runtime CPU and little else** (class-(a) parse/memory/
  save-size only, tiny). The runtime cost is elsewhere (below).

**IMPORTANT — pre-existing `PERF_AUDIT.md` discovered:** it states the **quarterly economy/trade sim is
95%+ of the mod's added load** (`quarterly_trade_pulse` / `oa_wealth_changes.txt:138`, O(countries ×
governorships × goods × 5 passes × 8 categories)) — start-date-agnostic, and NOT touched by any Qing-suite
change. This is task #19 on our list (the deferred trade-engine flood) and is almost certainly the single
biggest runtime cost in the whole mod, dwarfing the Qing council scans. Flagged for the fixes list as a
separate track. (This audit's Qing-suite findings remain the second cost center + all the correctness/dead-code wins.)

---

## SCOPING RULES (user-directed)

1. **Upstream findings are HIGH-RISK by default** — the sobisonator trade/economy sim
   (`oa_wealth_changes`, `se_GLOBALTRADE_split`, `se_GOODS`, `TRADE_svalues`, `DEMAND_svalues`,
   Industry-A2) is NOT to be edited in the low/medium implementation batch. Flag only.
2. **Focus on changes WE added** — the Qing player-experience suite (`se_QING_*`, our scripted_guis,
   our events/GUI). This is where the safe, high-value optimizations live.

## 12. Precision-for-performance (accept minor inaccuracy for major speedup) — DONE

Ranked by gain ÷ precision-lost. All are OUR (Qing-suite) code, all feed player-visible values that are
**consumed only as coarse bands / thresholds**, so the accuracy budget is generous (quarterly, one player).

- **#1 (BIGGEST — zero precision lost): collapse the 6 global `every_character` court scans into ONE
  classified sweep.** Same as §1/§2-P1. ~60,000 world-char visits/pulse → ~10,000 (6× on the filter,
  6 body-passes → 1). Pure structural merge, identical outputs.
- **#3: sinicization count walk → cache with ~annual staleness** (`se_QING_SINICIZATION.txt:53-88`).
  Consumed only as a 3-way band (up/steady/down) in the report; culture flips are glacial. Precedent
  already in-codebase: `QING_DECLINE_scan_ethnic_target` (`se_QING_DECLINE.txt:446`) is annually throttled.
  ~4× fewer full-province walks. **Cross-confirmed by 3 agents — top cadence win.**
- **#6: granary ever-normal pool `every_country_state` food sweep → ~180d cadence or near-empty/near-max
  sampling** (`se_QING_DECLINE.txt:2009-2102`). Stock consumed only as bands; code already tolerates a
  1-quarter lag. ~2× on the largest DECLINE state sweep.
- **#7: ethnic-tension does FOUR `every_owned_province` passes/pulse** (`se_QING_ETHNIC_TENSION.txt:50-101`)
  — merge passes 2-4 (snowball/erupt/clear) into pass 1 based on the just-written value; optional 2× cadence.
  4 province sweeps → 1. Tension consumed via thresholds; eruptions are rare set-pieces.
- **#4: council effectiveness TARGET re-summed from scratch each pulse** (`se_QING_COUNCIL.txt:363-402`)
  though it only drifts ±3/pulse and is banded — recompute the target only on appoint/vacate/death (already
  wired) and let the pulse do just the cheap ±3 drift + band. Lag ≤1 quarter, already masked by the smoothing.
- **#5: Manchu/Han/Other split reclassified each pulse** (`se_QING_COUNCIL.txt:193-200`) though consumed
  only as `>=1` threshold gates — maintain ±1 incrementally in appoint/vacate. Folds into #1's sweep.
- **#2: redundant precision** — Zongli avg-charisma & officer avg-martial are accumulated per member each
  pulse but the perf term uses only the COUNT (`se_QING_MINISTRY.txt:429-469`). Drop the unused sum.
- **#8: sphere 4× neighbor walk → 1** (already yearly-throttled, low priority; = §3-P2).

**Explicitly NOT worth touching (verified):** `QING_council_refresh_candidates` (top-N capped, lazy),
the already-annual target scans, `QING_amban_evaluate`/tribute (single non-nested `every_subject`).

---

## Relationship to the pre-existing `PERF_AUDIT.md` (2026-07-05)

That earlier audit found the **quarterly trade sim = 95%+ of load** (structurally load-bearing per #77;
rewrite ruled out as #76-class regression risk) and classified **Qing mechanics as "negligible, O(1)
counter reads"** (its §5). **This audit CORRECTS that Qing classification as now-stale:** since July the
concrete-object layer (ministry rosters, officer corps, granary/works province sweeps) has accreted into
**~12 unbounded iterators per quarterly pulse** (§1/§2/§3). It's still CHI-human-only and quarterly, so it
remains the *second* cost center behind trade — but it is no longer "O(1) negligible," and unlike the trade
sim it IS safely optimizable (the redundancy is clear). The old audit's own open items (P1 Industry-A2
43-traversal collapse, P2 infra-svalue caching) remain valid and untouched by this pass.

---

# HIGH-VALUE FIXES — synthesized & triaged by risk

Risk rubric: **LOW** = additive throttle/guard, dead-code delete w/ 0 callers; no behaviour change beyond
frequency/safety. **MEDIUM** = merge redundant iterator passes / restructure a recompute (same output,
verifiable). **HIGH (defer)** = gameplay-balance change, boot-construction/trait territory, invasive
council-recompute restructure, or **any upstream (sobisonator) file**.

### LOW-RISK (implement now — OUR code)
| ID | Fix | File | Class |
|----|-----|------|-------|
| L1 | Throttle `QING_sinic_pulse` STEP 1 recount to annual (gate on existing `qing_sinic_year_cd`) | se_QING_SINICIZATION.txt:53 | PERF — biggest cadence win (3-agent confirmed) |
| L2 | Drop `QING_council_refresh_candidates` from the quarterly pulse (lazy + office.40 already refresh) | se_QING_GOVERNANCE.txt:348 | PERF |
| L3 | `has_variable = qing_corruption_level` guard | se_QING_COUNCIL.txt:547 | CORRECTNESS |
| L4 | Guard `current_ruler` context-switch with `exists` | se_QING_DIPLO.txt:411 | CORRECTNESS (crash-class) |
| L5 | `QING_gp_init` at top of `QING_tribute_gp_interference_check` | se_QING_TRIBUTE.txt:350 | CORRECTNESS |
| L6 | Guard `add_trait = ambitious` with `NOT = { has_trait }` | se_QING_HOUSEHOLD.txt:251 | CORRECTNESS |
| L7 | `has_variable` guard on `qing_han_provincial_power` is_shown read | QING_mechanics_actions.txt:166 | CORRECTNESS |
| L8 | `has_variable` guard on `qing_canton_purse_share` is_valid reads | QING_mechanics_actions.txt:596,603,610 | CORRECTNESS |
| L9 | `remove_variable = qing_opium_net_flow_tmp` (save-bloat scratch leak) | se_QING_OPIUM.txt:~207 | CORRECTNESS |
| L10 | Delete dead `QING_harem_rank_cap` (0 callers, var never read) | se_QING_HAREM.txt:104 | DEAD CODE |
| L11 | `QING_students_graduate` — pass magnitude as `$mag$` param | se_QING_STUDENTS.txt:119 | CORRECTNESS |
| L12 | Drop internal roster-recompute in harem/SS/US draw effects when reached from pulse | HAREM/SS/US | PERF |

### MEDIUM-RISK (implement now — OUR code, verify output unchanged)
| ID | Fix | File | Class |
|----|-----|------|-------|
| M1 | Merge SUBPOSTS strip+recount into ONE `every_character` pass (6 scans → 3) | se_QING_SUBPOSTS.txt:107,117 | PERF |
| M2 | Cooldown on `QING_DECLINE_granary_pool` `every_country_state` sweep (~180d) | se_QING_DECLINE.txt:1988 | PERF |
| M3 | Biyearly scan cooldown on `QING_fgar_scan` (match its 180d downstream) | se_QING_FRONTIER.txt:31 | PERF |
| M4 | Merge ethnic-tension 4 `every_owned_province` passes → 1 | se_QING_ETHNIC_TENSION.txt:50 | PERF |

### HIGH-RISK (DEFER for later review)
| ID | Fix | Why deferred |
|----|-----|--------------|
| H1 | Shared court character-pass: ~9-10 `every_character` walks → 1 (§1/§8-P1, §12-#1) | Biggest CPU win, but invasive & touches the council-recompute path that just had a boot crash. Own pass + boot test. |
| H2 | Boot recompute storm: suppress per-appoint `office.40` during autofill (§8-P3/P4) | Touches boot construction ordering — crash-sensitive. |
| H3 | War-ministry 4 army-walks → 2 + council reads war roster (§8-P2) | Cross-effect data-flow change. |
| H4 | Council eff-target / Manchu-Han split → recompute only on appoint/vacate (§12-#4/#5) | Balance-sensitive recompute restructure. |
| H5 | Move study/exam boot `add_trait` into follow-up scope (§4-C1) | Boot-construction trait territory (safe today, but the crash class). |
| H6 | `QING_justice_pulse` dead — wire or delete (§5-D1) | Gameplay decision (has a live `add_stability`). |
| H7 | `qing_sect_pressure` one-way ratchet (§5-C2) | Balance/design confirmation needed. |
| H8 | Cache per-frame is_shown iterators in works/household panels (§6 Cat 1) | GUI restructure; medium-high, needs in-game verify. |
| H9 | **ALL upstream (sobisonator):** trade sim, `decentralize_realm_button`, hoa/mercenary/release-subject boot-inline `create_character`, `republic_party_button` dangling, WAR/subject dead guis | User-directed: upstream = high-risk by default. Flag only. |

### DEAD-CODE (parse/memory only — human-check ambiguous)
- 3 dead events (§7): `qing_censorate.5`, `qing_justice.5` (superseded — safe delete), `qing_war.3` (wire-or-delete).
- ~11 `*_open_panel_button` + ~23 `*_close_panel` + `qing_gov_office_appoint_*` scripted_guis (§6) — check before bulk delete.

---

# IMPLEMENTED (2026-07-18)

Per user instruction: implement all LOW/MEDIUM-risk fixes, defer HIGH-risk. All edits are OUR (Qing-suite)
code; brace-balance verified after each. **A mandatory boot-crash review + boot test is still owed before
these are declared safe** (they touch the quarterly pulse + a boot-init effect).

## Batch 1 — LOW-risk (DONE)
- **L1 DONE** — `se_QING_SINICIZATION.txt` — wrapped STEP 1 recount in `if = { limit = { NOT = { has_variable
  = qing_sinic_year_cd } } … }` so the triple-nested province walk runs annually (with STEP 2) instead of
  every quarter. First-touch baseline seed + `QING_sinic_recompute_delta` remain every-pulse. Braces 65/65 OK,
  def 52/52 OK. Precision: count/delta may lag ≤1yr (band-invisible). **~4× fewer full province walks.**
- **L3 DONE** — `se_QING_COUNCIL.txt:546` — added `has_variable = qing_corruption_level` before the `>= 45` read.
- **L4 DONE** — `se_QING_DIPLO.txt:411` — wrapped `current_ruler = { add_popularity = -10 }` in `if = { limit = { exists = current_ruler } … }`.
- **L5 DONE** — `se_QING_TRIBUTE.txt:350` — added idempotent `QING_gp_init = yes` at top of `QING_tribute_gp_interference_check` before its `var:qing_gp_tension_*` limit reads.
- **L6 DONE** — `se_QING_HOUSEHOLD.txt:246` — added `NOT = { has_trait = ambitious }` to the eunuch-faction-leader `ordered_character` limit.
- **L10 DONE** — `se_QING_HAREM.txt:104` — deleted dead `QING_harem_rank_cap` (0 callers, var never read); replaced with a note.
- **L2 DONE** — `se_QING_GOVERNANCE.txt:348` — commented out `QING_council_refresh_candidates = yes` from `QING_GOV_pulse`; the candidate list is already rebuilt on tab-open (`qing_gov_council_refresh_candidates`, QING_governance_actions.txt:370) and via `qing_office.40` — so the every-pulse rebuild was redundant. **Removes a whole-court candidate rescan every pulse.**
- **L7 DONE** — `QING_mechanics_actions.txt:166` — added `has_variable = qing_han_provincial_power` guard before the `>= 20` read in `is_shown` (prevents a per-frame read of an unset var).
- **L8 DONE** — `QING_mechanics_actions.txt:598/605/612` — each Canton-share `is_valid` now `OR = { NOT = { has_variable = qing_canton_purse_share }  NOT = { var:… = N } }` so an unset var doesn't misread on first open (N=0/50/100).
- **L9 DONE** — `se_QING_OPIUM.txt:213` — added `remove_variable = qing_opium_net_flow_tmp` next to its two sibling removes (was leaked into saves).
- **L11 DONE** — `se_QING_STUDENTS.txt:110` — de-fragilized `QING_students_graduate`: it now DERIVES its magnitude locally from `$amount$` (`set_variable = $amount$` then `multiply = -1`) instead of reading the caller-primed `qing_students_graduate_mag`. Removed the now-dead `set_variable` in the sole caller (`QING_students_pulse:278`). Correctness-hardening (a future direct caller can no longer read a stale/unset mag); perf-neutral. Braces 136/136 OK.
- **L12 DEFERRED to review** — the draw/favour recompute-dropping (harem/SS/US) turned out to be MEDIUM not LOW: those effects are called from BOTH the pulse (which recomputes) and event/button trampolines (where the internal recompute IS needed). Dropping it needs flag-threading = out of the clean-low batch. Logged for later.

## Batch 2 — MEDIUM-risk (DONE — OUR code)
- **M1 DONE** — `se_QING_SUBPOSTS.txt:107` — merged the two global `every_character` passes in `QING_subpost_staff_corps` (strip-then-recount) into ONE pass: per marked member, strip-and-skip if disqualified (commander/governor/office-held), else count. Behaviour-equivalent (the old strip removed the marker from every office-holder before the recount, making the recount's `NOT=qing_office_held` guard redundant). **Halves the global character-iterator cost of every corps staffing** (runs at boot ×3 + on each ministry-panel refresh). Braces 66/66 OK.
- **M2 DONE** — `se_QING_DECLINE.txt:1988` — gated the whole-CHI `every_country_state` grain sweep in `QING_DECLINE_granary_pool` to a ~180-day cadence (self-throttle `qing_granary_pool_cd`). Was every DECLINE pulse (~90d). The derived `qing_granary_stock`/`_capacity` persist between runs so every consumer keeps reading last-computed values. **Halves the granary sweep frequency.** Precision: relief timing lags ≤½yr. Braces 1155/1155 OK.
- **M3 DONE** — `se_QING_FRONTIER.txt:31` — gated the `every_army` walk in `QING_fgar_scan` to a ~180-day cadence (`qing_fgar_scan_cd`). The per-garrison consequence is ALREADY self-throttled per subject to 180d, so more frequent scans walked every owned army only to no-op. Zero behavioural change. Braces 47/47 OK.
- **M4 DONE (partial vs scope)** — `se_QING_ETHNIC_TENSION.txt:74` — merged STEP 3 (erupt, tension≥80) + STEP 4 (clear cooldown, tension<70) into ONE `every_owned_province` walk (disjoint sets → if/else_if). **AUDIT CORRECTION:** the "4→1" scope was over-optimistic — STEP 1 (local drift) and STEP 2 (snowball, which reads a province's tension then writes its NEIGHBOURS') require a barrier between them and before STEP 3, so they cannot join the merge. Only the disjoint 3+4 are safe. **Saves 1 of 4 global province walks per pulse**, zero behavioural change. Braces 134/134 OK.

## Batch 3 — HIGH-risk: DEFERRED (per user)
H1–H9 + ALL upstream (sobisonator) findings incl. the trade sim are left for later review per the user's "treat upstream as high-risk by default" + "defer the high-risk ones."

## Verification owed (before commit)
- Independent boot-crash review of the batch (standing rule — pulse + boot-init touched).
- Brace/UTF-8 check across all edited files. — **brace check DONE (all balanced); UTF-8 check pending.**
- Commit as freekumquats; do NOT push (leave for user boot test).
