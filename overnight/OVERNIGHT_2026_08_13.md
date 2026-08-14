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
- **#51 customs revenue rollup**: `qing_customs_income_last` publishes the PRE-currency-conversion
  `thousands` input (~0-20/quarter), not the real post-peg treasury delta (~1000x larger) — a
  deliberate scale choice to keep it comparable to the other 3 streams in the sum it joins, not a
  literal ledger reconciliation. Boot-tune against econ logs; if customs visibly dominates or is
  inert relative to salt/canton/caravan, retune the scale here, not the shared /4 divisor. See
  design/DESIGN_51_CUSTOMS_REVENUE_PERF_ROLLUP.md.
- **#56 Indo-China rulers**: CPK (Sayakumane), LPR (Sotika-Kuomane), VIN (Ong Long), PHN (Chao Ong Lo)
  all get a placeholder `birth_date` of c.1720-1725 — sources confirm each reigned through 1763.2.16
  but do not document an exact birth date. Best-guess adult age only; not a claim of a sourced date.

## Task #56 — Fix BUR 1763 territory + author minor Indo-China rulers — DONE
- **What it was**: task title named a single fix ("strip Arakan core, author Hsinbyushin ruler") for
  BUR, following on from #47's Kokang-border research digest
  (`research/RESEARCH_KOKANG_BURMA_BORDER_1763.md`), which found BUR's `own_control_core` at 1763 start
  was still carrying its full 1815-inherited territory, including Arakan (independent under the Mrauk-U
  dynasty until Konbaung's 1785 conquest — 22 years after this mod's 1763.2.16 start).
- **Territorial half**: added new tag `ARK` (`setup/countries/countries.txt`, `setup/countries/
  indo_china/arakan.txt` — new file) and carved provinces 30/1696/5667/6627 (Arakan proper, per
  `map_data/areas.txt`'s own area boundary, distinct from Pegu/Lower Burma) out of BUR's
  `own_control_core` in `setup/main/00_default.txt`, giving ARK its own country block (absolute_kingdom,
  burmese/theravada, capital=30). Both blocks got comment headers citing #56 and the research digest.
- **Scope decision (mid-task, logged per Rule 1's genuine-user-decision carve-out)**: before authoring
  a ruler, checked whether any OTHER minor Indo-China tag had an authored ruler — none did; all ~20
  siblings (Hsipaw, Kengtung, Siam, Cambodia, the Lao/Vietnamese splinters, etc.) ran on the engine's
  generated placeholder. Authoring Hsinbyushin alone for BUR would have been the sole exception among
  ~20 siblings, an inconsistent one-off. This is a genuine judgment call the code/history can't settle
  on its own (how far to widen scope), so — per the skill's Rule 1 exception for a real user-only
  decision — asked the user directly rather than picking silently. **User chose the largest of 3
  offered options: research and author historically-correct 1763 rulers for every minor Indo-China tag
  with a documentable individual, not just BUR.** This is a deliberate, user-approved scope expansion,
  not a self-granted one.
- **Research correction (own assumption overturned)**: the task's own title named "Hsinbyushin" as
  BUR's ruler, matching common knowledge of the Konbaung dynasty's most famous 18th-century king — but
  research established Hsinbyushin only accedes 1763.11.28, AFTER the mod's actual 1763.2.16 start
  (confirmed against `bookmark/1763_bookmark.md:76`, "day after the Treaty of Hubertusburg"). The
  ruler correctly on the throne at the actual start date is **Naungdawgyi**. Used Naungdawgyi instead,
  overriding the task title's own wording in favor of accuracy at the real start date. Two more of my
  own first-guesses were also corrected by the research pass before writing anything: VIE is Nguyễn
  Phúc Khoát (not Phúc Thuần, who only succeeds 1765), VIN is Ong Long (not Ong Boun/Siribunyasan, who
  only succeeds 1767).
- **Ruler half**: new file `setup/characters/00_Indo_China.txt`, char IDs 647-655 (contiguous off the
  confirmed prior global max of 646), one per tag, each seated via the proven AUS/Korea template
  (`c:TAG={ set_as_ruler=char:N }` from inside the character block itself — no `00_default.txt` change
  needed for ruler-seating). Rulers authored: BUR=Naungdawgyi (b.1734, `tactician`), SIA=Ekkathat
  (b.1718, `lazy` — matches his documented reputation as a disengaged ruler who deferred to his
  brothers-in-law), CBI=Outey Reachea II (b.1740), CPK=Sayakumane, LPR=Sotika-Kuomane, VIE=Nguyễn Phúc
  Khoát (b.1714), TRH=Trịnh Doanh (b.1720, `tactician` — successful revolt-suppression record),
  VIN=Ong Long, PHN=Chao Ong Lo. ARK (this task's own new tag) and CPA (Champa) deliberately get NO
  authored ruler — research found no individually-documented monarch for either at this date, so both
  stay on the engine-generated default, same as the other 14 minor tags (CHH/CMI/HSI/KTG/MKN/MLM/MMT/
  MPN/TNI/LPG/LPP/LSU/NAN + CPA) that were checked and confirmed to have no viable documented ruler.
- **Review, one fix**: code-review agent found `add_trait = decadent` (my first draft, for SIA/Ekkathat)
  is not a defined trait anywhere in `common/traits/` — would have silently no-op'd and logged
  "invalid trait" noise. Swapped for the verified `lazy` (`common/traits/00_personality.txt:548`),
  which fits the same historical intent. Also added a one-line doc note flagging the 4 placeholder
  birth dates as best-guess (see ASSUMPTIONS above). All other 8 checks (char-ID contiguity, template
  match, tag/culture/religion validity, birth-date plausibility, no parser-desync hazard, `dna=""`
  convention, no double ruler-seating, no BOM) passed clean on first pass.
- Committed `6bf0364be` (territory) + `24f07942e` (rulers). Both pushed together to `merge-overnight`.
- **STATUS: DONE — closing #56.**

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

### Task #51 (4th piece) — Revenue perf rollup — DONE (2 adversarial review rounds, implemented)
- **What it was**: 3 of #51's 4 named pieces (Customs IG title, Canton card, 1:1 rule) were already
  done and committed earlier this session (`54cdd52ed`). Diagnosis (Explore agent) traced the 4th
  ("Revenue perf rollup") to a specific, real gap: `QING_ministry_recompute_perf_revenue`'s term (g)
  (#431, "TREASURY-INFLOW REWARD") sums three real revenue streams — salt, Canton, caravan — into the
  Revenue Ministry's own performance score, specifically so a minister isn't punished because one
  stream underperforms. Maritime Customs (shipped after #431) was never added, purely because the
  subsystem didn't exist yet when #431 shipped — a missed-follow-up gap, not a deliberate exclusion.
- **Design round 1 proposed a broken fix**: snapshot the REAL post-currency-conversion treasury delta
  from the customs revenue grant (mirroring a cited "before/after diff" precedent) and fold that into
  the existing sum. Adversarial review found this was a HIGH-severity defect the design never
  checked: the real delta is ~1000x larger than the other three streams (a `CURRENCY_grant_country_
  wealth` internal ×1000 scaling factor), so folding it in would permanently pin the Ministry's
  performance term at its `+15` cap forever — the term would stop discriminating between a good and
  bad minister at all, the opposite of #431's own stated intent. Review also found the cited
  precedent (`se_SUBJECT_QING.txt:1213`) was misdescribed — it's a min-clamp, not a before/after diff
  — so no real precedent for that pattern actually exists in this codebase.
- **Fixed (round 2)**: publish the PRE-conversion `thousands` INPUT value directly instead (a single
  unconditional `set_variable`, no snapshot, no diff, no branching) — this input (~0-20/quarter) sits
  in the same order of magnitude as the three existing streams (combined ~0-60), even though it is
  technically a different currency-scale number, not a literal tael count. A genuinely simpler fix
  than round 1's, and it fixes the scale problem as a side effect. Second adversarial review round
  independently re-verified the value range against all three sibling streams' own income
  computations and found zero further issues — CLEAN, ready to implement.
- **Implementation**: `se_QING_CUSTOMS.txt` (one new unconditional `set_variable` publishing
  `qing_customs_income_last`, placed right after `qing_customs_revenue_tmp` is computed and before
  the existing grant block — untouched); `se_QING_MINISTRY.txt` (one new guarded `has_variable`/
  `change_variable add` line, identical shape to its three siblings, inside the existing sum).
- **Review (implementation)**: code-review dispatched on the full diff — CLEAN, zero findings.
  Verified brace balance, correct read-ordering (the tmp var is fully computed before the new publish
  line reads it), correct position in the Ministry sum (before the `/4` divide and `+15` cap), zero
  dangling references repo-wide, and confirmed the explicitly-out-of-scope Accountability metric
  (`QING_acc_metric_treasury`, a separate "revenue" judgment system this design deliberately did not
  touch) is genuinely untouched in the diff.
- **Commit**: `0c04c6620`, pushed.
- **STATUS: DONE. Task #51 (all 4 pieces) now fully complete.**

### Task #19 (#107) + #20 (#108 residual) — DONE (#19 already-complete on re-check; #20 boot-log-traced and fixed)
- **#19 (#107 Div/0 + stockpile + bimetallic error-log flood)**: re-checking the task tracker against
  `git log` found this was ALREADY FULLY COMPLETE from a prior session (`3ffc8cf03` food-stockpile
  seed, `02acceb9f` GT_set_tradegood_price Div/0 guard, `ad7765927` final #108 accounting) — the
  tracker's "pending" status was stale, not a real gap. Verified via `overnight/OVERNIGHT_2026_08_11.
  md`: all three sub-roots (food-stockpile unset flood, the Div/0 sub-root, the 242 bimetallic reads)
  closed; the bundled WAR_scripted_guis.txt 804-line flood correctly identified as a non-fatal
  engine WARNING in defunct upstream code, not a real error. Marked DONE, no new work needed.
- **#20 (#108 residual EDU Div/0, 16x/boot, explicitly left open for boot-log confirmation)**: read
  the newest available boot log (`~/Downloads/logs.zip`, 2026-08-12 18:39 — predates today's #101/
  #88/#51 commits but postdates the #107/#108 fix commits, so it's a valid source for THIS residual)
  per the logs skill's full-ranked-inventory discipline. Found the exact frame: `oa_wealth_changes.
  txt:101 -> EDU_update_effect:3 -> EDU_set_t2_national_bonus_from_universities:2`. Traced the call
  chain (`EDU_set_t2_national_bonus_from_universities` -> `EDU_university_national_bonus` ->
  `EDU_university_law_religious_colleges_country_impact_owner_scope`, only reachable when
  `law_university_religious_colleges` is active) to a bare `divide = num_of_cities` with no guard — a
  country with zero owned cities Div/0s. **Fix**: clamped the divisor via the proven `divide = {
  value = X  min = 1 }` idiom already used at `ADMIN_svalues.txt:193-195` and `AI_svalues.txt:1234-
  1238`. Code-review confirmed this is the ONLY unguarded divide reachable from the traced error
  frame (not a wrong-site guess), confirmed the fallback value is sensible (bounded, in-range,
  matching the function's own `≤0.9×base` intent), and flagged a LOW-severity twin
  (`EDU_university_law_religious_colleges_country_impact`, province-scope, same bug shape) that is
  genuinely DEAD CODE (repo-wide grep: unreferenced anywhere) — correctly left untouched per this
  fix's own narrow scope (the traced error frame, not a speculative expansion to unreachable code).
- **Commit**: `7b4a92b8d`, pushed.
- **STATUS: Both DONE.**

### Task #22 (#35) — restore #23 currency verify tooling — HARD BLOCK, correctly left in_progress (Rule 1 block type #3: genuine user-only dependency)
- **Checked, not re-done**: the tooling restoration itself is already complete from a prior session
  (`d40a53ffa`/`c9da3fc16`, reverting the premature strip in #16) and verified still intact in-tree
  this run: `se_ECON_LOG_TZPROBE.txt`, `tools/curx_analyze.py`, `tools/gen_econ_tzprobe.py`, and both
  call sites (`ECON_LOG_curx_dump_pre` in `se_ECON_LOG.txt:222`, `ECON_LOG_curx_dump_post` in
  `oa_wealth_changes.txt:365`) all present, nothing has silently re-stripped them since.
- **Why this is a genuine hard block, not a fake one**: the task's own remaining steps (boot
  `-debug_mode` across several quarters, run `curx_analyze.py`, confirm #23's gbip-flat/inflation~0
  fix AND characterize the #46 gold/silver crossover, THEN re-strip as a fresh commit) require the
  USER's own boot — there is no way to fabricate or substitute for a real multi-quarter play session
  from within this session. Per the standing `imp19c-verify-before-strip-logs-rule` memory (written
  after the user's own explicit correction: "making changes deep in the inner workings of the economy
  and then stripping logs to monitor said changes is insane"), re-stripping BEFORE that confirmation
  would repeat the exact strip-before-verify mistake this task exists to prevent. Left in_progress,
  not force-closed — nothing to commit this pass.

### Task #23 — unify silver/gold reserve values to 千兩 — DONE (full inventory + scoped fix + 1 new follow-up task)
- **What it was**: task title asked to "unify all silver/gold reserve values to 千兩," explicitly
  labeled "not a bug, a consistency task." Diagnosis (Explore agent, full inventory of every reserve-
  adjacent surface touching CHI) found: gold is genuinely, deliberately inert for CHI (`gold_reserve_
  size = 0` at every seed site, no design doc anywhere gives Qing China a meaningful gold reserve —
  historically correct, a silver-standard economy) — nothing to unify there. Silver, however, had ONE
  genuinely unforked display surface: the silver-reserve row's TOOLTIP (`RESERVE_VALUE_SILVER_TT`)
  computes "Market value"/"Currency value" via svalues calibrated to the vanilla hundreds-troy-lb
  unit — the exact same garbled-by-scale bug `#89` already fixed for the row's LABEL text, one
  tooltip layer over, apparently missed when `#89` shipped.
- **Fix**: forked the tooltip for CHI via a new `silver_reserve_tooltip_text` customizable_
  localization selector, byte-identical in shape to `#89`'s proven `silver_reserve_row_text`
  selector — CHI gets a new loc key (`RESERVE_VALUE_SILVER_TT_QING`) showing the raw 千兩 figure
  directly (no attempt to compute an equivalent "market value" conversion for CHI, since none has a
  well-defined 千兩 analogue without inventing new economic semantics — correctly out of scope for a
  unit-CONSISTENCY fix, not a design decision this ticket should make); ROW keeps the vanilla
  tooltip byte-for-byte.
- **Found but deliberately NOT folded in (logged loudly, new task #54)**: the same diagnosis pass
  surfaced a genuinely different, more severe issue while surveying every reserve surface —
  `INCOME_sell_reserves` (hit by BOTH the manual sell-reserve button and the automatic deficit-
  mitigation path, confirmed via the function's own code comment that CHI reaches this path) mixes
  units for CHI's silver: it depletes `silver_reserve_size` (千兩) by `amount_to_sell`, but prices the
  treasury credit using `global_base_import_price_silver` (hundreds-lb-calibrated) and credits the
  capital governorship's `silver_stockpile` with the same raw number as if it were hundreds-lb of
  physical silver goods. This silently mis-prices every CHI reserve sale — a LIVE economic-
  calculation bug, not a display consistency nit, and a different severity class than what #23's own
  task text ("not a bug") describes. Per this project's own bug-vs-missing-feature and no-silent-
  scope-expansion discipline, NOT fixed here — logged as task #54 for its own diagnosis→design→
  review→fix cycle, matching how economy-touching bugs are handled in this codebase.
- **Review**: code-review dispatched on the 3-file diff (selector, loc key, GUI wiring) — CLEAN, zero
  findings. Confirmed selector shape matches the proven `#89` precedent exactly, confirmed the
  `Custom()`-selector GUI syntax matches another proven live example (`inflation_deflation_tooltip`),
  confirmed loc formatting-tag balance (9 openers/9 closers, matching the original), confirmed the
  fork is complete (no second unforked tooltip-wiring site anywhere in the repo).
- **Commit**: `175596688`, pushed.
- **STATUS: DONE.**

### Task #26 — Aligun (585) holds Salt Commissioner + Jingzhou garrison commander — NO DEFECT, self-corrects by design (user-confirmed, dropped)
- **What it was**: task reported Aligun (char:585, the historical Jingzhou banner-garrison commander,
  raised by `SE_qing_armies` at day-30 boot) also seated as Salt Commissioner — a 1:1-rule violation.
- **Diagnosis**: traced both draws. `QING_salt_commissioner_appoint`'s candidate gate DOES exclude
  `has_variable = qing_officer_marker` (the flag stamped on any character successfully attached as a
  garrison/fleet commander) — so on a clean draw Aligun should never be picked at all. But the two
  systems race at boot: the garrison raise (`qing_force_setup.1`, day 30, one-shot) and the salt
  commissioner's first seat (`QING_salt_init`, called from the monthly on_action) land in the same
  early window, so a commissioner could in principle be drawn just before (or in the same tick as)
  the garrison stamp lands. Rather than a missing exclusion, `QING_salt_reconcile` (called every
  pulse, AFTER income is banked) already has a built-in self-correction for exactly this: branch (a)
  explicitly relieves "a commissioner who later took a command... `has_variable = qing_officer_
  marker`," then branch (b) immediately backfills a fresh, eligible pick the SAME pulse.
- **Verified against the newest available boot log** (`~/Downloads/logs.zip`, 2026-08-12): found the
  EXACT sequence live in `debug.log` — `QING_salt_commissioner_seat`/`QING_post_stamp` at 17:28:40
  (initial draw), then at 17:41:08 `QING_salt_reconcile` fires `"salt: relieved a double-booked
  commissioner (also a serving commander/officer) for"` followed immediately by a fresh
  `QING_salt_commissioner_appoint`/`_seat`/`_post_stamp` sequence in the SAME log block — i.e. the
  exact self-healing the reconcile design promises, observed actually happening, not just claimed in
  a comment. The double-booking relief fired exactly once (not repeatedly), consistent with a
  transient boot-race that the very next pulse corrects, not a persistent live bug.
- **User confirmation mid-diagnosis: "drop this task, it already solves itself."** Matches the
  evidence exactly — closing as NO DEFECT, no code change. This is a genuine diagnosis outcome
  (mechanism working as designed), not a deferral.
- **STATUS: DONE (no code change — confirmed self-correcting by design + boot-log evidence + user
  confirmation).**

### Task #25 — Talleyrand phantom-char + scan all events — DONE (fix already shipped; scan clean)
- **Talleyrand phantom-char half**: already fixed earlier this session (commit `4aef63a7e`,
  before this compaction) — `qing_roster.8.a`'s inline `QING_customs_establish`/`_appoint_ig` calls
  were the first-ever writers of `qing_customs_foreign_control`/`qing_customs_efficiency`, and an
  option's effects are ALSO evaluated once, unexecuted, to render the tooltip preview before the
  player clicks — the guard's `set_variable` doesn't commit in that pass, so the next read of the
  same not-yet-existing var threw (14,832 hits in error.log) and spilled the wrong scope (Talleyrand)
  into the rendered preview. Deferred the real work to a hidden follow-up event (`qing_roster.22`,
  `is_triggered_only`), mirroring the identical fix already shipped for `qing_keju.4.a` ->
  `qing_keju.21`.
- **"Scan all events" half**: dispatched a very-thorough background sweep of every file in
  `events/imp19c_mod_events/` (including subdirectories) for the same bug class — an option whose own
  effects are the first-ever writer of some var via an own-var-guard idiom, called inline (not
  deferred to a hidden event), where a later effect in the SAME option reads that var unconditionally
  or a create_character risks a phantom-scope spill into the tooltip. Four independent, cross-checked
  passes (duplicate-var scan, inline-create_character scan, first-writer-function inventory across
  all ~150 guarded vars in `common/scripted_effects/`, and boot-seed reachability closure) found MANY
  structurally-similar candidates but confirmed EVERY one is already protected — either boot-seeded
  unconditionally elsewhere, guarded by `has_variable` before the later read, or already wrapped in
  `hidden_effect`/`trigger_event` from an earlier fix pass (`#38`/`#92`/`#123`/`#31` are all prior
  instances of the same defensive pattern already applied). Cross-checked against the newest available
  error.log (pre-dating this session's own #25 fix) and found zero hits of the diagnostic signature
  that flagged both prior confirmed instances — consistent with #25 having been the only LIVE instance
  that had actually fired and left a flood signature.
- **STATUS: DONE. No further code change needed — the scan is a clean result, not a gap.**

### Task #28 — Robert Hart seated as Caravan Superintendent instead of Maritime Superintendent — DONE
- **What it was**: task #27 (already shipped, `54cdd52ed`) added `qing_customs_ig_marker` (the
  Customs Inspector-General, Robert Hart) and `qing_court_artist` (the court painter, Castiglione) to
  `QING_char_holds_court_position`'s OR-set, which correctly stops FUTURE appointment draws from
  picking a man already holding either post. But #28 reported Hart STILL showing up seated as Caravan
  Superintendent — the wrong-post symptom persisted despite #27.
- **Diagnosis**: each of the three office suites (caravan superintendent, salt commissioner, Hoppo)
  has its own quarterly RECONCILE function that self-corrects a double-booking arising from a race or
  a stale/pre-#27 save (the SAME proven pattern that made #26 self-heal without a code change) — but
  each reconcile's OWN double-book relief gate checked only `is_general`/`is_admiral`/`is_governor`/
  `qing_officer_marker` (military/administrative double-booking), never `qing_customs_ig_marker` or
  `qing_court_artist`. So a man double-booked against either of THOSE two posts specifically could
  never be caught and relieved by the reconcile — the appointment picker was fixed, but nothing would
  ever un-seat an EXISTING bad double-booking against the new markers.
- **Fix**: added `has_variable = qing_customs_ig_marker` and `has_variable = qing_court_artist` to
  all THREE reconciles' double-book OR-conditions (caravan superintendent, salt commissioner, AND the
  Hoppo — not just the one office #28 named, since all three share the identical #27-caused gap and
  fixing only one would leave the other two silently broken in the same way), mirroring the existing
  general/admiral/governor/officer_marker shape exactly.
- **Review**: code-review dispatched on the 3-file diff — CLEAN, zero findings. Confirmed all three
  edits are syntactically identical in shape, confirmed the semantic correctness (this is the relief
  gate, not the picker's own exclusion — a genuinely different piece of code), confirmed the backfill
  logic immediately after each relief block runs correctly (re-seats a fresh, properly-excluded man
  the same pulse), confirmed no legitimate double-holding scenario exists that this relief could
  wrongly break (both markers are explicit "one man, one post" members of `QING_char_holds_court_
  position`'s own OR-set, per #27's own comments), and confirmed this directly covers #28's reported
  symptom (Hart as caravan superintendent trips the new OR line, gets relieved, backfilled).
- **Commit**: `bfb5ff3b9`, pushed.
- **STATUS: DONE.**

### Task #33 — persistent -10% deflation — HARD BLOCK, correctly left in_progress (Rule 1 block type #2: unproven diagnosis on shared upstream currency logic)
- **Checked, not re-diagnosed from scratch**: `audits/AUDIT_CURRENCY_23.md` already tracks this exact
  symptom under "Finding 5" (revised 2026-08-13). Status as of the audit's own last update:
  "PARTIALLY DIAGNOSED, mechanism confirmed real, magnitude and dominant channel NOT yet confirmed."
  The audit traces a real, unfixed gap in Finding 3's guard (the `order_size/stockpile`-driven
  `wealth_owed` term can inflate at THIN, non-zero stockpile levels — Finding 3's fix, which is this
  session's own #30 commit `ba8b38672`, only guards the exact-zero/unset case) — but whether this is
  actually LARGE at typical (non-worst-case) stockpile levels, and whether the income-tax channel or
  the state's own channel dominates, are both explicitly still-open questions per the audit's own
  text, not something resolvable by further static code reading.
- **Why this is a genuine hard block, not a fake one**: the audit's own "Next step, before any design
  work" section is explicit: get ONE fresh boot with #30's own diagnostic tags populated
  (`ECON_LOG_curx_natexp`, `ECON_LOG_curx_zerostock_guard`), read the ACTUAL stockpile values for real
  goods/zones, and only then determine whether this mechanism is the dominant driver or a red herring.
  The only log available when the audit was last updated predates #30's own fix by ~7 hours, so it
  cannot show the post-fix state either — there is no log-reading substitute for the boot this task
  needs. This is the SAME underlying boot dependency task #22 (#35) tracks, not a separate blocker
  needing its own resolution.
- **Not force-closed, not silently dropped**: left in_progress. Per this run's own standing discipline
  (Rule 1 block type #2 — unproven diagnosis on shared upstream currency logic — respond by building
  the instrumentation that will prove it, not by guessing at a fix), the instrumentation ALREADY
  exists (this is exactly what task #22/#35 restored and kept live). No further design/implementation
  work is legitimate here until that boot lands and the audit's own next-step question is answered.
- **Closed per user instruction** ("close this then") — same disposition as task #22 (#35): a
  correctly-identified hard block, not a defect to force through, closed rather than left spinning on
  a dependency this session cannot satisfy itself.

### Task #35 — qing_personnel/qing_censorate missing localizations — DONE
- Explore agent found 4 live, unlocalized modifiers (qing_personnel_cultivated_minor/major,
  qing_censorate_oversight_minor/major, `00_from_events_character.txt`) applied every quarter by
  `QING_council_apply_officer_buffs` — a capable Personnel Minister or Grand Inspector rendered the
  raw key on a fellow councillor's tooltip. Found + fixed 2 same-pattern siblings in the same file
  (`qing_grand_secretary_counsel_*`, `qing_guard_vitality_*`) in the same pass, per the audit's own
  recommendation. Review found one LOW wording inaccuracy (Personnel's desc said "all council
  members" when the holder actually excludes himself) — fixed.
- **Commit**: `3c17f699f`, pushed. **STATUS: DONE.**

### Task #37 — tie Crumbling Fortress event into the Ministry of Works — DONE (3 design review rounds)
- `flavor_eve.8` is a generic, all-nations event with no `tag = CHI` gate. Round 1 of the design
  caught a CRITICAL (a static `right_portrait` field would dangle for every non-Qing firing) and a
  second CRITICAL (the cited dike-cost "finesse-discount factor" doesn't exist). Round 2's fix for
  the first introduced a NEW dangling-scope bug one layer down (`scope:works_minister`, never saved).
  Round 3 fixed both by acting directly on `var:qing_office_works_holder` with no scope save at all,
  matching a proven precedent (`qing_household_events.txt:356`), and derived a real cost number from
  the dike-cost tier ratio (175/220 ≈ 0.795 → -40 vs -50) instead of an invented constant.
- Implementation: both options gain a CHI-gated `if`/`else` block entirely in the option body,
  every non-CHI/vacant-seat case falls through to the exact original flat effects unchanged.
  Code-review confirmed exactly one `add_treasury` call fires in all 4 possible cases (non-CHI,
  vacant seat, weak minister, able minister) — the specific risk the design's own reviews flagged.
- **Commit**: `02e2adc56`, pushed. **STATUS: DONE.**

### Task #38 — confirm Southern/Upper Study fill mechanism, then FIX (user correction mid-session)
- Diagnosis confirmed both studies' DRAW functions already correctly draw from the exam pool via
  `QING_char_holds_court_position`'s canonical exclusion, matching every GC position's own idiom —
  correctly reported as "no defect." **User corrected this reading**: the actual gap is that neither
  study AUTOFILLS — both were capped at their boot-seed size (2 for Southern Study, 0 for Upper
  Study) because their quarterly pulses had an autofill explicitly REMOVED on 2026-07-22, before the
  #116/#118 structural 1:1 protections existed. Since both draw functions already carry those
  protections (built after that removal), the original removal's safety concern no longer applies to
  them specifically — reintroducing autofill here does not reproduce the double-booking bug that
  removal was guarding against, and does not touch the separate #116 decision to keep GC OFFICES on
  create_character.
- Fixed: both quarterly pulses now call their own draw function repeatedly (each call self-guarded
  on count<cap + a real candidate existing, so extra calls are cheap no-ops) — mirroring
  `QING_subpost_staff_corps_minted`'s own "N rungs so the highest law tier is reachable in one pulse"
  pattern. Review caught a real gap: Southern Study's cap is LAW-driven (4/8/12), and the first draft
  only added 8 rungs — fixed to 12 so the Broad Cabinet tier is reachable in one pulse too.
- **Commit**: `cf5d49c7c`, pushed. **STATUS: DONE.**

### Task #39 — Lifan Yuan "Replace amban" only shows for half the sitting ambans — CLOSED (no defect found; one unrelated bug fixed along the way)
- Diagnosis: traced `qing_amban_manage_replace_button` (`SUB_QING_amban.txt:238+`) to its eligibility
  gate `QING_amban_warrants_resident_trigger` (`qing_dynasty_triggers.txt:136-148`) — the same shared
  trigger the Post button uses. Confirmed via `git show 1b9549d22` ("#34") that a prior commit already
  fixed the EXACT bug class described here: an old culture-only inline test missed the two
  Manchu-ruled `autonomous_governorship` posts (ILI/ULS), so Replace showed for the mongolic/bodish
  subjects only — that commit re-aligned BOTH buttons to the shared trigger. That fix is present,
  unchanged, in the current file.
- Verified all 6 amban-hosting subjects (TIB/ILI/ULS/MKD/MNC/HLJ) independently satisfy the shared
  trigger: TIB via `primary_culture = tibetan` (confirmed in the `bodish` culture group,
  `00_bodish.txt:44`) and the other 5 via `subject_type = autonomous_governorship`
  (`setup/main/00_default.txt`). No half-coverage in the trigger logic as currently written.
- Checked the newest boot log (`~/Downloads/logs.zip`) — the manual replace picker fired successfully
  twice in debug.log, consistent with the button currently working rather than being half-gated.
- Could not reproduce the reported symptom in source. Verdict: **not a live defect in the current
  codebase** — the bug class described was already fixed pre-session by #34's commit. Closing with no
  further change to the Replace-button gating itself.
- **Found while investigating (unrelated, but real and fixed)**: `qing_amban_events.txt:301` called
  `LOG_fail = { sys = QING  fn = "qing_amban.6" }` with no `reason` argument. `LOG_fail`'s definition
  (`se_LOG.txt:88-93`) references `$sys$ $fn$ $reason$` in its debug_log string — a missing required
  macro param voids the WHOLE invocation at compile time (the established log-string-macro-rule
  class), so this fail-branch's diagnostic logging was silently dead on every boot. Fixed by adding
  `reason = "picked candidate no longer eligible or seat filled before the trampoline fired"`,
  matching the convention used everywhere else (e.g. `se_QING_AMBAN.txt:161`). This does not touch
  the Replace-button gating and is not believed to be the cause of #39's reported symptom — logged
  separately per the no-untraced-assertion rule (found live, fixed live, not conflated with #39's
  premise).
- **Commit**: `259f01fb2`, pushed. **STATUS: CLOSED — #39's described symptom not reproducible in
  current source (already fixed by prior commit 1b9549d22); one unrelated LOG_fail compile bug found
  in the same file and fixed.**

### Task #40 — "A Dispute at Kashgar" loc broken for all 3 options — FIXED
- Diagnosis: checked the newest boot log (~/Downloads/logs.zip, Aug 12 18:43) and found the exact live
  error class matching the raw ERROR:[...] string symptom: `Could not find promote for 'MakeScope' in
  'ROOT.MakeScope.GetVariable(...)'` — repeated for all 6 `_shown` vars (negotiate/coerce/collude ×
  success/fail). `ROOT` has no `MakeScope` promote in the loc data-context; only scope objects with a
  bound country (Player, a saved character/province scope, GetCountry) carry it. The prior "#90
  2026-08-11" fix had swapped one broken form (`ROOT.GetCountry.MakeScope`) for a DIFFERENT broken form
  (bare `ROOT.MakeScope`) and called it "proven" without ever boot-verifying it — the tooltip has been
  rendering the raw error string since that commit, not since before it.
- Fix: all 6 `GetVariable` reads in the 3 option tooltips (qing_caravan.4.negotiate/.coerce/.collude.tt)
  now use `[Player.MakeScope.GetVariable(...)]` — the idiom actually proven elsewhere in the codebase
  (`economic_enchancement_l_english.yml`'s national_debt_text_*, `imp19c_windows.gui:1919`'s salt-income
  read). CHI is always the player in this mod and the event is CHI-gated (`trigger = { tag = CHI }`), so
  Player.MakeScope resolves the exact same scope the vars were stashed on in the event's `immediate`.
- Code-review (dispatched, verdict: fix correct/complete/safe, no CRITICAL/HIGH) caught one MED: my
  first-draft comment overclaimed that the #90 form was "ALSO broken the same way" as unverified fact —
  `.GetCountry` DOES carry a MakeScope promote (a materially different chain from bare ROOT), so it may
  have failed for a different reason. Corrected the comment to state this as a live possibility, not a
  established mechanism, per the same "don't call unverified things proven" principle the fix itself is
  about.
- **Follow-up filed, NOT fixed now (out of this task's boot-confirmed scope)**: the review also flagged
  `subject_add_to_customs_union_federation` (duplicated in `00_subject_rework_l_english.yml:97` and
  `trade_actions_l_english.yml:57`) uses `[ROOT.GetCountry.MakeScope.GetVariable('member_of_federation')
  ...]` — a DIFFERENT chain from the one just fixed, renders only in a subject-trade panel the boot log
  never exercises, so absence-from-log is not evidence either way. Logged as a new task (#55) to verify
  live rather than assumed broken.
- **Commit**: `6d3d18d96`, pushed. **STATUS: DONE.**

### Task #41 — Henan "Overstretched Administration" despite reported Administrative Capacity surplus — FIXED
- Diagnosis: `ADMIN_state_loyalty_from_province_drain`/`_gain` (the state modifiers behind the label) are
  only reapplied by `ADMIN_set_loyalty_impact_all_states` (se_ADMIN.txt), called from exactly 2 sites:
  economy setup (once) and `yearly_country_pulse` (00_yearly_country.txt:95-99), gated behind a 730-DAY
  per-country throttle. That throttle exists because the walk is `every_governorships ->
  every_governorship_state` across EVERY country — the old monthly version of this same call
  (`monthly_administration_pulse`, oa_wealth_changes.txt) was disabled for "unacceptable monthly
  slowdowns" for exactly that all-countries cost. Meanwhile the live Administrative Capacity REPORT
  window (`qing_report_open_admin`) computes `ADMIN_provided_state`/`ADMIN_required_state` fresh on every
  open — so a state can show a live surplus in the report while its actual loyalty modifier stays stuck
  on "Overstretched" for up to ~2 years after admin capacity crossed into surplus. Exactly the reported
  mismatch, not a misdiagnosis (#33/#115 precedent checked — this is a DIFFERENT stale-cache class, not
  the regional-price formula).
- Fix: added `ADMIN_set_loyalty_impact_all_states = yes` inside `QING_GOV_pulse` (se_QING_GOVERNANCE.txt,
  step "2a"), the Qing governance suite's own pulse — already CHI-only + human-only + ~90-day-throttled
  (`qing_mechanics_pulse_on_action`). This costs ONE country's governorships per quarter, not the
  all-countries walk that forced the original 730-day throttle, so the state modifier now tracks the
  report's live numbers within a quarter instead of up to two years, without reintroducing the perf
  problem that disabled the old monthly version (that walked every AI country; this walks one human one).
- Code-review (dispatched, verdict: correct/safe, no CRITICAL/HIGH) confirmed: correctly scoped (country
  scope match), performance claim holds (O(states×provinces), same cost CHI already pays at setup/yearly,
  now just more often), fully idempotent (remove-then-reapply, safe to double-fire with the yearly call),
  CHI/human-only confirmed via the trigger chain. One LOW fixed: the function's header comment ("All
  O(1)") was stale after the insertion — corrected to note the new step's real cost and why it's
  affordable at this cadence. Two informational notes logged (not action items): the CHI-side yearly
  730-day refresh is now redundant (harmless, still needed for AI/other countries); a pre-existing
  upstream quirk means `ADMIN_state_loyalty_gain` can structurally never apply a nonzero stack (the
  provided/required clamp keeps overall_impact >= 0) — unrelated to this fix, not touched.
- **Commit**: `ba6396d00`, pushed. **STATUS: DONE.**

### Task #42 — Ministry of Personnel clash events firing far more than other Ministries — FIXED
- Diagnosis: `QING_personnel_evaluate_governors` (se_QING_PERSONNEL.txt) `every_character`-loops over
  EVERY governor each quarterly pulse; the per-governor clash roll (chance=10) and promotion roll
  (chance=8) both gate on `NOT has_variable = qing_dept_cd_personnel`, but the cooldown was only
  STAMPED inside each roll's SUCCESS branch. A failed roll left the cooldown unset, so every OTHER
  eligible governor in that same quarterly pass rolled independently too (N governors -> effective
  chance 1-(0.9)^N, not a flat 10%), and a fully-failed quarter left it unset for the NEXT quarter as
  well, compounding. Confirmed against the proven sibling idiom: Revenue (se_QING_REVENUE.txt:287) and
  Works (se_QING_WORKS.txt:55) both stamp their department cooldown on ENTRY, before the roll —
  consuming exactly one attempt per ~3-quarter cycle regardless of outcome. Personnel's stamp-only-on-
  success was the divergence. Boot log cross-check: 211 personnel-evaluation lines this boot vs a
  single-digit count for Revenue/Works domain rolls, consistent with the N-governor multiplier.
- Fix: moved the `qing_dept_cd_personnel` stamp in BOTH the promotion (.3) and clash (.2) branches to
  fire unconditionally right after the outer gate passes, before the `random` roll — matching
  Revenue/Works exactly. Removed the now-duplicate stamp from inside each success branch.
- Code-review (dispatched, verdict: fix correct, bug confirmed real, no CRITICAL/HIGH) flagged two
  non-blocking trade-offs, both consistent with the fix's own intent rather than new bugs: (1) the
  promotion and clash rolls now mutually throttle each other within one quarterly pass in an
  iteration-order-dependent way (a failed promotion roll can consume the department's one attempt
  before a clash-eligible governor is reached) — Revenue/Works avoid this by picking event TYPE from a
  random_list AFTER a single roll succeeds, but restructuring Personnel's per-governor dispatch to match
  is a larger design change outside this bug's scope; (2) Personnel's per-roll chances (8/10%) are much
  lower than Revenue/Works (30-40%), so the ministry may now read as quieter than before, not just
  "not too often" — noted as a tuning lever (the chance values), not a defect, if a boot shows it's now
  under-firing.
- **Commit**: `6480f63b1`, pushed. **STATUS: DONE.**

### Task #43 — exam event targeted Chenggunjab (25261) for a degree despite already holding fanyi_jinshi — FIXED
- Diagnosis: `qing_keju.2` (Palace Examination event, qing_keju_events.txt) picks its "laureate" via two
  candidate pickers (a primary `any_character`+`ordered_character` pair, and an `else` fallback). Both
  filtered candidates on ONLY `NOT = { has_trait = jinshi }` — narrower than the shared canonical
  `QING_char_exam_degreeless` trigger (qing_dynasty_triggers.txt), which excludes all 11 exam-degree
  traits (civil + banner fanyi_jinshi + wuju). Every OTHER exam-conferral site in se_QING_EXAM.txt (mint/
  cohort-confer/per-person-sit) already used the shared trigger; qing_keju.2 was the one hand-rolled
  exception. A bannerman already holding fanyi_jinshi passed the narrow filter, got picked as laureate,
  and option `.2.b`'s `add_trait = jinshi` stacked a SECOND, mutually-exclusive degree onto him (jinshi/
  fanyi_jinshi are declared `opposites` in 00_imp19c.txt) — exactly the reported Chenggunjab case.
- Fix: replaced the `NOT = { has_trait = jinshi }` filter with `QING_char_exam_degreeless = yes` in both
  the primary `any_character` check and its paired `ordered_character`. Also gated the previously-
  UNFILTERED `else` fallback `ordered_character` (which had no degree check at all) with the same
  trigger, so when the primary picker finds nobody degreeless, the fallback correctly finds nobody too
  (rather than re-picking an already-degreed man) and control falls through to the event's existing
  guaranteed-mint safety net (`create_character` under `NOT exists scope:laureate`) — the same net that
  already protects against the unrelated Talleyrand-char:0 dangling-scope bug this event was patched for.
- Code-review (dispatched, verdict: correct, no CRITICAL/HIGH/MED) confirmed the diagnosis, verified
  `QING_char_exam_degreeless` evaluates correctly in both `any_character.limit` and `ordered_character.
  limit` (proven precedent at se_QING_EXAM.txt:252/430/921), confirmed the mint safety net still fires
  correctly, confirmed no residual double-degree race in option `.2.b`'s effect order, and confirmed
  brace balance. One LOW noted (not fixed): the `else` fallback's `ordered_character` is now dead code
  (mechanically guaranteed to find nobody once the primary already returned nobody) — harmless, the
  mint net catches it correctly; left as-is since the LOW review verdict called it optional cleanup, not
  a defect.
- **Commit**: `4286fdee3`, pushed. **STATUS: DONE.**

### Task #44 — "Examination Convenes" says N graduates, Palace Examination only names one — FIXED
- Diagnosis: `qing_keju.1`'s convene prompt shows `qing_keju_expected_grads` (computed by
  `QING_keju_compute_convene`, se_QING_EXAM.txt), but the follow-up `qing_keju.2` (Palace Examination,
  fired 60-150 days later) only ever names/confers a degree on the single `scope:laureate` in its desc
  and both options. The REST of the cohort (hall-band civil extras, a banner Translation Laureate, a
  martial graduate) IS actually seated — via `QING_exam_graduate_cohort`, called from both options inside
  a `hidden_effect` — but with zero player-facing text acknowledging it. Judged a text/communication gap,
  not a logic bug: the 1-named + N-pool-bound-extras split is the deliberate #114/#321 design.
- Fix: added a sentence to `qing_keju.2.desc` restating the expected total via the same
  `qing_keju_expected_grads` var qing_keju.1 already shows (proven `Player.MakeScope.GetVariable` form,
  cross-checked against #40's fix earlier today — NOT the broken bare `ROOT.MakeScope`), and noting the
  rest join the waiting-graduate ranks.
- Code-review (dispatched) confirmed the var read is never stale (set once at convene, never cleared,
  and the 60-150-day fire delay is far shorter than the ~3-year triennial cooldown so no cross-cycle
  overwrite risk) and the `Player.MakeScope` form is correct — but caught a real MED wording overclaim in
  my first draft: "join the hiring pool at once" is factually wrong for most of the cohort (conferred
  juren extras never enter `qing_scholar_pool` at all per its own gate; banner/martial tracks are
  explicitly NOT pool-related; only a freshly-MINTED civil graduate enters immediately). Also caught a
  self-contradiction: at a war-shrunk network (expected=1) the original wording asserted "he is not the
  only one" while displaying "1." Rewrote to "any beyond [laureate.GetName] enter the ranks of waiting
  graduates" — mechanism-neutral and degrades cleanly to "none beyond him" when N=1, no contradiction.
- **Commit**: `ce82d111e`, pushed. **STATUS: DONE.**

### Task #46 — Salt Gabelle event should reference the Salt Commissioner, not the Revenue minister — FIXED
- Diagnosis: `qing_revenue.1` (the Salt Gabelle reform event) was written 2026-07-07, before the #44 Salt
  Commissioner subsystem existed (se_QING_SALT.txt, added 2026-08-10) — a real, always-seated office with
  its own corruption/finesse/squeeze meter feeding the STANDING quarterly 鹽課 income. The event was never
  retargeted onto it: it scored (`QING_revenue_assess_fitness`) and portrayed the generic Grand Minister
  of Revenue on a decision that is squarely the Commissioner's own domain. Confirmed real (a genuine
  staleness gap from sequential feature addition, not a misdiagnosis).
- Fix (5 files): added `QING_salt_assess_fitness` (se_QING_SALT.txt) mirroring the proven
  `QING_revenue_assess_fitness` shape but reading the seated Commissioner; retargeted `qing_revenue.1`'s
  trigger/scope/all-3-options onto `qing_salt_commissioner_holder`; matched the retargeted trigger in the
  panel button (`QING_revenue_ministry_panel.txt`) and the AI pulse's offer-roll (`se_QING_REVENUE.txt`)
  so neither claims the shared court-event slot for an event that would then fail its own trigger; updated
  loc (`qing_revenue_l_english.yml`) to reference the Commissioner. Option B's corrupt-trait windfall now
  correctly checks the man actually skimming the gabelle (previously checked the Revenue minister's trait
  while paying the same character regardless).
- Code-review (dispatched, verdict: sound, no CRITICAL/HIGH) caught one real MED: Option A's first draft
  capped `qing_salt_squeeze` directly, but `QING_salt_reconcile` unconditionally re-mirrors that var from
  the commissioner's REAL corruption stat every quarter — the cap would evaporate after one quarter,
  overpromising the "durable cleanup" the comment claimed. Fixed by acting on his actual corruption stat
  via `QING_char_corruption` (mirroring Option B's own idiom), so reconcile mirrors the reduction forward
  durably. Also fixed a LOW: the pulse's offer-gate matched the event's `is_alive` check but not its
  `employer = ROOT` clause — added for full parity so a non-ROOT-employer edge case can't still claim the
  slot for a no-op. Left the panel's double-gate (both Revenue holder AND Commissioner) as-is per the
  review's own read — a defensible design choice (narratively the Revenue Ministry panel), not a bug.
- **Commit**: `2333c6164`, pushed. **STATUS: DONE.**

### Task #47 — investigate current map/borders near Kokang — DIAGNOSED (research digest, no code change)
- No province, tag, or loc string anywhere in the repo names "Kokang" — read the task as the Yunnan-Burma
  frontier generally, since Kokang sits directly on it. Full research digest at
  `research/RESEARCH_KOKANG_BURMA_BORDER_1763.md`.
- Verified finding: BUR's `own_control_core` (00_default.txt:44368) includes the ENTIRE Arakan/Rakhine
  coast (Akyab + ~9 sibling provinces, 68 provinces total for BUR). Arakan (Mrauk-U) was still an
  independent kingdom in 1763 — Konbaung Burma didn't conquer it until 1785, well past even the 1765-69
  Sino-Burmese War window the mod's own research already dates correctly. The project's OWN existing
  research doc (`1763_WORLD_EAsia_SEAsia.md`) contains an internal contradiction: it lists Arakan under
  "1763 Territory" while its own "Delta vs 1815" note four lines below correctly assigns Arakan to the
  LATER Bodawpaya peak-extent era — the setup file inherited the uncorrected 1815-derived line. A
  pre-existing checklist (`1763_DELTA_Asia.md:355`) explicitly flagged "verify 1763 Konbaung extent...
  may need to trim Arakan/Assam/Manipur if added by 1815" years ago and it was never applied.
- Checked Manipur/Assam separately — NOT actually a problem; BUR's core never extended there (no Meitei/
  Assamese-culture provinces in BUR's core). The Delta checklist's caution was pre-emptive and doesn't
  apply to this map.
- Checked the Kokang-adjacent Shan-state cluster itself (Hsipaw/Lisu/Mongmit/Mongpan/Mongkung/Kengtung/
  etc.) — all correctly modeled as tiny BUR client_states, matching real mid-18th-century Shan-state
  subordination to Ava. NOT anachronistic. Verified programmatically: zero province overlap between CHI's
  Yunnan core (614 provinces) and BUR/Shan-state cores — no border gap or double-claim either.
- Second finding: BUR's ruler was never authored (no character file references BUR) — the Delta doc
  already names the correct 1763 ruler (Hsinbyushin, acceded Jan 1763, son of Alaungpaya) but it was
  never applied either.
- Both real fixes (strip Arakan from BUR's core + decide unowned-frontier vs a minimal Arakan tag; author
  Hsinbyushin) require a territorial-remap + new-entity design call, which is a genuine scope decision
  beyond "investigate the border" — logged as follow-up **#56**, not actioned inline, per the
  no-scope-expansion discipline (same pattern as #54 during #23).
- **Commit**: `151fe6481` (research digest only), pushed. **STATUS: DIAGNOSED, follow-up #56 filed.**

### Task #52 — audit other backfilling-dispatch callers for #49's redraw hole — FIXED (11 sites, 1 CRITICAL missed on first pass)
- Diagnosis: audited every live caller of `QING_office_vacate_dispatch` (the backfilling dispatcher whose
  trailing `QING_council_autofill_office` redraws a replacement ranked by `combined_stats_council_svalue`,
  with an exclusion list checking only `QING_char_hard_disgraced`/`qing_pending_trial`/`is_alive`). Any
  punitive-removal option that applies only a loyalty/popularity penalty — or the `QING_char_taint`
  `corrupt` trait, ALSO not on the exclusion list — leaves the just-vacated man fully eligible to be
  redrawn straight back into the seat he was just punished for, silently undoing the option's effect.
- First pass found and fixed 7 sites: `qing_office_events.txt` (qing_office.1.a "purge the grandee",
  1.b "clip his wings", 9.b both branches "back the abler disputant", 10.a "break the clique", 10.b
  "sacrifice the chief"), `qing_faction_events.txt` (qing_faction.3.a both branches "purge the smaller
  bloc"), `se_QING_JUSTICE.txt` (`QING_justice_vindicate_appeal`). All swapped to the existing structural
  twin `QING_office_vacate_dispatch_nobackfill` (identical per-office branch dispatch, minus the trailing
  autofill call).
- Code-review (dispatched) confirmed all 7 swaps correct AND found a CRITICAL scoping miss: the audit's
  "grep confirmed these are ALL of them" was wrong — 4 more live buggy sites sat in
  `qing_censorate_events.txt` (qing_censorate.1.c "punish the censor for insolence", 2.c "punish for
  lèse-majesté" [taint-only, same non-excluded corrupt trait], 4.a "break the captured censorate", 4.c
  "dissolve the censorate" [net-benign due to a trailing explicit re-vacate, but fragile — fixed for
  robustness anyway]). Fixed all 4 the same way.
- Second review pass (dispatched to verify the CRITICAL fix) confirmed: repo-wide grep now finds exactly
  3 remaining live backfilling calls, all already correctly guarded (on_character_death: target dead;
  `QING_censorate_impeach_uphold`: hard-disgraces first; `QING_justice_strip_for_trial`: stamps
  `qing_pending_trial` first) — no other live call anywhere in the repo. Braces balanced across all 4
  touched files. Confirmed qing_censorate.4.c's trailing `QING_office_vacate = { office = censor }`
  unconditionally clears the seat regardless of dispatch-call order, so the office can never end up
  un-vacated.
- **Commit**: `1e93c2ede`, pushed. **STATUS: DONE** (11 sites fixed total; 3 pre-existing safe sites
  confirmed and left unchanged; verified clean by a second independent review pass after the CRITICAL
  was caught and fixed).

### Task #50 — Zhengzhou city panel shows anomalous "+1815%" figure — FIXED (icon), diagnosed (number is not a bug)
- Diagnosis: dispatched a trace agent (given the difficulty pinning an exact GUI widget from a
  screenshot's pixels alone) which structurally matched the described icon/percent row to
  `gui/province_window.gui:1323-1335` (the "province_output" `icon_and_text` block in the compact
  city card), reading `local_output_modifier` via `GetModifierValue`/`GetModifierTooltip` with an icon
  at `gfx/interface/icons/modifiers/local_output_modifier.dds`.
- **Icon (real bug, fixed)**: confirmed via `git log --diff-filter=D` that this exact icon file was
  deleted in commit `b11371ec3` ("Basic new game compatibility with 2.0", 2021) and never restored,
  while the GUI's reference to it stayed live and unremoved ever since — every boot since 2021 has
  rendered this row with the engine's missing-texture fallback glyph (a generic building/box), matching
  the "anomalous icon" the user described. Restored the original 50x50 ARGB8888 DDS via `git show`
  against the parent commit — byte-identical format/dimensions to the ~15 sibling icons in the same
  directory (verified by code-review, including a git-history + DDS-header re-verification pass).
- **Number (investigated, NOT a bug, not touched)**: traced `local_output_modifier`'s value to the
  vanilla `civilization_value` modifier block (`common/modifiers/00_hardcoded.txt`, `local_output_
  modifier = 1.5`), one of several ENGINE-HARDCODED modifier names in that file (its own header:
  "these names can NOT be removed or changed, as the code uses them") that the engine auto-applies
  SCALED by the province's own live matching attribute — never manually `add_*_modifier`'d anywhere in
  script. Review corroborated the pattern with in-repo siblings carrying explicit "scaled by X" comments
  (`tyranny`, `character_wealth_mod`, `loyal_cohorts`, `office_loyalty`, all in the same file) — and the
  observed arithmetic (1.5 × Zhengzhou's civilization_value ~12 ≈ +1800%, plus the mod's own small
  building/event `local_output_modifier` bonuses stacking on top) is the only mechanism that reaches
  "+1815%"; a flat 150% could not. This is correct vanilla engine behavior for a highly-developed
  metropolis-tier city, just visually startling — left untouched per the honest framing that the scaling
  mechanic itself is engine behavior, not provable from a script line, but strongly corroborated.
- **Commit**: `6ddd18fd7`, pushed. **STATUS: DONE** (icon fixed; number diagnosed as not-a-bug, logged
  loudly rather than silently assumed fine).

### Task #53 — audit overseas-colonization orphaned population modifiers — DIAGNOSED (no defect found)
- Follow-up from #88, which found and fixed a genuine orphan bug: `qing_newworld_agriculture` (a
  standalone `global_population_growth`/`global_population_capacity_modifier` modifier) was a SILO —
  a second system modeling population relief that the #369 Malthusian pressure meter (`qing_pop_pressure`,
  se_QING_POPULATION.txt) had zero awareness of, so the modifier's effect was invisible to the mechanic
  meant to react to population pressure. #88's own review flagged 3-4 similarly-SHAPED modifiers in the
  UNRELATED overseas-colonization subsystem as worth a separate look — this task is that look.
- Found and checked ALL 6 colonization/new-world modifiers carrying `global_population_growth` (not
  just the 3 named): `qing_nw_columbia_country`, `qing_oc_new_zealand`, `qing_oc_queensland`,
  `qing_col_golden_shore`, `qing_col_new_holland_settled`, `qing_nw_alta_california_mod` — each granted
  once, permanently (`duration = -1`), on a colonization mission's `on_completion`, in
  `common/modifiers/qing_colonization_modifiers.txt`.
- **Verdict: NOT orphaned, no fix needed.** These differ structurally from #88's actual bug in the one
  way that matters: `global_population_growth` is a REAL, always-live VANILLA engine modifier key
  (confirmed used the same way in `00_hardcoded.txt` and both oracle mods) that the engine applies
  directly to the country's population-growth RATE every tick — it is not a mod-invented flag nobody
  reads. The #369 pressure meter's own crowding driver reads `total_population` DIRECTLY at country
  scope (`QING_pop_recompute_target`, se_QING_POPULATION.txt:60-88) — any extra growth these 6 modifiers
  cause flows straight into the one number the meter already watches. There is no parallel/duplicate
  population-relief CONCEPT here the way `qing_newworld_agriculture` duplicated the golden-crop relief
  term; these are ordinary flavor-reward growth boosts that were never meant to be a pressure-meter INPUT
  in the first place, and mechanically they already are one (via total_population), just not by name.
  #88's bug was a modifier the pressure system needed to know about but couldn't see; these are
  modifiers the pressure system already "sees" through the population count itself.
- Also confirmed (per #88's own review correction) that `qing_nw_puget_sound`, previously miscited as a
  4th orphan, does NOT carry `global_population_growth` — it's a commerce/naval-range-only modifier, so
  there was never anything to check there.
- No code change. **STATUS: DIAGNOSED — audit complete, no defect found, closing #53.**

### Task #55 — verify subject_add_to_customs_union_federation loc in-context — VERIFIED CLEAN (no defect)
- Follow-up from #40's review, which flagged this loc key (duplicated verbatim across
  `00_subject_rework_l_english.yml:97` and `trade_actions_l_english.yml:57`) as worth checking in-context
  since it uses a DIFFERENT scope chain (`ROOT.GetCountry.MakeScope.GetVariable('member_of_federation')`)
  from the `ROOT.MakeScope` bug #40 actually fixed, and the boot log never exercises it.
- Traced the full mechanism: `common/customizable_localization/subject_interactions_custom_loc.txt`'s
  `customs_union_button_tooltip` selector picks this loc variant when `any_governorships = { has_variable
  = federation_customs_union }` passes on the OVERLORD. The loc text itself reads `member_of_federation`
  on the SUBJECT's own country (`ROOT.GetCountry` — `ROOT` in a `type = country` custom_loc block IS the
  country being interacted with) — confirmed via `se_federation.txt:42-47` that `member_of_federation` is
  genuinely set as a COUNTRY-scope var (not a stray/wrong-scope reference) on every federation member,
  pointing at `scope:federation_scope` — confirmed at `se_federation.txt:9-13` that this scope is
  literally a PROVINCE (the federation's "capital" holding province) — so
  `.GetProvince.MakeScope.Var('federation_name')` in the loc string is the CORRECT chain, matching the
  var's actual stored type exactly. No `ROOT.MakeScope`-class defect here; internally consistent.
- Checked the newest boot log: zero errors for `member_of_federation`/`federation_name`/this loc key (one
  unrelated benign "set but never used" note for `federation_name` elsewhere, not a runtime failure).
  Confirmed this is genuinely unverifiable live from THIS boot — the federation-customs-union mechanic is
  a vanilla Western-power feature (German Confederation etc.), never exercised by a CHI-focused session,
  and confirmed both loc files are vanilla base-game loc carried forward by the mod (not mod-authored
  Qing content) — the duplicate key across 2 files is harmless (same string, last-load wins per PDX
  convention), not a functional bug.
- No code change. **STATUS: VERIFIED CLEAN — closing #55, no defect found.**

### Task #54 — INCOME_sell_reserves unit mismatch for CHI — MISDIAGNOSIS, closed (no fix)
- The original #23 diagnosis pass claimed `INCOME_sell_reserves` (se_INCOME.txt:716-761) mixes units for
  CHI: depletes `silver_reserve_size` (labeled "千兩" in a seeding comment) but prices/credits using
  `global_base_import_price_silver` (labeled "hundreds-lb"), and pollutes `silver_stockpile` with the
  raw number. Dispatched a dedicated verification agent (research-only, no edits) to confirm or refute
  before writing a fix, given the severity framing ("real economic bug, not display").
- **Verdict: misdiagnosis, matching #23's own "not a bug" pattern.** `silver_reserve_size` is ONE engine
  variable seeded identically for every country (GBR=7, FRA=0, CHI=62000, etc.) via the same
  `CURRENCY_country_setup_reserves` macro, and read by the SAME uniform backing-value formula
  (`CURRENCY_update_backing_value`, se_CURRENCY.txt:1996/2018) with zero country-specific branching
  anywhere. The "千兩" comment is a MASS-EQUIVALENCE relabeling, not a different scale: the mod's own
  sourcing states 100 troy-lb ≈ 1000 kuping taels (both ≈37.3kg of silver) — so CHI's 62000 genuinely IS
  62000 of the SAME engine unit every other country uses, just a historically much larger hoard (per
  #372/#425's own research), not a rescaled number needing conversion. `INCOME_sell_reserves`'s three
  operations (deplete reserve / credit treasury / credit stockpile) are tautologically unit-consistent
  by construction for every country: `amount_to_sell = deficit / global_base_import_price_$metal$`, so
  `price × amount_to_sell = deficit` exactly, with no cross-unit multiplication anywhere, and the
  stockpile credit uses the same global price unit the trade system already values that stockpile at.
- One genuinely minor, non-functional finding logged but not worth its own fix: the CHI seeding block's
  two adjacent lines (`silver_reserve_size` labeled "千兩", `silver_reserve_accumulation_rate` on the
  next line labeled "hundreds lb") use inconsistent comment labels for the same variable family — almost
  certainly what seeded the original misdiagnosis's suspicion. A one-line comment clarity fix, not a
  functional issue; not actioned as its own task since it's purely cosmetic.
- No code change. **STATUS: MISDIAGNOSIS — closing #54, no defect found** (same resolution class as #23).
