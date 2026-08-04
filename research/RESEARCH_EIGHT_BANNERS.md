# Eight Banners 八旗 — Internal Structure Research Digest

For imp19c Eight Banners content (1763-appropriate). Sources: Elliott *Manchu Way*, Crossley *Translucent Mirror*/*Orphan Warriors*, Rawski; 八旗通志/清史稿兵志/杜家骥. Numbers are order-of-magnitude (paper niru=300, real effectives ~150-200).

## The 8 colours + precedence (Bordered Yellow is TOP — common mod error to put Plain Yellow first)
Order: 1.鑲黃 Bordered Yellow, 2.正黃 Plain Yellow, 3.正白 Plain White, 4.正紅 Plain Red, 5.鑲白 Bordered White, 6.鑲紅 Bordered Red, 7.正藍 Plain Blue, 8.鑲藍 Bordered Blue.

## Upper Three (上三旗) vs Lower Five (下五旗)
- Upper Three = 鑲黃 + 正黃 + 正白 — emperor's DIRECT command, supplied the imperial bodyguard 侍衛, palace/inner-court, 內務府 booi (bondservants from Upper Three).
- Lower Five = 正紅 鑲白 鑲紅 正藍 鑲藍 — nominal princely banner-lords (旗主), honorific by Qianlong.
- Origin: Shunzhi confiscated Dorgon's 正白 after Dorgon's 1651 posthumous disgrace → fixed the canonical Upper Three. Stable through 1763.

## 24 banners = 8 colours × 3 ethnic divisions
- 滿洲八旗 Manchu (senior, dominant, largest by Qianlong)
- 蒙古八旗 Mongol (separated out 1635; light cavalry; smallest)
- 漢軍八旗 Hanjun/Han-martial (*ujen cooha* "heavy troops" = artillery/firearms specialty; completed as 8 in 1642)
- HANJUN PURGE 出旗 from 1742 (Qianlong 7): systematic demotion/expulsion of Hanjun from rolls (fiscal 八旗生計 + Manchu-centric ethnicization). By 1763 Hanjun substantially reduced esp. in provincial garrisons → model as DECLINING/second-class; Manchu dominant.

## Hierarchy
牛录 niru (company, paper 300) → 甲喇 jalan (參領, ~5 niru) → 固山 gūsa (旗, 都統 commands).

## Metropolitan elite corps 禁旅八旗 (Beijing, ~half of all banners) — prestige tiers
- 護軍營 Hujun / 巴牙喇 Bayara = palace GUARDS (bayara = archaic name, NOT a separate 1763 corps — it's the Hujun's Manchu name). Top prestige.
- 前鋒營 Qianfeng = VANGUARD (advance/skirmish/shock). Top.
- 火器營 Firearms brigade, founded KANGXI 1691 (musket 鳥槍 + cannon; Manchu/Mongol-manned).
- 健銳營 JIANRUI = storming/scaling brigade, founded QIANLONG 1748 for First Jinchuan (stone-tower 碉樓 assault); trained at 香山 near 昆明湖. Most 1763-specific elite unit.
- 驍騎營 Xiaoqi = LINE banner cavalry (aliha cooha), largest/bread-and-butter, all banners.
- 步軍營 Bujun = Beijing gendarmerie under 步軍統領/九門提督.

## Provincial garrisons 駐防八旗 (walled 滿城 under 將軍)
Interior mostly Manchu (Hanjun pulled out by purge); frontier mixed Manchu/Mongol/新滿洲 (Xibe 錫伯/Solon 索倫/Daur/Chahar).
- Homeland: 盛京(Mukden) 吉林 黑龍江 generals.
- NW frontier: 伊犁 Ili general ESTABLISHED 1762 (brand-new at 1763; Xibe migration to Ili 1764 = one year after start). 烏魯木齊都統 = post-1763 (~1770s), keep minor/absent.
- Interior: 西安 寧夏 成都 江寧(Nanjing) 京口 杭州 荊州 福州 廣州(Canton, sole Western port post-1757).

## In-game application (imp19c)
Existing OOB (imp19c_effects_legion_setup.txt SE_qing_armies) already has a 八旗 block (Metropolitan + ~18 named 將軍 garrisons: Xi'an/Ili/Shengjing/Jingzhou/Hangzhou/Jiangning/Chengdu/Canton/Fuzhou/Ningxia/Liangzhou/Kaifeng/Taiyuan/Suiyuan/Heilongjiang/Urumqi/Kashgar) + a 綠營 block. New unit types qing_eight_banners / qing_green_standard / qing_bayara / qing_ever_victorious. Route banner garrisons → qing_eight_banners, green → qing_green_standard. Jianrui/Bayara already exist as legion distinctions + traditions + the Bayara-guard readiness meter (se_QING_MINISTRY.txt).

_Migrated from memory imp19c-eight-banners-research, per the research-digest-location rule._
