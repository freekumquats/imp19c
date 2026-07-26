#!/usr/bin/env python3
"""Bespoke military-tradition node icons (00_manchu / 00_napoleon / 00_qing).
Writes gfx/interface/icons/military_traditions/<nodekey>.dds (198x72 BGRA8 donor) and
repoints each icon=/image= line to its node key."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from icon_common import ROOT, load_loc, process_keyed_file

TRAD_DIR = os.path.join(ROOT, "gfx", "interface", "icons", "military_traditions")
SRC      = os.path.join(ROOT, "art_src", "tradition")
LOG      = os.path.join(ROOT, "tools", "tradition_icon_log.tsv")

def donor():
    c = sorted(glob.glob(os.path.join(TRAD_DIR, "arabic_*.dds")))
    return c[0] if c else os.path.join(TRAD_DIR, "arabic_african_path_5.dds")

FILES_HINTS = [
    ("common/military_traditions/00_manchu.txt",   "Qing dynasty Qianlong military campaign"),
    ("common/military_traditions/00_napoleon.txt", "Napoleonic Grande Armee"),
    ("common/military_traditions/00_qing.txt",     "Qing dynasty army banner soldier"),
]

def main():
    loc = load_loc(); d = donor()
    with open(LOG, "w", encoding="utf-8") as log:
        log.write("file\tkey\ttitle\tquery\tsource\tstatus\n")
        for rel, hint in FILES_HINTS:
            fp = os.path.join(ROOT, rel)
            if not os.path.exists(fp):
                print("skip missing", rel); continue
            print("==", os.path.basename(rel))
            process_keyed_file(fp, loc, TRAD_DIR, d, SRC, log, hint=hint, quoted=False)
    print("done ->", LOG)

if __name__ == "__main__":
    main()
