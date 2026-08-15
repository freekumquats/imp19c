#!/usr/bin/env python3
# tools/tariffs_expense_trace.py -- one-off, task #102 (reopened #79).
# Parses the ECON_LOG_curx_tariffs_expenses tick-count probe (se_ECON_LOG.txt:895-961):
# each metric is "IMP19C CURXV LABEL <name>" followed by N "IMP19C CURXV unit" lines,
# where N = round(value * scale). Scale is 1 for all expense_* vars, 1000 for
# expense_taxrate_tariffs. Read-only, streamed from stdin (never extract logs.zip).
import sys, re

SCALES = {
    "expense_extraction_upper": 1, "expense_manufacturing_upper": 1,
    "expense_extraction_middle": 1, "expense_manufacturing_middle": 1,
    "expense_extraction_lower": 1, "expense_manufacturing_lower": 1,
    "expense_extraction_proletariat": 1, "expense_manufacturing_proletariat": 1,
    "expense_extraction_indentured": 1, "expense_manufacturing_indentured": 1,
    "expense_extraction_slaves": 1, "expense_manufacturing_slaves": 1,
    "expense_taxrate_tariffs": 1000,
}

label_re = re.compile(r'IMP19C CURXV LABEL (\S+)')
unit_re = re.compile(r'IMP19C CURXV unit')
zero_re = re.compile(r'IMP19C CURXV flag ZERO')
capped_re = re.compile(r'IMP19C CURXV flag CAPPED')

snapshots = []
cur_label = None
cur_count = 0
cur_snap = None

def flush_metric():
    global cur_label, cur_count, cur_snap
    if cur_label is not None and cur_snap is not None:
        scale = SCALES.get(cur_label)
        if scale:
            cur_snap[cur_label] = cur_count / scale
        else:
            cur_snap[cur_label] = cur_count  # e.g. "end" sentinel, ignore
    cur_label = None
    cur_count = 0

for line in sys.stdin:
    if "IMP19C CURXV" not in line:
        continue
    idx = line.find("IMP19C CURXV")
    s = line[idx:]
    m = label_re.match(s)
    if m:
        flush_metric()
        name = m.group(1)
        if name == "expense_extraction_upper":
            cur_snap = {}
            snapshots.append(cur_snap)
        if name == "end":
            cur_label = None
            continue
        cur_label = name
        cur_count = 0
        continue
    if unit_re.match(s):
        cur_count += 1
        continue
    if zero_re.match(s):
        cur_count = 0
        continue
    if capped_re.match(s):
        pass  # count already includes the capped 8000 ticks; just informational

flush_metric()

if not snapshots:
    print("# NO snapshots found -- ECON_LOG_curx_tariffs_expenses probe not present in this log")
    sys.exit(0)

extraction_keys = [k for k in SCALES if k.startswith("expense_extraction")]
manuf_keys = [k for k in SCALES if k.startswith("expense_manufacturing")]

print(f"# snapshots found: {len(snapshots)}")
print(f"{'idx':>3} {'taxrate':>8} {'SUM_extraction':>15} {'SUM_manuf':>10} {'TOTAL_expenses':>14} {'tariffs_est(total*rate)':>24}")
for i, snap in enumerate(snapshots):
    rate = snap.get("expense_taxrate_tariffs", 0.0)
    sum_ext = sum(snap.get(k, 0.0) for k in extraction_keys)
    sum_man = sum(snap.get(k, 0.0) for k in manuf_keys)
    total = sum_ext + sum_man
    tariffs_est = total * rate
    print(f"{i:3d} {rate:8.3f} {sum_ext:15.1f} {sum_man:10.1f} {total:14.1f} {tariffs_est:24.1f}")

print()
print("# per-stratum breakdown (extraction | manufacturing), last snapshot:")
last = snapshots[-1]
for strat in ["upper", "middle", "lower", "proletariat", "indentured", "slaves"]:
    e = last.get(f"expense_extraction_{strat}", 0.0)
    m = last.get(f"expense_manufacturing_{strat}", 0.0)
    print(f"  {strat:12} extraction={e:10.1f}  manufacturing={m:10.1f}")
