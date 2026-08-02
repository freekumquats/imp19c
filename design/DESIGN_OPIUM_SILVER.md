# DESIGN — Silver/Opium Balance-of-Trade Monetary Model (白銀外流 / 鴉片貿易) — task #366

**Branch:** merge-overnight. **Status:** BUILT (both oracle probes returned NOT-PROVEN; the engine is
authored to the low-risk verdict — time-ramp import intensity + aggregate addiction counter). Ships as:
`se_QING_OPIUM.txt` (engine), `qing_opium_events.txt` (.1 silver-drain memorial / .2 Humen reckoning /
.3 treaty legalization / .4 epidemic crisis), `QING_opium_panel.txt` + `qing_opium.gui` (L4 panel),
`qing_opium_modifiers.txt` (epidemic bands), `qing_opium_l_english.yml`. Wiring: `QING_opium_init` in
`qing_mechanics_on_actions.txt` (after `QING_xj_init`); `QING_opium_assess_trade_balance` called in
`QING_DECLINE_pulse` BEFORE `update_currency_stress`; `QING_opium_pulse` after the concrete-object
hangers; open button in `government_view.gui` (`menu_trade.dds` icon — `menu_economy.dds` does not exist).
The D3 Grand-Council fold is satisfied transitively (see §2). No `se_DEMAND.txt` edit was needed — the
opium demand is modelled entirely by the import-index ramp, not a trade-goods demand term.

## 1. Thesis — layer a CONCRETE trade-flow feed onto the EXISTING currency-stress engine

The mod already models the *symptom* (a `qing_currency_stress` 0..100 meter that drifts off the live
reserve ratio) but not the *cause* (the silver a trade surplus earns, or an opium drain bleeds). #366
supplies the cause: a quarterly balance-of-trade assessment that computes a net silver flow and feeds
it into `qing_currency_stress` as an additive nudge — the same meter, now driven by a real economic
signal instead of pure reserve-ratio drift.

This is the **layer-don't-duplicate** archetype (same as #367 → the Xinjiang control meter): #366 owns
NO new stress meter, NO new band machinery, NO new modifier appliers on the stress side. It computes
"how much silver flowed this quarter" and nudges the existing counter. The existing
`QING_DECLINE_apply_currency_band` then bands it onto the country for free, and the existing
`qing_decline.*` / `qing_treaty.1` (Nanjing-moment, gated on `qing_currency_stress >= 40`) events fire
off it unchanged.

## 2. The Grand-Council fold is ALREADY WIRED (D3 requirement satisfied transitively)

`QING_ministry_recompute_perf_revenue` (se_QING_MINISTRY.txt:520-527, term **d**) already subtracts
`qing_currency_stress / 6` from the Board of Revenue minister's performance meter
(`qing_min_perf_revenue`), which folds into his Grand Council standing via
`QING_council_fold_ministry_perf`. So the opium drain reaches the office-holder's council standing
**transitively and correctly**: opium net-drain → `qing_currency_stress` (term A of the decline suite)
→ `qing_min_perf_revenue` term (d) → `qing_council_eff_target`. #366 adds NO new fold; it makes the
existing silver-crisis-drag term reflect a real trade balance. The Board of Revenue (戶部) is the
historically correct office — it owned the response to the 19th-c. silver crisis (銀荒/銀貴錢賤).

## 3. Proven integration primitives (all verified in-repo before authoring)

- **Per-good national production** — `GOODS_national_production_{tea,silk,porcelain,opium}` are
  country-scope script values (GOODS_svalues.txt:195/217/276/364), each summing
  `GOODS_governorship_<good>_produced` over `every_governorships`. Read into a var via the proven
  `set_variable = { name = x  value = GOODS_national_production_tea }` staging pattern
  (mirrors CURR_STRESS_update's reserve-ratio read).
- **Stress nudge** — `QING_DECLINE_nudge = { var = qing_currency_stress  amount = N }` (clamps 0..100,
  self-inits). Additive; safe to call each quarter.
- **Quarterly cadence** — the assessment rides `QING_DECLINE_pulse` (00_monthly_country.txt:75,
  CHI-only, human-gated, 90-day cooldown). It runs BEFORE `QING_DECLINE_update_currency_stress` so the
  reserve-ratio drift and the trade-flow nudge compound in the same pulse.
- **GBR sphere influence** — `britain_influence` per-state var (se_QING_SPHERE.txt) is the fallback for
  the opium-import intensity if the engine has no cross-country trade-flow read (probe 1).
- **Treaty flag** — `qing_treaty_system_imposed` (se_QING_TREATIES.txt:35) gates legal vs smuggled
  opium; `qing_treaty_ports` counts opened ports.
- **GP tension** — `QING_gp_react = { power = britain  tag = GBR  severity = N }` (se_QING_DIPLO.txt)
  is the proven verb to spike GBR tension on a Lin Zexu crackdown; `QING_gp_grip_grace` refunds it
  pre-consolidation. Lin Zexu's destruction of the opium is a bold move → aggressive expansion + GBR
  opinion drop, exactly what QING_gp_react models.

## 3b. PROBE VERDICTS (oracle-confirmed, both point to the low-risk approach)

- **Probe 1 — cross-country trade flows: NOT PROVEN.** The engine has no per-partner/per-destination
  trade matrix (no `trade_route` data iterator, no `import_from_country`). Proven reads are aggregate
  only (`is_importing_trade_good`, `country_trade_good_exports = { target=..  value.. }`,
  province `num_goods_produced`, and the mod's own `GOODS_national_production_*` country svalues).
  → **Decision:** opium-import intensity is driven by a **historical TIME RAMP** (opium imports grew
  exponentially 1763→1838 as British Bengal "country trade", a process external to the Qing frontier
  spheres), NOT the `britain_influence` sphere var. That var was the design's tentative fallback, but
  the sphere ring is the *Inner Asian land frontier* (se_QING_SPHERE.txt builds it from land-neighbour
  + subject-march states) — geographically wrong for a *maritime Canton* opium trade. The time ramp is
  the historically faithful driver; treaty ports, player posture, and domestic-production toggle
  MODULATE it. Export inflow uses `GOODS_national_production_{tea,silk,porcelain}` (proven, real, and
  correctly reflects the Qing's actual export economy).
- **Probe 2 — per-pop addiction flag: NOT PROVEN.** No `set_variable` on pop scope, no
  `add_pop_modifier` upstream. → **Decision:** addiction is an **aggregate country counter**
  `qing_opium_addicted_share` (0..100) + **province-modifier bands** (`qing_opium_epidemic_low/_high`,
  the proven corruption-band pattern) stamped on opium-relevant provinces. Feeds `qing_sect_pressure`
  (White Lotus / Taiping recruited among addicts) and a productivity/unrest drag.

## 4. The trade-balance formula (calibrated to Dermigny/Hsü magnitudes)

Historiography checkpoints (net silver flow, taels/yr): **1763 ≈ +19.5M (healthy)** · 1820 ≈ +12M
(strain) · **1838 ≈ +5M then negative (crisis)**. Baseline healthy inflow ≈ 20M taels/yr; peak opium
drain ≈ 10M taels/yr (40k chests × ~250 taels). Lin Zexu 1839 = 20k chests destroyed; opium NOT
legalized until the 1858 Treaty of Tianjin; domestic Yunnan/Sichuan production rises 1850s+.

```
net_silver_flow (quarter) = export_inflow − opium_outflow

export_inflow  = (tea + silk + porcelain national production) × export_price_factor
                 scaled so a healthy 1763 surplus is a large POSITIVE
opium_outflow  = opium_intensity × drain_factor
                 opium_intensity = (pre-treaty)  britain_influence-weighted smuggling volume
                                   (post-treaty) legal import volume (taxed, larger, but revenue offsets)
```

The net flow is normalised to a small signed nudge on the 0..100 stress meter each quarter:
surplus (1763 zenith) nudges stress DOWN toward 0; drain (post-1820s opium crisis) nudges it UP.
Exact scaling locked once the historiography agent returns tael magnitudes (≈+20M taels/yr 1763
surplus vs ≈−10M taels/yr 1838 drain per Dermigny/Hsü). The High Qing era flag (`qing_high_qing_era`,
pre-1775) means the opium term is near-zero at a 1763 start — historically opium imports were
negligible (<1k chests/yr) until the 1820s.

## 5. Policy tree (player-facing levers, in the L4 opium panel)

- **Prohibition posture** (pre-treaty): PROHIBIT (legitimacy, but smuggling largely unabated — interdiction
  RNG) vs TOLERATE-FOR-REVENUE (opium taxed, currency-drain continues, corruption up).
- **Lin Zexu crackdown** (event, fitness-gated commissioner): DESTROY seized opium → legitimacy +
  GBR fury (QING_gp_react britain) vs RELEASE → drain continues. Historically 1839 Guangzhou.
- **Treaty legalization** (forced, post-Opium-War, gated on `qing_treaty_system_imposed`): opium legal
  but taxed — a revenue offset that eases the fisc while the addiction epidemic worsens.
- **Domestic production** (Yunnan/Sichuan, 1850s+): substitute-import reduces silver outflow but
  deepens the addiction epidemic at home.

## 6. Addiction model — SHAPE TBD from probe 2

Either: (a) per-pop `has_opium_addiction` flag if pop-scope variables are proven; OR (b) an aggregate
`qing_opium_addicted_share` 0..100 country counter + province-modifier bands
(`qing_opium_epidemic_low/_high`, same pattern as the corruption bands). Recommendation pending; the
aggregate counter is the low-risk default and is almost certainly what ships. Addiction feeds
`qing_sect_pressure` (White Lotus recruited among addicts) and a productivity/unrest drag.

## 7. File list (to author to the probe verdicts)

- NEW `common/scripted_effects/se_QING_OPIUM.txt` — QING_opium_init, QING_opium_assess_trade_balance
  (the quarterly calc + stress nudge), QING_opium_addiction_pulse, prohibition/crackdown/legalization
  verbs, QING_opium_pulse.
- NEW `events/imp19c_mod_events/qing_opium_events.txt` — the crisis/policy event chain.
- NEW `common/scripted_guis/QING_opium_panel.txt` + `gui/qing_opium.gui` — the L4 policy panel
  (Grand-Council clone), trade-balance read-out, policy toggles, Lin Zexu button.
- NEW `common/modifiers/qing_opium_modifiers.txt` — prohibition/tolerate/legalized postures + addiction bands.
- NEW `localization/english/qing_opium_l_english.yml`.
- EDIT `se_QING_DECLINE.txt` — call QING_opium_assess_trade_balance inside QING_DECLINE_pulse (before
  update_currency_stress). EDIT `se_DEMAND.txt` — opium demand conditional on posture (if needed).
  EDIT `government_view.gui` — the panel open button.
```
