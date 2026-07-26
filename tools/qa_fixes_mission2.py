#!/usr/bin/env python3
"""qa_fixes_mission2.py — second QA pass over mission icons flagged by the heuristic
detector (document-scans / flat blurs). Curated concept queries favouring a depictable
photographic/painted subject. Overwrites in place."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fetch_wm import fetch
from dds_icon import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MT = os.path.join(ROOT, "gfx", "interface", "icons", "mission_tasks")
DON = os.path.join(MT, "test1.dds")

FIX = {
 "qing_burma_capital":        "Mandalay royal palace Burma",
 "qing_burma_trade":          "Burmese ruby teak logging",
 "qing_col_taiwan":           "Taiwan Fort Zeelandia Tainan",
 "qing_con_parliament":       "parliament chamber interior hall",
 "qing_hs_capstone":          "Qing dynasty tribute envoys painting",
 "qing_hs_siam":              "Grand Palace Bangkok Thailand",
 "qing_india_calcutta":       "Fort William Calcutta 1828 painting",
 "qing_india_heartland":      "Ganges river Varanasi India",
 "qing_japan_mission":        "Meiji Japan warship navy",
 "qing_nanyang_kongsi":       "West Borneo Chinese kongsi Pontianak",
 "qing_settle_manchuria":     "Manchuria forest landscape",
 "qing_settle_mongol_govs":   "Mongolian steppe yurt landscape",
 "qing_sp_menagerie":         "imperial garden exotic animals zoo painting",
 "qing_treasure_capstone":    "Zheng He treasure ship junk",
 "qing_treasure_grand_shipyard":"Chinese junk shipyard drydock",
 "qing_treasure_mao_kun_chart":"Mao Kun map ancient Chinese navigation chart",
 "qing_treasure_myriad_court":"万国来朝图 Qing tribute painting",
 "qing_xj_begs":              "Uyghur Kashgar official portrait",
 "qing_xj_colonies":          "Xinjiang farmland oasis fields",
 "qing_con_abolish_exam":     "Chinese imperial examination hall cells",
 "qing_jp_alliance":          "Qing Japan diplomatic delegation photograph",
 "qing_hk_congregation":      "Taiping Christian worship China painting",
 "qing_hk_proclaim":          "Hong Xiuquan Taiping Heavenly King",
 # extra low-detail greyish ones worth improving
 "qing_central_asia_mission": "Tian Shan mountains Central Asia landscape",
 "qing_burma_yunnan":         "Yunnan mountains terraced landscape",
 "qing_settle_willow":        "Willow Palisade Manchuria frontier",
 "qing_ss_telegraph":         "19th century telegraph office operator",
}

def main():
    log = os.path.join(ROOT,"tools","qa_fix_mission2_log.tsv")
    with open(log,"w",encoding="utf-8") as f:
        f.write("key\tquery\tsource\tstatus\n")
        for key,q in FIX.items():
            out=os.path.join(MT,key+".dds")
            if not os.path.exists(out):
                f.write(f"{key}\t{q}\tmissing\t-\n"); continue
            src=os.path.join(ROOT,"art_src","qafixm2",key+".jpg")
            os.makedirs(os.path.dirname(src),exist_ok=True)
            try:
                if os.path.exists(src): os.remove(src)
                _,desc=fetch(("search",q),src,width=360)
                convert(src,out,like=DON)
                f.write(f"{key}\t{q}\t{desc}\tOK\n"); print("OK",key)
            except Exception as e:
                f.write(f"{key}\t{q}\tERR\t{e}\n"); print("ERR",key,str(e)[:60])
    print("done ->",log)

if __name__=="__main__":
    main()
