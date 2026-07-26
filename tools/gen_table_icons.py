#!/usr/bin/env python3
"""
gen_table_icons.py — bespoke icons for the doc-table categories (panels, trade goods,
event pictures, modifier-cost glyphs, building-type icons, military traditions).

Each entry: (out_path, donor, query-or-url). Curated queries come from placeholder_icons.md
§2/§3/§3b/§4/§5/§6 concepts. Writes DDS via dds_icon.convert; GUI/def repointing is done by
a companion step (repoint_refs.py) so this file only produces art.

Idempotent: skips an out_path that already exists (unless --force).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def g(*p): return os.path.join(ROOT, "gfx", "interface", *p)
SRC = os.path.join(ROOT, "art_src", "table")
LOG = os.path.join(ROOT, "tools", "table_icon_log.tsv")
os.makedirs(SRC, exist_ok=True)

MENU   = g("icons", "menu_buttons", "menu_trade.dds")        # 50x50 shaped-alpha donor
TRADE  = g("icons", "tradegoods", "coal.dds")                # 50x50 shaped-alpha donor
BLDG   = g("icons", "buildings", "EDU_school.dds")           # 200x200 donor
MODIF  = g("icons", "modifiers", "commerce_value.dds")       # 50x50 shaped-alpha donor
EVENT  = g("event_window", "Event_senate_debate.dds")        # DXT donor (opaque)
def TRAD():
    import glob
    c = sorted(glob.glob(g("icons","military_traditions","arabic_*.dds")))
    return c[0] if c else g("icons","military_traditions","arabic_african_path_5.dds")

# ---- category tables: key -> (out_dds, donor, query) -----------------------------------
# ('D', url) forces a direct upload.wikimedia.org URL; ('S', q) does a Commons search.

PANELS = {
 # menu_buttons/qing_<panel>.dds  (repoint the .gui texture= line)
 "qing_zongli":        ("D","https://upload.wikimedia.org/wikipedia/commons/7/7e/Four_Members_of_the_Tsung-li_Yam%C3%AAn.jpg"),
 "qing_lifanyuan":     ("S","Lifan Yuan Qing court colonial affairs"),
 "qing_greatgame":     ("S","Great Game Central Asia 19th century map"),
 "qing_censorate":     ("S","Qing censor official portrait"),
 "qing_hanlin":        ("S","Hanlin Academy Beijing"),
 "qing_justice":       ("S","Qing dynasty court punishment yamen"),
 "qing_rites_ministry":("S","Qing dynasty ancestral rite ceremony"),
 "qing_southern_study":("S","Forbidden City study hall qing"),
 "qing_upper_study":   ("S","Qing palace school study"),
 "qing_deliberative":  ("S","Manchu Deliberative Council princes"),
 "qing_guard":         ("S","Qing imperial guard soldier"),
 "qing_war_ministry":  ("S","Qing Eight Banners military flag"),
 "qing_xinjiang":      ("D","https://upload.wikimedia.org/wikipedia/commons/7/71/Qing_dynasty_and_Xinjiang.jpg"),
 "qing_personnel":     ("S","Qing dynasty mandarin official portrait"),
 "qing_caravan":       ("S","Silk Road camel caravan Kashgar"),
 "qing_harem":         ("S","Qing dynasty imperial consort portrait"),
 "qing_household":     ("S","Forbidden City hall Beijing"),
 "qing_opium":         ("S","19th century Chinese opium den"),
 "qing_population":    ("S","Along the River During the Qingming Festival crowd"),
 "qing_princes":       ("S","Qing dynasty prince portrait"),
 "qing_revenue_ministry":("S","Chinese sycee silver ingot"),
 "qing_secretariat":   ("S","Grand Council Qing dynasty office"),
 "qing_works_ministry":("S","Grand Canal China engineering"),
}

TRADEGOODS = {
 "maize":        ("D","https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Corncobs.jpg/640px-Corncobs.jpg"),
 "sweet_potato": ("S","sweet potato tuber"),
 "potato":       ("S","potatoes tubers"),
 "peanut":       ("S","peanuts groundnuts"),
 "chili":        ("S","red chili peppers"),
 "porcelain":    ("S","Jingdezhen blue and white porcelain vase"),
 "rifles":       ("S","19th century percussion musket rifle"),
}

# building-TYPE icons (200x200) at gfx/interface/icons/buildings/<key>.dds — currently stopgap-copied
BUILDINGS = {
 "qing_shuyuan_building":        ("S","Chinese academy shuyuan hall"),
 "qing_yamen_building":          ("S","Chinese yamen government office building"),
 "qing_granary_building":        ("S","Chinese granary storehouse"),
 "qing_customs_house_building":  ("S","Chinese maritime customs house building"),
 "qing_silk_filature_building":  ("S","silk reeling filature"),
 "qing_porcelain_kiln_building": ("S","Jingdezhen porcelain kiln"),
 "qing_tea_workshop_building":   ("S","Chinese tea processing workshop"),
 "qing_cotton_workshop_building":("S","cotton textile mill 19th century"),
 "qing_salt_yard_building":      ("S","Chinese salt evaporation works"),
 "qing_opium_poppy_farm_building":("S","opium poppy field"),
 "qing_selfstr_wonder_building": ("S","Jiangnan Arsenal Shanghai"),
 "qing_dike_building":           ("S","Yellow River dike embankment"),
 "qing_grand_canal_building":    ("S","Grand Canal China"),
 "qing_canal_depot_building":    ("S","Chinese canal grain barge"),
 "qing_great_wall_building":     ("S","Great Wall of China"),
 "qing_wall_section_building":   ("S","Great Wall of China rampart"),
 "qing_embassy_building":        ("S","19th century legation embassy building"),
 "qing_foreign_concession_building":("S","Shanghai foreign concession bund"),
 "qing_foreign_works_building":  ("S","19th century arsenal machine works China"),
 "qing_frontier_colony_building":("S","tuntian military agricultural colony"),
 "qing_frontier_fort_building":  ("S","Qing frontier fort Xinjiang"),
 "qing_mission_cathedral_building":("S","cathedral in China 19th century"),
 "qing_mission_public_building": ("S","Christian church China 19th century"),
 "qing_mission_underground_building":("S","secret chapel prayer"),
 "qing_treaty_port_building":    ("S","treaty port China waterfront"),
 "military_depot_building":      ("S","military supply depot warehouse"),
 "row_manufactory_building":     ("S","19th century factory manufactory"),
 "row_plantation_building":      ("S","colonial plantation"),
}

EVENTS = {  # event_window/qing_<alias>.dds  (repoint picture=)
 "qing_senate":     ("S","parliament chamber assembly hall"),
 "qing_navy":       ("S","age of sail naval battle warship"),
 "qing_greek_siege":("S","walled city under siege"),
}

def main():
    jobs = [
        (PANELS,     g("icons","menu_buttons"),        MENU),
        (TRADEGOODS, g("icons","tradegoods"),          TRADE),
        (BUILDINGS,  g("icons","buildings"),           BLDG),
        (EVENTS,     g("event_window"),                EVENT),
    ]
    with open(LOG,"w",encoding="utf-8") as log:
        log.write("key\tquery\tsource\tstatus\n")
        for table, outdir, donor in jobs:
            print("==", os.path.basename(outdir), f"({len(table)})")
            for key,(kind,val) in table.items():
                out = os.path.join(outdir, key + ".dds")
                src = os.path.join(SRC, key + ".jpg")
                try:
                    spec = ("direct",val) if kind=="D" else ("search",val)
                    if not os.path.exists(src):
                        _,desc = fetch(spec, src, width=400)
                    else:
                        desc="cached"
                    convert(src, out, like=donor)
                    log.write(f"{key}\t{val}\t{desc}\tOK\n"); print(f"  OK {key}")
                except Exception as e:
                    log.write(f"{key}\t{val}\tERR\t{e}\n"); print(f"  ERR {key}: {e}")
    print("done ->", LOG)

if __name__ == "__main__":
    main()
