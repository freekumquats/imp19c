# DESIGN: 1763 starting-tech seeding by culture-group bloc

Status: REVISED post-adversarial-review (2026-08-25), ready to implement. Scope: the
`else` (pre-1815) branch of `TECH_unlock_all_starting_techs` in
`common/scripted_effects/se_TEST.txt`. The `current_date >= 1815.1.1` branch is frozen —
do not touch it.

## Corrections from adversarial review (applied below)

1. **`commissioned_staff` moved OUT of the SYW-safe set.** Its actual in-game description
   (`localization/english/technology_l_english.yml:37`) is meritocratic officer commissioning
   ("any soldier that proves their worth... can obtain a commission") — this is the
   career-open-to-talent reform of Revolutionary France / Prussia, explicitly breaking with
   ancien-régime purchase/birth systems (France's 1781 Ségur Ordinance went the OTHER way,
   barring non-nobles). Not real anywhere in Europe by 1763.
2. **oratory_level_4 (central banking) is NOT a whole-Bloc-A grant.** Only Britain (Bank of
   England, 1694) and the Dutch Republic (Amsterdam Wisselbank, 1609) qualify. France's own
   central bank (Banque Royale) collapsed in 1720; no French central bank existed until 1800.
   Granting it to Hungary/Scandinavia/Italy/the Baltic/etc. alongside France was wrong twice
   over. Split into a GBR+NED-only carve-out (mirrors the existing `c:GBR` tag-scoped pattern
   already in the file), NOT a whole-bloc grant.
3. **Three "current state" claims were wrong** — re-verified against the actual 1763 branch
   already in the file (not the 1815 branch): Bloc C's civic cap is already correctly at
   level 2 (nothing to trim), Bloc D's civic cap is already correctly at level 2 (nothing to
   trim — the level-3 reference was from the 1815 branch), and the Sub-Saharan Africa
   tradezone grant already exists in BOTH branches (`se_TEST.txt`'s tradezone `every_country`
   block) — so Bloc E's "zero grant" framing only genuinely applies to Native American
   culture groups, not Sub-Saharan Africa as a whole.
4. **SYW subset macro corrected to cover all 19 items in `military_level_3` with an explicit
   verdict on each**, resolving an inconsistency where Bloc A dropped `naval_explosives` (no
   stated reason) while Bloc D kept it. Resolved by excluding it from BOTH — it's ambiguous
   (likely represents 19th-century explosive shell doctrine, distinct from the separately-teched
   `tech_torpedoes`) and consistency beats a shaky keep.
5. **`copper_plating` dropped from the 1763 branch entirely**, not just re-scoped. Royal Navy
   copper hull-sheathing was a single experimental ship (HMS Alarm) in **1761**, with fleet-wide
   adoption only from **1779** (after solving galvanic hull-fastening corrosion) — post-1763
   even for Britain specifically, and it was Britain-only for decades after that.
6. **Bloc E's West-African firearms example swapped.** Hausa firearms adoption is more securely
   a 19th-century (Sokoto Caliphate, post-1804) phenomenon; the coastal Atlantic-trade states
   (Dahomey, Asante, Oyo) are the better-evidenced 1763 West African firearms example. Doesn't
   change the recommendation, just the citation — and this bloc is implemented as a coverage
   catch-all (see below), not a hand-picked culture-group list, so the specific example no
   longer gates anything in code.
7. **Coverage gaps closed with a provably-complete catch-all**, not a hand-enumerated list.
   The review found ~10+ culture groups (Native American, mongolic, kartvelian, siberian_turkic,
   east_turkic, non-CHI chinese_group/jurchen, malagasy, swahili_group, berber, Southern African
   Bantu groups) matching NONE of the mod's OR-lists, and flagged that `southern_africa_tradezone`
   exists in the trigger file but was never referenced. Rather than hand-listing every group (the
   error-prone approach that produced this gap in the first place), the implementation below adds
   `southern_africa_tradezone` to the existing geography catch, then uses a marker-variable
   catch-all at the very end of the 1763 branch to grant the minimal floor to any country that
   didn't already qualify for something bigger — by construction, nothing can fall through.

## Problem

The starting-tech effect was tuned for the 1815 bookmark and fired ungated regardless
of date. The first-pass 1763 fix (this session) added a date branch but used a crude
**uniform tier cap** (military 0-1, oratory 1-2, civic 1-2, religious 1-2) across every
bloc. That heuristic is wrong in two directions, which this audit corrects.

## The two granularity problems the uniform cap missed

1. **Tier boundaries cut through mixed-era content.** A single tech LEVEL macro bundles
   inventions of different real-world dates. Capping at a whole tier either grants
   anachronistic items inside an otherwise-OK tier, or denies period-OK items to avoid the
   anachronistic ones. Two tiers are especially mixed:
   - **military_level_3** (19 items total, every one now given an explicit verdict):
     - OK for 1763: sword_bayonet, mortar, wheeled_cannons, limber, howitzer,
       multiple_deck_warships, regimental_structure, specialised_corps (Royal Artillery 1716,
       Royal Engineers 1716 — specialized corps as an institution predates 1763), cartography
       (national triangulated surveys underway by the 1750s, e.g. the Cassini map of France).
     - Anachronistic, excluded: replaceable_weapon_parts (interchangeable-parts manufacturing,
       1770s-80s Honoré Blanc onward), rifles [as mass-issue infantry arm] (Napoleonic-era),
       naval_explosives (ambiguous; likely 19th-c. explosive-shell doctrine, distinct from the
       separately-teched `tech_torpedoes` — excluded for consistency, not kept in one bloc and
       dropped in another), carronade (1778), round_bow_megavessels (reads as a later,
       escalated ship-of-the-line category beyond ordinary 1763 first-rates — excluded
       conservatively), copper_plating (1761 single experimental ship, 1779 fleet-wide —
       post-1763 even for Britain), commissioned_staff (meritocratic commissioning — see
       correction #1 above), mass_mobilisation (1793 levée en masse), skirmisher_corps and
       mass_artillery (both Napoleonic doctrine).
   - **religious_level_3** is mostly period-OK for Enlightenment Europe (scientific_method,
     secular_sciences, neoclassicism [EMERGING movement ~1755-64 — Winckelmann's key text 1755,
     Herculaneum excavations from 1738; note his major *Geschichte der Kunst des Alterthums* is
     1764, one year AFTER the bookmark, so grant this as an emerging style, not a fully mature
     one]) but contains two 19th-century items (astrophysics, absorption_spectroscopy
     [spectroscopy = 1859]). Note: astronomy is NOT in this tier — it's already in
     religious_level_1, granted everywhere; an earlier draft of this doc mistakenly listed it
     here.
   - **civic_level_2** looked risky but is actually period-OK: artificial_canals (Canal du
     Midi 1681, British canal age from 1760s), gear_systems (millwork), templating, and
     mining_rails (wooden mine wagonways existed from the 1600s — NOT modern rail).

2. **civic_level_3 is the real Industrial-Revolution line, and it is universal.** spinning_frame
   (Arkwright water frame, 1769) and threshing_machine (Meikle, 1786) postdate 1763 for
   EVERYONE. So does everything in civic_level_4+ (mechanical_tools, manufactories,
   blast_furnace [as a *tech tier* here], electricity, reciprocating_engine, telegraph).
   **No bloc should receive civic_level_3 or higher at a 1763 start.** This is the single
   firmest line in the whole audit.

## Audit: what is genuinely pre-1763 vs anachronistic

Tier-by-tier verdict (real-world dates):

| tier | contents | 1763 verdict |
|---|---|---|
| military_0 | weapon_manufacturing, firearms, shipyards | OK — universal |
| military_1 | permanent_army, field_ambulances, warships, cannons | OK for organized states (standing armies normal by 1763) |
| military_2 | bombard_cannons, warships | OK |
| military_3 | 9 SYW-safe items (see subset list above) **+** 10 anachronistic items (replaceable_weapon_parts, rifles, naval_explosives, carronade, round_bow_megavessels, copper_plating, commissioned_staff, mass_mobilisation, skirmisher_corps, mass_artillery) | MIXED — grant the 9-item SYW subset macro only, never the whole tier |
| oratory_1 | archiving, monetary_theory, central_administration | OK — universal for organized states |
| oratory_2 | urban_planning, standardised_writing, chancery_diplomatics | OK |
| oratory_3 | clearing_houses | GBR/NED only (informal goldsmith-banker clearing by the 1760s in London; Amsterdam's Wisselbank sophistication) — NOT France (no functioning central financial institution; see oratory_4) or the rest of Bloc A. DATING CAVEAT (2026-08-26): the London clearing house is only loosely sourced to a 1750-1770 window (Ingram 1911), which straddles 1763 — treat this as a genuinely borderline grant, not a firmly-pre-1763 one; it survives on the informal-practice reading, not a hard date. |
| oratory_4 | central_banking, insurance_agencies, public_debt_administration | GBR/NED ONLY (Bank of England 1694, Amsterdam Wisselbank 1609). NOT France — Banque Royale collapsed 1720, no French central bank until 1800 — and NOT the rest of Bloc A. Tag-scoped carve-out, never a whole-bloc grant. |
| civic_1 | metalworking, construction | OK — universal |
| civic_2 | artificial_canals, gear_systems, templating, mining_rails | OK — all pre-industrial |
| civic_3 | spinning_frame, threshing_machine | **ANACHRONISTIC for all** (1769/1786) |
| civic_4-6 | manufactories, blast_furnace, electricity, engine, telegraph | **ANACHRONISTIC for all** |
| religious_1 | education, art_history, astronomy | OK |
| religious_2 | national_epic, theatre | OK |
| religious_3 | scientific_method, secular_sciences, neoclassicism, astronomy **+** astrophysics, absorption_spectroscopy | MIXED — first group OK for Enlightenment Europe, last two 19th-century |

Individual GBR/FRA grants (all ungated today) — from the fork audit:

| tech | real date | verdict |
|---|---|---|
| rotative_beam_engine | 1781-83 | anachronistic ~2 decades |
| cotton_gin | 1793 | anachronistic ~3 decades |
| double_acting_cylinders | 1782 | anachronistic ~2 decades |
| experimental_railway | 1804+ | anachronistic ~4-6 decades |
| steam_locomotive | 1804-29 | anachronistic ~4-6 decades |
| rack_railway | 1812+ | anachronistic ~5-12 decades |
| rocket_artillery (Congreve, Western) | 1804-07 | anachronistic ~4 decades for Western recipients |
| torpedoes (Whitehead) | 1866 | anachronistic ~10 decades |
| steam_powered_ships | 1783-1840s | anachronistic ~2-8 decades |
| scientific_revolution | name: ~1550-1700 | name OK; EFFECT unknown — flag to verify it isn't a late-industrial payload |

Verdict: **all GBR + FRA/NED/USA/German individual grants are anachronistic for 1763** and
should be removed from the 1763 branch (already done in the first-pass fix — this confirms it).

## Per-bloc recommendation for the 1763 branch

Tiers are the ceiling; where a tier is MIXED, see the exclusion note.

**Bloc A — Western/Central Europe** (french/british/spanish/portuguese/latino/german/
scandinavian/italian/mediterranean_romance/hungarian/north_ugric/baltic/dutch/north_american):
- Military: level 0-2 whole + the 9-item SYW subset macro (`TECH_unlock_military_1763_syw`) —
  never the whole military_3 tier.
- Oratory: **level 1-2 only for the whole bloc.** Oratory 3-4 (clearing houses, central
  banking) is a SEPARATE tag-scoped carve-out for GBR + NED only — not a bloc-wide grant.
- Civic: **level 1-2** (hard stop — civic_3 is the Industrial-Revolution line).
- Religious: level 1-2 whole + the 3-item Enlightenment subset macro
  (`TECH_unlock_religious_1763_enlightenment`: scientific_method, secular_sciences,
  neoclassicism) — never the whole religious_3 tier.
- Justification: most developed 1763 economies; Scientific Revolution complete, Enlightenment
  at its peak, mature fiscal-military states — but pre-industrial, and financially advanced
  only in the two countries that actually had the institutions.

**Bloc B — Slavic** (south/west/east_slavic — Russia, Poland, Balkans):
- Military: level 0-2 whole + the same SYW subset macro (Russia fought the Seven Years' War
  with comparable European arms; the bloc also covers Ottoman-subject Balkan Slavs, but level
  2 + the SYW subset is the safe common denominator either way).
- Oratory: **level 1-2** (post-Petrine Russia had central administration; central banking
  [oratory 3-4] is not extended to this bloc — no carve-out, unlike GBR/NED).
- Civic: **level 1-2.**
- Religious: level 1-2 whole + the same Enlightenment subset macro (Catherine the Great's
  Russia was deeply Enlightenment-engaged — Voltaire/Diderot correspondence, the 1767
  Nakaz — scientific_method/secular_sciences/neoclassicism are defensible here too).

**Bloc C — South/Southeast Asia + East-Asian periphery** (Indian-subcontinent groups,
dravidian, burmic, tai, vietic, malaysian, gurkani [Mughal], indo-himalayan, bodish
[Tibet], koreanic, japanese_group):
- Military: level 0-2 (organized gunpowder states — Mughal/Ottoman-adjacent artillery
  traditions, Japanese matchlock/cannon tradition, Korean cannon — bombard_cannons/warships
  are a reasonable, not a stretch. **Upgrade from the current branch's level 0-1** — no
  Napoleonic-era items are involved, so no subset macro needed here).
- Oratory: level 1-2 (sophisticated bureaucracies — Mughal, Joseon, Tokugawa administration —
  urban planning/standardized writing/chancery-diplomatics are all plausible.
  **Upgrade from the current branch's level 1 only.** No oratory 3-4 carve-out — that stays
  GBR/NED-only.)
- Civic: level 1-2 (**already correct in the current branch — no change**).
- Religious: level 1 only (literate, but the level-2/3 items — national epic/theatre/secular
  science — are Euro-centric framings; level 1 education/astronomy/art_history fits best.
  **Already correct in the current branch — no change**).
- Note: no individual rocket_artillery grant for this bloc. Mysorean iron-cased war rockets
  were fielded effectively in the 1780s-90s (Hyder Ali / Tipu Sultan; source-checked against
  en.wikipedia.org/wiki/Mysorean_rockets — the earlier "~1750s-60s" figure in a prior draft
  was wrong, real dating is later), so they are post-1763 AND Mysore-specific (one tag) —
  doubly not defensible as a whole-bloc 1763 grant. Left out.

**Bloc D — Islamic / Middle East / East Mediterranean** (west_turkic [Ottoman], arabic
groups, albanian, greek, armenian, romanian, iranian groups, dagestani, central_aryan):
- Military: level 0-2 + **mortar and wheeled_cannons only** as individual grants (dropped
  BOTH naval_explosives and carronade — naval_explosives for the same cross-bloc consistency
  reason as Bloc A/B above, carronade because 1778 is unambiguously post-1763).
- Oratory: level 1-2 (**already correct in the current branch — no change**).
- Civic: level 1-2 (**already correct in the current branch — no change; the "currently
  level 3" claim in an earlier draft of this doc was wrong, sourced from the frozen 1815
  branch by mistake**).
- Religious: level 1-2 (**already correct — no change**).
- Justification: Ottoman Empire still a great power in 1763 but militarily lagging Europe
  post-Karlowitz (1699); Zand Persia recovering. Solid gunpowder-empire tier, not industrial.

**Bloc E — the true gap: Native American + every other culture group matching no OR-list**
(NOT Sub-Saharan Africa as a whole — the tradezone-based grant already reaches any capital in
`west_africa_tradezone`/`east_africa_tradezone`, which already covers Ethiopia/Horn-of-Africa
and the Sahel in both branches. The genuine gap is Native American groups plus ~10 more the
review found matching nothing at all: mongolic, kartvelian, siberian_turkic, east_turkic,
non-CHI chinese_group/jurchen, malagasy, swahili_group, berber, and Southern African Bantu
groups — the last of these ARE geographically reachable via `southern_africa_tradezone`, which
exists in the trigger file but was never referenced here):
- Fix 1: **add `southern_africa_tradezone` to the existing tradezone geography OR-list**
  (`west_africa_tradezone`/`east_africa_tradezone`/`middle_east_tradezone`/
  `india_tradezone`/`south_east_asia_tradezone`) — same grant (weapon_manufacturing, firearms,
  civic_level_1), same idiom, zero new logic, closes the Southern African Bantu gap.
- Fix 2: **a marker-variable catch-all**, not a hand-enumerated culture-group list (the
  hand-enumeration approach is exactly what produced this gap — the original file's OR-lists
  are already an incomplete hand-enumeration, and a revised one would just be a differently
  incomplete hand-enumeration). Each `every_country`/`c:` block in the 1763 branch sets a
  scratch flag (e.g. `TECH_1763_seeded`) on every country it grants to; one final block at the
  end of the branch grants military_level_0 + civic_level_1 to any country that never got the
  flag set. This is provably complete by construction — nothing can fall through, regardless
  of what culture groups exist in the mod now or are added later.
- Justification for the floor itself (military_0 + civic_1, nothing more): firearms reached
  eastern-woodland Native American polities via centuries of fur-trade gun commerce — well
  evidenced, and Pontiac's War is literally happening in 1763 — and basic
  metalworking/construction is universal. No oratory/religious grant — not evidenced broadly
  enough across this residual catch-all to justify.

## Implementation approach (the macro-granularity fix)

The blocker: tech LEVEL macros are all-or-nothing, and two tiers (military_3, religious_3)
have period-OK content mixed with anachronistic content that Europe (and, for religious_3,
also the Slavic bloc) should get the good half of. A third tier, oratory_4 (plus oratory_3),
is not mixed-content but mixed-COUNTRY — the content is fine, but only 2 of Bloc A's 17
culture groups actually qualify.

Three new 1763-only constructs in `se_TEST.txt`, none touching the frozen 1815 branch:
- `TECH_unlock_military_1763_syw` — the 9-item Seven-Years'-War-safe subset of military_3
  (sword_bayonet, mortar, wheeled_cannons, limber, howitzer, multiple_deck_warships,
  regimental_structure, specialised_corps, cartography). Granted to Bloc A and Bloc B.
- `TECH_unlock_religious_1763_enlightenment` — the 3-item Enlightenment subset of religious_3
  (scientific_method, secular_sciences, neoclassicism). Granted to Bloc A and Bloc B.
- A `tag = GBR` OR `tag = NED` carve-out (mirrors the existing `c:GBR` tag-scoped pattern
  already in the file) granting oratory_level_3 + oratory_level_4 whole — the two are small
  enough tiers that no subset macro is needed, just a narrower country list.

Everything else the blocs get is whole safe tiers (military 0-2, oratory 1-2, civic 1-2,
religious 1-2) via the existing per-tier macros, unchanged. The marker-variable catch-all
(Bloc E fix 2) is new control flow but not a new macro — it reuses `TECH_unlock_military_level_0`
and `TECH_unlock_civic_level_1`.

## Resolved (former open questions)

1. **Bloc E scope addition** — RESOLVED via the marker-variable catch-all (provably complete,
   no hand-picked list to get wrong).
2. **Russia vs Balkan Slavs** — RESOLVED: kept the bloc uniform (level 0-2 + SYW subset for
   everyone in it) — simpler, and the SYW subset's content is safe for the whole bloc anyway.
3. **Mysore rocket_artillery** — RESOLVED: left out of Bloc C. One tag, right at the edge,
   not worth a one-off carve-out.
4. **scientific_revolution effect** — still open, low priority (CHI gets it in neither branch,
   so it doesn't block this implementation). Worth a follow-up look at its actual modifier.
5. **carronade in Bloc D** — RESOLVED: dropped (1778, unambiguously post-1763).
