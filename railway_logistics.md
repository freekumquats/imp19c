# Countrywide Railway Network (#440) + Logistics Wiring (#441)

Branch: **merge-overnight**. Two related infrastructure tasks. Decisions, the
building→system wiring audit, and the adversarial-review outcome are recorded here.

## #441 — Wire railways / canals / granaries / depots into the logistics system

### Audit (what was already wired)
A full building→system matrix (Explore agent + hand-check) showed the four building
types are already deeply integrated into the ECONOMIC systems:
- **Railways** (`INF_railway_upgrade`): TRADE throughput, SHIPPING, MOVEMENT trade-route
  transportation svalue (`railway_bonus`, MOVEMENT_svalues.txt:9), INDUSTRY, JOBS, EDU,
  WEALTH; and `army_movement_speed = 0.1` on the building + mobilization supply.
- **Depots** (`INF_depot`): TRADE, SHIPPING (+cap), JOBS (+building-cap ×10/depot), EDU,
  mobilization supply.
- **Canals** (`INF_canal`): TRADE, SHIPPING, INDUSTRY, JOBS. Grand Canal buildings
  (`qing_grand_canal_building` 0.25, `qing_canal_depot_building` 0.10) carry
  `army_movement_speed`.
- **Granaries** (`qing_granary_building` 常平倉): food pool / price stabilisation /
  currency (se_QING_DECLINE / REVENUE / CANAL / MINISTRY).

`se_LOGISTICS.txt` is a military munitions/coal SHORTAGE-consumption layer and reads none
of the four (correctly — it is a shortage layer, not an infrastructure layer).

### The genuine MILITARY-logistics gaps (fixed)
1. **`INF_canal` had no `army_movement_speed`** — it was the only transport artery (vs
   rail, Grand Canal, canal-depot) with no movement teeth. FIX: added
   `army_movement_speed = 0.1` (00_infrastructure_buildings.txt).
2. **Canals & granaries were NOT muster-supply sources** in `se_MOBILIZATION.txt` — the
   levy-supply gate read only depot/arsenal/rail. A 常平倉 grain magazine or a Grand Canal
   at the muster is the most natural supply source of all. FIX: added `INF_canal`,
   `qing_grand_canal_building`, `qing_canal_depot_building`, `qing_granary_building` to the
   supported-levy `has_building` OR-list.

Deferred (documented, not built): adding canals to the 20 hardcoded per-TZ
`*_transportation_svalue` blocks — canals already feed trade throughput via
`TRADE_canal_bonus`; adding them to inter-zone transportation too would double-dip and is a
large balance-affecting edit. The orphan `INF_railway_upgrade_army_movement_bonus_province`
svalue (ECON_svalues.txt, zero consumers) left as-is (out of scope, deletion risk).

## #440 — Countrywide Railway Network (全國鐵路網)

### Design
Distinct from the single-line `QING_selfstr_found_rail` (which founds railways as a
CONCEPT). This is the progressive NETWORK: a repeatable Works-panel action lays
`INF_railway_upgrade` in the next most-populous unconnected core province (levying 60
treasury + 5 manpower, gated on tech_steam_locomotive + a seated Works minister finesse 7+,
mirroring the great-monument projects). The network's REACH grants escalating national
tier modifiers:
- **trunk line (幹線, ≥3)**: army_movement +0.05, build_cost −0.05, commerce +0.05
- **regional (區域網, ≥8)**: +0.10 / −0.08 / +0.10 + tax +0.05
- **national grid (全國網, ≥15)**: +0.15 / −0.12 / +0.15 + tax +0.08 + manpower +0.10 + legitimacy +0.03

Reuses the #441 wiring: every laid railway already speeds armies and counts as muster
supply, so the network's teeth are concrete; the tier modifiers are the emergent NATIONAL
layer on top.

Files: se_QING_SELFSTR.txt (effects), qing_selfstrengthening_modifiers.txt (3 tier
modifiers), QING_works_ministry_panel.txt + qing_works_ministry.gui (repeatable button),
2 loc yml. `QING_selfstr_found_rail` calls the band on completion; the quarterly governance
pulse (QING_GOV_pulse, gated on rail tech) re-applies it.

### Adversarial review (12-agent workflow) — 1 real defect, FIXED
All idioms verified PROVEN (`ROOT = { change_variable }` inside every_owned_province ↔
se_QING_MINISTRY.txt:711; add_treasury/add_manpower negatives; ordered_owned_province;
add_building_level; army_movement_speed country+province key). Refuted: no CHI-leak (pulse
is tag=CHI gated), no supply-trivialization, movement-speed stacking is intended, the
suspected founding-line double-count is not real.

**CONFIRMED defect (medium): `qing_rail_network_count` was a once-seeded MONOTONIC counter.**
It only ever incremented on the Extend button, so railways built via the ordinary
construction UI, rail gained by conquest, and rail lost to war/cession never updated it —
the tier bands drifted from the true network (under-count withholds bands; un-decremented
losses keep a national-grid bonus for rail no longer held).

FIX: made the count **authoritative** — `QING_rail_network_apply_band` now RECOUNTS from
actual rail provinces every call (`QING_rail_network_recount`: set 0 → census
every_owned_province with INF_railway_upgrade), and the band is wired into the quarterly
QING_GOV_pulse so manual builds / conquest / war losses are always reflected. The Extend
action no longer keeps a manual +1; the census is the single source of truth. This mirrors
how se_QING_MINISTRY recomputes qing_granary_count/qing_works_building_count every pulse.
The low-severity founding-line edge dissolves with it (no incremental counter remains).

All files brace-balanced (verified). CHI-gated. Committing.
