# DESIGN #72 — make Relieve & Resettle / Remit the Taxes concrete-over-abstract

## Task
User: "the Relieve & Resettle + Remit the Taxes buttons need to be reworked to be concrete over
abstract... they should take real food from the ever normal granaries and move real pops, and
stop collecting taxes for a year."

## Diagnosis (Rule 1c — why the current state is what it is, traced before changing it)

`QING_pop_relief_resettle` (`common/scripted_effects/se_QING_POPULATION.txt:244-265`) and
`QING_pop_tax_remission` (`:272-284`) both exist and are NOT stubs — they charge real treasury,
touch a real variable, and log. But neither does what its own tooltip narrates:

- **Relieve & Resettle's tooltip** ("Open the granaries to feed the stricken") describes
  DISTRIBUTING existing stored grain (開倉放糧, the historical action this button names). The
  current code instead ADDS 150 to `qing_granary_food` (`:252`) — the granary pool GROWS, funded
  by the -310 treasury charge, as if the state bought extra grain on the market. This is backwards
  from the narrated action: nothing is drawn FROM the granary to feed anyone; the granary number
  and the "relief" are unconnected — the actual crisis relief is entirely the abstract
  `qing_pop_pressure`/`qing_sect_pressure` nudges (`:254-255`). The pop-movement half is closer to
  concrete already: `QING_pop_open_frontier_valve` (`:315-330`) sets `migr_gov_pull = 12` on real
  frontier provinces, which is confirmed (per this file's own `migr_gov_pull` usage) to be a real
  engine migration-pull weight that influences the ENGINE's own migration model — not an abstract
  counter. So resettlement is already substantially concrete; the granary interaction is not.
- **Remit the Taxes's tooltip** ("Remit the land tax of the stricken provinces") describes
  SUSPENDING real tax collection. The current code does nothing to any tax mechanism at all — it
  only nudges `qing_pop_pressure` down by 8 (`:277`) and adds 1 stability. No province or country
  actually stops paying tax; the "remission" is entirely a meter nudge, exactly the complaint.

## Fix

### 1. Relieve & Resettle draws DOWN the real granary pool, gated on having enough to draw
Replace the `+150` add with a real distribution: subtract a real amount from `qing_granary_food`
(floored at 0), gated so the lever can't fire past what the granaries actually hold (mirrors the
existing `treasury >= 310` affordability gate's own idiom — an action that can't be funded/stocked
simply can't be taken). Amount: 150 (unchanged magnitude, now a real distribution instead of a
market purchase — this session's own best-guess, boot-tunable, logged as such). `QING_DECLINE_
granary_rederive` (already called, `:253`) re-derives the cached `qing_granary_stock` band from
the real pool afterward — unchanged, still correct, just now reflecting a real DROP instead of a
real rise.

```
if = {
    limit = {
        treasury >= 310
        has_variable = qing_granary_food
        var:qing_granary_food >= 150
    }
    add_treasury = -310
    change_variable = { name = qing_granary_food  subtract = 150 }
    QING_DECLINE_granary_rederive = yes
    QING_DECLINE_nudge = { var = qing_pop_pressure    amount = -15 }
    QING_DECLINE_nudge = { var = qing_sect_pressure   amount = -6 }
    QING_pop_open_frontier_valve = yes
    add_stability = 1
    LOG_line = { sys = QING  msg = "population: 賑濟移墾 relief distributed real granary stock, resettlement mounted for" }
}
else = {
    LOG_fail = { sys = QING  fn = "QING_pop_relief_resettle"  reason = "treasury below 310 or granary stock below 150 -- cannot fund relief" }
}
```
The GUI's own `is_valid` (`common/scripted_guis/QING_population_panel.txt:41`) must mirror this
new joint gate (treasury AND stock), not just treasury, so the button doesn't invite a click that
silently no-ops (the file's own header comment states this exact "mirrors the effect's own guard"
invariant already — this fix must honor it, not just the effect side).

### 2. Remit the Taxes suspends REAL tax collection for a year, on top of the existing meter nudge
Add a real country modifier that zeroes tax income for 365 days. Checked the existing modifier
vocabulary for a ready-made "no tax" effect before inventing a new one: `common/modifiers/*.txt`
has no existing zero-tax modifier to reuse, so this adds one, `qing_tax_remission_active`
(`local_tax_modifier = -1.0`, i.e. -100%, at the PROVINCE level, applied to every owned province via
`add_province_modifier` — mirrors the existing `qing_granary_empty` idiom in `se_QING_DECLINE.txt`
for "a real, timed, visible province-level suspension", not a country-wide flat modifier, since
the tooltip specifically says "the stricken provinces", not the whole realm). Duration 365 days
(one year, per the task's own wording — best-guess, boot-tunable, logged as such). Scope: only
provinces the pressure model is currently treating as stricken (mirrors `QING_DECLINE_granary_
concrete`'s own "Yellow River basin, stocked" scoping pattern) — for Remit specifically, the
stricken-province proxy already used elsewhere in this suite is `qing_pop_pressure`'s own
provincial pressure source; absent a per-province pressure breakdown, the safest, most defensible
scope (avoiding scope creep into a full new per-province pressure model this task does not ask
for) is EVERY owned province with `has_city_status = yes` — the same populous-city scoping the
granary-build lever already uses for "where the crisis actually bites".

```
QING_pop_tax_remission = {
    LOG_enter = { sys = QING  fn = "QING_pop_tax_remission" }
    if = {
        limit = { treasury >= 220 }
        add_treasury = -220
        QING_DECLINE_nudge = { var = qing_pop_pressure  amount = -8 }
        add_stability = 1
        every_owned_province = {
            limit = { has_city_status = yes }
            add_province_modifier = { name = qing_tax_remission_active  duration = 365 }
        }
        LOG_line = { sys = QING  msg = "population: 蠲免 tax remission proclaimed, real land tax suspended for a year for" }
    }
    else = {
        LOG_fail = { sys = QING  fn = "QING_pop_tax_remission"  reason = "treasury below 220" }
    }
    LOG_exit = { sys = QING  fn = "QING_pop_tax_remission"  result = OK }
}
```
New modifier `qing_tax_remission_active` — **corrected per adversarial review**: `common/modifiers/
qing_population_modifiers.txt` already exists but is scoped to COUNTRY-level `qing_pop_pressure`
band modifiers only (its own header says so). `common/modifiers/imp19c_province_modifiers.txt`
already houses exactly this category — Qing PROVINCE-scope famine/relief modifiers
(`qing_granary_empty`, `qing_grain_relief`), right next to a "# FAMINE" section header. Add
`qing_tax_remission_active` there, not to `qing_population_modifiers.txt` and not to a new file.
`local_tax_modifier = -1.0` is a proven, real key — confirmed by review against
`generic_microstate_modifier` (`00_microprovince_modifiers.txt`), which uses the identical `-1`
convention for "zero this out". Loc'd name/desc for the province-tooltip stack ("蠲免 — Tax
Remission: land tax suspended by imperial decree").

**Two known limitations, logged explicitly per review (not blockers, but real tradeoffs):**
1. **150 food is not a flat, boot-tunable-and-forget constant — it decays in relative impact
   over a long campaign.** At the 1763 seed, granary capacity is `5 granaries × 200 = 1000` and the
   starting pool is pre-filled to 600 (`QING_revenue_seed_historical_granaries`) — so 150 is ~15%
   of total capacity and ~25% of the starting stock, a real felt chunk. But capacity grows as more
   granaries get built (both player-funded and the ~3-year-throttled auto-build), while this
   lever's draw stays flat at 150 — so its relative bite shrinks the longer the campaign runs. This
   is a real design property of the mechanic, not just an untuned number; flagging it here so a
   future pass doesn't mistake "feels weak late-game" for a magnitude bug alone.
2. **Tax-remission province scope is a real over-shoot against the tooltip's "the stricken
   provinces" promise.** Confirmed via review: `qing_pop_pressure` is a single flat COUNTRY-scope
   variable with no per-province breakdown anywhere in this codebase — so "every owned province
   with `has_city_status = yes`" is the best available proxy, but it will apply the modifier to
   every prosperous city nationwide (Canton, Suzhou, etc.) regardless of whether any famine exists
   near them, unlike the narrower, geographically-real Zhili/Shandong/Henan basin scoping the
   granary-BUILD lever uses. Accepted as a known simplification (building a real per-province
   pressure model is out of this task's scope) rather than silently presented as equivalent to that
   narrower precedent.

## Blast radius
Two functions changed (`QING_pop_relief_resettle`, `QING_pop_tax_remission`), one new modifier
definition + its loc, one GUI `is_valid` gate widened to match the effect's new joint condition.
Nothing else in the population/pressure suite, the granary pool's OTHER readers/writers, or the
tax-rate script_values themselves changes — `local_tax_modifier` is a proven, standard engine
modifier key (mirrors how every other percentage-modifier in this suite is applied), not a new
mechanic.

## Assumptions (boot-tunable, logged per the overnight doc's own ASSUMPTIONS section)
- Relief distribution amount: 150 (unchanged from the current add, now a real subtract).
- Remission duration: 365 days (one year, per the task's literal wording).
- Remission province scope: every owned city-status province (best available proxy for "the
  stricken provinces" absent a per-province pressure breakdown this task does not ask for).
