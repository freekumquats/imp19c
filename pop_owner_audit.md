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
