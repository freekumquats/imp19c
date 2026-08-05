# Assessment — Qing starting Administrative Capacity (1763) [task #25]

## Question
Is the Qing's starting administration supply appropriate for 1763, or does it begin badly
under-administered (which would show as widespread "Overstretched Administration" state-loyalty
drain — `ADMIN_state_loyalty_from_province_drain`, se_ADMIN.txt)?

## How supply and demand are computed (verified in code)
**Supply** (`ADMIN_provided_state`, ADMIN_svalues.txt:74): `10 × num_of_URB_administration_district`
in the state, plus a 10% spillover of the capital's districts to every state.

**Demand** (`ADMIN_required_state` ← `ADMIN_required_province`, ADMIN_svalues.txt:29): per province
`1 base + terrain surcharge (0 / +1 harsh / +3 extreme) + total_population/10`, summed over the
state's provinces, then × `MODIFIER_country_all_state_admin_points_efficiency` (law multiplier).

**Impact** (`ADMIN_set_loyalty_impact_state`, se_ADMIN.txt): `required − provided > 0` → drain
(`-0.01 monthly state loyalty per point of shortfall`); `≤ 0` → gain.

## How admin districts are SEEDED (setup/buildings_generator.py:72)
`URB_administration_district = round(middle_strata / 10)` — **applied uniformly to every province in
the world**, not Qing-tuned. So a province's admin SUPPLY ≈ `10 × round(middle_strata/10) ≈ middle_strata`.

## The mismatch
Per province: **supply ≈ middle_strata**, **demand ≈ total_population/10 + terrain**.
- In the Qing agrarian heartland, the middle strata (merchants, lower gentry, clerks) is a small
  fraction of a population that is overwhelmingly lower-strata peasantry. If middle_strata is, say,
  5–10% of total population, supply (`≈ middle_strata`) is BELOW demand (`≈ pop/10 = 10% of pop`) —
  before the terrain surcharge is even added.
- The seeded distribution confirms the thinness: of CHI provinces, **887 get just 1 admin district**
  (10 capacity — covers only ~90 pop + terrain), 375 get 2, tailing off; only a handful exceed 5.
- High-terrain frontier provinces (Tibet/Xinjiang/Mongolia — extreme mountain/desert = +3 demand
  each) carry a heavy terrain surcharge with almost no middle strata to supply districts, so they are
  the worst-covered.

**Conclusion: the Qing begins systematically under-administered** across its populous interior and its
rough frontier — the "Overstretched Administration" drain would be broad at game start. This is an
artifact of the global `middle_strata/10` seeding formula, which does not reflect the historically
large and effective High-Qing (Qianlong-era) bureaucracy — the county-magistrate (知縣) network, the
provincial governor / governor-general (督撫) hierarchy, and the sub-bureaucratic yamen clerk/runner
establishment that actually administered ~300M people.

## Recommendation (proposed — a real balance change, flagged for greenlight)
Seed a **Qing-specific administration top-up** at game start, so CHI's supply meets the demand its own
population + terrain raise, rather than the thin global `middle_strata/10` allotment. Options, least to
most invasive:

1. **Targeted district seed (preferred):** in a CHI game-start seed effect (se_QING_BUILDINGS.txt
   pattern), for each CHI-owned state, add admin districts until `ADMIN_provided_state_max_bonus`
   meets `ADMIN_required_state` (cap at the requirement — extra districts are wasted, ADMIN_svalues.txt:67).
   Respects the city/potential gate ([[imp19c-add-building-level-respects-potential]]); historically
   grounded; leaves ROW untouched (asymmetric fidelity).
2. **Efficiency modifier:** grant CHI a country modifier raising admin points per district (there is a
   hook, `ADMIN_country_points_from_admin_districts_modifier`, ADMIN_svalues.txt:60). Cheaper but blunt.
3. **Do nothing / treat the drain as intended friction** — the Qing's over-extension IS a theme; but a
   near-universal drain from turn 1 is noise, not a meaningful signal.

Prefer (1): concrete on-map objects (the yamen network), demand-capped so it can't over-shoot, Qing-only.

## Dependencies / interaction
- The drain modifier only tracks reality after the **biannual refresh** just added ([task #24],
  yearly_country_pulse) — before that fix it was frozen at setup, so the shortfall wasn't even
  updating. Assess the true post-seed balance from a boot log AFTER #24 lands.
- Loc for the drain/gain modifiers was just added ([task #6]) so the impact is now legible in-game.

## RESOLUTION (2026-08-04, implemented) — count the yamen as admin capacity
The user pointed out the cleaner fix: rather than seed extra generic `URB_administration_district`
onto China, make the **衙門 (qing_yamen_building) actually provide admin capacity** — which it thematically
already IS ("the CONCRETE face of the abstracted bureaucracy-CAPACITY meter", per its own building
comment), but fed nothing into `ADMIN_provided_state` (which counted only `URB_administration_district`).

Implemented in `ADMIN_svalues.txt`: `ADMIN_provided_state` now adds
`num_of_qing_yamen_building × ADMIN_provided_per_qing_yamen (=8)` per province (a yamen administers a
county — a shade below a dedicated administration district's 10). Why this is the right fix over
option 1:
- **Thematically correct:** the mod's own concrete admin building finally relieves the admin drain it
  represents. Before, the Qing built yamens (via `QING_GOV_yamen_band_track` on the capacity band) that
  did nothing for the engine's admin supply — two disconnected tracks.
- **Self-scaling:** the governance capacity-band pulse already raises/removes yamens as the abstracted
  capacity meter moves, so admin supply now tracks Qing governance quality automatically — no static
  seed to maintain, no ROW change (asymmetric fidelity preserved; the yamen is Qing-only).
- **Safe:** `ADMIN_provided_state_max_bonus` caps supply at demand, so yamens only reduce shortfall,
  never create surplus.

The ADMIN capacity system is confirmed MOD-INVENTED (vanilla Imperator has no admin-capacity /
URB_administration_district; git history = WiP mod work), so this edit is mod-owned, not upstream.

Option 1 (seed more admin districts) is therefore NOT needed and NOT done. Re-check the post-fix balance
from a boot after this + the #24 biannual refresh land; if yamens alone don't close the gap in the
populous heartland, revisit the per-yamen value (8) or add a modest 1763 yamen seed then.
