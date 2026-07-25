# Boot test 2026-07-24 17:42–17:54 (branch merge-overnight @ 0d718dc48 — Stream 1 + PART IV)

Log: logs.zip (error.log 17:54). 6 screenshots (17:45–17:51). Analysis below.

## STREAM 1 FIXES — ALL HELD, ZERO REGRESSIONS (log-confirmed)
- family scope-fail flood: 0 (was 13) ✓
- qing_btc_gov promote flood: 0 ✓
- religion_view margin_right: 0 ✓
- government_view 'margin' not handled: 0 ✓
- diplomatic_view position-in-layout: 0 ✓
- qing_reform_pressure unset: 0 ✓

## PART IV — ZERO NEW LOG ERRORS
No error references any new effect/event/law (QING_settle_forge_nation, QING_settle_plant_works,
QING_treaty_impose_concession, greatgame.4/.5, ideology.3/.4, military_upkeep_law, etc.). Laws render
complete (screenshot: all 13 incl. Military Upkeep 武備 → Statutory Minimum). Deities show WITH holy sites
(Karl Marx→Temple of Trier, etc.).

## USER-REPORTED UI ISSUES (this test) — punch-list, NOT YET FIXED
1. **religion — deity list slightly overspills bottom.** Fragile @window_height chase (900→872→852). Real fix:
   give omens scrollarea a FIXED height + drop layoutpolicy_vertical=expanding (per scroll-rule), so clip is
   carried by the scrollarea not the window.
2. **religion — vertical scrollbar too far right (on window edge).** Inset it left at the call site. NOTE: no
   repo call site insets the bar via position/margin, and VerticalScrollBarForBox is a SHARED template (do not
   edit it — would move every scrollbar). Needs a per-instance position/anchor override — unproven idiom, verify.
3. **religion — Faith & Sedition tab content floats vertically-centered mid-panel** (screenshot 174747 confirms
   big empty gap above/below). Its outer vbox (religion_view.gui:1405) has layoutpolicy_vertical=expanding but a
   fixed-height inner content that isn't top-pinned (unlike the omens tab whose scrollarea fills the space). Fix:
   top-anchor the F&S content (drop expanding on the outer vbox, or add a bottom spacer/expanding filler).
4. **religion/F&S — "Suppress Missions" list empty → NOT A BUG.** Screenshot 174640 shows the tab reads "No
   province yet bears a mission station..." — correct: no missions exist at the fresh 1763 start. Button worked
   then greyed = its cooldown. Button + list are consistent; my earlier "gate mismatch" framing was wrong.
5. **religion — remove the redundant sub-header.** margin_widget block at religion_view.gui:294–315 (three
   sub_header textboxes echoing the active tab title: LOCAL_HOLY_SITES / QING_FAITH_SEDITION_HEADER; omens one
   already blanked at :300). The category_tab buttons (316+) are the real tabs. Fix = delete the margin_widget.
6. **foreign buildings — 4 authorization-only types invisible on BOTH city AND settlement provinces.** Screenshots
   175143 (city Maoming: Foreign shows only 3) + 175147 (settlement Qujing: Foreign empty). My R2 fix (Stream 1)
   is DISPROVEN: `allow = custom_tooltip{ has_variable = qing_fbuild_menu_unlock }` does NOT list-grey the type —
   it hides it, same as the old always=no. The 3 VISIBLE foreign buildings (underground/public mission,
   concession) use a plain trigger allow (has_city_status / sufficient_job_slots). ALSO: potential={has_city_status}
   on all foreign buildings excludes settlement-rank provinces entirely (why the settlement Foreign box is empty).
   Fix direction: match the proven-visible pattern (plain trigger allow like the concession, or a real tech gate
   that greys like production buildings); reconsider `potential` for settlement visibility. Drop the sentinel-var
   theory — this boot proves it hides, not greys.

## PRE-EXISTING (NOT PART IV, NOT ACTIONABLE HERE)
- "should be in utf8-bom encoding" warning: emitted for ~300 files mod-wide incl. vanilla Imperator files;
  benign ("will try anyways"). My settle_frontier files are 3 of ~300. Not my regression.
- "Mission <X> lacks a final task and can't be completed": 18 mission trees (nearly all Qing + vanilla
  russian/hispano_american). Systemic — only qing_treasure_fleet uses final=yes. Pre-existing (in the old log).
  Cosmetic validation warning; missions still complete via task completion. Candidate cleanup: add final=yes to
  each capstone task across the enterprise trees.

## U4 CURRENCY FLOOD — STILL PRESENT ON merge-overnight (EXPECTED)
DIPLOMACY:100 (22,638) + CURRENCY cluster (18,746×7 + 13,230 + 5,831). The U4 fix lives only on the
upstream_bugs branch, not merge-overnight — so the fork still floods. Unchanged/expected.
