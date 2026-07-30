#!/usr/bin/env python3
"""
gen_table_icons.py — bespoke icons for the doc-table categories (panels, trade goods,
event pictures, modifier-cost glyphs, building-type icons, military traditions).

Each entry: key -> (kind, query|url). ('D', url) forces a direct upload.wikimedia.org
URL; ('S', query) does a Commons search; ('S', [q1, q2, ...]) tries each query in turn
until one yields a legible photo. Curated queries come from placeholder_icons.md
§2/§3/§3b/§4/§5/§6 concepts (BUILDINGS also carries the 37 new building keys from the
buildings-research batch, commit 1ea45ce52). Writes DDS via dds_icon.convert; GUI/def
repointing is done by a companion step (repoint_refs.py) so this file only produces art.

Search results are quality-filtered (smart_fetch): PDF/map/document thumbnails and
near-black/near-uniform scans are rejected so the picked source is an actual photograph.
The brightness/detail score needs PIL+numpy; if they're absent it degrades to the plain
top hit. (Base python3 usually lacks them — run under a venv with Pillow+numpy.)

Idempotent: skips an out_path that already exists unless run with --force (this protects
already-committed curated art from being replaced by a different search pick on re-run).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch, download
from dds_icon import convert

# Titles whose top Commons hit is typically NOT a usable photo (maps, scans, crests).
BAD_TITLE = ("map", "plan", "pdf", ".svg", "document", "diagram", "chart", "book",
             "letter", "manuscript", "stamp", "coat of arms", "seal ", "memorial")

def _candidates(query, width=400, limit=12):
    """Commons File-namespace search -> [(thumb_url, title)], jpeg/png only, bad
    titles dropped, in search-rank order."""
    import json, urllib.parse
    from fetch_wm import _get, API
    params = {"action": "query", "generator": "search", "gsrsearch": query,
              "gsrnamespace": 6, "gsrlimit": limit, "prop": "imageinfo",
              "iiprop": "url|mime", "iiurlwidth": width, "format": "json"}
    j = json.loads(_get(API + "?" + urllib.parse.urlencode(params)).decode("utf-8"))
    pages = (j.get("query") or {}).get("pages") or {}
    out = []
    for p in sorted(pages.values(), key=lambda p: p.get("index", 999)):
        ii = (p.get("imageinfo") or [{}])[0]
        t = (p.get("title") or "").lower()
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        if not ii.get("thumburl"):
            continue
        if any(b in t for b in BAD_TITLE):
            continue
        out.append((ii["thumburl"], p.get("title")))
    return out

def _photo_ok(path):
    """True if the raster reads like a legible photo (not a near-black/near-uniform
    document scan). Needs PIL+numpy; if unavailable, accept unconditionally."""
    try:
        import numpy as np
        from PIL import Image
    except Exception:
        return True
    im = np.asarray(Image.open(path).convert("RGB"), dtype="float32")
    return (25 < im.mean() < 235) and im.std() > 28

def smart_fetch(spec, src):
    """('D', url) downloads the curated URL directly (trusted). ('S', query|[queries])
    searches Commons, skipping PDF/map/document thumbnails and near-black scans, and
    keeps the first legible photo. Falls back to the plain top hit if none pass."""
    kind, val = spec
    if kind == "D":
        n = download(val, src)
        return f"direct:{val} ({n}B)"
    queries = val if isinstance(val, list) else [val]
    for q in queries:
        for url, title in _candidates(q):
            try:
                download(url, src)
                if _photo_ok(src):
                    return f"search:'{q}' -> {title}"
            except Exception:
                continue
    # nothing passed the filter: plain top hit of the first query
    _, desc = fetch(("search", queries[0]), src, width=400)
    return desc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def g(*p): return os.path.join(ROOT, "gfx", "interface", *p)
SRC = os.path.join(ROOT, "art_src", "table")
LOG = os.path.join(ROOT, "tools", "table_icon_log.tsv")
os.makedirs(SRC, exist_ok=True)

MENU   = g("icons", "menu_buttons", "menu_trade.dds")        # 50x50 shaped-alpha donor
TRADE  = g("icons", "tradegoods", "coal.dds")                # 50x50 shaped-alpha donor
BLDG   = g("icons", "buildings", "EDU_school.dds")           # 200x200 donor
MODIF  = g("icons", "modifiers", "commerce_value.dds")       # 50x50 shaped-alpha donor
EVENT  = g("event_window", "Event_senate_debate.dds")        # DXT donor (opaque)
def TRAD():
    import glob
    c = sorted(glob.glob(g("icons","military_traditions","arabic_*.dds")))
    return c[0] if c else g("icons","military_traditions","arabic_african_path_5.dds")

# ---- category tables: key -> (out_dds, donor, query) -----------------------------------
# ('D', url) forces a direct upload.wikimedia.org URL; ('S', q) does a Commons search.

PANELS = {
 # menu_buttons/qing_<panel>.dds  (repoint the .gui texture= line)
 "qing_zongli":        ("D","https://upload.wikimedia.org/wikipedia/commons/7/7e/Four_Members_of_the_Tsung-li_Yam%C3%AAn.jpg"),
 "qing_lifanyuan":     ("S","Lifan Yuan Qing court colonial affairs"),
 "qing_greatgame":     ("S","Great Game Central Asia 19th century map"),
 "qing_censorate":     ("S","Qing censor official portrait"),
 "qing_hanlin":        ("S","Hanlin Academy Beijing"),
 "qing_justice":       ("S","Qing dynasty court punishment yamen"),
 "qing_rites_ministry":("S","Qing dynasty ancestral rite ceremony"),
 "qing_southern_study":("S","Forbidden City study hall qing"),
 "qing_upper_study":   ("S","Qing palace school study"),
 "qing_deliberative":  ("S","Manchu Deliberative Council princes"),
 "qing_guard":         ("S","Qing imperial guard soldier"),
 "qing_war_ministry":  ("S","Qing Eight Banners military flag"),
 "qing_xinjiang":      ("D","https://upload.wikimedia.org/wikipedia/commons/7/71/Qing_dynasty_and_Xinjiang.jpg"),
 "qing_personnel":     ("S","Qing dynasty mandarin official portrait"),
 "qing_caravan":       ("S","Silk Road camel caravan Kashgar"),
 "qing_harem":         ("S","Qing dynasty imperial consort portrait"),
 "qing_household":     ("S","Forbidden City hall Beijing"),
 "qing_opium":         ("S","19th century Chinese opium den"),
 "qing_population":    ("S","Along the River During the Qingming Festival crowd"),
 "qing_princes":       ("S","Qing dynasty prince portrait"),
 "qing_revenue_ministry":("S","Chinese sycee silver ingot"),
 "qing_secretariat":   ("S","Grand Council Qing dynasty office"),
 "qing_works_ministry":("S","Grand Canal China engineering"),
}

TRADEGOODS = {
 "maize":        ("D","https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Corncobs.jpg/640px-Corncobs.jpg"),
 "sweet_potato": ("S","sweet potato tuber"),
 "potato":       ("S","potatoes tubers"),
 "peanut":       ("S","peanuts groundnuts"),
 "chili":        ("S","red chili peppers"),
 "porcelain":    ("S","Jingdezhen blue and white porcelain vase"),
 "rifles":       ("S","19th century percussion musket rifle"),
 # [#144 I12] Phase-5 new goods. saltpetre = raw; refined_sugar/silk_cloth/paper/dyes/gunpowder = manufactured.
 "saltpetre":    ("S","white saltpetre potassium nitrate mineral crystals"),
 "refined_sugar":("S","refined white sugar loaf and crystals"),
 "silk_cloth":   ("S","bolt of woven silk cloth fabric"),
 "paper":        ("S","stack of handmade paper sheets"),
 "dyes":         ("S","jars of coloured textile dye pigment powder"),
 "gunpowder":    ("S","black gunpowder powder and powder horn"),
}

# building-TYPE icons (200x200) at gfx/interface/icons/buildings/<key>.dds — currently stopgap-copied
BUILDINGS = {
 "qing_shuyuan_building":        ("S","Chinese academy shuyuan hall"),
 "qing_yamen_building":          ("S","Chinese yamen government office building"),
 "qing_granary_building":        ("S","Chinese granary storehouse"),
 "qing_customs_house_building":  ("S","Chinese maritime customs house building"),
 "qing_silk_filature_building":  ("S","silk reeling filature"),
 "qing_porcelain_kiln_building": ("S","Jingdezhen porcelain kiln"),
 "qing_tea_workshop_building":   ("S","Chinese tea processing workshop"),
 "qing_cotton_workshop_building":("S","cotton textile mill 19th century"),
 "qing_salt_yard_building":      ("S","Chinese salt evaporation works"),
 "qing_opium_poppy_farm_building":("S","opium poppy field"),
 "qing_selfstr_wonder_building": ("S","Jiangnan Arsenal Shanghai"),
 "qing_dike_building":           ("S","Yellow River dike embankment"),
 "qing_grand_canal_building":    ("S","Grand Canal China"),
 "qing_canal_depot_building":    ("S","Chinese canal grain barge"),
 "qing_great_wall_building":     ("S","Great Wall of China"),
 "qing_wall_section_building":   ("S","Great Wall of China rampart"),
 "qing_embassy_building":        ("S","19th century legation embassy building"),
 "qing_foreign_concession_building":("S","Shanghai foreign concession bund"),
 "qing_foreign_works_building":  ("S","19th century arsenal machine works China"),
 "qing_frontier_colony_building":("S","tuntian military agricultural colony"),
 "qing_frontier_fort_building":  ("S","Qing frontier fort Xinjiang"),
 "qing_mission_cathedral_building":("S","cathedral in China 19th century"),
 "qing_mission_public_building": ("S","Christian church China 19th century"),
 "qing_mission_underground_building":("S","secret chapel prayer"),
 "qing_treaty_port_building":    ("S","treaty port China waterfront"),
 "military_depot_building":      ("S","military supply depot warehouse"),
 "row_manufactory_building":     ("S","19th century factory manufactory"),
 "row_plantation_building":      ("S","colonial plantation"),

 # --- buildings-research batch (37 new keys, commit 1ea45ce52). Queries are the
 # --- concrete historical subjects that produced the committed art; list-valued
 # --- entries carry the fallback queries used when the first hit was a map/scan. ---
 # Industry (China-specific)
 "qing_steel_works_building":        ("S","Hanyang Iron Works"),
 "qing_textile_mill_building":       ("S","cotton mill 19th century interior"),
 "qing_machine_works_building":      ("S","Jiangnan Arsenal Shanghai"),
 "qing_navy_yard_building":          ("S","Foochow Arsenal"),
 "qing_coal_mine_building":          ("S",["colliery coal mine workers historic","Chinese coal mine miners historic photograph","coal mine surface buildings historic photograph"]),
 "qing_telegraph_building":          ("S","telegraph office 19th century"),
 "qing_tongwen_guan_building":       ("S","Zongli Yamen Qing dynasty"),
 "qing_imperial_university_building":("S","Imperial University of Peking"),
 # Industry (generic worldwide)
 "IND_coal_mine_building":           ("S",["colliery winding tower headframe","coal mine pit head wheel"]),
 "IND_blast_furnace_building":       ("S","blast furnace 19th century ironworks"),
 "IND_electric_plant_building":      ("S","electric power station 1890s dynamo"),
 "IND_gasworks_building":            ("S","Victorian gasworks gasometer"),
 # Garrison / military
 "qing_banner_garrison_building":    ("S","Manchu banner garrison Manchu city"),
 "qing_horse_pasture_building":      ("S","Mongolian horse herd grassland"),
 "qing_green_standard_post_building":("S",["Qing dynasty soldier photograph","Chinese soldiers Qing army historic photograph"]),
 "qing_coastal_battery_building":    ("S",["Bogue forts cannon","Dagu Forts cannon","Chinese fort cannon Opium War historic photograph"]),
 "qing_military_colony_building":    ("S","Jiayuguan fortress Great Wall"),
 # Agriculture / hydraulic
 "qing_river_conservancy_building":  ("S",["Grand Canal China historic photograph","Chinese river embankment stone historic","Yellow River dike flood control China"]),
 "qing_dujiangyan_building":         ("S","Dujiangyan irrigation system"),
 "qing_karez_building":              ("S",["qanat irrigation shaft","karez qanat Turpan underground irrigation"]),
 "qing_fishpond_dyke_building":      ("S","fish pond aquaculture China"),
 "qing_polder_building":             ("S",["terraced paddy field China","rice paddy terraces Yangtze delta"]),
 "qing_community_granary_building":  ("S",["traditional Chinese barn building","Chinese granary storehouse historic photograph"]),
 # Scholarship
 "qing_hanlin_academy_building":     ("S","Hanlin Academy"),
 "qing_guozijian_building":          ("S",["Guozijian Beijing archway","Biyong Hall Imperial College Beijing"]),
 "qing_examination_hall_building":   ("S","Nanjing examination hall Jiangnan Gongyuan"),
 # Commerce / fiscal
 "qing_mint_building":               ("S",["ancient Chinese bronze coins","Chinese cash coins pile photograph"]),
 "qing_draft_bank_building":         ("S","Rishengchang draft bank Pingyao"),
 "qing_guild_hall_building":         ("S","huiguan guild hall China"),
 "qing_tribute_depot_building":      ("S",["Chinese warehouse building historic photograph","junk boat Grand Canal China historic"]),
 "qing_likin_station_building":      ("S",["Chinese Maritime Customs Service building","Shanghai Customs House"]),
 "qing_imperial_bank_building":      ("S",["HSBC Building Shanghai Bund","bank building Shanghai Bund historic"]),
 # Religion
 "qing_temple_of_heaven_building":   ("S","Temple of Heaven Beijing"),
 "qing_ancestral_temple_building":   ("S","Taimiao Imperial Ancestral Temple Beijing"),
 "qing_confucian_temple_building":   ("S","Temple of Confucius Beijing"),
 "qing_gelug_monastery_building":    ("S","Tibetan Buddhist monastery Gelug"),
 "qing_great_mosque_building":       ("S","Great Mosque of Xian"),
}

EVENTS = {  # event_window/qing_<alias>.dds  (repoint picture=)
 "qing_senate":     ("S","parliament chamber assembly hall"),
 "qing_navy":       ("S","age of sail naval battle warship"),
 "qing_greek_siege":("S","walled city under siege"),
}

# [#117] NATIONAL-IDEA icons. Each national idea (common/ideas/00_imperatrix_ideas.txt)
# resolves art by filename at gfx/interface/icons/ideas/<key>.dds (72x72) + <key>_small.dds
# (40x40). Only civilising_mission + defender_of_the_faith shipped icons; the other 15
# rendered blank. Curated concept queries below; the ideas job writes BOTH sizes per key.
IDEAS = {
 # military_ideas
 "idea_world_police":        ("S",["gunboat diplomacy 19th century warship","19th century naval squadron flags"]),
 "idea_spanish_revanchism":  ("S",["Ferdinand VII Spain portrait","Spanish royalist army 19th century"]),
 "idea_gott_mit_uns":        ("S",["Prussian soldier Pickelhaube helmet","German infantry soldier 1870 uniform"]),
 "idea_qing_banner_host":    ("S",["Eight Banners Qing soldier armour","Manchu bannerman Qing cavalry"]),
 # civic_ideas
 # Mercantilism — Jean-Baptiste Colbert, Louis XIV's mercantilist minister.
 "idea_mercantilism":        ("D","https://commons.wikimedia.org/wiki/Special:FilePath/"
   "Jean-Baptiste_Colbert.jpg?width=800"),
 "idea_free_trade":          ("S",["19th century free trade port merchant ships","Manchester cotton exchange 19th century"]),
 "idea_monopsony":           ("S",["company town factory 19th century","single buyer market monopoly warehouse"]),
 # 摊丁入亩 — the Qing land-poll tax merger; a silver sycee ingot reads the fiscal reform.
 "idea_qing_tanding":        ("S",["sycee silver ingot Chinese","Chinese silver tael ingot Qing dynasty"]),
 # oratory_ideas
 "idea_merchant_colonialism":("S",["East India Company trading post factory","colonial merchant trading house Asia"]),
 # Settler colonialism — John Gast, "American Progress" (1872), the westward-settlement allegory.
 "idea_settler_colonialism": ("D","https://commons.wikimedia.org/wiki/Special:FilePath/"
   "American_Progress_(John_Gast_painting).jpg?width=800"),
 # Isolationism — the Great Wall of China, the archetypal shut-out-the-world rampart.
 "idea_isolationism":        ("D","https://commons.wikimedia.org/wiki/Special:FilePath/"
   "GreatWall_2004_Summer_4.jpg?width=800"),
 # 萬國來朝 — envoys of many nations at the Qing court (the tributary order); known-good PD scan.
 "idea_qing_tributary_system":("D","https://upload.wikimedia.org/wikipedia/commons/8/8f/"
   "%E4%B8%87%E5%9B%BD%E6%9D%A5%E6%9C%9D%E5%9B%BE_Myanmar_%28%E7%BC%85%E7%94%B8"
   "%E5%9B%BD%29_delegates_in_Peking_in_1761.jpg"),
 # Counter-colonialism — Boxer Uprising fighters resisting the foreign powers.
 "idea_counter_colonialism": ("D","https://commons.wikimedia.org/wiki/Special:FilePath/"
   "Boxer_Rebellion.jpg?width=800"),
 # religious_ideas
 # Pan-nationalism — Delacroix, "Liberty Leading the People" (1830), the flag-borne national rising.
 "idea_pan_nationalism":     ("D","https://commons.wikimedia.org/wiki/Special:FilePath/"
   "Eug%C3%A8ne_Delacroix_-_Le_28_Juillet._La_Libert%C3%A9_guidant_le_peuple.jpg?width=800"),
 "idea_qing_reverence_heaven":("S",["Temple of Heaven Beijing altar ceremony","Qing emperor heaven sacrifice ritual"]),
}

def main(force=False):
    # BLDG donor: EDU_school is a DX10 (compressed) icon, so convert() would keep the
    # icon opaque — fine, but the new building icons were cut against the legacy-BGRA8
    # qing_salt_yard_building donor. Prefer it when present for byte-identical output.
    bldg_donor = g("icons","buildings","qing_salt_yard_building.dds")
    if not os.path.exists(bldg_donor):
        bldg_donor = BLDG
    jobs = [
        (PANELS,     g("icons","menu_buttons"),        MENU),
        (TRADEGOODS, g("icons","tradegoods"),          TRADE),
        (BUILDINGS,  g("icons","buildings"),           bldg_donor),
        (EVENTS,     g("event_window"),                EVENT),
    ]
    ok = skip = err = 0
    with open(LOG,"w",encoding="utf-8") as log:
        log.write("key\tquery\tsource\tstatus\n")
        for table, outdir, donor in jobs:
            print("==", os.path.basename(outdir), f"({len(table)})")
            for key,spec in table.items():
                out = os.path.join(outdir, key + ".dds")
                if os.path.exists(out) and not force:
                    log.write(f"{key}\t-\t-\tSKIP (exists)\n"); skip += 1; continue
                src = os.path.join(SRC, key + ".jpg")
                try:
                    if os.path.exists(src):
                        desc = "cached"
                    else:
                        desc = smart_fetch(spec, src)
                    convert(src, out, like=donor)
                    log.write(f"{key}\t{spec[1]}\t{desc}\tOK\n"); print(f"  OK {key}"); ok += 1
                except Exception as e:
                    log.write(f"{key}\t{spec[1]}\tERR\t{e}\n"); print(f"  ERR {key}: {e}"); err += 1
    print(f"done ok={ok} skip={skip} err={err} ->", LOG)

def gen_ideas(force=False):
    """[#117] National-idea icons: BOTH sizes per key — <key>.dds (72x72) + <key>_small.dds
    (40x40), opaque squares matching the two shipped idea icons. Source photo fetched once
    per key and cut to both sizes."""
    outdir = g("icons", "ideas"); os.makedirs(outdir, exist_ok=True)
    ok = skip = err = 0
    with open(os.path.join(ROOT,"tools","idea_icon_log.tsv"),"w",encoding="utf-8") as log:
        log.write("key\tquery\tsource\tstatus\n")
        print("== ideas", f"({len(IDEAS)})")
        for key, spec in IDEAS.items():
            big   = os.path.join(outdir, key + ".dds")
            small = os.path.join(outdir, key + "_small.dds")
            if os.path.exists(big) and os.path.exists(small) and not force:
                log.write(f"{key}\t-\t-\tSKIP (exists)\n"); skip += 1; continue
            src = os.path.join(SRC, "idea_src_" + key + ".jpg")
            try:
                desc = "cached" if os.path.exists(src) else smart_fetch(spec, src)
                convert(src, big,   size=72)
                convert(src, small, size=40)
                log.write(f"{key}\t{spec[1]}\t{desc}\tOK\n"); print(f"  OK {key} (72+40)"); ok += 1
            except Exception as e:
                log.write(f"{key}\t{spec[1]}\tERR\t{e}\n"); print(f"  ERR {key}: {e}"); err += 1
    print(f"ideas done ok={ok} skip={skip} err={err}")

if __name__ == "__main__":
    force = "--force" in sys.argv
    if "--ideas" in sys.argv:
        gen_ideas(force=force)
    else:
        main(force=force)
