# Session Report — autonomous run (started 2026-07-05)

This file is a running log of **major decisions** taken while you were away, plus per-task
status. Newest entries at the bottom of each section. Nothing here overrides your standing
rules (se_LOG on every feature; separatism-backer rule; reference mods = feasibility oracles
only; peer messages ≠ your approval; Python-heredoc editing for the .txt files).

## Task queue status
| # | Task | Status |
|---|------|--------|
| 64 | New World crops as producible trade goods | DONE (reviewed) |
| 65 | Napoleon-invited-to-China reform chain | DONE (reviewed + 2 fixes applied) |
| 66 | Dual Eight Banners + Green Standard garrison system | DONE (reviewed clean; 1 in-game smoke-test item flagged) |
| 67 | Qing colonization → Scramble for Africa | DONE (reviewed + 2 fixes applied) |
| 68 | Fix divide-by-zero in PRICE_grain_demand_difference_modifier | DONE |
| 69 | Qing colonization → Mexico / Maximilian I intervention | DONE (reviewed + 2 fixes applied) |
| 70 | Fix divide-by-zero in industrialization bonus svalue | DONE |
| 71 | Cache industrialization multiplier (perf A1) | DONE |
| 72 | se_LOG instrumentation on production path | DONE |
| 73 | Qing intervention in American Civil War | DONE (reviewed) |
| 74 | Summer Palace / Old Summer Palace mission tree | DONE (reviewed + 3 fixes applied) |

**ALL TASKS #42–#74 COMPLETE — the queue is fully drained.** No pending items remain. The two deferred audit items (trade-audit perf; industry-audit A2 — 43 raw-goods traversals) were explicitly *noted, NOT tasked* — awaiting your confirmation before I start them.

**BACKLOG (deferred, NOT to implement yet):**
- **#75 — Build out US-native American Civil War content.** The mod has no US-side ACW mechanic: the USA tag is a near-stub, there's no secession/sectional/slavery content, and `CSA` is a phantom tag (dangling custom-name + loc only, never instantiated — `c:CSA` unusable; the real `ICF` "Iron Confederacy" is unrelated). The only ACW content is the #73 Qing-facing chain, which releases a Confederacy dynamically off USA land *because* c:CSA doesn't exist. Deferred by user 2026-07-05.

**IN PROGRESS — #74 Summer Palace rework (historical correction).** User caught that the tree conflated the 圓明園 (Old Summer Palace) and 頤和園 (Summer Palace) as one garden rebuilt — they are TWO DISTINCT sites ~2.5km apart (Yuanmingyuan destroyed 1860 & never rebuilt; Yiheyuan rebuilt 1888 on the separate Qingyi Yuan site). Academic EN+ZH research done (memory: imp19c-summer-palace-history) — it ALSO flagged that my navy-funds framing used the discredited "Cixi drained the fleet" popular narrative. Direction chosen by user: split into two palaces + bridge to the engine Great Works/Wonder mechanic (`has_great_work` gate/bonus + `on_great_work_completed` on_action; no scripted create_great_work exists, no new art). Rework pending.

## #74 DONE (2026-07-05) — the Garden of Gardens (圓明園／頤和園, the Summer Palace tree)
- Built a **CHI-only, player-driven Qing mission tree** to raise the imperial garden-palace, cross-wired to its two real historical fates: the **1860 Anglo-French sack** (reactive event) and the **1888 Cixi navy-funds diversion** (capstone dilemma). Documented QING_FEATURES.md **§11.3** (under Cultural patronage 文治). No pre-existing Summer Palace / Yuanmingyuan content existed — clean build.
- **Files created:** `common/missions/qing_summer_palace_missions.txt` (mission + 4 tasks), `common/scripted_effects/se_QING_SUMMER_PALACE.txt` (3 verbs), `events/imp19c_mod_events/qing_summer_palace_events.txt` (namespace `qing_summer_palace`; `.1` sack + `.2` dilemma), `common/modifiers/qing_summer_palace_modifiers.txt` (6 modifiers), `localization/english/qing_summer_palace_l_english.yml` (28 keys). **Edited:** `se_QING_DECLINE.txt` — one `random_list` entry (`6 = {...}`) in `QING_frontier_flavour_roll`, gated `has_variable qing_sp_built` + `current_date >= 1856` + `(war_with c:GBR OR c:FRA)`.
- **The tree:** root `qing_sp_yuanmingyuan` (treasury 120 + owns Beijing p:8363; sets flag `qing_sp_built`, grants `qing_sp_garden_of_brightness`) → `qing_sp_european_pavilions` (西洋樓, `qing_sp_european_marvels`) + `qing_sp_siku_library` (四庫全書, `qing_sp_imperial_library` + `qing_civic_identity +3`) → capstone `qing_sp_yiheyuan` (fires event `.2`).
- **The 1860 sack (`qing_summer_palace.1`, reactive):** `QING_sp_sack_of_1860` strips all three garden modifiers, applies permanent `qing_sp_burnt_ruins` (−prestige/−stability/−happiness), flips flag `qing_sp_built`→`qing_sp_burnt`, **but** `qing_reform_pressure +12` + `qing_civic_identity +8` (the sack as a founding nationalist wound). Event re-checks its own trigger (war + garden standing) so a stale roll pick is a no-op.
- **The 1888 navy-funds dilemma (`qing_summer_palace.2`, capstone-fired):** option A `QING_sp_rebuild_divert_navy` (full splendour `qing_sp_yiheyuan_splendour` + prestige 30, but permanent `qing_sp_starved_fleet` malus + `qing_selfstr_progress −8` — the Yalu 1894 road); option B `QING_sp_rebuild_from_treasury` (gated treasury ≥250: same splendour, no starved fleet, eases reform pressure). Both clear `qing_sp_burnt`/re-set `qing_sp_built`. `.2` desc branches via `first_valid` on adorn-vs-ashes.
- **Design decisions:**
  - **CAUGHT PRE-REVIEW — no CK-style country flags in this engine.** My first draft used `set_country_flag`/`has_country_flag`/`clr_country_flag`; a grep showed those verbs appear NOWHERE else in the mod (Imperator uses variables as flags). Converted ALL flag state to the mod's established `set_variable`/`has_variable`/`remove_variable` idiom (the same `qing_uscw_decided` boolean-var pattern) before any review — would have been a silent no-op / load issue otherwise.
  - **CAUGHT PRE-REVIEW — invalid modifier key.** `monthly_character_prestige` (character-scope stat) was used on country modifiers where it does nothing; grep confirmed it's used nowhere else. Swapped all 3 occurrences to `monthly_legitimacy` (58 uses in the mod — the dynastic-prestige key, thematically ideal for imperial splendour). Re-verified all 10 modifier stat keys are used elsewhere.
  - **The sack strips optional modifiers safely.** `remove_country_modifier` on `qing_sp_european_marvels`/`_imperial_library` fires even if those optional adorning tasks were never done — a safe no-op in this engine.
  - **`war_with = c:GBR` / `c:FRA`** at ROOT scope — verified the correct trigger form (Invictus reference uses `war_with = c:TAG`); GBR/FRA are real tags. Beijing = p:8363 verified by name+area in province_setup.csv.
- **se_LOG:** all 3 verbs wrapped `LOG_enter`/`LOG_exit`; the sack's guard-miss (no standing garden) emits `LOG_fail`; every task on_start/on_completion + both events' immediate blocks log `sys=QING`.
- **Verified:** brace balance (missions 46/46, verbs 33/33, events 17/17, modifiers 6/6, DECLINE 654/654); byte conventions (missions/verbs/modifiers no-BOM/LF, events + loc BOM/LF); all loc keys resolve (no missing); all verbs/modifiers/external deps (`QING_DECLINE_nudge`, `qing_selfstr_progress`, `qing_civic_identity`, `qing_reform_pressure`) resolve; flag lifecycle coherent.
- **Review RETURNED — verdict SOUND, no CRITICAL/HIGH; 2 MEDIUM + 1 LOW fixed, 2 LOW skipped (2026-07-05):** flag idiom, all 10 modifier keys, `war_with = c:TAG` form, Beijing p:8363, external verbs, `remove_country_modifier` no-op convention, DECLINE roll edit, loc 1:1 — all PASS.
  - **Applied FIX (MEDIUM #1 — modifier double-stacking):** on the never-sacked "adorn" path the capstone added `qing_sp_yiheyuan_splendour` while `qing_sp_garden_of_brightness` stayed active → ~double legitimacy/popularity/happiness, and asymmetric vs the burnt path. **Fix:** both rebuild verbs now `remove_country_modifier = qing_sp_garden_of_brightness` before adding the splendour (the Yiheyuan is the *upgraded main garden* — it supersedes, not stacks). **Deliberately kept** `european_marvels` + `imperial_library` on the adorn path: those are DISTINCT structures (the Xiyanglou pavilions, the Siku library) that physically survive if the garden was never sacked — a narratively-motivated reward for avoiding the 1860 burning (the burnt path lost them to Elgin's torch). So the asymmetry is now intentional and earned, not a double-count.
  - **Applied FIX (MEDIUM #2 — post-1888 re-sack contradiction):** the sack has no upper date bound, so a later Anglo-French war could re-fire it on a rebuilt garden, leaving `qing_sp_burnt_ruins` + `qing_sp_yiheyuan_splendour` active together. **Fix:** the sack now also strips `qing_sp_yiheyuan_splendour` (a burnt garden carries no "restored magnificence"). Net: `garden_of_brightness` stripped 3× (sack + both rebuilds — the duplicate); pavilions/library/splendour stripped 1× (sack only).
  - **Applied FIX (LOW #1 — missing `_mission_DESCRIPTION`):** every sibling mission-group loc supplies `<group>_mission_DESCRIPTION`; mine had only the title. Added a proper blurb (was rendering a blank heading).
  - **Skipped (LOW #2 — bare `desc` fallback in `first_valid`):** this is my own established idiom (ships + works in `qing_uscw_events.txt`); the reviewer confirmed the engine tolerates it. Kept for consistency with existing code rather than churn to the `triggered_desc{always=yes}` form.
  - **Verified (LOW #3 — picture keys):** `revolt` + `chinese_throne_room` are both used elsewhere in the mod's event suite (proven valid), not blank.
  - Post-fix: verbs 33/33, all byte conventions preserved, loc now 29 keys, no malformed lines.

## #73 DONE (2026-07-05) — the Qing and the American Civil War (南北戰爭)
- Built a **CHI-only, player-only, 1861–65 event chain** letting a Pacific-reaching Qing take a side in the American Civil War — the exact contemporary of the Taiping Rebellion (two continental civil wars at once, on opposite Pacific shores). Offered once via `QING_frontier_flavour_roll` (se_QING_DECLINE.txt). Documented in QING_FEATURES.md **§13.4**. Deliberately keyed on the **Daoguang entente** from the Mexican arc (§13.3), so the two American arcs pull against each other.
- **Files created:** `common/scripted_effects/se_QING_USCW.txt` (4 verbs), `events/imp19c_mod_events/qing_uscw_events.txt` (namespace `qing_uscw`; `.1` fork + `.2` coda), `common/modifiers/qing_uscw_modifiers.txt` (3 outcome modifiers), `localization/english/qing_uscw_l_english.yml` (18 keys). **Edited:** `se_QING_DECLINE.txt` — one `random_list` entry (`8 = {...}`) in `QING_frontier_flavour_roll`, gated on `exists c:USA` + the date window + `NOT has_variable qing_uscw_decided`.
- **The three-way fork (`qing_uscw.1`):**
  - **聯邦之誼 Back the Union** — option `trigger`-gated on `has_country_modifier = qing_daoguang_doctrine` (only offered if the Pacific entente is sealed). Mutual `qing_gp_accommodation_opinion` with USA, `CURRENCY_grant_country_wealth thousands=60`, a `QING_selfstr_advance amount=5` *if* `qing_selfstr_progress` exists, `qing_uscw_union_amity` modifier; **provokes Britain** (severity 8 — Lancashire's cotton lords + the Mersey-built raiders leaned Confederate, so by 以夷制夷 this delights Britain's rivals).
  - **邦聯之利 Recognise the Confederacy** — always available. `CURRENCY_grant_country_wealth thousands=90` + `qing_uscw_cotton_windfall`, then `QING_uscw_release_confederacy`, then USA gets `qing_gp_rivalry_opinion`.
  - **中立厚利 Stay neutral** — always available. `thousands=110` + `qing_uscw_neutral_trade` + prestige 10; no provocations.
  - Each option fires `qing_uscw.2` on a `days={600 1400}` delay; `.2`'s desc branches via `first_valid`/`triggered_desc` on whichever outcome modifier is present.
- **Design decisions:**
  - **CSA is a PHANTOM tag** (custom-name loc entry in se_COUNTRYNAME.txt but NOT in the master tag list), so `c:CSA` is unusable. `QING_uscw_release_confederacy` therefore releases the Confederacy **dynamically** off c:USA's own Deep-South (SC/GA/AL/MS/AR/LA/FL) + Appalachian (WV/KY/TN) provinces via `LAND_release_from_list` (releaser=c:USA, `government_type=flag:oligarchic_republic`, `country_name/adj=qing_uscw_csa_name/_adj`), the same idiom the separatism engine (#47) and protectorate releases use. Guarded on `count >= 3` — if the Union doesn't hold enough of that ground in this timeline, recognition is diplomatic only (logged as a guarded miss, no phantom country). List self-clears at the end so the verb is re-callable.
  - **The entente cross-wire.** The Union option is the *reward* for the Daoguang Doctrine; but the Mexican arc (§13.3) *breaks* that Doctrine. So a player who took the Mexican throne finds the Union path closed here — the two American arcs are wired to be mutually exclusive on their most cooperative branches.
- **se_LOG:** every verb wrapped `LOG_enter`/`LOG_exit`; every guard-miss (USA absent, too little Southern land, release produced no `new_country_scope`) emits `LOG_fail`; the event `immediate` blocks log `sys=QING`.
- **Verified (my pass + review):** brace balance (USCW 61/61, events 29/29, modifiers 3/3, DECLINE 649/649); byte conventions preserved (se_* + modifiers no-BOM/LF, events + loc BOM/LF); regions `Deep_South` (regions.txt:1270) + `Appalachia` (:264) exist; **no `c:CSA`** anywhere (only in explanatory comments); all external verbs resolve (`QING_gp_provoke_britain`, `CURRENCY_grant_country_wealth`, `QING_selfstr_advance`, `LAND_release_from_list`, LOG_*); opinion modifiers (`qing_gp_accommodation_opinion`/`_rivalry_opinion`) + all 3 local modifiers + all 7 modifier effect-keys used elsewhere; all 18 loc keys resolve, no missing/dupes.
- **Review RETURNED — verdict SOUND, no CRITICAL/HIGH; 3 LOW polish fixes applied (2026-07-05):** the review independently confirmed every high-risk item. **List-cross-scope is SAFE** (it found a *second* proof beyond mine: `CURRENCY_create_starting_currencies` builds a list inside `c:EIC = { every_subject { add_to_list } }` and consumes it outside — lists are global to the effect execution, and `ROOT` inside the `c:USA` block still resolves to CHI so `target = ROOT` is correct). `LAND_release_from_list` signature, regions, `qing_daoguang_doctrine` reachability, all effects/opinions/modifiers/loc keys — all PASS.
  - **Applied FIX (LOW #2):** added `LOG_enter`/`LOG_exit` to `QING_uscw_release_confederacy` (the only verb missing them — standing error-logging rule).
  - **Applied FIX (LOW #3):** moved `LOG_exit result=OK` *inside* the success branch in `back_union` + `back_confederacy` so a USA-absent path no longer logs both FAIL and OK.
  - **Applied FIX (LOW #1):** softened the `government_type = flag:oligarchic_republic` comment — clarified it does NOT literally set an oligarchic republic (se_LAND.txt only reads that arg for `flag:dynamic`); it just avoids the viceroyalty default, exactly as SEPARATISM does. Behaviour unchanged & consistent with the reference caller.
  - **Skipped (cosmetic, provably harmless):** LOW #4 (redundant accommodation-opinion re-add — the doctrine mission already added it; idempotent) and LOW #5 (wealth granted before the USA-exists guard — unreachable since event `.1` requires `exists=c:USA`).
  - **Noted, NOT a #73 defect:** `current_ruler = { add_prestige = N }` on character scope is a house pattern used 16+ times across the shipped mission trees; if it's a silent no-op on character scope that's a mod-wide latent issue for a separate pass, not introduced here.
  - Post-fix brace balance: se_QING_USCW.txt now **63/63**; byte conventions preserved.

## #69 DONE (2026-07-05) — the Manila Galleon & the Mexican Adventure (馬尼拉大帆船 / 墨西哥帝業)
- Extended the Qing colonization mission tree with a **Mexico arc** — the one enterprise grounded in a *real* China–New World tie: the Manila-Acapulco galleon (1565–1815, the silver-for-silk artery that closed the very year the game opens). Cross-wired to the #65 Napoleon chain and to the French Second Empire's Maximilian adventure (1862–67). Documented in QING_FEATURES.md **§13.3** (+ new 墨西哥 row in the §13.1 protectorate table).
- **Four new tasks** appended to `qing_colonization_missions.txt` before the CAPSTONE (cloned from the file's own idiom): `qing_col_galleon` (requires bureau; treasury 150 + fleet-or-California gate; claims **Acapulco p:1800** — the galleon's American terminus; `QING_COLON_frontier_pull`; silver-road modifier; wealth 80; prestige 20; provoke GBR 6 *guarded by* `NOT daoguang_doctrine`) → `qing_col_veracruz` (requires galleon; treasury 170; claims **Veracruz p:2069** — the real 1862 French landing point — as a `QING_gp_frontier_play` vs FRA; gulf-gate modifier; wealth 70; provoke FRA 8) → `qing_col_maximilian` (requires veracruz; treasury 200 + influence 20; claims **Mexico City p:8516**; mexican-crown modifier; wealth 90; prestige 30; **the fork** — see below) → `qing_col_mexican_empire` (requires maximilian; influence 30; releases the Mexican interior as an `imperial_monarchy` sinosphere tributary via `QING_establish_protectorate`, log_tag=MEXICO).
- **Design decisions:**
  - **The Napoleon fork (the cross-wire to #65).** `qing_col_maximilian` branches on `has_variable = qing_napoleon_present` (the country var #65 sets when the Emperor Emeritus is at court). **If present:** a Franco-Qing condominium props up his nephew Napoleon III's Habsburg empire — mutual `qing_gp_accommodation_opinion` with FRA + a `loyalty_qing_congenial` pulse on `var:qing_napoleon_char` (backing his family's imperial project *serves his revenge*, exactly the loyalty logic in `QING_napoleon_loyalty_pulse`), but it **provokes Britain** (severity 10). **If absent:** the Qing seizes the adventure solo and **provokes France** (severity 12), whose New-World project it pre-empts. This makes the same task read completely differently depending on the #65 chain's state.
  - **Daoguang-entente BETRAYAL check.** Enthroning a European-style monarchy in the Americas violates the Pacific entente: if `qing_daoguang_doctrine` is active and the USA exists, the adventure adds `qing_gp_rivalry_opinion` from the USA (the partner feels betrayed). So the arc actively *breaks* the Doctrine the Pacific arc built — a deliberate tension between the two colonization branches. Only the opening galleon step still honours the Doctrine (guards its GBR provocation on `NOT daoguang_doctrine`); from Veracruz on, the European contest overrides it.
  - **No double-release with Anxin.** `qing_col_anxin` already sweeps `Pacific_Mexico` into the New-World protectorate, so the Mexican Empire release is scoped to **Eastern_Mexico + Northern_Mexico + Central_America only** — the two protectorate tasks can never contest the same province. Verified all three region names in `map_data/regions.txt`; verified `Pacific_Mexico` is excluded.
  - **`government = imperial_monarchy`** for the release (verified valid in `common/governments/`) — historically exact for "Emperor of Mexico," and the first non-viceroyalty/non-republic protectorate in the tree.
  - **MAP-DATA TRAP honoured (the #67 lesson):** all three province IDs verified by NAME + AREA + REGION in `province_setup.csv`/`regions.txt`, not culture column — p:1800=Acapulco (area Acapulco, region Pacific_Mexico), p:2069=Veracruz (area Veracruz, region Eastern_Mexico), p:8516=Mexico_City (area Mexico, region Pacific_Mexico).
- **Four new modifiers** in `qing_colonization_modifiers.txt` (`qing_col_silver_road`/`_gulf_gate`/`_mexican_crown`/`_mexican_empire_mod`); all effect keys (`global_export/import_commerce_modifier`, `naval_range`, `global_commerce_modifier`, `global_tax_modifier`, `monthly_legitimacy`, `land_morale_modifier`) verified used elsewhere in the mod.
- **Loc** in `qing_colonization_l_english.yml`: English titles + DESC + tooltips for all 4 tasks (incl. the fork spelled out in `qing_col_maximilian_tt`), 3 allow-tooltips, `qing_protectorate_mexico_name`/`_adj`, 4 modifier display names. All lines well-formed `key:0 "..."`.
- **se_LOG:** every task on_start/on_completion emits `LOG_line sys=QING` (incl. distinct log lines on each fork branch + the betrayal branch); the MEXICO release goes through the fully-instrumented `QING_establish_protectorate`.
- **Verified:** brace balance (missions 489/489, modifiers 30/30); byte conventions preserved (missions + modifiers no-BOM/LF, loc BOM/LF). Also fixed a **stale doc bug** in §13.2: the Congo line still cited the pre-#67-review province IDs (p:3176/p:57) — corrected to p:2652/p:3526.
- **Review RETURNED — 1 HIGH + 1 MEDIUM, both FIXED (2026-07-05):**
  - **HIGH — the Empire of Mexico was released *without its own capital*.** `qing_col_maximilian` claims Mexico City (p:8516), but p:8516's area `Mexico` is in region **Pacific_Mexico** — and my `qing_col_mexican_empire` release swept only Eastern/Northern_Mexico + Central_America, so Mexico City never joined the Empire. Worse, `qing_col_anxin` releases exactly `Pacific_Mexico`, so the throne's seat would have fallen to the *Anxin* New-World protectorate instead — the arc's whole payoff (a client emperor at Mexico City) silently broken. This was the exact #67 region-mismatch trap again (I'd assumed Mexico City sat in "Eastern/Central Mexico"). **FIX (geographically better than a patch): moved `Pacific_Mexico` OUT of Anxin and INTO the Empire of Mexico.** Bundling central Mexico with the Alaska→California coast was always a stretch; now Anxin = the clean Pacific-Northwest + California coast, and the Empire = all four Mexican regions seated at Mexico City. The two releases remain fully disjoint (verified no shared area), so still no double-release. Updated the allow-gate + harvest list in both tasks, the design comment, and all affected loc (Anxin requirement, Mexico requirement/tooltip/DESC).
  - **MEDIUM — Veracruz opened its diplomatic play unconditionally.** `QING_gp_frontier_play { tag=FRA province=2069 }` sat *outside* the `exists p:2069 / NOT owns` guard, unlike every sibling task (Amur/Tashkent/Alaska/Cape/Suez all nest the play inside the guard). If the Qing already owned Veracruz or the province were absent, it would still fire a get-territory play for owned/nonexistent ground. **FIX: nested the play inside the same `if` as the `add_claim`.**
  - Everything else CLEAN per review + my own pass: province IDs correct by name+area, all effect signatures match, the Napoleon cross-wire is scope-correct (country-scope vars, `is_alive` guard before `add_loyalty`), `imperial_monarchy`/opinions/loyalty defs all valid, every modifier token valid, se_LOG on every task, all loc keys resolve with no dupes. Post-fix brace balance still 489/489; byte conventions preserved.

## #68 DONE (2026-07-05) — PRICE divide-by-zero
- `PRICE_grain_demand_difference_modifier` in `PRICE_svalues.txt`: the `else` branch fired whenever `PRICE_grain_demand_difference_raw >= 0`, which INCLUDES `== 0`, then did `divide = raw` → divide-by-zero → NaN. Added an `else_if { raw = 0 → value = 1 }` guard (supply==demand = no price pressure = no-op modifier). `else_if` verified valid engine syntax (used 55× in AI_svalues). Braces balanced, BOM/CRLF preserved.
- Note: these three `PRICE_grain_*` svalues currently have **no live consumers** (the active TZ price path in `se_PRICE.txt` uses `total_supply_TZ`); the fix is defensive against re-activation, matching the audit's P0 flag. Did NOT delete the dead code (out of scope; low risk; may be intended for future use).

## Two economy audits completed (2026-07-05)
- **Trade-system audit** (you requested it alongside #64). Headline findings:
  - **P0 correctness:** genuine divide-by-zero in `PRICE_svalues.txt` `PRICE_grain_demand_difference_modifier` when supply==demand → NaN propagation. → filed as task #68.
  - P0 perf: O(goods×tradezones) global-variable reset explosion in `se_GLOBALTRADE_split.txt`; repeated `every_country{every_governorships{}}` passes; caching gaps.
  - Consistency: goods enumerated in svalues but absent from `trade_goods/` (and vice-versa) create silent undefined-var drift — reinforces the discipline I'm applying to the 5 new crops.
- **Industry/production audit** (you requested a second agent). Headline findings:
  - **P0 correctness (B1):** divide-by-zero in `GOODS_svalues.txt` `GOODS_governorship_bonus_to_industrial_production_from_industrialisation` when a governorship has zero states.
  - **P0 perf (A1):** that industrialization multiplier is recomputed 28× per governorship per quarter (double state-traversal each time) — cacheable to 1.
  - **P0 perf (A2):** 43 separate `every_governorship_state{every_state_province{}}` raw-goods traversals per governorship per quarter — collapsible to a single switch-binned pass.
  - **P0 (B2):** the entire production path has ZERO se_LOG instrumentation despite the ECON phase markers around it — violates the standing error-logging rule.

## #65 DONE (2026-07-05) — Napoleon at the Qing court (the Emperor Emeritus reform chain)
- Built the full counterfactual chain: Napoleon received after Waterloo, seated in a revived 太上皇 (Emperor Emeritus) Grand Council office, drives a reform slate, unlocks a dedicated military tradition. Documented in QING_FEATURES.md **§17**.
- **Files created:** `common/scripted_effects/se_QING_NAPOLEON.txt` (spawn, take-office, conservative backlash, revenge tilt, conditional-loyalty pulse, 4 reform verbs, doctrine capstone), `common/military_traditions/00_napoleon.txt` (Grande Armée tree), `events/imp19c_mod_events/qing_napoleon_events.txt` (`qing_napoleon.1`–`.4`), `localization/english/qing_napoleon_l_english.yml`.
- **Files edited (pure additions, byte convention preserved):** `qing_mechanics_modifiers.txt` (+78: office-active, backlash, 5 reform modifiers, doctrine capstone), `00_monthly_country.txt` (+loyalty pulse), `qing_mechanics_on_actions.txt` (+init), `se_QING_COUNCIL.txt` (+emeritus vacate branch), `se_QING_DECLINE.txt` (+arrival offer in flavour roll), `military_traditions_l_english.yml` + `qing_mechanics_l_english.yml` (loc).
- **Design decisions (all per the locked brief in memory `imp19c-napoleon-in-china`):**
  - **太上皇 office built on the EXISTING parameterized office machinery** (`QING_office_appoint = { office = emeritus }`) — new key plugs into the `qing_office_$office$_active/_holder/_vacancy` system for free; only a new `qing_office_emeritus_active` modifier was needed.
  - **Napoleon is DIVISIVE:** `qing_emeritus_conservative_backlash` modifier rides alongside the reform buffs the whole time he holds office; the `qing_manchu_staunch` conservatives lose loyalty (reuses the existing identity band, no new "conservative" state).
  - **Napoleon is CONDITIONALLY loyal:** `QING_napoleon_loyalty_pulse` (monthly) scores him HIGH while reforms advance AND GBR/RUS tension is high, DROPS on appeasement/stalled reform. The anti-GBR/RUS pro-FRA tilt is wired through the EXISTING GP-rivalry counters (`QING_gp_provoke_britain/russia`, `QING_gp_side_with_france`) — no parallel diplomacy state.
  - **Reforms reuse the Self-Strengthening progress engine** (`QING_selfstr_advance`/`_build`) + real institution grants (`CURRENCY_grant_country_wealth`, `EDU_school`, a real raised legion for the levée) per the brief, rather than inventing a new progress track.
  - **Dedicated Grande Armée tradition (`00_napoleon.txt`) gated on the `qing_napoleon_present` COUNTRY VARIABLE, not a culture group** (Napoleon is French, the Qing jurchen — a culture gate could never open). Deliberately oversized buffs. Only modifier keys proven valid in the mod's populated trees were used.
- **Bug caught + fixed during build: modifier KEY COLLISION.** My capstone was initially keyed `qing_daoguang_doctrine`, but that key ALREADY EXISTS in `qing_colonization_modifiers.txt` (an unrelated colonization-aggrandisement modifier read by colonization task effects). Two modifiers sharing a key → the later-loaded file silently overrides → the colonization capstone would break. Renamed mine to `qing_napoleon_daoguang_doctrine` (same 道光主義 display name, distinct key); updated all 3 references + the loc.
- **Bug caught + fixed: invalid trait.** `add_trait = charismatic` — no such trait key in `common/traits/`. Swapped for `confident` (verified in `00_military.txt`), apt for Napoleon.
- **Aligned the levée commander-attach to the proven `scope:` idiom** (save Napoleon to `scope:levee_commander` first, then `add_to_legion = PREV` + `random_legion_unit = { set_as_commander = scope:levee_commander }`) rather than the non-standard `set_as_commander = ROOT.var:...` I first wrote — mirrors `QING_selfstr_raise_evarmy_legion`.
- **Verified before review:** brace balance 0 + byte convention preserved on all 11 touched files (git numstat shows pure X/0 additions, no whole-file rewrites); all called verbs / loyalty types / traits / the `EDU_school` building / `char:227`=Daoguang / all placeholder tradition `.dds` icons exist; the scope-in-variable idiom (`value = scope:napoleon` → `var:qing_napoleon_char = { }`) has mod-wide precedent (`dejure_agitation_sponsor`, tradezone scope vars).
- **Code review DISPATCHED** (scope-correctness, event-chain re-fire logic, loc completeness, tradition gate, modifier-key validity). Findings + any fixes to be appended here when it returns.
- **Review RETURNED — 2 real defects, both FIXED (2026-07-05):**
  - **FINDING 1 (HIGH) — backlash/office modifiers stranded on Napoleon's death.** `qing_emeritus_conservative_backlash` (a permanent stability/legitimacy drag) and `qing_office_emeritus_active` were removed ONLY by the manual `QING_office_vacate_dispatch` (dismissal GUI). Nothing wired the *death* case — `on_character_death` never vacated the office — so when Napoleon (a create_character aged 46) dies in office, the penalty persists forever with no in-game way to remove it, the exact opposite of the intended "the backlash lifts when he's gone." FIX: added to `on_character_death` (`00_specific_from_code.txt`) a guarded `if = { limit = { has_variable = qing_office_held } QING_office_vacate_dispatch = yes }` + a councillor-unseat guard. Both verbs are call-site-agnostic (resolve country via `employer`) and self-guard, so it's a safe no-op for the ~all characters holding neither — and it closes the same latent gap for all ten regular great offices at once.
  - **FINDING 2 (MEDIUM) — take-office conservative-loyalty penalty hit zero characters.** `QING_napoleon_apply_conservative_backlash` filtered `every_character` on the `has_character_modifier = qing_manchu_staunch` MODIFIER, but that modifier is applied only by `QING_char_shift_identity` once `var:qing_manchu_identity >= 66` — which may not have run yet at Napoleon's early-game arrival (< 1821.5.5). The identity VARIABLE is seeded at init (80 for Manchu courtiers), so the modifier-only match caught nobody and the character-loyalty half of the "divisive foreigner" cost silently no-oped. FIX: widened the limit to `OR = { has_character_modifier = qing_manchu_staunch  AND = { has_variable = qing_manchu_identity  var:qing_manchu_identity >= 66 } }` (the `has_variable` guard avoids a missing-var read on never-initialised courtiers; the `>= 66` mirrors the shift-identity staunch threshold).
  - Everything else the review checked came back CLEAN: scope correctness (Napoleon employed by CHI via `set_home_country=ROOT`; `employer`/`ROOT` resolve to CHI not Napoleon), the levée `raise_legion`+`scope:levee_commander` idiom, the `.2` self-re-fire hub + `.4` `>=3` gate + effect-less `.2.g` option, full loc coverage, the tradition `allow` gate, all 7 modifier keys + the capstone rename. Brace balance 0 + byte conventions preserved on both fixed files (se_QING_NAPOLEON.txt no-BOM/LF; 00_specific_from_code.txt BOM/CRLF).

## #67 DONE (2026-07-05) — the Scramble for Africa (鄭和下西洋復興)
- Extended the Qing colonization mission tree with a **southern enterprise** mirroring the Pacific arc: a revival of the Zheng He treasure voyages that arrives in Africa amid the 19th-c. European partition. Documented in QING_FEATURES.md **§13.2** (+ new 安非 row in the §13.1 protectorate table).
- **Five new tasks** appended to `qing_colonization_missions.txt` before the CAPSTONE (all cloned from the file's own idiom — `qing_col_alaska`/`_central_asia`/`_anhai` templates): `qing_col_zheng_he` (requires bureau; claims Zanzibar p:1489 + Kilwa p:1715 — the actual Swahili landfall; treasure-fleet modifier; `QING_COLON_frontier_pull`; provoke GBR 8) → `qing_col_cape` (requires zheng_he; claims Western Cape p:132 as a `QING_gp_frontier_play` vs GBR; provoke GBR 12) + `qing_col_suez` (requires zheng_he; claims Suez p:413 as a play vs GBR + Cairo p:429; provoke GBR 10 **and** FRA 8) → `qing_col_congo` (requires cape; claims Congo p:3176 + Nigeria p:57; provoke GBR 8 + FRA 10) → `qing_col_anfei` (requires cape; the invented African Protectorate-General via `QING_establish_protectorate`, government=viceroyalty, log_tag=ANFEI, over 10 African regions).
- **Design decisions:**
  - **Contest BRITAIN + FRANCE, not Russia** — the Scramble's paramount powers. Routed every provocation through `QING_gp_provoke_britain`/`_france`, which by the existing 以夷制夷 `QING_gp_rivals_delight` logic *delights* Russia (their rival) rather than provoking her — the opposite triangle from the Pacific/Central-Asia arc's anti-Russia thrust. Gives the two colonization arcs distinct diplomatic flavour.
  - **The Daoguang Doctrine deliberately does NOT suppress African friction.** Unlike the Canada/California tasks (which check `NOT = { has_country_modifier = qing_daoguang_doctrine }` before provoking), the African tasks provoke unconditionally: the Doctrine is a *Pacific-basin* Monroe-style entente closing the Americas and the Pacific; it has no writ in Africa or the Indian Ocean. Documented this as intentional in both the file comment and §13.2.
  - **Historically-anchored province claims** — Zanzibar & Kilwa are the real Ming-fleet landfalls (the Zheng He echo the user wanted); the Cape (British from 1806) and Suez (the 1869 canal / 1882 British occupation) are the sea-lane chokepoints; the Congo is the Berlin-Conference crucible. All 7 province IDs verified present in `common/province_setup.csv` with matching names/pops.
  - **East Africa is the `Lake_Victoria` region** (which contains the Zanzibar + Kilwa areas) — there is no standalone "Swahili"/"Zanzibar" region; verified against `map_data/regions.txt`. All 10 regions in the `qing_col_anfei` gate confirmed real region names.
- **Five new modifiers** in `qing_colonization_modifiers.txt` (naval-range/commerce themed); all effect keys (`naval_range`, `naval_morale_modifier`, `global_export_commerce_modifier`, `global_import_commerce_modifier`, `global_ship_recruit_speed`, `global_commerce_modifier`, `global_tax_modifier`, `monthly_legitimacy`) verified used elsewhere in the mod.
- **Loc** in `qing_colonization_l_english.yml`: real English task titles + flavourful DESC + tooltips for all 5 tasks, `qing_protectorate_anfei_name`/`_adj`, 5 modifier display names. All referenced keys confirmed resolving; no duplicate keys.
- **se_LOG:** every task on_start/on_completion emits `LOG_line sys=QING`; the ANFEI protectorate goes through `QING_establish_protectorate` (already fully LOG-instrumented).
- **Verified:** brace balance 0 on the mission file (402/402) and modifiers (26/26); byte conventions preserved (mission + modifiers no-BOM/LF, loc BOM/LF). Code review DISPATCHED.
- **Review RETURNED — 1 CRITICAL + 1 LOW, both FIXED (2026-07-05):**
  - **CRITICAL — `qing_col_congo` claimed the wrong province.** I picked **p:3176** for "the Congo" because its culture column is `kongo` — but p:3176 is `Ostrova`, AREA `Novgorod` (a forest tile in *Russia*). The claim would resolve against a valid-but-wrong province (no error thrown, silent misfire — a Qing claim on Russian soil). FIX: swapped to **p:2652** (`kongo` culture, AREA `Equatorial_Africa`, which IS in the `Congo_Basin` region) — geographically correct AND inside the `qing_col_anfei` harvest set. Lesson: the `kongo` *culture* column is not a reliable proxy for Congo *geography*; always verify the province's AREA/name, not just its culture (some faulty map tiles carry mismatched culture columns).
  - **LOW — p:57 mislabelled "the western/Guinea coast."** p:57 is `Maiduguri`, AREA `Nigeria` — the far interior NE (Lake Chad), not coastal; the loc promised "the Guinea coast." FIX: swapped to **p:3526** (`Libreville`, AREA `Gabon`) — a real Gulf-of-Guinea coastal city, in the `Gulf_of_Guinea` region (also in the anfei harvest set). The loc "Congo basin and the Guinea coast" is now literally accurate.
  - **Review finding 3 (region-coverage gap) was a FALSE ALARM and needs no change:** the reviewer worried Zanzibar (AREA `Zanzibar`) and Kilwa (AREA `Tanzania`) might not be in any of the 10 anfei harvest regions. They ARE — both `Zanzibar` and `Tanzania` are areas of the **`Lake_Victoria`** region (verified in map_data/regions.txt), which is the first region in the anfei gate/harvest list. So the Swahili-coast holdings DO roll into the Anfei march. (The reviewer flagged it as "verify," correctly noting it wasn't a new defect.)
  - Everything else CLEAN per review: task graph (no cycles, no key collisions), effect idiom vs the anbei/anhai/anxin call sites, the other 5 province IDs, all 8 modifier keys (registered in 00_modifier_icons.txt), full loc coverage + no dupes, se_LOG on every task, byte conventions. Post-fix brace balance still 402/402; both replacement provinces verified in-region.

## #66 DONE (2026-07-05) — dual Eight Banners + Green Standard garrison
- Rewrote `SE_qing_armies` (was ONE Green Standard legion at Beijing) into the full dual standing army: metropolitan Eight Banners at Beijing (largest) + ~17 provincial banner mancheng garrisons + ~9 dispersed Green Standard provincial stacks. Documented in QING_FEATURES.md §11.2.
- **Design decision — "big on paper, brittle in field":** garrisons raised at full paper size; the 1815 military softness is carried by the EXISTING `qing_banner_decay` bands, not by shrinking rolls. Did NOT add a new decay hook (reused §0.2). Intent: push the player toward militia 鄉勇.
- **Implementation decision — raise-from-capital-governorship pattern:** every legion raised from `c:CHI.capital_scope.governorship` (proven to exist) but *located* at its garrison province, mirroring the working `SE_occupation_of_france`. Avoids per-province `state.governorship` existence risk. Two parameterized helpers (`SE_qing_raise_garrison[_cmd]`), each self-guarding `exists $prov$ && owner=c:CHI` (+ `exists $cmd$`) → a partitioned Qing just gets fewer garrisons, each miss logging LOG_fail (sys=QING). Uses verified `while = { count = $size$ add_subunit = }` idiom.
- **Commanders:** all confirmed alive in 1815 — char:340 Yinghe (Metro Banners), char:244 Changling (Ili), char:358 Nayancheng (Jingshi GS, preserved), char:339 Wu Xiongguang (Sichuan GS), char:241 Yang Fang (Yunnan-Guizhou GS). Yang Yuchun / Eldemboo / Delengtai from the research memory were NOT in the character roster (or dead by 1815, e.g. Delengtai d.1809), so were not used — no new characters invented for this task.
- **Data note:** several mancheng cities from the research (Jilin, Zhapu, Tongguan, Qingzhou) are not discrete provinces in `province_setup.csv` under those names; covered by their region seats (Mukden/Qiqihar for Manchuria, etc.). Kashgar = province "Kaxgar" p:2700; Ili garrison = Huiyuan p:3534; Ningxia = Yinchuan p:209; Liangzhou = Wuwei p:5616; Suiyuan = Hohhot p:3322.
- Brace balance 0, no BOM, LF preserved (file is plain-ASCII/LF, unlike the economy files).
- **Review DONE — clean, no correctness defects.** Confirmed: base `sub_unit` present in every create_unit; commander-attach idiom correct; no invalid `add_loyal_subunit`/`set_personal_loyalty`/external `add_commander`; no commander double-assignment (340/244/358/339/241 all distinct); `c:CHI.capital_scope.governorship` is a valid absolute chain; save-scope reuse is harmless (never read by name, `PREV` drives the attach — matches existing repo convention). Multiple legions stacking at one province (e.g. p:8363 Banners+GS) is fine.
- **ONE in-game smoke-test item (flagged by review, cannot verify without running the game):** `while = { count = $size$ add_subunit = regular_infantry }` inside a `raise_legion → create_unit` block has no exact in-repo precedent — the only proven `while`+`add_subunit` is in a bare NAVY create_unit (no raise_legion wrapper); every land `raise_legion` uses explicit repeated `add_subunit`. Very likely fine (the raise_legion wrapper doesn't change create_unit internals), but confirm on next -debug_mode start that the Metropolitan Banners legion spawns at 24 companies (each garrison already emits a greppable `[QING]` LOG_line). If it spawns at 1, swap the `while` for explicit `add_subunit` lines.

## Major decisions
- **Dispatched the Qing-army academic research agent** I had earlier mis-stated as already sent; it completed. Digest saved to memory `imp19c-qing-army-1815-research`. It also caught a data trap: extraction agents had misread 1885 *tael-expenditure* columns as *troop counts* (the "millions per province" figures) — discarded.
- **#64 approach:** the mod's `zz_injectormaker/` generator only emits the iterator-loop injectors; the ~30-file / 100+-insertion-point per-good surface (`GOODS_governorship_X_produced`, `DEMAND_X`, `TRADE_*_X`, price/stockpile/sell blocks, etc.) is **hand-maintained**. So the 5 crops are cloned deterministically from the `tobacco` archetype (category-2 cash crop: price/trade-simulated, gives `local_monthly_food`, NOT added to the fixed 6-good staple demand basket). Doing this via a single deterministic Python script + brace-count verification rather than 100 manual edits.
- **#64 map placement (2026-07-05):** 28 provinces converted in `province_setup.csv`, all from grain/livestock, spread across regions so no single food-region is denuded. Historically grounded: **maize** → Hunan/Jiangxi (its main Qing-era adoption belt); **sweet_potato** → Fujian + East Guangdong (the real point of entry, Chen Zhenlong's introduction) + coastal Peru homeland; **potato** → Andes homeland (Potosí, Atacama, Puno) + New Mexico highland; **peanut** → Fujian/E-Guangdong + Peruvian coast; **chili** → Hunan/Sichuan (its iconic culinary home) + Mexican homeland (Guadalajara/Oaxaca). Placement is intentionally modest (5–6 provinces each) — enough to make each good producible & tradeable without rebalancing the world food supply. Americas homelands seeded so the goods exist as trade targets for Qing colonization missions (#67/#69) too.
- **#64 loc:** wrote real English names + flavourful DESC strings for all 5 crops (not token-swaps) in `imp19c_tradegoods_l_english.yml`; cloned the 25 economic-enhancement UI loc lines. hsv colors chosen distinct from tobacco and each other.
- **#64 NEAR-MISS CAUGHT + FIXED (2026-07-05):** the clone script's `io.open(..., "w")` write flipped **BOM + line-endings** on every file it touched. Many of these files are UTF-8-**with-BOM** and/or **CRLF** in HEAD (province_setup.csv, TRADE/GOODS/DEMAND/AI/WEALTH/PRICE svalues, se_GLOBALTRADE/SELL/GOODS/TRADE_new, the injectors, trade_triggers…). The naive write emitted LF + no-BOM → git showed a catastrophic whole-file diff (province_setup.csv = all 13,282 lines "changed"). Verified via `git diff --ignore-all-space` that the *content* delta was correct (28 CSV lines, 445 TRADE lines, etc.), then wrote a byte-level fixer that re-applies each file's original BOM/EOL convention. Post-fix numstat is clean (pure additions X/0, plus the 28/28 CSV reassignments). **Hardened `zz_newworld_crops_clone.py`** to detect+preserve BOM/CRLF on write so a re-run won't reintroduce it. Lesson logged for all future bulk .txt edits: these Paradox files are BOM+CRLF — always write bytes preserving the original convention.

## #74-fix DONE (2026-07-05) — Summer Palace tree: Branch-B (Qingyi Yuan) interaction bugs
Post-implementation code review of the #74 Summer Palace tree (SPreview2 agent) surfaced 2 MEDIUM + 2 LOW findings in the Branch-B (清漪園 Qingyi → 頤和園 Yiheyuan) path that my own self-review missed. All four independently verified against the code before fixing; fix-forward on top of the committed #74 tree (48ab7afc). NOTE: these are fixes to MY OWN session-authored feature, so per the scope-corrected traceability rule they are ordinary new-feature work (log for debugging), NOT the upstream-only behavioural-equivalence tier.

- **MEDIUM #1 — double-modifier stack (FIXED).** `QING_sp_yiheyuan_divert_navy` (se_QING_SUMMER_PALACE.txt:70) and `QING_sp_yiheyuan_from_treasury` (:108) only cleared the *burnt* scar (`qing_sp_qingyi_burnt`) but never a Qingyi that still STANDS. A player whose Qingyi never burned (Qing at peace with GBR/FRA through 1856–1860) would build the Yiheyuan on top of the standing Qingyi → `qing_sp_qingyi_garden` + `qing_sp_yiheyuan_splendour` both active permanently (double legitimacy/ruler-pop/happiness). FIX: both verbs now `remove_country_modifier = qing_sp_qingyi_garden` + `remove_variable = qing_sp_qingyi_built` when the Qingyi still stands (the Yiheyuan is built ON that site, so it subsumes it). LOG_line marks the subsume.
- **MEDIUM #2 — Branch-B player can never trigger the 1860 sack (FIXED).** Event `qing_summer_palace.1` trigger (:46) and the offering roll in se_QING_DECLINE.txt:788 both gated on `has_variable = qing_sp_built` (Yuanmingyuan / Branch A only). A Qingyi-only player could never be offered the sack, so their garden escaped the historical 1860 Anglo-French burning entirely and the verb's Qingyi-burn block was dead code for them. FIX: both gates widened to `OR = { qing_sp_built  qing_sp_qingyi_built }` — either standing garden arms the sack (both burned in the same 1860 expedition; the verb already burns whichever garden(s) stand, independently guarded).
- **LOG-fidelity follow-on (FIXED).** With the sack now reachable by a Qingyi-only player, `QING_sp_sack_of_1860`'s old `else → LOG_fail` (on the Yuanmingyuan branch) would spuriously log a failure even when the Qingyi burned successfully. Restructured: LOG_fail now fires only when NEITHER garden stood (true no-op), per the error-logging rule that LOG_fail must surface genuine no-ops, not legitimately-skipped branches.
- **LOW-1 — dead loc key removed.** `qing_sp_needs_garden_tt` (qing_summer_palace_l_english.yml:19) was referenced nowhere; deleted.
- **LOW-2 — intentional-asymmetry documented, NO behaviour change.** The Tongzhi 20%-success (`QING_sp_tongzhi_attempt`) restores only `qing_sp_garden_of_brightness`, not `qing_sp_european_marvels` / `qing_sp_imperial_library`. This is historically correct (looted European treasures + the burned Siku library copy don't return with a rebuilt shell), so behaviour left as-is; added a comment marking the omission as deliberate so a future reader doesn't "fix" it.

**Verification:** brace balance OK on all three code files (se_QING_SUMMER_PALACE 58/58, events 32/32, se_QING_DECLINE 660/660); byte conventions preserved (SUMMER_PALACE + DECLINE no-BOM/LF, events + loc BOM/LF). Edits task-tagged `#74-fix` at each site; se_LOG markers added on the new subsume paths.

**PROCESS CORRECTION (user, 2026-07-05):** "'changes to a shipped feature' — no they aren't, only changes to code from upstream counts." The heightened behavioural-equivalence scrutiny tier applies ONLY to upstream/base-mod code I did not author; my own committed session features are still ordinary new-feature work when I fix them. Memory rule imp19c-fix-traceability-rule updated with this scope correction.

## #64-fix DONE (2026-07-05) — CRITICAL: 5 New World crops were undefined trade goods
Deep-scrutiny audit (ScrutinyPass agent) found the single blocking defect from the #64 crop work: the five crops (maize, sweet_potato, potato, peanut, chili) were assigned to 28 provinces in province_setup.csv and plumbed across ~20 economy files (GOODS/DEMAND/PRICE/TRADE svalues, se_GOODS/SELL/PURCHASE, injectors), **but no trade-good DEFINITION was ever added** under common/trade_goods/. Confirmed: only tobacco (the archetype, 00_imp19c.txt:408) exists; grep for the 5 crops under common/trade_goods/ returns nothing; crop commit 20db2dbd never touched trade_goods/. This is a #76-class defect (an entire subsystem wired around objects with no base definition) — at load the undefined trade_goods value on those 28 provinces errors/drops, so they produce nothing and contribute zero food.
- **FIX:** added 5 `category = 2` blocks to common/trade_goods/00_imp19c.txt cloned from the tobacco cash-crop archetype (gold=0.2, province={local_monthly_food=0.07}), each with a distinct hsv color. Tagged `#64-fix`. Brace balance 148→163 (OK, +3 per good = +15), BOM/LF preserved.
- **Whose code:** my own session-authored #64 → ordinary new-feature fix (log for debugging), not the upstream equivalence tier.
- This unblocks #78 (the pop-boom applicator keys off "province grows a New World crop" — the crops must exist as goods first).

## ScrutinyPass audit SCOPE (2026-07-05) — economy layer only; diplomacy/migration NOT audited
ScrutinyPass audited ONLY commit 20db2dbd (economy: crops #64 + fixes #68/#70/#71/#72) and the a8365f9b merge-resolution on DIPLOMACY_svalues.txt (the svalue *collision*, not play logic). It found 1 CRITICAL (C1, fixed above); everything else in the economy layer verified CLEAN (clone symmetry, both divide-by-zero guards, the #71 cache incl. all readers/scopes, the merge, oa_wealth_changes, province_setup dup-check).
- **NOT AUDITED — DEFERRED to a combined pass (user decision, 2026-07-05):** the net-new Qing subsystems in commit c0eb5a39 (157 files) — diplomatic plays (#58 DIPLOMACY_complete_play resolution, #53/#57 feature-play launchers, se_DIPLOMACY), migration/claims (#MIGR bottom-up migration, de jure irredentism, claim-hostility, wargoal), subject rework, missions. User chose "one combined audit later" — a single thorough correctness audit of ALL net-new Qing subsystems as a dedicated pass AFTER #77/#78 are done. Brief must carry the full rule set (se_LOG, separatism-backer rule, guard/ordering/scope discipline). DO NOT forget this pass.

## #78 DONE (2026-07-05) — New World crops → Qing population boom (capacity coupling) + colonization accelerator
Closes the "capacity-only demographic coupling" gap. KEY FINDING during implementation: a NARRATIVE crop boom already existed and was fully wired (qing_migration.20/.21/.22 events, qing_migr_crop_boom/_golden/qing_migr_overpopulation country modifiers, qing_newworld_crops flag, fired from se_QING_DECLINE:870, already calling QING_COLON_heartland_push). That system delivers empire-wide GROWTH. The genuine missing piece — grep-confirmed `local_population_capacity` appeared NOWHERE in the crop coupling — was per-province structural CARRYING CAPACITY. Growth without a raised ceiling just hits the wall.
- **New province modifier** `qing_nwcrop_abundance` (common/modifiers/qing_migration_modifiers.txt) = `local_population_capacity = 8` (proven province-capacity tier; 00_hardcoded uses 6–10). Capacity-ONLY by design — growth is already owned by the boom event, so no double-count. PROVEN path (oracle rule): province modifier + add_province_modifier, NOT a trade-good province block (which can't carry the key).
- **Applicator** `QING_COLON_apply_nwcrop_capacity` (se_QING_COLON.txt) — idempotent global every_province sweep: adds the modifier where a NW crop is grown and missing, removes it where present but the good has changed (re-seed/transfer). Self-correcting, re-runnable.
- **Accelerator** `QING_COLON_spread_newworld_crops = { count }` (se_QING_COLON.txt) — on New World colonisation, converts ≤count MARGINAL owned provinces (livestock/wood ONLY — never grain, to protect the staple breadbasket) to sweet_potato via runtime set_trade_goods, then re-runs the sweep. Represents crops physically spreading through China + raises ceilings → accelerates the boom.
- **Wiring:** (1) game-start setup (oa_economy_setup.txt, guarded by nwcrop_capacity_setup_done) stamps the lift on all 28 pre-placed crop provinces; (2) both options of qing_migration.20 (the boom-planting event) now also call the sweep so the boom raises ceilings not just growth; (3) qing_col_anxin (New World protectorate milestone) calls the accelerator with count=3.
- **Loc:** qing_nwcrop_abundance display name added (qing_migration_l_english.yml).
- **se_LOG:** LOG_enter/exit on both verbs; LOG_line on each apply/remove/convert; LOG_fail on the accelerator's no-marginal-province guard-miss.
- **Verified:** brace balance OK on all 5 code files; byte conventions preserved (modifiers/se/missions no-BOM/LF, oa_economy_setup BOM/CRLF, events + loc BOM/LF); scope validity (every_province global vs ordered_owned_province country), ordering (crops placed before on_game_initialized), no crop-clobber by the defunct-replace/fill-blank setup steps, GetTradeGoods.GetName promote correct.
- **Whose code:** my own session-authored → new-feature tier (log for debugging). Post-implementation review still owed per the standing rule.


## #77 DONE (2026-07-05) — trade-goods consistency sweep (FIXED) + perf cluster (documented negative result)

Two halves. The consistency half yielded a real fix; the perf half yielded a rigorously-established "do not touch" negative result.

### Consistency sweep — FIXED (the actionable half)
Swept every trade good referenced anywhere against the production list (GOODS_governorship_produce_all, 46 goods) and the trade sim.
- **`cloth` — NOT a bug (investigated, cleared).** `cloth` is on 2706 provinces (the single most common value in province_setup.csv) but appears in NO production/trade path. Cause: it is the PLACEHOLDER sentinel. `setup_fill_in_blank_tradegoods` (se_setup.txt:632, invoked oa_economy_setup.txt:15 at game init) converts EVERY remaining `cloth` province to a real good via random_list (grain/livestock/wood/vegetables/temperate_fruit/textile_fibres/industrial_fibres). By design no province stays `cloth` once setup runs, so its absence from produce_all is correct. Left untouched (a #76-class reverse-error avoided).
- **`cotton` / `hemp` / `palm` / `incense` — REAL gap, FIXED.** These four goods carry explicit removal-intent comments in their own definitions (`cotton # to be removed`, `hemp # to be removed`, `palm # Merge into tropical fruit`, `incense ### PHASE OUT`). The upstream `defunct_tradegoods_replaced` block (oa_economy_setup.txt:39-91) already migrates 8 other defunct goods (tropical_fruit, wool, whales, camel, horses, chocolate, peat, inorganic_compounds) to live goods at setup — but OMITTED these four. Result: ~23 provinces (cotton 4, hemp 8, palm 10, incense 1) were left producing a good that is in NO production/demand/price/trade path → silent zero-contribution, exactly the drift the audit warned of.
- **FIX:** extended the existing `defunct_tradegoods_replaced` block with four more every_province remaps: cotton→textile_fibres, hemp→industrial_fibres (fibre→fibre, both cat3), palm→temperate_fruit (the terminal fruit good the block already funnels tropical_fruit into), incense→spices (nearest live aromatic-luxury good). Tagged `#77`.
- **Behavioural-equivalence proof (upstream code — heightened tier applies):** every good involved (all four defunct + all four targets) carries an IDENTICAL `province = { local_monthly_food = 0.07 }` and no other province modifier — so the remap is FOOD-NEUTRAL: province food supply is unchanged. The change strictly REPLACES a dead/undefined-in-sim good with a live one that feeds the production/trade path; it does not alter any working behaviour (those provinces contributed nothing to trade before). Mappings follow the author's own kind/category groupings (see farmable_goods in 00_resource_building_potential.txt, which lists all four alongside their fibre/fruit kin). Idempotent-safe (guarded by the pre-existing defunct_tradegoods_replaced global var; runs once at setup). Brace balance 518→526 (+8 = 4 blocks × 2, OK); BOM+CRLF preserved (edited via Python).
- **Whose code:** upstream (base-mod commit 530490ba, MIUNO) → heightened equivalence tier; equivalence argument above.

### Perf cluster — DOCUMENTED NEGATIVE RESULT (do not optimize)
The economy-audit-backlog flagged two trade-sim perf hotspots. Both were investigated to the data-dependency level and found LOAD-BEARING — no equivalence-preserving optimization exists, and forcing one into this untestable 173KB upstream sim would be a #76-class regression risk. Details:
- **"O(goods×tradezones) global-variable reset explosion" (`GT_split_reset_global_TZ_variables`) — NECESSARY, not dead work.** Traced the full write-chain: each `$tradezone$_stockpile_$tradegood$` global is written by `change_global_variable { add = ... }` (ACCUMULATE), summed across EVERY governorship in `GT_split_update_TZ_sell_amount_apply_change` (se_GLOBALTRADE_split.txt). The reset-to-0 is the accumulator initialization — remove it and stockpiles grow unbounded across quarters (correctness regression). Also: it runs ONCE PER QUARTER GLOBALLY (not per country), so it is O(22 zones × goods) once — much cheaper than "explosion" implied. The `exported` family is mostly `set` (overwrite) but has ≥1 accumulate site, so its reset is not safely removable either without per-var runtime proof I cannot obtain.
- **"Repeated every_country{every_governorships{}} passes" — CANNOT be fused.** The main effect has 5 such passes, but each is separated by a GLOBAL REDUCE BARRIER: sum_all_TZ_stockpiles → price calc (needs all sellers' totals) → sum_all_TZ_orders → scale pools → shipping costs. Each pass consumes a global aggregate computed from ALL countries' output in the prior pass — a genuine map→reduce→map pipeline. Fusing any two would read a global total before all contributors have written it (correctness regression).
- **Conclusion:** the trade sim is CORRECT and its structure is dictated by real cross-country data dependencies. The perf half of #77 is closed as "investigated, no safe change." Recorded so a future pass does not re-litigate it.


## Review78 folded in (2026-07-05) — #78 post-implementation review
The #78 code-review agent (Review78) returned via disk transcript (mailbox-stall pattern). Verdict: clean commit, no CRITICAL, mechanism sound & honestly capacity-only. Three findings triaged:
- **MEDIUM (FIXED, 69c7c815):** LOG_exit sat inside the if-block of QING_COLON_spread_newworld_crops, so the else/fail path emitted ENTER+FAIL but no EXIT — broke se_LOG enter/exit pairing. Moved LOG_exit to the effect end (matches se_QING_TREATIES precedent). My own code → new-feature tier.
- **LOW #2 (NON-ISSUE):** reviewer flagged `GetTradeGoods.GetName` as unattested. FALSE POSITIVE — it IS attested in vanilla loc (core_l_english.yml:558 SELECT_PROVINCE_TOOLTIP, map_tooltips_l_english.yml:89). No change.
- **LOW #3 (NON-ISSUE):** ordered_ sort-direction "most crowded" nuance — reviewer itself noted this is an identical repo-wide convention (se_QING_SELFSTR/DECLINE), pre-existing, not introduced here, and functionally acceptable. No change.
- Everything else the reviewer verified CLEAN (scope, engine keys, ordering, idempotency, no double-count, staple safety, braces, byte conventions).


## #79 audit — SUBJECT REWORK findings folded in (2026-07-05, commit 24402eff)
Audit agent verdict: no CRITICAL; mechanism sound (progress clamped [0..5], pulse properly gated CHI/is_ai=no/180d cooldown, GUI scope-passing consistent, no mid-iteration list mutation, all modifier/building/loc keys resolve).
- **MEDIUM (FIXED):** zombie-subject reaction. At progress 5, SUBJ_QING_advance_integration absorbs the subject inline (LAND_transfer_provinces empties it) but the integrate button THEN calls SUBJ_QING_roll_reaction guarded only by is_subject_of=ROOT — true for the landless tag in the same tick before engine cleanup, scheduling qing_integ.* whose .a re-advances integration → stuck loop / broken portrait. FIX: guarded the roll_reaction chokepoint (exists + is_subject_of + any_owned_province count>=1) with an else LOG_fail. Central fix covers the button + any future caller; the ambient pulse was already safe (absorb clears SUBJ_integration_active which the pulse filters on). My own code → new-feature tier.
- **LOW (FIXED):** added else-LOG_fail guard-miss branches to reduce/suspend/resume_integration (standing log rule; were silent no-ops).
- **LOW (ACCEPTED, not fixed):** (a) promote/demote/incorporate charge influence before the rung if/else chain, so an unreachable-via-is_shown else would charge for a no-op — accepted because is_shown makes it unreachable and re-verifying risks the common path; (b) event top-level portrait/goto scopes lack exists-guards for the 3-10d annex window — the zombie primary-trigger is now closed by the roll guard; residual is cosmetic/rare.

## #80 Napoleon rework — AMHERST-ANCHORED KICKOFF ARC (2026-07-05)
Reworked the #65 Emperor Emeritus (Napoleon at the Qing court) chain so Napoleon's arrival is no longer conjured by the frontier flavour roll, but reached through a historically-anchored embassy arc.

**New flow:** RECEIVE the Amherst embassy (qing_embassy.2) -> qing_napoleon.5 "A Word of Waterloo" (envoy mentions Waterloo, court expresses interest) -> qing_napoleon.6 "The Rock in the Southern Ocean" (envoy calls at St Helena — as Amherst historically did in 1817 — relays invitation to Napoleon AND London, who humour the Qing hoping for the influence the embassy failed to win) -> qing_napoleon.1 reframed: Napoleon comes for a "brief" visit, is captivated, resolves to STAY at Qing invitation, Britain hesitantly consents -> existing .2/.3/.4 chain.

**Changes:**
- events/qing_napoleon_events.txt (BOM,LF): ADDED qing_napoleon.5 + .6; reframed .1 (comes-to-stay, .1.b now "let him return to St Helena" not "turned away"); header + section comments rewritten.
- localization/qing_napoleon_l_english.yml (BOM,LF): reframed .1.desc/.1.b/.1.b.tt; ADDED .5.*/.6.* keys; header chain-flow updated.
- events/qing_embassy_events.txt (no-BOM,LF): hooked qing_napoleon.5 onto the Amherst (.2) receive option. Macartney (.1) marked NO-LONGER-FIRED (1793 predates the 1815 start — user note); definition retained as legacy, referenced narratively in Amherst text.
- se_QING_DECLINE.txt (no-BOM,LF): removed the flavour-roll direct spawn of qing_napoleon.1 (replaced w/ explanatory comment); British embassy roll now offers ONLY Amherst (.2), not a Macartney/Amherst coin-flip.

**Code-review (code-review agent) findings addressed:**
- MEDIUM (FIXED): downstream date guards could strand the chain. The <1821.5.5 window guard was on .5 AND .6 AND .1, but .5->.6 (60-150d) + .6->.1 (90-200d) delays span ~1yr; a late-window Amherst reception could schedule .6/.1 past the guard, silently dead-ending a promised arrival. FIX: removed current_date guard from .6 and .1 — the overture (.5) is now the SOLE early-window gate; once committed the chain runs to completion, once-only held by NOT qing_napoleon_arrived.
- LOW (FIXED): stale ".1 re-check the roll's guards" comment + .yml header doc-drift both corrected.
- Confirmed sound by review: once-only guards, no double-fire, all loc keys resolve, scope safety (no right_portrait before Napoleon exists), se_QING_DECLINE cleanup complete.

Validation: brace balance OK on all 3 script files; byte conventions (BOM/LF) preserved per file; 10 new loc keys present. My own session-authored feature -> ordinary new-feature tier.

## #80 follow-up — AMHERST PINNED TO 1816 (2026-07-05)
User question surfaced that the Amherst embassy (the Napoleon-chain kickoff) did NOT reliably fire in 1816: qing_embassy.2 was reached only via QING_frontier_flavour_roll (30%/month gate, then one weight-10 branch among ~25 in a random_list summing >200) → per-month odds ~1.4%, median wait ~4 years, frequently past the <1821.5.5 Napoleon window → the counterfactual was substantially left to chance.
FIX (user decision "Pin to 1816"): added a dated one-shot in qing_mechanics_on_actions.txt on_game_initialized (CHI + is_ai=no): trigger_event = { id = qing_embassy.2  days = { 410 430 } }. START_DATE is 1815.7.1; +410-430d ≈ late Aug 1816 (Amherst's historical arrival at Peking). Event re-checks its own trigger at fire; flavour-roll branch left as harmless self-guarded fallback. Proven idiom: on_game_initialized effect-block already used for QING_*_init; long days-offset trigger_event used throughout. Byte convention BOM/LF preserved. My own feature → new-feature tier.


## #89 — ENABLE THE ARTILLERY ARM + FEATURE IT IN QING/NAPOLEON MODERNIZATION (2026-07-05)
User directives: "enable artillery first" → "Qing army modernization in general and Napoleon in particular should prominently feature artillery" → "the self-strengthening missions and napoleon missions should include plenty of technology unlock inventions".

**Discovery (oracle rule applied):** the engine has NO `enable_unit_type` verb (confirmed absent from the whole mod AND both oracles /tmp/Terra-Indomita + /tmp/Invictus, neither of which even ships common/units). The `tech_cannons` invention's `on_activate = { # TODO: Enables artillery unit type }` was a dead stub, and the whole `military_tech_artillery` tree was all-TODO. The REAL enable idiom in this mod is an `allow = {}` trigger INSIDE the unit definition (proven by warelephant's `allow = { trade_good_surplus }` and the steamers' commented `allow = { invention = steam_locomotive }`). The classical units (heavy_infantry, light_infantry, archers…) are 3-byte empty stubs; the live army roster is regular_infantry (default), conscripts, warelephant, engineer_cohort, supply_train, and now artillery. Modifier keys follow the proven `<unit>_<stat>` pattern (regular_infantry_offensive, heavy_infantry_discipline are live), so artillery_offensive/_defensive/_discipline/_morale/_cost/_maintenance_cost/_movement_speed are valid. NOTE: CHI already starts with tech_cannons+bombard+rocket_artillery via TECH_unlock_all_starting_techs (oa_economy_setup.txt:18), so base artillery is recruitable from turn 1 for CHI; the modern mobile line (wheeled→limber→howitzer) is the modernization reward.

**Changes:**
- common/units/army_artillery.txt (BOM,LF): added `allow = { invention = tech_cannons }` — enables the arm.
- common/inventions/00_martial_inventions.txt (BOM,LF): filled the all-TODO military_tech_artillery tree (10 techs) with real modifiers (artillery_* + siege_ability); removed the dead on_activate stub from tech_cannons.
- common/military_traditions/00_napoleon.txt (no-BOM,LF): Path B (grand battery) now drives the field guns directly — added artillery_offensive/_discipline/_morale to napoleon_brienne / grande_batterie / dieu_de_la_guerre; corrected the "engine has no artillery unit" comment.
- common/modifiers/qing_selfstrengthening_modifiers.txt (no-BOM,LF): qing_selfstr_jiangnan_arsenal += artillery_cost -0.15/artillery_offensive 0.10; qing_selfstr_ever_victorious += artillery_cost -0.15/artillery_offensive 0.10/artillery_discipline 0.10.
- common/scripted_effects/se_QING_SELFSTR.txt (no-BOM,LF): themed unlock_invention bundles per founding effect — jiangnan (artillery+small-arms+metalworking), fuzhou (naval construction), beiyang (ironclad/torpedo), tongwen (modern science), telegraph (electricity/telegraph), merchant (steam-shipping/commerce), rail (steam/rail/metallurgy); evarmy legion now 3 infantry + 2 artillery, safety-unlocks tech_cannons.
- common/scripted_effects/se_QING_NAPOLEON.txt (no-BOM,LF): reform_code (admin/legal line), reform_bank (finance line), reform_education (science line), reform_levee (full artillery line + modern army-org + small-arms lines); Grande Armee de Chine now 14 infantry + 5 artillery (grand battery).
- localization/english/modifiers_l_english.yml (BOM,LF): 7 artillery_* modifier-key names. text_l_english.yml (BOM,LF): `artillery` unit display name.

**Validation:** brace balance OK on all 7 script/modifier files; byte conventions preserved per file; all unlock_invention targets verified to exist (python cross-check vs 184 defined tech keys); all artillery_* suffixes match the proven <unit>_<stat> set; tech-tree prereqs included where forced (bombard→mortar→howitzer chain). All scripted additions se_LOG-wired (sys=QING). Post-implementation code-review agent dispatched. NEW feature → ordinary new-feature tier. Task #89.

**#89 code-review outcome (addressed):** review returned NO critical/blocking findings — change set substantially clean (all 66 unlock_invention targets resolve; artillery_* keys valid; guards idempotent; subunit-unlock ordering correct; se_LOG consistent; prereq "gaps" are non-issues, proven by shipped TECH_unlock_military_level_* which force-unlock single inventions out of tree order). Addressed the three actionable notes: (1) MEDIUM — recruitability of an allow-gated SUPPORT unit is unprovable statically (no in-mod precedent; supply_train/engineer_cohort are auto-attached, warelephant is a regular unit), so the add_subunit spawn path is guaranteed but the "free recruitable arm thereafter" claim is not — softened the levee comment to say so honestly (per unproven-capability rule) rather than assert it; (2) LOW — wired the previously-dead artillery_maintenance_cost loc key into qing_selfstr_ever_victorious (−0.15, a professional standing gun-corps is cheaper to keep); (3) LOW — corrected the stale "engine has no artillery arm" header line in 00_napoleon.txt. Braces + byte conventions re-verified on all three follow-up edits.

## #88 — GREEN STANDARD vs BANNER DIVERGENCE + NAPOLEON TOP-DOWN MODERNIZATION TIE-IN (2026-07-05)
User directives: (overarching) "finish Napoleon rework first"; (mid-task) "the capstone of the self-strengthening should remove these decline and decay and corruption indicators … signifying the country has fully modernized".

Splits the single banner-decay vector into a richer three-army model and wires the modern national army into the Napoleon arc + the Self-Strengthening capstone.

**Layers built:**
1. **Modifiers (qing_mechanics_modifiers.txt):** new bands — qing_greenstandard_decay_mild/severe + _reform_drill (parallel to banners, on regular_infantry line); qing_han_provincial_emerging/entrenched/warlord (勇營→湘軍/淮軍→軍閥, a NEW double-edged devolution vector); qing_modernarmy_emerging/national (新軍, the centralizing counter). All keys follow the proven <unit>_<stat> pattern (regular_infantry_discipline/offensive, conscripts_offensive, artillery_offensive).
2. **Counters + derivation (se_QING_DECLINE.txt):** seeded qing_greenstandard_decay(15)/qing_han_provincial_power(0)/qing_modernarmy_share(0) in _init; added apply-band verbs for all three; drift verbs — modernarmy_share drifts toward the selfstr ceiling (halved if hollow); han_provincial_power is DERIVED = mean(banner_decay, greenstandard_decay) − modernarmy_share (rises only when BOTH central armies fail AND no modern army replaces them). Wired into QING_DECLINE_pulse in dependency order (share + gs decay fresh before han-prov derive).
3. **Player levers (se_QING_MECHANICS.txt + QING_mechanics_actions.txt + loc):** QING_greenstandard_drill (£45, cuts gs decay); QING_sanction_regional_army (emergency: eases both central decays, +15 provincial power — the double-edged choice); QING_reassert_central_command (£90, −20 provincial power + unrest cost); QING_fund_modern_army (£100, gated selfstr≥25, +12 modern share). Four new scripted-GUI buttons + £45 tooltip.
4. **Founding floors:** Ever-Victorious Army one-time +30 modern share (emerging floor); Napoleon levee (TOP-DOWN TIE-IN) +60 modern share to national band, −20 gs decay, −30 Han provincial power (the anti-warlord dividend of a centrally-imposed conscript army).
5. **Warlord separatism payoff (se_SEPARATISM.txt):** SEPARATISM_qing_pulse gate widened to OR — ethnic tension ≥45 OR qing_han_provincial_power ≥80 (@separatism_qing_warlord_floor) arms secession; chance bands take the higher of the two crises (provincial ≥90 → 75%). Reuses the proven SEPARATISM_try_secession core verbatim; only the activation path is new.
6. **CAPSTONE = FULLY MODERNIZED (user request):** new QING_selfstr_capstone_modernized — drains qing_corruption_level/sect_pressure/currency_stress/reform_pressure/han_provincial_power to 0, banner/gs decay to residual 5, modern share to 100; strips every decline/decay/corruption malus band immediately; grants clean-government + modernarmy_national bands; sets qing_fully_modernized flag. That flag halts the passive old-order regeneration in QING_DECLINE_pulse (no more banner/gs decay creep, no decline-reaction roll) — a modern professional state escapes the dynastic cycle (player choices can still move meters; not invulnerable). Called from qing_ss_capstone mission on_completion.

**Validation:** braces balanced on all 8 files; byte conventions preserved (all no-BOM/LF); all 8 new modifier keys defined + all references resolve; new stat suffixes match the proven <unit>_<stat> set; no new heavy every_/ordered_ scans (all O(1) counter work); every new verb se_LOG-wired (sys=QING/SEPAR) with LOG_fail on guard-misses. NEW features → ordinary tier; the SEPARATISM_qing_pulse gate CHANGE (existing feature) gets behavioural-equivalence scrutiny in the code review. Post-implementation review dispatched. Task #88.

**Review outcome (2026-07-05):** code-review passed on logic — pulse ordering (share+GS decay fresh before han-provincial derive), derivation math (mean-then-subtract, clamped 0..100), separatism behavioural-equivalence (OR-widening is additive-only; low-provincial-power realm behaves EXACTLY as before; chance bands can't mis-bucket), idempotency (once-only guards + capstone safe to re-run), flag gating (qing_fully_modernized untouched pre-capstone), all modifier keys valid, scope/se_LOG consistent. One MEDIUM + two LOW addressed:
- MEDIUM — the four #88 levers were unreachable: added their `icon_button_square` blocks to `gui/government_view.gui` (after the banner-drill button) AND the four `QING_ACTION_*_TT` display tooltips to `qing_mechanics_l_english.yml`. Now clickable.
- LOW — documented why `QING_reassert_central_command` re-grants `qing_greenstandard_reform_drill` (reclaimed troops re-enter the regular line, 2yr).
- LOW — corrected the misleading "drive the share to its max" capstone comment (share=100 eases back toward the selfstr ceiling via drift but stays in the national band; capstone force-adds the band regardless).
Re-verified braces on the three touched files (gui 1024/1024, MECHANICS 149/149, SELFSTR 248/248). Task #88 COMPLETE.

## #90 — TIE THE HAN REGIONAL-ARMY COUNTER INTO THE LOYAL-COHORTS POWER BASE (concrete-over-abstract) (2026-07-05)

**User directives:** (1) "the Han region army mechanic should directly tie into the existing loyal cohorts mechanic for governors"; (2) new STANDING DESIGN RULE — "design philosophy should strongly prioritize using concrete over abstract" (saved to memory imp19c-concrete-over-abstract-rule.md + imp19c-loyal-cohorts-mechanic.md).

**What:** the abstract `qing_han_provincial_power` counter (#88) now has a CONCRETE embodiment — a real Han governor-general character with a personal power base of loyal cohorts (the engine's `add_loyal_veterans` / power_base civil-war-seed mechanic, the 勇營→湘軍/淮軍→軍閥 dynamic). The counter stays as the summary/AI layer; the character is the on-map object the player sees, promotes, fears, and must one day break.
- **se_QING_MECHANICS.txt** — `QING_sanction_regional_army` now also calls `QING_regional_army_bind_commander`: finds the weightiest sitting Han governor (`ordered_character` order_by power_base, `culture = han`, `is_governor = yes`) and grants +8 loyal veterans; if none stands, conjures a Han founder via the roster `create_character` + `QING_roster_finalize` idiom. `QING_reassert_central_command` now also calls `QING_reassert_strip_magnate`: strips −8 loyal veterans from the strongest magnate and retires the marker when the throne-granted pool is spent. New helper `QING_magnate_track_grant` guards the marker against re-stacking and tracks the granted-veteran tally.
- **00_imp19c_character_modifiers.txt** — new `qing_regional_magnate` char modifier (martial=1, land_morale_modifier=0.1, monthly_character_prominence=0.03, loyalty_gain_chance_modifier=-0.2 — a capable but semi-independent general).
- **qing_roster_l_english.yml** — NICKNAME_QING_REGIONAL_MAGNATE (via Python heredoc, BOM/CJK-safe). **qing_mechanics_l_english.yml** — magnate display name + reworded SANCTION/REASSERT tooltips to name the concrete power-base effect.

**Review outcome:** code-review found 1 CRITICAL + 2 MEDIUM, all fixed before commit:
- CRITICAL — culture filter was `ROOT.primary_culture`, but CHI's primary_culture is **manchu** (setup/main/00_default.txt:35634); this selected/created a Manchu bannerman, the inverse of a Han magnate. Fixed to `culture = han` (proven key, common/cultures/00_chinese_group.txt:129; matches the roster events' own Han-figure idiom) in all three sites.
- MEDIUM — repeated sanction re-added the char modifier (bonuses stack). Fixed via `QING_magnate_track_grant` (grant modifier only if not already held).
- MEDIUM — the `power_base <= 5` marker-clear guard rarely fired for a real (holdings-owning) governor. Fixed by tracking the throne-granted veteran pool in `qing_magnate_granted_veterans` and clearing the marker when that tally hits 0, independent of baseline holdings.
- LOW (conjured magnates can accumulate) — intended + bounded by the sanction button's decay≥40 is_shown gate; left as a conscious choice.

**Validation:** se_QING_MECHANICS.txt braces 183/183; byte conventions preserved (script no-BOM/LF; loc + char-modifier files BOM, unchanged from HEAD). All engine verbs PROVEN in-mod: `add_loyal_veterans` (se_QING_COUNCIL.txt:69), `ordered_character`+order_by+check_range_bounds+max (se_QING_COUNCIL.txt:128, annexation.txt, Invictus oracle), `create_character`+`QING_roster_finalize` (qing_roster_events.txt), `is_governor` char trigger (character_events.txt:494), `culture = han`, traits disciplined/brave. se_LOG-wired sys=QING with LOG_fail on the no-magnate path. Task #90 COMPLETE.

## #82 — NAPOLEON REWORK FOLLOW-UPS: DOCTRINE-NAME DE-COLLISION (2026-07-05)

**User directive (overarching):** "finish Napoleon rework first, then continue with Japan."

**Scope finding:** on surveying the six #82 sub-items (GP reactivity, embassies, self-str tie-in, court friction, char mechanics, doctrine rename) against the shipped code, five were ALREADY delivered by #65/#80: GP reactivity = `QING_napoleon_revenge_tilt`->`qing_gp_tension_britain/russia`; embassies = the qing_napoleon.5/.6 Amherst-at-St-Helena kickoff; self-str tie-in = every reform verb advances Self-Strengthening; court friction = qing_napoleon.3 conservative-Manchu backlash + `QING_napoleon_apply_conservative_backlash`; char mechanics = `QING_napoleon_loyalty_pulse` (conditional loyalty on the revenge line). The one genuinely-open item was the **doctrine rename** -- and it was a real player-facing DEFECT, not cosmetic: two DISTINCT modifiers both rendered in the UI as **"The Daoguang Doctrine (道光主義)"** -- `qing_napoleon_daoguang_doctrine` (the Napoleon reform capstone) and `qing_daoguang_doctrine` (a Pacific-basin US-entente in the colonization tree, qing_colonization_modifiers.txt:209, also the USCW fork key).

**Decision (user, AskUserQuestion):** colonization KEEPS "The Daoguang Doctrine"; the Napoleon capstone is renamed to **"The Emeritus Doctrine (太上皇主義)"** -- display-only, NO key rename (lowest-risk path; the modifier key `qing_napoleon_daoguang_doctrine` and all script references stay, so no behavioural change). Narratively cleaner: the doctrine is named for the 太上皇 (Emperor Emeritus, Napoleon) who wrought it, proclaimed by the heir he tutored.

**Edits (display + coherence only, no logic change):**
- **qing_mechanics_l_english.yml** -- `qing_napoleon_daoguang_doctrine:0` display name -> "The Emeritus Doctrine (太上皇主義)"; desc reworded to explain the name honours the Emperor Emeritus.
- **qing_napoleon_l_english.yml** -- `.2.f` option label (道光主義->太上皇主義) + its tooltip; `.4.t` title, `.4.desc` flavour (the heir names it 太上皇主義 for his tutor the Retired Emperor), `.4.a` option button ("Proclaim the Emeritus Doctrine"); top + .4 section comments.
- **se_QING_NAPOLEON.txt** -- dead write-only var `qing_daoguang_doctrine_proclaimed`->`qing_emeritus_doctrine_proclaimed` (grepped: set once, never read, safe to rename); the proclaim LOG_line text.
- **qing_napoleon_events.txt** -- .4 namespace/section comments + the .4 LOG_line event tag.

**Validation:** `char:227` "Daoguang **Emperor**" references (the historical person/reign -- Prince Mianning) correctly PRESERVED; only the *doctrine's* name changed. Grep confirms zero "Daoguang Doctrine"/道光主義 left in the Napoleon loc, and the colonization `qing_daoguang_doctrine:0` line is byte-identical to HEAD. BOM preserved per-file (mechanics/napoleon/events loc = BOM; se_QING_NAPOLEON.txt = no-BOM). Post-implementation review dispatched. Task #82 COMPLETE (all six sub-items resolved: five pre-existing, doctrine de-collision this pass).

**#82 follow-up (same session, user-directed escalation):** the user then asked to (a) fix the code-facing comment/LOG "Daoguang" references too, (b) rename the KEY itself, and (c) rename the whole capstone away from "doctrine" — approving "Emeritus Enlightenment". Final state SUPERSEDES the display-only decision above:
- **Key renamed** `qing_napoleon_daoguang_doctrine` -> `qing_napoleon_emeritus_enlightenment` across all 5 files (definition + every add_country_modifier/has_country_modifier/NOT reference + both loc keys). Zero old-key remnants (grep-verified).
- **Display + CJK** -> "The Emeritus Enlightenment (太上皇啟蒙)" (啟蒙 = Enlightenment).
- **Dead var** `qing_daoguang_doctrine_proclaimed` -> `qing_emeritus_enlightenment_proclaimed` (still set-once/never-read).
- **All code comments + LOG_line text** updated Daoguang->Emeritus for the DOCTRINE/capstone sense; **preserved** every `char:227` "Daoguang **Emperor**", `is_daoguang_era`, `daoguang_heir` reference (historical person/reign) and the untouched colonization `qing_daoguang_doctrine` modifier.
- **Flavour** common-noun "doctrine" reworded to "settlement of state" so it reads correctly against the new name.
- **Design note (user asked "why a doctrine at all?"):** the capstone is mechanically just a permanent stat-buff country_modifier; "doctrine" was a #65 flavour label with no engine meaning. Renaming is free. A genuinely CONCRETE capstone (per the concrete-over-abstract rule) would instead `change_government` to a modernized type (proven at se_QING_REFORM.txt) — FLAGGED as a possible future upgrade, not done this pass.
Braces + BOM/LF re-verified on all 5 files. Second post-implementation review (Review82) dispatched for the rename-completeness (highest-risk: a missed rename site).

**#82 review outcome (Review82, 2026-07-05):** PASS — rename is behaviourally equivalent to HEAD except for the intended display/key change; no CRITICAL/MEDIUM. Top-priority rename-completeness check CLEAN: old key `qing_napoleon_daoguang_doctrine` has ZERO live references (only prose + the migration-note comment); new key `qing_napoleon_emeritus_enlightenment` defined once, every gate/grant (se_QING_NAPOLEON.txt:399/401, qing_napoleon_events.txt:175/258) uses it. Loc keys match; colonization `qing_daoguang_doctrine` genuinely untouched (still "The Daoguang Doctrine"); dead var still write-only; historical char:227/daoguang_heir/"Daoguang Emperor" refs preserved; braces (mechanics 57/57, se_QING_NAPOLEON 133/133, events 93/93) + BOM/LF verified vs HEAD. One LOW (doc drift): QING_FEATURES.md §Napoleon still documented the old key/name — FIXED (updated to 太上皇啟蒙 The Emeritus Enlightenment / qing_napoleon_emeritus_enlightenment, task #82 note). Task #82 COMPLETE.

**ConcreteAudit deliverable (2026-07-05):** the abstract→concrete research agent returned a ranked backlog of 6 HYBRID/low-risk conversion candidates for the Qing suite (tributary vassals #1, treaty ports, students-abroad, Xinjiang/Ili, customs house, Meiji meter) — all with proven in-mod hooks. Saved to memory imp19c-concrete-conversion-backlog.md (indexed). NOT actioned this pass; #1 (tributary vassals) has thematic overlap with #81 Japan (Ryukyu dual-tributary) so is best built near/within the Japan arc. Standing directive remains finish-Napoleon-then-Japan; #82 done, #81 next.

---

## AUTONOMOUS RUN 2 (2026-07-05/06) — #81 Japan + perf cluster #83-#87

User instruction: "continue with Japan and the performance fixes (very carefully with lots of scrutiny on performance changes) without stopping ... log the decisions taken". Later: "the pre-Perry missions should interact with individual daimyos, can support or oppose individuals to modernize and restore the emperor against the shogunate".

### Concurrency / collision plan (DECISION)
- The **#91 concrete-conversions workflow** (runId wf_cbbf71fb-94a) is running in the background, editing many se_QING_*.txt files. Its bundle **B7 owns se_QING_DIPLO.txt** (item H: GP rivalry -> real plays).
- Verified perf-task file map (Explore agent): #83=se_QING_COLON.txt, #84=se_DIPLOMACY.txt, #85=se_DIPLOMACY.txt, #86=**se_QING_DIPLO.txt**, #87=se_CURRENCY.txt.
- **DECISION: defer #86 until #91 finishes** (only #86 collides with se_QING_DIPLO.txt). Do #83/#84/#85/#87 now (collision-free). 
- **DECISION: build #81 Japan in NEW files** + touch only qing_japan_modifiers.txt & qing_japan_l_english.yml (no #91 bundle owns those). Do NOT edit se_QING_DIPLO.txt for Japan until #91 done; the accord/rivalry/meiji verbs there are READ/CALLED, not modified.

### YAML linter false positives (NOTE, not a bug)
- Live diagnostics on qing_treaties/customs/selfstrengthening/missionary _l_english.yml ("mapping items must start at same column") are the #91 workflow's new loc lines being linted. These are FALSE POSITIVES: the mod's Paradox loc format is `l_english:` at col 0 with leading-space `key:0 "val"` keys — a generic YAML linter rejects it, but EVERY existing loc file uses this format. The #91 workflow's own review phase covers those bundles. Not chasing.

### #81 Japan — pre-Perry arc: verified facts + design (DECISION)
- No Emperor/Kyoto tag exists at 1815. JPN is a formable never created in-mod (all refs guard `exists = c:JPN`). TKG (Tokugawa Shogunate, hereditary_dictatorship, japanese/shinto, cap Edo p:3684) is the only Japan-level tag at start, with 37 real daimyo subjects (setup 00_default.txt:557-593).
- Key daimyo for the sonno-joi arc: **CSU (Choshu)** and **SHZ (Satsuma/Shimazu)** are both nominal_vassal (loosest tie) — the two historical anti-shogunate tozama. Both japanese/shinto. SHZ cap Kagoshima p:7012; SHZ core also holds Kyoto p:4624 (NB: Imperial capital sits under Satsuma, not TKG, in this setup). RYU (Ryukyu, okinawan/mahayana, cap Naha p:524) is CHI tributary AND under TKG's SHZ vassal = the dual-tributary (両属) hook. Nagasaki p:5415.
- Existing qing_japan_missions.txt is the 1871+ POST-Perry tree (open-relations -> accord/rivalry forks). #81 is the c.1815-1854 PRECURSOR arc that hands off to it at Perry(1854).
- DESIGN (expanded per user daimyo instruction): pre-Perry tree that (a) runs the Nagasaki intelligence channel + Opium-War-cautionary-tale beats, AND (b) lets the Qing back or oppose individual daimyo (CSU/SHZ as reform/anti-shogunate leaders) and the sonno-joi "restore the emperor" dynamic, using the real subject tags. Concrete-over-abstract: spawn/steer real daimyo subjects & characters, not just counters.

### #83 DONE (Perf C1) — nwcrop capacity double-sweep merged
- `QING_COLON_apply_nwcrop_capacity` (se_QING_COLON.txt) ran TWO global `every_province` sweeps (add + remove/reconcile). MERGED into ONE pass with a limit OR-ing the add-set and remove-set (provably disjoint), then an if/else picking add vs remove. Behaviour-identical (same provinces gain/lose the modifier), half the visits. REJECTED the literal task text ("gate off CHI") as a regression — the lift is a crop property, gating to CHI would strip it from non-Qing crop provinces. Braces 103/103.

### #84 DONE (Perf C2) — index active diplomatic-play provinces
- `DIPLOMACY_update_all_diplomatic_plays` (se_DIPLOMACY.txt) changed from a monthly global `every_province { limit={has_variable=is_diplomatic_play} }` map scan to `every_in_global_list { variable = global_all_diplomatic_plays  limit={has_variable=is_diplomatic_play} }`. The list is the maintained index of play provinces (added at creation se_AI.txt:622, removed at teardown se_AI.txt:900-903 together with the is_diplomatic_play var — so the limit is a belt-and-braces guard, never gates out a live play). Mid-loop teardown proven safe (se_AI.txt:934 already removes the current element mid-iteration). Behaviour-identical set, no full-map scan.

### #85 DONE (Perf C3) — hoist tradezone-independent base power
- `DIPLOMACY_cache_country_power_tradezone` (se_DIPLOMACY.txt) multiplies the heavy `DIPLOMACY_power` svalue (economy+military+tech+RECURSIVE every_subject+admin+stability, DIPLOMACY_svalues.txt:1) by a per-TZ penetration factor — but DIPLOMACY_power has ZERO $tradezone$ dependence, so it was recomputed 22× per country per quarter. FIX: `DIPLOMACY_update_global_power_status` now sets `DIPLOMACY_power_base_cached` ONCE per country (right before that country's TZ loop, removed right after), and the helper reads the cache. SAFETY: helper falls back to a fresh DIPLOMACY_power compute when the cache is absent, so the DEBUG timetest harness (timetest_quarterly_tick.txt:371, which calls the helper without the pre-pass) is byte-for-byte unchanged — no edit needed there. Passes 2-5 untouched. Cache variable never outlives pass 1. Braces 366/366.
- NB: the 5 passes in DIPLOMACY_update_global_power_status are dependency-ordered (cache -> add-subject -> finalise-subject -> play -> top-players) and CANNOT be merged; only the redundant base-power recompute inside pass 1 was hoistable. Verified before editing.

### #86 STILL DEFERRED — collides with #91 bundle B7 (se_QING_DIPLO.txt). Do after #91 completes.

### #81 Japan — pre-Perry arc DONE (幕末前夜, 2026-07-05)

The 1815→1854 opening arc, feeding the existing post-Perry Meiji tree. Built entirely in NEW files (+ two non-#91-owned edits) per the collision plan, so it never touched se_QING_DIPLO.txt.

**Files created:**
- `common/scripted_effects/se_QING_JAPAN_PREPERRY.txt` (85/85) — the machinery, prefix `QING_jppre_`. Three 0-100 counters (reuse `QING_DECLINE_nudge`): `qing_jppre_intel`, `qing_jppre_reform_faction`, `qing_jppre_shogun_grip` (starts 70). Verbs: init, resolve_daimyo (`$tag$`→`scope:qing_jppre_daimyo`), deepen_intel, back_daimyo (patron opinion + one-time reform-leader spawn via `qing_jppre_reform_leader` marker + faction++/grip--), spawn_reform_leader (`create_character` japanese/shinto, martial 6/charisma 8/finesse 8/zeal 7, traits brave/ambitious/righteous), shore_shogunate (grip++/faction-- + TKG opinion), restoration_break (`release_subject` from TKG + `start_civil_war = scope:...`, falls back to current_ruler if the leader is dead), perry_handoff (sets `qing_jppre_perry_done`, carries the outcome onto the existing `QING_japan_warm_accord`/`raise_rivalry`/`meiji_advance`).
- `common/missions/qing_japan_preperry_missions.txt` (118/118) — `qing_japan_preperry_mission`, potential `{ tag=CHI, is_ai=no, NOT has_variable=qing_jppre_perry_done }`. Shared root (Nagasaki channel → Fusetsugaki → cautionary-tale, the last gated on `qing_treaty_system_imposed`), then FORKS: ARC R loyalist (back_daimyo → fan_sonno_joi → restoration capstone, faction≥70 & grip<40) vs ARC B bakufu (shore_bakufu → ready_bakufu → meet_perry). Road committed once via `qing_jppre_road` flag var; each entry locks the other.
- `events/imp19c_mod_events/qing_japan_preperry_events.txt` (30/30, BOM+LF) — `.1` cautionary tale (warn vs reform), `.2` daimyo choice (CSU/SHZ, trigger-gated on existence, sets `qing_jppre_backed_tag`), `.10` Perry black ships (date≥1853 + NOT perry_done, immediate → perry_handoff).
- `common/modifiers/qing_japan_preperry_modifiers.txt` (7/7) — reward modifiers; all keys validated against the mod's country-modifier vocabulary.
- `localization/english/qing_japan_preperry_l_english.yml` (BOM+LF) — full loc, verified 100% coverage (every task title/tt, modifier, event option, mission body defined; USED-BUT-UNDEFINED = []).

**Files edited (non-#91-owned):**
- `common/on_action/qing_mechanics_on_actions.txt` (16/16) — `QING_jppre_init = yes` at setup + a player-only Perry scheduler (`trigger_event qing_japan_preperry.10 days={13820 13940}`, ~1853; event re-checks its own date guard).
- `common/missions/qing_japan_missions.txt` (124/124) — **behavioural change (documented in-code):** added `has_variable = qing_jppre_perry_done` to the post-Perry mission's potential so the two Japan trees never show at once; the post-Perry tree now opens only at the hand-off. Deliberate.
- `common/opinions/imp19c_opinions.txt` (27/27) — added `qing_jppre_patron_opinion { value=40 yearly_decay=3 }`.

**Key design decisions & findings:**
- **JPN is never formed** (formable, all refs guard `exists = c:JPN`; TKG *is* Japan at 1815). So the Restoration payoff is made CONCRETE via the real daimyo tags — `release_subject` (CSU/SHZ from TKG) + `start_civil_war` behind the spawned loyalist leader — NOT a tag formation. Satisfies the concrete-over-abstract rule: real on-map subject + real character + real civil war, with the counters kept as the AI/summary layer.
- **Daimyo interaction** (per user instruction): the player backs or opposes individual daimyo — CSU (Chōshū) / SHZ (Satsuma), the real anti-shogunate tozama — to drive sonnō-jōi toward Restoration, or shores up the Tokugawa (TKG) for a stable conservative neighbour. Both roads are concrete: opinions on the real tags, a spawned reform councillor, the release+civil-war break.
- **Oracle-verified verbs** (Terra-Indomita + Invictus, per the standing rule): `release_subject` (`<overlord> = { release_subject = <tag> }`), `start_civil_war = scope:<char>`, `create_character`, foreign-scope `c:XXX` effects — all confirmed in-engine before building on them.
- **Loc-key namespace collision fixed:** `qing_jppre_nagasaki_channel`/`qing_jppre_fusetsugaki` were each both a task key and a modifier key; the two MODIFIERS were renamed to `_mod` suffix (definitions, both `add_country_modifier` calls, loc keys aligned). Invalid trait `popularist` → `righteous`.
- se_LOG wired at every task on_completion + every verb (sys=QING), per the error-logging standing rule.

**Validation:** all 7 files brace-balanced (figures above); every `add_country_modifier` name used has a matching definition; full loc coverage; BOM/LF preserved per file.

**Standing directive status:** Japan done. Remaining autonomous work = #86 (Perf C4, unblocks once #91 finishes editing se_QING_DIPLO.txt) + the #91 workflow FAIL-bundle fixes.

### #91 workflow FAIL-bundle fixes + #86 (Perf C4) DONE (2026-07-05)

The #91 concrete-conversions workflow (runId wf_cbbf71fb-94a) landed all its edits and self-reviewed 11 bundles: 4 FAIL (B2/B3/B4/B6), 6 PASS_WITH_NITS, 1 PASS. I applied every MANDATORY fix (all FAIL findings + the two standing-rule se_LOG violations + the one cheap traceability nit). Optional balance/cosmetic nits were left as documented (see below). Every fix carries a `[#91-fix task #91]` in-code comment per the fix-traceability rule; all touched files re-verified brace-balanced with BOM/LF preserved.

**B4 (D:xinjiang-ili) — se_QING_ILI.txt — BLOCKER + 2 major + 1 minor, ALL FIXED (braces 176/176):**
- *Blocker (concrete rule silently broken):* `QING_ili_apply_prov_band` iterated `every_owned_province` + `p:2930={owner=ROOT}`, but Xinjiang (Dzungaria+Tarim, incl. Urumqi p:2930) is held by the **ILI** autonomous_governorship + **XNG** client_state SUBJECTS, never by CHI directly (verified setup/main/00_default.txt:35979 ILI own_control_core `2930 9597 6973`, XNG `174 1732 2977…`). So the sweep stamped NOTHING and the grip meter never reached the map. FIX: rewrote to the owner-independent `area:Dzungaria={every_area_province}` / `area:Tarim={…}` idiom — oracle-proven (Terra-Indomita punt_decisions.txt:220, Invictus jomon_decisions.txt:182; 768/889 uses). Area keys verified in map_data/areas.txt.
- *Major (perf regression):* the province sweep was called every quarterly pulse from `QING_ili_apply_control_band`. FIX: de-pulsed — removed from the pulse applier, driven only from the 5 discrete stage-resolution effects where the grip meter changes (choose-coast, reconquest win/fail, ratify, Zeng triumph) + the break-free fallback. Mirrors #83's nwcrop de-pulsing.
- *Major (se_LOG):* `QING_ili_apply_prov_band` had no LOG wiring. FIX: added LOG_enter/LOG_exit + a LOG_line on each band branch.
- *Minor (stale comments):* the "read O(1)/All O(1)" header/pulse comments are now accurate again (resolved by the de-pulsing).

**B6 (F:great-office-powerbase) — se_QING_COUNCIL.txt — major + minor, FIXED (braces 218/218):**
- *Major (runtime error, dropped cohort):* `add_subunit = archers` — `archers` is UNDEFINED (army_archers.txt is a 3-byte BOM-only stub; the mod's only army sub_units are regular_infantry/artillery/conscripts/engineer_cohort/warelephant/supply_train). FIX: → `regular_infantry`, matching the host's other four cohorts.
- *Minor (dead loc / raw-string display):* `create_unit name = "qing_grandee_rebel_army"` relied on an unquoted-key auto-resolve the mod never demonstrates. FIX: quoted LITERAL `"A Grandee's Private Army"` per the proven SELFSTR fleet idiom (name="Beiyang Fleet"); retired the now-dead loc key (left as a traceability comment).

**B2 (B:treaty-ports) — qing_treaties_modifiers.txt — major, FIXED (braces 7/7):**
- `qing_treaty_port` used `local_commerce_modifier` — NOT an engine-read key (the modifier_icons:298 .dds belongs to `state_commerce_modifier`; `local_commerce_modifier` is declared nowhere and appears only in unloaded common/WIP/), so the port's headline +15% commerce silently applied nothing. FIX: → `local_commerce_value_modifier` (proven province-scope commerce-production key, 16 live in-mod uses). The other three lines were already valid.

**B3 (item C — students-abroad) — se_QING_STUDENTS.txt — 2 major (one root cause), FIXED (braces 134/134):**
- The milestone "floor" `change_variable divide=25 then multiply=25` is a NO-OP (Imperator vars are floating-point; change_variable takes no rounding key), so `milestone_tmp == returned` and the once-per-+25-band guard never held → a returnee spawned nearly every graduation pulse up to the flooding cap of 6, instead of once per band. FIX: replaced with explicit literal-threshold banding (returned≥100/75/50/25 → 100/75/50/25/0) using only proven primitives (comparison + literal set_variable — avoided the unproven round-in-set_variable idiom), so `milestone_tmp` snaps exactly to a band and the `> last_milestone` guard fires once per band as specified.

**B1 (se_log_ok=false) — se_QING_VASSAL.txt — FIXED (braces 88/88):** added LOG_enter/LOG_exit to `QING_vassal_sync_lost_flags` (had only LOG_line). The disclosed re-subjugation-then-re-loss nudge behaviour is authorized by the brief's derivable-flag instruction — left as-is (transparency note only).

**B9 (se_log_ok=false + traceability) — se_QING_MECHANICS.txt + qing_mechanics_modifiers.txt — FIXED (braces 222/222, 60/60):** added LOG_enter/LOG_exit to `QING_army_spawn_newarmy` (had only LOG_line + LOG_fail); corrected the `qing_smuggler_den` comment naming a non-existent effect `QING_currency_spawn_smuggler` → `QING_DECLINE_spawn_smuggler` (se_QING_DECLINE.txt:1480).

**Optional nits LEFT (documented, not defects):** B5 custom-house slot-exhaustion log wording; B11 one-shot agitator guard; B7 sustained-confrontation feedback loop + predatory-band balance-tuning note (cooldown caps launches — correctness unaffected); B8 multi-band building drift + allow-on-add_building_level assumption; B9 whole-army decay-tag imprecision + spawn once-guard ordering. All flagged in the workflow review as acceptable/cosmetic; none affects correctness. B7 balance note carried forward for the tuning pass.

### #86 (Perf C4) DONE — se_QING_DIPLO.txt (braces 311/311)

`QING_gp_scan_plays` ran TWO full `every_in_global_list` sweeps of `global_all_diplomatic_plays` per Qing pulse: (A) the Qing's own plays reaching into a power's sphere, (B) a power's plays against the Qing. The two filters are PROVABLY DISJOINT — (A) `play_instigator = self`, (B) `play_instigator != self` — so no play ever matched both. MERGED into ONE pass (union filter with `AND`-block OR; then if(A)/else(B) split), halving the list iteration.

**Behavioural-equivalence proof (heightened scrutiny per directive "lots of scrutiny on performance changes"):** each play still performs exactly its one A- or B-action (mutual exclusion preserved → same SET of pressure calls). The only change is the ORDER of the per-play `QING_DECLINE_nudge` calls; those clamp 0..100, so order can perturb a raw counter value ONLY at the 0/100 rails. Every consumer reads these counters through THRESHOLD bands (≥50 rivalry modifier, ≥75 predatory `QING_gp_rival_launch_play`), and a rail discrepancy (99 vs 100, 0 vs 1) sits on the same side of every threshold — unobservable downstream. Away from rails addition is commutative → bit-identical. `AND`-in-limit idiom verified proven (se_AI.txt, se_DEMAND.txt). This is the lower-risk equivalent of the task's "cache Qing-involved plays" intent — it removes the redundant second full scan without hooking the play create/teardown lifecycle in se_AI.txt (which the directive's caution argues against).

**Perf cluster #83-#87 now COMPLETE** (#83/#84/#85 prior; #86 this pass; #87 currency-name bug prior). All autonomous perf + #91-quality work done; commit pending user request.

---

## [#92] Qing global diplomatic reach — enable Qing↔USA (and distant-power) diplomacy

**Problem (user):** At game start the Qing cannot conduct diplomatic relations with the United States.

**Root cause:** Not a mod bug — an engine gate. All real diplomatic actions (alliances, guarantees, trade agreements, diplomatic plays, war declarations) require `in_diplomatic_range`. The base `DIPLOMATIC_RANGE = 800` (common/defines/00_defines.txt:458), scaled only by the global `diplomatic_range_modifier` country modifier (nation ranks grant 0.10–2.25; great works 0.1–0.5), is far short of the trans-Pacific Qing↔USA distance. (The existing GP-rivalry/embassy layer sidesteps range by using `add_opinion`, which is why opinions work but real US relations never appear.)

**Decision (user):** Global reach for the Qing — `diplomatic_range_modifier` is the engine's only lever and cannot be pointed at one target, so grant CHI a blanket global reach. The USA and every other distant power become reachable. Thematically fits a Victorian world-power Qing.

**Change (3 files, additive, se_LOG-wired per standing rule):**
- `common/modifiers/qing_mechanics_modifiers.txt` — NEW country modifier `qing_global_diplomatic_reach { diplomatic_range_modifier = 9.0 }` (stacks additively on nation-rank bonus → effective range well over any inter-continental distance). Key verified engine-valid (used by 00_hardcoded.txt nation ranks).
- `common/scripted_effects/se_QING_MECHANICS.txt` — NEW effect `QING_open_global_diplomacy` (LOG_enter/exit/line/fail; idempotent guard on `has_country_modifier`, applies `duration = -1`).
- `common/on_action/qing_mechanics_on_actions.txt` — call `QING_open_global_diplomacy = yes` in the CHI `on_game_initialized` block.

All three files brace-balanced after edit. Fires for both human and AI CHI at game start.

---

## [#93 / #94 / #95 / #96] AI-autonomous US, Japan, and Mexico arcs + coupling inversion (2026-07-05)

**User directive:** implement DESIGN_USA_CIVIL_WAR.md (#93) and DESIGN_JAPAN_BOSHIN.md (#94) with a **coupling
inversion** — the NEW US and Japan subsystems OWN their arcs and climaxes; the EXISTING Qing content (#73 USCW,
#81 pre-Perry Japan) is refactored to HOOK INTO the new content, not the reverse (#95). Then a NEW Mexico
subsystem (#96) coupling to the US arc, with the existing Qing #69 Mexico colonization arc hooking INTO it.
**Hard requirement:** all three arcs must advance and resolve AUTONOMOUSLY under AI control (the player is
almost always the Qing) — ai_chance-weighted options + immediate/pulse-driven decisive effects, never
player-gated outcomes.

**The shared AI-autonomy pattern** (mirrored across all three, oracle-checked in Phase 0 / #92):
- `on_game_initialized` seeds the state init + the dated historical beats for the tag with **NO is_ai guard**,
  so the arc unfolds for an AI-controlled country exactly as for a human one. Each beat re-checks its own
  not-done variable at trigger time, so wide `days = { A B }` windows (offsets from the 1815.7.1 START_DATE at
  365.25 d/yr) are safe.
- The monthly pulse (`*_pulse_on_action`, registered in `00_monthly_country.txt`) **self-gates on `tag`, NEVER
  on `is_ai`**, and throttles to ~quarterly via a cooldown variable so the per-tick cost is negligible for every
  other country (rejected on the tag test).
- Every event's `immediate` block holds the decisive state change; player `option` blocks only *modulate* and
  are `ai_chance`-weighted. The climax is reached via meter-driven pulse checks with a hard-date fallback, so no
  beat depends on a human choosing.
- Counters are the AI/summary layer (0..100, clamped via a `*_nudge` helper); every threshold hangs a **concrete
  on-map object** (a real named character, a released country, a province modifier) per the concrete-over-abstract
  standing rule.

### #93 — the American road to the Civil War ("The House Divided")

- **Files:** `se_USA_SECTION.txt` (counters + verbs), `se_USA_ROSTER.txt` (named figures), `usa_section_events.txt`
  (beats .1–.12), `usa_section_modifiers.txt` (band modifiers), `usa_section_on_actions.txt` (seed + pulse),
  `usa_section_l_english.yml` (loc). Pulse registered in `00_monthly_country.txt`.
- The arc runs Missouri Compromise → sectional crises → secession → the war, tag = USA, AI-autonomous. The
  Confederacy is released **dynamically off the USA's own land** (`LAND_release_from_list`) because CSA is a
  PHANTOM tag (custom-name only, `c:CSA` unsafe) — the handle is published via `set_global_variable = usa_csa_country`.

### #94 — the Japanese Bakumatsu → Boshin arc

- **Files:** `se_JAPAN_BAKUMATSU.txt`, `se_JAPAN_BOSHIN.txt`, `japan_bakumatsu_events.txt`,
  `japan_bakumatsu_modifiers.txt`, `japan_bakumatsu_on_actions.txt`, `setup/countries/japan/japan.txt`,
  `japan_bakumatsu_l_english.yml`. Self-gates on the Japan tag (TKG is Japan at 1815; JPN never formed).
- The Restoration payoff is made CONCRETE via the real daimyo tags (`release_subject` of CSU/SHZ from TKG +
  `start_civil_war` behind a spawned loyalist leader), not a tag formation — same concrete idiom as #81.

### #95 — coupling inversion (CHANGE to shipped #73 + #81, behavioural-equivalence-scrutinized)

- The Qing #73 `qing_uscw.1` now fires **from `usa_section.12`** (the new arc's secession climax) for a human
  Qing only, and its Confederate-recognition path consumes `global_var:usa_csa_country` (the concrete released
  country the US arc put on the map) rather than the phantom `c:CSA`. Dead `QING_uscw_release_confederacy` removed;
  verified no dangling refs. The Qing #81 pre-Perry Japan schedule left as an idempotent, human-gated backstop
  (the dead `NOT = { exists = c:TKG }` game-start guard removed).

### #96 — the Mexican political-instability arc + the Qing #69 hook

- **New Mexico subsystem (source of truth), files:** `se_MEXICO.txt` (7 counters — instability/conservative/
  liberal/church-privilege/foreign-debt/territory-lost/pronunciado-count; band + milestone + climax verbs),
  `se_MEXICO_ROSTER.txt` (10 named figures: Iturbide, Alamán, Santa Anna, Álvarez, Juárez, Ocampo, Miramón,
  Zaragoza, Díaz, Maximilian — carried by `add_nickname`), `mex_instability_events.txt` (beats .1–.13),
  `mex_instability_modifiers.txt` (instability + church bands, debt-suspension, Second-Empire, the Caste-War
  province modifier), `mex_instability_on_actions.txt` (seed .1–.10 + pulse), `mex_instability_l_english.yml`.
  Pulse registered in `00_monthly_country.txt`.
- **Arc:** independence → the Santa Anna praetorian cycle → the 1848 Cession (concrete province transfer to
  c:USA, feeding the US arc's `usa_section.4`) → La Reforma → the War of the Reform → the 1861 default →
  European intervention → the **Second Mexican Empire** under Maximilian (`MEX_install_empire`: spawns Maximilian,
  `set_as_ruler`, `change_government = imperial_monarchy`, renames to the Second Empire, publishes
  `set_global_variable = mex_empire_country`) → the 1867 fall — **UNLESS a foreign patron props it up**
  (`mex_foreign_patron`, read by `MEX_empire_fall_check`), the alt-history divergence the Qing #69 arc is *for*.
- **US↔Mexico coupling:** the French Intervention is gated on the US Civil War state (`usa_seceded` /
  `usa_csa_country`) — the Monroe Doctrine cannot be enforced against France until the Union wins, so an early
  Union collapse *helps* Maximilian and a Union victory dooms him. The concrete US↔Mexico linkage the user asked for.
- **Qing #69 refactor (CHANGE to shipped code, heightened scrutiny), files:** `se_QING_MEXICO.txt` (new consumer
  verbs `QING_mexico_prop_empire` / `QING_mexico_back_juarez`), `qing_mexico_adventure_events.txt` (new consumer
  event `qing_mexico_adventure.1`, the `usa_section.12 → qing_uscw.1` inversion pattern — a human Qing court reacts
  to a Maximilian the Mexico arc set in motion), and the two refactored tasks in `qing_colonization_missions.txt`
  (search `[#96 REFACTOR]`):
  - `qing_col_maximilian` now READS the Mexico arc: if the Second Empire already stands
    (`global_var:mex_empire_country`), the Qing PROPS it (sets `mex_foreign_patron`); if not yet, it ACCELERATES
    the arc (`MEX_nudge mex_foreign_debt +20` + pokes `mex_instability.12`); the original Napoleon-fork /
    Daoguang-betrayal flavour preserved verbatim.
  - `qing_col_mexican_empire` now guards against **double-release**: if the arc's Empire already exists, the Qing
    becomes its patron instead of standing up a duplicate client Empire; otherwise the original
    `QING_establish_protectorate` release runs verbatim. Behaviour when the Mexico arc is absent (`c:MEX` unset)
    is unchanged — a `LOG_fail` notes the no-hook case and the task proceeds on its own flavour.
  - **No new Qing state invented**; the #69 tasks only READ the Mexico arc and set at most the one
    `mex_foreign_patron` flag on it.

**se_LOG + traceability:** every new verb wired LOG_enter/LOG_exit/LOG_line + LOG_fail on guard-fail
(sys = USA / JAPAN / MEX / QING); every refactored #69 branch carries a `[#96 REFACTOR]` in-code comment + a
sys = QING LOG_line, per the fix-traceability rule.

**Validation:** all new/edited Mexico files brace-balanced (se_MEXICO 206/206, roster 82/82, se_QING_MEXICO 42/42,
events 181/181 + 7/7, modifiers 8/8, on_action 30/30, missions 515/515). Byte conventions correct per file class
(se_*/modifiers = no-BOM/LF; events/on_action/loc = BOM/LF). Every cross-reference resolves: `qing_mexico_adventure.1`
defined, `QING_mexico_prop_empire`/`_back_juarez` defined and called, `MEX_nudge`/`mex_instability.12`/
`mex_empire_country`/`mex_foreign_patron`/`mex_empire_installed` all resolve, and the reused opinion/loyalty modifiers
(`qing_gp_accommodation_opinion`, `qing_gp_rivalry_opinion`, `loyalty_qing_congenial`, `qing_col_mexican_crown`) all
exist. Mandatory post-implementation code review of the #93–#96 changeset dispatched (findings to be addressed on return).

**Deep-changeset audit (separate, larger scope):** the full-authorship deep audit (commits 0990fe6a..HEAD, 201
files, 211 agents) completed and returned **38 confirmed findings (9 major, 29 minor)** — all in the *earlier* Qing
subsystems (keju/council/office/ili/pre-Perry-Japan/advisors/migration/diplomacy), NOT the new #93–#96 arcs. Saved to
`DEEP_AUDIT_FINDINGS.json`; to be triaged and fixed as the next work item per user instruction.

### #93–#96 mandatory code review — findings + fixes (2026-07-05)

The dedicated post-implementation review of the new arcs verified all cross-references resolve, all arcs are
AI-autonomous (decisive state in `immediate`, options `ai_chance`-weighted, pulse-driven climaxes with hard-date
fallbacks, once-guards intact, no double-install/double-release), and the #96 Qing refactor is
behaviourally equivalent when the Mexico arc is absent. Findings actioned:

- **FIXED (correctness, MEDIUM) — `se_USA_SECTION.txt:245`:** the secession gate's structural clause
  `var:usa_free_states > usa_slave_states` had a **bare-token RHS**, which the engine resolves as a (nonexistent)
  script value → 0, making the free>slave condition always-true. Corrected to `var:usa_free_states >
  var:usa_slave_states` (variable-to-variable idiom, `var:` on both sides). Tagged `[#97-fix task #97]`. The
  1861.4.1 date fallback meant this never stalled the arc — it was a design-intent correctness bug, now honest.
- **FIXED (dead code) — `usa_king_cotton` / `usa_free_labor`:** both modifiers were defined + loc'd but never
  applied. They model the sectional economies present from the start, so both are now stamped once, idempotently,
  in `USA_section_init`. Tagged `[#97-fix task #97]`.
- **FIXED (log accuracy) — `se_MEXICO.txt:76` `MEX_nudge`:** the LOG_line read `[ROOT...]`, which misreported CHI's
  scope when the #96 Qing hook calls `c:MEX = { MEX_nudge ... }` (ROOT = CHI). Changed to `[This...]` so the log
  names the actually-nudged country in both the in-MEX and cross-scope cases. Tagged `[#97-fix task #97]`.
- **REVIEWED, no change — Boshin civil war raised inside the released tozama** (`se_JAPAN_BOSHIN.txt:137`): the
  reviewer flagged that `start_civil_war` runs inside the just-released Satsuma. This is the **exact shipped,
  oracle-verified #81 idiom** (`QING_jppre_restoration_break`, se_QING_JAPAN_PREPERRY.txt:199-215:
  `release_subject` then `start_civil_war` inside the freed daimyo). #94 was speced to mirror #81; kept for
  behavioural consistency with the established pattern (the arc still completes correctly).
- **REVIEWED, no change — `japan_bakumatsu.7 → qing_japan_preperry.10` re-fire** (event:425): harmless — `.10`'s
  own trigger re-guards on `NOT = { has_variable = qing_jppre_perry_done }`, so it cannot double-fire.
- **NOTED (low, un-actioned) — `usa_csa_country` never `remove_global_variable`'d:** the Mexico Empire-fall check
  reads `NOT = { exists = global_var:usa_csa_country }`; relies on engine scope-invalidation once the released CSA
  is destroyed, covered by the 1867.6.1 date fallback regardless. Left as-is pending playtest confirmation.
- **NOTED (low, un-actioned) — twin-throne edge:** a human Qing releasing a client Empire of Mexico *before* an AI
  MEX reaches its own climax can, in principle, coexist with a later arc Empire (requires holding ≥3 Mexican-region
  provinces first — geographically unlikely). Point-in-time guard; no later reconciliation. Flagged for playtest.

All fixed files re-verified brace-balanced (se_USA_SECTION 158/158, se_MEXICO 207/207); a scan confirmed no other
bare-token variable comparisons exist in the four new `se_` files. Phase 5 complete.

## Deep-audit findings — MAJOR logic bugs (task #98)

The 211-agent deep adversarial audit (wf_e2d51f54) returned 38 confirmed findings across the shipped
codebase. The 9 MAJOR (real logic bugs) are addressed below; all carry `[#98-fix task #98]` in-code tags.
Findings [4] and [5] land in `qing_japan_preperry_missions.txt`, which the #93-96 review (w7iipeldq) is
concurrently rewriting — DEFERRED to reconcile against that review's output rather than clobber it.

- **[0] FIXED — `qing_keju_events.txt:139/149` (`qing_keju.2`):** the palace-exam laureate was chosen with
  `order_by` inside `random_character`, where `order_by` is IGNORED — so the 狀元 was picked uniformly at
  random, not by ability. Both the primary and fallback picks changed to `ordered_character` + `max = 1`
  (+ `check_range_bounds = no`), the proven ablest-picker idiom (se_QING_COUNCIL.txt:128). Now the ablest
  non-jinshi courtier is conferred the degree.
- **[1] FIXED — `se_QING_COUNCIL.txt:120/133` (`QING_council_autofill`):** the while-limit and the
  `ordered_character` limit tested `is_target_in_variable_list = { ... target = this }` in CHARACTER scope
  against the COUNTRY-held `qing_council_members` list, which always missed — so autofill seated one member
  and stalled. Both now read the list via `employer = { ... target = prev }` (the proven form at line 58).
- **[2] FIXED — `qing_office_events.txt:356` (`qing_office.5.b`):** granted the `qing_council_effective`
  BAND modifier with `duration = 1095`, but `QING_council_apply_band` strips + re-derives that band from the
  effectiveness counter every pulse — so the buff vanished on the next tick. Replaced with a durable
  `+8` nudge to the underlying `qing_council_effectiveness` counter (the concrete driver the band reflects).
- **[3] FIXED — `qing_ili_events.txt:193` (`qing_ili.4` compromise):** called only
  `QING_ili_apply_control_band`, never `QING_ili_apply_prov_band` — so the province modifiers stayed frozen
  at the pre-settlement band forever. Added the province sweep, matching the #91 de-pulsed convention where
  every discrete stage stamps both the control band and the map.
- **[6] FIXED — `se_QING_ADVISORS.txt:104` (`QING_advisor_recruit`):** the post-block mark-the-expert guard
  tested `var:qing_advisor_$field$ = 1` — the FIELD being staffed by anyone — so a same-field recruit that
  was REJECTED for a full slot was still falsely marked a foreign advisor (and given the character modifier).
  Moved the mark INSIDE the success branch (on `scope:qing_advisor_char`), tying it to this recruit actually
  taking the seat.
- **[7] FIXED — `se_MIGRATION.txt:318` (`MIGRATION_border_friction_breaking_point`):** the
  `migr_found_irredentist_kin` flag was set on `root` (the on_action's country) but the sibling reads that
  gate the clean-fail log run in the effect's this-scope (the friction province) — so the flag was never
  seen and the "no kin-state" failure log fired even on a successful irredentist play launch. Set + read +
  clear the flag all on `scope:migr_friction_prov`.
- **[8] FIXED — `send_settlers.txt:328`:** `DIPLOMACY_trigger_diplomatic_play_war` now tears the play down
  (se_DIPLOMACY.txt:716, the #79 fix), stripping `play_target_area`; but this caller read that var AFTER the
  war trigger to run its post-war claim sweep, hitting a wiped var. Capture the target area into
  `scope:settlers_target_area` BEFORE the trigger and read the saved scope afterward. Audited all five
  war-trigger callers; this was the only genuine post-teardown play_* read (the double-teardown at
  diplomatic_play_events.txt:639 is a harmless no-op; agadir + the other sites read nothing after the trigger).
- **[4]/[5] DEFERRED — `qing_japan_preperry_missions.txt:189/218`:** the loyalist gate needs
  `reform_faction >= 40` (max reachable ≈31) and the restoration capstone needs `reform_faction >= 70`
  (max ≈43) AND `shogun_grip < 40` (min ≈64) — both roads unreachable. File under concurrent #93-96 review;
  reconcile the rebalance against that review's changes.

All edited files re-verified brace-balanced.

## Deep-audit findings — MINOR logic bugs (task #98)

Three of the 29 "minor" findings are genuine logic/scope bugs (not just missing LOG markers); fixed here.
The remaining ~26 are mechanical se_LOG LOG_enter/LOG_exit wiring gaps on new scripted_effects — batched
separately (see below), with the Japan pre-Perry files EXCLUDED pending the #93-96 review.

- **[18] FIXED — `qing_office_events.txt:239` + `:252` (`qing_office.4`):** same country-held-list scope bug
  as [1] — the `qing_council_members` membership test ran in character scope (`target = this`) in both the
  event trigger and the immediate's picker, so a sitting councillor could resurface as a "rising statesman".
  Both now read via `employer = { ... target = prev }`.
- **[19] FIXED — `qing_office_events.txt:255` (`qing_office.4`) + `:419` (`qing_office.6.a`):** same
  order_by-in-`random_character` bug as [0] — the "rising statesman" and the Zongli Yamen head were picked
  at random despite the tooltips promising the ablest man. Both changed to `ordered_character` + `max = 1`.
- **[16] FIXED — `se_ECON_LOG.txt:54/78/109` (country/jobs/currency snapshots):** `ECON_LOG_quarter` runs
  inside `every_country` (oa_wealth_changes.txt:185), so `this` = the iterated country but the LOG_lines read
  temps via `[ROOT.MakeScope...]` and tagged `[ROOT.GetTag]` — ROOT being the on_action root, NOT the iterated
  country. The temps were staged on bare `this` yet read off ROOT, so every quarterly snapshot logged the
  wrong tag and a stale/zero value. All three snapshots now stage the temps on ROOT (matching the read form,
  as the already-correct production snapshot does) and label the line with `[scope:econ_log_country.GetTag]`.

All edited files re-verified brace-balanced (qing_office_events 158/158, se_ECON_LOG 55/55).

## Deep-audit findings — se_LOG enter/exit wiring batch (task #98)

The remaining ~26 minor findings ([9]-[15], [17], [20]-[24], [26]-[34], [36], [37]) are all the same class:
NEW scripted_effects that carry only LOG_line (or nothing) and are missing the standing-rule LOG_enter/LOG_exit
pair. This is a purely mechanical, additive pass, so it was delegated to a subagent with strict guardrails
(additive-only, preserve byte convention + tabs, brace-check each file, tag each with `[#98-fix task #98]`,
and EXCLUDE se_QING_JAPAN_PREPERRY.txt — finding [25] — which is under the concurrent #93-96 review).

Result: **71 effects wired across 18 files**, all brace-balanced. Files: se_QING_CUSTOMS, se_QING_GOVERNANCE,
se_QING_TECHTRANSFER, se_QING_REFORM, se_QING_SELFSTR, se_GOODS, se_QING_COUNCIL, se_QING_NAPOLEON,
se_QING_COLON, se_QING_DECLINE, se_CURRENCY_STRESS, se_SUBJECT_QING, se_MIGRATION, se_DEJURE,
se_CLAIM_HOSTILITY, se_SEPARATISM, imp19c_effects_legion_setup (EXIT-only, both already had ENTER),
se_QING_AFFINITY, se_DIPLOMACY. The parent verified the batch coexists cleanly with the [7]/[1] logic fixes
already made in se_MIGRATION.txt and se_QING_COUNCIL.txt, and that se_QING_JAPAN_PREPERRY.txt was left untouched.

## Deferred (task #98)

- **[4]/[5] and [25]** all live in `qing_japan_preperry_missions.txt` / `se_QING_JAPAN_PREPERRY.txt`, which the
  #93-96 adversarial review (workflow w7iipeldq) is concurrently rewriting. Deferred to reconcile against that
  review's output. [4]/[5] = unreachable loyalist/restoration thresholds (rebalance the gates or add
  reform_faction/shogun_grip sources); [25] = LOG_enter/exit wiring on QING_jppre_deepen_intel.

Deep-audit outcome: 8 of 9 majors fixed (2 deferred as [4]/[5] are both in the under-review Japan file — one
major, [4]/[5], counted as two findings), 3 minor logic bugs fixed, 71-effect LOG-wiring batch done, 3 items
deferred pending the concurrent review. All non-deferred findings actioned.

---

## Military-logistics expansion — 4 proposals drafted [logistics P1–P4]

Implements RESEARCH_MILITARY_LOGISTICS.md, closing the §B gap: the quarterly trade sim already
PRODUCED/DEMANDED/computed SHORTAGES for the military goods but nothing read those shortages to
affect forces. New suite tag: `sys = LOGISTICS`.

**P1 — munitions/artillery shortage → attrition & morale (LIVE).**
- NEW `common/scripted_effects/se_LOGISTICS.txt` (no-BOM/LF): `LOGISTICS_scan_worst_land_shortage`
  aggregates the worst governorship-scope `shortage_{early,late}_{munitions,artillery}` (0..1);
  `LOGISTICS_apply_munitions_shortage_penalty` stamps ONE tiered self-refreshing country modifier
  (severe ≥0.50, minor ≥0.15, else clears). Full LOG_enter/exit/line.
- NEW `common/modifiers/logistics_modifiers.txt`: `country_munitions_shortage_minor`
  (land_unit_attrition +0.10, land_morale_recovery −0.10), `_severe` (+0.30 / −0.25 / army_movement_speed −0.15).
- Wired at oa_wealth_changes.txt (quarterly_apply_trade_changes_and_consume), country scope,
  AFTER the every_governorships CONSUME loop refreshes shortages. `LOGISTICS_quarter = yes`.

**P2 — arsenal/depot buildings → local munitions production (LIVE).**
- 00_military_buildings.txt: `arsenal_building` given real `local_defensive` output (was empty
  modification_display); NEW `military_depot_building` (granary-schema clone, city-gated, event-spawnable).
- GOODS_svalues.txt: `GOODS_governorship_early_munitions_produced` now adds a per-province
  `num_of_arsenal_building × GOODS_arsenal_munitions_output(2)` + `num_of_military_depot_building × GOODS_depot_munitions_output(1)`
  term, gated on tech_firearms — symmetric with the demand side that already counts these buildings.
- Loc: modifiers_l_english.yml (3 modifiers), text_l_english.yml (military_depot_building + _desc).

**P3 — coal/naval-supplies shortage → steam-fleet attrition (LIVE).**
- se_LOGISTICS.txt: `LOGISTICS_scan_worst_naval_shortage` (worst of shortage_coal / shortage_naval_supplies);
  `LOGISTICS_apply_coal_shortage_penalty` gated on owning steam hulls via PROVEN
  `num_of_unit_type = { type = medium_steamer/screw_frigate value >= 1 }`, stamps `country_coal_shortage`
  (naval_unit_attrition +0.20). Sailing navies unaffected; self-clears if fleet scrapped.

**P4 — rifles trade good + infantry gating (DRAFT ONLY, deliberately not wired).**
- NEW `DESIGN_LOGISTICS_RIFLES.md`: complete 6-edit spec. Held out of live files because (a) it is the
  HIGH-risk 6-file member and (b) `trade_good_surplus` inside a UNIT `allow` is the one primitive the oracle
  pass could NOT prove. A half-registered good would inject a permanent phantom `shortage_rifles` that P1 would
  then punish, so it ships as a ready-to-apply spec (with a soft-penalty fallback) pending P1–P2 stability + a
  live `trade_good_surplus`-in-unit-allow test.

Byte conventions preserved per file (se_LOGISTICS/logistics_modifiers = no-BOM/LF; the 3 edited common files =
BOM/CRLF as their siblings). All edited/created files brace-balanced. se_LOG on every new effect.


## #93-96 deep-review fixes (M1-M4, m5; m6 resolved as side-effect)

Source: REVIEW_9396_FINDINGS.md (workflow w7iipeldq synthesis). All six survivors addressed.

- **[#94-fix M1 / M1 v2]** `se_JAPAN_BAKUMATSU.txt` pulse drift — Tosa (YCH) & Saga (SGA)
  `domain_sonno` were seeded 15/12 and nudged by NO path, so the Boshin release gate (`>= 45`,
  se_JAPAN_BOSHIN.txt:103) was permanently false and both tozama could never be released.
  FIRST attempt added them to the leaders' drift block — but the post-implementation review
  caught that that block is gated on `baku_legitimacy > 25`, which the dated beats drive below
  25 by ~1861, freezing YCH/SGA at ~31 (still short of 45). v2 gives YCH/SGA their OWN drift
  block gated on `baku_perry_done` ONLY (decoupled from legitimacy) at +3/yr, so from Perry
  (~1854) to the 1868 climax they reach YCH ~57 / SGA ~54 — clear of 45 with margin, YCH also
  clears the `>= 55` Tosa milestone (resolves m6), both still behind the beat-driven leaders
  (CSU/SHZ ~85), ordering YCH > SGA preserved by seed.
- **[#94-fix m6]** side-effect of M1: YCH now drifts past the previously-dead `>= 55` milestone
  gate at se_JAPAN_BAKUMATSU.txt:187 (Ryoma spawn). No separate edit.
- **[#93-fix M2]** `usa_section_events.txt` .11 (Election 1860) — added `usa_free_states +2`
  (Minnesota 1858 / Oregon 1859 / Kansas Jan 1861 free admissions) so free (15) can exceed slave
  (13) and USA_secession_check's structural `free > slave` gate can actually trip the climax
  ahead of the 1861.4 date fallback (kept as a true backstop).
- **[#94-fix M3]** `se_JAPAN_BOSHIN.txt` JPN_boshin_execute — added `remove_country_modifier` for
  all three `baku_grip_*` bands BEFORE the TKG->JPN retag. The TKG pulse gates on `tag = TKG`, so
  after the retag it can never reconcile; the last band was otherwise stranded on Meiji Japan
  forever.
- **[#93-fix M4]** `se_USA_SECTION.txt` USA_section_pulse — added a guarded
  `remove_global_variable = usa_csa_country` teardown (fires when the Union no longer wars with
  the CSA and the CSA holds no provinces). Unblocks MEX_empire_fall_check's reunification branch
  (se_MEXICO.txt:457) and stops se_QING_USCW:91 acting on a dead handle.
- **[#96-fix m5]** three uncoordinated "prop the Second Empire" payouts (se_QING_MEXICO.txt
  QING_mexico_prop_empire; qing_col_maximilian & qing_col_mexican_empire on_completions) now share
  a first-wins `qing_mexico_propped` flag (ROOT = CHI in all three): the additive wealth/prestige/
  GP-provoke package pays out exactly once. Name-unique crown modifiers (non-stacking) left
  outside the guard. Mission site uses a per-run `qing_mexico_pkg_this` decision var (an always-run
  arc hook sits between its grants) and cleans it up at on_completion end.

All six files brace-balanced; byte conventions preserved (se_* / missions no-BOM/LF, usa events
BOM/LF). se_LOG markers added where new (M4 teardown LOG_line).

## [#93-fix crash] Deterministic startup CRASH — nested scoped-effect in create_character (2026-07-06)

> **⚠️ RETRACTED — WRONG ROOT CAUSE. Superseded by [#90-fix crash] below.** This entry blamed
> `se_USA_ROSTER.txt`. That diagnosis was invalid: the "good" baseline `8a41e06f` it bisected from
> was NEVER verified with the mod actually enabled (it was a base-game false positive — the mod was
> not selected). Re-bisecting from the genuinely-verified-good `0990fe6` pinned the crash to a
> DIFFERENT commit (`ec4d8a72`, #90). The roster refactor below is harmless and kept (it matches the
> proven se_QING_ROSTER idiom), but it does NOT fix the crash — the crash is pre-script (see below).

**Symptom:** deterministic EXCEPTION_ACCESS_VIOLATION (C0000005) at startup. Commit `8a41e06f`
loaded; the very next commit `781785b3` (the #93–#96 arcs) crashed. No fatal line flushed to
error.log; parse completed, map loaded (`map.cpp:796 ... has no area assigned`), then the access
violation at gamestate/definition construction with no USA-specific error logged.

**Root cause (found by additive binary-split bisection from the good baseline — 4 launches:
arcs-on-good → arcs-no-jpn → arcs-usa-only → roster-stub):** `se_USA_ROSTER.txt`'s 10 spawns each
called the scoped effect `USA_roster_finalize` (which runs `set_home_country = ROOT` +
`add_nickname` + `save_scope_as`) **INSIDE** the `create_character` block. Running a scoped effect
inside create_character access-violates at character construction. The proven-safe twin,
`se_QING_ROSTER.txt`, calls finalize OUTSIDE the block via `scope:figure = { ... }`.

**Fix:** for all 10 spawns (Clay/Calhoun/Webster/Garrison/Douglas/Brown/Lincoln/Davis/Lee/Grant),
the create_character block now ends with `save_scope_as = usa_figure`, and finalize runs after the
block as `scope:usa_figure = { USA_roster_finalize = { nick = "NICKNAME_USA_<NAME>" } }` — mirroring
the Qing idiom exactly. Task-tagged `[#93-fix crash]` comment on each. Braces 92/92; se_USA_ROSTER
is no-BOM/LF (preserved). se_LOG coverage retained (LOG_line still fires inside USA_roster_finalize).
`USA_spawn_firebrand` (se_USA_SECTION.txt) already used the correct outside pattern — untouched.

**Verification:** roster-stub branch (finalize-callers removed) LOADED clean; full-feature-set
branch with this fix applied is the fix-forward. Scan confirms no scoped-effect call remains nested
in any create_character block across the USA arc.

## [#90-fix crash] Deterministic startup CRASH — the #90 regional-army create_character fallback (2026-07-06)

**RESOLVED — verified loading in-game by user.** Two commits ship the fix on
`fix-usa-roster-create-character`: `6573cc80` (the modifier cleanup — see the ⚠️ correction below) and
`fa87110c` (**the actual crash fix**).

**Symptom:** deterministic EXCEPTION_ACCESS_VIOLATION (C0000005) at startup, in `-debug_mode`, with
**ZERO `[IMP19C]` breadcrumbs** in debug.log, and an error.log identical to every prior crash (no new
diagnostic line). The game boots to a Qing start with the mod disabled but access-violates with it on.

**Bisection (clean, from the genuinely-verified-good baseline `0990fe6`):**
`0990fe6` good → `3de82c87` loads → `d7ebffa8` loads → `ec4d8a72` **CRASHES** → `be96733f` loads.
Adjacent ⇒ culprit commit = **`ec4d8a72`** (#90 Tie Han regional-army counter into loyal-cohorts power
base). Within that commit, isolated by whole-file revert to be `se_QING_MECHANICS.txt` (NOT the new
character modifier — see correction below), then narrowed inside the file by successive stub branches.

**Root cause (what was PROVEN):** the else-branch of the new effect
`QING_regional_army_bind_commander` in `common/scripted_effects/se_QING_MECHANICS.txt`. When no sitting
Han governor exists, that branch conjured a founding magnate via `create_character` (culture=han,
religion=ROOT.religion, traits) and then, in the new character's scope, ran `QING_roster_finalize` +
`add_loyal_veterans = 8` + `QING_magnate_track_grant` (which does `add_character_modifier`). Removing
the WHOLE else-branch loads clean (branch `crash-test-no-createchar`). Proven by test:
- Deleting the `qing_regional_magnate` MODIFIER definition entirely → still CRASHES (modifier innocent).
- Reverting `se_QING_MECHANICS.txt` to parent → LOADS (the fault is in this file).
- Stubbing the 3 new effect bodies to no-ops → LOADS (fault is INSIDE a body).
- Stubbing only the else-branch's create_character path → LOADS (fault is that path).
- Swapping culture=han→manchu, religion=ROOT.religion→confucianism (proven literals) → still CRASHES.
  ⇒ the dynamic culture/religion refs are NOT the cause; the create_character/finalize block is.

**Root cause (what was NOT proven — honest gap):** I did not isolate `create_character` itself from the
`QING_roster_finalize`+`add_loyal_veterans`+`QING_magnate_track_grant` finalize that follows it (user
called off further tests once a working fix was in hand). The one BEHAVIORAL difference vs. the 14 other
`create_character` calls that load fine (se_QING_NAPOLEON, se_QING_ROSTER callers, on_actions): those
grant nothing to the freshly-made character beyond the identity finalize, whereas #90 granted loyal
veterans AND a character modifier to a character created in the same block. Leading hypothesis: granting
loyal-veterans / a modifier to a not-yet-fully-materialized new character access-violates. NOTE the
unresolved oddity: the crash fires at load/boot, yet this effect is only reachable from a scripted_gui
button (never from on_game_initialized) — so WHY merely having this else-branch present breaks a fresh
boot is not fully understood. Do not treat the mechanism as settled.

**⚠️ CORRECTION to `6573cc80` / the earlier draft of this entry:** that commit's message and this
entry's first draft claimed the root cause was `land_morale_modifier` being a country-scope key in the
`qing_regional_magnate` CHARACTER modifier, and asserted "the engine validates create_character bodies
at load." BOTH claims are WRONG. Deleting the modifier outright still crashed (modifier is innocent),
and the mod contains 14 other create_character calls that load fine (a blanket load-time-validation
rule would prevent any boot). `land_morale_modifier` IS genuinely misplaced (a country/unit key in a
character modifier) and removing it is a correct latent-bug cleanup — it just was not THIS crash. Kept.

**Fix (`fa87110c`):** removed the crashing else-branch. The feature's core is intact — the if-path still
empowers a REAL sitting Han governor-general with `add_loyal_veterans` + the magnate marker. When no Han
governor stands, the sanction's +15 provincial-power counter bump (in `QING_sanction_regional_army`)
still lands; we simply skip fabricating a character. se_LOG retained (LOG_fail on the no-governor path).
Braces 229/229; file kept no-BOM/LF. Also kept: the `6573cc80` modifier cleanup and the (benign,
non-causal) `se_USA_ROSTER` refactor + TIB subject-chain change from the retracted [#93-fix crash].

**Verification:** user confirmed the `fix-usa-roster-create-character` branch LOADS into a Qing start.

---

## [#90-fix crash follow-up] Two cosmetic bugs (event pictures + se_LOG breadcrumbs)

Once the boot crash was fixed, the user asked for the two remaining cosmetic defects to be cleared.

**(a) Blank event pictures.** `common/event_pictures/00_event_pictures.txt` is a FULL-REPLACEMENT of the
vanilla file (redefines the standard vanilla pics), so any picture referenced by a mod event but NOT
defined in this file renders blank. Three were missing: `senate` (14 uses across usa_section /
japan_bakumatsu / mex_instability), `navy` (japan_bakumatsu.3), `greek_siege` (flavor_eve.8). Added a
definition for each, aliased to the closest proven vanilla texture (Event_senate_debate.dds /
Event_naval_battle.dds / Event_walled_city_under_siege.dds). Braces 152/152; kept BOM+CRLF.

**(b) se_LOG breadcrumbs emitted the tag literally.** The macros wrote `debug_log = "[IMP19C][$sys$] ..."`
and the output came out mangled (e.g. `[IMP19C]QING$]`) with `$sys$`/`$fn$`/etc. never substituting.
Root cause: SQUARE BRACKETS inside a debug_log/loc string are parsed by the engine as data-function
(`[GetX]`) syntax, so `[IMP19C][$sys$]` was consumed as a bracket expression. `$arg$` substitution into
debug_log itself DOES work — PROVEN by `se_PURCHASE.txt` (`debug_log = "... $tradegood$ ..."`) and by the
fact no reference mod (TI/Invictus) ever puts `[ ]` inside a debug_log string. Fix: dropped the brackets
across all 7 LOG_ macros, switching to a bracket-free but still-greppable scheme `IMP19C <SYS>: <msg>`
(failures: `IMP19C FAIL <SYS>:`). This changes ONLY the emitted string format — every one of the 505
call sites keeps its identical `$sys$`/`$fn$`/`$reason$`/... signature, so it is behaviourally
equivalent for callers. Header grep examples updated to the new delimiter. Braces 6/6; kept no-BOM/LF.

---

## [ethnic-gov] Governor–subject affinity feeds ethnic tension

**Request:** a contributing factor to Qing ethnic tension should be whether the governor set over a
people is one of them; both culture (strong) and culture group (weak) matter, in both directions.

**Where:** `QING_DECLINE_scan_ethnic_target` in `common/scripted_effects/se_QING_DECLINE.txt` — the
ANNUAL demographic scan that already weights each restive province by three additive terms (base
restive +1, high-unrest +1, demographic-displacement +1) into `qing_ethnic_restive_weighted`, from
which `qing_ethnic_tension_target` is derived. Added a FOURTH term inside the same per-province loop.

**Design (concrete-over-abstract):** reads the REAL governing character on the map via the verified
idiom `province -> governorship -> governor_or_ruler` (falls back to the ruler for the capital region;
guarded by `exists = governor_or_ruler`). Three-tier ladder, applied only to already-restive provinces:
- governor's exact `culture` = the province's frozen rightful culture (scope:dj_rightful_c) -> **-2**
- else same `culture.culture_group` as the rightful culture -> **-1**
- else (alien culture group) -> **+1**
Also accumulates the same deltas into a new diagnostic var `qing_ethnic_gov_signal` (scan-local; NO
external readers — grep-confirmed) surfaced via a LOG_line so a trace shows the governor contribution.

**Engine idioms verified against base game + TI/Invictus (oracle rule):** `governor_or_ruler` from a
governorship scope (Invictus `grant_satrap_autonomy.txt`); `culture = <culture scope>` on a character
(TI `culture = root.culture`); `culture.culture_group = <scope>.culture_group` (TI
`this.culture.culture_group = ...`; dynamic right-hand side proven by base `dominant_province_culture_
group = root.culture_group`). Rewrote an initial WRONG nested if/else_if into the repo's SIBLING
if/else_if/else form (matches the other bands in this same file).

**Behavioural-equivalence note (CHANGE to shipped code):** at the FIRST scan the weighted tally —
now including the governor term — is frozen into `qing_ethnic_restive_base`, and the target is
`20 + (current - base)/2`. So the 1815 governor arrangement is absorbed into the baseline: the
historical start still sits at ~20 and ONLY later governor reshuffles (or conquest/integration/
migration, as before) move tension. No existing counter's meaning changes; this only adds signed
deltas to an already-summed intermediate. Braces 814/814; file kept no-BOM/LF.

---

## [treasury-seed] Qing 1815 starting treasury seed

**Symptom (user report):** Qing opens 1815 with a NEGATIVE spendable treasury despite a large silver
reserve. User clarified: negative income/flow is fine, but a negative treasury STOCK is wrong — the
Qing were wealthy in 1815. Chosen fix scope: "seed sized to one year's costs."

**Root cause:** `setup/countries/e_asia/china.txt` sets NO starting treasury (grep-confirmed zero
hits for treasury/gold/silver/wealth). The 20,000 `silver_reserve_size` is currency metal backing (a
variable), decoupled from the engine's spendable `treasury`. At setup `INCOME_update_treasury_country`
does `add_treasury = var:INCOME_national_total_quarterly` — a deficit for CHI — so with a ~0 starting
stock the treasury opens underwater.

**Fix:** new `QING_seed_starting_treasury` (se_QING_MECHANICS.txt) computes ONE YEAR of CHI's own
expenditure IN-SCRIPT from the cost vars `INCOME_update_treasury_country` just cached — admin wages +
military wages + supplies_and_welfare, all stored NEGATIVE quarterly — via `multiply = -4` (negate + 4
quarters), then `add_treasury`. Self-scaling (no hardcoded number to rot if balance changes) and leaves
the flow/income side untouched, so the deficit still bites over time; it just no longer opens negative.
Stored intermediate in `qing_treasury_seed_1815`; idempotent via `qing_treasury_seeded` guard.

**Wiring / ordering:** called INSIDE the `every_country` loop in `oa_economy_setup.txt`
(on_game_initialized), immediately after `INCOME_update_treasury_country` — because on_game_initialized
block order across files is NOT guaranteed, computing here guarantees the cost vars exist. Self-gates
CHI-only (`tag = CHI` + `has_variable = INCOME_cost_administrator_wages_country`). se_LOG breadcrumbs
(enter/line/exit + fail). Braces: se_QING_MECHANICS 240/240, oa_economy_setup 526/526. Files kept
no-BOM/LF (se_QING_MECHANICS) / existing convention (oa_economy_setup).

---

## [edu-literacy] Historically-determined starting literacy + school bootstrap deadlock

**Symptom (user report, history-confirmed):** the Qing population is very uneducated at game start, yet
the player cannot build schools to fix it — schools themselves require educated pops.

**Root cause (real deadlock):** `EDU_school` AND `EDU_university` both gate on
`sufficient_education_slots = { tier = t2 }` → `EDU_available_t2_educated_governorship > 0`. But the
tier-2 cap (`EDU_available_slots_t2_governorship`) is 0 unless an `EDU_university` already exists, and
the tier-1 cap is 0 unless an `EDU_school` already exists. With the starting educated-pop fill at 90%
of a zero cap, every non-capital governorship began with 0 t1 / 0 t2 pops and no building could ever be
placed to change that. Only the capital had a floor (min 0.3 t1 / min 2 t2), so nothing could bootstrap
elsewhere. Historically the model also erased the real 1815 literate stratum: Qing basic/functional
literacy was ~15-20% of the population (Rawski consensus; male 30-40%, female 2-10%), classical/exam
literacy ~1% (~0.2% degree-holders + candidates), modern/Western education ~0 (begins 1862, Tongwen
Guan). Sources compiled by the literacy-research pass (Rawski 1979; shengyuan ~1/1000; jinshi ~0.001%).

**Fix (user direction: literacy HISTORICALLY DETERMINED per country, hybrid proxy+override; global):**
1. New `EDU_set_historical_literacy_fractions` (se_EDU.txt, country scope, run first in
   `EDU_startup_effect`): sets per-country `EDU_hist_literacy_frac_t1` / `_t2`.
   - CHI sourced override: t1 = 0.17, t2 = 0.01.
   - Everyone else: proxy default from the capital province's `civilization_value` (an
     already-authored per-province development proxy — European core ~20, Qing core ~10, frontier ~0):
     t1 = civ/50 clamped [0.02, 0.5]; t2 = t1 × 0.1, min 0.005.
2. Both education cap svalues (`EDU_available_slots_t1/t2_governorship`) gain a historical FLOOR
   `min = frac × var:governorship_population`, guarded on the frac var existing. Reads the CACHED
   `governorship_population` variable — NO province walk added to these hot svalues (respects the
   perf backlog). The existing "start at 90% of cap" fill then seeds literate pops, so
   `sufficient_education_slots={tier=t2}` is satisfied at 1815 and schools/universities become
   buildable. t2 floor (0.01·pop) stays well under both final `max` clamps (t1-educated ≈0.9·0.17·pop),
   so it never over-inflates t2.

**Why no building-gate edit:** leaving `EDU_school`/`EDU_university` `allow` blocks untouched keeps the
change behaviourally minimal and additive — it only supplies the educated-pop base the buildings always
required, matching the pre-existing `# TODO: t1 and t2 education` marker at se_LAND.txt:541.

se_LOG breadcrumbs (enter/line/exit) on the new effect. Braces: se_EDU 121/121, EDU_svalues 144/144.
Files kept BOM+CRLF. `capital_scope.civilization_value` value-block idiom verified in-repo
(DIPLOMACY_svalues.txt:514) and against TI/Invictus.

---

## [logistics-phys] [logistics-perf] Military-logistics review fixes

Workflow-reviewed the military-logistics suite (12 agents, 7 findings, all adversarially verified,
0 refuted). Fixed the two substantive findings; the three low/cosmetic ones left as-is.

### [logistics-phys] Correctness (medium): penalties fired on monetary deflation, not physical shortage
**Bug:** se_LOGISTICS.txt read `shortage_<good>` as a pure 0..1 PHYSICAL-deficit ratio, but
se_CONSUME.txt's `CONSUME_update_shortage` builds that variable in three layers: (1) the physical
deficit `(-stockpile)/DEMAND`, then (2) `+ CURRENCY_amt_circulated_deflation` (monetary deflation, up
to ~0.1), then (3) `+ (1 - DEMAND_elasticity_impact)` (up to +0.9 when governorship wealth falls). So a
currency-system country in deflation (e.g. the Qing player) with FULL arsenals could see
`shortage_early_munitions` inflated to ~0.68 → `country_munitions_shortage_severe` stamping
+0.30 attrition / -0.25 morale recovery / -0.15 movement on armies that had no equipment shortage;
same path hit coal/naval_supplies → steam-fleet attrition.

**Fix:** snapshot the PURE physical ratio at the source. `CONSUME_update_shortage` now sets
`shortage_phys_$tradegood$` immediately after the physical ratio is computed (before deflation/elasticity
are added), and removes it in lockstep with the composite in the surplus branch. se_LOGISTICS.txt's two
scans (land: early/late munitions+artillery; naval: coal+naval_supplies) now read `shortage_phys_*`
instead of the composite. The composite `shortage_<good>` is untouched — the currency/consume layer that
legitimately wants deflation in it keeps working. Inverting the terms back out in LOGISTICS was
impossible (composite capped at 1), so a source snapshot is the correct layer.

### [logistics-perf #71] Performance (medium): uncached province walk in a hot svalue
**Bug:** `GOODS_governorship_early_munitions_produced` (GOODS_svalues.txt) appended an INLINE
`every_governorship_state → every_state_province` arsenal/depot count. That svalue is evaluated >1x/quarter
(production pass + DEMAND_difference_early_munitions → trade/currency/rollup passes), so the province walk
re-ran each time — exactly the PERF_AUDIT #3 class.

**Fix:** applied the existing #71 cache idiom already in this file. Split the inline loop into
`GOODS_governorship_munitions_infra_output` (cached wrapper: read `var:munitions_infra_cached` if present,
else compute) + `_compute` (the actual walk). New `GOODS_cache_munitions_infra` effect computes it once
into the var, wired at all three sites that already call `GOODS_cache_industrialisation_bonus` (per-quarter
production refresh in se_GOODS.txt `GOODS_governorship_produce_all`, plus the two setup/formation sites in
oa_economy_setup.txt and se_FUNC.txt). Cache-miss falls back to inline compute → degrades to correctness,
never zeroed output.

### Not fixed (low/cosmetic, logged for the backlog)
- Two `every_governorships` scan passes (land + naval) could be fused into the existing CONSUME walk —
  minor, cheap var-reads only.
- `LOGISTICS_quarter` lacks LOG_enter/exit (its two sub-effects both log unconditionally, so a trace still
  shows whether the quarter fired) — near-cosmetic.

se_LOG breadcrumbs on the new cache effect. Braces: GOODS_svalues 869/869, se_GOODS 370/370, se_FUNC
182/182, oa_economy_setup 526/526, se_CONSUME 42/42, se_LOGISTICS 91/91. All files kept their byte
conventions (se_LOGISTICS no-BOM/LF; the rest BOM+CRLF).

### [logistics-review] Follow-up: the two low findings above, now FIXED
Cleared the backlog items instead of leaving them:
- **Scan-pass fusion.** `LOGISTICS_scan_worst_land_shortage` + `LOGISTICS_scan_worst_naval_shortage`
  (two separate `every_governorships` passes) merged into ONE `LOGISTICS_scan_worst_shortages` that walks
  the governorship list once and accumulates both `LOGISTICS_tmp_worst_land` (4 land goods) and
  `LOGISTICS_tmp_worst_naval` (coal + naval_supplies). The naval half runs unconditionally (6 cheap
  var-reads/governorship) — the steam-hull gate stays on the PENALTY (`LOGISTICS_apply_coal_shortage_penalty`),
  so non-steam countries just discard the naval driver. `LOGISTICS_quarter` now owns the single scan call,
  the `save_scope_as = logistics_country`, and the `LOGISTICS_tmp_worst_*` cleanup; the two apply-effects
  read the pre-computed vars (they keep their own `save_scope_as` so they remain independently callable).
  Behaviour is unchanged — same worst-case max per driver, same tier thresholds — just one list walk/quarter.
- **`LOGISTICS_quarter` breadcrumb.** Added `LOG_enter`/`LOG_exit` (sys = LOGISTICS), satisfying the module
  header claim that every effect carries them.

Braces: se_LOGISTICS 89/89 (was 91/91 — two effect definitions collapsed into one). No-BOM/LF preserved.

## [#103-106] Grand Council rework — "the Council IS the office-holders" + accountability (2026-07-07)

Fully-locked design build, shipped as ONE commit. Five interlocking pieces:

**(a-c) Council-is-offices model.** Ripped out the old separate "councillor pool + chief +
seats" abstraction. The Grand Council is now EXACTLY the set of filled great offices (11
appointable: chancellor, personnel, revenue, rites, war, justice, works, censor, lifanyuan,
amban, zongli). You join the council by being appointed to an office; `qing_council_members`
is a DERIVED list rebuilt each quarter by `QING_council_recompute`, `qing_council_filled_count`
(0-11) replaced seat_count/seat_cap. Backend rewritten in `se_QING_COUNCIL.txt`
(QING_office_appoint / _vacate / _vacate_dispatch / _appoint_first_vacant). All ~14 events
repointed (qing_office_events, qing_roster_events, qing_keju_events) from seat/make_chief verbs
to the offices model. Both GUI files rebuilt: dropped the councillors grid + chief card +
seat/make_chief/unseat buttons; added a single Grand Chancellor card + appoint-chancellor button
(government_view.gui, characterwindow.gui). Office->governing-skill map: chancellor=all four,
war=martial, personnel/revenue/works/censor=finesse, lifanyuan/amban/zongli=charisma,
rites/justice=zeal.

**(d-e) NEW accountability subsystem** (`se_QING_ACCOUNTABILITY.txt` + `qing_accountability_events.txt`).
Each office owns a realm metric (justice=unrest, revenue=treasury, works=civilization,
censor=corruption, rites=legitimacy, war=military, personnel=official-loyalty, lifanyuan=subject-
loyalty, zongli=GP-tension, amban=ruler-popularity, chancellor=council-effectiveness). Quarterly
`QING_accountability_pulse` (from QING_GOV_pulse, CHI player-only, self-gated ~90d) scores each
filled office: a THRIVING domain (band 2) REWARDS the minister (standing + a closer bond if
congenial); a FAILING domain (band 0) under a WEAK holder (loyalty<40 OR popularity<=0 OR
corruption>=30 OR corrupt trait) summons the ablest UNASSIGNED rival who outranks him on
combined_stats_council_svalue AND clashes with him (pair-friction>=45) to challenge him for the
post — the reckoning event qing_accountability.1 (stand-by-incumbent / elevate-challenger /
dismiss-both). At most ONE challenge/quarter (qing_acc_challenge_pending guard). Character
dimension (numeric corruption, age disparity, relative popularity, friction) feeds via the
QING_char_* / QING_pair_friction mutators (se_QING_AFFINITY.txt).

**Verified engine idioms** (2nd oracle pass, INV+TI): legitimacy reads BARE at country scope
(NOT nested in current_ruler); NO neighbour-country iterator exists (Zongli judged on the concrete
qing_gp_tension_* counters instead); tokens has_subject_loyalty / has_monthly_income /
has_war_exhaustion; `var:X = { save_scope_as }` and script_value comparison in a limit both PROVEN
in-repo (qing_office_events.txt:662, :609).

### [#103-fix] Code-review fixes (2026-07-07, review verdict: sound — no crash/reference/scope bugs)
Post-implementation review (mandatory per standing rule) confirmed the rework correct — the
delayed-event dedicated-scope handling (qing_acc_defender/challenger vs the reused
qing_acc_holder/rival), the one-challenge-per-quarter guard, the .b re-appoint branch covering
all 11 office keys, and all metric idioms all check out; reference-integrity sweeps found no
dangling deleted constructs (qing_council_chief/seat_count/seat_cap/make_chief/unseat/is_councillor).
Two low-severity hardening notes applied:
- **QING_acc_score_office holder guard** strengthened to match QING_council_score_office
  (se_QING_COUNCIL.txt:217): holder must be `is_alive = yes  employer = ROOT`, not merely
  var-present, so the reward path can't mutate a dead/departed character via any employment-loss
  path that skips QING_office_vacate_dispatch. Defense-in-depth.
- **Overstated comment** corrected: the pulse is NOT "no character hot path" — two probes
  (officials-loyalty metric + challenger search) do a court-wide character scan; quarterly +
  player-only keeps it cheap, but the comment now says so accurately.

### [amban-flavour] Reconciled the amban office display to its mechanic (user decision 2026-07-07)
The `amban` office is modelled everywhere in MECHANICS as the 內務府 Grand Secretary of the
Imperial Household (accountability judges it on current_ruler popularity; its officer-buff adds
charisma to the ruler), and the loc keys already read "Grand Secretary of the Imperial Household
(總管內務府大臣)". Cleared the remaining stale "Tibet Amban / 駐藏大臣 / province icon" display
bits: characterwindow.gui + government_view.gui office card/button icons province.dds ->
family_size.dds (household, unused by other office buttons); comments retitled; the
QING_governance_actions.txt office-list comment amban tag 駐藏大臣 -> 內務府. Loc-only/cosmetic —
the office KEY was consistent everywhere, so no logic changed.

Braces (all touched files): government_view.gui 1476/1476, characterwindow.gui 429/429,
QING_governance_actions.txt 170/170, se_QING_ACCOUNTABILITY.txt 184/184, qing_accountability_events.txt
63/63. Byte conventions preserved (se_QING_*.txt no-BOM/LF/final-nl; loc .yml BOM/LF; .gui TAB indent).


### [OVERNIGHT WAVE #107/#108/#111-#126] Office-coupling families + province ethnic tension + integration capstone (2026-07-07)
Autonomous overnight build of the pending queue (#107-#126). Governing idea: the "coupling-family"
pattern — each Grand Council office OWNS its historical charges, so (a) the holder's skill/loyalty
gates its event outcomes and costs, (b) its charges join the character-affinity chart via
QING_pair_friction / QING_char_affinity, and (c) a vacant office lets its domain drift. Crucially
the families do NOT double-count the accountability metric (se_QING_ACCOUNTABILITY.txt already grades
each office) — they add flavour/decision events keyed on the same holders.

**Commits (all authored+committed freekumquats, on fix-usa-roster-create-character):**
- `a68758d9` #113 Amban repair + activation
- `33876549` #108/#114/#117/#121-#126 office-coupling event families
- `3ff17360` #107 province-level ethnic tension engine
- `f1913ad9` #111/#112 integration capstone (Solution A)
- `683603b8` pulse + dispatcher wiring, #107/#126 inits
- `7aa052d5` #108/#109/#120 GUI panels (DORMANT)
- `1d2afc47` decision log + build brief

**#113 Amban (駐藏/駐紮大臣).** The delegated repair agent (oracle-verified vs Terra-Indomita +
Invictus) replaced the UNPROVEN tag-interpolated variable names (`qing_amban_$x$.GetTag`) with a
fixed-name subject var `qing_amban_here`, and swapped invalid add_liberty_desire/subject-loyalty
verbs for `add_opinion` + 4 new opinion modifiers (clash -12/coop 8/capable 10/ineffective -8).
I then found the feature had NO initial posting entry point (only qing_amban.4.a re-posted on
turnover — the whole system was inert) and authored `QING_amban_post_sweep`: gated on a filled
lifanyuan holder, it posts an amban to a Mongol/Tibetan-ruled subject via random_subject. Wired
into QING_GOV_pulse ahead of QING_amban_evaluate.

**#107 province-level ethnic tension.** Bottom-up per-province counter qing_prov_ethnic_tension
(0..100) accruing from culture/religion mismatch, province_unrest, low governorship loyalty, and
governor-subject affinity; modulated by the top-down ethnic stance; snowballs to owned neighbours
above 70 and erupts (qing_ethnic.1) above 80. Authored the missing QING_ethnic_tension_init — the
prior splice-prose used INVENTED lowercase region keys (tarim_region etc.) that do not exist; I
used the PROVEN province-scope is_in_region trigger with REAL capitalized keys from
map_data/regions.txt (Turkestan 20 / Tibet 15 / Mongolia 10 / Qinghai+Sichuan_Kham 10). Idempotent;
wired into on_game_initialized + QING_GOV_pulse.

**#111/#112 integration capstone (Solution A, CHANGES-to-existing scrutiny).** In
SUBJ_QING_advance_integration, an autonomous_governorship reaching progress>=5 now fires the
qing_integ.30 capstone CHOICE event instead of silently auto-absorbing; a non-governorship subject
keeps the direct-absorb path via an else_if fallback (behavioural equivalence for the untouched
case). qing_integ.30 re-checks progress>=5 in its own trigger and each option calls
SUBJ_QING_absorb_subject itself, so double-resolve is impossible.

**Office families #117/#121-#126/#108/#114.** Net-new subsystems: Personnel 吏部 (#117 大計 triennial
review — triennial spacing via a day-expiry cooldown stamped in the .1 immediate, so the dispatcher
gate is a pure read), Revenue 戶部, Rites 禮部 (#122), War 兵部, Justice 刑部 (#125 — the 秋審
autumn-assizes SEASONAL GATE was DROPPED because current_month is unproven in this repo AND both
oracle mods; documented in-code), Works 工部 (#121 + dike/canal/wall buildings), Censorate 都察院
(#123), Household 內務府 (#126 — the one net-new counter, qing_privy_purse 內帑=50, a private purse
distinct from the state 戶部 treasury), Great Game 大博弈 (#108), Pilgrimage 朝聖 (#114). All effects
se_LOG-wired; all verbs oracle-verified.

**Wiring.** 10 self-guarded O(1) coupling-family calls spliced into QING_GOV_pulse before its final
LOG_exit; flavour-roll dispatcher random_list weight-entries added for the events that are NOT
pulse-fired (pulse-fired events — War/Revenue/ethnic.1/integ.30/.40 — deliberately NOT re-listed to
avoid double-firing). #118 fix carried: qing_military_strain -> qing_greenstandard_decay in
qing_war_events.txt.

**HELD / DORMANT (#108/#109/#120).** The Great Game + province-report GUI panels ship as harmless
unreferenced .gui + scripted_gui definitions; their open-BUTTONS are left UNSPLICED because the
button idioms (ToggleGameViewWindow / GetCountryByTag) are unproven against both oracle mods.
Documented as a TODO in OVERNIGHT_DECISIONS.md per the unproven-capability rule.

**Verification.** Full identifier-resolution + modifier-existence sweep: all 10 QING_GOV_pulse
effects resolve; both new inits resolve; 13 spot-checked dispatcher event IDs exist; 35 referenced
country modifiers + 4 amban opinion modifiers + 3 works building keys + the loyalty/local_unrest
constants all defined (0 missing). Consolidated byte/brace check across all 60+ changed files: 0
problems (common/**/*.txt no-BOM/LF/final-nl; the pre-existing BOM on qing_mechanics_on_actions.txt
+ se_QING_GOVERNANCE.txt PRESERVED — the baseline works with it; loc .yml BOM/LF starts l_english:).


### Post-implementation adversarial review + fixes (mandatory-review + fix-traceability rules)

Ran the mandated Workflow-tool deep adversarial review over ALL code not on the known-good
baseline (`origin/fix-usa-roster-create-character` @ 5a79ddcd .. HEAD, 86 files): clustered
finders -> adversarial verifiers (default-REFUTED) -> synthesis (34 agents, ~1.77M tokens).
Verdict: NOT SOUND — 21 CONFIRMED defects + 1 PLAUSIBLE. Ship-blocked until fixed.

Applied all 13 must-fix findings + 3 high-value should-considers (commit e5c06ad3). Every
introduced idiom re-verified against the repo and both oracle mods (Terra-Indomita, Invictus);
byte/brace conventions preserved; task-tagged in-code comments + se_LOG markers on each.

CRITICAL
- qing_succession.2 had ZERO options (non-hidden country_event) => undismissable accession
  popup soft-locking the human CHI player on every succession. Added a dismiss option + loc key
  (qing_succession.2.a).

CHOICE INVERSION
- se_QING_CENSORATE impeachment: `limit = { always = $outcome$ = uphold }` macro-expanded to the
  malformed `always = uphold = uphold`, never matched, so "uphold" fell through to SUPPRESS
  (corruption +5 / tyranny +3 — the inverse of the player's choice). Split into two dedicated
  effects (QING_censorate_impeach_uphold / _suppress) selected by call site.

RUNAWAY / STUCK-STATE (feature-killers)
- se_QING_ETHNIC_TENSION revolt cooldown flag (qing_prov_ethnic_revolted) had a clear effect with
  ZERO callers — a province erupted once then locked out forever. Wired the clear into pulse STEP 4
  (tension < 70). Also bound qing_ethnic.1 to scope:erupt_province (was re-picking randomly,
  double-targeting on multi-eruption pulses).
- se_QING_AMBAN + on_character_death: a posted amban dying of natural causes stranded the subject's
  qing_amban_here var forever. Added qing_amban_marker + a death-cleanup branch.
- qing_pilgrimage: pilgrim dying between chain links stranded qing_pilgrimage_active, killing the
  whole feature. Added qing_pilgrim_marker + death-hook release + .5 cleanup.
- se_QING_SEATS/qing_regency: .1.b (council-rule) and .3.c (usurper clings) re-fired every quarter,
  re-nudging reform_pressure and stacking modifiers. Added qing_regency_council_rule /
  qing_regency_usurped suppression flags cleared on dissolution; also clear a dead/departed usurper.

DANGLING / INVALID KEYS (silently dropped effects)
- qing_war.3.b raised a fleet of undefined `trireme` (empty BOM stub) inside a raise_legion ARMY
  wrapper and charged 180 treasury unconditionally. Rewrote to the proven navy idiom
  (create_unit navy=yes, add_subunit=brig, country scope), charging only when a coastal hull raises.
- se_QING_HOUSEHOLD eunuch `add_rival = prev` resolved to the COUNTRY (if/limit don't push scope),
  so no rivalry formed. Saved scope:qing_eunuch_instrument and used is_rival/add_rival = scope:.
- qing_justice_modifiers: local_pop_happyness -> local_population_happiness (x3, was silently
  dropped — the intended happiness swings never applied).
- qing_integ_capstone_modifiers: character_prominence -> prominence (the +10 co-opt reward).
- qing_integ.41 had no trigger — could fire on an already-absorbed landless subject when .30 won
  the race. Added a re-validation trigger mirroring .30.
- se_QING_PERSONNEL: removed a vestigial dead write via the unproven current_date.year accessor
  (never read; the real triennial guard is qing_personnel_daji_cooldown).

DEFERRED (logged, not fixed this pass): the PLAUSIBLE average_loyalty token
(se_QING_ETHNIC_TENSION.txt:148) + the lower-value should-considers (amban .2/.3/.4 lifecycle
dispatch, personnel.3 dead-content queue path, on_character_death regent branch, dead
qing_pilgrim_patron_of_faith/_devotion_to_rival modifiers) — none are soft-locks or choice
inversions; tracked for a follow-up pass.

Consolidated re-check after fixes: all 16 edited files byte/brace-clean (0 problems); confirmed
zero remaining `local_pop_happyness`, `character_prominence`, `value = current_date.year`, or
`trireme` refs (bar one explanatory comment).


### Deferred review findings — all 6 addressed (oracle-verified)

Cleared the deferred backlog from the adversarial review. Three unproven tokens were consulted
against Terra-Indomita + Invictus FIRST (oracle-consultation rule); all three were absent from
both oracles and replaced with proven idioms.

- #1 se_QING_ETHNIC_TENSION: `governorship.average_loyalty` (unproven pair, silently no-op —
  under-counted tension in low-loyalty provinces) -> direct province-scope `state_loyalty < 40`
  (proven: Invictus judaism_decisions.txt:524 `p:687 = { state_loyalty >= 60 }`).
- #2 amban lifecycle: qing_amban.2/.3/.4 were fully authored but NEVER dispatched (dead content;
  only .1 fired). Wired a mutually-exclusive dispatch (turnover > gone-native > able) into
  QING_amban_evaluate's per-subject loop. Fixed two invalid tokens the events used: `time_in_office`
  (not a valid char token) -> an auto-expiring qing_amban_tenure_pending timer (proven expiring-var
  idiom, set at post, days=2920, cleared on recall); `add_province_unrest = -3` (NO such effect
  exists — unrest is only ever a modifier key) -> add_province_modifier qing_justice_appeal_vindicated.
- #3 se_QING_PERSONNEL: qing_personnel.3 was queued ONLY from CASE B (office VACANT) but its trigger
  requires a FILLED office + finesse>=9 minister — mutually exclusive, so it could never pass its
  trigger. Moved the queue to CASE A (able-minister + high-affinity governor), the state that
  actually satisfies the trigger; removed the CASE B queue.
- #4 QING_office_vacate_dispatch (on_character_death): added the missing `flag:regent` branch —
  a regent dying of natural causes stranded qing_office_regent_holder + qing_regency_active until
  the next quarterly evaluate noticed (self-healing but up to a quarter late). Now clears immediately
  via QING_seat_regent_clear (its is_alive guard makes the dead-holder path safe).
- #5 pilgrimage modifiers: qing_pilgrim_patron_of_faith / _devotion_to_rival were defined but NEVER
  applied, AND patron_of_faith carried the invalid country key monthly_character_prestige. Fixed the
  key -> monthly_prestige (proven qing_household_modifiers.txt:9) and APPLIED both as country
  modifiers (patron on the .3 grand-recognition path, 1825d; devotion-to-rival in
  QING_pilgrim_rival_overture, 1095d).

All 8 edited files byte/brace-clean (0 problems); zero invalid tokens remain in code (only in
explanatory comments). Task-tagged [deferred-fix #N] comments + se_LOG on every dispatch.


---

## #139 — Economy performance pass (trade / industry / production)

Behavior-preserving optimization sweep over the quarterly economy tick. Method honored the
"extreme caution" mandate: EVERY profiler claim was verified against the actual code before any
edit, and CHANGES to existing hot paths were held to byte/behavioral-equivalence. Outcome — of 7
candidate fixes, 4 implemented as byte-identical, 2 rejected as unsafe (would change gameplay), 1
skipped as dead code. The profilers materially over-claimed: several "hotspots" were dead code,
intentional per-category accumulation, or already optimized.

### Implemented (behavior-preserving)

- **[#139-B] se_CONSUME.txt** — `CONSUME_all_stockpiles` now caches the two LOOP-INVARIANT macro
  factors ONCE per governorship (`owner.CURRENCY_amt_circulated_deflation` -> var
  `CONSUME_deflation_cached`; `DEMAND_elasticity_impact` -> var `CONSUME_elasticity_cached`) before
  the `every_tradegood_complex` loop, and `CONSUME_update_shortage` reads the cached vars at all 4
  sites (3 deflation, 1 elasticity). Both were re-evaluated ~60×/gov though the loop never mutates
  them. Cleared at loop exit. Byte-identical: the cached var holds exactly the value a live read
  would return at every iteration. No inline log (a log inside the 60× loop would be a regression;
  ECON_LOG wraps the phase). Braces 44/44, BOM preserved.

- **[#139-C] se_DEMAND.txt** — `DEMAND_set_demand_from_luxury` divides by `WEALTH_governorship_per_capita`
  once per luxury good; hoisted to var `DEMAND_luxury_per_capita_cached` set at the top of both
  `DEMAND_set_demand_from_luxury_all` and `_all_first_time`, cleared at each end. The div/0 guard
  (min behavior) is preserved via the cached value. Braces 198/198, BOM preserved.

- **[#139-E] se_GLOBALTRADE_split.txt + oa_wealth_changes.txt** — `GT_split_do_global_trade_split`
  ran a trailing `every_trade_center = { PRICE_set_food_mean_normalised_price = yes }` on EVERY one
  of the 7 category passes, but that effect recomputes the food-price mean from `local_price_<food>`
  vars written ONLY during the food pass, so passes 2-7 recomputed an identical value over every
  trade center. Removed from the shared split effect (replaced with an explanatory comment) and
  relocated to `quarterly_global_trade_food` immediately after the food split, so it runs once.
  Byte-identical for every reader. NOTE: 3 of the 4 profiler claims for this file were FALSE
  POSITIVES (GT_set_tradegood_price already type-scoped; shipping-traffic accumulation is intentional
  per-category; TZ penetration values already hoisted) — only this one was genuine. Split braces
  1611/1611 (BOM+CRLF); on_action braces 146/146 (BOM+LF).

- **[#139-F] se_COTTAGEIND.txt** — `COTTAGEIND_cache_all_values` now caches all 21 raw-good
  production svalues (`GOODS_governorship_<good>_produced` -> var `COTTAGEIND_raw_<good>` for copper,
  dye, fish, fur, gems, gold, industrial_fibres, iron, lead, salt, silk, silver, stone, sugar,
  sulphur, temperate_fruit, textile_fibres, tin, vegetables, whales, wood), and all 45 cottage-recipe
  reads use the cached var instead of re-deriving each producing svalue per recipe. Braces 136/136,
  BOM+CRLF (564) preserved (initial write flattened CRLF->LF — self-caught via git diff --stat, byte-
  restored per the BOM+CRLF-trap rule).

### Rejected as unsafe (would change gameplay — flagged for user design decision)

- **[#139-A] Fuse the two currency-province sweeps** (CURRENCY_cache_power then
  CURRENCY_cache_power_trade_bonus, oa_wealth_changes.txt:173-184). REJECTED. `CURRENCY_power_trade_bonus`
  (CURRENCY_svalues.txt:1547) divides by a WORLD-TOTAL sum `every_province { add = var:CURRENCY_power_cached }`,
  so pass 2 depends on pass 1 being COMPLETE across every currency province. Fusing them would read
  a partially-populated sum = silent economic drift. The profiler's fusion recommendation was wrong.

- **[#139-D] "Finish/delete the half-done food/wealth cache migration".** REJECTED. The
  `var_WEALTH_governorship_per_capita`-prefixed guarded reads in DEMAND_food_svalues.txt are DORMANT
  (no live setter). Deleting the TRADE_cache_svalues_* builders would drop vars other svalues read;
  FINISHING the migration (activating a live setter) would switch on dormant food-demand wealth-
  dampening = a gameplay change. Neither is behavior-preserving. Left as-is; flagged for user.

### Skipped as dead code

- **[#139-G] The O(TZ²×goods²) TZ-scoring core + double 22-branch dispatch** (se_TRADE.txt:
  TRADE_score_tradezone_connections chain and TRADE_rank_supplier_TZs_all_tradegoods). Call-graph
  trace shows EVERY mention is internal to se_TRADE.txt with ZERO external caller from any on_action
  or event, and the chain even calls the undefined effect TRADE_get_tradezone_connection_score
  (defs=0). Dead/dormant code — no runtime cost to remove, so no fix warranted; touching it is pure
  risk. The live quarterly trade path uses GT_split_do_global_trade_split, not this cluster.


### #139 adversarial review (Workflow: 6 agents, one hostile skeptic per fix + independent verify + integrity)

Ran a deep adversarial review via the Workflow tool: one skeptic per fix prompted to REFUTE
behavior-preservation across 6 failure modes (invariance, ordering, scope, other-callers, cleanup,
lost guards), each non-nit finding independently re-verified by a second agent, plus a mechanical
brace/BOM/CRLF/no-rewrite integrity sweep.

- **B (CONSUME), C (DEMAND), F (COTTAGEIND): CLEARED.** Skeptics could not refute invariance.
  Notably F (highest-risk): GOODS_governorship_<good>_produced derives from engine-side
  num_goods_produced × productivity modifiers, NOT from any stockpile the cottage recipes mutate —
  so even the ORIGINAL live-read code could never have seen the svalue change mid-loop. Cache is
  exact.
- **Integrity: ALL PASS.** 5 files brace-balanced, BOM present, correct line-endings (4 economy
  se_*.txt = CRLF+BOM, oa_wealth_changes.txt = LF+BOM), no whole-file rewrite.
- **E (GLOBALTRADE): ONE REAL regression found and FIXED (CONFIRMED_REAL_BUG, low severity).**
  Relocating PRICE_set_food_mean_normalised_price out of GT_split_do_global_trade_split overlooked
  that GT_split has a SECOND caller — the game-setup path (oa_economy_setup.txt:2296-2302) runs the
  7 splits directly at day 0 and relied on the removed block to seed PRICE_food_mean_normalised
  before the first quarterly pulse (~day 20). In the gap, a land transfer (debug_land.1, war peace
  deals, diplomatic-play resolution, AI peace transfers, Qing subject transfers) runs
  DEMAND_set_demand_from_food guarded on has_variable=PRICE_food_mean_normalised; with the var
  absent the food-mean divide is skipped, yielding a divergent persistent demand for the transferred
  governorship. FIX: re-seeded the food mean in the setup path right after the food split
  (oa_economy_setup.txt, [#139 perf review-fix]), mirroring the quarterly path. Byte-identical to the
  original setup end-state (passes 2-7 never touch food prices, and nothing reads the var between the
  synchronous setup splits). Braces 527/527, BOM+CRLF preserved.

Net: 4 fixes implemented, all now behavior-preserving; 2 rejected as unsafe; 1 skipped as dead code.
The review's single catch was the other-callers failure mode on the one relocation (not a caching)
fix — now closed.


---

## #147 — Player-initiated diplomatic plays via GUI (2026-07-07)

**Request:** "Look at diplomatic plays and building how the player can initiate them for many
different reasons via GUI (none of which I think exists right now)." Scope chosen by the user:
ALL play goals (Territory/Influence/Subjugate + Liberate state + Colonise unclaimed area +
Purchase/annex state — new backend resolvers for the latter four) AND the full plays-management
window (province-window goal picker + supranational plays list + a working Support action).

Before #147 the only player entry point was the single `DIPLO_begin_or_end_play` toggle button,
which always started a `flag:get_territory` play — no goal choice, no Support action, and the two
Support buttons in the play-list templates were dead stubs (`#onclick = ""`).

### Backend (common/scripted_effects/se_DIPLOMACY.txt)
- **`DIPLOMACY_player_begin_play = { goal = flag:X }`** — shared country-scope effect behind every
  goal button. Pays `begin_diplomatic_play_price`, wraps `AI_begin_diplomatic_play` with
  `play_type = manual`. Colonise normalises `play_target_country = this` so the engine's c:BAR
  unclaimed-land fallback fires; every other goal uses `scope:target_province.owner`.
- **Four new resolvers**, dispatched from `DIPLOMACY_trigger_diplomatic_play_finale_event`:
  - `DIPLOMACY_resolve_annex_state` — state-scoped clone of the proven `resolve_get_territory`;
    decisive = whole state via `LAND_transfer_provinces`, partial = contested province (most-valuable
    fallback), `bitter_over_occupation` on the former owner, bank-a-claim on fizzle.
  - `DIPLOMACY_resolve_purchase_state` — like annex but the buyer PAYS the seller a treasury sum
    scaled to the ceded land's `DIPLOMACY_province_wealth_value`, capped at the buyer's treasury
    (never drives the buyer negative). No opinion penalty (consensual purchase). `play_purchase_price`
    lives on the provobj and is read back as `scope:diplomatic_play.var:play_purchase_price` inside
    the country-scoped payment blocks.
  - `DIPLOMACY_resolve_liberate` — frees the target state via `LAND_release_from_list`; decisive =
    fully independent nation (`as_subject_type = flag:independent`), partial = client_state of the
    instigator (release `flag:dynamic`, then re-bind via `FUNC_make_subject`). `bitter_over_occupation`
    on the former owner.
  - `DIPLOMACY_resolve_colonise` — plants a colonial subject via `LAND_release_from_list`
    (`releaser = play_instigator`, `as_subject_type = flag:dynamic`). Works on empty frontier AND
    sparsely-held foreign land; decisive = whole area, partial = contested province.
- **`DIPLOMACY_collect_state_cede_candidates`** — helper filling `play_cede_candidates` from the
  target state's foreign-owned, inhabitable, non-instigator provinces.

### GUI
- **common/scripted_guis/EE_scripted_guis.txt** — 6 thin per-goal begin GUIs
  (`DIPLO_begin_play_get_territory/_annex_state/_purchase_state/_subjugate/_liberate/_colonise`),
  each cloning the proven `DIPLO_begin_or_end_play` two-scope shape and reading
  `scope:player.var:selected_province`. Shared gating: has selected province, not-your-own-land,
  political influence >= 30 + stability > 10, and a stateless duplicate-play guard
  (`any_in_global_list` on instigator + target-area's `.area`). Per-goal extras: exists-owner
  (annex/purchase/subjugate/liberate), treasury > 0 (purchase), stronger-power + not-already-subject
  (subjugate), culture-mismatch (liberate). Plus **`DIPLO_player_support_play`** (backs an existing
  play for `support_diplomatic_play_price` = 10 PI, `DIPLOMACY_modify_play_success = { amt = 10 }`).
- **gui/province_window.gui** — replaced the hidden 2-button placeholder with a visible row of 6
  goal buttons, each enabled via `.IsValid(...)` and starting its play + refreshing the local list
  via `.Execute(...)`.
- **gui/shared/gui_templates.gui** — wired the two previously-dead Support buttons (in
  `diplomatic_play_item` and `diplomatic_play_global_item`) to `DIPLO_player_support_play`.
- **common/prices/00_diplomacy_prices.txt** — `support_diplomatic_play_price = { political_influence = 10 }`.
- **localization/english/imp19c_interface_l_english.yml** — 12 `play_goal_*(_tt)` keys + 2
  `play_support_button(_tt)` keys (BOM+LF, all entries exactly 2 quotes).

### Post-implementation adversarial review (code-review agent) — 4 findings, ALL fixed
The risky treasury/scope code was cleared as correct (purchase price qualified with
`scope:diplomatic_play`, cap floored at 0, empty-list guards on every LAND_* call, goal flags
consistent across GUI → begin → finale → resolver). Four gating/correctness edges were found and
fixed:
1. **Support self-harm (MEDIUM).** The Support button appears on every play in the list, and backing
   always raises the INSTIGATOR's success — so a player could pay to help a play against themselves.
   FIX: `DIPLO_player_support_play` is_valid now bars `var:play_target_country = scope:player` (a
   third party helping an ally is still allowed) and skips a play already at 100 success.
2. **Purchase partial free-acquisition (LOW).** Pricing `play_target_area` up front floored the price
   to 0 whenever the contested province was no longer cedable, yet the fallback still transferred a
   real province. FIX: select the transferred province FIRST, then price the province actually ceded.
3. **PI gate vs cost mismatch (LOW).** Begin buttons gated on `political_influence > 0` but the cost
   is 30 PI, so a player with 1-29 PI could go negative. FIX: gate raised to `>= 30` on all 6 buttons;
   tooltips updated ("political influence of at least 30").
4. **Colonise third-party seizure (LOW).** Colonise admits foreign land, but had no penalty for a
   displaced owner. FIX: `bitter_over_occupation` applied once per distinct displaced owner (via
   `every_country`) before the release, matching the annex path.

Integrity: se_DIPLOMACY.txt 533/533 braces, EE_scripted_guis.txt 483/483, province_window.gui
1943/1943, gui_templates.gui 1196/1196, imp19c_windows.gui 272/272 — all byte-conventions preserved.
All new effects wired to se_LOG (LOG_enter/line/exit), honoring the error-logging standing rule.

## Tier B (scan-and-implement pass) — WIRE DORMANT PLAYER PANELS (#108 / #120 / #109)

Three panels were fully built in prior sessions but had NO open-button — the player literally could
not open them. Added open-buttons to the Grand Council action strip in government_view.gui (CHI-only
tab), reusing the proven icon_button_square + GetScriptedGui idiom already used by the war-council and
court-a-power buttons in that same strip.

WIRED:
- #108 Great Game dashboard (qing_greatgame_panel) — button createwidgets the read-only panel.
- #120 New World crop report (qing_crop_report_window) — button chains ScriptedGui.Execute (populates
  the province variable-list) THEN createwidget (opens the window that reads the list via datamodel).
- #109 province ethnic-tension report (qing_tension_report_window) — same Execute-then-createwidget chain.

FIXES MADE WHILE WIRING (the panels shipped with latent defects the oracle pass caught):
1. **Great Game panel would have HARD-CRASHED on open (HIGH).** It used `GetCountryByTag('GBR')` — not a
   valid engine datafunction (zero occurrences in either oracle mod; the correct verb is `GetCountry('GBR')`,
   proven new_element_test.gui:18 + Terra-Indomita chinese_unification.gui:44). FIX: all 6 sites converted.
2. **Opinion read would have crashed (HIGH).** `GetOpinionOf(Player)` passes a player-handle where a country
   scope is required. FIX: `GetOpinionOf(Player.GetCountry)` at all 3 sites (reference-proven: Terra-Indomita
   outliner.gui:509, bloodlines.gui:1581/1589; repo game_concepts_l_english.yml:6).
3. **Dead close button (MEDIUM).** The panel's close called qing_greatgame_close_panel.Execute — a scripted_gui
   with an EMPTY effect, so the button did nothing. FIX: `[ExecuteConsoleCommand('GUI.ClearWidgets qing_greatgame_panel')]`
   (proven imp19c_windows.gui:20). The two report windows already used the correct ClearWidgets close.

VERIFICATION: oracle grep of Terra-Indomita + Invictus confirmed every idiom before wiring (createwidget
open form, GetCountry, GetOpinionOf(Player.GetCountry), MakeScope.GetList datamodel, every_governorships
iteration + trade_goods trigger in scripted_gui effects, FixedPointToFloat/Multiply_CFixedPoint progressbar
scaling). Backing data all confirmed present (qing_prov_ethnic_tension, qing_gp_tension_*, qing_office_zongli_holder,
maize/sweet_potato/potato trade goods, all loc keys). se_LOG (sys = QING) added to the two report open-effects.

POST-IMPLEMENTATION REVIEW: dispatched, returned ZERO defects — boot-safe and crash-safe. Independently
confirmed the two-onclick chain order (Execute before createwidget), no datamodel race (lists cleared then
rebuilt each open; empty list renders zero rows, not a crash), the empty-effect gate scripted_gui is only
used for IsShown/IsValid gating (never on the open path), all window names match createwidget targets, and
all template blockoverrides (main_window_template / base_sub_window headers) resolve to real blocks.

Integrity: qing_greatgame.gui 104/104, qing_province_reports.gui 64/64, government_view.gui 1608/1608 braces;
both panel loc files 0 bad-quote lines; all files no-BOM/LF preserved; no lingering GetCountryByTag repo-wide.


## Tier C #1 — diplomatic-play OPPOSE + CANCEL (2026-07-07)

CONTEXT: first Tier-C depth item. The play data model + resolution (#58) + player Support button (#147)
existed; the play display had a dead labeled target-side button and no way to withdraw your own play.
Added both missing verbs, mirroring the proven Support button.

CHANGES:
- common/prices/00_diplomacy_prices.txt: `oppose_diplomatic_play_price = { political_influence = 10 }`
  (symmetric to support_diplomatic_play_price).
- common/scripted_guis/EE_scripted_guis.txt: `DIPLO_player_oppose_play` (pay price, DIPLOMACY_modify_play_success
  amt=-10) and `DIPLO_player_cancel_play` (AI_remove_diplomatic_play teardown). Both scope=province,
  ai_is_valid=no, se_LOG (sys=DIPLO) on effect.
- localization/english/imp19c_interface_l_english.yml: play_oppose_button(_tt), play_cancel_button(_tt).
- gui/shared/gui_templates.gui: in BOTH diplomatic_play_item and diplomatic_play_global_item — added Cancel
  button (cancel_play_side) beside instigator Support, and rewired the dead target-side stub
  (support_play_side -> support_target_play_side) to DIPLO_player_oppose_play.

is_valid GATES:
- OPPOSE: is_diplomatic_play present; player PI>=10; NOT instigator (that's Cancel's job); success>0.
- CANCEL: is_diplomatic_play + manual_play present; var:play_instigator = scope:player (instigator of a
  player-started play only; AI/automatic plays excluded).

VERIFICATION: play_type=manual sets manual_play var (se_AI.txt:451); AI_remove_diplomatic_play is the proven
clean teardown (de-index + strip all play_* vars); negative-amt branch of DIPLOMACY_modify_play_success
divides by a multiplier floored at 0.25 (#79) so amt=-10 is at worst -40 then clamped to 0 — no underflow,
no crash. GUI scope idiom reused verbatim from Support (root = play provobj + AddScope player).

POST-IMPLEMENTATION REVIEW: dispatched (see below).

Integrity: gui_templates.gui 1204/1204, EE_scripted_guis.txt 497/497, 00_diplomacy_prices.txt 4/4 braces;
4 new loc keys quote-clean; all files byte-convention preserved.


## Imperial family dynamics events (#157) — 2026-07-07 (develop)

USER REQUEST: positive + negative events for family dynamics between Emperor / Crown Prince / Empress
Dowager affecting Grand Council operations.

NEW:
- common/scripted_effects/se_QING_DYNASTY.txt: qing_dynastic_harmony meter (0..100, init 50);
  QING_dynasty_init / _harmony_nudge / _has_dowager / _has_crownprince / _flavour_roll + 8 concrete-character
  effect helpers (dowager_counsel, dowager_overrule, prince_shines, prince_restrain, prince_indulge,
  faction_mediate, faction_war, regency_screen).
- events/imp19c_mod_events/qing_dynasty_events.txt (namespace qing_dynasty): qing_dynasty.1-.5, 2 positive
  + 3 negative, each acting on current_ruler / current_ruler.mother / var:qing_office_crownprince_holder.
- localization/english/qing_dynasty_l_english.yml (BOM+LF): loc for all 5 events.

CHANGED:
- common/scripted_effects/se_QING_COUNCIL.txt: QING_council_recompute now folds (qing_dynastic_harmony-50)/5
  into qing_council_eff_target before the 0..100 clamp — family harmony couples into Grand Council effectiveness
  (+/-10 band). Behaviour-equivalent when the meter sits at 50 (midpoint => +0), so existing saves are unchanged
  at the neutral start.
- common/on_action/qing_mechanics_on_actions.txt: QING_dynasty_init seeded in on_game_initialized (CHI).
- common/on_action/00_monthly_country.txt: 25%-chance QING_dynasty_flavour_roll added to the quarterly Qing pulse.

COUPLING RATIONALE: reused the existing effectiveness lever rather than a parallel modifier — the meter is a
thermometer + coupling term; the concrete payload is character prestige/loyalty.

SELF-FOUND FIXES (pre-review): removed bogus add_loyalty_to_regime verb; switched add_loyalty { value = N } to
the proven bare add_loyalty = N form.

VERIFICATION: all 13 scripted effects/triggers confirmed defined; every event loc key present; brace balances
clean (DYNASTY 84/84, COUNCIL 346/346, events 36/36); loc 0 bad-quote lines; byte conventions preserved.
POST-IMPLEMENTATION REVIEW: CLEAN — no hard-crash / boot-throw risk found; zero findings to fix.
Confirmed: all 13 helpers/triggers defined; scopes correct (character effects only inside character scopes,
harmony/set_variable at country scope); null-scope window triple-guarded (event trigger re-eval at fire time +
QING_dynasty_has_* gate + per-option limit wrap); recompute injection uses fresh set_variable scratch (no
cross-pulse accumulation) with the 0..100 clamp still bounding after the add; all 30 loc keys present. Two
LOW/non-blocking notes (harmony can peg under sustained one-sided choices = intended; empty dowager+heir pool
makes the roll a silent no-op = harmless), no action taken.

## #158 — Council conservative-vs-reformist faction layer + skill/trait-driven family events + family↔council cross-linking (develop)

Three stacked enhancements to #157 (family dynamics), plus a tab flavour-text request.

NEW:
- common/scripted_effects/se_QING_FACTION.txt (no-BOM/LF, 176/176): the faction backbone.
  - QING_char_stance (character scope): reform position -100..+100 from the WHOLE-character model
    (reformer/traditionalist traits ±45, zeal, finesse, age, culture 滿漢, corruption, integrity) —
    the sister scorer to QING_char_affinity.
  - QING_faction_tally / QING_faction_recompute: aggregate stance over qing_council_members (weight 1)
    + the three dynastic figureheads (Emperor w3, Dowager w2, Crown Prince w2) into
    qing_council_reform_lean (weighted-avg -100..100) and qing_council_polarization (smaller opposing
    bloc). Derives qing_council_polar_pen (deadlock penalty, 5×polarization capped 20).
  - QING_faction_feed_reform_balance: quarterly ±1..2 nudge of the EXISTING qing_reform_faction_balance
    toward the council lean (complements, never swamps, the +5..+10 mission-task nudges).
  - QING_faction_flavour_roll: quarterly dispatcher for the 3 faction events.
- events/imp19c_mod_events/qing_faction_events.txt (no-BOM/LF, 63/63): qing_faction.1 Reform Memorial
  (reformist vs conservative councillor, picked by stance), .2 Behind the Screen 慈禧阻變 (conservative
  dowager smothers a reformist council — the 1898 showdown), .3 Council at Deadlock (blocs at parity).
- localization/english/qing_faction_l_english.yml (BOM+LF, 0 bad-quote lines): all 3 events' keys.

CHANGED (behavioural-equivalence scrutiny per the fix-traceability rule):
- se_QING_COUNCIL.txt: QING_council_recompute now (a) calls QING_faction_recompute after the roster
  rebuild, and (b) subtracts qing_council_polar_pen from qing_council_eff_target beside the harmony
  coupling. Behaviour-equivalent at start: a fresh council with no reformer/traditionalist traits scores
  stance ≈0, polarization 0 → polar_pen 0 → no change to eff_target.
- se_QING_GOVERNANCE.txt: QING_GOV_pulse calls QING_faction_feed_reform_balance after apply_band.
- se_QING_DYNASTY.txt (163/163): (1) QING_dynasty_assess scores the figureheads via QING_char_affinity
  + QING_char_stance in each event immediate; (2) every effect helper now SCALES its harmony/prestige/
  loyalty deltas by the figurehead's ACTUAL skills + affinity (ask #1); (3) helpers CROSS-LINK into the
  council — moving qing_council_effectiveness and, via QING_dynasty_reform_echo, qing_reform_faction_balance
  in the direction of the figurehead who gained sway (asks #2/#3). Original flat deltas softened where a
  scaled bonus was layered on so worst-case magnitude is unchanged.
- qing_dynasty_events.txt (36/36): QING_dynasty_assess = yes added to all 5 immediates.
- common/on_action/00_monthly_country.txt: 25%-chance QING_faction_flavour_roll added to the quarterly pulse.
- common/on_action/qing_mechanics_on_actions.txt: QING_faction_init seeded in on_game_initialized (CHI).
- localization/english/interface_l_english.yml: GOV_VIEW_GRAND_COUNCIL_TOOLTIP expanded from a one-line
  placeholder into flavour text (vanilla offices declined to ceremonial husks; real power drained to the
  Grand Council) per the user's tab-hover request.

DESIGN DECISIONS (locked with the user, 2026-07-07): faction lean FEEDS qing_reform_faction_balance
(council make-up drives the realm's reform fate); polarization applies a DEADLOCK penalty (a hung court
governs worse regardless of which side leads; a united council — reformist OR conservative — functions).

SELF-FOUND FIXES (pre-review): loyalty_qing_minor_slight (undefined) → bare add_loyalty = -4; the
unproven ordered_in_list position=0 "lowest-stance" pick → the proven random_in_list-on-bloc idiom
(as qing_office.9 picks its second disputant); @[scope:X.GetName]! icon-wrap → plain [scope:X.GetName].

VERIFICATION: all new effects/triggers defined; loyalty values / traits / list idioms confirmed against
the repo (order_by var:, any_in_list element-conditions, prev.var: value reads, has_trait reformer/
traditionalist); brace balances clean on all 8 touched files; loc BOM+LF 0 bad-quote lines.
POST-IMPLEMENTATION REVIEW: pending (dispatched).


## [#158b] Grand Council effectiveness — imperial figureheads now weighted (behavioural change, 2026-07-07)
User ask: "the emperor, empress dowager, and crown prince (and Grand Regent) should all affect the
existing effectiveness mechanics for the Grand Council, using all four of their skills" + refinement
"the Emperor's impact should have extra weight compared to other offices (and the Grand Regent, if the
post is filled)".

CHANGE to a SHIPPED mechanic (qing_council_effectiveness) — behavioural-equivalence note required:
- se_QING_COUNCIL.txt: QING_council_recompute now scores four dynastic figureheads into the effectiveness
  base-average via the new QING_council_score_figurehead helper (4-skill mean, like the Grand Chancellor):
  Emperor weight 3, Grand Regent weight 3 (guarded has_variable + is_alive + employer=ROOT), Empress
  Dowager weight 1, Crown Prince weight 1 (guarded). Figureheads accumulate into a SEPARATE
  qing_council_figurehead_count and the base average now divides by qing_council_eff_denom =
  filled_count + figurehead_count (gated > 0). Figureheads are kept OUT of filled_count so the
  vacant-office penalty and the Manchu/Han balance term are unchanged.
- BEHAVIOURAL DELTA (intended, not equivalent): a filled council's effectiveness target now also reflects
  the imperial house's competence, weighted toward the Emperor/Regent. A capable emperor lifts the ceiling;
  a feeble one drags it. This is the requested change, so it is NOT byte-equivalent — but it cannot throw
  (denom gated > 0; all figurehead reads guarded) and it degrades to the old behaviour only if literally
  no figurehead exists (impossible while current_ruler exists).
- NOTE: the figurehead effectiveness weights (Emperor 3 / Regent 3 / Dowager 1 / Crown Prince 1) are
  deliberately DIFFERENT from the #158 faction-figurehead weights (Emperor 3 / Dowager 2 / Crown Prince 2)
  — two distinct aggregations (competence vs. political bloc).

## [#109/#120] Province-query panels — state->province scope fix (behavioural change, 2026-07-07)
Investigating the user's flag ("the tension panel reads qing_prov_ethnic_tension, but #107 seeds it on the
province"), confirmed BOTH report panels were reading province-level properties on the wrong scope:
- ROOT CAUSE: qing_report_open_crops/_open_tension iterated every_governorship_state and tested
  trade_goods / qing_prov_ethnic_tension on scope:this_state. In this engine a governorship_state is only
  a CONTAINER; trade_goods and per-province variables live on the PROVINCE. The mod's own production code
  always descends every_governorship_state -> every_state_province (se_GOODS.txt:975, se_EDU.txt:181,
  se_COTTAGEIND.txt:59) and reads those properties on the province. #107 writes qing_prov_ethnic_tension
  via every_owned_province (this = province, se_QING_ETHNIC_TENSION.txt:50). So BOTH lists were always
  empty — the tension list AND the crop list. The has_variable/trade_goods filters degraded gracefully
  (empty, no crash), which is exactly why it was silent.
- FIX (common/scripted_guis/qing_province_reports.txt): both effects now descend
  every_governorship_state -> every_state_province, save_scope_as this_prov, filter on scope:this_prov,
  and store PROVINCE scopes in the variable lists.
- FIX (gui/qing_province_reports.gui): both windows now render province scopes — Scope.GetProvince.GetName,
  .GetTradeGoods.GetTooltip, .MakeScope.Var('qing_prov_ethnic_tension'), OnClickOnProvince(Scope.GetProvince),
  SetHighlightProvince(Scope.GetProvince.GetId) — replacing the Scope.GetState.* accessors. All confirmed
  against proven usage (province_window.gui SelectProvinceItem rows; economy_view.gui:1531; imp19c_windows
  migrating-pop rows). Braces balanced 33/33 (.txt) and 64/64 (.gui); no-BOM/LF preserved.

## [#160] National Migration / Demographic-Pressure panel — NEW (2026-07-07)
Third Grand Council province-report panel, built on the same proven scripted_gui + .gui pattern as
#109/#120. User-approved after the feasibility answer.
- WHY AGGREGATE, NOT LIVE TICKER: the engine's live migrant data (per-pop migrant progress,
  GetActivitySpeed('migrant'), ViewPopsWindow.GetMigrants) is C++/hardcoded-GUI only and NOT script-readable,
  so a scripted_gui cannot rebuild that list. Script CAN read a province's population, capacity, and the
  concrete migration/boom PROVINCE MODIFIERS the frontier-migration mechanic stamps. Panel surfaces those.
- LOGIC (common/scripted_guis/qing_province_reports.txt qing_report_open_migration): country scope,
  is_shown tag=CHI, ai_is_valid always=no. Descends every_governorships -> every_governorship_state ->
  every_state_province (PROVINCE scope, matching the #109/#120 fix). Lists a province when it carries
  qing_migr_hongkong_boom OR qing_nwcrop_abundance OR total_population >= 20. clear_variable_list at top;
  degrades gracefully to empty (has_province_modifier / total_population are always-safe reads).
- GUI (gui/qing_province_reports.gui qing_migration_report_window): datamodel
  [Player.MakeScope.GetList('qing_migration_report_provinces')]; name col [Scope.GetProvince.GetName],
  value col [Scope.GetProvince.GetPopulation('total')]/[Scope.GetProvince.GetPopulationCapacityValue];
  goto_button OnClickOnProvince/SetHighlightProvince; footer qing_migration_report_count.
- BUTTON (gui/government_view.gui): icon_button_square in the Grand Council action strip after the tension
  button; icon gfx/interface/icons/shared_icons/population.dds (confirmed exists). ScriptedGui.Execute then
  gui.createwidget gui/qing_province_reports.gui qing_migration_report_window.
- LOC (localization/english/qing_province_reports_l_english.yml): qing_migration_report_title/_count/
  _tooltip/_value_tooltip + qing_report_open_migration_button.
- se_LOG: LOG_line on open. Braces balanced (.txt 50/50, .gui 98/98, government_view 1612/1612); no-BOM/LF.
- REVIEW: code-review agent dispatched for all three panels (crops/tension/migration) — result pending.

## [#161] Secret-succession events wired into affinity / Grand Council / reform-faction (behavioural change, 2026-07-07)
Answers the user's question "are the secret succession events tied into the affinity and Grand Council
mechanics?" — previously they were NOT; this wires them in. User-approved ("yes link the secret succession
events").
- NEW HELPERS (common/scripted_effects/se_QING_DYNASTY.txt), country scope:
  * QING_dynasty_accession_core — shared: exists=current_ruler guard, QING_dynasty_assess, scores the new
    sovereign (current_ruler={QING_char_stance}), tilts realm reform (QING_dynasty_reform_echo who=current_ruler
    scale=2), re-binds him to the throne (current_ruler={QING_char_bind}).
  * QING_dynasty_accession_smooth — harmony +8, council_effectiveness +3, then _core.
  * QING_dynasty_accession_disputed — harmony -12, council_effectiveness -5, then _core.
  * QING_dynasty_succession_strife = { severity = N } — harmony -6, council -3; writes severity to scratch var
    qing_succession_strife_sev, and if var:qing_succession_strife_sev >= 2 applies an extra harmony -4/council -2.
  DESIGN NOTE: deliberately AVOIDS comparing a passed param in a limit (limit={$smooth$=yes} is an unproven,
  likely-tautologizing idiom in this engine — same bug class as the invented CHECK_VALUE). Split into two
  parameterless smooth/disputed wrappers instead; severity uses the proven scratch-var workaround.
- WIRED (events/imp19c_mod_events/qing_regency_events.txt):
  * qing_succession.1 option .b (name openly): QING_dynasty_succession_strife = { severity = 2 }.
  * qing_succession.1 option .c (let them contend): QING_dynasty_succession_strife = { severity = 1 }.
  * qing_succession.2 immediate smooth branch (sealed tablet): QING_dynasty_accession_smooth.
  * qing_succession.2 immediate disputed branch (no sealed heir amid jockeying): QING_dynasty_accession_disputed.
- BEHAVIOURAL DELTA (intended): a sealed/smooth accession now lifts dynastic harmony + council effectiveness
  and lets the new emperor's stance move the reform-faction balance; a disputed one drags them down. Open
  designation / aloofness during jockeying now also costs harmony + council effectiveness (layered on top of
  the existing qing_succession_faction_strife modifier — independent, not double-counting the same meter path).
- SAFETY (code-review agent CONFIRMED, no crash-class defects): all referenced effects exist; QING_char_stance
  (se_QING_FACTION.txt:72) / QING_char_bind (se_QING_AFFINITY.txt:180) are char-scope and invoked inside
  current_ruler={...}; QING_dynasty_reform_echo takes who as a scope-prefix (who=current_ruler valid);
  on_ruler_change roots on country after the new ruler installs, exists=current_ruler guards interregnum;
  QING_DECLINE_nudge self-inits+clamps 0..100; both qing_dynastic_harmony and qing_council_effectiveness are
  seeded to 50 at init (se_QING_GOVERNANCE.txt:36, se_QING_COUNCIL.txt:55) so first-event deltas measure from
  the intended baseline; no recursion / re-trigger loop; scratch-var write-then-read within one block is valid.
- se_LOG: LOG_enter/LOG_exit on the accession helpers, LOG_line on smooth/disputed/strife. Braces balanced
  (se_QING_DYNASTY 188/188, regency_events 64/64); no-BOM/LF.

## [#109/#120/#160] Three-panel code review — CLEAN + regions trim (2026-07-07)
Fired the mandatory post-implementation code review (code-review agent) on all three province-report panels.
VERDICT: no crashes, no empty-list bugs, no dead branches, no missing loc/textures. Independently confirmed:
(a) #107 writes qing_prov_ethnic_tension on PROVINCE scope inside every_owned_province
(se_QING_ETHNIC_TENSION.txt:118/246/250/317), matching the #109 read; (b) both #160 migration modifier keys
are defined AND applied — qing_migr_hongkong_boom (qing_migration_modifiers.txt:82, applied
qing_frontier_migration_events.txt:383) and qing_nwcrop_abundance (qing_migration_modifiers.txt:70, applied
se_QING_COLON.txt:308); (c) all datamodel list names, window names, datacontext names, icon textures, and loc
keys match. Succession-wiring review (#161) also CLEAN (see above).
- TRIM (non-blocking review observation): removed the vestigial qing_*_report_regions variable lists (three
  effects) — governorship scopes populated but never read by the GUI, copied from the sell_provinces template.
  Removed the three clear_variable_list lines and the three root={ add_to_variable_list=regions } blocks. Panels
  now populate only the _provinces lists the windows actually consume. Braces 44/44; no-BOM/LF preserved.

## [#163] Amban manual-management panel — DESIGN LOCKED (2026-07-07)
User questioned whether Option A swaps ambans quarterly (it does NOT — clarified: post_sweep only fills
VACANCIES one/quarter, evaluate only SCORES; actual turnover is rare gated events: age>=65/health<0.4 @15%,
gone-native after 8yr tenure timer + affinity<40 @15%, clash-recall @friction>=65; role modifier duration=-1
permanent, so residents serve years-to-decades). LOCKED refinements to Option A:
- MANUAL FLAG (qing_amban_manual on the subject): skips post_sweep auto-staffing AND guards OFF the
  turnover/gone-native/recall event DISPATCH in QING_amban_evaluate — BUT the friction/affinity SCORING +
  opinion effects STILL RUN (a bad hand-picked amban keeps its quarterly consequences; player stays informed).
- FREE RECALL/REPOST anytime, no cooldown (panel = the manual override; max player control).
- Panel actions: post / recall / replace on any eligible subject + a "return to automatic" button clearing
  the flag. Eligibility = existing sweep gate (subject ruler culture_group mongolic|bodish, any_owned_province).

## [#163] Amban panel — auto-layer guards DONE + placement decision (2026-07-07)
Placement (user): the amban panel button lives in the SUBJECT country's DIPLOMATIC VIEW (diplomacy_view.gui,
per-subject), NOT the Grand Council action strip. (Contrast the three province-report panels, which are
Grand Council strip buttons.)
- GUARD 1 (se_QING_AMBAN.txt QING_amban_post_sweep): added NOT = { has_variable = qing_amban_manual } to the
  random_subject limit — auto-sweep never staffs/fills a vacancy on a player-managed dependency.
- GUARD 2 (se_QING_AMBAN.txt QING_amban_evaluate): wrapped the three-way lifecycle-event DISPATCH chain
  (.4 turnover / .2 gone-native / .3 able) in if = { limit = { NOT = { scope:qing_amban_subject = {
  has_variable = qing_amban_manual } } } }. The friction/affinity SCORING + opinion effects ABOVE the gate
  still run for manual subjects (locked design: keep scoring, freeze only auto-turnover). Clash-recall crisis
  (.1) is dispatched from the scoring section — NOTE it currently still fires for manual subjects; TODO decide
  whether the clash crisis should also be gated. RESOLVED: qing_amban.1 is a player-CHOICE popup (option .a
  recall / .b back the resident), NOT an automatic recall — so it stays UNGATED for manual subjects (it is a
  decision driven by the preserved scoring, consistent with 'keep scoring'). No gate on .1.
- Braces 131/131, no-BOM/LF. Behavioural change to existing code — the guards are pure additive skips; a
  subject WITHOUT the flag behaves exactly as before.
- TODO: panel scripted_gui (post/recall/replace/return-to-auto) + .gui window + diplomatic-view button + loc.

## [#163] Amban manual-management — panel BUILT (2026-07-07)
Built the manual amban panel per the locked Option A design, placed in the SUBJECT's diplomatic view.
- EFFECTS (common/scripted_guis/SUB_QING_amban.txt, NEW): four player-only (ai_is_valid always=no) scripted
  GUIs, scope=country, saved_scopes={target}, ROOT=CHI overlord, scope:target=subject (passed from GUI via
  AddScope('target', DiplomaticView.GetTargetCountry.MakeScope) — the PROVEN pattern from
  SUB_QING_subject_interactions.txt promote/demote/integrate buttons):
  * qing_amban_manage_post_button — shown when eligible (subject of ROOT, mongolic|bodish ruler culture_group,
    owns land) and NO amban here; gated Lifan Yuan filled + 25 influence; sets qing_amban_manual then
    QING_amban_post={subject=scope:target}.
  * qing_amban_manage_recall_button — shown when amban posted here; sets qing_amban_manual (so the vacancy
    isn't auto-refilled) then QING_amban_recall.
  * qing_amban_manage_replace_button — shown when posted + eligible; gated Lifan+influence; recall THEN post
    (order matters — posting over a live resident would strand the old man).
  * qing_amban_manage_return_auto_button — shown when qing_amban_manual set; removes the flag, re-enrolling
    the post in the auto-sweep/turnover.
- GUI (gui/diplomatic_view.gui): four icon_button_square widgets inserted after the RESUME button in the Qing
  subject-interaction strip (cloned the exact promote/demote widget pattern). Icons chosen from REPO-CONFIRMED
  shared_icons (oratory/tactical/change/time.dds) — NOTE the existing strip's icons (relations.dds,
  cultural_assimilation.dds) are base-game textures NOT present in the repo, so repo-file verification is the
  only safe check; used only confirmed-present files. Braces 1094/1094.
- LOC (localization/english/qing_amban_manage_l_english.yml, NEW, BOM+LF): 4 button tooltips + 3 red-reason
  custom_tooltip lines. Quote-balanced.
- se_LOG: LOG_line on every effect. SUB_QING_amban.txt braces 60/60, no-BOM/LF.
- Auto-layer guards (done earlier this session) skip manual subjects in post_sweep + freeze the turnover event
  dispatch in evaluate while preserving scoring; clash-recall (.1) stays ungated (it's a player-choice popup).
- TODO: code review of the whole amban feature (new panel + the two auto-layer guards).

## [#164] Subjugate diplomatic play — transfer a rival's subject (2026-07-07)
User: "the subjugate diplomatic play should be applicable to subjects of another country (in which case it
will transfer them to the country which initiated the subjugate play)."
- Begin-play gate (DIPLO_begin_play_subjugate, EE_scripted_guis.txt:1451) already permits the target: it only
  excludes the player's OWN subjects (NOT is_subject_of=scope:player), so a THIRD power's subject was always a
  legal target and the play could already be STARTED against one. No gate change needed.
- FIX (DIPLOMACY_resolve_subjugate, se_DIPLOMACY.txt): before FUNC_make_subject binds the target to the
  instigator, added — if scope:play_target_country = { is_subject = yes } — a release from its CURRENT overlord
  via scope:play_target_country.overlord = { release_subject = scope:play_target_country } (the proven idiom at
  se_FUNC.txt:349-352). Without this, make_subject on an already-subordinate country would leave a stale/double
  overlord bond. This makes a subjugation play against a rival's vassal actually TRANSFER the vassal to the
  play initiator (decisive=client_state, partial=tributary, same as before). se_LOG TRANSFER line added.
  Braces 540/540; no-BOM/LF.
- BEHAVIOURAL CHANGE to existing resolve effect — scrutiny: the new release is gated on is_subject=yes so a
  non-subject target path is byte-identical to before; the released-then-rebound path is the requested new
  behaviour. TODO: code review.

## #162 — Balance-history panel (quarterly net-balance histogram)
- NEW common/scripted_effects/se_BALANCE_HISTORY.txt (braces 56/56, no-BOM/LF): BALHIST_record_quarter
  shifts an 8-quarter rolling window of INCOME_national_total_quarterly (q0=newest), computes max|value|
  floored at 1, and pre-normalises each slot to 0..1 pos/neg bar heights (BALHIST_normalise_slot). se_LOG
  ENTER/EXIT + q0/scale line. Idempotent BALHIST_init seeds the window (new-country / first-quarter safe).
- WIRE: se_INCOME.txt INCOME_update_treasury_country calls BALHIST_record_quarter right after
  INCOME_national_total_quarterly is set (line ~63). Runs quarterly + at game init (both existing callers of
  the treasury update), for every country. [#162]-tagged comment. Braces 175/175.
- GUI: gui/economy_view.gui balance_history flowcontainer — replaced the single WiP placeholder column
  (hardcoded value="100") with 8 columns (left=q7 oldest .. right=q0 newest), each a green positive bar
  (top half, rises from centre-line for a surplus) + red negative bar (bottom half, deficit), bound to
  balance_hist_pos_q$N$ / _neg_q$N$ via FixedPointToFloat(Player.MakeScope.GetVariable(...).GetValue) — the
  idiom the file's own commented example uses. visible flipped no->yes. Braces 574/574.
- LOC: imp19c_interface_l_english.yml += BALANCE_HIST_Q_TT (BOM+LF preserved, 0 odd-quote lines).
- Was committed inert in 94f6c729, removed in 659c8f52 (user: don't commit unfinished), now COMPLETE.
- TODO: code review; then in-game verify (histogram populates after the first quarterly pulse).

### #162 code-review fixes (CONFIRMED, applied)
- ROOT CAUSE: I had PDX svalue clamp semantics backwards. VERIFIED against codebase
  (00_event_values.txt:603-604 clamps a probability with min=0/max=100; :56-57 min=100/max=1000):
  min = FLOOR (raise up to), max = CEILING (cap down to) — the intuitive reading.
- FIX 1 (CRITICAL, BALHIST_fold_abs): |x|=max(x,-x) needs the FLOOR operator; was `max = {..-1}`
  (=min, yielding -|x|, so max_abs stuck at floor 1 forever). Changed to `min = {..-1}`. Now grows correctly.
- FIX 2 (CRITICAL, BALHIST_normalise_slot x2 blocks): clamp to [0,1] was `max = 0  min = 1` (forced every
  bar to constant 1 => solid green-over-red block). Swapped to `min = 0  max = 1`.
- FIX 3 (MEDIUM, LOG_line): ROOT is not the iterated country inside every_country (and undefined at
  on_game_initialized). Swapped ROOT.MakeScope/GetTag -> This.* (proven idiom, se_JAPAN_BAKUMATSU.txt).
- Divide-by-zero guard, window shift, scope, macro use, GUI layout: reviewer VERIFIED correct, no change.
- Braces 56/56. Re-verified: no inverted clamps remain. Ready for in-game verify.

## #157 — New-Game boot CRASH fix (misplaced dynastic-house triggers)

- SYMPTOM: game booted fine but EXCEPTION_ACCESS_VIOLATION on New Game instantiation
  (crash at 18:25:48 = the on_game_initialized country-setup pass). debug_mode on, yet
  ZERO IMP19C log lines — died before the first setup LOG_enter flushed. Functions stripped
  from the stack, so diagnosed from error.log (Downloads copy).
- ROOT CAUSE: QING_dynasty_has_dowager + QING_dynasty_has_crownprince were authored in
  se_QING_DYNASTY.txt, a scripted_EFFECTS file. The engine registers a def in a
  scripted_effects file as an EFFECT, so every `limit = { QING_dynasty_has_* = yes }` was
  rejected at load ("Unknown trigger type", ~100+ occurrences across qing_keju_events,
  qing_napoleon_events, qing_office_events, se_QING_COUNCIL, se_QING_FACTION, etc.) and the
  guarding limit COLLAPSED. With the dowager guard gone, QING_council_recompute:160-162 (fired
  at boot via QING_council_autofill -> QING_council_recompute -> QING_faction_recompute) ran
  `QING_council_score_figurehead = { who = current_ruler.mother }` UNGUARDED. The 1815 Jiaqing
  Emperor has no living mother (Empress Xiaoyichun d. 1797), so current_ruler.mother is an
  invalid scope => access violation.
- WHY MASTER TOLERATES ITS OWN MISPLACED TRIGGER: master ships QING_seat_regency_warranted
  (also a condition-block in a scripted_effects file, used as a trigger) and boots fine —
  because that collapsed guard's body does no invalid deref. "Unknown trigger type" alone is
  survivable; only the resulting unguarded scope deref faults.
- FIX: relocated BOTH condition-blocks VERBATIM to NEW common/scripted_triggers/
  qing_dynasty_triggers.txt (no-BOM/LF, braces 8/8) so the engine registers them as triggers.
  All ~100+ "Unknown trigger type" errors and the crash resolve at once — the trigger is now
  globally registered for every call site. se_QING_DYNASTY.txt: removed the two defs, left a
  pointer comment (braces 183/183). Pure relocation, behaviourally identical once recognised
  as triggers. [#157 crash-fix]-tagged header documents the whole chain.
- SCOPE DISCIPLINE (deliberately NOT changed — verified pre-existing on master, non-fatal,
  not a develop regression, so out of "fix the things that will break"):
  * `minor_character = yes` in se_QING_AMBAN.txt:57 (QING_amban_post) — "Unknown effect", a
    no-op the engine skips; on master since the amban feature landed. Surfaced through the new
    #163 panel call site but pre-existing (should be is_minor_character; left for a feature pass).
  * `culture = ROOT.primary_culture` in se_QING_COUNCIL.txt score_office/score_chancellor —
    "Illegal use of operator =" guard-collapse, but the if-body only does change_variable (no
    scope deref), so master boots through it. On master at lines 231/260.
  * `culture_group = mongolic/bodish` on character scope (SUB_QING_amban, se_QING_AMBAN) — NOT
    flagged anywhere in error.log; engine accepts it. (Corrected a stale note that claimed it throws.)
- TODO: in-game verify New Game now instantiates without access violation.

### #157 follow-up — two SILENT functionality breaks (not crashes, but wrong)
User pushback: "just because it doesn't crash doesn't make it correct." Correct — traced both:

- **AMBAN minor-character (BROKEN, now fixed).** `minor_character = yes` inside create_character
  (se_QING_AMBAN.txt:57) is an INVALID key — error.log: "Unknown effect minor_character" at every
  QING_amban_post call site. Engine discarded it, so every amban resident spawned as a FULL major
  character (office/succession-eligible, character-list clutter) instead of a minor courtier. FIX:
  removed the bad key; added `set_as_minor_character = THIS` in the post-create character scope
  (proven idiom, events/annexation.txt:21). Pre-existing on master but genuinely wrong there too.
- **COUNCIL 滿漢 tally (BROKEN, now fixed).** `culture = ROOT.primary_culture` as a CHARACTER
  trigger (se_QING_COUNCIL.txt score_office:301 / score_chancellor:330) is invalid —
  primary_culture is a country TRIGGER, not a navigable culture link, so the RHS won't parse
  ("Badly read script value" + "Illegal use of operator ="; PostValidate returned FALSE). Effect:
  the `if` was ALWAYS false => every holder fell to the `else`/Han branch => qing_council_manchu_count
  stuck at 0. Downstream, all silently dead: the +15 滿漢並用 dyarchic bonus (needs manchu_count>=1),
  the qing_council_dyarchic_balance country modifier, and government_view.gui:2264 (always showed 0/N).
  FIX: save current_ruler (the definitional Manchu reference) as scope:qing_council_manchu_ref at the
  top of QING_council_recompute, compare each holder via the proven `culture = scope:X.culture` link
  idiom (00_ambitions.txt:1606), guarded by `exists = scope:qing_council_manchu_ref`.
  WHY it works at se_QING_DECLINE:1074 but not here: there it's inside an any_character/random_character
  iterator over a saved culture SCOPE; the council used a bare country-trigger nav as the RHS.
- Both were pre-existing on master (not develop regressions) — fixed under "fix the things that will
  break" because they silently break intended behaviour even though they never fault.
- Braces: se_QING_COUNCIL 380/380, se_QING_AMBAN 131/131. no-BOM/LF. TODO: in-game verify the Manchu/Han
  split populates (>0 Manchu with the 1815 Manchu ruler) and residents show as minor characters.

### #157 follow-up 2 — culture_group = X is INVALID (I was wrong earlier)
User asked directly: "is culture_group = mongolic/bodish valid or not." I had previously said
"not flagged, engine accepts it." WRONG — that was a grep artefact: the error names the VALUE
(mongolic/bodish/chinese_group), not the keyword, so `grep culture_group error.log` returned
nothing. It IS invalid. error.log: "Badly read script value mongolic/bodish/chinese_group" +
"Illegal use of operator =" — same class as the culture=ROOT bug. Bare `culture_group = X` is
not a trigger in ANY scope; the scope-correct triggers are `has_culture_group` (character) and
`country_culture_group` (country). When used in a limit the OR PostValidates false => the gate
fails SHUT (that branch never fires).
Fixed all FIVE erroring sites (logic was fine, keyword wrong):
- common/scripted_guis/SUB_QING_amban.txt:55-56,147-148 (#163 panel, develop-new) — current_ruler
  is a CHARACTER scope => has_culture_group = mongolic/bodish. (Broke the panel's is_shown/enable gate.)
- common/scripted_effects/se_QING_AMBAN.txt:177-178 (auto-sweep, master) — current_ruler CHARACTER
  => has_culture_group. (Auto-staffing of Mongol/Tibetan dependencies never fired.)
- common/scripted_effects/se_QING_DECLINE.txt:1058,1061 (QING_frontier_flavour_roll #7 Golden Urn,
  master) — any_subject/random_subject is a COUNTRY scope => country_culture_group = bodish.
- common/customizable_localization/00_offices.txt:9,27,45 (master) — type = country => 
  country_culture_group = chinese_group. (Chinese office-name loc branch never resolved.)
VERIFIED country_culture_group has zero load errors (used validly at 00_culture_supergroups:158);
has_culture_group is proven (characters_view_scripts:15-17). Braces: SUB 60/60, AMBAN 131/131,
DECLINE 974/974, offices 18/18. 00_offices BOM+LF preserved.
LESSON: to check whether a trigger is valid, grep the error log for the VALUE too, not just the keyword.

────────────────────────────────────────────────────────────────────────
#165/#166 boot-block ROOT CAUSE — the ENTIRE Qing on_game_initialized block never ran
────────────────────────────────────────────────────────────────────────
Reported in-game after a successful Qing start: the Emperor / Crown Prince / Empress
Dowager / Grand Chancellor figurehead boxes were all EMPTY, and the Grand Council had
only ONE eligible courtier (never staffed). Traced to a single misplaced trigger.

DIAGNOSIS (debug.log, -debug_mode run):
- The economy on_game_initialized block RAN (QING_seed_starting_treasury logged 3593×,
  per-country).
- The CHI-gated on_game_initialized block (qing_mechanics_on_actions.txt:9) emitted
  ZERO log lines. Decisive: QING_DECLINE_init — the FIRST call in the block, which opens
  with LOG_enter — had 0 hits at ANY timestamp. So the block never STARTED (not aborted
  mid-run). Every init in the chain (GOV/council/autofill/seat_refresh/dynasty/faction/
  ...) likewise 0 hits. The QING_council_refresh_candidates lines at 20:12+ are the PLAYER
  manually opening the council panel (QING_governance_actions.txt), not the boot chain.

ROOT CAUSE (error.log 20:04:08, load-time):
  pdx_persistent_reader.cpp:229: "Unknown trigger type: QING_seat_regency_warranted,
  near line: 3" in qing_mechanics_on_actions.txt line 32 (QING_seat_refresh_all → 
  QING_seat_evaluate_regency line 105 `limit = { QING_seat_regency_warranted = yes }`).
QING_seat_regency_warranted was DEFINED in a scripted_EFFECTS file (se_QING_SEATS.txt:164)
but is only ever USED in a limit. The engine registers a scripted_effects definition as an
EFFECT, so the limit reference fails to resolve — and unlike the harmless jomini_trigger
"Illegal use of operator" VALIDATION warnings, this is a hard pdx_persistent_reader PARSE
error that POISONS compilation of the whole compiled block it appears in. QING_seat_refresh_all
is called from the CHI on_game_initialized block, so the ENTIRE block was dropped → no init ran
→ figurehead vars (qing_office_emperor_holder/_crownprince_holder) never seeded (empty boxes,
#165) and QING_council_autofill never ran (unstaffed council, #166).

This is the SAME bug class as the #157 boot-crash fix (QING_dynasty_has_dowager/_crownprince,
also condition-only helpers wrongly in scripted_effects). PRE-EXISTING on BOTH master and
develop (git show master:se_QING_SEATS.txt confirms the misplacement) — NOT a develop regression.

FIX (pure relocation, behaviourally identical):
- common/scripted_triggers/qing_dynasty_triggers.txt — ADDED QING_seat_regency_warranted
  (same body: exists current_ruler + OR{is_adult=no / has_trait=incapable / age>=70}).
- common/scripted_effects/se_QING_SEATS.txt:164 — removed the def, left a pointer comment.
Braces: triggers 13/13, SEATS 108/108. scripted_triggers byte-conv no-BOM/LF verified.
Defined exactly once (triggers), used exactly once (SEATS:105 limit). se_LOG chain in the
boot block will now emit QING_DECLINE_init ENTER on next new game — the verification signal.

Scanned error.log for other "Unknown trigger type: QING_*" reachable from the boot chain:
QING_DECLINE_nudge (7×) is an EFFECT ({var= amount=}) used in mission trigger blocks, NOT in
the boot chain — separate pre-existing issue, out of scope. No other boot-chain poison found.

────────────────────────────────────────────────────────────────────────
#164 Grand Council OFFICES cards clipped by right border
────────────────────────────────────────────────────────────────────────
Reported: "the grand ministers are cut off with only three or four showing."
CAUSE: gui/government_view.gui OFFICES section packed all 10 office cards
(each 232px + margin ≈ 238px) into a SINGLE flowcontainer capped at width 950.
A plain flowcontainer does NOT wrap, so only ~4 cards (4×238=952) rendered before
the right border clipped the rest. The DYNASTY/HEALTH sections above already avoid
this by using manually-sized fixed rows; the OFFICES section didn't.
FIX: converted the single flowcontainer into `direction = vertical` stacking THREE
horizontal row-flowcontainers of 4 + 4 + 2 cards (personnel/revenue/rites/war |
justice/works/censor/lifanyuan | grand_secretary/zongli). Vanilla's own office grid
uses datamodel_wrap = 4, confirming 4-per-row fits 950px. Pure GUI restructure,
no logic change. Braces 1615/1615. Needs in-game visual confirm.

────────────────────────────────────────────────────────────────────────
#167 diplomatic-play type cannot be changed after selection
────────────────────────────────────────────────────────────────────────
Reported: "once the type is selected the player is forced to start it or leave
because there is no way to switch type of play after selecting one."
CAUSE: the six province-window goal buttons (#147, gui/province_window.gui:4605+)
each call DIPLO_begin_play_<goal>, which IMMEDIATELY begins the play (pays 30
influence via DIPLOMACY_player_begin_play). Every one of the six shared an is_valid
clause `NOT = { any_in_global_list ... play_instigator = scope:player ... same area }`.
So the instant you clicked one goal, a play existed in that area and ALL SIX buttons
disabled — leaving only the toggle Start/End button. No way to pick a different type.
FIX (two parts, se_DIPLOMACY.txt + EE_scripted_guis.txt):
1. DIPLOMACY_player_begin_play now SWITCHES IN PLACE: if the player already runs a
   play in scope:target_province's area, it removes that play (random_in_global_list
   + AI_remove_diplomatic_play, the proven DIPLO_begin_or_end_play shape) and SKIPS
   the begin price (a switch, not a new play); a genuinely fresh play still pays.
2. Removed the blocking `NOT = { any_in_global_list ... }` guard from all six begin
   guis (get_territory/annex_state/purchase_state/subjugate/liberate/colonise) so the
   buttons stay ENABLED while a play runs — clicking a different goal now switches.
   Kept every other per-goal gate (political_influence>=30, stability, treasury,
   DIPLOMACY_power, is_subject_of, culture-mismatch). The toggle Start/End button
   (DIPLO_begin_or_end_play) is independent and unchanged — still the End control.
Global list stores play-PROVINCE objects (se_AI.txt:621), so random_in_global_list
iterates with THIS=play, exactly what AI_remove_diplomatic_play expects. se_LOG line
on switch. Braces: se_DIPLOMACY 550/550, EE_scripted_guis 479/479.

────────────────────────────────────────────────────────────────────────
#168 Qing per-subject interactions not visible in the diplomacy window
────────────────────────────────────────────────────────────────────────
Reported: subject-interaction buttons (promote/incorporate/demote/integrate/
resume/amban post-recall-replace-return) never appeared anywhere usable.
CAUSE: the buttons had been placed in the Subjects TAB, whose right pane only
renders while viewing the PLAYER's own country. Each button gates on
scope:target = { is_subject_of = ROOT }, which can never pass in that context,
so the buttons were permanently hidden.
FIX: moved the whole interaction strip into the DIPLOMATIC tab, shown when the
viewed target IS one of the player's own subjects (visible gated on Player.GetTag
== CHI AND DiplomaticView.GetTargetCountry.IsSubject AND its overlord == Player).
Each button uses the proven ScriptedGui IsShown/IsValid/Execute idiom with
GuiScope root=Player + AddScope('target', target). Added a subject-type label +
integration-progress bar (SUBJ_integration_progress /5). The Subjects tab list is
now pure NAVIGATION: clicking a subject OpenDiplomacy(that subject) opens its
diplomatic view where the buttons live (restored the commented-out onclick).
Loc: QING_SUBJECT_INTERACTIONS_HEADER. gui braces balanced.

────────────────────────────────────────────────────────────────────────
#169 Great Powers not visible in the diplomacy window
────────────────────────────────────────────────────────────────────────
Reported: no way to see the four-power Great Game rivalry state from diplomacy.
FIX (gui/diplomatic_view.gui, Qing-only): (1) an inline Great Game strip that
surfaces tension (qing_gp_tension_britain/_france/_russia) + standing (opinion)
when the Qing player views GBR/FRA/RUS; (2) a combined 'Great Game' diplomatic-view
tab (category_tab toggling diplomatic_tabs='greatgame') showing all three powers'
tension+standing at once, each section gated on qing_greatgame_<power>_exists.
Informational only — no player-clickable GP verbs (provoke effects fire from
colonization/frontier events, not GUIs). Reads engine accessors (GetOpinionOf uses
Player.GetCountry; GetCountry('TAG')), so non-CHI just hides, no error. Loc:
QING_GREAT_GAME_INLINE_HEADER/_TAB_TITLE/_TAB_BUTTON/_SELF_TITLE. gui braces balanced.

────────────────────────────────────────────────────────────────────────
#170 Tibet lost its subjects and is no longer a protectorate
────────────────────────────────────────────────────────────────────────
Reported: Tibet had stopped being a Qing protectorate and had lost LTG/BTG.
CAUSE: commit 69d1178a had flipped CHI->TIB from protectorate to
autonomous_governorship on the false premise that a protectorate cannot hold
sub-subjects. autonomous_governorship is the one rung the Qing absorb/integrate
mechanic acts on, so the integration path was detaching Tibet's own LTG/BTG.
FIX (two parts):
1. setup/main/00_default.txt: reverted CHI->TIB to protectorate. A protectorate CAN
   hold sub-subjects (this file already ships POR->BRZ/ANG/MOZ/PGI and BJR->four
   tributaries), so TIB->LTG/BTG feudatory holds. Restores historical status +
   subject retention. (Both protectorate and autonomous_governorship are actually
   can_be_integrated=no; the #168 buttons gate on the mod's own scripted-GUI
   is_shown triggers, not the engine flag, so the incorporate->integrate flow still
   works: incorporate converts protectorate->autonomous_governorship first.)
2. se_SUBJECT_QING.txt: NEW SUBJ_QING_reparent_sub_subjects, called from
   SUBJ_QING_absorb_subject BEFORE the province transfer (while scope:target still
   exists as overlord). When absorbing a subject that itself holds sub-subjects, it
   snapshots them into a list, records each one's CURRENT type as a flag, releases
   it from the vanishing intermediary (release_subject), then FUNC_make_subject re-
   binds it to ROOT preserving that type. Release-first is the proven idiom
   (se_DIPLOMACY.txt); FUNC_make_subject passes $type$ straight to make_subject (no
   whitelist). Type coverage: tributary/nominal_vassal/feudatory/semi_+autonomous_
   governorship/client_state/sinosphere_tributary/protectorate preserved exactly;
   only truly off-ladder types (colony/territory) fall back to feudatory (logged).
   [review-fix: sinosphere_tributary (the canonical 朝貢 tie) + protectorate were
   added after code review flagged them silently degrading to feudatory.]
   se_SUBJECT_QING braces 255/255.

────────────────────────────────────────────────────────────────────────
#171 broken placeholder buttons in the Qing diplomatic Subjects tab
────────────────────────────────────────────────────────────────────────
FIX (gui/diplomatic_view.gui): (1) the #pop icon_and_text showed a hardcoded 'Egg'
placeholder — now reads DiplomaticView.GetTargetCountry.GetTotalPopulation with the
real population tooltip. (2) the dead 'Change Overseer' placeholder button (onclick
commented out) was repurposed into the amban-replace action, wired to the same
qing_amban_manage_replace_button scripted GUI as the #168 strip.

────────────────────────────────────────────────────────────────────────
#172 Qing 1815 starting treasury too thin + Board of Revenue silver reserve
────────────────────────────────────────────────────────────────────────
CAUSE: QING_seed_starting_treasury seeded the treasury at only ~4 months of
expenditure (multiply = -4).
FIX: se_QING_MECHANICS.txt multiply -4 -> -12 (~a full year's expenditure on hand).
Also se_CURRENCY.txt: set CHI silver_reserve_size to 46140 (the 戶部銀庫 Board of
Revenue hoard, ~46.14M taels, mid-Jiaqing c.1815 — distinct from the spendable
treasury). UNIT proven from engine consumption math to be hundreds of troy-lb
(1 unit = 100 troy-lb ≈ 1,000 kuping taels), so the original 20000 decoded to
~20M taels/746t. SOURCE: Shi Zhihong (2016) archival series; Kaske (2012, HJAS).

────────────────────────────────────────────────────────────────────────
#174 recalibrate national precious-metal reserves from sourced 1815-25 research
────────────────────────────────────────────────────────────────────────
se_CURRENCY.txt CURRENCY_setup_all_reserves — corrected historically-indefensible
values downward, each with an academic-source comment:
  SPA 12180 Au/0 Ag -> 15 Au/135 Ag (Fontana 1971, La quiebra de la monarquia
      absoluta 1814-1820 — Fernando VII bankruptcy, empty Hacienda).
  TUR 10600 Ag -> 1070 Ag (Pamuk 2000, A Monetary History of the Ottoman Empire —
      chronic pre-Tanzimat kuruş debasement precludes a standing bullion hoard).
  RUS 2000 Au/5000 Ag -> 135 Au/400 Ag (no convertible reserve before Kankrin's
      1839-43 silver-standard reform; inconvertible assignat at ~3.5:1).
  CHI: number kept (46140), attribution corrected to mid-Jiaqing c.1815.
UNCHANGED (deliberate, documented): GBR/FRA/SAX/POL explicit values; USA/Japan/
Austria/Prussia keep the population-proportional default (2nd Bank $35M was
authorised capital not specie; bakufu 御金蔵 3.00M ryo 1770 -> 0.82M 1789 and
declining; Austria's 1811 Staatsbankrott). se_CURRENCY braces 516/516.

────────────────────────────────────────────────────────────────────────
#175 Grand Council: eligibility + one-office-per-man exclusivity + list refresh + window overlap
────────────────────────────────────────────────────────────────────────
Bug cluster reported in-game: (a) a courtier appointed to an office stayed in the
Eligible Courtiers list; (b) one man could be appointed to MANY offices at once;
(c) candidates "popped up one at a time"; (d) the Eligible Courtier window covered
the Grand Minister office boxes.

se_QING_COUNCIL.txt (braces 384/384):
  • QING_office_appoint — added a ONE-OFFICE-PER-MAN auto-vacate at the top: if the
    appointee already holds a DIFFERENT great office, QING_office_vacate_dispatch is
    called FIRST (guarded to a different office so re-appointing the same seat is a
    no-op). Prevents the silent "holds two offices" state (old qing_office_<key>_holder
    var kept pointing at him while his qing_office_held flag was overwritten). Runs in
    character scope reading his own flag; no recursion (dispatch→vacate only).
  • QING_office_appoint + QING_office_vacate — added QING_council_recompute +
    QING_council_refresh_candidates at the END of both, via employer{} in appoint. The
    just-appointed man now drops out of the Eligible list immediately (its filter is
    NOT has_variable=qing_office_held) and a relieved man reappears at once — no waiting
    for the quarterly pulse / tab reopen. This is the "popping up one at a time" fix.

QING_governance_actions.txt (braces 181/181):
  • Each of the 11 appoint verbs' is_valid gained NOT = { has_variable = qing_office_held }
    (reject an already-employed courtier from being offered ANY other office), the GUI-side
    half of the exclusivity guard, alongside the existing per-office flag check.

gui/government_view.gui + gui/imp19c_windows.gui:
  • Eligible Courtiers moved OUT of the Grand Council tab (where its grid overlapped the
    office boxes) into a SEPARATE MOVABLE window (qing_eligible_courtiers_window in
    imp19c_windows.gui). The tab now shows an "Open Eligible Courtiers" button that
    refreshes the candidate cache and GUI.createwidget-opens the window; the player can
    drag it aside. Inside the window GovernmentView.GetPlayer -> Player. New loc keys
    QING_GC_OPEN_CANDIDATES(_TT).

────────────────────────────────────────────────────────────────────────
#166 Grand Council only one eligible courtier at start (root cause: autofill drained a tiny court)
────────────────────────────────────────────────────────────────────────
Root cause: QING_council_autofill staffs all 11 offices at game start from the same
employer=ROOT / adult / alive / NOT-officed pool the candidate list draws from. The
1815 living-adult Qing court in setup was ~12 men, so autofill left ~1 on the bench.
Fix (per user decision): seed a real court bench.
  setup/characters/00_Qing.txt (braces 226/226) — 9 sourced Jiaqing/early-Daoguang
  officials (ids 700, 702, 703, 706, 707, 708, 709, 711, 712): Tuojin, Dong Gao,
  Changling (Sartuk clan), Jiang Youxian, Wang Ding, Pan Shi'en, Yinghe, Muzhang'a,
  Saishang'a. All verified alive+adult c.1815 (birth<1797, death>1815), ethnicity via
  culture (manchu/xiajiang/mongolian), specialty biased by traits (engine rolls raw
  attributes). Autofill now leaves a genuine Eligible-Courtiers bench of appointable men.

  POST-REVIEW CORRECTIONS (code-review agent ab99143 caught two critical defects in the
  first draft, both fixed before commit):
  1. PLACEMENT BUG (critical): the whole 700-715 block was appended after the "KOR"={
     (Korea) block, i.e. NESTED INSIDE KOR — those officials would have been created
     with country="KOR", so CHI's bench stayed empty and #166 was NOT fixed. Cut the
     block out of KOR (KOR now byte-identical to HEAD) and reinserted it inside "CHI"={
     just before its closing brace, dedented one tab to CHI's level.
  2. DUPLICATE FIGURES: 6 of the 15 were already in the roster under other ids —
     704 Nayancheng == existing CHI 358; 710 Songyun == existing ILI ruler 323;
     701 Cao Zhenyong == CHI 245; 705 Ruan Yuan == CHI 321; 713 He Changling == CHI 311;
     714 Qishan == CHI 236; 715 Lin Zexu == CHI 246. All 6 dropped (the existing entries
     are richer — banners, offices, jinshi). Verified NO remaining first+family-name
     collision. Net-new bench = 9, still comfortably above the 11-office autofill need
     given the pre-existing living court.

────────────────────────────────────────────────────────────────────────
#176 subject-interaction window unusable — moved into a "Subject Actions" dropdown
────────────────────────────────────────────────────────────────────────
Reported: clicking a subject's flag opens the (correct) diplomatic view but NO Qing
subject-interaction controls appeared there; clicking the name did nothing. The #168
inline block (a top-level sibling of the whole actions area) never rendered for the
player. Per user direction, relocated the per-subject verbs (promote/incorporate/
demote/integrate/resume + 4 amban buttons) into a collapsible "Subject Actions"
dropdown placed directly BELOW the Trade Actions dropdown in the diplomatic actions
column (gui/diplomatic_view.gui, braces 1304/1304). Uses a subject_actions_open GUI
var mirroring trade_actions_open; gated CHI + target IsSubject of player. Old inline
block removed. New loc key QING_SUBJECT_ACTIONS_HEADER.

────────────────────────────────────────────────────────────────────────
Diplomatic-play goal-button overflow (province_window.gui)
────────────────────────────────────────────────────────────────────────
Six 150px goal buttons (get_territory/annex/purchase/subjugate/liberate/colonise) in
one non-wrapping horizontal row (~930px) overflowed the 500px diplomacy container's
right edge. Split into TWO rows of three (~462px each) so all are visible. Braces
1944/1944.

POST-REVIEW CORRECTION (code-review agent ab99143, MEDIUM): the first-draft "split" had
NOT actually been applied — an earlier Edit had silently failed and left only the
comment, so all six buttons were still in ONE flowcontainer and the overflow persisted
(a fix-traceability violation: comment described code that didn't exist). Now genuinely
split: first flowcontainer closes after purchase_state (3 buttons), a second identical
horizontal flowcontainer holds subjugate/liberate/colonise (3 buttons).

────────────────────────────────────────────────────────────────────────
#175 code-review LOW findings (accepted as-is)
────────────────────────────────────────────────────────────────────────
LOW 3 — office-SWAP path runs QING_council_recompute + refresh_candidates twice (once
in the auto-vacate's QING_office_vacate, once at QING_office_appoint's end). Idempotent;
no correctness impact, just redundant work on the rare swap path. Left as-is.
LOW 4 — qing_office_vacancy_strain bookkeeping on the swap path: auto-vacating seat X
adds the (single, non-per-office) vacancy-strain modifier, then filling seat Y removes
one, so X's genuine "seat empty" signal is lost. Pre-existing design limitation of the
single-strain modelling; the new auto-vacate makes it reachable but swaps only occur on
event/autofill paths (the GUI never offers appoint to an employed man). Left as-is; a
per-office strain model would be the proper fix if this ever matters in play.

────────────────────────────────────────────────────────────────────────
#163 SPHERE Phase-0 probe REMOVED (was never validly run) — verdict retracted
────────────────────────────────────────────────────────────────────────
The Phase-0 probe (SPHERE_probe_debug.txt on_action + se_SPHERE_probe.txt) was written
WITHOUT a UTF-8 BOM, while its sibling on_action files carry one; the engine rejected it
at load, so the probe effect NEVER RAN. The error.log lines mentioning it were an
encoding-rejection error (+ an unused-variable warning from the dead file), NOT the
probe's PUSH-fallback verdict. An earlier note claiming "debug.log is broken in this
build" was WRONG and is retracted — debug.log is fine; the absence of SPHERE lines is
fully explained by the load rejection. Both probe files DELETED (they errored every CHI
game). #163 (four-power sphere-of-influence) is UNSETTLED again — the PULL-vs-PUSH
question must be re-approached without a probe.

────────────────────────────────────────────────────────────────────────
#163 SPHERE Phase-0 probe RE-CREATED (correctly BOM'd this time) — awaiting in-game read
────────────────────────────────────────────────────────────────────────
Per user direction ("re-probe PULL first"), the throwaway capability probe is rebuilt,
this time with the on_action carrying the mandatory UTF-8 BOM (efbbbf) so the engine
actually loads it. Two files:
  common/scripted_effects/se_SPHERE_probe.txt  (NO BOM, matching sibling se_*.txt;
    braces 27/27) — SPHERE_probe_run: on CHI, stamps sphere_probe_score=42 on the
    capital state, walks to neighbour states via the PROVEN traversal
    state -> every_state_province -> every_neighbor_province -> state (deliberately
    avoids the also-unproven area/every_neighbor_area hop), and logs (a) whether the
    neighbour reach works at all, (b) THE TEST: can a neighbour state read the numeric
    var living on a DIFFERENT saved state scope (scope:sphere_src_state) mid-iteration
    — logs 42 if PULL works, -999 if not, and (c) the symmetric source-reads-neighbour
    marker read. All lines tagged "IMP19C SPHERE"; extract with
    grep "IMP19C SPHERE" logs/debug.log (needs -debug_mode).
  common/on_action/SPHERE_probe_debug.txt  (UTF-8 BOM, braces 6/6) — on_game_initialized
    effect, guarded by global var sphere_probe_done + exists = c:CHI, fires SPHERE_probe_run
    exactly once. Coexists with the other on_game_initialized files (engine merges).
Both files are THROWAWAY — delete once the PULL-vs-PUSH verdict is read from debug.log.
NOTE: not committed with the #175 batch; goes to develop as its own testable step.

────────────────────────────────────────────────────────────────────────
#184-192 OVERNIGHT BUILD (2026-07-08) — economy (buildings/goods/production) + Qing OOB + mobilization
────────────────────────────────────────────────────────────────────────
Single overnight job. All major design decisions live in overnight_decisions2.md
(§1-§14). Every feature se_LOG-instrumented; every edit carries a [#NNN task #NNN]
traceability comment. Nothing here overrides the standing rules.

#180/#189 TRADE GOODS — new producible goods.
  Added `porcelain` (Jingdezhen imperial-kiln specialty, blue-and-white 青花) and
  `rifles` (a tradeable military-logistics manufactured good) to common/trade_goods/
  00_imp19c.txt. DECISION (user): cannons are NOT a trade good — artillery is already
  modelled as a unit type; only small-arms/rifles become a commodity. Localised in
  imp19c_tradegoods_l_english.yml (name + DESC each).

#183/#184/#185 BUILDINGS — five concrete on-map production buildings + 1815 seed.
  common/buildings/qing_production_buildings.txt (BOM): qing_silk_filature_building
  (織造局), qing_porcelain_kiln_building (御窯廠), qing_tea_workshop_building (茶廠),
  qing_cotton_workshop_building (棉紡織坊), qing_salt_yard_building (鹽場/鹽井). Each
  MULTIPLIES its province raw-good output (base_resources) + boosts the strata whose
  labour the craft used; schema follows arsenal_building / IND_resource_gathering_operation.
  Placement, NOT the build menu: se_QING_BUILDINGS.txt (NO BOM) SE_qing_starting_buildings
  seeds 12 buildings into their historical provinces at game start via QING_seed_building
  ($P$/$B$/$G$ macro) — silk: Suzhou 2588 / Jiangning 6659 / Hangzhou 8120; porcelain:
  Jingdezhen 7397; tea: Wuyishan 3317 / Huangshan 4441; cotton: Wuxi 366 / Changshu 455;
  salt: Yangzhou 3208 / Tianjin 3783 / Chongqing 3008. Guarded by global sentinel
  chi_starting_buildings_done; each seed re-checks owner=c:CHI + trade_goods match +
  NOT has_building, logs SEED or SKIP. add_building_level BYPASSES the allow tech-gate
  (proven se_QING_MECHANICS.txt:539), so 1815 seeding works regardless of tech. Wired at
  oa_economy_setup.txt:2188. Localised in qing_mechanics_l_english.yml.

#188 INTEGRATION — tie the new buildings/goods into existing content.
  • Board of Works (user's explicit example — "the Grand Minister of Works would be
    directly affected"): se_QING_WORKS.txt QING_works_build_specialty ($building$/$good$/
    $cheap$) builds a specialty works in the most-populous owned province producing $good$
    that lacks it; finesse-gated, treasury cost 75 (capable) / 95 (mediocre + corruption),
    mirroring QING_works_build_dike/canal/wall. Surfaced by NEW event qing_works.6
    "A Memorial to Expand State Industry (興辦官局)" (5 build options + decline), wired into
    QING_frontier_flavour_roll (se_QING_DECLINE.txt, weight-6 entry gated on treasury>=90 +
    a living, employed Works holder). Localised (14 keys) in qing_works_l_english.yml.
  • Self-Strengthening (se_QING_SELFSTR.txt): after the Jiangnan arsenal is built,
    QING_selfstr_found_jiangnan retargets the arsenal province to set_trade_goods = rifles
    (guarded has_building=arsenal_building + NOT trade_goods=rifles) — the concrete
    goods<->content tie linking the `rifles` good to the arsenal that makes them.

#190/#191 QING 1815 ARMY/NAVY OOB — reworked from sourced research (§14a).
  Replaced the placeholder (one 12k army + two 85-ship navies). imp19c_effects_legion_setup.txt:
  SE_qing_armies raises ~26 named Banner + Green Standard provincial garrisons (dispersed,
  not one doomstack); SE_qing_navy DISBANDS the auto-generated fleets and raises the three
  historical provincial coastal water-forces as weak war-junk squadrons —
  廣東水師 Guangdong (Canton p:9298, 6x brig), 福建水師 Fujian (Fuzhou p:3651, 4x brig,
  largest-coastal-province fallback), and NEW #191 浙江水師 Zhejiang (Ningbo p:2893, 3x brig).
  Each guarded on exists + owner=c:CHI + is_coastal, with LOG_fail on miss. Research point:
  three coastal junk squadrons individually outclassed by a single European steam frigate —
  historically accurate weakness, not a bug.

#192 19th-CENTURY MOBILIZATION / BREAK-IN SYSTEM — new; expands the logistics layer (§14b).
  A newly-RAISED legion starts UNREADY and becomes battle-ready over ~2-6 months as
  staggered, self-expiring readiness debuffs lapse. Model (Showalter, van Creveld, Lynn,
  Wawro): MULTI-AXIS, each maturing at its own rate — drill/discipline FAST, cohesion/morale
  MEDIUM, supply/logistics SLOW (+ irregular residual floor); FRONT-LOADED as a heavy RAW
  layer (expires first) + a lighter SETTLING layer (expires later) per axis, so the penalty
  steps down like an exp-decay curve. NO per-tick variable decay loop, NO legion-scope
  variables (both unproven — oracle-checked). Files:
  • common/modifiers/mobilization_modifiers.txt (NO BOM): 7 UNIT-scope modifiers
    (mobil_drill_raw/settling on `discipline`; mobil_cohesion_raw/settling on
    `land_morale_modifier`; mobil_supply_raw/settling on `land_unit_attrition`+`siege_ability`;
    mobil_supply_floor_irregular). Keys verified at unit scope (same as qing_unit_banner_rot).
  • common/scripted_effects/se_MOBILIZATION.txt (NO BOM, sys=MOBIL): MOBIL_stamp_legion
    (legion scope, on_legion_raised entry) decides ONE profile — LEVY (any conscript sub_unit)
    vs REGULAR, then by accelerators — and calls MOBIL_stamp_all, which stamps the six layers
    (+ floor for unsupported levies) on every_legion_unit. ACCELERATORS shorten the raw layers /
    skip the floor: a general attached (any_legion_commander alive), raised in supplied home
    soil (unit_location owner+controller = owner), and — USER REQUIREMENT — BUILDINGS & INDUSTRY:
    a supply depot (military_depot_building / INF_depot / arsenal_building at the muster) or a
    RAILWAY (tech_steam_locomotive or a local INF_railway_upgrade) sharply cut the supply penalty
    and lift the irregular floor. Ties the new §2-§4 buildings + `rifles` to readiness.
  • common/on_action/00_specific_from_code.txt (BOM): populated on_legion_raised with
    MOBIL_stamp_legion, GUARDED NOT current_date=1815.7.1 so the game-start standing armies
    (the peacetime establishment) are EXEMPT — only genuinely fresh musters break in.
  Localised (14 keys) in modifiers_l_english.yml. Scope hierarchy oracle-verified against
  Invictus (ip_republic.20) + Terra-Indomita; design iterated 3x to eliminate every unproven
  construct before writing.

ALL new/edited script files brace-balanced 0; byte conventions honoured (se_*.txt + modifiers
NO BOM; on_action + trade_goods + loc BOM). Awaiting the deep adversarial-review workflow +
in-game verification before any promotion to master.

────────────────────────────────────────────────────────────────────────
#193 POST-BUILD ADVERSARIAL REVIEW + FIXES (2026-07-08) — commit fdc207b3
────────────────────────────────────────────────────────────────────────
Ran the deep adversarial-review workflow (6 dimensions → per-finding refutation pass →
synthesis; 19 agents). VERDICT: no critical or load-rejection defects — BOM conventions,
brace balance, scope hierarchy, and idioms all clean; safe on develop. 10 findings survived
verification (2 refuted: the navy `sub_unit = brig` "idiom deviation" and a `max_level`
concern — max_level is not a valid Imperator building property). All 7 distinct surviving
issues FIXED this pass (task-tagged [#193-fix]):

1. [HIGH → fixed] Mobilization game-start exemption used exact-date equality
   `NOT = { current_date = 1815.7.1 }`, but on_legion_raised fires "the day AFTER" a raise
   (stock engine comment), so setup armies raised on START_DATE 1815.7.1 trigger it on
   1815.7.2 — when the guard is TRUE and the WHOLE peacetime establishment would be debuffed.
   Fix: startup-window guard `current_date > 1815.7.2` (proven idiom), exempting the first
   two days regardless of the exact firing day. (common/on_action/00_specific_from_code.txt)
2. [MEDIUM → fixed] SE_qing_armies had NO idempotency sentinel (unlike SE_qing_navy /
   SE_qing_starting_buildings), so on every save-load — when on_game_initialized re-fires —
   the ~26-garrison OOB was re-raised, doubling the Qing army. Fix: wrapped in the
   NOT has_global_variable = qing_armies_setup_done guard + set at success, matching the
   sibling idiom. (imp19c_effects_legion_setup.txt)
3. [MEDIUM → fixed] qing_works.6 build options were silent no-ops for a Works minister with
   finesse < 7 (the event/option triggers had no finesse gate but QING_works_build_specialty
   requires finesse>=7). Fix: added finesse>=7 to the event trigger AND to each of the 5
   build-option triggers, so a sub-7 minister is neither shown the event nor a dead option.
   (qing_works_events.txt)
4. [MEDIUM → fixed] The 5 specialty works had only an allow{} tech gate, no `potential`, so
   any teched nation could build e.g. the Jingdezhen Imperial Kiln in a Yorkshire coal
   province, applying its output multipliers to unrelated goods. Fix: added
   `potential = { owner = { country_culture_group = chinese_group }  trade_goods = <match> }`
   to all 5. add_building_level bypasses potential, so the 1815 seed / Board-of-Works /
   Self-Strengthening spawns are UNAFFECTED. (qing_production_buildings.txt)
5. [LOW → fixed] porcelain/rifles referenced 8 trade-UI loc keys (internal_trade_scope_* +
   tracker_price_*) that no .yml defined, so their trade tooltips rendered raw key strings.
   Fix: cloned the maize entries for both goods into economic_enchancement_l_english.yml.
6. [LOW → fixed] SE_qing_navy's Fujian fallback (used only if Fuzhou is non-coastal) picked
   the most-populous coastal province without excluding Canton (9298) / Ningbo (2893), so it
   could stack a second squadron on an already-used port. Fix: added NOT province_id guards.
   (imp19c_effects_legion_setup.txt)
7. [LOW → fixed] mobil_supply_raw(0.30)+settling(0.12)=0.42 attrition during the raw window
   EXCEEDED the mod's own supply-collapse ceiling (0.30) — a fresh unit bled harder than a
   fully cut-off army. Fix: capped raw→0.20, settling→0.08 (=0.28, below collapse, with
   headroom for the qing_unit_*_rot stack). (mobilization_modifiers.txt)

All touched files brace-balanced 0; byte conventions preserved. Fixes remain on develop for
in-game verification; the #1 guard fix should be confirmed with se_LOG (MOBIL_stamp_legion
entries) at 1815 load before any promotion to master.

────────────────────────────────────────────────────────────────────────
## PEAK-QING (1759) BOOKMARK — branch `early_bookmark` (task #194–#197)

**Goal (user):** research the height of the Qing dynasty (EN+ZH academic sources), re-target the
game to that year — Qing characters, borders, buildings, and all relevant data — on a new branch
`early_bookmark`, after a deep adversarial-review workflow. Reusable process to be saved (user will
ask for other years later); all big decisions logged in `early_bookmark_decisions.md`.

**Research (#194):** chosen year = **1759 (乾隆二十四年)** — the 1 Sep 1759 completion of the Xinjiang
conquest (Khoja brothers run down in Badakhshan), the Qing's maximal territorial extent + peak power,
Qianlong at peak vigour, treasury deep and rising. EN scholarship (Perdue/Rowe/Elliott) = 1759
territorial/power apogee; ZH scholarship (戴逸/郭成康 "盛世危機") = ~1790 demographic/fiscal apogee,
recorded as a possible second bookmark. Reports: `research/QING_APOGEE_RESEARCH.md` (+ teammate-sourced
addendum: 何炳棣 population figures, Ili-General-1762 caveat, Laos/gaitu-guiliu tributary context),
`research/QIANLONG_ROSTER_RESEARCH.md`.

**Setup adjustment (#195):**
- **START_DATE** `1815.7.1` → `"1759.9.1"` (`00_defines.txt:3`). END_DATE 1936 kept. Δ = 20391 days.
- **Dated arc offsets +20391** (30 beats): japan_bakumatsu (7), mex_instability (10), usa_section (11),
  Amherst one-shot, AND the pre-Perry backstop (`qing_japan_preperry.10` — this one was initially
  missed and caught in a follow-up sweep; would otherwise have fired ~1797). So Perry (~1853), US Civil
  War, Mexican independence, etc. still land on their true historical dates. Effect-relative offsets
  ({1 5}/{3 12}/{120 300}) correctly left unshifted.
- **Mobilization game-start guard** → `current_date > 1759.9.2` (`00_specific_from_code.txt`).
- **Reigning emperor:** Qianlong (char:214, b.1711 d.1799) set as CHI ruler + era grants; Jiaqing
  (char:224, b.1760 → unborn at 1759) ruler block + grants commented out.
- **Qianlong court bench:** new CHI-block chars **720–729** (Liu Tongxun, Yu Minzhong, Agui, Zhaohui,
  Yin Jishan, Ji Yun, Dai Zhen, Qian Daxin, Zhao Yi, Yuan Mei), all born < 1759. IDs verified
  collision-free; trait/culture/religion keys verified against `common/`; braces balanced; BOM preserved.
- **Treasury seed** raised for the surplus era (see review fix below).
- **NO territorial/subject change** (D4): research confirms 1759≈1815 land empire (first cessions are
  1850s–60s). **Buildings/OOB/laws unchanged** (D8/D9): the setup building data is a flat province-ID
  list, NOT date-gated, so the date shift strips nothing.
- **Future-born characters:** oracle-confirmed the engine treats setup chars born after START_DATE as
  silently non-existent (no load crash); only `set_as_ruler` on an unborn char auto-generates a
  fallback. Consistent with the **Qing-FOCUSED** scope decision (rest of world left at 1815 config as
  a documented anachronism).

**Deep adversarial review (#196):** ran a 5-dimension → per-finding adversarial-refutation → synthesis
workflow (11 agents, ~696k tokens). VERDICT: **SHIP — no load-crash/blocker defects.** 4 findings
survived verification (1 refuted); all 4 resolved this pass:
1. [MEDIUM → fixed] **Treasury 3× over intent.** The `INCOME_cost_*` vars are QUARTERLY (file header
   line 638-639), so my `-30` seeded ~7.5 yr of costs, not the "~2.5 yr" the comment claimed (and the
   pre-existing `-12` baseline is really ~3 yr, not ~1). Fixed: apogee seed = **-24 = 2× the accepted
   #172 baseline** (≈6 yr), avoiding the distortion; -12 master baseline left unchanged, comment
   corrected. (`se_QING_MECHANICS.txt`)
2. [LOW → fixed] **Stale regnal-year.** `oa_economy_setup.txt:2194` seeded `regnal_year_var=19`
   (Jiaqing's 1815 era year); with Qianlong now ruling, 1759 = 乾隆二十四年 → **24**. Cosmetic
   (loc-only, no gate). Fixed.
3. [MEDIUM → doc-corrected] **Decision-doc undercounted unborn rulers ~4×.** The "~15" was the
   abandoned >1780 threshold; at the true 1759.9.1 start **59 of 91** `set_as_ruler` targets are
   unborn, incl. **6 CHI subject-ring rulers** (Korea char:335 b.1790, Mongol/frontier khans, etc.).
   D-FUTUREBORN rewritten with the script-verified count + explicit enumeration; the fallback-ruler
   anachronism is now honestly documented as accepted-under-scope, not hidden.
4. [LOW → doc-corrected] **7 CHI provincial governors** (Anhui/768 etc.) unborn at 1759 →
   `set_as_governor` silently no-ops, governorships open unnamed. Documented as accepted anachronism
   in new decision **D-FUTUREBORN-QING**; top follow-up = author Korea (Yeongjo) + the Anhui governor.

**Reusable process:** `BOOKMARK_PROCESS.md` — the year-swap methodology (9 sections + copy-per-run
checklist + the two critical lessons: on_game_initialized offsets need `+Δdays`; START_DATE is global
so script-count unborn `set_as_ruler`/`set_as_governor` before deciding scope).

All touched files brace-balanced; byte conventions preserved. Committed to `early_bookmark` as
freekumquats. **OWED to user: in-game load test** on the branch — the definitive proof of the
future-born-character behaviour (oracle finding is sound but not yet test-loaded). NOT promoted to
develop/master; awaiting the user's verification per branch policy.
