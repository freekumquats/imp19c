# DESIGN — `qing_gunpowder_works_building`, a dedicated Modern Industry building for gunpowder

> STATUS 2026-08-20: DRAFT v1 — not yet reviewed. Companion to
> `DESIGN_COTTAGE_SALTPETRE_GUNPOWDER.md` (the cottage-tier half); this covers the factory tier.
>
> STATUS 2026-08-20: DRAFT v3 — found during implementation, before any code was written: v2's
> finding #3 ("no on_built-style direct-bump pattern exists anywhere in this repo") was WRONG, and
> I missed the same thing the reviewer missed. `GOODS_governorship_dyes_produced_mechanised`
> (`GOODS_svalues.txt:3660-3676`) adds `GOODS_governorship_dyes_infra_output`, which counts
> `num_of_qing_dyeworks_building` directly (`every_governorship_state { every_state_province {
> add = num_of_qing_dyeworks_building } }`, multiplied by a flat `GOODS_dyeworks_dyes_output = 2`)
> straight into dyes production — a REAL, direct per-building production bonus, not an indirect
> raw-good effect. Its own comment names the pattern explicitly: "the named-building production
> hook, mirroring clothing/naval_supplies/munitions verbatim" — so this is an established family
> of hooks, not a one-off. `qing_gunpowder_works_building` gets the same treatment below: a new
> `GOODS_governorship_gunpowder_infra_output` term added into the existing
> `GOODS_governorship_gunpowder_produced_mechanised` (`GOODS_svalues.txt:3717-3728`, which already
> exists and already reads `INDUSTRY_production_gunpowder` — this just adds a second term beside
> it). This makes the building a real, direct gunpowder-output lever, not the "modest indirect
> booster" v2 settled for. `local_output_modifier` on the saltpetre/sulphur gate is KEPT as a
> secondary, genuinely-indirect bonus on top — it just isn't the building's main effect anymore.
> Skipped dyeworks' caching wrapper (`dyes_infra_cached`) for simplicity — traced its setter and
> found no dedicated `GOODS_cache_dyes_infra` caller anywhere, so dyes itself falls back to the
> inline compute every time in practice; calling the compute function directly for gunpowder is a
> plain, honest simplification, not a regression from an actually-used fast path.
>
> STATUS 2026-08-20: DRAFT v2 — round-1 adversarial review complete. Every code claim independently
> re-verified against the actual files (by the reviewer, and a second time by me before writing
> this revision). Findings incorporated:
>
> 1. **SHOULD-FIX (fixed): wrong tech gate.** v1 gated on `invention = tech_manufactories`
>    (requires `tech_mechanical_tools`, confirmed at `00_civic_inventions.txt:571-572` — a real,
>    gated civic-tree prerequisite). But `qing_machine_works_building` — the sibling this doc
>    itself should have used as the template, since it's the one ALREADY citing Jiangnan Arsenal
>    (`qing_industry_buildings.txt:111`: "江南製造局 — the Jiangnan Arsenal... 1865") — gates on
>    `invention = tech_weapon_manufacturing` instead, confirmed at `00_martial_inventions.txt:181`
>    to be a root/pre-modern tech with no `requires` at all. Switched the gate below to match. This
>    also answers v1's own open question #4: yes, `tech_manufactories` would have created exactly
>    the early-game gap it worried about, and there's a precedented fix, not a novel one —
>    `add_gunpowder_button` stays on `tech_manufactories` (unchanged, that's the generic system),
>    only this dedicated building moves to the earlier tech, exactly mirroring how machine_works /
>    `add_machine_parts_button` already split the same way.
> 2. **SHOULD-FIX (fixed): citation-tier mismatch.** Two of v1's three cited institutions
>    (兵仗局/火藥局, provincial 軍器局) predate 1763 and don't actually match a tech-gated modern
>    building — only the Jiangnan/Tianjin arsenals are genuinely `tech_weapon_manufacturing`-era.
>    Rewritten below to lead with Jiangnan Arsenal (now tech-matched) and cut the pre-1763
>    institutions from the MECHANICAL justification (they can stay as flavor-text color, clearly
>    separated, not as the tech-gate's citation). Also: the reviewer flagged real uncertainty about
>    whether 兵仗局 was actually a 工部 (Board of Works) institution rather than a Ming
>    eunuch-directorate Palace-Household office — the commonly-cited 工部 gunpowder bureau is
>    actually 王恭廠, not 兵仗局. I have NOT independently resolved this and am flagging it rather
>    than asserting either attribution; the flavor comment below uses 王恭廠 instead pending that
>    check, since it's the safer of the two claims, not because I've verified it either.
> 3. **SHOULD-FIX (fixed): honest framing of the mechanical effect.** v1 left open question #2
>    ("does local_output_modifier actually help gunpowder") unresolved. Re-traced the full chain
>    (`INDUSTRY_svalues.txt:4318-4436`): gunpowder factory output = a flat rate × the button-
>    assigned slot count × `owner.production_bonus_gunpowder` (confirmed a dead constant — grepped
>    every building/law/invention file in the repo, zero writers to `production_bonus_<good>` for
>    ANY good) × a country-wide shortage malus. `local_output_modifier` on a saltpetre/sulphur-
>    gated province only feeds that shortage-malus term indirectly, diffusely, country-wide — it
>    is NOT a direct gunpowder-output lever the building's name implies. Confirmed this is a
>    SYSTEMIC property of the whole `qing_industry_buildings.txt` family (steel_works/dyeworks have
>    the identical structural property), not a defect unique to this design, and there is no
>    precedented `on_built`-style direct-bump pattern anywhere in the repo to reach for instead
>    (zero `on_built` effects exist in any building file, grep-confirmed). Reframed below as an
>    honest "modest indirect supply booster," not oversold.
> 4. **NOTE (confirmed correct, no change): keep the raw-material `allow` gate, not a garrison
>    gate.** v1's open question #1 asked whether a garrison-presence gate would better match the
>    軍器局-at-garrisons citation. Checked: every saltpetre/sulphur province reachable by Qing
>    tops out at `civilization_value` 13 (confirmed directly, e.g. Weng'an = 5) — none would ever
>    clear a machine_works-style hard gate (`civilization_value >= 35`) even if one were wanted, so
>    dyeworks' softer shape was the right call, just not verified as such in v1. Separately,
>    `qing_banner_garrison_building`'s `potential` restricts it to `country_culture_group =
>    jurchen` only and it's seeded in a handful of named garrison cities — gating on it would make
>    this building near-unbuildable and functionally Jurchen-only, working against the whole point
>    (addressing gunpowder scarcity broadly). Kept `trade_goods = saltpetre OR sulphur`.
>
> Minor citation-hygiene fix: v1 cited `se_INDUSTRY_setup.txt:211` for
> `INDUSTRY_factories_assigned_gunpowder`; the correct line is 213.

## What's actually there today

Gunpowder's factory-tier production runs through `INDUSTRY_factories_assigned_gunpowder`
(`se_INDUSTRY_setup.txt:213`, `INDUSTRY_svalues.txt`), assigned via the generic
`add_gunpowder_button` / `remove_gunpowder_button` pair (`common/scripted_guis/
industrial_goods_buttons.txt:1508-1560`) — a governorship-wide abstract "industry slot" (created
by the base `IND_industrial_estate` building, `00_industrial_buildings.txt:1`) that the player
manually assigns to whichever good they want, gated on `invention = tech_manufactories`.

Separately, `qing_industry_buildings.txt` already has 10 dedicated, per-good Modern Industry
buildings (steel works, textile mill, machine works, navy yard, coal mine, telegraph, tongwen
guan, imperial university, dyeworks, Yunnan copper works), plus 4 more base-game-style ones in
`IND_heavy_industry_buildings.txt`. These do NOT touch `INDUSTRY_factories_assigned_<good>` at
all — confirmed by reading `qing_dyeworks_building` and `qing_machine_works_building` in full:
both are standalone buildings with native output-modifier fields, coexisting alongside their own
generic slot button (`add_dyes_button`, `add_machine_parts_button` both confirmed present) — same
dual arrangement steel has. **Gunpowder currently has the generic-slot half of this pattern and is
missing the dedicated-building half** — not a special case, parity with dyes/steel/machine_parts.

## Historical basis

Leading with the tech-matched institution, per round-1 review:

- **Jiangnan Arsenal** (江南製造局, est. 1865, 曾國藩·李鴻章) — the direct template precedent:
  `qing_machine_works_building` already cites this exact institution and gates on
  `invention = tech_weapon_manufacturing`. The arsenal had a dedicated powder/cartridge
  manufacturing department as a named sub-institution, not incidental production — this is the
  citation actually doing mechanical work here, matched to the tech gate below.
- Flavor-only context (pre-1763, NOT the tech-gate justification): the Ming-inherited armament
  bureau tradition the Qing continued from Beijing — cited here as **王恭廠** (the Board of Works'
  historically-attested gunpowder works) rather than 兵仗局, per the round-1 finding that 兵仗局's
  own institutional lineage (Ming eunuch-directorate vs. 工部) is unresolved and I have not
  independently verified it either way.

Source: Joseph Needham, *Science and Civilisation in China*, Vol. V:7, *Military Technology: The
Gunpowder Epic* (Cambridge, 1986).

## Building spec

Template: `qing_dyeworks_building` for the field shape (round-1 confirmed this soft-gate choice
is correct, not just copied by analogy — see finding #4 above), `qing_machine_works_building` for
the tech gate and historical citation.

```
qing_gunpowder_works_building = {
	# 火藥局 — the state gunpowder works, in the register of the Self-Strengthening arsenals:
	# 江南製造局 (Jiangnan Arsenal, 1865) ran a dedicated powder/cartridge department, the same
	# institution qing_machine_works_building already cites -- this building shares its tech gate
	# (tech_weapon_manufacturing, NOT tech_manufactories) for that reason, not by analogy to
	# dyeworks. Flavor lineage only (not the tech justification): the Ming-inherited Board of
	# Works gunpowder tradition, 王恭廠. Needham, SCC V:7, Military Technology: The Gunpowder Epic.
	# Distinct register from the cottage-tier powder mill (companion design doc, artisan/village
	# scale) -- this is state-organized manufacture. Coexists with the generic factory-slot button
	# (add_gunpowder_button, unchanged, stays on tech_manufactories), same dual arrangement dyes/
	# steel/machine_parts already have.
	#
	# REAL DIRECT EFFECT (v3 correction): mirrors qing_dyeworks_building's OWN named-building
	# production hook (GOODS_svalues.txt:3660-3676, its own comment: "mirroring clothing/naval_
	# supplies/munitions verbatim") -- a new GOODS_governorship_gunpowder_infra_output term, added
	# into the EXISTING GOODS_governorship_gunpowder_produced_mechanised, counts num_of_qing_
	# gunpowder_works_building directly via every_governorship_state{every_state_province{add=...}}
	# and adds a flat rate straight into gunpowder production -- a real per-building bonus, not an
	# indirect one. local_output_modifier below is a SECONDARY, genuinely-indirect bonus on top
	# (boosts whichever raw good the gated province produces) -- kept, but no longer the building's
	# main effect.
	local_proletariat_output = 0.20
	local_middle_strata_output = 0.08
	local_output_modifier = 0.15           # [ASSUMPTION, boot-tune] modestly above dyeworks'
	local_monthly_civilization = 0.03      #  0.12 -- a state arsenal outproducing a guild house
	local_state_trade_routes = 0.05        #  is the intended read, no clean numeric source exists

	cost = 200     # [ASSUMPTION] above dyeworks' 180 -- state/military institution, not a
	time = 480     #  merchant guild house; boot-tune

	allow = {
		owner = {
			OR = {
				country_culture_group = jurchen
				country_culture_group = chinese_group
			}
			invention = tech_weapon_manufacturing
		}
		sufficient_job_slots = yes
		NOT = { has_city_status = yes }
		OR = {
			trade_goods = saltpetre
			trade_goods = sulphur
		}
	}

	modification_display = {
		0 = local_proletariat_output
		1 = local_middle_strata_output
		2 = local_output_modifier
		3 = local_monthly_civilization
		4 = local_state_trade_routes
	}
}
```

## Open questions for review (round 2 / v3)
1. Is the 王恭廠-over-兵仗語 attribution swap actually correct, or does it need its own independent
   history pass before shipping the flavor comment (round-1's own hedge — not yet resolved)?
2. Is `GOODS_dyeworks_dyes_output = 2` the right magnitude to benchmark a `GOODS_gunpowder_works_
   gunpowder_output` rate against, or does gunpowder's different demand/price profile (already
   the subject of the boot-log investigation that motivated both these designs) warrant a
   different flat rate?
3. Is it safe to skip the `dyes_infra_cached`-style caching wrapper, given no dedicated cache-setter
   for dyes itself was found — i.e. is the inline `_compute` call actually cheap enough every
   quarter, or does `every_governorship_state{every_state_province{...}}` have a real perf cost at
   world scale that the existing dyes precedent is already quietly paying and this would add to?
3. Are the cost/time/magnitude "boot-tune, no clean numeric source" bumps over dyeworks defensible?
