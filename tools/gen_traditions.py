#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_traditions.py — [#129] breadth-expand the Qing/Manchu/Napoleon military-tradition
trees to >=20 nodes each, table-driven, using ONLY the proven node idiom + proven
combat-modifier keys already present in these files.

Per tree we add N new nodes (qing 5x +11, manchu +9, napoleon +6 = 70) so every tree
reaches 20. Each new node:
  <key> = {
      icon = <key>
      requires = { <anchor> }              # hangs off an existing node in the SAME tree
      [ai_will_do = { modifier = { trigger = { <t> } add = { value = v } } }]  # only if the
                                            # tree already uses per-node ai_will_do
      modifier = { <proven_key> = <val> ... }
  }
Introduces ZERO new modifiers/effects/triggers — only the exact keys + ai triggers the
existing nodes in each tree use. Loc: `<key>:0 "Title (CJK)"` + `<key>_desc:0 "desc"`
appended to military_traditions_l_english.yml (matches shipped format). Icons handled
separately by the canonical tools/gen_tradition_icons.py (loc-driven, idempotent).

Idempotent: a node already present (its `<key> = {` node line) is skipped; re-running only
adds what is missing. Pass --check to print the plan without writing.
ABORTS if any new key already exists as a FOREIGN tradition node (one this table did not
author) — no clobber.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MT   = os.path.join(ROOT, "common", "military_traditions")
LOC  = os.path.join(ROOT, "localization", "english", "military_traditions_l_english.yml")


class N:
    """One new tradition node."""
    __slots__ = ("key", "cjk", "en", "desc", "req", "mods")
    def __init__(self, key, cjk, en, desc, req, mods):
        self.key, self.cjk, self.en, self.desc, self.req, self.mods = key, cjk, en, desc, req, mods


# ai_will_do: the per-node trigger a tree uses, or None if the tree has no per-node ai_will_do.
# file: which 00_*.txt the tree lives in. tree: the tree's node key (col-0 opener).
TREES = [
    # ================= 00_qing.txt =================
    {"file": "00_qing.txt", "tree": "qing_eight_banners_tradition",
     "ai": "country_culture_group = jurchen", "nodes": [
        N("qing_banner_xiaoqi", "驍騎營", "Light Cavalry Camp",
          "The Xiaoqi, the main mounted reserve of the metropolitan banners.",
          "qing_banner_start", [("light_cavalry_offensive", 0.1), ("global_manpower_modifier", 0.05)]),
        N("qing_banner_hujun", "護軍營", "Guards Division",
          "The Hujun, the household guard that stood watch over the Forbidden City.",
          "qing_banner_start", [("heavy_infantry_defensive", 0.1), ("land_morale_modifier", 0.05)]),
        N("qing_banner_bujun", "步軍營", "Gendarmerie",
          "The Bujun, the infantry-and-police command that kept order in the capital.",
          "qing_banner_garrison", [("global_unrest", -0.5), ("global_defensive", 0.05)]),
        N("qing_banner_hanjun", "漢軍八旗", "Han Martial Banners",
          "The Hanjun bannermen who served the heavy guns and the musket lines.",
          "qing_banner_firearms", [("artillery_offensive", 0.1), ("siege_ability", 0.1)]),
        N("qing_banner_mongol", "蒙古八旗", "Mongol Banners",
          "The Mongol banners of the Eight-Banner establishment, the empire's shock horse.",
          "qing_banner_cavalry", [("light_cavalry_movement_speed", 0.1), ("light_cavalry_plains_combat_bonus", 0.1)]),
        N("qing_banner_solon", "索倫勁旅", "Solon Levies",
          "The Solon and Daur hunters of the Amur, the finest archers of the frontier.",
          "qing_banner_cavalry", [("archers_offensive", 0.1), ("cohort_reinforcement_speed", 0.05)]),
        N("qing_banner_huqiang", "虎槍營", "Tiger-Spear Camp",
          "The Huqiang, the imperial hunt-guard schooled to face beasts and men with the spear.",
          "qing_banner_vanguard", [("heavy_infantry_offensive", 0.1)]),
        N("qing_banner_shanpu", "善撲營", "Buku Wrestlers",
          "The Shanpu, the palace wrestlers and close guard of the emperor's person.",
          "qing_banner_hujun", [("land_morale_modifier", 0.05)]),
        N("qing_banner_upper_three", "上三旗", "Upper Three Banners",
          "The Plain and Bordered Yellow and Plain White banners, held by the emperor himself.",
          "qing_banner_capstone", [("global_cohort_start_experience", 0.1), ("ruler_popularity_gain", 0.1)]),
        N("qing_banner_generals", "駐防將軍", "Garrison Generals",
          "The Tartar generals who commanded the great provincial banner garrisons.",
          "qing_banner_niru", [("fort_maintenance_cost", -0.1), ("global_defensive", 0.05)]),
        N("qing_banner_yuanmingyuan", "圓明園護軍", "Summer Palace Guard",
          "The banner guard raised to watch the imperial gardens of the Yuanmingyuan.",
          "qing_banner_hujun", [("global_defensive", 0.1)]),
     ]},
    {"file": "00_qing.txt", "tree": "qing_green_standard_tradition", "ai": None, "nodes": [
        N("qing_green_biao", "督標", "Governor-General's Command",
          "The biao battalions attached directly to each governor-general and governor.",
          "qing_green_start", [("global_manpower_modifier", 0.1), ("land_morale_modifier", 0.05)]),
        N("qing_green_fen", "分防汛", "Dispersed Garrisons",
          "The web of small posts that put a Green-Standard squad in every county.",
          "qing_green_garrison", [("global_unrest", -0.5)]),
        N("qing_green_transport", "塘馬遞運", "Courier & Transport Corps",
          "The relay horses and baggage trains that moved the provincial army.",
          "qing_green_start", [("army_movement_speed", 0.1)]),
        N("qing_green_musket", "鳥槍隊", "Matchlock Companies",
          "The matchlock musketeers who gave the provincial infantry its firepower.",
          "qing_green_battalion", [("archers_offensive", 0.1)]),
        N("qing_green_artillery", "綠營砲隊", "Field-Gun Batteries",
          "The Green-Standard gun crews serving the light field pieces.",
          "qing_green_musket", [("artillery_offensive", 0.1), ("artillery_discipline", 0.1)]),
        N("qing_green_hills", "山地綠營", "Highland Battalions",
          "The mountain battalions of the southwest, at home in broken country.",
          "qing_green_rattan", [("light_infantry_hills_combat_bonus", 0.1)]),
        N("qing_green_colony", "屯田綠營", "Military Colonies",
          "The tuntian farms that fed and settled the standing provincial army.",
          "qing_green_garrison", [("army_maintenance_cost", -0.05), ("global_manpower_modifier", 0.05)]),
        N("qing_green_river", "河標", "River Defence Command",
          "The river commands that policed the Yangzi and the Grand Canal.",
          "qing_green_marines", [("blockade_efficiency", 0.1)]),
        N("qing_green_relief", "協餉", "Inter-Provincial Subsidy",
          "The xiexiang transfers that funded the armies of the poorer frontier provinces.",
          "qing_green_biao", [("army_maintenance_cost", -0.05)]),
        N("qing_green_veteran", "綠營宿將", "Veteran Officers",
          "The seasoned provincial officers who carried the memory of past wars.",
          "qing_green_drill", [("global_cohort_start_experience", 0.05), ("land_morale_recovery", 0.1)]),
        N("qing_green_reserve", "額外外委", "Supernumerary Officers",
          "The reserve of brevet officers ready to raise fresh battalions in emergency.",
          "qing_green_guard", [("global_manpower_modifier", 0.05)]),
     ]},
    {"file": "00_qing.txt", "tree": "qing_mongol_cavalry_tradition", "ai": None, "nodes": [
        N("qing_mongol_jasak", "札薩克旗", "Jasak Banners",
          "The hereditary banner-princes who mustered the steppe for the emperor.",
          "qing_mongol_start", [("global_manpower_modifier", 0.05), ("light_cavalry_movement_speed", 0.05)]),
        N("qing_mongol_relay", "塔站驛傳", "Steppe Relay Stations",
          "The tai relay posts that carried orders and remounts across the grasslands.",
          "qing_mongol_start", [("army_movement_speed", 0.1), ("global_supply_limit_modifier", 0.05)]),
        N("qing_mongol_lance", "蒙古長矛", "Mongol Lancers",
          "The heavy lance-horse of the banners, the hammer of the charge.",
          "qing_mongol_raiders", [("light_cavalry_offensive", 0.1)]),
        N("qing_mongol_horsearcher", "蒙古弓騎", "Mongol Horse Archers",
          "The bow-cavalry that harried an enemy to ruin before the lances struck.",
          "qing_mongol_raiders", [("archers_offensive", 0.1), ("light_cavalry_plains_combat_bonus", 0.1)]),
        N("qing_mongol_remount", "官馬廠", "Imperial Horse Pastures",
          "The state stud-farms that kept the banners deep in remounts.",
          "qing_mongol_start", [("light_cavalry_movement_speed", 0.1), ("cohort_reinforcement_speed", 0.05)]),
        N("qing_mongol_winter", "寒地行軍", "Winter Campaigning",
          "The hardened columns that could march and fight through the steppe winter.",
          "qing_mongol_endurance", [("hostile_attrition", 1), ("land_unit_attrition", -0.05)]),
        N("qing_mongol_gobi", "瀚海之師", "Gobi Column",
          "The desert-crossing cavalry that could strike over the waterless waste.",
          "qing_mongol_endurance", [("light_cavalry_desert_combat_bonus", 0.1)]),
        N("qing_mongol_torghut", "土爾扈特", "Torghut Return",
          "The Torghut who trekked back from the Volga to serve under the banners.",
          "qing_mongol_league", [("light_cavalry_discipline", 0.1), ("global_manpower_modifier", 0.05)]),
        N("qing_mongol_leaguelaw", "盟旗制度", "League-Banner System",
          "The league assemblies that bound the Mongol banners to the Lifan-Yuan order.",
          "qing_mongol_chahar", [("subject_loyalty", 0.1), ("loyalty_to_overlord", 0.1)]),
        N("qing_mongol_lamas", "藏傳護法", "Lamaist Blessing",
          "The Gelug lamas whose blessing steadied the faith and courage of the horse.",
          "qing_mongol_hunt", [("land_morale_modifier", 0.05)]),
        N("qing_mongol_scouts", "探馬", "Scout Screens",
          "The tamma scout-screens that were the eyes of the banner army.",
          "qing_mongol_khalkha", [("army_movement_speed", 0.1)]),
     ]},
    {"file": "00_qing.txt", "tree": "qing_frontier_defence_tradition", "ai": None, "nodes": [
        N("qing_frontier_amban", "駐防大臣", "Resident Ambans",
          "The imperial residents who governed the frontier dominions in the emperor's name.",
          "qing_frontier_start", [("subject_loyalty", 0.1), ("global_defensive", 0.05)]),
        N("qing_frontier_beacon", "烽燧墩臺", "Beacon Towers",
          "The chain of watch-towers that carried warning of raids across the frontier.",
          "qing_frontier_pickets", [("global_defensive", 0.1)]),
        N("qing_frontier_ili", "伊犁將軍", "Ili General",
          "The general of Ili, supreme commander of the whole New Dominion.",
          "qing_frontier_colonies", [("fort_maintenance_cost", -0.1), ("global_manpower_modifier", 0.05)]),
        N("qing_frontier_beg", "回部伯克", "Beg Administration",
          "The Muslim begs who ruled the Tarim oases under the empire's warrant.",
          "qing_frontier_desert", [("subject_loyalty", 0.1), ("global_unrest", -0.5)]),
        N("qing_frontier_passes", "邊牆關隘", "Frontier Passes",
          "The fortified passes and gates that sealed the roads into the empire.",
          "qing_frontier_start", [("global_defensive", 0.1), ("fort_maintenance_cost", -0.05)]),
        N("qing_frontier_postroad", "軍臺驛遞", "Military Post-Roads",
          "The military courier roads that knit the far garrisons to the centre.",
          "qing_frontier_supply", [("army_movement_speed", 0.1)]),
        N("qing_frontier_reclaim", "開墾戍邊", "Frontier Reclamation",
          "The soldier-farmers who broke new land to root the garrisons in the frontier.",
          "qing_frontier_colonies", [("global_manpower_modifier", 0.05), ("army_maintenance_cost", -0.05)]),
        N("qing_frontier_tibet", "駐藏定制", "Tibet Garrison Code",
          "The standing code that governed the garrison on the roof of the world.",
          "qing_frontier_highland", [("heavy_infantry_mountain_combat_bonus", 0.1)]),
        N("qing_frontier_oirat", "厄魯特降眾", "Submitted Oirat",
          "The Oirat who came over to the empire and rode in its frontier columns.",
          "qing_frontier_native", [("light_cavalry_offensive", 0.1)]),
        N("qing_frontier_granary", "邊糧儲備", "Frontier Granaries",
          "The stockpiled grain that let a garrison outlast a siege or a hard winter.",
          "qing_frontier_supply", [("global_supply_limit_modifier", 0.1)]),
        N("qing_frontier_watch", "換防輪戍", "Rotation Watch",
          "The regular relief of the frontier watch that kept the garrisons fresh.",
          "qing_frontier_rotation", [("land_morale_recovery", 0.1)]),
     ]},
    {"file": "00_qing.txt", "tree": "qing_tributary_levy_tradition", "ai": None, "nodes": [
        N("qing_tributary_lifan", "理藩院", "Court of Colonial Affairs",
          "The Lifan-Yuan that managed the Mongol, Tibetan and Muslim dependencies.",
          "qing_tributary_start", [("subject_loyalty", 0.1), ("loyalty_to_overlord", 0.1)]),
        N("qing_tributary_annam", "安南貢使", "Annamese Tribute",
          "The tribute embassies of Annam, restored to the throne's investiture.",
          "qing_tributary_investiture", [("subject_loyalty", 0.1)]),
        N("qing_tributary_ryukyu", "琉球入貢", "Ryukyu Tribute",
          "The Ryukyu missions that carried the empire's writ out onto the eastern sea.",
          "qing_tributary_revenue", [("blockade_efficiency", 0.1)]),
        N("qing_tributary_siam", "暹羅朝貢", "Siamese Tribute",
          "The rich Siamese tribute that fattened the southern treasuries.",
          "qing_tributary_revenue", [("army_maintenance_cost", -0.05)]),
        N("qing_tributary_tusi_levy", "土司徵調", "Tusi War-Levies",
          "The native chieftains' warbands, summoned to fight in the broken southwest.",
          "qing_tributary_tusi", [("light_infantry_forest_combat_bonus", 0.1)]),
        N("qing_tributary_kazakh", "哈薩克內附", "Kazakh Submission",
          "The Kazakh hordes who acknowledged the throne and traded their fine horses.",
          "qing_tributary_host", [("light_cavalry_offensive", 0.1)]),
        N("qing_tributary_mart", "邊境互市", "Frontier Markets",
          "The licensed border marts that turned tributary trade into revenue.",
          "qing_tributary_revenue", [("army_maintenance_cost", -0.05)]),
        N("qing_tributary_hostage", "質子宿衛", "Hostage Guard",
          "The tributary princes kept at court, both surety and honoured guard.",
          "qing_tributary_investiture", [("monthly_general_loyalty", 0.05)]),
        N("qing_tributary_code", "藩屬軍律", "Tributary War-Code",
          "The rules of muster and command that disciplined the summoned levies.",
          "qing_tributary_host", [("global_cohort_start_experience", 0.05)]),
        N("qing_tributary_muster", "會盟徵兵", "Grand Muster",
          "The great assembly at which the whole tributary order was called to arms.",
          "qing_tributary_mobilise", [("global_manpower_modifier", 0.1)]),
        N("qing_tributary_loyalists", "歸誠義勇", "Loyalist Volunteers",
          "The volunteers of the submitted peoples, eager to prove their loyalty in war.",
          "qing_tributary_auxiliaries", [("global_manpower_modifier", 0.05), ("land_morale_modifier", 0.05)]),
     ]},
    # ================= 00_manchu.txt =================
    {"file": "00_manchu.txt", "tree": "manchu_shiquan",
     "ai": "country_culture_group = jurchen", "nodes": [
        N("shiquan_amursana", "阿睦爾撒納之亂", "Amursana's Revolt",
          "The crushing of Amursana's rising that sealed the conquest of Dzungaria.",
          "shiquan_dzungar_2", [("global_unrest", -0.5), ("cohort_reinforcement_speed", 0.05)]),
        N("shiquan_ili", "伊犁屯戍", "Ili Garrison",
          "The permanent garrison and colonies planted to hold the conquered Ili valley.",
          "shiquan_altishahr", [("global_manpower_modifier", 0.05), ("fort_maintenance_cost", -0.05)]),
        N("shiquan_khoja", "大小和卓", "The Khoja Brothers",
          "The reduction of the Khoja brothers that broke resistance in the Tarim oases.",
          "shiquan_altishahr", [("archers_desert_combat_bonus", 0.1)]),
        N("shiquan_stockades", "金川碉樓", "Stockade-Breakers",
          "The sappers and heavy guns that finally cracked the Jinchuan watch-towers.",
          "shiquan_jinchuan_2", [("siege_engineers", 0.1), ("assault_ability", 0.05)]),
        N("shiquan_penghu", "澎湖水師", "Penghu Squadron",
          "The fleet that carried the army across to reconquer rebel Taiwan.",
          "shiquan_taiwan", [("blockade_efficiency", 0.1), ("naval_morale_modifier", 0.05)]),
        N("shiquan_konbaung", "木邦孟拱", "Burmese Marches",
          "The bitter lessons of the Burma jungle, paid for in fever and blood.",
          "shiquan_burma", [("land_unit_attrition", -0.1)]),
        N("shiquan_thanglong", "昇龍之役", "Battle of Thang Long",
          "The lightning march that seized Thang Long before the tide turned.",
          "shiquan_vietnam", [("army_movement_speed", 0.1)]),
        N("shiquan_himalaya", "喜馬拉雅", "Himalayan Crossing",
          "The march over the highest passes on earth to the gates of Kathmandu.",
          "shiquan_gurkha", [("global_supply_limit_modifier", 0.1), ("hostile_attrition", 1)]),
        N("shiquan_stele", "御製碑文", "Victory Stelae",
          "The stone stelae the emperor raised to proclaim the ten complete victories.",
          "shiquan_laoren", [("ruler_popularity_gain", 0.1), ("land_morale_modifier", 0.05)]),
     ]},
    # ================= 00_napoleon.txt =================
    {"file": "00_napoleon.txt", "tree": "napoleon_grande_armee",
     "ai": "has_variable = qing_napoleon_present", "nodes": [
        N("napoleon_marechaux", "元帥府", "The Marshalate",
          "Les marechaux — the marshals raised from the ranks to lead the corps.",
          "napoleon_lempereur", [("monthly_general_loyalty", 0.05), ("land_morale_modifier", 0.05)]),
        N("napoleon_ordre_mixte", "混合隊形", "The Ordre Mixte",
          "L'ordre mixte — the mix of line and column that gave both fire and shock.",
          "napoleon_manoeuvre", [("heavy_infantry_offensive", 0.1), ("discipline", 0.05)]),
        N("napoleon_tirailleurs", "散兵", "The Tirailleurs",
          "Les tirailleurs — the swarm of skirmishers that screened and galled the enemy.",
          "napoleon_bataillon_carre", [("archers_offensive", 0.1), ("light_infantry_hills_combat_bonus", 0.1)]),
        N("napoleon_horse_artillery", "騎砲兵", "Horse Artillery",
          "L'artillerie a cheval — the galloping guns that kept pace with the cavalry.",
          "napoleon_grande_batterie", [("artillery_offensive", 0.1), ("army_movement_speed", 0.05)]),
        N("napoleon_conscription", "徵兵制", "The Conscription",
          "La conscription — the levy of a whole nation that filled the ranks anew.",
          "napoleon_levee", [("global_manpower_modifier", 0.1), ("global_cohort_recruit_speed", 0.1)]),
        N("napoleon_bulletins", "戰報", "The Bulletins",
          "Les bulletins — the emperor's dispatches that made a legend of every field.",
          "napoleon_la_gloire", [("ruler_popularity_gain", 0.1), ("war_exhaustion", -0.02)]),
     ]},
]

NODEKEY_RE = re.compile(r'^\s*([a-z][a-z0-9_]+)\s*=\s*\{', re.M)
LOCKEY_RE  = re.compile(r'^\s*([A-Za-z0-9_]+):\d*\s+"', re.M)

# block keywords the NODEKEY_RE also matches (`modifier = {`, `requires = {`, ...) — filtered
# out so the key sets hold only tradition/node keys, not generic PDXScript block openers.
_KW = {"allow", "modifier", "ai_will_do", "trigger", "trigger_if", "trigger_else",
       "trigger_else_if", "limit", "custom_tooltip", "on_activate", "potential", "bonus",
       "add", "value", "OR", "AND", "NOT"}


def node_keys_in(text):
    return {k for k in NODEKEY_RE.findall(text) if k not in _KW}


def fmt_val(v):
    return str(v) if isinstance(v, int) else (f"{v:g}")


def node_block(n, ai):
    L = [f"\t{n.key} = {{"]
    L.append(f"\t\ticon = {n.key}")
    L.append(f"\t\trequires = {{ {n.req} }}")
    if ai:
        L.append(f"\t\tai_will_do = {{ modifier = {{ trigger = {{ {ai} }} add = {{ value = 4 }} }} }}")
    mods = "  ".join(f"{k} = {fmt_val(v)}" for k, v in n.mods)
    L.append(f"\t\tmodifier = {{ {mods} }}")
    L.append("\t}")
    return "\n".join(L) + "\n"


def all_node_keys():
    """Every tradition/node key across ALL military_traditions files (glob, not a fixed
    list — so a foreign node in any file is seen). Block keywords are excluded."""
    keys = set()
    for fp in glob.glob(os.path.join(MT, "*.txt")):
        keys.update(node_keys_in(open(fp, encoding="utf-8").read()))
    return keys


def splice_file(fname, per_tree):
    """Insert each tree's new node blocks before that tree's closing col-0 `}`."""
    fp = os.path.join(MT, fname)
    lines = open(fp, encoding="utf-8").readlines()
    out = []
    cur_tree = None
    tree_open_re = re.compile(r'^([a-z][a-z0-9_]+)\s*=\s*\{')
    for line in lines:
        m = tree_open_re.match(line)
        if m:
            cur_tree = m.group(1)
        if line.strip() == "}" and not line[:1].isspace() and cur_tree in per_tree and per_tree[cur_tree]:
            # closing brace of a tree we augment: emit new nodes first.
            out.append("\n")
            for blk in per_tree[cur_tree]:
                out.append(blk)
            per_tree[cur_tree] = []  # consumed
            cur_tree = None
        out.append(line)
    open(fp, "w", encoding="utf-8").writelines(out)


def keys_by_tree():
    """Map every existing node key -> the tree (col-0 opener) that owns it, across all
    military_traditions files. Lets us tell one of OUR own already-spliced nodes (present in
    exactly the tree our table assigns it to) apart from a FOREIGN node that merely shares a
    key (present in some other tree / file)."""
    owner = {}
    tree_open = re.compile(r'^([a-z][a-z0-9_]+)\s*=\s*\{')
    for fp in glob.glob(os.path.join(MT, "*.txt")):
        cur = None
        for line in open(fp, encoding="utf-8"):
            m = tree_open.match(line)
            if m:
                cur = m.group(1); continue
            km = NODEKEY_RE.match(line)
            if km and km.group(1) not in _KW and cur:
                owner.setdefault(km.group(1), cur)
    return owner


def main():
    check = "--check" in sys.argv
    owner = keys_by_tree()

    # collision guard + dupe guard.
    # A table key already present in the tree our table assigns it to = OUR own prior splice
    # (idempotent no-op, handled below). A table key present in ANY OTHER tree = a genuine
    # FOREIGN collision we must NOT clobber -> abort. (This is the check the earlier
    # `n.key not in own` form could never make, since every table key is in `own`.)
    seen, collide = {}, []
    for t in TREES:
        for n in t["nodes"]:
            if n.key in owner and owner[n.key] != t["tree"]:
                collide.append(f"{n.key}: FOREIGN node in tree '{owner[n.key]}' (table assigns it to '{t['tree']}')")
            if n.key in seen:
                collide.append(f"{n.key}: duplicated in content table ({seen[n.key]}, {t['tree']})")
            seen[n.key] = t["tree"]
    if collide:
        print("ABORT — collisions:")
        for c in collide:
            print("  " + c)
        sys.exit(1)

    # loc keys present
    loc_present = set(LOCKEY_RE.findall(open(LOC, encoding="utf-8-sig").read()))

    # group by file, skipping nodes already spliced (idempotent)
    by_file = {}
    loc_lines = []
    total = 0
    for t in TREES:
        fp = os.path.join(MT, t["file"])
        present = node_keys_in(open(fp, encoding="utf-8").read())
        blocks = []
        for n in t["nodes"]:
            if n.key in present:
                continue
            blocks.append(node_block(n, t["ai"]))
            if n.key not in loc_present:
                loc_lines.append(f' {n.key}:0 "{n.en} ({n.cjk})"\n')
            if (n.key + "_desc") not in loc_present:
                loc_lines.append(f' {n.key}_desc:0 "{n.desc}"\n')
            total += 1
        if blocks:
            by_file.setdefault(t["file"], {}).setdefault(t["tree"], []).extend(blocks)
        # nodes already IN this tree (owned by it) — the true "had" baseline.
        had = sum(1 for k, tree in owner.items() if tree == t["tree"])
        print(f"  {t['tree']:34s} +{len(blocks)} (tree already had {had})")

    print(f"{'PLAN' if check else 'DONE'}: {total} new traditions across {len(TREES)} trees")
    if check or total == 0:
        return

    for fname, per_tree in by_file.items():
        splice_file(fname, per_tree)
    if loc_lines:
        with open(LOC, "a", encoding="utf-8") as f:
            f.write("\n # [#129] breadth-expansion traditions\n")
            f.writelines(loc_lines)


if __name__ == "__main__":
    main()
