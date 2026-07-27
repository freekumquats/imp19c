#!/usr/bin/env python3
"""
unit_icons.py — bespoke subunit icons for the new Qing unit types (#96).

Draws distinctive, historically-grounded emblems (NOT photo crops — photos turn to mud
at the 18x18 small size). Each unit type gets a themed banner/patch that reads at both
57x57 (large) and 18x18 (small). Output: uncompressed 32-bit BGRA8 DDS matching the
shipped subunit icons (gfx/interface/icons/subunits/regular_infantry.dds: 57x57, pfflags
0x41, bits 32, fourcc 0 — verified). Resolved by filename <unit_key>.dds + _small.dds.

Design rationale per unit (see common/units/army_qing_*.txt + memory eight-banners/
yongying research):
  qing_green_standard  綠營  — plain GREEN banner (the Han Green Standard's colour).
  qing_eight_banners   八旗  — Bordered Yellow banner: yellow field + red border (the
                               premier Upper-Three banner, the emperor's own).
  qing_bayara          巴牙喇 — dark-crimson elite field + gold vertical blade (shock guard).
  qing_ever_victorious 常勝軍 — Western navy-blue field + gold crossed rifles (Ward/Gordon
                               Western-drilled rifle corps).
  qing_yongying        勇營  — the character 勇 ("brave") in white on a round black patch,
                               exactly as the tunic roundel the Brave Battalions wore.
"""
import struct, sys, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

DDPF_ALPHAPIXELS=0x1; DDPF_RGB=0x40
DDSD_CAPS=0x1; DDSD_HEIGHT=0x2; DDSD_WIDTH=0x4; DDSD_PITCH=0x8; DDSD_PIXELFORMAT=0x1000
DDSCAPS_TEXTURE=0x1000

OUT = os.path.join(os.path.dirname(__file__), '..', 'gfx', 'interface', 'icons', 'subunits')
CJK = "/System/Library/Fonts/STHeiti Medium.ttc"

def write_dds_bgra8(path, rgba):
    h, w, _ = rgba.shape
    pitch = w * 4
    flags = DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH|DDSD_PITCH|DDSD_PIXELFORMAT
    header = bytearray(124)
    struct.pack_into('<I', header, 0, 124)
    struct.pack_into('<I', header, 4, flags)
    struct.pack_into('<I', header, 8, h)
    struct.pack_into('<I', header, 12, w)
    struct.pack_into('<I', header, 16, pitch)
    struct.pack_into('<I', header, 24, 1)
    struct.pack_into('<I', header, 72, 32)
    struct.pack_into('<I', header, 76, DDPF_ALPHAPIXELS|DDPF_RGB)
    struct.pack_into('<I', header, 84, 32)
    struct.pack_into('<I', header, 88, 0x00FF0000)
    struct.pack_into('<I', header, 92, 0x0000FF00)
    struct.pack_into('<I', header, 96, 0x000000FF)
    struct.pack_into('<I', header, 100, 0xFF000000)
    struct.pack_into('<I', header, 104, DDSCAPS_TEXTURE)
    bgra = rgba[:, :, [2,1,0,3]].astype(np.uint8)
    with open(path, 'wb') as f:
        f.write(b'DDS '); f.write(bytes(header)); f.write(bgra.tobytes())

# --- draw at high res (4x supersample) then downsample for clean edges ---
S = 4

def new_canvas(px):
    return Image.new('RGBA', (px*S, px*S), (0,0,0,0))

def finalize(im, px, out):
    im = im.resize((px, px), Image.LANCZOS)
    write_dds_bgra8(out, np.asarray(im, dtype=np.uint8))

def rounded_field(d, box, fill, outline=None, ow=0, radius=None):
    if radius is None: radius = (box[2]-box[0])//7
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=ow)

def _pennant(d, x, y, w, h, fill, border=None, bw=0):
    """A hung triangular banner (swallow-point down): rectangle top tapering to a point.
    Matches the embroidered-flag look of the Mongol Banner Cavalry tradition."""
    pts=[(x,y),(x+w,y),(x+w,y+h*0.60),(x+w*0.5,y+h),(x,y+h*0.60)]
    if border:
        d.polygon(pts, fill=border)
        inner=[(x+bw,y+bw),(x+w-bw,y+bw),(x+w-bw,y+h*0.60-bw*0.5),
               (x+w*0.5,y+h-bw*1.7),(x+bw,y+h*0.60-bw*0.5)]
        d.polygon(inner, fill=fill)
    else:
        d.polygon(pts, fill=fill)

def draw_green_standard(px):
    # 綠營 — a single GREEN embroidered triangular banner on a gold pole (was a plain
    # blob). Green is the Green Standard's defining colour.
    im = new_canvas(px); d = ImageDraw.Draw(im)
    px4=px*S
    # pole + finial
    polex=int(px4*0.24)
    d.rectangle((polex-max(2,int(px4*0.03)), int(px4*0.08), polex, int(px4*0.92)),
                fill=(196,150,60,255))
    d.ellipse((polex-int(px4*0.06), int(px4*0.04), polex+int(px4*0.02), int(px4*0.12)),
              fill=(232,196,90,255))
    # the green banner, gold-trimmed
    _pennant(d, polex, int(px4*0.12), int(px4*0.60), int(px4*0.62),
             fill=(40,140,64,255), border=(232,206,110,255), bw=max(2,int(px4*0.045)))
    return im

def draw_eight_banners(px):
    # 八旗 — SEVERAL embroidered triangular banners together (per user): a compact fan of
    # the banner colours (yellow, white, red, blue), the Manchu Eight Banners.
    im = new_canvas(px); d = ImageDraw.Draw(im)
    px4=px*S
    cols=[(240,196,44),(238,238,238),(196,36,36),(40,70,150)]  # yellow/white/red/blue
    n=len(cols)
    margin=int(px4*0.08)
    slot=(px4-2*margin)/n
    fw=int(slot*0.74)
    fh=int(px4*0.70); top=int(px4*0.12)
    for i,c in enumerate(cols):
        x=int(margin+i*slot+(slot-fw)*0.5)
        # tiny pole per banner
        d.rectangle((x-max(1,int(px4*0.02)), top, x, top+fh+int(px4*0.08)),
                    fill=(140,112,56,255))
        _pennant(d, x, top, fw, fh, fill=c+(255,))
    return im

def draw_bayara(px):
    # dark-crimson elite field + gold vertical blade (shock guard).
    im = new_canvas(px); d = ImageDraw.Draw(im); m = int(px*S*0.10)
    b = (m, m, px*S-m, px*S-m)
    rounded_field(d, b, (120,20,28,255), outline=(70,10,16,255), ow=max(2,int(px*S*0.03)))
    cx = px*S//2
    # blade: a tall gold triangle (point up) over a short hilt
    bw = int(px*S*0.11)
    top = int(px*S*0.20); bot = int(px*S*0.66)
    d.polygon([(cx, top), (cx-bw, bot), (cx+bw, bot)], fill=(236,204,88,255))
    d.rectangle((cx-bw, bot, cx+bw, bot+int(px*S*0.05)), fill=(236,204,88,255))     # guard
    d.rectangle((cx-int(bw*0.4), bot+int(px*S*0.05), cx+int(bw*0.4), px*S-m-int(px*S*0.04)),
                fill=(150,96,40,255))                                              # grip
    return im

def draw_ever_victorious(px):
    # Western navy-blue field + gold crossed rifles.
    im = new_canvas(px); d = ImageDraw.Draw(im); m = int(px*S*0.10)
    b = (m, m, px*S-m, px*S-m)
    rounded_field(d, b, (30,52,110,255), outline=(18,32,72,255), ow=max(2,int(px*S*0.03)))
    lw = max(3, int(px*S*0.05))
    p0, p1 = int(px*S*0.24), int(px*S*0.76)
    d.line((p0, p1, p1, p0), fill=(228,198,96,255), width=lw)   # rifle 1
    d.line((p0, p0, p1, p1), fill=(228,198,96,255), width=lw)   # rifle 2
    # small bayonet tips
    for (x,y) in [(p1,p0),(p1,p1)]:
        d.ellipse((x-lw, y-lw, x+lw, y+lw), fill=(240,220,140,255))
    return im

def draw_yongying(px):
    # 勇 ("brave") white on a round black tunic-roundel — the yongying's own insignia.
    # At the tiny 18px size a ring + full glyph turns to mud, so the glyph is enlarged and
    # the ring thinned as px shrinks; centring uses anchor='mm' (robust vs per-glyph bbox).
    im = new_canvas(px); d = ImageDraw.Draw(im); m = int(px*S*0.05)
    b = (m, m, px*S-m, px*S-m)
    ring = max(2, int(px*S*0.035)) if px > 24 else max(2, int(px*S*0.02))
    d.ellipse(b, fill=(24,24,24,255), outline=(224,224,224,255), width=ring)
    fs = int(px*S*(0.72 if px > 24 else 0.86))   # fill more of the roundel when small
    try:
        font = ImageFont.truetype(CJK, fs)
    except Exception:
        font = ImageFont.load_default()
    c = px*S/2.0
    d.text((c, c), "勇", font=font, fill=(240,240,240,255), anchor='mm')
    return im

BUILDERS = {
    'qing_green_standard':  lambda px: draw_green_standard(px),
    'qing_eight_banners':   lambda px: draw_eight_banners(px),
    'qing_bayara':          lambda px: draw_bayara(px),
    'qing_ever_victorious': lambda px: draw_ever_victorious(px),
    'qing_yongying':        lambda px: draw_yongying(px),
}

def main():
    os.makedirs(OUT, exist_ok=True)
    for key, fn in BUILDERS.items():
        for suffix, px in [('', 57), ('_small', 18)]:
            out = os.path.join(OUT, f"{key}{suffix}.dds")
            finalize(fn(px), px, out)
            print(f"wrote {out}")

if __name__ == '__main__':
    main()
