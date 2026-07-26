#!/usr/bin/env python3
"""qa_fixes_mission.py — curated re-fetch for mission-task icons flagged in visual QA
(text-page scans, flags, book covers, off-concept photos). Concept-appropriate queries
emphasising a concrete depictable subject. Overwrites the .dds in place (keys already wired)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "gfx", "interface", "icons", "mission_tasks")
DON  = os.path.join(OUT, "test1.dds")

FIX = {
 # burma / central asia
 "qing_burma_fever":       "tropical jungle mist mountains Burma",
 "qing_ca_ili_general":    "Qing dynasty general portrait armor",
 # colonization — Pacific-rim / protectorates: use concrete places
 "qing_col_alaska":        "Sitka Russian America fort Alaska",
 "qing_col_amur":          "Amur river China frontier",
 "qing_col_anbei":         "Mongolian steppe frontier",
 "qing_col_andong":        "Manchuria forest frontier",
 "qing_col_annan":         "Vietnam Hue imperial citadel",
 "qing_col_anxin":         "California Pacific coast landscape",
 "qing_col_anhai":         "Pacific ocean islands sea",
 "qing_col_anfei":         "African savanna coast",
 "qing_col_anxi":          "Xinjiang desert oasis Central Asia",
 "qing_col_california":    "California gold rush 19th century",
 "qing_col_zheng_he":      "Chinese treasure ship junk sailing",
 "qing_col_daoguang_doctrine":"Daoguang Emperor Qing portrait",
 # constitutional reform
 "qing_con_edict":         "Qing imperial edict scroll ceremony",
 "qing_con_legal_code":    "law book gavel justice",
 "qing_con_local_gov":     "Qing dynasty provincial official portrait",
 # taiping (heavenly kingdom)
 "qing_hk_land_system":    "Chinese rice paddy field farmers",
 "qing_hk_congregation":   "19th century Chinese Christian congregation",
 "qing_hk_new_admin":      "Taiping Heavenly Kingdom Nanjing",
 "qing_hk_proclaim":       "Hong Xiuquan Taiping leader",
 # himalaya / SE asia
 "qing_hs_burma":          "Konbaung Burma palace Mandalay",
 "qing_hs_tibet":          "Potala Palace Lhasa Tibet",
 "qing_hs_lifanyuan":      "Qing dynasty Mongolian tribute envoys",
 # japan
 "qing_jppre_cautionary_tale":"First Opium War naval battle China",
 "qing_jp_read_danger":    "Meiji Japan imperial army soldiers",
 "qing_openjapan_shogun":  "Edo castle Tokugawa shogun Japan",
 "qing_india_mission":     "British East India Company India",
 # nanyang / settle / xinjiang / treasure
 "qing_nanyang_lanfang":   "West Borneo Pontianak river",
 "qing_settle_migration":  "Chinese migrant farmers frontier settlement",
 "qing_settle_uriankhai":  "Mongolia Tuva steppe grassland",
 "qing_treasure_myriad_court":"Qing dynasty court tribute ceremony painting",
 "qing_xj_road":           "Silk Road desert caravan Xinjiang",
 "qing_xj_pacify":         "Kashgar oasis Xinjiang old city",
 "qing_xj_begs":           "Uyghur official Xinjiang portrait",
}

def main():
    log = os.path.join(ROOT,"tools","qa_fix_mission_log.tsv")
    with open(log,"w",encoding="utf-8") as f:
        f.write("key\tquery\tsource\tstatus\n")
        for key,q in FIX.items():
            out=os.path.join(OUT,key+".dds")
            if not os.path.exists(out):
                f.write(f"{key}\t{q}\tskip-missing\t-\n"); print("skip",key); continue
            src=os.path.join(ROOT,"art_src","qafixm",key+".jpg")
            os.makedirs(os.path.dirname(src),exist_ok=True)
            try:
                if os.path.exists(src): os.remove(src)
                _,desc=fetch(("search",q),src,width=360)
                convert(src,out,like=DON)
                f.write(f"{key}\t{q}\t{desc}\tOK\n"); print("OK",key)
            except Exception as e:
                f.write(f"{key}\t{q}\tERR\t{e}\n"); print("ERR",key,e)
    print("done ->",log)

if __name__=="__main__":
    main()
