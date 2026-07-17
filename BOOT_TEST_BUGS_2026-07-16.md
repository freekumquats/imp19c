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

## B9 — Palace Eunuch roster rows squashed (skills cut off)
Refer to Captains of the Guard (qing_guard.gui) for the correct row height. Household panel eunuch list.

## B10 — Palace Eunuch list is ABOVE the action buttons; should be at the BOTTOM
Like Captains of the Guard, the roster list belongs after the button strip, not before.

## B11 — Harem women list rows slightly squashed
Same as B9 — bump row height to match the Guard panel.

## B12 — Palace Eunuch characters lack the eunuch trait
The minted eunuchs (QING_household_mint_eunuch) don't carry the eunuch/castrated trait.

## B13 (fixed) — confucianism showed raw generic-deity keys
Excluded confucianism from the 8 generic region1 deities (00_generic.txt) so only the 12 themed
Qing deities show. DONE.

## B14 — pops starving in Yongzhou (203/64) + Hengyang (258/124): raise pop capacity drastically
Same class as #9 (over-capacity prefectures). Extend the QING_boot_relieve mechanism to these 2 provinces.

## B3 — Treasure Fleet: triggers all valid (num_of_ships/num_of_port_building/is_port proven in oracle).
Definition confirmed valid by 2 agents. Applying `final = yes` on the capstone as the best remaining
hypothesis (the boot log warns missions "lack a final task"); noting uncertainty since visible sibling
xinjiang also lacks it.

## B15 — Colonize + "Establish an Overseas Colony" buttons both greyed out
Both appear on an unowned island but are disabled. Actions: (a) double-check vanilla Colonize
requirements (may be legit); (b) "Establish an Overseas Colony" (capitalize thus) should NOT be greyed
for the islands being selected — the #18 button's is_valid is too strict. NEEDS INVESTIGATION.

## B16 — Overseas-colony pops conjured from thin air; should come from real crowded provinces
The #18 colonise effect create_state_pop's new tribesmen; instead it should DRAW pops from real
(over-capacity) source provinces — tie into the migration source model.

## B17 — US still disconnected: research whether provinces 5204 and 1154 should be empty/unowned in 1763
Historical check like #16. DONE-flag pending research.

## Holy sites (B7 follow-on) — added the 4 missing custom-deity holy sites
deity_xuanwu→Shiyan 7249 (Wudang), deity_nezha→Chengdu 3537, deity_caishen→Suzhou 2588,
deity_tudigong→Baoding 5213. (Beijing 8363 already holds deity_shangdi.) DONE.

## B18 — French Louisiana main chunk = exactly modern-Louisiana shape (wrong); research 1763 extent
The extra disconnected provinces may be fine, but the core is shaped like the modern US state, not the
vast 1763 Louisiana. NOTE: in 1763 France ceded Louisiana to SPAIN (secret Treaty of Fontainebleau
1762 / Paris 1763) — so a FRENCH Louisiana at a Feb-1763 start is itself historically suspect. Research
the real 1763 controlled extent + correct owner. NEEDS RESEARCH.
RESEARCH DONE (agent a9e0b3cc) + VERIFIED IN SETUP → RESOLVED (no change). LSA already IS a Spanish
subject = the historically-correct 1763 owner (Fontainebleau 1762). The agent recommended adding the
Arkansas River-valley posts (1804 5826 5832 6176 7458 7476 7776 9911 9915 9987 10062 10077) to LSA, but
a setup check shows THOSE PROVINCES ARE ALREADY OWNED by the Caddo (CDD own_control_core, 00_default.txt
:35372) — a deliberate boot #16 decision to give the trans-Mississippi interior to Native nations.
Adding them to LSA would be a fatal double-assignment. The "modern-Louisiana shape" is therefore the
INTENDED footprint, not a bug: Spanish Louisiana's controlled riverine posts (already extended up the
west bank to St. Louis per boot #15) with the plains interior left to Caddo/Osage. Owner correct,
footprint deliberate → nothing to fix. (Illinois-Country-east-bank→GBR is a separate possible
enhancement, not the reported bug.)

# ======================================================================
# ROUND 2 (this boot test) — new reports
# ======================================================================

## B19 — Character-window court-position title row completely absent
The f867bcb69 subtitle row (names the GC office / sub-post under a character's name) shows for NO
character — not Grand Council office-holders, not sub-post holders. Static-clean (loc keys exist, marker
vars are set by the office/subpost effects, Or()-IsSet + Custom() idioms individually proven elsewhere),
so this is the "static-clean but broken" trap. PLAN: rebuild the visible-gate as a proven
ScriptedGui.IsShown gate (a new qing_has_court_position char-scope scripted_gui) instead of the
hand-rolled 8-way Or() chain, and give the textbox an explicit fixed size like the working incumbent
marker (imp19c_windows.gui:110). NEEDS FIX.

## B20 — Some Zongli Yamen diplomats are ALSO commanders → breaks the 1:1 position mapping
A courtier can hold the qing_zongli_diplomat sub-post AND be an army/navy commander at once, so the
"one man, one court position" rule I was told to enforce is violated. The subpost fill/eligibility
gate (QING_subpost_eligible_candidate) must exclude is_general/is_admiral (and the sweep should
release a diplomat who later takes a command). NEEDS FIX.

## B21 — School icon in the Outliner "Building Constructions" queue is a broken placeholder
The construction-queue entry for a school building shows gfx/interface/placeholder.dds instead of the
proper school building icon. Likely a missing/placeholder construction-icon mapping for the school
building type in the outliner build-queue widget. NEEDS INVESTIGATION.

## B22 (feature request) — "Dispatch Diplomat" button on each Great Power row (Great Game screen)
Diplomats should be dispatchable to a Great Power to SOOTHE it and reduce tension modestly (not zero it
out). Add a "Dispatch Diplomat" button in each Great Power's row on the Great Game screen; consumes /
occupies a Zongli diplomat, applies a modest one-shot tension reduction to that power. NEW FEATURE.
