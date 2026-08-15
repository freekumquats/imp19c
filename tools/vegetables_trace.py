#!/usr/bin/env python3
# tools/vegetables_trace.py — one-pass streaming trace of vegetables' PRICE (not just stock)
# per trade zone, around the q9-q13 window where GLOBAL stock hits zero, to check whether
# the collapse is price-driven (task #79/#69 diagnosis). Read-only. Pair with:
#   unzip -p ~/Downloads/logs.zip logs/debug.log | python3 tools/vegetables_trace.py
import sys, re

mark_re = re.compile(r'IMP19C CURX QUARTER-MARK (PRE|POST)')
tzp_re  = re.compile(r'IMP19C TZP BAND vegetables ([a-z_]+) (price|stock|order|pct) (.+?)\s*$')
tzpg_re = re.compile(r'IMP19C TZP BAND vegetables GLOBAL (stock|gbip) (.+?)\s*$')

quarters = []
cur = None
tzs = set()
n_lines = 0

for line in sys.stdin:
    n_lines += 1
    if "IMP19C " not in line:
        continue
    idx = line.find("IMP19C ")
    s = line[idx:].rstrip("\n")

    mm = mark_re.match(s)
    if mm:
        cur = {"ph": mm.group(1)}
        quarters.append(cur)
        continue
    if cur is None:
        continue

    m = tzp_re.match(s)
    if m:
        tz, fld, val = m.group(1), m.group(2), m.group(3).split(" (")[0].strip()
        tzs.add(tz)
        cur[f"{tz}.{fld}"] = val
        continue
    m = tzpg_re.match(s)
    if m:
        cur["GLOBAL." + m.group(1)] = m.group(2).split(" (")[0].strip()
        continue

print(f"# lines read: {n_lines:,} | quarter-marks: {len(quarters)} | zones seen: {len(tzs)}")
print()
print("=== vegetables per-zone price|stock|order, ALL quarters (PRE+POST) ===")
for tz in sorted(tzs):
    seq = []
    for i, q in enumerate(quarters):
        p = q.get(f"{tz}.price", "?")
        st = q.get(f"{tz}.stock", "?")
        o = q.get(f"{tz}.order", "?")
        seq.append((i, q["ph"], p, st, o))
    # only print zones with ANY nonzero stock/price ever (real producers/consumers)
    if any(x[3] not in ("0", "?") or x[2] not in ("0", "?") for x in seq):
        print(f"\n{tz}:")
        for i, ph, p, st, o in seq:
            print(f"   q{i:2d} {ph:4} price={p:15} stock={st:15} order={o}")

print()
print("=== GLOBAL vegetables: gbip + global stock, every quarter ===")
for i, q in enumerate(quarters):
    print(f"q{i:2d} {q['ph']:4} GLOBAL.stock={q.get('GLOBAL.stock','?'):15} GLOBAL.gbip={q.get('GLOBAL.gbip','?')}")
