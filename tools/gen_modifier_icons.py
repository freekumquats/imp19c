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
    main()
