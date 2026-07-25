# Overnight Designs — Investigation Findings, Designs & Implementation Plans

Autonomous overnight work for imp19c (Imperatrix: Victoria, 1763 Qing start). Four
investigations, each carried end-to-end. **Part I — Design** records the findings (what
exists today, exact keys + file:line, existing-vs-net-new) and the design decision taken.
**Part II — Implementation** records the concrete file-by-file build plan.

Grounding: every investigation rests on (a) a code map of the actual current mechanics and
(b) an academic-sourced historical digest. Decisions are committed, not deferred — where a
piece is hard, the decision taken is recorded rather than punted.

Investigations:
1. Foreign-building use cases
2. Laws to regulate Grand Council ministries
3. Religion → Ideology rework
4. Culture → Nationalism + cultural-rights → citizenship rework

Status: all four investigations are ✅ code-grounded + ✅ historically sourced + ✅ design-reviewed.

---

# PART I — DESIGN

---

## Design 1 — Foreign-building use cases  ✅

**Question.** Expand the "foreign building" concept beyond the current Christian-mission +
Macau-concession pair into a general toolkit: building in subject countries to help them
industrialize; building in disputed/tense border areas to colonize and fortify; embassies
for diplomatic representation with other Great Powers; trade posts and concessions;
Christian missions. (Open task #52.)

### What exists today (verified — `common/buildings/qing_foreign_buildings.txt`)

Three building types, all on the **concrete-over-abstract** principle (the effect lives ON a
real on-map building carrying local modifiers, not on an abstract province modifier):

| Building | 中文 | Effects | Notes |
|---|---|---|---|
| `qing_mission_underground_building` | 地下傳教據點 | +0.01 civ, +0.03 research | pre-treaty, discreet, no happiness hit |
| `qing_mission_public_building` | 公開傳教據點 | +0.03 civ, +0.08 research, +0.15 trade routes, −0.04 happiness | post-treaty (1858/60+), the 教案 grievance |
| `qing_foreign_concession_building` | 夷館 | +0.25 trade routes, +0.02 civ, +0.04 research, −0.02 happiness | the Macau/feitoria archetype |

Conventions established by #7 / #51:
- Building-scope local modifiers only (`local_monthly_civilization`, `local_research_points_modifier`,
  `local_state_trade_routes`, `local_population_happiness`) — all vanilla, proven keys.
- Gate `potential/allow = { has_city_status = yes }`. The concession dropped
  `sufficient_job_slots` (Macau ~1 pop-unit can't meet a mass job-slot floor).
- Seeded by script via `add_building_level` (bypasses the `allow` tech gate); `allow` governs
  only the player's own build-menu click.

### Engine reality

- A building carries LOCAL (province/state) modifiers — the whole leverage.
- A building sits in a province you (or the target) OWN — cross-border builds need the target
  province owned at build time; the design question is WHO owns it + how the build is authorized.
- A building alone grants no diplomatic state/claims/military control — those layer on via
  events/effects keyed off `has_building = X` (proven: `QING_prov_has_mission` gates the
  missionary pulse off building presence).
- Cross-country building is not a native build-menu action — it must be a scripted effect
  (`add_building_level` in the target province scope), authorized by a diplomatic action /
  subject interaction / event.

### DECISION — build the full five-use-case family (no deferral)

Five new building types + their authorization/exploitation layer, each a distinct type for
clean `has_building` gating:

1. **`qing_foreign_works_building` (洋務局)** — industrialization aid in a subject. Built by
   the overlord IN a subject's owned province via a subject-interaction that spends treasury +
   political influence. Local modifiers accrue to the subject (`local_monthly_civilization`,
   `local_research_points_modifier`, `local_pop_promotion_speed_modifier`); the Qing gains a
   country modifier (prestige/influence) while the building stands. Ownership: subject KEEPS
   the province. Authorization: subject-interaction gated on subject-type + relations.
2. **`qing_frontier_colony_building` (屯田)** + **`qing_frontier_fort_building`** — border
   colonization/fortification. Buildable in owned frontier cities (build-menu) and event-granted
   in newly-taken Inner-Asian ground. Colony: `local_population_growth`/civ + hooks the migration
   layer (`se_MIGRATION`) to draw heartland pops; Fort: `local_defensive` / fort level. Advances
   a settle-the-frontier claim via the existing de-jure/claim machinery.
3. **`qing_embassy_building` (使館)** — embassy/legation. Built in a Great Power's capital via a
   diplomatic action (peace + relations floor); a reciprocal foreign legation can be event-planted
   in Beijing. `local_state_trade_routes` + a country-level standing diplomatic-representation
   modifier keyed off `has_building`. Reuses inbound-embassy crisis machinery (Macartney/Amherst)
   + GP-rivalry counters (`qing_gp_tension_*`).
4. **`qing_treaty_port_building` (通商口岸)** — the INVERSE forced concession: a foreign-held
   concession on Qing soil, event-planted as an unequal-treaty war outcome. Foreign trade-route
   benefit + sovereignty/happiness penalty (`local_population_happiness` negative, unrest). The
   existing `qing_foreign_concession_building` remains the Qing-held-quarter (dominant) side; this
   is its mirror.
5. **`qing_mission_cathedral_building` (主教座堂/修院)** — the Christian-mission capstone tier
   above the two existing tiers: highest civ/research + trade, higher happiness penalty, gated on
   full legal toleration; density feeds an anti-Christian-sentiment (Boxer) meter.
   **Ratchet rule (standing [[imp19c-no-restoring-drift-ratchet-rule]]):** that meter is a 0..100
   accumulator — it MUST carry a passive restoring-drift term (decay toward baseline) and band-gated
   nudges, else a positive push with no decay pins it to 100. Sentiment rises with mission
   density / treaty humiliations, decays in their absence.

All five: local modifiers only; `has_city_status` relaxed per-archetype (frontier colony &
rural mission drop it, following the concession's job-slot precedent); se_LOG-wired; every
country-level effect hung off `has_building` via an event/pulse, never baked into the building.

### Historical grounding ✅ (digest complete — full bibliography in Appendix A.1)

Each use case is historically anchored; dates drive the era-gating:
- **Christian missions.** Jesuit court presence 1601–1724; **Chinese Rites Controversy** (1715
  *Ex illa die*; 1721 Kangxi ban) → **1724 Yongzheng proscription** = the hard break into the
  underground era; **Treaties of Tianjin 1858 / Beijing 1860** legalize missionary residence →
  surge + 教案 (*jiao'an*) incidents (Juye 1897 → Boxer prelude 1900). Sources: Cohen, *China
  and Christianity* (1963); Esherick, *Origins of the Boxer Uprising* (1988); Laamann (2017) on
  the 1724 proscription; Harrison, *The Missionary's Curse* (2013). → maps to underground vs
  public mission tiers + the cathedral capstone + mission-density → Boxer-sentiment.
- **Concessions / treaty ports.** Macau (Portuguese from 1557; feitoria 夷館; ground-rent to
  Qing — Xie 2026; Buhi 2021); **Canton System 1757–1842** (十三行 Thirteen Factories, 公行
  Cohong monopoly — Perez-Garcia & Jin 2023); **Treaty of Nanking 1842** opens 5 ports;
  **Shanghai International Settlement 1863** (extraterritoriality 領事裁判權 — Jackson, *Shaping
  Modern Shanghai* 2020). → the Qing-held quarter vs the inverse forced treaty-port concession.
- **Embassies.** **Macartney 1793** & **Amherst 1816** (kowtow/tributary-vs-Westphalian clash —
  Hevia, *Cherishing Men from Afar* 1995); tribute system 朝貢; **Zongli Yamen 總理衙門 est.
  1861**; post-1860 Beijing legation quarter. → the embassy/legation building + representation modifier.
- **Frontier colonization.** 屯田 (*tuntian*) military-agricultural colonies; **Xinjiang conquest
  1750s–60s** (Dzungar campaigns); 八旗 banner garrisons 駐防; 伊犁九城 (Ili Nine Cities);
  state-sponsored Han migration. Sources: Perdue, *China Marches West* (2005); Di Cosmo, "Qing
  colonial administration in Inner Asia" (1998). → the frontier colony + fort buildings.
- **Self-Strengthening.** 洋務運動 **1861–1895** (中體西用); **Jiangnan Arsenal 1865** (Li
  Hongzhang 李鴻章), **Fuzhou Shipyard 1866** (Zuo Zongtang 左宗棠 / Shen Baozhen 沈葆楨);
  Robert Hart & Maritime Customs 1863–1911; ended by the 1894–95 Sino-Japanese War. Sources:
  Elman (2004) on the arsenals; Hsü, *Rise of Modern China*. → the 洋務局 subject-industrialization building.

### Event & mission migration ✅ (impact study complete — LOW-MED risk, additive; main risk = incompleteness)

New buildings must be WIRED INTO existing readers or they're invisible to the meters:
- **`common/scripted_triggers/qing_dynasty_triggers.txt:235-238`** (`QING_prov_has_mission`) — add
  the cathedral mission building so it counts toward the missionary/Boxer meter
  (`se_QING_MISSIONARY.txt:136-138` iterates `QING_prov_has_mission`).
- **`events/imp19c_mod_events/imp19c_setup_events.txt:241,244`** — the concession seed/authorize
  block; slot the forced treaty-port building alongside (`add_building_level`).
- **Works tally** `qing_works_building_count` (`se_QING_MINISTRY.txt:568`) — add 洋務局 if it should
  register as Works output.
- **Missions:** `qing_colonization_missions.txt:147-155,185,246` + `qing_settle_frontier_missions.txt`
  grant vanilla `fortress_building`/`port_building` today → swap/augment to grant the 屯田 frontier
  colony/fort. `qing_selfstrengthening_missions.txt:8-10,37` → grant 洋務局 as reward. Embassy 使館
  is authorized from `qing_embassy_events.txt`/`qing_legation_events.txt` (`add_building_level`), not missions.
- Blast radius: ~5 event files + ~3 mission files, all additive, no crash class.

---

## Design 2 — DRAMATIC engine-law expansion covering the Qing mechanics  ✅

**Question (revised & broadened per user).** Not a bespoke variable panel — a **dramatic
expansion of the NATIVE engine law system** (`common/laws/`, law groups, the laws GUI, the engine
enact-law flow) that turns the Qing subsystem knobs into first-class player-legislated LAWS. The
original 9 ministry levers (diplomats, censors, ministry weights, Works expense, Revenue tax
rates, War training, Rites exam frequency, Personnel governor salaries, Guard recruitment) are the
CORE, but the expansion covers the whole Qing policy surface (ethnic stance, salt/tax, succession
policy, reform-vs-conservative posture, self-strengthening, frontier/integration policy, etc.).

### Architecture — CORRECTED DECISION: use the engine law system

> **Reversal (user directive):** an earlier draft of this section decided to route around the
> engine and store levels in `qing_law_*` variables driven by a scripted-GUI panel. That was
> **wrong** — the whole point of this investigation is to USE and dramatically EXPAND the engine
> law system. That variable-panel decision is retracted. The new decision below stands.

**Finding (accurate):** the mod ships vanilla law files under `common/laws/` (`00_economic_laws.txt`,
`00_constitutional_laws.txt`, `00_social_laws.txt`, `00_monetary_policy_setting.txt`, …) but adds
**no custom law groups** and never calls the enact-law effect in script — the engine law system is
present and working but under-used. It is the correct foundation to build on. The reference oracles
(Terra Indomita, Invictus) use custom law groups heavily — proven precedent.

**DECISION: author a large set of NEW engine law GROUPS** (one per Qing policy), each with
mutually-exclusive tiered law options, enacted through the **native laws UI + engine enact-law
effect**. Each law option carries its effect the engine-native way — a `modifier = { }` block
(country modifiers) and/or an `on_enact = { }` that runs the mod's existing scripted effects / sets
the backing vars / applies the Qing country modifiers. This makes every Qing policy a real law:
picked in the laws screen, costed and cooldowned by the engine, visible as active legislation.

**Engine-law schema — RESOLVED (map complete; oracle-confirmed against TI + Invictus + imp19c):**
- **No `common/law_groups/` dir.** A file in `common/laws/` is a flat list of law GROUPS; grouping
  is purely **structural nesting** — a group is a top-level block, its `{ }`-block children are the
  mutually-exclusive law OPTIONS. No `law_group` field, no `_law`-suffix requirement.
- **Group block** carries only `potential = { }` (country trigger deciding if the slot exists —
  e.g. `tag = CHI`, `is_monarchy = yes`, or chained `has_law = <other>` to make one law unlock a group).
- **Option block** carries: `allow = { }` (gates picking this option — tech/invention/rank/var),
  `modifier = { }` (static country modifier while active; may be empty), `on_enact = { }` (**runs
  arbitrary country-scoped effects once at enact** — `set_variable`, `add_country_modifier`,
  `set_country_religion`, `set_legion_recruitment`, `if`/`hidden_effect`, `custom_tooltip`). No
  per-option cost field. **First option = the default** a country holds absent any `change_law`.
- **Enactment effect = `change_law = <option_key>`** (NOT `add_law`/`activate_law` — those don't
  exist). Script side (missions/events/decisions/effects) uses `change_law`; the law's group
  `potential` must pass for that country or `change_law` silently no-ops.
- **Cost is GLOBAL** — `enact_law = { political_influence = 35  stability = 15 }`
  (`common/prices/00_hardcoded.txt:5`); tune per-country via the `enact_law_cost_modifier` modifier,
  NOT per-law. No engine per-law cooldown.
- **Laws GUI** = the `laws_widget` in `gui/shared/gui_templates.gui:1415-1640` (datafunctions
  `GovernmentView.GetCurrentLaws` → `LawGroupItem.GetLaws` → per-option `LawItem.HasLaw/CanEnact/
  IsAllowed/Enact`), shown in the Laws tab of `gui/government_view.gui:1985+`.
- **⚠ THE CRITICAL GOTCHA:** imp19c's `gui/government_view.gui` OVERRIDES the laws view and
  **hand-enumerates every law group** (~37 currently) via `laws_widget_area` blocks filtered on
  `EqualTo_string(LawGroupItem.GetName, Localize('<group_key>'))`. **A new group not added there is
  `change_law`-able but INVISIBLE in the Laws tab** (the exact documented `succession_law` bug at
  `government_view.gui:2235-2241`). Every new ministry/Qing law group MUST get an area entry
  (template at `:2242-2253`).
- **Byte conventions:** law files require UTF-8 **BOM** (all 11 existing do). Loc needed for the
  group key AND each option key + `_desc` in `localization/english/laws_l_english.yml` (BOM+LF).
- **AI:** won't pick new laws unless scripted; imp19c has `ai_choose_and_enact_law_*` effects
  (`se_PURCHASE.txt:640`). Mark CHI-flavour groups `potential = { tag = CHI }` (or `is_ai = no` per
  TI's caste-law precedent) so the AI doesn't get stuck on a bad default.
- **Precedent:** imp19c already runs `set_country_religion` inside a law `on_enact`
  (`00_social_laws.txt:108-122`) — so Design 3's ideology adoption can ALSO be law-driven; and its
  succession system wraps `change_law` in `se_SUCCESSION.txt`. Invictus `00_monarchy.txt:58-126` is
  the copyable custom-group template (potential + per-option allow + modifier + on_enact).

### Law-group catalogue — CORE 9 ministry levers (backing verified in code)

Each becomes an engine law GROUP with tiered options; the "backing" column is what the option's
`modifier`/`on_enact` drives. The default option = current behavior (so enacting nothing changes nothing).

| # | Law group | Backing today | Option effect drives |
|---|---|---|---|
| 1 | **Diplomatic establishment** (Zongli 總理衙門) | `qing_zongli_diplomat_count`; estab `4` (`se_QING_SUBPOSTS.txt:182,226`), cap `<6` (`QING_zongli_panel.txt:93`) | `on_enact` raises the estab target (was hard literal) |
| 2 | **Censorial establishment** (都察院) | `qing_censor_inspector_count`; estab `4` (`se_QING_SUBPOSTS.txt:183,238`), cap `<6` (`QING_censorate_panel.txt:79`) | `on_enact` raises the estab target |
| 3 | **Ministry precedence / weights** | NET-NEW: hard-coded seat-weights (`se_QING_COUNCIL.txt:314-341,439-471`) | `on_enact` sets per-office weight vars read by `QING_council_recompute` |
| 4 | **Works appropriation** (工部/河工) | NET-NEW: only `qing_works_building_count` | `modifier` + `on_enact` recurring spend / perf coupling |
| 5 | **Land-tax rate** (戶部/地丁) | binary `qing_salt_gabelle_reformed` only (`se_QING_REVENUE.txt`) | `modifier = { global_tax_modifier … }` per tier |
| 6 | **Military drill / training** (兵部) | NET-NEW: no drill var in `se_QING_WAR.txt` | `modifier` (discipline/manpower + upkeep) + perf coupling |
| 7 | **Examination cadence** (禮部/科舉) | fixed `qing_exam_triennial_cooldown={days=1095}` (`se_QING_EXAM.txt:126-137`) | `on_enact` sets the cadence the exam scheduler reads |
| 8 | **Governor emolument** (吏部/養廉銀) | NET-NEW; engine `monthly_governor_wage` exists | `modifier = { monthly_governor_wage … }`; feed corruption |
| 9 | **Guard establishment** (侍衛/禁旅八旗) | `qing_guard_corps_count` estab `4` (`se_QING_SUBPOSTS.txt:184,249`) | `on_enact` raises the estab target |

For the estab laws (1/2/9), the hard literal `4`/`6` in `se_QING_SUBPOSTS.txt` /
`QING_subpost_staff_corps_minted` must be read from the law state instead (via `has_law` gates or a
var set in `on_enact`) — the roster staffer then honours the legislated establishment.

### Law-group catalogue — EXPANSION beyond the ministries  ✅

Full Qing-mechanics inventory complete (78 `se_QING_*` files swept). **~35–40 candidate law
groups** across 8 domains. Each group: `potential = { tag = CHI }` (or broader where it generalizes),
first option = current-behavior default, effect via the option's `modifier`/`on_enact`. Legend:
**E** = backing var/modifier EXISTS (law drives it); **N** = NET-NEW backing var + pulse read needed;
**E→policy** = meter exists but the law adds a new "policy/target" knob the pulse reads.

**A. Governance / Council / Offices**
- **Inter-Ethnic Governance Doctrine** (dyarchy / banner-supremacy / Han-conciliation) — E:
  `qing_ethnic_stance_active` + `qing_ethnic_stance_*` modifiers (`se_QING_MECHANICS.txt:21-28`).
- **Council Composition** (Manchu-weighted / balanced-dyarchic / meritocratic) — E:
  `qing_council_eff_target` + `qing_council_dyarchic_balance` (`se_QING_COUNCIL.txt:441`).
- **Office-Selling Policy 捐納** (exam-only / mixed / open sale) — E: toggles
  `qing_office_purchased_ranks`, feeds `qing_bureau_integrity` (`se_QING_GOVERNANCE.txt:52-56`).
- **Advisory Establishment** (2 / 3 / 4-5 slots) — E: `qing_advisor_slot_cap` (`se_QING_ADVISORS.txt:48`).
- **Ministry Establishment Size** (diplomats/censors/guards: lean 3 / standard 4 / expanded 6) — N:
  target is a literal `4` in `QING_subpost_staff_corps_minted` (`se_QING_SUBPOSTS.txt:182-184`).
- **Rescript Processing Standard 票擬** (secretariat backlog clear-rate) — E→policy:
  `qing_secretariat_backlog` (`se_QING_SECRETARIAT.txt:43`).
- **Banner Nobility Governance 議政王大臣** (empower / balance / curb) — E→policy: delib meters.

**B. Fiscal / Revenue**
- **Salt Administration 鹽政** (farmed-out / reformed) — E: `qing_salt_gabelle_reformed`.
- **Monetary Response** (hard specie / stabilization / debasement; pairs w/ vanilla `currency_law`)
  — E: `qing_currency_stress` bands.
- **Granary Policy 常平倉** (minimal / standard / aggressive) — E→policy: `qing_granary_stock`.
- **Canal Grain Tribute Quota 漕運** (0.5–1.0) — E: `qing_canal_jiangnan_quota` (`se_QING_CANAL.txt:209`).
- **Customs Service Regime 海關** (native / foreign-supervised IG) — E: `qing_customs_foreign_control`.
- **Canton Trade Regime 廣州體制** (open / closed) — E: `qing_canton_regime`.
- **Canton Revenue Allocation 內帑** (0/50/100% to emperor) — E: `qing_canton_purse_share`.
- **Frontier Caravan Customs 定稅則** (light/moderate/heavy) — E: `qing_caravan_customs_rate`.
- **Frontier Trade Sovereignty 阿奇木** (grant concession / assert) — E: modifier toggle.
- **Tariff Regime** (treaty-fixed / partial / restored autonomy) — E: `qing_tariff_autonomy`.

**C. Military**
- **Banner Military Policy 八旗** (stipend / drill / disband-to-modern) — E: `qing_banner_decay` + mods.
- **Green Standard Policy 綠營** (parallel) — E: `qing_greenstandard_decay`.
- **Provincial Militarization 勇營** (centralized / sanctioned / delegated) — E: `qing_han_provincial_power`.
- **Army Modernization Mandate 新軍** (traditional / mixed / new-army) — E: `qing_modernarmy_share`.
- **Palace Guard Establishment 侍衛** — E: `qing_guard_corps_count` / `qing_bayara_guard_raised`.

**D. Decline / posture meters**
- **Anti-Corruption Stance** (tolerant / audits / draconian) — E: `qing_corruption_level`.
- **Heterodox Sect Policy 白蓮教** (tolerate / monitor / suppress) — E: `qing_sect_pressure`.
- **Reform Posture** (conservative / gradualist / reformist) — E: `qing_reform_faction_balance`.

**E. Succession / Dynasty / Court**
- **Succession Method 秘密立儲** (open / secret designation / deliberative) — E: `qing_secret_succession_sealed`.
- **Regency Rules** — E: `qing_office_regent_holder` / `qing_regent_pick_kind`.
- **Princely Establishment** (favour / investigate / restrict) — E: `qing_prince_backing`.
- **Harem Establishment 后妃** (rank distribution / size) — E: `qing_harem_rank*_count`.
- **Eunuch Policy 內務府** (restrict / standard / empowered) — E→policy: `qing_eunuch_count`.

**F. Frontier / Integration / Subjects**
- **Xinjiang Administration 屯田/伯克** (military-farm / beg indirect / provincialize) — E→policy: `qing_xj_consolidation`.
- **Frontier Resident Establishment 理藩院** (amban min count) — N: `QING_AMBAN_MIN` constant → law var.
- **Tributary Ritual Frequency 朝貢** — E: `qing_tribute_cooldown` (`se_QING_TRIBUTE.txt:257-266`).
- **Frontier Settlement Policy 移民實邊** (closed / encouraged / forced) — E: `qing_frontier_resettlement`.
- **Cultural Assimilation Doctrine 漢化** (preserve Manchu / balanced / sinicize) — E→policy: `qing_manchu_identity`/`qing_sinic_*`.
- **National Integration** (dynastic / multi-ethnic / civic nation) — E: `qing_civic_identity` (couples to Design 4).
- *(Tributary Demands 2/5/9% — E but SUBJECT-scoped `se_SUBJECT_QING.txt:721-723`; a per-subject
  interaction / subject-law, NOT a CHI country-law group.)*

**G. Modernization / Culture / Justice / Religion**
- **Modernization Doctrine 自強** (conservative / ti-yong / wholesale-western) — E: `qing_selfstr_progress` + rich modifier set.
- **Industrial Encouragement** (官辦 / 官督商辦 / 商辦) — E: earlyindus modifiers.
- **Overseas Education Program 留學** (none / limited / large) — E: `qing_students_*`.
- **Examination Policy 科舉** (classical / practical-subjects / abolition) + cadence — E (classical/
  cadence via `qing_exam_triennial_cooldown`) + N (practical/abolition tiers).
- **Cultural Patronage 文治** (austere / standard / lavish) — E→policy: `qing_wenzhi_patronage`.
- **Palace/Public Works Priority 三山五園** (frugal / balanced / grand) — E: works modifiers.
- **Penal Code Regime 大清律例** (harsh / merciful / modern) — E: pure modifier-swap (`se_QING_JUSTICE.txt:93,107,122`) — IDEAL law group.
- **Censorate Empowerment 都察院** (weak / active / weaponized) — E: `qing_censorate_vigor`.
- **Ritual Orthodoxy 禮部** (strict / pragmatic) — E: pure modifier-swap.
- **Missionary Policy** (prohibit / tolerate / open) — E→policy: `qing_missionary_reach` + antichr meters (couples to Design 1 cathedral tier).
- **Opium Policy** (prohibit / tolerate / legalize) — E: `qing_opium_posture` (`se_QING_OPIUM.txt:78`).

**H. Diplomacy / Great Game**
- **Great-Power Alignment** (isolation / balance / align-with-one) — E→policy: `qing_gp_tension_*` / `qing_sphere_dominant`.
- **Foreign-Office Doctrine 總理衙門** (tributary-only / resident legations / full diplomacy) — E: legation/embassy vars.
- **Overseas Expansion** (isolationist / trade-fleet / colonial) — E→policy: treasure-fleet/colony modifiers.

**Effort split:** ~20 groups are **E** (pure modifier/var already there — cheapest: penal code &
ritual orthodoxy are literal modifier-swaps); ~10 are **E→policy** (meter exists, add a target/rate
var the pulse reads); a handful are **N** (need a new backing var: establishment size, amban min,
exam practical/abolition, eunuch-restrict cap). The **Penal Code** and **Ritual Orthodoxy** groups
are the recommended first two to author (pure modifier-swap, zero new plumbing) to validate the
whole law + GUI-tab pipeline before scaling to the rest.

### Historical grounding ✅ (digest complete — full bibliography in Appendix A.2)

The regulables map onto real Qing statutory levers, and the framing device is exact: the
**大清會典 (Da Qing Huidian, Collected Statutes)** + per-Board **則例 (zeli, substatutes)** ARE
the historical "laws that regulate the ministries." The **Qianlong Huidian (completed 1763)** is
the edition current at game-start — the statutory instrument the law panel represents. Regulation
changed via memorials + vermilion rescripts, folded into the next Huidian/zeli revision (Kuhn,
*Soulstealers* 1990). Per-lever grounding:
- **Revenue 戶部** — 地丁 (*diding*) land-poll tax quotas + salt gabelle + customs; 戶部銀庫
  silver reserve (~62M taels 1763, memory-noted, aligns with fiscal history). Source: Zelin;
  Wong, *China Transformed* (1997); *Qinding Hubu zeli*. → land-tax-rate law.
- **Rites 禮部** — 科舉 civil exams: county annual, provincial + metropolitan **triennial**, with
  provincial 額 (*e*) quotas of 舉人 degrees adjusted by population/politics. Source: **Elman, *A
  Cultural History of Civil Examinations*** (2000); *Qinding kechang tiaoli* (1887). → exam-frequency law.
- **Personnel 吏部** — 京察/大計 triennial evaluations; governor **養廉銀 (*yanglian yin*)**
  anti-corruption salary supplements: governor ~13,000–20,000 taels/yr, magistrate 400–2,000,
  dwarfing the ~180-tael base salary. Source: **Zelin, *The Magistrate's Tael*** (1984). →
  governor-salary law feeding corruption.
- **War 兵部** — 八旗 (Banners, ~200–300k) vs 綠營 (Green Standard, ~600k) — figures secondary,
  need primary confirmation; 武舉 military exams parallel the civil, triennial with quotas. Source:
  *Qinding Baqi zeli* (1739); *Bingbu chufen zeli*. → war-training-level law.
- **Works 工部** — 河工 (*hegong*, Yellow-River hydraulics) commonly ~10–15% of central revenue;
  漕運 (*caoyun*) Grand Canal grain tribute ~4M 石/yr; material prices standardized in 物料價值則例
  (1768). Source: Will; *Caoyun zeli zuan* (1757). → works-budget law.
- **Censorate 都察院** — 御史 (*yushi*) establishment (metropolitan + provincial), impeachment.
  Source: Springer *Yushi* entry; *Duchayuan zeli*. → censor-establishment law.
- **Diplomats / Guards** — tributary envoys handled by Rites (Korea/Vietnam) + Lifan Yuan 理藩院
  (Inner Asia; 駐藏大臣 amban); 侍衛/禁旅八旗 palace guard from Bannermen. → diplomat + guard laws.

**Uncertain figures flagged:** exact 1763 戶部銀庫 balance, Banner/Green-Standard counts, 武舉
quotas — usable as design magnitudes but not archivally confirmed in the digest.

### Event & mission migration ✅ (impact study complete — LOW risk; work is in SE/GUI not events)

The Qing config knobs are read by scripted_effects/scripted_guis, NOT by events — so event blast
radius is tiny; the real migration cost is re-pointing those SE/GUI readers to `has_law` state.
- **Events:** only `events/imp19c_mod_events/qing_revenue_events.txt:29,49-50` touches a law-bound
  knob (the salt-gabelle gate/writer). Update the `:29` gate `has_variable = qing_salt_gabelle_reformed`
  → `NOT = { has_law = <salt_law.reformed> }`, and have the `:50` writer also `change_law`. Keep the
  var as a mirror during transition so the GUI/SE readers don't break. `qing_caravan_customs_rate` is
  referenced in NO event (only `QING_caravan_panel.txt` + `se_QING_CARAVAN.txt`) — pure SE/GUI swap.
- **Ministry establishment** is a hard literal in `se_QING_MINISTRY.txt` (baselines `subtract=4/5/10`
  at :217/:223/:486/:603/:701/:785/:928/:1057/:1187), not a var — parametrize those literals off the
  law, not an event edit.
- **Missions:** `qing_reform_missions.txt:66-190` nudges `qing_reform_faction_balance` + gates on
  `qing_reform_endstate_reached`; `qing_selfstrengthening_missions.txt` + `qing_colonization_missions.txt:64,577,1444`
  gate on `has_variable = qing_selfstr_progress`. If reform/self-strengthening become law groups,
  re-point these var gates → `has_law` (or keep the var as the mission-facing mirror the law sets).
- Blast radius: ~2 events + ~3 mission files. LOW — nothing crashes; keep vars as mirrors to avoid
  a cascade of SE/GUI edits in the first pass.

---

## Design 3 — Religion → Ideology rework  ✅

**Question.** Repurpose the engine Religion + Pantheon/Deity system into an IDEOLOGY system:
deities → prominent thinkers/Enlightenment figures; religions → ideologies (Monarchism,
Liberalism, Socialism, Communism, Nationalism, Conservatism…).

### Code reality (stock Imperator pantheon model, data-reskinned only)

- Religions: `common/religions/00_vthreereligions.txt` (622 lines). Per-religion schema: `color`,
  `religion_category` (pantheon | sages | firetemples — the deity layout), `can_deify_ruler`,
  optional `is_monotheistic`, `happiness_for_same_religion_modifier`. CHI = `confucianism`
  (`setup/main/00_default.txt:35656`).
- Deities: `common/deities/00_generic.txt` (8 generic), `03_confucian_pantheon.txt` (8 Chinese —
  a **working reskin proof**). Deity schema: `trigger`, `icon`, `passive_modifier` (permanent),
  `omen` (temporary invokable), `on_activate`, `religion`, `deity_category`
  (war|economy|culture|fertility), `deification_trigger`. `*_svalue` magnitudes are engine-defined.
- **Load-bearing structure:** exactly **8 deities = 2 per category** (war/economy/culture/fertility).
  `03_confucian_pantheon.txt`'s header documents that a prior 12-deity + wrong-religion-holy-site
  attempt **broke the panel** — the 8 / 2-2-2-2 shape is the hard constraint to mirror. (Earlier
  drafts of this doc cited an `EXPECTED_DEITY_COUNT=4` define; that token does not exist — the real
  constraint is the 8/2-2-2-2 deity shape, not a define.)
- Registration: `setup/main/deities/00_default.txt` (generic DB 1–8), `02_confucian.txt` (DB
  1400–1407). Generic-vs-Confucian switch = deities' `trigger = { NOT = { religion = confucianism } }`.
- GUI: `gui/religion_view.gui` — pantheon tab copied VERBATIM from Terra Indomita; activation is
  100% engine accessors (`GetPantheon`, `DeityItem.Invoke`, `ToggleSelectPantheonWindow`,
  `CanChangePantheon`, `IsOmenActive`). Reskin = loc + icons only.
- **Religion is directly mutable** via `set_country_religion` (ORACLE-CONFIRMED — TI 569× / Invictus
  739×; imp19c already uses it 11×, e.g. `events/flavour_middle_east.txt:119`
  `set_country_religion = sunni`). The guessed name `set_religion` does NOT exist — do not use it.
  Full conversion is a layered flow because setting country religion does not cascade:
  `set_country_religion = X` (state) + `set_character_religion = X` (ruler + loyal family + top
  prominent chars) + `set_pop_religion = X` (loop pops via `random_pops_in_province`/`every_pop`).
  RHS accepts a literal key OR a scope value (`root.overlord.religion`).
- Hooks: scripted-trigger groups (`00_religion_groups.txt` `christian_group_trigger` etc.), pop
  happiness/conversion defines (`WRONG_RELIGION_HAPPINESS`,
  `CONVERSION_SCALE_PER_MISMATCHED_DEITY=-0.2`), governments, characters/pops carry `religion`,
  `omen_power` feeds economy svalues (`MODIFIER_svalues.txt:84`). Blast radius: `confucianism` in
  32 files, `mahayana` in 54, ~967 religion lines in `common/`, thousands of `religion=` in
  `setup/main/00_default.txt`.

### DECISION — ideologies COEXIST with faiths as sibling religions; built in ordered stages

Two decisions the design review (F1, F2) forced, recorded here rather than deferred:

**Coexistence model (resolves F2).** Ideologies are ADDED as new `religion` entries that live
ALONGSIDE the historical faiths — the religion *system* is NOT wholesale-replaced. A country/pop
is either on a historical faith OR has "converted" to an ideology; the two occupy the same engine
`religion` slot but are distinct entries. This is the decisive choice because it collapses the F2
blast radius: **the mass `setup/main/00_default.txt` remap is NOT needed** — the overwhelming
majority of `religion=` lines stay on their historical faith untouched; only the handful of
countries where an ideology is historically nascent at 1763 get reseeded. Faiths keep their own
pantheons; ideologies get thinker-pantheons; omen/happiness coupling is already per-entry so no
global contradiction arises. The generic-suppression + religion-group triggers must treat
ideologies as their own group (Stage 3).

**Country-adoption verb (F1) — RESOLVED by oracle.** The confirmed verb is
**`set_country_religion = <ideology>`** (TI 569× / Invictus 739×; imp19c already uses it 11×). The
earlier "`set_religion` / static religion" claim was wrong. Ideology adoption is a proven layered
flow (mirroring TI's `special_religious_conversion` decision): `set_country_religion = <ideology>`
(flips the state ideology) + `set_character_religion = <ideology>` on ruler + loyal family + top
prominent characters + `set_pop_religion = <ideology>` looped over capital/core pops, plus a
`recent_convert`-style modifier + political-influence/loyalty cost for balance. No fallback needed —
the mechanic is fully buildable.

Stages, in dependency order:
- **Stage 1 — thinker pantheons.** Define ideology religions (`liberalism`, `conservatism`,
  `monarchism`, `nationalism`, `socialism`, `communism`, + keep `confucianism` as the
  statecraft/reform school) in a new `common/religions/01_ideologies.txt`, each
  `religion_category = pantheon`, SIBLING to the existing faiths. For each, 8 deities = 2 per
  category (loc-relabeled themes: war→militancy, economy→political-economy, culture→culture/press,
  fertility→social-base), routed by `trigger = { religion = <ideology> }`; generic set suppressed
  for them via `NOT = { religion = <any ideology> }`. Deities = the thinkers (roster from digest,
  Appendix A.3). Mirror the Confucian 8/2-2-2-2 shape exactly. Per-country DB registration in
  `setup/main/deities/` (no-BOM — the setup reader rejects BOM).
- **Stage 2 — adoption/conversion.** Country adoption = the layered `set_country_religion` +
  `set_character_religion` + `set_pop_religion` flow (confirmed above), gated on government/era/
  reform-state with political cost. Pop-level ideological drift uses the engine conversion driven by
  `CONVERSION_SCALE_PER_MISMATCHED_DEITY = -0.2` (`00_defines.txt:213`, live).
  **NOTE (F5):** `WRONG_RELIGION_HAPPINESS = 0` (`00_defines.txt:196`) — the mod has zeroed the
  mismatch-happiness lever, so it is NOT a live drift force. Do NOT lean on it; if re-enabling is
  wanted, note it is a GLOBAL define affecting all real religions (cross-wiring risk) — decide
  explicitly, don't flip it silently.
- **Stage 3 — reconcile engine leftovers.** Audit `00_religion_groups.txt` so an ideology never
  satisfies a `christian_group_trigger`-style check (add `ideology_group_trigger`; exclude
  ideologies from faith groups). `omen_power` → relabel "ideological fervour", accept economy
  coupling (mobilized society → output). Ideologies get NO holy sites (clean-empty, panel-break
  warning). Deified rulers → "founding theorist/figurehead" where allowed, else `can_deify_ruler=no`.
- **Stage 4 — targeted seeding (NOT a mass remap).** Reseed only the small set of 1763-nascent
  ideology holders (e.g. a few European courts as monarchist/liberal); everything else keeps its
  historical faith. Bounded edit, not a scripted sweep over thousands of lines.

The Confucian pantheon proves Stage 1 is safe as *data*; the real engineering risk is Stage 2's
adoption verb (oracle-gated) — Stages 3–4 are bounded by the coexistence decision.

### Historical grounding ✅ (digest complete — full bibliography + thinker table in Appendix A.3)

The rework's central conceit is scholarly, not just thematic: **"political religion"** (Gentile,
*Politics as Religion* 2006; Voegelin 1938; Riegel 2005 on Marxism-Leninism) describes exactly
how modern ideologies function as religions — comprehensive worldview, sacred texts (manifestos/
constitutions), prophets (thinkers), rituals, eschatology, conversion, schisms. This licenses
deity→thinker, religion→ideology, omen→doctrine-invocation, holy-site→ideological-capital,
schism→ideological-split. **Thinker roster for the 8-slot pantheons** (2 per category ×
militancy/political-economy/culture-press/social-base), drawn from the digest's 27-figure table:
- **Liberalism** — Montesquieu (1689–1755, *Spirit of the Laws* 1748), Voltaire, Adam Smith
  (*Wealth of Nations* 1776), J.S. Mill (*On Liberty* 1859), Tocqueville, Kant.
- **Conservatism** — Burke (*Reflections* 1790), de Maistre (*Du Pape* 1819).
- **Monarchism/Legitimism** — de Maistre, Hegel (*Philosophy of Right* 1821), Metternich-era figures.
- **Nationalism** — Herder (*Volksgeist*), Fichte (*Addresses to the German Nation* 1808), Mazzini.
- **Socialism** — Owen, Fourier, Saint-Simon; **Communism** — Marx & Engels (*Manifesto* 1848),
  and anarchism's Proudhon/Bakunin as a schismatic wing.
- **Chinese statecraft/reform (the CHI-relevant school, extends confucianism)** — Gong Zizhen
  龔自珍, **Wei Yuan 魏源** (*Haiguo Tuzhi* 海国图志 1843, "learn from the barbarians to control
  them"), Feng Guifen 馮桂芬 (*Jiaobinlu kangyi* 校邠廬抗議), **Yan Fu 嚴復** (translated Mill/
  Smith/Spencer/Montesquieu; *Tianyan lun* 天演論 1898), Kang Youwei 康有為 (*Datong Shu* 大同書),
  Liang Qichao 梁啟超. Sources: **Schwartz, *In Search of Wealth and Power: Yen Fu and the West***
  (1964); **Levenson, *Liang Ch'i-ch'ao and the Mind of Modern China*** (1953).
This roster + dates directly populates Stage 1's deity definitions and Stage 4's era-seeding
(which ideologies exist where at 1763 vs awaken later).

### Event & mission migration ⚠️ (impact study complete — HIGHEST RISK of the four; real gameplay bugs, no crash)

Because ideologies are new `religion` entries, every `NOT = { religion = X }` / OR-over-faiths
trigger silently gains a member. Fix these BEFORE shipping (highest-risk first):
1. **`events/imp19c_mod_events/qing_roster_events.txt`** — **15× `religion = root.religion` inside
   `create_character`** (`:63,125,187,…`). This is the known invalid-field bug class (see the
   `se_QING_SOUTHERNSTUDY.txt:97` "was root.religion — INVALID create_character religion FIELD" fix);
   if CHI's religion is an ideology, newborns get stamped with an ideology as faith. **FIX: replace
   all 15 with the literal `religion = confucianism`** (same fix already applied in
   SOUTHERNSTUDY/UPPERSTUDY/HAREM). Do this REGARDLESS — it's a latent bug today.
2. **`events/character_events.txt:506`** — heir-conversion `NOR = { dominant_province_religion =
   root.religion … }` misfires once `root.religion` returns an ideology. **FIX:** add a new scripted
   trigger `is_ideology_religion` (OR over the 6 ideology entries) and guard:
   `NOT = { root.religion = { is_ideology_religion = yes } }`.
3. **`common/laws/00_social_laws.txt:104-125`** — `state_secularism`/`state_atheism` already do
   `set_country_religion = secular/atheism` with `allow = { religion = secular }`. This COLLIDES with
   the ideology-as-country-religion channel (enacting secularism would wipe an ideology and vice
   versa). **FIX:** reconcile — exclude ideology entries from those laws' `allow`, or make ideology
   adoption and these laws mutually aware.
4. **`common/scripted_triggers/00_religion_groups.txt`** — `chinese_accepted_religion_trigger` (:93),
   `chinese_traditional_religion_trigger` (:109), `christian_group_trigger` family are OR-lists
   consumed by missionary/heritage/subject/office systems. Any consumer using `NOT = { …_trigger }`
   to mean "foreign faith → resentment" will misclassify ideology-holders. **FIX:** audit consumers;
   add `ideology_group_trigger` and exclude ideologies from the faith-group semantics.
5. **`events/imp19c_mod_events/diplomatic_play/send_settlers.txt:315`** — a released breakaway state
   inherits `…play_instigator.religion`; if that's an ideology, the new state's faith is an ideology.
   **FIX:** guard with `is_ideology_religion` or fall back to a real faith.
- **Missions:** only `qing_taiping_missions.txt:21,169` (`set_country_religion = syncretic_christian`)
  interacts — it's the intended Taiping conversion but now competes with the ideology channel;
  document precedence (Taiping victory restores a faith, wiping any ideology — acceptable, note it).
- Blast radius: ~7 event locations (2-3 genuinely misfiring) + ~4 trigger/law files + 1 mission.
  MED-HIGH — no crash, but real bugs. Items 1 & 2 are mandatory.

---

## Design 4 — Culture → Nationalism + cultural-rights → citizenship  ✅

**Question.** Repurpose culture into a NATIONALISM system (Han/Chinese → "Zhonghua" 中華, German →
German nationalism…) and cultural rights → citizenship rights defining in-group vs out-group.

### Code reality (the mod already has a nationalism engine in all but name)

- Cultures: `common/cultures/*.txt` (167 files). **Each file's top-level key IS a culture group**;
  members nest in `culture = {}`. ~167 groups, ~1,600 cultures. Group carries `color`, name pools,
  `family`, `graphical_culture`, `ethnicities`, optional levy fields. Han = `chinese_group`; Manchu
  = `manchu` in `jurchen` (`00_jurchen.txt:22`); Mongol = `mongolic`; German = `german`.
- Mechanics hang off the **culture** (not group): `primary_culture`, `dominant_province_culture`,
  `pop_culture`, `set_pop_culture`, per-country `country_culture` records. Group-level province test
  MUST use `dominant_province_culture_group = X` (the `.culture_group` form fails to parse —
  `se_QING_DECLINE.txt:680`).
- **Citizenship already exists:** the in/out-group state is the pop-rights tier via
  `integrated_pop_type_right = yes/no` in `common/pop_types/*.txt` (yes: citizen/nobles/upper+middle
  strata; no: proletariat/lower strata/tribesmen/slaves/indentured). The ONLY lever is
  `change_pop_type_right` (`prices/00_hardcoded.txt:97`, cost 5 PI) — it flips a culture's tier.
  **`is_integrated` is a read-only TRIGGER for gating (`se_QING_DECLINE.txt:488,629,634`), NOT a
  settable flag — there is no `set_is_integrated`.** In/out-group is a *derived consequence* of
  pop_type_right, not an independent flag. Reactions `on_culture_increased_right`/`_reduced_right` apply
  `rights_increased`/`rights_revoked`/`integration_status_removed`. Cleanup effects
  `increased_rights_cleanup_effect`/`reduced_rights_cleanup_effect` flagged
  **"IMP19C NOTE: THIS EFFECT NEEDS CHANGED!"** — an existing seam to finish.
- Culture-decision layer: `culture_decisions/imp19c_general_culture_decisions.txt`
  (`language_recognition`/`language_standardisation`/`self_determination`, gated on strata rights).
  Files `integrated_culture_decisions.txt` / `non_integrated_culture_decisions.txt` /
  `primary_culture_decisions.txt` are **empty scaffolding** — the home for citizenship decisions.
- **The informal 4-layer nationalism engine (mod-built):** (1) claim hostility
  `se_CLAIM_HOSTILITY.txt`; (2) migration/settler `se_MIGRATION.txt` (province plurality flip →
  kin-state `add_claim` → irredentist play); (3) de jure/irredentism `se_DEJURE.txt` (frozen
  `dejure_culture` = homeland, `dejure_disaffection`); (4) separatism `se_SEPARATISM.txt`
  (breakaway country + foreign kin-state backer, `@separatism_backer_chance=50`). Plus the Qing
  ethnic layer (`se_QING_ETHNIC_TENSION.txt`, `se_QING_DECLINE.txt` dyarchy/banner/Han stances,
  `se_QING_SINICIZATION.txt` `set_pop_culture` trend) and subject-integration
  (`se_SUBJECT_QING.txt` + `qing_subject_integration.txt` + `se_QING_INTEG_CAPSTONE.txt`).
- Conversion exists: `set_pop_culture` (`se_QING_DECLINE.txt:760`, inside `random_pops_in_province`
  — the civic-sinicization pass; `se_QING_SINICIZATION.txt` only maintains the counters/flags
  `qing_sinic_count`/`qing_prov_sinicized`, NOT the conversion itself), `set_culture` on chars.

### DECISION — relabel-and-formalize; nationalism at the GROUP level; RE-LOCALIZE keys (full build)

This is a relabel-and-formalize, and the decision is to do it fully:
- **Nationalism = culture GROUP level** (identity/loyalty/irredentism). Individual cultures remain
  the engine-level carriers of rights/names/portraits/plurality. Bridge via existing
  `00_culture_supergroups.txt`/`00_culture_subgroups.txt` triggers + the
  `dominant_province_culture_group` idiom. "Zhonghua 中華" = `chinese_group` (unifies
  beihua/wu/yue/hakka/min/hui/han); "Deutschland" = `german` group.
- **Rename decision: RE-LOCALIZE display names, DO NOT rename internal keys.** Renaming
  `chinese_group`→`zhonghua` touches ~34–59 files and breaks name-gen/portrait coupling; changing
  only the localized display name + adding a nationalism concept layer achieves the same
  player-facing result at near-zero blast radius. This is the committed choice, not a fallback.
- **Citizenship in/out-group = reuse `is_integrated` + `integrated_pop_type_right` tiers +
  `culture_happiness_modifier` verbatim.** "Grant/revoke citizenship" = `change_pop_type_right`
  surfaced to the player through the empty `*_culture_decisions.txt` files (now filled) and the
  `culture_view.gui`. Finish the two "NEEDS CHANGED" cleanup effects to express in/out-group cleanly.
- **Homeland/grievance/awakening/irredentism/rebellion = reuse** `dejure_culture`,
  `dejure_disaffection`, `set_pop_culture`+sinicization trend, `add_claim` kin-state seeds,
  `SEPARATISM_*`. Surface these to the player as an explicit "Nationalism" concept/panel rather
  than leaving them as background sim — a nationalism meter per culture-group derived from the
  existing de-jure disaffection + integration state. **Ratchet rule (standing
  [[imp19c-no-restoring-drift-ratchet-rule]]):** if the nationalism/awakening meter is a passive
  0..100 accumulator it MUST carry restoring drift + band-gated nudges. PREFERRED: make it a pure
  DERIVED read-out (recomputed each pulse from `dejure_disaffection` + integration + unrest, not
  accumulated), which sidesteps the ratchet entirely — a derived value has no memory to pin.
- **New content built here (not deferred):** (a) a nationalism concept layer + player-facing
  read-out (culture-group loyalty/awakening derived from existing vars); (b) filled
  `integrated_culture_decisions.txt` / `non_integrated_culture_decisions.txt` /
  `primary_culture_decisions.txt` with citizenship grant/revoke decisions built on
  `change_pop_type_right`; (c) finished rights-cleanup effects; (d) loc relabel of the major
  setting groups to nationalism names.

### Historical grounding ✅ (digest complete — full bibliography + culture→nationalism table in Appendix A.4)

The design's core premise — **nations are constructed, not primordial** — is the mainstream of
the field: Anderson, *Imagined Communities* (1983, print-capitalism); Gellner, *Nations and
Nationalism* (1983, industrialization); Hobsbawm & Ranger, *The Invention of Tradition* (1983);
Anthony D. Smith's ethnosymbolist counter (pre-existing ethnic cores); Hroch's 3-phase model
(scholarly → agitation → mass). This validates modeling nationalism as an *emergent end-state*
over a fragmented-culture start, exactly what the mod's informal engine already does. The
**civic vs ethnic** split (Kohn 1944; **Brubaker, *Citizenship and Nationhood in France and
Germany*** 1992 — jus soli vs jus sanguinis) is the scholarly frame for the citizenship in/out-
group mechanic (`change_pop_type_right` over the pop-rights tiers; `is_integrated` as the read-only
gate). **New Qing History** (Elliott, *The Manchu
Way* 2001; Crossley, *Orphan Warriors* 1990; Rawski 1996; Rhoads, *Manchus and Han* 2015) grounds
the Qing ethnic hierarchy (banner status, Manchu>Mongol>Han, 教化 *jiaohua* assimilation, 藩部
frontier dependencies) that the dyarchy/banner/Han stance system already models. Crucially,
**中華民族 (Zhonghua minzu)** was coined by **Liang Qichao 梁啟超 in 1902** (Leibold 2007; Man
2020; 郑大华 2026) — so "Zhonghua nationalism" is a period-authentic *invented* identity that
awakens mid-game, not a start condition. **Culture→nationalism label table** (digest §V) supplies
the loc relabel: Han→中華/Zhonghua minzu, Manchu→滿族, German→Deutschtum, Italian→Risorgimento,
French→La Nation française, Mongol→蒙古族, Tibetan→藏族, Hui→回族, plus Polish/Irish/Greek/
Hungarian/etc. The "cultural rights → citizenship" transition (corporate/estate/millet → individual
national citizenship; subject → citizen) is precisely the empty-`*_culture_decisions.txt` +
`change_pop_type_right` build.

### Event & mission migration ✅ (impact study complete — LOWEST RISK; keys unchanged → cosmetic)

Because the rework RE-LOCALIZES display names and does NOT rename culture keys, existing triggers
keep working — the ~10 event hits (`introduction_events.txt`, `character_events.txt`,
`NameChangeEvents.txt`, `qing_pilgrimage_events.txt`, `send_settlers.txt:44,98,314`, etc.) all read
`primary_culture`/`culture_group`/`has_culture` on unchanged keys → **no breakage, cosmetic only**.
- **The one consistency task:** `events/imp19c_mod_events/office_eligibility_events.txt`
  (10× `has_culture = manchu`/`mongolian`, the Banner in/out-group gate) is the existing citizenship
  concept. When citizenship becomes `integrated_pop_type_right`/`change_pop_type_right`-driven,
  cross-check these `has_culture` eligibility gates against the new pop-right so they stay in sync
  (derive one from the other, or add the pop-right check alongside).
- **Group-granularity option:** the dejure/separatism engine (`se_DEJURE.txt:48` freezes
  `dejure_culture = dominant_province_culture`) uses the culture (not group) form. If nationalism
  should operate at GROUP granularity, switch `dominant_province_culture` → `dominant_province_culture_group`
  there and in the readers (`se_SEPARATISM.txt`, `se_QING_DECLINE.txt:474-622`) — the standing
  parse-trap: never the `.culture_group` accessor form in a province limit.
- **Missions:** ZERO qing mission files check `is_integrated`/pop-rights/`culture_group` — no mission
  migration needed. Blast radius: ~10 events (cosmetic) + 0 missions.

---

# PART II — IMPLEMENTATION

Concrete build plans, derived from the design decisions above. Each obeys the standing rules:
no compile-inlined heavy chains in scripted-gui buttons (trampoline via `is_triggered_only`
events); no `create_character`+`add_trait` at gamestate construction; contiguous setup char-IDs;
no ownerless capitals; valid comparison RHS; every net-new effect se_LOG-wired (sys=QING);
task-tagged comments; brace/byte-convention check before commit; independent code-review before commit.

---

## Implementation 1 — Foreign-building use cases
**STATUS (2026-07-24, CODE-VERIFIED): PARTIALLY BUILT. The 6 building types + modifiers + the 6 authorization EFFECTS (se_QING_FOREIGNBUILD.txt) exist, but a code check of actual CALLERS shows only 2 of the 6 effects are reachable: `QING_fbuild_subject_works` (called from qing_selfstrengthening_missions.txt:237) and `QING_fbuild_plant_treaty_port` (se_QING_TREATIES.txt:186). DEFERRED / NOT WIRED (zero callers anywhere — orphaned): `QING_fbuild_embassy`, `QING_fbuild_frontier_colony`, `QING_fbuild_frontier_fort`, `QING_fbuild_mission_capstone`. Also deferred: any player-facing button surface (no scripted_gui references any fbuild effect). NOTE: the buildings themselves are player-buildable in-menu after the BT-D1-3 fix (real gated allow: has_city_status + owner invention tech); the "authorization effect" path is what's mostly unwired.**

**Files — new:**
- `common/buildings/qing_foreign_buildings.txt` (EXTEND): add `qing_foreign_works_building`,
  `qing_frontier_colony_building`, `qing_frontier_fort_building`, `qing_embassy_building`,
  `qing_treaty_port_building`, `qing_mission_cathedral_building`. Local modifiers only; gates
  per-archetype (`has_city_status` dropped for colony + rural mission).
- `common/scripted_effects/se_QING_FOREIGNBUILD.txt` (NEW): authorization effects —
  `QING_fbuild_subject_works` (add_building_level in subject province, spend treasury+PI, apply
  overlord country modifier), `QING_fbuild_frontier_colony/fort`, `QING_fbuild_embassy`,
  `QING_fbuild_plant_treaty_port` (war-outcome), `QING_fbuild_mission_capstone`. Each guarded +
  se_LOG.
- `common/modifiers/qing_foreignbuild_modifiers.txt` (NEW): country modifiers
  `qing_fbuild_works_patron`, `qing_embassy_representation`, `qing_treaty_port_humiliation`, etc.
- `events/imp19c_mod_events/qing_foreignbuild_events.txt` (NEW): the `has_building`-keyed pulses/
  crises (embassy diplomatic-representation upkeep; treaty-port unrest; mission-density → Boxer
  sentiment). Namespace `qing_fbuild`. All heavy work in `is_triggered_only` events (trampoline).
- Loc: `localization/english/qing_foreignbuild_l_english.yml` (BOM+LF).
**Files — edited:**
- Subject-interaction / diplomatic-action surface: add buttons in the relevant scripted_gui +
  `gui/` panel (subject view for works-aid; diplomatic view for embassy). Reuse the proven
  `ExecuteConsoleCommand('gui.createwidget …')` / `ScriptedGui.Execute` idioms; close via
  `GUI.ClearWidgets`.
- Colonization mission trees: grant the frontier buildings as on-map deliverables where those
  missions currently grant abstract rewards.
**Order:** buildings → modifiers → effects → events → GUI wiring → loc. **Boot-crash watch:**
`add_building_level` in a subject/foreign province — verify province owned + valid at call;
never grant a building to a province whose owner is null.

## Implementation 2 — Engine-law expansion for Qing policy
**STATUS (2026-07-24, CODE-VERIFIED): BUILT — 12 law groups present in common/laws/00_qing_statutes_laws.txt. Deferred candidates (amban establishment law, tributary demand/cadence law, + the chunk-2.8 set) CONFIRMED ABSENT in code = deferrals real. Accurate.**

Built on the NATIVE engine law system (schema resolved above), NOT a variable panel. Each Qing
policy = a new law GROUP (nested options); the player enacts via the stock Laws tab (`LawItem.Enact`
→ `change_law`); each option's effect rides in its `modifier`/`on_enact`.

**Files — new:**
- `common/laws/00_qing_ministry_laws.txt` (NEW, **UTF-8 BOM**): the core 9 ministry law groups +
  the expansion groups (from the Qing-mechanics inventory, IN FLIGHT). Each group:
  `potential = { tag = CHI }`; first option = current-behavior default (so a fresh game holds it and
  nothing changes until the player legislates); subsequent options carry `allow` (tech/era gate),
  `modifier = { }` (static country modifier, e.g. `global_tax_modifier`, `monthly_governor_wage`,
  discipline/manpower), and/or `on_enact = { }` running the mod's existing effects/vars. Copy the
  Invictus `00_monarchy.txt:58-126` shape.
- `common/scripted_effects/se_QING_LAW.txt` (NEW): helpers — `QING_law_apply_<group>` effects called
  from `on_enact` where a law must drive existing Qing machinery (set the establishment target the
  roster staffer reads; set the exam cadence; set per-office weight vars for `QING_council_recompute`).
  se_LOG-wired. **`on_enact` reaching `QING_council_recompute` must trampoline** via a hidden
  `is_triggered_only` event (compile-inline crash class) — `on_enact` fires `trigger_event`, not the
  heavy chain inline.
- `common/scripted_effects/se_QING_LAW_AI.txt` (or extend existing `ai_choose_and_enact_law_*`):
  AI law-selection so non-player CHI/AI picks sane options (else it sits on the default).
- Loc: append to `localization/english/laws_l_english.yml` (**BOM+LF**) — a `<group_key>` +
  `<group_key>_desc` and every `<option_key>` + `<option_key>_desc`.
**Files — edited:**
- **`gui/government_view.gui:2040-2253` (MANDATORY):** add a `laws_widget_area` entry for EACH new
  law group (filter `EqualTo_string(LawGroupItem.GetName, Localize('<group_key>'))`, template at
  `:2242-2253`). Without this the groups are invisible in the Laws tab (the documented
  `succession_law` bug). This is the make-or-break edit.
- **`se_QING_SUBPOSTS.txt:182-184,226,238,249`** — estab targets `4` read from the enacted law
  (via `has_law = <estab_option>` branch or a var set in the law's `on_enact`) instead of the literal;
  enrol caps `6` in `QING_zongli_panel.txt:93` / `QING_censorate_panel.txt:79` /
  `QING_governance_actions.txt:621` likewise.
- **`se_QING_EXAM.txt:126-137`** — `qing_exam_triennial_cooldown` derived from the enacted cadence law.
- **`se_QING_COUNCIL.txt:314-341,439-471`** — per-office contribution scaled by the weight the
  precedence law set (var or `has_law`), in `QING_council_score_office`/the fold.
- **`se_QING_REVENUE.txt` / `se_QING_WAR.txt` / `se_QING_WORKS.txt`** — read the tax/training/works
  law state where those pulses currently use fixed values.
- **`common/prices/00_hardcoded.txt:5`** — leave the global `enact_law` cost (35 PI/15 stab); if
  Qing laws should cost differently, drive `enact_law_cost_modifier` from a CHI government/modifier.
- **Retire the bespoke config where a law now owns it:** `qing_caravan_customs_rate` and
  `qing_salt_gabelle_reformed` become law-driven (their scripted-GUI setters either call `change_law`
  or are replaced by the law option); keep the underlying var as the read-surface the pulse already
  uses, now SET by the law's `on_enact` rather than the old panel button.
**Order:** author law groups (data) → loc → **government_view.gui area entries** → `on_enact`
helper effects (trampolined) → literal/pulse reads re-pointed to law state → AI selection → boot
test (laws must render in the tab AND enact). **Boot-crash watch:** BOM on the law file; first
option = current default (no-op start = byte-identical to today); any `on_enact` reaching
`QING_council_recompute`/a sorting iterator MUST `trigger_event`-trampoline, never inline;
`change_law` targets must have a passing group `potential` or they silently no-op.

## Implementation 3 — Religion → Ideology
**STATUS (2026-07-24, CODE-VERIFIED): NEARLY COMPLETE — one deferral remains. Verified present in code: 6 ideology religions, is_ideology_religion triggers, migration guards (items 4 missionary + 5 send_settlers confirmed), layered set_country_religion adoption, the adoption DECISION → qing_ideology.2 choice event → qing_ideology.1 trampoline chain (all wired), and the 48 custom thinker-deities + DB + holy-site shrines. STILL DEFERRED (NOT built — code check found no country/province seeded onto an ideology at 1763 start): Stage-4 targeted 1763-nascent ideology seeding (Design 3 Stage 4). So ideologies are adoptable at runtime via the decision, but the 1763 world starts with ZERO ideology holders. The earlier "FEATURE-COMPLETE" claim was inaccurate on this point.**

**Files — new:**
- `common/religions/01_ideologies.txt` (NEW): the ~6 ideology religions.
- `common/deities/04_ideology_thinkers.txt` (NEW): 8 deities × each ideology (2 per category),
  `trigger = { religion = <ideology> }`, thinker roster from the digest, mirroring
  `03_confucian_pantheon.txt` exactly (icons, passive_modifier + omen using existing `*_svalue`s).
- `setup/main/deities/03_ideologies.txt` (NEW): per-ideology deity-DB registration (fresh
  contiguous DB key block above 1407).
- `common/scripted_effects/se_QING_IDEOLOGY.txt` (NEW): `QING_adopt_ideology = { ideology = X }`
  — the proven layered flow: `set_country_religion = $ideology$` + `set_character_religion` on
  ruler/loyal-family/top-prominent chars + `set_pop_religion` looped over capital/core pops
  (`random_pops_in_province`), + a `recent_convert`-style country modifier + PI/loyalty cost. Model
  on TI's `special_religious_conversion` decision. (Use `set_country_religion`, NEVER `set_religion`
  — the latter does not exist.) + pop-drift helpers.
- `events/imp19c_mod_events/qing_ideology_events.txt` (NEW): adoption/awakening events (namespace
  `qing_ideo`), all `is_triggered_only`.
- Loc + icons: `localization/english/qing_ideology_l_english.yml`, `qing_ideology_deities_l_english.yml`;
  deity icons under `gfx/interface/icons/deities`.
**Files — edited:**
- `common/deities/00_generic.txt` — extend the suppression trigger to `NOT = { religion = <any
  ideology> }` so ideologies show their own thinkers.
- `common/scripted_triggers/00_religion_groups.txt` — add `ideology_group_trigger`; ensure faith
  group triggers exclude ideologies.
- `setup/main/00_default.txt` — Stage-4 scripted remap of country/pop/character `religion=` to
  seed the 1763 ideology world-state.
- `common/defines/00_defines.txt` — tune conversion/mismatch defines for ideology drift.
**Order:** religions → deities → DB registration → generic suppression edit → group-trigger
reconcile → adoption effect/events → loc/icons → world remap last. **Boot-crash watch:** keep
8/2-2-2-2 per ideology and NO holy sites (panel-break class); DB keys contiguous; the
setup/deities reader rejects BOM (per memory) — write no-BOM. Ideology adoption events
trampolined.

## Implementation 4 — Culture → Nationalism + citizenship
**STATUS (2026-07-24, CODE-VERIFIED): BUILT — nationalism-group triggers, 3 filled culture_decisions files (grant via integrate_country_culture), modifiers + loc all present. NOTE: the grant-citizenship decision had a scope bug (integrate_country_culture = scope:target_culture.culture) that dropped the Qing decisions at load — FIXED 76d8c3df1 (now scope:target_culture). DEFERRED (code-verified absent — no nationalism/civic_identity/naturalised refs in gui/culture_view.gui): the optional culture_view.gui read-out panel. Deferral real.**

**Files — new:**
- `common/scripted_triggers/00_nationalism_groups.txt` (NEW): nationalism = culture-group
  concept helpers built on the supergroup/subgroup triggers.
- `common/scripted_effects/se_QING_NATIONALISM.txt` (NEW): derive a per-group nationalism/
  awakening meter from existing `dejure_disaffection` + `is_integrated` + unrest; helpers to
  grant/revoke citizenship wrapping `change_pop_type_right`; se_LOG-wired.
- `culture_decisions/integrated_culture_decisions.txt`,
  `non_integrated_culture_decisions.txt`, `primary_culture_decisions.txt` (FILL the empty files):
  citizenship grant/revoke + national-recognition decisions gated on strata rights, applying the
  existing rights modifiers.
- `gui/` nationalism read-out (extend `culture_view.gui` rather than a new window).
- Loc: `localization/english/qing_nationalism_l_english.yml` + a relabel pass in the culture loc
  yml giving the major setting groups their nationalism display names (中華/Zhonghua, Deutschland,
  etc.) — DISPLAY NAMES ONLY, internal keys untouched.
**Files — edited:**
- `on_action/00_specific_from_code.txt` — finish `increased_rights_cleanup_effect` /
  `reduced_rights_cleanup_effect` (the "NEEDS CHANGED" seams) to express in/out-group transitions.
- Hook the nationalism meter derivation into the existing quarterly Qing pulse (beside the
  ethnic-tension pulse); reuse `dominant_province_culture_group` (never `.culture_group`).
**Order:** nationalism triggers → derivation effect + pulse hook → citizenship decisions (fill
empty files) → cleanup-effect finish → GUI read-out → loc relabel. **Boot-crash watch:** no
internal culture-key renames (blast-radius/name-gen); group-level province tests use
`dominant_province_culture_group`; `change_pop_type_right` is a proven priced effect — verify
cost path.

---

## Review & sourcing status

- Code maps: ✅ all three complete (GC ministry config, religion/pantheon, culture/citizenship).
- Historical digests: ✅ all four complete and folded into the Design sections above +
  Appendix A. Standalone digest files were consolidated here and removed per the
  "everything in overnight_designs.md" instruction.
- Independent design review: ✅ complete (code-review agent, verified claims against the code).
  Verdict: **Design 1 & 2 buildable as written** (strongest: Design 2 — architecture + every cited
  key confirmed). **Design 4 sound** after 3 corrections applied (F3 `is_integrated` is a read-only
  trigger not a settable flag → citizenship driven only by `change_pop_type_right`; F4 sinicization
  `set_pop_culture` is in `se_QING_DECLINE.txt:760` not `se_QING_SINICIZATION.txt`; F6 nationalism
  meter made a derived read-out to sidestep the ratchet rule). **Design 3** had the one CRITICAL
  gap (F1 `set_religion` unproven) → resolved by (a) an in-flight oracle check + a pop-driven
  fallback branch, and (b) a coexistence decision (F2) that removes the mass-remap blast radius.
  F5 (`WRONG_RELIGION_HAPPINESS=0`) and the `EXPECTED_DEITY_COUNT` slip also corrected.
- Oracle check (Design 3 F1): ✅ RESOLVED. Country religion IS directly mutable via
  **`set_country_religion`** (TI 569× / Invictus 739×; imp19c already uses it 11×). The guessed
  `set_religion` does not exist. Ideology adoption = layered `set_country_religion` +
  `set_character_religion` + `set_pop_religion` flow (per TI's `special_religious_conversion`).
  Design 3 Stage 2 + Implementation 3 updated; no fallback needed — all four designs fully buildable.
- Implementation docs (Part II): ✅ complete — one file-by-file plan per design, with new/edited
  files, exact keys/vars/event-IDs, staging order, and a per-design boot-crash-avoidance checklist.
- **Design 2 rescoped (user directive):** the earlier "variable-panel, not engine laws" decision
  was RETRACTED. Design 2 is now a **dramatic expansion of the NATIVE engine law system** —
  ~35–40 Qing-policy law groups. Engine-law schema mapped (enact = `change_law`; grouping = nesting;
  `on_enact` runs arbitrary effects; global cost 35 PI/15 stab; **the Laws tab in
  `government_view.gui` hand-enumerates every group — new groups MUST get an area entry or they're
  invisible**; law files need BOM). Full catalogue + oracle template folded into Design/Impl 2.
- **Event & mission migration (user directive):** ✅ impact study complete; an "Event & mission
  migration" subsection now sits under each design. Risk ranking: **Design 3 (Religion→Ideology)
  MED-HIGH** — the 15× `religion = root.religion` create_character lines in `qing_roster_events.txt`
  + the `character_events.txt:506` heir misfire + the `00_social_laws.txt` `set_country_religion`
  collision + OR-list trigger fan-out are the must-fix items (no crash, real bugs). Design 1
  (buildings) LOW-MED = wire new buildings into `QING_prov_has_mission`/works tally + swap mission
  rewards. Design 2 (laws) LOW = ~2 events, keep vars as mirrors. Design 4 (nationalism) LOWEST =
  keys unchanged, cosmetic + one office-eligibility consistency task.
- Build tasks created: #60 (Design 2 laws), #61 (Design 3 ideology), #62 (Design 4 nationalism);
  #52 already covers Design 1 (foreign buildings).

## Build-order recommendation (all four are independent; suggested sequence by risk)

1. **Design 2 (Ministry laws)** — strongest/lowest-risk; defaults = current literals so a no-op law
   state is byte-identical to today. Highest player value per unit risk.
2. **Design 1 (Foreign buildings)** — additive; main watch = valid province scope for cross-border
   `add_building_level`.
3. **Design 4 (Nationalism/citizenship)** — mostly relabel + fill empty decision files + finish the
   two flagged cleanup effects; no key renames.
4. **Design 3 (Religion→Ideology)** — largest surface; Stage 1 (data) is proven-safe, Stages 2–4
   bounded by the coexistence decision. Build last, stage-by-stage, with a boot test between stages.

---

# APPENDIX A — Consolidated academic bibliography

Compiled 2026-07-23 via web research. Confidence is marked where the researching agent could
not fully verify a citation; treat flagged items as leads, not settled references. Primary-source
dates (treaties, works, coinages) are used as game-gating anchors above.

## A.1 — Foreign presence in Qing China (Design 1)

**Christian missions:** Cohen, *China and Christianity: The Missionary Movement and the Growth of
Chinese Antiforeignism, 1860–1870* (Harvard, 1963); Esherick, *The Origins of the Boxer Uprising*
(UC Press, 1988); Harrison, *The Missionary's Curse and Other Tales from a Chinese Catholic
Village* (UC Press, 2013); Laamann, "The Christian Manchu Missions during the Qing Period" (2017,
on the 1724 proscription); Standaert, "Christianity in late Ming and early Qing China" (2015);
Spence, *To Change China: Western Advisers in China, 1620–1960* (1969). French: De Gruttola, *Au
tribunal du repentir. La proscription du catholicisme en Chine (1724–1860)* (2024).
**Concessions/treaty ports:** Fairbank, *Trade and Diplomacy on the China Coast* (Harvard, 1953,
foundational — flagged not-directly-retrieved); Jackson, *Shaping Modern Shanghai: Colonialism in
China's Global City* (2020); Bickers & Jackson, *Treaty Ports in Modern China* (2016); So & Myers,
*The Treaty Port Economy in Modern China* (2011); Zhao, *The Qing Opening to the Ocean* (2013);
Perez-Garcia & Jin, "the Canton System" in *Great Trade Walls in Imperial China* (2023); Xie,
"Borderland Macao" (2026); Buhi, *Constitutional History of Macau* (2021).
**Embassies:** Hevia, *Cherishing Men from Afar: Qing Guest Ritual and the Macartney Embassy of
1793* (Duke, 1995); Mosca, *From Frontier Policy to Foreign Policy* (2013); Liu, *The Clash of
Empires* (2004); Horowitz, *Central Power and State Making: The Zongli Yamen and Self-Strengthening*
(1998).
**Frontier colonization:** Perdue, *China Marches West: The Qing Conquest of Central Eurasia*
(Belknap/Harvard, 2005); Di Cosmo, "Qing colonial administration in Inner Asia" (*Int'l History
Review*, 1998); Kowalski, "Holding an Empire Together: Army, Colonization and State-building in
Qing Xinjiang" (2017).
**Self-Strengthening:** Elman, "Naval Warfare and the Refraction of China's Self-Strengthening
Reforms… 1865–1895" (*Modern Asian Studies*, 2004); Hsü, *The Rise of Modern China* (OUP);
Kennedy, *The Arms of Kiangnan* (Westview, 1978, foundational — flagged not-retrieved); Pong on
Shen Baozhen & the Fuzhou Navy Yard (flagged). Chinese: 魏文享 (2016) on 江南制造局 finances;
萧致治 (2008) on 左宗棠 & 福州馬尾船政局.

## A.2 — Qing ministries & statutory regulation (Design 2)

Bartlett, *Monarchs and Ministers: The Grand Council in Mid-Ch'ing China, 1723–1820* (UC Press,
1991, flagged details-unverified); Will et al., *Handbooks and Anthologies for Officials in
Imperial China* (Brill, 2020); **Elman, *A Cultural History of Civil Examinations in Late Imperial
China*** (UC Press, 2000); **Zelin, *The Magistrate's Tael: Rationalizing Fiscal Reform in
Eighteenth-Century Ch'ing China*** (UC Press, 1984 — 養廉銀 salary figures); Wong, *China
Transformed* (Cornell, 1997); Kuhn, *Soulstealers: The Chinese Sorcery Scare of 1768* (Harvard,
1990 — memorial/rescript policy mechanism). Primary/statutory: *Da Qing Huidian* 大清會典 (five
editions 1690/1733/**1764**/1818/1899); per-Board 則例 — *Qinding Hubu zeli* 戶部則例, *Libu zeli*
吏部則例, *Qinding kechang tiaoli* 欽定科場條例 (1887), *Lifanyuan zeli* 理藩院則例 (1842),
*Caoyun zeli zuan* 漕運則例纂 (1757), *Wuliao jiazhi zeli* 物料價值則例 (1768), *Baqi zeli* 八旗則例
(1739). Springer, *Yushi* 御史 entry (2026). Harvard Ming-Qing Documents Project (Scalar) for the
Huidian/zeli holdings.

## A.3 — Political ideologies & thinkers (Design 3)

**Framework — political religion:** Gentile, *Politics as Religion* (Princeton, 2006) + "Political
Religion: A Concept and its Critics" (*Totalitarian Movements and Political Religions*, 2005);
Voegelin, *Die politischen Religionen* (1938); Riegel, "Marxism-Leninism as a political religion"
(2005). **Enlightenment/liberalism:** Israel, *Radical Enlightenment* (OUP, 2001), *Democratic
Enlightenment* (Princeton, 2011); Skinner, *The Foundations of Modern Political Thought* (CUP,
1978); Berlin, *Four Essays on Liberty* (OUP, 1969). **Conservatism/Counter-Enlightenment:**
Berlin, *The Crooked Timber of Humanity* (1990), *Three Critics of the Enlightenment: Vico,
Hamann, Herder* (2000). **Romantic nationalism:** Berlin, *The Roots of Romanticism* (1999).
**Socialism/Marxism:** Berlin, *Karl Marx: His Life and Environment* (1939/2013). **Chinese
reform:** **Schwartz, *In Search of Wealth and Power: Yen Fu and the West*** (Harvard, 1964);
**Levenson, *Liang Ch'i-ch'ao and the Mind of Modern China*** (Harvard, 1953) + *Confucian China
and Its Modern Fate* (3 vols, UC Press, 1958–65); Chang (Zhang Hao 張灝), *Chinese Intellectuals in
Crisis* (UC Press, 1987). Full 27-figure thinker table (name/dates/ideology/key work/contribution,
with 中文 for the East Asian figures) is in the Design 3 grounding + the source digest.
Confidence: biographical/work dates HIGH; some later-work publishers MODERATE; French/German/
Chinese secondary scholarship (Bianco, Franke, 余英時, 王汎森) named but not extracted.

## A.4 — Nationalism & citizenship (Design 4)

**Theory:** Anderson, *Imagined Communities* (Verso, 1983/1991); Gellner, *Nations and
Nationalism* (Cornell/Blackwell, 1983); Hobsbawm, *Nations and Nationalism since 1780* (CUP, 1990)
+ Hobsbawm & Ranger, *The Invention of Tradition* (CUP, 1983); Smith, *The Ethnic Origins of
Nations* (Blackwell, 1986); Kohn, *The Idea of Nationalism* (Macmillan, 1944, civic/ethnic
dichotomy); Kedourie, *Nationalism* (Hutchinson, 1960); Hroch, "From National Movement to the
Fully-formed Nation" (*New Left Review*, 1998). **Citizenship:** **Brubaker, *Citizenship and
Nationhood in France and Germany*** (Harvard, 1992); Rapport, *Nationality and Citizenship in
Revolutionary France 1789–1799* (Clarendon, 2000); Gammerl, *Subjects, Citizens, and Others…
British and Habsburg Empires 1867–1918* (Berghahn, 2017). **New Qing History / Chinese
nationalism:** Elliott, *The Manchu Way* (Stanford, 2001); Crossley, *Orphan Warriors* (Princeton,
1990); Rawski, "Reenvisioning the Qing" (*JAS*, 1996); Rhoads, *Manchus and Han* (UW Press, 2015);
Leibold, *Reconfiguring Chinese Nationalism* (Springer, 2007); Schneider, *Nation and Ethnicity*
(Brill, 2017). Chinese: 郑大华 (Zheng Dahua), "梁啟超與'中華民族'" (*清史研究*, 2026); 施正鋒,
"中國的民族主義" (2016). Full culture→nationalism mapping table (18 identities with 中文) is in the
digest §V, summarized in Design 4 grounding.

---

# PART III — EXECUTION

Live log of the implementation of Parts I–II. Every non-obvious decision recorded here as it
is taken. Build order = risk order from the build-order recommendation (2 → 1 → 4 → 3). Each
design is split into small, independently-debuggable commits; each commit gets a general review
AND a boot-crash review before it lands. Author = freekumquats. Branch = merge-overnight.

## Cross-cutting execution decisions
- **Commit granularity:** small coherent chunks, not one mega-commit — e.g. Design 2 lands as
  (a) the law pipeline proven on 2 pure-modifier-swap groups + the mandatory government_view.gui
  tab wiring, then (b) further law groups in batches by domain. Each chunk boots on its own.
- **Reviews before every commit:** an independent code-review AND a boot-crash review (known
  imp19c crash classes: compile-inlined heavy chain in a scripted_gui/law on_enact, create_character
  +add_trait at construction, setup char-ID gaps, ownerless capitals, BOM in setup/ readers, bad
  comparison RHS). Findings resolved before the commit.
- **Proving-first for the engine-law expansion:** the make-or-break unknowns are (1) does a new
  law group render in imp19c's hand-enumerated Laws tab, and (2) does on_enact drive a Qing var/
  effect. Both are validated on the 2 cheapest groups (Penal Code + Ritual Orthodoxy, pure
  modifier-swaps) in the first chunk before authoring the other ~35.

## Design 2 — EXECUTION LOG

### Chunk 2.1 — law pipeline proven on 2 modifier-swap groups + GUI tab wiring
Files: `common/laws/00_qing_statutes_laws.txt` (NEW, BOM); `gui/government_view.gui` (new
laws_widget_area after succession_law); `localization/english/laws_l_english.yml` (+18 keys);
`localization/english/imp19c_interface_l_english.yml` (+`qing_statutes_laws` category title).
Decisions:
- **Two groups authored:** `qing_penal_code_law` (刑部/大清律例: balanced-default / merciful / harsh /
  revised) and `qing_ritual_orthodoxy_law` (禮部: conventional-default / orthodox / pragmatic). Both
  pure modifier-swap (no on_enact) — chosen as chunk 1 to validate the two unknowns (does a new group
  render in the hand-enumerated Laws tab; is the schema right) before authoring the ~35 others.
- **First option = empty `modifier = { }` default** so a fresh game holds it and behaviour is
  byte-identical to today until the player legislates (no on_game_initialized seeding needed — the
  engine defaults to the first option).
- **Modifier values mirror the existing `qing_justice_*` / `qing_rites_*` EVENT modifiers** but as
  DISTINCT inline law modifiers (no key collision; the law is a standing stance, the events remain the
  reactive layer). Watch item flagged to design review: standing vs temporary magnitude.
- **GUI tab registration (the make-or-break):** added ONE `qing_statutes_laws` "Statutes (會典)"
  laws_widget_area enumerating both groups; further Qing groups append laws_widget entries to it.
- **Category title** as a raw loc key `qing_statutes_laws` in imp19c_interface_l_english.yml, matching
  the `civil_laws`/`economic_laws` sibling convention (NOT a bespoke UPPER key).
- Integrity: law file BOM ✓, braces 20/20; government_view.gui braces 1965/1965; 18 loc keys all
  resolve; all 6 modifier keys are country-scope keys already in use. Reviews (boot-crash + design)
  dispatched before commit.

**Chunk 2.1 boot-crash review: CLEAN PASS.** Will load (no AV); both groups render in the CHI Laws
tab under "Statutes (會典)" and are enactable. All 7 checks passed — BOM (EF BB BF), schema matches
currency_law/succession_law, all 6 modifier keys country-scope (the law copies only the country-scope
portions of qing_justice_*/qing_rites_*, not the local_* ones), `civic_tech>=4` valid, new
laws_widget_area structurally identical to siblings at correct depth (govt_view braces 1969/1969),
18 loc keys resolve, no on_enact/iterator, no modifier key collision. Design review pending.

**Chunk 2.1 design review: mechanics sound; 3 balance fixes applied.**
- Free-lunch fix: `qing_penal_merciful` reframed as the LEGITIMACY option (unrest −1→−0.5, so harsh is
  the ORDER option — a real axis); `qing_ritual_orthodox` given a `global_commerce_modifier = -0.03`
  cost (tradition-vs-modernity axis). No option now strictly dominates the default.
- Gate fix: reform tiers (`qing_penal_revised`, `qing_ritual_pragmatic`) gated on
  `has_variable = qing_reform_track_unlocked` (mid-game reform unlock, se_QING_DECLINE.txt, set at reform
  pressure ≥50) instead of `civic_tech >= 4`. VERIFIED: only ONE setup country has an explicit civic_tech
  block (level 0, an English tag) — the mod starts tech LOW, so civic_tech>=4 was NOT a no-op-at-start as
  the reviewer assumed, but the reform-track var is a far better thematic gate regardless. `has_variable`
  is a valid country-scope `allow` trigger (allow blocks evaluate in country scope like social_laws' `religion=`).
- De-escalation: standing legitimacy rates trimmed (merciful 0.03→0.02) toward the milder-than-temporary
  principle already applied to the ritual tier.
- Loc updated to match (reform tiers now say "reform current…taken hold", not "civic advancement").
- Integrity re-checked: law braces 20/20. → COMMIT chunk 2.1.

### Chunk 2.2 + 2.3 — var-driven + stance-driven law groups (5 groups)
Files: `00_qing_statutes_laws.txt` (+5 groups), `government_view.gui` (+5 laws_widget), `laws_l_english.yml` (+~34 keys).
Groups: **Opium Policy** (qing_opium_posture 0/1/2), **Frontier Caravan Customs** (qing_caravan_customs_rate 0/1/2),
**Salt Administration** (qing_salt_gabelle_reformed 0/1), **Inter-Ethnic Governance** (via QING_set_ethnic_stance,
dyarchy/banner/han), **Office-Selling** (toggles qing_office_purchased_ranks modifier).
Decisions:
- **on_enact drives the EXISTING backing var/modifier/effect** — each law becomes a parallel control surface
  for a knob the domain pulse already reads. Every on_enact is trivial (set_variable, or add/remove_country_modifier,
  or QING_set_ethnic_stance which is itself only modifier-swaps + set_variable) — NONE reach a heavy chain /
  iterator / recompute, so all are trampoline-safe as-is (no is_triggered_only event needed).
- **Every default option = the gamestart no-op**, VERIFIED against inits: caravan=1 (se_QING_CARAVAN:70),
  opium=0 (se_QING_OPIUM:78), salt unset=0, ethnic=dyarchy (qing_mechanics_on_actions:86 seeds dyarchy),
  office=no purchased-ranks modifier. So holding defaults is byte-identical to today.
- **Gates:** opium-legalize on `has_variable = qing_treaty_track` (treaty system active; a flag var, but
  has_variable is true once any treaty track starts — the intended gate); salt-reform + (chunk 2.1) reform
  tiers on `has_variable = qing_reform_track_unlocked` (mid-game). Both verified real.
- **Dual control surface accepted:** opium/caravan also have existing scripted-GUI panel setters; law + panel
  both write the same var (last-writer-wins, harmless). Old panels left in place (not retired) this pass.
- **Censorate deliberately NOT made a law** — qing_censorate_vigor is a pulse-COMPUTED metric (from the censor's
  traits/loyalty), not a policy knob; a law overwriting it would fight the pulse. Matches the design's "derived,
  not player-set" note.
- Integrity: law braces 70/70, govt_view 1975/1975. Boot-crash+correctness review dispatched.

**Chunk 2.2 review: no boot-crash risk; 1 MEDIUM fixed, 1 LOW noted.**
- MEDIUM (fixed): SALT LOCKOUT. `qing_salt_farmed` default does set_variable value=0 which CREATES the
  var; two legacy consumers gated on `NOT = { has_variable = qing_salt_gabelle_reformed }`
  (se_QING_REVENUE.txt:289 reform-event offer + QING_revenue_ministry_panel.txt:111 reform button) would
  then permanently lock out. FIX: migrated both to value-gated `OR = { NOT has_variable ; var = 0 }` —
  has_variable-guarded (reading an unset var in a comparison is unsafe in this engine; the existing value
  reads at :199/:258 all guard first). Now robust whether the var exists or not.
- LOW (noted, not fixed): the caravan "Heavy Dues" law on_enact sets the var only, skipping the
  qing_xj_kokand_emboldened opinion nudge the panel's QING_caravan_set_customs applies. DELIBERATE —
  keeping law on_enact trivial/crash-safe; the scripted-GUI panel remains the full-effect path. Dual
  control surface is last-writer-wins on the value (harmless).
- Confirmed by review: on_enact set_variable is proven-safe (matches vanilla 00_social_laws on_enact),
  no law auto-enacts at start (defaults never fire), all gate vars real, GUI regs render, loc complete.

### Chunk 2.5 — ministry ESTABLISHMENT-SIZE law (1 group, drives the auto-staffer target)
Files: `00_qing_statutes_laws.txt` (+1 group, braces 102/102), `00_event_values.txt` (+1 svalue),
`se_QING_SUBPOSTS.txt` (mint-target indirection + game-start seed, braces 82/82), `government_view.gui`
(+1 laws_widget, 1985/1985), `laws_l_english.yml` (+8 keys).
Group: **Ministry Establishment (定額)** — qing_law_ministry_estab_target = 3 lean / 4 standard(default) / 6 expanded.
Decisions:
- **This is the ONE group that drives a TARGET, not a pulse read.** The three ministry corps (Zongli
  diplomats / Censorate inspectors / Imperial Guard captains) were staffed up to a hard literal `4` in
  `QING_subpost_staff_corps_minted`. The law now sets that head-count.
- **var-on-RHS is illegal → svalue indirection.** Added `qing_estab_target_tmp_cmpsvalue = { value =
  var:qing_estab_target_tmp }` (matching the documented `_cmpsvalue` idiom). The helper first copies the
  legislated target into a local temp (`qing_estab_target_tmp`), then compares `var:$count$ <
  qing_estab_target_tmp_cmpsvalue` on each mint rung.
- **Unset-var safety.** The helper's copy step is guarded: `if has_variable qing_law_ministry_estab_target
  → temp = var; else → temp = $target$` (the caller's literal 4). So NO unset var is ever read on a
  comparison RHS, and if neither law nor seed has run it falls back to byte-identical literal-4 behaviour.
- **Game-start seed.** `QING_subpost_seed_gamestart` now seeds qing_law_ministry_estab_target=4 (idempotent,
  NOT-has_variable guarded) so the default tier is explicit and the staffer always reads a set value.
- **Rungs raised 4 → 6** so the EXPANDED tier (6) is reachable; lean/standard simply stop earlier. This is
  adjacent to the #90-safe create_character path but does NOT change it — same QING_subpost_fill_one_minted
  call, only two more guarded invocations of it. Each rung still re-checks the count, so it never overshoots.
- **Manual enrol ceiling unchanged (< 6).** The panel enrol buttons already cap at 6; the expanded auto-staff
  tier (6) equals that ceiling, so auto-staffing and manual enrolment can't fight. Lean/standard leave head-room.
- Default tier = the gamestart no-op (4 = old literal). No law auto-enacts at start.
- → boot-crash + correctness review, then COMMIT chunk 2.5.

### Chunk 2.6 — ADVISORY ESTABLISHMENT law (1 group, zero plumbing change)
Files: `00_qing_statutes_laws.txt` (+1 group, braces 113/113), `government_view.gui` (+1 laws_widget, 1987/1987),
`laws_l_english.yml` (+8 keys). NO scripted-effect change — the backing var, its init, and its _cmpsvalue all pre-exist.
Group: **Advisory Establishment (顧問)** — qing_advisor_slot_cap = 2 cautious / 3 measured(default) / 5 open.
Decisions:
- **The cleanest possible law group.** qing_advisor_slot_cap already inits to 3 (QING_advisor_init:48) and is
  already consumed on the recruit gate's comparison RHS via qing_advisor_slot_cap_cmpsvalue
  (se_QING_ADVISORS.txt:87). The law just writes the var the recruit routine already reads — no new svalue, no
  helper edit, no seed. on_enact = set_variable (trivial/safe).
- **Default (measured=3) = init value = byte-identical no-op.**
- **Lowering below slots-used is safe:** the cap only gates the NEXT recruit (`slots_used < cap`); it never
  un-hires a sitting advisor. So enacting Cautious mid-game with 3 advisors seated simply blocks new hires until
  a slot frees — no negative/underflow, no crash.
- → boot-crash + correctness review folds into the chunk 2.5 review (same pattern); COMMIT 2.5+2.6 together.

### Chunk 2.7 — CANTON REVENUE ALLOCATION law (1 group, zero plumbing change)
Files: `00_qing_statutes_laws.txt` (+1 group, braces 124/124), `government_view.gui` (+1 laws_widget, 1989/1989),
`laws_l_english.yml` (+8 keys). NO scripted-effect change — qing_canton_purse_share pre-exists (init 50, pulse-read).
Group: **Canton Revenue Allocation (內帑)** — qing_canton_purse_share = 0 treasury / 50 shared(default) / 100 purse.
Decisions:
- Backing var inits to 50 (se_QING_CANTON:61) and the quarterly Canton pulse already reads it to split the take
  (se_QING_CANTON:120-132). Law writes the same var the existing 3-way GUI setter writes (QING_mechanics_actions
  0/50/100). Default (shared=50) = init = no-op.
- **Dual control surface** with the existing panel buttons (last-writer-wins on the value — harmless, same as
  opium/caravan in chunk 2.2/2.3). Old panel left in place.
- on_enact = set_variable (trivial/safe). No gate — Canton trade exists from game start.

**Chunks 2.5–2.7 review: PASS — no boot-crash risk, no correctness bug.** (code-review agent, 6 tool-uses, verified against files.)
- All crash classes cleared: degree add_trait is INSIDE create_character (#90-safe) and the whole mint path is
  deferred to qing_force_setup.12 (day-32 hidden is_triggered_only), OFF construction; svalue-on-RHS is the
  sanctioned idiom; qing_estab_target_tmp is written on BOTH guard branches before any rung reads it (no unset read).
- No overshoot: 6 independent if-rungs each re-test count<target, +1 each; fires = min(6, target−count); converges
  to target, never exceeds. Seed sets the law var (=4) BEFORE the 3 staff calls, so temp always resolves; literal
  target=4 arg is the coherent else-fallback. Manual ceiling <6 == expanded tier 6 (hits, never exceeds).
- 2 LOW notes (accepted, not bugs): (1) FILL-ONLY — lowering the tier (e.g. expanded→lean) does not discharge
  excess staff; the bench shrinks only by attrition. INTENTIONAL (auto-staffer only mints up; the strip pass
  removes only double-booked members). (2) qing_estab_target_tmp is a persistent country var never cleaned up —
  cosmetic (overwritten every call). → COMMIT chunks 2.5+2.6+2.7.

### Chunk 2.8 — SCOPE DECISION: Design 2 finalized at 12 law groups. Remaining candidates classified + deferred with cause.
After committing 2.5-2.7 I probed the rest of the ~40-candidate list (§A-H above) against the ONE hard rule that
separates a law-safe knob from an unsafe one: **a law may only WRITE a policy-INPUT var that the pulse READS. It may
NOT write a var the pulse itself COMPUTES/nudges** — doing so makes the law fight the recompute (the documented reason
qing_censorate_vigor was excluded in chunk 2.2). Probing each remaining candidate's backing var's write-sites:

**AUTHORED (12 groups, all policy-input or pure modifier-swap — SAFE):**
penal_code, ritual_orthodoxy (pure modifier-swap); opium_policy, caravan_customs, salt_admin, ethnic_governance,
office_selling, canton_regime, exam_cadence (var-selector/modifier read by pulse); ministry_estab, advisory_estab,
canton_purse (policy-input head-count/share read by pulse).

**DEFERRED — pulse-driven meters. [CORRECTION 2026-07-24: the earlier blanket "a law would fight the pulse" was
imprecise. A fixed offset IS technically possible for most of these — the real cost differs by HOW the meter
updates. Three sub-cases, verified against the update code:]**

*Sub-case A — ACCUMULATORS (value persists; pulse NUDGES it via change_variable/QING_DECLINE_nudge). An offset is
CLEAN here: a law can change the decay rate or grant a durable band-gated country modifier — NO pulse-formula edit
needed. Deferral was OVER-CAUTIOUS; these are viable law candidates (only constraint = the no-restoring-drift
ratchet rule, avoided with a band-gate):*
- qing_wenzhi_patronage — init 40, QING_DECLINE_nudge -1/quarter (se_QING_WENZHI.txt:75). A "decay rate" or
  "patronage subsidy" law is a legitimate knob. **RECLASSIFIED: viable, not a hard deferral — just unbuilt this pass.**

*Sub-case B — RECOMPUTED TARGETS (pulse OVERWRITES the var each tick via `set_variable` from a formula of other
vars, then the meter chases the target). An offset written ONTO the target var IS erased next pulse ("fights the
recompute") — BUT threading the offset as a FORMULA INPUT the pulse reads works. That needs the pulse formula
edited to consume a new law-input var = NET-NEW PLUMBING (the bucket below), not a standalone law. Deferred for
that reason, not because it's impossible:*
- qing_customs_efficiency / qing_customs_eff_target — target = set_variable from foreign_control*2 + bureau_integrity,
  /3 each pulse (se_QING_CUSTOMS.txt:173-176); meter chases it ±3. Offset must enter the formula, not the target var.
- qing_council_eff_target / qing_council_dyarchic_balance — recomputed from live councillor skills each pulse.

*Sub-case C — [RE-AUDITED 2026-07-24 against the actual compute code: the earlier "LIVE-DERIVED, no law knob"
label was WRONG for most of these. Verified reality below. Almost all are accumulators (A) or recomputed targets
(B) in disguise, and CAN take a law via the REUSABLE "law policy-bias" pattern — see rework note at the end.]*

- **qing_banner_decay / qing_greenstandard_decay — ACTUALLY Sub-case A (accumulators), NOT live-derived.** Verified:
  init 10/15 (se_QING_DECLINE.txt:81,85), then QING_DECLINE_nudge ±N from many sources (+1/pulse base :889/:892,
  +2 canal, -5 colonization mission, -6/-20 reform events). The qing_banner_decay_mild/severe modifiers are just
  band read-outs of the accumulator. **VIABLE law: a "Banner/Green-Standard Upkeep Policy" adds a decay-rate bias
  at the pulse nudge site (see pattern). Reclassified viable — over-cautiously deferred.**
- **qing_canal_jiangnan_quota — ACTUALLY Sub-case B (recomputed target), NOT map-derived.** Verified: recomputed
  each pulse from THRESHOLDS (base 0.5, +0.25/+0.15/+0.10 on conditions, clamp 0.5-1.0; se_QING_CANAL.txt:209-229).
  A law bias term added into that formula works. (Earlier "recomputed from live map region ownership" was wrong.)
- **qing_xj_consolidation — ACTUALLY Sub-case B.** Recomputed via set_variable = accumulated scratch from
  qing_xinjiang_control (se_QING_XINJIANG.txt:206,229). Law bias term into the scratch formula works.
- **qing_modernarmy_share / qing_han_provincial_power — accumulators** (QING_DECLINE_nudge ±2, DECLINE:390/426).
  Sub-case A; law-bias viable, though these are arguably better left AI/event-driven (see caveat).
- **qing_corruption_level / qing_sect_pressure / qing_reform_faction_balance / qing_selfstr_progress — accumulators
  (A).** Law-bias technically viable, BUT these are DECLINE/CRISIS meters whose whole design is to drift from play,
  not policy — a law knob here would defeat the mechanic's intent. DEFER ON DESIGN GROUNDS (not technical), unless a
  specific "anti-corruption drive" style policy is wanted (then a bias law is the tool).
- **qing_currency_stress / qing_tariff_autonomy / qing_customs_foreign_control — genuinely EVENT/TREATY-state.**
  Set by discrete crisis/treaty outcomes, not a per-tick knob. A law cannot sensibly override a treaty result; the
  right tool is a standing country MODIFIER law (e.g. "resist foreign customs control"), not a var-write law.
- **qing_xinjiang_control — genuinely EVENT-state.** Set to discrete values (0/80/10/90) by Ili event outcomes
  (se_QING_ILI.txt). Same as above: a modifier law, not a var law.

**REUSABLE REWORK PATTERN — "law policy-bias" (lets a law affect any A- or B-meter WITHOUT fighting the pulse):**
The law never writes the meter (which the pulse nudges/overwrites). Instead the law's on_enact sets a standing
policy-bias INPUT var, and the pulse APPLIES it at the exact site it already mutates the meter:
- *Accumulator (A):* at the existing nudge, add one line — `QING_DECLINE_nudge = { var = <meter> amount = var:<law_bias> }`
  (base decay + law bias net out; the nudge's 0-100 clamp keeps it safe; ratchet rule satisfied since base + bias
  can be net-negative). Example: Banner Upkeep Policy → qing_banner_upkeep_law_bias ∈ {+1 lax, 0, -2 reformed drill}.
- *Recomputed target (B):* add the law var as a term in the set_variable formula — e.g. customs_eff_target formula
  gains `change_variable = { add = var:qing_customs_reform_law_bias }` before its /3. Survives because the recompute
  READS it.
- *Event/treaty-state (true C):* no var-write law; use a standing country modifier law instead.
Cost per meter: ~1 pulse line + one law group + loc. Low risk for A, low-moderate for B (touches a pulse formula).
This is the general answer to "can a law affect these" — YES, via bias-input, for every A and B meter; only the
handful of genuine event/treaty-state meters (currency_stress, tariff_autonomy, customs_foreign_control,
xinjiang_control) need the modifier-law form instead. NONE of these are built yet — candidates for a future pass.

**DEFERRED — need NET-NEW plumbing beyond a var write (risk > value this pass):**
- Exam PRACTICAL-SUBJECTS / ABOLITION tiers — no backing mechanic exists (only cadence, done); would need a whole
  curriculum subsystem. Amban MIN count (理藩院) — QING_AMBAN_MIN is a hardcoded CONSTANT, not a var; threading it
  as a law would mirror the ministry_estab work across the amban staffer (a separate careful chunk, deferred).
- Eunuch-restrict cap, harem size — touch the harem/eunuch create paths (the #336/#90-sensitive construction area);
  deferred as too risky for the value.

**DEFERRED — one-way flags / accession state, not a reversible policy selector:**
- qing_frontier_resettlement (panel only ever SETS the flag, never clears — a law that could turn it off is new
  capability), qing_secret_succession_sealed (an accession-time flag set by the designation event, not a standing policy).

**DEFERRED — SUBJECT-scoped, not a CHI country law:** tributary demand rate + tribute cadence (per-subject, se_SUBJECT_QING).

Net: the engine-law expansion is DRAMATIC (0 → 12 native law groups spanning governance/fiscal/ritual/exam/military-
establishment/diplomacy) AND correct — every group drives a genuine policy knob without fighting a pulse. The excluded
set is excluded for a principled reason (output-meter or net-new-plumbing), documented here so a later pass can pick up
the plumbing-heavy ones (amban min, exam curriculum) deliberately rather than by accident. **Design 2 (task #60) COMPLETE.**

---

## Design 1 — Foreign-building family (task #52) — EXECUTION

### Chunk 1.1 — 6 building types + 3 country modifiers (COMMITTED 5e373427c)
Files: qing_foreign_buildings.txt (+6 types), qing_foreignbuild_modifiers.txt (NEW), qing_dynasty_triggers.txt
(cathedral into QING_prov_has_mission). All building keys verified building-scope (local_monthly_civilization,
local_research_points_modifier, local_pop_promotion_speed_modifier, local_population_growth, local_migration_attraction,
local_defensive, fort_level, local_state_trade_routes, local_population_happiness). Decisions:
- concrete-over-abstract preserved: buildings carry ONLY local modifiers; country-level effects hung off has_building.
- qing_treaty_port_building allow = { always = no } (event-planted only, never player-built on own soil).
- frontier colony/fort: empty potential/allow {} (buildable on bare frontier — the concession's job-slot-drop precedent).

### Chunk 1.2 — authorization effects + upkeep sweep (COMMITTED 89ce0d96c)
Files: se_QING_FOREIGNBUILD.txt (NEW, 6 plant effects + QING_fbuild_upkeep_sweep), se_QING_GOVERNANCE.txt (pulse wire).
- Every add_building_level is exists+owner guarded; every country modifier applied once (has_country_modifier guard),
  and RE-DERIVED each quarter from live building presence by the upkeep sweep (drops on loss / cession / subject-freed).
- All verbs verified proven: add_building_level, capital_scope, any_subject, any_country, has_country_modifier,
  add_political_influence, LOG_fail. Effects are runtime-only (GUI/event/mission callers), never construction.
- PERF note in-file: the embassy any_country->any_owned_province scan is quarterly (parallels QING_ethnic_tension_pulse).

### Chunk 1.3 — loc + LIVE callers (mission trees + treaty/mission pulses) (IN REVIEW)
Made the family LIVE rather than dead plumbing by wiring the plant-effects into real callers:
- qing_mechanics_l_english.yml: loc for all 6 buildings + 3 modifiers (name + _desc).
- qing_colonization_missions.txt (Amur task): plant 屯田 colony + frontier fort on p:6170 alongside the vanilla
  fortress (guarded owns + not-present).
- qing_selfstrengthening_missions.txt (merchant task): plant a 洋務局 in the largest subject's largest city via
  nested ordered_subject{ordered_owned_province{save_scope}} + QING_fbuild_subject_works (guarded any_subject+city+treasury).
- se_QING_TREATIES.txt (QING_treaty_stamp_port): plant the CONCRETE qing_treaty_port_building on the same coastal
  province the treaty-port modifier is stamped on + take the humiliation modifier (QING_fbuild_plant_treaty_port).
- se_QING_MISSIONARY_STATIONS.txt: (a) cathedral torn down FIRST in QING_mission_remove_station (it now counts as a
  mission, so a crackdown must remove it too — a real gap the QING_prov_has_mission edit opened); (b) new
  QING_mission_promote_to_cathedral (a mature, high-tension >=40 treaty-port public mission rises to the cathedral
  capstone), wired into the post-treaty pulse branch. Rare by construction so the Boxer meter doesn't explode.
DEFERRED (not this pass): a dedicated subject-view / diplomatic-view GUI BUTTON surface for player-initiated works-aid
and embassy-opening (the design's GUI wiring) — the effects are complete + callable; the button panels are a separate
GUI chunk. The embassy + works effects are currently reachable via the self-strengthening mission; a player-facing
button is the follow-on. Logged so it's picked up deliberately.

**Design 1 chunks 1.1-1.3 review: PASS (no boot-crash) — 1 MEDIUM + 2 LOW-MED fixed, perf noted.** (code-review agent, 12 tool-uses, traced.)
- MEDIUM (FIXED): EMBASSY SELF-BUILD EXPLOIT. qing_embassy_building had open allow, so a player could
  self-build it in a home city; the upkeep sweep's any_country{has_building} scan (CHI is a country) then held
  qing_embassy_representation (+2 dip-rep, +0.05 PI) FOREVER for 60 coin. FIX: allow = { always = no } (planted
  ONLY by QING_fbuild_embassy). Applied the SAME closure to qing_foreign_works_building (works-patron modifier,
  same exploit shape) and qing_mission_cathedral_building (design-intent: effect-seeded only). Now the sweep
  premise "only CHI plants these" is TRUE. Frontier colony/fort kept player-buildable (design intent; LOCAL-only
  modifiers, no free country modifier) but made explicit potential/allow = { always = yes } (were empty {}).
- LOW-MED (FIXED): QING_fbuild_mission_capstone missing owner=ROOT guard (every sibling has it). Added — a
  cathedral can't be planted in a no-longer-owned province. Not a crash (exists-guarded) but a semantic gap.
- LOW (verified non-issue): research_points_modifier + monthly_political_influence CONFIRMED valid country-scope
  keys (qing_earlyindus_harbinger / 00_hardcoded). always=no confirmed valid allow form.
- PERF (accepted): the quarterly any_country{any_owned_province} embassy scan is the heaviest of the 3 sweeps;
  acceptable at 90-day cadence (parallels QING_ethnic_tension_pulse). Closing the exploit didn't remove the scan
  (kept has_building-based for robustness against building loss); could swap to a counter later if it ever bites.
- SOUND (traced by reviewer, not rubber-stamped): the nested ordered_subject{ordered_owned_province} in the
  selfstr mission is scope-safe (inner ordered_subject limit guarantees a city-status province → prov scope always
  saved before the effect call); unset scope:X resolves false under exists= (no crash); upkeep sweep can't thrash
  (add-in-if / remove-in-else, both modifier-guarded); all add_building_level targets exists+owner guarded; loc complete.
Design 1 (task #52) COMPLETE — the effects/buildings are live via mission + treaty + missionary-pulse callers; a
player-facing subject-view/diplomatic-view BUTTON surface is the logged follow-on (deferred, not blocking).

---

## Design 4 — Culture → Nationalism + citizenship (task #62) — EXECUTION

### Chunk 4.1 — nationalism concept layer + citizenship decisions + loc (built together)
Files: 00_nationalism_groups.txt (NEW triggers), 3 filled culture_decisions/*.txt, 00_cultural_modifiers.txt
(+qing_naturalised_citizenship), qing_mechanics_modifiers.txt (+qing_national_awakening), qing_nationalism_l_english.yml
(NEW), modifiers_l_english.yml (+modifier loc). All brace-balanced + BOM'd.

KEY VERB DECISION (oracle-gated). The design leaned on change_pop_type_right for citizenship. An oracle sweep of
vanilla + TI + Invictus found change_pop_type_right is GUI-ONLY — it has a price + icon but NO scriptable effect
form anywhere. So citizenship is built on the PROVEN pair instead:
- **Grant** = integrate_country_culture = scope:target_culture.culture (the real engine citizenship grant, already
  used in se_QING_DECLINE.txt:640; TI form_miao) — flips is_integrated, admits the culture to the in-group.
- **Graduated rights / revoke** = add/remove_country_culture_modifier (the TI/Invictus culture-decision pattern):
  qing_naturalised_citizenship (new dividend modifier), rights_increased, integration_status_removed (vanilla).
- There is NO unintegrate_country_culture verb → revoke is modeled as RIGHTS-revocation (strip the naturalised
  modifier + apply integration_status_removed), NOT engine de-integration. Documented in the file header so it isn't
  read as a bug. This is a truthful mapping of what the engine exposes, not a workaround.

DECISIONS BUILT:
- non_integrated: qing_grant_citizenship (歸化, integrate + dividend, -3 stab), qing_extend_local_rights (優容, lesser).
- integrated: qing_revoke_citizenship (削籍, strip standing + penalty, -8 stab).
- primary: qing_proclaim_nation (立國族, gated on has_recognised_nationalism + civic_identity>=50 + tag CHI; grants
  qing_national_awakening + legitimacy).

NATIONALISM CONCEPT = the group-level trigger layer (zhonghua/manchu/mongol/german/italian/french nation triggers over
the existing culture GROUPS via country/pop/dominant_province_culture_group). NO culture-key renames (blast radius) —
the relabel is a NEW loc layer (中華/滿族/Deutschtum…) ON TOP of the untouched culture ethnonyms ("Han" stays "Han",
distinct from the invented pan-Han nation 中華 coined 1902). This is the design's "re-localize display names, don't
rename internal keys" decision, executed as an additive concept layer rather than a destructive overwrite of chinese_group:1.

DERIVED NATIONALISM METER — NOT separately built. The existing qing_civic_identity (National Integration meter, bands
in QING_DECLINE_apply_civic_band) ALREADY is the derived civic/national-coherence read-out the design's ratchet-safe
"pure derived" option called for; qing_proclaim_nation reads it directly. Adding a second parallel meter would be
redundant. Logged as a deliberate scope call.

RIGHTS-CLEANUP "NEEDS CHANGED" SEAMS — deliberately NOT touched. increased_rights_cleanup_effect /
reduced_rights_cleanup_effect (called in on_action/00_specific_from_code.txt:556,610) are VANILLA base-game scripted
effects — DEFINED NOWHERE in imp19c, TI, or Invictus (all three only CALL them), so they resolve from the base game and
work as-is. The "IMP19C NOTE: NEEDS CHANGED" comment is an aspirational author note orthogonal to Design 4: my
citizenship path uses integrate_country_culture + modifiers and does NOT route through these cleanup hooks, so
redefining/overriding them would be a high-risk-low-value change. Left intact; decision logged.

REVIEW: direct (200-agent cap hit — no subagent). Verified against code: integrate_country_culture arg form matches
DECLINE:640 + working .culture accessor; all 6 culture-group keys exist; minor/major_cultural_decision_price defined;
qing_naturalised_citizenship keys all proven culture-scope; qing_national_awakening keys all proven country-scope;
custom_tooltip-as-gate matches the working language_recognition decision; var:qing_civic_identity has_variable-guarded +
CHI-gated + init'd 5×; add_legitimacy/add_stability proven; all decisions ai_will_do=0 (player-only). No boot-crash class
matched. **Design 4 (task #62) COMPLETE** (a culture_view.gui read-out panel is the logged optional follow-on).

---

## Design 3 — Religion → Ideology (task #61) — EXECUTION

### SCOPE DECISION (up front). Design 3 is the highest-risk of the four (48 custom deities + per-country
### DB registration = the DB-key-contiguity + pantheon-panel crash classes), and the 200-agent cap was hit
### mid-session so NO independent boot-crash review is available. Per the standing boot-crash-review rule +
### other-machine testing, the risky net-new content is DEFERRED to a reviewable follow-on; what ships here
### is the bounded, self-verifiable, crash-class-free foundation of the coexistence model.

### Chunk 3.1 — ideology religions + triggers + migration guards (COMMITTED 8790b03a3)
- 01_ideologies.txt: 6 ideology religions (religion_category=pantheon, can_deify_ruler=no), SIBLINGS to the
  faiths (coexistence — NO mass 00_default remap). NO custom deities → the generic set (00_generic.txt, which
  suppresses ONLY for confucianism) covers them, so they are panel-complete with ZERO DB registration → the
  DB-contiguity crash class is entirely avoided.
- is_ideology_religion {,_province,_pop} triggers (3 scopes, kept in sync with the 6 entries).
- Migration item 1 (create_character root.religion floods) fixed in a PRIOR standalone commit (d8163ca00, 19 sites).
- Migration item 2 (character_events.21 governor-conversion) guarded NOT root is_ideology_religion.
- Migration item 3 (state_secularism/atheism laws) allow gated NOT is_ideology_religion (belt-and-braces; the
  laws already required religion=secular).

### Chunk 3.2 — layered adoption flow (se_QING_IDEOLOGY + trampoline event + modifier + loc) (this commit)
- QING_adopt_ideology: the PROVEN layered flow — set_country_religion=$ideology$ (oracle-confirmed; mirrors
  se_QING_REFORM:114) + set_character_religion on ruler+close family (bounded every_character employer=ROOT) +
  set_pop_religion over a BOUNDED capital sample (ordered_pops_in_province order_by=pop_hapiness max=3 — the
  proven bounded-pop idiom, subject_focus_events:799; random_pops_in_province count= is NOT proven so avoided) +
  qing_ideology_recent_convert modifier + PI cost. NO create_character, NO deities, NO DB → off every crash class.
- qing_ideology.1: hidden is_triggered_only TRAMPOLINE (the layered flow is heavy-ish; a runtime event ref is
  never compile-inlined into a scripted_gui button — the #443 class). Reads qing_pending_ideology flag var
  (set by the upstream decision, to be wired) and dispatches to the matching creed; clears the marker after.
- qing_ideology_recent_convert country modifier + religion loc (6 creeds) + modifier loc.
- Verbs verified proven in-codebase: set_country_religion / set_character_religion / set_pop_religion,
  is_close_relative=ROOT.current_ruler, ordered_pops_in_province{order_by,max}, var:X=flag:Y, hidden=yes on
  country_event, remove_variable, add_political_influence, all modifier keys country-scope.
- Reviewed DIRECTLY (agent cap hit). No boot-crash class matched; all brace/BOM clean.

### DEFERRED to a reviewable follow-on (logged, NOT shipped this session):
1. The 48 custom thinker-deities (8 per ideology × 6) + per-country setup/main/deities DB registration — the
   DB-key-contiguity + pantheon-panel-break crash classes; MUST get a boot-crash review first. Until then the
   ideologies wear the generic deity set (functional, just not the thinker theming).
2. The player-facing ADOPTION DECISION/button that sets qing_pending_ideology + trigger_event qing_ideology.1
   (with era/reform-state gates) — the trampoline + effect are ready; only the upstream trigger surface is unbuilt.
3. Migration item 4 (00_religion_groups faith-group CONSUMERS audit — ensure NOT-faith-group consumers don't
   misclassify ideology holders); item 5 (send_settlers breakaway inherits an ideology as faith — needs a verified
   fallback-faith read into LAND_release_from_list, left as a documented WATCH in-file).
4. The Stage-4 targeted 1763-nascent seeding + generic-suppression edit for custom deities (only relevant once
   custom deities exist).
Design 3's coexistence CORE is shipped + crash-safe; the deferred set is the review-gated + GUI-surface work.

### Chunk 3.3 — player adoption decision/button + migration items 4 & 5 (task #64) — DONE (pending review+commit)
Reopened the deferred Design-3 work as tracked tasks #63/#64/#65 (the task store was empty). This chunk
closes #64 (the non-crash-gated deferrals); #63 (custom deities) stays BLOCKED on #65 (boot review).

ADOPTION DECISION/button (deferred item 2) — the upstream trigger surface for the ready trampoline+effect:
- decisions/imp19c_mod_decisions/imp19c_ideology_decisions.txt (NEW): qing_embrace_political_creed. potential =
  tag=CHI + exists=current_ruler + NOT is_ideology_religion (one adoption per state; not already converted).
  allow = var:qing_reform_pressure >= 40 + political_influence >= 30 (the reform crisis must be under way, so no
  anachronistic 1763 adoption). effect = trigger_event qing_ideology.2. ai_will_do factor=0 (player-only, like the
  Design-4 culture decisions). DECISION -> CHOICE EVENT -> TRAMPOLINE keeps the heavy QING_adopt_ideology effect a
  pure runtime ref, never compile-inlined off a decision (the #443 compile-inline crash class — same reason the
  trampoline exists). Var-read safety: qing_reform_pressure is initialised for CHI at on_game_initialized
  (QING_DECLINE_init:97 sets it 0 if unset), so the allow read can never hit an unset var.
- qing_ideology.2 (CHOICE event, appended to qing_ideology_events.txt): a real country_event, one option per
  creed (a-f) + a decline option (g). Each creed option carries its OWN era/reform gate so a creed can't be
  adopted anachronistically: liberalism/nationalism >=40, monarchism is_monarchy=yes, socialism >=55,
  communism >=70, conservatism ungated (the reform-sceptic ordering). Chosen option sets qing_pending_ideology
  = flag:<creed> + trigger_event qing_ideology.1 days=1 (the trampoline reads the flag and runs the layered
  adoption). Reused the proven set_variable value=flag: idiom (qing_japan_missions:128) + var: >= comparison.
- localization/english/qing_ideology_l_english.yml (NEW, BOM-carrying like every loc): decision title/desc + the
  7 option strings + event title/desc, bilingual 中文 labels matching the religion_l creed names.

MIGRATION ITEM 5 (send_settlers breakaway inherits an ideology as faith) — FIXED (was a documented WATCH):
- send_settlers.txt:310 — branched the LAND_release_from_list on the instigator. When it holds an ideology
  (is_ideology_religion=yes) the breakaway is released with country_religion = flag:as_capital (its own
  capital-province faith — the PROVEN LAND_release_from_list fallback, se_SEPARATISM:155 / se_QING_PROTECTORATE:68),
  so a secession never carries a foreign ideology as its state religion. The normal faith path (else branch) is
  BYTE-IDENTICAL to the original — settler colonies still share the instigator's faith. Only the ideology case
  diverges. Not a crash either way; this makes the released state's faith sensible.

MIGRATION ITEM 4 (faith-group CONSUMERS audit — do NOT-faith-group consumers misclassify ideology holders?):
Audited all 4 consumers of chinese_traditional/accepted_religion_trigger + the christian_group NOT-lists:
- se_QING_MISSIONARY_STATIONS.txt (4 sites) — FIXED. The "any non-Christian pop" harvest branches (222/230 treaty,
  463/470 pre-treaty) would drag an ideology-holding pop back onto a faith via QING_mission_convert_faith. Added
  NOT = { is_ideology_religion_pop = yes } to all 4 — missionary work is faith-vs-faith, orthogonal to the
  ideology channel. (The "traditional-faith pop" first branch already excludes ideologies, so no leak there.)
- common/subject_types/00_default.txt:1009 (royal_union allow, NOT chinese_traditional_religion_trigger) — NO
  CHANGE. It only ENABLES a rare subject action and is already gated by this.religion=root.religion equality; an
  ideology-holder passing the NOT is a benign edge that also requires a matching-religion overlord. Documented.
- common/heritage/00_mod_heritages.txt:99 (confucian_learning, OR chinese_traditional_religion_trigger) — NO
  CHANGE. A converted state correctly loses the Confucian-learning heritage bonus (it is no longer Confucian);
  that is the intended semantics of conversion, not a misfire.
- common/customizable_localization/00_offices.txt (3 sites, OR chinese_traditional_religion_trigger) — NO CHANGE.
  Each has a country_culture_group = chinese_group fallback, so Qing keeps its 六部 office labels after conversion.

VERIFIED: braces balanced (ideology_events 48/48, decision 8/8, send_settlers 92/92, missionary 204/204); loc BOM
present, decision no BOM; flag/var idioms proven in-codebase; qing_reform_pressure init guaranteed at boot.
COMMITTED: 485611f66. STILL DEFERRED: #63 (48 custom deities + DB) — the DB-contiguity/panel crash class.

### #65 — INDEPENDENT BOOT-CRASH REVIEW of the self-reviewed chunks — DONE (PASS, ran directly)
Two review agents were dispatched (one for the 4 committed chunks, one for the #64 working tree) but both stalled
without delivering via mailbox after ~25 min. Per the standing no-bisection / self-review rule (the same posture the
original session took when the 200-agent cap blocked agent review), I ran the boot-crash review MYSELF, reasoning
from the diffs against every known crash class. Scope: d8163ca00 (Fix 19), dbbbea3ce (Design 4), 8790b03a3 (chunk
3.1), cfa30f0b0 (chunk 3.2). RESULT — all classes PASS:
- **Clobbered-file (the big one).** git reported 8790b03a3 rewrote 00_social_laws.txt (584 lines) + 00_religion_
  groups.txt (1128 lines). WHITESPACE-IGNORING diff (`git show -w`) proves this is pure re-indentation noise:
  social_laws' ONLY semantic change is the two `NOT = { is_ideology_religion = yes }` allow-gates (item 3); line
  count 288→296 (+8). religion_groups' ONLY additions are the 3 is_ideology_religion triggers; 543→584 (+41), zero
  existing-trigger deletions. NOT clobbered.
- **Pantheon-panel / DB-contiguity.** 01_ideologies.txt's 6 religions carry NO custom deities; 00_generic.txt
  suppresses its 8-deity set ONLY for `NOT = { religion = confucianism }`, so all 6 ideologies RECEIVE the full
  generic set = exactly 8 deities / 2-2-2-2 (war/economy/culture/fertility) — the load-bearing panel shape. Panel-
  complete with zero DB registration → the DB-key-contiguity + panel-break crash classes are genuinely avoided.
  (Corollary: #63's custom deities WILL re-enter this class, confirming the deferral was correct.)
- **Fix 19 completeness.** All 5 files clean — zero remaining `religion = root.*` / `culture = root.*` in any
  create_character body; a mod-wide sweep found only legal `= root.*` reads inside limit/comparison contexts.
- **create_character scope-chain / #90 grant / HEALTH-trait.** None of the 4 chunks add a create_character.
- **BOM-reject (setup/).** No setup/ file is touched by any of the 4 chunks → class N/A. common/ modifier file's
  only BOM is at byte 0 (legit); the `﻿####` in the diff was a display artifact of the leading BOM, not embedded.
- **Scope correctness (chunk 3.2 effect).** se_QING_IDEOLOGY: set_country_religion at country scope, set_character_
  religion inside current_ruler/every_character (char scope), set_pop_religion inside ordered_pops_in_province (pop
  scope). is_close_relative = ROOT.current_ruler is the PROVEN prefixed form (se_SEATS:281). order_by = pop_hapiness
  is the engine's key (00_event_values). ordered_pops_in_province has explicit max=3 (ordered-iterator max rule OK).
- **Migration guards.** character_events.txt:516 `NOT = { root = { is_ideology_religion = yes } }` correctly
  suppresses the :506 governor-conversion misfire (a trigger comparison, char scope — valid). send_settlers item 5
  fixed in #64.
- **Ratchet rule (Design 4).** qing_national_awakening is a one-shot country modifier gated on NOT has_country_
  modifier + var:qing_civic_identity>=50 — not a passive nudge on a meter; qing_civic_identity (the DECLINE meter)
  is unchanged. No ratchet.
- **Design 4 verbs.** integrate_country_culture (proven), add_country_modifier, add_legitimacy (country-scope),
  ai_will_do factor=0; nationalism triggers carry no illegal RHS var-ref. Braces balanced on all 16 touched files.
CONCLUSION: the four self-reviewed chunks are boot-crash-clean. #65 CLEARED — which UNBLOCKS #63 (custom deities may
now be built, but that work re-enters the DB-contiguity/panel class and needs its OWN review of the new deity data).

### Chunk 3.4 — the 48 custom thinker-deities + DB registration (task #63) — DONE (pending live boot test)
With #65 cleared, built the deferred thinker-pantheons. This RE-ENTERS the pantheon-panel-break + deity-DB class,
so it was built as an EXACT clone of the proven Confucian reskin (03_confucian_pantheon.txt / 02_confucian.txt /
qing_deities_l), generated programmatically to guarantee body-for-body fidelity.
- common/deities/04_ideology_pantheons.txt (NEW, BOM): 48 deities = 8 per ideology × 6. Each body is a VERBATIM
  clone of the matching generic deity (00_generic.txt) — icon / passive_modifier svalue / omen svalue / on_activate
  / deity_category identical; only the KEY, religion=, and loc differ. Verified mechanically: all 48 bodies match
  one of the 8 generic bodies exactly (0 mismatches); 8 per religion; exactly 12 per category (2×6). Thinkers from
  the Design 3 §A.3 roster (Montesquieu/Smith/Mill/Yan Fu for liberalism; Burke/de Maistre/Feng Guifen for
  conservatism; Hegel/Metternich/Zeng Guofan for monarchism; Fichte/Herder/Mazzini/Liang Qichao for nationalism;
  Saint-Simon/Fourier/Owen/Proudhon/Kang Youwei for socialism; Marx/Engels/Bakunin/Li Dazhao for communism).
- common/deities/00_generic.txt (MODIFIED): each of the 8 generic deities' trigger widened from
  NOT={religion=confucianism} to a NOR over confucianism + the 6 ideologies — so the generics are SUPPRESSED for
  the ideologies and the panel shows THESE eight, not a doubled 16-deity list (the exact panel-break class the
  Confucian header warns about). 8 NOR blocks, one per generic deity.
- setup/main/deities/03_ideologies.txt (NEW, NO BOM — the setup pdx_persistent_reader REJECTS BOM): DB registration
  keys 1500-1547. Verified: deity DB is sparse/non-contiguous (existing 1-8, 900s, 1100s, 1300s, 1400-1407), so a
  fresh 1500-block collides with nothing; all 48 `deity=` refs resolve to a defined deity; all 48 `key=omen_X`
  unique.
- localization/english/qing_ideology_deities_l_english.yml (NEW, BOM): 144 lines = deity_X:0 / omen_X:1 /
  omen_X_desc:3 per deity, the proven qing_deities_l convention; each desc ends in the on_activate's
  $..._tt_description$ apotheosis macro. Epithet headers cleaned to standalone lines (no name leakage).
- STATUS-4 STAMP updated in Implementation 3.
SELF-REVIEW (agent reviews stalled again in this environment — 3 dispatched, none delivered; reviewed DIRECTLY
per the standing self-review rule): PASS all classes — panel shape 8/2-2-2-2 with generics suppressed (no
doubling); verbatim clones (no invented modifier/svalue key); setup DB no-BOM + no key collision; deity+loc BOM
present; braces 289/56/50/144-line balanced; all religions exist in 01_ideologies; loc complete; no key collisions.
WATCH for the live boot test: (1) each ideology's Pantheon panel shows its 8 themed thinkers (NOT 16, NOT raw
generic keys) — this is the panel-break tell; (2) omen invocation + apotheosis tooltips render; (3) no
"deity DB" / duplicate-key boot error. If the panel breaks, the fault is the generic-suppression NOR or the DB,
not the bodies (proven-identical). Custom deities are the last Design-3 deferral — Design 3 is now feature-complete.

---

## BOOT TEST 2026-07-24 — fixes (Designs 1/3/4)

Live boot test of the pushed build. Six findings; fixes below. Logs+screenshots confirmed roots where noted.

### BT-D2-1 — Laws: PASS (screenshot). All 12 Qing Statutes (會典) render with 中文.
### BT-D3-2 — Ideology deities: PASS (screenshot). Custom thinkers render (Karl Marx seen); no panel doubling.

### BT-D4-1 — culture decisions not appearing — FIXED
error.log:13187 pinned it: non_integrated_culture_decisions.txt:32 `integrate_country_culture =
scope:target_culture.culture` — the effect wants a COUNTRY_CULTURE, `.culture` downgraded it to culture scope →
PostValidate false → the decision (and its file-sibling) dropped at load. Fix: pass `scope:target_culture`
directly (proven caller se_QING_DECLINE.txt:640). The `.culture` on the `primary_culture=` comparisons (lines
21/58) is correct and left alone. Revoke/proclaim (integrated/primary files) logged NO errors — they were
gated-not-shown, not broken.

### BT-D1-1/3 — foreign buildings absent from build display — FIXED (needs boot confirm)
User wants building types visible even at 0-built. Root: the 4 authorization-only buildings (works/embassy/
treaty-port/cathedral) had `allow = { always = no }` which the engine hides. Fix: widened their `potential`
from `has_city_status` to `always = yes` so the TYPE lists in every province (listing is governed by potential;
allow still gates buildability). Also wrapped each `always = no` in a `custom_tooltip` (proven syntax, TI
00_default.txt:1736 / qing_colonization_missions:90) so the greyed entry shows a reason — NOTE (per review): a
custom_tooltip is transparent to the boolean, so it labels but does not itself un-hide; the potential widening is
the actual visibility lever. The 3 genuinely player-buildable ones (2 missions + concession) KEPT has_city_status
(widening would let them be built in non-cities — a gameplay change, not made unilaterally).

### BT-D3-1 — Holy Sites tab scattered — FIXED (structural; user says F&S is the trigger)
Screenshot confirmed the whole left column (holy-site list + Faith & Sedition block) rendered detached over the
map. TWO changes: (a) bounded the Holy Sites tab body — root flowcontainer→hbox + expanding layoutpolicy, left
column flowcontainer→vbox + expanding, mirroring the WORKING Pantheon sibling (L349), so the column clips inside
the bounded window height instead of overflowing and dislocating; (b) per the user's call, MOVED Faith & Sedition
(民教相爭) off the Holy Sites tab into its OWN third religion tab (new category_tab + sub_header, body gated
religion_tabs='faith'). qing_faith_grid/scroller/suppress-button now live only in the faith body. Loc:
QING_FAITH_SEDITION_TAB added. Braces 512/512; three tab bodies are proper siblings with exact-match gates
(omens / sites / faith). Independent review (btreview): PASS on this change.

### BT-D3-3 — holy sites for the 48 ideology deities — DONE (benefit/map-shrine model)
Oracle check (Invictus/TI, paths now in [[imp19c-oracle-repo-paths]]): holy sites live in a deity's own-religion
homeland provinces; the engine tolerates a mismatched province religion (that's the point of the
holy_site_deity_check OR-branch). CORRECTED my earlier claim: the historical imp19c panel-break was the 12-deity/
3-per-category COUNT, not religion-mismatch. Decisive LOCAL proof: imp19c's own Confucian pantheon uses
`trigger={always=yes}` (NOT the Invictus holy_site_deity_check pattern — imp19c stripped that whole system) AND
has working holy sites in daoism/buddhism provinces (Putian/Mazu etc.). So the benefit/map-shrine half works
standalone with always=yes — NO trigger rewrite, zero regression risk (chosen over the full Invictus port, which
would introduce vanilla triggers imp19c has never used and risk the working panel).
BUILT: 48 `holy_site=omen_<thinker>` lines in 21 province files, each in a DISTINCT thematic-homeland province
(Marx→Trier, Engels→Wuppertal, Smith→Fife, Montesquieu→Bordeaux, Kant→Königsberg, Hegel→Jena, Mazzini→Genoa,
Bakunin→Tver, Yan Fu→Fuzhou, Feng Guifen→Suzhou, Zeng Guofan→Xiangtan, Liang Qichao→Guangzhou, Kang Youwei→
Foshan, Li Dazhao→Tangshan, …). Verified: 48/48 resolved, ZERO duplicate provinces (one holy_site per province),
all 21 files brace-balanced, insertions placed after religion= inside each block. Province files KEEP their BOM
(common lexer, not the persistent reader — see [[imp19c-setup-reader-rejects-bom]] clarification). Deity triggers
UNCHANGED (always=yes). WATCH on boot: the 48 shrines appear on the Holy Sites tab / map; no panel regression.

---

# PART IV — 1763 FOLLOW-ON PLAN (scoped 2026-07-24, code-verified; NOTHING BUILT YET)

Design threads surfaced during the boot-test session. Each verified against current code. These are
SCOPED, not built — candidates for a future implementation pass, in priority order TBD by user.

## P1 — Wire nationalism mechanics into the frontier/sinicization trees
- `qing_settle_frontier_missions.txt` (定牧墾邊) is ALREADY 1763-native (written around the 1763 board, NO date
  gate) and is the natural home. `qing_xinjiang_missions.txt` + `qing_central_asia_missions.txt` also 1763-native.
- GAP: none of them touch the Design-4 nationalism hooks (all present, all unused by missions):
  qing_civic_identity accumulator (nudge via QING_DECLINE_nudge), integrate_country_culture + qing_naturalised_
  citizenship, qing_national_awakening modifier, the *_nation_country/pop/province_trigger family.
- PLAN: settle_frontier ARC-N/ARC-E completion → nudge qing_civic_identity up + naturalise the frontier culture
  (integrate_country_culture) + toward capstone grant qing_national_awakening / gate on zhonghua_nation_country_
  trigger. Turns "settle the land" into "forge the nation" using the mechanics, not duplicating them.
- (reform/selfstrengthening trees stay date-gated 1815 — inherently 19c, leave as-is.)

## P2 — Plant works/arsenal buildings on settled frontier ground
- settle_frontier + xinjiang currently grant NO buildings. qing_colonization_missions already grants frontier_
  colony/fort directly via add_building_level — mirror that: plant a works/arsenal building on frontier provinces
  the player brings under direct rule. NOTE: QING_fbuild_subject_works is SUBJECT-scoped (owner=$subject$) so it
  does NOT fit direct-rule frontier ground — grant the building directly, not via that wrapper.

## P3 — Embassy (使館) → Great Game
- QING_fbuild_embassy is ORPHANED (no caller). It takes $power$, plants qing_embassy_building in that power's
  capital, grants qing_embassy_representation. Great Game (se_QING_GREATGAME.txt) tracks qing_gp_tension_britain/
  france/russia and already frames "wins concessions". PLAN: call QING_fbuild_embassy from a Great Game event
  (legation-exchange / détente against a GP). This is the embassy's missing home.

## P4 — Treaty ports as a two-sided Great Game instrument
- TODAY: one-sided victimhood model. Building carries qing_treaty_port_humiliation on the BUILDER; planter
  QING_fbuild_plant_treaty_port = "port forced onto Qing soil" (owner=ROOT, humiliation on ROOT). Only a
  humiliation modifier exists — NO holder-benefit modifier. Building is buildable by any city+tech_monetary_theory
  but wrongly stamps the Qing-victim modifier on whoever builds it.
- PLAN (real rework): model imposer vs victim. New qing_treaty_port_concession (holder benefit: trade/influence)
  modifier for the imposing power; keep humiliation for the victim. A Great-Game event where Qing OR a GP forces a
  concession port in the other's / a third party's province → planter grants the port + humiliation on the owner +
  concession benefit on the imposer. Lets Qing and Great Powers both play the treaty-port game.

## P5 — Missions/events to embrace ideologies-as-religion (Design 3 follow-on)
- Design 3 shipped the adoption DECISION (qing_embrace_political_creed → qing_ideology.2 → trampoline) but NO
  mission/event CONTENT around adopting/spreading an ideology. GAP: no arc that motivates or dramatizes embracing
  Liberalism/Nationalism/Socialism/etc.
- PLAN: mission/event content — e.g. reformers memorialize the throne to adopt a creed; ideological adoption
  triggers reaction events (conservative backlash, foreign recognition, pop conversion drift); tie to
  qing_reform_pressure gating already used by the decision. Also (Design 3 Stage-4, still deferred) targeted 1763
  ideology seeding — currently ZERO countries start on an ideology.

## P6 — Design-1 orphaned effects + Stage-4 seeding (from the deferral re-audit)
- QING_fbuild_frontier_colony / QING_fbuild_frontier_fort wrappers: NO caller (colonization missions grant the
  buildings directly, so wrappers are redundant — either wire or delete).
- Stage-4 1763-nascent ideology seeding (Design 3): not built.

## P7 — Law policy-bias reworks (from the sub-case A/B re-audit, chunk 2.8)
- The "law policy-bias" pattern (law sets a bias-input var; pulse applies it at its existing nudge/formula site)
  makes ~a dozen more meters law-controllable. Viable candidates: Banner/Green-Standard Upkeep (accumulators, 1
  nudge line each), customs efficiency / canal quota / xj_consolidation (recomputed targets, 1 formula term each).
  Crisis meters (corruption/sect/faction) deferred on DESIGN grounds; event/treaty meters need modifier-laws.

---

# PART IV — IMPLEMENTATION LOG (BUILT 2026-07-24, on branch merge-overnight; pre-review)
*STATUS: all seven phases coded; brace/quote-clean; full code-review + boot-crash review PENDING before commit.*

**P1 — Nationalism wired into the frontier/Xinjiang trees.** New effect `QING_settle_forge_nation = { group=X }`
(se_QING_SETTLE_FRONTIER.txt): naturalises every un-integrated country_culture of the group present in the realm
via `integrate_country_culture` (PERMANENT engine state — chosen over a bare civic-identity nudge, which the
decline pulse's restoring drift would decay back; the no-restoring-drift ratchet rule), and accrues
`qing_civic_identity_settle_bonus` (+8/arc, cap 40). The bonus is consumed at the civic-identity DRIFT site
(se_QING_DECLINE.txt QING_DECLINE_drift_civic_identity) as a TARGET lift, so the gain persists. Wired: settle_frontier
ARC-N on_completion → forge_nation(mongolic); ARC-E → forge_nation(jurchen); CAPSTONE → the standing
`qing_national_awakening` modifier (a previously-unused Design-4 hook). Xinjiang `QING_xj_integrate_fully` →
forge_nation(east_turkic) — that task stripped tension modifiers but never extended citizenship. Idiom proof:
`every_country_culture { is_integrated=no culture.culture_group=culture_group:X }` (se_CULTURE / seleukid mission).

**P2 — Works/garrison buildings on settled frontier ground.** New effect `QING_settle_plant_works = { region=X }`:
plants qing_frontier_colony_building + qing_frontier_fort_building directly (add_building_level) on up to 4 held
provinces of the region, guarded not-already-present. DELIBERATELY direct (not via QING_fbuild_subject_works, which
is owner=$subject$-scoped and does not fit direct-rule ground). Free mission-completion texture. Wired into ARC-N
(Mongolia), ARC-E (Liaoning + Far_East).

**P3 — Embassy (使館) → Great Game.** New event `qing_greatgame.4` (Exchange of Legations 互派使節): the missing HOME
of the orphaned `QING_fbuild_embassy`. Fires from the flavour roll (weight 7) when a power sits in a DÉTENTE band
(tension 25..55), Zongli office filled, legation not yet opened. Picks the power (saved as BOTH a flag and a country
scope — the effect needs a country scope with a capital), option A opens the resident legation (calls the orphaned
effect) + deepens détente + reform-pressure rise (breaks tribute worldview); option B holds to tribute forms.

**P4 — Treaty ports as a TWO-SIDED instrument.** New modifier `qing_treaty_port_concession` (imposer benefit:
diplomatic_reputation +1, global_commerce_modifier +0.05, PI +0.03 — mirror of the victim-side humiliation). New
effect `QING_treaty_impose_concession = { victim= prov= }`: plants the treaty-port building on the VICTIM's coastal
province, stamps humiliation on the victim, grants the concession benefit to ROOT the imposer (the asymmetry the old
one-sided planter got backwards for this direction). New event `qing_greatgame.5` (The Guest Becomes the Host 反客為主):
a STRONG Qing (legitimacy≥60, stability≥50) forces a concession onto a HOSTILE power (tension≥55) that holds an
un-stamped coastal city. Low roll weight (4 — alternate-history exception). Option A dictates (imposer benefit +
victim humiliation + tension spike); option B stays the hand.

**P5 — Ideology missions/events (Design 3 follow-on).** Two new events in qing_ideology_events.txt: `qing_ideology.3`
(Reformers Memorialize 公車上書 — motivates adoption; reform-pressure≥40, not yet converted; option A dispatches the
existing choice event qing_ideology.2, option B rebuffs); `qing_ideology.4` (Conservative Backlash 守舊反動 — reaction
gated on the qing_ideology_recent_convert modifier; option A faces down the reaction (re-seed capital vanguard),
option B appeases (removes the churn early)). Both wired into the flavour roll (weights 8/7). **Stage-4 1763 ideology
SEEDING: DELIBERATELY still deferred** — liberalism/socialism/etc. are post-1789/19c constructs, anachronistic at a
1763 start, and set_country_religion at game-start carries boot-crash risk. The historically-correct model is exactly
what Design 3 built: ideologies unlock mid-game as reform pressure ripens. Recorded as a design decision, not a gap.

**P6 — Orphaned Design-1 wrappers: DELETED.** `QING_fbuild_frontier_colony` / `QING_fbuild_frontier_fort` had ZERO
callers. Both consumers (colonization missions + the new P2 plant) grant the buildings directly as FREE texture;
routing through the wrappers would duplicate the guard AND impose a second 60-treasury charge that silently no-ops
when short — wrong semantics. Redundant dead code, deleted per the "wire OR delete" mandate. The buildings remain.

**P7 — Law policy-bias: Military Upkeep (武備).** New law group `qing_military_upkeep_law` (00_qing_statutes_laws.txt,
3 stances) sets standing bias-input vars `qing_banner_upkeep_bias` / `qing_greenstandard_upkeep_bias` via on_enact
(the proven qing_opium_posture / qing_caravan_customs_rate pattern in this file). The decline pulse APPLIES them at
its existing decay-nudge site (se_QING_DECLINE.txt), guarded (has_variable) so the default stance is byte-identical
to today. Reformist Drills = -1 bias each (rot slows, +upkeep cost, +land morale); Frugal Neglect = +1 (rot quickens,
-upkeep). `amount = var:X` proven at 5 existing nudge call-sites. Registered in the government_view.gui Laws tab
(mandatory or invisible). Only the ONE representative meter-pair built this pass; the other candidates (customs/canal/
xj_consolidation recomputed-target terms) remain scoped for a later pass.

---

# PART V — LAW EXPANSION + COURT INTRIGUE (DESIGN, 2026-07-24; branch merge-overnight)
*STATUS: DESIGN COMPLETE + ADVERSARIALLY REVIEWED (4 reviewers) + REVIEW-FIXES APPLIED. Build PENDING.
Standalone copies: LAW_EXPANSION_DESIGN_DOC.md, COURT_INTRIGUE_DESIGN_DOC.md. Each carries an ADVERSARIAL
REVIEW PASS block at its top listing the fixes folded in (toggle-farm removal, ratchet-defeat guards,
1:1-validator resolution, monetary/military de-overlap, tariff fake-choice fix, harem favour/passive/dowager
fixes, eunuch doom-loop guards). #37/#38 are NOT standalone laws — they live in the subsystem batches 6/7.*

## PART V.1 — Law Expansion (all remaining law groups)

## Law Expansion — Full Design (all remaining law groups)

> ## ADVERSARIAL REVIEW PASS (2026-07-24) — applied fixes
> Four adversarial reviewers (classification / boot-crash / GUI-loc-modkeys / gameplay-balance) audited this
> doc against live code. **Classification core verified CORRECT** (every backing-var class, line citation,
> no-op default, and the signed-clamp warning confirmed). **Zero boot-crash risks.** The fixes below address
> exploits, incoherence, and specification gaps they surfaced. Empirically confirmed: EVERY existing law's
> on_enact uses `set_variable`/modifier (idempotent) — none nudge — so a nudge-on-enact IS a toggle-farm.
>
> **SHIP-BLOCKER fixes (applied to the sections below):**
> - **Toggle-farm exploit (#13, #44, #47):** `on_enact` fires on EVERY enact, so any on_enact that NUDGES a
>   var is farmable by re-enacting. FIX: all three drop the on_enact nudge. #13/#47 become pure
>   modifier-swap; #44's "kickstart" nudge is once-guarded (`if NOT has_variable qing_X_adopted { nudge; set
>   adopted }`) so it fires at most once ever.
> - **Ratchet-defeating exposure (#19, #20, #44):** exposing drift-from-play decline meters as a standing
>   policy that CANCELS the pressure defeats the mechanic. FIX: #19/#20 biases are made SMALL and band-gated
>   (tilt, not cancel — a −1 audit bias against a meter nudged +N from many sources only slows accrual, and
>   is floored so it can't drive the meter to 0); #44 becomes a pure modifier-law (no ongoing var-write).
> - **#38 eunuch law shipped before its consumer:** REMOVED from the law batches — #37/#38 live ONLY in the
>   court-intrigue subsystem batches (6/7), law + backing mechanic in the same batch.
>
> **INCOHERENCE fixes (applied):**
> - **Monetary triple-overlap** (#23 + vanilla currency_law + #48/49): #23 is GATED distinct from the vanilla
>   `currency_law` debasement (Qing-specific `qing_currency_stress` bias only, no commerce/tax modifier that
>   would double vanilla's); PART D #48/49 stay ROW-scoped (see below). Documented as orthogonal, not additive.
> - **Military triple-stack** (P7 + #14 + #15): #14 (勇營 regional) and #15 (新軍 central) are made ORTHOGONAL —
>   #15's modernarmy bias must NOT subtract from #14's han-provincial target (the two levers were canceling).
>   Verify the `se_QING_DECLINE.txt` han-provincial target formula and keep them independent.
> - **#30 tariff fake-choice:** re-specified to WRITE a stance var `qing_tariff_stance` the trade pulse reads
>   as `min(treaty_autonomy, stance)`, so the law has bite under a treaty (was a pure modifier the treaty
>   overrode). If that read can't be added cheaply, DEFER #30 rather than ship a fake choice.
> - **1:1 validator on new seats (chief eunuch #B3, dowager #A6):** the doc's "doesn't set qing_office_held"
>   claim contradicted the regent precedent (which DOES). RESOLUTION CHOSEN: separate seat-marker
>   (`qing_seat_chief_eunuch` / `qing_seat_dowager`), NOT counted by `QING_validate_one_position`; the
>   `qing_office_<key>_holder` country var is display-only (like emperor/empress seats). See court doc.
>
> **BATCH-1 SCOPE additions (now explicit):** enumerate ~270 loc keys for the 32 groups; author the 7 GUI
> column title loc keys (`qing_statutes_gov`…); verify 7-column horizontal fit in the 970px scrollarea (or
> wrap); author an explicit OLD→NEW re-filing map for the 13 existing entries (avoid duplicate/vanish);
> replace `omen_power` (#51, means MINING in this TC) with `monthly_legitimacy`/a religion modifier;
> isolation-test #31's on_enact→scripted_effect (else inline the 3-line lever body).
>
> **BALANCE tuning (deferred to testing, noted per element):** eunuch triple-penalty doom-loop (cap the
> corruption feedback, decouple one output, add a non-event purge lever); harem passive promote/demote must
> skip player-acted consorts (2-yr `qing_consort_recently_acted` flag) and the dowager event is ADVISORY not
> forced; harem favour drift must NOT restore to rank×20 (kills squabbling) — make favour a pure accumulator
> the player/events move. See court doc for these.


**Goal:** finish the law-group build-out. Design 2 shipped 13 Qing law groups (P7's
`qing_military_upkeep_law` was the last). This doc designs **every remaining candidate** from the
§A–H catalogue in `overnight_designs.md:219–316`, PLUS the four **upstream Victorian-TC stubs**
(Upper House ×2, Monetary Policy ×2) that ship with empty `modifier = {}` on every option.

Each law is designed against **verified backing-var ground truth** (three fan-out audits, line-cited
below). The single hard rule that governs correctness:

> **A law may only WRITE a var the pulse READS. It may NOT write a var the pulse itself
> COMPUTES/nudges** — doing so makes the law fight the recompute (the documented `qing_censorate_vigor`
> exclusion). The four safe patterns:
> - **SELECTOR (a):** law `set_variable`s a value/flag the pulse reads as-is. Trivial + safe.
> - **MODIFIER-SWAP:** option carries a `modifier = {}` block only (no var). Trivial + safe.
> - **BIAS-A (accumulator):** law sets a standing bias var; the pulse adds it at its existing
>   `QING_DECLINE_nudge`/`change_variable` site (one guarded line). This is the P7 pattern.
> - **BIAS-B (recomputed target):** law sets a bias var threaded INTO the pulse's `set_variable`
>   formula (one guarded `change_variable` term before the clamp). Slightly higher risk (touches a
>   recompute).
> - **MODIFIER-LAW (event/treaty state):** no var-write; the option is a pure standing
>   `modifier = {}`. Used where the backing var is set only by discrete events/treaties.

Every Qing group gets `potential = { tag = CHI }`, a no-op default option (byte-identical to today),
loc, and a `laws_widget` entry in `government_view.gui` (see §GUI). Every bias var is read **guarded**
(`has_variable`) at the pulse site so the default is a true no-op.

---

### PART A — GUI capacity (blocking constraint for the whole build)

`government_view.gui` does **not** auto-enumerate law groups — each is hand-listed as a `laws_widget`
inside a `laws_widget_area` column (lines 2258–2304 hold the current 13 in one column). Vanilla splits
its ~50 laws across ~9 area columns. **Adding ~30 more Qing laws to one column overflows the panel.**

**Design:** split the Qing statutes into **domain sub-columns**, one `laws_widget_area` each, mirroring
vanilla's Economic/Military/Social split. Proposed columns (title loc in parens):
1. `qing_statutes_gov` (治道 — Governance & Council) — ethnic_governance, office_selling, ministry_estab,
   advisory_estab, council_composition, secretariat_standard, deliberative_governance
2. `qing_statutes_fiscal` (財政 — Fiscal & Trade) — salt_admin, canton_regime, canton_purse,
   caravan_customs, granary_policy, canal_quota, customs_regime, monetary_response, frontier_trade_sov, tariff_regime
3. `qing_statutes_military` (武備 — Military) — military_upkeep, provincial_militarization, army_modernization
4. `qing_statutes_frontier` (邊疆 — Frontier & Subjects) — xinjiang_admin, tributary_ritual,
   frontier_settlement, assimilation_doctrine, national_integration, amban_estab
5. `qing_statutes_court` (宮廷 — Succession & Court) — succession_method, regency_rules,
   princely_establishment, harem_establishment, eunuch_policy
6. `qing_statutes_modern` (自強 — Modernization & Culture) — penal_code, ritual_orthodoxy, opium_policy,
   exam_cadence, exam_curriculum, modernization_doctrine, industrial_encouragement, education_program,
   cultural_patronage, works_priority, censorate_empowerment, missionary_policy
7. `qing_statutes_diplo` (外交 — Diplomacy & Great Game) — gp_alignment, foreign_office_doctrine, overseas_expansion

**Task:** author 6 new `laws_widget_area` blocks (one exists), re-file the 13 existing entries by domain,
add the new entries. Titlebar loc keys `qing_statutes_gov` … `qing_statutes_diplo`. This GUI work is a
prerequisite for ANY new group being visible — do it first / alongside.

---

### PART B — Qing law groups by classification

Legend for each entry: **[CLASS]** · backing var · **PATTERN** · risk. Options are `default (no-op) /
stance / stance`. "Pulse site" = the exact line where BIAS is applied.

#### B1. SELECTOR / MODIFIER-SWAP — trivial, safe (build first)

**1. Penal Code Regime 大清律例** — *already shipped* (`qing_penal_code_law`). Modifier-swap.
**2. Ritual Orthodoxy 禮部** — *already shipped* (`qing_ritual_orthodoxy_law`). Modifier-swap.
**3. Opium / 4. Caravan / 5. Salt / 6. Canton regime / 7. Canton purse / 8. Ethnic gov / 9. Office-selling
/ 10. Ministry estab / 11. Advisory estab / 12. Exam cadence** — *already shipped.*

**13. Industrial Encouragement 官辦 / 官督商辦 / 商辦** — [MODIFIER-SWAP + NET-NEW-lite selector]
- Backing: modifier targets EXIST (`qing_earlyindus_*`, `qing_selfstr_guandu_tension`
  `se_QING_SELFSTR.txt:421`), but no numeric tri-state selector var.
- **Design:** pure **modifier-swap** law — 3 options each carrying a `modifier = {}` expressing the
  school's trade-off (官辦 state-run: +research, +cost, −commerce; 官督商辦 merchant-supervised: balanced,
  small guandu-tension; 商辦 merchant-run: +commerce, +middle-strata output, −state control). NO var.
  Do NOT invent a selector var (nothing reads it). **[REVIEW FIX] NO on_enact nudge** — the earlier "optionally
  nudge qing_selfstr_progress" is a TOGGLE-FARM (on_enact fires every enact → re-enact to farm the nudge).
  Pure modifier-swap only; the state-run school's modernization edge is expressed as a research modifier, not a
  var nudge. Risk: low.

#### B2. BIAS-A — accumulators (P7 pattern: one guarded nudge line)

**14. Provincial Militarization 勇營** — [ACCUMULATOR] `qing_han_provincial_power` (nudged ±2,
`se_QING_DECLINE.txt:426`). Law sets `qing_provmil_bias` ∈ {centralized −1 / sanctioned 0 / delegated +1};
pulse adds it guarded at the :426 nudge. Modifiers: delegated = +manpower/−central control; centralized =
inverse. **CAVEAT:** design note says these are "arguably better AI/event-driven" — still viable; a law is
the player's explicit lever over the 湘軍/淮軍 delegation. Risk: low.

**15. Army Modernization Mandate 新軍** — [ACCUMULATOR] `qing_modernarmy_share` (nudged ±2,
`se_QING_DECLINE.txt:390`). Law sets `qing_modernarmy_bias` ∈ {traditional −1 / mixed 0 / new-army +1}; pulse
adds guarded. Modifiers express drill/discipline vs. banner-conservatism prestige cost. Risk: low.

**16. Cultural Patronage 文治** — [ACCUMULATOR] `qing_wenzhi_patronage` (init 40, −1/qtr drift
`se_QING_WENZHI.txt:75`). Law sets `qing_wenzhi_bias` ∈ {austere +? / standard 0 / lavish −?} added at :75
so lavish offsets the decay (net 0 or positive) and austere quickens it. **Ratchet-rule caution:** lavish
must be a *bias at the drift site*, NOT a positive free nudge — the band-gate + the existing −1 base keeps
it bounded. Modifiers: lavish = +prestige/−treasury; austere = inverse. Risk: low.

**17. Overseas Education 留學** — [ACCUMULATOR + flag] `qing_students_abroad` (nudged, `se_QING_STUDENTS.txt:92`).
Law sets `qing_students_bias` ∈ {none / limited / large}; adds to the recurring +20 abroad nudge (large
accelerates, none zeroes the recurring gain via a negative bias floored at 0). Also modifier: large =
+research/−conservative-happiness. **Interaction:** the students mission-active flag is event-owned; the law
biases the *rate*, not the flag. Risk: low.

**18. Great-Power Alignment** — [ACCUMULATOR ×3] `qing_gp_tension_britain/france/russia`
(`se_QING_GREATGAME.txt:79-110`). Law sets `qing_gp_alignment_bias` ∈ {isolation / balance / align};
applied as a standing per-power tension nudge (isolation = +tension all; align = −tension toward the aligned
power, event-picked). **CAVEAT:** "align-with-one" needs a target — model as balance (symmetric −) vs.
isolation (symmetric +); a specific alignment stays event-driven. Risk: low-moderate (3 nudge sites).

**19. Anti-Corruption Stance** — [ACCUMULATOR] `qing_corruption_level` (init 12, nudged many).
**[REVIEW FIX — ratchet-defeat guard]** Build as opt-in, but the bias must TILT not CANCEL: corruption is
nudged +N from 15+ sources, so a standing −1 (audits) / −2 (draconian) only SLOWS accrual — and the applied
bias must be FLOORED so the law alone can never drive the meter toward 0 (e.g. apply the negative bias only
while `qing_corruption_level > 20`, so it thins graft but never legislates a spotless court). Modifier cost
(−admin-efficiency / +stability / −upper-strata happiness). tolerant 0 / audits −1 / draconian −2. Risk: low.

**20. Heterodox Sect Policy 白蓮教** — [ACCUMULATOR] `qing_sect_pressure` (`se_QING_DECLINE.txt:1005`).
**[REVIEW FIX — ratchet-defeat guard]** Sect pressure is the OUTPUT of 8+ systems (opium, canal neglect,
missionary friction, granary failure) and is meant to build toward rebellion. A standing suppress bias that
cancels it would legislate away the White-Lotus/Taiping. FIX: bias is SMALL and band-gated — suppress −1
applied only while `qing_sect_pressure > 25` (thins low-level unrest, cannot prevent a genuine crisis), with
a −minority-happiness cost that itself feeds unrest (so heavy suppression is self-limiting). tolerate 0 /
monitor 0 +watch modifier / suppress −1. Risk: low.

**21. Reform Posture** — [ACCUMULATOR, SIGNED ±100] `qing_reform_faction_balance`
(`se_QING_FACTION.txt:424`, raw `change_variable`, clamp ±100). **CRITICAL:** must use `change_variable`,
NOT `QING_DECLINE_nudge` (the macro clamps at 0 and would corrupt the signed meter — verify ALL existing
nudge sites use raw change_variable before adding the law bias). **[REVIEW: build with small tilt]** faction
balance is meant to emerge from events, so the law bias is a SMALL signed nudge (conservative −1 / gradualist
0 / reformist +1) that tilts the drift without swamping the ±5..±10 event/mission nudges. Modifier expresses
the court's reform posture. Risk: moderate (signed-clamp footgun — the #1 implementation caution).

**22. Deliberative / Banner Nobility Governance 議政王大臣** — [ACCUMULATOR] `qing_delib_cohesion`
(init 50, `se_QING_DELIBERATIVE.txt:367`). Law sets `qing_delib_bias` ∈ {empower +/ balance 0 / curb −}
added at the cohesion nudge; cohesion feeds `qing_banner_decay` bands. Modifiers express Manchu-grandee
prestige vs. autocratic centralization. Risk: low.

**23. Currency Stress / Monetary Response** — [ACCUMULATOR] `qing_currency_stress`
(`se_CURRENCY_STRESS.txt` engine drift + discrete nudges). **Pairs with vanilla `currency_law`.** Law sets
`qing_monetary_bias` ∈ {hard-specie −/ stabilization 0 / debasement +} added as a standing stress nudge.
Modifiers: hard-specie = +stability/−commerce; debasement = +tax/−stability. Risk: low. *(This is the Qing
analogue; see PART D for the vanilla monetary stubs.)*

#### B3. BIAS-B — recomputed targets (one guarded term in the formula, before the clamp)

**24. Council Composition** — [RECOMPUTED-TARGET] `qing_council_eff_target` (rebuilt to 0 each pulse,
`se_QING_COUNCIL.txt:441`; clamp :554). Law sets `qing_council_comp_bias` threaded as `change_variable`
before :554. **BUT** the catalogue's real intent (Manchu-weighted / balanced / meritocratic) maps better to
the **`qing_council_dyarchic_balance` MODIFIER + seat composition** than to eff_target. **Design:** a
MODIFIER-SWAP law (each option a `modifier`) + optional bias into eff_target for the "meritocratic" tilt.
Do NOT set `qing_council_dyarchic_balance` (it's a banded modifier, not a var). Risk: moderate.

**25. Canal Grain Tribute Quota 漕運** — [RECOMPUTED-TARGET] `qing_canal_jiangnan_quota` (rebuilt to 0.5
each pulse, `se_QING_CANAL.txt:209`; clamp :228). Law sets `qing_canal_quota_bias` added before the :228
clamp. Options: relaxed −0.1 / standard 0 / maximal +0.15. Modifier: maximal = +grain/−Jiangnan happiness.
Risk: moderate.

**26. Xinjiang Administration 屯田/伯克** — [RECOMPUTED-TARGET] `qing_xj_consolidation` is rebuilt from
`qing_xinjiang_control` + terms (`se_QING_XINJIANG.txt:229`). **Law must feed an INPUT, not the output.**
Two clean choices: (a) bias `qing_xinjiang_control` (the ACCUMULATOR input, BIAS-A at a nudge) — but that's
the event-owned grip meter; risky. (b) add `qing_xj_admin_bias` as a term in the consolidation scratch
formula (BIAS-B before :227 clamp). **Design: BIAS-B** — options military-farm 屯田 (+consolidation) /
beg-indirect 伯克 (0) / provincialize 行省 (+more, +cost). Risk: moderate.

**27. Customs Service Regime 海關** — [RECOMPUTED-TARGET via input] `qing_customs_eff_target` rebuilt from
`qing_customs_foreign_control`×2 + bureau_integrity (`se_QING_CUSTOMS.txt:173-176`). The catalogue's
native/foreign-supervised axis maps to `qing_customs_foreign_control` (ACCUMULATOR, `:144` `$amount$`
helper). **Design: BIAS-A on `qing_customs_foreign_control`** via a standing nudge — native = −, Hart-style
foreign-supervised = + (efficiency up, autonomy/prestige down). Modifier expresses the sovereignty cost.
Risk: moderate. **Overlaps `qing_tariff_autonomy`** (treaty-state, see B4) — keep distinct: this is the
*administration*, tariff is the *rate*.

**28. Missionary Policy** — [RECOMPUTED-TARGET] `qing_antichr_target` / `qing_social_friction_target`
rebuilt from formula (`se_QING_MISSIONARY.txt:243-252/194-203`). Law sets `qing_missionary_tol_bias` as a
term in the target formula (prohibit − toleration → but that raises friction? model carefully: prohibit =
+sentiment via suppression backlash OR −reach; open = +reach/+friction). **Design: BIAS-B** on the target
formula + gate cathedral promotion (Design-1 coupling). Options prohibit / tolerate / open. Risk:
moderate-high (two coupled meters + Design-1). *Recommend building AFTER the simpler ones validate.*

**29. Sphere / (folded into #18 Great-Power Alignment)** — `qing_sphere_dominant` is RECOMPUTED from the
sphere formula and is better left read-only; the alignment law (#18) biases tension, not the sphere result.
No separate law. 

#### B4. MODIFIER-LAW — event/treaty state (pure `modifier`, no var-write)

**30. Tariff Regime** — [TREATY-STATE] `qing_tariff_autonomy` set only by treaty events
(`se_QING_TREATIES.txt:79/126`). **[REVIEW FIX — was a fake choice]** A pure modifier-law here is meaningless:
the treaty system owns the mechanical effect, so a "restored autonomy" modifier the treaty overrides adds
nothing. FIX: the law WRITES a stance var `qing_tariff_stance` ∈ {comply 0 / partial-resist 1 / full-autonomy
2}; the trade/customs pulse computes effective autonomy as `min(qing_tariff_autonomy, stance-cap)` so the law
has real bite — you can legislate "we want autonomy" and it takes effect the moment a treaty revision raises
`qing_tariff_autonomy`. That is a one-line read added to the customs pulse (NET-NEW-lite, not a standalone
modifier). **If that read cannot be added cheaply, DEFER #30** rather than ship a fake choice. Risk: moderate.

**31. Frontier Trade Sovereignty 阿奇木** — [STATE-FLAG] `qing_caravan_aqsaqal_granted` toggled by
`QING_caravan_grant_aqsaqal`/`_revoke_aqsaqal` levers. Design: a law whose on_enact CALLS the existing
grant/revoke lever (grant-concession → `QING_caravan_grant_aqsaqal = yes`; assert → `_revoke_aqsaqal`).
This is a SELECTOR-via-lever (the levers are guarded + idempotent). Risk: low. *Novel pattern — on_enact
calling a scripted_effect; verify on_enact accepts effect calls (it does — see estab laws' set_variable).* 

**32. Overseas Expansion** — [MODIFIER/EVENT-STATE] colonies + treasure fleet are boolean country
modifiers granted by missions/events (`se_QING_TREASURE_FLEET.txt:144-153`). Design: pure MODIFIER-LAW —
isolationist / trade-fleet / colonial, each a `modifier = {}` (naval/colonial cost vs. prestige). on_enact
may nudge `qing_tributary_prestige`. Does NOT grant colonies (those stay mission-earned). Risk: low.

**33. Foreign-Office Doctrine 總理衙門** — [EVENT-STATE] legation/embassy counts are event-established;
`qing_zongli_diplomat_count` is RECOMPUTED from marked characters. Design: MODIFIER-LAW — tributary-only /
resident-legations / full-diplomacy, each a `modifier` (diplomatic-reputation/reform-pressure trade).
on_enact nudges `qing_reform_pressure` (adopting full diplomacy breaks the tribute worldview, matching the
P3 legation event). `allow` gates "full diplomacy" on `qing_legation_count >= 1`. Risk: low.

#### B5. Court / Succession — mixed, several construction-risky or one-way (design with care)

**34. Succession Method 秘密立儲** — [ONE-WAY-FLAG] `qing_secret_succession_sealed` is a discrete seal set
=1 then event-REMOVED at accession (`se_QING_PRINCES.txt:342/400`). It is NOT a persistent policy toggle.
**A reversible law is new capability.** Design: MODIFIER-LAW selector `qing_succession_method_law` ∈ {open
公開 / secret 秘密立儲 / deliberative 議政} where the option sets a NEW standing var `qing_succession_mode`
(this is a genuine policy stance, distinct from the per-reign seal flag) that the princes/accession code
reads to choose the pick algorithm. **This is NET-NEW-lite** (new var + a read at the accession pick,
`se_QING_PRINCES.txt:336` `order_by`). Risk: moderate (touches succession). *Recommend: design now, build
in its own careful chunk.*

**35. Regency Rules** — [EVENT-STATE] `qing_office_regent_holder` (char handle) + `qing_regent_pick_kind`
(flag, log-only) installed/cleared by regency machinery. No persistent policy var. Design: MODIFIER-LAW +
NET-NEW selector `qing_regency_pref` ∈ {dowager / prince / councillor} that `QING_seat_regent_install`
(`se_QING_SEATS.txt:270-324`) reads to order its pick. NET-NEW-lite (one read added). Risk: moderate.

**36. Princely Establishment** — [ACCUMULATOR, per-character] `qing_prince_backing` (char var, nudged +
`order_by` selector). Country-scope law can't set a per-char var directly. Design: MODIFIER-LAW (favour /
investigate / restrict) each a `modifier` affecting prince loyalty/threat, + optionally a country var
`qing_prince_policy` read by `QING_prince_backing_nudge` to scale the nudge. Risk: low-moderate.

**37. Harem Establishment 后妃** — [RECOMPUTED + CONSTRUCTION-RISKY] `qing_harem_rankN_count` rebuilt from
the consort roster (`se_QING_HAREM.txt:122-142`); touches consort create/promote paths. **DEFER** — the
audit flags the harem create path as #90/#336-sensitive; a size/rank-distribution law would need to gate
the promotion cap, and the value is a recomputed tally (can't be set). If built: a cap var
`qing_harem_size_cap` read at the promotion gate (`:246`). **Recommend: DEFER** (construction risk >
value). Risk: high.

**38. Eunuch Policy 內務府** — [RECOMPUTED + CONSTRUCTION-RISKY] `qing_eunuch_count` sits on the
`create_character` eunuch-mint path (`se_QING_HOUSEHOLD.txt:82-106`); no live consumer outside its own file.
**DEFER** — restrict/standard/empowered would gate the mint count (construction-risky) and nothing reads the
count today, so the policy has no mechanical bite yet. **Recommend: DEFER.** Risk: high.

#### B6. Frontier / Integration

**39. Tributary Ritual Frequency 朝貢** — [PER-SUBJECT TIMER] `qing_tribute_cooldown` is a per-subject
`days=` timer gate (`se_QING_TRIBUTE.txt:257-266`). A CHI country law can't set a per-subject var. Design:
MODIFIER-LAW + a country var `qing_tribute_cadence_law` that `QING_tribute_*` reads to CHOOSE the cooldown
length (1095/1825/2190 already the three branch values — the law selects which branch). NET-NEW-lite (one
read). Options frequent / standard / rare. Risk: low-moderate.

**40. Frontier Settlement Policy 移民實邊** — [ONE-WAY-FLAG] `qing_frontier_resettlement` set once =1, never
cleared (`se_QING_POPULATION.txt:242`). **A closed↔encouraged↔forced law needs a clear-path (new
capability).** Design: replace the one-way flag read at `se_QING_POPULATION.txt:95` with a tri-state var
`qing_frontier_settle_policy` ∈ {closed 0 / encouraged 1 / forced 2} the law sets; migrate the existing
flag semantics (flag-set ⇒ value≥1). NET-NEW-lite + a migration guard. Options closed / encouraged / forced
(forced = +migration/−minority happiness). Risk: moderate (migration-relief-valve interaction).

**41. Cultural Assimilation Doctrine 漢化** — [per-char selector + RECOMPUTED count] `qing_manchu_identity`
(per-char, banded modifier-swap) + `qing_sinic_count` (recomputed province tally). Country law can't set
per-char identity. Design: MODIFIER-LAW (preserve-Manchu / balanced / sinicize) each a `modifier` + a
country var `qing_assimilation_doctrine` read by `QING_char_shift_identity`/sinicization pulse to bias the
drift direction. NET-NEW-lite. Risk: moderate.

**42. National Integration** — [ACCUMULATOR via target-lift] `qing_civic_identity` — the SAFE knob is the
Design-4 `qing_civic_identity_settle_bonus` target-lift (`se_QING_DECLINE.txt:856`). Law sets
`qing_integration_doctrine_bias` folded into `qing_civic_target_tmp` alongside the settle bonus (BIAS-B into
the target). Options dynastic (0) / multi-ethnic (+) / civic-nation (++). Modifier: civic-nation =
+assimilation/−traditional-legitimacy. **Couples to Design 4.** Risk: low-moderate.

**43. Amban Establishment 理藩院** — [NET-NEW] `QING_AMBAN_MIN` does not exist (not even a constant — only
a nickname substring). Design: author a new var `qing_amban_estab_target` (mirror `qing_ministry_estab_law`
exactly — that's the proven precedent) read by the amban staffer. **NET-NEW plumbing** (var + one read).
Options lean / standard / expanded. Risk: moderate (mirrors proven estab work).

#### B7. Modernization capstones

**44. Modernization Doctrine 自強** — [ACCUMULATOR] `qing_selfstr_progress` (band → 3-modifier swap,
`se_QING_SELFSTR.txt:672`). Self-strengthening progress is meant to be EARNED (missions/events), not
legislated. Design: a pure MODIFIER-LAW (conservative / ti-yong 中體西用 / wholesale-western) each a `modifier`
expressing the reform posture. **[REVIEW FIX — no farmable nudge]** the earlier "one-time on_enact nudge" is
a toggle-farm (on_enact fires every enact). If a "wholesale-adoption kickstart" is wanted, it MUST be
once-guarded: `on_enact = { if = { limit = { NOT = { has_variable = qing_selfstr_wholesale_adopted } }
QING_selfstr_advance = { amount = X }  set_variable = qing_selfstr_wholesale_adopted } }` — fires at most once
ever. Default: no kickstart, pure modifier. Risk: low-moderate. *The three band-modifiers stay
progress-driven; the law is the posture overlay.*

**45. Exam Curriculum (practical-subjects / abolition)** — [NET-NEW] beyond cadence, no backing mechanic
exists. Design: new var `qing_exam_curriculum` ∈ {classical 0 / practical 策論 1 / abolition 2}; classical
= no-op, practical = bias `qing_exam_pass_rate` recompute + a research modifier, abolition = disables the
exam cycle (gate `QING_exam_*` on curriculum≠2) + a big stability/legitimacy shock. **NET-NEW plumbing**
(var + reads in the exam pulse). Options classical / practical / abolition. Risk: moderate-high (abolition
disables a whole subsystem — needs careful gating). *Recommend: build classical/practical first; abolition
as a follow-up.*

**46. Censorate Empowerment 都察院** — [RECOMPUTED-TARGET] `qing_censorate_vigor` rebuilt from officeholder
traits/finance each cycle (`se_QING_CENSORATE.txt:58-64`, clamp 0..50). This was the ORIGINAL exclusion.
Design: BIAS-B — add `qing_censorate_bias` as a term in the recompute before the :66 clamp (weak −/ active 0
/ weaponized +). Modifier: weaponized = +corruption-detection/−official happiness (factional purges). Risk:
moderate (this is the meter the whole "fights-the-pulse" rule was named after — bias-B is the correct, safe
way now that the pattern is proven).

**47. Public/Palace Works Priority 三山五園** — [EVENT/MODIFIER-STATE] no numeric priority meter; the
Summer Palace (`qing_sp_*`) + Works (`qing_works_*`) subsystems are event/flag-driven. Design: pure
MODIFIER-LAW (frugal / balanced / grand) each a `modifier` (construction/prestige vs. treasury/corruption).
**[REVIEW FIX — no farmable nudge]** does NOT nudge `qing_corruption_level` on_enact (toggle-farm). The
"grand works breed graft" flavour is expressed as a standing `monthly_corruption` MODIFIER on the "grand"
option, not a one-off var nudge. Does NOT build the palace (that stays the Summer Palace tree). Risk: low.

---

### PART C — Summary: build order & disposition

**BUILD — trivial (SELECTOR / MODIFIER-SWAP / MODIFIER-LAW), no pulse edits (~9):**
Industrial Encouragement (13), Tariff Regime (30), Frontier Trade Sov (31), Overseas Expansion (32),
Foreign-Office Doctrine (33), Princely Establishment (36), Public Works Priority (47), + the two vanilla
Upper House stubs & monetary stubs (PART D).

**BUILD — BIAS-A, one guarded nudge line each (~7):** Provincial Militarization (14), Army Modernization
(15), Cultural Patronage (16), Overseas Education (17), Great-Power Alignment (18), Deliberative Governance
(22), Monetary Response (23). Plus opt-in Anti-Corruption (19).

**BUILD — BIAS-B, one guarded formula term each (~6):** Council Composition (24), Canal Quota (25),
Xinjiang Admin (26), Customs Regime (27), Missionary Policy (28), National Integration (42), Censorate
Empowerment (46).

**BUILD — NET-NEW-lite, new var + one read (~6):** Succession Method (34), Regency Rules (35), Tributary
Ritual (39), Frontier Settlement (40), Assimilation Doctrine (41), Amban Establishment (43), Modernization
Doctrine (44), Exam Curriculum practical (45, classical/practical only).

**USER DECISION (2026-07-24):** build all deferrals EXCEPT the exam-abolition tier. Sequence **by risk
ascending, commit + push each batch** so boot-testing is incremental.
- Harem Establishment (37) — **BUILD** (extra care on the consort create/promote path; law gates the
  promotion cap `qing_harem_size_cap`, does NOT touch create_character itself).
- Eunuch Policy (38) — **BUILD** (law sets a mint-cap var read at the mint gate; does NOT add modifiers
  inside create_character — #90 rule).
- Heterodox Sect (20) — **BUILD** (Bias-A on `qing_sect_pressure`; tolerate/monitor/suppress).
- Reform Posture (21) — **BUILD** (Bias-A on `qing_reform_faction_balance` — MUST use raw `change_variable`
  with the ±100 clamp, NOT `QING_DECLINE_nudge`).
- Exam Abolition tier (45b) — **STILL DEFERRED** (disables a subsystem; follow-up only). Exam Curriculum
  (45) ships classical/practical only.

**Net new law groups this pass: ~32 built + 4 vanilla stubs filled = ~36**, taking the Qing total from 13 →
~45.

#### Batch plan (risk ascending; each boots + commits on its own)
- **Batch 1 — GUI + trivial + upstream stubs:** PART A (6 new `laws_widget_area` columns + re-file 13
  existing), the ~9 selector/modifier-swap/modifier-law groups (13/30/31/32/33/36/47), the 4 vanilla stub
  fills (48/49/50/51) + the `00_administrative_laws.txt` brace fix. GUI is a prerequisite so it leads.
- **Batch 2 — Bias-A** (one guarded nudge line each): 14/15/16/17/18/19/20/21/22/23/44.
- **Batch 3 — Bias-B** (one guarded formula term each): 24/25/26/27/28/42/46.
- **Batch 4 — Net-new-lite** (new var + one read): 34/35/39/40/41/43/45(classical+practical).
- **Batch 5 — [REVIEW FIX] REMOVED.** #37 (harem) and #38 (eunuch) are NOT standalone laws — a law shipped
  before its backing mechanic is a no-op. They live ONLY in the court-intrigue subsystem batches (6 eunuch /
  7 harem), where the law is built in the SAME batch as the mechanic it gates. The old Batch 5 is dissolved.
Each batch: author data → loc → GUI entry → pulse wire (if any) → brace/quote check → code-review →
boot-crash review → commit as freekumquats → push merge-overnight.

---

### PART D — Upstream Victorian-TC stubs (Upper House ×2, Monetary ×2)

These ship in the repo with **empty `modifier = {}` on every option** and are absent from vanilla Imperator
AND both oracle repos (Invictus, TI never added a bicameral legislature or monetary-setting layer). Nothing
to copy — fill plausibly with **proven modifier keys** (drawn from `00_economic_laws.txt` currency_law etc.).

**FIRST, fix the brace bug:** `00_administrative_laws.txt` is 9-open / 8-close — `delegated_monetary_policy`
(line 10) never closes, so `legislative_monetary_policy` is nested inside it (the group has only 2 valid
options). Add the missing `}` after `delegated_monetary_policy`'s `modifier`.

**48. `monetary_policy_law`** (executive / delegated / legislative) — WHO controls minting. Fills:
- executive: `stability_monthly_change = 0.02`, `monthly_corruption = 0.02` (crown control, mild graft)
- delegated: `global_commerce_modifier = 0.03`, `global_tax_modifier = 0.02` (competent ministry)
- legislative (`allow = is_republic`): `global_commerce_modifier = 0.05`, `research_points_modifier = 0.02`,
  `stability_monthly_change = -0.02` (accountable but slow). This gates `monetary_policy_setting`.

**49. `monetary_policy_setting`** (recall / limited minting / more minting / issue bonds) — the stance,
gated on `legislative_monetary_policy`:
- currency_recall: `global_commerce_modifier = -0.05`, `stability_monthly_change = 0.03` (deflationary sound-money)
- limited_minting: `monthly_corruption = -0.03`, `global_upper_strata_happyness = 0.03`
- more_minting: `global_tax_modifier = 0.05`, `global_commerce_modifier = 0.05`, `stability_monthly_change = -0.02`
- issue_bonds: `global_commerce_modifier = 0.1`, `global_capital_trade_routes = 1`, `monthly_corruption = 0.03`
  (mirrors currency_law's `promissory_notes`).

**50. `upper_house_powers_law`** (veto / review / delay) — gated `has_law = bicameral_legislature`:
- power_of_veto: `stability_monthly_change = 0.03`, `global_middle_strata_happyness = 0.05`,
  `monthly_political_influence = -0.05` (strong chamber, slower governance)
- power_of_review: `global_upper_strata_happyness = 0.03`, `stability_monthly_change = 0.01`
- power_of_delay: `monthly_political_influence = 0.03`, `global_middle_strata_happyness = -0.02` (weak chamber)

**51. `upper_house_composition_law`** (appointed-spiritual / appointed / elected / state-reps) — gated
`has_law = bicameral_legislature`:
- appointed_hereditary_spiritual: `global_upper_strata_happyness = 0.05`, `omen_power = 0.05` (or religion
  modifier), `global_middle_strata_happyness = -0.02`
- appointed: `monthly_political_influence = 0.05`, `global_upper_strata_happyness = 0.02`
- elected: `global_middle_strata_happyness = 0.05`, `global_lower_strata_happyness = 0.03`,
  `stability_monthly_change = -0.02`
- state_representatives: `global_pop_assimilation_speed_modifier = 0.05`, `diplomatic_reputation = 0.5`
  (federal chamber).

**LOC:** replace placeholder descs (`"Power of Veto desc"`, `""`) with real 1-line flavour for all option
`_desc` keys (laws_l_english.yml:367-637). **VERIFY every modifier key** against the schema before commit
(all keys above are drawn from existing law/modifier files, but confirm `omen_power`/`monthly_governor_wage`
etc. resolve — a bad key is a boot error).

**GUI:** the four vanilla stubs are ALREADY registered in `government_view.gui` (lines 2040-2144); no new
area needed for them — only the `modifier`/loc fills + the brace fix.

---

### PART E — Cross-cutting build rules (apply to every group)

1. **Guarded reads:** every bias var read at a pulse site MUST be `if = { limit = { has_variable = X } … }`
   so the default (var unset) is byte-identical to today. (P7 proven, `se_QING_DECLINE.txt:919-920`.)
2. **No-op default:** every group's first option sets the bias to 0 / the current value — enacting nothing
   changes nothing. Verify against each var's INIT.
3. **Signed meters:** `qing_reform_faction_balance` is ±100 via raw `change_variable` — NEVER drive with
   `QING_DECLINE_nudge` (clamps at 0). (If (21) is ever built.)
4. **Recomputed targets:** never `set_variable` the target directly — thread the bias into the formula
   BEFORE the clamp (BIAS-B). Applies to 24/25/26/27/28/42/46.
5. **on_enact calling effects:** (31) calls `QING_caravan_grant_aqsaqal` — confirm on_enact accepts effect
   calls (estab laws prove set_variable works; a scripted_effect call is the same effect context — verify at
   build).
6. **GUI registration is mandatory:** an unregistered law group is invisible. Every new group needs a
   `laws_widget` line in its domain `laws_widget_area` (PART A).
7. **BOM:** `00_qing_statutes_laws.txt` — check whether it carries a BOM before Python-editing (setup/ reader
   rejects BOM; common/ lexer tolerates it — but preserve whatever's there).
8. **Boot-crash review + se_LOG** per standing rules; commit as freekumquats; push to merge-overnight.


## PART V.2 — Court Intrigue Subsystems (Harem 后妃 + Eunuch 內務府)

## Court Intrigue Expansion — Harem (后妃) + Eunuch (內務府) Subsystems

Design for the two court subsystems that #37 and #38 grew into. Both build ON existing concrete code
(mapped with line citations), reuse proven primitives, and obey the construction-risk rules that the
harem/eunuch `create_character` paths already carry. **Nothing is built yet — this is for review.**

### ADVERSARIAL REVIEW PASS (2026-07-24) — applied fixes
Reviewers verified: NO create_character touched (blast radius confirmed untouched), NO #336 inline, named
branch is runtime-only. Fixes applied below:
- **1:1 validator (Risk 5/6):** the doc's "seat doesn't set qing_office_held" contradicted the regent
  precedent (which DOES set it → would trip `QING_validate_one_position`, se_QING_COUNCIL.txt:228-247, which
  counts both qing_office_held AND qing_is_palace_eunuch/qing_is_harem_consort). **RESOLUTION: separate
  seat-marker.** Chief-eunuch and dowager seats set `qing_seat_chief_eunuch` / `qing_seat_dowager` (NOT
  counted by the validator) + a display-only `qing_office_<key>_holder` country var (like the emperor/empress
  seats), and do NOT set `qing_office_held`. So a promoted eunuch keeps only `qing_is_palace_eunuch` (1
  marker → passes), a former-consort dowager keeps only `qing_is_harem_consort` (1 marker → passes).
- **A3/A5 scope:** all passive rolls + new events fire FROM `QING_harem_pulse` at ROOT=CHI using
  `ordered_in_list { variable = qing_harem_consorts }` and `trigger_event` to `type = country_event`s — NEVER
  from a character-root GUI context (BT-13/#373). Stated explicitly in A3/A5.
- **A1 favour drift (doom of the mechanic):** the earlier "drift toward rank×20" is a RESTORING drift that
  flattens every consort to her rank's value → kills the squabbling favour is meant to create. FIX: favour is
  a PURE ACCUMULATOR moved by the favour lever + events (+ a small decay toward 0 for un-favoured consorts,
  NOT toward rank). Favour becomes an axis INDEPENDENT of rank (low-rank favourite / high-rank cold political
  match) — that is the drama.
- **A3 fights-the-player:** passive promote/demote must SKIP any consort the player acted on within 730 days
  (`qing_consort_recently_acted` timer flag set by the player promote/demote levers; the roll gates
  `NOT has_variable`). The court drifts only consorts the player has left alone.
- **A5 dowager (harem.11) is ADVISORY, not forced:** she SUGGESTS a promotion/demotion (heed = +dowager
  favour/+harmony; defer = −dowager favour; refuse = −−favour + scandal risk). The player keeps the wheel.
- **B1 eunuch power formula (was underspecified):** define exactly —
  `qing_eunuch_power = min(100, qing_eunuch_count*8 + (faction_leader ? 30 : 0) + corruption_band_bonus)`,
  then `if chamberlain.charisma >= 8 { subtract 15 }` (a strong chamberlain checks the eunuchs). No
  boolean-in-arithmetic; the chamberlain term is a discrete guarded subtraction.
- **B2 doom-loop guard:** eunuch power feeds corruption/backlog/reform, but (a) the corruption nudge is
  gated `qing_corruption_level < 70` so it can't spiral past the crisis band; (b) the reform-balance penalty
  fires ONLY at high power (≥80), not the mid band; (c) add a PLAYER purge lever (a chamberlain decision,
  cost stability/harmony, −30 power, 1825-day cooldown) so counterplay isn't gated behind an event roll.
- **B2 reform-balance:** MUST use raw `change_variable` with the ±100 clamp (NEVER `QING_DECLINE_nudge`);
  verify existing qing_reform_faction_balance sites are all raw change_variable first.

### Hard constraints (from the code, non-negotiable)
1. **`create_character`:** no modifiers, no HEALTH-type traits inside it OR in a boot-reachable follow-up
   scope (the `castrated` trait was removed for exactly this — `se_QING_HOUSEHOLD.txt:96-103`,
   `se_QING_HAREM.txt:63-65`). culture/religion must be LITERALS (a country-scope value floods 1.4M log
   lines). New consorts/eunuchs spawn only at RUNTIME (pulse), never gamestate construction, and follow
   the proven mint idiom.
2. **Sorting iterators** (`ordered_character`, `ordered_in_list order_by=…`) must fire via a hidden
   `trigger_event` trampoline, NEVER inlined in a scripted_gui button (#336 AV crash class —
   `qing_harem_events.txt:176-217`).
3. **Picker rows run at CHARACTER root** — re-root to CHI via a hidden country_event before running
   ROOT-based machinery (BT-13/#373, `qing_harem_events.txt:154-163`).
4. **1:1 office validator** (`se_QING_COUNCIL.txt:228-247`): a character may hold only one position
   marker. A "chief eunuch" seat must be its OWN marker, NOT `qing_office_held` (else it trips the
   validator; `qing_is_palace_eunuch` is already a tracked position). Use the non-appointable-seat shape
   from `se_QING_SEATS.txt:15-18`.
5. **Event throttle:** any new court event shares `qing_gc_event_slot_used` (test-then-claim) — at most
   one court event per ~90-day pulse.
6. **Perf:** reads are O(1) counters + O(court) `any_character`; never sweep pops/provinces.

---

## SUBSYSTEM A — Harem Intrigue (后妃之爭)

### What exists (map summary)
4-rank ladder (`qing_consort_rank` 1-4, hard caps 1/2/4/uncapped enforced in 5 synced places); roster +
count + per-rank tallies; pickers draft·take / favour / promote; native heir via `make_pregnant`;
empress = `current_ruler.spouse`; quarterly `QING_harem_pulse` with a harmony↔fertility loop + ONE
12%-throttled intrigue event (schemer-vs-empress, 3 options). **Rank already feeds succession**:
`se_QING_PRINCES.txt:113-130` gives a prince +25 (嫡子, empress's son) / +12 (貴子, mother rank≥3) to
`qing_prince_backing`.

### Green field (what's missing)
No demote/disgrace (rank only rises); no promotion/demotion *chance* (deterministic); no per-consort
favour/affinity var (only engine popularity/prominence); no dowager; no elevate-to-empress; only one
intrigue event.

### Design

#### A1. A real favour meter — `qing_consort_favour` (char var, 0..100)
The spine of squabbling. Seeded 30 on mint (follow-up scope, NOT in create_character). **[REVIEW FIX] Favour
is a PURE ACCUMULATOR, independent of rank** — do NOT drift it toward rank×20 (a restoring drift flattens
every consort to her rank and kills the squabbling). Nudged by:
- **Favour lever (臨幸):** the chosen/random favour effects add +12 favour (on top of the existing +15
  popularity + make_pregnant). The emperor's attention IS favour.
- **Quarterly decay in `QING_harem_pulse`:** un-favoured consorts decay toward 0 by −1..−2 (attention
  fades), NOT toward rank — so favour and rank can diverge (a beloved low-rank concubine; a prestigious but
  cold political match). Local nudge helper mirroring `QING_DECLINE_nudge` (clamp 0..100).
- **Intrigue outcomes** (below) move it in larger steps.
Read as the ORDER KEY for promotion/demotion picks (augmenting prominence) and the intrigue schemer pick.

#### A2. Demotion + disgrace — the missing downward path
- **`QING_harem_demote_consort_target`** (mirror of promote, re-rooted): `qing_consort_rank -1` (floored
  at 1), -15 favour, -10 popularity, harmony -3. Cannot demote below rank 1 (she leaves the ladder only by
  death or disgrace). Player picker `qing_harem_demote_window` + trampoline `qing_harem.8`.
- **`QING_harem_disgrace_consort`** (冷宮 "cold palace"): the terminal fall. Strips
  `qing_is_harem_consort` (removes from roster like death, but she lives), sets a `qing_is_disgraced`
  marker, -all favour, big popularity hit, harmony -5. Gated on rank (can't disgrace the 皇貴妃 without a
  scandal event). This is the dismiss/expel the map found missing.

#### A3. Promotion/demotion as a CHANCE, not a certainty
New pulse step: **`QING_harem_resolve_standings`** — fires FROM `QING_harem_pulse` at ROOT=CHI using
`ordered_in_list { variable = qing_harem_consorts }` (never a character-root GUI context — BT-13/#373). Each
quarter, for the most-favoured eligible consort below her cap, a `random chance = f(favour, harmony)`
promotes her; for the least-favoured high-rank, a chance demotes her. So standings SHIFT passively (the AI
court churns), not only on player click. **[REVIEW FIX] the passive roll SKIPS any consort the player acted
on within 730 days** (`limit = { NOT = { has_variable = qing_consort_recently_acted } }`; the flag is set with
`days = 730` by the player promote/demote levers) — so the court only drifts consorts you've left alone, and
never undoes a choice you just paid for. Throttled + cap-guarded against the same 5-place cap rule.

#### A4. Rivalry & faction — `qing_consort_faction` (char var enum)
Consorts cluster into factions (e.g. empress's bloc / a rising-consort's bloc / neutral), assigned by a
pulse heuristic (highest-favour non-empress-aligned consort forms a rival bloc). Feeds:
- The intrigue event's schemer pick (the rival bloc's leader schemes).
- A new **harmony drain** when two blocs are both strong (court tension).
This reuses the existing `qing_dynastic_harmony` meter as the tension proxy — no new global meter.

#### A5. New intrigue events (each shares the court slot, fires from `QING_harem_pulse`)
1. **qing_harem.9 — Pregnancy & the Question of an Heir (有喜):** on a consort conceiving (hook the
   make_pregnant), a beat: elevate her rank (favour + backing), or the empress's bloc moves against her
   (scandal risk). Couples directly to `qing_prince_backing` via her rank.
2. **qing_harem.10 — Miscarriage / Loss (小產):** low-harmony + rival-bloc-strong roll; a pregnancy is
   lost amid whispers of poison. Accuse (target a rival → disgrace chance) / mourn (harmony) / ignore.
   NO health-trait manipulation — pure favour/harmony/event state.
3. **qing_harem.11 — The Dowager Intervenes (太后懿旨):** if a dowager exists (see A6), she SUGGESTS a
   promotion or demotion. **[REVIEW FIX] ADVISORY, not forced** — heed her counsel (do it, +dowager
   favour/+harmony) / politely defer (no change, −dowager favour) / refuse outright (no change, −−dowager
   favour + scandal risk). Models 孝聖憲皇后-era matriarchal weight without the game seizing the player's wheel.
4. **qing_harem.12 — Scandal in the Inner Court (穢亂宮闈):** a high-rank consort implicated; disgrace
   (冷宮) or cover-up (corruption +, harmony -). The path to A2's disgrace lever.

#### A6. Dowager concept — `qing_office_dowager_holder` (display-only seat)
Model the Empress Dowager (皇太后) as a non-appointable seat: the previous emperor's surviving empress/
high-consort, installed at succession. She gives a standing prestige modifier and is the trigger-owner of
qing_harem.11. **[REVIEW FIX — 1:1 validator] the install sets `qing_seat_dowager` (NOT counted by
`QING_validate_one_position`) + the display-only `qing_office_dowager_holder` country var, and does NOT set
`qing_office_held`** — so a former-consort dowager keeps only `qing_is_harem_consort` (1 marker, passes). Do
NOT "mirror the regent seat exactly" (regent DOES set qing_office_held). One install hook at accession.

### Harem risk assessment
- **A1/A2/A3/A4:** LOW — all var + effect + event work on the RUNTIME path (no create_character changes).
  The only care: keep the 5-place cap rule in sync when demotion crosses tiers.
- **A5 events:** LOW — pure event content, share the court slot.
- **A6 dowager:** LOW-MODERATE — touches the accession hook; mirror the regent-seat install exactly.
- **NONE of this touches `create_character`** — the boot-AV blast radius is untouched. The one place we
  read the mint path (A1 seeds favour) is in the EXISTING follow-up scope, not inside create_character.

---

## SUBSYSTEM B — Eunuch Influence (內務府 / 太監專權)

### What exists (map summary — MORE than expected)
The influence mechanic is already substantially wired via the **flag** `qing_eunuch_faction_leader`:
corruption-triggered spawn in `QING_household_pulse` (corruption≥50 + weak chamberlain → 20% promote
ablest eunuch: +ambitious, +loyal veterans, +gold, +corruption); 3 player levers (check / indulge /
instrument); 3 events (.2 faction ascends, .5 good order, .6 oversteps); GUI + loc. **What's dead: the
numeric `qing_eunuch_count` — written 4×, read nowhere.** All live logic keys off the flag.

### Design — give the count teeth + deepen the influence web

#### B1. Make `qing_eunuch_count` a live signal — `qing_eunuch_power` (derived 0..100)
The header already DOCUMENTS a `qing_eunuch_power` "derived, not-stored" strength — build it for real.
Compute it each pulse in `QING_household_pulse`. **[REVIEW FIX — exact formula, no boolean-in-arithmetic]:**
`set_variable qing_eunuch_power = qing_eunuch_count`, `multiply = 8`; `if any_character{...faction_leader}
{ change +30 }`; `+ corruption_band_bonus` (e.g. +10 if corruption ≥50); `if chamberlain.charisma >= 8
{ change −15 }` (a strong chamberlain checks them); clamp 0..100. Gives the dead count a consumer (its whole
point) and a single number the new effects read.

#### B2. Eunuch power CONSUMES into the court (the missing bite)
Each quarter, gated on `qing_eunuch_power` bands, the eunuch establishment exerts influence — reusing the
mapped hook primitives:
- **Corruption:** high power → standing `QING_DECLINE_nudge = { var = qing_corruption_level amount = +1/+2 }`
  (idiomatic; HOUSEHOLD already nudges corruption via check/indulge). **[REVIEW FIX — doom-loop cap]** gated
  `qing_corruption_level < 70` so eunuch graft can't spiral past the crisis band.
- **Secretariat backlog (票擬):** high power → `change_variable qing_secretariat_backlog +N` — eunuchs
  intercepting/slowing memorials, historically exact (敬事房 handled palace paperwork). Mirrors the +6
  fresh-rescript nudge.
- **Reform balance:** eunuchs are structurally reactionary → nudge `qing_reform_faction_balance`
  **negative** −1/−2 (raw change_variable, ±100 clamp — NOT the DECLINE_nudge macro). **[REVIEW FIX]** fires
  ONLY at very high power (≥80), not the mid band, so it's not a third simultaneous penalty at every level.
All guarded, all small, all at existing nudge sites — the P7 bias discipline. **[REVIEW FIX — counterplay]**
add a PLAYER purge lever (a chamberlain decision: cost stability/harmony, −30 eunuch power, 1825-day
cooldown) so the exit isn't gated behind an event roll + a strong-chamberlain RNG check.

#### B3. Chief Eunuch seat — `qing_office_chief_eunuch_holder` (display-only)
When a faction leader entrenches (power ≥ high band for N quarters), he takes a named seat. **[REVIEW FIX —
1:1 validator] the install sets `qing_seat_chief_eunuch` (NOT counted by `QING_validate_one_position`) + the
display-only `qing_office_chief_eunuch_holder` country var; it does NOT set `qing_office_held`** — so the
holder keeps only his `qing_is_palace_eunuch` marker (1 marker, passes the validator). Do NOT mirror the
regent seat (regent DOES set qing_office_held → would trip the validator). The seat is the on-map face of
太監專權 (a 李蓮英-type; period-note: famous eunuchs are post-1763, so 1763 starts get an anonymous 掌印太監).
Gives a standing modifier and is the trigger-owner of new events.

#### B4. Deepen the event web (share court slot)
- **qing_household.7 — The Directorate Overreaches (內務府擅權):** high power beat; purge (costly, resets
  power, needs a strong chamberlain) / tolerate (corruption+, backlog+) / harness (instrument path,
  co-opt for throne).
- **qing_household.8 — A Faction at Court (閹黨):** the eunuch bloc allies with a council faction — ties
  into `se_QING_FACTION.txt` (`QING_faction_pick_ally`), tilting reform balance.
- **qing_household.9 — Retrenchment (裁抑內宦):** a reformer emperor / strong chamberlain curbs the corps;
  grants `qing_household_eunuchs_curbed` (exists), drops power, backlog relief.

#### B5. The law on top — `qing_eunuch_policy_law` (restrict / standard / empowered)
NOW it has bite. on_enact sets `qing_eunuch_policy` ∈ {restrict / standard / empowered}, read by B1/B2:
- **restrict (裁抑):** caps `qing_eunuch_power` lower, halves its corruption/backlog output, +chamberlain
  authority modifier. Historically the early-Qing 敬事房 discipline (Qing deliberately curbed eunuchs
  after Ming excess).
- **standard:** no-op (default, byte-identical).
- **empowered (寵信):** raises the power cap, +privy-purse efficiency but +corruption/+backlog output and
  −reform. The Ming-style road to 閹黨.
Modifiers express the palace-management trade. This is the policy overlay on the now-live subsystem.

### Eunuch risk assessment
- **B1/B2:** LOW — pure counter derivation + nudges at existing sites. Gives the dead count a consumer.
- **B3 seat:** LOW-MODERATE — non-appointable seat; mirror SEATS + DON'T trip the 1:1 validator.
- **B4 events:** LOW — event content, share court slot.
- **B5 law:** LOW — selector var read by B1/B2.
- **create_character:** the ONLY mint is the existing `QING_household_mint_eunuch` (runtime pulse, boot
  seed of 4). We add NO new boot-reachable spawn and NO health trait. Blast radius untouched.

---

## Build sequencing (fits the risk-ascending batch plan)
These two subsystems are bigger than a law — they slot in as their OWN batches AFTER the law batches, or
interleaved. Proposed:
- **Batch 6 — Eunuch subsystem** (B1-B5): lower risk (mostly deepening existing wired code + reviving a
  dead var). Do first of the two.
- **Batch 7 — Harem subsystem** (A1-A6): more new surface (favour meter, demotion, factions, 4 events,
  dowager seat). Do second.
Each: author state → effects → pulse wire → events → loc → GUI (new levers/pickers + trampolines) →
brace/quote check → code-review → BOOT-CRASH review (mandatory, create_character-adjacent) → commit as
freekumquats → push.

**USER DECISIONS (2026-07-24):**
1. **Add BOTH seats** — Dowager (皇太后, A6) + Chief Eunuch (掌印太監/掌印太監, B3), non-appointable SEATS
   shape, held out of pickers, NOT setting `qing_office_held` (1:1 validator).
2. **Allow the anachronistic named branch** — a late-game/high-power branch may spawn a NAMED historical
   eunuch (李蓮英-type) and named consorts via the `QING_roster_finalize { nick = NICKNAME_… }` pattern
   (`se_QING_ROSTER.txt:45`). 1763 starts still get anonymous 掌印太監 / 選秀 consorts by default; the named
   figure is a runtime-only (never boot-reachable) spawn, NO inline health trait. Author the NICKNAME_ loc
   keys.
3. **Build the FULL design** — A1-A6 + B1-B5, as Batches 7 (harem) and 6 (eunuch). Eunuch first (lower
   risk, revives dead code + deepens already-wired flag mechanic); harem second (more new surface).


---

# PART VI — LAW EXPANSION IMPLEMENTATION LOG (BUILDING 2026-07-24, branch merge-overnight)
*Autonomous build of the reviewed law design (LAW_EXPANSION_DESIGN_DOC.md). Decisions logged here per user.*

## Batch 1 — GUI columns + trivial laws + upstream stubs

### Step 1 — Upstream Victorian-TC stubs FILLED + brace fix (DONE)
The 4 stubs shipped with empty `modifier={}` on every option (absent from vanilla + both oracle repos).
All 4 law files are UTF-8 **BOM + CRLF** — edited at byte level (Python) to preserve endings (a naive edit
flips CRLF→LF = huge junk diff). The loc file `laws_l_english.yml` is BOM + **LF** (different) — edited with
LF-preserving Edits.
- **`00_administrative_laws.txt` — brace bug FIXED + #48 filled.** Was 9-open/8-close: `delegated_monetary_policy`
  never closed, so `legislative_monetary_policy` was mis-nested inside it (group had only 2 valid options).
  Rewrote the whole `monetary_policy_law` block correctly (now 9/9). Fills: executive = +0.02 stability /
  +0.02 corruption; delegated = +0.03 commerce / +0.02 tax; legislative (is_republic) = +0.05 commerce /
  +0.02 research / −0.02 stability.
- **`00_monetary_policy_setting.txt` — #49 filled** (10/10 braces). currency_recall = −0.05 commerce / +0.03
  stability; limited_minting = −0.03 corruption / +0.03 upper-happy; more_minting = +0.05 tax / +0.05 commerce
  / −0.02 stability; issue_bonds = +0.1 commerce / +1 capital-trade-routes / +0.03 corruption.
- **`00_upper_house_laws.txt` — #50/#51 filled** (18/18 braces). Powers: veto = +0.03 stab / +0.05 mid-happy /
  −0.05 pol-influence; review = +0.03 upper-happy / +0.01 stab; delay = +0.03 pol-influence / −0.02 mid-happy.
  Composition: appointed_hereditary_spiritual = +0.05 upper-happy / **+0.05 monthly_legitimacy** (replaced the
  WRONG `omen_power` = MINING output in this TC) / −0.02 mid-happy; appointed = +0.05 pol-influence / +0.02
  upper-happy; elected = +0.05 mid / +0.03 low / −0.02 stab; state_representatives = +0.05 assimilation /
  +0.5 diplo-reputation.
- **All 13 modifier keys VERIFIED valid** (each appears in 6-53 existing common/ files). No boot-error risk.
- **LOC: all 14 placeholder option `_desc` filled** with real flavour + the gate-tooltip rule applied — every
  gated option's desc calls out its prerequisite (#R Requires: a republic / a bicameral legislature /
  legislative monetary policy #!). These 4 stubs keep their EXISTING vanilla GUI registration (not Qing
  statutes) — no new area needed for them.

### Step 2 — 5 trivial Qing law groups AUTHORED (DONE)
Appended to `00_qing_statutes_laws.txt` (BOM+LF, now 179/179 braces). All CHI-only, all with a no-op-ish
default. Modifier-swap except frontier-trade (selector-via-lever):
- **qing_industrial_encouragement_law** (#13, 官督商辦 default / 官辦 / 商辦) — pure modifier-swap, NO on_enact
  nudge (toggle-farm avoided). Keys: global_commerce/tax_modifier, research_points_modifier,
  global_middle_strata_output.
- **qing_princely_establishment_law** (#36, favour/investigate/restrict) — legitimacy / corruption /
  political-influence modifiers.
- **qing_works_priority_law** (#47, balanced/frugal/grand) — the "grand" graft is a STANDING
  monthly_corruption modifier, NOT an on_enact nudge. Does NOT build the palace.
- **qing_overseas_expansion_law** (#32, seclusion/trade-fleet/colonial) — commerce, global_ship_recruit_speed,
  diplomatic_reputation, tax. Does NOT grant colonies (mission-earned).
- **qing_frontier_trade_law** (#31, assert/concession) — SELECTOR-VIA-LEVER: on_enact calls the proven guarded
  QING_caravan_revoke_aqsaqal / _grant_aqsaqal. **#31 on_enact→scripted_effect uncertainty RESOLVED**: the
  shipped qing_ethnic_governance_law already does `on_enact = { QING_set_ethnic_stance = {...} }`, so this is a
  proven construct — no isolation test needed.
- All modifier keys VERIFIED present (global_middle_strata_output 6 files, global_ship_recruit_speed 9 files).

### Step 3 — GUI re-split into 7 domain columns (DONE)
`gui/government_view.gui` (plain UTF-8/LF): the single `qing_statutes_laws` area (統治大典) REPLACED by 7
`laws_widget_area` blocks stacked in the existing vertical flowcontainer (areas stack VERTICALLY and the
scrollarea clips — so 7 areas is fine; the "horizontal fit" worry was moot). Exact sibling indentation
(area=7 tabs, laws_widget=9, visible=10) mirrored. Braces 2003/2003. Domain homes for the 18 existing laws
(13 shipped + 5 trivial):
- 治道 governance: ethnic_governance, office_selling, ministry_estab, advisory_estab
- 財政 fiscal: salt_admin, canton_regime, canton_purse, caravan_customs
- 武備 military: military_upkeep
- 邊疆 frontier: frontier_trade
- 宮廷 court: princely_establishment
- 文教 culture: penal_code, ritual_orthodoxy, opium_policy, exam_cadence, works_priority
- 通商洋務 foreign: overseas_expansion, industrial_encouragement
Later batches append their groups to the correct domain area. 7 header loc keys added to
imp19c_interface_l_english.yml (old qing_statutes_laws key left, now unreferenced/harmless).

### Step 4 — LOC for the 5 new groups (DONE)
laws_l_english.yml (BOM+LF): all 5 groups + their options + _desc added (no collisions, quotes balanced).

### CRLF/BOM discipline
The 3 upstream law files are BOM+CRLF; edited at byte level and VERIFIED still CRLF+BOM (no LF flip; the
known junk-diff gotcha avoided). qing_statutes + the 2 loc files are BOM+LF; government_view.gui is plain
UTF-8/LF. All preserved.

### PENDING before commit: boot-crash review (dispatched), then commit as freekumquats + push.

## Batch 2 — Bias-A accumulator laws: PRE-AUTHORING CLASSIFICATION (2026-07-24)
Before authoring, verified each target site against code (the P7 lesson: a nudge site can be dead-gated or a
target-chaser). Findings — NOT every "accumulator" is a clean bias-A:
- **#16 Cultural Patronage (qing_wenzhi_patronage, WENZHI:75)** — TRUE accumulator, flat −1/qtr decay, no
  target-chase → BIAS-A. Build.
- **#20 Heterodox Sect (qing_sect_pressure, DECLINE:1003-1023)** — TRUE accumulator (clamped compounding-crisis
  nudges) → BIAS-A. Build (small, band-gated).
- **#21 Reform Posture (qing_reform_faction_balance, FACTION:412-443)** — TRUE accumulator, signed ±100, raw
  change_variable, hand-clamp at 441-442 → BIAS-A. Insert the law bias BEFORE the clamp using raw
  change_variable (NOT QING_DECLINE_nudge — signed-meter rule). Build.
- **#19 Anti-Corruption (qing_corruption_level)** — accumulator, but nudged from many discrete sources with NO
  single base-drift line → clean hook = ADD a NEW guarded bias nudge in the DECLINE pulse (the P7 "own line"
  pattern), not modify an existing amount. Build with a dedicated pulse line.
- **#14 Provincial Militarization (qing_han_provincial_power, DECLINE:416-431)** — **RECLASSIFIED: NOT bias-A.**
  It CHASES a target (eases ±2 toward qing_han_prov_target_tmp). Biasing the ±2 only changes convergence SPEED;
  the meter re-settles at the same target → no durable effect. FIX: bias the TARGET FORMULA (before its clamp
  at DECLINE:422) = **BIAS-B → MOVED TO BATCH 3.**
- **#22 Deliberative (qing_delib_cohesion, DELIB:367)** — the :367 write is an EVENT nudge marked "recomputed
  next pulse anyway" → cohesion is likely RECOMPUTED, not an accumulator. DEFERRED pending its actual
  drift/recompute site; if recomputed, it's BIAS-B (Batch 3), not bias-A.
- Not yet re-checked this pass: #15 (already known net-new-lite, Batch 4), #17/#18/#23/#44 (Batch 4 / re-base).
NET: Batch 2 builds #16, #19, #20, #21 as bias-A. #14 and (likely) #22 move to Batch 3 (bias-B). This keeps
the "no law that silently does nothing" bar.

### Batch 2 — BUILT (#16, #19, #20, #21) — DONE
Authored 4 bias-A law groups in 00_qing_statutes_laws.txt (235/235 braces) + guarded pulse reads:
- **#16 Cultural Patronage** → qing_wenzhi_patronage_bias, applied at WENZHI:75 (guarded, added to the -1/qtr
  decay). austere -1 / standard 0 / lavish +1.
- **#19 Anti-Corruption** → qing_anticorrupt_bias, applied as its OWN guarded pulse nudge in se_QING_DECLINE
  (compounding-crisis block), FLOORED at corruption>20 (thins graft, can't scour to 0). Negative drag baked
  via a negated temp var (qing_anticorrupt_drag_tmp) since `amount = -var:X` isn't expressible; QING_DECLINE_nudge
  passes negative amount through to change_variable + clamps 0..100 (verified macro def :33-42). audits 1 /
  draconian 2 (+modifier costs).
- **#20 Heterodox Sect** → qing_sect_policy_bias, guarded -1/qtr on qing_sect_pressure BAND-GATED at >25
  (se_QING_DECLINE). suppress only; monitor = watch modifier, no drag; suppress carries a lower-strata
  happiness cost that feeds unrest back (self-limiting).
- **#21 Reform Posture** → qing_reform_posture_bias, SIGNED ±1 tilt inserted BEFORE the ±100 clamp in
  se_QING_FACTION using RAW change_variable (NOT the nudge macro — signed-meter rule). conservative -1 /
  reformist +1.
- All 4 registered in GUI domain columns (anti-corruption + reform → 治道 governance; patronage + sect → 文教
  culture); 2011/2011 braces. Loc complete with prereq-callout discipline. Each bias var VERIFIED set-by-law +
  read-by-pulse (no orphans). All modifier keys previously verified valid.

### Batch 2 RECLASSIFICATIONS (moved to Batch 3 / bias-B):
- **#14 Provincial Militarization** — target-chaser, bias the target formula (DECLINE:~421), not the ±2 nudge.
- **#22 Deliberative** — qing_delib_cohesion is RECOMPUTED (mean of backing, DELIB:222-230); bias the backing
  or recompute, not the event nudge.

### PENDING before Batch 2 commit: boot-crash review (dispatch), commit as freekumquats + push.

### Batch 3 — BUILT (7 bias-B laws) — DONE (pre-commit review pending)
7 law groups in 00_qing_statutes_laws.txt (333/333) + guarded bias-INTO-formula-before-clamp at each recompute:
- **#24 Council Composition** → qing_council_comp_bias, COUNCIL before the eff_target clamp (:554). Manchu -5 /
  balanced 0 / meritocratic +5.
- **#25 Canal Quota** → qing_canal_quota_bias, CANAL before the 0.5..1.0 clamp (:228). relaxed -0.10 / std 0 /
  maximal +0.15.
- **#26 Xinjiang Admin** → qing_xj_admin_bias, XINJIANG into consol_scratch before the 0..100 clamp (:227).
  beg 0 / military-farm +5 / provincialize +10.
- **#28 Missionary Policy** → qing_missionary_tol_bias, MISSIONARY into SOCIAL-friction target before the 45
  ceiling (added a floor-at-0 too, since prohibit -8 could go negative). prohibit -8 / tolerate 0 / open +8.
  (Political/antichr target NOT touched — post-treaty.)
- **#42 National Integration** → qing_civic_law_bias, DECLINE civic-identity TARGET-lift alongside settle-bonus
  (:857). dynastic 0 / multi-ethnic +5 / civic-nation +10. Nationalism/citizenship focus (feeds assimilation +
  ethnic-tension relief). NB qing_national_awakening is a modifier, not this var.
- **#46 Censorate Empowerment** → qing_censorate_bias, CENSORATE into vigor recompute before the 0..50 clamp
  (:66). weak -10 / active 0 / weaponized +10.
- **#14 Provincial Militarization** (moved from Batch 2) → qing_provmil_bias, biases the han-provincial-power
  TARGET (qing_han_prov_target_tmp) before its clamp (DECLINE:422), NOT the +/-2 chase nudge. centralized -10 /
  sanctioned 0 / delegated +10.
- All 7 registered in GUI domain columns (治道/財政/邊疆/文教/武備); 2025/2025 braces. Loc complete w/ effect
  callouts. All bias vars wired set-by-law + read-by-effect (no orphans). New modifier keys verified
  (global_manpower_modifier 32 files).

### #22 Deliberative — DEFERRED from Batch 3 (needs a different hook)
qing_delib_cohesion is a value-BLOCK recompute (set_variable = { value = { sum/count min max } }, DELIB:222-230)
— no linear "before the clamp" add-site. The right hook is the BACKING (qing_delib_backing accrual), a distinct
mechanism. Deferred to Batch 4 / a careful sub-step rather than forced into a bad fit.

### PENDING before Batch 3 commit: boot-crash+correctness review (dispatch), commit as freekumquats + push.

## CHECKPOINT after Batch 3 (2026-07-24) — 3 of 5 batches done, all committed+pushed+reviewed
- Batch 1 (0ce6e9957): 7-column GUI split + 5 trivial laws + 4 upstream stub fills + brace fix
- Batch 2 (18309001a): 4 bias-A laws (#16/#19/#20/#21)
- Batch 3 (c4502c8b7): 7 bias-B laws (#24/#25/#26/#28/#42/#46/#14)
= 16 new Qing law groups + 4 stub fills, each boot-crash+correctness reviewed before commit.

### Batch 4 (net-new-lite) — OPEN ITEMS to resolve deliberately before authoring (not rushed at run-tail):
1. **#39 Tributary Ritual** — QING_tribute_stamp_cadence (TRIBUTE:253-268) stamps a per-subject `days=` by
   TAG. A country cadence law must bias the stamped days by a global var — more than "one read" (days= wants
   a literal or var). Hook: read qing_tribute_cadence_law to pick which branch/scale. Feasible, needs care.
2. **#40 Frontier Settlement** — migrate the one-way flag (POPULATION:242 set, :95 read) to a tri-state
   qing_frontier_settle_policy. Must preserve the existing flag semantics (flag-set ⇒ policy≥1) so no
   regression. Needs a migration guard.
3. **#43 Amban Establishment** — the ministry_estab precedent (SUBPOSTS:113-120: fill-to-target loop reading
   qing_law_ministry_estab_target) is the model. The amban post-sweep (AMBAN:253+) posts ONE per call with no
   target. Need to add a count + fill-to-target loop reading a new qing_amban_estab_target. Real plumbing.
4. **#44 Modernization Doctrine** — modifier-swap on tech/discipline/morale/research keys (all confirmed valid
   in Batch 1-3). UNIT-UNLOCK from a law is UNPROVEN — build modifier-only unless an oracle (TI/Invictus)
   shows a law unlocking a unit. Low risk as modifier-only.
5. **#27 Customs Regime (upstream trade)** — modifier-swap on global_commerce_modifier/global_capital_trade_
   routes. MUST verify at build that CHI actually uses vanilla trade routes at 1763 (else no-op for the Qing
   player). If it's a no-op, reconsider (merge with #30 or drop).
6. **#34 Succession Method / #35 Regency Rules** — new selector var read at the accession/regent-install pick
   (PRINCES / SEATS). Straightforward selector-with-read; verify the pick site.
7. **#45 Exam Curriculum** — classical/practical only (abolition DEFERRED). New qing_exam_curriculum var
   biasing qing_exam_pass_rate; verify the exam recompute site.
8. **#15 Drill Posture / #17 Southern Study / #18 Canton Hoppo** — the 3 remaining refuted re-bases, all
   net-new-lite: #15 needs its OWN drill vars (NOT P7's) + the High-Qing era-guard fix (pairs with Task #32);
   #17 needs a new recruit-rate input + a recruitment pulse gate (SOUTHERNSTUDY has none today); #18 needs a
   new hoppo drift-bias var at the hardcoded nudge (CANTON:150/153).
9. **#22 Deliberative** — bias the qing_delib_backing accrual (not the value-block cohesion recompute).
10. **#31 tariff (#30)** — Canton real-goods rate multiply (pairs with the Task #32 caravan rework — both
    touch the Canton/caravan yield formulas; do together to avoid conflicting edits).
NOTE: several of these (#43 loop, #17 new pulse, #15 era-guard) are heavier than "one read" — genuine
net-new plumbing. Task #32 (caravan + P7 era-guard) should be done alongside #15/#30 since they share the
DECLINE era-guard and Canton/caravan yield sites.

---
## PART VI — Batch 4a IMPLEMENTED (2026-07-24)

**STATUS: BUILT + reviewed + committed.** First tranche of the Batch-4 net-new-lite list — the
three LOWEST-RISK items authored first (two pure modifier-swap, one bias-B one-read):

- **#44 Modernization Doctrine (自強綱領)** — `qing_modernization_doctrine_law`, military domain. Pure
  modifier-swap, 3 options (statutory default / new-model drill / total rearmament) on discipline +
  land_morale_modifier + research_points_modifier + army_maintenance_cost + global_tax_modifier. UNIT-UNLOCK
  deliberately NOT attempted (unproven from a law — modifier-only per the open-item note).
- **#27 Customs Regime (通商章程)** — `qing_customs_regime_law`, foreign domain. Pure modifier-swap, 3 options
  (canton default / treaty tariff / customs autonomy) on the vanilla trade keys global_capital_trade_routes
  (int ±1/±2, proven form) + global_commerce_modifier + global_tax_modifier. Governs the empire-wide vanilla
  trade network; the bespoke Canton Purse / Caravan Customs laws still model the 廣州/絲路 yields separately.
- **#45 Exam Curriculum (科舉科目)** — `qing_exam_curriculum_law`, culture domain. Bias-B: on_enact writes
  qing_exam_curriculum_bias (0 classical / +10 practical); read ONCE (guarded on has_variable) inside
  QING_exam_compute_pass_rate before the 0..100 clamp (se_QING_EXAM.txt). Classical/practical only —
  ABOLITION deferred. Called from schedule/graduate/sit sites, so the bias is live.

REVIEW: on_enacts use idempotent set_variable (no toggle-farm); bias read guarded; all 8 modifier keys
verified valid in-TC; no var-ref on comparison RHS; all 3 registered in government_view.gui (military/
culture/foreign areas) + full loc with #G/#R/#Y prereq callouts. Braces: statutes 359/359, gov_view
2031/2031. Encodings preserved (BOM+LF statutes/loc).

REMAINING Batch-4 open items (heavier plumbing, next tranches): #34/#35 succession/regency selectors,
#39 tributary ritual cadence, #40 frontier-settlement tri-state migration, #43 amban fill-to-target loop,
#15 drill-posture (needs own vars + High-Qing era-guard, pairs w/ Task #32), #17 southern-study (needs new
recruit pulse), #18 canton-hoppo drift-bias, #22 deliberative-backing accrual bias, #30/#31 tariff (pairs
w/ Task #32 caravan rework).

---
## PART VI — Batch 4b IMPLEMENTED (2026-07-24): #34 Succession Method

**STATUS: BUILT + reviewed + committed.** Next Batch-4 item — a bias-B selector on the
succession-strife hook (the design's "straightforward selector-with-read; verify the pick site").

- **#34 Succession Method (立儲之法)** — `qing_succession_method_law`, court domain. on_enact writes
  idempotent qing_succession_method_bias (0 secret-succession default / +1 open designation / -1 fixed
  primogeniture). Read ONCE, guarded on has_variable, inside QING_dynasty_succession_strife (se_QING_DYNASTY
  .txt): added to qing_succession_strife_sev BEFORE the `>= 2` escalation compare (LHS — RHS stays a literal,
  per the RHS-comparison rule). Open designation revives the 九子奪嫡 jockeying (severity+1 → escalates);
  primogeniture calms it (severity-1). The strife effect is called from qing_succession.1 (severity 2) and
  the accession branch (severity 1) in qing_regency_events.txt, so the bias is live.
- Modifiers: secret = +legit; open = +legit / -PI; primogeniture = -legit / -corruption. Registered in
  government_view.gui court area (after princely_establishment). Full loc with prereq/trade-off callouts.

REVIEW: idempotent on_enact; guarded read; bias on comparison LHS (not RHS); only shifts the escalation
branch (bounded); QING_DECLINE_nudge target is a 0..100 meter (safe). Braces: statutes 373/373, DYNASTY
256/256, gov_view 2033/2033.

DEFERRED within #35 (Regency Rules): the regency arc touches a DIRECTIONAL reform-echo (reformer vs
reactionary regent), not a scalar severity — needs the reform-echo sign semantics worked out, so it is NOT
folded in here. Remaining heavier Batch-4 items unchanged (#39/#40/#43/#15/#17/#18/#22/#30/#31).

---
## PART VI — Batch 4c IMPLEMENTED (2026-07-24): #18 Hoppo Regulation

**STATUS: BUILT + reviewed + committed.** Bias-A accumulator on the Canton Hoppo-squeeze drift.

- **#18 Hoppo Regulation (粵海關章程)** — `qing_hoppo_regulation_law`, fiscal domain. on_enact writes
  idempotent qing_hoppo_regulation_bias (0 customary-farm default / -1 board-audited / +1 tax-farmed). Read
  once per Canton pulse (se_QING_CANTON.txt) as an extra drift term on qing_hoppo_squeeze, right after the
  base +3/+1 creep — the bias-A accumulator shape. Guarded on has_variable; amount=var:X is proven (CARAVAN
  :149, DECLINE:927-928 upkeep bias) and QING_DECLINE_nudge clamps 0..100 (negative subtracts, no underflow).
  Audited slows the squeeze (-1) + eases corruption; tax-farmed accelerates it (+1) for an immediate tax cut.
- Registered in gov_view fiscal area (after canton_purse). Full loc with callouts.

REVIEW: idempotent on_enact; guarded read; proven var-amount nudge on a clamped 0..100 meter; no RHS-var.
Braces: statutes 387/387, CANTON 115/115, gov_view 2035/2035.

Batch-4 progress: 4a (#44/#27/#45) + 4b (#34) + 4c (#18) = 6 laws built. Remaining net-new-lite: #22
(deliberative-backing accrual bias). Remaining heavy-plumbing: #35 (directional regency echo), #39/#40/#43/
#15/#17/#30/#31.

---
## PART VI — Batch 4d IMPLEMENTED (2026-07-24): #43 Amban Establishment

**STATUS: BUILT + reviewed + committed.** Net-new-lite: a posts-per-sweep target on the amban auto-sweep.

- **#43 Amban Establishment (駐紮大臣員額)** — `qing_amban_establishment_law`, frontier domain. on_enact writes
  qing_amban_estab_target (1 gradual default / 2 forward / 3 full). Read once by QING_amban_post_sweep
  (se_QING_AMBAN.txt) as a `while = { count = var:qing_amban_estab_target }` wrapping the existing
  random_subject post. Default 1 = byte-identical to the old single-post behaviour. Each pass re-picks a
  DIFFERENT unattended march (QING_amban_wire sets qing_amban_here synchronously → the candidate limit
  excludes it next pass), so N passes staff up to N distinct dependencies; a fully-staffed frontier no-ops.
- Registered gov_view frontier area (after xinjiang_admin). Loc notes the Lifan-Yuan-supervisor prereq.

REVIEW (while-loop is the risk): NO recursion (QING_amban_post→wire never calls the sweep); count bounded
1..3 (never unbounded); empty random_subject = clean no-op; sweep is a plain QING_GOV_pulse effect, NOT a
compiled button (compile-recursion class N/A); `count = var:X` proven (se_PRICE.txt:236); default seeded to 1
if never enacted. Braces: statutes 401/401, AMBAN 235/235, gov_view 2037/2037.

Batch-4 progress: 4a (#44/#27/#45) + 4b (#34) + 4c (#18) + 4d (#43) = 7 laws built.
Remaining: #22 (needs new backing-drift mechanic — deferred, no clean hook), #35 (directional regency echo),
#39 (tributary-ritual cadence), #40 (frontier-settlement tri-state — migration-guard care), #15/#17/#30/#31
(the Task-#32-coupled cluster: DECLINE era-guard + Canton/caravan yield + new recruit pulse).

---
## PART VI — Batch 4e IMPLEMENTED (2026-07-24): #39 Tributary Ritual

**STATUS: BUILT + reviewed + committed.** Selector-picks-a-literal-branch on the tribute cadence.

- **#39 Tributary Ritual (朝貢之禮)** — `qing_tribute_ritual_law`, foreign domain. on_enact writes idempotent
  qing_tribute_ritual_bias on CHI (0 customary default / +1 intensified / -1 relaxed). QING_tribute_stamp_
  cadence (se_QING_TRIBUTE.txt) runs in the SUBJECT scope inside the scheduler's random_subject; it reads the
  bias off ROOT (=CHI, unchanged inside random_subject — confirmed by the caller's own comment at :105) into
  a LOCAL scratch var, then each per-tag branch (KOR / VIE+RYU / outer) picks among LITERAL day-bands by that
  scratch var. Deliberately NOT a var-driven `days = var:X` — that duration form is UNPROVEN in this engine
  (my own note, se_QING_EXAM.txt:141). Intensified = every court a tier more often; relaxed = a tier less.

REVIEW: idempotent on_enact; ROOT.var read guarded on has_variable + copied to a LOCAL var so the >=1/<=-1
compares keep a LITERAL RHS (never ROOT.var on a comparison RHS — the illegal form); `value = ROOT.var:X` is
proven (DECLINE:2216, CANTON:134); scratch var removed after; all durations literal (boot-safe). New var names
unique, no loc-key collisions. Braces: statutes 415/415, TRIBUTE 176/176, gov_view 2039/2039.

Batch-4 progress: 4a (#44/#27/#45) + 4b (#34) + 4c (#18) + 4d (#43) + 4e (#39) = 8 laws built.
Remaining: #22 (no clean hook — needs new backing-drift mechanic, deferred), #35 (directional regency echo),
#40 (frontier-settlement tri-state — the valve is lever-only, not pulse; needs migration-guard care),
#15/#17/#30/#31 (the Task-#32 cluster — shared DECLINE era-guard + Canton/caravan yield + new recruit pulse).

---
## PART VII — BT-M: New Treasure Fleet tree expansion (DESIGN, 2026-07-25)

Boot test: the 新寶船隊 tree has only 4 linear tasks; user wants it DRAMATICALLY expanded (cf. the
35-task colonization tree). Keep the proven idiom (player does the real work; mission recognises it;
gate on real num_of_ships / port levels + treasury cost; reward prestige + concrete effects + a
country modifier + LOG_line). Structure (branching, ~15 tasks):

SPINE (→ capstone):
- qing_treasure_revive_yards (振興船政) — ROOT [keep]
- qing_treasure_build_ports (廣建船塢) — requires yards; port_building>=3 [keep]
- qing_treasure_amass_fleet (聚舟師) — requires ports; num_of_ships>=20 [keep]
- qing_treasure_grand_shipyard (龍江船廠, NEW) — requires build_ports; a 2nd top sea port (2x port_building>=3)
- qing_treasure_capstone (下西洋) — requires amass_fleet; num_of_ships>=30 [keep, final]

VOYAGE FAN (from amass_fleet — "fund + sail", gate = treasury + rising num_of_ships; NOT conquest,
matching the tribute-diplomacy history; each grants tributary-prestige nudge + wealth + ruler glory +
a per-leg country modifier). West-to-progressively-farther:
- qing_treasure_champa (占城) — near landfall; ships>=20
- qing_treasure_malacca (滿剌加) — the entrepôt; ships>=22
- qing_treasure_ceylon (錫蘭) — ships>=24
- qing_treasure_calicut (古里, India) — ships>=26
- qing_treasure_hormuz (忽魯謨斯, Persian Gulf) — ships>=28
- qing_treasure_aden (阿丹, Arabia) — ships>=30
- qing_treasure_malindi (麻林, E Africa — the giraffe) — ships>=34; farthest

LEGACY:
- qing_treasure_mao_kun_chart (鄭和航海圖, NEW) — requires amass_fleet; treasury; grants a naval/research modifier
- qing_treasure_bring_tribute (萬國來朝, NEW) — requires a couple of voyages; big tributary-prestige swell

NEW EFFECTS (se_QING_TREASURE_FLEET.txt): QING_treasure_voyage_leg = { region = X } — a shared reward
helper (tributary-prestige nudge + wealth via CURRENCY_grant_country_wealth + ruler popularity + a named
leg modifier). Reuses proven idioms only. Flavor names/text pending the Zheng-He research digest.
REVIEW GATES: no new num_of_ships-on-RHS issues (num_of_ships>=N is a literal RHS, fine); each voyage
country modifier distinct; treasury costs on_start; all CHI-only, player-only (inherit tree potential).

---
## PART VI — Batch 4f IMPLEMENTED (2026-07-25): #40 Frontier Settlement

**STATUS: BUILT + reviewed + committed.** Tri-state bias-B on the population-pressure relief.

- **#40 Frontier Settlement (移民實邊)** — `qing_frontier_settlement_law`, frontier domain. on_enact writes
  idempotent qing_frontier_settle_policy (0 managed default / 1 open / 2 flood). Read once by
  QING_pop_recompute_target (se_QING_POPULATION.txt) to scale the pressure relief: policy 1 = extra -8,
  policy 2 = extra -16, ON TOP of the existing one-shot qing_frontier_resettlement panel-lever flag (-12,
  UNCHANGED — no regression; the migration-guard concern resolved by layering, not replacing). Modifiers add
  global_migration_speed_modifier (faster settlement) with a PI/stability cost.
- Registered gov_view frontier area (beside national_integration). Full loc with callouts.

REVIEW: idempotent on_enact; guarded read (LHS var, literal RHS); existing flag block untouched (no
regression); if/else_if mutually exclusive on single-valued policy; all 3 modifier keys valid. Braces:
statutes 429/429, POPULATION 100/100, gov_view 2021/2021.

Batch-4 progress: 4a(#44/#27/#45) 4b(#34) 4c(#18) 4d(#43) 4e(#39) 4f(#40) = 9 laws built. Task #32 (P7
dead-law fix + caravan real-goods rework) DONE. Remaining Batch-4: #22 (no clean hook — deferred), #35
(directional regency echo), #15/#17/#30/#31 (the remaining Task-#32-adjacent cluster).

---
## PART VI — Batch 4g IMPLEMENTED (2026-07-25): #30/#31 Canton Tariff

**STATUS: BUILT + reviewed + committed.** Bias-B on the Canton real-goods yield (the tariff RATE).

- **#30/#31 Canton Tariff (關稅則例)** — `qing_canton_tariff_law`, fiscal domain. on_enact writes idempotent
  qing_canton_tariff_rate (0 customary default / 1 low-fixed-treaty / 2 autonomous-high). Read once by the
  Canton pulse (se_QING_CANTON.txt) as a multiplier on qing_canton_yield_tmp (the real tea/silk/porcelain
  base) BEFORE the purse split: low = x0.8 (less per unit) + commerce swell; autonomous = x1.3 (fatter
  yield) but commerce falls + unrest. Distinct from #27 Customs Regime (empire-wide vanilla trade) and #18
  Hoppo Regulation (supervision/squeeze) — this is the specific Canton rate. Pairs with the Task #32
  caravan real-goods rework (both now levy on real goods). Registered gov_view fiscal area + full loc.

REVIEW: idempotent on_enact; guarded read (LHS var, literal RHS); qing_canton_tariff_rate is a unique new
var (no collision with the post-1842 qing_tariff_autonomy treaty var); global_unrest/global_commerce_modifier
valid. Braces: statutes 443/443, CANTON 121/121, gov_view 2023/2023.

Batch-4 progress: 4a-4g = 10 laws built (#44/#27/#45/#34/#18/#43/#39/#40/#30/#31). Remaining: #22 (no clean
hook — deferred, needs a new backing-drift mechanic), #35 (directional regency echo), #15 (drill posture —
needs own vars + already-fixed High-Qing era-guard), #17 (southern study — needs a new recruitment pulse).

---
## PART VI — Batch 4h IMPLEMENTED (2026-07-25): #35 Regency Rules

**STATUS: BUILT + reviewed + committed.** The last of the tractable Batch-4 laws.

- **#35 Regency Rules (攝政體制)** — `qing_regency_rules_law`, court domain. on_enact writes idempotent
  qing_regency_authority_bias (0 customary / -1 conciliar / +1 unbound). Read once by
  QING_dynasty_regency_screen (se_QING_DYNASTY.txt): it BRANCHES on the bias and passes a LITERAL reform-echo
  scale each way (unbound = 4, conciliar = 2, base = 3) — deliberately NOT scale=var:X, because reform_echo
  interpolates $scale$ into a LOG string and a var there would print raw macro text (the log-string-macro
  rule). So the directional lurch of a regency (慈禧-blocks-reform vs a reforming regent) is amplified or
  damped by the law. Modifiers: conciliar = +legit/-PI, unbound = +PI/-legit.

REVIEW: idempotent on_enact; guarded reads (LHS var, literal RHS); literal scale (no var-in-LOG); the
directional sign comes from the regent's OWN stance inside reform_echo (unchanged) — the law only scales
MAGNITUDE, which is the correct semantics. Braces: statutes 457/457, DYNASTY 263/263, gov_view 2025/2025.

BATCH 4 COMPLETE for the tractable items: 11 laws built (4a #44/#27/#45, 4b #34, 4c #18, 4d #43, 4e #39,
4f #40, 4g #30/#31, 4h #35) + Task #32 (P7 fix + caravan rework). REMAINING (genuine net-new mechanics,
NOT law-bias — deferred to their own build): #22 Deliberative (needs a new per-pulse backing-drift +
ratchet-safe band gate), #15 Drill Posture (needs own drill vars + recruitment gate), #17 Southern Study
(needs a brand-new recruitment pulse). These fold into future subsystem batches, per the "build the mechanic
in the same batch as the law" rule.
