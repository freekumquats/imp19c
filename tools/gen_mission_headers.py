#!/usr/bin/env python3
"""
gen_mission_headers.py — build the mission SELECTOR-CARD icons (icons/missions/).

CORRECTION (review): a mission tree declares TWO separate art fields (see
common/defines/graphic/00_graphics.txt):
  icon   = <tree>_mission            -> gfx/interface/icons/missions/<key>.dds
                                        = the SELECTOR CARD in the mission-list (300x120,
                                        MissionItem.GetImage, ~2.5:1 to fit the card)
  header = mission_image_<tree>       -> gfx/interface/missions/<key>.dds
                                        = the 624x120 HEADER banner at the top of the
                                        mission view (MissionView.GetHeaderImage)
This script generates the SELECTOR CARDS (icons/missions/), which were missing for the
Qing trees (only russian_missions_1 + test1 existed). The HEADER banners already existed
in gfx/interface/missions/ but were DXT5 (widget rejects it); those are re-encoded to
DX10 separately, NOT by this script.

Format: 300x120 DX10 BGRA8-sRGB (dxgiFormat=91), matching vanilla's selector-card aspect.
Each card composites the tree's 118x68 TASK-icon art as an emblem on a gold-ruled band.
"""
import struct, os, glob
from PIL import Image, ImageDraw
import numpy as np
import sys; sys.path.insert(0, os.path.dirname(__file__))
from dds_icon import write_dds_dx10_bgra8, read_dds_bgra8, read_dds_dims
from fetch_wm import download

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MT   = 'gfx/interface/icons/mission_tasks'
OUT  = 'gfx/interface/icons/missions'          # selector cards  icons/missions/<tree>.dds  (300x120)
HDR  = 'gfx/interface/missions'                # header banners  mission_image_<tree>.dds (624x120)
CARD_W, CARD_H = 300, 120   # selector-card size (vanilla russian_missions_1.dds aspect)
BANNER_W, BANNER_H = 624, 120   # header-banner size (mission-view top banner)
HW, HH = CARD_W, CARD_H     # back-compat aliases for the emblem path below
SRC  = os.path.join(ROOT, 'art_src', 'missions')

# ---------------------------------------------------------------------------
# Per-tree PHOTO override. A tree listed here gets BOTH user-visible images
# (selector card + header banner) rendered from a real photograph rather than
# the emblem-on-band card. Both images are cover-cropped from the same source
# and written as DX10 BGRA8-sRGB (the only form the mission widgets accept).
#
# The key is the mission-tree name (its `qing_<tree>` stem). The two target
# files must match the tree node's declared fields EXACTLY — they are NOT
# derivable from one another (see common/missions/qing_*_missions.txt):
#   icon   = qing_<tree>_mission  -> gfx/interface/icons/missions/<icon>.dds   (card,   300x120)
#   header = mission_image_qing_<tree> -> gfx/interface/missions/<header>.dds  (banner, 624x120)
# So each entry stores (spec, icon_name, header_name). The emblem loop in
# main() SKIPS these icon_names so the photo card is never overwritten.
# ---------------------------------------------------------------------------
PHOTOS = {
 # Invasion of Burma — 1761 Myanmar tribute delegates at the Qing court (万国来朝图)
 "qing_burma_war": (
   ("D", "https://upload.wikimedia.org/wikipedia/commons/8/8f/"
         "%E4%B8%87%E5%9B%BD%E6%9D%A5%E6%9C%9D%E5%9B%BE_Myanmar_%28%E7%BC%85%E7%94%B8"
         "%E5%9B%BD%29_delegates_in_Peking_in_1761.jpg"),
   "qing_burma_war_mission", "mission_image_qing_burma_war"),
 # The Settlement of the New Dominion (新疆善後) — the Western Regions / Xinjiang
 "qing_xinjiang": (
   ("D", "https://upload.wikimedia.org/wikipedia/commons/c/c8/Chengde_summer_palace_writings.jpg"),
   "qing_xinjiang_mission", "mission_image_qing_xinjiang"),
 # Colonization — Ortelius' 1589 map of the Pacific (Maris Pacifici)
 "qing_colonization": (
   ("D", "https://static-prod.lib.princeton.edu/visual_materials/maps/websites/"
         "pacific/pacific-ocean/map-pacific-ortelius-1589.jpg"),
   "qing_colonization_mission", "mission_image_qing_colonization"),
 # Central Asia — d'Anville's 1734 map of China, Chinese Tartary and Tibet
 "qing_central_asia": (
   ("D", "https://commons.wikimedia.org/wiki/Special:FilePath/"
         "Carte%20la%20plus%20generale%20et%20qui%20comprend%20la%20Chine,%20la%20"
         "Tartarie%20Chinoise,%20et%20le%20Thibet%20(1734).jpg"),
   "qing_central_asia_mission", "mission_image_qing_central_asia"),
}

def _cover_crop(im, W, H):
    """Scale to fully cover WxH then centre-crop the overflow (no distortion,
    no letterbox). Anchored slightly above centre so faces/titles survive."""
    im = im.convert("RGBA")
    s = max(W / im.width, H / im.height)
    rw, rh = max(W, int(round(im.width * s))), max(H, int(round(im.height * s)))
    im = im.resize((rw, rh), Image.LANCZOS)
    x = (rw - W) // 2
    y = int((rh - H) * 0.40)              # bias toward the top third
    return im.crop((x, y, x + W, y + H))

def _framed(im):
    """Thin gold rule around the band, matching the emblem cards' trim."""
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, im.width - 1, im.height - 1), outline=(196, 158, 86, 255), width=3)
    return im

def gen_photo_tree(tree, entry, force=False):
    """Fetch the source once and write BOTH DX10 images for one tree, to the
    tree's EXACT declared icon (card) + header (banner) filenames."""
    spec, icon_name, header_name = entry
    os.makedirs(SRC, exist_ok=True); os.makedirs(OUT, exist_ok=True); os.makedirs(HDR, exist_ok=True)
    src = os.path.join(SRC, tree + ".jpg")
    if not os.path.exists(src) or force:
        n = download(spec[1], src)
        print(f"  fetched {tree}: {n}B <- {spec[1][:60]}...")
    base = Image.open(src)
    card_path   = f'{OUT}/{icon_name}.dds'
    banner_path = f'{HDR}/{header_name}.dds'
    write_dds_dx10_bgra8(card_path,   np.asarray(_framed(_cover_crop(base, CARD_W, CARD_H)),     dtype=np.uint8))
    write_dds_dx10_bgra8(banner_path, np.asarray(_framed(_cover_crop(base, BANNER_W, BANNER_H)), dtype=np.uint8))
    print(f"  wrote card {card_path} (300x120) + banner {banner_path} (624x120)")

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

def main(force=False):
    os.makedirs(OUT, exist_ok=True)
    # 1) Photo trees: BOTH images (card + banner) from a real photograph.
    print("== photo trees (card + banner) ==")
    for key, spec in PHOTOS.items():
        gen_photo_tree(key, spec, force=force)
    # 2) Everything else: the emblem-on-band selector card only (banners for
    #    those already exist / are re-encoded elsewhere). PHOTOS keys are skipped.
    print("== emblem selector cards ==")
    trees = [os.path.splitext(os.path.basename(p))[0]
             for p in glob.glob(f'{MT}/qing_*_mission.dds')]
    for key in sorted(trees):
        if key in PHOTOS:
            continue
        out = f'{OUT}/{key}.dds'
        if os.path.exists(out) and not force:
            continue
        write_dds_dx10_bgra8(out, make_header(key))
        print("wrote", out)

if __name__ == '__main__':
    main(force="--force" in sys.argv)
