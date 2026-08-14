# Qing Board-of-Revenue Silver Reserve 戶部銀庫存銀 — Sourced Figures

戶部銀庫存銀 (Board of Revenue central silver treasury balance), in 萬兩 (10k taels), sourced from 《清代户部银库收支和库存统计》(史志宏) + 陶庐杂录 卷1 (軍機大臣 1775 memorial on 康雍乾年間 annual balances). Used for #372 (Ministry of Revenue silver-reserve event chain to historical peak).

> **[2026-08-13 CORRECTION]** The original 乾隆28/1763 entry below (~6200萬兩) was WRONG — it was
> transcribed from the wrong row of the underlying multi-year table. 6200萬兩 actually belongs to
> **雍正8年 (1730)**, not 1763; a nearby "~4700萬兩" figure some sources cite belongs to **康熙47年
> (1708)**, also not 1763. The correct 乾隆28年/1763 figure, confirmed by 2 independent secondary
> sources both explicitly citing 史志宏's book (a curated 2025 Chinese exam-board historical table,
> mirrored across ≥4 unrelated exam-prep sites, and a 2021 pop-history article giving the full
> 1760-1765 run), is **47,063,611兩 (钱271串)** — corrected in the table below.
>
> The 乾隆42/1777 PEAK figure (8182萬兩) is NOT affected by this correction and remains verified:
> the same primary-source lineage (陶庐杂录 卷1's 1775 軍機處 memorial) that confirms the corrected
> 1763 figure also gives 1777's full ledger breakdown (旧管7466萬+新收1811萬-开除1095萬=实在8182萬),
> independently corroborating the existing peak constant. `qing_silver_reserve_peak = 81820`
> (se_QING_REVENUE.txt) is UNCHANGED and remains correctly sourced.

- 康熙61 (1722): 2716
- 康熙47 (1708): ~4700 (previously mis-cited as belonging to 1763 — see correction above)
- 雍正8 (1730): ~6200 (previously mis-cited as belonging to 1763/乾隆28 — see correction above)
- 雍正末 (1735): 3453
- 乾隆元 (1736): 3000
- 乾隆20 (1755): ~5200–5500 (interpolated)
- 乾隆25 (1760): 3549.7
- 乾隆26 (1761): 3663.9
- 乾隆27 (1762): 4192.8 (钱909串)
- **乾隆28 (1763, GAME START): 4706.4** (47,063,611兩, 钱271串; ~57.5% of peak) — the corrected seed value
- 乾隆29 (1764): 5427.4
- 乾隆30 (1765): 6033.6
- 乾隆42 (1777): **8182 = the PEAK** (well-documented, independently corroborated — unaffected by the 1763 correction above)
- 乾隆60 (1795): 6939 (handover to Jiaqing)
- 嘉慶元 (1796): 5600
- 嘉慶4 (1799, Qianlong dies + Heshen falls): ~2000 (嘉慶中衰)
- 嘉慶25 (1820): 3121
- 光緒 late: <1000

Trajectory for modelling: smooth, monotonic rise from the corrected 1763 figure (4706萬) through
1777's peak (8182萬) — no discontinuity, consistent with the post-Ten-Great-Campaigns fiscal
recovery — then plateau ~1777–85, then ~70/yr drain 1777→1795 (later Ten Campaigns, White Lotus,
和珅 corruption). Reserve is DISTINCT from the abstract qing_currency_stress meter (0=sound)
already in the revenue panel; #372 adds a concrete 萬兩 balance. Modelled in se_QING_REVENUE.txt /
QING_revenue_pulse; peak-milestone + decline events in qing_revenue_events.

_Migrated from memory imp19c-silver-reserve-figures, per the research-digest-location rule._
