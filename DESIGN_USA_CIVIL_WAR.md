# Design Plan — "The House Divided": USA 1815–1861, Road to the Civil War

**Status:** proposed (design only; no code written)
**Feature id:** #93 (USA sectional arc) + #73-refactor (invert Qing USCW coupling)
**Author scope:** net-new US subsystem that OWNS the American Civil War arc and its machinery;
the existing Qing #73 reaction content is refactored to HOOK INTO this, not the other way around.

---

## 0. Guiding principle — coupling direction (per user directive)

> "Qing content should hook into existing US and Japan content, not the other way around."

**The US subsystem is the source of truth.** It owns:
- the sectional-tension state (on `c:USA`),
- the CSA release machinery (relocated out of the Qing files),
- the actual Civil War (declared/fought on the map),
- the canonical "the war has begun / the war has ended" signals.

**The Qing #73 arc becomes a pure consumer.** After this build, `qing_uscw.1` (the court's
three-way reaction) is triggered *by the US secession event*, and `QING_uscw_release_confederacy`
is deleted — the Qing never releases the CSA; it only *reacts* to a Confederacy the US arc has
already put on the map. This is a CHANGE to shipped code (#73) and gets heightened
behavioural-equivalence scrutiny (fix-traceability rule).

**AI-autonomous by construction.** The player is almost always the Qing, so the US arc must
advance and resolve with the USA under AI control. Everything decisive is pulse-driven or in
event `immediate` blocks; player options only *modulate*. No beat depends on a human choosing.

---

## 1. Historical spine (sourced digest)

Historiography: Potter, *The Impending Crisis 1848–1861* (1976); McPherson, *Battle Cry of
Freedom* (1988); Freehling, *The Road to Disunion* v.1–2 (1990/2007); Wilentz, *The Rise of
American Democracy* (2005); Varon, *Disunion!* (2008); Foner, *Free Soil, Free Labor, Free Men*
(1970). Freehling's thesis — the South was never monolithic; the *border* South's slow
radicalization is the real story — is what makes an avertable, branching chain historically honest.

| Date | Beat | Why it matters to the meter |
|---|---|---|
| 1819–20 | **Missouri crisis / Tallmadge amendment → Missouri Compromise** (Clay; 36°30′ line) | Founds the *balance rule* (admit in pairs); the arc's starting 11/11 slave–free equilibrium. |
| 1828–33 | **Nullification Crisis** (Tariff of Abominations; Calhoun's *Exposition*; Jackson's Proclamation + Force Bill) | States'-rights dress rehearsal that resolves *without* disunion — the template "Union coerces a state back" beat. |
| 1845 | **Texas annexation** | Slave republic admitted; expansion as accelerant. |
| 1846–48 | **Mexican War + Wilmot Proviso + Mexican Cession** | The hinge (Potter): expansion becomes an existential sectional referendum. |
| 1850 | **Compromise of 1850 + Fugitive Slave Act** (Clay/Douglas; Webster's 7 March speech) | CA free; the FSA radicalizes the North (Varon). |
| 1854 | **Kansas–Nebraska Act** (Douglas; repeals 36°30′) | Catastrophe beat: kills the Whigs, births the Republican Party, shatters the party system. |
| 1854–59 | **Bleeding Kansas; Sumner caning (1856)** | Sectional violence made concrete; John Brown emerges. |
| 1857 | **Dred Scott** (Taney) | Congress can't bar slavery anywhere; radicalizes the North. |
| 1858 | **Lincoln–Douglas debates; "House Divided"** | Lincoln becomes national. |
| 1859 | **John Brown / Harpers Ferry** | Point of no return; Brown a Northern martyr, Southern nightmare. |
| Nov 1860 | **Election of 1860** (four-way; Lincoln wins ~40%, zero Southern electors) | The trigger. |
| Dec 1860–Apr 1861 | **Secession Winter → CSA (Montgomery, Davis/Stephens) → Fort Sumter** | War. |

**Structural drivers to model:** slave/free state count (the balance rule); economic divergence
(King Cotton vs free-labor industrial North); abolitionism; states'-rights doctrine; the party
system's realignment (its collapse in 1854 is the political pressure valve — when it breaks,
secession follows).

**Characters** (culture `dixie`/`yankee`; add to `setup/characters/00_North America.txt` as
dated historicals like Clay/Jackson already are, and *promote* at the right beat — spawn only as
fallback): **Calhoun** (nullifier firebrand), **Clay** (existing; the compromise engine),
**Webster** (Unionist orator), **Jackson** (existing; crushed nullification), **Douglas**
(popular sovereignty), **Lincoln** (the 1860 trigger), **Jefferson Davis** (CSA president / war
instigator), **Alexander Stephens** (CSA VP), **John Brown** (abolitionist firebrand),
**Garrison**, **Sumner**.

---

## 2. Existing mod assets to reuse (verified in-repo)

- **Counter+band+pulse idiom** — `se_QING_DECLINE.txt` (`QING_DECLINE_nudge` = create-if-absent,
  add, clamp 0..100, log; band appliers remove-all-then-add-one-`duration=-1` modifier per family).
  We ship a **generic `USA_nudge` twin** (no CHI-tied log text). `sys = USA`.
- **Milestone → concrete-character spawn** — `QING_students_check_milestone` /
  `QING_students_spawn_returnee` (once-per-band guard + flooding cap). Model for firebrand spawns.
- **se_LOG** — `LOG_enter/exit/line/fail` with `sys =` tag. Every new effect wired in.
- **CSA release engine** — currently `QING_uscw_release_confederacy` (se_QING_USCW.txt:118):
  gathers `c:USA`'s non-capital `Deep_South`+`Appalachia` provinces into `uscw_csa_provinces`,
  guards `count >= 3`, `LAND_release_from_list{ … country_name = qing_uscw_csa_name … }` →
  `scope:new_country_scope`. **We RELOCATE this to US ownership** (§4.2).
- **Release + war + wargoal** — `se_SEPARATISM.txt` `SEPARATISM_spawn_breakaway`:
  `LAND_release_from_list` → `add_claim` on seceded provinces →
  `FUNC_declare_war_with_wargoal_province{ war_goal = reconquest_wargoal, target, province }`.
  This is the proven, AI-safe model for the Union's war to hold the South.
- **Civil-war primitive** — `start_civil_war = scope:<leader>` (proven at
  se_QING_JAPAN_PREPERRY.txt:214).
- **US assets at 1815** — `USA` master tag (`setup/countries/n_america/usa.txt`); territory
  subjects MIC/ILL/MSI/MSP/IND + protectorates (00_default.txt:515+); cultures `yankee`/`dixie`;
  regions `Deep_South` (SC/GA/AL/MS/AR/LA/FL), `Appalachia` (WV/KY/TN), `New_England`,
  `Great_Plains`, `American_Southwest`, `California`.
- **The phantom CSA tag** — `CSA` has only a custom-name binding (`CUSTOM_CSA`); it is NOT a
  live map tag. `c:CSA` is unsafe. The Confederacy exists ONLY as a dynamically-released country
  (`scope:new_country_scope`). This design honours that.

---

## 3. File plan (mirrors the existing suite's naming)

| New file | Contents |
|---|---|
| `common/scripted_effects/se_USA_SECTION.txt` | `USA_section_init`, `USA_nudge`, crisis effects `USA_sectional_crisis_*`, `USA_spawn_firebrand`, `USA_section_check_milestone`, `USA_flip_border_state`, `USA_secession_check`, `USA_release_confederacy` (the relocated engine), `USA_start_civil_war`, `USA_section_pulse`, `USA_section_apply_band`. `sys = USA`. |
| `events/imp19c_mod_events/usa_section_events.txt` | namespace `usa_section` — beats `.1`–`.12` (§5). Each: `immediate` decisive effect + `ai_chance`-weighted options. |
| `common/modifiers/usa_section_modifiers.txt` | band modifiers (`usa_sectional_calm/strained/crisis`), `usa_king_cotton` / `usa_free_labor` economic modifiers, `usa_fugitive_act`, `usa_bleeding` (province), `usa_secession_winter`. |
| `common/missions/usa_sectional_missions.txt` | **OPTIONAL human-USA overlay** (`potential = { tag = USA  is_ai = no }`) — "Preserve the Union" vs "Southern Rights". Not required for AI drift. |
| `common/on_action/usa_section_on_actions.txt` | `on_game_initialized` seeds (`USA_section_init` for USA + dated one-shots, NO `is_ai` gate); registers `usa_sectional_pulse_on_action`. |
| `localization/english/usa_section_l_english.yml` | all loc; **reuses** `qing_uscw_csa_name`/`_adj` for the released CSA (single canonical CSA name across both arcs). |
| **CHANGE** `00_monthly_country.txt` | add `usa_sectional_pulse_on_action` to the `monthly_country_pulse.on_actions` list. |

---

## 4. Mechanics

### 4.1 Meters (0..100, on `c:USA`) — the AI/summary layer

| Var | Meaning | Init | Concrete object hung off its bands |
|---|---|---|---|
| `usa_sectional_tension` | master road-to-disunion meter | 20 | bands → economic modifiers; thresholds → firebrand spawns, border-state flips, secession |
| `usa_slave_states` / `usa_free_states` | the balance rule (legible count) | 11 / 11 | free pulls ahead + high tension → Southern secession trigger |
| `usa_abolitionism` | Northern antislavery opinion | 15 | high → spawn Garrison/Sumner/Brown; feeds tension |
| `usa_states_rights` | Southern nullification/secession doctrine | 20 | high → spawn Calhoun/Davis; gates nullification & secession |
| `usa_party_system` | health of the 2nd Party System (100 = intact) | 80 | Kansas–Nebraska crashes it; **< 30 = safety valve gone → secession enabled** |

**Additive concreteness (STANDING RULE 1):** meters are the summary/AI layer; every threshold
hangs a real on-map object:
- tension ≥ 45 → **spawn a firebrand** (once-per-band guard, flooding cap ~4), Southern at
  `states_rights` bands / Northern at `abolitionism` bands; **promote existing setup chars**
  (Clay, Jackson, and the dated historicals) rather than duplicate.
- tension ≥ 60 → **flip a border-state province** in `Appalachia`/`Great_Plains` to `usa_bleeding`
  unrest ("Bleeding Kansas" as a real map object).
- tension ≥ 80 ∧ `usa_party_system` < 30 ∧ `usa_free_states > usa_slave_states` → **secession
  climax** (§4.2).

### 4.2 The secession climax — US-owned CSA release + a real war

**Relocate the CSA release to US ownership.** Extract the body of the current
`QING_uscw_release_confederacy` into a new **`USA_release_confederacy`** in `se_USA_SECTION.txt`,
releaser rebound to `c:USA`, `sys = USA`. Same `Deep_South`+`Appalachia` gather, same `count >= 3`
guard, same `LAND_release_from_list{ country_name = qing_uscw_csa_name … }` → `scope:new_country_scope`.

**`USA_secession_check`** (called every pulse — the autonomous trigger):
```
if tension≥80 AND usa_party_system<30 AND usa_free_states>usa_slave_states AND NOT has_variable=usa_seceded:
    set_variable usa_seceded
    USA_release_confederacy = yes          # CSA appears on the map (scope:new_country_scope)
    USA_start_civil_war    = yes           # the Union fights to hold the South
    # fire the US-side "war has begun" event; the Qing arc listens for this (§6)
    trigger_event = { id = usa_section.12 ... }
```

**`USA_start_civil_war`** — the war made real, proven verbs only. **Baseline = the SEPARATISM
reconquest path** (proven AND the AI prosecutes it autonomously): after the release,
`add_claim` the seceded provinces for `c:USA`, then `FUNC_declare_war_with_wargoal_province{
war_goal = reconquest_wargoal, target = scope:new_country_scope, province = <csa_capital> }`.
`start_civil_war = scope:<Davis>` is the truer-flavour alternative, held for an oracle-check on
whether it composes with a just-released country (§7).

### 4.3 AI-autonomy — how each mechanism advances with an AI USA

| Mechanism | Advances under AI USA via | Risk |
|---|---|---|
| Meter drift | `USA_section_pulse` runs monthly for `tag = USA` with **NO `is_ai` gate** | none |
| Beats .1–.11 | decisive effect in `immediate`; options carry `ai_chance` favouring the historical default; dated one-shots re-check their own date guard | .9 (Lincoln–Douglas) is pure flavour — acceptable, no gating role |
| Firebrand spawns / border flips | pulse-driven off meter bands, not events | none |
| Secession climax .12 | `USA_secession_check` in the pulse fires release + war with no option | **R1** verify below |

**Design risk R1:** confirm the reconquest-war path resolves for an AI USA vs. a freshly-released
AI CSA (SEPARATISM uses it, but verify with an AI-only USA). **R2:** the `usa_seceded` guard plus
the release's `count>=3` / `exists new_country_scope` guards must make the release idempotent so
the CSA can never be released twice (see §6 — the Qing arc must NOT also release it).

---

## 5. Beat list (date-anchored)

Dated one-shots are seeded in `on_game_initialized` with `days=` offsets from the 1815.7.1 start,
each re-checking its own `current_date` guard (the proven `qing_embassy.2` idiom, minus the
`is_ai=no` wrapper). "AI advance" states how it progresses with no human.

| # | Beat / date | Trigger | Player options (overlay) | Concrete effect | Meter nudge | AI advance |
|---|---|---|---|---|---|---|
| .1 | Missouri, ~1820 | dated | balance / restrict / spread | admit MO slave + ME free; flag Clay "compromiser" | tension +8; → 12/12 | immediate pairs them; `ai_chance` Balance 10/Restrict 2/Spread 2 |
| .2 | Nullification, ~1832 | dated; `states_rights≥25` | Force Bill / compromise tariff / concede | spawn Calhoun; Jackson coerces; **resolves w/o disunion** | states_rights +12, tension +6 then −4 | immediate coerces SC back; `ai_chance` Force 8/Compromise 6/Concede 1 |
| .3 | Texas, ~1845 | dated | annex / decline | Texas → slave state | slave +1, tension +6 | immediate annexes; Annex 10/Decline 1 |
| .4 | Mexican War + Wilmot, ~1846 | dated | free-soil / pop-sov / extend line | Mexican Cession added; the Proviso fight | tension **+12**, abolitionism +5 | immediate grants Cession; Pop-sov 8/Proviso 4/Extend 3 |
| .5 | Compromise of 1850 + FSA | dated | pass omnibus / reject | CA free (+1); `usa_fugitive_act` raises abolitionism | free +1, tension +6, abolitionism +8 | immediate passes; Pass 9/Reject 2 |
| .6 | **Kansas–Nebraska, 1854 (hinge)** | dated | pass / preserve line | repeal 36°30′; **crash party_system −40**; birth Republicans | tension +15, party −40, abolitionism +8 | immediate repeals+crashes; Pass 8/Preserve 3 |
| .7 | Bleeding Kansas + Sumner, 1856 | pulse `tension≥60` OR dated | troops / let it burn | flip Great_Plains province `usa_bleeding`; spawn John Brown | tension +10, abolitionism +6 | pulse auto-spawns+flips |
| .8 | Dred Scott, 1857 | dated | (reaction) | Taney modifier; **spawn Lincoln** if absent | tension +8, abolitionism +8, states_rights +6 | immediate; no gate |
| .9 | Lincoln–Douglas, 1858 | dated; Lincoln alive | escalate / accommodate | prestige to Lincoln; `usa_lincoln_rising` | tension +5 | immediate; overlay only |
| .10 | Harpers Ferry, 1859 | dated; Brown alive | execute / pardon | Brown executed → martyr; point of no return | tension **+15**, abolitionism +10, states_rights +8 | immediate executes; Execute 10/Pardon 1 |
| .11 | Election of 1860 | dated Nov 1860; `party_system<40` | Lincoln wins / accommodation | Lincoln → president char; `usa_lincoln_elected` | tension +12 | immediate elects Lincoln (ai_chance heavily weighted) |
| .12 | **Secession Winter → CSA + Fort Sumter** | **pulse `USA_secession_check`** OR dated Apr 1861 fallback | coerce (war) / let them go | **§4.2: release CSA + start the war**; emit the "war begun" signal | `usa_secession_winter` | **pulse fires it with no human**; Coerce 10/Let-go 1 |

---

## 6. Refactor of the Qing #73 arc (invert the coupling)

**Today:** `qing_uscw.1` is triggered from the CHI-only decline flavour roll
(`se_QING_DECLINE.txt:959`), and if the Qing player picks "back the Confederacy",
`QING_uscw_back_confederacy` calls `QING_uscw_release_confederacy`. So the Civil War *only exists
if a human Qing conjures it*, and no war is ever fought.

**After this build (the inversion):**
1. **Delete** `QING_uscw_release_confederacy` and its call in `QING_uscw_back_confederacy`. The
   Qing no longer releases the CSA — the US arc already put it on the map.
2. **Delete** the `trigger_event = { id = qing_uscw.1 }` branch from the decline flavour roll
   (`se_QING_DECLINE.txt:947–959`). The Qing reaction is no longer self-conjured on a date.
3. **Trigger `qing_uscw.1` FROM the US arc.** In `usa_section.12`'s `immediate` (or a tiny
   `after`), add: *if a human Qing exists*, `c:CHI = { trigger_event = { id = qing_uscw.1 } }`.
   Gate `if = { limit = { c:CHI = { is_ai = no } } }` so the reaction only bothers a human Qing.
   `qing_uscw.1`'s own `is_triggered_only`/date guards stay as a safety net.
4. **Qing options become pure diplomacy/economy reactions** (recognize the CSA, profit as a
   neutral, back the Union) — they add opinions/wealth/modifiers toward the *already-released*
   `scope:new_country_scope`, and never touch the map's territory. Pass the CSA scope from the
   US event into the Qing event (saved scope or re-resolve the seceded country).

**Scrutiny (fix-traceability rule — CHANGE to shipped #73):** the behavioural change is
intended and large — the Civil War now happens on the historical drift regardless of the player,
where before it required a human Qing to back the CSA. Document in SESSION_REPORT that (a) the CSA
name/adj are unchanged (`qing_uscw_csa_name`), so a Qing-side observer sees the identical country;
(b) the Qing outcome modifiers (`qing_uscw_union_amity` etc.) are unchanged; (c) the only removed
capability is the Qing's power to *manufacture* the war, which is now owned by the US arc.

---

## 7. Unproven engine capabilities — oracle-check before build (Terra-Indomita + Invictus)

1. `reconquest_wargoal` / `FUNC_declare_war_with_wargoal_province` with an **AI attacker (USA)**
   vs. a freshly-released **AI CSA** — does the AI USA declare and prosecute it? (R1.)
2. `LAND_release_from_list` from an **AI-controlled `c:USA`** (proven only from human-CHI direction).
3. `create_character` placing a firebrand at an **AI-controlled** `c:USA` court.
4. Dated one-shot `trigger_event{days=}` seeded in `on_game_initialized` firing for an **AI**
   country (the Qing seeds all gate `is_ai=no`; the AI context is the untested variable).
5. `start_civil_war` composing with a country that just had land removed via
   `LAND_release_from_list` (only relevant if we choose the civil-war alt over reconquest).
6. Cross-event scope hand-off: passing `scope:new_country_scope` from `usa_section.12` into
   `qing_uscw.1` (saved-scope lifetime across a `trigger_event` to a different country).

---

## 8. Open questions / scope decisions

1. **War model:** reconquest-wargoal (proven, AI-safe, recommended baseline) vs. `start_civil_war`
   (truer flavour, unproven composition, held as oracle-gated upgrade). **Recommend reconquest.**
2. **Free/slave states as real tags?** Recommend keep the counter as summary + flip real
   provinces + the CSA release as the one big real-tag object (not per-state admission tags).
3. **Character sourcing:** add Calhoun/Douglas/Lincoln/Davis/Brown/Garrison/Sumner/Stephens to
   `setup/characters/00_North America.txt` as dated historicals and *promote* them (recommended),
   spawn only as fallback.
4. **Overlay mission tree** (`usa_sectional_missions.txt`, human-USA only): build now or defer?
   The AI arc is complete without it. **Recommend defer to a follow-up.**
5. **Timing coupling to the Qing arc:** confirm we want `usa_section.12` to trigger `qing_uscw.1`
   (the recommended inversion) rather than leaving the Qing arc's date-window fallback as primary.
6. **Border-state granularity:** province-flip in `Great_Plains`/`Appalachia` enough for
   "Bleeding Kansas", or a dedicated Kansas-area target?

---

## 9. Build order

1. Oracle-check §7 items 1–4 (the AI-autonomy load-bearers) FIRST.
2. Add the dated historical characters to setup.
3. `se_USA_SECTION.txt` (meters, pulse, bands, firebrand/border concreteness) + on_action + modifiers + loc.
4. Relocate the CSA release engine into `USA_release_confederacy`; wire `USA_start_civil_war`.
5. Beats `.1`–`.12` events.
6. **Then** refactor #73 (§6) — delete the Qing release + self-trigger, wire the US→Qing hook.
7. se_LOG audit of every new effect; SESSION_REPORT entries (#93 + #73-refactor).
