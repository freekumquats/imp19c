#!/usr/bin/env python3
"""Bespoke mission-tree HEADER banners (624x120) + building modifier-COST glyphs (50x50).
Headers: write gfx/interface/missions/mission_image_<tree>.dds, repoint each file's
`header = mission_image_test` to it. Modifier-cost: write gfx/interface/icons/modifiers/<key>.dds
and repoint the `positive = "..."` line in 00_modifier_icons.txt."""
import os, sys, re, glob
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def g(*p): return os.path.join(ROOT, "gfx", "interface", *p)
SRC = os.path.join(ROOT, "art_src", "hdr"); os.makedirs(SRC, exist_ok=True)
LOG = os.path.join(ROOT, "tools", "hdrmod_icon_log.tsv")
HDR_DONOR = g("missions", "mission_image_test.dds")
MOD_DONOR = g("icons", "modifiers", "commerce_value.dds")

# tree file stem -> (header art key suffix, themed wide-banner query)
HEADERS = {
 "burma_war":       "Konbaung dynasty Burma war army",
 "central_asia":    "Central Asia steppe caravan mountains",
 "colonization":    "Pacific ocean sailing ship colony map",
 "himalaya_seasia": "Himalaya mountains monastery Tibet",
 "india":           "Mughal India fort Ganges",
 "japan":           "Meiji Japan army Sino-Japanese",
 "japan_preperry":  "Edo Japan Black Ships harbor",
 "nanyang":         "South China Sea junk overseas Chinese",
 "open_japan":      "treasure ship fleet Japan coast",
 "reform":          "late Qing parliament constitution assembly",
 "selfstrengthening":"Jiangnan Arsenal Qing steamship",
 "settle_frontier": "Mongolian Manchurian steppe frontier settlement",
 "summer_palace":   "Yuanmingyuan Summer Palace Beijing garden",
 "taiping":         "Taiping Heavenly Kingdom Nanjing rebellion",
 "treasure_fleet":  "Zheng He treasure ship Ming fleet",
 "xinjiang":        "Xinjiang Kashgar oasis Qing fort",
}

def do_headers(log):
    for stem, q in HEADERS.items():
        art_key = "mission_image_qing_" + stem
        out = g("missions", art_key + ".dds")
        src = os.path.join(SRC, stem + ".jpg")
        fp = os.path.join(ROOT, "common", "missions", f"qing_{stem}_missions.txt")
        if not os.path.exists(fp):
            log.write(f"HDR\t{stem}\t{q}\tERR\tmission file missing\n"); continue
        try:
            if not os.path.exists(out):
                if not os.path.exists(src):
                    _, desc = fetch(("search", q), src, width=640)
                else:
                    desc = "cached"
                convert(src, out, like=HDR_DONOR)
            else:
                desc = "exists"
            txt = open(fp, encoding="utf-8").read()
            new = txt.replace("header = mission_image_test", f"header = {art_key}", 1)
            if new != txt:
                open(fp, "w", encoding="utf-8").write(new)
            log.write(f"HDR\t{stem}\t{q}\t{desc}\tOK\n"); print("  OK hdr", stem)
        except Exception as e:
            log.write(f"HDR\t{stem}\t{q}\tERR\t{e}\n"); print("  ERR hdr", stem, e)

# modifier-cost glyph concept queries (small icons; from doc §3)
MODIFIERS = {
 "qing_silk_filature_building_cost":  "silk cocoon reeling",
 "qing_porcelain_kiln_building_cost": "porcelain vase blue white",
 "qing_tea_workshop_building_cost":   "green tea leaves",
 "qing_cotton_workshop_building_cost":"cotton boll textile",
 "qing_salt_yard_building_cost":      "salt crystals",
 "qing_customs_house_building_cost":  "customs seal stamp",
 "qing_yamen_building_cost":          "Chinese official seal chop",
 "qing_shuyuan_building_cost":        "Chinese scroll book calligraphy",
 "qing_granary_building_cost":        "rice grain sack",
 "qing_selfstr_wonder_building_cost": "steam engine machinery",
 "qing_dike_building_cost":           "river dike stone embankment",
 "qing_canal_depot_building_cost":    "canal barge grain",
 "qing_wall_section_building_cost":   "stone rampart wall",
}

MODFILE = os.path.join(ROOT, "common", "modifier_icons", "00_modifier_icons.txt")

def do_modifiers(log):
    if not os.path.exists(MODFILE):
        print("no modifier file"); return
    txt = open(MODFILE, encoding="utf-8").read()
    for key, q in MODIFIERS.items():
        out = g("icons", "modifiers", key + ".dds")
        src = os.path.join(SRC, "mod_" + key + ".jpg")
        try:
            if not os.path.exists(out):
                if not os.path.exists(src):
                    _, desc = fetch(("search", q), src, width=200)
                else:
                    desc = "cached"
                convert(src, out, like=MOD_DONOR)
            else:
                desc = "exists"
            # repoint: within the `<key> = { positive = "OLD" }` block, swap OLD to our art.
            art = f"gfx/interface/icons/modifiers/{key}.dds"
            pat = re.compile(r'(' + re.escape(key) + r'\s*=\s*\{\s*positive\s*=\s*)"[^"]+"', re.S)
            new = pat.sub(r'\1"' + art + '"', txt, count=1)
            if new != txt:
                txt = new
            log.write(f"MOD\t{key}\t{q}\t{desc}\tOK\n"); print("  OK mod", key)
        except Exception as e:
            log.write(f"MOD\t{key}\t{q}\tERR\t{e}\n"); print("  ERR mod", key, e)
    open(MODFILE, "w", encoding="utf-8").write(txt)

def main():
    with open(LOG, "w", encoding="utf-8") as log:
        log.write("kind\tkey\tquery\tsource\tstatus\n")
        print("== headers"); do_headers(log)
        print("== modifiers"); do_modifiers(log)
    print("done ->", LOG)

if __name__ == "__main__":
    main()
