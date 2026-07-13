# 1763 boot-test notes — 2026-07-13

User playtest of 1763_bookmark. Findings below are NOTED ONLY (not yet fixed) unless marked FIXED.

## FIXED this session
- **Dynastic Harmony row height.** The #387 Dynastic Harmony / Suzerain Prestige row was 950x26
  (margin 12 3, 22px cells) while the two health-counter rows below are 950x44 (12 6, 30px). Bumped
  to match. (gui/government_view.gui, commit 08c6dc4c2)
- **BT-47b — throne cards, wasted gap.** Emperor/Crown Prince/Empress cards had the favor +
  faction squares in their own full-height columns (24px tall) between portrait and info block,
  leaving empty space and pushing the loyalty/statesmanship/skills block right. Rewired all three
  to the office-card idiom: portrait-only column, favor→faction→name INLINE in the name row, so
  the block sits flush after the portrait and grows left. (gui/government_view.gui, commit 125b1aa26)

## NOTED — to fix

### N1 — Heir sub-header still shows "Primary Heir" instead of "Taizi (皇太子)"
BT-49 (eec8490fc) gated ONLY the monarchy heir sub-header at government_view.gui:587 with the
SelectLocalization(qing_ruler_is_sinosphere → QING_TAIZI, NEXT_RULER_TEXT) idiom. But there are
TWO OTHER `text = "NEXT_RULER_TEXT"` sub-headers still ungated:
- **government_view.gui:418** (tooltip NEXT_RULER_TT_REPUB) — the one the user is seeing.
- **government_view.gui:901** (tooltip NEXT_RULER_TT_REPUB_CO).
These appear to be the republic/co-ruler candidate headers BT-49 deliberately left alone, but at
least one is rendering for the Qing player and showing "Primary Heir". Fix: determine which of
:418/:901 is on the Qing monarchy path and apply the same SelectLocalization gate (or confirm the
:587 gate is on the wrong sub-header and the real monarchy heir header is :418). qing_ruler_is_sinosphere
scripted_gui already exists (QING_governance_actions.txt:662) — just needs the same wrap.
(Loc QING_TAIZI = "Taizi (皇太子)" exists at qing_governance_l_english.yml:432.)

### N2 — A sitting governor is allowed on the Grand Council; governors should NOT be able to sit
A provincial governor appears as an eligible Grand Council appointee / is seated. Governors hold a
separate office (the governor corps under the Board of Personnel 吏部) and should be excluded from
the council candidate pool. Fix location: the council candidate-refresh / eligibility filter that
builds the appoint-picker list (QING_council_refresh_lns / QING_council_refresh_lns_by, and the
per-office `ln_*` refreshers in QING_governance_actions.txt; candidate eligibility lives in
se_QING_COUNCIL.txt around the employer=ROOT guards). Add an `is_governor = no` (or exclude
`government = *_governorship` holders) to the candidate limit so a seated governor can neither be
listed nor appointed. Verify against characters_view_scripts.txt:330/361 which already use
`is_governor = yes` as a proven trigger. Also confirm the reverse: appointing a councillor should
not silently leave them holding a governorship (double-seat).

**DESIGN DIRECTION (user):** the clean fix is to make Grand Council positions REAL ENGINE OFFICES,
the same way governors are engine offices — not var-tracked pseudo-offices. The engine already
enforces one-office-per-character, so modelling council seats as genuine offices would
AUTOMATICALLY exclude governors (and every other office-holder) from dual-hatting, in both
directions, without per-filter `is_governor = no` patches. This supersedes the narrow N2 filter fix.
NOTE: this is the same direction as existing task **#396 "Grand Council members need real exclusive
engine offices (EXECUTE ON merge-overnight)"** — which is currently scoped to merge-overnight, not
1763_bookmark. Decide whether to (a) do #396 on merge-overnight and let it flow to 1763 via the
merge, or (b) apply the exclusive-office model directly on 1763_bookmark now. The current 1763
council uses `qing_office_<X>_holder` VARIABLES (se_QING_COUNCIL.txt) rather than engine offices,
so converting is a substantial rework — not a quick boot-test patch. Until then, N2's `is_governor = no`
candidate-filter is the stopgap that stops the visible governor-on-council bug.


### N3 — Religion "Faith & Sedition" window: header only, and clicking opens nothing
Window shows only the "Faith & Sedition" header; body is empty AND clicking the header/button does
not open the separate religion panel. Wiring LOOKS correct: religion_view.gui:230 onclick =
`gui.createwidget gui/qing_religion.gui qing_religion_panel`, and gui/qing_religion.gui:24 defines
`name = "qing_religion_panel"` (names match); qing_religion_open_panel_button scripted_gui exists
(is_shown tag=CHI). Two symptoms: (a) empty BODY — likely the BT-53 layout issue (body-as-sibling /
missing layoutpolicy) BT-53 left a diagnostic sentinel for at 6f35dbcc7; check debug.log for
"QING F9: religion panel open." to tell OPEN-fires vs body-fails-to-lay-out. (b) click DOES NOTHING —
the createwidget console onclick may fail silently (wrong path/name, or widget already exists so
createwidget no-ops), OR the clickable element the user sees is a different widget than the one
carrying the onclick. Prior tasks #345/#377/BT-14/BT-53 all touched this and it is STILL broken —
treat as a proper re-investigation, not another nudge. Mirror the government-view F9 open idiom
(gui.createwidget + ClearWidgets, imp19c-gui-panel-open-idiom).

### N4 — Migration report lists only one province (Nanchang); "used to list many"
BT-55 (39ddaf7c4) rewrote the build into PASS 1 (mark qualifying governorship provinces with
qing_migr_report_pick) + PASS 2 (emit via ordered_owned_province order_by total_population). Qualifying
filter (qing_province_reports.txt ~156): province shows if qing_migr_hongkong_boom OR qing_nwcrop_abundance
OR total_population >= 20. Possibly intended (only hotspots show, and at 1763 few qualify — no HK boom,
NW-crop not spread). BUT verify a possible regression: PASS 1 marks inside every_governorships >
every_governorship_state > every_state_province, then PASS 2 emits via `ordered_owned_province` filtered
on the mark. If a marked province is not enumerated by ordered_owned_province the same way (governorship
vs capital-domain, or ownership-scope mismatch), PASS 2 emits FEWER than PASS 1 marked — that would drop
provinces from the list. Check: does marked count (PASS 1) == emitted count (PASS 2)? If equal, it is
intended/threshold behaviour; if PASS 2 < PASS 1, that is the regression. Either way, consider lowering
the pop threshold or documenting the "hotspots only" intent so it does not read as a bug.

### N5 — Subject tab (Qing diplomatic view): loyalty-to-overlord text + breakdown not visible
In the Subject tab of the Qing diplomatic view, the line "Loyalty to the Jurchen Major Power of Great
Qing" and its numeric breakdown do not appear. They SHOULD render below the "Type: [subject type]" row
and the loyalty bar. This is the BT-58/59 area (restore subject loyalty bar + loyalty-breakdown overlap
fix, commit 64a110cad) — the breakdown block is either still overlapping/clipped, zero-height, or
positioned off the visible area. Fix location: the subject/diplomatic-view GUI (diplomacy/subject tab
in gui/, the widget stack holding Type: + loyalty bar + the loyalty-breakdown textbox). Ensure the
breakdown widget is a sibling laid out BELOW the loyalty bar with real height (multiline + fixed size,
not autoresize collapsing to 0), matching the BT-59 overlap fix intent.
- **N5b (same area):** there is EMPTY SPACE below the "Decisions" block; move the Type: [subject type]
  row + loyalty bar UP to close that gap AND to free vertical room for the missing loyalty-breakdown
  text below them. So the fix is a layout reflow of the subject-tab stack in gui/diplomatic_view.gui
  (BT-58/59 area, ~commit 64a110cad): Decisions -> Type -> loyalty bar -> loyalty-breakdown, tightened
  vertically so the breakdown fits without overrunning.

## DESIGN ITEMS (not bugs — deferred features)

### D1 — Canton trade open/close should be a proper LAW
Currently Canton open/close is a toggle (scripted_gui / event-driven). User wants it modelled as a real
game LAW: a `law_group` with open/closed laws carrying their own modifiers, switched like vanilla laws,
not an ad-hoc toggle. Implementation: define the law_group + laws in common/laws, move the Canton
open/closed modifiers/effects onto the laws, wire the existing Canton mechanic (se_QING_CANTON /
qing_canton_events) to read/set the law, add loc, surface in the Canton panel. Medium build; after the
boot-test pass.
