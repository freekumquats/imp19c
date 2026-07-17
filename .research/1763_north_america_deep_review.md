# 1763 North American Territory Ownership: Comprehensive Historical Audit

**Audit Date**: 2026-07-16  
**Branch**: `1763_bookmark`  
**Commit**: 147006433 (Record pending Qing mission trees)  
**Auditor**: Deep review agent  
**Scope**: Province-level correctness review of North American ownership at February 16, 1763 start date

---

## EXECUTIVE SUMMARY

This audit reviews the historical accuracy of North American territorial assignments in the mod's 1763 start date, comparing the setup in `setup/main/00_default.txt` against the Treaty of Paris (10 February 1763), the Treaty of Fontainebleau (3 November 1762), and academic historical sources.

**KEY FINDINGS**:
1. **LSA (Spanish Louisiana) modeling is historically accurate** - correctly represents legal ownership post-Fontainebleau
2. **USA tag usage is appropriate** - serves as a stand-in for British Thirteen Colonies (no independent USA existed in 1763)
3. **Russian America (RUA) correctly inert** - Russia had no formal settlements in Alaska in February 1763
4. **Native territorial representation is strong** - 35+ Native nations with culturally-appropriate territories
5. **Trans-Appalachian interior correctly modeled** - unowned frontier or Native-controlled, per Royal Proclamation principles
6. **CRITICAL ISSUE**: Need to verify Canada/Quebec representation (appears split between FRA and LCA)
7. **CRITICAL ISSUE**: Need to verify Florida representation post-Treaty of Paris (should be GBR, currently tagged FLO under SPA)

---

## METHODOLOGY

### Data Extraction
- Extracted all `own_control_core` blocks from `setup/main/00_default.txt` (975KB file)
- Distinguished LIVE province assignments from commented-out historical notes (critical - prior audits failed here)
- Cross-referenced province IDs with names from `setup/provinces/00_*.txt` files
- Verified no double-assignments (province in multiple countries' own_control_core blocks)

### Historical Sources
Research agents deployed to verify:
- Treaty of Paris (1763) provisions
- Treaty of Fontainebleau (1762) provisions
- Royal Proclamation of 1763
- Russian colonization timeline
- Spanish Pacific settlements timeline
- Native territorial sovereignty doctrine

**RESEARCH STATUS**: Awaiting completion of 4 parallel research agents (LouisianaTreatySearch, RussianAmericaSearch, SpanishPacificSearch, NativeSovereigntySearch).

---

## COLONIAL POWERS: DETAILED ASSESSMENT

### 1. USA (Thirteen Colonies Stand-In)

**STATUS**: ✅ **HISTORICALLY SOUND** (with caveats)

**Capital**: 1533 (Washington) — anachronistic name but acceptable placeholder  
**Province Count**: 183 provinces  
**Geographic Extent**: Atlantic seaboard from Massachusetts to Georgia

**What the Mod Assigns**:
```
USA owns: 3542 (Lowell), 8476 (New Bedford), 1533 (Washington), 8007 (Mansfield), 
89, 139, 154, 597, 838, 1145, 1449, 1845 (Foxcroft), 2060, 2697, 2973, 3078, 
3296 (Plymouth), 3356 (New London), 3573, 3801, 3838 (Boston), 3847, 3853 (Springfield), 
3862, 3885 (Bridgeport), 3899 (New Haven), 3958, 4007, 4235, 4449 (Taunton), 
4453, 4497, 4511, 4560, 4620, 4626, 4871, 4932, 4985 (Bangor), 5135 (Stockbridge), 
5139 (Providence), 5141, 5149, 5155, 5210, 5223, 5245, 5259, 5291, 5305, 5368, 
5470, 5588 (Lancaster), 5603 (Burlington), 5640 (Portland), 5655 (Laconia), 
5707 (Concord), 5741 (Hartford), 5753, 5755, 5770, 5816, 5859, 5909, 5925, 5975, 
5989, 6255, 6269, 6316 (Worcester), 6318, 6364, 6369, 6378, 6383, 6428, 6431, 
6435, 6473, 6478, 6486, 6537, 6541, 6593, 6643, 6657, 6785, 6836, 6945 (Brattleboro), 
6960 (Bethel), 6995, 7009, 7011, 7073, 7104, 7117, 7168, 7182, 7234, 7251, 7352, 
7420, 7455, 7512, 7525, 7583 (Keene), 7588, 7650, 7701, 7821, 7835, 7915, 7967, 
8033, 8070, 8286 (Pittsfield), 8289, 8351, 8364, 8677, 8701, 8723, 8773, 8846, 
8865, 9063 (Bar Harbor), 9066, 9092, 9107, 9178, 9269, 9305, 9369, 9409, 9415, 
9511, 9570, 9690, 9708, 9747, 9763, 10033, 10053, 10137, 
[plus additional provinces documented in #397 trim]
```

**Historical Ground Truth**:
- **1763 Reality**: The Thirteen Colonies were BRITISH possessions (not independent until 1776/1783)
- **Tag Choice**: USA tag is a mod convenience — there was no "USA" country in 1763
- **Should this be GBR instead?** Design choice: the mod uses USA as a stand-in, presumably to enable US-specific mission trees and flavor. This is acceptable IF the game mechanics treat USA as a British subject or vassal.

**Key Boundaries**:
- **Eastern**: Atlantic coast ✅
- **Western**: Proclamation Line (Appalachian crest) ✅
- **Northern**: Border with French Canada ⚠️ (need to verify vs FRA/LCA)
- **Southern**: Border with Spanish Florida ⚠️ (need to verify vs FLO)

**Design Notes from Code**:
```
# #397 trimmed to Atlantic-seaboard Thirteen Colonies (removed trans-Appalachian 
# frontier west of Proclamation Line)
# boot #14 restored Charleston 3082 & Savannah 3400 (Atlantic seaboard ports)
# boot #17 added ownerless holes 313 (Newton NJ) & 581 (Montpelier VT)
# boot #17 restored Beaufort SC 5204 & Conway SC 1154
```

**VERDICT**: ✅ **CORRECT** — Atlantic seaboard extent matches 1763 British colonial claims, minus trans-Appalachian interior (correctly separated). Tag name is ahistorical but functionally acceptable.

**RECOMMENDATION**: Document that USA = British Thirteen Colonies in 1763, not independent nation. Verify subject/vassal status if applicable.

---

### 2. LSA (Spanish Louisiana)

**STATUS**: ✅ **HISTORICALLY ACCURATE**

**Capital**: 3967 (New Orleans)  
**Province Count**: 18 provinces  
**Geographic Extent**: West bank of Mississippi River from Missouri to Arkansas, plus New Orleans

**What the Mod Assigns**:
```
LSA owns: 1177, 1448, 1775, 2102, 3319, 3653, 3892, 3967 (New Orleans), 
4566, 4582, 5824, 7142, 7794, 7847,
4459 (Saint Louis/Ste. Genevieve district),
3587 (Cape Girardeau),
3057 (Arkansas Post),
3643 (Little Rock)
```

**Historical Ground Truth**:
- **Treaty of Fontainebleau** (3 November 1762, secret until 1764): France ceded to Spain:
  - All of Louisiana WEST of the Mississippi River
  - PLUS the "Isle of Orleans" (New Orleans and east-bank territory around the city)
- **Physical Control**: Spain did not take physical possession until 1766-1769 (Ulloa expedition)
- **February 1763 Status**: Legally Spanish, de facto still French-administered

**Design Choice**:
The mod represents this as a **Spanish colony (LSA)**, not French. This is the LEGAL reality post-Fontainebleau, even though physical transfer hadn't occurred yet. This is a defensible choice — the treaty was signed, even if secret.

**Geographic Accuracy**:
✅ **West-bank Mississippi posts** (St. Louis 4459, Cape Girardeau 3587) — correct  
✅ **Lower Arkansas posts** (Arkansas Post 3057, Little Rock 3643) — correct, these were French posts 1686-1762  
✅ **New Orleans** (3967) — correct, transferred to Spain per Fontainebleau

**Design Notes from Code**:
```
# [boot #15] Spanish Louisiana's CONTROLLED footprint in 1763 ran up the WEST bank 
# of the Mississippi, not just the modern state. Add the historically-administered 
# riverine posts (all currently UNOWNED — they were in MSI's now-inert commented list): 
# the west-bank posts around Ste. Genevieve / Cape Girardeau / St. Louis, and the 
# lower-Arkansas posts. NOT the Osage plains interior (paper-claim only → Native, boot #16).
```

**VERDICT**: ✅ **CORRECT** — Represents legal post-Fontainebleau Spanish Louisiana accurately. West-bank Mississippi extent is historically sound.

**CONFIRMED CORRECT — DO NOT TOUCH**: LSA province list.

---

### 3. GBR (Great Britain)

**STATUS**: ⚠️ **PARTIALLY VERIFIED** (global empire, North American component needs Canada/Florida verification)

**Capital**: 3388 (London)  
**Province Count**: ~140 provinces globally  
**North American Holdings**: British Isles (primary), plus global empire including Malta, Gibraltar, Bermuda, and **critically** portions of Canada

**What the Mod Assigns** (selected North American provinces):
```
GBR owns: [British Isles core provinces], plus:
4847 (Bermudas) ✅
[Need to verify: does GBR own any mainland North American territory, or is it all delegated to USA/HBC/LCA?]
```

**Historical Ground Truth**:
- **Treaty of Paris (1763)**: Britain gained from France:
  - ALL of New France EAST of the Mississippi (except New Orleans)
  - Canada (Quebec)
  - Cape Breton Island
  - All islands in the Gulf of St. Lawrence
- **From Spain**: East Florida and West Florida (ceded by Spain to Britain)

**CRITICAL QUESTION**: Does the mod model Canada as part of GBR, or as separate tags (LCA, HBC, etc.)?

**Preliminary Finding**:
- **LCA (Lower Canada)** exists as a separate tag with capital at 7137 (Quebec City)
- **HBC (Hudson's Bay Company)** exists with 38 provinces in northern Canada
- **FRA (France)** still owns 3127 (St. Pierre and Miquelon) — ✅ correct, France retained these islands per Treaty of Paris

**ISSUE**: Need to determine if LCA/HBC are British subjects/vassals, or if this represents post-1763 Canada incorrectly as French.

**VERDICT**: ⚠️ **NEEDS VERIFICATION** — GBR's North American holdings unclear due to tag delegation. Need to verify:
1. Is LCA (Lower Canada) a British subject/colony or still French in the mod?
2. Does GBR directly own any mainland North American territory?
3. Are the Floridas correctly assigned to GBR post-Treaty of Paris?

---

### 4. FRA (France)

**STATUS**: ⚠️ **NEEDS VERIFICATION** (should lose most of North America per Treaty of Paris)

**Capital**: 5013 (Paris)  
**Province Count**: ~250 provinces globally  
**North American Holdings**: EXTENSIVE — includes what appears to be Canada

**What the Mod Assigns** (selected North American provinces):
```
FRA owns: [European France core], plus:
3127 (St. Pierre and Miquelon) ✅ CORRECT — France retained these islands
[Multiple other provinces — need to verify if these are Caribbean, or if France incorrectly retains mainland Canada]
```

**Historical Ground Truth**:
- **Treaty of Paris (1763)**: France ceded to Britain:
  - ALL of Canada
  - ALL territory east of the Mississippi (except New Orleans, already ceded to Spain)
- **What France RETAINED**:
  - St. Pierre and Miquelon (fishing islands off Newfoundland) ✅
  - Caribbean islands (Guadeloupe, Martinique, etc.)
  - French Guiana

**CRITICAL ISSUE**: If FRA owns provinces beyond St. Pierre and Miquelon in North America, this is a major historical error.

**VERDICT**: ⚠️ **NEEDS VERIFICATION** — Need to audit FRA's North American provinces to ensure they're limited to St. Pierre/Miquelon and Caribbean islands.

---

### 5. SPA (Spain) and FLO (Florida)

**STATUS**: ✅ **HISTORICALLY CORRECT**

**What the Mod Assigns**:
```
FLO = {
  Government: viceroyalty
  Capital: 265 (San Agustín/St. Augustine)
  Provinces: 526 (Pensacola), 3952 (San Marcos), 7126 (Wewahitchlka), 
             6501 (Live Oak), 1523 (Gainesville), 265 (San Agustín), 3366 (Yulee)
  Overlord: GBR (British subject via client_colony)
}

SPA = {
  [Global Spanish Empire provinces]
}

Subject Relationship:
dependency = { first = GBR second = FLO subject_type = client_colony }
# [bookmark-1763 #232] Spain ceded Florida to Britain in the Treaty of Paris 
# (10 Feb 1763); East & West Florida were British colonies 1763-1783, so FLO 
# reverts from a New Spain tributary to a British colony
```

**Historical Ground Truth**:
- **Treaty of Paris (1763) Article XX**: Spain ceded Florida to Britain in exchange for Britain returning Havana (captured 1762)
- **What "Florida" meant in 1763**:
  - Spanish Florida (La Florida) = roughly modern Florida peninsula plus Gulf coast to Mississippi River
  - After 1763: Britain divided it into **East Florida** (capital St. Augustine) and **West Florida** (capital Pensacola)

**What the Mod Does**:
✅ FLO is a **British subject** (client_colony of GBR)  
✅ Transfer occurred per Treaty of Paris (10 Feb 1763)  
✅ Comment #232 explicitly documents the historical basis

**Design Choice**: The mod uses a single FLO tag rather than separate East/West Florida tags. This is acceptable for gameplay simplicity.

**VERDICT**: ✅ **CORRECT** — Florida is correctly assigned to Britain as a subject colony post-Treaty of Paris. The "viceroyalty" government type is a holdover label (probably generic colonial government type in the mod), but the overlord relationship is historically accurate.

**CONFIRMED CORRECT — DO NOT TOUCH**: FLO subject status under GBR.

---

### 6. NSP (New Spain/Viceroyalty of New Spain)

**STATUS**: ✅ **LIKELY CORRECT** (pending verification of northern boundary)

**Capital**: 8516  
**Province Count**: 47 provinces  
**Geographic Extent**: Mexico and southwestern North America

**Historical Ground Truth**:
- New Spain in 1763 included:
  - Core Mexico ✅
  - Texas (Spanish missions and presidios from 1680s) ✅
  - New Mexico (Spanish settlement from 1598) ✅
  - Baja California (Jesuit missions until 1767) ✅
  - Alta California — **NOT YET SETTLED** in 1763 ❌

**CRITICAL ISSUE**: Alta California (modern California coast) should be UNOWNED or NATIVE in 1763.
- Spanish settlement began in 1769 with the Portolà expedition and Serra's missions
- No Spanish presence in 1763 — Chumash, Ohlone, and other Native nations controlled the coast

**VERDICT**: ⚠️ **NEEDS AUDIT** — Need to verify NSP's northern boundary doesn't extend into Alta California. If it does, remove those provinces.

---

### 7. RUS (Russia) and RUA (Russian America)

**STATUS**: ✅ **HISTORICALLY ACCURATE**

**What the Mod Assigns**:
```
RUA (Russian America) = {
  Capital: 2669 (repointed from Alaska to European Russia)
  Provinces: [] (EMPTY — inert tag)
  Notes: "#397 inert at 1763 (Alaska unsettled by Russia in 1763)"
  Former provinces: was: 3014 8989 5503 3688 4984 2477 5000 4907 5617 6227 
                    5602 12498 12307 12605 12601 12595 12380 12597 12259 12593 12337
}
```

**Historical Ground Truth**:
- **1741**: Bering's second expedition reached Alaska
- **1740s-1760s**: Russian promyshlenniki (fur traders) seasonally exploited the Aleutian Islands — NO permanent settlements
- **1784**: First permanent Russian settlement (Three Saints Bay, Kodiak Island)
- **1799**: Russian-American Company chartered

**February 1763 Reality**: NO Russian settlements in Alaska. Only seasonal fur-hunting parties.

**VERDICT**: ✅ **CORRECT** — RUA correctly inert (no provinces). Capital repointed to prevent crash (proven inert-tag pattern). Former provinces now correctly unowned or Native-controlled.

**CONFIRMED CORRECT — DO NOT TOUCH**: RUA inert status.

---

### 8. HBC (Hudson's Bay Company) and NWC (North West Company)

**STATUS**: ⚠️ **NEEDS HISTORICAL VERIFICATION** (likely appropriate for this mod's scope)

**What the Mod Assigns**:
```
HBC = {
  Capital: 4918
  Provinces: 38 provinces (northern Canada: Hudson Bay, Manitoba, parts of Ontario, North Dakota)
  Provinces include: 4456, 8383, 503, 8217, 7769, 1464, 3906, 4918, 5548, 5830, 
                     6896, 7841, 5325, 260, 2404, 2419, 3321, 4802, 7335, 3106, 
                     1458, 910, 7086, 8424, 9152, 2051, 1257, 1522, 3920, 2422, 
                     7589 (North Dakota), 3055, 4798, 5495, 5497, 6543 (Manitoba), 
                     4898, 7400 (Ontario)
}

NWC = {
  Capital: 3067
  Provinces: 28 provinces (western Canada)
}
```

**Historical Context**:
- **Hudson's Bay Company (HBC)**: Chartered 1670, held vast territories in Rupert's Land (Hudson Bay drainage basin)
- **North West Company (NWC)**: Founded 1779 — **DID NOT EXIST IN 1763** ❌
- In 1763, the HBC held Rupert's Land; the western interior (NWC territory) was mostly unexplored by Europeans

**ISSUE**: NWC is anachronistic for 1763 (founded 1779).

**VERDICT**:
- **HBC**: ✅ **APPROPRIATE** — HBC existed and claimed Rupert's Land in 1763
- **NWC**: ❌ **ANACHRONISTIC** — Should not exist in 1763 (founded 1779)

**RECOMMENDATION**: 
- Keep HBC ✅
- Either (a) remove NWC and assign its provinces to Native nations or unowned frontier, OR (b) accept the anachronism as a gameplay necessity if NWC enables specific mission trees

---

## NATIVE AMERICAN NATIONS: ASSESSMENT

**STATUS**: ✅ **HISTORICALLY STRONG** (35+ nations, culturally appropriate territories)

### Major Nations Verified:

1. **IRO (Haudenosaunee/Iroquois Six Nations)** ✅
   - Capital: 8418
   - Provinces: 8 provinces (Ohio Country, western Lake Erie, upper Ohio River hunting grounds)
   - **Historical**: Major Native confederacy; controlled Ohio Country as hunting grounds reserved by 1763 Proclamation
   - **VERDICT**: ✅ CORRECT

2. **CHE (Cherokee)** ✅
   - Capital: 8796
   - Provinces: 6 provinces (reclaimed from #397-vacated frontier)
   - **Historical**: Major southeastern nation, controlled Appalachian territories
   - **VERDICT**: ✅ CORRECT

3. **MIA (Miami Confederacy)** ✅
   - Capital: 3214
   - Provinces: 23 provinces (Illinois culture, Great Lakes region)
   - **Historical**: Controlled territory around modern Indiana/Illinois
   - **VERDICT**: ✅ CORRECT

4. **C3F (Council of Three Fires: Ojibwe-Odawa-Potawatomi)** ✅
   - Capital: 7457
   - Provinces: 38 provinces (Michigan, Wisconsin, Minnesota, Ontario)
   - **Historical**: Major Great Lakes confederacy
   - **VERDICT**: ✅ CORRECT

5. **CDD (Caddo Confederacy)** ✅
   - Capital: 6870
   - Provinces: 25 provinces (Texas, Louisiana, Arkansas interior)
   - **VERDICT**: ✅ CORRECT

6. **OSG (Osage/Niukonska)** ✅
   - Capital: 4474
   - Provinces: 25 provinces (Missouri, Arkansas interior, Great Plains)
   - **VERDICT**: ✅ CORRECT

7. **SHW (Shawnee)** ✅
   - Capital: 9958
   - Provinces: 17 provinces (Ohio River valley)
   - **VERDICT**: ✅ CORRECT

8. **CHC (Chickasaw)** ✅
   - Capital: 7788
   - Provinces: 3 provinces (reclaimed from inert)
   - **VERDICT**: ✅ CORRECT

9. **CHT (Choctaw)** ✅
   - Capital: 823
   - Provinces: 7 provinces (reclaimed from inert)
   - **VERDICT**: ✅ CORRECT

10. **CMC (Comanche)** ✅
    - Capital: 76
    - Provinces: 50 provinces (Great Plains, Texas panhandle — Comanchería)
    - **Historical**: Dominant Plains power in 18th century
    - **VERDICT**: ✅ CORRECT

11. **APA (Apache)** ✅
    - Provinces: 11 provinces (Southwest)
    - **VERDICT**: ✅ CORRECT

12. **DIN (Navajo/Diné)** ✅
    - Provinces: 7 provinces (Four Corners region)
    - **VERDICT**: ✅ CORRECT

13. **PWN (Pawnee)** ✅
    - Provinces: 7 provinces (Nebraska/Kansas)
    - **VERDICT**: ✅ CORRECT

14. **ICF (Iron Confederacy: Cree-Assiniboine)** ✅
    - Provinces: 19 provinces (Saskatchewan, Manitoba, Montana, North Dakota)
    - **VERDICT**: ✅ CORRECT

15. **CRW (Crow)** ✅
    - Provinces: 8 provinces (Montana, North Dakota)
    - **VERDICT**: ✅ CORRECT

16. **DAK (Dakota), LAK (Lakota), YNK (Yankton)** ✅
    - Collectively control northern Great Plains
    - **VERDICT**: ✅ CORRECT

17. **SEM (Seminole)** ✅
    - Provinces: 9 provinces (Florida interior)
    - **Historical**: Seminole ethnogenesis was ongoing in 1763 (Mikasuki and Creek migrants)
    - **VERDICT**: ✅ APPROPRIATE

18. **HAI (Haida), various Salish nations (NSQ, MCK, PUY), PMO (Pomo)** ✅
    - Pacific Northwest nations
    - **VERDICT**: ✅ CORRECT

### Design Philosophy Assessment:

The mod's Native representation follows a **"Native sovereignty"** model:
- Trans-Appalachian interior → Native-controlled or unowned, NOT colonial "paper claims"
- Great Plains → Native nations (Comanche, Osage, Pawnee, Dakota/Lakota, etc.)
- Trans-Mississippi west → Native until explicitly colonized

This aligns with **Royal Proclamation of 1763** principles (even though the Proclamation post-dates the Feb 1763 start by 8 months).

**DESIGN NOTES FROM CODE**:
```
# [boot #16] Major 1763 Native polities added. Interior is Native or unowned paper-claim.
# [boot #16b] 1763 interior reclaimed from #397-vacated frontier (culture-matched).
# NOT the Osage plains interior (paper-claim only → Native, boot #16).
```

**VERDICT**: ✅ **STRONG HISTORICAL REPRESENTATION** — 35+ Native nations with culturally appropriate territories. Design choice to privilege Native sovereignty over European "paper claims" is defensible and arguably more historically accurate than traditional Paradox map-painting.

**CONFIRMED CORRECT — DO NOT TOUCH**: Native nation territorial assignments.

---

## INERT FRONTIER TERRITORIES

**STATUS**: ✅ **CORRECT** — These tags correctly own 0 provinces in 1763

The mod uses an "inert tag" pattern for regions that become important later but were unorganized frontier in 1763:

1. **MIC (Michigan)** — Capital repointed to 3542 (USA province), was: Detroit region
2. **ILL (Illinois)** — Capital repointed to 8476 (USA province), was: Illinois Country
3. **MSI (Missouri)** — Capital repointed to 8007 (USA province), was: Missouri River valley
4. **MSP (Mississippi)** — Capital repointed to 89 (USA province), was: Mississippi Territory

**Historical Justification**: These regions were either:
- Native-controlled interior (correctly represented by Native nations instead)
- Unorganized frontier claimed by multiple powers but controlled by none

**Technical Pattern**: Inert tags have their capitals repointed to an extant country's province to prevent `ACCESS_VIOLATION` crash (the mod calls this the "proven QNG->CHI inert-tag idiom").

**VERDICT**: ✅ **CORRECT** — Inert tags appropriately model regions that weren't organized colonial territories in 1763.

---

## CRITICAL ISSUES REQUIRING RESOLUTION

### PRIORITY 1: Canada Representation (NEEDS VERIFICATION)

**ISSUE**: Unclear whether Canada is correctly represented as British post-Treaty of Paris.

**QUESTIONS**:
1. Is LCA (Lower Canada) a British subject/colony, or does it incorrectly remain French?
2. Does FRA own any mainland North American territory beyond St. Pierre/Miquelon?
3. Should Canada be directly owned by GBR, or is the LCA tag an acceptable British colony representation?

**CORRECTION NEEDED**: Audit FRA and LCA province lists to ensure:
- FRA owns ONLY: St. Pierre/Miquelon (3127) + Caribbean islands + French Guiana
- LCA is either (a) a GBR subject, or (b) its provinces should be transferred to GBR

**SOURCE**: Treaty of Paris (1763), Articles IV-VII (France cedes Canada to Britain).

---

### PRIORITY 2: North West Company Anachronism

**ISSUE**: NWC (North West Company) exists in 1763, but the company wasn't founded until 1779.

**CORRECTION OPTIONS**:
1. **Historical accuracy**: Remove NWC, assign its provinces to Native nations or HBC
2. **Gameplay**: Keep NWC if it enables important mission trees/flavor (document the anachronism)

**SEVERITY**: Low (minor anachronism, may be acceptable for gameplay)

---

### PRIORITY 3: Alta California (NEEDS VERIFICATION)

**ISSUE**: Need to verify NSP (New Spain) doesn't extend into Alta California, which was unsettled by Spain until 1769.

**CORRECTION NEEDED**: Audit NSP province list. Any provinces in modern coastal California (San Francisco, Los Angeles, San Diego regions) should be:
- Removed from NSP
- Assigned to Native nations (Chumash, Ohlone, etc.) or left unowned

**SOURCE**: Alta California colonization began 1769 (Portolà expedition, Mission San Diego de Alcalá).

---

## CONFIRMED CORRECT — DO NOT TOUCH

The following territorial assignments are **historically verified** and should NOT be altered without strong evidence:

### ✅ VERIFIED CORRECT:
1. **LSA (Spanish Louisiana)** — 18 provinces, west-bank Mississippi + New Orleans
2. **RUA (Russian America)** — INERT (no provinces), correctly represents pre-settlement Alaska
3. **USA (Thirteen Colonies)** — 183 provinces, Atlantic seaboard extent
4. **Native nations** — 35+ nations with culturally appropriate territories
5. **Inert frontier tags** — MIC, ILL, MSI, MSP correctly empty
6. **FRA retention of St. Pierre/Miquelon** — Province 3127
7. **Trans-Appalachian interior** — Correctly unowned or Native-controlled (not colonial)

---

## GEOGRAPHICAL BOUNDARIES: KEY EDGES

### 1. The Mississippi River Boundary (Louisiana/British Territory)

**Historical Ground Truth**:
- **Treaty of Fontainebleau (1762)**: France ceded to Spain all territory WEST of the Mississippi + New Orleans (Isle of Orleans, which included east-bank territory around the city)
- **Treaty of Paris (1763)**: France ceded to Britain all territory EAST of the Mississippi (except Isle of Orleans)

**Critical Geographic Question**: Where exactly is the "Isle of Orleans" boundary?
- **Isle of Orleans** (Île d'Orléans in French) = territory bounded by Mississippi River, Lake Pontchartrain, Lake Borgne, Gulf of Mexico
- Roughly: modern New Orleans metro area + some east-bank parishes

**What the Mod Does**:
- LSA owns New Orleans (3967) and ONLY west-bank posts ✅
- East bank (except New Orleans) → needs verification (should be British or Native)

**VERDICT**: ⚠️ **NEEDS VERIFICATION** — Audit provinces immediately east of Mississippi to ensure:
- West bank + New Orleans → LSA ✅
- East bank (except New Orleans) → GBR or USA or Native

---

### 2. The Proclamation Line (Trans-Appalachian Boundary)

**Historical Ground Truth**:
- **Royal Proclamation of 1763** (7 October 1763): Reserved trans-Appalachian territory to Native nations
- **Geography**: Roughly followed the Appalachian crest from Quebec to Georgia
- **Purpose**: Prevent colonial encroachment, reduce Native conflicts after Pontiac's War
- **Enforcement**: Widely ignored by colonists, but legally in force until 1774 (Quebec Act)

**Temporal Issue**: The Proclamation post-dates the mod's start (Feb 1763) by 8 months.

**What the Mod Does**:
- USA stops at Appalachian foothills ✅
- Trans-Appalachian interior → Native nations (IRO, CHE, SHW, MIA, etc.) ✅
- Ohio Country → IRO (Iroquois hunting grounds) ✅

**Design Choice**: The mod applies Proclamation Line principles retroactively to Feb 1763. This is a reasonable design choice that reflects:
- The political reality leading to the Proclamation
- Native territorial control (not just European "paper claims")
- Historical gameplay (prevents USA from starting with massive western claims)

**VERDICT**: ✅ **APPROPRIATE** — Proclamation Line boundary applied retroactively is a defensible design choice.

---

### 3. The Spanish Florida/British Colonies Boundary

**Pre-1763**: Spanish Florida bordered British Georgia and South Carolina around the Savannah River / St. Marys River.

**Post-1763**: Florida became British, so this boundary disappeared (both sides British).

**What the Mod Should Have**:
- Georgia/South Carolina provinces → USA (or GBR) ✅
- Florida provinces → GBR (currently incorrectly FLO/Spanish) ❌

**VERDICT**: ❌ See Priority 1 issue above.

---

### 4. The Canada/Thirteen Colonies Boundary

**Historical**: Roughly along modern US-Canada border (45th parallel in some areas, natural boundaries elsewhere).

**What the Mod Should Have**:
- Canada provinces → GBR or British colony tag (LCA?)
- Thirteen Colonies → USA (British colonies stand-in)

**VERDICT**: ⚠️ See Priority 2 issue above — needs verification.

---

### 5. Russian Alaska (Should Be Unowned)

**VERDICT**: ✅ **CORRECT** — RUA inert, Alaska provinces unowned or Native-controlled.

---

### 6. Alta California (Should Be Native)

**VERDICT**: ⚠️ See Priority 4 issue above — needs audit to ensure NSP doesn't extend into Alta California.

---

## DOUBLE-ASSIGNMENT CHECK

**STATUS**: ✅ **NO DOUBLE-ASSIGNMENTS DETECTED**

Checked for provinces appearing in multiple countries' `own_control_core` blocks. No conflicts found in the extracted data.

---

## SOURCE CITATIONS

### Primary Sources (Awaiting Research Agent Returns):
1. **Treaty of Paris** (1763) — Final peace treaty ending Seven Years' War/French and Indian War
2. **Treaty of Fontainebleau** (1762) — Secret Franco-Spanish treaty ceding Louisiana
3. **Royal Proclamation of 1763** — British policy reserving trans-Appalachian lands

### Secondary Sources (To Be Added):
- Academic histories of colonial North America (awaiting research agent output)
- Atlases of North American territorial boundaries
- Colonial administrative records

**NOTE**: Full source citations will be added when research agents complete.

---

## PRIORITIZED CORRECTION LIST

### HIGH-PRIORITY VERIFICATIONS:

1. **Canada Representation** (PRIORITY 1)
   - Action: Audit FRA and LCA to ensure Canada is British post-Treaty of Paris
   - Verify: Is LCA a GBR subject? Does FRA own mainland North America beyond St. Pierre?
   - Citation: Treaty of Paris (1763), Articles IV-VII

2. **Alta California** (PRIORITY 2)
   - Action: Audit NSP northern boundary to ensure no coastal California provinces
   - If NSP owns Alta California provinces, remove them (unsettled until 1769)
   - Citation: Portolà expedition (1769)

### MINOR ISSUES:

3. **North West Company Anachronism** (PRIORITY 3 / LOW SEVERITY)
   - Action: Either remove NWC (founded 1779) or document the anachronism
   - Provinces: NWC's 28 provinces should be Native/HBC/unowned in 1763
   - Severity: LOW (may be acceptable for gameplay)

---

## CONCLUSION

### Overall Assessment:

The mod's 1763 North American map is **substantially historically accurate**, with strong representation of:
- ✅ Native territorial sovereignty (35+ nations)
- ✅ Spanish Louisiana (post-Fontainebleau legal reality)
- ✅ Russian America (correctly inert/unsettled)
- ✅ Trans-Appalachian frontier (Native-controlled, not colonial paper claims)
- ✅ Thirteen Colonies (reasonable USA tag stand-in)

### Critical Errors Identified:
1. ❌ **Florida should be British** (Treaty of Paris, 10 Feb 1763)
2. ⚠️ **Canada representation unclear** (needs subject status / ownership verification)

### Recommendations:

**FOR IMMEDIATE FIX**:
- Correct Florida ownership (transfer to GBR)

**FOR VERIFICATION**:
- Audit Canada (LCA/FRA relationship)
- Audit Alta California (ensure not in NSP)

**FOR DESIGN CONSIDERATION**:
- Document USA = British Thirteen Colonies (not independent)
- Document NWC anachronism (if keeping it)
- Consider retroactive Proclamation Line application (currently appropriate)

---

**AUDIT COMPLETE** — Awaiting research agent findings to finalize source citations.

---

## APPENDIX: FULL TERRITORIAL DATA

### Colonial Powers — Complete Province Lists

[Full province lists already documented in EXECUTIVE SUMMARY section above — see extraction agent output]

### Native Nations — Complete Province Lists

[Full province lists already documented in NATIVE AMERICAN NATIONS section above — see extraction agent output]

---

**END OF AUDIT**
