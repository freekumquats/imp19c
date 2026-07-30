#!/usr/bin/env python3
"""
gen_mission_icons.py — batch bespoke mission-task icons for the Qing mission suite.

For each qing_*_missions.txt: find every task node that carries `icon = testN`, look up
the task's English loc title, derive a Wikimedia Commons search query from it, fetch the
top image, convert to a 320x320 square DX10 BGRA8 DDS (matching Terra Indomita's mission-task
icon geometry — the mission_view.gui task widget renders every icon at ~128x133, so a SQUARE
source downscales cleanly whereas a wide 118x68 strip is stretched ~2x vertically and, being
opaque and full-bleed, overflows the 112px node cell and collides with neighbouring nodes), write it to
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

# [#125] Curated per-task search queries live in tools/mission_task_queries.py (one query per
# task, aimed at period artwork). A task key present there overrides query_from_title entirely.
try:
    from mission_task_queries import CONCEPT_QUERY
except Exception:
    CONCEPT_QUERY = {}
# [#126/#127] the breadth-expansion tasks carry their own curated period-art query in the
# content table; merge them in (content-table query wins for its own keys).
try:
    from mission_task_content import CONTENT_QUERY
    CONCEPT_QUERY = {**CONCEPT_QUERY, **CONTENT_QUERY}
except Exception:
    pass

# regex: a task node key line "  <key> = {"
KEY_RE = re.compile(r'^(\s*)([a-z][a-z0-9_]+)\s*=\s*\{\s*$')
ICON_RE = re.compile(r'^(\s*)icon\s*=\s*(\S+)\s*$')

def process_file(path, loc, log, force=False):
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
            # [#125] Skip the tree-root node (icon = qing_<tree>_mission). Its art is the
            # curated selector CARD written by gen_mission_headers.py (PHOTOS table); fetching
            # a generic search image here would clobber that period banner. Task nodes only.
            if key.endswith(ROOT_SUFFIX):
                continue
            title = loc.get(key)
            out_dds = os.path.join(OUT, key + ".dds")
            cur = im.group(2)
            need_convert = force or not os.path.exists(out_dds)
            need_repoint = (cur != key)
            if not need_convert and not need_repoint:
                continue
            if need_convert:
                # [#125] curated query wins over the loc-derived one for flagged tasks.
                if key in CONCEPT_QUERY:
                    query = CONCEPT_QUERY[key]
                else:
                    query = query_from_title(title, key) if title else key.replace('_', ' ')
                src = os.path.join(SRC, key + ".jpg")
                try:
                    # [#125] --force re-fetches even a cached source so the improved
                    # period-art ranker actually re-selects the image.
                    if force or not os.path.exists(src):
                        _, desc = fetch(("search", query), src, width=320)
                    else:
                        desc = "cached"
                    # [#125] mission-task widgets require the DX10 BGRA8 layout (the donor
                    # test1.dds + stock icons are DX10); legacy BGRA8 renders as placeholder.
                    # [#183] Emit a 320x320 SQUARE icon (TI's mission-task geometry) rather than
                    # cloning the donor's 118x68 strip: the task widget forces ~128x133, so a
                    # square source downscales cleanly instead of being stretched ~2x vertically
                    # and overflowing the node cell into its neighbours. size= (not like=) also
                    # takes the fully-opaque alpha path, matching TI's opaque square task art.
                    convert(src, out_dds, size=320, dx10=True)
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
    force = "--force" in sys.argv
    # [#125] optional --only=<substr> limits the run to matching mission files (so a single
    # curated tree can be regenerated without re-fetching all 205 icons / hammering Commons).
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None)
    loc = load_loc()
    files = sorted(glob.glob(os.path.join(MISS, "qing_*_missions.txt")))
    if only:
        files = [f for f in files if only in os.path.basename(f)]
    with open(LOG, "w", encoding="utf-8") as log:
        log.write("file\tkey\ttitle\tquery\tsource\tstatus\n")
        for fp in files:
            print("==", os.path.basename(fp))
            process_file(fp, loc, log, force=force)
    print("done; log ->", LOG)

if __name__ == "__main__":
    main()
