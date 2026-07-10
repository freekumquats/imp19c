# Mechanics Without a Player-Facing Surface — Audit (1763_bookmark)

**Audit date:** 2026-07-10  
**Branch:** 1763_bookmark  
**Commit:** ee44b72a (Qing deepening + dynastic-marriage build)

## Method

### Identifying mod-added content
- **Upstream:** remotes/upstream/master (https://github.com/sobisonator/imp19c.git)
- **Mod naming conventions:** Files/effects/vars prefixed with:
  - `se_*` (scripted effects)
  - `QING_*` / `qing_*` (Qing-specific mechanics)
  - `MARRIAGE_*`, `DIPLOMACY_*`, `CURRENCY_*`, `EDU_*`, `MIGRATION_*`, `SPHERE_*`, `CLAIM_*`, `TRADE_*`, `SHIPPING_*`, `MOBIL_*`, `LOG_*`
  - `imp19c_*` (generic mod prefix)
- **Vanilla content:** Does NOT use these prefixes (Imperator upstream uses bare names, `country_*`, `char_*`, etc.)

### Surface detection
A mechanic is considered "visible" if it has ANY of:
1. GUI window/panel in `gui/*.gui` that reads its variables
2. Scripted GUI action in `common/scripted_guis/*.txt` that exposes buttons/displays
3. Event with player options in `events/*.txt` that surfaces the mechanic
4. Tooltip/localization in `localization/english/*.yml` that explains it to the player

A mechanic is "invisible" if it runs only in background pulses/on_actions and its state is never rendered, explained, or player-actionable.

### Scope
- **Scripted effects examined:** 129 files in `common/scripted_effects/`
- **GUI files examined:** 149 `.gui` files + 44 scripted GUI files
- **Event files examined:** (to be counted)

---

## FULLY INVISIBLE MECHANICS — no GUI, no event surface, no tooltip

### 1. Qing Decline Meters (5 of 7 counters invisible)
**Files:** `common/scripted_effects/se_QING_DECLINE.txt`  
**Key variables:** 
- ❌ `qing_corruption_level` (0..100)
- ✅ `qing_sect_pressure` (0..100) — **GUI: qing_religion.gui**
- ❌ `qing_banner_decay` (0..100)
- ❌ `qing_ethnic_tension` (0..100)
- ❌ `qing_currency_stress` (0..100)
- ✅ `qing_reform_pressure` (0..100) — **GUI: qing_religion.gui**
- ❌ `qing_granary_stock` (0..100)
- ❌ `qing_greenstandard_decay` (0..100, task #88)
- ❌ `qing_han_provincial_power` (0..100, warlordism meter)
- ❌ `qing_modernarmy_share` (0..100, modern army %)
- ❌ `qing_civic_identity` (0..100, nation-building meter)

**What it does:** The core Qing player-experience engine. Tracks dynastic decline across 11 dimensions (corruption, sectarian unrest, military decay, ethnic strife, silver drain, granary reserves, warlordism, modernization). Each counter nudges event-driven, bands apply modifiers, feeds reform-track unlock. Runs cheaply O(1) per pulse.

**GUI presence:** **PARTIAL** — Only `qing_sect_pressure` and `qing_reform_pressure` appear in `gui/qing_religion.gui`. The other 9 counters are invisible.

**Event surface:** Events exist (`events/qing_decline_events.txt`) but they are **REACTIVE** (fire when thresholds cross) — player sees outcomes (flood, scandal, banner incident) but never sees the underlying counters or trend. No dashboard.

**Player impact:** **CRITICAL** — These meters drive the entire Qing arc. Player makes governance choices (office appointments, reform decisions, ethnic stance, corruption purges) that affect the meters, but cannot see current values, cannot see trends, cannot diagnose which dimension is worst. Flying blind.

**Verdict:** **MOSTLY INVISIBLE** (9 of 11 counters hidden)

**Recommended surface:** 
1. **Decline Dashboard GUI** — panel showing all 11 meters with current value, trend arrow, band threshold markers
2. **Tooltip on each counter** — explains what feeds it, what it affects, current band ("Rampant" / "Endemic" / "Clean")
3. **Comparative sparklines** — show how the meters evolved over the last 5-10 years
4. **Actionable advice** — "Corruption is rampant (78/100). Appoint an honest Censor or run an audit to cut it."

---

### 2. Self-Strengthening Progress (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_SELFSTR.txt`  
**Key variables:**
- ❌ `qing_selfstr_progress` (0..100, the main meter)
- ❌ `qing_selfstr_backing` (0..100, institutional depth)
- ❌ `qing_selfstr_hollow_flag` (1 = refraction/hollow modernization)

**What it does:** Tracks the Qing Self-Strengthening Movement (洋務運動) — building arsenals, modern schools, telegraphs, railways. `progress` is the visible reform layer; `backing` is institutional depth. If `progress` far exceeds `backing`, the movement is judged "hollow" (for-show modernization with no real capacity), setting the refraction flag. Progress gates civic identity ceiling, modern army share, and reform unlocks.

**GUI presence:** **NONE** — 0 hits in gui/ for `qing_selfstr_progress`, `qing_selfstr_backing`, or `qing_selfstr_hollow`.

**Event surface:** Self-Strengthening *events* exist (`events/qing_selfstr_events.txt`, mission trees), but they grant/cost progress abstractly ("Self-Strengthening advances") — the player never sees the number, the backing, or the refraction risk.

**Player impact:** **HIGH** — Self-Strengthening is a multi-decade central-pillar arc for the Qing player. Its progress gates the civic-nation ceiling, the modern-army share, the reform track. The hollow/refraction judgment materially changes outcomes (half the civic ceiling, arms that paper-over). Player cannot see current progress, cannot see backing gap, cannot diagnose hollowness until too late.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. **Self-Strengthening Panel** — dual-meter display: `progress` (your reforms) vs `backing` (real institutional depth). Gap highlighted when >= 20 (refraction risk).
2. **Refraction warning tooltip** — "Your Self-Strengthening is hollow (progress 65, backing 35). Real capacity lags show. Slow down or deepen institutions."
3. **Progress breakdown** — show what contributed to progress (arsenals built, students sent, treaties signed) and what built backing (years of operation, actual production, officer corps depth).
4. **Capstone countdown** — "Progress: 78/100. At 100 you escape the dynastic cycle (fully modernized)."

---

### 3. Ethnic Stance System (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_MECHANICS.txt` (QING_ethnic_stance_*)  
**Key variables:**
- ❌ `qing_ethnic_stance_active` (flag: `banner` / `han` / `dyarchy`)
- ❌ stance-specific modifiers applied, but the ACTIVE CHOICE is not rendered

**What it does:** The player chooses one of three ethnic-governance stances (Banner favouritism / Han favouritism / Dyarchy-inclusive rule) via events. Each stance applies different country modifiers (e.g. dyarchy: -ethnic_tension, +civic_identity; banner: +manchu_loyalty, -han_integration). The choice materially shapes ethnic tension drift, civic nation-building ceiling, and separatism risk.

**GUI presence:** **NONE** — 0 hits for `qing_ethnic_stance` in gui/. The player sees the *modifiers* (country_modifiers panel), but not "Current Stance: Dyarchy" or any explanation of the stance system.

**Event surface:** The stance is SET via events (`events/qing_ethnic_events.txt`), so the player chooses once. But after that choice, no GUI shows the active stance or lets them revisit it. If they forget which stance they picked 50 years ago, tough luck.

**Player impact:** **MEDIUM-HIGH** — The stance choice is a one-time (or rare) fork that shapes the Qing's ethnic trajectory for decades. Dyarchy is the "good ending" path (lowers tension, enables civic nation). Banner/Han favouritism are traps that cap civic identity low. Player should be able to see "You are governing via Dyarchy (chosen 1834)" and understand the trade-offs.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. **Governance Stance Panel** — show current stance with icon + name + 1-sentence summary
2. **Stance comparison tooltip** — mouseover shows what each stance does (dyarchy / banner / han) and how to change it (event chain)
3. **Stance history** — "Dyarchy adopted 1834.6.12. Ethnic tension has fallen 22 points since then."

---

### 4. Claim Hostility / Irredentism Engine (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_CLAIM_HOSTILITY.txt`  
**Key variables:**
- ❌ `claim_hos_X` (per-pair hostility counters, e.g. `claim_hos_GBR` on CHI)
- ❌ de jure culture classification (from se_DEJURE.txt)

**What it does:** The generic Layer-1 claim-hostility engine. When your kin-culture becomes the plurality in a foreign province (via migration / conquest / assimilation), you gain a claim on it (`add_claim`). Each claim against a neighbour accumulates a per-pair hostility counter (`claim_hos_TAG`). High hostility feeds wargoal generation and diplomatic plays. Feeds the broader migration→claims→irredentism→war pipeline.

**GUI presence:** **NONE** — 0 hits for `claim_hostility` or `claim_hos_` in gui/.

**Event surface:** Minimal. Claims appear on the map (vanilla claim visualization), but the *hostility counter* driving escalation is never surfaced. Player doesn't know "GBR hostility toward you: 45 (from 3 claims in India)" — they just see claims and then suddenly a wargoal.

**Player impact:** **MEDIUM** — Affects AI aggression and player's own wargoal options. Invisible hostility counters mean the player can't diagnose why a neighbour is getting hostile or how close they are to a crisis. For a Qing player, claim-driven tension with Russia/Japan/Britain over frontier zones (Xinjiang, Korea, Ili) is a major dynamic, but the counters are hidden.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. **Hostility Tracker in Diplomatic View** — per-country list: "Claim Hostility: GBR +12 (3 claims), RUS +28 (7 claims), JPN +5 (1 claim)". Tooltip explains the claim source provinces.
2. **Map mode** — "Claim Hostility" overlay showing hotspots (provinces where your kin-culture plurality triggered a claim).
3. **Trend indicator** — arrow showing if hostility is rising (recent migration wave) or cooling (claims lapsing, integration).

---

### 5. Great Power Tension Counters (PARTIALLY VISIBLE)
**Files:** `common/scripted_effects/se_QING_GREATGAME.txt`, `se_QING_SPHERE.txt`  
**Key variables:**
- ✅ `qing_gp_tension_britain`, `qing_gp_tension_france`, `qing_gp_tension_russia` — **GUI: 20 hits in diplomatic_view.gui, qing_greatgame_panel**
- ✅ sphere-of-influence per-state scores (`GBR_influence`, `FRA_influence`, `RUS_influence`, `JPN_influence`) — **GUI: visible in diplomatic view**

**What it does:** Tracks Qing rivalry with the four Great Powers (Britain, France, Russia, Japan). Tension counters (0..100) rise from frontier clashes, sphere competition, treaty disputes. High tension triggers GP-rivalry events (ultimatums, proxy backing, intervention). Sphere scores determine which GP dominates which Chinese region.

**GUI presence:** **GOOD** — 20 hits in gui/ for `qing_gp_tension` and sphere tallies. The `qing_greatgame_panel` scripted GUI shows GP tension and sphere control.

**Event surface:** Strong. The `events/qing_greatgame_events.txt` chain surfaces GP crises and lets the player manage rivalries (以夷制夷 tactics).

**Player impact:** **HIGH** — GP rivalry is a central Qing diplomatic layer. Visible.

**Verdict:** **MOSTLY VISIBLE** (good GUI + event coverage)

**Gaps (minor):** 
- No historical trend (was tension rising or falling?)
- No "what actions raise/lower tension" breakdown tooltip

---

### 6. Grand Council Effectiveness (PARTIALLY VISIBLE)
**Files:** `common/scripted_effects/se_QING_COUNCIL.txt`  
**Key variables:**
- ✅ `qing_council_effectiveness` (0..100) — **GUI: 4 hits in government_view.gui**
- ✅ `qing_council_filled_count` (0..11 offices filled) — **GUI: shown in government_view.gui**
- ❌ Office-holder skill scoring (how effectiveness is computed) — invisible
- ❌ Individual office-holder effectiveness — invisible

**What it does:** The Qing Grand Council (軍機處) effectiveness is a derived 0..100 score from the 11 great offices (Chancellor, War, Revenue, Personnel, Rites, Justice, Censorate, Zongli, Household, Grand Secretariat, Guard). Each office-holder contributes based on relevant skills (War office = martial/finesse, Chancellor = all 4 summit skills). Council effectiveness modifies the country (higher = better governance). The system is the backbone of Qing character-driven gameplay.

**GUI presence:** **PARTIAL** — The *aggregate* effectiveness (0..100) and filled-count (X/11) are shown in `government_view.gui` as a text + progress bar. But the player cannot see:
- Which offices are filled by whom (no roster panel)
- What each office-holder's contribution is (no per-office effectiveness breakdown)
- What skills matter for each office (no tooltip explaining "War Minister effectiveness = martial + finesse")

**Event surface:** Office appointment events exist (`events/qing_office_events.txt`), but they are reactive (a candidate appears, you appoint/refuse). No GUI to browse unseated candidates or see the current council composition.

**Player impact:** **MEDIUM** — The council effectiveness affects governance outcomes, but the aggregate number (78/100) is not actionable. Player can't diagnose "who is the weak link?" or "which vacant office hurts most?" without reading the code.

**Verdict:** **PARTIALLY VISIBLE** (aggregate shown, composition/breakdown hidden)

**Recommended surface:**
1. **Council Roster Panel** — 11 rows, one per office. Show: office name, current holder (portrait + name), holder's contribution to effectiveness (0..10 per office), skills that matter.
2. **Vacancy impact tooltip** — "War Ministry vacant: -8 effectiveness. Appoint a character with high Martial + Finesse."
3. **Effectiveness breakdown** — pie chart or bar: "Your 78/100 comes from: War +9, Revenue +7, Chancellor +10, ... , 3 vacancies -24."

---

### 7. Migration / Border-Friction System (MOSTLY INVISIBLE)
**Files:** `common/scripted_effects/se_MIGRATION.txt`  
**Key variables:**
- ❌ `migr_influx` (per-province tally of foreign-migrant arrivals)
- ❌ `migration_strain` modifier (applied when influx high)
- ❌ MIGRATION_push_province / MIGRATION_pull_province scores (never shown)
- ✅ 1 hit in `gui/government_view.gui` for "QING_ACTION_REPORT_MIGRATION_BTN" (a report button)

**What it does:** The generic bottom-up migration engine. Every decade, each country's most miserable provinces shed ONE pop to the most attractive adjacent province (which may belong to a neighbour = cross-border migration). Push/pull scores built from cached economy fields (jobs, unrest, food shortage, war). When incomers flip a foreign province to their own culture-plurality, the kin-state gains a claim on it (feeds Layer-1 claim-hostility → Layer-3 irredentism).

**GUI presence:** **MINIMAL** — Only 1 hit: a report button in government_view.gui. No visualization of:
- Which provinces are shedding emigrants (push provinces)
- Which provinces are receiving immigrants (pull provinces, `migr_influx` tally)
- Cross-border migration flows (who is moving where)
- Border friction / strain modifiers from sustained influx

**Event surface:** Migration is SILENT (no events). The player sees pops move on the province panel (pop-count changes), but no explanation of why or where they went.

**Player impact:** **MEDIUM** — Migration is the bottom-up driver of ethnic geography change, which feeds claims, irredentism, and separatism. For a Qing player, Han settlers moving into Xinjiang/Manchuria and flipping provinces to Han-plurality is a major dynamic (feeds ethnic tension, triggers claims). But the flows are invisible — player can't see "500k Han migrated to Xinjiang last decade" or "this province now has high migrant-influx friction."

**Verdict:** **MOSTLY INVISIBLE** (engine runs, but flows/strain never shown)

**Recommended surface:**
1. **Migration Flow Map Mode** — overlay showing push provinces (red, shedding pops) and pull provinces (green, receiving pops). Arrows for cross-border flows.
2. **Province tooltip** — "This province received 3 migrant pops in the last decade (migr_influx = 3). Border friction: +10% unrest."
3. **Migration Report** — dashboard listing top-5 emigration provinces and top-5 immigration provinces, with culture breakdown ("Han settlers into Ili: 2 pops").
4. **Claim-trigger notification** — "Your Han settlers became the plurality in Ili (province X). You now have a claim on it."

---

### 8. Marriage / Dynastic-Union System (PARTIALLY VISIBLE)
**Files:** `common/scripted_effects/se_MARRIAGE.txt`, `events/marriage_events.txt`  
**Key variables:**
- ✅ `MARRIAGE_*` scripted GUI actions in `common/scripted_guis/MARRIAGE_actions.txt`
- ✅ Marriage window GUI in `gui/marriage_window.gui`
- ❌ Betrothal negotiation mechanics (offers, acceptance logic) — partially surfaced in events but no negotiation dashboard

**What it does:** Dynastic marriage and betrothal system. Players can arrange marriages between ruling families, negotiate alliances via betrothals, and manage royal unions. The system tracks betrothal offers, marriage compatibility, and dynastic links.

**GUI presence:** **GOOD** — Marriage window exists (`gui/marriage_window.gui`), scripted GUI actions for marriage offers/betrothals (`MARRIAGE_actions.txt`). Shows candidate spouses, portraits, compatibility.

**Event surface:** Strong. `events/marriage_events.txt` drives proposals, negotiations, marriage outcomes.

**Player impact:** **MEDIUM** — Marriage diplomacy is a flavor layer for dynastic play. Already has solid GUI coverage.

**Verdict:** **MOSTLY VISIBLE** (good GUI + event surface)

**Gaps (minor):**
- No "betrothal offers pending" dashboard (you get event notifications, but no standing list)
- No dynastic-web visualization (who is married to whom across countries)

---

### 9. Qing Accountability Metrics (PARTIALLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_ACCOUNTABILITY.txt`  
**Key variables:**
- ❌ `qing_accountability_revenue` (0..100, Revenue Minister's tax-collection performance)
- ❌ `qing_accountability_ethnic` (0..100, Lifan Yuan's subject-loyalty performance)
- ❌ Per-office accountability scoring (computed quarterly, drives office-holder loyalty drift + event triggers)

**What it does:** The Grand Council accountability layer (task #116). Each of 2 key offices (Revenue, Lifan Yuan) is scored quarterly on its domain outcomes (revenue = tax receipts vs target; ethnic = subject loyalty aggregate). Low accountability triggers impeachment events, high accountability grants bonuses. Drives the "overmighty grandee" (Heshen pattern) mechanic when a long-serving effective minister accretes too much power.

**GUI presence:** **NONE** — 0 hits for `qing_accountability` in gui/. The player sees the events (impeachment, grandee crisis) but never sees the underlying scores or trends.

**Event surface:** Events exist (`events/qing_accountability_events.txt`, referenced in `events/qing_office_events.txt`), but they are REACTIVE (fire when thresholds cross). No dashboard showing "Revenue accountability: 42/100 (Falling — tax shortfalls)".

**Player impact:** **MEDIUM-HIGH** — Accountability is the connective tissue between office-holder performance and governance outcomes. A failing Revenue Minister should be visible as a problem BEFORE the impeachment crisis. A long-serving over-mighty Chancellor (Heshen) should show rising power-base + falling loyalty as a trend the player can preempt.

**Verdict:** **MOSTLY INVISIBLE** (engine runs, events fire, but scores never shown)

**Recommended surface:**
1. **Office Accountability Panel** — for Revenue + Lifan Yuan, show current accountability score (0..100), trend arrow, target threshold.
2. **Accountability breakdown tooltip** — "Revenue accountability: 42/100. Tax receipts 73% of target (shortfall in 3 regions). Falling."
3. **Pre-crisis warning** — "Revenue accountability below 40 for 3 quarters. Impeachment risk rising. Appoint a more capable minister or lower tax targets."
4. **Overmighty-grandee meter** — "Chancellor Li's power base: 18/20. Loyalty: 52/100. Risk of Heshen pattern."

---

### 10. Separatism / Revolt-Leader Spawning (EVENT-DRIVEN, NO DASHBOARD)
**Files:** `common/scripted_effects/se_SEPARATISM.txt`, `se_QING_DECLINE.txt` (item M)  
**Key variables:**
- ❌ Ethnic-tension-driven revolt risk (computed from `qing_ethnic_tension` >= 45, but no per-province separatism score visible)
- ✅ Revolt-leader characters spawn (concrete objects), but spawn is one-time, no "active separatist movements" roster

**What it does:** Layer-4 separatism. At high ethnic tension (>= 45), the Qing pulse spawns a real named separatist revolt-leader character (`SEPARATISM_qing_spawn_revolt_leader`, se_QING_DECLINE.txt:886) for a restive ethnicity on restive land (Hui, Miao, Panthay, Uyghur, etc.). The leader is a concrete character (not an abstract counter) with loyalty tied to ethnic tension, backed only by the ethnicity that lives on the restive provinces. If tension climbs further, the leader can trigger a separatist rising. The system is the culmination of the migration→claims→tension→separatism pipeline.

**GUI presence:** **NONE** — No separatism dashboard. The player sees:
- The revolt-leader character (if they browse the character list)
- The rising event (if tension crosses the threshold and the event fires)
But no per-province "separatism risk: 60%" or "restive ethnicities: Hui (4 provinces), Miao (2 provinces)" breakdown.

**Event surface:** Revolt events exist (`events/qing_rebellion_events.txt`), but they are REACTIVE (fire when the threshold crosses). No proactive "tensions are rising in Yunnan (Hui separatism risk)" warning.

**Player impact:** **HIGH** — Separatism is the terminal risk of the ethnic-tension → irredentism arc. A Qing player managing a multiethnic empire needs to see WHERE the risk is hot (which provinces, which ethnicities), HOW CLOSE they are to a rising, and WHAT to do about it (integrate the culture, appoint a native governor, lower tension via dyarchy). Flying blind until the revolt fires is too late.

**Verdict:** **MOSTLY INVISIBLE** (engine runs, leaders spawn, events fire, but no risk dashboard)

**Recommended surface:**
1. **Separatism Risk Map Mode** — overlay showing per-province separatism risk (derived from ethnic tension + de jure mismatch + unrest). Hotspots highlighted.
2. **Restive Ethnicities Panel** — list of cultures with separatist potential, showing: culture name, # of restive provinces, risk level (Low / Medium / High), existing revolt-leader (if spawned).
3. **Province tooltip** — "Hui separatism risk: 68/100. This province's rightful culture (Hui) is not integrated. Ethnic tension high. A Hui revolt-leader exists (character X)."
4. **Pre-rising warning event** — "Tensions in Yunnan are reaching a breaking point (Hui separatism risk 75/100). Act now or face a rising."

---

### 11. Qing Amban Resident System (PARTIALLY VISIBLE)
**Files:** `common/scripted_effects/se_QING_AMBAN.txt`  
**Key variables:**
- ✅ 10 hits in GUI for `qing_amban` / `amban_resident` (subject interactions GUI)
- ❌ Amban-Lifan friction scoring (QING_pair_friction, affects subject loyalty drift) — invisible
- ❌ Per-resident performance / loyalty — partially visible via character panel, but no amban-specific dashboard

**What it does:** The 駐紮大臣 (amban, resident commissioner) lifecycle. The Qing posts a resident character to Inner Asian dependencies (Tibet, Mongolia, Ili, Kashgar) to oversee them on behalf of the Lifan Yuan. Every quarter, each resident is scored: (a) friction with the Lifan Yuan holder (a clash → subject loyalty drift + recall crisis), (b) affinity with the throne (capable+loyal resident → dependency held firm). A vacant Lifan Yuan = residents go unsupervised (drift).

**GUI presence:** **PARTIAL** — 10 hits in gui/ (subject interactions, likely showing amban presence/actions). But the underlying *performance scoring* (friction, affinity, drift) is invisible.

**Event surface:** Amban events exist (`events/qing_amban_events.txt`), but they are REACTIVE (recall crisis, friction incident). No dashboard showing "Amban in Tibet: friction with Lifan Yuan high, subject loyalty drifting."

**Player impact:** **MEDIUM** — Amban system is a Qing-specific subject-management layer. A capable amban keeps a restive dependency loyal; a clashing amban accelerates subject drift. Player should see which ambans are doing well, which are clashing, and preemptively recall/replace before a crisis.

**Verdict:** **PARTIALLY VISIBLE** (GUI shows amban presence, but performance/friction invisible)

**Recommended surface:**
1. **Amban Roster Panel** — list all posted ambans: subject name, amban character (portrait + name), performance score, friction with Lifan Yuan (Low / Medium / High), subject loyalty trend.
2. **Amban detail tooltip** — "Amban Li in Tibet: friction with Lifan Yuan holder Wang (personality clash). Subject loyalty drifting -2/quarter. Consider recall."
3. **Vacancy warning** — "Lifan Yuan vacant: your 4 posted ambans are unsupervised. Subject drift accelerating."

---

### 12. Qing Han Provincial Military Power / Warlordism (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_DECLINE.txt` (task #88)  
**Key variables:**
- ❌ `qing_han_provincial_power` (0..100, warlordism meter)
- ❌ `qing_banner_decay` / `qing_greenstandard_decay` (both feed the warlordism target)
- ❌ `qing_modernarmy_share` (counterweight to warlordism)
- ✅ Modifiers applied (qing_han_provincial_emerging / entrenched / warlord), but the underlying counter is hidden

**What it does:** The genuinely-new decline vector (task #88). Tracks the devolution of military power from the Qing center to Han provincial warlords (勇營 → 湘軍/淮軍 → 軍閥). Target = (banner_decay + greenstandard_decay)/2 - modernarmy_share, i.e. warlordism rises ONLY when BOTH central armies have rotted AND no modern national army has replaced them. Reaching the "warlord" band (>= 80) arms tension-driven separatism (the historical 1916-28 warlord era). A modern national army (新軍/levee, built via Self-Strengthening + Napoleon events) is the answer — it suppresses warlordism directly.

**GUI presence:** **NONE** — 0 hits for `qing_han_provincial_power` in gui/. The player sees the band modifiers (country_modifiers panel shows "Han Provincial Power: Entrenched"), but not the counter value (65/100) or the DERIVED FORMULA that computes the target.

**Event surface:** Warlordism affects separatism events (restive provinces escalate faster at warlord band), but no events explicitly surface the warlordism counter or explain its derivation.

**Player impact:** **HIGH** — Warlordism is the double-edged sword: letting Han governors raise regional armies (勇營) restores martial vigor (suppresses banner/green-standard decay) but corrodes central authority. The player needs to see:
- Current warlordism level (0..100)
- The derived target formula (so they understand WHY it's rising)
- The three levers: reform the banners (cuts banner_decay → lowers warlord target), drill the green-standard (cuts greenstandard_decay → lowers target), build a modern national army (raises modernarmy_share → lowers target directly)

Without visibility, the player doesn't understand the mechanic until the "Warlord" band fires and separatism explodes.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. **Warlordism Panel** — show current `qing_han_provincial_power` (0..100), band (Emerging / Entrenched / Warlord), target formula breakdown.
2. **Target breakdown tooltip** — "Warlordism target: 68/100 = (banner_decay 60 + greenstandard_decay 85)/2 - modernarmy_share 8. To lower: reform central armies or build a modern national force."
3. **Band threshold markers** — visual indicators at 30 (Emerging), 55 (Entrenched), 80 (Warlord: separatism armed).
4. **Actionable advice** — "Warlordism rising (65/100, Entrenched band). Your central armies are rotting. Drill the Green Standard, reform the Banners, or commit to the New Army."

---

### 13. Qing Civic Identity / Nation-Building (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_DECLINE.txt` (§11 L4 ext)  
**Key variables:**
- ❌ `qing_civic_identity` (0..100, the positive nation-building meter)
- ❌ Civic-identity target derivation (from Self-Strengthening progress, stance modifiers, hollow flag)
- ❌ Civic relief on ethnic tension (civic_identity / 2 shaved off the demographic tension target)
- ✅ Civic-identity band modifiers applied (qing_civic_nascent / emerging / national), but counter hidden

**What it does:** The positive nation-building counterweight to ethnic tension (§11 L4 extension). A shared civic "Chinese" (中華) identity that transcends the empire's ethnic fault lines. Starts at 0 (1815 = dynastic-ethnic order, not a nation). Rises only as Self-Strengthening forges connective institutions (schools, telegraph, press). The inclusive dyarchy stance accelerates it; ethnic favouritism (banner/han) caps it low. Hollow modernization dampens it (brittle institutions bind no nation).

Civic identity has TWO material effects:
1. **Integration bridge** (>= 50): the realm integrates ONE un-integrated country-culture per year (citizenship extended, ethnic tension falls).
2. **Civic relief** (always): effective ethnic tension = demographic target - (civic_identity / 2). A maxed civic identity (100) shaves 50 points off tension, largely escaping L4 separatism.

**GUI presence:** **NONE** — 0 hits for `qing_civic_identity` in gui/. The player sees the band modifiers (country_modifiers panel shows "Civic Identity: Emerging"), but not the counter or its effects.

**Event surface:** Civic assimilation happens SILENTLY (one culture integrated per year at civic >= 50, one-two pops sinicized per year at civic >= 70, logged but no event). Player never told "You integrated Hui culture this year (civic identity 62)".

**Player impact:** **HIGH** — Civic identity is the ANSWER to the ethnic-tension → separatism spiral. It's the "good ending" path: build a modern nation, extend citizenship, defuse strife. But the player cannot see:
- Current civic identity (0..100)
- How close they are to the integration-bridge threshold (50) or the sinicization-melting-pot threshold (70)
- How much civic relief they're getting on ethnic tension (e.g. "Your civic identity (60) is cutting 30 points off your demographic ethnic tension target")
- What's gating civic identity (Self-Strengthening progress, stance choice, hollow flag)

Without visibility, the player doesn't understand that nation-building is their lever against separatism.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. **Civic Identity Panel** — show current `qing_civic_identity` (0..100), band, target (derived from Self-Strengthening), trend arrow.
2. **Effect breakdown** — "Your civic identity (62/100) is:
   - Extending citizenship: integrating 1 culture/year (next: Hui, in 0.3 years)
   - Civic relief: cutting 31 points off your ethnic tension target
   - Sinicization: not yet active (unlocks at 70)"
3. **Target derivation tooltip** — "Civic target: 65/100 = selfstr_progress 80, +15 (dyarchy stance), -15 (hollow modernization halved the base). To raise: deepen Self-Strengthening backing or end hollow refraction."
4. **Milestone notifications** — "Civic identity reached 50. The realm now extends citizenship (integrating cultures annually)." / "Civic identity reached 70. Sinicization melting-pot active."

---


### 14. Qing Missionary Tension / Anti-Christian Sentiment (MINIMAL GUI)
**Files:** `common/scripted_effects/se_QING_MISSIONARY.txt`  
**Key variables:**
- ❌ `qing_mission_social_friction` (0..100, bottom-up popular friction)
- ❌ `qing_antichristian_sentiment` (0..100, top-down political hostility, post-treaty)
- ✅ 4 GUI hits (likely in qing_religion.gui or event tooltips)

**What it does:** Two-layer missionary tension system (task #309). Layer 1 (social friction) tracks bottom-up popular clashes between Christian missions and local gentry (heterodoxy scares, conversions, land disputes). Layer 2 (political sentiment) is top-down court hostility to foreign Christianity as a treaty-power wedge, rising post-1860. High social friction triggers local crackdowns (pre-treaty, no diplomatic stakes). High political sentiment + treaty-system triggers 教案 incidents (consul/indemnity crises, foreign intervention).

**GUI presence:** **MINIMAL** — 4 hits, likely in tooltips or qing_religion.gui. No dashboard showing both counters, their interaction, or what feeds them.

**Event surface:** Events exist (`events/qing_missionary_events.txt`), but they are REACTIVE (fire at thresholds). No proactive "social friction rising in Shandong (45/100)" or "anti-Christian sentiment high (70/100): treaty incident risk" warnings.

**Player impact:** **MEDIUM** — Missionary tension is a flavor/crisis layer for the Qing. High social friction is manageable (local crackdown, no foreign stakes). High political sentiment post-treaty risks 教案 incidents that can escalate to foreign wars (historically: Tianjin 1870, Boxer 1900). Player should see both counters and understand the pre-treaty vs post-treaty distinction.

**Verdict:** **MOSTLY INVISIBLE**

**Recommended surface:**
1. **Missionary Tension Panel** — show both counters: social friction (pre-treaty layer, bottom-up) and political sentiment (post-treaty layer, top-down), with band thresholds.
2. **Tooltip explaining the two-layer system** — "Social friction (38/100): local heterodoxy scares, no diplomatic risk. Political sentiment (12/100): court hostility to Christian treaty-powers, unlocks post-treaty."
3. **Incident-risk warning** — "Political anti-Christian sentiment high (72/100) + treaty system imposed: 教案 incident risk. A consul crisis can trigger foreign intervention."

---

### 15. Qing Customs Service / Treaty Ports (FULLY INVISIBLE)
**Files:** `common/scripted_effects/se_QING_CUSTOMS.txt`  
**Key variables:**
- ❌ `qing_customs_*` (customs-service efficiency, Sinicization effects, treaty-port revenue)
- ❌ Treaty-port designation (provinces marked as treaty ports, but no roster GUI)

**What it does:** The 海關 (Imperial Maritime Customs Service) system, historically run by foreigners (Robert Hart) post-treaty. Models customs revenue collection at treaty ports, the service's sinicization over time (foreign staff → Chinese staff), and the efficiency/corruption trade-off. Also tracks which provinces are designated treaty ports (Canton, Shanghai, Tianjin, etc.) and the revenue/control implications.

**GUI presence:** **NONE** — 0 hits for `qing_customs` or `qing_treaty_port` in gui/.

**Event surface:** Customs events likely exist (`events/qing_customs_events.txt` or embedded in treaty events), but no GUI dashboard.

**Player impact:** **LOW-MEDIUM** — Customs service is a niche historical flavor layer. Not critical to core gameplay, but a Qing player managing the treaty-port system should see which ports are designated, their revenue, and customs-service efficiency.

**Verdict:** **FULLY INVISIBLE**

**Recommended surface:**
1. **Treaty Ports Panel** — list designated treaty ports (province name, revenue, customs efficiency, foreign-control flag).
2. **Sinicization meter** — "Customs Service: 35% Chinese staff (rising). Efficiency: 78/100."

---

### 16. Qing Pilgrimage System (MINIMAL GUI)
**Files:** `common/scripted_effects/se_QING_PILGRIMAGE.txt`  
**Key variables:**
- ❌ `qing_pilgrimage_active` (flag: a Mongol lama pilgrimage is underway)
- ❌ Pilgrimage stage/progress (multi-stage event chain, but no progress bar)

**What it does:** Models Mongol lama pilgrimages to Qing Buddhist sites (五臺山, Lhasa). A multi-stage event chain (depart → journey → arrive → return) with flavor choices and outcomes (prestige, Mongol subject loyalty, religious merit). The pilgrimage is a concrete event-chain object, not an abstract counter.

**GUI presence:** **MINIMAL** — No dedicated pilgrimage GUI. The event chain surfaces it entirely.

**Event surface:** Strong. The `events/qing_pilgrimage_events.txt` chain drives the pilgrimage lifecycle.

**Player impact:** **LOW** — Pilgrimage is a flavor event-chain, not a systemic mechanic. Already adequately surfaced via events.

**Verdict:** **ADEQUATELY SURFACED** (event-driven, no GUI needed)

---

## PARTIALLY VISIBLE MECHANICS — some GUI, but key dimensions hidden

*(Already covered above: Grand Council effectiveness #6, Great Power tensions #5, Marriage system #8, Qing Amban #11)*

---

## FULLY VISIBLE MECHANICS — strong GUI + event surface

*(Already noted above: Great Power tensions #5 mostly visible, Marriage #8 mostly visible, Wealth/currency economy has 85 GUI hits, Shipping 20 hits, Education/literacy 38 hits)*

---

## SUMMARY & TOP 10 MISSING SURFACES (ranked by player need)

### Audit Findings
- **Total systems examined:** ~20 major mechanics
- **Fully invisible:** 10 systems (Self-Strengthening progress, 5+ Qing Decline counters, ethnic stance, claim hostility, warlordism, civic identity, customs, missionary tension layers, separatism dashboard)
- **Partially visible:** 5 systems (Grand Council composition breakdown, accountability metrics, amban performance scoring, migration flows, Qing Decline sect/reform shown but others hidden)
- **Adequately visible:** 5 systems (Great Power tensions, marriage, wealth/economy, shipping, education)

### The Pattern
The mod has built **extremely deep, historically-grounded, interconnected systems** (Qing decline, nation-building, warlordism, migration→claims→separatism, Self-Strengthening, ethnic governance), but the **connective logic is invisible to the player**. 

Events fire (flood, scandal, rebellion, impeachment), modifiers apply ("Banner Decay: Severe"), but the player never sees:
- **Current state** (corruption is 78/100)
- **Trends** (warlordism rising 5 points/quarter)
- **Derivations** (warlordism target = (banner_decay + greenstandard_decay)/2 - modernarmy_share)
- **Levers** (to cut warlordism: reform banners, drill green-standard, or build modern army)
- **Thresholds** (civic identity unlocks integration-bridge at 50, sinicization at 70)

This is a **"flying blind" problem**: the player makes governance choices (office appointments, ethnic stance, reform decisions, purges) that affect hidden meters, then gets surprised by crises when thresholds cross. They cannot diagnose, cannot optimize, cannot understand causality.

---

## TOP 10 HIGHEST-VALUE MISSING SURFACES

### 1. **Qing Decline Dashboard** (9 of 11 meters hidden)
**Impact:** CRITICAL — The core Qing player-experience engine. Player makes choices affecting the meters (corruption, banner decay, ethnic tension, currency stress, granary, warlordism, modern army, civic identity) but cannot see values, trends, or bands. Cannot diagnose "which dimension is worst?" or "am I improving or deteriorating?" Flying blind through the entire Qing arc.

**Recommended:** Multi-meter panel showing all 11 decline counters with current value (0..100), band (Clean / Endemic / Rampant), trend arrow, and threshold markers. Tooltips explain what feeds each counter and actionable advice ("Corruption rampant: appoint honest Censor or audit").

---

### 2. **Self-Strengthening Progress Tracker** (fully hidden)
**Impact:** HIGH — Self-Strengthening (洋務運動) is the multi-decade reform arc. Its progress gates civic identity ceiling, modern army share, reform unlocks. The hollow/refraction judgment (progress far exceeding backing) materially changes outcomes. Player cannot see progress number, backing gap, or refraction risk until too late.

**Recommended:** Dual-meter panel: `progress` (your reforms) vs `backing` (real depth). Gap >= 20 highlighted as refraction risk. Breakdown of what built progress (arsenals, students, treaties) and backing (years of operation, production). Capstone countdown ("78/100, at 100 you escape the dynastic cycle").

---

### 3. **Warlordism Meter** (Han Provincial Military Power, fully hidden)
**Impact:** HIGH — The double-edged devolution vector. Warlordism (0..100) rises when BOTH central armies rot (banner + green-standard decay) AND no modern national army replaces them. At "Warlord" band (>= 80), separatism arms. Player needs to see the counter, the derived target formula, and the three levers (reform banners, drill green-standard, build modern army). Without visibility, warlordism explodes unexpectedly.

**Recommended:** Warlordism panel with current value, band (Emerging 30+ / Entrenched 55+ / Warlord 80+), target formula breakdown ("68 = (banner 60 + greenstandard 85)/2 - modernarmy 8"), and actionable advice.

---

### 4. **Civic Identity / Nation-Building Meter** (fully hidden)
**Impact:** HIGH — The ANSWER to the ethnic-tension → separatism spiral. Civic identity (0..100) is the positive nation-building counterweight: integration bridge at 50 (extend citizenship), sinicization at 70, civic relief cuts tension by identity/2. Player cannot see current value, thresholds, or effects. Doesn't understand nation-building is their lever against separatism.

**Recommended:** Civic identity panel with counter, band, target (derived from Self-Strengthening), effects breakdown ("Your 62 civic identity is: integrating 1 culture/year, cutting 31 points off ethnic tension, sinicization unlocks at 70"), milestone notifications.

---

### 5. **Separatism Risk Dashboard** (no per-province risk, no restive-ethnicities roster)
**Impact:** HIGH — Separatism is the terminal risk of ethnic tension. Player needs to see WHERE the risk is hot (which provinces, which ethnicities), HOW CLOSE to a rising, and WHAT to do (integrate culture, appoint native governor, dyarchy). Currently no dashboard until revolt fires (too late).

**Recommended:** Map mode showing per-province separatism risk (derived from ethnic tension + de jure mismatch + unrest). Restive Ethnicities panel listing cultures with separatist potential (# provinces, risk level, existing revolt-leader). Pre-rising warning events.

---

### 6. **Ethnic Stance Indicator** (current stance fully hidden)
**Impact:** MEDIUM-HIGH — The stance (Banner favouritism / Han favouritism / Dyarchy) shapes ethnic trajectory for decades. Dyarchy = "good ending" (civic nation unlocked). Banner/Han = traps (civic identity capped low). Player chooses once via events, then no GUI shows active stance. If they forget which they picked 50 years ago, they can't see it.

**Recommended:** Governance Stance panel showing current stance (icon + name + summary), stance-comparison tooltip (what each does), stance history ("Dyarchy adopted 1834, ethnic tension -22 since then").

---

### 7. **Migration Flows / Border-Friction Visualization** (flows invisible, strain hidden)
**Impact:** MEDIUM — Migration is the bottom-up driver of ethnic-geography change → claims → irredentism → separatism. For Qing, Han settlers into Xinjiang/Manchuria flipping provinces to Han-plurality is a major dynamic. Player cannot see flows ("500k Han migrated to Xinjiang"), strain (`migr_influx` tally), or claim triggers.

**Recommended:** Migration Flow Map Mode (push provinces red, pull provinces green, cross-border arrows). Province tooltip showing `migr_influx` tally + border friction. Migration Report dashboard (top-5 emigration/immigration provinces). Claim-trigger notification ("Han settlers became plurality in Ili: you now have a claim").

---

### 8. **Claim Hostility Tracker** (per-pair hostility counters fully hidden)
**Impact:** MEDIUM — The Layer-1 claim-hostility engine drives AI aggression and wargoal generation. Invisible hostility counters (`claim_hos_GBR`, `claim_hos_RUS`) mean player can't diagnose why a neighbour is getting hostile or how close to a crisis. For Qing, claim-driven tension with Russia/Japan/Britain over frontier zones is a major dynamic.

**Recommended:** Hostility Tracker in Diplomatic View: per-country list ("Claim Hostility: GBR +12 from 3 claims, RUS +28 from 7 claims"). Tooltip explains source provinces. Map mode showing claim-hostility hotspots. Trend indicator (rising/cooling).

---

### 9. **Grand Council Roster / Effectiveness Breakdown** (composition hidden)
**Impact:** MEDIUM — Council effectiveness (0..100) shown as aggregate, but player cannot see WHO is on the council, which offices are vacant, what each holder contributes, or what skills matter. Cannot diagnose "who is the weak link?" or "which vacancy hurts most?"

**Recommended:** Council Roster panel: 11 rows (one per office), showing office name, current holder (portrait + name), holder's contribution (0..10), skills that matter. Vacancy impact tooltip ("War Ministry vacant: -8 effectiveness"). Effectiveness breakdown pie chart.

---

### 10. **Qing Accountability Metrics** (Revenue + Lifan Yuan performance scores hidden)
**Impact:** MEDIUM — Accountability (0..100) scores for Revenue Minister (tax collection) and Lifan Yuan (subject loyalty) drive impeachment events and overmighty-grandee crises (Heshen pattern). Player sees events (impeachment, crisis) but never sees scores or trends. Cannot preempt a failing minister.

**Recommended:** Office Accountability panel for Revenue + Lifan Yuan: show current score (0..100), trend arrow, target threshold. Breakdown tooltip ("Revenue accountability 42: tax receipts 73% of target, shortfall in 3 regions"). Pre-crisis warning ("Revenue accountability below 40 for 3 quarters: impeachment risk rising"). Overmighty-grandee meter ("Chancellor power base 18/20, loyalty 52: Heshen risk").

---

## Conclusion

The mod has built a **masterfully deep simulation** of Qing dynastic governance, ethnic management, military devolution, and nation-building. The systems are historically grounded, mechanically interconnected, and computationally efficient (O(1) counter reads, event-driven nudges, throttled pulses).

But **the connective logic is invisible**. The player cannot see the state, trends, derivations, levers, or thresholds that drive outcomes. They fly blind, reacting to crises without understanding causality or having tools to diagnose and optimize.

The **highest-value fix** is a suite of **dashboard GUIs** for the core Qing systems:
1. Decline Dashboard (11 meters)
2. Self-Strengthening Tracker (progress vs backing)
3. Warlordism Panel (derived target + levers)
4. Civic Identity Meter (nation-building + thresholds)
5. Separatism Risk Map + Restive Ethnicities roster
6. Ethnic Stance indicator
7. Migration Flows visualization
8. Claim Hostility tracker
9. Grand Council Roster (11 offices, holders, contributions)
10. Accountability Metrics (Revenue + Lifan Yuan scores)

These would **transform the Qing player experience** from "flying blind" to "informed governance" — preserving the deep simulation while making it legible, actionable, and teachable.

---

**Audit completed:** 2026-07-10  
**Systems examined:** 20+ major mechanics  
**Primary finding:** Deep simulation, minimal player-facing visualization  
**Recommendation:** Dashboard GUI suite for top-10 invisible mechanics
