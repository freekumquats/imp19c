# Overnight Technology Rework — decisions log

**Goal (user):** the technology trees have not been adjusted from their 1815 start date. Assess the current
in-game representation, assess the historical academic state of technology in 1763, and adjust the in-game
trees to match a 1763 baseline. Add Qing-specific technology (mirror Invictus / Terra Indomita templates for
country-specific tech). Also use vanilla's **culture-based** and **integration-based** invention mechanics —
the Qing has many cultures and many subjects, so there is rich room for Qing-specific features there.

**Then (queued):** Military Traditions — same approach (research in-game + historical ca.1763, adjust to match).

**Working mode:** fully autonomous, no deferring hard parts, no questions. Every decision logged here.
Branch merge-overnight, commits freekumquats. Phased: research → design doc → review doc → implement →
review implementation → commit → push.

---

## PHASE 1 — RESEARCH (in flight)

Four parallel research agents dispatched 2026-07-25:
- **1a in-game map**: current invention system structure + the anachronism audit (what's reachable too early
  for 1763) + gating mechanics + starting tech (oa_starting_techs.txt) + existing tag-gated inventions.
- **1b historical 1763**: academic state of tech c.1763 globally + Qing-specific; the "1763 ceiling" list of
  techs that should NOT be near-start (steam loco, rail, telegraph, percussion cap, rifled musket, ironclad…).
- **1c oracle country-specific templates**: how Invictus + TI implement tag/culture-gated inventions (exact
  schema + complete quoted examples) + invention loc convention + any date/era gating.
- **1d culture + integration tech mechanics**: vanilla/oracle culture-gated + integration-gated invention /
  research / civilization-value mechanics; how subjects + integrated cultures can be read; military_traditions
  as a parallel culture/tag-gated tree. (Qing = many cultures + many subjects → rich Qing-specific vector.)

### Firsthand orientation (my own read, for implementation-readiness)
- Tech system = `common/inventions/{civic,martial,oratory,religious}.txt`, 4 files. Inventions grouped into
  named groups each `= { technology = <X>_tech  color = hsv{...}  <inventions> }`. Each invention:
  `modifier = {}`, `potential = {}` (visibility/availability), `requires = {}` (prereq inventions).
- Gating observed so far is **civilization-value + prerequisite** driven, NOT date-driven (e.g.
  tech_steam_locomotive gates `potential = { country_civilization_value > 45 }`). This is the lever: a 1763
  baseline means raising the civ-value thresholds (and/or adding prereq depth / date gates) on post-1763 tech.
- Starting tech: `common/on_action/technology/oa_starting_techs.txt` (agent 1a reading it fully).
- Defines (common/defines/00_defines.txt): INNOVATIONS_PER_TECHLEVEL 1.0, TECH_ENTRY_YEARS 16,
  MAX_INVENTIONS_SAME_TYPE 3, TECH_AHEAD/BEHIND_OF_TIME -0.12, MAX_INVENTION_TECH_TREE_DEPTH 124.
- `omen_power` in this TC = MINING output (per prior memory), NOT religious omens — inventions use it for
  mining productivity. Keep that in mind for any modifier edits.

### 1b HISTORICAL DIGEST — RECEIVED (research agent, academic history-of-tech)

**1763 = end of Seven Years' War / mid-Qianlong. BEFORE the Industrial Revolution proper (1760s-1830s) and
the 19thC military revolution. The "Napoleonic-industrial" imagery is 1770s-1840s and must be gated out.**

CURRENT/ALLOWED at 1763 (start or near techs): flintlock musket + socket bayonet (standard); smoothbore
muzzle-loading artillery; **Gribeauval artillery system 1765** (borderline — early researchable, NOT start);
Vauban bastion fortification (mature); 74-gun ship of the line, age of sail, **hull coppering (1760s+)**;
Newcomen pumping engine (1712); coke iron (1709, immature); **Bridgewater/canal engineering (1761 — genuine
leading edge)**; Norfolk rotation + selective breeding + enclosure; flying shuttle (1733); **Harrison H4
chronometer (1761) + sextant (1757) — a real 1763-era navigation breakthrough, good to feature**; variolation
(smallpox inoculation, known); Enlightenment/Encyclopédie at high tide; phlogiston chemistry (pre-modern).

**THE 1763 CEILING — gate these OUT (intro dates):** Watt separate-condenser steam (1769/1776) · high-pressure
steam (1800) · steam locomotive (Rocket 1829) · railway network (1825-30) · steamship (1807 / screw 1840s) ·
ironclad (1859-60) · naval shell guns (Paixhans 1822) · factory system / powered textile machinery (jenny
1764, water frame 1769, mule 1779, power loom 1785) · puddled wrought iron at scale (Cort 1783) · percussion
cap (1807/1820s, military 1830s-40s) · rifled musket general issue (Minié 1849, Enfield 1853) · breechloader
rifle (Dreyse 1841) · metallic cartridge / repeaters / revolvers (1836-60s) · rifled/steel breech artillery
(1855-60s) · electric telegraph (1837-44) · voltaic pile / current electricity (1800; Ørsted 1820, Faraday
1831) · modern chemistry / oxygen theory (1774-89) · cowpox vaccination (Jenner 1796) · anesthesia/antisepsis/
germ theory (1846-80s).

**QING c.1763 — LED / distinctive (candidate Qing-specific tech nodes):**
- 景德鎮 Jingdezhen imperial porcelain kilns (world's premier ceramic industry, proto-industrial, huge export)
- 絲綢 sericulture / imperial silk workshops (Jiangnan — Suzhou/Hangzhou/Nanjing)
- 茶 tea cultivation & processing + the 廣州十三行 Canton System trade node (sole global tea source)
- 大運河 Grand Canal / 漕運 grain transport / 河工 Yellow-River conservancy — the most sophisticated state
  hydraulic engineering on earth
- 雕版 woodblock printing + 四庫全書 state scholarly compilation (launched 1772)
- 算學 / 欽天監 court mathematics & astronomy (Jesuit-transmitted, stayed court-bound — a "learning" node)
- 八旗 Eight Banners military-organizational system
- Columbian crops (maize/sweet potato/peanut) + intensive wet-rice = the population-boom agronomy node
- 中醫 / variolation traditional medicine node

**QING c.1763 — LAGGED Europe (design implication: Qing starts BEHIND in these, catches up via Self-
Strengthening arc which already exists):** firearms still largely matchlock (no flintlock drill reform);
NO blue-water navy (post-1433 Ming-voyage end + 海禁 sea-ban legacy — ties to the BT-M Treasure Fleet revival
+ Lift-the-Sea-Ban decision candidate); no mechanization/factory move; no experimental-science institutions.

---

## PHASE 2 — DESIGN (drafting after remaining agents 1a/1c/1d report)

Preliminary design direction (from 1b + firsthand read):
1. **Anachronism gating**: the trees gate on `country_civilization_value` thresholds, not dates. To impose a
   1763 baseline, RAISE the civ-value thresholds on the ~20 ceiling techs so they're unreachable near start,
   ordered by their historical intro date (steam→rail→telegraph→rifling etc. progressively higher). Possibly
   add date gates where the engine supports `current_date` in an invention potential (agent 1c checking).
2. **Feature the 1763-current leading edge** as reachable/near-start: Gribeauval artillery, canal engineering,
   Harrison chronometer/sextant navigation, Norfolk agriculture, hull coppering, socket-bayonet drill.
3. **Qing-specific tech** (tag=CHI + culture/integration gated, per agents 1c/1d): the 9 distinctive nodes
   above — porcelain/silk/tea/canal-hydraulics/woodblock/court-math/banners/Columbian-crops/variolation —
   as a Qing invention group (or tag-gated inventions), Qing starting AHEAD in these but BEHIND in
   firearms/navy/mechanization.
4. **Culture + integration vector** (Qing has many cultures + subjects): per agent 1d findings — culture-gated
   bonuses / integration-scaled research, so the multi-cultural multi-subject empire is a tech lever.

### 1a IN-GAME MAP — RECEIVED (research agent)

**184 inventions, 4 categories, 12 groups, ~1943 lines:**
- **civic** (00_civic_inventions.txt, 61 inv): `railway_tech_1` (mining rails→steam rail→electrified/tram),
  `medical_and_chemistry_tech` (clinical→germ theory→vaccines + canning/pasteurization),
  `civic_tech_manufacturing` (metalworking→steam engine→electricity→telegraph).
- **martial** (00_martial_inventions.txt, 71 inv): `military_tech_culture` (standing army→Napoleonic→WWI
  trench/storm troopers), `military_tech_firearms` (matchlock→rifling→percussion→breechloader→bolt-action→
  SMG), `military_tech_vehicles` (sail warships→copper plating→steam ships→torpedoes),
  `military_tech_artillery` (cannon→wheeled/limber→howitzer→quick-firing).
- **oratory** (00_oratory_inventions.txt, 30 inv): `monetary_tech_1` (archiving→central banking→exchange
  rates), `writing_and_society_1` (admin→typewriter→photography).
- **religious** (00_religious_inventions.txt, 22 inv): `education_tech` (education→scientific method/
  revolution→psychology/historicism), `arts_tech` (art history→neoclassicism→romanticism/museums),
  `physics_tech` (astronomy→spectroscopy→molecular physics→geology).

**★ KEY DISCOVERY — date-gating an invention IS PROVEN:** the ONLY date gate in the whole system today is
`tech_bottling_and_canning` (00_civic_inventions.txt:345) with `current_date > 1820` in its potential. So
`current_date > YYYY` inside an invention `potential = {}` is a working engine idiom → **date-gating is the
clean lever for the 1763 baseline** (far simpler + more historically precise than re-tuning civ-value across
184 inventions). All 183 other inventions gate purely on civ-value + prereqs → post-1763 tech is reachable
~50 years early (steam ~1770s, rail civ>45, electricity, percussion rifles by ~1810-30, MGs by ~1840-60,
WWI tech by ~1880-1900).

**oa_starting_techs.txt is EMPTY (0 bytes)** — no scripted starting tech; all countries start tech-0. CHI
setup carries no invention grants. **No country-specific/tag-gated inventions exist today** (clean slate for
Qing tech). Soft numeric gates exist on 4 firearms (military_tech>=25/30, >15).

**DESIGN LEVER CONFIRMED:** add `current_date > YYYY` gates (historical intro date, from 1b's ceiling list)
to the post-1763 inventions. This is the primary mechanism. Optionally raise civ-value on the worst offenders
as belt-and-suspenders, but date gates are the precise tool.

### 1c ORACLE COUNTRY-SPECIFIC TEMPLATES — RECEIVED (Invictus + TI)

**★ Country-specificity goes in `allow = {}`, NOT `potential`.** (`potential` = player-vs-AI / mutual-
exclusion / conditional visibility.) Proven gate forms:
- `allow = { tag = CAR }` — hard tag-only (Invictus punic_principles_inv).
- `allow = { OR = { current_ruler = { has_trait = maurya }  tag = BHA } }` — tag OR trait (TI).
- `allow = { primary_culture = athenian }` — single-culture (Invictus alarm_clock_inv).
- `allow = { OR = { country_culture_group = hellenic  custom_tooltip = { text = integrated_any_hellenic_culture  has_variable = greek_science  any_integrated_culture = { is_greek_culture_group_trigger = yes } } } }`
  — **THE INTEGRATION IDIOM**: culture-group OR (a science-flag + any_integrated_culture of that group).
  This is exactly the Qing-many-cultures/subjects vector (Invictus greek_advanced_mechanics_inv:54-80).
- TI monsoon_navigation_inv:1690 stacks several `country_culture_group` + `any_country_culture { is_integrated
  = yes  this.culture.culture_group = culture_group:X }` branches — a multi-culture unlock.

**Full invention schema:** `modifier={} · requires={one} · requires_or={a b} · allow={} · potential={} ·
on_activate={} (fires once on unlock — can create_unit, run scripted effects, custom_tooltip "unlocks X
building", change_law) · keystone=yes · icon_override=X · ai_will_do={}`.
**Group header** is ONLY `technology = <X>_tech` + `color = hsv{}` — a whole group can't be tag-gated, only
individual inventions (via allow). **Loc:** `localization/english/ecd_inventions_l_english.yml`,
`<inv_name>:0 "Name"` + `<inv_name>_desc:0 "Desc"`.
**Neither oracle date-gates inventions** — but imp19c ITSELF already does (tech_bottling_and_canning
current_date>1820), so date-gating is proven in THIS mod. Use the mod's own idiom.

### 1d CULTURE + INTEGRATION MECHANICS — RECEIVED (Invictus + TI + vanilla)

**★ THE INTEGRATION-SCIENCE SYSTEM (proven, the core Qing vector):** Invictus/TI gate culture-FAMILY
inventions behind a per-family `has_variable = X_science` flag, set PERMANENTLY (`set_variable {name=X_science
days=-1}`) by a **culture decision** that requires you've INTEGRATED a culture of that family (with a pop
threshold). Proven vars: greek_science, latin_science, indian_science, egyptian_science, mesopotamian_science,
persian_science, anatolian_science, arabian_science, etc. The invention `allow` is:
`OR = { country_culture_group = X  custom_tooltip = { text = integrated_any_X_culture  has_variable = X_science
any_integrated_culture = { this.culture.culture_group = culture_group:X } } }`.
→ **QING PLAN: mint manchu/mongol/tibetan/uyghur/han(_science) flags via integration decisions, gate Qing
culture-family inventions behind them.** Qing's many cultures+subjects = many unlockable branches.

**Research-modifier keys (proven valid):** `research_points_modifier` (% research), `country_civilization_
value` (flat), `global_monthly_civilization` (monthly tick), `local_research_points_modifier` /
`local_country_civilization_value` / `local_monthly_civilization` (province), `technology_investment`
(cheaper investment), `max_research_efficiency`. NO invention_cost/slot key exists.

**Cultures themselves carry NO modifier block** — bonuses flow through integration-unlocked inventions, not
culture defs. **Integrated-culture-pop COUNT is readable** in a script_value: `every_country_culture = {
limit = { is_integrated = yes }  add = country_culture_pop_count }` → a dynamic research bonus scaling with
how many cultures the Qing has integrated (cap it). **Subjects are NOT readable in an invention allow** (no
num_of_subjects gate proven) — but a country VARIABLE tracking subject count (set via on_action) CAN be read
in `allow` (`has_variable + var:X >= N`) — that's how a tributary-count-gated Qing invention would work.

**Military traditions = a parallel culture-gated tree** (common/military_traditions/): tree `allow` gates on
`country_culture_group` / `primary_culture` / `has_variable = X_influence`; laws can gate on
`any_integrated_culture = { is_culture = scythian }` to unlock culture-specific unit bonuses. → the Phase-6
Qing tradition trees (banner/Mongol/Green-Standard/frontier) use this exact idiom.

---

# PHASE 2 — DESIGN (LOCKED)


### MARTIAL requires-graph — the TWO independent roots (verified 2026-07-25)
The modern-firearms tree has TWO roots that must BOTH be gated (one does not feed the other):
1. **tech_guncotton:226** (requires tech_firearms) — seals the explosives spine: nitroglycerin -> smokeless_powder
   -> percussion_cap -> bullet_innovation -> early/improved_cartridges -> breechloader -> minie_ball -> pinfire_primer
   -> experimental_revolver -> hand_cranked_MG / standard_revolver -> late_small_arms -> bolt_action -> recoil_MG ->
   rifle/frag grenades. Gate >1846.
2. **tech_rifling_standardisation:240** (requires replaceable_weapon_parts + rifles — INDEPENDENT of guncotton) —
   the general-issue rifled musket. Gate >1849 (Minie). NOTE percussion_cap requires BOTH rifling_standardisation
   AND smokeless_powder, so it is double-sealed.
NAVAL: tech_steam_powered_ships:577 requires copper_plating + `potential = { invention = tech_reciprocating_engine }`
-> ALREADY sealed once the Watt engine is civic-date-gated (>1769); add explicit >1807 floor for tooltip clarity.
tech_torpedoes:611 requires naval_explosives + rocket_artillery -> gate >1866. Copper_plating/warships/round-bow =
1760s age-of-sail, LEAVE UNGATED. Explicit iconic-leaf floors (breechloader >1841, minie_ball >1849, hand_cranked_MG
>1862, bolt_action >1880, recoil_MG >1884) added for tooltip precision even though inherited-sealed.

## Part A — 1763 anachronism gating (date-gate the ceiling)
Use the mod's OWN proven idiom (`current_date > YYYY` bare in `potential = {}`, per tech_bottling_and_canning
:345). Add a date floor to each post-1763 ceiling invention = its historical intro year (from 1b), so the
tech is invisible/unavailable until then. This preserves the civ-value + prereq race WITHIN each era but
stops a fast researcher reaching steam/rail/telegraph/rifling in the 1770s. Belt-and-suspenders: leave the
existing civ-value gates as-is (they still pace within an era).

**Date floors (invention → current_date > YEAR), by file:line:**
- CIVIC (00_civic_inventions.txt): tech_spinning_frame:464 >1764 · tech_threshing_machine:474 >1784 ·
  tech_reciprocating_engine:632 (Watt) >1769 · tech_cotton_gin:651 >1793 · tech_experimental_railway:23 >1804
  · tech_steam_locomotive:44 >1825 · tech_passenger_railway:78 >1830 · tech_electrified_railway:115 >1879 ·
  tech_electricity:568 >1800 · tech_experimental_telegraph:576 >1837 · tech_voltaic_pile:585 >1800 ·
  tech_electromagnet:602 >1825 · tech_magnetic_telegraph:610 >1844 · tech_organometallic_compounds:558 >1800
  · tech_epidemiology:241 >1800 · tech_germ_theory:263 >1861 · tech_antiseptic_principle:271 >1867 ·
  tech_cholera_vaccines:279 >1885 · tech_pasteurization:391 >1862. (canning:345 already >1820.)
- MARTIAL (00_martial_inventions.txt): tech_guncotton:226 >1846 · tech_nitroglycerin:233 >1847 ·
  tech_rifling_standardisation:240 >1849 · tech_smokeless_powder:263 >1884 · tech_percussion_cap_ignition:272
  >1820 · tech_bullet_innovation:284 >1826 · tech_breechloader:310 >1841 · tech_minie_ball:318 >1849 ·
  tech_dynamite:328 >1867 · tech_hand_cranked_machine_guns:354 >1862 · tech_bolt_action_rifle:385 >1880 ·
  tech_recoil_powered_machine_guns:393 >1884 · tech_quick_firing_gun:733 >1897 · tech_steam_powered_ships:577
  >1807 · tech_torpedoes:611 >1866. (+ the WWI culture techs trench/storm/camouflage >1914, and grenade
  chain >1914; MG/SMG chain by prereq once bolt-action is date-gated.)
- Gribeauval-class artillery reforms: allow the wheeled-cannon/limber/howitzer line (1763-current); no floor.
- NAVAL: leave sail/copper-plating (1760s) ungated; date-gate steam ships (1807) + torpedoes (1866).
- Approach: I'll date-gate the ROOT of each anachronistic chain; downstream techs inherit the block via their
  `requires`. This minimizes edits while sealing whole eras (e.g. gating tech_reciprocating_engine seals the
  Watt-steam→rail→steamship branches; gating tech_electricity seals the whole electricity→telegraph branch).

### VERIFIED requires-graphs (firsthand read, 2026-07-25) — precise ROOT gates
**CIVIC** (00_civic_inventions.txt): the industrial spine roots at **tech_organometallic_compounds:558**
(requires tech_bloomery) → **tech_electricity:568** (whole electricity→telegraph→voltaic→electromagnet→magnetic-
telegraph branch) + **tech_reciprocating_engine:632** (Watt; → rotative-beam/cotton-gin/double-acting/grasshopper
+ blast_furnace:623). **tech_experimental_railway:23** gates `potential = { invention = tech_reciprocating_engine }`
so the whole railway group is ALREADY downstream of the Watt engine — gating tech_reciprocating_engine (>1769)
seals rail too. But add explicit floors on the ICONIC leaves where the intra-chain date gap is large:
tech_electricity >1800, tech_experimental_telegraph >1837, tech_magnetic_telegraph >1844, tech_steam_locomotive
>1825, tech_passenger_railway >1830, tech_electrified_railway >1879. Medical spine: tech_epidemiology:241 >1800
(→ germ_theory/antiseptic/vaccines downstream), + explicit tech_germ_theory >1861. Agronomy: tech_spinning_frame
:464 >1764, tech_cotton_gin:651 >1793 (also requires reciprocating_engine so double-sealed).
**MARTIAL** (00_martial_inventions.txt): firearms spine — start techs tech_weapon_manufacturing:165 /
tech_firearms:174 / tech_rifles:186 / tech_sword_bayonet:213 are 1763-APPROPRIATE (flintlock musket + socket/
sword bayonet — LEAVE UNGATED). Explosives/rifling roots: **tech_guncotton:226** (requires tech_firearms) >1846
→ tech_nitroglycerin:233 >1847 → tech_smokeless_powder:263 / **tech_rifling_standardisation:240** >1849 (requires
replaceable_parts+rifles). NOTE the existing tree mis-orders history: tech_percussion_cap_ignition:272 requires
rifling_standardisation + smokeless_powder, so percussion (hist. 1820s) sits BEHIND 1847 nitroglycerin — an
existing quirk; I gate percussion >1820 anyway for correctness but it's already sealed by its requires. Downstream
bullet_innovation:284→early/improved_cartridges + breechloader:310 + minie_ball:318 inherit; add explicit
tech_breechloader >1841, tech_minie_ball >1849. MG chain: tech_hand_cranked_machine_guns:354 >1862, tech_bolt_
action_rifle:385 >1880, tech_recoil_powered_machine_guns:393 >1884. Naval: tech_steam_powered_ships:577 >1807,
tech_torpedoes:611 >1866. Artillery: tech_quick_firing_gun:733 >1897 (requires breechloader+smokeless, sealed).
→ Gate the ROOTS (guncotton, rifling_standardisation, steam_ships, MG-cranked, organometallic OR electricity/
reciprocating) + explicit floors on the named iconic leaves for tooltip precision. **PENDING review agent's
requires-graph audit before I commit the exact leaf set.**

## Part A (cont.) — ORATORY + RELIGIOUS anachronisms (verified 2026-07-25)
These files hold softer anachronisms (research-investment bonuses, comms tech) but still 19thC — gate for a
consistent 1763 baseline:
- ORATORY (00_oratory_inventions.txt): photography chain roots at **tech_heliography:244** (requires central_
  administration; Niepce 1826) -> monochrome_processes -> daguerreotype (1839; also potential invention=tech_
  electricity, double-sealed) -> survey_photography / magic_lanterns. Gate tech_heliography >1826. Typewriter:
  **tech_prototype_typewriter:236** >1868 (-> commercial_typewriter, which also potential invention=tech_
  electricity). tech_railway_post_office:98 potential invention=tech_steam_locomotive -> already sealed. The
  monetary/postal/census/banking spine (central_archiving/monetary_theory/postal/central_banking) is 18thC-
  plausible (double-entry, national banks, census, penny-post ~1840 borderline) — LEAVE the core ungated;
  optionally floor tech_central_banking's late children if they read too modern (defer — not anachronistic
  enough to matter at 1763 reachability).
- RELIGIOUS (00_religious_inventions.txt): physics chain astronomy/astrophysics = Newtonian, 1763-fine; gate
  **tech_absorption_spectroscopy:203** >1859 (Kirchhoff-Bunsen; root of spectroscopy->molecular_physics->
  geology). Education chain: scientific_method/scientific_revolution/scientific_journals = 17thC, fine; gate
  **tech_anthropology:48** >1800 (root of anthropology->psychology/historiography->historicism), + explicit
  tech_psychology >1879, tech_historicism >1830. tech_secular_sciences (enables secularism state religion) is a
  19thC concept -> gate >1789 (post-French-Revolution secularization) as the earliest defensible floor.

## Part B — Qing-specific technology (tag=CHI + integration-science)
New invention group **`qing_inventions` (civic_tech)** in a new file common/inventions/00_qing_inventions.txt,
individual inventions `allow`-gated `tag = CHI` (+ some integration-science gated). The 9 distinctive 1763
Qing nodes from 1b, each granting a fitting proven modifier + a keystone flavour:
- 景德鎮御窯 Imperial Kilns (porcelain) — global_commerce_modifier + a trade-goods output.
- 江南織造 Imperial Silk Works — commerce + citizen output.
- 茶政 Tea Administration (+ Canton trade) — commerce + tariff/tax.
- 河工 River Conservancy / 大運河 Grand Canal hydraulics — supply-limit + build cost (canals).
- 四庫全書/雕版 Woodblock Compilation — research_points_modifier + civilization (learning).
- 欽天監 Court Mathematics & Astronomy — research_points_modifier + max_research_efficiency (Jesuit math).
- 八旗 Banner System — a martial-flavoured national mod (recruit/morale) — martial-tech invention.
- 番薯玉米 Columbian-Crop Diffusion — population growth/food (the pop-boom agronomy).
- 種痘 Variolation — a health/population mod.
INTEGRATION-SCIENCE branch (Qing's many cultures): manchu_science / mongol_science / tibetan_science /
uyghur_science / han_science flags (set by integration decisions in Part D), each unlocking a culture-family
Qing invention (banner cavalry / steppe horse / Tibetan highland admin / Xinjiang oasis / Confucian
bureaucracy). This is the "lots of Qing-specific features via cultures + subjects" the user asked for.

## Part C — Hanlin Academy research mechanics (Phase 4c)
The 翰林院 Hanlin panel (gui/qing_hanlin.gui + QING_hanlin_panel.txt) currently a char roster that already folds
into the Grand Secretary's standing (qing_min_perf_grand_secretariat). Expand: the Hanlin scholars' summed
literary skill drives a standing research bonus — a country modifier (research_points_modifier + max_research_
efficiency + global_monthly_civilization) banded to corps depth, recomputed in a pulse from the researcher
characters. Ties the roster to vanilla research points/progress/efficiency + researcher characters (the user's ask).
**PROVEN IDIOM — mirror the Southern-Study `luster` (se_QING_SOUTHERNSTUDY.txt):** a QING_hanlin_apply_luster-
style effect that (1) removes both tier modifiers, (2) re-adds one tier based on summed literary depth bands
(major >= 45, minor >= 20, none below). This is remove-then-add tier-swap → NO restoring-drift ratchet, NO
0..100 meter. Define qing_hanlin_luster_minor/major modifiers in common/modifiers/ with the research keys. The
recompute runs in the EXISTING roster pulse (a plain governance pulse, not a compiled GUI button) — safe from
the scripted-gui compile-recursion class. **Existing research-bonus modifiers to check for duplication:** the
Self-Strengthening + Wenzhi + Southern-Study systems already grant civilization/research nudges — the Hanlin
luster must be additive-and-distinct (a scholarship channel), not a re-skin. Verify keys don't stack to absurd
totals with those (band the Hanlin tiers modestly, e.g. research_points_modifier 0.05/0.10).

## Part D — integration decisions (the X_science unlocks)
culture_decisions/ file: per-family "patronize/integrate the X scholars" decisions, gated on an integrated
culture of that family (proven Invictus decision idiom), setting the permanent X_science var. These arm the
Part-B integration-science inventions.

## Part E — Phase 6 (queued, after tech): Military Traditions
Adjust existing trees to 1763 + add Qing culture/subject tradition trees (banner 八旗 / Mongol cavalry /
Green-Standard 綠營 / frontier-Xinjiang / tributary-levy), each `allow`-gated on tag/culture/integration.
Existing Qing-relevant trees: 00_manchu.txt (Ten Great Campaigns 十全武功, jurchen-gated, began_with_tradition_
group idiom) + 00_napoleon.txt. The 1763-adjust pass: the vanilla trees are era-agnostic (culture-flavour, not
dated) so little to gate; the work is the NEW Qing trees. Add:
- **八旗 Eight Banners** (jurchen/manchu gated) — the banner garrison system: cavalry/discipline/loyalty.
- **綠營 Green Standard Army** (han-culture/integrated-han gated) — Han provincial infantry: manpower, garrison,
  fort defence, cheap maintenance.
- **蒙古騎兵 Mongol Banner Cavalry** (mongol integrated-culture gated) — light horse, steppe/plains, raiding.
- **藩部邊防 Frontier Defence** (tibetan/uyghur integrated OR has a frontier var) — highland/desert combat,
  supply-over-distance, the Xinjiang/Tibet garrison idiom.
- **朝貢徵調 Tributary Levy** (gated on a subject/tributary-count var, set via on_action) — allied/subject troop
  bonuses, war-score, morale from the tributary system.
Each uses the manchu_shiquan `allow` idiom (culture-group + custom_tooltip began_with_tradition_group), plus the
integration branch reads has_variable=X_science / X_influence where cultures are integrated not owned.

## Part F — Legion Distinctions (Phase 4d) — IDIOM CONFIRMED
common/legion_distinctions/ ships only an empty BOM-only 00_default.txt in the mod (vanilla distinctions were
stripped). **CONFIRMED (research agent, 2026-07-25):** distinction schema is `distinction_X = { icon="phalera_*"
commander={<char mods>}  unit={<unit mods>}  legion={<legion-wide mods, e.g. siege_ability/siege_engineers>} }`.
Distinctions have **NO `allow`/`enable`/`potential`/`trigger`/`country` block — they CANNOT be gated in the
definition.** They are PASSIVE REWARDS granted by the **`add_distinction = distinction_X` effect** from events /
missions / on_actions / unit_abilities (checked with `has_distinction`). There is NO free-pick UI. So Qing
distinctions are DEFINED globally, then GRANTED to Qing legions via a **tag=CHI-gated grant path** — which is
EXACTLY the Ministry-of-War tie-in (Part G): an on_action/event that reads qing_office_war_holder +
qing_min_perf_war and calls add_distinction on eligible legions. **This merges Parts F and G: the distinctions'
Qing-ness AND their Ministry tie live entirely in the grant path, not the definition.**
Plan: a set of 1763-appropriate + Qing distinctions, defined in a new common/legion_distinctions/00_qing_
distinctions.txt (icon = an existing phalera_* so nothing renders blank), e.g.
- 綠營標營 Green-Standard Battalion — garrison/fort defence + cheap upkeep (Han infantry).
- 健銳營 Jianrui (Vanguard) Brigade — the elite storming corps that took the Jinchuan stockades: siege/assault.
- 索倫勁旅 Solon Levies — Manchu-frontier marksmen: skirmish/forest/archer bonuses.
- 火器營 Firearms Brigade — the Beijing artillery/musket division: ranged/artillery bonus (1763-appropriate
  smoothbore/matchlock-flintlock, NOT rifled — historically accurate).
- 藤牌兵 Rattan-Shield Troops — the southern anti-cavalry shield infantry: defensive/light-infantry.
- 駝城 Camel-Fort Artillery — the Zunghar-war mobile camel-mounted swivel guns: desert/mobility.

## Part G — Ministry of War tie-in (both Traditions + Distinctions) — IDIOM CONFIRMED
se_QING_WAR.txt (兵部) runs QING_war_review_commanders (quarterly pulse, reads qing_office_war_holder) +
qing_min_perf_war standing. **CONFIRMED (research agent):**
- **Traditions gate**: a military_tradition tree `allow = {}` CAN read `has_variable` (proven: Invictus
  00_greek_2.txt gates on has_variable=unlock_greek_kingdom_var via trigger_else_if). So the Qing tradition
  trees add a `trigger_else_if { limit = { has_variable = qing_office_war_holder } ... }` branch — the tree
  unlocks for the culture group OR when the 兵部 is staffed. `var:X >= N` value comparison in `allow` is NOT
  proven → do NOT gate a tradition on qing_min_perf_war >= N directly.
- **Distinctions tie (the real mechanism)**: distinctions can't be gated, only GRANTED. The 兵部 quarterly pulse
  (QING_war_review_commanders, which ALREADY reads qing_office_war_holder + can read var:qing_min_perf_war in a
  normal effect trigger — value comparisons ARE legal in effect triggers, just not in tradition `allow`) grants
  the Qing distinctions to eligible legions via add_distinction, banded by qing_min_perf_war: a well-run 兵部
  unlocks the elite distinctions (健銳營/火器營), a bare one only the basic 綠營標營. This is the user's "tied to
  Ministry of War" — the martial standing literally decides which distinctions the army earns.
- **Ministry panel surfacing**: gui/qing_war_ministry.gui gets a read-out of which Qing distinctions are
  currently granted + a button routing to the military-traditions view — folding the martial-tech layer into
  the 兵部 hub, same way the harem folds into the chamberlain. Any button that reaches an iterator MUST
  trampoline through a hidden trigger_event (compile-recursion rule).
- **Feedback**: no new 0..100 meter; the grant/tier logic reads the EXISTING qing_min_perf_war band → no
  restoring-drift ratchet introduced.

## Part H — Heritages + National Ideas for 1763 Qing (Phase 7)
**Heritage.** Heritages (common/heritage/00_mod_heritages.txt) are AUTO-assigned by satisfying `trigger = {}`
(no set_ effect). The Qing today gets **confucian_learning** = `{ technology_investment = -0.3  character_loyalty
= 30 }` — a HEAVY -30% tech-investment penalty (the "Confucian stagnation" trope). For a 1763 baseline this is
defensible as the STARTING drag but should be (a) less crude and (b) escapable via the Self-Strengthening arc.
Plan:
- Refine/replace the Qing's heritage. Option (locked): add a **CHI-specific heritage** (tag/culture-group-gated
  trigger, evaluated before confucian_learning via ordering or a NOT-CHI exclusion on confucian_learning) named
  e.g. **考據學 Evidential Learning / 樸學** — the real 1763 Qianlong-era scholarly movement (Dai Zhen, the 四庫
  全書 project): a MILDER tech penalty + a scholarship/loyalty bonus, reflecting that High-Qing
  learning was rigorous (philology, mathematics, compilation) but inward-turned, not a blanket -0.3 dead weight.
  **CONFIRMED (research agent): research_points_modifier / country_civilization_value / global_monthly_civilization
  / max_research_efficiency ARE ALL valid in a heritage modifier block** (Invictus italiote_heritage, 01_groups,
  00_country_specific). So the CHI heritage is a genuine SCHOLARSHIP heritage: small +research_points_modifier /
  +global_monthly_civilization (rigorous evidential scholarship) BUT a countervailing technology_investment penalty
  (inward-turned, resists applied/foreign tech) + character_loyalty (Confucian cohesion) — net: good at codifying
  what's known, slow to adopt the new. Must EXCLUDE confucian_learning from CHI (add NOT={tag=CHI} to its trigger,
  or make the CHI heritage's trigger more specific + ordered first) so they don't double-stack. Assignment = trigger
  auto-apply (set_country_heritage exists but isn't needed).
**National Ideas.** common/ideas/00_imperatrix_ideas.txt: `idea_X = { trigger={}  <mods>  group=<military|civic|
oratory|religious>_ideas  soundeffect=... }`. **Groups CONFIRMED = exactly 4 (military/civic/oratory/religious).
Tag-gating is NOT in the oracles but IS a proven imp19c-OWN idiom** (idea_gott_mit_uns trigger=tag=PRU, idea_
spanish_revanchism tag=SPA in this mod's 00_imperatrix_ideas.txt) -> use `trigger = { tag = CHI }`. **Idea triggers
CANNOT read has_variable (not proven) -> no Ministry-of-War tie via ideas; ideas are pure tag-gated flavour.** Slot
limit = vanilla-hardcoded 3/group. Add a spread of CHI-gated 1763 Qing national ideas — one per group so the Qing
player has a distinctive pick in each slot:
- MILITARY 八旗勁旅 Banner Host — discipline / land_morale_recovery (the banner martial idea).
- CIVIC 攤丁入畝 Tanding-into-land (攤丁入畝) Land-Tax Reform — tax/pop-growth (the Yongzheng fiscal consolidation, mature by
  1763) — a real economic idea.
- ORATORY 朝貢體系 Tributary System — diplomatic reputation / subject-loyalty / trade (the Canton + tributary
  order).
- RELIGIOUS 敬天法祖 Reverence for Heaven & Ancestors — stability / ruler-popularity / same-religion happiness.
- (optional 2nd civic) 改土歸流 Gaitu-guiliu — integration speed / frontier stability (the SW-China
  bureaucratization of native chieftaincies — ties to the many-cultures theme).
Modifier keys: only those proven in existing ideas (discipline, land_morale_recovery, war_score_cost, plus civic/
oratory keys quoted in 00_imperatrix_ideas.txt). **[PENDING research agent: idea slot limit + full valid group
list + whether idea trigger can read has_variable for a Ministry-of-War tie-in idea.]**

### IMPLEMENTATION ASSETS CONFIRMED (2026-07-25)
- **Invention loc file = `localization/english/technology_l_english.yml`** (NOT ecd_inventions — that doesn't
  exist). Convention: `<key>:0 "Name"` + `<key>_desc:0 ""`. 392 entries; group names too (military_tech etc.).
  New Qing inventions + their _desc go here.
- **Distinction icons = base-game phalera sprites** referenced bare: phalera_tower/archer/horse/swords/eagle/
  helmet/ox/sword_shield/swords_dishonor/skull_dishonor/zeus/amphore/lion (proven by TI 00_default). imp19c is
  an I:R total conversion running on the base game, so these resolve without shipping art. Qing distinctions map
  to fitting ones (火器營->phalera_swords, 綠營->phalera_sword_shield, 索倫->phalera_archer, 駝城->phalera_horse,
  健銳->phalera_tower, 藤牌->phalera_helmet).
- **Invention icons**: existing inventions use NO explicit icon (icon_override is commented out everywhere) —
  the engine auto-derives from the invention key. Qing inventions follow suit (no icon block) to avoid blanks.
- **Military-tradition node images**: manchu tree uses existing arabic_*/indian_* .dds as placeholders (proven
  no-blank pattern). New Qing trees reuse the same placeholder .dds names.

REVIEW GATES for implementation: date-gate a chain's ROOT not every node (inheritance via requires); all Qing
inventions `allow = { tag = CHI }` (not potential); integration idiom exactly per Invictus; research modifier
keys only from the proven list; loc in ecd_inventions_l_english.yml naming; brace/BOM discipline; boot-crash
review (no create_character in inventions; Hanlin pulse iterators run in a plain pulse not a compiled button).
For Parts F/G/H: distinction/heritage/idea/tradition modifier keys ONLY from proven-valid lists (confirmed by
the F/G/H research agent); heritage 1763-CHI must not double-apply with confucian_learning (order or exclude);
Ministry-of-War gates read has_variable/var:X only if the research agent confirms that trigger form is legal in
that context; no restoring-drift ratchet on any Ministry feedback meter; loc for every new heritage/idea/
distinction/tradition; boot-crash review pass over all new files before commit.

---

## SCOPE ADDITIONS (user, 2026-07-25, mid-run) — folded into the doc above
1. "the Hanlin Academy should have expanded mechanics tied to vanilla research mechanics" → **Part C** (Phase 4c).
2. "expand vanilla Distinctions for 1763 and also Qing-specific distinctions" → **Part F** (Phase 4d).
3. "both Military Traditions and Distinctions should be tied to the Ministry of War mechanics" → **Part G**.
4. "define Heritages and National Ideas suitable for 1763 Qing" → **Part H** (Phase 7).
Research agent dispatched 2026-07-25 to confirm the unproven idioms for Parts F/G/H (distinction gating +
grant path; heritage auto-assign + valid modifier keys; idea group list + slot limit + tag-gate; whether
tradition allow / idea trigger can read a country variable for the Ministry-of-War tie-in). Design above is
LOCKED pending that agent's idiom confirmations (marked [PENDING ...] inline).

---

# PHASE 4 — IMPLEMENTATION LOG

## Part A DONE (2026-07-25): 28 date-gates applied (+ the pre-existing canning gate = 29 total)
Applied via a brace-balanced Python injector (merges `current_date > YEAR` into an existing potential block or
creates one; idempotent; preserves existing invention=/military_tech> gates). All four files brace-balanced.
- CIVIC (11): electricity>1800, reciprocating_engine>1769, experimental_telegraph>1837, magnetic_telegraph>1844,
  steam_locomotive>1825, passenger_railway>1830, electrified_railway>1879, epidemiology>1800, germ_theory>1861,
  spinning_frame>1764, cotton_gin>1793. (DROPPED organometallic_compounds — it's the SHARED parent of both the
  electricity AND the Watt-engine branches; gating it would wrongly push the 1769 engine to its year. Left
  ungated so each branch's own floor governs.)
- MARTIAL (10): guncotton>1846, rifling_standardisation>1849, percussion_cap_ignition>1820, breechloader>1841,
  minie_ball>1849, hand_cranked_machine_guns>1862, bolt_action_rifle>1880, recoil_powered_machine_guns>1884,
  steam_powered_ships>1807, torpedoes>1866. (The TWO independent firearms roots — guncotton + rifling_
  standardisation — both gated. Start techs weapon_manufacturing/firearms/rifles/sword_bayonet LEFT UNGATED as
  1763-appropriate flintlock+bayonet.)
- ORATORY (2): heliography>1826 (photography root), prototype_typewriter>1868.
- RELIGIOUS (5): absorption_spectroscopy>1859, anthropology>1800, psychology>1879, historicism>1830,
  secular_sciences>1789.
Torpedoes verified: floor merged ABOVE the existing `military_tech > 15` + `invention = tech_rocket_artillery`
lines, both preserved. steam_locomotive floor merged above the existing `country_civilization_value > 45`.
NOTE: downstream techs inherit the block via `requires` so the whole post-1763 tree is sealed; explicit leaf
floors added only for tooltip precision on the iconic nodes. Loc for gated techs unchanged (names already exist
in technology_l_english.yml). Parts B/C/D/E/F/G/H still to implement.

## Part B DONE (2026-07-25): common/inventions/00_qing_inventions.txt
New civic_tech group `qing_inventions`, 14 inventions, brace-balanced, no BOM, no icon block, no create_character.
- LAYER 1 (9 nodes, allow={tag=CHI}): imperial_kilns, imperial_silk, tea_canton, grand_canal, siku_compilation,
  court_mathematics, eight_banners, columbian_crops, variolation. Modifier keys all validated against existing
  mod usage (commerce/citizen/export/import/supply/build_cost/research_points/civilization/manpower/defensive/
  pop-capacity/food/same-religion-happiness; max_research_efficiency proven in Invictus).
- LAYER 2 (5 integration-science nodes): manchu/han/mongol/tibetan/uyghur_science, each allow=OR{ country_
  culture_group=X  custom_tooltip{ text has_variable=X_science any_integrated_culture{ this.culture.culture_group
  = culture_group:X } } } — EXACT Invictus greek_advanced_mechanics idiom (verified this.culture.culture_group =
  culture_group:X proven in Invictus 00_religious_inventions.txt). Culture groups: jurchen/chinese_group/mongolic/
  bodish/east_turkic (verified in common/cultures/). CHI's own group is jurchen so manchu_science is near-free;
  the rest reward integrating Han/Mongol/Tibetan/Uyghur subjects (the many-cultures/subjects vector).
- LOC: 15 tech names+descs in technology_l_english.yml; 5 qing_integrated_any_*_culture tooltips in interface_l_
  english.yml. The X_science VARIABLES are armed by Part D (culture_decisions/qing_integration_science.txt) —
  until Part D ships, the integration branch unlocks only via country_culture_group (still valid, no crash).

## Part D DONE (2026-07-25): culture_decisions/qing_integration_science.txt
Four integration-science decisions (han/mongol/tibetan/uyghur — NOT manchu, that's CHI's own jurchen group so its
invention unlocks via country_culture_group directly). Each: potential = tag=CHI + NOT has_variable=X_science +
scope:target_culture{ is_integrated=yes  this.culture.culture_group = culture_group:FAMILY }; effect =
pay major_cultural_decision_price + set_variable{ name=X_science days=-1 } (PERMANENT) + stability. ai_will_do=0.
- **BUG CAUGHT + FIXED before commit**: first draft used bare `culture_group = chinese_group` inside
  scope:target_culture (a country_culture scope) — the mod's own boot-fix note (qing_province_reports.txt:236)
  documents that this form FAILS to parse in a culture scope ("Illegal use of operator ="). Corrected all four to
  the proven `this.culture.culture_group = culture_group:X` form (matches the invention allow + 00_language_groups).
- No create_character (TI's version spawns a researcher; deliberately OMITTED — #90 grant-to-fresh-char rule).
- major_cultural_decision_price confirmed to exist (common/prices/00_culture_prices.txt:9). LOC: 4 titles + descs
  + qing_patronize_science_req + 4 unlocked tooltips in qing_nationalism_l_english.yml. Brace-balanced.
Parts A/B/D of the technology phase now DONE. Remaining: Part C (Hanlin), then Phases 6/7 (traditions/distinctions/
Ministry tie / heritage / ideas). Awaiting the adversarial design-review agent before finalising + committing.

## Part C DONE (2026-07-25): Hanlin Academy research mechanics
Extended the EXISTING canonical Hanlin recompute (QING_ministry_recompute_perf_grand_secretariat,
se_QING_MINISTRY.txt) rather than adding a new pulse — so it fires on every roster rebuild (quarterly pulse +
panel open) with zero new wiring and zero compile-recursion risk (it's a plain effect path, not a GUI button).
- The roster loop now also tallies qing_hanlin_literary = summed finesse+charisma of the living Hanlin corps
  (the researcher characters' skill IS the bonus — the user's ask). Set to 0 before the loop, accumulated inside.
- New effect QING_hanlin_apply_research_luster (mirrors QING_southernstudy_apply_luster exactly): remove-then-
  reapply two country-modifier tiers keyed on qing_hanlin_literary — minor >=20, major >=45. Tier-swap => no
  restoring-drift ratchet.
- New modifiers (common/modifiers/qing_hanlin_modifiers.txt): qing_hanlin_research_minor (research_points_
  modifier 0.05 + global_monthly_civilization 0.01), qing_hanlin_research_major (0.10 + 0.02 + max_research_
  efficiency 0.5). Deliberately MODEST + distinct from the Southern-Study (prestige), Wenzhi + Self-Strengthening
  (civilization) channels so research keys don't stack absurdly (the review-gate concern about duplication).
- GUI: added a "Scholarly Depth (學養)" read-out to gui/qing_hanlin.gui (reads qing_hanlin_literary) + loc
  QING_HANLIN_RESEARCH_LABEL/_TT in qing_hanlin_l_english.yml explaining the tiers.
All 5 touched files brace-balanced; var-set-before-read + modifier-name consistency verified. This is the
vanilla-research tie-in the user asked for (points/progress/efficiency + researcher characters), routed through
the Academy that historically DID drive Qing scholarship (the 四庫全書 compilation).

## Part H DONE (2026-07-25): Heritages + National Ideas for 1763 Qing
HERITAGE (common/heritage/00_mod_heritages.txt): added evidential_learning (考據學, trigger=tag=CHI) —
research_points_modifier 0.05 + global_monthly_civilization 0.01 + technology_investment -0.15 + character_
loyalty 20. A subtler read than confucian_learning's flat -0.3: High-Qing scholarship was rigorous (a research
+ civilization bonus) yet inward-turned (a milder tech-investment drag). EXCLUDED CHI from confucian_learning
(added NOT={tag=CHI}) so the two never both match; verified CHI (confucianism/manchu) matches no other heritage.
Placed evidential_learning directly above confucian_learning. LOC: heritage_l_english.yml (name+desc).
NATIONAL IDEAS (common/ideas/00_imperatrix_ideas.txt): 4 CHI-gated ideas, one per group (tag=CHI proven idiom
per idea_gott_mit_uns):
- MILITARY idea_qing_banner_host (八旗勁旅): discipline 0.1 + land_morale_recovery 0.05.
- CIVIC idea_qing_tanding (攤丁入畝): global_tax_modifier 0.1 + global_population_capacity_modifier 0.05.
- ORATORY idea_qing_tributary_system (朝貢體系): diplomatic_reputation 1 + subject_loyalty 0.1.
- RELIGIOUS idea_qing_reverence_heaven (敬天法祖): ruler_popularity_gain 0.1 + happiness_for_same_religion 0.05.
All modifier keys validated as country-scope modifiers (in oracle ideas or mod modifiers). LOC: ideas_I_english.yml
(4 name+desc; banner_host reuses no existing key). Both files brace-balanced, LF. Ideas CANNOT read has_variable
so no Ministry tie here (confirmed) — these are pure tag-gated flavour, as designed.

---

# PHASE 3 REVIEW — RESOLUTIONS (adversarial design-review agent, 2026-07-25)
The review read the files MID-EDIT so some findings were already-addressed; the genuine leaks are now fixed.
- **F1 (oratory/religious ungated)**: ALREADY DONE before review landed — oratory (heliography>1826, prototype_
  typewriter>1868) + religious (absorption_spectroscopy>1859, anthropology>1800, psychology>1879, historicism
  >1830, secular_sciences>1789) were gated. Review saw a stale mid-edit civic/martial-only state. NO further action.
- **F2 (naval_explosives / Paixhans 1822 leak)**: FIXED — added current_date>1822 to tech_naval_explosives
  (seals carronade + confirms torpedoes). REAL leak, now closed.
- **F3 (medical physiology branch: cellular_pathology/medical_imaging)**: FIXED — cellular_pathology>1858,
  medical_imaging>1895. REAL leak, now closed.
- **F4 (over-gate organometallic_compounds)**: ALREADY handled — I DROPPED organometallic from the civic gate
  list during implementation for exactly this reason (it's the shared parent of blast_furnace + the Watt engine).
  reciprocating_engine>1769 + electricity>1800 gate the branches directly; blast_furnace stays ungated. NO action.
- **F5 (heritage selection semantics)**: RESOLVED via the deterministic path the review endorses — shipped
  NOT={tag=CHI} on confucian_learning (not ordering). CHI matches only evidential_learning; verified no other
  heritage trigger matches CHI (confucianism/manchu/imperial_monarchy).
- **F6 (recoil_buffers ~1897)**: FIXED — current_date>1897.
- **F7 (dangling requires typos)**: FIXED the two that my inheritance-sealing depends on: martial
  smokeless_powder->tech_smokeless_powder, civic asprin->tech_asprin. (Both affected roots percussion_cap +
  epidemiology are ALSO directly date-gated, so no actual leak existed, but graph integrity restored.)
- **F8 (research stacking / max_research_efficiency oversized)**: TRIMMED court_mathematics max_research_
  efficiency 0.5->0.25. The technology_investment vs research_points_modifier distinction noted — the heritage
  drag is on investment cost, a separate key; kept the evidential_learning research bonus modest (0.05). Cumulative
  CHI research is intentional (High-Qing scholarship WAS strong) but now bounded.
- **F9 (rocket_artillery Congreve 1804)**: FIXED — current_date>1804.
- **F10 (Part E asserts unproven has_variable in tradition allow)**: the F/G/H research agent SUBSEQUENTLY PROVED
  it (Invictus 00_greek_2.txt gates on has_variable via trigger_else_if). Part G updated to confirmed; Part E
  reconciled — the Qing trees use trigger_else_if{ has_variable } which IS proven. No contradiction remains.
- **F11 (Tanding-rube typo)**: FIXED in doc.
- **F12 (00_default.txt 0-byte not BOM)**: noted; the mod's 00_default.txt IS 3 bytes (a BOM) per earlier xxd —
  minor; no BOM-discipline concern for the new 00_qing_distinctions.txt (will write clean).
- **naming (punic_principles_inv -> hundred_four_inv)**: FIXED the oracle example name in the Qing invention header.
Net: 6 real anachronism leaks closed (naval_explosives, cellular_pathology, medical_imaging, recoil_buffers,
rocket_artillery, central_banking) + 2 requires typos + 1 efficiency trim. Date-gate total now 35.

# PHASE 6 DONE (2026-07-25): Military Traditions
1763-ADJUST: the existing trees (00_manchu Ten Great Campaigns, 00_napoleon, + the vanilla arabic/indian/etc.)
are era-AGNOSTIC culture-flavour trees (no dated tech), so there is nothing anachronistic to gate — the manchu
tree is already 1755-92 High-Qing content. The 1763 work is therefore the NEW Qing trees, not edits to old ones.
NEW: common/military_traditions/00_qing.txt — 5 Qing culture/subject trees (28 nodes), each FLAT (manchu/arabic
pattern), placeholder .dds, all modifier keys validated against the mod's populated trees:
- 八旗 qing_eight_banners_tradition (jurchen | 兵部 staffed): banner reserve -> cavalry/騎射 -> garrison + 火器營 -> capstone.
- 綠營 qing_green_standard_tradition (chinese_group | han_science | 兵部): provincial mass -> battalions -> garrison-posts + 藤牌兵.
- 蒙古馬隊 qing_mongol_cavalry_tradition (mongolic | mongol_science | 兵部): remount -> raiders -> endurance -> capstone.
- 藩部邊防 qing_frontier_defence_tradition (bodish/east_turkic | tibetan/uyghur_science | 兵部): garrison -> 屯田 colonies -> highland + desert war.
- 朝貢徵調 qing_tributary_levy_tradition (兵部 | qing_rites_tributary_count): levy -> auxiliaries -> host -> capstone.
MINISTRY-OF-WAR TIE-IN (Part G traditions half): every tree's allow uses the PROVEN Invictus 00_greek_2.txt
idiom — trigger_if{ culture_group began_with_tradition_group } / trigger_else_if{ has_variable = qing_office_war_
holder ... }. has_variable in a tradition allow is proven engine behaviour (the F10 review concern is thereby
resolved — it's not the unproven var:X>=N form, just has_variable). So the Qing trees unlock for their culture
group OR once the 兵部 is staffed — the martial ministry literally opens the martial trees.
- BUG CAUGHT + FIXED: first draft gated the tributary tree on bare `qing_tributary_count` which doesn't exist;
  corrected to the REAL country var qing_rites_tributary_count (se_QING_MINISTRY.txt:674, recomputed from actual
  tributary subjects). The other science vars (han/mongol/tibetan/uyghur_science) are armed by Part D decisions.
LOC: 28 tradition names+descs in military_traditions_l_english.yml; 5 unlock tooltips in interface_l_english.yml.
Brace-balanced, LF (matches sibling manchu tree). interface_l CRLF restored after append.

# PHASE 4d DONE (2026-07-25): Legion Distinctions + Ministry-of-War tie-in (Parts F + G merged)
DISTINCTIONS (common/legion_distinctions/00_qing_distinctions.txt): 6 Qing distinctions —
綠營標營/健銳營(Jianrui)/索倫勁旅(Solon)/火器營(Firearms)/藤牌兵(Rattan)/駝城(Camel-fort). Distinctions CANNOT be
gated (oracle-verified), so defined globally.
- SCOPE BUG CAUGHT + FIXED: first draft put terrain bonuses as unit-prefixed (heavy_infantry_mountain_combat_
  bonus) + siege_ability in unit{}. Verified against TI 00_default.txt: in a distinction, terrain bonuses are
  BARE (mountain_combat_bonus) and siege_* lives in legion{}. Rewrote: unit-type offensive/defensive/discipline
  keys prefixed, terrain bonuses bare, siege_ability+siege_engineers in legion{}. All keys proven in TI distinctions.
- Icons = base-game phalera_* sprites (bare refs, resolve on the base game).
MINISTRY-OF-WAR GRANT PATH (the tie-in, Part G distinctions half): QING_war_grant_legion_distinction
(se_QING_WAR.txt), called from on_legion_raised (00_specific_from_code.txt, scope=legion — the PROVEN
add_distinction site, alongside the existing MOBIL_stamp_legion). Reads owner's qing_min_perf_war band:
>=70 elite (健銳營/火器營 random), 40-69 standard (綠營/藤牌/索倫/駝城 random), <40 or no-var basic (綠營標營).
Self-guards tag=CHI + no-existing-Qing-distinction (non-CHI = no-op; no re-grant/stack). Startup-window
exemption (current_date>1763.2.17) so the setup establishment isn't retro-branded. No character iterator (legion
scope) — no compile-recursion risk; runs from a real on_action not a compiled button.
PANEL SURFACING (Part G): gui/qing_war_ministry.gui gets an "Army Doctrine (營制)" read-out with 3 band-gated
tier labels (elite/standard/basic) via GreaterThanOrEqualTo_CFixedPoint + And/Not (all proven GUI funcs) on
qing_min_perf_war, + a tooltip explaining the bands. LOC: 6 distinction names+descs in legions_l_english.yml;
5 panel strings in qing_war_ministry_l_english.yml.
Def<->grant<->loc names cross-checked (all 6 consistent); all files brace-balanced; endings match HEAD.

# PHASE 5 — IMPLEMENTATION REVIEW RESOLUTIONS (agent, 2026-07-25)
Pre-commit adversarial review: NO boot-crash risk found; load-bearing idioms verified against oracles
(this.culture.culture_group=culture_group:X, owner={save_scope_as} legion->country, add_distinction at legion
scope, all 35 date-gates correctly in potential preserving existing lines, all modifier keys valid at scope, all
77 loc keys defined, all read-vars set, standing rules clean). Findings actioned:
- **M1 (tradition allow gated only cosmetically — trigger_if-only evaluates TRUE for all)**: FIXED. Added a
  fail-closed `trigger_else` (sibling of trigger_if/trigger_else_if) to ALL 5 trees, re-asserting the full OR of
  unlock conditions so a country matching neither branch is LOCKED. First automated pass mis-NESTED the else
  inside the else_if; rewrote the file cleanly — verified all 5 trigger_else are 2-tab siblings. This is a
  genuine improvement over the mod's existing manchu/arabic trees (which have the cosmetic-only pattern). 5 new
  qing_tradition_locked_* loc tooltips added.
- **M2 (loyalty_gain_chance_modifier in distinction commander{} — diverges from TI's sole proven placement)**:
  FIXED. Moved to unit{} in all 6 distinctions (TI 00_default.txt places it in unit{}). No empty commander blocks.
- **L1 (does CHI match a 2nd heritage?)**: VERIFIED CLEAN. buddhist_group_trigger = theravada/mahayana/vajrayana/
  pure_land/thagyaminist/bon — NOT confucianism; CHI (jurchen group, confucianism, imperial_monarchy, non-tribal)
  matches none of tribal_learning's ORs. CHI matches ONLY evidential_learning.
- **L2 (BOM/LF on 6 new files)**: VERIFIED CLEAN. All no-BOM, LF (matching siblings).
FINAL VALIDATION: all 16 touched .txt/.gui files brace-balanced; all line-endings match HEAD (interface_l +
oratory kept CRLF; rest LF); new files no-BOM. Ready to commit + push.

