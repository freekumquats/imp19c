# ECON_BUILD.md — Concrete build spec for three economy systems

**Status:** SPEC / for review. Nothing here has been written into the live economy
files yet. Every effect body below references symbols verified to exist in the repo
(file + line cited). Places where a value must be *confirmed* rather than invented are
called out with **⚠ CONFIRM**.

Three systems, deliberately ordered so each de-risks the next:

1. **§1 `se_ECON_LOG`** — economic diagnostic tracing (the validation loop). Build first;
   it's how we tell whether §2/§3 produce sane numbers.
2. **§2 Employment → Wages activation** — the `JOBS_pulse` that connects the already-built
   `JOBS_svalues.txt` wage math to pop wealth via the existing `WEALTH_*` pending-change idiom.
3. **§3 Currency-crisis event layer** — threshold reads over the existing `CURRENCY_*` meters,
   plus the DD8 China silver/copper debasement crisis.

---

## Ground truth (verified symbols these builds stand on)

| Symbol | Scope | File:line | Role |
|---|---|---|---|
| `LOG_line/enter/exit/state/fail/ok` | any | `se_LOG.txt:27-78` | logging macros, no-op outside `-debug_mode` |
| `JOBS_wages_due_all` | governorship | `JOBS_svalues.txt:148` | sum of all `WEALTH_wages_due_*` (guarded on `official_currency`) |
| `JOBS_wages_due_middle_strata` / `_proletariat` | governorship | `:210` / `:219` | wage split by strata share of pop |
| `JOBS_wages_expense_upper_strata` | governorship | `:228` | owner-borne share (gated on `state_pays_wages_*` flags) |
| `JOBS_wages_expense_the_state` | governorship | `:281` | treasury-borne share |
| `JOBS_available_slots` / `JOBS_num_used_slots` / `JOBS_unemployed_pops_province` | province/gov | `:402/:346/:351` | employment counts |
| `WEALTH_modify_pending_change {poptype function amount}` | governorship | `se_ECON_wealth.txt:127` | stage a wealth delta |
| `WEALTH_apply_pending_changes` | governorship | `:208` | commit staged deltas quarterly |
| `WEALTH_startup_set_pending_change_variables` | governorship | `:174` | seed `PENDING_*_wealth` at start |
| `WEALTH_cache_national_wealth` | country | `se_ECON_wealth.txt:3` | national wealth aggregate |
| `official_currency` (var) | country | `JOBS_svalues.txt:153` | does this country run a monetary economy |
| `purchasing_power` (var) | currency province | `se_CURRENCY.txt:1749` | wealth units per currency unit |
| `backing_value` (var) | currency province | `se_CURRENCY.txt:1835` | metal-backed intrinsic value |
| `CURRENCY_peg_country_currency` | country | `se_CURRENCY.txt:1564` | change exchange rate (the debasement lever) |
| `CURRENCY_apply_inflation_wealth_malus_country` | country | `se_CURRENCY.txt:1987` | existing inflation penalty hook |
| `APPLY = <effect>` over `every_*` | — | `se_TRADE.txt:2368` | safe list-iteration idiom |
| `quarterly_trade_pulse` (on_action) | — | `oa_wealth_changes.txt:10` | runs 4×/yr inside `yearly_country_pulse` |
| `monthly_currency_pulse` (on_action) | — | `oa_wealth_changes.txt` | monthly currency tick |

Poptypes used by `WEALTH_*`: `upper_strata middle_strata lower_strata proletariat indentured tribesmen slaves` (`se_ECON_wealth.txt:174-206`).

---

## §1 — `se_ECON_LOG.txt` (diagnostic tracing)

**New file:** `common/scripted_effects/se_ECON_LOG.txt`
**Prefix:** `ECON_LOG` · **sys tag:** `ECON`
**Risk:** ~none. Pure `debug_log`; silent no-op in normal play (`se_LOG.txt:11`).

This is a thin domain wrapper over `se_LOG` plus one composite snapshot that dumps the
economic state we most need to eyeball. It does **not** re-implement the log macros — it
calls them with `sys = ECON`.

```txt
########################################################################
# se_ECON_LOG.txt — economic diagnostic tracing.
# Mirrors se_LOG usage with sys = ECON. Zero cost outside -debug_mode.
# Extract with: grep "\[IMP19C\]\[ECON\]" debug.log > econ_trace.log
# Prefix = ECON_LOG
########################################################################

# One-line country economic snapshot. Country scope. Called at the tail of the
# quarterly wealth/jobs pulse. All reads are existing cached vars/svalues.
ECON_LOG_country_snapshot = {
	# Scope: country
	LOG_line = {
		sys = ECON
		msg = "[SNAP] [ROOT.GetTag] treasury=[ROOT.MakeScope.ScriptValue('treasury')|0] natl_wealth=[ROOT.MakeScope.GetVariable('national_wealth').GetValue|0] has_currency=[ROOT.MakeScope.Var('official_currency').GetName]"
	}
}

# Employment slice — jobs vs unemployment, aggregated once per country per quarter.
# ⚠ CONFIRM: whether unemployed is best summed province-side or read from an
# existing country cache; sketch sums provinces via APPLY to stay O(provinces).
ECON_LOG_jobs_snapshot = {
	# Scope: country
	set_variable = { name = ECON_LOG_tmp_unemployed  value = 0 }
	set_variable = { name = ECON_LOG_tmp_used        value = 0 }
	every_owned_province = {
		prev = {
			change_variable = { name = ECON_LOG_tmp_unemployed  add = prev.JOBS_unemployed_pops_province }
			change_variable = { name = ECON_LOG_tmp_used        add = prev.JOBS_num_used_slots }
		}
	}
	LOG_line = {
		sys = ECON
		msg = "[JOBS] [ROOT.GetTag] used=[ROOT.MakeScope.GetVariable('ECON_LOG_tmp_used').GetValue|0] unemployed=[ROOT.MakeScope.GetVariable('ECON_LOG_tmp_unemployed').GetValue|0]"
	}
	remove_variable = ECON_LOG_tmp_unemployed
	remove_variable = ECON_LOG_tmp_used
}

# Currency slice — read off the country's official currency province.
ECON_LOG_currency_snapshot = {
	# Scope: country
	if = {
		limit = { has_variable = official_currency }
		var:official_currency = {
			LOG_line = {
				sys = ECON
				msg = "[CURR] backing=[This.MakeScope.GetVariable('backing_value').GetValue|0] pp=[This.MakeScope.GetVariable('purchasing_power').GetValue|0]"
			}
		}
	}
}

# Composite — the one call the pulse makes.
ECON_LOG_quarter = {
	# Scope: country
	ECON_LOG_country_snapshot = yes
	ECON_LOG_jobs_snapshot = yes
	ECON_LOG_currency_snapshot = yes
}
```

**⚠ CONFIRM before writing:**
- The exact promptable-variable read syntax (`[ROOT.MakeScope.GetVariable('x').GetValue|0]`)
  is used verbatim across the Qing suite (e.g. `se_QING_GOVERNANCE.txt:107`), so it's known-good;
  but `ScriptValue('treasury')` and `.Var(...).GetName` for a scope-valued variable I'd verify
  against one existing tooltip before committing.
- Whether `national_wealth` is the live var name or whether to call `WEALTH_cache_national_wealth`
  first and read its output var. One grep confirms.

**Wire-up:** add `ECON_LOG_quarter = yes` at the end of the quarterly economic pass (see §2
step 4 — same call site as `JOBS_pulse`, after trade settles).

---

## §2 — Employment → Wages activation (`JOBS_pulse`)

> **⛔ SUPERSEDED BY CODE READ — do not build the `JOBS_pulse` below.** Tracing the live
> code before writing (per the §2 gate) showed the premise here is wrong on three counts:
> (1) the `JOBS_*_governorship` values are **pure derived script values** that recompute on
> every read — there is nothing to "refresh on a cadence"; (2) wages are **already paid**
> quarterly by `WEALTH_pay_wages_all_countries` (`oa_wealth_changes.txt:163`); (3)
> `JOBS_set_employment_slots` is **dead code** — its only output `JOBS_slots_subsistence` is
> read nowhere. So a `JOBS_pulse` would either duplicate the existing wage payment or refresh
> nothing. What §2 *actually* surfaced was a correctness bug, fixed and recorded in the
> IMPLEMENTED section. The design sketch below is retained only as a record of the original
> (incorrect) plan.

**Extends:** `common/scripted_effects/se_ECON_employment.txt` (currently 46 lines: only
`JOBS_set_employment_slots`).
**Depends on:** `JOBS_svalues.txt` (all wage math — already built) + `se_ECON_wealth.txt`
pending-change idiom (already built). **This is orchestration, not new math.**
**Risk:** medium-low. Structure is safe; the wage↔currency magnitude is a balance question
(§1 exposes it). The one real hazard — ordering — is handled by calling *after* trade settles.

### The gap, precisely
`JOBS_wages_due_all` (`:148`) and the strata/expense splits (`:210-320`) are fully defined but
**nothing calls them**, and nothing routes the result into `PENDING_*_wealth`. There is no
`JOBS_pulse`. We add exactly that: read the existing svalues → stage via `WEALTH_modify_pending_change`.

### New effects (append to `se_ECON_employment.txt`)

```txt
# ======================================================================
# JOBS_pay_wages — stage this quarter's wage income into pop wealth pools.
# Scope: governorship. Reads the existing JOBS_wages_due_* svalues and routes
# them through the existing WEALTH pending-change machinery. No new economics.
# ======================================================================
JOBS_pay_wages = {
	# Only monetary economies pay wages (JOBS_wages_due_all already returns 0
	# without official_currency — this guard just skips the staging work).
	if = {
		limit = { owner = { has_variable = official_currency } }

		# Workers' take, split by strata share (svalues at JOBS_svalues.txt:210/:219).
		WEALTH_modify_pending_change = {
			poptype = middle_strata
			function = add
			amount = JOBS_wages_due_middle_strata
		}
		WEALTH_modify_pending_change = {
			poptype = proletariat
			function = add
			amount = JOBS_wages_due_proletariat
		}
		# ⚠ CONFIRM: lower_strata / indentured wage shares. JOBS_svalues defines
		# middle+proletariat splits explicitly; if lower_strata earns wages it needs
		# a parallel JOBS_wages_due_lower_strata svalue (one to add, or confirm 0).

		# Owners' expense — upper strata pay the business/military/etc share they're
		# liable for (svalue gates on state_pays_wages_* flags, JOBS_svalues.txt:228).
		WEALTH_modify_pending_change = {
			poptype = upper_strata
			function = subtract
			amount = JOBS_wages_expense_upper_strata
		}
	}
}

# ======================================================================
# JOBS_pay_state_wages — the treasury-borne wage share. Country scope.
# ======================================================================
JOBS_pay_state_wages = {
	# Scope: country
	if = {
		limit = { has_variable = official_currency }
		every_owned_governorship = {
			owner = {
				add_treasury = {
					value = 0
					subtract = prev.JOBS_wages_expense_the_state
				}
			}
		}
	}
	# ⚠ CONFIRM: add_treasury signage + whether wages are paid in treasury (wealth)
	# vs a currency-denominated pool. DD16 says state pays "real wages"; confirm the
	# unit before committing the sign.
}

# ======================================================================
# JOBS_pulse — the quarterly employment tick. Country scope. Called from the
# quarterly economic pass AFTER trade has settled prices/production, so wage
# math reads final numbers (avoids the documented "compute before consume" hazard).
# ======================================================================
JOBS_pulse = {
	LOG_enter = { sys = ECON  fn = "JOBS_pulse" }

	# 1. refresh slots (existing effect, currently the only thing in this file)
	every_owned_governorship = {
		JOBS_set_employment_slots = yes
	}

	# 2. stage wage income/expense per governorship
	every_owned_governorship = {
		JOBS_pay_wages = yes
	}

	# 3. treasury-borne wages
	JOBS_pay_state_wages = yes

	# 4. commit the staged wealth deltas (existing quarterly effect)
	every_owned_governorship = {
		WEALTH_apply_pending_changes = yes
	}

	# 5. diagnostics (§1)
	ECON_LOG_quarter = yes

	LOG_exit = { sys = ECON  fn = "JOBS_pulse"  result = OK }
}
```

### Wire-up (`common/on_action/economy/oa_wealth_changes.txt`)
`quarterly_trade_pulse` already fires 4×/yr inside `yearly_country_pulse` (`:10-22`). Add a
jobs pulse **immediately after each** trade pulse so wages read settled trade output:

```txt
yearly_country_pulse = {
	on_actions = {
		yearly_edu_update_pulse
		delay = { days = 1 }
		yearly_edu_update_pulse_from_trade

		quarterly_trade_pulse
		quarterly_jobs_pulse          # <-- NEW, each quarter, after trade
		quarterly_flavour_pulse
		delay = { days = 91 }
		quarterly_flavour_pulse
		quarterly_trade_pulse
		quarterly_jobs_pulse          # <-- NEW
		...
	}
}
```
…where `quarterly_jobs_pulse` is a new on_action whose effect is `if = { limit = { <once-per-all-countries guard> } every_country = { JOBS_pulse = yes } }`, mirroring how `quarterly_trade_pulse` runs once for all countries. **⚠ CONFIRM** the exact "run once for all countries" guard pattern `quarterly_trade_pulse` uses (it's noted as "run only once for all countries" at `oa_wealth_changes.txt:12`) and copy it verbatim.

### Startup
Ensure `WEALTH_startup_set_pending_change_variables` (`se_ECON_wealth.txt:174`) already runs
at game start for every governorship (it seeds the `PENDING_*_wealth` vars `JOBS_pay_wages`
writes to). **⚠ CONFIRM** it's called in `oa_economy_setup.txt`; if not, add it.

---

## §3 — Currency-crisis event layer

**New files:** `common/scripted_effects/se_CURRENCY_CRISIS.txt`,
`events/imp19c_mod_events/currency_crisis_events.txt`,
`localization/english/currency_crisis_l_english.yml`.
**Reads (does not modify) the currency engine.** Same pattern as the Qing suite:
threshold band off an existing meter → gated events → tooltip'd choices → logged.
**Risk:** low. Additive; the only judgment call is the crisis threshold constant.

### Threshold helper (`se_CURRENCY_CRISIS.txt`)
```txt
########################################################################
# se_CURRENCY_CRISIS.txt — player-facing currency crises read off the existing
# CURRENCY_* meters (backing_value / purchasing_power). Engine untouched.
# Prefix = CURR_CRISIS · sys tag = ECON
########################################################################

# Classify the country's currency health once per month. Country scope.
# Writes qing-style band flags other code / events can gate on. O(1).
CURR_CRISIS_classify = {
	# Scope: country
	if = {
		limit = { has_variable = official_currency }
		var:official_currency = { save_scope_as = cur }

		# ⚠ CONFIRM the "real vs official value" ratio source. DD14 spec calls it the
		# RESERVE RATIO (% of circulating money backed by metal). backing_value and
		# purchasing_power exist (se_CURRENCY.txt:1749/1835); confirm whether a
		# reserve_ratio var is already computed or must be derived as
		# backing_value / amount_circulated. Grep amt_circulated (CURRENCY_update_amt_circulated:1273).
		remove_variable = curr_state_deflation
		remove_variable = curr_state_inflation
		if = {
			limit = { scope:cur.var:purchasing_power < CURR_CRISIS_deflation_floor }   # ⚠ tunable
			set_variable = curr_state_deflation
			LOG_line = { sys = ECON  msg = "[CRISIS] [ROOT.GetTag] deflation flagged" }
		}
		else_if = {
			limit = { scope:cur.var:purchasing_power > CURR_CRISIS_inflation_ceiling } # ⚠ tunable
			set_variable = curr_state_inflation
			LOG_line = { sys = ECON  msg = "[CRISIS] [ROOT.GetTag] inflation flagged" }
		}
	}
}
```

### Wire-up
Add `CURR_CRISIS_classify = yes` inside the existing `monthly_currency_pulse`
(`oa_wealth_changes.txt`), guarded like the Qing pulse (one cheap classify + a
`trigger_event` only when a band flips and a cooldown var is absent). No new tick.

### Events (`currency_crisis_events.txt`) — `namespace = currency_crisis`
- **`currency_crisis.1` (deflation squeeze):** trigger `has_variable = curr_state_deflation`.
  Options: (a) lower the reserve exchange rate to ease the squeeze — calls the **existing**
  `CURRENCY_peg_country_currency` (`se_CURRENCY.txt:1564`) at a stability + political-influence
  cost (the DD14 lever); (b) hold and eat unrest.
- **`currency_crisis.2` (inflation drain):** trigger `has_variable = curr_state_inflation`.
  Mirror image; option to tighten via the same peg lever, or let the **existing**
  `CURRENCY_apply_inflation_wealth_malus_country` (`:1987`) bite.
- **`currency_crisis.china` (DD8 銀貴錢賤 silver-vs-copper debasement):** `tag = CHI` +
  deflation band. Ties into the Qing suite already in the repo — a copper-debasement choice
  (short-term relief, long-term backing erosion) vs. holding the silver standard. Uses the
  same peg/backing effects; adds a Qing-flavoured `custom_tooltip`.

All options `custom_tooltip` + `LOG_line`, exactly as the Qing events do.

**⚠ CONFIRM before writing §3:** the real cost args `CURRENCY_peg_country_currency` expects
(read its param block at `:1564`) so the options pass the right `$…$` arguments.

---

## Build order & effort

| Step | Files touched | New/edit | Confidence | Blockers |
|---|---|---|---|---|
| §1 `se_ECON_LOG` | 1 new + 1 on_action line | new | **high** | confirm 2 read-syntax forms |
| §2 `JOBS_pulse` | `se_ECON_employment.txt`, `oa_wealth_changes.txt` | edit+edit | **medium-high** | confirm treasury signage, lower-strata share, once-per-all-countries guard |
| §3 currency crisis | 3 new files | new | **medium** (China variant), **high** (generic) | confirm reserve-ratio source + peg args |

Recommended sequence: **§1 → §2 → §3**, verifying `debug.log` output after §2 before
layering §3, so we're never tuning blind.

### Open questions for you (the only real design forks)
1. **Wage unit** — are wages paid/earned in *wealth* (vanilla currency) or in the new
   *currency* resource? DD16 says "real wages"; this decides §2's `add_treasury` vs a
   currency-pool change and the sign convention.
   - **UPDATE after code read:** wages are **already paid** by `WEALTH_pay_wages_all_countries`
     (`oa_wealth_changes.txt:162`), called inside `quarterly_trade_pulse`. So §2 is NOT
     "activate wages from scratch" — it's "the slot/employment *counts* (`JOBS_set_employment_slots`)
     aren't refreshed on the same cadence, and the file is otherwise a stub." §2's real scope
     shrinks to: refresh slots quarterly + verify the existing wage payment reads current slots.
     This makes §2 **lower risk** than first estimated, but I must trace `WEALTH_pay_wages_all_countries`
     before touching it. **⚠ Re-scope §2 against that effect first.**
2. **Reserve-ratio source** — is there already a computed `reserve_ratio`, or should §3
   derive it from `backing_value / amount_circulated`? (Changes §1's currency snapshot too.)
3. **Crisis thresholds** — I'll expose `CURR_CRISIS_deflation_floor` / `_inflation_ceiling`
   as `defines` constants; you set the numbers (I can't playtest them).

---

# TIER 1 — additional "build well" systems (high confidence)

These share the §1–§3 signature: an existing template + statically-checkable correctness
(schema validation / brace balance / reference resolution) + no invention on a hot loop.

## §4 — Repo-wide economic instrumentation (generalize §1)

**This is §1 applied beyond the jobs/currency snapshot to the whole economy pipeline.**
The big trade/currency effects (`se_GLOBALTRADE_split.txt` 5,877 ln, `se_PURCHASE.txt` 2,804 ln,
`se_TRADE.txt` 4,611 ln) currently run with **no tracing** — when a quarter produces a wrong
number, there's nothing to grep. Add `LOG_enter/exit/fail` at the phase boundaries already
present in `quarterly_trade_pulse`'s `on_actions` chain (`oa_wealth_changes.txt:201-`):
`quarterly_global_trade_food/luxury/…/apply_trade_changes_and_consume`.

- **Risk:** ~none (no-op outside `-debug_mode`; additive only).
- **Payoff:** converts the *un*-checkable core into a checkable one — the single highest-leverage
  thing for every subsequent economy build. **This is the piece being implemented now (see
  "IMPLEMENTED" note at end).**

## §5 — Laws + inventions content expansion

`common/laws` (10 files) and `common/inventions` (4 files) are **declarative, schema-validated
data** — the engine rejects malformed entries, so correctness is largely static, exactly like
the Qing modifier files.

- **What:** economy-gating laws the DD roadmap calls for — tariff/subsidy laws (read existing
  treaty/customs vars), education-tier laws (gate `se_EDU.txt` caps), property/income-tax laws
  (feed `INCOME_*`). Inventions unlock industrial-district tiers (the memory's industrialisation gate).
- **Template:** existing `common/laws/*.txt` entries + the Qing modifier idiom.
- **Risk:** low for correctness; ceiling is balance, not code.
- **⚠ CONFIRM:** each law's `modifier`/`effect` block references only existing modifier keys
  (grep `common/modifiers/00_*.txt`), same discipline as the Qing suite.

## §6 — Mission-tree content

`common/missions` (70 files); I built Qing mission trees cleanly this project, so this is a
**proven** capability, not a projection.

- **What:** national/economic mission trees hung off existing triggers, granting existing objects
  (`add_building_level`, modifiers, `change_variable` on economy counters — all in the verified
  event-object vocab from memory).
- **Risk:** low. Static-checkable; established pattern.

## §7 — `monthly_job_pulse` activation

**Found during survey:** `common/on_action/00_monthly_job_pulse.txt` is an empty flavour stub
(`random_events = { 500 = 0 }` — a no-op). It's a named on_action already registered with the
engine, awaiting a body.

- **What:** the monthly-cadence sibling of §2 — unemployment drift, job-related flavour events,
  social-mobility hooks (there's already a `social_mobility_pulse` seam).
- **Risk:** low (pre-wired seam; same shape as §2). **⚠ CONFIRM** intended monthly vs quarterly
  split of responsibilities against `quarterly_trade_pulse`.

---

# TIER 2 — "build well WITH a design decision from you first"

Greenfield **data** with a known engine schema and clear vanilla analogues — I build the
scaffolding well, but the *content* (which parties, which offices) is a design call you own.

## §8 — Political parties / factions (`common/parties` — EMPTY, confirmed)

DD roadmap: "internal politics overhaul — parties, factions, public voting."

- **I can build well:** the party *definitions* schema, faction-support meters (the
  `QING_DECLINE_nudge` 0..100 counter idiom generalizes directly), a party-support pulse,
  band modifiers for governing coalition. There's a `common/scripted_effects/se_POLITICS.txt`
  (408 ln) + `00_parties.txt` scripted_effect already to pattern against.
- **You decide:** the roster of parties/ideologies and what each wants. **Design fork — needs
  your input before I start.**

## §9 — Government offices (`common/government_offices` — EMPTY, confirmed)

Directly adjacent to the Qing Grand Council/office work I already did — pattern in hand.

- **I can build well:** the office-slot scaffolding, character assignment, office-effect bands
  (mirrors `QING_office_*` / `QING_council_*`).
- **You decide:** the universal (non-Qing) office roster and their effects. **Design fork.**

## §10 — De jure (culture-plurality generated) — ✅ DONE (generator); formable consumer deferred

**Correction to an earlier note:** there is **no `de_jure_setup` directory** in this mod and
the `de_jure` token appears nowhere — the earlier "EMPTY, confirmed" line was wrong. The map
topology (`map_data/regions.txt` 512, `areas.txt` 1770) is *de facto* and is **generated** by
`map_data/area_designator.py` from `map_data/province_setup.csv`, not hand-authored.

De jure is really **one generated data table** (`culture | formable | region → set of areas`)
with **several independent consumers** — they are additive, not mutually exclusive. The only
real fork is the *seed* of the table:

- **Culture-plurality keying** — the de jure owner of an area is its plurality culture. Free
  from the existing `CULTURE` column. **← IMPLEMENTED (see IMPLEMENTED §10).**
- **Historic-nation keying** — areas as the historic territory of a formable. Needs a *new*
  authored de-jure column in the CSV (culture ≠ nation). **NOT implemented; noted below.**

**Formable-requirement consumer — NOTED, NOT IMPLEMENTED (user deferred).** The formable
system is already scaffolded but inert: `common/scripted_triggers/imp19c_formable_triggers.txt`
defines `imp19c_can_form_country_trigger` with three formable classes (`is_historic_state`,
`is_nation_state_culture`, `is_nation_state_culture_group`) whose membership lists are still
placeholder stubs (`flag:BOH`/`flag:CZE`/`flag:GER`), and all 53 `decisions/tier_*_formables/
form_*.txt` files are 0-byte stubs. A "control X% of your historic areas to form" requirement
is the obvious consumer of a historic-nation de jure table — but that needs the authored
de-jure column above, so it is left for a future pass pending user design input.

---

## §11 — Colonial-claims & bottom-up migration program

A four-layer program, **generic-first (every country gets it) then Qing extends** — the same
pattern as the currency-stress layer. Built layer-by-layer with a review after each. Richer,
costlier Qing behaviour is explicitly acceptable. The engine is Imperator, **not** EU4/Vic3:
there is no casus-belli folder, no fabricate-claim CB, no `add_state_claim`, no rivalry/attitude
object. The reusable primitives are `add_claim`/`remove_claim` (province) with `is_core_of` as
the read-back, the opinion system (per-(source,target), self-decaying), and the province-scope
`on_ownership_change` / `on_province_occupied` on-actions.

- **Layer 1 — claim-hostility engine** (`se_CLAIM_HOSTILITY.txt`). **← IMPLEMENTED.** When a
  province a country *claims but does not control* is seized (ownership change) or occupied
  (controller change) by anyone else, the claimant's **opinion** of the taker drops. Because the
  actors are dynamic (any claimant vs. any taker) per-pair named counters are impossible — the
  opinion *is* the per-pair hostility store. Seizure (`claim_violated_opinion`, −35) bites harder
  and lingers longer than a reversible wartime occupation (`claim_incursion_opinion`, −15); the
  incursion path self-throttles to once/year/province. Wired to the two (previously empty)
  province on-actions in `00_specific_from_code.txt`. Logged `sys = CLAIM`.
- **Layer 2 — generic bottom-up migration → claims** (`se_MIGRATION.txt`, `MIGRATION_svalues.txt`,
  `00_decade_country.txt`). **← IMPLEMENTED.** See IMPLEMENTED §11 below.
- **Layer 2b — Qing colonisation reworked to drive Layer 2** (`se_QING_COLON.txt`, mission &
  event call-sites). **← IMPLEMENTED.** The colonisation missions now set frontier *pull* and the
  New World crop-boom events set heartland *push* on the generic engine, instead of settling by
  `create_state_pop` fiat; formal `add_claim` calls preserved (they feed Layer 1). See IMPLEMENTED §11.
- **Layer 3 — de jure irredentism + deep Qing ethnic-tension re-derivation** (`se_DEJURE.txt`,
  `dejure_on_actions.txt`, `se_QING_DECLINE.txt` extension). **← IMPLEMENTED.** Generic: at game
  start each settled province's 1815 plurality culture is *frozen* into `var:dejure_culture` (the
  runtime bridge — the §10 table is generated data the engine never loads); on conquest, if the new
  owner has not *integrated* that rightful culture, the land gets a decaying `dejure_disaffection`
  unrest modifier and the rightful culture's kin-state gains an irredentist claim. Qing: the
  abstract `qing_ethnic_tension` counter is now largely *computed* from the realm's ethnic geography
  — an annual demographic scan writes a target, the quarterly pulse drifts toward it. See IMPLEMENTED §11.
- **Layer 4 — reconquest wargoal + separatist rebellions** (`00_default.txt` `reconquest_wargoal`;
  `se_SEPARATISM.txt`; `00_decade_country.txt` + `00_monthly_country.txt` wiring). **← IMPLEMENTED.**
  A claims-based `reconquest_wargoal` (cheap `take_province`, offered only when the attacker holds a
  Layer 1-3 seeded claim — `is_core_of = root` — on the defender's land), plus a separatist-rebellion
  engine: an alien-ruled, disaffected homeland (Layer 3 `dejure_disaffection` + frozen
  `var:dejure_culture` + real unrest) breaks away as a **new country** (`LAND_release_from_list`),
  the parent wages a reconquest war to drag it back, and a **neighbouring country where the rebel
  culture actually lives** may be invited into the war on the rebels' side (`add_to_war`). If the
  culture is split across several empires, the one new state also opens **cross-border liberation wars**
  (Option A) on its other neighbouring parents' de jure-X land, capped at 3 fronts. Generic
  layer piggybacks `decade_country_pulse` (rare, self-throttled, no new polling); the Qing extension
  adds a tension-scaled quarterly risk gated on `qing_ethnic_tension`. See IMPLEMENTED §11.

**Migration design philosophy (firm):** migration is **bottom-up** — pops move because *they*
want to, driven by poverty/opportunity, religion, ethnic minority status, war, and
overpopulation/unrest/famine (push) vs. prosperity and calm (pull). The government/player is only
**one factor among many**: they *incentivize/disincentivize* via modifiers folded into the
push/pull scores, they never directly order a move. **Reuse, don't recompute:** the push/pull
scores read already-cached economy fields (jobs, unrest, food shortage, war/occupation), so a
pulse is O(provinces) cheap reads, not a resimulation.

---

## Revised build-order recommendation

| Priority | Item | Confidence | Gate |
|---|---|---|---|
| 1 | §1/§4 instrumentation | **high** | ✅ DONE |
| 2 | §7 monthly_job_pulse | high | ✅ DONE (marker only — see IMPLEMENTED) |
| 3 | §2 employment slot refresh | — | ✅ DONE — was a bug fix, not a build (see IMPLEMENTED) |
| 4 | §5 laws/inventions | high | currency_law ✅; university laws + 2 inventions ✅ (see IMPLEMENTED); net-new law *groups* still need design |
| 5 | §6 missions | high (proven) | SKIPPED for now (user) |
| 6 | §3 currency crises | — | ✅ DONE — generic layer + Qing refactored to extend it (see IMPLEMENTED) |
| 7 | §8/§9 parties/offices | med | **design input from you** |
| — | §10 de jure (culture-plurality) | high | ✅ DONE — generator extended (see IMPLEMENTED); formable consumer deferred |
| — | §11 L1 claim-hostility | high | ✅ DONE — `se_CLAIM_HOSTILITY.txt` + on-action wiring (see IMPLEMENTED §11) |
| — | §11 L2 bottom-up migration → claims | high | ✅ DONE — `se_MIGRATION.txt` on `decade_country_pulse` (see IMPLEMENTED §11) |
| — | §11 L2b Qing colonisation → drives L2 | high | ✅ DONE — `se_QING_COLON.txt` + mission/event rewire (see IMPLEMENTED §11) |
| — | §11 L3 de jure irredentism + Qing ethnic-tension re-derivation | high | ✅ DONE — `se_DEJURE.txt` + game-start freeze + Qing annual demographic scan (see IMPLEMENTED §11) |
| — | §11 L4 reconquest wargoal + separatist rebellions | med | ✅ DONE — `reconquest_wargoal` + `se_SEPARATISM.txt` (breakaway via `LAND_release_from_list`, reconquest war, neighbouring-kin backer) + Qing tension-scaled extension (see IMPLEMENTED §11) |
| — | §11 L4 ext Qing civic (national) identity | med | ✅ DONE — `qing_civic_identity` meter (`se_QING_DECLINE.txt`): selfstr-gated drift, civic relief on tension, annual integration bridge + majority-weight sinicization melting pot, bands, GUI lever (see IMPLEMENTED §11) |

---

## IMPLEMENTED

**§1 `se_ECON_LOG.txt`** — written to the repo (`common/scripted_effects/se_ECON_LOG.txt`),
wired into `oa_wealth_changes.txt`. Notes:
- All promptable reads use the **verified `debug_log`-safe form**
  `[ROOT.MakeScope.GetVariable('x').GetValue|0]` (the GUI `Player.MakeScope`/`GuiScope`
  form seen in tooltips is NOT valid inside a `debug_log` effect, so values are staged into
  ROOT temp vars first).
- National wealth var confirmed as `WEALTH_total_private_moveable_wealth`
  (`se_ECON_wealth.txt:6`), cached by `WEALTH_cache_national_wealth`.
- `ECON_LOG_quarter` hooked at country scope right after `WEALTH_cache_national_wealth`
  so the snapshot reads freshly-cached values.

**§4 trade-pipeline phase markers** — `ECON_LOG_phase_enter` placed *inside the guard* of
each quarterly trade stage in `oa_wealth_changes.txt`, so a stage only logs when it actually
does work (not on the no-op re-fires blocked by the `done_*` globals). Stages tagged:
`trade_reset_totals`, `trade_food`, `trade_luxury`, `trade_luxury_2`, `trade_3..6`,
`trade_apply_consume` (+ the pre-existing `quarterly_production` enter/exit pair). The trace
now shows the exact order stages ran and where one aborts.

**§7 `monthly_job_pulse` instrumentation** — confirmed via the Imperator wiki
(On_action_modding) that this on_action is **engine-invoked (From Code: yes) in "none" scope**
(no root country/province). Given its sibling `monthly_administration_pulse` was disabled for
"unacceptable monthly slowdowns", NO heavy per-governorship logic was added here. Only a
scope-safe `ECON_LOG_phase_enter { stage = "monthly_job_pulse" }` marker inside a new `effect`
block, so a `-debug_mode` run confirms the hook fires and its cadence before any load is added.
The real employment slot-refresh work stays on the quarterly cadence (§2). BOM preserved.

**§5 `currency_law` filled** — `common/laws/00_economic_laws.txt`. The four options
(`precious_metal_content_coinage` / `silver_standard_currency` / `promissory_notes` /
`fiat_currency`) shipped as authored-but-empty `modifier = {}` stubs; filled with a coherent
hard-specie ↔ fiat spectrum. **All 9 modifier keys verified valid in law context** (each used
elsewhere in `common/laws/` or `common/modifiers/`). `monetary_policy_setting` and
`monetary_policy_law` were **deliberately left empty** — their options (`currency_recall`,
`limited_minting`, `more_minting`, `issue_bonds`) interlock with the live `se_CURRENCY` minting
engine, so flat modifiers there risk double-counting; those need engine-aware wiring, not law
modifiers.

**§2 employment → wages — resolved as a correctness fix, not a new build.** Tracing the
live system (the §2 gate) showed there was nothing to "activate": derived job-count svalues
recompute on read, and `WEALTH_pay_wages_all_countries` already pays wages quarterly. The one
real finding was a bad-reference bug in `JOBS_non_subsistence` (`JOBS_svalues.txt:320`), the
script value that counts employed pops:
- `JOBS_industrial_worker` — a **typo** for the defined `JOBS_industrial_workers`
  (`:135`, `value = num_of_IND_industrial_estate`). The engine reads an undefined script value
  as 0, so **industrial jobs were silently dropped from the employed-pops count.** Corrected to
  the plural.
- `JOBS_arts_workers` / `JOBS_health_workers` — referenced but **defined nowhere**; their
  buildings are already counted under other categories (cultural district → `JOBS_commercial`;
  hospital → `JOBS_infrastructure_workers`), so defining them would double-count. **Removed.**

The counted set is now a 1:1 match with the seven wage-paid categories (administrators,
commercial, educators, industrial_workers, infrastructure_workers, military,
resource_gatherer) — the used-slot count, the building-construction gate
(`00_buildings_scripted_triggers.txt:4`, `JOBS_available_slots > 0`), demand
(`DEMAND_svalues.txt:1178`), and the wage bill now all describe the same workforce.
Braces 103/103, BOM preserved. Dead `JOBS_set_employment_slots`/`JOBS_slots_subsistence`
left in place (flagged, not removed — separate cleanup, not a behavior fix).

**§3 currency-crisis layer — built generic-first, then Qing refactored to extend it.**
The original §3 sketch was corrected by a code read on two counts: (a) the intended
"reserve ratio" signal already exists as `CURRENCY_reserve_ratio_impact` (0..1 country
script value, `CURRENCY_svalues.txt:376`) — no need to derive one; (b) `CURRENCY_peg_country_currency`
is **not** a debasement lever (it adopts another country's currency), so it was dropped from
the option wiring in favour of verified levers. Critically, the code read also found the **Qing
suite already owned a complete China currency-crisis mechanic** (`qing_currency_stress` +
`qing_curr_silver_drain`/`qing_curr_monetary_crisis` bands, `se_QING_DECLINE.txt`) reading that
same meter. Per the "Qing should extend the generic, not silo" directive, the build was
inverted: **use the existing Qing implementation as the template for a generic engine, then
refactor Qing to extend it.**

- **New generic engine `se_CURRENCY_STRESS.txt`** — owns the two pure O(1) primitives factored
  out of the Qing mechanic: `CURR_STRESS_update { counter }` (the reserve-ratio→stress-drift
  transfer function, ±2/−1 around health 0.5) and `CURR_STRESS_classify { counter out }`
  (threshold→band level 0/1/2 at 30/60), plus `CURR_STRESS_nudge` (clamped 0..100 counter).
  **Design seam:** the primitives name **no modifier and no event** — the consumer maps the band
  level to its own flavour. (Parameterized modifier *names* are avoided: zero existing uses in
  the repo → unproven; parameterized *variable* names, used here, are proven by `QING_DECLINE_nudge`.)
- **Generic consumer** (also in `se_CURRENCY_STRESS.txt`): `CURR_STRESS_apply_generic_band` +
  `CURR_STRESS_pulse`, owning the generic meter var `currency_stress`, the generic bands
  `currency_reserve_strain`/`currency_reserve_crisis` (`00_currency.txt`), and the crisis event.
  Self-gated to **non-CHI monetary economies** (`has_variable = official_currency`, `NOT = tag = CHI`)
  and throttled to a **quarterly drift** by a 90-day cooldown var — matching the Qing cadence and
  keeping the per-country monthly cost to a single `has_variable` check 2 months in 3.
- **Wire-up:** `CURR_STRESS_pulse = yes` added to the country-scoped `monthly_currency_pulse`
  (`oa_wealth_changes.txt`).
- **Event `currency_crisis.1`** ("A Run on the Reserves") — offered once per 365-day cooldown
  when a country enters the crisis band. Three options route through **verified levers only**:
  spend treasury to buy specie (`add_treasury -100` + big meter cut), emergency print
  (`CURRENCY_grant_country_wealth = { thousands = 60 }`, `se_CURRENCY.txt:1239`, + stability hit),
  or ride it out. Full loc (`currency_crisis_l_english.yml`, BOM added to match siblings).
- **Qing refactor (behavior-preserving):** `QING_DECLINE_update_currency_stress` now delegates
  to `CURR_STRESS_update { counter = qing_currency_stress }`, and `QING_DECLINE_apply_currency_band`
  now classifies via `CURR_STRESS_classify` then maps the band to the Qing modifiers. Same counter,
  same 30/60 thresholds, same modifiers → identical in-game behavior; the private
  `qing_currency_reserve_health` scratch var (read nowhere else) is retired in favour of the
  generic engine's internal staging. The Qing meter keeps its own feed into reform-pressure and
  the opium/treaty/Boxer events untouched.

**Review (§3):** braces balanced (`se_CURRENCY_STRESS` 58/58, `se_QING_DECLINE` 430/430,
`00_currency` 3/3, `oa_wealth_changes` 145/145, `currency_crisis_events` 12/12); every called
`CURR_STRESS_*` resolves; both new modifiers defined; all 8 loc keys resolve; namespace unique;
no `currency_stress` var collision (all Qing hits are `qing_currency_stress`); band-threshold
refactor confirmed (no stray direct `qing_currency_stress >= 30/60` — the remaining `>= 40`
hits are unrelated event-dispatch gates); `qing_curr_band_tmp` set→read→removed (no leak).
**Bug caught in review & fixed:** the event's `picture = trade_wealth` was an **undefined event
picture** (would render blank) → changed to `trade_port` (defined, `00_event_pictures.txt:227`);
BOM was **missing** on the new loc file → added to match its siblings.

**§5 (second slice) — inert law/invention stubs filled, guided by their live consumers.**
A survey of all law + invention files (rather than trusting the spec's assumptions) found that
`00_economic_laws.txt` was already fully filled (currency/land/labour/business — no stubs left),
but three other empty stubs turned out to be **genuine gaps whose consumers already exist**:
- **`university_law` — 3 of 4 options empty** (`00_social_laws.txt`). Only `law_university_religious_colleges`
  had effects; `law_university_classical_institutions` / `_secular_instutions` / `_technical_colleges`
  had empty `modifier = {}` and placeholder loc (`"...desc"`). Yet the education system
  (`EDU_svalues.txt`: religious colleges down-multiply university education slots) and the politics
  system (`POLITICS_svalues.txt:205-213`: religious = +conservative support, secular/technical =
  −support) already branch on all four. Filled the three along the traditionalist→modernizing
  spectrum the game already assumes: classical = prestige/elite (civilization + upper-strata),
  secular = research + assimilation + civic culture (−devout), technical = strongest research +
  industrial output (−upper strata, −devout). Real loc descriptions written to replace the
  placeholders. This confirms the null baseline `no_state_financial_assistance = { modifier = {} }`
  was correctly left empty (it's the "do nothing" choice) — not every empty block is a gap.
- **2 civic inventions empty** (`00_civic_inventions.txt`, 2 of 61): `tech_artificial_canals` and
  `tech_sewer_systems` had `modifier = {}` while every sibling in their chain grants at least
  `country_civilization_value`, and both are live (they gate infrastructure buildings in
  `00_infrastructure_buildings.txt`). Filled with thematically-apt, non-double-counting national
  effects: canals → `country_civilization_value 2` + `global_commerce_modifier 0.05` (inland trade);
  sewers → `country_civilization_value 2` + `global_population_growth 0.02` (the sanitation dividend,
  distinct from the *local* population-capacity the gated building grants).

**Review (§5):** braces balanced (`00_social_laws` 78/78, `00_civic_inventions` 218/218). All 10
modifier keys verified valid (each used elsewhere in laws/inventions/modifiers); the
`global_pop_assimilation_speed_modifier` suffix disambiguated from the flat
`global_pop_assimilation_speed` variant (both real; the `_modifier` form matches my 0.1 scale).
All magnitudes sit within each file's existing value distribution. BOM + line-ending integrity
preserved via byte-exact Python (`00_social_laws` is **BOM+CRLF**, `00_civic_inventions` is
**BOM+LF** — the Edit tool would have corrupted the CRLF file). Loc: 3 university descriptions
filled; the 2 inventions correctly need no manual desc (siblings use auto-generated effect
display, `_desc:0 ""`). `monetary_policy_setting`'s 4 empty options remain deliberately deferred
(they interlock with the live minting engine — flat modifiers would double-count).

**§10 de jure — culture-plurality table, generated (not hand-authored).** Extended the existing
map generator `map_data/area_designator.py` (the same script that emits `areas.txt`/`regions.txt`
from `province_setup.csv`) with a `generate_de_jure(df)` pass and a third output file,
`map_data/de_jure_output.txt`. For each area it tallies the `CULTURE` of every province, takes
the plurality culture, and emits a `<culture> = { areas = { ... } }` lookup — the generated
"which culture this land rightfully belongs to" table. Design choices, all matching the existing
generator's idioms:
- **Skip, don't guess:** areas whose provinces have no listed culture are omitted (exactly one —
  `state_98`), rather than assigned a placeholder.
- **Deterministic tiebreak:** where two cultures share the top province count (50 areas), the
  alphabetically-first culture wins, so regenerating the file is stable/diff-clean.
- **Same sanitisation** (`sanitise_string`) applied to area names as the areas/regions passes;
  culture tokens are already clean lowercase (verified: 0 of 379 contain spaces/dots).
- Output sorted (cultures, then areas) for a stable diff.

**Review (§10):** logic replicated in dependency-free Python (pandas isn't in this shell; the
user runs the generator in their own env) and the artifact actually produced and checked:
**243 cultures, 865 of 866 distinct areas assigned** (the 1 gap = `state_98`, the culture-less
area — matches the skip rule), **braces balanced 486/486**. Spot-checks confirmed correct
plurality (Vancouver Island → `ahtna` 3 vs `salish` 2) and correct tiebreak (`state_100`:
`baloch` 3 = `persian` 3 → `baloch`). Plurality winners are sane (roman 61, russian 42, han 24).
Style matches the existing generator (shared `sanitise_string`, same brace/indent idiom); the
pre-existing NaN-area quirk from `df.AREA.unique()` is handled by the empty-counts `continue`.
**No mod script consumes the table yet** — this is the generated data layer only; a consumer
(irredentism, or the formable requirement below) is separate future work.

**§11 Layer 1 — claim-hostility engine, generic.** New `common/scripted_effects/se_CLAIM_HOSTILITY.txt`
(no BOM, tabs, `sys = CLAIM`) with two effects: `CLAIM_HOSTILITY_on_transfer` (permanent seizure —
every *other* country holding a core/claim on the province drops its opinion of the new owner via
`claim_violated_opinion`) and `CLAIM_HOSTILITY_on_incursion` (wartime occupation — a milder,
faster-decaying `claim_incursion_opinion`, per-province throttled to once/year via a
`claim_incursion_cd` variable). Two opinion types added to `common/opinions/imp19c_opinions.txt`
(LF, no BOM; −35 / −15 with 3 / 6 yearly-decay) and localised in `opinions_l_english.yml`
(BOM+LF). Wired into the two previously-empty province on-actions in
`common/on_action/00_specific_from_code.txt` (BOM+CRLF — edited byte-exactly in Python to preserve
CRLF and single BOM): `on_ownership_change` gained `CLAIM_HOSTILITY_on_transfer = yes` alongside
its preserved holding-cleanup effect; the empty `on_province_occupied` gained an effect block with
`CLAIM_HOSTILITY_on_incursion = yes`. Rationale for the opinion-as-store design and the every_country
scan cost is in the file header (event-driven, not a hot loop; the incursion path self-throttles).

**§11 Layer 2 — bottom-up migration → claims, generic.** Three files:
- `common/script_values/MIGRATION_svalues.txt` — extended the pre-existing (unwired)
  `MIGRATION_push_province` and added `MIGRATION_pull_province`. Both are built **entirely from
  already-cached economy fields** (no recompute): `JOBS_unemployed_pops_province` /
  `JOBS_available_slots` (jobs), `province_unrest`, `civilization_value`, `total_population`
  (engine per-tick), and `governorship.ECON_governorship_food_shortage` (itself a sum of the cached
  `var:shortage_<food>` the consume step writes). War (`owner = { war = yes }`) and occupation
  (`NOT = { controller = owner }`) push people out / repel them in. Per-pop grievances that vary
  *within* a province (minority status, poverty) are deliberately **not** in the province score —
  they live in the emigrant `weight` so they decide *who* leaves, not *whether* the province sheds.
- `common/scripted_effects/se_MIGRATION.txt` (no BOM, tabs, `sys = MIGR`) — `MIGRATION_country_pulse`
  runs once per country per pulse: `ordered_owned_province order_by = MIGRATION_push_province max = 3`
  (top-3 worst, gated `push > 5` and "has a non-slave/non-noble who could go"); from each,
  `ordered_neighbor_province order_by = MIGRATION_pull_province max = 1` picks the single best
  adjacent destination (must be owned land, positive pull, **and** beat the source's own pull — so
  pops don't shuffle between two equally-bad provinces; cross-border neighbours are eligible, i.e.
  inter-country migration). One `random_pops_in_province` with a grievance `weight` (cultural
  minority ×3, religious minority ×2, proletariat/lower-strata ×2, unhappy `pop_hapiness < 0.4` ×2;
  slaves & nobles excluded) is `move_pop`-ed to the destination. `MIGRATION_seed_claim_if_flipped`
  then checks the destination: if its `dominant_province_culture` is no longer its `owner.culture`,
  the country whose `primary_culture` matches that plurality (and which is neither the owner nor
  already a core-holder) gains `add_claim` — organic settler colonialism feeding Layer 1 & Layer 3.
- `common/on_action/00_decade_country.txt` (BOM+LF — Edit-safe) — populated the empty
  `decade_country_pulse` with a scheduled `MIGRATION_decade_pulse` child on-action (`delay = { days
  = { 1 3650 } }` spreads the world's migration across the decade window instead of one tick), whose
  `effect` calls `MIGRATION_country_pulse`. `decade_country_pulse` confirmed a genuine engine
  on-action and moddable at country scope (used by both reference mods, Terra-Indomita and Invictus).
  The decade cadence *is* the throttle — a steady trickle, no per-pair state, heavy scans only for
  the few worst provinces.

**Review (§11 — all green).** Braces balanced: `se_CLAIM_HOSTILITY` 26/26, `imp19c_opinions` 24/24,
`00_specific_from_code` 318/318 (single BOM, CRLF preserved), `se_MIGRATION` 39/39,
`MIGRATION_svalues` 21/21, `00_decade_country` 6/6 (single leading BOM, no interior BOM, no CRLF).
Every referenced symbol resolves to a definition (`MIGRATION_push/pull_province`,
`JOBS_unemployed_pops_province`, `JOBS_available_slots`, `ECON_governorship_food_shortage`, the three
`MIGRATION_*` effects, `LOG_enter/exit/line`). Every cross-scope traversal verified against real repo
usage: province→`governorship.<named_svalue>` (COTTAGEIND/EDU "Scope: Province" svalues),
`order_by = <named script_value>` (AI_interest_value, DIPLOMACY_global_power_score), `war = yes` inside
a country `limit` (se_AI `every_country { limit { war = yes } }`), `exists = controller` /
`NOT = { controller = owner }`, pop-scope `pop_culture`/`pop_religion`/`pop_hapiness` and per-pop
`weight` (shortage_events, decentralize_realm_button), `.dominant_province_culture` as a scope link
(hoa_league_city_button, se_LAND), `move_pop = <province scope>` (subject_focus, send_settlers).
**One bug caught and fixed in review:** the kin-state lookup first used `is_culture` on a `random_country`
scope — but `is_culture` is only ever valid inside a *culture* iterator (`random_country_culture`), never
on a country; switched to the proven `primary_culture = <culture scope>` idiom (send_settlers release,
se_QING_DECLINE). Stale header comment updated to match. No conflict markers, no dead references, all
encodings preserved.

**§11 Layer 2b — Qing colonisation reworked to drive the generic migration engine.** New
`common/scripted_effects/se_QING_COLON.txt` (no BOM, tabs, `sys = QING`) is the bridge that turns
the old settle-by-fiat colonisation missions into *incentives* for the Layer 2 bottom-up engine,
honouring the firm bottom-up philosophy — the state makes the frontier attractive and the heartland
crowded, then people move of their own accord:
- `QING_COLON_frontier_pull = { province = <id> }` — sets a durable `migr_gov_pull = 12` variable on
  an *owned* frontier province (the value the generic `MIGRATION_pull_province` score reads behind its
  `has_variable` guard), on the same scale as the natural pull terms so a state-backed frontier
  competes with genuine prosperity without swamping the organic signal. Guarded by `owns` — if the
  land is not yet held, it logs a `LOG_fail` (the pull is deferred until the mission's `add_claim` is
  realised by conquest; you cannot recruit settlers to land you do not hold).
- `QING_COLON_heartland_push = { count = <n> }` — tags the `n` most-populous owned provinces with
  `migr_gov_push = 6` (a nudge on an already-crowded core, read by `MIGRATION_push_province`), turning
  a demographic bulge into actual out-migrants. `LOG_enter`/`LOG_exit` wrap it; `LOG_fail` if the
  country owns nothing to push from.
- `QING_COLON_clear_heartland_push = yes` — lifts the push (`remove_variable`) when crowding is
  relieved, so migration settles back to its organic baseline.

Call-sites rewired (all pre-existing `add_claim` calls **preserved** — a formal claim is a real
diplomatic act that now also feeds Layer 1; only the `create_state_pop` *settling fiat* was replaced):
- `common/missions/qing_colonization_missions.txt` (byte-exact Python edit — no-BOM LF, tabs) — the
  Xinjiang task's two `create_state_pop = freemen` calls became `QING_COLON_frontier_pull` on prov
  2930 & 2977 (fortress/city construction kept); the Taiwan task gained `frontier_pull` on 6799 & 6781
  after the Penghu claim; the Amur task gained `frontier_pull` on 6170. Braces 312/312.
- `events/imp19c_mod_events/qing_frontier_migration_events.txt` (byte-exact Python edit) — the New
  World crop-boom / overpopulation events are now the *push* engine: `.20.a` (managed boom) and `.20.b`
  (unmanaged boom) call `QING_COLON_heartland_push = { count = 3 }`; `.23.b` (neglect) escalates to
  `count = 4`; `.22.a` (blessing) and `.23.a` (relief works) call `QING_COLON_clear_heartland_push`.
  The crop-boom's own `create_state_pop` (population *growth*, not migration) was intentionally kept.
  Braces 152/152.

This closes the loop between two previously-disconnected Qing systems: the colonisation missions now
*aim* the migration engine (pull on the frontier, push in the heartland) rather than bypassing it, and
a Han-settled frontier province that flips its plurality seeds a claim through the same generic
`MIGRATION_seed_claim_if_flipped` path as any settler colonialism.

**Review (§11 L2b — all green).** Braces: `se_QING_COLON` 23/23, `qing_colonization_missions` 312/312,
`qing_frontier_migration_events` 152/152. All 10 `QING_COLON_*` call-sites resolve to the 3
definitions. `migr_gov_pull` / `migr_gov_push` are read only in `MIGRATION_svalues.txt` behind
`has_variable` guards (zero cost when unset) and written/cleared only here. Parameterised idioms
(`owns = $province$`, `p:$province$`, `max = $count$`) are textual substitution verified against proven
repo forms. Inline literals (12 / 6), not `@`-constants (no precedent in this mod's scripted_effects,
and `@` does not substitute inside quoted log strings). Encodings preserved on every edited file. Every
path — set, deferred, cleared, and both empty-guard misses — emits `LOG_line` / `LOG_fail` / `LOG_enter`
/ `LOG_exit`.

**§11 Layer 3 — de jure irredentism (generic) + deep Qing ethnic-tension re-derivation.**
*The runtime-bridge problem:* the culture-plurality de jure table (`map_data/de_jure_output.txt`, §10)
is **generated reference data the engine never loads at runtime**, and Layer 2 migration *mutates* the
live `dominant_province_culture`. So "de jure culture" had to be materialised into script state and
made immutable, or irredentism would evaporate exactly where settlers flip a province.
- `common/scripted_effects/se_DEJURE.txt` (no BOM, tabs, `sys = DEJURE`) — the generic engine, and a
  deliberately **crude, event-driven** layer per the performance guidance:
  - `DEJURE_freeze_setup` — a **one-time** game-start pass (`every_province`, global-var guard
    `dejure_baseline_frozen` so it runs exactly once however the engine fires it) that stores each
    settled province's starting plurality culture *scope* into `var:dejure_culture`. That frozen value
    is the province's rightful (1815) culture.
  - `DEJURE_on_ownership_change` — fired from the existing `on_ownership_change` on-action (no new
    polling; conquest is infrequent). If the new owner has **not integrated** the land's rightful
    culture (`is_integrated` neatly excludes the owner's own primary culture, so retaking your own de
    jure land triggers nothing), it applies a decaying `dejure_disaffection` province modifier
    (`local_unrest = 3`, `local_monthly_civilization = -0.05`, ~20-yr duration, re-applied per conquest)
    and calls `DEJURE_seed_dejure_claim`.
  - `DEJURE_seed_dejure_claim` — the kin-state of the *frozen* de jure culture (`random_country` with
    `primary_culture = scope:dj_rightful`, not owner, not already core) gains `add_claim`. Keyed to the
    frozen culture, not the live plurality — so a conquered/demographically-swamped people still has its
    homeland claimed on its behalf. A stateless rightful culture logs a diagnostic and adds no claim.
  - Wired via new `common/on_action/dejure_on_actions.txt` (`on_game_initialized { effect { DEJURE_freeze_setup } }`,
    engine-merged with the Qing suite's block) and a three-line insert into `on_ownership_change` in
    `00_specific_from_code.txt` (byte-exact, CRLF+single-BOM preserved) right after the Layer 1 call.
  - `dejure_disaffection` modifier added to `00_from_events_province.txt`; localised (bilingual, 非本族統治)
    in `modifiers_l_english.yml` (byte-exact, BOM preserved).
- **Qing extension in `se_QING_DECLINE.txt`** — the `qing_ethnic_tension` counter (was hand-tuned nudges)
  is now largely **computed from the realm's real ethnic geography**, and — per the annual-vs-quarterly
  decision — split into a heavy annual scan + a cheap quarterly drift:
  - `QING_DECLINE_scan_ethnic_target` (annual, `yearly_country_pulse`, **CHI + human only**) — an
    `every_owned_province` scan tallies *restive* land (owned, settled, has a frozen de jure culture
    that CHI has **not** integrated), weighting +1 base, +1 if `province_unrest >= 4`, +1 if the rightful
    people are no longer the plurality (settler displacement). On the **first** scan it freezes the 1815
    weighted tally as `qing_ethnic_restive_base`; the target is `20 + (current − baseline)/2`, clamped
    0..100. This calibration is what makes the manchu-primary / Han-majority realm sit at the historical
    ~20 at start (the huge static mass of un-integrated Han de jure land *is* the baseline and nets to
    zero) and move only as conquest / integration / migration change the realm. The scope of the frozen
    culture is pulled into a named scope (`save_scope_as = dj_rightful_c`) before the `any_country_culture`
    test — **a review-caught bug fix**: `prev.var:dejure_culture` would resolve `prev` to the country
    (where the variable does not live); a saved scope is unambiguous across the scope change.
  - `QING_DECLINE_drift_ethnic_tension` (quarterly, O(1)) — drifts the live counter ±3/pulse toward the
    scanned target; logs a `LOG_fail` before the first annual scan has produced a target. Called from
    `QING_DECLINE_pulse` before reform-pressure so the latter reads a fresh value. The existing
    `QING_ethnic_stance_drift` still nudges on top as a player lever (dyarchy can hold tension below the
    demographic baseline). All bands / reform-pressure consumers that read `qing_ethnic_tension` are
    unchanged and keep updating every quarter.
  - **Performance:** the only O(provinces) work (the demographic scan, ~600 provinces for CHI) runs
    **once a year, human-Qing-only**; everything else is O(1). Ethnic tension moves only through slow
    processes that do not shift within a year, so annual granularity is near-lossless while cutting scan
    cost ~4× vs. per-pulse. The generic layer adds **zero** new polling (freeze once + react on conquest).

**Review (§11 L3 — all green).** Braces balanced: `se_DEJURE` 35/35, `dejure_on_actions` 2/2,
`se_QING_DECLINE` 479/479, `00_yearly_country` 22/22, `00_specific_from_code` 318/318 (single BOM, CRLF
preserved), `00_from_events_province` 337/337. All five new symbols (`DEJURE_freeze_setup`,
`DEJURE_on_ownership_change`, `DEJURE_seed_dejure_claim`, `QING_DECLINE_scan_ethnic_target`,
`QING_DECLINE_drift_ethnic_tension`) resolve from their call-sites. Every idiom verified against proven
repo usage: `every_province` global iterator (se_FUNC/se_GLOBALTRADE), `set_variable value = <scope link>`
storing a culture (`value = owner`/`value = employer` precedent + `dominant_province_culture` as a scope),
`var:X = { save_scope_as }` (se_SELL, 00_ambitions), `is_culture = scope:<culture>` inside
`any_country_culture` (on_state_secession, Invictus), `is_integrated` on a country-culture scope
(governor_policies), count-into-var then `divide = var:` (se_QING_COUNCIL). **One bug caught and fixed in
review:** the `prev.var:dejure_culture` scope error described above. Encodings preserved on every edited
file. Full `sys = DEJURE` / `sys = QING` logging on every path incl. guard-misses.

**§11 Layer 4 — reconquest wargoal + separatist-rebellion engine.** Two parts.

*Reconquest wargoal* (`common/wargoals/00_default.txt`, new `reconquest_wargoal`): a cheap
`take_province` war (`conquer_cost = -0.4`, `ticking_war_score = 1`) offered only when the attacker
actually holds a Layer 1-3 seeded claim on the defender's land. The `allow` block tests
`scope:defender = { any_owned_province = { is_core_of = root } }` — in a wargoal `allow` block **root
is the attacker** (verified against Invictus' `maurya_revival_wargoal`, whose top-level `tag`/`is_subject`
tests read the attacker), and `add_claim` is read back via `is_core_of` (the repo-wide convention used by
`se_CLAIM_HOSTILITY`/`se_MIGRATION`/`se_DEJURE`). Loc keys `war_goal_reconquest_wargoal(_desc)` added to
`diplomacy_l_english.yml` (BOM+LF, single-space indent preserved). *Corrected in this pass:* the initial
draft used `is_core_of = prev.prev`, changed to the unambiguous `root`.

*Separatism engine* (`common/scripted_effects/se_SEPARATISM.txt`, new; sys = SEPAR): where alien rule
has festered — a province still carries its frozen 1815 `var:dejure_culture`, a live `dejure_disaffection`
modifier, and real unrest — the people can rise and tear the land away as a new country:
- `SEPARATISM_country_pulse` (generic, on the **existing** `decade_country_pulse` via a new
  `SEPARATISM_decade_pulse` child on-action — **no new polling hook**): cheap guard (own a high-unrest
  disaffected de jure province) + decade cooldown (`separatism_cd`) + a low chance roll (20%). At most one
  attempt per country per decade, usually none.
- `SEPARATISM_try_secession`: picks the angriest disaffected province, takes its **frozen** rightful
  culture as the banner, gathers every owned disaffected province of that same rightful culture into
  `sep_secession_provinces`.
- `SEPARATISM_spawn_breakaway`: `LAND_release_from_list` spawns the rebel state (economy init handled by
  the existing `ECON_events.7`/`monthly_setup_new_countries` safety net — no inline `FUNC_setup_new_country`
  needed), the working list is cleared immediately after (codebase convention, per `se_SUBJECT_QING`), the
  parent wages `reconquest_wargoal` via `FUNC_declare_war_with_wargoal_province` (which saves
  `scope:current_war_scope`), and a backer may join the rebels.
- **Cross-border liberation (Option A, user-approved):** `SEPARATISM_liberate_across_borders` — when a
  culture is split across several empires (Poles, Kurds, Balkan peoples under multiple crowns), the one new
  national state also wages **liberation wars** on its *other* parents to reunite its whole homeland. For
  each **neighbouring** other empire (not the parent, not the rebel, non-subject) still holding frozen de
  jure land of the rebel culture, it grants the rebel `add_claim` on that empire's de jure-X provinces and
  declares a `reconquest_wargoal` there via `FUNC_declare_war_with_wargoal_province`. Capped at
  `@separatism_max_extra_fronts = 3` fronts; the cap is **enforced by an `if` inside the loop body** (not the
  `every_` limit — Clausewitz builds the candidate list once, so a mutating-counter test in the limit never
  bites) and any skipped fronts are logged (no silent truncation). Feasible because `LAND_transfer_provinces`
  transfers each province individually reading its own governorship (multi-owner-safe). **Scope-safety fix:**
  `FUNC_declare_war_with_wargoal_province` overwrites `scope:current_war_scope` on every call, so the primary
  reconquest war is pinned to `scope:sep_primary_war` *before* the liberation loop runs; the backer then joins
  `sep_primary_war` (not the last liberation war, which would have put the kin-state on the wrong side).
- **Backer rule (firm, user):** the backer must be a **neighbouring country where the rebel culture
  actually lives** — `scope:sep_rebel_state = { random_neighbour_country = { any_country_culture = {
  is_culture = scope:sep_culture } ... } }` — never a random or far-flung power, and broader than the
  titular kin-state (a multiethnic neighbour holding those pops qualifies). Joins via `add_to_war`
  (attacker = no). See memory `imp19c-separatism-backer-rule`.
- *Qing extension* `SEPARATISM_qing_pulse` (on the quarterly Qing pulse in `00_monthly_country.txt`,
  CHI+human only): layers an **extra**, tension-scaled risk on top of the generic decade cadence — gated on
  `qing_ethnic_tension >= 45`, with a ~3yr cooldown and a chance banded 30/50/75% as tension climbs past
  60/80. Reuses the generic `SEPARATISM_try_secession` core verbatim; only cadence + trigger are Qing-specific.

*Why a real country, not engine rebels:* the vanilla `on_state_secession` path only flips loyalty — it
cannot let the seceded land be joined/annexed by a third power, which is the whole point. Spawning an actual
country lets the kin-state be invited into the war.

*Support Rebels feasibility (user question):* the vanilla `support_rebels` diplomatic action is a
**hardcoded engine registration** — neither Invictus nor Terra-Indomita defines *any* custom diplomatic
action, and this repo's `common/faction_impact/diplomatic_actions/00_default.txt` is a 3-byte empty stub, so
a new action cannot be registered and `support_rebels`' core behaviour cannot be rewritten in script. Only its
**price** (`prices/00_hardcoded.txt`), its three applied **modifiers** (`foreign_support_for_rebels`,
`foreign_rebels`, `supporting_rebels_abroad` in `modifiers/00_hardcoded.txt`) and its **party-approval impact**
are tunable; there is no `on_support_rebels` on-action hook. Conclusion: the covert-backing feature is built as
a bespoke **diplomatic-play event chain** (the `agitator_sponsorship` model in `se_DIPLOMACY`), not by
extending the engine action — matching the original plan.

**Review (§11 L4 — all green, two passes).** Braces balanced: `se_SEPARATISM` 106/106 (after the
cross-border addition), `00_default` (wargoals) 23/23, `00_decade_country` 8/8, `00_monthly_country` 36/36.
All five `SEPARATISM_*` effects resolve from their call-sites; the two new on-action children
(`SEPARATISM_decade_pulse`, `SEPARATISM_qing_pulse`) are wired. Every idiom verified against proven repo
usage: `LAND_release_from_list` (all 12 params match its consumed set; `set_primary_culture` accepts a
culture scope, confirmed at se_LAND.txt:709/717 — so passing `scope:sep_culture` is valid), saves
`scope:new_country_scope`; `FUNC_declare_war_with_wargoal_province` (called on attacker, saves
`scope:current_war_scope`, no `war = no` guard so simultaneous liberation wars are allowed);
`every_neighbour_country`/`random_neighbour_country` (Invictus + assemble_war_council_button);
`any_country_culture { is_culture = scope: }` (se_DEJURE); `var:X = scope:Y` equality-as-trigger (se_AI);
`random { chance }` (se_QING_DECLINE); list build→clear (se_SUBJECT_QING); variable interpolation
`[SCOPE.MakeScope.GetVariable('n').GetValue|0]` (se_QING_COUNCIL). **Second-pass review fixes (code-review
agent):** (1) added `LOG_fail` for the "no eligible backer / roll failed" path (was a silent no-op); (2) added
`LOG_fail` `else` for the primary-war-didn't-resolve pin; (3) replaced `@separatism_max_extra_fronts` inside a
quoted log string with the literal `3` (`@`-constants aren't substituted inside strings). Encoding:
`se_SEPARATISM` no-BOM LF, loc BOM+LF preserved. Full `sys = SEPAR` logging on every path incl. guard-misses.
*Known design assumption (flagged, not a bug):* the cross-border loop and backer query run on the rebel
`scope:sep_rebel_state` created earlier the same tick; if the engine doesn't refresh country adjacency until
after the tick, they'd no-op on the spawning secession — worth a `-debug_mode` confirmation, and shared with
the already-shipped backer code.

**§11 L4 ext — Qing civic (national) identity, the positive counterweight to ethnic tension.** A new
0..100 country meter (`qing_civic_identity`) on CHI that models a coalescing *civic* "Chinese" nation
(中華民族) binding the multiethnic empire together — the answer the L1–L4 program's separatist pressure
demands. All in `se_QING_DECLINE.txt` (+ modifiers, effect, GUI, loc). Reuses the existing
`chinese_group` Sinitic culture group (beihua/wu/xiang/gan/jin/hakka/min/yue/… — excludes Manchu/Mongol/
Tibetan/Turkic); culture *groups* are static load-time data (no runtime `set_culture_group`), so the group
is the civic core and `integrate_country_culture` / `set_pop_culture` are the runtime levers.
- **Drift (`QING_DECLINE_drift_civic_identity`, quarterly):** target = self-strengthening progress
  (`qing_selfstr_progress`) — civic identity CANNOT outrun the movement whose schools/press/telegraph ARE
  the connective tissue. Hollow modernization (`qing_selfstr_hollow_flag`) halves the ceiling; the inclusive
  **dyarchy** stance lifts it +15; a **favouritist** stance (banner/han) caps it −20. Clamped 0..100, drifts
  ±2/pulse (slower than tension — nations are built over generations).
- **Civic relief on tension (`QING_DECLINE_drift_ethnic_tension`):** the effective tension target the live
  counter drifts toward is `scanned_demographic_target − civic_identity/2` (clamped). A maxed civic identity
  shaves up to 50 points off the demographic baseline — a high-civic realm sits below the `>= 45` gate of
  `SEPARATISM_qing_pulse` and largely escapes L4 separatism. Nation-building is thus a *real, powerful*
  answer to the separatist threat the program creates. Relief computed into a scratch var each pulse (never
  mutating the annually-scanned target the scan owns).
- **Annual nation-building pass (`QING_DECLINE_civic_assimilation`, from `00_yearly_country.txt`, CHI+human)
  — two registers:** **(A) Integration bridge (inclusive citizenship, ≥ 50):** integrates ONE not-yet-
  integrated *rightful* culture per year — walks our restive de jure provinces (`var:dejure_culture`), and
  a positive `any_country_culture { is_integrated = no is_culture = scope: }` test both confirms the culture
  is actually *present* among our pops (skips fully-displaced peoples) and un-integrated before spending the
  year; body-side `qing_civic_bridge_done` sentinel caps it at one (an `every_` limit can't cap mid-loop).
  Because tension is derived from un-integrated restive land, this lowers next year's scanned target. No
  culture erased — minorities become citizens. **(B) Sinicization melting pot (assimilative, ≥ 70):** the
  *popular* counterpart to the elite `qing_manchu_identity` meter and customs-service sinicization. Driven by
  **majority weight, NOT strife** (user, firm — applies to happily-integrated pops too): in the ≤4 most-
  populous provinces where a Sinitic culture is already a majority (`any_pops_in_province percent >= 0.5`),
  one non-Sinitic non-slave non-noble pop `set_pop_culture`s into the local Sinitic plurality; an *over-
  whelming* majority (≥ 75%) pulls a second the same year. Deliberately **no unrest/happiness filter** —
  follows demography, never manufactures a majority that isn't there (complements L2 bottom-up migration).
- **Bands (`QING_DECLINE_apply_civic_band`):** `qing_civic_nascent` (≥ 25, −1 unrest/loyalty), `_emerging`
  (≥ 50, +assimilation/stability), `_national` (≥ 85, strong loyalty + assimilation + civilization) — the
  inverse counterweight to `qing_ethnic_high_tension`.
- **Player lever:** `QING_promote_civic_identity` (effect) + `qing_action_promote_civic` (GUI button, shown
  once `qing_selfstr_progress >= 10`, costs £90) nudges civic +8 and self-strengthening +3 (shared
  institutions). Loc `qing_civic_*`, `QING_ACTION_PROMOTE_CIVIC_TT` in `qing_mechanics_l_english.yml`.

**Review (§11 L4 ext — all green).** Braces `se_QING_DECLINE` 609/609, `se_QING_MECHANICS` 89/89,
`QING_mechanics_actions` 155/155. All modifier keys verified real; all called effects resolve; `chinese_group`
RHS token form proven (`00_language_groups.txt:227`); `integrate_country_culture = scope:` / `set_pop_culture
= scope:` proven (Invictus, Terra-Indomita). Full `sys = QING` logging incl. guard-misses. **Code-review fixes
(this pass):** (1) **scope-direction bug** — part (A) originally nested `any_owned_province { var:dejure_culture
= prev }` *inside* `any_country_culture` (a culture scope has no owned-province list; the var lives on the
province) — the exact reverse-scope trap the file warns about at the ethnic scan; rewrote to iterate provinces
+ save the frozen culture scope + inner body-side cap. (2) part (B) **silent no-op** when the gate passes but
no province matches — added a `qing_civic_sinic_done` sentinel (set on ROOT — loop body scope is the province)
+ `LOG_fail`. (3) part (B) **misleading success log** — added `NOT = { pop_type = nobles }` to the outer gate
so it matches the helper's real eligibility (helper excludes nobles), and (4) part (A) **wasted integration**
on a fully-displaced culture — the positive presence test now guards it.

### Deferred (need design input from you)
- **§5 new laws** (tariff/subsidy/tax-tier) & **§5 inventions** — beyond filling the currency_law
  stub, net-new law/invention *content* is a balance/design surface. The stub-fill is the safe
  slice; new levers should be scoped with you.
- **§6 mission trees** — proven capability but net-new content; which nation + what goals is your call.
- **§8/§9 parties/offices** — as in the Tier-2 section above.
- **§10 formable-requirement de jure** — NOTED, deferred indefinitely (user). Unlike the
  culture-plurality table, this is **not generatable** — culture ≠ nation, so there is no column
  to roll up. It needs an *authored* historic-nation de-jure column in `province_setup.csv`, and
  filling that means a per-formable historical-geography judgment (which areas constitute each
  formable's rightful/historic territory) **for every formable across the whole globe** — a large
  research burden (borders shift by era; historic vs. aspirational extents differ; hypothetical
  formables have no single correct extent) with modest payoff. Only *then* could the generator
  emit a formable→areas table for `imp19c_can_form_country_trigger`'s "control X% of your historic
  territory" check. The formable decisions are all 0-byte stubs today. Not worth doing now.

### Review (per standing instruction — all green)
Braces balanced on all touched files (`se_ECON_LOG` 35/35, `oa_wealth_changes` 145/145,
`00_monthly_job_pulse` 4/4, `00_economic_laws` 49/49, `JOBS_svalues` 103/103,
`se_CURRENCY_STRESS` 58/58, `se_QING_DECLINE` 430/430, `00_currency` 3/3,
`currency_crisis_events` 12/12). Every called `ECON_LOG_*` / `CURR_STRESS_*` effect resolves to
a definition. All §5 law keys and §3 modifier keys valid. All §3 loc keys resolve; loc BOM
added to match siblings. BOM integrity preserved (present where it was, absent on `se_ECON_LOG`
to match sibling `se_LOG`). §7 marker correctly inside an `effect` block (valid in "none" scope).
§2: no lingering references to the removed undefined svalues anywhere in the repo (only
explanatory comments name them); the corrected `JOBS_industrial_workers` matches the shape of
the other summed categories. §3: Qing refactor behavior-preserving (same counter/thresholds/
modifiers); no var collision; `picture = trade_wealth` bad-reference caught and fixed to
`trade_port`. No conflict markers, no dead references.


---

## New World crops (#64) — five fully-simulated cash-crop trade goods

Added **maize, sweet_potato, potato, peanut, chili** as producible/tradeable goods, cloned
deterministically from the `tobacco` archetype (category-2 consumer cash crop: price- and
trade-simulated, gives `local_monthly_food` via its `trade_goods` block, NOT part of the fixed
6-good staple DEMAND basket, no downstream industrial recipe). Generated by
`zz_newworld_crops_clone.py`, which clones tobacco's full ~30-file / 100+-site reference surface
with per-file brace verification and BOM/CRLF preservation.

* **Definition** — `common/trade_goods/00_imp19c.txt`: five `category = 2` goods, each with a
  distinct `color` (hsv).
* **Simulation surface** — national-production / stockpile / governorship-produced / country-sold
  svalues (`GOODS_svalues`), demand (`DEMAND_svalues`, `DEMAND_luxury_svalues`), price
  (`PRICE_svalues`, `AI_svalues`), trade/export (`TRADE_svalues`, `se_TRADE`, `se_SELL`,
  `se_PURCHASE`, `se_TRADE_new`, `se_GLOBALTRADE_split`), wealth/durability (`WEALTH_svalues`),
  excise income (`INCOME_svalues` — clones use `add =`, not tobacco's initializing `value =`),
  food contribution (`DEMAND_food_svalues`), stockpile init + produce path (`se_GOODS`),
  demand-from-luxury (`se_DEMAND`), resource-building potential + trade triggers, ECON custom-loc,
  and cultural fascination/taboo modifiers.
* **Iterator injectors** — the four `zz_*injector.txt` tables each got a **standalone**
  `$PREFIX$<crop>$SUFFIX$` wrapper per crop (one `$APPLY$` each), so every crop is addressable by
  name on the targeted `parse_/switch_/random_` injector paths — not nested under tobacco's
  wrapper (a latent bug the code review caught and we fixed).
* **Map placement** — `common/province_setup.csv`, 28 provinces converted from grain/livestock,
  historically grounded: maize → Hunan/Jiangxi; sweet_potato → Fujian + E-Guangdong + coastal
  Peru; potato → Andes + New Mexico highland; peanut → Fujian/E-Guangdong + Peru coast; chili →
  Hunan/Sichuan + Mexican homeland. Americas homelands seeded so the goods exist as targets for
  the Qing colonization missions.
* **Localization** — real names + flavour descriptions (`imp19c_tradegoods_l_english.yml`); the 25
  economic-UI loc lines cloned (`economic_enchancement_l_english.yml`).

**Code review (per standing rule):** dispatched a review agent over the whole clone. Verdict —
functionally complete and correct for all live runtime paths: no missed tobacco reference site, no
dropped aggregate-sum term, INCOME accumulator correct, distinct colors, no duplicate keys, no loc
gaps, no map typos. The one structural finding (crops nested under tobacco's injector wrapper) was
latent (the live `every_*` path fired them all) but fixed anyway so the crops are name-addressable
on all injector paths.

## Economy audit P0 fixes (#68, #70, #71, #72)

Two audit agents swept the trade and industry/production systems; the P0 findings were fixed:

* **#68 — PRICE divide-by-zero.** `PRICE_grain_demand_difference_modifier` (`PRICE_svalues.txt`)
  divided by `PRICE_grain_demand_difference_raw` in its `else` branch, which fired on `raw == 0`
  (supply exactly meets demand) → NaN. Added an `else_if { raw = 0 -> value = 1 }` guard (no price
  pressure = no-op modifier). These three `PRICE_grain_*` svalues have no live consumers today; the
  fix is defensive against re-activation.
* **#70 — industrialisation-bonus divide-by-zero.**
  `GOODS_governorship_bonus_to_industrial_production_from_industrialisation` (`GOODS_svalues.txt`)
  divided by the governorship's state count, which is 0 for a stateless governorship → NaN
  multiplier corrupting ALL industrial output. Guarded with `any_governorship_state = { count >= 1 }`;
  the no-state case returns 1.
* **#71 — cache the industrialisation multiplier.** That bonus was recomputed ~28× per governorship
  per quarter (each read a double state-traversal). Split into a `_compute` svalue (the guarded math)
  and a cached wrapper that reads `var:industrialisation_bonus_cached` **if present, else computes**
  (so a missing cache degrades to correctness, never to zeroed output). `GOODS_cache_industrialisation_bonus`
  refreshes the cache once at the top of `GOODS_governorship_produce_all` (the quarterly hot path) and
  in the setup governorship loops, keeping it current as civilization drifts.
* **#72 — se_LOG on the production path.** The quarterly production path had zero tracing despite the
  `quarterly_production` phase markers around it. Added `ECON_LOG_production_snapshot` (per-country:
  producing-governorship count + summed industrialisation bonus, verified `ROOT.MakeScope` form) wired
  into `quarterly_trade_pulse` after the produce loop, plus a per-governorship cache-line from
  `GOODS_cache_industrialisation_bonus`. All no-ops outside `-debug_mode`.

All touched files: braces balanced, BOM/CRLF preserved to match each file's existing convention.
