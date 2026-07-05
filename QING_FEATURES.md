# The Qing Player Experience — Feature Documentation

*Imperatrix: Victoria* — the Qing (CHI) mechanics suite

This document catalogues the player-facing systems built for a Qing playthrough,
with references to (a) the code that implements each and (b) the historical basis
it models. Everything here is **CHI-only and player-only**: every interaction sets
`ai_is_valid = { always = no }` or gates on `is_ai = no`, so the AI never touches
these systems. All effects are instrumented with the shared logging module
(`se_LOG.txt`); traces land in `game.log` under `[IMP19C][QING]` / `[IMP19C][SUBJ]`
and cost nothing outside `-debug_mode`.

---

## 0. Cross-cutting infrastructure

### 0.1 The logging module — `common/scripted_effects/se_LOG.txt`
A thin wrapper over `debug_log` used by the whole suite:
`LOG_line`, `LOG_enter`, `LOG_exit`, `LOG_fail`, `LOG_state`. Every message is
`"[IMP19C][$sys$] …"`; `$sys$` is `QING` for the Qing systems and `SUBJ` for the
subject-interaction system. `debug_log` only emits in `-debug_mode`, so these are
zero-cost in a normal game.

### 0.2 The decline state engine — `common/scripted_effects/se_QING_DECLINE.txt`
The design keystone. Rather than sweeping pops/provinces, every "dynastic health"
axis is a plain **0..100 counter variable on CHI**, nudged **event-driven** and read
**O(1)** by a single throttled monthly pulse that swaps in the modifier band matching
each counter's current value. This is why the whole suite stays cheap.

* `QING_DECLINE_nudge = { var = <name> amount = <±N> }` — the generic clamped (0..100)
  nudge used by *every* counter across the suite; auto-initialises the variable to 0
  and logs the change.
* Counters: `qing_corruption_level` (D), `qing_sect_pressure` (G),
  `qing_banner_decay` (C), `qing_ethnic_tension` (#1), `qing_currency_stress` (A),
  `qing_reform_pressure` (#9b), plus the governance and diplomacy counters below.
* The pulse hooks live in `common/on_action/00_monthly_country.txt` (throttled, gated
  to the single human Qing).

**History:** the "High Qing → nineteenth-century crisis" arc — the fiscal-military
decline of the Eight Banners, the silver drain of the opium trade, endemic corruption
(the Heshen 和珅 archetype), millenarian sects (White Lotus 白蓮教), and Manchu–Han
tension — compressed into steerable meters.

---

## 1. Subject interactions & gradual integration
**Code:** `common/scripted_effects/se_SUBJECT_QING.txt`,
`common/scripted_guis/SUB_QING_subject_interactions.txt`,
`common/modifiers/qing_integration_modifiers.txt`,
`events/imp19c_mod_events/qing_subject_integration.txt`,
loc `qing_subject_integration_l_english.yml`.

Two player systems on a single named subject:

1. **Change subject type** — promotion (tighter control) / demotion (looser) steps one
   rung along the Qing control ladder. Primitive: vanilla `make_subject`, wrapped by
   `FUNC_make_subject` (`se_FUNC.txt`).
2. **Gradual integration** — spend political influence to accrue integration progress
   on one subject; at threshold, absorb its provinces via `LAND_transfer_provinces`
   (`se_LAND.txt`, which correctly splits governorship wealth/stockpiles). Integration
   can be **suspended** by a subject-reaction event (`SUBJ_integration_suspended` flag);
   while suspended the monthly pulse skips the subject and the **Resume** button shows
   *instead of* the Integrate button (the Integrate button's `is_shown` excludes the
   suspended flag, matching the pulse).

3. **Incorporate a protectorate** — a protectorate (Tibet, under the 1815 amban
   settlement) sits **off** the control ladder (`can_be_integrated = no`) and can be
   neither promoted nor integrated as it stands. `qing_subject_incorporate_button` →
   `SUBJ_QING_incorporate_protectorate` is a one-way, coercive act that converts it
   straight to an `autonomous_governorship` (rung 4), after which the ordinary integrate
   verb applies. Priced in prestige + political influence and carries a tyranny + AE
   bite; it is **not** date-restricted (available from the 1815 start). A dedicated
   `qing_subject_type_is_protectorate` indicator keeps the diplomatic-view "Type:" label
   from mislabelling a protectorate as an autonomous governorship.

Buttons (`qing_subject_promote/demote/integrate/resume_integration/incorporate_button`)
are surfaced in the diplomatic view. Costs and cooldowns live in `is_valid`; all paths
log via `sys = SUBJ`.

**History:** the Qing subject order — the graded dependence of tributaries, the
autonomous governorships, and the *gaitu guiliu* (改土歸流) conversion of native
chieftaincies into directly-administered territory; the incorporate act follows
Zhao Erfeng's (趙爾豐) forced incorporation of Kham (川邊改土歸流, 1904–11).

---

## 2. The governance engine & Grand Council
**Code:** `common/scripted_effects/se_QING_GOVERNANCE.txt`,
`common/scripted_effects/se_QING_COUNCIL.txt`,
`common/scripted_effects/se_QING_AFFINITY.txt`,
`common/script_values/QING_governance_svalues.txt`,
`common/scripted_guis/QING_governance_actions.txt`,
`common/modifiers/qing_governance_modifiers.txt`,
events `qing_office_events.txt`, `qing_keju_events.txt`, loc `qing_governance_l_english.yml`.

The abstracted bureaucracy the player steers from the top:

* Two meters — `qing_bureau_capacity` (administrative throughput) and
  `qing_bureau_integrity` (merit 科舉 vs patronage 捐納 staffing) — plus the Grand
  Council's own `qing_council_effectiveness`.
* **The Grand Council (軍機處)** is the hub: seat grand councillors (軍機大臣) into a
  capped set of seats, name a chief (領班軍機大臣); the Manchu/Han balance and the
  councillors' skills drive effectiveness, which *feeds* bureau capacity, which feeds
  the whole decline/reform machine. `QING_GOV_pulse` calls `QING_council_recompute` +
  `QING_council_apply_band`.
* **Great offices** held by named characters: the Six Boards (六部尚書), Censorate
  (都察院), Court of Colonial Affairs (理藩院), Zongli Yamen (總理衙門), Amban (駐藏大臣).
* **Character affinity** (`se_QING_AFFINITY.txt`) scores a courtier's compatibility with
  the reigning emperor from the *full* Imperator character model — charisma, zeal gap,
  culture (the 滿漢 fault line), religion, friend/rival relations, kinship, age/health —
  so councillors and office-holders are not interchangeable counters.

**History:** the Yongzheng-era Grand Council atop the Six Boards; the examination
system (科舉) versus the sale of offices (捐納); the Censorate; the overmighty-kinsman
danger; the Zongli Yamen as the first modern foreign office (1861).

---

## 3. Dynastic-decline events (the mechanics hub)
**Code:** `common/scripted_effects/se_QING_MECHANICS.txt`,
`common/scripted_guis/QING_mechanics_actions.txt`,
`common/modifiers/qing_mechanics_modifiers.txt`,
events `qing_decline_events.txt`, `qing_office_events.txt`, `qing_keju_events.txt`,
`common/on_action/qing_mechanics_on_actions.txt`, loc `qing_mechanics_l_english.yml`.

Player verbs and reactive events driving the decline counters. Examples:

* **Sale of offices (捐納)** — `QING_sell_offices`: immediate wealth via the
  currency-aware `CURRENCY_grant_country_wealth = { thousands = 80 }` (scaled by the
  reserve ratio, so it routes through the economy layer rather than dumping raw
  treasury), at the cost of +corruption and a decaying purchased-ranks modifier.
* **Ever-normal granaries (常平倉)** — `QING_granary_invest` / `QING_granary_release`
  (raw-treasury *cost* + stock counter; releases buffer famine).
* **Statecraft investment (振興庶政)** — `QING_statecraft_invest`: spend treasury +
  political influence to raise `EDU_school` in the three most-populous city provinces
  and `URB_administration_district` in the two largest at a stroke, thickening state
  capacity from the 1815 start. What can be built is gated on the enabling reforms
  (`tech_education` / `tech_central_administration`), guarded manually because
  `add_building_level` does not enforce a building's `allow`; the cost is **charged only
  on delivery** (deducted inside the "≥1 building raised" branch, never for a no-op), and
  each successful build-out nudges `qing_bureau_capacity`. The action's `is_valid` also
  gates on holding at least one enabling reform so the button never reads as a dead click.
* Ethnic-tension stance (banner-favouring 旗 / Han-favouring / dyarchy 滿漢), corruption
  audits, sect suppression, banner-reform drills, currency/silver stress.

**History:** the whole nineteenth-century crisis cluster — the opium silver drain,
Heshen-scale corruption, secret societies, banner decay, the fiscal expedient of
selling degrees (Elisabeth Kaske, *The Price of an Office*, 2011).

---

## 4. The Self-Strengthening Movement (自強運動 / 洋務運動)
**Code:** `common/scripted_effects/se_QING_SELFSTR.txt`,
`common/missions/qing_selfstrengthening_missions.txt`,
`common/modifiers/qing_selfstrengthening_modifiers.txt`,
loc `qing_selfstrengthening_l_english.yml`.

The **positive, preemptive** track — the inverse of the decline cascade. A single
`qing_selfstr_progress` 0..100 counter, advanced by completing the mission tree, read
by the governance pulse which swaps the progress band
(`qing_selfstr_nascent` ≥25 → `_advancing` ≥50 → `_golden_age` ≥85). Each named-
institution task calls `QING_selfstr_found_*`, which grants the institution's country
modifier, advances progress, **builds the real institution** via `add_building_level`,
and — where historical — grants treasury via the currency interface.

Institutions modelled (each a modifier now with a localised display name):
Jiangnan Arsenal (江南製造總局), Fuzhou Navy Yard (福州船政局), Beiyang Fleet (北洋水師),
Nanyang Fleet (南洋水師), Fujian Fleet (福建水師), Guangdong Fleet (廣東水師),
Ever-Victorious Army (常勝軍), Tongwen College (同文館), China Merchants' Steam
(輪船招商局), Rail and Iron (鐵路與鋼鐵).

**ti-yong framing** (中學為體，西學為用): the bonuses are industrial/military/fiscal, never
political — political modernization is the *separate* reform track (§6).

**The four fleets are REAL squadrons, not only abilities.** The naval "design lock"
(fleets-as-abstract) was **lifted** once the engine's navy-spawn idiom was confirmed:
`create_unit = { navy = yes location=<port> while={ count=N add_subunit=screw_frigate/
medium_steamer } }`, called directly in country scope (there is no `raise_navy` wrapper).
The four fleet tasks (北洋/南洋/福建/廣東) each call `QING_selfstr_found_beiyang/_nanyang/
_fujian/_guangdong`, which grant the fleet's lasting "cheaper ships / fleet quality"
country modifier **and** raise an actual squadron via the shared `QING_selfstr_raise_fleet`
effect. Home ports: Tianjin (`p:3783`, Beiyang) / Shanghai (`p:5429`, Nanyang) / Fuzhou
(`p:3651`, Fujian) / Guangzhou (`p:9298`, Guangdong); if the home port is not held+coastal,
the squadron musters at the most-populous owned coastal province instead, with `LOG_fail`
if the empire holds no coast. Squadrons are **historically sized**, not token forces —
Beiyang the strongest fleet in Asia at its peak (14 major + 10 lighter hulls), Nanyang the
second squadron (8 + 10), Fujian the Fuzhou-yard force annihilated at 馬江海戰 1884 (6 + 5),
Guangdong a dozen southern gunboats (3 + 9); `screw_frigate` = a major warship,
`medium_steamer` = a smaller steam vessel. They carry naval maintenance, matching the real
fiscal burden the fleets imposed. Because each fleet is *created by* its task (not seeded at
game start), no pre-existing navy is required — historically apt, since all four are
1860s–80s creations that did not exist in 1815.

**The Ever-Victorious Army (常勝軍) is likewise a REAL unit.** `QING_selfstr_found_evarmy`
grants the `qing_selfstr_ever_victorious` army-ability modifier *and* raises an actual
Ever-Victorious legion at its historical base, Songjiang/Shanghai (`p:5429`), or the capital
if Shanghai is not held (guarded, `LOG_fail` if landless). When the founding comes from a
commander's arrival event — Ward (`qing_roster.14`) or Chinese Gordon (`qing_roster.9`) —
that character is saved as `scope:evarmy_commander` and attached to the legion
(`add_to_legion = PREV` + `random_legion_unit = { set_as_commander }`); the mission-tree
founding raises it commander-less for the player to assign. Land forces (banners, Green
Standard, Ever-Victorious) are on-map legions and the four fleets are on-map navies — the
Self-Strengthening military reward is now fully concrete (see §"Historical starting armies"
for the corrected `create_unit`/`raise_legion` idiom).

**History:** the 1861–1895 movement under Prince Gong 恭親王, Li Hongzhang 李鴻章, Zeng
Guofan 曾國藩, Zuo Zongtang 左宗棠, Zhang Zhidong 張之洞. Sources: Pong, *Modernization
and Politics in China* (1994); Kwang-Ching Liu & Richard Smith in *Cambridge History of
China* v.11; Benjamin Elman on the refraction of the reforms (2004).

### 4.1 The refraction reckoning & the guandu-shangban / telegraph split (deepening)
The movement now carries an **Elman refraction** dimension: `QING_selfstr_advance` grants
*less* real progress when the bureaucracy that must absorb it is weak — the founding
effects halve their gain if `qing_bureau_capacity < 50` or `qing_council_effectiveness <
50`, so self-strengthening bought without the administrative backbone to hold it comes out
"hollow". When progress has run far ahead of that backbone, a `qing_selfstr_hollow_flag`
trips and the refraction-reckoning event (`qing_reform.35`, offered by the flavour roll)
forces the throne to confront the gap. The **merchant-conglomerate** strand
(`QING_selfstr_found_merchant`, 官督商辦 official-supervised/merchant-managed — the China
Merchants' Steam Navigation model) and the **Imperial Telegraph** (`QING_selfstr_found_
telegraph`, 電報總局, Sheng Xuanhuai 盛宣懷, 1881) are now **distinct** foundings rather than
one lumped institution, reflecting that the telegraph administration was a separate 1880s
undertaking. All foundings are guarded no-ops if the institution already stands.

**History:** Benjamin Elman, *On Their Own Terms* (2004) on the refraction of Western
science through the late-imperial framework; Wellington Chan on Sheng Xuanhuai's
conglomerates and the crony-capital shadow of the guandu-shangban model.

---

## 5. The Japan / Meiji tree (東亞近代化)
**Code:** `common/missions/qing_japan_missions.txt`,
`common/modifiers/qing_japan_modifiers.txt`, diplomacy poles in `se_QING_DIPLO.txt`,
loc `qing_japan_l_english.yml`; opinions `qing_japan_accord_opinion` /
`qing_japan_rivalry_opinion`.

Japan is the Qing's **peer**, not a predatory Western power, so it runs on its own
accord/rivalry poles surfaced in the two courts' mutual opinion. A shared overture
forks into: **Arc A — 同文同種 the Accord** (pan-Asian entente, Ryukyu settled by
negotiation, capstone the East Asian Alliance) or **Arc B — 海防 the Rivalry**
(ready the coast and fleets, forestall/win the 1894–95 war, capstone the Collision Won).

**History:** the parallel modernizations racing each other; the Ryukyu/Korea/Taiwan
collision course to the First Sino-Japanese War.

---

## 6. Constitutional reform & the four end-states
**Code:** `common/scripted_effects/se_QING_REFORM.txt`,
`common/missions/qing_reform_missions.txt`, `events/…/qing_reform_events.txt`,
end-state + rebellion modifiers in `qing_mechanics_modifiers.txt`,
loc `qing_reform_missions_l_english.yml` + `qing_mechanics_l_english.yml`.

Two routes converge on the same end-state machinery:

* **Reactive crisis** (`qing_reform_events.txt`) — `qing_reform_pressure` crosses a
  threshold and the throne is *forced* to choose; faction events move
  `qing_reform_faction_balance` (−100 reactionary .. +100 constitutional).
* **Proactive tree** (`qing_reform_missions.txt`) — a translation bureau → provincial
  assemblies (諮議局) → the constitutional mission abroad (五大臣出洋, 1905) → the draft
  constitution (欽定憲法大綱, 1908) → summon the national parliament. The mission's
  `on_start` now **guarantees `qing_reform_faction_balance` is initialised** (it is
  otherwise only seeded by the crisis event), so a player who walks the tree without
  ever tripping the crisis still has a defined variable for the tasks to nudge and the
  capstone to read.

Both settle into **one of four durable alternate-history end-states**, each a government
(and for the heterodox path a religion) change plus a permanent golden modifier, once-only
(guarded by `qing_reform_endstate_reached`):

| End-state | Government | Modifier |
|---|---|---|
| 同治中興 revitalised absolute monarchy | `imperial_monarchy` | `qing_endstate_restoration` |
| 君主立憲 constitutional monarchy | `constitutional_parliament` | `qing_endstate_constitutional` |
| 中華共和 the republic | `constitutional_republic` | `qing_endstate_republic` |
| 天國 Christian theocracy | `militant_theocracy` + religion change | `qing_endstate_heavenly_kingdom` |

**History:** Wei Yuan 魏源 *Haiguo Tuzhi* (1843); Kang Youwei 康有為 / Liang Qichao 梁啟超
(戊戌變法, 1898); the 1906 預備立憲 and 1908 憲法大綱.

---

## 7. The Taiping / Heavenly-Kingdom tree (天國)
**Code:** `common/missions/qing_taiping_missions.txt`,
Taiping helpers in `se_QING_REFORM.txt`, loc `qing_taiping_missions_l_english.yml`.

The hardest, most heterodox road — the alternate history in which the throne *joins*
the Taiping faith. Gated behind the Taiping **overture** (`qing_taiping_overture`, seeded
by the Hong Xiuquan roster event and echoed by a rebellion event); each task calls
`QING_taiping_advance`, pushing `qing_taiping_progress` toward the 70 the theocracy end-
state requires, leaning on Western backing. This is the fourth and rarest golden-age fate.

**History:** the Taiping Heavenly Kingdom (太平天國, 1851–64), Hong Xiuquan 洪秀全, and a
counterfactual syncretic Chinese Christianity.

---

## 8. Rebellions
**Code:** `events/imp19c_mod_events/qing_rebellion_events.txt`, rebellion helpers in
`se_QING_REFORM.txt`, flavour modifiers in `qing_mechanics_modifiers.txt`,
loc `qing_rebellion_l_english.yml`.

Great risings fire while pressure is high. Ten once-guard **variables**
(`qing_rebel_white_lotus`, `qing_rebel_nian`, …) track which historical revolts have
occurred; five thematic **flavour modifiers** bite while a rising is live:
`qing_rebel_sectarian` (白蓮教/天理教), `qing_rebel_taiping` (太平天國),
`qing_rebel_ethnic` (回變/陝甘/苗變), `qing_rebel_restorationist` (紅巾/天地會/捻軍),
`qing_rebel_boxer` (義和團 — a two-edged pro-dynastic sword). Each now has a localised
display name.

---

## 9. Frontier migration & demographic flavour
**Code:** `events/imp19c_mod_events/qing_frontier_migration_events.txt`,
`common/scripted_effects/se_QING_COLON.txt` (the nomad-ingathering effects),
`common/modifiers/qing_migration_modifiers.txt`, loc `qing_migration_l_english.yml`,
tributary opinions in `common/opinions/imp19c_opinions.txt`.

* **Nomad in-migration** — the Torghut Return (土爾扈特東歸, 1771) and lesser echoes:
  manpower + light cavalry + martial vigour. Reworked to honour the bottom-up
  migration philosophy: `QING_MIGR_nomad_ingather = { count }` **moves real** Oirat-
  Kalmyk-Mongol tribesmen pops (`culture:kalmyks/oirat/mongolian/buryat`) OUT of the
  foreign-held (Russian) lower-Volga/Kazakh steppe INTO the Qing's most populous arid
  frontier province (`semi_arid`/`desert`/`plains`), one pop per iteration via
  `move_pop`; it falls back to `create_state_pop` only when the historical source has
  run dry, so the promised host always arrives. The settling ground is then tagged with
  a durable frontier pull (`QING_COLON_frontier_pull_here` → `migr_gov_pull`), so the
  newcomers and the empire's own surplus keep flowing there through the generic decade
  migration pulse — closing the loop into `se_MIGRATION.txt`.
* **Cross-border migration friction → diplomatic play** (generic, `se_MIGRATION.txt`) —
  the bottom-up decade pulse already lets a grievance-weighted pop trickle across a
  border (the destination selector only requires `exists = owner`, not `owner = ROOT`).
  When it lands on foreign soil, arrival strains the two peoples and their governments
  **even though neither state ordered the move**: the destination province accrues a
  running `migr_influx` tally (+2 per arrival, decaying −1 each decade so only a
  *sustained* flow climbs), which drives an escalating ladder — **TIER 1** a modest
  `migration_strain` province modifier + a mild two-way opinion knock (`migrant_influx_opinion`
  on the receiver, `migrant_emigration_opinion` on the sender); **TIER 2** (influx ≥3)
  the heavier `migration_strain_high` + a larger opinion hit; **TIER 3** (influx ≥5, once
  per ~decade via `migr_friction_play_cd`) the **breaking point**: a diplomatic play whose
  instigator is *situational* — if the settlers have flipped the province's plurality, the
  now-dominant culture's **kin-state** presses an irredentist `get_territory` play (mirroring
  the settler-claim track); if not, the **receiving** state presses a nativist `influence`
  play against the source. Deliberately lighter than the feature-rich Qing GP layer:
  cheap variable writes + a guarded decay loop (`has_variable = migr_influx`), with the one
  expensive step — launching the play — gated behind the tier and cooldown. All logged
  `sys = MIGR`. The play now **resolves** (see the diplomatic-play resolution note): if it
  develops enough success before reaching max progression, the irredentist `get_territory`
  play cedes the contested land to the kin-state, and the nativist `influence` play plants
  the receiving state's sway over the source country — while the modifiers, opinions and the
  kin-state claim land regardless, so a play that never develops still leaves a real mark.
* **New World crop revolution** (番薯/玉米/落花生) — the double-edged population boom,
  resolving to a golden (`qing_migr_crop_boom_golden`) or Malthusian
  (`qing_migr_overpopulation`) state by dynastic strength.
* **Hong Kong** (香港) — a Chinese-run entrepot growing from free port → harbour district
  (province modifier) → "Pearl of the Orient".
* **Tributary suzerainty** affirmed by investiture/naming (越南, 1804), with the
  `qing_investiture_opinion` / `qing_overbearing_opinion` opinions.

**History:** Ho Ping-ti, *Studies on the Population of China 1368–1953* (1959); Perdue,
*China Marches West* (2005); Carroll, *A Concise History of Hong Kong* (2007); Woodside,
*Vietnam and the Chinese Model* (1988).

---

## 10. The Golden Urn (金瓶掣籤)
**Code:** `events/imp19c_mod_events/qing_golden_urn.txt`, `QING_urn_check` +
on-action hook in `00_monthly_country.txt`.

When a Tibetan-Buddhist (vajrayana / bodish-culture) subject's ruler dies, the throne may
**enforce** the golden-urn lottery for the reincarnation (asserting sovereignty) or
**waive** it (buying Tibetan goodwill).

**History:** Qianlong's 1793 reform (欽定藏內善後章程二十九條) requiring high-lama
reincarnations to be drawn by lot under the amban's supervision; enforced to assert
control, waived (1860, 1879) for goodwill. Source: Max Oidtmann, *Forging the Golden Urn*
(2018).

---

## 11. Cultural patronage (文治)
**Code:** `events/imp19c_mod_events/qing_culture_events.txt`,
`common/modifiers/qing_culture_modifiers.txt`, loc `qing_culture_l_english.yml`.

Acts of imperial patronage offered anachronistically to the 1815 player — dictionaries,
poetry corpora, the colossal encyclopaedias, the vernacular novel, the palace workshops
(jade/porcelain/silk/painting) — each a lasting prestige-of-letters modifier. The shadow
side is the literary inquisition (文字獄) shadowing the *Siku Quanshu* (四庫全書): order
bought with fear.

### 11.1 The Ten Great Campaigns (十全武功) — the Manchu military tradition
**Code:** `common/military_traditions/00_manchu.txt`, loc `military_traditions_l_english.yml`
(the `manchu_shiquan` / `shiquan_*` keys).

The martial counterpart (武功) to §11's letters (文治). Rather than a bespoke counter/GUI suite,
this reuses the **engine's own military-tradition tree** — the vanilla screen the arabic/indian/
japanese trees already populate — so the Qing gets a real, browsable heritage tree for free. It is
gated on the **jurchen** culture group (CHI's primary culture is `manchu`, a jurchen culture) via
the same `began_with_tradition_group` idiom the other trees use. Qianlong styled himself
十全老人, "the Old Man of the Ten Complete Victories"; the tree commemorates those ten campaigns
**and grants their martial lessons as real bonuses** (buffs, not inert flavour). Three theatres
descend from the `shiquan_start` opener, each a historically-ordered `requires` chain:

* **平定西域 Pacification of the Western Regions** — First Dzungar (1755, cavalry offence + supply),
  Second Dzungar (1757, cavalry discipline + hostile-attrition endurance), the Muslim-tribes /
  Altishahr campaign (1759, desert combat + manpower + a folded-in land-morale theatre reward).
* **大小金川 The Jinchuan Wars and the Island** — First Jinchuan (1747-49, siege), Second Jinchuan
  (1771-76, assault + engineers), Taiwan / Lin Shuangwen (1787-88, unrest-suppression + blockade +
  a folded-in siege reward).
* **外藩征討 The Tributary Frontiers** — Burma (1765-69, attrition resistance), Vietnam (1788-89,
  reinforcement speed), the two Gurkha marches (1788-92, supply + morale + a folded-in
  war-exhaustion reward).

Because this is a **flat** tradition tree (the arabic/indian/japanese shape, with no path-container
level), each theatre's completion reward is folded into its final node's own `modifier` rather than a
separate `bonus = {}` block — a `bonus` block only fires inside the nested three-level layout that
`01_default.txt` uses, and would be silently dropped here (caught in review).

The capstone **shiquan_laoren (十全武功 complete)** requires the last campaign of all three theatres
(`requires = { shiquan_altishahr shiquan_taiwan shiquan_gurkha }`) and grants the summit reward —
land morale, manpower, ruler popularity. Every modifier key is one already proven valid in the
mod's populated trees; every node carries a **placeholder icon that resolves to an existing
`.dds`** in `gfx/interface/icons/military_traditions/` (no node renders blank), to be swapped for
bespoke art later.

**History:** Qianlong's 御製十全記 (Record of the Ten Complete Victories); Perdue, *China Marches
West*. The campaign roster tallies as ten by counting each Dzungar, Jinchuan and Gurkha war twice.

### 11.2 The dual standing army at game start (八旗 + 綠營) — #66
**Code:** `common/scripted_effects/imp19c_effects_legion_setup.txt` (`SE_qing_armies` +
the `SE_qing_raise_garrison` / `SE_qing_raise_garrison_cmd` helpers), fired once at
game setup from `oa_economy_setup.txt`.

The Qing did not field one army; it fielded **two permanent, separately-administered,
ethnically-defined institutions that met only at the throne**, and the 1815 starting
order-of-battle now reflects that (replacing the earlier single Beijing legion):

* **八旗 Eight Banners** — the hereditary conquest-elite caste + strategic reserve.
  * *禁旅八旗 jinlü baqi (metropolitan banners)* — one large **Metropolitan Eight Banners**
    legion at Beijing (p:8363, +23 coy), by far the biggest single force, under **Yinghe**
    (char:340, general of the Manchu Plain Blue Banner since 1814).
  * *駐防八旗 zhufang baqi (provincial garrisons)* — smaller banner legions in the walled
    Manchu cities 滿城: **Xi'an** (largest interior), **Ili/Huiyuan** (seat of the 伊犁將軍,
    under **Changling** char:244), **Shengjing** (Mukden), Jingzhou, Hangzhou, Jiangning,
    Chengdu, Canton, Fuzhou, Ningxia, Liangzhou, Kaifeng, Taiyuan, Suiyuan, Heilongjiang
    (Qiqihar), Ürümqi and Kashgar.
* **綠營 Green Standard** — the Han professional territorial/constabulary army, deliberately
  fragmented; modelled as several mediocre provincial stacks under the great regional
  commands: **Zhili/京師** (under **Nayancheng** char:358, Viceroy of Zhili — preserved from
  the original single-army setup), Liangjiang, Huguang, **Sichuan** (under **Wu Xiongguang**
  char:339), Liangguang, Shaan-Gan, Fujian, **Taiwan**, and **Yunnan-Guizhou** (under
  **Yang Fang** char:241, a Han White-Lotus veteran — the emblem that the Green Standard and
  militia, not the banners, won the era's wars).

**"Big on paper, brittle in field."** Garrisons are raised at full paper size; the
militarily-soft reality of 1815 (旗人生計 banner-poverty crisis, lost 國語騎射) is expressed
through the **existing `qing_banner_decay` bands** (`qing_banner_decay_mild` / `_severe`
country modifiers in §0.2 / `se_QING_DECLINE.txt`), which carry the combat penalty rather
than shrinking the rolls. Design intent: the Qing player should feel driven to **raise
militia 鄉勇** (the real late-Qing fighting edge) rather than lean on the standing army.

**Implementation.** Every legion is raised from `c:CHI.capital_scope.governorship` (proven
to exist) but *located* at its garrison province — the same pattern `SE_occupation_of_france`
uses. Two parameterized helpers do the work: `SE_qing_raise_garrison { prov name size }` and
`SE_qing_raise_garrison_cmd { prov name size cmd }`, each individually guarding
`exists = $prov$ && owner = c:CHI` (and `exists = $cmd$`), so a **partitioned or shrunken Qing
simply gets fewer garrisons** (each miss emits `LOG_fail`, sys=QING) instead of a scope error.
Unit count uses the verified `while = { count = $size$ add_subunit = regular_infantry }` idiom
(total = size + 1 base company). All commanders are confirmed alive in 1815. Fully wired to
se_LOG (sys=QING) with enter/exit + per-garrison lines. See memory
`imp19c-qing-army-1815-research` for the historiography behind the placements and totals.

### 11.3 The Garden of Gardens (圓明園／頤和園) — the Summer Palace tree — #74
**Code:** `common/missions/qing_summer_palace_missions.txt` (mission `qing_summer_palace_mission`),
`common/scripted_effects/se_QING_SUMMER_PALACE.txt` (`QING_sp_*` verbs),
`events/imp19c_mod_events/qing_summer_palace_events.txt` (namespace `qing_summer_palace`),
`common/modifiers/qing_summer_palace_modifiers.txt`, loc `qing_summer_palace_l_english.yml`. The
1860 sack is offered through `QING_frontier_flavour_roll` (se_QING_DECLINE.txt).

The imperial garden-palaces north-west of Beijing (Haidian, in Beijing's capital province p:8363).
A player-driven build tree that then confronts the palace with its **two real historical fates**:

- **Build (圓明園).** Root task `qing_sp_yuanmingyuan` (treasury 120, must hold Beijing) restores
  Qianlong's *Garden of Perfect Brightness* and sets the flag `qing_sp_built`; two branches adorn it
  — `qing_sp_european_pavilions` (西洋樓, Castiglione's Jesuit baroque) and `qing_sp_siku_library`
  (四庫全書, the Complete Library, which also nudges `qing_civic_identity`). Each grants a lasting
  prestige/legitimacy modifier.
- **The sack of 1860 (火燒圓明園, reactive `qing_summer_palace.1`).** The roll offers it only if the
  garden stands *and* the Qing is at war with Britain or France after 1856 — the historical trigger
  of Elgin's burning. `QING_sp_sack_of_1860` strips all three garden modifiers, leaves a permanent
  `qing_sp_burnt_ruins` scar (−prestige/−stability/−happiness), flips the flag to `qing_sp_burnt`,
  **but** feeds `qing_reform_pressure +12` and `qing_civic_identity +8` — the sack as a founding
  wound of modern Chinese nationalism.
- **The navy-funds dilemma of 1888 (頤和園之議, capstone `qing_summer_palace.2`).** The capstone task
  `qing_sp_yiheyuan` (available whether the garden stands or lies in the 1860 ashes) poses Cixi's
  historical choice: **A — divert the Beiyang fleet's budget** (`QING_sp_rebuild_divert_navy`: full
  splendour + big prestige, but a permanent `qing_sp_starved_fleet` malus and `qing_selfstr_progress
  −8` — the road to the Yalu, 1894); or **B — pay honestly from the treasury** (`QING_sp_rebuild_
  from_treasury`, gated on treasury ≥250: same splendour, no starved fleet, and eases reform
  pressure — the reformed Qing that can afford both). The `.2` description branches (`first_valid`)
  on whether the garden is being adorned or raised from ashes.

**Engine note (caught pre-review):** the mod has **no CK-style country flags** — `set_country_flag`/
`has_country_flag` do not exist here. All flag state uses the mod's own `set_variable`/`has_variable`/
`remove_variable` boolean-variable idiom (as `qing_uscw_decided` does), and the `remove_country_modifier`
calls in the sack are safe no-ops when an optional adorning modifier was never added.

**History:** Young-tsu Wong, *A Paradise Lost: The Imperial Garden Yuanming Yuan* (2001); Hevia,
*English Lessons* (2003, the 1860 sack); on the navy-funds diversion, the Beiyang historiography and
Cambridge History of China v.11.

---

## 12. The anachronistic historical-character roster
**Code:** `common/scripted_effects/se_QING_ROSTER.txt`,
`events/imp19c_mod_events/qing_roster_events.txt`, `qing_character_events.txt`,
loc `qing_roster_l_english.yml`.

Real late-Qing / reform / revolutionary figures step onto the stage **keyed to mechanic
context, not birth date** — Li Hongzhang appears when self-strengthening stirs; Sun
Yat-sen when reform pressure is ripe; Hong Xiuquan seeds the Taiping overture.

**Engine reality:** the mod's `create_character` takes no name argument, so identity is
carried two ways — `add_nickname = "<loc key>"` pins the real name as an epithet (findable
in the court list), and every arrival event writes the full name (Chinese + pinyin) into
its title/desc/options. `QING_roster_finalize` is called inside the fresh character's scope.

**The roster (21 figures).** The decline/reform anchors — Heshen 和珅, Lin Zexu 林則徐,
Prince Gong 恭親王, Li Hongzhang 李鴻章, Zeng Guofan 曾國藩, Zuo Zongtang 左宗棠, Zhang
Zhidong 張之洞, Robert Hart 赫德, Charles Gordon 戈登, Kang Youwei 康有為, Sun Yat-sen 孫中山,
Yuan Shikai 袁世凱, Hong Xiuquan 洪秀全 (roster.1–13) — are joined by eight figures who each
arrive keyed to (and cross-wired into) one of the systems below (roster.14–21):

| Figure | Context key | Cross-wire |
|---|---|---|
| 華爾 Frederick Ward | sect pressure, before Gordon | founds the Ever-Victorious Army (§4) |
| 日意格 Prosper Giquel | self-strengthening stir | founds the Fuzhou Navy Yard + naval advisor (§4, New#2) |
| 郭嵩燾 Guo Songtao | Zongli Yamen / reform | opens the London legation, endures the vilification (New#3); or is disgraced |
| 蒲安臣 Anson Burlingame | reform + a Western power | negotiates an equal treaty (prestige, eases Britain) |
| 容閎 Yung Wing | reform / self-strengthening | launches the Educational Mission (New#4) |
| 盛宣懷 Sheng Xuanhuai | advanced self-strengthening | founds the merchant conglomerates or the telegraph (§4.1) |
| 琅威理 William Lang | naval SS + Britain | founds the Beiyang Fleet + naval advisor (§4, New#2) |
| 曾紀澤 Zeng Jize | Zongli Yamen / Ili stage ≥2 | opens the St Petersburg legation, eases Russia (New#3, New#9) |

Each is guarded once-only (`qing_spawned_*`), the dispatcher (`QING_roster_roll`) flag
matching the event's `set_variable` exactly. Foreign figures (Ward, Giquel, Burlingame,
Lang) carry culture/religion of their homeland and a correspondingly lower throne-affinity.

---

## 13. The Great Pacific Enterprise (大洋洲事業) — overseas colonization
**Code:** `common/missions/qing_colonization_missions.txt`,
`common/modifiers/qing_colonization_modifiers.txt`,
`events/imp19c_mod_events/qing_frontier_sea_events.txt`,
loc `qing_colonization_l_english.yml`.

An anachronistic maritime-expansion tree: the Maritime Bureau (海洋事務局) opens the
enterprise; branches develop Taiwan (臺灣建省), secure the Amur (黑龍江), consolidate
Xinjiang (新疆), play the Great Game for the Silk Road cities, and reach across the Pacific
— Russian America/Alaska, the Northwest fur coast, California (金山), and the island road
(Ryukyu, the Marianas, Hawaii). The **Daoguang Doctrine** (道光主義) forges a US entente
(a Pacific-basin Monroe Doctrine) that suppresses the European friction the enterprise
would otherwise generate. The capstone is a globe-spanning Qing (環太平洋大清).

**History:** Perdue, *China Marches West* (2005); Gibson, *Otter Skins, Boston Ships and
China Goods* (1992, the maritime fur trade & Russian America); Millward, *Eurasian
Crossroads* (2007, Xinjiang); Dennett, *Americans in Eastern Asia* (1922) and the Treaty
of Wanghia (望廈條約, 1844) for the American entente.

### 13.1 The Protectorates-General (都護府)
**Code:** `common/scripted_effects/se_QING_PROTECTORATE.txt`, the seven protectorate tasks
in the colonization mission, the `qing_col_protectorate_*` modifiers.

Sufficient territory/influence in a frontier region lets the player **erect a
Protectorate-General** — reviving the Tang institution of indirect ("loose-rein", 羈縻)
frontier rule. `QING_establish_protectorate` spins the region's owned provinces off as a
**new country** (`LAND_release_from_list`) and immediately binds it as a
`sinosphere_tributary` (`FUNC_make_subject`), an autonomous march that pays tribute and
shields the empire's edge without the cost of direct rule. The overlord gains the march's
reward modifier.

| Protectorate | Region | Government | Historical basis |
|---|---|---|---|
| 安北 Anbei (Pacified North) | Mongolia | viceroyalty | Tang steppe protectorate, seat Ordu-Baliq |
| 安東 Andong (Pacified East) | Liaoning / Korea | viceroyalty | Tang, seat Pyongyang → Liaodong |
| 安西 Anxi (Pacified West) | Turkestan | viceroyalty | Tang Tarim protectorate, Four Garrisons (安西四鎮) |
| 安南 Annan (Pacified South) | Vietnam | viceroyalty | Tang Red River protectorate, seat Hanoi |
| 安海 Anhai (Pacified Seas) | Pacific islands | viceroyalty | **invented** — no Tang precedent |
| 安新 Anxin (Pacified New World) | N-American coast | viceroyalty | **invented** — a continent the Tang never knew |
| 安非 Anfei (Pacified Africa) | Africa (10 regions) | viceroyalty | **invented** — the shore Zheng He last crossed (§13.2) |
| 墨西哥 Empire of Mexico | all Mexico (Pacific/E/N Mexico + C. America), seated at Mexico City | imperial_monarchy | the Second Mexican Empire, Maximilian I 1864 (§13.3) |
| 蘭芳 Lanfang | Borneo | oligarchic_republic | the historical kongsi republic (公司), 1777 |

The two ocean protectorates (安海/安新) are explicitly framed in-fiction as inventions of
*this* Qing. Lanfang is not a march of conquest but the overseas-Chinese kongsi republic
of western Borneo (Luo Fangbo 羅芳伯, 1777) — whose tributary overtures the historical
Qing spurned and whom the Dutch crushed in 1884 — here recognised and sheltered; it is
released as an elected oligarchy, not a viceroyalty.

**History:** Beckwith, *Empires of the Silk Road* (2009); Skaff, *Sui-Tang China and its
Turko-Mongol Neighbors* (2012); Twitchett (ed.), *Cambridge History of China* Vol. 3; on
Lanfang, Heidhues, *Golddiggers, Farmers, and Traders* (2003), Yuan Bingling 袁冰凌 (2000),
Wang Tai Peng (1994).

### 13.2 The Treasure Voyages Reborn (鄭和下西洋復興) — the Scramble for Africa
**Code:** the five African tasks in the colonization mission
(`qing_col_zheng_he` → `qing_col_cape`/`qing_col_suez` → `qing_col_congo` → `qing_col_anfei`),
the `qing_col_treasure_fleet`/`_cape_route`/`_suez_passage`/`_congo_interior`/`_protectorate_africa`
modifiers, loc in `qing_colonization_l_english.yml`.

A second, **southern** enterprise mirroring the Pacific arc, branching off the same Maritime
Bureau root. Where the Pacific arc looks east across an ocean the Ming fleets never crossed,
this arc looks **west** across the one they did — reviving the seven treasure voyages of the
eunuch-admiral **Zheng He (鄭和, 1405–1433)**, which reached the Swahili coast (Malindi,
Mombasa, Kilwa) and bore a tribute-giraffe home to the Yongle court. The historical dynasty
then burned its shipyards and turned inward; here a self-strengthened Qing sails again and
arrives in Africa in the very decades the European powers are partitioning it:

- **鄭和下西洋 Revive the Treasure Voyages** — land on the Swahili coast (claims Zanzibar p:1489,
  Kilwa p:1715); treasure-fleet modifier (naval range/morale, export commerce); provokes Britain.
- **好望角 Round the Cape of Good Hope** — contest the sea-lane hinge with the Royal Navy
  (claims the Western Cape p:132, pressed as a diplomatic play vs GBR); sharp British affront.
- **蘇伊士 Force the Suez Passage** — the short road home (claims Suez p:413 as a play vs GBR,
  Cairo p:429); offends **both** Britain and France, the Egyptian condominium powers.
- **剛果 Carve the Congo Interior** — thrust inland (claims the Congo p:2652 in Equatorial Africa,
  Libreville p:3526 on the Gabon/Guinea coast); sets the Qing against both Britain and France, the
  Berlin-Conference partitioners.
- **安非 Erect the Protectorate of the Pacified Africa** — the invented African march (see §13.1
  table), gathering the continent's holdings across ten regions into one tributary viceroyalty.

The arc deliberately contests **Britain and France** (the paramount powers of the Scramble),
not Russia — so by the 以夷制夷 logic each provocation *delights* Russia rather than provoking
her. Unlike the Canada/California tasks, these do **not** check the Daoguang Doctrine: that
entente is a Pacific-basin settlement and does not extend to Africa or the Indian Ocean, so the
European friction of the Scramble stands regardless of the American partnership.

**History:** Dreyer, *Zheng He: China and the Oceans in the Early Ming Dynasty* (2007); Wade,
"The Zheng He Voyages: A Reassessment" (2005); Pakenham, *The Scramble for Africa* (1991).

### 13.3 The Manila Galleon Reborn & the Mexican Adventure (馬尼拉大帆船 / 墨西哥帝業)
**Code:** the four tasks `qing_col_galleon` → `qing_col_veracruz` → `qing_col_maximilian` →
`qing_col_mexican_empire` in the colonization mission, the
`qing_col_silver_road`/`_gulf_gate`/`_mexican_crown`/`_mexican_empire_mod` modifiers, loc in
`qing_colonization_l_english.yml`. Branches off the Maritime Bureau root, cross-wired to the
Napoleon-at-court chain (§17).

The one arc grounded in a *real* China–New World tie. For two and a half centuries the **Manila
galleon (1565–1815)** carried Mexican silver west to Canton and Chinese silk east to Acapulco —
the single sustained artery between the Middle Kingdom and the Americas, and the pump that drew
the world's silver into China. Spain cut the line in **1815, the very year the game opens**. A
self-strengthened Qing may take up the route the galleons abandoned and follow the silver road to
its terminus — arriving in Mexico in the decades of France's own **Second Mexican Empire (1862–67)**,
when Napoleon III, screened by the American Civil War, shipped the Habsburg archduke **Maximilian**
across the ocean to reign as Emperor of Mexico:

- **馬尼拉大帆船 Reopen the Silver Road** — revive the Acapulco galleon trade (claims Acapulco p:1800,
  the galleon's American terminus; draws settlers); Silver-Road modifier (export/import commerce,
  naval range); provokes Britain — *unless* the Daoguang Doctrine has made the Pacific a shared lake.
- **韋拉克魯斯 Land at Veracruz** — cross to the Gulf coast (claims Veracruz p:2069, the real 1862
  French landing point, pressed as a diplomatic play vs France); affronts France.
- **墨西哥帝業 The Mexican Adventure** — the fork over the throne of Mexico (claims Mexico City p:8516).
  **If the Emperor Emeritus (Napoleon) is at court** (`qing_napoleon_present`): a **Franco-Qing
  condominium** props up his nephew's Habsburg empire — warm relations with France and Napoleon's
  gratitude (a loyalty pulse, since it serves his imperial revenge), but it **provokes Britain**.
  **Otherwise**: the Qing seizes the adventure alone and **provokes France**, whose New-World project
  it pre-empts. Either road, planting a monarchy in the Americas **betrays the Daoguang entente** and
  affronts the United States.
- **墨西哥帝國 The Empire of Mexico** — release **all of Mexico** (Pacific Mexico *incl. the capital
  Mexico City p:8516*, Eastern Mexico, Northern Mexico, Central America) as a client
  **imperial_monarchy** tributary seated at Mexico City — the Son of Heaven's most distant
  vassal-throne. Pacific Mexico belongs *here*, not with Anxin: Anxin (§13.1) is the fur coast and
  California, north of the mountains, so the two New-World protectorates stay disjoint (Anxin =
  Alaska/BC/Cascadia/California; the Empire = the four Mexican regions).

Unlike Canada/California but like the Scramble, only the opening galleon step honours the Daoguang
Doctrine; from Veracruz onward the arc is a European contest (France's adventure) that the American
entente cannot smooth over — indeed the Mexican throne actively *breaks* it.

**History:** Schurz, *The Manila Galleon* (1939); Flynn & Giráldez, "Born with a Silver Spoon: The
Origin of World Trade in 1571" (1995); Cunningham, *The Mexican Empire of Maximilian* / Hanna,
*Napoleon III and Mexico* (1971).

### 13.4 The Qing and the American Civil War (南北戰爭) — #73
**Code:** the verbs `QING_uscw_back_union` / `_back_confederacy` / `_neutral_profit` /
`_release_confederacy` in `common/scripted_effects/se_QING_USCW.txt`, events `qing_uscw.1` (the
three-way fork) and `qing_uscw.2` (the coda) in `events/imp19c_mod_events/qing_uscw_events.txt`, the
`qing_uscw_union_amity`/`_cotton_windfall`/`_neutral_trade` modifiers, loc in
`qing_uscw_l_english.yml`. Offered once in the 1861–65 window, CHI-only and player-only, through
`QING_frontier_flavour_roll` (se_QING_DECLINE.txt). All paths logged `sys = QING`.

The American Civil War is the **exact contemporary of the Taiping Rebellion** (1850–64): two of the
century's largest civil wars raging on opposite Pacific shores at once. A Qing that has crossed the
ocean — the Anxin march on the California coast, the revived Manila silver road, perhaps the
**Daoguang entente** sealed in §13.3 — is a Pacific power with a stake in the outcome. News of the
split reaches Beijing and the court must choose:

- **聯邦之誼 Stand with the Union** — *available only if the Daoguang Doctrine is in force.* The
  Burlingame-era friendship: ship the labour that will build the Union Pacific, extend recognition
  and credit, deepen the entente (mutual accommodation opinion with the USA, wealth, a
  self-strengthening advance if the reform is under way). **Provokes Britain**, which leaned
  Confederate — Lancashire's cotton lords and the commerce-raiders built on the Mersey — and so by
  以夷制夷 delights her rivals.
- **邦聯之利 Recognise the Confederacy** — run its cotton through the Union blockade for silver in the
  world cotton famine (a large wealth windfall). If the Union holds enough of its Deep-South
  (SC/GA/AL/MS/AR/LA/FL) and Appalachian (WV/KY/TN) ground in this timeline, a **Confederacy is
  released** off that land as an independent republic (dynamically, via `LAND_release_from_list` —
  CSA is a phantom tag). Affronts Washington (rivalry opinion from the USA).
- **中立厚利 Stay neutral and profit** — sell to both belligerents and bank the largest windfall of
  the three; no provocations, but no lasting tie either way.

Years on, `qing_uscw.2` closes the chain with a coda whose text branches on the modifier the choice
left behind. The fork deliberately keys on the same **Daoguang entente** as the Mexican adventure
(§13.3): plant a monarchy in Mexico and you break the entente, closing the Union option here — the
two American arcs are wired to pull against each other.

**History:** Spence, *The Search for Modern China*; Foreman, *A World on Fire* (2010, British
Confederate sympathy); Chang, *Ghosts of Gold Mountain* (2019, Chinese railroad labour);
Schoonover, *Dollars over Dominion* (French/Qing Pacific interests).

---

## 14. The Himalaya & Maritime Southeast Asia (南疆與海疆)
**Code:** `common/missions/qing_himalaya_seasia_missions.txt`,
`common/modifiers/qing_himalaya_seasia_modifiers.txt`,
loc `qing_himalaya_seasia_l_english.yml`.

Two arcs fan from a shared root (the Court of Colonial Affairs / expanded 理藩院): **the
Himalaya** (Nepal/Gurkha, Sikkim, Bhutan, Ladakh — bringing the Qing up against the
British Raj) and **maritime Southeast Asia**. Pushing the ring of states into the
tributary order.

**History:** the Sino-Nepalese War (1788–92) ending in a Gurkha tribute mission; Tibet as
a Qing protectorate under the ambans (駐藏大臣).

---

## 15. The foreign-reaction / Great-Power layer
**Code:** `common/scripted_effects/se_QING_DIPLO.txt`,
great-power modifiers + opinions in `qing_colonization_modifiers.txt` /
`imp19c_opinions.txt`.

Each theatre of Qing expansion antagonises a **specific** power via a per-power tension
counter (0..100), read the same O(1) way as the decline counters:

* Southeast Asia (incl. Vietnam) → **France**
* Burma + British India → **Britain**
* Central Asia + Siberia + Alaska → **Russia**

High tension raises that power's predatory/hostile events and closes its
advisor/investment offers; deference/deals lower it. When a counter crosses the hostility
threshold the pulse applies that power's rivalry band (`qing_gp_rivalry_britain/france/
russia`). Opinion layer: direct rivalry/accommodation (`qing_gp_rivalry_opinion` /
`qing_gp_accommodation_opinion`), a stacking improved-relations bonus
(`qing_gp_relation_opinion`, a mod-owned replacement for the undefined vanilla
`opinion_improve_relation`), and the 以夷制夷 balance-of-power play-off pair
(`qing_gp_playoff_opinion` / `qing_gp_partisan_opinion`).

**Colonisation aims launch as first-class diplomatic plays** (`QING_gp_frontier_play`, #53).
The sharpest frontier tasks no longer merely stamp a claim and bump a counter: each also
opens a real diplomatic play against the sphere power over the *same* province its `add_claim`
covers, so the aim reads as a live Great-Game **confrontation** rather than a silent fiat.
Wired at five flashpoints — the Amur/Okhotsk coast (11553), the Silk-Road city of Tashkent
(9370) and Russian America / Sitka (9429) vs **Russia**; Mandalay (6562) vs **Britain** (only
on the *push* branch — never when the player takes the negotiated `QING_gp_partition_britain`
deal); and Phnom Penh (2637) vs **France**. The wrapper is guarded (`exists = c:<tag>`,
instigator ≠ target, `exists = p:<province>`) with a `LOG_fail` when the power is absent or the
province is off-map (claim + tension still stand), and uses `play_type = manual` so the
engine respects the intended target instead of re-deriving it from the area's top adversary.
Each host task is `repeatable = no`, so a play launches at most once per aim. Payoff: the
play now **resolves** (task #58, `DIPLOMACY_complete_play`). A `flag:get_territory` frontier
play that develops enough success before reaching max progression cedes the contested
province to the Qing — the very cession the `add_claim` anticipates. A **decisive** win takes
the whole target area; a **partial** win takes **the contested province itself** (the one the
`add_claim` covers, #61 — not the area's richest province, so the award always matches the
claim; it falls back to the most valuable eligible province only if the contested one is not
cedable, e.g. already ours); below the success floor the play lapses with nothing gained. So
that these justified aims are not near-certain to lapse cold, each feature-launched play opens
with a **baseline success seed** (`DIPLOMACY_seed_feature_play_success`, value 18 — see the
resolution note below) rather than starting at 0 like a bare AI interest-play. The claim, the
tension, and the standing quarrel the scan below keeps alive are the confrontation's teeth
throughout; the cession is the payoff if the play matures.

**Diplomatic plays feed the tension too** (`QING_gp_scan_plays`, run on the 90-day Qing
pulse *before* `QING_gp_apply_bands` so fresh tension converts to bands the same tick). It
reads the Qing's **own live diplomatic plays** from `global_all_diplomatic_plays`; for each
play whose `play_target_area` sits in a great power's sphere — classified at runtime by the
`QING_gp_sphere_is_france/britain/russia` scripted triggers (`imp19c_diplomacy_triggers.txt`,
the same theatres the missions provoke by hand, generalised over the map's regions) — the
owning power's tension mounts a notch (`+3`) and its two rivals' eases (`-1` each, the
balance-of-power tilt). So an ordinary colonial play into the Turkestan khanates becomes a
**standing quarrel with St. Petersburg** the longer it runs. Deliberately **counter-only**:
the scan re-fires every pulse while a play lives, so it moves only the clamped 0..100 tension
counters (never `add_opinion`/`add_aggressive_expansion`, which would stack unbounded) — the
opinion/rivalry-band/relation consequences are applied downstream by `QING_gp_apply_bands`
exactly as on the mission path. No per-play flag is stored, so a recycled play-provobj can
never carry stale Qing state.

**Diplomatic-play resolution note** (`DIPLOMACY_complete_play`, `se_DIPLOMACY.txt`, task #58).
The mod's first-class diplomatic-play system can now RESOLVE a play into a real outcome — for
years it created and progressed plays but completed them into nothing (`play_goal` was never
read). When a play passes `DIPLOMACY_play_max_progression` (240 monthly ticks ≈ 20 years) it is
scored on its accumulated `diplomatic_play_success` (0..100, moved by the play's own events):
**below the floor (25)** it fizzles with nothing gained — the common fate of an interest-play
that never developed; **at/above the decisive line (60)** the goal is achieved in full; between,
a partial outcome. By goal: `flag:get_territory` cedes territory to the instigator via
`LAND_transfer_provinces`/`LAND_transfer_province` — decisive = the whole target area; partial =
**the contested `play_target_area` province itself** (#61), so a feature play's award is exactly
the province its seeding claim named, falling back to the most valuable eligible province only
when the contested one is not cedable — the same transfer idiom `diplomatic_play.2` uses;
`flag:influence` plants the instigator's foreign influence on the **target country's** capital
state (`DIPLOMACY_add_state_foreign_influence`); `flag:subjugate_nation` binds the target as a
`client_state` (decisive) or `tributary` (partial) via `FUNC_make_subject`. Every branch ends
with `AI_remove_diplomatic_play` — mandatory, because the monthly update re-calls completion each
tick while progression stays above max, so without teardown the outcome would re-fire forever.

**Feature plays start with a head-start** (`DIPLOMACY_seed_feature_play_success`, #61). An AI
interest-play begins cold at `diplomatic_play_success = 0` and, if its success-moving events
never fire, deservedly lapses below the floor. But a **mod-feature** play models an aim that is
*already justified* at launch — a standing frontier claim (#53) or years of accumulated
demographic pressure (§9 / #57) — so each feature launcher calls this helper right after
`AI_begin_diplomatic_play` to seed `DIPLOMACY_play_success_seed_feature` (**18**, deliberately
*below* the floor of 25). The play must still develop through its own events to reach even a
partial win — the seed only removes the cold-start penalty, it does not hand a free outcome —
but it is no longer near-certain to fizzle before those events can move the needle. Guarded on
the play provobj existing (a launcher that aborted seeds nothing) with a `LOG_fail` otherwise.
All logged `sys = DIPLO`. This is what makes the frontier plays above and the migration
breaking-point plays (§9) pay off rather than lapse.

**History:** the Great Game; Perdue, *China Marches West*; Hsü, *The Ili Crisis* (1965).

---

## 16. The treaty-century systems (條約世紀) — nine interlocking foreign-pressure loops

Nine event-driven systems model the Qing's entanglement with the treaty powers between the
Opium Wars and the Boxer settlement. Each follows the suite pattern — one or more **0..100
counters on CHI**, nudged by player choices and drifted by a **pulse step read O(1) by the
central `QING_GOV_pulse`** (steps 6–12), with a modifier band matching each counter's value,
all instrumented via `se_LOG` (`sys = QING`). Player verbs are surfaced as scripted-GUI
buttons (`common/scripted_guis/QING_mechanics_actions.txt`) or fired by the flavour roll
(`QING_frontier_flavour_roll` in `se_QING_DECLINE.txt`); every init is seeded in the
`on_game_initialized` CHI block (`qing_mechanics_on_actions.txt`).

### 16.1 The Imperial Maritime Customs Service (海關) — New#1
**Code:** `se_QING_CUSTOMS.txt`, `qing_customs_modifiers.txt`, `qing_customs_events.txt`,
loc `qing_customs_l_english.yml`.

A foreign-run revenue office: `QING_customs_establish` founds the service and
`QING_customs_appoint_ig` seats an Inspector-General (the first foreign-held office, cross-
wired to Robert Hart's roster arrival, §12). A clean, rising customs revenue and a check on
graft, at the price of foreign management and the sovereignty reproach.

### 16.2 Foreign advisors / technical experts (顧問) — New#2
**Code:** `se_QING_ADVISORS.txt`, `qing_advisors_modifiers.txt`, `qing_advisor_events.txt`,
loc `qing_advisors_l_english.yml`.

A capped set of advisor **fields** (naval, army, fiscal, technical), each recruited from a
home power via `QING_advisor_recruit = { field power tag }`, granting a field-active
modifier. The named historical experts (Giquel, William Lang, Ward, Gordon) enter through
the roster (§12) and call this system directly.

### 16.3 Diplomatic missions & permanent legations (遣使／駐外使館) — New#3
**Code:** `se_QING_LEGATIONS.txt`, `qing_legations_modifiers.txt`, `qing_legation_events.txt`,
loc `qing_legations_l_english.yml`.

`QING_legation_open = { power tag }` opens a resident legation in one of five capitals
(London, Paris, St Petersburg, Tokyo, Washington), each a per-power modifier that eases that
power's tension (where a counter exists) and grants diplomatic reach — but levies the
conservative backlash (the **Guo Songtao vilification**). The **Burlingame grand embassy**
(`qing_legation.2`) fires once the Zongli Yamen exists. `qing_legation_count` tracks the
total, gating the treaty-revision verb.

### 16.3a Western embassies to the court (西使覲見／貢使問題) — #60
**Code:** `se_QING_EMBASSY.txt`, `qing_embassy_modifiers.txt`, `qing_embassy_events.txt`,
loc `qing_embassy_l_english.yml`.

The **inbound mirror** of the legation engine: a Western power arrives at the court seeking
audience and trade, and the player chooses between the tribute ceremony and a modern
reception. Six flavour-roll crises, each re-checking its own trigger (power on the map + not
yet resolved): **Macartney 1793** (`qing_embassy.1`) and **Amherst 1816** (`qing_embassy.2`)
for Britain — the kowtow crisis (叩頭之爭); **Titsingh** (Dutch, `.3`); **Golovkin** (Russia,
Kyakhta, `.4`); a **French** embassy (`.5`); and the **Cushing/Wanghia** mission (America, `.6`).

Each embassy offers one choice, resolved once per power via a `qing_embassy_<power>` flag
(1 = rebuffed, 2 = received; `qing_embassy_count` tracks the total). The layer **owns no new
great-power state** — it drives the existing GP-rivalry engine (§9 / se_QING_DIPLO):
- **Rebuff** (stand on ceremony / demand the kowtow / expel) → `QING_gp_react` (rising tension
  + `QING_gp_rivals_delight`, 以夷制夷: the power's two rivals are pleased) + eased reform
  pressure and prestige (the conservatives vindicated). Amherst's expulsion carries a sharper
  severity (9) than Macartney's polite refusal (7).
- **Receive** (audience as near-equals, open trade) → `QING_gp_accommodate` (cooled tension +
  goodwill + `QING_gp_rivals_bristle`) + a lasting `qing_embassy_trade` commerce modifier and,
  where the treaty order already stands, a further treaty port (`QING_treaty_open_port`) — but
  rising reform pressure (the tribute worldview broken).

The two **minor** powers (America, the Netherlands) carry no GP-tension counter — exactly as
the legation layer treats America — so their verbs (`QING_embassy_minor_*`) route the effect
through prestige, reform pressure, trade, and the shared `qing_gp_relation_opinion` directly.
All paths logged (sys = QING), with `LOG_fail` on the once-per-power guard and on a missing tag.

### 16.4 The Educational Mission / students abroad (留學生) — New#4
**Code:** `se_QING_STUDENTS.txt`, `qing_students_modifiers.txt`, `qing_students_events.txt`,
loc `qing_students_l_english.yml`.

`QING_students_launch` sends the first cohort; the pulse graduates a slice each tick
(returnee corps) while a conservative **alarm** meter drifts up. When alarm and reform
pressure are both high the **recall crisis** (`qing_students.10`, the 1881 blow) fires — the
throne defends the mission (40 PI) or yields to the recall. Cross-wired to Yung Wing's roster
arrival (§12).

### 16.5 Unequal treaties & the treaty-port system (條約口岸／租界) — New#5
**Code:** `se_QING_TREATIES.txt`, `qing_treaties_modifiers.txt`, `qing_treaty_events.txt`,
loc `qing_treaties_l_english.yml`.

The **imposition** (`qing_treaty.1`, the Nanjing moment) fires from the flavour roll when
currency stress is high; it opens five ports and sets a `qing_treaty_burden` counter. Further
port demands (`qing_treaty.2`) raise a ports-tier modifier (minor/major/dominant). The
**revision** verb (`qing_treaty.10`, gated on a legation existing) lets the player claw back
**tariff autonomy** (repeatable) or **extraterritoriality** (one-off, gated on autonomy ≥50).
The treaty burden feeds the anti-Christian sentiment target (§16.8).

### 16.6 Technology-transfer bargains (help-for-favours) — New#6
**Code:** `se_QING_TECHTRANSFER.txt`, `qing_techtransfer_events.txt`, loc
`qing_techtransfer_l_english.yml` (reuses the self-strengthening modifiers).

A per-power **favour-debt** ledger (britain/france/russia/america). The player bargains for
a technology track (arsenal→Jiangnan, naval→Fuzhou, rail, telegraph — each firing the
matching `QING_selfstr_found_*`), incurring debt; when a debt crosses the threshold the power
**calls the favour** (`qing_techtransfer.10`), and the throne pays the concession or refuses
(a tension spike). Wires the self-strengthening founding effects to the great-power layer.

### 16.7 Protect the Vassal (保藩) — the tributary crises — New#7
**Code:** `se_QING_VASSAL.txt`, `qing_vassal_modifiers.txt`, `qing_vassal_events.txt`, loc
`qing_vassal_l_english.yml`.

A `qing_suzerain_prestige` meter (starts 70) with a band (ascendant ≥70 / crumbling ≤30).
Four crises fire from the flavour roll, each gated on the vassal not-yet-lost + the encroacher
on the map: **Korea vs Japan** (1894), **Vietnam vs France** (Sino-French War), **Ryukyu vs
Japan** (1879), **Burma vs Britain** (1886). The throne defends (a treasury cost, pressuring
the encroacher via the Japan-rivalry or great-power tension hooks) or abandons the vassal
(marking `qing_vassal_lost_*`).

### 16.8 Missionary incidents & the road to the Boxers (教案) — New#8
**Code:** `se_QING_MISSIONARY.txt`, `qing_missionary_modifiers.txt`, `qing_missionary_events.txt`,
loc `qing_missionary_l_english.yml`.

An `qing_antichristian_sentiment` meter drifting toward a blend of the treaty burden (§16.5)
and sect pressure. At an incident (`qing_missionary.1`, aggrieved power chosen at fire-time,
France→Britain→Russia) the throne **suppresses** it (satisfy the consuls, but the gentry
seethe — sentiment climbs) or **indulges** the fury (relieve sentiment, but affront the power
and feed reform pressure). When sentiment boils over the pulse escalates directly into the
**existing Boxer rising** (`qing_rebellion.9`, §8) rather than duplicating it — guarded on the
same `qing_rebel_boxer_rose` flag.

### 16.9 The Ili Crisis & the reconquest of Xinjiang (新疆／伊犁) — New#9
**Code:** `se_QING_ILI.txt`, `qing_ili_modifiers.txt`, `qing_ili_events.txt`, loc
`qing_ili_l_english.yml`.

A discrete **four-stage set-piece** (stage variable `qing_ili_stage` 0..4, control meter
`qing_xinjiang_control`), offered once the far-western rising has flared (it gates on
`qing_rebel_dungan`, set by the **existing** `qing_rebellion.6` — the Dungan/Yaqub Beg revolt
— which it connects to rather than duplicating):

1. **The debate** (`qing_ili.1`, 海防塞防之爭) — commit the treasury to the **frontier**
   (Zuo Zongtang, launching the reconquest) or turn to the **coast** (Li Hongzhang, writing
   off Xinjiang for the Beiyang fleet — the chain ends).
2. **The reconquest** (`qing_ili.2`, 克復新疆) — press the final strike (destroy Yaqub Beg's
   emirate, restore the grip, close out the rising via a guarded `QING_rebellion_end`) or
   consolidate slowly (a partial, faltering recovery — the chain ends).
3. **Chonghou's blunder** (`qing_ili.3`, 崇厚誤國) — the Livadia disaster: **repudiate** the
   treaty and condemn Chonghou (a war footing with Russia, `qing_gp_tension_russia` +25, the
   ground for a better bargain) or **ratify** it (peace, but the valley ceded — chain ends).
4. **Zeng Jize's treaty** (`qing_ili.4`, 改訂條約) — hold firm for the full recovery of Ili
   (the historic St Petersburg triumph, for an indemnity — prestige, the war footing stands
   down, Russia tension falls) or take a compromise settlement.

Cross-wired to Zeng Jize's roster arrival (§12) and the great-power layer (§15).

**History:** Immanuel Hsü, *The Ili Crisis* (1965); Kim Hodong, *Holy War in China* (2004);
Bales, *Tso Tsung-t'ang* (1937). For the treaty century as a whole: Fairbank & Liu,
*Cambridge History of China* v.10–11; Spence, *The Search for Modern China*; Cohen, *China
and Christianity* (1963); Esherick, *The Origins of the Boxer Uprising* (1987).

---

## 17. The Emperor Emeritus (太上皇) — Napoleon at the Qing court (#65)

A **counterfactual reform chain**: after Waterloo the exiled Napoleon is received in
Beijing instead of sailing for St Helena, and the court revives the 太上皇 (Retired /
Grand Emperor) office — the title the Qianlong Emperor actually held 1796–99 after
abdicating to Jiaqing while keeping real power — conferring it on him. From that seat he
tutors the heir (the future **Daoguang Emperor**, `char:227`), drives a slate of radical
Enlightenment reforms, and steers Qing foreign policy toward his own **revenge on Britain
and Russia**.

**Code:** `se_QING_NAPOLEON.txt` (all `QING_napoleon_*` verbs), `qing_napoleon_events.txt`
(the chain `qing_napoleon.1`–`.4`), `00_napoleon.txt` (the Grande Armée military tradition),
the reform/office/backlash modifiers in `qing_mechanics_modifiers.txt`, loc
`qing_napoleon_l_english.yml` + additions to `qing_mechanics_l_english.yml` and
`military_traditions_l_english.yml`. Offered once via the frontier flavour roll
(`QING_frontier_flavour_roll`), early window only (`current_date < 1821.5.5`, Napoleon's
historical post-Waterloo lifespan), CHI-only, player-only. All logged `sys = QING`.

**The chain.**
1. **L'arrivée** (`qing_napoleon.1`) — the exile offered the throne's right hand. The
   opening text carries the apocryphal *"Let China sleep; when she wakes, she will shake the
   world."* Receiving him conjures a fully-statted Napoleon (`QING_napoleon_spawn`, via the
   shared `QING_roster_finalize` idiom — martial 14, the traits of a great captain) and
   confers the office (`QING_napoleon_take_office`, built on the parameterized
   `QING_office_appoint = { office = emeritus }` machinery). Refusing burns the one-time
   chance for a little stability.
2. **Le grand œuvre** (`qing_napoleon.2`) — a **self-re-triggering reform hub**. Each measure
   is a once-only option (hidden by an option `trigger` once taken):
   拿破崙法典 the **Napoleonic Code** (cuts corruption; +tax/+promotion), 中央銀行 a
   **central bank** (treasury grant; +commerce/+tax), 國民教育 **primary education** (builds a
   school; +research/+promotion), 全民皆兵 the **levée en masse** (raises *La Grande Armée de
   Chine* at the capital under Napoleon's command; cuts banner decay; +manpower/+morale), and
   以夷制夷 the **foreign-policy tilt** (`QING_napoleon_revenge_tilt` → the existing GP-rivalry
   engine: provoke GBR+RUS, warm FRA). Every reform advances the Self-Strengthening progress
   counter and increments `qing_napoleon_reforms_done`.
3. **La réaction** (`qing_napoleon.3`) — the **conservative Manchu backlash**. A foreign
   usurper-emperor forcing reform is divisive: `qing_emeritus_conservative_backlash` rides
   alongside the buffs from the moment he takes office, and the `qing_manchu_staunch`
   conservatives (§ identity band) lose loyalty. The throne stands with him (ease reform
   pressure, −1 stability) or reins him in (soothe the old guard, +1 stability — but he sours).
4. **道光主義 The Daoguang Doctrine** (`qing_napoleon.4`) — the **capstone**, gated on the
   reform slate being substantially complete (`qing_napoleon_reforms_done >= 3`). The heir
   Napoleon tutored proclaims the reforms and the anti-GBR/RUS pro-FRA line a lasting doctrine
   of state, granting the permanent apex modifier `qing_napoleon_daoguang_doctrine` (renamed
   from the bare `qing_daoguang_doctrine`, which is already taken by an unrelated colonization
   modifier — same 道光主義 display name, distinct key).

**Conditional loyalty.** Napoleon is loyal only while his revenge project is served. The
monthly pulse (`QING_napoleon_loyalty_pulse`, wired into `qing_mechanics_pulse_on_action`)
scores him **HIGH** while reforms advance *and* GBR/RUS tension stays high, and **DROPS** when
the court appeases his enemies or lets the reforms stall — so the anti-GBR/RUS pro-FRA tilt is
the *price* of keeping him engaged. When he dies/vacates, the `emeritus` branch of
`QING_office_vacate_dispatch` strips the office bonus and lifts the backlash.

**The Grande Armée tradition** (`00_napoleon.txt`) — a dedicated, **deliberately oversized**
military tradition tree (≈1.5–2× the Manchu tree's buffs), gated NOT on culture group but on
the country variable `qing_napoleon_present` (set by the spawn), so exactly one country in one
timeline can take it. Four theatres + capstone: **La Garde Impériale** (elite heavy infantry),
**Le Dieu de la guerre** (the grand battery, modelled through assault/siege/discipline as the
engine has no artillery arm), **La Manœuvre** (the corps system + forced march: movement,
reinforcement, supply), **Le Maréchalat** (the marshalate + levée: manpower, general loyalty,
experience), capped by **L'Empereur** (the largest single node in the mod).

**History:** the 太上皇 precedent (Qianlong's 1796 abdication) — *Cambridge History of China*
v.9; the Napoleonic reform package (the Code, the Banque de France, the lycée system,
conscription) and the operational art (the corps d'armée, the grand battery, the marshalate) —
standard Napoleonic historiography. The scenario itself is counterfactual.

---

## Appendix — review & correctness notes

The suite was reviewed end-to-end for wiring, consistency, and dead references. Fixes
applied during that review:

* **Amur task** guarded the fortress build on `owns = 6170` rather than `exists`, so it no
  longer fortifies an enemy-held province.
* **Event pictures** — all `picture = senate` corrected to the defined `senate_debate`
  (9 occurrences across the reform/office/keju/roster event files).
* **Opinion** `opinion_improve_relation` (undefined in both vanilla and mod) replaced with
  the mod-owned `qing_gp_relation_opinion` (definition + loc + all three references).
* **Lanfang loc collision** — the modifier display-name key was renamed
  `qing_col_lanfang → qing_col_protectorate_lanfang` to stop it colliding with the task
  title key.
* **44 missing modifier display-names** localised across the colonization, self-
  strengthening, migration, and mechanics loc files (all Qing modifiers now render a name).
* **`qing_reform_faction_balance` initialisation** — the constitutional mission's
  `on_start` now guarantees the variable exists, so the proactive tree no longer relies on
  the crisis event having fired.
* **Suspended integration** — the Integrate button now hides while a subject's integration
  is suspended, so only the Resume button shows (consistent with the pulse).
* **Band-swap tracing** — every modifier-band applier (decline currency/corruption/sect/
  banner/ethnic, governance capacity/integrity/exam-ladder, council, self-strengthening,
  Japan, and the three great-power rivalries) now emits a `LOG_line` recording *which* band
  went active and the counter value that selected it, so a mis-banded counter is visible in
  `debug.log` rather than silent. (`LOG_line`, not `LOG_state` — no per-pulse scope dumps.)
* **`QING_sell_offices` treasury unit** — reviewed and kept as-is: income routes through the
  currency layer's `CURRENCY_grant_country_wealth` (reserve-ratio-scaled), consistent with the
  self-strengthening/colonization/himalaya missions; only *costs* use flat `add_treasury`. The
  tooltip's "~£80" tilde already signals the approximation.
* **Comment/behaviour alignment** — `QING_rebellion_end`'s comment corrected to state the
  one-rising-at-a-time invariant the code actually enforces; the stale `opinion_improve_relation`
  mention in the `QING_gp_react` header comment updated to `qing_gp_relation_opinion`.

**Treaty-century build (§16) review.** The nine systems and the roster expansion (§12) were
reviewed per-task and end-to-end:

* **Central-pulse wiring** — every system's `_pulse` is invoked from `QING_GOV_pulse`
  (steps 6–12); every `_init` is seeded in the `on_game_initialized` CHI block. The port /
  student / treaty pulses are guarded on their "system established" flag so they no-op until
  the system is in play.
* **No duplication of existing content** — the missionary system escalates into the existing
  Boxer rising (`qing_rebellion.9`), and the Ili set-piece connects to the existing
  Dungan/Yaqub Beg revolt (`qing_rebellion.6`) via a guarded `QING_rebellion_end = { flavour
  = ethnic }` (matching how that event's own option ends the rising), rather than re-defining
  either. A phantom `qing_vassal_lost_xinjiang` flag (the vassal system has no Xinjiang
  entry) was replaced with the Ili system's own `qing_xinjiang_abandoned` marker.
* **Reference integrity** — all cross-called effects, all `add_country_modifier`/`remove_
  country_modifier` targets (incl. the five per-power `qing_legation_*_active` variants), all
  `trigger_event` ids, and all localization keys (event text, GUI verb name/desc/gating-
  tooltip, and modifier display-names) resolve. All trigger-read variables are seeded (or are
  set/unset flags). Roster dispatcher flags (`QING_roster_roll`) match each event's
  `set_variable` exactly; no duplicate event ids, spawn flags, or nickname keys.
* **Verified keys** — all new modifier keys checked against `common/modifiers/00_*.txt`; all
  `create_character` culture keys are the same set the existing roster (roster.1–13) uses; the
  substituted traits (the roster memory's `cynical`/`fearful` do not exist as engine traits —
  replaced with `cautious`/`shrewd`/`reckless`).

All script and modifier files balance braces; all localization files carry the UTF-8 BOM
and use the leading-space `key:0 "value"` format Paradox expects (YAML-linter diagnostics
on these files are false positives).
