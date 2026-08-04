# Nine Qing Player-Experience Mechanics — Approved Roadmap

_Migrated from memory imp19c-qing-mechanics-roadmap per the research/design-digest-location rule. Design spec — see the memory pointer for status._

Roadmap for fleshing out the Qing (CHI) player experience, proposed 2026-07-03 after the subject-integration event chain shipped. Nine mechanics, three groups. Proposal is approved in principle; implementation sequencing agreed but each mechanic still built + reviewed on the pattern of the shipped [[imp19c-subject-interactions]] chain.

**Build on existing (event-chain + country modifiers + gated pulse, like qing_integ.*):**
1. Inter-ethnic tension as an ongoing stance (banner/civilian divide, Manchu-Han dyarchy, Lifan Yuan).
2+3. Distance + language friction — **DECISION: SIMULATE** via distance- and culture-mismatch-scaled modifiers + "orders arrived too late" events. NO literal turn-delayed orders (too much plumbing for the payoff).
6. Ming-style treasure fleets / maritime revival — alternate-history, best as a mission-tree branch or major decision (heavy cost, Confucian-official backlash, tributary/trade reach).
7. Golden Urn (金瓶掣籤) — Tibetan-subject succession event: enforce (control+, loyalty-) vs. exempt (loyalty+, control-). Cheapest + most flavorful → recommended PILOT.

**Needs a new mechanic:**
8. Sinicization vs. Manchu identity — per-character variable (0..N) + trait/modifier consequences + choice events (Han marriage, Manchu-language exams). Medium effort.
4+5. Squabbling heirs + Yongzheng's secret succession (秘密立儲) — factional-support character vars + decline-triggered clash events + a reform that swaps the succession ruleset. Highest effort; sequence LAST. Imperator succession is engine-driven, so this layers on top.

**Reform track — DECISION: FULL TRACK, split into TWO DISCRETE STEPS:**
- **Step 9a — Reform events (@1815):** indigenous Confucian statecraft (經世致用) events — admin/anti-corruption reform within the monarchy (reuse existing modifiers). BUILD ON EXISTING; low–med effort. Build first.
- **Step 9b — Full constitutional republic track:** three-way traditionalist ↔ constitutionalist (君主立憲) ↔ republican tension with government-form consequences, up to ending the Qing as a republic (1911 analogue). NEW SUBSYSTEM; high effort. Build second, after 9a. Committed.
  - **DECISION: gate LOOSENED — don't tie 9b tightly to the ~1840 historical trigger.** It's fine for the track to open somewhat EARLIER than it really happened (gameplay > strict chronology). Trigger should still be event-/pressure-driven (reform pressure from A silver-drain / C banner decay / D corruption / J literati + some foreign-contact or defeat pressure), but the pressure can accumulate and unlock the track before 1840 if the player's situation warrants. No hard pre-1840 date lock. Perf note: this means it is NOT reliably dormant early — build the pressure meters counter-based so an early unlock stays cheap.

Historical grounding + full citations for all nine are in the research report (Elliott *The Manchu Way*, Rawski *The Last Emperors*, Oidtmann *Forging the Golden Urn*, Silas Wu *Passage to Power*, Rowe *China's Last Empire*, etc.) — see [[imp19c-qing-history-and-mechanics]].

## ADDITIONAL mechanics I proposed from the same research (A–J), not on the user's original list

A/D/F/G interlock into a single "dynastic decline" engine (silver stress → corruption → floods/famine → rebellion) that is the natural pressure source unlocking 9b. Each is a counter reading the others' state, so combined cost stays negligible.

- **A. Currency-crisis stress (silver drain).** REFRAMED: the currency layer is bimetallic **gold/silver** (not silver/copper — copper doesn't exist as state). Map onto the EXISTING reserve-ratio + inflation values (CURRENCY_ideal_reserve_ratio, CURRENCY_stability_impact_ideal_reserve_ratio, CURRENCY_inflation_value), NOT a silver/copper spread. Opium trade as a reserve-drain; widening reserve stress → real-tax/unrest pressure + events (legalize vs suppress → Lin Zexu → the war that feeds 9b). Ties economy sim → reform track. Highest-value non-original idea.
- **B. Sale of offices (捐納).** Decision: treasury now → rising corruption meter (D) + admin malus. Feeds D and currency layer.
- **C. Banner fiscal/martial decay.** INSTITUTIONAL (distinct from #8 cultural identity): growing stipend upkeep + decaying banner military-effectiveness modifiers. Small new mechanic. Feeds 9b pressure.
- **D. Systemic corruption meter.** One country var; generalizes shipped qing_integ.11 (Heshen/yanglian yin). Raised by B & war, lowered by audits/9a. Read by A/E/G.
- **E. Yellow River / Grand Canal (河工).** Flood events whose severity scales with D; fund-maintenance vs defer-and-gamble. Province modifiers.
- **F. Ever-normal granaries (常平倉).** Grain-reserve stock built in good years (extends shipped tuntian harvest qing_integ.20), spent in famine; failure feeds G.
- **G. Secret societies / millenarian sects (白蓮教/天理教/天地會).** Hidden pressure counter fed by A/D/F → rebellion triggers. The consequence engine.
- **H. Tributary / Canton System diplomacy (公行).** ACTUAL system (distinct from #6 alt-history fleets): manage Cohong monopoly + tribute missions; trade income; friction point that ignites 9b's war.
- **I. Palace-memorial intelligence (奏摺).** FOLD INTO #2/#3 — the info-vs-courier-speed counterweight, not a separate build.
- **J. Literati loyalty (聖諭).** Small counter or fold into #9; the swing constituency reformers/constitutionalists come from. Reads government form, doesn't drive it.

## BINDING CONSTRAINTS (dependency-safety — do NOT violate; discovered by auditing repo WIP markers)

1. **Bind to public effects + CACHED values, never internals or hot-paths.** Use documented CURRENCY_*/TRADE_* effects and read cached values (CURRENCY_cache_power, CURRENCY_update_global_currency_status). NEVER add work to common/on_action/economy/oa_wealth_changes.txt — authors flag it "causing unacceptable monthly slowdowns." A and any per-governorship currency reader must ride cached values, not recompute on the monthly tick.
2. **9b must NOT bind to `is_parliamentary_government`** (common/scripted_guis/government_view_scripts.txt) — it's a hardcoded government-type list with a live TODO to replace it with a generic parliamentary-legislature trigger. Drive 9b transitions through the government-form-change effect + 00_constitutional_laws.txt, or a Qing-scoped predicate I control. Otherwise transitions silently misfire when that TODO lands.
3. **A is reframed onto gold/silver reserve-ratio + inflation** (see A above). The original silver/copper-spread framing depended on state that does not exist.

Net dependency risk: only A and 9b had real risk; the constraints above neutralize both. Everything else binds to engine-stable modifier keys / variables / triggered events. NO mechanic depends on the pop-employment system (there is no standalone jobs system; labor = buildings + pops + trade sim). Future currency/trade/government completion changes the NUMBERS these mechanics see (tuning), not the INTERFACES they call (correctness) — provided the constraints hold.

Standing constraint: features are QING-ONLY, player-only (ai_is_valid always=no, pulse gated is_ai=no). Finish + review each before starting the next.

## IMPLEMENTATION STATUS — all 19 mechanics IMPLEMENTED + validated (session 2026-07-03 cont.)

"implement everything proposed here" is DONE and self-validated (game not installed → validated by brace-balance + repo-precedent + cross-reference, not an in-engine run). Files created:
- `common/scripted_effects/se_QING_DECLINE.txt` — shared decline engine: clamped counters (qing_corruption_level / sect_pressure / banner_decay / ethnic_tension / currency_stress / reform_pressure / granary_stock), band appliers, derived reform-pressure, `QING_DECLINE_pulse`, `QING_frontier_flavour_roll`, `QING_DECLINE_roll_reaction`.
- `common/scripted_effects/se_QING_MECHANICS.txt` — player verbs (set stance, sell offices, granary invest/release, banner drill, audit, suppress sects/opium, Canton open/close, char identity init/shift).
- `common/modifiers/qing_mechanics_modifiers.txt` — all suite modifiers (country + one province `qing_flood_devastation` + two character `qing_manchu_*`).
- `common/scripted_guis/QING_mechanics_actions.txt` — 12 always-available player buttons; `custom_tooltip{text+condition}` inside `is_valid` matches shipped `summon_curiate_assembly`/`WAR_scripted_guis` convention.
- Events: `qing_decline_events.txt` (.10-.14,.20), `qing_reform_events.txt` (.10,.11,.30,.31,.32), `qing_frontier_sea_events.txt` (.10,.11,.20,.21,.30), `qing_character_events.txt` (.10,.11,.20,.21,.22), `qing_golden_urn.txt` (.1).
- `common/on_action/qing_mechanics_on_actions.txt` (on_game_initialized CHI init) + `qing_mechanics_pulse_on_action` added to monthly_country_pulse in `00_monthly_country.txt` (CHI+human gated, 90-day cooldown var).
- `localization/english/qing_mechanics_l_english.yml` — UTF-8 **with BOM** (had to prepend manually); all 154 event/tooltip keys + all 32 modifier display names, cited-history style matching qing_subject_integration loc.

Validation pass results (all PASS): brace-balance across 11 files; every `trigger_event` id resolves (only outside-suite refs are vanilla `scheme.*` in the shipped integration file); every referenced modifier defined (incl. base `local_unrest_harsh`, golden-urn reuse of `qing_integ_frontier_resentment`/`qing_integ_imperial_favor`); every `QING_*` scripted effect + `LOG_enter/exit/line` resolves; no event-ID collisions; all namespaces declared; loc coverage 100%. Constraint compliance held: decline engine reads only cached `CURRENCY_reserve_ratio_impact` (never touches oa_wealth_changes.txt); 9b uses `change_government` + `qing_reform_faction_balance` var, NOT `is_parliamentary_government`; A framed on reserve-ratio.

Known deferable follow-ups (not blockers): scripted-GUI buttons exist as scripted_guis but are not yet wired to a specific GUI window widget (.gui) — reachable once a Qing panel/button is added, same as any scripted_gui; numeric tuning is placeholder-reasonable and will want a playtest pass.
