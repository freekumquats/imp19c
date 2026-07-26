#!/usr/bin/env python3
"""qa_fixes.py — re-fetch + re-convert the icons flagged as off-concept/poor in the visual
QA pass, using curated concept-appropriate queries. Forces a fresh fetch (removes cached
art_src) and overwrites the .dds in place. No repointing needed (keys already wired)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def g(*p): return os.path.join(ROOT, "gfx", "interface", *p)
def trad_donor(): return sorted(glob.glob(g("icons","military_traditions","arabic_*.dds")))[0]

# (out_dds, donor, query)  — grouped by category
FIXES = []
def add(out, donor, q): FIXES.append((out, donor, q))

TD = None  # set in main
MENU = g("icons","menu_buttons","menu_trade.dds")
TRADE= g("icons","tradegoods","coal.dds")
BLDG = g("icons","buildings","EDU_school.dds")
MOD  = g("icons","modifiers","commerce_value.dds")

def build():
    global TD; TD = trad_donor()
    # --- trade goods ---
    add(g("icons","tradegoods","potato.dds"),      TRADE, "raw potatoes pile")
    add(g("icons","tradegoods","peanut.dds"),      TRADE, "shelled peanuts pile")
    # --- panels ---
    add(g("icons","menu_buttons","qing_southern_study.dds"), MENU, "Chinese scholar calligraphy painting")
    add(g("icons","menu_buttons","qing_justice.dds"),        MENU, "Chinese imperial magistrate court")
    add(g("icons","menu_buttons","qing_deliberative.dds"),   MENU, "Qing dynasty officials meeting portrait")
    add(g("icons","menu_buttons","qing_population.dds"),     MENU, "crowded ancient Chinese city painting")
    # --- buildings (clear wrong matches) ---
    add(g("icons","buildings","qing_dike_building.dds"),            BLDG, "Yellow River flood dike China")
    add(g("icons","buildings","qing_embassy_building.dds"),         BLDG, "19th century diplomatic legation building Beijing")
    add(g("icons","buildings","qing_frontier_colony_building.dds"), BLDG, "Chinese farmers rice field terraces")
    add(g("icons","buildings","qing_frontier_fort_building.dds"),   BLDG, "Chinese fortress watchtower wall")
    add(g("icons","buildings","qing_salt_yard_building.dds"),       BLDG, "sea salt evaporation ponds")
    # --- modifier-cost glyphs (clear document/wrong matches) ---
    add(g("icons","modifiers","qing_customs_house_building_cost.dds"), MOD, "Chinese silver ingot coins")
    add(g("icons","modifiers","qing_yamen_building_cost.dds"),         MOD, "red Chinese seal stamp")
    add(g("icons","modifiers","qing_canal_depot_building_cost.dds"),   MOD, "wooden cargo barge boat")
    # --- military traditions (military-appropriate concept imagery) ---
    T = g("icons","military_traditions","%s.dds")
    trad = {
      "napoleon_bataillon_carre":"Napoleonic infantry square formation painting",
      "napoleon_baton":"marshal baton France ceremonial",
      "napoleon_brienne":"military cadet school artillery drill",
      "napoleon_grande_batterie":"Napoleonic cannon artillery battery",
      "napoleon_manoeuvre":"Napoleon battle map campaign painting",
      "napoleon_start":"Napoleonic Grande Armee soldiers painting",
      "napoleon_baton_de_marechal":"marshal baton France",
      "qing_banner_bondservants":"Qing dynasty Manchu official portrait",
      "qing_banner_capstone":"Manchu Eight Banners soldier armor",
      "qing_banner_garrison":"Qing dynasty banner garrison soldiers",
      "qing_banner_niru":"Manchu banner officer portrait",
      "qing_banner_start":"Manchu Eight Banners cavalry",
      "qing_banner_vanguard":"Qing dynasty elite soldier armor",
      "qing_frontier_defence_tradition":"Qing frontier fort watchtower",
      "qing_frontier_native":"Qing dynasty frontier soldiers",
      "qing_frontier_pickets":"watchtower frontier steppe",
      "qing_frontier_rotation":"Qing dynasty garrison soldiers marching",
      "qing_frontier_start":"Qing frontier fortress Xinjiang",
      "qing_green_battalion":"Green Standard Army Qing soldier",
      "qing_green_garrison":"Qing dynasty infantry soldiers",
      "qing_green_rattan":"rattan shield soldier",
      "qing_green_standard_tradition":"Green Standard Army Qing dynasty",
      "qing_mongol_capstone":"Mongolian cavalry horsemen",
      "qing_mongol_cavalry_tradition":"Mongolian mounted archer horse",
      "qing_mongol_khalkha":"Mongolian horsemen steppe",
      "qing_mongol_league":"Mongolian cavalry banner",
      "qing_mongol_raiders":"Mongolian mounted warriors",
      "qing_tributary_auxilia":"Qing dynasty auxiliary troops",
      "qing_tributary_capstone":"Qing dynasty tributary envoys",
      "qing_tributary_host":"Qing dynasty army assembled",
      "qing_tributary_levy_tradition":"Chinese tributary mission envoys",
      "qing_tributary_mobilis":"Qing dynasty soldiers marching",
      "qing_tributary_revenue":"Chinese tribute gifts silver",
      "qing_tributary_start":"Qing dynasty allied soldiers",
      "shiquan_laoren":"Qianlong Emperor portrait",
      "shiquan_start":"Qianlong Emperor military armor portrait",
      "shiquan_laoren_2":"Qianlong Emperor old age portrait",
    }
    for k,q in trad.items():
        p = T % k
        if os.path.exists(p):
            add(p, TD, q)

def main():
    build()
    log = os.path.join(ROOT,"tools","qa_fix_log.tsv")
    with open(log,"w",encoding="utf-8") as f:
        f.write("out\tquery\tsource\tstatus\n")
        for out, donor, q in FIXES:
            key = os.path.basename(out)[:-4]
            src = os.path.join(ROOT,"art_src","qafix",key+".jpg")
            os.makedirs(os.path.dirname(src), exist_ok=True)
            try:
                if os.path.exists(src): os.remove(src)
                _,desc = fetch(("search",q), src, width=400)
                convert(src, out, like=donor)
                f.write(f"{key}\t{q}\t{desc}\tOK\n"); print("OK",key)
            except Exception as e:
                f.write(f"{key}\t{q}\tERR\t{e}\n"); print("ERR",key,e)
    print("done ->", log)

if __name__=="__main__":
    main()
