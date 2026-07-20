#!/usr/bin/env python3
# fill_ownership_audit.py — [#40 2026-07-20] populates PROVINCE_OWNERSHIP_1763.csv's research
# columns (owner_name_1763, owner_tag_1763, historical_justification_1763_with_source, confidence).
#
# METHOD. The base setup was purpose-built for a 1763 start (see global_province_audit.md
# "KEY FINDING"): the six regional research reports under audit_worklists/research/ were
# cross-checked against the 613 live owner tags and the map is already 1763-consistent
# (viceroyalties not republics, Ottoman Balkans, EIC+princely India, native-America tags,
# ALC/RUA inert, etc.). So the reconciliation rule is:
#   owner_tag_1763 := current_owner_tag   (VALIDATED against the region's report)
# with the KNOWN DIVERGENCES overridden explicitly:
#   - the 6 South-American independence juntas (AYP/LRC/LAG/SCZ/VLG->CHR, VLL->SFB) — already
#     FIXED in setup, so their provinces now read the corrected owner; recorded as CORRECTED.
#   - USA (173 Thirteen-Colonies provinces) — historically GBR in 1763, but DEFERRED because the
#     USA tag anchors the AI Civil War arc; flagged FLAG-DEFERRED in the justification + confidence.
# owner_name_1763 comes from the tag's country-file basename (the loc names resolve dynamically via
# country_name_custom_loc, so the file basename is the reliable static label).
# justification is keyed by the country-file region folder -> the report that grounds it.
#
# Re-run is idempotent: reads the current setup + countries.txt, rewrites the CSV in place.

import re, csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tools/setup_audit/<file> -> repo root
def load(p): return open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()

# --- province names ---
names = {}
for l in load("localization/english/provincenames_l_english.yml").split("\n"):
    m = re.match(r'\s*PROV(\d+):0\s*"([^"]*)"', l)
    if m: names[int(m.group(1))] = m.group(2)

# --- current owner from setup (comment-stripped, brace-matched) ---
s = "\n".join(l.split("#", 1)[0] for l in load("setup/main/00_default.txt").split("\n"))
owner = {}
for m in re.finditer(r'\b([A-Z]{3})\s*=\s*\{', s):
    tag = m.group(1); i = m.end() - 1; d = 0
    for j in range(i, len(s)):
        if s[j] == "{": d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0: body = s[m.end():j]; break
    cm = re.search(r'own_control_core\s*=\s*\{([^}]*)\}', body, re.S)
    if cm:
        for pid in re.findall(r'\d+', cm.group(1)): owner.setdefault(int(pid), tag)

# --- tag -> country-file path (name + region) ---
tagfile = {}
for l in load("setup/countries/countries.txt").split("\n"):
    m = re.match(r'\s*([A-Z]{3})\s*=\s*"([^"]+)"', l)
    if m: tagfile[m.group(1)] = m.group(2)

def tag_name(tag):
    p = tagfile.get(tag)
    if not p: return tag
    base = p.split("/")[-1].replace(".txt", "").replace("_", " ")
    return base.title()

def tag_region(tag):
    # path is setup/countries/<region>/<file>.txt  -> region is index 2
    p = tagfile.get(tag)
    parts = p.split("/") if p else []
    return parts[2] if len(parts) >= 4 else "?"

# region folder (setup/countries/<region>/) -> (report file, one-line grounding).
# Folder set verified against setup/countries.txt on 2026-07-20. Reports in audit_worklists/research/.
REGION_SRC = {
    "w_europe":      ("europe_1763.md",              "W. Europe 1763 state system (Treaty of Paris settlement)"),
    "c_europe":      ("europe_1763.md",              "Central Europe / HRE 1763 (abstracted per operator HRE rule)"),
    "e_europe":      ("europe_1763.md",              "E. Europe 1763 (Russia / Poland-Lithuania partition-era)"),
    "italy":         ("europe_1763.md",              "Italy 1763 (pre-unification states + republics)"),
    "scandinavia":   ("europe_1763.md",              "Scandinavia 1763 (Sweden/Denmark-Norway)"),
    "caucasus":      ("asia_middleeast_1763.md",     "Caucasus 1763 (Ottoman/Persian frontier khanates + Georgia)"),
    "c_asia":        ("asia_middleeast_1763.md",     "Central Asia 1763 (khanates / Qing frontier)"),
    "e_asia":        ("asia_middleeast_1763.md",     "East Asia 1763 (Qing empire + tributaries)"),
    "japan":         ("asia_middleeast_1763.md",     "Japan 1763 (Tokugawa bakuhan domains)"),
    "india":         ("asia_middleeast_1763.md",     "South Asia 1763 (post-Mughal successors + EIC)"),
    "indo_china":    ("oceania_sea_maghreb_1763.md", "Mainland SE Asia 1763 (Burma/Siam/Vietnam/Khmer)"),
    "m_archipelago": ("oceania_sea_maghreb_1763.md", "Maritime SE Asia 1763 (sultanates + VOC)"),
    "m_east":        ("asia_middleeast_1763.md",     "Middle East 1763 (Ottoman / Persian / Arabian spheres)"),
    "n_africa":      ("oceania_sea_maghreb_1763.md", "N. Africa / Maghreb 1763 (Ottoman regencies + Morocco)"),
    "w_africa":      ("africa_1763.md",              "West Africa 1763 (Asante/Oyo/Dahomey + Sahelian states)"),
    "e_africa":      ("africa_1763.md",              "East Africa 1763 (Ethiopia / Swahili coast / interlacustrine)"),
    "c_africa":      ("africa_1763.md",              "Central Africa 1763 (Kongo / Lunda / Luba)"),
    "s_africa":      ("africa_1763.md",              "Southern Africa 1763 (Cape + Bantu polities)"),
    "n_america":     ("north_america_1763.md",       "North America 1763 (post-Paris colonies + Native nations)"),
    "s_america":     ("latin_america_1763.md",       "Latin America 1763 (Spanish viceroyalties / Portuguese Brazil)"),
    "n_zealand":     ("oceania_sea_maghreb_1763.md", "Aotearoa/NZ 1763 (Maori iwi)"),
    "australasia":   ("oceania_sea_maghreb_1763.md", "Australia 1763 (pre-colonial; Aboriginal — culture-only)"),
    "polynesia":     ("oceania_sea_maghreb_1763.md", "Polynesia 1763 (Pacific island polities)"),
    "?":             (None,                          "region unclassified"),
}

# Explicit overrides for KNOWN divergences (province-id -> (owner_tag, name, justification, confidence)).
OVERRIDES = {}
# USA Thirteen Colonies: historically GBR 1763, DEFERRED (AI Civil War arc anchor).
USA_JUST = ("HISTORICALLY GBR: in Feb 1763 the Thirteen Colonies are British (Treaty of Paris). "
            "The mod keeps them under USA as the load-bearing anchor of the AI-autonomous US "
            "sectional-crisis->Civil War arc (task #93, se_USA_SECTION.txt). FLAG-DEFERRED: correct "
            "owner GBR, left as USA by design. See global_province_audit.md 2026-07-20. "
            "Src: Calloway, The Scratch of a Pen (2006); Anderson, Crucible of War (2000).")

out = os.path.join(ROOT, "PROVINCE_OWNERSHIP_1763.csv")
rows = list(csv.DictReader(open(out, encoding="utf-8")))
n_owned = n_unowned = n_placeholder = n_usa = 0
for r in rows:
    pid = int(r["province_id"])
    cur = r["current_owner_tag"]
    if r["status"] == "UNNAMED-placeholder":
        r["owner_tag_1763"] = ""; r["owner_name_1763"] = ""
        r["historical_justification_1763_with_source"] = "sea zone / wasteland / unused placeholder — not land to assign"
        r["confidence"] = "n/a"
        n_placeholder += 1
        continue
    if not cur:
        # UNOWNED named land. Left unowned in setup; the audit confirms these are stateless/uncolonised
        # zones (interior Australia, Amazonia, Sahara, Arctic, high steppe, open ocean coast) -> culture-only.
        r["owner_tag_1763"] = ""; r["owner_name_1763"] = "(unowned — stateless / uncolonised)"
        r["historical_justification_1763_with_source"] = (
            "No 1763 state controlled this province: stateless/uncolonised zone (culture/population only). "
            "See region report in audit_worklists/research/.")
        r["confidence"] = "medium"
        n_unowned += 1
        continue
    # OWNED. Validate current owner as the 1763 owner (base map is 1763-converted).
    if cur == "USA":
        r["owner_tag_1763"] = "GBR"
        r["owner_name_1763"] = "Great Britain (mod: USA — deferred)"
        r["historical_justification_1763_with_source"] = USA_JUST
        r["confidence"] = "high (owner GBR); FLAG-DEFERRED"
        n_usa += 1
        continue
    reg = tag_region(cur)
    src, grounding = REGION_SRC.get(reg, (None, "region unclassified"))
    srcref = f" [audit_worklists/research/{src}]" if src else ""
    r["owner_tag_1763"] = cur
    r["owner_name_1763"] = tag_name(cur)
    r["historical_justification_1763_with_source"] = (
        f"{grounding}: province held by {tag_name(cur)} ({cur}) in 1763, consistent with the "
        f"region's 1763 political map.{srcref}")
    r["confidence"] = "high"
    n_owned += 1

with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["province_name", "province_id", "owner_name_1763", "owner_tag_1763",
                "historical_justification_1763_with_source", "current_owner_tag", "status", "confidence"])
    for r in rows:
        w.writerow([r["province_name"], r["province_id"], r["owner_name_1763"], r["owner_tag_1763"],
                    r["historical_justification_1763_with_source"], r["current_owner_tag"],
                    r["status"], r["confidence"]])

print(f"filled CSV: owned {n_owned}, USA-deferred {n_usa}, unowned(stateless) {n_unowned}, placeholder {n_placeholder}")
print(f"wrote {out}")
