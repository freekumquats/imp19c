# DESIGN #101 — Cottage Industry as real, rural-only buildings (REVISED v5)

> STATUS 2026-08-13: DRAFT v5. Supersedes v4 — an adversarial review found v4's own "direct
> verification" of v3 was itself wrong (see corrected section below), found a real GUI defect that
> would have defeated the niche in the macro builder, found two reader-list undercounts (repeating
> the exact defect class v4 already fixed once for stone), an invalid trigger-syntax shorthand, an
> unproven fractional `base_resources` value, and confirmed the stacking-exploit open question has a
> real answer (no cap exists) rather than remaining open. All fixed below. The core mechanism
> (job-slot omission as the niche) survives review and is UNCHANGED; only its justification, the
> GUI wiring, two reader lists, one syntax detail, one numeric risk, and the stacking question are
> corrected.

## What was wrong with v4's own "verification" of v3 (do not repeat — corrected here)

v4 claimed *"Every existing raw-good building in this mod is buildable from turn one, with no tech
prerequisite whatsoever"* and that v3's invention-gate niche "never existed." **This is false and
contradicts v4's own v2-section three lines later** (which correctly states `IND_resource_
gathering_operation` "needs only `tech_construction`"). Re-verified directly:
- `IND_resource_gathering_operation`: `owner = { invention = tech_construction }`
  (`00_industrial_buildings.txt:36`).
- `row_manufactory_building`: `owner = { invention = tech_manufactories }`
  (`row_production_buildings.txt:62`).
- `row_plantation_building`: `owner = { invention = tech_construction }`
  (`row_production_buildings.txt:110`).
- Only the SIX QING WORKS genuinely have no invention gate (`qing_production_buildings.txt`, all
  six `allow` blocks checked — confirmed, no `invention` key present in any).

So v3's niche ("no invention required") was real for 3 of the 9 comparison buildings
(`IND_resource_gathering_operation` and both ROW generics) — it only failed against the six
Qing works, which v3's own review round had already flagged specifically. v4 over-corrected a
partially-valid finding into a false blanket one. This matters because it means the job-slot niche
below is not REPLACING a nonexistent invention-gate advantage — for 3 of 9 siblings, cottage
buildings get BOTH advantages (no invention gate AND no job-slot requirement); for the six Qing
works, only the job-slot advantage applies. The niche argument below is stated to hold regardless of
which siblings have an invention gate, so this correction does not change the fix, only the
(previously false) supporting narrative.

## The real niche (v5, mechanism unchanged from v4): cottage buildings do not require sufficient_job_slots

`sufficient_job_slots` (`common/scripted_triggers/00_buildings_scripted_triggers.txt:1-6`,
`JOBS_available_slots > 0`) is the ONE shared gate every existing raw-good building's `allow` block
requires to be BUILT at all (the six Qing works, both ROW generics, `IND_resource_gathering_
operation` — confirmed, all nine). **Cottage buildings omit `sufficient_job_slots` from their own
`allow` block entirely**, so they remain buildable when `JOBS_available_slots <= 0` — the one
situation where every existing raw-good building becomes unbuildable.

**Corrected mechanism detail (review finding, fixed): this is a shared GATE, not necessarily a
shared CONSUMPTION, and the design no longer claims otherwise.** `JOBS_available_slots =
JOBS_buildings_cap - JOBS_non_subsistence` (`JOBS_svalues.txt:449-452`), and `JOBS_non_subsistence`
(`:325-339`) sums only `JOBS_industrial_workers` (`num_of_IND_industrial_estate`), `JOBS_resource_
gatherer` (`num_of_IND_resource_gathering_operation`), `JOBS_military`, `JOBS_commercial`, `JOBS_
infrastructure_workers`, `JOBS_educators`, `JOBS_administrators`. The six Qing works and both ROW
generics are NOT in that sum — building one does not itself reduce `JOBS_available_slots` for later
buildings, even though building one REQUIRES `JOBS_available_slots > 0` at the moment it is built.
Only `IND_industrial_estate` and `IND_resource_gathering_operation` both require AND deplete the
pool. This does not change the niche's conclusion: in a province where `JOBS_available_slots` has
already reached 0 (typically via industrial estates, resource-gathering operations, military,
administrative, or commercial buildings), EVERY existing raw-good building — Qing works and ROW
generics included, even though they don't personally deplete the count — becomes unbuildable, while
a cottage building, gated on nothing but its `trade_goods`/culture/rural checks, remains buildable.
The niche holds; only the "consumes from the same pool" phrasing (v4's error) is withdrawn as
imprecise — the accurate claim is "gated by the same pool," not "depletes the same pool."

This is a genuine, structural, historically-grounded difference, not an invented timing gate:
cottage industry is household/family labor OUTSIDE the formal employment-slot economy (the
historical research's own core point — Philip Huang's "involutionary growth," more HOURS worked by
family members who are not counted as formal employees, not higher productivity per employed
worker). A rural province that has already filled every job slot can STILL add cottage buildings,
since they draw on labor the job-slot system was never modeling in the first place. This creates a
real "always-available top-up" niche that does not depend on timing, tech, or any temporary window —
cottage buildings remain useful for the ENTIRE game, in any rural province that has maxed out its
formal job-slot capacity but still has underemployed rural population, exactly matching the
historical economics this design is grounded in.

## What was wrong with v2 (do not repeat)

1. **The wrong sibling building was used to justify a rural niche.** v2 argued cottage buildings fill
   a gap `IND_industrial_estate` cannot (that building needs `tech_manufactories` +
   `civilization_value >= 30` + industry-capacity slots — genuinely unreachable early). But the TRUE
   raw-good sibling is `IND_resource_gathering_operation` (`00_industrial_buildings.txt:20-43`), which
   ALSO has no city gate and is FAR cheaper to unlock than v2 implied — it needs only `tech_
   construction` (`00_civic_inventions.txt:473-481`, itself requiring only `tech_metalworking`, an
   early tech) + `sufficient_job_slots`. At v2's own numbers (cheaper cost, LOWER output per gold and
   per pop-slot, same tech-tier reachability), a rational player never builds the cottage version —
   it was strictly dominated, not a genuine cheap fallback. **Fixed below: cottage buildings require
   NO invention at all** (buildable from game start, before `tech_construction` is researched) — THIS
   is the real, defensible niche: available immediately, at a real efficiency cost, not "cheap but
   unlocked at the same time as something strictly better."
2. **Bronze had zero coverage.** `COTTAGEIND_produce_bronze` reads only `raw_tin` + `raw_copper`
   (`se_COTTAGEIND.txt:439,443`) — no v2 building touched either raw good. **Fixed below: a 7th
   building added for copper+tin.**
3. **The ROW building was wrongly added to the macro allowlist**, reversing a documented exclusion
   (`00_default.txt:94`, "row_manufactory/row_plantation REMOVED... rest-of-world buildings"). **Fixed
   below: the ROW cottage building is NOT added to the macro builder's includes list** — matching its
   siblings' own precedent exactly, not contradicting it.
4. **"Two existing ROW siblings" was miscounted** — `row_production_buildings.txt` holds two
   buildings (`row_manufactory_building`, `row_plantation_building`), which was correct; the wording
   error was calling the file itself the sibling. Restated correctly below.
5. **No tech/invention gate was specified at all** in v2 — the single most important number, since it
   decides whether the building has any reason to exist. Fixed by point 1 above.

## What was wrong with v1 (do not repeat, unchanged from v2)

1. **`base_resources` boosts a RAW good's province output, not one finished good directly.**
   Confirmed by reading `GOODS_governorship_iron_produced` (`GOODS_svalues.txt:1592-1603`): it sums
   `num_goods_produced` across every province in the governorship assigned that ONE raw good (e.g.
   iron), then `COTTAGEIND_raw_iron` (`se_COTTAGEIND.txt:114-117`) caches that same value. A building
   with `base_resources` raises the PROVINCE's raw output. It cannot target "feed early_munitions
   only" — `COTTAGEIND_raw_iron` is read by `COTTAGEIND_produce_construction_materials`,
   `_early_artillery`, and `_steel` all at once (confirmed: `se_COTTAGEIND.txt:242,292,423`). v1's
   "one building, one Military-Supplies good" framing does not match this mechanism.
2. **"Factories are city buildings" is wrong.** `IND_industrial_estate` (`00_industrial_buildings.
   txt:1-18`), the generic factory-slot building, has NO `has_city_status` gate — confirmed by
   reading its `allow` block in full. Only the `URB_*` district buildings (commerce, administration,
   residential, cultural) require a city. v1 cited `IND_resource_gathering_operation`'s own
   `base_resources` precedent while ALSO claiming factories are city-only — those two claims
   contradict each other, since `IND_resource_gathering_operation` has no city gate either.

## Corrected mental model

- A **raw good** (iron, lead, wood, textile_fibres, silk, stone, copper, tin, vegetables, whales, ...)
  is a province-level `trade_goods` assignment. `num_goods_produced` is that province's raw output.
  Buildings with `base_resources` multiply it.
- A **manufactured good** (early_munitions, clothing, construction_materials, ...) is produced by a
  RECIPE reading several raw-good totals across the WHOLE governorship (`COTTAGEIND_produce_<good>`
  for the cottage pipeline; `INDUSTRY_production_<good>` for the factory pipeline, gated on
  `INDUSTRY_factories_assigned_<good>`). Neither pipeline has a building that produces a
  manufactured good directly — both work through the SAME two-step raw→recipe structure.
- Cottage buildings, correctly modeled, are RAW-GOOD buildings — the same shape as
  `IND_resource_gathering_operation` and the six existing Qing production works
  (`qing_silk_filature_building`, etc., all of which also boost a RAW good via `base_resources`,
  gated to one `trade_goods` value each). Cottage buildings are not a NEW building-to-good pattern;
  they are a CHEAPER, RURAL-ONLY variant of the EXISTING raw-good-building pattern, differentiated
  from the factory-side raw-good buildings (`IND_resource_gathering_operation`,
  `qing_*_workshop_building`) by cost/output ratio and a rural gate — not by which good they touch.

## Why rural-only, and why the job-slot-free niche makes this a REAL, permanent choice

Since `IND_resource_gathering_operation` has no city gate, cottage buildings cannot rely on
"rural-only" alone to matter — a player could otherwise just build the factory-tier raw-good building
in the countryside instead, since nothing stops it. The real, defensible niche is CAPACITY, not
timing: **cottage buildings omit `sufficient_job_slots` from their `allow` block** — the ONE shared
gate every factory-tier raw-good building (the six Qing works, both ROW generics, `IND_resource_
gathering_operation`) requires to BE BUILT, on the ONE finite, capped resource in a province's
building economy (`JOBS_available_slots`, depleted by industrial estates, resource-gathering
operations, military/administrative/commercial/infrastructure buildings — NOT by the Qing works or
ROW generics themselves, see correction above). A rural province whose job-slot pool has already
hit zero can STILL raise a cottage building for a further raw-good boost, where it could NOT raise
another factory-tier building of the same kind. This gives cottage buildings a PERMANENT reason to
exist alongside the stronger factory-tier option, for the entire game, in exactly the situation the
historical research describes: a province whose formal economy (job-holding pops) is already
saturated, but whose informal/household labor (family members outside the counted workforce) is not.
The rural gate then narrows this always-useful top-up option to the countryside specifically,
matching the literal "buildable outside cities" ask, while the factory-tier buildings (city or
rural, gated on job slots) remain the primary, higher-output choice everywhere they still have
capacity.

## Historical grounding (unchanged from v1, still correct — research pass 2026-08-13)

The "putting-out system" (*Verlagssystem*; Mendels' "proto-industrialization," 1969/1972;
Kriedte/Medick/Schlumbohm, *Industrialization Before Industrialization*, 1977) was never MORE
efficient than the factory — it survived on near-zero-opportunity-cost rural household labor and
near-zero fixed capital. Philip Huang's "involutionary growth" (內卷化): Qing rural handicraft output
rose from MORE HOURS WORKED, not higher productivity per hour. Pomeranz's *Great Divergence* frames
this as rational given China's cheap-labor, capital-scarce conditions.

Recommended ratio (unchanged): cottage buildings at roughly **40-60% of a factory-equivalent's build
cost**, producing roughly **15-30% of a factory-equivalent's per-building output**.

## Proposed cottage-industry building set (REVISED — raw-good buildings, not good-specific)

### Qing-specific named buildings

Each is a RAW-GOOD building (mirrors `qing_cotton_workshop_building`'s exact shape: `base_resources`,
strata `local_output`, `cost`, `time`, `potential`/`allow` gated on culture group + ONE `trade_goods`
value), differentiated from its factory-tier sibling ONLY by: (a) a `NOT = { has_city_status = yes }`
rural gate, (b) a lower `cost`/`base_resources` per the ratio above. Named for the historical craft,
not for a Military-Supplies good, since one raw good feeds many recipes:

1. **`qing_cottage_smithy_building`** (鄉村鐵匠鋪, Village Smithy) — raw good **iron**.
   `trade_goods = iron`. Feeds `COTTAGEIND_raw_iron`, read by `_construction_materials`,
   `_early_artillery`, `_steel` (confirmed, `se_COTTAGEIND.txt:242,292,423`) — a rural smithy
   plausibly touches all three crafts at once, which is historically apt (a village smith worked
   iron for tools, fittings, and simple arms alike, not one single end product).
2. **`qing_cottage_leadworks_building`** (鄉村鉛作坊, Village Lead Works) — raw good **lead**.
   `trade_goods = lead`. Feeds `COTTAGEIND_raw_lead`, read by `_early_munitions`, `_early_artillery`,
   `_glass` (`se_COTTAGEIND.txt:262,284,592`).
3. **`qing_cottage_weaving_hut_building`** (農家織屋, Peasant Weaving Hut) — raw good
   **textile_fibres**. `trade_goods = textile_fibres`. Feeds `COTTAGEIND_raw_textile_fibres`, read by
   `_clothing`, `_luxury_clothing`, `_luxury_furniture`, `_paper` (`se_COTTAGEIND.txt:455,471,544,
   682`). Cheapest of the set (textile handicraft needed almost no fixed capital historically).
4. **`qing_cottage_silk_reeling_shed_building`** (繅絲棚, Village Silk-Reeling Shed) — raw good
   **silk**. `trade_goods = silk`. Feeds `COTTAGEIND_raw_silk`, read by `_clothing`,
   `_luxury_clothing`, `_luxury_furniture`, `_silk_cloth` (`:459,483,535,660`).
5. **`qing_cottage_woodlot_building`** (鄉村伐木場, Village Woodlot) — raw good **wood**.
   `trade_goods = wood`. Feeds `COTTAGEIND_raw_wood`, read by `_construction_materials`,
   `_early_artillery`, `_furniture`, `_luxury_furniture`, `_paper`, `_gunpowder`
   (`:234,296,511,523,678,707`) — **and, in a coastal governorship only, also
   `_naval_supplies` (`:325`) and `_wooden_ships` (`:382`)** (review finding: the earlier count of
   6 readers omitted these two coastal-gated recipes). This is a real, disclosed side-effect, not a
   defect: a woodlot in a coastal governorship also lifts naval-supplies/wooden-ships output, which
   is historically apt (village woodlots supplied ordinary ship timber too) — noted here so it is not
   silently discovered later.
6. **`qing_cottage_herbalist_building`** (鄉村藥鋪, Village Herbalist) — raw good **vegetables**.
   `trade_goods = vegetables`. Feeds `COTTAGEIND_raw_vegetables`, read by `_pharmaceuticals`
   (`:604`) — this raw good has only the one cottage-eligible reader, so this building maps
   cleanly to a single craft, matching v1's original intent for this one case.
7. **`qing_cottage_founders_workshop_building`** (鄉村鑄坊, Village Founder's Workshop) — raw goods
   **copper and tin**, gated with an explicit `OR` block (review finding, fixed: an earlier draft
   wrote the invalid shorthand `trade_goods = copper OR tin`, which is not valid Jomini trigger
   syntax — the proven form, matching `row_manufactory_building`'s own multi-good gate
   (`row_production_buildings.txt:51-58`), is `OR = { trade_goods = copper  trade_goods = tin }`).
   Feeds `COTTAGEIND_raw_copper`/`COTTAGEIND_raw_tin`, read by `_bronze` (`:439,443`) and
   `_early_artillery` (`:289-290`, alongside iron/lead/stone/wood already covered by the smithy and
   woodlot) — **and, in a coastal governorship only, also `_naval_supplies` (`:331`) and
   `_wooden_ships` (`:386`)**, both of which read `COTTAGEIND_raw_copper` (review finding: an
   earlier draft claimed `_bronze` and `_early_artillery` were the ONLY readers of either raw good,
   which was wrong for copper by the same coastal-recipe omission as the woodlot above — tin has no
   such extra reader). Closes the bronze coverage gap v2 left open.

8. **`qing_cottage_quarry_building`** (鄉村採石場, Village Quarry) — raw good **stone**.
   `trade_goods = stone`. Feeds `COTTAGEIND_raw_stone`, read by `_construction_materials`,
   `_early_munitions`, `_early_artillery`, `_glass` (`se_COTTAGEIND.txt:238,254,286,588` — FOUR
   readers, not the two an earlier draft claimed; see "corrected coverage" below).

**Corrected coverage (v4 fix — do not repeat v3's stone gap):** v3 claimed stone needed no
building because its readers were "already covered by other buildings' overlap." This was wrong on
two counts: stone actually has FOUR cottage-eligible readers, not two (`_early_munitions` and
`_glass` were both missed); and more importantly, boosting iron/lead/wood/copper/tin raw-good
totals does NOT raise the STONE raw-good total itself — each raw good is a separate
`COTTAGEIND_raw_<good>` variable read independently by the recipes, not a shared pool. Roughly 280
matching lines (`grep -h 'trade_goods="stone"' setup/provinces/*.txt | wc -l`; a handful sit in
non-province template lines, so the true distinct-province count is somewhat lower, in the
high-200s) are assigned `stone` as their `trade_goods` — a substantial number either way. Without
building 8, every one of them has NO cottage-industry option at all, despite stone feeding four
different recipes. Building 8 closes this gap.

**Explicitly NOT built:** a dedicated building per finished good (v1's mistake), and the research's
"Merchant Collection Post"/"Porcelain Subcontractor" concepts (no existing building schema
precedent for a pure multiplier-on-other-buildings or a cross-building input dependency — flagged
as a follow-up, not built this pass).

### Generic ROW building (1)

**`row_cottage_workshop_building`** — one generic raw-good building for any non-Chinese state,
mirroring `row_manufactory_building`'s and `row_plantation_building`'s own breadth (both live in
`row_production_buildings.txt`; `potential` on an `OR` of `trade_goods`, not one named good per
building — deliberately lower granularity than the Qing set, matching those two siblings' own stated
design intent). `potential = { owner = { NOT = { OR = { country_culture_group = jurchen
country_culture_group = chinese_group } } }  NOT = { has_city_status = yes }  OR = { trade_goods =
iron  trade_goods = lead  trade_goods = textile_fibres  trade_goods = silk  trade_goods = wood
trade_goods = vegetables  trade_goods = copper  trade_goods = tin  trade_goods = stone } }` (the
`stone` term added in v4, matching Qing building 8 above — the same coverage gap applies to any
non-Chinese stone-assigned province). **Omits `sufficient_job_slots`**,
same as the Qing set, for the same reason: it is a permanent, job-slot-free top-up option, not a
temporary one — a rural non-Chinese province that has filled its job-slot capacity with
`row_manufactory_building`/`IND_resource_gathering_operation` can still add this on top.

## Cost / efficiency figures (unchanged ratio, now correctly attached to raw-good buildings)

Existing raw-good buildings for comparison: `IND_resource_gathering_operation` (cost 100,
`base_resources = 1`, `local_lower_strata_output = 0.7`); the six Qing works (cost 65-90,
`base_resources = 2-3`). Per the 40-60% cost / 15-30% output ratio against these (revised per
second-review finding — see the cost correction below):

- **Cost: 50 gold, time 150.**
- **`base_resources` contribution: 1, but the cost is revised UP from an earlier draft's 40 to 50
  gold (second-review finding, fixed here, not left as an open question): an earlier draft paired
  `base_resources = 1` — matching `IND_resource_gathering_operation`'s own value exactly — with a
  40-gold cost (40% of that building's 100), which meant the cottage building matched the factory
  sibling's raw-output-per-building for less than half the price and NO job-slot cost, dominating it
  on efficiency rather than trading efficiency for availability as intended. Since `base_resources`
  has no proven fractional-safe form (every shipped value in this codebase is a whole integer —
  `IND_resource_gathering_operation` = 1, every Qing/ROW work = 2-3, grep-confirmed, none fractional
  — and a fraction risks silent truncation to 0, a total-inertness failure this design will not ship
  unverified), the integer `1` is kept, and the COST is raised instead to restore a genuine
  trade-off: 50 gold is still a real discount off the 100-gold factory sibling (50%, at the low end
  of the original 40-60% band) but no longer makes the cottage building strictly cheaper AND
  equally efficient with zero downside. The niche remains capacity-availability (job-slot-free),
  layered on top of a real, non-dominant cost/output trade-off, not instead of one.
- Strata `local_output`: `local_lower_strata_output = 0.2`, `local_proletariat_output = 0.15` (roughly
  20-30% of `IND_resource_gathering_operation`'s 0.7/0.5 pair) — same strata, since this is still
  low-skill rural labor.
- `local_monthly_civilization`: omitted (0) — deliberately undistinguished, unlike the named Qing
  works' 0.002-0.006; a rural handicraft building should not meaningfully advance civilization the
  way a state-sponsored works does.
- **`allow`/`potential`: `sufficient_job_slots` is OMITTED entirely** (only the existing
  culture/rural/trade_goods gates remain) — this is the load-bearing gate this design's whole niche
  argument depends on (see "The real niche (v5)" above); every Qing building and the ROW generic
  share this same job-slot-free `allow` block. Whether each building specifies an invention gate is
  incidental to the niche (see "What was wrong with v4's own verification" above) — some of the
  factory-tier siblings have one and some don't, but none of the cottage buildings need one either
  way, since the niche is job-slot-freedom, not tech-timing.

These are starting figures for review, not a final balance pass.

## GUI wiring (new "Cottage Industry" category, both screens, directly above "Modern Industry")

1. `gui/shared/gui_templates.gui`'s `building_box` template: new `flowcontainer` section, copy-shaped
   from the `Modern Industry` section (~1260-1285), placed immediately BEFORE it. Header reads a new
   loc key `buildings_cottage_industry`. Two block placeholders, `CottageIndustryItems` +
   `CottageIndustryItemsRow2` (9 buildings: 8 Qing + 1 ROW, fits comfortably across two rows the same
   width the existing Foreign/Commerce/ModernIndustry two-row sections already use).
2. `gui/province_window.gui`: `blockoverride` those two block names with `macro_build_item_<building>`
   entries, one per building — for ALL 9 buildings, INCLUDING the ROW generic (the province window's
   own build menu is not the macro-config-gated model; every building type shown there today,
   `row_manufactory_building`/`row_plantation_building` included, per `province_window.gui`'s own
   existing wiring, confirms ROW buildings ARE meant to appear here).
3. `gui/macro_builder_view.gui`: `blockoverride` the SAME two block names, but with ONLY the 8 Qing
   `macro_build_item_<building>` entries — the ROW cottage building is DELIBERATELY excluded here,
   matching the documented, existing exclusion of `row_manufactory_building`/`row_plantation_building`
   from the Qing player's macro builder (`macro_builder_view.gui:178-180`, "they are rest-of-world
   buildings... and should not show in the Qing player's macro builder"). v2 wrongly proposed adding
   the ROW building to the macro allowlist, reversing this existing, intentional exclusion — v3/v4 do
   not repeat that.

   **Disclosed limitation (review finding, decided not fixed): the macro builder's "where to build"
   list applies its OWN, pre-existing, building-type-agnostic gate,
   `enabled = And(BuildableGlueItem.CanBuild, JOBS_available_slots > 0)`
   (`macro_builder_view.gui:508`), to every listed building, cottage or otherwise. This means a
   province with `JOBS_available_slots <= 0` — precisely the case this design's whole niche is
   built for — will show a cottage building as GREYED OUT in the macro builder's province list,
   even though the building's OWN `allow` block (omitting `sufficient_job_slots`) would let it be
   built there. The niche is therefore only reachable through the per-province build window
   (`gui/shared/gui_base.gui:6935`, gated purely on `BuildingItem.CanBuild`, no separate job-slot
   check), not through the macro builder's bulk "pick building, then highlight eligible provinces"
   flow named in point 1 above.**

   **Corrected impact assessment (second-review finding: an earlier draft understated this — fixed
   here, not softened): this limitation hits harder than "one screen instead of two."** The macro
   builder is this project's established BULK-build tool — the documented Qing workflow is "pick a
   building, then it highlights every eligible province across the realm" (`qing_production_
   buildings.txt:32-37`). The cottage niche specifically targets provinces that are job-slot-
   saturated late-game, which is exactly the scenario where a player wants to top up MANY provinces
   at once — the primary case the macro builder exists for. In that exact scenario, `:508`'s
   independent gate greys every cottage building out in the ONE tool built for it, forcing a
   province-by-province fallback through the tedious per-province window instead. This is not a
   minor UX rough edge; it undercuts the feature's primary intended use case.

   **Decision (made here, not deferred): ship the macro builder wiring as planned anyway — the niche
   still functions, just not through the tool best suited to it.** Rejected alternative: special-
   case `macro_builder_view.gui:508`'s `enabled` expression to skip the `JOBS_available_slots > 0`
   clause for cottage-category buildings. Not chosen because the expression has no existing
   per-building-type branch to hook (it is one shared line for every building the macro builder
   lists, keyed only on `BuildableGlueItem`, not on which building is selected) — adding that branch
   would be an unproven GUI-scripting capability with no precedent anywhere in this codebase's `.gui`
   files, the class of change this project's standing rules require a labeled boot spike for, not a
   blind edit. Shipping as-is means the province window (point 2 above) is the ONLY fully-functional
   path to the niche; the macro builder will list and let a player click into cottage buildings
   normally in any province that still has spare job slots, but will grey them out in the specific
   job-slot-zero case this design exists for. This is logged here loudly, not minimized: the
   feature's value is real but only reachable through the less convenient screen for its own
   headline use case, and a follow-up task to build the `:508` boot-spike (an explicit per-category
   branch, verified on a real boot before trusting it) should be opened separately rather than
   blocking this one.
4. `common/buildings/qing_cottage_buildings.txt` (new file, 8 Qing buildings) +
   `row_production_buildings.txt` (append the 1 ROW generic, alongside its two existing siblings,
   `row_manufactory_building` and `row_plantation_building`).
5. `gfx/interface/macro_builder/config/00_default.txt`'s `includes` allowlist: add the 8 Qing building
   keys ONLY (confirmed this is the actual gate populating `MacroBuilderView.GetBuildInProvinceModel`
   — matching point 3 above, the ROW building is never listed here, consistent with its siblings;
   the "REMOVED... rest-of-world buildings" exclusion rationale itself lives in
   `macro_builder_view.gui:178-180`, not in `00_default.txt` — corrected citation, review finding).
6. Localization: 8 Qing + 1 ROW name/desc (new file `qing_cottage_buildings_l_english.yml` +
   append to wherever `row_manufactory_building`'s own loc lives) + the `buildings_cottage_industry`
   category header key.

## What this design does NOT touch

- The existing automatic `COTTAGEIND_produce_all` pop-driven trickle — unchanged; these buildings add
  a further `base_resources` multiplier on the SAME raw-good proxy the trickle already reads, exactly
  like `IND_resource_gathering_operation` does today.
- `late_munitions`/`late_artillery` — confirmed factory-only, no cottage recipe exists for either
  (`se_COTTAGEIND.txt`, bare `# CANNOT BE PRODUCED BY COTTAGE INDUSTRY` comments) — consistent with
  the historical research (modern ordnance needs factory precision). No cottage building targets
  these; a raw-good building cannot create a recipe path that does not exist.
- The existing city-buildable raw-good buildings (`IND_resource_gathering_operation`, the six named
  Qing works) — untouched, remain fully buildable everywhere they are today (including rural
  provinces, since neither has a city gate) — this design adds a cheaper, additional rural option
  alongside them, not a restriction on them.
- Task #30 / task #23 (currency/treasury) — separate, unrelated in-progress work, not touched here.

## Open questions for review

1. Is omitting `sufficient_job_slots` entirely (unlimited stacking, no capacity cost at all) the
   right mechanism, or should cottage buildings instead consume a SMALL, separate, non-zero job-slot
   cost (a partial capacity cost, modeling that household labor is not perfectly free of contention
   with formal employment either)? v4 chose the simpler, stronger option (full omission) as the
   clearer niche — not because a partial-cost variant was ruled out on the merits.
2. **RESOLVED (review finding, no longer open): the stacking exploit is real and unbounded, not
   self-limiting.** `global_settlement_building_slot = 9999` (`common/modifiers/00_hardcoded.txt:741`,
   "all provinces have effectively unlimited building slots") confirms there is NO generic
   per-province building-slot cap in this codebase to rely on. Combined with no job-slot cost and no
   existing precedent anywhere in `common/buildings/` for a building capping ITS OWN instance count
   via `num_of_<building> < N` in its own `allow` block (the one related precedent found,
   `00_default.txt:27-28`'s port-building chance modifiers, is a spawn-weight, not a hard cap), a
   player CAN build unlimited copies of e.g. `qing_cottage_smithy_building` on one province for
   unbounded iron-output multiplication today, with or without this design. **Decision: ship without
   an added cap.** This is a PRE-EXISTING property of every `base_resources` building in this
   codebase (the six Qing works and both ROW generics have exactly the same unbounded-stacking
   exposure — `global_settlement_building_slot = 9999` applies to them too, and none of them caps its
   own instance count either), not a defect this design introduces. Adding a one-per-province gate
   to ONLY the cottage set, while leaving the identical exposure on every existing raw-good building
   unfixed, would be an inconsistent, cosmetic patch rather than a real fix — a genuine fix (a
   universal per-province-per-building-type cap) is a separate, pre-existing-scope task, not part of
   introducing 9 more buildings that share a property every current raw-good building already has.
3. **RESOLVED (second-review finding, fixed, not left open): cost raised from 40 to 50 gold** so
   matching `IND_resource_gathering_operation`'s `base_resources = 1` exactly no longer makes the
   cottage building dominate it (half the cost, equal raw-good output, zero job-slot cost — a strict
   win with no trade-off, which a second adversarial review round correctly flagged). 50 gold + the
   lower strata output (0.2/0.15 vs 0.7/0.5) restores a genuine price/output trade-off alongside the
   job-slot-freedom niche, rather than replacing the trade-off with a pure upgrade. Still a starting
   figure for a real balance pass, not a final tuning number — but no longer strictly dominant.
