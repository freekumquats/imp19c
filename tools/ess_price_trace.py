#!/usr/bin/env python3
# tools/ess_price_trace.py — trace CHI's paid unit price ("country_unit_price_<good>") for
# all 12 goods that feed CURRENCY_essentials_buying_power ("ess"), per quarter, to find
# which one collapsed at the idx-10->11 regime shift (task #69, corrected diagnosis).
# Read-only. Pair with:
#   unzip -p ~/Downloads/logs.zip logs/debug.log | python3 tools/ess_price_trace.py
import sys, re

GOODS = ["grain", "livestock", "fish", "vegetables", "temperate_fruit", "processed_foods",
         "clothing", "furniture", "pharmaceuticals", "alcohol", "luxury_clothing", "luxury_furniture"]

mark_re = re.compile(r'IMP19C CURX QUARTER-MARK (PRE|POST)')
paid_re = re.compile(r'IMP19C TZP BAND (' + "|".join(GOODS) + r') CHI paidprice (.+?)\s*$')

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
        quarters.append(cur)
        continue
    if cur is None:
        continue
    m = paid_re.match(s)
    if m:
        good, val = m.group(1), m.group(2).split(" (")[0].strip()
        cur.setdefault(good, val)

print(f"quarter-marks: {len(quarters)}")
print()
header = "idx  | " + " | ".join(g[:10].ljust(10) for g in GOODS)
print(header)
for i, q in enumerate(quarters):
    row = " | ".join(q.get(g, "?")[:10].ljust(10) for g in GOODS)
    print(f"{i:3d}  | {row}")
