# Industrial-Revolution production chains + Late-Qing industrialisation — sourced research digest (2026-08-10)

For **#69** (Modern Industry buildings ↔ manufactured-goods var-sim join) — see `design/DIAGNOSIS_INDUSTRY_TWO_SYSTEMS_69.md`
for the Stage-0 engine diagnosis (two parallel factory representations, not a dead driver). This is the Stage-1 grounding:
what the REAL production chains + dates + arsenal outputs were, so whichever join model the design stage picks
(buildings feed the counter / unify / leave parallel) rests on correct history.

**Discipline:** WebFetch against named academic/encyclopedic sources; scholarly monographs distinguished from
Wikipedia/tertiary reference (Wikipedia is used extensively below for VERIFIABLE dates/facts — it is flagged as
tertiary, not a substitute for the named monographs, several of which I could not get full text of in this session
— see the confidence tags per claim and the Sources list). Numeric input:output ratios are RARE in the tertiary
sources I could reach; every ratio below is flagged with where it came from, and gaps are stated as gaps, not
invented.

---

## 1. The core Industrial-Revolution production chains + dating

### 1a. Iron → steel chain (the mod's `coal`/`iron`/`steel` goods)

| Stage | Process | Key figure / date | What it does | Confidence |
|---|---|---|---|---|
| Fuel | **Coke smelting** replaces charcoal | **Abraham Darby I, Coalbrookdale, 1709** | Coke's crushing strength let blast furnaces grow taller/larger; broke the charcoal/woodland supply ceiling | HIGH (Wikipedia *Coke (fuel)*, citing S.H. Beaver 1951; corroborated by Wikipedia *Blast furnace*) |
| Ore→pig iron | **Blast furnace** (coke-fired) | spreads slowly after 1709; "coke iron initially only used for foundry work" before general adoption; anthracite variant 1837 (Ynyscedwyn, Wales), adopted in the US 1839 (Lehigh Crane Iron Co.) | Iron ore + coke + limestone → **cast/pig iron** (brittle, high-carbon) | HIGH (Wikipedia *Blast furnace*) |
| Pig→wrought | **Puddling** | **Henry Cort, patented 1784, Fontley, Hampshire** | Reverberatory furnace, oxidising atmosphere decarburises pig iron → malleable **wrought iron**. Solved the specific problem that coke-smelted pig iron was sulphur-contaminated ("red-short"/brittle) and couldn't be converted by the old charcoal finery method | HIGH (Wikipedia *Puddling (metallurgy)*) |
| Fuel efficiency | **Hot blast** | **James Beaumont Neilson, patented 1828** | Preheating blast air to ~149°C cut fuel needed **from 8.06 to 5.16 long tons of coal per ton of iron produced (~36% reduction)** — the one directly-sourced input:output figure recovered this session | HIGH (Wikipedia *Hot blast*) — **this is the ratio to use for the mod's coal:iron recipe tuning, flagged as the strongest sourced anchor found** |
| Wrought→bulk steel | **Bessemer process** | **Henry Bessemer, patented 1856**, demonstrated 1856, "successful operation by 1864"; American Wm. Kelly claimed independent 1851 discovery (patent priority 1857, disputed) | Blowing air through molten pig iron in a converter to decarburise — **10–20 minutes to convert 3–5 tons**, vs a full day+ by puddling/older methods. Cost collapsed **£40/long ton → £6–7/long ton**. THIS is the event that makes bulk cheap steel possible — before ~1860 "steel was an expensive product, made in small quantities... for swords, tools and cutlery; all large metal structures were made of wrought or cast iron" (Wikipedia *History of the steel industry (1850–1970)*) | HIGH |
| Wrought/bulk steel (2) | **Siemens-Martin open-hearth** | Carl Wilhelm Siemens' regenerative furnace (claimed 1857, 70–80% fuel saved) adapted for steel by **Pierre-Émile Martin, 1865** (licensed from Siemens) | Slower, more controllable than Bessemer; crucially **could remelt scrap** and avoided Bessemer's nitrogen-embrittlement. Overtook Bessemer in the UK by **1900**; "after 1890 the Bessemer process was gradually supplanted by open-hearth steelmaking" | HIGH (Wikipedia *Open-hearth furnace*, *History of the steel industry*) |

**KEY DATING TAKEAWAY for the mod's tech-gate:** bulk/cheap **steel is an 1856–1860s good, full stop** — it did not exist as a mass-produced commodity before that. Pre-1856, "steel" existed only as small-batch **crucible/blister steel** for tools and cutlery — a luxury/craft good, not an industrial input. The mod's `steel` trade-good tech-gate should sit at Bessemer (~1856) at the earliest, with a *better* steel-industry modifier (cheaper/more) unlocking again at Siemens-Martin (~1865, dominant ~1890-1900). **Before 1856, the iron chain terminates at wrought iron**, not steel — wrought iron is the correct "structural metal" good for 1709–1850s (rails, machinery, ships' frames of the early railway age were wrought iron, not steel, until the 1870s-80s).

**Production growth as an independent cross-check (not a per-unit ratio, but scale evidence):** British pig iron output: 1840 = 1.3M tons → 1870 = 6.7M tons → 1913 = 10.4M tons. US steel: 1875 = 380,000 tons → 1920 = 60M tons. German steel: 1885 = 1M tons → 1918 = 19M tons. (Wikipedia *History of the steel industry (1850–1970)*, HIGH confidence for the raw figures, though the article itself does not cite primary sources inline).

**Unsourced/weak claim flagged:** I could NOT recover a directly-sourced tons-of-coal-or-coke-per-ton-of-pig-iron or per-ton-of-steel ratio from Bessemer/open-hearth-era sources this session (Wikipedia's *Bessemer process*, *Pig iron*, and *Blast furnace* articles explicitly have none). The **Neilson hot-blast 8.06→5.16 long tons coal/ton iron figure is pre-Bessemer (1828, charcoal-era wrought-iron chain)** — use it as the best available order-of-magnitude anchor for the coal:iron recipe leg, but do not present it as a Bessemer-era steel ratio without further sourcing. Recommend if precision is later needed: consult Allen (2009) Table data directly (not accessed full-text this session — see Sources) or a metallurgical-engineering reference, not Wikipedia.

### 1b. Textiles — cotton → thread → cloth (the mod's `textile_fibres`/`clothing`/`silk_cloth` goods)

| Stage | Machine | Inventor / date | Effect | Confidence |
|---|---|---|---|---|
| (pre-mechanised weaving demand shock) | **Flying shuttle** | John Kay, 1733 | Doubled a weaver's throughput, creating the yarn-supply bottleneck that spinning mechanisation answers | HIGH |
| Cotton→thread (jenny) | **Spinning jenny** | **James Hargreaves, 1764–65** | Multi-spindle hand-powered spinning; 8+ spindles per worker; but yarn too weak for warp threads | HIGH (Wikipedia *Spinning jenny*) |
| Cotton→thread (frame) | **Water frame** | **Richard Arkwright, patented 1769**; first factory-scale mill **Cromford, 1771** | Water-powered, produces **strong** warp-quality thread; began the factory system proper (the mill, not the cottage, as the unit of production) | HIGH |
| Cotton→thread (mule) | **Spinning mule** | **Samuel Crompton, 1779** | Combined jenny's fineness with the frame's strength; became the dominant spinning machine | HIGH |
| Thread→cloth | **Power loom** | **Edmund Cartwright, patented 1785**; commercially reliable only much later | Mechanised weaving; deliberately LAGGED spinning — "spinning developed first and, until [~]1830, the handloom was still more important economically than the power loom" | HIGH (Wikipedia *Power loom*) |

**Power-loom adoption curve (UK, direct count):** 1803 = 2,400 looms → 1820 = 14,650 → 1829 = 55,500 → 1833 = 100,000 → 1857 = 250,000. Crossover point (power loom > handloom in economic importance) **≈ 1830**. (Wikipedia *Power loom*, HIGH confidence for the table itself.)

**Mechanisation-lag lesson for the mod:** spinning mechanised ~20 years before weaving (jenny 1764 vs power loom 1785, dominance 1830 vs mule dominance ~1790s-1800s). If the mod's `textile_fibres → thread → cloth` chain has a single flat tech-gate, it is missing this real 40–65 year internal stagger; a historically-grounded design should gate **thread-production tech before cloth-production tech** by roughly a generation.

**Chain classification:** cotton (raw good) → thread/yarn (**INTERMEDIATE**, not directly consumed/traded as a final good in most economies) → cloth (**FINAL** consumer good, though itself an input to clothing/sails/etc. in other recipes — a good can be final in one recipe and intermediate in another, which the mod's BOM system already allows).

### 1c. Machine-goods / capital-goods chain (the mod's `machine_parts`/`motors` goods)

| Stage | Development | Date | Confidence |
|---|---|---|---|
| Precision boring | **Wilkinson's cylinder-boring machine** | 1774, first used to bore Boulton & Watt's first commercial engine, 1776 | HIGH |
| Separate condenser (efficiency leap) | **Watt's steam engine** | Condenser concept 1765; **first commercial engine 1776** (Boulton & Watt partnership); used ~75% less fuel than Newcomen | HIGH |
| Rotative power (freed factories from waterwheels) | Watt's sun-and-planet gear | 1781 | HIGH |
| Interchangeable-parts precision | **Maudslay's screw-cutting lathe / master gauges** | c. 1797–1809 | HIGH |
| Surface-plate precision (scraping) | **Whitworth**, after joining Maudslay's shop | early 19th c. | HIGH |

**Chain shape:** machine tools (capital equipment, itself built from iron/steel) → precision **machine parts** (INTERMEDIATE — gears, cylinders, fittings) → **engines** (Watt-type stationary steam engines, 1776+) as a FINAL capital good that is then itself an input to factories, pumps, locomotives, ships. This is a genuinely recursive capital-goods chain (machines building machines) — the mod's `machine_parts → motors/engines` recipe direction is historically the right shape; the tech-gate anchor for "engines exist as a buildable/tradeable good" should be **1776 (Watt/Boulton commercial engine)**, with a precision-parts prerequisite dated to **1774–1809 (Wilkinson→Maudslay)**.

### 1d. Intermediates vs. final goods — classification summary

| Good | Class | Why |
|---|---|---|
| Coal | Raw/base input | Mined; the universal enabling fuel (see §2) |
| Coke | INTERMEDIATE | Processed from coal specifically for smelting; not itself a consumer good |
| Pig/cast iron | INTERMEDIATE | Brittle, unusable directly for most purposes; must be puddled or steeled |
| Wrought iron | Could be FINAL (rails, structural iron, tools) or INTERMEDIATE (stock for further working) — context-dependent, same as the mod's existing dual-use goods | |
| Steel (bulk, post-1856) | Same dual role, higher up the value chain — FINAL for rails/plate, INTERMEDIATE for machine parts/ships | |
| Raw cotton | Raw input | |
| Thread/yarn | INTERMEDIATE | Not a consumer good in itself |
| Cloth | FINAL (as clothing/consumer good) but INTERMEDIATE if consumed by e.g. a sailmaking or uniform recipe | |
| Machine tools | Capital good — INTERMEDIATE in the sense of being an input to *production of other goods*, not consumed by pops | |
| Machine parts | INTERMEDIATE | |
| Engines | FINAL capital good — sold/deployed, not consumed by pops, but represents an end-state of that sub-chain | |

This matches the general economic-history convention: **intermediates are inputs consumed entirely within a single further production step (coke, thread, pig iron, machine parts)**; **finals are either consumed by pops/end-users or represent a completed capital asset (cloth, rails, ships, engines)**. The mod's existing BOM design (recipes consuming other tradegoods) already encodes this correctly in structure — the research gap was dating, not shape.

---

## 2. Coal as the enabling input — Wrigley's energy argument

**Confidence: MEDIUM-refracted.** I could not retrieve E.A. Wrigley's *Energy and the English Industrial Revolution*
(Cambridge UP, 2010, ISBN 978-0-521-76693-7 — bibliographic detail confirmed HIGH via Wikipedia *E.A. Wrigley*) in
full text or via a reachable scholarly review this session (JSTOR/Cairn/T&F reviews all returned 403; EH.net's
book-review URL for it 404'd). The core Wrigley thesis as commonly summarised in the literature — **that pre-industrial
("organic") economies were fundamentally capped by the annual solar/biomass energy flux available from a fixed land
area (wood, fodder, human/animal muscle), and that Britain's coal reserves let it substitute a stock of fossilised
solar energy for a land-area flow, decoupling growth from the Malthusian land ceiling** — is WELL-ESTABLISHED in the
Great-Divergence literature (it is explicitly the mechanism Pomeranz invokes when arguing Britain's coal-plus-New-World
resources let it escape the constraint China faced; see §4) but I am flagging that I have NOT verified Wrigley's own
book text directly in this session — treat the "organic economy vs mineral-based energy economy" framing as
**attributed to Wrigley by the secondary Great-Divergence literature, not confirmed against his primary text here.**
This is a real gap; if it matters for shipping copy, someone should pull the book or a JSTOR review directly.

**What IS directly sourced (Wikipedia, HIGH confidence for the plain facts):** every stage of the iron/steel chain in
§1a runs on coal or its derivative coke — smelting (coke), puddling (reverberatory furnace, coal-fired), Bessemer/
Siemens-Martin (coal-fired furnaces and — critically — the STEAM ENGINES driving the air blast). British coke-industry
scale evidence: "by 1870, 14,000 beehive ovens on the West Durham coalfields, producing 4 million long tons annually";
British iron-industry coal demand rose from ~1M tons/yr (1850s) to ~7M tons/yr (1880). The Watt steam engine (§1c) is
ITSELF a coal-burning machine that then drives every other mechanised process (spinning mules could be steam- as well
as water-powered from the 1780s-90s; blast-furnace air blasts, boring machines, eventually locomotives and ships).
**So the dependency graph is: coal → (a) direct smelting fuel for the iron/steel chain, AND (b) steam power that
drives every OTHER chain (textile mechanisation beyond water-power sites, machine tools, later rail/naval transport
of all goods).** Coal is not one input among many — it is the fuel substrate the whole tech-tree sits on, which is
exactly Wrigley's point even where I can't cite his own pages directly.

**Design implication:** the mod's `coal` good should carry unusually broad demand-fan-in (it already does — DEMAND_svalues.txt shows coal consumed by bronze, alcohol, steel, chemicals, steel_ships, glass, refined_sugar) — that breadth is HISTORICALLY CORRECT, not over-scoped. If anything, coal's centrality argues coal-supply shocks (mine flooding, blockade, transport cost) should be a more visible bottleneck lever in the sim than most other raw goods, mirroring its real economic centrality.

---

## 3. Late-Qing Self-Strengthening industrialisation (洋務運動) — the named works

All four dates below are corroborated across at least two independently-fetched sources this session (Wikipedia's
dedicated articles + the *Self-Strengthening Movement* overview article), which is as strong as tertiary
cross-referencing gets without primary-document access. The monographic literature (Kennedy, Kwang-Ching Liu,
Feuerwerker — see Sources) is the correct next step for anyone needing tonnage/output precision beyond what's below;
I could reach only their existence/topic via Wikipedia bibliography citations, not their argued content, this session
— flagged explicitly per entry.

| Enterprise | Chinese name | Founding date | Founder(s) | Output | Confidence |
|---|---|---|---|---|---|
| **Jiangnan Arsenal** | 江南製造總局 | **1865**, Shanghai | Planned under Zeng Guofan (as Viceroy of Liangjiang); established in practice by Li Hongzhang | Rifles/arms and ships; first domestically-produced steamboat **1868 (the *Huiji*)**; first domestically-produced steel **1891**; also ran a language school + translation bureau (143 Western books translated 1868–1879) | HIGH (Wikipedia *Jiangnan Arsenal*, cites Thomas L. Kennedy directly + Adrian A. Bennett on John Fryer) |
| **Fuzhou/Foochow Navy Yard** | 福州船政局 | Ordered **1866**, construction from **1867**, Mawei near Fuzhou | **Zuo Zongtang** (initiator) and **Shen Baozhen** (first director) — the task's naming of Zuo+Shen for this yard is confirmed | Warships; first ship (150hp *Wan Nien Ching*/"Qing Forever") launched **June 1869**; the ironclad-precursor cruiser *Yangwu* built 1872; also founded the **Fuzhou Naval College (1866)** for navigation/engineering training. French contract staff (Prosper Giquel, Paul d'Aiguebelle) recruited ~40 European engineers; workforce reached 2,000+ by 1872; 5-year budget ~3M taels. Badly damaged in the 1884 Sino-French War, rebuilt after | HIGH |
| **Kaiping Mines** | 開平礦務局 | Established **1877–78** (sources split — company chartered 1878 under Tong King-sing/Li Hongzhang; mine operations from 1877, "production began 1881" per one Wikipedia figure) | Li Hongzhang (patron); Tong King-sing/Zhou Xuexi (management); Herbert Hoover later chief engineer (much later, Boxer-era) | Coal; output reached **187,000 tons by 1892** (vs 300,000 tons then still imported); peak **1.4M tons/yr** in the 1881–1912 span. Built the **Kaiping Tramway (1881)** — China's first surviving standard-gauge railway, ~30 miles, moving coal to river transport at Beitang; the "Rocket of China" locomotive entered service 9 June 1881 | HIGH-for-dates, MEDIUM for the exact 1877-vs-1878 founding year (genuine source disagreement, both plausible: mine survey/start 1877, formal company charter 1878) |
| **Hanyang Ironworks** | 漢陽鐵廠 | Ordered from England under **Zhang Zhidong**; construction through the late 1880s; **production began 1894** (per Zhang Zhidong's own Wikipedia bio) — the task's "1890-94" bracket is consistent with this: ordered/built 1890, first iron/steel output 1894 | Zhang Zhidong (as Viceroy of Huguang) | Iron and steel — widely characterised (task's own framing, and consistent with the broader Self-Strengthening literature) as **China's first modern INTEGRATED iron-and-steel works** (ore mining, smelting, and finishing under one combine, later folded with Daye ore and Pingxiang coal into the **Hanyeping Coal & Iron Co.** — I could NOT get a dedicated Wikipedia article on Hanyeping this session, 404, so the combine's exact incorporation date is a GAP; Sheng Xuanhuai took over the works in **1896** per the *Self-Strengthening Movement* article) | MEDIUM-HIGH for the works itself (1894 production start well corroborated); MEDIUM for "first integrated steelworks" superlative (consistent with the literature's general framing but not independently verified against a named scholar's exact wording this session — flagged as the kind of claim Feuerwerker's monograph would need to confirm precisely) |

**Hanyang Arsenal ≠ Hanyang Ironworks — a distinction worth keeping straight in the mod's naming.** Wikipedia's dedicated
*Hanyang Arsenal* article describes a **separate facility**, "originally the Hubei Arsenal," founded **1891** by Zhang
Zhidong, producing **rifles** (magazine rifles, Gruson quick-fire guns, cartridges; later the famous Type 88 and
Chiang Kai-Shek rifles), production beginning 1895 after a 1894 fire, closing 1947. It drew on "iron and coal mines"
in the surrounding area (implicitly the Ironworks) but is textually distinct from the Ironworks (steel plant) itself.
**If the mod's `qing_steel_works_building` (comment says "漢陽鐵廠, 1891/94") is meant to represent the Ironworks
specifically (as its in-code comment states — "steel for rails, ships, machinery and modern arms"), that is the
correct enterprise; the Hanyang ARSENAL (rifle factory) is a related-but-separate historical entity the mod does not
currently appear to model as its own building** — noted for design awareness, not necessarily a gap to fill.

**Zhang Zhidong's other enterprises (context, not separately modelled arsenals per the task's four):** mint, tanneries,
tile/silk factories, paper/cotton/woolen mills, and — matching `qing_textile_mill_building`'s in-code citation — the
**Hubei Textile Mill**, whose profits were explicitly redirected to fund the Ironworks (per the *Self-Strengthening
Movement* article). This corroborates the mod's building comment ("湖北織布局 1889") as historically grounded.

**Cross-check against the mod's existing building files:** `qing_industry_buildings.txt`'s in-code historical comments
(steel works 漢陽鐵廠 "1891/94"; textile mill 機器織布局 "1878/90… 1889"; machine works 江南製造局 "1865"; navy yard
福州船政局 "1866"; coal mine 開平礦務局 "1878") are **all consistent with the sourced dates above** — the prior
buildings-research pass (2026-07-27, per the file header) got the history right. This digest's main NEW contribution
is (a) the precise Bessemer/open-hearth dating that pins down when the *generic* `steel` tradegood itself should be
buyable/tradeable (§1a, ~1856/1865, well AFTER the Qing-specific works start construction ~1890 — i.e. Hanyang is
catching up to a technology already ~35 years old in the West, which is itself a historically important point: the
Self-Strengthening enterprises were adopting mature, not frontier, Western technology) and (b) the
Hanyang-Arsenal-vs-Ironworks naming distinction.

---

## 4. The Great Divergence framing — why China didn't industrialise early (brief, design-flavour)

**Confidence: HIGH for the framing as commonly presented; MEDIUM for exact page-level fidelity to the two
monographs, neither of which I read in full text this session — both summaries below are drawn from Wikipedia's
dedicated articles on the books/concepts, which is a legitimate tertiary source for a framing paragraph but not a
substitute for the primary texts if a designer needs to quote them directly.**

Kenneth Pomeranz's *The Great Divergence: China, Europe, and the Making of the Modern World Economy* (Princeton UP,
2000; John K. Fairbank Prize 2001) argues that as late as the early-to-mid 18th century, the most developed regions of
Qing China — above all the **Yangzi Delta** — were roughly on par with the most developed parts of Europe by measures
like grain wages and commercial sophistication (paralleling the mod's own High-Qing commercial-flourishing framing).
What actually diverged was **geography and access to two very specific windfalls**: (1) Britain's coal deposits sat
close to its centres of production, while China's largest coal reserves were remote from the Yangzi Delta, making
coal transport to the economic core prohibitively costly (contrast the mod's Kaiping/Hanyang siting further north,
away from the Yangzi Delta's commercial heartland — historically apt); and (2) European access to New World "ghost
acreage" — Pomeranz's estimate that New World wood/cotton/wool imports saved England the equivalent of 23–25 million
acres of its own land — freed European land and labour from subsistence production for manufacturing in a way China's
comparably-developed core could not replicate. Mark Elvin's earlier *The Pattern of the Chinese Past: A Social and
Economic Interpretation* (Eyre Methuen/Stanford UP, 1973) offers a complementary, more INTERNAL explanation: the
**"high-level equilibrium trap"** — pre-industrial Chinese production methods (intensive wet-rice agriculture,
sophisticated handicraft manufacture) had become so efficient, and labour so cheap and abundant relative to capital,
that there was no economic incentive to mechanise; a supplementary intellectual-history strand of his argument holds
that Confucian moral/social philosophy had displaced the more nature-focused inquiry of philosophical Taoism as the
dominant elite paradigm, thinning the base for the kind of natural-philosophical inquiry that fed Western mechanical
tinkering. (The two theses are not presented as in direct competition anywhere I could verify this session — Pomeranz
is geography/resource-external, Elvin is factor-price/institutional-internal; both are commonly cited together as
complementary halves of the "why not China" question, but I did not find a source directly reconciling or ranking
them.) **Design payoff:** this is exactly why the mod's Self-Strengthening arsenals (§3) are a **late, defensive,
state-sponsored catch-up effort (1860s-90s) responding to military crisis (Taiping, Second Opium War, Sino-French,
Sino-Japanese)**, not an organic mid-century industrial takeoff — the historical record supports gating them
strictly as reactive/top-down institutions (viceroy-driven procurement of foreign plant and expertise) rather than
private entrepreneurial ventures, which the mod's existing owner-culture-gated, high-civilization-value building
allow-conditions already reflect correctly.

---

## 5. Design implications for the mod

- **`steel` (bulk/tradeable good) tech-gate should not predate ~1856 (Bessemer), with a meaningful second jump at
  ~1865-1890 (Siemens-Martin dominance).** Before that, the iron chain's terminal *bulk* good is **wrought iron**
  (Cort's puddling, 1784) — if the mod currently allows `steel` to appear meaningfully before the mid-19th century, that
  is an anachronism the tech requirements should close off; check `tech_manufactories`'s current placement (it requires
  only `tech_mechanical_tools`, no date floor visible in the file read this session) against whatever era that
  invention unlocks in the tech tree's overall pacing.
- **`coke` and `pig/cast iron` are INTERMEDIATES**, not directly tradeable/consumer-facing goods in most historical
  economies — if the mod's BOM treats them as such already (recipes consuming them, not pops), that's correct; don't
  add a pop-consumption sink for coke.
- **Textile mechanisation has a real ~20-65 year internal stagger (spinning 1764-79 vs weaving dominance ~1830)** — if
  the mod's `thread`/`cloth` (or `textile_fibres`/`clothing`) tech-gates currently unlock together, splitting them by
  a meaningful tech-tier gap would be more accurate; spinning-side mechanisation should unlock distinctly earlier.
- **`machine_parts`/`motors`(engines) should not be tradeable before ~1774-76 (Wilkinson boring machine / Watt's
  first commercial engine)** — this is a capital-goods chain (machines building machines), and its recursive
  character (machine tools → precision parts → engines → more machine tools) is worth preserving in the BOM rather
  than flattened to a single tier.
- **Coal is not "just another raw good"** — its demand fan-in across nearly every manufactured good (already true in
  `INDUSTRY_svalues.txt`: bronze, alcohol, glass, steel, chemicals, steel_ships, refined_sugar all consume coal) is
  historically correct per Wrigley's/the Great-Divergence literature's energy argument (§2) and should be preserved/
  reinforced, not trimmed as "over-coupled."
- **China's Self-Strengthening buildings are correctly late (1860s-90s) and correctly state-driven/reactive** per the
  Great-Divergence framing (§4) — the mod's existing culture-gated, high-civilization-value, viceroy-flavoured
  building `allow` blocks match the history. The one concrete correction/addition this research surfaces: **Hanyang
  Arsenal (rifles, founded 1891) is historically distinct from Hanyang Ironworks (iron/steel, production from 1894)**
  — worth a design note if #69's building↔counter join ever wants a dedicated small-arms-manufacturing Qing building
  separate from the steel works.
- For #69's actual join-model decision (Option A/B/C in the diagnosis doc): this research doesn't resolve which
  option to pick, but it DOES confirm the underlying history supports a **staged, date-gated join** — i.e. whichever
  option is chosen, the trigger dates for the generic `IND_` buildings (coal_mine → `tech_mining_rails`; blast_furnace
  → `tech_manufactories`; electric_plant → `tech_electricity`) and the Qing-specific buildings (steel_works, textile_mill,
  machine_works, navy_yard, coal_mine, all → various inventions) should be checked against §1's dates once the
  mod's invention-tech-to-calendar-year mapping is known (not resolved in this session — the `.txt` files define
  invention prerequisites/`requires` chains but not fixed calendar dates, since Imperator's invention system is
  progress-based, not year-gated. This is a genuine limitation: the MOD's own tech pacing, not real-world dates,
  ultimately determines when players reach steel/engines/etc., and this research cannot by itself guarantee 1763-start
  games hit Bessemer-steel around 1856-equivalent progress. That calibration is a SEPARATE, follow-on design question).

---

## 6. Sources (confidence-tagged)

### Scholarly monographs named in the task (existence/topic confirmed; full-text NOT accessed this session — treat citations of their ARGUMENTS above as drawn from secondary paraphrase/Wikipedia bibliography entries, not primary verification)
- David S. Landes, *The Unbound Prometheus: Technological Change and Industrial Development in Western Europe from
  1750 to the Present* (Cambridge UP, 1969). — Existence/date HIGH confidence; thesis content NOT verified this
  session (Wikipedia bio gave no thesis detail).
- Robert C. Allen, *The British Industrial Revolution in Global Perspective* (Cambridge UP, 2009). — Could not reach
  any content this session (dedicated Wikipedia article + JSTOR both 404/403'd). GAP — the coal/high-wage
  induced-innovation argument commonly attributed to Allen is NOT independently confirmed here; do not cite Allen's
  specific numbers from this digest.
- Robert C. Allen, *Global Economic History: A Very Short Introduction* (Oxford UP, 2011). — Not accessed this
  session at all. GAP.
- E.A. Wrigley, *Energy and the English Industrial Revolution* (Cambridge UP, 2010). — Bibliographic detail HIGH
  confidence (Wikipedia author page); thesis content MEDIUM (attributed via secondary Great-Divergence framing, not
  the book's own text — see §2 caveat).
- Kenneth Pomeranz, *The Great Divergence: China, Europe, and the Making of the Modern World Economy* (Princeton UP,
  2000). — Thesis summary HIGH confidence (dedicated Wikipedia article on the book gave substantive content,
  cross-checked against Pomeranz's own bio page).
- Mark Elvin, *The Pattern of the Chinese Past: A Social and Economic Interpretation* (Eyre Methuen/Stanford UP,
  1973). — Thesis summary (high-level equilibrium trap) HIGH confidence (dedicated Wikipedia article gave
  substantive content); scholarly reception/critique of the trap concept NOT found this session — GAP.
- Thomas L. Kennedy — cited BY NAME as a source in Wikipedia's *Jiangnan Arsenal* article ("The Kiangnan Arsenal in
  the Era of Reform 1895-1911"); his own argument's content not independently accessed — MEDIUM (existence + topic
  confirmed, content not verified).
- Kwang-Ching Liu — confirmed as author of the Self-Strengthening chapter in *The Cambridge History of China* and of
  *Anglo-American Steamship Rivalry in China, 1862-1874* (Harvard UP, 1962); his specific assessment of arsenal
  output was NOT retrievable this session — GAP, flagged explicitly in §3's table note.
- Albert Feuerwerker, *China's Early Industrialization: Sheng Hsuan-huai (1844-1916) and Mandarin Enterprise*
  (Harvard UP, 1958). — Existence + general thesis direction (traditional Chinese values as an obstacle to
  modernity, later contested by Paul Cohen) confirmed MEDIUM via Wikipedia bio; no output/tonnage data from
  Feuerwerker specifically was recovered — GAP for the quantitative claims in §3, which rely on Wikipedia's
  dedicated arsenal articles instead.

### Tertiary/reference sources actually fetched and used for verifiable facts + dates (Wikipedia, HIGH confidence for the specific factual claims cited, but tertiary — not a substitute for the monographs above)
- *Coke (fuel)*, *Puddling (metallurgy)*, *Bessemer process*, *Open-hearth furnace*, *Blast furnace*, *Hot blast*,
  *Pig iron*, *History of the steel industry (1850–1970)* — iron/steel chain dating + the one directly sourced
  input:output ratio (Neilson hot blast, §1a).
- *Spinning jenny*, *Power loom*, *Cotton mill* — textile mechanisation chain + UK power-loom adoption table.
- *Watt steam engine*, *Machine tool* — capital-goods chain.
- *Jiangnan Arsenal*, *Foochow Arsenal*, *Kaiping Mines*, *Kaiping Tramway*, *Hanyang Arsenal*, *Zhang Zhidong*,
  *Self-Strengthening Movement* — the four named arsenals/mills' dates, founders, and output (§3). Note: no
  dedicated Wikipedia article exists for "Hanyang Ironworks"/"Hanyeping" as such (both attempted URLs 404'd) — its
  detail is reconstructed from the *Self-Strengthening Movement* overview article + *Zhang Zhidong*'s bio page, which
  is thinner sourcing than the other three enterprises — flagged as the weakest-sourced row in §3's table.
- *Kenneth Pomeranz*, *The Great Divergence*, *High-level equilibrium trap*, *Mark Elvin* — Great Divergence framing (§4).
- *David Landes*, *Kwang-Ching Liu*, *Albert Feuerwerker*, *E. A. Wrigley*, *Robert Allen (economist)* — author
  bio/bibliography pages, used only to confirm existence/dates of the named monographs, not their content (multiple
  404s on the Allen page specifically — GAP).

### Sources attempted and NOT reachable this session (explicit gaps, not silently dropped)
- EH.net Encyclopedia (iron/steel industry article; Wrigley book review) — both targeted URLs 404'd; the EH.net
  articles that DID resolve (via the encyclopedia index) were about 19th-c. US coal and women workers, not directly
  on point.
- JSTOR (Allen review, Elvin critique) — 403 Forbidden (paywalled/blocked for automated fetch).
- Cambridge Core, Taylor & Francis, Cairn.info (Wrigley book page/reviews) — 404/403.
- Hanyeping Coal & Iron Co. dedicated article — 404 (no such Wikipedia page found under several title guesses).

**Overall confidence assessment:** the DATES (Darby 1709, Cort 1784, Bessemer 1856, Siemens-Martin 1865/dominance
~1890-1900, Hargreaves 1764, Arkwright 1769/1771, Crompton 1779, Cartwright 1785/dominance ~1830, Watt 1776, the four
Self-Strengthening enterprises' founding years) are all HIGH confidence, cross-corroborated across multiple
independently-fetched pages. The ANALYTICAL FRAMEWORKS (Wrigley's energy argument, Pomeranz's coal-geography +
ghost-acreage argument, Elvin's high-level-equilibrium-trap) are HIGH-to-MEDIUM confidence as commonly-presented
summaries, but this session could not verify them against the named monographs' own text — a follow-up session with
JSTOR/library access would strengthen §2 and §4 specifically. The one genuinely rare find — a sourced input:output
ratio (Neilson's 8.06→5.16 long tons coal per ton iron) — is flagged as the single strongest quantitative anchor
recovered, and everything else in the "rough ratios" ask of the task is a stated GAP rather than an invented number.
