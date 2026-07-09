# RIFLE_PRODUCTION_1815.md — sited rifle production (#281 fix)

Academic research (EN + FR/DE/RU native-language agents, runs wk1kglemi + province lookup wf_f16d7f78).
THE #281 BLOCKER: rifles was a new manufactured good with pop+army demand but NO baseline production
anywhere (only the Qing arsenal event ever set trade_goods=rifles), so it ran a false global shortage.
FIX: assign trade_goods=rifles to the real early-19thC small-arms manufacturing provinces below.
Sited sparsely (15 provinces), >=1 per great power, like munitions/artillery.

## Provinces assigned trade_goods = rifles (map_data/province_setup.csv, col 4)
| prov | town | power |
|---|---|---|
| 9889 | Birmingham | GBR gun trade |
| 6426 | Liege | NED/Belgium |
| 2376 | Saint-Etienne area | FRA |
| 4231 | Tulle area | FRA royal manufacture |
| 353 | Tula | RUS state arsenal |
| 6135 | Izhevsk/Vyatka | RUS |
| 3174 | Sestroretsk/St Petersburg | RUS |
| 3853 | Springfield | USA national armory |
| 89 | Harpers Ferry/WV | USA |
| 308 | Steyr/Linz | AUS |
| 403 | Ferlach | AUS gun trade |
| 245 | Vienna Zeughaus | AUS state |
| 9218 | Suhl | German gun trade (SWM) |
| 929 | Spandau/Berlin | PRU royal Gewehrfabrik |
| 1882 | Eskilstuna | SWE |

NOTE traps avoided: Tower of London (storage), Weipert (hunting guns), Zlatoust (edged weapons),
Tophane (cannon foundry), Waltham Abbey (gunpowder) — NOT assigned rifles.

## PENDING (needs boot test): after confirming no phantom shortage on a supplied country, re-add the
reverted se_LOGISTICS shortage_phys_rifles scan + army-linked DEMAND_rifles term.

---

## Full research synthesis

## Consolidated sited-rifles list (deduplicated, ranked)

### TIER 1 — the ~13 that should DEFINITELY produce rifles (trade_goods = rifles)

| # | Town | Country / region (for province match) | Type | Why |
|---|------|----------------------------------------|------|-----|
| 1 | **Birmingham** | Britain — Warwickshire / West Midlands | private trade | Dominant volume producer; ~2/3 of English output, the "gun quarter" |
| 2 | **Liège** | United Kingdom of the Netherlands → Belgium (1830); Meuse valley | private trade | One of the largest small-arms centres on earth in this window |
| 3 | **Saint-Étienne** | France — Loire (Forez/Lyonnais) | state + private | Leading French centre; royal/national manufacture + huge private fabrique |
| 4 | **Tula** | Russia — Tula Governorate | state | Largest Russian works; ~100k stand/yr in wartime |
| 5 | **Springfield** | USA — Massachusetts | state (federal) | First US national armory; interchangeable-parts pioneer |
| 6 | **Harpers Ferry** | USA — Virginia (now West Virginia) | state (federal) | Second national armory; Hall's Rifle Works / M1819 |
| 7 | **Izhevsk** | Russia — Vyatka Governorate | state | Rising second Russian producer |
| 8 | **Steyr** | Austria — Upper Austria | private (contracted) | Leading Erblande small-arms centre (pre-Werndl craft base) |
| 9 | **Ferlach** | Austria — Carinthia | private guild | Major army supplier; 308 master gunmakers in 1845 |
| 10 | **Enfield (Enfield Lock)** | Britain — Essex / Lea Valley | state arsenal | Intended state arms works (built 1816); strategically primary though output modest until 1856 |
| 11 | **Tulle** | France — Corrèze (Limousin) | state | Principal royal manufacture for military longarms |
| 12 | **Sestroretsk** | Russia — St Petersburg Governorate | state | Third state firearms works, near the capital |
| 13 | **Vienna** | Austria — Lower Austria / Vienna | state | Imperial Zeughaus / k.k. Gewehrfabrik (the OLD arsenal — the grand 1849-56 Arsenal is anachronistic) |

### TIER 2 — longer tail (optional / lower-output; site sparingly)

| Town | Country / region | Type | Note |
|------|------------------|------|------|
| **London gun trade** (Minories/City) | Britain — City of London | private | Second English proof house; high-grade & EIC contract arms |
| **Châtellerault** | France — Vienne (Poitou) | state | Founded 1819, inherits Charleville (closed 1836); still building up |
| **Eskilstuna** (Carl Gustafs stad) | Sweden — Södermanland | state | Sweden's main new state rifle factory (1812) |
| **Huskvarna** | Sweden — Jönköping/Småland | private | Privatised crown musket works supplying the crown |
| **New Haven / Whitneyville (Hamden)** | USA — Connecticut | private contractor | Whitney armory; American-system contractor |
| **Middletown / Berlin** | USA — Connecticut | private contractor | Simeon North; pistols + Hall breech-loaders |
| **Mutzig** | France — Bas-Rhin (Alsace) | state | Minor frontier royal manufacture |
| **Maubeuge** | France — Nord | state | Minor frontier royal manufacture |
| **Lewisham** | Britain — Kent/SE London | state | Live only at the very start (collapsed post-1815, sold 1819) — skip unless you want a pre-1819 flavour |

### DO NOT assign rifles here (documented traps in the research)
- **Tower of London** — inspection/storage/pattern only after 1811; not manufacture.
- **Weipert (Vejprty)**, Bohemia — lost military work; hunting guns/pistols only.
- **Zlatoust**, Ural — edged weapons (sabres), not firearms.
- **Istanbul / Tophane-i Amire** — cannon & shot foundry, not small arms.
- **Waltham Abbey** — gunpowder (propellant), not small arms.

---

### ⚠️ Coverage GAP — "germanic" was returned EMPTY
No German/Prussian centres were researched, so no rifle province can be sited for the largest gap in the map. Before finalizing you should research and almost certainly add:
- **Suhl** (Thuringia) — the historic German gun-trade town, the "Birmingham of Germany" (Tier 1 candidate).
- **Spandau / Potsdam** (Brandenburg, Prussia) — Prussian royal Gewehrfabrik (state, Tier 1–2).
- **Danzig** and **Saarn/Sömmerda** — secondary Prussian arms works.
Treat these as unconfirmed until sourced, but Germanic must not ship with zero rifle provinces.

---

### Design note — realistic COVERAGE (siting sparsely)
Early-19thC rifle-making was concentrated in a **handful of specialised towns per power**, not spread across the map — either (a) a state arsenal cluster or (b) a dense private gun-trade town with a proof house. So:
- **Site rifles like munitions/artillery: rare, deliberate, one node of prestige per power.** Give each great power at least ONE rifle province (state arsenal or gun-trade town), but keep the total map count low — roughly the Tier-1 set plus a few Tier-2, ~15-22 provinces total.
- **Model both siting patterns:** state arsenals (Tula, Springfield, Enfield, Vienna, Tulle) AND private gun-trade clusters (Birmingham, Liège, Saint-Étienne, Steyr, Ferlach, Suhl). These are the map's "gunsmith cities."
- **Anchor to the correct province, mind the anachronisms:** Enfield's mass output and Vienna's grand Arsenal both postdate the window — assign the good (a strategic capacity), but they read as small/state works pre-1840, not mass producers. Izhevsk and Châtellerault are *rising*, so if your economy layer supports growth they're good "expands over the campaign" nodes.
- **Belgium/Liège is a must-have** even though it isn't a great power — it was a top-3 world producer and a natural neutral arms exporter; ideal as a contestable/tradeable rifle source.
