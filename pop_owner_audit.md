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

### Owner audit — findings so far
- **CRT (Cartagena) — BUG.** Independent `constitutional_republic`, primary_culture=colombian,
  owns 944 Sincelejo, 4366 Montería, 9689 Cartagena (cap), 2772 Magangué, 8703 Mojana,
  8514 Tierralta, 5171 San Marcos. An independent Colombian republic is ~1811 — anachronistic
  for 1763. These were Spanish New Granada. → FIX: move all 7 to **SFB** (Viceroyalty of New
  Granada, owns all surrounding provinces); empty CRT (QNG-inert). STATUS: pending review+apply.
- SA Spanish hierarchy otherwise correct: SPA→PR1(Peru)→{AR1,LFP,CHR,CHL,PRG}, SPA→SFB(New
  Granada)→{QTO,VNZ→{TNJ,CAU,ANQ}}, Brazil POR→BRZ, Guianas NED→{DUG,BIG}/FRA→FRG,
  Mapuche independent (LFQ/LFM/INP). Unowned=55 (frontier/independent-indigenous — expected).
- Remaining SA tags/provinces: full per-province sweep PENDING.

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
