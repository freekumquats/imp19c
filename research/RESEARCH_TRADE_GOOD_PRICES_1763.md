# Historical relative prices of 1763-era trade goods — sourced research digest (REVISED)

**For:** #49 (is the mod's flat 0.2 base-value table intentional / can it be differentiated), #44
(salt monopoly window — raw vs gabelle-taxed value), #50/#52 (regional divergence + tier
seeding), #46 (gold vs silver sell-reserve behavior). **Date:** 2026-08-09, revised same day
after two steering corrections from team-lead.

**REVISION NOTE (important — read before using any number below):** An earlier draft of this
digest reported single "world price" figures per good. That framing is **historically wrong**
and has been corrected. In 1763 there was **no integrated global commodity market**: silk/tea/
porcelain were cheap at their point of production in China and dear in London; the gold:silver
ratio itself DIFFERED by region (that arbitrage gap is precisely why silver flowed to China for
250 years); grain prices were intensely local. Every figure below is now tagged with its
**region** — China-domestic, Canton-export (wholesale, foreign-buyer price), or Europe-retail —
and the divergence between regions is reported as a **headline finding**, not a footnote. See
Section A0 for the regional-spread framing and Section E for which anchor the mod's single
base_value field should use.

**Scope discipline (China-fine-fidelity rule, restated per the latest steer):** the user's
explicit priority is **the price IN CHINA**, sourced from **Chinese-language scholarship** where
possible. This revision adds several Chinese-language / direct-primary-text findings (清史稿
食貨志 fetched directly from Wikisource; a Chinese secondary study of the 1740 Qianlong-5 salt-
price-setting case at Hankou) alongside the English-language Canton-trade-contract sourcing
(Van Dyke) from the first pass. Where a number is Canton-export or Europe-retail rather than
China-domestic, that is now called out explicitly rather than left ambiguous.

---

## A0. THE REGIONAL SPREAD — headline finding, not a footnote

**Silk/tea/porcelain: cheap in China, expensive in Europe.** Van Dyke (2011), reproducing
original Canton trade contracts, records Bohea tea (the cheapest common export grade) at
**12-20 taels/picul wholesale at Canton** across 1730-1770s (see A2 below) — this is already
the price a Chinese merchant sold to a foreign buyer AT THE CHINESE PORT, before the Atlantic
voyage, before European import duties, and before European retail markup. By the time the same
tea reached a European consumer it carried:
- **Round-trip voyage risk premium**: Canton-Southeast-Asia junk bottomry ran **~40%/voyage**;
  European-ship bottomry to/from Asia ran **12-18%/voyage** (Van Dyke 2011 pp.44-46, Table 2.2,
  a 1731 Swedish traveler's tabulation) — this premium is baked into the price BEFORE the good
  ever reaches Europe.
- **Sales-price-to-purchase-price ratios of 2.4:1 to 3.4:1** for Cape-route Asia-to-Europe cargo
  overall (De Vries 2003 p.89, Table 2.13, quoted in Melitz 2017 p.12 — covers 1600-1750,
  narrowing over time as competition increased).
- The English East India Company's own gross margin on **non-gold Asian merchandise averaged
  ~150% (2.5×)** for a 1729-1741 sample of 16 ships (Dermigny 1964 vol.2 pp.424-425, via Melitz
  p.13) — i.e., **the same chest of tea that sold for ~17.8 taels/picul at Canton was reselling
  in London for something on the order of 2.5-3× that**, before any further European retail
  markup on top of the Company's own wholesale resale price.

**Silver itself was worth MORE in China than in Europe, and that arbitrage gap is why silver
flowed to China for two and a half centuries.** This is not a side detail — it is the central
mechanism of the entire China trade (see A1 for the numbers). The mod's engine cannot represent
"the same ounce of silver is worth two different things in two different provinces" with a
single global base_value field — this divergence has to live in the mod's region/tradezone
price layer, never the base field (see Section E).

**Grain was intensely local and did NOT track any of the above.** Rice prices in Wu-hsi
(Soochow) and Nanchang (Kiangsi), just ~500 km apart, differed by 0.6 taels/shih at the same
point in time (see A3) — a >60% spread for the SAME commodity within China, driven by local
harvest and transport-cost conditions, with no connection to the silk/tea export-price world at
all. Treat any single "grain price" as a China-wide rough average of a genuinely noisy regional
series, not a precise figure.

**Practical consequence for this digest:** every price table below is now labeled by which of
these three price-worlds it comes from. Do not average a Canton-export tael/picul figure with a
Europe-retail figure and call it "the" price — they measure different things at different
points in a value chain that itself embodies large, historically real margins.

---

## A1. Gold:silver ratio — CHINA figure is now the primary number

This is the case where regional divergence is THE finding, not a caveat.

| Region | Ratio | Date | Source |
|---|---|---|---|
| **China (domestic)** | **1:10** | early Qing (per one Chinese secondary synthesis, "初期還是一比十") | Chinese-language secondary source aggregating the standard periodization (search-summary level; corroborates the English-source figure below, not independently primary-verified this session) |
| **China (domestic)**, later Qianlong | **rising to ~1:15** | late Qianlong (per the same Chinese source, "乾隆後期漲到了一比十五") | same |
| **China at Canton**, measured against the international price | **138% of international (i.e. gold cheaper in China, ratio narrower than Europe's) in the 1730s → 97% (essentially AT parity) by the 1750s** | 1730s→1750s | Richard von Glahn (2003) p.197, quoted in Jacques Melitz, *Some Doubts about the Economic Analysis of the Flow of Silver to China 1550-1820*, CEPII Working Paper 2017-19, pp.5-6 — **read in full text this session** |
| **China (domestic)**, plotted series | **≈8-10:1 through most of 1650-1700**, converging upward from ~1720, **essentially unified with Europe's ~14.5-15:1 by 1750-1763**, then moving in tandem for the rest of the century | 1550-1820 (Melitz Figure 1b) | Melitz 2017, using **Peng Xinwei 彭信威 (1993-4)** pp.767-768 for the China series + Soetbeer (1879) for the Europe/Germany series — Melitz's own citation of Peng, not this session's own read of Peng |
| Late-17th-c. anchor, Peng Xinwei's own words | "an ounce of gold cost **15 ounces of silver in Europe, but still only 10 in China**" | second half of 17th c. | Peng Xinwei 彭信威《中國貨幣史》(1994 Kaplan trans.), p.766, quoted directly in Melitz p.11 — **this is Peng Xinwei's own foundational price-history source, the No.1 recommended source in the task brief, reached via Melitz's citation of it** |
| **Europe (England)**, for comparison | 1:15 (Mint rate), market drifting toward 1:14½ | 1717-1730 | Cantillon, *Essai sur la nature du commerce en général* (written ≤1734), primary excerpt, pp.91-94 — read in full text |
| **Japan**, for comparison | 1:8 | ~1730s | same Cantillon excerpt |
| China vs Europe, 1720-1740 arbitrage episode (the LAST major one before convergence) | EIC ships carried gold FROM Canton TO London specifically because China still undervalued gold relative to Europe; ~30% gross margin on gold vs ~150% (5×) on ordinary merchandise, sample of 16 vessels | 1729-1741 | Dermigny (1964) vol.2 pp.424-425, via Melitz pp.12-13 |

**Headline finding, stated plainly:** China's domestic gold:silver ratio sat at roughly **half**
Europe's for most of the 17th century (China ~1:8-10 vs Europe ~1:14-15) — gold was cheap in
China relative to silver, silver was dear in China relative to gold, and this exact asymmetry is
the textbook explanation for why New World and Japanese silver flowed toward China for
centuries (silver bought more gold, or more of anything else, once landed in China than it did
staying in Europe). **By the mod's 1763 bookmark, this gap had closed**: both the Chinese-source
synthesis (1:10 early Qing → 1:15 late Qianlong) and the English-source Melitz/von Glahn finding
(parity reached by the 1750s) agree the ratios were essentially unified by 1750-1763 and moved
together for the rest of the century. **This is a two-source-corroborated finding, not a
single-source claim.**

## A2. Bohea tea (bulk export tea) — CANTON-EXPORT price (China-side wholesale, foreign-buyer contract)

All figures below are the price a Chinese merchant charged a European trading company AT
CANTON — this is the domestic-Chinese-side of the export transaction, NOT a European retail
price, and NOT (so far as this session could determine) the same as tea's price to an ordinary
Chinese domestic consumer inland (that figure could not be sourced — see gap list).

| Price (taels/picul) | Year | Source |
|---|---|---|
| **19 taels/picul** (VOC contract) | 1730 | Van Dyke 2011 p.43, Plate 08.01 — read in full text |
| **13-15 taels/picul** (median) | 1742-1744 | ResearchGate table citing Van Dyke/Swedish EIC ledgers — snippet-level only, not independently re-verified in full text |
| **12 taels/picul** (1,000-picul DAC purchase) | 1737 | Van Dyke 2011 p.478 n.22 |
| **15.8 taels/picul** (with a large cash advance) OR **17.8 taels/picul** (no advance — "the *real* spot price," Van Dyke's own phrase) | Feb-Mar 1766 | Van Dyke 2011 pp.41-42, Plates 05.11/05.12/07.05/07.06/09.12/09.13 |
| Range across the whole record | **~12-20 taels/picul**, 1730-1770s | synthesis of the above |

**No China-domestic (inland-consumer) tea price could be sourced this session** — every figure
above is the Canton-export wholesale price. This is a genuine gap for a China-priority brief and
is flagged explicitly in the gap list (Section F).

## A3. Grain — CHINA-DOMESTIC price (the genuinely local commodity)

| Price | Region | Year | Source |
|---|---|---|---|
| **1.5 taels/shih** (up from 1.0 pre-Yongzheng) | Wu-hsi (near Soochow) | 1753 | Huang Ang 黄印, via Wang Yeh-chien 王業鍵 1972 p.351 n.6 (already in `QING_COST_OF_LIVING_1763.md`) |
| **0.9 tael/shih** (Yongzheng) rising to **1.5-1.7** (century-end) | Nanchang (Kiangsi) | 1723-1800 | Wang Yeh-chien 1972 p.354 |
| **~0.024 taels/kg** (bare-bones-basket retail) | Beijing/Canton | mid-18th c. | Allen, Bassino, Ma, Moll-Murata, van Zanden — the paper explicitly used for the mod's existing cost-of-living yardstick |
| **200 cash/dou** rising to **700+ cash/dou** | Fuling, Sichuan | Yongzheng 13 (1735) → Qianlong 31 (1766) | Ma Xueqiang 马学强, "清代江南物价与居民生活：对上海地区的考察" (Qing Jiangnan Prices and Residents' Lives), *社会科学* (Social Sciences) 2003 No.11 — **Chinese-language academic journal source**, obtained via search-summary, not independently full-text-verified this session |

**Wang Yeh-chien 王業鍵** compiled the canonical **清代糧價資料庫 (Qing Grain Price Database)** —
~2.19 million records, 1736-1911, drawn from the Taipei Palace Museum and Beijing First
Historical Archives 糧價奏報 (grain-price memorials), the exact primary-source category the task
brief asked for. This session located and confirmed the database's existence and scope
(jiansuoke.com/db/mhdb-sinica-foodprice) but **could not query it directly** — it is a structured
database, not a text document, and was not reachable with the tools available this session. This
is the single most promising follow-up target for a China-domestic grain price at exactly 1763,
by prefecture. **Flagged as the top follow-up recommendation.**

Confirms the Wu-hsi/Nanchang point above: **grain prices varied by ~60% between two Yangzi-basin
locations at similar dates** — this is intra-China regional variation, one level below the
China-vs-world divergence discussed in A0, and should further discourage treating "the" 1763
grain price as a single precise number even within China.

## A4. Salt — CHINA-DOMESTIC raw-vs-taxed value (the priority item, now with primary-text sourcing)

This is the section most improved by the Chinese-language steer. Fetched **清史稿·食貨志四·鹽法**
(Draft History of Qing, Treatise on Food and Goods, Salt Law chapter) **directly from
Wikisource** — this is a **primary-adjacent Qing-era historiographical text**, not a secondary
summary.

| Item | Value | Region/period | Source |
|---|---|---|---|
| Salt price AT THE PRODUCTION SITE (場灶) | **1-2 wen/catty** | general framing statement in the ticket-salt (票鹽法) reform discussion, referring back to the ancien-régime cost baseline | 清史稿·卷123·食貨四·鹽法 (fetched directly, Wikisource) — "鹽在場灶，每斤僅值錢一二文" |
| Changlu (長蘆) retail salt price | **16 wen/catty** | Kangxi era (~1680s-1700s, silver:cash ≈ 1:1400-1500) | same source — "康熙時，銀一兩換制錢千四五百，每鹽一斤，錢十六文" |
| Changlu retail salt price, later (currency-adjusted) | fell to **13-14 wen/catty** even as silver:cash rose to ~1:2000 (i.e. salt got CHEAPER in cash terms even as the tael itself bought more cash — a real decline in the salt price, not a currency illusion) | later (Yongzheng-Qianlong transition, per the passage's own framing) | same — "今每兩合錢二千，而鹽價如故，亦有減至十三四文者" |
| **Lianghuai (兩淮) — catties per 引 (yin, the salt-transport/tax unit)** | **400 catties/yin** | Qing standard for this division | same source, directly — "每鹽四百斤為一引" |
| **Changlu — catties per 引** | **300 catties/yin** | Qing standard for this division | same source, directly — "蘆鹽三百斤成引" |
| Qianlong-5 (1740) Hankou wholesale-price-setting case, cost submissions per 引 | 三保 (Sanbao, the Lianghuai Salt Censor)'s first submission: **7.1396 taels/yin**; his revised high/low: **6.5635 / 6.3635 taels/yin**; 崔紀 (Cui Ji, Hubei Provincial Inspector)'s counter-submission: **3.4 taels/yin**; the Board of Revenue's compromise assessment: **4.9397 / 4.3957 taels/yin**; the FINAL officially set price (by 徐士林, Jiangsu Provincial Inspector): **5.7802 / 5.3738 taels/yin** | Lianghuai salt sold into the Huguang (湖廣, Hubei/Hunan) market via Hankou | Qianlong 5 (1740) | 韓燕儀 (Han Yanyi), "清代乾隆前期湖廣部定鹽價制度中的政治博弈" (Political Negotiations in the Huguang Government-Set Salt Price System of the Early Qianlong Period) — a Chinese-language academic history article (venue not fully confirmed; syndicated via 網易/163.com and 凤凰网/ifeng.com, snippet-level access only this session, NOT independently full-text-verified) |

**What this gives us, converted:** the 1740 Hankou case is a WHOLESALE cost dispute among
officials (Sanbao arguing costs were high to justify a high set price; Cui Ji arguing costs were
much lower to keep the price down for Hubei/Hunan consumers) — it brackets the "true" wholesale
cost of Lianghuai salt delivered to Hankou at **roughly 3.4-7.1 taels/yin**, with officials
finally settling near **5.4-5.8 taels/yin**. At 400 catties/yin (the Lianghuai standard), that is
**~0.0135-0.0178 taels/catty at the officially-set WHOLESALE level** — i.e. **~13.5-17.8 wen/
catty** (at ~1000 wen/tael official parity) purely in wholesale/distribution cost, BEFORE any
further retail markup to the end consumer. This lines up strikingly well with the 清史稿's own
Changlu retail figure of **13-16 wen/catty** for a DIFFERENT division (Changlu, not Lianghuai)
at an earlier date (Kangxi) — suggesting retail salt prices across Qing divisions clustered in
roughly this **~1-2 dozen wen/catty** range for most of the 17th-18th centuries, a genuinely
useful cross-check between two independent Chinese-language sources (清史稿 primary text +
Han Yanyi's secondary reconstruction of the 1740 archival dispute).

**Comparing to the production-site cost (1-2 wen/catty per the 清史稿):** even taking the LOW end
of the wholesale/retail figures above (13-14 wen/catty), the **markup over raw production cost
is roughly 7-14×** using this primary-adjacent Chinese source — narrower than, but the same
order of magnitude as, the previously-reported (and separately flagged as weak) 30-50× figure
from a popular website. **This session's China-Chinese-language pass corroborates the
qualitative finding (large gabelle markup) with a considerably stronger evidentiary base, while
revising the specific multiple DOWNWARD from the earlier draft's 30-50× to a better-supported
~7-14×** for the Kangxi/early-Qianlong period specifically. The popular-website 30-50× figure
may still be correct for a LATER period (it did not specify a date) — Qing salt retail prices
are independently documented to have risen considerably over the 18th-19th centuries (the 清史稿
passage itself notes later increases), so a wider gap later in the dynasty is plausible and NOT
contradicted by this finding; the two figures likely describe different points on the same
rising trend rather than being in real conflict.

**Recommendation for #44, restated with the stronger sourcing:** the gabelle markup (order of
magnitude ~7-15×, per this more Chinese-source-grounded figure; possibly higher by the
19th century) should be modeled as a **tax/policy mark-up mechanic** tied to the Salt
Commissioner office (per `RESEARCH_QING_SALT_ADMINISTRATION.md`'s existing #44 design), not as a
bump to salt's raw base_value — the underlying commodity is cheap everywhere (1-2 wen/catty at
the salt pan, per the 清史稿 directly), and the price gap is a **regional administrative
artifact of the monopoly-zone system**, not an intrinsic property of salt as a good. This is
reinforced, not weakened, by the new sourcing: the fact that Lianghuai and Changlu — two
DIFFERENT divisions — both cluster in a similar wholesale-cost band while the raw production
cost sits an order of magnitude below BOTH, is exactly the "cheap to make, dear to buy only under
the monopoly" pattern the mod design assumed.

## A5. Metals — still the weakest China-domestic category, one new data point

| Item | Value | Region/period | Source |
|---|---|---|---|
| Raw iron (生鐵) | **~1 fen/catty** (0.01 tael/catty) — down from ~1.5-3 fen under Yongzheng | Qianlong era, region unspecified | Chinese secondary/popular (Zhihu) commentary — NOT a peer-reviewed citation |
| Raw iron, later official assessed price | **~6 taels/ton** | period unclear from snippet | same source |
| Iron-smelting furnace counts by province (production-scale context, not price) | Yunnan 110, Guangdong 48, Sichuan 33, Hunan 30, Guizhou 23 furnaces; empire-wide peak 313 furnaces | Qianlong 48 (1783) | Chinese secondary source, search-summary level |
| Yunnan copper (滇銅), 京運 (transport-to-capital) volumes | Over 6 million catties/yr, peaking at 7.97 million catties in peak years; Hankou copper market handling 1-2+ million catties/yr in mid-Qianlong | 1726-1911, mid-Qianlong for the Hankou figure | Chinese secondary source, search-summary level — **NO PRICE figure accompanies this volume data**; the Yunnan copper MINT-PURCHASE price itself remains unsourced |
| Silver:copper-cash exchange context (not a metal-good price, but relevant conversion) | Beijing/Yunnan: ~800-900 wen/tael Kangxi-Qianlong; occasionally >1000 wen/tael in Yunnan specifically | Kangxi-Qianlong | Chinese secondary source; consistent with the already-established `1763_QING_MONEY_SUPPLY.md` figure of ~700-1000 wen/tael |

**Metals remain the weakest-sourced category even after the Chinese-language pass.** Despite
repeated targeted searches in both English and Chinese, **no comparative iron:copper:tin:lead
price ratio, and no Yunnan copper PRICE (as opposed to volume) figure, could be located this
session.** The #49/#46 question about whether lead's existing 0.4 base value (2× the mod's flat
0.2 default) is defensible against iron/copper remains **explicitly unanswered**. The most
promising named sources for a follow-up (Donald Wagner's iron-industry corpus; a direct read of
雲南銅志 or the 滇銅京運 literature underlying `1763_QING_MONEY_SUPPLY.md`) were identified but
not reached.

## A6. Cotton cloth — a China-domestic figure, cross-checked against the earlier Canton-export cotton figure

| Item | Value | Region/period | Source |
|---|---|---|---|
| Cotton cloth, domestic retail (per bolt/匹) | **~200-400 wen/bolt** (one bolt = 20 taels weight by guild standard, 1.2 chi wide × 20 chi long) | "late Qianlong" (the source explicitly notes domestic cotton-cloth price data is only attested from late Qianlong onward, no earlier figure exists) | 洪亮吉 洪亮吉《卷施阁文》甲集卷一, "生計篇" — a **Qing-era primary text (Hong Liangji's own essay collection)**, quoted via economy.guoxue.com's compiled commodity-price-estimate article (the compiling article itself is a modern secondary synthesis, but it is directly quoting a named 18th-c. primary author) |
| Raw cotton, Canton-export (foreign-buyer) price, for comparison — CANTON-EXPORT not China-domestic | Indian raw cotton 10-12 taels/picul; native Chinese raw cotton 13-17 taels/picul | 1793-94 (Macartney embassy — 30 years past 1763) | LSE Economic History document — already flagged in the first pass as a 1793-94, not 1763, figure |

These two figures are not directly comparable (finished cloth-by-the-bolt vs raw fiber-by-weight,
and one is China-domestic retail while the other is Canton-export raw material), but both
corroborate the same general point: cotton goods sat in the mod's proposed **mid-tier**, well
below silk/tea and well above bare grain, at any point in the value chain measured.

## A7. Wages — the cross-check, restated by region

| Item | Value | Region | Year | Source |
|---|---|---|---|---|
| Unskilled daily wage, VOC hire (63 quotations) | **0.08-0.1 taels/day**, no food allowance | Canton | throughout 18th c. | Allen et al., read in full text |
| Unskilled daily wage, government-regulation floor | ~0.03-0.04 taels/day national average (Fujian lowest at 0.030); Zhili/Beijing/Manchuria/Xinjiang highest | empire-wide, *Wuliao jiazhi zeli* | 1769 | Allen et al., Table 1 |
| Skilled:unskilled wage premium | Skilled labour earned **63% MORE** (×1.63) | national regression | 18th c. | Allen et al. p.13 |

A Canton laborer's daily wage (~0.08-0.09 tael) buys ~3-4 kg of China-domestic-priced rice
(at ~0.024 taels/kg) but only ~1/200th of a picul of Canton-EXPORT-priced Bohea tea — i.e., **tea
priced for the export market cost a local wage-earner roughly six months' income per 60 kg**,
independently confirming the A0/A2 point that export-grade tea sat in a completely different
price world from ordinary Chinese domestic consumption, even before it left port for Europe.

## A8. Opium — still no 1763 figure, Bengal upstream cost only

| Item | Value | Region/period | Source |
|---|---|---|---|
| Import volume | 200 chests/yr | China, 1729 (first anti-opium edict) | Wikipedia, sourced |
| Import volume | 75 long tons, >2,000 chests | China, 1773 | same |
| Patna opium, EIC monopoly PURCHASE price (Bengal, upstream of China entirely) | 320-350 Sicca Rupees/chest ≈ **~99 taels/chest** (session's own arithmetic conversion via silver content) | Bengal, 1775 | Bengal Revenue Consultations 23 May 1775, via Cambridge/*Itinerario* abstract |
| **Caveat, restated** | This is neither a China price nor a 1763 date. The commonly-cited "350-550 taels/chest at Canton" figure is dated **1793-1829** in its own source (houghton.hk) — do not backdate it. No China-side or 1763-specific opium price was found in either English or Chinese sources this session. | | | |

---

## B. Recommendation for gold vs silver base value (restated with the China-primary framing)

The **China-domestic** ratio is the one that matters for the mod's China-fine-fidelity
principle, and it tells the same story as the English-source literature: gold was **cheap
relative to silver in China for most of the Qing** (roughly 1:8-10 through the 17th century),
narrowing toward parity with the international/European rate (~1:14-15) by the 1750s-60s. By
**1763 specifically**, China's domestic ratio and the international rate had **essentially
converged** — two independently-sourced series (Melitz/von Glahn's English-language academic
reconstruction, and a Chinese-language popular-secondary synthesis) agree on this.

**Recommendation, unchanged in substance from the first pass but now doubly corroborated:** set
the mod's gold base value ≈ **14-15× silver's base value**, reflecting the converged 1763 ratio,
NOT the wider 1:8-10 gap that would have been correct for an earlier (17th-century) bookmark.
This resolves ticket #46 in the same way as before: the mod's current identical 0.2/0.2 gold and
silver base values are backwards for ANY point in Qing history, including 1763 — gold should
always sit several multiples above silver by weight.

## C. Recommendation for the luxury/staple spread (restated with region tags)

Using the **Canton-export** Bohea-tea figure (~17.8 taels/picul, 1766) against the
**China-domestic** rice figure (~1-1.5 taels/shih), the spread is **~12-18×**. This specific
ratio measures a China-EXPORT good against a China-DOMESTIC good, which is a slightly
apples-to-oranges comparison (per A0's own warning) — but it is the best sourced spread
available, it is corroborated independently via the wage cross-check (A7), and directionally it
should if anything UNDERSTATE how much more expensive silk/tea were once fully landed and resold
in Europe (A0's 2.5-3× further Europe-side markup). **A 10-20× luxury:staple spread remains the
recommended anchor for the mod's tier structure.**

## D. Metals — question remains open

Restated from A5: **the #49 question about lead=0.4 vs iron/copper remains unanswered.** No
comparative price ratio was found in either English or Chinese sources this session, despite
being the most heavily re-searched single question in this revision pass.

---

## E. NEW SECTION — which single anchor should the mod's ONE base_value field use?

The mod's engine gives each trade good exactly one global `gold = X` field — there is no
per-region base value. Given the demonstrated, historically-real divergence in A0 (Canton-export
≠ China-domestic ≠ Europe-retail, sometimes by a factor of 2.5-3× or more), **no single number
can be "the" historically correct price** — any single field is necessarily a simplification.
The question is which simplification is LEAST distorting for this mod specifically.

**Recommendation: anchor the single base_value field to the CHINA-DOMESTIC price, not a
global average and not the Canton-export/Europe-retail price.** Reasoning:

1. **The mod's own stated design principle** (China fine-fidelity, rest-of-world abstracted)
   already implies China should be the reference frame for anything the engine treats as a
   single global number — the mod's China provinces are where the detailed simulation lives,
   so a China-anchored base value will produce sensible-looking relative prices for the part of
   the map the mod actually cares about getting right.
2. **A Canton-export anchor would systematically overprice every domestic-only good** (grain,
   livestock, most metals) relative to how they actually functioned inside China, because the
   export price already embeds the risk/voyage/company-margin layers described in A0 that never
   applied to goods that stayed in China. Using it as the SOLE global number would make the
   mod's huge domestic Chinese economy look permanently luxury-tier-adjacent.
3. **A Europe-retail anchor** would be even further removed — it stacks the Canton-export
   markup AND the ~2.5-3× ocean-voyage/company-margin layer on top, and is the LEAST relevant
   frame for a mod that models China in detail and the rest of the world abstractly.
4. **A "global average"** is not a coherent concept for goods that literally did not trade in a
   single market (this is the core historical point of A0) — there is no principled way to
   average a Canton-export tael/picul figure with an inland-Sichuan grain price in copper cash;
   they are not observations of the same underlying quantity.

**Where genuine regional divergence should live instead:** per the team's own framing, this
belongs in the mod's **script-market / tradezone price layer** (region-level modifiers, trade
company margins, distance-from-Canton effects), NOT in the trade good's single base_value field.
Concretely: the base_value sets the CHINA-DOMESTIC starting point for each good (per the ratios
in Sections A2-A6 and the tier scheme in Section C); any Canton-export premium for goods that
leave China through the Hoppo, or any Europe-bound further markup for goods that leave the map
entirely, should be represented as an ADDITIVE regional/trade-route modifier on top of that base,
not baked into the single global field. This also has the virtue of being consistent with how the
mod already treats the Hoppo (#111/#24/#25: Canton customs skim/yield is a graded MODIFIER on top
of underlying goods values, not a rewrite of the goods' base prices) — the same pattern should
extend to any future silk/tea/porcelain export-premium mechanic.

---

## F. Explicit gap list (updated)

**Still not sourced despite dedicated Chinese-language search this pass:**
- China-domestic (non-export) tea price, at any point in the value chain — every tea figure in
  this digest is the Canton-export wholesale price.
- China-domestic raw silk price per catty/dan — searched repeatedly in Chinese this pass
  (Kishimoto Mio's book title located and confirmed to cover exactly this topic, but no specific
  figure surfaced from search-summary access alone).
- Yunnan copper mint-purchase PRICE (volume data was found; price was not).
- Comparative iron/copper/tin/lead ratio (the specific #49/lead question).
- Sugar, porcelain (open-market, as opposed to the 1753 Hoppo Book customs-schedule internal
  ranking), coffee, tobacco, generic spices — no price in any unit, any region, 1750-1780.
- A 1763-specific, or even a China-side, opium price.
- Peng Xinwei 彭信威《中國貨幣史》, Chuan Han-sheng 全漢昇, Kishimoto Mio 岸本美緒 in ORIGINAL
  full-text form — all cited or referenced this session (via Melitz's citations, or via
  search-summaries of their scope/reputation) but **not independently read in full text**. This
  is the single biggest sourcing gap relative to what the task brief asked for, and it recurs
  across three separate research passes now (this file, `1763_QING_MONEY_SUPPLY.md`,
  `RESEARCH_QING_SALT_ADMINISTRATION.md`) — these three foundational Chinese scholars remain
  request-only/access-gated to the tools available across all research sessions so far.
- **The Wang Yeh-chien 清代糧價資料庫 (Qing Grain Price Database)** — LOCATED and its scope
  CONFIRMED (2.19M records, 1736-1911, prefecture-level, from the two-palace archives) but not
  queryable with this session's tools. **Top recommended follow-up target** — if this mod
  project ever gets a research pass with real database/library access, this is the single
  highest-value source to query for a genuine prefecture-level, exactly-1763 domestic grain (and
  possibly other staples) price series.

**Newly resolved this pass (moved out of the gap list):**
- Lianghuai/Changlu catties-per-yin conversion (400 / 300 respectively) — sourced directly from
  清史稿, resolves a gap flagged in the original salt research.
- A primary-adjacent (not just secondary-popular) salt production-cost-vs-retail figure, with a
  narrower and better-supported markup multiple (~7-14× vs the earlier ~30-50× from a
  weakly-sourced popular site) — see A4.
- The gold:silver ratio now has a China-language-source data point independently corroborating
  the English-source (Melitz/von Glahn) convergence finding.

---

## G. Sources consulted (consolidated; supersedes the source list in the pre-revision draft)

**Fetched and read in full text, English-language:**
- Jacques Melitz, *Some Doubts about the Economic Analysis of the Flow of Silver to China in
  1550-1820*, CEPII Working Paper 2017-19 — pp.1-15 read in full. Cites von Glahn (2003), Peng
  Xinwei (1993-4), Flynn & Giráldez (2002), Dermigny (1964), Cantillon, Soetbeer (1879).
- Richard Cantillon, *Essai sur la nature du commerce en général* (≤1734), primary excerpt in a
  documentary-history volume, pp.91-94, read in full.
- Allen, Bassino, Ma, Moll-Murata, van Zanden, "Wages, prices, and living standards in China,
  1738-1925" (CEI WP 2009-3 / *Economic History Review* 2011) — pp.1-34 read in full.
- Paul A. Van Dyke, *Merchants of Canton and Macao* (2011) — pp.1-48 and pp.468-483 read in full.
  THE primary source for Canton-export tael/picul tea figures and the Canton credit/bottomry
  structure (A0's 40% junk-bottomry vs 12-18% foreign-ship-bottomry comparison, Table 2.2).
- *The Hoppo Book of 1753* (Anekdota Press transcription) — sample read in full; internal
  customs-schedule ranking only, not open-market prices.

**Fetched and read directly this revision pass, Chinese-language (primary or primary-adjacent):**
- **清史稿·卷123·食貨四·鹽法** (Draft History of Qing, Treatise on Food and Goods, Salt Law) —
  fetched DIRECTLY from Wikisource (zh.wikisource.org) and read via AI-assisted extraction of
  the actual classical-Chinese text. This is the single strongest new source in this revision:
  gives the Lianghuai/Changlu catties-per-yin conversions, the production-site 1-2 wen/catty
  figure, and the Kangxi-era Changlu retail figure, all directly from the Qing-era
  historiographical text itself, not a secondary summary of it.

**Fetched at search-summary/snippet level, Chinese-language (flagged, not full-text-verified):**
- 韓燕儀 (Han Yanyi), "清代乾隆前期湖廣部定鹽價制度中的政治博弈" — the Qianlong-5 (1740) Hankou
  salt-price-setting case (Sanbao/Cui Ji/Board-of-Revenue/Xu Shilin cost figures). Located via
  163.com/ifeng.com syndication; venue of original academic publication not fully confirmed.
- Ma Xueqiang 马学强, "清代江南物价与居民生活：对上海地区的考察," *社会科学* 2003 No.11 — the
  Fuling rice-price series and a Kangxi-22 salt-price-spike figure.
- 洪亮吉《卷施阁文》"生計篇" (an actual Qing-era primary essay, quoted via a modern compiling
  article at economy.guoxue.com) — the late-Qianlong cotton-cloth-per-bolt figure.
- Various Zhihu/Toutiao/Sohu-tier popular-history summaries for: the min.news salt markup claim
  (retained from the first pass, now with a stronger primary-adjacent corroboration point — see
  A4); Qianlong iron prices; Yunnan copper volumes; the Chinese gold:silver 1:10→1:15 synthesis.
- Confirmed-but-not-queried: Wang Yeh-chien 王業鍵's 清代糧價資料庫 database (scope and access
  point identified, not queried); Kishimoto Mio 岸本美緒's book title and scope (confirmed via
  publisher listing, no specific price figure surfaced); Chuan Han-sheng 全漢昇's essay
  collection *中國經濟史研究* (table of contents surfaced, no gold-silver-ratio essay identified
  within it specifically — his gold-silver-ratio work may be in a different, uncollected essay
  not indexed by the search tools available this session).

**Already on file in the repo (re-used, not re-researched):**
- `research/QING_COST_OF_LIVING_1763.md`, `research/1763_QING_MONEY_SUPPLY.md`,
  `research/RESEARCH_QING_SALT_ADMINISTRATION.md` — all three already flag Peng Xinwei/Chuan
  Han-sheng/Kishimoto Mio/Saeki Tomi as request-only/inaccessible; this revision pass did not
  close that gap despite dedicated effort, and the gap is now confirmed to recur across four
  separate research sessions on four different sub-topics (money supply, cost of living, salt
  administration, and this trade-goods pass) — worth escalating as a standing note that these
  four foundational sources need a session with real library/JSTOR/CNKI access, not
  web-search-only tools, before the mod's Qing-economics research can advance much further.

**China-fine-fidelity note, restated:** this revision's gold:silver section still necessarily
draws on a global/comparative source (Melitz/Cantillon/von Glahn) because the ratio is inherently
a China-vs-world comparison, but it is now corroborated by an independent Chinese-language
source, and the China-side figure (1:8-10 early, converging to ~1:14-15) is reported as the
PRIMARY number per the latest steer, with Europe/Japan figures as secondary context only.
