# Overnight Decisions — Session 3 (develop branch)

Running log of major design/engineering decisions taken during the overnight autonomous
run on the **develop** branch. Major decisions taken on the **1763_bookmark** branch are
logged in that branch's own doc (see the 1763 section at the end for the pointer), NOT here.

Author/committer for all commits: **freekumquats**. develop = testing candidate; promote
to master only after in-game verification and only when asked.

Work queue for this run (in order — as directed by the user across several messages):
1. **#272 + #273** — Grand Council: Empress throne seat + 2 new appointable offices
   (Central Secretariat 內閣大學士 + Imperial Guard 領侍衛內大臣) + Chamberlain rename.
   → code review → commit + push develop.
2. **#165** — Four-power dynamic sphere-of-influence system.
3. **Religion rework** — traditional Chinese Confucian/Taoist/Buddhist/Shenist folk
   religion vs. arriving Christian missionaries → religious tension/conflict.
4. **Marriage diplomacy** (DESIGN_MARRIAGE_DIPLOMACY.md follow-up).
5. Deep adversarial review of #165 + religion + marriage → commit + push develop.
6. Switch to **1763_bookmark**, implement Phase 2/3/etc (major 1763 decisions logged in
   the 1763 branch's own doc, NOT here).
7. On 1763: populate ALL countries with 1763-appropriate buildings/trade-goods/industry/
   production (fire off deep native-language historical-research agents as needed).
8. When develop + 1763 are both exhausted: new branch **trade_goods** — add New World
   crops to the required basket of 6 essentials + add rifles/porcelain/etc to manufactured
   goods (RISKY: ties into many core systems). Document in a NEW `new_trade_goods` doc;
   refer to SESSION_REPORT for why risky trade changes were previously deferred.

**Cross-cutting standing instruction:** log every major decision as I go — develop decisions
here in overnight_decisions3.md; 1763 decisions in the 1763 doc; trade_goods decisions in
new_trade_goods.md.

---

## 1. Grand Council #272 + #273 (Empress seat + 2 offices + Chamberlain rename)

**Status:** script + appoint-verb + all localization complete; GUI + SESSION_REPORT +
code review pending before the single combined develop commit.

### #272 — Empress throne seat + figurehead
- **Scope link:** `current_ruler.spouse` (PROVEN — `exists = spouse` at 00_ambitions.txt:1230).
  Empress is display + figurehead only (`QING_council_score_figurehead` weight 1); she NEVER
  enters any appointable-office loop.
- **Seat storage:** `qing_office_empress_holder` country var, refreshed each quarter by
  `QING_seat_refresh_empress` (added to `QING_seat_refresh_all` after crownprince; mirrors
  `current_ruler.spouse` when alive, else clears the var).
- **Gate trigger:** `QING_dynasty_has_empress` added to `qing_dynasty_triggers.txt` (a
  scripted_TRIGGERS file, per the #157/#165 lesson that limit-position conditions must NOT
  live in scripted_effects or the guard collapses at load → boot crash).

### #272 — Empress dynastic events (qing_dynasty.6/.7/.8)
- **.6 Empress Intercedes** (POSITIVE): heed-her (harmony +6, prestige) vs keep-to-palace
  (emperor prestige +15, harmony -5).
- **.7 Consort Clan 外戚** (NEGATIVE): curb-clan (harmony +2, corruption eased, empress
  loyalty -8) vs indulge-clan (empress loyalty +12, corruption up, harmony -4).
- **.8 Two Suns in the Inner Palace** (empress-vs-dowager, NEGATIVE): side-with-dowager
  vs back-the-empress. Gated on BOTH `QING_dynasty_has_empress` AND `_has_dowager`.
- All three: `is_triggered_only`, tag=CHI + empress gate, saved scopes `scope:empress`
  (+`scope:dowager` for .8), fired from `QING_dynasty_flavour_roll` weighted random_list.
- **#253 rule honoured:** every new `LOG_line` msg is STATIC text only ("EVENT qing_dynasty.6
  (empress intercedes)") — no bracketed `[data-functions]`, which `debug_log` cannot resolve
  and which flood error.log. Bracketed `[scope:X.GetName]` is used ONLY in loc desc strings
  (valid there — the loc renderer resolves them; only debug_log does not).

### #273 — two new appointable offices (council 11 → 13)
- **Central Secretariat — 內閣大學士 Grand Secretary** (key=`grand_secretariat`, skill=charisma):
  drafts edicts/rescripts, generates political influence. Office modifier =
  `monthly_political_influence_modifier`.
- **Imperial Guard — 領侍衛內大臣 Grand Commandant** (key=`guard_commandant`, skill=martial):
  commands the palace guard, guards the emperor's PERSON. Buff = Guard vitality; power-base
  reconciled onto the emperor in `QING_council_recompute`.
- **Chamberlain rename:** Household Grand Secretary → **Grand Chamberlain of the Imperial
  Household** (內務府, key renamed `grand_secretary` → `chamberlain`). BEHAVIOURAL-CHANGE:
  existing office renamed, not new — flagged for behavioural-equivalence scrutiny in review.
- **Office events:** `qing_secretariat.1/.2/.3` (Edict Mill / Rescript Backlog / Drafting
  Scandal) + `qing_guard.1/.2/.3` (Guard Reviewed / Plot Against Throne / Overmighty
  Commandant — the praetorian/Oboi problem). Each gated on its office being filled by a
  living holder in ROOT's service; fired from `QING_frontier_flavour_roll` (se_QING_DECLINE).
- **Appoint verbs:** `qing_gov_office_appoint_grand_secretariat` + `_guard_commandant`
  (scope=character, CHI+employer shown, cost 15 political influence, calls `QING_office_appoint`).
- **Accountability:** grand_secretariat OWNS the influence metric (`QING_acc_metric_influence`:
  PI<20 fail / ≥80 thrive); guard_commandant OWNS the civil-war metric
  (`QING_acc_metric_civil_war`: civil war or disloyal-powerful char = fail).
- **Displaced/vacated-holder cleanup:** censorate-oversight (minor+major) buff strips added at
  BOTH appoint-displacement (~910) and vacate (~971) cleanup sites in se_QING_COUNCIL.txt, so a
  relieved officer leaves clean.

### Localization
- `qing_governance_l_english.yml`: chamberlain rename, 2 new office name/desc pairs, card
  titles, MOD one-liners, appoint-button + tooltip loc; Empress seat loc (QING_GC_EMPRESS +
  _VACANT); "eleven appointable" → "thirteen" in SEATS_TT + TITLES_UNASSIGNED_TT.
- `qing_dynasty_l_english.yml`: appended qing_dynasty.6/.7/.8 (title/desc/2×option+tt).
- NEW `qing_secretariat_l_english.yml` + `qing_guard_l_english.yml`: full loc for the 6 office
  events (BOM + `l_english:` header, matching house style).

### GUI (DONE)
- **`government_view.gui`:**
  - Chamberlain card: fixed stale loc keys (`QING_GC_OFFICE_GRAND_SECRETARY` →
    `_CHAMBERLAIN`, `QING_GC_MOD_GRAND_SECRETARY` → `_CHAMBERLAIN`) left over from the rename.
  - Office grid 10 → 12: added `grand_secretariat` (oratory icon, GetCharisma, refresh_charisma)
    and `guard_commandant` (military icon, GetMartial, refresh_martial) cards to OFFICES row 3,
    templated exactly from the zongli card so alignment/statesmanship-bar/appoint idiom match.
  - **Throne row** (was Emperor | Crown Prince | Regent): Regent box REPLACED by an **Empress**
    box (templated from the Crown Prince box incl. the #270 favour square; datacontext
    `qing_office_empress_holder`, loc QING_GC_EMPRESS/_VACANT). Throne row is now
    Emperor | Crown Prince | Empress.
  - **Regent + Emeritus relocated** into a right-hand vertical column beside the Grand
    Chancellor card (horizontal wrapper: Chancellor card | {Regent, Emeritus}). Regent box
    widened 312→470 to fill the column. Emeritus block moved up out of its old
    below-the-grid position (its IsSet visibility gate preserved, so it still only shows when
    a 太上皇 exists). This declutters the throne row and groups the "power behind the throne"
    seats with the Chancellor.
- **`imp19c_windows.gui`:** added the two per-office Appoint buttons (grand_secretariat,
  guard_commandant) to the shared picker window, keyed on `qing_gc_picker_office`, templated
  from the zongli button; tooltips QING_GOV_OFFICE_GRAND_SECRETARIAT_BTN_TT /
  _GUARD_COMMANDANT_BTN_TT (both confirmed present in loc).
- Both GUI files brace-balanced (delta 0) after edits.

### Still pending for #272/#273
- SESSION_REPORT.md entries (fix-traceability; behavioural-CHANGE note for the Chamberlain
  rename + reworked War/Censorate office modifiers).
- Post-implementation code review, then ONE combined develop commit as freekumquats.

**Status update:** #272/#273 code review DONE (workflow wf_f4b3dc43) — 2 CONFIRMED findings,
both FIXED (HIGH accountability-dispatch gap for the two new offices; MEDIUM stale tooltip
key). Committed + pushed develop as freekumquats (7a67d063).

---

## 2. #165 — Four-power dynamic sphere-of-influence

**Status:** built (script + on_action wiring + GUI tally + loc). Brace-balanced, BOM
preserved on all touched files. Pending: adversarial review, then folded into the combined
#165+religion+marriage develop commit (queue item 5).

### The model — PROVEN "PUSH", numeric dominant codes
The 19th-century Great Game modelled as a running contest for the states of the Qing's
contested MARCHES. Four powers (China/CHI, Britain/GBR, France/FRA, Russia/RUS) each hold a
0..100 influence score on every contested state; a dominant holder is the 4-way max.

- **PUSH not PULL.** Each power PUSHES a score onto states it can reach via PROVEN property
  reads (ownership, `is_subject_of`, `is_in_region` through the sphere classifiers,
  `every_neighbor_province`). The oracle-flagged PULL model — reading a *neighbour's* numeric
  influence var to pull toward it — is UNPROVEN in this engine, so it is NOT used. This is the
  documented safe fallback (memory `imp19c-sphere-idioms-oracle`).
- **Numeric dominant codes, not flags.** Dominant holder stored as `qing_sphere_dominant`
  (+`_prev`) = 0 neutral | 1 china | 2 britain | 3 france | 4 russia. Flag-var-to-flag-var
  equality (`var:X = var:Y` where both hold flags) has ZERO codebase precedent → avoided.
  Numeric equality is proven everywhere. Flip detection = numeric `NOT = { dominant = _prev }`.
- **4-way max, fixed-name vars.** `QING_sphere_recompute_dominant` uses `set_local_variable
  top_val` and three strictly-greater comparisons — no dynamic `ordered_in_list` deref (also
  unproven for this use). Ties break China>Britain>France>Russia (home-field: only a STRICTLY
  greater rival displaces the incumbent). Contest floor 20 → below it the march reads neutral.

### Mechanics
- **Ring** (`QING_sphere_build_ring`, rebuilt each pulse): every land state just outside the
  empire (a non-CHI-owned, populated land neighbour of a CHI province) PLUS every populated
  state a Qing subject holds (the tributary marches are China's own contested sphere).
  Dedup via `is_target_in_variable_list`. State influence vars live ON the state, so rebuilding
  the LIST never discards accumulated balance.
- **Seed** (`QING_sphere_seed_state`, 1815): China 60 on own/subject soil else 25; the theatre
  European power gets a head start (Britain 45 / France 40 / Russia 45) via the province-scope
  `QING_gp_sphere_is_*` classifiers (non-overlapping by invariant).
- **Yearly pulse** (`QING_sphere_pulse`, CHI player-only, self-throttled 365d): all scores
  decay −3; China pushes +11 (own/subject) or +7 (CHI-owned neighbour province); the theatre
  power pushes ramped by date (+3 early / +7 after soft / +12 after hard, mirroring the
  existing GP grip-grace windows — GBR soft 1826 hard 1852; FRA/RUS soft 1858 hard 1885).
  Recompute dominant; tally per-power counts for the GUI.
- **GP tie-in** (`QING_sphere_flip_reaction`): China LOSING a march to a European rival nudges
  that rival's existing `qing_gp_tension_<power>` +3 (a provocation); China WINNING one back
  eases it −2. Reuses proven `QING_DECLINE_nudge` + `qing_gp_tension_*` (se_QING_DIPLO.txt).
  China↔neutral and rival↔rival shifts are ignored (no direct Sino-foreign provocation).

### Wiring / surface
- Seeded once by `QING_sphere_init` in `qing_mechanics_on_actions.txt`
  (`imp19c_qing_on_game_initialized`, LIST form per #254); evolved by `QING_sphere_pulse` in
  `00_monthly_country.txt` (`qing_mechanics_pulse_on_action`, tag=CHI + is_ai=no).
- GUI: a `QING_SPHERE_INLINE_TALLY` textbox in the Great Game inline strip of
  `diplomatic_view.gui` (CHI + target GBR/FRA/RUS gate). Loc resolves the four `|0`-guarded
  counters via `Player.MakeScope.GetVariable(...).GetValue|0` (proven pattern; e.g.
  economic_enchancement_l_english.yml). Reads 0 until the first yearly pulse — informational.
- **#253 honoured:** every new `LOG_line`/`LOG_enter`/`LOG_exit` msg is STATIC text; bracketed
  data-functions appear ONLY in the loc .yml strings (valid there — loc renderer resolves them).
- New file `se_QING_SPHERE.txt` (all sys=QING logging). No behavioural CHANGE to existing
  features — purely additive; reuses `QING_DECLINE_nudge`/`qing_gp_tension_*`/`QING_gp_sphere_is_*`.

### #165 adversarial review (workflow wf_951d19ad) — 1 CONFIRMED finding, FIXED
- **MEDIUM degenerate-balance (CONFIRMED):** China's frontier push (+7) beat the yearly
  decay (−3), so `china_influence` climbed monotonically to the 100 clamp on EVERY contested
  march; the China-first tie-break then held all marches for China forever, collapsing the
  four-power contest and making the European historical ramp irrelevant. **FIX:** added a
  FRONTIER CAP in `QING_sphere_tick_state` — a `local_var:is_home` flag distinguishes China's
  own/subject soil (uncapped, +11 net holds) from a mere frontier march, where `china_influence`
  is now capped at 55 after the clamp. 55 leads early (rivals seed 40–45) but sits below the 100
  a fully-entrenched European power reaches after its hard date, so the ramp genuinely flips its
  sphere mid-century. Idiom `set_local_variable`/`local_var` already proven in this same file.

---

## 3. #275 — Religion rework (traditional Chinese faiths vs Christian missionaries)

**Status:** built (concrete province/pop conversion layer + modifiers + loc + wiring),
brace-balanced, BOM preserved. Pending: adversarial review, then folded into the combined
develop commit (queue item 5).

### What already existed (built on, not duplicated)
- **Religions:** `confucianism`, `daoism`, `mahayana`/`pure_land_buddhism`/`vajrayana`,
  `chinese_shamanism` (Wuism/Shenist folk), `nuoism` + the Christian denominations
  (`catholic`, `evangelical`, `anglican`, `orthodox`, `sino_catholic`, `syncretic_christian`)
  are all defined in `common/religions/00_vthreereligions.txt`.
- **Religion-group triggers:** `common/scripted_triggers/00_religion_groups.txt` already has a
  rich pop/province/country taxonomy — `christian_group_trigger_pop`,
  `chinese_traditional_religion_trigger_pop` (daoism/chinese_shamanism/nuoism/confucianism),
  `chinese_accepted_religion_trigger_pop`, `buddhist_group_trigger_pop`, etc.
- **National meter + Boxer escalation:** `se_QING_MISSIONARY.txt` already runs the COUNTRY-level
  `qing_antichristian_sentiment` 0..100 meter, the 教案-incident event (suppress/indulge), the
  fever/simmering bands, the fever-pitch agitator spawn, and the boil-over into the Boxer rising
  (`qing_rebellion.9`). This was the SUMMARY/drama layer — the missing piece was the concrete
  on-the-ground half.

### The rework — the CONCRETE missionary-station layer (concrete-over-abstract rule)
New file `se_QING_MISSIONARY_STATIONS.txt` puts REAL missions on the map and converts REAL pops:
- **`qing_mission_station`** — a province modifier (a real mission), founded at the treaty-port
  provinces (the existing `qing_treaty_port` province modifier stamped by se_QING_TREATIES.txt)
  and spreading INLAND to neighbouring Qing provinces (`random_neighbor_province`, gradual).
  Carries province var `qing_mission_faith` (flag) = its denomination.
- **Denomination mix** (`random_list`, historical): 55% Catholic (French protectorate, the
  largest presence), 35% evangelical (Anglo-American Protestant societies), 10% Orthodox (the
  small Beijing ecclesiastical mission).
- **Conversion** (`QING_mission_convert_pops`, yearly per station): converts up to two eligible
  non-Christian, non-slave/noble pops to the station's faith via `set_pop_religion`
  (ORACLE-VERIFIED effect — Invictus 00_india_effects.txt:835, TI 00_christianity.txt:306;
  NOT used in-mod before, so oracle-gated per the standing rule). PREFERS a
  `chinese_traditional_religion_trigger_pop` (Confucian/Daoist/Buddhist/Shenist) — the resented
  harvest that bred the real 教案 grievance — raising local tension +8; a merely-non-Christian
  pop raises it +4.
- **Local conflict:** province var `qing_prov_missionary_tension` 0..100 (decays −3/yr, so a
  quiet/fully-converted field cools; an actively-worked one climbs). At ≥50 it stamps
  `qing_mission_unrest` (province modifier, local_unrest +3) — 地方教案 anti-Christian disorder.
- **Loop back to the national meter:** `qing_missionary_reach` (live station count, recomputed
  each pulse) is fed ADDITIVELY into `qing_antichr_target` in the existing `QING_missionary_pulse`
  — more missions on the ground → higher national anti-Christian sentiment → the existing
  fever/agitator/Boxer escalation. So the concrete layer DRIVES the summary layer that was
  previously fed only by treaty-burden + sect-pressure.
- **Gating:** the whole station pulse is dormant until `qing_treaty_system_imposed` (the interior
  was closed to missions before the 1858/60 Tianjin treaties — the Canton system banned inland
  proselytising), self-throttled ~yearly. Runs off the governance pulse (step 11b, after the
  existing `QING_missionary_pulse` step 11) in se_QING_GOVERNANCE.txt.

### Files
- NEW `common/scripted_effects/se_QING_MISSIONARY_STATIONS.txt`.
- NEW `common/modifiers/qing_missionary_station_modifiers.txt` (qing_mission_station +
  qing_mission_unrest; all keys verified province-scope-valid).
- EDIT `se_QING_MISSIONARY.txt` — reach fed into the national sentiment target.
- EDIT `se_QING_GOVERNANCE.txt` — station pulse added to the governance pulse (step 11b).
- EDIT `localization/english/qing_missionary_l_english.yml` — the two new modifier name/desc pairs.
- **#253 honoured** (all LOG msgs static); no bracketed data-functions in logs. No behavioural
  CHANGE to existing features — purely additive; the reach-add is a no-op (0) until treaties open.

## 4. #276 — Dynastic marriage diplomacy

### Scope (DESIGN_MARRIAGE_DIPLOMACY.md §6, conservative default)
- A **Western-monarchy AI feature**, driven AI-autonomously exactly like the USA #93 /
  Japan #94 / Mexico #96 arcs (self-gates on a trigger, NOT on `is_ai`, so a player running
  such a realm gets it too). The **Qing are excluded** (CHI integrate their subjects; they are
  not inherited) — a foreign-princess Empress for CHI is left to the separate Empress-seat flavour.
- Gate: `MARRIAGE_eligible_realm_trigger` = `basic_western_group_country_trigger` +
  `narrow_monarchy_trigger` + `is_subject = no` + has ruler + holds land, minus CHI/BAR.
- Built **L1 pact + L2 union + L3 inheritance**. **L4 GUI deliberately NOT built** — this is an
  AI-autonomous background system; no player panel is needed for the conservative scope.

### Oracle gate — all 4 §3 hooks cleared (Terra-Indomita + Invictus, feasibility only)
- **[U-3] cross-court `marry_character`** — PROVEN: `c:TAG = { <child iterator> = { save_scope_as = X } }`
  then `char = { marry_character = scope:X }` (Invictus me_bithynia.txt:173-229). `ordered_child`
  (order_by=age, max=1) is the standard child iterator; engine requires an OPPOSITE-SEX pair.
- **[U-2] royal_union from a marriage** — PROVEN verb `FUNC_make_subject { type = royal_union }`
  (se_FUNC.txt:412). The *logic* (junior house = the heirless one) is ours.
- **[U-1] auto-inheritance on shared-ruler death** — engine auto-merge is UNPROVEN, so NOT
  relied on. Modelled ourselves on `on_character_death` (`is_ruler = yes`), transferring the junior
  realm's land with the PROVEN `LAND_transfer_provinces` idiom (se_LAND.txt:348 — the only
  sanctioned land-transfer path; re-homes governorship vars). `annex_country` is ABSENT from both
  oracles + the mod, so NOT used.
- **[U-4] AI willingness / diplomatic-action payload** — UNPROVEN, so NOT used. An AI-autonomous
  PULSE drives it (the proven arc idiom).

### The model — 3 layers
- **L1 pact (`MARRIAGE_pulse` → `MARRIAGE_form_pact`):** a Western monarchy, capped at 3 standing
  bonds, whose ruler still has a marriageable child, picks ONE eligible foreign realm (bounded
  `random_country`, not already wedded, in diplomatic range, partner ruler also has a marriageable
  child) and weds a MALE child of our house to a FEMALE child of theirs. Records the bond both ways
  via the PROVEN `variable_list` idiom (`marriage_partners` + `marriage_bond_count`), applies
  `royal_marriage_opmod` goodwill both ways, and — for a peace-time non-allied pair — an
  `add_alliance` (the Coburg pattern).
- **L2 union (`MARRIAGE_check_unions`):** for a realm we are wedded to whose junior house is now
  heirless (ruler has no living child), bind it as a `royal_union` and mark `marriage_union_junior`
  so L3 fires only on our own marriage-made unions, never pre-existing ones.
- **L3 inheritance (`MARRIAGE_on_ruler_death_union`, from `on_character_death`):** when a
  marriage-made royal_union junior's ruler dies with no living heir, the overlord inherits — the
  junior's land is collected into a named list (`every_owned_province`+`add_to_list`) and handed
  over with `LAND_transfer_provinces`. The defunct bond is then pruned from the overlord's
  `marriage_partners` list + counter so a dead realm never lingers as a partner or blocks a slot.

### Correctness refinements applied during build
- **Opposite-sex marriage gate** (engine requirement): bride = eldest eligible `is_female` child of
  partner ruler; groom = eldest eligible `is_male` child of own ruler, `NOT = { this = bride }`.
- **Defunct-bond pruning** on inheritance (above) — prevents a dead realm from occupying a bond slot.
- Rejected 4 UNPROVEN idioms in the first draft (caught by self-verification per the oracle rule):
  `married_to_this@this` dynamic-var suffix → `variable_list`; `random_child` → `ordered_child`;
  `is_ally_with` → `alliance_with`; `annex_country` → `LAND_transfer_provinces`.

### Cadence / cost
- `MARRIAGE_pulse` from `yearly_country_pulse`, self-throttled ~5 years (`marriage_pulse_cooldown
  days = 1825`), ONE partner attempt per pulse (a bounded `random_country` pick, not an O(n^2) scan)
  → O(1) amortised even across many monarchies.

### Files
- NEW `common/scripted_effects/se_MARRIAGE.txt` — the full suite (init/pulse/form_pact/check_unions/
  on_ruler_death_union).
- NEW `common/scripted_triggers/00_marriage_triggers.txt` — `MARRIAGE_eligible_realm_trigger` +
  `MARRIAGE_has_marriageable_child_trigger` (guard fragments in scripted_TRIGGERS per the
  #157/#165 boot-crash lesson, NOT scripted_effects).
- NEW `common/on_action/marriage_on_actions.txt` — the AI-autonomous pulse registration.
- EDIT `common/on_action/00_yearly_country.txt` — pulse added to `yearly_country_pulse` list.
- EDIT `common/on_action/00_specific_from_code.txt` — L3 death hook into `on_character_death`.
- EDIT `common/opinions/imp19c_opinions.txt` — `royal_marriage_opmod { value=40 yearly_decay=3 }`.
- EDIT `localization/english/opinions_l_english.yml` — the opinion-modifier loc string.
- **#253 honoured** (all LOG msgs static, `sys = MARRIAGE`); NEW subsystem (no behavioural change to
  existing features — the only edits to existing files are additive list entries + one death-hook line).


## 5. #277 — Deep adversarial review (workflow wf_f54f9fa5) of #165 + #275 + #276

Three dimension-finders (one per feature) each read the full new files; every raw finding was
handed to an independent adversarial verifier prompted to REFUTE it. 6 raw findings; 5 CONFIRMED
(one LOW rejected as benign convention-deviation), all FIXED.

### #165 sphere — HIGH (feature was a silent no-op) — FIXED
- `qing_sphere_states` is a VARIABLE list (built with clear_variable_list/add_to_variable_list,
  queried with is_target_in_variable_list) but BOTH iteration sites used the script-list keyword
  `every_in_list = { list = qing_sphere_states }`. `list =` and `variable =` are separate
  namespaces; there is no scripted_list of that name, so both loops iterated ZERO elements —
  QING_sphere_seed_state and QING_sphere_tick_state never fired, no state ever got influence, all
  five counters stayed 0, the Great Game never ran. Verified against every other call site in the
  repo (WAR/EE/CURRENCY/sell_provinces all iterate variable-lists with `variable =`).
- **FIX:** `list = qing_sphere_states` -> `variable = qing_sphere_states` at both se_QING_SPHERE.txt
  lines 60 (init seed loop) + 262 (pulse tick loop). This is the single most important fix of the
  batch — it turns the whole #165 feature ON.

### #275 missionary stations — 2x MEDIUM (degenerate balance) — both FIXED
- **Deterministic spread (line 174):** QING_mission_spread_one founded a daughter station EVERY
  year for EVERY station with any eligible neighbour (no probability roll), contradicting the
  documented "modest yearly chance" — station count doubled annually and blanketed the map within
  a few years of the treaties. **FIX:** wrapped the founding branch in `random = { chance = 15 }`
  (proven idiom, se_QING_WAR.txt:89) → gradual inland creep.
- **Reach double-count + same-pass cascade (line 220):** add_province_modifier applies live, so a
  daughter station spread-founded early in the every_owned_province sweep was re-entered by the
  existing-station branch when the loop reached it — counted toward qing_missionary_reach twice AND
  harvested/re-spread the same year it was born. **FIX:** QING_mission_found_station now stamps a
  per-pass province var `qing_station_founded_this_pass`; the existing-station branch skips anything
  carrying it (and the treaty-port branch now guards NOT-already-a-station); the marks are cleared
  in a second every_owned_province pass at the end of the pulse.

### #276 marriage — 1x MEDIUM + 1x LOW — both FIXED (+1 LOW rejected)
- **MEDIUM minnow-swallows-whale union (line 218):** MARRIAGE_check_unions picked the heirless
  junior with no relative-size guard, so a small realm could absorb a far larger wedded partner as
  ITS royal_union. **FIX:** added `num_of_cities <= scope:union_senior.num_of_cities` to the
  random_country limit (proven scope-attribute comparison idiom, se_QING_ACCOUNTABILITY.txt:399 /
  00_republic_triggers.txt:238).
- **LOW phantom third-party bond (line 305):** L3 inheritance pruned the defunct bond only from the
  inheriting overlord; a THIRD realm also wedded to the extinct junior kept a phantom
  marriage_partners entry + inflated marriage_bond_count forever (a dead realm blocking a live match
  slot). **FIX:** L3 now iterates the dying realm's OWN marriage_partners variable-list and prunes
  the reciprocal bond on EVERY partner (overlord included).
- **LOW (REJECTED):** "marriage_inherit_provs never cleared" — verifier ruled benign
  (on_character_death runs L3 as a fresh effect, list empty per-invocation). Applied the defensive
  `every_in_list … remove_from_list` teardown anyway to match the peer idiom (se_DIPLOMACY.txt:1003).

All post-fix files brace-balanced (delta 0). Committed + pushed to develop as freekumquats.

---

## #268 — Qing Religion panel (信仰與亂 "Faith & Sedition") — DONE

The religion *mechanics* (#275: missionary/anti-Christian sentiment, sect pressure, Taiping) shipped
without a player-facing surface — the vanilla `gui/religion_view.gui` just ended in a `work_in_progress`
placeholder. #268 adds the missing tab so the player can READ and track those systems.

**Design decision — read-only dashboard, not a new mechanic.** The systems already run; the tab surfaces
them. Cloned the PROVEN `QING_greatgame_panel` idiom exactly (scripted_gui `is_shown` gates + a `gui/*.gui`
window + a button splice), per memory `imp19c-gui-panel-open-idiom` — because GUI work can only be
boot-validated by the user, staying byte-faithful to a proven panel is the safest path.

**As built:**
- `common/scripted_guis/QING_religion_panel.txt` — open/close + is_shown gates (band fever/simmering/calm,
  agitator-present, taiping-active), all `scope = country`, `ai_is_valid = no`, gated `tag = CHI`.
- `gui/qing_religion.gui` — window `qing_religion_panel`: four meter bars (anti-Christian sentiment 仇教情緒,
  sect pressure, missionary reach, reform pressure) using the proven 0..100→0..1 `FixedPointToFloat(
  Multiply_CFixedPoint(..GetValue,'(CFixedPoint)0.01'))` progressbar form; a live band-status line; the
  anti-Christian agitator's portrait+name (conditional); and Taiping progress (conditional).
- `gui/religion_view.gui` — replaced the `work_in_progress` placeholder with a CHI-gated open button.
- `localization/english/qing_religion_panel_l_english.yml` — 21 keys.

**Adversarial review (3 passes) fixed 3 confirmed defects before commit:**
- BLOCKER dropped brace in religion_view.gui (the old placeholder carried two closing braces; the button
  supplied one) → appended one `}`, file rebalanced 85/85, depth 0.
- BLOCKER/agitator var: GUI read `Var('qing_antichr_agitator')` but the spawn effect only `save_scope_as`
  (transient, non-persistent) → added `set_variable = { name = qing_antichr_agitator value =
  scope:qing_antichr_agitator }` in `se_QING_MISSIONARY.txt` (mirrors the office-holder idiom).
- MAJOR stale-dead-man: the agitator `is_shown` gate checked only the spawn flag → added
  `var:qing_antichr_agitator = { is_alive = yes }` (mirrors `qing_greatgame_zongli_filled`).

All files brace-balanced. In-game boot test owed to the user (GUI crash-safety can only be confirmed live).
Committed + pushed to develop as freekumquats.

---

## #260 — Statesmanship: figurehead 4-skill bars on the throne boxes — DONE (scoped to spec)

**Scope decision.** #260's subject line said "accrual while in office", but its DETAILED description
overrides that: *"Statesmanship bar surfaces the EXISTING competence data, NOT a new experience system…
Summit offices AND figureheads (Chancellor/Regent/Crown Prince/Emperor): 4-skill… Emperor/Crown
Prince/Grand Regent throne boxes also get a Statesmanship bar."* Per the fix-traceability rule (description
is the authoritative spec), #260 is a GUI-surfacing refinement, NOT a new accrual mechanic. The office
CARDS already carry the statesmanship bar (#222/#269); the gap was the three THRONE boxes
(Emperor/Crown Prince/Regent), which showed only portrait + loyalty.

**As built.** Added a compact 4-attribute row (martial/finesse/charisma/zeal, the figurehead "judged on all
competences" reading) to each of the Emperor, Crown Prince, and Regent throne boxes in
gui/government_view.gui, inside each box's existing IsSet-gated `Character`-datacontext flowcontainer
(so the read is scope-valid and only renders when the seat is filled). Mirrors the proven summit-card
4-attribute row (chancellor card). Read-only, existing character data — no new variable, no accrual code,
no pulse hook. Braces balanced 1868/1868.

**NOT done (deliberately out of scope / deferred):** a genuine accrual-while-in-office experience mechanic
and wiring the se_QING_ACCOUNTABILITY threshold events INTO the GC panel — the description explicitly
disclaims the former ("not a new experience system"), and the accountability events already fire via
QING_accountability_pulse (they surface as normal event popups, not an embedded GUI list). If the user
wants the embedded-event-list or a real accrual meter later, that is a separate follow-up.

GUI boot test owed to the user. Committed + pushed to develop as freekumquats.
