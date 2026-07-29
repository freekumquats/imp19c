# -*- coding: utf-8 -*-
# [#125] Curated Wikimedia-Commons search queries, one per mission task.
#
# WHY: auto-derived queries (verb-stripped loc titles) pull MODERN photos for these abstract
# historical concepts (e.g. "Revive the Shipyards" -> a 21st-century container yard; "The Jade
# Cotton Trade" -> a 2011 photo). Generic full-text Commons search simply cannot select period
# artwork for abstract concepts. So every task gets a hand-written query aimed at period art —
# named Qing court paintings, the Qianlong "Ten Great Campaigns" battle copperplates, historical
# maps of the named place, specific historical events — and the fetch_wm._art_score ranker then
# prefers the most art-like candidate among the results.
#
# gen_mission_icons.py loads CONCEPT_QUERY from here (a task key present here overrides the
# loc-derived query entirely). Every entry was resolved against the live Commons API and the
# chosen file title logged to tools/mission_icon_log.tsv for audit.
CONCEPT_QUERY = {
    # ---- New Treasure Fleet (新寶船隊) — Zheng He / Ming maritime era ---------------------
    "qing_treasure_revive_yards":   "Ming dynasty hybrid junk ship",
    "qing_treasure_build_ports":    "Chinese harbour historical painting Qing",
    "qing_treasure_amass_fleet":    "Zheng He treasure ship voyages",
    "qing_treasure_grand_shipyard": "Chinese junk ship 1804 painting",
    "qing_treasure_mao_kun_chart":  "Mao Kun map",
    "qing_treasure_champa":         "Map Kingdom of Champa 1380",
    "qing_treasure_malacca":        "Malacca historical map 18th century",
    "qing_treasure_ceylon":         "Mannevillette map Trincomalee Ceylon 1775",
    "qing_treasure_calicut":        "Malabar coast historical map",
    "qing_treasure_hormuz":         "East Indies map Salmon 1766",
    "qing_treasure_aden":           "Aden historical map 18th century",
    "qing_treasure_malindi":        "Sultanate of Pate East Africa map",
    "qing_treasure_myriad_court":   "Wanguo Laichao",
    "qing_treasure_capstone":       "Zheng He voyages map",

    # ---- Invasion of Burma (平定緬甸) — Sino-Burmese War 1765-69, a Ten Great Campaign -----
    "qing_burma_mobilise":  "Qianlong campaign copperplate engraving battle",
    "qing_burma_frontier":  "Victory banquet Qianlong campaign painting",
    "qing_burma_mandalay":  "Ava Burmese kingdom historical",
    "qing_burma_capital":   "Konbaung dynasty court painting",
    "qing_burma_yunnan":    "Yunnan historical map 18th century",
    "qing_burma_shan":      "Shan states historical map",
    "qing_burma_tribute":   "Myanmar delegates Peking 1761",
    "qing_burma_trade":     "Konbaung dynasty painting",
    "qing_burma_fever":     "Qing dynasty medicine herbal illustration",
    "qing_burma_capstone":  "Victory banquet Qianlong campaign painting",

    # ---- Central Asia (西域) — Dzungar conquest, Altishahr, Ili -----------------------------
    "qing_ca_beyond_pass":  "Qing empire historical map 18th century",
    "qing_ca_kazakh":       "Zunghar Khanate emperor presented prisoners",
    "qing_ca_khanates":     "Kokand khanate historical",
    "qing_ca_ferghana":     "Central Asia historical map 19th century",
    "qing_ca_ili_general":  "Qing conquest Dzungaria copperplate",
    "qing_ca_begs":         "Military Governor Hami Xinjiang 1875",
    "qing_ca_tuntian":      "Qing dynasty farming painting",
    "qing_ca_silk_road":    "Bactrian camel Tang dynasty figure",
    "qing_ca_border":       "Qing dynasty stele historical",
    "qing_ca_capstone":     "Pacification of Dzungars copperplate engraving",

    # ---- Colonization (海洋開拓) — maritime empire, Great Game, New World -------------------
    "qing_col_bureau":       "Qing dynasty government office painting",
    "qing_col_taiwan":       "China historical map 18th century",
    "qing_col_amur":         "Amur river historical map",
    "qing_col_xinjiang":     "Pacification of Dzungars copperplate engraving",
    "qing_col_central_asia": "Central Asia historical map 19th century",
    "qing_col_alaska":       "Russian America Alaska historical painting",
    "qing_col_canada":       "Northwest coast historical map 18th century",
    "qing_col_california":   "California historical map 19th century",
    "qing_col_pacific_isles":"Pacific ocean historical map Ortelius",
    "qing_col_new_holland":  "New Holland Australia historical map",
    "qing_col_new_guinea":   "New Guinea historical map 18th century",
    "qing_col_daoguang_doctrine":"Daoguang Emperor portrait",
    "qing_col_anbei":        "Tang dynasty protectorate historical map",
    "qing_col_andong":       "Manchuria historical map 18th century",
    "qing_col_anxi":         "Western Regions historical map Tang",
    "qing_col_annan":        "Annam Vietnam historical map 18th century",
    "qing_col_anhai":        "South China Sea historical map",
    "qing_col_anxin":        "Pacific ocean historical map 18th century",
    "qing_col_lanfang":      "Borneo historical map 18th century",
    "qing_col_zheng_he":     "Zheng He treasure ship voyages",
    "qing_col_cape":         "Cape of Good Hope historical map",
    "qing_col_suez":         "Suez isthmus historical map 19th century",
    "qing_col_congo":        "Congo river historical map 19th century",
    "qing_col_anfei":        "Africa historical map 18th century",
    "qing_col_galleon":      "Manila galleon",
    "qing_col_veracruz":     "Mexico historical map 18th century",
    "qing_col_maximilian":   "Second Mexican Empire Maximilian painting",
    "qing_col_mexican_empire":"Flag map First Mexican Empire",
    "qing_col_capstone":     "Pacific ocean historical map Ortelius",

    # ---- Himalaya & Southeast Asia (南天) — tributary sphere -------------------------------
    "qing_hs_lifanyuan":    "Qing dynasty court tribute painting",
    "qing_hs_tibet":        "Potala Palace Lhasa historical painting",
    "qing_hs_nepal":        "Nepal kingdom historical map",
    "qing_hs_himalaya_ring":"Sikkim Bhutan historical map 19th century",
    "qing_hs_vietnam":      "Nguyen dynasty Vietnam painting",
    "qing_hs_indochina":    "Cambodia Laos historical map 19th century",
    "qing_hs_burma":        "Konbaung dynasty court painting",
    "qing_hs_siam":         "Siam Rattanakosin court painting",
    "qing_hs_maritime":     "South China Sea historical map",
    "qing_hs_coastal":      "Qing dynasty coastal defence map",
    "qing_hs_capstone":     "Wanguo Laichao",

    # ---- India (南征印度) — alt-history descent on Hindustan -------------------------------
    "qing_india_descent":   "Mughal army battle miniature painting",
    "qing_india_nawab":     "Nawab of Bengal miniature painting",
    "qing_india_calcutta":  "Calcutta historical view 18th century",
    "qing_india_mughal":    "Mughal emperor durbar miniature painting",
    "qing_india_heartland": "Ganges river historical painting 18th century",
    "qing_india_capstone":  "Battle of Plassey painting",
    "qing_india_maratha":   "Maratha court miniature painting",
    "qing_india_sikh":      "Sikh empire Ranjit Singh painting",
    "qing_india_trade":     "East India Company trade historical painting",
    "qing_india_himalaya_road":"Himalaya mountains historical",

    # ---- Meiji Japan diplomacy (東亞) -----------------------------------------------------
    "qing_jp_open_relations":"Meiji treaty signing woodblock print",
    "qing_jp_treaty_amity": "Meiji treaty signing woodblock print",
    "qing_jp_shared_learning":"Meiji era students woodblock print",
    "qing_jp_ryukyu_accord":"Ryukyu kingdom historical painting",
    "qing_jp_alliance":     "Meiji emperor woodblock print",
    "qing_jp_read_danger":  "Meiji Japan navy woodblock print",
    "qing_jp_ready_coast":  "Qing dynasty coastal defence map",
    "qing_jp_korea_shield": "Joseon Korea court painting",
    "qing_jp_triumph":      "First Sino-Japanese War woodblock print",

    # ---- Pre-Perry Japan (鎖国) -----------------------------------------------------------
    "qing_jppre_nagasaki_channel":"Nagasaki Dejima historical painting",
    "qing_jppre_fusetsugaki":"Edo period document scroll",
    "qing_jppre_cautionary_tale":"Opium War painting",
    "qing_jppre_back_daimyo":"Daimyo procession woodblock print",
    "qing_jppre_fan_sonno_joi":"samurai woodblock print",
    "qing_jppre_restoration":"Meiji Restoration woodblock print",
    "qing_jppre_shore_bakufu":"Tokugawa shogunate castle woodblock print",
    "qing_jppre_ready_bakufu":"Perry Black Ships woodblock print",
    "qing_jppre_meet_perry":"Perry Black Ships woodblock print",

    # ---- Nanyang / South Seas (南洋) ------------------------------------------------------
    "qing_nanyang_champion":"Chinese junk painting",
    "qing_nanyang_lanfang": "Borneo historical map 18th century",
    "qing_nanyang_borneo":  "Borneo historical map 18th century",
    "qing_nanyang_sulu":    "Sulu sultanate historical",
    "qing_nanyang_severed": "Dutch East Indies historical painting",
    "qing_nanyang_capstone":"South China Sea historical map",
    "qing_nanyang_kongsi":  "Borneo historical map 18th century",
    "qing_nanyang_java":    "Java Dutch East Indies historical painting",
    "qing_nanyang_straits": "Strait of Malacca historical map",
    "qing_nanyang_diaspora":"Chinese junk ship painting",

    # ---- Open Japan (開國) — the Treasure Fleet reaches Japan ------------------------------
    "qing_openjapan_arrive":"Chinese junk fleet painting",
    "qing_openjapan_kyushu":"Kyushu Japan historical map",
    "qing_openjapan_edo":   "Edo castle historical woodblock print",
    "qing_openjapan_ainu":  "Ainu people historical",
    "qing_openjapan_ezo":   "Ezo Hokkaido old map",
    "qing_openjapan_capstone":"Yokohama harbour woodblock print",
    "qing_openjapan_nagasaki":"Nagasaki Dejima historical",
    "qing_openjapan_shogun":"Tokugawa shogun procession woodblock print",
    "qing_openjapan_ryukyu":"Ryukyu kingdom historical painting",
    "qing_openjapan_treaty_ports":"Treaty port China historical painting",

    # ---- Constitutional Reform (預備立憲) — late Qing ------------------------------------
    "qing_con_bureau":      "Qing dynasty translation bureau",
    "qing_con_assemblies":  "Qing dynasty imperial edict document",
    "qing_con_mission_abroad":"Qing dynasty diplomats portrait",
    "qing_con_draft":       "Qing dynasty imperial edict document",
    "qing_con_edict":       "Qing dynasty imperial edict document",
    "qing_con_abolish_exam":"Imperial examination hall Qing painting",
    "qing_con_new_army":    "Late Qing New Army photograph",
    "qing_con_local_gov":   "Qing dynasty yamen painting",
    "qing_con_legal_code":  "Qing dynasty law code document",
    "qing_con_parliament":  "Eighteen Scholars Ming painting",

    # ---- Self-Strengthening (自強) — the 1860s-90s modernisation ------------------------
    "qing_ss_zongli":       "Zongli Yamen historical photograph",
    "qing_ss_jiangnan":     "Kiangnan Arsenal",
    "qing_ss_fuzhou":       "Foochow Arsenal historical",
    "qing_ss_tongwen":      "Tongwen Guan",
    "qing_ss_peiyang_university":"Peiyang University historical photograph",
    "qing_ss_peking_university":"Imperial University of Peking 1900",
    "qing_ss_merchant":     "China Merchants Steam Navigation historical",
    "qing_ss_rail":         "Qing dynasty railway historical photograph",
    "qing_ss_telegraph":    "Great Northern Telegraph China historical",
    "qing_ss_ever_victorious":"Ever Victorious Army",
    "qing_ss_beiyang":      "Dingyuan Chinese battleship",
    "qing_ss_nanyang":      "Chinese cruiser 1880s",
    "qing_ss_fujian":       "Chinese warship 1884",
    "qing_ss_guangdong":    "Qing dynasty warship historical photograph",
    "qing_ss_beiyang_army": "Beiyang Army historical photograph",
    "qing_ss_nanyang_army": "Late Qing soldiers photograph",
    "qing_ss_capstone":     "Chinese ironclad warship",

    # ---- Settle the Frontier (定牧墾邊) — Mongolia/Manchuria colonisation ----------------
    "qing_settle_policy":   "Qing dynasty frontier map 18th century",
    "qing_settle_mongolia": "Mongolia historical map 18th century",
    "qing_settle_manchuria":"Manchuria historical map 18th century",
    "qing_settle_mongol_govs":"Qing dynasty administrative map Mongolia",
    "qing_settle_willow":   "Willow Palisade Manchuria historical map",
    "qing_settle_uriankhai":"Tannu Uriankhai map",
    "qing_settle_migration":"Qing dynasty agricultural scene painting",
    "qing_settle_garrison": "Manchu bannerman painting",
    "qing_settle_forge":    "Manchu horsemen painting",
    "qing_settle_capstone": "Qing empire historical map 18th century",

    # ---- Summer Palace (圓明園) ----------------------------------------------------------
    "qing_sp_yuanmingyuan": "Old Summer Palace Yuanmingyuan engraving",
    "qing_sp_european_pavilions":"Xiyang Lou European palaces Yuanmingyuan engraving",
    "qing_sp_siku_library": "Siku Quanshu manuscript Qing",
    "qing_sp_qingyi":       "Kunming Lake Summer Palace painting",
    "qing_sp_tongzhi_restoration":"Tongzhi Emperor portrait",
    "qing_sp_yiheyuan":     "Summer Palace Kunming Lake painting",
    "qing_sp_fountains":    "Xiyang Lou Yuanmingyuan engraving",
    "qing_sp_porcelain_tower":"Porcelain Tower Nanjing engraving",
    "qing_sp_theatre":      "Qing dynasty opera painting",
    "qing_sp_menagerie":    "Qing dynasty animals painting Giuseppe Castiglione",

    # ---- Taiping Heavenly Kingdom (太平天國) --------------------------------------------
    "qing_hk_channel":      "Taiping Heavenly Kingdom historical",
    "qing_hk_western_backing":"Ever Victorious Army",
    "qing_hk_doctrine":     "Taiping Heavenly Kingdom document",
    "qing_hk_heavenly_capital":"Nanjing Taiping historical painting",
    "qing_hk_congregation": "Taiping Heavenly Kingdom historical",
    "qing_hk_uprising":     "Jintian uprising Taiping historical",
    "qing_hk_land_system":  "Taiping Heavenly Kingdom document",
    "qing_hk_northern_expedition":"Qing ambush Taiping Army Wangjiakou 1854",
    "qing_hk_new_admin":    "Taiping Heavenly Kingdom historical",
    "qing_hk_proclaim":     "Taiping Heavenly Kingdom Hong Xiuquan",

    # ---- Xinjiang settlement (新疆善後) --------------------------------------------------
    "qing_xj_governorship": "Qing conquest Dzungaria copperplate",
    "qing_xj_fortify":      "Qing empire historical map Xinjiang",
    "qing_xj_colonies":     "Qing dynasty farming painting",
    "qing_xj_governor":     "Qing dynasty official portrait Xinjiang",
    "qing_xj_pacify":       "Pacification of Dzungars copperplate engraving",
    "qing_xj_integrate":    "Qing empire historical map Xinjiang",
    "qing_xj_karez":        "Turpan karez irrigation",
    "qing_xj_jade":         "Chinese jade carving Qing museum",
    "qing_xj_begs":         "Kashgar Uyghur historical",
    "qing_xj_road":         "Bactrian camel Tang dynasty figure",
}
