# DESIGN — #58 research-back cottage-building culture gating, generic-ize what isn't Qing-specific

> STATUS 2026-08-13: DRAFT v2 — round-1 adversarial review complete. Round 1 independently
> re-assessed all 8 per-good historical calls using its own economic-history knowledge (Pomeranz,
> Bray, Huang) rather than just checking the draft's citations, and found: (a) the silk
> citation offered in v1 ("household reeling feeds urban filatures") does NOT hold up — that
> pattern is close to the DEFAULT everywhere silk was produced pre-industrially (documented for
> Tokugawa/Meiji Japan, Ottoman Bursa/Mount Lebanon, Bengal, Piedmont/Lombardy), so v1 was
> smuggling in scale/fame as if it were distinctiveness, exactly the move the user's own principle
> rules out — **silk now folds to generic too, pending a much sharper citation than any offered
> so far (a specific FISCAL linkage or a documented Jiangnan-specific brokerage institution, not
> "household reeling exists")**; (b) the textile fold's STATED rationale (v1: "redundant with
> `qing_cotton_workshop_building` because both are household-scale") was mechanically wrong — that
> building requires `sufficient_job_slots`, the cottage tier deliberately doesn't, so they are NOT
> mechanic-redundant — but the fold CONCLUSION was still right for a different reason (Pomeranz's
> actual thesis is comparability, not Chinese distinctiveness, between Yangzi-delta and English
> cottage textile production), now corrected below; (c) the restructure plan as drafted would
> REGRESS Qing macro-builder access from 8 buildings to 0 (the generic building has never had
> macro-builder wiring — it was explicitly excluded, mirroring row_manufactory/row_plantation) —
> fixed by adding an explicit wiring step; (d) the cleanup file list was incomplete (missed
> `province_window.gui` and `macro_builder_view.gui` per-building entries) — completed below; (e)
> the `allow`->`potential` gate-type change was previously unflagged — now flagged. Working
> conclusion after this round: **0 of 8 cottage buildings currently clear the "genuinely
> Qing-specific" bar** — a legitimate result under the user's own stated principle, not a
> deficiency.
>
> STATUS 2026-08-13: DRAFT v3 — round-2 adversarial review complete. Round 2 independently
> re-derived the silk verdict from scratch (using Elvin, Pomeranz, Li Bozhong, Bray, Meng Zhang)
> rather than just checking round 1's reasoning, and confirmed the fold MORE decisively than round
> 1's own hedged language: Qing silk sourcing for the Imperial Manufactories ran through market
> brokers (絲行/絲棧) rather than a distinctive tribute/fiscal pipeline, meaning it is structurally
> CLOSER to Bursa/Lyon/Lombardy's market-intermediated putting-out than round 1 even argued — the
> "materially sharper citation" that could rescue silk does not appear to exist. Round 2
> independently re-hunted for a missed counter-example across the other 7 goods and found one
> legitimate near-miss (Meng Zhang's documented Huizhou/Fujian LINEAGE-managed forest-tenure
> system for wood) that does NOT flip wood's verdict (it describes timber ESTATE TENURE, not the
> simple village woodlot the mod's building actually models) but is logged below as a documented,
> inapplicable citation so it isn't rediscovered and misapplied later. Round 2 found ONE NEW HIGH
> issue: the cleanup file list, even after v2's "completed" correction, still missed
> `gui/shared/gui_templates.gui` and `gui/shared/custom_tooltip.gui` (16 per-building blocks EACH
> — 8 buildings × build_item + macro_build_item, and × tooltip + macro-tooltip, respectively) and
> did not explicitly call out deleting the entire loc file `qing_cottage_buildings_l_english.yml`
> — fixed below. Round 2 also confirmed the macro-builder-fix necessity (option (a), not (b)) is
> correct: this mod's design assumes a Qing-only human player, so — unlike the ORIGINAL
> row_manufactory/row_plantation exclusion, which has no cost to Qing since Qing never needs those
> buildings — excluding the widened generic cottage building from the macro builder WOULD have a
> real cost, since it becomes Qing's only surviving cottage-tier coverage. Working conclusion
> (0-of-8, including silk) now CONFIRMED by 2 independent review rounds — not re-opened for a
> round 3 on the historical judgment; round 3, if any, should focus only on the mechanical
> cleanup-completeness fix below.
>
> STATUS 2026-08-14: FINAL v8 — round-3 adversarial review complete, VERDICT: READY FOR
> IMPLEMENTATION. Round 3 independently re-verified all 4 of round 2's substantive fixes (Fujian
> count/list, the 3 named stale comments, the row-capacity redistribution math, the 8+2=10
> building-count arithmetic) against real source — all held up. Round 3's own contribution was
> finding round 2's stale-comment sweep was ITSELF incomplete (a 4th "eight Qing cottage buildings"
> comment at `gui/shared/gui_templates.gui:1495`, a separate macro-builder template block from the
> one at `:615`) plus 3 smaller text-consistency nits (a stray "nine Qing buildings," an off-by-one
> "7 of the 8" that should read "8 of 8," and a stale "13 terrain-candidates" cross-reference that
> never got updated to 14). All fixed above — pure documentation-consistency corrections, zero
> effect on the actual mechanical plan (province IDs, GUI targets, row math all already verified
> correct by round 2). The 2 historical-geography judgment calls (final timber Fujian subset, final
> sugarhouse province subset) remain legitimately open — no in-repo research resolves either —
> and correctly do NOT block this ready verdict; they're implementation-time research tasks, not
> design defects.
>
> STATUS 2026-08-14 (superseded, kept for provenance): DRAFT v7 — round-2 adversarial review complete. Round 2 independently
> re-verified round 1's 5 fixes against live source: 4 held cleanly (the 4-file cleanup list, the
> `hui`-culture religion check, the sugar province list, the Taiwan-has-no-sugar-province claim).
> One did NOT fully hold: round 1's OWN "checked directly" Fujian terrain sweep was itself
> incomplete — Fujian has 25 provinces, not 24, and the terrain-qualifying candidate list has 14
> members, not 13 (round 1 missed Hua'an, 4247, `terrain="forest"`, meeting the exact same
> criterion as 2 already-included provinces). Fixed above with the corrected count/list. Round 2
> also found and fixed: 3 more stale "eight Qing cottage buildings" header comments beyond the one
> round 1 already flagged (`gui/shared/gui_templates.gui:615`, `gui/shared/custom_tooltip.
> gui:912`, `gui/macro_builder_view.gui:294-301`); muddled building-count arithmetic in open
> question 9 (corrected to the clean 8-survive + 2-new = 10 total, not the confusing "7 + ... + the
> deleted ROW generic" framing); and — this round's main deliverable — a CONCRETE, evidence-backed
> resolution for the row-capacity risk round 1 only flagged: append both new buildings to the
> EXISTING Row2 (4→6 items, 396px, well inside this file's own proven ≤462px-safe / ≥528px-unsafe
> boundary), no third row needed, zero `gui_templates.gui` template changes required. Round 2 also
> confirmed the 2 remaining historical-geography judgment calls (final timber Fujian subset, final
> sugar province subset) are genuinely unresolvable from anything in this repo's own research
> docs — left explicitly open, not manufactured a false resolution.
>
> STATUS 2026-08-14 (superseded, kept for provenance): DRAFT v6 — round-1 review of the v5
> restructure complete. Round 1 found: (1,
> CRITICAL) the cleanup-completeness claim ("row_cottage_workshop_building has no GUI/loc wiring,
> comment/definition-only deletion") is FALSE against CURRENT source — `#101`'s implementation
> (commit `b7b223729`, this session) gave it full wiring: `gui/shared/gui_templates.gui:607-614`,
> `gui/shared/custom_tooltip.gui:902-911`, `gui/province_window.gui:4473-4489`, and loc keys in
> `localization/english/row_buildings_l_english.yml:18-19,24`. Fixed below — the cleanup list is
> corrected to name all 4 real deletions. (2, CRITICAL) the Fujian-province selection method
> ("start from wood-tagged provinces, terrain-verify") is unworkable — round 1 terrain-checked
> every one of Fujian's 24 provinces directly and found exactly ONE is wood-tagged (Fuqing, 8420),
> and its terrain is `farmland`, not hilly; zero Fujian provinces are both wood-tagged AND hilly.
> Fixed below: the method is corrected to pick from the terrain-verified hill/low_mountain/forest
> candidate list directly (the same trade-good-independent approach already used for Huangshan),
> not filtered by the `wood` trade good at all. (3, HIGH) the `culture="hui"` corroboration for
> Huangshan is unreliable — round 1 checked all 15 `hui`-culture provinces in the mod and found
> 100% carry an Islamic religion (`sunni`/`syncretic_muslim`), including Huangshan itself
> (`religion="sunni"`) — historic Huizhou merchant lineages were Han Confucian/Buddhist, not
> Muslim, so this mod's `hui` culture functions as the Hui-Muslim/Dungan ethnonym everywhere it's
> used, not a Huizhou-dialect marker. Fixed below: the culture-tag corroboration is dropped from
> the reasoning; the province-ID gate itself is unaffected (it never queried culture), and the
> remaining identifiers (province-ID comment, terrain=hills, CHI ownership) still hold
> independently. (4, HIGH) sugar's dismissal ("regionally narrow, not built here") fails the doc's
> OWN consistency test — timber's citation is equally regionally narrow and got a province-gated
> building, not a footnote; sugar's real 糖廍 pooled-mill institution deserves the SAME treatment
> under the doc's own stated bar and its own accepted remedy for narrowness. Logged as a genuine
> gap, not fixed in THIS task (see below). (5, HIGH) the province_window.gui row-capacity risk —
> confirmed CottageIndustryItems/Row2 currently hold 5+4 slots; removing the ROW generic returns
> Row1 to 4, but adding qing_timber_lineage_building as a 9th building pushes a row back to 5,
> risking the SAME overflow bug this file already hit and fixed once before. Flagged explicitly
> below as an implementation-time GUI-layout decision, not silently left to the implementer to
> discover.
>
> **STATUS 2026-08-13: DRAFT v5 — TWO user corrections applied, restructuring the whole approach.**
>
> **Correction 1 — "generic" was wrongly implemented as "merge 9 crafts into 1 building."** v3/v4
> proposed deleting all 8 named buildings and routing every good through the single already-
> existing `row_cottage_workshop_building` (one building object, `OR`-gated on all 9 trade goods).
> The user correctly rejected this: a smithy and a weaving hut are not the same building —
> iron-forging and textile-weaving did not happen "under the same roof." "Generic" means "not
> culture-gated," never "merged into one interchangeable building." CORRECTED: keep each of the 7
> non-timber, non-silk goods as its OWN separate building (smithy, leadworks, weaving hut, silk
> reeling shed, herbalist, founder's workshop, quarry) — each simply drops its culture-exclusivity
> gate, nothing else about it changes. The single merged `row_cottage_workshop_building` is
> DELETED (it has the identical "9 crafts, 1 building" defect, just for non-Qing cultures — never
> scrutinized as its own design until now).
>
> **Correction 2 — the timber/wood near-miss deserved a REAL building, not a footnote.** Round 2
> found Meng Zhang's documented Huizhou/Fujian lineage forest-tenure system (山主/佃山人 share
> contracts, 力分/山分) but dismissed it as "doesn't fit the existing woodlot building's scope" and
> moved on. The user correctly rejected treating a genuinely-sourced Chinese-specific institution
> as a dead end: **if the research finds a real distinct Qing/Chinese arrangement, build the thing
> that arrangement actually describes**, don't fold the good into a generic building just because
> the EXISTING building's shape doesn't fit. A follow-up research pass (this session) surveyed
> EVERY trade good in the mod, not just the original 8, specifically to find (a) any other
> good with a comparable real institutional citation, and (b) confirm which goods only ever had
> universal-craft framing. Findings, condensed (full detail in "Full goods survey" below):
> - **Timber deserves a genuinely NEW, dedicated mechanic** — not a cottage building at all, since
>   the historical institution (multi-decade lineage/tenant-planter share contracts, tied to
>   SPECIFIC real provinces — Huizhou prefecture in Anhui, the Fujian highlands) is a land-tenure
>   arrangement, not a workshop that converts inputs to outputs each quarter. Designed as its own
>   mechanic below.
> - **Iron and copper DO have real Chinese-distinctive institutions** (Foshan's guild-organized
>   ironworks; Yunnan's state-quota copper-mining/minting system, 滇銅) — but BOTH operate at
>   workshop/guild or state-monopoly scale, not household/cottage scale. This doesn't rescue the
>   COTTAGE-tier smithy/founder's-workshop buildings (those stay generic, per Correction 1) — it
>   flags a possible FUTURE factory-tier building (parallel to the existing silk/porcelain/tea
>   Qing-only works) as a separate, later task, not something to build now under #58's cottage-tier
>   scope.
> - **Hemp/linen/dye have a real but lower-order citation** (Yifan Peng's upland Fujian/Zhejiang
>   ramie-and-indigo household lineage-craft complex) — genuine household practice, geographically
>   the same highland communities as the timber system, but with no distinct legal/tenure
>   innovation (unlike timber's share-contract system). Not strong enough on its own to warrant a
>   dedicated building under the SAME bar silk failed — logged as a candidate for a future,
>   separately-scoped pass if the mod ever wants a "textile fibres" cottage building's Fujian/
>   Zhejiang-highland variant, not built here.
> - **Everything else researched — lead, stone, vegetables, saltpetre, tobacco, sugar, grain, fish,
>   New World crops, oil, fur** — confirmed no Qing-distinctive cottage-scale institution (fur is
>   Manchu-distinctive but via the Eight Banners tribute-quota system, a military/tributary
>   mechanic, not a cottage building; sugar's real intermediate pooled-mill form is Taiwan/
>   Guangdong-regional, not Qing-China-wide). These stay generic, per Correction 1's per-building
>   fix.

## Task text / governing principle

User (this session): "there is nothing wrong with Qing-specific buildings so long as they are
backed by academic research as actually being specific to Qing." This supersedes any blanket
"make cottage buildings generic" instinct — the bar is per-building: keep the culture gate ONLY
where research shows the activity was genuinely distinctive to Qing/China at this scale, form, or
organization, not merely "China also did this" (which is true of nearly every craft in the list
and would justify nothing).

## Current state (confirmed in source)

`common/buildings/qing_cottage_buildings.txt` (#101, this session) defines 8 buildings, ALL
gated `owner = { OR = { country_culture_group = jurchen  country_culture_group = chinese_group
} }`:

| Building | Good | File:line |
|---|---|---|
| `qing_cottage_smithy_building` | iron | :20-46 |
| `qing_cottage_leadworks_building` | lead | :48-75 |
| `qing_cottage_weaving_hut_building` | textile_fibres | ~:78-... |
| `qing_cottage_silk_reeling_shed_building` | silk | :107-... |
| `qing_cottage_woodlot_building` | wood | :... |
| `qing_cottage_herbalist_building` | vegetables | :164-189 |
| `qing_cottage_founders_workshop_building` | copper OR tin | :191-220 |
| `qing_cottage_quarry_building` | stone | :222-... |

`row_production_buildings.txt:132-163` defines ONE generic `row_cottage_workshop_building`
covering the SAME 9 goods (iron/lead/textile_fibres/silk/wood/vegetables/copper/tin/stone) via an
`OR`-of-`trade_goods` `potential`, explicitly EXCLUDING jurchen/chinese_group — i.e. every good is
currently double-defined: once named+Qing-only, once generic+non-Qing-only. Mutually exclusive by
culture, matching the convention `qing_production_buildings.txt`/`row_production_buildings.txt`
already use for the NAMED FACTORY-TIER works (silk filature, porcelain kiln, tea workshop, opium
poppy farm, cotton workshop, salt yard) — a convention that IS defensible there because those six
are sourced, real, named Qing state/regional institutions (each carries a citation in its own
header comment, e.g. `qing_silk_filature_building`: "織造局 — the Imperial Silk Manufactory
[Jiangnan 江南三織造]"). The cottage tier's header comment, by contrast, cites NO per-building
historical distinctiveness — it only argues the MECHANIC (job-slot-free rural household labour,
Philip Huang's "involutionary growth") is worth having, which is true, but says nothing about
whether that mechanic's flavour should be culture-exclusive per good.

## Per-good research pass (draft — needs verification, not final)

The standard: was HOUSEHOLD/COTTAGE-SCALE production of this good, specifically, organized in a
way distinctively Chinese/Qing (not just "China had this too")? Contrast against the sourced
factory-tier siblings, which set the bar for what "genuinely Qing" citation looks like in this
project.

1. **Iron (smithy)** — NOT Qing-specific. Village smithing (tools, fittings, simple ironwork) at
   household scale is a near-universal pre-industrial craft; no source found that ties Chinese
   cottage ironworking to a distinctive form or scale differing from, say, an English village
   smith. **Recommend: generic.**
2. **Lead (leadworks)** — NOT Qing-specific. Same reasoning as iron; household-scale lead-working
   (shot, fittings, glazing inputs) has no documented Chinese distinctiveness at this project's
   research bar. **Recommend: generic.**
3. **Textile fibres (weaving hut)** — NOT Qing-specific AS A CRAFT, but the reasoning is corrected
   (round-1 review): household/putting-out textile production being ORGANIZED COMPARABLY in the
   Yangzi delta and in England is Pomeranz's (*The Great Divergence*) actual, central argument —
   the book's whole surprise is that pre-1800 Chinese and British cottage textile production were
   similar enough that the eventual divergence needs a DIFFERENT explanation (coal, colonies), not
   that Chinese textile production was itself distinctive. That is a stronger reason to fold than
   the v1 draft's claim (v1 said folding was justified because `qing_cotton_workshop_building`
   already covers this at a different tier and is "redundant" — checked against source and that
   claim is mechanically WRONG: the factory building requires `sufficient_job_slots = yes`, the
   cottage tier deliberately omits it, so they are NOT stat/mechanic redundant; the correct fold
   reason is craft-universality, not tier-redundancy). **Recommend: generic**, rationale corrected.
4. **Silk (silk reeling shed)** — **REVISED, no longer a survivor (round-1 review correction).**
   v1's citation — "household reeling feeding urban filatures... a Chinese rural-economy
   distinction" — does not hold up under independent check: peasant-household cocoon-raising/
   reeling feeding into urban/organized processing is close to the DEFAULT pattern everywhere
   pre-industrial silk was produced, not a Chinese peculiarity — documented for Tokugawa/early-
   Meiji Japan (household sericulture feeding regional weaving houses and later filatures),
   Ottoman Bursa and Mount Lebanon (household reeling feeding urban khans), Bengal (household
   reeling feeding karkhanas), and Piedmont/Lombardy (rural reeling feeding urban/Lyon-linked
   mills). China's version is large in SCALE (Jiangnan) and its urban end is unusually
   well-DOCUMENTED (the state-run 江南三織造, already captured by `qing_silk_filature_building`) —
   but scale and documentation-quality are exactly what the user's own principle excludes as a
   basis ("not merely China also did this... at scale"). **Recommend: generic**, UNLESS a
   materially sharper citation is found — specifically a Chinese-specific FISCAL linkage
   (household sericulture tied to tax-in-kind quotas feeding state filatures directly, bypassing
   market intermediation) or a documented Jiangnan-specific brokerage institution (e.g. raw-silk
   絲行/絲棧 houses) that is organizationally distinct from the Italian/Japanese/Ottoman
   market-based putting-out pattern — "household reeling feeds urban filature," on its own, is not
   that citation and should not be treated as settled without one.
5. **Wood (woodlot)** — NOT Qing-specific AS THE BUILDING IS SCOPED, though round-2 review found a
   genuine documented near-miss worth logging so it isn't rediscovered and misapplied later: Meng
   Zhang, *Timber and Forestry in Qing China* (2021), documents a real, sourced, distinctively
   Chinese INSTITUTIONAL form — Huizhou/Fujian lineage (宗族) corporate forest-property tenure,
   with long-term share contracts between landowning lineages and tenant planters (山主/佃山人,
   splitting yield via 力分/山分 shares), feeding raft-merchant timber markets down the Yangzi. This
   is exactly the kind of organizational citation the user's bar asks for — but it describes
   ESTATE-TENURE-scale timber cultivation with lineage contracts, not the simple village
   woodlot/timber-gathering the mod's `qing_cottage_woodlot_building` actually models (no tenure
   or lineage framing anywhere in the building's text or citation). Does NOT justify keeping this
   building as currently authored — logged here ONLY as a flag in case a differently-scoped
   lineage-forestry building is ever proposed separately. **Recommend: generic**, for the building
   as it exists today.
6. **Vegetables/herbs (herbalist)** — NOT Qing-specific. Household herb gathering/processing is
   universal. The materia medica (中藥) exception hypothesized in v1 doesn't even apply here
   (confirmed by round-1 review): the trade good this building actually gates on is the generic
   `vegetables` (`common/trade_goods/00_imp19c.txt`), not a distinct medicinal-herb good — there is
   no mechanical hook for a materia medica argument regardless of the historical merits. **Settled:
   generic.**
7. **Copper/tin (founder's workshop)** — NOT Qing-specific at COTTAGE scale. Household
   bronze-casting from copper+tin has no documented Chinese distinctiveness. One non-rescuing
   note from round-1 review: Qing-period Yunnan copper mining/smelting for coinage (滇銅) WAS a
   genuinely distinctive, state-regulated Chinese institution — but it operated at
   mine/smelter scale, not household-casting scale, so it does not save this building as
   currently conceived; it would justify a different, non-cottage building if ever pursued.
   **Recommend: generic.**
8. **Stone (quarry)** — NOT Qing-specific. Village quarrying is about as culturally neutral an
   activity as exists. **Recommend: generic.**

**Working conclusion after round-1/round-2 review: 0 of 8 EXISTING cottage buildings clear the
Qing-specificity bar** (v1's silk survivor did not hold up under independent check, see #4). This
remains correct and is NOT being revisited — the historical judgment on all 8 original goods is
settled. What v3/v4 got wrong was the STRUCTURAL response to that finding (merging into 1
building), corrected above, and the SCOPE of the research (only the original 8 goods were
checked; the full survey below extends this to every good in the mod and finds one, timber, that
deserves a wholly new mechanic rather than a fold).

## Full goods survey (v5, following user correction — every trade good, not just the original 8)

A dedicated research pass covered every trade good defined in the mod (`common/trade_goods/
00_imp19c.txt`), not just the 8 the original #101 task happened to build cottage buildings for,
specifically to check whether any OTHER good has a real institutional citation the original scope
would have missed entirely.

**Not cottage-industry candidates at all** (dismissed quickly, not building-shaped): camel,
elephants, horses (pastoral/military husbandry), gems, amber (extractive minerals, not a
household craft), rifles (finished military-industrial good), industrial_fibres (abstracted
modern category), generic_fruit/temperate_fruit (abstracted catch-all categories), coffee/rubber
(not period-real 1763 Qing crops — both are 20th-century Chinese cultivation), palm/spices
(entrepôt/import goods for China at this date, not domestic Chinese cottage production).

**Confirmed generic — universal craft, no Chinese-distinctive institution found** (same
conclusion as the original 8, extended): lead, stone, vegetables/herbs, saltpetre (Foshan
saltpetre production is workshop-scale, tied to the gunpowder/foundry economy, not household),
tobacco (genuine household/family-farm curing, but a universal early-modern peasant cash-crop
pattern with no distinguishing institution), grain, fish, oil (one interesting tangent: Chinese
oil-pressing has a documented link to Buddhist monastery-run presses — a real institutional
wrinkle, but monastic, not household/lineage, so it doesn't support a COTTAGE building), and all
5 New World crops (maize/sweet_potato/potato/peanut/chili — universal smallholder crops, no
distinguishing Chinese processing institution; already covered by the generic, non-culture-gated
`new_world_farmstead_building`, unrelated to this task).

**Iron and copper — real Chinese-distinctive institutions exist, but at the WRONG scale for a
cottage building.** Foshan (Guangdong) ironworking is documented (multiple independent sources)
as organized at guild/workshop scale — "10 iron-smelting workshops and more than one hundred iron
[foundries]," named craft guilds, merchant-organized production — genuinely Chinese-distinctive,
but a factory/manufactory tier, not household/cottage. Yunnan copper (滇銅) mining-and-minting was
a state-quota, monopoly-adjacent system — also genuinely distinctive, also NOT cottage-scale. Both
support a FUTURE Qing-only factory-tier building (parallel to the existing sourced silk
filature/porcelain kiln/tea workshop/salt yard buildings), which is explicitly OUT OF SCOPE for
this task (cottage-tier only) — logged as a follow-up idea, not built here. The EXISTING cottage
tier smithy/founder's-workshop buildings stay generic (household bronze-casting/smithing at
cottage scale has no Chinese-distinctive citation at THAT scale).

**Hemp/linen/textile-fibres-adjacent (ramie) and dye — a real but lower-order citation, not built
here.** Yifan Peng's *A Herbaceous Revolution* documents household ramie-growing-and-processing
plus indigo-dye-making as an integrated upland Fujian/Zhejiang lineage-household craft complex
(the same highland geography as the timber system below). Genuine household practice, but with no
distinct legal/tenure innovation — it doesn't clear the SAME bar silk failed (a documented craft
practiced by a specific community is not, on its own, an institutional distinction; that's exactly
the standard silk's citation failed under). Logged as a candidate for a future, separately-scoped
building if the mod ever wants a Fujian/Zhejiang-highland-specific textile variant — not built
under this task.

**Fur — Manchu-distinctive, but via a tributary/military mechanic, not a cottage building.**
Manchurian sable production ran through the Eight Banners system and imperial tribute quotas
(banner-assigned mountains, the Solon Sable Tribute), not household craft. Genuinely Chinese/
Manchu-distinctive, but the correct mechanic for it (if ever built) is a tribute-quota/banner
system, not a production building — out of this task's scope entirely.

**Sugar — a real intermediate form. [round-1 fix, HIGH, RESOLVED: build it, matching timber's
treatment.]** Cane-growing was smallholder, but processing ran through jointly-capitalized "sugar
houses" (糖廍) — a genuine pooled-household institution, distinct from both pure cottage and full
factory scale, documented specifically for Taiwan and Guangdong. Round 1 found the ORIGINAL
dismissal ("regionally narrow... not built here") fails this doc's OWN consistency test: timber's
citation is EQUALLY regionally narrow, and this doc's answer to timber's narrowness was to build a
province-ID-gated building, not discard it. **Decision: build a matching `qing_cottage_sugarhouse_
building`**, same shape as `qing_timber_lineage_building` (flavor citing 糖廍, a couple of modest
stat bonuses over the generic sugar-cane cottage baseline, gated on specific province IDs, Qing-
only). Candidate provinces confirmed by direct grep of `setup/provinces/00_*.txt` for
`trade_goods="sugar"`: **Guangdong** — Haikou (2218, farmland), Shantou (2993, farmland), Chaonan
(7842, farmland); **Fujian** — Jian'ou (2693, hills), Nanping (4244, farmland), Minqing (7470,
hills). [Note: Taiwan, cited in the historical literature as the OTHER core sugar-house region,
has NO `sugar`-tagged province in this mod's current 1763 setup — every Taiwan province is tagged
wood/temperate_fruit/grain/iron/fish instead; the mod's own sugar geography is currently
Guangdong/Fujian-only, not Taiwan/Guangdong as the historical citation names. This is a real,
useful finding for the province-list decision, not treated as blocking — the mod's own data
simply doesn't have a Taiwan sugar province to gate on.] [OPEN, round 2 or implementation:
finalize which of these 6 provinces qualify (a terrain-only filter isn't obviously right here the
way it was for timber, since 糖廍 histories don't specifically require hill terrain the way
Huizhou/Fujian timber tenure did) — this needs the same historical-geography judgment call timber's
Fujian list still needs, not a mechanical terrain filter.]

**Timber/wood — the other good that clears the bar for a wholly NEW, dedicated mechanic.** See the
next section.

## NEW MECHANIC — Huizhou/Fujian lineage timber tenure (力分/山分 share contracts)

### The historical institution

Meng Zhang, *Timber and Forestry in Qing China: Sustaining the Market* (U. Washington Press,
2021) documents a real, specific, Chinese-distinctive institutional form: in the mountainous
Huizhou prefecture (徽州, historically in southern Anhui) and the Fujian interior highlands,
landowning lineages (宗族) with unused hill land granted tenant planters long-term rights to
plant and tend timber (China-fir/杉木, pine) in exchange for a divisible, tradable SHARE of the
eventual harvest — the **力分/山分 (labor-share/mountain-share)** system, one sourced split giving
the tenant planter ~40% of the eventual timber crop. These shares were themselves registered,
tradable financial instruments (per Zhang's related work on securitized timberland shareholding),
and the rotation from planting to harvest ran roughly 20-30 years — explicitly NOT an
instant-yield craft, a multi-decade land-tenure arrangement feeding raft-merchant timber markets
down the Yangzi to Hankou/Shanghai.

This is NOT building-shaped in the same sense as a cottage workshop (an input→output converter
that runs every quarter). It is a long-horizon contract over a plot of land, with the payoff
arriving decades after the initial grant.

### Where it applies (confirmed against actual province data, not assumed)

- **Huangshan** (黄山, province ID 4441, `setup/provinces/00_Anhui.txt`) is the real, mappable
  1763 province matching historic Huizhou prefecture: `terrain="hills"`, CHI-owned at 1763 start
  (confirmed present in CHI's `own_control_core` list, `setup/main/00_default.txt:35725`).
  Currently tagged `trade_goods="tea"`, not wood — this mechanic does NOT require changing its
  trade good; the tenure system is about the province's HILL LAND, not what good it happens to be
  assigned for the vanilla trade system. **[round-1 fix, HIGH]** the doc previously ALSO cited
  `culture="hui"` as corroborating evidence ("徽州's own historical people are literally named
  `hui` in this mod's culture list") — round 1 checked this directly and found it unreliable: ALL
  15 `hui`-culture provinces in the mod, including Huangshan itself, carry an Islamic religion
  (`religion="sunni"` at 4441 specifically). Historic Huizhou merchant lineages were Han
  Confucian/Buddhist/folk-religion, not Muslim — this mod's `hui` culture functions as the
  Hui-Muslim/Dungan ethnonym everywhere it's seeded, not a Huizhou-dialect marker. **Dropped from
  the reasoning** — the building's `allow` gate never queries culture anyway (see below), so this
  doesn't change the mechanism, only removes a piece of corroborating text that didn't hold up.
  The identification still rests on solid ground: the province-ID comment (`#Huangshan`),
  `terrain="hills"`, and CHI ownership.
- **Fujian highlands — [round-1 fix, CRITICAL, method corrected; round-2 fix, HIGH, count/list
  corrected].** The prior text suggested starting from wood-tagged Fujian provinces and
  terrain-checking those. Round 1 terrain-checked Fujian's provinces directly and found this method
  is unworkable: exactly ONE province is tagged `trade_goods="wood"` (Fuqing, ID 8420), and its
  terrain is `farmland` — not hilly. **Round 2 found round 1's own "checked directly" sweep was
  itself incomplete** — Fujian has **25** provinces total (round 1 said 24), and the terrain-
  qualifying hill/low_mountain/forest list has **14** members, not 13 (round 1's list omitted
  Hua'an, ID 4247, `terrain="forest"`, currently `trade_goods="grain"` — meets the exact same
  criterion as Jianyang/Liancheng, both correctly included, with no principled reason to exclude
  it). Corrected full list: Jianyang 831/forest, Yanxi 1785/hills, Jian'ou 2693/hills,
  Anxi 3302/low_mountain, Wuyishan 3317/hills, Hua'an 4247/forest, Zhouning 5218/hills,
  Pocheng 5822/hills, Minqing 7470/hills (source comment spells it "Minging" — a typo in the mod's
  own data, not this doc's error), Sanming 7474/hills, Liancheng 7862/forest, Shuibei 8172/hills,
  Zhenghe 8498/low_mountain, Pinghe 9711/hills — 14 total, ALL tagged tea/sugar/porcelain/
  sweet_potato/temperate_fruit/grain/wood(Fuqing only, excluded), none wood among the 14. **Method
  unchanged, still correct**: pick candidates from this terrain-verified list DIRECTLY, the same
  trade-good-independent approach already used for Huangshan — do NOT filter by the `wood` trade
  good at all. [OPEN, implementation-time, genuinely unresolvable from this repo per round 2's own
  research-doc sweep] which of these 14 terrain-qualifying provinces actually represent Zhang's
  documented interior timber-highland region needs a historical-geography check no in-repo research
  doc currently answers — left open, not guessed at.

### Resolved mechanic shape — a Qing-specific building, flavor + a couple of bonuses, nothing more

**Final, simplified design (2 rounds of overbuilding corrected — no province decision, no
maturation timer, no new mechanic).** Timber gets the SAME treatment as every other sourced
Qing specialty building in this mod: unique flavor text citing the real history, and a couple of
stat bonuses over the generic equivalent. Nothing else.

**`qing_timber_lineage_building`** — lives alongside the other 7 generic-ized cottage buildings in
`common/buildings/qing_cottage_buildings.txt`. Baseline it's compared against, the existing
`qing_cottage_woodlot_building` (`:136-162`):
```
local_lower_strata_output = 0.2
local_proletariat_output = 0.15
base_resources = 1
cost = 50
time = 150
allow = { NOT = { has_city_status = yes }  trade_goods = wood }
```

- **Flavor**: header comment citing 力分/山分 (labor-share/mountain-share) lineage-tenure timber
  contracts (Meng Zhang, *Timber and Forestry in Qing China*), matching the citation style every
  other Qing specialty building in this file already uses.
- **Gate**: restricted to the SPECIFIC historic provinces, not a generic terrain/culture-group
  condition — `province = { id = 4441 }` (Huangshan/Huizhou, confirmed) OR-listed with qualifying
  Fujian highland province IDs (terrain-verification pass still needed to finalize that list — do
  not assume every Fujian wood-tagged province qualifies). Does NOT require `trade_goods = wood`
  (Huangshan is currently tagged `tea`) — the institution is about the LAND, not the current good.
  Stays Qing-only (`owner = { OR = { country_culture_group = jurchen  country_culture_group =
  chinese_group } } }`) — unlike the other 7 buildings in this task, which are going generic, this
  one IS the genuinely Qing-specific case the whole doc has been looking for.
- **Bonuses**: modestly better than the generic woodlot — `base_resources = 1.5` (vs `1`) plus a
  small `local_monthly_civilization` kicker for the documented merchant/lineage trade network.
  [ASSUMPTION] exact magnitude is a placeholder, boot-tune — no source gives a clean numeric
  "% better than an ordinary woodlot," only the historical tenant/landowner split, which is a
  distribution detail between two historical parties, not itself a game-balance number.

That's the whole mechanic. No timer, no new variable, no new pulse.
4. **Sharing represented via yield split, not a new office**: rather than inventing a full
   character/office mechanic (previously option 3 — REJECTED as unnecessary complexity for what
   the history actually needs), represent the tenant-planter/landowning-lineage split as a FLAT,
   FIXED proportion baked into the yield modifier's magnitude (Zhang's sourced ~40%-to-tenant
   split informs the modifier's SIZE relative to a hypothetical undivided yield — a design
   constant, not a live character relationship). This avoids inventing a new office/character
   mechanic for an institution the sourcing doesn't actually describe as personality-driven (unlike
   the Salt Commissioner/Hoppo, who ARE real historical individual office-holders with corruption
   stats) — the timber lineage system is a property-law arrangement between anonymous landowning
   families and tenant planters, not a single appointed official.

**Still needs before implementation**: (a) **[round-1 fix, round-2 count-corrected]** the Fujian
highland province selection — the METHOD is settled (terrain-verified hill/low_mountain/forest
list, not wood-tagged filtering) and the list is now the CORRECT 14 candidates (round 2 found
round 1's own list had missed Hua'an, 4247 — see the corrected section above), but the FINAL
qualifying-province SUBSET (which of the 14 genuinely represent Zhang's documented timber region)
is still open — round 2 confirmed no in-repo research doc resolves this; do this as the first
implementation step, not a separate task; (b) an adversarial design review of this resolved shape
(magnitude of the yield modifier, exact treasury/PI cost of the grant decision, whether 25 years
is the right single point-estimate or whether the mod should offer a range) before coding, per
this project's design-first convention for new mechanics; (c) **[round-1 fix, round-2 RESOLVED]**
`qing_timber_lineage_building` AND `qing_cottage_sugarhouse_building` are two new cottage
buildings (10 total surviving, up from the original 8) — round 1 flagged the row-overflow risk;
**round 2 resolved it with a concrete, evidence-backed recommendation, adopted here**: do NOT add
a third row (no 3-row precedent exists anywhere in this codebase, confirmed by repo-wide grep for
"Row3" across every `.gui` file — would be a novel, unprecedented pattern). Instead, append BOTH
new buildings to the EXISTING `CottageIndustryItemsRow2` blockoverride, in both
`gui/province_window.gui` and `gui/macro_builder_view.gui` — Row1 stays at 4 items (264px), Row2
grows from 4 to 6 items (396px), both comfortably inside this file's own proven-safe threshold
(≤7 items/≤462px is safe per `CommerceItems`' current 7-item row; 8 items/528px is the confirmed-
unsafe point that forced the original Industrial/Foreign 2-row splits). Zero changes needed to
`gui/shared/gui_templates.gui`'s template structure — only the two `blockoverride` bodies gain two
lines each.

## Proposed restructure — CORRECTED (v4, user correction 2026-08-13)

> **This section previously proposed deleting all 8 named `qing_cottage_*_building` entries and
> routing every good through the ALREADY-EXISTING, single merged `row_cottage_workshop_building`
> (one building object, gated on an `OR` of all 9 trade goods). The user correctly rejected this:
> a smithy and a weaving hut are not the same building — iron-forging and textile-weaving did not
> happen "under the same roof." Collapsing 9 distinct crafts into 1 interchangeable building
> object is a mechanical error, independent of and orthogonal to the historical
> culture-specificity question this design doc otherwise resolves correctly. "Generic" means
> "not culture-gated," NOT "merged into one building." Corrected below: keep 8 SEPARATE
> buildings, one per craft, each simply dropping its culture-exclusivity gate. The existing
> merged `row_cottage_workshop_building` (which has the SAME underlying flaw — it already
> pretends iron/lead/textile/silk/wood/vegetables/copper/tin/stone are one interchangeable
> non-Qing building, unnoticed until now because it was never scrutinized as its own design) is
> DELETED, not widened.**

1. **For EACH of the 8 goods, take the EXISTING `qing_cottage_*_building` and simply drop its
   culture gate** (`owner = { OR = { country_culture_group = jurchen  country_culture_group =
   chinese_group } } }` → removed entirely, or replaced with no `owner` culture condition at all —
   every OTHER condition, e.g. `NOT = { has_city_status = yes }`, `trade_goods = <good>`, stays
   exactly as-is). Rename away from the `qing_` prefix if project convention wants that reflected
   (e.g. `cottage_smithy_building`), or keep the name and just drop the gate — a naming decision,
   not a structural one. Result: **8 separate buildings survive**, each still doing exactly one
   craft on exactly the good(s) it always gated on, now available to every culture including
   Qing, not merged into anything.
2. **Delete the single merged `row_cottage_workshop_building`** (`row_production_buildings.txt:
   132-164`) entirely — it is superseded by the 8 now-generic buildings above, and its own
   9-good-`OR` shape has the identical "iron and textile in one building" defect this correction
   exists to fix. Nothing needs widening; the thing being widened was the wrong shape to begin
   with.
3. **Silk specifically**: since round 2 confirmed (independently, twice) that silk does not clear
   the Qing-specificity bar either, `qing_cottage_silk_reeling_shed_building` gets the SAME
   treatment as the other 7 — culture gate dropped, building kept, not deleted. It remains a
   DIFFERENT building from the factory-tier `qing_silk_filature_building` (which stays Qing-only,
   sourced, unaffected by this task) — the two already differ structurally (urban skilled
   filature vs rural household reeling, different strata mix, different `NOT has_city_status`
   framing) and that distinction is orthogonal to the culture-gate question this task resolves.
4. **Macro-builder access — NO ACTION NEEDED under the corrected plan.** All 8 buildings keep
   their EXISTING `qing_cottage_*` names, allowlist entries, `gui_templates.gui` types,
   `custom_tooltip.gui` templates, `province_window.gui`/`macro_builder_view.gui` entries, and
   loc file — NONE of that GUI/macro wiring is touched by this task, since the buildings
   themselves are not being deleted or renamed, only having one `owner` culture condition
   removed. (This entire concern — and the prior versions' extensive discussion of a
   macro-builder regression — was an artifact of the REJECTED delete-8/widen-1 plan; it does not
   apply to the corrected 8-buildings-stay plan and is retained here only so a future reader
   understands why it isn't relevant anymore.)
5. **Cleanup — CORRECTED, round 1 (the "comment/definition-only" claim below was TRUE when
   written, against round-2's source, but is FALSE now — `#101`'s implementation, commit
   `b7b223729`, this session, gave `row_cottage_workshop_building` full GUI/loc wiring AFTER round
   2's grep ran).** The deletion is the single merged `row_cottage_workshop_building`
   (`row_production_buildings.txt:132-164`) PLUS its now-real references, re-verified against
   CURRENT source (round 1 grepped directly, not the doc's stale claim):
   - `gui/shared/gui_templates.gui:607-614` — the `type build_item_row_cottage_workshop_building`
     block. DELETE.
   - `gui/shared/custom_tooltip.gui:902-911` — the `template building_row_cottage_workshop_
     building_tooltip` block. DELETE.
   - `gui/province_window.gui:4473-4489` — the explanatory comment (references the ROW generic by
     name) AND the `build_item_row_cottage_workshop_building = { }` line inside `blockoverride
     "CottageIndustryItems"`. DELETE the line; UPDATE the comment (it currently says "eight Qing
     cottage buildings + one ROW generic," stale on both counts — see the corrected building-count
     note below).
   - `localization/english/row_buildings_l_english.yml:18-19,24` — the name/desc/tooltip loc keys
     for this building. DELETE.
   - `gfx/interface/macro_builder/config/00_default.txt:107-110`'s explanatory comment (currently
     explains why the ROW generic is excluded from the allowlist, citing `province_window.gui`
     line numbers, AND ALSO says "eight Qing cottage buildings" — round 3 found this file was the
     SAME staleness class as the 4 comments below, not a separate concern) — UPDATE or DELETE,
     since it will otherwise reference a building/line-range/count that no longer means anything.
     Confirmed (round 1 AND round 2 agree): no ACTUAL allowlist entry exists for this building —
     only the comment needs touching, not an allowlist removal.
   - **[round-2 fix, extended round 3 — round 2's own sweep for this defect class was ITSELF
     incomplete, the same pattern round 2 caught round 1 in]** FOUR more stale `[#101 2026-08-13]
     ... eight Qing cottage buildings ...` header comments exist beyond the one in
     `province_window.gui` round 1 already flagged — round 2 found 3 of them, round 3 found a 4th
     round 2 missed: `gui/shared/gui_templates.gui:615`, `gui/shared/custom_tooltip.gui:912`,
     `gui/macro_builder_view.gui:294-301`, AND **`gui/shared/gui_templates.gui:1495`** (a SEPARATE
     template block, `macro_build_item_qing_cottage_*`, distinct from the one at `:615` — fixing
     one does not fix the other). UPDATE all four (plus the macro-config comment above) to state:
     **8 of the 8 original buildings survive (culture gate dropped on all 8, including silk — none
     are deleted), PLUS 2 genuinely NEW buildings (`qing_timber_lineage_building`,
     `qing_cottage_sugarhouse_building`) = 10 total.** Only 2 of the 10 remain Qing-exclusive
     (the 2 new ones); the other 8 are now fully generic.
   This is a REAL, multi-file cleanup — not the "comment/definition-only" no-op the doc previously
   claimed. This correction should be applied at implementation time exactly as listed above, not
   re-derived from the now-superseded round-2-of-v4 grep this section originally cited.
6. **Gate-type change, flagged (round-1 review, MEDIUM, currently moot but must be stated).** The
   8 Qing buildings gate on `allow` (bypassed by `add_building_level`/scripted seeding, per the
   convention documented in `qing_silk_filature_building`'s own comment); the generic building
   gates on `potential` (NOT bypassed — blocks even scripted adds). Folding changes bypass
   semantics for any FUTURE cottage-industry seeding effect. Currently moot — zero
   `add_building_level`/scripted-effect references to any `qing_cottage_*` building exist today
   (grep-confirmed) — but state this explicitly in the implementation log rather than silently
   changing gate type.

## Open questions for round 2

1. **[RESOLVED, round 1]** Verified the 7 "no source found" verdicts by independent literature
   sweep — no new candidate citation found across a fresh check of every trade good. Rests on
   trusting secondary-literature citations that can't be independently fact-checked from this
   repo alone (a standing epistemic caveat, not a defect).
2. **[PARTIALLY RESOLVED, round 1]** Hemp/ramie/dye's dismissal holds. **Sugar's dismissal does
   NOT hold** — round 1 found it fails this doc's own consistency test (timber's citation is
   equally regionally narrow and got a building, not a footnote). Fixed above with an explicit
   either/or: build a matching sugar building, or state a non-narrowness reason to decline. NOT
   yet decided which — round 2 should make this call, not leave it open a third time.
3. **[RESOLVED, round 1]** Timber mechanic shape verified minimal and coherent — no timer, no
   office/character mechanic, no new pulse; the yield-modifier framing doesn't imply a live
   character relationship.
4. **[RESOLVED, round 1 — method fixed; count corrected round 2; list still open]** The Fujian
   province-selection METHOD was broken (wood-tagged filtering excludes every real candidate) —
   fixed above to use the terrain-verified hill/low_mountain/forest list directly. Round 2
   corrected the candidate count from 13 to 14 (round 1's own sweep had missed Hua'an, 4247). The
   FINAL qualifying-province SUBSET (which of the 14 terrain-candidates are genuinely Zhang's
   timber-highland region) remains open for implementation-time historical-geography research —
   round 2 confirmed no in-repo research doc resolves this.
5. **[RESOLVED, round 1]** The `culture="hui"` corroboration for Huangshan is unreliable (all 15
   `hui`-culture provinces in the mod are Islamic-religion, contradicting the Han-Huizhou reading)
   — dropped from the reasoning above; the identification still holds on province-ID/terrain/
   ownership grounds alone, which never depended on the culture tag.
6. **[RESOLVED, round 1]** Stacking exploit — confirmed IDENTICAL for `qing_timber_lineage_
   building` and the 7 generic-ized buildings: no per-building instance cap exists anywhere in
   `common/buildings/`, and `global_settlement_building_slot = 9999` applies uniformly. Not a new
   or different risk.
7. **[RESOLVED, round 1 — and found WORSE than assumed]** GUI/loc cleanup was NOT
   comment/definition-only as the doc claimed — `#101`'s implementation gave
   `row_cottage_workshop_building` real wiring across 4 files AFTER the doc's own citation was
   written. Fixed above with the corrected, complete deletion list. **New finding, not previously
   flagged**: `qing_timber_lineage_building` as a 9th cottage building risks a `province_window.
   gui` row-overflow (Row1/Row2 currently hold 5+4 slots; see the "still needs before
   implementation" section) — round 2 should confirm the GUI-layout fix (third row vs.
   redistribution) is specified before this is implementation-ready.
8. **[RESOLVED, round 1]** Removing the `owner = { OR = { country_culture_group = jurchen
   country_culture_group = chinese_group } } }` block from each of the 7 buildings' `allow` leaves
   a syntactically valid block — round 1 read all 8 current `allow` shapes directly (6 with a
   simple `owner`+`NOT`+`trade_goods` shape, founders_workshop with an extra nested `OR` for
   copper/tin) and confirmed no syntax risk in any of them.
9. **[RESOLVED, round 1, arithmetic corrected round 2]** Open question #2's sugar decision — build
   a matching `qing_cottage_sugarhouse_building`, per the corrected Full Goods Survey section
   above. **Building count, corrected**: 8 original `qing_cottage_*` buildings SURVIVE (all 8 drop
   or keep their gate per the per-good verdicts above; woodlot itself is one of these 8, not
   separate from them), PLUS the 2 genuinely NEW buildings (`qing_timber_lineage_building`,
   `qing_cottage_sugarhouse_building`) = **10 total surviving buildings**. The single merged
   `row_cottage_workshop_building` is DELETED, not counted as a survivor either way. **[RESOLVED,
   round 2]** the row-capacity risk this creates (10 buildings needing to fit across 2 rows that
   currently define 5+4 slots) is resolved above: redistribute into the existing Row2 (4→6 items),
   no third row needed.
10. **New, round 2**: finalize the sugarhouse building's qualifying province list from the 6
    sugar-tagged Guangdong/Fujian candidates found above (Haikou/Shantou/Chaonan/Jian'ou/Nanping/
    Minqing, source-spelled "Minging") — unlike timber, a terrain filter isn't obviously the right
    cut here; needs a historical-geography judgment call specifically about which provinces
    represent genuine 糖廍 pooled-mill organization vs. ordinary smallholder cane-growing. Also
    finalize open question
    #4's timber Fujian-province list — both are now open historical-geography decisions of the
    same kind, not blocking each other.
