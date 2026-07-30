#!/usr/bin/env python3
"""[#133 I9] Generator for the 17 manufactured-goods factory tooltips (D8).

The province-window factory tooltip is a macro-assembled string in
localization/english/industry_l_english.yml. Each producible good has:
  * one `PROVWINDOW_GOV_<GOOD>_PRODUCED_TT` body that stitches the shared frame
    macros (industry_TT_p0..p11) around the good key and lists its ingredients, and
  * one `ind_<good>_ingredient_<ing>` submacro per ingredient, which expands the
    shared ingredient frame (industry_TT_ingredient_p1..p5) around:
        p1 -> ingredient display name
        p2 -> <good>_<ing>            (INDUSTRY_base_demand_<good>_<ing>)
        p3 -> <good>_production_<ing> (INDUSTRY_malus_<good>_production_<ing>)
        p4 -> <good>_<ing>            (INDUSTRY_demand_importance_<good>_<ing>)

Shape is byte-for-byte the same idiom as the 7 hand-built goods (clothing, bronze,
naval_supplies, machine_parts, alcohol, early_munitions, luxury_clothing). This just
data-drives the remaining 17 from the ground-truth INDUSTRY_base_demand svalues so the
list never drifts from the production chains.

Emits YAML fragments to stdout for insertion into industry_l_english.yml (replacing the
`# PLACEHOLDERS` block). The caller wires them in preserving BOM+CRLF.
"""
import sys

# good -> (title-cased industry name, [(ingredient_key, ingredient_display), ...])
# Ingredient order + membership is taken from INDUSTRY_svalues.txt (INDUSTRY_base_demand_*),
# so it matches the production chain exactly. Display names match imp19c_tradegoods loc.
GOODS = {
    "furniture":              ("Furniture",              [("wood", "Wood")]),
    "luxury_furniture":       ("Luxury Furniture",       [("wood", "Wood"), ("silk", "Silk"), ("gold", "Gold"), ("gems", "Gemstones"), ("dyes", "Dyes")]), # [#144 I12g] dye -> manufactured dyes
    "glass":                  ("Glass",                  [("coal", "Coal"), ("stone", "Stone"), ("lead", "Lead")]),
    "pharmaceuticals":        ("Pharmaceuticals",        [("vegetables", "Vegetables"), ("whales", "Whales")]),
    "processed_foods":        ("Processed Foods",        [("livestock", "Livestock"), ("vegetables", "Vegetables"), ("fish", "Fish"), ("salt", "Salt"), ("glass", "Glass")]),
    "motors":                 ("Motors",                 [("steel", "Steel"), ("machine_parts", "Machine Parts"), ("oil", "Oil")]),
    "electronics":            ("Electronics",            [("rare_alloys", "Rare Alloys"), ("chemicals", "Chemicals"), ("copper", "Copper")]),
    "rare_alloys":            ("Rare Alloys",            [("steel", "Steel"), ("tin", "Tin"), ("lead", "Lead"), ("copper", "Copper")]),
    "construction_materials": ("Construction Materials", [("wood", "Wood"), ("stone", "Stone"), ("iron", "Iron")]),
    "steel":                  ("Steel",                  [("iron", "Iron"), ("coal", "Coal")]),
    "chemicals":              ("Chemicals",              [("sulphur", "Sulphur"), ("coal", "Coal"), ("salt", "Salt")]),
    "late_munitions":         ("Late Munitions",         [("steel", "Steel"), ("chemicals", "Chemicals"), ("lead", "Lead")]),
    "steel_ships":            ("Steel Ships",            [("steel", "Steel"), ("machine_parts", "Machine Parts"), ("coal", "Coal")]),
    "wooden_ships":           ("Wooden Ships",           [("wood", "Wood"), ("copper", "Copper"), ("industrial_fibres", "Industrial Fibres")]),
    "early_artillery":        ("Early Artillery",        [("sulphur", "Sulphur"), ("wood", "Wood"), ("stone", "Stone"), ("lead", "Lead"), ("textile_fibres", "Textile Fibres"), ("iron", "Iron"), ("steel", "Steel"), ("bronze", "Bronze"), ("livestock", "Livestock")]),
    "late_artillery":         ("Late Artillery",         [("steel", "Steel"), ("machine_parts", "Machine Parts"), ("chemicals", "Chemicals")]),
    "petrochemicals":         ("Petrochemicals",         [("oil", "Oil"), ("chemicals", "Chemicals")]),
    # [#144 I12] Phase-5 new goods.
    "refined_sugar":          ("Refined Sugar",          [("sugar", "Sugar"), ("coal", "Coal")]),
    "silk_cloth":             ("Silk Cloth",             [("silk", "Silk"), ("dye", "Dye")]),
    "paper":                  ("Paper",                  [("wood", "Wood"), ("textile_fibres", "Textile Fibres")]),
    "dyes":                   ("Dyes",                   [("dye", "Dye"), ("chemicals", "Chemicals")]),
    "gunpowder":              ("Gunpowder",              [("saltpetre", "Saltpetre"), ("sulphur", "Sulphur"), ("wood", "Wood")]),
}


def submacro(good, ing, disp):
    """One ind_<good>_ingredient_<ing> line (matches the hand-built idiom exactly)."""
    return (f'ind_{good}_ingredient_{ing}:0 '
            f'"$industry_TT_ingredient_p1${disp}'
            f'$industry_TT_ingredient_p2${good}_{ing}'
            f'$industry_TT_ingredient_p3${good}_production_{ing}'
            f'$industry_TT_ingredient_p4${good}_{ing}'
            f'$industry_TT_ingredient_p5$"')


def produced_tt(good, title, ings):
    """The PROVWINDOW_GOV_<GOOD>_PRODUCED_TT body. A single TAB separates the header from the
    frame, then each ingredient submacro is prefixed with a run of TABs, matching the hand
    idiom (the whitespace is cosmetic inside the tooltip)."""
    key = f"PROVWINDOW_GOV_{good.upper()}_PRODUCED_TT"
    head = (f'{key}:0 "#L #T {title} Industry#!#!\t'
            f'$industry_TT_p0${good}$industry_TT_p1${good}$industry_TT_p2${good}'
            f'$industry_TT_p3${good}$industry_TT_p4${good}$industry_TT_p5${good}$industry_TT_p6$')
    body = "".join(f'\t\t\t\t\t$ind_{good}_ingredient_{ing}$' for ing, _ in ings)
    tail = (f'\t\t\t\t$industry_TT_p7${good}$industry_TT_p8${good}'
            f'$industry_TT_p9${good}$industry_TT_p10${good}$industry_TT_p11$"')
    return head + body + tail


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    goods = [only] if only else list(GOODS)
    lines = ["", "# MANUFACTURED GOODS TOOLTIPS [#133 I9] (generated by tools/gen_industry_tooltips.py)", ""]
    for g in goods:
        title, ings = GOODS[g]
        lines.append(f"# {title.upper()}")
        lines.append("")
        for ing, disp in ings:
            lines.append(submacro(g, ing, disp))
            lines.append("")
        lines.append(produced_tt(g, title, ings))
        lines.append("")
    print("\n".join(lines))
