# DESIGN — Seed Qing garrisons in Altishahr/Tarim for 1763 (#21)

**Branch:** merge-overnight. **Status:** DESIGN (needs adversarial review before build). **Scope:** setup seed.
**Research:** research/RESEARCH_QING_XINJIANG_GARRISONS_1763.md.

## 0. Problem
Boot test: the Outliner shows an Ili Banner Garrison (4,500) + interior banner garrisons, but **Altishahr/Tarim
has NO garrison** — historically wrong. The Ili General (est. 1762) garrisoned the Tarim oases (Kashgar,
Yarkand, Aksu, Ush, Khotan, …) with rotating Green Standard under Resident Ministers over beg 伯克 rule.

## 1. How garrisons are currently seeded (verified)
`imp19c_setup.12` (events/imp19c_mod_events/imp19c_setup_events.txt:290, the #234 seed) places the BUILDING
`qing_banner_garrison_building` (and `qing_military_colony_building` tuntian) on named subject-capital province
IDs, each guarded: `exists = p:N`, `p:N = { owner = { is_subject_of = ROOT } NOT = { has_building = ... } }`.
ILI's garrison is on p:3534. It is a BUILDING seed, not create_unit. (The "4,500 army" the player sees is the
garrison the building represents / spawns.)

## 2. TWO BLOCKERS that make this NOT a copy-paste of the ILI seed

### BLOCKER A — XNG is a NESTED subject; `is_subject_of = ROOT` fails
Kashgaria/Altishahr = tag **XNG**, capital **Kashgar p:2700**, owns the Tarim belt (own_control_core: 2700
2977[Aksu] 2075 3659 5271 174 1732 4527 5280 6880 2062 8872 8129 498 5226 8648 4253 2354 6065 6396 — 20 provs).
XNG is `client_state of ILI`, and ILI is a subject of CHI → **nested CHI→ILI→XNG**. `is_subject_of` is
NON-RECURSIVE ([[imp19c-is-subject-of-not-recursive]]), so the seed's `owner = { is_subject_of = ROOT }` guard
is FALSE for XNG-owned provinces. **FIX: use the nested-overlord guard** `owner = { overlord = { is_subject_of
= ROOT } }` for XNG provinces (one extra `overlord` level per nesting tier).

### BLOCKER B — the garrison building's POTENTIAL gate rejects uighur XNG
`qing_banner_garrison_building` potential = `owner = { country_culture_group = jurchen }`
(qing_military_buildings.txt:39-41). ILI is **manchu** (jurchen group) → passes. XNG is **uighur** (east_turkic
group, 00_east_turkic.txt:49) → **FAILS**. And `add_building_level` RESPECTS potential — force-adding to a
gate-failing province HIDES the building ([[imp19c-add-building-level-respects-potential]]). So even with the
guard fixed, the building would not take on XNG soil.
**FIX OPTIONS (pick in review):**
- (B1) WIDEN the garrison building potential to also admit a Qing-subject owner regardless of culture group
  (e.g. `OR = { owner={country_culture_group=jurchen}  owner={overlord={is_subject_of=CHI}}  ... }`) — the
  #234 precedent widened building gates to admit Qing subjects. Cleanest if the building is the right object.
- (B2) Use a DIFFERENT representation for the Tarim (light, non-banner) garrison — the history is ROTATING
  GREEN STANDARD, not banner. A Green-Standard/rotating-garrison building (if one exists) or a lighter modifier
  is more historically apt for Altishahr than the banner-garrison building (which is a 駐防八旗 — a NORTHERN
  institution). Check what garrison/military buildings exist besides qing_banner_garrison_building.
- **LEANING B2** (or a mix): Kashgar/Yarkand get a Green-Standard-style garrison (historically correct), NOT the
  banner building. Confirm the building vocabulary in review.

## 3. Per-province ownership (verify EACH before seeding — owner varies)
- Tarim oases (Kashgar 2700, Aksu 2977, + the 20 XNG core provs) → owner XNG (nested; guard via overlord).
- Ürümqi p:2930 → owner **ILI** (in ILI's core, not XNG) → direct `is_subject_of = ROOT` guard works, manchu
  culture passes the banner gate → Ürümqi can take the banner building directly.
- So the seed splits: NORTH (Ürümqi, ILI-owned, manchu → banner building, existing guard) vs SOUTH (Tarim,
  XNG-owned, uighur → the B1/B2 fix + overlord guard). This mirrors the research's N-heavy/S-light asymmetry.

## 4. Anachronism gate (research caveat)
Do NOT seed cities that post-date 1763: Tarbagatai (built 1764), Huiyuan finished 1766, the Sibe battalion
(arrived 1764). Kashgar/Yarkand/Aksu/Ush/Khotan garrisons + Ürümqi ARE 1763-extant (post-1759 conquest). Seed
only those.

## 5. Proposed seed (subject to B1/B2 decision + review)
Add to imp19c_setup.12, SOUTH block (XNG, overlord guard + culture-safe building):
- Kashgar p:2700 — the Tarim command seat (largest southern garrison).
- Yarkand, Aksu p:2977, Ush, Khotan — smaller oasis garrisons.
NORTH block (ILI, existing guard + banner building):
- Ürümqi p:2930 — banner garrison (size between Ili and the Tarim oases).
Sizes: the buildings are level-based, not troop-count; the N-heavy/S-light asymmetry is expressed by WHICH
building (banner vs green-standard) + whether a tuntian colony accompanies it (North yes, South no — Han
settlement was banned in the Tarim). Verify province IDs for Yarkand/Ush/Khotan (not yet pinned — grep
setup/provinces/00_Turkestan.txt).

## 6. Files affected
- `events/imp19c_mod_events/imp19c_setup_events.txt` — extend imp19c_setup.12 (SOUTH XNG block + Ürümqi).
- `common/buildings/qing_military_buildings.txt` — IF B1: widen qing_banner_garrison_building potential; OR
  identify/point at a Green-Standard garrison building for the Tarim (B2).
- (loc only if a new building is introduced.)

## 7. Build checklist
1. RESOLVE B1 vs B2 in review (widen banner potential vs use a Green-Standard garrison for the Tarim).
2. Pin the remaining Tarim province IDs (Yarkand/Ush/Khotan) from setup/provinces/00_Turkestan.txt.
3. Verify each target province's actual 1763 owner (XNG vs ILI vs CHI) → pick the right guard per province.
4. Add the seed blocks (overlord guard for XNG; direct guard for ILI's Ürümqi), each guarded exists +
   not-already-present, matching the existing imp19c_setup.12 idiom.
5. Boot-test: confirm the garrison buildings TAKE (has_building true after day 2) on the Tarim provinces
   (i.e. the potential fix worked — not silently hidden), and appear in the Outliner.
6. Confirm no new error.log classes; confirm anachronistic cities NOT seeded.

## 8. Risks
- **R1 (BLOCKER B):** add_building_level respects potential — if the culture gate isn't fixed, the seed
  SILENTLY no-ops (building hidden). MUST resolve B1/B2 or the whole task fails invisibly. Boot-verify has_building.
- **R2 (BLOCKER A):** wrong guard → seed skips XNG. Use the overlord guard.
- **R3 double-count with #19:** #19 (concrete-garrison-link) will make QING_xj_derive_control COUNT garrison
  objects. If #21 seeds garrison buildings that #19 then counts, the two must be designed together so control
  isn't double-fed. Sequence #21 (seed the objects) before/with #19 (count them).
- **R4 historical building choice:** the banner building (駐防八旗) is a NORTHERN institution; using it for the
  Tarim (which had Green Standard, not banners) is a fidelity compromise. B2 (green-standard) is more correct.
