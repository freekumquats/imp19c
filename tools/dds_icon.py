#!/usr/bin/env python3
"""
dds_icon.py — mechanical reference-photo -> game DDS icon converter for imp19c.

Produces uncompressed 32-bit BGRA8 (A8R8G8B8) DDS files matching the mod's existing
icons (verified against gfx/interface/icons/tradegoods/coal.dds and
menu_buttons/menu_trade.dds): 124-byte DDS header, no mipmaps, non-power-of-two OK,
masks R=0x00FF0000 G=0x0000FF00 B=0x000000FF A=0xFF000000 (BGRA byte order in memory).

Pipeline (mechanical conversion, option (i)):
  source raster  -> center square-crop -> resize to target WxH -> apply alpha mask -> DDS

The alpha mask is BORROWED from the sibling icon the new art replaces, so the rounded /
soft-edge shape matches its icon family byte-for-byte. If no sibling is given, a soft
circular mask is synthesized.

Usage:
  dds_icon.py --src IN.(jpg|png) --out OUT.dds --like SIBLING.dds
  dds_icon.py --src IN.jpg       --out OUT.dds --size 50   # synth circular alpha
  dds_icon.py --probe SOME.dds                             # print header + alpha stats
"""
import argparse, struct, sys
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

DDSD_CAPS=0x1; DDSD_HEIGHT=0x2; DDSD_WIDTH=0x4; DDSD_PITCH=0x8
DDSD_PIXELFORMAT=0x1000
DDPF_ALPHAPIXELS=0x1; DDPF_RGB=0x40
DDSCAPS_TEXTURE=0x1000

def write_dds_dxt5(path, rgba):
    """Compressed DXT5 (FourCC 'DXT5') via Pillow.
    NOTE: the mission-task / mission-header widgets REJECT this (they show placeholder);
    they require the DX10 BGRA8-sRGB layout — use write_dds_dx10_bgra8 for those."""
    from PIL import Image
    im = Image.fromarray(rgba.astype(np.uint8), 'RGBA')
    im.save(path, pixel_format='DXT5')

def write_dds_dx10_bgra8(path, rgba):
    """Uncompressed BGRA8 with a DX10 extended header, dxgiFormat=91
    (DXGI_FORMAT_B8G8R8A8_UNORM_SRGB), 1 mip. This is the EXACT layout of the
    stock/vanilla mission icons (e.g. russian_missions_1_10.dds) that render
    correctly in the mission-task + mission-header widgets. Those widgets reject
    BOTH plain-FourCC DXT5 AND the legacy 124-byte BGRA8 header (pfflags 0x41) —
    only this DX10 form works. rgba: HxWx4 uint8, R,G,B,A order."""
    h, w, _ = rgba.shape
    pitch = w * 4
    flags = DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH|DDSD_PITCH|DDSD_PIXELFORMAT  # 0x2100f w/ mips flag below
    flags |= 0x20000                                    # DDSD_MIPMAPCOUNT (matches vanilla 0x2100f)
    header = bytearray(124)
    struct.pack_into('<I', header, 0, 124)              # dwSize
    struct.pack_into('<I', header, 4, flags)            # dwFlags = 0x2100f
    struct.pack_into('<I', header, 8, h)                # dwHeight
    struct.pack_into('<I', header, 12, w)               # dwWidth
    struct.pack_into('<I', header, 16, pitch)           # dwPitchOrLinearSize
    struct.pack_into('<I', header, 20, 1)               # dwDepth = 1 (vanilla)
    struct.pack_into('<I', header, 24, 1)               # dwMipMapCount = 1
    # pixel format at offset 72: FourCC 'DX10', no masks
    struct.pack_into('<I', header, 72, 32)              # pf.dwSize
    struct.pack_into('<I', header, 76, 0x4)             # pf.dwFlags = DDPF_FOURCC
    header[80:84] = b'DX10'                              # pf.dwFourCC (offset 80, NOT 84 = RGBBitCount)
    struct.pack_into('<I', header, 104, DDSCAPS_TEXTURE)# caps1 = 0x1000
    # DX10 extended header (20 bytes)
    dx10 = struct.pack('<5I', 91, 3, 0, 1, 0)           # dxgiFormat=91, resDim=3(TEXTURE2D), misc=0, arraySize=1, misc2=0
    bgra = rgba[:, :, [2,1,0,3]].astype(np.uint8)       # R,G,B,A -> B,G,R,A
    with open(path, 'wb') as f:
        f.write(b'DDS '); f.write(bytes(header)); f.write(dx10); f.write(bgra.tobytes())

def write_dds_bgra8(path, rgba):
    """rgba: HxWx4 uint8 numpy array in R,G,B,A order."""
    h, w, _ = rgba.shape
    pitch = w * 4
    flags = DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH|DDSD_PITCH|DDSD_PIXELFORMAT
    header = bytearray(124)
    struct.pack_into('<I', header, 0, 124)              # dwSize
    struct.pack_into('<I', header, 4, flags)            # dwFlags
    struct.pack_into('<I', header, 8, h)                # dwHeight
    struct.pack_into('<I', header, 12, w)               # dwWidth
    struct.pack_into('<I', header, 16, pitch)           # dwPitchOrLinearSize
    struct.pack_into('<I', header, 20, 0)               # dwDepth
    struct.pack_into('<I', header, 24, 1)               # dwMipMapCount
    # pixel format at offset 72 within header
    struct.pack_into('<I', header, 72, 32)              # pf.dwSize
    struct.pack_into('<I', header, 76, DDPF_ALPHAPIXELS|DDPF_RGB) # pf.dwFlags = 0x41
    struct.pack_into('<I', header, 80, 0)               # pf.dwFourCC
    struct.pack_into('<I', header, 84, 32)              # pf.dwRGBBitCount
    struct.pack_into('<I', header, 88, 0x00FF0000)      # R mask
    struct.pack_into('<I', header, 92, 0x0000FF00)      # G mask
    struct.pack_into('<I', header, 96, 0x000000FF)      # B mask
    struct.pack_into('<I', header, 100, 0xFF000000)     # A mask
    struct.pack_into('<I', header, 104, DDSCAPS_TEXTURE)# caps1
    # In-memory byte order for these masks is B,G,R,A per pixel.
    bgra = rgba[:, :, [2,1,0,3]].astype(np.uint8)
    with open(path, 'wb') as f:
        f.write(b'DDS ')
        f.write(bytes(header))
        f.write(bgra.tobytes())

def read_dds_dims(path):
    """Read (width,height) from ANY DDS header, regardless of pixel format."""
    with open(path,'rb') as f: h=f.read(128)
    assert h[:4]==b'DDS ', "not a DDS"
    height,width=struct.unpack('<2I', h[12:20])
    return width,height

def is_uncompressed_bgra8(path):
    """True iff the DDS is the 32-bit RGB+ALPHA layout our reader can decode."""
    with open(path,'rb') as f: h=f.read(128)
    if h[:4]!=b'DDS ': return False
    pfflags,fourcc,bits=struct.unpack('<3I', h[80:92])
    return (pfflags & DDPF_RGB) and bits==32 and fourcc==0

def read_dds_bgra8(path):
    with open(path,'rb') as f: b=f.read()
    assert b[:4]==b'DDS ', "not a DDS"
    h=b[4:128]
    height,width,pitch=struct.unpack('<3I', h[8:20])
    px=np.frombuffer(b[128:128+width*height*4], dtype=np.uint8).reshape(height,width,4)
    # stored B,G,R,A -> return R,G,B,A
    return px[:, :, [2,1,0,3]].copy(), (width,height)

def center_square_crop(im):
    w,h=im.size; s=min(w,h)
    l=(w-s)//2; t=(h-s)//2
    return im.crop((l,t,l+s,t+s))

def center_aspect_crop(im, tw, th):
    """Center-crop the source to the TARGET aspect ratio (tw:th) so the subsequent
    resize does not stretch it. For a wide banner (198x72) this takes a wide strip
    from the middle of the photo rather than squashing a square."""
    w,h=im.size
    target=tw/th; cur=w/h
    if cur>target:                      # source too wide -> crop width
        nw=int(round(h*target)); l=(w-nw)//2
        return im.crop((l,0,l+nw,h))
    else:                               # source too tall -> crop height
        nh=int(round(w/target)); t=(h-nh)//2
        return im.crop((0,t,w,t+nh))

def synth_circular_alpha(size):
    yy,xx=np.mgrid[0:size,0:size]
    cx=cy=(size-1)/2.0
    r=np.sqrt((xx-cx)**2+(yy-cy)**2)
    rmax=size/2.0
    # soft edge over the outer ~8% of the radius
    a=np.clip((rmax-r)/(rmax*0.08),0,1)
    return (a*255).astype(np.uint8)

def convert(src, out, like=None, size=None, enhance=True, dxt5=False, dx10=False):
    im=Image.open(src).convert('RGB')
    # target size: from the donor's header (any format) or explicit --size.
    if like:
        tw,th=read_dds_dims(like)
    else:
        tw=th=size or 50
    # crop to the TARGET aspect ratio (not always square) so wide banners aren't stretched.
    im=center_aspect_crop(im, tw, th)
    if enhance:
        # tiny photo-derived icons crush to a dark blob otherwise: stretch histogram
        # (clip 2% tails) and lift saturation a touch so the concept is legible at 50px.
        im=ImageOps.autocontrast(im, cutoff=2)
        im=ImageEnhance.Color(im).enhance(1.25)
    im=im.resize((tw,th), Image.LANCZOS)
    rgb=np.asarray(im,dtype=np.uint8)
    # alpha: borrow the donor's SHAPED alpha only if the donor is a decodable
    # uncompressed BGRA8 with a genuine shape (panel headers / tradegoods). For
    # compressed donors (DX10/DXT, e.g. mission tasks, buildings) or square art we
    # can't decode, keep the icon fully opaque — matching those donors, which are
    # opaque rectangles (verified distinct-alpha <= 2).
    alpha=None
    if like and is_uncompressed_bgra8(like):
        sib,_=read_dds_bgra8(like)
        a=sib[:, :, 3]
        if len(np.unique(a))>4:               # genuinely shaped, not ~opaque
            if a.shape!=(th,tw):
                a=np.asarray(Image.fromarray(a).resize((tw,th),Image.LANCZOS))
            alpha=a
    if alpha is None:
        alpha=np.full((th,tw),255,dtype=np.uint8)
    rgba=np.dstack([rgb, alpha]).astype(np.uint8)
    # [#125] The mission-task / mission-header widgets REJECT both legacy 124-byte BGRA8
    # (pfflags 0x41) and plain-FourCC DXT5, silently showing the engine placeholder. They
    # accept ONLY the DX10 BGRA8-sRGB layout (matches stock russian_missions_1_10.dds). So
    # mission icons MUST pass dx10=True; other icon families keep the legacy BGRA8 writer.
    if dx10:
        write_dds_dx10_bgra8(out, rgba)
    elif dxt5:
        write_dds_dxt5(out, rgba)
    else:
        write_dds_bgra8(out, rgba)
    return (tw,th)

def probe(path):
    with open(path,'rb') as f: b=f.read()
    # file offsets = 4-byte magic + DDS_HEADER field offset
    height,width,pitch=struct.unpack('<3I', b[12:24])   # hdr +8,+12,+16
    mips=struct.unpack('<I', b[28:32])[0]               # hdr +24
    # pixel format block starts at hdr +72 (file +76): dwSize,dwFlags,dwFourCC,dwRGBBitCount,masks
    pfsize,pfflags,fourcc,bits=struct.unpack('<4I', b[76:92])
    masks=struct.unpack('<4I', b[92:108])
    fcc=struct.pack('<I',fourcc).rstrip(b'\x00').decode('latin1') if fourcc else '0'
    print(f"{path}: {width}x{height} pitch={pitch} mips={mips} pfflags={hex(pfflags)} "
          f"fourcc={fcc} bits={bits} masks={[hex(m) for m in masks]}")
    if is_uncompressed_bgra8(path):
        rgba,_=read_dds_bgra8(path)
        a=rgba[:,:,3]
        print(f"  alpha: min={a.min()} max={a.max()} distinct={len(np.unique(a))} "
              f"opaque={(a==255).sum()} transparent={(a==0).sum()}/{a.size}")
    else:
        print("  (compressed/non-BGRA8 donor — alpha not decoded)")

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--src'); ap.add_argument('--out')
    ap.add_argument('--like'); ap.add_argument('--size', type=int)
    ap.add_argument('--no-enhance', action='store_true')
    ap.add_argument('--dx10', action='store_true', help='DX10 BGRA8 layout (required for mission icons)')
    ap.add_argument('--probe')
    a=ap.parse_args()
    if a.probe:
        probe(a.probe); sys.exit(0)
    if not (a.src and a.out):
        ap.error("need --src and --out (or --probe)")
    wh=convert(a.src, a.out, like=a.like, size=a.size, enhance=not a.no_enhance, dx10=a.dx10)
    print(f"wrote {a.out} {wh[0]}x{wh[1]}")
    probe(a.out)
