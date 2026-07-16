# Scripted Revolutions — Design & Decision Log

> **Task (user, 2026-07-16):** Deep-research the exact historical sequence of the **American Revolution**, the **French Revolution & Napoleonic Wars**, and their **ripple onto European Asian colonies + Russia**, and represent them deterministically in the mod via **events**. **No player is involved** — this is strictly about guiding the **AI** down the proper historical path. Script pieces **well in advance** of the revolutions so all the proper pieces are in place. Work without stopping. Note all major decisions here. Finish with a **workflow adversarial review**.
>
> Branch: `merge-overnight` (byte-identical to `1763_bookmark` as of the merge). Game start: **1763.2.16** (day after Treaty of Paris; Seven Years' War just ended).

---

## 0. Scope (as expanded by the user, in order)

1. **American Revolution** (GBR → USA independence, 1763–1783), AI-autonomous.
2. **French Revolution + Napoleonic Wars** (1774–1815) — deepen the existing 5-beat skeleton into a deterministic sequence.
3. **Ripple onto European Asian colonies** — Dutch East Indies, Spanish Philippines, **British India** — with **new/enhanced Qing missions to exploit the opening**.
4. **Russia / Siberia** — Russia deeply distracted by Napoleon → a **Qing tie-in exploiting the Siberia/Amur frontier**.
5. **Expand existing Qing SE-Asia content** (Lanfang 蘭芳, India, etc.) and add new content as appropriate.

**Constraints (standing):** AI-autonomous (self-gate on `tag = X`, never `is_ai = no`); commits authored by freekumquats; independent review before commit; push only when the user asks / at a batch end; proven idioms only; BOM on events/loc `.txt`/`.yml`, none on `.gui`; scripted_gui iterators/create_character must trampoline through hidden events.

---

## 1. Baseline: what already exists (pre-work survey)

### 1763 territorial truth (setup/main/00_default.txt)
- **The Thirteen Colonies are a GBR `client_colony` (tag USA)** in 1763 — `dependency = { first = GBR second = USA subject_type = client_colony }` (line 669). USA reverts from the 1815 sovereign republic to a British colony; historically released as independent by the **`gbr_empire.3` "Loss of America" event (1783)**.
- USA trimmed to the Atlantic-seaboard Thirteen Colonies (#397/BT-60); trans-Appalachian frontier left unowned.
- **Spanish Louisiana** (tag LSA) — SPA `client_colony` per Treaty of Fontainebleau (1762/63), until 1800 retrocession → 1803 Louisiana Purchase.

### Existing France arc (the "high-level, not deterministic" content to deepen)
- `events/imp19c_mod_events/fra_revolution_events.txt` (271 lines, namespace `fra_revolution`, #283): a **5-beat skeleton** —
  - `.1` 1774 Accession of Louis XVI (fiscal-crisis modifier)
  - `.2` 1789 Bastille (stability collapse)
  - `.3` 1792 First Republic (monarchy → republic government transition)
  - `.4` 1799 18 Brumaire (Napoleon installed via create_character + set_as_ruler)
  - `.5` 1804 First Empire
  - `.6` 1814 Restoration
- Seeded by `common/on_action/fra_revolution_on_actions.txt` via the on_actions LIST form of `on_game_initialized`, `tag = FRA` gate, day-offsets from 1763.2.16. Offsets recorded there:
  - 1774.5.10 accession → 4101 · 1789.7.14 Bastille → 9645 · 1792.9.21 Republic → 10810 · 1799.11.9 Brumaire → 13415 · 1804.12.2 Empire → 15264 · 1814.4.6 fall → 18676
- **Design note in that file:** GP wars (#303) ARE scripted separately as dated war-declaration events (the earlier "leave wars to the engine" note was reversed by user directive 2026-07-09). Character deaths use setup death_dates (Louis XV d.1774, Louis XVI d.1793).
- **Napoleon-at-Qing-court** alt-history (`qing_napoleon_events.txt`, se_QING_EMERITUS) — a SEPARATE alt-history branch reached only via the Amherst embassy route; not part of the base European arc.

### Existing GBR arc (`gbr_empire`, #283)
- `events/imp19c_mod_events/gbr_empire_events.txt` — 6 beats, `tag = GBR` gated, done-flags + ai_chance:
  - `.1` 1765.3.22 Stamp Act · `.2` 1775.4.19 The American War · `.3` **1783.9.3 Loss of America** (`release_subject = c:USA` — the actual independence release, guarded on USA still being GBR's subject) · `.4` 1801 Act of Union · `.5` 1805 Trafalgar · `.6` 1815 Waterloo.
  - Currently mostly prestige/stability/aggressive_expansion **posture nudges** — the "high-level, not deterministic" content. `.3` is the one load-bearing state change (the release).
- Seeded by `common/on_action/gbr_empire_on_actions.txt`.

### Existing dated-WAR backbone (`imp19c_setup`, #302/#303)
- `events/imp19c_mod_events/imp19c_setup_events.txt` — hidden one-shot war-declaration events via **`FUNC_declare_war_with_wargoal_province`**:
  - `.1` 1810 Spanish-American independence wars (`setup_trigger_spanish_american_independence_wars`)
  - `.2` **1775 American Revolutionary War** — USA (GBR client_colony) declares `independence_wargoal` on GBR, province=capital_scope
  - `.3` 1792 War of the First Coalition — FRA `conquer_wargoal` vs AUS (p:245) + PRU (p:929)
  - `.4` 1803 Anglo-French resumption — FRA vs GBR (p:3388)
  - `.5` 1805 Third Coalition — FRA vs AUS (p:245) + RUS (p:3174)
- Seeded from `common/on_action/economy/oa_economy_setup.txt` (offsets: USA war 4445, FRA coalition wars 10656/14700/15559, SPA 17120).
- **Key verbs confirmed available:** `FUNC_declare_war_with_wargoal_province = { war_goal=X province=Y target=c:TAG }` (wraps `declare_war_with_wargoal` + `add_to_war`), `release_subject = c:TAG`, wargoals `independence_wargoal`/`conquer_wargoal`. `war_with = c:TAG` guard for idempotency.

### Territory / war / country verbs for RAILROADING (proven in-mod)
- **`p:N = { set_owned_by = c:TAG }`** — the proven province→country ownership transfer (se_QING_BURMA.txt:149, se_QING_ILI, sell_province_events, se_FUNC). `owner =` is read-only; `set_owned_by` is the settable form. Also `set_controlled_by`.
- **`release_subject = c:TAG`** (overlord scope) — free a subject to independence (gbr_empire.3).
- **`LAND_release_from_list`** — carve a new country from a province subset (saves `scope:new_country_scope`); the SEPARATISM/protectorate/USCW path.
- **`change_country_tag = X`** — in-place tag change (tag must pre-exist in countries.txt).
- **`create_country`** (province scope) — genuinely new realm.
- **`start_civil_war = scope:<char>`** (remove_all_positions first).
- **`add_alliance = c:TAG` / `add_guarantee = c:TAG`**; `create_subject`/`release_subject`; `add_truce`.
- **create_character** — no name/modifiers in block (#90), add_nickname after; set culture+religion+age.
- Because **all non-Qing are AI (railroad freely)**, I can also just `set_owned_by` the historical peace outcomes directly at the treaty date rather than depend on the AI winning the scripted war — belt-and-braces determinism.

### Existing USA arc
- `events/imp19c_mod_events/usa_section_events.txt` — "The House Divided" (1815–1861 sectional crisis → Civil War), AI-autonomous, 12 beats. This is the *post-independence* arc; the *Revolution itself* is not yet scripted (only the `gbr_empire.3` release exists). **New American Revolution arc must dovetail into the existing USA tag before this arc's 1820 start.**

### AI-autonomous arc idioms available (memory imp19c-ai-autonomous-arc-verbs, oracle-verified)
- Dated one-shots fire for AI via `on_game_initialized` → `trigger_event = { id=X days={A B} }`; each event re-checks its own done-guard. Self-gate `tag`, never `is_ai = no`.
- `start_civil_war = scope:<char>` (remove_all_positions first, reach breakaway via `scope:leader.employer`).
- `LAND_release_from_list` (saves `scope:new_country_scope`) — proven release path.
- `change_country_tag = X` in place (tag must exist in countries.txt); cosmetic changes in `hidden_effect`.
- Cross-event country handoff via **global variable**, not raw `scope:`.
- `create_character`: set culture+religion+age, `save_scope_as` immediately, NO name arg / NO modifiers inside (the #90 boot-crash rule); identity via add_nickname.
- `add_alliance` / `add_guarantee` (NOT create_alliance).
- Every AI-reachable option needs explicit `ai_chance`.

---

## 2. Research (agents dispatched 2026-07-16)

Six background agents (English + French + Russian + Chinese sources + mod scout):
- **AmRevResearch** — American Revolution 1763–1783 chronology + causal turning points.
- **FrRevResearch** — French Revolution + Napoleonic Wars 1774–1815 (English + French sources).
- **AsiaColonyResearch** — Rev/Napoleon impact on Dutch E. Indies, Spanish Philippines, British India + Lanfang.
- **RussiaResearch** — Russia in the coalitions + Russian Far East/Siberia/Amur exposure + Qing frontier angle.
- **QingCJKResearch** — (Chinese sources) Qing–SE Asia, 蘭芳公司, 華僑, tributary framework, Tây Sơn 1788.
- **ModContentScout** — existing mod content (Qing SE-Asia/Lanfang/India/Siberia), mission-tree patterns, arc machinery, gbr_empire events.

*(Findings distilled below as agents report.)*

---

## 3. Design decisions

*(populated as research lands + scripting proceeds)*

### Decided so far
- **D0 — RAILROAD FREELY (user directive 2026-07-16):** *Every country except Qing is AI and can be railroaded safely.* I have **great leeway to hard-script** the raising of armies, the starting/ending of wars, and territorial changes. → **Design consequence:** the American/French/Napoleonic arcs are scripted **DETERMINISTICALLY** — force the historical government transitions, ruler installs, war declarations, province transfers, and peace outcomes outright (in `immediate {}` / `hidden_effect {}`), rather than relying on soft `ai_chance` weights and hoping the AI complies. `ai_chance` is now only a *flavour* nicety on any surfaced option; the load-bearing outcome is forced. **The SOLE exception is Qing (CHI):** the player controls it, so all Qing-facing content (the SE-Asia / India / Siberia exploitation missions) must **offer opportunities, never force** — normal mission/event choices with real player agency.
- **D1 — Base branch:** work on `merge-overnight` (== 1763_bookmark content). All revolution work lands here.
- **D2 — American Revolution is a NET-NEW arc** (only the 1783 `gbr_empire.3` release exists today); it must pre-position tension from 1763 and hand off cleanly to the existing USA tag / `usa_section` arc.
- **D3 — French arc is a DEEPENING** of the existing `fra_revolution` skeleton, not a rewrite — preserve its offsets/guards, add intermediate beats + coalition wars.
- **D4 — AI-autonomy is mandatory** for every beat (self-gate on tag, ai_chance on every option, load-bearing changes in immediate{}).
- **D5 — Asian-colony ripple + Qing missions** are downstream of the European arcs: the "opening" is the window (~1795–1815) when European metropoles were cut off from their Asian colonies.
- **D6 — Scripting proceeds from established history + the computed offset table** (§4), with the six research agents' findings folded in as citations/contingency-weights/obscure detail (Lanfang structure, Tây Sơn, exact character dates) as they report. The core beat structure of these well-documented events does not block on the research. Rationale: user directive "work without stopping"; the offsets are pure arithmetic and the causal chains are canonical.
- **D7 — Extend, don't replace, the three existing AI arcs.** `gbr_empire` (American Rev + British Napoleonic beats), `fra_revolution` (French Rev + Napoleon transitions), and `imp19c_setup` (the dated GP-war declarations) already exist and interlock. Deepen each in place — add the missing causal beats and make the load-bearing outcomes deterministic (`set_owned_by` / `release_subject` / forced government+ruler) rather than posture-nudges — preserving existing done-flags/offsets so nothing double-fires.

---

## 4. Day-offset table (from START_DATE 1763.2.16)

All computed as `(historical_date − 1763.2.16)` in days. Seed windows use `{ off  off+90 }` so a beat lands in its correct historical quarter; each event re-checks its own done-guard, so wide windows are safe/idempotent. **These are the authoritative scheduling numbers for every arc below.**

### American Revolution (GBR→USA)
| off | date | beat |
|----:|------|------|
| 233 | 1763.10.07 | Proclamation Line of 1763 |
| 414 | 1764.04.05 | Sugar Act |
| 765 | 1765.03.22 | Stamp Act *(gbr_empire.1 already here)* |
| 964 | 1765.10.07 | Stamp Act Congress |
| 1126 | 1766.03.18 | Repeal + Declaratory Act |
| 1594 | 1767.06.29 | Townshend Acts |
| 2574 | 1770.03.05 | Boston Massacre |
| 3736 | 1773.05.10 | Tea Act |
| 3956 | 1773.12.16 | Boston Tea Party |
| 4061 | 1774.03.31 | Coercive/Intolerable Acts |
| 4219 | 1774.09.05 | First Continental Congress |
| 4445 | 1775.04.19 | Lexington & Concord *(imp19c_setup.2 war seed here)* |
| 4504 | 1775.06.17 | Bunker Hill; Washington takes command |
| 4887 | 1776.07.04 | Declaration of Independence |
| 5357 | 1777.10.17 | **Saratoga** (the hinge → French entry) |
| 5469 | 1778.02.06 | Franco-American Alliance |
| 5969 | 1779.06.21 | Spain enters |
| 6820 | 1781.10.19 | Yorktown |
| 7504 | 1783.09.03 | Treaty of Paris *(gbr_empire.3 release_subject USA)* |

### French Revolution + Napoleonic Wars (FRA)
| off | date | beat |
|----:|------|------|
| 4101 | 1774.05.10 | Louis XVI accession *(fra_revolution.1)* |
| 8772 | 1787.02.22 | Assembly of Notables (fiscal crisis peaks) |
| 9575 | 1789.05.05 | Estates-General |
| 9621 | 1789.06.20 | Tennis Court Oath |
| 9645 | 1789.07.14 | **Bastille** *(fra_revolution.2)* |
| 9688 | 1789.08.26 | August Decrees / Rights of Man |
| 10008 | 1790.07.12 | Civil Constitution of the Clergy |
| 10351 | 1791.06.20 | Flight to Varennes |
| 10426 | 1791.09.03 | Constitution of 1791 |
| 10656 | 1792.04.20 | War on Austria *(imp19c_setup.3 1st Coalition)* |
| 10768 | 1792.08.10 | Storming of the Tuileries |
| 10809 | 1792.09.20 | Valmy |
| 10810 | 1792.09.21 | **Republic proclaimed** *(fra_revolution.3)* |
| 10932 | 1793.01.21 | Execution of Louis XVI |
| 11159 | 1793.09.05 | Terror / Committee of Public Safety |
| 11484 | 1794.07.27 | Thermidor (fall of Robespierre) |
| 11919 | 1795.10.05 | Directory / Vendémiaire |
| 12109 | 1796.04.12 | Italian campaign begins |
| 12919 | 1798.07.01 | Egyptian expedition |
| 13415 | 1799.11.09 | **18 Brumaire** (Consulate) *(fra_revolution.4)* |
| 14028 | 1801.07.15 | Concordat |
| 14281 | 1802.03.25 | Peace of Amiens |
| 15264 | 1804.12.02 | **First Empire** *(fra_revolution.5)* |
| 15629 | 1805.12.02 | Ulm/Austerlitz *(imp19c_setup.5 3rd Coalition)* |
| 15945 | 1806.10.14 | Jena-Auerstedt |
| 16211 | 1807.07.07 | Friedland / Tilsit |
| 16511 | 1808.05.02 | Peninsular War begins |
| 16941 | 1809.07.06 | Wagram |
| 18025 | 1812.06.24 | **Invasion of Russia** |
| 18100 | 1812.09.07 | Borodino |
| 18504 | 1813.10.16 | Leipzig (Battle of Nations) |
| 18676 | 1814.04.06 | Abdication / Elba *(fra_revolution.6)* |
| 19024 | 1815.03.20 | Hundred Days begin |
| 19114 | 1815.06.18 | **Waterloo** *(gbr_empire.6)* |
| 19134 | 1815.07.08 | Second Restoration |

### Asian-colony ripple + Russia/Siberia
| off | date | beat |
|----:|------|------|
| 5068 | 1777.01.01 | Lanfang Kongsi 蘭芳公司 founded (Luo Fangbo) |
| 9116 | 1788.02.01 | Tipu Sultan's embassy to France |
| 9480 | 1789.01.30 | Tây Sơn defeat Qing at Ngọc Hồi (Vietnam) |
| 11660 | 1795.01.19 | Batavian Republic — Dutch fall to France |
| 12328 | 1796.11.17 | Paul I of Russia accedes |
| 13226 | 1799.05.04 | Seringapatam — Tipu dies, 4th Anglo-Mysore War |
| 13467 | 1799.12.31 | VOC dissolved |
| 13914 | 1801.03.23 | Franco-Russian India plan; Paul I assassinated |
| 16211 | 1807.07.07 | Tilsit (Russia allied to France) |
| 17700 | 1811.08.04 | British take Java (Raffles) |
| 18025 | 1812.06.24 | Napoleon invades Russia (Far East stripped) |
| 18670 | 1814.03.31 | Russians in Paris |
| 19542 | 1816.08.19 | Java returned to the Dutch (window closes) |

**Windows of opportunity for the Qing (distracted-Europe):**
- **SE Asia / Dutch:** ~1795 (Batavian Republic) → 1811 (British take Java) → 1816 (return) — Batavia cut off from its metropole 1795–1815.
- **Philippines / Spain:** ~1796–1814 (Spain pinned by Peninsular War; Manila isolated).
- **British India:** ~1798–1799 (Napoleon in Egypt threatens India; Mysore crisis) — the EIC most stretched.
- **Russia / Siberia-Amur:** ~1805–1814 (Russian army/attention pinned in Europe; Far East thin).

## 5. Event/file manifest

### American Revolution — DONE (deepened `gbr_empire` arc)
- `events/imp19c_mod_events/gbr_empire_events.txt` — expanded 6→12 beats. NEW: `.7` Proclamation 1763, `.8` Townshend, `.9` Tea Party→Coercive Acts, `.10` First Continental Congress, `.11` **Saratoga → France enters** (railroaded: `c:FRA = { add_alliance = c:USA + FUNC_declare_war… vs GBR }`), `.12` Yorktown. KEPT: `.1` Stamp Act, `.2` American War, `.3` **Loss of America** (now also `force_white_peace = c:USA`/`c:FRA` before `release_subject = c:USA` for a clean settled map), `.4` Union, `.5` Trafalgar, `.6` Waterloo. Added a `gbr_colonial_grievance` meter (seeded in .7, built up through the tax beats — flavour/analytics, load-bearing outcome is still the forced release). All done-flags preserved (no double-fire).
- `common/on_action/gbr_empire_on_actions.txt` — seeded all 12 beats at the §4 offsets.
- `localization/english/gbr_empire_l_english.yml` — +6 beat loc blocks (.7-.12).
- **Verbs used (all proven):** `add_alliance = c:USA`, `FUNC_declare_war_with_wargoal_province`, `force_white_peace = c:TAG` (WAR_scripted_guis.txt:1202 / se_AI.txt:2624), `release_subject = c:USA`. BOM preserved on both .txt and .yml.

### French Revolution + Napoleon — DONE (deepened `fra_revolution` arc)
- `events/imp19c_mod_events/fra_revolution_events.txt` — expanded 6→15 beats. KEPT `.1` accession, `.2` Bastille, `.3` Republic (change_government revolutionary_republic), `.4` Brumaire (create Napoleon + personalist_dictatorship + set_as_ruler), `.5` Empire (imperial_monarchy), `.6` Restoration (absolute_kingdom + char:411 Louis XVIII). NEW: `.7` Assembly of Notables, `.8` Estates-General/Tennis Court Oath, `.9` **Regicide+Terror+levée en masse** (`add_manpower = 20`), `.10` Thermidor, `.11` Directory, `.12` Egypt, `.13` Austerlitz, `.14` **Russia 1812** (`add_manpower = -25` + war_exhaustion), `.15` Hundred Days (re-seats `scope:fra_napoleon` if alive + imperial_monarchy).
- **Ordering safety:** dependent beats gate on prior milestone done-flags (`.9` needs `fra_beat_republic` set by `.3`; `.13`/`.14` need `fra_beat_empire` set by `.5`; `.15` needs `fra_beat_restoration`). The milestone events are seeded at EARLIER offsets than their dependents (10810<10932, 15264<15629/18025, 18676<19024), so the flag is always set when the dependent fires. `.7`/`.8` self-skip if the Revolution already broke out (guard on `fra_beat_1789`/`_republic`).
- `common/on_action/fra_revolution_on_actions.txt` — all 15 beats seeded at §4 offsets, in chronological order.
- `localization/english/fra_revolution_l_english.yml` — +9 beat loc blocks (.7-.15).
- **Verbs used (all proven):** `change_government`, `create_character`+`set_as_ruler`, `add_nickname`, `add_manpower` (se_QING_ILI.txt:129), `add_war_exhaustion` (se_setup.txt), `char:411 set_as_ruler`, `scope:fra_napoleon` reuse. **Caveat for review:** `scope:fra_napoleon` in `.15` is a saved scope from `.4` — it may not survive across the ~16-year gap / save-reload; guarded on `exists` so it degrades to a flavour beat if lost (acceptable — the government change still fires).

### Asian-colony board — TAGS ALREADY EXIST (major finding)
The 1763 setup already models the exact pieces needed (setup/countries/countries.txt + setup/main/00_default.txt):
- **`DEI`** Dutch East Indies — `NED → DEI autonomous_colony` (line 913); DEI holds Borneo protectorates BJR/BCN.
- **`LAF`** Lanfang — **`CHI → LAF nominal_vassal` (line 828)** — the Lanfang Kongsi is ALREADY a Qing nominal vassal at start! Allied to **`PNK`** Pontianak (line 831).
- **`PHI`** Philippines — `NSP → PHI autonomous_governorship` (line 769) (New Spain / Spanish).
- **`SLU`** Sulu, **`SIK`** Siak, **`VIE`**/**`TRH`** Vietnam (Nguyễn/Trịnh), **`SIA`** Siam, **`EIC`** the Company (India tree).
- **Design consequence:** the exploitation missions don't need to create tags — they leverage the Napoleonic disruption of NED (1795 Batavian Republic) / SPA (Peninsular War) to let the Qing (already Lanfang's suzerain) press into the archipelago, and the EIC's Egypt/Mysore stretch (1798-99) to reinforce the existing India tree (#449).

### Asian-colony ripple + Qing exploitation + Russia/Siberia — DONE
**Ripple events** (NEW `events/imp19c_mod_events/asia_napoleonic_events.txt`, namespace `asia_napoleonic`, seeded from NEW `common/on_action/asia_napoleonic_on_actions.txt`, fired to c:CHI as carrier):
- `.1` 1795 Batavian Republic → DEI cut off (`asia_dei_cutoff` global flag + `asia_colony_cut_off` modifier on DEI).
- `.2` 1808 Peninsular War → PHI cut off (`asia_phi_cutoff` + modifier on PHI).
- `.3` 1798 Napoleon-in-Egypt + Mysore → EIC overstretched (`asia_india_opening` + `asia_company_overstretched` on EIC, ~15 yr).
- `.4` 1816 Europeans return → `asia_window_closed`, clears the cut-off modifiers (Qing gains stand).
- `.5` 1812 Napoleon invades Russia → RUS Far East stripped (`asia_russia_distracted` + `asia_russia_pinned_west` on RUS, ~3 yr).
- Events carry a player-facing notify (option gated `tag = CHI`) + a silent AI branch; the load-bearing effect (flags/modifiers) is in immediate{}.

**Qing Nanyang mission tree** (NEW `common/missions/qing_nanyang_missions.txt` "南洋乘機", CHI player-only, unlocks on the cut-off flags OR c:LAF existing; texture in NEW `common/scripted_effects/se_QING_NANYANG.txt`): champion the 華僑 → fork W (consolidate **Lanfang** LAF from nominal_vassal → firm tributary; secure Pontianak p:2604) / fork E (embrace **Sulu** SLU — the 1753 overture; strike a severed colony — Batavia p:6270 or Manila p:2004) → capstone `qing_nanyang_hegemony`. Uses `FUNC_make_subject`/`add_claim`/`QING_gp_provoke_britain` — all proven. **Respects D0 (Qing = player): offers, never forces.**

**Russia/Siberia:** reinforces the EXISTING `qing_col_amur` mission (colonization tree) rather than duplicating — added a `has_global_variable = asia_russia_distracted` bonus branch (extra Outer-Manchuria claim + stability when the Amur is pressed during the 1812-15 Russian distraction). The `.5` event supplies the flag + the RUS weakness modifier.

**Modifiers** (NEW `common/modifiers/asia_napoleonic_modifiers.txt`): `asia_colony_cut_off`, `asia_company_overstretched`, `asia_russia_pinned_west`, `qing_nanyang_protector`, `qing_nanyang_hegemony`. All keys verified in 00_from_events_country / qing_india_modifiers.
**Loc** (NEW `localization/english/qing_nanyang_l_english.yml`): Nanyang tree + all 5 ripple events + all modifiers; +1 key in qing_colonization loc (`qing_col_amur_napoleonic_tt`).

### Tag/province reference (for the review)
- Colonies: DEI (cap 6270 Batavia), PHI (cap 2004 Manila), LAF (cap 2604 Pontianak, CHI nominal_vassal), SLU (cap 6503), EIC (India tree).
- Amur (existing tree): p:6170 Aigun (fortress), p:11553 Okhotsk/Outer-Manchuria (claim + frontier play).

---

## 6. Pre-review integrity sweep (2026-07-16) — PASS

- **Brace balance:** all 10 touched `.txt` files balanced (verified).
- **BOM:** events `.txt` + loc `.yml` + on_action + modifiers + scripted_effects all carry BOM; mission files (`qing_nanyang_missions.txt`) NO-BOM to match siblings (qing_india/himalaya_seasia are NO-BOM); `qing_colonization_missions.txt` NO-BOM preserved (pre-existing state).
- **No ID/namespace collisions:** `asia_napoleonic` namespace unique; `qing_nanyang_mission` group unique; new event IDs (gbr_empire.7-.12, fra_revolution.7-.15, asia_napoleonic.1-.5) don't clash.
- **Loc coverage:** every `custom_tooltip`/`text=`/`name=` key referenced by the new content is defined.
- **Verbs all proven:** `release_subject`, `force_white_peace`, `add_alliance`, `FUNC_declare_war_with_wargoal_province`, `FUNC_make_subject`, `change_government`, `create_character`+`set_as_ruler`+`add_nickname`, `add_manpower` (incl. negative — se_QING_WORKS.txt:439), `add_war_exhaustion`, `add_claim`, `QING_gp_provoke_britain/russia`, `set_owned_by` (available, not needed — releases/claims sufficed). All modifier keys verified in 00_from_events_country / qing_*_modifiers.
- **Files auto-load** by directory scan (mission/event/modifier/on_action dirs).

## 7. Research status — DELIVERED (2026-07-16, late)

The research agents ultimately returned. Findings **corroborate** the scripted dates end-to-end (AmRev + FrRev/Napoleon beat lists match the §4 offsets exactly) and enriched the Asian material. Key reconciliations applied:

- **CORRECTION (applied):** the Sulu "1753 submission offer" I wrote was **unattested**. The real anchor is the **1726-1733** Sulu tribute to the Qing (revived after a ~300-yr Ming-era lapse). Fixed in qing_nanyang_missions.txt, se_QING_NANYANG.txt, and the loc.
- **Lanfang nuance:** history is that Qianlong *rejected formal tributary status* but accepted a *trade* tie (Luo Fangbo 1777; Luo d.1795). The mod's setup nonetheless ships `CHI → LAF nominal_vassal`, so my "raise nominal→firm tributary" arc is alt-history built on the mod's own board — defensible, kept.
- **AmRev causal chain confirmed:** Saratoga (1777.10.17) → **Franco-American alliance (1778.02.06)** is the load-bearing hinge (matches my gbr_empire.11 forcing France in AFTER Saratoga). French war debt → French Revolution link corroborated.
- **FrRev confirmed:** all 52 researched beats align with the scripted 15; contingency weights (Bastille 40%, regicide 55%, Thermidor 50%, Waterloo 50% — but arc-beats scripted deterministically for AI flow, per D0) support the railroad approach.

**Additional mission hooks the research surfaced (NOT yet built — candidate follow-up pass):** the Tây Sơn/Vietnam 1788-89 intervention choice (refuse / historical defeat / commit-and-win — a strong datable Qing southern venture, Battle of Ngọc Hồi-Đống Đa); "The Chinese King of Siam" (Taksin, half-Chinese, Qing recognition 1772); "Avenge the Batavia Massacre (紅溪慘案 1740)"; Penang 1786 contest; end-the-海禁 reform. These fit the existing himalaya_seasia / colonization / nanyang trees and could deepen the Qing-Nanyang content further if the user wants a second pass.

## 8. Adversarial review — DONE (2026-07-16)

Ran a workflow: 4 dimension reviewers (boot-crash / ai-autonomy / historical / integration) → each finding adversarially verified by an independent skeptic → synthesis. **11 agents, 7 findings raised, 3 CONFIRMED (all medium), 4 refuted.** No boot-crash or AI-autonomy defects found. All 3 confirmed findings FIXED:

1. **Missing Second Restoration** (historical + integration, found twice) — after the Hundred Days (`fra_revolution.15`) re-installed Napoleon, nothing reverted France; it stayed a Bonapartist `imperial_monarchy` forever post-1815. **FIX:** added `fra_revolution.16` "The Second Restoration" (offset 19134, after Waterloo 19114): `change_government = absolute_kingdom` + re-seat Louis XVIII (char:411), gated on `fra_beat_hundred_days`. Seeded + loc'd.
2. **Dead `asia_india_opening` flag** (integration) — `asia_napoleonic.3` set the flag but nothing read it; the documented India-tree dovetail didn't exist (only the EIC modifier worked). **FIX:** wired `qing_india_descent` to read `has_global_variable = asia_india_opening` — a stability + popularity bonus if the descent is mounted during the Company's Napoleonic overstretch. +loc `qing_india_descent_napoleonic_tt`.
3. (Same as #1, raised independently by the integration reviewer — same fix.)

**Refuted (correctly, no change):** Saratoga→France-entry "compression" (the window fires before the historical treaty + matches when news reached Paris — sound); Sulu/counterfactual narrative nits (deliberate alt-history); LAF-available-from-start (intended + documented). The Sulu **date** error was separately caught from the research reconciliation and fixed (§7).

## 9. Open questions / residual risks

- Boot-crash safety: no scripted_gui iterator inlining (all these are events, not scripted_guis, so lower risk); watch create_character (#90 rule — no modifiers/loyal-veterans in the create block).
- Tag existence: any new country tags (if needed) must be added to `setup/countries/countries.txt` before `change_country_tag`.
- Offset arithmetic: all dated beats computed as (historical_date − 1763.2.16) in days; windows `{ off  off+90 }`.
- AI war prosecution: reconquest/wargoal needs `add_claim` on target provinces first for the AI's `allow` to pass.
