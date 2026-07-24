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

**DEFERRED — pulse-COMPUTED output meters (a law would fight the pulse; would need a decoupling redesign, out of scope):**
- qing_wenzhi_patronage — decays -1/quarter in QING_wenzhi_pulse (a meter, not a knob).
- qing_customs_efficiency / qing_customs_eff_target — QING_DECLINE_nudge'd; the target MIRRORS the meter.
- qing_council_eff_target / qing_council_dyarchic_balance — recomputed from live councillor skills each pulse.
- qing_modernarmy_share, qing_banner_decay*, qing_greenstandard_decay*, qing_han_provincial_power — decline-pulse
  computed shares/decay; their modifiers (qing_banner_decay_mild etc.) are pulse-applied bands, not policy toggles.
- qing_corruption_level, qing_sect_pressure, qing_reform_faction_balance, qing_selfstr_progress — decline/progress meters.
- qing_canal_jiangnan_quota — recomputed from LIVE map region ownership every pulse (geography, not policy).
- qing_currency_stress / qing_tariff_autonomy / qing_customs_foreign_control — event-driven crisis/treaty meters (output).
- qing_xj_consolidation / qing_xinjiang_control — recomputed from the live beg corps + map each pulse.

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
