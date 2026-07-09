# 1763 Americas Delta Plan

**Status**: In progress
**Branch**: 1763_bookmark
**Generated**: 2026-07-03

## Executive Summary

This document specifies the exact edits required to convert the 1815 Americas baseline to 1763 (Treaty of Paris +6 days). The 1815 baseline ALREADY models Spanish/Portuguese colonial trees; the 1763 delta is NARROW territorial/subject/character corrections, not a rebuild.

### Scope: 10 Core Edits + Character Fix

1. **USA → British Thirteen Colonies**: Convert USA tag (line 35029, owns ~70 provinces) to GBR colonial subject OR assign provinces to GBR directly
2. **Florida → Britain**: Transfer FLO from NSP tributary (line 766) to GBR client_colony
3. **Louisiana partition**: Split MSP tag's Deep_South provinces — west of Mississippi → SPA/NSP (Spanish Louisiana), east → GBR (Illinois Country)
4. **Canada/Quebec → Britain**: Activate CAN tag (registered, unused) as GBR subject; assign Quebec/Saint-Laurent regions
5. **Haiti → French colony**: Convert HAI tag (line 35000, owns Hispaniola) to FRA subject OR split Haiti area (FRA) / Dominicana area (SPA)
6. **Río de la Plata → Peru subject**: Assign empty Argentina + Paraguay + Uruguay regions to NEW subject (RPL/BUE) under PR1, or to PR1 directly
7. **New Granada restoration**: Create SPA → NGR dependency (line ~758, NGR was independent in 1815); NGR = Viceroyalty of New Granada (1763)
8. **Venezuela → New Granada subject**: Make VNZ (currently independent, line 41152) a subject of NGR; review VNZ's own subjects TNJ/CAU/ANQ
9. **Ecuador → Peru subject**: Change QTO overlord from SPA (line 759) to PR1 (Audiencia of Quito under Lima in 1763, not New Granada)
10. **Cuba/Caribbean check**: Verify Cuba/Puerto Rico/Santo Domingo representation (no CUB/PRI/DOM tags found); if modeled, group under NSP or create CUB subject
11. **MEX ruler fix**: Replace José María Morelos (char:15, birth 1765.09.30, UNBORN) with Joaquín de Montserrat (Viceroy 1760-1766) in setup/characters/00_North America.txt line ~577

### Status of 1815 Baseline Components

**CORRECT (no change required)**:
- SPA → NSP (New Spain), NSP → GUA/PHI/SEM/ALC ✓
- SPA → PR1 (Peru), PR1 → CHR (Charcas/Upper Peru) + CHL (Chile) ✓
- POR → BRZ (Brazil) ✓
- Spanish colonial government types (viceroyalty) ✓

**INCORRECT for 1763**:
- USA independent republic (should be British colony)
- HAI independent (should be French Saint-Domingue)
- FLO under NSP (should be under GBR, Treaty of Paris transfer)
- QTO under SPA (should be under PR1/Peru in 1763)
- VNZ independent (should be under NGR/New Granada)
- NGR independent (should be under SPA as viceroyalty)

**MISSING**:
- British Canada (CAN tag registered but not active)
- Spanish Louisiana (west of Mississippi, from France 1762)
- British trans-Appalachian territory (east of Mississippi, from France 1763)
- Río de la Plata organization under Peru (Buenos Aires + hinterland)

### High-Priority Risks

1. **USA tag references**: If events/missions assume USA independence, conversion to British subject breaks content (requires grep audit)
2. **Louisiana geography**: Mississippi River split requires manual province-by-province assignment (no engine delineation)
3. **Empty Río de la Plata**: Buenos Aires area appears unowned in 1815 — verify before assigning
4. **TNJ/CAU/ANQ tags**: VNZ subjects (lines 1043-1045) — unknown entities, may be 1815-specific, need investigation
5. **Bookmark coexistence**: If 1763 is SECOND bookmark (not replacing 1815), need start-date conditionals on ALL dependency/character changes

### Key Findings

- Río de la Plata tags (ARG/PRY/URU) do NOT exist in 1815 setup → correct (should not exist in 1763 either; territory under PR1/Peru)
- USA/HAI exist and own provinces in 1815 → MUST convert to British Thirteen Colonies and French Saint-Domingue
- Florida currently NSP tributary (line 766) → MUST transfer to GBR
- MSP (Mississippi) tag exists (line 35258) representing Deep South → must split for Louisiana partition
- MEX ruler char:15 (Morelos b.1765) is unborn at 1763.2.16 → MUST change to avoid crash

## 1815 Baseline Verification

**Spanish America dependency chain (setup/main/00_default.txt lines 757-771):**
- Line 759: SPA → QTO (client_colony)
- Line 760: SPA → PR1 (client_colony, Peru)
- Line 761: PR1 → CHR (autonomous_governorship)
- Line 762: PR1 → CHL (autonomous_governorship)
- Line 763: SPA → NSP (client_colony, New Spain)
- Line 764: NSP → GUA (autonomous_governorship, Guatemala)
- Line 765: SPA → SFB (client_colony)
- Line 766: NSP → FLO (tributary) **[1763 DELTA: must transfer to GBR]**
- Line 767: NSP → SEM (tributary)
- Line 768: NSP → PHI (autonomous_governorship, Philippines)
- Line 769: NSP → ALC (territory, Alta California)
- Line 770: SPA → CPV (client_colony, Cape Verde)
- Line 771: SPA → MEX (client_colony) **[tagged #208 for 1763 conversion]**

**Portuguese America (line 899):**
- Line 899: POR → BRZ (client_colony) **[CORRECT for 1763]**

**Venezuela subjects (lines 1043-1045):**
- Line 1043: VNZ → TNJ (protectorate)
- Line 1044: VNZ → CAU (protectorate)
- Line 1045: VNZ → ANQ (protectorate)
- **NOTE**: VNZ exists as independent tag in 1815; in 1763, should be under New Granada (NGR). Line 758 comment shows NGR was independent confederacy in 1815.

**Tags that OWN provinces in 1815:**
- USA: capital 1533, owns territory **[MUST convert to British colonies]**
- HAI: capital 733, owns territory **[MUST convert to French Saint-Domingue]**
- MEX: viceroyalty government (correct), ruler char:15 **[MUST fix unborn ruler]**

**Tags MISSING from 1815 (correctly):**
- ARG, PRY, URU (Río de la Plata): correct absence — territory should be under PR1/Peru in 1763
- CUB, DOM, PRI (Caribbean): need to check if represented under NSP
- GCO, COL (Gran Colombia/Colombia): need to check if under NGR
- PER, BOL (Peru proper, Upper Peru): need to check if under PR1

**Tags REGISTERED but unused:**
- CAN (setup/countries/n_america/canada.txt): exists but not in setup **[MUST add as British Quebec]**
- USA (setup/countries/n_america/usa.txt): exists and used in 1815 **[MUST replace with British colonies or remove]**

## 1763 Target State

Per research/1763_WORLD_Americas.md Treaty of Paris settlement:

**North America:**
- **Thirteen Colonies** → BRITISH (tag GBR or colonial subjects)
  - Currently: USA tag owns capital 1533 + ~70 provinces (New England, Mid-Atlantic, South)
  - Target: Must convert to British authority
- **Canada/Quebec** → BRITISH (NEW from France)
  - Currently: No active CAN tag (registered but unused); Quebec/Saint-Laurent regions exist
  - Target: Must create British Quebec or assign to GBR
- **Florida** → BRITISH (NEW from Spain, Treaty of Paris)
  - Currently: FLO tributary of NSP (line 766)
  - Target: Must transfer FLO to GBR overlord or dissolve and give provinces to GBR
- **Louisiana WEST of Mississippi + New Orleans** → SPANISH (NEW from France, Treaty of Fontainebleau 1762)
  - Currently: MSP (Mississippi) tag exists with Deep South provinces; Deep_South region includes Louisiana + Florida areas
  - Target: Must check which provinces are Louisiana west vs east of river; west → SPA/NSP, east → GBR
- **Louisiana EAST of Mississippi** → BRITISH (from France)
  - Target: Illinois Country, trans-Appalachian territory → GBR

**Spanish America:**
- **Viceroyalty of New Spain** (SPA → NSP) ✓ correct at line 763
  - Subjects: GUA (Guatemala) ✓ line 764, PHI (Philippines) ✓ line 768, ALC (Alta California) ✓ line 769, SEM ✓ line 767
  - MEX currently SPA → MEX (line 771) with viceroyalty government ✓ — BUT MEX is the viceroyalty capital's representation; check if separate or merged
- **Captaincy-General of Cuba** → under New Spain
  - Cuba, Puerto Rico, Santo Domingo should be NSP subjects or SPA direct
  - Currently: No CUB/PRI/DOM tags found in setup — likely unrepresented or merged into NSP/SPA holdings
- **Viceroyalty of Peru** (SPA → PR1) ✓ correct at line 760
  - PR1 owns core Peru region ✓
  - Subjects: CHR (Charcas/Upper Peru) ✓ line 761, CHL (Chile) ✓ line 762
  - CHR owns Upper_Peru region (La Paz 2439/2932, Potosí 2128/4432/5281 confirmed)
  - **Argentina/Paraguay/Uruguay** (Río de la Plata) — MUST be under PR1 in 1763
    - Currently: Buenos Aires area (535, 2064, etc.) NOT found in any own_control_core → likely EMPTY
    - Target: Must assign Argentina + Paraguay + Uruguay regions to PR1 OR create a Río de la Plata subject under PR1
- **Viceroyalty of New Granada** (SPA → NGR)
  - Currently: Line 758 comment says NGR was "independent confederacy" in 1815 — so NOT under SPA
  - Target: Must create SPA → NGR dependency; Ecuador (QTO) must move from SPA (line 759) to NGR or PR1 depending on 1763 status
  - Research says QTO under PERU in 1763 (transferred back from New Granada 1751)
- **Captaincy-General of Venezuela** (under New Granada)
  - Currently: VNZ independent with subjects TNJ/CAU/ANQ (lines 1043-1045)
  - Target: VNZ must become subject of NGR (loosely organized in 1763 per research)

**Portuguese America:**
- **Estado do Brasil** (POR → BRZ) ✓ correct at line 899
  - Capital Rio de Janeiro (moved 1763, exact year)

**French America:**
- **Saint-Domingue** (western Hispaniola) → FRENCH
  - Currently: HAI tag owns capital 733 + 12 provinces (Haiti + Dominicana areas = full Hispaniola)
  - Target: Must convert HAI to French colony OR split Haiti region (western = FRA, eastern = SPA Santo Domingo)

**Caribbean:**
- Cuba region → Spanish (under NSP)
- Antilles (Puerto Rico, Jamaica, Lesser Antilles) → check ownership split British/French/Spanish/Dutch

## Delta: Required Changes

### A. North America — United States → British Thirteen Colonies

**FINDING**: USA tag (line 35029) owns capital 1533 + extensive territory (New_England, Appalachia, eastern seaboard regions).

**REQUIRED CHANGE**:
1. **Option 1 (colonial subject model)**: Convert USA to British colonial subject
   - Change line 35029 USA government from `constitutional_republic` to colonial type (e.g., `colonial_government` or `viceroyalty`)
   - Add dependency line after line 899: `dependency = { first = GBR second = USA subject_type = client_colony }`
   - USA represents the Thirteen Colonies as a unified subject (like NSP/New Spain)
   
2. **Option 2 (direct British rule)**: Dissolve USA, assign provinces to GBR
   - Delete USA country block (lines 35029-35200, approx)
   - Add all USA provinces to GBR own_control_core
   - RISK: Large province list for one country; harder to model colonial administration

**RECOMMENDATION**: Option 1 (colonial subject) matches existing Spanish Americas pattern and preserves the 1815→1763 upgrade path.

### B. North America — Florida Transfer

**CURRENT STATE**: Line 766: `dependency = { first = NSP second = FLO subject_type = tributary }`

**REQUIRED CHANGE**: Florida ceded to Britain in Treaty of Paris 1763.
- **Option 1**: Change line 766 to `dependency = { first = GBR second = FLO subject_type = client_colony }`
- **Option 2**: Dissolve FLO tag, assign Florida area provinces (from Deep_South region) to GBR directly
- **Option 3**: Make FLO subject of USA (if USA becomes British colonial subject) — WRONG, Florida was separate British colony

**RECOMMENDATION**: Option 1 (GBR → FLO) — East/West Florida were distinct British colonies 1763-1783.

### C. North America — Louisiana and Mississippi River Partition

**CURRENT STATE**: MSP tag (line 35258) owns Deep South provinces including Louisiana area.

**REQUIRED CHANGE**: Treaty of Paris partitions Louisiana:
- **West of Mississippi River + New Orleans** → SPAIN (via Treaty of Fontainebleau 1762, confirmed 1763)
- **East of Mississippi River** → BRITAIN (Illinois Country, trans-Appalachian)

**PROVINCE-LEVEL TASK** (requires manual mapping):
1. Read Deep_South region areas (Louisiana, Arkansas, Mississippi, Alabama, Georgia, South_Carolina, Florida)
2. Read Louisiana area provinces from map_data/areas.txt
3. Determine which provinces are west vs east of Mississippi River (may need map inspection or geographic knowledge)
4. WEST provinces: assign to SPA or NSP (Spanish Louisiana should be NSP subject)
5. EAST provinces: assign to GBR or USA (if USA is British colonial subject)
6. New Orleans (check capital of Louisiana area): must go to SPA/NSP (Spanish)

**COMPLICATION**: MSP tag in 1815 represents post-1812 Mississippi/Deep South states (after Louisiana Purchase 1803, Mississippi Territory, Alabama, etc.). The 1763 partition is DIFFERENT — Louisiana as a whole doesn't exist as one polity; it's split French→Spanish (west) and French→British (east).

**OPTIONS**:
- **Option A**: Keep MSP tag, rename to "Spanish Louisiana" (LOU?), assign only west-of-Mississippi provinces, change to NSP subject
- **Option B**: Dissolve MSP, assign west provinces to NSP or new LOU subject, east provinces to GBR/USA
- **Option C**: Create two tags: SLO (Spanish Louisiana, NSP subject) and BLO (British Louisiana/Illinois Country, GBR subject)

**RECOMMENDATION**: Option B or C — the Treaty of Paris partition is load-bearing for 1763 start. Need definitive province list.

### D. North America — Canada/Quebec

**CURRENT STATE**: CAN tag registered (setup/countries/n_america/canada.txt) but NOT active in 1815 setup. Quebec region (areas: Quebec, Saint-Laurent) exists on map.

**REQUIRED CHANGE**: Britain acquires New France (Canada) in Treaty of Paris 1763.
- **Must create** CAN tag as British subject OR assign Quebec/Ontario regions to GBR directly
- Quebec region provinces: need to check current ownership (likely FRA or unowned/indigenous)

**ACTION**:
1. Check if FRA owns Quebec region provinces in 1815 setup (if so, transfer to GBR)
2. If unowned, assign to GBR or create CAN subject
3. Add dependency line: `dependency = { first = GBR second = CAN subject_type = client_colony }` (if using CAN tag)

### E. Caribbean — Haiti → French Saint-Domingue

**CURRENT STATE**: HAI tag (line 35000) owns capital 733 + 12 provinces, covers Haiti + Dominicana areas (= full Hispaniola island).

**REQUIRED CHANGE**: In 1763, western Hispaniola = French Saint-Domingue, eastern Hispaniola = Spanish Santo Domingo.

**OPTIONS**:
1. **Convert HAI to French colony**: Change HAI government to colonial type, add `dependency = { first = FRA second = HAI subject_type = client_colony }`
2. **Split Hispaniola**: 
   - Haiti area provinces → FRA or new FHA (French Haiti) subject
   - Dominicana area provinces → SPA or NSP subject (Santo Domingo was under Captaincy-General of Cuba, under New Spain)

**COMPLICATION**: HAI in 1815 represents independent Haiti (post-1804 revolution). The tag name suggests independence. For 1763, using HAI as French colony is anachronistic but pragmatic IF government/subject status is set correctly.

**RECOMMENDATION**: Option 1 (convert HAI to FRA subject) for minimal edits, OR Option 2 (split) for historical accuracy (separate French and Spanish holdings).

### F. South America — Río de la Plata Under Peru

**CURRENT STATE**: 
- Argentina, Paraguay, Uruguay regions exist on map
- Buenos Aires area (provinces 535, 2064, 2077, 2689, 3038, 3660, etc.) NOT found in any own_control_core → **EMPTY/unowned**
- Paraguay region: need to check ownership
- Uruguay area: need to check ownership

**REQUIRED CHANGE**: Viceroyalty of Río de la Plata does NOT exist in 1763 (created 1776). Territory under Viceroyalty of Peru (PR1).

**OPTIONS**:
1. **Assign to PR1 directly**: Add Argentina + Paraguay + Uruguay region provinces to PR1 own_control_core (line 39991+)
2. **Create subject under PR1**: Create a Río de la Plata subject tag (RPL? BUE?) under PR1, similar to CHR (Charcas/Upper Peru)
   - Add dependency line: `dependency = { first = PR1 second = RPL subject_type = autonomous_governorship }`

**RECOMMENDATION**: Option 2 (create subject) matches the viceroyalty structure — Peru had subordinate audiencias. Buenos Aires Audiencia exists 1661-1671, re-established 1783 — but in 1763, it's governed from Lima. Use autonomous_governorship like CHR/CHL.

**ACTION**: Populate Buenos Aires, Cordoba_Argentina, Santa_Fe, Mesopotamia, Tucuman, Salta areas + Paraguay area + Uruguay area → new RPL or BUE tag → PR1 subject.

### G. South America — Venezuela Under New Granada

**CURRENT STATE**: VNZ tag (line 41152) independent with subjects TNJ/CAU/ANQ (lines 1043-1045).

**REQUIRED CHANGE**: In 1763, Venezuela is under Viceroyalty of New Granada (though Captaincy-General of Venezuela not formally established until 1777).

**OPTIONS**:
1. **Make VNZ subject of NGR**: Add `dependency = { first = NGR second = VNZ subject_type = client_colony }` or `autonomous_governorship`
2. **Dissolve VNZ subjects**: TNJ/CAU/ANQ → either remove or make direct VNZ subjects (but research doesn't mention these as 1763 entities)

**COMPLICATION**: Line 758 comment says NGR was "independent confederacy" in 1815 → so NGR exists in 1815 but NOT as Spanish subject. Must create SPA → NGR dependency for 1763.

**ACTION**:
1. Add line ~758: `dependency = { first = SPA second = NGR subject_type = client_colony }` (Viceroyalty of New Granada)
2. Add line after 1045: `dependency = { first = NGR second = VNZ subject_type = autonomous_governorship }`
3. Review TNJ/CAU/ANQ tags (what are these? check setup for definitions)

### H. South America — Ecuador/Quito Under Peru (Not New Granada)

**CURRENT STATE**: Line 759: `dependency = { first = SPA second = QTO subject_type = client_colony }`

**REQUIRED CHANGE**: Research says "Audiencia of Quito under Viceroyalty of PERU in 1763 (transferred back from New Granada 1751-1802)."

**ACTION**: Change line 759:
- FROM: `dependency = { first = SPA second = QTO subject_type = client_colony }`
- TO: `dependency = { first = PR1 second = QTO subject_type = autonomous_governorship }`

QTO should be a subject of Peru (PR1), not Spain directly, in 1763.

### I. Character Fix — MEX Ruler José María Morelos

**CURRENT STATE**: setup/characters/00_North America.txt line 577: `set_as_ruler=char:15` (José María Morelos, birth_date=1765.09.30)

**PROBLEM**: Morelos born 1765, game start 1763.02.16 → **UNBORN RULER** (will crash or error).

**REQUIRED CHANGE**: Replace with a 1763-appropriate viceroy for New Spain.

**OPTIONS**:
1. **Use historical viceroy**: Research lists "Joaquín de Montserrat, Marqués de Cruilles (Viceroy 1760-1766)" as Viceroy of New Spain in 1763
   - Create new character or point to existing Montserrat character
2. **Auto-generate**: Use a generic Spanish administrator if no historical character exists
3. **Remove ruler assignment**: Let MEX start without a set ruler (game will generate one) — RISKY, may cause issues

**RECOMMENDATION**: Option 1 (historical viceroy). Check if "Joaquín de Montserrat" or "Cruilles" exists in Spanish character files; if not, create.

### J. Caribbean — Cuba, Puerto Rico, Santo Domingo Representation

**CURRENT STATE**: No CUB, PRI, DOM tags found in setup.

**QUESTION**: Are Cuban/Puerto Rican/Dominican provinces represented?
- Cuba region (area: Cuba) → need to check ownership (likely SPA or NSP direct)
- Antilles region (areas: Puerto_Rico, Virgin_Islands, Jamaica, Lesser_Antilles, Curacao) → need to check ownership split

**REQUIRED CHANGE**: In 1763, Cuba/Puerto Rico/Santo Domingo under Captaincy-General of Cuba (subordinate to New Spain).

**ACTION** (requires investigation):
1. Grep Cuba area provinces from map_data/areas.txt
2. Check setup/main/00_default.txt for current owners
3. If SPA owns directly, consider creating CUB subject under NSP
4. Puerto Rico, Santo Domingo (eastern Hispaniola) similarly

**OPTIONS**:
- **Option A**: Keep as NSP direct holdings (provinces in NSP own_control_core)
- **Option B**: Create CUB tag as NSP subject, assign Cuba + Puerto Rico + Santo Domingo provinces

**RECOMMENDATION**: Check current state first; if provinces are modeled, Option B (create CUB subject) for consistency with viceroyalty/captaincy-general structure.

## Province/Area Moves

This section specifies REGIONS and AREAS (not individual province IDs) to move. Exact province lists must be extracted from map_data/areas.txt.

### North America

**USA → GBR colonial subject** (or GBR direct):
- REGIONS: New_England, Appalachia, and portions of Deep_South (eastern seaboard)
- AREAS (New_England region): Maine, New_Hampshire, Vermont, Massachusetts, Connecticut
- AREAS (Appalachia and Mid-Atlantic — need to verify region assignments): Pennsylvania areas, New York areas, Virginia areas, Carolina areas, Georgia (if not in Deep_South)
- ACTION: Read USA own_control_core (line ~35040+), cross-reference with areas.txt to identify which areas are included

**Florida → GBR**:
- AREA: Florida (from Deep_South region)
- CURRENT OWNER: FLO tag (tributary of NSP)
- ACTION: Transfer FLO subject from NSP to GBR (dependency line 766)

**Louisiana partition**:
- AREA: Louisiana (from Deep_South region) — need to split west vs east of Mississippi River
- WEST of Mississippi → SPA/NSP (Spanish Louisiana)
- EAST of Mississippi → GBR (British Illinois Country)
- AREAS potentially affected: Arkansas, parts of Mississippi area, Illinois Country (need to verify if Illinois area exists or is part of broader region)
- CURRENT OWNER: MSP tag (line 35258) owns Deep_South provinces
- ACTION: Manual province-level split based on Mississippi River geography; may require map inspection

**Canada/Quebec → GBR**:
- REGION: Quebec (areas: Quebec, Saint-Laurent)
- REGION: Ontario (area: Ontario) — if this is French-held Great Lakes interior in 1815
- CURRENT OWNER: Unknown (likely FRA or unowned); need to check FRA own_control_core
- ACTION: Assign to GBR or CAN subject of GBR

### Caribbean

**Haiti → FRA colonial subject**:
- REGION: Haiti (areas: Haiti, Dominicana)
- CURRENT OWNER: HAI tag (line 35000)
- ACTION: If splitting Hispaniola, Haiti area → FRA, Dominicana area → SPA/NSP (Santo Domingo)

**Cuba/Puerto Rico/Santo Domingo → NSP subject**:
- REGION: Cuba (area: Cuba)
- AREAS from Antilles region: Puerto_Rico, Lesser_Antilles (British/French/Dutch split), Jamaica (British)
- CURRENT OWNER: Unknown; need to check SPA/NSP/GBR own_control_core
- ACTION: Assign Cuba + Puerto_Rico + Dominicana (if split from Haiti) to CUB subject of NSP, OR keep as NSP direct holdings

### South America

**Argentina + Paraguay + Uruguay → PR1 (or PR1 subject)**:
- REGION: Argentina (areas: Buenos_Aires, La_Pampa, Mendoza_Argentina, Cordoba_Argentina, San_Juan, La_Rioja, Salta, Tucuman, Santa_Fe, Mesopotamia, Chaco)
- REGION: Paraguay (area: Paraguay)
- AREA: Uruguay (from Haiti region or separate — need to verify)
- CURRENT OWNER: Appears EMPTY (Buenos Aires province 535 not found in any own_control_core)
- ACTION: Create RPL or BUE subject of PR1, assign all Argentina + Paraguay + Uruguay areas to it

**Ecuador/Quito → PR1 subject** (from SPA direct):
- REGION: Ecuador (areas: Sierra_de_Ecuador, Costa_de_Ecuador, Amazonas_de_Ecuador)
- CURRENT OWNER: QTO tag, subject of SPA (line 759)
- ACTION: Change dependency line 759 from `first = SPA` to `first = PR1`

**Venezuela → NGR subject**:
- REGION: Venezuela (areas: Venezuela, Zulia, Apure, Orinoco, Coro, Los_Llanos)
- CURRENT OWNER: VNZ tag (line 41152), independent with own subjects
- ACTION: Make VNZ subject of NGR; check TNJ/CAU/ANQ tags (current VNZ subjects, lines 1043-1045) for historical accuracy

**Upper Peru/Charcas → PR1 subject** (ALREADY CORRECT):
- REGION: Upper_Peru (areas: Beni_y_Pando, Santa_Cruz, La_Paz, Oruro, Potosi, Tarija_y_Chuquisaca)
- CURRENT OWNER: CHR tag (line 40046), subject of PR1 ✓
- NO CHANGE REQUIRED

**Chile → PR1 subject** (ALREADY CORRECT):
- REGION: Chile (areas: Chile_Central, Chile_del_Sur, Norte_Chico, Norte_Grande)
- CURRENT OWNER: CHL tag (line 39388), subject of PR1 ✓
- NO CHANGE REQUIRED

**Colombia → NGR direct** (or NGR subject):
- REGION: Colombia (areas: Cauca, Tolima, Choco, Cartagena, Santander, Magdalena, Cundinamarca, Antioquia, Azuay)
- CURRENT OWNER: Unknown; need to check NGR own_control_core (if NGR tag exists in 1815 as independent, it likely owns these)
- ACTION: Ensure NGR exists and is SPA subject (client_colony) for 1763

### Other Americas

**Brazil → POR subject** (ALREADY CORRECT):
- REGIONS: Northeast_Brazil, North_Brazil, and central/southern Brazil regions
- CURRENT OWNER: BRZ tag (line 39587), subject of POR ✓
- NO CHANGE REQUIRED

## Character Fixes

### MEX Ruler — José María Morelos (UNBORN)

**FILE**: setup/characters/00_North America.txt, line ~577

**CURRENT**:
```
15={
    first_name="Jose Maria"
    family_name = "Morelos"
    birth_date=1765.09.30
    ...
    c:MEX={
        set_as_ruler=char:15
    }
}
```

**PROBLEM**: Morelos born 1765.09.30, game start 1763.02.16 → unborn at start (2.5 years in the future). This will crash or produce error when MEX country initializes.

**SOLUTION**:
Replace with historical Viceroy of New Spain (1763): **Joaquín de Montserrat, Marqués de Cruilles** (Viceroy 1760-1766, per research).

**STEPS**:
1. Check if Montserrat/Cruilles character exists in setup/characters/00_Spain.txt or related Spanish character files
2. If exists: change `set_as_ruler=char:15` to `set_as_ruler=char:XXXX` (Montserrat's ID)
3. If NOT exists: create new character block in Spanish characters or MEX block:
   ```
   15={  # or new ID if 15 is reserved
       first_name="Joaquin"
       family_name = "de Montserrat"
       nickname = "Cruilles"  # or append to family_name
       birth_date=1710.01.01  # approximate, historical dates unknown
       culture="castilian"
       religion="catholic"
       add_martial=5
       add_charisma=6
       add_finesse=7
       add_zeal=4
       add_trait="administrator"  # or appropriate viceregal trait
       c:MEX={
           set_as_ruler=char:15
       }
   }
   ```
4. OR: Use auto-generation — remove `set_as_ruler` line, let game generate a ruler (RISKY, may not have appropriate stats/culture)

**RECOMMENDATION**: Create Montserrat character (Option 3 above) if not in Spanish roster.

### Other Potential Character Issues

**VNZ ruler** (if VNZ becomes NGR subject): Check if VNZ has a set ruler; if anachronistic (post-1763 birth), replace with colonial governor.

**HAI ruler** (if HAI becomes FRA subject): Check if HAI has a set ruler for independent Haiti (post-1804 revolutionary leader?); if so, replace with French colonial governor (Saint-Domingue governor 1763).

**USA ruler** (if USA becomes GBR subject): Check if USA has a set ruler; if it's a post-1776 president, replace with British colonial governor or leave unset.

**ACTION**: Grep setup/characters files for rulers set for VNZ, HAI, USA tags; verify birth dates and roles against 1763 context.

## Risks and Dependencies

### High-Risk Changes

1. **USA → British conversion**
   - RISK: USA tag may be referenced in events, missions, scripts elsewhere in the mod
   - IMPACT: If USA is converted to British subject, any event targeting `c:USA` with independence/republic logic will break
   - MITIGATION: Grep common/**, events/**, decisions/**, missions/** for `c:USA` or `tag = USA` before changing; may need to conditionalize on start date or create separate 1763 event chains

2. **Louisiana partition (Mississippi River split)**
   - RISK: Province-level geography required; no clear engine/map delineation of "west vs east of Mississippi"
   - IMPACT: Manual error-prone assignment; may misassign provinces
   - MITIGATION: Cross-reference province IDs with real-world geography or in-game map; consider using Mississippi area as the river itself (provinces adjacent = split point)

3. **HAI → French colony (Hispaniola split)**
   - RISK: HAI tag name suggests independent Haiti (post-1804); using for French colony is semantically confusing
   - IMPACT: Potential event/mission conflicts if HAI is scripted as independent revolutionary state
   - MITIGATION: Grep for HAI tag references; consider renaming to FHA (French Haiti) or SDO (Saint-Domingue) if engine allows tag rename, OR accept semantic mismatch with government/subject enforcement

4. **Empty Río de la Plata territory**
   - RISK: Buenos Aires and surrounding areas appear EMPTY in 1815 setup (no owner found)
   - IMPACT: If truly empty, assigning to PR1/new subject is straightforward; if owned by unlisted tag or Indigenous nation, may conflict
   - MITIGATION: Verify by reading FULL setup file or in-game inspection; check for Indigenous/tribal tags in South America

5. **VNZ subjects (TNJ/CAU/ANQ)**
   - RISK: Unknown what TNJ, CAU, ANQ tags represent (not identified in research)
   - IMPACT: If these are 1815-specific (post-independence fragmentation), they should not exist in 1763
   - MITIGATION: Grep setup for TNJ/CAU/ANQ definitions; check if they own provinces or are subject-only entities; likely need to remove or make them post-1763 conditional

6. **NGR independence in 1815**
   - RISK: Line 758 comment says NGR was "independent confederacy" in 1815 → implies Gran Colombia or New Granada independence (1810s-1820s)
   - IMPACT: Converting NGR to SPA subject for 1763 changes its 1815 status; if mod has 1815-specific NGR content (missions, events), may break
   - MITIGATION: Check if 1763 bookmark is REPLACING 1815 or COEXISTING; if coexisting, need start-date conditionals for SPA → NGR dependency

### Medium-Risk Changes

7. **QTO → PR1 subject** (from SPA direct)
   - RISK: QTO may have SPA-targeted events/missions as direct subject
   - IMPACT: Changing overlord to PR1 may orphan content
   - MITIGATION: Grep for QTO references; update overlord conditionals

8. **CAN tag creation**
   - RISK: CAN registered but unused in 1815 → may lack history/culture/government setup
   - IMPACT: Activating CAN may require additional setup (primary culture, religion, capital, ruler)
   - MITIGATION: Read setup/countries/n_america/canada.txt for tag definition; may need to flesh out

9. **Character replacement for MEX/VNZ/HAI**
   - RISK: Replacing rulers changes gameplay (stats, traits, dynasty)
   - IMPACT: If ruler characters are tied to events (e.g., Morelos in Mexican independence chain), those events will fail
   - MITIGATION: Audit events for character-specific triggers; consider keeping character definitions but NOT setting as ruler (spawn later via event)

### Low-Risk Changes

10. **Florida transfer (NSP → GBR)**
    - LOW RISK: Simple dependency line change; FLO already exists as tag
    - MITIGATION: Verify FLO has appropriate government type for British colony (may need to change from tributary to client_colony government)

11. **BRZ under POR** (already correct)
    - NO RISK: No change required

12. **CHR/CHL under PR1** (already correct)
    - NO RISK: No change required

### Dependencies and Sequencing

**MUST CHECK FIRST** (investigation phase):
1. FRA own_control_core: Does France own Quebec/Canada provinces in 1815? (need to transfer)
2. Cuba/Puerto Rico province ownership: Are they modeled? Who owns them?
3. TNJ/CAU/ANQ tag definitions: What are these? Should they exist in 1763?
4. Indigenous tags in North America: Are Comanche, Sioux, etc. represented as tags? May own Louisiana interior.
5. Río de la Plata empty status: Confirm no hidden owner.

**EDIT SEQUENCE** (if proceeding):
1. **Character fixes FIRST**: Replace unborn rulers (Morelos) to prevent crash on load
2. **Dependency additions**: Add missing SPA → NGR, GBR → USA, GBR → CAN, NGR → VNZ, PR1 → QTO (change from SPA), PR1 → RPL (new), FRA → HAI (or split)
3. **Province assignments**: Assign empty/French/Spanish territories to correct owners (Louisiana split, Quebec, Buenos Aires)
4. **Dependency removals/changes**: FLO from NSP to GBR, QTO from SPA to PR1, VNZ from independent to NGR subject
5. **Tag government changes**: USA/HAI from republic to colonial, any new tags (CAN, RPL, etc.) need government/capital/culture
6. **Verification**: In-game load test; check for crashes, missing dependencies, uninitialized tags

### Open Questions for User Decision

- **USA representation**: Colonial subject (keep USA tag, change government) vs direct GBR rule (dissolve USA, assign provinces)? Recommendation: Colonial subject.
- **Louisiana split**: Create new tags (SLO Spanish Louisiana, BLO British Louisiana) vs assign to existing (NSP, GBR)? Recommendation: Assign to existing, or create SLO under NSP if distinct administration desired.
- **Hispaniola split**: Keep HAI as unified French colony vs split Haiti/Dominicana areas? Recommendation: Unified is simpler; split is more accurate.
- **Río de la Plata**: Direct PR1 ownership vs create subject (RPL/BUE)? Recommendation: Create subject to match viceroyalty structure.
- **CAN tag**: Activate CAN as British subject vs assign Quebec to GBR directly? Recommendation: Activate CAN for future 1763→1783→1815 upgrade path (Canada remains British).
- **1763 bookmark coexistence**: Is this REPLACING 1815 start or ADDING a second bookmark? If adding, need start-date conditionals throughout (dependency lines, character births, etc.).

### Critical Path Issues

**BLOCKER**: If mod has extensive USA-specific content (missions, events, decisions) that assumes independence/republic government, converting to British colony will require extensive rewrites beyond setup file changes.

**BLOCKER**: If Louisiana interior is owned by Indigenous tags not yet identified, province reassignment will conflict.

**BLOCKER**: If TNJ/CAU/ANQ are load-bearing in 1815 (own significant territory, have missions), removing them for 1763 requires conditional existence.

**MITIGATION**: Recommend implementing 1763 as ISOLATED bookmark (separate setup file branch) with start_date conditionals in shared content (events/missions), OR as a mod-flag-gated alternative (e.g., `has_global_variable = start_1763` checks throughout).
