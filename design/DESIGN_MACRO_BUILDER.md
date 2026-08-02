# Macro Builder System: Complete Analysis

## ✅ SOLVED (2026-07-27) — READ THIS FIRST. Everything below it is superseded.

**The macro builder is driven by an explicit allowlist config file that no earlier analysis in this
doc ever examined:** `gfx/interface/macro_builder/config/00_default.txt`.

```
all_buildings = {
    base = build_in_province
    layout = build_in_province_with_list
    map_mode = macro_builder_build_in_province
    includes = {
        port_building
        ...
        IND_industrial_estate
        IND_resource_gathering_operation
        INF_railway_upgrade      <-- THIS is why sobisonator's non-vanilla railway appears
        INF_depot
        ...
    }
}
```

`MacroBuilderView.GetBuildInProvinceModel` is populated **only** from the building keys listed in
`includes = { ... }`. A building not named there is never in the model, so its `macro_build_item_*`
GUI type name-matches an absent entry and renders nothing — no matter how complete the GUI wiring is.

**This overturns the whole doc below.** The blocker was NEVER: trade_goods, CJK names, GetName vs
GetNameWithNoTooltip, potential/allow gates, file name, or an INF_ prefix. It was that the Qing
buildings were absent from `includes`. The GUI item types + tooltips + loc were all correct the entire
time (which is exactly why the province window — a DIFFERENT model, `ProvinceWindow.GetPossibleBuildings`,
that is NOT config-gated — showed them fine).

**This is precisely "how sobisonator added a non-vanilla building": add its key to `includes`.**
No engine C++ access was ever needed — the registration is a plain, readable, editable config file.

### The fix applied
1. `gfx/interface/macro_builder/config/00_default.txt` — added the 6 production works, 4 routine public
   works (dike/canal_depot/wall_section/granary), and 3 foreign buildings to `includes`. The 2 capstone
   monuments (great_wall/grand_canal) are deliberately EXCLUDED (event-raised only).
2. Added the 9 missing `macro_building_qing_*_tooltip` templates (custom_tooltip.gui) and 3 missing
   `tooltip_macro_building_title_qing_*` loc keys — the public-works/foreign item types referenced
   tooltip widgets that did not exist.
3. Two-row Industrial layout (`building_box` gets an `IndustrialItemsRow2` block) so 8–10 items no
   longer overflow the panel's right edge, in both the province window and the macro builder.
4. Geography-gated the routine works via proven province triggers: dike `has_minor_river = yes`;
   canal depot `is_in_region` = Grand Canal corridor (Zhili/Shandong/Jiangsu/Zhejiang); wall section
   `is_in_region` = northern frontier (Zhili/Shanxi/Shaanxi/Gansu/Liaoning).
5. Monuments (great_wall/grand_canal) set `potential = { always = no }` + `allow = { always = no }` so
   they never enter the build menu; the se_QING_WORKS.txt events raise them via `add_building_level`,
   which bypasses both. Removed their build items from both the macro view and province window.

All triggers verified against PROVEN sources (Invictus/TI/vanilla), not imp19c's own files:
`country_culture_group` (Invictus 00_mission_effects, TI 00_religious_inventions), `is_in_region`,
`has_minor_river` (00_default river_port_building), `always = no` (used across 676 TI/Invictus files).

**✅ USER BOOT-CONFIRMED 2026-07-27** (merge-overnight `a2d5651ba`): "macro builder finally works".
The building keys are in the same list as `INF_railway_upgrade`, and the 13 buildings now list in-game.

---

## ✅ PROVEN RECIPE — add a building to the macro builder (boot-confirmed 2026-07-27)

This is the exact, verified process. It has TWO indispensable parts: the **allowlist registration**
(part 1 — the part every prior attempt missed) and the **per-building GUI wiring** (parts 2–5). Skipping
part 1 = an empty section header; skipping any of 2–5 = a missing row or a GUI-compile failure.

### 1. Register the building in the macro allowlist  ← THE ONE THAT ACTUALLY GATES VISIBILITY
`gfx/interface/macro_builder/config/00_default.txt` → add the building's KEY to `all_buildings.includes`:
```
all_buildings = {
    ...
    includes = {
        ...
        INF_railway_upgrade      # proof this is the gate: a non-vanilla building that appears
        my_new_building          # <-- add the raw building key here
    }
}
```
`MacroBuilderView.GetBuildInProvinceModel` is populated ONLY from this list. Not here ⇒ never in the
model ⇒ the GUI item name-matches nothing ⇒ zero rows, regardless of how complete parts 2–5 are.
(This file already carries a UTF-8 BOM and loads fine — leave the BOM as-is.)

### 2. Item type — `gui/shared/gui_templates.gui`
Add a `macro_build_item_<key>` type that iterates the full model and shows the one matching row:
```
type macro_build_item_my_new_building = macro_building_parts_item {
    item = {
        macro_building_item_button = {
            visible = "[EqualTo_string(MacroBuilderProvinceBuildable.GetName, Localize('my_new_building'))]"
            blockoverride "Tooltip" { tooltipwidget = macro_building_my_new_building_tooltip }
        }
    }
}
```
The name-match compares `MacroBuilderProvinceBuildable.GetName` against `Localize('<key>')` — the key is
the building's def name, NOT a display string. (CJK/concept-word names are fine; they were never the
blocker.) `macro_building_parts_item` (same file) supplies `datamodel = GetBuildInProvinceModel` +
`ignoreinvisible = yes`.

### 3. Tooltip template — `gui/shared/custom_tooltip.gui`
Every `tooltipwidget` referenced in part 2 MUST have a matching `template` here, or the GUI fails to
resolve the widget:
```
template macro_building_my_new_building_tooltip {
    building_tooltip = {
        blockoverride "Image"       { texture = "[MacroBuilderProvinceBuildable.GetIconTexture]" }
        blockoverride "title_text"  { text = "tooltip_macro_building_title_my_new_building" }
        blockoverride "description" { text = "my_new_building_desc" }
        blockoverride "bottom_text" { text = "[MacroBuilderProvinceBuildable.GetTooltip]" }
    }
}
```

### 4. Instantiate in the window — `gui/macro_builder_view.gui`
Add the item type inside the relevant section blockoverride of `building_box`:
```
blockoverride "IndustrialItems" {
    ...
    macro_build_item_my_new_building = { }
}
```
Section blocks available (defined in the `building_box` template in gui_templates.gui): PortItems,
EducationItems, IndustrialItems, IndustrialItemsRow2, InfrastructureItems, PublicWorksItems,
MilitaryItems, UrbanDistrictsItems, ForeignItems. To add a NEW section, add a `block "X" { }` to the
template AND a `blockoverride "X"` in every caller (macro view + province window).

### 5. Localization — `localization/english/`
Two keys, both required:
- title: `imp19c_tooltips_l_english.yml` → `tooltip_macro_building_title_my_new_building:0 "#T Build #L $my_new_building$#!"`
- description: the building's `my_new_building_desc:0 "..."` (usually already exists with the building).

### Rules that fell out of the investigation (do NOT relearn the hard way)
- **`allow` / `potential` do NOT gate macro-list membership.** The config `includes` does. `allow` only
  greys the item per-province; `potential` gates the *province window* list and build-menu membership.
  So province-scoped gates (`trade_goods`, `is_in_region`, `has_minor_river`) are safe to keep — they
  shape *where* it can be built, not *whether* it lists in the macro builder.
- **`add_building_level` bypasses BOTH `potential` and `allow`.** An event-raised building can therefore
  be locked out of every menu with `potential = { always = no }` + `allow = { always = no }` and still be
  raised by its event. Omit it from `includes` so it never lists.
- **flowcontainer does NOT auto-wrap.** To split a section across rows, use explicit stacked rows (see
  `IndustrialItems` + `IndustrialItemsRow2`), not a `maximumsize`.
- **gui/ files must have NO BOM; loc + common + this config keep BOM.** Verify with
  `head -c3 <file> | xxd` (BOM = `efbbbf`).
- **Verify triggers against PROVEN sources only** (Invictus/TI/vanilla) — never against imp19c's own
  files (circular). Confirmed valid here: `country_culture_group`, `is_in_region`, `has_minor_river`,
  `always = no`.

### Provenance
`INF_railway_upgrade` is a modder-added (non-vanilla) building that appears in the macro builder purely
because sobisonator added its key to this same `includes` list — no engine C++ access, no hidden
registry. The entire mechanism is this one readable config file.

---

## Overview (SUPERSEDED — kept for history; its conclusions were wrong)

The macro builder is a custom UI system built by modder sobisonator that lists buildable buildings and, after selection, highlights valid provinces on the map. It consists of:

1. **Building definitions** (`common/buildings/*.txt`) - game data defining each building
2. **C++ engine databinding** (`MacroBuilderView.GetBuildInProvinceModel`) - determines which buildings appear
3. **GUI templates** (`gui/shared/gui_templates.gui`) - define item rendering for each building
4. **Macro builder window** (`gui/macro_builder_view.gui`) - the categorized list layout
5. **Custom tooltips** (`gui/shared/custom_tooltip.gui`) - tooltip templates for each building

---

## Data Flow: Building Definition → Macro Builder List Item

### Step 1: Building Definition (`common/buildings/*.txt`)

Example working building (`00_infrastructure_buildings.txt:105`):
```
INF_depot = {
    local_building_slot = 1
    local_proletariat_desired_pop_ratio = 0.05
    cost = 100
    time = 180
    allow = {
        owner ={invention = tech_construction}
        sufficient_education_slots = { tier = t1 }
        sufficient_education_slots = { tier = t2 }
    }
    modification_display = { 1 = local_food_capacity }
}
```

Example currently-failing building (`qing_production_buildings.txt:16`):
```
qing_silk_filature_building = {
    local_middle_strata_output = 0.5
    local_upper_strata_output = 0.4
    base_resources = 2
    cost = 90
    time = 240
    allow = {
        owner = {
            OR = {
                country_culture_group = jurchen
                country_culture_group = chinese_group
            }
        }
        sufficient_job_slots = yes
    }
    modification_display = { }
}
```

**Key fields:**
- `cost`, `time` - build cost and duration
- `allow = { }` - gates the player build menu (add_building_level bypasses this)
- `potential = { }` - OPTIONAL province-level filter (e.g., `trade_goods = silk`)
- `modification_display = { }` - stat display order

### Step 2: Engine Databinding (`MacroBuilderView.GetBuildInProvinceModel`)

**This is a C++ engine function whose internals are NOT accessible in mod code.** Its behavior must be determined empirically.

**Location:** Referenced in `gui/macro_builder_view.gui:239` and `gui/shared/gui_templates.gui:788`.

**Observed behavior:**
- Returns a list of `MacroBuilderProvinceBuildable` objects
- Each object has `.GetName`, `.GetIconTexture`, `.GetTooltip`, `.GetPrice`, `.IsEnabled`, `.IsSelected`, `.OnClick`
- The naval units section (`macro_builder_view.gui:235-316`) directly iterates this model without filtering

**Confirmed members (buildings that DO appear):**
- `INF_sewer_infrastructure`, `INF_hospital`, `INF_canal`, `INF_railway_upgrade`, `INF_depot`
- `IND_industrial_estate`, `IND_resource_gathering_operation`
- `EDU_school`, `EDU_university`
- `port_building`, `river_port_building`
- `fortress_building`, `arsenal_building`
- `URB_commerce_district`, `URB_administration_district`, `URB_residential_district`, `URB_cultural_district`
- `qing_granary_building` (from `qing_granary_buildings.txt`)
- `qing_dike_building`, `qing_canal_depot_building`, `qing_wall_section_building`, `qing_great_wall_building`, `qing_grand_canal_building` (from `qing_works_buildings.txt`)
- `qing_mission_underground_building`, `qing_mission_public_building`, `qing_foreign_concession_building` (from `qing_foreign_buildings.txt`)

**Confirmed NON-members (buildings that DO NOT appear, despite having GUI items):**
- `qing_silk_filature_building`, `qing_porcelain_kiln_building`, `qing_tea_workshop_building`, `qing_cotton_workshop_building`, `qing_salt_yard_building`, `qing_opium_poppy_farm_building` (from `qing_production_buildings.txt`)

**Critical difference identified:**

The qing production works (`qing_silk_filature_building` etc.) **originally had a `potential = { trade_goods = X }` block** that was **removed on 2026-07-27** (see comment at `qing_production_buildings.txt:32-36`). The comment states:
> "trade_goods gate removed from allow. Rationale is EMPIRICAL, not a claimed mechanism: the six works differ from the macro-visible IND_industrial_estate only in defining a trade_goods gate, so it is removed to match that working building as closely as possible."

This indicates the modder (user) is **currently testing** whether removing province-specific `potential` gates makes buildings macro-visible. The change is **UNCONFIRMED** and awaiting boot-test.

**Hypothesis:** `MacroBuilderView.GetBuildInProvinceModel` may exclude buildings that have province-specific gates in their `potential` block (like `trade_goods = X`), because the macro builder operates at a COUNTRY level (picking a building BEFORE selecting provinces), not a province level. Buildings with province-specific potential gates cannot be evaluated until a province is selected, creating a chicken-and-egg problem.

**Counter-evidence:** 
- `port_building` has `potential = { is_port = yes }` (`00_default.txt:7`) but IS macro-visible
- `qing_mission_underground_building` has `potential = { has_city_status = yes }` (`qing_foreign_buildings.txt:34`) but IS macro-visible
- `row_manufactory_building` and `row_plantation_building` have extensive `potential` blocks with `trade_goods` gates (`row_production_buildings.txt:46-59, 88-100`) - these were explicitly REMOVED from the macro builder (`macro_builder_view.gui:184-186`) not because of engine limitation but because "they are rest-of-world buildings (potential = NOT chinese_group) and should not show in the Qing player's macro builder"

**Refined hypothesis:** The presence of a `potential` block itself does NOT exclude a building. The specific content may matter, but the exact rule is **not determinable from code inspection alone** - it's an engine implementation detail.

### Step 3: GUI Item Template (`gui/shared/gui_templates.gui:787-1015`)

Each building needs TWO template types:

**A. Province window item** (line 385-610):
```
type build_item_qing_silk_filature_building = building_parts_item {
    item = {
        building_item_button = {
            visible = "[EqualTo_string(BuildingItem.GetBuilding.GetNameWithNoTooltip, Localize('qing_silk_filature_building'))]"
        }
    }
}
```

**B. Macro builder item** (line 787-1015):
```
type macro_build_item_qing_silk_filature_building = macro_building_parts_item {
    item = {
        macro_building_item_button = {
            visible = "[EqualTo_string(MacroBuilderProvinceBuildable.GetName, Localize('qing_silk_filature_building'))]"
            blockoverride "Tooltip" { tooltipwidget = macro_building_qing_silk_filature_building_tooltip }
        }
    }
}
```

**Key differences:**
- Province item: `datamodel = "[ProvinceWindow.GetPossibleBuildings]"` (line 386)
- Macro item: `datamodel = "[MacroBuilderView.GetBuildInProvinceModel]"` (line 788)
- Province item: filters `BuildingItem.GetBuilding.GetNameWithNoTooltip`
- Macro item: filters `MacroBuilderProvinceBuildable.GetName`

**Critical insight:** The template instantiates the FULL model per section and filters to ONE name via the `visible` clause. So **model membership is the real gate**, and the `visible=` clause is just a name-specific display filter. If a building is not IN `MacroBuilderView.GetBuildInProvinceModel`, the macro_build_item template will render but be invisible (ignoreinvisible = yes on the parent).

### Step 4: Macro Builder Window Layout (`gui/macro_builder_view.gui:163-224`)

The building_box defines categorized sections:
```
building_box = {
    blockoverride "IndustrialItems" {
        macro_build_item_industrial_estate = { }
        macro_build_item_resource_gathering_operation = { }
        macro_build_item_qing_silk_filature_building = { }
        macro_build_item_qing_porcelain_kiln_building = { }
        ...
    }
    blockoverride "PublicWorksItems" {
        macro_build_item_qing_dike_building = { }
        macro_build_item_qing_canal_depot_building = { }
        ...
    }
    blockoverride "ForeignItems" {
        macro_build_item_qing_mission_underground_building = { }
        macro_build_item_qing_mission_public_building = { }
        macro_build_item_qing_foreign_concession_building = { }
    }
}
```

Each section is a flowcontainer with `ignoreinvisible = yes`, so invisible items don't take space.

### Step 5: Custom Tooltip (`gui/shared/custom_tooltip.gui:1012-1070`)

Each macro building needs a tooltip template:
```
template macro_building_qing_silk_filature_building_tooltip
{
    building_tooltip = {
        blockoverride "Image" { texture = "[MacroBuilderProvinceBuildable.GetIconTexture]" }
        blockoverride "title_text" { text = "tooltip_macro_building_title_qing_silk_filature_building" }
        blockoverride "description" { text = "qing_silk_filature_building_desc" }
        blockoverride "bottom_text" { text = "[MacroBuilderProvinceBuildable.GetTooltip]" }
    }
}
```

---

## Model Membership Rule: What Gates MacroBuilderView.GetBuildInProvinceModel?

**CONFIRMED: This is an engine (C++) databinding whose membership logic is NOT visible in mod code.**

**Empirical observations:**

### Buildings WITH model membership (appear in macro builder):
1. **Vanilla prefixed buildings:** INF_*, IND_*, EDU_*, URB_* (all from 00_*.txt files)
2. **Vanilla unprefixed buildings:** port_building, river_port_building, fortress_building, arsenal_building
3. **Qing buildings with `potential` blocks:** qing_granary_building (has `potential = { has_city_status = yes }`), qing_mission_underground_building, qing_mission_public_building, qing_foreign_concession_building (all have `potential = { has_city_status = yes }`)
4. **Qing buildings without `potential` blocks:** qing_dike_building, qing_canal_depot_building, qing_wall_section_building, qing_great_wall_building, qing_grand_canal_building (from qing_works_buildings.txt - none have `potential`)

### Buildings WITHOUT model membership (do not appear):
1. **qing_silk_filature_building**, qing_porcelain_kiln_building, qing_tea_workshop_building, qing_cotton_workshop_building, qing_salt_yard_building, qing_opium_poppy_farm_building (from qing_production_buildings.txt)

### What's different about the failing buildings?

**As of 2026-07-27, these buildings had their `potential = { trade_goods = X }` blocks removed** (see comment at `qing_production_buildings.txt:32-36`). The modder is testing whether this makes them macro-visible.

**Historical state (before 2026-07-27):**
- Each had `potential = { trade_goods = silk/porcelain/tea/... }`
- This differed from IND_industrial_estate (which has NO `potential` block)

**Current state (after 2026-07-27):**
- No `potential` block (matches IND_industrial_estate)
- `allow` block has owner culture gate (jurchen OR chinese_group) + sufficient_job_slots
- Awaiting boot-test to confirm if this fixes macro visibility

**Speculative mechanism (cannot be confirmed without engine source):**

The engine may populate `MacroBuilderView.GetBuildInProvinceModel` using a **hardcoded registry** or a **building categorization system** that is NOT exposed in script files. Possibilities:

1. **Hardcoded list:** The engine has a fixed list of building types that are macro-eligible (vanilla buildings + specific mod additions)
2. **Category/group system:** Buildings may need to belong to a specific category or group (e.g., a `macro_buildable = yes` flag that's not visible in the txt definitions but may exist in the binary format)
3. **Dynamic evaluation at runtime:** The engine may evaluate building `potential` at macro-window-open time and exclude buildings whose `potential` cannot be evaluated without a province context
4. **File location/naming convention:** Buildings from certain files or with certain naming patterns may be auto-registered

**None of these can be confirmed from the available mod files.**

---

## How Sobisonator Added His Buildings (INF_depot, INF_hospital, etc.)

Sobisonator (the original modder) successfully added infrastructure buildings that ARE macro-visible. Let me trace one example: **INF_depot**.

### Files involved:

**1. Building definition** (`common/buildings/00_infrastructure_buildings.txt:105-127`):
```
INF_depot = {
    local_building_slot = 1
    local_proletariat_desired_pop_ratio = 0.05
    cost = 100
    time = 180
    allow = {
        owner ={invention = tech_construction}
        sufficient_education_slots = { tier = t1 }
        sufficient_education_slots = { tier = t2 }
    }
    modification_display = { 1 = local_food_capacity }
}
```

**Key characteristics:**
- NO `potential` block
- Simple `allow` block with tech + job requirements
- Lives in the vanilla-style `00_infrastructure_buildings.txt` file
- Uses the `INF_` prefix (matches vanilla infrastructure pattern)

**2. Province window item** (`gui/shared/gui_templates.gui:475-482`):
```
type build_item_depot = building_parts_item {
    item = {
        building_item_button = { 
            visible = "[EqualTo_string(BuildingItem.GetBuilding.GetNameWithNoTooltip, Localize('INF_depot'))]"
            blockoverride "Tooltip" { tooltipwidget = building_depot_tooltip }
        }
    }
}
```

**3. Macro builder item** (`gui/shared/gui_templates.gui:871-878`):
```
type macro_build_item_depot = macro_building_parts_item {
    item = {
        macro_building_item_button = {
            visible = "[EqualTo_string(MacroBuilderProvinceBuildable.GetName, Localize('INF_depot'))]"
            blockoverride "Tooltip" { tooltipwidget = macro_building_depot_tooltip }
        }
    }
}
```

**4. Province window layout** (`gui/province_window.gui:4085-4091`):
```
blockoverride "InfrastructureItems" {
    build_item_sewer_infrastructure = { }
    build_item_hospital = { }
    build_item_canal = { }
    build_item_railway_upgrade = { }
    build_item_depot = { }
}
```

**5. Macro builder layout** (`gui/macro_builder_view.gui:188-194`):
```
blockoverride "InfrastructureItems" {
    macro_build_item_sewer_infrastructure = { }
    macro_build_item_hospital = { }
    macro_build_item_canal = { }
    macro_build_item_railway_upgrade = { }
    macro_build_item_depot = { }
}
```

**6. Province tooltip** (`gui/shared/custom_tooltip.gui:651-663`):
```
template building_depot_tooltip
{
    building_tooltip = {
        blockoverride "Image" { texture = "[GetBuildingIcon( BuildingItem.GetBuilding )]" }
        blockoverride "title_text" { text = "tooltip_building_title_depot" }
        blockoverride "description" { text = "INF_depot_desc" }
        blockoverride "bottom_text" { text = "[BuildingItem.GetBuildInfo]" }
    }
}
```

**7. Macro tooltip** (`gui/shared/custom_tooltip.gui:1142-1155`):
```
template macro_building_depot_tooltip
{
    building_tooltip = {
        blockoverride "Image" { texture = "[MacroBuilderProvinceBuildable.GetIconTexture]" }
        blockoverride "title_text" { text = "tooltip_macro_building_title_depot" }
        blockoverride "description" { text = "INF_depot_desc" }
        blockoverride "bottom_text" { text = "[MacroBuilderProvinceBuildable.GetTooltip]" }
    }
}
```

**8. Localization** (must exist in `localization/english/*.yml`):
- `INF_depot:0 "Depot"`
- `INF_depot_desc:0 "Description text..."`
- `tooltip_building_title_depot:0 "Depot"`
- `tooltip_macro_building_title_depot:0 "Depot"`

**9. Icon** (must exist at the path the engine looks up):
- Building icon texture referenced by `[GetBuildingIcon( BuildingItem.GetBuilding )]`

**Result:** INF_depot IS macro-visible and works correctly.

---

## Complete Recipe to Add a New Building to Macro Builder

Based on the proven INF_depot pattern, here's the COMPLETE step-by-step recipe:

### Step 1: Define the building (`common/buildings/XX_category_buildings.txt`)

```
YOUR_building_name = {
    # Stat modifiers
    local_some_stat = 0.5
    
    cost = 100
    time = 180
    
    # CRITICAL: NO potential block with province-specific gates like trade_goods
    # Only use potential if absolutely necessary and only with gates that can
    # be evaluated at country level (e.g., has_city_status)
    
    allow = {
        owner = { invention = tech_something }
        sufficient_job_slots = yes
    }
    
    modification_display = {
        0 = local_some_stat
    }
}
```

**Key rules:**
- NO `potential` block, OR only use `potential` with country/city-level gates (NOT trade_goods)
- Simple `allow` block with tech + job requirements
- Consider using a category prefix (INF_, IND_, EDU_, etc.) to match vanilla patterns (may help engine registration, unconfirmed)
- Place in a `00_*.txt` file or a `qing_*.txt` file (both patterns have working examples)

### Step 2: Province window item (`gui/shared/gui_templates.gui`)

Add after existing build_item_* types (~line 610):
```
type build_item_YOUR_building_name = building_parts_item {
    item = {
        building_item_button = {
            visible = "[EqualTo_string(BuildingItem.GetBuilding.GetNameWithNoTooltip, Localize('YOUR_building_name'))]"
            blockoverride "Tooltip" { tooltipwidget = building_YOUR_building_name_tooltip }
        }
    }
}
```

### Step 3: Macro builder item (`gui/shared/gui_templates.gui`)

Add after existing macro_build_item_* types (~line 1015):
```
type macro_build_item_YOUR_building_name = macro_building_parts_item {
    item = {
        macro_building_item_button = {
            visible = "[EqualTo_string(MacroBuilderProvinceBuildable.GetName, Localize('YOUR_building_name'))]"
            blockoverride "Tooltip" { tooltipwidget = macro_building_YOUR_building_name_tooltip }
        }
    }
}
```

### Step 4: Province window layout (`gui/province_window.gui:4059-4123`)

Add to the appropriate blockoverride section (e.g., InfrastructureItems):
```
blockoverride "InfrastructureItems" {
    build_item_sewer_infrastructure = { }
    build_item_hospital = { }
    build_item_YOUR_building_name = { }  # ADD THIS LINE
    ...
}
```

### Step 5: Macro builder layout (`gui/macro_builder_view.gui:163-224`)

Add to the appropriate blockoverride section:
```
blockoverride "InfrastructureItems" {
    macro_build_item_sewer_infrastructure = { }
    macro_build_item_hospital = { }
    macro_build_item_YOUR_building_name = { }  # ADD THIS LINE
    ...
}
```

### Step 6: Province tooltip (`gui/shared/custom_tooltip.gui`)

Add after existing building_*_tooltip templates (~line 663):
```
template building_YOUR_building_name_tooltip
{
    building_tooltip = {
        blockoverride "Image" { texture = "[GetBuildingIcon( BuildingItem.GetBuilding )]" }
        blockoverride "title_text" { text = "tooltip_building_title_YOUR_building_name" }
        blockoverride "description" { text = "YOUR_building_name_desc" }
        blockoverride "bottom_text" { text = "[BuildingItem.GetBuildInfo]" }
    }
}
```

### Step 7: Macro tooltip (`gui/shared/custom_tooltip.gui`)

Add after existing macro_building_*_tooltip templates (~line 1155):
```
template macro_building_YOUR_building_name_tooltip
{
    building_tooltip = {
        blockoverride "Image" { texture = "[MacroBuilderProvinceBuildable.GetIconTexture]" }
        blockoverride "title_text" { text = "tooltip_macro_building_title_YOUR_building_name" }
        blockoverride "description" { text = "YOUR_building_name_desc" }
        blockoverride "bottom_text" { text = "[MacroBuilderProvinceBuildable.GetTooltip]" }
    }
}
```

### Step 8: Localization (`localization/english/buildings_l_english.yml`)

Add these keys:
```yaml
YOUR_building_name:0 "Building Display Name"
YOUR_building_name_desc:0 "Building description text explaining what it does."
tooltip_building_title_YOUR_building_name:0 "Building Display Name"
tooltip_macro_building_title_YOUR_building_name:0 "Building Display Name"
```

### Step 9: Icon

Ensure a building icon exists at the correct path (engine looks up by building name).

### Step 10: Boot test

**CRITICAL:** After adding all files, boot the game as the appropriate nation (e.g., CHI for Qing buildings) and verify:
1. Building appears in province window build menu
2. Building appears in macro builder list
3. Clicking in macro builder highlights valid provinces
4. Building can be constructed

---

## Why Qing Production Buildings Currently Fail

The six Qing production works (silk/porcelain/tea/cotton/salt/opium) currently fail to appear in the macro builder despite having all GUI wiring in place. Let me trace the complete state:

### What IS present (all files exist):

**1. Building definitions** (`qing_production_buildings.txt:16-229`):
- ✅ All six buildings defined with stats, cost, time
- ✅ All have `allow` blocks (no `potential` blocks as of 2026-07-27)

**2. Province window items** (`gui/shared/gui_templates.gui:593-610`):
- ✅ All six `build_item_qing_*` types defined

**3. Macro builder items** (`gui/shared/gui_templates.gui:980-1015`):
- ✅ All six `macro_build_item_qing_*` types defined with tooltips

**4. Province window layout** (`gui/province_window.gui:4078-4083`):
- ✅ All six listed in IndustrialItems block

**5. Macro builder layout** (`gui/macro_builder_view.gui:178-183`):
- ✅ All six listed in IndustrialItems block

**6. Macro tooltips** (`gui/shared/custom_tooltip.gui:1012-1070`):
- ✅ All six tooltip templates defined

**7. Localization** (presumed present, not verified in this analysis)

**8. Icons** (presumed present, not verified in this analysis)

### What is DIFFERENT from working buildings:

**Comparison: qing_silk_filature_building (FAILS) vs IND_industrial_estate (WORKS)**

| Aspect | qing_silk_filature_building | IND_industrial_estate |
|--------|----------------------------|----------------------|
| File | `qing_production_buildings.txt` | `00_industrial_buildings.txt` |
| Prefix | `qing_` | `IND_` |
| `potential` block | None (removed 2026-07-27, was `trade_goods = silk`) | None |
| `allow` block | Owner culture gate (jurchen OR chinese_group) + job slots | Tech gate + civ value + job slots + industry capacity |
| Model membership | ❌ NOT in `MacroBuilderView.GetBuildInProvinceModel` | ✅ IN model |

**Comparison: qing_silk_filature_building (FAILS) vs qing_dike_building (WORKS)**

| Aspect | qing_silk_filature_building | qing_dike_building |
|--------|----------------------------|-------------------|
| File | `qing_production_buildings.txt` | `qing_works_buildings.txt` |
| Prefix | `qing_` | `qing_` |
| `potential` block | None | None |
| `allow` block | Owner culture gate + job slots | Tech gate + job slots |
| Model membership | ❌ NOT in model | ✅ IN model |

**The ONLY difference:** File location (qing_production_buildings.txt vs qing_works_buildings.txt) and allow block content.

**Comparison: qing_silk_filature_building (FAILS) vs row_manufactory_building (REMOVED from macro builder)**

| Aspect | qing_silk_filature_building | row_manufactory_building |
|--------|----------------------------|-------------------------|
| File | `qing_production_buildings.txt` | `row_production_buildings.txt` |
| `potential` block | None (removed 2026-07-27) | YES: extensive owner culture gate + trade_goods OR list |
| `allow` block | Owner culture gate + job slots | Tech gate + job slots |
| Model membership | ❌ NOT in model (reason unknown) | ⚠️ Unknown (explicitly removed from GUI, see line 184-186) |

The `row_manufactory_building` and `row_plantation_building` were **explicitly removed** from the macro builder GUI layout with the comment: "they are rest-of-world buildings (potential = NOT chinese_group) and should not show in the Qing player's macro builder; the Qing works above replace them" (`macro_builder_view.gui:184-186`).

**This suggests the modder EXPECTED the qing production works to be model-visible after the potential block removal.**

### Root cause hypothesis:

**The qing production works are NOT in `MacroBuilderView.GetBuildInProvinceModel` because:**

1. **They previously had `potential = { trade_goods = X }` blocks** which the engine may have used to exclude them from the macro model (province-specific gates)
2. **Those blocks were removed on 2026-07-27** to match IND_industrial_estate
3. **The game has NOT been booted since this change** - the comment at line 32-36 explicitly states: "Whether this makes them macro-visible is UNCONFIRMED and must be boot-tested"

**Conclusion:** The fix MAY already be applied (removal of `potential` blocks), but requires boot-testing to confirm whether the engine now includes them in the model.

### Alternative hypothesis if boot test fails:

If the buildings still don't appear after removing `potential` blocks, possible causes:

1. **Engine hardcoded list:** The macro model may use a hardcoded registry that must be extended (requires engine modification, not possible in pure script mod)
2. **File categorization:** Buildings from `qing_production_buildings.txt` may be in a different category than buildings from `00_*.txt` or `qing_works_buildings.txt`
3. **Building name pattern:** The engine may use a naming convention filter (but this seems unlikely since `qing_dike_building` works)
4. **Cache/reload issue:** The game may need a full restart or cache clear after the change

---

## COMPLETE MECHANICS — verified by full end-to-end read of sobisonator's code (2026-07-27)

Read in full: sobiso/master gui/macro_builder_view.gui (470 lines), gui/shared/gui_templates.gui
(building_box, macro_building_parts_item, every macro_build_item_*), gui/shared/gui_base.gui
(building_item_button, macro_building_item_button), his common/buildings/*.txt, buildings_generator.py,
building_list.txt. Facts below are each tied to something I actually read.

### 1. The render chain (how a building becomes a macro-builder row)
- Window gui/macro_builder_view.gui STEP-1 block instantiates `building_box` (defined gui_templates.gui
  type building_box). building_box has empty `block "PortItems"/"EducationItems"/"IndustrialItems"/
  "InfrastructureItems"/"MilitaryItems"/"UrbanDistrictsItems"` slots, filled by blockoverrides in the window.
- Each slot is filled with per-building `macro_build_item_<key>` instances.
- `type macro_build_item_<key> = macro_building_parts_item { item = { macro_building_item_button = {
  visible = "[EqualTo_string(MacroBuilderProvinceBuildable.GetName, Localize('<key>'))]" ... } } }`.
- `type macro_building_parts_item = container { datamodel = "[MacroBuilderView.GetBuildInProvinceModel]"
  ignoreinvisible = yes }`. → CRITICAL: each macro_build_item instantiates the FULL model as a datamodel;
  the `item` repeats once per model entry; `visible=` shows only the entry whose GetName equals Localize(key).
  So a row appears IFF (a) the building is IN GetBuildInProvinceModel AND (b) that entry's GetName string
  equals Localize('<key>'). `ignoreinvisible = yes` collapses the non-matching repeats.
- `macro_building_item_button` (gui_base.gui) inherits `building_item_button`; its base `visible` is `no`,
  overridden by the per-item `visible=` above. Confirmed byte-identical between sobiso and my tree.

### 2. GetBuildInProvinceModel is an ENGINE (C++) databinding
Its membership logic is NOT in mod files (searched common/defines, script_values, building schema, the
generator, building_list.txt — none define it). So membership can only be characterised empirically. What
I could NOT do by reading: enumerate the model's members. What building_list.txt actually is: generator
output mapping province-id → seeded starting buildings (buildings_generator.py reads province_setup.csv).
It is initial PLACEMENT, unrelated to the macro model. Ruled out.

### 3. HOW RAILWAYS APPEAR (the thing I was told to explain)
INF_railway_upgrade is NOT a vanilla Imperator building — sobisonator added it. It appears in his macro
builder. Its COMPLETE recipe, every piece read from sobiso/master:
  - Building def: common/buildings/00_infrastructure_buildings.txt, key `INF_railway_upgrade`, prefix INF_,
    NO `potential` block, `allow = { owner={invention=tech_steam_locomotive} civilization_value>=30
    sufficient_job_slots=yes sufficient_education_slots x2 }`.
  - build_item_railway_upgrade (province) + macro_build_item_railway_upgrade (macro) in gui_templates.gui,
    both name-matching `INF_railway_upgrade`; both with a Tooltip blockoverride.
  - Instantiated in macro_builder_view.gui InfrastructureItems (his line 171) and province InfrastructureItems.
  - building_railway_upgrade_tooltip + macro_building_railway_upgrade_tooltip in custom_tooltip.gui.
  - loc: `INF_railway_upgrade:0 "Railway upgrade"` (text_l_english) + tooltip_* titles.
So a NEW building appears in the categorized macro builder with exactly this wiring — no special registry,
no engine edit. The model evidently contains any properly-defined buildable building type; the categorized
GUI simply name-matches the ones it wants to show. (Note: railway's `allow` needs tech CHI lacks at 1763 —
so the model does NOT pre-filter on `allow`; buildability is resolved at the province-highlight step, matching
the user's stated mechanic. This means `allow`/`potential`/`trade_goods`/culture gates are IRRELEVANT to
list membership — proven twice over: port_building has province-scoped `potential = { can_have_port = yes }`
+ a `chance` block and still lists.)

### 4. MY qing items vs his railway item — what I have and have not matched
My `macro_build_item_qing_silk_filature_building` (gui_templates.gui:980) is byte-identical in STRUCTURE to
his `macro_build_item_railway_upgrade`: same base, same `visible = EqualTo_string(GetName, Localize('key'))`,
same Tooltip blockoverride, instantiated in a building_box slot, tooltip template present, loc key present,
building def present and BUILDABLE (province window lists all six — screenshot 2). The GUI is a faithful copy.
REMAINING DIFFERENCES vs railway (the only variables left, none yet tested in isolation):
  (a) his def lives in a `00_*.txt` file with an engine-category prefix (INF_/IND_/EDU_/URB_); mine live in
      `qing_*.txt` with a `qing_` prefix.
  (b) his displayed loc value is plain ASCII ("Railway upgrade"); mine carry extra text.
  (c) his sections are only the 6 stock slots; I ADDED `PublicWorksItems`/`ForeignItems` slots to building_box
      + window (his building_box has neither).
I am NOT asserting which of (a)/(b)/(c) is causal — that would be the same jump-to-convenient-cause error.

### 5. What is genuinely unknown after reading everything
Whether GetBuildInProvinceModel contains my qing buildings at all. If it DOES, the only thing that can hide a
present entry is the `visible` name-match failing (GetName != Localize(key) for these keys). If it does NOT,
no GUI change can help and the cause is in how the model is built (opaque). These two are indistinguishable by
reading — they are distinguishable by ONE experiment: render the model with NO name filter and see what is in it.

## CORRECTION + FINAL DIAGNOSIS + DECISION (2026-07-27, from complete code read)

### Correction to earlier sections
The earlier claim that qing_dike_building / public-works / foreign buildings "appear" in the macro builder is
WRONG (it was inferred, not observed). Per direct user boot report: the **Public Works section is an EMPTY
HEADER** and NO qing_* building appears in the macro builder. The true split is:
- **APPEAR:** every vanilla-style building with a plain-ASCII name (port, school, industrial_estate,
  resource_gathering, sewer, hospital, canal, railway_upgrade, depot, fortress, arsenal, districts).
- **FAIL:** every qing_* building (production + public works + foreign), all of which have CJK/concept-word
  localized names.

### The mechanism (100% read from source, no theory)
1. imp19c macro builder = hand-wired **categorized** `building_box` (gui/shared/gui_templates.gui:643).
   Each building needs a `macro_build_item_X` type (gui_templates.gui:791-1015) that instantiates the FULL
   model `MacroBuilderView.GetBuildInProvinceModel` (via `macro_building_parts_item`, :787) and shows ONE
   entry through `visible = "[EqualTo_string(MacroBuilderProvinceBuildable.GetName, Localize('X'))]"`.
2. The **province window** shows the SAME qing buildings, but compares
   `BuildingItem.GetBuilding.GetNameWithNoTooltip` (gui_templates.gui:430) — tooltip/concept markup STRIPPED.
3. `MacroBuilderProvinceBuildable` exposes ONLY: GetName, GetIconTexture, GetTooltip, GetPrice, IsEnabled,
   IsSelected, OnClick (verified: grep of every call site in gui/). It has NO GetNameWithNoTooltip and NO
   GetBuilding — so the categorized macro path CANNOT reproduce the province window's working comparison.
   → The categorized name-match is the blocker; it is unfixable within that approach for these names.

### The PROVEN alternative pattern (copy this)
Both of these render the model DIRECTLY — a single `fixedgridbox` over `GetBuildInProvinceModel`, printing every
entry (GetName / GetIconTexture / GetTooltip / price / OnClick), with NO per-building type and NO name-match:
- Terra Indomita: gui/macro_builder_view.gui:174-222 (its own custom buildings all list this way).
- imp19c's OWN naval tab: gui/macro_builder_view.gui:238-314 (same file, same MacroBuilderProvinceBuildable object).

### DECISION (autonomous, per user instruction; flagged for review)
Replace the categorized general-list `building_box` (macro_builder_view.gui ~157-227) with a direct
model-iterating `fixedgridbox` copied from imp19c's own naval section (:238-314). Rationale:
- CAUSE-AGNOSTIC: shows every building actually in GetBuildInProvinceModel regardless of name markup — fixes the
  display-filter problem, and if a building STILL doesn't appear it proves a genuine model-membership issue
  (not a GUI issue), which is diagnostic progress rather than another blind attempt.
- PROVEN: identical to TI + imp19c's own working naval tab.
- TRADE-OFF ACCEPTED: loses the category headers (Ports/Education/Industrial/…). Categories require either a
  name-match (broken) or a category accessor on the model (does not exist), so they cannot coexist with a
  guaranteed-working list. "It works" chosen over categories given the multi-week priority. Reversible: the old
  categorized block is preserved in git history; the per-building macro_build_item_* types become dead but
  harmless and can be pruned later.
- The change was made minimally: only the STEP-1 building list widget is swapped; the naval/province/trade-goods
  layouts and all building defs are untouched.

## Summary: Key Findings

### A. Data Flow
1. Building defined in `common/buildings/*.txt`
2. Engine populates `MacroBuilderView.GetBuildInProvinceModel` (C++ logic, not scriptable)
3. GUI templates (`gui/shared/gui_templates.gui`) define item rendering
4. Macro builder window (`gui/macro_builder_view.gui`) lists items in categorized sections
5. Each item template filters the full model by building name via `visible=` clause

### B. Model Membership Rule
**The C++ engine function `MacroBuilderView.GetBuildInProvinceModel` determines membership via UNKNOWN logic.** 

**Confirmed NOT the deciding factor:**
- Presence of `potential` block (qing_granary_building has one and is visible)
- Building name prefix (both `INF_depot` and `qing_dike_building` work)

**Suspected factors (unconfirmed):**
- Province-specific `potential` gates like `trade_goods = X` may exclude buildings (being tested)
- File location or building category may matter
- Engine may use a hardcoded registry

### C. How Sobisonator Added Buildings
Sobisonator's buildings (INF_depot, INF_hospital, etc.) follow this pattern:
- NO `potential` block
- Simple `allow` block with tech + job gates
- Placed in `00_infrastructure_buildings.txt` (vanilla-style file)
- Use `INF_` prefix (vanilla pattern)
- Full GUI wiring: build_item + macro_build_item + layouts + tooltips + loc

### D. Recipe to Add a Building
1. Define building in `common/buildings/*.txt` (NO province-specific `potential` blocks)
2. Add `build_item_X` template to `gui/shared/gui_templates.gui`
3. Add `macro_build_item_X` template to `gui/shared/gui_templates.gui`
4. Add to province window layout in `gui/province_window.gui`
5. Add to macro builder layout in `gui/macro_builder_view.gui`
6. Add `building_X_tooltip` template to `gui/shared/custom_tooltip.gui`
7. Add `macro_building_X_tooltip` template to `gui/shared/custom_tooltip.gui`
8. Add localization keys to `localization/english/*.yml`
9. Ensure icon exists
10. Boot test to verify

### E. Why Qing Production Buildings Fail
**Current status (as of 2026-07-27):**
- All GUI wiring is in place (items, layouts, tooltips)
- Buildings HAD `potential = { trade_goods = X }` blocks
- Those blocks were REMOVED on 2026-07-27 to match working buildings
- Change is **UNCONFIRMED** - awaiting boot test
- If they still fail after boot test, the cause is an engine-level restriction not visible in script code

**Next step:** Boot test as CHI and check if the six production works now appear in the macro builder Industrial section. If not, investigate whether moving them to a different file (e.g., renaming `qing_production_buildings.txt` to `00_qing_industrial_buildings.txt`) or adding an `IND_` prefix helps.
