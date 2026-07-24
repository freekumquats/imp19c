# Upstream Bugs (Sobisonator) — report + fix 10× carefully

Bugs found in the boot-test logs whose offending lines are authored by **Sobisonator** (upstream, remote-tracked), NOT the fork (freekumquats). Per standing rule: these are NOT ignored — they must be **reported upstream** AND fixed, but any fix must be **10× more careful and precise** than a fork bug (minimal, surgical, provably behaviour-preserving on the working path, heavily reviewed). Diagnosed 2026-07-24 from the 01:28 boot logs.

---

## U1 — WEALTH_cost_of_living unset-var flood (127,778 errors = 99.8% of error.log)

- **File:** `common/script_values/WEALTH_svalues.txt` (~lines 1360–1382, the `WEALTH_cost_of_living` svalue)
- **Blame:** Sobisonator, commit `e6f38e7425` (2025-09-01)
- **Root cause:** The `else` branch (for countries WITHOUT `official_currency`) sums 12 `var:country_unit_price_*` (grain/livestock/fish/…/luxury_furniture). Those price vars are only reliably set on currency countries / countries actively trading each good (set by `GT_split_get_country_import_unit_price_all` over `every_tradegood_$type$_complex`). On the ~300 non-currency / low-trade countries they are unset → "Failed to fetch variable … due to not being set" every evaluation.
- **Frequency:** clusters at game load (~24k) AND recurs each quarterly economy pulse (~13k at 01:41) → the dominant contents of the 40 MB error.log.
- **NOT just log spam — load-bearing:** `WEALTH_cost_of_living` feeds
  - pop income for upper/middle strata (`INCOME_svalues.txt:242,256`),
  - the cost-of-living crisis event (`events/imp19c_mod_events/economy/cost_of_living_events.txt:148/155/200`, `DEMAND_luxury_svalues.txt:36`),
  - the per-governorship cost-of-living shown in `gui/province_window.gui:4226/4284`.
  So every non-currency country computes cost-of-living from unset/garbage price data → wrong pop income, spurious/missing crisis events, wrong UI number.
- **Fix direction (NOT yet applied — needs 10× care):** do NOT naively guard-to-zero (that would zero non-currency cost-of-living → inflate pop income). Options: (a) guard each `var:` read to a sensible non-zero default; (b) ensure `country_unit_price_*` is populated for all goods on all countries before cost-of-living is read; (c) reorder pulse so trade-split prices exist first. Must confirm whether the vars are genuinely never-set vs set-late (ordering) before choosing. The `if`-branch (currency countries) MUST remain byte-identical.

## U2 — remove_country_modifier on non-existent INCOME modifiers (28×4 = 112 errors)

- **File:** `common/scripted_effects/se_INCOME.txt:407+` (`remove_country_modifier = INCOME_$category$_00_modifier` etc.)
- **Blame:** Sobisonator, commit `703da7c08d`
- **Root cause:** removes `INCOME_tariffs_N_modifier` / `INCOME_property_tax_N_modifier` / `INCOME_income_tax_N_modifier` / `INCOME_excise_duty_essentials_N_modifier` that are not present in the ProvinceModifier database at removal time (never added, or wrong db/scope). Error: `Cannot find INCOME_*_modifier in ProvinceModifier database`.
- **Impact:** low — a failed removal is a no-op; log noise, no known gameplay effect. Verify the modifiers are defined and added somewhere before concluding.

## U3 — pdx_persistent_reader unexpected-token flood (422 is_triggered_only + 136 secondary + misc)

- **Reader:** `pdx_persistent_reader.cpp:229` (the save/history persistent reader, engine-level)
- **Files:** ~80 event files across the mod incl. untouched base ones (fra_revolution, pru_ascendancy, ChineseEvents, gbr_empire, …) — uniform, identical count across boots.
- **Root cause:** the persistent (save/history) reader is parsing event-grammar files it doesn't understand (`is_triggered_only`, `secondary`, modifier keys, custom triggers like `IND_resource_gathering_operation`). Not the event loader — events fire fine in-game.
- **Assessment:** engine/save-path systemic noise, almost certainly benign. Report upstream; likely not patchable at the mod level. Do NOT chase per-file.

## U4 — CURRENCY/DIPLOMACY svalues read unset vars on non-currency countries (~130k errors, the 01:41 flood)

- **Files & top sites (all blame Sobisonator, 2024):**
  - `common/script_values/DIPLOMACY_svalues.txt:100` — 22,638 (`else` branch, `Value of wrong type … Got value of type 'none'`)
  - `common/script_values/CURRENCY_svalues.txt` cluster: `:653` (18,767), `:505/510/514/527/532/536/560` (~18,228 each — the `*_scaled` svalues reading `var:CURRENCY_national_debt_*` and `var:CURRENCY_amt_circulated_*`), `:910` (13,230, `owner.CURRENCY_minting_rate_wealth_value`), `:381` (5,733, `CURRENCY_reserve_ratio_total`).
- **Root cause:** the currency system is scoped to the 8 Great Powers (CHI/GBR/FRA/RUS/SPA/TUR/POL/SAX) that carry an `official_currency`. The ~300 minor countries have no `official_currency` **by design** (confirmed earlier), so `var:CURRENCY_*` / `var:gold_reserve_size` / `var:*_amt_circulated_*` are never set on them. The `*_scaled` svalues and the DIPLOMACY:100 `else` read those vars unconditionally → "Value of wrong type … 'none'" / "returned an unset scope" on every non-currency country, every economy pulse.
- **Answer to the user's question ("why are other countries not setting gold reserves / currency?"):** they are not *supposed* to — currency/reserves are a Great-Power-only subsystem. The minor economies run on the pop/trade/production sim without a minted currency layer. The errors are the currency svalues being *evaluated* for countries that legitimately have no currency, not a failure to seed reserves. A correct fix guards each currency svalue on `has_variable = official_currency` (or the specific var) and returns 0/neutral when absent — but per 10× rule the currency-country path must stay byte-identical, and we must confirm no minor-country consumer actually needs a non-zero fallback.
- **Impact:** massive log volume; on the working (Great-Power) path the numbers are correct. For minors these svalues resolve to engine-default 0, which is the intended "no currency" behaviour — so likely log-noise, but must be verified before applying any guard.
- **Fix:** NOT applied (upstream, 10× care). Report upstream.

---

### Not upstream, not fork — vanilla/base (ignore)
- `tetrere` / `octere` / `liburnian` "Failed to read key reference … from database" (137 each) — vanilla naval unit types referenced by vanilla deity naval-apotheosis. Base game.
- debug.log "missing valid file magix, defaulting to TEXT" — normal for text setup files.
- database_conflicts.log "Overriding entry" — intentional mod-over-vanilla overrides.
