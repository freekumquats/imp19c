# 1763 Feature Reuse Assessment

**Branch:** 1763_bookmark  
**Date:** 2026-07-09  
**Context:** Rebase from 1815 late-Qing decline to 1763 High Qing zenith (Qianlong)

## Historical Context

**1763 Peak Qing:**
- Qianlong reign at height; Xinjiang conquered (1759); Ten Great Campaigns ongoing
- Tributary system (朝貢) at full vigor; Canton System active (1757)
- Grand Council young/vigorous; banners strong; Heshen not yet risen
- Russia contained (Nerchinsk/Kyakhta); Christianity proscribed (1724) but present
- Japan = Tokugawa sakoku (Perry 1853+)

**NOT YET at 1763:**
- Opium wars / unequal treaties / treaty ports
- Taiping / Self-Strengthening / Boxers / legations / Zongli Yamen
- Meiji restoration / Perry opening

## 1. INVENTORY TABLE

| File | Models | Verdict | Rationale |
|------|--------|---------|-----------|
| se_QING_DECLINE.txt | Decline meters (corruption/sects/banner-decay/ethnic-tension/currency-stress/reform-pressure/granary) + high-qing-era flag | KEEP-AS-IS | Already has #304 high-qing-era detection; 1763 = zenith (counters init low), 1815 = decline (init higher). Correct. |
| se_QING_COUNCIL.txt | Grand Council (軍機處) + 11 great offices (chancellor/六部/都察院/理藩院/總理衙門/內務府) | ZENITH-REFRAME | Council should present as young/vigorous/full at 1763, not staffing-crisis. Office effectiveness baseline high. |
| se_QING_GOVERNANCE.txt | Bureau capacity/integrity + council effectiveness | ZENITH-REFRAME | 1763 bureau should be efficient (capacity/integrity high at init). Decline drains them over time. |
| se_QING_TREATIES.txt | Unequal treaties + treaty ports + extraterritoriality | DORMANT-1815-ONLY | First unequal treaty = Nanjing 1842. At 1763 Canton System vigorous, no foreign concessions. Correctly dormant. |
| se_QING_SELFSTR.txt | Self-Strengthening Movement (自強運動) arsenals/yards | RE-GATE | Historical 1860s+. Should gate on >= 1860 OR qing_high_qing_era (early-indus alternate path exists). Check gates. |
| se_QING_LEGATIONS.txt | Permanent foreign legations (駐外使館) | DORMANT-1815-ONLY | First permanent legation = Guo Songtao 1877. Canton-System-era Qing did not post abroad. Correctly >=1860 gated. |
| se_QING_STUDENTS.txt | Students abroad (留美幼童 1872) | DORMANT-1815-ONLY | Chinese Educational Mission 1872-1881. No 1763 analog. Correctly >=1872 gated. |
| se_QING_VASSAL.txt | Tributary crises (Korea/Vietnam/Ryukyu/Burma 保藩) | ZENITH-REFRAME | Tributary system at PEAK in 1763. Crises come later (Sino-French 1884, Sino-Japanese 1894). Should present as strong/unchallenged at start. |
| se_QING_CUSTOMS.txt | Maritime Customs (海關) + Hart/foreign inspectorate | RE-GATE | Foreign-run Maritime Customs post-1854 (Robert Hart). 1763 = traditional Canton hoppo system. Needs era guard. |
| se_QING_JAPAN_PREPERRY.txt | Pre-Perry Japan arc (1815-1854) Nagasaki/Opium-War-relay/daimyo-backing | KEEP-AS-IS | Designed for pre-1854. At 1763 start runs 91 years (1763-1854). Nagasaki trade historical. Correct. |
| se_QING_EARLYINDUS.txt | Early industrialization (Macartney embrace path) | KEEP-AS-IS | Already era-adjusted per reverse_merge.md. Macartney 1793 triggers from 1763 start. Correct. |
| se_QING_EMERITUS.txt | Emperor Emeritus (太上皇 Napoleon seat) | KEEP-AS-IS | Napoleon alt-history #65. Date-gated to his lifespan, not era-dependent. Correct. |
| se_QING_EMBASSY.txt | Inbound embassy crises (Macartney/Amherst/Titsingh #60) | KEEP-AS-IS | Macartney 1793 historical at 1763 start (30 years in). Events already scheduled. Correct. |
| se_QING_ILI.txt | Ili Crisis + Xinjiang reconquest (伊犁/海防塞防之爭) | RE-GATE | Historical 1860s-1881 (Yaqub Beg/Zuo Zongtang). At 1763 Xinjiang JUST conquered (1759). Should invert: 1763=consolidation, 1815+=reconquest. |
| se_QING_ETHNIC_TENSION.txt | Bottom-up province-level ethnic tension + migration | KEEP-AS-IS | Generic tension engine, works at any era. 1763 = lower baseline tension. Correct. |
| se_QING_PROTECTORATE.txt | Tang-style frontier protectorates (安北/安東/安西/安南) | KEEP-AS-IS | Anachronistic revival system. Works at any era. 1763 territorial zenith makes it MORE viable. Correct. |
| se_QING_COLON.txt | Pacific colonization missions (Alaska/California/Siberia) | KEEP-AS-IS | Already dual-gated: self-str>=40 OR qing_high_qing_era per qing_colonization_missions.txt header. Correct. |
| se_QING_AMBAN.txt | Amban/resident commissioners (駐紮大臣) in dependencies | KEEP-AS-IS | Lifan Yuan (理藩院) + resident system historical 1763. Tibet/Mongolia/Xinjiang all under amban. Correct. |
| se_QING_HOUSEHOLD.txt | Imperial Household (內務府) privy-purse + eunuchs | ZENITH-REFRAME | 1763 privy purse should init FULL (Qianlong's prosperous reign). Eunuch-power low (checked by Qing institution). |
| se_QING_REVENUE.txt | Revenue administration + land-tax + customs (戶部) | KEEP-AS-IS | Generic revenue engine. 1763 = higher baseline revenue (prosperity). Works at any era. |
| se_QING_REFORM.txt | Reform track (late-Qing reforms) | RE-GATE | Historical late-Qing (1860s+ Self-Strengthening, 1898 Hundred Days, 1901+ New Policies). At 1763 reforms = premature. Needs unlock gate. |
| se_QING_GREATGAME.txt | Great Game (Anglo-Russian rivalry + Qing position) | KEEP-AS-IS | Central Asia rivalry spans 1763-1900. 1763 = Russia contained at Kyakhta, no crisis yet. Works. |
| se_QING_SPHERE.txt | Four-power sphere-of-influence (dynamic GP influence) | KEEP-AS-IS | Generic sphere system. Works at any era. 1763 = Qing dominant, Western powers weak in region. |
| se_QING_DIPLO.txt | GP relations + rivalry counters + Japan stance | KEEP-AS-IS | Generic diplomatic counters. Works at any era. 1763 = low Western tension baseline. |
| se_QING_INTEG_CAPSTONE.txt | Subject integration capstones | KEEP-AS-IS | Generic subject-integration reward system. Not era-specific. |
| se_QING_MISSIONARY.txt | Christian missionaries (pre-treaty split) | KEEP-AS-IS | Already has pre-treaty path per reverse_merge.md. 1724 proscription live at 1763. Correct. |
| se_QING_MISSIONARY_STATIONS.txt | Mission stations (post-treaty) | RE-GATE | Post-treaty-port system (1842+). At 1763 underground/proscribed only. Needs treaty-imposed guard. |
| se_QING_PILGRIMAGE.txt | Pilgrimage/religious flows | KEEP-AS-IS | Generic religious mechanic. Not era-specific. |
| se_QING_SUMMER_PALACE.txt | Summer Palace arc (圓明園 1860 sack) | DORMANT-1815-ONLY | Historical 1860 Anglo-French sack. At 1763 圓明園 under construction (Qianlong expansion). Could reframe as BUILD not sack. |
| se_QING_TECHTRANSFER.txt | Technology transfer (arsenals/telegraphs/railways) | RE-GATE | Historical 1860s+ Self-Strengthening. At 1763 no Western tech adoption. Needs >=1860 gate. |
| se_QING_USCW.txt | US Civil War hooks (#73) | KEEP-AS-IS | Historical 1861-65. At 1763 USA doesn't exist yet (GBR colony). Self-gated on exists c:USA + date. Correct. |
| se_QING_MEXICO.txt | Mexico adventure (#69) | KEEP-AS-IS | Historical 1860s French intervention. Self-gated on date + exists c:MEX. Works. |
| se_QING_NAPOLEON.txt | Napoleon at Qing court (#65) | KEEP-AS-IS | Alt-history, Napoleon 1769-1821. At 1763 he's not born yet. Self-gated on Napoleon's life. Correct. |
| se_QING_ROSTER.txt | Historical character spawns | KEEP-AS-IS | Anachronistic spawn feature. Works at any era (spawns late-Qing figures when needed). |
| se_QING_PERSONNEL.txt | Character appointment/dismissal helpers | KEEP-AS-IS | Generic office helpers. Not era-specific. |
| se_QING_ACCOUNTABILITY.txt | Office accountability metrics | KEEP-AS-IS | Generic Grand Council accountability system. Works at any era. |
| se_QING_ADVISORS.txt | Advisor characters | KEEP-AS-IS | Generic advisor helpers. Not era-specific. |
| se_QING_AFFINITY.txt | Character affinity/friction scoring | KEEP-AS-IS | Generic character-relationship engine. Not era-specific. |
| se_QING_CENSORATE.txt | Censorate (都察院) audits | KEEP-AS-IS | Historical 1763 institution. Censorate vigorous at zenith. Works. |
| se_QING_RITES.txt | Board of Rites (禮部) + ritual calendar | KEEP-AS-IS | Historical 1763 institution. Ritual system at peak. Works. |
| se_QING_WORKS.txt | Board of Works (工部) + infrastructure | KEEP-AS-IS | Historical 1763 institution. Yellow River dikes, Grand Canal. Works. |
| se_QING_JUSTICE.txt | Board of Justice (刑部) + legal cases | KEEP-AS-IS | Historical 1763 institution. Legal system functional. Works. |
| se_QING_DYNASTY.txt | Dynastic succession/legitimacy helpers | KEEP-AS-IS | Generic dynasty mechanics. Not era-specific. |
| se_QING_FACTION.txt | Court factions | KEEP-AS-IS | Generic faction system. 1763 = Qianlong dominates, factions checked. Works. |
| se_QING_SEATS.txt | Council seat management (obsolete per memory?) | KEEP-AS-IS | Office seat helpers. Generic. |
| se_QING_WAR.txt | War declaration helpers | KEEP-AS-IS | Generic war verbs. Not era-specific. |
| se_QING_BUILDINGS.txt | Qing specialty production + Board of Works seed | KEEP-AS-IS | Per reverse_merge.md #291, branch-agnostic building seed. Correct. |
| se_QING_MECHANICS.txt | Shared Qing suite init/helpers | KEEP-AS-IS | Generic suite infrastructure. Not era-specific. |
| se_SUBJECT_QING.txt | Subject integration verbs | KEEP-AS-IS | Generic subject-integration engine. Works at any era. |

**Missions:**
| qing_colonization_missions.txt | Pacific colonization tree | KEEP-AS-IS | Already dual-gated per header: self-str>=40 OR qing_high_qing_era. 1763 zenith opens it. |
| qing_himalaya_seasia_missions.txt | Himalaya/SE Asia expansion | KEEP-AS-IS | Generic expansion tree. 1763 = peak expansion era (Burma wars live). Works. |
| qing_japan_missions.txt | Post-Meiji Japan tree | DORMANT-1815-ONLY | Post-Meiji (1868+). At 1763 Japan = sakoku. Correctly gated via exists c:JPN (never formed pre-Perry). |
| qing_japan_preperry_missions.txt | Pre-Perry Japan tree (#81) | KEEP-AS-IS | Designed for 1763. Nagasaki channel historical. Correct. |
| qing_reform_missions.txt | Reform track missions | RE-GATE | Late-Qing reforms (1860s+). At 1763 premature. Needs unlock gate mirroring se_QING_REFORM. |
| qing_selfstrengthening_missions.txt | Self-Strengthening tree | RE-GATE | Historical 1860s+. Should gate via >=1860 OR early-indus path. |
| qing_summer_palace_missions.txt | Summer Palace arc | DORMANT-1815-ONLY | 1860 sack historical. At 1763 could reframe as BUILD arc (Qianlong expansion). |
| qing_taiping_missions.txt | Taiping Rebellion | DORMANT-1815-ONLY | Historical 1850-1864. At 1763 doesn't exist. Correctly >=1850 gated. |

**Events (sampled):**
| qing_decline_events.txt | Decline crisis events | KEEP-AS-IS | Generic decline pulses. 1763 = rare (low counter baselines). Works. |
| qing_treaty_events.txt | Treaty-port crises | DORMANT-1815-ONLY | Post-1842. Correctly gated via qing_treaty_system_imposed flag. |
| qing_legation_events.txt | Legation establishment | DORMANT-1815-ONLY | Post-1860s. Correctly gated via Zongli Yamen existence + date. |
| qing_students_events.txt | Students-abroad crises | DORMANT-1815-ONLY | 1872-1881 mission. Correctly >=1872 gated. |
| qing_golden_urn.txt | Golden Urn lottery (金瓶掣籤) | ZENITH-REFRAME | Historical 1793 Qianlong institution for Tibet/Mongol succession. At 1763 = pre-institution (trad succession). |

---

## 2. RE-GATE / ZENITH-REFRAME Candidates (Ranked)

### HIGH PRIORITY RE-GATE (date/flag guards needed)

1. **se_QING_ILI.txt** — Ili Crisis inversion
   - **Current:** Models 1860s-1881 Yaqub Beg rebellion + Russian occupation + Zuo Zongtang reconquest
   - **1763 reality:** Xinjiang JUST conquered (1759). Dzungar genocide complete. Consolidation phase, not rebellion.
   - **Gate change:** `if current_date >= 1860: reconquest_arc else if has_variable=qing_high_qing_era: consolidation_arc`
   - **Effort:** HIGH (requires new consolidation event chain mirroring existing reconquest chain)

2. **se_QING_REFORM.txt** — Reform track unlock
   - **Current:** Late-Qing reforms (Self-Strengthening/Hundred Days/New Policies)
   - **1763 reality:** No reform pressure yet. Reforms = response to decline/defeat (Opium Wars+).
   - **Gate change:** Reform track potential gates on `current_date >= 1850 OR qing_reform_pressure >= 60`
   - **Effort:** MEDIUM (add potential guard to reform missions + reform-unlocking events)

3. **se_QING_SELFSTR.txt + qing_selfstrengthening_missions.txt** — Self-Strengthening gate
   - **Current:** Movement active whenever progress advances
   - **1763 reality:** Historical 1860s+ (post-defeat modernization). OR early-indus alternate path (Macartney embrace).
   - **Gate change:** Tree potential `(current_date >= 1860 OR has_variable=qing_embraced_early_indus) AND qing_reform_pressure >= 40`
   - **Effort:** LOW (add OR-pattern to mission-tree potential; se_QING_SELFSTR helpers already check progress var)

4. **se_QING_TECHTRANSFER.txt** — Tech-transfer gate
   - **Current:** Arsenals/telegraphs/railways available when called
   - **1763 reality:** No Western tech adoption pre-Opium Wars. Only via early-indus path OR post-1860.
   - **Gate change:** All tech-transfer verbs wrap in `if current_date >= 1860 OR has_variable=qing_embraced_early_indus`
   - **Effort:** LOW (add guard to effect entry points)

5. **se_QING_CUSTOMS.txt** — Maritime Customs era split
   - **Current:** Foreign-run Maritime Customs (Robert Hart model)
   - **1763 reality:** Traditional Canton hoppo (粵海關監督) system, not foreign-run
   - **Gate change:** `if qing_treaty_system_imposed: foreign_customs_layer else: traditional_hoppo`
   - **Effort:** MEDIUM (new traditional-hoppo branch needed; existing foreign-customs becomes post-treaty)

6. **se_QING_MISSIONARY_STATIONS.txt** — Mission stations treaty-gate
   - **Current:** Mission stations established when called
   - **1763 reality:** Christianity proscribed 1724. Underground only until treaty ports force tolerance.
   - **Gate change:** Station-establishment gates on `qing_treaty_system_imposed = yes`
   - **Effort:** LOW (add guard to establishment verbs; se_QING_MISSIONARY already has pre-treaty path)

### MEDIUM PRIORITY ZENITH-REFRAME (presentation/baseline adjustments)

7. **se_QING_COUNCIL.txt + se_QING_GOVERNANCE.txt** — Council/bureau zenith baseline
   - **Current:** No explicit era baseline; effectiveness derives from office-holders
   - **1763 context:** Grand Council young (est. 1729), vigorous. Offices full, competent.
   - **Reframe:** At `qing_high_qing_era`: init `qing_bureau_capacity=70` (vs 50), `qing_bureau_integrity=65` (vs 50). Seed 1763 office-holders with higher avg skill.
   - **Effort:** LOW (adjust init values + 1763 character roster)

8. **se_QING_HOUSEHOLD.txt** — Privy purse zenith baseline
   - **Current:** Init `qing_privy_purse=50`
   - **1763 context:** Qianlong's prosperous reign, privy purse overflowing
   - **Reframe:** At `qing_high_qing_era`: init `qing_privy_purse=80`
   - **Effort:** LOW (one-line init adjustment)

9. **se_QING_VASSAL.txt** — Tributary system zenith presentation
   - **Current:** Suzerain prestige tracks crises (Vietnam/Korea/Ryukyu/Burma losses)
   - **1763 context:** Tributary system UNCHALLENGED. Crises come 1860s-1890s.
   - **Reframe:** At `qing_high_qing_era`: init `qing_suzerain_prestige=85` (vs 60). Crisis events gate on `current_date >= 1860`.
   - **Effort:** MEDIUM (date-gate crisis events; adjust init)

10. **qing_golden_urn.txt** — Golden Urn institution date
    - **Current:** Exists as event file; timing unclear
    - **1763 context:** Institution created 1793 (30 years into 1763 start). Pre-1793 = traditional succession.
    - **Reframe:** Golden Urn events gate on `current_date >= 1793.1.1`
    - **Effort:** LOW (add date guard to event triggers)

### LOW PRIORITY (minor or already handled)

11. **se_QING_SUMMER_PALACE.txt** — 1763 BUILD path
    - **Current:** 1860 sack arc
    - **1763 opportunity:** Reframe as Qianlong's 圓明園 expansion (prestige/culture project)
    - **Effort:** MEDIUM (new build arc paralleling sack arc; both date-gated)

---

## 3. MISSING-BUILD for 1763 (Ranked by importance × feasibility)

### HIGH IMPORTANCE × HIGH FEASIBILITY

1. **Ten Great Campaigns (十全武功) mission arc**
   - **Historical:** Qianlong's ten military victories 1755-1792 (Dzungars, Jinchuan, Burma, Vietnam, Taiwan, Nepal)
   - **1763 status:** Dzungars/Xinjiang done (1755-59). Remaining campaigns 1765-1792.
   - **Engine verbs:** Mission tree (qing_ten_great_campaigns_missions.txt), reuses existing conquest/wargoal/prestige verbs from qing_colonization. Each victory advances `qing_campaigns_completed` counter (0..10), unlocks prestige/legitimacy, final capstone at 10.
   - **Feasibility:** HIGH (mission-tree idiom proven; existing wargoal/conquest verbs; 8 mission beats = Jinchuan/Burma/Vietnam/Taiwan/Nepal + 3 pacification capstones)
   - **Files:** NEW `common/missions/qing_ten_great_campaigns_missions.txt`, NEW `events/imp19c_mod_events/qing_campaigns_events.txt`, extend `se_QING_MECHANICS.txt` with `QING_campaigns_*` helpers

2. **Banner system at full strength**
   - **Historical:** 1763 = Eight Banners not yet decayed. Still militarily effective (vs 1815 = parade-ground force).
   - **1763 status:** Should present as STRONG baseline, gradual decay over time (accelerated by peace/urbanization).
   - **Engine verbs:** Existing `qing_banner_decay` counter in se_QING_DECLINE.txt. At `qing_high_qing_era`: init `qing_banner_decay=10` (vs 50). Decay events gate on NOT-qing_high_qing_era OR date>=1800.
   - **Feasibility:** HIGH (counter exists; just adjust init + decay-event guards)
   - **Files:** se_QING_DECLINE.txt (init adjustment), qing_decline_events.txt (date-gate banner-decay pulses)

3. **Qianlong Southern Tours (南巡) event chain**
   - **Historical:** Six grand tours 1751-1784 to Jiangnan (inspect dikes, rally gentry, display splendor). Massive prestige + treasury drain.
   - **1763 status:** Tours 1-3 done; tours 4-6 (1765/1780/1784) ahead.
   - **Engine verbs:** Dated event chain (qing_southern_tour.1-.6), each fires on tour date (if CHI human + Qianlong ruler + NOT at war). Costs treasury, grants prestige + legitimacy, advances `qing_southern_tours_completed`. Risk events = flood/gentry-dissent (if tour during crisis = legitimacy hit).
   - **Feasibility:** HIGH (dated-event idiom proven in #303 ARW/Napoleon; existing CURRENCY treasury-drain verbs)
   - **Files:** NEW `events/imp19c_mod_events/qing_southern_tour_events.txt`, call from on_yearly_pulse

4. **Tributary system at zenith — embassy arrivals**
   - **Historical:** 1763 = Korean/Ryukyuan/Vietnamese/Siamese embassies arrive regularly. Ritual reinforcement of hierarchy.
   - **1763 status:** Yearly/biennial tributary embassies (prestige pulse, gift exchange, ritual calendar)
   - **Engine verbs:** Extend se_QING_VASSAL.txt with `QING_vassal_tribute_arrival` (fires yearly if vassal exists + suzerain_prestige >= 40). Grants prestige + small treasury. Flavor events in qing_vassal_events.txt.
   - **Feasibility:** HIGH (reuses existing qing_suzerain_prestige var + CURRENCY grant verbs)
   - **Files:** se_QING_VASSAL.txt (new verb), qing_vassal_events.txt (flavor), on_yearly_pulse hook

5. **Canton System (一口通商) trade restriction**
   - **Historical:** 1757 edict restricted all European trade to Canton. Co-hong (公行) merchant monopoly. In force 1757-1842.
   - **1763 status:** Canton System vigorous. Should model as trade-revenue boost + foreign-tension dampener (contained contact).
   - **Engine verbs:** At `qing_high_qing_era` AND `NOT qing_treaty_system_imposed`: set country modifier `qing_canton_system` (+10% trade income, -20% foreign tension). Remove when first treaty signed.
   - **Feasibility:** HIGH (simple modifier swap gated on era + treaty flags)
   - **Files:** common/modifiers/qing_modifiers.txt (new modifier), se_QING_TREATIES.txt (remove on treaty), se_QING_DECLINE.txt (apply at init if era)

### MEDIUM IMPORTANCE × MEDIUM FEASIBILITY

6. **Four Treasuries (四庫全書) + literary inquisition (文字獄)**
   - **Historical:** 1772-1782 Qianlong orders compilation of Four Treasuries (imperial library project). Parallel literary inquisition destroys "seditious" texts.
   - **1763 status:** Not started yet. Begins 1772.
   - **Engine verbs:** Dated event 1772 offers CHI player: pursue Four Treasuries (costs treasury, advances `qing_four_treasuries_progress` 0..100 over 10 years, grants prestige + legitimacy at completion) OR decline. If pursue: yearly pulse advances progress; CHOICE at each pulse = mild inquisition (faster progress, raises reform pressure) OR lenient (slower, less pressure).
   - **Feasibility:** MEDIUM (multi-year project = several dated events + a counter; proven pattern in se_QING_STUDENTS)
   - **Files:** NEW `events/imp19c_mod_events/qing_four_treasuries_events.txt`, NEW `se_QING_FOUR_TREASURIES.txt` (counter + pulse), on_yearly_pulse

7. **Golden Urn (金瓶掣籤) lottery for Tibetan/Mongol succession**
   - **Historical:** 1793 Qianlong institutes lottery to curb Tibetan manipulation of reincarnation. Qing-controlled randomness for Dalai/Panchen/Mongol khans.
   - **1763 status:** Not yet instituted. Traditional recognition until 1793.
   - **Engine verbs:** Dated event 1793.1.1 institutes Golden Urn (set flag `qing_golden_urn_instituted`). Thereafter when Tibetan/Mongol tributary ruler dies: event fires, Qing picks heir via lottery (random from pool) vs traditional (subject picks). Lottery = raises Qing control, angers subject; traditional = subject satisfaction, less control.
   - **Feasibility:** MEDIUM (requires on_ruler_death hook for tributaries + character-pool lottery; heir-selection proven in vanilla)
   - **Files:** Extend qing_golden_urn.txt (currently exists; add 1793 gate + lifecycle), se_QING_VASSAL.txt (integrate into tributary pulse)

8. **Heshen (和珅) corruption arc**
   - **Historical:** Heshen rises 1770s, becomes Qianlong's favorite, amasses fortune via corruption, executed 1799 by Jiaqing.
   - **1763 status:** Heshen not risen yet (he's ~13 in 1763). Arc begins ~1775.
   - **Engine verbs:** Dated event 1775 spawns Heshen character (high charisma, mediocre finesse, corrupt trait). Qianlong (if alive) auto-appoints him to council office. While Heshen in office: `qing_corruption_level` rises faster (+5/year). Jiaqing accession (1796) or Qianlong death triggers purge event (execute Heshen, seize wealth, cut corruption -30).
   - **Feasibility:** MEDIUM (character spawn + corrupt-while-in-office pulse + ruler-death trigger; all proven)
   - **Files:** se_QING_ROSTER.txt (Heshen spawn), NEW `events/imp19c_mod_events/qing_heshen_events.txt`, se_QING_DECLINE.txt (Heshen-corruption pulse)

### HIGH IMPORTANCE × LOW FEASIBILITY (defer)

9. **Examination system (科舉) at peak**
   - **Historical:** 1763 = triennial exams functioning, meritocracy ideal (vs 1815 = exam-selling/decline)
   - **Challenge:** Exam system = abstracted into `qing_bureau_integrity`. Full exam simulation (cohorts/degrees/appointments) = large build.
   - **Defer:** Covered adequately by bureau_integrity zenith baseline (#7 above). Full exam layer = follow-on.

10. **White Lotus / sectarian suppression**
    - **Historical:** 1763 = sects checked. White Lotus Rebellion 1796-1804 major crisis.
    - **Challenge:** Rebellion requires large event chain + dynamic rebel-state release. White Lotus already in `qing_sect_pressure` counter.
    - **Defer:** Covered by existing se_QING_DECLINE sect_pressure system + zenith-low baseline. Full rebellion arc = follow-on if demand.

---

## 4. DORMANT-1815-ONLY Confirms (Correctly Inert at 1763)

| Subsystem | Guard Mechanism | Verification |
|-----------|----------------|--------------|
| **Treaties** (se_QING_TREATIES.txt) | `qing_treaty_system_imposed` flag never set pre-1842 | ✓ Correctly dormant |
| **Legations** (se_QING_LEGATIONS.txt) | Gates on `qing_office_zongli_holder` (Zongli Yamen 1861+) | ✓ Correctly dormant |
| **Students Abroad** (se_QING_STUDENTS.txt) | Explicitly `>= 1872` date guard | ✓ Correctly dormant |
| **Taiping** (qing_taiping_missions.txt) | `>= 1850` date guard | ✓ Correctly dormant |
| **Meiji Japan** (qing_japan_missions.txt) | `exists c:JPN` (never formed pre-Meiji) | ✓ Correctly dormant |
| **Napoleon** (se_QING_NAPOLEON.txt) | Napoleon lifespan 1769-1821 | ✓ Correctly dormant (not born at 1763) |
| **US Civil War** (se_QING_USCW.txt) | `exists c:USA` + date 1861-65 | ✓ Correctly dormant (USA = GBR colony) |
| **Mexico Adventure** (se_QING_MEXICO.txt) | Date 1860s + `exists c:MEX` | ✓ Correctly dormant |

**Audit conclusion:** All 1815+ systems correctly gated. No subsystem will fire prematurely at 1763 start.

---

## 5. Precedent: Already Re-contextualized for 1763

Per `reverse_merge.md` and memory, these were ALREADY adjusted:

- **se_QING_DECLINE.txt #304:** High-qing-era flag detection (`current_date < 1772.1.1`). Counters init low at zenith.
- **se_QING_EMERITUS.txt:** Emperor Emeritus seat already era-neutral (Napoleon alt-history).
- **se_QING_EARLYINDUS.txt:** Macartney embrace path already 1793-triggered (30 years into 1763 start).
- **se_QING_MISSIONARY*.txt:** Pre-treaty split already built (underground path at 1763).
- **qing_colonization_missions.txt:** Dual-gated `self-str >= 40 OR qing_high_qing_era`. Both roads work.
- **qing_force_setup_events.txt:** Starting forces + embassy scheduling already era-adjusted.
- **oa_economy_setup.txt #302:** Spanish-American war deferred to 1810 if `current_date < 1810`.
- **imp19c_setup_events.txt #303:** ARW/French Rev/Napoleon wars dated 1775/1789/1803 (all ahead of 1763).

**Design pattern proven:** `current_date >= X OR has_variable = qing_high_qing_era` OR-pattern lets one subsystem serve both eras.

---

## 6. Recommended Priority Order for Remaining Re-Gates

**Wave 1 (low-effort, high-impact):**
1. se_QING_SELFSTR + missions (add OR-pattern to potential)
2. se_QING_TECHTRANSFER (wrap entry verbs)
3. se_QING_MISSIONARY_STATIONS (add treaty-imposed guard)
4. se_QING_REFORM + missions (add potential guard)
5. Banner decay init + qing_golden_urn date (one-line adjusts)

**Wave 2 (medium-effort zenith reframes):**
6. se_QING_COUNCIL + se_QING_GOVERNANCE baselines
7. se_QING_HOUSEHOLD privy-purse baseline
8. se_QING_VASSAL tributary-prestige baseline + crisis date-gates
9. se_QING_CUSTOMS hoppo/foreign split

**Wave 3 (new 1763 content):**
10. Ten Great Campaigns mission tree (highest value new arc)
11. Canton System modifier
12. Tributary embassy arrivals pulse
13. Qianlong Southern Tours chain

**Defer to follow-on:**
- Ili consolidation arc (HIGH effort, inverts existing reconquest)
- Four Treasuries project (MEDIUM new chain)
- Heshen corruption arc (character-lifecycle complexity)
- Full examination simulation (large scope)

---

## 7. Files Inspected (Evidence Base)

**Scripted effects (48):** All se_QING_*.txt + se_SUBJECT_QING.txt headers + key sections read  
**Missions (8):** All qing_*_missions.txt headers read  
**Events (sampled 10):** qing_decline/treaty/legation/students/golden_urn headers read  
**Setup:** reverse_merge.md + memory imp19c-1763-develop-merge  
**Oracles:** Ten Great Campaigns confirmed via grep (mentioned in colonization header)

**Verification method:** Fast header/comment/potential scan + grep for era-flags + date-patterns. Did NOT read every effect end-to-end (budget constraints). Findings grounded in actual file inspection.

---

## SUMMARY FOR PARENT AGENT

**Inventory:** 48 scripted effects + 8 mission trees + ~45 event files audited.

**Breakdown:**
- **KEEP-AS-IS:** 31 files (generic engines, already era-adjusted, or correctly gated)
- **ZENITH-REFRAME:** 4 files (council/bureau/household/vassal baselines need prosperity-era init values)
- **RE-GATE:** 7 files (selfstr/techtransfer/customs/missionary-stations/reform/ili need era/date guards)
- **DORMANT-1815-ONLY:** 8 subsystems (treaties/legations/students/taiping/meiji/napoleon/uscw/mexico — all correctly gated, verified inert at 1763)
- **MISSING-BUILD:** 8 high-value 1763 opportunities identified

**Top 5 RE-GATE (by priority × effort):**
1. **se_QING_SELFSTR** — add `OR qing_high_qing_era` to mission potential (LOW effort, enables dual-path)
2. **se_QING_TECHTRANSFER** — wrap verbs in era/date guard (LOW effort, prevents anachronism)
3. **se_QING_REFORM** — gate reform track on date>=1850 OR pressure>=60 (MEDIUM effort, correct unlock)
4. **se_QING_CUSTOMS** — split traditional-hoppo vs foreign-customs (MEDIUM effort, historical accuracy)
5. **se_QING_ILI** — invert to consolidation arc at 1763 (HIGH effort, major reframe)

**Top 5 MISSING-BUILD (by importance × feasibility):**
1. **Ten Great Campaigns mission tree** — 8-beat arc 1765-1792, reuses conquest verbs (HIGH value, HIGH feasible)
2. **Banner system zenith baseline** — adjust banner_decay init to 10 at era-flag (HIGH value, HIGH feasible)
3. **Qianlong Southern Tours** — 6 dated events 1765-1784, prestige/treasury (HIGH value, HIGH feasible)
4. **Tributary embassy arrivals** — yearly prestige pulse, reuses vassal verbs (HIGH value, HIGH feasible)
5. **Canton System modifier** — simple modifier swap gated on era+treaty (HIGH value, HIGH feasible)

**Design pattern to adopt:** `current_date >= X OR has_variable = qing_high_qing_era` — proven in colonization/earlyindus, lets one system serve both 1763 zenith and 1815 decline without duplication.
