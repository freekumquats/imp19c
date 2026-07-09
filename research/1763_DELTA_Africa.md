# 1763 Africa DELTA Plan
## Read-Only Recon: Current 1815 Baseline → 1763 Target

**Branch**: `1763_bookmark`  
**Date**: 2026-07-08  
**Baseline**: setup/main/00_default.txt (49,422 lines)  
**Target**: research/1763_WORLD_Africa.md

---

## EXECUTIVE SUMMARY

This document provides the **EXACT EDIT PLAN** to convert the current 1815 Africa setup to the 1763 state. Key changes:

1. **Cape Colony**: Must transfer from British (CPC, line 704) to Dutch (NED→DAF or new Dutch Cape tag)
2. **Sokoto Caliphate**: Does NOT exist in 1763 — revert to independent Hausa city-states (Kano, Katsina, Zaria, Gobir, etc.)
3. **Swahili Coast**: Already correctly under Omani control (OMA owns Zanzibar/Kilwa, lines 44711); MZR (Mazrui Mombasa) exists separately
4. **Oyo-Dahomey**: Dahomey must become tributary to Oyo (currently independent in 1815 setup)
5. **Ethiopia**: Ruler change (Emperor Iyoas I, r. 1755-1769, not Zemene Mesafint warlords)
6. **Hausa States**: Need NEW tags for Kano, Katsina, Zaria/Zazzau, Daura, Rano, Biram (currently only GBI/Gobir exists)

**CRITICAL DEPENDENCIES**:
- **Areas/Regions**: This plan references AREAS/REGIONS for province moves but does NOT invent province IDs. User must verify map_data/areas.txt and regions.txt for correct area names.
- **New Tags**: Six new Hausa city-state tags required (Kano, Katsina, Zaria, Daura, Rano, Biram). User must decide tag codes and create country files.
- **Cape**: Decision needed: repurpose existing DAF (currently Dutch Caribbean, line 39258-39274) for Cape, or create new Dutch Cape tag.

---

## I. CURRENT 1815 BASELINE: AFRICAN STATES IN 00_default.txt

### A. Dependencies (Lines 550-1068)

| First | Second | Type | Line | Notes |
|-------|--------|------|------|-------|
| **SOK** | LIP | feudatory | 551 | Sokoto Caliphate (founded 1804) |
| **SOK** | GBI | feudatory | 552 | Gobir (Hausa) |
| **SOK** | ADM | feudatory | 553 | Adamawa |
| **SOK** | GMB | feudatory | 554 | Gombe |
| **SOK** | BIU | feudatory | 555 | Biu |
| WAD | BAG | tributary | 597 | Wadai-Bagirmi |
| **ATI** | ABR | vassal_tribe | 600 | Ashanti-Abron |
| ROZ | MUT | protectorate | 603 | Rozvi-Mutapa |
| ROZ | MGJ | tributary | 604 | Rozvi-Manganja |
| **GDR** | TGR | tributary | 887 | Ethiopia (Gondar)-Tigray |
| **GDR** | SWA | tributary | 888 | Ethiopia-Shewa |
| **GDR** | WLO | tributary | 889 | Ethiopia-Wollo |
| **GDR** | GJJ | tributary | 890 | Ethiopia-Gojjam |
| **NED** | DAF | client_colony | 907 | Dutch Africa (currently Caribbean, see line 39258) |
| DEN | DGC | client_colony | 917 | Danish Gold Coast |
| **KBO** | MRG | feudatory | 1001 | Bornu-Marghi |
| **KBO** | BDE | feudatory | 1002 | Bornu-Bedde |
| **KBO** | DAM | tributary | 1003 | Bornu-Damagaram |
| **KBO** | KKO | tributary | 1004 | Bornu-Kotoko |
| POR | **ANG** | client_colony | 1015 | Portuguese Angola |
| POR | **MOZ** | client_colony | 1016 | Portuguese Mozambique |
| FRA | FCA | client_colony | 1031 | French Coastal Africa |
| **OYO** | IJE | feudatory | 1064 | Oyo-Ijebu |
| **OYO** | IFE | feudatory | 1065 | Oyo-Ife |
| **OYO** | **DAH** | tributary | 1066 | **Oyo-Dahomey** |
| **GBR** | **CPC** | client_colony | 704 | **British Cape Colony** (MUST CHANGE to Dutch in 1763) |

### B. Country Blocks: African States

| Tag | Lines | Capital | Culture | Religion | Notes |
|-----|-------|---------|---------|----------|-------|
| **MOR** | 39038+ | ? | ? | sunni | Morocco (North Africa; cross-ref Ottoman recon) |
| **ATI** | 46331-46353 | 2571 (Kumasi area) | akan | akan | Ashanti Empire |
| **OYO** | 46607-46629 | 492 | yoruba | orisha | Oyo Empire (at zenith in 1763) |
| **DAH** | 46649-46666 | 7897 (Abomey area) | fon | dahoman | Dahomey (MUST be tributary to Oyo in 1763) |
| BEN | 46668-46686 | 1081 | ede | orisha | Benin Kingdom |
| IFE | 46688-46700 | 4384 | yoruba | orisha | Ife (Oyo tributary) |
| **KBO** | 46095-46113 | 4083 | hausa | sunni | Kanem-Bornu Empire (Mai Dunama IX, r. 1747-1792) |
| DAM | 46115-46131 | 8014 | hausa | sunni | Damagaram (Bornu tributary) |
| **GBI** | 46169-46185 | 6005 | hausa | sunni | **Gobir** (currently SOK feudatory; MUST be independent in 1763) |
| ABJ | 46187-46203 | 7691 | hausa | sunni | Abuja (Hausa, not Sokoto in 1763?) |
| NUP | 46205+ | 6931 | hausa | sunni | Nupe (Hausa region) |
| **SOK** | 46859-46887 | 10155 | fulani | sunni | **Sokoto Caliphate (DELETE for 1763 — founded 1804)** |
| ADM | 46889-46905 | 1173 | fulani | sunni | Adamawa Emirate (Sokoto tributary in 1815; independent in 1763?) |
| GMB | 46907+ | 6861 | fulani | sunni | Gombe Emirate (Sokoto tributary in 1815; independent in 1763?) |
| LIP | 46943-46959 | 7204 | fulani | sunni | Liptako Emirate (Sokoto tributary in 1815; independent in 1763?) |
| **KON** | 47343-47360 | 1366 | kongo | catholic | Kingdom of Kongo (fragmented by 1763, more so by 1815) |
| KKG | 47362-47378 | 4525 | kongo | syncretic_christian | Kakongo |
| **LUN** | 47477-47496 | 7689 | luba | bantu | Lunda Empire |
| CHK | 47498-47521 | 2122 | kambunda | bantu | Chokwe |
| KAZ | 47523-47547 | 919 | shona | bantu | Kazembe |
| ROZ | 47549+ | ? | shona | bantu | Rozvi Empire |
| **GDR** | (East Africa section, not read in full) | ? | amhara | coptic | Ethiopian Empire (Gondar) — Emperor Iyoas I in 1763 |
| **OMA** | 44696-44728 | 7874 (Muscat) | omani | ibadi | Oman (owns Swahili coast: line 44711 = 1489 Zanzibar, etc.) |
| **MZR** | 44731-44746 | 8882 (Mombasa) | omani | sunni | Mazrui (semi-autonomous Mombasa governors under Oman) |
| **CPC** | 48764-48796 | 2750 (Cape Town) | anglo_african | lutheran | **British Cape Colony (MUST be Dutch VOC in 1763)** |

### C. Current DAF (Dutch Africa) Block — Lines 39258-39274

```
DAF = {
    government = viceroyalty
    diplomatic_stance= appeasement_stance
    primary_culture = dutch
    religion = evangelical

    capital = 5821  # Dutch Aruba, Curaçao, Bonaire (Caribbean, NOT Cape!)

    own_control_core = {
        5821
    }
}
```

**PROBLEM**: DAF is currently Dutch Caribbean. For 1763, the Cape must be Dutch. Two options:
1. **Repurpose DAF**: Move DAF capital to 2750 (Cape Town), give it Cape provinces (see CPC block lines 48774-48792), rename to Dutch Cape Colony.
2. **Create new tag**: E.g., DCE (Dutch Cape Colony), new country file.

---

## II. 1763 TARGET STATE (from research/1763_WORLD_Africa.md)

### A. Key Deltas vs 1815

| Region | 1763 | 1815 Current Baseline | Delta |
|--------|------|----------------------|-------|
| **Cape** | **Dutch VOC** (Governor Ryk Tulbagh, r. 1751-1771) | **British CPC** (seized 1806, formalized 1814) | Transfer CPC provinces to Dutch (NED or new tag) |
| **Hausaland** | **Independent Hausa city-states**: Kano, Katsina, Zazzau/Zaria, Gobir, Daura, Rano, Biram | **Sokoto Caliphate** (SOK + GBI/ADM/GMB/LIP/BIU as feudatories) | DELETE SOK overlordship; make GBI independent; CREATE 6 new Hausa tags |
| **Oyo-Dahomey** | Oyo at zenith; **Dahomey tributary** to Oyo (annual tribute since 1730s) | Oyo declining; Dahomey independent (tributary relationship ended) | CHANGE line 1066: keep OYO→DAH tributary |
| **Ethiopia** | Centralized under **Emperor Iyoas I** (r. 1755-1769); pre-Zemene Mesafint | Zemene Mesafint (1769-1855): weak emperors, warlords | Ruler change (not structural — GDR tributaries remain) |
| **Swahili Coast** | Omani Swahili coast (Kilwa, Zanzibar, Mombasa); Muscat is capital (NOT Zanzibar) | Same (Zanzibar becomes capital 1832 under Said bin Sultan) | **NO CHANGE** (baseline already correct for 1763) |
| **Sokoto Caliphate** | **DOES NOT EXIST** (founded 1804 via Fulani jihad) | Exists (SOK tag + emirates) | **DELETE SOK tag block, DELETE dependencies lines 550-555** |
| **Zulu/Mfecane** | Fragmented Nguni chiefdoms; no Zulu kingdom | Zulu kingdom (Shaka, r. 1816-1828); Mfecane states | (Not in current baseline — likely post-1815 content, not in scope) |

### B. Rulers (1763 Historical Figures)

| Polity | 1763 Ruler | Notes |
|--------|-----------|-------|
| **Asante** | Kusi Obodom (regent, d. 1764) or **Osei Kwadwo** (successor 1764) | Transition period |
| **Oyo** | **Alaafin Abiodun** (r. c. 1754-1789) | Territorial zenith |
| **Dahomey** | **King Tegbesu** (r. 1740-1774) | Tributary to Oyo |
| **Ethiopia** | **Emperor Iyoas I** (r. 1755-1769) | Son of Empress Mentewab |
| **Oman** | **Imam Ahmad bin Said Al Busaidi** (r. 1749-1783) | Controls Swahili coast |
| **Cape** | **Governor Ryk Tulbagh** (VOC, r. 1751-1771) | Dutch administrator |
| **Bornu** | **Mai Dunama IX** (r. c. 1747-1792) | Sayfawa dynasty |
| **Hausa states** | Various **Sarkis** (kings) — independent rulers | No unified state |

---

## III. EXACT EDIT PLAN: 1815 → 1763

### PHASE 1: CAPE COLONY (British → Dutch)

#### Current State
- Line 704: `dependency = { first = GBR second = CPC subject_type = client_colony }`
- Lines 48764-48796: CPC country block (capital 2750, owns Cape provinces)
- CPC provinces: 132, 530, 1645, 2081, 2750, 2751, 3631, 5619, 5681, 6719, 6942, 7292, 7757, 7838, 8010, 8655, 9648

#### Target State
- Dutch VOC control (Governor Ryk Tulbagh, 1751-1771)
- Cape Town (2750) as capital
- Trekboer frontier expansion; Xhosa conflicts begin late 18thC (not yet 1763)

#### Option A: Repurpose DAF (Recommended)
1. **Delete line 907**: `dependency = { first = NED second = DAF subject_type = client_colony }` (currently points to Caribbean DAF)
2. **Delete lines 39258-39274**: Current DAF block (Caribbean)
3. **Change line 704**: `dependency = { first = GBR second = CPC subject_type = client_colony }` → `dependency = { first = NED second = DAF subject_type = client_colony }`
4. **Move CPC block (lines 48764-48796) → rename to DAF**:
   - Capital: 2750 (Cape Town)
   - Culture: `dutch` (not anglo_african)
   - Religion: `evangelical` (Dutch Reformed)
   - Government: `viceroyalty` (VOC administration)
   - Provinces: same as current CPC (lines 48774-48792)
5. **Ruler**: Add character for Governor Ryk Tulbagh (r. 1751-1771) — will need character block in setup

#### Option B: Create New Dutch Cape Tag (DCE or DCA)
1. Create `setup/countries/s_africa/dutch_cape.txt`
2. Add `DCE = "setup/countries/s_africa/dutch_cape.txt"` to countries.txt (line ~705 after CPC)
3. Replace line 704: `dependency = { first = NED second = DCE subject_type = client_colony }`
4. Create DCE country block (duplicate CPC structure, change culture/religion to Dutch)
5. Keep DAF as Caribbean (no change to line 907/39258-39274)

**RECOMMENDATION**: Option A (repurpose DAF) — cleaner, uses existing tag, DAF historically ambiguous (can mean "Dutch Africa" generically).

#### Required Area/Region References
- **Current CPC provinces** (lines 48774-48792): 132, 530, 1645, 2081, 2750, 2751, 3631, 5619, 5681, 6719, 6942, 7292, 7757, 7838, 8010, 8655, 9648
- **Cape region** (map_data/regions.txt): verify these provinces are in a "Cape" or "Southern Africa" region
- **Trekboer frontier**: Eastern Cape provinces (conflicts with Xhosa begin 1779, so in 1763 frontier is expanding but not yet contested)

**RISK**: If DAF is referenced elsewhere in events/missions as "Caribbean Dutch colony," those will break. User must global-search for DAF references.

---

### PHASE 2: SOKOTO CALIPHATE → INDEPENDENT HAUSA STATES

#### Current State (1815 Baseline)
- Line 550-555: SOK dependencies (LIP, GBI, ADM, GMB, BIU as feudatories)
- Lines 46859-46887: SOK country block (capital 10155, owns 14 provinces)
- Lines 46889-46905: ADM (Adamawa) as SOK feudatory
- Lines 46907+: GMB (Gombe) as SOK feudatory
- Lines 46943-46959: LIP (Liptako) as SOK feudatory
- Lines 46169-46185: GBI (Gobir) as SOK feudatory
- Line 555: BIU as SOK feudatory

#### Target State (1763)
- **Sokoto Caliphate does NOT exist** (founded 1804 via Usman dan Fodio's Fulani jihad)
- **Independent Hausa city-states** (Hausa Bakwai = "Seven True Hausa States"):
  1. **Kano** (major commercial center, trans-Saharan trade hub)
  2. **Katsina** (major commercial center, rival of Kano)
  3. **Zazzau/Zaria** (southern Hausa state)
  4. **Gobir** (northern, capital Alkalawa after 1715; rivalry with Zamfara; tensions with Fulani)
  5. **Daura** (legendary origin of Hausa states)
  6. **Rano** (near Kano)
  7. **Biram** (eastern)
- **Banza Bakwai** (illegitimate seven): often includes Zamfara, Kebbi, Nupe, Gwari, Yauri, Yoruba states (Oyo), etc. — less central to Hausaland proper

#### Edit Plan

##### A. DELETE Sokoto Overlordship
1. **Delete lines 550-555** (SOK dependencies):
   ```
   # Sokoto Caliphate Emirates
   dependency = { first = SOK second = LIP subject_type = feudatory } # Emirate
   dependency = { first = SOK second = GBI subject_type = feudatory } # Emirate
   dependency = { first = SOK second = ADM subject_type = feudatory } # Emirate
   dependency = { first = SOK second = GMB subject_type = feudatory } # Emirate
   dependency = { first = SOK second = BIU subject_type = feudatory } # Emirate
   ```
2. **Delete lines 46859-46887** (SOK country block) — entire block

##### B. MAKE Existing Tags Independent
- **GBI (Gobir)**: Lines 46169-46185 — already has country block, just remove dependency (step A1)
- **BIU**: Currently a SOK feudatory (line 555); need to verify if BIU has a country block or is only a province under SOK
- **ADM (Adamawa)**, **GMB (Gombe)**, **LIP (Liptako)**: These are FULANI emirates founded during the jihad (1804+) — should they exist in 1763?
  - **RECOMMENDATION**: DELETE ADM/GMB/LIP country blocks OR convert to independent Fulani pastoral polities (not emirates, not subjects)
  - **Research note**: Adamawa jihad was led by Modibo Adama (1806+); Gombe founded 1804; Liptako was a Fulani state but not a Sokoto emirate until later. In 1763, these areas were either Hausa-controlled or independent Fulani groups.
  - **DECISION NEEDED**: User must decide if ADM/GMB/LIP exist in 1763 as independent polities or are absorbed into Hausa states.

##### C. CREATE New Hausa City-State Tags (6 new tags)
Current: Only **GBI (Gobir)** exists as a Hausa state tag in countries.txt (line 631).

**Required New Tags**:
1. **KAN** (Kano) — `setup/countries/w_africa/kano.txt`
2. **KAT** (Katsina) — `setup/countries/w_africa/katsina.txt`
3. **ZAR** or **ZAZ** (Zazzau/Zaria) — `setup/countries/w_africa/zaria.txt`
4. **DAU** (Daura) — `setup/countries/w_africa/daura.txt`
5. **RAN** (Rano) — `setup/countries/w_africa/rano.txt`
6. **BIR** (Biram) — `setup/countries/w_africa/biram.txt`

**COLLISION CHECK**:
- KAN: Not in countries.txt ✓
- KAT: Not in countries.txt ✓
- ZAR: Not in countries.txt ✓ (ZAZ also free)
- DAU: Not in countries.txt ✓
- RAN: Not in countries.txt ✓
- BIR: Not in countries.txt ✓

**PROVINCE ALLOCATION** (from SOK block, lines 46869-46883):
SOK currently owns: 3416, 3429, 4322, 4707, 4718, 5237, 6069, 6920, 7678, 8416, 8472, 8967, 10155

These provinces must be redistributed to the new Hausa states. **User must verify via map_data/areas.txt which provinces correspond to which historical Hausa city-state**. Example allocation (PLACEHOLDER — user must verify):
- **Kano** (KAN): capital 10155 (or nearby), largest commercial center
- **Katsina** (KAT): capital 8416 (or nearby), rival of Kano
- **Zaria** (ZAR): capital 7678 (or nearby), southern Hausa
- **Gobir** (GBI): already has capital 6005 (line 46175) — keep as-is, make independent
- **Daura** (DAU): capital 3429 (or nearby)
- **Rano** (RAN): capital 6920 (or nearby), close to Kano
- **Biram** (BIR): capital 4322 (or nearby), eastern

**TEMPLATE for New Country Blocks** (insert after line 46885, replacing deleted SOK block):
```
KAN = { # Kano
    government = absolute_duchy  # or tribal_monarchy
    diplomatic_stance = appeasement_stance
    primary_culture = hausa
    religion = sunni

    capital = 10155  # PLACEHOLDER — user must verify Kano province ID

    own_control_core = {
        10155  # Kano city
        # [additional Kano-region provinces]
    }
}

KAT = { # Katsina
    government = absolute_duchy
    diplomatic_stance = appeasement_stance
    primary_culture = hausa
    religion = sunni

    capital = 8416  # PLACEHOLDER

    own_control_core = {
        8416
        # [additional Katsina provinces]
    }
}

ZAR = { # Zazzau/Zaria
    government = absolute_duchy
    diplomatic_stance = appeasement_stance
    primary_culture = hausa
    religion = sunni

    capital = 7678  # PLACEHOLDER

    own_control_core = {
        7678
        # [additional Zaria provinces]
    }
}

DAU = { # Daura
    government = absolute_duchy
    diplomatic_stance = appeasement_stance
    primary_culture = hausa
    religion = sunni

    capital = 3429  # PLACEHOLDER

    own_control_core = {
        3429
    }
}

RAN = { # Rano
    government = absolute_duchy
    diplomatic_stance = appeasement_stance
    primary_culture = hausa
    religion = sunni

    capital = 6920  # PLACEHOLDER

    own_control_core = {
        6920
    }
}

BIR = { # Biram
    government = absolute_duchy
    diplomatic_stance = appeasement_stance
    primary_culture = hausa
    religion = sunni

    capital = 4322  # PLACEHOLDER

    own_control_core = {
        4322
    }
}
```

**RULERS** (1763):
- Each Hausa state ruled by a **Sarki** (king). User must create character blocks for each ruler (generic or historical, if names known).

**REGION/AREA REFERENCES**:
- **Hausaland region**: map_data/regions.txt — likely includes Kano, Katsina, Zaria, Gobir, etc.
- **Areas**: User must cross-reference map_data/areas.txt to determine which provinces belong to which Hausa state historically.

**RISK**:
- **Tag collision**: Six new tags (low risk, all checked as free).
- **Province allocation**: If SOK provinces are not correctly split, some Hausa states may be too large/small or overlap.
- **Nested subjects**: If any of the deleted SOK feudatories (ADM/GMB/LIP) are themselves overlords, their subjects will orphan. User must check for nested dependencies.

---

### PHASE 3: OYO-DAHOMEY TRIBUTARY RELATIONSHIP

#### Current State (Line 1066)
```
dependency = { first = OYO second = DAH subject_type = tributary }
```

**STATUS**: **ALREADY CORRECT** for 1763. Oyo-Dahomey tributary relationship existed from 1730s to 1820s. Line 1066 shows Dahomey as tributary to Oyo.

#### Target State (1763)
- Oyo at territorial zenith (Alaafin Abiodun, r. 1754-1789)
- Dahomey pays annual tribute to Oyo (from 1730s after Oyo's 1726-1730 invasions)
- King Tegbesu of Dahomey (r. 1740-1774) is ruler in 1763

#### Edit Plan
**NO CHANGE REQUIRED**. Line 1066 is historically accurate for 1763.

**Ruler Changes** (not in 00_default.txt dependencies, but in character blocks if they exist):
- **Oyo**: Alaafin Abiodun (r. c. 1754-1789)
- **Dahomey**: King Tegbesu (r. 1740-1774)

---

### PHASE 4: ETHIOPIA — RULER CHANGE (Emperor Iyoas I)

#### Current State
- Lines 886-890: GDR (Gondar/Ethiopia) dependencies (TGR, SWA, WLO, GJJ as tributaries)
- GDR country block: (not read in full recon, assumed to exist in East Africa section)

#### Target State (1763)
- **Emperor Iyoas I** (r. 1755-1769), son of Empress Mentewab
- Pre-Zemene Mesafint (Era of Princes begins ~1769 after Iyoas's assassination)
- Ethiopia still centralized, though weakening

#### Edit Plan
1. **Dependencies**: NO CHANGE (lines 886-890 are correct — GDR tributaries existed in 1763)
2. **Ruler**: Change GDR character block (if ruler defined) to **Emperor Iyoas I** (r. 1755-1769)
   - **Note**: User must locate GDR character/ruler block in 00_default.txt (likely in East Africa section, not read in this recon)
   - **Placeholder ruler stats** (from research):
     - Name: Iyoas I
     - Birth: 1753 (age ~10 in 1763)
     - Reign: 1755-1769
     - Regent: Empress Mentewab (mother, regent during minority)
     - Traits: young, influenced by regent

**NO STRUCTURAL CHANGES** to Ethiopian tributaries — the 1763 empire structure is the same as 1815 in terms of tributary relationships.

---

### PHASE 5: SWAHILI COAST / OMANI EMPIRE

#### Current State
- Lines 44696-44728: OMA (Oman) country block
  - Capital: 7874 (Muscat)
  - Owns Swahili coast provinces: line 44711 = `1489 8950 7812 5895 1715` (Zanzibar, etc.)
- Lines 44731-44746: MZR (Mazrui/Mombasa) — separate polity, capital 8882 (Mombasa)
  - Owns: 8882, 937, 7412

#### Target State (1763)
- **Omani Empire** under Imam Ahmad bin Said Al Busaidi (r. 1749-1783)
- Oman controls Swahili coast cities (Kilwa, Mombasa, Pate, Lamu) via governors
- **Zanzibar NOT capital** (Omani capital is Muscat until 1832 when Said bin Sultan moves it)
- **Mazrui family** governs Mombasa (semi-autonomous, often rebellious, 1746-1837)

#### Edit Plan
**NO CHANGE REQUIRED**. Current baseline (lines 44696-44746) is already correct for 1763:
- OMA capital is Muscat (7874) ✓
- OMA owns Zanzibar (1489) and other Swahili coast provinces ✓
- MZR (Mazrui Mombasa) exists as separate polity ✓

**Ruler Change**:
- **Oman**: Change ruler (if defined) to **Imam Ahmad bin Said Al Busaidi** (r. 1749-1783)
- **Mazrui**: Mazrui governors (user must verify if ruler defined; family = Mazrui clan)

**DEPENDENCY QUESTION**: Is MZR a subject of OMA in the current baseline? Let me check:
- No dependency line found in lines 550-1068 for OMA→MZR.
- **DECISION NEEDED**: Should MZR be a protectorate/tributary of OMA in 1763? Historically, Mazrui were semi-autonomous governors under Oman, often rebellious.
- **RECOMMENDATION**: Add `dependency = { first = OMA second = MZR subject_type = protectorate }` (insert after line 890, in East Africa dependencies section)

---

### PHASE 6: WEST AFRICAN KINGDOMS (Ashanti, Oyo, Bornu, Kongo, Lunda)

#### A. ASHANTI (ATI)
- **Current**: Lines 46331-46353, capital 2571, owns 7 provinces
- **1763 Ruler**: Kusi Obodom (regent, d. 1764) or Osei Kwadwo (successor 1764)
- **Change**: Ruler only (if character block exists)
- **NO STRUCTURAL CHANGE**

#### B. OYO (OYO)
- **Current**: Lines 46607-46629, capital 492, owns 6 provinces
- **1763 Ruler**: Alaafin Abiodun (r. c. 1754-1789)
- **Change**: Ruler only
- **Dependency**: Line 1066 (OYO→DAH tributary) already correct ✓
- **NO STRUCTURAL CHANGE**

#### C. KANEM-BORNU (KBO)
- **Current**: Lines 46095-46113, capital 4083, owns 3 provinces
- **1763 Ruler**: Mai Dunama IX (r. c. 1747-1792)
- **Change**: Ruler only
- **Dependencies**: Lines 1001-1004 (KBO→MRG/BDE/DAM/KKO) — correct for 1763 ✓
- **NO STRUCTURAL CHANGE**

#### D. KONGO (KON)
- **Current**: Lines 47343-47360, capital 1366, owns 14 provinces
- **1763 Ruler**: King Pedro V (r. 1763-1764?) or late Sebastião I (d. 1764)
- **Change**: Ruler only
- **Note**: Research says Kongo is "fragmented by civil wars" in 1763, but the current 1815 baseline may already reflect this (no major structural change between 1763 and 1815 for Kongo — it's fragmented in both periods).
- **NO STRUCTURAL CHANGE**

#### E. LUNDA (LUN)
- **Current**: Lines 47477-47496, capital 7689, owns 4 provinces
- **1763 Ruler**: Mwant Yav (title of king) — generic or specific ruler name needed
- **Change**: Ruler only
- **NO STRUCTURAL CHANGE**

---

### PHASE 7: MINOR ADJUSTMENTS & ANACHRONISMS

#### A. ZULU / MFECANE STATES
- **1763**: No Zulu kingdom (founded c. 1816 by Shaka); fragmented Nguni chiefdoms
- **Current baseline**: No ZUL tag found in countries.txt (line 708 has ZUL defined but likely not in 1815 setup block)
- **Check**: User must verify if ZUL/MAT/LST (Zulu/Matabele/Lesotho) country blocks exist in 00_default.txt. If they do, DELETE them for 1763.
- **PLACEHOLDER**: Assuming these are not in the 1815 baseline (as Zulu kingdom is 1816+), no change needed.

#### B. MOROCCO (MOR)
- **Current**: Line 39038+ (not fully read)
- **1763**: Independent sultanate (Alaouite dynasty, Sultan Mohammed ben Abdallah, r. 1757-1790)
- **Cross-reference**: Ottoman recon will cover Maghreb (Algiers, Tunis, Tripoli as Ottoman vassals; Morocco independent)
- **NO CHANGE EXPECTED** for Morocco in this recon (defer to Ottoman recon)

#### C. PORTUGUESE AFRICA (Angola/Mozambique)
- **Current**: Lines 1015-1016 (POR→ANG/MOZ as client_colony)
- **1763**: Same structure (Portugal controls Luanda, Benguela, Mozambique Island, coastal settlements)
- **NO CHANGE**

#### D. FRENCH COASTAL AFRICA (FCA)
- **Current**: Line 1031 (FRA→FCA client_colony)
- **1763**: French forts in Senegambia (Saint-Louis, Gorée), Slave Coast
- **NO CHANGE** (FCA represents French coastal holdings in both 1763 and 1815)

#### E. DANISH GOLD COAST (DGC)
- **Current**: Line 917 (DEN→DGC client_colony)
- **1763**: Danish forts (Christiansborg/Osu)
- **NO CHANGE**

---

## IV. SUMMARY OF CHANGES: LINE-BY-LINE EDIT TABLE

| Action | Lines | Current | Target | Notes |
|--------|-------|---------|--------|-------|
| **DELETE** | 550-555 | SOK dependencies (6 lines) | (none) | Sokoto Caliphate does not exist in 1763 |
| **CHANGE** | 704 | `dependency = { first = GBR second = CPC...` | `dependency = { first = NED second = DAF...` | Cape is Dutch in 1763 (if Option A) |
| **DELETE** | 907 | `dependency = { first = NED second = DAF...` | (none) | DAF repurposed for Cape (if Option A) |
| **DELETE** | 39258-39274 | DAF country block (Caribbean) | (none) | Repurpose DAF for Cape (if Option A) |
| **DELETE** | 46859-46887 | SOK country block (29 lines) | (none) | Sokoto does not exist in 1763 |
| **CHANGE** | 46169-46185 | GBI country block (feudatory) | GBI independent | Remove SOK dependency (already done by deleting line 552) |
| **INSERT** | After 46887 | (none) | 6 new Hausa state blocks (KAN/KAT/ZAR/DAU/RAN/BIR) | ~150 lines (25 per state) |
| **MOVE+EDIT** | 48764-48796 | CPC country block | DAF country block (Dutch Cape) | If Option A: rename CPC→DAF, change culture/religion to Dutch |
| **INSERT** | After 890 | (none) | `dependency = { first = OMA second = MZR...` | Mazrui Mombasa as Omani protectorate (optional) |
| **CHANGE** | (character blocks, not found in recon) | Rulers for GDR/OYO/DAH/ATI/KBO/OMA | 1763 historical rulers | Iyoas I, Abiodun, Tegbesu, Kusi Obodom, Dunama IX, Ahmad bin Said |

**Total Lines Changed**: ~200 lines (deletions + insertions)

---

## V. NEW TAG REQUIREMENTS

### A. New Country Files to Create

| Tag | Filename | Culture | Religion | Capital (PLACEHOLDER) | Notes |
|-----|----------|---------|----------|----------------------|-------|
| **KAN** | setup/countries/w_africa/kano.txt | hausa | sunni | 10155 | Kano (major Hausa commercial center) |
| **KAT** | setup/countries/w_africa/katsina.txt | hausa | sunni | 8416 | Katsina (rival of Kano) |
| **ZAR** | setup/countries/w_africa/zaria.txt | hausa | sunni | 7678 | Zazzau/Zaria (southern Hausa) |
| **DAU** | setup/countries/w_africa/daura.txt | hausa | sunni | 3429 | Daura (legendary Hausa origin) |
| **RAN** | setup/countries/w_africa/rano.txt | hausa | sunni | 6920 | Rano (near Kano) |
| **BIR** | setup/countries/w_africa/biram.txt | hausa | sunni | 4322 | Biram (eastern Hausa) |

### B. countries.txt Additions (after line 670, in West Africa section)

```
# Hausa City-States (1763)
KAN = "setup/countries/w_africa/kano.txt"
KAT = "setup/countries/w_africa/katsina.txt"
ZAR = "setup/countries/w_africa/zaria.txt"
DAU = "setup/countries/w_africa/daura.txt"
RAN = "setup/countries/w_africa/rano.txt"
BIR = "setup/countries/w_africa/biram.txt"
```

### C. Localization (common/localization/*.yml)

Add localization entries for the 6 new tags:
```yml
KAN: "Kano"
KAN_ADJ: "Kanoan"
KAT: "Katsina"
KAT_ADJ: "Katsinan"
ZAR: "Zaria"
ZAR_ADJ: "Zarian"
DAU: "Daura"
DAU_ADJ: "Dauran"
RAN: "Rano"
RAN_ADJ: "Ranoan"
BIR: "Biram"
BIR_ADJ: "Biraman"
```

---

## VI. RISKS & COLLISIONS

### A. Tag Collisions
- **KAN/KAT/ZAR/DAU/RAN/BIR**: All checked against countries.txt — **NO COLLISIONS** ✓

### B. Nested Subject Orphans
- **SOK deletion**: Check if ADM/GMB/LIP/BIU (former SOK feudatories) are themselves overlords of other tags.
  - **Found**: No nested dependencies in lines 550-1068 for ADM/GMB/LIP/BIU.
  - **Safe to delete SOK overlordship** ✓

### C. Province Allocation Conflicts
- **SOK provinces** (lines 46869-46883): 14 provinces must be redistributed to 6+ new Hausa states.
  - **RISK**: If map_data/areas.txt does not clearly delineate Hausa city-state territories, provinces may overlap or be misallocated.
  - **MITIGATION**: User must cross-reference map_data/areas.txt and historical Hausa state maps (e.g., Lovejoy 2005, Last 1967) to assign provinces correctly.

### D. Cape Ownership
- **DAF repurpose**: If DAF is referenced in events/missions as "Caribbean Dutch colony," those references will break.
  - **MITIGATION**: Global-search for `DAF` in events/ and missions/ directories. Replace with new Caribbean tag if needed (e.g., DWI = Dutch West Indies).

### E. Ruler Character IDs
- **1763 rulers**: If character IDs are hardcoded in 00_default.txt (e.g., `ruler = 12345`), changing rulers requires creating new character blocks.
  - **RECON LIMITATION**: Character blocks not fully read in this recon. User must locate and edit ruler assignments.

---

## VII. AREA/REGION CROSS-REFERENCES (TO VERIFY)

User must cross-reference the following with map_data/areas.txt and regions.txt:

### A. Cape Region
- **CPC provinces** (lines 48774-48792): 132, 530, 1645, 2081, 2750, 2751, 3631, 5619, 5681, 6719, 6942, 7292, 7757, 7838, 8010, 8655, 9648
- **Expected areas**: Cape Peninsula, Western Cape, Eastern Cape (Trekboer frontier)
- **Neighboring regions**: Xhosa territories (eastern), Khoikhoi/San lands (northern)

### B. Hausaland Region
- **SOK provinces to redistribute** (lines 46869-46883): 3416, 3429, 4322, 4707, 4718, 5237, 6069, 6920, 7678, 8416, 8472, 8967, 10155
- **Expected areas**: Kano, Katsina, Zaria, Gobir, Daura, Rano, Biram (historical city-state centers)
- **Historical references**:
  - Kano: major trans-Saharan trade hub, walled city
  - Katsina: rival of Kano, also trans-Saharan trade
  - Zaria: southern Hausa, cavalry power
  - Gobir: northern Hausa, capital Alkalawa (post-1715)
  - Daura, Rano, Biram: smaller states

### C. Swahili Coast Region
- **OMA Swahili provinces** (line 44711): 1489 (Zanzibar), 8950, 7812, 5895, 1715
- **MZR provinces** (line 44741): 8882 (Mombasa), 937, 7412
- **Expected areas**: Kilwa, Zanzibar, Mombasa, Lamu, Pate (coastal city-states)

---

## VIII. OPEN QUESTIONS FOR USER DECISION

1. **Cape Colony Tag**: Option A (repurpose DAF) or Option B (create new DCE/DCA tag)?
   - **Recommendation**: Option A (cleaner, uses existing tag)

2. **Hausa Province Allocation**: Which provinces (from SOK's 14) go to which of the 6 new Hausa states?
   - **Requires**: map_data/areas.txt cross-reference + historical Hausa city-state territorial maps

3. **ADM/GMB/LIP in 1763**: Do these Fulani polities exist in 1763 as independent states, or should they be deleted/absorbed?
   - **Research context**: These are Fulani emirates founded during the 1804+ jihad. In 1763, Fulani were pastoral groups, not organized emirates.
   - **Recommendation**: DELETE ADM/GMB/LIP country blocks (lines 46889-46959) OR convert to generic Fulani pastoral polities (not emirates, not subjects).

4. **BIU (Biu)**: Is BIU a separate polity or just a province under SOK? If separate, it should be independent in 1763.
   - **Requires**: Check if BIU country block exists beyond line 555 dependency.

5. **OMA→MZR Dependency**: Should Mazrui Mombasa be a protectorate of Oman in 1763?
   - **Historical**: Semi-autonomous governors under Oman, often rebellious (1746-1837)
   - **Recommendation**: Add `dependency = { first = OMA second = MZR subject_type = protectorate }`

6. **Morocco (MOR)**: Defer to Ottoman recon or handle here?
   - **Recommendation**: Defer to Ottoman recon (Maghreb coverage)

---

## IX. EXECUTION CHECKLIST

### Pre-Edit
- [ ] Read map_data/areas.txt to identify Hausa city-state areas
- [ ] Read map_data/regions.txt to verify Cape/Hausaland/Swahili Coast regions
- [ ] Decide: DAF repurpose (Option A) or new DCE tag (Option B)?
- [ ] Decide: ADM/GMB/LIP in 1763 (delete or convert)?
- [ ] Decide: OMA→MZR protectorate dependency (add or skip)?

### Phase 1: Cape (British → Dutch)
- [ ] Delete line 907 (NED→DAF Caribbean)
- [ ] Delete lines 39258-39274 (DAF Caribbean block)
- [ ] Change line 704 (GBR→CPC) to (NED→DAF)
- [ ] Move CPC block (48764-48796) → rename DAF, edit culture/religion to Dutch
- [ ] Create character block for Governor Ryk Tulbagh (r. 1751-1771)
- [ ] Global-search for `DAF` in events/missions — replace Caribbean references if needed

### Phase 2: Sokoto → Hausa States
- [ ] Delete lines 550-555 (SOK dependencies)
- [ ] Delete lines 46859-46887 (SOK country block)
- [ ] Allocate SOK's 14 provinces to 6 new Hausa states (using areas.txt)
- [ ] Create 6 new country files (kano.txt, katsina.txt, zaria.txt, daura.txt, rano.txt, biram.txt)
- [ ] Add 6 new tags to countries.txt (after line 670)
- [ ] Insert 6 new country blocks in 00_default.txt (after line 46887, ~150 lines)
- [ ] Add localization for 6 new tags (*.yml)
- [ ] Decide fate of ADM/GMB/LIP (delete or convert)
- [ ] Verify GBI (Gobir) is independent (dependency removed by step 1)

### Phase 3: Oyo-Dahomey
- [ ] Verify line 1066 (OYO→DAH tributary) — NO CHANGE needed ✓

### Phase 4: Ethiopia
- [ ] Locate GDR character/ruler block (East Africa section, not in this recon)
- [ ] Change ruler to Emperor Iyoas I (r. 1755-1769)
- [ ] Dependencies (lines 886-890) — NO CHANGE ✓

### Phase 5: Swahili Coast
- [ ] Verify OMA capital is Muscat (7874) — NO CHANGE ✓
- [ ] Verify MZR (Mazrui) exists — NO CHANGE ✓
- [ ] (Optional) Insert `dependency = { first = OMA second = MZR...` after line 890
- [ ] Change OMA ruler to Imam Ahmad bin Said (r. 1749-1783)

### Phase 6: West African Kingdoms
- [ ] Change ATI ruler to Kusi Obodom/Osei Kwadwo (1763)
- [ ] Change OYO ruler to Alaafin Abiodun (1754-1789)
- [ ] Change KBO ruler to Mai Dunama IX (1747-1792)
- [ ] Change KON ruler to King Pedro V/Sebastião I (1763)
- [ ] Change DAH ruler to King Tegbesu (1740-1774)
- [ ] Change LUN ruler to Mwant Yav (generic title)

### Phase 7: Minor Adjustments
- [ ] Verify no ZUL/MAT/LST country blocks exist in 1815 baseline (delete if present)
- [ ] Verify POR→ANG/MOZ (lines 1015-1016) — NO CHANGE ✓
- [ ] Verify FRA→FCA (line 1031) — NO CHANGE ✓
- [ ] Verify DEN→DGC (line 917) — NO CHANGE ✓

### Post-Edit
- [ ] Run game to main menu — check for script errors
- [ ] Load 1763 bookmark — verify African tags exist and are independent/subject as planned
- [ ] Check Cape is Dutch-controlled (DAF or DCE)
- [ ] Check Hausa states are independent (no SOK)
- [ ] Check Dahomey is tributary to Oyo
- [ ] Check Swahili coast is Omani (OMA + MZR)

---

## X. APPENDIX: KEY RESEARCH SOURCES (from 1763_WORLD_Africa.md)

- **Last, Murray.** (1967). *The Sokoto Caliphate*. Longmans. [Hausa states, Sokoto formation]
- **Law, Robin.** (1977). *The Oyo Empire c.1600–c.1836*. Oxford: Clarendon Press. [Oyo-Dahomey]
- **Bay, Edna G.** (1998). *Wives of the Leopard: Gender, Politics, and Culture in the Kingdom of Dahomey*. University of Virginia Press. [Dahomey, Tegbesu]
- **Wilks, Ivor.** (1975). *Asante in the Nineteenth Century*. Cambridge University Press. [Asante, covers late 18thC context]
- **Giliomee, Hermann.** (2003). *The Afrikaners: Biography of a People*. University of Virginia Press. [Cape Colony, VOC]
- **Marcus, Harold G.** (2002). *A History of Ethiopia* (updated ed.). University of California Press. [Ethiopia, Iyoas I]
- **Sheriff, Abdul.** (1987). *Slaves, Spices and Ivory in Zanzibar*. James Currey. [Omani East Africa, Swahili coast]
- **Lovejoy, Paul E.** (2012). *Transformations in Slavery: A History of Slavery in Africa* (3rd ed.). Cambridge University Press. [Hausa states, trans-Saharan trade]
- **Brenner, Louis.** (1973). *The Shehus of Kukawa: A History of the al-Kanemi Dynasty of Bornu*. Oxford: Clarendon Press. [Bornu, Dunama IX]

---

## END OF DOCUMENT

**Next Steps**: User must make the decisions outlined in Section VIII, verify area/region mappings in Section VII, and execute the checklist in Section IX. This document provides the blueprint; user provides the map data and executes the edits.
