# Dangling References & Integrity Sweep — audit (1763_bookmark)

**Repo**: /Users/alan.chiang/github.com/imp19c  
**Branch**: 1763_bookmark  
**Date**: 2026-07-10  
**Scope**: Mod-added content (se_, QING_/qing_, MARRIAGE_, DIPLOMACY_, CURRENCY_, EDU_, MIGRATION_, SPHERE_, CLAIM_, TRADE_, SHIPPING_, MOBIL_, LOG_, imp19c_ prefixes)

## Method + Caveats

This audit searches for dangling references in mod-added scripted content:

1. **Scripted effects/triggers**: Distinguished DEFINITION (`NAME = { ... }` appearing as block header) from INVOCATION (`NAME = yes` or `NAME = { params }` in effect/trigger context). Macro parameters (`$VAR$`) are excluded.

2. **Script values**: Checked `value = NAME` / `order_by = NAME` invocations against definitions in common/script_values/*.txt.

3. **Modifiers**: Verified `add_*_modifier = { name = X }` and `add_opinion = { modifier = X }` against common/modifiers/*.txt and common/opinions/*.txt.

4. **Events**: Checked `trigger_event = { id = X }` against event namespace definitions.

5. **On actions**: Verified referenced on_action names exist in common/on_action/*.txt.

6. **Localization**: Checked mod-named keys referenced in text=/desc=/custom_tooltip= against localization/english/*.yml.

7. **Defined-but-unused**: Listed mod symbols defined but never invoked (potential dead code).

**Caveat**: Vanilla symbols are out of scope. Dynamic name construction (e.g., `$TAG$_influence`) is not flagged if the pattern is used consistently.

---

## Analysis in Progress


### Class 1: Called-but-Undefined Scripted Effects

**1.1 TRADE_update_all_TZ_local_prices**
- **Invoked at**: common/scripted_effects/se_TRADE.txt:3716
- **Context**: `TRADE_update_all_TZ_local_prices = yes` in TRADE_prepare_quarterly_values
- **Status**: DEFUNCT - definition commented out at se_TRADE.txt:3134-3140 with note "see SELL_set_TZ_prices_OLD"
- **Impact**: Silently no-ops every quarterly trade update

**1.2 TRADE_setup_TZ_travel_time_records**
- **Invoked at**: common/scripted_effects/wip_quicktraderank.txt:57
- **Context**: `TRADE_setup_TZ_travel_time_records = yes` in TRADE_setup_all_TZ_travel_time_records (called per trade center)
- **Status**: No definition found
- **Note**: wip_quicktraderank.txt may be work-in-progress code not yet integrated
- **Impact**: Silently no-ops if TRADE_setup_all_TZ_travel_time_records is invoked


---

## CONFIRMED DANGLING REFERENCES

### Class 1: Called-but-Undefined Scripted Effects

**1.1 TRADE_update_all_TZ_local_prices** — CRITICAL
- **Invoked at**: common/scripted_effects/se_TRADE.txt:3716
- **Context**: Invoked in `TRADE_prepare_quarterly_values`, which runs every trade quarter
- **Definition**: Commented out as DEFUNCT at se_TRADE.txt:3134-3140 with note "see SELL_set_TZ_prices_OLD for what this used to do"
- **Impact**: **HIGH** — Silently no-ops on every quarterly trade update. Intended to update trade-zone-specific local prices; those prices now never update after game start
- **Recommendation**: Either uncomment/restore the definition, or remove the invocation line 3716

**1.2 TRADE_setup_TZ_travel_time_records** — LOW (WIP code)
- **Invoked at**: common/scripted_effects/wip_quicktraderank.txt:57
- **Context**: Invoked per trade center in `TRADE_setup_all_TZ_travel_time_records`
- **Definition**: Not found anywhere
- **Caller usage**: `TRADE_setup_all_TZ_travel_time_records` is defined in wip_quicktraderank.txt:55 but never invoked anywhere in the mod
- **Impact**: **NEGLIGIBLE** — wip_quicktraderank.txt appears to be work-in-progress scaffolding that is not wired into the live economy system
- **Recommendation**: If/when integrating wip_quicktraderank.txt, implement this effect or remove the invocation

### Class 2: Undefined Scripted Triggers

**Status**: ✅ **NONE FOUND**  
All mod-prefixed trigger invocations resolve to definitions in common/scripted_triggers/*.txt.

Note: Several triggers are invoked without the `_trigger` suffix (e.g., `QING_dynasty_has_crownprince = yes` in trigger context), which is valid Clausewitz syntax — the suffix is conventional but optional.

### Class 3: Undefined Script Values

**Status**: ⚠️ **INCONCLUSIVE**  
Script value invocations are difficult to distinguish from variable reads (`value = SVALUE` vs `value = var:VARNAME`) without full AST parsing. Spot checks of candidates (e.g., `COTTAGEIND_raw_iron`, `DIPLOMACY_power_base_cached`, `EDU_hist_literacy_frac_t1`) all resolved to variable names, not script_values.

**Recommendation**: If load-time errors appear mentioning "unknown script value", revisit this class with a refined extraction pattern.

### Class 4: Undefined Modifiers

**Status**: ✅ **NONE FOUND**  
All statically-named mod modifier invocations (add_country_modifier/add_character_modifier with `name = X`) resolve to definitions in common/modifiers/*.txt.

Candidates like `qing_advisor_`, `qing_ethnic_stance_`, `qing_legation_`, `qing_office_`, `qing_rebel_` are **dynamic modifier names** constructed via parameter substitution (e.g., `qing_advisor_$field$_active` in se_QING_ADVISORS.txt:92). These expand at runtime to concrete names (qing_advisor_military_active, qing_advisor_trade_active, etc.), all of which are properly defined.

### Class 5: Undefined Events

**Status**: ✅ **NONE FOUND**  
All mod-prefixed event trigger invocations (trigger_event with `id = X.N`) resolve to event definitions in events/*.txt.

Checked namespaces: qing_*, marriage_*, diplomacy_*, mex_*, usa_*, jpn_*, imp19c_*. Sample: 248 event definitions, 245 invocations, 0 dangling.

### Class 6: Undefined On-Actions

**Status**: ✅ **NONE FOUND**  
Spot-checked on_action invocations; all resolve to vanilla or mod-defined on_actions in common/on_action/*.txt.

### Class 7: Missing Localization Keys

**Status**: ⚠️ **SPOT-CHECK ONLY**  
A comprehensive loc-key audit would require checking ~2,400 mod loc keys against all event titles/descs/options, GUI text fields, modifier/opinion names, etc.

**Spot-checked**: qing_embassy.* event keys (6 events × ~4-6 keys each) — ✅ all present in qing_embassy_l_english.yml.

**Method for future full audit**: Extract all `custom_tooltip =`, `text =`, `desc =` from events/GUIs; extract implicit event loc keys (`namespace.N.t`, `.desc`, `.option_key`); diff against defined keys in localization/english/*.yml.

**Recommendation**: Run game with `-debug_mode` and check error.log for "Unknown localization key" warnings after exercising mod features.


---

## DEFINED-BUT-UNUSED (Class 8 — Lower Priority, Dead Code)

**Methodology caveat**: Effect invocations can take the form `NAME = yes` OR `NAME = { params }`. My initial scan for unused effects checked only `= yes` patterns and missed parametric invocations. A comprehensive dead-code audit would require checking ALL invocation forms.

**Sample findings** (verified as truly unused):

The following are defined in wip_quicktraderank.txt but never invoked (WIP scaffolding):
- `TRADE_setup_all_TZ_travel_time_records` — defined but never called
- `TRADE_setup_TZ_connection_time_records` — marked OBSOLETE in comments

**Recommendation**: A full dead-code audit (Class 8) is **deferred** as lower-priority. It would require:
1. Extracting ALL effect invocation patterns (both `= yes` and `= { ... }`)
2. Cross-referencing against definitions
3. Manual verification of each candidate (some "unused" code may be intended for future features or triggered by player actions not yet tested)

**Known WIP files** (likely to contain unused scaffolding):
- common/scripted_effects/wip_quicktraderank.txt


---

## SUMMARY

### Confirmed Defects by Class

| Class | Type | Count | Severity |
|-------|------|-------|----------|
| 1 | Called-but-undefined scripted effects | **2** | 1 HIGH, 1 NEGLIGIBLE |
| 2 | Undefined scripted triggers | 0 | — |
| 3 | Undefined script values | Inconclusive | — |
| 4 | Undefined modifiers | 0 | — |
| 5 | Undefined events | 0 | — |
| 6 | Undefined on-actions | 0 | — |
| 7 | Missing localization keys | Spot-check only | — |
| 8 | Defined-but-unused (dead code) | Not exhaustively checked | Low priority |

### Top Priority Findings

**1. TRADE_update_all_TZ_local_prices (Class 1.1) — CRITICAL**
- **File**: common/scripted_effects/se_TRADE.txt:3716
- **Impact**: Silently no-ops every quarterly trade update; trade-zone local prices never update after game start
- **Fix**: Either restore the commented-out definition (lines 3134-3140) or remove the invocation

**2. TRADE_setup_TZ_travel_time_records (Class 1.2) — LOW**
- **File**: common/scripted_effects/wip_quicktraderank.txt:57
- **Impact**: WIP code, not invoked in live game
- **Fix**: Implement when/if integrating wip_quicktraderank.txt

### Overall Assessment

**Engine integrity**: ✅ **GOOD**  
The mod's core scripted systems (effects, triggers, modifiers, events) are well-connected. Of 683 mod-defined scripted effects and 23 mod-defined triggers checked, only **1 high-impact dangling reference** was found (TRADE_update_all_TZ_local_prices).

**Defect count**: **2 confirmed dangling references**, 1 critical.

**Recommendations**:
1. **Fix TRADE_update_all_TZ_local_prices immediately** (Class 1.1) — this affects the live quarterly trade economy
2. Spot-check Class 7 (loc keys) by running the game with `-debug_mode` and reviewing error.log after exercising major features (Qing missions, embassies, marriage diplomacy)
3. Defer full Class 8 (dead code) audit until after fixing active defects

---

## Audit Metadata

- **Branch**: 1763_bookmark
- **Commit**: (head at time of audit)
- **Files scanned**: 
  - 236 files containing mod-prefixed code
  - 683 mod scripted effects
  - 23 mod scripted triggers
  - 1,437 mod script values
  - 331 mod modifiers
  - 248 mod events
  - 2,368 mod localization keys
- **Method**: grep-based extraction + manual verification of candidates
- **Duration**: ~1 hour
- **Auditor**: Claude (Sonnet 4.5)

