# DESIGN — #103 follow-up: cottage industry building count visibly matters for Military Supplies (v2, post-review corrections)

## Goal
User built ~20 cottage-industry buildings. The Military Supplies TOPBAR HEADLINE number (a
demand-fulfilment balance, `Σ DEMAND_<good> × (1 − shortage_<good>)`, confirmed the number being
watched) did not move.

## Fix (three parts, all additive, zero Sobisonator code touched)

### Part 1 — new sulphur cottage building — CORRECTED gate (round 2: verified, 2 low-risk notes)
Round 2 verified all 4 province IDs directly (`setup/provinces/00_Anhui.txt:462,552`,
`setup/provinces/00_Qinghai.txt:44,219`) carry `trade_goods="sulphur"` and all 4 resolve to CHI
ownership (`setup/main/00_default.txt`). Two notes for the implementer, not blockers:
- **Copy ALL FOUR of sugarhouse's gate clauses**, not just "province list + trade_goods": culture-
  group check (`owner = { OR = { country_culture_group = jurchen / chinese_group } }`,
  `qing_cottage_buildings.txt:309-314`), `NOT = { has_city_status = yes }` (`:315`),
  `trade_goods = sulphur`, AND the province-ID OR-list. Dropping the culture/city-status clauses
  by only reading "trade_goods + province list" would under-copy the proven template.
- **7200 Xining's CHI ownership is fragile** — it resolves only through a pre-existing brace-
  comment quirk in `00_default.txt`'s `#SHG` block (unrelated to this task, not touched here). If
  that map area is ever fixed independently, this building could silently lose reach there. Not
  a defect in this design; noted so a future session isn't confused.
**Round 1 review found the original province gate (Beitou/Datun, Taiwan) was wrong.** A cottage
building can only BOOST a province's EXISTING trade good via `base_resources`; it cannot create a
new one. The mod's own province data (not the real-world historical geography) determines this.
Checked directly: exactly 4 CHI provinces carry `trade_goods = sulphur` —
**6703 Yuexi and 8425 Ningguo** (`setup/provinces/00_Anhui.txt:462,552`), and
**2167 Zhag'gar and 7200 Xining** (`setup/provinces/00_Qinghai.txt:44,219`). No Taiwan province
has sulphur in this mod's setup. **New building gate: those 4 province IDs, keeping
`trade_goods = sulphur`** — matching `qing_cottage_sugarhouse_building`'s shape exactly (province
ID list PLUS the trade_goods condition), not `qing_timber_lineage_building`'s shape (which drops
the trade_goods check and appears to be a latent, pre-existing mismatch in that building — not a
precedent to copy). Reach is limited (only Anhui/Qinghai governorships gain cottage sulphur), and
that is accurate to this mod's actual geography, not a defect.

### Part 2 — new, wholly fork-owned building-count bonus (does NOT touch COTTAGEIND_pops_output) — CORRECTED
A brand-new effect, `COTTAGEIND_military_goods_building_bonus`, called from
`oa_wealth_changes.txt` immediately AFTER the existing `COTTAGEIND_produce_all = yes` (`:176`) —
a new line, not an edit to any existing line. Confirmed by review: this insertion point is already
inside `every_country { every_governorships { ... } }` (opened `:173`), so the active scope is
correctly governorship — no extra wrap needed.

**Corrected building→good mapping** (review found smithy wrongly included for early_munitions,
and the mapping never referenced the new sulphur building from Part 1):
- early_munitions (0.5×stone+lead+**sulphur**): **quarry (stone) + leadworks (lead) + the new
  sulphur building** — NOT smithy (smithy produces iron, not a munitions input).
- clothing (textile_fibres+silk): weaving_hut + silk_reeling_shed. Unchanged, confirmed correct.
- pharmaceuticals (vegetables+whales[dead]): herbalist only. Unchanged, confirmed correct.
- construction_materials (wood+stone+iron): woodlot + quarry + smithy. Unchanged, confirmed correct.
- **early_artillery: DROPPED from this fix.** Confirmed by review: `MILITARY_supplies_income_
  country` (`INCOME_svalues.txt:1143-1254`) does NOT sum early_artillery at all — it is excluded
  from the topbar headline by the mod's own existing formula (`:1046-1054`). Boosting it here
  cannot move the number this fix targets; including it was an internal contradiction in v1
  (acknowledged the exclusion, then boosted it anyway). Out of scope — a separate, pre-existing
  gap in `INCOME_svalues.txt`'s own formula, not touched under this task.

**Mandatory safety guard (review found this missing — real risk, not hypothetical):** every write
MUST be `change_variable = { name = $good$_stockpile  add = <bonus> }` (never `set_variable`, which
would clobber `COTTAGEIND_scale_production`'s own contribution to the same var), wrapped in
`if = { limit = { has_variable = $good$_stockpile } }` — the ~9 unseeded frontier "Rebels [0]"
governorships lack this var entirely, and an unguarded write there reproduces the exact
"Type: empty" flood this codebase has already fixed elsewhere (`se_COTTAGEIND.txt:189-198`,
`se_CONSUME.txt:47-51`).

**Magnitude — SET (round 4, user direction): derived from the modern-industry per-building
analogs, discounted by this codebase's own cottage-vs-formal ratio, not a fresh guess.**
`GOODS_svalues.txt:2686-2706` already defines flat, UNDISCOUNTED per-building output rates for the
modern factory/works buildings that feed these same goods: `GOODS_arsenal_munitions_output = 2`
and `GOODS_depot_munitions_output = 1` (both → early_munitions, `GOODS_governorship_munitions_
infra_output_compute:2771-2812`, added straight into the mechanised term with NO industrialisation/
employment multiplier — a genuinely flat per-building add, the same shape Part 2 needs) and
`GOODS_machine_works_munitions_output = 3` (→ early_munitions), `GOODS_textile_mill_clothing_
output = 2` (→ clothing). Average of the 4 directly-analogous rates ≈ 2.
Cottage is confirmed far less productive than these — NOT because the raw-material pipeline is
broken (round 4 found it is NOT: `COTTAGEIND_raw_stone/lead/sulphur/textile_fibres/silk/
vegetables/wood/iron/copper/tin` in `COTTAGEIND_cache_all_values` already read `GOODS_governorship_
<good>_produced`, which sums `num_goods_produced` per province — the SAME engine stat `base_
resources` on a cottage building raises, exactly like `qing_production_buildings.txt`'s modern
works. So a cottage quarry/leadworks/weaving_hut/etc. already raises `COTTAGEIND_raw_stone`/etc.,
which already reaches `early_munitions_stockpile`/`clothing_stockpile` via the existing
`COTTAGEIND_produce_early_munitions`/`_clothing`/`_pharmaceuticals`/`_construction_materials` →
`COTTAGEIND_scale_production` chain — this is real, Sobisonator-original, and not the bug). The
actual reason it reads as "not contributing" is MAGNITUDE: that existing path multiplies by
`COTTAGEIND_pops_output` (which itself carries the ×0.1 cottage-discount the codebase already
established and this task does not touch), then `×0.5` efficiency and `×TECH_cottage_industry_
overall_bonus` again in `COTTAGEIND_scale_production` — compounding discounts that can render ~20
buildings' contribution too small to read on the topbar. Part 2's flat per-building bonus is a
DIRECT, undiscounted supplement (mirroring the arsenal/depot's own undiscounted-flat-add
precedent), not a duplicate of the existing weak pipeline.
**Rate: applying this same codebase's own already-established cottage-discount ratio (×0.1, from
`COTTAGEIND_pops_output`) to the modern per-building average (≈2) gives 0.2 per building** — traced
to two numbers already in the repo, not invented. `+0.2` per building, uniform across all 4 mapped
goods (early_munitions, clothing, pharmaceuticals, construction_materials) — pharmaceuticals/
construction_materials have no modern flat-building analog to anchor to individually, so they take
the same derived rate for consistency rather than a second, ungrounded guess.

### Part 3 — comprehensive logging (matches the #102 tariffs-fix pattern) — CORRECTED for scope
Add exact-tick `ECON_LOG_curx_*`-style metrics, reusing the EXACT scope-safe idiom this session's
own #102 fix established (`se_ECON_LOG.txt:882-911`'s rewrite, forced by the same class of bug):
- `shortage_<good>` (early_munitions, clothing, pharmaceuticals, construction_materials — NOT
  early_artillery, dropped per Part 2) and `COTTAGEIND_produced_<good>` are BOTH
  GOVERNORSHIP-scoped (`se_CONSUME.txt:10/20/45`) and sometimes REMOVED entirely on surplus
  (`se_CONSUME.txt:111`) — MUST read via `every_governorships` + `save_scope_as` + `owner = {
  change_variable = { add = scope:<saved>.var:<field> } }`, each `has_variable`-guarded, exactly
  like the #102 probe fix. Reading these at country scope directly would repeat that exact bug
  (all-zero data).
- **CORRECTED (round 2 found a real coherence defect):** do NOT log `MILITARY_supplies_country`
  as the primary headline metric. It is a FLOORED, ACCUMULATING STOCK (`se_TEST.txt:373-376`),
  refreshed at quarter-OPEN by `MILITARY_update_supplies` (`oa_wealth_changes.txt:208`) — a
  DIFFERENT on_action pass than the consume step (`:339-344`) this probe places after, so reading
  it post-consume is a full quarter STALE relative to the co-logged `shortage_<good>`. It is also
  not the quantity the Goal names (`Σ DEMAND × (1−shortage)`, the per-quarter INFLOW) — it can sit
  pinned at 0 (chronic deficit) or saturated (chronic surplus), in which case added production is
  invisible in the stock regardless of whether it moved the inflow. This mismatch could itself be
  why the original complaint saw no change — the design must be able to tell "production didn't
  rise" apart from "production rose but the floored stock display can't show it."
  **Instead, log `MILITARY_supplies_income_country` (the actual per-quarter inflow, the formula
  named in this doc's Goal) AND `MILITARY_supplies_balance_country` (net balance) — both are
  on-demand script_values, so reading them after the consume pass reflects THIS quarter's real
  numbers, same-tick coherent with the shortage metrics.** Also still log
  `MILITARY_supplies_country` itself (country-scoped, direct read, no iteration) as a secondary
  metric, so the design can distinguish "the inflow moved" from "the floored stock display didn't
  show it" — the two different failure modes this correction exists to tell apart.
- **Placement:** after the quarterly consume pass (`quarterly_apply_trade_changes_and_consume`,
  `oa_wealth_changes.txt:339-344`), so the shortage read reflects that quarter's real consumption,
  not a stale pre-consume value.

## Explicitly NOT done
- `COTTAGEIND_scale` / `COTTAGEIND_pops_output`'s `×0.1`: untouched, per standing instruction.
- `early_artillery`'s topbar exclusion: not fixed — a separate, pre-existing formula gap, out of
  scope. (Also dropped from Part 2's boost, since boosting it can never move the headline anyway.)
- Whales-producing building: not added — whales is defunct/remapped
  (`common/trade_goods/00_imp19c.txt:227`); a building for it would be pointless.
- Setup province files are NOT edited to add sulphur anywhere new — Part 1 uses the mod's existing
  4 sulphur provinces as-is.

## Resolved from round 1 review
1. Sulphur province gate corrected (Anhui/Qinghai, not Taiwan) — real, verified in-game data.
2. early_munitions mapping corrected (dropped smithy, added the new sulphur building).
3. Mandatory `has_variable` guard + `change_variable add` (never `set_variable`) specified.
4. early_artillery dropped entirely from Part 2 (cannot move the targeted headline).
5. Part 3 scope corrected — explicit governorship-iteration idiom for the two governorship-scoped
   metrics, matching the #102 probe-fix pattern precisely.
6. Magnitude sequencing fixed: log first, then size the constant from real numbers, not a guess.

## Round 3 review: CONFIRMED, ready for implementation. Three precision notes applied:
1. **File path**: `common/on_action/economy/oa_wealth_changes.txt` (not the bare filename).
2. **Placement scope**: the consume pass at `:339-344` runs INSIDE a nested `every_governorships {
   }` block spanning `:342-347`. The country-scope Part 3 metrics (`income`/`balance`/
   `MILITARY_supplies_country`) must be placed AFTER that block closes at `:347`, in the
   country-scope tail (`:348-385`) — not literally "at line 345," which is still governorship
   scope. The governorship-scoped metrics (`shortage_<good>`, `COTTAGEIND_produced_<good>`) use
   their own `every_governorships`+`save_scope_as` iteration per the #102 idiom, so they are
   unaffected by this clarification.
3. Confirmed: `COTTAGEIND_scale_production` already accumulates via `change_variable` (`se_
   COTTAGEIND.txt:186-198`), consistent with Part 2's own guard requirement — no other site resets
   `$good$_stockpile` between the new bonus write and consume.
