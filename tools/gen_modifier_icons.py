#!/usr/bin/env python3
"""
gen_modifier_icons.py — silence the "Missing Icon for Modifier" boot-log warnings by
supplying a themed 50x50 BGRA8 icon for every auto-generated unit/building/pop modifier
key the engine looks for. One drawn base icon per SEMANTIC CATEGORY (offensive, defensive,
morale, ...), copied to every matching <key>.dds in gfx/interface/icons/modifiers/.

Keys come from tools/_missing_mods.txt (the distinct keys pulled from the boot log). This
is engine noise (vanilla regular_infantry emits the same), but the user asked to silence it;
themed shared icons beat 443 blank tiles and cost ~9 unique images.
Format matches the shipped modifier icons: 50x50 uncompressed BGRA8 (pfflags 0x41).
"""
import struct, os, re, shutil
from PIL import Image, ImageDraw
import numpy as np

OUT='gfx/interface/icons/modifiers'
S=4; PX=50
DDPF_ALPHAPIXELS=0x1; DDPF_RGB=0x40
DDSD_CAPS=0x1; DDSD_HEIGHT=0x2; DDSD_WIDTH=0x4; DDSD_PITCH=0x8; DDSD_PIXELFORMAT=0x1000
DDSCAPS_TEXTURE=0x1000

def write_bgra8(path, rgba):
    h,w,_=rgba.shape; pitch=w*4
    hdr=bytearray(124)
    struct.pack_into('<I',hdr,0,124)
    struct.pack_into('<I',hdr,4,DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH|DDSD_PITCH|DDSD_PIXELFORMAT)
    struct.pack_into('<I',hdr,8,h); struct.pack_into('<I',hdr,12,w); struct.pack_into('<I',hdr,16,pitch)
    struct.pack_into('<I',hdr,24,1)
    struct.pack_into('<I',hdr,72,32); struct.pack_into('<I',hdr,76,DDPF_ALPHAPIXELS|DDPF_RGB)
    struct.pack_into('<I',hdr,84,32)
    struct.pack_into('<I',hdr,88,0x00FF0000); struct.pack_into('<I',hdr,92,0x0000FF00)
    struct.pack_into('<I',hdr,96,0x000000FF); struct.pack_into('<I',hdr,100,0xFF000000)
    struct.pack_into('<I',hdr,104,DDSCAPS_TEXTURE)
    bgra=rgba[:,:,[2,1,0,3]].astype(np.uint8)
    with open(path,'wb') as f: f.write(b'DDS '); f.write(bytes(hdr)); f.write(bgra.tobytes())

def canvas(): return Image.new('RGBA',(PX*S,PX*S),(0,0,0,0))
def save_base(im,name):
    im=im.resize((PX,PX),Image.LANCZOS)
    p=f'/tmp/modicon_{name}.dds'
    write_bgra8(p, np.asarray(im,dtype=np.uint8)); return p

def disc(d, col, m=0.06):
    b=(int(PX*S*m),int(PX*S*m),int(PX*S*(1-m)),int(PX*S*(1-m)))
    d.ellipse(b, fill=col, outline=(30,30,30,255), width=max(2,int(PX*S*0.03)))

GOLD=(228,196,96,255); STEEL=(200,206,214,255); RED=(176,42,42,255)
BLUE=(56,86,150,255); GREEN=(56,128,64,255); BROWN=(140,96,52,255)

def i_offensive():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    c=PX*S//2; w=int(PX*S*0.06)
    d.line((c-int(PX*S*0.22),c+int(PX*S*0.22),c+int(PX*S*0.22),c-int(PX*S*0.22)),fill=STEEL,width=w)  # blade
    d.polygon([(c+int(PX*S*0.22),c-int(PX*S*0.22)),(c+int(PX*S*0.12),c-int(PX*S*0.24)),(c+int(PX*S*0.24),c-int(PX*S*0.12))],fill=STEEL)
    d.line((c-int(PX*S*0.20),c+int(PX*S*0.12),c-int(PX*S*0.08),c+int(PX*S*0.24)),fill=GOLD,width=w)  # guard
    return im
def i_defensive():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    c=PX*S//2
    d.polygon([(c,int(PX*S*0.20)),(int(PX*S*0.74),int(PX*S*0.34)),(c,int(PX*S*0.80)),(int(PX*S*0.26),int(PX*S*0.34))],fill=STEEL,outline=(40,40,40,255))
    d.line((c,int(PX*S*0.24),c,int(PX*S*0.74)),fill=(90,96,104,255),width=max(2,int(PX*S*0.03)))
    return im
def i_morale():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    c=PX*S//2
    d.rectangle((int(PX*S*0.30),int(PX*S*0.22),int(PX*S*0.34),int(PX*S*0.80)),fill=(150,120,60,255))  # pole
    d.polygon([(int(PX*S*0.34),int(PX*S*0.24)),(int(PX*S*0.74),int(PX*S*0.32)),(int(PX*S*0.34),int(PX*S*0.48))],fill=RED)  # flag
    return im
def i_discipline():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    # three drilled ranks (bars)
    for k,y in enumerate([0.34,0.50,0.66]):
        d.rectangle((int(PX*S*0.26),int(PX*S*y),int(PX*S*0.74),int(PX*S*(y+0.06))),fill=GOLD)
    return im
def i_movement():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    c=PX*S//2
    # right-pointing chevrons
    for k,x in enumerate([0.34,0.50,0.62]):
        d.line((int(PX*S*x),int(PX*S*0.32),int(PX*S*(x+0.12)),c),fill=STEEL,width=max(2,int(PX*S*0.045)))
        d.line((int(PX*S*(x+0.12)),c,int(PX*S*x),int(PX*S*0.68)),fill=STEEL,width=max(2,int(PX*S*0.045)))
    return im
def i_coin():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,GOLD)
    c=PX*S//2
    try:
        from PIL import ImageFont
        font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf",int(PX*S*0.5))
        d.text((c,c),"£",font=font,fill=(120,90,20,255),anchor='mm')
    except Exception:
        d.ellipse((int(PX*S*0.3),int(PX*S*0.3),int(PX*S*0.7),int(PX*S*0.7)),outline=(120,90,20,255),width=int(PX*S*0.05))
    return im
def i_terrain():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    c=PX*S//2; w=int(PX*S*0.055)
    d.line((int(PX*S*0.28),int(PX*S*0.72),int(PX*S*0.72),int(PX*S*0.28)),fill=STEEL,width=w)
    d.line((int(PX*S*0.28),int(PX*S*0.28),int(PX*S*0.72),int(PX*S*0.72)),fill=STEEL,width=w)  # crossed swords
    return im
def i_pop():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    c=PX*S//2
    d.ellipse((int(PX*S*0.40),int(PX*S*0.26),int(PX*S*0.60),int(PX*S*0.46)),fill=GOLD)  # head
    d.polygon([(int(PX*S*0.30),int(PX*S*0.74)),(int(PX*S*0.70),int(PX*S*0.74)),(int(PX*S*0.60),int(PX*S*0.50)),(int(PX*S*0.40),int(PX*S*0.50))],fill=GOLD)  # body
    return im
def i_faction():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(70,74,82,255))
    # a rosette / cockade
    c=PX*S//2
    for col,r in [(RED,0.30),(GOLD,0.20),(BLUE,0.10)]:
        d.ellipse((c-int(PX*S*r),c-int(PX*S*r),c+int(PX*S*r),c+int(PX*S*r)),outline=col,width=max(2,int(PX*S*0.04)))
    return im
def i_generic():
    im=canvas(); d=ImageDraw.Draw(im); disc(d,(88,92,100,255))
    c=PX*S//2
    d.ellipse((c-int(PX*S*0.10),c-int(PX*S*0.10),c+int(PX*S*0.10),c+int(PX*S*0.10)),fill=STEEL)
    return im

BASES={}
def build_bases():
    for name,fn in [('offensive',i_offensive),('defensive',i_defensive),('morale',i_morale),
                    ('discipline',i_discipline),('movement',i_movement),('coin',i_coin),
                    ('terrain',i_terrain),('pop',i_pop),('faction',i_faction),('generic',i_generic)]:
        BASES[name]=save_base(fn(),name)

def category(k):
    for suf in ['_maintenance_cost','_movement_speed','_discipline','_morale','_offensive','_defensive','_cost']:
        if k.endswith(suf):
            s=suf.lstrip('_')
            return {'maintenance_cost':'coin','cost':'coin','movement_speed':'movement',
                    'discipline':'discipline','morale':'morale','offensive':'offensive',
                    'defensive':'defensive'}[s]
    if k.endswith('_combat_bonus'): return 'terrain'
    if 'price' in k: return 'coin'
    if re.search(r'(happiness|output|desired_pop_ratio)$',k): return 'pop'
    if re.search(r'(bloc|faction)_(influence|conviction)$',k) or 'conviction' in k or 'bloc' in k or 'faction' in k: return 'faction'
    return 'generic'

# ---------------------------------------------------------------------------
# [#115] CUSTOM-STRATA family — distinct per (stratum x metric).
# The generic category() above maps EVERY output/happiness/desired_pop_ratio key
# to the one shared `pop` silhouette, so the imp19c custom strata (upper/middle/
# lower/proletariat/indentured) all rendered as the SAME icon in tooltips. This
# pass OVERWRITES the strata family with icons distinct on both axes:
#   colour + corner emblem  = the STRATUM   (crown / tophat / sheaf / hammer / shackle)
#   central glyph           = the METRIC    (coin=output, smile=happiness,
#                                            people=desired_pop_ratio, tower=city ratio)
# Two files share art only if they are the same stratum AND metric and differ only
# by scope (local/global/culture) — which is correct, they mean the same thing.
# ---------------------------------------------------------------------------
STRATA_COL = {
    'upper_strata':  (150, 96, 176, 255),   # imperial purple
    'middle_strata': (56,  96, 156, 255),   # merchant blue
    'lower_strata':  (120, 92, 52, 255),    # earth brown
    'proletariat':   (168, 52, 46, 255),    # labour red
    'indentured':    (96,  100, 108, 255),  # iron grey
}

def _blade_disc(col):
    im=canvas(); d=ImageDraw.Draw(im); disc(d,col); return im,d

def strata_emblem(d, stratum):
    """Small stratum badge, top-left, so strata are told apart even at equal metric."""
    x0,y0 = int(PX*S*0.10), int(PX*S*0.10); s=int(PX*S*0.30)
    if stratum=='upper_strata':      # coronet: three points
        pts=[(x0,y0+s)]
        for k in range(4):
            xx=x0+int(s*k/3); pts.append((xx,y0)); pts.append((xx+int(s/6),y0+int(s*0.5)))
        pts.append((x0+s,y0+s))
        d.polygon(pts, fill=GOLD, outline=(60,50,20,255))
    elif stratum=='middle_strata':   # top hat
        d.rectangle((x0,y0+int(s*0.6),x0+s,y0+int(s*0.8)),fill=(20,20,24,255))       # brim
        d.rectangle((x0+int(s*0.2),y0,x0+int(s*0.8),y0+int(s*0.62)),fill=(20,20,24,255))  # crown
    elif stratum=='lower_strata':    # wheat sheaf (three stalks)
        for k,xx in enumerate([0.2,0.5,0.8]):
            d.line((x0+int(s*xx),y0+s,x0+int(s*xx),y0),fill=(210,180,70,255),width=max(2,int(PX*S*0.02)))
    elif stratum=='proletariat':     # hammer
        d.line((x0,y0+s,x0+s,y0),fill=(150,120,60,255),width=max(2,int(PX*S*0.03)))       # handle
        d.rectangle((x0+int(s*0.55),y0,x0+s,y0+int(s*0.28)),fill=STEEL,outline=(40,40,40,255))  # head
    elif stratum=='indentured':      # chain link
        for cx in (0.3,0.6):
            d.ellipse((x0+int(s*cx)-int(s*0.16),y0+int(s*0.3),x0+int(s*cx)+int(s*0.16),y0+int(s*0.7)),
                      outline=(180,184,190,255),width=max(2,int(PX*S*0.02)))

def metric_glyph(d, metric):
    """Central motif = what the modifier measures."""
    c=PX*S//2
    if metric=='output':             # coin with up-tick
        d.ellipse((c-int(PX*S*0.22),c-int(PX*S*0.22),c+int(PX*S*0.22),c+int(PX*S*0.22)),
                  fill=GOLD, outline=(120,90,20,255), width=max(2,int(PX*S*0.03)))
        d.line((c-int(PX*S*0.10),c+int(PX*S*0.08),c,c-int(PX*S*0.10)),fill=(120,90,20,255),width=max(2,int(PX*S*0.035)))
        d.line((c,c-int(PX*S*0.10),c+int(PX*S*0.10),c+int(PX*S*0.08)),fill=(120,90,20,255),width=max(2,int(PX*S*0.035)))
    elif metric=='happiness':        # smile
        d.ellipse((c-int(PX*S*0.24),c-int(PX*S*0.24),c+int(PX*S*0.24),c+int(PX*S*0.24)),
                  fill=(240,210,90,255), outline=(120,90,20,255), width=max(2,int(PX*S*0.03)))
        for ex in (-0.09,0.09):
            d.ellipse((c+int(PX*S*ex)-int(PX*S*0.03),c-int(PX*S*0.08),c+int(PX*S*ex)+int(PX*S*0.03),c-int(PX*S*0.02)),fill=(60,45,20,255))
        d.arc((c-int(PX*S*0.13),c-int(PX*S*0.10),c+int(PX*S*0.13),c+int(PX*S*0.14)),20,160,fill=(60,45,20,255),width=max(2,int(PX*S*0.03)))
    elif metric=='desired_pop_ratio':# two figures (a population)
        for dx in (-0.11,0.11):
            d.ellipse((c+int(PX*S*dx)-int(PX*S*0.07),c-int(PX*S*0.16),c+int(PX*S*dx)+int(PX*S*0.07),c-int(PX*S*0.02)),fill=STEEL)
            d.polygon([(c+int(PX*S*dx)-int(PX*S*0.10),c+int(PX*S*0.20)),(c+int(PX*S*dx)+int(PX*S*0.10),c+int(PX*S*0.20)),
                       (c+int(PX*S*dx)+int(PX*S*0.06),c),(c+int(PX*S*dx)-int(PX*S*0.06),c)],fill=STEEL)
    elif metric=='city_desired_pop_ratio':  # figure + city tower
        d.polygon([(c-int(PX*S*0.20),c+int(PX*S*0.20)),(c-int(PX*S*0.02),c+int(PX*S*0.20)),
                   (c-int(PX*S*0.02),c-int(PX*S*0.14)),(c-int(PX*S*0.20),c-int(PX*S*0.14))],fill=STEEL,outline=(40,40,40,255))
        for wy in (-0.09,0.02,0.13):  # windows
            d.rectangle((c-int(PX*S*0.15),c+int(PX*S*wy),c-int(PX*S*0.09),c+int(PX*S*(wy+0.05))),fill=(60,64,70,255))
        d.ellipse((c+int(PX*S*0.04),c-int(PX*S*0.16),c+int(PX*S*0.18),c-int(PX*S*0.02)),fill=GOLD)      # head
        d.polygon([(c+int(PX*S*0.02),c+int(PX*S*0.20)),(c+int(PX*S*0.20),c+int(PX*S*0.20)),
                   (c+int(PX*S*0.16),c),(c+int(PX*S*0.06),c)],fill=GOLD)

def parse_strata(fn):
    """<key>.dds -> (stratum, metric) or None if not a custom-strata modifier."""
    k=fn[:-4] if fn.endswith('.dds') else fn
    for scope in ('local_','global_','culture_'):
        if k.startswith(scope): k=k[len(scope):]; break
    else:
        return None
    for st in STRATA_COL:
        if k.startswith(st+'_'):
            metric=k[len(st)+1:]
            if metric in ('happyness','happiness'): metric='happiness'
            if metric in ('output','happiness','desired_pop_ratio','city_desired_pop_ratio'):
                return st, metric
    return None

def gen_strata():
    """Overwrite every custom-strata modifier icon with distinct (stratum x metric) art."""
    os.makedirs(OUT,exist_ok=True)
    made={}   # (stratum,metric) -> cached base path
    n=0
    for fn in sorted(os.listdir(OUT)):
        pm=parse_strata(fn)
        if not pm: continue
        st,metric=pm
        if pm not in made:
            im,d=_blade_disc(STRATA_COL[st])
            metric_glyph(d, metric)
            strata_emblem(d, st)
            made[pm]=save_base(im, f'strata_{st}_{metric}')
        shutil.copyfile(made[pm], f'{OUT}/{fn}')
        n+=1
    print(f"[#115] wrote {n} custom-strata icons across {len(made)} distinct (stratum x metric) images")
    return n

def main():
    os.makedirs(OUT,exist_ok=True)
    build_bases()
    keys=[l.strip() for l in open('tools/_missing_mods.txt') if l.strip()]
    import collections
    used=collections.Counter()
    for k in keys:
        cat=category(k); used[cat]+=1
        shutil.copyfile(BASES[cat], f'{OUT}/{k}.dds')
    print(f"wrote {len(keys)} modifier icons")
    for c,n in used.most_common(): print(f"  {n:4} <- {c}")

if __name__=='__main__':
    import sys
    if '--strata' in sys.argv:
        gen_strata()          # [#115] only refresh the strata family
    else:
        main()
        gen_strata()          # base pass copies the shared silhouette; strata pass wins for the strata family
