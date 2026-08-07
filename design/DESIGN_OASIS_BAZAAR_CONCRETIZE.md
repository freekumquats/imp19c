# DESIGN — Concretize the oasis bazaar: retire `qing_caravan_yarkand_market` → a real `qing_oasis_bazaar_building` (回疆巴札)

**Branch:** merge-overnight. **Status:** ✅ SHIPPED 2026-08-06 (#10A commit 0fda07d2b; caravan derive 3b6daa4d8/3052a2bba). **Scope:** CHI. #10A bespoke-entrepôt (supersedes the
inert `regional_center_of_trade` bonus shipped in `3052a2bba`). Part of the meter-concretization program
([[imp19c-concrete-over-abstract-rule]]).

## 0. Why — the problem this fixes
⚠️ **CORRECTION 2026-08-06: the earlier "trade-center branches are DEAD CODE, remove them" premise was WRONG
(verified by reading `tradezone_setup_effect`, se_TRADE.txt:920).** The setup does `random_region { limit =
{ $TRADE_ZONE$ } ordered_region_province { order_by = total_population } }` — it picks a random MEMBER REGION
of the tradezone, THEN the most-populous province of THAT region. `eastern_steppe_tradezone` includes the
**Gansu** region, and **Tarim is in Gansu** — so the center CAN land on a Tarim oasis. Levels 2-5 are live
(stamped by ECON_events upgrades, read by EE_lists/se_SHIPPING). So the `regional_center_of_trade` bonus in
`QING_caravan_oasis_trade_svalue` is **LIVE, not dead — KEEP IT.** (The prior #10A review's "always 0" claim
missed the per-region random pick. My repeating it without reading the setup was the error.) This doc no
longer touches that svalue.

The ACTUAL problem this fixes:
1. **`qing_caravan_yarkand_market` is an abstract counter** (int 0–4, +5 each to prosperity) that MODELS a
   thing that should be a real object: **the oasis bazaars/caravanserai** — the covered markets that made
   Kashgar/Yarkand entrepôts. Concrete-over-abstract: make it a real BUILDING and derive prosperity from it.

## 1. Thesis — the bazaar is a real building; prosperity counts the buildings
- **New building `qing_oasis_bazaar_building`** (回疆巴札 / oasis bazaar). Placed on oasis provinces (Dzungaria/Tarim; NO city-status requirement — §5).
- **RETIRE `qing_caravan_yarkand_market`** (the abstract counter). The 6 sites (full census, §3) migrate:
  the invest-market lever STAMPS a bazaar building; prosperity COUNTS the buildings; the panel/cap read the
  count. Abstract counter deleted; the building is the source of truth (same inversion as #8 treaty-ports).
- **Prosperity term** in `QING_caravan_recompute_target`: `+ W_bazaar × (count qing_oasis_bazaar_building over
  the oasis areas)` — replacing the `yarkand_market × 5` term. W_bazaar = 5 (reproduce the old +5/bazaar).

## 2. USER RULINGS (2026-08-06)
- **Bazaar = a BUILDING, buildable by the user.** ✅ Both hold via the annexation arc (§2a).
- **Aqsaqal = a diplomatic CONCESSION (flag), NOT a building** — it stays `qing_caravan_aqsaqal_granted`, a
  merchant-draw lever (Kokand consul over the Andijani merchants, 1832). It is NOT concretized to a building;
  instead it modulates bazaar THROUGHPUT (§4).

### §2a — buildability + the subject-ownership reality (verified)
⚠️ **At 1763 EVERY Tarim (XNG) + Dzungaria (ILI) oasis province is SUBJECT-held; ZERO are CHI-direct.** In
Imperator the player builds only in provinces they OWN, so the bazaar is NOT province-menu-buildable early.
This is NOT a contradiction — the whole #367/Ili tree is CHI **progressively ANNEXING** ILI/XNG
(`QING_xj_integrate_fully` → "a normal province like any interior one"), so the oases BECOME CHI-direct as
the tree advances → the bazaar becomes province-menu-buildable then (historically right: bazaars flourished
once Xinjiang was made a full province, 1884). So buildability is TWO-TRACK:
- **Early (oases still subject):** the player builds bazaars via the EXISTING country-scope lever
  `QING_caravan_invest_market` (the caravan panel button, treasury −40) — which STAMPS the building on an
  oasis via area-iteration. And this lever ALREADY advances c:ILI integration — it drives the annexation it
  depends on. ⚠️ **FEASIBILITY (review CRIT/HIGH — was mis-cited): the "proven QING_xj_plant_tuntian pattern"
  claim was WRONG — plant_tuntian uses `add_province_MODIFIER` (no potential gate, always applies), NOT
  `add_building_level`. The real building-on-subject-land precedent is `QING_seed_frontier_building`
  (se_QING_BUILDINGS.txt:494-511): `add_building_level` on a hardcoded `p:$P$` with an owner-OR-subject guard.
  So `area:Tarim + random_area_province + add_building_level` (area-iterated building placement) is
  PLAUSIBLE (area-iter is owner-independent for modifiers; add_building_level is province-scope; the corrected
  §5 potential passes on XNG-via-ILI) but UNATTESTED — BOOT-PROBE it (or oracle-check) before build, do not
  call it proven. If it fails, fall back to the proven form: iterate to pick a target oasis, save the scope,
  then `<prov> = { add_building_level }`.**
- **Late (oasis CHI-annexed):** the building's `potential` (oasis area + `owner = CHI` + tech) opens the
  normal province BUILD MENU. Same building, now directly buildable.
Both are "the user builds it"; the lever is the early path, the menu the late path.

## 3. Full census — every `qing_caravan_yarkand_market` site (6, verified) → migration
| Site | Now | Becomes |
|---|---|---|
| `se_QING_CARAVAN.txt` header comment | doc line | reword to the building |
| `se_QING_CARAVAN.txt` init `set = 0` | seed counter | **DELETE** (no counter) |
| `QING_caravan_recompute_target` `mkt_tmp = yarkand_market ×5` | counter term | `+ W_bazaar × (count bazaar buildings over oasis areas)` |
| `QING_caravan_invest_market` gate `< 4` + `change +1` | cap + increment | STAMP `qing_oasis_bazaar_building` on an oasis province lacking one (area + random_area_province); cap = "an un-bazaared oasis province exists" (NO city gate) |
| `QING_caravan_panel.txt` `is_valid < 4` | button enable | enable while an un-bazaared oasis province exists |
| `gui/qing_caravan.gui` GetVariable display | show counter | show the building count (svalue or a cached read) |
There are NO external readers — fully self-contained in the caravan subsystem.

## 4. Aqsaqal as a throughput MULTIPLIER (not a flat +8)
Today aqsaqal is a flat `+8` to prosperity (`:121`). Keep it a flag, but reframe as a **multiplier on the
bazaars' throughput** (the concession draws the Andijani merchants THROUGH the bazaars): e.g. the bazaar term
becomes `W_bazaar × bazaar_count × (aqsaqal ? 1.5 : 1.0)` — so the concession's value SCALES with how many
bazaars exist (a concession with no markets draws little; with a full bazaar network it swells the volume).
This makes aqsaqal concrete-adjacent (it acts on the real buildings) without making it a building. [If a flat
term is preferred for simplicity, keep +8 — but the multiplier is the truer model. PLACEHOLDER-decide.]

## 5. The building def (mirror the seed-only academy pattern, adapted for buildable + subject-land)
```
qing_oasis_bazaar_building = {
    # 回疆巴札 — the covered oasis market/caravanserai; the entrepôt infrastructure of the Silk-Road oases.
    local_state_trade_routes = ...   # the REAL commerce key (100+ uses); + local_tax_modifier /
    local_tax_modifier = ...         # local_middle_strata_output / local_monthly_civilization as fits.
    local_middle_strata_output = ... # (review LOW: `local_commerce_value` is NOT a valid key — do not use.)
    cost = 40   time = ...
    max_amount = 1               # one bazaar per oasis province (proven cap key — NOT max_level; see the yamen fix)
    potential = {
        # ⚠️ CRITICAL (review): the oases are SUBJECT-owned (XNG=uighur, ILI=manchu), NOT jurchen/chinese
        # DIRECTLY. An owner-only culture check silently DROPS the building on all Tarim provinces (incl.
        # Kashgar 2700) — add_building_level respects potential. MUST include the owner-OR-OVERLORD branch,
        # the PROVEN pattern from qing_great_mosque_building (qing_religion_buildings.txt:253-277, whose
        # comment documents exactly this: Kashgar 2700 owned by XNG, XNG's overlord ILI is manchu → passes;
        # overlord is NOT recursive, single-level only — XNG→ILI works because ILI is manchu at one level).
        OR = {
            owner = { OR = { country_culture_group = jurchen  country_culture_group = chinese_group } }
            owner = { exists = overlord  overlord = { OR = { country_culture_group = jurchen  country_culture_group = chinese_group } } }
        }
        # oasis gate: use is_in_region (PROVEN in building potentials — great_mosque/military_colony;
        # is_in_area is UNATTESTED in a building potential, review MED). Region Gansu (Tarim) + Turkestan
        # (Dzungaria) is broader than the two areas, but the prosperity COUNT scopes to area:Dzungaria/Tarim
        # (owner-independent, proven), so only oasis-area bazaars are credited regardless of the menu gate.
        OR = { is_in_region = Gansu  is_in_region = Turkestan }
        # ⚠️ NO has_city_status gate (USER 2026-08-06): a bazaar sat on the TRADE ROAD — Silk-Road markets
        # were at waystations, not only chartered cities. Same ruling as the yamen. (province-menu build opens
        # only when CHI owns the oasis — the late/annexed track; early = the lever.)
    }
    allow = { owner = { invention = <appropriate tech> }  sufficient_job_slots = yes }
}
```
⚠️ Modifier keys: use `local_state_trade_routes` (the real commerce key) + tax/output/civ — NOT
`local_commerce_value` (not a valid key, review LOW). Nearest template = `qing_guild_hall_building`
(`qing_fiscal_buildings.txt:108`). Icon: new `qing_oasis_bazaar_building.dds` (placeholder from an existing
commerce icon; bespoke art owed).

## 6. Prosperity count — area-iterated, owner-independent (the CRIT-1 discipline)
The count MUST use `area:Dzungaria`/`area:Tarim` + `every_area_province { has_building = qing_oasis_bazaar_
building }`, NOT `every_owned_province` (the oases are subject-held → owned-scan returns 0, the #91 blocker).
Sum into the prosperity target as a script_value (like `QING_caravan_oasis_trade_svalue`) or an effect
scratch. Counts bazaars whether the oasis is still subject-held (seeded/lever-built) or CHI-annexed.

## 7. The trade-center branches STAY (correction — see §0)
⚠️ **RESOLVED by reading se_TRADE.txt:920: the branches are LIVE, not dead — DO NOT remove them.** The
tradezone center is placed per-random-member-region, and Gansu (→ Tarim) is a member of eastern_steppe, so a
Tarim oasis CAN carry `regional_center_of_trade`. `QING_caravan_oasis_trade_svalue` is left UNTOUCHED by this
doc. (Fix only the one stale inline comment that says both oases are in western_steppe — Tarim is in Gansu →
eastern_steppe — a doc nit, no code change.)

## 8. 1763 opening + seed — ⚠️ the seed pushes the opening toward the ≥55 ultimatum gate (review MED)
- ⚠️ **The old counter opens at 0 markets → +0 at 1763.** Seeding 2 bazaars adds `2×W_bazaar (5) = +10`,
  pushing prosperity from ~45 toward **~55 — exactly the Kokand-ultimatum trigger** (`se_QING_CARAVAN.txt:249`).
  So EITHER: (a) DON'T seed at 1763 (opens at 0 bazaars like the old counter — cleanest, the player builds
  them), OR (b) seed but re-pin S (oasis-trade scale) / W_bazaar so the opening stays sub-55. Prefer (a)
  unless a historical starting bazaar network is wanted; if (b), show the arithmetic against ≥55/≥40.
- **Seed by AREA, not by hardcoded ID (review LOW): Kashgar = prov 2700 (confirmed) but YARKAND has no
  locatable province ID.** So if seeding, use `area:Tarim`/`area:Dzungaria` + `random_area_province` (N times)
  via a subject-tolerant placement, not `QING_seed_frontier_building { P = <Yarkand> }`.

## 9. Build checklist (ONE commit) — with the review-round fixes folded
0. **Both former "unknowns" RESOLVED by reading (no boot needed):** (a) building-on-subject-land is PROVEN —
   qing_military_colony_building seeds on Urumqi 2930 (ILI-owned) via QING_seed_frontier_building; use the
   proven scope-pick form (iterate to pick the oasis, save_scope, `<prov> = { add_building_level }`). (b) the
   trade-center branches are LIVE (§7) — leave them untouched.
1. Define `qing_oasis_bazaar_building`: `max_amount = 1`; **owner-OR-OVERLORD potential** (§5 CRITICAL, copy
   great_mosque — owner-only silently drops on XNG-held Tarim incl. Kashgar) + `is_in_region = Gansu/Turkestan`
   (NOT is_in_area — unattested in a building potential); NO city gate; real modifier keys
   (`local_state_trade_routes` etc., NOT `local_commerce_value`); allow tech. + loc + tooltip + icon.
2. `QING_caravan_invest_market`: stamp the building instead of `yarkand_market +1`. ⚠️ **Gate BOTH the cap-check
   AND the random pick on POTENTIAL-ELIGIBLE + un-bazaared oasis provinces** (owner-OR-overlord + region + NOT
   has_building) so the −40 treasury is NOT charged for a silently-dropped placement (review MED). Keep the
   treasury cost + the ILI integration advance.
3. `QING_caravan_recompute_target`: replace the `yarkand_market ×5` term with `W_bazaar × (area-counted bazaar
   buildings)`; fold the aqsaqal multiplier (§4). Also write a **cached `qing_caravan_bazaar_count` var** here
   each recompute — the GUI can't read a script_value (review MED).
4. Delete the `yarkand_market` init seed + header; retire the var. Panel `is_valid` (gate on an eligible
   un-bazaared oasis existing) + GUI display read the new cached `qing_caravan_bazaar_count`.
5. 1763 seed: prefer NO seed (opens at 0 bazaars like the old counter, avoids the ≥55 gate — §8); if seeding,
   by AREA (not Yarkand-by-ID, which has no province) + re-pin so the opening stays sub-55.
6. Leave `QING_caravan_oasis_trade_svalue` untouched (the trade-center branches are LIVE — §7); optionally fix
   the one stale western_steppe comment.
7. Review gates: **owner-OR-overlord potential (not owner-only — CRIT)**; count via area-iteration NOT
   every_owned_province; `max_amount` not `max_level`; real modifier keys (`local_state_trade_routes`); lever
   gated on a potential-eligible pick (no money-sink); GUI reads a cached var not an svalue; no external
   `yarkand_market` reader left; 1763 opening vs ≥55/≥40; brace/quote/BOM; boot-crash review.
