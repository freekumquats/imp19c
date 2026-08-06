# OVERNIGHT 2026-08-05 — autonomous run

Branch: `merge-overnight`. Mandate: implement all open tasks autonomously, no deferring;
log every decision here; code-review adversarially BEFORE each commit.

Task board at start (pending): #32, #33, #34, #35, #36, #37, #39, plus new #40, #41.

---

## #40 — Verify all QING_seed_* province + trade-good mappings resolve on the 1763 map — DONE

**Why:** memory `imp19c-288-buildings-correction` flagged that `se_QING_BUILDINGS.txt`
seeds were authored against 1815-on-develop and their seed provinces + good-mappings
needed confirming on the 1763 map (post #284 pop/trade-good changes). A stale mapping =
a specialty building silently never seeds (all four seed macros fail silently+logged).

**Method:** wrote a Python cross-referencer. Extracted province→owner from every
`own_control_core` block in `setup/main/00_default.txt` and province→`trade_goods` from
all `setup/provinces/*.txt`, then checked each of the ~90 seed calls: province exists +
correct ownership (CHI-only for seed/works/port; CHI-or-subject for frontier) + (for
`QING_seed_building`) the required trade good G.

**Parser trap caught (verified against raw bytes, per AAA rule 7):** first pass reported
40 "problems" all clustering on tags MZH/SHG/YNG. Those are **commented-out** viceroyalty
blocks (`#MZH = { ... }`) whose *uncommented* province-ID lists fold directly into CHI's
`own_control_core`. My parser matched the dead `#TAG = {` headers. Re-ran with comment-
stripping → **3 real problems**, each then confirmed against raw setup:

1. **Foshan/Shiwan 石灣 kiln (P9301, `qing_porcelain_kiln_building`, G=porcelain)** — 1763
   models Foshan as `trade_goods="iron"` (its real Guangdong iron-casting industry; also a
   #63 holy site). G=porcelain guard silently failed → dead seed. No other Guangdong
   province is porcelain; the good is #234 pop-derived (not to be overridden). **Fix:**
   RETIRED the seed (Dehua 德化 Fujian + Jingdezhen 景德鎮 Jiangxi both resolve to porcelain
   correctly and remain the porcelain-kiln seeds).
2. **Turpan 吐魯番 karez (P9597, `qing_karez_building`)** — owned by ILI (the Xinjiang
   autonomous_governorship subject), not CHI directly → CHI-only `QING_seed_works_building`
   silently skipped. **Fix:** switched to the subject-tolerant `QING_seed_frontier_building`
   (building potential `is_in_region=Turkestan` already admits it).
3. **Kashgar 喀什 Id Kah Mosque (P2700, `qing_great_mosque_building`)** — owned by XNG,
   which is a subject of ILI, which is a subject of CHI (NESTED sub-subject). `is_subject_of`
   is NOT recursive (`imp19c-is-subject-of-not-recursive`), so even the frontier macro's
   `owner={is_subject_of=c:CHI}` branch failed. **Fix:** added a THIRD guard branch to
   `QING_seed_frontier_building` — `owner = { overlord = { is_subject_of = c:CHI } }` —
   admitting a province whose owner's DIRECT overlord is a CHI subject (XNG→ILI→CHI). This
   mirrors the single-level `overlord` branch the affected buildings already carry in their
   own `potential` (qing_great_mosque_building). One nesting level suffices for 1763.

**Post-fix:** re-ran the verifier with the corrected guard logic → **0 remaining problems**.
Braces balanced (212/212).

**Files:** `common/scripted_effects/se_QING_BUILDINGS.txt` only.

**Review:** code-review found ONE real defect (MEDIUM/HIGH): the new 3rd guard branch did an
`overlord = {}` scope-switch WITHOUT the `exists = overlord` guard — CHI itself hits this macro
(Liangzhou/Chahar/Xining) and has no overlord, which would re-trigger the 41,005-line overlord
flood that commit 7b88e9962 fixed mod-wide. FIXED: guarded with `exists = overlord` (matching
qing_great_mosque_building:257 and the 7-site convention). Re-verified 0 problems, braces 213/213.

**Status:** DONE — committed `6061c7f28`.

---

## #41 — Add ungranted modern-industry buildings as Self-Strengthening mission rewards — DONE

**Why:** three modern `qing_*` industrial buildings had NO `add_building_level` grant anywhere
(not seeded, not mission-granted) — reachable only via the invention-gated player build menu,
which may never open. User: add them as mission rewards; add new missions if necessary.

**Investigation (corrected the candidate list first, per the flag I raised):**
- Caught a false-grep: my initial "ungranted" scan matched only literal `add_building_level`,
  MISSING the `QING_selfstr_build = { building = X }` indirection. Re-ran catching all grant
  idioms. Results:
  - `qing_tongwen_guan_building` — **already granted** via `QING_selfstr_found_tongwen`
    (se_QING_SELFSTR.txt). EXCLUDED.
  - `qing_cotton_workshop_building` — a SEEDED specialty building (se_QING_BUILDINGS.txt:48).
    EXCLUDED (not modern-industry; user's original list conflated it).
  - `qing_n_poppy_farm_building` — buildable-from-start (poppy long cultivated), not gated.
    EXCLUDED.
- TRUE ungranted modern-industry set = **3**: `qing_steel_works_building` (漢陽鐵廠),
  `qing_coal_mine_building` (開平礦務局), `qing_textile_mill_building` (機器織布局).

**No new missions needed** — the Self-Strengthening tree ALREADY has three tasks named exactly
for these buildings (`qing_ss_hanyang`, `qing_ss_kaiping`, `qing_ss_cotton_mill`), but they only
granted `add_popularity` (+`add_stability` on cotton). They were stubs. Wired each to build its
eponymous building.

**Placement care:** steel/coal carry `base_resources = 2` (a MULTIPLIER on the province's
iron/coal output), so placing them on the most-populous province (what the existing
`QING_selfstr_build` helper does) would raise them where they yield nothing. None of the 3
buildings has a `potential` block, so `add_building_level` lands anywhere. Added a new helper
`QING_selfstr_build_on_good = { B = <building> GOOD = <good> }` (se_QING_SELFSTR.txt) that PREFERS
an owned province of the target good lacking the building (idempotent), and ONLY if none exists
falls back to the most-populous province — so the reward is never silently lost. Verified 1763
CHI owns iron provinces (5) and coal provinces (6). Each task also now calls
`QING_selfstr_advance = { amount = 8 }` (matching the other founding tasks, which all advance the
0..100 selfstr meter — the three stubs previously did not).

Wiring: hanyang→steel_works/iron, kaiping→coal_mine/coal, cotton_mill→textile_mill/textile_fibres.

**Files:** `common/scripted_effects/se_QING_SELFSTR.txt` (new helper),
`common/missions/qing_selfstrengthening_missions.txt` (3 task on_completions).

**Review:** code-review raised 3 findings.
- Finding #1 (MEDIUM, PLAUSIBLE): claimed the helper bets `add_building_level` bypasses the
  `allow` gate, contradicting memory `imp19c-add-building-level-respects-potential`, so the
  buildings would silently drop on rural resource provinces. **REFUTED after verification:** that
  memory VERIFIES `potential` is enforced, not `allow`; the review conflated the two — the exact
  error the memory itself flags a prior agent made. The 3 buildings have NO `potential` block. The
  decisive precedent: `qing_machine_works_building` has the IDENTICAL gate class (no potential;
  allow with has_city_status + civilization_value>=35 + sufficient_job_slots + industry-capacity +
  invention) and has shipped since #234 placed via add_building_level on capital_scope (reform
  mission) and most-populous (QING_selfstr_build) with ZERO gate replication. If `allow` were
  enforced on force-add, that flagship reward would silently fail — it doesn't. So the mechanism
  the comment describes is correct. No change.
- Finding #2 (LOW, design, ACCEPTED): good-targeting buys nothing for the textile mill (no
  base_resources, no trade-good gate) and could steer it to a smaller fibres settlement. FIXED:
  textile mill now uses plain `QING_selfstr_build` (most-populous, where the proletariat lives);
  good-targeting retained only for steel (iron) and coal (coal) where base_resources=2 bites.
- Finding #3 (LOW, convention, ACCEPTED): new LOG strings embedded `$B$`/`$GOOD$` macro params
  (log-string-macro rule). FIXED: both LOG_line strings made static.

Brace balance OK both files after fixes.

**Status:** DONE — committed (see git log).

---

## #39 — Protectors-General: Lifan Yuan roster section + event arc — IMPLEMENTED

Design doc `design/DESIGN_PROTECTORS_GENERAL_EVENTS.md` (READY, reviewed) implemented in the
build order it prescribed. The 都護府 marches = subject countries with qing_march=1; the GG is
the march's current_ruler (a Lifan appointee, set_as_ruler by QING_march_appoint_gg). Modelled
on the amban arc.

**PART A — roster (Lifan Yuan panel):**
- `se_QING_MINISTRY.txt` QING_ministry_recompute_perf_lifanyuan: rebuild
  `qing_lifanyuan_march_subjects` each Lifan pulse (every_subject over qing_march — non-recursive,
  same as the amban roster). Also added perf **term (h)**: fold `qing_lifan_recent_march_outcome`
  at HALF weight (divide by 2) — separate var from the amban term (g), no cross-contamination,
  no over-swing (review #4).
- `gui/qing_lifanyuan.gui`: new Protectors-General section between the amban roster and the
  tributary section. GG portrait via `Country.GetRuler` (proven datacontext — the GG IS the ruler,
  so no per-GG var, unlike the amban); PartyIcons chip suppressed (#86); empty-note.
- loc: `QING_LIFANYUAN_PG_TITLE` / `_EMPTY`.

**PART B — evaluate pulse + fold helper (se_QING_MARCH.txt):**
- `QING_march_evaluate`: called from QING_GOV_pulse right after QING_amban_evaluate. CHI player-only.
  Iterates marches, re-scores each GG's affinity (QING_char_affinity), rolls ~10% per quarter for
  AT MOST ONE mutually-exclusive event by priority (turnover .5 > overmighty .4 > unrest .2 >
  petition .1 > commend .3), sharing the court-event slot (qing_gc_event_slot_used).
  - SCOPE-LIFETIME care: the per-iteration scopes (qing_march_here/gg_here) would be overwritten
    by later iterations before a DEFERRED event (days 5-15) fires. Each fire branch re-saves
    DEDICATED event scopes (qing_march_evt_march/qing_march_evt_gg) at the moment of firing; only
    one branch fires per pulse (slot claim), and every event re-validates the scopes in its trigger.
  - Petition gate simplified to the subsidy-tier signal only (a var-vs-var cohort compare would
    break the RHS-operator rule; the invented svalue didn't exist).
- `QING_march_appoint_gg`: added a self-expiring tenure timer (qing_march_gg_tenure_pending, 2920d)
  mirroring the amban's, so the overmighty (.4) event can gate on "served long enough".
- `QING_march_recent_gg_outcome = { delta }`: clone of SUBJ_QING_lifan_amban_outcome; stamps the
  self-expiring 730d var (no ratchet).

**PART C — events (`events/imp19c_mod_events/qing_march_events.txt`, namespace qing_march) + loc:**
5 events (.1 petition, .2 unrest, .3 able, .4 overmighty, .5 turnover), each with a defensive
`trigger` re-validating the saved scopes (march still a subject + GG alive), CHI-only. Petition
grant has a light skill-gate (finesse>=6 → cheaper grant, a cost modifier not a roll); unrest .2.a
is a martial+zeal skill check (qing_garrison_clean_crush_chance_svalue from #27); .4/.5 reappoint via
QING_march_appoint_gg. Denials stamp a NEW stacking/decaying `qing_march_neglected_opinion`
(imp19c_opinions.txt) — the design's denial teeth (mod expresses subject disaffection via opinions,
not a raw liberty_desire poke, which is unused mod-wide). Every outcome folds via
QING_march_recent_gg_outcome. New loc file (UTF-8 BOM per loc convention).

**Self-check:** all touched files brace-balanced; pictures/verbs (add_gold/add_loyalty/
loyalty_qing_congenial/QING_char_promote_standing) all proven in the amban arc; Country.GetRuler
datacontext proven (the review's earlier "unproven" NO-GO was refuted in the design doc).

**Files:** se_QING_MINISTRY.txt, se_QING_MARCH.txt, se_QING_GOVERNANCE.txt, gui/qing_lifanyuan.gui,
localization/english/qing_lifanyuan_l_english.yml, common/opinions/imp19c_opinions.txt,
events/imp19c_mod_events/qing_march_events.txt (new), localization/english/qing_march_l_english.yml (new).

**Review:** code-review returned CLEAN — no crash/flood/correctness-critical defect. It confirmed
the scope-lifetime handling is sound (only one branch fires per pulse via the slot claim; scopes
survive the deferred event; cross-pulse clobber impossible), the slot serialisation is correct
(amban evaluate claims the same var first, so amban > march priority), the perf scratch var is
re-inited per term (no clobber), and all verbs/pictures/loc are legal. Four LOW findings, all fixed:
- #1 (LOW-MED): event triggers re-validated only scope existence, not the firing condition — a
  situation could drift in the 5-15d defer window (unrest subsided, affinity recovered). FIXED:
  .2/.3/.4 triggers now re-assert their scoring condition (parity with the amban arc).
- #2 (LOW): a displaced GG kept a stale qing_march_gg=1 (no tenure timer) after reappoint — could
  re-qualify for .4/.5 if succession re-elevated him. FIXED: QING_march_appoint_gg now clears the
  outgoing ruler's qing_march_gg + tenure var before set_as_ruler.
- #3 (LOW, balance): .1.b (troops) strictly dominated .1.a (silver) — same tier bump, cheaper, plus
  a host rebuild. FIXED: silver grant made cheaper (−20/−35) and troops pricier (−55), so silver is
  the lighter recurring commitment and troops the heavier all-in.
- #4 (LOW, doc): comment said the slot "resets monthly"; it clears each ~90d Qing pulse. FIXED wording.
The earlier design-round "Country.GetRuler unproven" NO-GO was re-confirmed refuted.

Brace balance OK all files after fixes.

**Status:** DONE — committed (see git log). Design doc committed alongside.

---

## #33 — Buildings pass: fortress-format tooltip (complete Results) across every mod building — IMPLEMENTED

**Requirement (user):** every building follows the Fortress template — flavor desc, a description
of the modifiers it grants (visible whether buildable or not), count, cost/time, cost modifiers, and
a **Results:** section with all changed numbers + icons. "Results should list all appropriate
modifiers, Other Results only modifiers that cannot go in Results, FOR EVERY BUILDING." Plus the
Ever-Normal Granary complaint: "why two sections (Results + Other Results), just combine them."

**Mechanism (verified, not assumed):** the province building panel's "Results:" section renders the
building's `modification_display` list as icons. The FORTRESS — the user's cited gold standard —
lists EVERY modifier it grants (fort_level + value_manpower + local_defensive). Vanilla and the mod's
own IND_* buildings CURATE to 2-4 keys, so their other modifiers fall to "Other Results:" (or don't
show). #33's fix = expand every mod building's `modification_display` to enumerate ALL its engine-key
modifiers, matching the fortress. This also resolves the Ever-Normal Granary two-section complaint:
with all 6 modifiers now in Results, nothing is left for Other Results.

**What I did:**
- Wrote `tools/gen_building_modification_display.py`: for each mod-added building (qing_*, IND_heavy_*,
  row_*), rewrite `modification_display` to list every top-level modifier key (all standard engine
  keys — local_*, base_resources, army_movement_speed, fort_level — verified renderable via the
  fortress + IND_coal_mine base_resources precedent), in source order, excluding cost/time. Idempotent;
  brace-guarded; preserves BOM; SKIPS upstream/vanilla 00_* files (proven-code rule).
- Applied to **56 buildings** across 15 files. Re-run is a no-op (0 changes). All files brace-balanced.
- The DESCRIPTION side was already fully wired in a prior session — `tools/gen_building_tooltips.py`
  reports 0 uncovered build_items (every mod building points its build_item at a custom tooltipwidget
  that shows its `_desc` unconditionally, even when unbuildable).

**Deliberately NOT changed (scope discipline):**
- The 7 monument buildings with `allow = { always = no }` (Great Wall / Dujiangyan / Temple of Heaven /
  Hanlin / Guozijian / Ancestral Temple / Grand Canal): the #24 sweep INTENTIONALLY set that + a real
  satisfiable `potential` so add_building_level plants them (seed + Works verb) while they stay out of
  the routine build menu — documented in-file and matching memory
  `imp19c-add-building-level-respects-potential`. They are NOT hidden (visible + full tooltip where
  built); making them menu-buildable would be a design regression. Left as-is.
- The ~22 buildings with no `potential` block (industry/production): they are menu-gated by `allow`
  (culture-group + invention + resource), so they are correctly gated, NOT hidden. Adding a `potential`
  culture gate to restrict menu visibility to China would be a behavior change beyond #33's legibility
  scope AND risks the "too-tight potential hides it from China too" trap the memory warns about. Left as-is.

**Runtime caveat (stated honestly):** the "Results:" split is engine-rendered (MODIFICATION_DIFFERENCE_
HEADER, not scriptable GUI), so the exact on-screen result of the expanded modification_display — and
whether the `always=no` monuments render their Results when already built — cannot be proven statically.
The change is additive to an existing curated list and matches the fortress template that is known to
work, so the risk is low, but it wants a boot-check to confirm the panels render as intended.

**Files:** 15 common/buildings/*.txt (modification_display only) + tools/gen_building_modification_display.py (new).

**Review:** code-review returned CLEAN — no defects. Verified every added key was ALREADY a
top-level modifier in that building's body (the tool reads existing keys, never synthesises), no
dropped keys, no leaked nested/structural tokens (allow/potential inner keys stripped; a
`local_monthly_food` inside a comment correctly did NOT leak), all 15 files brace-balanced, no
duplicates, correct scope (no 00_* upstream touched, idempotent no-ops on already-complete blocks).
Minor tool-regex note (leading-dot decimals like `.05` would be missed) — confirmed non-applicable
(grepped: no such values in any touched file). No changes needed.

**Status:** DONE — committed (see git log).

---

## #34 — Surface the Military Supplies breakdown in the topbar tooltip — IMPLEMENTED

**Why:** the topbar Military-supplies figure is a black box — the old MILITARY_SUPPLIES_TT showed
only total income and total consumption ("gains X, consumes Y"). User wants the breakdown surfaced.

**What I did:** enriched MILITARY_SUPPLIES_TT (imp19c_tooltips_l_english.yml) with a per-good
"Consumption by good (quarterly)" section: munitions (early/late), artillery, clothing,
pharmaceuticals, construction materials.

**Correctness catch:** the obvious country-scope reads (DEMAND_country_clothing / _pharmaceuticals /
_construction_materials) sum CIVILIAN + military demand and would massively overstate military
consumption. Added SEVEN new country-scope MILITARY-only svalues in INCOME_svalues.txt that sum the
exact same `_base` military addends MILITARY_supplies_country_consumed_quarterly uses, so the
breakdown is internally consistent with the displayed total.

**Dangling-ref catch:** DEMAND_late_artillery_base is UNDEFINED upstream (the existing consumed-total
svalue references it too; DEMAND_late_artillery Total is stubbed value=0 — late artillery isn't
modelled yet), so it always contributes 0. Omitted the late-artillery line rather than propagate the
dangling reference / show a permanent 0.00; documented for when it's modelled.

**Files:** localization/english/imp19c_tooltips_l_english.yml, common/script_values/INCOME_svalues.txt.

**Review:** code-review CLEAN — all 8 tooltip ScriptValue refs resolve, new svalues read the correct
military-only `_base` addends (not civilian DEMAND_country_*), scope idiom proven, single valid YAML
line, braces balanced, no double-count. One LOW: the total-consumption line rendered NEGATIVE (the
canonical consumed svalue is ×-1) while the positive per-good breakdown summed to +X — a sign
mismatch made adjacent by this change. FIXED: added MILITARY_supplies_country_consumed_quarterly_magnitude
(same addends, positive) and used it in the "consumes X" clause so total + breakdown agree in sign.

**Status:** DONE — committed (see git log).

---

## #35 + #36 (+#32) — two new Reports-hub reports: Military Supplies ledger + Admin Capacity — IMPLEMENTED

Both are new tabs in the existing Reports hub (qing_reports_window, opened from the Central
Secretariat). #36 (Admin Capacity) directly satisfies #32 (surface the yamen→admin-capacity link):
its yamen-count column + per-yamen capacity tooltip makes the link legible, so #32 is folded in.

**#35 — Military Supplies Ledger:** scripted-gui `qing_report_open_milsupply` walks owned provinces
and lists those producing a military-supply good (early/late munitions, rifles, naval_supplies) into
qing_milsupply_report_provinces; the window shows province + good icon + actual output
(Custom('province_actual_goods_produced'), proven province_window.gui:1314), with a footer of the
realm's quarterly income / consumption / stockpile (same svalues as #34). Empty-state gate for a fresh
1763 start (no arsenals yet).

**#36 — Administrative Capacity:** scripted-gui `qing_report_open_admin` walks governorship-states,
snapshots each state's ADMIN_provided_state / ADMIN_required_state / available + yamen & district
counts onto the state (read back via Scope.GetState.MakeScope.GetVariable, proven), lists them in a
5-column table (state / provided / required / yamens / districts) with a per-state deficit gate
(qing_report_admin_state_deficit) and a footer of the country ADMIN_supplied/required/available totals.
The yamen column's tooltip states the 8-per-yamen / 10-per-district capacity — surfacing #32.

**Scope-correctness catch:** in the admin walk, accumulating per-province building counts onto the
state var required the right scope dance — inside every_state_province THIS=province, prev=state; saved
the province as scope:admin_rep_prov and added scope:admin_rep_prov.num_of_X onto scope:this_state's var
(scope:X.num_of_BUILDING proven se_MARRIAGE_PLAY.txt:179). Also simplified the "provided" cell from a
loc-indirection to an inline read (removed the now-unused loc key).

**Wiring:** two new buttons in the hub window (grown 320→420h), each Execute()s its opener + opens its
window; loc for buttons (qing_governance_l_english.yml) + windows (qing_province_reports_l_english.yml,
BOM preserved).

**Files:** common/scripted_guis/qing_province_reports.txt, gui/qing_province_reports.gui,
localization/english/qing_province_reports_l_english.yml, localization/english/qing_governance_l_english.yml.

**Status:** implemented; pending adversarial code-review before commit.

**Review (#35/#36):** code-review CLEAN on all 8 concern areas (scope-correctness of the yamen/district
accumulation confirmed, ADMIN svalues genuinely state-scope, list/datamodel scopes match, hub-button
order + window sizing correct, all datafunctions proven, braces balanced, BOM kept). 4 findings, all
resolved:
- #1 (MEDIUM): dangling tooltip key qing_report_open_admin_button. FIXED — added the loc.
- #2 (LOW-MED): dead deficit gate + unused `available` var. FIXED by WIRING them — added an "Avail."
  column (provided − required) colored #R red#! on deficit / #G green#! on surplus via the
  qing_report_admin_state_deficit gate; widened the window + row for the column + its header/tooltip loc.
- #3 (LOW): state snapshot vars persist without expiry — accepted (read-only snapshot, overwritten each
  open; same trade-off as the other reports).
- #4 (PLAUSIBLE, the important one): both walked every_governorships, which EXCLUDES the capital domain
  (boot #10 class). For the ADMIN report that's model-consistent (ADMIN totals are governorship-scoped)
  — left as-is. For the MILSUPPLY ledger it was a real gap: an arsenal/navy-yard seeded in the capital
  domain would produce yet never list. FIXED — switched the milsupply walk to every_owned_province (the
  same fix boot #10 applied to the migration report), so the producer list is complete; footer totals
  stay governorship-scoped (documented upstream-model limitation).

**Status:** DONE — committed (see git log).

---

## #37 — Gold/silver reserve price-when-untraded — BLOCKED ON RUNTIME PROOF (not changed)

**Status: intentionally NOT changed this run.** The reserve/price-setting system is complex and — per
memory `imp19c-vanilla-trade-request-flood-open` and the prior session's record — every previous
attempt to change it was ultimately dismissed as too risky. The standing decision (user-set) is: do
NOT change the reserve/price system without RUNTIME PROOF that the price is actually broken +
a user greenlight.

**Why no proof yet:** the read-only PRICE_PROBE (commit `7b4e31f22`, Aug 5 00:26) logs
global_base_import_price_gold/silver each quarter. The newest available log is Aug 4 22:00 — it
PREDATES the probe commit by ~2.5h, so it contains 0 PRICE_PROBE lines (confirmed: unzip -p ... |
grep -c PRICE_PROBE = 0, even though the log has 628k IMP19C lines, i.e. it DID boot -debug_mode).
There is simply no post-probe log to read.

**Verified this run:** the probe is still in place and well-formed (oa_wealth_changes.txt:494-511),
fires once per quarter right after the type-6 trade split, uses the proven ROOT-country-var staging
idiom (GetGlobalVariable is unresolvable in a debug_log; se_ECON_LOG.txt SYNTAX NOTE), and emits no
macro/# in the string. It will produce the diagnostic on the next -debug_mode boot.

**Next step (needs a boot, then user):** boot -debug_mode into 1763, play a few quarters, then read
debug.log for the PRICE_PROBE series. If gold/silver log as 0 → the reserve-sale income math is inert
(a real bug to fix); if nonzero but wildly swinging → the thin-stockpile volatility concern. EITHER
finding, plus a greenlight, unblocks the fix. Until then, changing the system blind would repeat the
exact over-eager mistake the standing constraint exists to prevent.

---

## RUN SUMMARY (2026-08-05)

Completed + committed + adversarially reviewed (in order): **#40** (3 stale 1763 seed mappings),
**#41** (3 modern buildings → selfstr tasks), **#39** (Protectors-General roster + 5-event arc),
**#33** (56-building modification_display / Results sweep), **#34** (military-supplies topbar
breakdown), **#35 + #36 + #32** (Military Supplies ledger + Admin Capacity reports, incl. the
yamen→capacity legibility). **#37** left blocked on a runtime boot (probe in place; do not change blind).

Every task was code-reviewed BEFORE commit (AAA rule 1); review findings were verified against the
repo before acting (two review "criticals" were REFUTED after verification — the overlord-guard one
was real and fixed, the allow-vs-potential one was a conflation). All commits authored by freekumquats.
Every commit brace-checked; loc BOM preserved.

---

# SESSION 2 (2026-08-05, after boot-test) — user reported multiple failures; reworking

User boot-tested and found #33/#34/#35/#36/#40/#30 did NOT work. Reopened them. New task
batch #42–#53. Working in order; every decision logged here; review before each commit.
Building rework (#42) to be done BY HAND per building — no generator scripts (user directive).

## #52 — PRICE_PROBE result (feeds #37) — DIAGNOSIS COMPLETE
Newest log (logs.zip Aug 5 14:58) post-dates the probe. Probe output:
`IMP19C PRICE_PROBE gold=ERROR:[...] silver=ERROR:[...]` — the read did not resolve.
ROOT CAUSE FOUND (grep, not guess): `global_base_import_price_gold` / `_silver` is READ in ~12
sites — CURRENCY_svalues.txt (reserve valuation, lines 21/27/32/37/624/640/1079-1093) and
se_INCOME.txt (reserve SELLING, lines 580/599/644/647/659/673) — but is **NEVER set_global_variable'd
anywhere in common/**. So the reserve-sale price global is permanently unset (reads 0/error).
This is the #37 bug: reserve-sale income math multiplies/divides by an unset global → inert.
Also corroborated by error.log: 47+47 "Failed to fetch variable for silver_needed_for_deficit /
gold_reserve_value_greater_than_silver due to not being set" (DEBT_events.txt:13 →
INCOME_mitigate_deficit:111 → INCOME_sell_largest_reserve:26/50 → INCOME_sell_reserves:8).
FIX (deferred to #37 proper): determine where the global SHOULD be set (likely from the per-zone
country_unit_price_* or the type-6 trade split that computes gold/silver prices) and set it there.
Careful fix — reserve system, burn history.

## #48 / #30 — Currency £→¥ — REAL FIX (icon, not text)
Root cause of #30's failure: the on-screen currency symbol is NOT the literal £/¥ text #30
swapped (that swap DID apply — 0 £ / 694 ¥ in mod text now). The symbol the player sees on
money VALUES is the `@gold!` texticon = the IMAGE gfx/interface/icons/font_icons/
font_icon_treasury.dds (font_icons.gui:113, used ~115×), plus the topbar's big
gfx/interface/icons/shared_icons/treasury.dds. Both were a £ glyph — verified by rendering
the DDS to PNG (25×25 and 50×50 BGRA8). #30 fixed a layer that isn't displayed.
FIX (user chose "replace the .dds icon"): redrew BOTH icons as a ¥ glyph (Arial Bold ¥,
sampled the £'s exact per-row gold gradient so shading matches), written back at the SAME
dimensions/format/byte-size reusing the ORIGINAL 128-byte DDS header (25×25→2628 bytes;
50×50→10128 bytes) so the engine loads them identically. Verified both re-render as ¥.
The #30 text swap (£→¥ in strings) is harmless and left in place (¥ prefixes in cost loc
strings are still correct). Other £-name hits (tech_treasury_bills, qing_con_currency,
tradegoods) are unrelated button/good art, not the currency glyph — left alone.

## #47 — Conservative-Bloc "C" chip in the Character window — FIXED (all characters, per user)
User directive refined mid-task: NOBODY should show the "C" chip in the Character window — not
just ambans. So instead of an amban-specific guard, the chip is flatly hidden across the whole
Character window:
- characters_view.gui:999 (roster card party chip) -> visible = no.
- characters_view.gui family-member portraits (cpt_button, gui_base PartyIcons block) ->
  blockoverride "PartyIcons" {} (the proven Lifan-Yuan suppression idiom).
- characterwindow.gui:110 (the character DETAIL window portrait chip) -> visible = no, so an
  amban (or anyone) opened from the roster no longer shows the bloc chip on his detail card either
  (the code-review of the earlier amban-only version flagged this detail-window site as missed).
REVERTED my earlier over-reach: the gui_base.gui shared-template change (4 party-chip lines) was
NOT what was asked (it affects many other windows) — reverted; only the two Character-window files
are touched. Braces balanced both.

## #46 — one man, one post (REDONE generically per user)
User feedback: my first #46 was a "special rule for a generic case" (pairwise NOT=has_variable
guards, amban↔upperstudy only, missing southern study). There was NO single shared "already holds
a post" trigger — the user: "then that is a mistake"; the 1:1-violation audit (se_QING_COUNCIL:240-248)
enumerated the full marker set but only LOGGED a clash — the user: "it should explicitly prevent".
REDONE:
- NEW canonical trigger QING_char_holds_court_position (qing_dynasty_triggers.txt) = OR of the exact
  1:1-audit marker set (office_held / zongli_diplomat / censor_inspector / imperial_guardsman /
  southernstudy / upperstudy / amban_marker / palace_eunuch / harem_consort). One place, enumerated once.
- Gated the THREE candidate draws on NOT={QING_char_holds_court_position=yes}, replacing the hand-rolled
  per-marker NOTs: amban draw (se_QING_AMBAN QING_amban_post, both any_/ordered_ filters), Upper Study
  draw (se_QING_UPPERSTUDY, both), Southern Study draw (se_QING_SOUTHERNSTUDY, both). So ANY post-holder
  is now explicitly PREVENTED from being drawn into a second post — covers every pair incl. both studies.
- Reverted my pairwise #46 guards. The 4 remaining office_held NOTs are roster-REBUILD filters (a tutor
  promoted to a great office leaves the corps) — a different, correct use, left as-is.
Braces balanced all 4 files.

## #43 — make yamen + all other new mod buildings VISIBLE in the build menu — DONE
Audit: 15 mod buildings had NO build_item_<X> type in gui_templates.gui, and 17 were not
instantiated in the province_window.gui build list (incl. the yamen — which is why the #42
yamen tooltip was invisible; visibility must precede the tooltip).
FIX (copied the Fortress/coal_mine build_item pattern exactly — a proven working template):
- Added 15 build_item_<X> types (gui_templates.gui), each pointing at its already-existing
  building_<X>_tooltip widget. (grand_canal + great_wall already had types.)
- Instantiated all 17 in the province build list under the right sections: yamen/dujiangyan/
  great_wall/grand_canal → PublicWorks; customs_house/embassy/foreign_works/treaty_port/
  mission_cathedral → Foreign; frontier_colony/frontier_fort → Garrison; hanlin/guozijian/
  shuyuan → Scholarship; temple_of_heaven/ancestral_temple → Religion; selfstr_wonder → Modern.
  Monuments/seed-only buildings with allow=always no render visible-but-not-buildable (the
  user's "no hidden buildings, effects described" intent), exactly as any gated building does.
Braces balanced (gui_templates 1740/1740, province_window 2094/2094).
