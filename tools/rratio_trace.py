#!/usr/bin/env python3
# tools/rratio_trace.py — trace rratio (CURRENCY_reserve_ratio_total) and agreserve
# (silver_reserve_size) bands per quarter, to check the reserve-ratio-rail ratchet
# hypothesis directly against a real boot (task #69). Read-only. Pair with:
#   unzip -p ~/Downloads/logs.zip logs/debug.log | python3 tools/rratio_trace.py
import sys, re

mark_re = re.compile(r'IMP19C CURX QUARTER-MARK (PRE|POST)')
curx_re = re.compile(r'IMP19C CURX ([a-z_]+) (.+?)\s*$')
quarters = []
cur = None

for line in sys.stdin:
    if "IMP19C " not in line:
        continue
    idx = line.find("IMP19C ")
    s = line[idx:].rstrip("\n")
    mm = mark_re.match(s)
    if mm:
        cur = {}
        quarters.append((mm.group(1), cur))
        continue
    if cur is None:
        continue
    m = curx_re.match(s)
    if m:
        met, val = m.group(1), m.group(2).split(" (")[0].strip()
        cur.setdefault(met, val)

print("idx ph   rratio             agreserve           ess                 infl")
for i, (ph, d) in enumerate(quarters):
    print(f"{i:3d} {ph:4} {d.get('rratio','?'):18} {d.get('agreserve','?'):18} {d.get('ess','?'):18} {d.get('infl','?')}")
