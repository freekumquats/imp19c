# DESIGN — #66 TWO factory-tier Qing buildings: dyeworks, Yunnan copper works (Foshan ironworks
# FOLDED to generic per round-2 review, see below)

> STATUS 2026-08-14: FINAL v4 — round-3 adversarial review complete, VERDICT: READY FOR
> IMPLEMENTATION. Round 3 independently re-verified both round-2 fixes against live source:
> Xiushui genuinely clears every remaining `allow` clause once `set_trade_goods = dye` runs
> (confirmed `NOT = { has_city_status = yes }` passes at settlement rank), dropping the
> factory-slot-capacity gate is mechanically safe (the MG-hook mechanism never reads it — traced
> directly), Foshan has zero remaining scoped-in references anywhere in the doc, the corrected
> iron count (5, not 7) is stated consistently everywhere, and the copper strata choice
> (`local_indentured_output`, matching salt) survives an independent sweep of every other
> extraction/mining building in the mod for a closer sibling (none found). One MEDIUM
> documentation-precision fix applied: the dyeworks/copper gate isn't literally "cottage-tier
> shaped" (true cottage buildings omit `sufficient_job_slots` entirely) — it's a hybrid matching
> `qing_silk_filature_building`/`qing_salt_yard_building`'s named-works pattern instead; corrected
> the inline comment, no mechanical change. Remaining open items (magnitude/cost/time tuning, the
> dyes cache-writer's exact current call-site re-trace) are implementation-time work, not design
> gaps — both already flagged as such in the doc's own open-questions list.
>
> STATUS (superseded, kept for provenance): round 2 found ONE CRITICAL
> and settled the doc's own most-important open question. **(CRITICAL, C1)** round 1's Xiushui
> reassignment fix only satisfied ONE of the dyeworks building's four `allow` clauses —
> `trade_goods = dye` — but the building ALSO requires `has_city_status = yes` AND
> `civilization_value >= 30` (it mirrors `qing_textile_mill_building` exactly, gate included).
> Xiushui is `province_rank="settlement"` (not city) and `civilization_value=13` — round 2
> confirmed via direct sweep of Jiangxi/Anhui/Fujian/Hubei/Hunan that ZERO provinces in that
> region are simultaneously city-rank AND civ>=30; the building remained permanently
> unbuildable even after round 1's "fix." **Resolved below by dropping the city-status/civ-value
> gates entirely** — the dyeworks building keeps `trade_goods = dye` + `invention =
> tech_manufactories` + `sufficient_job_slots = yes`, matching the SAME cottage-tier-shaped gate
> the Foshan/copper buildings already used (`NOT = { has_city_status = yes }`), not the harder
> textile-mill shape. This also resolves round 2's own MEDIUM #1 finding (the doc had, without
> explanation, given dyeworks the harder factory-tier gate while giving Foshan/copper the softer
> cottage-tier gate) — all three (now two) buildings use the SAME gate shape consistently.
>
> **(Foshan verdict, the doc's own round-1 open question #6, now RESOLVED, round 2): Foshan
> ironworks FOLDS TO GENERIC.** Round 2 checked Foshan's citation against BOTH available bars
> directly — the timber/indigo financial-instrument bar (which the doc already admitted failing)
> AND the softer salt state-fiscal-scale bar the doc downgraded to. Neither holds: Foshan's
> citation ("10 workshops, 100 foundries, named guilds, merchant-organized") describes PRIVATE
> guild/merchant organization, not a state revenue apparatus comparable to salt's actual
> fiscal-administration role — the "softer bar" was a goalposts-move, not a genuine downgrade to
> a bar that's still met. This is the same failure mode silk's citation hit in #58 (scale +
> documentation + named organization, without a genuine institutional/fiscal distinction). Unlike
> silk, folding Foshan does NOT create redundancy (no other Qing-exclusive iron building exists at
> any tier once #58's smithy also goes generic) — so the mod ends up with zero dedicated
> Qing-exclusive iron building, which is the correct, principle-consistent outcome, not a
> shortfall. **`qing_foshan_ironworks_building` is REMOVED from this task's scope below.**
>
> **(HIGH #1, corrected)**: the doc's own "confirmed via direct grep" iron province count was
> wrong — claimed 7, independently recounted at **5** (Guangdong/Foshan, Shandong/Laiwu,
> Shanxi/Changzi, Taiwan/Taichung, Yunnan/Tiechang). Moot now that Foshan folds to generic (no
> building reads this count anymore), but corrected for the historical record. The copper count
> (8, 3 in Yunnan) was independently re-verified and is correct, unchanged.
>
> **(MEDIUM #2, resolved)**: the copper works' `local_indentured_output` strata choice (open since
> round 1) — round 2 found `qing_coal_mine_building` (the OTHER extraction-building comparison)
> uses `local_proletariat_output`, contradicting salt's `local_indentured_output` precedent. Since
> copper is graded throughout this doc against SALT's bar specifically (state-monopoly
> administration), not coal's, resolved by explicitly picking salt's strata pattern and stating
> why, rather than leaving a round 3 to get a mixed signal from checking coal.
>
> STATUS (superseded, kept for provenance): round 1 found: (HIGH #1) both
> Foshan ironworks and Yunnan copper works were drafted with ZERO invention gate — every other
> building in `qing_industry_buildings.txt` (including the doc's own cited precedent,
> `qing_steel_works_building`) requires one; fixed below with `invention = tech_manufactories` on
> both. (HIGH #2, informational) the iron/copper `allow` gates are empire-wide on the raw good, not
> geographically restricted to Foshan/Yunnan specifically — confirmed this MATCHES existing
> convention (`qing_steel_works_building`/`qing_salt_yard_building` are the same shape), so not a
> defect, but now stated explicitly rather than implied place-exclusivity the mechanism doesn't
> deliver. (MEDIUM #3) Foshan's `has_city_status` gate is confirmed SAFE — Foshan (province 9301)
> is coded `province_rank="settlement"`, so `NOT = { has_city_status = yes }` currently passes
> there — but flagged as fragile (a future city-status bump, which this mod has done elsewhere,
> would silently lock the building out of the one place the citation is about). (MEDIUM #4)
> Foshan's citation does NOT actually clear the timber/indigo innovation bar the doc originally
> claimed parity with — "10 workshops, 100 foundries, named guilds" is a scale/organization claim,
> the same shape that failed for silk, not a documented financial/tenure innovation. Downgraded
> below to the SOFTER, already-accepted "distinctive by scale/state-fiscal-role" bar (matching
> `qing_salt_yard_building`'s own justification standard), not claimed parity with timber/indigo.
> (MEDIUM #5) Yunnan copper's citation, by contrast, DOES clear ITS correct comparison bar (state-
> monopoly administration, matching salt's precedent) — confirmed sound as-is. (INFORMATIONAL #9,
> the most severe finding) **the dyeworks building's `trade_goods = dye` gate has ZERO eligible
> CHI province under current 1763 setup data** — grepped every China-region province file, zero
> hits for `trade_goods="dye"` anywhere. As drafted the building would be permanently unbuildable.
> Fixed below by identifying a real, historically-apt province to reassign via `set_trade_goods`
> (a proven idiom, `se_QING_COLON.txt:361/466`) — Xiushui (修水), Jiangxi, province 5809, is a
> direct geographic match for "寧州" in the 1792 Yining/Xiushui property-division document the
> whole citation is built on.

## Task text

User: fold three sourced Qing-distinctive institutions (indigo/dye, Foshan guild ironworking,
Yunnan copper monopoly) into one task, as factory-tier buildings — `qing_industry_buildings.txt`,
alongside the existing named Qing works (`qing_steel_works_building`, `qing_textile_mill_building`,
`qing_machine_works_building`, `qing_navy_yard_building`), not cottage-tier.

**[round-2 revision]** Of the three, Foshan ironworking's citation did NOT survive honest grading
against either available Qing-distinctiveness bar (see Building 2's fold section below) — this
task now delivers TWO buildings (dyeworks, Yunnan copper works), not three, with Foshan's
citation-check documented as a legitimate "does not clear the bar" outcome, not a shortfall.

## Ground truth — two DIFFERENT production mechanisms, confirmed by direct trace, not assumed

The two surviving buildings do NOT share one mechanism (iron's row below is retained only for the
historical record — building 2, `qing_foshan_ironworks_building`, is REMOVED per round 2's fold
decision; iron needed no NEW mechanism anyway, so nothing here needs unwinding). Checked each
good's actual production model in source before designing:

| Good | Model | Evidence |
|---|---|---|
| `dyes` | Factory-slot, MG-hook-eligible | `INDUSTRY_factories_assigned_dyes` real (player-assignable, `industrial_goods_buttons.txt:1562-1620`, gated `tech_manufactories`); `GOODS_governorship_dyes_produced_mechanised` exists (`GOODS_svalues.txt:3645-3656`) with the exact `if has_variable=INDUSTRY_factories_assigned_dyes { add=INDUSTRY_production_dyes }` shape the MG-hook pattern already extends for clothing/naval_supplies/munitions. COTTAGEIND stub confirms cottage cannot produce it (`se_COTTAGEIND.txt:648-652`). |
| `copper` | Pure raw good, NO factory-slot layer | `GOODS_governorship_copper_produced` (`GOODS_svalues.txt:1579-1590`) is a bare `every_governorship_state { add = num_goods_produced } × MODIFIER_mining_productivity` — vanilla raw province output. Confirmed NO `INDUSTRY_factories_assigned_copper` exists anywhere. The MG-hook pattern (a fourth term added to a `_mechanised` split) does NOT apply — there is no `_mechanised` split for copper at all. |
| ~~`iron`~~ | *(removed, round 2 — kept for provenance)* | `GOODS_governorship_iron_produced` (`:1592-1603`) is the identical bare raw-output shape as copper. Moot: no building reads this anymore. |

So dyes gets the proven MG-hook cached-term pattern; copper gets the OTHER proven pattern already
used by `qing_steel_works_building` itself — a plain `base_resources` bonus on the building,
stacking with the province's own raw output the same way every raw-good building in this mod
already works (silk filature, porcelain kiln, salt yard, the #58 cottage buildings, etc.). This is
NOT a new mechanism for copper — it's the SAME mechanism the mod already uses for raw goods
everywhere; only dyes needs the newer MG-hook pattern because dyes lives one layer higher
(finished good, factory-assignable).

## Building 1 — `qing_dyeworks_building` (indigo → `dyes`)

### Historical grounding
1792 Yining/Xiushui property-division document (寧州懷遠護仙坑陳何邱三姓析產分關案卷): three
lineages (Chen, He, Qiu) divided jointly-owned indigo-processing infrastructure (ponds, pools,
vaults — 藍窖場/靛塘/靛池/藍坪) into 21 registered, tradable, inheritable shares. Documented
follow-on sale contracts: 1811 (He family sold ponds for 49 taels), 1823 (Chen brothers
consolidated ownership), 1841 (He family sold half-ownership of a pool for 1 tael) — a genuine,
decades-long paper trail of a share market, not a one-off pooling arrangement (contrast with
sugar's 糖廍, which #58 correctly kept generic — seasonal capital-pooling, no registered/tradable
instrument). Plus a dedicated commodity-specific guild: Tingzhou merchants built branded
"Indigo Guild House" (靛青會館) houses in Shanghai, Zhapu, and Lanxi specifically for the indigo
trade, distinct from ordinary native-place guilds.

### Mechanism — mirrors `qing_textile_mill_building` exactly, MG-hook production term
```
qing_dyeworks_building = {
	# 靛青會館 / indigo guild houses — [flavor citing the 1792 Yining/Xiushui share-division
	# document + the Tingzhou merchants' dedicated Indigo Guild House network, Shanghai/Zhapu/
	# Lanxi]. A registered, tradable-share processing institution turning household-grown/
	# gathered dye into refined indigo dyestuff at commercial scale.
	local_proletariat_output = 0.20        # [ASSUMPTION, boot-tune — no source gives a clean
	local_middle_strata_output = 0.08      #  output-per-building figure; calibrated near
	local_output_modifier = 0.12           #  qing_textile_mill_building's own magnitudes as the
	local_monthly_civilization = 0.03      #  nearest sibling of comparable historical scale]
	local_state_trade_routes = 0.08

	cost = 180     # [ASSUMPTION] slightly below textile mill's 200 — a smaller trade in absolute
	time = 450     #  volume than cotton/silk cloth; boot-tune

	allow = {
		owner = {
			OR = { country_culture_group = jurchen  country_culture_group = chinese_group }
			invention = tech_manufactories
		}
		# [round-2 fix, CRITICAL C1] DROPPED has_city_status/civilization_value/factory-slot-
		# capacity gates. v2 mirrored qing_textile_mill_building's harder factory-tier gate shape,
		# but Xiushui (the ONLY eligible dye province after the round-1 reassignment) is
		# province_rank="settlement", civ=13 -- neither clause is satisfiable there, and no other
		# CHI province in the region clears BOTH clauses either (round-2 swept Jiangxi/Anhui/
		# Fujian/Hubei/Hunan directly). The building would have been permanently unbuildable.
		# [round-3 precision fix] this gate is NOT true cottage-tier shape (cottage buildings omit
		# sufficient_job_slots entirely, per qing_cottage_buildings.txt's own header) -- it's a
		# hybrid matching qing_silk_filature_building/qing_salt_yard_building's named-works
		# pattern instead (sufficient_job_slots=yes + trade_goods=X, no city/civ gate). Same
		# hybrid shape the copper works building uses -- consistent between the two, just not
		# literally "cottage-tier."
		sufficient_job_slots = yes
		NOT = { has_city_status = yes }
		trade_goods = dye
	}
}
```
Production hook (new, following the proven MG-hook shape verbatim — `GOODS_svalues.txt:3086-3106`
is the literal template):
```
GOODS_governorship_dyes_produced_mechanised = {
	... existing body unchanged ...
	add = GOODS_governorship_dyes_infra_output          # NEW disjoint term
}
GOODS_governorship_dyes_infra_output = {
	if = { limit = { has_variable = dyes_infra_cached }  value = var:dyes_infra_cached }
	else = { value = GOODS_governorship_dyes_infra_output_compute }
}
GOODS_governorship_dyes_infra_output_compute = {
	value = 0
	if = { limit = { owner = { invention = tech_manufactories } }
		every_governorship_state = { every_state_province = {
			add = { value = num_of_qing_dyeworks_building  multiply = GOODS_dyeworks_dyes_output }
		} }
	}
}
GOODS_dyeworks_dyes_output = { value = 2 }   # [ASSUMPTION] matches textile mill's clothing rate=2
```
Cache writer: extend the SAME per-governorship pass already extended twice for
`clothing_infra_cached`/`naval_supplies_infra_cached` to also write `dyes_infra_cached` — one walk,
not a new one (matching the existing G4 discipline).

### Province anchor — CORRECTED (round-1 review, most severe finding)

Round 1 found `trade_goods = dye` has **ZERO eligible CHI province under current 1763 setup
data** — grepped every China-region province file in `setup/provinces/*.txt`; zero hits for
`trade_goods="dye"` anywhere in Qing territory. The good exists (`common/trade_goods/
00_imp19c.txt:576`) and has real factory infrastructure (`INDUSTRY_factories_assigned_dyes`), but
no province anywhere in China currently carries it as its trade good — as drafted, this building
would be **permanently unbuildable**, a real blocker, not a footnote.

**Fix: reassign a real, historically-apt province via `set_trade_goods`** (a proven idiom already
used for exactly this kind of targeted good-reassignment — `se_QING_COLON.txt:361` and `:466`,
the sweet-potato spread mechanic). Found the correct target by tracing the citation's own
geography: the 1792 property-division document is titled 寧州懷遠護仙坑陳何邱三姓析產分關案卷 —
**寧州 (Ningzhou) is the historical name for Xiushui County (修水縣), Jiangxi**. This mod's
province list has an EXACT match: **`5809={ #Xiushi`, `setup/provinces/00_Jiangxi.txt:359-372`**
— currently `terrain="farmland"`, `culture="gan"`, `religion="daoism"`, `trade_goods="tea"`,
`civilization_value=13`, `province_rank="settlement"`, CHI-owned. This is not a guess at a
plausible region — it is the actual named county the citation is about, confirmed present in this
mod's own province set under its historical name (修水 renders as "Xiushi" in this mod's naming).

**Implementation**: at setup (a one-time `set_trade_goods = dye` on province 5809, either in
`setup/main/00_default.txt` directly or via a boot-time effect mirroring how other historical
good-corrections are applied elsewhere in this mod) reassign Xiushui from `tea` to `dye` before
the `qing_dyeworks_building`'s `allow` gate is ever checked. [OPEN QUESTION, round 2] should this
reassignment happen at raw setup (permanent, simplest) or via a scripted one-time effect (more
consistent with how #58's timber-tenure-adjacent research treats other place-specific
reassignments)? Recommend raw setup — this is a factual correction to the map's trade-good
seeding (Xiushui genuinely grew/processed indigo historically), not a gameplay-triggered event,
matching how `trade_goods=` values are set for every other province in this file already.

## Building 2 (REMOVED, round 2) — `qing_foshan_ironworks_building` folds to generic

### Why this building is REMOVED, not built (round-2 review, resolving the doc's own round-1
### open question #6 — the single most important question that round flagged)

Round 1 downgraded Foshan's justification bar from the timber/indigo financial-instrument
standard (which it admitted failing) to a softer "distinctive by scale/state-fiscal-role"
standard matching `qing_salt_yard_building`. Round 2 checked this softer bar directly and found
it is ALSO not cleared: `qing_salt_yard_building`'s own justification is that the 鹽政 salt
administration was "one of the largest single sources of QING STATE REVENUE" — a formal, taxed,
audited fiscal apparatus. Foshan's citation ("10 workshops, 100 foundries, named craft guilds,
merchant-organized production") describes PRIVATE guild/merchant organization — there is no claim
anywhere in the sourcing that Foshan iron was a state revenue stream comparable to salt. The
"downgrade to a softer bar" was, on inspection, a goalposts-move: rephrasing "practiced at
documented scale with named organizations" so it sounds like a fiscal-role claim without actually
being one. This is the exact failure mode #58 already established for silk (scale + names +
documentation is not, on its own, evidence of institutional distinctiveness) — Foshan's citation
does not distinguish itself from ordinary pre-industrial guild ironworking practiced at
comparable scale elsewhere (contemporary Japan, Sweden's Bergslagen, the English Midlands), and
no comparative check ruling those out has been done, the same gap that sank silk's first draft.

**Unlike silk, this is NOT a redundancy fold** — #58's `qing_cottage_smithy_building` (iron,
cottage tier) is itself folding to generic per DESIGN_58, so once both changes land, the mod will
have ZERO dedicated Qing-exclusive iron building at any tier. This is the correct, principle-
consistent outcome under this project's own stated rule ("the principle cuts both ways, not a
failure of the task") — not a gap to backfill with a weaker citation.

`qing_foshan_ironworks_building` is REMOVED from this task's scope. Iron remains a purely generic
raw good, boosted only by the (now-generic) cottage smithy building, same as any other CHI
province producing iron.

## Building 3 — `qing_yunnan_copper_works_building` (Yunnan copper monopoly → raw `copper`)

### Historical grounding — confirmed sound against the CORRECT comparison bar (round-1 MEDIUM #5)
Yunnan's 滇銅 (dianju) system: a state-quota, monopoly-adjacent copper mining-and-smelting
institution feeding the imperial mints (copper cash coinage) — miners operating under state
quota, output shipped to Beijing. This is an administrative/fiscal institution, graded correctly
against `qing_salt_yard_building`'s own accepted state-monopoly-administration bar (NOT the
timber/indigo financial-instrument bar this doc's "Ground truth" section originally conflated it
with) — under the correct bar, this citation passes cleanly, confirmed by round-1 review.
Genuinely Qing-distinctive: a state-administered mining/coinage-feed institution, not a household
or even ordinary guild-merchant arrangement — closer in character to a state monopoly than the
private guild-organized manufactories building 2's fold above found insufficient for Foshan.
Copper is NOT symmetric with Foshan's case: this is an actual state-quota fiscal institution, not
a private-guild claim re-graded to look like one.

**Province count corrected (round-1 HIGH #2, re-verified round 2)**: `trade_goods="copper"`
exists in **8 CHI provinces total**, not just Yunnan — Gansu ×1, Guizhou ×3, Sichuan_Kham ×1,
PLUS 3 in Yunnan (confirmed: 502 Panzhihua, 2418 Qujing, 3315 Pu'er, `setup/provinces/
00_Yunnan.txt`). Round 2 independently re-confirmed this count is correct (unlike the doc's iron
count, which round 2 found was wrong at 7 — now moot since building 2 is removed). Same
empire-wide-gate reality — matches existing convention, not a defect, but the building's
Yunnan-specific flavor/name implies more geographic exclusivity than the mechanism delivers.

### Strata choice RESOLVED (round-2 fix, was open question #3) — `local_indentured_output` kept,
### explicitly picking salt's precedent over coal's
Round 1 left this as an open "verify against `qing_coal_mine_building`" question. Round 2 checked
both comparison siblings directly and found they DISAGREE: `qing_coal_mine_building` uses
`local_proletariat_output` (no indentured term at all), while `qing_salt_yard_building` — the bar
this ENTIRE building's justification is graded against, per the section above — uses
`local_indentured_output = 0.5` alongside `local_lower_strata_output`. Since copper's whole case
rests on matching salt's state-monopoly-administration bar (not coal's, which is a modern
1878-founded mechanised colliery with no historical monopoly/quota framing), the strata choice
should follow the SAME sibling the historical justification follows. **Decision: keep
`local_indentured_output`, explicitly because it matches salt (the bar being used), not because it
was independently verified against a labor-status source — this is a consistency choice, not a
separately-sourced calibration.**

### Mechanism — same `base_resources` pattern `qing_steel_works_building`/`qing_salt_yard_
### building` already use (copper has no factory-slot layer to hook into)
```
qing_yunnan_copper_works_building = {
	# 滇銅官運商銷 — the Yunnan copper monopoly: state-quota mining and smelting feeding the
	# imperial mints (制錢), administered copper output shipped to Beijing for coinage. A
	# state-organized institution distinct from ordinary merchant-guild manufactories or
	# household cottage bronze-casting.
	local_lower_strata_output = 0.20
	local_indentured_output = 0.15   # [round-2 fix] kept, matching qing_salt_yard_building's
	                                   # own strata pattern -- the bar this building's historical
	                                   # justification is graded against (state-monopoly
	                                   # administration), not qing_coal_mine_building's (a
	                                   # modern mechanised colliery with no monopoly framing).
	local_tax_modifier = 0.05         # reflects the state-fiscal (mint-feeding) character
	base_resources = 1.5              # [ASSUMPTION, boot-tune] no source gives a clean numeric
	                                   # yield multiplier; the qualitative citation is
	                                   # administrative/fiscal scale, not a yield figure.

	cost = 150
	time = 360

	allow = {
		owner = {
			OR = { country_culture_group = jurchen  country_culture_group = chinese_group }
			invention = tech_manufactories   # [round-1 HIGH #1 fix] matches every sibling in the file
		}
		NOT = { has_city_status = yes }
		trade_goods = copper
	}
}
```

## Building 4 candidate (NOT built in this task — stub only, per the cottage-finished-goods
## doc's round-2/round-3 routing note, landed here so the citation isn't lost)

`design/DESIGN_COTTAGE_FINISHED_GOODS_BUILDINGS.md` routed a real, sourced citation here: **Xuan
paper (宣紙), Jing County (涇縣), Anhui** — lineage-controlled production (traditionally the
Cao/曹氏 clan of Xiaoling township, trade-secret transmission within the lineage since Ming/
early-Qing), organized under a licensed workshop/guild system with imperial-tribute grade control
(貢紙). This clears the SAME bar timber/indigo cleared (a documented, distinctive institutional
form, not mere scale) and operates at licensed-workshop/tribute scale — matching this doc's own
dyeworks/copper-works buildings' tier, not the cottage tier. Proposed name:
`qing_xuan_papermill_building`, gated `trade_goods = wood` (paper's raw input, same good the
cottage papermill building also gates on — province-anchor eligibility not yet checked; unlike
dye, wood is NOT a rare good in CHI territory, so a zero-eligible-province problem is unlikely
here but not yet confirmed) plus `invention = tech_manufactories`, mechanism TBD (paper's
`_produced_mechanised` split needs the same trace this doc gave dyes/copper before choosing the
MG-hook pattern vs. a plain `base_resources` bonus — NOT yet done). **Not built, not designed in
detail — this stub exists so the citation has a landing place in the doc that will eventually own
it, per this project's own "log the citation, don't lose it" discipline.** Building this out is a
follow-up, tracked here, not folded into this task's own scope.

## Non-goals / explicitly NOT changed
- `qing_steel_works_building`, `qing_textile_mill_building`, `qing_machine_works_building`,
  `qing_navy_yard_building`: untouched, cited only as the precedent/comparison each new building
  is checked against.
- COTTAGEIND recipes, #58's cottage buildings, the finished-goods cottage doc's 3 buildings:
  untouched, fully separate files/mechanisms.
- `qing_xuan_papermill_building` (building 4 candidate above): NOT built in this task — stub only.
- `qing_cottage_smithy_building` (iron, cottage tier): untouched by THIS doc — its own fold to
  generic is #58's scope, cited here only because it's why Foshan's fold (above) leaves zero
  Qing-exclusive iron building anywhere, not a gap this doc needs to backfill.

## Open questions for round 3

1. **[RESOLVED, round 2]** Foshan's `has_city_status` gate fragility question — MOOT. Foshan
   ironworks is removed entirely per round 2's fold decision; there is no building left for a
   future city-status promotion to silently break.
2. **[RESOLVED, round 1, corrected round 2]** Full province lists — dye: ZERO under the original
   gate (fixed via Xiushui reassignment AND, per round 2's CRITICAL fix, dropping the
   city-status/civ-value gates that made Xiushui insufficient on its own); iron: round 1 claimed 7
   provinces, round 2 independently recounted and found the true figure is **5** — moot now since
   the building is removed, but corrected for the record; copper: 8 provinces empire-wide (3 in
   Yunnan), re-confirmed accurate by round 2.
   empire-wide (3 in Yunnan). All confirmed via direct grep, not assumed.
3. **[RESOLVED, round 2]** Strata output choice for the copper works (`local_indentured_output`)
   — round 1 left this open; round 2 found `qing_coal_mine_building` and `qing_salt_yard_building`
   give CONTRADICTING signals (coal uses `local_proletariat_output`, no indentured term; salt uses
   `local_indentured_output` alongside lower-strata) and resolved by explicitly picking salt's
   pattern, since copper's ENTIRE historical justification is graded against salt's bar, not
   coal's (a modern 1878 mechanised colliery with no monopoly/quota framing).
4. All magnitude/cost/time constants — still pure [ASSUMPTION], needs boot-log tuning. Unchanged
   by round 2's fixes.
5. Dyes MG-hook cache-writer extension — still needs the exact current call-site trace (the
   function has been extended MORE times than this doc's v1 assumed — round 3 should re-verify
   against current source, not the v1 citation, since other tasks may have extended it further
   in the meantime).
6. **[RESOLVED, round 2 — this was the single most important open question from round 1]**
   Foshan's citation does NOT clear either available bar — not the timber/indigo financial-
   instrument bar (already admitted failing) NOR the softer salt state-fiscal-scale bar it was
   downgraded to (round 2 checked directly: Foshan's guilds are private/merchant organization,
   never claimed as a state revenue apparatus comparable to salt's actual fiscal role). **Verdict:
   Foshan folds to generic, consistent with #58's harder line on silk** — the "softer bar" was a
   goalposts-move that round 2 found doesn't survive direct comparison. `qing_foshan_ironworks_
   building` is REMOVED from this doc.
7. **[RESOLVED, round 1, moot after round 2]** The Xiushui province reassignment (dye) — round 1
   confirmed `set_trade_goods` at raw setup is the right mechanism and no other mechanic depends
   on Xiushui's `tea` good. Round 2 found the reassignment ALONE still left the building
   unbuildable (see CRITICAL C1 fix above, dropping the city-status/civ-value gates) — the
   reassignment itself remains correct and unchanged, just no longer sufficient on its own.
8. **New, round 2**: confirm the dyeworks building's now-corrected gate (dropped
   `has_city_status`/`civilization_value >= 30`/factory-slot-capacity, matching the copper works'
   cottage-tier-shaped gate) doesn't undermine the building's own factory-tier MG-hook production
   mechanism — the MG-hook pattern itself doesn't require city status (it's about which
   `_produced_mechanised` term gets read, not where the building can be sited), but round 3 should
   double check no OTHER factory-tier building in this file relies on the city/civ gate for a
   reason this doc hasn't considered (e.g. factory-slot capacity accounting).