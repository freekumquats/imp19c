# Boot-test bugs — 2026-07-16 (build 1763_bookmark @ b37cb9847)

Bugs reported from the boot test of the b37cb9847 build. Fixes committed as freekumquats and
pushed so the user can re-test on the other machine.

## B1 — Propose-a-Marriage: realm rows are dead (clicking a country does nothing)
**Symptom:** the Propose-a-Marriage button now opens the realm list correctly (fixing the earlier
blank-window bug), but clicking a country row does nothing — screen 2 never opens.
**User redesign (adopted):** rather than debug the standalone realm-picker window, move the entry
point to the **diplomatic view**: add a **"Royal Marriage"** action button under the country's
actions area. The viewed country IS the target (`DiplomaticView.GetTargetCountry`), so the realm
picker (screen 1) is dropped entirely — the button jumps straight to screen 2 (our character) →
screen 3 (their character) → launch.
**Feasibility:** confirmed. The diplomatic view already hosts mod-added scripted_gui action buttons
(the "Trade Actions" collapsible block, diplomatic_view.gui:1475+) that pass
`DiplomaticView.GetTargetCountry.MakeScope` as `target` — the exact pattern needed.
**Fix:** new scripted_gui `marriage_play_diplo_open` (country scope, saved_scopes = target) that
combines marriage_play_open + marriage_play_pick_realm — clears stale vars, sets marriage_play_target
= the viewed realm, builds own + their candidate lists — then the button opens marriage_play_own_window.
Gated Player = CHI, target ≠ self, target has a current_ruler. Old realm-picker screen (screen 1)
retained but no longer the entry path (or removed if clean).

## B2 — Public Works crowded the Infrastructure row (province build view)
**Symptom:** the 6 Board-of-Works build items were appended into `InfrastructureItems`, misaligning
that row. **Fix:** new standalone `PublicWorksItems` section in the `building_box` template
(gui_templates.gui) — its own row like Infrastructure/Military; moved the 6 items there in
province_window.gui; new loc `buildings_public_works` = "Public Works". DONE.

## B3 — New Treasure Fleet tree STILL not visible in the mission browser
**Symptom:** despite the #19 fix (moved the province-walk out of `potential`), the tree still does not
appear. Loc is complete (all 5 tree keys + task keys present), definition is structurally identical to
visible siblings (xinjiang), custom_tooltip block-form in `allow` is proven. Cause not yet found —
UNDER INVESTIGATION.

## B4 — South Seas Opening (Nanyang) tree missing loc (raw keys shown)
**Symptom:** `qing_nanyang_mission_DESCRIPTION` / `_CRITERIA_DESCRIPTION` shown raw. **Cause:** the 4
tree-level keys (_DESCRIPTION/_CRITERIA_DESCRIPTION/_REWARD_DESCRIPTION/_BUTTON_TOOLTIP) were never
added. **Fix:** added all 4 to qing_nanyang_l_english.yml (BOM preserved). DONE.

## B5 — Ministry of Works window: giant blank black section
**Symptom:** the #5 hydraulic-rows change used a `vbox`, which EXPANDS to fill the panel → giant black
gap. **Fix:** replaced the vbox with a fixed-height vertical `flowcontainer` (hugs content like every
other row in the panel); header row + 3 indented type rows. DONE.

## B6 — Religion window: deity list overflows the window bottom (no scroll)
**Symptom:** the Confucian/Buddhist/Taoist/folk pantheon list (12 deities from #8) spills past the
window's bottom edge instead of scrolling. Likely the deity grid isn't inside a scrollarea, or the
window is fixed-height with the list unbounded. UNDER INVESTIGATION.

## B7 — Pantheon deities have no localization (raw keys: omen_deity_war1, omen_deity_economy1, ...)
**Symptom:** the seeded deities (#8) show raw omen/deity keys instead of names. **Cause:** the 12 new
deities in common/deities/03_confucian_pantheon.txt reference name/omen loc keys that were never
written. **Fix:** add deity name + omen/description loc. UNDER INVESTIGATION (find the exact keys).

## B8 — Migration Report still shows only Nanchong (possibly intended)
**Symptom:** the migration report (fixed in #10 to walk every_owned_province) still lists only
Nanchong. May be correct (only Nanchong currently meets the push threshold) or the walk/threshold is
still wrong. NEEDS INVESTIGATION — confirm whether the report lists all provinces above threshold or
is still province-scope-limited.

## Holy sites / deities — see B6/B7 (one cluster, under investigation)
User also reports Holy Sites section blank + unsure if the 12 custom deities appear at all.
