# DESIGN — #88 unify frontier-settlement + NW pop-boom + Population/Famine

> STATUS 2026-08-12: REVIEWED — CLEAN after 1 fix. Adversarial review confirmed the scoping (already-
> unified system, discoverability-only gap, sizing fits) but found one real defect in the proposed
> fix's loc-key reuse (below, now corrected). Ready to implement.

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:44`: "UNIFY frontier-settlement + NW pop-boom +
Population/Famine into one system (Population & Famine window)."

## Finding: the unification #88 asks for is ALREADY BUILT, under task #369

`design/DESIGN_POPULATION_FAMINE.md` (task #369, status "BUILDING" in its own banner but confirmed
IMPLEMENTED AND COMMITTED on disk) is titled "Population/Migration/Famine Deep Model" and its own
§1 thesis states the unification goal in the same terms #88 uses. Tracing the three named pieces:

1. **Frontier-settlement** — `events/imp19c_mod_events/qing_frontier_migration_events.txt`
   (`qing_migration.20`-`.23`, one-shot: arrival → boom → forks to golden `.22` or crisis `.23`) +
   `common/scripted_effects/se_QING_COLON.txt` (`QING_COLON_heartland_push`/`_clear`,
   `QING_COLON_apply_frontier_pull`). One-shot by design; plants the modifiers `qing_migr_crop_boom`
   / `qing_migr_crop_boom_golden` / `qing_migr_overpopulation`
   (`common/modifiers/qing_migration_modifiers.txt`) and a `qing_newworld_crops` flag.
2. **NW pop-boom** — the SAME family as #1, not a separate mechanic: the three modifiers above are
   the NW-boom's persistent trace after its one-shot event fires. There is no independent "NW
   pop-boom" system to unify separately.
3. **Population & Famine window** — fully built: `common/scripted_effects/se_QING_POPULATION.txt`
   (321 lines, standing `qing_pop_pressure` meter 0..100, quarterly pulse), a scripted_gui
   (`common/scripted_guis/QING_population_panel.txt`, 91 lines, 4 levers: RELIEVE & RESETTLE 賑濟移墾,
   REMIT TAXES 蠲免, PROMOTE FRONTIER SETTLEMENT 移民實邊, plus the meter itself), and a GUI window
   (`gui/qing_population.gui`, 230 lines). Follows the proven `#366 opium` scripted_gui meter-panel
   template (`QING_population_panel.txt:15-16` names it explicitly; `is_valid` mirrors each effect's
   own guard, `ai_is_valid = { always = no }`).

**The coupling is real, not incidental.** `se_QING_POPULATION.txt`'s target-recompute reads
`qing_newworld_crops`/`qing_migr_crop_boom_golden` (a +18 involution term when the boom fired but
wasn't golden) and `qing_granary_stock` (the existing famine buffer) as direct inputs to the
pressure meter; the quarterly pulse itself calls `QING_COLON_heartland_push`/`_clear` off the
pressure band (>=60 push, <35 clear), with an explicit `[#371-R]` guard (`se_QING_POPULATION.txt:
176-182`) so the standing quarterly clear never stomps a push the one-shot boom event just made. One
meter reads and drives all three legacy pieces — this IS the unification #88 describes, already
shipped under #369's commits (`ca52862fc` + 4 follow-up fixes, latest `62d7fb23c`).

## The one real gap found: the panel is not reachable from the main government view

`QING_population_panel.txt:15-16`'s own header comment claims the open-button lives "in
government_view.gui" — that claim is **stale/aspirational, not true on disk**. Confirmed via grep:
zero references to `qing_population_open_panel_button` or `qing_population.gui` anywhere in
`gui/government_view.gui`. The button is currently wired into exactly two places, both SUB-panels
reached by first opening something else:
- `gui/qing_province_reports.gui:404-421` (a caption-replacement button under the "In-Migration
  Hotspots & Crowded Provinces" report section — added under task #49).
- `gui/qing_revenue_ministry.gui:490-503` (under the Ministry of Revenue 戶部 window).

By contrast, every other L4 dashboard of this class (Southern Study, Court Intrigue/Princes) gets a
direct button in `government_view.gui`'s main Throne row (`gui/government_view.gui:2874-2907`,
`text_button_square_highlighted` + `GetScriptedGui(...)` + `gui.createwidget` — the exact same
scripted_gui idiom `qing_population_open_panel_button` already implements). The Population & Famine
panel is the ONE dashboard of its tier missing a top-level entry point; a player who hasn't opened
province reports or the revenue ministry has no obvious way to find it at all.

## Proposed fix (minimal, additive, no logic change)

Add a THIRD button instance to `gui/government_view.gui`'s Throne row, alongside Southern Study and
Court Intrigue (`:2874-2907`), using the identical `text_button_square_highlighted` +
`qing_population_open_panel_button` scripted_gui + `gui.createwidget gui/qing_population.gui` idiom
already proven at the two existing call sites. This does NOT touch `se_QING_POPULATION.txt`,
`QING_population_panel.txt`, or `gui/qing_population.gui` — those are correct and complete. It is
purely a THIRD `datacontext`/`onclick` wiring of the SAME existing scripted_gui object, matching a
pattern this file already uses successfully in two other places for two OTHER panels. No new loc key
is needed: `QING_POPULATION_OPEN_TT` for the tooltip, and **`QING_POPULATION_OPEN_BTN`** (already
defined, `localization/english/qing_population_l_english.yml:3`, "Population & Famine (人口壓力)",
already used verbatim at the revenue-ministry call site, `gui/qing_revenue_ministry.gui:498`) for the
`Center_text` label — parallel in form to `QING_SS_OPEN_BTN`/`QING_PRINCES_OPEN_BTN`, the sibling
Throne-row buttons' own generic dashboard-name labels.

**Correction (adversarial review finding):** the original draft of this doc wrongly proposed reusing
`qing_migration_report_count` (a report-SECTION CAPTION — "In-Migration Hotspots & Crowded
Provinces," `localization/english/qing_province_reports_l_english.yml:15`) for the new button's
label. That key is contextually wrong outside the province-reports caption it was written for — it
would render as a confusing, unrelated sentence in the Throne row. `QING_POPULATION_OPEN_BTN` is the
correct, already-proven generic label and must be used instead.

Existing sub-panel entry points (province reports, revenue ministry) are left in place — this is
additive, not a relocation; a player already used to finding it there is unaffected.

## Scope explicitly excluded (not #88, not this doc)

- No new meter, lever, or mechanic — #369 already covers the substance.
- No GUI redesign of `qing_population.gui` itself.
- Not a "unify the code" refactor — the three legacy pieces (frontier events, NW-boom modifiers,
  population meter) correctly remain three separate files/effects; #369's unification is behavioral
  (one meter reads/drives all three), not a file-merge, and that is the correct shape — merging the
  one-shot event files into the standing pulse effect would violate this codebase's own
  concrete-over-abstract / don't-collapse-working-mechanics conventions for no benefit.

## Disposition

Pending review: if confirmed, implementation is a single ~15-line additive GUI block in
`gui/government_view.gui`, code-reviewed like any other GUI change, no design risk. #88 closes as
"already unified by #369; discoverability gap fixed."
