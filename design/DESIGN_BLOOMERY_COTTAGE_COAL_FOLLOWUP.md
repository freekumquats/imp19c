# DESIGN — Bloomery invention, bonuses 2 and 3 (follow-up to the #12 "Unknown effect" fix)

## Goal
`tech_bloomery` (`common/inventions/00_civic_inventions.txt:589-612`) documents 3 bonuses. The
2026-08-22 fix implemented only bonus 1 (RGO output for Iron/Copper, via `tech_bloomery_modifier`,
mirroring `tech_dynamite`). This design covers the other two:
- Bonus 2: +10% cottage industry output for Bronze, Naval supplies, Early artillery.
- Bonus 3: a small coal-demand modifier per RGO where bonus 1's modifier applies.

## Investigation correction (recorded so a future session doesn't repeat it)
The original fix's follow-up comment claimed "no proven goods-specific, invention-gated
cottage/demand idiom exists in this codebase." That was wrong on inspection, twice over:
1. `COTTAGEIND_military_goods_building_bonus` (`se_COTTAGEIND.txt:727-793`, live, wired at
   `oa_wealth_changes.txt:179`) already adds a goods-specific bonus to a stockpile — but it has no
   branch for bronze/naval_supplies/early_artillery, and it's unconditional, not invention-gated.
2. A separate claim — "cottage industry doesn't produce bronze/naval_supplies/early_artillery at
   all" — was also wrong, caused by a ripgrep escaping mistake (`\|` is a literal pipe in ripgrep's
   default regex, not alternation, so the search silently matched nothing). All three ARE fully
   implemented and wired into `COTTAGEIND_produce_all` (`se_COTTAGEIND.txt:4-33`, lines 19/24/27):
   `COTTAGEIND_produce_bronze` (:435), `COTTAGEIND_produce_naval_supplies` (:312),
   `COTTAGEIND_produce_early_artillery` (:279). Each already calls the shared
   `COTTAGEIND_scale_production` (:183-216), which multiplies every one of the 17 cottage goods by
   one shared, non-goods-specific `TECH_cottage_industry_overall_bonus`.

This means bonus 2 needs NO new production pathway — the goods already exist and already produce.
It needs a small, goods-specific, invention-gated multiplier layered on top of the 3 relevant
`COTTAGEIND_produce_X` functions specifically (never added to the shared `TECH_cottage_industry_
overall_bonus`, which would incorrectly boost all 17 cottage goods, not just these 3).

## Fix, Part 1 — Bonus 2: goods-specific +10% cottage output

**[revision 1 — corrects a critical error found on adversarial review, see below]** The first
draft multiplied `COTTAGEIND_produced_$good$` by 1.1 AFTER calling `COTTAGEIND_scale_production`.
That's too late: `COTTAGEIND_scale_production` (:183-218) already adds the (pre-bonus)
`COTTAGEIND_produced_$output$` into `$output$_stockpile` as its OWN last action (:211-217,
`if = { limit = { has_variable = $output$_stockpile } change_variable = { name = $output$_
stockpile  add = var:COTTAGEIND_produced_$output$ } } }`). A multiply applied after
`COTTAGEIND_scale_production` returns changes the `produced` variable but the stockpile add has
already happened with the OLD value — the actual sellable stock never gets +10%, only the
`produced` stat (read by `GOODS_governorship_bronze_produced` and the tin/copper input-demand
calcs) does. That is backwards: it would look like Bloomery raises raw-material demand without
raising the good it's supposed to boost.

Corrected sequence — add the delta to the stockpile FIRST (using the pre-multiply produced value,
which is exactly the value `COTTAGEIND_scale_production` just finished computing and stockpiling),
THEN multiply `produced` in place so the stat and input-demand readers also see the boosted figure:

```
if = {
	limit = {
		has_variable = bronze_stockpile
		owner = { invention = tech_bloomery }
	}
	change_variable = {
		name = bronze_stockpile
		add = { value = var:COTTAGEIND_produced_bronze  multiply = 0.1 }
	}
	change_variable = { name = COTTAGEIND_produced_bronze  multiply = 1.1 }
}
```

- `owner = { invention = tech_bloomery }` is the proven idiom for checking an invention from a
  scope one level below country (confirmed live at `common/script_values/TECH_svalues.txt:12`,
  `owner = { invention = tech_manufactories }`, evaluated from the SAME governorship-adjacent
  context `COTTAGEIND_scale_production` runs in). `COTTAGEIND_produce_bronze`/`_naval_supplies`/
  `_early_artillery` all run at Governorship scope (each function's own header comment), and
  `owner` from Governorship resolves to the owning country — same link, same scope depth as the
  proven citation. Confirmed reachable: `COTTAGEIND_produce_all` is called quarterly from
  `oa_wealth_changes.txt:176`, no scope shift between that call and these functions.
- The stockpile `add` must be guarded the same way `COTTAGEIND_scale_production` guards its own
  stockpile write (`has_variable = $good$_stockpile`) for the same reason (unseeded frontier
  governorships) — copy that exact guard around the whole `if` block, not just assume it.
- `naval_supplies` has a coastal gate (`if = { limit = { any_governorship_state = { any_state_
  province = { is_coastal = yes } } } ... }`, :312-361, `else` removes the variable at :361). The
  new block goes INSIDE that `if`, right after its own `COTTAGEIND_scale_production` call — never
  outside, since a non-coastal governorship has no `COTTAGEIND_produced_naval_supplies` or
  `naval_supplies_stockpile` write to extend.
- `bronze` and `early_artillery` have no such gate — the new block goes directly after their single
  `COTTAGEIND_scale_production` call.
- Rate: 1.1 / 0.1-of-produced (a flat +10%), taken directly from the invention's own documented
  "+10%" wording — not derived, because the invention text already states the exact number.
- No change needed to `COTTAGEIND_scale_production` itself or its call signature — this sidesteps
  adding a new macro parameter to a function all 17 cottage goods call (which would force every
  other caller to also supply it, per the same "macro args expand across the whole body" hazard
  already hit once this session with `LAND_release_from_list`).

## Fix, Part 2 — Bonus 3: coal demand per bloomery-boosted RGO

**[revision 1 — corrects a critical error found on adversarial review, see below]** The first
draft inserted a new count block directly into `DEMAND_coal`, followed by a bare top-level
`multiply = 0.5`. In a Jomini script_value, a top-level `multiply` scales the ENTIRE accumulated
running total up to that point, not just the immediately-preceding block — `DEMAND_coal`'s own
existing code proves this (residential add → `multiply = 0.3`, then industrial add →
`multiply = 3`, each scaling the WHOLE running total so far; every factory branch AFTER that
point deliberately uses a bare `add` of an already-pre-scaled named svalue, with no trailing
multiply, specifically to avoid rescaling the total again). A bare `multiply = 0.5` inserted after
the existing `multiply = 3` would halve the ENTIRE running value at that point — all previously
accumulated residential + industrial coal demand — not just the new RGO count. That directly
violates this doc's own stated rule ("one dedicated multiply for this block only — never misscale
someone else's count").

Corrected shape — mirror the factory branches exactly: define a new named script_value that
scales ONLY its own internal count, then `add` it into `DEMAND_coal` unscaled, same as
`add = INDUSTRY_demand_bronze_coal` etc.:

```
# in common/script_values/DEMAND_svalues.txt, alongside the other DEMAND_coal-adjacent values
DEMAND_bloomery_coal = {
	value = 0
	every_governorship_state = {
		every_state_province = {
			limit = {
				has_province_modifier = tech_bloomery_modifier
			}
			add = num_of_IND_resource_gathering_operation
		}
	}
	multiply = 0.5
}
```

Then in `DEMAND_coal` itself, add one bare line among the existing factory-branch `if`s (order
doesn't matter there since they're all unscaled adds onto the running total):

```
add = DEMAND_bloomery_coal
```

- `has_province_modifier = tech_bloomery_modifier` reads the SAME modifier bonus-1 already stacks
  (`tech_modifier_applicator_tech_bloomery`, `00_tech_modifier_applicator_effects.txt`), so this
  demand term only ever counts RGOs in provinces where bonus 1 is actually active — "per RGO where
  the modifier applies," exactly as the invention's comment specifies.
- `add = num_of_IND_resource_gathering_operation` inside `every_state_province` is the proven
  count-accumulation idiom — the SAME field name is already used this way elsewhere in this file
  (`DEMAND_svalues.txt:646, 1063, 1110`); the block one line above at :470-475 uses the same
  pattern with a different building count (`num_of_IND_industrial_estate` etc.), confirming the
  general `every_governorship_state { every_state_province { add = num_of_X } }` shape is proven,
  not just this one field. The difference here is the count lives in its OWN named value (so its
  own `multiply = 0.5` only ever scales this value's own total), not inlined into `DEMAND_coal`'s
  shared running total.
- Magnitude derivation (not a fresh guess, per this codebase's own standing convention —
  `DESIGN_103_FOLLOWUP_COTTAGE_MILITARY_BOOST.md` Part 2): the closest formal-industry analogs to
  bloomery's iron/copper smelting are bronze and steel factories' own per-unit coal demand —
  `INDUSTRY_base_demand_bronze_coal = 4`, `INDUSTRY_base_demand_steel_coal = 6`
  (`INDUSTRY_svalues.txt:733-736, 2738-2741`). Average ≈ 5 coal per formal-factory-equivalent.
  Applying this codebase's own already-established cottage-discount ratio (×0.1, from
  `COTTAGEIND_pops_output`, same ratio DESIGN_103 used) gives 5 × 0.1 = **0.5 coal demand per RGO**
  — two real numbers already in the repo, not invented, and "small" as the invention's comment
  requires (a single-RGO iron province adds 0.5 to a country-wide DEMAND_coal that already carries
  multi-hundred contributions from urban/industrial buildings and factories).

## Explicitly NOT done
- No change to `TECH_cottage_industry_overall_bonus` or `COTTAGEIND_scale_production` itself — both
  stay shared/global; bonus 2 is added as a separate, goods-scoped multiplier specifically to avoid
  leaking Bloomery's bonus onto the other 14 cottage goods.
- No change to `COTTAGEIND_military_goods_building_bonus` — that function's existing 5 branches
  (early_munitions/clothing/pharmaceuticals/construction_materials/gunpowder) are untouched;
  bonus 2 does not reuse that function since it is unconditional where this bonus must be
  invention-gated, and none of its existing branches target bronze/naval_supplies/early_artillery.
- No new script_value FILE; both additions land in the same files their proven analogs live in
  (`se_COTTAGEIND.txt`, `DEMAND_svalues.txt`). Revision 1 does add one new named script_value
  (`DEMAND_bloomery_coal`) inside `DEMAND_svalues.txt` — required by the multiply-scoping fix
  above, not a new file.

## Open questions — resolved on adversarial review (kept for record)
1. `owner = { invention = tech_bloomery }` scope reachability: RESOLVED SAFE. Confirmed no scope
   shift between `COTTAGEIND_produce_all`'s quarterly call site and these functions; same chain
   depth as the proven `TECH_svalues.txt:16` citation.
2. Multiply vs. delta-add shape: RESOLVED NOT A CONCERN. No `min`/`max` clamp sits between the
   `produced` write and its readers (clamps are `min=0` on `DEMAND_coal`'s TOTAL, applied after
   all adds/multiplies) — but the stockpile-timing issue this question was fishing for turned out
   to be real for a DIFFERENT reason (see revision 1, Part 1 above).
3. One-tick lag between the modifier applying and `DEMAND_coal` seeing it: RESOLVED LOW RISK.
   `tech_modifier_applicator_tech_bloomery` stacks with `DUR=-1` (persistent), and `DEMAND_coal` is
   a script_value recomputed on demand every quarter — no meaningful lag.
4. Other consumers reading `COTTAGEIND_produced_$good$` before the new multiplier runs: THIS WAS
   THE REAL BUG, see revision 1 Part 1 — `COTTAGEIND_scale_production`'s own internal stockpile add
   is exactly such an earlier consumer, and it runs before the original draft's multiplier had a
   chance to apply. Fixed by moving the stockpile credit to before the in-place multiply.

## Round 2 adversarial review — PASS
Hand-traced the corrected Part 1 sequence with produced=100: scale_production's own stockpile add
credits +100 (pre-bonus, unavoidable — it already ran), the new block's stockpile add credits
+10 (0.1×100, read before the in-place multiply), total stockpile credit = 110 = exactly produced×
1.1. No double-count, no compounding across quarters (produced_$good$ is re-set via unconditional
set_variable every quarter). Part 2's `DEMAND_bloomery_coal` is confirmed self-contained (own
`value=0`, own `multiply=0.5`, bare-added into `DEMAND_coal` with no collision). Ready to
implement.
