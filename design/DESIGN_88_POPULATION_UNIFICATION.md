# DESIGN — #88 unify frontier-settlement + NW pop-boom + Population/Famine into one system

> STATUS 2026-08-13: REVIEW ROUND 4 — CLEAN, ready to implement. Round 1 found the `-10` magnitude
> analogy to the golden-crop relief term questionable (gated behind a risky, RNG-contingent path that
> can fail and backfire; the settle-mission's path is deterministic and risk-free) and 2 stale loc
> strings — both fixed. Round 2 found the round-1 fix INCOMPLETE (prose still argued the old `-10`
> case) — fixed. Round 3 (autonomous, per this run's no-stopping-to-ask discipline) resolved both
> remaining open questions. Round 4 found round 3's "empty modifier body" choice would display a
> named, described, effect-free modifier to the player (a visible wart) — replaced with the silent
> `set_variable`/`has_variable` flag idiom already proven at `qing_frontier_resettlement`
> (`se_QING_POPULATION.txt:117/282`); also fixed 3 LOW doc-accuracy nits (stale mission comment, a
> mischaracterized overseas-modifier claim, this banner). Supersedes the withdrawn
> `DESIGN_88_POPULATION_UNIFICATION_STATUS.md` (reverted per user correction: that draft wrongly
> concluded the systems were already unified based on a surface check — it never actually traced
> whether the #65 mission reward and the #369 pressure meter read each other's state, and they do
> not).

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:44`: "UNIFY frontier-settlement + NW pop-boom +
Population/Famine into one system (Population & Famine window)."

## The actual defect (confirmed by tracing every read/write site, not just checking for a GUI link)

`se_QING_POPULATION.txt`'s `QING_pop_recompute_target` (task #369, the standing Malthusian pressure
meter) already reads the NARRATIVE crop-boom chain's state — `qing_newworld_crops`,
`qing_migr_crop_boom_golden` — as an involution term (+18 pressure if the boom fired but didn't go
golden, `:92-100`) and a relief term (-10 if golden, `:134-137`). That part is genuinely coupled.

But task #65 ("flesh out the NW pop-boom — generic farmstead + settle-frontier mission beat",
shipped `beb75715c`) built a SECOND, entirely independent population mechanism that #369 has zero
awareness of:

- `qing_settle_newworld_crops` mission (`common/missions/qing_settle_frontier_missions.txt:487-505`)
  — allow-gated on owning >=3 `new_world_farmstead_building`s, grants `qing_newworld_agriculture`
  (a country modifier) on completion.
- `qing_newworld_agriculture` (`common/modifiers/qing_migration_modifiers.txt:112-115`, the
  removable effect lines at :113-114): a flat, PERMANENT `global_population_growth = 0.03` +
  `global_population_capacity_modifier = 0.03`.

This modifier is applied once (`duration = -1`) and never read by anything — confirmed by grepping
the whole repo for `qing_newworld_agriculture`: it appears ONLY at its own definition and at the one
`add_country_modifier` call. `QING_pop_recompute_target`'s crowding/involution/relief-valve math
(`:52-142`) has no term for "has the player completed the settle-frontier mission," no term reading
`qing_newworld_agriculture`, nothing. So a player who builds farmsteads and completes the mission
gets a permanent, silent population boost that the pressure meter never sees coming and never
credits as a relief valve — exactly the "two silos" defect: both systems independently model "New
World crops affect population," neither aware the other exists.

## User ruling (this session): FULLY FOLD, don't just cross-read

Retire `qing_newworld_agriculture`'s standalone `global_population_growth`/
`global_population_capacity_modifier` effect. Route the mission's reward through the `qing_pop_pressure`
system instead, as a relief-valve term, so there is ONE population mechanic, not two running in
parallel.

## The fold (concrete change) — REVISED round 4 per adversarial-review findings (both MEDIUM issues
## fixed: the empty-modifier display wart, and an explicit statement that the vanilla-engine
## capacity effect is REMOVED, not re-homed, since the custom pressure meter has no capacity term)

1. **Retire the modifier reward; use a silent flag instead (fixes the "empty modifier displays as a
   do-nothing effect" finding).** Round 3 proposed keeping `qing_newworld_agriculture` as an empty
   modifier body, citing `qing_migr_crop_boom_golden` as precedent — review found that citation false
   (`_golden` carries 5 real effects, it is never empty) and found a cleaner idiom ALREADY live in
   this exact function: the frontier-resettlement relief valve is gated on
   `has_variable = qing_frontier_resettlement` (`se_QING_POPULATION.txt:117`), a silent flag with NO
   loc name, NO description, and NO active-modifiers-list display. Adopt the same idiom here:
   - `common/missions/qing_settle_frontier_missions.txt:503`: change
     `add_country_modifier = { name = qing_newworld_agriculture  duration = -1 }` to
     `set_variable = { name = qing_newworld_agriculture  value = 1 }`.
   - `common/modifiers/qing_migration_modifiers.txt:112-115`: DELETE the `qing_newworld_agriculture`
     modifier definition entirely — no modifier object is needed once nothing declares it as a
     country-modifier reward.
   - `localization/english/qing_migration_l_english.yml:81-82`: DELETE the
     `qing_newworld_agriculture`/`_desc` loc keys — no modifier name/desc to display once it is a
     silent variable, not a modifier.
   - `common/missions/qing_settle_frontier_missions.txt:480-485`: update the comment block, which
     currently still describes the removed effect ("a permanent empire-wide carrying-capacity +
     growth lift... reward = the `qing_newworld_agriculture` country modifier") — reword to describe
     the pressure-relief flag this fold replaces it with (review finding: an implementer following
     only the numbered edits below would leave this comment stale and wrong).
2. **`QING_pop_recompute_target`** (`se_QING_POPULATION.txt:52-142`): add ONE new relief-valve term,
   in the same "- RELIEF VALVES" section as the existing frontier-resettlement/golden-crop terms
   (`:114-137`), gated on the new flag (`has_variable`, matching the frontier-resettlement precedent's
   own gate type exactly, NOT `has_country_modifier`, since step 1 makes this a variable):
   ```
   # --- - NEW WORLD AGRICULTURE (settle-frontier mission #65 reward): the realm has organized New
   # World crop cultivation across its farmsteads. NOTE: this REPLACES the mission's old standalone
   # global_population_growth/global_population_capacity_modifier effect — the custom qing_pop_
   # pressure_target has no capacity term of its own (its crowding driver is a fixed total_population
   # /1200 ratio, :86-87), so the old vanilla-engine capacity lift is not "re-homed" here, it is
   # RETIRED; this pressure-meter credit is the mission's entire replacement reward, not an addition
   # to a capacity effect that still exists elsewhere.
   if = {
       limit = { has_variable = qing_newworld_agriculture }
       change_variable = { name = qing_pop_pressure_target  subtract = 6 }
   }
   ```
   Magnitude `-6` chosen BELOW the golden-crop relief term's own `-10` (`:136`), per the round-1
   review finding: the golden-crop path is gated behind a risky, RNG-contingent chain
   (`qing_migration.20/.21`) that can fail and instead grant a MALUS (`qing_migr_overpopulation`),
   while the settle-frontier mission's path (`treasury >= 60` + owning >=3 farmsteads) is
   deterministic and risk-free — a guaranteed build-and-spend task with no failure branch. Equal
   weighting would over-reward the strictly-easier, risk-free path. `-6` sits below every existing
   relief-valve term in this function (frontier-resettlement `-12`, frontier-settle-law `-8`/`-16`,
   golden-crop `-10`) — a deliberately smaller credit for the deterministic path. OVERNIGHT
   ASSUMPTION per the original #65 design's own convention; boot-tune against pop logs like every
   other term in this function already is.

This is the "fully fold" shape the user specified: the mission's population effect no longer exists
as an independent flat bonus anywhere — it exists ONLY as one more input to the single
`qing_pop_pressure_target` calculation, alongside crowding, involution, granary stress, and the other
relief valves. A player who completes the mission sees it move the SAME meter the famine/resettlement
levers move, not a silent separate stat, and does NOT see a named, described, empty modifier sitting
inertly in their active-modifiers list.

## Why this is the correct fold point, not a different one

`QING_pop_recompute_target` is already the SINGLE function every other piece of this Malthusian
system routes through (crowding, involution, granary stress, frontier-settlement law bias, golden-crop
relief) — it is the established "all population-pressure inputs land here" chokepoint, per #369's own
header comment ("LAYER, DON'T DUPLICATE... owns no new meter machinery"). Adding the #65 term here,
in the same shape as its nearest peer (golden-crop relief), is the minimal, idiom-consistent fix — not
a new pipeline, not a second meter, not a GUI change (the panel already reads `qing_pop_pressure`;
crediting one more input to that same meter requires no panel change at all).

## What this does NOT touch

- `new_world_farmstead_building` itself (`00_infrastructure_buildings.txt`) — its LOCAL effects
  (`local_population_capacity_modifier`, `local_lower_strata_output`, `local_monthly_food`) are a
  separate, correctly-scoped per-province mechanism (the player-built structural coupling #65's design
  doc describes) and are NOT part of this fold — only the mission's EMPIRE-WIDE completion reward is.
- `qing_nwcrop_abundance` (the automatic per-province capacity stamp, `se_QING_COLON.txt`) — untouched,
  a different, already-correctly-scoped mechanism.
- The narrative event chain (`qing_migration.20-.23`) and its existing #369 coupling — untouched,
  already correctly folded.
- The government_view.gui discoverability question from the withdrawn prior draft — NOT part of this
  design. If a genuine discoverability gap exists it is a separate, narrower follow-up; this doc
  focuses solely on the silo the user identified.

## Loc fix (review round 1 finding, folded in)

Two localization strings named the population-growth/capacity effect this fold removes and were
missed from the original change list:
- `qing_newworld_agriculture_desc` (`localization/english/qing_migration_l_english.yml:82`) — was
  "...A lasting lift to carrying capacity and growth." Reworded to "Eases the pressure of the
  realm's swelling millions on its finite fields" — matching the fold's actual mechanism (a
  pressure-relief term) rather than the removed standalone growth/capacity claim.
- `qing_settle_newworld_crops_tt` (`localization/english/qing_settle_frontier_l_english.yml:99`) —
  the mission's own completion tooltip, was "carrying capacity and population growth rise
  empire-wide..." Reworded to "population pressure eases empire-wide..." for the same reason.

## Resolved (round 3, decided here — no reviewer available mid-run, per this run's own discipline)

**Q1 — should `qing_newworld_agriculture` retain a standalone effect?** Decision: **no standalone
effect — retired to a silent flag, per "The fold" section above (revised round 4).** Rejected
alternative 1: mirror `qing_migr_crop_boom`'s `global_tax_modifier = 0.05` companion term. Not chosen
because `qing_migr_crop_boom`'s tax term models a DIFFERENT thing — a sudden windfall harvest raising
taxable surplus in the SAME tick the boom fires (a narrative, one-shot event payload) — whereas the
settle-frontier mission is the COMPLETION marker of a deliberate, already-treasury-costed action
(`treasury >= 60` is the mission's own price of admission, per
`qing_settle_frontier_missions.txt:487-505`, and the mission's own `on_completion` already grants
`current_ruler = { add_popularity = 12 }` + `add_stability = 1`, :504-505). Adding a further
standalone modifier reward on top would double-reward the same action outside this fold's stated
scope. Rejected alternative 2 (round 3's original call): keep `qing_newworld_agriculture` as an
EMPTY country-modifier body, citing `qing_migr_crop_boom_golden` as precedent. Adversarial review
(round 4) found this citation false — `_golden` is never empty, it carries 5 real effects — and
found no genuine precedent anywhere in this codebase for a deliberately empty modifier; an empty
modifier would still display a named, described entry with zero listed effects in the player's
active-modifiers list, reading as a bug. Replaced with the flag idiom (`set_variable`/`has_variable`)
already proven at `qing_frontier_resettlement` (`se_QING_POPULATION.txt:117`) for this EXACT
shape — a silent completion marker with no display artifact.

**Q2 — are there other orphaned one-shot population modifiers of this shape?** A full grep of
`common/modifiers/qing_migration_modifiers.txt`, `qing_population_modifiers.txt`, and
`qing_settle_frontier_modifiers.txt` for every modifier carrying `global_population_growth`,
`global_population_capacity_modifier`, or `local_population_capacity` was cross-checked against
`se_QING_POPULATION.txt`'s full read-list (`has_country_modifier` and `has_global_variable` checks
in `QING_pop_recompute_target`, `:52-142`, PLUS `QING_pop_pulse` which also reads narrative-chain
modifiers, `:179-180`). Result, within this fold's own three named files: **`qing_newworld_agriculture`
is the only orphan.** `qing_migr_crop_boom_golden` is read at `:97`/`:135` (the involution/relief
terms this doc's opening section documents); `qing_migr_crop_boom`/`qing_migr_overpopulation` are
read at `:179-180` inside `QING_pop_pulse` (a different function in the same file, also part of the
existing, correctly-folded coupling). `qing_nwcrop_abundance` (`qing_migration_modifiers.txt:70-72`)
is a PROVINCE-scope capacity stamp applied automatically by `QING_COLON_apply_nwcrop_capacity` every
relevant tick, not a one-shot country reward with a completion moment to credit — it has no
analogous "did this fire" flag to fold in, and is explicitly out of scope per "What this does NOT
touch" above. No other modifier in the three named files matches the shape (one-shot country-scope
population effect, unread by the pressure meter).

**Scope note added (review finding): this "only orphan" claim is scoped to the frontier-settlement/
NW-crop cluster's own three modifier files, not mod-wide.** An independent, whole-directory sweep of
`common/modifiers/` found FOUR other never-read, one-shot mission-reward modifiers in the UNRELATED
overseas-colonization subsystem (`qing_colonization_modifiers.txt`) — `qing_nw_columbia_country`
(`global_population_growth = 0.03`), `qing_oc_new_zealand` (`global_population_growth = 0.05`),
`qing_oc_queensland` (`global_population_growth = 0.04`), and `qing_nw_puget_sound` (review
correction: this one does NOT carry `global_population_growth` — it is
`global_commerce_modifier = 0.04` + `naval_range = 0.03` — so it is a never-read orphan of a
DIFFERENT, non-population shape, not a population sibling to the other three). These are correctly
OUT OF SCOPE for this design — task #88 named "frontier-settlement + NW pop-boom +
Population/Famine," not the overseas-colonization tree, and folding them here would silently expand
scope into a different subsystem with its own missions/modifiers file. Logged here loudly rather
than silently omitted: task #53 tracks auditing whether the overseas-colonization subsystem has (or
needs) its own version of the `qing_pop_pressure` coupling this design builds for the
frontier-settlement cluster, and separately whether any of its non-population orphans (like Puget
Sound) need their own fold.
