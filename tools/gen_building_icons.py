#!/usr/bin/env python3
"""
gen_building_icons.py — [buildings-research 2026-07-27 follow-up] bespoke 200x200
building icons for the 37 new Qing/industrial buildings (commit 1ea45ce52).

Building icons resolve PURELY by filename: gfx/interface/icons/buildings/<building_key>.dds
(buildings have no `icon=` field). A missing file => engine placeholder. All 37 new
keys shipped without art, so all 37 showed placeholders in the boot test.

Pipeline (same as the existing bespoke Qing building icons):
  Wikimedia Commons search (curated, subject-specific query) -> center-crop ->
  200x200 -> BGRA8 DDS (donor = an existing legacy-BGRA8 building icon).

Each query is hand-picked to a concrete historical subject so the 200px icon reads
as the RIGHT thing (e.g. the Hanyang Ironworks, not a generic "steel works").
Idempotent: skips a key whose .dds already exists (delete to regenerate).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_wm import fetch
from dds_icon import convert, probe

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "gfx", "interface", "icons", "buildings")
SRCDIR = "/tmp/bldsrc"
# an existing legacy-BGRA8 (pfflags 0x41) building icon => exact format match
DONOR  = os.path.join(OUTDIR, "qing_salt_yard_building.dds")

# key -> Wikimedia Commons search query (concrete historical subject)
QUERIES = {
    # --- Industry (China-specific) ---
    "qing_steel_works_building":       "Hanyang Iron Works",
    "qing_textile_mill_building":      "cotton mill 19th century interior",
    "qing_machine_works_building":     "Jiangnan Arsenal Shanghai",
    "qing_navy_yard_building":         "Foochow Arsenal",
    "qing_coal_mine_building":         "Kaiping coal mine",
    "qing_telegraph_building":         "telegraph office 19th century",
    "qing_tongwen_guan_building":      "Tongwen Guan Peking",
    "qing_imperial_university_building": "Imperial University of Peking",
    # --- Industry (generic worldwide) ---
    "IND_coal_mine_building":          "coal mine pithead Victorian",
    "IND_blast_furnace_building":      "blast furnace 19th century ironworks",
    "IND_electric_plant_building":     "electric power station 1890s dynamo",
    "IND_gasworks_building":           "Victorian gasworks gasometer",
    # --- Garrison / military ---
    "qing_banner_garrison_building":   "Manchu banner garrison Manchu city",
    "qing_horse_pasture_building":     "Mongolian horse herd grassland",
    "qing_green_standard_post_building": "Qing dynasty soldiers Green Standard Army",
    "qing_coastal_battery_building":   "Chinese coastal fort cannon battery Qing",
    "qing_military_colony_building":   "Qing military agricultural colony Xinjiang",
    # --- Agriculture / hydraulic ---
    "qing_river_conservancy_building": "Yellow River dike flood control China",
    "qing_dujiangyan_building":        "Dujiangyan irrigation system",
    "qing_karez_building":             "karez qanat Turpan underground irrigation",
    "qing_fishpond_dyke_building":     "mulberry dyke fish pond Pearl River delta",
    "qing_polder_building":            "rice paddy terraces Yangtze delta",
    "qing_community_granary_building": "Chinese granary storehouse historic",
    # --- Scholarship ---
    "qing_hanlin_academy_building":    "Hanlin Academy",
    "qing_guozijian_building":         "Guozijian Imperial College Beijing",
    "qing_examination_hall_building":  "Nanjing examination hall Jiangnan Gongyuan",
    # --- Commerce / fiscal ---
    "qing_mint_building":              "Chinese cash coins Qing dynasty mint",
    "qing_draft_bank_building":        "Rishengchang draft bank Pingyao",
    "qing_guild_hall_building":        "Chinese guild hall huiguan historic",
    "qing_tribute_depot_building":     "Grand Canal granary depot China",
    "qing_likin_station_building":     "Qing dynasty customs barrier tax station",
    "qing_imperial_bank_building":     "Imperial Bank of China Shanghai historic building",
    # --- Religion ---
    "qing_temple_of_heaven_building":  "Temple of Heaven Beijing",
    "qing_ancestral_temple_building":  "Taimiao Imperial Ancestral Temple Beijing",
    "qing_confucian_temple_building":  "Temple of Confucius Beijing",
    "qing_gelug_monastery_building":   "Tibetan Buddhist monastery Gelug",
    "qing_great_mosque_building":      "Great Mosque of Xian",
}

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(SRCDIR, exist_ok=True)
    logpath = "/tmp/building_icons.log"
    ok = skip = err = 0
    with open(logpath, "w") as log:
        for key, q in QUERIES.items():
            out = os.path.join(OUTDIR, key + ".dds")
            if os.path.exists(out):
                skip += 1; log.write(f"{key}\tSKIP (exists)\n"); continue
            src = os.path.join(SRCDIR, key + ".jpg")
            try:
                if not os.path.exists(src):
                    _, desc = fetch(("search", q), src, width=360)
                else:
                    desc = "cached"
                convert(src, out, like=DONOR)
                log.write(f"{key}\t{q}\t{desc}\tOK\n")
                print(f"OK   {key:40s} <- {q}")
                ok += 1
            except Exception as e:
                log.write(f"{key}\t{q}\tERR\t{e}\n")
                print(f"ERR  {key:40s} {e}")
                err += 1
    print(f"\n--- ok={ok} skip={skip} err={err}  log={logpath}")

if __name__ == "__main__":
    main()
