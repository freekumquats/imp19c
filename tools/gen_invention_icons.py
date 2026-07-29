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
import os, sys, re, glob, struct, hashlib
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

def emblem(d, key, base_col):
    """Deterministic per-key motif: a rosette of N spokes at angle-offset A, plus a central
    pip — driven by a hash of the key, so every invention gets a visually distinct mark."""
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    c = PX * S // 2
    spokes = 3 + (h % 6)                       # 3..8 spokes
    ang0 = (h >> 3) % 360
    r_out = int(PX * S * (0.20 + 0.10 * ((h >> 6) % 3)))   # 0.20/0.30/0.40
    lw = max(2, int(PX * S * 0.035))
    tint = tuple(min(255, x + 90) for x in base_col) + (255,)
    import math
    for k in range(spokes):
        a = math.radians(ang0 + k * 360.0 / spokes)
        x = c + int(r_out * math.cos(a)); y = c + int(r_out * math.sin(a))
        d.line((c, c, x, y), fill=tint, width=lw)
        rr = max(3, int(PX * S * 0.035))
        d.ellipse((x-rr, y-rr, x+rr, y+rr), fill=tint)
    pip = int(PX * S * 0.06)
    d.ellipse((c-pip, c-pip, c+pip, c+pip), fill=(245, 240, 220, 255), outline=(40, 40, 40, 255))

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
        emblem(d, key, base)
        im = im.resize((PX, PX), Image.LANCZOS)
        write_bgra8(out, np.asarray(im, dtype=np.uint8))
        ok += 1
    print(f"[#118] invention icons: wrote {ok}, skipped {skip} (of {len(dmap)}) -> {OUT}")
    write_gfx(list(dmap.keys()))
    inject_overrides(dmap)

if __name__ == "__main__":
    gen(force="--force" in sys.argv)
