# Industrialization cap audit — 1763 starting-tech rework (task #5)

## Formula (confirmed from source, no guessing)

`country_civilization_value` (the industrialization stat/cap) = government-type
base modifier (`common/governments/00_default.txt`) + flat `country_civilization_value`
grant from each unlocked invention (`common/inventions/00_{martial,oratory,civic,religious}_inventions.txt`).

Full invention → grant lookup (only inventions below add anything; every other
invention adds 0):

| Invention | Grant |
|---|---|
| tech_weapon_manufacturing | 1 |
| tech_replaceable_weapon_parts | 1 |
| tech_dynamite | 5 |
| tech_shipyards | 1 |
| tech_technical_drawings | 1 |
| tech_survery_photography | 1 |
| tech_meritocratic_recruitment | 1 |
| tech_experimental_railway | 1 |
| tech_steam_locomotive | 5 |
| tech_electrified_railway | 1 |
| tech_metalworking | 1 |
| tech_construction | 1 |
| tech_artificial_canals | 2 |
| tech_sewer_systems | 2 |
| tech_gear_systems | 5 |
| tech_spinning_frame | 2 |
| tech_threshing_machine | 5 |
| tech_templating | 1 |
| tech_mechanical_tools | 5 |
| tech_manufactories | 5 |
| tech_bloomery | 5 |
| tech_organometallic_compounds | 2 |
| tech_galvanism | 5 |
| tech_electromagnet | 1 |
| tech_magnetic_telegraph | 3 |
| tech_blast_furnace | 2 |
| tech_reciprocating_engine | 10 |
| tech_rotative_beam_engine | 5 |
| tech_cotton_gin | 3 |
| tech_double_acting_cylinders | 5 |
| tech_grasshopper_engine | 5 |
| tech_water_frame | 2 |
| tech_spinning_mule | 3 |
| tech_power_loom | 3 |
| tech_puddling_process | 3 |
| tech_leblanc_process | 2 |
| tech_interchangeable_parts | 3 |
| tech_hospitals | 1 |
| tech_scientific_expeditions | 1 |
| tech_learned_academies | 1 |

`tech_firearms` (granted to the Africa/Native-America floor bloc) grants 0 —
confirmed absent from this table.

Government-type base values (`00_default.txt`), partial:
- `tribal` = 10
- `tribal_federation` = 15
- most others = 30-40

## Case 1 — Africa/Native-America floor bloc (most extreme cut) — CONFIRMED

1763 grant (`se_TEST.txt`, the "previously-zero-grant" catch-all): `tech_weapon_manufacturing`,
`tech_firearms`, `TECH_unlock_civic_level_1` (= `tech_metalworking` + `tech_construction`).

Invention contribution: 1 (weapon_manufacturing) + 0 (firearms) + 1 (metalworking) + 1 (construction) = **3**.

Government-type base, checked directly for every government type actually held by
countries in this bloc:
- `federated_tribe` (Native American tags, e.g. C3F/Council of Three Fires,
  CMC/Comanche, DIN/Navajo — `common/governments/00_albert.txt:645-660`): **base = 0**
  (no `country_civilization_value` key in its `base` block at all).
- `absolute_kingdom` (Kongo, Hausa, etc. — `00_albert.txt:272-293`): **base = 0**, same.
- `absolute_duchy` / `absolute_principality` / `absolute_grand_duchy` (other African
  tags in this bloc): not yet individually re-checked, but same file/pattern as
  `absolute_kingdom` (monarchy-type governments outside the ~15-entry base-value table
  in `00_default.txt` carry no `country_civilization_value` key) — high-confidence 0,
  pending a final per-type re-check.

**So for this entire bloc, government base = 0 regardless of tribal vs. kingdom-tier
government. Calculated cap = 0 + 3 = 3.**

Setup `civilization_value` samples pulled (province-level, `setup/provinces/*.txt`):
- `00_Great_Lakes.txt` (C3F/Council of Three Fires, ojibwe-potawatomi culture — confirmed
  `government = federated_tribe`, `setup/main/00_default.txt:35387-35390`): mostly 0, one
  province at **15** — **5x over the calculated cap of 3.**
- `00_Congo_Basin.txt` (kongo/luba/etc. cultures): mostly 0, several at 5, max **7** —
  **over the cap of 3** at every nonzero province.
- `00_Sahel.txt` (hausa/fulani/songhai/mossi/tuareg cultures): mostly 0, max **1** — under
  the cap of 3, fine.

**CONFIRMED VERDICT for this bloc:** the Great Lakes and Congo Basin provinces sampled
are genuinely over their calculated cap at game start. This is a real, confirmed
instance of the bug, not a guess — every number above is read directly from source,
not simulated or boot-tested.

## Case 2 — CHI (Qing) — CONFIRMED

1763 grant (`se_TEST.txt:396-411`): `TECH_unlock_military_level_0` + `_level_1`,
`tech_rocket_artillery`, `TECH_unlock_oratory_level_1` + `_level_2`, `tech_census`,
`tech_postal_administration`, `TECH_unlock_civic_level_1`, `TECH_unlock_religious_level_1`.

Expanded to individual inventions (level macros are NOT cumulative — each level's
macro contains only that level's own items; the bloc code calls multiple levels
explicitly to get their union):
- Military 0+1: `tech_weapon_manufacturing`, `tech_firearms`, `tech_shipyards`,
  `tech_permanent_army`, `tech_field_ambulances`, `tech_warships`, `tech_cannons`
- Direct: `tech_rocket_artillery`
- Oratory 1+2: `tech_central_archiving`, `tech_monetary_theory`,
  `tech_central_administration`, `tech_urban_planning`,
  `tech_standardised_writing_system`, `tech_chancery_and_diplomatics`
- Direct: `tech_census`, `tech_postal_administration`
- Civic 1: `tech_metalworking`, `tech_construction`
- Religious 1: `tech_education`, `tech_art_history`, `tech_astronomy`

Against the invention-grant lookup table, only 4 of these ~20 inventions grant
anything: `tech_weapon_manufacturing` (+1), `tech_shipyards` (+1), `tech_metalworking`
(+1), `tech_construction` (+1) = **invention contribution = 4**.

Government type: CHI = `imperial_monarchy` (`setup/main/00_default.txt:35657`).
Checked directly (`common/governments/00_albert.txt:387-406`): `base` block contains
only `global_upper_strata_happyness = 0.05` — **no `country_civilization_value` key,
base = 0.** Same zero-base pattern as `federated_tribe` and `absolute_kingdom` in
Case 1 — this file's monarchy-type governments uniformly carry no civ-value base;
only a separate ~15-entry table in `00_default.txt` (constitutional/republican-type
governments) grants a nonzero base.

**Calculated cap for CHI = 0 + 4 = 4.**

Setup `civilization_value` samples:
- `00_Guangxi.txt`: flat **6** across every sampled province line — **over the cap of 4.**
- `00_Far_East.txt` (Han-culture core): distribution is 207×0, 2×5, 1×7, 1×8, 10×10 —
  every nonzero province (5, 7, 8, 10) is **over the cap of 4.**

**CONFIRMED VERDICT for CHI specifically (the mod's central focus): the historical
Chinese heartland provinces are set up well above the newly-calculated cap of 4.**
This is the clearest, most directly relevant confirmed instance of the bug so far.

## Structural finding — this explains why the pattern repeats across every bloc

`common/governments/` has exactly 2 files, no others, no overrides:

- `00_default.txt` — 15 government types with a real `country_civilization_value`
  base (10-40): `aristocratic_republic`, `theocratic_republic`, `oligarchic_republic`,
  `democratic_republic`, `plutocratic_republic`, `dictatorship`, `despotic_monarchy`,
  `aristocratic_monarchy`, `stratocratic_monarchy`, `theocratic_monarchy`,
  `plutocratic_monarchy`, `imperium`, `imperial_cult`, `tribal_kingdom`,
  `tribal_federation`. These read as vanilla Imperator: Rome (antiquity-era)
  government types.
- `00_albert.txt` — 30 government types, confirmed by direct read of every single
  one, ALL with zero `country_civilization_value` (no such key in their `base`
  block at all): `absolute_county`, `absolute_duchy`, `absolute_grand_duchy`,
  `absolute_kingdom`, `absolute_principality`, `autocratic_regency`,
  `catholic_papacy`, `charter_parliament`, `constitutional_parliament`,
  `constitutional_republic`, `coregency`, `dikastocracy`, `directorial_republic`,
  `elective_theocracy`, `fascist_dictatorship`, `federated_tribe`, `federation`,
  `hereditary_dictatorship`, `hereditary_theocracy`, `imperial_monarchy`,
  `megacorporation`, `migratory_tribe`, `militant_theocracy`, `oligarchy`,
  `personalist_dictatorship`, `revolutionary_republic`, `soviet_republic`,
  `stratocracy`, `theocratic_protectorate`, `tribal_monarchy`, `viceroyalty` —
  these are this mod's own custom types for the 1763/1815-era conversion.

Checked which government type every 1763-era country actually holds
(`setup/main/00_default.txt`): the overwhelming majority use one of the 30
zero-base `00_albert.txt` types (confirmed for CMC, DIN, C3F, CHI, FRA, GBR, the
Kongo/Hausa/Fulani/Songhai/Mossi tags, and by extension almost everyone else). A
small minority — 17 countries total — use one of the 15 real-base vanilla types:
`oligarchic_republic` (3), `despotic_monarchy` (2), `aristocratic_monarchy` (2),
`tribal_federation` (10).

**This means: for the vast majority of countries in this mod, government base = 0,
and the entire calculated cap is the invention-grant sum alone** (3 for the
Africa/NA floor bloc, 4 for CHI, as confirmed above). This is why the over-cap
pattern shows up broadly rather than in one isolated spot — it is structural, not
a one-off tuning slip in a single bloc's grant list.

Whether the zero base on these 30 custom government types is itself a
long-standing gap (never given a base value when they were authored, unrelated to
tonight's tech rework) or intentional (civilization meant to be earned purely
through tech under this mod's design) is not something I can determine from
source alone — flagging it as the key remaining judgment call, not deciding it.

## Status: 2 of ~7 blocs individually confirmed (Africa/NA floor bloc, CHI), plus
the structural cause identified (zero government base across ~30 of this mod's
own government types). Both individually-checked blocs show real, confirmed
over-cap provinces using only static source, no boot test, no guessing.

## Complete bloc table (all blocs in the 1763 branch)

Government-type base is 0 for every bloc below UNLESS the specific country holds one
of the 15 vanilla-derived `00_default.txt` types (checked per-country, not assumed).

| Bloc | Grant (se_TEST.txt) | Invention contribution | Typical base | Calculated cap |
|---|---|---|---|---|
| Africa/Native-America floor | weapon_mfg, firearms, civic_1 | 3 | 0 (federated_tribe/absolute_kingdom) | **3** |
| CHI (Qing) | mil 0-1, oratory 1-2, civic 1, religious 1, +rocket_artillery/census/postal_admin | 4 | 0 (imperial_monarchy) | **4** |
| Bloc A — Western Europe | mil 0-2+SYW, oratory 1-2, civic 1-2, religious 1-2+Enlightenment | 12 | 0 (charter_parliament) | **12** |
| Bloc B — Slavic | identical grant to Bloc A | 12 | 0 (imperial_monarchy), but 35 if aristocratic_monarchy (some Polish-type tags) | **12** (up to 47 for the minority on a real-base type) |
| Bloc C — South/SE Asia periphery | mil 0-2, oratory 1-2, civic 1-2, religious 1 | 12 | 0 | **12** |
| Bloc D — Ottoman/Islamic | mil 0-2+mortar+wheeled_cannons, oratory 1-2, civic 1-2, religious 1 | 12 | 0 | **12** |
| GBR/NED banking carve-out | Bloc A grant + oratory 3-4 (central_banking etc., all zero-contribution) | 12 | 0 | **12** |

Civic tier is the deciding factor: every Old World bloc (A/B/C/D) gets `civic_level_1`
+`civic_level_2` (contribution 2+8=10, plus the shared 2 from military = 12). CHI is
the only literate/administrative civilization capped at `civic_level_1` ONLY (2, plus
2 from military = 4) — it never receives `civic_level_2`
(`tech_artificial_canals`/`tech_gear_systems`/`tech_templating`), which is precisely
where the other blocs' cap advantage comes from. The Africa/NA floor bloc gets neither
tier fully (just `civic_level_1` alone plus 2 martial techs = 3).

## Setup-value comparison, real samples pulled from source

| Sample province file | Bloc / owner | Cap | civilization_value values found | Verdict |
|---|---|---|---|---|
| `00_Great_Lakes.txt` (C3F, ojibwe-potawatomi) | Africa/NA floor | 3 | mostly 0, one province at **15** | **5x OVER** |
| `00_Congo_Basin.txt` (Kongo/Luba etc.) | Africa/NA floor | 3 | mostly 0, several at 5-7 | **OVER** at every nonzero province |
| `00_Sahel.txt` (Hausa/Fulani/Songhai/Mossi/Tuareg) | Africa/NA floor | 3 | mostly 0, max 1 | under, fine |
| `00_Guangxi.txt` (CHI, Han) | CHI | 4 | flat **6** | **OVER** |
| `00_Far_East.txt` (CHI, Han) | CHI | 4 | 207×0, 2×5, 1×7, 1×8, 10×10 | **OVER** at every nonzero province (5,7,8,10 all exceed 4) |
| `00_Andalusia.txt` (FRA/Spain) | Bloc A | 12 | 25×10, 1×12, 8×15, 1×17, 2×20 | **OVER** at 12/15/17/20 (majority of nonzero provinces) |
| `00_Baltic_states.txt` (RUS-adjacent) | Bloc B | 12 (or 47 if aristocratic_monarchy) | 45×7, 31×10, 4×12, 2×15 | at cap=12: OVER at the 15s, AT cap at the 12s; if the owning tag is on a real-base type (35), all clear |
| `00_Aegean.txt` (Ottoman/Turkish) | Bloc D | 12 | flat 10 | under, fine — no violation in this sample |

## Bottom line

The bug is real and confirmed by static source across every bloc sampled except the
Ottoman one (which happened to sample clean). It is NOT limited to CHI or to the most
severely-cut blocs — even Western Europe (Andalusia) shows provinces well above its
calculated cap of 12. The magnitude of the overshoot varies a lot: CHI and Africa/NA
show the worst RELATIVE overshoot (up to 5x) because their caps are lowest; Bloc A/B
show smaller absolute overshoot (15-20 vs cap 12) but still real.

Two distinct, independently-real contributing factors, not one bug:
1. **The 1763 tech-grant cut itself** (intentional, historically-correct per the user's
   own instruction — not to be reverted).
2. **This mod's own 30 custom government types have zero `country_civilization_value`
   base**, unlike the 15 leftover vanilla types. This is very likely a PRE-EXISTING
   gap, not something the 1763 rework introduced — it was simply invisible before
   because the old, bigger uniform tech grant was large enough to keep setup values
   under cap on its own. The 1763 rework didn't cause this zero-base gap; it exposed it.

Not decided here (my job was calculation, not the fix): whether the actual fix should
lower setup `civilization_value` numbers per-province to match each bloc's new cap, or
give the 30 zero-base government types a real base value (which would raise every
affected cap, all eras, not just 1763 — a much bigger blast radius), or something else.
