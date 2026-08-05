#!/usr/bin/env python3
"""[#33] Complete every mod-added building's `modification_display` block so the province
building panel's "Results:" section lists ALL of the building's engine-modifier keys — the
fortress-template standard (fortress lists fort_level + value_manpower + local_defensive, i.e.
every modifier it grants). Buildings that currently curate 2-4 keys leave the rest to fall to
"Other Results:" (or not show at all); the user's #33 requirement is that Results list every
appropriate (engine-key) modifier, and Other Results hold only the non-engine-key/scripted
provisions. So we expand modification_display to the full modifier set.

MECHANISM (verified against the repo, not assumed):
- modification_display is a curated ordered list `{ 0 = key  1 = key ... }` of modifier keys
  the panel renders as icons under "Results:". The fortress (the user's gold-standard template,
  00_military_buildings.txt) lists EVERY modifier it has. Vanilla/upstream buildings curate to a
  handful; the mod's IND_* buildings curate to 2. #33 changes the mod-added buildings to list all.
- A "modifier key" here = a TOP-LEVEL `key = <number>` line in the building body that is not a
  structural key (cost/time/fort_level handled explicitly; fort_level IS renderable so kept).
  All keys observed are standard engine modifiers (local_*, base_resources, army_movement_speed,
  fort_level) — every one is a valid modification_display entry (base_resources/fort_level proven
  by IND_coal_mine / fortress).

SCOPE = mod-added building files only (qing_*, IND_heavy_industry_*, row_*). Upstream/vanilla
(00_*) buildings are LEFT ALONE (proven-code rule — do not reformat Sobisonator/vanilla curation).

USAGE
  python3 tools/gen_building_modification_display.py            # report the diff, write nothing
  python3 tools/gen_building_modification_display.py --apply    # rewrite the files in place

Idempotent: re-running after the sweep is a no-op (the block already lists every key). Preserves
BOM/encoding. Only the modification_display block is touched; nothing else in the building moves.
"""
import re, sys, glob, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = [f for f in glob.glob(os.path.join(REPO, "common/buildings/*.txt"))
         if re.search(r"(qing_|IND_heavy|row_)", os.path.basename(f))]

# structural keys that are NOT rendered as modifier icons. fort_level IS a renderable
# modifier (fortress lists it), so it is NOT structural.
STRUCTURAL = {"cost", "time"}


def read(path):
    raw = open(path, "rb").read()
    bom = raw[:3] == b"\xef\xbb\xbf"
    return raw.decode("utf-8-sig"), bom


def write(path, text, bom):
    data = text.encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    open(path, "wb").write(data)


def building_blocks(text):
    """Yield (name, start, end) for each top-level *_building = { ... } block."""
    for m in re.finditer(r"(?m)^([A-Za-z_][A-Za-z0-9_]*_building)\s*=\s*\{", text):
        i = m.end(); d = 1
        while d and i < len(text):
            if text[i] == "{": d += 1
            elif text[i] == "}": d -= 1
            i += 1
        yield m.group(1), m.start(), i


def top_level_modifier_keys(body):
    """Ordered list of top-level `key = number` modifier keys in the building body,
    in source order, excluding structural keys. Strips one level of nested blocks
    (allow/potential/modification_display/on_*) so their inner keys don't leak in."""
    flat = re.sub(r"\{[^{}]*\}", "", body)  # drop innermost nested blocks
    # then drop any remaining nested blocks (2nd pass for allow{owner{...}} etc.)
    while re.search(r"\{[^{}]*\}", flat):
        flat = re.sub(r"\{[^{}]*\}", "", flat)
    keys = []
    for m in re.finditer(r"(?m)^\s*([a-z_][a-z0-9_]*)\s*=\s*-?[0-9]", flat):
        k = m.group(1)
        if k in STRUCTURAL:
            continue
        if k not in keys:
            keys.append(k)
    return keys


def main():
    apply = "--apply" in sys.argv
    total_changed = 0
    for path in sorted(FILES):
        text, bom = read(path)
        # process blocks back-to-front so offsets stay valid as we splice
        blocks = list(building_blocks(text))
        newtext = text
        file_changes = []
        for name, start, end in reversed(blocks):
            block = text[start:end]
            body = block[block.index("{") + 1: block.rindex("}")]
            keys = top_level_modifier_keys(body)
            if not keys:
                continue  # a building with no modifiers (pure fort_level handled as a key anyway)
            # find the existing modification_display block within this building
            md = re.search(r"([ \t]*)modification_display\s*=\s*\{[^}]*\}", block)
            # build the new block with the SAME indentation the existing one used (or a tab).
            indent = md.group(1) if md else "\t"
            entry_indent = indent + "\t"
            lines = "\n".join("%s%d = %s" % (entry_indent, i, k) for i, k in enumerate(keys))
            new_md = "%smodification_display = {\n%s\n%s}" % (indent, lines, indent)
            if md:
                # current keys, to detect a no-op
                cur = re.findall(r"=\s*([a-z_][a-z0-9_]*)", md.group(0))
                if cur == keys:
                    continue  # already complete + in order
                new_block = block[:md.start()] + new_md + block[md.end():]
            else:
                # no modification_display at all: insert before the building's final closing brace
                ci = block.rindex("}")
                new_block = block[:ci] + new_md + "\n" + indent[:-1] + block[ci:] if False else \
                            block[:ci] + new_md + "\n" + block[ci:]
            newtext = newtext[:start] + new_block + newtext[end:]
            file_changes.append((name, keys))
        if file_changes:
            total_changed += len(file_changes)
            print("# %s: %d buildings" % (os.path.basename(path), len(file_changes)), file=sys.stderr)
            for name, keys in reversed(file_changes):
                print("#   %-40s -> %s" % (name, ", ".join(keys)), file=sys.stderr)
            # brace balance guard
            if newtext.count("{") != newtext.count("}"):
                print("# ABORT: brace imbalance in %s — not writing" % path, file=sys.stderr)
                sys.exit(1)
            if apply:
                write(path, newtext, bom)
    print("# %s %d buildings" % ("APPLIED to" if apply else "WOULD change", total_changed), file=sys.stderr)


if __name__ == "__main__":
    main()
