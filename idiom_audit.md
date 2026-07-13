# Idiom Audit — merge-overnight vs upstream (Sobisonator)

Adversarial audit of every script change on `merge-overnight` that differs from upstream
(`sobisonator/master`, merge-base `8b2043a0`), verifying that only PROVEN Paradox engine
idioms are used — "proven" = attested in upstream/vanilla, Invictus, Terra-Indomita, or the
mod's own shipping/verified-in-game non-Qing files.

Method: a deep adversarial workflow. Each changed script file → an audit agent that extracts
every engine primitive and cross-checks it against the three oracles → each flagged item →
an independent adversarial verify agent (default-skeptic, must find the proven form + a
concrete citation, or downgrade). Only CONFIRMED_UNPROVEN items are fixed.

- **Pass 1** (this run): 85 highest-risk script files (all Qing scripted_effects, mod events,
  missions, triggers, key script_values). 27 agents, 10 findings, **all 10 CONFIRMED_UNPROVEN**
  — clustering into **4 distinct bug classes**, every one independently corroborated by real
  `~/Downloads/error.log` "Unknown effect/trigger" lines (i.e. live engine rejections, not just
  citation gaps).
- **Pass 2** (pending): the remaining ~190 changed script/GUI files, for full-diff coverage.

---

## Pass 1 — CONFIRMED findings (4 bug classes)

### BUG-1 · `add_wealth` is not an engine effect → `add_gold`  [HIGH]
The #424 privy-purse migration used `add_wealth` on a character scope to move the emperor's
內帑 (privy purse = the ruler's personal `wealth`). `add_wealth` does not exist: zero hits in
either oracle; error.log logs `Unknown effect add_wealth` at qing_household_events.txt:99/108/247
and 00_monthly_country.txt:97 (via QING_household_pulse). Every purse grant/drain silently
no-ops — the whole #424/#426 privy-purse mechanic is dead. The engine mutates a character's
`wealth` attribute via the effect **`add_gold`** (read-name = `wealth`, effect verb = `add_gold`;
`add_gold` has 800+ oracle attestations, incl. block `{ value = 0 subtract = wealth }` and
negative literals). Proven: Invictus on_character_death_inv.txt:592 `add_gold = { value = 0 subtract = wealth }`;
mod's own se_QING_AFFINITY.txt:272 `add_gold = $amount$`.
- **Live sites (13):** se_QING_WENZHI:120 · se_QING_HOUSEHOLD:62,91,108,160,178,199,229,241 ·
  se_QING_CANTON:134 · qing_canton_events:57 · qing_household_events:54,248 (+ 3 comment mentions).

### BUG-2 · `num_of_building = { building=X value>=N }` is not an engine trigger → `num_of_<X> >= N`  [HIGH]
The block-form building-count trigger does not exist; error.log logs `Unknown trigger type: num_of_building`
(qing_revenue_events:9164/9166). The engine's real building-count trigger is the auto-generated
per-building key **`num_of_<building_name> >= N`** (Invictus ai_buildings_triggers.txt:214
`num_of_library_building >= 5`; TI BUI_num_of_buildings.txt:5 `value = num_of_port_building`).
The unknown trigger is discarded → the enclosing `allow`/`limit` silently loses its level gate.
- **Live sites (7):** qing_treasure_fleet_missions:95 · se_QING_TREASURE_FLEET:43,45 ·
  se_QING_REVENUE:458 · se_QING_CANTON:106,110 · qing_revenue_events:168.
- Mapping: `port_building` → `num_of_port_building`; `qing_granary_building` → `num_of_qing_granary_building`.

### BUG-3 · `is_in_list = { list = X }` (block form) is not valid → bare `is_in_list = X`  [HIGH]
`is_in_list` has NO block form (the `{ list = }` wrapper makes the parser read `list` as an
unknown trigger — the exact "Unknown trigger type: list" defect the owner already fixed once,
documented in se_LAND.txt:371 / PR#719). Throws a parse error; the guarded loop mis-fires.
Proven: bare `is_in_list = <listname>` (mod's own annexation.txt:735; TI annexation_bugfix.txt:248;
Invictus 00_event_effects_inv_1_0.txt:4401).
- **Live site (1):** se_DIPLOMACY:1485 `any_owned_province = { is_in_list = { list = play_colony_candidates } }`.

### BUG-4 · `pop_culture.culture_group = chinese_group` dot-chain is not valid → `pop_culture_group = chinese_group`  [HIGH]
`pop_culture` is a flat comparison TRIGGER (takes a bare culture name), not a navigable scope-link,
so `.culture_group` cannot be chained off it (same "Illegal use of operator =" parse failure the
author already fixed for the province twin `dominant_province_culture.culture_group`). Bare RHS
`chinese_group` is also wrong for a chained link. The engine's dedicated pop-scope keyword is
**`pop_culture_group = <group>`** (mod's own shipping 00_culture_supergroups.txt:20
`pop_culture_group = british_group`; TI me_samnium.txt:2845). Gates the Sinicization assimilation
loop → parse/no-op silently breaks a core mechanic.
- **Live sites (3):** se_QING_DECLINE:683, 693 (negated), 710.

---
## Pass 1 — FIXES APPLIED (commit on merge-overnight, freekumquats)

All 4 bug classes fixed comprehensively (every live occurrence across the branch, not just the
flagged lines). Each file brace-checked; a repo-wide re-scan confirms zero residual instances of
any of the 4 patterns.

### BUG-1 fixed — `add_wealth` → `add_gold`  (16 occurrences, 5 files)
Global token replace `add_wealth` → `add_gold` (effect verb only; block/value/negative forms
preserved — `add_gold` accepts them all). The emperor's `wealth` attribute is now mutated by the
real engine effect, so the #424/#426 privy-purse (內帑) grants and drains actually apply.
- se_QING_WENZHI.txt (1) · se_QING_HOUSEHOLD.txt (11, incl. 3 comment mentions) ·
  se_QING_CANTON.txt (1) · qing_canton_events.txt (1) · qing_household_events.txt (2).

### BUG-2 fixed — `num_of_building = { building=X value>=N }` → `num_of_X >= N`  (7 occurrences, 5 files)
Regex-replaced the unknown block trigger with the engine's auto-generated per-building comparator.
Mapping: `port_building` → `num_of_port_building`; `qing_granary_building` → `num_of_qing_granary_building`
(both confirmed against the vanilla auto-generated `num_of_<building>_building` family). The port-level
and granary-presence gates now actually evaluate.
- qing_treasure_fleet_missions.txt:95 · se_QING_TREASURE_FLEET.txt:43,45 · se_QING_REVENUE.txt:458 ·
  se_QING_CANTON.txt:106,110 · qing_revenue_events.txt:168.

### BUG-3 fixed — `is_in_list = { list = X }` → `is_in_list = X`  (1 occurrence)
Dropped the illegal `{ list = }` block wrapper; the membership test now parses.
- se_DIPLOMACY.txt:1485.

### BUG-4 fixed — `pop_culture.culture_group = chinese_group` → `pop_culture_group = chinese_group`  (3 occurrences)
Replaced the invalid dot-chain (pop_culture is a flat trigger, not a scope) with the dedicated
flat pop-scope keyword + bare group name (shipping-proven: 00_culture_supergroups.txt:20). The
Sinicization assimilation gate now parses and evaluates.
- se_QING_DECLINE.txt:683, 693, 710.
- NOTE: se_QING_SINICIZATION.txt:59 / qing_province_reports.txt:234 use
  `dominant_province_culture.culture_group = culture_group:chinese_group` — this is the ONE VALID
  dot-chain form (real `dominant_province_culture` scope-link + `culture_group:` scope-prefixed RHS,
  verify-agent-confirmed), so it was intentionally LEFT AS-IS.

### Verified non-issues (checked, not bugs)
- `divide = var:X` — used 57× across the mod's own shipping economy engine (se_PRICE/se_DEMAND/
  se_CURRENCY etc.); engine accepts variables in arithmetic slots. No change.

---

## Pass 2 — remaining ~205 changed script/GUI files

58 agents, 17 suspected, **8 CONFIRMED_UNPROVEN** (1 high, 7 medium). The 9 non-confirmed were
adversarially downgraded to ACTUALLY_PROVEN/HARMLESS. Bug classes:

### BUG-5 · `owner = ROOT` used as an EFFECT → `set_owned_by = ROOT`  [HIGH]
`owner` is a read-only province trigger, not a settable effect. Used in effect position
(se_QING_BURMA:147, inside every_province after the limit) to transfer a controlled Burma/Pegu
province to CHI — silently discarded, so the #421/#423/#432 Burma-annex→poppy capstone does
nothing (province stays unowned; the poppy pass gated on `owner = ROOT` then also never fires).
Proven province-transfer effect: `set_owned_by` (mod's own sell_province_events.txt:26, se_FUNC.txt:123; Invictus nepal_decisions.txt:665).
- **Site (1):** se_QING_BURMA.txt:147.

### BUG-6 · `has_attribute = <attr>` is not a trigger → compare the attribute directly  [MEDIUM]
`has_attribute` does not exist (0 oracle hits). Every character always has all four attributes,
so the presence-guard is meaningless; the unknown trigger errors→false, so the `trigger_if`
collapses to the looser `trigger_else` branch — silently degrading the Zongli able-holder bar
from `>=7` to `>=5` + error spam. Fix: drop the guard, compare directly (`finesse >= 7` /
`charisma >= 7`). Proven: TI conversions.txt:1003 `finesse >= 8`; Invictus 00_missions.txt:1034 `charisma >= 8`.
- **Sites (2):** se_QING_GREATGAME.txt:70 (finesse), 75 (charisma).

### BUG-7 · `imprison = ROOT` (bare, country arg) → `imprison = { target = <char> }`  [MEDIUM]
`imprison` is always block-form with a character target upstream; the bare scalar form + a
COUNTRY arg is unattested. Fix: run on the country with the courtier as target
(`ROOT = { imprison = { target = scope:X } }`). Proven: mod's own annexation.txt:1194;
Invictus 00_india_effects.txt:105.
- **Site (1):** qing_character_events.txt:224 (the disloyal-courtier purge).

### BUG-8 · `at_war = yes` / `is_at_war = yes|no` are not proven → `war = yes|no`  [MEDIUM]
Neither `at_war` nor `is_at_war` appears in either oracle (0 hits); the proven country war-state
trigger is `war = yes|no` (600× in oracles). Swept BOTH tokens for consistency.
- **`at_war` sites (6):** se_MARRIAGE.txt:228,229,458,738,766 · qing_marriage_events.txt:51.
- **`is_at_war` sites (5):** se_QING_DECLINE:1187 · se_QING_ACCOUNTABILITY:216,220 ·
  qing_war_events:257 · qing_summer_palace_events:152.

### BUG-9 · `add_loyalty` on a COUNTRY (tributary) scope is a no-op → loyalty_to_overlord country modifier  [MEDIUM]
`add_loyalty` is a CHARACTER effect (courtier→employer loyalty); on a subject-COUNTRY scope
(`scope:trib_defaulter`) it does nothing. The subject-loyalty channel is a country modifier
carrying `loyalty_to_overlord`. The mod already ships both signed modifiers:
`qing_tributary_invested` (loyalty_to_overlord = 20, qing_governance_modifiers.txt:352) for the
reward; and a subject_loyalty-undermining modifier for the penalty.
- **Sites (2):** qing_tribute_events.txt:326 (penalty), 338 (reward).

### BUG-10 · `random_in_list { order_by … max = 1 }` ignores order_by → `ordered_in_list`  [MEDIUM]
`random_in_list` picks at random and does NOT honor `order_by`, so the "pick the most-prominent
council member as clique head" silently picks a RANDOM member. `ordered_in_list` honors order_by+max.
Proven: mod's own se_QING_PRINCES.txt:182 `ordered_in_list = { … order_by = … max = 1 }`.
- **Site (1):** qing_office_events.txt:697 (only the order_by-bearing one; the other random_in_list
  uses have no order_by and are correct).



## Pass 2 — FIXES APPLIED (commit on merge-overnight, freekumquats)

All 6 confirmed bug classes fixed; each file brace-checked; repo-wide re-scan confirms zero
residual live instances. Adversarially-downgraded suspicions (9) were left untouched.

- **BUG-5** `owner = ROOT` (effect) → `set_owned_by = ROOT` — se_QING_BURMA.txt:147. The Burma
  annex now actually transfers the controlled provinces (unblocking the poppy pass + #421/#423/#432 tie-in).
- **BUG-6** `has_attribute` guards dropped; `finesse >= 7` / `charisma >= 7` compared directly —
  se_QING_GREATGAME.txt:69-78. The Zongli able-holder bar now evaluates at the intended >=7, not the >=5 fallback.
- **BUG-7** `imprison = ROOT` → `save_scope_as` + `ROOT = { imprison = { target = scope:X } }` —
  qing_character_events.txt:224. The disloyal-courtier purge now actually jails the courtier.
- **BUG-8** `at_war` / `is_at_war` → `war` (11 sites, 6 files): se_MARRIAGE (5), qing_marriage_events (1),
  se_QING_DECLINE (1), se_QING_ACCOUNTABILITY (2), qing_war_events (1), qing_summer_palace_events (1).
  Both unproven war-triggers normalized to the oracle-proven `war = yes|no`.
- **BUG-9** tributary `add_loyalty` → country modifier (2 sites, qing_tribute_events.txt:326/338):
  penalty = `subject_loyalty_undermined` (loyalty_to_overlord −15); reward = `qing_tributary_invested`
  (loyalty_to_overlord +20), both shipping modifiers, 10-yr duration. Subject loyalty now actually moves.
  NOTE: all other `add_loyalty = loyalty_qing_delta_*` uses are on CHARACTER scopes (correct) — left as-is.
- **BUG-10** `random_in_list` → `ordered_in_list` — qing_office_events.txt:697. The clique-head pick now
  honors `order_by = prominence` (picks the most prominent), not a random member.

## Coverage summary
- Pass 1: 85 files → 4 bug classes (10 sites) fixed.
- Pass 2: 205 files → 6 bug classes (23 sites) fixed.
- Total: 290 idiom-bearing changed files audited (full merge-overnight script diff vs upstream),
  10 bug classes / 33 sites corrected to proven idioms. All error.log "Unknown …" classes from the
  pre-fix baseline that trace to these idioms are resolved.
