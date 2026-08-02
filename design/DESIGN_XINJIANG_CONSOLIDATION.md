# #367 — Xinjiang Consolidation Arc (新疆 consolidation, 1763)

The 1763 **consolidation** layer for the New Frontier (新疆), built to LAYER on the existing
Xinjiang machinery, never to duplicate it.

## What already exists (do NOT duplicate)

1. **se_QING_ILI.txt** — the LATE-QING (1874-81) **Ili crisis set-piece** (海防塞防 debate →
   Yaqub-Beg reconquest → Chonghou/Zeng-Jize Ili diplomacy). It OWNS:
   - `qing_xinjiang_control` (0..100) — the grip on the New Dominion.
   - `QING_ili_apply_control_band` (called every pulse from `QING_ili_pulse`) — keeps the
     country grip modifiers (`qing_xinjiang_grip_firm` / `_lost`) in step with the meter.
   - `QING_ili_apply_prov_band` (called at discrete stage transitions) — stamps the
     Dzungaria/Tarim province bands (`qing_xinjiang_prov_secured` / `_contested`).
   - Gated on `qing_rebel_dungan` (fires only after the 1860s Dungan revolt) — in a 1763 game
     this set-piece stays dormant unless the far west later collapses.
2. **se_QING_AMBAN.txt** — the 駐紮大臣 resident lifecycle (post/recall/evaluate, Lifan-Yuan
   supervision, the clash/gone-native/turnover events) on the Inner-Asian subjects.
3. **se_QING_FRONTIER.txt** — the #346 frontier-garrison overlay (將軍 banner garrisons on the
   ILI/XNG autonomous-governorship subjects, the War-Ministry↔Lifan-Yuan turf war).

## What #367 adds (the consolidation layer)

The historical arc between conquest (1759) and the eventual test (Jahangir Khoja 1826): the
player-emperor's LEVERS to make the new frontier pacified, integrated and self-sustaining — or
to bungle it into revolt. #367 FEEDS `qing_xinjiang_control` (which the ILI pulse then bands
onto the map for free) and folds the frontier's health into the **Lifan Yuan** office-holder,
the 理藩院 that historically governed Xinjiang.

### Concrete on-map objects (concrete-over-abstract rule)

- **Begs (伯克)** — real Uighur characters minted onto the **XNG (Kashgaria/Altishahr)** subject
  (`primary_culture = uighur`, `religion = sunni`, the setup's own "Beg appointed from Uighur
  nobles by a Qing amban"). Held in a corps list `qing_xj_begs` on CHI, rebuilt each pulse
  excluding office-holders. A loyal, capable beg corps holds the south; a disloyal/empty one
  invites the khoja.
- **Tuntian military colonies (屯田)** — a concrete count `qing_xj_tuntian` of state farms
  planted in **Dzungaria** (the genocide-emptied north, open to colonization). Each raises
  control + tightens ILI's integration. Backed by a real province modifier
  `qing_xj_tuntian_colony` on a Dzungaria province.
- **Xiexiang silver subsidy (協餉)** — the interior-province silver stipend that kept Xinjiang
  solvent. A country modifier `qing_xj_xiexiang` (a treasury drain that buys control/stability),
  toggled by the player; historically permanent, so cutting it erodes the grip.

### Levers (panel)

1. **Plant a Tuntian Colony (屯田)** — spend treasury; +control, +1 `qing_xj_tuntian`, stamp a
   Dzungaria province, advance ILI integration a step. Gated on treasury + an unstamped
   Dzungaria province held by CHI or ILI.
2. **Appoint a Beg (伯克)** — mint a loyal Uighur notable onto XNG (cap 5). +control. Gated on
   XNG being a live subject + corps below cap.
3. **Discipline a Beg (懲辦)** — cashier a venal/disloyal beg (corrupt / low affinity). Cleans
   the corps, small control cost now for stability later. Row action; gated on a venal target.
4. **Ship the Xiexiang Subsidy (協餉)** — toggle the silver stipend on: treasury drain modifier
   + control/stability lift. Gated on treasury.

### The fold (into the Grand Council office-holder)

Per the standing directive — *every Qing bureaucracy's performance determines its leader's
standing on the Grand Council* — Xinjiang consolidation folds into the **Lifan Yuan Grand
Director** (`qing_office_lifanyuan_holder`, `qing_min_perf_lifanyuan`). The recompute
`QING_xj_recompute_consolidation` computes a 0..100 `qing_xj_consolidation` score from control +
beg loyalty + tuntian depth + xiexiang, and nudges `qing_min_perf_lifanyuan` toward it (the
Court of Colonial Affairs is judged on how well the New Dominion is held). This is the SAME
office the amban coverage already feeds, so the two are consistent, not double-counted (the
amban coverage scores STAFFING; #367 scores the frontier's HEALTH).

### Risk (khoja revolt)

When `qing_xinjiang_control` is low AND the beg corps is disloyal/empty, the White-Mountain
khojas stir (the 1826 Jahangir payoff of poor consolidation). The pulse rolls a low chance to
fire `qing_xinjiang.1` — a revolt-scare event that (player choice) either spends to suppress
(control back up) or lets it fester (control down, ethnic tension up, and at the extreme backs
an **XNG breakaway** — but ONLY from Kokand/a neighbouring Turkic power, per the separatism-
backer standing rule, never a far-flung one).

## Idioms locked in (all proven)

- Meter nudge: `QING_DECLINE_nudge = { var = qing_xinjiang_control  amount = N }` (self-inits,
  clamps 0..100 — the same helper se_QING_ILI uses).
- Beg mint: `create_character` (#90 — no modifiers inside; culture = uighur; religion = sunni;
  finalize `move_country = XNG` / `set_variable` / `set_as_minor_character` in the saved scope),
  mirroring `QING_amban_post`.
- Corps rebuild: `every_character { limit = { has_variable = qing_is_xj_beg  is_alive = yes
  employer = c:XNG  NOT = { has_variable = qing_office_held } } }` (the #362-R2 exclusion).
- Province stamp: `area:Dzungaria = { random_area_province { limit = {...} add_province_modifier } }`
  (owner-independent area iteration — the proven idiom se_QING_ILI uses).
- Integration: `SUBJ_QING_advance_integration = { steps = 1 }` with `scope:target = c:ILI`.
- LOG: static messages only (#253). Brace balance 0. GUI text wraps.
- Panel: a Grand-Council-clone L4 window (scope = country scripted_guis, `ai_is_valid = no`,
  opened from a button in government_view.gui). Since all scripted_guis are country-scope,
  employer=ROOT resolves to CHI (the #362 root-rebinding bug does not apply).

## Files

- `common/scripted_effects/se_QING_XINJIANG.txt` — init / recompute / the four levers / the
  khoja-risk pulse / mint / remove-on-death.
- `common/scripted_guis/QING_xinjiang_panel.txt` — the panel scripted_guis.
- `gui/qing_xinjiang.gui` — the L4 window.
- `common/modifiers/qing_xinjiang_consol_modifiers.txt` — xiexiang + tuntian-colony modifiers.
- `events/imp19c_mod_events/qing_xinjiang_events.txt` — the khoja-revolt-scare event.
- `localization/english/qing_xinjiang_l_english.yml` — all loc + beg nicknames.
- Wiring: init on_action, `QING_xj_pulse` in the governance pulse, remove-on-death hook, open
  button in government_view.gui.
