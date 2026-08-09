# Qing granary capacities — sourced research digest (2026-08-09)

For #94/#95 (Capital Grain Reserve / canal on real food) and the proposed 京倉/通倉 capital-granary
building. Discipline: sourced figures only; primary vs estimate distinguished; gaps flagged, not invented.

## Findings

### 常平倉 ever-normal granaries, empire-wide — STRONGEST result
- Pre-1748 (Qianlong 13) peak: **48,118,350 shi**
- Daoguang 15 (1835): **~24,000,000 shi**
- Source: Liu Ts'ui-jung (劉翠溶), "清代倉儲制度穩定功能之檢討," 經濟論文 (Economic Papers) 8:1 (Mar 1980),
  pp. 1-31, citing primary 《大清會典事例》 juan 190:5b / 192:8b (via secondary reproduction; original
  not directly verified).
- CAVEAT: these are almost certainly **nominal quota (額儲)** figures, not audited physical stock
  (He Weiguo 和衛國, 清史研究 2019 no.2). Not cross-checked against Will & Wong, *Nourish the People*
  (1991) — that source was access-gated (JSTOR/IA).

### 漕糧 tribute grain, annual throughput — INDICATIVE only
- **~4,000,000 shi/year** (Qing) — attested but only at tertiary depth (中文 Wikipedia 漕運, Baidu 漕粮);
  best corroboration a gazetteer quote 《西江志》 "本朝漕額計四百萬石" (edition/juan unverified).
- The often-quoted **"~400,000 tons"** figure is **Ming** (15th-16th c., transportgeography.org, itself
  uncited) — do NOT reconcile it with the Qing 4M-shi figure; different dynasty/century.
- No named Western-scholar page-cited Qing confirmation found (Hoshi Ayao's tribute-grain work, as
  accessible, is framed Ming).

### 京倉/通倉 capital / Tongzhou granaries — GENUINE GAP
- **No defensible Qing-specific capacity/stock figure sourced.** The "capital granaries ~4M shi" number
  turned out to be **Ming** (《明史·食貨志》). Only institutional facts found (early Shunzhi: 8 capital + 3
  Tongzhou granaries → the "京通十三倉" / 17 granaries by Qianlong), from popular web history, not peer-reviewed.
- Qing-specific numbers found were only event-level relief withdrawals (100k-400k shi drawn from Tongzhou
  in a famine episode; year/source unverified) — order-of-magnitude, not a capacity.
- CONSEQUENCE: a 京倉 building's per-level capacity cannot be anchored to a sourced absolute. Anchor it
  RELATIVELY (e.g. to the ~4M-shi/yr 漕糧 flow it buffers) and LABEL it a game-balance figure — not a fake cite.

### Unit conversion
- 1 Qing **shi** (grain volume unit, 石) ≈ **103.5 litres** (2 斛 / 10 斗 / 3,160 cubic cun; 中國度量衡 refs).
- This is the VOLUME shi — distinct from the **weight dan/picul** (120 jin ≈ 70.8 kg, a general-goods unit).
  Conflating volume-shi and weight-picul is a common trap. No sourced shi-of-rice→kg conversion found
  (would require rice bulk density ~0.75-0.85 kg/L = unsourced arithmetic).

## Use in the design (see design/DESIGN_GRAIN_FOOD_VALUE_94_95.md §5e)
- Ever-normal pool math stays on its game-abstract count×200 unit (NOT shi); 48.1M-shi usable as FLAVOUR/loc.
- Capital 京倉 capacity: relative/balance-anchored (flow-based ~1yr tribute, or the code's 200-basis scaled),
  labelled as balance, not sourced stock.
- Express the capital reserve in the engine's state-food unit (the natural common scale); shi figures in
  tooltips as flavour with the nominal-quota caveat noted.
