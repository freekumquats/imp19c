# DESIGN — #88 unify frontier-settlement + NW pop-boom + Population/Famine into one system

> STATUS 2026-08-12: REVIEW ROUND 2 — NOT CLEAN, 1 finding fixed below. Round 1 found the `-10`
> magnitude analogy to the golden-crop relief term questionable (that term is gated behind a risky,
> RNG-contingent path that can fail and backfire; the settle-mission's path is deterministic and
> risk-free) and 2 stale loc strings — both fixed in round 1's pass. Round 2 found the round-1 fix
> was INCOMPLETE: the code snippet was correctly changed to `-6`, but the prose rationale paragraph
> and an open question below it still argued the old `-10` equal-weighting case verbatim,
> contradicting the code and the STATUS banner. Fixed: rationale paragraph rewritten to justify `-6`
> directly; stale open question replaced with a resolved-note. Re-review needed before
> implementation. Supersedes the
> withdrawn `DESIGN_88_POPULATION_UNIFICATION_STATUS.md` (reverted per user correction: that draft
> wrongly concluded the systems were already unified based on a surface check — it never actually
> traced whether the #65 mission reward and the #369 pressure meter read each other's state, and
> they do not).

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
- `qing_newworld_agriculture` (`common/modifiers/qing_migration_modifiers.txt:108-113`): a flat,
  PERMANENT `global_population_growth = 0.03` + `global_population_capacity_modifier = 0.03`.

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

## The fold (concrete change)

1. **Modifier `qing_newworld_agriculture`** (`qing_migration_modifiers.txt:108-113`): remove
   `global_population_growth = 0.03` and `global_population_capacity_modifier = 0.03`. The modifier
   itself is KEPT as a marker (a `has_country_modifier` check is the cheapest, already-proven idiom
   this file uses everywhere else to record "has this one-shot reward fired" — e.g.
   `qing_migr_crop_boom_golden` is checked the identical way at `se_QING_POPULATION.txt:97/135`), but
   it becomes an EMPTY modifier body (a pure flag object), or optionally retains a small NON-population
   effect if the reviewer judges the mission needs SOME standalone flavor (e.g. a modest
   `global_commerce_modifier`, mirroring how `qing_migr_crop_boom`/`_golden` also carry a commerce/tax
   term alongside their population term) — open question below, not decided here.
2. **`QING_pop_recompute_target`** (`se_QING_POPULATION.txt:52-142`): add ONE new relief-valve term,
   in the same "- RELIEF VALVES" section as the existing frontier-resettlement/golden-crop terms
   (`:114-137`):
   ```
   # --- - NEW WORLD AGRICULTURE (settle-frontier mission #65 reward): the realm has organized
   # New World crop cultivation across its farmsteads — a structural capacity gain the pressure
   # meter should credit exactly like the golden-crop relief above, not silently outside it.
   if = {
       limit = { has_country_modifier = qing_newworld_agriculture }
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
levers move, not a silent separate stat.

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

## Open questions for review
- Should `qing_newworld_agriculture` retain ANY standalone effect (e.g. a small commerce/tax term,
  mirroring `qing_migr_crop_boom`'s own commerce term) once its population effect is removed, or
  should it become a pure empty marker? Either is defensible; needs a reviewer call, not left silently
  decided by omission.
- (Resolved round 1: `-6`, below the golden-crop term, per the risk/effort asymmetry finding — see
  the magnitude rationale above. Still an OVERNIGHT ASSUMPTION, boot-tune against pop logs like
  every other term in this function.)
- Confirm there is no OTHER silo of this shape elsewhere in the population/migration/famine cluster
  that this pass should also catch (i.e., is `qing_newworld_agriculture` the ONLY orphaned modifier of
  this kind, or does a broader grep for other one-shot population-affecting modifiers turn up
  siblings this design should also fold in the same pass).
