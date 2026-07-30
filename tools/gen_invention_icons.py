#!/usr/bin/env python3
"""
gen_invention_icons.py — [#118] one filled, DISTINCT icon per invention key.

The 1763 technology rework replaced vanilla's classical inventions wholesale, so every
mod invention key (260 of them across common/inventions/*.txt) has NO base-game icon at
INVENTIONS_ICON_PATH (gfx/interface/buttons/inventions). GetInventionIcon therefore fell
back to raw engine coloured-shape placeholders — and #81 papered over that by forcing one
generic per-tree glyph, which made every node in a tree look identical. #118 reverts to
GetInventionIcon (per-node art) and this script SUPPLIES that art: a real 50x50 BGRA8 icon
for every invention key, tinted by its tech domain and stamped with a deterministic per-key
emblem so no two nodes look the same and nothing renders as a bare placeholder.

Format matches the shipped idea-group icons: 50x50 uncompressed BGRA8 (pfflags 0x41) — the
exact form gen_modifier_icons.write_bgra8 already produces (reused here).

Domains (by source file): military / civic / oratory / religious / qing.
Run:  python tools/gen_invention_icons.py           (skips existing)
      python tools/gen_invention_icons.py --force   (rewrite all)
"""
import os, sys, re, glob, struct
from PIL import Image, ImageDraw
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV_DIR = os.path.join(ROOT, "common", "inventions")
OUT = os.path.join(ROOT, "gfx", "interface", "buttons", "inventions")
GFX_DIR = os.path.join(ROOT, "interface")
GFX_FILE = os.path.join(GFX_DIR, "imperatrix_inventions.gfx")
PX = 50; S = 4  # supersample

# ---- DDS writer (same header as gen_modifier_icons.write_bgra8) ------------------------
def write_bgra8(path, rgba):
    h, w, _ = rgba.shape; pitch = w * 4
    hdr = bytearray(124)
    struct.pack_into('<I', hdr, 0, 124)
    struct.pack_into('<I', hdr, 4, 0x1 | 0x2 | 0x4 | 0x8 | 0x1000)
    struct.pack_into('<I', hdr, 8, h); struct.pack_into('<I', hdr, 12, w); struct.pack_into('<I', hdr, 16, pitch)
    struct.pack_into('<I', hdr, 24, 1)
    struct.pack_into('<I', hdr, 72, 32); struct.pack_into('<I', hdr, 76, 0x1 | 0x40)
    struct.pack_into('<I', hdr, 84, 32)
    struct.pack_into('<I', hdr, 88, 0x00FF0000); struct.pack_into('<I', hdr, 92, 0x0000FF00)
    struct.pack_into('<I', hdr, 96, 0x000000FF); struct.pack_into('<I', hdr, 100, 0xFF000000)
    struct.pack_into('<I', hdr, 104, 0x1000)
    bgra = rgba[:, :, [2, 1, 0, 3]].astype(np.uint8)
    with open(path, 'wb') as f:
        f.write(b'DDS '); f.write(bytes(hdr)); f.write(bgra.tobytes())

# ---- domain palettes (base disc colour) ------------------------------------------------
DOMAIN_COL = {
    'military':  (150, 52, 46),    # martial red
    'civic':     (56, 96, 156),    # civic blue
    'oratory':   (150, 112, 40),   # oratory ochre
    'religious': (96, 72, 150),    # religious violet
    'qing':      (196, 158, 86),   # imperial gold
}
DOMAIN_FILE = {
    '00_martial_inventions.txt':  'military',
    '00_civic_inventions.txt':    'civic',
    '00_oratory_inventions.txt':  'oratory',
    '00_religious_inventions.txt':'religious',
    '00_qing_inventions.txt':     'qing',
}

def domain_of_key():
    """key -> domain, by which inventions file defines it."""
    m = {}
    for f in glob.glob(os.path.join(INV_DIR, "*.txt")):
        dom = DOMAIN_FILE.get(os.path.basename(f))
        if not dom:
            continue
        for line in open(f, encoding="utf-8"):
            # invention nodes sit one tab in; tolerate trailing whitespace after the brace
            # (e.g. "tech_cartography = {  ") and flexible spacing around '='.
            mt = re.match(r'^\t([a-z_0-9]+)\s*=\s*\{\s*$', line)
            if mt:
                m[mt.group(1)] = dom
    return m

def canvas():
    return Image.new('RGBA', (PX * S, PX * S), (0, 0, 0, 0))

def disc(d, col, m=0.05):
    b = (int(PX*S*m), int(PX*S*m), int(PX*S*(1-m)), int(PX*S*(1-m)))
    d.ellipse(b, fill=col + (255,), outline=(28, 28, 28, 255), width=max(2, int(PX*S*0.03)))

# [MO#9 2026-07-29] The old hash-rosette emblem() (+ its hashlib import) was removed — it was
# exactly the "generic graph/node" look this task replaces. gen() now draws a subject motif.

# ============================================================================
# [MO#9 2026-07-29] SUBJECT MOTIFS — replace the hash rosette (which read as a
# generic graph/node diagram) with a legible per-invention emblem, drawn on the
# existing tinted disc. Style matches the mod's traditions/deities/tradegoods
# icon families (a flat silhouette on a coloured disc); the domain tint is kept
# so within-domain nodes still read as a family, the motif carries the subject.
# Each motif_<name>(d, tint, c, r) uses only PIL primitives; c=centre, r≈working radius.
# ============================================================================
def _L(d, tint, pts, w):  # polyline helper
    for a, b in zip(pts, pts[1:]):
        d.line((a[0], a[1], b[0], b[1]), fill=tint, width=w)

def motif_war_banner(d, tint, c, r):
    w = max(3, int(r*0.10))
    d.line((c-int(r*0.1), c-r, c-int(r*0.1), c+r), fill=tint, width=w)                 # pole
    d.polygon([(c-int(r*0.1), c-r), (c+r, c-int(r*0.6)), (c+int(r*0.5), c-int(r*0.35)),
               (c+r, c-int(r*0.1)), (c-int(r*0.1), c-int(r*0.15))], fill=tint)         # pennant
def motif_rifle(d, tint, c, r):
    w = max(3, int(r*0.12))
    d.line((c-r, c+int(r*0.6), c+int(r*0.8), c-int(r*0.7)), fill=tint, width=w)        # barrel
    d.polygon([(c-r, c+int(r*0.6)), (c-int(r*0.5), c+r), (c-int(r*0.75), c+r)], fill=tint)  # stock
def motif_cannon(d, tint, c, r):
    d.line((c-r, c-int(r*0.15), c+int(r*0.8), c-int(r*0.15)), fill=tint, width=max(4, int(r*0.30)))  # barrel
    d.ellipse((c+int(r*0.55), c-int(r*0.4), c+r, c+int(r*0.1)), fill=tint)             # muzzle
    for wx in (-0.4, 0.3):
        d.ellipse((c+int(r*wx)-int(r*0.28), c+int(r*0.2), c+int(r*wx)+int(r*0.28), c+int(r*0.76)), outline=tint, width=max(2, int(r*0.06)))
def motif_machine_gun(d, tint, c, r):
    d.line((c-int(r*0.7), c-int(r*0.2), c+int(r*0.7), c-int(r*0.2)), fill=tint, width=max(3, int(r*0.14)))  # barrel
    _L(d, tint, [(c, c-int(r*0.2)), (c-int(r*0.5), c+r)], max(3, int(r*0.08)))
    _L(d, tint, [(c, c-int(r*0.2)), (c+int(r*0.5), c+r)], max(3, int(r*0.08)))
    _L(d, tint, [(c, c-int(r*0.2)), (c, c+r)], max(3, int(r*0.08)))
def motif_revolver(d, tint, c, r):
    d.line((c-int(r*0.7), c-int(r*0.3), c+int(r*0.7), c-int(r*0.3)), fill=tint, width=max(3, int(r*0.14)))
    d.line((c-int(r*0.2), c-int(r*0.3), c-int(r*0.5), c+int(r*0.8)), fill=tint, width=max(3, int(r*0.16)))
    d.ellipse((c-int(r*0.15), c-int(r*0.15), c+int(r*0.25), c+int(r*0.25)), fill=tint)
def motif_grenade(d, tint, c, r):
    d.ellipse((c-int(r*0.5), c-int(r*0.3), c+int(r*0.5), c+int(r*0.8)), fill=tint)
    d.rectangle((c-int(r*0.15), c-int(r*0.6), c+int(r*0.15), c-int(r*0.3)), fill=tint)  # neck
    d.ellipse((c+int(r*0.05), c-int(r*0.85), c+int(r*0.4), c-int(r*0.5)), outline=tint, width=max(2, int(r*0.06)))  # ring
def motif_sailing_ship(d, tint, c, r):
    d.polygon([(c-r, c+int(r*0.2)), (c+r, c+int(r*0.2)), (c+int(r*0.6), c+int(r*0.7)), (c-int(r*0.6), c+int(r*0.7))], fill=tint)  # hull
    d.line((c, c+int(r*0.2), c, c-r), fill=tint, width=max(3, int(r*0.08)))            # mast
    d.polygon([(c, c-int(r*0.9)), (c+int(r*0.55), c-int(r*0.1)), (c, c-int(r*0.1))], fill=tint)  # sail
def motif_anchor(d, tint, c, r):
    w = max(3, int(r*0.10))
    d.line((c, c-int(r*0.7), c, c+int(r*0.8)), fill=tint, width=w)
    d.line((c-int(r*0.4), c-int(r*0.4), c+int(r*0.4), c-int(r*0.4)), fill=tint, width=w)
    d.arc((c-int(r*0.7), c+int(r*0.1), c+int(r*0.7), c+r), 20, 160, fill=tint, width=w)
    d.ellipse((c-int(r*0.12), c-int(r*0.85), c+int(r*0.12), c-int(r*0.6)), outline=tint, width=w)
def motif_vial_flask(d, tint, c, r):
    d.polygon([(c-int(r*0.2), c-r), (c+int(r*0.2), c-r), (c+int(r*0.5), c+int(r*0.7)),
               (c-int(r*0.5), c+int(r*0.7))], outline=tint, width=max(3, int(r*0.08)))
    d.line((c-int(r*0.36), c+int(r*0.2), c+int(r*0.36), c+int(r*0.2)), fill=tint, width=max(2, int(r*0.06)))  # liquid
def motif_compass_dividers(d, tint, c, r):
    w = max(3, int(r*0.10))
    d.line((c, c-int(r*0.7), c-int(r*0.5), c+r), fill=tint, width=w)
    d.line((c, c-int(r*0.7), c+int(r*0.5), c+r), fill=tint, width=w)
    d.ellipse((c-int(r*0.12), c-int(r*0.85), c+int(r*0.12), c-int(r*0.6)), fill=tint)
def motif_book_scroll(d, tint, c, r):
    d.rectangle((c-r, c-int(r*0.45), c+r, c+int(r*0.45)), outline=tint, width=max(3, int(r*0.08)))
    for ex in (-1.0, 1.0):
        d.ellipse((c+int(r*ex)-int(r*0.18), c-int(r*0.45), c+int(r*ex)+int(r*0.18), c+int(r*0.45)), fill=tint)
def motif_rail_track(d, tint, c, r):
    for rx in (-0.3, 0.3):
        d.line((c+int(r*rx), c-r, c+int(r*rx), c+r), fill=tint, width=max(3, int(r*0.08)))
    for ry in (-0.6, -0.2, 0.2, 0.6):
        d.line((c-int(r*0.55), c+int(r*ry), c+int(r*0.55), c+int(r*ry)), fill=tint, width=max(2, int(r*0.06)))
def motif_jar(d, tint, c, r):
    d.rectangle((c-int(r*0.55), c-int(r*0.5), c+int(r*0.55), c+r), outline=tint, width=max(3, int(r*0.08)))
    d.rectangle((c-int(r*0.4), c-int(r*0.8), c+int(r*0.4), c-int(r*0.5)), fill=tint)   # lid
def motif_loom_thread(d, tint, c, r):
    d.rectangle((c-r, c-r, c+r, c+r), outline=tint, width=max(3, int(r*0.08)))
    for wx in (-0.5, -0.17, 0.17, 0.5):
        d.line((c+int(r*wx), c-r, c+int(r*wx), c+r), fill=tint, width=max(2, int(r*0.05)))
    d.line((c-r, c, c+r, c), fill=tint, width=max(3, int(r*0.08)))                     # shuttle
def motif_hammer_anvil(d, tint, c, r):
    d.polygon([(c-r, c+int(r*0.1)), (c+r, c+int(r*0.1)), (c+int(r*0.5), c+int(r*0.5)),
               (c-int(r*0.3), c+int(r*0.5))], fill=tint)                               # anvil
    d.line((c-int(r*0.5), c-int(r*0.7), c+int(r*0.3), c-int(r*0.1)), fill=tint, width=max(3, int(r*0.10)))  # handle
    d.rectangle((c-int(r*0.7), c-int(r*0.95), c-int(r*0.2), c-int(r*0.55)), fill=tint) # head
def motif_bridge_canal(d, tint, c, r):
    d.arc((c-r, c-int(r*0.3), c+r, c+int(r*1.1)), 180, 360, fill=tint, width=max(3, int(r*0.10)))  # span
    for px in (-0.7, 0.7):
        d.line((c+int(r*px), c-int(r*0.1), c+int(r*px), c+int(r*0.6)), fill=tint, width=max(2, int(r*0.07)))
    d.line((c-r, c+int(r*0.7), c+r, c+int(r*0.7)), fill=tint, width=max(2, int(r*0.06)))  # water
def motif_kiln_flame(d, tint, c, r):
    d.polygon([(c-int(r*0.6), c+int(r*0.7)), (c+int(r*0.6), c+int(r*0.7)),
               (c+int(r*0.35), c-int(r*0.5)), (c-int(r*0.35), c-int(r*0.5))], outline=tint, width=max(3, int(r*0.08)))
    d.pieslice((c-int(r*0.25), c+int(r*0.2), c+int(r*0.25), c+int(r*0.7)), 180, 360, fill=tint)  # arch
    d.polygon([(c, c-int(r*0.9)), (c+int(r*0.2), c-int(r*0.4)), (c-int(r*0.2), c-int(r*0.4))], fill=tint)  # flame
def motif_cogwheel(d, tint, c, r):
    import math
    d.ellipse((c-int(r*0.6), c-int(r*0.6), c+int(r*0.6), c+int(r*0.6)), outline=tint, width=max(4, int(r*0.14)))
    for k in range(8):
        a = math.radians(k*45)
        x, y = c+int(r*0.75*math.cos(a)), c+int(r*0.75*math.sin(a))
        d.ellipse((x-int(r*0.12), y-int(r*0.12), x+int(r*0.12), y+int(r*0.12)), fill=tint)
    d.ellipse((c-int(r*0.15), c-int(r*0.15), c+int(r*0.15), c+int(r*0.15)), fill=tint)
def motif_telegraph_pole(d, tint, c, r):
    w = max(3, int(r*0.09))
    d.line((c, c-r, c, c+r), fill=tint, width=w)
    for cy in (-0.5, -0.1):
        d.line((c-int(r*0.6), c+int(r*cy), c+int(r*0.6), c+int(r*cy)), fill=tint, width=w)
    d.line((c-int(r*0.6), c-int(r*0.5), c+int(r*0.6), c-int(r*0.1)), fill=tint, width=max(2, int(r*0.04)))
def motif_lightning_bolt(d, tint, c, r):
    d.polygon([(c+int(r*0.2), c-r), (c-int(r*0.4), c+int(r*0.15)), (c, c+int(r*0.15)),
               (c-int(r*0.2), c+r), (c+int(r*0.5), c-int(r*0.2)), (c, c-int(r*0.2))], fill=tint)
def motif_steam_engine(d, tint, c, r):
    d.rectangle((c-r, c-int(r*0.3), c+int(r*0.2), c+int(r*0.3)), fill=tint)            # cylinder
    d.ellipse((c+int(r*0.2), c-int(r*0.6), c+r, c+int(r*0.6)), outline=tint, width=max(3, int(r*0.10)))  # flywheel
    d.line((c, c, c+int(r*0.6), c), fill=tint, width=max(2, int(r*0.06)))              # rod
def motif_seal_stamp(d, tint, c, r):
    d.ellipse((c-int(r*0.65), c-int(r*0.1), c+int(r*0.65), c+int(r*0.9)), outline=tint, width=max(3, int(r*0.09)))  # face
    d.rectangle((c-int(r*0.2), c-r, c+int(r*0.2), c-int(r*0.1)), fill=tint)            # handle
    d.line((c-int(r*0.25), c+int(r*0.4), c+int(r*0.25), c+int(r*0.4)), fill=tint, width=max(2, int(r*0.06)))
def motif_coin_ingot(d, tint, c, r):
    d.polygon([(c-r, c-int(r*0.2)), (c+r, c-int(r*0.4)), (c+r, c+int(r*0.3)), (c-r, c+int(r*0.5))], outline=tint, width=max(3, int(r*0.08)))
    d.ellipse((c-int(r*0.2), c-int(r*0.15), c+int(r*0.2), c+int(r*0.25)), fill=tint)
def motif_envelope_letter(d, tint, c, r):
    d.rectangle((c-r, c-int(r*0.55), c+r, c+int(r*0.55)), outline=tint, width=max(3, int(r*0.08)))
    _L(d, tint, [(c-r, c-int(r*0.55)), (c, c+int(r*0.05)), (c+r, c-int(r*0.55))], max(2, int(r*0.06)))
def motif_scales_of_justice(d, tint, c, r):
    w = max(3, int(r*0.08))
    d.line((c, c-r, c, c+int(r*0.8)), fill=tint, width=w)
    d.line((c-r, c-int(r*0.6), c+r, c-int(r*0.6)), fill=tint, width=w)
    for px in (-1.0, 1.0):
        d.line((c+int(r*px), c-int(r*0.6), c+int(r*px), c-int(r*0.1)), fill=tint, width=max(2, int(r*0.04)))
        d.arc((c+int(r*px)-int(r*0.3), c-int(r*0.25), c+int(r*px)+int(r*0.3), c+int(r*0.35)), 0, 180, fill=tint, width=w)
    d.line((c-int(r*0.4), c+int(r*0.8), c+int(r*0.4), c+int(r*0.8)), fill=tint, width=w)  # base
def motif_printing_press(d, tint, c, r):
    d.rectangle((c-r, c-r, c+r, c+r), outline=tint, width=max(3, int(r*0.08)))
    d.rectangle((c-int(r*0.7), c-int(r*0.1), c+int(r*0.7), c+int(r*0.2)), fill=tint)   # platen
    d.line((c, c-r, c, c-int(r*0.1)), fill=tint, width=max(3, int(r*0.12)))            # screw
def motif_camera_lens(d, tint, c, r):
    d.rectangle((c-r, c-int(r*0.5), c+r, c+int(r*0.6)), outline=tint, width=max(3, int(r*0.08)))
    d.ellipse((c-int(r*0.4), c-int(r*0.25), c+int(r*0.4), c+int(r*0.55)), outline=tint, width=max(3, int(r*0.09)))
    d.rectangle((c+int(r*0.3), c-int(r*0.75), c+int(r*0.7), c-int(r*0.5)), fill=tint)  # viewfinder
def motif_theatre_mask(d, tint, c, r):
    d.ellipse((c-int(r*0.6), c-int(r*0.8), c+int(r*0.6), c+int(r*0.8)), outline=tint, width=max(3, int(r*0.09)))
    for ex in (-0.25, 0.25):
        d.ellipse((c+int(r*ex)-int(r*0.12), c-int(r*0.3), c+int(r*ex)+int(r*0.12), c-int(r*0.05)), fill=tint)
    d.arc((c-int(r*0.3), c+int(r*0.05), c+int(r*0.3), c+int(r*0.5)), 20, 160, fill=tint, width=max(3, int(r*0.08)))
def motif_fossil_spiral(d, tint, c, r):
    import math
    pts = []
    for k in range(48):
        t = k/6.0
        rad = r*0.12*t
        pts.append((c+int(rad*math.cos(t*2)), c+int(rad*math.sin(t*2))))
    _L(d, tint, pts, max(3, int(r*0.08)))
def motif_plough_wheat(d, tint, c, r):
    for wx in (-0.4, 0.0, 0.4):
        d.line((c+int(r*wx), c+r, c+int(r*wx), c-int(r*0.4)), fill=tint, width=max(2, int(r*0.06)))
        for s in (-1, 1):
            d.line((c+int(r*wx), c-int(r*0.4), c+int(r*wx)+s*int(r*0.18), c-int(r*0.1)), fill=tint, width=max(2, int(r*0.05)))
def motif_mortarboard(d, tint, c, r):
    d.polygon([(c, c-int(r*0.6)), (c+r, c-int(r*0.2)), (c, c+int(r*0.2)), (c-r, c-int(r*0.2))], fill=tint)
    d.line((c+int(r*0.4), c, c+int(r*0.4), c+int(r*0.7)), fill=tint, width=max(2, int(r*0.05)))  # tassel
    d.ellipse((c+int(r*0.3), c+int(r*0.6), c+int(r*0.5), c+int(r*0.8)), fill=tint)
def motif_quill_pen(d, tint, c, r):
    d.polygon([(c-r, c+r), (c+int(r*0.7), c-int(r*0.9)), (c+r, c-int(r*0.5)), (c-int(r*0.6), c+r)], fill=tint)
def motif_tea_leaf(d, tint, c, r):
    d.polygon([(c, c-r), (c+int(r*0.5), c), (c, c+r), (c-int(r*0.5), c)], fill=tint)
    d.line((c, c-r, c, c+r), fill=(28, 28, 28, 255), width=max(2, int(r*0.05)))        # vein
def motif_abacus(d, tint, c, r):
    d.rectangle((c-r, c-int(r*0.7), c+r, c+int(r*0.7)), outline=tint, width=max(3, int(r*0.08)))
    for ry in (-0.35, 0.0, 0.35):
        d.line((c-r, c+int(r*ry), c+r, c+int(r*ry)), fill=tint, width=max(2, int(r*0.04)))
        for bx in (-0.6, -0.2, 0.3):
            d.ellipse((c+int(r*bx)-int(r*0.1), c+int(r*ry)-int(r*0.1), c+int(r*bx)+int(r*0.1), c+int(r*ry)+int(r*0.1)), fill=tint)
def motif_bow_arrow(d, tint, c, r):
    d.arc((c-int(r*0.2), c-r, c+r, c+r), 300, 60, fill=tint, width=max(3, int(r*0.10)))  # bow
    d.line((c-int(r*0.6), c, c+r, c), fill=tint, width=max(2, int(r*0.06)))            # arrow
    d.polygon([(c+r, c), (c+int(r*0.6), c-int(r*0.15)), (c+int(r*0.6), c+int(r*0.15))], fill=tint)
def motif_horse(d, tint, c, r):
    d.polygon([(c-int(r*0.6), c+r), (c-int(r*0.4), c-int(r*0.2)), (c+int(r*0.1), c-int(r*0.7)),
               (c+int(r*0.2), c-r), (c+int(r*0.45), c-int(r*0.6)), (c+int(r*0.1), c-int(r*0.3)),
               (c+int(r*0.5), c+int(r*0.1)), (c+int(r*0.2), c+r)], fill=tint)          # head+neck silhouette
def motif_pagoda_temple(d, tint, c, r):
    for k, (wy, ww) in enumerate([( -0.6, 1.0), (-0.1, 0.75), (0.4, 0.5)]):
        d.polygon([(c-int(r*ww), c+int(r*wy)+int(r*0.15)), (c+int(r*ww), c+int(r*wy)+int(r*0.15)),
                   (c+int(r*ww*0.6), c+int(r*wy)-int(r*0.1)), (c-int(r*ww*0.6), c+int(r*wy)-int(r*0.1))], fill=tint)
    d.line((c, c-r, c, c-int(r*0.7)), fill=tint, width=max(2, int(r*0.06)))            # spire

def motif_telescope(d, tint, c, r):
    d.polygon([(c-r, c-int(r*0.7)), (c+int(r*0.7), c+int(r*0.1)), (c+int(r*0.4), c+int(r*0.4)),
               (c-r, c-int(r*0.3))], fill=tint)                                        # tube
    _L(d, tint, [(c-int(r*0.7), c-int(r*0.5)), (c-r, c+r)], max(3, int(r*0.07)))       # tripod legs
    _L(d, tint, [(c-int(r*0.7), c-int(r*0.5)), (c, c+r)], max(3, int(r*0.07)))
    d.ellipse((c-r-int(r*0.05), c-int(r*0.7), c-int(r*0.6), c-int(r*0.2)), fill=tint)  # eyepiece

MOTIFS = {
    'war_banner': motif_war_banner, 'rifle': motif_rifle, 'cannon': motif_cannon,
    'machine_gun': motif_machine_gun, 'revolver': motif_revolver, 'grenade': motif_grenade,
    'sailing_ship': motif_sailing_ship, 'anchor': motif_anchor, 'vial_flask': motif_vial_flask,
    'compass_dividers': motif_compass_dividers, 'book_scroll': motif_book_scroll,
    'rail_track': motif_rail_track, 'jar': motif_jar, 'loom_thread': motif_loom_thread,
    'hammer_anvil': motif_hammer_anvil, 'bridge_canal': motif_bridge_canal, 'kiln_flame': motif_kiln_flame,
    'cogwheel': motif_cogwheel, 'telegraph_pole': motif_telegraph_pole, 'lightning_bolt': motif_lightning_bolt,
    'steam_engine': motif_steam_engine, 'seal_stamp': motif_seal_stamp, 'coin_ingot': motif_coin_ingot,
    'envelope_letter': motif_envelope_letter, 'scales_of_justice': motif_scales_of_justice,
    'printing_press': motif_printing_press, 'camera_lens': motif_camera_lens, 'theatre_mask': motif_theatre_mask,
    'telescope': motif_telescope, 'fossil_spiral': motif_fossil_spiral, 'plough_wheat': motif_plough_wheat,
    'mortarboard': motif_mortarboard, 'quill_pen': motif_quill_pen, 'tea_leaf': motif_tea_leaf,
    'abacus': motif_abacus, 'bow_arrow': motif_bow_arrow, 'horse': motif_horse, 'pagoda_temple': motif_pagoda_temple,
}

# literal qing_tech_* overrides (checked first)
QING_LITERAL = {
    'qing_tech_imperial_kilns': 'kiln_flame', 'qing_tech_imperial_silk': 'loom_thread',
    'qing_tech_tea_canton': 'tea_leaf', 'qing_tech_grand_canal': 'bridge_canal',
    'qing_tech_siku_compilation': 'book_scroll', 'qing_tech_court_mathematics': 'abacus',
    'qing_tech_eight_banners': 'war_banner', 'qing_tech_columbian_crops': 'plough_wheat',
    'qing_tech_variolation': 'vial_flask', 'qing_tech_manchu_science': 'bow_arrow',
    'qing_tech_han_science': 'seal_stamp', 'qing_tech_mongol_science': 'horse',
    'qing_tech_tibetan_science': 'pagoda_temple', 'qing_tech_uyghur_science': 'plough_wheat',
}
# ordered (regex, motif) rules, first match wins
MOTIF_RULES = [
    (r'artillery_cartridges', 'cannon'),
    (r'grenade', 'grenade'),
    (r'machine_gun|sub_machine|light_machine', 'machine_gun'),
    (r'revolver|pistol', 'revolver'),
    (r'rifle|bayonet|firearm|weapon_manufactur|small_arms|replaceable_weapon|cartridge|bullet|percussion_cap|fulminate|smokeless_powder|guncotton|nitroglycerin|rifling|breechloader|minie|pinfire|sniper|dispersed_unit|trench|camouflage|post_napoleonic', 'rifle'),
    (r'torpedo|naval_explosive|carronade|cannon|artillery|mortar|howitzer|limber|bombard|shrapnel|congreve|gribeauval|recoil_buffer|quick_firing_gun', 'cannon'),
    (r'shipyard|warship|steam_powered_ship|marine_barometer|diving_bell|copper_plating|round_bow|multiple_deck', 'sailing_ship'),
    (r'anchor', 'anchor'),
    (r'banner|regiment|specialised_corps|corps|mobilisation|storm_troop|permanent_army|commissioned_staff|skirmisher', 'war_banner'),
    (r'ambulance|clinical|physiology|pathology|epidemiology|vaccin|antiseptic|antitoxin|hygiene|hospital|pharmacology|pasteuriz|germ|bonesaw|elixir|tincture|asprin|ophthalmoscopy|medical|comparative_anatomy', 'vial_flask'),
    (r'cartograph|expedition', 'compass_dividers'),
    (r'treatise', 'book_scroll'),
    (r'rail|tramway|locomotive|tender_carriage|stock_car|sprinkler_car|sand_pump', 'rail_track'),
    (r'jarring|canning|_jar|canneries|can_opener|explorers_rations|pasteurization', 'jar'),
    (r'spinning|loom|cotton_gin|water_frame', 'loom_thread'),
    (r'metalworking|bloomery|organometallic|construction$|templating|puddling', 'hammer_anvil'),
    (r'canal|sewer', 'bridge_canal'),
    (r'blast_furnace', 'kiln_flame'),
    (r'gear_systems|mechanical_tools|manufactories|threshing|interchangeable_parts', 'cogwheel'),
    (r'telegraph', 'telegraph_pole'),
    (r'electric|voltaic|electromagnet|electrochemistry', 'lightning_bolt'),
    (r'reciprocating_engine|rotative_beam_engine|double_acting_cylinders|grasshopper_engine|thermodynamics', 'steam_engine'),
    (r'smallpox|leblanc', 'vial_flask'),
    (r'administra|registry|records|census|gazette|codification|cadastral|municipal|passport|identification|recruitment|civil_service|police|archiving|building_society|fire_brigades|urban_planning', 'seal_stamp'),
    (r'bank|monetary|debt|saving|insurance|credit|exchange_rate|bookkeeping|bond|stock_compan|commodity|sinking_fund|treasury|clearing_house|custom_union', 'coin_ingot'),
    (r'postal|post_stamp|letter_box', 'envelope_letter'),
    (r'diplomat|embass|international_law|consular|treaties|treaty|protocol|chancery', 'scales_of_justice'),
    (r'newspaper|lithography|stereotyping|periodical|public_opinion', 'printing_press'),
    (r'photograph|daguerreo|heliography|monochrome|magic_lantern', 'camera_lens'),
    (r'typewriter', 'printing_press'),
    (r'technical_drawings|metric_system', 'compass_dividers'),
    (r'standardised_writing_system', 'quill_pen'),
    (r'statistical_bureau', 'seal_stamp'),
    (r'scientific_method|society_analysis|scientific_revolution|secular_sciences|anthropology|scientific_journals|psychology|historiography|historicism|^tech_education$', 'book_scroll'),
    (r'art_history|national_epic|theatre|neoclassicism|cultural_imperialism|museum|romanticism', 'theatre_mask'),
    (r'astronomy|astrophysics|optics', 'telescope'),
    (r'geology|stratigraphy|palaeontology', 'fossil_spiral'),
    (r'systematic_botany|agronomy|crop|plough|wheat|agri', 'plough_wheat'),
    (r'chemistry|spectroscopy|molecular_physics|atomic_theory|pneumatics|electromagnetism', 'vial_flask'),
    (r'philology|linguistics|epigraphy|political_economy|sociology|ethnography', 'quill_pen'),
    (r'school|teacher|polytechnic|universit|academ', 'mortarboard'),
    (r'horse', 'horse'),
]
DOMAIN_FALLBACK = {'military': 'war_banner', 'civic': 'cogwheel', 'oratory': 'book_scroll',
                   'religious': 'quill_pen', 'qing': 'pagoda_temple'}

def motif_for(key, dom):
    if key in QING_LITERAL:
        return QING_LITERAL[key]
    for pat, name in MOTIF_RULES:
        if re.search(pat, key):
            return name
    return DOMAIN_FALLBACK.get(dom, 'cogwheel')

def write_gfx(keys):
    """Register one spriteType GFX_<key> -> our <key>.dds per invention.

    PROVEN mechanism (Invictus/TI both leave the invention folder EMPTY and rely on
    `icon_override = <sprite>` for the few nodes they theme — e.g. `icon_override = gw_icon`,
    which the engine resolves to a base-game spriteType named GFX_gw_icon). GetInventionIcon
    does NOT load loose <key>.dds by filename, so per-node art MUST go through a spriteType +
    icon_override. This file supplies GFX_<key> for every mod invention key; inject_overrides()
    then adds `icon_override = <key>` to each node so the engine picks up GFX_<key>."""
    os.makedirs(GFX_DIR, exist_ok=True)
    lines = [
        "# imperatrix_inventions.gfx — [#118/#124/#128] one spriteType per mod invention key.",
        "# GENERATED by tools/gen_invention_icons.py — do not hand-edit; re-run the generator.",
        "# GetInventionIcon needs a registered sprite (loose <key>.dds is NOT loaded by the engine);",
        "# each node carries `icon_override = <key>` which resolves to GFX_<key> defined here.",
        "spriteTypes = {",
    ]
    rel = "gfx/interface/buttons/inventions"
    for key in sorted(keys):
        lines.append("\tspriteType = {")
        lines.append(f'\t\tname = "GFX_{key}"')
        lines.append(f'\t\ttexturefile = "{rel}/{key}.dds"')
        lines.append("\t}")
    lines.append("}")
    with open(GFX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[#118] wrote {len(keys)} spriteTypes -> {GFX_FILE}")


def inject_overrides(dmap):
    """Add `icon_override = <key>` immediately after each `<key> = {` node header.

    Idempotent: first strips any previously-generated `# [#118]` override lines, then re-adds,
    so re-running the generator never stacks duplicates."""
    total = 0
    for f in glob.glob(os.path.join(INV_DIR, "*.txt")):
        if os.path.basename(f) not in DOMAIN_FILE:
            continue
        src = open(f, encoding="utf-8").read()
        # 1. drop any prior generated override lines
        kept = [ln for ln in src.split("\n") if "# [#118]" not in ln]
        # 2. re-inject after every node header
        out_lines = []
        for line in kept:
            out_lines.append(line)
            mt = re.match(r'^\t([a-z_0-9]+)\s*=\s*\{\s*$', line)
            if mt and mt.group(1) in dmap:
                out_lines.append(f"\t\ticon_override = {mt.group(1)}\t# [#118] -> GFX_{mt.group(1)}")
        new = "\n".join(out_lines)
        if new != src:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(new)
        total += new.count("icon_override =")
    print(f"[#118] icon_override lines now present across invention files: {total}")


def gen(force=False):
    os.makedirs(OUT, exist_ok=True)
    dmap = domain_of_key()
    ok = skip = 0
    for key, dom in sorted(dmap.items()):
        out = os.path.join(OUT, key + ".dds")
        if os.path.exists(out) and not force:
            skip += 1; continue
        im = canvas(); d = ImageDraw.Draw(im)
        base = DOMAIN_COL[dom]
        disc(d, base)
        # [MO#9] subject motif (was emblem()'s hash rosette = generic graph look). Domain tint
        # kept so within-domain nodes still read as a family; the motif carries the subject.
        tint = tuple(min(255, x + 90) for x in base) + (255,)
        cc = PX * S // 2
        rr = int(PX * S * 0.34)
        MOTIFS[motif_for(key, dom)](d, tint, cc, rr)
        im = im.resize((PX, PX), Image.LANCZOS)
        write_bgra8(out, np.asarray(im, dtype=np.uint8))
        ok += 1
    print(f"[MO#9/#118] invention icons: wrote {ok}, skipped {skip} (of {len(dmap)}) -> {OUT}")
    write_gfx(list(dmap.keys()))
    inject_overrides(dmap)

if __name__ == "__main__":
    gen(force="--force" in sys.argv)
