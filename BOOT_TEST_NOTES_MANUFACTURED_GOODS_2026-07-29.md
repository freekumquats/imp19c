# Boot Test Notes — manufactured_goods branch

Branch: `manufactured_goods` | HEAD: `c9bd073fc`
Baseline: `master`. Untested commits = everything in `git log master..manufactured_goods`.
Test machine: separate box (see [[imp19c-testing-on-other-machine]]) — must be pushed (all pushed).

Boot with `-debug_mode` so LOG emits. Logs land in `~/Downloads` (error.log is huge — narrow with patterns).
NOTE: `~/Downloads/error.log` may be a PRE-FIX baseline — trust git HEAD, not stale logs ([[imp19c-stale-log-vs-git-rule]]).

This is a CHECKLIST ONLY (per request). No investigation / no fixes until told.

---

## Owed boot-tests by increment (all "boot-test owed" markers from manufactured_goods.md §6)

- [ ] **I2** — 4 pre-wired goods (split-writer D1a live): clothing, luxury_clothing, machine_parts, alcohol — verify no cottage double-count, output sane
- [ ] **I5** — employment scaling live for the 4 pre-wired goods: verify factory output delta vs employment fill-ratio
- [ ] **I6** — 20 newly un-gated goods actually produce once factories assigned; inert at 0 factories (no phantom output)
- [ ] **I7** — prices for all 24 producible goods compute (no zero/NaN, no div-0); input-cost factoring reads global_mean_price_*
- [ ] **I8** — manufacturing wealth routes to workers: proletariat_wealth + lower_strata_wealth credited from factory income; owners still dominant
- [ ] **I9** — loc/GUI tooltips: all 24 PRODUCED_TT render, ingredient submacros resolve, no raw `$macro$` keys, no `NONE DESC`; rare_alloys NAME+DESC show
- [ ] **I10** — steel cottage recipe: artisan steel is a TRICKLE pre-industrialisation; does NOT flood market; does NOT trivialise Bessemer unlock (efficiency 0.35 sanity)
- [ ] **I11** — DEMAND-layer fixes bite once factories exist:
  - [ ] naval_supplies factory draws bronze demand (FIX A) — no more undefined-svalue log for INDUSTRY_naval_supplies_parts_bronze
  - [ ] glass factory draws coal + stone demand (FIX B1/B2)
  - [ ] early_artillery factory draws textile_fibres demand (FIX C)

## Log-flood / error scans (patterns to grep in error.log)

- [ ] `INDUSTRY_naval_supplies_parts_bronze` — must be ZERO (I11 FIX A removed the dangling ref)
- [ ] Any `Undefined script value` / `Unknown` referencing GOODS_/INDUSTRY_/DEMAND_/COTTAGEIND_/WEALTH_ names
- [ ] `WEALTH_rare_alloys_durability` — should resolve (added I5.5); no undefined-svalue flood in quarterly WEALTH loop
- [ ] COTTAGEIND_raw_coal — resolves (I10 added it to cache); steel recipe reads it without error
- [ ] Currency / wealth read-before-set floods (the U4 class) — confirm none reappeared

## Sanity / balance observations to jot (not asserting bugs — just record numbers)

- [ ] Steel stockpile growth rate at game-start (cottage-only) vs after a steel factory — should be a large jump
- [ ] Any good with runaway stockpile (missing consumption sink) or stuck-at-zero (missing production)
- [ ] Price stability across first few quarters (no wild swings from mis-scaled DEMAND)
- [ ] proletariat_wealth not draining to floor / not ratcheting (I8 distributor fix)

---

## Log floods (from `~/Downloads/logs.zip`, 2026-07-29 17:xx test box; error.log 296,979 lines) — DIAGNOSED + FIXED

Two MG-caused floods dominated the log (together the bulk of the 80,537 "Script system error!" +
35,380 "unset scope" wrapper lines). Both FIXED (uncommitted, pending review):

- **FLOOD #1 — `trade_share_manufacturing_*` (29,488 hits = 8 strata × 3,686).** Root cause: the
  manufacturing `GT_split_calculate_trade_shares` call in `GT_split_calculate_all_trade_shares`
  (se_GLOBALTRADE_split.txt ~3853) was MISSING its `category = manufacturing` arg (unlike the
  resource_extraction/shipping siblings), so `$category$` expanded EMPTY and it wrote `trade_share__*`;
  the distributor read `trade_share_manufacturing_*` unset. Also meant I8's whole point (routing mfg
  income to workers) was a silent no-op. FIX: added `category = manufacturing`.
- **FLOOD #2 — `rare_alloys` asymmetry (~10,850 hits): `global_base_import_price_rare_alloys` 2,769;
  `wealth_owed_for_rare_alloys` 1,843; `income_due_rare_alloys` 1,843; `DEMAND_country_rare_alloys`
  target-link 50; `TRADE_governorship_for_export_internal_rare_alloys` 7; etc.** Root cause: I5.5
  registered rare_alloys in the SINGULAR master `tradegood` injector only — missing from the PLURAL
  `tradegoods` and CATEGORY `tradegood_3` injector lists (so per-category setters skipped it while
  master-list readers hit it), AND missing 12 of the 26 per-good svalue stems its cat-3 sibling
  `electronics` has. FIX: added rare_alloys to both injector lists + cloned all 14 missing svalues
  (`DEMAND_country`, `GOODS_national_production` + sum entry, and the 12 electronics-parity stems
  across DEMAND/GOODS/PRICE/AI/TRADE _svalues.txt). Verified FULL electronics parity + all deps resolve.

Residual/pre-existing (NOT MG-caused, out of scope, noted only): uniform 18× `INDUSTRY_factories_assigned_*`
unset for ALL 24 goods (setup-ordering, flag-only guard); `cattle`/`livestock` flag mismatch (split 3491
vs 3600); bimetallic `_silver_reserves`→`_gold_reserves` multiply typo (5437); merge-overnight baseline
floods #13-17 (tetrere/is_triggered_only/religion-scope/TRADE_national_expenditure) all present in the
merge-overnight box too.

Linear read of se_GLOBALTRADE_split.txt (1–5984, per user request) COMPLETE — no further MG bugs found.

## Findings

| # | Increment | Severity | Symptom | Repro / where | Status |
|---|-----------|----------|---------|---------------|--------|
| MG-1 | trade goods loc | BROKEN | Some trade goods are MISSING DESCRIPTIONS in the trade-goods list/UI. (`porcelain` + `rifles` confirmed PRESENT in the list — this is about OTHER goods showing blank/absent descriptions.) Which specific goods TBD — user to note keys if visible; otherwise triage from loc files when told to fix. | Trade-goods list / good tooltip. Reported during manufactured_goods boot test. | OPEN — not investigated (list-only) |
| MG-2 | trade goods loc | BROKEN | Some trade goods have NON-CAPITALIZED display names (e.g. name shows lowercase like "porcelain"/"rifles" style rather than "Porcelain"). Indicates missing/lowercased loc name entries — likely the same goods that are missing descriptions (MG-1), or a broader set. Which specific goods TBD. | Trade-goods list / good name label. Reported during manufactured_goods boot test. | OPEN — not investigated (list-only) |
| MG-3 | trade goods effects | BROKEN | ALL trade goods give the SAME "Local Monthly Amenities" modifier — wrong. Each trade good should grant a DIFFERENT/good-appropriate modifier (its own province/state effect), not a shared identical amenities bonus. Suggests goods were defined with a copy-pasted `province`/effect block (cf. the shared `local_monthly_food = 0.07` byproduct convention on porcelain/rifles — likely the same template applied everywhere, or an amenities equivalent). | Trade-good tooltip / province effect from owning the good. Reported during manufactured_goods boot test. | OPEN — not investigated (list-only) |

### MG-3 reference — proven upstream pattern (Terra Indomita + Invictus)

Both oracles give EACH good a DISTINCT pair: a `province = { ... }` local modifier **and** a `country = { ... }` global effect, thematically matched to the good. Structural template every good follows:

```
<good> = {
	category = <0-5>
	gold = <base value>
	province = { <one local modifier appropriate to the good> }
	country  = { <one global effect appropriate to the good> }
	color = ...
}
```

Concrete examples to model imp19c's goods on:
- **TI `porcelain`** — `province = { local_nobles_output = 0.03 }`, `country = { stability_monthly_decay = -0.0001 }` (luxury → elite output + prestige/stability). Direct precedent for OUR `porcelain`.
- **TI `wootz_steel`** (strategic metal, precedent for OUR `rifles`/steel) — `province = { local_tax_modifier = 0.02 }`, `country = { heavy_infantry_offensive = 0.1 ... }` (military-good → combat bonus).
- **TI/Invictus `iron`** — `province = { local_tax_modifier = 0.02 }`, `country = { <unit>_discipline }` + `allow_unit_type = heavy_infantry`.
- **TI/Invictus `salt`/`wine`** — `province = { local_freemen_happyness = happiness_small_svalue }`, `country = { army_maintenance_cost = -0.05 }`.
- **`grain`/`rice`/`fish`** — food goods: `province = { local_monthly_food = N }`, `country = { global_monthly_food_modifier / happyness }`.
- **TI `tea`** — `province = { local_citizen_output = 0.03 }`, `country = { global_monthly_civilization = 0.01 }`.
- **`horses`/`wood`** — `allow_unit_type = ...` + a matching combat/logistics effect.

TI files: `/Users/alan.chiang/github.com/dementive/Terra-Indomita/common/trade_goods/{00_default.txt,00_TI_goods.txt}`.
Invictus: `/Users/alan.chiang/github.com/SnowletTV/Invictus/common/trade_goods/00_default.txt`.

FIX SHAPE (when told to fix): give each imp19c good in `common/trade_goods/00_imp19c.txt` its own thematically-appropriate `province` + `country` block (strategic → military/tax, luxury → elite output/prestige, food → food yield, raw → output/build/manpower), instead of the shared amenities modifier. Category-tier meaning (0-5) and `happiness_*_svalue` named values are proven upstream.

| MG-4 | loyal cohorts event | BROKEN | Event(s) that GRANT a regional governor loyal cohorts do NOT actually add any loyal cohorts — the effect fires (event appears) but no loyal cohorts materialise on the governor's legion. Likely NOT MG-branch work (loyal-cohorts is a separate governor/military mechanic; see [[imp19c-loyal-cohorts-mechanic]] — verified idiom is `add_loyal_veterans` + `set_personal_loyalty = root.commander`). Candidate causes to check when fixing: effect scoped to wrong character/unit, governor has no legion to attach to, or `add_loyal_veterans`/`create_unit` not actually invoked. | Regional-governor loyalty/cohort event. Reported during manufactured_goods boot test. | OPEN — not investigated (list-only) |
| MG-5 | Personnel/governor dispute event | BROKEN | Event for a dispute between the Minister of Personnel and a regional governor: selecting the "recall the governor" option does NOT actually remove the governor from office — governor stays seated after the recall choice. Effect on that option is a no-op or mis-scoped. Likely NOT MG-branch work (GC/ministry mechanic). Candidate causes to check when fixing: the office-vacate effect not invoked, wrong char/office scope, or governor-role removal verb missing/incorrect. Cross-ref GC office-holder model ([[imp19c-grand-council-office-redesign]]) + Titles-Unassigned regression (merge-overnight #10). | Minister-of-Personnel vs regional-governor event, recall option. Reported during manufactured_goods boot test. | OPEN — not investigated (list-only) |

<!-- Severity: CRASH / BROKEN / COSMETIC / NIT -->
<!-- List only for now; triage root cause from the diff when told to fix. -->

## Cross-references (owed elsewhere, NOT this branch's MG work)

- [ ] **#129** military-traditions boot test still OWED (7 trees filled to 20; commit 0c56dfb2b) — separate feature
- [ ] merge-overnight branch has its own open findings — see `BOOT_TEST_NOTES.md` (#2 strata icons, #3 indentured loc still OPEN)
