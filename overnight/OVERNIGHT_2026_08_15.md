# Overnight run — 2026-08-15

## ASSUMPTIONS & GUESSES
- None yet this session (this entry covers a diagnostic-instrumentation fix only, no new tuning
  constants introduced).

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
