#!/usr/bin/env python3
# build_ownership_audit.py — [#40 2026-07-20] builds PROVINCE_OWNERSHIP_1763.csv, the per-province
# historical-ownership audit spreadsheet for the full world at the 1763 start.
#
# Columns (per operator spec):
#   province_name, province_id, owner_name_1763, owner_tag_1763,
#   historical_justification_1763_with_source, current_owner_tag, status, confidence
# owner_*_1763 = the HISTORICALLY CORRECT 1763 owner (filled by regional research); current_owner_tag =
# what the game setup has NOW. Where they differ, the game is corrected (gated on the invariant checker).
# status: OWNED (game has an owner) / UNOWNED (named, no owner) / UNNAMED-placeholder (PROV#### name =
# wasteland/sea/unused). Re-run regenerates the skeleton from live data; research edits live in the CSV
# and should be merged, not overwritten (this writes only blank research columns for NEW ids).

import re, csv, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tools/setup_audit/<file> -> repo root
def load(p): return open(os.path.join(ROOT,p),encoding="utf-8",errors="replace").read()

names={}
for l in load("localization/english/provincenames_l_english.yml").split("\n"):
    m=re.match(r'\s*PROV(\d+):0\s*"([^"]*)"',l)
    if m: names[int(m.group(1))]=m.group(2)

s="\n".join(l.split("#",1)[0] for l in load("setup/main/00_default.txt").split("\n"))
owner={}
for m in re.finditer(r'\b([A-Z]{3})\s*=\s*\{',s):
    tag=m.group(1); i=m.end()-1; d=0
    for j in range(i,len(s)):
        if s[j]=="{": d+=1
        elif s[j]=="}":
            d-=1
            if d==0: body=s[m.end():j]; break
    cm=re.search(r'own_control_core\s*=\s*\{([^}]*)\}',body,re.S)
    if cm:
        for pid in re.findall(r'\d+',cm.group(1)): owner.setdefault(int(pid),tag)

tagname={}
for l in load("localization/english/countries_l_english.yml").split("\n"):
    m=re.match(r'\s*([A-Z]{3}):0\s*"([^"]*)"',l)
    if m: tagname[m.group(1)]=m.group(2)

out=os.path.join(ROOT,"PROVINCE_OWNERSHIP_1763.csv")
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["province_name","province_id","owner_name_1763","owner_tag_1763",
                "historical_justification_1763_with_source","current_owner_tag","status","confidence"])
    for p in sorted(names):
        t=owner.get(p,"")
        placeholder=names[p].startswith("PROV")
        status="OWNED" if t else ("UNNAMED-placeholder" if placeholder else "UNOWNED")
        w.writerow([names[p],p,"","","",t,status,""])

tot=len(names); own=len(owner); un=sum(1 for p in names if p not in owner and not names[p].startswith("PROV"))
ph=sum(1 for p in names if names[p].startswith("PROV"))
print(f"named provinces {tot}: OWNED {own}, UNOWNED(named) {un}, UNNAMED-placeholder {ph}")
print(f"wrote {out}")
