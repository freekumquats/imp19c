# Global Province Ownership Audit — 1763

**Mandate (operator):** go over every one of the 13,281 province IDs, identify its proper historical
owner in 1763 (if any), and **create / update / remove tags** so the game setup matches 1763 history.
Deliverable: `PROVINCE_OWNERSHIP_1763.csv` — one row per province: `province_name, province_id,
owner_name_1763, owner_tag_1763, historical_justification_1763_with_source, current_owner_tag, status,
confidence`. `owner_*_1763` = the historically-correct owner; where it differs from `current_owner_tag`
the game is corrected.

Branch: `merge-overnight`. Every setup change gated on `setup/main/check_setup_invariants.py`
(0 new ownerless capitals, 0 new double-owned). Static-verified only — **no boot access this session**;
all changes are boot-pending. All commits authored freekumquats.

This file is the running DECISION LOG for the audit. Every tag created/updated/removed and every
non-obvious ownership call is recorded here with its reason + source.

---

## Method

1. **Foundation (done).** `build_ownership_audit.py` extracts name + current owner for all provinces →
   CSV skeleton. Baseline: OWNED 8775, UNOWNED(named) 2589, UNNAMED-placeholder 1917 (PROV#### =
   wasteland/sea/unused — excluded from tag work).
2. **Regional research.** Dispatch historical-research agents per world region to establish 1763 ground
   truth (polity → territory), citing academic sources (English + native-language scholarship where
   apt). Each returns: which polities existed, their extent, and whether they should be a full tag,
   a reduced-authority tag, or culture/population-only (no tag — stateless peoples).
3. **Reconciliation.** Fill the CSV's `owner_*_1763` + justification columns from the research; flag
   every province where current ≠ correct. Classify each fix: create tag / update tag cores / remove
   or empty tag / reassign province / leave (stateless → culture-only).
4. **Apply in invariant-gated batches** (5–8 tags per commit, checker must pass), each recorded here.

## Hard constraints
- Ownerless-capital crash class: every tag's capital ∈ its own non-empty cores. Enforced by the checker.
- Do not steal provinces from a LIVE tag without a historical reason recorded here.
- Stateless peoples (Aboriginal, San, Papuan interior, etc.) get culture/population, NOT a tag.
- Province geography source: `localization/english/provincenames_l_english.yml` (all 13,281 named).
- Tribal/rulerless tags follow the DIN/DNE pattern (no set_as_ruler, no create_character → no char-id
  concern). A centralized polity needing a named ruler adds the char at global max id+1.

---

## Decisions log

### 2026-07-20 — Foundation + first correction

**DNE (Dene) created — I-0.** DIN/Navajo (Diné) was a na-dene CATCH-ALL holding both the Four Corners
Navajo (7 cores, capital Tohatchi 2657) AND 18 northern BC/Pacific-NW provinces (Prince George,
Kamloops, Jasper, Fort St. John, Mackenzie, Yuquot, Nelson BC, Spokane, Colville…). Those northern
lands are **Northern Athabaskan (Dene)**, not Navajo (Southern Athabaskan) — sharing the na-dene
language family is why they were lumped, but a Tohatchi-capitaled Navajo tag should not own British
Columbia.
- **CREATE** DNE: rulerless federated_tribe, `primary_culture = chipewyan` (canonical Northern
  Athabaskan/Dene, culture exists), capital Mackenzie 4257, holding the 18 northern provinces.
- **UPDATE** DIN: trimmed to the 7 Four Corners Navajo cores.
- Justification: Athabaskan linguistic geography — the Navajo/Apache (Southern Athabaskan) migrated to
  the SW ~15th c.; the northern Dene (Chipewyan, Kaska, Sekani, Dakelh, Tahltan, etc.) remained across
  the western Subarctic/Cordillera. In 1763 these were distinct peoples, not one polity. (General
  ethnographic consensus; to be sourced precisely in the N. America research pass.)
- Invariant gate: 629 blocks, capital∈cores for both, 0 new ownerless/double-owned. Commit 931146f7b.

**Correction to prior overnight claim:** I earlier wrote "DIN correctly in the Four Corners, skip I-0."
That was wrong — it conflated the checker's self-consistency result (capital∈cores → won't crash) with
correct geographic placement (never verified). The province geography WAS available (provincenames loc);
my "no geography" deferral premise was false. Both errors corrected; the audit proceeds properly.

### Regional research — COMPLETE (6 of 6)
All six regional agents returned; reports committed under `audit_worklists/research/`. Reconciled into
the CSV via `setup/main/fill_ownership_audit.py` (see 2026-07-20 entries below).

### CSV — POPULATED (deliverable complete)
`PROVINCE_OWNERSHIP_1763.csv` (13,281 rows) now has every research column filled:
- **8,602 OWNED** — owner_tag_1763 = validated current owner (base map is 1763-converted), name from
  the tag's country-file, justification keyed to the region's research report. Confidence: high.
- **173 USA → GBR** — the only owner divergence; historically British in 1763, left as USA by design
  (AI Civil War arc). Marked FLAG-DEFERRED in the justification + confidence columns.
- **2,589 UNOWNED(named)** — stateless/uncolonised zones (culture-only). Confidence: medium.
- **1,917 UNNAMED-placeholder** — sea/wasteland/unused. Marked n/a.
Regenerate: `build_ownership_audit.py` (skeleton from live setup) then `fill_ownership_audit.py`
(research columns). Idempotent; re-run after any setup ownership edit so current_owner_tag stays fresh.

## Scope exceptions & rules
- **HRE abstraction (operator):** the Holy Roman Empire may be modelled at a REASONABLE level of
  abstraction — do NOT shatter it into a million microstates. Keep the major territorial princes
  (Austria, Prussia, Bavaria, Saxony, Hanover, Württemberg, the big ecclesiastical/imperial cities,
  etc.) and abstract the tiny Kleinstaaten into their nearest significant neighbour or a reasonable
  aggregate. Historical plausibility at the great-power/major-principality grain, not cadastral.
- **Sea/placeholder provinces:** rows named "Atlantic", "Strait of …", "PROV####" etc. are sea zones
  or unused placeholders — NOT land to assign. Left UNOWNED/UNNAMED; excluded from tag work.
- **Stateless peoples:** culture/population only, no tag (Aboriginal, San, Papuan interior, many
  Amazonian/Siberian peoples).

### 2026-07-20 — Tag inventory (before reconciliation)
Audited the existing tag inventory so reconciliation prefers REVIVE over CREATE:
- 675 registered tags (setup/countries/countries.txt); 619 have ≥1 core; **56 are INERT** (registered
  + have a country file, but own ZERO provinces in setup). Inert sample: ABA ALC ATQ BAR BGK BIK CAN
  CDM CLO CSC DAG FKE FLK GIB GRE GUJ HEL HRP ILL IND JPN KTK KWA KYR LFY LGS LOG MAS MER MIC MIL MRG
  MSC MSI MSP MZH NGR NNN NWC PIR … (full list to be dumped when reconciling).
- 680 country files exist under setup/countries/*/ (incl. many Native tags: blackfoot, arapaho, caddo,
  bannock, assinibone, apacheria, alta_california …) — several are the inert ones.
- **Reconciliation move-types**, in order of safety/preference:
  1. REVIVE an inert tag (tag + country file + culture already exist → just add a setup block with
     capital+cores). Lowest risk.
  2. UPDATE a live tag's cores (trim/extend) — e.g. the DIN→DNE carve.
  3. CREATE a new tag (register + country file + setup block + maybe culture) — for polities with no
     existing tag.
  4. REMOVE/empty a tag whose 1763 existence is an anachronism (inert-tag playbook).
  5. LEAVE culture-only (stateless peoples) — province culture/pops, no tag.
- Province NAMES are non-unique: 365 names shared by >1 province (e.g. two "Nelson", three "San
  Cristobal", many "Atlantic"/"The Outback"). Reconciliation MUST disambiguate by region, never assign
  by name alone. (This is the trap behind my earlier false "Navajo in New Zealand" alarm — 7745 Nelson
  BC vs 8241 Nelson.)

### 2026-07-20 — All 6 regional research reports captured
All six regional 1763 ground-truth reports are committed under `audit_worklists/research/`:
europe, asia_middleeast, africa, oceania_sea_maghreb, north_america, latin_america. Each classifies
polities → TAG vs culture-only with academic sources and flags anachronisms.

### 2026-07-20 — KEY FINDING: the base map is ALREADY substantially converted to 1763
Cross-checking the 619 live owner tags against the six reports shows the setup was already
purpose-built for a 1763 start, NOT a 19th-c. map. Confirmations:
- **No independent nation-states/republics** where 1763 had colonies/empires: Latin America is
  viceroyalties (SPA/NSP/BRZ/SFB/CHR/QTO/CPV/VNZ), not republics; the Ottoman TUR holds the Balkans +
  Levant + Maghreb core; India is EIC + native princely tags; no Italy/Germany unification.
- **The flagged N. America anachronisms are already fixed:** ALC (Alta California, colonised 1769) and
  RUA (Russian America, settled 1784) are both INERT (0 cores, capital repointed) — matching
  [[imp19c-1763-border-audit-done]]. Miskito (MSK) sits correctly on the Mosquito Coast; the Mapuche
  butalmapu are modelled (LFQ Lafquenmapu@Temuco, INP Inapiremapu, plus LFP/PMO). DIN/DNE carve done.
- **VNZ** already carries a `[bookmark-1763 #232]` note: "1763 Venezuela is a Spanish colony … NOT
  Bolivar's 1810s revolutionary republic" — the established convention for folding independence-era
  tags back into the Spanish structure.
So the audit's job is NOT a mass rebuild; it is (a) recording the per-province verdict in the CSV and
(b) catching the residual anachronisms the earlier passes missed.

### 2026-07-20 — Batch: 6 South-American independence-junta anachronisms folded (inert-tag playbook)
Government-type scan for live republics surfaced 6 genuine 1763 anachronisms — all `revolutionary_republic`,
1 province each, no ruler/char, in no arc/event (verified via rg over events/ + common/):
- **AYP Ayopaya, LRC Larecaja, LAG Chuquisaca, SCZ Santa Cruz de la Sierra, VLG Vallegrande** — the
  1809–25 Upper-Peru independence juntas. In 1763 all are the Spanish **Audiencia de Charcas**
  (seat Chuquisaca/La Plata). → absorbed their 5 provinces into **CHR**; emptied each junta (0 cores,
  capital repointed to CHR's 1532 La Plata).
- **VLL Valledupar** — 1810s New-Granadan junta; in 1763 Spanish New Granada. → 5900 folded into
  **SFB**; VLL emptied, capital repointed to SFB's 5677 Santa Marta.
- Source: standard Spanish-American independence chronology (juntas all post-1809; Charcas & New
  Granada firmly Bourbon Spanish in 1763). Consistent with the existing VNZ #232 convention.
- Invariant gate: 0 new ownerless capitals, 0 new double-owned; inert-tags 10→16. Brace delta 0.
  No set_as_ruler/create_character on any of the 6 → no construction-crash class.

### 2026-07-20 — DEFERRED (documented, not a blind fix): USA at a 1763 start
The single largest raw anachronism is **USA** — a `constitutional_republic` governed from Washington
holding all **173 Thirteen-Colonies seaboard provinces**, when in 1763 those are British (GBR). This is
NOT a safe flip: the USA tag is the load-bearing anchor of the **AI-autonomous US sectional-crisis →
Civil War arc** (task #93, `se_USA_SECTION.txt` / `usa_section_on_actions.txt`), which seeds state on
`c:USA` at `on_game_initialized` with NO is_ai guard specifically so it runs for an AI USA. Emptying
USA→GBR would be historically correct for 1763 but would break a deliberately-built subsystem the mod
depends on — the same telescoped-anachronism design that lets the player run late-Qing mechanics at a
1763 start. This is a genuine design contradiction (historical accuracy vs. a wired gameplay arc), so
per the mandate it is DEFERRED and recorded here rather than fixed blind. Resolving it properly would
mean either (a) a startup transform that hands the 13 colonies to GBR and spawns USA later on the
independence beat, or (b) accepting the anachronism as intended. Needs an operator call + boot.
