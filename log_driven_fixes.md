# LOG-DRIVEN fixes — #371 (fresh 1763 boot error.log/debug.log sweep)

This file tracks the LOG-DRIVEN bug-fixing effort: fixes driven by what the fresh
error.log/debug.log actually report (ranked by frequency/severity), separate from the
user-reported BT-N playtest items. See SESSION_REPORT.md for all other work.

## #371 LOG-DRIVEN fixing — 6 runtime-error clusters from the fresh 1763 boot (2026-07-11)

Per the directive to fix what the LOGS actually report (ranked by frequency), swept the fresh error.log (~5.09M lines) with a dedup signature survey and fixed the six highest-frequency scope/variable clusters (>1.55M log lines total). Each is a SCOPE-MISMATCH or unset-variable class error, fixed to a PROVEN upstream idiom (not my own files). `[logfix]` comments on every touched line; all files brace-balanced; line endings preserved.

**1. `invention` in unit `allow` — Wrong scope: state, expected country (~1.5M lines, two files).**
Unit `allow`/`on_activate` blocks evaluate in STATE scope, not country (the in-file comment claiming "country scope" was wrong). `invention` is a COUNTRY trigger. Fixed by hopping state->country via `owner = { invention = ... }` (proven building-gate idiom, qing_production_buildings.txt:42):
  - common/units/army_riflemen.txt: `invention = tech_rifles` -> `owner = { invention = tech_rifles }` (trade_good_surplus stays bare — valid in state scope, warelephant precedent).
  - common/units/army_artillery.txt: `invention = tech_cannons` -> `owner = { invention = tech_cannons }`.

**2. `qing_trib_gift` unset-variable — Failed to fetch variable (60k lines).**
common/scripted_effects/se_QING_TRIBUTE.txt QING_tribute_receive: `set_variable = { value = has_monthly_income }` was not persisting the var, so the `< 0` / `> 0` reads below hit an unset var. Switched to INITIALIZE-BEFORE-READ: seed to 0, then `change_variable = { add = has_monthly_income }` under a `>= 0` guard (proven add-income form, 00_event_values.txt:23). Guarantees a real value type before any compare.

**3. `num_of_unit_type` in governorship scope — Wrong scope: governorship, expected country (4071 lines).**
common/script_values/DEMAND_luxury_svalues.txt DEMAND_rifles_base evaluates in GOVERNORSHIP scope. `num_of_unit_type` is a COUNTRY trigger. Moved it INTO the existing `owner = {}` hop alongside the (already-correctly-hopped) invention gate.

**4. `total_population` read in STATE scope — Wrong scope: state, expected province (~1.5k lines, two files).**
`total_population` is a PROVINCE trigger.
  - se_QING_SPHERE.txt: the STATE-scope `state = { total_population > 0 }` and two `every_country_state` limits -> reach the province via `any_state_province = { total_population > 0 }` (proven, invest_in_state_buttons.txt:149).
  - se_QING_MISSIONARY_STATIONS.txt: six `state = { total_population > 0 }` reads were already in PROVINCE scope (inside owned/neighbor-province iterators) -> dropped the stray `state = {..}` wrapper, read `total_population > 0` directly. (order_by = total_population at line 322 is a valid province-scope order key, untouched.)

**5. `famine_province` undefined event target (245 lines).**
events/imp19c_mod_events/economy/shortage_events.txt shortage.1: the event could fire (and the random pick could land) on a shortage-governorship whose every candidate province was already recent_famine-flagged, so save_scope_as = famine_province never ran and every scope:famine_province read threw. Tightened the event `trigger` and each `random_*` `limit` to require, at EVERY level, a descendant province that is populated (`total_population > 1`) AND not already `recent_famine` — guaranteeing a save-able province before the scope is read.

**6. bare `religion =` on CHARACTER scope — Wrong scope: character, expected country (~261 lines, three files).**
`religion` is a COUNTRY trigger (CONTRAST: `culture` IS a valid character trigger — the parallel culture-compare lines correctly needed no change, and log evidence confirmed 0 culture errors). A char-scope faith compare must navigate the `.religion` link on BOTH sides: `this.religion = X.religion` (proven, party_types 00_default_republic.txt:154).
  - se_QING_AFFINITY.txt QING_char_affinity:73 (`limit = { this.religion = root.current_ruler.religion }`) and QING_pair_friction:371 (`limit = { NOT = { $a$ = { this.religion = $b$.religion } } }`).
  - 00_marriage_triggers.txt MARRIAGE_same_faith_trigger:106 (`current_ruler = { this.religion = scope:target.current_ruler.religion }`).

**Adversarial self-review:** full diff re-read; all 9 files brace-balanced (verified OK); every fix maps to a cited proven upstream site; no behaviour change beyond eliminating the scope/unset error (each fix makes an errored read into the intended clean read/false). Committed to 1763_bookmark. In-game boot test owed to confirm the clusters are gone.

**DEFERRED (documented, next log clusters):** illegal-operator `<`/`>` council chain (BT-13/#373); `sqrt line: 27` illegal-op + empty-type "Variable not of the 'value' scope type" (3796) in oa_wealth_changes.txt; ADD_PRESTIGE_EFFECT_POSITIVE loc-key 66k (display-only, overlaps BT-5/6/#380); char-via-ID scope failures (272); ChineseEvents.txt:43 parse (low priority, upstream 1815-only Amherst event); set_as_ruler nulls (upstream setup files).

## #371 LOG-DRIVEN fixing — economy WEALTH chain + two `prev`-across-absolute-jump empty-type bugs (2026-07-11)

Second batch, continuing the frequency-ranked sweep. Root-caused the largest remaining cluster — 41,073 "Invalid left side during comparison 'var'" plus a big share of the ~3,802 empty-scope errors — to the WEALTH quarterly cache/aggregation path, and two smaller empty-type clusters to a newly-characterised `prev` scope rule. Four files, all brace-balanced (403/283/56/396), CRLF preserved on WEALTH_svalues.txt.

**The `prev`-across-absolute-`root`-jump rule (empirically established this session).** `prev` is NOT preserved across an ABSOLUTE `root`/`ROOT` scope jump — inside `root = { ... }` (or `ROOT = { ... }`), `prev` resolves to an EMPTY scope, so `prev.var:X` yields an empty-type value and `change_variable`/comparisons on it throw "Variable not of the 'value' scope type. Type: empty". It IS preserved across a RELATIVE link (`owner = {}`, `scope:X = {}`) or an explicit inline scope-change. Proven working precedent, all 0 errors: se_SELL.txt:1124 (`owner = { add = prev.var:... }`), se_QING_COUNCIL.txt:439 (`<char> = { ROOT = { add = prev.martial } }`). FIX PATTERN: `save_scope_as = X` before the jump, then read `scope:X.var:` inside root (proven idiom se_SELL.txt:1569).

**1. WEALTH quarterly cache — 41,073 "Invalid left side during comparison 'var'" (two edits).**
  - common/scripted_effects/se_ECON_wealth.txt WEALTH_cache_shipping_trade_values (~1103): this effect runs at oa_wealth_changes.txt:277, ONE line BEFORE GT_reset seeds `trade_income_due_shipping`/`trade_expenses_due_shipping`, so both reads hit unset vars. Rewrote both `set_variable`s to seed 0 then `add` under a `has_variable` guard (INITIALIZE-BEFORE-READ; proven SHIPPING_svalues.txt:281). The expenses sign-flip now also guards on the var existing.
  - common/script_values/WEALTH_svalues.txt WEALTH_total_last_quarter_governorship (~1250): the four `final_quarterly_trade_*` vars (income/expenses × resource_extraction/manufacturing) are NEVER set ANYWHERE in the codebase (only read here, unguarded, and in TRADE_svalues.txt:4154 where they ARE has_variable-guarded). Wrapped the four subtracts in a combined `has_variable` guard — behaviour-preserving (they were already no-ops) but eliminates the unset-var errors. CRLF re-applied after a Python-heredoc write flattened endings (same gotcha as #348 se_LAND.txt).

**2. ECON_LOG production snapshot — 1,860 empty-type errors (`prev`-across-`root`).**
common/scripted_effects/se_ECON_LOG.txt ECON_LOG_production_snapshot (~206): `every_governorships = { ... root = { change_variable = { add = prev.var:industrialisation_bonus_cached } } }` — `prev` inside the absolute `root` jump was empty. FIX: `save_scope_as = econ_log_snapshot_gov` before the jump, read `scope:econ_log_snapshot_gov.var:` inside root.

**3. QING faction tally — 152 empty-type errors (`prev`-across-`ROOT`).**
common/scripted_effects/se_QING_FACTION.txt QING_faction_tally (~205): same pattern inside `ROOT = { ... }`. FIX: `save_scope_as = qing_faction_tally_char`, read `scope:qing_faction_tally_char.var:qing_char_stance_wtd` inside ROOT.

**4. LOG-string `$amount$` macro violation (latent, pre-existing) — se_QING_FACTION.txt:141.**
QING_char_stance_shift's exit `LOG_line` embedded a `$amount$` macro inside the debug string, which triggers mass "unknown arguments" load errors (the string is scanned for macro params at parse-time — the standing log-string-macro rule). Made the message STATIC ("char stance shift applied to drift for"); the signed shift remains observable via the qing_stance_drift var trace.

**Adversarial self-review:** full diff re-read; 4 files brace-balanced (0); WEALTH_svalues.txt diff confirmed as the ~14 real lines (no phantom reflow) after CRLF restore; each fix maps to a cited proven site; the two `prev` fixes and the WEALTH guards are strict no-op-or-cleaner (no behaviour change beyond eliminating the error). HYPOTHESIS to confirm on re-boot: the faction_tally empty-write corrupted `qing_faction_stance_total`, which may have cascaded into the deferred illegal-operator `<`/`>` council chain (BT-13/#373) — verify that cluster shrinks after this batch.

## #371 LOG-DRIVEN fixing — officer-report commander scope non-promotable for `.GetName` (2026-07-11)

Third batch. The Downloads/error.log (5.09M lines, boot 13:28–14:36) is the PRE-fix baseline — its entire top tier maps 1:1 to clusters already fixed in batches 1–2 (invention 1.5M, qing_trib_gift ~82k, WEALTH invalid-left-side 41,105, num_of_unit_type 4071, empty-type 3796, total_population 899, religion 261). Skipping those (fixed) and taking the largest GENUINELY-unfixed cluster.

**79k `officer_report_commander.GetName` promote failures — a scope saved off a unit's `commander` LINK is not loc/LOG-promotable.**
common/scripted_effects/se_QING_COUNCIL.txt QING_council_officer_report_check (~1339). The Grand-Council officer-report event `qing_office.31` references `[scope:officer_report_commander.GetName]` in its desc + both option tooltips. That threw `pdx_data_factory` "Failed to find type 'scope:officer_report_commander' … Could not find promote" — 26,332 desc + 120 (minister sibling elsewhere) but 78,996 total across the three loc slots + the immediate LOG — every frame the popup was open (22k/min over 4 min for a single fire).
DIAGNOSIS: in the SAME desc string, `officer_report_minister.GetName` resolved (360 errors, incidental) but `officer_report_commander.GetName` did not (78,996). The only difference: the minister was saved from a COUNTRY VARIABLE (`var:qing_office_war_holder`), the commander from a unit's `commander` LINK inside `random_unit = { commander = { save_scope_as } }`. A commander-link-sourced character scope resolves in script triggers/effects (the event's `exists` guard passed, `right_portrait` rendered, `add_loyalty` applied) but is NOT typeable by the data-factory for a `.GetName` promote — even one line later in the effect's own immediate LOG.
PROOF: `qing_war.1`'s `able_commander`, saved via `random_character` and read via `[scope:able_commander.GetName]` in loc, logs 0 promote errors. Invictus only ever uses `commander = { save_scope_as }` in effects/triggers, never a loc `.GetName`.
FIX: pick the officer as a CHARACTER via `random_character = { limit = { is_general = yes  is_alive = yes  employer = ROOT } }` (a general is by definition a live unit commander → same population; `is_general` is a proven `random_character` filter, internal_politics_monarchy.txt), with capital-garrison detection via the general's own `.location` link (proven province link, recruit_general.txt:85) instead of `random_unit`'s `unit_location`. Brace-balanced (0). The `any_unit` guard likewise became `any_character = { is_general = … }`.
NOTE: se_JAPAN_BOSHIN.txt:180 `jpn_boshin_commander` is saved from a country VARIABLE (`var:domain_commander`), so it is promotable — NOT the same bug, left as-is.

**BT-13/#373 illegal-operator `<`/`>` council chain — believed resolved by batch 2, pending re-boot.** Static trace: `QING_faction_tally`'s pre-fix empty `prev.var:qing_char_stance_wtd` write corrupted `qing_faction_stance_total` (se_QING_FACTION.txt:222) → copied into `qing_council_reform_lean` (line 357) → every downstream `reform_lean` `<`/`>` comparison (feed_reform_balance, council_recompute, and the ~11 event files that terminate in QING_council_recompute/QING_faction_recompute) threw "Illegal use of operator". Batch 2's faction_tally fix makes `stance_total` a clean value, so `reform_lean` is clean and the whole chain should resolve. To confirm on the next boot's log.

## #371 LOG-DRIVEN fixing — council recompute run character-rooted from the appoint/vacate GUI (2026-07-11)

Fourth batch. The single LARGEST genuinely-unfixed runtime cluster: **2,072 "Left side and right side during comparison were of different types (left was 'country', right was 'character')"** plus the 64-count "Event target link 'current_ruler' … Expected 'country', but got 'character'" and shares of the QING_char_affinity / QING_faction_tally / QING_council_score_figurehead / QING_council_prune_seat error counts. This is ALSO the root cause of the user-reported **BT-13/#373 "Grand Council chancellor appoint mass-vacates the council"** — the same defect surfaces both as a log flood and as the seat-clearing gameplay bug.

**ROOT CAUSE — the character-scope GUI appoint/vacate verbs run the country-scope council machinery with ROOT = the clicked courtier, not CHI.**
Every error signature in the cluster begins at `common/scripted_guis/QING_governance_actions.txt` (the 13 `qing_gov_office_appoint_*` verbs + `qing_gov_office_vacate`), which are `scope = character`. They call `QING_office_appoint` / `QING_office_vacate_dispatch` on the clicked courtier, so **ROOT = that character**. Inside the effects, `employer = { … }` rebases `this` to CHI but LEAVES ROOT pointing at the character. The entire `QING_council_recompute` helper tree (prune_all_seats → prune_seat, score_office / score_chancellor / score_figurehead, classify_ethnicity, QING_faction_recompute → faction_tally, and the per-member QING_char_affinity) plus `QING_council_refresh_candidates` are all written for **ROOT = CHI**. So on the GUI path:
  - every `employer = ROOT` / `is_alive = yes  employer = ROOT` guard compared a **country** (`employer`) against a **character** (ROOT) → the 2,072-line type-mismatch flood;
  - `root.current_ruler.*` reads (QING_char_affinity zeal/culture/religion/friendship compares) hit "expected country, got character" (the 64-count current_ruler error);
  - critically, the mistyped `NOT = { var:qing_office_$office$_holder = { is_alive = yes  employer = ROOT } }` guard in `QING_council_prune_seat` (and the parallel guards in score_office) mis-evaluated, so LIVE, valid seats were read as invalid and **pruned/skipped** — the visible "appointing a chancellor empties the council" bug (BT-13).
The pulse (`qing_mechanics_on_actions.txt`), the council events, and `QING_council_autofill` all invoke the machinery **country-rooted** (ROOT = CHI), which is why the council works normally outside a manual appoint/vacate — and why every error signature traced back to the GUI, never the pulse.

**FIX — re-root once at the GUI boundary via a hidden CHI `country_event`, leaving the ~2,000 lines of tested machinery byte-identical.**
Added `qing_office.40` (events/imp19c_mod_events/qing_office_events.txt): `type = country_event  hidden = yes  is_triggered_only = yes`, immediate = `QING_council_recompute = yes` + `QING_council_refresh_candidates = yes`. A triggered country_event always roots on the country it fires on, so ROOT = CHI inside it.
  - `QING_office_appoint` tail (se_QING_COUNCIL.txt:1155): `employer = { QING_council_recompute … refresh … }` → `employer = { trigger_event = { id = qing_office.40 } }` (employer of the appointee = CHI → event roots on CHI).
  - `QING_office_vacate` tail (se_QING_COUNCIL.txt:1211): `QING_council_recompute … refresh …` → `trigger_event = { id = qing_office.40 }` (this effect already runs with `this` = CHI via the dispatcher's `employer = {}`, so the event targets CHI).
This is the SAME rooting the working pulse/event/autofill callers give the machinery, and matches the in-file precedent `QING_council_officer_report_check` → `trigger_event = { id = qing_office.31/32 }` for re-rooting. Behaviour-equivalent: the recompute+refresh still run once per appoint/vacate, now always on CHI. The nested appoint-over-sitting-holder path (QING_office_appoint → QING_office_vacate_dispatch → QING_office_vacate) previously ALSO ran a char-rooted recompute inline (part of the flood); it now re-roots through .40 too.

**Adversarial self-review:** both files brace-balanced (0/0); `qing_office.40` id is unique; hidden triggered country_events need no title/desc (proven imp19c_setup.1); `trigger_event` with no delay is the codebase's synchronous re-root idiom (officer_report_check). No behaviour change beyond eliminating the mis-typed comparisons and the wrongful seat prune. CONFIRM on re-boot: the 2,072 country-vs-character + 64 current_ruler + associated affinity/faction/figurehead/prune counts drop to 0, and (BT-13) appointing a chancellor no longer empties the council.
