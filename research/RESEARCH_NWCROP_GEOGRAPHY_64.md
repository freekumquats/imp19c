# RESEARCH #64 — New World crop 1763 geography (feeds #64 seeding + #62 demand)

**Date:** 2026-08-10. Region/area keys verified directly against common/province_setup.csv (col16=AREA) + map_data/regions.txt. Current seeding verified by grep (col4=TRADEGOOD).

## Current (broken) seeding — verified
- maize = 6 provinces, ALL China (Hunan/Jiangxi)
- sweet_potato = 6 (4 China Fujian/Guangdong + 2 Costa de Peru)
- potato = 5, ALL Americas but WRONG sub-region: New Mexico ×2, Atacama de Peru ×2, Potosí ×1
- peanut = 5, ALL China (Guangdong/Fujian)
- chili = 6, ALL China (Hunan)

Confirmed American mod areas exist: New Mexico/American_Southwest, Appalachia, Northern_Mexico, Pacific_Mexico, Eastern_Mexico, Central_America, Antilles (Lesser_Antilles), Argentina, Costa de Peru, Atacama de Peru, Potosi, five Brazil regions.

## Per-crop verdict

**MAIZE** — Mesoamerican origin; by 1763 THE dominant staple grain across ~the whole Western Hemisphere (Mesoamerica, N.American woodlands, Andean valleys, Caribbean, Brazil-secondary). Old World: major in W.Africa, moderate Iberia/Balkans, a real-but-MINORITY spread through SW China hill country (Ho Ping-ti thesis). SUBSISTENCE everywhere; not an export crop. MAJOR staple.
→ SEED: Eastern_Mexico, Pacific_Mexico, Northern_Mexico, Central_America (core, top priority), Antilles, Costa/Atacama de Peru (valleys), American_Southwest, Appalachia, Argentina, Brazil ×5 (minor). KEEP Hunan/Jiangxi but as a MINORITY share.

**SWEET_POTATO** — Tropical-American origin (secondary there behind maize/manioc/potato); introduced Fujian ~1594, MAJOR south-China staple by 1763 (the one crop where China legitimately IS the center of gravity). Subsistence both hemispheres.
→ KEEP Fujian/Guangdong (correct, don't touch) + the 2 Costa de Peru (correct). ADD minor: Antilles, Central_America/Eastern_Mexico lowlands, Brazil. Basically right already — minor rounding-out only.

**POTATO** — Andean altiplano origin; by 1763 THE staple of the Andean HIGHLANDS specifically (Potosí, Atacama/Puno highlands) because maize can't grow at altitude; fed the Potosí mining population (chuño). Old World: significant in Ireland, marginal continental Europe, NEGLIGIBLE in China at 1763 (potato didn't gain Chinese traction until 19th–20th c.). Subsistence + local-market trade to Potosí miners. MAJOR but geographically narrow.
→ CONCENTRATE in Potosi + highland Atacama de Peru / Costa de Peru. **CORRECTION: New Mexico is WRONG** — Pueblo agriculture was maize/beans/squash (Three Sisters), never potato; the 2 New Mexico potato provinces are misplaced within the Americas (right hemisphere, wrong sub-region → move to Andean highlands). Ireland minor if provinces exist; leave Old World thin (correct near-zero 1763 China).

**PEANUT** — South-American origin (Bolivia–Paraguay–Brazil border domestication + coastal Peru); spread to W.Africa (16th c.) + coastal China (Fujian/Guangdong, 16th–17th c.), minor-to-moderate by 18th c. SUBSISTENCE everywhere in 1763. **IMPORTANT: the W.African groundnut EXPORT boom is 19th-c. (post-1830s) — must NOT be modeled as a cash-export good at 1763.** Minor/garden crop everywhere.
→ KEEP modest Guangdong/Fujian. ADD native range: Brazil (esp. Northeast/North), Costa de Peru, Antilles. W.African provinces if they exist — minor, subsistence, NOT export-tagged.

**CHILI** — Multiple Mesoamerican + Andean domestications; by contact the dominant flavoring across the ENTIRE pre-Columbian Americas (universal garden crop). Post-1492 explosive Portuguese-network spread to W.Africa, India (Goa), SE Asia, China. By 1763 an established Chinese presence is reasonable (interior/upland) — but the intensive Hunan/Sichuan chili-cuisine identity is more a later 18th–19th-c. intensification. A GARDEN/kitchen-spice crop everywhere, NOT a plantation export. **Validates #62's decision to keep chili luxury-only (condiment, not bulk food).** Minor by volume, culturally near-universal — the most pan-American of the five.
→ ADD real American range: Eastern/Pacific_Mexico, Central_America (core), Costa/Atacama de Peru (ají), Antilles, Brazil. KEEP Hunan modest (don't expand). India/W.Africa minor if provinces exist.

## Summary table
| Crop | Core region(s) | Current | Fix |
|---|---|---|---|
| maize | Mesoamerica, N.America, Andes, Caribbean, Brazil (+minor China) | 100% China | ADD Americas broadly; demote China to minority |
| sweet_potato | Trop.America (minor) + China (major, correct) | China + 2 Costa de Peru | minor Americas rounding-out only |
| potato | Andean highlands (Potosí/Atacama) | 100% Americas, WRONG sub-region (New Mexico) | move New Mexico → Potosi/Atacama highlands |
| peanut | S.America (Brazil/coastal Peru) + coastal China (minor) | 100% China | ADD Brazil/Costa de Peru/Antilles |
| chili | pan-American garden crop + post-1500 China/India/W.Africa | 100% China (Hunan) | ADD Mesoamerica/Andes/Antilles/Brazil; keep China minor |

## Downstream for #62 (H3 resolved)
Once maize/peanut have real American subsistence producers (not just China), each crop's food-vs-luxury basket decision can be made per-region on CORRECT geography rather than the all-China artifact. Potato's Andean-highland concentration (once off New Mexico) supports treating it as a genuine regional subsistence staple there, distinct from near-absence in China.
