# DESIGN — cottage-tier saltpetre extraction + gunpowder milling buildings

> STATUS 2026-08-20: DRAFT v1 — not yet reviewed. Written after a boot-log investigation found
> gunpowder is the single largest thin-stock price-spike offender in this economy (165 of 348
> total spike-guard firings across one boot, concentrated in `yellow_sea`/`eastern_steppe`), and a
> follow-up code read found: (a) saltpetre — gunpowder's dominant input — is the ONLY one of its
> three raw inputs (saltpetre/sulphur/wood) with no cottage-tier building to boost it (sulphur has
> `qing_cottage_sulphur_pit_building`, wood has `qing_cottage_woodlot_building`); (b) the
> conversion step itself (`COTTAGEIND_produce_gunpowder`, se_COTTAGEIND.txt:690) has no building
> gate at all — every governorship converts raw stockpile into gunpowder automatically, for free,
> regardless of whether it has anything resembling a mill.
>
> STATUS 2026-08-20: DRAFT v2 — round-1 adversarial review complete. Every code claim in v1 was
> independently re-verified against the actual files by the reviewer, and by me a second time
> before writing this revision. Two real findings, both incorporated below:
>
> 1. **BLOCKING (fixed): Part 2's central premise was false.** v1 claimed no cottage building
>    boosts a COTTAGEIND conversion step, and flagged the building-presence-count mechanism as an
>    open engineering question needing a review. Both wrong: `COTTAGEIND_military_goods_building_
>    bonus` (se_COTTAGEIND.txt:727-793, already shipped, in the SAME file) already does exactly
>    this for 4 other goods (`early_munitions_stockpile`/`clothing_stockpile`/`pharmaceuticals_
>    stockpile`/`construction_materials_stockpile`), via `every_governorship_state { every_state_
>    province { add = num_of_<building> } }` counted against each stockpile, multiplied by
>    `GOODS_cottage_military_goods_output`. I confirmed by direct read: `gunpowder_stockpile`
>    already exists too (`se_GOODS.txt:118`), set from `GOODS_governorship_gunpowder_produced`
>    exactly parallel to the 4 goods above. Part 2 below is rewritten around this precedent — it
>    is now a ~5-line addition to already-shipped code, not a novel mechanism, and this resolves
>    v1's open questions 1 and 4 outright (additive, not a hard gate, was always the right call —
>    it's literally the house pattern; and the mechanism is already proven, not unverified).
> 2. **SHOULD-FIX (fixed): wrong/incomplete citation, and the sulphur_pit template was probably
>    the wrong choice for Part 1.** v1 cited Needham SCC V:7 only. The reviewer found this mod
>    already has a more specific, more directly-relevant, ALREADY-IN-REPO citation for this exact
>    geography: `oa_economy_setup.txt:217-226` (#228 fix) cites **Jin Xu et al., Industrial
>    Archaeology Review 47(2) 2025**, and explicitly states Bihar/Bengal (India) was "the dominant
>    world source," with the SW-China karst belt as the secondary, domestic-Chinese source — I
>    re-read this comment directly and confirmed it word-for-word. v1 never mentioned the Bihar/
>    Bengal side at all; this revision now cites Jin Xu et al. as primary (Needham kept as
>    supplementary) and says explicitly that the dominant real-world geography is being excluded
>    by the CHI-only culture gate — not silently omitted. Separately, the reviewer independently
>    re-derived (from their own knowledge, not v1's citation) that Chinese earth-niter leaching was
>    predominantly diffuse household/village-scale work (boiling nitrous soil from caves, old
>    walls, latrines), closer in organization to the 8 GENERIC cottage crafts (no culture gate, no
>    province list) than to sulphur's shaft/adit mining — and separately noted that since
>    `trade_goods = saltpetre` already narrows to exactly the 5 seeded provinces, sulphur_pit's
>    extra province-ID list was redundant regardless of which template shape was chosen. Both
>    points independently point the same way: Part 1 below now uses the SIMPLER 8-generic-craft
>    shape (no culture gate, no province list, `base_resources = 1`), not the sulphur_pit clone.
>
> Two NOTE-level items also fixed: the "10 existing cottage buildings" count was stale (the file
> has 11, including sulphur_pit itself — corrected below), and the mill's `allow` gate omitting
> `trade_goods = wood` (a real, 0.25-weighted input) now has an explicit one-line reason instead of
> a silent exclusion.

## Motivating source (read directly, not inferred)

`se_COTTAGEIND.txt:690-710`'s own comment already describes a real, historically-named
institution that has no in-game representation at all:

> "Powder-mill gunpowder (water-mechanised since well before 1763, but organised as artisan/mill
> craft not a modern factory). Consumes saltpetre (dominant) + sulphur + wood (charcoal proxy).
> No coastal gate — powder mills were sited inland near niter and running water."

So the mod's own code already asserts the existence of "powder mills" as the production
mechanism — this design doesn't invent a new institution, it builds the building the comment
already presupposes.

## Part 1 — `qing_cottage_saltpetre_works_building` (raw extraction)

### Historical basis
This mod's own code already cites the primary source for this exact geography —
`oa_economy_setup.txt:217-226` (#228 fix): **Jin Xu et al., Industrial Archaeology Review 47(2)
2025**, which shows Chinese saltpetre (niter, 硝) came from the SW-China karst-cave belt
(Guangxi/Guizhou/Sichuan) via leached "earth-niter" (土硝) from nitrate-rich cave deposits and old
walls/manure-rich soil — while the DOMINANT world source in this period was Bihar/Bengal (India),
which that same comment says the mod deliberately seeds too (`00_Bahar.txt`). This design's
CITATIONS/FLAVOR are CHI/Qing-scoped, but the CORRECTION found in implementation review: since
Part 1's building has no culture gate (deliberately, to mirror the 8 generic crafts' own
unrestricted reach), it IS buildable on the 6 Bahar/India saltpetre provinces too, same as any
generic craft on any matching trade_goods tag world-wide — this was NOT excluded as originally
claimed, just not the design's own flavor focus. Joseph Needham, *Science and Civilisation in
China*, Vol. V:7,
*Military Technology: The Gunpowder Epic* (Cambridge, 1986), is cited as a supplementary source
on the leaching/boiling process itself.

Confirmed by direct read (not grep) of `setup/provinces/00_Guizhou.txt` and
`00_Guangxi.txt` — every CHI province currently carrying `trade_goods="saltpetre"`:

| Province ID | Name | File |
|---|---|---|
| 2745 | Weng'an | 00_Guizhou.txt |
| 3566 | Zunyi | 00_Guizhou.txt |
| 246 | Xuancun | 00_Guangxi.txt |
| 878 | Chongzuo | 00_Guangxi.txt |
| 899 | Rong'an | 00_Guangxi.txt |

### Template — the 8 GENERIC cottage crafts, not sulphur_pit
Earth-niter leaching was diffuse household/village-scale work (boiling nitrous soil scraped from
cave floors, old walls, latrines, stables), not the concentrated shaft/adit mineral mining
sulphur_pit's own rationale is built on. `trade_goods = saltpetre` alone already restricts
buildability to exactly the 5 provinces above (a province carries only one trade good), so a
sulphur_pit-style province-ID list on top of it would be redundant, not just stylistically
inconsistent. This building instead mirrors the 8 undifferentiated crafts (smithy, leadworks,
woodlot, etc. — `qing_cottage_buildings.txt:40-223`) exactly: no culture gate, no extra province
list, `base_resources = 1`.

```
qing_cottage_saltpetre_works_building = {
	# 硝廠 — niter works. Karst-cave "earth-niter" (土硝) leaching + boiling, SW-China karst belt
	# (Jin Xu et al., Industrial Archaeology Review 47(2) 2025; supplementary: Needham, SCC V:7).
	# Diffuse household/village-scale work, not concentrated mineral mining -- mirrors the 8
	# GENERIC cottage crafts' shape (smithy/leadworks/woodlot etc.), not qing_cottage_sulphur_pit_
	# building's specialized-institution shape (trade_goods=saltpetre already narrows to exactly
	# the 5 seeded provinces below; a province-ID list on top would be redundant).
	# Feeds COTTAGEIND_raw_saltpetre, read by gunpowder (dominant input).
	local_lower_strata_output = 0.2
	local_proletariat_output = 0.15
	base_resources = 1

	cost = 50
	time = 150

	allow = {
		NOT = { has_city_status = yes }
		trade_goods = saltpetre
	}

	modification_display = {
		0 = local_lower_strata_output
		1 = local_proletariat_output
		2 = base_resources
	}
}
```

## Part 2 — `qing_cottage_powder_mill_building` (the conversion step)

**Corrected mechanism (v2): this is a proven, already-shipped pattern, not novel.**
`COTTAGEIND_military_goods_building_bonus` (se_COTTAGEIND.txt:727-793) already counts cottage
building presence across every province in a governorship and adds the count (times
`GOODS_cottage_military_goods_output`) directly onto a good's stockpile, for 4 goods:
`early_munitions_stockpile` (quarry/leadworks/sulphur_pit), `clothing_stockpile` (weaving_hut/
silk_reeling_shed), `pharmaceuticals_stockpile` (herbalist), `construction_materials_stockpile`
(woodlot/quarry/smithy). `gunpowder_stockpile` already exists too (`se_GOODS.txt:118`, set from
`GOODS_governorship_gunpowder_produced` in the exact same place as the other 4 goods' stockpile
vars). So this building's bonus ships as a 5th sibling branch in the SAME already-working
function — no changes to `COTTAGEIND_produce_gunpowder` itself, no new mechanism:

```
	if = {
		limit = { has_variable = gunpowder_stockpile }
		change_variable = {
			name = gunpowder_stockpile
			add = {
				value = 0
				every_governorship_state = {
					every_state_province = {
						add = num_of_qing_cottage_powder_mill_building
					}
				}
				multiply = GOODS_cottage_military_goods_output
			}
		}
	}
```
(Added inside `COTTAGEIND_military_goods_building_bonus`, se_COTTAGEIND.txt, alongside the
existing 4 `if` blocks — not a new function.)

### Building definition
```
qing_cottage_powder_mill_building = {
	# 碾房/火藥作 — the water-powered stamping/incorporation mill: grinds and combines saltpetre,
	# sulphur, and charcoal into usable powder. Distinct from raw extraction (qing_cottage_
	# saltpetre_works_building / qing_cottage_sulphur_pit_building) -- this is the MILLING step
	# COTTAGEIND_produce_gunpowder's own comment already describes but has no building for
	# (se_COTTAGEIND.txt:690-693: "water-mechanised... organised as artisan/mill craft").
	# Needham, SCC V:7, on stamp-mill/edge-runner incorporation technology in this period.
	local_lower_strata_output = 0.2
	local_proletariat_output = 0.15
	base_resources = 1

	cost = 55
	time = 150

	allow = {
		owner = {
			OR = {
				country_culture_group = jurchen
				country_culture_group = chinese_group
			}
		}
		NOT = { has_city_status = yes }
		OR = {
			trade_goods = saltpetre
			trade_goods = sulphur
		}
		# NOT trade_goods = wood: wood is a real 0.25-weighted input, but wood-tagged provinces are
		# common across the map -- including it would make this gate nearly universal and defeat
		# the "sited near a scarce/concentrated input" logic the saltpetre/sulphur gate rests on.
	}

	modification_display = {
		0 = local_lower_strata_output
		1 = local_proletariat_output
		2 = base_resources
	}
}
```

## Open questions for review (round 2)
1. Is `trade_goods = saltpetre OR sulphur` still the right allow-gate for the mill, or does siting
   a mill on a SULPHUR (not niter) province stretch the "near at least one input" logic too far?
2. Does the corrected Part 1 template call (8-generic-craft shape, no culture gate, no province
   list) actually hold up, or is there a citation-backed reason saltpetre extraction specifically
   (as opposed to sulphur) should still carry a culture/province restriction?
3. Is `GOODS_cottage_military_goods_output`'s existing multiplier calibrated for 4 already-shipped
   goods appropriate to reuse unchanged for a 5th (gunpowder), or does gunpowder's different
   demand/price profile warrant a distinct multiplier?
