#!/usr/bin/env python3
# [#5 2026-08-18] Vegetables Fix A -- geographic reseed of vegetables into deficit trade zones.
# Implements DESIGN_93_VEGETABLES_FIX_A_GEOGRAPHIC_RESEED.md sections 5/6, with the SIZING
# rule directed by the task brief (probe-first sizing per the design's own S3 is blocked: the
# live TZP BAND "order" metric is supply-scaled post-collapse -- see
# DESIGN_14_VEGETABLES_DEMAND_COLLAPSE_DIAGNOSIS.md -- so it cannot be read as raw demand).
# SIZING USED HERE (guess-and-log, boot-tunable):
#   target_veg(zone) = 0.15 * food_province_count(zone) * 1.25   [15% ratio + 25% margin]
#   additions(zone)  = max(0, target_veg(zone) - current_veg(zone))
# applied ONLY to the DESIGN #4 collapse-set (19 zones); central_europe/india/baltic are the
# sizing-ratio ANCHOR and are left untouched, per the task brief -- NOTE: the honest post-x4-revert
# boot (2026-08-18, ~/Downloads/logs.zip) shows these 3 zones ALSO now hit stock=0 (just later:
# quarter 4/6 vs quarter 1/2 for the 19), so the anchor itself is degrading. Flagged in the report;
# out of THIS task's scope to decide (setup-data reseed only, no formula edits -- that is #14/#15).
#
# DATA SOURCES (all live, none from research/PROVINCE_CONTENTS_1763.csv per design S6):
#   - common/scripted_triggers/00_tradezone_triggers.txt  -> zone -> region list (trigger_if only,
#     `#`-commented is_in_region lines ignored -- these are dead/moved memberships, see design S4).
#   - map_data/regions.txt   -> region -> area list
#   - map_data/areas.txt     -> area -> province id list
#   - setup/provinces/*.txt  -> province id -> {file, good, name, civilization_value}
#
# OUTPUT: prints a per-zone sizing table, applies BOM/tab-preserving byte edits to
# setup/provinces/*.txt, and writes a manifest to design/MANIFEST_5_VEGETABLES_RESEED.txt.
#
# Run with --dry-run to print the plan without touching any province file.

import re
import sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Design S4 -- the 19 collapsing zones this task targets, and the 3 survivor/anchor zones.
# ---------------------------------------------------------------------------
COLLAPSE_ZONES = [
    "atlantic_seaboard", "caribbean", "east_africa", "east_europe", "east_mediterranean",
    "east_north_america", "east_south_america", "eastern_steppe", "indo_china", "middle_east",
    "south_east_asia", "southern_africa", "upper_yangtzi", "west_africa", "west_mediterranean",
    "west_north_america", "west_south_america", "western_steppe", "yellow_sea",
]
ANCHOR_ZONES = ["central_europe", "india", "baltic"]

# Design S5 -- literal-zero / thin regions to prefer first within each zone.
PREFER_THIN_REGIONS = {
    "Korea", "Kyushu", "Honshu", "Zhejiang", "Jiangsu", "Taiwan",
    "Congo_Basin", "Angola", "South_Africa",
    "Argentina", "American_Southwest", "Appalachia", "Antilles",
}

# Design S5/S2 -- goods that may be displaced (grain/livestock ONLY -- fish struck, review Finding 2).
DISPLACEABLE_GOODS = {"grain", "livestock"}

# Provincial food goods (used to compute each zone's "food province" denominator for sizing).
FOOD_GOODS = {"grain", "livestock", "fish", "vegetables", "temperate_fruit",
              "maize", "potato", "sweet_potato", "tropical_fruit"}

# Design S3/S10 -- first-pass sizing constants (guess-and-log, boot-tunable).
RATIO = 0.15
MARGIN = 1.25

# Design S6 -- per-region depletion guard: keep >= this fraction of a region's provinces of the
# displaced good before allowing a flip (proxy for "region production - 1 >= region local demand").
DEPLETION_KEEP_FRACTION = 0.60


def parse_tradezone_triggers():
    """zone -> ordered list of LIVE region names (trigger_if section only, # lines skipped)."""
    text = (REPO / "common/scripted_triggers/00_tradezone_triggers.txt").read_text(encoding="utf-8-sig")
    if not text.endswith("\n"):
        text += "\n"
    zone_to_regions = {}
    for m in re.finditer(r"(\w+)_tradezone\s*=\s*\{(.*?)\n\}\n", text, re.S):
        zone, body = m.group(1), m.group(2)
        if zone == "any_governorship_in":
            continue
        m2 = re.search(r"trigger_if\s*=\s*\{(.*?)\n\s*\}\s*\n\s*trigger_else", body, re.S)
        section = m2.group(1) if m2 else body
        regions = []
        for line in section.splitlines():
            s = line.strip()
            if s.startswith("#"):
                continue
            m3 = re.match(r"is_in_region\s*=\s*([\w-]+)", s)
            if m3:
                regions.append(m3.group(1))
        zone_to_regions[zone] = regions
    return zone_to_regions


def parse_regions_to_areas():
    """region name -> list of area names."""
    text = (REPO / "map_data/regions.txt").read_text(encoding="utf-8-sig")
    out = {}
    for m in re.finditer(r"^([\w-]+)\s*=\s*\{\s*areas\s*=\s*\{(.*?)\}\s*\}", text, re.S | re.M):
        region, body = m.group(1), m.group(2)
        areas = [a.strip() for a in body.split() if a.strip()]
        out[region] = areas
    return out


def parse_areas_to_provinces():
    """area name -> list of province ids (int)."""
    text = (REPO / "map_data/areas.txt").read_text(encoding="utf-8-sig")
    out = {}
    for m in re.finditer(r"^([\w-]+)\s*=\s*\{\s*provinces\s*=\s*\{(.*?)\}\s*\}", text, re.S | re.M):
        area, body = m.group(1), m.group(2)
        ids = [int(x) for x in re.findall(r"-?\d+", body)]
        out[area] = ids
    return out


PROVINCE_BLOCK_RE = re.compile(r"^(\d+)=\{[ \t]*#?[ \t]*([^\n]*)\n(.*?)(?=^\d+=\{|\Z)", re.M | re.S)
TRADE_GOODS_RE = re.compile(r'trade_goods\s*=\s*"(\w+)"')
CIV_VALUE_RE = re.compile(r"civilization_value\s*=\s*(-?\d+(?:\.\d+)?)")


def parse_all_provinces():
    """province id -> dict(file=Path, name=str, good=str|None, civ=float)."""
    provinces = {}
    files = sorted((REPO / "setup/provinces").glob("*.txt"))
    for f in files:
        if f.name == "00_0_setup.txt_old":
            continue
        raw = f.read_bytes()
        text = raw.decode("utf-8-sig")
        for m in PROVINCE_BLOCK_RE.finditer(text):
            pid, name, body = int(m.group(1)), m.group(2).strip(), m.group(3)
            gm = TRADE_GOODS_RE.search(body)
            good = gm.group(1) if gm else None
            cm = CIV_VALUE_RE.search(body)
            civ = float(cm.group(1)) if cm else 0.0
            provinces[pid] = {"file": f, "name": name, "good": good, "civ": civ}
    return provinces


def build_region_to_provinces(region_to_areas, area_to_provinces):
    out = {}
    for region, areas in region_to_areas.items():
        ids = []
        for a in areas:
            ids.extend(area_to_provinces.get(a, []))
        out[region] = ids
    return out


def main():
    dry_run = "--dry-run" in sys.argv

    zone_to_regions = parse_tradezone_triggers()
    region_to_areas = parse_regions_to_areas()
    area_to_provinces = parse_areas_to_provinces()
    region_to_provinces = build_region_to_provinces(region_to_areas, area_to_provinces)
    provinces = parse_all_provinces()

    print(f"# Parsed {len(zone_to_regions)} zones, {len(region_to_areas)} regions, "
          f"{len(provinces)} provinces.", file=sys.stderr)

    # province id -> owning region name (reverse map; a province should belong to exactly one region)
    province_to_region = {}
    for region, ids in region_to_provinces.items():
        for pid in ids:
            province_to_region[pid] = region

    # Region-level running counts of each displaceable good, used by the depletion guard.
    # good -> region -> count (recomputed as we flip provinces during selection)
    region_good_count = defaultdict(lambda: defaultdict(int))
    for pid, region in province_to_region.items():
        p = provinces.get(pid)
        if not p:
            continue
        if p["good"] in DISPLACEABLE_GOODS:
            region_good_count[p["good"]][region] += 1
    region_total_count = defaultdict(int)
    for pid, region in province_to_region.items():
        region_total_count[region] += 1

    # Frozen PRE-reseed snapshot of each (good, region) count -- the depletion floor is a
    # fraction of THIS starting count, not of the region's unrelated total province count
    # (a region can be genuinely thin on a good with plenty of other land uses; comparing
    # against total province count would make the floor unreachable for such regions).
    region_good_count_pre = {
        good: dict(region_good_count[good]) for good in DISPLACEABLE_GOODS
    }

    def depletion_ok(good, region):
        """Design S6: region production of `good` minus this flip must stay >= 60% of that
        good's OWN pre-reseed count in the region (proxy for region local demand)."""
        cur = region_good_count[good][region]
        if cur <= 0:
            return False
        pre = region_good_count_pre[good].get(region, 0)
        keep_floor = DEPLETION_KEEP_FRACTION * pre
        return (cur - 1) >= keep_floor

    manifest_lines = []
    manifest_lines.append("# MANIFEST -- vegetables reseed (task #5), generated by tools/reseed_vegetables.py")
    manifest_lines.append("# Columns: province_id | name | region | zone | old_good -> vegetables")
    manifest_lines.append("")

    per_zone_report = []
    per_region_pre = region_good_count_pre  # same frozen snapshot the depletion guard uses

    all_edits = []  # (pid, old_good) tuples, in application order
    grand_total_added = 0

    for zone in COLLAPSE_ZONES:
        regions = zone_to_regions.get(zone, [])
        zone_pids = []
        for r in regions:
            zone_pids.extend(region_to_provinces.get(r, []))
        zone_pids = [pid for pid in zone_pids if pid in provinces]

        current_veg = sum(1 for pid in zone_pids if provinces[pid]["good"] == "vegetables")
        food_prov_count = sum(1 for pid in zone_pids if provinces[pid]["good"] in FOOD_GOODS)

        target_veg = round(RATIO * food_prov_count * MARGIN)
        additions_needed = max(0, target_veg - current_veg)

        # Group zone provinces by governorship proxy = region (breadth-first spread, design S3/S5:
        # "deficit governorships" -- the setup's closest static analogue to a governorship is its
        # region, since governorships are dynamic player-assigned groupings not present in setup data).
        # Candidates: displaceable-good provinces, not already vegetables, grouped by region.
        candidates_by_region = defaultdict(list)
        for pid in zone_pids:
            p = provinces[pid]
            if p["good"] in DISPLACEABLE_GOODS:
                candidates_by_region[province_to_region.get(pid)].append(pid)

        # Order regions: thin/literal-zero-preferred regions first, then by descending candidate
        # surplus size (more headroom first), then name for determinism.
        def region_sort_key(region):
            is_thin = 0 if region in PREFER_THIN_REGIONS else 1
            return (is_thin, -len(candidates_by_region[region]), region)

        ordered_regions = sorted(candidates_by_region.keys(), key=region_sort_key)

        # Within each region, order candidates by (bulk-staple surplus size desc [region-level,
        # constant within region], civilization_value desc, province_id asc) per design S5.
        for region in ordered_regions:
            candidates_by_region[region].sort(
                key=lambda pid: (-provinces[pid]["civ"], pid)
            )

        added_this_zone = []
        # Breadth-first round-robin across regions: one province per region per pass.
        cursor = {region: 0 for region in ordered_regions}
        made_progress = True
        while len(added_this_zone) < additions_needed and made_progress:
            made_progress = False
            for region in ordered_regions:
                if len(added_this_zone) >= additions_needed:
                    break
                lst = candidates_by_region[region]
                idx = cursor[region]
                while idx < len(lst):
                    pid = lst[idx]
                    idx += 1
                    good = provinces[pid]["good"]
                    if not depletion_ok(good, region):
                        continue
                    # Commit this flip (in-memory) so subsequent depletion checks in this zone see it.
                    region_good_count[good][region] -= 1
                    provinces[pid]["good"] = "vegetables"
                    added_this_zone.append((pid, good, region))
                    made_progress = True
                    break
                cursor[region] = idx

        grand_total_added += len(added_this_zone)
        all_edits.extend(added_this_zone)

        per_zone_report.append({
            "zone": zone, "food_prov": food_prov_count, "current_veg": current_veg,
            "target_veg": target_veg, "additions_needed": additions_needed,
            "additions_made": len(added_this_zone),
        })

        for pid, old_good, region in added_this_zone:
            p = provinces[pid]
            manifest_lines.append(f"{pid} | {p['name']} | {region} | {zone} | {old_good} -> vegetables")

    # --- Report ---
    print(f"{'zone':22} {'food_prov':>9} {'cur_veg':>8} {'target':>7} {'need':>5} {'added':>6}")
    for r in per_zone_report:
        print(f"{r['zone']:22} {r['food_prov']:>9} {r['current_veg']:>8} {r['target_veg']:>7} "
              f"{r['additions_needed']:>5} {r['additions_made']:>6}")
    print(f"\nGRAND TOTAL ADDED: {grand_total_added}")

    # [#5 2026-08-18] The ~400 guard was the sizing-review's SANITY threshold against a selection
    # bug, not a hard cap. It was hit at 510 and the team lead confirmed this is the honest
    # 0.15x1.25-over-19-zones arithmetic (parser validated against DESIGN_93's own numbers;
    # depletion guard blocked nothing) -- raised to 600 as the new bug-detection ceiling.
    if grand_total_added > 600:
        print("STOP: total additions exceed 600 -- likely a selection bug. Aborting without edits.",
              file=sys.stderr)
        return 1

    # Per-region pre/post counts of the displaced good, for the manifest.
    manifest_lines.append("")
    manifest_lines.append("# Per-region pre/post counts of the displaced good (depletion headroom)")
    touched_region_goods = set()
    for pid, old_good, region in all_edits:
        touched_region_goods.add((old_good, region))
    for good, region in sorted(touched_region_goods):
        pre = per_region_pre[good][region]
        post = region_good_count[good][region]
        total = region_total_count[region]
        manifest_lines.append(f"{good} in {region}: pre={pre} post={post} region_total_provinces={total}")

    manifest_path = REPO / "design" / "MANIFEST_5_VEGETABLES_RESEED.txt"
    if dry_run:
        print(f"\n[dry-run] would write manifest to {manifest_path} and edit "
              f"{len({p['file'] for pid,_,_ in all_edits for p in [provinces[pid]]})} province files.")
        return 0

    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # --- Apply byte-safe edits, grouped by file ---
    edits_by_file = defaultdict(list)
    for pid, old_good, region in all_edits:
        edits_by_file[provinces[pid]["file"]].append((pid, old_good))

    files_touched = []
    for f, edits in edits_by_file.items():
        raw = f.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf"), f"{f} missing BOM"
        text = raw.decode("utf-8-sig")
        for pid, old_good in edits:
            # Locate this exact province block and replace ONLY its trade_goods line.
            block_re = re.compile(
                rf'(^{pid}=\{{[ \t]*#?[^\n]*\n)(.*?)(?=^\d+=\{{|\Z)', re.M | re.S
            )
            bm = block_re.search(text)
            if not bm:
                raise RuntimeError(f"province {pid} block not found in {f} during edit pass")
            header, body = bm.group(1), bm.group(2)
            new_body, n = re.subn(
                rf'(trade_goods\s*=\s*)"{old_good}"', r'\1"vegetables"', body, count=1
            )
            if n != 1:
                raise RuntimeError(f"trade_goods={old_good!r} not replaced for province {pid} in {f}")
            text = text[:bm.start()] + header + new_body + text[bm.end():]
        new_raw = b"\xef\xbb\xbf" + text.encode("utf-8")
        # Brace-balance check
        if new_raw.count(b"{") != new_raw.count(b"}"):
            raise RuntimeError(f"brace imbalance after edit in {f}: "
                                f"{{ count={new_raw.count(b'{')} }} count={new_raw.count(b'}')}")
        f.write_bytes(new_raw)
        files_touched.append(f)

    print(f"\nWrote {len(files_touched)} province files. Manifest: {manifest_path}")
    for f in sorted(files_touched):
        print(f"  {f.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
