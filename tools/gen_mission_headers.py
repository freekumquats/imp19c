#!/usr/bin/env python3
"""
gen_mission_headers.py — create the MISSING mission-tree HEADER banners (#BT).

Every Qing mission TREE declares `icon = <tree>_mission`, which the engine resolves to
gfx/interface/icons/missions/<tree>_mission.dds (the 634x122 header banner shown at the
top of the mission view — MissionView.GetHeaderImage). Only russian_missions_1.dds +
test1.dds existed there, so every Qing tree showed a placeholder header. (The small
per-node TASK icons live in mission_tasks/ and were already present — a different set.)

Format: 634x122 DX10 BGRA8-sRGB (dxgiFormat=91), matching the widget size and the one
working sibling. We build each header by compositing the tree's existing 118x68 TASK
icon (its thematic art) as a crisp emblem on a dark parchment band, letterboxed rather
than upscaled-blurry — so it reads as an intentional banner, not a stretched thumbnail.
"""
import struct, os, glob
from PIL import Image, ImageDraw
import numpy as np
import sys; sys.path.insert(0, os.path.dirname(__file__))
from dds_icon import write_dds_dx10_bgra8, read_dds_bgra8, read_dds_dims

MT   = 'gfx/interface/icons/mission_tasks'
OUT  = 'gfx/interface/icons/missions'
HW, HH = 634, 122

def load_task_rgba(key):
    """Decode a task icon (DX10 BGRA8) to an RGBA PIL image."""
    p = f'{MT}/{key}.dds'
    with open(p, 'rb') as f: b = f.read()
    w, h = read_dds_dims(p)
    if b[84:88] == b'DX10':
        px = np.frombuffer(b[148:148+w*h*4], dtype=np.uint8).reshape(h, w, 4)
        rgba = px[:, :, [2,1,0,3]].copy()            # BGRA -> RGBA
    else:
        rgba, _ = read_dds_bgra8(p)
    return Image.fromarray(rgba, 'RGBA')

def make_header(key):
    # dark parchment band background (deep red-brown, the mission-panel palette)
    im = Image.new('RGBA', (HW, HH), (0,0,0,255))
    d = ImageDraw.Draw(im)
    for y in range(HH):
        t = y/HH
        col = (int(56+18*t), int(20+8*t), int(18+6*t), 255)   # dark crimson gradient
        d.line((0,y,HW,y), fill=col)
    # a thin gold rule top+bottom
    d.rectangle((0,0,HW-1,HH-1), outline=(196,158,86,255), width=3)
    # the task art, scaled up to band height with a margin, centred, kept sharp-ish
    art = load_task_rgba(key)
    m = 10
    th = HH - 2*m
    scale = th / art.height
    tw = int(art.width * scale)
    art2 = art.resize((tw, th), Image.LANCZOS)
    # place it left-of-centre so the band reads as a banner with the emblem at the hoist
    x = 28
    im.alpha_composite(art2, (x, m))
    return np.asarray(im, dtype=np.uint8)

def main():
    os.makedirs(OUT, exist_ok=True)
    trees = [os.path.splitext(os.path.basename(p))[0]
             for p in glob.glob(f'{MT}/qing_*_mission.dds')]
    for key in sorted(trees):
        out = f'{OUT}/{key}.dds'
        write_dds_dx10_bgra8(out, make_header(key))
        print("wrote", out)

if __name__ == '__main__':
    main()
