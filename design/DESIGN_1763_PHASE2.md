# DESIGN_1763_PHASE2.md — Full political-map surgery for the 1763 bookmark

**Branch:** `1763_bookmark`. **Status:** DRAFT (staged 2026-07-08). Companion to `1763_bookmark.md`
(master decision log) and `BOOKMARK_PROCESS.md` §10 (methodology). All commits authored + committed
by `freekumquats`.

> **GATE:** The engine-mechanics section (§2) is PENDING the oracle consult (task #230, Terra-Indomita
> + Invictus). No Phase-2 building starts until that verdict lands and this doc's §2 is filled + the
> approach confirmed. This draft stages the region inventory, mapping tables, risk ranking, and
> sequencing that do NOT depend on the verdict.

---

## 1. WHAT PHASE 1 ALREADY PROVED (the baseline Phase 2 extends)

Phase-1 PoC (committed, boot-test still OWED) established the setup-file surgery pattern on the 2–3
hardest cases:
- **New tags with provinces at game start:** LIT (Grand Duchy), VEN (Venice) — registered in
  `setup/countries/countries.txt` + a country file + given provinces/gov/culture/religion/capital in
  `setup/main/00_default.txt`. Booted (pending in-game confirm).
- **Tag-only registration (no provinces yet):** GEN (Genoa), MIL (Milan) — registered but not yet
  placed on the map. Phase 2 must give them provinces.
- **Subjects via `dependency` in setup:** RUS → POL(protectorate) → LIT(royal_union) nested chain;
  SPA → MEX(client_colony) reversion.
- **Government-type swaps:** POL viceroyalty→aristocratic_monarchy; MEX revolutionary_republic→viceroyalty.
- **Province ownership moves** via `own_control_core` (both sides) — #218 LIT core (95 prov),
  #229 PLC border (32 prov).

Phase 2 = the SAME idioms applied at scale across the rest of the world.

---

## 2. ENGINE MECHANICS — ORACLE-VERIFIED (#230, 2026-07-08)

**Bottom line: Phase 2 full-map surgery via SETUP FILES is FEASIBLE. `create_country` is NOT needed** —
it is a runtime-only spawn (revolts/breakaways). Every 1763 country exists at game start, so setup
files handle everything. Evidence: all three mods activate their entire country roster purely via
setup files (imp19c 580 active / 650 registered; Terra-Indomita 498 / 1022; Invictus 411 / 741).

### 2.1 Q1 — Setup-file tag activation → **FEASIBLE**
A tag owns provinces at game start with NO `create_country` if: (a) registered in
`setup/countries/countries.txt` → its country file, (b) given a country block in
`setup/main/00_default.txt`. **Mandatory fields** (100% of samples, zero exceptions): `government`,
`primary_culture`, `religion`, `capital`, and `own_control_core` (if it owns land). Capital MUST be a
province the tag owns. Idiom:
```
# setup/countries/countries.txt
GEN = "setup/countries/italy/genoa.txt"
# setup/main/00_default.txt  (inside country = { countries = { ... } })
GEN = {
    government = oligarchic_republic
    primary_culture = north_italian
    religion = catholic
    capital = <owned_prov_id>
    own_control_core = { <prov ids...> }
}
```
This is EXACTLY the Phase-1 idiom (LIT/VEN), now confirmed to scale.

### 2.2 Q2 — Tag-count ceiling → **FEASIBLE to 500-600 active**
No hard limit found; registry handles 1000+ names (TI 1022). imp19c already ships 580 active cleanly.
Phase 2 net change is modest (+50-100 active est.: adds pre-partition Poland/pre-unification Italy/more
colonial subjects, but SUBTRACTS independent Latin-American states via reversion). Well within proven
range. **File-size caution:** 00_default.txt is already ~90k lines; consider splitting new blocks into
a numbered file (TI uses `02_countries.txt`) — engine reads all setup/main/*.txt.

### 2.3 Q3 — `dependency` subject_type in setup → **FEASIBLE, all types**
royal_union / protectorate / client_colony CONFIRMED valid in setup blocks (imp19c already uses
royal_union 14×, protectorate 28×, client_colony 37×, client_state 42×, feudatory 56×, tributary 31×,
etc.). Full valid set from `common/subject_types/00_default.txt` (16): vassal_tribe, tributary,
sinosphere_tributary, nominal_vassal, protectorate, feudatory, satrapy, client_state,
autonomous_governorship, semi_autonomous_governorship, subsidiary_ally, autonomous_colony,
client_colony, territory, royal_union, confederate_ally. The subject_type `allow = {}` block gates
runtime negotiation only — NOT setup placement. Idiom (AFTER all country blocks):
```
dependency = { first = SPA second = MEX subject_type = client_colony }
```

### 2.4 Q4 — `create_country` (runtime) → **FEASIBLE but OUT OF SCOPE**
Runtime-only (rebellions/scripted secession). Idiom for reference (imp19c flavour_middle_east.txt:112):
`p:<id> = { create_country = { name={name=.. adjective=..} set_primary_culture=.. set_country_religion=..
change_government=.. save_scope_as=X add_treasury=.. } }` then `p:<id2> = { set_conquered_by = scope:X }`.
Phase 2 does NOT use this — everything is game-start.

### 2.5 Q5 — Province reassignment at scale → **FEASIBLE, explicit ID lists**
No bulk/range/area idiom exists anywhere — explicit space-separated province IDs in `own_control_core`
is the universal norm (TI ships 200+ prov/country this way, no perf issue). `own_control_core` sets
owner + controller + de-jure core together for setup. No wasteland/uncolonized gotcha in setup.
**Practice:** comment ID groups by voivodeship/region for review (as #218/#229 did); one commit per
region for reviewable diffs; generate lists from the area map as a preprocessing step (off-engine).

**Net: the Phase-1 idiom is the Phase-2 idiom, proven to scale. No new engine capability required.**

---

## 3. REGION INVENTORY & 1815→1763 MAPPING TABLES (research-backed)

Source: `research/1763_WORLD_*.md`. Each region carries a "1815-independent-tag → 1763-overlord"
mapping (the reversion table) OR a "missing-tag → provinces to assign" list.

### 3A. AMERICAS (reversion — undo independence; `research/1763_WORLD_Americas.md`)
The 1763 Peace of Paris partition (already noted): FRANCE→GB (Canada + east-Mississippi), FRANCE→SPA
(Louisiana), SPA→GB (Florida). Then the Spanish/Portuguese colonial reversion — bind each 1815-
independent tag to its 1763 overlord as a colony (mechanic per §2; MEX PoC used `client_colony`):

| 1815 tag | 1763 overlord (Spanish viceroyalty/captaincy) |
|----------|-----------------------------------------------|
| MEX (Mexico) | New Spain |
| Central America / Guatemala | Captaincy-General of Guatemala (under New Spain) |
| GCO (Gran Colombia) | New Granada |
| COL (Colombia) | New Granada |
| VEN* (Venezuela) | Captaincy-General of Venezuela (under New Granada) — *tag collision risk with Venice; verify |
| ECU (Ecuador) | Audiencia of Quito (under Peru in 1763) |
| PER (Peru) | Viceroyalty of Peru |
| BOL (Bolivia) | Upper Peru / Charcas (under Peru) |
| CHL (Chile) | Captaincy-General of Chile (under Peru) |
| ARG (Argentina) | Río de la Plata region (under Peru — RdlP viceroyalty not created until 1776) |
| PRY (Paraguay) | Gobernación del Paraguay (under Peru) |
| URU (Uruguay) | Banda Oriental (under Peru; disputed w/ Portugal) |
| CUB (Cuba) | Captaincy-General of Cuba (under New Spain) |
| PRI (Puerto Rico) | under Cuba / New Spain |
| DOM (Santo Domingo) | under Cuba / New Spain |
| Brazil (POR colony) | Estado do Brasil (capital → Rio 1763) |

**NOTE (tag collision):** research uses "VEN" for Venezuela but VEN is now VENICE. Venezuela must use a
different tag or fold into New Granada. FLAG for resolution before building.

### 3B. ITALY (missing tags + reversion; `research/1763_WORLD_Italy.md`)
- **VEN (Venice)** — DONE in Phase 1 (independent republic; →Austria 1797).
- **GEN (Genoa)** — registered, needs provinces (independent republic; →Sardinia 1815).
- **MIL (Milan)** — registered, needs provinces (Austrian Lombardy in 1763; folded into 1815
  Lombardy-Venetia).
- Other Italian states (Tuscany, Modena, Parma, Papal States, Naples/Two Sicilies, Lucca, San Marino):
  check which exist as tags vs. need creation; full transformation table at Italy.md:280.

### 3C. CENTRAL EUROPE / HRE (the biggest delta; `research/1763_WORLD_CEurope_HRE.md`)
Hundreds of pre-1803-mediatization states, incl. ~23 ecclesiastical principalities (Salzburg,
Würzburg, Bamberg, Münster, …) all gone by the 1815 German Confederation. **This is the hardest and
largest region.** Likely a documented LIMITATION rather than full representation — scope to be decided
after the oracle tag-ceiling verdict. Watch tag collision TRI = Tripoli (not Trier).

### 3D. E. EUROPE — largely handled (PLC done via #208/#218/#229). Remaining: Crimea/Ottoman vassals
(`research/1763_rulers_crimea_ottoman_vassals.md`), Sweden (`1763_rulers_sweden.md`).

### 3E. OTTOMAN / MENA / PERSIA (`research/1763_WORLD_Ottoman_MENA.md`, `1763_MENA_independent_states_partial.md`)
Zand Persia (not 1815 Qajar), First Saudi State/Diriyah (exists 1763, destroyed 1818), Egypt/Iraq
Mamluks, Morocco, Oman. Ruler swaps + some tag work.

### 3F. S ASIA (`research/1763_WORLD_SouthAsia.md`)
Collapsed Mughal (Shah Alam II) + Maratha confederacy post-Panipat + Durrani + Bengal-EIC +
Mysore/Hyderabad. Multipolar patchwork vs 1815 EIC raj — mostly ownership + ruler surgery.

### 3G. E + SE ASIA (`research/1763_WORLD_EAsia_SEAsia.md`)
Edo Japan (Ieharu), Joseon (Yeongjo), **divided Vietnam** (Trịnh/Nguyễn), **Ayutthaya Siam** (not
Bangkok), Konbaung Burma, VOC insular SE Asia. Qing itself already done (Part A).

### 3H. AFRICA (`research/1763_WORLD_Africa.md`)
Asante/Oyo/Dahomey, pre-Sokoto Hausa states (no 1804 Caliphate), Ethiopia, **Dutch (not British)
Cape**, Omani Swahili coast. Mostly ruler + ownership; some tag work.

---

## 4. RISK RANKING (hardest → easiest) & SEQUENCING

Per BOOKMARK_PROCESS §10.2 "prove the tag mechanic on the hardest regions first" — Phase 1 already did
the composite-monarchy (PLC) + missing-tag (Venice) hardest cases.

1. **HRE / C.Europe (HARDEST)** — hundreds of states; likely partial + documented limitation. Do LAST
   or scope-cap after the tag-ceiling verdict.
2. **Italy** — finish GEN/MIL provinces + remaining states (medium; tag mechanic proven).
3. **Americas** — high province churn but LOW regression surface (research #198: Latin-American tags
   have ZERO mission/event deps). Reversion via dependency (proven by MEX PoC). Resolve the VEN/VEN
   tag collision first.
4. **Ottoman/MENA, S Asia, SE Asia, Africa** — mostly ruler + ownership swaps; fewer new tags.
   Lower risk once §2 idioms are confirmed.

**Proposed build order:** Americas reversion (proven pattern, low regression) → Italy completion →
Ottoman/S Asia/SE Asia/Africa ruler+ownership → HRE last (scoped). Each region: build → per-region
regression re-check (grep `tag = XXX` in missions/events for that region's tags) → adversarial review →
commit as freekumquats → in-game boot test before the next region.

---

## 5. STANDING-RULE DISCIPLINE (applies to every Phase-2 region)
- **Oracle-before-unproven:** §2 must be settled before ANY building (#230).
- **Review-before-commit:** deep adversarial review per region batch before commit; branches don't cross.
- **Concrete over abstract:** real province/tag/subject objects (this whole phase already is).
- **Fix-traceability:** task-tagged `[bookmark-1763 #NNN]` comments + SESSION_REPORT entry +
  1763_bookmark.md Part B decision record per region.
- **No promotion off `1763_bookmark`** without the user's in-game verification + explicit request.
- **Tag-collision audit:** before creating/assigning any tag, grep `setup/countries/countries.txt` for
  the intended 3-letter code (known collisions: VEN=Venice vs Venezuela; TRI=Tripoli vs Trier).

---

## 6. SCOPE DECISIONS (LOCKED by user, 2026-07-08)
- **HRE scope:** **Major states + fold the rest.** Represent the ~15-25 significant 1763 states as tags;
  fold minor mediatized statelets into their eventual 1815 absorber (Austria/Prussia/Bavaria/…).
  Accepted, DOCUMENTED limitation.
- **Americas:** **Full reversion of all ~15 LatAm tags** — but see §7: the baseline is ALREADY largely
  colonial, so this is a DELTA-to-1763, not a from-scratch reversion.
- **Tag collisions:** **New distinct tags.** Venezuela already exists as `VNZ` (VEN=Venice is safe).
  Trier (electorate) needs a new code (candidate KTR/TRR — grep countries.txt; TRI=Tripoli is taken).

---

## 7. BASELINE CORRECTION (discovered 2026-07-08 — supersedes §3's assumptions)

Inspecting the LIVE `setup/main/00_default.txt` (not the research tables) shows the 1815 baseline is
**far more colonial than §3 assumed**. The Americas are already modelled as a Spanish/Portuguese
colonial TREE, so Phase 2's Americas job is the narrow 1763 DELTA, not a mass reversion:

- **Existing Spanish tree** (00_default.txt ~757-771): `SPA→QTO` (Quito), `SPA→PR1`(Peru)`→CHL`/`CHR`,
  `SPA→NSP`(New Spain)`→GUA`/`FLO`/`SEM`/`PHI`/`ALC`, `SPA→SFB`, `SPA→CPV`, `SPA→MEX`
  (`MEX` already tagged `[bookmark-1763 #208]`).
- **`VNZ` (Venezuela) already exists** as its own tag WITH subjects `TNJ`/`CAU`/`ANQ` (~1043-1045) —
  the collision question is already resolved in-repo.
- **`POR→BRZ`** (Brazil) already a client_colony (~899).
- **PR1 = Peru** (Americas), so the Persia tag is **PR2** (Qajar) — the Zand/Qajar dynasty delta is a
  separate issue flagged to the Ottoman/MENA recon. NOTE the PR1/PR2 ambiguity explicitly.

**The real 1763 Americas deltas are therefore narrow:** Río de la Plata should NOT exist yet (ARG/PRY/
URU under Peru, not a separate RdlP); Florida → Britain (Spain ceded it 10 Feb 1763); Louisiana W of
Mississippi + New Orleans → Spain, E of Mississippi → Britain; Canada/Quebec → Britain; USA → British
Thirteen Colonies; Haiti → French Saint-Domingue; viceroy ruler/gov corrections.

**Same correction applies world-wide:** the baseline already has rich vassal trees (Ottoman ~777-812,
Qajar ~814-822, Qing tributaries ~824-884, Ethiopia ~886-890, Dutch/Danish colonies). So EVERY region
is a delta, not a rebuild. **Method (locked):** one read-only recon agent per region cross-references
the live 00_default.txt against `research/1763_WORLD_<region>.md` and writes an exact itemized edit
plan to `research/1763_DELTA_<region>.md` (tag, current line #, precise target, area/region names for
province moves — NO guessed IDs). Build proceeds region-by-region off those delta plans, in the §4
order (Americas → Italy → Ottoman/Asia/Africa → HRE last), each: build → per-region regression grep →
adversarial review → commit as freekumquats → in-game boot test before the next region.
