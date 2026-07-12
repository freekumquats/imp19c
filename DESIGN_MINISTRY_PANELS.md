# DESIGN — Qing Ministry Management Panels (War · Works · Lifan Yuan Directorate)

**Status:** SCOPED, not built. Design spec captured 2026-07-11 from the exploration of the
existing Grand Council / War-office / Works / Lifan-Yuan machinery. Related tasks: #346 (frontier
garrisons under War Ministry), #347 (standing-army province effects). This spec supersedes the
"mirror the Works panel" phrasing — the panels mirror the **Grand Council GUI**.

---

## 1. Concept

Three new **Ministry management panels**, each a standalone L4 window that clones the Grand
Council tab's layout. Each panel gives one great office a dedicated command surface:

| Panel | Office key | Minister (top slot) | Manages |
|---|---|---|---|
| **Ministry of War** (兵部) | `war` | Grand Minister of War | all garrisons + commanders |
| **Ministry of Works** (工部) | `works` | Minister of Works | all special buildings / canals / dikes |
| **Lifan Yuan Directorate** (理藩院) | `lifanyuan` | Grand Director of the Lifan Yuan | all Ambans + Inner-Asian subjects |

How well or poorly each Ministry is doing **directly feeds the Minister's standing on the Grand
Council** (via the same `qing_council_effectiveness` / accountability-band hooks the offices
already use — see §6).

---

## 2. Shared panel layout (clone of the Grand Council tab)

The Grand Council is NOT a standalone `.gui` file — it is the 4th tab inside
`gui/government_view.gui` (`flowcontainer name="Grand Council tab"`, from **line 2237**), gated
`visible = "[GetVariableSystem.HasValue('qing_gc_tab', 'grand_council')]"`. For the three new
panels we instead build **standalone `base_sub_window`s** opened by the proven
`createwidget` / `ClearWidgets` idiom (the province-reports pattern, §7), because they are opened
from buttons outside the government view. The *internal layout* is cloned from the council tab.

Top-to-bottom structure of each Ministry panel:

### (A) Summary bar — very top
Three aggregate readouts, mirroring the council's roster summary bar (`government_view.gui:2257-2304`):

1. **Filled / total positions** — `icon_and_text`, text `[...Var('<count var>').GetValue|0] / <total>`.
   The council uses `qing_council_filled_count` / 13. Each Ministry needs its OWN filled/total of
   just that ministry's seats (Minister + its subordinates) — a new per-ministry count var
   (e.g. `qing_war_seats_filled` / `qing_war_seats_total`), computed in that ministry's pulse.
2. **Statesmanship bar** — `icon_and_text_progress_S`, a 0..100→0..1 scaled bar. The council's
   effectiveness bar idiom (`:2279-2284`):
   ```
   value = "[FixedPointToFloat( Multiply_CFixedPoint( GovernmentView.GetPlayer.MakeScope.GetVariable('<var>').GetValue, '(CFixedPoint)0.01' ) )]"
   ```
   Per-ministry this is the ministry-performance score (§6): `qing_war_ministry_perf`, etc.
3. **Ethnic-balance counter** — `icon_and_text`. The council shows a Han/Manchu split
   (`government_view.gui:2289`, from the #308 Han/other balance system). Each ministry can show
   the ethnic split of ITS OWN seat-holders (a per-ministry recompute) or reuse the council-wide
   figure — decide per ministry; War (banner vs green-standard officer corps) genuinely differs
   from the council-wide split, so War computes its own.

### (B) Minister card — the "Grand Chancellor slot"
Clone the Chancellor **summit card** (`government_view.gui:2614-2716`): wide card,
`datacontext = "[...Var('qing_office_<key>_holder').GetCharacter]"`, FILLED branch gated on
`...IsSet`, VACANT branch on `[Not(...IsSet)]`. Inside FILLED: `cpt_button` portrait,
`qing_favor_square`, `qing_faction_square`, name tag, the **4-skill row** of `icon_and_text`
(`[Character.GetMartial]` / `GetFinesse` / `GetCharisma` / `GetZeal`), loyalty `icon_and_text`,
and a **statesmanship bar** `icon_and_text_progress_S` value `[FixedPointToFloat( Character.GetExperience )]`.
Appoint/Replace button repeats the picker idiom (`:2679-2688`):
```
onclick = "[GetVariableSystem.Set('qing_gc_picker_office', '<key>')]"
onclick = "[GetScriptedGui('qing_gov_refresh_candidates_<skill>').Execute( GuiScope.SetRoot( Player.MakeScope ).End )]"
onclick = "[ExecuteConsoleCommand('gui.createwidget gui/imp19c_windows.gui qing_office_picker_window')]"
```

### (C) Ministry-health modifier list — alongside/under the Minister card
A list of the modifiers tracking that ministry's health.

**GUI-idiom caveat (important):** NO Qing panel currently lists active modifiers via a datamodel.
The only proven "list of active modifiers" idiom in the codebase is vanilla
`gui/province_window.gui:1131-1148` (`overlappingitembox datamodel="[ProvinceWindow.GetModifiers]"`
+ `modifier_icon` + `TimedModifier.GetTooltip`) — but `GetModifiers` is a C++ method on specific
window contexts, and there is **no confirmed script-scope `GetActiveModifiers` on a country** exposed
to a custom scripted_gui. So we CANNOT reliably rebuild a live country-modifier list from
`Player.MakeScope`.

**Chosen approach:** the **fixed-meter list** idiom (matches sibling panels `qing_religion.gui:134-233`
and `qing_greatgame.gui:203-364`): a vertical stack of labelled `progressbar` rows bound to named
health vars, one row per health dimension. This renders the "health of the Ministry" as concrete
meters rather than a dynamic modifier icon-list. Where we specifically want to show an active
country/character modifier icon, render it as a fixed conditional row gated on
`has_country_modifier` / `has_character_modifier` (the minister's `.GetCharacter` datacontext for
character-scope ones — country and character modifiers cannot share one datamodel).

### (D) Subordinate office-holders — below
Clone the subordinate office grid (`government_view.gui:2808-`). NOT a datamodel — a hand-built
grid of compact office cards (`government_view.gui:3151-3216` is the war-office card), each
`datacontext = "[...Var('qing_office_<sub>_holder').GetCharacter]"` with FILLED/VACANT branches,
portrait, name, loyalty, a narrow statesmanship bar (`[FixedPointToFloat( Character.GetExperience )]`),
and an appoint button. For the **War panel** the subordinates are e.g. the Guard Commandant
(`guard_commandant`) + frontier garrison commanders; for **Works** the subordinate directors; for
the **Lifan Yuan Directorate** the Ambans (see §5 — Ambans may be a *datamodel* list rather than fixed cards,
because they are per-subject and variable in number).

### (E) Ministry Directives — bottom action strip
Clone the "Grand Council Edicts" strip (`government_view.gui:4053-4260`): a column of
`text_button_square_highlighted`, each wired to a scripted_gui verb:
```
datacontext = "[GetScriptedGui('<verb>')]"
visible = "[ScriptedGui.IsShown( GuiScope.SetRoot( Player.MakeScope ).End )]"
blockoverride "On_click" {
    enabled = "[ScriptedGui.IsValid( GuiScope.SetRoot( Player.MakeScope ).End )]"
    onclick = "[ScriptedGui.Execute( GuiScope.SetRoot( Player.MakeScope ).End )]"
}
```
A directive verb either fires an effect directly or `trigger_event = { id = ... }`. Existing war
directives already live in `common/scripted_guis/QING_mechanics_actions.txt`
(`qing_action_sanction_regional_army`, `qing_action_reassert_central_command`,
`qing_action_fund_modern_army`, drill actions) — the War panel's Directives section reuses these.

---

## 3. Ministry of War (兵部) panel

**Backend already largely exists (feature #331) — the panel surfaces it.**

- Office: key `war`, holder var `qing_office_war_holder`, scored on **martial**
  (`se_QING_COUNCIL.txt:160`), grants country modifier `qing_office_war_active`
  (`qing_governance_modifiers.txt:135`, LOGISTICS/UPKEEP). Appoint via
  `qing_gov_refresh_candidates_martial` + picker.
- **Garrison/commander linkage (built):**
  - Officer-corps coupling into council effectiveness: `se_QING_COUNCIL.txt:370-409` — walks
    `every_unit` w/ `has_commander`, sums commander martial into `qing_officer_corps_martial` /
    `qing_officer_corps_count`, folds deviation from baseline into `qing_council_eff_target`.
  - Quarterly commander review `QING_war_review_commanders` (`se_QING_WAR.txt:42-164`), saves
    `var:qing_office_war_holder` as `scope:war_minister`, scores each general via `QING_pair_friction`
    + `QING_char_affinity`; fires `qing_war.2` (warlord danger) on high friction.
  - Officer marker `qing_officer_marker` stamped on legion commanders
    (`imp19c_effects_legion_setup.txt:166,408,456`).
  - Commander lifecycle events: `qing_office.31` (War Minister's Report, `qing_office_events.txt:844`),
    `qing_office.32` (A Commander Falls, `:904`); dispatched by `QING_council_officer_report_check`
    (`se_QING_COUNCIL.txt:1285`) + `QING_council_on_commander_death` (`:1341`).
- **Panel content:**
  - Summary bar: filled/total war seats · `qing_war_ministry_perf` statesmanship · officer-corps
    ethnic split (banner vs green-standard).
  - Minister card: the war holder.
  - Health meters: `qing_council_effectiveness` contribution, `qing_officer_corps_count`,
    `qing_officer_corps_martial` (avg), + conditional rows for active war modifiers
    (`qing_war_army_expansion`, `qing_war_officer_purge`, etc.).
  - **Subordinates / managed list:** all garrisons + their commanders. This is where #346's frontier
    garrisons + #331's OOB commanders surface. Iterate `every_unit` (or a cached variable_list of
    garrison units) → per-row show the unit, its province, its commander (portrait/name/martial/loyalty),
    and a go-to button. Consider a datamodel list (variable_list of garrison scopes) rather than fixed
    cards, since garrison count is variable.
  - Directives: `qing_action_sanction_regional_army`, `qing_action_reassert_central_command`,
    `qing_action_fund_modern_army`, drill actions (from `QING_mechanics_actions.txt`) + new #346
    directives (place/recall a frontier garrison, assign a commander).

## 4. Ministry of Works (工部) panel

**Backend exists (event-driven); there is NO existing Works GUI window — this panel is net-new UI.**

- Office: key `works`, holder var `qing_office_works_holder`, scored on **finesse**
  (`se_QING_COUNCIL.txt:162`), grants `qing_office_works_active` (`qing_governance_modifiers.txt:156`).
- Backend `se_QING_WORKS.txt` (411 lines): pulse `QING_works_pulse` (`:42`), build effects
  `QING_works_build_dike` (`:146`), `_build_canal_depot` (`:209`), `_build_wall_section` (`:265`),
  `_build_specialty` (`:361`). Buildings in `common/buildings/qing_works_buildings.txt` /
  `qing_production_buildings.txt`. Currently invoked ONLY from `qing_works_events.txt` options.
- **Panel content:**
  - Summary bar: filled/total works seats · a new `qing_works_ministry_perf` · (ethnic split optional).
  - Minister card: the works holder.
  - Health meters: canal/dike maintenance state (from `qing_works_modifiers.txt` — `qing_works_dike_maintained/shoddy`, `qing_works_canal_maintained/decay/abandoned`, `qing_works_wall_restored/shoddy/deferred`, `qing_works_graft_tolerated`), rendered as conditional rows.
  - **Subordinates / managed list:** all special buildings. Populate a variable_list of the provinces
    holding qing_* works buildings (the province-reports enumeration idiom, §7) → per-row show
    building type, province, level, condition, go-to. This is the "manage all special buildings"
    surface the user described.
  - Directives: promote the existing event-only build effects to player-initiable directives
    (commission a dike / canal depot / wall section / specialty building), gated on finesse + treasury.

## 5. Lifan Yuan Directorate (理藩院) panel — manage all Ambans

**Panel full name: "Lifan Yuan Directorate".** Backend for the office AND the Ambans already exists
(office model + feature #113 Amban lifecycle + #163 manual buttons) — the panel is a NEW CENTRAL
roster that gathers what is today only reachable per-subject from the diplomacy view.

### Office (built)
- Key `lifanyuan`, holder var `qing_office_lifanyuan_holder`, scored on **charisma**
  (`se_QING_COUNCIL.txt:164`; declared `:21`, autofill `:76`). Appoint via generic
  `QING_office_appoint = { office = lifanyuan }`; vacate branch `se_QING_COUNCIL.txt:1185`.
- Grants country modifier `qing_office_lifanyuan_active` (`qing_governance_modifiers.txt:174`:
  `subject_loyalty = 5  integrate_speed = 0.10`).
- Loc: `QING_GC_OFFICE_LIFANYUAN` / `_TT` (`qing_governance_l_english.yml:238,253`).

### Ambans (built — REAL character objects, #113 `se_QING_AMBAN.txt`)
- An Amban is a `create_character` (Manchu, vajrayana, mid stats), `set_as_minor_character`,
  `move_country = $subject$` (`se_QING_AMBAN.txt:49-67`). So the panel CAN show portrait / stats /
  loyalty / affinity per Amban.
- Markers: character modifier `qing_amban_resident` (`qing_amban_modifiers.txt:7`); char var
  `qing_amban_marker = 1`; tenure var `qing_amban_tenure_pending` (8-yr expiry).
- **Link to subject = a fixed-name var ON THE SUBJECT:** `qing_amban_here` holds the resident char
  (`se_QING_AMBAN.txt:84`). Each dependency holds ≤1 resident. `qing_amban_manual` freezes
  auto-turnover for a post (#163). **There is NO CHI-side list of all Ambans** — see build note below.
- Lifecycle effects: `QING_amban_post` (`:44`), `QING_amban_recall` (`:114`), quarterly
  `QING_amban_post_sweep` (`:155`) + `QING_amban_evaluate` (`:198`).
- Events (`qing_amban_events.txt`): `.1` clash, `.2` gone-native, `.3` able-resident, `.4` turnover.
- **Which subjects the Lifan Yuan oversees:** no named set — an inline culture-group predicate:
  subject `is_subject_of = ROOT`, ≥1 province, `current_ruler.has_culture_group = mongolic OR bodish`
  (`se_QING_AMBAN.txt:174` and duplicated in `SUB_QING_amban.txt:49`). The Lhasa/Urga/Kashgar/Ili march.

### Existing GUI (per-subject only — the gap the panel fills)
Manual Amban scripted_guis (`common/scripted_guis/SUB_QING_amban.txt`, #163):
`qing_amban_manage_post_button` / `_recall_button` / `_replace_button` / `_return_auto_button`,
wired PER-SUBJECT into `gui/diplomatic_view.gui` (button strip ~1734-1824; Overseer block 2543-2647;
action cluster 2929-2989). **There is no central roster showing all Ambans / all Inner-Asian subjects
at once.** That is exactly what this panel adds.

### Panel content
- Summary bar: filled/total Amban posts (posted vs eligible-subject count) · a new
  `qing_lifanyuan_ministry_perf` statesmanship bar · Inner-Asian ethnic balance
  (Mongol/Tibetan/Turkic vs Manchu across the residents).
- Minister card: the `qing_office_lifanyuan_holder` (charisma-scored).
- Health meters: aggregate subject loyalty/integration for the Lifan-administered subjects,
  average Amban↔Director friction, and (from #346) the War-Ministry vs Lifan-Yuan turf-friction level.
- **Subordinates / managed list = ALL AMBANS (the panel's core).** Datamodel over subjects filtered
  on `qing_amban_here.IsSet`; each row shows the resident char (`subject.Var('qing_amban_here').GetCharacter`
  — portrait/name/skills/loyalty/affinity), the subject he oversees, that posting's loyalty/integration
  state, and per-row buttons reusing the EXISTING manual verbs (`qing_amban_manage_recall/replace/
  return_auto`) — so the central panel and the diplomacy-view buttons share code.
- Directives: post a new Amban (`QING_amban_post` on an eligible unstaffed subject), launch an
  integration push, mediate a War-Ministry friction incident (#346), investiture (冊封) actions.

### Build notes (gaps flagged by the exploration)
- **Add a CHI-side `qing_amban_posts` variable_list** maintained in `QING_amban_post` / `_recall`, so
  the panel datamodel is O(list) not a full `every_subject` scan each refresh (the province-reports
  builder idiom, §7). Alternatively a GUI datamodel over `every_subject` filtered on `qing_amban_here`.
- **Extract the mongolic/bodish eligibility predicate into a shared scripted_trigger** (it is currently
  duplicated in `se_QING_AMBAN.txt:174` and `SUB_QING_amban.txt:49`) so the panel filter stays in sync.
- **The War-Ministry ↔ Lifan-Yuan friction object does NOT exist yet** (today it's only narrative loc,
  `qing_office_lifanyuan_active_desc`). #346 builds it: a garrison placed under direct War-Ministry
  command on Lifan-Yuan subject soil steps on the院's indirect-rule remit. The friction beat surfaces
  in BOTH the War panel (as a directive consequence) and this panel (as a health meter + a mediation
  directive).

---

## 6. Ministry performance → Grand Council hook (the shared spine)

There is **no per-minister persisted performance score today**. Two shared hooks exist:

1. **Council effectiveness meter** `qing_council_effectiveness` (0..100), written by
   `QING_council_recompute` (`se_QING_COUNCIL.txt:122-485`), read widely (accountability bands,
   governance capacity, decline gates, self-strengthening, and the government-view S-bar at
   `government_view.gui:2282`). Band → country modifiers `qing_council_effective` (≥66) /
   `qing_council_dysfunctional` (≤33).
2. **Accountability metric band** `qing_acc_metric` (0 fail / 1 mid / 2 thrive) per office, via
   `QING_acc_score_office = { office = <k> metric = <m> }` (`se_QING_ACCOUNTABILITY.txt:63-133`).
   War already uses `metric = military` (`QING_acc_metric_military`, `:214`); Works uses
   `metric = civilization` (`QING_acc_metric_civilization`, `:171`).

**Plan for each Ministry's performance score** (`qing_<office>_ministry_perf`, 0..100):
- Compute it in that ministry's own pulse from concrete ministry state (War: officer-corps avg
  martial + garrison coverage + friction; Works: canal/dike maintenance ratio + buildings built;
  Lifan Yuan: subject loyalty/integration avg + Amban coverage − friction).
- **Feed it back to the council** exactly as the officer-corps coupling already does
  (`se_QING_COUNCIL.txt:404-408` folds a deviation into `qing_council_eff_target`). So a
  well-run ministry raises the council meter (and the Minister's standing); a poorly-run one drags
  it down. This is the "how well or poorly the Ministry is doing directly affects the Minister's
  performance on the Grand Council" mechanic.
- Display the same var as the panel's summary-bar statesmanship bar (§2A) so the player sees it.

---

## 7. Reusable open / list idioms (proven)

- **Open a standalone window from a button** (province-reports idiom, `gui/qing_province_reports.gui:476-491`,
  `gui/government_view.gui:4236-4245`):
  ```
  datacontext = "[GetScriptedGui('<open_verb>')]"
  visible = "[ScriptedGui.IsShown( GuiScope.SetRoot( Player.MakeScope ).End )]"
  blockoverride "On_click" {
      enabled = "[ScriptedGui.IsValid( GuiScope.SetRoot( Player.MakeScope ).End )]"
      onclick = "[ScriptedGui.Execute( GuiScope.SetRoot( Player.MakeScope ).End )]"
      onclick = "[ExecuteConsoleCommand('gui.createwidget gui/<file>.gui <window_name>')]"
  }
  ```
  Close with `[ExecuteConsoleCommand('gui.ClearWidgets <window_name>')]`.
- **Datamodel list of scopes** (`gui/qing_province_reports.gui:49-81`): scrollarea → scrollwidget →
  `dynamicgridbox datamodel="[Player.MakeScope.GetList('<var_list>')]"`; the open scripted_gui does
  `clear_variable_list` then iterates and `add_to_variable_list`. This is the idiom for the War
  garrison list, the Works buildings list, and the Lifan Yuan Amban list.
- **Fixed meter** (`gui/qing_religion.gui:134`): `progressbar using=progressbar_flat_green` value
  `[FixedPointToFloat( Multiply_CFixedPoint( Player.MakeScope.GetVariable('<var>').GetValue, '(CFixedPoint)0.01' ) )]`.
- **GUI text must wrap** (standing rule): any paragraph textbox uses `multiline = yes` + a fixed
  width, never `autoresize`.

---

## 8. Build order & wiring

1. Build the three ministry-performance scores + the council feedback fold (§6) first — pure script,
   testable without GUI.
2. Build the three panels sharing a common GUI template (summary bar / minister card / health meters /
   subordinate-or-datamodel list / directives).
3. Wire open buttons (War + Lifan Yuan from the government/military views; Works from government view).
4. #346 frontier-garrison friction cross-links War ↔ Lifan Yuan panels.
5. se_LOG: every new effect wired (sys=WAR / WORKS / LIFANYUAN as appropriate). Post-build code review
   mandatory. Task-tagged comments + SESSION_REPORT entries.

**New files (anticipated):** `gui/qing_ministry_panels.gui` (or one file per panel), scripted_guis for
the open verbs + directive verbs + list builders (in `common/scripted_guis/`), the perf-score effects
(in `common/scripted_effects/`), loc in `localization/english/`.
