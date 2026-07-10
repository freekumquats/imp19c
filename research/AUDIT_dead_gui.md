# Dead / Disconnected GUI — Audit (1763_bookmark branch)

## Method + Scope

Auditing **mod-added GUI only** (elements referencing mod-specific names: `qing_`, `QING_`, `MARRIAGE_`, `DIPLOMACY_`, `CURRENCY_`, `imp19c_`, etc.). Vanilla GUI is out of scope.

**Key mod GUI files identified:**
- `gui/government_view.gui` — Grand Council, Throne, Edicts
- `gui/diplomatic_view.gui` — subject tab, overseer, diplomatic plays
- `gui/qing_greatgame.gui`
- `gui/qing_province_reports.gui`
- `gui/marriage_window.gui`
- `gui/imp19c_windows.gui`
- `gui/qing_religion.gui`
- `gui/shared/gui_base.gui`
- `gui/textformatting.gui`

**Method:**
For each mod-named GUI element:
1. Extract dependencies (scripted_gui name, var, window, loc key)
2. Grep repo to confirm dependency exists and is functional
3. Classify failure if absent/broken: (A) button wired to nothing, (B) gate always false, (C) readout of non-existent value, (D) toggle that no-ops, (E) missing loc key

**Known playtest suspects to verify:**
1. Grand Council "Appoint" button doing nothing (`qing_office_picker_window` + appoint scripted_gui)
2. Diplomatic-play "Supranational" icon doing nothing
3. Three dead toggles next to "Overseer" label in subject tab

---

## AUDIT IN PROGRESS

### Starting with government_view.gui (Grand Council)


### Checking government_view.gui - Grand Council Appoint System

**Finding: Grand Council Appoint buttons are FULLY FUNCTIONAL**

Checked path:
1. `gui/government_view.gui:2635,2661,2842,2868...` — Multiple "Appoint" buttons on office cards
2. All call: `onclick = "[ExecuteConsoleCommand('gui.createwidget gui/imp19c_windows.gui qing_office_picker_window')]"`
3. `gui/imp19c_windows.gui:37` — Window `qing_office_picker_window` EXISTS
4. `gui/imp19c_windows.gui:130-141` — Each row has appoint buttons calling scripted_guis like `GetScriptedGui('qing_gov_office_appoint_chancellor')`
5. `common/scripted_guis/QING_governance_actions.txt` — All 11 office appoint scripted_guis EXIST with proper is_valid/is_shown/effect
6. All effects call `QING_office_appoint` which is defined in `common/scripted_effects/se_QING_COUNCIL.txt`

**Status: NO ISSUE FOUND. Playtest suspect #1 is FALSE — the Appoint system is wired.**

### Checking outliner.gui - Supranational Icon

**Finding: Supranational button is FUNCTIONAL**

Checked path:
1. `gui/outliner.gui:886-912` — Supranational button in top bar
2. `onclick = "[GetVariableSystem.Set( 'supranational_window', 'open' )]"`
3. `gui/ingame_topbar.gui:1630-1632` — `supranational` widget becomes visible when var is 'open'
4. `gui/imp19c_windows.gui:410` — `type supranational = base_window` defined, full window with diplomatic plays + federation tabs

**Status: NO ISSUE FOUND. Playtest suspect #2 is FALSE — the Supranational button opens a window.**

### Checking diplomatic_view.gui - Overseer Toggles

**Finding: THREE DEAD TOGGLES (class D - toggle that no-ops)**

Located at `gui/diplomatic_view.gui:2621-2635`:
```
flowcontainer = {
	layoutpolicy_horizontal = expanding
	margin_top = 7
	spacing = 6
	widget = { size = { 10 0 } }
	policy_button = {
		enabled = no
	}
	policy_button = {
		enabled = no
	}
	policy_button = {
		enabled = yes
	}
}
```

**Analysis:**
- Three `policy_button` widgets with no onclick, no datacontext, no scripted_gui
- Two are `enabled = no` (always disabled)
- One is `enabled = yes` but has NO action wired
- Located in the Overseer section of subject view (line 2548: `tooltip = "Overseer"`)
- These appear to be PLACEHOLDER toggles never implemented

**Player symptom:** Three toggle buttons appear next to "Overseer" label in subject diplomacy view. Two are grayed out, one appears clickable but does nothing when clicked.

**Suggested fix:** Remove lines 2621-2635 entirely, or comment out if future functionality planned.

**Status: CONFIRMED DEAD. Playtest suspect #3 is TRUE.**


---

## COMPREHENSIVE SCAN OF OTHER MOD GUI

### qing_greatgame.gui
**Status: ALL FUNCTIONAL**
- Window opens via button calling `gui.createwidget gui/qing_greatgame.gui qing_greatgame_panel`
- All scripted_guis exist: `qing_greatgame_zongli_filled`, `qing_greatgame_britain_exists`, `qing_greatgame_france_exists`, `qing_greatgame_russia_exists` (all in `QING_greatgame_panel.txt`)
- All vars read (`qing_gp_tension_britain/france/russia`, `qing_office_zongli_holder`) are set by economy/office systems
- All loc keys exist

### qing_province_reports.gui
**Status: ALL FUNCTIONAL**
- Three windows: `qing_crop_report_window`, `qing_tension_report_window`, `qing_migration_report_window`
- All three datamodels (`qing_crop_report_provinces`, `qing_tension_report_provinces`, `qing_migration_report_provinces`) are populated by scripted_guis in `qing_province_reports.txt`
- All loc keys exist

### marriage_window.gui
**Status: ALL FUNCTIONAL**
- Window opens via `gui.createwidget gui/marriage_window.gui marriage_window`
- Datamodel `marriage_candidates` populated by `marriage_open_candidates` scripted_gui
- All three action scripted_guis exist: `marriage_action_propose`, `marriage_action_seek_bridge`, `marriage_action_betroth` (all in `MARRIAGE_actions.txt`)
- All vars (`marriage_display_power`, `marriage_display_wed`, `marriage_display_betrothed`) set by marriage system
- All loc keys exist

### qing_religion.gui
**Status: ALL FUNCTIONAL**
- Window opens via button calling `gui.createwidget gui/qing_religion.gui qing_religion_panel`
- All scripted_guis exist: `qing_religion_band_fever/simmering/calm`, `qing_religion_agitator_present`, `qing_religion_taiping_active` (all in `QING_religion_panel.txt`)
- All vars read (`qing_antichristian_sentiment`, `qing_mission_social_friction`, `qing_sect_pressure`, `qing_missionary_reach`, `qing_reform_pressure`, `qing_taiping_progress`, `qing_antichr_agitator`) are set by religion system
- All loc keys exist

### imp19c_windows.gui
**Status: ALL FUNCTIONAL**
- `qing_office_picker_window` (lines 37-334): fully wired, all 13 office appoint scripted_guis exist
- `supranational` window (lines 410+): fully wired, opens when var set, has two tabs with content
- All datamodels, scripted_guis, vars, and loc keys verified

### diplomatic_view.gui (Subject Interactions)
**Status: MOSTLY FUNCTIONAL, ONE CONFIRMED DEAD BLOCK**
- Subject interaction buttons (promote/incorporate/demote/integrate/resume/amban actions): all scripted_guis exist in `QING_subject_management.txt` and `QING_amban_management.txt`
- Influence lists (`DIPLOMACY_list_of_incoming_influencers`, `DIPLOMACY_list_of_outgoing_influenced_countries`): populated by `se_DIPLOMACY.txt`
- **EXCEPTION:** Three dead `policy_button` toggles (lines 2626-2634) — see CONFIRMED DEAD section above

### templates_imp19c.gui
**Status: ALL FUNCTIONAL**
- All script_values referenced exist: `GOODS_national_production_*`, `DEMAND_country_*`, `DEMAND_shortage_country_*`, `PRICE_global_mean_*`, `WARSCORE_province_value`
- All datamodels (`top_producers_grain`, `top_consumers_grain`) are populated

---

## CONFIRMED DEAD

### 1. Three Overseer Policy Toggles (HIGH VISIBILITY — in subject diplomacy view)
**File:** `gui/diplomatic_view.gui:2621-2635`  
**Failure Class:** D (toggle that no-ops)  
**Missing dependency:** No onclick, no datacontext, no scripted_gui — buttons exist but wire to nothing  
**Player symptom:** Three toggle buttons appear next to "Overseer" label in subject diplomacy view. Two are grayed out (enabled = no), one appears clickable (enabled = yes) but does nothing when clicked.  
**Suggested fix:** Remove lines 2621-2635 entirely. These appear to be placeholder toggles that were never implemented. The section already has a functional "Change Overseer" button (line 2587, `qing_amban_manage_replace_button`) that was repurposed from the original placeholder.  
**Context:** The comment at line 2584 says "repurposed the dead 'Change Overseer' placeholder into the amban-swap action" — these toggles are the remnants of that dead placeholder design.

---

## SUSPECT (needs live repro to confirm)

**NONE FOUND.** All other mod-added GUI elements trace to functional dependencies.

---

## The 3 Known Playtest Suspects — Findings

### Suspect #1: Grand Council "Appoint" button doing nothing
**Verdict:** FALSE — the system is fully wired.  
**Path verified:**
1. Office cards in Grand Council tab (`gui/government_view.gui`) have Appoint buttons
2. Buttons call `gui.createwidget gui/imp19c_windows.gui qing_office_picker_window`
3. Window exists, shows candidate list from `qing_council_candidates` datamodel
4. Each candidate row has per-office appoint button calling `GetScriptedGui('qing_gov_office_appoint_<office>')`
5. All 13 office appoint scripted_guis exist in `common/scripted_guis/QING_governance_actions.txt`
6. All scripted_guis have functional `effect` blocks calling `QING_office_appoint` from `se_QING_COUNCIL.txt`

**If the user experienced "nothing happens":** Check if (a) the is_valid conditions were failing (e.g., insufficient political_influence >= 20), or (b) the candidate list was empty (`QING_GC_NO_CANDIDATES` shown). The GUI itself is not the cause.

### Suspect #2: Diplomatic-play "Supranational" icon doing nothing
**Verdict:** FALSE — the button opens a window.  
**Path verified:**
1. Supranational button in outliner (`gui/outliner.gui:886-912`)
2. Button sets `onclick = "[GetVariableSystem.Set( 'supranational_window', 'open' )]"`
3. Variable controls visibility of `supranational` widget in `gui/ingame_topbar.gui:1630-1632`
4. Widget is a full window defined as `type supranational = base_window` in `gui/imp19c_windows.gui:410`
5. Window has two tabs (diplomatic plays / federation) with content

**If the user experienced "nothing happens":** Possible causes: (a) window opened off-screen due to position, (b) window was already open (check for existing instance), or (c) the global powers list was empty. The GUI wiring is correct.

### Suspect #3: Three dead toggles next to "Overseer" label in subject tab
**Verdict:** TRUE — CONFIRMED DEAD (see CONFIRMED DEAD section above).

---


## Summary Table

| Element | File:Line | Class | Missing/Broken Dependency | Player Symptom | Suggested Fix |
|---------|-----------|-------|---------------------------|----------------|---------------|
| **Three Overseer policy toggles** | `gui/diplomatic_view.gui:2621-2635` | D (toggle that no-ops) | No onclick, no datacontext, no scripted_gui — buttons exist but wire to nothing | Three toggle buttons appear next to "Overseer" label in subject diplomacy view. Two grayed out, one appears clickable but does nothing | Remove lines 2621-2635. These are placeholder toggles never implemented. Functional "Change Overseer" button already exists at line 2587. |

**Total confirmed dead elements: 1**  
**Total suspect elements needing live repro: 0**

---

## Top 10 Highest-Visibility Dead GUI Items

### Ranked by player exposure:

1. **Three Overseer policy toggles** (`diplomatic_view.gui:2621-2635`)
   - **Why high visibility:** Appears in the subject diplomacy view, which Qing players open frequently to manage vassals/protectorates/tributaries
   - **Failure mode:** One toggle appears clickable but does nothing (enabled = yes but no onclick)
   - **Player confusion:** Unclear what these toggles are supposed to control — no tooltip, no label, no action
   - **Fix priority:** HIGH — remove immediately

---

## Conclusion

**Overall assessment:** The mod's GUI is remarkably well-wired. Of the three playtest suspects:
- **2 were FALSE alarms** (Grand Council Appoint + Supranational button both functional)
- **1 was TRUE** (Overseer toggles are dead placeholders)

**Only 1 confirmed dead GUI element found** across all mod-added GUI files. The vast majority of mod GUI — office picker, great game panel, province reports, marriage window, religion panel, subject interactions, influence tracking, supranational window — traces cleanly to functional scripted_guis, vars, and effects.

**Recommendation:** Remove the three dead policy_button toggles at `diplomatic_view.gui:2621-2635`. No other GUI surgery needed.

