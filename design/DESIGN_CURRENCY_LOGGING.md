# DESIGN — Currency diagnostic logging (#28) — v2 (post-review rewrite)

**Branch:** merge-overnight. **Status:** DESIGN v2 (rewritten after adversarial review of v1). **Scope:** CHI-only, -debug_mode.
**Serves:** #23 (the "deflation resets to −10% every year" report).

## 0. What the v1 review changed (why this is a rewrite)

The v1 design assumed we could render numeric currency values into a script `debug_log`. The adversarial
review proved that is **INFEASIBLE**: there is **no working numeric-value render anywhere in the repo** —
every `.GetValue` / `ScriptValue` / `Multiply_CFixedPoint` reference is either a comment documenting the
FAILURE (the removed ECON_LOG snapshot bodies) or a `.gui`/`.yml` DISPLAY string. The `MakeScope` promote
does not resolve in a script debug_log; the "staging then render" fallback also relies on the same
unproven render. So v2 does NOT render numbers.

The review also reframed **#23**: there is **NO annual reset** anywhere in `se_CURRENCY.txt` /
`CURRENCY_svalues.txt`. `CURRENCY_amt_circulated_deflation` (CURRENCY_svalues.txt:1111) is a script_value
`value=1; subtract=private_cash_ratio; min=0.001; divide=10`, whose ceiling is exactly **0.1 (=10%)** when
`private_cash_ratio → 0`, recomputed EVERY read. So "−10% every year" is almost certainly the **equilibrium
ceiling of a chronically starved money supply**, recomputed quarterly — not an annual event. The v1 "yearly
site" (`yearly_country_pulse`, oa_wealth_changes.txt:1) contains **no currency logic at all** (education +
4 quarterly trade pulses) — a red herring. Circulation/ratio recompute **quarterly** (oa_wealth_changes.txt:
345-347); minting is **monthly** (:111-122).

## 1. The PROVEN idiom to use — band-bucketing, NO render

`ECON_LOG_fx_classify_good` (se_ECON_LOG.txt:300-486) is the working, greppable pattern already in the file:
stage a script_value into a temp var (`set_variable = { name = X  value = <script_value> }` — proven, does
NOT error), then CLASSIFY it with sentinel comparisons and emit a BAND LABEL — no numeric render:
```
set_variable = { name = ECON_LOG_cur_ratio  value = CURRENCY_private_cash_ratio }
if      = { limit = { NOT = { has_variable = ECON_LOG_cur_ratio } }         debug_log = "IMP19C CURR ratio = UNSET" }
else_if = { limit = { var:ECON_LOG_cur_ratio >= 1 }                          debug_log = "IMP19C CURR ratio >= 1.0 (inflation side)" }
else_if = { limit = { var:ECON_LOG_cur_ratio >= 0.5 }                        debug_log = "IMP19C CURR ratio 0.5-1.0 (mild deflation)" }
else_if = { limit = { var:ECON_LOG_cur_ratio >= 0.1 }                        debug_log = "IMP19C CURR ratio 0.1-0.5 (serious deflation)" }
else    = { debug_log = "IMP19C CURR ratio < 0.1 (deflation FLOOR ~-10%)" }
remove_variable = ECON_LOG_cur_ratio
```
This tells us WHICH band the ratio sits in each cycle — enough to see whether it's pinned at the floor and
whether minting moves it, without ever rendering a float.

## 2. What to log, and WHERE (retargeted per review)

Drop the yearly site. Two real sites:

### 2a. QUARTERLY (the recompute) — oa_wealth_changes.txt:345-347
After `CURRENCY_update_amt_circulated`, classify (CHI-only):
- `private_cash_ratio` band (<0.1 / 0.1–0.5 / 0.5–1.0 / >=1.0) — the core signal.
- `private_cash_needed` band + `amt_circulated_scaled` band — to see if the DENOMINATOR is what moves
  (the leading #23 hypothesis: private_cash_needed swings, ratio drops, deflation floor). Use coarse
  magnitude buckets (e.g. thresholds at 10/25/50/75/100M-equivalents — tune to CHI's scale).
- deflation/inflation band (already implied by the ratio band; log explicitly for grep clarity).

### 2b. MONTHLY (minting) — oa_wealth_changes.txt:111-122 / CURRENCY_mint_currency (se_CURRENCY.txt:1371)
- `CURRENCY_minting_rate` band (this IS a variable — but still classify, don't render).
- Whether minting HIT ITS CAP: classify `CURRENCY_minting_rate` vs `CURRENCY_minting_rate_cap`
  (se_CURRENCY.txt:1374-1381 clamps rate to cap) — a "minting capped?" YES/NO line. This is the key
  monthly signal for #23 ("minting 1k barely moves it"): is the player's lever capped or swamped?

### 2c. Reserve correction (the feedback amount)
Classify `CURRENCY_inflation_cash_selloff_amt` / `CURRENCY_deflation_money_demand_amt` bands at the
quarterly reserve buy/sell (oa_wealth_changes.txt:345) — to size the auto-correction vs the manual mint
(the #14/#23 "feedback swamps the lever" thesis).

## 3. Structure
- New effect `ECON_LOG_currency_snapshot` in se_ECON_LOG.txt (scope: country), doing the classifications
  above via the proven stage→classify→remove idiom. CHI-gated by the caller.
- Call it at the quarterly site (2a+2c) and a lighter `ECON_LOG_minting_snapshot` at the monthly site (2b).
- Greppable tag `IMP19C CURR` (consistent with the file's `IMP19C ECON`/`IMP19C FORENSIC`). sys via debug_log.

## 4. Gating
CHI-only (`limit = { tag = CHI }` at the call site) + inherent -debug_mode (debug_log only outputs then).
Staging set_variables are a handful of writes on one tag per quarter/month — negligible (confirmed R2/R4/L3).
Obey log-string-macro rule: static strings only (band labels are static — good), no `$macro$`/`#`.

## 5. Files affected
- `common/scripted_effects/se_ECON_LOG.txt` — `ECON_LOG_currency_snapshot` + `ECON_LOG_minting_snapshot`.
- `common/on_action/economy/oa_wealth_changes.txt` — call quarterly (~:347) + monthly (~:120), CHI-gated.
- No changes to CURRENCY_svalues.txt / se_CURRENCY.txt (read-only observation).

## 6. Build checklist
1. Write the two snapshot effects using ONLY the band-bucketing idiom (stage→classify→remove); NO `.GetValue`
   / `MakeScope` / `ScriptValue` render.
2. Pick real bucket thresholds for CHI's scale (ratio is 0..~2.6 per the boot screenshot showing 265%;
   needed/circulation in tens of millions).
3. Wire quarterly + monthly, CHI-gated.
4. Boot-test -debug_mode ~2 in-game years; `grep "IMP19C CURR"`; verify: real band lines emit (no "Could not
   find promote", no errors), the ratio band shows the floor, and whether minting is capped / the denominator
   band shifts. That answers #23.
5. Confirm no NEW error.log classes.

## 7. Alternative the review surfaced (record, don't necessarily build)
The economy panel ALREADY displays deflation %, private_cash_ratio, amt_circulated_balance (loc
economic_enchancement_l_english.yml:1129/1131; economy_view.gui:1040/1081/1163). For a FAST #23 diagnosis,
reading those in-game tooltips across a few years may beat building the trace. But the band log is durable +
greppable + captures the monthly minting-cap signal the tooltip doesn't, so it's still worth building for #23
and future currency work.

## 8. Risk register (v2)
- **R1 (was CRUX): numeric render** → ELIMINATED by using band-bucketing instead. No render anywhere.
- **R2 bucket thresholds mis-chosen** → coarse bands + tune after first boot; low harm.
- **R3 staging set_variable of a script_value that Div/0s** (e.g. private_cash_ratio has min=0.01 so safe;
  private_cash_needed could be negative/zero) → stage into temp (proven not to error), classify with a
  sentinel `> -999999999` UNSET/EMPTY branch exactly as ECON_LOG_fx_classify does. Handles empty/none.
- **R4 #23 is equilibrium not a bug** → if the trace confirms the ratio is simply floored by a starved money
  supply (not an annual reset), the "fix" for #23 becomes a BALANCE question (is the money-supply model too
  tight for CHI?), NOT a code bug — feed that back into #23's design. The log is what distinguishes the two.
