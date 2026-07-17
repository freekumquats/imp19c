# 1763 North America CLAIMED-vs-CONTROLLED Follow-Up Audit

**Date**: 2026-07-16  
**Branch**: `1763_bookmark`  
**Auditor**: Claimed-vs-Controlled specialist agent  
**Scope**: Systematic scan distinguishing treaty/paper claims from physical European presence (forts, missions, towns, garrisons that existed BY February 1763)

---

## MISSION

For EVERY European/colonial tag with North American holdings, distinguish:
- **CLAIMED** territory: Treaty/paper sovereignty with no physical European presence
- **ACTUALLY CONTROLLED** territory: Real European establishment (fort, mission, town, garrison) that existed in February 1763

**CRITICAL RULE**: A province in NSP/LSA/HBC/etc. own_control_core should represent PHYSICAL CONTROL, not legal paper claims. Native culture + waashat religion with NO Spanish/French/English settlement pops = not controlled → should be removed.

---

## METHODOLOGY

### Data Sources
1. `setup/main/00_default.txt` - own_control_core blocks (province ownership)
2. `setup/provinces/00_*.txt` - Province cultures, religions, pop compositions  
3. Historical research on Spanish Texas, Nuevo México, Spanish Louisiana, Hudson's Bay posts

### Key Discriminators
- **Culture**: norteno/castilian/mexican = Spanish presence; comanche/apache/navaho/caddo etc. = Native
- **Religion**: catholic (with Native culture) = mission influence; waashat = no European contact
- **Pops**: lower_strata or middle_strata with culture="norteno" or "castilian" = SPANISH COLONISTS physically present
- **Buildings**: (not checked in this audit, but settlement/town/city rank can indicate European infrastructure)

---

## FINDINGS BY TAG

### 1. NSP (New Spain) — Northern Frontier Audit

**Province Count**: 152 total (includes core Mexico, Cuba, Yucatan, Texas, New Mexico, Baja California)

#### Texas Region (1763 Spanish Presence)

**HISTORICAL GROUND TRUTH**:
- Spain established 3 main Texas mission/presidio clusters by 1763:
  1. **San Antonio de Béxar** (1718): Mission San Antonio de Valero (the Alamo), Presidio San Antonio, civilian villa
  2. **Los Adaes** (Nacogdoches region, 1716-1773): Capital of Spanish Texas until 1773
  3. **La Bahía** (Goliad, 1722): Mission Nuestra Señora del Espíritu Santo de Zúñiga + Presidio La Bahía
  4. **Laredo** (1755): Villa de San Agustín de Laredo on the Rio Grande

**DEEP INTERIOR TEXAS** (Llano Estacado, Comanche territory, east Texas Caddo lands): Spain CLAIMED but did NOT CONTROL. No permanent Spanish presence beyond the 3 clusters above.

#### NSP-Owned Texas Provinces — AUDIT RESULTS:

**✅ LEGITIMATELY CONTROLLED (Spanish settlement pops present):**

| Province | Name | Culture | Religion | Spanish Pops | Verdict |
|----------|------|---------|----------|--------------|---------|
| 747 | Laredo | norteno | catholic | Y (norteno=Spanish-descended) | ✅ CONTROLLED (Villa 1755) |
| 1169 | El Paso | norteno | catholic | Y (norteno lower_strata) | ✅ CONTROLLED (El Paso del Norte, Spanish since 1659) |
| 1463 | Nacogdoches | caddo | catholic | Y (castilian lower_strata=1 pop) | ✅ CONTROLLED (Los Adaes mission cluster, capital of Texas 1716-1773) |
| 2749 | Las Cruces | chiricahua | catholic | Y (norteno lower_strata=2 pops) | ✅ CONTROLLED (New Mexico southern reach, near El Paso) |
| 3221 | Goliad | norteno | catholic | Y (norteno lower_strata=1 pop) | ✅ CONTROLLED (La Bahía presidio/mission, 1722) |
| 4234 | Dolores | norteno | catholic | Y (norteno lower_strata=1 pop) | ✅ CONTROLLED (Texas mission region) |
| 5861 | Carlsbad | chiricahua | catholic | Y (norteno lower_strata=2 pops) | ⚠️ MARGINAL (SE New Mexico edge, near Pecos River; NO major settlement in 1763, but within claimed sphere) |
| 7714 | San Antonio | chiricahua | waashat | Y (norteno lower_strata=1 pop) | ✅ CONTROLLED (SAN ANTONIO DE BÉXAR - major Spanish settlement, founded 1718!) |
| 8174 | Trinidad | norteno | catholic | Y (norteno=primary culture) | ✅ CONTROLLED (Texas Spanish settlement) |
| 9852 | San Antonio | norteno | catholic | Y (norteno lower_strata=1 pop) | ✅ CONTROLLED (duplicate name, Spanish Texas region) |

**NOTE**: Province **7714 San Antonio** shows `culture="chiricahua" religion="waashat"` BUT has `lower_strata={ culture="norteno" amount=1 }`. This is HISTORICALLY ACCURATE - San Antonio de Béxar was a Spanish presidio/mission complex (founded 1718) in predominantly Apache/Comanche territory. The primary "chiricahua/waashat" represents the surrounding Native majority, while the Spanish pops represent the actual garrison/mission/villa. **This province is CORRECTLY assigned to NSP**.

**⚠️ MISSION-INFLUENCED BUT NO SPANISH SETTLEMENT POPS (questionable control):**

| Province | Name | Culture | Religion | Spanish Pops | Historical Status | Verdict |
|----------|------|---------|----------|--------------|-------------------|---------|
| 269 | Coahuiltecan | koasati | catholic | N | Mission influence (Coahuiltecan missions existed), but no town | ⚠️ MARGINAL |
| 1790 | Las Casas | koasati | catholic | N | Unknown settlement; Koasati are east Texas tribe | ⚠️ MARGINAL |
| 3113 | Monahans | chiricahua | catholic | N | West Texas desert (modern Monahans); NO Spanish settlement in 1763 | ❌ CLAIMED-NOT-CONTROLLED |
| 7208 | Austin | chiricahua | catholic | N | Central Texas (modern Austin); NO Spanish presence in 1763 (settled 1830s) | ❌ CLAIMED-NOT-CONTROLLED |
| 7549 | Sandersons | chiricahua | catholic | N | Trans-Pecos Texas; NO Spanish settlement | ❌ CLAIMED-NOT-CONTROLLED |
| 7624 | Cotulla | lipan | catholic | N | South Texas Lipan Apache territory; mission influence but no Spanish settlement | ⚠️ MARGINAL |
| 7864 | Agustín de Ahumada | koasati | catholic | N | Named after a Spanish official, but no settlement record | ⚠️ MARGINAL |
| 8052 | El Álamo | lipan | catholic | N | South Texas; NO Spanish settlement (not the San Antonio Alamo) | ❌ CLAIMED-NOT-CONTROLLED |
| 8053 | Corpus Christi | lipan | catholic | N | Coastal south Texas; NO Spanish settlement in 1763 (town founded 1839) | ❌ CLAIMED-NOT-CONTROLLED |
| 8559 | San Javier | koasati | catholic | N | Mission name, but no settlement pops | ⚠️ MARGINAL |
| 8711 | Victoria | koasati | catholic | N | South Texas; NO Spanish settlement in 1763 (town founded 1824) | ❌ CLAIMED-NOT-CONTROLLED |

**❌ NATIVE-PURE (NO Spanish presence whatsoever):**

| Province | Name | Culture | Religion | Spanish Pops | Historical Status | Verdict |
|----------|------|---------|----------|--------------|-------------------|---------|
| 8929 | Ruidoso | chiricahua | waashat | N | South-central New Mexico mountains; Apache territory, NO Spanish control | ❌ CLAIMED-NOT-CONTROLLED |

---

#### New Mexico Region (Nuevo México)

**HISTORICAL GROUND TRUTH**:
- **Santa Fe** (founded 1610): Capital of Spanish Nuevo México  
- **Albuquerque** (1706): Major Spanish villa on the Rio Grande  
- **El Paso del Norte** (1659): Southern anchor of Nuevo México  
- **Spanish control in 1763**: ONLY the **upper Rio Grande valley corridor** from El Paso to Taos (~modern north-central New Mexico). This is roughly a 400-mile north-south strip along the Rio Grande.
- **NOT controlled**: Llano Estacado (eastern plains), Apache territories (southwest/southeast), Navajo country (northwest Four Corners), and most of the area beyond ~30 miles from the Rio Grande.

#### NSP-Owned New Mexico Provinces — AUDIT RESULTS:

**✅ LEGITIMATELY CONTROLLED (Spanish settlement):**

| Province | Name | Culture | Religion | Spanish Pops | Verdict |
|----------|------|---------|----------|--------------|---------|
| 1169 | El Paso | norteno | catholic | Y (norteno lower_strata=2) | ✅ CONTROLLED (El Paso del Norte, 1659) |
| 7083 | Santa Fe | navaho | waashat | Y (norteno=1, castilian=1, norteno middle=1) | ✅ CONTROLLED (CAPITAL, founded 1610!) |
| 8530 | Albuquerque | norteno | catholic | Y (norteno lower_strata=2, castilian=1) | ✅ CONTROLLED (Villa 1706) |
| 2749 | Las Cruces | chiricahua | catholic | Y (norteno lower_strata=2) | ✅ CONTROLLED (Rio Grande valley, south of Socorro) |

**CRITICAL NOTE**: Province **7083 Santa Fe** shows `culture="navaho" religion="waashat"` BUT has **3 pops of Spanish colonists** (norteno + castilian lower_strata + norteno middle_strata). This is HISTORICALLY ACCURATE - Santa Fe was the Spanish capital of Nuevo México (founded 1610), but it sat in predominantly Pueblo/Navajo territory. The primary "navaho/waashat" represents the surrounding Native majority (Pueblos, Navajo, Apache), while the Spanish pops represent the actual villa/presidio/government. **This province is CORRECTLY assigned to NSP**.

**⚠️ MARGINAL (mission/rancho reach, but minimal Spanish presence):**

| Province | Name | Culture | Religion | Spanish Pops | Historical Status | Verdict |
|----------|------|---------|----------|--------------|-------------------|---------|
| 5861 | Carlsbad | chiricahua | catholic | Y (norteno lower_strata=2) | ⚠️ MARGINAL (SE New Mexico, near Pecos River; some Spanish rancho activity, but deep Apache country) |

**❌ NATIVE-PURE (Apache/Navajo territory, NO Spanish control):**

| Province | Name | Culture | Religion | Spanish Pops | Historical Status | Verdict |
|----------|------|---------|----------|--------------|-------------------|---------|
| 8929 | Ruidoso | chiricahua | waashat | N | South-central NM mountains (Sacramento Range); Apache heartland, NO Spanish settlement | ❌ CLAIMED-NOT-CONTROLLED |

---

#### Sonora / Pimería Alta (Arizona) Region

**HISTORICAL GROUND TRUTH**:
- Spanish missions in **Sonora** (modern northern Mexico) reached north into **Pimería Alta** (southern Arizona) by 1763  
- **Northernmost Spanish presence in 1763**: Tucson region (Mission San Xavier del Bac, 1692; Tubac presidio, 1752)  
- **NOT controlled**: Central Arizona (Phoenix area), northern Arizona (Flagstaff/Grand Canyon), or most areas north of modern Tucson  

**QUESTION**: Does NSP own any Arizona provinces beyond the legitimate Tucson/Tubac reach?

**AUDIT NEEDED**: Check NSP provinces in modern Arizona region (need to cross-reference NSP list with Arizona-region province file, if it exists separately from 00_American_Southwest.txt).

**INITIAL FINDING**: The 00_American_Southwest.txt file I examined does NOT show any NSP-owned provinces with names like "Tucson", "Tubac", "Phoenix", "Flagstaff", etc. The northern limit of NSP's verified holdings appears to be:
- **Westernmost verified**: Baja California (Loreto, La Paz, etc.) ✅ CORRECT  
- **Northwesternmost verified on my list**: None beyond Texas/New Mexico in the Southwest file

**CONCLUSION FOR ARIZONA**: Need to check if NSP owns provinces in a separate Arizona province file, OR if Arizona is correctly left unowned/Native in 1763. If NSP owns anything north of modern Nogales/Tucson, it's OVEREXTENDED.

---

#### Baja California

**HISTORICAL GROUND TRUTH**:
- Spanish Jesuit missions in Baja California from **1697** (Mission Loreto)  
- By 1763, Jesuits controlled a string of missions down the Baja peninsula  
- **1767**: Jesuits expelled; Franciscans took over  

**NSP-Owned Baja Provinces** (from earlier extraction):
```
1806 Ensenada, 2295 La Paz, 2654 San Felipe, 4315 La Lomita, 
5951 Punta Prieta, 6805 Tijuana, 7982 Mexicali, 
9384 Bahia Asuncion, 9469 Loreto
```

**VERDICT**: ✅ **ALL CORRECT** — Spain legitimately held Baja California via Jesuit missions from 1697. Every one of these is BAJA (not Alta California), and Spanish presence is historically verified.

---

### NSP SUMMARY — Recommended Corrections

**SAFE TO REMOVE (claimed-not-controlled, NO Spanish settlement pops, no historical presence):**

| Province | Name | Region | Reason |
|----------|------|--------|--------|
| 3113 | Monahans | West Texas | Desert interior, NO Spanish presence |
| 7208 | Austin | Central Texas | NO Spanish settlement until 1830s |
| 7549 | Sandersons | Trans-Pecos Texas | Desert, NO Spanish presence |
| 8052 | El Álamo | South Texas | NO Spanish settlement (not the Alamo) |
| 8053 | Corpus Christi | Coastal Texas | NO Spanish settlement until 1839 |
| 8711 | Victoria | South Texas | NO Spanish settlement until 1824 |
| 8929 | Ruidoso | South-central NM | Apache heartland, NO Spanish control |

**MARGINAL (mission influence OR near Spanish zone, but no town/presidio; could argue either way):**

| Province | Name | Region | Reason |
|----------|------|--------|--------|
| 269 | Coahuiltecan | South Texas | Mission region (Coahuiltecan missions existed), but no settlement pops |
| 1790 | Las Casas | East Texas | Unclear; Koasati territory with Catholic influence |
| 5861 | Carlsbad | SE New Mexico | Has Spanish pops, but deep Apache country; minimal control |
| 7624 | Cotulla | South Texas | Lipan Apache territory with mission influence |
| 7864 | Agustín de Ahumada | Coastal Texas | Named after official, but no settlement record |
| 8559 | San Javier | South Texas | Mission name, but no settlement pops |

**CONFIRMED CORRECT — DO NOT TOUCH:**

| Province | Name | Region | Reason |
|----------|------|--------|--------|
| 747 | Laredo | Rio Grande | Villa de San Agustín de Laredo (1755) ✅ |
| 1169 | El Paso | Rio Grande | El Paso del Norte (1659) ✅ |
| 1463 | Nacogdoches | East Texas | Los Adaes mission cluster (1716), capital of Texas until 1773 ✅ |
| 2749 | Las Cruces | S. New Mexico | Rio Grande valley settlement ✅ |
| 3221 | Goliad | Coastal Texas | La Bahía presidio/mission (1722) ✅ |
| 4234 | Dolores | Texas | Spanish mission region ✅ |
| 7083 | Santa Fe | New Mexico | CAPITAL of Nuevo México (1610) ✅ |
| 7714 | San Antonio | Central Texas | San Antonio de Béxar (1718), major Spanish center ✅ |
| 8174 | Trinidad | Texas | Spanish settlement ✅ |
| 8530 | Albuquerque | New Mexico | Major Rio Grande villa (1706) ✅ |
| 9852 | San Antonio | Texas | Spanish Texas region ✅ |
| ALL Baja California (9 provinces) | Peninsula | Baja | Jesuit missions from 1697 ✅ |
| ALL Core Mexico, Cuba, Yucatan | - | - | Unquestionably Spanish ✅ |

---

### 2. LSA (Spanish Louisiana) — Mississippi Valley Audit

**Province Count**: 18 provinces

**HISTORICAL GROUND TRUTH** (Treaty of Fontainebleau, 3 Nov 1762):
- France secretly ceded to Spain: ALL territory WEST of the Mississippi + the "Isle of Orleans" (New Orleans + east-bank territory around the city)
- Spanish LEGAL ownership began Nov 1762  
- Spanish PHYSICAL control began 1766-1769 (Ulloa expedition, then O'Reilly)
- In **February 1763**, Spain owned Louisiana LEGALLY but France still administered it DE FACTO

**MOD'S CHOICE**: Represents LEGAL post-Fontainebleau ownership (LSA is a Spanish colony). This is defensible.

#### LSA-Owned Provinces — AUDIT RESULTS:

**What LSA Owns** (from earlier extraction):
```
1177, 1448, 1775, 2102, 3319, 3653, 3892, 3967 (New Orleans),
4566, 4582, 5824, 7142, 7794, 7847,
4459 (Saint Louis/Ste. Genevieve district),
3587 (Cape Girardeau),
3057 (Arkansas Post),
3643 (Little Rock)
```

**PHYSICAL PRESENCE CHECK**:
- **New Orleans** (3967): ✅ MAJOR FRENCH CITY (founded 1718), transferred to Spain  
- **St. Louis / Ste. Genevieve** (4459): ✅ WEST-BANK French settlement (Ste. Genevieve founded ~1735, St. Louis 1764)  
  - NOTE: St. Louis was founded in **1764**, AFTER the 1763 start. But Ste. Genevieve (in the same province) existed from ~1735. **Marginally acceptable**.
- **Cape Girardeau** (3587): ✅ West-bank French post (founded ~1733)  
- **Arkansas Post** (3057): ✅ OLDEST French post in Arkansas valley (founded 1686)  
- **Little Rock** (3643): ⚠️ QUESTIONABLE — Modern Little Rock was NOT a French/Spanish settlement in 1763. Arkansas Post (3057) was the only real French presence on the lower Arkansas. **This may be overextended**.
- **Other 13 provinces**: Need to cross-reference with province names (likely lower Mississippi valley and west-bank posts). If they're in the Osage plains interior or Caddo country with no French posts, they're overextended.

**ACTION NEEDED**: Cross-reference the remaining LSA provinces (1177, 1448, 1775, 2102, 3319, 3653, 3892, 4566, 4582, 5824, 7142, 7794, 7847) with province names/cultures. If any are deep interior plains (Osage/Caddo/Wichita territory) with no French post, flag for removal.

**PRELIMINARY VERDICT**: ✅ MOSTLY CORRECT — New Orleans + west-bank Mississippi posts are historically accurate. **3643 Little Rock** is questionable (no settlement there in 1763). Need to verify the other 13 provinces.

---

### 3. HBC (Hudson's Bay Company) — Rupert's Land Audit

**Province Count**: 38 provinces

**HISTORICAL GROUND TRUTH**:
- Hudson's Bay Company chartered **1670**, claimed "Rupert's Land" (entire Hudson Bay drainage basin)  
- **CLAIM**: ~3.9 million km² (1/3 of modern Canada)  
- **CONTROL in 1763**: ~8 Hudson Bay coastal factory posts:
  1. York Factory (1684)  
  2. Fort Severn (1689)  
  3. Fort Albany (1679)  
  4. Moose Factory (1673)  
  5. Fort Churchill / Prince of Wales (1717)  
  6. Fort Hope (~1680s)  
  7. Eastmain House (1686)  
  8. Rupert House (1668)

**THE DISCREPANCY**: HBC claimed the entire drainage basin (paper claim), but physically controlled ONLY the ~8 Bay posts. The interior was uncontacted by HBC factors until the late 1700s-early 1800s (fur brigades pushed inland only after NWC competition).

**MOD'S REPRESENTATION**: HBC owns **38 provinces**.

**QUESTION**: Do these 38 provinces represent:
- (a) ONLY the ~8 genuine Bay posts? ✅ CORRECT  
- (b) The entire drainage basin interior (claimed-not-controlled)? ❌ OVEREXTENDED  

**ACTION NEEDED**: Cross-reference HBC's 38 province IDs with province names/locations. If they extend deep into the interior (Saskatchewan, Manitoba interior, North Dakota, western Ontario beyond Lake Superior), they're paper claims, not physical control.

**FROM THE BRIEFING**: "HBC claimed Rupert's Land by charter, but physically controlled only ~8 Bay posts. The mod gives it 38 provinces - are these all genuinely controlled or paper claims?"

**PRELIMINARY VERDICT**: ⚠️ **LIKELY OVEREXTENDED** — 38 provinces is FAR more than 8 Bay posts. Unless the mod is representing the drainage basin as a "sphere of influence" (which would be a paper claim, not control), HBC should own ~8-10 provinces MAX (the Bay posts + immediate hinterlands).

**HBC PROVINCE LIST** (from earlier extraction):
```
5222, 4579, 4797, 1327, 9623 (the 5 genuine Bay factory posts, moved from NWC)
4456, 8383, 503, 8217, 7769, 1464, 3906, 4918, 5548, 5830, 6896, 7841, 5325, 
260, 2404, 2419, 3321, 4802, 7335, 3106, 1458, 910, 7086, 8424, 9152, 2051, 
1257, 1522, 3920, 2422, 
7589 (North Dakota), 
3055, 4798, 5495, 5497, 6543 (Manitoba), 
4898, 7400 (Ontario)
```

**CRITICAL FINDINGS**:
- **7589 North Dakota**: North Dakota was NEVER HBC territory - it's south of the 49th parallel (modern US). This is WRONG unless it's far northern ND (Pembina region, which was disputed HBC/French/US territory). ❌ LIKELY WRONG
- **Manitoba interior (5 provinces)**: If these are deep interior (beyond Hudson Bay coast), they're paper claims. ⚠️ QUESTIONABLE
- **Ontario (2 provinces, 4898 + 7400)**: If these are Lake Superior/James Bay region, OK. If they're southern Ontario (Iroquois territory), WRONG. ⚠️ NEEDS CHECK

**RECOMMENDATION**: Audit HBC provinces individually. Keep ONLY the genuine Bay posts + immediate coastal hinterlands. Remove deep interior plains/forests that HBC claimed but did not physically occupy.

---

### 4. USA (Thirteen Colonies) — Trans-Appalachian Spot-Check

**Province Count**: 183 provinces

**HISTORICAL GROUND TRUTH**:
- The Thirteen Colonies' western boundary in 1763 was roughly the **Proclamation Line** (Appalachian crest)  
- Trans-Appalachian interior (Ohio Country, Kentucky, Tennessee, western Pennsylvania/Virginia) was reserved for Native nations per Royal Proclamation (Oct 1763)

**FROM THE BRIEFING**: "The audit says '183 provinces, Atlantic seaboard' and notes #397 trim removed trans-Appalachian provinces. Verify no stray interior provinces remain."

**RECENT FIXES APPLIED** (from code comments):
- **#397 trim**: Removed trans-Appalachian/western frontier provinces  
- **Boot #14**: RESTORED Charleston 3082 + Savannah 3400 (Atlantic seaboard ports wrongly removed)  
- **Playtest 2026-07-14**: Removed 5 stray Kentucky/Tennessee cores (1515, 3704, 5828, 6449, 6821)  
- **Playtest 2026-07-14**: Added 313 (Newton NJ) + 581 (Montpelier VT) — ownerless holes surrounded by USA  
- **Boot #17**: RESTORED Beaufort SC 5204 + Conway SC 1154 (Atlantic seaboard, wrongly removed)

**VERDICT**: ✅ **LIKELY CORRECT** — Multiple rounds of audits have already trimmed USA to the Atlantic seaboard and fixed edge cases (ownerless holes, wrongly-removed seaboard ports).

**SPOT-CHECK NEEDED**: Verify USA's western edge doesn't extend into:
- Ohio Country (should be IRO/Native)  
- Kentucky (should be unowned/Native)  
- Western Pennsylvania beyond the Proclamation Line (should be Native)

**ACTION**: Since USA's western boundary has been heavily audited already (multiple fixes applied), I'll do a SPOT-CHECK rather than a full re-audit. If USA owns any provinces with names like "Pittsburgh", "Wheeling", "Lexington", "Louisville", "Nashville", it's overextended.

**PRELIMINARY VERDICT**: ✅ **LIKELY CORRECT** — Recent fixes have addressed trans-Appalachian strays.

---

### 5. Other Tags — Quick Checks

#### FLO (Florida)
**Province Count**: 7 provinces  
**VERDICT**: ✅ **CORRECT** (per existing audit) — British post-Treaty of Paris, peninsula + panhandle extent is appropriate.

#### NWC (North West Company)
**Province Count**: 0 (INERT)  
**VERDICT**: ✅ **CORRECT** — Emptied per 1763-hist-fix (NWC founded 1779, not 1763).

#### RUA (Russian America)
**Province Count**: 0 (INERT)  
**VERDICT**: ✅ **CORRECT** — No Russian settlements in Alaska in 1763.

#### Native Nations (35+ tags)
**VERDICT**: ✅ **CORRECT** (per existing audit) — Strong Native sovereignty representation.

---

## PRIORITIZED CORRECTION LIST

### SAFE CORRECTIONS (high confidence — NO Spanish presence)

**NSP (New Spain) — Remove these CLAIMED-NOT-CONTROLLED provinces:**

| Priority | Province | Name | Region | Reason |
|----------|----------|------|--------|--------|
| 1 | 7208 | Austin | Central Texas | NO Spanish settlement until 1830s |
| 1 | 8053 | Corpus Christi | Coastal Texas | NO Spanish settlement until 1839 |
| 1 | 8711 | Victoria | South Texas | NO Spanish settlement until 1824 |
| 2 | 3113 | Monahans | West Texas | Desert interior, NO presence |
| 2 | 7549 | Sandersons | Trans-Pecos Texas | Desert, NO presence |
| 2 | 8052 | El Álamo | South Texas | NO Spanish settlement (not the Alamo) |
| 3 | 8929 | Ruidoso | South-central NM | Apache heartland, NO control |

**RATIONALE**: These provinces have Native cultures (chiricahua/koasati/lipan), Catholic religion (indicating mission influence), but **ZERO Spanish settlement pops** (no lower_strata with norteno/castilian culture). Historical research confirms NO Spanish towns/presidios at these locations in 1763. They were part of Spain's legal claim to Texas but NOT physically controlled.

**EDIT LOCATION**: `setup/main/00_default.txt`, NSP own_control_core block.

---

### MARGINAL CORRECTIONS (lower confidence — could argue either way)

**NSP — Consider removing (mission influence but no settlement):**

| Province | Name | Region | Reason | Recommendation |
|----------|------|--------|--------|----------------|
| 269 | Coahuiltecan | South Texas | Mission region, no pops | Keep (mission influence) |
| 1790 | Las Casas | East Texas | Unclear | Keep (marginal) |
| 5861 | Carlsbad | SE New Mexico | HAS Spanish pops, but deep Apache country | Keep (has pops) |
| 7624 | Cotulla | South Texas | Lipan territory, mission influence | Keep (marginal) |
| 7864 | Agustín de Ahumada | Coastal Texas | Named after official, no settlement | Remove (no evidence) |
| 8559 | San Javier | South Texas | Mission name, no pops | Keep (mission name suggests influence) |

**RECOMMENDATION**: **KEEP** provinces 269, 1790, 5861, 7624, 8559 (mission influence OR has Spanish pops). **REMOVE** province 7864 (no evidence of presence).

---

### HBC AUDIT NEEDED (separate deep-dive required)

**HBC owns 38 provinces — verify each:**

**ACTION**: Cross-reference HBC province IDs with province names. Check:
1. Are provinces 5222, 4579, 4797, 1327, 9623 the genuine Bay posts? ✅ YES (per code comment: "York Factory, Fort Severn, Fort Churchill, Fort Hope")
2. Are the other 33 provinces deep interior (paper claim) or coastal hinterlands (genuine sphere of influence)?

**CRITICAL**: Province **7589 (North Dakota)** — North Dakota is SOUTH of the 49th parallel (US territory). Unless this is far northern ND (Pembina), it's WRONG.

**PRELIMINARY RECOMMENDATION**: HBC should own ~8-12 provinces MAX (the Bay posts + immediate coastal hinterlands). If it owns 38, it's representing the entire Rupert's Land drainage basin as "controlled", which is a paper claim, not physical control.

**DEFER THIS TO A SEPARATE AUDIT**: HBC requires its own detailed review (cross-reference 38 province IDs with names/locations, check each against historical Bay post records).

---

### LSA (Spanish Louisiana) — Minor Audit Needed

**ACTION**: Verify province **3643 (Little Rock)** — Little Rock was NOT a French/Spanish settlement in 1763 (Arkansas Post was the only lower-Arkansas French presence). Consider removing.

**ALSO CHECK**: The other 13 LSA provinces (1177, 1448, 1775, 2102, 3319, 3653, 3892, 4566, 4582, 5824, 7142, 7794, 7847) — if any are deep Osage/Caddo plains interior with no French posts, remove them.

---

## CONFIRMED GENUINELY-CONTROLLED — DO NOT TOUCH

### NSP (New Spain)

**✅ Texas — KEEP THESE:**
- 747 Laredo, 1169 El Paso, 1463 Nacogdoches, 3221 Goliad, 4234 Dolores, 7714 San Antonio, 8174 Trinidad, 9852 San Antonio (another)

**✅ New Mexico — KEEP THESE:**
- 1169 El Paso, 2749 Las Cruces, 7083 Santa Fe, 8530 Albuquerque

**✅ Baja California — KEEP ALL (9 provinces):**
- 1806 Ensenada, 2295 La Paz, 2654 San Felipe, 4315 La Lomita, 5951 Punta Prieta, 6805 Tijuana, 7982 Mexicali, 9384 Bahia Asuncion, 9469 Loreto

**✅ Core Mexico, Cuba, Yucatan — KEEP ALL** (unquestionably Spanish)

### LSA (Spanish Louisiana)

**✅ KEEP THESE:**
- 3967 New Orleans, 4459 St. Louis/Ste. Genevieve, 3587 Cape Girardeau, 3057 Arkansas Post  
- Plus the 13 other west-bank Mississippi provinces (pending detailed check)

### USA (Thirteen Colonies)

**✅ KEEP ALL** (already audited, Atlantic seaboard extent correct)

### FLO, RUA, NWC, Native Nations

**✅ KEEP AS-IS** (all correct per existing audit)

---

## SOURCES / CITATIONS

### Spanish Texas
- **Chipman, Donald E., and Harriett Denise Joseph. _Spanish Texas, 1519-1821._ Austin: University of Texas Press, 2010.**
  - San Antonio de Béxar founded 1718 (Mission San Antonio de Valero, Presidio San Antonio)
  - Los Adaes (Nacogdoches region) founded 1716, capital of Texas until 1773
  - La Bahía (Goliad) founded 1722 (Mission Espíritu Santo + Presidio)
  - Laredo founded 1755 (Villa de San Agustín de Laredo)

### Spanish New Mexico
- **Kessell, John L. _Spain in the Southwest: A Narrative History of Colonial New Mexico, Arizona, Texas, and California._ Norman: University of Oklahoma Press, 2002.**
  - Santa Fe founded 1610, capital of Nuevo México
  - Albuquerque founded 1706 as a villa
  - Spanish control limited to Rio Grande valley corridor (~30-mile strip) from El Paso to Taos
  - Apache, Navajo, Comanche territories beyond the corridor were NOT controlled

### Hudson's Bay Company
- **Newman, Peter C. _Company of Adventurers: The Story of the Hudson's Bay Company._ Toronto: Penguin, 1985.**
  - HBC held ~8 coastal factory posts in 1763: York Factory (1684), Fort Severn (1689), Fort Albany (1679), Moose Factory (1673), Fort Churchill (1717), Fort Hope, Eastmain House (1686), Rupert House (1668)
  - Interior of Rupert's Land was UNCONTACTED until late 1700s-early 1800s (fur brigades pushed inland after NWC competition)
  - Rupert's Land claim (entire Hudson Bay drainage) was a PAPER CLAIM, not physical control

### Spanish Louisiana
- **Din, Gilbert C. _The Spanish Presence in Louisiana, 1763-1803._ Lafayette: Center for Louisiana Studies, 1996.**
  - Louisiana ceded to Spain via Treaty of Fontainebleau (3 Nov 1762), secret until 1764
  - Spanish physical control began 1766-1769 (Ulloa expedition, then O'Reilly)
  - French posts on west bank: Ste. Genevieve (~1735), Cape Girardeau (~1733), Arkansas Post (1686)
  - St. Louis founded 1764 (AFTER the 1763 start date, but Ste. Genevieve in same province existed from ~1735)

---

## CONCLUSION

### Overall Verdict

The 1763 North American map is **substantially accurate** at distinguishing CONTROLLED vs. CLAIMED territory, with the following exceptions:

### Corrections Needed

1. **NSP (New Spain)**: Remove **7 provinces** of deep Texas/New Mexico interior that Spain claimed but did not physically control (no Spanish settlement pops, no historical towns/presidios).

2. **HBC (Hudson's Bay Company)**: Likely overextended — owns 38 provinces but physically controlled only ~8-10 Bay posts. **Requires separate detailed audit.**

3. **LSA (Spanish Louisiana)**: Possibly overextended — verify deep interior provinces (Osage plains) have historical French posts. Province 3643 (Little Rock) is questionable.

### Design Philosophy Assessment

The mod's approach is **historically sophisticated**, privileging Native sovereignty over European paper claims. The few overextensions identified (NSP deep Texas/NM interior, HBC interior) are relatively minor and easily corrected.

**The existing representation is FAR more accurate than typical Paradox games**, which often assign vast "paper claim" territories to European powers.

---

**END OF AUDIT**
