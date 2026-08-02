# Placeholder Icons — imp19c fork

Every icon/sprite below is a **placeholder** used by code added in this fork relative to the
sobisonator upstream (`git diff sobiso/master...HEAD`, merge-base `8b2043a0f`). Each reuses a
stock/borrowed `.dds` standing in for bespoke art that does not yet exist in `gfx/`. This doc
catalogues them by category, names the concept each is meant to depict, and — where found — links
a representative public-domain / freely-licensed image (mostly Wikimedia Commons) that an artist
could use as a reference when producing the real sprite.

> **Image-link column:** these are *reference images of the concept*, not game-ready sprites. Prefer
> the Wikimedia Commons file page (which states the licence); the linked file is the underlying
> jpg/png. Verify licence before any redistribution.

---

## 1. Mission-tree task icons

All mission task icons resolve to the stock sprites `test1` / `test2` / `test3` with header
`mission_image_test` (generic test art). Concepts inferred from each task's localized name. Bespoke
mission art is not yet in `gfx/`.

> **STATUS 2026-07-25 — every Qing mission tree was expanded to ≥10 tasks** (user directive
> "all mission trees should have at least 10 items"). Current task counts (2-tab `icon =` per tree):
> burma_war 10, central_asia 10, colonization 29, himalaya_seasia 11, india 10, japan 9, japan_preperry 9,
> nanyang 10, open_japan 10, reform 10, selfstrengthening 15, settle_frontier 10, summer_palace 10,
> taiping 10, treasure_fleet 14, xinjiang 10. The tables below list the ORIGINAL core tasks with
> researched reference images; the tasks added in the 2026-07-25 expansion reuse the same
> `test1/2/3` placeholder convention (no new icon concepts — each new task's art need is covered by
> the borrow-a-sibling-and-produce-real-art pipeline in §"Producing real .dds icons" below). japan /
> japan_preperry sit at 9 (their capstone is the 10th, non-`icon` task node).

### Self-Strengthening — `qing_selfstrengthening_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_ss_zongli | test1 | Zongli Yamen, foreign-affairs office (總理衙門) | [ref](https://upload.wikimedia.org/wikipedia/commons/7/7e/Four_Members_of_the_Tsung-li_Yam%C3%AAn.jpg) — members of the Zongli Yamen 總理衙門 |
| qing_ss_jiangnan | test2 | Jiangnan Arsenal, arms works (江南製造總局) | [ref](https://commons.wikimedia.org/wiki/Category:Jiangnan_Arsenal) — the Jiangnan Arsenal, Shanghai |
| qing_ss_fuzhou | test2 | Fuzhou Navy Yard / shipbuilding (福州船政局) | [ref](https://en.wikipedia.org/wiki/Foochow_Arsenal) — the Foochow (Fuzhou) Navy Yard (article) |
| qing_ss_tongwen | test3 | Tongwen Guan foreign-language college (同文館) | [ref](https://en.wikipedia.org/wiki/Tongwen_Guan) — the Tongwen Guan 同文館 (article) |
| qing_ss_peiyang_university | test3 | Peiyang University (北洋大學堂) | [ref](https://en.wikipedia.org/wiki/Tianjin_University) — Peiyang University 北洋大學堂 (article) |
| qing_ss_peking_university | test3 | Imperial University of Peking (京師大學堂) | [ref](https://en.wikipedia.org/wiki/Guozijian_(Beijing)) — the Imperial University of Peking 京師大學堂 (article) |
| qing_ss_merchant | test1 | China Merchants Steamship Co. (輪船招商局) | [ref](https://commons.wikimedia.org/wiki/File:Headquarters_of_China_Merchants_Steam_Navigation_Company_in_1901.jpg) — China Merchants Steam Nav. Co. |
| qing_ss_rail | test1 | railways and ironworks (鐵路與鐵廠) | [ref](https://en.wikipedia.org/wiki/Woosung_Railway) — the Woosung Railway, early Qing rail (article) |
| qing_ss_telegraph | test1 | national telegraph lines (電報總局) | [ref](https://commons.wikimedia.org/wiki/Category:Telegraphy) — a 19thC telegraph line/office |
| qing_ss_ever_victorious | test2 | Ever-Victorious Army (常勝軍) | [ref](https://en.wikipedia.org/wiki/Ever_Victorious_Army) — the Ever-Victorious Army (article) |
| qing_ss_beiyang | test2 | Beiyang Fleet (北洋水師) | [ref](https://commons.wikimedia.org/wiki/File:ChineseIroncladZhenyuan.jpg) — Beiyang Fleet ironclad Zhenyuan |
| qing_ss_nanyang | test2 | Nanyang Fleet (南洋水師) | [ref](https://en.wikipedia.org/wiki/Nanyang_Fleet) — the Qing Nanyang Fleet (article) |
| qing_ss_fujian | test2 | Fujian Fleet (福建水師) | [ref](https://en.wikipedia.org/wiki/Fujian_Fleet) — the Qing Fujian Fleet (article) |
| qing_ss_guangdong | test2 | Guangdong Fleet (廣東水師) | [ref](https://en.wikipedia.org/wiki/Guangdong_Fleet) — the Qing Guangdong Fleet (article) |
| qing_ss_capstone | test1 | culmination of Self-Strengthening (自強大成) | [ref](https://en.wikipedia.org/wiki/Self-Strengthening_Movement) — the Self-Strengthening Movement (article) |

### Constitutional Reform — `qing_reform_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_con_bureau | test1 | Bureau for Foreign Law / translation office (譯書局) | [ref](https://en.wikipedia.org/wiki/Jiangnan_Arsenal) — late-Qing translation bureau 譯書局 (Jiangnan translation dept, article) |
| qing_con_assemblies | test2 | provincial deliberative assemblies (諮議局) | [ref](https://en.wikipedia.org/wiki/Provincial_Assembly_(late_Qing)) — a late-Qing provincial assembly 諮議局 (article) |
| qing_con_mission_abroad | test3 | Five Ministers' constitutional study mission abroad (五大臣出洋) | [ref](https://en.wikipedia.org/wiki/Reform_movement_(Qing_dynasty)) — Qing 1905 five-ministers constitutional mission (article) |
| qing_con_draft | test3 | Draft Constitution (欽定憲法大綱) | [ref](https://en.wikipedia.org/wiki/Constitutional_Outline_by_Imperial_Order) — 1908 draft constitution 欽定憲法大綱 (article) |
| qing_con_parliament | test1 | National Parliament / legislature (國會) | [ref](https://commons.wikimedia.org/wiki/Category:Parliament_buildings) — a national parliament chamber |

### Burma War — `qing_burma_war_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_burma_mobilise | test1 | mobilizing Yunnan frontier defenses (雲南備邊) | [ref](https://commons.wikimedia.org/wiki/Category:Yunnan) — the Yunnan frontier |
| qing_burma_frontier | test2 | crossing the Burma frontier pass (度緬關) | [ref](https://en.wikipedia.org/wiki/Sino-Burmese_War_(1765%E2%80%931769)) — Yunnan-Burma frontier war (article) |
| qing_burma_mandalay | test3 | march on Ava / Mandalay (取阿瓦) | [ref](https://commons.wikimedia.org/wiki/File:Ava_Palace.jpg) — Ava / Inwa royal palace, Burma |
| qing_burma_capital | test3 | fall of the Burmese capital (下緬京) | [ref](https://commons.wikimedia.org/wiki/File:Mandalay_Palace.jpg) — Mandalay royal palace |
| qing_burma_capstone | test1 | pacification of Burma (平定緬甸) | [ref](https://commons.wikimedia.org/wiki/Category:Konbaung_dynasty) — the Konbaung dynasty of Burma |

### Central Asia — `qing_central_asia_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_ca_beyond_pass | test1 | road beyond the pass, into Central Asia (出關) | [ref](https://en.wikipedia.org/wiki/Yumen_Pass) — the Jade Gate / Yumen Pass (article) |
| qing_ca_kazakh | test2 | Kazakh steppe (撫哈薩克) | [ref](https://en.wikipedia.org/wiki/Kazakh_Steppe) — the Kazakh steppe (article) |
| qing_ca_khanates | test2 | caravan cities / cowing Kokand (懾服浩罕) | [ref](https://commons.wikimedia.org/wiki/Category:Khanate_of_Kokand) — the Khanate of Kokand |
| qing_ca_ferghana | test3 | Ferghana Valley (據費爾干納) | [ref](https://commons.wikimedia.org/wiki/Category:Fergana_Valley) — the Ferghana Valley |
| qing_ca_capstone | test1 | Western Regions pacified (西域大定) | [ref](https://en.wikipedia.org/wiki/Western_Regions) — the Western Regions 西域 (article) |

### Himalaya & Southeast Asia — `qing_himalaya_seasia_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_hs_lifanyuan | test1 | Lifan Yuan / Court of Colonial Affairs (理藩院) | [ref](https://en.wikipedia.org/wiki/Lifan_Yuan) — the Lifan Yuan 理藩院 (article) |
| qing_hs_tibet | test2 | Amban protectorate over Tibet (駐藏大臣) | [ref](https://upload.wikimedia.org/wikipedia/commons/c/c0/Lhasa%2C_Amban%27s_Yamen_from_Southeast.jpg) — the Amban's Yamen, Lhasa 駐藏大臣 |
| qing_hs_nepal | test3 | restored Gurkha/Nepal tribute (廓爾喀) | [ref](https://commons.wikimedia.org/wiki/Category:Gurkha) — a Gurkha soldier of Nepal |
| qing_hs_himalaya_ring | test2 | Sikkim, Bhutan, Ladakh (錫金・不丹・拉達克) | [ref](https://commons.wikimedia.org/wiki/Category:Rumtek_Monastery) — a Himalayan kingdom monastery (Sikkim/Bhutan/Ladakh) |
| qing_hs_vietnam | test3 | deepened Vietnamese tribute (越南) | [ref](https://commons.wikimedia.org/wiki/Category:Imperial_City,_Hu%E1%BA%BF) — the Nguyen dynasty / Hue citadel |
| qing_hs_indochina | test2 | Indochina sphere — Cambodia, Laos (柬埔寨・寮國) | [ref](https://commons.wikimedia.org/wiki/Category:Angkor_Wat) — Angkor Wat / mainland SE Asia |
| qing_hs_burma | test3 | Konbaung (Burma) reckoning (緬甸) | [ref](https://commons.wikimedia.org/wiki/Category:Konbaung_dynasty) — the Konbaung dynasty of Burma |
| qing_hs_siam | test2 | Siamese pivot (暹羅) | [ref](https://en.wikipedia.org/wiki/Rattanakosin_Kingdom_(1782%E2%80%931932)) — Rattanakosin-era Siam (article) |
| qing_hs_capstone | test1 | Southern Dominion restored (南天一統) | [ref](https://en.wikipedia.org/wiki/Tributary_system_of_China) — the Chinese tributary system (article) |

### India — `qing_india_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_india_descent | test1 | descent on Hindustan / invasion of India (南征印度) | [ref](https://commons.wikimedia.org/wiki/Category:Khyber_Pass) — the Khyber Pass |
| qing_india_nawab | test2 | backing the Nawab of Bengal (撫孟加拉) | [ref](https://commons.wikimedia.org/wiki/Category:Nawabs_of_Bengal) — the Nawab of Bengal |
| qing_india_calcutta | test3 | fall of Calcutta (克加爾各答) | [ref](https://commons.wikimedia.org/wiki/File:Fort_William_Calcutta_1828.jpg) — Fort William, Calcutta |
| qing_india_mughal | test2 | Mughal emperor restored (復蒙兀兒) | [ref](https://commons.wikimedia.org/wiki/Category:Bahadur_Shah_II) — late Mughal emperor (Bahadur Shah II) |
| qing_india_heartland | test3 | Gangetic heartland (據恆河) | [ref](https://commons.wikimedia.org/wiki/File:Ganges_River_at_Varanasi.jpg) — the Ganges River |
| qing_india_capstone | test1 | East India Company expelled (逐夷復印) | [ref](https://commons.wikimedia.org/wiki/Category:British_East_India_Company) — British East India Company |

### Japan (collision) — `qing_japan_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_jp_open_relations | test1 | envoy to Japan (遣使日本) | [ref](https://commons.wikimedia.org/wiki/Category:Relations_of_Japan_and_the_Qing_dynasty) — Qing-Japan diplomatic relations |
| qing_jp_treaty_amity | test2 | Sino-Japanese Treaty of Amity (修好條規) | [ref](https://commons.wikimedia.org/wiki/File:Sino_Japanese_Friendship_and_Trade_Treaty_13_September_1871.jpg) — 1871 Sino-Japanese treaty |
| qing_jp_shared_learning | test3 | exchange students / shared arsenals (留學生) | [ref](https://commons.wikimedia.org/wiki/Category:Chinese_Educational_Mission) — Chinese Educational Mission students |
| qing_jp_ryukyu_accord | test2 | Ryukyu question / island partition (琉球分島) | [ref](https://commons.wikimedia.org/wiki/Category:Shuri_Castle) — the Ryukyu Kingdom / Shuri Castle |
| qing_jp_alliance | test1 | East Asian alliance (東亞同盟) | [ref](https://en.wikipedia.org/wiki/Pan-Asianism) — pan-Asian / East-Asian alliance (article) |
| qing_jp_read_danger | test2 | reading the eastern (Japanese) danger (東洋之患) | [ref](https://commons.wikimedia.org/wiki/Category:Imperial_Japanese_Army) — the early Meiji Imperial Japanese Army |
| qing_jp_ready_coast | test3 | coastal defense (海防) | [ref](https://en.wikipedia.org/wiki/Dagu_Forts) — Qing coastal defense fort (Dagu Forts) |
| qing_jp_korea_shield | test2 | holding the Korean shield (朝鮮) | [ref](https://commons.wikimedia.org/wiki/Category:Joseon) — Joseon-dynasty Korea |
| qing_jp_triumph | test1 | victory in the collision (甲午雪恥) | [ref](https://commons.wikimedia.org/wiki/Category:First_Sino-Japanese_War) — the First Sino-Japanese War |

### Japan (pre-Perry) — `qing_japan_preperry_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_jppre_nagasaki_channel | test1 | Nagasaki China-House trading channel (唐人屋敷) | [ref](https://upload.wikimedia.org/wikipedia/commons/5/50/Tojin-yashiki.jpg) — Tojin Yashiki, Nagasaki Chinese quarter |
| qing_jppre_fusetsugaki | test2 | Dutch/Chinese news-reports (風説書) | [ref](https://commons.wikimedia.org/wiki/File:DejimaInNagasakiBay.jpg) — Dejima / Nagasaki foreign trade (風説書 source) |
| qing_jppre_cautionary_tale | test3 | China's own experience as warning (前車之鑑) | [ref](https://commons.wikimedia.org/wiki/File:Destroying_Chinese_war_junks,_by_E._Duncan_(1843).jpg) — the First Opium War (Nemesis) |
| qing_jppre_back_daimyo | test2 | backing a tozama daimyo — Satsuma/Chōshū (薩長) | [ref](https://commons.wikimedia.org/wiki/Category:Bakumatsu) — a Satsuma daimyo / Bakumatsu samurai |
| qing_jppre_fan_sonno_joi | test3 | "revere the emperor, expel the barbarian" (尊王攘夷) | [ref](https://en.wikipedia.org/wiki/Sonn%C5%8D_j%C5%8Di) — Sonnō jōi movement 尊王攘夷 (article) |
| qing_jppre_restoration | test1 | Meiji Restoration (王政復古) | [ref](https://en.wikipedia.org/wiki/Meiji_Restoration) — the Meiji Restoration (article) |
| qing_jppre_shore_bakufu | test2 | shoring up the shogunate (佐幕) | [ref](https://commons.wikimedia.org/wiki/Category:Tokugawa_shogunate) — the Tokugawa shogunate / Edo Castle |
| qing_jppre_ready_bakufu | test3 | Bakufu coastal defense (海防) | [ref](https://en.wikipedia.org/wiki/Odaiba) — the Odaiba coastal batteries, Tokyo Bay (article) |
| qing_jppre_meet_perry | test1 | Black Ships / Perry (黒船来航) | [ref](https://commons.wikimedia.org/wiki/File:Black_Ships_by_Hibata_Osuke.jpg) — Perry's Black Ships 1853 |

### Nanyang (South Seas) — `qing_nanyang_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_nanyang_champion | test1 | championing the overseas Chinese (護僑南洋) | [ref](https://commons.wikimedia.org/wiki/Category:Overseas_Chinese) — overseas Chinese communities |
| qing_nanyang_lanfang | test2 | Lanfang Republic (固蘭芳) | [ref](https://en.wikipedia.org/wiki/Lanfang_Republic) — the Lanfang Republic (article) |
| qing_nanyang_borneo | test3 | West Borneo / Pontianak (據坤甸) | [ref](https://commons.wikimedia.org/wiki/Category:Pontianak,_Indonesia) — Pontianak, West Borneo |
| qing_nanyang_sulu | test2 | Sulu Sultanate (撫蘇祿) | [ref](https://commons.wikimedia.org/wiki/Category:Sultanate_of_Sulu) — the Sulu Sultanate |
| qing_nanyang_severed | test3 | striking a severed European colony (乘虛擊夷) | [ref](https://commons.wikimedia.org/wiki/Category:Batavia,_Dutch_East_Indies) — colonial Batavia, Dutch East Indies |
| qing_nanyang_capstone | test1 | mastery of the South Seas (南洋乘機) | [ref](https://commons.wikimedia.org/wiki/File:South_China_Sea.png) — the South China Sea (map) |

### Open Japan (treasure fleet) — `qing_open_japan_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_openjapan_arrive | test1 | treasure fleet arrives in Japan (寶船抵日) | [ref](https://upload.wikimedia.org/wikipedia/commons/c/c4/Zheng_He%27s_Treasure_Ship_3.jpg) — a Ming treasure ship (baochuan) |
| qing_openjapan_kyushu | test2 | southern gate / Kyushu landing (南路叩關) | [ref](https://commons.wikimedia.org/wiki/Category:Kyushu) — Kyushu island, Japan |
| qing_openjapan_edo | test3 | march on Edo (進逼江戶) | [ref](https://commons.wikimedia.org/wiki/Category:Edo_period_Tokyo) — Edo (Tokugawa Tokyo) |
| qing_openjapan_ainu | test2 | winning over the Ainu (撫蝦夷) | [ref](https://commons.wikimedia.org/wiki/File:Ainu_group.JPG) — Ainu people |
| qing_openjapan_ezo | test3 | holding Ezo/Hokkaido (據蝦夷地) | [ref](https://commons.wikimedia.org/wiki/Category:Landscapes_of_Hokkaido) — Hokkaido / Ezo landscape |
| qing_openjapan_capstone | test1 | Japan forced open (開國) | [ref](https://commons.wikimedia.org/wiki/File:Black_Ships_by_Hibata_Osuke.jpg) — Perry's Black Ships 1853 |

### Settle the Frontier — `qing_settle_frontier_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_settle_policy | test1 | frontier settlement policy (定邊策) | [ref](https://en.wikipedia.org/wiki/Tuntian) — tuntian military-agricultural colonies 屯田 (article) |
| qing_settle_mongolia | test2 | settling the Mongol lands (定漠北) | [ref](https://upload.wikimedia.org/wikipedia/commons/d/da/Mongolian_steppe.jpg) — Mongolian steppe |
| qing_settle_manchuria | test2 | populating the Manchurian homeland (實東北) | [ref](https://commons.wikimedia.org/wiki/Category:Landscapes_of_Manchuria) — Manchuria landscape |
| qing_settle_capstone | test1 | pastoral/agrarian colonization (定牧墾邊) | [ref](https://en.wikipedia.org/wiki/Willow_Palisade) — the Willow Palisade 柳條邊 (article) |

### Summer Palace — `qing_summer_palace_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_sp_yuanmingyuan | test1 | Yuanmingyuan / Old Summer Palace (圓明園) | [ref](https://upload.wikimedia.org/wikipedia/commons/1/13/Yuanmingyuan_Haiyantang_20130126.JPG) — Yuanmingyuan ruins (Haiyantang) |
| qing_sp_european_pavilions | test2 | Western/European Pavilions (西洋樓) | [ref](https://commons.wikimedia.org/wiki/Category:Xiyang_Lou) — the Xiyang Lou / European Palaces |
| qing_sp_siku_library | test3 | Siku Quanshu "Four Treasuries" library (四庫全書) | [ref](https://en.wikipedia.org/wiki/Siku_Quanshu) — the Siku Quanshu 四庫全書 (article) |
| qing_sp_qingyi | test2 | Qingyi Yuan garden (清漪園) | [ref](https://commons.wikimedia.org/wiki/File:Kunming_Lake_(Summer_Palace,_Beijing)_in_summer.JPG) — Kunming Lake, Summer Palace |
| qing_sp_tongzhi_restoration | test1 | Tongzhi Restoration (同治中興) | [ref](https://upload.wikimedia.org/wikipedia/commons/e/ea/Tongzhi_Emperor_%28closeup%29.jpg) — the Tongzhi Emperor |
| qing_sp_yiheyuan | test1 | Yiheyuan / Summer Palace (頤和園) | [ref](https://commons.wikimedia.org/wiki/File:Summer_Palace%2C_Beijing%2C_China.jpg) — the Yiheyuan / Summer Palace 頤和園 |

### Heavenly Kingdom (Taiping) — `qing_taiping_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_hk_channel | test1 | God-Worshipping Society (拜上帝會) | [ref](https://commons.wikimedia.org/wiki/Category:Taiping_Rebellion) — the Taiping Heavenly Kingdom |
| qing_hk_western_backing | test2 | courting Western missionaries and arms | [ref](https://commons.wikimedia.org/wiki/Category:Christian_missionaries_in_China) — a 19thC missionary in China |
| qing_hk_doctrine | test3 | New Treatise on Administration (資政新篇) | [ref](https://en.wikipedia.org/wiki/The_New_Treatise_on_Administration) — Taiping 資政新篇 (article) |
| qing_hk_heavenly_capital | test3 | Heavenly Capital / Nanjing (天京) | [ref](https://commons.wikimedia.org/wiki/Category:City_walls_of_Nanjing) — Nanjing city walls |
| qing_hk_proclaim | test1 | Heavenly Kingdom proclaimed (天國) | [ref](https://commons.wikimedia.org/wiki/Category:Hong_Xiuquan) — Hong Xiuquan, Taiping leader |

### Treasure Fleet — `qing_treasure_fleet_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_treasure_revive_yards | test1 | reviving the shipyards (振興船政) | [ref](https://commons.wikimedia.org/wiki/Category:Shipyards_established_in_the_19th_century) — a 19thC shipyard |
| qing_treasure_build_ports | test2 | great ports / drydocks (廣建船塢) | [ref](https://commons.wikimedia.org/wiki/Category:Dry_docks) — a shipbuilding drydock |
| qing_treasure_amass_fleet | test3 | amassing the fleet (聚舟師) | [ref](https://en.wikipedia.org/wiki/Chinese_Maritime_Customs_Service) — Qing war junk / fleet — cf. junk (article) |
| qing_treasure_capstone | test1 | voyage to the Western Ocean, Zheng He revival (下西洋) | [ref](https://commons.wikimedia.org/wiki/Category:Zheng_He) — Admiral Zheng He |

### Xinjiang — `qing_xinjiang_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_xj_governorship | test1 | Ili Governorship (伊犁將軍) | [ref](https://en.wikipedia.org/wiki/General_of_Ili) — the General of Ili 伊犁將軍 (article) |
| qing_xj_fortify | test2 | walls and checkpoints (築城設卡) | [ref](https://commons.wikimedia.org/wiki/Category:Forts_in_Xinjiang) — a Qing frontier fort in Xinjiang |
| qing_xj_colonies | test3 | military agricultural colonies (屯田實邊) | [ref](https://en.wikipedia.org/wiki/Tuntian) — tuntian military-agricultural colonies 屯田 (article) |
| qing_xj_governor | test1 | installing a capable governor (簡任能員) | [ref](https://upload.wikimedia.org/wikipedia/commons/f/fa/Zuo_Zongtang_1875.jpg) — Zuo Zongtang, reconquered Xinjiang |
| qing_xj_pacify | test2 | pacifying the Muslim oases (綏靖回疆) | [ref](https://commons.wikimedia.org/wiki/Category:Kashgar) — Kashgar, Tarim Basin oasis |
| qing_xj_integrate | test1 | Xinjiang integrated as a province (新疆一體) | [ref](https://upload.wikimedia.org/wikipedia/commons/7/71/Qing_dynasty_and_Xinjiang.jpg) — Qing Xinjiang province (map) |

### Colonization — `qing_colonization_missions.txt`
| Task | Placeholder | Concept | Reference image |
|---|---|---|---|
| qing_col_bureau | test1 | Maritime Affairs Bureau (海洋事務局) | [ref](https://en.wikipedia.org/wiki/Chinese_Maritime_Customs_Service) — a Qing maritime affairs office (article) |
| qing_col_taiwan | test3 | Taiwan into a province (臺灣建省) | [ref](https://commons.wikimedia.org/wiki/Category:Fort_Zeelandia_(Taiwan)) — Qing-era Taiwan / Fort Zeelandia |
| qing_col_amur | test2 | securing the Amur frontier (鞏固黑龍江) | [ref](https://commons.wikimedia.org/wiki/File:Amur_River.jpg) — Amur River |
| qing_col_xinjiang | test3 | consolidating the New Dominion (經營新疆) | [ref](https://upload.wikimedia.org/wikipedia/commons/7/71/Qing_dynasty_and_Xinjiang.jpg) — Qing Xinjiang province (map) |
| qing_col_central_asia | test3 | the Great Game in Central Asia (中亞大博弈) | [ref](https://en.wikipedia.org/wiki/The_Great_Game) — the Great Game (article) |
| qing_col_alaska | test2 | contesting Russian America / Alaska (爭奪阿拉斯加) | [ref](https://commons.wikimedia.org/wiki/Category:New_Archangel) — Russian America / Sitka |
| qing_col_canada | test2 | Northwest fur coast (西北毛皮海岸) | [ref](https://commons.wikimedia.org/wiki/File:Maritime_Fur_Trade-WorldContext.png) — Pacific maritime fur trade |
| qing_col_california | test3 | Californian "Golden Shore" (開拓金山) | [ref](https://commons.wikimedia.org/wiki/File:California_Gold_Rush_handbill.jpg) — California Gold Rush |
| qing_col_pacific_isles | test2 | Pacific island-hopping (太平洋群島) | [ref](https://commons.wikimedia.org/wiki/Category:Islands_of_the_Pacific_Ocean) — Pacific islands |
| qing_col_new_holland | test2 | New Holland / Australia (新荷蘭) | [ref](https://commons.wikimedia.org/wiki/File:Australia_1828_Tanner_map.jpg) — 1828 map of Australia |
| qing_col_new_guinea | test3 | Papuan coast (巴布亞) | [ref](https://commons.wikimedia.org/wiki/File:New_Guinea_(non-political).png) — the island of New Guinea |
| qing_col_daoguang_doctrine | test1 | "Daoguang Doctrine" (Monroe-style, 道光主義) | [ref](https://commons.wikimedia.org/wiki/Category:Daoguang_Emperor) — Daoguang Emperor |
| qing_col_anbei | test2 | Protectorate of the Pacified North (安北都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_andong | test2 | Protectorate of the Pacified East (安東都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_anxi | test3 | Protectorate of the Pacified West (安西都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_annan | test3 | Protectorate of the Pacified South (安南都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_anhai | test2 | Protectorate of the Pacified Seas (安海都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_anxin | test2 | Protectorate of the Pacified New World (安新都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_lanfang | test3 | Lanfang Republic recognized (蘭芳共和國) | [ref](https://en.wikipedia.org/wiki/Lanfang_Republic) — the Lanfang Republic (article) |
| qing_col_zheng_he | test2 | Zheng He treasure voyages revived (鄭和下西洋) | [ref](https://commons.wikimedia.org/wiki/Category:Zheng_He) — Admiral Zheng He |
| qing_col_cape | test2 | rounding the Cape of Good Hope (好望角) | [ref](https://commons.wikimedia.org/wiki/File:Cape_of_Good_Hope.jpg) — Cape of Good Hope |
| qing_col_suez | test3 | forcing the Suez passage (蘇伊士) | [ref](https://commons.wikimedia.org/wiki/Category:Suez_Canal) — the Suez Canal |
| qing_col_congo | test3 | carving the Congo interior (剛果) | [ref](https://commons.wikimedia.org/wiki/File:Congo_River_-_Kinshasa.jpg) — Congo River |
| qing_col_anfei | test2 | Protectorate of the Pacified Africa (安非都護府) | [ref](https://en.wikipedia.org/wiki/Protectorate_General_to_Pacify_the_West) — a Protectorate-to-Pacify frontier command 都護府 (article) |
| qing_col_galleon | test2 | Manila galleon "Silver Road" (馬尼拉大帆船) | [ref](https://en.wikipedia.org/wiki/Manila_galleon) — the Manila galleon (article) |
| qing_col_veracruz | test3 | landing at Veracruz (韋拉克魯斯) | [ref](https://commons.wikimedia.org/wiki/Category:Veracruz_(city)) — Veracruz, Mexico |
| qing_col_maximilian | test1 | Mexican Adventure (墨西哥帝業) | [ref](https://commons.wikimedia.org/wiki/Category:Maximilian_I_of_Mexico) — Emperor Maximilian I of Mexico |
| qing_col_mexican_empire | test1 | Empire of Mexico (墨西哥帝國) | [ref](https://commons.wikimedia.org/wiki/Category:Second_Mexican_Empire) — the Second Mexican Empire |
| qing_col_capstone | test1 | Pacific-rim empire (環太平洋大清) | [ref](https://commons.wikimedia.org/wiki/File:Pacific_Ocean_-_en.png) — the Pacific Ocean (map) |

---

## 2. New trade goods — `common/trade_goods/00_imp19c.txt`
Cash crops clone the tobacco cash-crop archetype `.dds`; porcelain/rifles clone silk/coal.

| Good | Concept | Borrows | Reference image |
|---|---|---|---|
| maize | maize / corn (New World crop) | tobacco archetype | [ref](https://commons.wikimedia.org/wiki/File:Corncobs.jpg) — maize / corn |
| sweet_potato | sweet potato | tobacco archetype | [ref](https://commons.wikimedia.org/wiki/File:Ipomoea_batatas_006.JPG) — sweet potatoes |
| potato | potato | tobacco archetype | [ref](https://commons.wikimedia.org/wiki/File:Patates.jpg) — potatoes |
| peanut | peanut / groundnut | tobacco archetype | [ref](https://commons.wikimedia.org/wiki/File:Peanut_9417.jpg) — peanuts / groundnuts |
| chili | chili pepper | tobacco archetype | [ref](https://commons.wikimedia.org/wiki/File:Chili_pepper_plant.jpg) — Chili pepper plant |
| porcelain | Jingdezhen blue-and-white porcelain (青花) | silk/coal | [ref](https://commons.wikimedia.org/wiki/Category:Blue_and_white_porcelain_of_China) — Jingdezhen blue-and-white porcelain |
| rifles | rifles (military commodity) | silk/coal | [ref](https://commons.wikimedia.org/wiki/Category:Percussion_muskets) — a 19thC military rifle |

---

## 3. New buildings — modifier-cost icons — `common/modifier_icons/00_modifier_icons.txt`
Each points at an existing vanilla building-cost `.dds`.

| Building modifier icon | Concept | Borrows | Reference image |
|---|---|---|---|
| qing_silk_filature_building_building_cost | silk filature (絲) | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Silk_reeling) — a silk filature / reeling |
| qing_porcelain_kiln_building_building_cost | porcelain kiln | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Jingdezhen_porcelain) — a Jingdezhen porcelain kiln |
| qing_tea_workshop_building_building_cost | tea workshop | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Tea_production_in_China) — a Chinese tea workshop |
| qing_cotton_workshop_building_building_cost | cotton workshop | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Cotton_mills) — a cotton textile mill |
| qing_salt_yard_building_building_cost | salt yard / works | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Salt_production_in_China) — a Chinese salt works |
| qing_customs_house_building_building_cost | maritime customs house (海關) | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Chinese_Maritime_Customs_Service) — Chinese maritime customs house 海關 |
| qing_yamen_building_building_cost | yamen / local government office (衙門) | population_building_cost.dds | [ref](https://upload.wikimedia.org/wikipedia/commons/4/4d/Yamen_of_Three_Counties%2C_Huanglongxi%2C_Sichuan.jpg) — a Chinese yamen 衙門 |
| qing_shuyuan_building_building_cost | shuyuan / academy (書院) | population_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Academies_(Shuyuan)) — a Chinese shuyuan / academy 書院 |
| qing_granary_building_building_cost | state granary (倉) | population_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Granaries_in_China) — a Chinese state granary |
| qing_selfstr_wonder_building_building_cost | Self-Strengthening wonder (arsenal/works) | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Jiangnan_Arsenal) — the Jiangnan Arsenal, Shanghai |
| qing_dike_building_building_cost | river dike / flood works (堤) | fortress_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Yellow_River) — a Yellow River dike / flood works |
| qing_canal_depot_building_building_cost | Grand Canal grain-transport depot (漕運) | commerce_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Grand_Canal_(China)) — the Grand Canal of China |
| qing_wall_section_building_building_cost | Great Wall / fortified wall section | fortress_building_cost.dds | [ref](https://commons.wikimedia.org/wiki/Category:Great_Wall_of_China) — the Great Wall of China |

---

## 3b. New buildings — BUILDING-TYPE queue icons — `gfx/interface/icons/buildings/<building_key>.dds`
[B21] A SEPARATE icon from the modifier-cost icon above: the engine renders the building-TYPE icon
in the Outliner "Building Constructions" queue + the macro-builder, resolved BY FILENAME from
`gfx/interface/icons/buildings/<building_key>.dds` (no `.gfx` registry entry — proven by the vanilla
"Added missing port building icon" commit).

> **STATUS 2026-07-25 — ALL 25 Qing buildings now HAVE a stopgap icon.** The 24 that were missing
> (blank in both the macro builder AND the province window — the reported "foreign buildings missing")
> were fixed by COPYING the borrow-icon in each row's "Borrow (stopgap)" column to
> `gfx/interface/icons/buildings/<key>.dds`. These are borrowed stock icons standing in for bespoke art —
> the DDS pipeline below is still how the REAL 書院/衙門/瓷窯 etc. art gets produced and dropped in.
> Caveat: most stock icons are 200×200 but `food_exchange_building.dds` (source for granary) is 100×100 —
> the engine scales it, but the granary icon is lower-res until real art replaces it. Also added this
> session (not in the table below, same copy-stopgap treatment): qing_embassy_building, qing_foreign_
> concession_building, qing_foreign_works_building, qing_frontier_colony_building, qing_frontier_fort_
> building, qing_mission_cathedral_building, qing_mission_public_building, qing_mission_underground_
> building, qing_treaty_port_building.

Original catalogue (the mapping used for the stopgap copies; all now DONE):

| Building type icon (file `<key>.dds`) | Concept | Borrow (stopgap) | Reference image |
|---|---|---|---|
| qing_shuyuan_building | shuyuan / academy (書院) — school | **DONE: EDU_school.dds** | classical academy |
| qing_yamen_building | yamen / local government office (衙門) | URB_administration_district.dds | [ref](https://upload.wikimedia.org/wikipedia/commons/4/4d/Yamen_of_Three_Counties%2C_Huanglongxi%2C_Sichuan.jpg) — a Chinese yamen 衙門 |
| qing_granary_building | state granary (倉) | food_exchange_building.dds | [ref](https://commons.wikimedia.org/wiki/Category:Granaries_in_China) — a Chinese state granary |
| qing_customs_house_building | maritime customs house (海關) | port_building.dds | [ref](https://commons.wikimedia.org/wiki/Category:Chinese_Maritime_Customs_Service) — maritime customs house 海關 |
| qing_silk_filature_building | silk filature (絲) | IND_industrial_estate.dds | [ref](https://commons.wikimedia.org/wiki/Category:Silk_reeling) — a silk filature / reeling |
| qing_porcelain_kiln_building | porcelain kiln (瓷) | IND_industrial_estate.dds | [ref](https://commons.wikimedia.org/wiki/Category:Jingdezhen_porcelain) — a Jingdezhen porcelain kiln |
| qing_tea_workshop_building | tea workshop (茶) | IND_resource_gathering_operation.dds | [ref](https://commons.wikimedia.org/wiki/Category:Tea_production_in_China) — a Chinese tea workshop |
| qing_cotton_workshop_building | cotton workshop (棉) | IND_industrial_estate.dds | [ref](https://commons.wikimedia.org/wiki/Category:Cotton_mills) — a cotton textile mill |
| qing_salt_yard_building | salt yard / works (鹽) | IND_resource_gathering_operation.dds | [ref](https://commons.wikimedia.org/wiki/Category:Salt_production_in_China) — a Chinese salt works |
| qing_opium_poppy_farm_building | opium poppy farm (罌粟) | IND_resource_gathering_operation.dds | [ref](https://commons.wikimedia.org/wiki/Category:Opium_poppy) — an opium poppy field |
| qing_selfstr_wonder_building | Self-Strengthening wonder (arsenal/works) | IND_industrial_estate.dds | [ref](https://commons.wikimedia.org/wiki/Category:Jiangnan_Arsenal) — the Jiangnan Arsenal, Shanghai |
| qing_dike_building | river dike / flood works (堤) | INF_canal.dds | [ref](https://commons.wikimedia.org/wiki/Category:Yellow_River) — a Yellow River dike |
| qing_grand_canal_building | Grand Canal (大運河) | INF_canal.dds | [ref](https://commons.wikimedia.org/wiki/Category:Grand_Canal_(China)) — the Grand Canal |
| qing_canal_depot_building | Grand Canal grain-transport depot (漕運) | INF_depot.dds | [ref](https://commons.wikimedia.org/wiki/Category:Grand_Canal_(China)) — the Grand Canal |
| qing_great_wall_building | Great Wall (長城) | fortress_building.dds | [ref](https://commons.wikimedia.org/wiki/Category:Great_Wall_of_China) — the Great Wall |
| qing_wall_section_building | fortified wall section | fortress_building.dds | [ref](https://commons.wikimedia.org/wiki/Category:Great_Wall_of_China) — the Great Wall |
| military_depot_building | military supply depot | INF_depot.dds | [ref](https://commons.wikimedia.org/wiki/Category:Military_logistics) — a military supply depot |
| row_manufactory_building | Rest-of-World manufactory | IND_industrial_estate.dds | [ref](https://commons.wikimedia.org/wiki/Category:Factories) — a manufactory / factory |
| row_plantation_building | Rest-of-World plantation | IND_resource_gathering_operation.dds | [ref](https://commons.wikimedia.org/wiki/Category:Plantations) — a plantation |

---

## 4. Military traditions
Both trees borrow shared arabic/indian tradition sprites; each slot flagged `# placeholder`.

### The Ten Great Campaigns (十全武功) — `common/military_traditions/00_manchu.txt`
| Slot | Concept | Borrows | Reference image |
|---|---|---|---|
| manchu_shiquan (tree) | the Ten Complete Victories reign | arabic_philosophy_start_bonus | [ref](https://commons.wikimedia.org/wiki/Category:Qianlong_Emperor) — the Qianlong Emperor |
| shiquan_start | Eight Banners manpower reserve | indian_philosophy_start_bonus | [ref](https://en.wikipedia.org/wiki/Eight_Banners) — the Manchu Eight Banners (article) |
| shiquan_dzungar_1 | First Dzungar Campaign 1755 | arabic_peninsula_path_1 | [ref](https://en.wikipedia.org/wiki/Dzungar%E2%80%93Qing_Wars) — Qing-Dzungar War (article) |
| shiquan_dzungar_2 | Second Dzungar Campaign 1757 | arabic_peninsula_path_5 | [ref](https://en.wikipedia.org/wiki/Dzungar%E2%80%93Qing_Wars) — Qing-Dzungar War (article) |
| shiquan_altishahr | Altishahr campaign 1759 | arabic_levantine_path_1 | [ref](https://commons.wikimedia.org/wiki/File:Kashgar-medressa-d04.jpg) — Kashgar / Altishahr oasis |
| shiquan_jinchuan_1 | First Jinchuan 1747-49 | arabic_levantine_path_4 | [ref](https://en.wikipedia.org/wiki/Jinchuan_campaigns) — the Jinchuan campaigns (article) |
| shiquan_jinchuan_2 | Second Jinchuan 1771-76 | arabic_african_path_5 | [ref](https://en.wikipedia.org/wiki/Jinchuan_campaigns) — the Jinchuan campaigns (article) |
| shiquan_taiwan | Taiwan / Lin Shuangwen 1787-88 | indian_northern_path_3 | [ref](https://commons.wikimedia.org/wiki/Category:Lin_Shuangwen_rebellion) — the Lin Shuangwen rebellion, Taiwan |
| shiquan_burma | Burma Campaign 1765-69 | indian_southern_path_1 | [ref](https://commons.wikimedia.org/wiki/Category:Konbaung_dynasty) — the Konbaung dynasty of Burma |
| shiquan_vietnam | Vietnam Campaign 1788-89 | indian_southern_path_7 | [ref](https://upload.wikimedia.org/wikipedia/commons/4/42/T%C3%A0u_chi%E1%BA%BFn_t%C3%A2y_S%C6%A1n.jpg) — Tây Sơn dynasty warship |
| shiquan_gurkha | Gurkha/Nepal campaigns 1788-92 | indian_western_path_2 | [ref](https://commons.wikimedia.org/wiki/Category:Gurkha) — a Gurkha soldier of Nepal |
| shiquan_laoren | "Old Man of the Ten Complete Victories" | arabic_philosophy_start_bonus | [ref](https://commons.wikimedia.org/wiki/Category:Qianlong_Emperor) — the Qianlong Emperor |

### La Grande Armée — `common/military_traditions/00_napoleon.txt`
| Slot | Concept | Borrows | Reference image |
|---|---|---|---|
| napoleon_grande_armee (tree) | the Napoleonic army system | arabic_philosophy_start_bonus | [ref](https://commons.wikimedia.org/wiki/Category:Grande_Arm%C3%A9e) — Napoleon's Grande Armée |
| napoleon_start | corps system / nation in arms | indian_philosophy_start_bonus | [ref](https://commons.wikimedia.org/wiki/Category:Grande_Arm%C3%A9e) — Napoleon's Grande Armée |
| napoleon_jeune_garde | the Young Guard | arabic_peninsula_path_1 | [ref](https://commons.wikimedia.org/wiki/File:Napoleon-imperial-guard.png) — Napoleon's Imperial Guard |
| napoleon_vieille_garde | the Old Guard veterans | arabic_peninsula_path_5 | [ref](https://commons.wikimedia.org/wiki/Category:Imperial_Guard_(Napoleon_I)) — Napoleon's Old Guard |
| napoleon_la_garde_meurt | "La Garde meurt" (Path A capstone) | arabic_levantine_path_1 | [ref](https://commons.wikimedia.org/wiki/Category:Imperial_Guard_(Napoleon_I)) — Napoleon's Old Guard |
| napoleon_brienne | artillery schooling at Brienne | arabic_levantine_path_4 | [ref](https://commons.wikimedia.org/wiki/Category:Artillery_of_the_Napoleonic_Wars) — Napoleonic artillery |
| napoleon_grande_batterie | massed grand battery | arabic_african_path_5 | [ref](https://commons.wikimedia.org/wiki/Category:Artillery_of_the_Napoleonic_Wars) — massed Napoleonic battery |
| napoleon_dieu_de_la_guerre | "artillery is the god of war" (Path B capstone) | indian_northern_path_3 | [ref](https://commons.wikimedia.org/wiki/Category:Artillery_of_the_Napoleonic_Wars) — massed Napoleonic battery |
| napoleon_bataillon_carre | the bataillon carré | indian_southern_path_1 | [ref](https://commons.wikimedia.org/wiki/Category:French_infantry_of_the_Napoleonic_period) — Napoleonic French line infantry |
| napoleon_manoeuvre | la manœuvre sur les derrières | indian_southern_path_7 | [ref](https://upload.wikimedia.org/wikipedia/commons/e/e0/Napoleon-Studying.jpg) — Napoleon studying a map (Flameng) |
| napoleon_campagne_1805 | 1805 Ulm/Austerlitz (Path C capstone) | indian_western_path_2 | [ref](https://commons.wikimedia.org/wiki/File:Battle_of_Austerlitz,_2nd_December_1805.png) — Battle of Austerlitz 1805 |
| napoleon_levee | la levée en masse | arabic_peninsula_path_1 | [ref](https://commons.wikimedia.org/wiki/File:Levee_en_masse.jpg) — the levée en masse |
| napoleon_baton | the marshal's baton | arabic_peninsula_path_5 | [ref](https://commons.wikimedia.org/wiki/Category:Marshal%27s_batons_of_France) — a Napoleonic marshal's baton |
| napoleon_la_gloire | la gloire, cult of victory (Path D capstone) | arabic_levantine_path_4 | [ref](https://commons.wikimedia.org/wiki/File:Fran%C3%A7ois_G%C3%A9rard_-_Napoleon_in_Coronation_Robes.jpg) — Napoleon in glory / coronation |
| napoleon_lempereur | "L'Empereur" grand capstone | arabic_philosophy_start_bonus | [ref](https://upload.wikimedia.org/wikipedia/commons/5/50/Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project.jpg) — David's Napoleon portrait 1812 |

### The Five Qing Military Traditions — `common/military_traditions/00_qing.txt`
Five trees, each expanded to 9 nodes (root start-bonus + 8 nodes). Every `image`/`icon` slot borrows a
stock `arabic_*`/`indian_*` tradition sprite and is flagged `# placeholder`. Concepts by node name:

| Tree (root) | Concept | Node keys (borrowed sprites, all placeholder) | Reference image |
|---|---|---|---|
| qing_eight_banners_tradition | Eight Banners 八旗 elite host | qing_banner_start / _cavalry / _garrison / _firearms / _capstone / _vanguard / _jianrui / _bondservants / _niru | [ref](https://en.wikipedia.org/wiki/Eight_Banners) — the Manchu Eight Banners (article) |
| qing_green_standard_tradition | Green Standard Army 綠營 (Han provincial infantry) | qing_green_* nodes | [ref](https://en.wikipedia.org/wiki/Green_Standard_Army) — the Green Standard Army (article) |
| qing_mongol_cavalry_tradition | Mongol banner cavalry 蒙古馬隊 | qing_mongol_* nodes | [ref](https://commons.wikimedia.org/wiki/Category:Mongolian_cavalry) — Mongol cavalry |
| qing_frontier_defence_tradition | frontier defence / garrison 邊防 | qing_frontier_* nodes | [ref](https://commons.wikimedia.org/wiki/Category:Forts_in_Xinjiang) — a Qing frontier fort |
| qing_tributary_levy_tradition | tributary levy 藩屬徵兵 (subject auxiliaries) | qing_tributary_* nodes | [ref](https://en.wikipedia.org/wiki/Tributary_system_of_China) — the Chinese tributary system (article) |

---

## 5. Event pictures — `common/event_pictures/00_event_pictures.txt`
Referenced-but-undefined pictures aliased to the closest vanilla event texture.

| Alias | Concept | Borrows | Reference image |
|---|---|---|---|
| senate | senate / legislative debate scene | Event_senate_debate.dds | [ref](https://commons.wikimedia.org/wiki/Category:Parliament_buildings) — a national parliament chamber |
| navy | navy / naval scene | Event_naval_battle.dds | [ref](https://commons.wikimedia.org/wiki/Category:Naval_battles_involving_France_(Napoleonic_Wars)) — an age-of-sail naval battle |
| greek_siege | a besieged city | Event_walled_city_under_siege.dds | [ref](https://commons.wikimedia.org/wiki/Category:Sieges) — a walled city under siege |

---

## 6. GUI panel header icons — Qing ministry/panel windows
Each panel header reuses a generic `menu_buttons/menu_*.dds` sprite as a stand-in for a missing
ministry-specific icon.

| Panel | Concept | Borrows | Reference image |
|---|---|---|---|
| qing_zongli.gui | Zongli Yamen, foreign affairs (總理衙門) | menu_diplomacy.dds | [ref](https://upload.wikimedia.org/wikipedia/commons/7/7e/Four_Members_of_the_Tsung-li_Yam%C3%AAn.jpg) — members of the Zongli Yamen 總理衙門 |
| qing_lifanyuan.gui | Lifan Yuan, Court of Colonial Affairs (理藩院) | menu_diplomacy.dds | [ref](https://en.wikipedia.org/wiki/Lifan_Yuan) — the Lifan Yuan 理藩院 (article) |
| qing_greatgame.gui | Great Game diplomacy dashboard | menu_diplomacy.dds | [ref](https://en.wikipedia.org/wiki/The_Great_Game) — the Great Game (article) |
| qing_censorate.gui | Censorate (都察院) | menu_religion.dds | [ref](https://en.wikipedia.org/wiki/Censorate) — Qing Censorate 都察院 (article) |
| qing_hanlin.gui | Hanlin Academy (翰林院) | menu_religion.dds | [ref](https://en.wikipedia.org/wiki/Hanlin_Academy) — the Hanlin Academy (article) |
| qing_justice.gui | Board of Punishments (刑部) | menu_religion.dds | [ref](https://en.wikipedia.org/wiki/Ministry_of_Justice_(imperial_China)) — Imperial Board of Punishments (article lead) |
| qing_rites_ministry.gui | Board of Rites (禮部) | menu_religion.dds | [ref](https://en.wikipedia.org/wiki/Ministry_of_Rites) — Board of Rites (article lead) |
| qing_southern_study.gui | Southern Study (南書房) | menu_religion.dds | [ref](https://en.wikipedia.org/wiki/Southern_Study) — the Southern Study 南書房 (article) |
| qing_upper_study.gui | Upper Study (上書房) | menu_religion.dds | [ref](https://en.wikipedia.org/wiki/Shangshufang) — the Upper Study 上書房 palace school (article) |
| qing_deliberative.gui | Deliberative Council (議政) | menu_military.dds | [ref](https://en.wikipedia.org/wiki/Deliberative_Council_of_Princes_and_Ministers) — Manchu Deliberative Council (article) |
| qing_guard.gui | imperial Guard / commandant (侍衛) | menu_military.dds | [ref](https://commons.wikimedia.org/wiki/Category:Imperial_Guards_(Qing_dynasty)) — Qing imperial guard 侍衛 |
| qing_war_ministry.gui | Board of War (兵部) | menu_military.dds | [ref](https://commons.wikimedia.org/wiki/File:Qing_Dynasty_Eight_Banners.svg) — Qing Eight Banners |
| qing_xinjiang.gui | Xinjiang / New Dominion (新疆) | menu_military.dds | [ref](https://upload.wikimedia.org/wikipedia/commons/7/71/Qing_dynasty_and_Xinjiang.jpg) — Qing Xinjiang province (map) |
| qing_personnel.gui | Board of Personnel (吏部) | menu_government.dds | [ref](https://commons.wikimedia.org/wiki/File:Qing_Dynasty_Mandarin.jpg) — Qing mandarin official |
| qing_caravan.gui | caravan trade | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/File:Moden_carpet_illustrating_camel_caravan_on_Silk_Road._Kashgar.jpg) — a Silk Road camel caravan |
| qing_harem.gui | harem / inner court | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/Category:Qing_dynasty_imperial_consorts) — a Qing imperial consort |
| qing_household.gui | Imperial Household Department (內務府) | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/Category:Forbidden_City) — the Forbidden City |
| qing_opium.gui | opium trade / suppression | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/Category:Opium_dens) — a 19thC Chinese opium den |
| qing_population.gui | population / Malthusian pressure | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/Category:Along_the_River_During_the_Qingming_Festival) — a crowded Qing town (cf. Qingming scroll) |
| qing_princes.gui | succession / princes contest | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/Category:Qing_dynasty_princes) — a Qing dynasty prince 親王 |
| qing_revenue_ministry.gui | Board of Revenue (戶部) | menu_trade.dds | [ref](https://commons.wikimedia.org/wiki/Category:Sycee) — Chinese sycee silver ingots 銀錠 |
| qing_secretariat.gui | Grand Secretariat (內閣) | menu_trade.dds | [ref](https://en.wikipedia.org/wiki/Grand_Council_(Qing_dynasty)) — the Grand Council / Grand Secretariat (article) |
| qing_works_ministry.gui | Board of Works (工部) | menu_trade.dds | [ref](https://en.wikipedia.org/wiki/Ministry_of_Works) — Board of Works (article lead) |

---

## 7. Legion distinctions — `common/legion_distinctions/00_qing_distinctions.txt`
Six Qing legion distinctions (granted via `add_distinction`, not gated in the definition). Each `icon =`
borrows a stock vanilla `phalera_*` distinction sprite as a placeholder for bespoke banner-unit art.

| Distinction | Concept | Borrow (phalera_* placeholder) | Reference image |
|---|---|---|---|
| distinction_qing_green_standard | Green Standard Army 綠營 | phalera_sword_shield | [ref](https://en.wikipedia.org/wiki/Green_Standard_Army) — the Green Standard Army (article) |
| distinction_qing_jianrui | Jianrui Battalion 健銳營 (storm troops) | phalera_tower | [ref](https://en.wikipedia.org/wiki/Jianruiying) — the Jianrui Battalion 健銳營 (article) |
| distinction_qing_solon | Solon/Sibe banner archers 索倫 | phalera_archer | [ref](https://en.wikipedia.org/wiki/Solon_people) — the Solon banner people (article) |
| distinction_qing_firearms_brigade | Firearms Brigade 火器營 | phalera_swords | [ref](https://en.wikipedia.org/wiki/Firearms_Brigade_(Qing_dynasty)) — the Qing Firearms Brigade 火器營 (article) |
| distinction_qing_rattan_shield | Rattan-shield troops 藤牌兵 | phalera_helmet | [ref](https://en.wikipedia.org/wiki/Rattan_shield) — the rattan shield 藤牌 (article) |
| distinction_qing_camel_fort | Camel-borne swivel-gun fort 駝城 | phalera_horse | [ref](https://commons.wikimedia.org/wiki/Category:Bactrian_camels) — a Bactrian war camel (駝城 mount) |

---

## 8. Qing inventions — `common/inventions/00_qing_inventions.txt`
14 Qing-specific inventions across the civic tree. **No icon block** — inventions render with the
technology-tree node styling, not a bespoke sprite, so there is no placeholder icon to catalogue here;
this section is a completeness record. Nodes: qing_tech_imperial_kilns, _imperial_silk, _tea_canton,
_grand_canal, _siku_compilation, _court_mathematics, _eight_banners, _columbian_crops, _variolation,
_manchu_science, _han_science, _mongol_science, _tibetan_science, _uyghur_science (the last five are the
integration-science unlocks armed by the culture decisions in culture_decisions/qing_integration_science.txt).

> **Note — Administrative + Academic tree build-out (2026-07-25):** the +28 oratory and +29 religious
> nodes added to `00_oratory_inventions.txt` / `00_religious_inventions.txt` likewise carry **no bespoke
> icons** (invention nodes are text/tech-tree styled), so they need no placeholder-art catalogue entry.
> They DO have full name+desc loc in `technology_l_english.yml`.

---

*Reference-image links: Wikimedia Commons file pages / categories and Wikipedia article leads, gathered by web search. Category/article links point to a page whose imagery represents the concept (grab the lead/representative image); direct upload.wikimedia.org links are specific files. Verify each licence before redistribution.*

---

## Producing real `.dds` icons from the reference images

**Environment as found (2026-07-17):** Compressonator is present at `~/github.com/compressonator/`
as a **source checkout only** — the `compressonatorcli` files there are bash wrapper scripts and
there is **no built binary** (no `bin/`, no Mach-O executable). This machine has `python3`, `cmake`,
`xcodebuild`, and `brew`, but **no image library** (no Pillow, no ImageMagick) and no DDS encoder on
`PATH`. So an encoder must be built or installed before any DDS can be produced.

**Target DDS formats (match the existing icons):**
- Mission task icons, trade-goods, and `menu_buttons`/panel icons → **50×50, uncompressed BGRA8
  (`A8R8G8B8`, 32-bit, masks BGRA), 1 mip, no mipmaps, non-power-of-two OK.** (verified: `tradegoods/coal.dds`,
  `menu_buttons/menu_trade.dds`)
- Small modifier icons → **DXT1** (or **DXT5** if alpha needed) at the sibling's size (e.g.
  `administration.dds` = 46×46 DXT1). No mipmaps.
- The engine needs neither mipmaps nor power-of-two dimensions.

### Steps YOU need to do (blockers — I can't do these from here)

1. **Stand up a DDS encoder.** Either:
   - **(a) Build the Compressonator CLI** (best format coverage — does both BGRA8 and DXT):
     ```
     cd ~/github.com/compressonator
     cmake -S . -B build_cli -DOPTION_ENABLE_ALL_APPS=OFF -DOPTION_BUILD_APPS_CMP_CLI=ON
     cmake --build build_cli --config Release
     ```
     Then symlink the resulting `compressonatorcli` onto `PATH` (or tell me its path). If the CLI
     build drags in Qt5/other deps and fails, paste me the error and I'll adjust the flags.
   - **(b) Fallback:** `brew install imagemagick` — scriptable, writes DXT1/DXT5 DDS out of the box.
     (For the uncompressed 50×50 BGRA8 style I can hand-write correct DDS headers in Python instead.)
2. **Install an image-processing lib** (needed for crop/resize/alpha regardless of encoder):
   `brew install imagemagick` **and/or** `pip3 install Pillow numpy`.
3. **Decide the licensing/style approach (the real decision — see the reference-link note above).**
   The links are *reference* images (photos/paintings under assorted licences), not sprites:
   - **(i) Mechanical conversion** — I crop/resize/alpha/encode the reference images as-is into DDS
     placeholders. Fast and functional, but photo-style (mismatched with the mod's painted-icon look)
     and licence-encumbered (attribution/redistribution obligations per file).
   - **(ii) Reference-only** — the links guide real art that you/an artist draw; I only encode DDS
     from your finished PNGs. Clean licence + consistent style.
4. **Confirm I may fetch the source rasters** (if going with (i)): I can `curl` the URLs into a scratch
   folder, but many links are Commons **category/article** pages, not direct files — so I'd pick a
   representative image per concept (your call), or you drop chosen PNGs into `art_src/<icon_key>.png`.

### Steps I will do once 1–4 are set

5. Fetch/read each source raster → **square-crop + resize** to the target size + **apply the alpha**
   (transparent rounded-icon look matching siblings).
6. **Encode** each to DDS in the correct format:
   - `compressonatorcli -fd DXT1 in.png out.dds` (or `-fd DXT5` for alpha), or
   - ImageMagick / a small Python BGRA8 writer for the uncompressed 50×50 icons.
7. **Place** each DDS at the right `gfx/interface/icons/...` path, keyed off this catalogue.
8. **Wire the sprite defs.** Mission task icons currently point at stock `test1/2/3`, so besides the
   DDS I'll add real `spriteType`/`spriteTypes` entries and repoint the mission-file `icon =` lines
   (and the trade-good / building / panel references) to the new sprites.
9. **Verify** every DDS header (magic `DDS `, format, dimensions) and run a boot-safety pass before
   committing.

### Fastest validation path
Do **step 1** (build CLI *or* `brew install imagemagick`) + **step 2**, answer **step 3** with (i) or
(ii). Then I convert **one** icon end-to-end (e.g. the Zongli Yamen panel icon) to prove the pipeline
before batching all ~130 concepts.

---

# IMPLEMENTATION (2026-07-26) — mechanical DDS generation run

Executing the user directive: *replace ALL placeholders with bespoke icons*, mechanical
conversion (option (i)), non-commercial so licensing is not a blocker. Decisions logged here as
work proceeds.

## Environment / tooling decisions
- **Compressonator ABANDONED + deleted** (762M checkout) and **cmake uninstalled** (brew). Its CLI
  build hard-requires OpenCV via the `canalysis` plugin even with `-DOPTION_ENABLE_ALL_APPS=OFF`;
  it is massive overkill for tiny icons. Removed at user request.
- **Encoder = pure Python** (`tools/dds_icon.py`, venv `~/.dds_venv`: Pillow 12.3.0 + numpy 2.5.1).
  We write **uncompressed 32-bit BGRA8 (A8R8G8B8)** DDS directly (124-byte header, no mipmaps,
  non-power-of-two OK). Verified byte-identical to shipped icons (round-trip test on
  `menu_trade.dds`: pixels identical, header fields match `pfflags=0x41 bits=32 masks=[ff0000,ff00,ff,ff000000]`).
  Uncompressed BGRA8 is universally engine-loadable — the shipped `tradegoods/*` and
  `military_traditions/*` icons already use exactly this format, so writing every bespoke icon in it
  is safe regardless of the donor's own format.
- **Pillow can also emit DXT1/DXT5** natively (tested) — kept in reserve; not needed since BGRA8 works.
- **Pipeline:** source raster → center square-crop → `ImageOps.autocontrast(cutoff=2)` +
  `Color.enhance(1.25)` (tiny photo icons otherwise crush to a dark blob) → resize to the donor's
  native dimensions → apply alpha → BGRA8 DDS. Enhancement is ON by default (user-approved).
- **Alpha:** borrow the donor's shaped alpha ONLY when the donor is an uncompressed BGRA8 with a
  genuine shape (>4 distinct alpha values — panel headers `distinct=209`, tradegoods `distinct=168`).
  Compressed donors (DX10/DXT3, e.g. mission tasks / buildings / event pictures) are opaque
  rectangles (distinct≤2), so those icons are written fully opaque — matching the donors.

## Graphics-resolution model (verified against imp19c + upstream sobiso + Invictus + TI + vanilla)
NONE of the mods ship a `.gfx` sprite registry or a top-level `interface/` dir — **all custom
graphics resolve BY FILENAME** from a conventional `gfx/interface/icons/<subdir>/<key>.dds` path.
Proven: imp19c `mission_tasks/russian_missions_1_*.dds` (custom mission set) and
`buildings/qing_*_building.dds`; Invictus `mission_tasks/task_apollo.dds` (ref'd `icon = task_apollo`)
and `military_traditions/dacian_path_1.dds` (ref'd `icon = ...`/`image = ...`). So a bespoke icon =
drop `<key>.dds` at the convention path + (for missions) repoint the `icon =` line from `test1/2/3`
to the task key.

Per-category donor + target path:
| Category | donor (size/format) | output path | wiring change |
|---|---|---|---|
| Mission task icons | `mission_tasks/test1.dds` (118×68, DX10) | `mission_tasks/<taskkey>.dds` | repoint `icon = testN` → `icon = <taskkey>` |
| Mission headers | `missions/mission_image_test.dds` (624×120, DX10) | `missions/mission_image_<tree>.dds` | repoint `header =` |
| Trade goods | `tradegoods/coal.dds` (50×50 BGRA8, shaped α) | `tradegoods/<good>.dds` | none (filename = good key) |
| Building-type icons | `buildings/EDU_school.dds` (200×200 DX10) | `buildings/<key>.dds` | none (already convention) |
| Military traditions | `military_traditions/arabic_*_path_*.dds` (198×72 BGRA8) | `military_traditions/<nodekey>.dds` | repoint `icon=`/`image=` |
| GUI panel headers | `menu_buttons/menu_trade.dds` (50×50 BGRA8, shaped α) | `menu_buttons/qing_<panel>.dds` | repoint `.gui texture=` |
| Event pictures | `event_window/Event_*.dds` (DXT3) | `event_window/qing_<alias>.dds` | repoint `picture=` |

## BLOCKERS (noted, working around per user instruction)
- **Legion distinctions (§7):** reference base-game sprite NAMES `phalera_*` with NO filename dir in
  ANY mod (imp19c/INV/TI all `icon = "phalera_zeus"` etc.) — resolved from the base-game sprite
  registry, not installable/inspectable locally. No local donor to size against. **Deferred** — would
  require adding a `.gfx` registry + guessing base sprite dims. Left as-is (they render via base game).
- **Modifier-cost icons (§3):** NOT blocked after all — they use an explicit `positive = "gfx/...dds"`
  path I can repoint to NEW mod art, and a local donor exists (`modifiers/commerce_value.dds`, 50×50
  BGRA8 shaped α). Handled: bespoke art written to `modifiers/<key>.dds` and the `positive =` line
  repointed. (These are the small building-cost glyphs; low visual priority but done for completeness.)

## Batch 1 — Mission task icons: DONE (203/203)
All 203 qing_*_missions.txt task `icon = testN` slots now have a bespoke
`gfx/interface/icons/mission_tasks/<taskkey>.dds` (118×68 BGRA8) and the `icon =` lines are
repointed to the task key. Queries auto-derived from each task's English loc title (verb-stripped,
CJK-stripped); 10 stragglers that returned no image were hand-queried (Konbaung/Daoguang/Lanfang/
Bakumatsu/Hokkaido/Uriankhai/Champa/Malacca/Malindi/Ezo). Commons rate-limited hard (HTTP 429) →
added 1.1s throttle + exponential backoff in fetch_wm.py; full run took ~40 min.
QUALITY NOTE: mechanical auto-match quality is mixed — most are on-concept (Zongli Yamen officials,
Beiyang ironclads, Daoguang portrait), but a minority drew weak Commons matches (e.g. qing_xj_pacify,
qing_hk_proclaim). Functional + correctly wired; flagged for optional hand-curation later.
Tools: tools/gen_mission_icons.py + icon_common.py; log tools/mission_icon_log.tsv.

## Batches 2–7 + Visual QA — DONE (367 bespoke icons total)
All placeholder icon slots replaced with bespoke mechanically-converted art (uncompressed 50×50/
118×68/198×72/200×200/624×120 BGRA8 as per each category's donor). Counts:
- Mission task icons: 203 (mission_tasks/<key>.dds, icon= repointed)
- Mission header banners: 16 (missions/mission_image_qing_<tree>.dds, header= repointed)
- GUI panel headers: 23 (menu_buttons/qing_<panel>.dds, .gui texture= repointed)
- Trade goods: 7 (tradegoods/<good>.dds)
- Building-type icons: 25 (buildings/qing_*.dds — overwrote the stopgap copies)
- Military traditions: 77 (military_traditions/<nodekey>.dds, icon=/image= repointed; manchu+napoleon+5 qing trees)
- Modifier-cost glyphs: 13 (modifiers/<key>.dds, positive= repointed)
- Event pictures: 3 (event_window/qing_<alias>.dds, picture= repointed)

VISUAL QA (in lieu of code review, per user directive — quality AND contextual appropriateness):
- Rendered per-category review montages (tools/qa_montage.py) + an objective heuristic detector
  flagging document-scans (high brightness + near-zero saturation) and flat/blur images.
- Two automated sweeps + manual montage review across all 8 categories. Re-fetched every flagged
  icon with curated concept-appropriate queries (and, where Commons search returned PDFs/wrong
  culture, hand-picked verified file titles). The military-tradition category (worst-hit by the wide
  198×72 aspect) was fully re-done from a curated pool of Qianlong-campaign battle engravings +
  Napoleonic battle paintings.
- Final detector state: 0 flagged in buildings/panels/modifiers/tradegoods/headers/traditions/events;
  1 in missions = qing_treasure_mao_kun_chart, a TRUE POSITIVE concept (the Mao Kun Chart genuinely
  is a pale historical navigation map — correct art, not a defect).
- Residual: a small minority of mission auto-matches remain imperfect (inherent ceiling of mechanical
  photo conversion); all are on-theme + correctly wired. Flagged for optional hand-curation.

BOOT-SAFETY VERIFY: all 367 new DDS validated (magic 'DDS ', 124-byte header, pfflags=0x41, bits=32,
masks BGRA, byte-length == 128 + w*h*4) — 0 malformed. All icon=/header=/image=/texture=/picture=/
positive= references resolve to an existing file — 0 dangling.

Tools (all under tools/, venv ~/.dds_venv): dds_icon.py (BGRA8 writer/probe), fetch_wm.py (Commons
fetch w/ throttle+backoff), icon_common.py, gen_mission_icons.py, gen_table_icons.py,
gen_tradition_icons.py, gen_header_modifier_icons.py, repoint_refs.py, qa_montage.py, qa_fixes*.py.

## BLOCKER (unchanged): Legion distinctions (§7)
The 6 qing legion distinctions still reference base-game sprite NAMES (phalera_*) with no filename
dir in any mod — resolved from the base-game sprite registry, not present locally. Replacing them
would require a .gfx registry + base sprite dims we can't inspect. Left as-is (renders via base game).
