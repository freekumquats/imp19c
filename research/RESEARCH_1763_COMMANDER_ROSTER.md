# 1763 Qing Commander Roster — Research Digest

Sourced roster (2026-07-11, EN+ZH Wikipedia / 清史稿 cross-check) of period-appropriate 1763 Qing commanders to attach to the High Qing garrison OOB (SE_qing_raise_garrison_cmd). All verified ALIVE on 1763.2.16.

**NOTE (engine caveat lives in memory imp19c-1763-commander-roster):** the setup snapshot treats a char with a `death_date` as already-dead, so attaching a death-dated char as a `create_unit commander=` AT SETUP fails. Proven fix = strip death_date from attached commanders (or attach at runtime). See that memory for the reusable spawn pattern.

**ALREADY IN 00_Qing.txt** (carry death_date): Agui char:564 (d.1797), Zhaohui char:565 (d.1764), Yin Jishan char:566 (d.1771), Liu Tongxun char:562 (d.1773). Fuheng's father is char:211 but Fuheng himself is NOT a char.

**EXACT 1763 GARRISON-GENERAL POSTHOLDERS (駐防將軍)** — most ABSENT from the mod + have UNKNOWN birth dates:
- Guangzhou General 廣州將軍: **Langfu 朗福** (Manchu Bordered Yellow), term 1763-64
- Xi'an General 西安將軍: **Songchun 嵩椿** (Manchu Bordered Blue, imperial clansman), 1762-64
- Hangzhou General 杭州將軍: **Fulu 福祿** (Mongol Plain White), 1760-67
- Shengjing/Mukden General 盛京將軍: **Chaoquan 朝铨**, 1762-67
- Jiangning General 江寧將軍: **Rongbao 容保**, 1762-65
- Ili General 伊犁將軍: **Mingrui 明瑞** (Manchu Bordered Yellow, Fuca, b.1730 d.1768 Burma) — FIRST holder, appointed Nov 1762; building Huiyuan城 in 1763.

**BANNER-ELITE FIELD COMMANDERS:**
- **Fuheng 傅恆** (Fuca, Bordered Yellow, b.1720 d.1770) — Chief Grand Councillor, empress's brother; premier commander. First Jinchuan, Dzungar, Burma(fatal).
- **Zhaohui 兆惠** (Uya, Plain Yellow, b.1708 d.1764) — Xinjiang hero, Black Water Camp siege survivor. [char:565 exists]
- **Agui 阿桂** (Janggiya, Plain Blue→White, b.1717 d.1797) — future greatest general; Grand Councillor 1762-65. [char:564 exists]
- **Šuhede 舒赫德** (Šumuru, Plain White, b.1710 d.1777) — Xinjiang assistant cmdr, Heisuiying relief.
- **Aligun 阿里袞** (Niohuru, Bordered Yellow, b.? d.1769) — relieved Zhaohui at Black Water; brother of Aibida.
- **Hailancha 海蘭察** (Dolar, Solon/Ewenki→Bordered Yellow, b.1739 d.1793) — rising star age 24 in 1763; later 領侍衛內大臣.
- **Chenggunjab 成衮扎布** (Khalkha Mongol Borjigin, b.? d.1771) — senior Mongol ally/prince-commander.

**GREEN STANDARD / NAVAL (綠營/水師):**
- Fujian Naval Cmdr 福建水師提督: **Gan Guobao 甘國寶** (Han, b.1709 d.1776) term 1761-63; then **Huang Shijian 黃仕簡** (Han, b.1722 d.1789) from 1763. → Fujian/Guangdong navy squadrons.

**GOVERNORS-GENERAL (總督, military authority):** Yin Jishan (Liangjiang), Fang Guancheng 方觀承 (Zhili, Han, b.1696 d.1768), Su Chang 蘇昌 (Liangguang), Wu Dashan 吳達善 (Yun-Gui), Yang Yingju 楊應琚 (Shaan-Gan, Han-banner), Yang Tingzhang 楊廷璋 (Min-Zhe, Han-banner), Aibida 愛必達 (Huguang), Chen Hongmou 陳宏謀 (Han), Li Shiyao 李侍堯 (Han-banner). → Green Standard regional-army commanders.

**Culture/religion mapping:** Manchu → culture=manchu, religion=mahayana/vajrayana (mod uses mahayana); Mongol → mongol/vajrayana; Han → han/xiajiang + confucianism; Uyghur (Emin Khoja 額敏和卓, Yarkand, b.1694 d.1777) → uyghur/turkish + sunni.

**DEAD before 1763 — DO NOT USE:** Bandi 班第 (d.1755), Yarhašan 雅爾哈善 (d.1759). **Fude 富德** — no birth/death found; unverifiable.

Sources: EN+ZH Wikipedia (傅恆/兆惠/阿桂/明瑞/舒赫德/阿里袞/海蘭察/尹繼善/劉統勳 + 將軍列表 + 總督 lists + 福建水師提督列表), 清史稿.

_Migrated from memory imp19c-1763-commander-roster, per the research-digest-location rule._
