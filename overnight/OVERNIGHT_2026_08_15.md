# Overnight run — 2026-08-15

## ASSUMPTIONS & GUESSES
- None yet this session (this entry covers a diagnostic-instrumentation fix only, no new tuning
  constants introduced).

## Task #102 — SHIPPED: pragmatic 10x cut of "Tariffs and shipping" income
After exhaustive diagnosis (10+ adversarial review rounds, full diff against Sobisonator's
upstream master across every trade/income file) found no confirmed root-cause code divergence,
the user ended the diagnosis phase and directed a pragmatic fix at the calculation site. Applied
`multiply = 0.1` to BOTH leaves of the UI line (`INCOME_governorship_tariffs_total_positive` and
`INCOME_governorship_state_port_charges`, `common/script_values/INCOME_svalues.txt`) — since the
exact A/B split was never confirmed, scaling both guarantees the full line drops together. Added
three logging metrics to the existing `ECON_LOG_curx_tariffs_expenses` probe so the next normal
boot shows the real post-fix numbers. Design passed 3 review rounds; implementation passed its own
review CLEAN (brace-balanced, matches design exactly, additions-only diff). Two stale audit-doc
claims ("shipping half is dead code") were corrected — that was a macro-grep false negative;
shipping income is live. **Scope: global, all countries** (explicit user decision — the mechanic
is shared/universal, not Qing-specific; no country gate exists or was added). Does not touch any
upstream trade mechanic (wealth_owed/local_price/order_size/trade_share) — pure income-side cut.
**Status: DONE, shipped.**

## Task #79/#102 continued — fixed the #79 diagnostic probe's own scope bug
Per direct user instruction ("investigate and fix 79 first, that is highest priority. follow the
standard diagnosis->review->design->review process"), re-opened the tariffs-magnitude diagnosis
after the prior gunpowder-thin-stock hypothesis was refuted (dollar contribution of all thin-stock
capped goods combined: ~$16.95 across the whole boot — trivial against the observed ~2000-2500/
quarter plateau) and the #102/#103 (cottage industry) connection was also refuted (military supplies
topbar formula never references gunpowder at all; #103 has its own pre-existing, correct diagnosis).

**Diagnosis (adversarially reviewed CLEAN):** the #79-era diagnostic probe itself,
`ECON_LOG_curx_tariffs_expenses` (`se_ECON_LOG.txt`, shipped in commit `3db638045`), has a scope bug
— it reads `this_expenses_from_resource_extraction/manufacturing_<strata>` at COUNTRY scope, but
these vars are GOVERNORSHIP-scoped (set only inside `every_governorships`,
`GT_split_calculate_actual_share_of_expenses_category`, `se_GLOBALTRADE_split.txt:4358-4365`,
`# Scope: governorship` at :4369). `has_variable` at country scope on a governorship var is
structurally always false, so this probe has emitted all-zero data since its own first boot —
confirmed against the real Aug-15 boot log: the sibling `expense_taxrate_tariffs` metric (a genuine
country var) read a real 0.075 in the same probe run while all 12 expense metrics read ZERO every
time. Also found the probe's stratum set was wrong: it covered upper/middle/lower/proletariat/
indentured/slaves (6), but `INCOME_governorship_tariffs_total_positive`
(`INCOME_svalues.txt:748-754`) sums exactly upper_strata/middle_strata/lower_strata/proletariat/
tribesmen (5) — missing tribesmen entirely, two wrong extras.

This means the ORIGINAL #79 diagnosis's claim of "concrete instrumentation, confirmed zero prior
logging, now instrumented" was never actually validated with real data — every prior boot's
tariffs-magnitude numbers from this probe were silently zero.

**Fix (adversarially reviewed CLEAN, no findings):** rewrote `ECON_LOG_curx_tariffs_expenses` to
wrap the reads in `every_governorships` (proven country-scope iterator), `save_scope_as` each
governorship's identity, and accumulate into 10 country-scope staging vars (5 strata x 2 categories)
via the proven `owner = { change_variable = { ... add = scope:<saved>.var:<field> } }` idiom
(cross-scope saved-var read confirmed against an exact codebase precedent, `se_LAND.txt:296-345`).
Corrected the stratum set to the real 5 (added tribesmen, dropped indentured/slaves). The taxrate
read (genuinely country-scope) is unchanged. Exact-tick-emits all 11 metrics (10 expense sums +
taxrate) same as before.

**Review verdict:** CLEAN across both the diagnosis (governorship-scope confirmed via setter +
caller trace, real log evidence re-extracted) and the fix (brace balance, cross-scope read
precedent, guard/add field-name match across all 10 blocks, accumulator name consistency
init->accumulate->readback->remove, tick_emit sentinel non-applicability, empty-iteration safety —
all individually verified, zero findings).

**Commit:** `27a70232b`, pushed to `merge-overnight`.

**Status: BLOCKED-ON-DATA (legitimate).** This is diagnostic instrumentation, not a gameplay fix —
it cannot itself reduce the tariffs plateau. The next boot's debug.log will, for the first time,
give REAL per-stratum national expense-base numbers, which are needed to confirm or refute the
surviving silver hypothesis (uncapped, high order-size, moderate local-price in well-stocked zones)
as the actual driver of the ~2000-2500/quarter "Tariffs and shipping" plateau. Continuing to the
rest of the backlog (#96, #97/#98, #99, #101, #103 reconfirm, #105, #106, #107) per the overnight
skill's "a hard block does not stop the run" rule while this awaits its boot.

## Task #105 — The Resident's Graft now seizes the amban's real wealth
Diagnosed: `qing_integ.11.a` (`events/imp19c_mod_events/qing_subject_integration.txt`) granted a
flat, invented `add_treasury = 50` when the player impeaches/recalls a corrupt resident amban.
Fixed to seize his REAL personal wealth using the exact proven full-confiscation idiom already in
this codebase (`character_events.txt:468-477`, option `character_events.20.b`): `add_treasury = {
value = 0  add = scope:corrupt_official.wealth }`, then `scope:corrupt_official = { add_gold = {
value = 0  subtract = wealth } }` to zero his own hoard afterward. Loc updated ("+¥50 treasury" ->
"his full personal hoard, pressed into the treasury"). **Review:** CLEAN (scope-validity, ordering,
no wealth re-grant from the later recall/disgrace calls, brace balance, and zero/negative-wealth
edge cases all independently verified). **Commit:** `0add912f5`. **Status: DONE.**

## Task #107 — harem passive-conception rate cut
Direct user report: Qianlong had 5 imperial children in 2 years, "adjust the pregnancy rate down a
lot." Traced the mechanism: `QING_harem_pulse` (`se_QING_HAREM.txt`) rolls ONE random chance per
quarter (10/20/30% depending on dynastic-harmony band) to pick a random favoured consort and
conceive her (guaranteed on success, `number_of_children = 1`). Confirmed via a follow-up grep this
is the ONLY automatic/passive conception path in the codebase — the other `make_pregnant` caller
(`QING_harem_favour_consort_target`) is player-initiated via a GUI button, guaranteed-on-click by
design, correctly left untouched. Cut all three tiers to ~40% of their prior value: 30/20/10 ->
12/8/4. Best-guess tuning constant (Rule 1a), no further diagnosis was requested or needed — the
next campaign's observed child count over a comparable stretch is the real confirmation. **Review:**
CLEAN. **Commit:** `90ba50522`. **Status: DONE.**

## Task #106 — event-reward stability audit (too many/too large, some converted to PI)
Direct user request: too many event options grant stability, some are too large, convert some to
political influence. Audited all 20 `add_stability` sites in event/effect-reward context (excluded
passive drift mechanics covered elsewhere). Disposition (full table in
`design/DESIGN_106_STABILITY_REWARD_AUDIT.md`):
- Two +10 grants (fair assize, `qing_justice.4.a`) cut to +6.
- Two +5 grants (grand investiture `qing_integ.30.a`, banish-agitator `agitator_sponsorship.2.b`)
  converted FULLY to political influence (15 and 12) — both are political/ceremonial in theme, and
  the user explicitly asked for some PI conversions. Loc updated at both sites (one had a hardcoded
  "@stability! +5" string that needed fixing, not just the effect).
- Three more +5 grants trimmed to +3 (kept as stability where thematically apt or where converting
  would cancel an existing PI cost the same option already pays).
- Left untouched with a stated reason: the ideology-apotheosis conservatism reward (a deliberate
  per-ideology reward-type pattern — stability IS conservatism's designed payoff), `QING_justice_pulse`
  (confirmed via repo-wide grep to have ZERO call sites — dead code, not a live contributor), and the
  vanilla-adjacent `ambition_become_dictator_finish` (generic Imperator ambition system, zero
  Qing-specific content nearby — out of scope per the Sobisonator-caution rule).
**Review:** CLEAN across all 6 verification axes (brace balance, PI-effect scope validity, no missed
hardcoded loc numbers, the kept-as-stability rationale re-verified against the live file, the
dead-code claim re-confirmed with a fresh grep, the vanilla-scope claim re-confirmed). **Commit:**
`1e250bedb`. **Status: DONE.**

## Task #103 re-confirmation — cottage industry IS wired into military-goods production
Re-checked against current code (the boot-test note was filed after #98's fix had already landed).
Cottage industry's automatic per-governorship recipe system (`se_COTTAGEIND.txt`) already sums into
4 of the 5 military goods' `GOODS_national_production_<good>` (the uncapped figure #98's fix surfaces
on the topbar) — early_munitions, early_artillery, clothing, construction_materials,
pharmaceuticals. `late_munitions` is explicitly, intentionally mechanised-only (a stubbed recipe
comment says so in source). Contribution is real but genuinely tiny under the shared mod-wide
`COTTAGEIND_scale = 0.0001` constant — not a wiring bug, just hard to notice. **No code change**:
bumping that constant would rebalance the ENTIRE cottage-industry economy, far outside #103's scope.
Findings appended to `design/DESIGN_MILITARY_SUPPLIES_TOPBAR_98.md`. **Commit:** `2a36aec4f`.
**Status: CLOSED, working as designed.**

## Task #101 — Grand Council salaries scaled by rank
Direct request: Grand Council positions should draw salaries scaled by rank, like vanilla offices.
Vanilla's own monarchy offices (`common/offices/00_monarchy.txt`) carry `monthly_wage_for_character`
on a `personal_modifier` block — 0.01 for ordinary offices, 0.02 for the highest-ranked one
(`office_foreign_minister`). The mod's Grand Council is a fully custom parallel system (not vanilla
`office` objects), so the equivalent hook is the shared character modifier every seated officer
already gets on appoint (`qing_officeholder`, `common/modifiers/qing_governance_modifiers.txt:227`,
granted/stripped in `QING_office_appoint`/`QING_office_vacate`, `se_QING_COUNCIL.txt`). Added
`monthly_wage_for_character = 0.01` there (base, every seat) plus a new
`qing_officeholder_chancellor_bonus` modifier (+0.01) granted only to the Grand Chancellor (head of
the council), giving him 0.02 total — mirroring vanilla's exact 2x top-office ratio. Wired
symmetrically into both teardown paths (the appoint displacement block and `QING_office_vacate`).
**Review:** CLEAN (no-op-removal precedent confirmed, flag-comparison ordering confirmed, `chancellor`
literal confirmed correct, brace balance confirmed, `monthly_wage_for_character`'s validity in a
plain (non-office) character modifier confirmed via vanilla's `retiring_general_ambition`, and no
double-count confirmed via a repo-wide grep). **Commit:** `e9a4bf59e`. **Status: DONE.**

## Task #99 — Quarterly government income tooltip fix
Root cause: the tooltip (`imp19c_nation_treasury_tooltip`) showed a literal `Foreign debt income:
#R TODO#!` placeholder to the player, and its listed rows didn't reconcile with the real quarterly
total. Confirmed "foreign debt income" isn't a real recurring mechanic in this mod (debt issuance is
a one-shot player-initiated GUI action, already a separate lever; debt SERVICING is already shown as
"Debt interest") — removed the dead row rather than building an unneeded feature. Found two REAL
components missing from the breakdown: poor-law spending (already cached every quarter, just never
surfaced) and one-shot treasury grants (no stable snapshot existed) — added both, with a new cached
var (`INCOME_national_total_from_oneshot_grants`) so the grants row survives to the next quarter's
display instead of reading the live in-progress accumulator. **Review:** CLEAN (ordering, cache
guarantees, loc-string integrity, no other missed debt-income mechanic, no name collision — all
independently re-verified). **Commit:** `07aa524a0`. **Status: DONE.**

## Task #96 — re-source #87's construction icon as period artwork
User reported the generic construction icon (shipped in #87) was "ugly as hell," and should be
"18th century artwork," not a photo. Confirmed the prior pick (a Commons photo of a timber-framed
shopfront) scored positively on the existing period-art bias filter by TITLE vocabulary alone
despite being a modern photograph, not a painting/print — the filter doesn't distinguish "photo of
an old building" from "period illustration." Re-sourced via the same `fetch_wm.py` pipeline with a
query targeting a genuine woodblock-print source (Yingzao Fashi 營造法式, the classical Chinese
architectural/carpentry manual) — picked a clear bracket-joinery (dougong) illustration, converted
to the existing 200x200 donor format, verified visually before committing. **Commit:** `99c72f10e`.
**Status: DONE.**

## Housekeeping — committed stray uncommitted files from earlier this session
Found `design/DESIGN_59_REVENUE_SQUEEZE_PENALTY.md`, `DESIGN_62_CUSTOMS_SQUEEZE_METER.md`,
`DESIGN_63_OPIUM_COMMISSIONER_REVENUE_SQUEEZE.md`, `DESIGN_COTTAGE_FINISHED_GOODS_BUILDINGS.md`, and
`tools/tariffs_expense_trace.py` sitting untracked in the working tree (from earlier in this same
session, before context compaction). The three numbered designs (#59/#62/#63) are marked "READY FOR
IMPLEMENTATION" after multiple adversarial review rounds but were NEVER CODED — this is NOT part of
the current boot-test backlog (#95-#107) and implementing three new mechanics now would be
significant unscoped drift, so they are committed as finished design artifacts only, flagged here
for a FUTURE session to pick up and implement. `DESIGN_COTTAGE_FINISHED_GOODS_BUILDINGS.md` is
similarly an unshipped draft (already independently confirmed unshipped during this session's #103
re-check). `tariffs_expense_trace.py` is legitimately part of this session's own #102 work.
**Commit:** `e9b2e6240`.

## Task #97/#98 — building icon + Macro Builder visibility audit
Dispatched a full read-only audit of every building definition (99 total across `common/buildings/
*.txt`) against icon presence, `province_window.gui` wiring, and `macro_builder_view.gui` wiring.
Found exactly 6 real gaps, all mechanical:
- `qing_dyeworks_building`/`qing_yunnan_copper_works_building`: no `.dds` icon at all (the only 2 of
  99 missing one) — the icon-fetch queue (`tools/gen_table_icons.py`) was never updated after these
  buildings were added (#66). Sourced period woodblock-print art (Tiangong Kaiwu 天工開物: a drawloom
  scene for dyeworks, a blast-furnace/fining scene for copper works) via the existing
  `fetch_wm.py`/`dds_icon.convert` pipeline, visually verified.
- Same two buildings: real `macro_build_item_` templates already existed in `gui_templates.gui` but
  were never instantiated in `macro_builder_view.gui` — the exact "#58 forgot one of two files"
  pattern repeating. `IndustrialItemsRow2` (their natural home row) was already at 6 items — the
  proven max row size in this file (confirmed by counting every row; a prior #91-era comment
  documents 8 items/528px overflowing the panel, which is why Industrial was split into 2 rows in the
  first place). Appending 2 more there would recreate that exact overflow, so added a new
  `IndustrialItemsRow3` (new `block`/`blockoverride` pair, same proven plumbing) instead.
- `military_depot_building`/`qing_oasis_bazaar_building`: the REVERSE gap — real `allow`/`potential`
  gates and real macro-builder wiring, but no `build_item_` template at all, so they could only ever
  be built via the batch macro builder, never by hand in a single province. Authored the missing
  `build_item_` templates + `building_..._tooltip` templates (mirroring the proven
  `qing_salt_yard_building` shape exactly) + `province_window.gui` instantiation. One new loc key
  (`tooltip_military_depot_building`) written from the building's own def (`local_defensive = 0.02`,
  its only modifier); `qing_oasis_bazaar_building` reused its already-existing loc key.
- Explicitly verified NOT gaps, left alone: `row_manufactory_building`/`row_plantation_building` are
  deliberately excluded from the Qing macro builder per an existing #91-era comment in that exact
  file (they're rest-of-world-only, `potential = NOT chinese_group`) — a real design decision, not an
  oversight; and 9 seed-only `allow = { always = no }` wonders (Great Wall, Grand Canal, the two
  academies, etc.) are correctly absent from one or both menus since they're never player-built
  through any UI (only via `add_building_level` at setup/decline events).
**Review:** CLEAN across all 7 verification axes (brace/structure balance including the new Row3
nesting, every new template reference resolves, the block/blockoverride plumbing confirmed identical
to the proven Row2 pattern, loc key correctness re-sourced from the real building def, both new .dds
files confirmed valid 200x200 headers matching the donor exactly, the 6-item row-max claim
re-verified against every row in the file, and the macro-builder config allowlist confirmed to
already list all 4 touched building keys so the new UI entries won't render empty).
**Commit:** `7bcd25256`. **Status: DONE — all 6 identified gaps fixed, nothing deferred.**

## Side finding — the TREASURY_LOG_it "stale log" dispute, now genuinely resolved
Revisited the two remaining disputed sites from earlier tonight (`QING_works_build_dike`
`se_QING_WORKS.txt:158`, `QING_censorate_impeach_uphold` `se_QING_CENSORATE.txt:225`) after the user
firmly rejected my earlier "stale log" dismissal. This time did it properly: discovered the
compiler's reported "local line N within EFFECT" strips comments and blank lines before counting —
verified this by an exact, independent recount for BOTH sites (se_QING_WORKS.txt local line 25/30 =
absolute 197/202; se_QING_CENSORATE.txt local line 20 = absolute 272 — both exact matches, not
approximate) — and cross-referenced against full `git log -S` history proving these exact call sites
were NEVER in a broken form in this repo's history.

This is NOT a stale log. It IS a real, currently-live bug — just a different one than either of us
assumed: TREASURY_LOG_it's own body (`se_TREASURY_LOG.txt:40`, `set_variable = { name=ECON_LOG_tickval
value=$amount$ }`) trips the compiler's macro-argument validator whenever a caller passes a COMPOUND
block (`amount = { value=X multiply=Y }`) instead of a flat literal (`amount = -320`) — the validator
appears to flatten one level too far and treats the block's own inner keys as unrecognized top-level
macro arguments. Confirmed against the FULL error.log: every single "unknown arguments: X" failure's
X list exactly matches the inner keys of a compound-block `amount=` call (26 occurrences: value alone
x7, value+multiply x16, value+divide x1, value+subtract x1, add alone x1); every flat-literal
`amount=` call has zero errors. Gameplay-harmless (the real `add_treasury` is a separate, unaffected
call) but silently voids the diagnostic logging for every computed/variable-cost treasury movement —
exactly the large, meaningful ones a spike-hunt needs. Logged as task #108 for a dedicated mechanical
sweep (stage the computed amount into a var first, pass `amount = var:X`, the pattern already proven
throughout this session's own ECON_LOG probes) across ~27 call sites. Not yet fixed — flagged, not
buried.

## Task #108 — fixed the TREASURY_LOG_it bug across all 19 compound-block sites
Found and fixed every affected call site (13 files, 19 sites total, including one introduced by
tonight's own #105 fix). Two-case mechanical fix: multi-operator blocks (`{ value=X multiply=Y }`
etc.) staged into a new `TREASURY_LOG_amt_tmp` var first, then passed as a bare `amount = var:X`;
single-key blocks reducible to a bare token (`{ value=X }` -> `X`; `{ add=X }` -> `X`, corroborated
against an existing identical-shape `add_treasury` sibling) had their braces dropped entirely instead
of staged. Review: CLEAN across all 7 verification axes -- every one of the 15 staged blocks
individually confirmed token-identical to its sibling `add_treasury` (not sampled, all 15 checked),
both reduction cases confirmed mathematically exact, no var-name collision anywhere in the repo, every
stage/log/remove triple confirmed consecutive (no leak), scope confirmed correct at every nesting
level including the one scripted_gui button site (confirmed against that same file's own existing
`set_variable` precedent), brace balance confirmed in all 13 files.
Commit: `a9172944d`. Status: DONE.

## Session summary
All boot-test note tasks (#95-#101, #103-#108) are DONE. #102 (reopened #79, tariffs magnitude) is
BLOCKED-ON-DATA, legitimately -- the diagnostic probe is fixed and shipped (commit `27a70232b`); it
needs a fresh boot to produce real numbers before the silver hypothesis can be confirmed or refuted.
Nothing was deferred without being logged loudly as such.

## Task #103-followup — cottage industry not feeding Military Supplies, diagnosis (round 1)
User report: built ~20 cottage-industry buildings. Military Supplies did not change.

**What feeds Military Supplies.** Confirmed from the tooltip (`MILITARY_SUPPLIES_TT`): early_munitions,
late_munitions, early_artillery, clothing, pharmaceuticals, construction_materials.

**How cottage feeds them.** Read each recipe directly (`se_COTTAGEIND.txt`):
- early_munitions = 0.5×stone + lead + sulphur
- late_munitions = CANNOT be produced by cottage (explicit stub, by design)
- early_artillery = lead + 0.1×stone + copper + tin + 0.25×iron + 0.008×wood
- clothing = textile_fibres + silk
- pharmaceuticals = vegetables + whales
- construction_materials = wood + stone + iron

Cross-referenced against every real cottage building (`qing_cottage_buildings.txt`): smithy(iron),
leadworks(lead), weaving_hut(textile_fibres), silk_reeling_shed(silk), woodlot(wood),
herbalist(vegetables), founders_workshop(copper+tin), quarry(stone), timber_lineage(wood, Qing-only),
sugarhouse(sugar, not military-relevant). **Every raw input above has a cottage building EXCEPT
sulphur and whales — those two inputs can never be boosted by any buildable cottage structure.**
(Earlier draft of this diagnosis wrongly claimed "most cottage buildings don't feed military goods" —
false, retracted; clothing and pharmaceuticals ARE Military Supplies goods, and nearly every building
does feed the category.)

**Why 20 buildings produced no visible change.** Two real, independently-confirmed causes:
1. **Missing input.** Sulphur (1 of 3 inputs to early_munitions) has zero cottage source — no amount
   of building construction can move it.
2. **Magnitude.** `COTTAGEIND_pops_output` (`COTTAGEIND_svalues.txt:85-97`) scales the pop-strata term
   by `COTTAGEIND_scale = 0.0001` (Sobisonator's own 2025 rebalance) AND a further `multiply = 0.1`
   (Sobisonator's original 2024 code) — combined ×1e-5. Confirmed via `git show upstream/master:
   common/script_values/COTTAGEIND_svalues.txt`: byte-identical to upstream, both factors are
   genuinely Sobisonator's, not fork-introduced. **This code must NOT be altered or removed** — any
   fix must be additive (new fork-owned bonus/building), never touch this formula.

**Wiring itself is confirmed LIVE, not broken:**
- `COTTAGEIND_produce_all` is called every quarter (`oa_wealth_changes.txt:176`), inside
  `every_country{every_governorships{...}}`, correctly ordered AFTER `GOODS_governorship_produce_all`
  (raw-good production) in the same pass — no staleness issue.
- Real boot log (`~/Downloads/logs.zip`, debug.log) confirms `cottage_produced<good>$ = REAL` (nonzero
  classification) for manufactured goods including construction_materials — the mechanism does
  compute a real, nonzero number.
- The `error.log` "Variable 'COTTAGEIND_produced_<X>' is used but is never set" flood (52 hits) is
  confirmed NOISE, not a bug: it fires uniformly for RAW goods (tin/copper/iron/gold/silver/dye/lead/
  sulphur/saltpetre/stone) that have no "produced" variant by design (cottage produces MANUFACTURED
  goods FROM raw inputs; raw goods themselves are never a cottage OUTPUT) — matches the standing
  `imp19c-econ-log-noise-not-bugs` pattern, not specific to military goods or to this playthrough.

**Round 1 adversarial review: PARTIALLY-CONFIRMED. Corrections applied:**
1. **The magnitude claim was mischaracterized.** `COTTAGEIND_pops_output`'s `0.0001 × 0.1` scales
   `governorship_middle_strata`/`governorship_lower_strata` — RAW SUMMED POPULATION COUNTS
   (`ECON_svalues.txt:62-84`), not a flat crush to near-zero. Cottage output is
   POPULATION-SCALED, not literally negligible; building count enters only weakly, through the
   raw-good sum, not through this term.
2. **"Whales" is a dead good.** `whales` is DEFUNCT, remapped to `fish` at boot
   (`common/trade_goods/00_imp19c.txt:227`) — `GOODS_governorship_whales_produced` is ~0
   empire-wide. Pharmaceuticals' cottage recipe effectively runs on vegetables ALONE. A whales
   cottage building would be pointless; retracted from the gap list.
3. **THE REAL, PREVIOUSLY-MISSED PRIMARY MECHANISM:** the Military Supplies TOPBAR number
   (`MILITARY_supplies_country`, `ingame_topbar.gui:820-822`) is a DEMAND-FULFILMENT BALANCE, not
   a production total — `Σ DEMAND_<good> × (1 − shortage_<good>)` (`INCOME_svalues.txt:1129`),
   capped at 1. Cottage's stockpile write reaches this number ONLY by reducing `shortage_<good>`
   in `CONSUME_from_stockpile` — never via a direct production read. Given the user's own report
   that demand is genuinely UNMET (a real, live shortage — confirmed, not the #98 "demand already
   met" scenario), this formula SHOULD be responsive to added production; the question is whether
   cottage's real (population-scaled) contribution is large enough, and fast enough, to move
   `shortage_<good>` down given a documented ONE-QUARTER LAG (`MILITARY_update_supplies` reads the
   PRIOR quarter's consumption-set shortage, `oa_wealth_changes.txt:208` vs `:344`).
4. **`early_artillery` is FULLY EXCLUDED from the topbar income-side calc** (`INCOME_svalues.txt:
   1035/1129` never reference it) — cottage's artillery contribution can NEVER move the headline
   number, structurally, regardless of shortage state or magnitude. If the user was specifically
   watching artillery, this alone explains "no change," independent of everything else.
5. Sulphur gap (early_munitions' 3rd input) and the error.log flood classification stand, with one
   correction: the flood's "never set" list is every good with NO cottage recipe (raw goods AND
   factory-only manufactured goods like late_munitions/late_artillery), not exclusively raw goods —
   still confirmed harmless (the 5 produce-able goods classify `REAL`, never appear in the flood).

**User confirmed: the number being watched is the TOPBAR HEADLINE** (`MILITARY_supplies_country`,
the demand-fulfilment balance, NOT the tooltip's uncapped "Produced by good" line). This settles
which mechanism matters: the `Σ DEMAND_<good> × (1 − shortage_<good>)` formula, given a REAL,
live shortage (user-confirmed demand is genuinely unmet). Checked the existing boot log
(`~/Downloads/logs.zip`) for real `shortage_<good>` / `MILITARY_supplies_country` numbers — NONE
exist; this was never instrumented. No real numbers are available without new logging (not a new
dedicated test — the same normal-boot-instrumentation pattern already used for the #102 tariffs
fix).

**Diagnosis, final for this round:** two independently real, additive-fixable factors, honestly
scoped:
1. Sulphur (1 of 3 early_munitions inputs) has zero cottage source — closing this gap is purely
   additive (new province-gated building, decision made: gate to Beitou/Datun, Taiwan, matching
   the `qing_timber_lineage_building`/`qing_cottage_sugarhouse_building` province-ID pattern, NOT
   a generic `trade_goods=sulphur` condition, since sulphur extraction was geographically
   concentrated, not a diffuse peasant craft).
2. `early_artillery` is structurally excluded from the topbar formula entirely — if any of the
   user's 20 buildings fed artillery specifically, that contribution could never show up here
   regardless of anything else. Separate from cottage industry's own wiring; worth flagging to the
   user as a distinct, real gap in the topbar formula's own coverage (not proposing a fix for it
   under this task unless asked — it's a pre-existing formula gap, not obviously cottage-specific).
3. Cottage's real (population-scaled) contribution to `shortage_<good>` reduction is UNMEASURED —
   no boot-log evidence exists either way. Proceeding to design an ADDITIVE fork-owned boost
   (not touching Sobisonator's `COTTAGEIND_scale`/`pops_output`) PLUS comprehensive logging of the
   real shortage/production numbers, so the next normal boot settles the remaining magnitude
   question without a dedicated test.

**Status: diagnosis passed round 1 review (PARTIALLY-CONFIRMED, corrections applied above).
Moving to DESIGN.**

## Boot-test confirmations #100 / #104 — no new work, logged for completeness
#100 (amban/garrison fix, #77/#78) and #104 (#69 inflation fix) were both re-confirmed working via
direct screenshot review during this session's earlier /imp19c-logs triage (see
`~/Downloads/scratch_logs_screenshots.md` for the shot-by-shot evidence) — no code change was needed
or made tonight. Marked completed in the task tracker on that basis; noted here so the doc's task
list matches the tracker's.

## #103-follow-up implementation (2026-08-16) — Parts 2/3 shipped

**Key correction found before implementing Part 2:** re-reading `se_COTTAGEIND.txt` in full
(`COTTAGEIND_cache_all_values:39-181`) found the earlier diagnosis's "cottage isn't wired to
military goods" framing was itself wrong. `COTTAGEIND_raw_stone/lead/sulphur/textile_fibres/
silk/vegetables/wood/iron/copper/tin` already read `GOODS_governorship_<good>_produced`, which
sums the engine's own `num_goods_produced` per province — the SAME stat a cottage building's
`base_resources` raises (the identical mechanic `qing_production_buildings.txt`'s modern works
use). So a cottage quarry/leadworks/weaving_hut/etc. ALREADY raises `COTTAGEIND_raw_<good>`,
which ALREADY reaches `early_munitions_stockpile`/`clothing_stockpile`/etc. via the existing,
Sobisonator-original `COTTAGEIND_produce_<good>` → `COTTAGEIND_scale_production` chain — this
pipeline is real and not broken. The actual reason ~20 buildings read as "no effect" is
MAGNITUDE: that chain multiplies by `COTTAGEIND_pops_output` (already ×0.1'd, per the standing
"don't touch it" rule) then ×0.5 efficiency then ×`TECH_cottage_industry_overall_bonus` again —
compounding discounts small enough to be invisible on the topbar at real building counts. This
reframes Part 2 from "wire up a disconnected mechanism" to "supplement a correctly-wired but
too-weak one," same spirit as the #102 tariffs pragmatic cut.

**Part 2 shipped**: new effect `COTTAGEIND_military_goods_building_bonus` (`se_COTTAGEIND.txt`,
new function, end of file) — a DIRECT, undiscounted, has_variable-guarded `change_variable add`
onto `early_munitions_stockpile` (quarry+leadworks+sulphur-pit buildings) / `clothing_stockpile`
(weaving_hut+silk_reeling_shed) / `pharmaceuticals_stockpile` (herbalist) /
`construction_materials_stockpile` (woodlot+quarry+smithy), counted via
`every_governorship_state{every_state_province{add=num_of_<building>_building}}` (the same
counting idiom `GOODS_governorship_munitions_infra_output_compute` already uses for
arsenal/depot). Wired at `oa_wealth_changes.txt`, right after `COTTAGEIND_produce_all = yes`.

**Rate: 0.2 per building — user directive to derive it from Modern Industry building output
numbers, discounted for cottage's lower productivity, not a fresh guess.** New constant
`GOODS_cottage_military_goods_output = 0.2` (`GOODS_svalues.txt`) = the average of the 4 directly
analogous modern per-building flat-add rates already in the repo (`GOODS_arsenal_munitions_
output=2`, `GOODS_depot_munitions_output=1`, `GOODS_machine_works_munitions_output=3`,
`GOODS_textile_mill_clothing_output=2`, avg≈2) × this codebase's own already-established
cottage-vs-formal discount ratio (`COTTAGEIND_pops_output`'s ×0.1, untouched) = 2×0.1 = 0.2.
Pharmaceuticals/construction_materials have no individual modern flat-building analog, so they
take the same derived rate rather than a second, ungrounded guess.

**Part 3 shipped**: new effect `ECON_LOG_curx_cottage_military` (`se_ECON_LOG.txt`, reuses the
exact #102 `every_governorships`+`save_scope_as`+`owner.change_variable` idiom) logs
`shortage_<good>`/`COTTAGEIND_produced_<good>` (all 4 mapped goods, governorship-scoped, summed
nationally) plus `MILITARY_supplies_income_country`/`MILITARY_supplies_balance_country` as the
PRIMARY headline metrics (the real per-quarter inflow/balance, matching the topbar formula) and
`MILITARY_supplies_country` (the floored stock) as a secondary/diagnostic metric — per round-2
design review's correction that the stock alone can't distinguish "production didn't rise" from
"production rose but the floored display can't show it." Wired at `oa_wealth_changes.txt`, in the
country-scope tail right after the governorship-scoped consume pass closes.

Design doc (`design/DESIGN_103_FOLLOWUP_COTTAGE_MILITARY_BOOST.md`) updated in place with the
final magnitude derivation and the pipeline-not-broken correction. Next: dispatch an
implementation-review pass on both parts, per the standing implement→review cycle.

## New tasks queued mid-session (2026-08-16): Qing event/mechanic pacing
User flagged, in quick succession: (1) Qing subject integration proceeds far too fast — should
take decades, matching history; (2) subject-integration events should fire far less often, ~once
every few years; (3) caravan trade events likewise should fire only every few years; (4) Canton
trade events too — user reports NEVER seeing one fire (possibly a real non-firing bug, not just
wrong cadence — flagged for diagnosis-first, not an assumed cadence tweak); (5) salt monopoly
events, same ~once-every-few-years ask. Queued as tasks #10-#14. Diagnosis starts next: find each
mechanic's actual current timer/MTTH/on_action interval before touching anything.

## #103-follow-up Parts 2/3 — review-fix round (2026-08-16)
Implementation review found 1 MEDIUM + 1 LOW, both fixed:
- MEDIUM: `ECON_LOG_curx_cottage_military` call site (`oa_wealth_changes.txt`) had no `tag = CHI`
  guard, unlike the #102 probe it copies — it ran once per country per quarter (~200x), corrupting
  the CHI read-back (all countries' ticks interleaved) and flooding -debug_mode logs. Fixed: wrapped
  the call in `if = { limit = { tag = CHI } }`.
- LOW: the 4 summed shortage_<good> metrics used tickscale=1000 (right for a single governorship's
  0..1 fraction) but the probe SUMS across all of CHI's governorships first, so >8 concurrently-short
  governorships pegs the 8000-tick cap. Rescaled to 500.
Both pure additions/parameter tweaks, no Sobisonator line touched, no new files.

## Qing pacing overhaul — implemented (2026-08-16)
design/DESIGN_QING_PACING_OVERHAUL.md passed 3 review rounds (round 1 found the original section 2
diagnosis wrong + section 6's rotation scheme broken, both redesigned; round 2 found a placement-
precedent gap + an honest-disclosure gap, both fixed; round 3 confirmed clean bar one label typo).
Implemented:
1. `se_QING_FRONTIER.txt` (QING_fgar_apply_occupation): occupation cooldown 180->1825 days, and
   the integration advance is no longer unconditional -- wrapped in a 60% chance roll. Together,
   full absorption of a garrisoned subject via this path now takes decades (expected ~40+ years),
   not ~2.5 years.
2. `se_SUBJECT_QING.txt` (SUBJ_QING_integration_pulse): the per-subject ambient-reaction roll now
   also checks/claims the shared qing_gc_event_slot_used slot, so multiple actively-integrating
   subjects can no longer all fire in the same pulse -- fixes the real complaint (multi-subject
   stacking), not the originally-misdiagnosed "monthly spam" (the pulse was already ~twice/year).
3. `se_QING_DECLINE.txt` (QING_frontier_flavour_roll): chance 30->15 -- this was the single largest
   structural reason the same few court events dominated the shared slot every quarter.
4. `se_QING_GOVERNANCE.txt` (QING_GOV_pulse): Revenue and Canton pulses moved to the front of the
   pulse's internal chain (were checked after ~10-15 other shared-slot claimants). Directly targets
   the user's "Canton events never fire" report. Honestly scoped: does NOT deliver true uniform
   randomness across all 49 existing slot-claim sites (rejected as disproportionate) -- expect
   Canton/Revenue to visibly improve; the broader "same few events" complaint may persist in a
   milder form (GOV_pulse chain as a whole still checked before frontier/dynasty/faction/spouse/
   officer).
Also resolved via user confirmation: salt monopoly's existing ~2-year one-time-reform cadence is
fine as-is (no code change). Caravan's recurring event already correctly throttled (no bug).
Canton's silver-reserve contribution already unconditional every quarter (no gap).
Implementation review dispatched; all 4 files brace-balanced.

## Art Patronage / Court Painter events (task #15) — Event 1 implemented; Event 2 blocked on a
## real, separate finding (task #19)
Round-1 review of design/DESIGN_ARTPATRONAGE_PAINTER_EVENTS.md surfaced something bigger than this
task: `00_specific_from_code.txt` and `qing_mechanics_on_actions.txt` each independently define a
BARE inline `on_character_death` block (192 vs 65 lines of real logic: QING_post_release/betrothal
dissolution vs aqsaqal-teardown/succession-contest) AND a bare `on_ruler_change` block (67 vs 23
lines). Two comments inside the SAME file directly contradict each other on whether bare on_action
blocks merge across files for RECURRING on_actions (as opposed to the one-time on_game_initialized
hook, which a #254 comment specifically documents as NOT merging). If they don't merge here either,
one half of each pair is silently dead code today -- independent of anything this session touched.
Dispatched a dedicated research pass (oracle repos / vanilla precedent / Paradox docs) to resolve
which claim is right; tracked as task #19. The FIX (convert both pairs to the proven list-
registration form, `army_effects_on_actions.txt`'s own precedent) is correct regardless of which
way the ambiguity resolves, so it doesn't have to wait on the research to be designed -- just to be
implemented with full confidence of the "why."
Event 1 (ambient "atelier presents a finished work" beat, no on_action dependency) implemented
now: new block in `QING_wenzhi_pulse` (rescans `qing_court_artist_count` at the roll site so a
stale button-only-maintained count can't wrongly gate it open after a natural death), new event
file `qing_wenzhi_painter_events.txt` (`qing_wenzhi_painter.1`), 4 new loc keys. Shared-slot +
1095-day department cooldown, matching the established pacing convention. Implementation review
dispatched.

## Art Patronage Event 2 implemented (2026-08-16)
Task #19's research resolved cleanly: recurring on_actions (on_ruler_change, on_character_death)
DO merge bare inline blocks across files -- confirmed via oracle-repo existence proof (Terra
Indomita defines on_ruler_change bare-inline in two separate files, both load-bearing, in an
actively-played mod). The #254 comment in qing_mechanics_on_actions.txt is correctly scoped to
on_game_initialized only, not a general rule. No bug; task #19 closed with no code change.
Event 2 (a court painter's death) implemented as originally designed: one new line in
qing_mechanics_on_actions.txt's existing on_character_death block (QING_wenzhi_painter_death_check
= yes), new effect in se_QING_WENZHI.txt (has_variable/employer-guarded, saves a permanent scope
to the dying character, claims the shared court slot, triggers qing_wenzhi_painter.2 with a 3-8
day delay), new event qing_wenzhi_painter.2 (desc branches via triggered_desc -- a unique text if
the dead painter is Castiglione by character-identity match against qing_castiglione_char, generic
otherwise), 5 new loc keys. Implementation review dispatched.

## Art Patronage review-fix round (2026-08-16)
Event 1 implementation review: CLEAN, zero defects. One accepted low-impact trade-off (count
rescan now runs every quarter unconditionally, not just on button click).
Event 2 implementation review found 1 MEDIUM + 2 LOW, all fixed:
- MEDIUM: the 3-8 day delay on trigger_event reading a permanently-saved scope to an already-dead
  character was unproven in this codebase (the cited precedent, betroth_dead_partner, actually uses
  save_temporary_scope_as and is consumed same-tick, not a real match). Fixed: removed the delay
  entirely, matching the one genuine precedent (vanilla 00_ambitions.txt:1085/1124, no days param).
- LOW: neither painter event had is_ai=no despite the module being documented player-only. Fixed:
  added to both.
- LOW (accepted, not fixed): Event 1's own 5-20 day delay has the same class of staleness risk at
  much lower odds (would need the sole painter to die in that exact window) -- left as documented
  residual risk per the reviewer's own "very low impact" read.
Also implemented task #18 (Justice strip-for-trial subpost gap) -- one-line addition mirroring the
Censorate fix, calling the same proven QING_post_dispatch_vacate dispatcher. Implementation review
dispatched.

## Pacing implementation review-fix + Censorate widened fix implemented (2026-08-16)
Pacing implementation review found 1 MEDIUM (real regression): the qing_frontier_garrisoned flag
(drives the Lifan Yuan panel's "Under imperial garrison" indicator) had its TTL still at 200 days
while the cooldown that refreshes it moved to 1825 days -- would have gone dark ~89% of every
cycle. Fixed: TTL bumped to 1900 days. Confirmed brace-balanced.
Round 7 (widened Censorate title-strip fix design) confirmed correct and safe, 2 non-blocking notes
(Amban/March-GG/Xinjiang-Beg formally unreachable by any strip mechanism, currently inert since
both disgrace pickers already gate on employer=ROOT; a bonus fix for GC-office holders' stale
qing_current_post, previously unnoticed). Implemented in se_QING_CENSORATE.txt: the old single
censor-inspector-only strip line replaced with remove_command + remove_as_governor +
QING_post_dispatch_vacate (a strict superset covering all 11 qing_current_post families).
Implementation review dispatched.

## Widened Censorate title-strip fix — CONFIRMED CLEAN (2026-08-16)
Implementation review: clean, all 6 checks pass (brace balance, sole-change diff, scope, strict
superset for the censor-inspector case, no double-strip for GC-office holders, proven guarded
idioms). One non-blocking note logged: the no-regression argument rests on the pre-existing #118
invariant that marker-set always pairs with post-stamp -- true at every current call site, not
introduced by this fix. This closes the last open item blocking roles 7-9 implementation.
Moving to implement roles 7-9 (zongli diplomat, censor-inspector, imperial guardsman) wage grants
themselves, per the confirmed design.

## GC sub-position salaries roles 7-9 implemented (2026-08-16)
After 7 rounds of design review (all confirmed sound), implemented the full rollout: 3 new
modifiers (qing_zongli_diplomat_office 0.02, qing_censor_inspector_office 0.01,
qing_imperial_guardsman_office 0.01, qing_governance_modifiers.txt). Param-threaded a new
$wage_modifier$ through all three shared SUBPOSTS functions (fill_one_minted grants it;
staff_corps_minted and strip_double_booked each strip it in their disqualify branches) across all
15 invocation lines (6 internal pass-through + 6 external callers in seed_gamestart/refill_sweep +
3 strip_double_booked callers). Added the 6 hardcoded player-appoint grant sites (3 in the shared
row-click picker, 3 in the dedicated panel appoint verbs) and the 3 dedicated Recall/Discharge
lever strips, the 3 se_QING_POST.txt vacate-function strips, and zongli's se_QING_MINISTRY.txt
recompute strip (its effective primary strip site). All 8 touched files brace-balanced.
Implementation review dispatched -- this closes out task #5 (GC sub-position salaries) pending
that review's result.

## Task #5 (GC sub-position salaries, all 9 roles) — CLOSED, confirmed clean
Implementation review of roles 7-9 found zero issues -- faithful to the design across all 9 touched
files (3 grant paths + strip paths per role, correct asymmetry between zongli's self-stripping
ministry recompute vs censor/guard's exclude-only recompute, Censorate-impeachment end-to-end
coverage confirmed). Every Qing character-appointment post (amban, salt/caravan/hoppo/opium
commissioners, customs IG, zongli diplomat, censor-inspector, imperial guardsman) now draws a
salary, matching the Grand Council seats' own existing convention.
