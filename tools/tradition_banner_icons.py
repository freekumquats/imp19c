#!/usr/bin/env python3
"""
tradition_banner_icons.py — redraw 4 flagged Qing/Japan military-tradition HEADER icons
(#101-#104) as clean banner emblems, replacing bad photo crops / wrong-colour art.

Header format: 198x72, legacy uncompressed BGRA8 (pfflags 0x41, fourcc 0, bits 32) —
verified against qing_mongol_cavalry_tradition.dds. Resolved by filename
gfx/interface/icons/military_traditions/<key>.dds. Drawn at 4x supersample, downsampled.

  qing_green_standard_tradition  — a GREEN field with a hung pennant (the 綠營's colour;
                                   the prior art was a dark bull photo, not green at all).
  qing_eight_banners_tradition   — the actual EIGHT BANNERS in a row: the 4 plain + 4
                                   bordered banners in their historical colours (yellow,
                                   white, red, blue), like several embroidered flags.
  qing_frontier_defence_tradition— a Great-Wall watchtower silhouette on a dusk sky
                                   (a clean emblem, not a bad photo).
  japanese_philosophy_start_bonus— the Rising Sun (日章旗/旭日旗): red disc + rays on white.
"""
import struct, os, math
from PIL import Image, ImageDraw
import numpy as np

DDPF_ALPHAPIXELS=0x1; DDPF_RGB=0x40
DDSD_CAPS=0x1; DDSD_HEIGHT=0x2; DDSD_WIDTH=0x4; DDSD_PITCH=0x8; DDSD_PIXELFORMAT=0x1000
DDSD_MIPMAPCOUNT=0x20000
DDSCAPS_TEXTURE=0x1000
OUT='gfx/interface/icons/military_traditions'
W,H=198,72
S=4

def write_dds_bgra8_mip1(path, rgba):
    """Legacy 124-byte BGRA8 header WITH mipcount=1 flag — matches the tradition headers
    (flags 0x2100f, pfflags 0x41)."""
    h,w,_=rgba.shape
    pitch=w*4
    flags=DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH|DDSD_PITCH|DDSD_PIXELFORMAT|DDSD_MIPMAPCOUNT
    hdr=bytearray(124)
    struct.pack_into('<I',hdr,0,124)
    struct.pack_into('<I',hdr,4,flags)
    struct.pack_into('<I',hdr,8,h)
    struct.pack_into('<I',hdr,12,w)
    struct.pack_into('<I',hdr,16,pitch)
    struct.pack_into('<I',hdr,24,1)                  # mipcount
    struct.pack_into('<I',hdr,72,32)
    struct.pack_into('<I',hdr,76,DDPF_ALPHAPIXELS|DDPF_RGB)  # 0x41
    struct.pack_into('<I',hdr,84,32)
    struct.pack_into('<I',hdr,88,0x00FF0000)
    struct.pack_into('<I',hdr,92,0x0000FF00)
    struct.pack_into('<I',hdr,96,0x000000FF)
    struct.pack_into('<I',hdr,100,0xFF000000)
    struct.pack_into('<I',hdr,104,DDSCAPS_TEXTURE)
    bgra=rgba[:,:,[2,1,0,3]].astype(np.uint8)
    with open(path,'wb') as f:
        f.write(b'DDS '); f.write(bytes(hdr)); f.write(bgra.tobytes())

def canvas():
    return Image.new('RGBA',(W*S,H*S),(0,0,0,255))

def finalize(im, key):
    im=im.resize((W,H),Image.LANCZOS)
    write_dds_bgra8_mip1(os.path.join(OUT,f'{key}.dds'), np.asarray(im,dtype=np.uint8))
    print("wrote",key)

def vgrad(d, box, top, bot):
    x0,y0,x1,y1=box
    for y in range(y0,y1):
        t=(y-y0)/max(1,(y1-y0))
        col=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))+(255,)
        d.line((x0,y,x1,y),fill=col)

def pennant(d, x, y, w, h, fill, border=None, bw=0):
    """A hung triangular pennant: rectangle top, tapering to a point at the bottom-right
    (swallow-tail style banner). Point down-right like a hanging military flag."""
    pts=[(x,y),(x+w,y),(x+w,y+h*0.62),(x+w*0.5,y+h),(x,y+h*0.62)]
    if border:
        d.polygon([(px,py) for px,py in pts], fill=border)
        inner=[(x+bw,y+bw),(x+w-bw,y+bw),(x+w-bw,y+h*0.62-bw),(x+w*0.5,y+h-bw*1.6),(x+bw,y+h*0.62-bw)]
        d.polygon(inner, fill=fill)
    else:
        d.polygon([(px,py) for px,py in pts], fill=fill)

def draw_green_standard(key):
    im=canvas(); d=ImageDraw.Draw(im)
    vgrad(d,(0,0,W*S,H*S),(18,54,28),(30,92,44))          # deep green field
    # a large hung green pennant with a gold pole + finial, centred
    px=int(W*S*0.30)
    d.rectangle((px-4*S,int(H*S*0.10),px,int(H*S*0.92)),fill=(196,150,60,255))   # gold pole
    d.ellipse((px-7*S,int(H*S*0.06),px+1*S,int(H*S*0.14)),fill=(230,196,90,255)) # finial
    pennant(d,px,int(H*S*0.14),int(W*S*0.42),int(H*S*0.66),
            fill=(46,140,66,255),border=(232,206,110,255),bw=3*S)               # green flag, gold trim
    # a small gold sunburst emblem on the flag
    cx,cy=px+int(W*S*0.20),int(H*S*0.40)
    for a in range(0,360,45):
        dx,dy=math.cos(math.radians(a)),math.sin(math.radians(a))
        d.line((cx,cy,cx+dx*10*S,cy+dy*10*S),fill=(232,206,110,255),width=2*S)
    d.ellipse((cx-5*S,cy-5*S,cx+5*S,cy+5*S),fill=(232,206,110,255))
    finalize(im,key)

def draw_eight_banners(key):
    # The eight banners in a row: 4 plain + 4 bordered, historical colours.
    im=canvas(); d=ImageDraw.Draw(im)
    vgrad(d,(0,0,W*S,H*S),(28,30,42),(46,50,66))          # slate field so all colours pop
    colours=[  # (field, border-or-None). Plain then Bordered for each colour.
        ((240,196,44), None),          # Plain Yellow 正黃
        ((240,196,44), (196,36,36)),   # Bordered Yellow 鑲黃 (red border)
        ((238,238,238), None),         # Plain White 正白
        ((238,238,238), (196,36,36)),  # Bordered White 鑲白 (red border)
        ((196,36,36), None),           # Plain Red 正紅
        ((196,36,36), (238,238,238)),  # Bordered Red 鑲紅 (white border)
        ((40,70,150), None),           # Plain Blue 正藍
        ((40,70,150), (196,36,36)),    # Bordered Blue 鑲藍 (red border)
    ]
    n=8; margin=int(W*S*0.03)
    slot=(W*S-2*margin)/n
    fw=int(slot*0.62); gap=slot-fw
    fh=int(H*S*0.66); top=int(H*S*0.16)
    for i,(field,bord) in enumerate(colours):
        x=int(margin+i*slot+gap*0.5)
        # tiny pole
        d.rectangle((x-2*S,top,x,top+fh+int(H*S*0.06)),fill=(150,120,60,255))
        pennant(d,x,top,fw,fh,fill=field+(255,),
                border=(bord+(255,)) if bord else None, bw=2*S)
    finalize(im,key)

def draw_frontier_defence(key):
    im=canvas(); d=ImageDraw.Draw(im)
    vgrad(d,(0,0,W*S,H*S),(196,150,96),(120,86,58))       # dusk desert sky
    # sun disc low behind the wall
    d.ellipse((int(W*S*0.60),int(H*S*0.18),int(W*S*0.60)+22*S,int(H*S*0.18)+22*S),
              fill=(244,214,150,255))
    # Great-Wall silhouette: a ridge line with crenellated watchtowers
    base=int(H*S*0.86)
    wall=(58,46,40,255)
    ridge=[(0,int(H*S*0.72))]
    xs=[0,0.14,0.30,0.46,0.62,0.78,0.92,1.0]
    ys=[0.72,0.66,0.70,0.62,0.68,0.60,0.66,0.70]
    pts=[(int(W*S*x),int(H*S*y)) for x,y in zip(xs,ys)]
    poly=pts+[(W*S,base),(0,base)]
    d.polygon(poly,fill=wall)
    # crenellations on the ridge
    for (x,y) in pts:
        d.rectangle((x-3*S,y-6*S,x+3*S,y),fill=wall)
    # two square watchtowers
    for tx in (0.30,0.78):
        x=int(W*S*tx)
        d.rectangle((x-9*S,int(H*S*0.44),x+9*S,base),fill=(70,56,48,255))
        for cx in (x-9*S,x-2*S,x+5*S):
            d.rectangle((cx,int(H*S*0.44)-5*S,cx+4*S,int(H*S*0.44)),fill=(70,56,48,255))
    finalize(im,key)

def draw_rising_sun(key):
    im=canvas(); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W*S,H*S),fill=(244,244,240,255))     # white field
    cx,cy=int(W*S*0.5),int(H*S*0.5)
    red=(200,32,42,255)
    # 16 rays
    R=W*S
    for k in range(16):
        a0=math.radians(k*22.5); a1=math.radians(k*22.5+11.25)
        d.polygon([(cx,cy),
                   (cx+math.cos(a0)*R,cy+math.sin(a0)*R),
                   (cx+math.cos(a1)*R,cy+math.sin(a1)*R)],fill=red)
    # central disc
    r=int(H*S*0.30)
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=red)
    finalize(im,key)

BUILDERS={
    'qing_green_standard_tradition': draw_green_standard,
    'qing_eight_banners_tradition': draw_eight_banners,
    'qing_frontier_defence_tradition': draw_frontier_defence,
    'japanese_philosophy_start_bonus': draw_rising_sun,
}

if __name__=='__main__':
    for k,fn in BUILDERS.items():
        fn(k)
