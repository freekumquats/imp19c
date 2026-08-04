#!/usr/bin/env python3
"""Generator for province-menu building tooltips of MOD-ADDED buildings.

WHY THIS EXISTS
The province buildings menu renders each building via the `building_item_button`
template (gui/shared/gui_base.gui), whose default tooltip is the loc key
BUILDING_ITEM_WITH_INSTRUCTIONS. That key shows `[BuildingItem.GetBuilding.GetDescription]`
— and the engine's GetDescription COLLAPSES to the "X technology required" line for a
building the player cannot currently build. So a force-seeded building (e.g. the tuntian
military colony, present from 1763 but gated) shows ONLY "Construction technology required"
and HIDES what the building does.

Buildings that already dodge this (arsenal, industrial_estate, port, row_manufactory, …)
do so by pointing their `build_item_*` at a CUSTOM `tooltipwidget` whose `building_tooltip`
renders a hand-written effect description in a `new_tooltip_text_area`, which shows
UNCONDITIONALLY. Every mod-added Qing/IND building already ships a `<building>_desc` loc
string (used by the macro-builder tooltips) — so the fix is purely to (1) point each
regular `build_item_*` at a custom tooltipwidget and (2) emit that tooltipwidget template
reusing the EXISTING `_desc` loc. No new effect text is written here.

SCOPE = mod-added buildings only (not Sobisonator upstream). Determined by diffing
common/buildings/ against sobiso/master: every qing_*, IND_heavy_industry_*, row_* file is
mod-added, plus military_depot_building added into 00_military_buildings.txt. Buildings that
already have a regular tooltipwidget (arsenal, row_manufactory, row_plantation,
military_colony) are skipped automatically (detected in the GUI).

WHAT IT EMITS (to stdout, two fragments the caller splices in, preserving BOM/CRLF):
  1. For gui/shared/gui_templates.gui: the `blockoverride "Tooltip"` line to inject into
     each bare `build_item_<X>` (printed as a per-building marker the caller applies).
  2. For gui/shared/custom_tooltip.gui: a `template building_<X>_tooltip` per building.

USAGE
  python3 tools/gen_building_tooltips.py            # report worklist + emit fragments
  python3 tools/gen_building_tooltips.py --apply    # edit the two GUI files in place

The --apply path is idempotent: it skips any build_item that already has a tooltipwidget
and any template that already exists, so re-running after new buildings are added only
fills the gaps.
"""
import re
import sys
import glob
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUI_TEMPLATES = os.path.join(REPO, "gui/shared/gui_templates.gui")
CUSTOM_TOOLTIP = os.path.join(REPO, "gui/shared/custom_tooltip.gui")
LOC_GLOB = os.path.join(REPO, "localization/english/*.yml")


def read(path):
    """Read preserving whether the file had a BOM; return (text, had_bom)."""
    raw = open(path, "rb").read()
    had_bom = raw[:3] == b"\xef\xbb\xbf"
    return raw.decode("utf-8-sig"), had_bom


def write(path, text, had_bom):
    data = text.encode("utf-8")
    if had_bom:
        data = b"\xef\xbb\xbf" + data
    open(path, "wb").write(data)


def all_loc_keys():
    keys = set()
    for f in glob.glob(LOC_GLOB):
        try:
            txt = open(f, encoding="utf-8-sig", errors="ignore").read()
        except Exception:
            continue
        for m in re.finditer(r"^\s*([A-Za-z0-9_]+):", txt, re.M):
            keys.add(m.group(1))
    return keys


def find_bare_build_items(gui_text):
    """Return [(building_name, full_block_text)] for regular build_item_* blocks
    that do NOT already have a tooltipwidget. Macro build items are separate types
    (macro_build_item_*) and are not matched here."""
    out = []
    for m in re.finditer(
        r"type build_item_([A-Za-z0-9_]+) = building_parts_item \{(.*?)\n\t\}",
        gui_text,
        re.S,
    ):
        name, body = m.group(1), m.group(2)
        if "tooltipwidget" in body:
            continue
        out.append((name, m.group(0)))
    return out


def rewrite_build_item(block, building):
    """Insert the tooltipwidget blockoverride into a bare build_item block.
    Shape-agnostic: works for BOTH the single-line form
        item = { building_item_button = { visible = "..." } }
    and the expanded multi-line form
        item = {
            building_item_button = {
                visible = "..."
            }
        }
    by inserting the blockoverride on its own line immediately AFTER the `visible = "..."`
    line, matching that line's indentation. Returns None if no visible line is found."""
    tt = "building_%s_tooltip" % building
    m = re.search(r'([ \t]*)visible = "[^"]*"\n', block)
    if not m:
        return None
    indent = m.group(1)
    insert = '%sblockoverride "Tooltip" { tooltipwidget = %s }\n' % (indent, tt)
    return block[: m.end()] + insert + block[m.end() :]


def template_for(building, desc_key):
    return (
        "template building_%s_tooltip\n"
        "{\n"
        "\tbuilding_tooltip = {\n"
        "\t\t# [#tooltip-fix gen_building_tooltips.py] show effects even when unbuildable —\n"
        "\t\t# reuse the existing %s loc (the macro-builder tooltip uses the same key).\n"
        '\t\tblockoverride "description" { text = "%s" }\n'
        "\t}\n"
        "}\n" % (building, desc_key, desc_key)
    )


def main():
    apply = "--apply" in sys.argv
    keys = all_loc_keys()
    gui, gui_bom = read(GUI_TEMPLATES)
    ctt, ctt_bom = read(CUSTOM_TOOLTIP)

    bare = find_bare_build_items(gui)
    worklist = []
    skipped_no_desc = []
    for building, block in bare:
        desc_key = "%s_desc" % building
        if desc_key not in keys:
            skipped_no_desc.append(building)
            continue
        worklist.append((building, block, desc_key))

    print("# gen_building_tooltips.py — %d build_items need the fix" % len(worklist), file=sys.stderr)
    for b, _, d in worklist:
        print("#   %-42s -> %s" % (b, d), file=sys.stderr)
    if skipped_no_desc:
        print("# SKIPPED (no _desc loc — would need effect text written first):", file=sys.stderr)
        for b in skipped_no_desc:
            print("#   %s" % b, file=sys.stderr)

    # build the new custom_tooltip templates (skip any already defined)
    new_templates = []
    for building, _, desc_key in worklist:
        if re.search(r"\ntemplate building_%s_tooltip\b" % re.escape(building), ctt):
            continue
        new_templates.append(template_for(building, desc_key))

    if not apply:
        print("\n# ==== FRAGMENT for gui/shared/custom_tooltip.gui (append) ====")
        print("\n".join(new_templates))
        print("\n# ==== gui_templates.gui: %d build_items get a Tooltip blockoverride (use --apply) ====" % len(worklist))
        return

    # APPLY: rewrite each bare build_item in gui_templates, append templates to custom_tooltip
    applied = 0
    for building, block, desc_key in worklist:
        new_block = rewrite_build_item(block, building)
        if new_block is None:
            print("# WARN: unexpected block shape for %s — skipped" % building, file=sys.stderr)
            continue
        if new_block == block:
            continue
        gui = gui.replace(block, new_block, 1)
        applied += 1
    write(GUI_TEMPLATES, gui, gui_bom)

    if new_templates:
        # append before the final closing brace region? custom_tooltip.gui templates sit at
        # top level — safe to append at EOF (templates are order-independent).
        if not ctt.endswith("\n"):
            ctt += "\n"
        ctt += "\n# [#tooltip-fix] regular-menu building tooltips (gen_building_tooltips.py)\n"
        ctt += "\n".join(new_templates)
        write(CUSTOM_TOOLTIP, ctt, ctt_bom)

    print("# APPLIED: %d build_item Tooltip overrides, %d new templates" % (applied, len(new_templates)), file=sys.stderr)


if __name__ == "__main__":
    main()
