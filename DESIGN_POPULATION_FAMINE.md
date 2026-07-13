# DESIGN — Population / Migration / Famine Deep Model (人口壓力 / 人地矛盾 / 饑荒) — task #369

**Branch:** merge-overnight. **Status:** BUILDING.
No oracle probe needed — every primitive is proven in-repo (see §3): the shared clamped-counter
idiom (`QING_DECLINE_nudge`), banded country modifiers, `total_population` at country scope
(`slave_revolt_svalue` 00_event_values.txt:113, DIPLOMACY_svalues.txt:527), the migration
government levers (`migr_gov_push`/`migr_gov_pull` in MIGRATION_svalues.txt), and the scripted_gui
meter-panel pattern (#366 opium). The once-only event offered-flags are set in each event's own
`immediate` (the #366/#368 flag-leak fix), NOT in the pulse.

## 1. Thesis — a STANDING Malthusian pressure driver over the EXISTING one-shot boom

The mod already models the demographic story in PIECES, but each is a one-shot or a static field:

- **`qing_migration.20`–`.23`** (qing_frontier_migration_events.txt) — the New World crop boom fires
  ONCE, forks ONCE to blessing (`.22`) or Malthusian crisis (`.23`) off a snapshot of dynastic
  health, and is done. It plants `qing_migr_crop_boom` / `qing_migr_overpopulation` and pushes the
  heartland once (`QING_COLON_heartland_push`). There is no *continuing* pressure that mounts,
  relaxes, and re-bites as the game runs.
- **`qing_granary_stock`** (0..100, se_QING_DECLINE.txt:25) + the concrete `qing_granary_building`
  (QING_DECLINE_granary_concrete) — a famine RESERVE, built in good years and eaten in bad, but it
  is not *driven* by demographic pressure; it just drifts.
- **`se_MIGRATION.txt`** — a complete bottom-up migration engine reading `MIGRATION_push_province`
  / `MIGRATION_pull_province`, with `migr_gov_push`/`migr_gov_pull` government levers. But nothing
  standing tells it "the heartland is overcrowded THIS decade" — only the one-shot crop event does.
- **`qing_sect_pressure`** — raised ad hoc by famine/unrest events, but not by a persistent
  overpopulation signal.

The genuine gap (the concrete-over-abstract + layer-don't-duplicate house rules) is a **standing
population-pressure meter** — `qing_pop_pressure` (0..100, 人口壓力 / 人地矛盾) — that continuously
reads the realm's crowding (population outrunning land), MOUNTS with the boom and involution,
RELAXES with New World crops / frontier resettlement / granary relief, and continuously COUPLES the
existing pieces: it drives the migration heartland-push, feeds `qing_sect_pressure` (the
famine→rebellion linkage: White Lotus 1794, Taiping 1850), and drags the Board of Revenue's
performance. This is Hong Liangji's 洪亮吉 治平篇 (c.1793) thesis — "China's Malthus", predating
Malthus — made into a live meter.

## 2. The Grand-Council fold — the Board of Revenue (戶部) perf drag (a REAL per-office fold)

Unlike the Harem/Upper Study/Court-Intrigue (dynastic institutions that fold transitively via
`qing_dynastic_harmony`), population-pressure is a matter of STATE ADMINISTRATION, and it folds into
a real Grand Council office: the **Board of Revenue (戶部)**, whose `QING_ministry_recompute_perf_revenue`
(se_QING_MINISTRY.txt:477) already scores granary coverage, salt, currency stress, and corruption.
The 戶部 historically held the 黃冊 (Yellow Registers, the population census) and the 常平倉
(ever-normal granaries) — the two instruments of demographic management — so a realm buckling under
人地矛盾 IS a Board of Revenue failure. #369 adds ONE new term (f) to that perf function:

```
# (f) POPULATION PRESSURE DRAG — the 人地矛盾 the Board is failing to relieve.
#     subtract pop_pressure/8 (0..-~12 at the rails), guarded on the var existing.
```

This is the same shape as the existing (d) currency-stress and (e) corruption drags. NO new fold
machinery — it rides the Revenue perf that `QING_council_perf_accumulate` already reads into
`qing_council_eff_target`.

## 3. Proven primitives (all verified in-repo — NO oracle needed)

- **The meter** — the shared clamped 0..100 counter idiom `QING_DECLINE_nudge = { var = X amount = N }`
  (se_QING_DECLINE.txt:33), initialised in `QING_DECLINE_init`. `qing_pop_pressure` joins the existing
  counter family (corruption/sect/currency/granary), so it is banded and read exactly like them.
- **Population read at country scope** — `total_population` reads directly at country scope
  (`slave_revolt_svalue` 00_event_values.txt:113–116; `DIPLOMACY_svalues.txt:527`). The pressure
  target is derived from population vs a carrying baseline (see §4), all cached O(1) reads.
- **Banded country modifiers** — `qing_pop_pressure_*` bands added/removed in `QING_DECLINE_apply_bands`
  exactly like `qing_currency_stress_*` (the proven band-swap: remove the family, add the current one).
- **Migration coupling** — `QING_COLON_heartland_push`/`QING_COLON_clear_heartland_push`
  (se_QING_COLON.txt) already set/clear `migr_gov_push` on the crowded core, which
  `MIGRATION_push_province` reads. #369's pulse calls these off the pressure band (high pressure →
  push the heartland; relieved → clear).
- **Frontier pull** — `QING_COLON_apply_frontier_pull` sets `migr_gov_pull` on the frontier (屯田 /
  闖關東 / 移民實邊) — the resettlement safety valve.
- **Sect coupling** — `QING_DECLINE_nudge = { var = qing_sect_pressure amount = N }` (proven).
- **The scripted_gui meter panel** — cloned from `QING_opium_panel.txt` / `qing_opium.gui` (#366):
  a description, the pressure bar, the granary-reserve bar, and lever buttons, each `is_valid`
  mirroring its effect's own guard.
- **Relief buildings** — `add_building_level = qing_granary_building` (QING_DECLINE_granary_concrete,
  proven). The relief lever tops up `qing_granary_stock` (proven `QING_DECLINE_nudge`).

## 4. The pressure model (`QING_pop_recompute_target` → `qing_pop_pressure`)

A quarterly recompute writes a **target** (not a snapshot swap — the counter EASES toward the target
so the meter has hysteresis, matching the currency-stress design). The target sums:

- **CROWDING (the core driver)** — the realm's `total_population` vs a carrying baseline. High Qing
  China is already crowded; the target rises as population grows past the baseline. Read as a scaled
  `total_population` term with a floor/ceiling so it sits in a sane 0..~70 range at 1763 numbers.
- **+ INVOLUTION** — if the New World crop boom has fired (`has_variable = qing_newworld_crops`) but
  NOT resolved to the golden path, add pressure (more mouths on the same marginal land — 內卷).
- **+ FAMINE STRESS** — low `qing_granary_stock` (< 30) adds pressure (no reserve against the next
  bad harvest); high stock (>= 60) subtracts a little (the state can feed the crowd).
- **− RELIEF VALVES** — an active frontier pull (`has_variable = qing_frontier_resettlement`) and the
  golden crop path (`qing_migr_crop_boom_golden` active) subtract pressure (the safety valves work).

`qing_pop_pressure` then eases 1/4 of the way toward the target each pulse (the proven ease idiom).

## 5. The pulse (`QING_pop_pulse`, quarterly, from QING_GOV_pulse after QING_princes_pulse)

1. `QING_DECLINE_init` (idempotent — ensures `qing_pop_pressure` exists).
2. `QING_pop_recompute_target` → ease `qing_pop_pressure` toward the target.
3. **Couple into migration**: pressure >= 60 → `QING_COLON_heartland_push` (the crowded core sheds
   people to the frontier); pressure < 35 → `QING_COLON_clear_heartland_push` (the pressure is off).
4. **Couple into sects**: pressure >= 70 → nudge `qing_sect_pressure += 2` (the landless feed the
   millenarian sects — the historical White Lotus / Taiping recruiting ground).
5. **Offer the crisis event** once pressure first crosses the danger band (>= 65), player-only, the
   offered-flag set in the event's own immediate.

## 6. Player levers (L4 panel + events)

- **RELIEF & RESETTLEMENT (賑濟移墾)** — spend treasury to relieve a famine: top up `qing_granary_stock`,
  cut `qing_pop_pressure` and `qing_sect_pressure`, and open a frontier pull (`migr_gov_pull` via
  `QING_COLON_apply_frontier_pull`) so the surplus resettles (闖關東 / 移民實邊). The 以工代賑 work-relief.
- **TAX REMISSION (蠲免)** — the classic imperial mercy: cut `qing_pop_pressure` + a stability lift at
  a treasury cost (forgone land tax). Eases the immediate crisis, does nothing structural.
- **PROMOTE FRONTIER SETTLEMENT (移民實邊)** — a standing policy: open/refresh the frontier pull and set
  `qing_frontier_resettlement` (a relief valve the target reads), at a prestige/admin cost. The
  durable safety valve, vs the one-shot relief.
- **DO NOTHING (聽其自然)** — the Hong Liangji fatalism: no cost, pressure and sects mount.

## 7. Events (namespace qing_population)

- `.1` **THE MEMORIAL ON POPULATION (治平之憂)** — Hong Liangji's warning, offered when pressure first
  turns dangerous: RELIEVE (賑濟移墾) vs REMIT TAXES (蠲免) vs PROMOTE RESETTLEMENT (移民實邊) vs
  LET NATURE TAKE ITS COURSE (harmony/sect risk).
- `.2` **FAMINE IN THE PROVINCES (歲饑)** — offered when pressure is high AND granary reserves are
  exhausted: OPEN THE GRANARIES (賑災, costly, big relief) vs WORK-RELIEF (以工代賑, cheaper, resettles)
  vs the throne cannot respond (a hard sect + stability hit — the road to rebellion).

## 8. File list

- NEW `common/scripted_effects/se_QING_POPULATION.txt` — init hook, target recompute, the pulse, the
  four levers.
- NEW `events/imp19c_mod_events/qing_population_events.txt` — .1 the memorial, .2 the famine.
- NEW `common/scripted_guis/QING_population_panel.txt` + `gui/qing_population.gui` — the L4 panel
  (pressure meter + granary reserve + the four lever buttons).
- NEW `localization/english/qing_population_l_english.yml`.
- NEW `common/modifiers/qing_population_modifiers.txt` — the `qing_pop_pressure_*` bands.
- EDIT `se_QING_DECLINE.txt` (init `qing_pop_pressure`; add the `qing_pop_pressure_*` band-swap to
  `QING_DECLINE_apply_bands`), `se_QING_GOVERNANCE.txt` (call `QING_pop_pulse` in `QING_GOV_pulse`
  after `QING_princes_pulse`), `se_QING_MINISTRY.txt` (add the (f) pop-pressure drag to
  `QING_ministry_recompute_perf_revenue`), `government_view.gui` (open button).
