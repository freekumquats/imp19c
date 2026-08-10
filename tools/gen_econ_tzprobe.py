#!/usr/bin/env python3
# [#23 2026-08-09] Generator for the EXHAUSTIVE trade-zone economic probe (se_ECON_LOG_TZPROBE.txt).
#
# WHY A GENERATOR: the debug_log LABEL string CANNOT carry a $param$ (proven-broken: the engine eats
# the leading space and leaves a trailing literal $, se_ECON_LOG.txt:263-280). So a per-trade-zone probe
# needs one hand-identical block per (zone, metric) with a LITERAL label. 22 zones x several metrics x
# two goods = ~180 near-identical blocks; generating them guarantees consistency and zero copy-paste drift.
# Output is committed as the .txt; this generator is the canonical source (like tools/gen_table_icons.py).
#
# WHAT IT PROBES (to unwind the whole trade-price -> currency layer in ONE boot):
#   - BANDS (one cheap debug_log line each, order-of-magnitude buckets) for EVERY trade zone's
#     local_price / stockpile / total_order_size / pct_of_global_stockpile, for silver (the confirmed
#     oscillator) AND grain (a CONTROL good — is the swing silver-specific or systemic?). Full coverage,
#     near-zero log volume.
#   - EXACT TICKS (bounded, cap 8000) for the silver ratio-inputs that actually feed gbip: per-zone
#     local_price_silver + stockpile_silver + total_order_size_silver, plus the global aggregates
#     (global_stockpile_silver, global_base_import_price_silver). Precise magnitudes where it counts.
#
# BOOT SAFETY: bands are 1 line/metric. Exact ticks are while-count capped at 8000/metric (the shared
# tail ECON_LOG_curx_tick_emit already hard-caps + emits a CAPPED flag). Emitted only PRE and POST of the
# quarterly trade recompute, CHI-only, -debug_mode-gated by the callers. Reads are existence-guarded so an
# unset global var emits a ZERO/UNSET flag, never an error.
#
# READ-BACK (same convention as the existing CURXV layer, se_ECON_LOG.txt:608-673):
#   bands:  grep "IMP19C TZP BAND <good> <zone> <metric>"           -> the bucket line
#   exact:  per quarter window, (count "IMP19C TZP unit" after "TZP LABEL <good> <zone> <metric>"
#           and before the next LABEL) / SCALE  == exact value.

ZONES = [
    "india", "east_north_america", "west_north_america", "caribbean",
    "west_south_america", "east_south_america", "south_east_asia", "indo_china",
    "yellow_sea", "southern_africa", "west_africa", "east_africa", "middle_east",
    "western_steppe", "eastern_steppe", "upper_yangtzi", "atlantic_seaboard",
    "central_europe", "west_mediterranean", "baltic", "east_europe", "east_mediterranean",
]

# [#51 2026-08-09] The goods the probe tracks. Extended beyond the #23 silver/grain pair so ONE boot can
# confirm whether the trade system is WELL-DESIGNED across the axes now under active work:
#   silver, gold   — the metal SELL-RESERVE comparison (#46: does gold stay > silver, and how does the
#                    gold/silver ratio move? both feed global_base_import_price_<metal>, the sell price).
#   grain          — the staple CONTROL (baseline low-tier price).
#   salt           — #44 salt revenue = output x market x gabelle markup: watch its local_price + output.
#   tea, silk      — luxuries for BOTH the cross-good tier spread (#52: luxury vs grain ~10-20x?) AND the
#                    regional same-good gap (#50: is yellow_sea/upper_yangtzi tea cheaper than European tea?).
# The CHI-PAID section below additionally logs what the QING actually pays + its per-good penetration, so
# the regional divergence that reaches the PLAYER (not just the world price) is measurable.
GOODS = ["silver", "gold", "grain", "salt", "tea", "silk"]

# China-adjacent vs European TZs — the pair the regional-divergence question (#50) turns on. Logged as an
# explicit BANDSET tag so the read-back can eyeball the same-good gap without hunting all 22 zones.
CHINA_TZS = ["yellow_sea", "upper_yangtzi"]
EUROPE_TZS = ["atlantic_seaboard", "central_europe", "west_mediterranean", "baltic", "east_europe", "east_mediterranean"]

# Bands: log2-ish order-of-magnitude buckets that make a ~200x swing unmistakable while staying 1 line.
def band_block(good, zone, metric, read_expr, exists_guard):
    tag = f"IMP19C TZP BAND {good} {zone} {metric}"
    return f"""\t\t# {good} {zone} {metric}
\t\tif = {{ limit = {{ NOT = {{ {exists_guard} }} }}  debug_log = "{tag} UNSET" }}
\t\telse = {{
\t\t\tset_variable = {{ name = ECON_LOG_tzp_v  value = {read_expr} }}
\t\t\tif = {{ limit = {{ NOT = {{ var:ECON_LOG_tzp_v > -999999999 }} }}  debug_log = "{tag} EMPTY" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v <= 0 }}       debug_log = "{tag} 0" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 0.01 }}     debug_log = "{tag} 0-0.01" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 0.1 }}      debug_log = "{tag} 0.01-0.1" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 1 }}        debug_log = "{tag} 0.1-1" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 10 }}       debug_log = "{tag} 1-10" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 100 }}      debug_log = "{tag} 10-100" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 1000 }}     debug_log = "{tag} 100-1000" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 10000 }}    debug_log = "{tag} 1000-10000" }}
\t\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 100000 }}   debug_log = "{tag} 10000-100000" }}
\t\t\telse = {{ debug_log = "{tag} >=100000" }}
\t\t\tremove_variable = ECON_LOG_tzp_v
\t\t}}
"""

# Band block for a bare SCRIPT VALUE (not a stored variable) — e.g. DEMAND_country_<good>, which is a
# script_value (DEMAND_svalues.txt), NOT a var. There is no `exists`/`has_variable` for a script value, so
# stage it into ECON_LOG_tzp_v unconditionally and let the sentinel (NOT > -999999999 -> EMPTY) + the <=0
# bucket classify it. Mirrors the proven ECON_LOG_curx_agdemand reader (se_ECON_LOG.txt) which reads the
# bare svalue into a temp and buckets it.
def band_block_svalue(good, zone, metric, svalue_expr):
    tag = f"IMP19C TZP BAND {good} {zone} {metric}"
    return f"""\t\t# {good} {zone} {metric} (bare script_value, no exists guard)
\t\tset_variable = {{ name = ECON_LOG_tzp_v  value = {svalue_expr} }}
\t\tif = {{ limit = {{ NOT = {{ var:ECON_LOG_tzp_v > -999999999 }} }}  debug_log = "{tag} EMPTY" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v <= 0 }}       debug_log = "{tag} 0" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 0.01 }}     debug_log = "{tag} 0-0.01" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 0.1 }}      debug_log = "{tag} 0.01-0.1" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 1 }}        debug_log = "{tag} 0.1-1" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 10 }}       debug_log = "{tag} 1-10" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 100 }}      debug_log = "{tag} 10-100" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 1000 }}     debug_log = "{tag} 100-1000" }}
\t\telse_if = {{ limit = {{ var:ECON_LOG_tzp_v < 10000 }}    debug_log = "{tag} 1000-10000" }}
\t\telse = {{ debug_log = "{tag} >=10000" }}
\t\tremove_variable = ECON_LOG_tzp_v
"""

# Exact-tick block: stages RAW value + scale, calls the shared proven tail (guards/scales/rounds/caps/emits).
def tick_block(good, zone, metric, read_expr, exists_guard, scale):
    label = f"IMP19C TZP LABEL {good} {zone} {metric}"
    return f"""\t\tdebug_log = "{label}"
\t\tif = {{ limit = {{ {exists_guard} }}  set_variable = {{ name = ECON_LOG_tickval  value = {read_expr} }} }}
\t\telse = {{ set_variable = {{ name = ECON_LOG_tickval  value = 0 }} }}
\t\tset_variable = {{ name = ECON_LOG_tickscale  value = {scale} }}
\t\tECON_LOG_curx_tick_emit = yes
"""

def read_forms(good, zone):
    # local_price sits on the tradezone OBJECT global var; the other three are flat globals.
    return {
        "price": (f"global_var:global_{zone}_tradezone.var:local_price_{good}",
                  f"exists = global_var:global_{zone}_tradezone"),
        "stock": (f"global_var:{zone}_stockpile_{good}",
                  f"exists = global_var:{zone}_stockpile_{good}"),
        "order": (f"global_var:{zone}_total_order_size_{good}",
                  f"exists = global_var:{zone}_total_order_size_{good}"),
        "pct":   (f"global_var:{zone}_percentage_of_global_stockpile_{good}",
                  f"exists = global_var:{zone}_percentage_of_global_stockpile_{good}"),
    }

def build():
    out = []
    out.append("""########################################################################
# se_ECON_LOG_TZPROBE.txt  —  #23 EXHAUSTIVE trade-zone economic probe (GENERATED)
#
# GENERATED by tools/gen_econ_tzprobe.py — DO NOT HAND-EDIT; edit the generator + regen.
#
# Read-only diagnostic. Instruments the WORLD trade-price layer that feeds gbip_silver -> the CHI
# currency peg -> the #23 period-2 currency oscillation. Two independent deep-traces proved CHI is a
# price-TAKER (produces zero silver); the oscillator lives in the producer-side trade zones, which the
# CHI-scoped CURX dump could not see. This probe reads the WORLD trade-zone globals (readable from any
# scope) so ONE boot pins WHERE and WHY the trade price oscillates.
#
# BANDS (cheap, full coverage): every zone x {price,stock,order,pct} for silver + a grain CONTROL.
# EXACT TICKS (bounded, cap 8000): silver's per-zone price/stock/order + global aggregates.
#
# Emitted PRE and POST of quarterly_global_trade_6 via ECON_LOG_curx_dump_pre/_post (CHI-only,
# -debug_mode-gated). Uses the proven tick tail ECON_LOG_curx_tick_emit (se_ECON_LOG.txt:639).
# No $param$ in any log string (all labels literal — the proven constraint). All global reads
# existence-guarded (unset -> UNSET/ZERO flag, never an error).
########################################################################

# ==== BANDS: full-coverage order-of-magnitude survey (1 line/metric) ====
ECON_LOG_tzprobe_bands = {
\t# Scope: country (CHI, guarded by caller). Order-of-magnitude bucket per world trade-zone metric.
""")
    for good in GOODS:
        out.append(f'\t\tdebug_log = "IMP19C TZP BANDSET {good}"\n')
        # global aggregates for this good (world stockpile + post-sqrt gbip) as bands so their
        # magnitude is covered even though the world-sum stockpile is not exact-ticked (review HIGH-2).
        out.append(band_block(good, "GLOBAL", "stock",
                              f"global_var:global_stockpile_{good}",
                              f"exists = global_var:global_stockpile_{good}"))
        out.append(band_block(good, "GLOBAL", "gbip",
                              f"global_var:global_base_import_price_{good}",
                              f"exists = global_var:global_base_import_price_{good}"))
        for zone in ZONES:
            rf = read_forms(good, zone)
            for metric in ("price", "stock", "order", "pct"):
                expr, guard = rf[metric]
                out.append(band_block(good, zone, metric, expr, guard))
    out.append("}\n\n")

    # ==== CHI-PAID + REGIONAL-GAP survey ====================================================
    # [#51] What the QING actually PAYS per good, and its per-good market penetration — the numbers that
    # reveal whether regional divergence reaches the PLAYER (not just the world price) and whether the
    # ~1.9-3x penetration cap (#50 adversarial review) binds. Plus an explicit China-TZ-vs-Europe-TZ
    # local_price grouping so the same-good regional gap (#50) is eyeballable without scanning 22 zones.
    # Scope: country (CHI, guarded by caller). Bands only (cheap); the exact metal series is ticked below.
    out.append("""# ==== CHI-PAID: what the Qing pays per good + its penetration (regional divergence AS FELT) ====
ECON_LOG_tzprobe_chipaid = {
\t# Scope: country (CHI, guarded by caller). country_unit_price_<good> = world gbip / (0.5 + penetration);
\t# penetration is the per-country, per-TZ, shipping-driven access term (capped 1, x0.4545). Together these
\t# show whether the Qing pays LESS for China-sourced goods than the world price implies (#46/#50).
""")
    for good in GOODS:
        out.append(f'\t\tdebug_log = "IMP19C TZP CHIPAID {good}"\n')
        # [#51 review MED] country-local vars use has_variable guard (the proven country-var reader form in
        # se_ECON_LOG.txt:480/700/726), NOT exists = var: which is untested against this file's convention.
        out.append(band_block(good, "CHI", "paidprice",
                              f"var:country_unit_price_{good}",
                              f"has_variable = country_unit_price_{good}"))
        out.append(band_block(good, "CHI", "penetration",
                              f"var:country_global_market_penetration_{good}",
                              f"has_variable = country_global_market_penetration_{good}"))
        # [#51 review CRITICAL 2] DEMAND_country_<good> is a SCRIPT VALUE, not a var — read it bare via the
        # svalue band block (var:DEMAND_country_<good> would always read UNSET, silently logging nothing).
        out.append(band_block_svalue(good, "CHI", "demand",
                              f"DEMAND_country_{good}"))
    out.append("}\n\n")

    # ==== REGIONAL GAP: China-adjacent TZ local_price vs European TZ local_price, per good ====
    # [#51] The #50 same-good regional gap made directly comparable: for each good, the China-source TZs
    # (yellow_sea/upper_yangtzi) then the European TZs, banded, under one grouped tag so read-back can
    # diff "is Canton tea cheaper than London tea?" at a glance.
    out.append("""# ==== REGIONAL GAP: China-source TZ price vs Europe TZ price, per good (the #50 same-good gap) ====
ECON_LOG_tzprobe_regiongap = {
\t# Scope: country. For each good, band local_price in the China-source TZs then the European TZs.
""")
    for good in GOODS:
        out.append(f'\t\tdebug_log = "IMP19C TZP REGIONGAP {good} CHINA"\n')
        for zone in CHINA_TZS:
            expr, guard = read_forms(good, zone)["price"]
            out.append(band_block(good, zone, "price", expr, guard))
        out.append(f'\t\tdebug_log = "IMP19C TZP REGIONGAP {good} EUROPE"\n')
        for zone in EUROPE_TZS:
            expr, guard = read_forms(good, zone)["price"]
            out.append(band_block(good, zone, "price", expr, guard))
    out.append("}\n\n")

    out.append("""# ==== EXACT TICKS: metal price inputs that feed gbip (bounded; shared tail caps at 8000) ====
ECON_LOG_tzprobe_exact = {
\t# Scope: country (CHI). Exact scaled-integer tick-counts for the metal PRICE inputs to gbip.
\t# SCALE chosen so realistic values land well under the shared tail's 8000 cap. Read: count
\t# "IMP19C TZP unit" after a "TZP LABEL ..." and before the next LABEL, / SCALE.
\t# NOTE [review HIGH-2]: world-scale SUM vars (global_stockpile_*, per-zone stock/order) are NOT
\t# exact-ticked — they would peg the 8000 cap every dump (multi-GB log, truncated=useless). Their
\t# magnitude is captured by the BANDS. Only gbip (post-sqrt, small) + per-zone local_price are ticked.
\t# [#51] BOTH metals ticked (was silver-only): the gold/silver gbip pair is the #46 sell-reserve
\t# comparison — exact values needed to see whether/how far silver crosses gold.
""")
    for metal in ("silver", "gold"):
        out.append(f'\tdebug_log = "IMP19C TZP LABEL {metal} GLOBAL gbip"\n')
        out.append(f'\tif = {{ limit = {{ exists = global_var:global_base_import_price_{metal} }}  set_variable = {{ name = ECON_LOG_tickval  value = global_var:global_base_import_price_{metal} }} }}\n')
        out.append('\telse = { set_variable = { name = ECON_LOG_tickval  value = 0 } }\n')
        out.append('\tset_variable = { name = ECON_LOG_tickscale  value = 2000 }\n')
        out.append('\tECON_LOG_curx_tick_emit = yes\n')
        out.append(f'\t# --- per-zone {metal} price (the local_price = order/stockpile x0.6 input to gbip) ---\n')
        for zone in ZONES:
            rf = read_forms(metal, zone)
            # [review HIGH-2] ONLY per-zone price is exact-ticked (scale 100 -> realistic ~0..20 -> 0..2000,
            # well under the 8000 cap). Per-zone stock/order are NOT exact-ticked: world-scale sums that
            # would peg the cap. Magnitude covered by the BANDS; exact PRICE is what gbip = sqrt(Σ price×share) needs.
            out.append(tick_block(metal, zone, "price", *rf["price"], scale=100))
        out.append(f'\tdebug_log = "IMP19C TZP LABEL {metal} END"\n')
    out.append("}\n")
    return "".join(out)

if __name__ == "__main__":
    import os
    dst = os.path.join(os.path.dirname(__file__), "..", "common", "scripted_effects", "se_ECON_LOG_TZPROBE.txt")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("wrote", os.path.normpath(dst))
