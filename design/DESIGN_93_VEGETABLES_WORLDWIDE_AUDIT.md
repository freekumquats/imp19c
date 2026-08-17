# DESIGN (draft, pre-review) — worldwide vegetables province-count audit

## Question

Sibling to `DESIGN_93_VEGETABLES_PROVINCE_COUNT_AUDIT.md` (China-scoped, concluded NO CHANGE),
but explicitly WORLDWIDE per direct user correction: "no you fool you were supposed to look
worldwide for where more vegetables would be historically justified." Same question, no China
limit: does the mod's `trade_goods=vegetables` map (418 provinces worldwide, almost entirely
inside China) undercount any real historical market-garden region outside China?

## Research (dispatched agent, worldwide scope, mixed source quality — graded honestly below)

**Sourced (moderate-strong confidence)**:
- **Paris / Île-de-France, maraîchage.** Real, named, documented market-garden industry
  immediately outside the city walls (the *Marais* district — literally "marsh" — and later
  the Left Bank market gardens). Sourced via fr.wikipedia.org.
- **Amiens, Hortillonnages.** Real, documented floating/marsh market gardens, still extant
  today as a heritage site. Same source pass.
- **Geneva, Plainpalais.** Documented market-garden plain adjacent to the city, worked in part
  by Huguenot refugee gardeners. Same source pass.

**Unsourced this session, from-memory, medium confidence (flagged by the research agent itself
as needing a follow-up source check before being treated as fact)**:
- London: Neat House Gardens, Fulham, Battersea market gardens.
- Ottoman Istanbul/Damascus: *bostan* urban market gardens; Damascus's al-Ghouta oasis.
- Japan, Edo/Kyoto: *kyo-yasai* (Kyoto heirloom vegetables) tradition.

**Checked and found weak/negative**:
- Netherlands/Westland: the famous glasshouse vegetable industry is 19th-20th century, not
  1600-1800 — too late for this mod's 1763 bookmark.
- Mexico City chinampas: real, but historically a maize/beans/squash system; the vegetable-
  specific framing is weak for 1763 specifically.
- India: no strong candidate surfaced.

**Overall assessment from the research pass**: no region found anywhere, sourced or
unsourced, operates at cash-crop-belt SCALE. Every real case — Paris, Amiens, Geneva, and the
unverified London/Istanbul/Damascus/Kyoto flags — fits the identical shape already found for
China: a narrow ring of market gardens immediately outside one specific city's walls, not a
broad province-spanning regional specialty. Paris/Île-de-France (plus Amiens, Nevers as a
Loire-valley grain comparator, and Geneva) is the single strongest SOURCED candidate worth a
direct data check, since it is the only claim resting on citable sources rather than memory.

## Direct check against the mod's own data

Checked the mod's actual province files for the sourced candidate region (province IDs found
by name-comment grep in `setup/provinces/*.txt`):

| Location | Current `trade_goods` | Province rank |
|---|---|---|
| Paris (5013) | `grain` | city_metropolis |
| Amiens (7781) | `grain` | city |
| Nevers (5899) | `grain` | settlement |
| Geneva (2265) | `livestock` | city |

None of these are empty, and none carry an unrelated or dubious tag — Paris/Amiens/Nevers all
carry `grain` (Île-de-France and the Loire valley are real, well-documented grain breadbasket
regions for this period; Paris importing grain from its own surrounding farmland is the
dominant historical fact about its food supply, more so than its market gardens), and Geneva
carries `livestock` (also a real regional specialty, unrelated to and not contradicted by its
documented market gardens).

**[Correction, caught by independent review]** An earlier draft of this doc claimed these
three files contain zero `vegetables`-tagged provinces. That claim was FALSE — a narrower
grep (missing rows further than 3 lines from the province header on some blocks) produced a
false negative. Re-checked directly with a correct grep: `00_Northern_France.txt` and
`00_Grand_Est.txt` DO use the tag, 11 times between them (`00_Helvetia.txt` alone is
genuinely zero):

| Location | Rank |
|---|---|
| Abbeville, Boulogne-sur-Mer, Dreux, Dieppe (Northern France) | settlement |
| Cambrai, Arras (Northern France) | city |
| Haguenau, Verdun, Chaumont, Commercy (Grand Est) | settlement |
| Vesoul (Grand Est) | city |

This actually strengthens, rather than undercuts, the "no change" case, once read correctly:
the mod already places `vegetables` in this exact region — just not at Paris/Amiens/Nevers
specifically. The pattern is the same one the China audit found at Baoji (Xi'an's own
hinterland already carries vegetables while Xi'an itself carries silk): the tag is used at
the smaller/secondary towns in a cluster while the largest, most historically dominant city
(Paris — a city_metropolis, an order of civilization_value above every other checked
province here) keeps its real, better-documented specialty (grain). This is the mod
discriminating correctly by city size/rank, not omitting the tag from a whole region.

## Free data check on the unsourced-from-memory candidates (review-driven)

Per independent review: checking a province's CURRENT tag against the mod's own file is a free
mechanical grep, not a sourcing exercise — it costs nothing and should never be gated on
whether the underlying historical claim is cited. Ran it for all four unsourced-from-memory
candidate cities:

| City | Current `trade_goods` | Rank | Any `vegetables` tag elsewhere in that city's region file? |
|---|---|---|---|
| London (3388, Southern England) | `stone` | city_metropolis | Yes — 5 elsewhere in `00_Southern_England.txt` |
| Konstantiniyye/Istanbul (7709, Marmara) | `silk` | city_metropolis | No — 0 in `00_Marmara.txt` |
| Damascus (299, Syria) | `iron` | city | No — 0 in `00_Syria.txt`/`00_syria_region.txt`/`00_Levant.txt` |
| Kyoto (4624, Honshu) | `silk` | city | No — 0 in `00_Honshu.txt` |

None of the four cities themselves carry `vegetables`, and none carry an obviously wrong or
placeholder tag — Istanbul and Kyoto both carry `silk` (both real, well-documented historical
silk centers, at least as strong a claim as their market-garden traditions), Damascus carries
`iron`, London carries `stone` (odd on its face but pre-existing and out of scope for this
audit — not a vegetables question). This is the same shape as every other check in this
document and the China audit: real cities keep their own independently-justifiable specialty;
no case surfaces where `vegetables` is obviously the missing or correct tag.

## Recommendation: NO CHANGE, worldwide

1. No region anywhere in the world — sourced or unsourced-from-memory — shows evidence at the
   scale the mod's `trade_goods` field is meant to represent (a province's DEFINING product).
   Every real case, including the best-sourced one (Paris), is a narrow city-wall ring, exactly
   matching the already-established China pattern.
2. Every city checked directly against the map (Paris, Amiens, Nevers, Geneva, and — per the
   free-check extension above — London, Istanbul, Damascus, Kyoto) already carries a different,
   defensible, real historical specialty. Same result as every China spot-check, and now
   confirmed across all eight candidate cities, not just the sourced French cluster.
3. The region-level data (corrected above) shows the mod ALREADY uses `vegetables` in the
   Paris/Picardy/Lorraine area, at the secondary/settlement-tier towns — the same
   city-size discrimination pattern the China audit found at Baoji. This is evidence the
   existing map is applying the "narrow, city-ring, minor product" rule correctly, not
   evidence of a systematic gap to fix.

This does NOT touch or revert the production-multiplier fix already shipped
(`GOODS_vegetables_production_multiplier = 4`) or the China-scoped audit's conclusion — both
stand independently of this worldwide question.

## Review outcome (adversarial review, 2026-08-17) — factual error found and corrected

Reviewed independently. First draft's "zero vegetables tags in this region" claim was FALSE
(a narrow grep produced a false negative) — the review agent caught it, I independently
re-ran and confirmed the correction above (11 real instances, France/Lorraine). The review's
required fixes are applied: the false claim is replaced with the real 11-province list, the
old point 4 (which rested on the false claim) is dropped, and the free data check was run for
all four previously-unchecked candidate cities (London/Istanbul/Damascus/Kyoto) rather than
setting them aside for lack of sourcing — per the review's correct distinction that a free
mechanical file check is not gated by whether the underlying historical claim is cited.
**Final verdict, unchanged by the correction: NO CHANGE, worldwide.** The corrected data made
the case stronger, not weaker — the region already discriminates by city size the same way
China's map does, and all four additional candidate cities check out the same as every prior
one.
