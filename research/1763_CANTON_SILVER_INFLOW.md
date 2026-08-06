# Canton silver inflow & 戶部銀庫 reserve — sourced figures (1700–1840)

Research digest (2026-08-06) for calibrating the Canton→silver-reserve feed
(design/DESIGN_CANTON_SILVER_RESERVE.md §5) and auditing the mod's existing
戶部銀庫 seed/peak figures (se_QING_REVENUE.txt, se_CURRENCY.txt). Academic
sources, citation counts noted where available.

## 1. Net silver inflow (annual)
- **129 tons/yr** Europe→Asia, first half 18th c. — Cao & Flynn (2020), *Revista de Historia Económica* (Cambridge).
- **190 tons/yr** into China's money supply, 18th c. — Von Glahn (2013), "Cycles of silver in Chinese monetary history."
- **350 tons/yr** avg over 250+ yrs — Irigoin (2020), *Handbook of History of Money and Currency* (Springer).
- **~700 tons/yr** fine silver globally, ~70% to Asia — Irigoin (2018), MPRA.
- Canton-specific: **~3,000 tons total** landed 1800–1830 — Deng (2008), *Pacific Economic Review* (cited 52).
- Manila galleon: <1M pesos/yr (1719–26) → **3.5M pesos/yr** by mid-18th c. — Von Glahn (2020).

## 2. Trade composition / balance
- Tea: **23M lb/yr** by end-18th c. (Flynn & Giráldez 2002, *J. World History*, cited 389); **30M lb/yr avg 1800–42** with **$7M** silver bullion shipped (Greenberg 1969, *British Trade and the Opening of China*).
- Europeans "required to export silver from Europe to pay for their tea"; payments **min 24% in silver** — Von Glahn (2013).
- Commodity-level split (tea vs silk vs porcelain shares) is **fragmentary** in the scholarship — data gap.

## 3. 粵海關 Canton customs revenue (the ad-valorem levy)
- **>1 million taels/yr** by 1789 (double the prior peak) — Wong (2016), *Global Trade in the Nineteenth Century* (Cambridge, cited 68).
- **855,500 taels/yr** remitted to Beijing (~40% of national customs) — 王迪安 (2025), 《大交流：伍秉鑑的怡和行與十九世紀的全球貿易》.
- "Squeeze" (Hoppo corruption) acknowledged qualitatively; precise % split Peking-vs-squeeze **not found** — data gap.

## 4. 戶部銀庫 (Board of Revenue treasury) reserves — ⚠️ MOD FIGURE DISCREPANCY
- **69.4M taels** in QL60 (1795) — Chen (2026), "Corruption on the Ladder," SSRN.
- **~70M taels** at peak — Ma (2013), "State capacity and great divergence," *Eurasian Geography and Economics* (cited 45).
- 27M taels (1722, Kangxi); 27.5M (1748) — Li (2018); Dunstan (2014). Expansion ~**4.5M taels/yr**.
- **The commonly-cited 81.8M-tael (8182萬兩) peak was NOT confirmed** in accessible academic sources.
  Verified peak is **69–70M taels (~c.1795)**, NOT ~1777. (81.8M may derive from a specific 內帑+戶部
  aggregate or an older/secondary figure; provenance unverified.)

### Bearing on the mod (se_QING_REVENUE.txt / se_CURRENCY.txt)
- Current code: seed **62000 千兩** (1763), **46140 千兩** (1815); peak var **81820 千兩**; milestone at ≥80000.
- Against the research: the **62000 (1763)** seed is plausible mid-trajectory (between 1748's 27.5M and
  1795's ~70M), though possibly a touch high for 1763 specifically. The **81820 peak is likely too high /
  unsourced** — a ~70000 (千兩) peak matches the verified ~70M-tael figure. OPEN: adjust peak 81820→~70000
  and milestone 80000→~68000? (Would also want to re-date: verified peak is c.1795, not the 1777 the code
  comment cites.) Not changed yet — flagged for user decision.

## 5. Reversal (opium-driven outflow)
- Inflow reversed **1826–27** (consensus) — Irigoin (2009), *J. World History* (cited 135); Von Glahn (2020).
  Minority: **1808** — Lin Man-houng 林滿紅.
- Net outflow **~62M taels** during 1820s–30s crisis — Lin Man-houng, in Von Glahn (2018), p.104.
- Opium: 2,000–4,000 chests/yr pre-1820 → **>16,000/yr by 1820**; 20,000 seized by Lin Zexu (1839).
- Lin Man-houng thesis: **global silver supply** more causal than opium per se — *China Upside Down* (2006/2020, Harvard, cited 201).

## Context
- China total silver stock **~15,000 tons c.1750** (Cao & Flynn 2020); ~20,270 tons accumulated via surplus (Deng 2008).

## Data gaps
1. Commodity-level payment split (tea/silk/porcelain) — fragmentary.
2. Hoppo squeeze % — qualitative only.
3. 81.8M-tael peak — unverified; academic peak is 69–70M.

## Calibration takeaway for the Canton feed (§5)
- Canton customs ≈ **~1M taels/yr = ~100 千兩/quarter** levy (Wong 2016), of which ~855.5K reached Peking.
- The mod's Canton yield is already ~30–45 萬兩/quarter = 300–450 千兩/quarter — i.e. the mod's *levy* figure
  is ALREADY roughly the whole-trade order, so the **reserve feed (specie for goods, larger than the levy)**
  should mirror the real inflow: net inflow ~190 tons/yr (Von Glahn) ≈ (at ~26.8 kg/千兩... see note) a
  few-thousand 千兩/yr. RECONCILE units carefully before setting §5's factor (the "Canton contribution
  should mirror this" instruction). See DESIGN doc §5 — replace the placeholder ×0.3 with a figure pinned
  to these numbers.
