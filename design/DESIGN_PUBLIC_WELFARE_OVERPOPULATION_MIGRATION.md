# DESIGN — flesh out Public Welfare (Poor Law) spending, tie into overpopulation + migration

> STATUS 2026-08-20: DRAFT v1 — design only, not implemented.

## Current state (read directly, not inferred)

Public Welfare is vanilla Imperator's Poor Law spending, gated on the `local_poor_laws` law
(`common/laws/00_social_laws.txt:274-284`, modifier: lower/proletariat happiness +0.1, upper -0.1,
middle -0.05). Mechanically (`common/script_values/INCOME_svalues.txt:1300-1370`):

- Each governorship's lower-strata/proletariat pops have a cost-of-living figure. If actual income
  falls short, that shortfall is the welfare gap.
- `INCOME_public_welfare_spending_rate` (a player slider, 25/50/75/100%) sets what fraction of the
  gap the treasury covers, paid straight onto the pops' wealth (`INCOME_lower_strata_poor_law_due`
  et al.).
- Total quarterly cost (`INCOME_cost_public_welfare` -> `INCOME_cost_poor_law_spending`) is the
  Economy tab's "Public welfare" expense line.
- Two open `TODO`s in the file (:1314, :1317): welfare income is not yet folded into the pop-wealth
  tooltips or the national-income tooltip. `INCOME_cost_public_welfare`'s own comment (:1369) flags
  it was meant to grow to cover "public healthcare, subsidies" -- never added.

## Finding 1 — the migration tie-in ALREADY EXISTS, but is invisible

`MIGRATION_wealth_relative_province` (`common/script_values/MIGRATION_svalues.txt:105-124`) reads
`governorship.WEALTH_governorship_per_capita` against the national per-capita average; a governorship
poorer than average produces a NEGATIVE deviation, and `MIGRATION_push_province`
(`MIGRATION_svalues.txt:135-217`) sums that deviation ("only the poor-half pushes... impoverishment
-> emigration pressure") into the province's emigration push score.

Poor Law spending writes DIRECTLY into `lower_strata_wealth`/`proletariat_wealth`
(`WEALTH_distribute_new_wealth`'s siblings feed `WEALTH_governorship_per_capita`), so **turning up
the welfare spending rate already, today, raises governorship per-capita wealth and reduces
emigration push from that governorship** -- through the ordinary wealth pipeline, with zero new
code. This is a real causal link, not a proposal.

The problem is it is completely invisible to the player: nothing in the Public Welfare tooltip, the
migration panel, or the Poor Law's own modifier mentions this. **Recommended fix (small, no new
mechanic): surface it.** Add a line to `PUBLIC_WELFARE_EXPENSE_TT` (added this session,
`localization/english/economic_enchancement_l_english.yml`) noting welfare spending eases emigration
pressure from poor governorships, and/or a `MIGRATION_push_province` tooltip breakdown line reading
the wealth-deviation term so the player can see welfare's effect on it directly.

## Finding 2 — overpopulation has NO existing tie-in; this is a real gap

`qing_pop_pressure_strain` (`common/modifiers/qing_population_modifiers.txt:20-24`: global_unrest
+1, global_population_growth -0.05, global_tax_modifier -0.05) and the stronger
`qing_migr_overpopulation` band (`common/modifiers/qing_migration_modifiers.txt:52-57`:
global_population_growth +0.05 [sic -- a Malthusian crisis band, see its own "weak dynasty" comment],
local_monthly_food_modifier -0.10, global_population_happiness -1, global_tax_modifier -0.05) are
driven by `MIGRATION_pop_overcapacity_overflow` (province pop above its readable ceiling) -- a
CAPACITY measure, not a WEALTH measure. Public Welfare (a wealth transfer) has no read on capacity
at all, so it does nothing for overpopulation today. This is the genuine gap to design, not an
already-existing-but-hidden link like Finding 1.

### Proposed new tie-in: welfare eases the SOCIAL cost of overpopulation, not the capacity itself

Historically, poor relief (荒政/賑濟, the same tradition `qing_pop_pressure_strain`'s Hong Liangji
citation gestures at) never raised the land's carrying capacity -- it kept an overcrowded populace
fed and quiet while the capacity problem was solved some other way (reclamation, migration, new-world
crops -- the mod's OWN `qing_migr_crop_boom`/capacity-lift mechanic, `qing_migration_modifiers.txt:59-67`).
So the correct tie-in is: **Public Welfare should NOT reduce overpopulation itself, but SHOULD dampen
the unrest/happiness penalty an overpopulated governorship pays**, representing the state actively
relieving the crowded poor rather than leaving them to riot.

Concrete mechanism (mirrors the ALREADY-PROVEN "counter-only, clamped, idempotent-safe" pattern this
codebase uses for exactly this kind of passive per-pulse dampening -- e.g. `QING_dynasty_harmony_nudge`
callers): a new small modifier fold, applied on the SAME quarterly pulse that recomputes
`qing_pop_pressure_strain`/`qing_migr_overpopulation`, scaled by `INCOME_public_welfare_spending_rate`
AND gated on `has_law = local_poor_laws` (no law, no effect -- matches the base mechanic's own gate):

- At 100% welfare spending under an active Poor Law, halve the unrest penalty of whichever
  overpopulation band is live (`qing_pop_pressure_strain`'s +1 global_unrest -> +0.5;
  `qing_migr_overpopulation`'s -1 global_population_happiness -> -0.5), scaling linearly with the
  0-100% slider. Population GROWTH and food penalties are left untouched -- welfare buys calm, not
  more capacity or more food, which is the historically correct boundary (a granary/reclamation
  problem needs a granary/reclamation fix, not a wealth transfer).
- Implementation shape: a `QING_welfare_overpopulation_relief` effect, called from wherever
  `qing_pop_pressure_strain`/`qing_migr_overpopulation` are (re-)applied (find via
  `has_country_modifier = qing_migr_overpopulation`, se_QING_POPULATION.txt:195/324), which
  remove-then-reapplies a SECOND, additive counter-modifier (never edits the band modifiers
  themselves, so the base Malthusian mechanic stays untouched and this stays a pure toggleable
  overlay) sized off the welfare rate.

## Finding 3 — the two open TODOs (tooltip integration) should close alongside this

- `INCOME_svalues.txt:1314` (no `WEALTH_income_total_POPTYPE` including welfare for
  lower_strata/proletariat tooltips) and `:1317` (welfare missing from the national income tooltip)
  are small, mechanical gaps -- once Finding 1's tooltip surfacing is done, these should be closed in
  the same pass so the player can see welfare's wealth effect in the SAME places they see everything
  else (pop wealth breakdown, national income breakdown), not just the Economy tab's own expense line.

## Finding 4 — the missing categories (healthcare, subsidies)

`INCOME_cost_public_welfare`'s own comment (`INCOME_svalues.txt:1369`) flags this as intended scope
never built. Recommend treating this as a SEPARATE, later design (a healthcare category plausibly
ties into the mod's existing epidemic/health mechanics if any exist; a subsidies category into the
manufactured-goods demand-support mechanics) rather than bolting it onto this pass -- Findings 1-3
are the concrete, evidenced work; healthcare/subsidies need their own scoping pass to find what
existing mechanics (if any) they should hook into, the same way Findings 1-2 did here.

## Open questions for review
1. Is a flat linear 0-50% dampening (at 100% welfare spending) the right magnitude, or should it
   scale with HOW overcrowded the province is (i.e. read `MIGRATION_pop_overcapacity_overflow`
   directly rather than a flat band-halving)?
2. Should the dampening also touch `global_tax_modifier` (both bands carry -0.05), or is unrest/
   happiness alone the right scope (tax relief reads more like a capacity/growth fix, arguably out
   of welfare's proper boundary per Finding 2's own reasoning)?
3. Finding 1's tooltip surfacing -- exact wording/placement -- needs a pass once this is scheduled.
