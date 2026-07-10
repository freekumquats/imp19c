# High Qing (1763) Mechanic Adaptation Research Digest

**Anchor Date**: 1763.2.16 — Mid-reign Qianlong Emperor (乾隆帝, r. 1735-1796)  
**Context**: Post-Xinjiang conquest (1755-59), territorial peak, mid-way through Ten Great Campaigns (十全武功), decades before White Lotus Rebellion (1794-1804) and Opium War (1839)

## 1. DYNASTIC DECLINE vs ZENITH

### Peak Indicators (1763 as Zenith)

1763 falls squarely within the **High Qing / 盛清 / Kang-Qian Prosperity** (康乾盛世, ~1683-1799). William T. Rowe's *China's Last Empire: The Great Qing* (2009) characterizes the Qianlong reign's mid-decades as the dynasty's territorial, demographic, and fiscal apogee. Mark Elliott's *Emperor Qianlong: Son of Heaven, Man of the World* (2009) notes the decade 1755-65 saw the completion of the Zunghar/Xinjiang campaigns (conquest complete by 1759, with the Ili governorship established 1762) at manageable fiscal cost — a net treasury surplus still growing.

**Treasury**: Qianlong-era central reserves peaked at ~70-73 million taels by the mid-1780s (戴逸《乾隆帝及其时代》, 1992; 賴福順《乾隆重要戰爭之軍需研究》, 1984). The 1763 position, mid-campaign sequence, is estimated at 60-65M taels (Rowe 2009:127) — already double Yongzheng's handover. Military campaigns (Burma 1765-69, first Jinchuan 1747-49 and second 1771-76, Vietnam 1788-89) were fiscally manageable until the 1790s Nepal/Gurkha war, which combined with Yellow River flood relief to drain reserves. The 1763 treasury is robustly positive.

**Administrative Vigor**: The Grand Council (軍機處, est. 1730s under Yongzheng, formalized under Qianlong) operated efficiently; R. Kent Guy's *Qing Governors and Their Provinces* (1987) documents governorship rotation and reporting discipline at peak effectiveness in the 1750s-70s. The palace memorial system (奏摺) and routine memorials (題本) functioned without the late-dynasty backlog. Gaitu guiliu (改土歸流, substituting appointed officials for hereditary chieftains) continued actively in the southwest — this is era-appropriate for 1763.

**Population and Agriculture**: Population estimates for 1763 are ~200-220 million (高王凌 *Eighteenth Century China*, 1995; Perkins 1969). The agrarian boom (new crops: maize, sweet potato, peanuts enabling marginal-land settlement) continued unchecked; soil exhaustion and the Malthusian ceiling lay decades ahead. The 1780s-90s White Lotus millenarian unrest (1794-1804) — a symptom of landlessness and resource strain — had not yet materialized.

### Early Seeds of Decline (Present but Subordinate in 1763)

**Military Fiscal Strain**: 賴福順's monograph on Qianlong military finance notes that campaign supply (especially the 1755-59 Xinjiang logistics over 2000+ km) introduced systemic corruption in procurement — meltage fees (火耗), markup chains, phantom troops drawing pay. However, this corruption was still controllable in the 1760s; the catastrophic hollowing-out of the Eight Banners and Green Standard came later (post-1800 White Lotus demobilization revealed mass desertion and phantom musters).

**Sub-Bureaucratic Informal Fees (陋規)**: The informal fee / "customary fees" system that supplemented official salaries existed in 1763 but had not yet metastasized. Yongzheng's 養廉銀 (integrity-nourishing stipend) reform in the 1720s-30s attempted to formalize/limit it. By the late-Qianlong era (post-1780), 陋規 ballooned under Heshen's regime, but in 1763 it remained a managed friction, not systemic collapse.

**Heshen 和珅 (1750-1799)**: The arch-symbol of late-Qianlong corruption entered palace service only ~1772 (as a bodyguard) and rose to Grand Councillor by ~1776. His two-decade stranglehold on appointments, monopolies, and revenue skimming (estimated personal wealth 800M-1B taels at confiscation in 1799, per 戴逸 and Elliott) defines the **post-1775 inflection** toward decline. In 1763, Heshen was 13 years old. The court favorite mechanism (寵臣) that enabled him did not yet exist.

**Social Anxiety Precursors**: Philip Kuhn's *Soulstealers: The Chinese Sorcery Scare of 1768* (1990) documents a mass panic over queue-cutting sorcery (叫魂) that gripped provinces in 1768 — five years after 1763. Kuhn reads this as an early indicator of social strain (vagrancy, suspicion of itinerant monks/beggars, local-official nervousness about central discipline) even at the height of prosperity. The 1763 snapshot is just before this — anxiety latent but not yet manifest.

**Population Pressure Lag**: The crisis of the 1790s-1810s (landlessness driving the White Lotus Rebellion, 1794-1804, and later the Eight Trigrams 1813) stemmed from population outpacing arable expansion. In 1763, the frontier (Sichuan, Guizhou, Hunan/Hubei highlands, Taiwan) still absorbed migration. The Malthusian ceiling is ~20-30 years away.

### Historiographic Framing

The standard periodization (Rowe, Elliott, Crossley, Perdue) treats **1760s-1770s as the hinge**: zenith in territorial/fiscal terms, but the institutional/social seeds of the 19th-century crisis already planted. 戴逸 and 郭成康 (Chinese Qianlong-era historiography) emphasize the **turning point ~1775-1780**: Heshen's rise + end of the major campaigns + population crossing 300M. The 1763 date lands decisively on the zenith side of that hinge.

**ADAPTATION RECOMMENDATION**:  
The imported `se_QING_DECLINE.txt` corruption/harmony erosion pulse is **anachronistic for 1763 and should be re-phased**. Proposed tuning:

1. **Start State (1763.2.16)**: `qing_corruption_level` = 10-15 (low; baseline administrative friction, not systemic). `qing_dynastic_harmony` = 80-85 (high; no succession crisis, military victorious, treasury flush, no mass unrest). Apply a **positive "High Qing Prosperity" modifier** (+10% tax efficiency, +5% manpower recovery, or equivalent) active 1763-1775.

2. **First Inflection (~1775-1780)**: Date-gated event: "Rise of Heshen" or "Court Favorite Corruption" fires if Qianlong still reigns and no player intervention. `qing_corruption_level` begins climbing (starts the current decline pulse, or a gentler version). Prosperity modifier removed or halved. Harmony begins slow erosion.

3. **Second Inflection (~1794-1804)**: White Lotus Rebellion or equivalent mass unrest if population > threshold + corruption > 40. Accelerated decline phase (the current 1815-tuned pulse). Harmony drops sharply; regional governorships may defect or go rogue.

4. **Crisis Phase (post-1815)**: Opium, indemnities, treaty ports, Taiping — the current pulse is appropriate here.

**Date Anchors**: 1763 start = zenith phase; 1775 = Heshen inflection (corruption ramp); 1794 = White Lotus (unrest/collapse risk); 1815+ = foreign-pressure overlay. The 1763 bookmark should **not** run the decline pulse immediately; it should gate it to historical triggers or player failure to reform.

## 2. STARTING MILITARY (Armies + Navies) at 1763

### Land Forces: Eight Banners vs Green Standard

The Qing military in 1763 comprised two parallel systems with sharply different roles and effectiveness:

**Eight Banners (八旗)**: The hereditary Manchu-Mongol-Han martial caste, organized into 24 banners (8 Manchu, 8 Mongol, 8 Han). Nominal roll ~200,000-250,000 in 1760s (Mark Elliott *The Manchu Way*, 2001; Rowe 2009:112), divided between:
- **Capital Banners** (京旗, ~60-80k): garrisoned in Beijing, the Zhili plain, and the Three Eastern Provinces (Manchuria). Elite units included the Imperial Guard (侍衛, ~3000) and the Firearms Battalion (火器營).
- **Provincial Banners** (駐防八旗, ~120-170k): garrisoned at strategic nodes (Xi'an, Hangzhou, Jingzhou, Guangzhou, etc., ~40+ garrison cities). By the 1760s, many garrison bannermen had settled into hereditary sinecures with deteriorating training.

**Effectiveness in 1763**: The Xinjiang campaigns (1755-59) and the first Jinchuan War (1747-49) were *Eight Banner* operations, demonstrating that the institution retained **offensive capability** when mobilized under capable commanders (e.g., Zhaohui 兆惠, Fude 富德, Agui 阿桂). Elliott and Perdue (*China Marches West*, 2005) note the Banners' cavalry mobility and siege engineering were decisive in the Zunghar destruction. The rot — banner hereditary pay for non-service, opium addiction, urban poverty — accelerated post-1800 but was manageable in 1763. **The 1763 Banners are significantly more capable than the 1815 hollowed-out version.**

**Green Standard Army (綠營)**: Provincial infantry/garrison troops recruited from the Han population, officered by a mix of Han and banner commanders. Nominal roll ~600,000-660,000 in the mid-Qing (Rowe 2009:113; Guy 1987). Organized by province under provincial military commanders (提督, 總兵). Primary roles: local security, anti-banditry, waterway/granary escort, and *occasionally* as auxiliary campaign forces (the Banners led offensives; Green Standard provided logistics and garrison backfill).

**Effectiveness in 1763**: Adequate for internal policing but never elite. The Green Standard's weakness — local recruitment fostering corruption, low pay, part-time farming — existed throughout the dynasty. In 1763, however, the *absence* of major internal rebellion (the century between the Three Feudatories 1673-81 and the White Lotus 1794-1804 saw relative peace) meant the Green Standard's garrison function sufficed. Post-1800, mass desertion and phantom musters rendered it near-useless; the 1815 Green Standard is visibly decrepit, while 1763's is merely mediocre.

**Order of Magnitude Comparison**:
- **1763**: ~200-250k Eight Banners (functional offensive force) + ~600-660k Green Standard (adequate garrison force) = ~850k nominal troops, perhaps ~600-700k effectives.
- **1815**: ~200k Eight Banners (mostly hollow, opium-ridden, incapable of campaigning) + ~600k Green Standard (deserted or phantom) = ~800k nominal, perhaps ~300-400k effectives, and those of poor quality. The Opium War (1839-42) and Taiping (1850-64) revealed the Qing had to raise **new** irregular forces (tuanlian 團練, yongying 勇營) because the standing army was unusable.

### Naval Forces: Brown-Water Junks Only

The Qing "navy" in both 1763 and 1815 was coastal and riverine — **no ocean-going battle fleet**. The dynasty's strategic focus was landward (Mongolia, Tibet, Xinjiang), and maritime policy was defensive (anti-piracy, customs enforcement).

**1763 Composition**:
- **Fujian Navy (福建水師)**: ~100-150 war junks, based at Xiamen (Amoy) and Fuzhou. Primary mission: Taiwan Strait patrol (Taiwan formally annexed 1683) and anti-smuggling. The *garrisons* included Green Standard marine units (~10-15k troops).
- **Guangdong Navy (廣東水師)**: ~80-120 junks, based at Canton (Guangzhou) and coastal forts. Mission: Pearl River delta control, anti-piracy in the South China Sea approaches.
- **Zhejiang, Jiangsu, Shandong provincial squadrons**: smaller (20-50 junks each), focused on the Yangzi delta, Grand Canal junction, and the Yellow Sea coast.

Junks were sail-and-oar, armed with small cannon (typically 6-12 guns per vessel, bronze or iron, muzzle-loading). Officers were Green Standard, with some banner supervision. **No centralized Admiralty**; each provincial fleet reported to its governor-general or admiral (水師提督).

**1763 vs 1815 Naval Context**:
- **1763**: The southern coast was relatively quiet. The Zheng pirate-dynasty (Koxinga's heirs) had been defeated in 1683; the next major piracy surge did not begin until the 1790s-1800s (**Cai Qian 蔡牽, Zheng Yi Sao 鄭一嫂** and the great pirate confederations, 1795-1810, which the Qing could not suppress without Portuguese/British help). In 1763, the navy's mission was *routine* — no existential maritime threat.
- **1815**: Post-Napoleonic Wars, British/French/American warships appeared regularly in Asian waters. The Qing junks were obsolete against Western ships-of-the-line and steamers (the 1839-42 Opium War demonstrated this crushingly). The 1815 Qing navy is the **same institutional type** as 1763 — no oceanic modernization — but facing a different threat environment.

**Technology and Doctrine**: Both 1763 and 1815 Qing navies were **tactically static**. No adoption of European ship-of-the-line design, no naval gunnery schools, no ocean navigation capability. The Self-Strengthening Movement's modern fleets (Fuzhou Navy Yard 1866, Beiyang Fleet 1880s) came **after** 1815 and represent a discontinuous leap, not evolution. For a 1763 start, the imported 1815 naval setup (coastal junks, anti-piracy, no ocean power) is *accurate* and requires no scaling.

**ADAPTATION RECOMMENDATION**:  
1. **Land Forces (Eight Banners + Green Standard)**: The 1763 start should seed **higher-quality and/or numerically larger land forces** than 1815. Specific guidance:
   - **Eight Banners**: Increase starting manpower by ~25-40% over 1815 levels (if 1815 seeds ~150k, make 1763 ~200-220k). Apply a **quality modifier** (+10-15% discipline, +5% morale, or equivalent) representing pre-decline effectiveness. This modifier should **degrade over time** if corruption rises (linked to Section 1's Heshen inflection).
   - **Green Standard**: Slightly larger (if 1815 seeds ~500k, make 1763 ~600k) and **less degraded** (remove or reduce any 1815-specific "decrepit garrison" malus). Still inferior to Banners, but functional.
   - **Composition by Region**: Xinjiang/Ili garrisons (established 1762-64) should reflect the post-conquest occupation force (Manchu/Mongol Banners, perhaps 10-20k). Core China garrisons are as-historical (Beijing, Xi'an, Hangzhou, Jingzhou, Guangzhou, etc.).

2. **Naval Forces**: Maintain the 1815 setup (coastal/riverine junks, provincial squadrons, no ocean capability). The 1763 navy is the same **type** as 1815; the difference is threat environment, not Qing capacity. No mechanical change needed — perhaps flavor text emphasizing the "pre-piracy-crisis calm" vs the 1815 "post-Zheng Yi Sao exhaustion."

3. **Military Decay Linked to Decline Pulse**: If the Section 1 corruption/decline mechanics fire (post-1775 Heshen, post-1794 White Lotus), military quality should degrade: Banner discipline penalty, Green Standard desertion events, manpower drain. By the 1815-equivalent date, the 1763-start military should *converge* toward the 1815-start baseline if the player does nothing to reform.

## 3. EMPEROR EMERITUS 太上皇 OFFICE

### Historical Institution and Qianlong's Abdication (1796)

The **太上皇 (Taishang Huang, "Supreme Emperor Emeritus")** title is rare in Chinese history but was realized by the Qianlong Emperor in **1796**. The institution itself is ancient — most famously, **宋高宗 (Song Gaozong, r. 1127-62)** abdicated to his adopted son Xiaozong in 1162 and lived as Taishang Huang until 1187, retaining advisory (but not executive) power. Earlier precedents include Tang Gaozong's father Tang Taizong being posthumously styled 太上皇 by his son, and sporadic abdications under duress (usurpations, coups). Qianlong's 1796 abdication was **voluntary and planned**, making it distinctive.

### Qianlong's Abdication: Mechanics and Motivation

**Date**: Qianlong formally abdicated on **1796.2.9** (Jiaqing 1.1.1, the first day of the new year), passing the throne to his 15th son **Yongyan 永琰 (Jiaqing Emperor, r. 1796-1820)**. Qianlong was 85 years old (born 1711.9.25).

**Stated Rationale**: Qianlong **did not want to out-reign his grandfather Kangxi** (r. 1661-1722, 61 years). Qianlong's reign length at abdication: 1735-1796 = **60 years**, deliberately one year short of Kangxi. This was publicly framed as filial piety (孝) and deference to the dynastic founder-patriarch. Mark Elliott (*Emperor Qianlong*, 2009:305-7) notes this justification was both genuine (Confucian propriety) and politically convenient — Qianlong retained power without the throne's formal burdens.

**Reality: Retained Power (1796-1799)**: Qianlong as Taishang Huang continued to:
- **Reside in the Forbidden City** (the main palaces; Jiaqing occupied secondary quarters).
- **Review major memorials** and **issue edicts** (co-signed or implicitly required Qianlong's approval).
- **Control the Grand Council** (軍機處) — Heshen remained Grand Councillor, loyal to Qianlong not Jiaqing.
- **Command military appointments** (e.g., suppression of the Miao Rebellion 1795-97 and White Lotus Rebellion 1796-99 continued under his oversight).

Jiaqing was emperor **in name only** until Qianlong's death on **1799.2.7**. Within days, Jiaqing arrested Heshen, confiscated his wealth, and forced his suicide (1799.2.22) — a clear signal that Jiaqing's reign began *after* his father's death, not at the 1796 abdication. Pamela Kyle Crossley, Elliott, and 戴逸 all characterize the 1796-99 period as **Qianlong's de facto regency** under the Taishang Huang title.

### Institutional Precedent and Constraints

The Taishang Huang role had no codified powers — it was **personal charisma + institutional inertia**. In Qianlong's case:
- **No formal office removal**: He remained head of the Imperial Clan Court (宗人府), the Lifan Yuan (理藩院, Court of Colonial Affairs), and effectively the Grand Council.
- **Succession already secured**: Jiaqing was chosen in 1795 (announced early to prepare officials); no rival claimants, no succession crisis.
- **Financial control**: The privy purse and campaign budgets remained Qianlong's to allocate.

Contrast with Song Gaozong's Taishang Huang: Gaozong ceded *executive* power to Xiaozong (who made independent appointments), retaining only advisory/veto authority. Qianlong ceded **nothing** but the throne title.

### Why Not Earlier or More Common?

Most Qing emperors died on the throne: Kangxi (1722, age 68), Yongzheng (1735, age 56), Jiaqing (1820, age 60), Daoguang (1850, age 68), Xianfeng (1861, age 30), etc. The **Taishang Huang was exceptional** because:
1. **Longevity + Succession Certainty**: Qianlong lived to 87 (rare); his heir was adult and groomed. Most emperors died before designating + securing succession, making abdication risky.
2. **Will to Retain Power**: Qianlong wanted the **legitimacy** of deferring to Kangxi's record *without* surrendering control. This requires unusual ego + political strength.
3. **No Precedent for Routine Abdication**: Chinese political culture (Confucian + Legalist) centered on the emperor dying in office. Abdication implied either usurpation (forced) or decrepitude (voluntary but shameful). Qianlong reframed it as **super-filial piety**.

### Game-Mechanical Implications

The mod's current **Napoleon alt-history Taishang Huang** (#65, se_QING_NAPOLEON.txt) exists but is ahistorical for the 1815 start (Napoleon never reached China). For **1763**, the Taishang Huang office should be:

1. **Latent for Qianlong**: Qianlong (born 1711, age 51 in 1763) won't consider abdication until **~1795-96** (age 84-85), and only if:
   - He is still alive and ruling (not assassinated, deposed, or dead of natural causes).
   - He has reigned **60+ years** (i.e., year ≥ 1795).
   - An adult male heir exists and is designated (historically Yongyan/Jiaqing, born 1760, age 35 in 1795).

2. **Mechanic**: A **date-gated event** (~1795-96) offering Qianlong the choice:
   - **Abdicate to Taishang Huang** (keeps all or most power modifiers; new emperor is puppet; Grand Council loyalty stays with Qianlong; player retains control of "Qianlong" as Taishang Huang, not Jiaqing). Flavor: "To honor the Kangxi Emperor's record of 61 years..."
   - **Remain on throne** (forgo the filial-piety prestige but avoid the institutional split). Flavor: "The empire requires the Mandate unbroken."

3. **Death Event (1799)**: If Qianlong abdicates, a follow-up event ~1799 (age 87-88 or health-triggered) fires: Qianlong dies, Jiaqing assumes real power, **Heshen purge event** (if Heshen still Grand Councillor → arrest/suicide, treasury bonus as wealth confiscated), and the Taishang Huang office becomes vacant. The office should then be **available** to future emperors who meet similar conditions (60-year reign, heir ready, high legitimacy).

4. **Alt-History Extension**: The existing Napoleon path can remain as a *separate* route: if Napoleon arrives/joins court (alt-history), he could be granted Taishang Huang as a sinecure (the current #65 implementation). But **historically, the office belongs to Qianlong first**.

**ADAPTATION RECOMMENDATION**:  
1. **Enable the Taishang Huang office for Qianlong** as a historical path, not only the Napoleon alt-history. Implement a **date-gated event (~1795-96)** offering abdication if Qianlong is alive, has reigned 60 years, and has a viable heir. If accepted, Qianlong becomes Taishang Huang (retains power modifiers, Grand Council control, military command; new emperor is figurehead). Player continues as "Qianlong/Taishang Huang" in the GUI (or a modifier that makes Jiaqing transparent).

2. **Death and Succession (~1799)**: Follow-up event when Qianlong dies: transfer power to Jiaqing, trigger Heshen purge if applicable, confiscate Heshen's wealth (treasury bonus ~50-100M taels if corruption was unchecked). Jiaqing's independent reign begins.

3. **Reusability**: After Qianlong, the Taishang Huang office could be available to **any Qing emperor** meeting conditions (60-year reign is rare, so this would be exceptional). If the Napoleon path fires, it slots into the same office structure.

4. **For 1815 Start**: The Taishang Huang is historical memory (Qianlong used it 1796-99, now dead). Jiaqing or Daoguang could *theoretically* use it if they reign 60 years (unlikely), or it remains a Napoleon-only alt-history. No change needed for 1815 unless the player runs to 1860+.

5. **For 1763 Start**: Fully implement the above. The office is **32 years away** at game start — a long-term milestone. If the player keeps Qianlong alive and stable to 1795, the Taishang Huang abdication should fire as a **reward/capstone event** ("Your reign has matched the great Kangxi..."), not a crisis.

## 4. GREAT POWER INTEREST (Britain/Russia/France) toward China in 1763

The mod's Great Power tension counters (`qing_gp_tension_britain`, `qing_gp_tension_russia`, `qing_gp_tension_france`) model escalating pressure from European powers. For a **1763 start**, all three powers have **lower interest and less capacity** to project force into East Asia than in 1815. The Industrial Revolution, steam navies, and the opium-fueled trade imbalance that drove the 1839-42 Opium War are decades away.

### Britain: Canton Trade, Not Confrontation (1763)

**1763 Context**: Britain's East India Company (EIC) presence in China was **commercial and peripheral**. The EIC traded at **Canton (Guangzhou)** under the restrictive **Canton System** (formally established 1757 by Qianlong edict, consolidating all European trade to Canton and banning it elsewhere). The EIC's China trade in the 1760s centered on:
- **Tea exports** (to Britain, increasingly important as tea became a mass commodity).
- **Silver imports** (to pay for tea; the EIC had chronic trade deficit with China until opium reversed it post-1780s).
- **Minimal territorial ambition**: No treaty ports, no extraterritoriality, no military confrontation. The EIC's priority was **India** (Battle of Plassey 1757, conquest of Bengal, Mysore Wars 1760s-90s). China was a trading counter, not a target.

**Key Contrast with 1815+**:
- **1763**: The EIC operated at Canton as a **licensed merchant** via the Cohong (公行, guild monopoly). No British warships in Chinese waters; no British consuls (the EIC supercargoes were merchants, not diplomats). The **Macartney Embassy (1793)**, which sought diplomatic equality and trade expansion, had **not yet happened** — and it **failed**, rejected by Qianlong as "barbarian tribute" (the famous "we have no use for your manufactures" edict).
- **1815+**: Post-Macartney, post-Amherst (second failed embassy 1816), and crucially post-**opium**. By 1815, the EIC's private "country traders" had massively scaled opium smuggling from India into China (reversing the silver flow). The Daoguang Emperor's 1839 opium crackdown (Lin Zexu 林則徐 at Canton) triggered the **First Opium War (1839-42)**, resulting in Hong Kong cession, treaty ports, indemnities, and extraterritoriality. This is the 1815+ confrontational posture.

**1763 British Tension Level**: Should start **low** (10-20 on a 0-100 scale, if the 1815 start is ~40-50). British interest in China is latent, tied to the tea trade but not militarized. **Inflection points**:
- **1793: Macartney Embassy** (diplomatic rebuff → slow tension rise).
- **1810s-1830s: Opium trade escalation** (smuggling + Qing anti-opium edicts → sharp tension rise).
- **1839-42: First Opium War** (war onset → maximum tension, reset post-war to "treaty-port coexistence" baseline).

### Russia: Post-Kyakhta Accommodation (1763)

**1763 Context**: Russia and Qing China had **formalized and stable** relations under the **Treaty of Kyakhta (1727)**, which:
- **Demarcated the Sino-Russian border** (Outer Mongolia, the Selenga-Argun river line, the Sayan-Altai frontier).
- **Established trade protocols**: Kyakhta (恰克圖) as the sole Russo-Chinese trade town (Russian furs, leather, and European goods for Chinese tea, silk, rhubarb). The Kyakhta trade was **regulated and profitable** for both sides (C.R. Bawden *The Modern History of Mongolia*, 1968; Joseph Fletcher, "Sino-Russian Relations 1800-62").
- **Russian Ecclesiastical Mission in Beijing** (東正教北京傳道團): Allowed under the 1727 treaty as a carve-out (ostensibly to serve baptized Albazinians captured in 1680s border clashes, but functionally a standing Russian presence).

**Territorial Status in 1763**: Qing had **just destroyed the Zunghar Khanate (1755-59)**, the steppe power that had been Russia's rival and buffer. Perdue (*China Marches West*, 2005) notes the Qing annexation of Xinjiang brought the Qing border **up to the Russian frontier** (the Sayan-Altai, the Irtysh basin). Russia's reaction was **cautious accommodation**, not confrontation — the Qing military had just demonstrated overwhelming superiority over a steppe confederation, and Russian Siberia was thinly held. The 1768 Russo-Turkish War and the Polish partitions (1772-95) consumed Russian attention westward.

**Key Contrast with 1815+**:
- **1763**: Russia and Qing are **non-threatening trade partners**. No territorial disputes (the border was settled 1689 Nerchinsk + 1727 Kyakhta). No Russian expansion into Xinjiang or Mongolia (both now Qing). Russian focus: Europe (Ottoman Wars, Poland, Napoleon).
- **1815+**: Russia begins probing Central Asia (the "Great Game" vs Britain in Afghanistan/Persia) and eyes the Amur/Ussuri borderlands (northern Manchuria), which the Qing had left nominally under their control but under-populated. The **Treaty of Aigun (1858)** and **Treaty of Beijing (1860)** ceded the north bank of the Amur and the Ussuri basin to Russia — this is **post-1850s**, after the Opium War weakened Qing bargaining power. In 1815, this is incipient; in 1763, it's not even imaginable.

**1763 Russian Tension Level**: Should start **very low** (5-10 on a 0-100 scale). Russia is **status-quo satisfied**. The Kyakhta trade is profitable; the border is settled; Russian expansion vectors point west and south (Poland, Crimea, Caucasus), not east. **Inflection points**:
- **1850s-1860s: Amur Question** (Russian exploration + settlement of the Amur basin, coinciding with Qing crisis of Opium War/Taiping; tension rises).
- **1858-60: Unequal Treaties** (Aigun, Beijing; Russia seizes Outer Manchuria; tension spike then reset to "new border" baseline).

### France: Minimal China Presence (1763)

**1763 Context**: France had **negligible direct interest** in China in 1763, as the French state was:
- **Recovering from the Seven Years' War (1756-63)**, which ended with French losses in India (Pondicherry capitulated 1761, returned 1763 but as a hollow shell) and North America (Canada ceded to Britain). France's colonial focus post-1763 was **survival and West Indies retention**, not Asian expansion.
- **No French EIC equivalent** after 1769: The French *Compagnie des Indes* was dissolved 1769 (it had traded at Canton sporadically but was never competitive with the British EIC or Dutch VOC). French China trade became **private/port-based** (minimal).

**French Missionary Presence**: The **Jesuits** at the Qing court were disproportionately French (Verbiest, Gerbillon, Bouvet, Regis, Castiglione, Benoist, Attiret, etc., over the Kangxi-Qianlong reigns). The French **Académie des Sciences** sponsored Jesuit scientific missions to China (1685+). However, this was **cultural-scientific, not political**. The Jesuits served Qing emperors and reported to Rome + Paris; they did not advance French territorial claims. After the **papal suppression of the Jesuits (1773)**, the French mission was taken over by **Lazarists/Vincentians** (1780s-1800s, e.g., Raux, Ghislain), who continued scientific/cartographic service but at reduced scale.

**Key Contrast with 1815+**:
- **1763**: France has **no state-level China policy**. The missionaries are a cultural curiosity; trade is negligible. French attention: post-Seven Years' War recovery, then the French Revolution (1789-99) and Napoleonic Wars (1799-1815).
- **1815+**: Post-Napoleon, France gradually rebuilds colonial ambitions. French Catholic missions (now Lazarist/MEP) expand in southern China/Indochina. The **Second Opium War (1856-60)** saw France ally with Britain (pretext: murder of French missionary Chapdelaine 1856); the **Treaty of Tianjin (1858)** gave France (and other powers) treaty ports, indemnities, and missionary toleration. French **Indochina colonization** (Vietnam, Cambodia, Laos, 1858-1887) put France on China's southern border. This is a **post-1850s** development.

**1763 French Tension Level**: Should start **very low** (5-10). France is **distracted and weak** in Asia. The Jesuit presence at court is neutral/friendly (they serve the Qing, not French interests). **Inflection points**:
- **1840s-1850s: Missionary incidents** (e.g., Chapdelaine 1856 → French co-belligerence in Second Opium War).
- **1858-60: Second Opium War treaties** (France joins treaty-port system → tension baseline rises to "colonial power" level).
- **1880s: Sino-French War (1884-85)** over Vietnam (French Indochina vs Qing tributary claims; tension spike, then reset to "spheres of influence" status quo).

### Other Powers (Not Modeled but Notable for 1763)

- **Portugal**: The longest-standing European presence (Macau leased 1557, formalized 1887). In 1763, Portugal was a **declining power** (post-1755 Lisbon earthquake, Brazil-dependent economy). Macau was a trading enclave tolerated by the Qing; Portugal sent occasional embassies (Pacheco 1753, Metelo 1727) but had no military leverage. Should be treated as **neutral/vassal** in the mod (if modeled at all).
- **Netherlands**: The Dutch VOC traded at Canton under the Canton System. By 1763, Dutch power in Asia was **waning** (British/French rivalry marginalized them). The **Titsingh Embassy (1794-95)** was post-1763 and, like Macartney, failed. Low tension.
- **United States**: Did **not exist** until 1776 independence (recognized 1783). The first US-China contact was the **Empress of China** ship (1784 Canton voyage). The **Cushing Embassy (1844)** and **Treaty of Wanghia (1844)** came post-Opium War. Irrelevant for 1763; minor for 1815.

**ADAPTATION RECOMMENDATION**:  
1. **Starting Tension Levels (1763)**: Dramatically lower than 1815. Proposed values (0-100 scale):
   - **Britain**: 10-15 (Canton trade stable, no opium, no Macartney yet).
   - **Russia**: 5-10 (Kyakhta trade, border settled, no Amur ambitions).
   - **France**: 5-10 (missionary presence only, no state policy, post-war weakness).

2. **Tension Ramp Schedule (Date-Gated)**:
   - **1793: Macartney Embassy** → Britain +5-10 (diplomatic rebuff).
   - **1810s-1830s: Opium trade escalation** → Britain +1-2 per year (smuggling + anti-opium edicts).
   - **1839-42: First Opium War** → Britain spike to 70-80 (war), then reset to 40-50 (treaty-port baseline).
   - **1850s: Amur Question** → Russia +10-15 (border probing).
   - **1858-60: Unequal Treaties** → Russia +20, France +20, Britain +10 (Second Opium War + territorial seizures).
   - **1884-85: Sino-French War** → France +15-20 (Indochina conflict).

3. **Tension Decay**: In the **1763-1793 window**, tensions should **not rise organically** unless triggered by Qing actions (e.g., closing Canton, anti-Christian pogroms, border clashes). The default state for 1763-1793 is **stable coexistence**. The historical escalation was driven by **European industrial/military growth + opium**, not by Qing provocation.

4. **Embassy Events**: The existing **Western embassy crisis events** (#60, se_QING_EMBASSIES.txt: Macartney, Amherst, etc.) should be **date-gated**. For 1763:
   - **Macartney (1793)** is the first possible British embassy → fires only if year ≥ 1793 and Britain tension > threshold.
   - **Titsingh (1794-95)** (Dutch) is similarly gated.
   - **Amherst (1816)** and **Cushing (1844)** are later.
   - If the mod includes earlier embassies (Russian Kyakhta renegotiation, Portuguese tribute missions), those are 1760s-appropriate but should be **low-stakes** (trade protocol, not confrontation).

5. **Campaign Linkage**: The Qing's Xinjiang/Burma/Nepal campaigns (1755-59, 1765-69, 1788-89, 1790-92) did **not** provoke European interest (they were seen as "interior barbarian wars"). Only the **Opium War (1839-42)** and later crises involved European militaries. The GP tension counters should **not** rise due to Qing campaigning in Central Asia/Southeast Asia unless a European power has a border/proxy involved (e.g., British India post-1815 cares about Burma; Russia post-1850s cares about Xinjiang).

## 5. EUROPEANS AT COURT + EMBASSIES

The 1763 picture of Europeans at the Qing court and inbound embassies differs sharply from the post-Opium-War (1815+) reality. In 1763, the **Jesuit mission** dominated court scientific/artistic service, the **Canton System** (est. 1757) had just formalized trade restrictions, and **no modern diplomatic embassies** had yet been sent (Macartney 1793 was 30 years away). The mod's embassy and missionary mechanics must be **re-gated to historical chronology**.

---

## (A) EMBASSIES: Historical Sequence and Gating

### Pre-1763 Embassies and Missions

The concept of a "Western embassy" to China was contested throughout the 17th-18th centuries, as the Qing and European powers held irreconcilable frameworks: the Qing **tributary system** (朝貢體系, which treated all foreign contact as barbarian tribute) vs European **Westphalian sovereignty** (which assumed diplomatic equality). Early contacts:

**Russian Embassies (17th-18th century)**:
- **Nikolai Spafary (1675-76)**: Russian embassy to Kangxi, failed to secure trade treaty but opened negotiations.
- **Treaty of Nerchinsk (1689)**: Border settlement (first Sino-Western treaty on equal terms, negotiated in Latin via Jesuit interpreters Gerbillon and Pereira). Established Argun River boundary and expelled Russia from the Amur basin.
- **Izmailov Embassy (1720-21)**: Failed to revise Nerchinsk; no trade expansion.
- **Treaty of Kyakhta (1727)**: Formal border + trade agreement (see Section 4). Established Kyakhta as sole trade town and formalized the Russian Orthodox Ecclesiastical Mission in Beijing. This was the **successful** embassy model — Russia accepted tributary ritual (the ambassador kowtowed) in exchange for concrete gains.

**Papal and Catholic Missions (Rites Controversy Era)**:
- **Tournon Legation (1705-07)**: Papal legate Charles-Thomas Maillard de Tournon sent by Pope Clement XI to resolve the **Chinese Rites Controversy** (could Chinese Christians venerate Confucius and ancestors?). Tournon demanded Jesuits cease tolerating rites; Kangxi expelled him as meddling in internal affairs. This was a **diplomatic disaster** (Kangxi banned Christianity 1706, reversed 1708 with caveats).
- **Mezzabarba Legation (1720-21)**: Papal legate Carlo Ambrogio Mezzabarba, second attempt; Kangxi received him but ignored the rulings. The Rites Controversy persisted until the **papal suppression of the Jesuits (1773)**, after which the issue became moot (Jesuits dissolved, Catholic missions in China fragmented).

**Portuguese Embassies (Canton Era)**:
- **Metelo de Sousa e Meneses (1727)**: Portuguese envoy from Macau, seeking trade confirmation. Received as tribute mission; minor success (Macau trade continued).
- **Francisco de Assis Pacheco (1753)**: Another tribute mission from Macau. Routine.

### The 1757 Canton System and its Implications

In **1757**, Qianlong issued the edict **restricting all Western maritime trade to Canton** (Guangzhou) and banning it at other ports (Ningbo, Shanghai, etc., which had previously hosted limited foreign trade). The **Canton System** (also called the Cohong system, 公行) placed all foreign merchants under the supervision of the **Cohong guild** (licensed Chinese monopoly merchants). This was the **restrictive baseline** for 1763 and remained in force until the **Treaty of Nanking (1842)** ended it.

The Canton System framework meant:
- **No foreign ambassadors resident in Beijing**. All Western contact was commercial, mediated by Cohong merchants in Canton.
- **Embassies treated as tributary missions**. Any delegation to Beijing was required to perform the **kowtow** (三跪九叩, three kneelings nine prostrations) to the emperor, which European states found humiliating.
- **Trade as imperial favor, not right**. The Qing framed trade as "bestowing benevolence on outer barbarians," not a mutual treaty relationship.

### Post-1763 Embassies (Date-Gate These)

**Macartney Embassy (1792-93)**:  
- **Date**: Arrived Canton late 1792, reached Beijing summer 1793, met Qianlong at his Rehe (Chengde) summer palace 1793.9.14.
- **British Goal**: Permanent ambassador in Beijing, trade expansion beyond Canton (open northern ports), tariff reform, territory for a British warehouse/base.
- **Outcome**: Total failure. Macartney performed a "one-knee bend" compromise (not the kowtow), which satisfied neither side. Qianlong's **1793.9.23 edict** to King George III famously rejected all requests: "We possess all things. I set no value on objects strange or ingenious, and have no use for your country's manufactures." (See Peyrefitte *The Immobile Empire*, 1992; Hevia *Cherishing Men from Afar*, 1995.)
- **Aftermath**: British humiliation + resentment, contributing to the hardline opium-trade policy and eventual war.

**Titsingh Embassy (1794-95)** (Dutch):  
- **Date**: 1794-95, Amsterdam-sponsored mission (VOC was bankrupt; this was a state effort).
- **Outcome**: Received at Beijing, kowtowed, granted nothing beyond Canton trade continuation. Less famous than Macartney but equally ineffective.

**Amherst Embassy (1816)** (British):  
- **Date**: 1816, under the Jiaqing Emperor (Qianlong died 1799).
- **Outcome**: Worse than Macartney. Amherst **refused the kowtow**, was denied imperial audience, expelled without meeting the emperor. Diplomatic break.

**Cushing Embassy (1844)** (American):  
- **Date**: 1844, **after** the First Opium War (1839-42) and the Treaty of Nanking. Caleb Cushing negotiated the **Treaty of Wanghia (1844)**, which gave the US **most-favored-nation** status (matching British treaty-port concessions). This was **post-crisis** diplomacy, not pre-war.

### Embassy Mechanical Gating for 1763 Start

The mod's **inbound embassy events** (se_QING_EMBASSIES.txt, #60: Macartney, Amherst, Titsingh, Golovkin, French, Cushing) must be **date-gated** for 1763:

- **Pre-1793**: No British/French/Dutch/American embassies. Only **Russian embassies** (Kyakhta renegotiation, Orthodox mission resupply) and **Portuguese tribute missions** (Macau). These should be low-stakes, routine (trade protocol confirmation, missionary toleration requests).
- **1793: Macartney** (earliest major British embassy). Should fire only if year ≥ 1793, Britain tension > threshold, and Canton trade has been stable/growing (justifying the push for expansion).
- **1794-95: Titsingh** (Dutch, rare; can be optional).
- **1816: Amherst** (if Macartney failed and Britain tension remained high).
- **1844+: Cushing** (post-Opium War only).

### Golovkin Embassy (1805-06) (Russian, Not Chinese)

The **Golovkin Embassy (1805-06)** was a **Russian embassy to Japan**, not China (though it failed — Japan refused landing). It is sometimes confused in Western historiography. If the mod includes a "Golovkin to China" event, it is ahistorical and should be removed or replaced with an 1805-era **Russian Kyakhta renegotiation** (which did happen sporadically).

---

## (B) COURT EUROPEANS: Jesuits, Lazarists, and Orthodox (1763)

### Jesuit Dominance (1700-1773)

In 1763, the **Society of Jesus (Jesuits)** held near-monopoly status as court Europeans, serving Kangxi (r. 1661-1722), Yongzheng (r. 1722-35), and Qianlong in scientific, artistic, and technical capacities. Key figures and roles:

**Scientific Roles**:
- **Imperial Astronomy Bureau (欽天監, Qintianjian)**: Jesuits monopolized the calendar bureau from the 1660s (after defeating Chinese/Muslim astronomers in prediction contests). In 1763, the director was likely **Anton Gogeisl** (高慎思, served 1750s-70s) or a similar Jesuit. They calculated the annual calendar, predicted eclipses, and maintained astronomical instruments (including the great Beijing Observatory bronzes designed by Verbiest 1673-88).
- **Cartography**: Jesuits surveyed and mapped the empire under Kangxi (**Jesuit Atlas of China, 1718**, Régis, Jartoux, Bouvet, et al.) and continued under Qianlong (mapping Xinjiang post-1759). This was strategic intelligence controlled by the throne.

**Artistic/Engineering Roles**:
- **Giuseppe Castiglione (郎世寧, 1688-1766)**: The most famous. Italian Jesuit, court painter 1715-66 (died 1766, three years after 1763). His synthesis of European perspective + Chinese brushwork produced iconic portraits of Qianlong, battle scenes (e.g., the Zunghar campaign paintings), and the **百駿圖** (Hundred Horses). In 1763, Castiglione was **75 years old** and still active (his last major work was 1764).
- **Michel Benoist (蔣友仁, 1715-74)**: French Jesuit, mathematician and engineer. Designed the **Xiyang Lou (西洋樓, European Palaces)** fountains at the **Old Summer Palace (圓明園, Yuanmingyuan)**, combining European Baroque architecture with Chinese gardens (completed 1747-60s; destroyed 1860 by British/French). In 1763, Benoist was at the peak of his career.
- **Jean-Denis Attiret (王致誠, 1702-68)**: French Jesuit painter, worked alongside Castiglione. Active in 1763.

**Other Jesuits**: By 1763, ~20-30 Jesuits served at court (mostly French, some German/Italian/Portuguese). They lived in the **Beitang (北堂, North Church)** and **Nantang (南堂, South Church)** mission compounds in Beijing, had limited contact with Chinese Christians outside the court, and depended entirely on imperial favor.

### The 1773 Suppression and Transition to Lazarists

**Papal Suppression of the Jesuits (1773)**:  
Pope Clement XIV issued the brief ***Dominus ac Redemptor*** (1773.7.21), dissolving the Society of Jesus under pressure from Bourbon monarchies (France, Spain, Portugal). This did not immediately affect China (news traveled slowly, and the Qing court was indifferent to papal politics), but by **1775-1780**, the Beijing Jesuits had died off or formally left the order. The last major court Jesuit was **Amiot (錢德明, 1718-93)**, who continued as a *de facto* Jesuit until his death.

**Lazarists (Vincentians) Take Over (1780s-1800s)**:  
The **Congregation of the Mission (Lazarists)**, a French order, inherited the Beijing mission via the **French Académie des Sciences** and **Collège des Missions Étrangères (MEP)**. Key figures:
- **Louis-Antoine de Poirot (鮑友仁, 1735-1813)**: Lazarist, served Qianlong and Jiaqing as court artist (succeeded Attiret/Castiglione). Present in Beijing from 1770s; in 1763 he had not yet arrived (was still in Europe).
- **Joseph-Marie Amiot (錢德明, 1718-93)**: Jesuit who stayed after 1773 suppression, worked until death 1793. Translator, sinologist, correspondent with Voltaire and the Académie. Still active in 1763 as a Jesuit.

**For 1763**: Jesuits are **dominant and unchallenged**. The 1773 suppression is **10 years away**. The Lazarist takeover begins ~1780s, so Lazarists are **irrelevant in 1763**.

### Russian Orthodox Ecclesiastical Mission

The **Russian Ecclesiastical Mission (Российская духовная миссия в Пекине)** was a **standing presence** in Beijing from 1715 (formalized 1727 Treaty of Kyakhta). It ostensibly served baptized **Albazinians** (Cossack prisoners from the 1680s Nerchinsk border wars, settled in Beijing as a banner company), but functionally it was a **quasi-consular** Russian outpost.

**Mission Structure**:
- A **Russian Orthodox archimandrite** (head priest) + 3-5 junior priests + students (language students sent by St. Petersburg to learn Chinese/Manchu).
- Rotated every **10-12 years** (each "mission" was a cohort; by 1763, the **6th or 7th Mission** was resident).
- Lived in the **Beitang** compound (shared with Jesuits, later separate).

**Function**:
- Religious services for Albazinians (a few hundred people).
- **Language training** and **intelligence gathering** for Russia (students returned to Russia as interpreters/diplomats).
- Informal diplomatic back-channel (Russian state communications sometimes went via the mission, bypassing Kyakhta trade officials).

**For 1763**: The Russian mission is **established and routine**. It is **not a provocation** (the Qing tolerated it as part of the Kyakhta deal). It is **not Catholic** (Orthodox), so it is neutral in the Rites Controversy. It continues uninterrupted until the Russian Revolution (1917).

### Other Europeans at Court (1763)

- **Dominicans, Franciscans, MEP**: These Catholic orders operated **outside Beijing** (provincial missions in Fujian, Sichuan, etc.) and were **rivals of the Jesuits** in the Rites Controversy (they opposed Jesuit accommodation of ancestor rites). In 1763, they had **no court presence** (Kangxi and Yongzheng had expelled or restricted them). They resurge post-1773 Jesuit suppression but remain **provincial**, not court.
- **Protestant Missionaries**: None until the **19th century**. The first Protestant missionary to China was **Robert Morrison** (1807, LMS, based in Canton/Macau). Irrelevant for 1763.

---

## (C) ADAPTATION RECOMMENDATION

### Embassy Mechanics (Date-Gating)

**For 1763 Start**:
1. **Pre-1793**: No British/French/Dutch **crisis embassies**. Only routine:
   - **Russian Kyakhta Protocol Missions** (every 10-20 years; low-stakes, trade/border minutiae).
   - **Portuguese Macau Tribute Missions** (every 5-10 years; ceremonial, no demands).
   - These can be minor flavor events (+1 prestige for receiving barbarian tribute, maybe a minor trade-income tick).

2. **1793: Macartney Embassy** (British):
   - **Trigger**: Year ≥ 1793, Britain tension < 30 (i.e., not yet hostile), Canton trade active.
   - **Player Choices**:
     - Accept demands (open ports, permanent envoy) → Britain tension -10, but domestic prestige -5 (kowtowing to barbarians), risk of conservative faction backlash.
     - Reject demands (historical) → Britain tension +10, Qianlong's "we need nothing" prestige boost +5.
     - Compromise (some trade concessions, no envoy) → Britain tension +5, neutral domestic.
   - **Outcome Gates Next Events**: If rejected, Amherst 1816 becomes more likely; if accepted, may delay/avert Opium War.

3. **1816: Amherst Embassy** (British):
   - **Trigger**: Year ≥ 1816, Macartney failed (or didn't fire), Britain tension 30-50.
   - **Outcome**: Almost certainly failure (historical Amherst refused kowtow). Britain tension +15. Sets stage for Opium War if opium trade is also escalating (Section 4 mechanic).

4. **1844+: Cushing and Later** (American, post-Opium War):
   - Only if Opium War has occurred (or equivalent crisis). These are **post-unequal-treaty** embassies, no longer tributary but treaty-port system.

**For 1815 Start**:
- Macartney (1793) and Amherst (1816) are **historical memory** (already failed). The Opium War (1839-42) is imminent or recent past. Cushing (1844) is the next beat. No change needed.

### Court Missionary Mechanics (Composition Over Time)

**For 1763 Start**:
1. **1763-1773: Jesuit Period**:
   - Court Europeans = **~20-30 Jesuits** (mostly French, some Italian/German).
   - Roles: Astronomy Bureau (1-3 Jesuits), cartography (2-3), court painting (Castiglione, Attiret), engineering (Benoist), music/translation (Amiot).
   - Modifier: **"Jesuit Scientific Service"** → +5% tech research speed (or equivalent; they provide European astronomical/mathematical knowledge), +2 prestige (exotic foreign talent). This is **positive** for the Qing (the Jesuits serve loyally).
   - **Russian Orthodox Mission** (~5-10 people) is also present; neutral (no modifier, just flavor).

2. **1773-1780: Transition**:
   - Event: "Suppression of the Jesuits" (~1773-75). Jesuits die off or leave.
   - Player choices:
     - Invite **Lazarists** (French) to replace them → maintain modifier (renamed "Lazarist Scientific Service").
     - Rely on Chinese astronomers → lose modifier, but +3 prestige ("rejected foreign dependence").
     - Let the court mission collapse → lose modifier, potential calendar errors (minor legitimacy hit if lunar calendar mispredicts eclipse).

3. **1780-1815: Lazarist Period** (if invited):
   - Court Europeans = **~10-20 Lazarists** + lingering ex-Jesuits (Amiot until 1793).
   - Same roles as Jesuits but reduced prestige (Lazarists were less famous/skilled). Modifier: **"Lazarist Scientific Service"** → +3% tech research (weaker than Jesuits).

4. **Post-1815: Decline**:
   - By 1815, court European scientific service is **vestigial**. The Jiaqing and Daoguang emperors were less interested; Qing astronomy stagnated. The Opium War (1839) and subsequent Western military superiority revealed the **obsolescence** of Jesuit-era science. The court mission persists (Catholic Beitang/Nantang survive) but is no longer prestigious.

**For 1815 Start**:
- Court Europeans are **Lazarists (post-Jesuit) + Russian Orthodox**. Weak positive modifier or none. The dynamic Jesuit era is over. The focus shifts to **treaty-port missionary influx** (post-1842), which is **outside** court control (Protestant LMS, Baptist, Presbyterian missions in Shanghai, Ningbo, etc.).

---

## Summary Table: Embassy and Court European Periodization

| **Date Range** | **Embassies** | **Court Europeans** |
|---------------|--------------|---------------------|
| **1700-1763** | Russian (Kyakhta, routine), Portuguese (Macau tribute), Papal (Rites, failed) | **Jesuits dominant** (Castiglione, Benoist, Attiret, Amiot, ~20-30 total) + Russian Orthodox (~5-10) |
| **1763-1773** | Same (pre-Macartney) | Jesuits unchallenged |
| **1773-1793** | Macartney (1793, British, failed) | **Jesuit→Lazarist transition** (1773 suppression; Lazarists arrive ~1780s) |
| **1793-1816** | Amherst (1816, British, failed worse) | Lazarists + ex-Jesuits (Amiot dies 1793) |
| **1816-1842** | No major embassies (pre-Opium War) | Lazarists (court declining interest) |
| **1842-1860** | Cushing (1844, US, post-war), treaty-port consuls (British, French, etc.) | Lazarists at court + **mass treaty-port missionaries** (outside court control) |

**ADAPTATION RECOMMENDATION**:  
1. **Date-gate all embassy events** to historical sequence (Macartney 1793, Amherst 1816, Cushing 1844). For 1763 start, only Russian/Portuguese routine missions fire pre-1793.
2. **Court European composition**:
   - **1763-1773**: "Jesuit Scientific Service" (+5% tech research or equivalent) active. ~20-30 Jesuits + Russian Orthodox mission.
   - **1773-1780**: "Jesuit Suppression" event → player choice (invite Lazarists, go Chinese-only, or let it lapse).
   - **1780+**: "Lazarist Scientific Service" (+3% tech research) if invited; otherwise no modifier.
   - **1815+**: Lazarists persist but weakened; treaty-port missionary influx (separate mechanic, not court-controlled).
3. **Russian Orthodox Mission**: Always present 1727-1917, neutral/flavor (or minor +1 relations with Russia).

## 6. OTHER ANACHRONISTIC MECHANICS — Triage List

This section identifies imported Qing mechanics from the 1815-start branch that are **era-mismatched** for 1763 and provides **earliest sensible fire dates** for each. Mechanics are classified as:
- **FINE AS-IS**: Era-appropriate for 1763, no gating needed.
- **DATE-GATE**: Relevant but historically post-1763; gate to real date.
- **DISABLE/REMOVE**: Fundamentally anachronistic for 1763, should not fire even late-game.

---

## ANACHRONISTIC (Date-Gate or Disable)

### Self-Strengthening Movement (洋務運動, ~1860s-1890s)
**Imported Mechanic**: Likely tech-transfer events, foreign advisors, arsenals (Jiangnan Arsenal 1865, Fuzhou Shipyard 1866), military academies, students sent abroad.

**Historical Dates**: 1860s-1895 (post-Opium War + Taiping trauma). Key figures: Zeng Guofan 曾國藩, Li Hongzhang 李鴻章, Zuo Zongtang 左宗棠. The movement was a **response to defeat** (Opium War 1839-42, Second Opium War 1856-60, Taiping Rebellion 1850-64). Its premise ("Chinese learning for essence, Western learning for utility" 中體西用) assumed Qing institutional survival but Western military tech adoption.

**1763 Context**: **Nonsensical**. The Qing in 1763 had just **crushed the Zunghars** (1759) and were at peak military confidence. There is no defeat to respond to, no perception of Western military superiority (the Qing saw Europeans as maritime traders, not land-power threats). Western firearms (matchlocks, light cannon) were known and **selectively adopted** by the Qing (Firearms Battalion 火器營 under Yongzheng/Qianlong used some European-style guns), but this was **ad hoc incorporation**, not a systemic "Self-Strengthening" ideology.

**Recommendation**: **DATE-GATE to 1860s**. Self-Strengthening events should **not fire before 1860** (post-Second Opium War + Taiping). Even if the 1763 game runs to 1900, these mechanics are post-1860 only. Alternatively, if the player suffers a **major military defeat** to a Western power (e.g., loses a war to Britain/France/Russia post-1840), a "proto-Self-Strengthening" response could fire early (but still post-1840).

---

### Students Abroad / Foreign Study Programs
**Imported Mechanic**: Missions sending Qing students to Europe/America (e.g., **Chinese Educational Mission to the US, 1872-81**, 120 boys sent to Hartford, Connecticut; **Fuzhou Navy School students to Europe, 1870s-80s**).

**Historical Dates**: 1860s-1890s (Self-Strengthening era). The **Yung Wing 容閎 mission** (1872-81) was the first large-scale program (ended prematurely when conservatives opposed Westernization of the students). Earlier, isolated students (Yung Wing himself went to Yale 1850-54, but as a **private Cantonese**, not Qing-sponsored).

**1763 Context**: **Absurd**. No Qing official in 1763 would conceive of sending banner or Han youth to Europe for education (the Qing saw Europe as peripheral barbarians). The **Jesuits brought European knowledge TO China**; there was no reverse flow. Even in 1815, no such programs existed.

**Recommendation**: **DATE-GATE to 1870s** (or 1860s at earliest if player is desperate post-defeat). Students-abroad is a **post-Taiping, post-unequal-treaties** desperation move.

---

### Taiping Rebellion Missions (1850-1864)
**Imported Mechanic**: Likely event chains or mission tree related to the **Taiping Heavenly Kingdom** (太平天國, 1850-64), the largest civil war in Chinese history (~20-30M dead).

**Historical Dates**: 1850-64. **Hong Xiuquan 洪秀全**, the Hakka visionary claiming to be Jesus's brother, launched the rebellion in Guangxi 1850, captured Nanjing 1853 (renamed Tianjing 天京), and was suppressed by **Zeng Guofan's Xiang Army** (湘軍, irregular provincial force) and **Li Hongzhang's Huai Army** (淮軍) in 1864. The Taiping crisis nearly toppled the Qing and forced the Self-Strengthening reforms.

**1763 Context**: **Impossible**. The Taiping ideology required **Protestant Christianity** (Hong was exposed to missionary tracts in Canton in the 1840s) + **Hakka millenarianism** + **social collapse** (post-Opium War banditry, land pressure). None of these exist in 1763: Christianity is restricted to Jesuits (Catholic, not Protestant); Canton missionaries are decades away (Robert Morrison, first Protestant, arrives 1807); Hakka-Punti ethnic tensions in Guangdong are latent but not explosive; and social stability is high (pre-White Lotus, pre-Opium War).

**Recommendation**: **DATE-GATE to 1850s**. Taiping events cannot fire before 1850. If the game runs 1763-1900 and the player reaches 1850, Taiping should fire **only if** (a) year ≥ 1850, (b) corruption high, (c) major unrest or recent defeat (e.g., Opium War), (d) Christian missionary presence in southern provinces (Canton, Guangxi). Otherwise disable.

---

### Summer Palace Sack (圓明園, 1860) and Navy Funds Dilemma (1888)
**Imported Mechanic**: Likely a **mission tree** (#74, per memory) covering:
1. **Construction of the Summer Palace** (圓明園 Yuanmingyuan, "Old Summer Palace").
2. **1860 Sack** (British/French troops looted and burned it during the Second Opium War).
3. **1888 Navy Funds Scandal** (Empress Dowager Cixi 慈禧 allegedly diverted Beiyang Fleet funds to rebuild the 頤和園 Yiheyuan, "New Summer Palace" — though memory notes the Cixi story is contested historiography; see imp19c-summer-palace-history.md).

**Historical Dates**:
- **圓明園 construction**: Began **1707** (Kangxi), expanded massively under Yongzheng (1720s-30s) and Qianlong (1740s-60s). The **Xiyang Lou (European Palaces)** fountains (Benoist, Castiglione) were completed **1747-60s**. In **1763, the Old Summer Palace is COMPLETE and operational** (Qianlong's favorite retreat).
- **1860 Sack**: October 1860 (Second Opium War; Lord Elgin ordered the burning as punishment for Qing torture of British envoys).
- **頤和園 (New Summer Palace)**: Rebuilt **1886-95** by Cixi (using Qing treasury and naval funds controversially; though 陳悅's research shows the "navy-funds" story is exaggerated, as noted in memory).

**1763 Context**:
- **Construction phase**: **HISTORICAL in 1763**. The Old Summer Palace (圓明園) is **already built** by 1763 (the Xiyang Lou was finished ~1760s). A construction-phase event is **anachronistic UNLESS** it is a **reconstruction/expansion** option (e.g., player can invest in further gardens/palaces).
- **1860 Sack**: Impossible in 1763 (requires Second Opium War, which requires First Opium War 1839-42, which requires 1800s opium trade). **DATE-GATE to 1860**.
- **1888 Navy Funds**: Impossible in 1763 (requires Beiyang Fleet, which is 1880s Self-Strengthening; requires Cixi as Empress Dowager, which is 1860s-1908). **DATE-GATE to 1888** or disable.

**Recommendation**:
- **FOR 1763 START**: The Old Summer Palace (圓明園) is **already complete** at game start. Flavor text: "The Qianlong Emperor's Yuanmingyuan, with its European-style fountains, stands as the jewel of the dynasty." No construction event needed (it's a sunk cost). The **1860 Sack** event can remain in the code but **DATE-GATE to 1860** (fires only if year ≥ 1860, Second Opium War occurred, British/French armies reached Beijing). The **1888 Navy Funds** event is **unrelated** (it concerns the 頤和園, a different palace) and should be **DATE-GATE to 1888**.
- **FOR 1815 START**: The Old Summer Palace exists (will be sacked in 1860 if Second Opium War fires). The 1888 Navy Funds event is 1888-appropriate.

---

### Golden Urn Lottery (金瓶掣籤, 1793-)
**Imported Mechanic**: If the mod includes a **Tibetan/Mongolian succession mechanic** using the Golden Urn lottery (金瓶掣籤), this is **post-1793**.

**Historical Dates**: **Instituted 1793** by Qianlong (after the 1788-92 Nepal/Gurkha War, during which the Qing intervened in Tibet and imposed tighter control). The Golden Urn system required **drawing lots from a golden urn** to select reincarnated Tibetan/Mongolian Buddhist leaders (e.g., Dalai Lama, Panchen Lama, Jebtsundamba Khutuktu in Mongolia) in the presence of Qing ambans (駐藏大臣), to prevent aristocratic families from monopolizing the selection. This was a **Qing administrative reform** to control Tibetan/Mongolian religious authority.

**1763 Context**: **Does not exist yet**. The 1763 Qing controlled Tibet via the **amban system** (established 1720s under Kangxi/Yongzheng after expelling the Zunghars) but had not yet imposed the Golden Urn. The **7th Dalai Lama** (1708-1757) had recently died; the **8th Dalai Lama** (1758-1804) was enthroned 1762 (age 4), **without** the Golden Urn (selected by traditional Tibetan methods). The Golden Urn was instituted in **1793** (after the 8th Dalai Lama's reign, for future successions).

**Recommendation**: **DATE-GATE to 1793**. If the mod has a Tibet/amban mechanic, the Golden Urn option should **not** appear before 1793. Pre-1793, Tibetan succession is **Tibetan-controlled** (Qing ambans observe but do not dictate). Post-1793 (especially post-1792 Nepal War), the Qing impose the Golden Urn as a reform option (player choice: impose it for +control over Tibet, -Tibetan loyalty; or allow traditional methods, -control +loyalty).

---

### Japan Pre-Perry Arc (1850s Bakumatsu)
**Imported Mechanic**: Likely a **mission tree** or event chain related to **Qing-Japan interactions** in the **Bakumatsu 幕末 period** (1850s-1868: Perry's Black Ships 1853, Boshin War 1868-69, Meiji Restoration 1868). Memory references imp19c-Japan-pre-Perry-research.md and imp19c-AI-autonomous-arc-verbs.md (US #93, Japan #94 arcs).

**Historical Dates**: Japan-Qing **direct contact** in the 19th century was minimal until the **1870s** (post-Meiji Restoration). The **1850s-1860s** saw:
- **Perry (1853-54)**: Forced Japan to open (US, not Qing-related).
- **Boshin War (1868-69)**: Meiji overthrow of Tokugawa shogunate (internal Japanese, not Qing-related).
- **1871: Sino-Japanese Treaty of Tianjin**: First modern equal treaty (not tributary). Japan recognized Qing as equal, Qing recognized Japan's sovereignty over Ryukyu (contested — Ryukyu was dual-tributary).
- **1874: Japan-Taiwan Incident**: Japan invaded Taiwan (punitive expedition over Ryukyuan shipwreck); Qing paid indemnity, implicitly conceding Ryukyu to Japan.
- **1894-95: First Sino-Japanese War**: Japan crushed Qing; Treaty of Shimonoseki (Taiwan ceded, Korea independence recognized).

**1763 Context**: Qing-Japan relations in 1763 were **non-existent at the state level**. Japan (under the Tokugawa shogunate, 1603-1868) enforced **sakoku 鎖國 seclusion policy** (1639-1854): no foreign contact except:
- **Dutch VOC** at Dejima, Nagasaki (restricted trade enclave).
- **Chinese merchants** at Nagasaki (private Fujian/Cantonese traders, **not Qing state missions**). This was the **Tojin trade** (唐人貿易, "Tang people trade"), supervised by the shogunate but not a tributary relationship (the shogunate rejected Ming/Qing suzerainty claims).
- **Ryukyu Kingdom** (琉球, modern Okinawa): **Dual tributary** to both Qing (since 1644) and Satsuma domain of Japan (since 1609 invasion). The Qing treated Ryukyu as a loyal tributary; Japan treated it as a vassal. This arrangement persisted until 1874-79 (Japan annexed Ryukyu 1879).

The Qing and Tokugawa Japan had **no formal diplomatic relations** in 1763. The Qing considered Japan a "barbarian" state beyond the pale; Japan ignored Qing suzerainty claims. The **Opium War (1839-42)** was observed by Japan (via Dutch *Fusetsugaki* 風說書 reports at Nagasaki), which alarmed the shogunate and contributed to the decision to end sakoku (i.e., the Opium War was Japan's **cautionary tale**: "if we don't modernize, we'll be the next China"). But in 1763, this is 76 years away.

**Recommendation**: **DATE-GATE to 1850s-1870s**. Any Japan-Qing arc (missions, diplomatic plays, rivalry) should **not fire before 1850**. Even then:
- **1850s-1868**: Japan is in internal crisis (Bakumatsu), not interacting with Qing (both are targets of Western pressure; no rivalry yet).
- **1870s**: First contact (1871 treaty, 1874 Taiwan incident) → tension begins.
- **1894-95**: First Sino-Japanese War → full arc.

For a **1763 start**, Japan is **irrelevant** until the 1870s. If the mod includes Japan-Qing mechanics, disable them pre-1870 or make them purely **Ryukyu-mediated** (e.g., "Ryukyu tribute mission reports on Japanese seclusion" flavor event, no mechanical impact).

---

## FINE AS-IS (No Gating Needed)

These imported mechanics are **era-appropriate for 1763** and should remain active:

### Grand Council (軍機處, est. 1730s)
**Historical Dates**: Established **~1730s** under Yongzheng (formalized ~1732-35) as a **confidential inner-cabinet** bypassing the traditional Grand Secretariat (內閣). Qianlong relied on it heavily for military campaigns (Xinjiang, Burma, Nepal, etc.). The Grand Council was at **peak effectiveness in 1763**.

**Recommendation**: **No change**. The Grand Council mechanic (#74, memory: GC office redesign, expansion 2026-07) is fully appropriate for 1763. It is already **operating** at game start.

---

### Ambans (駐藏大臣 etc.) and Ili Governorship (伊犁將軍, est. 1762)
**Historical Dates**:
- **Ambans in Tibet** (駐藏大臣): Established **1720s** (Kangxi/Yongzheng, after expelling Zunghars from Tibet). Two Qing ambans in Lhasa supervised Tibetan affairs. Fully operational in 1763.
- **Ili Governorship** (伊犁將軍): Established **1762** (immediately after Xinjiang conquest 1755-59) at the fortress city of **Huiyuan** (惠遠城, near modern Yining). The Ili General-in-Chief (伊犁將軍) governed the newly conquered region (Zungharia + Altishahr). In **1763, this is brand new** (1 year old) but operational.

**Recommendation**: **No change**. Both are era-appropriate. The Ili Governorship is a **recent establishment** (1762), so it can be a **"just completed" milestone** at 1763 game start (flavor: "The Ili garrison secures the new frontier...").

---

### Tributary System and Canton Customs (1757)
**Historical Dates**:
- **Tributary system** (朝貢體系): Ancient, fully operational throughout Qing. Korea, Ryukyu, Vietnam, Siam, Burma, Nepal, etc., sent tribute missions. This is **core Qing foreign relations** in 1763.
- **Canton System** (1757): Just established (see Section 5). Restricts Western maritime trade to Canton. Operational in 1763.

**Recommendation**: **No change**. Both are 1763-appropriate. The Canton System is **recent** (1757 edict), so it's a **fresh policy** at game start (flavor: "The Canton monopoly has just been imposed...").

---

### Gaitu Guiliu (改土歸流, "Replace Chieftains with [Appointed] Officials")
**Historical Dates**: Ongoing throughout the Qing. Major phases under **Yongzheng (1720s-30s)** in Guizhou, Yunnan, Sichuan (converting hereditary Miao/Yi/Tujia chieftains to appointed Qing magistrates) and continuing under Qianlong. In **1763, gaitu guiliu is active policy** (the Miao rebellions of the 1790s-1800s were partly backlash against it, but in 1763 it's still successful expansion).

**Recommendation**: **No change**. Gaitu guiliu mechanics (if present) are 1763-appropriate. The process is **ongoing** (not complete), so it can be a **player-driven expansion option** (invest in converting chieftaincies → +control, +tax, risk of rebellion if mishandled).

---

### Subject Integration / Tributary Promotion Mechanics
**Historical Dates**: The Qing's multi-tiered subject system (direct provinces 省, protectorates like Mongolia/Tibet, tributary states like Korea/Vietnam, frontier vassals like Xinjiang begs) was **fully operational in 1763**. The Ili Governorship (1762) represented the integration of Xinjiang into the Qing administrative system (though it remained a military frontier, not a full province until 1884). The mod's subject-integration verbs (promote vassal to protectorate, demote rebellious subject, etc., per memory imp19c-subject-interactions.md) are **historically grounded** for 1763.

**Recommendation**: **No change**. Subject mechanics are 1763-appropriate. In fact, **1763 is more dynamic** than 1815 for subject integration (the Qing in 1763 are still expanding and consolidating Xinjiang, whereas 1815 is post-expansion stasis).

---

## DATE-GATE SUMMARY TABLE

| **Mechanic** | **Historical Date** | **Earliest Fire Date for 1763 Start** | **Gating Condition** |
|-------------|--------------------|------------------------------------|----------------------|
| **Self-Strengthening Movement** | 1860s-1890s | 1860 | Year ≥ 1860, major military defeat to Western power |
| **Students Abroad** | 1870s-1880s | 1870 | Year ≥ 1870, Self-Strengthening active |
| **Taiping Rebellion** | 1850-1864 | 1850 | Year ≥ 1850, high corruption, unrest, Christian missionary presence in south |
| **Summer Palace Sack (圓明園)** | 1860 | 1860 | Year ≥ 1860, Second Opium War, British/French in Beijing |
| **Navy Funds Dilemma (頤和園)** | 1888 | 1888 | Year ≥ 1888, Beiyang Fleet exists, Cixi in power |
| **Golden Urn Lottery (金瓶掣籤)** | 1793 | 1793 | Year ≥ 1793, post-Nepal War reform option |
| **Japan-Qing Arcs (Perry/Boshin)** | 1850s-1894 | 1850 (Japan internal), 1870 (Qing-Japan contact) | Year ≥ 1850 (Japan modernization), ≥ 1870 (Qing-Japan diplomatic tension) |
| **Macartney Embassy** | 1793 | 1793 | Year ≥ 1793, Britain tension 10-30, Canton trade active |
| **Amherst Embassy** | 1816 | 1816 | Year ≥ 1816, Macartney failed, Britain tension 30-50 |
| **Opium War** | 1839-1842 | 1839 | Year ≥ 1830s, Britain tension > 50, opium trade escalated (requires Section 4 opium-trade mechanic) |

---

## NOTES

1. **FOR 1763 START**: Disable or date-gate all mechanics listed above. The game should **feel different** from 1815 — no Western military threat, no reform pressure, no Japan rivalry, no treaty ports. The Qing are at their **zenith**. Challenges are **internal** (corruption over time, succession, frontier consolidation) and **regional** (Burma, Nepal, Central Asian khanates), not European.

2. **FOR 1815 START**: Most of these mechanics are already approaching or past their historical dates (Macartney/Amherst are memory, Opium War is imminent, Self-Strengthening is 40 years away). No major changes needed.

3. **LONG-GAME CONVERGENCE**: If a player starts in 1763 and plays to 1900, the game should **converge** with the 1815-start timeline by the 1840s-1860s (Opium War, Taiping, Self-Strengthening). The date-gated events ensure this happens organically without forcing 1815-era problems on a 1763 start.

**ADAPTATION RECOMMENDATION**:  
Audit all imported Qing mechanics and **date-gate anachronistic content** per the table above. For a 1763 start, the player should experience the **High Qing zenith** (strong military, fiscal surplus, Grand Council efficiency, tributary stability) for the first 30-50 years, with decline and Western pressure gated to historical inflection points (1775 Heshen, 1794 White Lotus, 1839 Opium War, 1850 Taiping, 1860 Self-Strengthening). Fine-as-is mechanics (Grand Council, ambans, Ili, tributary system, gaitu guiliu) should remain active from game start.

---

## IMPLEMENTATION STATUS (task #304, as built)

- **§1 Decline** — DONE. High Qing era flag + `qing_high_qing_prosperity` modifier seeded pre-1772 (low corruption 12, harmony 82); passive decay creep + decline-reaction rolls suppressed while the era is active. Condition-driven Heshen inflection (`qing_decline.40` yearly checker → `.41` player-facing event): ends the era on the earned conjunction (corruption ≥20 + aged/unpopular emperor + overmighty courtier) or an **AI-only** 1796 backstop (a human player is never railroaded off the golden age). All three date thresholds aligned at 1772.1.1. 1815 start unchanged.
- **§2 Military** — DONE (land). Date-aware `SE_qing_armies`: a larger, **commander-less** High Qing OOB pre-1772 (avoids the 1815-commander `exists=$cmd$` guard that would otherwise *shrink* the 1763 army by dropping garrisons under unborn officers). Navy unchanged (same brown-water type 1763↔1815, per this section).
- **§3 Emperor Emeritus** — DONE. Historical 太上皇 abdication path (`se_QING_EMERITUS.txt` + `qing_emeritus.1/.2` + `on_character_death` hook), generic/reusable, enthrones the historical Jiaqing (char:224) when Qianlong (char:214) abdicates. char:214 first_name → "Qianlong Emperor" (era-name display, mirroring char:224 "Jiaqing").
- **§4 Great Power interest** — DONE. `QING_greatgame_pulse` tension drift suppressed before 1793 (the Zongli Yamen it models is an 1861 institution; the powers are not yet pressing China). Ramps from Macartney 1793. 1815 start unchanged.
- **§5 Europeans at court / embassies** — DONE (embassy). British embassies scheduled on real dates for a 1763 start (Macartney 1793, Amherst 1816) via `qing_embassy_dated_schedule`, diverted from the decline roll; NED/RUS/FRA/USA embassies still roll-driven. Missionary-persecution (`qing_missionary.1`, 教案) needs **no gate** — it fires only from the (era-suppressed) decline roll gated on `qing_antichristian_sentiment ≥ 40`, which is 0 at start and only builds post-Heshen; the High Qing court's Jesuit tolerance is thus modeled by inaction, not a persecution event. Jesuit→Lazarist (1773) / Orthodox-mission court composition = flavor content, deferred (not a live mechanic).
- **§6 Era-mismatch triage (self-strengthening, taiping, summer-palace sack, golden urn, japan pre-perry)** — date-gating in progress (planned per subsystem; applied sequentially).
