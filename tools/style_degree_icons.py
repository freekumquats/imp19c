#!/usr/bin/env python3
"""
style_degree_icons.py — restyle the exam-degree trait icons (tasks #4 + #5).

The exam-degree trait icons (civil: shengyuan/juren/gongshi/jinshi/hanlin/fanyi_jinshi;
military 武: wu_shengyuan/wu_juren/wu_jinshi/wu_zhuangyuan) are 54x54 uncompressed BGRA8
circular discs — an inscribed circle (transparent corners), a light background fill, and a
dark ink calligraphy glyph of the degree name on top. The original calligraphy render was a
one-off; this is the COMMITTED, reusable, idempotent post-processor that applies two styling
passes on top of the existing art (it does NOT re-render the calligraphy):

  #4  GOLD BORDER — paint a gold rim annulus at the disc's outer edge (both civil + military),
      following the existing circular alpha so the rim is round and antialiased.
  #5  WHITE -> PARCHMENT — recolor the light, low-saturation background pixels (the CIVIL set's
      white fill) to a warm parchment. The MILITARY set's background is deliberately GREEN (the
      martial 武 distinguisher, NOT white) — the low-saturation gate spares it, so green stays.
      Decision (logged in overnight/OVERNIGHT_2026_08_09.md): #5 says "white -> parchment", and
      the military green is not white; recoloring it too would erase the martial marker. Rejected
      alt: recolor military green -> parchment-green for uniformity — dropped, the gold border
      already unifies the two sets (parchment+gold = civil, green+gold = martial).

The ink glyph (dark pixels) and the transparent corners are untouched by both passes.

Idempotent by construction: the parchment recolor targets light AND LOW-SATURATION pixels
(lum>165 AND sat<0.14). Parchment RGB(228,208,165) is light (lum≈209) but its SATURATION is
≈0.276 — well above the 0.14 gate — so an already-parchment fill is NOT re-targeted on a second
run (saturation, not brightness, is what spares it — see the assert below). The gold rim
overwrites the same annulus to the same colour. Safe to re-run (verified byte-identical).

Run under a venv with numpy (dds_icon needs it). Usage:
    python3 tools/style_degree_icons.py            # restyle in place
    python3 tools/style_degree_icons.py --preview  # also write /tmp preview contact sheets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from dds_icon import read_dds_bgra8, write_dds_bgra8

TRAITS_DIR = os.path.join(os.path.dirname(__file__), "..", "gfx", "interface", "icons", "traits")
CIVIL = ["shengyuan", "juren", "gongshi", "jinshi", "hanlin", "fanyi_jinshi"]
MILITARY = ["wu_shengyuan", "wu_juren", "wu_jinshi", "wu_zhuangyuan"]
KEYS = CIVIL + MILITARY

# Warm aged-parchment (河工-era memorial paper). Sits well below "near-white" so re-runs no-op.
PARCHMENT = np.array([228, 208, 165], dtype="float32")   # R,G,B
# Classic imperial gold for the rim.
GOLD = np.array([201, 162, 57], dtype="float32")         # R,G,B
GOLD_HI = np.array([232, 199, 104], dtype="float32")     # lighter gold, outer highlight


def _luma(rgb):
    return 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]


def _saturation(rgb):
    mx = rgb.max(axis=-1)
    mn = rgb.min(axis=-1)
    return np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-3), 0.0)


# Idempotency invariant: the parchment output must NOT itself satisfy the recolor target
# (lum>165 AND sat<0.14), or a second run would re-recolor it and drift. Saturation is the guard.
assert float(_saturation(PARCHMENT)) >= 0.14, "PARCHMENT saturation must stay above the recolor gate (idempotency)"


def restyle(rgba, parchment=True):
    """rgba: HxWx4 uint8. Returns a restyled copy (uint8). parchment=True does the #5 white->
    parchment recolor (CIVIL set); pass False for the MILITARY set to leave its green fill intact."""
    a = rgba.astype("float32")
    h, w, _ = a.shape
    rgb = a[..., :3]
    alpha = a[..., 3]

    # --- #5 parchment: recolor the WHITE background (CIVIL set only — the caller passes
    # parchment=False for the MILITARY set so its deliberate green martial marker survives; the
    # green is too near-white for a robust per-pixel saturation gate, so we gate by FILE instead).
    # A background pixel is light AND low-saturation (neutral white) AND at least partly opaque.
    # The luma>165 gate (not any per-pixel blend) is what preserves the dark ink glyph cores;
    # the recolor is a hard assignment, so light antialiased edge pixels are fully replaced. ---
    if parchment:
        lum = _luma(rgb)
        sat = _saturation(rgb)
        bg_mask = (lum > 165.0) & (sat < 0.14) & (alpha > 8.0)
        if bg_mask.any():
            # preserve subtle shading: scale parchment by how bright the source was (near 1.0 for
            # the ~238 white fill), so any faint vignette in the original disc survives the recolor.
            scale = np.clip(lum[bg_mask] / 238.0, 0.80, 1.0)[:, None]
            rgb[bg_mask] = PARCHMENT[None, :] * scale

    # --- #4 gold rim: annulus at the disc's outer edge. The disc is the inscribed circle, so use
    # the geometric radius from centre; gate on existing alpha so the rim inherits the round,
    # antialiased outer boundary (never paints into the transparent corners). ---
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2)
    r_outer = min(cy, cx)               # inscribed-circle radius (~26.5 for 54px)
    r_in = r_outer - 3.2                # ~3px rim
    rim = (r >= r_in) & (alpha > 8.0)
    if rim.any():
        # radial gold gradient: lighter at the very edge, deeper just inside, for a beaded look.
        t = np.clip((r[rim] - r_in) / max(r_outer - r_in, 1e-3), 0.0, 1.0)[:, None]
        rgb[rim] = GOLD[None, :] * (1.0 - t) + GOLD_HI[None, :] * t

    out = np.empty_like(a)
    out[..., :3] = np.clip(rgb, 0, 255)
    out[..., 3] = alpha                 # alpha (circle shape) preserved exactly
    return out.astype("uint8")


def main():
    preview = "--preview" in sys.argv
    before_tiles, after_tiles = [], []
    for k in KEYS:
        p = os.path.join(TRAITS_DIR, k + ".dds")
        rgba, _ = read_dds_bgra8(p)
        src = np.asarray(rgba, dtype="uint8")
        dst = restyle(src, parchment=(k in CIVIL))
        write_dds_bgra8(p, dst)
        print(f"restyled {k}.dds ({'civil/parchment' if k in CIVIL else 'military/green kept'} + gold rim)")
        if preview:
            before_tiles.append(src)
            after_tiles.append(dst)  # dst already restyled with the per-set parchment flag
    if preview:
        try:
            from PIL import Image
        except Exception as e:
            print("preview needs PIL:", e); return
        for name, tiles in (("before", before_tiles), ("after", after_tiles)):
            sz, pad, cols = 54, 6, 5
            rows = (len(tiles) + cols - 1) // cols
            sheet = Image.new("RGBA", (cols * (sz + pad) + pad, rows * (sz + pad) + pad), (110, 110, 110, 255))
            for i, t in enumerate(tiles):
                im = Image.fromarray(t, "RGBA")
                rr, cc = divmod(i, cols)
                sheet.alpha_composite(im, (pad + cc * (sz + pad), pad + rr * (sz + pad)))
            outp = f"/tmp/degree_icons_{name}.png"
            sheet.save(outp)
            print("wrote", outp)


if __name__ == "__main__":
    main()
