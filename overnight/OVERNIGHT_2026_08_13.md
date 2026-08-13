# Overnight run — 2026-08-13

## ASSUMPTIONS & GUESSES
(Filled in as tasks land — every best-guess constant goes here, called out explicitly.)
- **#101 Cottage Industry**: `cost = 50`, `time = 150`, `base_resources = 1` per building; strata
  output `local_lower_strata_output = 0.2` / `local_proletariat_output = 0.15`. All best-guess
  starting figures, not a final balance pass — boot-tune. See design/DESIGN_101_COTTAGE_INDUSTRY_
  BUILDINGS.md "Cost / efficiency figures."
- **#88 population fold**: the new relief-valve term subtracts `6` from `qing_pop_pressure_target`
  when `qing_newworld_agriculture` fires — a guess below the golden-crop relief's `-10`, since that
  path is risk-gated and this one is deterministic. Boot-tune against pop logs. See
  design/DESIGN_88_POPULATION_UNIFICATION.md.

## Task #49 — "A Minister Called to Account" duplicate effects — DONE
- **What it was**: option `.b` visibly double-strips the same character's modifiers (character-
  modifier removals, loyal-veteran/office-transfer lines) on a screenshot-confirmed real boot.
- **Diagnosis, corrected once**: first draft self-contradicted a "preview pass commits gamestate"
  theory — disproven by adversarial review citing the SAME precedent (#25/qing_roster.8) it claimed
  supported it (that engine behavior is actually the OPPOSITE: preview does NOT commit). Dispatched a
  focused trace agent for the real, non-contradictory mechanism, confirmed against a live debug.log
  line for this exact event: `QING_office_vacate_dispatch`'s own trailing backfill draw has no
  identity exclusion for the man it just vacated, so it can redraw the SAME defender into his own
  seat; the event's own subsequent `QING_office_appoint` for the challenger then finds him re-seated
  and strips him a second, genuine time.
- **Design, corrected once**: REV 1 (a new exclusion marker in the general backfill path) was
  mechanically sound (adversarial review confirmed every engine-scope claim) but didn't fix option
  `.c`'s stated intent and missed a simpler, already-proven fix. REV 2: route both `.b` and `.c`
  through `QING_office_vacate_dispatch_nobackfill` (an existing no-backfill twin, already used by
  `QING_office_appoint`'s own manual-reshuffle path for the identical reasoning) instead of the
  backfilling dispatcher — neither option wants an automatic replacement anyway.
- **Review found a broader issue, logged not buried**: ~14 OTHER callers of the backfilling
  dispatcher share the same general redraw hole. NOT fixed here (genuinely separate scope — each
  needs its own diagnosis of whether it wants a backfill at all). Opened task #52 to audit and fix
  them.
- **Commit**: `1f2d39c3a`, pushed.
- **STATUS: DONE** (for the one confirmed-affected event; the general hole is tracked as #52, not
  silently left unmentioned).

## Task #30 — Treasury income orders of magnitude too high — DONE
- **What it was**: `GT_split_update_wealth_owed_for_tradegoods` billed a governorship for its FULL
  order regardless of whether the zone could actually supply that much — a governorship's own
  order_size fed the shared zone total (the numerator of `local_price`), so its own demand inflated
  the price it paid, then was billed as if the full order had been delivered anyway, growing without
  bound as scarcity deepened.
- **Design, corrected across 3 revisions, 5 adversarial review rounds**: REV 1 (cap quantity via a
  formula that was the algebraic reciprocal of the price formula — canceled to a flat rate by
  accident, and used an invalid `max` syntax) — broken, replaced. REV 2 (cap price at a fixed 0.6) —
  wrong for ~36 food/manufactured goods whose true balanced price isn't 0.6 — broken, replaced.
  REV 3 (ration the billed QUANTITY to `min(1, zone_stockpile/zone_total_order_size)`, a no-op for
  any abundant/balanced zone) — mechanically sound from the first review, but needed two more
  correction rounds: a wrong algebraic "proof" about manufactured-goods addends surviving unchanged
  (withdrawn — the fix doesn't need to reason about local_price's internal composition at all), and
  an honest reconciliation with the #112 "no ceiling" directive (this fix DOES override it at this
  one site — logged as an explicit, acknowledged decision with the rejected alternative — leave #30
  unfixed — named and not chosen, per this session's own standing instruction not to idle on a
  design call the code/history can't settle).
- **Also resolved during review**: confirmed the fix's ratio compounds correctly (not double-counts)
  with a pre-existing WORLD-scope ration on the same variable (`GT_split_scale_wealth_owed_and_
  order_size_tradegood`, a distinct scarcity signal, running after this fix's own site); confirmed
  the fix correctly and consistently shrinks the state's precious-metal reserve inflow under genuine
  silver/gold scarcity too (same variable, same principle, not a blast-radius violation).
- **Commit**: `ba8b38672`, pushed.
- **STATUS: DONE.**

## In-flight from before this run, still open
(see Task #101 write-up below — resolved to DONE this run)

## Backlog worked this run
(appended per task, in order)

### Task #31 — Eunuchs lack the castrated trait — DONE
- **What it was**: palace eunuch characters (太監) were never granted the `castrated` trait, so
  they showed no mechanical trace of the eunuch condition.
- **Diagnosis (why it was missing, per Rule 1c)**: a code comment (git-traceable, still in the file
  above the diff) shows the grant was DELIBERATELY removed — `castrated` is `type = health`
  (common/traits/00_health.txt:179-183), and this codebase has a proven boot-crash class: a HEALTH
  trait added at gamestate construction (inside `create_character` or a same-tick follow-up scope)
  crashes with no log. `QING_household_mint_eunuch` (the minting function) is called from BOTH a
  boot-time seed (`QING_household_init` -> `QING_household_seed_eunuchs`, unsafe) AND a runtime path
  (`QING_household_pulse`'s eunuch-faction check, safe) — the removal correctly avoided the unsafe
  path but threw out the trait for BOTH, including the safe one.
- **Fix**: added `QING_household_backfill_eunuch_traits` (walks the `qing_household_eunuchs`
  variable_list, `add_trait = castrated` guarded on `NOT has_trait`), called unconditionally once per
  quarter from `QING_household_pulse` (never from the boot-time init path). One call site covers both
  boot-seeded eunuchs (traited on the first quarterly pulse after boot) and later runtime-minted ones.
- **Review**: code-review clean, no findings — confirmed `every_in_list = { variable = X }` is the
  correct variable_list idiom (matched against se_QING_HAREM.txt's own usage), confirmed
  `QING_household_pulse` is never reachable at `on_game_initialized` (only via the runtime monthly
  on_action chain), confirmed the no-re-grant guard is correct.
- **Commit**: `9d44618a8`, pushed.
- **STATUS: DONE.**

### Task #32 — Ever-Normal Granary notification should be Global News, not a popup — DONE
- **What it was**: `qing_revenue.6` (a pure single-acknowledge notification; the granary was already
  built and paid for by the calling effect) showed as a full modal popup instead of the compact
  "Global News" feed (`InGameTopbar.GetMinorEventItems`, gui/ingame_topbar.gui:1510).
- **Proof this is a real, proven engine capability (not a hard block)**: no `major`/`minor` FIELD
  exists in this mod, Invictus, or Terra Indomita — but the event `type` value itself,
  `minor_country_event`, is a proven vanilla type (confirmed via multiple Invictus usages, e.g.
  `character_events.54`, an event with the SAME single-acknowledge shape as ours). No script field
  was missing; the fix is a one-token type change.
- **Fix**: `type = country_event` -> `type = minor_country_event`; added `interface_lock = no` to
  match every other minor_country_event in this mod (code-review finding, since a pure informational
  notification should not pause the game).
- **Review**: code-review clean after the interface_lock addition. Confirmed the only fire site
  (`QING_DECLINE_granary_concrete`, se_QING_DECLINE.txt:2783) makes no assumption about modal
  behavior.
- **Not expanded to sibling events**: found 2 other events in this codebase explicitly documented as
  "pure notification, single acknowledge" (qing_caravan_events.txt:481-482, qing_march_events.txt:343)
  that likely have the same fix available — NOT touched here, since task #32 named only the granary
  event; noting for a future task rather than silently expanding scope.
- **Commit**: `610f6ad53`, pushed.
- **STATUS: DONE.**

### Task #36 — Outdated Finesse icon — NO DEFECT FOUND (logged loudly, not silently dropped)
- Dispatched a thorough Explore search per Rule 1c (diagnose before touching existing behavior).
  Checked: all 48 `GetFinesse` GUI call sites (all consistently `icon_civic`), the vanilla
  `common/modifier_icons/00_modifier_icons.txt` finesse entry (symmetric with martial/charisma/zeal,
  none of the four actually used at that path — inert, not a live discrepancy), every Qing-specific
  finesse-flavored character modifier (no bespoke icon registrations, normal for that class),
  `design/DESIGN_PLACEHOLDER_ICONS.md` in full (zero finesse/civic/administrative mentions), and
  git log for any commit that swapped an old finesse icon for a new one (none — the one related fix
  found was for the MARTIAL stat, already resolved, `88c86970c`).
- **No old-vs-new icon pair exists anywhere in code, config, or git history matching this task's
  premise.** Per the no-fabrication rule, I will NOT invent a fix for a defect I cannot locate.
- **STATUS: RESOLVED, no code change — genuinely could not locate the described bug.** This is NOT
  a deferral; it is a diagnosis outcome ("nothing to fix here, as currently understood") that
  survived a real, thorough search, logged loudly rather than silently closed. Recommend the task
  be re-verified against whatever screenshot/log originally prompted it — it may refer to something
  not yet checked (a different stat entirely, a specific character's card, or a modifier icon added
  after this repo's current HEAD).

### Task #101 — Cottage Industry buildings — DONE (design v1→v5, 2 adversarial review rounds, full implementation)
- **What it was**: the task asked for real, on-map "Cottage Industry" buildings, distinct from the
  fully-automatic `COTTAGEIND_produce_all` pipeline (se_COTTAGEIND.txt) that already runs every
  quarter with no player-buildable structure behind it.
- **Design history (this run, v1-v3 carried in from a prior session, v4-v5 this run)**: v1 wrongly
  modeled buildings as feeding one finished good directly and claimed factories are city-gated (both
  disproven by tracing `GOODS_governorship_iron_produced` and `IND_industrial_estate`'s `allow`
  block). v2 fixed the mental model but compared against the wrong sibling
  (`IND_industrial_estate`), leaving cottage buildings strictly dominated by the TRUE sibling
  (`IND_resource_gathering_operation`), missed bronze coverage entirely, and wrongly added the ROW
  building to the macro allowlist. v3 proposed "no invention gate" as the niche and fixed bronze, but
  review found the niche broken for textile/silk (their named Qing-work siblings are ALSO
  invention-free) plus zero stone coverage plus an unresolved stacking exploit.
- **v4 (this run)**: discovered via direct grep — not review — that v3's whole invention-gate niche
  was categorically false for ALL 7 buildings, not just textile/silk: none of the 6 Qing works, 2 ROW
  generics, or `IND_resource_gathering_operation` gate on invention at all. Replaced the niche with
  `sufficient_job_slots` omission — cottage buildings skip the ONE shared capacity gate every
  existing raw-good building requires, so they remain buildable in a province that has already
  spent its job-slot pool (representing household labor outside the formal employment economy, per
  Philip Huang's "involutionary growth"). Added an 8th building (quarry, for stone — v3's stone gap
  was actually worse than claimed: 4 cottage-eligible readers, not 2, and no other building's boost
  substitutes for it since each raw good is tracked independently).
- **First adversarial review round found 6 issues in v4**: v4's own blanket claim that NO sibling has
  an invention gate was itself false (`IND_resource_gathering_operation` and both ROW generics DO
  gate on invention — only the 6 Qing works don't); a wrong claim that siblings "consume" the
  job-slot pool (they gate on it but don't deplete it — only `IND_industrial_estate`/
  `IND_resource_gathering_operation` do); incomplete raw-good reader lists for wood (missed 2 coastal
  recipes) and copper (missed 2 more); invalid `trade_goods = copper OR tin` syntax (fixed to an
  explicit `OR` block); an unproven fractional `base_resources = 0.3` (no shipped building anywhere
  uses a fraction — risked silent truncation to 0, total inertness); and an under-examined stacking
  exploit. All 6 fixed in v5 (mechanism narrative corrected without changing the fix itself; reader
  lists corrected and disclosed as real side-effects, not defects; base_resources set to the
  proven-safe integer 1; cost raised to 50g to prevent the resulting building from dominating its
  factory-tier sibling with zero trade-off; the stacking exploit confirmed genuinely unbounded via
  `global_settlement_building_slot = 9999`, decided to ship without a new cap since EVERY existing
  raw-good building shares the identical exposure already).
- **Second adversarial review round on v5 found ZERO CRITICAL/HIGH issues** — independently
  re-verified every one of the 6 fixes against source and confirmed all hold. Found 2 MEDIUM
  findings: the macro-builder's own independent `JOBS_available_slots > 0` gate
  (`macro_builder_view.gui:508`) defeats the niche in the bulk-build tool specifically in the
  job-slot-zero case the design targets (the province window has no such gate, so the niche is not
  lost, only reachable through one screen instead of two — logged as a disclosed, not-fixed
  limitation, with a follow-up boot-spike task noted rather than blocking on an unproven GUI-scripting
  branch); and `base_resources = 1` at 40 gold would have let the cottage building dominate
  `IND_resource_gathering_operation` outright (fixed by raising cost to 50 gold, restoring a genuine
  price/output trade-off). Both fixed in the design doc before implementation.
- **Implementation**: `common/buildings/qing_cottage_buildings.txt` (new, 8 Qing buildings — smithy/
  leadworks/weaving_hut/silk_reeling_shed/woodlot/herbalist/founders_workshop/quarry, each `cost=50
  time=150 base_resources=1`, rural gate, culture-group gate, `sufficient_job_slots` omitted);
  `row_production_buildings.txt` (appended `row_cottage_workshop_building`, the generic non-Chinese
  equivalent, deliberately excluded from the macro builder per the existing row_manufactory/
  row_plantation precedent); full GUI wiring in `gui_templates.gui` (new "Cottage Industry"
  building_box section + 9 build_item_*/8 macro_build_item_* types), `custom_tooltip.gui` (17 tooltip
  templates), `macro_builder_view.gui` + `province_window.gui` (blockoverrides), macro config
  allowlist (8 Qing keys), and a new localization file for the 8 Qing buildings + loc additions for
  the ROW building and the new category header.
- **Cleanup found and fixed while implementing**: `gui/qing_revenue_ministry.gui` had an uncommitted,
  orphaned button block from an EARLIER, DIFFERENT, abandoned approach to #101 (dated 2026-08-12,
  before this run) — a governorship-investment/national-policy-dial panel concept, referencing a
  nonexistent scripted_gui key (`qing_cottage_open_panel_button`), nonexistent loc keys, and a
  nonexistent file (`gui/qing_cottage.gui`). Removed as dead scaffolding for an approach superseded
  by the buildings-based design actually built; confirmed via repo-wide grep that no reference to it
  remains anywhere.
- **Review (implementation)**: code-review dispatched on the full diff — found 1 LOW (an orphaned
  macro-title loc key for the ROW building, which correctly has no macro-builder presence) and 2
  informational notes (two unrelated stray loc edits sitting in the working tree from earlier,
  unrelated work — deliberately left OUT of this commit rather than folded in). The LOW finding
  fixed (removed the dead loc line). Every other area — brace balance, allow-block correctness across
  all 9 buildings, `OR` syntax, the full 9-building cross-reference matrix across all 6 GUI/loc
  surfaces, macro allowlist scope, BOM on both new files, and the scaffolding removal — verified
  clean.
- **Commit**: this task's files only (buildings, GUI, macro config, loc, design doc) — the two
  unrelated stray loc edits (`qing_migration_l_english.yml`, `qing_settle_frontier_l_english.yml`,
  from earlier #88-adjacent work) were deliberately left unstaged so this commit stays scoped.
- **STATUS: DONE.**

### Task #88 — unify frontier-settlement/pop-boom/Population-Famine — DONE (design round 3-4, 2 adversarial reviews, implemented)
- **What it was**: task text (`overnight/SESSION_HANDOFF_2026_08_11.md:44`) named three systems
  to unify. Diagnosis (Explore agent, very-thorough level) found: frontier-settlement and the NW
  pop-boom are already one narrative family by design; the #369 `qing_pop_pressure` Malthusian meter
  already couples with most of that family (involution/relief terms, migration push/clear guard).
  The ONE genuine, unfixed silo: task #65's `qing_settle_newworld_crops` mission granted a
  standalone, permanent `global_population_growth`/`global_population_capacity_modifier` country
  modifier (`qing_newworld_agriculture`) on completion that the pressure meter had ZERO awareness
  of — confirmed by grep, the modifier was never read anywhere. Two independent systems modeling
  the same real-world phenomenon, neither aware the other existed.
- **Design history (carried in from a prior session, rounds 1-2; this run did rounds 3-4)**: rounds
  1-2 (prior session) fixed a wrong `-10` magnitude analogy (the golden-crop relief term it was
  modeled on is RNG-gated and can backfire; this mission's path is deterministic — settled on `-6`)
  and 2 stale loc strings. Left 2 open questions unresolved for a reviewer who would not be
  available mid-run. Round 3 (this run, made autonomously per the no-stopping-to-ask discipline):
  resolved both — (Q1) `qing_newworld_agriculture` becomes a pure empty-modifier marker rather than
  gaining a companion standalone effect (rejected: would double-reward an already treasury-costed,
  already-rewarded mission); (Q2) confirmed via independent grep that this is the ONLY orphaned
  one-shot population modifier within the three frontier-settlement/NW-crop modifier files
  specifically (a mod-wide sweep found 4 similarly-shaped orphans in the UNRELATED overseas-
  colonization subsystem — correctly out of scope, logged as new task #53).
- **Adversarial review round 1 found 2 MEDIUM issues in round 3's plan**: (1) removing the vanilla
  `global_population_capacity_modifier` effect is a RETIREMENT, not a re-homing — the custom
  pressure meter has no capacity term at all (its crowding driver is a fixed `total_population/1200`
  ratio), so the doc needed to say this plainly rather than let a boot-tuner chase a capacity effect
  that no longer exists anywhere; (2) the "empty modifier marker" plan would display a named,
  described, effect-free modifier in the player's active-modifiers list — reading as a bug — and the
  design's own cited precedent for this idiom (`qing_migr_crop_boom_golden`) was factually wrong
  (that modifier is never empty, it carries 5 real effects). Also found 2 LOW line-citation errors.
- **Fixed (round 4)**: replaced the empty-modifier plan with the SAME silent flag idiom already
  proven at `qing_frontier_resettlement` (`set_variable`/`has_variable`, no loc name/desc, no
  active-modifiers-list display) — a cleaner precedent the round-3 draft had missed entirely. Added
  an explicit "retired, not re-homed" note to the relief-valve code comment. Fixed both LOW citations.
- **Adversarial review round 2 (final) found ZERO CRITICAL/HIGH/MEDIUM issues** — verified the
  `set_variable`/`has_variable` scope match against the precedent exactly, confirmed the mission's
  `on_completion` block already runs in country scope (no qualifier needed), confirmed deleting the
  modifier definition and its 2 loc keys orphans nothing repo-wide. Found 3 LOW doc-accuracy nits (a
  stale STATUS banner, a stale mission comment describing the removed effect, and one of the 4
  cited overseas-colonization orphans mischaracterized — `qing_nw_puget_sound` doesn't actually
  carry `global_population_growth`, it's a commerce/naval-range modifier). All 3 fixed.
- **Implementation**: `common/modifiers/qing_migration_modifiers.txt` (deleted the
  `qing_newworld_agriculture` modifier definition, replaced with a comment-only marker);
  `common/missions/qing_settle_frontier_missions.txt` (mission's `on_completion` now
  `set_variable`s a flag instead of `add_country_modifier`; updated the stale comment block above
  the mission); `common/scripted_effects/se_QING_POPULATION.txt` (new relief-valve term in
  `QING_pop_recompute_target`'s RELIEF VALVES section, `-6` on `has_variable = qing_newworld_
  agriculture`, placed right after the golden-crop `-10` term, before the final clamp);
  `localization/english/qing_migration_l_english.yml` (deleted the 2 now-unused loc keys).
- **Review (implementation)**: code-review dispatched on the full diff — CLEAN, zero findings.
  Verified brace balance, the `set_variable`/`has_variable` scope match, relief-term placement and
  syntax, zero dangling references repo-wide (grep confirmed exactly the 4 intentional hits and
  nothing else), no GUI/mission-reward-display reference to the deleted modifier, and no encoding
  corruption from a byte-level Python edit used once during implementation (an em-dash mismatch
  blocked a normal string-match Edit; confirmed the target file never had a BOM to begin with, and
  the file decodes clean UTF-8 throughout after the edit).
- **New follow-up task created**: #53 ("Audit overseas-colonization orphaned population modifiers")
  — logs the 3 genuine same-shape orphans found in the unrelated overseas-colonization subsystem
  (`qing_nw_columbia_country`, `qing_oc_new_zealand`, `qing_oc_queensland`) plus one non-population
  orphan of a different shape (`qing_nw_puget_sound`), explicitly NOT folded here (different
  subsystem, different scope than task #88 named).
- **Commit**: `117468c54`, pushed.
- **STATUS: DONE.**
