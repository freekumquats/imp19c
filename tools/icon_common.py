#!/usr/bin/env python3
"""Shared helpers for the key->icon-line batch drivers (missions, traditions)."""
import os, re, glob, unicodedata
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOC  = os.path.join(ROOT, "localization", "english")

def load_loc():
    """key -> english title across all english *.yml (last wins). Tolerates the
    game's `key:0 "text"` and `key: "text"` forms."""
    d = {}
    pat = re.compile(r'^\s*([A-Za-z0-9_]+):\d*\s+"(.*)"\s*$')
    for fp in glob.glob(os.path.join(LOC, "*.yml")):
        try:
            with open(fp, encoding="utf-8-sig") as f:
                for line in f:
                    m = pat.match(line)
                    if m: d[m.group(1)] = m.group(2)
        except Exception:
            pass
    return d

_STRIP = re.compile(
    r'^(Establish|Build|Found|Create|Form|Open|Launch|Restore|Secure|Seize|Take|March on|'
    r'Win over|Hold|Reading the|Read the|Back|Backing|Champion|Contest|Consolidate|Deepen|'
    r'Deepened|Restored|Install|Installing|Pacify|Pacifying|Integrate|Populate|Populating|'
    r'Settle|Settling|Contesting|Charter|Lay the|Lay|String|Assemble|Organise|Organize|'
    r'Commission|Raise|Reconquer|Reconquest of|Crush|Defeat|Repel|Expel|Cross|Round|Force|'
    r'Forcing|Carve|Carving|Land at|Landing at|Strike|Striking|Revive|Reviving|Amass|Amassing|'
    r'Fortify|Muster|Mobilise|Mobilize|Enter|Descend on|Descent on|Fall of|The)\s+',
    re.I)

def query_from_title(title, key, hint=""):
    if not title:
        return (key.replace('_', ' ') + " " + hint).strip()
    t = re.sub(r'\([^)]*\)', '', title)                 # drop (CJK/romanization)
    t = ''.join(ch for ch in t if ord(ch) < 0x2000 or ch in " -'")
    t = unicodedata.normalize('NFKD', t)
    t = re.sub(r'[^A-Za-z0-9 \-\']', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    t = _STRIP.sub('', t).strip()
    if len(t.split()) <= 1:
        t = (t + " " + hint).strip()
    return t or key.replace('_', ' ')

KEY_RE  = re.compile(r'^(\s*)([a-z][a-z0-9_]+)\s*=\s*\{\s*$')
ICON_RE = re.compile(r'^(\s*)(icon|image)\s*=\s*("?)([A-Za-z0-9_]+)\3\s*(#.*)?$')

def process_keyed_file(path, loc, outdir, donor, srcdir, log, hint="", quoted=False):
    """Repoint every `icon=`/`image=` line to its owning node key, writing bespoke art.
    quoted=True writes `icon = "<key>"` (distinctions style); else bare `icon = <key>`."""
    os.makedirs(outdir, exist_ok=True); os.makedirs(srcdir, exist_ok=True)
    lines = open(path, encoding="utf-8").readlines()
    fname = os.path.basename(path)
    changed = False; pending = None
    for idx, line in enumerate(lines):
        km = KEY_RE.match(line)
        if km:
            pending = km.group(2); continue
        im = ICON_RE.match(line)
        if im and pending:
            key = pending; pending = None
            kw = im.group(2)                              # 'icon' or 'image'
            cur = im.group(4)
            out = os.path.join(outdir, key + ".dds")
            if not os.path.exists(out):
                title = loc.get(key)
                q = query_from_title(title, key, hint)
                src = os.path.join(srcdir, key + ".jpg")
                try:
                    if not os.path.exists(src):
                        _, desc = fetch(("search", q), src, width=360)
                    else:
                        desc = "cached"
                    convert(src, out, like=donor)
                    log.write(f"{fname}\t{key}\t{title}\t{q}\t{desc}\tOK\n")
                except Exception as e:
                    log.write(f"{fname}\t{key}\t{title}\t{q}\tERR\t{e}\n")
                    print(f"  ERR {key}: {e}"); continue
            if cur != key:
                q = f'"{key}"' if quoted else key
                indent = im.group(1)
                lines[idx] = f"{indent}{kw} = {q}\n"
                changed = True
    if changed:
        open(path, "w", encoding="utf-8").writelines(lines)
    return changed
