# DESIGN (draft, pre-review) — should more provinces be tagged trade_goods=vegetables?

## Question

Separate from the production-multiplier fix already shipped (`DESIGN_93_FOLLOWUP_
VEGETABLES_STILL_COLLAPSING.md`), the user asked whether the underlying 419-province
`trade_goods=vegetables` assignment itself is historically accurate or an undercount, given
that these assignments were seeded/corrected by prior sessions of this same project (commit
`0e3f269fe`, "#228 (b): correct existing trade-good assignments to 1763 reality") and are not
guaranteed correct just because they were deliberate.

## Research (two independent passes, English-language and Chinese-language sources)

**English-language sources** (G. William Skinner, "Vegetable Supply and Marketing in Chinese
Cities," *The China Quarterly*, 1978; Du/Song/Cai/Zhu on night-soil fertilizer economics,
*Soil Ecology Letters*, 2024; Van der Lans et al. 2011, Wageningen; Marmé on Suzhou; Hu & Xia
on Guangzhou/Zhuhai): market gardening near Chinese cities was real, named, and structurally
documented — Skinner's "peri-urban zoning" describes concentric land-use rings around cities,
with intensive vegetable cultivation in the innermost ring, driven by spoilage (produce had to
reach market fast) and fertilizer logistics (vegetable plots needed nightsoil from the city,
so proximity was economically necessary in both directions). **But this ring was
geographically narrow — immediately around city walls, not broad or province-spanning.**
Broader Qing agricultural-economics literature (Perkins, Pomeranz, Huang, Marks) frames
regional specialization around staple grain vs. cash crops (cotton, silk, sugar, tea); none
single out vegetables as a distinct REGIONAL commodity zone the way those are.

**Chinese-language sources** (Baidu-indexed gazetteer/popular-history material, moderate
confidence — full academic monographs not reachable): concrete Qing vegetable-specialization
evidence found is dominated by small, administratively-bounded IMPERIAL supply gardens near
Beijing (畿辅菜园/官菜园, ~34-59 garden plots totaling tens of km², each staffed by ~5
gardeners — a palace rent-farm system, not a peasant-economy zone) plus one genuine
peasant-market anecdote (early-Qing Weifang, Shandong, county-level only). Gazetteers do
record vegetables under 物產 (local products), confirming it as a real recognized category —
but as ONE ITEM AMONG MANY per locality, never recorded as a county's DEFINING product ahead
of grain. Assessment: "leaning toward current assignment being defensible, not an undercount,"
with explicitly flagged low-to-moderate confidence (search was CAPTCHA-limited; Li Bozhong's
actual monographs and Pearl River Delta 菜基/桑基魚塘 literature were not reached).

**Both independent research passes converge on the same shape of answer** despite different
source bases: vegetable market-gardening was real but narrow — a thin ring right at city
walls, recorded as a minor item among many local products, not a broad regional specialty on
the scale of a cotton or silk belt.

## Direct check against the mod's own data

Given the "narrow ring around specific named cities" claim from both research passes, checked
the mod's actual province data for the 5 cities named by the English-source research
(Beijing 8363, Nanjing 6659, Suzhou 2588, Hangzhou 8120, Guangzhou 9298) and their real
historical immediate-neighbor counties:

| Location | Current `trade_goods` |
|---|---|
| Suzhou, Nanjing, Hangzhou (the cities themselves) | `silk` |
| Wuxi, Changshu (Suzhou's immediate hinterland) | `textile_fibres` |
| Taicang, Wujiang (Suzhou's immediate hinterland) | `grain` |
| Dongguan (Guangzhou's immediate hinterland) | `peanut` |
| Shunyi (Beijing's immediate hinterland) | `temperate_fruit` |

None of these are empty. Every one carries a DIFFERENT, independently well-documented
historical specialty (Jiangnan silk, the Songjiang cotton belt, Lingnan peanut cultivation,
north-China orchard fruit).

**[Review-corrected reasoning]** The engine allows exactly one `trade_goods` per province —
confirmed by direct inspection. An occupied slot only proves the slot isn't empty; it does
NOT by itself prove vegetables has no historical claim there (a real dual-specialty county
could exist where the mod had to pick one "winner," and "already assigned to X" doesn't
establish X was the *right* winner). The actual case against reassignment rests on the
research finding itself, not on slot occupancy: both research passes independently establish
vegetable market-gardening was NARROW (a city-wall ring) and recorded as a MINOR item among
many local products, never a county's defining product — so vegetables would rarely be the
historically correct winner over silk/cotton/grain at these specific, real locations in the
first place. That is the basis for "no change," not the fact that a slot happens to be filled.

## Sample-size check (review-driven extension, 4 additional cities)

The 5-city check above was a real risk of circularity — it checked exactly the cities the
English-source research happened to name. Extended independently to 4 cities the research did
NOT name (Chengdu, Wuhan/Wuchang, Xi'an, Fuzhou), checking each city and 1-2 real historical
immediate neighbors:

| Location | Current `trade_goods` |
|---|---|
| Chengdu (city) | `tea` |
| Deyang (Chengdu hinterland) | `grain` |
| Chongqing (Chengdu hinterland) | `salt` |
| Wuchang (city) | `grain` |
| Xianning (Wuchang hinterland) | `tea` |
| Xiaogan (Wuchang hinterland) | `grain` |
| Fuzhou (city) | `tea` |
| Fuqing (Fuzhou hinterland) | `wood` |
| Putian (Fuzhou hinterland) | `sweet_potato` |
| Xi'an (city) | `silk` |
| Xianyang (Xi'an hinterland) | `temperate_fruit` |
| Weinan (Xi'an hinterland) | `textile_fibres` |
| Baoji (Xi'an hinterland) | **`vegetables`** |

Same pattern holds outside the source's named cities: every location already carries a
documented specialty, none is empty or obviously wrong. Notably, Baoji (in Xi'an's own
hinterland) already IS tagged vegetables — the mod already places the tag where a genuine
city-ring pattern fits. This directly de-risks the circularity concern: the "no gap found"
result replicates on an independently-chosen sample, not just the research's own examples.

## Pearl River Delta 菜基 check (review-driven)

The Chinese-source research flagged it never reached Pearl River Delta 基塘 (dyke-pond)
literature, specifically 菜基 (vegetable-dyke), as a gap. Checked directly: the canonical
基塘 classification for this region lists 桑基 (mulberry, for silk — the dominant type),
蔗基 (sugarcane), and 果基 (fruit) as the standard categories; 菜基 is not a standard
category in general reference material, and where it does appear it is a minor, market-town-
adjacent variant — consistent with the "narrow city-ring" finding, not evidence of a broad
overlooked vegetable belt. Guangzhou's checked hinterland (Dongguan = peanut) sits in a delta
economy the era's own record shows dominated by mulberry/silk and sugarcane. The previously
unreached literature does not hide a gap.

## Recommendation: NO CHANGE to province trade_goods assignments

The evidence does not support expanding `trade_goods=vegetables` beyond the current 419
provinces:
1. Vegetable market-gardening's real historical footprint (immediate city-wall rings) is
   smaller in scale than the specialties already assigned to the specific locations checked.
2. Every real historical neighbor location checked against the mod's actual data already
   carries a different, independently well-sourced trade good, not an empty or clearly wrong
   one.
3. Both independent research passes, working from different source bases, converge on
   "narrow phenomenon, not a broad undercount."

This does NOT touch or revert the production-multiplier fix already shipped (`GOODS_
vegetables_production_multiplier = 4`) — that fix targets the mismatch between vegetables'
existing (correct) production base and pop-level demand's equal-per-good assumption, which is
a real, orthogonal problem regardless of whether the province count itself is right.

## Review outcome (adversarial review, 2026-08-17) — NO CHANGE survives (China scope)

Reviewed independently. Verdict: the no-change recommendation survives, for CHINA. One real
reasoning flaw was found and corrected above (the "slot already occupied" argument was
logically invalid on its own — fixed to rest on the actual research finding instead, which
does hold). The sample-circularity concern (only checking the research's own named cities)
was confirmed real, then directly de-risked by independently checking 4 more cities
(Chengdu, Wuhan/Wuchang, Xi'an, Fuzhou) — same pattern held, and notably Baoji (Xi'an's own
hinterland) already carries the vegetables tag, showing the mod already applies the pattern
correctly elsewhere. The Pearl River Delta 菜基 gap was checked directly and does not hide a
missed regional belt — 菜基 isn't even a standard 基塘 category; mulberry/silk dominates that
delta's real economy. Calibration confirmed appropriate: given thin-to-moderate evidence, the
burden of proof correctly sits on the side proposing to add provinces (the harder-to-verify-
safe direction), and both the research and the direct spot-checks push toward "no change," not
away from it. **This entire audit and its review are CHINA-scoped only** — a separate,
world-wide research pass (covering other historically-documented market-garden regions:
Low Countries, Paris, London, Ottoman cities, Japan, etc.) is running separately per direct
user correction that the original scoping was too narrow; that pass's findings will determine
whether any ROW (rest-of-world) provinces warrant a similar check.
