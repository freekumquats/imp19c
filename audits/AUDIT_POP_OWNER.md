# #234 — 1763 Pop + Ownership Audit

Province-by-province audit of the whole world's 1763 populations **and** political
ownership. Every province of every tag, every tag per region, every unowned province.
Region order: **South America → North America → Europe → Africa → Asia → onward.**
Workflow per region: audit → adversarial code-review → commit → push.

Scale: 1 unit (`amount`) = 4,000 people. Ownership in `setup/main/00_default.txt`
(`own_control_core` per tag; `dependency=` graph). Comment-strip `#` before parsing.

---

## Region 1 — British North America (committed 3b55091cc; under remediation)

### Adversarial code-review findings (agent, on 3b55091cc + 2778b31b9)

**Crash checks — CLEAN:** BOM present on all 9 files; no `amount=0`; braces balanced;
no dropped/dup province IDs; magnitudes sound (~2.34M vs ~2.1M target).

**HIGH — undefined cultures introduced by the pop rework (invalid data):**
- `lenape` — 10 provinces in `00_Mid-Atlantic.txt`: 5149 Punxsutawney, 5770 Lock Haven,
  6364 Scranton, 6378 Montrose, 6486 Bloomsburg, 6995 Williamsport, 7168 Uniontown,
  7251 Waynesburg, 7821 Bellefonte, 7835 Altoona. No `lenape` culture exists in
  `common/cultures/`. → FIX: `lenape` → `shawnee` (Algonquian, defined in 00_algic.txt).
- `atakapa` — 1 province in `00_Deep_South.txt`: 1775 Lake Charles (was `cajun`).
  Undefined. → FIX: `atakapa` → `koasati` (Muskogean Gulf, defined in 00_muskogean.txt).
- STATUS: **FIXED.** `lenape` DEFINED as a real Algonquian culture (added to
  00_algic.txt culture block + loc `lenape:0 "Lenape"`) — it's a distinct major
  nation in that exact region, no good-enough approximation, one-line add (China-
  granularity rule still favors approximation elsewhere). `atakapa` → `koasati`
  (good-enough Muskogean Gulf approximation for one sparse hex; not worth a new culture).

**MEDIUM — Mi'kmaq religion split:** `mikmaq` culture given `religion="inuit"` in
New_Brunswick + New_England but `catholic` in Nova_Scotia. Mi'kmaq were Catholic
(French missions) by 1763. → FIX: standardize `mikmaq` → `catholic` everywhere.
- STATUS: **FIXED.** All 11 mikmaq provinces now catholic (NB ×8 + New_England ×3
  flipped from inuit; Nova_Scotia ×3 already catholic). Verified every inuit in
  those files was on a mikmaq province before replacing.

**LOW (noted, not blockers):** Mansfield (8007) civ_value=40 stray; San Agustín/
Pensacola latin_caribbean (FL ceded to GBR 1763, borderline at start-of-year);
Springfield rifles (pre-existing, out of scope); enslaved `evangelical` mod-wide convention.

### Native RELIGION audit (prompted by "why are the natives catholic?")
- **Mi'kmaq (14 provs, NB/NS/NE): catholic → `syncretic_christian`.** Mi'kmaq WERE
  Jesuit-Catholic by 1763 (French allies since 1610s) so not animist — but bare
  `catholic` implies a European congregation; `syncretic_christian` (the mod's
  "Christianized-but-indigenous" faith) is the accurate choice. Verified ALL
  native-on-catholic provinces were Mi'kmaq — no other nation leaked onto catholic.
- **`gaihwiio` is ANACHRONISTIC** — it's Handsome Lake's Longhouse Code, founded
  **1799** (36 yrs too late). Iroquois in 1763 = traditional Longhouse; mod convention
  for unconverted eastern natives = `waashat` (confirmed: Appalachia Cherokee/Shawnee
  all waashat). FIXED in BNA scope: Mid-Atlantic (25) + Ontario (3) → waashat.
  ⚠️ REMAINING gaihwiio elsewhere (fix when reaching those regions): **Great_Lakes 18,
  Great_Forests 9** (both North America region, not yet audited).

### BNA border/owner audit
- Multi-core (comment-stripped): 0 true conflicts. The 27 `_fix_bna_cores.py` strips
  were ghosts (already-emptied tags' `# was:` comments) — NOT applied.
- Full per-province owner audit vs 1763: **PENDING** (per new mandate — old audit only
  checked multi-core, not wrong-single-owner).

---

## Region 2 — South America (pops committed bbc8fb286; owner audit IN PROGRESS)

### Pop review (agent, on bbc8fb286) — CLEAN after fix
- Crash-class BOM regressions found + FIXED (e85be8efe): 5 files had DOUBLE BOM,
  00_default.txt had an errant BOM. Now correct.
- Bogus "border fix" in bbc8fb286 REVERTED (330590304): was ghosts + regex comment corruption.

### Owner audit — COMPLETE (every province of every SA tag + every unowned province)
- **CRT (Cartagena) — BUG, FIXED (applied to 00_default.txt working tree).** Independent
  `constitutional_republic` (~1811 anachronism) owned 944/4366/9689(cap)/2772/8703/8514/5171.
  Moved all 7 to **SFB** (Viceroyalty of New Granada); CRT now inert (owns 0). Capital moved
  with land → no ownerless-capital crash. Comment-safe edit, no BOM, braces balanced.
- **Paraguay 913 Concepción — anachronism.** 12u paraguayan/catholic town, UNOWNED. Concepción
  (Paraguay) founded 1773 — shouldn't be a large catholic town in 1763. → FIX: shrink to small
  Guaraní frontier (pop). Unowned is then fine.
- Owner hierarchy otherwise ALL CORRECT (verified per-province): SPA→PR1(Peru)→{AR1,LFP,CHR,CHL,PRG},
  SPA→SFB(New Granada)→{QTO,VNZ→{TNJ,CAU,ANQ}}, Brazil POR→BRZ, S-Brazil frontier LFP (Rio Grande/
  Sacramento contested — plausible), Guianas NED→{DUG,BIG}/FRA→FRG, Mapuche+Tehuelche+Guaraní-missions
  independent (LFQ/LFM/INP/MSN + unowned Patagonia/Pampas). PR1 Amazon-headwaters (Purus/Acre) =
  defensible pre-1777-San-Ildefonso simplification. Empty provs (6351 Puerto Deseado, 10780 Osorno,
  6175 Boa Vista, 1694/2763 etc.) = clean-empty, valid, NOT amount=0 residue. Zero amount=0 in all SA.

### Pop audit — findings (magnitudes too high for 1763; to fix)
- **Northeast_Brazil:** Recife 50u→~7u, Salvador 40u→~11u (Bahia ~45k/Pernambuco ~27k; ~4-8× over);
  Itabuna 23u, Santo Antonio 13u, Sergipe 10u — trim inflated towns.
- **South_Brazil:** Desterro 25u, Rio Grande 14u, Porto Alegre 10u — trim (far-south was sparse frontier).
- **Uruguay:** Montevideo 20u + whole Banda Oriental over (thinly-settled ranching); trim.
- **Paraguay 913** anachronistic (above).
- North_Brazil/Center-West = mostly sparse tupi/kayapo/guarani, magnitudes OK.
- **Chile — was OVER-trimmed (my error), FIXED.** Had gutted to 77u/308k; real 1763 =
  colonial valley ~400-500k + independent Mapuche Araucanía ~200-300k. Boosted Mapuche
  Tranaquepe 5→22u, Temuco 7→30u; lifted Santiago/Concepción. Now 127u/508k (defensible-low).
  Owners all verified correct (CHL valley / LFQ Mapuche / PR1-CHR Atacama-north / AR1 trans-Andes).
- **Guyana — was ~3× high, FIXED + owner bug.** Trimmed plantation towns (Georgetown/Paramaribo/
  New Amsterdam/Cayenne/Nieuw Nickerie) + emptied Spanish-Orinoco interior (Santa Elena/El Jobal/
  Angostura — Ciudad Bolívar founded 1764). Now 38u/152k. **OWNER/COMPOSITION BUG FIXED: Georgetown
  (9868) was afro_caribbean/anglican/english under Dutch tag BIG — anachronistic (British took
  Demerara 1796). → creole/reformed/dutch to match its correct Dutch owner (BIG = NED client_colony,
  culture=dutch; tag NAME misleading but ownership right).**
- STATUS: **all pop+owner fixes applied. SA fully audited (every province, 4-point checklist).
  Firing fresh adversarial review on the full 7-file diff → fix → re-review → commit → push.**

---

## Region 3 — Mexico / Central America / Caribbean (NOT STARTED for real; deferred per SA-first order)

### Caribbean owner audit — findings so far
- **Trinidad (1591) — BUG.** Owned by LWI (British Lesser Antilles). Trinidad was **Spanish**
  until Britain took it in 1797. → FIX: reassign to Spanish (NSP or a Spanish Caribbean tag). PENDING.
- Hispaniola correct: west = French (HTI/HTK/GAS, all FRA client_colonies), east = Spanish (NSP).
- Lesser Antilles 1763 Treaty of Paris: Dominica/St Vincent/Grenada/Tobago → GBR (LWI) ✓;
  Guadeloupe/Martinique → FRA ✓; Cuba → NSP ✓ (Havana returned to Spain 1763); Bahamas → BAH (GBR) ✓.
- Pop magnitudes to fix: Cuba 572k→~170k; Bahamas(Lucayan) 124k→~4k; StDomingue 412k ✓ mag but
  needs ~85-90% enslaved composition; central Mexico 3.8M ✓ mag but needs ~62% indigenous.

---

## Region 3 — NORTH AMERICA (in progress; NOT committed — full region + review first)

Research: `1763_north_america_research.md` (Calloway/Hämäläinen/Cook/Ray/Ubelaker etc.).
8 of 9 interior/west regions = entirely Indigenous-owned (unowned on map); only American
Southwest Rio Grande corridor is Spanish. Missions: Alta CA starts Jul 1769, so 1763 CA=100% Native.

### Done (working tree, unreviewed):
- **Great_Lakes**: gaihwiio(anachronistic 1799)->waashat (all); Detroit yankee/reformed->quebecois/catholic
  (French Fort Pontchartrain) + Ojibwe minority. Owners (C3F/MIA/DAK independent natives) correct.
- **Great_Forests (Ohio/Illinois Country)**: 18 anachronistic yankee/Christian settler provinces
  (Cincinnati/Columbus/Dayton/etc — post-1763, Pontiac's War + Proclamation Line) -> Native tribesmen
  (Shawnee Ohio core, Illinois/Miami Indiana). Kaskaskia yankee->quebecois/catholic (French village).
  gaihwiio->waashat. 47u.
- **California**: Alta CA catholic->earth_lodge (missions start 1769, not 1763); Alta cities
  norteno->chumash; stripped anachronistic Spanish settler strata; Baja (Jesuit since 1697) KEPT
  Spanish/catholic. Pop 36u->83u/332k (research: densest HG region ~250-310k). Owners: native tags +
  unowned (correct); Baja NSP (correct).

### Remaining NA files to audit (per-province, 4-point checklist):
Great_Plains, Cascadia, Mountain_West, American_Southwest, British_Columbia, Praire_Provinces,
Northern_Territories, Vancouver_Island, Alaska, + Mexico(Eastern/Northern/Pacific), Central_America,
Antilles, Cuba, Haiti, Lucayan. THEN adversarial review -> fix -> re-review -> commit -> push.

### NA continued (working tree, unreviewed):
- **Great_Plains**: 5 anachronistic settler provinces fixed — St.Louis(4459) yankee->french/catholic
  (founded 1764, French habitants under Spanish LSA); Girardeau/St.Charles/Fayette/Kennet dixie/yankee
  ->osage/waashat. Owner LSA (Spanish Louisiana, got it 1762) verified correct, owns own capital 3967.
  Plains nations (DAK/CMC/OSG/LAK/etc) all correctly independent. 25u.
- **Cascadia**: clean (all Native, unowned/small native tags, no European contact 1763). No change.
- **Mountain_West**: 4 Apache/Chiricahua catholic->waashat (San Carlos/Yuma/Phoenix/Tucson — Apacheria
  independent, unconverted). Tucson kept small norteno mission element (San Xavier pre-1763). Owners correct.
- **British_Columbia / Northern_Territories / Vancouver_Island**: clean (Dene/Haida/Salish/Inuit, HBC posts + unowned).
- **Praire_Provinces**: Winnipeg(3055)/Grand Rapids(4798) metis/catholic->cree/waashat (Metis people
  = 1810s Red River, anachronistic; owner ICF Cree correct). 
- **Alaska**: Kodiak(2477) orthodox->inuit; Novoarkhangelsk/Sitka(12498) stripped russian/orthodox
  settler stratum (Russian America starts 1784/1799; ZERO Russian presence 1763). All unowned = correct.
- **Caribbean OWNER fixes (00_default.txt)**: Trinidad(1591) LWI->NSP (Spanish till 1797); St.Lucia(4849)
  LWI->FRA (French till 1814). Dominica/StVincent/Grenada/Tobago->LWI correct (ceded 1763). Comment-safe,
  no BOM, braces ok, spa_america.4 intact.
- **Cuba**: scaled ~0.3x -> 236k (was 572k; 1763 pre-sugar-boom ~170-200k). Composition (castilian
  elite/zambo/mulato/slaves) preserved.
- **Haiti**: Saint-Domingue FRENCH west (HTI/HTK/GAS: PauP/Jeremie/Jacmel/LosCayos/PortdePaix/CapHaitian/
  Gonaives) rewritten to ENSLAVED-MAJORITY (was 6% -> 67% file-wide, ~85%+ in the French provinces;
  richest slave colony on earth). Spanish east (Santo Domingo etc, NSP) kept free/mixed. dahoman religion.

REMAINING NA: Eastern_Mexico, Northern_Mexico, Pacific_Mexico, American_Southwest, Central_America,
Antilles (owner done; pop magnitudes TBD), Lucayan (Bahamas ~4k, currently ~29u — trim).

### NA Mexico/Caribbean (working tree, unreviewed):
- **American_Southwest**: 28 independent-native provinces (Comanche/Chiricahua/Caddo/Koasati/Lipan)
  catholic->waashat (unconverted, owned by CMC/CDD/APA/LIP not NSP). NSP Rio Grande/Texas mission-
  presidio corridor (El Paso/Santa Fe/Albuquerque/San Antonio/Laredo/etc, 11 provs) kept catholic. Owners correct.
- **Pacific_Mexico** (central Mexico core): re-indigenized to 68% indigenous / 26% mestizo (was 53%
  mestizo; research ~62% indigenous 1763). 37 mexican-primary provinces flipped to regional Native
  culture (nahuatl center, zapotec Oaxaca, purepecha Michoacan, tzeltal Chiapas) + small mexican minority.
  Cities (Mexico/Puebla/Guadalajara/Leon/Irapuato/Queretaro/Pachuca/Tulancingo) kept Hispanic-majority.
  Pre-existing 2x amount=0 stripped. Owner NSP correct.
- **Eastern_Mexico**: re-indigenized to 75% indigenous / 17% mestizo (was 38% mestizo). 16 provinces
  flipped (yucatec Yucatan/Campeche, tzeltal Tabasco, nahuatl Veracruz); Veracruz port + Merida kept
  Hispanic. Pre-existing amount=0 stripped. Owner NSP correct; Yucatan interior TUL(Maya) independent.
- **Cuba**: (above) 236k. **Haiti**: (above) Saint-Domingue enslaved-majority.
- **Northern_Mexico**: audited — silver-mining Bajio (Zacatecas/SanLuisPotosi/Aguascalientes) legitimately
  populous; far-north already sparse. 207u/828k DEFENSIBLE for the San Luis Potosi+Zacatecas intendancies.
  28% mestizo/40% norteno acceptable (frontier was more mixed). NO CHANGE needed. Owner NSP correct.

NA POP-MAGNITUDE FOLLOW-UP (done 2026-08-02): Central_America (GUA/pops) + Lucayan (Bahamas trim)
were completed in the "NA region reviewed" commit fa7e57cd0. **Antilles pop magnitudes were NOT** — that
commit landed only the OWNER fixes (Trinidad->NSP, StLucia->FRA in 00_default.txt), leaving the doc's
"Antilles (owner done; pop magnitudes TBD)" open. NOW DONE: full per-province Antilles pass (research:
Higman/Watts/O'Reilly 1765/Eltis). 00_Antilles.txt 250u->160u (~640k). Gross fixes: Puerto Rico
(San Juan 33u->11u + Ponce 20u->5u; 1765 O'Reilly census ~45k total, PR was a pre-sugar-boom FREE-
population outlier, not a slave colony); Trinidad 10u->2u (nearly empty pre-1783 Cedula; de-anachronized
- removed the English settler stratum, it was Spanish till 1797; trade cacao->coffee (chocolate is a DEFUNCT good; culture->latin_caribbean)); Barbados
28u->18u; Martinique/Guadeloupe kept ~mag (French sugar); Curacao 10u->4u (Dutch entrepot, not
plantation); the just-ceded-1763 Windwards (Grenada/StVincent/Dominica/Tobago) trimmed (barely settled,
Carib-held). ANACHRONISM FIX: St Barthelemy swedish->french (Swedish only from 1784). Jamaica
(Kingston+MontegoBay 40u~160k) already matched research - unchanged. No amount=0; single BOM; braces ok.

## EUROPE (region 3) — OWNER audit findings (pre-edit, confirmed vs sourced research)

Sourced basis: research/1763_econ_poland_lithuania.md ("Commonwealth intact; First Partition=1772"),
audit_worklists/research/europe_1763.md (Black/Doyle/Lynch/Dixon/Finkel/Clark/Ingrao/Wilson/Lukowski).
CSV owner col DISCARDED (echoes on-disk; proven by Trinidad 1591=LWI but was Spanish/NSP).

Aggregate Euro on-disk pop = 36,041u (~144M) vs ~150M expected — magnitude OK; Europe is an OWNER/distribution problem.

CONFIRMED 1763 OWNER ANACHRONISMS (map frozen at 1815/post-partition borders):
1. Galicia file (00_galicia.txt): 33 provs = AUS, but Lwów/Kraków/Przemyśl/Tarnopol/Brody = Austrian only from
   1772 First Partition. 1763 = POLISH. (Prov 10092 Krakau currently = KRA tag.)
2. Belgium: 00_low_countries.txt lumps Brussel/Antwerpen/Liège/Gent/Namur/Bruges/Mons/Luxembourg under NED
   (Dutch Republic). 1763 = AUSTRIAN NETHERLANDS (Habsburg). ~20+ provs need NED->AUS (or a Belgium subject tag).
3. dependency RUS->FIN (royal_union): Finland was SWEDISH in 1763 (Russian only from 1809). Fix overlord + FIN provs.
4. dependency SWE->NOR (royal_union): Norway was DANISH (Denmark-Norway); Swedish only from 1814. Fix overlord.
5. dependency PRU->POZ (royal_union): Poznań/Posen = Polish until 1793 2nd Partition. 1763 = POLISH.
6. Right-bank Ukraine (in 00_kiev.txt, currently all RUS): Bila Tserkva/Fastiv/Cherkasy/Chigirin/Berdychiv =
   Polish Crown until 1793. Left-bank (Poltava/Chernigov/Kursk/Belgorod)+Kiev city = Russian since 1667 (correct).
7. Lithuania-proper + Latgalia in 00_baltic_states.txt: ~20 provs = RUS (Kowno/Telšiai/Šiauliai/Panevežys/
   Kėdainiai/Jurbarkas/Plungė/Kelmė = Samogitia; Rēzekne/Dünaburg/Lucyn/Kreslavl = Latgalia). Commonwealth till partitions.

CORRECT (no change): Habsburg subjects HUN/CRO/TUS/LBV/TRS (royal_union/client); Ottoman vassals CRM(feudatory)/
WAL/MOL(autonomous); COU=RUS client but should be POLISH FIEF (flag); LIV/EST=RUS client (Baltic German, Russian
since 1721 — CORRECT). Silesia = PRU (correct, Hubertusburg Feb 1763). Corsica: check 00_corsica_and_sardinia (GEN:4 present).

PRIOR PARTIAL WORK (#218/#229, treat as UNVERIFIED but aligns w/ research): LIT already expanded to full GDL
(Vilno/Grodno/Minsk/Mogilev/Vitebsk/Volhyn/Brześć); POL got Podlachia. Remaining gaps = Galicia, Poznań, right-bank
Ukraine, Samogitia/Latgalia, Belgium, Finland, Norway, Courland.

STATUS: edits DEFERRED until two research truth docs assembled (user: consolidate first). Then execute + review.

## EUROPE — EXECUTION DECISION LOG (2026-08-01, autonomous per skill; source = research/1763_TRUTH_ROW.md E.Europe section)

Root cause: Eastern Europe map frozen at 1815 POST-PARTITION borders. Commonwealth was WHOLE in Feb 1763
(1st Partition 1772). All fixes below reverse partition anachronisms. CRASH-SAFETY: 00_default.txt has NO BOM
(plain utf-8); comment-safe edits only (no bare-int regex across file); keep every tag's capital owned by SOMEONE.

### A. DEPENDENCY inversions (1815 relations → 1763 reality) — edit dependency lines
1. RUS->FIN royal_union  => SWE->FIN royal_union.  Finland was integral SWEDEN in 1763 (Russian only 1809).
2. SWE->NOR royal_union  => DEN->NOR royal_union.  Norway was DENMARK-Norway (Swedish only 1814).
3. RUS->COU client_state => POL->COU client_state. Courland = Polish CROWN FIEF in 1763 (Russian only 1795).
4. PRU->POZ royal_union  => DELETE. Poznań/Greater Poland was Polish till 1793 2nd Partition; POZ neutralized (see C).

### B. GALICIA (00_galicia.txt, currently AUS:33) — Austria took Galicia 1772, Bukovina 1775
- ALL galicia AUS provs => POL (Polish Crown: Ruthenian/Lwów + Lesser Poland voivodeships), EXCEPT:
  - 6798 Radautz + 8767 Czernovitz => MOL (Bukovina = MOLDAVIAN, Ottoman vassal; Austria annexed 1775 not 1772).
  - (Kolomea 8769, Nadworna 7948, Kutty 8165, Zaleszczik 8098 = Pokuttya/Ruthenian voiv. = POLISH, NOT Bukovina => POL.)
- 10092 Krakau: currently owned by KRA tag (see C) => POL.

### C. KRA (Free City of Kraków) — ANACHRONISM: this is the 1815 Congress Free City, constitutional_republic, 1 prov.
- CRASH CLASS: landless constitutional_republic = construction crash ([[imp19c-landless-republic-crash]]).
- FIX (proven CRT template): government constitutional_republic => viceroyalty; own_control_core emptied;
  Krakau 10092 => POL; KRA capital stays 10092 (now owned by POL, exactly like CRT cap 9689 owned by SFB).
- KRA has 3 guarantee lines (RUS/AUS/PRU) — harmless on an inert tag, leave.

### D. POZ (Poznań) — neutralize; Greater Poland is Polish in 1763
- POZ is a viceroyalty (safe landless class). Move all 12 POZ provs => POL. POZ capital 563 => now owned by POL (CRT pattern).
- Delete PRU->POZ dependency (B4).

### E. RIGHT-BANK UKRAINE (00_kiev.txt, currently RUS) — west of Dnieper = Polish Crown till 1793
  Left-bank + Kiev city + Sloboda + Russia-proper Black Earth = Russian since 1667 => KEEP RUS.
- => POL (right-bank Kyiv voiv. + Bracław + Podolia + Pokuttya-adjacent): 4002 Bila Tserkva, 3937 Fastiw,
  2671 Berdichiv, 3989 Cherkassy, 3409 Chigirin, 5905 Bohuslav, 5414 Uman, 6533 Vinnitsya, 6521 Illintsy,
  5958 Orativ, 5971 Zhmerinka, 6600 Kamyanets-Podilsky, 5300 Proskuriv, 7175 Husiatyn, 6038 Yarmolintsy,
  6022 Murovani Kurilivsty, 7326 Kodima, 5361 Torodishe(Horodyshche), 5410 Mala Viska, 4604 Ruzhin,
  4542 Khmilnik, 2829 Ovruch, 6099 Pripyat.
- => MOL: 6586 Chernivtsi (Bukovina).
- FLAG (uncertain, left RUS pending review): 2187 Vishgorod (Vyshhorod, right-bank but abuts Kiev city 1667 cession).
- KEEP RUS (left-bank/Sloboda/Black-Earth): Poltava, Chernigov, Konotop, Nezhin, Romny, Priluki, Lubny, Kremenchuk,
  Zolotonosha, Pereyaslav, Starodub, Novgorod-Seversky, Kharkiv, Sumy, Okhtirka, Kursk, Belgorod, Stary Oskol, etc.

### F. BALTIC (00_baltic_states.txt, RUS provs) — Samogitia/Latgalia/Lithuania-proper = Commonwealth till partitions
- => LIT (Grand Duchy): 122 Pasvalys, 129 Kursenai, 751 Plunge, 1767 Visaginas, 2363 Rokiskis, 2379 Kelme,
  6140 Silale, 6472 Kowno(Kaunas), 7519 Kedainiai, 7723 Telsiai, 8222 Sakiai, 8237 Jurbarkas, 9694 Siauliai,
  10032 Panevezys  (Samogitia + Lithuania-proper);  3252 Rezekne, 5194 Dünaburg, 6029 Lucyn, 6609 Kreutzburg,
  6638 Vorklyany, 8359 Marienhausen, 10050 Kreslavl  (Latgalia/Inflanty).
- => PRU: 8352 Silute (Šilutė/Heydekrug = Memelland = PRUSSIAN Lithuania, never Commonwealth/Russia).
- FLAG (uncertain, left RUS pending review): 2880 Lyanskorona (possibly Livonia-proper Vidzeme, which correctly stays RUS).
- KEEP RUS (correct since 1721 Nystad): LIV (Livonia/Riga) + EST (Estonia/Reval) client_states — Baltic German, Russian.

### G. FINLAND (00_finland.txt, currently FIN) — Vyborg/"Old Finland" Karelia was Russian since 1721/1743
- => RUS (ceded to Russia by Nystad 1721 + Åbo 1743): 8832 Viipuri(Vyborg), 3761 Käkisalmi(Kexholm),
  7564 Sortavala, 6525 Muolaa, 9555 Virolahti, 9567 Kotka, 3766 Valkeala, 6580 Impilahti, 8212 Suojärvi.
  (rest of FIN stays FIN under SWE per A1.)
  FLAG: exact Vyborg-Karelia province set approximate — review to confirm none are core-Finland.

### NOT CHANGED (verified correct): Silesia=PRU (Hubertusburg Feb 1763); Corsica GEN (Genoese); Habsburg subjects
  HUN/CRO/TUS/LBV/TRS; Ottoman CRM(feudatory)/WAL/MOL(autonomous); Belgium=AUS (no Belgium tag — good-enough
  abstraction, Austrian Netherlands folded into AUS which already owns low_countries Belgian provs... VERIFY: are
  Brussel/Antwerpen/etc under NED? YES — NED:35. DECISION: Belgium provs NED->AUS. See H.)

### H. BELGIUM (00_low_countries.txt) — Austrian Netherlands (Habsburg), currently under NED (Dutch Republic)
- => AUS (Austrian Netherlands + Luxembourg): Brussel 235, s'Hertogenbosch(NO—Dutch Brabant, stays NED), Dinant 1090,
  Mons 3177, Kortryk 3187, Yper 3392, Charleroi 3992, Verviers 4447, Wavre 5133, Leuven 5148, Liège 6426,
  Antwerpen 6584, Bruges 7221, Gent 8056, Namur 8497, + LUX provs (Arlon 2361, Bastogne 2377, Luxembourg 4270).
  DECISION detail: the Dutch Republic kept the 7 northern provinces + Generality Lands (States Brabant incl.
  's-Hertogenbosch/Maastricht, Zeeland-Flanders). Austrian Netherlands = Brabant(Brussels/Antwerp/Leuven), Flanders
  (Gent/Bruges/Kortrijk/Ypres), Hainaut(Mons/Charleroi), Namur, Liège(prince-bishopric, tech. separate but abstract to AUS),
  Luxembourg. FLAG for review: exact NED-vs-AUS province split of the Low Countries is the error-prone call here.

### EUROPE — CRASH-SAFETY RESOLUTIONS (applied)
- KRA (Free City Kraków): constitutional_republic -> viceroyalty, core emptied, cap 10092 owned by POL. SAFE (CRT pattern).
- POZ (Poznań): already viceroyalty; core emptied, cap 563 owned by POL. SAFE. PRU->POZ dependency deleted.
- LUX (Luxembourg): already viceroyalty; core emptied (Luxembourg prov 4270 -> AUS), cap 4270 owned by AUS. SAFE.
  Stale NED->LUX royal_union DELETED (Luxembourg=Austrian Netherlands 1763; LUX left inert like QNG/ALC/CRT).
- VERIFIED post-edit: 0 double/zero-owned among 100 touched provs; all 13 relevant tags' capitals owned; braces 10967=10967; 00_default.txt has NO BOM (correct). All 3 landless tags are viceroyalty (NOT elected-head republic crash class).
- Dependency inversions applied: SWE->FIN, DEN->NOR, POL->COU (were RUS->FIN, SWE->NOR, RUS->COU).

### EUROPE — POP-SIDE + FINAL VERIFICATION (applied)
- Galicia pops: 10 anachronistic `culture="austrian"` strata (post-1772 Habsburg admin/colonists) fixed —
  Bukovina provs (Radautz/Czernowitz) -> romanian; Polish-Galicia provs (Lezaysk/Rzeszów/Neu Sandec/Bochnia/
  Wadowice/Bielitz/Kraków) -> polish. (Bielitz German enclave folded to polish = good-enough abstraction.)
- Latgalia (LIT now) small `russian` Old-Believer pops: KEPT — historically correct (Old Believers fled to Polish
  Inflanty late-17thC); old_belief religion present confirms. Right-bank Ukraine pops clean (ukrainian/polish/ashkenazi).
- Religions across touched files all DEFINED + period-appropriate (catholic/orthodox/jewish/sunni/lutheran/reformed/
  old_belief/evangelical). No anachronisms. Aggregate Euro pop ~144M (vs ~150M expected) — magnitude fine, no rescale needed.
- CRASH SWEEP: 00_Galicia single BOM (efbbbf, no double), braces 247=247, 0 zeros. 00_default NO BOM, braces balanced.
  Only 00_default.txt (owner) + 00_Galicia.txt (pops) changed — baltic/kiev/finland pop files already period-correct, owner-only fix.
- STATUS: Europe audit COMPLETE, pending adversarial code-review (mandatory gate before commit).

### EUROPE — ADVERSARIAL CODE-REVIEW: PASS (no blockers) [2026-08-01]
code-review subagent verdict: PASS, clear to commit. All crash-class checks CLEAR (landless-republic SAFE:
KRA/POZ/LUX all viceroyalty; ownerless-capital SAFE: caps owned by POL/POL/AUS — proven CRT/ALC pattern, NOT a
dangling-capital crash; 0 double/zero-owned; BOM correct both files; braces balanced; 0 amount=0; all culture/
religion keys defined; no bare-int/comment corruption). All 4 historical province sets independently CONFIRMED
(right-bank Dnieper, Bukovina->MOL, Vyborg/Old-Finland, Belgium NED/AUS split incl. Generality Lands kept Dutch).
2 LOW non-blocking notes (NOT from this diff): Roermond->AUS (Habsburg Upper Guelders, defensible); pre-existing
`jewish` religion tagged DO-NOT-USE (227 pre-existing lines, out of scope — FOLLOW-UP candidate). No fixes needed
=> no re-review of identical diff. Boot-test owed on separate machine (standing rule).

## NA/SA FOLLOW-UP CORRECTIONS (2026-08-01, from verification agents; source research/1763_TRUTH_ROW.md Americas)
NA:
- St.Louis 4459: was French settlement (culture=french +creole slaves) — founded 1764, anachronistic at Feb 1763.
  FIXED -> Osage (culture=osage/waashat, 2u tribesmen). Matches 1763 reality (Osage country, no St.Louis yet).
- Quebec: quebecois ~92k overshot New France St.Lawrence census (~70k). Trimmed Montréal/Quebec/Sorel/Boucherville/
  Joliette -> quebecois ~72k. Native pops (cree/nunavik/huron/abenaki 31u) untouched. Quebec total 54u->49u.
SA (magnitude/composition drift flagged by SA verify agent):
- Chile: colonial ~0.27M undercount -> raised Central Valley core (Santiago/Concepción/Talca/Rancagua/etc) to
  ~0.40M colonial; Mapuche ~0.24M untouched. Total 127u->161u (~0.64M) = matches 400-500k colonial + 200-300k Mapuche.
- Colombia: 1.20M -> 1.00M (top of 0.8-1.0M range). Scaled down 15 largest settled provinces (Bogota/Tunja/
  Cartagena/etc). Indigenous keys (zipa/zaque/achagua/panche/wayuu/tairona/sinu) preserved.
- Venezuela: 0.85M -> 0.76M (slightly above 0.5-0.7M; further trim would gut floors — ACCEPTED as defensible
  for cacao-coast+llanos+Maracaibo).
- Peru: indigenous share 47%->73%; Ecuador 44%->79% (research target 70-80%). Converted highland lower_strata
  (province-default peruvian/ecuadorian mestizo) -> quechua. Mestizo majority is 19thC; 1763 Andes were indigenous-
  majority. Totals unchanged (culture shift only).
- candomble/cabula/catimbo (SA verify flag): confirmed DEFINED in common/religions/00_vthreereligions.txt =
  intentional mod folk-religion abstractions, not crashes. Period-appropriateness = low-priority, LEFT.
- CRASH SWEEP all 7 files: single BOM, braces balanced, 0 zeros, all cultures defined. STATUS: pending adversarial review.

### NA/SA FOLLOW-UP — ADVERSARIAL REVIEW: PASS (no crash blockers) + fixes applied [2026-08-01]
Review verdict: no crash-class blockers (all 7 files single-BOM, braces balanced, 0 zeros, cultures/religions defined,
quechua regex insertions well-formed). Fixes applied for the 2 raised issues:
- B1 (MEDIUM) FIXED: file-wide quechua conversion wrongly hit COASTAL Ecuador (Guayaquil/Esmeraldas/Machala/
  Portoviejo/Babahoyo = montubio/mestizo/Afro-coast, not Andean). Reverted those 6 -> ecuadorian. Ecuador indigenous
  79%->65% (highland quechua-majority + coastal mestizo = geographically correct). Peru B2 (coastal quechua) LEFT:
  defensible (highland labor migration to coastal haciendas; afro_andean retained).
- B3 (LOW) DECISION: St.Louis 4459 owned by LSA (Spanish Louisiana), cap=3967 so no ownerless-capital risk.
  LEFT LSA-owned: research says Spanish authority over Osage country was NOMINAL but the CLAIM existed (from France
  1762); LSA-owned + Osage-populated = same pattern as Spanish Southwest/Apacheria (nominal claim, indigenous pops). Defensible.
- B4 (INFO) duplicate identical strata: engine-legal, standard in these files, no action.
Diff changed only Ecuador after fixes; re-verify then commit.

## AFRICA (ROW region 1) — DECISIONS + FIXES (2026-08-01, source research/1763_TRUTH_ROW.md Africa section)
Africa 1763 = overwhelmingly independent African states + European COASTAL POINTS (not territorial). Aggregate on-disk
pop ~13k u across 13 files. Owner audit found post-1763 Mfecane/jihad anachronistic tags (all founded 1804-1820s).
USER DECISION: reflavour-in-place (keep tag+territory, relabel to period-correct polity + fix pop culture).

REFLAVOURED (loc rename + primary_culture in 00_default.txt):
- SOK "Sokoto"->"Gobir", primary_culture fulani->hausa (Sokoto Caliphate=1804 jihad; 1763=Hausa city-states).
  Province 10155 culture fulani->hausa + added fulani pastoralist minority tribesmen (pre-jihad reality).
- ZUL "Zulu"->"Ndwandwe" (Zulu Kingdom=~1816 Shaka; Ndwandwe/Mthethwa were the pre-Shaka Nguni powers). Kept zulu
  culture as good-enough Nguni abstraction. Fixed 8 ZUL provinces: shona(Greytown, 1500km wrong!)/sotho/swazi -> zulu.
- MAT "Matabele"->"Kalanga", primary_culture ndebele->karanga (Ndebele arrived 1830s Mzilikazi; 1763 Zimbabwe=Rozvi/Karanga).
- LST "Lesotho"->"Basotho", primary_culture xhosa->sotho (WRONG people fixed; Lesotho kingdom=1820s Moshoeshoe but Sotho were there).
- ESW "Eswatini"->"Ngwane" (Swazi kingdom consolidation 1820s; Ngwane clan = nucleus). Kept swazi culture.

CAPE (CPC): already Dutch VOC client_colony of NED (prior #236, correct). Fixed Cape Town 2750: culture
  anglo_african->boer, religion anglican->reformed, dropped english/anglican upper stratum (=British Cape 1806
  anachronism); boer religion lutheran->reformed (Cape Dutch = Calvinist/Dutch Reformed, not Lutheran).

ETHIOPIA: map was POST-1769-fragmented (~15 tags), but 1763 = centralized under Emperor Iyoas I (Zemene Mesafint
  begins 1769). USER DECISION: subject highland Christian tags to Gondar (GDR). Prior work already had GDR->TGR/SWA/
  WLO/GJJ tributary; ADDED missing GDR->MDB (Medri Bahri, Tigrayan coastal march). Muslim Somali/Afar periphery
  (HRR/OGD/MEE/ASA/ISQ/ZEI/MWA) + southern Oromo/Sidama (KFA/SDM/BOE/etc) left independent (correct - outside Christian empire).

VERIFIED CORRECT (no change): European coastal footholds are POINTS (Angola/Mozambique coastal, VOC Cape small,
  Gold Coast forts); Oyo at zenith + Dahomey tributary; Lunda/Luba peak; Rozvi declining; Madagascar fragmented.
CRASH SWEEP: South_Africa (BOM,203/203,0 zeros), Gulf_of_Guinea (BOM,250/250) — the 3 amount=0 in GoG lines 75-85
  are PRE-EXISTING (in HEAD, not my edit to prov 10155); FOLLOW-UP candidate, out of scope. 00_default no BOM, braces
  balanced. loc file BOM preserved. All culture keys defined. STATUS: pending adversarial review.

## ASIA/PACIFIC (ROW region 2) — PREP NOTES (owner scan done, edits pending Africa commit)
Owner scan largely period-plausible: TKG Tokugawa dominant Japan; AFG Durrani holds Afghanistan+Punjab+Pashtunistan
(correct, withdrawing post-Panipat); fragmented Indian successor states (JAI/GWA/MAR Rajputs, AWA Awadh, BIH/PAT Bihar,
NAG Nagpur-Maratha); Central Asian khanates (BUK/KOK/KHV); PHI Philippines; Pacific mostly unowned (correct).
KEY ANACHRONISM TO FIX: EIC owns 31 Indo-Gangetic + 23 Bengal + 5 Bahar = post-1857 Raj footprint. In 1763 (pre-Buxar
1764) EIC held Calcutta+coastal factories w/ de-facto Bengal REVENUE control, but Nawab (BNG) nominal sovereign +
Gangetic plain = Awadh (AWA). Plan: shift bulk of EIC Gangetic provs -> AWA; Bengal core EIC->BNG (leave EIC a few
Calcutta/coastal provs); keep EIC as GBR client_colony. Also verify: Sikh=misls not empire (no unified SIK tag holding Punjab —
AFG holds it, OK); Mughal not territorial; Ayutthaya SIA standing; Manila PHI Spanish. Pacific/NZ/Australia unowned-indigenous.

### AFRICA — ADVERSARIAL CODE-REVIEW: PASS (no crash blockers) + all 3 findings fixed [2026-08-01]
Review verdict: no crash-class blockers (BOM correct all 4 files incl. loc BOM preserved; braces balanced; culture/
religion keys resolve; loc YAML valid; GDR->MDB unique dep, no double-overlord/ownerless-capital; no comment corruption).
Fixes applied:
- B1 (MED) FIXED: Cape Town had duplicate boer/reformed upper_strata (I'd CONVERTED the English elite instead of
  DROPPING it -> Boer overcount). Dropped the converted stratum -> single boer upper (matches "remove British-Cape 1806" intent).
- B2 (MED) FIXED: stale _ADJ loc keys synced to renames: SOK_ADJ Sokoto->Gobir, MAT_ADJ Matabele->Kalanga,
  ZUL_ADJ Zulu->Ndwandwe, ESW_ADJ Swazi->Ngwane, LST_ADJ Lesotho->Basotho.
- B3 (LOW) FIXED: MDB primary_culture amharic->tigre (Medri Bahri = Tigrinya highland march, not Amhara).
BONUS: removed 3 pre-existing amount=0 blocks in Gulf_of_Guinea prov 611 Fernando Poo (+ dropped anachronistic
  castilian/catholic residue; Bioko was minimally-settled Bubi/fang in 1763, Spanish only from 1778). GoG 0 zeros now.
Re-verified all files crash-safe. No further blockers -> commit.

## ASIA/PACIFIC — DECISIONS + FIXES (2026-08-01, source research/1763_TRUTH_ROW.md Asia section)
MAIN FIX — EIC de-Raj-ification (00_default.txt): EIC owned 134 provs = post-1857 Raj footprint. Pre-Buxar (1764)
EIC held Calcutta+coastal factories with de-facto Bengal REVENUE control, but Nawab nominal sovereign + Gangetic=Awadh.
- 31 Indo-Gangetic (Agra/Mathura/Meerut/Kanpur/Allahabad/Bareilly/Lucknow-doab) EIC->AWA (Awadh + Mughal/Maratha
  frontier; EIC took these 1801-1856 as Ceded&Conquered Provinces).
- 21 Bengal-proper (Dacca/Jessore/Barisal/Mymensingh/etc) EIC->BNG (Nawab of Bengal sovereign); EIC KEEPS Calcutta
  6219 (capital) + Chittagong 1491 (genuine footholds).
- 5 Bahar EIC->BIH (Bihar, Nawab sphere pre-Buxar).
- EIC now owns 77 (Madras/Bombay presidencies + Bengal coastal factories = realistic 1763). Still GBR client_colony. Verified: 0 double/zero-owned, capital safe, braces balanced, no BOM.
VERIFIED CORRECT (no change): AFG Durrani holds Punjab/Pashtunistan (withdrawing post-Panipat, correct); fragmented
  Indian successors (Rajputs/AWA/Hyderabad/Marathas NAG); Central Asian khanates BUK/KOK/KHV; TKG Tokugawa Japan;
  PHI Spanish Philippines (British occupation 1762-64 reverts to Spain 1764 = Spanish steady-state correct); SIA
  Ayutthaya standing; Pacific/NZ/Australia mostly unowned-indigenous. FALSE ALARM: "SIK" = Siak Sri Indapura
  (Sumatran sultanate, culture=sumatran), NOT Sikhs — Sikh Empire correctly ABSENT (Punjab=AFG/misls).
POP: religions all defined + period-appropriate (sunni/hindu/shinto/catholic-Luzon/mahayana/sikhism/theravada/
  anito/vajrayana/etc). anglican in Bengal = British Calcutta footholds (OK). No anachronistic religions found.
Only 00_default.txt changed (owner-only fix; pop composition already period-correct across Asia). STATUS: pending review.

### ASIA — REVIEW-DRIVEN EXTENSION (B1+B2 fixes applied) [2026-08-01]
First adversarial review PASSED (no crash blockers; 57-prov bijection verified) but flagged 2 medium historical gaps:
- B1 FIXED: ~half the Gangetic EIC->AWA provs weren't Awadh. Reassigned 19 AWA->MUG: Rohilkhand (Rampur/Bareilly/
  Moradabad/Badaun/Pilibhit/Shahjahanpur/Najibabad/Saharanpur/Muzaffarnagar = Rohilla Afghan), Agra-Braj (Agra/
  Mathura/Hathras/Firozabad = Jat Bharatpur), Delhi-Doab (Sonipat/Rohtak/Faridabad/Hapur/Meerut = Najib regent),
  Farrukhabad (Bangash). No Rohilla/Jat tag exists -> MUG nominal sphere = good-enough ROW abstraction. Genuine Awadh core kept AWA.
- B2 FIXED: EIC over-held the whole South/East/West/Central India + Sumatra (same pre-Buxar logic). Reassigned 70:
  Orissa->NAG (Nagpur Maratha since 1751); Northern Circars+coastal Andhra+Carnatic/Coromandel+Telangana->HYD (Nizam/
  Arcot; Circars ceded to EIC only 1766); Mysore-plateau+Malabar/Kanara->MYS (Hyder Ali); Nagercoil->TRV; Gujarat->MRT
  (Gaekwad); Daman->POR (Portuguese); Sumatra W-coast->DEI (Dutch/Minangkabau). Unowned: Aizawl(Mizo tribal), Maldives, Chagos.
  EIC KEEPS 6 genuine 1763 footholds: Calcutta 6219(cap)+Chittagong 1491+Madras 162+Bombay 8299+Surat 683+Bengkulu 6553.
- RESULT: EIC 134 -> 7 provinces (historically-accurate 1763 footprint = presidency towns + coastal factories). All 12
  touched tags' capitals owned by self (no ownerless-capital); 0 double/zero-owned; braces 10967=10967; no BOM.
- B3 (LOW, pre-existing NOT fixed here): EIC own_control_core still comment-lists French India (Pondicherry) + already
  moved Yanaon 3464->HYD, Daman 6414->POR. French Pondicherry cluster = FOLLOW-UP. B4 cosmetic whitespace in EIC core: harmless.
STATUS: pending RE-REVIEW (large extension beyond first-reviewed diff).

### ASIA — RE-REVIEW: PASS + B1 fixed [2026-08-01]
Re-review of extended diff: no crash blockers (127-prov bijection independently verified twice; 0 double/zero-owned;
all 637 capital= declarations resolve to an owner; no comment/event-id corruption; BOM correct; braces balanced).
- B1 (MED) FIXED: EIC still held a 7th province 146 Andaman (HEAD leftover; EIC had no Andaman presence 1763,
  first settlement 1789/1858). Dropped -> unowned (indigenous Andamanese). EIC now = exactly 6 footholds as intended.
- B2-B5 (LOW) non-blocking defensible ROW abstractions, accepted: Malabar->MYS ~3yr early (Hyder Ali took it 1766;
  Kanara 1763 OK); Carnatic/Coromandel->HYD (no Arcot tag, HYD=nominal Nizam suzerain); MUG=NOMINAL SPHERE for
  Rohilkhand/Jat-Agra/Farrukhabad (de-facto independent, but no Rohilla/Jat/Bangash tag -> good-enough per China-
  granularity rule); Burdwan/Midnapore 1760-cession folded to BNG (defensible under nominal-sovereign principle).
- B3 FOLLOW-UP: EIC own_control_core still comment-lists French Pondicherry cluster (out of scope this pass).
FINAL: EIC 134->6. STATUS: Asia COMPLETE, committing.

## CHINA (focus region, extra attention) — AUDIT + FIXES (2026-08-01, source research/1763_TRUTH_CHINA.md)
OWNERSHIP: SOUND (no fix needed). CHI directly owns 450 provs (18 provinces' core). Legitimate subjects: Manchuria
MKD/MNC/HLJ + ULS (autonomous_governorship); Xinjiang ILI (autonomous_governorship) + XNG Altishahr (ILI client);
Tibet TIB (protectorate) + LTG/DER/CKL/NGQ (feudatory); Yunnan CHH Shan (feudatory). Only 4 provs correctly UNOWNED:
Taiwan east coast (Ylan/Hualien/Taidong = indigenous Formosan, Qing held only W plain till 1870s-80s) + Lop Nur
(empty Xinjiang desert). PARSER LESSON: commented-out #YNG/#SHG/#MZH viceroyalty blocks broke naive brace-parse ->
falsely showed core provinces "unowned"; MUST comment-strip whole file before tag-scanning (skill rule confirmed).
POPULATION MAGNITUDE: SOUND. China-proper ~215M (top of truth-doc ~205-215M actual range). Per-province distribution
matches Cao Shuji shares proportionally (Jiangsu 25M densest, Shandong 19M, Zhejiang 16M...); all provinces uniformly
~15% below the c.1770s-peak target shares = internally consistent, correctly anchored to a slightly lower total. NO
rescale (uniform scaling = rejected flat-multiplier fake-work). Sichuan 7.3M = correct (rapidly-infilling frontier ~6-7M).
Inner Asia: Mongolia 2.4M, Tibet 1.0M, Turkestan 2.5M (Kazakh jüz outside Qing + Tarim Uyghur) — all in range.
COMPOSITION: richly developed already (Gansu Hui-Sunni+Uyghur+Oirat+Tibetan-Buddhist; Guizhou Miao+nuoism; Yunnan
Dai/Thai/Kachin+Theravada+Hui; Guangdong Yue+Hakka+Hlai). TWO FINE-FIDELITY FIXES:
- GUANGXI ZHUANG (real gap): zhuang culture DEFINED but unused; W/central Guangxi (Zhuang heartland, China's largest
  minority) was all 'yue' (Cantonese Han). Converted 14 W-Guangxi provs (Nanning/Chongzuo/Guigang/Fangchenggang/
  Liuzhou/Hechi/Laibin/etc) province-default yue->zhuang + added yue Han merchant minority. Eastern Guangxi (Guilin/
  Wuzhou/Yulin/Beihai/Qinzhou) kept Han. Guangxi now yue:25/zhuang:14/ping:7.
- NEPAL TRIBUTARY (anachronism): removed CHI->NEP sinosphere_tributary. Nepal NOT a Qing tributary in 1763 (Gorkha
  unified Kathmandu 1768-69; tributary only after 1792 war). NEP left independent (no GRK tag; good-enough).
KEPT CORRECT: KOR/VIE/RYU sinosphere_tributary; TIB protectorate; Manchuria/Xinjiang governorships; Dzungar-depopulated
N.Xinjiang; tributary ring. CRASH SWEEP: Guangxi single BOM/170=170/0 zeros; 00_default no BOM/braces balanced; zhuang defined.
STATUS: pending adversarial review.

### CHINA — ADVERSARIAL REVIEW + RE-REVIEW: PASS + fidelity fixes [2026-08-01]
First review: no crash blockers; Nepal fix confirmed correct; raised Guangxi-Zhuang fidelity issues (B1 Han-as-peasant
inverts Qing structure; B2/B7 flip too far east, western ping-heartland left Han; B6 wrong elite religion).
REDID Guangxi from HEAD: 16 provinces zhuang-majority (refined set — added true western heartland Baise/Donglan/Longlin/
Tian'e/Lingyun/Tiandong which were ping-Han; REVERTED too-east/coastal/urban-Han Lingshan/Fangchenggang/Guigang/Liuzhou
to yue), Han minority now upper_strata/confucianism (gentry-merchant = correct Qing social structure, not peasant).
RE-REVIEW: PASS, clear to commit (172/172 braces, single BOM, 0 zeros, 16 well-formed appended blocks, 4 reverts match
HEAD, keys defined, Nepal dep-graph intact). 2 LOW notes: B-LOW-1 (ex-ping provs' Han minority should be ping not yue)
APPLIED (6 provs yue->ping = Pinghua was the Han substrate there); B-LOW-2 (Longlan 8630) LEFT (reviewer + I both
uncertain on its geography — flipping uncertainly is worse). FINAL: Guangxi yue:31/zhuang:16/ping:1. STATUS: committing.

================================================================================
BOOT-LOG ERROR TRIAGE (2026-08-01) — task #22, post-successful-boot
================================================================================
Boot test PASSED (2 months daily ticks, no crash). User: "investigate and triage
them all, fix the ones which need to be fixed." Log = /tmp/imp_logs (STALE vs disk:
00_egypt_missions.txt already deleted; line numbers offset ~1). Triage METHOD =
DIFFERENTIAL (live-vs-dead key in the SAME load unit), NOT oracle-absence inference.

USER COURSE-CORRECTION (mid-task): "treat sobisonator upstream bugs with EXTREME
CAUTION; chance you're wrong and sobisonator is right is VERY HIGH." → new standing
memory [[imp19c-sobisonator-upstream-caution]]. LEFT UNTOUCHED accordingly:
  - TRADE_lists.txt base=region + every_*_TZ_region (MOVEMENT/PRICE/TRADE svalues):
    parse-line "Unexpected token" is a LOAD-ORDER artifact (scripted_lists parsed
    after script_values), NOT a real bug. Runs fine (game boots + ticks).
  - cultural_infatuation_modifiers.txt test_modifier custom_tooltip (Sobisonator stub).
  - .asset scale/rotation (MIUNO gfx) — valid syntax (TI identical), load-order noise.

FIXES APPLIED (all differential-proven real):
1. first_valid = yes (8 lines: 000_GOVERNMENT_custom_loc x7, 00_qing_harem_loc x1) —
   REMOVED. Not a valid customizable_localization key (0 in vanilla + both oracles;
   TI orders text{} top-down with NO first_valid). First-match is engine default.
2. is_triggered_only = yes (439 lines, 84 event files) — REMOVED. CK3/EU4-ism, 0 uses
   in either oracle; Imperator events fire only via trigger_event/on_action regardless.
3. DEAD-UNIT MODIFIERS (114 lines, 13 files) — REMAPPED to unit-agnostic keys. Vanilla
   land types (light/heavy_infantry, light/heavy_cavalry, archers, camels, chariots,
   horse_archers) + galley navy types were EMPTIED in #188 "Merge culture levies";
   their derived <unit>_offensive/etc keys no longer exist. PROOF: live types
   (artillery_/conscripts_) 0 errors, emptied types 28 errors, SAME files/load.
   Map: _offensive->discipline, _defensive->global_defensive, _discipline->discipline,
   _morale->land_morale_modifier, _movement_speed->army_movement_speed,
   _cost->cohort_cost, _maintenance_cost->army_maintenance_cost, _<terrain>_combat_bonus
   ->unit-agnostic <terrain>_combat_bonus. Colliding keys in a block SUMMED (merge).
   USER DECISION: "Remap everywhere (current state)" — restore intended bonuses in all
   files incl Sobisonator/krushka (00_indian, 00_arabic, 00_from_events_country,
   00_hardcoded). regulary_infantry_offensive typo->regular_infantry_offensive (live).
   ai_plan_goals dead trireme_* AI-weight block removed (generic naval_* covers intent).
4. religions 00_vthreereligions.txt (20 bare diplomatic_relations/happiness_for_same_
   religion_modifier keys) — WRAPPED in modifier={}. SOBISONATOR upstream → per user,
   MOVE TO upstream_bugs BRANCH (task #23), NOT this branch.
5. qing_war_modifiers.txt — morale_of_armies_modifier->land_morale_modifier,
   ship_recruit_speed->global_ship_recruit_speed, loyalty->character_loyalty,
   popularity->monthly_character_popularity, power_base->prominence (all my file).
6. qing_rites tributary opinions (3) — MOVED from common/modifiers/ (opinion=N, illegal)
   to common/opinions/imp19c_opinions.txt (value+yearly_decay); renamed + call sites.
7. qing_ili_modifiers movement_speed->army_movement_speed.
8. all_power_cost (qing_governance, qing_household) — dead key (Invictus icon-only);
   folded into monthly_political_influence_modifier / ruler_popularity_gain.
9. local_commerce_value_modifier (qing_mechanics, qing_treaties)->state_commerce_modifier
   (the engine-read province commerce key; the earlier "fix" landed on a vanilla-only key).
10. local_population_growth_modifier (00_province_feature x3)->local_population_growth.
11. monthly_character_loyalty (qing_amban, 00_from_events_character)->character_loyalty
    (monthly form is invention/icon-only, not an applied modifier key).
12. custom_tooltip inside modifier (imp19c_province_modifiers colonial_outpost) — REMOVED
    (illegal in modifier{}; tooltip comes from the modifier's own loc key).
13. hidden_effect inside modifier{} (00_civic_inventions tech_mechanical_tools/
    tech_manufactories) — UNWRAPPED (effect block illegal in modifier{}; the 7 inner
    output keys are all valid modifier keys, moved directly into modifier{}).

VERIFIED VALID (NO fix): diplomatic_relations as country-modifier (qing_legations, 25x
Inv), happiness_for_same_religion_modifier as country-modifier (00_from_events_country),
country_civilization_value as modifier key (70x Inv; only its TRIGGER form needed
civilization_value, fixed earlier). movement_speed/opinion/loyalty/custom_tooltip/
hidden_effect all valid in their proper (non-modifier) contexts.

STATUS: all edits brace-balanced + BOM-correct. PENDING: move #4 to upstream_bugs;
mandatory adversarial code-review of full diff BEFORE commit.

--------------------------------------------------------------------------------
REVISION (2026-08-01, post-review + user course-corrections)
--------------------------------------------------------------------------------
USER CORRECTIONS applied:
- classes 1 (first_valid) & 2 (is_triggered_only) reframed: these are NOT feature
  repairs — the keys are inert CK3/EU4 cargo-cult (unknown to Imperator engine), so
  removal only clears log noise; behavior was already correct via engine defaults
  (first-match text{}; no MTTH anywhere in mod → nothing auto-fires). Legitimate
  triage outcome, but not "fixes" in the functional sense.
- class 3 (dead-unit modifiers): user chose LIVE-UNIT remap (hybrid) over unit-agnostic.
  REDID from HEAD: Qing-themed blocks → the historically-correct LIVE Qing unit; non-Qing
  blocks → unit-agnostic (no generic live cavalry/archer unit exists). Mapping by
  enclosing-def theme:
    banner/Mongol trees, banner modifiers, jianrui/solon/camel distinctions → qing_eight_banners
    green-standard tree + green/rattan/firearms distinctions → qing_green_standard
    Self-Strengthening (ever-victorious/beiyang/nanyang/jiangnan), advisor army, Napoleon-
      at-Qing-court tree (00_napoleon IS Qing alt-history) → regular_infantry
    Arabic/Indian/Japanese/default/Rome-Carthage (00_from_events_country) → unit-agnostic
    terrain *_combat_bonus everywhere → unit-agnostic (no per-unit terrain key authored)
  Collisions re-summed per new key. Proven valid: oracle legion_distinctions unit{} blocks
  use <unittype>_<stat> (Invictus spearmen_*, TI archers_/engineer_cohort_*); all target
  units are army=yes so keys derive.
- religions wrap (00_vthreereligions): STAYS fixed on this branch; ALSO ported to
  upstream_bugs (task #23). NOT reverted here.

CODE-REVIEW (adversarial subagent) findings + resolution:
  HIGH  global_defensive in a legion-distinction unit{} block (invalid in unit scope) —
        RESOLVED by live-unit remap (now qing_green_standard_defensive, valid in unit{}).
  MED-1 rm_defence_focus_cmod dup global_defensive → merged to 0.15.
  MED-2 00_indian.txt dup global_defensive → merged to 0.15.
  MED-3 qing_advisor_army_active dup discipline → RESOLVED by live remap (discipline +
        regular_infantry_offensive, distinct keys).
  MED-4 relocated-opinion loc keys still opinion_qing_tributary_* → renamed to
        qing_tributary_* in qing_rites_l_english.yml (BOM preserved).
  LOW   cost/discipline magnitude shifts — intended per user "remap everywhere" + live choice.
  Review noted the diff also carries UNRELATED prior work (se_LAND flag:as_capital rework,
  WAR_scripted_guis LAND_transfer rewrite, new scripted_triggers, ECON svalue) — those
  predate this task and were reviewed/kept as-is; flagged for their own pass if needed.

FINAL VERIFY: 131 changed files, 0 brace problems, 0 BOM changes, 0 dead-unit keys, 0 dup
keys. Re-review dispatched before commit.

--------------------------------------------------------------------------------
NAPOLEON-CHAIN DATE AUDIT + AMHERST DEDUP (2026-08-01, user-requested)
--------------------------------------------------------------------------------
Q (user): does the Napoleon (#65 Emperor-Emeritus) chain, built for the old 1815 start,
still fire at the correct date in the 1763 start?

FINDING: YES — the chain reaches its 1816 window correctly.
  Path: oa_economy_setup.txt (gate current_date < 1793.9.14, so ALWAYS fires on the
  1763-only start) schedules Amherst embassy qing_embassy.2 at day 19552 (=1816.8.29,
  historically exact). Player receiving Amherst fires qing_napoleon.5 (Waterloo overture,
  gate current_date < 1821.5.5 — Napoleon alive) → .6 St Helena → .1 arrival → chain.
  Already migrated for 1763 ([bookmark-1763 #304-fix] on the Amherst re-entry guard).

STALE COMMENT FIXED: qing_mechanics_on_actions.txt:~277 said "START_DATE is 1815.7.1 /
  ~410-430 days" — described the DEFUNCT 1815 start. Code (days 19537-19557) was already
  correct for 1763; comment updated.

AMHERST DOUBLE-SCHEDULE FIXED (dedup, user "investigate further"):
  START_DATE is now ONLY 1763.2.16 (defines; 1815 start superseded, moved back 19127d;
  no bookmark file). Two schedulers both fired Amherst on a 1763 player-CHI game:
    A = oa_economy_setup.txt  (gate current_date < 1793.9.14 → always fires) day 19552
    B = qing_mechanics_on_actions.txt (gate is_ai=no only) days 19537-19557
  B was the DEFUNCT 1815 start's pin (A doesn't fire on 1815 since 1815 > 1793.9.14).
  On 1763 both fire; saved only by qing_embassy.2's amherst_done idempotency guard — a
  latent double-Amherst/double-Napoleon-overture trap. FIX (user choice): gate B with
  current_date >= 1793.9.14 (mirrors A's gate; race-free date gate, NOT the racy
  qing_embassy_dated_schedule flag since both are on_game_initialized). Now A alone pins
  Amherst on the 1763 start; B is a true fallback for a hypothetical post-1793 start.
  Matches the proven stand-down idiom at se_QING_DECLINE.txt:1265. current_date >= literal
  date is valid (3 mission-file uses, 0 errors). PRE-EXISTING issue, not from the triage.

--------------------------------------------------------------------------------
#25 MISSION/EVENT SWEEP for #234 setup changes (2026-08-01)
--------------------------------------------------------------------------------
Systematic sweep of ALL 16 Qing mission trees + all events for references made
stale by #234 setup changes. Method: extracted structural changes (tag/owner/dep)
from each #234 commit, grepped all missions+events for changed tags/provinces/cultures.

FINDINGS BY REGION:
- CHINA (Nepal now independent, commit 7a9ac8aec): Himalaya tree qing_hs_nepal
  MECHANICALLY CORRECT (guards exists c:NEP + NOT is_subject_of; makes NEP tributary
  later = models the 1792 war, exactly the user's intent). Fixed stale "returns to the
  tributary fold" wording (implied prior tributary status) in mission comment + the
  qing_tribute_events / color_picker tributary-list comments (NEP no longer a START
  tributary, joins via mission). Tribute event iterates every_subject dynamically — no
  mechanical break.
- ASIA (EIC 134 provs -> 6 pre-Buxar footholds, commit fa587c4f3): India tree
  (qing_india_missions) MECHANICALLY SOUND — EIC still holds Calcutta 6219 (the seat +
  central mission target); every task gates on is_subject_of=ROOT / province control,
  never on MUG/BNG starting as EIC subjects; QING_india_free_mughal only checks
  NOT-subject-of-ROOT. BUT 7 flavor refs called MUG a "Company puppet to free from
  tutelage" — stale (MUG independent pre-Buxar). Per user "flavor + strengthen premise":
  reframed the whole tree to pre-Buxar "strangle the upstart Company in its Bengal
  cradle; the independent Indian thrones (MUG/AWA/HYD) to bring under the wing, not
  Company puppets to liberate" — header, ARC E, inline comments, effect header/LOG, and
  3 player-facing loc strings (mission DESC, mughal_DESC, mughal_tt).
- AFRICA (reflavours/renames MAT->Kalanga, LST->Basotho, ESW->Ngwane, culture swaps +
  GDR->MDB dep, commit 307a4ad06): ZERO Qing mission/event references any reflavoured
  tag or swapped culture; colonization arc (#67) targets provinces by ID (unaffected by
  pop reflavours). No changes needed.
- EUROPE (FIN->SWE, COU->POL, NOR->DEN, POZ/LUX dep changes, commit 0e8ee2062): no Qing
  mission/event references FIN/COU/NOR/POZ/LUX. No changes needed.
- NA/SA (pop-composition only, no owner/dep changes): nothing to reconcile.

#26 (India TRADE arc, same changeset): reworked qing_india_trade from "open overland
trade" (flavor no-op) into "Seize the Company's Commerce (奪夷商)" with CONCRETE on-map
effects (new QING_india_seize_trade effect): on Qing-controlled EIC-footprint provinces
(Bengal/Bihar/South-India) raise qing_customs_house + qing_silk_filature buildings and
set_trade_goods = silk (raw textile_fibres -> finished silk); Calcutta 6219 seat gets a
customs house + draft bank; Bengkulu 6553 pepper post -> qing_tea_workshop + tea. Gated
on holding real trade ground. Proven idioms (add_building_level+has_building guard;
set_trade_goods). All keys/goods/regions verified valid; braces balanced; loc BOM kept.

--------------------------------------------------------------------------------
#24 QING BUILDINGS ON CHI SUBJECT NATIONS (2026-08-01, reviewed)
--------------------------------------------------------------------------------
Seed Qing-specific buildings on the capitals of CHI's 1763 subjects. KEY ENGINE FACT
(verified against repo, NOT the research agent which was WRONG): add_building_level does
NOT bypass a building's `potential` — a gate-failing building is hidden/dropped at boot
(proven: Macau was bumped to city rank specifically to pass has_city_status). So the
approach is to make the buildings' gates PASS, not to force-seed.

USER-DRIVEN INSIGHT: has_city_status was on many Qing buildings that are frontier/rural/
remote by nature (forts, garrisons, pastures, monasteries, mosques, granaries, likin
barriers) — historically wrong (forts sit on the frontier; the great lamaseries Labrang/
Kumbum/Chengde 外八廟 are remote; granaries served county-wide). So REMOVED has_city_status
from: qing_banner_garrison, qing_confucian_temple, qing_gelug_monastery, qing_great_mosque,
qing_granary, qing_likin_station. (frontier_fort/colony/military_colony/horse_pasture/karez/
customs_house were ALREADY correctly ungated by their authors.) This removed the need for
any city-rank bumps (an earlier settlement->city approach was built then REVERTED).

GATE RELAXATION: gelug + confucian owner-gate widened to admit a Qing subject
(owner={overlord={country_culture_group=jurchen/chinese}}) so CHI's non-manchu Buddhist/
sinosphere subjects qualify; gelug region gate gained Sichuan_Kham (the Kham feudatories).

REGRESSION CAUGHT + FIXED post-review: removing has_city_status left qing_granary with an
EMPTY potential{} = globally buildable by every nation. Fixed: gated to jurchen/chinese
owner-or-overlord (Chinese-realm-only, not city-restricted).

SEEDING: new hidden one-shot imp19c_setup.12 (dispatched day 2 from oa_economy_setup beside
.11), places 17 buildings on 12 subject capitals, each guarded exists+owner-is-subject-of-
ROOT+NOT-has-building:
  banner_garrison: ILI/ULS/MNC/MKD/HLJ (manchu governorships)
  military_colony: ILI(Gansu)/ULS(Mongolia)/MKD(Liaoning); horse_pasture: ULS/MKD
  gelug_monastery: TIB(Lhasa)/CKL(Kangding)/DER(Derge)
  confucian_temple: KOR/VIE/RYU/CHH (sinosphere tributaries + Sipsong Panna Shan court)
All 17 verified to PASS their post-edit gates. Adversarial review: CLEAN (1 informational
note re confucian build-menu breadth across all CHI subjects — thematically defensible,
left; the seeding event places only the 12 enumerated). NOT bumped/seeded: TNN/MLM/TNI/LSU/
LAF/FOS (non-city nominal vassals, not worth promoting). Braces balanced, BOMs preserved.
New memory: [[imp19c-add-building-level-respects-potential]].

--------------------------------------------------------------------------------
#27 WIRE QING BUILDINGS + TRADE GOODS INTO MISSION TREES (2026-08-01, reviewed)
--------------------------------------------------------------------------------
Went through ALL 16 Qing mission trees INDIVIDUALLY by hand (an earlier scripted/
templated attempt was rejected by the user as inappropriate and fully reverted). Each
tree read in full; buildings/goods added ONLY where they fit the task's actual theme.

WIRED (building/good as task reward, guarded NOT-has-building / subsistence-good-only):
- xinjiang: karez task->qing_karez_building; fortify->qing_frontier_fort; jade->set cotton (all Turkestan)
- central_asia: tuntian->qing_military_colony; border(karun line)->qing_frontier_fort (Fergana else Turkestan)
- settle_frontier: garrison task->qing_banner_garrison (the ONE gap; tree already plants colony+fort via QING_settle_plant_works)
- taiping: land_system->qing_granary (聖庫 shared granary — the Taiping's OWN institution, Yangzi heartland)
- reform: schools->imperial_university, railways->telegraph, currency->mint, new_army->machine_works (all capital_scope)
- burma_war: yunnan base->qing_frontier_fort (Yunnan); teak trade->set hardwood (Burma)
- nanyang: severed->qing_customs_house on captured Batavia(6270)/Manila(2004) [controller=ROOT, mirrors India #26]
- himalaya_seasia: tibet amban->qing_gelug_monastery on Lhasa when Qing owns it directly (complements #24 subject-seed)
- japan: ready-coast->qing_navy_yard at Weihaiwei 3033 (Beiyang base; steam-era apt here)
- open_japan: ezo->qing_frontier_colony (settling Hokkaido)
- colonization: Urumqi task->add qing_frontier_fort+military_colony alongside vanilla fortress
- selfstrengthening (se_QING_SELFSTR.txt): SWAPPED generic->purpose-built Qing buildings in 4 found-effects:
    jiangnan arsenal_building->qing_machine_works (機器局; + updated paired has_building ref for the rifles swap);
    telegraph URB_commerce_district->qing_telegraph (電報局); tongwen EDU_university->qing_tongwen_guan (同文館);
    fuzhou ADDED qing_navy_yard (船政局) beside the port.
- india: DONE separately in #26 (QING_india_seize_trade).

LEFT UNTOUCHED (no appropriate building — "where appropriate" cuts both ways):
- treasure_fleet: pre-modern Zheng-He fleet; the only Qing shipyard building (navy_yard) is steam-era
  (福州船政局 1866) = anachronistic. Its generic port/industrial-estate is correct for a wooden fleet.
- japan_preperry: pure diplomacy/intelligence; the Qing owns no Japanese ground to build on.
- summer_palace: a unique imperial garden (圓明園/頤和園) with its own dedicated buildings + verbs.

Adversarial code-review: CLEAN (all placements pass their post-#24 building potentials; no
inert-drop; no dangling arsenal_building ref; no double-plant in settle_frontier; idempotent).
2 low-severity notes, both non-defects / design-consistent: (1) nanyang customs on controller=ROOT
mirrors the reviewed India #26 seizure pattern; (2) reform/japan buildings place but sit idle until
their allow-gate tech lands (allow not enforced by add_building_level) — acceptable (institution
founded, activates on modernization). 12 files, braces balanced, BOMs preserved.

## #24 extension — subject-TERRITORY institution seeds (imp19c_setup.12, non-capital)

User: "24 should not just be on subject capitals, but on all subject territory (where appropriate)"
then corrected the approach: "why are you doing this iterator and cap nonsense — if there was a
real temple or fort or whatever else in a particular location in 1763, then seed it; if not, don't."
So: NO iterators, NO per-region caps, NO formulaic spread. Seed only real, named, 1763-extant
institutions on a subject's soil, one specific province each, matched to sourced historical fact.

Research (agent, MONOGRAPH-grade — Perdue, Millward, Elliott, Crossley, Goldstein, Berger, Deuchler,
Smits) folded into research/1763_TRUTH_CHINA.md ("Named institutions on SUBJECT soil (1763)").

Added FOUR non-capital blocks to imp19c_setup.12 (all guarded: exists + subjecthood + NOT has_building):
- 4799 Shigatse (TIB, direct subject)  -> qing_gelug_monastery  = Tashilhunpo, Panchen Lama's seat (1447). Region Tibet OK.
- 6767 Erdene Zuu/Karakorum (ULS, direct) -> qing_gelug_monastery = Khalkha's premier fixed monastery (1585). Region Mongolia OK.
- 8051 Jilin city (MNC, direct)        -> qing_banner_garrison   = Jilin General's yamen (moved there 1757). owner manchu OK.
- 6617 Khovd (KBD, NESTED CHI->ULS->KBD) -> qing_banner_garrison  = 科布多參贊大臣 garrison (1731).
    NESTED-subject guard: owner={ overlord={ is_subject_of=ROOT } } (is_subject_of is NOT recursive —
    verified via 000_GOVERNMENT_custom_loc.txt which checks is_subject_of=CHI and overlord={is_subject_of=CHI}
    as SEPARATE conditions). KBD's overlord ULS is manchu, so the banner potential (owner jurchen) is satisfied.

DELIBERATELY NOT seeded (research-driven negatives):
- Urga/Ikh Khuree (MGA, 5117): fixed monastic city is POST-1763 (seasonal camp only in 1763). Excluding it
    also sidesteps the nested-MGA (CHI->ULS->MGA) guard issue — correct on both history AND engine grounds.
- Xinjiang Gelug monasteries: institutionally BLANK in 1763 (Dzungar destruction 1755-59; re-seeding is 1760s-70s+).
- Korean seowon / Vietnamese Van Mieu / Ryukyu Shiseibyo: real, but Korea/Ryukyu are ROW-abstraction (no
    map provinces for the seowon cities); the existing capital-court Confucian-temple seed already stands for them.
    (Van Mieu is at Hanoi/TRH-north, not VIE-south's Hue — noted in the truth file; VIE capital seed left as-is.)
- Labrang/Kumbum: in directly-ruled Gansu/Qinghai, NOT subject soil.

Verify: braces 212/212 balanced; events file has NO BOM (unchanged); all four placements satisfy each
building's on-disk potential (region + owner/overlord culture-group), so nothing drops inert.

## #24 sweep — DROPPED core-empire building seeds (add_building_level respects potential)

User: "the buildings added to china itself predate the loosening of the has_city restriction, so do
another sweep on china to add buildings where historically there were buildings."

KEY: add_building_level RESPECTS a building's `potential` (region/city/culture gate) — it does NOT
bypass it (memory imp19c-add-building-level-respects-potential; confirmed by the #24 reviewer). So
se_QING_BUILDINGS.txt seeds whose target province FAILS the building's gate have been SILENTLY DROPPING
at boot. Audited every seed vs its building's on-disk potential. 11 drops found, two classes:

CLASS A — REGION-gate drops (FIXED by widening the building potential to the regions where the
institution historically stood; each still requires owner/overlord culture-group jurchen/chinese_group,
so no non-Qing over-grant):
- qing_great_mosque   +Shaanxi   -> Xi'an Great Mosque 西安清真大寺 (7129) now lands
- qing_gelug_monastery +Qinghai  -> Kumbum 塔爾寺 (Xining 7200) now lands
- qing_gelug_monastery +Zhili    -> Beijing Yonghegong 雍和宮 1744 (8363) now lands
- qing_horse_pasture   +Zhili    -> Hohhot 呼和浩特 (3322) + Mulan/Rehe 木蘭圍場 (9356) now land
- qing_military_colony +Tibet    -> Lhasa 拉薩 tuntian (3819) now lands
- qing_military_colony +Far_East -> Qiqihar 齊齊哈爾 tuntian (43) now lands
  (the military_colony file-comment already ASSUMED these landed via a bypass that does not exist;
   the widening makes the comment true.)

CLASS B — CITY-rank drops (building has_city_status vs a settlement-rank province). PENDING a design
call (bump the province to city rank vs relax the building gate) — deferred to research + review:
- qing_examination_hall @ Kaifeng 4931 (Henan capital, settlement) + Guilin 2162 (Guangxi capital, settlement)
- qing_draft_bank       @ Shanghai 5429 (Jiangsu, settlement; qianzhuang emerged here 1736)
- qing_tribute_depot    @ Jining 9041 (Shandong canal entrepôt, settlement)
- (also flag: Xiamen 7845 is settlement — affects the customs/port seeds there? port uses can_have_port, OK)

PART 2 (in progress): now that #24 dropped has_city_status from the frontier/religious buildings, ADD
NEW seeds at real REMOTE (non-city) 1763 sites that could not be placed before — pending research agent
(gelug: Wutaishan/Chengde-Puning/Hohhot Silituzhao; mosques: Linxia/Hami; frontier forts: Aigun/Hunchun/
Barkol/Tacheng; horse pastures: Chahar/Taipusi; karez/granaries at frontier towns).

### Class B resolution (city-rank drops)
- Kaifeng 4931 (Henan cap) + Guilin 2162 (Guangxi cap): FIXED by bumping province_rank settlement->city.
  Rationale: 16 of China's 18 provincial capitals are already city-rank; these two were the lone
  settlement outliers = a data gap. Bumping fixes the 貢院 exam-hall drop AND aligns them with peers
  (proven Macau precedent: bump rank to satisfy has_city gate).
- Shanghai 5429 (draft_bank/qianzhuang) + Jining 9041 (tribute_depot): PENDING. NOT provincial capitals;
  in 1763 both were sub-prefectural (Shanghai a Songjiang county; Jining a canal town). Bumping rank
  would be anachronistically generous (Shanghai's rise is 19th-c.). Leaning toward the BUILDING-side fix
  (a qianzhuang money-shop / canal grain-depot did not need metropolis rank — same #24 logic), but
  deferring to research + review rather than unilaterally relaxing gates.
  (Confirmed via potential re-scan: only draft_bank + tribute_depot are city-gated on these two; the
   Shanghai 江海關 customs has NO potential block and lands fine — earlier awk false-alarm corrected.)

### Class B FINAL + Part 2 (new remote seeds) — DONE
Class B (city-rank drops) all FIXED by province_rank settlement->city, justified by each being a
real city-scale 1763 place (evidence = mod's own civ-value/pop + provincial-capital status):
- Kaifeng 4931 (Henan cap, civ 12) + Guilin 2162 (Guangxi cap, civ 6): lone settlement outliers among 18 caps.
- Shanghai 5429 (civ 18 — higher than several city-rank capitals; qianzhuang origin 1736).
- Jining 9041 (civ 12, ~221 lower-strata pop, 漕運 canal hub + Qufu 孔廟 holy site).
Now their exam-hall / draft-bank / tribute-depot seeds land.

Part 2 — NEW remote (non-city) seeds enabled by #24's has_city drop + the region-gate widenings.
Curated, sourced, 1763-extant, not-already-seeded, potential-satisfied (research agent: Naquin & Yü;
Farquhar; Berger; Elliott; Perdue; Millward):
- gelug_monastery +Shanxi region -> Wutaishan 五臺山 (2407): imperial Gelug pilgrimage mtn (Pusa Ding).
- gelug_monastery (Zhili) -> Hohhot 呼和浩特 (3322): Da Zhao 大召 1580 / Xilitu Zhao 席力圖召 1585 (co-located with existing horse pasture — 2 diff buildings, OK).
- gelug_monastery (Mongolia) -> Dolonnor 多倫諾爾 (155): Huizong 匯宗寺 1691 lama-temple complex.
- banner_garrison -> Hunchun 琿春 (1952, MNC): 副都統 far-eastern frontier garrison (1714).
DELIBERATELY not mass-seeded: the dozens of Xinjiang/Manchuria granary+tuntian+fort sites the research
lists — most frontier garrison seats already carry buildings via the OOB/existing seeds, and blanketing
every documented outpost would be the formulaic over-seeding the user rejected. Added only the few
NAMED, singular, iconic sites that were genuinely missing.

### De-duplication (architecture)
Discovered the prior commit's imp19c_setup.12 seeded Shigatse 4799 + Jilin 8051, but the CORE seed
se_QING_BUILDINGS.txt ALREADY places both via its subject-tolerant QING_seed_frontier_building macro
(guard: owner=CHI OR is_subject_of=c:CHI). Removed the two redundant duplicates from setup.12. Kept
Erdene Zuu 6767 (ULS) + Khovd 6617 (nested KBD — the frontier macro's non-recursive is_subject_of=c:CHI
would MISS it, so it legitimately belongs in the event with the nested-overlord guard).

FINAL re-audit of se_QING_BUILDINGS: 0 remaining potential-fail drops (was 11).

## #24 sweep — CODEBASE-WIDE add_building_level potential-respect audit (CHINA)

User: "do a comprehensive scan for more buildings affected by this ... first in china, then for ROW."
187 add_building_level callsites total. Built an analyzer: per-building potential (region/city/culture,
brace-accurate) x province->region (areas/regions) x province rank x owner. Checked STATIC p:N seeds
AND dynamic ordered_owned_province/random_neighbor picks (does the limit/scope guarantee the gate?).

CHINA drops found & FIXED beyond se_QING_BUILDINGS.txt:
- se_QING_WORKS.txt — the 3 dynamic Works-commission verbs picked "most populous owned province lacking
  the building" with NO region/river guard, so the building silently dropped while the treasury was still
  charged + corruption applied (pay-for-nothing):
    * QING_works_build_dike     -> added has_minor_river guard (matches qing_dike_building potential)
    * QING_works_build_canal_depot -> added Zhili/Shandong/Jiangsu/Zhejiang region guard
    * QING_works_build_wall_section -> added Zhili/Shanxi/Shaanxi/Gansu/Liaoning guard (comment even
      admitted the old "any province" was a loose proxy -> it picked a southern city, always dropped)
- se_QING_TREATIES.txt QING_treaty_stamp_port — coastal pick lacked has_city_status; qing_treaty_port_building
  needs city -> stamped the qing_treaty_port MODIFIER but the BUILDING silently dropped (desync). Added
  has_city_status to the pick. This ALSO fixes the post-treaty mission founder (keys off the treaty-port modifier).
- se_QING_FOREIGNBUILD.txt — hardened BOTH treaty-port planter macros (domestic QING_fbuild_plant_treaty_port
  + victim QING_treaty_impose_concession) with has_city_status in their own limit (defense-in-depth: a dropped
  port building while still stamping humiliation/grievance is a desync).
- se_QING_MISSIONARY_STATIONS.txt — mission buildings (public/underground) need city; the spread founder
  (random_neighbor_province) + the pre-treaty FALLBACK founder guarded only is_sea=no + total_population>0,
  so a settlement pick dropped the building while STILL bumping qing_missionary_reach (phantom missions).
  Added has_city_status to both. (The historic-mission-city founder was already safe — its 9 cities are all
  city-rank; Shanghai 5429 among them, which I bumped to city earlier in this sweep.)

CHINA false positives verified (no fix): all imp19c_setup.12 fixed-province seeds (literal p:N in-region);
Macau 2481 foreign_concession (city rank per prior bump); INDIA draft_bank @ Calcutta 6219 (city); customs_house
(NO potential block — seeds anywhere); central_asia/colonization/xinjiang/himalaya frontier seeds (either
region-guarded in the limit, or on fixed in-region provinces, or the building has no potential).

NEXT: ROW pass (se_ROW_BUILDINGS.txt, row_production_buildings.txt, and generic-building callsites).

## #24 sweep — SECOND-ROUND fixes (from adversarial review of the WORKS/mission/monument batch)

Review of the codebase-wide China audit surfaced further drops of the SAME class (add_building_level
respects potential). All fixed:

1. HIGH — always=no seed-only buildings (7). qing_great_wall / qing_grand_canal / qing_hanlin_academy /
   qing_guozijian / qing_temple_of_heaven / qing_ancestral_temple / qing_dujiangyan all had
   potential={always=no} on the (now-DISPROVEN) assumption add_building_level bypasses potential. Proof it
   respects it: the qing_mission_cathedral_building BT#6 note ("a permanently-false gate HIDES the type").
   So ALL 7 silently dropped at their seed sites, AND the Great Wall / Grand Canal WORKS-verbs became
   REPEATABLE EXPLOITS (charge 240/220 treasury + 10 manpower, grant legitimacy/stability, but the once-only
   NOT-has_building guard never latched because the building never appeared). FIXES:
   - Wall/Canal: real region+culture potential (Wall = Zhili/Shanxi/Shaanxi/Gansu/Liaoning belt; Canal =
     Zhili/Shandong/Jiangsu/Zhejiang corridor; both owner Chinese/Manchu). Seed sites (Shanhaiguan 6974,
     Juyongguan 8380 = Zhili; Huai'an 8311 = Jiangsu) now satisfied.
   - Wall/Canal WORKS-verbs: added the region guard to BOTH the outer availability limit (so no treasury is
     levied when no valid province exists) AND the ordered_owned_province pick (so it can't land off-belt).
   - The 5 unique institutions (Hanlin/Guozijian/Temple-of-Heaven/Ancestral/Dujiangyan): real region+culture
     gate per USER CHOICE (region+culture proven idiom, over province_id which is unattested in a building
     potential). Beijing 4 = Zhili; Dujiangyan = Sichuan_Kham. allow = sufficient_job_slots (NOT always=no,
     which would re-hide the type per the cathedral note).

2. HIGH — qing_military_colony_building dropped at Lhasa 3819 (owned by TIB/bodish): its owner-culture gate
   had NO overlord branch, so a CHI-SUBJECT's province failed it even after the Tibet region widening. The
   whole point (#190) was food_capacity for the Lhasa garrison — still starving. FIX: added the
   owner={overlord={jurchen/chinese}} branch (mirror gelug). Now lands.

3. MEDIUM — qing_great_mosque_building dropped at Kashgar 2700 (owned by XNG/east_turkic): same missing
   overlord branch. FIX: added it. The Id Kah mosque seed now lands.

4. MISSIONARY root-fix: gated the SINK QING_mission_found_station on has_city_status (mission buildings need
   city) — covers EVERY caller (spread, both seed branches, pre-treaty spread, treaty-port branch) so a
   settlement pick is a clean logged no-op instead of a phantom station (reach bumped, no building). This
   also covers the pre-treaty-spread + historic-city callers the first pass missed.

5. EARLYINDUS + SELFSTR port picks: is_coastal -> can_have_port (match port_building's actual potential;
   a coastal-but-non-harbour top province would drop the port while the yard modifier/effects still fired).

Comment fix: se_QING_BUILDINGS.txt Dolonnor 155 note (it's region Mongolia, already in-gate, not part of the widening).

ROW pass: se_ROW_BUILDINGS.txt + row_production_buildings all CLEAN — manufactory/plantation picks already
match the trade_goods gate; ports guarded can_have_port; schools/districts has_city; university capital-civ.
Generic buildings (URB_*/EDU_*/IND_*/fortress) have no geo gate. Zero ROW drops.

## #24 sweep — batch-2 review CORRECTIONS (allow-gate + mission parity)

The batch-2 review confirmed all 8 seeds land + mechanical fixes sound, but caught that I'd changed the
`allow` gate the wrong way on the 7 always=no buildings. Engine model (uniform in-repo + cathedral BT#6):
add_building_level RESPECTS potential but BYPASSES allow. So the fix is: real POTENTIAL (seed lands) +
KEEP allow={always=no} (menu stays closed). I had deleted the monuments' allow (→ always-true → region-wide
menu-build snowball) and given the 5 uniques sufficient_job_slots (still menu-buildable region-wide). FIXED:
restored allow={always=no} on all 7 (great_wall/grand_canal/hanlin/guozijian/temple_of_heaven/ancestral/dujiangyan).
Seeds still land (add_building_level bypasses allow); no snowball; WORKS-verb once-only guard still latches.

Also (review LOW items, fixed for parity/robustness):
- se_QING_MISSIONARY_STATIONS: added has_city_status to the pre-treaty historic-city founder (else it could
  stall re-picking a sub-city historic seat forever) and the pre-treaty spread twin (parity w/ treaty-era twin).
  The sink QING_mission_found_station already backstops phantom stations; these close the wasted-pick/stall.
- qing_great_mosque comment corrected: Kashgar 2700 is XNG→ILI→CHI (passes via single-level overlord because
  ILI is manchu; overlord is NOT recursive); region is Gansu (Tarim area), not Turkestan.

Also folded in (earlier #27 intent): Taiwan colonization task (qing_colonization_missions.txt) now plants a
qing_customs_house on owned Taibei (6799/6781) beside the port/commerce — Qing institution on colonized soil.
