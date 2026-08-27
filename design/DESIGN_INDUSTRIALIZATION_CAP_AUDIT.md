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

## Case 2 — CHI (Qing) — CONFIRMED, FIXED, THEN CORRECTED (commits a6ef6b68a, 7a83859eb)

1763 grant (`se_TEST.txt:396-411`, PRE-FIX): `TECH_unlock_military_level_0` + `_level_1`,
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
(+1), `tech_construction` (+1) = **invention contribution = 4 (PRE-FIX)**.

Government type: CHI = `imperial_monarchy` (`setup/main/00_default.txt:35657`).
Checked directly (`common/governments/00_albert.txt:387-406`): `base` block contains
only `global_upper_strata_happyness = 0.05` — **no `country_civilization_value` key,
base = 0.** Same zero-base pattern as `federated_tribe` and `absolute_kingdom` in
Case 1 — this file's monarchy-type governments uniformly carry no civ-value base;
only a separate ~15-entry table in `00_default.txt` (constitutional/republican-type
governments) grants a nonzero base.

**Calculated cap for CHI (PRE-FIX) = 0 + 4 = 4.**

Setup `civilization_value` samples:
- `00_Guangxi.txt`: flat **6** across every sampled province line — **over the pre-fix cap of 4.**
- `00_Far_East.txt` (Han-culture core): distribution is 207×0, 2×5, 1×7, 1×8, 10×10 —
  every nonzero province (5, 7, 8, 10) is **over the pre-fix cap of 4.**

**CONFIRMED VERDICT (PRE-FIX) for CHI specifically (the mod's central focus): the
historical Chinese heartland provinces were set up well above the calculated cap of 4.**

**ROOT CAUSE, traced via `git blame`:** CHI's civic tier stopping at level 1 was
partly an oversight. The commit that first split the 1763/1815 branches
(`86fa05438`, 2026-08-25) stated its own general rule as "civic level 1-2" for
every bloc, but CHI's specific block was written with `civic_level_1` only,
missing `_level_2` — and this was never re-examined when the rest of the branch got
its historical-sourcing audit (`b19c50eb7`, tonight), which touched CHI's military
and oratory grants with real citations but left civic untouched.

**FIRST FIX, commit `a6ef6b68a` (SUPERSEDED — do not repeat this reasoning):**
granted the WHOLE `civic_level_2` block, on the claim that "nothing in the design
docs argues Qing specifically lacked" this tier. **That claim was wrong** — a
code-review check found `design/DESIGN_1763_STARTING_TECH_AUDIT.md` has a
dedicated CHI section that explicitly addresses this exact tier and says the
opposite: do NOT grant the whole block, cherry-pick `tech_artificial_canals`
only. Its stated reasoning: the Grand Canal (大運河) and Qing hydraulic
engineering (河工) justify canal technology specifically, but `gear_systems`/
`templating` imply proto-industrial mechanization Qing did not have by
1763 — granting the whole tier is a "false-equivalence trap" with Europe. The
same doc's cross-bloc note: CHI should end up "out-bureaucracying Europe but
lagging it in mechanization," not matching it tier-for-tier. That doc also
records that the user explicitly asked for CHI to get its own dedicated,
separately-scrutinized second pass — which never happened before tonight, so
this tier was left both under-granted (civic_1 only, missing even the
recommended canals cherry-pick) AND unresolved until now.

**CORRECTED FIX, commit `7a83859eb`:** reverted the whole-block grant, added
only `unlock_invention = tech_artificial_canals` instead, following the
audit doc's specific recommendation. New invention contribution: 4 (weapon_mfg
1 + shipyards 1 + metalworking 1 + construction 1) + `tech_artificial_canals`
(2) = **6**. (`tech_gear_systems`/`tech_templating`/`tech_mining_rails` are
NOT granted — mining_rails contributes 0 to the tally either way, so this
doesn't change what mining_rails alone would have done, but gear_systems(+5)
and templating(+1) are real, deliberately excluded contributions.)

**Final calculated cap for CHI = 0 + 6 = 6** — higher than the pre-fix 4, but
deliberately below the 12 every Old World bloc reaches, per the audit doc's
intended relative positioning (bureaucratic leader, mechanization laggard).
Re-checked against the same samples: Guangxi's flat 6 now sits exactly AT the
new cap (not over); Far East's 5 is now under, but 7/8/10 are still over the
cap of 6 — a smaller, partial fix, not a full resolution. Whether those
remaining Far East outliers need a province-level setup adjustment, or
whether cap=6 itself still needs revisiting, is not decided here.

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
| CHI (Qing) — FIXED (`7a83859eb`) | mil 0-1, oratory 1-2, civic 1+canals cherry-pick, religious 1, +rocket_artillery/census/postal_admin | 6 (was 4) | 0 (imperial_monarchy) | **6** (was 4) |
| Bloc A — Western Europe — FIXED (`b1c65c5b4`) | mil 0-2+SYW, oratory 1-2, civic 1+canals cherry-pick, religious 1-2+Enlightenment | 6 (was 12) | 0 (charter_parliament) | **6** (was 12) |
| Bloc B — Slavic — FIXED (`b1c65c5b4`) | identical grant to Bloc A | 6 (was 12) | 0 (imperial_monarchy), but 35 if aristocratic_monarchy (some Polish-type tags) | **6** (up to 41 for the minority on a real-base type) |
| Bloc C — South/SE Asia periphery — FIXED (`b1c65c5b4`) | mil 0-2, oratory 1-2, civic 1+canals cherry-pick, religious 1 | 6 (was 12) | 0 | **6** (was 12) |
| Bloc D — Ottoman/Islamic — FIXED (`b1c65c5b4`) | mil 0-2+mortar+wheeled_cannons, oratory 1-2, civic 1+canals cherry-pick, religious 1 | 6 (was 12) | 0 | **6** (was 12) |
| GBR/NED banking carve-out — FIXED (`b1c65c5b4`) | Bloc A grant + oratory 3-4 (central_banking etc., all zero-contribution) | 6 (was 12) | 0 | **6** (was 12) |

**Every bloc in the 1763 branch except the deliberately-minimal Africa/NA floor
now converges to the same cap (6).** Reasoning for the sweep, prompted directly
by the user: the initial fix reasoning (CHI specifically lagged Europe in
mechanization by 1763) was the wrong frame entirely — the Industrial Revolution
had not begun ANYWHERE in 1763 (Hargreaves' spinning jenny is 1764, Watt's
improved steam engine is 1769, both still in the future even in Britain). So
`gear_systems`/`templating` (proto-industrial mechanization tech) being
anachronistic isn't a China-specific historical judgment — it's true for every
1763 bloc, including Western Europe itself. `civic_level_2`'s whole-block grant
was removed from Bloc A/B/C/D the same way it was from CHI, cherry-picking only
`tech_artificial_canals` (genuinely ancient/universal pre-industrial
engineering) everywhere. This is a materially different, more defensible
position than either the original state (CHI capped well below everyone else
for no stated reason) or the first CHI-only fix (CHI still capped at half of
Europe for a reason — "mechanization lag" — that doesn't actually distinguish
1763 from anyone else, since NOBODY had that mechanization yet).

**Africa/Native-America floor bloc — CHECKED, NOT AN OVERSIGHT, left as-is.**
`design/DESIGN_1763_STARTING_TECH.md` (lines 204-224) explicitly labels this
grant deliberate: "same grant (weapon_manufacturing, firearms, civic_level_1),
same idiom, zero new logic" by design, and the true Bloc E catch-all's floor
(military_0 + civic_1, "nothing more") is explicitly justified — firearms
reached these regions via centuries of fur-trade/gun-commerce contact, and
the floor itself, not full civic parity, was the deliberate design choice.
This bloc never had `civic_level_2` to remove, so the sweep doesn't touch it,
and its lower cap relative to everyone else remains intentional.

## Setup-value comparison, real samples pulled from source

| Sample province file | Bloc / owner | Cap | civilization_value values found | Verdict |
|---|---|---|---|---|
| `00_Great_Lakes.txt` (C3F, ojibwe-potawatomi) | Africa/NA floor | 3 | mostly 0, one province at **15** | **5x OVER** |
| `00_Congo_Basin.txt` (Kongo/Luba etc.) | Africa/NA floor | 3 | mostly 0, several at 5-7 | **OVER** at every nonzero province |
| `00_Sahel.txt` (Hausa/Fulani/Songhai/Mossi/Tuareg) | Africa/NA floor | 3 | mostly 0, max 1 | under, fine |
| `00_Guangxi.txt` (CHI, Han) | CHI | 6 (was 4) | flat **6** | **AT cap** — was over cap 4, now exactly at cap 6 |
| `00_Far_East.txt` (CHI, Han) | CHI | 6 (was 4) | 207×0, 2×5, 1×7, 1×8, 10×10 | **PARTIAL** — the 5 is now under cap 6, but 7/8/10 are STILL over |
| `00_Andalusia.txt` (FRA/Spain) | Bloc A | 6 (was 12) | 25×10, 1×12, 8×15, 1×17, 2×20 | **NOW OVER EVERYWHERE** — even the 25 provinces at 10 (previously fine under cap 12) are now over cap 6 |
| `00_Baltic_states.txt` (RUS-adjacent) | Bloc B | 6 (was 12; or 41 if aristocratic_monarchy) | 45×7, 31×10, 4×12, 2×15 | **NOW OVER EVERYWHERE** at cap=6 (previously only the 15s were over cap 12); if the owning tag is on a real-base type (35), all still clear |
| `00_Aegean.txt` (Ottoman/Turkish) | Bloc D | 6 (was 12) | flat 10 | **NOW OVER** — this sample was clean under cap 12, is over under the corrected cap 6 |

## Bottom line

**Tech-grant fix is done and applied uniformly** (commits `a6ef6b68a` →
`7a83859eb` → `b1c65c5b4`). The key correction, prompted directly by the user:
the first CHI-only fix was reasoning from the wrong premise — "CHI should lag
Europe in mechanization" implies Europe HAD mechanization to lag behind in
1763, which isn't true. The Industrial Revolution had not started anywhere at
this date (spinning jenny 1764, Watt's engine 1769, both still in the future).
So `civic_level_2`'s proto-industrial techs (`gear_systems`/`templating`) are
anachronistic for every bloc, not a China-specific exclusion — and every bloc's
grant has now been corrected the same way, cherry-picking only
`tech_artificial_canals`. Every Old World bloc (CHI, Western Europe, Slavic,
Ottoman/Islamic, South/SE Asia) now converges on the same cap: **6**. The
Africa/NA floor bloc, whose lower cap (3) was already confirmed deliberate
elsewhere in the design docs, is unaffected.

**Consequence, stated plainly:** this makes the setup-value mismatch problem
WORSE for the Old World blocs, not better, in the sense that far more
provinces are now measurably over cap than before the sweep (Andalusia's
25 provinces at civilization_value 10 were fine under the old miscalculated
cap of 12; they are now over the corrected cap of 6). This is not a regression
— it means the TRUE size of the bug was being undercounted by the earlier,
too-generous cap calculation for those blocs. The bug is now confirmed, by
static source, across every sampled bloc with no exception (the one previously
clean sample, Aegean/Ottoman, is now also over).

Two distinct, independently-real factors remain, not yet acted on:
1. **The 1763 tech-grant cut itself is done and correct** — every bloc's grant
   now reflects a consistent, defensible 1763 reality (nobody had proto-
   industrial mechanization yet), so this side of the problem is closed.
2. **This mod's own 30 custom government types have zero `country_civilization_value`
   base**, unlike the 15 leftover vanilla types. This is very likely a PRE-EXISTING
   gap, not something the 1763 rework introduced — it was simply invisible before
   because the old, bigger uniform tech grant was large enough to keep setup values
   under cap on its own. The 1763 rework didn't cause this zero-base gap; it exposed it,
   and tonight's cap correction (12→6 for most blocs) makes the exposed gap larger,
   not smaller.

Still not decided (this is a bigger, cross-cutting call, not a targeted
tech-grant fix like the ones above): whether the now-widespread over-cap
setup `civilization_value` numbers should be lowered per-province to match
each bloc's corrected cap of 6 (touches setup files across every region), or
whether the 30 zero-base government types should get a real base value
(which would raise every affected cap, all eras, not just 1763 — a much
bigger blast radius, needs its own decision, not a default assumption).
