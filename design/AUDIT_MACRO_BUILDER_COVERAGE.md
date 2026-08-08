# Audit — Macro Builder building coverage (#31)

**Date:** 2026-08-07. **Status:** AUDIT COMPLETE; fix in progress.
**Rule basis (memory `imp19c-macro-builder-mechanic`):** the macro builder is a HAND-WIRED list.
A building appears only if (1) it is in the allowlist `gfx/interface/macro_builder/config/00_default.txt`
`includes {}`, (2) it has a `macro_build_item_<key>` widget in `gui/macro_builder_view.gui`, and (3)
its `potential` is EMPTY or country-independent — the macro builder evaluates `potential`
PROVINCE-INDEPENDENTLY, so ANY province-scoped trigger in `potential` (has_city_status, is_in_region,
trade_goods, owner-country checks) HIDES the building from the macro list. Province/country gates
belong in `allow` (evaluated per-province in both builders → greys correctly). Event-only buildings
(`allow = always = no`) are correctly ABSENT (they can populate no build menu).

## Method
Enumerated all 68 top-level building defs in `common/buildings/*.txt`; extracted the macro allowlist
(62 entries); computed player-buildable (has `cost`/`allow`) defs NOT in the allowlist (23); then read
each one's full `potential` + `allow` to classify.

## Classification of the 23 not-in-allowlist buildings

### A. CORRECTLY EXCLUDED — leave out (no change)
| Building | Reason |
|---|---|
| qing_grand_canal_building | `allow = always = no` — event/capstone-placed only |
| qing_great_wall_building | `allow = always = no` — event/capstone-placed only |
| qing_hanlin_academy_building | `potential = always = no` — not player-buildable |
| qing_ancestral_temple_building | `allow = always = no` — unique landmark, one-per-region, event-placed |
| qing_dujiangyan_building | `allow = always = no` — unique landmark |
| qing_guozijian_building | `allow = always = no` — unique landmark |
| qing_temple_of_heaven_building | `allow = always = no` — unique landmark |
| qing_bailudong_academy_building | `potential = has_variable qing_is_bailudong_site` — single fixed site |
| qing_yuelu_academy_building | `potential = has_variable qing_is_yuelu_site` — single fixed site |
| row_manufactory_building | `potential = NOT chinese_group` — ROW building, not for Qing player |
| row_plantation_building | `potential = NOT chinese_group` — ROW building, not for Qing player |

### B. GENUINELY PLAYER-BUILDABLE, MISSING — ADD (allowlist + GUI item), potential already macro-safe
| Building | potential | allow |
|---|---|---|
| qing_customs_house_building | (none) | tech_monetary_theory + slots |
| qing_selfstr_wonder_building | (none) | tech + modifier + civ≥40 + city + slots |
| qing_frontier_colony_building | always=yes | always=yes |
| qing_frontier_fort_building | always=yes | always=yes |
| qing_yamen_building | NOT has_building self | tech_central_administration + slots |
| qing_shuyuan_building | NOT has_building self | tech_education + slots |

(These have EMPTY or macro-safe potential — the `NOT has_building self` self-exclusion is
province-local and harmless in the macro list. Just need allowlist + GUI item.)

### C. PLAYER-BUILDABLE but HIDDEN by a province gate IN `potential` — ADD + migrate gate to `allow`
Each duplicates its province gate in BOTH `potential` and `allow`; the `potential` copy is what hides
it from the macro list. Fix: EMPTY the `potential` (the `allow` copy still enforces the gate
per-province in both builders) + add to allowlist + GUI item.
| Building | potential (to empty) | allow (keeps the gate) |
|---|---|---|
| military_depot_building | has_city_status | has_city_status + slots |
| qing_embassy_building | has_city_status | has_city_status |
| qing_foreign_works_building | has_city_status | has_city_status |
| qing_mission_cathedral_building | has_city_status | has_city_status + slots |
| qing_treaty_port_building | has_city_status | has_city_status |
| qing_oasis_bazaar_building | owner-culture OR overlord-culture | tech_urbanization + slots |

**CAUTION on C:** `military_depot_building` is a VANILLA/upstream military building — verify its
province-window behavior is unchanged by the potential→allow move (the gate is duplicated, so
emptying potential is behavior-preserving in the province window, and only ADDS macro visibility). The
`qing_treaty_port` / `foreign_works` / `mission_cathedral` / `embassy` are the #FOREIGN family — confirm
they are player-built (allow = has_city_status, a real gate) and not exclusively event-created before
adding (memory note: SOME foreign buildings are event-created via add_building_level; those must NOT be
added). Re-verify each against se_QING_FOREIGNBUILD.txt before migrating.

## Fix plan (verified batches, each reviewed)
1. Batch B (6): allowlist + GUI item only — lowest risk, potential already safe.
2. Batch C (6): potential→allow migration + allowlist + GUI item — verify each is player-built first;
   military_depot needs an upstream-behavior check.
Each building needs, per the 3-part rule: (1) allowlist line in config/00_default.txt, (2)
`macro_build_item_<key> = {}` in the right section blockoverride of macro_builder_view.gui.
