#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task #64 — clone the `tobacco` trade-good archetype into 5 New World crops.

tobacco = pure category-2 consumer cash crop (price/trade-simulated, gives
local_monthly_food, NOT in the fixed 6-good staple basket, NO downstream industrial
recipe). Verified the CLEAN archetype: sugar's extra refs are alcohol-recipe inputs that
tobacco lacks, so tobacco carries exactly the surface a pure cash crop needs.

DESIGN NOTE (recorded in SESSION_REPORT): the mod's demand engine simulates non-staple
goods only through the "luxury" demand path (category-2 goods: tobacco/sugar/coffee/tea/
opium/spices/chocolate). To be *simulated at all*, the New World crops must follow tobacco
into that path — so they are category-2 cash crops, NOT added to the locked 6-good staple
food basket. Their population effect is delivered via trade_goods `local_monthly_food`
(same as tobacco), which is the correct lever for a producible food-ish good here.

Edit kinds:
  block_named     — unique `Name...tobacco... = { ... }`; brace-matched, cloned ×5 after.
  block_enclosing — clone the brace-block ENCLOSING a unique inner line (for call-sites
                    whose effect name repeats). *_all variant clones at every occurrence.
  list_insert     — tobacco is a sibling line; add 5 crop siblings. *_all for N occurrences.
Fail-loud: every anchor must hit the expected count or abort. All edits computed in
memory; nothing is written unless the whole plan succeeds AND braces verify.
"""
import io, os, sys

ROOT = "/Users/alan.chiang/github.com/imp19c"
CROPS = ["maize", "sweet_potato", "potato", "peanut", "chili"]
DRY = "--dry" in sys.argv

def read(p):
    with io.open(os.path.join(ROOT, p), encoding="utf-8-sig") as f:
        return f.read()

changes = []

def clone_tok(block, crop):
    return block.replace("tobacco", crop).replace("TOBACCO", crop.upper())

def _occ(text, anchor):
    out, i = [], text.find(anchor)
    while i != -1:
        out.append(i); i = text.find(anchor, i + 1)
    return out

def _match_brace(text, open_idx):
    depth, j = 0, open_idx
    while j < len(text):
        c = text[j]
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: return j
        j += 1
    raise SystemExit("unbalanced from %d" % open_idx)

def block_named(text, name_anchor, fname, label):
    occ = _occ(text, name_anchor)
    if len(occ) != 1:
        raise SystemExit(f"[{fname}] {label}: name anchor count={len(occ)} (want 1): {name_anchor!r}")
    si = occ[0]
    b = text.index("{", si)
    end = _match_brace(text, b) + 1
    block = text[si:end]
    clones = "".join("\n\n" + clone_tok(block, c) for c in CROPS)
    changes.append((fname, f"block_named {label}"))
    return text[:end] + clones + text[end:]

def _enclosing_span(text, inner_idx):
    # walk back to the enclosing block's opening brace
    depth, j = 0, inner_idx
    while j >= 0:
        c = text[j]
        if c == "}": depth += 1
        elif c == "{":
            if depth == 0: break
            depth -= 1
        j -= 1
    if j < 0: raise SystemExit("no enclosing open brace")
    open_idx = j
    # back up to the start of the line the keyword sits on
    line_start = text.rfind("\n", 0, open_idx) + 1
    end = _match_brace(text, open_idx) + 1
    return line_start, end

def block_enclosing_all(text, inner_anchor, fname, label, expect):
    occ = _occ(text, inner_anchor)
    if len(occ) != expect:
        raise SystemExit(f"[{fname}] {label}: inner count={len(occ)} (want {expect}): {inner_anchor!r}")
    # process right-to-left so earlier indices stay valid after insertion
    for idx in sorted(occ, reverse=True):
        ls, end = _enclosing_span(text, idx)
        block = text[ls:end]                                  # e.g. "\t\tPURCHASE_... = { ... }"
        indent = block[:len(block) - len(block.lstrip("\t "))]  # leading whitespace of first line
        body = block[len(indent):]                            # block without leading indent
        clones = "".join("\n" + indent + clone_tok(body, c) for c in CROPS)
        text = text[:end] + clones + text[end:]
    changes.append((fname, f"block_enclosing {label} ×{expect}"))
    return text

def list_insert_all(text, anchor_line, fname, label, expect):
    occ = _occ(text, anchor_line)
    if len(occ) != expect:
        raise SystemExit(f"[{fname}] {label}: line count={len(occ)} (want {expect}): {anchor_line!r}")
    for idx in sorted(occ, reverse=True):
        endl = idx + len(anchor_line)
        add = "".join("\n" + clone_tok(anchor_line, c) for c in CROPS)
        text = text[:endl] + add + text[endl:]
    changes.append((fname, f"list_insert {label} ×{expect}"))
    return text

def _match(text, o):
    d, j = 0, o
    while j < len(text):
        if text[j] == "{": d += 1
        elif text[j] == "}":
            d -= 1
            if d == 0: return j
        j += 1
    raise SystemExit("unbalanced")

def block_ifelse_unit(text, inner_anchor, fname, label):
    """Clone the `if { ...inner_anchor... } else { ... }` unit that surrounds a UNIQUE
    inner line (the se_GOODS stockpile-init pattern). Both if and else are duplicated so
    the else stays bound to its if."""
    occ = _occ(text, inner_anchor)
    if len(occ) != 1:
        raise SystemExit(f"[{fname}] {label}: inner count={len(occ)} (want 1)")
    i = occ[0]
    ifs = text.rfind("if = {", 0, i)
    ls = text.rfind("\n", 0, ifs) + 1
    indent = text[ls:ifs]
    o1 = text.index("{", ifs); c1 = _match(text, o1)
    elsei = text.index("else", c1); o2 = text.index("{", elsei); c2 = _match(text, o2)
    unit = text[ls:c2 + 1]
    body = unit[len(indent):]
    clones = "".join("\n" + indent + clone_tok(body, c) for c in CROPS)
    changes.append((fname, f"block_ifelse_unit {label}"))
    return text[:c2 + 1] + clones + text[c2 + 1:]

def income_addchain(text, fname, label):
    """INCOME excise-duty chain: tobacco initializes with `value =`; clones must use
    `add =` and are inserted right after the tobacco sub-if."""
    anchor = ("\t\tif = {\n\t\t\tlimit = {\n\t\t\t\thas_variable = "
              "final_quarterly_wealth_owed_for_tobacco\n\t\t\t}\n\t\t\tvalue = "
              "var:final_quarterly_wealth_owed_for_tobacco\n\t\t}")
    occ = _occ(text, anchor)
    if len(occ) != 1:
        raise SystemExit(f"[{fname}] {label}: income anchor count={len(occ)} (want 1)")
    i = occ[0]; end = i + len(anchor)
    clones = "".join("\n" + anchor.replace("tobacco", c).replace("value =", "add =")
                     for c in CROPS)
    changes.append((fname, f"income_addchain {label}"))
    return text[:end] + clones + text[end:]

print("helpers ready; crops =", CROPS, "| DRY" if DRY else "| LIVE")

# =====================================================================================
# Per-crop presentation data (loc names/descs + trade_goods hsv color).
# Colors chosen distinct from tobacco's hsv{0.1 1 0.1}; kept in-gamut of existing goods.
CROP_META = {
    "maize":        ("Maize",        "hsv { 0.13 0.95 0.95 }",
        "A New World grain, hardy and prolific. Introduced to the Old World after Columbus, it spread to become a staple across southern China, feeding a booming population."),
    "sweet_potato": ("Sweet Potato", "hsv { 0.06 0.7 0.85 }",
        "The 'earth-dragon' tuber from the Americas. Thriving on poor upland soils, it underwrote much of the Qing demographic explosion of the eighteenth century."),
    "potato":       ("Potato",       "hsv { 0.11 0.35 0.9 }",
        "A tuber from the Andes that yields heavily even in cold, marginal ground, transforming the diet of highland and northern peoples."),
    "peanut":       ("Peanut",       "hsv { 0.09 0.55 0.8 }",
        "The groundnut, an American legume prized for its oil and protein. It grows where cereals cannot and enriches exhausted soils."),
    "chili":        ("Chili",        "hsv { 0.99 0.9 0.9 }",
        "The fiery American pepper that conquered the world's kitchens within a century, becoming inseparable from the cuisines of Sichuan, Hunan and beyond."),
}

def verify_braces(path, before_net):
    t = read(path)
    net = t.count("{") - t.count("}")
    if net != before_net:
        raise SystemExit(f"[{path}] BRACE IMBALANCE: baseline net={before_net}, now={net}")
    return net

# capture baselines
TARGETS = [
    "common/trade_goods/00_imp19c.txt",
    "common/script_values/GOODS_svalues.txt",
    "common/script_values/DEMAND_luxury_svalues.txt",
    "common/script_values/DEMAND_svalues.txt",
    "common/script_values/PRICE_svalues.txt",
    "common/script_values/AI_svalues.txt",
    "common/script_values/TRADE_svalues.txt",
    "common/script_values/WEALTH_svalues.txt",
    "common/script_values/INCOME_svalues.txt",
    "common/script_values/DEMAND_food_svalues.txt",
    "common/scripted_effects/se_GOODS.txt",
    "common/scripted_effects/se_TRADE.txt",
    "common/scripted_effects/se_PRICE.txt",
    "common/scripted_effects/se_DEMAND.txt",
    "common/scripted_effects/se_GLOBALTRADE_split.txt",
    "common/scripted_effects/se_PURCHASE.txt",
    "common/scripted_effects/se_SELL.txt",
    "common/scripted_effects/se_TRADE_new.txt",
    "common/scripted_triggers/00_resource_building_potential.txt",
    "common/scripted_triggers/00_trade_scripted_triggers.txt",
    "common/customizable_localization/000_ECON_loc.txt",
    "common/modifiers/00_cultural_modifiers.txt",
    "common/scripted_effects/zz_tradegoods_injector.txt",
    "common/scripted_effects/zz_tradegood_injector.txt",
    "common/scripted_effects/zz_luxury_goods_injector.txt",
    "common/scripted_effects/zz_tradegood_luxury_injector.txt",
]
BASELINE = {}
for p in TARGETS:
    t = read(p)
    BASELINE[p] = t.count("{") - t.count("}")

OUT = {}  # path -> new text

def edit(path, fn):
    t = OUT.get(path, read(path))
    OUT[path] = fn(t)

# ---- trade_goods definition (explicit: crop-specific color, not a token swap) --------
def do_trade_goods(t):
    anchor = "tobacco = {\n\tcategory = 2"
    i = find_unique_local(t, anchor, "trade_goods")
    b = t.index("{", i); end = _match(t, b) + 1
    block = t[i:end]
    out = block
    for c in CROPS:
        nb = clone_tok(block, c)
        # swap the color line to the crop-specific hsv
        nb = nb.replace("color = hsv { 0.1 1 0.1 }", "color = " + CROP_META[c][1])
        out += "\n\n" + nb
    return t[:i] + out + t[end:]

def find_unique_local(text, anchor, fname):
    occ = _occ(text, anchor)
    if len(occ) != 1:
        raise SystemExit(f"[{fname}] anchor count={len(occ)} (want 1): {anchor!r}")
    return occ[0]


# =====================================================================================
# APPLY ALL EDITS
edit("common/trade_goods/00_imp19c.txt", do_trade_goods)

edit("common/script_values/GOODS_svalues.txt", lambda t: (t := list_insert_all(t, "\tadd = GOODS_national_production_tobacco", "GOODS", "natprod_entry", 1), t := block_named(t, "GOODS_national_production_tobacco = {", "GOODS", "natprod"), t := block_named(t, "GOODS_tobacco_stockpile = {", "GOODS", "stockpile"), t := block_named(t, "GOODS_governorship_tobacco_produced = {", "GOODS", "gov_produced"), block_named(t, "GOODS_country_total_sold_tobacco = {", "GOODS", "country_sold"))[-1])

edit("common/script_values/DEMAND_luxury_svalues.txt", lambda t: block_named(t, "DEMAND_tobacco = { # Total", "DEMAND_lux", "demand_total"))

edit("common/script_values/DEMAND_svalues.txt", lambda t: (t := block_named(t, "DEMAND_difference_infrastructure_capped_tobacco = {", "DEMAND", "diff_capped"), t := block_named(t, "DEMAND_difference_tobacco = {", "DEMAND", "difference"), t := block_named(t, "DEMAND_country_tobacco = {", "DEMAND", "country"), block_named(t, "DEMAND_shortage_country_tobacco = {", "DEMAND", "shortage_country"))[-1])

edit("common/script_values/PRICE_svalues.txt", lambda t: (t := block_named(t, "global_mean_price_tobacco = {", "PRICE", "global_mean_price"), block_named(t, "PRICE_global_mean_tobacco = {", "PRICE", "price_global_mean"))[-1])

edit("common/script_values/AI_svalues.txt", lambda t: block_named(t, "AI_root_scope_unit_price_sqrt_tobacco = {", "AI", "unit_price_sqrt"))

edit("common/script_values/TRADE_svalues.txt", lambda t: (
    t := block_named(t, "TRADE_governorship_export_threshold_tobacco = {", "TRADE", "export_threshold"),
    t := block_named(t, "TRADE_governorship_export_cap_tobacco = {", "TRADE", "export_cap"),
    t := block_named(t, "TRADE_governorship_for_export_internal_tobacco = {", "TRADE", "for_export_internal"),
    t := block_named(t, "TRADE_governorship_for_export_tobacco = {", "TRADE", "for_export"),
    t := block_named(t, "TRADE_cash_balance_tobacco = {", "TRADE", "cash_balance"),
    t := block_named(t, "TRADE_total_expenditure_tobacco = {", "TRADE", "total_expenditure"),
    t := block_named(t, "TRADE_total_revenue_tobacco = {", "TRADE", "total_revenue"),
    block_named(t, "TRADE_governorship_cash_balance_tobacco = {", "TRADE", "gov_cash_balance"))[-1])

edit("common/script_values/WEALTH_svalues.txt", lambda t: (
    t := list_insert_all(t, "\tadd = var:country_unit_price_tobacco", "WEALTH", "unit_price_sum", 1),
    block_named(t, "WEALTH_tobacco_durability = {", "WEALTH", "durability"))[-1])

edit("common/script_values/INCOME_svalues.txt", lambda t: income_addchain(t, "INCOME", "excise_chain"))

edit("common/script_values/DEMAND_food_svalues.txt", lambda t: list_insert_all(t, "\tadd = GOODS_governorship_tobacco_produced", "DEMAND_food", "food_add", 1))

edit("common/scripted_effects/se_GOODS.txt", lambda t: (
    t := block_ifelse_unit(t, "has_variable = produces_tobacco", "se_GOODS", "stockpile_init"),
    t := block_enclosing_all(t, "goods = tobacco\n\t\tif_true = produces_tobacco", "se_GOODS", "update_produces", 1),
    block_enclosing_all(t, "do_if = produces_tobacco\n\t\tamount = GOODS_governorship_tobacco_produced", "se_GOODS", "produce_call", 1))[-1])

edit("common/scripted_effects/se_TRADE.txt", lambda t: (
    t := block_enclosing_all(t, "name = local_internal_revenue_cut_tobacco", "se_TRADE", "rev_cut", 1),
    t := block_enclosing_all(t, "name = internal_stockpile_cut_percentage_tobacco", "se_TRADE", "stock_cut", 1),
    list_insert_all(t, "\t\t\t\t\tvar:$tradegood$_name = flag:tobacco", "se_TRADE", "macro_name_cmp", 1))[-1])

edit("common/scripted_effects/se_PRICE.txt", lambda t: list_insert_all(t, "PRICE_factor_raw_input_costs_tobacco = {}", "se_PRICE", "raw_input", 1))

edit("common/scripted_effects/se_DEMAND.txt", lambda t: list_insert_all(t, "\tDEMAND_set_demand_from_luxury = { tradegood = tobacco }", "se_DEMAND", "set_demand", 2))

edit("common/scripted_effects/se_GLOBALTRADE_split.txt", lambda t: list_insert_all(t, "flag:$tradegood$ = flag:tobacco", "se_GLOBALTRADE", "macro_flag_cmp", 2))

edit("common/scripted_effects/se_PURCHASE.txt", lambda t: block_enclosing_all(t, "tradegood = tobacco ", "se_PURCHASE", "check_shopping", 2))

edit("common/scripted_effects/se_SELL.txt", lambda t: block_enclosing_all(t, "\t\ttradegood = tobacco", "se_SELL", "internal_cut", 2))

edit("common/scripted_effects/se_TRADE_new.txt", lambda t: block_enclosing_all(t, "tradegood = tobacco", "se_TRADE_new", "save_prev_demand", 1))

edit("common/scripted_triggers/00_resource_building_potential.txt", lambda t: list_insert_all(t, "\t\ttrade_goods = tobacco", "resbuild", "potential", 1))

edit("common/scripted_triggers/00_trade_scripted_triggers.txt", lambda t: list_insert_all(t, "        flag:$tradegood$ = flag:tobacco", "trade_trig", "flag_cmp", 1))

edit("common/modifiers/00_cultural_modifiers.txt", lambda t: (
    t := block_named(t, "fascination_with_tobacco = {", "cultmod", "fascination"),
    block_named(t, "taboo_with_tobacco = {", "cultmod", "taboo"))[-1])

# customizable loc: two custom_loc blocks + the tracker if-else chain + two trade_goods lists
edit("common/customizable_localization/000_ECON_loc.txt", lambda t: (
    t := block_named(t, "internal_trade_scope_custom_loc_tobacco = {", "ECONloc", "internal_scope"),
    t := block_enclosing_all(t, "localization_key = tracker_price_tobacco_expensive", "ECONloc", "tracker_exp", 1),
    t := block_enclosing_all(t, "localization_key = tracker_price_tobacco_cheap", "ECONloc", "tracker_cheap", 1),
    list_insert_all(t, "                trade_goods = tobacco", "ECONloc", "resbuild_lists", 2))[-1])

# injector hypercomplex lists (4 files) — insert 5 crop entries after the tobacco entry
INJ_ENTRY = "\t\t$PREFIX$tobacco$SUFFIX$ = {\n\t\t\t$APPLY$ = {\n\t\t\t\t$KEY$ = tobacco\n\t\t\t\t$EXTRA_KEY$ = $EXTRA_ARG$\n\t\t\t}\n\t\t}"
edit("common/scripted_effects/zz_tradegoods_injector.txt", lambda t: block_enclosing_all(t, "$KEY$ = tobacco", "inj_tg", "entry", 1))
edit("common/scripted_effects/zz_tradegood_injector.txt", lambda t: block_enclosing_all(t, "$KEY$ = tobacco", "inj_tgn", "entry", 1))
edit("common/scripted_effects/zz_luxury_goods_injector.txt", lambda t: block_enclosing_all(t, "$KEY$ = tobacco", "inj_lux", "entry", 1))
edit("common/scripted_effects/zz_tradegood_luxury_injector.txt", lambda t: block_enclosing_all(t, "$KEY$ = tobacco", "inj_txl", "entry", 1))

# =====================================================================================
# VERIFY braces vs baseline, then flush (unless dry)
print("\n--- brace verification ---")
for p, newt in OUT.items():
    net = newt.count("{") - newt.count("}")
    base = BASELINE[p]
    status = "OK" if net == base else "!!!! MISMATCH"
    print(f"  {status}  base={base:+d} now={net:+d}  {p}")
    if net != base:
        raise SystemExit("ABORT: brace mismatch, nothing written")

def _orig_bytes(p):
    with open(os.path.join(ROOT, p), "rb") as f:
        return f.read()

if DRY:
    print("\nDRY RUN — no files written.")
else:
    # CRITICAL: preserve each file's ORIGINAL byte convention (BOM + CRLF/LF).
    # Many of these files are UTF-8-with-BOM and/or CRLF; a naive text write flips
    # EVERY line and produces a catastrophic whole-file diff. Detect + re-apply.
    for p, newt in OUT.items():
        orig = _orig_bytes(p)
        had_bom = orig[:3] == b"\xef\xbb\xbf"
        had_crlf = b"\r\n" in orig
        body = newt.replace("\r\n", "\n")               # normalize working copy to LF
        if newt[:1] == "﻿":                          # strip any decoded BOM char
            pass  # io.open with utf-8-sig already stripped it on read
        data = body.replace("\n", "\r\n") if had_crlf else body
        raw = data.encode("utf-8")
        if had_bom and raw[:3] != b"\xef\xbb\xbf":
            raw = b"\xef\xbb\xbf" + raw
        with open(os.path.join(ROOT, p), "wb") as f:
            f.write(raw)
    print("\nWROTE", len(OUT), "files (BOM/EOL preserved).")

print("\n--- change log ---")
for f, d in changes:
    print(f"  {f}: {d}")
