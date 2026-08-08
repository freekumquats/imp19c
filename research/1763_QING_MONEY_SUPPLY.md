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
