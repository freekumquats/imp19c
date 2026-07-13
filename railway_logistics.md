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

3. **Canals were NOT in the inter-zone trade-route transportation svalue.** Initially
   deferred as "double-dip", but that reasoning was WRONG (corrected on review): railways
   feed BOTH the intra-zone throughput channel (`TRADE_railway_bonus ×2`, into
   `TRADE_governorship_infrastructure_capacity_svalue`, consumed live by
   se_GLOBALTRADE_split) AND the inter-zone transportation channel (`railway_bonus` in
   MOVEMENT_svalues) — and that is NOT double-dipping, because the two channels model
   different things (throughput capacity within a zone vs. connection cost between zones).
   A canal is a genuine inter-regional artery (the Grand Canal moved grain across regions),
   so by parity it belongs in both. FIX: added a `canal_bonus` svalue (num_of_INF_canal ×
   0.15, a touch below rail/port's 0.2) and a canal leg + canal qualifying-gate to all 22
   per-TZ `*_transportation_svalue` blocks (MOVEMENT_svalues.txt), mirroring the port leg
   (gated on has_building, since a canal is point infrastructure like a port, not
   feeding intra-zone throughput — matching railways.

### Canal refinements (post-review, user-directed)
- **Gating corrected**: a canal is a PATH, not a fixed point, so the canal leg is gated on
  route connectivity (`any_neighbor_province = { has_road_towards = PREV }`) like the
  railway leg — NOT on `has_building` like the port leg (my first pass wrongly copied the
  port pattern). The redundant `has_building = INF_canal` I'd added to the outer qualifying
  gate was reverted (a connected canal province is already caught by the road clause).
- **Canal bonus > railway bonus**: water carriage was historically the cheapest bulk
  transport (a barge far out-hauled early rail per ton-mile), so `canal_bonus` is weighted
  **0.3**, ABOVE `railway_bonus`/`port_bonus` (0.2). The canal is the STRONGER artery.
- **Costlier + slower to build**: a canal must be hand-dug over a long corvee haul. The
  build system has no manpower-cost field (the great monuments spend manpower via an event
  effect, and there is no on_building_constructed hook to deduct it), so the digging burden
  is expressed as a higher money cost AND a much longer build time: `INF_canal` cost 50→90,
  time 180→540 (3× the railway's 180). So canals move goods better but are dear and slow to
  dig — the intended trade-off.

### Post-review fix: clamp the inter-zone connection svalue (min = 0)
The canal review (12-agent workflow) confirmed the canal changes themselves are sound
(scope/idiom proven, build-time within precedent, the canal leg is actually the
better-behaved term — it adds 0 where absent, unlike the railway leg's per-province +1
base). But it surfaced a **pre-existing** correctness gap it shares: each of the 462
`X_to_Y_svalue` connection blocks is `(100 − X_transportation − Y_transportation) × 0.01`
with NO clamp, and that value feeds `se_PURCHASE` as a transport COST gated only on
`has_variable`, never on sign. In a rail/province-saturated late game the two zones'
transportation totals can exceed 100, driving the connection cost NEGATIVE — nonsensical
subsidised long-distance shipping. This is dominated by the pre-existing `railway_bonus`
`value = 1` per-province base (reachable with zero canals); the canal leg contributes ~10%
and only nudges it. Fix (user-directed): added `min = 0` to all 462 connection svalues so
shipping cost floors at free and can never go negative. Purely protective — changes nothing
in the normal regime, only clamps the pathological tail. MOVEMENT_connection_svalues.txt,
brace-verified 462/462.

The orphan `INF_railway_upgrade_army_movement_bonus_province` svalue (ECON_svalues.txt,
zero consumers) left as-is (out of scope, deletion risk).

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
