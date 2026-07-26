#!/usr/bin/env python3
"""qa_fixes_tradition.py — re-fetch ALL military-tradition node icons with curated,
verified concept-appropriate battle/military-painting queries (the 198x72 banner aspect
made auto-derived queries unreliable). Each of the 5 Qing trees + 2 campaign trees gets a
themed query pool; nodes cycle through their tree's pool so sibling banners differ.
Overwrites in place (keys already wired)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDIR = os.path.join(ROOT, "gfx", "interface", "icons", "military_traditions")
DON  = sorted(glob.glob(os.path.join(TDIR, "arabic_*.dds")))[0]

# themed, verified-good query pools (each returns a concept-accurate painting/photo)
POOLS = {
 "qing_banner":   ["Battle of Oroi-Jalatu","Victory at Khorgos Battle Copper Print Qianlong",
                   "Qing dynasty cavalry battle Nien","Qianlong campaign battle engraving",
                   "Manchu Qing dynasty soldier photograph 1874"],
 "qing_green":    ["Qing dynasty cavalry battle Nien","Qing dynasty soldiers photograph Beijing",
                   "Battle of Oroi-Jalatu","Qianlong campaign battle engraving"],
 "qing_mongol":   ["Mongol cavalry battle painting","Battle of Oroi-Jalatu",
                   "Qing dynasty cavalry battle Nien","Victory at Khorgos Battle Copper Print"],
 "qing_frontier": ["Qianlong campaign battle engraving","Battle of Oroi-Jalatu",
                   "Jiayuguan fort great wall","Qing dynasty frontier soldiers photograph"],
 "qing_tributary":["万国来朝图 tribute","Qing dynasty court ceremony painting",
                   "Qianlong emperor southern inspection scroll","Qing dynasty envoys painting"],
 "shiquan":       ["Victory at Khorgos Battle Copper Print","Battle of Oroi-Jalatu",
                   "Qianlong campaign battle engraving","Qianlong emperor military armor portrait",
                   "Qing dynasty cavalry battle Nien"],
 "manchu":        ["Qianlong emperor military armor portrait","Victory at Khorgos Battle Copper Print"],
 "napoleon":      ["Battle of Austerlitz painting Gerard","Charge of the French Cuirassiers Waterloo",
                   "Napoleon Old Guard Waterloo painting","Napoleonic artillery battery Hanau",
                   "Grande Armee marshal full dress uniform","French infantry Napoleonic painting"],
}

def pool_for(key):
    for pref in ("qing_banner","qing_green","qing_mongol","qing_frontier","qing_tributary",
                 "shiquan","manchu","napoleon"):
        if key.startswith(pref):
            return POOLS[pref]
    return POOLS["shiquan"]

def main():
    files = sorted(glob.glob(os.path.join(TDIR, "*.dds")))
    # only our bespoke tradition nodes (skip borrowed arabic_/indian_/etc donors)
    ours = [f for f in files if os.path.basename(f).startswith(
        ("qing_banner","qing_green","qing_mongol","qing_frontier","qing_tributary",
         "shiquan","manchu","napoleon"))]
    log = os.path.join(ROOT,"tools","qa_fix_trad_log.tsv")
    with open(log,"w",encoding="utf-8") as f:
        f.write("key\tquery\tsource\tstatus\n")
        for i,fp in enumerate(ours):
            key = os.path.basename(fp)[:-4]
            pool = pool_for(key)
            q = pool[i % len(pool)]
            src = os.path.join(ROOT,"art_src","qafixt",key+".jpg")
            os.makedirs(os.path.dirname(src),exist_ok=True)
            try:
                if os.path.exists(src): os.remove(src)
                _,desc = fetch(("search",q), src, width=400)
                convert(src, fp, like=DON)
                f.write(f"{key}\t{q}\t{desc}\tOK\n"); print("OK",key)
            except Exception as e:
                f.write(f"{key}\t{q}\tERR\t{e}\n"); print("ERR",key,str(e)[:60])
    print("done ->",log, f"({len(ours)} nodes)")

if __name__=="__main__":
    main()
