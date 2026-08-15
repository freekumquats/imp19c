# DESIGN — Qing cottage buildings that boost FINISHED cottage-tier goods (pharmaceuticals,
# gunpowder, paper, silk cloth), not just raw goods

> **Indigo/dye does NOT belong in this doc, and is NOT a cottage building — it's a FACTORY-tier
> Qing building, routed to `qing_industry_buildings.txt`.** A follow-up research pass (#58's
> sugar/hemp re-check) found a real, sourced Qing-distinctive institution for INDIGO specifically
> (registered, tradable, inheritable processing-property shares in Jiangxi, plus a dedicated
> commodity guild — clears the same bar timber cleared). Checked against source: the FINISHED
> good `dyes` (processed/synthetic dye, distinct from the raw `dye` map good) is explicitly
> factory-only — `se_COTTAGEIND.txt:648-652` stubs it `# CANNOT BE PRODUCED BY COTTAGE INDUSTRY —
> processed/synthetic dyes need a chemical works`, and `dyes` is a genuine player-assignable
> factory good (`INDUSTRY_factories_assigned_dyes`, gated `tech_manufactories`, per
> `industrial_goods_buttons.txt:1562-1620` and `INDUSTRY_svalues.txt:213/429-439`). This is the
> EXACT tier the mod's existing named Qing works already occupy (`qing_steel_works_building`,
> `qing_textile_mill_building`, `qing_machine_works_building`, `qing_navy_yard_building`, all in
> `common/buildings/qing_industry_buildings.txt`) — a NEW `qing_dyeworks_building` (or similar)
> belongs alongside them, NOT in this cottage-tier doc.
>
> **Shape, mirroring `qing_textile_mill_building` exactly** (`qing_industry_buildings.txt:70-105`):
> same `allow` gate shape (culture-group + `invention = tech_manufactories` + `has_city_status =
> yes` + `civilization_value >= 30` + `sufficient_job_slots = yes` + the shared
> `INDUSTRY_province_industry_capacity > num_of_IND_industrial_estate` factory-slot gate — this
> building DOES compete for industry capacity, unlike the cottage tier), similar `cost`/`time`
> (200/480 as a starting reference), and a production term added to
> `GOODS_governorship_dyes_produced_mechanised` via the SAME proven MG-hook cached-wrapper pattern
> already shipped for clothing/naval_supplies/munitions (`GOODS_svalues.txt:3086-3106` is the
> literal template — add `GOODS_dyeworks_dyes_output`, a `dyes_infra_output`/`_compute` cached
> pair, and one line in the existing cache-writer extension). Flavor text cites the Yining/Xiushui
> 1792 property-division document and the Tingzhou merchants' dedicated 靛青會館 (Indigo Guild
> House) network — the real Qing-distinctive institution.
>
> This is its own small, separately-scoped task (factory-tier, different file, different pattern
> owner than either this cottage doc or #58's raw-good list) — logged here and in #58 so the
> citation isn't lost, tracked for implementation alongside or after this doc's 3 cottage
> buildings, not merged into either.

> STATUS 2026-08-13: DRAFT v2 — round-1 adversarial review complete. Round 1 found 2 CRITICAL
> issues that would have shipped a non-functional feature: (1) the mechanism section placed the
> new term into `GOODS_governorship_<X>_produced` (the SUMMED wrapper) instead of
> `_produced_mechanised` — traced `GOODS_governorship_produce_industry` (`se_GOODS.txt:1480-1495`)
> directly and confirmed the quarterly stockpile-write loop reads ONLY `_produced_mechanised`, never
> `_produced`. Placing the bonus in `_produced` would have nudged tooltips/shortage figures but
> NEVER added anything to the actual sellable/exportable stockpile — the building would look like
> it worked but silently not. Fixed below: term now lands in `_produced_mechanised`, exactly
> mirroring the MG-hook's real placement. (2) The doc's own claim that a cache wrapper could be
> skipped "because cottage-tier goods are read less often" was independently checked and found
> FALSE — `_produced` for these 4 goods is read at the identical per-governorship-per-quarter
> frequency the MG-hook goods were, which is exactly why the MG-hook design treated its cache as
> "a REQUIRED part of the build, not an optimization afterthought." Fixed below: extends the real,
> existing `GOODS_cache_munitions_infra` function (`se_GOODS.txt:24-54`, already extended 3 times
> for munitions/clothing/naval_supplies/early_artillery) with 4 more cache lines, not deferred.
> Round 1 also found a HIGH gap: this doc's citations (paper "esp. in China," gunpowder "artisan/
> mill craft") are the SAME shape of citation `#58`'s own research explicitly rejected for silk —
> "China also did this, well-documented, at scale" is not Qing-distinctiveness. Resolved below by
> applying #58's exact bar to all 4 buildings honestly, not assuming they survive because #58's
> review happened to focus elsewhere.
>
> STATUS (superseded intro, kept for provenance): this doc originally corrected a scope error
> carried through #101 and #58 — #101's original v1 draft (never shipped) proposed cottage
> buildings feeding finished goods directly, but an in-session review "disproved" that model by
> comparing it against FACTORY-tier siblings and pivoted the whole task to RAW-good buildings
> instead. That pivot was itself the error: the correct comparison is the ALREADY-PROVEN MG
> named-building production-hook pattern (`design/DESIGN_MG_BUILDING_PRODUCTION_HOOKS.md`, shipped
> 2026-08-04), applied to the cottage tier instead of the factory tier.
>
> STATUS 2026-08-13: DRAFT v5 — round-4 adversarial review complete, VERDICT: READY FOR
> IMPLEMENTATION. Round 4 independently re-verified round 3's fix (confirmed
> `qing_cottage_silk_reeling_shed_building`/`qing_cottage_woodlot_building` really do carry
> `base_resources = 1` on the same gates the new buildings dropped it from; confirmed no
> existing building anywhere is gated on `saltpetre`, so the powdermill building never had this
> problem; confirmed the `_cottage_bonus` mechanism never assumed `base_resources` presence, so
> removing it broke nothing downstream), confirmed the pharmaceuticals `value = 1` rate is now
> consistent everywhere in the doc (no stray `value = 2` survivors), and confirmed the Xuan-paper
> stub actually landed in `DESIGN_66_QING_GUILD_FACTORIES.md` (not just referenced from here).
> Found ONE LOW, non-blocking gap: all 8 EXISTING cottage buildings carry a `modification_display`
> block (confirmed file-wide, zero exceptions), which the 3 new sketches omitted. Fixed below —
> added `modification_display` blocks (listing only the 2 stats these buildings actually carry,
> since neither has `base_resources` anymore) to all 3 new building sketches. No further review
> round needed for this doc; the only remaining open items are boot-tuning ([ASSUMPTION] rate
> constants) and the GUI/loc wiring pass, both implementation-time work, not design gaps.
>
> STATUS (superseded, kept for provenance): round 3 found a HIGH gap
> round 2 missed: `qing_cottage_silk_weaving_building` and `qing_cottage_papermill_building` each
> carried `base_resources = 1` on the SAME `trade_goods` gate (`silk`/`wood`) an EXISTING sibling
> building already uses at the same value (`qing_cottage_silk_reeling_shed_building`,
> `qing_cottage_woodlot_building`) — a flat, guaranteed double-count of raw output, wider in blast
> radius than the pharmaceuticals case (raw silk feeds 4 downstream goods, raw wood feeds 5,
> including gunpowder's own recipe input) and, unlike pharmaceuticals' single-building stacking,
> thematically backwards: a WEAVING building's flavor is turning raw silk into cloth, not growing
> more raw silk, and a PAPERMILL's flavor is turning wood into paper, not growing more wood — there
> is no in-fiction reason for either to duplicate the raw-good boost a DIFFERENT, already-existing
> building supplies. Fixed below by dropping `base_resources` entirely from these 3 new buildings
> — their job is the finished-good `_cottage_bonus` hook, not a second raw-output claim on a good
> a sibling building already covers. Round 3 also found the pharmaceuticals "half the naive guess"
> calibration (v3) wasn't an actual computed ratio despite being described as one — the indirect
> (raw-boost-through-COTTAGEIND) and direct (this design's new term) contributions use entirely
> different scaling (the indirect path is damped by `COTTAGEIND_scale × pops_output × efficiency ×
> TECH_bonus`; the direct term bypasses all of that) — so "half" was a narrative gloss on a guess,
> not a magnitude comparison. Fixed below: stated plainly as an unverified ASSUMPTION needing
> boot-log tuning, not as resolved reasoning. Also confirmed the Xuan-paper stub still needs to
> land in `#66` before that doc is finalized (tracked there, not blocking this doc).
>
> STATUS (superseded, kept for provenance): round 2 verified both
> CRITICAL fixes hold exactly against source (mechanism placement, cache extension) and found 2
> NEW HIGH gaps: (1) the "paper: no citation found" verdict was UNDER-RESEARCHED, not actually
> negative — Xuan paper (宣紙), Jing County (涇縣), Anhui, is a real, documented, lineage-
> controlled papermaking institution (traditionally the Cao/曹氏 clan, trade-secret transmission,
> licensed workshop/guild organization with imperial-tribute grade control, 貢紙) — the SAME shape
> of citation that saved timber/indigo/Foshan-iron/Yunnan-copper. Like those, it operates at
> licensed-workshop scale, not household/cottage scale — so it does NOT rescue the cottage-tier
> `cottage_papermill_building`, but per the same treatment #66 already gives iron/copper, it
> SHOULD be routed there as a future factory-tier `qing_xuan_papermill_building` candidate, not
> dismissed with "no citation found." Fixed below by routing it explicitly, matching the doc's own
> existing indigo/dye routing note. (2) The stacking-risk open question wasn't actually a
> hypothetical multi-building interaction — round 2 traced a CONCRETE, GUARANTEED double-benefit:
> `qing_cottage_herbalist_building`'s OWN existing raw-vegetables boost already feeds
> `COTTAGEIND_produced_pharmaceuticals` (the automatic recipe reads `COTTAGEIND_raw_vegetables`
> directly), so adding this doc's SECOND bonus term to the SAME building means one building now
> boosts pharmaceuticals through TWO channels at once, not two independent buildings compounding
> in the abstract. Resolved below with an explicit calibration decision, not left to boot-tuning.
> Names are now pinned to the `qing_cottage_*` prefix (matching #58's own resolution to keep names,
> drop only the culture gate) rather than left for #58 to decide independently, and literal
> building-shape sketches (allow + stat modifiers) are added for all 3 new buildings.

## Task

Build real, player-buildable Qing cottage buildings that boost FINISHED cottage-tier goods —
pharmaceuticals, gunpowder, paper, silk_cloth — the goods people actually associate with
"cottage industry" (household workshops making usable goods), not just raw material extraction.

## Ground truth (traced this session, not assumed)

`se_COTTAGEIND.txt` already runs a fully automatic, no-building, engine-driven quarterly
conversion for every governorship in the game. Four of its recipes make genuine finished goods
from inputs already tracked in this mod, with real historical grounding in their own comments:

| Good | Recipe (`se_COTTAGEIND.txt`) | Inputs | Efficiency |
|---|---|---|---|
| `pharmaceuticals` | `:600-614` | `COTTAGEIND_raw_vegetables` + `COTTAGEIND_raw_whales` | 5 |
| `silk_cloth` | `:654-670` | `COTTAGEIND_raw_silk` + `COTTAGEIND_raw_dye` | 0.75 |
| `paper` | `:672-687` | `COTTAGEIND_raw_wood` + `COTTAGEIND_raw_textile_fibres` | 3 |
| `gunpowder` | `:690-712` | `COTTAGEIND_raw_saltpetre` + `COTTAGEIND_raw_sulphur` + `COTTAGEIND_raw_wood×0.25` | 1.5 |

Mechanism (`COTTAGEIND_scale_production`, `:183-219`): `produced = raw_inputs_sum × pops_output ×
efficiency × 0.5 × TECH_cottage_industry_overall_bonus`, written directly to `<good>_stockpile`.
No building anywhere in this chain — every country gets this automatically from its raw
material stockpiles and pop count alone.

The finished good then flows to consumers via `GOODS_governorship_<good>_produced` (e.g.
`:3336-3346` for pharmaceuticals), which sums `COTTAGEIND_produced_<good>` (cottage) +
`GOODS_governorship_<good>_produced_mechanised` (factory). This is the SAME summed-total pattern
the shipped MG building hooks already extend for clothing/naval_supplies/munitions via a THIRD,
disjoint `_infra_output` term (`GOODS_svalues.txt:3086-3106`, quoted in full below) — proving the
"add a fourth disjoint term for a named building" pattern is safe and already proven at this
exact seam.

```
GOODS_governorship_clothing_produced_mechanised = {
	value = 0
	if = { limit = { has_variable = INDUSTRY_factories_assigned_clothing } ... }  # factory path
	add = GOODS_governorship_clothing_infra_output   # <-- the MG-hook pattern this design copies
}
```

## Why this is NOT the same as #101/#58's raw-good buildings, and NOT the same mistake v1 made

- **#101/#58's 8 buildings** boost `base_resources` (raw trade-good province output) — iron, lead,
  wood, etc. They never touch a finished good; a smithy makes more raw iron available for
  WHOEVER (cottage or factory) converts it downstream. That system stays as-is; this design does
  not touch it.
- **v1's original, never-shipped mistake** (per #101's own design-doc history) was proposing a
  cottage building that REPLACES the automatic COTTAGEIND conversion — i.e., the finished good
  would ONLY be produced if the building existed, contradicting the fact that COTTAGEIND already
  produces it for everyone unconditionally. THAT is what got correctly disproven by tracing
  `GOODS_governorship_iron_produced`. The disproof was correct; the OVERCORRECTION — abandoning
  finished-good buildings entirely instead of fixing the model — was not.
- **This design's model**: the building does NOT replace or gate the automatic COTTAGEIND
  conversion. It ADDS a small, disjoint, flat bonus on top of it — a Qing household with (say) an
  apothecary-workshop building produces MORE pharmaceuticals than an ordinary province's
  automatic cottage output, via a fourth summed term, exactly mirroring how the Qing textile
  mill adds clothing on top of the factory/cottage baseline. This is provably safe (already
  shipped, reviewed twice, for the factory tier) and requires no change to `COTTAGEIND_
  scale_production` or any of its four recipes.

## Qing-distinctiveness check (round-1 review HIGH finding — applying #58's own bar honestly)

#58 established: "China also did this, well-documented, at scale" does NOT clear the bar for a
Qing-exclusive gate — the bar is a genuine, sourced, DISTINCTIVE organizational/institutional form
(timber's lineage share-contracts, indigo's registered tradable processing shares), not mere
scale or documentation quality. Checking all 4 candidates against that exact bar, honestly, not
assuming they survive because #58's own review pass happened to focus on the 8 raw-good buildings
instead:

1. **Pharmaceuticals (materia medica)** — #58 ALREADY CHECKED this exact good (via the existing
   `qing_cottage_herbalist_building`'s vegetables gate) and found no distinct institution;
   household herb gathering/processing is universal. Extending this building's EFFECT to a
   finished good doesn't change that verdict — the underlying craft still has no sourced Qing-
   specific organizational form. **Verdict: generic, not Qing-exclusive.**
2. **Silk_cloth (household weaving+dyeing)** — #58 ALREADY CHECKED silk twice (round 1 hedged,
   round 2 confirmed the fold decisively: Qing silk sourcing ran through market brokers, no more
   distinctive than Bursa/Lyon/Lombardy's comparable putting-out systems). The finished-cloth
   step doesn't reopen that verdict. **Verdict: generic, not Qing-exclusive.**
3. **Paper (bamboo/rag-pulp papermaking) — REVISED, round 2.** The "artisan/mill craft, esp. in
   China" citation offered in v2 is indeed the same weak shape that failed for silk — but round 2
   found the search stopped too early: **Xuan paper (宣紙), Jing County (涇縣), Anhui**, is a real,
   documented, Chinese-distinctive institution — lineage-controlled production (traditionally the
   Cao/曹氏 clan of Xiaoling township, trade-secret transmission within the lineage since Ming/
   early-Qing), organized under a licensed workshop/guild system with imperial-tribute grade
   control (貢紙). This is the SAME shape of citation that saved timber (Meng Zhang's lineage-
   tenure) and indigo (guild houses). Like Foshan iron and Yunnan copper (#66), it operates at
   licensed-workshop/tribute scale, NOT household/cottage scale — so it does NOT rescue the
   COTTAGE-tier `qing_cottage_papermill_building` below, but the citation itself is real and
   should not be discarded. **Routed to #66 as a future factory-tier `qing_xuan_papermill_
   building` candidate**, mirroring exactly how #66 already handles iron/copper — logged there,
   not built in this doc. **Verdict for the COTTAGE-tier building: generic, not Qing-exclusive.**
4. **Gunpowder (water-mechanised powder milling)** — NOT previously checked by #58. Citation
   ("organised as artisan/mill craft not a modern factory") is again scale/organization-level
   description, not a specific institutional citation (no guild name, no share-contract, no
   state-quota system offered). **Verdict: generic, not Qing-exclusive**, same caveat as paper.

**Net result: all 4 candidates fold to GENERIC, matching #58's own 8-of-8 outcome for the
original raw-good buildings.** This is not a deficiency — it's the same principle applied
consistently. Restructured proposal below.

## Proposed buildings — CORRECTED (generic, not Qing-exclusive; names pinned, round 2)

Each building is gated the same way as #58's now-generic raw-good buildings (rural,
`sufficient_job_slots` omitted, `qing_cottage_*` name kept per #58's own resolution to keep names
and drop only the culture gate — but NO culture-group condition here), keyed off the RAW GOODS
the matching COTTAGEIND recipe consumes (2-3 inputs each, not one):

1. **NOT a new building — extend the EXISTING `qing_cottage_herbalist_building`**
   (pharmaceuticals), which — per #58's restructure — is ALREADY becoming generic (culture gate
   dropped, name kept) as part of #58's own implementation.

   **Calibration decision, round 2, CORRECTED round 3:** this building's EXISTING raw-vegetables
   `base_resources` boost already feeds `COTTAGEIND_produced_pharmaceuticals` (the automatic
   recipe reads `COTTAGEIND_raw_vegetables` directly, per the building's own header comment) — so
   adding a SECOND, independent bonus term to the SAME building means one structure boosts
   pharmaceuticals through two channels, not two buildings compounding in the abstract. This
   double channel is INTENTIONAL, not a bug to detune away — it matches the building's own flavor
   (a village herbalist who both grows more medicinal herbs AND compounds them into more finished
   remedies). **Round 3 correction:** v3 described setting the direct term's rate to "half the
   naive guess (2→1)" as if this were a computed calibration reflecting the two channels' relative
   size. It is not. The indirect channel (raw-vegetables boost → `COTTAGEIND_raw_vegetables` →
   `COTTAGEIND_scale_production`) is damped by `pops_output × efficiency(5) × 0.5 ×
   TECH_cottage_industry_overall_bonus`, most of it scaled down hard by `COTTAGEIND_scale`'s own
   pops-output term; the direct term this design adds bypasses ALL of that scaling, landing
   straight in `_produced_mechanised`. These two channels are not comparable in magnitude without
   actually computing both sides, which this doc has not done. **Set
   `GOODS_cottage_herbalist_pharmaceuticals_output = 1` as a plain, un-derived [ASSUMPTION]** —
   not "half of a computed value" — to be boot-log tuned against the actual combined stockpile
   output once both channels are live, jointly with #58's own raw-vegetables rate.

   ```
   # (added to the EXISTING qing_cottage_herbalist_building's effect list, no allow-gate change)
   # [this design] second bonus term on the FINISHED good this building's flavor is named for.
   # Stacks by design with the building's EXISTING raw-vegetables boost (one household craft, two
   # visible effects) -- rate below is an UN-DERIVED ASSUMPTION, not a computed calibration; the
   # two channels use different scaling (indirect: COTTAGEIND_scale-damped; direct: none) so their
   # relative size is not yet known. Boot-tune against actual combined stockpile output.
   ```
   (The svalue-side hook itself — `GOODS_governorship_pharmaceuticals_cottage_bonus` reading
   `num_of_qing_cottage_herbalist_building` — is unchanged from the sketch below.)

**[round-3 fix]** All 3 new buildings below DROP `base_resources` entirely. v3's sketches
carried `base_resources = 1` on the SAME `trade_goods` gate an EXISTING sibling building already
uses at the same value — `qing_cottage_silk_reeling_shed_building` (silk) and
`qing_cottage_woodlot_building` (wood) — which would flatly double raw output on a good these new
buildings don't even claim to be about. It's also backwards in flavor: a weaving building's job
is turning raw silk into cloth, not growing more raw silk (that's the reeling shed's job); a
papermill turns wood into paper, not growing more wood (that's the woodlot's job). These 3
buildings' entire purpose is the finished-good `_cottage_bonus` hook below — they carry no
`base_resources` claim on the raw good their `allow` gate merely uses to locate them.

2. **`qing_cottage_silk_weaving_building`** (silk_cloth):
   ```
   qing_cottage_silk_weaving_building = {
   	# 農家織染坊 -- household silk weaving and dyeing, the finishing step beyond raw silk
   	# reeling (qing_cottage_silk_reeling_shed_building) and distinct from the factory-tier
   	# Imperial Silk Manufactory (qing_silk_filature_building) -- three genuinely different
   	# tiers of the same craft, not redundant with either. No base_resources: this building's
   	# whole purpose is the silk_cloth cottage-bonus hook below, not a second raw-silk claim
   	# the reeling shed already covers.
   	local_lower_strata_output = 0.2
   	local_proletariat_output = 0.15
   	cost = 50
   	time = 150
   	allow = {
   		NOT = { has_city_status = yes }
   		trade_goods = silk
   	}
   	modification_display = {
   		0 = local_lower_strata_output
   		1 = local_proletariat_output
   	}
   }
   ```
3. **`qing_cottage_papermill_building`** (paper — cottage tier ONLY; the Xuan-paper/Jing-County
   citation is routed to #66's factory tier instead, see the distinctiveness check above):
   ```
   qing_cottage_papermill_building = {
   	# 鄉村造紙坊 -- household bamboo/rag-pulp papermaking, the dominant pre-Fourdrinier method.
   	# Generic (not Qing-exclusive) -- see distinctiveness check above; the genuinely
   	# Chinese-distinctive papermaking institution (Xuan paper, Jing County lineage guilds)
   	# is a licensed-workshop-scale case routed to a separate factory-tier building (#66).
   	# No base_resources: this building's whole purpose is the paper cottage-bonus hook below,
   	# not a second raw-wood claim the woodlot building already covers.
   	local_lower_strata_output = 0.2
   	local_proletariat_output = 0.15
   	cost = 50
   	time = 150
   	allow = {
   		NOT = { has_city_status = yes }
   		trade_goods = wood
   	}
   	modification_display = {
   		0 = local_lower_strata_output
   		1 = local_proletariat_output
   	}
   }
   ```
4. **`qing_cottage_powdermill_building`** (gunpowder — no existing sibling building is gated on
   `saltpetre`, so this one's raw-output question doesn't arise the same way; kept without
   `base_resources` anyway, for consistency with the other 2 new buildings and because this
   building's stated purpose is the finished good, not the raw input):
   ```
   qing_cottage_powdermill_building = {
   	# 鄉村火藥坊 -- household/artisan powder-milling, water-mechanised since well before 1763
   	# but organised as artisan/mill craft, not a modern factory. No coastal requirement --
   	# powder mills were sited inland near niter and running water.
   	local_lower_strata_output = 0.2
   	local_proletariat_output = 0.15
   	cost = 50
   	time = 150
   	allow = {
   		NOT = { has_city_status = yes }
   		trade_goods = saltpetre
   	}
   	modification_display = {
   		0 = local_lower_strata_output
   		1 = local_proletariat_output
   	}
   }
   ```

These 3 new buildings live in the SAME file as #58's other now-generic buildings
(`common/buildings/qing_cottage_buildings.txt`), same naming convention, same stat template —
not a separately-decided naming scheme.

### Mechanism — CORRECTED (round-1 review CRITICAL fix): term lands in `_produced_mechanised`,
### cache is NOT optional

Round 1 traced `GOODS_governorship_produce_industry` (`se_GOODS.txt:1480-1495`, the macro the
quarterly stockpile-write loop actually calls per good) directly:
```
GOODS_governorship_produce_industry = {
	if = { limit = { has_variable = INDUSTRY_factories_assigned_$tradegood$ }
		change_variable = { name = $tradegood$_stockpile  add = GOODS_governorship_$tradegood$_produced_mechanised }
	}
}
```
This reads `_produced_mechanised`, NEVER `_produced` — confirming placing the new term in
`_produced` (v1's plan) would have nudged tooltips/shortage math but NEVER reached the physical,
sellable stockpile. Corrected mechanism, now placed exactly where the MG-hook's own term lives:

```
GOODS_governorship_pharmaceuticals_produced_mechanised = {
	# ... existing body unchanged (factory-assignment branch) ...
	add = GOODS_governorship_pharmaceuticals_cottage_bonus   # NEW disjoint term, this design
}
GOODS_governorship_pharmaceuticals_cottage_bonus = {
	if = { limit = { has_variable = pharmaceuticals_cottage_bonus_cached }  value = var:pharmaceuticals_cottage_bonus_cached }
	else = { value = GOODS_governorship_pharmaceuticals_cottage_bonus_compute }
}
GOODS_governorship_pharmaceuticals_cottage_bonus_compute = {
	value = 0
	every_governorship_state = { every_state_province = {
		add = { value = num_of_qing_cottage_herbalist_building  multiply = GOODS_cottage_herbalist_pharmaceuticals_output }
	} }
}
GOODS_cottage_herbalist_pharmaceuticals_output = { value = 1 }   # [ASSUMPTION] un-derived, boot-tune (see calibration decision above)
```

Repeat identically for silk_cloth/paper/gunpowder with their own building/svalue names — each
reads `num_of_qing_cottage_silk_weaving_building` / `_papermill_building` / `_powdermill_building`
respectively; rate constants for these 3 are wide open [ASSUMPTION]s, not yet even guessed at a
specific number, since (per the round-3 fix above) they carry no `base_resources` term to
calibrate against — boot-tune from zero, not from an existing sibling's magnitude.

**Cache — NOT optional, per round-1 review's second CRITICAL finding.** Round 1 confirmed
`_produced` (and therefore `_produced_mechanised`) for these 4 goods is read at the IDENTICAL
per-governorship-per-quarter frequency the MG-hook's own factory-tier goods were, which is
exactly why that design treated caching as "a REQUIRED part of the build, not an optimization
afterthought" (G4). This design does the same: extend the REAL, existing cache function
(`GOODS_cache_munitions_infra`, `se_GOODS.txt:24-54` — already extended 3 times for munitions/
clothing/naval_supplies/early_artillery) with 4 more lines:
```
set_variable = { name = pharmaceuticals_cottage_bonus_cached  value = GOODS_governorship_pharmaceuticals_cottage_bonus_compute }
set_variable = { name = silk_cloth_cottage_bonus_cached       value = GOODS_governorship_silk_cloth_cottage_bonus_compute }
set_variable = { name = paper_cottage_bonus_cached            value = GOODS_governorship_paper_cottage_bonus_compute }
set_variable = { name = gunpowder_cottage_bonus_cached        value = GOODS_governorship_gunpowder_cottage_bonus_compute }
```
Same function, same one-walk-per-quarter discipline — not a fifth cache-writer, a fifth EXTENSION
of the one that already exists.

## Non-goals / explicitly NOT changed

- `COTTAGEIND_scale_production` and its four finished-good recipes: untouched.
- #101/#58's 8 existing raw-good buildings: untouched, this is a fully separate, additive set.
- No change to factory-tier MG hooks (clothing/munitions/naval_supplies): untouched, cited only
  as the proven pattern this design copies.

## Remaining items (design complete; these are implementation-time work, not open design gaps)

1. **[RESOLVED, round 1]** `_produced_mechanised` bodies confirmed directly for all 4 goods —
   `GOODS_svalues.txt:3323` (pharmaceuticals), `:3593` (silk_cloth), `:3619` (paper), `:3664`
   (gunpowder) — all four follow the identical factory-assignment-branch shape; none has an
   existing fourth term this would collide with.
2. **[RESOLVED, round 1]** Cache is required, not optional — extend
   `GOODS_cache_munitions_infra`, per the corrected mechanism above.
3. **[OPEN, implementation-time]** Tune the 4 `GOODS_cottage_*_output` rate constants — all 4
   are best-guess [ASSUMPTION]s, correctly labeled as un-derived (not computed), needing
   boot-log tuning once the feature ships. This can only be settled with boot data, per this
   project's own "guess and log, don't block on unavailable data" standing rule — not a reason
   to withhold implementation.
4. **[RESOLVED, round 1 + round 3]** pharmaceuticals' `whales` OR-branch — confirmed already
   moot; the shipped `qing_cottage_herbalist_building` gates on `trade_goods = vegetables` alone.
5. **[RESOLVED, round 3 fix + round 4 verification]** The base_resources double-count for
   silk_weaving/papermill — fixed by dropping `base_resources` from all 3 new buildings. Round 4
   independently confirmed this leaves a complete, non-vacuous building shape (2 real strata-
   output stats + the externally-hooked finished-good bonus), consistent with the file's own
   template minus the one term that had to go.
6. **[RESOLVED, round 3 fix + round 4 verification]** Xuan-paper factory-tier stub confirmed
   landed in `design/DESIGN_66_QING_GUILD_FACTORIES.md` itself (its own "Building 4 candidate"
   section), not just referenced from here.
7. **[RESOLVED, round 4 fix]** `modification_display` blocks — round 4 found all 8 existing
   cottage buildings carry one (file-wide convention, zero exceptions) and the 3 new sketches
   omitted it; added above to all 3 (listing only the 2 stats each building actually carries).
8. **[OPEN, implementation-time]** GUI/loc wiring: matches #58's own cleanup-completeness
   discipline (macro allowlist, `gui_templates.gui`, `custom_tooltip.gui`, `province_window.gui`,
   `macro_builder_view.gui`, loc file) — additive wiring for whichever of the 3 buildings ship as
   genuinely new (pharmaceuticals is an extension of an existing building, no new GUI entry
   needed for the building itself, only for its updated tooltip text reflecting the second bonus
   term).
