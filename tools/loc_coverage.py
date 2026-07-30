#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[#188] Localization coverage audit — enumerate every referenced game-object key that needs
display loc and diff against localization/english/*.yml. Deterministic, re-runnable; a
regression guard against the missing-loc class that recurred through the 2026-07 boot tests.

Reports keys with NO name loc (and, where relevant, NO _desc). Read-only: prints a punch-list,
writes nothing. Run: python3 tools/loc_coverage.py [--domain loyalty|deities|decisions|...]

Scope note: vanilla engine modifiers are auto-localized via MODIFIER_<UPPERCASE>; this script
only flags MOD-DEFINED objects, and for modifiers checks bare / MODIFIER_ / uppercase forms so
it does not false-positive on engine-loc'd tokens.
"""
import os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOC_GLOB = os.path.join(ROOT, "localization", "english", "*.yml")

LOCKEY = re.compile(r'^\s*([A-Za-z0-9_.]+):\d', re.M)
NODE   = re.compile(r'^([a-z][A-Za-z0-9_]+)\s*=\s*\{', re.M)   # col-0 def key


def all_loc_keys():
    keys = set()
    for f in glob.glob(LOC_GLOB):
        keys |= set(LOCKEY.findall(open(f, encoding="utf-8-sig").read()))
    return keys


def def_keys(path_glob, col0=True):
    """Top-level def keys across files matching path_glob."""
    keys = []
    pat = NODE if col0 else re.compile(r'^\t([a-z][A-Za-z0-9_]+)\s*=\s*\{', re.M)
    for f in glob.glob(os.path.join(ROOT, path_glob)):
        keys += pat.findall(open(f, encoding="utf-8-sig").read())
    return keys


def has_loc(k, lk):
    return k in lk or ("MODIFIER_" + k.upper()) in lk or k.upper() in lk or ("MODIFIER_" + k) in lk


def report(title, keys, lk, want_desc=False):
    keys = sorted(set(keys))
    miss_name = [k for k in keys if not has_loc(k, lk)]
    miss_desc = [k for k in keys if want_desc and (k + "_desc") not in lk and (k + "DESC") not in lk]
    print(f"\n=== {title}: {len(keys)} keys | {len(miss_name)} missing NAME"
          + (f" | {len(miss_desc)} missing _desc" if want_desc else "") + " ===")
    for k in miss_name:
        print(f"  NAME  {k}")
    if want_desc:
        for k in miss_desc:
            print(f"  DESC  {k}")
    return miss_name, miss_desc


def main():
    lk = all_loc_keys()
    only = None
    if "--domain" in sys.argv:
        only = sys.argv[sys.argv.index("--domain") + 1]

    domains = {
        "loyalty":   lambda: report("loyalty types", def_keys("common/loyalty/*.txt"), lk),
        "modifiers": lambda: report("mod modifiers", def_keys("common/modifiers/*.txt"), lk),
        "deities":   lambda: report("deities", def_keys("common/deities/*.txt"), lk, want_desc=True),
        "goods":     lambda: report("trade goods", def_keys("common/trade_goods/*.txt"), lk, want_desc=True),
        "laws":      lambda: report("laws (groups+options)",
                                    def_keys("common/laws/*.txt") + def_keys("common/laws/*.txt", col0=False), lk),
        "decisions": lambda: report("decisions", def_keys("common/decisions/*.txt", col0=False), lk, want_desc=True),
        "inventions":lambda: report("inventions", def_keys("common/inventions/*.txt", col0=False), lk, want_desc=True),
    }
    for name, fn in domains.items():
        if only and name != only:
            continue
        fn()


if __name__ == "__main__":
    main()
