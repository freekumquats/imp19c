# 1763 Central Europe / HRE DELTA Plan

**Target**: Convert 1815 baseline → 1763.02.16 (day after Treaty of Hubertusburg)  
**Scope**: Central Europe + Holy Roman Empire only (Italy/Americas/MENA/Asia covered in separate DELTAs)  
**Date**: 2026-07-08  

---

## EXECUTIVE SUMMARY

This is the **SINGLE LARGEST EUROPEAN MAP CHANGE** between 1815 and 1763. The Holy Roman Empire's 300+ constituent states (including 3 ecclesiastical Electorates, ~50 prince-bishoprics, ~51 imperial free cities) were **completely dissolved** between 1803-1806 via:
- **1803 Reichsdeputationshauptschluss** (Imperial Recess) — all ecclesiastical territories secularized, 45 free cities mediatized
- **1806 dissolution** of the HRE itself

**1815 reality**: 39 states in German Confederation; no ecclesiastical states; 4 surviving free cities (Hamburg, Bremen, Lübeck, Frankfurt)  
**1763 reality**: ~300 HRE states; 8 Electors (3 ecclesiastical); dozens of prince-bishoprics; 51 free cities; functioning imperial institutions

**Implementation scope decision**: Represent **15-25 MAJOR states** explicitly; fold minor principalities/free cities into their 1815 absorbers. Focus on:
- The 8 Electorates (including the 3 ecclesiastical)
- Major prince-bishoprics (Salzburg, Würzburg, Bamberg, Münster, Paderborn, etc.)
- Largest secular states (Austria, Prussia, Bavaria, Saxony, Hanover, Württemberg, Baden, Hesses, Mecklenburgs, Brunswick)
- Largest free cities (Frankfurt, Hamburg, Lübeck, Cologne, Nürnberg, Augsburg — as republics)

**NOT implemented**: 200+ minor principalities, imperial knights, tiny free cities, prince-abbacies. These are folded into their 1815 absorbers (e.g., Prince-Abbacy of Kempten → Bavaria's 1815 provinces).

---

## SECTION A: TAGS TO REUSE (Exist in 1815, alive in 1763)

These tags already exist in `countries.txt` and just need ruler/date/border adjustments.

| **Tag** | **1815 Name** | **1763 State** | **Capital AREA** | **Ruler 1763** | **Changes Needed** |
|---------|---------------|----------------|------------------|----------------|-------------------|
| **AUS** | Austria | Austrian Empire (Habsburg hereditary lands) | Niederosterreich | Maria Theresa (Archduchess, co-ruler Francis I as Emperor) | Ruler change; territory = Bohemia + Austria + Hungary + Styria + Tyrol + Lombardy + Galicia (pre-1772 partitions) |
| **PRU** | Prussia | Kingdom in Prussia | Preussen | Frederick II (the Great) | Ruler same; **Silesia PRUSSIAN** (confirmed Treaty of Hubertusburg 1763.02.15) |
| **BAV** | Bavaria | Electorate of Bavaria | Bavaria (Munich area) | Maximilian III Joseph (Elector) | Ruler same; smaller territory (no Würzburg/Bamberg/Franconia — those are separate ecclesiastical states in 1763) |
| **SAX** | Saxony | Electorate of Saxony | Sachsen-Anhalt (Dresden area) | Friedrich August II (Elector; also Augustus III of Poland, dies **5 Oct 1763**) | Ruler same (dies 8 months after start date); personal union with Poland |
| **HAN** | Hannover | Electorate of Hanover | Hannover | George III (Elector; also King of Great Britain) | Ruler same; personal union with Britain; no Osnabrück (separate prince-bishopric in 1763) |
| **WUR** | Württemberg | Duchy of Württemberg | (Württemberg area) | Karl I Eugen (Duke) | Ruler same; smaller territory (no mediatized free cities/ecclesiastical lands) |
| **HSK** | Hesse-Kassel | Landgraviate of Hesse-Kassel | (Hesse-Kassel area) | Friedrich II (Landgrave) | Ruler same |
| **HSD** | Hesse-Darmstadt | Landgraviate of Hesse-Darmstadt | (Hesse-Darmstadt area) | Ludwig VIII (Landgrave, r. 1739-1768) | Ruler change |
| **BAD** | Baden | Margraviate of Baden-Durlach | (Baden area) | Karl Friedrich (Margrave, r. 1746-1811) | Ruler same; smaller territory (Baden-Baden separate until 1771; no Konstanz/Basel ecclesiastical lands) |
| **MKS** | Mecklenburg-Schwerin | Duchy of Mecklenburg-Schwerin | (Mecklenburg area) | Friedrich II (Duke, r. 1756-1785) | Ruler same |
| **MKZ** | Mecklenburg-Strelitz | Duchy of Mecklenburg-Strelitz | (Mecklenburg area) | Adolf Friedrich IV (Duke, r. 1752-1794) | Ruler same |
| **BRG** | Braunschweig (Brunswick) | Duchy of Brunswick-Wolfenbüttel | (Brunswick area) | Karl I (Duke, r. 1735-1780) | Ruler same |
| **OLD** | Oldenburg | County of Oldenburg | (Oldenburg area) | Ruled by Danish kings in personal union | Same status |
| **ANH** | Anhalt | Principality of Anhalt | (Anhalt area) | Multiple lines (Anhalt-Dessau, -Bernburg, -Köthen, -Zerbst) | Still subdivided in 1763 |
| **SWI** | Switzerland | Old Swiss Confederacy | (Swiss areas) | Confederation of 13 cantons + associates | Same structure |
| **FRK** | Frankfurt | Free City of Frankfurt | Frankfurt am Main area | Republic | Surviving imperial free city (seat of imperial coronations) |
| **HAM** | Hamburg | Free City of Hamburg | Hamburg area | Republic | Surviving Hanseatic free city |
| **LBK** | Lübeck | Free City of Lübeck | (Lübeck area) | Republic | Surviving Hanseatic free city |
| **BRE** | Bremen | Free City of Bremen | Bremen area | Republic | Surviving Hanseatic free city |
| **NAS** | Nassau | Duchy of Nassau | (Nassau area) | Multiple lines in 1763 (Nassau-Usingen, Nassau-Weilburg, Nassau-Saarbrücken) | Consolidated into Duchy of Nassau 1806; in 1763 multiple principalities |
| **HUN** | Hungary | Kingdom of Hungary (Habsburg) | Pressburg/Buda area | Maria Theresa (as Queen of Hungary) | Part of Habsburg hereditary lands |
| **TRS** | Transylvania | Principality of Transylvania (Habsburg) | (Transylvania area) | Habsburg governance | Part of Habsburg realm |
| **CRO** | Croatia | Kingdom of Croatia (Habsburg) | (Croatia area) | Habsburg governance | Part of Habsburg realm |
| **POL** | Poland | Polish-Lithuanian Commonwealth | (Poland area) | Augustus III (also Elector of Saxony, r. 1733-1763) | **Personal union with Saxony**; pre-1772 partition borders |
| **LIT** | Lithuania | Grand Duchy of Lithuania | (Lithuania area) | Royal union junior partner of Poland | **Commonwealth structure** (pre-partition) |

---

## SECTION B: NEW TAGS REQUIRED (Ecclesiastical States + Missing Secular States)

These states exist in 1763 but **DO NOT exist in 1815** (secularized/mediatized 1803-1806). Require new tag creation.

### B1. The Three Ecclesiastical Electorates

| **Proposed TAG** | **State Name** | **Capital AREA** | **Culture** | **Religion** | **Ruler 1763** | **Notes** |
|------------------|----------------|------------------|-------------|--------------|----------------|-----------|
| **MNZ** ✓ FREE | Electorate & Archbishopric of Mainz | Mainz area (Rhine) | german | catholic | Emmerich Joseph von Breidbach zu Bürresheim (r. 1763-1774) | **Imperial Archchancellor for Germany**; appointed Feb 1763 (this month) |
| **KLN** ✓ FREE | Electorate & Archbishopric of Cologne | Cologne area (Rhine) | german | catholic | Maximilian Friedrich von Königsegg-Rothenfels (r. 1761-1784) | **Imperial Archchancellor for Italy**; also ruled Prince-Bishopric of Münster |
| **TRR** ✓ FREE | Electorate & Archbishopric of Trier | Trier area (Mosel) | german | catholic | Johann IX Philipp von Walderdorff (r. 1756-1768) | **Imperial Archchancellor for Burgundy** |

**Tag collision note**: TRI already taken (Tripoli, line 306 of countries.txt). Use **TRR** for Trier.

**Government type**: `theocracy` (ecclesiastical elective monarchy; prince-bishops elected by cathedral chapters)  
**TO BUILD**: 
- `setup/countries/c_europe/mainz.txt`
- `setup/countries/c_europe/cologne.txt`
- `setup/countries/c_europe/trier.txt`
- Add to countries.txt after line 57 (after CRO)
- `setup/main/00_default.txt` character definitions for the three archbishops (1763 officeholders)

### B2. Major Prince-Bishoprics

| **Proposed TAG** | **State Name** | **Capital AREA** | **Culture** | **Religion** | **Ruler 1763** | **Absorbed by (1803)** |
|------------------|----------------|------------------|-------------|--------------|----------------|----------------------|
| **SZG** ✓ FREE | Prince-Archbishopric of Salzburg | Salzburg | german (south_german) | catholic | Sigismund III von Schrattenbach (r. 1753-1771) | → Bavaria 1803, Austria 1816 |
| **WUE** ✓ FREE | Prince-Bishopric of Würzburg | (Franken area) | german | catholic | Adam Friedrich von Seinsheim (r. 1755-1779, also held Bamberg) | → Bavaria 1803 |
| **BAM** ✓ FREE | Prince-Bishopric of Bamberg | (Franken area) | german | catholic | Adam Friedrich von Seinsheim (r. 1757-1779, also held Würzburg) | → Bavaria 1803 |
| **MUN** ✓ FREE | Prince-Bishopric of Münster | (Westphalia area) | german | catholic | Maximilian Friedrich von Königsegg-Rothenfels (also Elector of Cologne) | → Prussia 1803 |
| **PDB** ✓ FREE | Prince-Bishopric of Paderborn | (Westphalia area) | german | catholic | Wilhelm Anton von Asseburg (r. 1763-1782, just took office) | → Prussia 1803 |
| **OSN** ✓ FREE | Prince-Bishopric of Osnabrück | (Lower Saxony area) | german | protestant/catholic (alternating) | Clemens August of Bavaria (r. 1728-1764, Catholic bishop, dies next year) | → Hanover 1803 |
| **HLD** ✓ FREE | Prince-Bishopric of Hildesheim | (Lower Saxony area) | german | catholic | Friedrich Wilhelm von Westphalen (r. 1763-1789, just appointed) | → Prussia 1803 |
| **AUG** ✓ FREE (tag collision: EIC = East India Company) | Prince-Bishopric of Augsburg | (Swabia/Bavaria area) | german | catholic | Joseph Ignaz Philipp von Hessen-Darmstadt (r. 1740-1768) | → Bavaria 1803 |
| **FRS** ✓ FREE | Prince-Bishopric of Freising | (Bavaria area) | german | catholic | Johann Theodor (r. 1727-1763, dies this year) | → Bavaria 1803 |
| **PAS** ✓ FREE | Prince-Bishopric of Passau | (Bavaria/Austria border area) | german | catholic | Joseph Maria von Thun und Hohenstein (r. 1761-1763, dies this year) | → Bavaria 1803 |
| **REG** ✓ FREE | Prince-Bishopric of Regensburg | (Bavaria area) | german | catholic | Clemens Wenzeslaus of Saxony (r. 1763-1769, just appointed) | → Bavaria 1810 |
| **SPY** ✓ FREE | Prince-Bishopric of Speyer | (Palatinate/Rhine area) | german | catholic | Franz Christoph von Hutten zum Stolzenberg (r. 1743-1770) | → Baden 1803 |
| **WRM** ✓ FREE | Prince-Bishopric of Worms | (Rhine area) | german | catholic | Held with Konstanz | → Hesse-Darmstadt 1803 |
| **KST** ✓ FREE (KON taken = Congo) | Prince-Bishopric of Konstanz (Constance) | (Lake Constance/Swiss border area) | german | catholic | Franz Konrad von Rodt (r. 1750-1775) | → Baden 1803 |
| **BAS** ✓ FREE | Prince-Bishopric of Basel | (Swiss border area) | german | catholic | Simon Nicolas de Montjoie (r. 1762-1775, just took office) | → Various states |
| **STB** ✓ FREE (Strasbourg) | Prince-Bishopric of Strasbourg | (Alsace area) | german | catholic | Louis Constantin de Rohan-Guéméné (r. 1756-1779) | → France (already annexed 1681, but retained some imperial privileges) |
| **TRN** ✓ FREE | Prince-Bishopric of Trent (Trento) | (Tyrol/Italy border area) | german/italian | catholic | Cristoforo Sizzo de Noris (r. 1748-1763, dies this year) | → Austria |
| **BRX** ✓ FREE | Prince-Bishopric of Brixen (Bressanone) | (Tyrol/Italy border area) | german/italian | catholic | Leopold Maria Joseph von Spaur (r. 1747-1778) | → Austria |
| **FUL** ✓ FREE | Prince-Abbacy of Fulda | (Hesse/Thuringia area) | german | catholic | Heinrich VIII von Bibra (r. 1759-1788, also Prince-Abbot) | → Prussia 1803, then Nassau |

**Government type**: `theocracy` (ecclesiastical elective principality)  
**TO BUILD**: 
- 18 new country files in `setup/countries/c_europe/`
- Add 18 entries to countries.txt after existing C.Europe block (after line 57)
- Character definitions in `setup/main/00_default.txt` for all 18 prince-bishops
- Province ownership changes in `setup/main/province_setup.csv` (move provinces from 1815 absorbers back to ecclesiastical states)

### B3. Secular Principalities (Missing from 1815)

| **Proposed TAG** | **State Name** | **Capital AREA** | **Culture** | **Religion** | **Ruler 1763** | **Notes** |
|------------------|----------------|------------------|-------------|--------------|----------------|-----------|
| *(None identified as critical)* | Multiple Nassau lines | (Nassau area) | german | protestant/catholic | Various | **NAS tag exists** but represents consolidated 1806 Duchy; in 1763 subdivided (Nassau-Usingen, Nassau-Weilburg, Nassau-Saarbrücken, Nassau-Dietz). **Fold into NAS** for simplicity. |
| *(Fold into ANH)* | Anhalt sub-divisions | (Anhalt area) | german | protestant | Multiple princes | **ANH tag exists**; in 1763 subdivided (Anhalt-Dessau, -Bernburg, -Köthen, -Zerbst). **Fold into ANH** for simplicity. |

**Implementation decision**: Represent Nassau and Anhalt as single tags (NAS, ANH) even though historically subdivided in 1763. The subdivision is minor for gameplay purposes.

### B4. Major Imperial Free Cities (Beyond HAM/BRE/LBK/FRK)

In 1763, ~51 imperial free cities existed. By 1815, only 4 survived (Hamburg, Bremen, Lübeck, Frankfurt). The largest 1763 free cities that were **mediatized 1803-1806**:

| **City** | **1815 Absorber** | **Proposed Action** | **Notes** |
|----------|-------------------|---------------------|-----------|
| **Cologne** (Köln) | Prussia 1815 (annexed by France 1794) | **Represent as republic** (separate from Electorate of Cologne) | Major Rhineland trading city; annexed by France 1794, to Prussia 1815 |
| **Nürnberg** (Nuremberg) | Bavaria 1806 | **Represent as republic** | Major cultural/artistic center; Bavaria absorbed 1806 |
| **Augsburg** | Bavaria 1806 | **Represent as republic** | Mixed Catholic-Protestant (*Paritätische Reichsstadt*); banking (Fugger), textiles |
| **Regensburg** | Bavaria 1810 | **Represent as republic** | Seat of perpetual Reichstag; Bavaria absorbed 1810 |
| **Ulm** | Bavaria 1803 → Württemberg 1810 | **Fold into Württemberg's 1815 provinces** | Textile center |
| **Aachen** (Aix-la-Chapelle) | Prussia 1815 (annexed by France 1794) | **Fold into Prussia's 1815 Rhineland provinces** | Imperial coronation city |
| *(All others)* | Various | **Fold into 1815 absorbers** | 45 free cities mediatized 1803-1806 |

**Proposed new free-city tags** (republic government):
- **KOL** (Cologne free city, distinct from KLN Electorate) — ✓ CHECK IF FREE
- **NUE** (Nürnberg) — ✓ CHECK IF FREE
- **AUB** (Augsburg free city, distinct from AUG Prince-Bishopric) — ✓ CHECK IF FREE
- **REB** (Regensburg free city, distinct from REG Prince-Bishopric) — ✓ CHECK IF FREE

**Tag collision check needed**:

```bash
for tag in KOL NUE AUB REB; do
  grep -q "^${tag} =" /path/to/countries.txt && echo "$tag TAKEN" || echo "$tag FREE"
done
```

**TO BUILD** (if free cities represented as separate tags):
- 4 new country files in `setup/countries/c_europe/` (cologne_city.txt, nurnberg.txt, augsburg_city.txt, regensburg_city.txt)
- Add 4 entries to countries.txt
- Province ownership for city provinces (Cologne city, Nürnberg city, Augsburg city, Regensburg city)
- Government type = `republic` (oligarchic city-state)

**ALTERNATIVE**: Fold these 4 cities into their 1815 absorbers (simpler). **Recommend this** unless user wants maximum 1763 authenticity.

---

## SECTION C: PROVINCE MOVES (Territory Reassignments)

### C1. Silesia — PRUSSIAN in 1763 (Confirmed by Treaty of Hubertusburg)

**Research finding** (lines 151-159 of research doc):
> **Status quo ante bellum** in Germany:
> - **Prussia retains Silesia** — the core objective secured by Frederick II; Prussian sovereignty over Silesia confirmed. This is the **critical outcome**: Prussia has successfully defended its 1740s conquest and is now recognized as a European great power.

**1815 status**: Silesia = Prussian (PRU)  
**1763 status**: Silesia = Prussian (PRU) — **NO CHANGE NEEDED** (already Prussian in 1815 baseline)

**Areas to verify** (grep from areas.txt):
- `Niederschlesien` (Lower Silesia) — line 2998-3014
- `Oberschlesien` (Upper Silesia) — line 7116-7129

**Action**: Verify in `setup/main/province_setup.csv` that all Silesian provinces are owned by PRU in 1815 baseline. **NO CHANGES NEEDED** if already Prussian.

### C2. Poland-Lithuania Commonwealth — Pre-1772 Partition Borders

**Research finding** (lines 122-144 table, lines 127-128):
> | **Poland** (Polish-Lithuanian Commonwealth) | Augustus III (also Elector of Saxony, r. 1733-1763) | **Personal union with Saxony**; pre-1772 partition borders |
> | **Lithuania** | Royal union junior partner of Poland | **Commonwealth structure** (pre-partition) |

**1815 reality**: Poland partitioned 1772/1793/1795; does not exist as independent state until 1815 Congress Kingdom (Russian client)  
**1763 reality**: Polish-Lithuanian Commonwealth intact; borders extend to: East Prussia (border), Black Sea coast (Podolia), Right-bank Ukraine, Belarus, Lithuania, Courland, Livonia

**Provinces to restore to POL** (from areas.txt analysis):
- **Grodno** area (line 196-212) — 1815 = Russian, 1763 = Polish
- **Augustowskie** area (line 473-483) — 1815 = Russian, 1763 = Polish
- **Kowno** area (line 2581-2598) — 1815 = Russian, 1763 = Polish
- **Minsk** area (line 1868-1904) — 1815 = Russian, 1763 = Polish
- **Vitebsk** area (line 7386-7414) — 1815 = Russian, 1763 = Polish
- **Podlaskie** area (line 6101-6107) — 1815 = Russian, 1763 = Polish
- **Plockie** area (line 7472-7481) — 1815 = Prussia/Russia?, 1763 = Polish
- *Others* — Right-bank Ukraine, Volhynia, Podolia (if represented)

**Provinces to assign to LIT** (Grand Duchy):
- **Kowno** area capital
- Courland/Livonia influence (but Courland = separate duchy, vassal of Poland)

**Action**:
1. Update `setup/main/province_setup.csv`: change owner of restored provinces from RUS/PRU → POL
2. Update `setup/main/00_default.txt`: 
   - POL ruler = Augustus III (also SAX ruler)
   - LIT = royal_union junior partner of POL
   - Establish POL-SAX personal union (Augustus III holds both thrones)

### C3. Saxony — War Devastation + Polish Crown

**1763 status**: Augustus III (Elector of Saxony) also King of Poland (r. 1733-1763). Dies **5 October 1763** (8 months after start date).

**Action**:
- Update SAX ruler in `00_default.txt`: Friedrich August II (Augustus III)
- Add personal_union relationship SAX ↔ POL
- Add event trigger for Augustus III's death (5 Oct 1763) → succession crisis in Poland + Saxony

### C4. Hungary, Transylvania, Croatia — Habsburg Hereditary Lands

**1815 status**: HUN, TRS, CRO = separate tags but under Habsburg rule  
**1763 status**: Same (part of Maria Theresa's hereditary lands)

**Action**: 
- Verify HUN, TRS, CRO rulers in `00_default.txt` = Maria Theresa (or Habsburg governance)
- Verify subject relationships (if any) to AUS

### C5. Ecclesiastical Territories — Restore from 1815 Absorbers

**For each new ecclesiastical state tag (MNZ, KLN, TRR, SZG, WUE, BAM, MUN, PDB, OSN, HLD, AUG, FRS, PAS, REG, SPY, WRM, KST, BAS, STB, TRN, BRX, FUL)**:

1. Identify capital province (from areas.txt + research doc)
2. Identify surrounding provinces historically belonging to that prince-bishopric
3. Update `setup/main/province_setup.csv`: change owner from 1815 absorber (BAV, PRU, HAN, BAD, etc.) → ecclesiastical tag

**Example: Salzburg (SZG)**
- Capital area: **Salzburg** (line 6852 in areas.txt)
- Historically: archbishopric ruled territory around Salzburg city + parts of modern Salzburg state
- 1815 absorber: Bavaria 1803, Austria 1816
- **Action**: Change provinces in Salzburg area from AUS → SZG in province_setup.csv

**Cross-reference for each ecclesiastical state**:
- Research doc Section I lists major prince-bishoprics (lines 60-90)
- Research doc Section IV.B lists 1803 absorbers (lines 228-248)
- Areas.txt lines 6852 (Salzburg), etc. — use area names to identify provinces

**TO BUILD**: 
- Spreadsheet mapping: ecclesiastical tag → capital area → provinces → 1815 absorber
- Province ownership changes in `province_setup.csv`

---

## SECTION D: RULERS (Dynasty & Character Changes for 1763)

### D1. The Eight Electors (1763)

From research doc Section I table (lines 122-144):

| **State Tag** | **1763 Ruler** | **Title** | **House/Dynasty** | **Reign** | **Notes** |
|---------------|----------------|-----------|-------------------|-----------|-----------|
| **MNZ** (new) | Emmerich Joseph von Breidbach zu Bürresheim | Archbishop-Elector of Mainz | — | 1763-1774 | Imperial Archchancellor for Germany; appointed **Feb 1763** |
| **TRR** (new) | Johann IX Philipp von Walderdorff | Archbishop-Elector of Trier | — | 1756-1768 | Imperial Archchancellor for Burgundy |
| **KLN** (new) | Maximilian Friedrich von Königsegg-Rothenfels | Archbishop-Elector of Cologne | — | 1761-1784 | Imperial Archchancellor for Italy; also ruled Münster |
| **AUS** (Bohemia crown) | Maria Theresa | Queen of Bohemia; Archduchess of Austria | Habsburg | 1740-1780 | Francis I as consort (Emperor) |
| *(Palatinate — need tag)* | Karl IV Theodor | Elector Palatine | Wittelsbach (Sulzbach) | 1742-1799 | Also ruled Jülich-Berg |
| **SAX** | Friedrich August II (Augustus III) | Elector of Saxony; King of Poland | Wettin (Albertine) | 1733-1763 | **Dies 5 Oct 1763** |
| **PRU** | Frederick II (the Great) | King in Prussia, Elector of Brandenburg | Hohenzollern | 1740-1786 | Same as 1815 |
| **HAN** | George III | Elector of Hanover; King of Great Britain | Hanover | 1760-1820 | Same as 1815 |

**TO BUILD**:
- Character definitions in `setup/main/00_default.txt` for all 8 Electors
- Ruler assignments in country files
- Event for Augustus III's death (5 Oct 1763)

### D2. Major Secular Rulers (From research doc table)

| **State Tag** | **1763 Ruler** | **Title** | **House** | **Reign** | **Notes** |
|---------------|----------------|-----------|-----------|-----------|-----------|
| **BAV** | Maximilian III Joseph | Elector of Bavaria | Wittelsbach | 1745-1777 | Same as 1815 |
| **WUR** | Karl I Eugen | Duke of Württemberg | Württemberg | 1737-1793 | Same as 1815 |
| **HSK** | Friedrich II | Landgrave of Hesse-Kassel | Hesse | 1760-1785 | Same as 1815 |
| **HSD** | Ludwig VIII | Landgrave of Hesse-Darmstadt | Hesse | 1739-1768 | **Change from 1815** (Ludwig IX ruled 1768-1790) |
| **BAD** | Karl Friedrich | Margrave of Baden-Durlach | Zähringen | 1746-1811 | Same as 1815 |
| **MKS** | Friedrich II | Duke of Mecklenburg-Schwerin | Mecklenburg | 1756-1785 | Same as 1815 |
| **MKZ** | Adolf Friedrich IV | Duke of Mecklenburg-Strelitz | Mecklenburg | 1752-1794 | Same as 1815 |
| **BRG** | Karl I | Duke of Brunswick-Wolfenbüttel | Welf | 1735-1780 | Same as 1815 |
| **NAS** | *(Multiple rulers — Nassau-Usingen, Nassau-Weilburg, etc.)* | Various princes | Nassau | Various | Consolidated 1806 |
| **ANH** | *(Multiple rulers — Anhalt-Dessau, -Bernburg, -Köthen, -Zerbst)* | Various princes | Anhalt | Various | Consolidated 1863 |
| **HUN** | Maria Theresa | Queen of Hungary | Habsburg | 1740-1780 | Same as AUS |

**TO BUILD**:
- Update `00_default.txt` character definitions
- Cross-reference with 1815 baseline; change where needed (e.g., HSD ruler)

### D3. Prince-Bishops (All 18 New Ecclesiastical States)

From research doc Section I (lines 60-90):

| **Tag** | **1763 Prince-Bishop** | **Reign** | **Notes** |
|---------|------------------------|-----------|-----------|
| **SZG** | Sigismund III von Schrattenbach | 1753-1771 | Patron of Mozart family |
| **WUE** | Adam Friedrich von Seinsheim | 1755-1779 | Also held Bamberg |
| **BAM** | Adam Friedrich von Seinsheim | 1757-1779 | Also held Würzburg |
| **MUN** | Maximilian Friedrich von Königsegg-Rothenfels | 1761-1784 | Also Elector of Cologne |
| **PDB** | Wilhelm Anton von Asseburg | 1763-1782 | **Just took office 1763** |
| **OSN** | Clemens August of Bavaria | 1728-1764 | **Dies 1764** (next year) |
| **HLD** | Friedrich Wilhelm von Westphalen | 1763-1789 | **Just appointed 1763** |
| **AUG** | Joseph Ignaz Philipp von Hessen-Darmstadt | 1740-1768 | |
| **FRS** | Johann Theodor | 1727-1763 | **Dies 1763** (this year) |
| **PAS** | Joseph Maria von Thun und Hohenstein | 1761-1763 | **Dies 1763** (this year) |
| **REG** | Clemens Wenzeslaus of Saxony | 1763-1769 | **Just appointed 1763** |
| **SPY** | Franz Christoph von Hutten zum Stolzenberg | 1743-1770 | |
| **WRM** | *(Held with Konstanz)* | — | |
| **KST** | Franz Konrad von Rodt | 1750-1775 | |
| **BAS** | Simon Nicolas de Montjoie | 1762-1775 | **Just took office 1762** |
| **STB** | Louis Constantin de Rohan-Guéméné | 1756-1779 | French influence |
| **TRN** | Cristoforo Sizzo de Noris | 1748-1763 | **Dies 1763** (this year) |
| **BRX** | Leopold Maria Joseph von Spaur | 1747-1778 | |
| **FUL** | Heinrich VIII von Bibra | 1759-1788 | Also Prince-Abbot |

**TO BUILD**:
- 18 character definitions in `00_default.txt`
- Events for deaths occurring in 1763 (FRS, PAS, TRN)
- Appointments for new bishops (PDB, HLD, REG, BAS all took office 1762-1763)

### D4. Free City Governments (If Represented)

If Cologne, Nürnberg, Augsburg, Regensburg represented as separate republic tags:
- **Government type**: `republic` (oligarchic city council)
- **No dynastic ruler** — city councils (Stadtrat, Rat)
- **TO BUILD**: Council character definitions (if mechanics require)

---

## SECTION E: SUBJECT/DEPENDENCY CHANGES

### E1. Poland-Lithuania Commonwealth (Royal Union)

**Structure**:
- **POL** (Poland) = senior partner
- **LIT** (Grand Duchy of Lithuania) = junior partner
- **Relationship type**: `royal_union` (personal union of crowns)
- **Ruler**: Augustus III (also Elector of Saxony)

**TO BUILD**:
- Update `00_default.txt`: 
  - POL subject = LIT (royal_union)
  - POL ruler = Augustus III (also SAX ruler)
- Subject interaction mechanics (already implemented in 1815 baseline)

### E2. Saxony-Poland Personal Union

**Structure**:
- SAX Elector = Augustus III
- POL King = Augustus III (same person)
- **NOT a subject relationship** — personal union of two separate thrones

**TO BUILD**:
- Character definition: Augustus III holds both titles
- Event for death (5 Oct 1763) → succession crisis (Poland elective, Saxony hereditary)

### E3. Hanover-Britain Personal Union

**Structure**:
- HAN Elector = George III
- GBR King = George III (same person)
- **NOT a subject relationship** — personal union

**TO BUILD**:
- Already implemented in 1815 baseline (verify)

### E4. Habsburg Composite Monarchy

**Structure**:
- AUS (Archduchy of Austria)
- HUN (Kingdom of Hungary) — under Habsburg rule
- Bohemia (crown lands) — under Habsburg rule (represented by AUS Bohemia areas)
- TRS (Transylvania) — under Habsburg rule
- CRO (Croatia) — under Habsburg rule
- Lombardy (LBV or MIL in 1815?) — under Habsburg rule 1763

**Relationship type**: Not clear if represented as subjects or integrated into AUS tag. Verify 1815 baseline structure.

**TO BUILD**:
- Verify HUN, TRS, CRO rulers = Maria Theresa
- Verify subject relationships (if any) to AUS

### E5. Ecclesiastical States — Imperial Immediacy

**Structure**: All ecclesiastical states (Electorates, prince-bishoprics) are **reichsunmittelbar** (immediate to the Empire) — they owe allegiance directly to the Emperor, not to any intermediate overlord.

**Representation in mod**:
- **NOT subjects** of AUS or any other power
- **Independent** but within HRE framework
- Emperor = Francis I (husband of Maria Theresa) — but Emperor has no direct sovereignty over member states (weak suzerain)

**TO BUILD**:
- Verify ecclesiastical states have no overlord in `00_default.txt`
- Consider adding HRE membership flag/variable (if HRE mechanics implemented)

---

## SECTION F: DOCUMENTED LIMITATIONS (What's NOT Implemented)

### F1. Minor Principalities — Folded into 1815 Absorbers

The following 1763 states are **NOT represented** as separate tags; their provinces remain part of their 1815 absorber:

**Mediatized Secular Principalities**:
- **Hohenlohe** lines → folded into Württemberg/Bavaria 1815 provinces
- **Solms**, **Isenburg**, **Wied**, **Salm** → folded into Nassau/Hesse/Bavaria 1815 provinces
- **Löwenstein-Wertheim** → folded into Bavaria/Baden 1815 provinces
- **Reuss** (elder + younger lines) → folded into Saxony/Thuringia 1815 provinces
- **Schwarzburg** (Sondershausen, Rudolstadt) → folded into Saxony/Thuringia 1815 provinces
- **Waldeck** → folded into Prussia/Hesse 1815 provinces (or represent as WDK if tag exists)
- **Schaumburg-Lippe** → folded into Hanover 1815 provinces
- **Lippe** → folded into Prussia 1815 provinces
- Dozens of **imperial knights** (*Reichsritter*) with tiny estates → all folded

**Mediatized Free Cities** (45 of 51):
- **Aachen**, **Ulm**, **Wetzlar**, **Worms**, **Speyer**, **Mühlhausen**, **Nordhausen**, **Goslar**, **Rottweil**, **Esslingen**, **Heilbronn**, **Reutlingen**, **Schwäbisch Gmünd**, **Schwäbisch Hall**, **Kaufbeuren**, **Kempten**, **Lindau**, **Memmingen**, **Ravensburg**, **Rothenburg ob der Tauber**, **Windsheim**, **Dinkelsbühl**, **Wangen** → all folded into 1815 absorbers (Bavaria, Württemberg, Baden, Prussia)

**Prince-Abbacies**:
- **Kempten**, **Berchtesgaden**, **Corvey**, **Weingarten**, **Salem**, **St. Gall**, **Reichenau**, many others → all folded

**Rationale**: 
- 200+ minor states = impractical to represent individually
- Gameplay impact minimal (tiny populations, negligible military/economic weight)
- Focus on **playable/visible** states: the 8 Electors + major prince-bishoprics + largest free cities + major secular states = ~40 tags total

### F2. Subdivisions Within Represented States

**Nassau**: Historically subdivided into Nassau-Usingen, Nassau-Weilburg, Nassau-Saarbrücken, Nassau-Dietz in 1763. **Represented as single NAS tag** for simplicity.

**Anhalt**: Historically subdivided into Anhalt-Dessau, Anhalt-Bernburg, Anhalt-Köthen, Anhalt-Zerbst in 1763. **Represented as single ANH tag** for simplicity.

**Baden**: Historically subdivided into Baden-Durlach and Baden-Baden until 1771. **Represented as single BAD tag** (Baden-Durlach absorbs Baden-Baden 1771, just 8 years after start).

### F3. Imperial Institutions — Not Mechanically Implemented

The HRE had complex institutional machinery in 1763:
- **Reichstag** (Imperial Diet) at Regensburg — permanent assembly
- **Reichskammergericht** (Imperial Chamber Court) at Wetzlar
- **Reichshofrat** (Aulic Council) at Vienna
- **Electoral College** (8 Electors)
- **Princely College** (~100 princes)
- **Imperial Cities College** (~51 cities)

**Implementation**: These institutions are **NOT mechanically represented** (no imperial diet votes, no imperial court cases, no formal HRE mechanics). The HRE exists as **flavor** (member states are independent but within nominal imperial framework).

**Rationale**: Imperator: Rome engine does not have built-in HRE mechanics. Implementing functional Reichstag/court systems would require extensive custom scripting beyond scope of 1763 conversion.

### F4. Economic Features — Generic Placeholder

The research doc (Section V) details rich economic specificity for 1763:
- **Saxony**: silver mining (Erzgebirge), Meissen porcelain, linen textiles, Leipzig fairs
- **Bohemia**: glass (Bohemian crystal), linen, brewing
- **Silesia**: linen (Europe's leading producer)
- **Switzerland**: watchmaking (Geneva), silk ribbons (Basel), mercenaries
- **Rhineland**: wine (Rhine/Mosel), trade (Frankfurt, Cologne)
- **Bavaria**: beer, salt mining (Reichenhall), crafts

**Implementation**: These economic features are represented via:
- **Trade goods** (already in 1815 baseline: silk, wine, porcelain, glass, etc.)
- **Buildings** (mines, manufactories, etc.)
- **Province modifiers** (economic bonuses)

**NOT implemented**: Detailed per-province economic modeling of every specific 1763 industry. Use **generic approximations** (Saxony provinces get silver/porcelain, Switzerland gets watch trade goods, Rhine gets wine, etc.).

---

## SECTION G: IMPLEMENTATION CHECKLIST

### G1. Tag Creation

**Step 1**: Verify proposed tags are free (already done above — all except EIC, KON, LIE confirmed free; use alternatives AUG, KST, LIE).

**Step 2**: Create country files:
- [ ] `setup/countries/c_europe/mainz.txt` (MNZ)
- [ ] `setup/countries/c_europe/cologne.txt` (KLN)
- [ ] `setup/countries/c_europe/trier.txt` (TRR)
- [ ] `setup/countries/c_europe/salzburg.txt` (SZG)
- [ ] `setup/countries/c_europe/wurzburg.txt` (WUE)
- [ ] `setup/countries/c_europe/bamberg.txt` (BAM)
- [ ] `setup/countries/c_europe/munster.txt` (MUN)
- [ ] `setup/countries/c_europe/paderborn.txt` (PDB)
- [ ] `setup/countries/c_europe/osnabruck.txt` (OSN)
- [ ] `setup/countries/c_europe/hildesheim.txt` (HLD)
- [ ] `setup/countries/c_europe/augsburg_bp.txt` (AUG — prince-bishopric)
- [ ] `setup/countries/c_europe/freising.txt` (FRS)
- [ ] `setup/countries/c_europe/passau.txt` (PAS)
- [ ] `setup/countries/c_europe/regensburg_bp.txt` (REG — prince-bishopric)
- [ ] `setup/countries/c_europe/speyer.txt` (SPY)
- [ ] `setup/countries/c_europe/worms.txt` (WRM)
- [ ] `setup/countries/c_europe/konstanz.txt` (KST)
- [ ] `setup/countries/c_europe/basel.txt` (BAS)
- [ ] `setup/countries/c_europe/strasbourg.txt` (STB)
- [ ] `setup/countries/c_europe/trent.txt` (TRN)
- [ ] `setup/countries/c_europe/brixen.txt` (BRX)
- [ ] `setup/countries/c_europe/fulda.txt` (FUL)
- [ ] *(Optional)* Free city files: cologne_city.txt (KOL), nurnberg.txt (NUE), augsburg_city.txt (AUB), regensburg_city.txt (REB)

**Step 3**: Add entries to `setup/countries/countries.txt` (after line 57, Central Europe block):

```
# Ecclesiastical Electorates (1763)
MNZ = "setup/countries/c_europe/mainz.txt"
KLN = "setup/countries/c_europe/cologne.txt"
TRR = "setup/countries/c_europe/trier.txt"

# Major Prince-Bishoprics (1763)
SZG = "setup/countries/c_europe/salzburg.txt"
WUE = "setup/countries/c_europe/wurzburg.txt"
BAM = "setup/countries/c_europe/bamberg.txt"
MUN = "setup/countries/c_europe/munster.txt"
PDB = "setup/countries/c_europe/paderborn.txt"
OSN = "setup/countries/c_europe/osnabruck.txt"
HLD = "setup/countries/c_europe/hildesheim.txt"
AUG = "setup/countries/c_europe/augsburg_bp.txt"
FRS = "setup/countries/c_europe/freising.txt"
PAS = "setup/countries/c_europe/passau.txt"
REG = "setup/countries/c_europe/regensburg_bp.txt"
SPY = "setup/countries/c_europe/speyer.txt"
WRM = "setup/countries/c_europe/worms.txt"
KST = "setup/countries/c_europe/konstanz.txt"
BAS = "setup/countries/c_europe/basel.txt"
STB = "setup/countries/c_europe/strasbourg.txt"
TRN = "setup/countries/c_europe/trent.txt"
BRX = "setup/countries/c_europe/brixen.txt"
FUL = "setup/countries/c_europe/fulda.txt"

# Free Cities (1763, optional)
# KOL = "setup/countries/c_europe/cologne_city.txt"
# NUE = "setup/countries/c_europe/nurnberg.txt"
# AUB = "setup/countries/c_europe/augsburg_city.txt"
# REB = "setup/countries/c_europe/regensburg_city.txt"
```

### G2. Character Definitions

**Step 1**: Add 18 prince-bishop characters to `setup/main/00_default.txt`:
- Emmerich Joseph von Breidbach (MNZ)
- Johann IX Philipp von Walderdorff (TRR)
- Maximilian Friedrich von Königsegg-Rothenfels (KLN, also MUN)
- Sigismund III von Schrattenbach (SZG)
- Adam Friedrich von Seinsheim (WUE + BAM)
- Wilhelm Anton von Asseburg (PDB)
- Clemens August of Bavaria (OSN)
- Friedrich Wilhelm von Westphalen (HLD)
- Joseph Ignaz Philipp von Hessen-Darmstadt (AUG)
- Johann Theodor (FRS)
- Joseph Maria von Thun und Hohenstein (PAS)
- Clemens Wenzeslaus of Saxony (REG)
- Franz Christoph von Hutten zum Stolzenberg (SPY)
- Franz Konrad von Rodt (KST)
- Simon Nicolas de Montjoie (BAS)
- Louis Constantin de Rohan-Guéméné (STB)
- Cristoforo Sizzo de Noris (TRN)
- Leopold Maria Joseph von Spaur (BRX)
- Heinrich VIII von Bibra (FUL)

**Format** (example for Mainz):
```
char:1000 = {
    first_name = "Emmerich Joseph"
    dynasty = 0  # Ecclesiastical ruler, no dynasty
    birth_date = 1707.1.12
    culture = german
    religion = catholic
    # Prince-bishops were elected, not hereditary
}
```

**Step 2**: Update existing rulers (if different from 1815):
- [ ] HSD: Ludwig VIII (r. 1739-1768) — change from 1815 Ludwig IX
- [ ] SAX: Friedrich August II (Augustus III, also POL king) — dies 5 Oct 1763
- [ ] POL: Augustus III (same as SAX)

**Step 3**: Add personal union relationships:
- SAX ruler = Augustus III (char:XXX)
- POL ruler = Augustus III (char:XXX) — same character

### G3. Province Ownership Changes

**Step 1**: Create province mapping spreadsheet (ecclesiastical states):

| **Tag** | **Capital Area** | **Provinces to Transfer** | **From (1815 Owner)** |
|---------|------------------|---------------------------|----------------------|
| MNZ | Mainz area | [list province IDs] | [1815 owner] |
| KLN | Cologne area | [list province IDs] | [1815 owner] |
| TRR | Trier area | [list province IDs] | [1815 owner] |
| SZG | Salzburg | [list province IDs from Salzburg area] | AUS (or BAV?) |
| ... | ... | ... | ... |

**Step 2**: Update `setup/main/province_setup.csv`:
- Change `owner` column for all transferred provinces
- Example: `province_id,owner,culture,religion,...`
  - `12345,SZG,south_german,catholic,...` (was AUS)

**Step 3**: Poland-Lithuania border restoration:
- Transfer provinces in Grodno, Augustowskie, Kowno, Minsk, Vitebsk, Podlaskie, Plockie areas from RUS/PRU → POL
- Update `province_setup.csv`

**Step 4**: Verify Silesia = PRU (should already be correct in 1815 baseline)

### G4. Subject Relationships

**Step 1**: Update `setup/main/00_default.txt` subject relationships:
- [ ] POL overlord of LIT (royal_union)
- [ ] Verify HUN, TRS, CRO relationships to AUS (if subjects)
- [ ] Remove any subject relationships for ecclesiastical states (they are independent)

**Step 2**: Personal unions (character-level, not subject relationships):
- SAX-POL: Augustus III holds both thrones (same character)
- HAN-GBR: George III holds both thrones (already in 1815 baseline)

### G5. Events

**Step 1**: Augustus III death event (5 Oct 1763):
- Trigger: date = 1763.10.5
- Effect: SAX ruler dies → succession to Friedrich Christian (rules 74 days, dies 17 Dec 1763) → Friedrich August III (minor, regency)
- Effect: POL succession crisis (elective throne) → Stanisław August Poniatowski elected 1764 (Russian influence)

**Step 2**: Prince-bishop deaths (1763):
- FRS: Johann Theodor dies 1763 → succession
- PAS: Joseph Maria von Thun und Hohenstein dies 1763 → succession
- TRN: Cristoforo Sizzo de Noris dies 1763 → succession

**Step 3**: Ecclesiastical elections:
- PDB: Wilhelm Anton von Asseburg just appointed 1763
- HLD: Friedrich Wilhelm von Westphalen just appointed 1763
- REG: Clemens Wenzeslaus just appointed 1763
- BAS: Simon Nicolas de Montjoie just appointed 1762

### G6. Government Types

**Step 1**: Ecclesiastical states government:
- Set government type = `theocracy` (or closest equivalent in Imperator: Rome)
- Verify inheritance mechanics (ecclesiastical states = elective, not hereditary)

**Step 2**: Free cities government (if represented):
- Set government type = `republic` (oligarchic city council)

### G7. Cultures & Religions

**Step 1**: Verify culture assignments:
- All German states (secular + ecclesiastical): `german` or `south_german` or `north_german` (check `/common/cultures/` for exact keys)
- Switzerland: `swiss_german`
- Italian border states (TRN, BRX): `german` or `italian` (mixed)

**Step 2**: Verify religion assignments:
- All ecclesiastical states: `catholic`
- Secular states: `catholic` (Bavaria, Austria), `protestant` (Prussia, Saxony, Hanover), `reformed` (Palatinate?, Switzerland), mixed (Württemberg, Baden)

### G8. Localization

**Step 1**: Add localization keys for all 22 new tags:
- `MNZ` → "Mainz" (English), "Mayence" (French), "Mainz" (German)
- `KLN` → "Cologne" (English), "Cologne" (French), "Köln" (German)
- ... (all 22 tags)

**Step 2**: Add localization for ruler titles:
- "Archbishop-Elector of Mainz"
- "Prince-Bishop of Salzburg"
- etc.

**Step 3**: Add localization for events (Augustus III death, etc.)

### G9. Testing & Boot Verification

**Step 1**: Boot test with all new tags:
- [ ] Boot game to 1763.02.16 start date
- [ ] Verify all 22 new ecclesiastical tags appear on map
- [ ] Verify borders (Poland-Lithuania restored, ecclesiastical territories carved out)
- [ ] Verify rulers (all 18 prince-bishops + secular rulers)

**Step 2**: Crash debugging:
- Check error.log for any create_country failures
- Check province ownership (any orphaned provinces?)
- Check character definitions (any missing rulers?)

**Step 3**: Playability test:
- [ ] Play as PRU (Prussia) — verify Silesia owned
- [ ] Play as POL (Poland) — verify pre-partition borders, LIT junior partner
- [ ] Play as MNZ (Mainz) — verify ecclesiastical state functions
- [ ] Play as SZG (Salzburg) — verify territory, ruler, mechanics

### G10. Commit & Documentation

**Step 1**: Commit message (as freekumquats):
```
1763 Phase 2: Central Europe / HRE ecclesiastical states + Poland-Lithuania restoration

- Add 22 new ecclesiastical state tags (3 Electorates + 18 prince-bishoprics + 1 prince-abbacy)
  MNZ (Mainz), KLN (Cologne), TRR (Trier), SZG (Salzburg), WUE (Würzburg), BAM (Bamberg),
  MUN (Münster), PDB (Paderborn), OSN (Osnabrück), HLD (Hildesheim), AUG (Augsburg),
  FRS (Freising), PAS (Passau), REG (Regensburg), SPY (Speyer), WRM (Worms), KST (Konstanz),
  BAS (Basel), STB (Strasbourg), TRN (Trent), BRX (Brixen), FUL (Fulda)
- Restore Poland-Lithuania Commonwealth pre-1772 partition borders (POL overlord of LIT)
- Update SAX-POL personal union (Augustus III holds both thrones, dies 5 Oct 1763)
- Province ownership: transfer ecclesiastical territories from 1815 absorbers back to 1763 states
- Character definitions: 18 prince-bishops + updated secular rulers (HSD Ludwig VIII)
- Events: Augustus III death (5 Oct 1763), prince-bishop successions
- Documented limitations: 200+ minor states folded into 1815 absorbers (see research/1763_DELTA_CEurope_HRE.md)

Task: #237 (Phase 2 region: C.Europe/HRE 1763 delta)
Research: research/1763_WORLD_CEurope_HRE.md (sourced EN+DE academic history)
```

**Step 2**: Update SESSION_REPORT.md:
- Document all 22 new tags
- Document province ownership changes
- Document ruler changes
- Document documented limitations (what's NOT implemented)

**Step 3**: Tag task #237 as completed

---

## SECTION H: FILE TARGETS (Line-by-Line Edit Locations)

### H1. `setup/countries/countries.txt`

**Location**: After line 57 (after `CRO = "setup/countries/c_europe/croatia.txt"`)

**Insert**:
```
# Ecclesiastical Electorates (1763)
MNZ = "setup/countries/c_europe/mainz.txt"
KLN = "setup/countries/c_europe/cologne.txt"
TRR = "setup/countries/c_europe/trier.txt"

# Major Prince-Bishoprics (1763)
SZG = "setup/countries/c_europe/salzburg.txt"
WUE = "setup/countries/c_europe/wurzburg.txt"
BAM = "setup/countries/c_europe/bamberg.txt"
MUN = "setup/countries/c_europe/munster.txt"
PDB = "setup/countries/c_europe/paderborn.txt"
OSN = "setup/countries/c_europe/osnabruck.txt"
HLD = "setup/countries/c_europe/hildesheim.txt"
AUG = "setup/countries/c_europe/augsburg_bp.txt"
FRS = "setup/countries/c_europe/freising.txt"
PAS = "setup/countries/c_europe/passau.txt"
REG = "setup/countries/c_europe/regensburg_bp.txt"
SPY = "setup/countries/c_europe/speyer.txt"
WRM = "setup/countries/c_europe/worms.txt"
KST = "setup/countries/c_europe/konstanz.txt"
BAS = "setup/countries/c_europe/basel.txt"
STB = "setup/countries/c_europe/strasbourg.txt"
TRN = "setup/countries/c_europe/trent.txt"
BRX = "setup/countries/c_europe/brixen.txt"
FUL = "setup/countries/c_europe/fulda.txt"
```

### H2. `setup/main/00_default.txt`

**Location**: Character definitions section (find existing character blocks, add after)

**Insert**: 22 new character definitions (see G2 above for format)

**Location**: Country ruler assignments section (find `c:SAX = { ... }` blocks)

**Edit**: Update SAX, POL, HSD rulers; add new ecclesiastical state rulers

**Location**: Subject relationships section (find `overlord = ...` blocks)

**Edit**: Add `c:POL = { overlord = c:LIT subject_type = royal_union }`

### H3. `setup/main/province_setup.csv`

**Location**: Province ownership column (column 2?)

**Edit**: Change owner for provinces transferred to ecclesiastical states (see G3 mapping spreadsheet)

**Edit**: Change owner for Poland-Lithuania restoration (RUS/PRU → POL for Grodno, Minsk, etc. provinces)

### H4. New Country Files (22 files)

**Create**: 22 new `.txt` files in `setup/countries/c_europe/`:
- mainz.txt, cologne.txt, trier.txt, salzburg.txt, wurzburg.txt, bamberg.txt, munster.txt, paderborn.txt, osnabruck.txt, hildesheim.txt, augsburg_bp.txt, freising.txt, passau.txt, regensburg_bp.txt, speyer.txt, worms.txt, konstanz.txt, basel.txt, strasbourg.txt, trent.txt, brixen.txt, fulda.txt

**Format** (example `mainz.txt`):
```
color = { 230 30 30 }  # Red (ecclesiastical)
culture = german
religion = catholic
capital = [capital province ID]
government = theocracy  # Or closest equivalent

# Historical setup
# Electorate & Archbishopric of Mainz
# Imperial Archchancellor for Germany
# Emmerich Joseph von Breidbach zu Bürresheim (1763-1774)
```

### H5. Localization Files

**Location**: `/localization/english/` (or wherever country names are localized)

**Insert**: 22 new tag localizations (MNZ, KLN, TRR, SZG, WUE, BAM, MUN, PDB, OSN, HLD, AUG, FRS, PAS, REG, SPY, WRM, KST, BAS, STB, TRN, BRX, FUL)

**Insert**: Ruler title localizations (Archbishop-Elector, Prince-Bishop, etc.)

### H6. Event Files (New)

**Create**: `events/1763_ce_succession.txt` (or similar)

**Content**: Events for:
- Augustus III death (5 Oct 1763)
- Prince-bishop deaths (FRS, PAS, TRN in 1763)
- Prince-bishop appointments (PDB, HLD, REG, BAS in 1762-1763)

---

## SECTION I: RESEARCH CROSS-REFERENCES

All historical claims in this DELTA are sourced from:

**Primary research document**: `/Users/alan.chiang/github.com/imp19c/research/1763_WORLD_CEurope_HRE.md`

### Key Research Findings Cross-Reference:

1. **HRE Structure** (Section I, lines 9-144):
   - 8 Electors (3 ecclesiastical) — lines 25-36
   - Major secular principalities — lines 38-54
   - Ecclesiastical principalities (prince-bishoprics) — lines 56-90
   - Imperial free cities — lines 92-116

2. **Seven Years' War Outcome** (Section III, lines 146-174):
   - Treaty of Hubertusburg (15 Feb 1763) — line 149
   - Prussia retains Silesia — lines 155-156
   - Saxony restored — line 158

3. **Rulers Table** (Section II, lines 122-144):
   - All 1763 rulers listed with reigns, houses, notes

4. **1763-1815 Transformation** (Section IV, lines 176-318):
   - Reichsdeputationshauptschluss 1803 — lines 183-200
   - HRE dissolution 1806 — lines 204-208
   - Secularized ecclesiastical states — lines 222-248
   - Mediatized free cities — lines 250-281

5. **Economy Section** (Section V, lines 320-518):
   - Regional economic specializations (Saxony silver/porcelain, Bohemian glass, Silesian linen, etc.)

6. **Sources** (Section VII, lines 552-592):
   - English-language academic sources (Clark, Ingrao, Wilson, etc.)
   - German-language sources (Aretin, Schilling, Vierhaus)

---

## SECTION J: ORACLE CONSULTATION REQUIREMENTS

Before implementing, **MUST consult Terra Indomita + Invictus oracles** (per standing rule `imp19c-oracle-consultation-rule.md`) for:

1. **Mass create_country at scale** (already done — Task #230 completed):
   - Oracle finding: Imperator: Rome engine CAN handle 40-50 new country tags (Terra Indomita mod has ~60 new countries)
   - Caveat: Performance impact if too many AI-controlled states; recommend AI disabling for minor ecclesiastical states if needed

2. **Theocracy government type**:
   - **UNPROVEN** capability: Does Imperator: Rome have a theocracy government type? Or must we use monarchy with flavor?
   - **ORACLE CONSULT NEEDED**: Check Terra Indomita + Invictus for ecclesiastical state representation

3. **Elective monarchy mechanics**:
   - Prince-bishops were elected by cathedral chapters (not hereditary)
   - **UNPROVEN** capability: Can we implement elective succession for ecclesiastical states?
   - **ORACLE CONSULT NEEDED**: Check Terra Indomita + Invictus for elective monarchy mechanics

4. **Personal union representation**:
   - SAX-POL: Augustus III holds both thrones
   - HAN-GBR: George III holds both thrones
   - **UNPROVEN** capability: How to represent personal unions? Same character holding two titles? Subject relationship?
   - **ORACLE CONSULT NEEDED**: Check Terra Indomita + Invictus for personal union mechanics

5. **HRE membership flag/variable**:
   - **UNPROVEN** capability: Can we tag states as "HRE members" for flavor/mechanics?
   - **ORACLE CONSULT NEEDED**: Check Terra Indomita + Invictus for HRE representation

**TO DO BEFORE IMPLEMENTATION**:
- [ ] Oracle consult: theocracy government type
- [ ] Oracle consult: elective monarchy mechanics
- [ ] Oracle consult: personal union representation
- [ ] Oracle consult: HRE membership mechanics

---

## SECTION K: SUMMARY

**Scope**: Central Europe / Holy Roman Empire 1763 conversion — the single largest European map change between 1763 and 1815.

**New tags required**: 22 (3 ecclesiastical Electorates + 18 prince-bishoprics + 1 prince-abbacy)

**Reused tags**: 25+ (Austria, Prussia, Bavaria, Saxony, Hanover, Württemberg, Hesses, Baden, Mecklenburgs, Brunswick, Hamburg, Bremen, Lübeck, Frankfurt, etc.)

**Province moves**: 
- Poland-Lithuania: Restore pre-1772 partition borders (Grodno, Minsk, Vitebsk, etc. from RUS → POL)
- Ecclesiastical territories: Transfer from 1815 absorbers (Bavaria, Prussia, Austria, Baden, etc.) back to 1763 ecclesiastical states
- Silesia: Already Prussian (no change)

**Ruler changes**: 18 prince-bishops + updated secular rulers (HSD, SAX-POL)

**Subject relationships**: POL overlord of LIT (royal_union); SAX-POL personal union (Augustus III)

**Documented limitations**: 200+ minor states folded into 1815 absorbers (not represented as separate tags)

**Implementation checklist**: 10 major steps (G1-G10 above)

**File targets**: 
- countries.txt (line 57 insert)
- 00_default.txt (character definitions + ruler assignments + subjects)
- province_setup.csv (ownership changes)
- 22 new country files
- localization files
- event files (Augustus III death, prince-bishop successions)

**Oracle consultation required**: Theocracy government type, elective monarchy, personal unions, HRE mechanics

**Commit target**: Task #237 (Phase 2 region: C.Europe/HRE 1763 delta)

---

**END OF DELTA PLAN**

---

**File**: `/Users/alan.chiang/github.com/imp19c/research/1763_DELTA_CEurope_HRE.md`  
**Date prepared**: 2026-07-08  
**Author**: Delta plan for Imperatrix: Victoria 1763 bookmark conversion  
**Target**: Convert 1815 baseline → 1763.02.16 (Central Europe / HRE only)  
**Research source**: `research/1763_WORLD_CEurope_HRE.md` (sourced EN+DE academic history)
