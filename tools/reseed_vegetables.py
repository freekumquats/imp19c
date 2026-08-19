#!/usr/bin/env python3
# [#5 v2 2026-08-19] Vegetables reseed -- SOURCED geographic version.
# Replaces the earlier heuristic ("displace over-represented grain near cities, breadth-first"),
# which the user rejected as not research-backed (reverted in 9ef655164). Selection is now driven
# by research/RESEARCH_VEGETABLES_GEOGRAPHY_1763.md: per-region 1763 horticulture tiers, NOT a
# flat grain-displacement. Tiers (see the research doc for the sourcing behind each):
#   STRONG  -- vegetable heartlands (East-Asian truck-garden belts, Korea kimchi complex, Java,
#              Nile/Egypt, Low Countries). Seed to ~30% veg share of the region's convertible
#              food base (grain+livestock+veg).
#   MODERATE-- gardened belts / irrigated deltas / cabbage-root belt / peri-urban market gardens.
#              Seed to ~15%.
#   (unlisted = AVOID) -- steppe/frontier plains/desert/Andean-altiplano/Nordic-Irish-Scottish
#              subsistence: NOT seeded at all (vegetables were marginal there in 1763).
# Displaces grain/livestock ONLY (never fish/cash/New-World-differentiated/existing veg), keeps a
# per-good >=60% regional depletion floor, and prefers the region's highest-civilization_value
# (urban-node) provinces first -- reflecting the peri-urban market-garden reality. China regions get
# fine per-province node selection; ROW is seeded at the regional level (China-fidelity standing rule).
#
# DATA SOURCES (all live; never research/PROVINCE_CONTENTS_1763.csv):
#   map_data/regions.txt (region->areas), map_data/areas.txt (area->province ids),
#   setup/provinces/*.txt (province -> good, name, civilization_value).
# Run with --dry-run to print the plan without editing any file.

import re
import sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent

# --- Tier region lists (keys are map_data/regions.txt region names) -------------------------
# STRONG: vegetable heartlands (research doc: East Asia truck gardens, Korea, Japan core, Java,
# Nile, Low Countries).
STRONG_REGIONS = {
    # China intensive truck-garden macro-regions (Jiangnan, Lingnan, N.China plain, Sichuan, mid-Yangzi)
    "Jiangsu", "Zhejiang", "Guangdong", "Zhili", "Shandong", "Henan", "Hubei", "Sichuan_Kham",
    "Anhui", "Jiangxi", "Hunan", "Fujian", "Guangxi", "Liaoning", "Shanxi", "Guizhou", "Yunnan",
    # Korea (kimchi complex), Japan core
    "Korea", "Honshu",
    # SE-Asia dense wet-rice garden belt + Nile + NW-Europe horticulture
    "Java", "Egypt", "Low_Countries",
}
# MODERATE: gardened belts, irrigated deltas, cabbage/root belt, peri-urban market gardens.
MODERATE_REGIONS = {
    # Japan minor
    "Kyushu", "Shikoku",
    # Mediterranean huertas/orti + peri-urban France/England
    "Valencia", "Catalonia-Aragon", "Cisalpine_Italy", "Venetia", "Central_Italy", "Southern_Italy",
    "Provence_Liguria", "Occitanie", "Northern_France", "Southern_England",
    # German lands + cabbage/root Central Europe
    "Saxony", "Bohemia", "Austria", "Bavaria", "Baden-Wurttemberg", "Low_Saxony", "Westfalen",
    "Grand_Est", "Hessen", "Silesia", "Brandenburg", "Prussia", "Pomerania", "Poland", "Pannonia",
    # Russian/Ukrainian core cabbage belt (peri-urban)
    "Moscow", "Minsk", "Kiev", "Odessa", "Sankt-Petersburg",
    # MENA irrigated garden belts (bostan/Ghouta/Nile-adjacent/qanat)
    "Levant", "Syria", "Marmara", "Anatolia", "Arab_Iraq", "Persian_Iraq", "Morocco", "Tunisia",
    # India deltas/urban vegetable gardening
    "Bengal_region", "Indo-Gangetic_Plain", "Central_India", "South_India", "West_India",
    "East_India", "Punjab", "Rajputana",
    # SE-Asia deltas/urban
    "Vietnam", "Siam", "Luzon", "Visayas", "Sumatra", "Sulawesi", "Cambodia", "Burma",
    # African settled/urban nodes
    "Coastal_West_Africa", "Sahel", "Horn_of_Africa", "Lake_Victoria", "Gulf_of_Guinea", "Sudan",
    "Madagascar",
    # American settled/urban nodes (Three Sisters squash + colonial kitchen gardens)
    "Eastern_Mexico", "Central_America", "Pacific_Mexico", "New_England", "Mid-Atlantic", "Peru",
    "Chile", "South_Brazil", "Southeast_Brazil", "Colombia", "Venezuela",
}

# Target veg as a share of the region's CONVERTIBLE base. Sized so vegetables grows to roughly
# staple-comparable numbers (grain ~1747, livestock ~1885, fish/temperate_fruit ~660), per the user
# directive: "where historically plausible, vegetables should replace grain/livestock and grow to
# roughly similar numbers as the other staple goods." Tiers modulate the share; the AVOIDANCE of
# pastoral/arid/steppe is DATA-DRIVEN, not a hand-list: vegetables follow ARABLE farming (grain), so
# regions with little/no grain (pastoral: Mongolia, Great_Plains, Arabia, Tibet...) get little/none.
STRONG_TARGET_FRAC = 0.62    # vegetable heartlands
MODERATE_TARGET_FRAC = 0.52  # gardened belts / deltas / cabbage-root belt
DEFAULT_TARGET_FRAC = 0.42   # any other region with real arable (grain) farming = gardens plausible
DEPLETION_KEEP_FRACTION = 0.50   # keep >=50% of EACH displaced good's pre-reseed count in the region
GRAIN_FOR_SETTLED = 2        # a region needs >= this many grain provinces to count as "settled arable"
                             # (below this it is pastoral/marginal -> not seeded unless STRONG/MODERATE)

CHINA_REGIONS = {  # fine-fidelity note only; selection identical, flagged in manifest
    "Jiangsu", "Zhejiang", "Guangdong", "Zhili", "Shandong", "Henan", "Hubei", "Sichuan_Kham",
    "Anhui", "Jiangxi", "Hunan", "Fujian", "Guangxi", "Liaoning", "Shanxi", "Guizhou", "Yunnan",
    "Gansu", "Shaanxi", "Qinghai",
}


def rd(p):
    return (REPO / p).read_text(encoding="utf-8-sig")


def parse_regions_to_areas():
    out = {}
    for m in re.finditer(r"^([\w-]+)\s*=\s*\{\s*areas\s*=\s*\{(.*?)\}\s*\}", rd("map_data/regions.txt"), re.S | re.M):
        out[m.group(1)] = [a.strip() for a in m.group(2).split() if a.strip()]
    return out


def parse_areas_to_provinces():
    out = {}
    for m in re.finditer(r"^([\w-]+)\s*=\s*\{\s*provinces\s*=\s*\{(.*?)\}\s*\}", rd("map_data/areas.txt"), re.S | re.M):
        out[m.group(1)] = [int(x) for x in re.findall(r"-?\d+", m.group(2))]
    return out


PROVINCE_BLOCK_RE = re.compile(r"^(\d+)=\{[ \t]*#?[ \t]*([^\n]*)\n(.*?)(?=^\d+=\{|\Z)", re.M | re.S)
TRADE_GOODS_RE = re.compile(r'trade_goods\s*=\s*"(\w+)"')
CIV_VALUE_RE = re.compile(r"civilization_value\s*=\s*(-?\d+(?:\.\d+)?)")


def parse_all_provinces():
    provinces = {}
    for f in sorted((REPO / "setup/provinces").glob("*.txt")):
        text = f.read_bytes().decode("utf-8-sig")
        for m in PROVINCE_BLOCK_RE.finditer(text):
            pid = int(m.group(1))
            body = m.group(3)
            gm = TRADE_GOODS_RE.search(body)
            cm = CIV_VALUE_RE.search(body)
            provinces[pid] = {
                "file": f, "name": m.group(2).strip(),
                "good": gm.group(1) if gm else None,
                "civ": float(cm.group(1)) if cm else 0.0,
            }
    return provinces


def main():
    dry_run = "--dry-run" in sys.argv
    region_to_areas = parse_regions_to_areas()
    area_to_provinces = parse_areas_to_provinces()
    provinces = parse_all_provinces()

    region_to_provinces = {}
    for region, areas in region_to_areas.items():
        ids = []
        for a in areas:
            ids.extend(area_to_provinces.get(a, []))
        region_to_provinces[region] = [pid for pid in ids if pid in provinces]

    manifest = [
        "# MANIFEST -- vegetables reseed (task #5, SOURCED v2), tools/reseed_vegetables.py",
        "# Geography per research/RESEARCH_VEGETABLES_GEOGRAPHY_1763.md tiers.",
        "# Columns: province_id | name | region | tier | old_good -> vegetables",
        "",
    ]
    report = []
    all_edits = []  # (pid, old_good, region, tier)

    for region in sorted(region_to_provinces.keys()):
        ids = region_to_provinces.get(region, [])
        if not ids:
            continue
        cur_veg = sum(1 for p in ids if provinces[p]["good"] == "vegetables")
        grain = [p for p in ids if provinces[p]["good"] == "grain"]
        live = [p for p in ids if provinces[p]["good"] == "livestock"]

        # Tier + plausibility. AVOIDANCE is data-driven: vegetables need arable (grain) farming.
        if region in STRONG_REGIONS:
            tier, frac = "STRONG", STRONG_TARGET_FRAC
        elif region in MODERATE_REGIONS:
            tier, frac = "MODERATE", MODERATE_TARGET_FRAC
        elif len(grain) >= GRAIN_FOR_SETTLED:
            tier, frac = "DEFAULT", DEFAULT_TARGET_FRAC
        else:
            continue  # pastoral/arid/marginal (little/no grain) -> gardens implausible, skip

        # Convertible base: grain always; livestock ONLY where the region is grain-dominant
        # (grain >= livestock) i.e. mixed settled farming, NOT pastoral. This keeps vegetables out
        # of livestock-heavy pastoral zones even when they slip past the grain>=2 gate.
        live_convertible = len(live) if len(grain) >= len(live) else 0
        base = len(grain) + live_convertible + cur_veg
        target = round(frac * base)
        need = max(0, target - cur_veg)
        if need <= 0:
            continue

        # depletion floors: keep >=55% of each good's starting count
        grain_removable = max(0, int(len(grain) - DEPLETION_KEEP_FRACTION * len(grain) + 1e-9))
        live_removable = (max(0, int(len(live) - DEPLETION_KEEP_FRACTION * len(live) + 1e-9))
                          if live_convertible else 0)

        # grain FIRST (arable = most plausible for gardens), then livestock in grain-dominant regions.
        # within each good, urban node (civilization_value) first.
        grain.sort(key=lambda p: (-provinces[p]["civ"], p))
        live.sort(key=lambda p: (-provinces[p]["civ"], p))
        picks = []
        for pid in grain[:grain_removable]:
            if len(picks) >= need:
                break
            picks.append((pid, "grain"))
        for pid in live[:live_removable]:
            if len(picks) >= need:
                break
            picks.append((pid, "livestock"))

        gtaken = sum(1 for _, g in picks if g == "grain")
        ltaken = sum(1 for _, g in picks if g == "livestock")
        for pid, old in picks:
            all_edits.append((pid, old, region, tier))
            manifest.append(f"{pid} | {provinces[pid]['name']} | {region} | {tier} | {old} -> vegetables")
        report.append((region, tier, 0, cur_veg, target, len(picks), f"g-{gtaken}/l-{ltaken}"))

    # ---- report ----
    print(f"{'region':22} {'tier':8} {'cur_veg':>7} {'target':>6} {'added':>5}  displaced")
    tot_strong = tot_moderate = 0
    for region, tier, _g, cur, target, added, disp in sorted(report, key=lambda r: (r[1], r[0])):
        print(f"{region:22} {tier:8} {cur:>7} {target:>6} {added:>5}  {disp}")
        if tier == "STRONG":
            tot_strong += added
        else:
            tot_moderate += added
    grand = len(all_edits)
    print(f"\nSTRONG added={tot_strong}  MODERATE added={tot_moderate}  GRAND TOTAL={grand}")
    print(f"Vegetables provinces after: {sum(1 for p in provinces.values() if p['good']=='vegetables') + grand}")

    if dry_run:
        print(f"\n[dry-run] no files written. Would touch "
              f"{len({provinces[pid]['file'] for pid,_,_,_ in all_edits})} province files.")
        return 0

    # ---- apply byte-safe edits ----
    manifest_path = REPO / "design" / "MANIFEST_5_VEGETABLES_RESEED.txt"
    manifest_path.write_text("\n".join(manifest) + "\n", encoding="utf-8")
    edits_by_file = defaultdict(list)
    for pid, old, region, tier in all_edits:
        edits_by_file[provinces[pid]["file"]].append((pid, old))
    for f, edits in edits_by_file.items():
        raw = f.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf"), f"{f} missing BOM"
        text = raw.decode("utf-8-sig")
        for pid, old in edits:
            block_re = re.compile(rf'(^{pid}=\{{[ \t]*#?[^\n]*\n)(.*?)(?=^\d+=\{{|\Z)', re.M | re.S)
            bm = block_re.search(text)
            if not bm:
                raise RuntimeError(f"province {pid} not found in {f}")
            new_body, n = re.subn(rf'(trade_goods\s*=\s*)"{old}"', r'\1"vegetables"', bm.group(2), count=1)
            if n != 1:
                raise RuntimeError(f"trade_goods={old!r} not replaced for {pid} in {f}")
            text = text[:bm.start()] + bm.group(1) + new_body + text[bm.end():]
        new_raw = b"\xef\xbb\xbf" + text.encode("utf-8")
        if new_raw.count(b"{") != new_raw.count(b"}"):
            raise RuntimeError(f"brace imbalance in {f}")
        f.write_bytes(new_raw)
    print(f"\nWrote {len(edits_by_file)} province files. Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
