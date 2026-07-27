#!/usr/bin/env python3
"""qa_fixes_tradition2.py — definitive tradition-icon regen: aspect-correct crop (no more
stretching), a UNIQUE curated query per node (no dupes), covering all 5 tradition files
including the Japanese tree + the default_philosophy root. BGRA8 (traditions render it).
Overwrites <nodekey>.dds in place."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDIR = os.path.join(ROOT, "gfx", "interface", "icons", "military_traditions")
SRC  = os.path.join(ROOT, "art_src", "trad2")
LOG  = os.path.join(ROOT, "tools", "qa_fix_trad2_log.tsv")
DON  = sorted(glob.glob(os.path.join(TDIR, "arabic_*.dds")))[0]  # 198x72 BGRA8

# unique query per node — concept-specific, image-rich military subjects.
Q = {
 # --- Eight Banners (八旗) --- distinct banner/Manchu-soldier imagery, larger flags
 "qing_eight_banners_tradition":"Manchu Eight Banners bannerman armor portrait",
 "qing_banner_start":"Manchu bannerman warrior armor",
 "qing_banner_cavalry":"Manchu Qing cavalry horseman painting",
 "qing_banner_garrison":"Qing dynasty garrison soldiers Beijing photograph",
 "qing_banner_firearms":"Qing dynasty matchlock musketeer soldier",
 "qing_banner_capstone":"Qianlong Emperor in ceremonial armour horseback",
 "qing_banner_vanguard":"Qing dynasty vanguard soldier armor",
 "qing_banner_jianrui":"Qing dynasty elite storm troops scaling ladder painting",
 "qing_banner_bondservants":"Manchu Qing court official portrait",
 "qing_banner_niru":"Manchu banner officer portrait Qing",
 # --- Green Standard Army (綠營) --- Han infantry
 "qing_green_standard_tradition":"Green Standard Army Qing Han soldier",
 "qing_green_start":"Qing dynasty Han infantry soldier photograph",
 "qing_green_battalion":"Qing dynasty infantry battalion formation",
 "qing_green_garrison":"Qing dynasty provincial garrison fort",
 "qing_green_rattan":"rattan shield soldier Chinese",
 "qing_green_capstone":"Qing dynasty army review parade painting",
 "qing_green_drill":"Qing dynasty soldiers drilling muskets",
 "qing_green_patrol":"Qing dynasty soldiers marching patrol",
 "qing_green_marines":"Qing dynasty war junk marines river",
 "qing_green_guard":"Qing dynasty city gate guards",
 # --- Mongol Banner Cavalry (蒙古馬隊) ---
 "qing_mongol_cavalry_tradition":"Mongolian mounted archer cavalry painting",
 "qing_mongol_start":"Mongolian horseman steppe",
 "qing_mongol_raiders":"Mongolian mounted warriors charge",
 "qing_mongol_endurance":"Mongolian horsemen winter steppe",
 "qing_mongol_capstone":"Mongolian cavalry banner battle painting",
 "qing_mongol_league":"Mongolian nobles assembly banner",
 "qing_mongol_chahar":"Inner Mongolia Chahar horsemen",
 "qing_mongol_camels":"Bactrian camel corps caravan desert",
 "qing_mongol_hunt":"Qianlong imperial hunt Mulan painting",
 "qing_mongol_khalkha":"Khalkha Mongol horsemen Mongolia",
 # --- Frontier Defence (藩部邊防) ---
 "qing_frontier_defence_tradition":"Qing frontier fortress Xinjiang wall",
 "qing_frontier_start":"Jiayuguan fort Great Wall gate",
 "qing_frontier_colonies":"tuntian military farm colony China",
 "qing_frontier_highland":"Tibetan plateau fortress mountains",
 "qing_frontier_desert":"Taklamakan desert oasis fort Xinjiang",
 "qing_frontier_capstone":"Qing western regions map conquest",
 "qing_frontier_pickets":"watchtower beacon tower steppe frontier",
 "qing_frontier_rotation":"Qing dynasty soldiers marching column",
 "qing_frontier_native":"Qing frontier native auxiliary troops",
 "qing_frontier_supply":"camel supply caravan desert army",
 # --- Tributary Levy (朝貢徵調) ---
 "qing_tributary_levy_tradition":"Qing dynasty tribute mission envoys painting",
 "qing_tributary_start":"Qing dynasty foreign envoys court",
 "qing_tributary_auxiliaries":"Qing dynasty allied native soldiers",
 "qing_tributary_host":"Qing dynasty massed army painting",
 "qing_tributary_capstone":"万国来朝图 Qing tribute painting",
 "qing_tributary_investiture":"Qing dynasty investiture ceremony envoy",
 "qing_tributary_korea":"Joseon Korea royal court soldiers",
 "qing_tributary_tusi":"southwest China tusi chieftain painting",
 "qing_tributary_revenue":"Chinese silver ingot tribute gifts",
 "qing_tributary_mobilise":"Qing dynasty army mobilisation banners",
 # --- Ten Great Campaigns (十全武功 / manchu) ---
 "manchu_shiquan":"Qianlong Emperor ceremonial armour portrait",
 "shiquan_start":"Eight Banners Manchu army muster",
 "shiquan_dzungar_1":"Battle of Oroi-Jalatu Qianlong campaign engraving",
 "shiquan_dzungar_2":"Victory at Khorgos Qianlong battle copper print",
 "shiquan_altishahr":"Kashgar Altishahr oasis Qing conquest",
 "shiquan_jinchuan_1":"Jinchuan campaign mountain fortress Qing",
 "shiquan_jinchuan_2":"Jinchuan stone tower battle Sichuan",
 "shiquan_taiwan":"Qing dynasty Taiwan campaign Lin Shuangwen",
 "shiquan_burma":"Konbaung Burma war elephant army",
 "shiquan_vietnam":"Tay Son Vietnam warship battle",
 "shiquan_gurkha":"Gurkha Nepal soldiers Himalaya",
 "shiquan_laoren":"Qianlong Emperor old age portrait",
 # --- La Grande Armée (napoleon) ---
 "napoleon_grande_armee":"Napoleon Grande Armee soldiers painting",
 "napoleon_start":"Napoleon reviewing troops painting",
 "napoleon_jeune_garde":"Napoleon Young Guard infantry painting",
 "napoleon_vieille_garde":"Napoleon Old Guard grenadier painting",
 "napoleon_la_garde_meurt":"Old Guard last stand Waterloo painting",
 "napoleon_brienne":"military academy artillery cadet painting",
 "napoleon_grande_batterie":"Napoleonic massed artillery battery painting",
 "napoleon_dieu_de_la_guerre":"Napoleonic cannon bombardment painting",
 "napoleon_bataillon_carre":"French infantry square Napoleonic painting",
 "napoleon_manoeuvre":"Napoleon studying battle map painting",
 "napoleon_campagne_1805":"Battle of Austerlitz 1805 painting",
 "napoleon_levee":"levee en masse French Revolution recruits",
 "napoleon_baton":"French marshal baton dress uniform",
 "napoleon_la_gloire":"Napoleon coronation glory painting",
 "napoleon_lempereur":"Napoleon emperor portrait David",
 # --- Japanese traditions ---
 "japanese_philosophy_start_bonus":"samurai armor bushido painting",
 "japan_start":"samurai warrior armor Japan",
 "japanese_traditionalist_path_1":"Japanese feudal samurai castle",
 "japanese_traditionalist_path_2":"ashigaru foot soldiers Japan painting",
 "japanese_traditionalist_path_3":"samurai cavalry charge painting",
 "japanese_traditionalist_path_4":"Japanese matchlock teppo gunner",
 "japanese_traditionalist_path_6":"samurai sword duel painting",
 "japanese_traditionalist_path_7":"Japanese castle siege painting",
 "japanese_imperial_ambitions_path_1":"Meiji imperial Japanese army soldiers",
 "japanese_imperial_ambitions_path_2":"Meiji era Japanese infantry rifles",
 "japanese_imperial_ambitions_path_4":"Imperial Japanese Navy warship Meiji",
 "japanese_imperial_ambitions_path_5":"Meiji Japanese artillery soldiers",
 "japanese_imperial_ambitions_path_6":"Imperial Japanese Army cavalry Meiji",
 "japanese_imperial_ambitions_path_7":"Meiji Japan army parade flag",
 # --- default philosophy root ---
 "default_philosophy_start_bonus":"ancient soldiers spears shields battle relief",
}

def fallbacks(q):
    """Progressively simpler variants if the specific query returns nothing."""
    words=q.split()
    yield q
    if len(words)>3: yield " ".join(words[:3])
    if len(words)>2: yield " ".join(words[:2])

def main():
    with open(LOG,"w",encoding="utf-8") as log:
        log.write("key\tquery\tsource\tstatus\n")
        for key,q in Q.items():
            out=os.path.join(TDIR,key+".dds")
            src=os.path.join(SRC,key+".jpg"); os.makedirs(SRC,exist_ok=True)
            done=False
            for fq in fallbacks(q):
                try:
                    if os.path.exists(src): os.remove(src)
                    _,desc=fetch(("search",fq),src,width=400)
                    convert(src,out,like=DON)     # aspect-correct crop now
                    log.write(f"{key}\t{fq}\t{desc}\tOK\n"); print("OK",key,"" if fq==q else f"(fb:{fq})")
                    done=True; break
                except Exception as e:
                    last=str(e)[:50]
            if not done:
                log.write(f"{key}\t{q}\tERR\t{last}\n"); print("ERR",key,last)
    print("done ->",LOG,f"({len(Q)} nodes)")

if __name__=="__main__":
    main()
