#!/usr/bin/env python3
"""
gen_mission_icons.py — batch bespoke mission-task icons for the Qing mission suite.

For each qing_*_missions.txt: find every task node that carries `icon = testN`, look up
the task's English loc title, derive a Wikimedia Commons search query from it, fetch the
top image, convert to a 118x68 BGRA8 DDS (donor = mission_tasks/test1.dds), write it to
gfx/interface/icons/mission_tasks/<taskkey>.dds, and repoint the `icon =` line to <taskkey>.

Idempotent: skips a task whose .dds already exists AND whose icon line already points to it.
Logs every (task -> query -> image) decision to tools/mission_icon_log.tsv.
"""
import os, re, sys, glob, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISS = os.path.join(ROOT, "common", "missions")
LOC  = os.path.join(ROOT, "localization", "english")
OUT  = os.path.join(ROOT, "gfx", "interface", "icons", "mission_tasks")
SRC  = os.path.join(ROOT, "art_src", "mission")
DONOR= os.path.join(OUT, "test1.dds")
LOG  = os.path.join(ROOT, "tools", "mission_icon_log.tsv")

os.makedirs(SRC, exist_ok=True)

# task keys that are NOT icon-bearing tasks (the tree root uses icon= too but is fine to skip
# repointing — however giving the root its own art is harmless; we handle all icon= owners).
ROOT_SUFFIX = "_mission"

def load_loc():
    """key -> english title, across all english yml (last wins)."""
    d = {}
    pat = re.compile(r'^\s*([A-Za-z0-9_]+):\d*\s+"(.*)"\s*$')
    for fp in glob.glob(os.path.join(LOC, "*.yml")):
        try:
            with open(fp, encoding="utf-8-sig") as f:
                for line in f:
                    m = pat.match(line)
                    if m:
                        d[m.group(1)] = m.group(2)
        except Exception:
            pass
    return d

def query_from_title(title, key):
    """Strip CJK, parenthetical romanizations, verbs -> a concept noun phrase for Commons."""
    # drop bracketed CJK e.g. "(總理衙門)"
    t = re.sub(r'\([^)]*\)', '', title)
    # remove any remaining CJK / non-latin
    t = ''.join(ch for ch in t if ord(ch) < 0x2000 or ch in " -'")
    t = unicodedata.normalize('NFKD', t)
    t = re.sub(r'[^A-Za-z0-9 \-\']', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    # trim leading imperative verbs that hurt image search
    t = re.sub(r'^(Establish|Build|Found|Create|Form|Open|Launch|Restore|Secure|Seize|'
               r'Take|March on|Win over|Hold|Reading the|Read the|Back|Backing|Champion|'
               r'Contest|Consolidate|Deepen|Deepened|Restored|Install|Installing|Pacify|'
               r'Pacifying|Integrate|Populate|Populating|Settle|Settling|Contesting|'
               r'Charter|Lay|Lay the|String|Assemble|Organise|Organize|Commission|Raise|'
               r'Reconquer|Reconquest of|Crush|Defeat|Repel|Expel|Cross|Round|Force|Forcing|'
               r'Carve|Carving|Land at|Landing at|Strike|Striking|Revive|Reviving|Amass|'
               r'Amassing|Fortify|Muster|Mobilise|Mobilize|Enter|Descend on|Descent on|Fall of)\s+',
               '', t, flags=re.I).strip()
    # append a China/Qing hint for very short/ambiguous queries
    if len(t.split()) <= 1:
        t = (t + " Qing dynasty China").strip()
    return t or key.replace('_', ' ')

# regex: a task node key line "  <key> = {"
KEY_RE = re.compile(r'^(\s*)([a-z][a-z0-9_]+)\s*=\s*\{\s*$')
ICON_RE = re.compile(r'^(\s*)icon\s*=\s*(\S+)\s*$')

def process_file(path, loc, log):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    # find task keys and the icon= line that immediately (within a few lines) follows
    changed = False
    fname = os.path.basename(path)
    i = 0
    # Track the most recent key seen so an icon= line can be attributed to it.
    pending_key = None
    for idx, line in enumerate(lines):
        km = KEY_RE.match(line)
        if km:
            pending_key = km.group(2)
            continue
        im = ICON_RE.match(line)
        if im and pending_key:
            key = pending_key
            pending_key = None
            # skip the tree-root node's icon (still give art? -> yes for completeness, but keep testN if it's the root wrapper)
            title = loc.get(key)
            out_dds = os.path.join(OUT, key + ".dds")
            cur = im.group(2)
            need_convert = not os.path.exists(out_dds)
            need_repoint = (cur != key)
            if not need_convert and not need_repoint:
                continue
            if need_convert:
                query = query_from_title(title, key) if title else key.replace('_', ' ')
                src = os.path.join(SRC, key + ".jpg")
                try:
                    if not os.path.exists(src):
                        _, desc = fetch(("search", query), src, width=320)
                    else:
                        desc = "cached"
                    convert(src, out_dds, like=DONOR)
                    log.write(f"{fname}\t{key}\t{title}\t{query}\t{desc}\tOK\n")
                except Exception as e:
                    log.write(f"{fname}\t{key}\t{title}\t{query}\tERR\t{e}\n")
                    print(f"  ERR {key}: {e}")
                    continue
            # repoint icon line
            if cur != key:
                lines[idx] = f"{im.group(1)}icon = {key}\n"
                changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    return changed

def main():
    loc = load_loc()
    files = sorted(glob.glob(os.path.join(MISS, "qing_*_missions.txt")))
    with open(LOG, "w", encoding="utf-8") as log:
        log.write("file\tkey\ttitle\tquery\tsource\tstatus\n")
        for fp in files:
            print("==", os.path.basename(fp))
            process_file(fp, loc, log)
    print("done; log ->", LOG)

if __name__ == "__main__":
    main()
