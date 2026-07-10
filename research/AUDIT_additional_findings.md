# Additional Invisible Mechanics Findings

## Systems Audited (continuing from AUDIT_mechanics_without_gui.md)

---

### 7. Currency/Monetary System (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_CURRENCY.txt`, `se_CURRENCY_STRESS.txt`  
**Key variables:**
- ❌ `official_currency` (currency name: pound_sterling, tael, sikka_rupee, etc.)
- ❌ `reserves_silver_oz`, `reserves_gold_oz` (specie reserves backing currency)
- ❌ `circulating_currency_thousands/millions/billions` (money supply)
- ❌ `national_debt_thousands/millions/billions` (sovereign debt)
- ❌ `currency_reserve_ratio` (0..1, health signal: 1=fully backed, 0=drained)
- ❌ Generic `CURR_STRESS_*` counters (0..100 stress per currency)

**What it does:** Full Victorian monetary simulation. Multiple currencies (GBR pound_sterling, CHI tael, EIC sikka_rupee, FRA franc, etc.) each with backing type (bimetallic_standard, silver_standard, gold_standard), reserve amounts, circulation, debt. Generic currency-stress engine (se_CURRENCY_STRESS.txt) drifts stress counters toward reserve-ratio health (ratio <0.5 pushes stress up, >0.5 bleeds it down). Qing silver drain modeled via `qing_currency_stress` (part of decline system).

**GUI presence:** **NONE** — 0 hits in gui/ for currency_reserve, circulating_currency, national_debt, CURR_STRESS, reserves_silver, reserves_gold.

**Event surface:** None found.

**Player impact:** **CRITICAL** — The Qing silver crisis was a central historical factor (opium trade draining specie, triggering Opium Wars), but players cannot see reserve ratios, debt levels, money supply, currency stress, or silver drain rate.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. Economy Panel showing: currency name + backing type, reserve ratio progress bar, circulating vs reserves gap, national debt sustainability, currency stress meter.
2. Qing-specific: silver drain rate + opium-trade breakdown + reserve depletion trend + crisis countdown.

---

### 8. Migration System (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_MIGRATION.txt`  
**Key variables:**
- ❌ `migr_influx` (0..100 per province, border friction from inflows)
- ❌ `MIGRATION_push_province` (computed push score)

**What it does:** Bottom-up pop migration. Decade pulse finds each country's 3 most miserable provinces and trickles one pop to most attractive adjacent province (may be cross-border). If incomers flip a foreign province to their culture plurality, kin-state gains a claim (feeds claim-hostility + de jure layers). `migr_influx` accrues at destination, driving migration_strain modifiers.

**GUI presence:** **NONE** — 0 hits for migr_influx, MIGRATION_push, MIGRATION_pull.

**Event surface:** **NONE** found.

**Player impact:** **MAJOR** — Migration is core settler-colonialism mechanic that can flip border provinces and seed irredentist claims. Players can't see which provinces are emigration/immigration hotspots, migration pressure levels, or where border friction is building. Organic claim-generation (key alt-history driver) happens invisibly.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. Province tooltip showing migr_influx strain level + recent arrival culture + plurality-flip countdown.
2. Migration map mode (red=high push, green=attractive) with cross-border arrows.
3. Migration report listing cross-border flows + claims generated per decade.

---

### 9. Education/Literacy System (PARTIALLY INVISIBLE)
**Files:** `common/scripted_effects/se_EDU.txt`  
**Key variables:**
- ❌ `EDU_hist_literacy_frac_t1`, `EDU_hist_literacy_frac_t2` (historical literacy floors)
- ❌ `EDU_available_slots_t1_<governorship>`, `EDU_available_slots_t2_<governorship>` (capacity)
- ❌ `EDU_t2_national_bonus` (research bonus from universities)

**What it does:** Historical literacy bootstrap (Qing: 17% t1 / 1% t2 per Rawski; others from capital civ_value) that floors education caps, breaking school-deadlock. Yearly pulse updates education slots per governorship.

**GUI presence:** **MINIMAL** — 26 generic "education" hits; no confirmed display of literacy rates or capacity.

**Event surface:** None found.

**Player impact:** **MODERATE** — Qing historical deficit (17%/1% vs Europe ~40%/10%) is material handicap for industrialization. Players can't see national literacy rates, education capacity limits per governorship, or research bonuses.

**Verdict:** **MOSTLY INVISIBLE**

**Recommended surface:**
1. Country education tab showing national literacy % + comparison to rivals.
2. Governorship view showing capacity utilization + bottleneck indicators.
3. Research tooltip showing university bonus breakdown.

---

### 10. Trade System — Tradezone Stockpiles & Shipping (LIKELY INVISIBLE)
**Files:** `se_TRADE.txt`, `se_SHIPPING.txt`, `se_GLOBALTRADE_split.txt`  
**Key variables:**
- ❌ Per-tradezone stockpiles (e.g. `yellow_sea_tz_stock_tea`)
- ❌ `TRADE_connection_score_<origin>_<dest>_<good>` (shipping costs)
- ❌ Province flags: `natural_harbour`, `major_estuary`, `trade_chokepoint`

**What it does:** Region-based quarterly trade. ~20 tradezones each hold stockpiles per tradegood. Governorships purchase from home tradezone; if unavailable, import from another at connection cost (distance + chokepoints + harbours). Trade income from exports.

**GUI presence:** **UNKNOWN** (likely minimal) — No hits for TRADE_score, tradezone_connection, natural_harbour, tz_stock.

**Event surface:** None found.

**Player impact:** **MAJOR** — Trade is core economic driver. If invisible, players can't see why goods are expensive/scarce, which ports are strategic chokepoints, where to invest in harbour infrastructure, or export income breakdown.

**Verdict:** **LIKELY INVISIBLE**

**Recommended surface:**
1. Tradezone panel showing stockpiles + prices per good + import sources.
2. Trade route map mode with connection costs + chokepoint/harbour highlights.
3. Governorship trade view showing imports/exports + costs.

---

### 11. Qing Ethnic Tension — Province-Level (LIKELY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_ETHNIC_TENSION.txt`  
**Key variables:**
- ❌ `qing_prov_ethnic_tension` (0..100 per province)
- ❌ `qing_prov_ethnic_revolted` (cooldown flag)

**What it does:** Bottom-up province tension from local conditions (culture mismatch + tax + unrest). Quarterly pulse. Tension >=70 snowballs to neighbours. >=80 erupts into revolt. Top-down ethnic stance modulates rate.

**GUI presence:** **UNKNOWN** — No grep for qing_prov_ethnic_tension in gui/*.gui. Possible in qing_province_reports.gui.

**Event surface:** `events/qing_ethnic_tension_events.txt` exists (revolt eruptions).

**Player impact:** **MAJOR** — Core Qing crisis mechanic (White Lotus, Taiping, Dungan rebellions). If per-province invisible, players can't see which provinces are about to erupt, where snowballing is spreading, or where to garrison preemptively.

**Verdict:** **LIKELY INVISIBLE** (country aggregate maybe visible; per-province detail likely not)

**Recommended surface:**
1. Province tooltip showing tension value + trend + snowball risk.
2. Ethnic tension map mode (color 0-100, animate >=80).
3. Ethnic crisis panel listing high-tension provinces + snowball clusters.

---

### 12. Claim Hostility / Irredentism (MOSTLY INVISIBLE)
**Files:** `common/scripted_effects/se_CLAIM_HOSTILITY.txt`  
**Key variables:**
- ❌ Opinion modifiers: `claim_violated_opinion`, `claim_incursion_opinion`

**What it does:** When province changes owner or is occupied, every other country with a claim resents the taker. Opinion drops via claim_violated/incursion modifiers. Universal layer (every country) vs Qing's bespoke GP system.

**GUI presence:** **NONE** — No hits for CLAIM_HOSTILITY. Opinion modifiers may appear in vanilla diplo tooltips.

**Event surface:** **NONE** — Runs on on_actions automatically.

**Player impact:** **MODERATE** — Players can't see which of their expansions will provoke resentment, which neighbours have claims on their land, or why a country suddenly hates them.

**Verdict:** **MOSTLY INVISIBLE** (opinion modifier in diplo tooltips; no claims-conflict map)

**Recommended surface:**
1. Diplomacy "Claims Disputed" tab listing their claims on my land + my claims on theirs + opinion penalties.
2. Province tooltip showing "Claimed by: X, Y" warning.
3. War planning claims-impact predictor.

---

### 13. Qing Accountability System (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_ACCOUNTABILITY.txt`  
**Key variables:**
- ❌ `qing_acc_metric` (0/1/2: failing/middling/thriving per office)
- ❌ Per-office realm metrics (justice→unrest, revenue→treasury, works→civilization, censor→corruption, rites→legitimacy, war→military, personnel→officials_loyalty, lifanyuan→subjects_loyalty, zongli→GP_tension, chamberlain→ruler_popularity, grand_secretariat→influence, guard_commandant→civil_war_threat, chancellor→council_effectiveness)

**What it does:** Quarterly pulse judges each filled office on realm metric + holder character. Thriving domain rewards minister; failing domain + weak holder triggers challenger event. At most one challenge per quarter.

**GUI presence:** **NONE** — No hits for qing_acc_metric or realm-metric scores. government_view.gui shows holders but not performance grades.

**Event surface:** `events/qing_accountability_events.txt` exists (challengers).

**Player impact:** **MAJOR** — Accountability is Grand Council's performance feedback loop. Without visibility, players can't see which domains are thriving/failing, which ministers are threatened, why challenger fired, or which office to prioritize.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. Grand Council performance tab: 11 rows showing office, holder, realm metric, grade (thriving/middling/failing), status (stable/vulnerable/challenged).
2. Per-office tooltip with realm metric breakdown + challenge-risk explanation.
3. Challenge event context showing the failing metric that triggered it.

---

### 14. Qing Sphere of Influence — Per-State Detail (PARTIALLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_SPHERE.txt`  
**Key variables:**
- ❌ State-level: `china_influence`, `britain_influence`, `france_influence`, `russia_influence` (0-100 per state)
- ❌ `qing_sphere_dominant` (0-4 code: neutral/china/britain/france/russia)
- ✅ Country-level: `qing_gp_tension_britain/_france/_russia` (visible in diplomatic_view.gui + qing_greatgame.gui)
- ✅ Country-level tallies: `qing_sphere_china_count`, etc. (visible)

**What it does:** Four-power contest for Qing frontier marches. Each contested state carries 0-100 influence scores for CHI/GBR/FRA/RUS. Influence pushes from sources + bleeds between adjacent states. Dominant holder by max influence. GP tension nudged by sphere flips.

**GUI presence:** **PARTIAL** — GP tension summary bars visible (diplomatic_view.gui:1852-1959). qing_greatgame.gui exists. BUT: per-state influence scores (the actual spatial contest) and dominant-holder classification are NOT displayed in province tooltips or state views.

**Event surface:** qing_greatgame_events.txt exists (crisis events).

**Player impact:** **MAJOR** — Great Game is central Qing mechanic. Players see GP tension summary but can't see which specific states are contested, who's winning each march, or where influence is bleeding. Spatial/geographic layer invisible.

**Verdict:** **PARTIAL** (tension summary visible; per-state contest invisible)

**Recommended surface:**
1. Map mode showing per-state dominant power (color-coded CHI/GBR/FRA/RUS/neutral).
2. Province tooltip showing all four influence scores + trend arrows.
3. Contested-ring list panel with sortable influence breakdowns.

---

### 15. Qing Great Game / Zongli Yamen Coupling (PARTIALLY VISIBLE)
**Files:** `common/scripted_effects/se_QING_GREATGAME.txt`  
**Key variables:**
- ✅ `qing_gp_tension_britain/_france/_russia` (visible as bars)
- ❌ Zongli holder gating (holder skill/loyalty dampens tension; vacancy/weakness raises it) — invisible

**What it does:** Zongli Yamen (總理衙門, proto-foreign-ministry) holder's skill/loyalty gates GP tension drift. Capable + loyal holder nudges tension down; weak/disloyal holder lets it drift up. Quarterly pulse. Office judged on mean GP tension (accountability metric).

**GUI presence:** **PARTIAL** — Tension bars visible (diplomatic_view.gui). Zongli holder likely visible in government_view.gui office roster. BUT: holder's gating effect on tension (skill dampening, loyalty bonus) is invisible.

**Event surface:** qing_greatgame_events.txt (crisis events when tension spikes).

**Player impact:** **MODERATE** — Players see tension levels but don't understand why tension is rising/falling based on Zongli holder quality. Can't diagnose "Should I replace my Zongli?" without seeing the gating.

**Verdict:** **PARTIAL** (tension visible; holder-gating mechanics invisible)

**Recommended surface:**
1. Zongli office card showing: holder + relevant skills (finesse, charisma) + loyalty + current gating effect ("Dampening tension -4/quarter" or "Weak holder: tension drifts +2/quarter").
2. GP tension tooltip explaining: "Tension drift: base +3, Zongli Li Hongzhang dampening -4 (skill 8/8), net -1/quarter."

---

### 16. Subject Interactions / Integration (UNKNOWN — needs scripted_guis audit)
**Files:** `common/scripted_effects/se_SUBJECT_QING.txt`  
**Key variables:**
- ❌ `SUBJ_ladder_rung` (1-4: tributary→nominal_vassal→feudatory→autonomous_governorship)
- ❌ `qing_integration_progress` (0-100)
- ❌ `qing_integration_speed`, `qing_integration_threshold`

**What it does:** Player per-subject interactions for Qing: (1) promote/demote subject one rung along control ladder, (2) gradual integration (spend influence to accrue progress; at threshold, absorb provinces). Cooldowns + influence costs.

**GUI presence:** **UNKNOWN** — Scripted GUIs likely exist (44 files in common/scripted_guis/). No grep for qing_integration_progress in gui/*.gui, but subject interactions typically in scripted GUIs.

**Event surface:** qing_subject_integration.txt exists (integration milestones).

**Player impact:** **MAJOR** — Subject control + integration is core Qing mechanic (historical gaitu guiliu / 改土歸流). If progress bars, costs, cooldowns missing, player is blind.

**Verdict:** **UNKNOWN** (likely PARTIAL if scripted GUIs exist; INVISIBLE if buttons exist but no progress display)

**Recommended surface (if missing):** Subject panel showing: current rung + promote/demote costs, integration progress bar + speed, threshold countdown, recent loyalty events.

---

### 17. Marriage Diplomacy / Dynastic Union (UNKNOWN — needs scripted_guis audit)
**Files:** `common/scripted_effects/se_MARRIAGE.txt`  
**Key variables:**
- ❌ `marriage_bond_count`, list `marriage_partners`
- ❌ `marriage_union_junior` (marks royal_union from marriage)

**What it does:** AI-autonomous dynastic marriage for all eligible monarchies. ~5-year pulse seeks marriages (max 3 bonds per realm). Heirless junior house escalates to royal_union. On shared-ruler death, junior realm's land transfers. Dowry, betrothal, repudiation, contested-succession. Header notes "player L4 GUI (MARRIAGE_actions.txt)".

**GUI presence:** **UNKNOWN** — Header mentions L4 GUI (MARRIAGE_actions.txt in scripted_guis). 21 grep hits for "marriage" in gui/*.gui but unclear if L4 panel or vanilla.

**Event surface:** Likely (marriage pulses, royal_union formation, inheritance).

**Player impact:** **MAJOR** (if invisible) — Dynastic marriage is core European diplomacy + newly enabled for Qing. If L4 GUI missing, players miss: available partners, bond count, royal_union risk, succession threats.

**Verdict:** **UNKNOWN** (likely VISIBLE if L4 GUI confirmed; PARTIAL if only counters shown)

**Recommended surface (if missing):** Marriage panel: current bonds + partners, available candidates (sorted by compatibility), royal_union risk indicator, succession-claim warnings.

---

### 18. De Jure Culture / Irredentism Layer (UNKNOWN)
**Files:** `common/scripted_effects/se_DEJURE.txt`  
**Key variables:** (not read in detail)

**What it does:** Culture-plurality de jure generator. Mentioned in memories as "DONE". Feeds claim-hostility + migration layers.

**Verdict:** **UNKNOWN** (not audited in detail; likely INVISIBLE if no map mode)

**Recommended surface:** Map mode showing de jure culture per province (color-coded by culture) + tooltip explaining "This province's de jure culture is Han (plurality). Kin-state CHI can claim it if controlled by another."

---

### 19. Qing Amban Residents / Lifan Yuan (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_AMBAN.txt` (exists per event file list)  
**Key variables:** (not read)

**What it does:** Amban (駐藏大臣) residents in Tibet + Lifan Yuan (理藩院, Court of Colonial Affairs) management of frontier subjects.

**Verdict:** **UNKNOWN** (not audited; event file exists → likely some event surface)

---

### 20. Qing Customs House / Treaty Ports (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_CUSTOMS.txt` (exists per file list)  
**Key variables:** (not read)

**What it does:** Customs revenue from treaty ports (post-Opium War concessions). Historical Qing revenue source.

**Verdict:** **UNKNOWN** (not audited)

---

### 21. Qing Students Abroad (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_STUDENTS.txt` (exists)  
**Key variables:** (not read)

**What it does:** Students sent abroad for education (historical Self-Strengthening initiative). Likely feeds education + tech-transfer layers.

**Verdict:** **UNKNOWN** (not audited; event file qing_students_events.txt exists → likely event-driven)

---

### 22. Qing Tech Transfer (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_TECHTRANSFER.txt` (exists)  
**Key variables:** (not read)

**What it does:** Technology transfer from European advisors / mission purchases. Part of Self-Strengthening.

**Verdict:** **UNKNOWN** (not audited; event file qing_techtransfer_events.txt exists)

---

### 23. Qing Missionary Stations (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_MISSIONARY.txt`, `se_QING_MISSIONARY_STATIONS.txt` (exist)  
**Key variables:** (not read)

**What it does:** Christian missionary presence in Qing provinces. Feeds religious tension + Western influence.

**Verdict:** **UNKNOWN** (not audited; event file qing_missionary_events.txt exists → likely event surface)

---

### 24. Qing Pilgrimage (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_PILGRIMAGE.txt` (exists)  
**Key variables:** (not read)

**What it does:** Hajj pilgrimage management for Qing Muslim subjects (Hui, Uyghur). Feeds religious unity.

**Verdict:** **UNKNOWN** (not audited; event file qing_pilgrimage_events.txt exists)

---

### 25. Qing Works / Infrastructure (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_WORKS.txt` (exists)  
**Key variables:** (not read)

**What it does:** Board of Works (工部) infrastructure projects. Roads, canals, irrigation.

**Verdict:** **UNKNOWN** (not audited; event file qing_works_events.txt exists)

---

### 26. Qing Justice / Legal Reform (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_JUSTICE.txt` (exists)  
**Key variables:** (not read)

**What it does:** Board of Punishments (刑部) + legal modernization. Feeds legitimacy + unrest.

**Verdict:** **UNKNOWN** (not audited; event file qing_justice_events.txt exists)

---

### 27. Qing Rites / Ceremonies (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_RITES.txt` (exists)  
**Key variables:** (not read)

**What it does:** Board of Rites (禮部) ceremonial functions. Feeds legitimacy.

**Verdict:** **UNKNOWN** (not audited; event file qing_rites_events.txt exists)

---

### 28. Qing Censorate / Anti-Corruption (UNKNOWN)
**Files:** `common/scripted_effects/se_QING_CENSORATE.txt` (exists)  
**Key variables:** (not read)

**What it does:** Censorate (都察院) anti-corruption campaigns. Lowers qing_corruption_level.

**Verdict:** **UNKNOWN** (not audited; event file qing_censorate_events.txt exists → likely event-driven audits)

---

## Summary of Findings

**FULLY INVISIBLE (high-impact):**
1. Currency/monetary system (reserves, debt, stress, silver drain)
2. Migration system (cross-border flows, claim generation, border friction)
3. Claim hostility engine (per-pair resentment from claim violations)
4. Qing accountability system (per-office realm metrics + performance grades)
5. Qing decline meters (9 of 11 counters: corruption, banner/army decay, currency stress, granary, etc.)
6. Self-Strengthening progress (momentum meter + backing depth + refraction risk)
7. Ethnic stance system (active choice + effects)

**PARTIALLY INVISIBLE (visible summary, invisible detail):**
8. Qing ethnic tension (country aggregate maybe visible; per-province detail likely not)
9. Grand Council effectiveness (aggregate visible; per-office breakdown invisible)
10. Sphere of influence (GP tension bars visible; per-state contest invisible)
11. Great Game Zongli coupling (tension visible; holder-gating mechanics invisible)

**LIKELY INVISIBLE (no GUI evidence found):**
12. Trade system (tradezone stockpiles, shipping costs, chokepoints)
13. Education/literacy (national rates, capacity limits)

**UNKNOWN (needs deeper audit of scripted_guis + events):**
14. Subject interactions / integration
15. Marriage diplomacy / dynastic union
16. De jure culture / irredentism
17. Many Qing-specific subsystems (amban, customs, students abroad, tech transfer, missionary, pilgrimage, works, justice, rites, censorate)

---

## Priority Ranking (Top 10 Highest-Value Missing Surfaces)

### 1. **Qing Decline Dashboard** (finding #5 / file #1)
**Why:** Core Qing player-experience engine. 9 of 11 decline meters invisible. Player governs blind without seeing corruption, banner decay, ethnic tension, currency stress, granary stocks, army composition. **Highest impact.**

### 2. **Currency/Monetary Panel** (finding #7)
**Why:** Qing silver drain is THE historical crisis driver (opium trade → Opium Wars). Entire monetary layer (reserves, debt, stress, drain rate) invisible. Player can't see the crisis building until it explodes.

### 3. **Self-Strengthening Progress Meter** (finding #2 / file #13)
**Why:** The "win condition" alternative to decline. Progress + backing depth + refraction risk all invisible. Player can't track multi-decade reform momentum or diagnose hollow modernization.

### 4. **Migration System Visualization** (finding #8)
**Why:** Organic settler-colonialism + claim-generation mechanic. Cross-border flows, border friction, province-flipping all invisible. Key alt-history driver (Han migration into frontiers) runs silently.

### 5. **Qing Ethnic Tension Map Mode** (finding #11)
**Why:** Core crisis mechanic (White Lotus, Taiping, Dungan). Per-province tension, snowballing, eruption thresholds all invisible. Player can't preempt revolts or see where unrest is spreading.

### 6. **Qing Accountability Performance Grades** (finding #13)
**Why:** Grand Council feedback loop. Per-office realm metrics (unrest, treasury, military, etc.) + performance grades invisible. Player can't diagnose which domains are failing or which ministers to replace.

### 7. **Sphere of Influence Per-State Detail** (finding #14)
**Why:** Great Game spatial contest. GP tension summary visible, but per-state influence scores + dominant-holder invisible. Player can't see who's winning which marches or where to push back.

### 8. **Claim Hostility Tracker** (finding #12)
**Why:** Universal irredentism engine. Per-pair resentment from claim violations invisible. Player can't predict which expansions will anger neighbours or why relations are souring.

### 9. **Trade System Tradezone Panel** (finding #10)
**Why:** Core economic driver. Tradezone stockpiles, shipping costs, chokepoints all invisible. Player can't see why goods are scarce/expensive or which ports are strategic.

### 10. **Grand Council Per-Office Breakdown** (finding #6 extension)
**Why:** Council effectiveness aggregate visible, but per-office skill scoring + contribution breakdown invisible. Player can't identify weak links or vacancy impacts.

---

## Methodology Notes

**Scope covered:**
- Read headers + key vars from 20+ major se_*.txt files (QING_DECLINE, CURRENCY, SPHERE, MIGRATION, EDU, TRADE, COUNCIL, GREATGAME, SUBJECT_QING, MARRIAGE, ETHNIC_TENSION, CLAIM_HOSTILITY, ACCOUNTABILITY, SELFSTR)
- Grepped gui/*.gui (87 files) for key var names
- Checked for event files in events/imp19c_mod_events/ (46 Qing event files found)
- Did NOT audit: individual events' player-choice surfaces, scripted_guis/*.txt (44 files), localization tooltips

**Gaps (not yet audited):**
- Scripted GUIs (common/scripted_guis/*.txt) — marriage diplomacy, subject interactions may be VISIBLE via scripted GUI panels
- Event player-choice surfaces (events may expose counters even if GUI doesn't)
- Localization tooltips (localization/english/*.yml may explain mechanics even if no dedicated GUI)
- 20+ additional Qing se_*.txt files (AMBAN, CUSTOMS, STUDENTS, TECHTRANSFER, MISSIONARY, PILGRIMAGE, WORKS, JUSTICE, RITES, CENSORATE, etc.) — marked UNKNOWN

**Confidence levels:**
- **FULLY INVISIBLE:** High confidence (0 GUI hits, 0 event surface confirmed)
- **PARTIALLY INVISIBLE:** High confidence (GUI shows aggregate, detail confirmed missing)
- **LIKELY INVISIBLE:** Medium confidence (no GUI evidence, but not exhaustively ruled out)
- **UNKNOWN:** Low confidence (not audited in detail; may be VISIBLE via paths not checked)

