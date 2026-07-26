#!/usr/bin/env python3
"""
repoint_refs.py — repoint game-file references from borrowed art to the new bespoke icons.

Only rewrites a line when the target bespoke .dds actually exists on disk (so a failed
fetch never produces a dangling reference). Reports every change. Idempotent.

Covers:
  - GUI panel headers: gui/qing_<panel>.gui  texture="...menu_X.dds" -> "...menu_buttons/<panel>.dds"
  - Event pictures:    common/event_pictures/00_event_pictures.txt  picture=... -> qing_<alias>.dds
  - Military traditions: repointing handled by gen_tradition_icons.py (writes <nodekey>.dds and
    rewrites icon=/image= in place there).
Trade goods & building-type icons need NO repoint (filename == key already).
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def exists(rel): return os.path.exists(os.path.join(ROOT, rel))

def repoint_panels():
    changes=[]
    gdir=os.path.join(ROOT,"gui")
    for fn in sorted(os.listdir(gdir)):
        if not (fn.startswith("qing_") and fn.endswith(".gui")): continue
        panel=fn[:-4]                       # qing_zongli
        art=f"gfx/interface/icons/menu_buttons/{panel}.dds"
        if not exists(art): continue
        fp=os.path.join(gdir,fn)
        txt=open(fp,encoding="utf-8").read()
        new=re.sub(r'texture = "gfx/interface/icons/menu_buttons/menu_[a-z]+\.dds"',
                   f'texture = "{art}"', txt, count=1)
        if new!=txt:
            open(fp,"w",encoding="utf-8").write(new)
            changes.append(fn)
    return changes

# event alias -> the current borrowed picture filename fragment to replace
EVENT_ALIASES = {
 "senate":     "qing_senate",
 "navy":       "qing_navy",
 "greek_siege":"qing_greek_siege",
}
def repoint_events():
    fp=os.path.join(ROOT,"common","event_pictures","00_event_pictures.txt")
    if not os.path.exists(fp): return []
    lines=open(fp,encoding="utf-8").readlines()
    changes=[]; out=[]; cur_alias=None
    alias_re=re.compile(r'^(\w+)\s*=\s*\{')
    pic_re=re.compile(r'^(\s*picture\s*=\s*)"[^"]+"(.*)$')
    for line in lines:
        am=alias_re.match(line)
        if am: cur_alias=am.group(1)
        pm=pic_re.match(line)
        if pm and cur_alias in EVENT_ALIASES:
            art=f"gfx/interface/event_window/{EVENT_ALIASES[cur_alias]}.dds"
            if exists(art):
                newline=f'{pm.group(1)}"{art}"{pm.group(2)}\n'
                if newline!=line:
                    out.append(newline); changes.append(cur_alias); continue
        out.append(line)
    if changes:
        open(fp,"w",encoding="utf-8").writelines(out)
    return changes

if __name__=="__main__":
    p=repoint_panels(); print("panels repointed:", len(p), p)
    e=repoint_events(); print("events repointed:", len(e), e)
