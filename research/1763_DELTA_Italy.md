# 1763 Italy Delta: Edit Plan

**Repo**: `/Users/alan.chiang/github.com/imp19c`  
**Branch**: `1763_bookmark`  
**Target date**: 16 February 1763  
**Context**: Phase 1 registered VEN, GEN, MIL tags and gave VEN ~13 provinces. Phase 2 must give GEN and MIL their provinces and adjust the rest of Italian 1763 states.

---

## CURRENT BASELINE (1815)

### Tags registered in `setup/countries/countries.txt`

**Present**:
- Line 62: **VEN** (Venice) — `setup/countries/italy/venice.txt`
- Line 63: **GEN** (Genoa) — `setup/countries/italy/genoa.txt`
- Line 64: **MIL** (Milan) — `setup/countries/italy/milan.txt`
- Line 65: **LUC** (Lucca)
- Line 66: **MCO** (Monaco)
- Line 67: **MOD** (Modena)
- Line 68: **MSS** (Massa-Carrara)
- Line 69: **NAP** (Naples)
- Line 70: **PAP** (Papal States)
- Line 71: **PRM** (Parma)
- Line 72: **SAR** (Sardinia)
- Line 73: **SIC** (Sicily)
- Line 74: **SMR** (San Marino)
- Line 75: **SSL** (Two Sicilies) — NOT needed for 1763; Naples + Sicily separate
- Line 76: **TUS** (Tuscany)
- Line 61: **LBV** (Lombardy-Venetia) — NOT needed for 1763; Austrian fusion entity

### Country blocks in `setup/main/00_default.txt`

#### VEN (Venice) — Line 40729–40757
- **Government**: oligarchic_republic
- **Capital**: 1135 (Venice city)
- **Provinces** (13): 1135, 6085, 573, 29, 6740, 1237, 3605, 9291, 9308, 9418, 522, 5067, 9970
- **Status**: Independent

#### GEN (Genoa) — **NOT PRESENT** (registered but no country block)

#### MIL (Milan) — **NOT PRESENT** (registered but no country block)

#### SAR (Sardinia) — Line 40582–40630
- **Government**: absolute_kingdom
- **Family**: 15 (Savoy)
- **Capital**: 1264 (Turin)
- **Provinces** (32): 19, 33, 644, 655, 1148, 1218, 1232, 1264, 1447, 1774, 1776, 2321, 2374, 2997, 4059, 4565, 4974, **5494**, 5715, **6103**, 6121, 6733, 7378, 7393, 8059, 8635, 9363, 9463, 9762, 9766, **6416**, 8768
  - **Liguria subset** (bold): 5494, 6103, 6416 — these must move to GEN
- **Dependencies**: `dependency = { first = SAR second = MCO subject_type = protectorate }` (Monaco)

#### AUS (Austria) — Line 36390–36643+
- **Government**: imperial_monarchy
- **Family**: 8 (Habsburg-Lothringen)
- **Capital**: 245 (Vienna)
- **Provinces** (partial extract, Italian-relevant):
  - **Veneto**: 1146, 1760
  - **Friuli**: 6685, 8561, 8687
  - **Dalmatia**: 1596, 1608, 4921, 6214, 8236, 8375
  - **Plus** Bohemia, Galicia, Hungary, Croatia, etc.
- **Issue**: Austria holds Venetian terra firma + Dalmatia in this baseline; in 1763 these are VENETIAN.

#### TUS (Tuscany) — Line 40839–40865
- **Government**: absolute_duchy
- **Capital**: 5528 (Florence)
- **Provinces** (11): 2848, 5479, 5542, 6860, 7521, 8315, 9024, 5528, 3882, 975, 13163
- **Status**: Habsburg-Lorraine (Grand Duke Francis I Stephen; shares family with AUS)

#### MOD (Modena) — Line 40671–40728
- **Government**: absolute_duchy
- **Family**: 45 (Este)
- **Provinces**: (not read in detail)

#### PRM (Parma) — Line 40650–40669
- **Government**: absolute_duchy
- **Family**: 54 (Bourbon)
- **Provinces**: 8041, 6729

#### PAP (Papal States) — Line 40885–40928
- **Government**: catholic_papacy
- **Capital**: 8830 (Rome)
- **Provinces** (17): 1207, 1433, 2198, 2263, 2896, 3558, 4877, 4937, 6088, 6101, 6844, 7595, 8830, 8964, 9443, 9835

#### NAP (Naples) — Line 40948–41005
- **Government**: absolute_kingdom
- **Family**: 35 (Bourbon)
- **Capital**: 4278 (Naples)
- **Provinces** (31): 200, 832, 820, 2334, 3947, 3951, 4055, 4278, 4290, 4550, 4971, 6381, 6794, 7193, 7322, 7382, 7398, 7904, 8100, 8104, 8288, 8296, 8306, 8631, 8802, 9047, 9089, 9101, 9222, 9518

#### SIC (Sicily) — Line 41007–41036
- **Government**: viceroyalty
- **Capital**: 8178 (Palermo)
- **Provinces** (14): 8178, 9368, 8907, 8911, 9386, 5457, 3446, 9700, 9629, 9293, 1820, 10233, 10303

#### LUC (Lucca) — Line 40795–40812
- **Government**: absolute_duchy
- **Provinces**: 3148, 4439

#### MSS (Massa-Carrara) — Line 38835–38851
- **Government**: absolute_duchy
- **Provinces**: 6150

#### SMR (San Marino) — Line 40930–40946
- **Government**: directorial_republic
- **Provinces**: 6356

#### MCO (Monaco) — Line 40632–40648
- **Government**: absolute_principality
- **Provinces**: 678
- **Dependencies**: subject to SAR

#### FRA (France) — Line 34426–34494
- Holds **Corsica** (357, 2910, 4636, 9042) in 1815 baseline

---

## 1763 TARGET (from `research/1763_WORLD_Italy.md`)

### Political Map

| **1763 State** | **Status** | **Capital** | **Ruler/Notes** |
|----------------|------------|-------------|-----------------|
| **Republic of Venice** | **Independent** | Venice | Doge Marco Foscarini; terra firma + Istria + Dalmatia + Ionian Islands |
| **Republic of Genoa** | **Independent** | Genoa | Doge Brignole Sale; Liguria + Corsica (nominal; Paoli revolt) |
| **Duchy of Milan** | **Austrian possession** | Milan | Maria Theresa governor; Lombardy E of Ticino |
| Kingdom of Sardinia | Independent (Savoy) | Turin | Charles Emmanuel III; Piedmont + Savoy + Sardinia island + **W Lombardy to Ticino** |
| Grand Duchy of Tuscany | Independent (Habsburg-Lorraine) | Florence | Francis I Stephen; Tuscany + Elba |
| Duchy of Parma | Independent (Bourbon) | Parma | Philip (Don Filippo); Parma + Piacenza |
| Duchy of Modena | Independent (Este) | Modena | Francesco III; Modena + Reggio + Massa-Carrara |
| Republic of Lucca | Independent | Lucca | Oligarchic republic |
| Papal States | Independent | Rome | Pope Clement XIII; Lazio + Umbria + Marche + Romagna |
| Kingdom of Naples | Independent (Bourbon) | Naples | Ferdinand IV (minor); mainland south |
| Kingdom of Sicily | Personal union with Naples | Palermo | Ferdinand III = IV; island |
| San Marino | Independent | San Marino | Republic |
| Monaco | French protectorate | Monaco | Honoré III Grimaldi |

### Key Area Definitions (from `map_data/areas.txt`)

- **Lombardy**: 16, 29, 513, 1104, 1195, 2371, 6740, 7341, 9445
- **Liguria**: 5494, 6103, 6416
- **Veneto**: 573, 1135, 1146, 1237, 1760, 3605, 4881, 5067, 6085, 9308, 9418
- **Friuli**: 522, 6685, 8561, 8687, 9291, 9970, 10105
- **Dalmatia**: 1596, 1608, 4921, 6214, 8236, 8375, 10538, 10714
- **Corsica**: 357, 2910, 4636, 9042
- **Tuscany**: (not extracted; TUS provinces appear correct)
- **Sardinia** (island): (part of SAR baseline; not changed)

---

## DELTA PLAN: 1815 → 1763

### A. TAG CREATION

#### 1. **GEN (Genoa)** — NEW country block after SAR (insert ~line 40631)

**Action**: Create country block for GEN.

```
		GEN = {
			government = oligarchic_republic
			diplomatic_stance=appeasement_stance
			primary_culture = north_italian
			religion = catholic

			capital = 6103					# Genoa city (infer from Liguria)

			#is_antagonist = yes

			own_control_core = 	{
				5494					# Liguria
				6103
				6416
				357						# Corsica (nominal; Paoli revolt 1755–1769)
				2910
				4636
				9042
			}

			#professional_soldiers = yes
			#organized_recruitment = yes
		}
```

**Notes**:
- **Capital**: 6103 is most likely Genoa city (verify by cross-checking population or name; if wrong, use 5494 or 6416).
- **Corsica**: Nominally Genoese in 1763 but in revolt (Paoli); ceded to France 1768. Include for now; can add event chain for revolt/cession later.

---

#### 2. **MIL (Milan)** — NEW country block as Austrian subject (insert ~line 40759, before VEN)

**Action**: Create country block for MIL + dependency.

**Country block** (insert ~line 40759):

```
		MIL = {
			government = viceroyalty				# Or absolute_duchy; Austrian-administered
			diplomatic_stance=appeasement_stance
			primary_culture = north_italian
			religion = catholic

			capital = 29							# Milan city (most likely; verify)

			#is_antagonist = yes

			own_control_core = 	{
				16									# Lombardy E of Ticino (Austrian Milan)
				29
				513
				1104
				1195
				2371
				7341
				9445
				# NOTE: 6740 may be on border; research shows Ticino River = SAR/MIL boundary. 
				# If 6740 = W of Ticino → leave with SAR; if E → move to MIL.
				# RECOMMENDATION: Cross-check province 6740 location. For now, EXCLUDE (leave with VEN or transfer to SAR).
			}

			#professional_soldiers = yes
			#organized_recruitment = yes
		}
```

**Dependency** (insert in dependency list ~line 516, after POL-LIT line):

```
	dependency = { first = AUS second = MIL subject_type = royal_union }		# [bookmark-1763 #208] Austrian Duchy of Milan (Lombardy); Habsburg possession from 1706; governed by Count Firmian
```

**Notes**:
- **Capital**: Province 29 is most likely Milan city (in Lombardy area).
- **Province 6740**: Currently held by VEN. Research states Milan = "Lombardy E of Ticino"; 6740's geographic position unclear. **DECISION NEEDED**: If 6740 = Como (N Lombardy), it's Austrian; if W of Ticino, Sardinian. For safety, EXCLUDE from MIL for now; manually verify location. If it should be Sardinian, add to SAR. If Milanese, add to MIL.
- **Subject type**: `royal_union` models personal union (shares Habsburg ruler); alternately `protectorate` or `client_state`. Oracle research suggests royal_union works for shared-dynasty subjects.

---

### B. PROVINCE TRANSFERS

#### 3. **SAR (Sardinia) → GEN (Genoa)**: Transfer Liguria

**Action**: Remove 5494, 6103, 6416 from SAR `own_control_core` (line 40592–40626).

**File**: `setup/main/00_default.txt`  
**Line**: 40592–40626 (SAR block)

**Current** (lines 40592–40626):
```
			own_control_core = 	{
				19
				33
				644
				655
				1148
				1218
				1232
				1264
				1447
				1774
				1776
				2321
				2374
				2997
				4059
				4565
				4974
				5494					← REMOVE
				5715
				6103					← REMOVE
				6121
				6733
				7378
				7393
				8059
				8635
				9363
				9463
				9762
				9766
				6416					← REMOVE
				8768
			}
```

**Target**:
```
			own_control_core = 	{
				19
				33
				644
				655
				1148
				1218
				1232
				1264
				1447
				1774
				1776
				2321
				2374
				2997
				4059
				4565
				4974
				5715
				6121
				6733
				7378
				7393
				8059
				8635
				9363
				9463
				9762
				9766
				8768
			}
```

**Rationale**: In 1763, Liguria (Genoa region) is independent Republic of Genoa. Sardinia gains Genoa only in 1815 (Congress of Vienna). The 1815 baseline reflects post-Napoleonic annexation.

---

#### 4. **VEN (Venice) ↔ AUS (Austria)**: Transfer Venetian terra firma + Dalmatia

**Action**:
- **Remove from AUS**: Veneto (1146, 1760), Friuli (6685, 8561, 8687), Dalmatia (1596, 1608, 4921, 6214, 8236, 8375)
- **Add to VEN**: Same provinces

**File**: `setup/main/00_default.txt`

##### 4a. **AUS provinces to remove** (line 36444–36643)

**Current AUS extract** (Italian-relevant provinces, line 36444+):
```
			own_control_core = 	{
				... [Bohemia, Galicia, Hungary omitted] ...
				1146					← REMOVE (Veneto)
				...
				1596					← REMOVE (Dalmatia)
				...
				1608					← REMOVE (Dalmatia)
				...
				1760					← REMOVE (Veneto)
				...
				4921					← REMOVE (Dalmatia)
				...
				6214					← REMOVE (Dalmatia)
				...
				6685					← REMOVE (Friuli)
				...
				8236					← REMOVE (Dalmatia)
				8375					← REMOVE (Dalmatia)
				...
				8561					← REMOVE (Friuli)
				...
				8687					← REMOVE (Friuli)
				...
			}
```

**Action**: Delete lines containing 1146, 1596, 1608, 1760, 4921, 6214, 6685, 8236, 8375, 8561, 8687 from AUS block.

**Exact line numbers**: NOT PROVIDED (file too large; must search in context). Perform:
```bash
grep -n "1146\|1596\|1608\|1760\|4921\|6214\|6685\|8236\|8375\|8561\|8687" setup/main/00_default.txt | grep -A2 -B2 "36444"
```
to find exact lines in AUS block, then delete.

##### 4b. **VEN provinces to add** (line 40729–40753)

**Current VEN** (line 40739–40753):
```
			own_control_core = 	{
				1135					# Venice city
				6085					# Veneto
				573						# Veneto
				29						← ISSUE (Lombardy; should this be Austrian MIL or Venetian?)
				6740					← ISSUE (Lombardy; Ticino boundary unclear)
				1237					# Veneto
				3605					# Veneto
				9291					# Friuli
				9308					# Veneto
				9418					# Veneto
				522						# Friuli
				5067					# Veneto
				9970					# Friuli
			}
```

**Target** (add from AUS + resolve Lombardy issue):
```
			own_control_core = 	{
				1135					# Venice city
				6085					# Veneto
				573						# Veneto
				1146					# Veneto (from AUS)
				1237					# Veneto
				1760					# Veneto (from AUS)
				3605					# Veneto
				4881					# Veneto (missing? Check baseline)
				5067					# Veneto
				6085					# [duplicate? check]
				9308					# Veneto
				9418					# Veneto
				522						# Friuli
				6685					# Friuli (from AUS)
				8561					# Friuli (from AUS)
				8687					# Friuli (from AUS)
				9291					# Friuli
				9970					# Friuli
				10105					# Friuli (missing? Check baseline)
				1596					# Dalmatia (from AUS)
				1608					# Dalmatia (from AUS)
				4921					# Dalmatia (from AUS)
				6214					# Dalmatia (from AUS)
				8236					# Dalmatia (from AUS)
				8375					# Dalmatia (from AUS)
				10538					# Dalmatia (missing? Check baseline)
				10714					# Dalmatia (missing? Check baseline)
				# IONIAN ISLANDS: NOT in area files searched; research states VEN holds Corfu, Cephalonia, Zante, etc. 
				# These are in ION (Ionian Isles) tag (line 40759–40775), currently British viceroyalty in 1815.
				# ACTION NEEDED: Transfer ION provinces to VEN OR create event for 1797 Campo Formio (VEN → AUS, then ION → GBR 1815).
			}
```

**Lombardy issue** (provinces 29, 6740):
- **Province 29**: In Lombardy area. Research: Milan (Austrian) = "Lombardy E of Ticino"; Sardinia = "W Lombardy to Ticino". 
  - **DECISION**: If 29 = Milan city, it's Austrian → move to MIL. If W of Ticino, keep with SAR.
  - **Current owner in baseline**: VEN. This is WRONG for both 1763 scenarios (should be AUS/MIL or SAR, NOT VEN).
  - **ACTION**: **Remove 29 from VEN**; add to **MIL** (most likely Milan city).
- **Province 6740**: In Lombardy area. Same Ticino boundary question.
  - **Current owner**: VEN. Also wrong.
  - **ACTION**: **Remove 6740 from VEN**. If Como (N Lombardy E of Ticino) → add to **MIL**. If Novara/Vercelli (W of Ticino) → add to **SAR**.
  - **RECOMMENDATION**: Cross-check province names via `setup/provinces/*.txt` or in-game. For now, tentatively assign **6740 to MIL** (more likely Austrian than Venetian).

**Rationale**: In 1763, Venice is independent and controls Venetia + Istria + Dalmatia + Ionian Islands. Austria holds these only after 1797 (Treaty of Campo Formio). The 1815 baseline reflects Austrian annexation.

---

#### 5. **FRA (France) → GEN (Genoa)**: Transfer Corsica

**Action**: Remove Corsica (357, 2910, 4636, 9042) from FRA (line 34472–34489).

**File**: `setup/main/00_default.txt`  
**Line**: 34472–34489 (FRA block)

**Current** (line 34472+):
```
			own_control_core = 	{
				... [mainland France] ...
				357 ...					← REMOVE (Corsica)
				...
				2910 ...				← REMOVE (Corsica)
				...
				4636 ...				← REMOVE (Corsica)
				...
				9042 ...				← REMOVE (Corsica)
				...
			}
```

**Target**: Delete 357, 2910, 4636, 9042 from FRA block.

**Rationale**: Corsica ceded to France 1768 (Treaty of Versailles). In 1763, nominally Genoese (though in Paoli revolt). Transfer to GEN.

---

### C. IONIAN ISLANDS (VEN vs ION)

**Issue**: Research states Venice holds Ionian Islands (Corfu, Cephalonia, Zante, etc.) in 1763. Current baseline:
- **ION (Ionian Isles)** tag exists (line 40759–40775), holds 380, 6377, 7504, 13164.
- ION is a **British viceroyalty** in 1815 (after Napoleonic wars; Treaty of Paris 1815).

**Historical chain**:
1. 1763: Venetian Stato da Màr
2. 1797: Campo Formio → Venice extinguished, Ionian Islands to France (then briefly Russia 1799, then France again 1807)
3. 1815: British protectorate (Treaty of Paris)

**Action for 1763**:
- **Option A**: Merge ION provinces into VEN (no separate ION tag in 1763).
- **Option B**: Keep ION as Venetian subject (royal_union or protectorate).

**RECOMMENDATION**: **Option A** (merge into VEN). ION is not a separate polity in 1763; it's Venetian overseas territory.

**Edit**:
1. Add ION provinces (380, 6377, 7504, 13164) to VEN `own_control_core`.
2. Delete ION country block (line 40759–40775).
3. For 1815 bookmark (if future start dates added), restore ION as British viceroyalty.

---

### D. MINOR ADJUSTMENTS

#### 6. **NAP + SIC separation** (already correct)

- **NAP** (Naples) and **SIC** (Sicily) are separate country blocks in baseline.
- In 1763, they share ruler (Ferdinand IV/III) in personal union.
- In 1815, they're merged into **SSL** (Two Sicilies).

**Action for 1763**: Add dependency:
```
	dependency = { first = NAP second = SIC subject_type = royal_union }		# [bookmark-1763 #208] Bourbon personal union: Ferdinand IV of Naples = Ferdinand III of Sicily (same ruler, legally distinct kingdoms until 1816)
```

**Insert**: After SAR-MCO dependency (line ~517).

---

#### 7. **MCO (Monaco) protectorate**

**Current**: `dependency = { first = SAR second = MCO subject_type = protectorate }` (line ~517).

**1763 status**: Research states Monaco is **French protectorate** (Treaty of Péronne 1641).

**Action**: Change to:
```
	dependency = { first = FRA second = MCO subject_type = protectorate }		# [bookmark-1763 #208] French protectorate since 1641 (Treaty of Péronne); shifts to Sardinian sphere 1815
```

**Rationale**: Sardinian protectorate is post-1815 (Congress of Vienna). In 1763, Monaco is French-aligned.

---

#### 8. **TUS (Tuscany) family**

**Current**: TUS block (line 40839–40865) has no `family` key.

**1763 status**: Grand Duke Francis I Stephen of Lorraine (Habsburg-Lorraine), married to Maria Theresa; shares dynasty with AUS (family 8).

**Action**: Add to TUS block (after `religion = catholic`, line ~40843):
```
			family = 8						# Habsburg-Lorraine (Grand Duke Francis I Stephen, r. 1737–1765)
```

---

#### 9. **LUC (Lucca) government**

**Current**: LUC (line 40795–40812) government = `absolute_duchy`.

**1763 status**: Oligarchic republic (Council of Elders).

**Action**: Change (line 40796):
```
			government = oligarchic_republic
```

---

#### 10. **MSS (Massa-Carrara) merger with MOD**

**1763 status**: Duchess Maria Teresa Cybo-Malaspina rules Massa-Carrara, married to Ercole III d'Este (Duke of Modena) → personal union.

**Current**: MSS (line 38835–38851) and MOD (line 40671–40728) are separate, no dependency.

**Action**: Add dependency (after NAP-SIC line):
```
	dependency = { first = MOD second = MSS subject_type = royal_union }		# [bookmark-1763 #208] Personal union: Duchess Maria Teresa Cybo-Malaspina (Massa) married to Duke Ercole III d'Este (Modena), 1741–1790
```

---

### E. PROVINCE VERIFICATION NEEDED

**Action**: Before finalizing, cross-check province IDs to resolve:

1. **Province 29**: Milan city? If yes, add to MIL. If not, determine location (E or W of Ticino).
2. **Province 6740**: Como (Austrian)? Novara (Sardinian)? Determine and assign to MIL or SAR.
3. **Veneto missing provinces**: 4881 (in Veneto area but not in VEN or AUS baseline) — who holds it? Same for Friuli 10105, Dalmatia 10538/10714.
4. **Ionian Islands exact provinces**: Confirm 380 = Corfu, 6377/7504/13164 = other islands.
5. **Corsica capital**: Which of 357, 2910, 4636, 9042 is Bastia (Genoese administrative center)?

**Method**: Search `setup/provinces/*.txt` or use in-game console `debug_mode` + province tooltips.

---

## SUMMARY: EXACT EDITS BY FILE

### 1. `setup/main/00_default.txt`

#### A. **CREATE GEN block** (insert after SAR, ~line 40631)
- Copy-paste template from Section A.1 above.

#### B. **CREATE MIL block** (insert before VEN, ~line 40759)
- Copy-paste template from Section A.2 above.

#### C. **EDIT SAR block** (line 40592–40626)
- **Remove** lines with: 5494, 6103, 6416

#### D. **EDIT AUS block** (line 36444–36643)
- **Remove** lines with: 1146, 1596, 1608, 1760, 4921, 6214, 6685, 8236, 8375, 8561, 8687
- **Search command** (to find exact line numbers):
  ```bash
  grep -n "^\s*1146$\|^\s*1596$\|^\s*1608$\|^\s*1760$\|^\s*4921$\|^\s*6214$\|^\s*6685$\|^\s*8236$\|^\s*8375$\|^\s*8561$\|^\s*8687$" setup/main/00_default.txt | awk -F: '$1 > 36444 && $1 < 36644'
  ```

#### E. **EDIT VEN block** (line 40739–40753)
- **Remove**: 29, 6740
- **Add**: 1146, 1760, 6685, 8561, 8687, 1596, 1608, 4921, 6214, 8236, 8375
- **Add** (Ionian Islands, from ION): 380, 6377, 7504, 13164
- **Result**: VEN = Veneto + Friuli + Dalmatia + Ionian Islands (full Venetian Republic terra firma + Stato da Màr minus Crete/Cyprus)

#### F. **EDIT FRA block** (line 34472–34489)
- **Remove**: 357, 2910, 4636, 9042

#### G. **DELETE ION block** (line 40759–40775)
- Remove entire country block (merged into VEN).

#### H. **EDIT TUS block** (line 40839–40865)
- **Add** after line 40843 (`religion = catholic`):
  ```
  			family = 8
  ```

#### I. **EDIT LUC block** (line 40795–40812)
- **Change** line 40796:
  ```
  			government = oligarchic_republic
  ```

#### J. **ADD dependencies** (insert after line 516, in dependency list section)

**Insert** (4 new lines):
```
	dependency = { first = AUS second = MIL subject_type = royal_union }		# [bookmark-1763 #208] Austrian Duchy of Milan (Lombardy E of Ticino); Habsburg possession from 1706
	dependency = { first = NAP second = SIC subject_type = royal_union }		# [bookmark-1763 #208] Bourbon personal union: Ferdinand IV of Naples = Ferdinand III of Sicily (1759–1816)
	dependency = { first = MOD second = MSS subject_type = royal_union }		# [bookmark-1763 #208] Personal union: Duchess Maria Teresa Cybo-Malaspina (Massa) married to Duke Ercole III d'Este (Modena)
	dependency = { first = FRA second = MCO subject_type = protectorate }		# [bookmark-1763 #208] French protectorate since 1641; shifts to Sardinia 1815
```

**Modify** existing SAR-MCO dependency (line ~517):
- **Delete** line: `dependency = { first = SAR second = MCO subject_type = protectorate }`
- (Replaced by FRA-MCO above.)

---

### 2. NO CHANGES NEEDED

- `setup/countries/countries.txt` — VEN, GEN, MIL already registered (Phase 1).
- `map_data/areas.txt` — No province reassignments; areas unchanged.
- Character/history files — Out of scope (Phase 2 is map only).

---

## RISKS AND COLLISIONS

### 1. **Tag Collision**: None identified
- TRI = Tripoli (N Africa), not Trier (HRE). No Italian collision.
- All Italian tags (VEN, GEN, MIL, SAR, TUS, MOD, PRM, PAP, NAP, SIC, LUC, MSS, SMR, MCO) are distinct.

### 2. **Province ID ambiguity**
- **29, 6740**: Assigned to wrong owner in baseline (VEN); must resolve Ticino boundary to assign to MIL or SAR.
- **4881, 10105, 10538, 10714**: Missing from both VEN and AUS; determine current owner before adding to VEN.

### 3. **Nested subjects**
- MIL (subject of AUS) is NOT a subject of another tag → safe.
- Oracle research confirms nested subjects work (e.g., CHI → ILI → XNG).

### 4. **Ionian Islands**
- Merging ION into VEN removes ION tag. If 1815 bookmark is later restored, ION must be recreated as British viceroyalty.

### 5. **Corsica revolt**
- Assigning Corsica to GEN reflects nominal sovereignty. Paoli revolt (1755–1769) could be modeled via:
  - Rebel occupation (not modeled in setup).
  - Event chain for revolt + French cession 1768.
  - For Phase 2 (map only), include in GEN; mark for future event work.

---

## VALIDATION CHECKLIST

After edits, verify:

1. **Game boots** on 1763 bookmark without crash.
2. **Tag definitions**:
   - VEN, GEN, MIL exist and have provinces.
   - ION tag removed (or provinces empty if kept as placeholder).
3. **Province ownership**:
   - SAR does NOT hold Liguria (5494, 6103, 6416).
   - GEN holds Liguria + Corsica.
   - AUS does NOT hold Veneto/Friuli/Dalmatia (1146, 1760, 6685, 8561, 8687, 1596, 1608, 4921, 6214, 8236, 8375).
   - VEN holds Veneto + Friuli + Dalmatia + Ionian Islands.
   - MIL holds Lombardy (resolve 29, 6740).
   - FRA does NOT hold Corsica.
4. **Dependencies**:
   - AUS → MIL (royal_union)
   - NAP → SIC (royal_union)
   - MOD → MSS (royal_union)
   - FRA → MCO (protectorate)
   - SAR-MCO dependency REMOVED.
5. **Minor states**:
   - TUS has `family = 8`.
   - LUC has `government = oligarchic_republic`.

---

## NEXT STEPS (Out of Scope for Phase 2)

1. **Rulers and characters**: Assign Doge Marco Foscarini (VEN), Doge Brignole Sale (GEN), Count Firmian (MIL governor), etc.
2. **Corsica revolt**: Event chain for Paoli uprising + French cession 1768.
3. **Venice extinction**: Event chain for 1797 Campo Formio (VEN → AUS annexation).
4. **1815 restoration**: If alternate start dates added, restore LBV (Lombardy-Venetia), ION (British), merge NAP+SIC → SSL.
5. **Economic scripts**: Venetian glass (Murano), Genoese banking, Milanese silk.
6. **Mission trees**: Venice decline, Genoa Corsica crisis, Austrian Lombardy reforms.

---

**END PLAN**
