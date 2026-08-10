# Research: Gold/silver monetary interaction — historical grounding for #59

Task #59 (backlog): the mod currently prices gold and silver as **two independent floating
goods with no ratio link** (each just another commodity in the trade-goods system). The user's
directive: consult academic sources first on how gold and silver interacted MONETARILY in the
18th–19th centuries, before deciding whether/how the mod should link them. This digest answers
the five sub-questions in the brief, gives a modelling recommendation, and flags what could not
be verified. Written 2026-08-10 (or thereabouts).

**Relationship to existing repo research — read these too, they carry the China-specific
numbers this digest leans on:**
- `research/1763_TRADE_GOOD_PRICES_1763.md` / `RESEARCH_TRADE_GOOD_PRICES_1763.md` — Section A1
  already has a two-source-corroborated gold:silver ratio series for China (1:8–10 in the 17th c.
  → converging to ~1:14–15 by 1750–63), via Melitz (2017) citing Peng Xinwei and von Glahn, plus
  an independent Chinese-language synthesis. **This digest does not re-derive that number — it
  explains the MECHANISM behind why the ratio moved that way, and what a game should do about it.**
- `research/1763_CANTON_SILVER_INFLOW.md` — Canton-era silver inflow volumes/reserve figures.
- `research/1763_QING_MONEY_SUPPLY.md` — copper cash (制錢) vs silver as the domestic circulating
  media, exchange rate ~700–800 wén/tael market in the 1750s–1800; this is the OTHER bimetallism
  (silver vs copper) that actually governed everyday Qing transactions — see Q4 below.

---

## Q1. Bimetallism vs monometallism (silver standard, gold standard) — definitions and who ran what

**Bimetallism** = a monetary system in which BOTH gold and silver are full legal tender, minted
freely by the state at a FIXED statutory mint ratio between them (e.g. France 1803, 15.5:1;
US Coinage Act of 1792, 15:1). Both metals coexist as money by law, at a rate the state sets, not
the market. [Wikipedia "Bimetallism", fetched]

**Monometallism** = only one metal is full legal tender; the other, if it circulates at all, does
so as subsidiary/token coinage capped by weight or amount, not as unlimited legal tender.
- **Silver standard**: silver is THE monetary metal; gold (if present) is not full legal tender.
  This was Qing China's system throughout — silver sycee/ingots by weight, not fixed-denomination
  coin, functioned as the high-value monetary metal; gold was not a general legal-tender coinage
  metal in China at all in this period. [Wikipedia "Silver standard", fetched — "China's system
  remained predominantly silver-based even as most Western economies transitioned to gold after
  1873... the Qing specifically resisted minting their own silver coins until 1890, preferring
  traditional ingots."]
- **Gold standard**: gold is THE legal-tender metal, silver (if present) is subsidiary/token only.

**Britain's path (1717 → 1816/1821), specifically:**
- **1717**: Isaac Newton, as Master of the Royal Mint, set the guinea (gold) at 21 shillings
  (silver) — a mint ratio that OVERVALUED gold relative to the contemporary market rate. Per
  Gresham's Law (Q3), this caused silver to be exported/hoarded rather than brought to the Mint,
  and Britain drifted into a **de facto** gold standard without ever formally choosing one — "for
  a century, hardly any silver coins were minted in Britain." [Wikipedia "Gresham's law", fetched]
- **1816 Great Recoinage / 1819 Act for the Resumption of Cash Payments (took effect 1821) /
  1844 Bank Charter Act**: these turned the de facto 1717 gold standard into a **formal, legislated
  one** — silver coinage was explicitly demoted to subsidiary/token status (limited legal tender,
  capped amounts), gold sovereigns became the full legal-tender unit, and banknote convertibility
  to gold plus mandated reserve ratios were legislated. [Wikipedia "Gold standard", fetched]
- So: Britain 1717–1816 = de facto (accidental, Gresham-driven) gold standard; 1816/1821 onward =
  formal, legislated gold standard. **By both the mod's bookmark years, Britain is already on a
  gold standard** (informally by 1763, formally by 1815... actually 1821 is AFTER the 1815
  bookmark — flag: in 1815 Britain was in a wartime suspension of gold convertibility, 1797–1821,
  the Restriction period, so 1815 specifically is a paper-pound / suspended-gold-standard moment,
  not yet the restored 1821 gold standard. This nuance is not covered by the Wikipedia gold-standard
  fetch and should be flagged as **unverified in this session's sourcing** if the mod wants
  1815-specific British monetary-regime accuracy.)

**The wider West's formal move to gold, 1871–1900** — this happened well AFTER both the mod's
1763 and 1815 bookmarks, so both bookmarks sit in a bimetallic-or-silver world for every major
power except Britain:
- **Germany**: Coinage Act of 4 Dec 1871 defined the gold mark; full implementation 1 Jan 1876 —
  the German move is credited as the trigger for the broader European cascade.
- **Latin Monetary Union** (Belgium/Switzerland/Italy/France, joined by Greece 1868) ran a
  15.5:1 bimetallic peg from 1865; suspended free silver coinage in 1873, ended it entirely in
  1878 — the "silver surplus" (from the ratio drifting, see Q2/Q3) made the peg unsustainable.
- **US**: Coinage Act of 1873 ("the Crime of 1873" to its opponents) suspended standard silver
  dollar coinage; de facto gold parity by 1879; formal gold standard legislated in 1900.
- **Scandinavian Monetary Union 1875, Netherlands 1875, Austria-Hungary 1892, Russia 1897** — the
  cascade of monometallic-gold adoptions through the 1870s–1890s.
- [All of the above from Wikipedia "Gold standard", fetched directly.]

**Summary table for the mod's two bookmarks:**

| Power | 1763 regime | 1815 regime |
|---|---|---|
| Qing China | Silver standard (silver by weight = high-value money; copper cash = everyday money; NOT gold-linked at all — see Q4) | Same — silver standard persists all the way to 1935 |
| Britain | De facto gold standard (since 1717, Gresham-driven) | De facto gold standard, but banknotes NOT convertible to gold 1797–1821 (Restriction period) — a suspended/paper-pound interlude, not full metallic convertibility |
| France | Bimetallic (15.5:1 statutory ratio; formalized 1803) | Bimetallic (same 15.5:1 ratio; would later anchor the 1865 Latin Monetary Union) |
| USA | Bimetallic (15:1 statutory ratio, Coinage Act of 1792) | Bimetallic (same 15:1 ratio; not overturned until 1834's re-ratioing and ultimately 1873) |
| Most of continental Europe/rest of world | Bimetallic or silver-standard, NOT gold | Same — the gold-standard cascade is 60+ years in the future |

**Bottom line for #59: at BOTH of the mod's bookmark years, gold monometallism is the exception
(Britain only, and only de facto/interrupted), not the rule.** Bimetallism (fixed legal mint
ratio) and silver standard (China) are the dominant regimes the mod needs to model correctly for
1763 and 1815 — a "gold standard" framing for the wider world would be anachronistic for both
bookmarks.

---

## Q2. The gold:silver RATIO — actual values and the convergence path

**This sub-question is already answered with sourcing in the repo's existing trade-goods digest**
(`research/RESEARCH_TRADE_GOOD_PRICES_1763.md`, Section A1) — repeating the headline finding here
because it is the load-bearing number for #59, with the mechanism explanation (Q3) added on top:

- **China domestic, 17th century: ~1:8–10** (gold cheap relative to silver, silver dear relative
  to gold) vs **Europe: ~1:14–15** in the same period. Peng Xinwei 彭信威 (via Melitz 2017, citing
  Peng's *Chinese Monetary History*, p.766): "an ounce of gold cost 15 ounces of silver in Europe,
  but still only 10 in China" (second half of 17th c.).
- **Convergence**: von Glahn (2003) p.197 (via Melitz 2017 pp.5–6) shows China's gold price moved
  from 138% of the international price in the 1730s to ~97% (essential parity) by the 1750s.
  A Chinese-language secondary synthesis independently corroborates: "初期還是一比十...乾隆後期漲到了
  一比十五" (early on still 1:10... by late Qianlong risen to 1:15).
- **By the mod's 1763 bookmark, the ratios were essentially unified** — both the English-language
  academic reconstruction (Melitz/von Glahn/Peng Xinwei) and the independent Chinese-language
  synthesis agree on this. The convergence is the joint product of (a) sustained silver inflow
  into China via the Canton trade and the Manila galleon (American/Japanese silver), which bid up
  gold's China price relative to silver as arbitrageurs shipped gold OUT of China while silver
  flowed IN (see Q3's Dermigny figures: EIC ships in 1729–41 carried gold from Canton to London
  specifically because China still undervalued gold, at ~30% gross margin vs ~150% on ordinary
  merchandise), and (b) the West's own bimetallic ratio (15:1 US, 15.5:1 France) acting as a
  relatively stable anchor that the China ratio converged toward, not the reverse.
- **By 1815** (the mod's second bookmark, 50 years further into the convergence and further into
  the post-Napoleonic silver-flow era), the ratio should be treated as **essentially the same
  Western-anchored ~1:15**, with China no longer meaningfully divergent — this session did not
  find a dedicated 1815-specific figure (see "what could not be verified" below), but nothing in
  the sourced material suggests a re-divergence before the much later 1870s bimetallic collapse
  (Q1) started pushing gold's price UP again as the West went monometallic-gold and demand for
  monetary gold rose relative to silver.

**Numbers to carry into a model**, per the existing digest: **gold ≈ 14–15× silver by weight**,
uniformly, for both 1763 and 1815 — NOT the wider 1:8–10 gap that would be correct for an earlier
(17th-century) starting point.

---

## Q3. Gresham's Law + the market-vs-mint ratio — is arbitrage the key mechanism?

**Statement**: "Bad money drives out good" — when a legal/statutory exchange rate between two
forms of money diverges from their market (bullion) value, the UNDERVALUED-at-the-legal-rate form
is hoarded, melted, or exported, while the OVERVALUED-at-the-legal-rate form is the only one that
actually circulates. Robert Mundell's sharper restatement: "Bad money drives out good **if they
exchange for the same price**" — the law is contingent on a FIXED legal exchange rate that no
longer reflects market fundamentals; it does not apply under floating/market exchange. [Wikipedia
"Gresham's law", fetched]

**Applied to bimetallism directly**: this is precisely the mechanism by which every bimetallic
regime historically failed to hold its peg once the market ratio drifted away from the mint
ratio:
- **Britain 1717**: Newton's mint ratio overvalued gold (21 shillings/guinea) relative to the
  market. Consequence: silver was exported/hoarded rather than brought to the Mint for coining,
  "for a century, hardly any silver coins were minted in Britain" — Britain backed into a de facto
  gold standard purely through this arbitrage mechanism, with no legislative intent to adopt one.
- **France/Latin Monetary Union 1870s**: the reverse direction — a SILVER surplus (new German
  silver being demonetized and dumped, per the Q1 German 1871–76 gold conversion) meant silver
  became UNDERVALUED at the legal 15.5:1 rate relative to its falling market value, so, per
  Gresham, silver flooded INTO the Union's mints (anyone could bring undervalued-by-the-market
  silver and get it coined at the generous legal rate) while gold was hoarded/exported. This
  "silver surplus" is exactly what forced the 1873 suspension and 1878 abolition of free silver
  coinage. [Wikipedia "Bimetallism", fetched]
- **US 1873 "Crime of 1873"**: suspending free silver coinage just as new Nevada silver
  discoveries (Comstock Lode) were about to make silver AGAIN undervalued at the legal 15:1/16:1
  rate — pre-empting the same Gresham dynamic that hit France, at the cost of a decades-long
  political fight (Bryan's "Cross of Gold," 1896) from producers/debtors who wanted silver
  remonetized.

**Is arbitrage/Gresham the mechanism a model should capture? Yes — this is the direct, sourced
answer.** Friedman's "Bimetallism Revisited" (*Journal of Economic Perspectives* 4:4, 1990)
argues, against the conventional view he himself once held, that bimetallism run as designed
(free coinage of both metals at the legal ratio) functioned as a **market-stabilizing arbitrage
mechanism**: because anyone could freely convert either metal into legal-tender coin at the fixed
ratio, a large enough bimetallic bloc (like the US pre-1873, or France/the Latin Monetary Union)
could absorb supply/demand shocks to EITHER metal by having the relatively-cheap metal do more of
the circulating, without the price of money itself swinging — i.e., bimetallism, while it held,
"stabilized" the metals market by construction, precisely because arbitrage was allowed to work.
This is corroborated by the AEA abstract fetched directly: Friedman found "the conventional view
[that bimetallism is unstable/unsatisfactory and monometallism is superior] is dubious, if not
outright wrong." Flandreau's *The Glitter of Gold* (Oxford UP; covers 1848–1873 France) makes the
matching micro-level argument: French bimetallism "effectively pegged the exchange rate between
gold and silver at its legal ratio of 15.5:1" through exactly this arbitrage channel, and
Flandreau's finding is that "gold and silver supply shocks under bimetallism were less
destabilizing than previously believed" — i.e., the arbitrage mechanism worked as a shock
absorber for as long as the bloc was large enough relative to world metal flows. Redish and
Kindleberger take the opposing, more skeptical position (bimetallism is inherently fragile once
the ratio drifts far enough that one metal's ENTIRE stock would need to flow to maintain the peg —
this is essentially what happened in 1873). **The debate in the literature is about how ROBUST
the arbitrage-peg is, not about whether arbitrage is the mechanism** — all sides agree the
mechanism is Gresham-style arbitrage between the legal/mint ratio and the market ratio; they
disagree about how long/how well a real-world bimetallic bloc can keep the two in line before the
peg breaks.

---

## Q4. Did gold and silver RESERVES actually interact, or were they independent? — and the China correction

**For the West (bimetallic powers, France/US pre-1870s): YES, tightly linked, by construction.**
Under a "proper" bimetallic standard, gold and silver are not two independent reserve pools —
they are two forms of the SAME legal-tender money, convertible into each other at the fixed mint
ratio on demand at the mint. A state's monetary "reserve," in the sense that matters for its money
supply, is the SUM of its gold and silver holdings valued at the legal ratio, not two separate
numbers. This is the direct implication of the arbitrage mechanism in Q3: the two metals are
fungible AT THE PEG, precisely so that shocks to one metal's supply get absorbed by substitution
toward the other.

**For Britain (gold standard from 1717/1816): effectively NO** — silver was demoted to capped
subsidiary token coinage, so Britain's *monetary* reserve is gold; silver held is a commodity, not
a monetary reserve metal, once the de facto gold standard set in.

**For Qing China (silver standard): gold was NOT a monetary reserve metal in any working sense —
this is the key clarifying finding, and it directly answers the brief's flagged common confusion.**
- China's real, functioning "bimetallism" — i.e., the actual TWO-CURRENCY system that governed
  everyday Qing monetary life — was **silver vs. COPPER CASH (制錢), not gold vs. silver.** This
  is confirmed directly by Kuroda Akinobu's work (fetched: Kuroda, "Monetary Structure under the
  Last Chinese Empire and its Breakdown," *Socio-Economic History* 57:2 (1991), pp.227–259,
  doi:10.20624/sehs.57.2_227): the Qing dynasty's monetary system split currency function between
  **silver bullion (by WEIGHT, not fixed coin denomination) for inter-regional/large-value
  transactions**, and **copper cash for local/everyday transactions**, and — crucially —
  **"[Qing authorities] didn't set up any fixed exchange ratio between two currencies"**: the
  silver:copper exchange rate FLOATED (per the repo's own `1763_QING_MONEY_SUPPLY.md`, market rate
  ~700–800 wén/tael in the 1750s–1800, vs. an official/statutory 1,000 wén/tael that the market
  rate did not actually track tightly). This is the opposite of Western bimetallism's FIXED legal
  ratio — China's domestic dual-currency system was a genuinely FLOATING two-money system, not a
  Gresham-vulnerable fixed peg.
- **Gold's actual role in Qing China**: a commodity / store-of-value / occasionally an export
  arbitrage good (per the Dermigny figures in Q2/Q3 — Europeans shipped Chinese gold TO Europe
  specifically because it was cheap relative to silver there), but **not part of the circulating
  money supply and not treated as a monetary reserve asset the way silver was.** Von Glahn's
  *Fountain of Fortune: Money and Monetary Policy in China, 1000-1700* (UC Press, 1996) is the
  standard reference establishing this — the book's own framing (per the fetched summary) is that
  it studies "state monetary policy from Song to early Qing" through the lens of silver/bullion
  flows specifically, treating gold as a subject of trade/commerce rather than of monetary policy.
  This session could not fetch von Glahn's exact wording on gold's non-reserve status (see gaps
  below), but the framing is corroborated by every other source touching China's system (Kuroda;
  the "Silver standard" Wikipedia entry's characterization of Qing China as resisting even silver
  coin standardization until 1890, let alone treating gold as a reserve metal; and the repo's own
  existing digest, which frames the gold:silver ratio purely as an ARBITRAGE/TRADE phenomenon
  driving Canton-era silver inflows, never as a Qing reserve-management decision).
- **Irigoin's "silver question"** work (LSE) reinforces the same point from the world-money angle:
  her research frames silver — specifically Spanish-American peso silver — as having become THE
  effective global reserve/settlement currency ("a currency standard for the international
  economy"), with China's demand for silver (in exchange for tea/silk/porcelain) as the central
  engine of that system; gold does not appear in her framing as a competing or complementary
  Chinese reserve asset at all.

**So: the brief's flagged confusion is real and directly relevant.** A model built around "China's
gold and silver reserves interact via a ratio" would be modelling the WRONG pair of metals for
China's actual historical monetary mechanics. China's real linked-reserve pair was **silver and
copper cash**, governed by a FLOATING (not fixed-peg) exchange rate. Gold/silver was an
international ARBITRAGE-TRADE relationship that happened to run largely through China (because
China was cheap-gold/dear-silver relative to the West) — not a domestic Chinese monetary-reserve
mechanism at all.

---

## Q5. Modelling recommendation for #59

Given Q1–Q4, here is the recommendation, split by which power is being modelled:

**For gold vs silver specifically (the mod's literal ask):**
- **(b) an arbitrage/Gresham mechanism that mean-reverts toward a ratio anchor is the
  historically-correct MECHANISM**, but it should be scoped narrowly: it describes how a
  BIMETALLIC power's gold and silver reserves/prices interact (France, the US, and — by
  construction of a global gold-silver TRADE market — the implicit "world price" that China's
  domestic gold price converged toward over the 18th century). It is NOT how Qing China's
  domestic monetary reserves worked, because China never ran a fixed gold:silver mint ratio to
  arbitrage against in the first place — China's gold:silver ratio was a MARKET/trade
  phenomenon (Q2/Q3's Dermigny arbitrage-shipping mechanism), not a policy-pegged one, so there
  was no "peg to defend" the way France had to defend 15.5:1 in 1873.
- **(a) a fixed ratio anchor (~1:15) is the right SIMPLIFICATION for most of the mod's map and
  both bookmarks**, precisely because both 1763 and 1815 sit in the post-convergence, pre-1873
  window where the ratio was in practice fairly stable near 1:14–15 worldwide (per Q2) — a full
  dynamic arbitrage simulation would be reproducing 150+ years of remarkably stable real-world
  behavior (the ratio did NOT gyrate wildly between 1750 and 1870; the big breaks are 1873+,
  outside the mod's timeframe) for very little payoff, UNLESS the mod specifically wants to model
  the 1870s bimetallic-collapse event as a late-game mechanic (a genuinely interesting option if
  the mod's timeline runs that far — see note below).
- **(c) leaving them fully independent (today's mod state) is NOT historically defensible for
  ANY power** — gold and silver were never priced independently of each other anywhere in this
  period; the ratio might have differed by region (Q2), but within any one region/power the two
  metals' relative value was always a meaningful, tracked, historically-attested number (~1:15 in
  the West by both bookmarks; converging to that same ~1:15 in China specifically by 1763). The
  mod's current two-independent-floating-goods design has no historical analogue.

**Recommended concrete mechanic**: treat gold and silver as **two goods whose prices are linked
by a ratio band, not fully independent, but also not literally pegged** — i.e., a soft version of
(a)+(b): anchor the ratio at ~1:15 (matching the converged, stable 1763/1815 reality), and let
each metal's own supply/demand (mining output events, trade flows, war finance demand for one
metal specifically) push the realized ratio away from 1:15 within a band, with a mean-reversion
pull back toward 1:15 representing the real arbitrage mechanism (Q3) that historically kept the
ratio from drifting far in this exact period. This gives the mod the historically-real MECHANISM
(arbitrage/Gresham pressure resists divergence) without requiring the mod to simulate the full
150-year convergence history (Q2) that's already over by 1763, or the 1873 collapse that hasn't
happened yet by either bookmark.

**Split by power, since the mod's China-fine-fidelity principle matters here specifically:**
- **Qing China specifically**: the gold:silver mechanic above should be understood as governing
  China's EXTERNAL/trade exposure to the world gold:silver ratio (i.e., how much gold China's
  merchants can arbitrage against incoming trade silver), NOT China's domestic monetary reserve
  mechanics. If the mod ever wants to model China's REAL domestic bimetallism with any fidelity,
  that is the **silver:copper-cash relationship** (Q4) — a FLOATING, not fixed-ratio, dual
  currency, which the mod's existing `backing_type = silver_standard` + separate chuan/silver
  fields in `se_CURRENCY.txt` (per `research/1763_QING_MONEY_SUPPLY.md`) already gestures toward
  more correctly than a gold:silver ratio would. **Do not conflate the two questions**: "should
  gold and silver be ratio-linked" (yes, per above, as a trade/reserve-valuation mechanic) is a
  DIFFERENT question from "should silver and copper cash be ratio-linked" (also yes, but as a
  FLOATING rather than pegged relationship, and that's the mechanic that actually drove Qing
  domestic monetary behavior — a separate #23/#71-adjacent design question, not this one).
- **Bimetallic Western powers (France, US, etc.)**: here the fixed-peg-with-Gresham-pressure
  mechanic (a)+(b) is closer to literally correct — these powers really did run a fixed statutory
  ratio, and really did experience Gresham-driven metal flows when the market ratio drifted from
  it (Q3). If the mod's Western powers ever get a bimetallic-collapse mechanic (a genuinely
  fun late-game event if the mod's 1815 bookmark timeline runs into the 1870s), THAT would be the
  moment to switch from "peg holds" to "peg breaks, metal floods in/out, power forced off
  bimetallism" — modelling the 1873 crisis directly rather than the smooth 1763/1815 baseline.
- **Britain**: already gold-monometallic (Q1) for both bookmarks in practice — silver for Britain
  specifically should probably NOT be ratio-linked to gold at all, consistent with silver's real
  status there as a capped subsidiary/token coinage rather than a competing reserve metal.

---

## Sources consulted (with access notes)

**Fetched and read (via WebFetch), general bimetallism/gold-standard/Gresham's Law:**
- Wikipedia, "Bimetallism" — fetched directly, full content extracted. Gives Croeseid origin
  (1:13.3, c.550 BCE), French 1803 15.5:1 law, US 1792 Coinage Act 15:1 (Hamilton), Latin Monetary
  Union 1865 (15.5:1, Belgium/Switzerland/Italy/France + Greece 1868), the 1873 "Crime of 1873"
  and French/LMU 1874/1878 abandonment, Friedman/Flandreau (pro-stability) vs Kindleberger/Redish
  (anti-stability) framing, Bryan's 1896 "Cross of Gold" speech, gold-supply-shock resolution
  (South Africa 1887+, Klondike 1896), and the 1971 Nixon "gold window" close as the final
  metallic-standard endpoint. **Solid tertiary source, consistent with everything else found.**
- Wikipedia, "Gresham's law" — fetched directly. Gives the "bad money drives out good" statement,
  Mundell's "if they exchange for the same price" qualifier, the 1717 Newton/guinea/shilling
  example (gold overvalued at 21 shillings → silver exports → de facto UK gold standard), the 1965
  US Coinage Act half-dollar debasement example, Hoppo's "only holds under price controls/fixed
  ratios" qualification, and "Thiers' Law" as the hyperinflation-era reverse case (Weimar 1923).
- Wikipedia, "Gold standard" — fetched directly. Gives Britain's 1717→1816 (Great Recoinage)→1819
  Act (1823 resumption target)→1844 Bank Charter Act sequence; Germany's 1871 Coinage Act/1876 full
  implementation as the trigger for the European cascade; Latin Monetary Union 1873 suspension;
  Scandinavian Union 1875; Netherlands 1875; Austria-Hungary 1892; Russia 1897; US 1873 Act/1879 de
  facto parity/1900 formal Gold Standard Act; Eichengreen's "only [by 1873] did countries settle on
  gold" framing.
- Wikipedia, "Silver standard" — fetched directly. Gives Qing China's silver-ingot-plus-copper-cash
  dual system, China's resistance to standardized silver coinage until 1890, China's silver
  standard's formal end in September 1935 (driven by the US Silver Purchase Program of 1934).
- American Economic Association (aeaweb.org), Friedman "Bimetallism Revisited" abstract page —
  fetched directly, full abstract extracted: Friedman's reversal of his own prior acceptance of
  "bimetallism is unstable/unsatisfactory... gold monometallism [is] superior," concluding "the
  conventional view is dubious, if not outright wrong." **Citation confirmed: Milton Friedman,
  "Bimetallism Revisited," Journal of Economic Perspectives 4:4 (Fall 1990), pp.85–104.** The
  page's abstract did not itself spell out the arbitrage-mechanism argument in full — that
  characterization in this digest's Q3 is inferred from the abstract's framing plus the Wikipedia
  "Bimetallism" article's own characterization of the Friedman/Flandreau side of the debate, and
  should be treated as **secondary-characterization-level, not a direct quote of Friedman's full
  mechanism**, pending a full-text read of the JEP article itself (paywalled/not fetched this
  session).

**Fetched at search-snippet level only (WebFetch on a search-engine results page, not the
underlying source) — flagged as weaker sourcing than a direct fetch:**
- Marc Flandreau, *The Glitter of Gold: France, Bimetallism, and the Emergence of the
  International Gold Standard, 1848-1873* (Oxford University Press) — snippet-level only. Gave:
  the 15.5:1 legal-peg framing, the 1848–1873 scope, the Franco-Prussian-War-triggered end of free
  silver coinage, and the "gold and silver supply shocks under bimetallism were less destabilizing
  than previously believed" characterization. **The book itself was not fetched/read; this is a
  search-result characterization of the book's argument, not a verified quote.**
- Akinobu Kuroda — profile/faculty pages and Academia.edu listing fetched at snippet level, but
  the JSTAGE article itself WAS fetched directly (see below) — the profile-level snippets
  corroborate (silver "used by weight rather than by count," concurrent-currencies research scope
  spanning India/China/Africa/Europe) but add no new claims beyond the direct article fetch.
- Richard von Glahn, *Fountain of Fortune: Money and Monetary Policy in China, 1000-1700* (UC
  Press, 1996) — snippet/summary level only (via a search-results synthesis, not the book itself
  or even a single dedicated review page). Confirms the book's scope and reputation ("first
  comprehensive study of state monetary policy from Song to early Qing," "a classic") but this
  session could **not extract a direct quote or specific claim about gold's non-reserve status in
  China** — that characterization in Q4 is this digest's own inference from the book's stated
  scope (a silver/bullion-flow-centered monetary-policy history) plus corroboration from Kuroda and
  the Silver-standard Wikipedia entry, NOT a verified von Glahn quote. **Flag: should be read
  directly (or via JSTOR/library access) before citing von Glahn's specific position on gold as
  a non-monetary-reserve metal as settled.**
- Alejandra Irigoin — snippet-level only (search-results synthesis, not a specific paper fetched).
  Gave the Spanish-American peso/"currency standard for the international economy" framing, silver
  "paramount in relations between China and the rest of the world since the 16th century," and the
  1820s Spanish coinage-monopoly-collapse framing. **No specific paper title/citation was pinned
  down this session** — "the silver question" is the task brief's own phrase for her general
  research area, not a single paper title this session verified exists under that exact name.
  Flag as under-cited; a follow-up session should locate and directly fetch her actual named
  papers (e.g. her 2009 *Journal of World History* piece already cited in
  `research/1763_CANTON_SILVER_INFLOW.md` as "Irigoin (2009)... cited 135" for the 1826–27
  silver-outflow-reversal date — that citation is solid; this digest's broader "silver question"
  framing is not independently re-verified).

**Directly fetched primary/secondary academic source, full content extracted:**
- Kuroda Akinobu, "Monetary Structure under the Last Chinese Empire and its Breakdown," *Socio-
  Economic History* (社会経済史学会) 57:2 (1991), pp.227–259, doi:10.20624/sehs.57.2_227 — fetched
  directly via J-STAGE, abstract/summary extracted. **This is the single strongest source in this
  digest for the Q4 silver-vs-copper-cash (not gold-vs-silver) clarification**: confirms Qing China
  ran silver (inter-regional) and copper cash (local) as its real dual-currency system, with
  **no fixed exchange ratio set between them** (a floating, not pegged, relationship — the
  opposite structure from Western fixed-ratio bimetallism), and that this arrangement shaped local
  autonomous-mint suppression and 18th-century regional-product overvaluation dynamics.

**Already on file in the repo (re-used per the task's own framing, not re-researched this
session):**
- `research/RESEARCH_TRADE_GOOD_PRICES_1763.md` §A1 — the two-source-corroborated China gold:silver
  ratio series (1:8–10 early Qing → ~1:14–15 by 1750–63), citing Melitz (2017) CEPII working paper
  (itself citing Peng Xinwei 彭信威, von Glahn 2003, Dermigny 1964, Cantillon, Soetbeer 1879) —
  Melitz's paper was READ IN FULL TEXT in that earlier session (per that digest's own sourcing
  notes), so this is a solid inherited number, not re-verified from scratch here.
- `research/1763_QING_MONEY_SUPPLY.md` — the ~700–800 wén/tael market silver:copper-cash exchange
  rate for the 1750s–1800 window, sourced to ChinaKnowledge.de, Wang Hongbin 王宏斌 (2015), and
  Springer's *Monetary System of China under the Qing* — used in this digest's Q4 as the concrete
  "floating, not fixed" rate that instantiates Kuroda's "no fixed ratio" claim.
- `research/1763_CANTON_SILVER_INFLOW.md` — silver inflow volumes/reserve figures, Irigoin (2009)
  citation for the 1826–27 outflow-reversal date specifically (a different, better-pinned Irigoin
  citation than this digest's own under-cited "silver question" framing above).

---

## What could NOT be verified this session (explicit flags)

1. **Friedman's specific arbitrage-mechanism argument, in his own words** — only the abstract was
   fetched; the full JEP 1990 article (pp.85–104) was not read. The Q3 characterization of his
   argument is a reasonable secondary-source-corroborated inference (Wikipedia's own framing of the
   Friedman/Flandreau side of the debate), not a direct quote.
2. **Flandreau's exact argument and evidence in *The Glitter of Gold*** — snippet-level only, book
   itself not fetched. The specific mechanism claims attributed to him here should be treated as
   search-result paraphrase, not verified quotation.
3. **Von Glahn's specific stated position on gold's non-monetary-reserve status in China** — this
   digest's Q4 claim rests on an INFERENCE from the book's stated scope plus corroboration from
   Kuroda and the Silver-standard Wikipedia article, not a direct quote from *Fountain of Fortune*
   itself. This is the single most important unverified claim in the digest, since it's the
   evidentiary anchor for the "gold was commodity/store-of-value, not reserve metal, in China"
   answer to Q4 — **recommend a follow-up session with direct JSTOR/library/archive.org access to
   von Glahn's actual text before treating this as fully settled.**
4. **Irigoin's specific named paper(s) on "the silver question"** — no single citation was pinned
   down this session (distinct from the ALREADY-VERIFIED Irigoin 2009 citation in
   `1763_CANTON_SILVER_INFLOW.md` for the 1826–27 date, which is solid). The broader "silver
   question" framing in this digest is search-synthesis-level, not a verified paper.
2. **Redish's specific arguments** (named in the task brief alongside Friedman/Flandreau) — not
   independently located or fetched this session at all; her position is known only via Wikipedia's
   characterization of her as being on the "anti-bimetallic-stability" side alongside Kindleberger.
   No direct citation to a specific Redish paper/book (e.g. her *Bimetallism: An Economic and
   Historical Analysis*, Cambridge UP, which the task brief itself names) was verified this session.
3. **1815-specific British monetary regime nuance** (the Restriction period, 1797–1821, suspended
   gold convertibility) — flagged in Q1 as a real complication for the mod's 1815 bookmark
   specifically, but not resolved with dedicated sourcing this session; it is asserted from general
   background knowledge of the period rather than a source fetched in this pass. **Needs a
   dedicated follow-up if the mod wants Britain's 1815-specific monetary status modelled precisely
   (paper pound under wartime suspension, not yet the restored 1821 gold sovereign standard).**
4. **A dedicated 1815-specific gold:silver ratio figure** (as opposed to the 1763-era convergence
   already sourced in the trade-goods digest) — not found this session; inferred by extrapolation
   ("stable near 1:15 for the whole pre-1873 stretch") rather than a direct period source.
5. **Chinese-language direct sourcing on gold's role in China specifically** (as opposed to the
   already-strong Chinese-language sourcing on the gold:silver RATIO number in the existing
   trade-goods digest) — this session's Q4 answer draws only on English-language
   secondary/tertiary sources (Kuroda, von Glahn via summary, Irigoin via summary); a dedicated
   Chinese-language pass (e.g. directly on Peng Xinwei's own discussion of gold's monetary status,
   not just the ratio number already extracted from him) was not attempted this session and would
   strengthen Q4 specifically.
