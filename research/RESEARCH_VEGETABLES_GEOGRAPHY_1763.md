# RESEARCH — vegetables ("garden/market vegetables" trade good) 1763 geography

**Purpose:** replace the algorithmic reseed (task #5, commit e297d76b9 — "displace over-represented
grain near cities, breadth-first") with a SOURCED per-region assignment, matching the standard set by
`RESEARCH_NWCROP_GEOGRAPHY_64.md` (origin → 1763 distribution → per-region seed verdict). The heuristic
version is NOT defensible per-province; this doc is the sourcing it should have had.

**Scope note (what "vegetables" is here):** the catch-all garden/market-garden/kitchen vegetable
complex — brassicas (cabbage, bok choy, napa), alliums (onion, garlic, leek), cucurbits (gourd,
cucumber, melon, pumpkin), roots (turnip, radish/daikon, carrot, beet), legume-greens, leafy greens,
eggplant/aubergine, peppers-as-vegetable, etc. EXCLUDES the separately-modelled differentiated New
World crops (maize, potato, sweet_potato, tropical/temperate_fruit) and cash/specialty crops. Per the
never-touch rule those are not converted.

**Key historiographic fact that must shape the seeding:** in 1763 vegetables were overwhelmingly a
**local subsistence + PERI-URBAN MARKET-GARDEN** good, NOT a long-distance traded commodity (they are
perishable). So production density tracks (a) intensive-horticulture culture and (b) proximity to
population/urban demand and reliable water — NOT raw arable acreage. The good should be DENSE in
market-gardening heartlands and near big cities, THIN in pastoral/steppe/frontier/arid zones. A flat
"displace grain everywhere" spread (what the heuristic did) is historically wrong in the opposite way
to the original all-absent artifact.

## Per-region verdict (sources named inline)

### East Asia — the strongest correction, and the fine-fidelity core (China)
The classic case: F. H. King, *Farmers of Forty Centuries* (1911) documents the most intensive
vegetable market-gardening on earth — peri-urban truck gardens, multi-cropping, night-soil manuring —
across China, Korea, Japan. This is the region most wrongly seeded at ~0.
- **China (fine fidelity):** densest around the great cities and in the intensively-gardened macro-
  regions — **Jiangnan** (Jiangsu/Zhejiang around Suzhou-Hangzhou-Nanjing), **Lingnan** (Guangdong
  Pearl River delta around Canton), the **North China Plain** near Beijing/Tianjin (Zhili) and the
  Grand Canal cities (Shandong, Henan), **Sichuan basin** (Chengdu plain), and the mid-Yangzi cities
  (Hubei/Hunan/Jiangxi around Wuhan/Changsha/Nanchang). These are the truck-garden belts. → SEED
  STRONG in Jiangsu, Zhejiang, Guangdong, Zhili, Shandong, Sichuan, Hubei; MODERATE Henan, Hunan,
  Jiangxi, Anhui, Fujian, Guangxi, Liaoning. Prefer the province(s) hosting the macro-region's big
  city.
- **Korea:** napa cabbage + radish (the kimchi complex) — intensive vegetable culture, currently a
  literal 0. → SEED STRONG (Korea).
- **Japan:** daikon, greens, roots; dense peri-urban gardens around Edo/Osaka/Kyoto. → SEED MODERATE
  (Honshu strong, Kyushu/Shikoku moderate).

### Europe — market gardens, concentrated, NOT a flat spread
Intensive market gardening in 1763 was regionally specific, not universal:
- **Low Countries / Netherlands–Flanders:** the most advanced European horticulture (Dutch intensive
  market gardens). → STRONG where provinces exist.
- **Paris basin "marais" market gardens** (Île-de-France) and **English market gardens** around London
  (Lea Valley / Kent–Essex "garden of England"): genuine peri-urban vegetable belts. → MODERATE, ONE
  province at the metropolitan node each (Northern_France ~Paris; Southern_England ~London/Kent), NOT
  a broad grain-belt conversion.
- **Mediterranean irrigated huertas/orti:** Valencia–Murcia huerta (Iberia), Po Valley orti (Lombardy/
  Veneto), Provence/Languedoc, Campania. Long vegetable-gardening tradition. → MODERATE in
  Catalonia-Aragon (Valencia), Cisalpine/Venetia (Po), Occitanie, Southern/Central Italy.
- **Central/Eastern Europe & Russia — the cabbage/root belt:** cabbage (sauerkraut), turnip, beet,
  onion were dietary staples across the German lands, Poland, and Russia. → MODERATE in Central Europe
  (already a survivor, leave largely as-is), and a MODEST presence in the Russian core (Moscow region)
  and Poland — NOT the current sweep across steppe/Siberian frontier.
- **AVOID:** thin/pastoral/upland Iberian meseta, Scottish highlands, Irish subsistence (potato/oats
  country), and steppe frontier — the heuristic wrongly flipped grain here.

### Middle East / Mediterranean littoral — irrigated garden agriculture (strong where water is)
Bostan (market gardens) ringed Ottoman cities (Istanbul); the **Nile Delta/Valley** (Egypt) and the
**Damascus Ghouta** and Levant coastal plains were famous irrigated vegetable gardens (onions, garlic,
cucurbits, eggplant, mulukhiyah). Anatolian and Persian qanat-fed gardens likewise. → SEED MODERATE in
Egypt, Levant, Marmara/Anatolia (Istanbul node), Mesopotamia (Iraq irrigated), coastal Morocco/Tunisia;
THIN in Arabian/Saharan interior.

### South & Southeast Asia — widespread garden vegetables (moderate)
Brinjal (eggplant), gourds, okra, leafy greens, alliums were universal kitchen/market crops in the
Indian subcontinent and monsoon SE Asia, densest in the wet-rice deltas and near cities. India is
already a survivor (keep). → MODERATE, delta/urban-weighted: Bengal/Ganges, Deccan urban, Java (dense),
Vietnam/Siam deltas, Luzon/Visayas near Manila.

### Africa — kitchen gardens near settlement (moderate-to-thin)
Indigenous African horticulture: okra, cowpea/leaf, gourds, melons, leafy greens, onions — kitchen
gardens universal in SETTLED farming zones (Sahel towns, Ethiopian highlands, Yoruba/Hausa urban
belts, Swahili coast, Great Lakes), thin in pastoral/desert. → MODERATE at the settled/urban nodes of
Coastal West Africa, Sahel, Horn (Ethiopia), Lake Victoria; THIN elsewhere; AVOID Kalahari/desert.

### Americas — Three Sisters squash + colonial kitchen gardens (moderate, geographically real)
Indigenous "Three Sisters" (maize+beans+SQUASH) means garden vegetables (squash, beans-as-veg) were
grown wherever settled agriculture existed — Mesoamerica, Eastern Woodlands, Andean valleys, Pueblo
Southwest — plus European colonial kitchen gardens near towns (New England, Mid-Atlantic, Mexico
valley, Peru coast, Rio de la Plata). NOTE: squash/beans are represented via the vegetables good (not
separate). → MODERATE near settled/urban nodes (Central Mexico valley, New England/Mid-Atlantic towns,
Costa de Peru around Lima, Rio de la Plata, Chile central valley); AVOID open plains/Amazonia/Patagonia
frontier.

## Seeding rule that follows from the above (for the reseed tool)
1. **Tiered by sourced density, not "displace-grain-anywhere":**
   - STRONG tier (heaviest add): Jiangnan (Jiangsu/Zhejiang), Lingnan (Guangdong), Zhili, Shandong,
     Sichuan, Hubei; Korea; Low Countries; Nile/Egypt; Java. 
   - MODERATE tier: rest of intensively-gardened China macro-regions + Japan (Honshu), Mediterranean
     huertas/orti (Valencia/Po/Provence/Italy), Levant/Anatolia/Mesopotamia irrigated, India deltas,
     SE-Asia deltas, settled African urban nodes, American settled/urban nodes, Russian/Polish core.
   - THIN/AVOID: steppe, Siberian & N-American frontier plains, Arabian/Saharan/Kalahari desert,
     Andean altiplano (potato country), Irish/Scottish subsistence, Patagonia, Amazonia.
2. **Urban/water weighting:** within a seeded region, prefer the province at the metropolitan node or
   the irrigated delta (highest civilization_value / known city), reflecting peri-urban market gardens —
   one node province, not the whole grain belt.
3. **Displace over-represented grain/livestock ONLY** (never fish/cash/NW-differentiated/existing veg),
   keep the ≥60%-of-region depletion guard.
4. **China gets fine granularity** (per-province node selection in the truck-garden belts); ROW is
   seeded at the regional-node level (China fine-fidelity / ROW-abstraction standing rule).

## Honest limits
- This is documented per-REGION with named horticultural traditions + a primary anchor (King 1911) and
  well-established economic-history facts (Dutch/marais/huerta/bostan/Ghouta market gardens, Three
  Sisters, kimchi complex). It is NOT a per-province primary-source census — no such 1763 vegetable
  cadastre exists at province granularity for the whole world. The region-tier + urban-node rule is the
  defensible translation of the sourced record onto the map, which is exactly how NWCROP #64 handled
  maize/chili (region-level verdicts, not per-province deeds).
- Magnitude (how many provinces per tier) stays boot-tunable; geography (WHICH regions, weighted) is
  now sourced rather than "wherever grain was over-represented near a city."
