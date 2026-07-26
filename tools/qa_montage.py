#!/usr/bin/env python3
"""qa_montage.py — render review montages of the bespoke icons for visual QA.
Composites each icon over dark grey with its key labelled, in a grid, one PNG per group.
Usage: qa_montage.py <group>   where group in {mission,panel,trade,building,tradition,header,modifier,event}
"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from dds_icon import read_dds_bgra8, is_uncompressed_bgra8
from PIL import Image, ImageDraw
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def g(*p): return os.path.join(ROOT, "gfx", "interface", *p)

GROUPS = {
 "mission":  (g("icons","mission_tasks"),      "qing_*.dds",  118,68),
 "panel":    (g("icons","menu_buttons"),       "qing_*.dds",  50,50),
 "trade":    (None, None, 50,50),   # explicit list below
 "building": (g("icons","buildings"),          "qing_*.dds",  96,96),
 "tradition":(g("icons","military_traditions"),"*.dds",       120,44),
 "header":   (g("missions"),                   "mission_image_qing_*.dds", 200,40),
 "modifier": (g("icons","modifiers"),          "qing_*.dds",  50,50),
 "event":    (g("event_window"),               "qing_*.dds",  160,64),
}
TRADE_KEYS = ["maize","sweet_potato","potato","peanut","chili","porcelain","rifles"]
TRAD_PREFIX = ("shiquan","manchu","napoleon","qing_banner","qing_green","qing_mongol","qing_frontier","qing_tributary")

def load_icon(path, w, h):
    if not is_uncompressed_bgra8(path):
        return None
    rgba,_ = read_dds_bgra8(path)
    return Image.fromarray(rgba,"RGBA").convert("RGB").resize((w,h))

def build(group):
    spec = GROUPS[group]
    outdir, pat, w, h = spec
    if group == "trade":
        files = [g("icons","tradegoods",k+".dds") for k in TRADE_KEYS]
    elif group == "tradition":
        files = [f for f in sorted(glob.glob(os.path.join(outdir, pat)))
                 if os.path.basename(f).startswith(TRAD_PREFIX)]
    else:
        files = sorted(glob.glob(os.path.join(outdir, pat)))
    files = [f for f in files if os.path.basename(f) not in ("test1.dds","test2.dds","test3.dds")]
    if not files:
        print("no files for", group); return
    cols = 6 if w<=60 else (5 if w<=130 else 4)
    lab = 14
    cw, ch = w+12, h+lab+8
    rows = (len(files)+cols-1)//cols
    canvas = Image.new("RGB", (cols*cw, rows*ch), (35,35,38))
    d = ImageDraw.Draw(canvas)
    for i,fp in enumerate(files):
        im = load_icon(fp, w, h)
        x=(i%cols)*cw+6; y=(i//cols)*ch+4
        if im: canvas.paste(im,(x,y))
        else:  d.rectangle([x,y,x+w,y+h], outline=(200,60,60))
        key=os.path.basename(fp)[:-4].replace("mission_image_","").replace("_building","")
        d.text((x, y+h+1), key[:22], fill=(200,200,200))
    out=os.path.join(ROOT,"tools",f"qa_{group}.png")
    canvas.save(out); print("wrote", out, f"({len(files)} icons, {rows}x{cols})")

if __name__=="__main__":
    grp = sys.argv[1] if len(sys.argv)>1 else "mission"
    if grp=="all":
        for gname in GROUPS: build(gname)
    else:
        build(grp)
