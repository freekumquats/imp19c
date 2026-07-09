# 1763 DELTA Asia — Exact Edit Plan
**Scope**: South Asia, East Asia, Southeast Asia mainland/insular  
**Excludes**: Qing tributary tree lines 824-884 (unchanged)  
**Date**: 2026-07-08  

---

## EXECUTIVE SUMMARY

**MASSIVE SURGERY REQUIRED.** The 1763→1815 delta for Asia is the largest single regional transformation in the world map:

1. **India**: EIC must be STRIPPED of territorial raj (Bengal, Bihar, Orissa, Madras territories) and redistributed to independent Maratha confederacy (with sub-houses), Mysore (Hyder Ali rising), Hyderabad, Awadh, Bengal Nawab (Mir Qasim). EIC retains only coastal forts (Calcutta, Madras, Bombay island). **Estimated 200+ province ownership changes.**

2. **Vietnam**: Currently unified VIE must be SPLIT into TWO regimes — Trịnh north (Đàng Ngoài) and Nguyễn south (Đàng Trong) with puppet Lê emperor. Research confirms division viable but requires new tag or dual-ruler system. **Feasibility: MEDIUM.**

3. **Siam**: Capital Bangkok (1815) must revert to Ayutthaya (1763, pre-1767 sack). Ruler swap: Rama II → Ekkathat. Dynasty swap: Chakri → Ayutthaya. **10+ edits.**

4. **Burma**: Ruler swap: 1815 Konbaung peak → 1763 Hsinbyushin (just acceded Jan 1763). Capital Ava. **5 edits.**

5. **Japan**: Ruler swap: TKG shogun from late-Edo to 1763 Tokugawa Ieharu (age 17). Empress Go-Sakuramachi as co-ruler/emperor. **8-10 edits.**

6. **Korea**: Ruler swap: 1815 KOR ruler → 1763 Yeongjo (Yi Geum, age 69). **3 edits.**

**HIGH RISK**: India province redistribution (EIC→ many tags) is prone to province-ID errors, dependency loop bugs, and balance breakage. Vietnam split is unproven engine capability (see Section V Limitations).

---

## SECTION I: SOUTH ASIA DELTA

### A. EIC TERRITORIAL STRIPPING (1815→1763)

**1815 STATE**: EIC (line 39844) holds vast territorial raj:
- Bengal, Bihar, Orissa (entire Gangetic plain)
- Madras Presidency (Coromandel coast, Northern Circars)
- Bombay Presidency (expanding Maharashtra)
- Subsidiary alliances with Hyderabad, Awadh, Mysore (not modeled as subjects but as independent weaklings)

**1763 TARGET**: EIC reduced to THREE COASTAL FORTS ONLY:
- **Calcutta/Fort William** (Bengal Presidency, 1 province)
- **Madras/Fort St. George** (Coromandel coast, 1 province)
- **Bombay island** (1 province only, NOT Presidency hinterland)

**WHAT EIC MUST LOSE** (redistribute to independent Indian states):
1. **Bengal + Bihar + Orissa** → to **Bengal Nawab** (Mir Qasim, awaiting Buxar 1764)
2. **Awadh region** → to **AWA** (already exists line 38392, expand territory)
3. **Madras Presidency hinterland** → to **Carnatic Nawab** (Muhammad Ali, EIC puppet but NOT EIC-owned)
4. **Maharashtra EIC holdings** → to **MRT** (Maratha Peshwa, line 38529)
5. **Deccan/Mysore region** → to **MYS** (Hyder Ali, line 40814, expand)
6. **Northern Circars** → to **HYD** (Nizam, line 39784, leased to EIC 1759 but nominally Nizam's)

### B. MARATHA EXPANSION + SUB-HOUSE ACTIVATION

**1815 STATE**: MRT (line 38529) exists as monolithic tag with 18 provinces.

**1763 TARGET**: MRT as **loose confederacy** with 4-5 great house **semi-independent** tags:
- **MRT** (Peshwa Madhavrao I at Pune) = confederacy head, reduced direct territory
- **GWA** (Gwalior, Scindia) — line 528 in countries.txt, EXISTS, needs country block added to 00_default.txt
- **INR** (Indore, Holkar) — line 530, EXISTS, needs country block
- **BRD** (Baroda, Gaekwad) — line 518, EXISTS, needs country block
- **NAG** (Nagpur, Bhonsle) — line 551, EXISTS, needs country block

**TECHNICAL IMPLEMENTATION**:
1. **Add country blocks** for GWA/INR/BRD/NAG to 00_default.txt (after MRT block, around line 38567).
2. **Redistribute MRT provinces**:
   - **GWA**: Gwalior, Malwa, northern Deccan (provinces from MRT own_control_core list + from EIC)
   - **INR**: Indore, Malwa (overlap with GWA, historically contested)
   - **BRD**: Gujarat, Baroda (provinces 1340, 4776, 5635 from MRT list + Gujarat from EIC)
   - **NAG**: Nagpur, Berar, Orissa raiding rights (eastern provinces from MRT list)
3. **Subject relationships**: 
   - Research shows confederacy = NOMINAL Peshwa overlordship, NOT strict vassals.
   - **DECISION**: Do NOT model as dependencies (risk: loop bugs, integration mechanics unwanted).
   - Instead: MRT + 4 houses all **independent**, alliance = { first = MRT second = GWA } pattern (non-subject alliance).

**LINE EDITS**:
- **Line 38543-38562** (MRT own_control_core): REMOVE provinces for GWA/INR/BRD/NAG.
- **After line 38566**: INSERT 4 new country blocks (GWA/INR/BRD/NAG) with:
  - government = absolute_duchy or feudatory_kingdom
  - primary_culture = marathi
  - religion = hindu
  - capital = [Gwalior, Indore, Baroda, Nagpur respectively]
  - own_control_core = [reassigned provinces]

### C. INDIA RULER SWAPS (1763 vs 1815)

| Tag | Line | 1815 Ruler (CURRENT) | 1763 Ruler (TARGET) | Capital Change? |
|-----|------|---------------------|---------------------|-----------------|
| **AWA** | 38392 | (unknown) | Shuja-ud-Daula (r. 1754-1775) | Faizabad (no change if cap = 1108) |
| **HYD** | 39784 | Asaf Jah (family 27) | Asaf Jah II (r. 1762-1803, NEW ruler, just installed 1762) | Hyderabad (no change) |
| **MYS** | 40814 | (unknown, family 28) | Hyder Ali (r. 1761-1782, de facto dictator); Nanjaraja Wodeyar (nominal king) | Seringapatam (capital 695, no change) |
| **MRT** | 38529 | (unknown) | Madhavrao I (Peshwa, b. 1745, r. 1761-1772, age 18 in 1763) | Pune (capital 9840, no change) |
| **BEN** | 46668 | (DIFFERENT BEN — this is BENIN in West Africa, NOT Bengal) | N/A | N/A |

**BENGAL NAWAB**: Does NOT exist as tag in 1815 (EIC absorbed). **MUST CREATE NEW TAG** for 1763.
- **Tag choice**: Research shows "Bengal" as Indian state is tricky (line 46668 = Benin in West Africa).
- **Option 1**: Use **BEN** collision (move Benin to different tag? Risky).
- **Option 2**: Use **BNG** or **BWB** (Bengal/Bangla) as new tag.
- **DECISION**: Flag as **LIMITATION** — tag collision risk.

### D. MYSORE 1763: HYDER ALI PUPPET STRUCTURE

**Historical reality**: Hyder Ali seized power 1761, kept Wodeyar king as puppet.

**Engine limitation**: Imperator has NO "puppet king" mechanic (unlike co-ruler or governor).

**WORKAROUND**:
1. **MYS ruler** = Hyder Ali (create new character, Muslim, military traits, low legitimacy).
2. **Co-ruler or consort slot**: Wodeyar king as ceremonial (if co-ruler mechanic available).
3. **Alternative**: Wodeyar as imprisoned/powerless character in MYS court (not ruler).

**LINE EDITS**:
- **Line 40814-40836** (MYS block): change ruler to Hyder Ali character reference.
- Add new character definition for Hyder Ali (setup/characters/).

### E. SIKH MISLS — 1763 EMERGING CONFEDERACY

**1815 STATE**: Likely exists as unified Sikh Empire (Ranjit Singh, 1801-1839) or Punjab tags.

**1763 TARGET**: **12 Sikh misls** = mobile guerilla bands, NO fixed state yet.

**Research verdict**: "Misls = mobile warrior bands, controlling villages/towns, paying no tribute."

**TECHNICAL FEASIBILITY**: 
- Imperator has NO "mobile tribal confederacy without fixed territory" mechanic.
- Closest = tribal client_state or feudatory with small territory + raiding rights.

**DECISION**: 
- **LIMITATION**: Full misl system unfeasible.
- **COMPROMISE**: Model 2-3 major misls as **client_state** tags with small Punjab provinces:
  - **Sukerchakia** (future Ranjit Singh's house, minor 1763)
  - **Ahluwalia** (Jassa Singh Ahluwalia, rising leader)
  - **Bhangi** (controlling Amritsar, Lahore)
- **Overlord**: Durrani Empire (AFG, line 45784) as nominal overlord (dependency = { first = AFG second = [misl] subject_type = client_state }).

**NEW TAGS REQUIRED**: 
- Check if Sikh tags exist in countries.txt (grep -n "sikh\|misl\|suker\|ahluw\|bhangi" setup/countries/countries.txt).
- If not: **FLAG AS LIMITATION** — requires new tag creation.

### F. OTHER INDIA DELTAS

**Rajput states**: Already exist (JAI = Jaipur, check line numbers). 
- **Ruler swap**: 1815 rulers → 1763 rulers (Sawai Madhav Singh II for Jaipur, Vijay Singh for Jodhpur, Ari Singh II for Udaipur).

**Travancore (TRV)**: Already exists (line 39822).
- **Ruler swap**: 1815 → 1763 Dharma Raja (Karthika Thirunal Rama Varma, r. 1758-1798).

**Portuguese/Dutch/Danish holdings**: Minor adjustments.
- **Dutch Ceylon**: VOC coastal strip + **Kandy kingdom independent** (check if KND tag exists line 538).

---

## SECTION II: EAST ASIA DELTA

### A. KOREA (KOR)

**LINE**: 44675-44692

**1815 STATE**: 
- Ruler: likely Sunjo (r. 1800-1834) or family placeholder
- Capital: 2429 (Hanseong/Seoul, correct)
- Tributary to CHI: line 876 dependency = { first = CHI second = KOR subject_type = tributary } — **UNCHANGED**

**1763 TARGET**:
- Ruler: **Yeongjo** (Yi Geum, 이금 / 李昑, r. 1724-1776, age 69 in 1763)
- Capital: 2429 (Hanseong, no change)
- Crown Prince: **Yi San** (future Jeongjo, age 11 in 1763, after Sado execution 1762)

**EDITS**:
1. **Line 44680** (family = 10): Check if this is Joseon Yi royal family. If placeholder, replace with correct Yi Geum character reference.
2. **Add co-ruler or heir**: Yi San as crown prince/heir (if mechanic available).
3. **Government**: line 44676 = absolute_kingdom (correct for 1763 Joseon).

**CHARACTER CREATION**:
- Create Yeongjo character (setup/characters/korea.txt or equivalent):
  - Name: Yi Geum / 李昑
  - Birth: 1694
  - Traits: administrative skill (Tangpyeong reforms), longevity
  - Religion: confucianism
  - Culture: korean

### B. JAPAN (TKG → JPN issue)

**LINE**: 44056-44081

**1815 STATE**:
- Tag: **TKG** (Tokugawa, line 44056)
- Ruler: family 1, family 2 (placeholder)
- Government: hereditary_dictatorship (correct for shogunate)
- Capital: 3684 (Edo, correct)

**1763 TARGET**:
- Tag: **TKG** (Tokugawa shogunate, 1603-1868)
- Shogun: **Tokugawa Ieharu** (徳川家治, 10th shogun, r. 1760-1786, age 17 in 1763)
- Emperor: **Go-Sakuramachi** (後桜町天皇, r. 1762-1771, empress regnant, ceremonial)
- Capital: 3684 (Edo, no change)

**JPN TAG**: Line 504 in countries.txt = JPN = "setup/countries/japan/japan.txt" — this is **Meiji Japan** (formed at Restoration 1868, arc #94). **NOT USED** in 1763/1815 starts.

**EDITS**:
1. **Line 44058** (family = 1, family = 2): Replace with Tokugawa Ieharu character reference.
2. **Add co-ruler**: Go-Sakuramachi as emperor (co_ruler or consort slot if available; she's empress regnant but powerless).
3. **Government**: hereditary_dictatorship (line 44059, correct).
4. **Provinces**: line 44068-44077 (own_control_core) — verify Hokkaido (line 44070 = 450 7367 4732 12730) is correct for 1763 (Matsumae domain controlled Hokkaido, subordinate to Tokugawa).

**RYUKYU (RYU)**: Line 494 in countries.txt, check setup block.
- **1815 STATE**: Likely independent or tributary to CHI.
- **1763 TARGET**: **Dual tributary** to CHI + TKG (Satsuma control). Line 877 dependency = { first = CHI second = RYU subject_type = tributary } — ADD second dependency to TKG (nested subject: CHI→RYU←TKG or TKG→RYU as client, CHI→RYU as tributary).
- **Ruler**: Shō Boku (尚穆, r. 1752-1794).

**CHARACTER CREATION**:
- Tokugawa Ieharu (setup/characters/japan.txt):
  - Name: Tokugawa Ieharu / 徳川家治
  - Birth: 1737
  - Traits: young (age 17), administrative (Tanuma Okitsugu regent)
  - Religion: shinto
  - Culture: japanese
- Go-Sakuramachi:
  - Name: Go-Sakuramachi / 後桜町天皇
  - Birth: 1740
  - Gender: female (empress regnant)
  - Traits: ceremonial, religious
  - Religion: shinto
  - Culture: japanese

---

## SECTION III: SOUTHEAST ASIA MAINLAND DELTA

### A. VIETNAM SPLIT (VIE → TRỊNH + NGUYỄN)

**LINE**: 43784-43802

**1815 STATE**:
- Tag: **VIE** (unified Nguyễn dynasty, 1802)
- Ruler: family 24 (likely Gia Long or successor)
- Capital: 2593 (Huế, correct for Nguyễn)
- Government: imperial_monarchy

**1763 TARGET**: **DIVIDED**:
1. **Trịnh Lords** (north, Đàng Ngoài):
   - Territory: north of Gianh River (Tonkin, Red River Delta)
   - Capital: Thăng Long (Hanoi)
   - Ruler: Trịnh Sâm (r. 1762-1782, just acceded 1762)
   - Puppet: Lê Hiển Tông (emperor, ceremonial)
2. **Nguyễn Lords** (south, Đàng Trong):
   - Territory: south of Gianh River to Mekong Delta
   - Capital: Phú Xuân (Huế) — line 2593 (current VIE capital)
   - Ruler: Nguyễn Phúc Khoát (r. 1738-1765)

**TAG OPTIONS**:
- **Option 1**: Use **VIE** for Nguyễn (south), create **NEW TAG** for Trịnh (north).
  - Precedent: Research file calls north "Trịnh" and south "Nguyễn" but both are under nominal Lê dynasty.
  - **Proposed tag for Trịnh north**: Check if **LVI** (Lê Vietnam) or **TRI** or **TRH** exists in countries.txt.
- **Option 2**: Keep **VIE** as Lê puppet emperor tag (ceremonial), create TWO new tags for Trịnh + Nguyễn as co-regents.
  - **COMPLEXITY**: Three-way split (Lê puppet + Trịnh real power north + Nguyễn real power south) is unprecedented in setup.

**PROVINCE SPLIT** (Gianh River line):
- **Trịnh north**: provinces from VIE own_control_core (line 43795-43797) north of Gianh River.
  - Research: "north of Gianh River" = Tonkin region.
  - **ACTION**: Grep map_data/areas.txt for "tonkin\|hanoi\|red_river" to identify area IDs, then grep 00_default.txt for those area province IDs.
- **Nguyễn south**: provinces south of Gianh River (including Huế capital 2593, Mekong Delta).

**FEASIBILITY CHECK**:
- **RISK**: Province split by river = manual province-by-province sorting.
- **RISK**: No existing tag for Trịnh north — requires new tag creation + character files.
- **LIMITATION**: Lê puppet emperor mechanics unclear (co-ruler? imprisoned character?).

**DECISION**: 
- **SIMPLIFICATION**: Model as TWO independent tags (Trịnh north, Nguyễn south), NO Lê puppet tag (engine limitation).
- **VIE** tag = Nguyễn south (keep current capital Huế).
- **NEW TAG** for Trịnh north (check tag availability).

**EDITS**:
1. **Line 43795-43797** (VIE own_control_core): SPLIT provinces into north (Trịnh) and south (Nguyễn).
2. **Create new country block** for Trịnh north (after VIE block, line ~43802):
   - Tag: TBD (TRI or TRH or new)
   - government = imperial_monarchy or absolute_kingdom
   - primary_culture = vietnamese
   - religion = confucianism
   - capital = [Hanoi province ID, grep for "hanoi\|thang_long"]
   - own_control_core = [northern provinces from VIE list]
3. **Line 43790** (VIE ruler family 24): Change to Nguyễn Phúc Khoát character reference.

**CHARACTER CREATION**:
- Trịnh Sâm:
  - Name: Trịnh Sâm / 鄭森
  - Birth: ~1740s
  - Traits: military, authoritarian
  - Religion: confucianism
  - Culture: vietnamese
- Nguyễn Phúc Khoát:
  - Name: Nguyễn Phúc Khoát / 阮福濶
  - Birth: ~1714
  - Traits: expansionist, naval
  - Religion: confucianism
  - Culture: vietnamese
- Lê Hiển Tông (if modeled):
  - Name: Lê Hiển Tông / 黎顯宗
  - Birth: ~1717
  - Traits: powerless, ceremonial
  - Religion: confucianism
  - Culture: vietnamese

### B. SIAM (SIA)

**LINE**: 43473-43491

**1815 STATE**:
- Tag: **SIA**
- Ruler: family 23 (likely Rama II, Chakri dynasty)
- Capital: 8873 (Bangkok, Chakri capital from 1782)
- Government: absolute_kingdom

**1763 TARGET**:
- Tag: **SIA** (Ayutthaya kingdom, pre-1767 sack)
- Ruler: **Ekkathat** (เอกทัศน์, r. 1758-1767, weak rule)
- Capital: **Ayutthaya** (NOT Bangkok) — **MUST CHANGE** capital from 8873 to Ayutthaya province ID.
- Government: absolute_kingdom (no change)

**CAPITAL CHANGE**:
- **ACTION**: Grep map_data for "ayutthaya" province ID.
- **LINE 43479**: Change capital = 8873 (Bangkok) → capital = [Ayutthaya province ID].

**EDITS**:
1. **Line 43478** (family = 23): Replace with Ekkathat character reference (Ayutthaya dynasty, NOT Chakri).
2. **Line 43479**: Change capital to Ayutthaya province.
3. **Provinces** (line 43484-43486): Verify 1763 Ayutthaya extent vs 1815 Bangkok Siam (likely similar, no major territorial change).

**CHARACTER CREATION**:
- Ekkathat:
  - Name: Ekkathat / เอกทัศน์
  - Birth: ~1710
  - Traits: weak administrator, factionalism, pre-Burmese-sack stress
  - Religion: theravada
  - Culture: thai

### C. BURMA (BUR)

**LINE**: 43666-43686

**1815 STATE**:
- Tag: **BUR**
- Ruler: (unknown, likely Bodawpaya r. 1782-1819 or successor)
- Capital: 7675 (likely Ava or Rangoon)
- Government: absolute_kingdom

**1763 TARGET**:
- Tag: **BUR** (Konbaung dynasty, founded 1752)
- Ruler: **Hsinbyushin** (ဆင်ဘြူရှင်, r. 1763-1776, just acceded Jan 1763)
- Capital: **Ava** (Inwa, line 43672 = 7675 likely Ava? Verify)
- Government: absolute_kingdom (no change)

**EDITS**:
1. **Line 43667-43671**: Replace ruler with Hsinbyushin character reference.
2. **Line 43672**: Verify capital 7675 = Ava (if not, change to Ava province ID).
3. **Provinces** (line 43677-43682): Verify 1763 Konbaung extent (just unified Burma 1757, expanding; 1815 = peak extent, may need to trim Arakan/Assam/Manipur if added by 1815).

**CHARACTER CREATION**:
- Hsinbyushin:
  - Name: Hsinbyushin / ဆင်ဘြူရှင်
  - Birth: 1736
  - Traits: military (aggressive expansionist, Siam invasion 1765-67, Qing war 1765-69)
  - Religion: theravada
  - Culture: burmese

### D. CAMBODIA (CBI)

**LINE**: Check setup for CBI block (grep -n "^[[:space:]]*CBI = {").

**1815 STATE**: Likely exists as Siamese or Vietnamese puppet.

**1763 TARGET**:
- Ruler: **Outey II** (r. 1762-1779, just installed 1762)
- Capital: **Udong** (check province ID)
- Status: **Contested** between Ayutthaya Siam (west) and Nguyễn Vietnam (east).

**EDITS**:
- Ruler swap to Outey II.
- **Dependency**: 1763 = probably Siamese client_state or tributary (dependency = { first = SIA second = CBI subject_type = tributary }).

### E. LAO KINGDOMS (LPR, VIN, CPK)

**TAGS**: 
- LPR (Luang Prabang, line 417 in countries.txt)
- VIN (Vientiane, line 425)
- CPK (Champasak, line 414)

**1763 STATE**: All exist as independent but tributary to Siam or Burma.

**EDITS**:
- **Ruler swaps**:
  - LPR: Sotika-Koumane (r. 1753-1771)
  - VIN: Ong Boun (r. 1760-1778)
  - CPK: Sayakuman (r. 1738-1791)
- **Dependencies**: 
  - LPR: Burmese tributary (dependency = { first = BUR second = LPR subject_type = tributary })
  - VIN: Siamese tributary (dependency = { first = SIA second = VIN subject_type = tributary })
  - CPK: Siamese tributary (dependency = { first = SIA second = CPK subject_type = tributary })

---

## SECTION IV: SOUTHEAST ASIA INSULAR DELTA

### A. DUTCH EAST INDIES (DEI)

**LINE**: 42743 (check for DEI block)

**1815 STATE**: 
- VOC dissolved 1799 → Dutch government control (Dutch East Indies).
- Java: divided sultanates (Surakarta, Yogyakarta).
- Moluccas: spice monopoly.

**1763 TARGET**:
- **VOC corporate rule** (NOT Dutch state).
- **Batavia** (capital 3684? verify Jakarta province ID).
- Java: same divided sultanates (Pakubuwono III at Surakarta, Hamengkubuwono I at Yogyakarta).

**EDITS**:
- **Government**: Change from colonial_government or state_colony (1815) to megacorporation or trade_company (1763).
- **Ruler**: VOC Governor-General (1763 = check who held office Feb 1763).

### B. SPANISH PHILIPPINES (PHI)

**LINE**: 48835

**1815 STATE**:
- Tag: **PHI**
- Spanish Captaincy General
- Capital: Manila
- Galleon trade ended 1815-21 (Mexican independence)

**1763 TARGET**:
- **Manila under BRITISH OCCUPATION** (Oct 1762 - 1764).
- Acting Spanish Governor: Simón de Anda y Salazar (resistance government at Bulacan).
- Treaty of Paris signed 10 Feb 1763 (6 days before 16 Feb 1763 date) → return to Spain imminent but not yet executed.

**FEASIBILITY**: 
- Model British occupation = GBR holds Manila province + PHI as Spanish rump (Bulacan)?
- **COMPLEXITY**: Temporary occupation + imminent handover is hard to model statically.

**DECISION**:
- **SIMPLIFICATION**: Show PHI as **Spanish** (as if post-Treaty return), note British occupation as recent in event text.
- **Ruler**: Simón de Anda y Salazar (acting governor).

**EDITS**:
- Ruler swap.
- No territorial change (keep Manila as PHI capital).

### C. BRUNEI, ACEH, JOHOR-RIAU, etc.

**Minor sultanates**: Likely exist in 1815 setup already.

**EDITS**: Ruler swaps only:
- **Brunei (BRU)**: Sultan Muhammad Tajuddin (r. 1750-1778)
- **Aceh (ACH)**: Sultan Badruddin (r. 1760-1764)
- **Johor-Riau (JHR)**: Abdul Jalil Riayat Shah IV (r. 1760-1761/?, Bugis-controlled, murky succession)

---

## SECTION V: LIMITATIONS

### 1. **NEW TAG REQUIREMENT: BENGAL NAWAB**
- **Issue**: Bengal in 1763 is independent Nawab (Mir Qasim), NOT EIC territory. No tag exists in 1815 for Bengal as state (line 46668 BEN = Benin, West Africa).
- **Options**: 
  - (A) Create **BNG** or **BWB** tag (Bengal/Bangla).
  - (B) Reassign BEN from Benin to Bengal (requires moving Benin to different tag — **RISKY**, breaks dependencies).
- **Recommendation**: Flag for user decision.

### 2. **NEW TAG REQUIREMENT: VIETNAM TRỊNH NORTH**
- **Issue**: No tag exists for Trịnh-ruled north Vietnam (Đàng Ngoài). VIE tag used for unified 1815 Nguyễn dynasty.
- **Options**: Create **TRI** or **TRH** or **LVI** tag for Trịnh.
- **Recommendation**: Use **TRI** (if available in countries.txt tag pool).

### 3. **NEW TAGS REQUIREMENT: SIKH MISLS**
- **Issue**: 12 Sikh misls = no tags exist. Modeling full confederacy unfeasible.
- **Compromise**: Model 2-3 major misls (Sukerchakia, Ahluwalia, Bhangi) as small client_state tags under AFG (Durrani).
- **Tag availability**: Check if **SKH** (Sukerchakia?), **AHL** (Ahluwalia?), **BNG** (Bhangi?) exist or can be created.

### 4. **PUPPET MECHANICS: MYSORE WODEYAR + LÊ EMPEROR**
- **Issue**: Imperator has no "puppet ruler" mechanic (unlike co-ruler or governor).
- **Workaround**: 
  - Mysore: Hyder Ali as ruler, Wodeyar as imprisoned/courtier character (not co-ruler).
  - Lê emperor: Omit entirely (simplify Vietnam to Trịnh north + Nguyễn south only).

### 5. **VIETNAM PROVINCE SPLIT BY GIANH RIVER**
- **Issue**: No automated way to sort provinces by river boundary. Requires manual province-by-province review of map_data + own_control_core lists.
- **Risk**: Province assignment errors (assigning south provinces to north or vice versa).

### 6. **SIKH MISLS AS MOBILE CONFEDERACY**
- **Issue**: Misls = "mobile warrior bands, no fixed borders" — Imperator has no mechanic for this (tribal tags need fixed provinces).
- **Compromise**: Small fixed territories in Punjab, modeled as client_state.

### 7. **MARATHA CONFEDERACY AS NON-SUBJECT ALLIANCE**
- **Issue**: Research shows Maratha houses = semi-autonomous, NOT strict vassals. But modeling 5 independent tags + alliance may break confederacy unity (no shared wars, no Peshwa authority).
- **Alternative**: Model as feudatory subjects to MRT (risk: integration mechanics may fire unwanted).
- **Recommendation**: Test both (independent + alliance vs feudatory) and choose based on gameplay.

### 8. **PHILIPPINES BRITISH OCCUPATION**
- **Issue**: Manila under GBR occupation Oct 1762 - 1764, but 16 Feb 1763 = 4 months into occupation, Treaty of Paris just signed (return imminent). Hard to model temporary occupation statically.
- **Simplification**: Show as Spanish (post-return), note British occupation in event/tooltip.

---

## SECTION VI: RISKS

### 1. **PROVINCE REASSIGNMENT SCALE**
- **Scope**: Estimated **200+ provinces** must change ownership (EIC → Bengal, Mysore, Hyderabad, Awadh, Maratha houses).
- **Risk**: Province ID typos, missing provinces, double-assigned provinces → boot crash or map holes.
- **Mitigation**: Systematic audit via grep for each area/region; boot-test after EACH tag's provinces added.

### 2. **SUBJECT DEPENDENCY LOOPS**
- **Risk**: Creating nested subjects (e.g., AFG → Sikh misls, or MRT → Maratha houses) may create dependency loops if provinces overlap or if integration mechanics fire.
- **Precedent**: Line 863 shows ILI → XNG → [KML via line 854] (nested 3-level), line 867 ULS → KBD (nested under CHI → ULS line 866). So nested subjects ARE viable.
- **Mitigation**: Audit all new dependencies for loops; check subject_type = client_state or tributary (not autonomous_governorship, which triggers integration).

### 3. **CHARACTER BIRTH DATES**
- **Risk**: Creating characters with birth dates pre-1763 but used in 1815 start = character age inconsistency (e.g., Yeongjo b. 1694 would be 121 years old in 1815, dead).
- **Mitigation**: Separate character files for 1763 vs 1815 bookmarks, OR use conditional character spawn (if bookmark = 1763).

### 4. **CAPITAL CHANGES**
- **Risk**: Changing SIA capital from Bangkok (8873) to Ayutthaya requires verifying Ayutthaya province ID exists + has correct area/region. If Ayutthaya province doesn't exist in map_data, fallback = manual province creation (OUT OF SCOPE).
- **Mitigation**: Grep map_data/areas.txt for "ayutthaya" BEFORE editing capital line.

### 5. **MARATHA SUB-HOUSE BALANCE**
- **Risk**: Splitting MRT into 5 tags (Peshwa + 4 houses) may make each individually too weak vs EIC/Mughals, breaking historical balance (Marathas were dominant 1760s-1790s).
- **Mitigation**: Ensure combined MRT+GWA+INR+BRD+NAG province count ≥ 1815 MRT (18 provinces line 38543-38562) + provinces stripped from EIC (60+?).

### 6. **VIETNAM TRỊNH-NGUYỄN SPLIT BALANCE**
- **Risk**: Splitting VIE into north (Trịnh) and south (Nguyễn) with equal province counts may not reflect reality (north = Red River Delta = dense pop, south = Mekong Delta = colonization frontier). If equal provinces, north should be economically stronger.
- **Mitigation**: Weight province quality (urban/trade vs rural) in split, OR accept rough 50/50 split as limitation.

### 7. **TAG COLLISIONS**
- **Risk**: Creating new tags (Bengal Nawab, Trịnh north, Sikh misls) may collide with existing tags in countries.txt (e.g., BNG may already exist for Bangladesh/Bangl/Bhopal abbreviation).
- **Mitigation**: Full grep of countries.txt for proposed tags BEFORE use; if collision, choose alternative tag (e.g., BWB, TRI, SKH).

---

## APPENDIX: LINE-BY-LINE EDIT CHECKLIST

### SOUTH ASIA

#### 1. EIC (line 39844-39900+)
- [ ] **Strip territorial provinces** from own_control_core (line 39844+):
  - [ ] Remove Bengal provinces (reassign to new Bengal Nawab tag)
  - [ ] Remove Bihar provinces (reassign to Bengal Nawab)
  - [ ] Remove Orissa provinces (reassign to Bengal Nawab)
  - [ ] Remove Madras hinterland provinces (reassign to Carnatic Nawab or EIC keeps as protectorate?)
  - [ ] Remove Bombay hinterland provinces (keep Bombay island only)
  - [ ] Remove Northern Circars (reassign to HYD)
- [ ] **Verify EIC retains only 3 provinces**: Calcutta (6219? verify), Madras (province ID?), Bombay island (province ID?)
- [ ] **Government/stance**: No change (megacorporation line 39845, correct)

#### 2. MRT (line 38529-38566)
- [ ] **Ruler swap**: Line 38534 family = 11, family = 29 → replace with Madhavrao I character reference
- [ ] **Province reduction**: Line 38543-38562 own_control_core → REMOVE provinces for GWA/INR/BRD/NAG (keep ~5-8 core Peshwa provinces around Pune)
- [ ] **Capital**: Line 38539 capital = 9840 (Pune) — no change

#### 3. GWA (NEW BLOCK, insert after line 38566)
- [ ] **Create country block**:
  ```
  GWA = {
      government = absolute_duchy
      diplomatic_stance = appeasement_stance
      primary_culture = marathi
      religion = hindu
      capital = [Gwalior province ID]
      own_control_core = { [Gwalior, Malwa, northern Deccan provinces] }
  }
  ```
- [ ] **Ruler**: Mahadji Scindia (b. 1730, wounded at Panipat 1761, recovering 1763)
- [ ] **Alliance**: After all country blocks, add alliance = { first = MRT second = GWA }

#### 4. INR (NEW BLOCK, insert after GWA)
- [ ] **Create country block** (similar to GWA):
  - Capital: Indore
  - Ruler: Malhar Rao Holkar I (d. 1766, alive 1763)
  - Provinces: Malwa, Indore region
- [ ] **Alliance**: alliance = { first = MRT second = INR }

#### 5. BRD (NEW BLOCK, insert after INR)
- [ ] **Create country block**:
  - Capital: Baroda
  - Ruler: Damaji Gaekwad (r. 1740s-1768)
  - Provinces: Gujarat, Baroda (provinces 1340, 4776, 5635 from MRT + Gujarat from EIC)
- [ ] **Alliance**: alliance = { first = MRT second = BRD }

#### 6. NAG (NEW BLOCK, insert after BRD)
- [ ] **Create country block**:
  - Capital: Nagpur
  - Ruler: Janoji Bhonsle (r. 1755-1772)
  - Provinces: Nagpur, Berar, eastern confederacy
- [ ] **Alliance**: alliance = { first = MRT second = NAG }

#### 7. AWA (line 38392-38416)
- [ ] **Ruler swap**: Line 38397 family = 59 → replace with Shuja-ud-Daula character reference
- [ ] **Province expansion**: Line 38403-38412 own_control_core → ADD Awadh region provinces (currently maybe under EIC or Mughals?)
- [ ] **Capital**: Line 38399 capital = 1108 → verify Faizabad (or Lucknow?)

#### 8. HYD (line 39784-39820)
- [ ] **Ruler swap**: Line 39789 family = 27 → replace with Asaf Jah II character reference (r. 1762-1803, new ruler 1762)
- [ ] **Province expansion**: Line 39794-39816 own_control_core → ADD Northern Circars provinces (currently under EIC)
- [ ] **Capital**: Line 39790 capital = 4316 (Hyderabad) — no change

#### 9. MYS (line 40814-40837)
- [ ] **Ruler swap**: Line 40819 family = 28 → replace with Hyder Ali character reference (de facto ruler 1761-1782)
- [ ] **Province expansion**: Line 40824-40833 own_control_core → ADD Mysore expansion territories (currently under EIC or Carnatic?)
- [ ] **Capital**: Line 40820 capital = 695 (Seringapatam) — no change
- [ ] **Government**: Line 40815 absolute_duchy — no change (Wodeyar nominal king, Hyder Ali dictator)

#### 10. BENGAL NAWAB (NEW BLOCK, NEW TAG)
- [ ] **Resolve tag**: Check if BNG/BWB available, or resolve BEN (line 46668) collision
- [ ] **Create country block**:
  ```
  BNG = {  # Or chosen tag
      government = absolute_duchy
      diplomatic_stance = appeasement_stance
      primary_culture = bengali
      religion = sunni  # Mir Qasim = Muslim
      capital = [Munger province ID, Bihar]
      own_control_core = { [Bengal, Bihar, Orissa provinces from EIC] }
  }
  ```
- [ ] **Ruler**: Mir Qasim (r. 1760-1763, until Oct 1763 deposed)
- [ ] **NOTE**: Mir Qasim about to rebel vs EIC (war July 1763, deposed Oct 1763, Buxar 1764) — model as independent 1763, event chain for rebellion?

#### 11. CARNATIC NAWAB (check if exists, or create)
- [ ] **Check for tag**: Grep for Carnatic/TJR (Thanjavur? line 560)/or other Tamil tags
- [ ] **If exists**: Expand provinces (Madras hinterland from EIC)
- [ ] **If not**: Create new tag for Muhammad Ali Khan Walajah (r. 1749-1795, EIC puppet)

#### 12. SIKH MISLS (NEW TAGS, 2-3 only)
- [ ] **Check tag availability**: SKH (Sukerchakia?), AHL (Ahluwalia?), BNG (Bhangi? collision with Bengal?)
- [ ] **Create 2-3 misl blocks** (small client_state tags):
  - Sukerchakia: 1-2 Punjab provinces
  - Ahluwalia: Amritsar region?
  - Bhangi: Lahore region?
- [ ] **Dependencies**: 
  ```
  dependency = { first = AFG second = SKH subject_type = client_state }
  dependency = { first = AFG second = AHL subject_type = client_state }
  dependency = { first = AFG second = BNG subject_type = client_state }  # If tag collision resolved
  ```

#### 13. AFG (line 45784-45808)
- [ ] **No major changes** (Afghanistan 1763 ≈ 1815, Durrani Empire post-Panipat withdrawal)
- [ ] **Verify**: Ruler Ahmad Shah Durrani (r. 1747-1772, alive 1763)

#### 14. RAJPUT STATES (check lines for JAI, etc.)
- [ ] **Jaipur**: Ruler swap to Sawai Madhav Singh II (r. 1750-1768)
- [ ] **Jodhpur**: Ruler swap to Vijay Singh (r. 1752-1793)
- [ ] **Udaipur**: Ruler swap to Ari Singh II (r. 1761-1773, new ruler 1761)

#### 15. TRV (line 39822+)
- [ ] **Ruler swap**: Dharma Raja (Karthika Thirunal Rama Varma, r. 1758-1798)

#### 16. DUTCH CEYLON + KANDY (check for tags)
- [ ] **KND (Kandy)**: Verify exists (line 538 in countries.txt), ruler swap to Kirti Sri Rajasinha (r. 1747-1782)
- [ ] **Dutch Ceylon (VOC)**: Strip interior provinces, assign to KND (Kandy independent interior)

---

### EAST ASIA

#### 17. KOR (line 44675-44692)
- [ ] **Ruler swap**: Line 44680 family = 10 → replace with Yeongjo (Yi Geum) character reference
- [ ] **Heir**: Add Yi San (future Jeongjo, age 11) as heir/crown prince if mechanic available
- [ ] **Capital**: Line 44681 capital = 2429 (Hanseong/Seoul) — no change
- [ ] **Tributary**: Line 876 dependency CHI→KOR — no change

#### 18. TKG (line 44056-44081)
- [ ] **Ruler swap**: Line 44058 family = 1, family = 2 → replace with Tokugawa Ieharu character reference
- [ ] **Co-ruler**: Add Go-Sakuramachi (empress regnant, ceremonial) if co-ruler mechanic available
- [ ] **Capital**: Line 44064 capital = 3684 (Edo) — no change
- [ ] **Hokkaido**: Line 44070 provinces 450 7367 4732 12730 — verify Matsumae domain control correct for 1763

#### 19. RYU (check setup block)
- [ ] **Ruler swap**: Shō Boku (r. 1752-1794)
- [ ] **Dual tributary**: Line 877 CHI→RYU tributary — ADD second dependency TKG→RYU (Satsuma covert control)
  ```
  dependency = { first = CHI second = RYU subject_type = tributary }
  dependency = { first = TKG second = RYU subject_type = client_state }  # Nested subject
  ```

---

### SOUTHEAST ASIA MAINLAND

#### 20. VIE (line 43784-43802) — SPLIT
- [ ] **Rename/reduce VIE** to Nguyễn south only:
  - Line 43790 capital = 2593 (Huế) — no change (Nguyễn capital)
  - Line 43789 family = 24 → replace with Nguyễn Phúc Khoát character reference
  - Line 43795-43797 own_control_core → REMOVE northern provinces (north of Gianh River)
- [ ] **PROVINCE SORT**: 
  - [ ] Grep map_data for Tonkin/Hanoi/Red River area IDs
  - [ ] Grep 43795-43797 province list for those area provinces → move to Trịnh north

#### 21. TRỊNH NORTH (NEW BLOCK, NEW TAG)
- [ ] **Resolve tag**: Use TRI or TRH (check availability)
- [ ] **Create country block**:
  ```
  TRI = {  # Or chosen tag
      government = imperial_monarchy  # Or absolute_kingdom
      diplomatic_stance = appeasement_stance
      primary_culture = vietnamese
      religion = confucianism
      capital = [Hanoi province ID, grep "hanoi\|thang_long"]
      own_control_core = { [Northern provinces from VIE list] }
  }
  ```
- [ ] **Ruler**: Trịnh Sâm (r. 1762-1782, just acceded 1762)
- [ ] **Tributary**: Add dependency = { first = CHI second = TRI subject_type = tributary } ? Or only VIE (Nguyễn) tributary?

#### 22. SIA (line 43473-43491)
- [ ] **Ruler swap**: Line 43478 family = 23 → replace with Ekkathat character reference (Ayutthaya dynasty, NOT Chakri)
- [ ] **Capital change**: Line 43479 capital = 8873 (Bangkok) → capital = [Ayutthaya province ID]
  - [ ] **ACTION FIRST**: Grep map_data/areas.txt for "ayutthaya" province ID
- [ ] **Provinces**: Line 43484-43486 own_control_core — likely no change (Ayutthaya 1763 extent ≈ Bangkok Siam 1815)

#### 23. BUR (line 43666-43686)
- [ ] **Ruler swap**: Line 43667-43671 → replace with Hsinbyushin character reference (r. 1763-1776, just acceded Jan 1763)
- [ ] **Capital**: Line 43672 capital = 7675 — verify Ava (if not, change to Ava province ID)
- [ ] **Provinces**: Line 43677-43682 — verify 1763 Konbaung extent (may need to trim Arakan/Assam/Manipur if those were post-1763 conquests)

#### 24. CBI (CAMBODIA, check setup block)
- [ ] **Ruler swap**: Outey II (r. 1762-1779, just installed 1762)
- [ ] **Capital**: Udong (check province ID)
- [ ] **Dependency**: Add dependency = { first = SIA second = CBI subject_type = tributary } (Siamese influence 1763)

#### 25. LPR (LUANG PRABANG, check setup block)
- [ ] **Ruler swap**: Sotika-Koumane (r. 1753-1771)
- [ ] **Dependency**: Add dependency = { first = BUR second = LPR subject_type = tributary } (Burmese tributary 1763)

#### 26. VIN (VIENTIANE, check setup block)
- [ ] **Ruler swap**: Ong Boun (r. 1760-1778)
- [ ] **Dependency**: Add dependency = { first = SIA second = VIN subject_type = tributary } (Siamese tributary 1763)

#### 27. CPK (CHAMPASAK, check setup block)
- [ ] **Ruler swap**: Sayakuman (r. 1738-1791)
- [ ] **Dependency**: Add dependency = { first = SIA second = CPK subject_type = tributary } (Siamese tributary 1763)

---

### SOUTHEAST ASIA INSULAR

#### 28. DEI (DUTCH EAST INDIES, line 42743?)
- [ ] **Government change**: Line ?+1 government = [colonial_government?] → government = megacorporation or trade_company (VOC corporate rule 1763, NOT state)
- [ ] **Ruler**: VOC Governor-General (check who held office Feb 1763)

#### 29. PHI (PHILIPPINES, line 48835)
- [ ] **Ruler swap**: Simón de Anda y Salazar (acting governor 1762-1764)
- [ ] **Capital**: Manila (no change, even though British-occupied — simplification)
- [ ] **NOTE**: Add event/tooltip noting British occupation Oct 1762 - 1764, Treaty of Paris return imminent

#### 30. BRU (BRUNEI, check setup block)
- [ ] **Ruler swap**: Sultan Muhammad Tajuddin (r. 1750-1778)

#### 31. ACH (ACEH, check setup block)
- [ ] **Ruler swap**: Sultan Badruddin (r. 1760-1764)

#### 32. JHR (JOHOR-RIAU, check setup block)
- [ ] **Ruler swap**: Abdul Jalil Riayat Shah IV (r. 1760-1761/?, Bugis-controlled, succession murky)
- [ ] **NOTE**: Flag as ambiguous (research shows "succession murky 1760s")

---

### CHARACTERS (CREATE NEW FILES OR ADD TO EXISTING)

#### INDIA
- [ ] **Madhavrao I** (Peshwa, MRT)
- [ ] **Mahadji Scindia** (GWA)
- [ ] **Malhar Rao Holkar I** (INR)
- [ ] **Damaji Gaekwad** (BRD)
- [ ] **Janoji Bhonsle** (NAG)
- [ ] **Shuja-ud-Daula** (AWA)
- [ ] **Asaf Jah II** (HYD)
- [ ] **Hyder Ali** (MYS)
- [ ] **Mir Qasim** (Bengal Nawab)
- [ ] **Sawai Madhav Singh II** (Jaipur)
- [ ] **Vijay Singh** (Jodhpur)
- [ ] **Ari Singh II** (Udaipur)
- [ ] **Dharma Raja** (TRV)

#### EAST ASIA
- [ ] **Yeongjo (Yi Geum)** (KOR)
- [ ] **Yi San** (KOR heir, future Jeongjo)
- [ ] **Tokugawa Ieharu** (TKG)
- [ ] **Go-Sakuramachi** (TKG co-ruler/emperor)
- [ ] **Shō Boku** (RYU)

#### SOUTHEAST ASIA
- [ ] **Trịnh Sâm** (Trịnh north)
- [ ] **Nguyễn Phúc Khoát** (VIE/Nguyễn south)
- [ ] **Ekkathat** (SIA)
- [ ] **Hsinbyushin** (BUR)
- [ ] **Outey II** (CBI)
- [ ] **Sotika-Koumane** (LPR)
- [ ] **Ong Boun** (VIN)
- [ ] **Sayakuman** (CPK)
- [ ] **Sultan Muhammad Tajuddin** (BRU)
- [ ] **Sultan Badruddin** (ACH)
- [ ] **Abdul Jalil Riayat Shah IV** (JHR)
- [ ] **Simón de Anda y Salazar** (PHI)

---

### DEPENDENCIES (LINES 800-900 RANGE)

#### ADD NEW:
- [ ] **Line ~885** (after BUR Shan States): Laos dependencies
  ```
  dependency = { first = BUR second = LPR subject_type = tributary }
  dependency = { first = SIA second = VIN subject_type = tributary }
  dependency = { first = SIA second = CPK subject_type = tributary }
  dependency = { first = SIA second = CBI subject_type = tributary }
  ```
- [ ] **Line ~878** (after CHI tributes): RYU dual tributary
  ```
  dependency = { first = CHI second = RYU subject_type = tributary }  # EXISTING line 877
  dependency = { first = TKG second = RYU subject_type = client_state }  # NEW nested
  ```
- [ ] **Line ~885+**: Maratha alliances (if non-subject model chosen)
  ```
  alliance = { first = MRT second = GWA }
  alliance = { first = MRT second = INR }
  alliance = { first = MRT second = BRD }
  alliance = { first = MRT second = NAG }
  ```
- [ ] **Line ~885+**: Sikh misl dependencies (if created)
  ```
  dependency = { first = AFG second = SKH subject_type = client_state }
  dependency = { first = AFG second = AHL subject_type = client_state }
  ```

#### VERIFY EXISTING:
- [ ] **Line 874**: CHI→VIE tributary — should this be CHI→TRI (Trịnh north) + CHI→VIE (Nguyễn south) dual? Or only one tributary?
- [ ] **Line 876**: CHI→KOR tributary — no change
- [ ] **Line 877**: CHI→RYU tributary — ADD TKG→RYU nested (see above)
- [ ] **Line 880-884**: BUR Shan States dependencies — no change

---

### BOOT-TEST MILESTONES

1. [ ] **After India EIC strip + Bengal Nawab creation**: Boot test, check map for holes/double-assignments
2. [ ] **After Maratha sub-house creation (GWA/INR/BRD/NAG)**: Boot test, check confederacy coherence
3. [ ] **After Vietnam split (TRI + VIE)**: Boot test, check province split correctness
4. [ ] **After Siam capital change**: Boot test, verify Ayutthaya province exists + displays correctly
5. [ ] **After all character swaps**: Boot test, check ruler display in-game
6. [ ] **After all dependencies added**: Boot test, check for dependency loops (game will crash if loop exists)
7. [ ] **FINAL AUDIT**: Compare 1763 Asia map to research files for missing/incorrect states

---

## END OF DOCUMENT

**NEXT STEPS** (for user):
1. **Resolve tag collisions**: Decide on Bengal Nawab tag (BNG/BWB?), Trịnh north tag (TRI/TRH?), Sikh misls tags (SKH/AHL?).
2. **Prioritize regions**: Execute in order:
   - Phase 1: EAST ASIA (KOR/TKG/RYU) — smallest delta, lowest risk
   - Phase 2: SOUTHEAST ASIA MAINLAND (SIA/BUR/VIE/Laos) — medium delta, capital changes + Vietnam split
   - Phase 3: SOUTHEAST ASIA INSULAR (PHI/DEI/Brunei/Aceh) — minor ruler swaps only
   - Phase 4: SOUTH ASIA (India) — LARGEST delta, highest risk, save for last
3. **Boot-test after EACH phase** — do NOT accumulate edits across regions (risk: cascading failures).
4. **CHARACTER FILES**: Decide whether to create separate 1763 vs 1815 character files, or use conditional spawn (if bookmark = 1763).

**ESTIMATED EFFORT**:
- East Asia: 2-3 hours (ruler swaps + RYU dual tributary)
- SE Asia mainland: 4-6 hours (Vietnam split + capital changes + Laos dependencies)
- SE Asia insular: 1-2 hours (ruler swaps only)
- South Asia: **12-20 hours** (EIC strip + Maratha sub-houses + Bengal Nawab + province reassignments + dependencies)

**TOTAL**: 20-30 hours for Asia delta (excludes Qing tributary lines 824-884 per scope).
