#!/usr/bin/env python3
# #23 — read the ENTIRE debug.log line by line (streaming) and reconstruct the full
# per-quarter economy: the CHI currency chain (CURX) + every trade-zone GOOD's
# price/stock/order/pct (TZP). One pass, comprehensive picture. Read-only.
#
# [2026-08-12] The TZP probe (se_ECON_LOG_TZPROBE.txt / tools/gen_econ_tzprobe.py) logs ALL 16 goods
# across all 22 zones, not just silver -- this tool used to hard-code "silver" in its regex and silently
# read only 1 of the 16 goods present in the log. Added --good (default silver, so old invocations are
# unchanged) so any tracked good can be inspected the same way.
import sys, re, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--good", default="silver", help="which TZP-tracked good to analyze (default: silver). "
                 "One of: silver, gold, grain, salt, fish, tea, silk, silk_cloth, porcelain, gems, opium, "
                 "coffee, sugar, spices, tobacco, chili (see tools/gen_econ_tzprobe.py GOODS list).")
args = ap.parse_args()
GOOD = args.good

CHAIN = ["gbip","wvuraw","agsilver","wvuscaled","pen","ratio","ess","need","circ",
         "rratio","agreserve","agdemand","defl","infl","trout","deflmult","inflmult","natexp"]

def band(v):
    return v.split(" (")[0].strip()

quarters = []   # (phase, dict)
cur = None
n_lines = 0
n_curx = 0
n_tzp = 0
tzs = set()

curx_re = re.compile(r'IMP19C CURX ([a-z_]+) (.+?)\s*$')
tzp_re  = re.compile(rf'IMP19C TZP BAND {re.escape(GOOD)} ([a-z_]+) (price|stock|order|pct) (.+?)\s*$')
tzpg_re = re.compile(rf'IMP19C TZP BAND {re.escape(GOOD)} GLOBAL (stock|gbip) (.+?)\s*$')
mark_re = re.compile(r'IMP19C CURX QUARTER-MARK (PRE|POST)')
# exact tick layer: LABEL sets current metric; each "unit" line = 1 tick; flag = state
cxv_label_re = re.compile(r'IMP19C CURXV LABEL ([a-z_]+)')
cxv_unit_re  = re.compile(r'IMP19C CURXV unit')
cxv_flag_re  = re.compile(r'IMP19C CURXV flag (\S+)')

for line in sys.stdin:
    n_lines += 1
    if "IMP19C " not in line:
        continue
    # strip everything up to the IMP19C tag (the engine prepends file:line noise)
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
        n_curx += 1
        met, val = m.group(1), band(m.group(2))
        # [2026-08-12] "trout" (CURRENCY_trade_wealth_outgoing_currency_value) logs TWO lines per
        # quarter under the SAME tag ("SIGN = ..." then "abs ..."); the old setdefault kept only the
        # first and silently dropped the magnitude. Store both under distinct keys so neither is lost.
        # [I.11 2026-08-12] "natexp" (TRADE_national_expenditure, added to isolate #112/#115's numerator
        # from wvuraw's divisor per the adversarial review's gap) has the identical SIGN/abs dual-line
        # shape -- same fix.
        if met in ("trout", "natexp"):
            if val.startswith("SIGN"):
                cur.setdefault(f"C_{met}_sign", val)
            else:
                cur.setdefault(f"C_{met}_abs", val)
            cur.setdefault("C_"+met, val)  # keep old key too, for anything still reading it
        else:
            cur.setdefault("C_"+met, val)
        continue
    m = tzp_re.match(s)
    if m:
        n_tzp += 1
        tz, fld, val = m.group(1), m.group(2), band(m.group(3))
        tzs.add(tz)
        cur.setdefault(f"{tz}.{fld}", val)
        continue
    m = tzpg_re.match(s)
    if m:
        cur.setdefault("GLOBAL."+m.group(1), band(m.group(2)))
        continue
    # exact-value tick layer
    m = cxv_label_re.match(s)
    if m:
        cur["_cxv_metric"] = m.group(1)
        cur.setdefault("V_"+m.group(1), 0)
        continue
    if cxv_unit_re.match(s):
        met = cur.get("_cxv_metric")
        if met is not None:
            cur["V_"+met] = cur.get("V_"+met,0) + 1
        continue
    m = cxv_flag_re.match(s)
    if m:
        met = cur.get("_cxv_metric")
        if met is not None:
            cur["F_"+met] = m.group(1)
        continue

print(f"# lines read: {n_lines:,} | CURX matched: {n_curx:,} | TZP matched: {n_tzp:,} | quarter-marks: {len(quarters)}")
print(f"# trade zones seen: {len(tzs)} | good analyzed: {GOOD}")
if GOOD not in ("silver", "gold"):
    print(f"# NOTE: --good={GOOD} has NO exact-tick data (that CURXV/EXACT layer is metals-only, per")
    print(f"#   tools/gen_econ_tzprobe.py's own scope note). Sections 1 and 2b below are ALWAYS the")
    print(f"#   SILVER-only CHI currency chain (the CURX/CURXV tags carry no good name) -- they do NOT")
    print(f"#   describe {GOOD}. Only the TZP-BAND sections (2, 2c onward) reflect --good={GOOD}.")
print()

# 1) CHI currency chain, every quarter in order (ALWAYS silver -- CURX/CURXV tags carry no good name)
print("=== CHI CURRENCY CHAIN (silver-only; every PRE/POST snapshot, in order) ===")
cols = ["gbip","agsilver","wvuraw","wvuscaled","pen","ratio","ess","need","defl","infl"]
print("idx ph  | " + " | ".join(c.ljust(11) for c in cols) + " | trout(sign|abs) | natexp(sign|abs)")
for i,(ph,d) in enumerate(quarters):
    row = " | ".join(d.get("C_"+c,"?")[:11].ljust(11) for c in cols)
    tsign = d.get("C_trout_sign","?").replace("SIGN = ","")[:16]
    tabs = d.get("C_trout_abs","?")
    # [I.11 2026-08-12] natexp = TRADE_national_expenditure, trout's un-divided numerator; printed
    # alongside trout so a PRE/POST row shows both operands of trout = natexp / wvuraw / 4 at once.
    nsign = d.get("C_natexp_sign","?").replace("SIGN = ","")[:16]
    nabs = d.get("C_natexp_abs","?")
    print(f"{i:3d} {ph:4}| {row} | {tsign} | {tabs} | {nsign} | {nabs}")

# 2) Producer TZ price/stock/order, POST snapshots, in order
print()
print(f"=== {GOOD.upper()} by TRADE ZONE (POST snapshots): price | stock | order ===")
posts = [d for ph,d in quarters if ph=="POST"]
for tz in sorted(tzs):
    seq = []
    for d in posts:
        p = d.get(f"{tz}.price","?"); st = d.get(f"{tz}.stock","?"); o = d.get(f"{tz}.order","?")
        seq.append(f"{p}|{st}|{o}")
    # only print zones that ever had nonzero stock (real producers) OR nonzero price
    if any(("stock 0"!=("stock "+x.split('|')[1]) and x.split('|')[1] not in ("0","?")) for x in seq):
        print(f"\n{tz}:")
        for j,x in enumerate(seq):
            print(f"   q{j:2d} POST  {x}")

# 2b) EXACT values from the CURXV tick layer (value = ticks / SCALE) -- ALWAYS silver, see note above.
# [I.11 2026-08-12] wvuraw/natexp added. The probe stages natexp's tick count as round(value * 0.0002)
# (scaled DOWN, since natexp runs into the millions); value = ticks / 0.0002, so SCALE["natexp"]=0.0002
# here too -- this dict is always "value = ticks / SCALE[metric]", matching the probe's own scale literal.
# [I.14 2026-08-12] need's scale changed 500->50 in se_ECON_LOG.txt (the old /500 hit the 8000-tick cap
# at need>=16.0 on 17/29 quarters -- an adversarial review flagged this as making need's true magnitude
# unmeasurable/circular). poptick (country_population, x0.001) and wealthgen (x0.0002, same money-unit
# scale as natexp) added to close the population and shared-divisor confounds the same review raised.
SCALE = {"ratio":1000,"agsilver":5000,"ess":1,"need":50,"circ":10,
         "wvuscaled":5000,"gbip":2000,"pen":2000,"wvuraw":500,"natexp":0.0002,
         "poptick":0.001,"wealthgen":0.0002}
print()
print("=== EXACT VALUES (silver-only CURXV tick-count / scale), every snapshot in order ===")
exact_cols = ["gbip","agsilver","wvuscaled","pen","ratio","ess","need","circ","wvuraw","natexp","poptick","wealthgen"]
print("idx ph  | " + " | ".join(c.ljust(12) for c in exact_cols))
for i,(ph,d) in enumerate(quarters):
    cells=[]
    for c in exact_cols:
        if "V_"+c in d:
            sc=SCALE.get(c,1)
            v=d["V_"+c]/sc
            fl=d.get("F_"+c,"")
            tag="!"+fl if fl else ""
            cells.append((f"{v:.4g}{tag}")[:12].ljust(12))
        else:
            cells.append("?".ljust(12))
    print(f"{i:3d} {ph:4}| " + " | ".join(cells))

# 2c) GLOBAL gbip + global stock per quarter (per --good; the probe emits a GLOBAL block for every good)
print()
print(f"=== GLOBAL {GOOD}: gbip band + global stock band per snapshot ===")
for i,(ph,d) in enumerate(quarters):
    print(f"{i:3d} {ph:4}| gbip={d.get('GLOBAL.gbip','?'):15} globalstock={d.get('GLOBAL.stock','?')}")

# 2d) gbip CONTRIBUTION per zone = price_band_mid × pct_band_mid, per POST quarter.
# Resolves the central paradox: which zone(s) actually move gbip² = Σ(price×share)?
def midband(b):
    # map a band string like "0.01-0.1" / "100-1000" / ">= 1" / "0" to a representative number
    b=b.strip()
    if b in ("0","?",""): return 0.0
    if b.startswith(">="):
        try: return float(b[2:].strip())
        except: return 0.0
    if "-" in b:
        lo,hi=b.split("-",1)
        try: return (float(lo)+float(hi))/2
        except: return 0.0
    try: return float(b)
    except: return 0.0

gbip_note = "" if GOOD in ("silver","gold") else f" (gbip row below is SILVER's exact value, not {GOOD}'s -- no exact tick exists for {GOOD})"
print()
print(f"=== {GOOD} gbip-shape CONTRIBUTION by zone (price_mid × pct_mid), POST quarters{gbip_note} ===")
zones = sorted(tzs)
# header
print("zone".ljust(20) + " | " + " ".join(f"q{j:02d}" for j in range(len(posts))))
tot=[0.0]*len(posts)
contribs={}
for tz in zones:
    row=[]
    for j,d in enumerate(posts):
        c = midband(d.get(f"{tz}.price","0")) * midband(d.get(f"{tz}.pct","0"))
        row.append(c); tot[j]+=c
    contribs[tz]=row
    # only print zones that contribute materially in at least one quarter
    if max(row) > 0.001:
        print(tz.ljust(20) + " | " + " ".join(f"{x:5.2f}" for x in row))
print("-"*60)
print(f"Σ price×share [{GOOD}]".ljust(20) + " | " + " ".join(f"{x:5.2f}" for x in tot))
print(f"sqrt(Σ)=gbip pred[{GOOD}]".ljust(20) + " | " + " ".join(f"{x**0.5:5.2f}" for x in tot))
print("gbip actual (silver, exact)".ljust(20) + " | " + " ".join(
    (f"{quarters[2*j+1][1].get('V_gbip',0)/2000:5.3f}" if 2*j+1 < len(quarters) else "  ?  ") for j in range(len(posts))))

# 2e) DECISIVE: gbip² = 0.6·Σorder/global_stock (stock cancels in price×share). Track the two aggregates.
# NOTE: Σorder/global_stock below are for --good=GOOD; "gbip_actual" is ALWAYS silver's exact tick (see note above).
print()
print(f"=== AGGREGATE test [{GOOD}]: Σorder vs global_stock vs SILVER's actual gbip (POST){gbip_note} ===")
print("q   | Σorder_mid | globalstock_mid | Σord/gstk | 0.6*ratio | sqrt() | gbip_actual(silver)")
for j,d in enumerate(posts):
    sord=sum(midband(d.get(f"{tz}.order","0")) for tz in zones)
    gstk=midband(d.get("GLOBAL.stock","0"))
    ratio=(sord/gstk) if gstk>0 else 0.0
    pred=0.6*ratio
    # gbip actual from chain exact tick (POST snapshot = quarters[2j+1]) -- always silver, see note above
    ga = quarters[2*j+1][1].get("V_gbip",0)/2000 if 2*j+1<len(quarters) else 0
    print(f"q{j:02d} | {sord:9.1f} | {gstk:14.1f} | {ratio:8.3f} | {pred:8.3f} | {pred**0.5:5.3f} | {ga:.4f}")

# 2f) RAW per-TZ ORDER bands, POST, aligned to gbip hi/lo — does Σorder actually collapse?
print()
print(f"=== RAW ORDER bands per TZ [{GOOD}] (POST), with SILVER's gbip actual on each quarter{gbip_note} ===")
ga_row = [ (quarters[2*j+1][1].get('V_gbip',0)/2000 if 2*j+1<len(quarters) else 0) for j in range(len(posts)) ]
print("gbip(silver):".ljust(20) + " | " + " ".join((f"{g:.3f}" if g>=0.05 else "  ~0 ") for g in ga_row))
print("-"*60)
for tz in sorted(tzs):
    cells=[]
    for d in posts:
        o = d.get(f"{tz}.order","?")
        cells.append(o[:5].rjust(5))
    # flag zones whose order band ever differs across quarters
    dist = sorted(set(c.strip() for c in cells if c.strip()!="?"))
    flag = "  <<<" if len(dist)>1 else ""
    print(tz.ljust(20) + " | " + " ".join(cells) + flag)

# 3) Oscillation summary: for every zone, does price or stock TOGGLE across quarters?
print()
print("=== OSCILLATION SUMMARY (POST): zones whose price OR stock changes band across quarters ===")
for tz in sorted(tzs):
    prices = [d.get(f"{tz}.price","?") for d in posts]
    stocks = [d.get(f"{tz}.stock","?") for d in posts]
    pdist = sorted(set(p for p in prices if p!="?"))
    sdist = sorted(set(s for s in stocks if s!="?"))
    toggles = (len(pdist)>1) or (len(sdist)>1)
    flag = "  <<< TOGGLES" if toggles else ""
    print(f"{tz:20} price∈{pdist}  stock∈{sdist}{flag}")
