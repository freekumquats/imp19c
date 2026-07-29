#!/usr/bin/env python3
"""[#133 I3] Generator for manufactured-goods production chains + split-writer pairs.

Emits, per good, the proven INDUSTRY_svalues chain (rate/production_bonus/base/
production/multiplier/efficiency + per-ingredient malus/importance/base_demand/demand
quad) IDENTICAL in shape to the 9 hand-built goods, and the GOODS_svalues split-writer
pair (_produced_mechanised + summed _produced) matching the I2 idiom.

Data-driven from RECIPES (see manufactured_goods.md D5a). This is the canonical MG-chain
generator; extend RECIPES here, never hand-copy a chain. Run with a batch name to emit
only that batch's goods:

    python3 tools/gen_mg_chains.py i3a industry   # INDUSTRY chains for the 5 cottage goods
    python3 tools/gen_mg_chains.py i3a goods      # GOODS split-pairs for the 5 cottage goods
    python3 tools/gen_mg_chains.py i3a demand     # DEMAND wiring lines (for manual insertion)

Output goes to stdout; the caller pastes/append it into the target file. DEMAND wiring is
emitted as per-raw-good fragments to be inserted before each aggregator's
`multiply = DEMAND_elasticity_impact` / `min = 0` closer.
"""
import sys

# good -> (rate, cottage_capable, [(ingredient, base_demand, importance), ...])
RECIPES = {
    # ---- I3a: cottage-capable (5) ----
    "construction_materials": (120, True, [("wood", 8, 1.0), ("stone", 6, 0.6), ("iron", 2, 0.3)]),
    "furniture":              (90,  True, [("wood", 10, 1.0)]),
    "luxury_furniture":       (55,  True, [("wood", 6, 1.0), ("silk", 2, 0.4), ("gold", 0.5, 0.3), ("gems", 0.5, 0.3), ("dye", 1, 0.2)]),
    "pharmaceuticals":        (40,  True, [("vegetables", 6, 1.0), ("whales", 2, 0.4)]),
    "wooden_ships":           (30,  True, [("wood", 20, 1.0), ("copper", 3, 0.4), ("industrial_fibres", 4, 0.5)]),
    # ---- I3b: mechanised-only intermediates (3) ----
    "steel":                  (90,  False, [("iron", 10, 1.0), ("coal", 6, 0.7)]),
    "chemicals":              (70,  False, [("sulphur", 6, 1.0), ("coal", 4, 0.5), ("salt", 3, 0.4)]),
    "rare_alloys":            (35,  False, [("steel", 4, 1.0), ("tin", 2, 0.4), ("lead", 2, 0.3), ("copper", 2, 0.3)]),
    # ---- I3c: mechanised-only consumers (7) ----
    "processed_foods":        (110, False, [("livestock", 6, 0.6), ("vegetables", 6, 0.6), ("fish", 4, 0.4), ("salt", 3, 0.5), ("glass", 2, 0.3)]),
    "late_munitions":         (70,  False, [("steel", 5, 0.7), ("chemicals", 4, 1.0), ("lead", 3, 0.4)]),
    "late_artillery":         (45,  False, [("steel", 8, 1.0), ("machine_parts", 3, 0.6), ("chemicals", 2, 0.4)]),
    "steel_ships":            (25,  False, [("steel", 20, 1.0), ("machine_parts", 5, 0.6), ("coal", 6, 0.4)]),
    "motors":                 (30,  False, [("steel", 6, 0.7), ("machine_parts", 5, 1.0), ("oil", 4, 0.5)]),
    "electronics":            (30,  False, [("rare_alloys", 4, 1.0), ("chemicals", 3, 0.5), ("copper", 3, 0.5)]),
    "petrochemicals":         (60,  False, [("oil", 10, 1.0), ("chemicals", 4, 0.6)]),
}

BATCHES = {
    "i3a": ["construction_materials", "furniture", "luxury_furniture", "pharmaceuticals", "wooden_ships"],
    "i3b": ["steel", "chemicals", "rare_alloys"],
    "i3c": ["processed_foods", "late_munitions", "late_artillery", "steel_ships", "motors", "electronics", "petrochemicals"],
}


def num(x):
    """Render a number without a trailing .0 (Paradox accepts both, but match house style)."""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def industry_chain(good, rate, ings):
    facs = f"INDUSTRY_{good}_factories"
    malus_adds = "\n".join(f"\tadd = INDUSTRY_malus_{good}_production_{ing}" for ing, _, _ in ings)
    out = []
    out.append(f"## {good.upper().replace('_', ' ')} [#133 I3]")
    out.append(f"INDUSTRY_production_rate_{good} = {{")
    out.append(f"\t# Base maximum output of one factory for this tradegood, at maximum productivity")
    out.append(f"\tvalue = {num(rate)}")
    out.append("}")
    out.append("")
    out.append(f"production_bonus_{good} = {{")
    out.append(f"\t# Scope: Country. Multiplier to mechanised industrial production.")
    out.append(f"\tvalue = 1")
    out.append("}")
    out.append("")
    out.append(f"INDUSTRY_production_{good}_base = {{")
    out.append(f"\tvalue = INDUSTRY_production_rate_{good}")
    out.append(f"\tmultiply = {facs}")
    out.append(f"\tmultiply = owner.production_bonus_{good}")
    out.append("}")
    out.append("")
    out.append(f"INDUSTRY_production_{good} = {{")
    out.append(f"\t# Applies modifiers from supply")
    out.append(f"\tvalue = INDUSTRY_production_{good}_base")
    out.append(f"\tmultiply = INDUSTRY_production_{good}_multiplier")
    out.append("}")
    out.append("")
    out.append(f"INDUSTRY_production_{good}_multiplier = {{")
    out.append(f"\t# Base production, minus maluses from ingredient shortages. All ingredient maluses listed here.")
    out.append(f"\tvalue = 1")
    out.append(malus_adds)
    out.append(f"\tmultiply = owner.MODIFIER_industry_productivity")
    out.append(f"\tmin = 0")
    out.append("}")
    out.append("")
    out.append(f"INDUSTRY_production_{good}_efficiency = {{")
    out.append(f"\tvalue = INDUSTRY_production_{good}")
    out.append(f"\tdivide = INDUSTRY_production_{good}_base")
    out.append("}")
    out.append("")
    out.append(f"# Ingredients")
    for ing, base, imp in ings:
        out.append("")
        out.append(f"# {ing.upper()}")
        out.append(f"INDUSTRY_malus_{good}_production_{ing} = {{")
        out.append(f"\tvalue = 0")
        out.append(f"\tif = {{")
        out.append(f"\t\tlimit = {{")
        out.append(f"\t\t\thas_variable = shortage_{ing}")
        out.append(f"\t\t}}")
        out.append(f"\t\tsubtract = var:shortage_{ing}")
        out.append(f"\t\tmultiply = INDUSTRY_demand_importance_{good}_{ing}")
        out.append(f"\t}}")
        out.append("}")
        out.append("")
        out.append(f"INDUSTRY_demand_importance_{good}_{ing} = {{")
        out.append(f"\t# 0..1 max malus this ingredient's shortage can impose on output")
        out.append(f"\tvalue = {num(imp)}")
        out.append("}")
        out.append("")
        out.append(f"INDUSTRY_base_demand_{good}_{ing} = {{")
        out.append(f"\t# Units demanded per factory")
        out.append(f"\tvalue = {num(base)}")
        out.append("}")
        out.append("")
        out.append(f"INDUSTRY_demand_{good}_{ing} = {{")
        out.append(f"\tvalue = {facs}")
        out.append(f"\tmultiply = INDUSTRY_base_demand_{good}_{ing}")
        out.append("}")
    out.append("")
    return "\n".join(out)


def goods_split(good, cottage_capable):
    out = []
    out.append(f"GOODS_governorship_{good}_produced_mechanised = {{")
    out.append(f"\t# [#133 I3] MECHANISED-ONLY term (split-writer D1a); this is what the produce loop adds.")
    out.append(f"\tvalue = 0")
    out.append(f"\tif = {{")
    out.append(f"\t\tlimit = {{")
    out.append(f"\t\t\thas_variable = INDUSTRY_factories_assigned_{good}")
    out.append(f"\t\t}}")
    out.append(f"\t\tadd = INDUSTRY_production_{good}")
    out.append(f"\t\tmultiply = GOODS_governorship_bonus_to_industrial_production_from_industrialisation")
    out.append(f"\t}}")
    out.append("}")
    out.append("")
    out.append(f"GOODS_governorship_{good}_produced = {{")
    if cottage_capable:
        out.append(f"\t# [#133 I3] SUMMED total (cottage + mechanised) for CONSUMERS (world price, wealth,")
        out.append(f"\t# DEMAND_difference, province GUI). Loop adds only the _mechanised term (D1a split-writer).")
        out.append(f"\tvalue = 0")
        out.append(f"\tif = {{")
        out.append(f"\t\tlimit = {{")
        out.append(f"\t\t\thas_variable = COTTAGEIND_produced_{good}")
        out.append(f"\t\t}}")
        out.append(f"\t\tadd = var:COTTAGEIND_produced_{good}")
        out.append(f"\t}}")
        out.append(f"\tadd = GOODS_governorship_{good}_produced_mechanised")
    else:
        out.append(f"\t# [#133 I3] SUMMED total for CONSUMERS. No cottage recipe for {good}, so equals the")
        out.append(f"\t# mechanised term; kept as a wrapper for consumer/consistency (I2 idiom).")
        out.append(f"\tvalue = GOODS_governorship_{good}_produced_mechanised")
    out.append("}")
    out.append("")
    return "\n".join(out)


def demand_wiring(goods):
    """Emit, per raw input, the `if` blocks to insert into that raw good's DEMAND aggregator."""
    by_raw = {}
    for g in goods:
        _, _, ings = RECIPES[g]
        for ing, _, _ in ings:
            by_raw.setdefault(ing, []).append(g)
    out = []
    for raw in sorted(by_raw):
        out.append(f"# --- insert into DEMAND_{raw} (before `multiply = DEMAND_elasticity_impact` / `min = 0`) ---")
        for g in by_raw[raw]:
            out.append(f"\tif = {{")
            out.append(f"\t\tlimit = {{")
            out.append(f"\t\t\thas_variable = INDUSTRY_factories_assigned_{g}")
            out.append(f"\t\t}}")
            out.append(f"\t\tadd = INDUSTRY_demand_{g}_{raw}")
            out.append(f"\t}}")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    batch = sys.argv[1] if len(sys.argv) > 1 else "i3a"
    mode = sys.argv[2] if len(sys.argv) > 2 else "industry"
    goods = BATCHES[batch]
    if mode == "industry":
        for g in goods:
            rate, cottage, ings = RECIPES[g]
            print(industry_chain(g, rate, ings))
    elif mode == "goods":
        for g in goods:
            _, cottage, _ = RECIPES[g]
            print(goods_split(g, cottage))
    elif mode == "demand":
        print(demand_wiring(goods))
    else:
        sys.exit(f"unknown mode {mode}")
