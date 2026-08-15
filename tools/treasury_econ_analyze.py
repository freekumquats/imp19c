#!/usr/bin/env python3
# tools/treasury_econ_analyze.py — one-pass streaming read of debug.log for:
#   (1) the 9 previously-uncovered essentials goods' GLOBAL stock/gbip per quarter (task #81:
#       find which good crashed ~51% in one quarterly tick), and
#   (2) the TREASURY_LOG_it / income exact-tick CURXV events (task #79: addtreasury,
#       addtreasury_balance, incometotal, oneshotgrant, wealthgen) -- reconciling summed
#       addtreasury deltas per quarter against incometotal (the displayed quarterly income).
# Read-only, streams stdin line by line (never buffers the whole file). Pair with:
#   unzip -p ~/Downloads/logs.zip logs/debug.log | python3 tools/treasury_econ_analyze.py
import sys, re

GOODS = ["livestock","vegetables","temperate_fruit","processed_foods","clothing",
         "furniture","pharmaceuticals","luxury_clothing","luxury_furniture"]

mark_re = re.compile(r'IMP19C CURX QUARTER-MARK (PRE|POST)')
tzpg_re = re.compile(r'IMP19C TZP BAND (' + "|".join(GOODS) + r') GLOBAL (stock|gbip) (.+?)\s*$')

cxv_label_re = re.compile(r'IMP19C CURXV LABEL ([a-z_]+)')
cxv_unit_re  = re.compile(r'IMP19C CURXV unit')
cxv_flag_re  = re.compile(r'IMP19C CURXV flag (\S+)')

TREASURY_LABELS = {"addtreasury", "addtreasury_balance", "incometotal", "oneshotgrant",
                    "wealthgen", "hiddenqingrev"}
SCALE = {"addtreasury": 1, "addtreasury_balance": 1, "incometotal": 0.1, "oneshotgrant": 1,
          "wealthgen": 0.0002, "hiddenqingrev": 1}

quarters = []
cur = None
cur_metric = None
treasury_events = []  # [quarter_idx, label, tickcount, flag]
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

    m = tzpg_re.match(s)
    if m and cur is not None:
        good, fld, val = m.group(1), m.group(2), m.group(3).split(" (")[0].strip()
        cur[f"{good}.GLOBAL.{fld}"] = val
        continue

    m = cxv_label_re.match(s)
    if m:
        cur_metric = m.group(1)
        if cur_metric in TREASURY_LABELS:
            treasury_events.append([len(quarters) - 1, cur_metric, 0, None])
        continue
    if cxv_unit_re.match(s):
        if cur_metric in TREASURY_LABELS and treasury_events and treasury_events[-1][1] == cur_metric:
            treasury_events[-1][2] += 1
        continue
    m = cxv_flag_re.match(s)
    if m:
        if cur_metric in TREASURY_LABELS and treasury_events and treasury_events[-1][1] == cur_metric:
            treasury_events[-1][3] = m.group(1)
        continue

print(f"# lines read: {n_lines:,} | quarter-marks: {len(quarters)} | treasury CURXV events: {len(treasury_events)}")
print()
print("=== ESSENTIALS GOODS: GLOBAL stock per quarter (looking for the ~51% crash) ===")
for good in GOODS:
    print(f"\n{good}:")
    for i, q in enumerate(quarters):
        st = q.get(f"{good}.GLOBAL.stock", "?")
        gb = q.get(f"{good}.GLOBAL.gbip", "?")
        print(f"   q{i:2d} {q['ph']:4} stock={st:20} gbip={gb}")

print()
print("=== PER-QUARTER RECONCILIATION: summed addtreasury deltas vs incometotal (displayed income) ===")
print("(negative flag applied; CAPPED deltas marked with a * since their true magnitude is >= 8000)")
by_q = {}
for qi, label, ticks, flag in treasury_events:
    by_q.setdefault(qi, {"addtreasury": [], "incometotal": None, "oneshotgrant": None, "wealthgen": None})
    if label == "addtreasury":
        signed = -ticks if flag == "SIGN-NEGATIVE" else ticks
        capped = (flag == "CAPPED")
        by_q[qi]["addtreasury"].append((signed, capped))
    elif label == "incometotal":
        by_q[qi]["incometotal"] = ticks / SCALE["incometotal"]
    elif label == "oneshotgrant":
        by_q[qi]["oneshotgrant"] = ticks
    elif label == "wealthgen":
        by_q[qi]["wealthgen"] = ticks / SCALE["wealthgen"]

for qi in sorted(by_q):
    d = by_q[qi]
    deltas = d["addtreasury"]
    total = sum(v for v, c in deltas)
    any_capped = any(c for v, c in deltas)
    it = d["incometotal"]
    print(f"q{qi:3d}: n_add_treasury_calls={len(deltas):3d} summed_delta={total:8d}{'*' if any_capped else ' '}  "
          f"incometotal={it if it is not None else '?':>10}  oneshotgrant={d['oneshotgrant']}  wealthgen={d['wealthgen']}")

print()
print("=== RAW addtreasury delta list per quarter (for manual magnitude-spike hunting) ===")
for qi in sorted(by_q):
    deltas = by_q[qi]["addtreasury"]
    print(f"q{qi:3d}: " + ", ".join(f"{v}{'*' if c else ''}" for v, c in deltas))
