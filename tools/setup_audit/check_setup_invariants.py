#!/usr/bin/env python3
# check_setup_invariants.py — [#24 2026-07-20] STATIC invariant gate for the map-populate batches.
#
# The #24 hard constraint (DESIGN_native_africa_oceania_populate.md §0): every new tag is an
# ownerless-capital HARD CRASH risk. This script is the pre-commit gate — a batch does NOT commit
# until it passes. It parses the setup block (setup/main/00_default.txt) and checks:
#   1. OWNERLESS CAPITAL: every tag's `capital` province appears in its own `own_control_core`.
#   2. DOUBLE-OWNED: no province id appears in two tags' own_control_core.
#   3. REFS EXIST: every tag's primary_culture exists in common/cultures/, religion in common/religions/.
#   4. BRACE BALANCE of the setup file.
#   5. LANDLESS SUBJECT: no `dependency = { first=A second=B }` where B has ZERO own_control_core.
#      (An emptied/inert tag left wired as a live subject = class-4 construction AV — the crash that the
#      #40 South-American-junta + NSW inert folds introduced. Inert-tag playbook step 3 = drop dependency.)
# Reports every violation with the offending tag(s)/province(s). Exit 0 = clean, 1 = violations.
#
# Usage: python3 setup/main/check_setup_invariants.py
# Best-effort brace-matched parser (the setup file is one giant nested block); it extracts each
# TAG = { ... } country block within the countries section and reads capital + own_control_core.

import re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tools/setup_audit/<file> -> repo root
SETUP = os.path.join(ROOT, "setup", "main", "00_default.txt")

def strip_comments(s):
    # remove # comments (line-level); keep newlines
    return "\n".join(line.split("#", 1)[0] for line in s.split("\n"))

def load(path):
    return open(path, encoding="utf-8", errors="replace").read()

def brace_delta(s):
    s = strip_comments(s)
    return s.count("{") - s.count("}")

def extract_country_blocks(text):
    """Yield (tag, body) for every 3-uppercase-letter TAG = { ... } block that contains a
    `capital` and/or `own_control_core` (i.e. a real country setup block, not a random 3-char key)."""
    t = strip_comments(text)
    blocks = {}
    # find 'TAG = {' openings where TAG is exactly 3 uppercase letters (Imperator tag convention)
    for m in re.finditer(r'\b([A-Z]{3})\s*=\s*\{', t):
        tag = m.group(1)
        # brace-match to find the block end
        i = m.end() - 1
        depth = 0
        for j in range(i, len(t)):
            if t[j] == "{":
                depth += 1
            elif t[j] == "}":
                depth -= 1
                if depth == 0:
                    body = t[m.end():j]
                    if "capital" in body or "own_control_core" in body:
                        # keep the LAST occurrence if a tag appears twice (setup uses one block)
                        blocks[tag] = body
                    break
    return blocks

def parse_capital(body):
    m = re.search(r'\bcapital\s*=\s*(\d+)', body)
    return int(m.group(1)) if m else None

def parse_cores(body):
    m = re.search(r'own_control_core\s*=\s*\{([^}]*)\}', body, re.S)
    if not m:
        return []
    return [int(x) for x in re.findall(r'\d+', m.group(1))]

def culture_keys():
    keys = set()
    for f in glob.glob(os.path.join(ROOT, "common", "cultures", "*.txt")):
        t = strip_comments(load(f))
        # top-level culture group -> `culture = { ... }` entries; grab any `key = X` and group names
        for m in re.finditer(r'^\s*([a-z_][a-z0-9_]*)\s*=\s*\{', t, re.M):
            keys.add(m.group(1))
    return keys

def religion_keys():
    keys = set()
    for f in glob.glob(os.path.join(ROOT, "common", "religions", "*.txt")):
        t = strip_comments(load(f))
        for m in re.finditer(r'^\s*([a-z_][a-z0-9_]*)\s*=\s*\{', t, re.M):
            keys.add(m.group(1))
    return keys

# The 15 pre-existing "capital not in cores" tags on the KNOWN-BOOTING baseline are the emptied
# INERT tags (inert-tag playbook: empty own_control_core + capital repointed). An empty-cores tag is
# NOT the construction-crash class — a tag with ZERO cores owns nothing and is dead/inert, which the
# base map ships and boots. The crash class is specifically a NON-EMPTY-cores tag whose capital lies
# OUTSIDE those cores. So we classify:
#   - capital not in cores AND cores is EMPTY  -> INERT (informational, not a violation)
#   - capital not in cores AND cores NON-EMPTY -> OWNERLESS-CAPITAL CRASH RISK (violation)
# Plus a BASELINE mode: `--save-baseline` records the current violation set; subsequent runs fail only
# on NEW violations (so a pre-existing double-owned like SNR/MLK 883 doesn't block new batches, but any
# regression WE introduce does).

BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".setup_invariant_baseline.txt")

def main():
    save_baseline = "--save-baseline" in sys.argv
    text = load(SETUP)
    violations = []
    inert = []

    bd = brace_delta(text)
    if bd != 0:
        violations.append(f"BRACE IMBALANCE in 00_default.txt: delta={bd}")

    blocks = extract_country_blocks(text)
    cultures = culture_keys()
    religions = religion_keys()

    owner_of = {}   # province id -> tag (first seen)
    for tag, body in sorted(blocks.items()):
        cap = parse_capital(body)
        cores = parse_cores(body)
        coreset = set(cores)

        # 1. ownerless capital — ONLY a crash risk when cores are NON-EMPTY (empty-cores = inert tag)
        if cap is not None and cap not in coreset:
            if len(coreset) == 0:
                inert.append(f"INERT (empty cores, safe): {tag} capital={cap}")
            else:
                violations.append(f"OWNERLESS CAPITAL: {tag} capital={cap} not in its {len(coreset)}-province own_control_core")

        # 2. double-owned
        for pid in cores:
            if pid in owner_of and owner_of[pid] != tag:
                violations.append(f"DOUBLE-OWNED province {pid}: {owner_of[pid]} and {tag}")
            else:
                owner_of[pid] = tag

        # 3. refs exist (only if cultures/religions parsed non-empty — else skip to avoid false alarms)
        if cultures:
            mc = re.search(r'primary_culture\s*=\s*([a-z_][a-z0-9_]*)', body)
            if mc and mc.group(1) not in cultures:
                violations.append(f"MISSING CULTURE: {tag} primary_culture={mc.group(1)} not found in common/cultures/")
        if religions:
            mr = re.search(r'religion\s*=\s*([a-z_][a-z0-9_]*)', body)
            if mr and mr.group(1) not in religions:
                violations.append(f"MISSING RELIGION: {tag} religion={mr.group(1)} not found in common/religions/")

    # 5. LANDLESS SUBJECT: a dependency whose `second` (subject) tag owns zero provinces. Scan the whole
    # setup text for dependency blocks; a subject with empty/absent own_control_core is a construction AV.
    landless = set()
    for tag, body in blocks.items():
        if len(parse_cores(body)) == 0:
            landless.add(tag)
    stext = strip_comments(text)
    for dm in re.finditer(r'dependency\s*=\s*\{[^}]*?\bsecond\s*=\s*([A-Z]{2,3})\b[^}]*?\}', stext):
        subj = dm.group(1)
        # only flag subjects that appear as an emptied/known setup block (avoid noise from non-setup refs)
        if subj in landless:
            violations.append(f"LANDLESS SUBJECT: dependency second={subj} but {subj} has ZERO own_control_core (emptied/inert tag left wired as a live subject — class-4 construction crash; drop the dependency)")

    print(f"checked {len(blocks)} country setup blocks; {len(owner_of)} owned provinces; {len(inert)} inert (empty-cores) tags")

    if save_baseline:
        with open(BASELINE, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(violations)))
        print(f"✔ saved baseline: {len(violations)} pre-existing violation(s) recorded to {os.path.basename(BASELINE)}")
        sys.exit(0)

    base = set()
    if os.path.exists(BASELINE):
        base = set(l for l in load(BASELINE).split("\n") if l.strip())
    new_violations = [v for v in violations if v not in base]
    pre_existing = [v for v in violations if v in base]

    if pre_existing:
        print(f"\n({len(pre_existing)} pre-existing violation(s) from baseline, ignored)")
    if new_violations:
        print(f"\n{len(new_violations)} NEW VIOLATION(S) — batch is NOT safe to commit:")
        for v in new_violations:
            print("  ✘", v)
        sys.exit(1)
    print("✔ no new invariant violations (0 new ownerless capitals, 0 new double-owned, all refs exist)")
    sys.exit(0)

if __name__ == "__main__":
    main()
