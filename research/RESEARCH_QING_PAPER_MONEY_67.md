# Qing Dynasty Paper Money — Research Digest (#67)

**For:** design of a paper-money law/regime — LATE, crisis-gated, BOUNDED minting cap + inflation/depreciation
penalty (NOT an always-available, infinite-mint instrument). Covers 1763 baseline through the 1853–61
Taiping-crisis note episode, plus Yuan/Ming precedent for the over-issue→depreciation mechanism, and the
government-fiat-vs-private-note distinction.

**Date:** 2026-08-10. **Method:** WebFetch against Wikipedia's *Da-Qing Baochao*, *Hubu Guanpiao* (aka *Hu Bu
Guan Piao*), *Paper money of the Qing dynasty*, *Qing dynasty coinage*, *Da-Ming Baochao*, *Jiaochao*,
*Qianzhuang*, *Piaohao* articles — each of which is itself heavily footnoted to the named academic sources
below. Direct fetches of the primary monographs (von Glahn, King, Peng Xinwei in-text, Horesh, Debin Ma
working papers) were attempted but blocked: chinaknowledge.de had a TLS handshake failure, JSTOR returned
403, Google/Bing/DuckDuckGo searches returned only search-chrome or CAPTCHA pages with no indexable snippets,
Springer/Semantic Scholar chapter fetches 404'd. **So every claim below is sourced at one remove** — via
Wikipedia editors' citations to the named scholars, not by this agent reading the monographs directly. This
is flagged per-section below; nothing here should be read as "I opened King (1965) page N."

---

## (a) Was High-Qing (1763) government paper money essentially ABSENT? — YES, high confidence

**Answer: yes — treat 1763 as a paper-money-free monetary regime; government fiat notes should be
unavailable at game start and unlock only later, on a fiscal-crisis trigger.**

- The Qing dynasty's *only* pre-1853 government note episode was a brief, small, and quickly-abandoned
  experiment under the **Shunzhi Emperor**: **Shunzhi Guanpiao**, introduced **1651** by Finance Minister
  Wei Xiangshu to fund anti-Ming-remnant military operations, at ~1.28 million *guàn* (strings)/year, and
  **declared void roughly a decade later** (~1661). — CONFIDENCE: MEDIUM-HIGH (Wikipedia *Paper money of the
  Qing dynasty*, itself citing Peng Xinwei for the causal claim below).
- From then until 1853 — spanning the ENTIRE Kangxi–Yongzheng–Qianlong high-Qing era, i.e. the 1763 game
  start — **no government paper money was issued.** Wikipedia's summary is explicit: "it was only rarely
  suggested by court officials to reintroduce paper money to the Qing Empire," and in **1814 the Jiaqing
  Emperor rejected a petition to restart paper currency**, reasoning "neither the Chinese government nor any
  individuals in the past had experienced benefits from the circulation of a paper money." — CONFIDENCE:
  MEDIUM-HIGH (Wikipedia, sourced ultimately to Peng Xinwei / Jerome Ch'ên per the article's citation list;
  not independently verified against Peng's original text).
- The stated causal mechanism for this ~200-year avoidance, attributed to **Peng Xinwei 彭信威**: the Manchu
  rulers were "atavistic towards the inflationary pressure" experienced by their Jurchen (Jin dynasty)
  predecessors from earlier jiaochao-style over-printing, and the failed 1651 Shunzhi experiment "entrenched"
  this reluctance because it too proved inflationary. — CONFIDENCE: MEDIUM (single-source attribution, not
  independently checked against Peng's Chinese-language original; plausible and consistent with the
  documented 1814 rejection, but treat the *specific phrasing* "atavistic" as a Wikipedia paraphrase, not a
  verified Peng Xinwei quote).
- Positive confirmation from the money-supply side: the mod's own prior digest (`1763_QING_MONEY_SUPPLY.md`,
  Yan Hongzhong 燕红忠 2008 series) models 1763 circulation as 100% metallic (silver + copper 制錢) with no
  paper leg — consistent with the absence claim here.

**Design implication:** a paper-money law/regime should be **gated OFF at the 1763 bookmark** and should
only become available through a fiscal-crisis unlock (see (d)), mirroring the *actual* ~200-year gap between
the 1651 failure and the 1853 Xianfeng reintroduction.

---

## (b) The 1853–61 Taiping-crisis note issue — depreciation story with sourced magnitudes

Both instruments were introduced **simultaneously in 1853** (Xianfeng 3) under the Xianfeng Emperor, as
emergency financing for the Taiping War, after conventional revenue (land tax, salt gabelle, customs) and
metal-mining supply (Yunnan copper routes disrupted by the rebellion) were disrupted. CONFIDENCE for the
overall narrative shape: HIGH (multiple independent Wikipedia articles converge and cross-cite King, Peng
Xinwei, Horesh, Lin Man-houng, Yang Duanliu); CONFIDENCE for exact figures below: MEDIUM (single-source,
Wikipedia-mediated, some internal inconsistency noted).

### 戶部官票 Hubu Guanpiao (silver-denominated Board of Revenue notes)
- **Issued:** spring 1853 (Xianfeng 3) through 1858 (Xianfeng 8), with total production continuing to be
  recorded through 1860; denominations of 1, 3, 5, 10, 50 taels (liǎng).
- **Total production:** **9,781,200 taels** issued 1853–1860 (one figure given; treat as approximate).
- **Backing/convertibility:** promised convertible to silver after 6 months — **promise not kept by the 8th
  month of 1853**; official money shops in Beijing refused payouts, i.e. non-convertible almost from the
  start. Intended note-to-specie ratio started at **80% real silver / 20% notes**, later loosened to **50/50**.
- **Depreciation:** by **1856**, notes had depreciated **~60%** (1 tael of face value fetching only 800–900
  wén, vs. an official par of ~1000 wén/tael); by **1859**, collapsed to **~5% of face value**; by the final
  years, trading at a **~99% loss** on Beijing streets.
- **Withdrawal:** formally deprecated 1858 in favor of the copper-cash Da-Qing Baochao; had **completely
  disappeared from circulation by 1863**.

### 大清寶鈔 Da-Qing Baochao (copper-cash-denominated notes)
- **Issued:** 1853–1859 (Xianfeng 3–9). Denominations started at 500/1000/1500/2000 wén and were expanded
  upward to 5000/10000/50000/100000 wén by Xianfeng 6–9 — itself a symptom of runaway depreciation (issuing
  ever-larger face values to keep pace).
- **Backing:** nominally supposed to be government-backed and fully convertible on demand (unlike the
  openly-unbacked Ming notes), but **lacked adequate metal reserves from inception.**
- **Over-issue volume:** in Beijing alone, issuance "exceeded over 15,000,000 strings of cash coins" (i.e.
  15M+ *guàn*/chuàn), with **provincial issuance likely matching or exceeding this** — so total over-issue is
  plausibly 30M+ strings, though this compound figure is not independently confirmed. CONFIDENCE: LOW-MEDIUM
  on the provincial multiplier specifically (explicitly described by the source as "likely," not measured).
- **Depreciation timeline** (note: two Wikipedia articles give slightly different numeric paths for what
  is nominally the same collapse — reported as-is, flagged as an internal inconsistency to resolve if a
  precise curve is needed for game-balance tuning):
  - By **1855** (Xianfeng 5): worth ~50% of nominal value.
  - By **1856** (Xianfeng 6): silver value had fallen to 50% of its Xianfeng-2 (1852) value; market rates for
    the 1000-wén note had collapsed to "450 Beijing cash or 200–300 standard cash coins."
  - **1857:** the "Yu" exchange banks (the primary institutions handling note-to-cash exchange) closed.
  - **1859:** notes no longer accepted for tax payments.
  - By **1860** (Xianfeng 10): exchange rate against private notes reached 2:1, later 3.5:1; the Ministry
    proposed ending issuance in March 1860.
  - By **1861** (Xianfeng 11): auctioned at only **~3% of nominal value**; one figure states a 1,000-wén note
    had fallen to as little as **26–52 wén market value** (i.e. ~2.6–5.2% of face — roughly consistent with
    the "3%" figure from the other article); in July 1861 workers refused them as salary.
  - **September 1861:** ceased circulating entirely; all three semi-official exchange banks (Yu, Qian, Tian)
    folded from bank runs by June 1861.
  - **1868:** the system formally/completely abolished.

### Net picture for the mod
Both instruments ran roughly **8 years (1853→1861) from full-value issue to near-total worthlessness (~3–5%
of face)**, with the collapse accelerating sharply in the final 2 years (1859–61) once tax offices stopped
accepting the notes and the exchange banks failed. Over-issue (Beijing alone 15M+ strings, likely 2x+ that
empire-wide) against an inadequate/broken backing ratio (nominal 80/20 collapsing to unenforced 50/50, then
to no real convertibility) is presented as the proximate driver.

---

## (c) Precedents: the over-issue → depreciation mechanism (Yuan and Ming)

CONFIDENCE: MEDIUM — again Wikipedia-mediated; the Yuan article's primary citation is a Chinese numismatic
picture-compilation (1992) rather than an Anglophone academic monograph, and the direct von Glahn *Fountain
of Fortune* text could not be fetched (search engines returned only chrome/CAPTCHA, no indexable content).
The qualitative mechanism (silver/backing anchor → later over-issue without matching reserves → collapse)//
is consistent across both precedents and matches the Qing 1853–61 case, which strengthens confidence in the
*mechanism* even where exact Yuan/Ming numbers are weakly sourced.

### 交鈔/中統鈔 Yuan jiaochao / Zhongtong chao
- **1260:** Kublai Khan issued two note series. The first (July 1260) was backed by **silk**, and failed;
  the second (October 1260, Zhongtong chao) used a **silver standard**, and is described as the first
  Chinese paper currency to become the **predominant circulating medium** — i.e., initially a genuine,
  reserve-anchored fiat/near-fiat success.
  - Silver-backing detail: whether/how strictly this silver anchor was maintained over time is not detailed
    in the fetched summary — GAP, flagged, would need von Glahn's in-text treatment to pin the anchor
    ratio and its erosion.
- **Over-issue and collapse:** the system underwent "devaluation and hyperinflation" over the following
  ~90 years. By **1350**, the final series (Zhizheng jiaochao) is described as "a fiat currency" that "was
  widely rejected" — i.e., by the end, the silver anchor had been abandoned/diluted, output had outrun
  reserves, and the public stopped accepting it. This sits within a couple of decades of the Yuan's
  collapse (1368), consistent with currency failure as one strand of terminal Yuan fiscal crisis.

### 大明寶鈔 Da-Ming Baochao (Ming)
- **1375** (Hongwu): the "Supervisorate of Paper Money" established 1374; the note itself explicitly **NOT
  backed by any hard currency or reserves, with no government-set production limit** — i.e. unlike the
  Yuan's initial silver anchor, Ming notes were unbacked fiat from the outset. Nominal par: notes for
  100–1000 wén, redeemable in theory for 1000 bronze cash.
- **Over-issue channel:** issued through multiple channels including military salaries; the government
  "hardly accepted or replaced any existing paper money," eroding confidence; by **1380**, worn notes were
  barred from replacement, forcing continued circulation at reduced real value — a direct engine-relevant
  mechanic (note wear + non-replacement = forced further devaluation, distinct from straightforward
  over-issue but compounding it).
- **Depreciation magnitude:** by **1535**, 1 *guàn* (nominally worth 1000 wén) was valued at only **0.28 of
  a single coin** — i.e., depreciation to roughly **0.03% of face value** over 160 years. This is the most
  extreme (near-total, multi-century) collapse of the three episodes reviewed here, versus the Qing's
  faster-but-partial collapse (~3–5% of face over 8 years) and the Yuan's ~90-year erosion to rejection.
- **Formal abandonment:** production and use of banknotes were eventually abolished under the Hongzhi/
  Zhengde emperors, citing hyperinflation and lost public trust.

### The shared mechanism to model
Across Yuan, Ming, and Qing 1853–61, the qualitative driver is consistent and simple enough to encode as a
game mechanic:
1. Notes start **anchored to a reserve** (silver for Yuan Zhongtong chao; nominally silver/copper for Qing
   Xianfeng notes; explicitly UNANCHORED from day one for Ming) — anchoring strength varies but is never
   perfectly enforced.
2. Fiscal pressure (war finance in all three: Yuan late-dynasty strain, Ming military payroll, Qing Taiping
   War) drives **issuance beyond the reserve/backing capacity**, with denominations/print-runs escalating
   over time (explicit in the Da-Qing Baochao case: face values inflating from 500 wén to 100,000 wén within
   6 years).
3. Once redemption promises are broken (Qing: "promise not kept by month 8 of the first year") or worn notes
   are refused replacement (Ming), **public confidence collapses faster than the nominal over-issue ratio
   alone would predict** — i.e. depreciation is not linear in over-issue; there's a confidence-cliff once
   convertibility visibly fails.
4. Terminal state is near-total worthlessness (Ming: ~0.03% of face over 160yr; Qing: ~3-5% of face over
   8yr) followed by formal abolition, not a graceful return to par.

---

## (d) Government fiat vs. PRIVATE notes — do NOT conflate

CONFIDENCE: MEDIUM-HIGH for the qualitative distinction (converges across three separate Wikipedia articles,
citing Lin Man-houng, Yun Liu, Niv Horesh, McElderry, Huang Jianhui, Cheng Linsun); LOW for exact dates/scale
figures (single-source, unverified against primary texts).

- **錢莊 Qianzhuang** ("native banks"): issued private notes — **zhuangpiao 莊票** and **yinqianpiao 銀錢票**
  ("silver money notes") — backed by the individual bank's own deposits/capital, NOT by state authority.
  Expanded significantly in the **19th century**, with roots noted as far back as the Ming. Notes required
  ~10–15 days to redeem via courier verification (anti-fraud), but were trusted enough that British banks in
  Shanghai accepted qianzhuang scrip (zhuangpiao) as loan security, and — pointedly — when the *government's*
  Xianfeng notes were depreciating, privately-issued zhuangpiao were valued at up to **double the nominal
  value of the government notes** for the same face amount. This is a strong illustrative datapoint for "why
  private ≠ government fiat" in the mod.
- **票號 Piaohao** (Shanxi remittance banks): first documented house **Rishengchang, founded 1823**; issued
  **money-order-like instruments** (duìtiē 兌帖, qītiē 期帖, qiántiē 錢帖, yínpiào 銀票) rather than
  circulating fiat currency — these functioned as **interregional remittance/exchange documents backed by
  silver held at specific branches** (branch capital stock ranged ~20,000–500,000 taels), not as a
  government-style circulating paper currency. Operated until nationalization in 1952.
- **The distinction that matters for the mod:** private qianzhuang/piaohao notes are **convertible
  instruments backed by a specific, identifiable private balance sheet**, redeemable at a known counterparty,
  and their value is disciplined by that counterparty's solvency and reputation — structurally different from
  a **state fiat note backed (if at all) by a diffuse, unaudited government promise** that can be broken
  unilaterally (as the Hubu Guanpiao's 6-month convertibility promise was, within its first year). The mod
  should **not** give the player's future "paper money" law/regime the same trust/backing dynamics as private
  note-issuing institutions — they are different mechanics with different failure modes, and historically the
  private instruments comfortably OUTLASTED and out-performed the state's fiat attempt during the very same
  Xianfeng crisis window.

---

## Design implications for the mod (#67)

1. **1763 start: paper money law/regime = UNAVAILABLE.** No historical basis for it; matches the ~200-year
   real gap (1661 Shunzhi withdrawal → 1853 Xianfeng reintroduction) and the explicit 1814 Jiaqing rejection.
2. **Unlock trigger should be FISCAL-CRISIS-GATED, not tech/time-gated on its own.** Historically the trigger
   was war finance under acute treasury stress (Taiping War revenue collapse), not steady economic growth or
   a "reached year X" unlock. Suggested mod hook: tie availability to an existing fiscal-crisis/treasury-
   depletion meter (e.g. something in the vein of the qing_currency_stress meter or a Ministry-of-Revenue
   silver-reserve collapse threshold — see `research/RESEARCH_QING_SILVER_RESERVE.md` for the reserve
   trajectory already modelled) crossing a "desperate" band, analogous to the historical ~6200万両 (1763) →
   deep drain that preceded 1853.
3. **Cap must be BOUNDED, and the bound should visibly ERODE trust as it's approached/exceeded** — not a
   flat infinite-mint tap. Model as: (a) a nominal backing ratio (start generous, e.g. Hubu Guanpiao's
   initial 80/20 silver/note ratio) that (b) the player can push toward the historical 50/50 floor under
   pressure, beyond which (c) a depreciation penalty kicks in that is **non-linear and accelerating**, not
   proportional to over-issue — mirroring the historical "confidence cliff" once the 6-month convertibility
   promise broke. A simple curve: value_multiplier stays near 1.0 while cumulative issuance < backing×ratio,
   then falls sharply (not linearly) once exceeded — reaching single-digit % of face within a small number of
   turns/years past the threshold, per the Xianfeng notes' ~3-5%-of-face outcome inside ~8 years.
4. **Depreciation should feed back into further need to print** (a doom-loop, not a one-off penalty) — this
   is what actually happened: falling real value of existing notes didn't stop new issuance, it accelerated
   it (denominations escalating 500→100,000 wén in 6 years). The mod's penalty should make the SAME nominal
   fiscal need require MORE printing as depreciation deepens, self-reinforcing toward collapse unless the
   player pulls back — this is the "bounded but with a runaway failure mode" shape the design brief wants,
   not a hard wall.
5. **Withdrawal/abolition should be a real terminal state**, not merely "value goes to near-zero and sits
   there." Historically the notes were formally withdrawn from tax acceptance (1859), then from circulation
   entirely (1861), then formally abolished (1868) — i.e. the regime should have an explicit end-state event
   (forced abolition once value/trust falls below some floor for long enough) rather than lingering
   indefinitely as a worthless-but-still-technically-legal instrument.
6. **Do not let private banking (qianzhuang/piaohao) share the same trust meter as the state paper-money
   regime.** If/when the mod also wants a private-banking mechanic (native banks, remittance houses), it
   should be a SEPARATE system with its own (better) backing dynamics — conflating the two would misrepresent
   the historical record, where private notes retained value and public trust *specifically because* they
   were not the failing government instrument.
7. **Two-instrument structure is optional but historically accurate** if the design wants flavor: a
   silver-denominated instrument (Hubu Guanpiao-like) and a copper-cash-denominated instrument (Da-Qing
   Baochao-like) were BOTH introduced together in the historical crisis and depreciated on similar but not
   identical timelines — could be modelled as one unified "paper money" law for simplicity, or split for
   texture; the digest does not find a strong mechanical reason to require splitting them.

---

## Sources list with confidence tags

All items below were accessed via WebFetch of Wikipedia articles on 2026-08-10; direct access to the primary
monographs was attempted and failed (TLS/403/CAPTCHA/404 across chinaknowledge.de, JSTOR, Springer,
Semantic Scholar, and general web search engines). Confidence tags reflect how the claim reached this
digest, not the underlying scholar's rigor.

- **Peng Xinwei 彭信威, *A Monetary History of China* (中國貨幣史, 1954; Kaplan trans. 1994)** — cited by
  Wikipedia for: the Shunzhi-1651-entrenched-reluctance causal claim; general historical-inflation analysis
  underlying the Da-Qing Baochao and Ming Baochao articles. TAG: **secondary, MEDIUM confidence** (claim
  attributed correctly per Wikipedia's citation, original text not read by this agent — see also the mod's
  existing `1763_QING_MONEY_SUPPLY.md` digest, which likewise could not access Peng's original in-text
  figures and flagged the same access gap).
- **Frank H.H. King** — cited by Wikipedia (*Da-Qing Baochao*, *Hubu Guanpiao*) for exchange-rate
  documentation of the Xianfeng note collapse. TAG: **secondary, MEDIUM confidence** — title *Money and
  Monetary Policy in China 1845-1895* not independently confirmed as the specific cited work (Wikipedia
  citation lists "King" without full bibliographic detail in the fetched excerpt); treat title match as
  LIKELY but unverified.
- **Niv Horesh** — cited across *Da-Qing Baochao*, *Hubu Guanpiao*, *Qianzhuang* for: hyperinflation
  causation (inadequately-backed notes + debased daqian coinage), and late-Qing paper-currency
  reintroduction driven by declining domestic mining + reduced Japanese metal imports. TAG: **secondary,
  MEDIUM confidence** — consistent with a real body of Horesh work on Chinese monetary history (e.g. his
  writing on the monetary system of China under the Qing), but this agent did not read Horesh's text
  directly; only Wikipedia's paraphrase.
- **Lin Man-houng** — cited (*Hubu Guanpiao*, *Qianzhuang*) for the timing of private qianzhuang note
  issuance (from "end of Qianlong period") and the north/south cash-vs-tael denomination split. TAG:
  **secondary, MEDIUM confidence**.
- **Yang Duanliu 楊端六 (1962)** — cited (*Da-Qing Baochao*, *Hubu Guanpiao*) for reserve-ratio studies
  (the 80/20 → 50/50 backing-ratio figures). TAG: **secondary, MEDIUM confidence** — these are the most
  game-relevant numbers in the whole digest (they map directly onto a "bounded cap" mechanic) but rest on a
  single unverified citation chain; if the mod team wants to lock in exact ratios for balance purposes,
  worth a follow-up pass to find Yang Duanliu's 1962 work directly.
- **Jerome Ch'ên** — cited (*Da-Qing Baochao*) for Ministry policy analysis around the 1859–60 withdrawal
  decisions. TAG: **secondary, LOW-MEDIUM confidence** (single mention, no detail retrieved).
- **Debin Ma (LSE)** — cited (*Paper money of the Qing dynasty*) for the official wén/tael exchange rate
  (1000 wén = 1 tael official, rising toward 1200 wén by the 19th century) and (via a separate LSE working
  paper, fetch attempt 404'd) for the broader claim that "the greatest transformation in China's monetary...
  system occurred with respect to paper money and banking," referring to the LATE Qing/Republican banking
  boom, not the 1763 baseline. TAG: **secondary, MEDIUM confidence** for the exchange-rate figure (consistent
  with the mod's own `1763_QING_MONEY_SUPPLY.md` figure of ~800-1000 wén/tael); the broader banking-
  transformation claim is UNVERIFIED beyond the search-snippet level.
- **Richard von Glahn** (*Fountain of Fortune: Money and Monetary Policy in China, 1000–1700*; *The Economic
  History of China*) — requested per the task brief as a target source; **NOT independently accessed** in
  this pass (search engines returned only chrome/CAPTCHA pages, no indexable snippets; no direct citation of
  von Glahn was found in the Wikipedia articles fetched — one article explicitly noted his absence from its
  citation list). TAG: **NOT SOURCED — explicit gap.** The Yuan jiaochao silver-standard-then-collapse
  narrative in section (c) is consistent with what is generally known of von Glahn's thesis (money essentially
  requires a credible reserve anchor; erosion of that anchor drives depreciation) but this digest cannot claim
  to have read or verified his specific text. Recommend a follow-up pass with library/JSTOR access if the
  mod wants von Glahn's numbers specifically pinned.
- **Inner Mongolian Numismatic Research Institute, *A Compilation of Pictures of Chinese Ancient Paper
  Money* (1992)** — primary citation underlying the Yuan *Jiaochao* Wikipedia article. TAG: **tertiary
  numismatic catalogue, LOW-MEDIUM confidence** for the historical narrative (not a monetary-history
  monograph).
- **Hosea Ballou Morse, *The Trade and Administration of the Chinese Empire* (1920)** — cited (*Da-Ming
  Baochao*) for documentation of surviving Ming note specimens. TAG: **primary-adjacent (period Western
  scholarship), MEDIUM confidence**, tangential to the depreciation-mechanism claims (specimen documentation
  only).
- **Wikipedia articles used as the access layer**: *Da-Qing Baochao*, *Hubu Guanpiao* / *Hu Bu Guan Piao*,
  *Paper money of the Qing dynasty*, *Qing dynasty coinage*, *Da-Ming Baochao*, *Jiaochao*, *Qianzhuang*,
  *Piaohao*. TAG: **tertiary aggregator — every factual claim above is only as reliable as Wikipedia's own
  citation accuracy, which was NOT cross-checked against the primary texts in this pass.** Flag explicitly:
  two of these articles gave mutually-slightly-inconsistent 1861 depreciation figures (3% of face vs.
  2.6–5.2% of face) — reported both, not reconciled.
- **Baidu-tier / non-academic sources encountered and explicitly EXCLUDED from citation**: "Totally History"
  (a general-audience history-blog site) surfaced in one search pass discussing Xianfeng-era private-bank
  over-issuance; **not used as a source above** — flagged here only to note it was seen and deliberately not
  relied upon, per the instruction to distinguish scholarly from tertiary/Baidu-tier sources.

### What is NOT resolved / needs a follow-up pass if higher confidence is required
1. Von Glahn's own text (both *Fountain of Fortune* and *The Economic History of China*) — zero direct access
   this pass; all Yuan/Ming mechanism claims are Wikipedia-mediated only.
2. Frank King's *Money and Monetary Policy in China 1845-1895* — title match to the Wikipedia "King"
   citations is plausible but unverified; no page numbers obtained.
3. Peng Xinwei's original Chinese text (or the 1994 Kaplan translation) — same access gap already flagged in
   the mod's prior `1763_QING_MONEY_SUPPLY.md` digest; this digest inherits, does not close, that gap.
4. The Beijing-only "15,000,000 strings" Da-Qing Baochao over-issue figure and its "provincial issuance
   likely matched or exceeded this" extension are the single most game-relevant over-issue magnitude and the
   weakest-sourced (explicit "likely," uncited multiplier).
5. Yang Duanliu's 80/20 → 50/50 backing-ratio figures — best candidate numbers for a literal in-game
   "backing ratio" parameter, but traced through only a single citation chain; worth confirming before hard-
   coding as a balance constant.
