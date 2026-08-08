# 1763 Qing money supply (M1 / circulating currency) — research digest

**For:** #71 (basis for the CHI M1 seed = 46.14M chuan, se_CURRENCY.txt:229-231) and #23 (currency swing).
**Date:** 2026-08-08. **Status:** partial — exchange rate + annual mint output SOURCED; total circulating
STOCK still unpinned (needs Peng Xinwei / Vogel in-text reading).

## The headline correction (retracts the earlier "46M is 14× too high" hypothesis)

The "~3.2 billion wén" cursory figure is **annual MINT OUTPUT, not the circulating STOCK.**
- Qianlong-era central+provincial mints produced **~3 billion good copper coins per YEAR**, averaged over
  1735–1795 (Xiaoyu Gao, U. Chicago — AHA 2026 "Minting Trouble in Copper Coins"; SSHA 2026 "The Cash Trade").
- ÷ nominal 1,000 wén/string ≈ **~3 million strings (chuan) per year** of output.
- Scale check: Shunzhi Beijing ministry quota ~400k strings/yr; Jiaqing quota 2,586,000 strings/yr (rarely
  met) — Qianlong ~3M strings/yr sits consistently above these (Wikipedia, *Qing dynasty coinage*).

=> The total money STOCK in circulation is a LARGER, currently-unpinned multiple of one year's output
(coins stayed in use for decades). So:
- Comparing the mod's 46.14M chuan seed against 3.2M chuan (one year's mint) is an **apples-to-oranges
  error** — 3.2M is a flow, 46M is meant to be a stock.
- The earlier inference "46M is ~14× too high" is **RETRACTED** — it rested on treating annual output as
  the stock. The real stock could plausibly be tens of millions of strings; 46M chuan is NOT obviously
  wrong and may be reasonable. Cannot confirm either way without the accumulated-stock figure.

## Exchange rate mid-Qianlong (SOURCED, clean — and opposite the 19th-c. crisis)

- **Official / statutory: 1,000 wén = 1 tael of silver** (ChinaKnowledge.de "Qing Period Money"; Wang
  Hongbin 王宏斌 2015 《清代价值尺度：货币比价研究》 SDX; Springer *Monetary System of China under the Qing*).
- **Actual market rate ~1750s–1800: copper STRONG, ~700–800 wén per tael** (ChinaKnowledge: "until c.1800
  the exchange rate was in practice 1:7–800"; Wikipedia *Qing dynasty coinage*: could fall to ~700 wén/tael).
- This is the **inverse** of the later silver crisis: von Glahn & So (2017) — Hebei ~1,250 wén/tael in 1820,
  ~2,300 by 1850. For a 1763 model, peg **~800 wén/tael market (1,000 official)**, silver relatively cheap.

## Silver stock c.1763 (secondary; from the existing repo digest, already sourced)

From `research/1763_CANTON_SILVER_INFLOW.md` (do not re-research — user confirmed the reserve number is fine):
- Total monetized silver stock ~15,000 tons c.1750 (Cao & Flynn 2020) ≈ order ~560M taels (rough).
- ~20,270 tons accumulated via trade surplus (Deng 2008). Net 18th-c. inflow ~130–190 tons/yr.
- Copper cash was **<20% of total money by VALUE** (silver dominated value; copper dominated everyday
  transaction COUNT) — Wikipedia *Qing dynasty coinage*.

## The mod's unit — reconciliation still needed

Mod: currency = Chuan, `backing_type = silver_standard`, `units_to_the_lb = 14`; M1 seed 46.14M chuan;
silver reserve 20,000 (hundreds-lb) = 2,000,000 lb. `CURRENCY_wealth_value_from_silver = country_unit_price_silver × 16`,
`wealth_value_1_unit = that ÷ 14`. So the mod pegs 1 chuan to a silver weight, NOT explicitly to ~1000 wén.
Historically 1 chuan ≈ 1,000 wén ≈ ~1.25–1.4 tael (at ~800 wén/tael market) — but the mod treats chuan as a
silver-pegged unit directly. Whether 46.14M silver-pegged-chuan corresponds to a defensible 1763 stock
depends on the unpinned copper-stock figure AND how the mod's chuan maps to a tael. UNRESOLVED.

## STOCK ESTIMATE (2nd research pass, 2026-08-08) — the missing number, DERIVED

No single published "1763 stock = X strings" figure exists in any reachable source (Peng Xinwei's copy
is access-restricted — only his 1900 table surfaced; Vogel's year-by-year Tables 10/18/21 are absent from
the free abbreviated diss). So the honest deliverable is a DERIVED estimate:

**~250-500 BILLION wén ≈ 250-500 MILLION strings (chuan), central point ~300 million chuan, mid-Qianlong.**

Method: empire-wide annual output × multi-decade coin lifetime.
- Annual output anchors: central mints (寶泉局+寶源局) ~4M strings/yr in the 1750s-60s (Vogel — this is the
  "~3-4 billion coins/yr" flow, NOT stock). EMPIRE-WIDE (central + provincial) "always beyond 10 million
  strings" late-18thc (Wang Yeh-chien 王業鍵, via Horesh 2020 p.318). Circulating stock uses the empire-wide flow.
- Coin lifetime: durable bronze/brass, circulated decades, net of melt/loss/hoard/export. 30-70yr life on
  ~10M strings/yr → 300-700B wén; conservative for mid-century (output below the late-18thc peak) → ~250-350B wén.
- Cross-check: Kuroda 黒田明伸 — Chinese small copper minted "in the hundreds of billions" (qualitative match).

TWO CORRECTIONS from this pass:
1. The famous "260 billion coins" figure is SONG (von Glahn 2016, Econ History of China, Table 6.9), NOT Qing.
   Do not use it for 1763.
2. Good 制錢 vs private/debased 私錢: around 1763 the good-cash fraction was relatively HIGH — irreversible
   debasement set in only c.1835+ (Vogel); private-mint share GREW after mid-century (Horesh p.258). No clean
   1763 ratio available.

### IMPLICATION FOR THE MOD SEED (reverses the earlier worry)
Historical M1 ≈ ~300 MILLION chuan. Mod seeds **46.14 million chuan** (se_CURRENCY.txt:229-231).
=> The seed is ~6-7x TOO LOW, not too high. (The original "14x too high" worry was based on mistaking
annual output [3.2bn wén] for the stock — RETRACTED; the stock is ~100x the 3.2bn-wén annual-mint figure.)
Mod China runs on ~1/7 of its real money supply. NOTE: a mod M1 is not obliged to equal historical M1
(it is a game abstraction and interacts with private_cash_needed scale + the #23 ratio), so this is a
FLAG for the #23 rebalancing, not an automatic "set it to 300M". Any M1 change = Sobisonator-caution +
must be tuned jointly with #23 (M1 is the ratio numerator; ~6-7x-ing it shifts every inflation/deflation
reading) and with units_to_the_lb (#72, now 8).

## YAN HONGZHONG 燕红忠 — the CANONICAL published series (3rd pass, 2026-08-08) — best source

Primary: **燕红忠《从货币流通量看清代前期的经济增长与波动》,《清史研究》2008(3): 24-43** (Yan Hongzhong,
"Economic Growth and Fluctuation in the Early Qing from the Perspective of Monetary Circulation"). Covers
1651-1860 (brackets 1763). Corroborated/reused by Xun Yan, LSE PhD thesis 2015 (etheses.lse.ac.uk/3307/),
Appendix D-1-1 p.80, "Total money in circulation in China 1644-1860 (millions of silver taels & millions of
copper cash strings)", redrawn directly from Yan (2008) p.33.

Yan's TOTAL money stock (silver+copper, in 亿两 = 100M taels; FIXED silver:copper = 3:1; ~1000 wén/tael):
- late-Ming base 2.0亿两 (copper = 5000万串 = ~50M strings); 1651-60 ~2.85亿两; 1700 trough 2.33亿两;
  fastest-growth phase 1721-1780; **1781-90 PEAK 6.9亿两**; 1790-1800 4.61亿两; 1810-30 5.7亿两.
- **1763 (interpolated across the 1700-trough → 1781-peak ramp): ~4.5-5.5亿两 ≈ 450-550 MILLION TAELS total M1.**
  (Exact 1761-70 cell is image-only in his Tables 3-5 / Figure 1; interpolation flagged.)
- Method: copper built from mint casting records (Burger's Qianlong data) + provincial share + 10%/decade
  cash depreciation; silver via the 3:1 ratio + rice-purchasing-power. (Depreciation is why Yan's copper
  leg is LOWER than the naive output×lifetime derivation above.)

CONVERSION TO THE MOD'S CHUAN (Yan's own anchor: 1 tael ≈ 1 string ≈ 1000 wén):
- **Copper-cash-only leg ~1763 ≈ (4.5-5.5亿两)/4 ≈ ~110-140 MILLION CHUAN of 制錢.**
- **Total M1 (silver+copper) ≈ ~450-550 MILLION string-equivalents.**

### VERDICT vs the mod's 46M-chuan seed (supersedes the earlier derived ~300M)
Depends on what the mod's "chuan" M1 represents:
- COPPER-CASH-ONLY → Yan ~110-140M chuan → seed is ~2.5-3x TOO LOW.
- TOTAL M1 (silver+copper) → Yan ~450-550M → seed is ~10x TOO LOW.
Yan's copper-only ~110-140M is ~half the digest's naive ~300M (he applies 10%/decade depreciation — better
method; supersede the ~300M with Yan's ~125M copper / ~500M total). User's ~260M eyeball sits between.
Either way the seed is too low; the apples-to-apples copper figure is **~110-140M chuan**.

IMPLICATION FOR #23 unchanged: any M1 rebase is Sobisonator-caution + must be tuned JOINTLY with #23 (M1 is
the ratio numerator) and units_to_the_lb (#72=8). Recommend: if the mod chuan = copper cash, rebase toward
~120M; if total M1, toward ~500M. Decide which the engine intends before changing (the silver_standard
backing + separate silver_reserve suggests chuan = the CIRCULATING copper-ish medium, i.e. the ~120M leg).

## GAPS — what to get next (needs direct in-text reading, ideally CJK-capable)
1. **Accumulated copper-cash STOCK in wén/chuan c.1763** — THE missing number. Best sources, both with free
   full text:
   - Peng Xinwei 彭信威 《中國貨幣史》 (1954; Kaplan trans. 1994) — archive.org/details/monetaryhistoryo00peng_0
     and centerforfinancialstability.org. Has cash-circulation + silver-stock estimates in-text.
   - Hans Ulrich Vogel, *Chinese Central Monetary Policy and the Yunnan Copper Mining Industry 1644–1800*
     — academia.edu/4263409, archive.org/details/IA41507227_0030. Mint-output + stock tables.
2. **Decade-specific 1750s–60s market rate pinned to a named scholar** (only have the general "1:700–800").
3. **Chuan Han-sheng 全漢昇 / Kishimoto Mio 岸本美緒** figures — need JSTOR/library.

## Citations
Xiaoyu Gao AHA 2026 (aha.confex.com/aha/2026/webprogram/Paper41338.html) + SSHA 2026 (ssha2026.ssha.org/abstracts/260775);
ChinaKnowledge.de "Qing Period Money"; Wikipedia *Qing dynasty coinage* & *Economy of the Qing dynasty*;
Wang Hongbin 王宏斌 2015; von Glahn & So 2017; Peng Xinwei 彭信威 1954/1994; Cao & Flynn 2020; Deng 2008; von Glahn 2013.
**Yan Hongzhong 燕红忠《从货币流通量看清代前期的经济增长与波动》《清史研究》2008(3):24-43, esp. p.33 (the canonical series)** —
also 燕红忠《货币供给量、货币结构与中国经济趋势：1650~1936》《金融研究》2011(7). Corroborated by Xun Yan, LSE PhD thesis 2015
(etheses.lse.ac.uk/3307/), App. D-1-1 p.80 (redrawn from Yan 2008 p.33). Burger's Qianlong mint data underlies Yan's copper series.
