# Overnight Build #2 — Buildings, Trade Goods & Production Overhaul (2026-07-08)

**Author:** freekumquats · **Branch:** develop · **Task IDs:** #179–#189
**Trigger:** User request to spec + build all changes to buildings (incl. new custom
buildings seeded into provinces), trade goods, and production; tie into existing
content (Board of Works office, Self-Strengthening, customs, revenue/salt, missions);
add `rifles` good; run as a continuous overnight job ending in a deep adversarial
Workflow review. (Named *2 because an overnight_decisions.md already exists.)

This file records every MAJOR DECISION and its rationale, so a later reviewer (human
or agent) can trace WHY each change was made. Per the fix-traceability standing rule
every code change also carries a task-tagged comment + se_LOG marker + SESSION_REPORT
entry; this doc is the design-level companion to those.

---

## 0. GUIDING PRINCIPLES (locked)

1. **Content over engine.** The quarterly production→trade→consumption→treasury sim is
   well-built and correct (GameEconScan confirmed). The historicity gap is almost
   entirely on the INPUT side: raw goods not on the map, and no starting buildings.
   So the bulk of this work is `province_setup.csv` + building definitions + a
   game-start seed — NOT rewrites of the production loop.

2. **NO scripted factories for CHI at 1815.** HistEconResearch is explicit: 1815 China
   was pre-industrial (high-level equilibrium trap, no mechanised industry). Giving CHI
   `INDUSTRY_assign_factory` calls like GBR/USA would be AHISTORICAL. China's handicraft
   economy is correctly modelled by the COTTAGE INDUSTRY layer (se_COTTAGEIND.txt), which
   needs no buildings — it just needs the raw goods present. Mechanised factories arrive
   later via the existing Self-Strengthening tree. "CHI has zero factories" is therefore
   CORRECT BY DESIGN and is NOT treated as a bug.

3. **Concrete over abstract** (standing design rule). New buildings are concrete on-map
   objects; behaviour that reads/spawns them lives in scripted_effects. Custom buildings
   act as production MULTIPLIERS (local_output_modifier) over the cottage-industry output
   in the province — the concrete face of "Jingdezhen/Suzhou is a production centre".

4. **Additive, byte-safe, low-risk.** New manufactured goods follow the EXACT plumbing
   pattern of an existing good (glass/bronze) across all ~20 files. New raw goods follow
   the maize/#64 pattern. No behavioural change to existing goods. Buildings follow the
   arsenal_building/qing_customs_house_building schema. File byte conventions respected
   (se_*.txt = NO BOM; on_action = MANDATORY efbbbf BOM; province_setup.csv unchanged).

5. **Oracle rule:** no reliance on unproven engine capability. `add_building_level` in a
   `p:<id>` scope at game start, cottage-industry recipes, and trade-good definitions are
   all PROVEN in this build. If any step needs an unproven capability, STOP and flag it.

---

## 1. TRADE GOODS — decisions

### 1a. New MANUFACTURED goods

**`porcelain`** — Jingdezhen (景德鎮, ~9,000 kilns) + Canton decorated ware.
- Category: luxury tier (matches export/luxury role; exact category number set to match
  the luxury trade-pass routing once the a675 plumbing trace confirms it).
- Produced by COTTAGE INDUSTRY from `inorganic_compounds` (explicitly "inc. clay" — kaolin
  proxy) + fuel (`wood`/`coal`). Recipe cloned from COTTAGEIND_produce_glass. Modest
  efficiency (historically DECLINING by 1815 due to European competition), concentrated at
  Jingdezhen, not sprawled.

**`rifles`** — small-arms military-logistics good (user request). Fills the gap between
`early_munitions`/`late_munitions` (powder/ammunition) and `early_artillery`/`late_artillery`
(cannon). Vestigial `# allow_unit_type = rifles` comment already exists on `peat`.
- Category: industrial (matches munitions/artillery routing).
- Produced by cottage industry at modest efficiency (proto-industrial gunsmithing) from
  `iron` + munitions-adjacent inputs; scales hard with industrialisation later. Recipe
  cloned from COTTAGEIND_produce_early_munitions/early_artillery. Conceptually feeds the
  LOGISTICS_quarter munitions layer.

**`cannons` — REJECTED.** Artillery already modelled (`early_artillery` + `late_artillery`,
full cottage recipes). A separate cannons good is redundant and fragments the chain.

### 1b. Retire defunct goods
- **`linen`** — retire the explicit leftover "# to be removed" good. MUST confirm zero
  province references first (the defunct_tradegoods_replaced block in oa_economy_setup.txt
  lines 33–115 already remaps defunct goods per-province at game start — check there + in
  province_setup.csv). If referenced, remap to textile_fibres before deleting the def.
- `hemp`/`cotton`/`incense`/`palm`/`amber` also marked phase-out but leave their DEFS in
  place this pass unless the province trace proves them unused (avoid load-time breakage).

### 1c. Province trade-good re-map (raw goods — activates cottage industry) — GAP 2
Target distribution (final IDs from a66e province-geography agent):
- **Silk** across Jiangnan (Suzhou/Huzhou/Nanjing/Hangzhou, `wu`) — was 1 province, the
  single biggest historicity miss; raising it auto-activates cottage clothing/luxury_clothing.
- **Cotton→textile_fibres** in Songjiang (松江).
- **Coal** in Shanxi/Zhili (was 1). **Iron** in Shanxi/Hebei/Sichuan (was 1).
- **Copper** at Yunnan (雲南) — coinage source (ties to currency/silver layer).
- **Tea** validated to Fujian Wuyi / Anhui / Hunan Anhua (refine, don't inflate count).
- **inorganic_compounds (clay)** at Jingdezhen for the porcelain input.
- **salt** at historical regions feeding the Yangzhou monopoly.
- New World crops (#64) kept, concentrated in highland provinces.
- **Opium NOT added as a CHI production good** — imported from British India in 1815; the
  current state (defined, assigned to no province) is CORRECT and stays.

[EXACT PROVINCE IDS — filled from a66e agent report in §8.]

---

## 2. CUSTOM BUILDINGS — decisions

New buildings follow arsenal_building / qing_customs_house_building schema (local_* mods,
cost, time, allow{ tech gate + sufficient_job_slots }, empty modification_display). All are
seed/event-spawned via add_building_level (bypasses the `allow` build-menu gate). Each acts
as a PRODUCTION MULTIPLIER (local_output_modifier) + flavour.

Planned NEW buildings (final modifiers locked in build):
1. **Silk filature (織造局/繅絲坊)** — Jiangnan silk + Imperial Silk Manufactory (Nanjing).
2. **Porcelain kiln (御窯/民窯, Jingdezhen)** — concrete face of porcelain production.
3. **Tea workshop (茶廠)** — Fujian/Anhui/Hunan processing.
4. **Cotton workshop (棉紡坊, Songjiang)** — cotton handicraft.
5. **Salt yard (鹽場/鹽運司, Yangzhou)** — salt production + tax; ties to Revenue office salt
   gabelle (concrete face of the abstract qing_salt_gabelle_reformed flag — GAP 3).

REUSE existing Qing buildings as 1815 seeds where they already model the thing (don't
duplicate): **qing_canal_depot_building** (Grand Canal grain depots, currently event-only —
SEED at 1815), **qing_yamen_building** (yamens existed in every prefecture in 1815),
**qing_granary_building** (ever-normal granaries operational in 1815). Add NEW buildings
only for production centres not already covered.

Bias: FEWER, well-integrated buildings over sprawl.

---

## 3. STARTING BUILDING SEED — decisions (confirmed by aa92 agent)

- New scripted_effect `QING_seed_1815_economy` in a NEW file
  `common/scripted_effects/se_QING_ECONOMY_SEED.txt` (NO BOM — match sibling se_QING_*.txt;
  will verify a neighbour's first bytes before creating).
- For fixed provinces: `if = { limit = { owns = <id> }  p:<id> = { add_building_level = X } }`
  (add_building_level is province-scope, bypasses allow, needs NO state.governorship hop).
- Called ONCE from `oa_economy_setup.txt` → `on_game_initialized` → `effect`, as a NEW
  self-guarded block with its own sentinel `chi_starting_buildings_done`, inserted AFTER the
  factory block closes (after line 243). Pattern confirmed by agent:
  ```
  if = {
      limit = { NOT = { has_global_variable = chi_starting_buildings_done } }
      c:CHI = { ... existing QING_* country-scope seeds ... }
      # fixed-province seeds:
      if = { limit = { owns = <id> }  p:<id> = { add_building_level = <building> } }
      set_global_variable = chi_starting_buildings_done
  }
  ```
- oa_economy_setup.txt carries the efbbbf BOM — MUST preserve when editing byte 0 / adding
  the block (edit mid-file, never touch the leading BOM).
- After seeding, ensure the goods/stockpile refresh runs so seeded raw goods register in Q1.
  Trade-good province re-map goes in province_setup.csv (authoritative at load) — the seed
  block only places BUILDINGS, not raw goods. CONFIRM the defunct_tradegoods_replaced block
  (lines 33–115) does not clobber my re-mapped provinces.
- se_LOG enter/exit/line wiring throughout.

---

## 4. PRODUCTION — decisions

- **No production-loop rewrite.** porcelain + rifles = additive plumbing only, one insertion
  each cloned from glass/bronze: trade-good def, `<good>_stockpile` setup var
  (GOODS_setup_governorship_stockpiles), `GOODS_governorship_<good>_produced` svalue,
  COTTAGEIND recipe + COTTAGEIND_produce_all entry, COTTAGEIND_cache_all_values raw-input
  cache line if needed, demand svalue, consumption entry (CONSUME_all_stockpiles), and
  trade-pass/category routing. FULL CHECKLIST from a675 agent in §9.
- Custom production buildings contribute via `local_output_modifier` — a province modifier the
  production svalues already read; no new production code for the multiplier effect.

[FULL PLUMBING CHECKLIST — §9, from a675 agent.]

---

## 5. INTEGRATION WITH EXISTING CONTENT — decisions

Per user ("the Grand Minister of Works would be directly affected"). Targets (final hooks
from aca9 integration agent in §10):
- **Board of Works / Grand Minister of Works office**: capable Works holder boosts/enables
  the works & production buildings (dike, canal depot, kiln, salt yard). Wire into Works
  office effectiveness / domain pulse.
- **Revenue office & salt**: salt yard ties to qing_salt_gabelle_reformed + salt-revenue.
- **Self-Strengthening**: new production buildings as context/prerequisites; mechanised
  upgrades of handicraft centres later in the tree.
- **Customs / treaty ports**: tea/silk/porcelain exports flow through Canton + customs.
- **Missions/events**: qing_* tasks that reference economy/buildings reward or require the
  new buildings/goods (Summer Palace, colonization, Self-Strengthening).

[EXACT HOOK POINTS — §10, from aca9 agent.]

---

## 6. OPEN QUESTIONS / RISKS (updated live)

- Trade-good CATEGORY numbers for porcelain/rifles must match the 7-pass trade routing —
  confirm from plumbing trace (§9).
- Verify `linen` province references before deletion; check defunct_tradegoods_replaced.
- Confirm the seeded buildings/goods register in Q1 (refresh order).
- Localization .yml for all new goods/buildings or the game shows raw keys.

---

## 7. BUILD LOG (chronological)

- 2026-07-08: Spec started. 4 research agents launched (a675 manufactured-good plumbing
  trace; a66e CHI province geography; aa92 building-seed init — DONE, folded into §3;
  aca9 integration hooks). Decisions doc created.

---

## 8. PROVINCE GEOGRAPHY (from a66e agent)

### CRITICAL SOURCE DECISION (resolved 2026-07-08)
The engine loads **`setup/provinces/00_<Region>.txt`** province-history files (the
`trade_goods="X"` line, keyed `<id>={ #Name`). `common/province_setup.csv` is ONLY the
input to the `buildings_generator.py` / `old_to_new_setup_*.py` modding scripts — it is
NOT read by the game. Therefore:
- **All trade-good re-map edits go in `setup/provinces/*.txt`** (authoritative).
- Optionally sync `province_setup.csv` for generator hygiene, but the .txt is what matters.
- **GameEconScan's & a66e's CSV-based good counts may be STALE** relative to the .txt files
  (confirmed discrepancies: Jingdezhen 7397 = `stone` in .txt vs `inorganic_compounds` in CSV;
  Wuyishan 3317 = `grain` in .txt vs `peanut` in CSV; Anhua 1249 = `tea` in .txt vs `maize`
  in CSV). Re-read the .txt value per province before editing.
- Confirmed: Suzhou 2588 in 00_Jiangsu.txt line 135 = `trade_goods="grain"`.

### Target province IDs (real-place mapping HIGH confidence; verify current .txt good per edit)
- **Jiangnan silk belt (`wu`)**: Suzhou 2588, Huzhou 5779, Nanjing 6659, Hangzhou 8120.
  Nearby `wu` textile: Wuxi 366, Changshu 455, Jingjiang 363, Taizhou 6039.
  → set several to `silk` (silk is currently mis-placed at Beijing 8363/Tianjin 3783/Dagang 2640).
- **Songjiang cotton (`wu`, AREA=Shanghai)**: Shanghai 5429, Jinshan 7402, Taicang 2572,
  Changshu 455, Jingjiang 363. No `cotton` good in China → use `textile_fibres`.
- **Jingdezhen porcelain (`gan`)**: 7397 (clay input) — set `inorganic_compounds` for kiln input.
- **Tea**: Fuzhou 3651, Quanzhou 3950 (`min`, already tea), Wuyishan 3317 (`min`), Jian'ou 2693;
  Hunan Anhua 1249, Changde 6434, Shaoyang 5315, Huaihua 2679, Linxiang 6111 (`xiang`/`shangjiang`,
  mostly already tea); Anhui candidates Huangshan 4441 / Hukou 783. Refine, don't inflate.
- **Coal (`jin` Shanxi / `beihua` Zhili)**: Taiyuan 8501, Datong 207, Changzi 3907 (Shanxi).
  No coal in China currently → create the Shanxi/Zhili coal cluster.
- **Iron**: only Laiwu 5874 (Shandong) currently. Add Shanxi/Hebei/Sichuan iron.
- **Yunnan copper (`shangjiang`/`kam-sui`, AREA=Yunnan/Dali)**: Kunming 2759, Qujing 2418
  (Dongchuan district ~NE Yunnan), Dali 493. Copper coinage source.
- **Yangzhou salt (`wu`)**: 3208 + canal-belt Gaoyou 7964, Huai'an 8311, Xinghua 3144.
  No `salt` good in China currently → create salt at these + coastal Jiangsu/Shandong.
- **Grand Canal**: Beijing 8363, Tianjin 3783, Yangzhou 3208, Xuzhou 9366, Huai'an 8311,
  Gaoyou 7964, Suqian 4330. (Beijing/Tianjin currently hold the mis-placed silk → free them.)
- **Canton (`yue`)**: Guangzhou 9298, Foshan 9301, Macau 2481, Hong Kong 8245, Dongguan 3036.

NOTE the takeaway: silk/salt/coal/iron/copper/porcelain are essentially ABSENT from Chinese
provinces today — this re-map creates the regional specialisations largely from scratch, which
is exactly the GAP 2 fix. Silk is currently mis-placed at the Beijing cluster (ahistorical).

---

## 9. NEW-GOOD PLUMBING — scope decision (from a675 agent + own investigation)

### CRITICAL FINDING (2026-07-08)
- The engine-loaded trade-goods registry is `common/trade_goods/00_imp19c.txt` and contains
  ONLY RAW goods. MANUFACTURED goods (glass, clothing, bronze, munitions, artillery…) are
  defined in `common/WIP/trade_goods/00_default.txt` — and **`common/WIP/` is NOT an
  engine-loaded path**. Manufactured goods therefore exist purely as SCRIPT-VARIABLE
  constructs (`<good>_stockpile`, `COTTAGEIND_produced_<good>`, `INDUSTRY_*_<good>`) routed
  through hand-written `zz_*_injector.txt` "complex" lists and the svalue chains.
- The a675 agent mapped the MANUFACTURED-good surface: ~16 files, ~40 insertion points per
  good, including GLOBAL trade-split (se_GLOBALTRADE_split), price (se_PRICE/PRICE_svalues),
  industry factory chain (INDUSTRY_svalues 1378-1495, se_INDUSTRY_setup, industrial_goods_buttons
  GUI), SELL/PURCHASE/TRADE category lists, AI/WEALTH svalues. A single error there breaks the
  economy for EVERY country in the game.

### DECISION — model porcelain + rifles as RAW-STYLE goods (maize/#64 proven pattern)
For this UNATTENDED overnight run, both new goods follow the RAW-good template proven and
shipped by the #64 New-World-crops fix (maize/sweet_potato/potato/peanut/chili), NOT the
high-blast-radius manufactured path. Rationale:
- **Safety:** the raw-good footprint avoids the global trade-split injector, the industry
  factory chain, and the price-input-cost machinery — the highest-risk shared code. maize
  proves the raw pattern works end-to-end in this build.
- **Porcelain fits raw modeling:** in THIS mod, tea/silk/salt are RAW provincial specialty
  goods (Jingdezhen porcelain is a provincial handicraft specialty, exactly analogous). The
  porcelain KILN building boosts its output via `base_resources`. Category = luxury (matches
  tea/silk category tier). Silk→clothing conversion still happens via existing cottage industry.
- **Rifles fits raw modeling as a tradeable military commodity:** produced provincially
  (arsenal/military regions), tradeable. Deeper army-CONSUMPTION wiring (tying rifles demand to
  the LOGISTICS munitions layer) is noted as a FOLLOW-UP, not attempted unattended, to avoid the
  manufactured-demand machinery. Category = an industrial category.

### RAW-GOOD footprint to replicate (precise line numbers from a66e/maize trace in §9b)
Definition (00_imp19c.txt) + injectors (zz_tradegood_injector, zz_tradegoods_injector, and the
appropriate category injector) + GOODS_svalues (`_produced`, `_national_production`) + se_GOODS
(produces_ flag in update_governorship_local_goods, stockpile in setup, produce_all entry) +
is_raw_tradegood trigger + DEMAND/PRICE/TRADE/SELL/PURCHASE/WEALTH/AI svalue clones + GUI
(province_window, trade_view) + font_icons + localization + placeholder .dds (cp an existing one).

### Icons
Cannot author binary .dds. Create placeholders by copying an existing icon:
`cp gfx/interface/icons/tradegoods/silk.dds .../porcelain.dds`,
`cp .../early_munitions.dds .../rifles.dds`. (maize ships with NO dedicated icon and works, so
even a missing icon is tolerated — but placeholders are cleaner. Flag for real art later.)

## 9b. MAIZE RAW-GOOD FOOTPRINT (precise checklist — from trace agent)

_pending maize-footprint trace agent_

## 9c. MANUFACTURED-GOOD SURFACE (a675 agent — recorded for the deferred manufactured path)
Full ~16-file/~40-point checklist captured in the a675 agent transcript; NOT used this run
(raw path chosen). Key files if manufactured is ever pursued: GOODS_svalues (2760 _produced
w/ industry branch), DEMAND_svalues, se_COTTAGEIND (500 glass recipe), zz_tradegood_5_injector
(type-5 pass), se_GLOBALTRADE_split (5826 input-cost OR), INDUSTRY_svalues (1378-1495 chain),
se_INDUSTRY_setup, se_SELL/se_PURCHASE/se_TRADE category lists, industrial_goods_buttons.txt,
province_window.gui (2702), trade_view.gui (1360), font_icons.gui (711), PRICE/AI/WEALTH/TRADE
svalues, customizable_localization. Trade-good def would go in the LOADED 00_imp19c.txt (NOT
WIP). Reference good = glass (category 4, type-5 pass, luxury_goods+business_goods categories).

---

## 10. INTEGRATION HOOK POINTS (from aca9 agent)

Mod idiom throughout: a 0–100 counter on CHI → read by quarterly `QING_GOV_pulse` → swaps
modifier bands and, at band-crossings, spawns/removes real buildings via `add_building_level`
on `ordered_owned_province { order_by = total_population max = 1 }`. Offices are single
character-seats `qing_office_<name>_holder` granting `qing_office_<name>_active` modifier.

**1. Board of Works / Grand Minister of Works (工部) — the user's headline hook.**
- Office modifier `qing_office_works_active` in `common/modifiers/qing_governance_modifiers.txt:150`
  currently = `{ build_cost = -0.10  global_monthly_civilization = 0.05 }`. → EXTEND with an
  output / building-production bonus so an installed Works minister makes the new production
  buildings cheaper/more productive.
- Works accountability metric = `civilization` (`se_QING_ACCOUNTABILITY.txt:165-177`, counts
  high-civ provinces). New production buildings carry `local_monthly_civilization`, so seeding
  them AUTOMATICALLY raises the Works minister's score — free thematic tie-in.
- NO dedicated Works pulse exists in `QING_GOV_pulse` (se_QING_GOVERNANCE.txt:440-483). Works is
  driven only by a flavour roll in se_QING_DECLINE.txt:1245-1255. → OPTION: add a
  `QING_works_pulse` that actively spawns/maintains works+production buildings, registered
  alongside the other office pulses (~L463), mirroring `QING_revenue_pulse`.

**2. Board of Works buildings & spawn idiom** — `se_QING_WORKS.txt`: `QING_works_build_dike`
(L27, finesse-gated: holder finesse≥7, cost scaled by finesse≥9 else overrun+corruption),
`_build_canal_depot` (L90), `_build_wall_section` (L146). Driven by `qing_works.*` events fired
from the decline roll. `qing_canal_depot_building` already carries `local_state_trade_routes`.
→ new works-style infra follows this finesse-gated idiom; production buildings use the
band-track idiom (§7) or Revenue province-targeted spawns (§3).

**3. Revenue office & salt (戶部)** — `se_QING_REVENUE.txt`: `qing_salt_gabelle_reformed` 0/1 flag;
`QING_revenue_pulse` (L40-121) vacant→salt graft+corruption, filled→offers `qing_revenue.1`
reform. CONCRETE spawn precedent for salt yard: `QING_revenue_stock_granary` (L210-228) does a
PROVINCE-ID-TARGETED `add_building_level = qing_granary_building` in specific Yellow River ids
(this is the model for region-specific salt-yard seeding, vs most-populous). Event
`qing_revenue.1` adds `qing_salt_gabelle_reformed_mod` / `qing_salt_gabelle_graft` modifiers.
→ salt yard spawns mirror stock_granary, gated by Revenue minister fitness; the reformed/graft
modifiers boost/suppress salt-yard output. salt good already defined (00_imp19c.txt:670).

**4. Self-Strengthening (自強運動)** — `se_QING_SELFSTR.txt`: `qing_selfstr_progress` counter;
generic spawner `QING_selfstr_build = { building = X }` (L76-90). ALREADY founds real economy
buildings (arsenal L105, port L145, IND_resource_gathering_operation + INF_railway L448-450,
URB_commerce_district). Wonder at progress≥85. Mission tree `qing_selfstrengthening_missions.txt`
drives it; tasks gate on `var:qing_bureau_capacity >= N` + `requires` prior tasks.
→ mechanised versions of the handicraft centres (cotton workshop, mechanised filature) fit as
Self-Strengthening rewards (`QING_selfstr_build = { building = qing_cotton_workshop_building }`)
or as `has_building` prerequisites on later tasks. Refraction test penalises hollow progress →
real production backing progress is rewarded.

**5. Customs & treaty ports (海關)** — `se_QING_CUSTOMS.txt`: `QING_customs_build_house` (L84-100)
adds `qing_customs_house_building` at most-populous COASTAL province; `QING_customs_pulse`
(L166-209) quarterly revenue scaled by efficiency. Treaty ports: `qing_treaty_port` province
modifier on coastal ports. Canton = Guangzhou p:9298. → export goods (tea/silk/porcelain) in
coastal/treaty-port provinces can scale customs revenue/efficiency; seed kiln/tea/silk near
treaty ports so customs revenue has a thematic source.

**6. Missions/events** — `qing_selfstrengthening_missions.txt` = richest economy tree, BEST home
for new-building rewards. `qing_colonization_missions.txt` (Taiwan tea historical → reward tea
workshop). `oa_economy_setup.txt` defunct-tradegoods remap block (L33-116, gated
`defunct_tradegoods_replaced`) is where game-start good remaps live. Summer Palace / reform trees
have ZERO economy refs = greenfield.

**7. THE SPAWN PATTERN (band-track idiom to follow)** — `se_QING_GOVERNANCE.txt:220-266`
`QING_GOV_yamen_band_track` (off `qing_bureau_capacity`) + `:277-317` shuyuan (off
`qing_exam_ladder`), invoked from pulse L378-379. Idiom: compute current band 0-3, seed
tracker WITHOUT building on first sighting (CRITICAL — no spawn burst on load), on RISE build
in most-populous province, on FALL remove one (guarded by has_building). → template for
spawning production buildings from a meter/office; optionally target specific province-id list
(like stock_granary) for region-locked goods (Jingdezhen porcelain, Jiangnan silk).

**CROSS-CUTTING (critical):** existing qing_* buildings use FLAT `local_*` modifiers, NOT the
goods-production pipeline. If new buildings must actually PRODUCE/multiply the new goods (not
just buff tax/civ), they need a modifier the GOODS/production svalues actually read
(`local_output_modifier` and/or the per-good output). VERIFY which modifier the production
svalues consume before finalising building modifiers — no Qing-building precedent for this.
[Verifying now — see §11.]

---

## 11. PRODUCTION-MODIFIER LINKAGE (RESOLVED 2026-07-08)

Raw production svalue pattern (e.g. `GOODS_governorship_silk_produced`, GOODS_svalues.txt:1259):
```
value = 0
every_governorship_state = { every_state_province = {
    limit = { trade_goods = silk }  add = num_goods_produced } }
multiply = owner.MODIFIER_agriculture_productivity
```
So raw output = Σ(engine `num_goods_produced` per matching province) × a country productivity
modifier. `MODIFIER_agriculture_productivity` = 1 + `modifier:tribute_income_modifier` (repurposed
vanilla key; MODIFIER_svalues.txt:75).

**DECISION — how new buildings boost production (PROVEN keys only):**
- To raise a province's RAW good output, use **`base_resources = N`** — the PROVEN key
  `IND_resource_gathering_operation` already uses (00_industrial_buildings.txt:33). It increases
  the engine `num_goods_produced`, which flows straight through the `_produced` svalues. This is
  the concrete production multiplier for silk/tea/salt/coal/iron/copper/clay buildings.
- Also use the strata-output modifiers `local_lower_strata_output` / `local_proletariat_output`
  etc. (also proven on IND_resource_gathering_operation) + pop-ratio `local_*_desired_pop_ratio`
  for flavour and to feed the pop-scaled COTTAGE recipes (clothing/luxury_clothing/porcelain).
- **AVOID `local_goods_output`** — grep shows it is UNUSED anywhere in this build; per the oracle
  rule (no reliance on unproven-in-this-build capability) prefer the proven `base_resources`.
- Manufactured goods (silk clothing, porcelain, rifles) scale on pops+industrialisation in the
  cottage layer, so their buildings help via base_resources on the RAW input + strata/pop modifiers,
  NOT a direct manufactured-output key. More raw silk (base_resources) → more cottage clothing.

This means new production buildings CAN plug into the goods pipeline via `base_resources` — the
"no Qing-building precedent" caveat from §10 is resolved: IND_resource_gathering_operation IS the
precedent, just not a qing_* one.

---

## 12. STARTING MILITARY OOB (Qing army/navy) — RESOLVED 2026-07-08 (#190)

User: Qing starts with one 12,000-man army and two 85-ship navies — almost certainly wrong.

### ROOT CAUSE (investigated + independently verified against the raw files)
Two independent mechanisms produce CHI's starting forces:
1. **Engine auto-gen** from global defines (common/defines/00_defines.txt): `STARTING_COHORTS_PER_MANPOWER
   = 0.2`, `STARTING_SHIPS_PER_PORT_POPULATION = 0.06`, `COHORT_SIZE = 500`. Applies to EVERY
   country; no per-country disable flag exists. This is where the two ~85-ship fleets come from
   (China's large coastal port population × 0.06).
2. **Scripted** `SE_qing_armies` (imp19c_effects_legion_setup.txt) — 27 historical garrison
   legions (Eight Banners + Green Standard), fired at oa_economy_setup.txt:2186. Metropolitan
   Eight Banners = size 23 → 24 cohorts × 500 = exactly 12,000 (matches the "one 12k army").

**Army under-materialisation:** an agent claimed 17/27 garrisons fail their `owner = c:CHI`
guard. I VERIFIED THE BRACE STRUCTURE MYSELF and CORRECTED that: in setup/main/00_default.txt
CHI's `own_control_core` opens at 35705 and its closing braces (35728-29) are COMMENTED OUT; the
"YNG/SHG/MZH viceroyalty" blocks have their tag/government/brace lines `#`-commented but their
PROVINCE-NUMBER lines LIVE — so those provinces fall through into CHI's still-open list (which
closes at the live `}` on 35770). Hence the 8 "viceroyalty" garrison provinces (7129/8120/3651/
209/5616/1303/5786/6781) ARE CHI-owned and already spawn. Only **5 frontier garrisons genuinely
fail**: Ili p:3534 + Ürümqi p:2930 (live tag ILI), Mukden p:1087 (MKD), Heilongjiang p:43 (HLJ),
Kashgar p:2700 (XNG, subject of ILI) — all owned by live autonomous-governorship SUBJECTS of CHI,
so `owner = c:CHI` is false for them. All 5 commander chars (340/244/358/339/241) exist.

### FIX (as built)
- **Garrison guard** (imp19c_effects_legion_setup.txt SE_qing_raise_garrison[_cmd]): widened the
  ownership limit from `owner = c:CHI` to `OR = { owner = c:CHI  owner = { is_subject_of = c:CHI } }`.
  is_subject_of is PROVEN (common/military_traditions/00_indian.txt; Invictus parthia_interactions).
  Restores the 5 frontier banner garrisons (Ili/Ürümqi/Mukden/Heilongjiang/Kashgar) — historically
  Qing frontier commands on Qing-administered subject land. Legions still raised from
  c:CHI.capital_scope.governorship so they belong to Qing. Net: all 27 garrisons now materialise.
- **Navy** (NEW effect `SE_qing_navy`, wired oa_economy_setup.txt:2187 after SE_qing_armies):
  the 1815 Qing had NO ocean-going battle-fleet — only provincial water-forces (水師) of war-junks.
  The two auto-gen ~85-ship fleets are categorically wrong. So: `every_navy = { destroy_unit = yes }`
  (proven Invictus 01_carthaginian_missions_08_naval.txt:152-157) disbands the auto-gen fleets, then
  raise two modest junk squadrons with `brig` (only period-appropriate light-warship key) — 廣東水師
  Guangdong Water-Force (6× brig at Canton p:9298) + 福建水師 Fujian Water-Force (4× brig at Fuzhou
  p:3651, with a largest-coastal-province fallback). GLOBAL-SENTINEL guarded (qing_navy_setup_done)
  because destroy_unit is destructive and must fire exactly once.
- **Army auto-gen LEFT IN PLACE** (deliberate): a large Qing land mass IS historical (~850k paper),
  and the mod's France-occupation design already relies on auto-gen for mobile field armies atop
  scripted garrisons. The army was only wrong in APPEARING singular, which the 27-garrison
  restoration fixes; the navy was wrong in KIND, which the disband+junk-squadron fix addresses.
- Blue-water modern navy still arrives only via the existing Self-Strengthening tree
  (se_QING_SELFSTR.txt QING_selfstr_raise_fleet), unchanged.


---

## 13. TRADE-GOOD PLUMBING — as-built (#182/#189, porcelain + rifles)

### Decision: clone the maize (#64) RAW-GOOD footprint, not the manufactured path
The un-loaded WIP manufactured goods (glass/clothing) would require editing ~40 points across
16 files that touch GLOBAL trade/price/AI/industry svalues — high blast radius for an unattended
run. Instead both new goods are modelled RAW-STYLE, cloning the **maize** footprint that #64 already
added to this repo. maize was verified **byte-identical to `tea`** across all **39 economy
identifiers** (see parity check below) — i.e. maize is a proven, complete, in-repo raw-good
template. Cloning it reproduces a known-good structure exactly.

### Why maize over tea/silk
- `silk` is ENTANGLED: it feeds the manufactured `luxury_clothing` chain via INDUSTRY_* blocks
  (INDUSTRY_demand_luxury_clothing_silk etc.). Cloning silk would drag in manufacturing coupling.
- `tea` is clean but is not itself a recently-added good.
- `maize` is clean (no downstream manufacturing consumer) AND was added by the exact #64 process
  we are replicating. Chosen as the template for BOTH porcelain and rifles.

### Decision: rifles modelled raw-style too (NOT the early_munitions building-count pattern)
early_munitions is entangled with the munitions-infra stockpile cache + COTTAGEIND. For overnight
safety and uniformity with porcelain, `rifles` clones the same clean maize template. Rifles is
assigned to arsenal provinces via `trade_goods=rifles`; the rifle-works/arsenal BUILDING boosts
output via `base_resources` (the building multiplies provincial output, exactly the "concrete
production centre" model in §0.3). This keeps rifles a tradeable military-logistics commodity
without touching the munitions-infra cache.

### The full footprint = THREE layers (all present for maize; all cloned for the twins)
1. **Per-good svalue/effect/loc blocks** (~90 insertions/good). Done via deterministic cloners
   (`zz_clone_goods.py` group A, `_B` group B, `_D` group D) that copy whole brace-balanced units
   or exact statement-ranges — never hand-typed line numbers (agent-remembered line numbers proved
   unreliable earlier this session). Each cloner validates brace-balance parity and
   maize→porcelain/rifles identifier-count parity against a tmp copy BEFORE writing, and is
   idempotent-guarded (skips a file if a twin is already present).
   - **Group A** (6 script_values files: GOODS/DEMAND/PRICE/TRADE/AI/WEALTH): column-0 top-level
     def detection + LOCAL forward brace-walk — immune to the files' pre-existing global brace
     quirk (TRADE_svalues has a harmless net -2 that carried through untouched, proving isolation).
   - **Group B** (7 effect/loc files: se_GOODS/se_GLOBALTRADE_split/se_SELL/se_PURCHASE/se_PRICE/
     se_TRADE/000_ECON_loc): fixed 1-indexed statement-ranges, because these hold maize as MULTI-LINE
     units (incl. an if/else pair in se_GOODS) that line-cloning would corrupt.
   - **Group D** (6 files missed in the first pass — see the CAUGHT-BUG note): DEMAND_luxury_svalues,
     INCOME_svalues, se_TRADE_new, se_DEMAND, 00_trade_scripted_triggers, 00_resource_building_potential.
2. **Generated iterator files** (`zz_clone_goods_C.py`): the 4 `zz_*_injector.txt` files each embed a
   hardcoded good-list as `$PREFIX$maize$SUFFIX$` template blocks; cloned porcelain/rifles blocks
   after maize in all 4. (The injectormaker GUI tool is not headless-runnable, so these generated
   files are hand-edited directly.)
3. **Injector INPUT lists** (`zz_clone_goods_C.py`): porcelain/rifles stanzas appended to
   `zz_injectormaker/all_goods.txt` + `luxury_goods.txt` so a future regeneration reproduces the edit.

### CAUGHT BUG (first-pass parity miss → fixed by Group D)
The initial target list omitted **`DEMAND_luxury_svalues.txt`**, which DEFINES the base-demand block
`DEMAND_maize`. My Group A clones in DEMAND_svalues/TRADE_svalues emit `subtract = DEMAND_porcelain`
/ `DEMAND_rifles` — which were therefore **referenced-but-undefined** (would break the demand sim).
Root cause of the miss: a `\btea\b`-style parity grep gave a false "tea=0" because `\b` does not
match before `_` (DEMAND_tea). Fixed by a substring-based full-footprint parity check across ALL
economy dirs, which surfaced `DEMAND_luxury_maize`/`DEMAND_maize` and 5 more plumbing files. Group D
clones them; `DEMAND_porcelain`/`DEMAND_rifles` are now defined (DEMAND_luxury_svalues.txt:338/378).

### Deliberate EXCLUSIONS (maize-as-New-World-crop content the twins must NOT inherit)
Classified using `silk` (a category-4 worked good, same tier as porcelain/rifles) as the analog —
files where silk is ABSENT but maize present are food-crop/New-World-crop specific:
`DEMAND_food_svalues.txt` (maize provides food; worked goods don't — silk absent),
`se_QING_COLON.txt` (New World crop colonization), `qing_migration_modifiers.txt` (comment only),
`qing_province_reports.txt` (New World crops GUI report), `00_cultural_modifiers.txt`
(fascination/taboo — consumer-novelty crops, not worked luxuries; silk/porcelain absent).
`tech_rifles` (a pre-existing invention) is an unrelated name-collision, correctly left alone.

### FINAL PARITY (verified): maize 39 idents → porcelain 39 twins, rifles 39 twins (+`tech_rifles` pre-existing). Brace balance preserved in every file.

---

## 14. RESEARCH-DRIVEN ADDITIONS requested mid-run (#191, #192)

Two historical-research agents (English + Chinese academic sources) were dispatched mid-build; their
sourced reports now drive two follow-on features. Full reports captured in session; headline decisions:

### 14a. #191 — Qing 1815 army/navy OOB, historically-grounded rework (SUPERSEDES the §12 stopgap)
Sourced OOB (清史稿·兵志, Elliott *The Manchu Way*, Wakeman, Wawro-style consensus): Green Standard
綠營 ~630k–660k effective (861,671 on the 1812 paper roll, inflated by 吃空額 phantom soldiers);
Eight Banners 八旗 ~200k (Metropolitan ~100–120k, Provincial garrisons ~100k, Ili/frontier ~15k+);
NO blue-water navy — only provincial 水師 war-junk squadrons (Guangdong ~400 junks/~20k men,
Fujian premier Taiwan-Strait command, Zhejiang/Jiangnan riverine). Both land forces were dispersed
CONSTABULARY, not field armies — deployable strength ~10–20% of paper roll. Quality LOW (post-White-
Lotus decay, matchlocks/bows, phantom rolls); the navy had only just survived (by amnesty, not
victory) the 1805–1810 Zheng Yi Sao pirate confederation that OUTMATCHED it.
**Decomposition (build target):** ~8 named land armies — Metropolitan Banner (elite, small ~15–20k,
low-readiness debuff), Manchurian Banner ~8k, Ili Frontier ~8k, and five Green Standard field forces
(NW/Central/Southern/SE/SW, infantry-heavy, cheap/numerous/low-quality, 12–20k each) — plus 3–4 weak
coastal war-junk fleets (Guangdong ~40 / Fujian ~30 / Zhejiang-Jiangnan ~20, all outclassed by a
single European steam frigate). Banner = small elite cavalry; Green Standard = the on-map bulk.
Extends SE_qing_armies / SE_qing_navy. This replaces the §12 two-junk-squadron stopgap.

### 14b. #192 — 19th-century mobilization / readiness system (expands military-logistics)
Sourced model (Showalter *Railroads and Rifles*, van Creveld *Supplying War*, Lynn *Bayonets of the
Republic*, Wawro): newly-raised units — ESPECIALLY levies — start UNREADY and break in over time.
**Multi-axis** (history says the axes mature at different rates): (1) drill/discipline — fast (~2mo),
(2) cohesion/morale — medium (~4mo), (3) supply/logistics — slow (~6mo, PERMANENT FLOOR for
irregulars; van Creveld: the logistical tail must be BUILT, cannot be conjured). **Front-loaded
exponential decay** `penalty(t)=p0·exp(-3t/D)` (≈95% gone at D). **Raise-time penalties by type**:
professional regulars −10/−10/−20% D≈1mo → line/trained-conscript −25/−30/−40% D≈3mo → fresh levy
−40/−45/−55% D≈5mo → hasty levy/militia −50/−55/−65% D≈6mo (supply floor). **Accelerators**: active
drilling stance (×1.5–2 k), friendly/supplied territory (enemy land stalls the supply track),
veteran cadre / amalgame (−30–40% raise penalty, Lynn), a skilled general attached, first-battle-
survived one-time morale drop.
**USER ADDITION (locked):** mobilization is ALSO driven by BUILDINGS & INDUSTRY — railways
(sharply cut concentration delay + supply penalty, the Prussian railway-mobilization theme, phased
in by tech), factories (war-materiel/output feeding readiness), and supply depots (large boost to
the supply/logistics track specifically + raise/removal of the supply floor when near a depot).
This is the concrete van-Creveld depot hook and ties the new buildings (§2–§4) and the `rifles`
good (§13) directly into readiness. Hook point: create_unit / raise_legion (per the create_unit
idiom memory) stamps the green-state and starts the decay tracks. Expands, not replaces, the
existing military-logistics layer.

## 15. AS-BUILT — final implementation of §14 (#191, #192)

The §14 research/design was implemented as follows. Deviations from the design targets are
noted; every deviation is a scope/engine-safety choice, not a change of intent.

### 15a. #191 army/navy OOB — as-built
- **File:** `common/scripted_effects/imp19c_effects_legion_setup.txt`.
- **Army:** `SE_qing_armies` raises ~26 named Banner + Green Standard provincial garrisons via
  `SE_qing_raise_garrison[_cmd]` — dispersed constabulary, matching the §14a "dispersed, not one
  field army" finding, rather than the §14a design's suggested ~8 consolidated named armies. The
  garrison-dispersal form was already the established mod idiom (#66/#190) and reads better on-map;
  the §14a decomposition target is recorded as a possible future consolidation, not a regression.
- **Navy:** `SE_qing_navy` disbands the auto-generated fleets, then raises the THREE historical
  provincial coastal water-forces as weak war-junk brig squadrons:
    - 廣東水師 Guangdong — Canton p:9298, 6× brig
    - 福建水師 Fujian — Fuzhou p:3651, 4× brig (with a largest-coastal-owned-province fallback
      because Fuzhou may be non-coastal in this map's province graph)
    - 浙江水師 Zhejiang — Ningbo p:2893, 3× brig  ← added this session to complete §14a's "3–4 weak
      coastal fleets"
  Each guarded on `exists` + `owner = c:CHI` + `is_coastal`, with `LOG_fail` on a miss. This
  supersedes the §12 two-junk-squadron stopgap.

### 15b. #192 mobilization — as-built (design simplification vs §14b, for engine safety)
- **Files:** `common/modifiers/mobilization_modifiers.txt` (7 unit-scope modifiers),
  `common/scripted_effects/se_MOBILIZATION.txt` (sys=MOBIL), `common/on_action/00_specific_from_code.txt`
  (`on_legion_raised` populated), `localization/english/modifiers_l_english.yml` (+14 keys).
- **Decay model — CHANGED from the §14b continuous `p0·exp(-3t/D)`.** A per-tick variable-decay loop
  and legion-scope variables are BOTH unproven in this engine (oracle-checked vs Invictus +
  Terra-Indomita). Implemented instead as the mod's PROVEN pattern: **staggered self-expiring
  `add_unit_modifier` layers** (like `qing_unit_banner_rot`). Each axis = a heavy RAW layer (short
  duration, expires first) + a lighter SETTLING layer (longer duration) → the penalty STEPS DOWN in a
  discrete approximation of the exp-decay curve. Same behaviour, zero unproven constructs.
- **Axes & durations (days), decided ONCE at legion scope by profile:**
    - regulars, general + supplied home: drill 30/settle 75, cohesion 60/120, supply 90/150, no floor
    - regulars, supplied home no general: 45/90, 90/150, 120/180, no floor
    - regulars, contested/foreign:        60/120, 120/180, 150/240, no floor
    - levy WITH depot/rail support:        60/150, 120/210, 150/300, no floor
    - levy UNSUPPORTED (hasty):            75/180, 150/270, 180/365, + irregular supply floor (730d)
  Roughly: drill fast (~1–2.5mo), cohesion medium (~2–5mo), supply slow (~3–6mo) — matches §14b's
  fast/medium/slow ordering. The continuous per-type `D` targets are approximated by these two-layer
  step schedules.
- **Accelerators — as designed, incl. the USER ADDITION (buildings/industry):**
    - general attached (`any_legion_commander = { is_alive = yes }`)
    - raised in supplied home soil (`unit_location = { owner = mobil_owner  controller = mobil_owner }`)
    - **supply depot** at the muster (`military_depot_building` / `INF_depot` / `arsenal_building`) OR a
      **railway** (`tech_steam_locomotive` / a local `INF_railway_upgrade`) → cuts the levy supply track
      and REMOVES the irregular floor. This is the concrete van-Creveld depot hook tying §2–§4 buildings
      + the `rifles` good to readiness.
    - The "active drilling stance", "veteran cadre/amalgame", and "first-battle morale drop" §14b
      accelerators were NOT built — no proven per-legion stance/veteran hook exists at raise time; recorded
      as deferred, not silently dropped.
- **Game-start exemption:** `on_legion_raised` guards `NOT = { current_date = 1815.7.1 }` so the 1815
  standing establishment (the §15a OOB) is EXEMPT — only genuinely fresh musters break in.
