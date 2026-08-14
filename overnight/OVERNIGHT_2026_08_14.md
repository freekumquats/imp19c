# Overnight run — 2026-08-14

## ASSUMPTIONS & GUESSES (best-guess values made without boot data — scan this section first)

- **`se_QING_SALT.txt` salt-income cap = 150.** Set just above the adversarial review's own
  calculated realistic ceiling (~46-138, from CHI's 8 salt provinces vs Canton's 42 tea+silk+
  porcelain provinces at the same per-province rate). No boot data confirms the exact right
  number — `LOG_line = "salt: national production base exceeded the 150 cap, clamped for"`
  fires if the cap is ever actually hit, which the next boot's debug.log will show.
- **`se_QING_DECLINE.txt` granary build cooldown = 1095 days (~3 years).** User asked for "once
  every few years"; 3 years is a plain reading of that, not derived from any in-game rate. No
  diagnostic log added specifically for this (the existing `LOG_line` on a successful build
  already shows the cadence on the next boot's timestamps).
- **Outliner building-icon fix is an unverified BOOT SPIKE, not a confirmed fix** — see task #73
  below. `OutlinerItem.GetBuilding` has no proven precedent anywhere (this repo, vanilla, or the
  Terra-Indomita oracle). It cannot regress below the current (already-broken) baseline if wrong.

## Task #67 — Fix amban/garrison subject-type check drift (integrating_governorship gap)
**What:** `QING_amban_warrants_resident_trigger` and `QING_fgar_scan` each kept their own
subject_type OR-set for amban/garrison eligibility; both were missing `integrating_governorship`
(the transient type a subject is rebound to during `SUBJ_QING_authorize_integration`), which is
why Urga silently lost its Replace-amban button and "Under imperial garrison" line mid-integration
despite remaining a direct CHI subject throughout.
**Decision:** consolidated both into one shared `QING_amban_garrison_eligible_type_trigger`
(`qing_dynasty_triggers.txt`) so the two systems can't drift apart again. Deliberately left the
two SEPARATE "integration-ladder-progression" gates (a narrower, intentionally different check)
unchanged — confirmed via review these are a different semantic, not a missed inconsistency.
**Review:** code-review CLEAN, no findings.
**Commit:** `0195b16b5`. **Status: DONE.**

## Task #69/#80/#81 — Inflation diagnosis: reserve-ratio-rail theory REFUTED, real cause open
**What:** first diagnosis (reserve-ratio multiplier railing at its cap as reserves accumulate) was
adversarially reviewed and REFUTED against the boot's own exact-tick data — the divisor
(`wvuscaled`) barely moves at the pivot quarter where `ess`/`ratio`/`infl` all jump. Real driver:
an unexplained ~51% collapse in the essentials-price SUM itself, in one quarterly tick. Only 2 of
its 12 inputs (grain, fish) had ever been probe-covered.
**Decision:** corrected `audits/AUDIT_CURRENCY_23.md` (added Finding 7, explicitly retracting the
refuted theory) rather than leaving a wrong diagnosis on record. Extended
`tools/gen_econ_tzprobe.py`'s GOODS list with the 9 remaining trackable essentials goods
(livestock, vegetables, temperate_fruit, processed_foods, clothing, furniture, pharmaceuticals,
luxury_clothing, luxury_furniture — `alcohol` excluded, confirmed dead/unloaded trade-good) and
regenerated `se_ECON_LOG_TZPROBE.txt`. Read-only diagnostic, zero gameplay effect.
**Review:** code-review CLEAN (one LOW doc count nit, fixed).
**Commit:** `754ffddf7`. **Status: root cause still OPEN (task #81) — genuinely BLOCKED-ON-DATA,
needs the next boot's new BAND rows to name the culprit good. Not a deferral: the probe that will
answer it is already shipped.**

## Task #79 — Treasury income enormously understates real treasury growth (hidden Qing revenue)
**What:** two-level bug, per the user's own framing: (1) magnitude — treasury jumps ~9000/quarter
some quarters vs a displayed few hundred to low thousands; (2) visibility — salt gabelle, Canton
customs, and caravan trade all pay `add_treasury` directly every quarter, entirely absent from the
topbar Change arrow and the nation-treasury tooltip (confirmed by reading both UI sources).
**Investigated as the magnitude suspect: salt's uncapped production base** (`se_QING_SALT.txt`
had no cap unlike its Canton/Caravan siblings, both of which explicitly cap their real-goods base
to prevent a "runaway export boom"). Adversarial review with real province-count arithmetic
REFUTED this as the ~9000 source (CHI has only 8 salt provinces vs Canton's 42 tea+silk+porcelain
provinces; salt's realistic ceiling lands at ~46-138, same order as Canton's own capped maximum
~106 — nowhere near 9000). Fixed the cap anyway as defensive hygiene/consistency with its
siblings (NOT sold as the spike fix — logged honestly as such).
**Fixed the visibility half in full:** added `INCOME_national_total_from_qing_revenue` (sums the
three streams' cached `_last` vars) and a NEW, separate `INCOME_national_total_quarterly_display`
(payment total + Qing revenue) read ONLY by the topbar's Plus/Minus/Change bindings and the
Ministry of Revenue's Total line — **first draft folded the Qing revenue directly into
`INCOME_national_total_quarterly`, which is also what `add_treasury` reads, and was caught by
adversarial review as a CRITICAL double-credit bug before commit.** Corrected to the
separate-display-value shape; re-reviewed CLEAN.
**Reviews:** salt-cap review CLEAN; income-wiring review CRITICAL (double-credit) → corrected →
re-review CLEAN (2 LOW comment nits, fixed).
**Commits:** `fda378e02` (salt cap), `f68d9e289` (income visibility).
**Status: visibility half DONE. Magnitude half (the actual ~9000 source) still OPEN — salt/Canton/
caravan all ruled out by arithmetic; remaining candidates not yet checked: tribute payments, the
silver-reserve-drift's own +250-350/quarter additions, the thin-stockpile wealth_owed trade
mechanism from AUDIT_CURRENCY_23 Finding 5/6. Genuinely BLOCKED-ON-DATA for the exact mechanism,
not a deferral — the UI half (which was fully fixable now) is shipped.**

## Task #71 — Fix Canton Silver Inflow unit display (lbs -> thousand-taels)
**What:** user reported this line might be showing lbs instead of thousand-taels.
**Diagnosis:** verified via source (`se_QING_CANTON.txt:223-237`, explicit ×10 萬兩→千兩
conversion, dated 2026-08-06, predates this session) and loc (`QING_REVENUE_MINISTRY_CANTON_
SILVER_LABEL`/`_TT` both explicitly say "千兩 (thousand taels)") — already correct, no lb/pounds
reference anywhere in this panel. **No code change made.**
**Status: DONE — verified already-correct, closed rather than left open on a stale report.**

## Task #74 — Slow Ever-Normal Granary auto-build cadence (every quarter -> every few years)
**What:** the good-year build branch of `QING_DECLINE_granary_concrete` matched and built a new
granary on every ~90-day governance pulse until the Yellow River basin backlog was exhausted,
reported as granaries auto-building too fast.
**Decision:** added a `qing_granary_build_cd` cooldown (1095 days, best-guess) gating ONLY the
build sub-block. **First draft accidentally put the cooldown in the shared outer `limit`, which
also silently gated the good-year RESTOCK block below it — caught by review as a MEDIUM bug** (a
famine-drained granary would stay wrongly flagged empty for up to 3 years after reserves actually
recovered). Corrected: restock is now its own sibling `if`, keyed purely on the stock band, no
cooldown/treasury/backlog dependency.
**Review:** first pass MEDIUM (restock over-gated) → corrected → not re-reviewed by a fresh agent
(mechanical restructure, verified the fix directly against the review's own suggested shape).
**Commit:** `6925d32dd`. **Status: DONE.**

## Task #73 — Fix Outliner icon fix regression (still showing placeholders)
**What:** a prior fix (`c1f84da9a`/`3afdea7bf`, #34) added `visible = yes` to reveal the
Construction categories' `action_icon` override, but a fresh boot screenshot (20260814014339_1.jpg)
confirms every queued item (9× Yamen, 2× Administration District) still shows the IDENTICAL
generic icon — the #34 fix did not actually resolve the symptom.
**Diagnosis:** the `action_icon` texture expression (`OutlinerItem.GetIcon`) is proven to resolve
for CHARACTER outliner items (the pattern it was copied from) but has NO proven precedent for
resolving a BUILDING's icon on a construction-queue item. Every confirmed-working building-icon
call site in this engine (`mapiconlayer.gui:1038`, `province_window.gui:4520`, and the
Terra-Indomita oracle's own `province_window.gui:324`/`gui_base.gui:6564`) instead uses
`GetBuildingIcon(<item>.GetBuilding)` — a different two-step accessor. No repo, vanilla, or oracle
precedent exists either way for `OutlinerItem` exposing `.GetBuilding`.
**Decision (Rule 1 hard-block #1 — unverifiable-without-a-boot render):** shipped as a labeled
BOOT SPIKE — changed both Construction categories' `action_icon` texture to
`GetBuildingIcon( OutlinerItem.GetBuilding )`. Cannot regress below the current (already-broken)
baseline: if the promote chain doesn't exist, it fails the same way the current code already
fails (icon blank, `_default.dds` still shows underneath).
**Status: SPIKE SHIPPED, NOT confirmed. Left in_progress. Needs a boot + fresh outliner
screenshot to confirm/refute.**

## Task #82 — Add COMPREHENSIVE LOGS across the entire economic system (log everything)
**What:** standing gap named directly by the user — every diagnostic probe this project has ever
built was scoped narrowly and reactively to one question at a time, not built as durable
exhaustive infrastructure, and "that wasn't logged" kept surfacing mid-investigation. User directive
(repeated, explicit): log everything, log volume is not a constraint.
**Status: IN PROGRESS, not yet complete.** First slice shipped as part of the inflation probe
extension (task #81/Finding 7, commit `754ffddf7`). Full scope (country_unit_price for every good,
not just zone-level prices; wealth_owed per category; exact-tick amounts for every hidden revenue
stream) still open — continuing this run.

## Task #79 continued — treasury ~9000/quarter spike hunt, sweeping the 24h commit surface
**Correction from the user mid-investigation:** this is NOT the same bug as #30/#112/#115
("treasury income orders of magnitude too high" — the DISPLAYED figure was wrong). The current bug
is "treasury income displayed is fine, but treasury VALUE increases by orders of magnitude more
than what income displays" — a hidden-payment bug, not a wrong-display bug. Per the user, the error
surface is code committed within 24h of the boot (Aug 13 02:00 - Aug 14 02:10).
**Swept and REFUTED, in order:**
- `ba8b38672` (fix #30) — user-confirmed different bug class, not this one.
- Maritime Customs (`QING_customs_pulse`/`CURRENCY_grant_country_wealth`, surfaced via `0c04c6620`)
  — arithmetic looked like an exact match (~1000x display-vs-real gap, up to ~11,400/quarter) but
  the mechanic is gated to the 1854+ Shanghai Customs founding and never fires in this 1763-1766
  boot — confirmed empirically, zero LOG-line occurrences. **Process lesson: checked the magnitude
  arithmetic before checking whether the mechanic was even ACTIVE — should always gate-check first.**
- Cottage Industry buildings / vegetables price (`b7b223729`) — user confirmed zero such buildings
  were actually constructed in the boot; considered for the separate inflation question, not this one.
- `qing_revenue.5` "Fullest Coffers" milestone event (`61a156e19`/`27e3ccdfb`) — double-refuted: no
  treasury effect in its own code, AND never fired in this boot (reserve well below its peak trigger).
**Still open, not yet ruled in or out:** tribute (`QING_subject_collect_tribute`,
`se_SUBJECT_QING.txt:1173-1224` — has an uncapped branch charging a subject its entire treasury,
paid directly to CHI) and the thin-stockpile `wealth_owed` income-side channel (AUDIT_CURRENCY_23
Finding 6). **Status: BLOCKED, genuinely unresolved at this point in the run — not a deferral, the
candidate list is real and traceable, just not yet finished.**
**Process note logged per user correction:** ruled-out hypotheses belong in
`audits/SCRATCH_CURRENCY_23.md`, never in `AUDIT_CURRENCY_23.md` (verified conclusions only) —
corrected mid-run (commit `5a9e96b88`) after initially polluting the audit doc.

## Task #75/#76 — Ministry of Works building breadth / Macro Builder missing buildings
Both audited and closed as NO DEFECT FOUND, not fixed:
- Ministry of Works already auto-constructs dikes, canal depots, wall sections, the two capstone
  monuments, AND 5 specialty production works (silk/porcelain/tea/cotton/salt) via
  `QING_works_build_specialty` — genuinely broad. The Ever-Normal Granary auto-build (already
  fixed, task #74) is a completely separate mechanism, not part of the Works Ministry at all —
  that's why it looked like "the only thing Works builds."
- Macro Builder correctly excludes Dujiangyan + 8 other unique historical monuments
  (`allow = { always = no }`, seeded via `add_building_level` bypassing `allow` — confirmed for
  Dujiangyan and spot-checked for 3 others sharing the same pattern). Not menu-buildable anywhere,
  by design, not a bug.

## Task #77/#78 — Lifan Yuan Vacant Positions / Yili garrison line
Both functions that should be firing (`QING_ministry_recompute_perf_lifanyuan`'s vacant-listing
else-branch; `QING_fgar_apply_occupation`) had ZERO diagnostic trace anywhere, so neither report
could be checked against a real boot log. Added logging to both — **first attempt used LOG_line
with a message ending in "for", which a code review caught as fundamentally broken: `LOG_line`
never appends a scope name anywhere in this codebase (confirmed via `se_LOG.txt` — it's a literal
line with no interpolation at all; only `LOG_state`/`LOG_fail` dump real scope info via
`debug_log_scopes = yes`).** Every historical "...for" `LOG_line` call across the whole codebase
has the same defect — logged as its own task (#83), not fixed broadly this session. Both of
TODAY's additions corrected to use `LOG_state` instead, verified by a second review to actually
resolve to the correct subject scope.
**Status: both BLOCKED-ON-DATA — the logging is now real, but confirming/refuting either report
needs the next boot.**

## Task #72 — Relieve & Resettle / Remit the Taxes: DONE
Designed (design/DESIGN_72_POPULATION_LEVERS_CONCRETE.md), adversarially reviewed (design doc had
the wrong modifier-file target — corrected to `imp19c_province_modifiers.txt` — plus two logged
known limitations: relief's flat 150-food draw decays in relative impact as granary capacity
grows over a campaign; remission's province scope over-shoots "the stricken provinces" since
`qing_pop_pressure` has no per-province breakdown to target more narrowly), implemented, re-
reviewed CLEAN. Relieve & Resettle now DISTRIBUTES real granary stock (was backwards — adding to
the pool, funded by treasury, disconnected from the "open the granaries" narrative) gated on
having enough to distribute; Remit the Taxes now suspends REAL land tax for a year via a new
province modifier (`qing_tax_remission_active`, `local_tax_modifier = -1.0`), not just an abstract
pressure-meter nudge.

## Task #63 — Opium Commissioner revenue + squeeze meter
Found an EXISTING, fully-adversarially-reviewed design doc from earlier in this session (before
compaction) — `design/DESIGN_63_OPIUM_COMMISSIONER_REVENUE_SQUEEZE.md`, 6 review rounds, marked
"FINAL v7, READY FOR IMPLEMENTATION" — and implemented THAT instead of drafting a new one from
scratch (my own first-draft redesign incorrectly treated this as a Salt-style revenue-farming
office; the existing design correctly identifies it as an INTERDICTION office modeled on Lin Zexu,
so the squeeze meter attenuates the prohibition-era suppression bonus continuously rather than
skimming a tariff, and the revenue piece generalizes an EXISTING one-shot "tolerate-for-revenue"
grant into a recurring credit instead of inventing a new tax on a still-nominally-prohibited
trade). Implemented across `se_QING_OPIUM.txt`, `se_QING_FRONTIER_PICKER.txt`, and folded the new
`qing_opium_income_last` into this session's own hidden-revenue visibility total
(`INCOME_national_total_from_qing_revenue`) so it doesn't immediately become a fifth hidden-income
gap. Code review in progress at time of this log entry.

## Task #63 continued — Opium Commissioner review landed CLEAN, committed
Review (agent `aa07c1b949914b17c`) returned CLEAN, no CRITICAL/HIGH. One MEDIUM left
open and logged rather than hidden: the nested `multiply = { value = 100 subtract =
var:qing_opium_commissioner_squeeze } }` inside a `change_variable` (`se_QING_OPIUM.txt`
ramp function) is proven only in `script_value` contexts elsewhere in this repo, never
before demonstrated inside an in-effect `change_variable`. Arithmetic hand-verified
correct (squeeze=0→-4, squeeze=100→0, squeeze=50→-2); the open risk is purely whether the
engine's parser accepts this construct here. Per Rule 1a this is NOT a hard block — shipped
as-is, flagged for boot confirmation, not held back.
**Commit:** `bb3bbffbd`. **Status: DONE (implementation), boot-verification of the one
MEDIUM-flagged construct still outstanding.**

## Task #59/#62 — Revenue Minister oversight-drag term (h) + Customs squeeze meter: DONE
Implemented `DESIGN_59_REVENUE_SQUEEZE_PENALTY.md` + `DESIGN_62_CUSTOMS_SQUEEZE_METER.md`
together in one pass (the docs are explicitly coupled — #62 depends on #59's scaffold).
Term (h) in `QING_ministry_recompute_perf_revenue` adds a running-average "subordinate
oversight drag" (Salt/Canton×0.7/Caravan/Customs squeeze meters ÷ count×9, mathematically
identical to the old fixed /27 divisor when Customs is absent). Customs gained its own
`qing_customs_ig_squeeze` meter (seed 30, mirrors Hart's `.corruption` when seated, decays
toward baseline when vacant — Customs' default state, unlike the other three offices).
**Review:** dispatched to a fresh agent covering both files together — CLEAN, no
CRITICAL/HIGH/MEDIUM. Hand-traced running-average arithmetic against 3 cases (3-office
baseline, all-maxed, Customs-present-and-maxed) all landed exactly on the design docs' own
predicted values (−3.0, −10.0, −10.28 respectively). One LOW doc nit (new squeeze var
missing from the file-header inventory) — fixed before commit.
**Commit:** `daf4732cf`. **Status: DONE.**

## Standing instruction — client_state added to amban/garrison eligibility
Direct user instruction from earlier in the session, carried forward unactioned across the
compaction boundary: add `client_state` to `QING_amban_garrison_eligible_type_trigger`
(`common/scripted_triggers/qing_dynasty_triggers.txt`). Done — verified `client_state` is a real,
already-used subject type (`00_default.txt:542`) before adding it to the OR-set.
**Commit:** `2afbabee9`. **Status: DONE.**

## Task #57 — Production-linked New World crop pop-boom pulse
Design (`design/DESIGN_57_NEWWORLD_CROPS_CONCRETE.md`) reached FINAL v9/READY FOR IMPLEMENTATION
(7 review rounds) earlier in this session, before the context compaction that lost track of this
status. Implemented the resolved shape exactly: new `QING_pop_newworld_growth_pulse`
(se_QING_POPULATION.txt), piggybacking `QING_GOV_pulse`'s cadence alongside `QING_pop_pulse`.
Recomputes `qing_newworld_farmstead_count` every pulse (owned provinces with the New World
farmstead building), computes `floor(farmstead_count/10)` via the proven `round = floor`
script-value idiom (se_AI.txt:373-379 precedent), and on an UPWARD tier crossing creates a small,
FIXED `pops_per_tier=2` pop batch (never scaling with farmstead_count — the exact conflation the
design's round-1 review existed to prevent) on the 2 highest-population New-World-crop-growing
provinces, sets `migr_gov_push`, and grants `qing_migr_crop_boom`. The tier ratchet is SET (never
incremented) per the design's round-5 fix. The removal check is a SEPARATE, unconditional branch
(NOT nested under the upward gate) per the design's round-3/round-4 fix — the exact stuck-modifier
bug those rounds existed to prevent. Diagnostic logging is a band-ladder snapshot (tier-crossed +
total_population band), matching `QING_DECLINE_apply_pop_pressure_band`'s proven idiom, since this
engine cannot render raw numeric trend values in logs. Retired the OLD event chain's own one-shot
`create_state_pop` calls (`qing_migration.20.a`, `qing_migration.22.a`) — pop creation is now
production-linked; the event chain keeps its modifier-swap/capacity/push levers as the narrative
wrapper, per the design's explicit instruction.
**New script_value**: `qing_newworld_pop_tier_cmpsvalue` (`00_event_values.txt`), matching the
file's own proven RHS-comparison-rule idiom (a var-ref is illegal directly on a comparison RHS).
**Review**: CLEAN except one MEDIUM (unconditional `qing_migr_crop_boom` re-grant could reintroduce
the neutral boom's growth/tax terms alongside a LATER-resolved `_golden`/`qing_migr_overpopulation`
state that the event chain had swapped it away for -- distinct modifier keys, would stack) --
fixed by gating the re-grant on `NOR = { golden, overpopulation }`. Two LOW notes accepted as-is
(boot-tunable band thresholds; TIER_THRESHOLD=10 duplicated in two commented-together spots). Also
fixed a pre-existing, unrelated brace-count false positive caught by the pre-commit hook in the
same file (00_event_values.txt) once touched: a comment quoting the engine's literal "Cannot read
[{]" error text had an unmatched brace in prose -- reworded, no meaning change.
**Commit:** `a54618271`. **Status: DONE.**

## Task #58 — Cottage-building culture-gate research pass (10 buildings, not 8)
Design (`design/DESIGN_58_COTTAGE_CULTURE_GATING.md`) reached FINAL v8/READY FOR IMPLEMENTATION
(3 review rounds) earlier in this session, before the same compaction. Implemented the resolved
shape: all 8 original `qing_cottage_*_building` entries (smithy/leadworks/weaving_hut/silk_reeling
_shed/woodlot/herbalist/founders_workshop/quarry) dropped their Qing-only culture gate — a per-good
research pass found ZERO of the 8 crafts clear the bar of a genuinely Qing-distinctive institution
at household/cottage scale, including silk (round-1/round-2 review: household reeling feeding
urban filatures is close to the DEFAULT pattern everywhere pre-industrial silk was produced, not a
Chinese peculiarity). The redundant non-Qing generic `row_cottage_workshop_building`
(`row_production_buildings.txt`) — which had the identical "9 crafts, 1 interchangeable building"
defect — is DELETED along with its full GUI/loc wiring across 7 files (gui_templates.gui,
custom_tooltip.gui, province_window.gui, row_buildings_l_english.yml, plus 5 stale "eight Qing
cottage buildings" header comments across gui_templates.gui/custom_tooltip.gui/
macro_builder_view.gui/province_window.gui/the macro config, all corrected to state the real
10-buildings/8-generic+2-Qing-exclusive count).
Two goods DID clear the bar with a sharper citation and got genuinely NEW Qing-only buildings,
gated on the SPECIFIC historic province IDs (via the proven bare `province_id = N` trigger,
`00_omens.txt` precedent — NOT the unprecedented `province = { id = N }` shape my first draft used
before catching it against source): `qing_timber_lineage_building` (力分/山分 lineage-tenure timber
contracts, Meng Zhang 2021 — Huangshan/4441 + the 14 terrain-verified Fujian-highland candidate
provinces; does NOT require `trade_goods = wood` since the institution is about the LAND, not the
current good — Huangshan is tagged `tea`) and `qing_cottage_sugarhouse_building` (糖廍 pooled
sugar-house, gated on `trade_goods = sugar` + the 6 Guangdong/Fujian sugar-tagged province IDs).
**Design's own 2 remaining open historical-geography judgment calls** (the final qualifying subset
within the 14 Fujian timber candidates; the final subset within the 6 sugar candidates) are
genuinely unresolvable from any in-repo research per the design doc's own 3 review rounds —
resolved per Rule 1a with an explicit, logged OVERNIGHT DEFAULT: gate on ALL candidates in both
lists rather than hold the buildings for an unresolvable call. Both new buildings got full
province-window + macro-builder GUI/loc wiring matching every sibling Qing building exactly
(build_item/macro_build_item template pairs, tooltip/macro-tooltip templates, macro-builder
allowlist entry, name/desc/tooltip/macro-title loc), appended to `CottageIndustryItemsRow2` in both
`province_window.gui` and `macro_builder_view.gui` (4→6 items), per the design's own resolved
row-capacity fix (no third row — matches this file's own proven ≤7-item-safe threshold).
**Review**: dispatched, in progress at time of this log entry.
**Status: implementation DONE, review pending.**

## Related files
- `audits/AUDIT_CURRENCY_23.md` — Finding 6 (treasury-spike hypotheses ruled out/advanced),
  Finding 7 (inflation reserve-ratio theory refuted, corrected direction).
- `audits/SCRATCH_CURRENCY_23.md` — working notes, not committed (local reference only).
- `design/DESIGN_72_POPULATION_LEVERS_CONCRETE.md`, `design/DESIGN_63_OPIUM_COMMISSIONER_REVENUE_
  SQUEEZE.md` — design docs for tasks #72/#63.
