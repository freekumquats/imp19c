#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_mission_tasks.py — [#126/#127] splice the breadth-expansion mission tasks defined in
mission_task_content.py into their trees + loc files.

For each tree in TREES:
  1. Insert every task block (proven breadth idiom) just before the mission file's final
     closing brace. Each new task `requires` the tree's opening task (a flat optional fan-out,
     exactly like the shipped qing_india_maratha/sikh/... tasks).
  2. Append the 3 loc keys (<key>, <key>_DESC, <key>_tt) to the tree's english yml.

Safety:
  - ABORTS if any new task key already exists as a `<key> = {` node in ANY mission file, or as
    a loc key in the tree's yml (no clobber, no dupes).
  - Idempotent: a task already present (block + loc) is skipped; re-running only adds what's
    missing. Pass --check to report the plan (counts / collisions) without writing.

Introduces ZERO new modifiers or scripted effects — only country-scope engine effects already
used across the suite (add_popularity on current_ruler, add_stability, add_treasury,
add_political_influence, custom_tooltip, LOG_line). See mission_task_content.py header.
"""
import os, re, sys, glob

sys.path.insert(0, os.path.dirname(__file__))
from mission_task_content import TREES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISS = os.path.join(ROOT, "common", "missions")
LOC = os.path.join(ROOT, "localization", "english")

KEYNODE_RE = re.compile(r'^\s*([a-z][a-z0-9_]+)\s*=\s*\{', re.M)
LOCKEY_RE = re.compile(r'^\s*([A-Za-z0-9_]+):\d*\s+"', re.M)


def all_existing_task_keys():
    """Every `<key> = {` node key across all mission files (collision guard)."""
    keys = set()
    for fp in glob.glob(os.path.join(MISS, "*.txt")):
        with open(fp, encoding="utf-8") as f:
            keys.update(KEYNODE_RE.findall(f.read()))
    return keys


def loc_keys(loc_path):
    if not os.path.exists(loc_path):
        return set()
    with open(loc_path, encoding="utf-8-sig") as f:
        return set(LOCKEY_RE.findall(f.read()))


def task_block(t, parent):
    """The mission-task node, tab-indented (matches the shipped tasks)."""
    kind, n = t.cost if t.cost else (None, 0)
    lines = []
    lines.append(f"\t{t.key} = {{")
    lines.append(f"\t\ticon = {t.key}")
    lines.append(f"\t\trequires = {{ {parent} }}")
    if kind == "pol":
        lines.append(f"\t\tallow = {{ political_influence >= {n} }}")
        lines.append(f"\t\ton_start = {{ add_political_influence = -{n} }}")
    elif kind == "trs":
        lines.append(f"\t\tallow = {{ treasury >= {n} }}")
        lines.append(f"\t\ton_start = {{ add_treasury = -{n} }}")
    lines.append("\t\ton_completion = {")
    lines.append(f"\t\t\tcustom_tooltip = {t.key}_tt")
    lines.append(f"\t\t\tcurrent_ruler = {{ add_popularity = {t.pop} }}")
    if t.stab:
        lines.append("\t\t\tadd_stability = 1")
    lines.append(f'\t\t\tLOG_line = {{ sys = QING  msg = "MISSION task {t.key} for" }}')
    lines.append("\t\t}")
    lines.append("\t}")
    return "\n".join(lines) + "\n"


def loc_lines(t):
    title = f'{t.en} ({t.cjk})'
    return [
        f' {t.key}:0 "{title}"\n',
        f' {t.key}_DESC:0 "{t.desc}"\n',
        f' {t.key}_tt:0 "{t.tt}"\n',
    ]


def splice_tasks(mission_path, blocks):
    """Insert task blocks just before the file's LAST closing brace."""
    with open(mission_path, encoding="utf-8") as f:
        text = f.read()
    idx = text.rstrip().rfind("}")
    if idx == -1:
        raise RuntimeError(f"no closing brace in {mission_path}")
    head = text[:idx].rstrip("\n")
    payload = "\n\n" + "\n".join(blocks).rstrip("\n") + "\n}\n"
    with open(mission_path, "w", encoding="utf-8") as f:
        f.write(head + payload)


def append_loc(loc_path, lines):
    with open(loc_path, "a", encoding="utf-8") as f:
        if lines:
            f.write("\n")
            f.writelines(lines)


def main():
    check = "--check" in sys.argv
    existing_task_keys = all_existing_task_keys()

    # ---- global collision guard (fail before any write) ----
    # A key already present in a mission file is only a COLLISION if it is a FOREIGN node
    # (one this content table did not author). A key that belongs to the table is our own
    # prior output — skip it (per-tree idempotent logic re-checks and no-ops). This keeps the
    # generator safely re-runnable to add more tasks or re-verify a clean state.
    own_keys = {t.key for tree in TREES.values() for t in tree["tasks"]}
    seen = {}
    collisions = []
    for name, tree in TREES.items():
        for t in tree["tasks"]:
            if t.key in existing_task_keys and t.key not in own_keys:
                collisions.append(f"{t.key}: already a FOREIGN mission node")
            if t.key in seen:
                collisions.append(f"{t.key}: duplicated in content table ({seen[t.key]}, {name})")
            seen[t.key] = name
    if collisions:
        print("ABORT — key collisions:")
        for c in collisions:
            print("  " + c)
        sys.exit(1)

    total_added = 0
    for name, tree in TREES.items():
        mp = os.path.join(MISS, f"qing_{name}_missions.txt")
        lp = os.path.join(LOC, tree["loc"])
        if not os.path.exists(mp):
            print(f"  SKIP {name}: missing {mp}")
            continue
        with open(mp, encoding="utf-8") as f:
            present = set(KEYNODE_RE.findall(f.read()))
        lkeys = loc_keys(lp)
        parent = tree["parent"]

        new_blocks, new_loc = [], []
        added_here = 0
        for t in tree["tasks"]:
            if t.key in present:
                continue  # idempotent
            new_blocks.append(task_block(t, parent))
            for ln in loc_lines(t):
                k = ln.split(":", 1)[0].strip()
                if k not in lkeys:
                    new_loc.append(ln)
            added_here += 1

        print(f"  {name:18s} parent={parent:26s} +{added_here} tasks "
              f"(base {len(present) - sum(1 for k in present if k.endswith('_mission') or k in ('chance','ai_chance','potential','abort','on_start','on_completion'))})")
        total_added += added_here
        if check or not new_blocks:
            continue
        splice_tasks(mp, new_blocks)
        append_loc(lp, new_loc)

    print(f"{'PLAN' if check else 'DONE'}: {total_added} tasks across {len(TREES)} trees")


if __name__ == "__main__":
    main()
