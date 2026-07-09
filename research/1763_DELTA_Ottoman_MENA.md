# 1763 Bookmark: Ottoman/MENA/Persia Conversion DELTA

**Date:** 2026-07-08  
**Branch:** 1763_bookmark  
**Baseline:** 1815 setup in `setup/main/00_default.txt` lines 777-822  
**Target:** 16 February 1763 (day after Treaty of Hubertusburg)  
**Research Sources:** `research/1763_WORLD_Ottoman_MENA.md`, `research/1763_MENA_independent_states_partial.md`

---

## EXECUTIVE SUMMARY

This document provides the **exact edit plan** to convert the 1815 Ottoman/MENA/Persia baseline to 1763 conditions. The conversion involves:

1. **PERSIA (PR2)**: Dynasty + capital change (Zand @ Shiraz, NOT Qajar @ Tehran)
2. **FIRST SAUDI STATE (DRY)**: NEW independent tag, **present 1763, absent 1815**
3. **OTTOMAN VASSALS**: Most 1815 vassals also existed in 1763; verify Crimean Khanate
4. **RULERS**: Character file changes for TUR (Mustafa III), PR2 (Karim Khan Zand), MOR (Mohammed III)
5. **NORTH AFRICA**: Continuity (Algiers/Tunis/Tripoli autonomous both dates)
6. **OMAN/YEMEN/MOROCCO**: Continuity with ruler updates only

**KEY FINDING**: The **First Saudi State (Emirate of Diriyah)** is the single most significant polity difference—it existed in 1763 but was destroyed by Ottoman-Egyptian forces in 1818, making it **absent from 1815**.

---

## 1. TAG VERIFICATION

### Tags in `setup/countries/countries.txt`:

| Polity | Tag | File Path | Status |
|--------|-----|-----------|--------|
| **Ottoman Empire** | TUR | `setup/countries/m_east/turkey.txt` | ✅ EXISTS |
| **Persia** | PR2 | `setup/countries/c_asia/persia.txt` | ✅ EXISTS |
| **Peru** | PR1 | `setup/countries/s_america/peru.txt` | ⚠️ NOT PERSIA |
| **First Saudi State** | DRY | `setup/countries/m_east/diryah.txt` | ✅ EXISTS |
| **Oman** | OMA | `setup/countries/m_east/oman.txt` | ✅ EXISTS |
| **Muscat** | MSC | `setup/countries/m_east/muscat.txt` | ✅ EXISTS (separate) |
| **Morocco** | MOR | `setup/countries/n_africa/morocco.txt` | ✅ EXISTS |
| **Algiers** | ALG | `setup/countries/n_africa/algiers.txt` | ✅ EXISTS |
| **Tunis** | TUN | `setup/countries/n_africa/tunis.txt` | ✅ EXISTS |
| **Tripoli** | TRI | `setup/countries/n_africa/tripoli.txt` | ✅ EXISTS |
| **Egypt** | EGY | `setup/countries/n_africa/egypt.txt` | ✅ EXISTS |
| **Iraq** | IRA | `setup/countries/m_east/iraq.txt` | ✅ EXISTS |
| **Mosul** | MOS | `setup/countries/m_east/mosul.txt` | ✅ EXISTS |
| **Mount Lebanon** | MLB | `setup/countries/m_east/mount lebanon.txt` | ✅ EXISTS |

**RESOLUTION OF PR1/PR2 AMBIGUITY:**
- **PR1 = PERU** (South America)
- **PR2 = PERSIA** (Central Asia)
- No tag collision; PR2 is the correct Persia tag.

### Tags NOT in 1815 baseline but NEEDED for 1763:

**CRIMEAN KHANATE**: Research indicates the Crimean Khanate was an Ottoman vassal in 1763 but was **annexed by Russia in 1783**, making it absent from 1815. **ACTION REQUIRED**: Search for a Crimean tag (CRI/CRM/KRM?) in the tag list and determine if it exists in the 1815 file or needs to be added for 1763 only.

---

## 2. CURRENT 1815 BASELINE EXTRACTION

### Lines 777-822 in `setup/main/00_default.txt`:

```
#Ottoman Balkan vassals
dependency = { first = TUR second = WAL subject_type = autonomous_governorship }
dependency = { first = TUR second = MOL subject_type = autonomous_governorship }
dependency = { first = TUR second = ATH subject_type = nominal_vassal }
# Ottoman feudal breakaway states
dependency = { first = TUR second = MNS subject_type = nominal_vassal }
dependency = { first = TUR second = AKH subject_type = nominal_vassal }
dependency = { first = TUR second = KOC subject_type = nominal_vassal }
dependency = { first = TUR second = ATY subject_type = nominal_vassal }
dependency = { first = TUR second = CIL subject_type = nominal_vassal }
dependency = { first = TUR second = GRS subject_type = nominal_vassal }
dependency = { first = TUR second = TRB subject_type = nominal_vassal }
dependency = { first = TUR second = RZE subject_type = nominal_vassal }
dependency = { first = TUR second = JNI subject_type = nominal_vassal }
dependency = { first = TUR second = SCU subject_type = nominal_vassal }
dependency = { first = TUR second = MLB subject_type = nominal_vassal }
dependency = { first = TUR second = BTS subject_type = nominal_vassal }
dependency = { first = TUR second = MUK subject_type = nominal_vassal }
dependency = { first = TUR second = BHD subject_type = nominal_vassal }
dependency = { first = TUR second = SRN subject_type = nominal_vassal }
dependency = { first = TUR second = BBN subject_type = nominal_vassal }
dependency = { first = TUR second = HAK subject_type = nominal_vassal }
dependency = { first = TUR second = IRA subject_type = nominal_vassal }
dependency = { first = TUR second = MOS subject_type = nominal_vassal }
#Ottoman African vassals
dependency = { first = TUR second = ALG subject_type = tributary }
dependency = { first = TUR second = TUN subject_type = tributary }
dependency = { first = TUR second = TRI subject_type = client_state }
dependency = { first = TUR second = EGY subject_type = nominal_vassal }
dependency = { first = TUR second = MWA subject_type = client_state }
dependency = { first = TUR second = HRR subject_type = subsidiary_ally }
dependency = { first = TUR second = ZEI subject_type = protectorate }
#Other Ottoman vassals
dependency = { first = TUR second = KWT subject_type = client_state }
dependency = { first = TUR second = MFQ subject_type = feudatory }
dependency = { first = TUR second = ACH subject_type = subsidiary_ally }

#Qajar Empire Vassals
dependency = { first = PR2 second = NKH subject_type = protectorate }
dependency = { first = PR2 second = ERI subject_type = protectorate }
dependency = { first = PR2 second = MRD subject_type = nominal_vassal }
dependency = { first = PR2 second = URM subject_type = nominal_vassal }
dependency = { first = PR2 second = MKU subject_type = nominal_vassal }
dependency = { first = PR2 second = MGH subject_type = nominal_vassal }
dependency = { first = PR2 second = ARD subject_type = nominal_vassal }
dependency = { first = PR2 second = BLO subject_type = nominal_vassal }
```

---

## 3. 1763 CONVERSION DELTA

### 3.1 PERSIA (PR2) — MAJOR DYNASTY/CAPITAL CHANGE

**CURRENT 1815 STATE:**
- **Dynasty:** Qajar (قاجاريان)
- **Ruler:** Fath-Ali Shah Qajar (r. 1797–1834)
- **Capital:** Tehran (تهران)
- **Character File:** `setup/characters/00_Persian Empire.txt` line 33-42 (char:539)

**TARGET 1763 STATE:**
- **Dynasty:** Zand (زندیان)
- **Ruler:** Karim Khan Zand (Vakil ol-Ra'aya, r. 1751–1779)
- **Capital:** Shiraz (شیراز)
- **Vassals:** UNKNOWN if the same Caucasian vassals applied in 1763; Khorasan was SEPARATE under Afsharid Shahrokh Shah (NOT part of Zand Persia)

**REQUIRED CHANGES:**

1. **Character File (`setup/characters/00_Persian Empire.txt`):**
   - **REPLACE** Qajar dynasty rulers (chars 536-542) with Zand dynasty rulers
   - **NEW CHAR**: Karim Khan Zand (c. 1705–1779)
     - `first_name="Karim Khan"`
     - `family = "c:PR2.fam:Zand"` (or family_name="Zand")
     - `birth_date=1705.1.1` (approximate; sources say "c. 1705")
     - `death_date=1779.3.1`
     - `culture="persian"` (or "lur"—Zand tribe of the Laks, Kurdish/Lur ethnicity)
     - `religion="shiite"`
     - `add_trait="vakil"` (if trait exists; otherwise generic ruler traits)
   - **Set as ruler** in 1763 start date: `c:PR2={ set_as_ruler=char:NEW_ID }`

2. **Capital Change:**
   - **ACTION REQUIRED**: Find the province ID for **Shiraz** in `map_data/provinces.txt` or `map_data/areas.txt`
   - In the country setup or via an on_action event at start, set PR2's capital to Shiraz
   - Tehran was a relatively minor city in 1763; the Qajars made it capital in 1796

3. **Vassal Adjustment:**
   - **UNKNOWN**: Did the Caucasian vassals (NKH, ERI, MRD, URM, MKU, MGH, ARD) exist under Zand Persia in 1763, or were they Qajar acquisitions?
   - **Research gap**: The 1763 research doc does not specify Zand vassals beyond "most of Persia except Khorasan"
   - **CONSERVATIVE APPROACH**: Retain the 1815 vassal list as a placeholder; adjust if historical sources identify different vassals
   - **ALTERNATE**: Remove Caucasian vassals entirely and restore them only for the 1815 bookmark

4. **Khorasan (Afsharid Remnant):**
   - In 1763, **Shahrokh Shah** (Afsharid) ruled Khorasan (capital Mashhad) as a SEPARATE polity from Zand Persia
   - **ACTION REQUIRED**: Check if there is a Khorasan/Mashhad tag (KHO/MSH/AFS?) in the tag list
   - If YES: Make it an independent country in 1763, NOT a Zand vassal
   - If NO: Khorasan may be represented as part of PR2's territory but with a note that it was autonomous

**EDIT LOCATION:**
- `setup/characters/00_Persian Empire.txt` lines 1-60 (entire PR2 character block)
- `setup/main/00_default.txt` lines 814-822 (Qajar vassal block—may need adjustment)
- **Capital change**: Unknown file; likely `setup/countries/c_asia/persia.txt` or an on_action event

---

### 3.2 FIRST SAUDI STATE (DRY) — NEW INDEPENDENT TAG

**CURRENT 1815 STATE:**
- **DOES NOT EXIST** (destroyed 1818)
- The tag **DRY** (Diriyah) EXISTS in `setup/countries/countries.txt` line 236, but it is **NOT in the 1815 setup file** (no dependencies, no relations)

**TARGET 1763 STATE:**
- **Status:** Independent emirate in Najd
- **Ruler:** Muhammad bin Saud (محمد بن سعود, r. 1744–1765; dies 1765)
- **Capital:** Diriyah (الدرعية) in Najd
- **Territory:** Najd (central Arabian plateau); did NOT yet control Hejaz (Mecca/Medina)
- **Ideology:** Wahhabi movement (الدعوة الوهابية)
- **Major opponent:** Dahham bin Dawas, emir of Riyadh (17 battles over 27 years)

**REQUIRED CHANGES:**

1. **ADD** DRY as an independent country in 1763:
   - **LOCATION**: Insert in `setup/main/00_default.txt` around line 810 (after Ottoman vassals, before Qajar vassals) or in a new Arabia section
   - **NO dependencies**: DRY was fully independent
   - **RELATION**: May have hostile relations with neighboring Ottoman vassal tags (if Hejaz is represented as TUR→??? )

2. **Character File:**
   - **CREATE** or **EDIT** `setup/characters/00_Saudi Arabia.txt` (or similar)
   - **NEW CHAR**: Muhammad bin Saud
     - `first_name="Muhammad bin Saud"`
     - `family_name="Al Saud"` or `family = "c:DRY.fam:Al_Saud"`
     - `birth_date=1697.1.1` (approximate; sources vary)
     - `death_date=1765.1.1`
     - `culture="bedouin"` (or "najdi" if culture exists)
     - `religion="sunni"`
     - `add_trait="wahhabi"` (if trait exists; otherwise generic ruler traits)
   - **Set as ruler**: `c:DRY={ set_as_ruler=char:NEW_ID }`

3. **Capital:**
   - **ACTION REQUIRED**: Find the province ID for **Diriyah** in Najd
   - Set DRY's capital to Diriyah (likely in `setup/countries/m_east/diryah.txt`)

4. **Territory:**
   - **ACTION REQUIRED**: Determine which provinces in Najd should be owned by DRY in 1763
   - Research indicates DRY controlled Najd but NOT Hejaz (Mecca/Medina remained under Ottoman-appointed Sharifs)
   - **REGION**: Najd (النجد) should map to a region/area in `map_data/regions.txt` or `map_data/areas.txt`

5. **Relations:**
   - **RIVAL**: Dahham bin Dawas (Riyadh)—check if Riyadh has a separate tag (RYD?)
   - **HOSTILE**: May have border tensions with Ottoman Hejaz (if represented)
   - **ALLY**: Muhammad ibn Abd al-Wahhab (religious leader, not a ruler—may be a character trait or event chain)

**EDIT LOCATION:**
- `setup/main/00_default.txt` — NEW independent country entry (exact line TBD)
- `setup/characters/` — NEW or EDIT file for DRY rulers
- `setup/countries/m_east/diryah.txt` — capital and province ownership

**CRITICAL NOTE**: The First Saudi State's destruction in 1818 means it should **NOT appear in 1815** but **MUST appear in 1763**. This is a **bookmark-conditional** setup.

---

### 3.3 OTTOMAN EMPIRE (TUR) — VASSAL/RULER CHANGES

**CURRENT 1815 STATE:**
- **Sultan:** Mahmud II (r. 1808–1839)
- **Character File:** `setup/characters/00_Ottoman Empire.txt` line 42 (char:45)
- **Vassals:** Lines 777-812 (Balkans, feudal breakaways, Africa, other)

**TARGET 1763 STATE:**
- **Sultan:** Mustafa III (مصطفى ثالث, r. 1757–1774)
- **Grand Vizier:** Koca Ragıp Pasha (d. 8 April 1763—TWO MONTHS after game start)
- **Vassals:** MOST 1815 vassals also existed in 1763; notable exceptions below

**REQUIRED CHANGES:**

1. **Character File (`setup/characters/00_Ottoman Empire.txt`):**
   - **NEW CHAR** (or verify existing): Mustafa III
     - Research indicates char:42 is "Abdul Hamid" (1725–1789) and char:43 is "Selim III" (1761–1808)
     - **ACTION REQUIRED**: Check if Mustafa III already exists in the file (he ruled BEFORE Abdul Hamid, so may be an earlier char ID)
     - If NOT present:
       - `first_name="Mustafa III"`
       - `family_name="Osmanlı"`
       - `birth_date=1717.1.28`
       - `death_date=1774.1.21`
       - `culture="turkish"`
       - `religion="sunni"`
       - `add_trait="caliph"`
   - **Set as ruler** in 1763: `c:TUR={ set_as_ruler=char:MUSTAFA_III_ID }`

2. **Grand Vizier:**
   - **NEW CHAR**: Koca Ragıp Pasha
     - `first_name="Koca Ragıp"`
     - `family_name="Pasha"`
     - `birth_date=1698.1.1`
     - `death_date=1763.4.8` (dies during game)
     - `culture="turkish"`
     - `religion="sunni"`
     - `add_trait="grand_vizier"` (if trait exists; otherwise set as court position)
   - **Successor (April 1763)**: Tevkii Hamza Hamid Pasha (brief tenure), then Muhsinzade Mehmed Pasha

3. **Vassal Verification (1763 vs 1815):**

   **Balkans (lines 778-780):**
   - **WAL (Wallachia)**: ✅ PRESENT both dates (Phanariote Greeks, Ottoman vassal)
     - 1763 Hospodar: Constantin Mavrocordat (1761–1763)
   - **MOL (Moldavia)**: ✅ PRESENT both dates (Phanariote Greeks, Ottoman vassal)
     - 1763 Hospodar: Grigore Callimachi (1761–1764)
   - **ATH (Athos)**: ✅ PRESENT both dates (Mount Athos, monastic republic under Ottoman protection)

   **Feudal Breakaway States (lines 782-800):**
   - All listed tags (MNS, AKH, KOC, ATY, CIL, GRS, TRB, RZE, JNI, SCU, MLB, BTS, MUK, BHD, SRN, BBN, HAK, IRA, MOS) appear to be Anatolian/Kurdish/Iraqi local beyliks or emirates
   - **ASSUMPTION**: Most existed in 1763 (Ottoman control over periphery was weak throughout 18th century)
   - **VERIFY**: MLB (Mount Lebanon) was ruled by Shihab dynasty in 1763 as an Ottoman *iltizam* (tax farm), not a nominal vassal—subject_type may need adjustment to `autonomous_governorship` or `feudatory`

   **African Vassals (lines 802-808):**
   - **ALG (Algiers)**: ✅ PRESENT both dates (Regency of Algiers, *de facto* independent under deys)
   - **TUN (Tunis)**: ✅ PRESENT both dates (Husainid dynasty, Bey Ali II ibn Hussein 1759–1782)
   - **TRI (Tripoli)**: ✅ PRESENT both dates (Karamanli dynasty, Ali I Karamanli 1754–1793)
   - **EGY (Egypt)**: ✅ PRESENT both dates (Mamluk control)
     - 1763: Ali Bey al-Kabir (Sheikh al-Balad, first term 1760–1766)
     - 1815: Muhammad Ali Pasha (autonomous dynasty-founder)
     - **NOTE**: Egypt's autonomy INCREASED 1763→1815; may need subject_type adjustment
   - **MWA, HRR, ZEI**: East African vassals—**VERIFY** if these existed in 1763 or were 19th-century acquisitions

   **Other Ottoman Vassals (lines 810-812):**
   - **KWT (Kuwait)**: ✅ PRESENT both dates (Al Sabah dynasty, autonomous under Ottoman suzerainty)
   - **MFQ (Muntafiq)**: ✅ PRESENT both dates (Arab tribal confederation in southern Iraq)
   - **ACH (Aceh)**: ❓ UNCLEAR—Aceh Sultanate in Sumatra was nominally Ottoman-allied but NOT a true vassal

   **MISSING FROM 1815, PRESENT IN 1763:**
   - **CRIMEAN KHANATE**: Ottoman vassal 1763, annexed by Russia 1783
     - **ACTION REQUIRED**: Search for Crimean tag (CRI/CRM/KRM/KHN?) and add to 1763 Ottoman vassal list
     - 1763 Khan: Qırım Giray (قرم كراى, r. 1758–1764)
     - Subject type: `tributary` or `feudatory` (privileged vassal, NO tribute paid, military service obligation)

**EDIT LOCATION:**
- `setup/characters/00_Ottoman Empire.txt` — ruler change (Mustafa III)
- `setup/main/00_default.txt` lines 777-812 — verify/adjust Ottoman vassal list
- **ADD** Crimean Khanate dependency (if tag exists)

---

### 3.4 NORTH AFRICA (BARBARY REGENCIES) — CONTINUITY

**CURRENT 1815 STATE:**
- **Algiers (ALG)**: *De facto* independent under deys
- **Tunis (TUN)**: Husainid dynasty, autonomous under nominal Ottoman suzerainty
- **Tripoli (TRI)**: Karamanli dynasty, autonomous

**TARGET 1763 STATE:**
- **Algiers (ALG)**: Same status, different dey (unknown for 1763)
- **Tunis (TUN)**: Bey Ali II ibn Hussein (1759–1782)
- **Tripoli (TRI)**: Ali I Karamanli (1754–1793)

**REQUIRED CHANGES:**

1. **Character Files:**
   - **Tunis**: REPLACE 1815 Bey (Mahmud, 1814–1824) with 1763 Bey (Ali II ibn Hussein)
   - **Tripoli**: REPLACE 1815 Pasha (Yusuf Karamanli, 1795–1832) with 1763 Pasha (Ali I Karamanli, 1754–1793)
   - **Algiers**: Dey unknown for 1763; use generic ruler or research further

2. **Vassal Status:**
   - **NO CHANGE** needed in `setup/main/00_default.txt` lines 802-804 (already `tributary` or `client_state`)

**EDIT LOCATION:**
- `setup/characters/00_Tunis.txt` (if exists) — ruler change
- `setup/characters/00_Tripoli.txt` (if exists) — ruler change
- `setup/characters/00_Algiers.txt` (if exists) — ruler change or generic

---

### 3.5 INDEPENDENT STATES (CONTINUITY WITH RULER UPDATES)

**MOROCCO (MOR):**
- **1815 Ruler:** Sultan Sulayman (1792–1822)
- **1763 Ruler:** Sultan Mohammed III (محمد بن عبد الله, r. 1757–1790)
- **Status:** Fully independent, Alaouite dynasty (both dates)
- **CHANGE**: Character file ruler swap only

**OMAN (OMA):**
- **1815 Ruler:** Said bin Sultan (1804–1856)
- **1763 Ruler:** Ahmad bin Said Al Bu Said (أحمد بن سعيد البوسعيدي, r. 1749–1783)
- **Status:** Fully independent, Al Bu Said dynasty (both dates)
- **Territory**: Oman + East African coast (Zanzibar, Mombasa, Pemba)
- **CHANGE**: Character file ruler swap only

**YEMEN (Qasimid State):**
- **1815 Ruler:** Imam al-Mutawakkil Ahmad (1809–1816)
- **1763 Ruler:** Imam Al-Mahdi Abbas (الإمام المهدي عباس, r. 1748–1775)
- **Status:** Independent Zaidi imamate (both dates)
- **CHANGE**: Character file ruler swap only

**EDIT LOCATION:**
- `setup/characters/00_Morocco.txt` (if exists)
- `setup/characters/00_Oman.txt` (if exists)
- `setup/characters/00_Yemen.txt` (if exists)

---

### 3.6 EGYPT (EGY) — MAMLUK AUTONOMY LEVEL

**CURRENT 1815 STATE:**
- **Ruler:** Muhammad Ali Pasha (1805–1848), dynasty-founder, effectively independent
- **Subject type:** `nominal_vassal` (line 805)

**TARGET 1763 STATE:**
- **Ruler:** Ali Bey al-Kabir (Sheikh al-Balad, first term 1760–1766)
- **Status:** De facto Mamluk beylicate rule, weaker autonomy than 1815

**REQUIRED CHANGES:**

1. **Character File:**
   - REPLACE Muhammad Ali Pasha with Ali Bey al-Kabir
   - `first_name="Ali Bey"`
   - `family_name="al-Kabir"` or `"Mamluk"`
   - `birth_date=1728.1.1` (c. 1728, sources say "around 1741" for age 13 kidnapping)
   - `death_date=1773.5.8`
   - `culture="circassian"` or `"abkhaz"` (born in Abkhazia/Circassia)
   - `religion="sunni"`

2. **Subject Type:**
   - **OPTIONAL**: Change from `nominal_vassal` to `autonomous_governorship` (weaker autonomy in 1763)
   - **REASONING**: Ali Bey had not yet declared independence (1769) or halted tribute (1769) in 1763
   - **CONSERVATIVE**: Keep `nominal_vassal` for simplicity

**EDIT LOCATION:**
- `setup/characters/00_Egypt.txt` (if exists)
- `setup/main/00_default.txt` line 805 (optional subject_type change)

---

### 3.7 IRAQ (IRA/MOS) — MAMLUK PASHAS

**CURRENT 1815 STATE:**
- **Ruler:** Dawud Pasha (Baghdad, 1816–1831)
- **Subject type:** `nominal_vassal` (line 799-800)

**TARGET 1763 STATE:**
- **Ruler:** Omar Pasha (عمر باشا, Baghdad, 1762–1776)
- **Status:** Georgian Mamluk Dynasty of Iraq, autonomous under nominal Ottoman suzerainty

**REQUIRED CHANGES:**

1. **Character File:**
   - REPLACE Dawud Pasha with Omar Pasha
   - `first_name="Omar"`
   - `family_name="Pasha"` or `"Mamluk"`
   - `birth_date=1720.1.1` (approximate)
   - `death_date=1776.1.1`
   - `culture="georgian"` or `"circassian"`
   - `religion="sunni"`

2. **Subject Type:**
   - **NO CHANGE** (already `nominal_vassal`)

**EDIT LOCATION:**
- `setup/characters/00_Iraq.txt` (if exists)

---

## 4. AREA/REGION MAPPING

**ACTION REQUIRED**: For territory changes, provide exact province IDs and area/region names from `map_data/`:

1. **Persia Capital**: Find Shiraz province ID (likely in Fars region)
2. **First Saudi State**: Find Diriyah/Najd province IDs
3. **Khorasan (if separate tag)**: Find Mashhad province ID

**METHOD**:
```bash
grep -i "shiraz\|najd\|mashhad\|diriyah" map_data/provinces.txt
grep -i "shiraz\|najd\|mashhad\|diriyah" map_data/areas.txt
grep -i "fars\|najd\|khorasan" map_data/regions.txt
```

---

## 5. RISK ASSESSMENT

### HIGH-RISK CHANGES:

1. **Persia Dynasty Swap:**
   - Changing PR2 from Qajar to Zand affects character lineage, events, mission trees
   - **MITIGATION**: Use a 1763-specific character file or branch characters by bookmark date

2. **First Saudi State (DRY):**
   - Adding a new independent country in Arabia may conflict with Ottoman Hejaz territory
   - **MITIGATION**: Verify province ownership and ensure DRY owns ONLY Najd, NOT Hejaz

3. **Crimean Khanate:**
   - If the tag does NOT exist, cannot add it without creating new tag + provinces
   - **MITIGATION**: Check tag list; if absent, document as "1763 limitation"

### MEDIUM-RISK CHANGES:

1. **Ottoman Vassal List:**
   - Minor polities (MWA, HRR, ZEI) may be 19th-century additions
   - **MITIGATION**: Verify each tag's founding date; remove anachronisms

2. **Egypt/Iraq Autonomy:**
   - Changing subject_type may affect integration mechanics
   - **MITIGATION**: Test in-game before finalizing

### LOW-RISK CHANGES:

1. **Ruler Name Swaps:**
   - Character file edits are low-risk if new characters are properly defined
   - **MITIGATION**: Copy DNA strings from existing characters, adjust birth/death dates

---

## 6. EXACT EDIT PLAN (STEP-BY-STEP)

### STEP 1: CHARACTER FILES

**File:** `setup/characters/00_Persian Empire.txt`

**ACTION:**
1. **READ** lines 1-60 (current Qajar dynasty rulers)
2. **REPLACE** with Zand dynasty rulers:
   - **NEW CHAR**: Karim Khan Zand (Vakil, r. 1751–1779)
   - Set as ruler for PR2 in 1763
3. **OPTIONAL**: Add Agha Mohammad Khan Qajar as a MINOR character (hostage in Shiraz, 1763)

**File:** `setup/characters/00_Ottoman Empire.txt`

**ACTION:**
1. **SEARCH** for Mustafa III (may already exist before Abdul Hamid)
2. **IF NOT FOUND**: Add Mustafa III character before char:42
3. **SET** as ruler for TUR in 1763

**File:** `setup/characters/00_Saudi Arabia.txt` (OR CREATE IF NOT EXISTS)

**ACTION:**
1. **CREATE** character for Muhammad bin Saud (founder, r. 1744–1765)
2. **SET** as ruler for DRY in 1763

**File:** `setup/characters/00_Morocco.txt`, `00_Oman.txt`, `00_Yemen.txt`, `00_Tunis.txt`, `00_Tripoli.txt`, `00_Egypt.txt`, `00_Iraq.txt`

**ACTION:**
1. **REPLACE** 1815 rulers with 1763 rulers (see sections 3.4, 3.5, 3.6, 3.7)

---

### STEP 2: SETUP FILE (`setup/main/00_default.txt`)

**Lines 814-822 (Qajar/Zand Vassals):**

**CURRENT:**
```
#Qajar Empire Vassals
dependency = { first = PR2 second = NKH subject_type = protectorate }
dependency = { first = PR2 second = ERI subject_type = protectorate }
dependency = { first = PR2 second = MRD subject_type = nominal_vassal }
dependency = { first = PR2 second = URM subject_type = nominal_vassal }
dependency = { first = PR2 second = MKU subject_type = nominal_vassal }
dependency = { first = PR2 second = MGH subject_type = nominal_vassal }
dependency = { first = PR2 second = ARD subject_type = nominal_vassal }
dependency = { first = PR2 second = BLO subject_type = nominal_vassal }
```

**TARGET (CONSERVATIVE):**
```
#Zand Empire Vassals [bookmark-1763 #208] Karim Khan Zand, capital Shiraz; Caucasian vassals TBD
dependency = { first = PR2 second = NKH subject_type = protectorate }
dependency = { first = PR2 second = ERI subject_type = protectorate }
dependency = { first = PR2 second = MRD subject_type = nominal_vassal }
dependency = { first = PR2 second = URM subject_type = nominal_vassal }
dependency = { first = PR2 second = MKU subject_type = nominal_vassal }
dependency = { first = PR2 second = MGH subject_type = nominal_vassal }
dependency = { first = PR2 second = ARD subject_type = nominal_vassal }
dependency = { first = PR2 second = BLO subject_type = nominal_vassal }
```

**NOTES:**
- Comment changed to reflect Zand dynasty and Shiraz capital
- Vassal list retained pending further research
- **ALTERNATIVE**: Remove vassals entirely if Zand Persia did NOT control Caucasus in 1763

---

**NEW SECTION (Insert after line 812, before line 814):**

```
#Arabian Independent States [bookmark-1763 #208]
# First Saudi State (Emirate of Diriyah) — founded 1744, destroyed 1818
# PRESENT in 1763, ABSENT in 1815
# Ruler: Muhammad bin Saud (1744-1765), capital Diriyah in Najd
# Territory: Najd only; Hejaz (Mecca/Medina) still under Ottoman Sharifs
# [NO dependencies for DRY — fully independent]
```

**ALTERNATIVE** (if DRY should have relations):
```
# First Saudi State vs. Riyadh rivalry
# rival = { first = DRY second = RYD } # [IF RYD tag exists for Riyadh]
```

---

**Lines 777-812 (Ottoman Vassals):**

**ACTION:**
1. **VERIFY** each vassal existed in 1763 (see section 3.3)
2. **ADD** Crimean Khanate (if tag found):
   ```
   dependency = { first = TUR second = CRM subject_type = tributary }  # [bookmark-1763 #208] Crimean Khanate, annexed by Russia 1783
   ```
3. **ADJUST** Mount Lebanon (MLB) subject_type if needed:
   - Change from `nominal_vassal` to `feudatory` (Ottoman *iltizam* tax farm under Shihab emirs)

---

### STEP 3: CAPITAL CHANGES

**ACTION REQUIRED:**
1. **FIND** Shiraz province ID
2. **EDIT** `setup/countries/c_asia/persia.txt` OR add on_action event:
   ```
   c:PR2 = {
       set_capital = p:SHIRAZ_ID
   }
   ```

---

### STEP 4: TERRITORY ADJUSTMENTS

**ACTION REQUIRED:**
1. **First Saudi State (DRY)**: Assign Najd provinces to DRY
2. **Khorasan**: If separate tag exists, assign Mashhad + Khorasan provinces to AFS/KHO tag

---

## 7. TESTING CHECKLIST

After applying edits:

- [ ] PR2 starts with Karim Khan Zand as ruler
- [ ] PR2 capital is Shiraz (not Tehran)
- [ ] DRY (First Saudi State) exists as independent country in Najd
- [ ] DRY does NOT control Hejaz (Mecca/Medina)
- [ ] TUR starts with Mustafa III as ruler
- [ ] TUR→CRM dependency exists (if Crimean tag found)
- [ ] Morocco starts with Mohammed III
- [ ] Oman starts with Ahmad bin Said
- [ ] Yemen starts with Imam Al-Mahdi Abbas
- [ ] Tunis starts with Bey Ali II
- [ ] Tripoli starts with Ali I Karamanli
- [ ] Egypt starts with Ali Bey al-Kabir
- [ ] Iraq starts with Omar Pasha
- [ ] NO 1763-anachronistic tags (e.g., no Muhammad Ali Pasha in 1763)

---

## 8. OPEN QUESTIONS FOR USER

1. **Crimean Khanate Tag**: Does a Crimean tag (CRI/CRM/KRM/KHN?) exist in the 1815 file? If yes, what is it?
2. **Khorasan Separation**: Should Khorasan (Afsharid Shahrokh Shah) be a separate tag in 1763, or part of Zand Persia?
3. **Zand Vassals**: Should the Caucasian vassals (NKH, ERI, etc.) be retained for Zand Persia, or were they Qajar acquisitions?
4. **Egypt Autonomy**: Should Egypt's subject_type change from `nominal_vassal` (1815) to `autonomous_governorship` (1763)?
5. **Province Ownership**: Should I provide exact province lists for DRY (Najd) and PR2 (Zand territories)?

---

## 9. SOURCES

- `research/1763_WORLD_Ottoman_MENA.md` (lines 1-1507)
- `research/1763_MENA_independent_states_partial.md` (lines 1-162)
- `setup/main/00_default.txt` (lines 777-822)
- `setup/countries/countries.txt` (lines 1-715)
- `setup/characters/00_Ottoman Empire.txt` (lines 1-50)
- `setup/characters/00_Persian Empire.txt` (lines 1-60)

---

**END OF DELTA DOCUMENT**

**Next Steps:**
1. User reviews and answers open questions
2. Apply character file edits (STEP 1)
3. Apply setup file edits (STEP 2)
4. Apply capital/territory changes (STEP 3-4)
5. Test in-game (STEP 5)
6. Commit with tag `[bookmark-1763 #208 Ottoman/MENA/Persia baseline]`
