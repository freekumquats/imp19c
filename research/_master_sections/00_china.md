# QING CHINA — 1763 Ground Truth (DEFINITIVE, high-fidelity)

China is the mod's FOCUS region — fine historical fidelity and granularity. Snapshot: **Feb 1763, mid-Qianlong** (乾隆28年). The empire is at its territorial and demographic apogee (peak conquest 1759; territory essentially identical to the 1815 baseline).

## Sources & their grade
- research/1763_POPS_China.md — STRONG: Ho Ping-ti *Studies on the Population of China 1368–1953* (1959); Cao Shuji 曹樹基《中国人口史·明清卷》; Rowe *China's Last Empire* (2009); Perdue *China Marches West* (2005); Liang Fangzhong 梁方仲; registered 民數/丁 returns (清實錄/戶部). [MONOGRAPH + PRIMARY-registered]
- research/QING_APOGEE_RESEARCH.md — apogee=1759; territory, treasury, tributary ring, Ili General 1762. [MONOGRAPH + 中文 Wikipedia corroboration]
- research/QIANLONG_ROSTER_RESEARCH.md — Qianlong court/commanders/scholars roster. [MONOGRAPH]
- research/1763_HIGH_QING_mechanic_adaptation.md — High-Qing administrative/territorial content. [MONOGRAPH-derived]
- research/1763_WORLD_EAsia_SEAsia.md — tributary relations (Korea/Vietnam/Ryukyu/Siam/Burma). [MONOGRAPH/PRIMARY]

---

## OWNERSHIP / TERRITORIAL STRUCTURE (Feb 1763, Qianlong)

### China proper (直省 — the 18 provinces)
Direct bureaucratic rule under governors (巡撫) / governors-general (總督):
Zhili/Hebei (Beijing), Shandong, Shanxi, Henan, Shaanxi, Gansu, Jiangsu, Anhui, Zhejiang, Jiangxi, Hubei, Hunan, Sichuan, Fujian (incl. Taiwan prefecture, annexed 1683), Guangdong, Guangxi, Yunnan, Guizhou. [MONOGRAPH]
- Note: mod ships CHI owning ~450 provinces via own_control_core; ~573 province blocks across 19 setup files, with some as autonomous governorships (MNC Manchuria, MKD/HLJ frontier).

### Inner Asian dominions (direct Qing rule / military governorship — NOT tributary)
- **Manchuria** (東北): 3 military jurisdictions — Shengjing/Fengtian 盛京, Jilin 吉林, Heilongjiang 黑龍江. Banner homeland; Han settlement officially banned (but leaking south).
- **Inner + Outer Mongolia**: league-banner (盟旗) system; Khalkha (Outer) + Inner Mongol banners under the Lifan Yuan 理藩院.
- **Xinjiang** (Dzungaria + Tarim): JUST conquered 1755–1759; unified under the **Ili General 伊犁將軍 from 1762** (military governorship over N+S of the Tianshan). [MONOGRAPH: Perdue]
- **Qinghai/Kokonor** (1724) and **Tibet** — Tibet a **protectorate since 1720**: amban 駐藏大臣 at Lhasa + small garrison (~2–3k), NOT settlement. Dalai/Panchen Lama theocracy under Qing oversight.

### Tributary states (autonomous, NOT Qing territory — model as tributaries/subjects, not provinces)
- **Korea (Joseon)** — the model tributary (since 1637); King Yeongjo; annual missions via Uiju. Fully autonomous internally.
- **Vietnam ("Annam")** — tribute via the Trịnh-controlled Lê court (Vietnam is internally divided Trịnh/Nguyễn — see 60_asia_pacific.md).
- **Ryukyu** — dual tributary (Qing + Satsuma/Japan); King Shō Boku.
- **Siam (Ayutthaya)** — tributary; falls to Burma 1767.
- **Burma** — tributary status only FORMALIZED after the Sino-Burmese War (1765–69); in Feb 1763 not yet (Qing invasions begin 1765).
- **Laos (Vientiane/Luang Prabang/Champasak), Sulu** — intermittent/nominal tribute only; do NOT model as reliable subjects.
- ANACHRONISM FLAG: **Nepal is NOT yet a Qing tributary** (Gorkha war with Tibet → tributary status 1792; modern scholarship doubts even that). Do not add Nepal as a 1763 tributary.

---

## POPULATION (scale: mod uses 4000 people = 1 unit)

### Total
- **~205–215M actual** (headline **~210M**) for China proper c.1760–65; range ~185–225M. [MONOGRAPH: Ho Ping-ti]
- Registered 民數 series [PRIMARY-registered]: 1749 ~177M, 1750 ~181.8M, **1766 ~208M**, 1776 ~268M (the jump = better registration, not real growth), 1790 ~301M.
- **ding-vs-head caveat**: pre-1740s counts were *ding* 丁 (fiscal adult-male units), NOT people; the 攤丁入地 tanding-rudi reform (empire-wide by 1740s) + the 1741 baojia 保甲 order to report total persons 民數 is why "population" leaps ~140M (1741) → 200M+ within a generation. Mod: use ~185M for a "registered" feel, ~205–215M for actual demographic weight.

### Province-by-province (China proper) — magnitude + composition [ESTIMATE, Cao Shuji-style shares; treat as magnitudes]
Ranked approx pop c.1770s (millions), dominant culture = Han unless noted, religion = Confucian–Mahayana–Daoist syncretism unless noted:
- **Jiangsu ~30** — Jiangnan core, highest population density on earth (Suzhou/Nanjing). Wu culture.
- **Shandong ~22–24** — North China Plain. Beihua (N. Han).
- **Zhejiang ~18–21** — Jiangnan (Hangzhou). Wu.
- **Guangdong ~16–19** — Lingnan/Pearl delta (Canton). Yue culture; Hakka pockets.
- **Henan ~16–18** — North China Plain. Beihua.
- **Anhui ~16–18** — S. Anhui = Jiangnan (Wu); N. Anhui = plain (beihua).
- **Jiangxi ~15–17** — Gan culture; Jingdezhen porcelain.
- **Zhili/Hebei ~14–17** — Beijing metropolitan. Beihua.
- **Hubei ~14–16** — mid-Yangzi (Wuhan). Xiajiang/Han.
- **Hunan ~13–16** — mid-Yangzi; Xiang culture; W. Hunan Miao/Tujia.
- **Fujian ~10–12** — SE coast; Min culture; Hakka; + Taiwan (Han settlers + aboriginal Formosans).
- **Shanxi ~10–12** — Jin culture; Shanxi merchant banks.
- **Gansu ~8–12** — large **Hui (Sino-Muslim, Sunni Islam)** population alongside Han.
- **Shaanxi ~7–9** — Xi'an; Han + some Hui (NW).
- **Sichuan ~6–8** — **rapidly-infilling immigrant frontier**: Ming-Qing collapse ~4M(c1600)→~0.8M(c1660, ~80% collapse); 湖廣填四川 migration refilled it ~4M(1720s)→~8M(1776)→~22M(1813). In 1763 ~6–7M, mostly recent Han from Hubei/Hunan/Jiangxi (in-migration candidate). Han syncretic.
- **Guangxi ~5–7** — many non-Han: **Zhuang** (largest), Yao; + Han. Ping/Yue Han.
- **Yunnan ~4–6** — frontier; **Yi, Dai, Bai, Miao** + expanding Han; some Hui. Han syncretic + indigenous/animist; Dai = Theravada.
- **Guizhou ~4–5** — Miao frontier; **Miao/Bouyei** + Han. 改土歸流 gaitu guiliu zone (hereditary 土司→bureaucratic), recurrent Miao revolts. Han syncretic + animist.
- Dense core = Lower Yangzi/Jiangnan (Jiangsu+Zhejiang+S.Anhui) + North China Plain (Shandong/Henan/S.Zhili). Rising secondary = mid-Yangzi (Hubei/Hunan/Jiangxi) + Lingnan. Frontier/low-density = SW + NW + Sichuan (refilling).
- Rule of thumb: **~95%+ of the empire's people are Han in the 18 provinces**; the frontier dependencies are only a few million combined but hold the ethnically/religiously distinctive populations.

### Inner Asia — magnitude + composition [ESTIMATE, lightly/unregistered]
- **Manchuria ~1–2M** — thin, mostly southern (Fengtian/Liaodong): Han settlers (south, despite ban) + Manchu bannermen + Tungusic (Sibe/Daur/Solon) + some Mongols. Han folk-religion; Manchu shamanism + Tibetan Buddhism among elites.
- **Inner Mongolia ~1–2M** Mongols (pastoral); **Outer/Khalkha** few-hundred-k to ~1M. Mongol; Tibetan (Gelug) Buddhism, heavily monastic (large share of adult males are lamas).
- **Xinjiang <1M, DEPOPULATION FLAG**: the Dzungar Khanate (~600k, Wei Yuan) was annihilated 1755–58 (~70–80% died: ~40% smallpox, ~30% killed, ~20% fled). So 1763 **Dzungaria (N. Xinjiang) is near-emptied steppe** just starting Qing resettlement (Han tuntian around Ürümqi, Hui, Manchu/Sibe garrisons, Taranchi Uyghur farmers). **Tarim Basin (Altishahr, S. Xinjiang) was populous**: ~250–300k+ households of Turkic-Muslim oasis farmers = **Uyghurs, Sunni Islam**. Unusually ethnically fragmented.
- **Tibet ~1–2M** (common low anchor ~1M) — Tibetan; Tibetan (Gelug/Vajrayana) Buddhism, very monastic.
- **Qinghai/Kokonor** — Tibetan (Amdo) + Mongol + Hui; Tibetan Buddhism + Islam.

### Major cities c.1763 [ESTIMATE]
- **Beijing ~0.9–1.0M** — political #1, among the world's largest.
- **Suzhou ~0.5–1M metro** — economic/cultural #1 of Jiangnan.
- **Hangzhou ~0.5M**; **Nanjing ~0.5M+**.
- **Guangzhou/Canton ~0.5–0.8M metro** — sole legal Western port under the 1757 Canton System (trade gateway).
- **Wuhan cities** (Hankou+Wuchang+Hanyang) ~0.5M+ — mid-Yangzi entrepôt.
- Others: Yangzhou (salt), Foshan (iron/ceramics), Jingdezhen (porcelain), Tianjin, Xi'an, Chengdu, Fuzhou.

### Mod data notes (culture/religion keys already present in setup files)
- CULTURE KEYS: beihua (N. Han dominant), shangjiang, yue, xiajiang, wu, hui, min, gan, manchu, uighur, jin, hakka, xiang, ping, amdo, miao, khams, thai, oirat, gyarlong, kachin, hlai, tajik, kam-sui, tujia, shan, tibetan, mongolian, kazakh.
- RELIGION KEYS: daoism (dominant), mahayana, sunni, pure_land_buddhism, linh, theravada, catholic, nuoism, confucianism, vajrayana, syncretic_muslim, siberian_shamanism, evangelical, nestorian, jewish.
- Pops live as strata `amount=` blocks in 19 setup/provinces/00_*.txt; province-level culture=/religion= is the per-strata default; a strata block may carry its own culture=/religion= for a minority pop. Total pop = sum of amount= (no size field). CHI literacy floors already in se_EDU.txt (t1=0.17, t2=0.01).

---

## KEY FACTS / ANACHRONISM CHECKLIST (China)
- Qianlong reign (弘曆, r.1735–1796) at apogee; peak conquest 1759; territory ≈ identical to the 1815 baseline (no border change 1759→1815; Ili loss 1864/1881 is later).
- **Xinjiang JUST conquered (Dzungar genocide 1755–57)** — Dzungaria near-empty in 1763, starting resettlement; Tarim Uyghur oases populous. Ili General office from 1762.
- **Tibet = amban protectorate (since 1720)** — Qing garrison + amban, not a province, not settled.
- Tributaries (Korea/Vietnam/Ryukyu/Siam) are AUTONOMOUS, NOT provinces. **Burma tributary only after 1769** (not in 1763). **Nepal NOT a tributary in 1763** (do not add).
- Population **~210M actual / ~185M registered** — mind the ding-vs-head registration caveat (the 1741→1776 "growth" is largely better counting).
- **Sichuan is a rapidly-infilling immigrant frontier (~6–7M)**, mostly recent Han from Huguang — not yet the ~22M it reaches by 1813.
- **Jiangnan (Lower Yangzi) is the densest region on earth**; Beijing ~1M; Canton = sole legal Western trade port (1757 Canton System).
- ~95%+ Han in the 18 provinces; distinctive minorities are frontier — Hui (Gansu/NW, Sunni), Zhuang/Yao (Guangxi), Yi/Dai/Bai/Miao (Yunnan/Guizhou), Miao/Tujia (W. Hunan/Guizhou), Manchu/Tungusic (Manchuria), Mongol (Mongolia, Gelug Buddhist), Uyghur (Tarim, Sunni), Tibetan (Tibet/Amdo, Vajrayana), Taiwan aboriginal Formosans.
- Treasury (戶部銀庫) at High-Qing strength (~74M taels peak mid-1770s); "before-decay" state (White Lotus 1796, Opium War 1839 all far future).
