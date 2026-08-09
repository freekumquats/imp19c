#!/usr/bin/env python3
# [#1 2026-08-09] Qing treasury-cost rescale — "into the hundreds, cap ~1200".
# Single monotonic map new = round5(40*sqrt(old)) applied to the player-initiated Qing
# spend surface (events + the ministry buttons that share their cost verbs) + matching
# free-text loc. Missions, non-Qing events, rewards, and var:-driven values are OUT.
#
# Usage:
#   python3 tools/treasury_rescale.py            # DRY RUN -> prints manifest, writes nothing
#   python3 tools/treasury_rescale.py --apply    # apply the edits in place
import os, re, glob, sys, math

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def m(x):
    return int(round(40 * math.sqrt(x) / 5.0)) * 5

# ---- in-scope mechanic files -------------------------------------------------
EVENT_FILES = [f for f in glob.glob('events/imp19c_mod_events/qing_*.txt')]
EVENT_FILES += ['events/imp19c_mod_events/currency_crisis_events.txt']
SE_FILES  = glob.glob('common/scripted_effects/se_QING_*.txt')
GUI_FILES = glob.glob('common/scripted_guis/QING_*.txt')
MECH_FILES = EVENT_FILES + SE_FILES + GUI_FILES

# regexes (integer, leading-minus anchored; positives and var: are never matched)
RE_COST  = re.compile(r'(add_treasury\s*=\s*)-(\d+)\b')
RE_GATE  = re.compile(r'(?<![_a-zA-Z])(treasury\s*>=\s*)(\d+)\b')
RE_PARAM = re.compile(r'(\bcost\s*=\s*)-(\d+)\b')

def rescale_mech_line(line):
    """Return (newline, hits[]) for a mechanic line.

    RE_GATE only matches a treasury comparison with a LITERAL-digit RHS: `treasury >= var:foo`
    (var operand) and `negative_treasury >= 90` are both structurally rejected by the regex
    itself (the `\\d+` requirement and the `(?<![_a-zA-Z])` lookbehind). So a `var:` appearing
    ELSEWHERE on the line — e.g. `limit = { var:power >= 20  treasury >= 90 }` — must NOT
    suppress the literal treasury gate on that same line. [review-1 finding 2 fix: the old
    line-level `'var:' not in line` guard wrongly skipped exactly those combined-condition
    guards, desyncing gate from its co-located charge.]
    """
    hits = []
    def sub_cost(mt):
        old = int(mt.group(2)); new = m(old); hits.append(('cost', old, new)); return f"{mt.group(1)}-{new}"
    def sub_param(mt):
        old = int(mt.group(2)); new = m(old); hits.append(('cost=', old, new)); return f"{mt.group(1)}-{new}"
    def sub_gate(mt):
        old = int(mt.group(2)); new = m(old); hits.append(('gate', old, new)); return f"{mt.group(1)}{new}"
    nl = RE_COST.sub(sub_cost, line)
    nl = RE_PARAM.sub(sub_param, nl)
    nl = RE_GATE.sub(sub_gate, nl)
    return nl, hits

def run_mech():
    manifest = []
    for f in MECH_FILES:
        raw = open(f, 'rb').read()
        bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8-sig')
        # preserve per-line EOL: split keeping terminators
        lines = text.splitlines(keepends=True)
        changed = False
        for i, line in enumerate(lines):
            # split terminator to protect EOL
            mterm = re.search(r'(\r\n|\n|\r)?$', line)
            term = mterm.group(0) if mterm else ''
            body = line[:len(line)-len(term)]
            nl, hits = rescale_mech_line(body)
            if hits:
                lines[i] = nl + term
                changed = True
                for kind, old, new in hits:
                    manifest.append((f, i+1, kind, old, new, body.strip()[:80]))
        if changed and APPLY:
            out = ''.join(lines)
            data = out.encode('utf-8')
            if bom and not data.startswith(b'\xef\xbb\xbf'):
                data = b'\xef\xbb\xbf' + data
            open(f, 'wb').write(data)
    return manifest

# ---- loc pass ----------------------------------------------------------------
# We rescale a cost number in a loc string ONLY when it is unambiguously a TREASURY
# cost (not political influence / legitimacy / manpower), and only in EVENT/BUTTON keys
# (.tt / _TT / _tt) — NEVER in mission-objective keys (_DESC / _DESCRIPTION), whose
# mechanic lives in common/missions/ (out of scope). Discipline verified against source:
#   _DESC/_DESCRIPTION -> mission objective (223 cost mentions, all backed by common/missions/)
#   .tt / _TT / _tt    -> event option / ministry button tooltip (in scope)

# NUMBER-LEVEL classifier. For EVERY 2-3 digit number we decide two things independently:
#   (1) treasury-association — is this number a treasury/gold/silver quantity at all?
#       yes iff a ¥ sits just before it, OR "treasury of" just before it, OR the nearest
#       resource NOUN after it (before the next number) is treasury/gold/silver (not
#       political/legitimacy/manpower/influence).
#   (2) sign — is it a COST (scale) or a GAIN (leave)? decided by the nearest signal before
#       the number: a leading '+' or a gain-verb (raise/gain/reclaim/seize/saved/enrich) =>
#       GAIN; a leading '-' or a cost-verb (cost/costs/spend/pay/require/"treasury of") =>
#       COST; nearest one wins. A value already established as a COST elsewhere in the SAME
#       string (e.g. "spend ¥140 ... and ¥140") is treated as a cost restatement.
# This catches the forms a verb-prefix regex missed (lowercase verbs, "Cost:" colon,
# parenthetical "(-150 gold)", "treasury of N", multi-resource "220 treasury AND 10
# manpower") while still rejecting the many "+N Treasury" / "Raise ~¥80" gains.
RE_NUM        = re.compile(r'\d{2,3}')
TREASURY_NOUN = re.compile(r'(treasury|gold|silver)', re.I)
OTHER_NOUN    = re.compile(r'(political|legitimacy|manpower|influence|prestige|stability|innovation|tyranny)', re.I)
COST_WORD     = re.compile(r'(costs?|spend|pay|requires?|treasury of)', re.I)
GAIN_WORD     = re.compile(r'(raise|gain|reclaim|seiz|saved|enrich|revenue|windfall|tops up)', re.I)
# Any tooltip wired as `custom_tooltip = X` from common/missions/ describes a MISSION cost.
# Missions are OUT (their add_treasury is not scaled), so scaling the tooltip would desync it
# from its own unscaled mechanic. Build the exclusion set at runtime from the mission tree.
def mission_tooltip_keys():
    keys = set()
    for f in glob.glob('common/missions/*.txt'):
        try:
            txt = open(f, 'rb').read().decode('utf-8-sig')
        except Exception:
            continue
        for mt in re.finditer(r'custom_tooltip\s*=\s*([A-Za-z0-9_.]+)', txt):
            keys.add(mt.group(1))
    return keys

MISSION_TT = mission_tooltip_keys()

def is_event_or_button_key(k):
    if k in MISSION_TT:                    # mission-tree tooltip: mechanic is OUT
        return False
    return (k.endswith('.tt') or k.endswith('_TT') or k.endswith('_tt')) \
           and not (k.endswith('_DESC') or k.endswith('_DESCRIPTION'))
# A handful of genuine treasury COSTS are phrased with no cost-verb and no +/- sign, so the
# number-level classifier's cost/gain test can't see them. Each is verified against its
# mechanic and allowlisted by (key, old value):
#  - qing_ili.2 option 'strike': colour-coded "#R60#!", charges add_treasury=-60 / gate >=60.
#  - qing_integ.40.e ("the same #Y100#! gold ... as the raw decree"): the garrison-backed
#    variant of qing_integ.40.a; both charge add_treasury=-100 / gate >=100. [review-1 finding
#    1 fix: .a was caught by its "Spend" verb, .e's verb-less restatement was not, so the
#    tooltip quoted 100 while the option charged the scaled 400.]
LOC_ALLOWLIST = {('qing_ili.2.strike.tt', 60),
                 ('qing_integ.40.e.tt', 100)}

def loc_files():
    return [f for f in glob.glob('localization/english/qing_*.yml')]

def key_of(line):
    mt = re.match(r'\s*([A-Za-z0-9_.]+):\d+', line)
    return mt.group(1) if mt else ''

def is_treasury(body, mt, treas_of_vals):
    """Is the number at match mt a TREASURY/gold/silver quantity?"""
    s, e = mt.start(), mt.end()
    old = int(mt.group(0))
    if old in treas_of_vals:                       # restated "treasury of N" in this string
        return True
    pre = body[max(0, s-2):s]                      # a ¥ (opt. space) just before
    if '¥' in pre:
        return True
    if re.search(r'treasury of\s*$', body[max(0, s-16):s], re.I):
        return True
    # nearest resource noun after the number, up to the next number
    nxt = RE_NUM.search(body, e)
    win = body[e: nxt.start() if nxt else len(body)]
    t = TREASURY_NOUN.search(win); o = OTHER_NOUN.search(win)
    if t and (not o or t.start() < o.start()):
        return True
    return False

def is_cost(body, mt):
    """COST (scale) vs GAIN (leave), by the nearest signal BEFORE the number."""
    s = mt.start()
    pre = body[max(0, s-40):s]
    # a sign token immediately before wins outright
    imm = body[max(0, s-1):s]
    if imm == '+':
        return False
    if imm == '-':
        return True
    # else nearest cost-word vs gain-word in the preceding window
    cw = list(COST_WORD.finditer(pre)); gw = list(GAIN_WORD.finditer(pre))
    c = cw[-1].start() if cw else -1
    g = gw[-1].start() if gw else -1
    if c < 0 and g < 0:
        return False                               # no signal => treat as non-cost, skip
    return c >= g                                  # nearest (largest index) wins; tie -> cost

def run_loc(scope_values):
    scope = set(scope_values)
    manifest = []
    for f in loc_files():
        raw = open(f,'rb').read()
        bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8-sig')
        lines = text.splitlines(keepends=True)
        changed = False
        for i, line in enumerate(lines):
            key = key_of(line)
            if not is_event_or_button_key(key):
                continue  # mission-tree / non-tooltip / _DESC loc: OUT
            mterm = re.search(r'(\r\n|\n|\r)?$', line); term = mterm.group(0) if mterm else ''
            body = line[:len(line)-len(term)]
            treas_of_vals = {int(x) for x in re.findall(r'treasury of\s*¥?\s*(\d{2,3})', body, re.I)}
            # Cost-restatement: a value confirmed as a treasury COST anywhere on this line is
            # the SAME cost wherever it recurs (e.g. PENSION "spend ¥140 ... and ¥140.", or
            # reform.35 "treasury of 80 ... Spend 80"). Verified safe: no qing .tt line uses
            # one treasury value as both a cost and a +gain (0 collisions across the corpus).
            cost_vals = set()
            for mt in RE_NUM.finditer(body):
                old = int(mt.group(0))
                if old in scope and is_treasury(body, mt, treas_of_vals) and is_cost(body, mt):
                    cost_vals.add(old)
            hits = []; out = []; last = 0
            for mt in RE_NUM.finditer(body):
                old = int(mt.group(0))
                allow = (key, old) in LOC_ALLOWLIST
                imm = body[max(0, mt.start()-1):mt.start()]
                restate = (old in cost_vals and imm != '+'
                           and is_treasury(body, mt, treas_of_vals))
                if old in scope and (allow or restate):
                    new = m(old)
                    out.append(body[last:mt.start()]); out.append(str(new))
                    last = mt.end()
                    hits.append((old, new, key))
            if hits:
                out.append(body[last:])
                lines[i] = ''.join(out) + term
                changed = True
                for old, new, k in hits:
                    manifest.append((f, i+1, k, old, new, body.strip()[:90]))
        if changed and APPLY:
            data = ''.join(lines).encode('utf-8')
            if bom and not data.startswith(b'\xef\xbb\xbf'):
                data = b'\xef\xbb\xbf' + data
            open(f,'wb').write(data)
    return manifest

if __name__ == '__main__':
    mech = run_mech()
    scope_values = sorted({old for (_,_,_,old,_,_) in mech})
    print(f"# MECHANIC PASS  ({'APPLIED' if APPLY else 'DRY RUN'}) — {len(mech)} edits, "
          f"in-scope values {scope_values}")
    for f,ln,kind,old,new,ctx in mech:
        print(f"  {f}:{ln}  [{kind}] {old}->{new}   | {ctx}")
    loc = run_loc(set(scope_values))
    print(f"\n# LOC PASS  ({'APPLIED' if APPLY else 'DRY RUN'}) — {len(loc)} edits")
    for f,ln,k,old,new,ctx in loc:
        print(f"  {os.path.basename(f)}:{ln}  <{k}> {old}->{new}   | {ctx}")
    # sanity: monotonic check on the union
    U = sorted(set(scope_values))
    mono = all(m(U[i])<m(U[i+1]) for i in range(len(U)-1))
    print(f"\n# map monotonic over in-scope set: {mono}; range [{m(min(U))},{m(max(U))}]" if U else "# no values")
