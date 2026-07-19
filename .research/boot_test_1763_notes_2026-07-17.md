# 1763_bookmark boot-test findings — captured 2026-07-15

Branch under test: **1763_bookmark @ a1d9b5675** (local, ahead of origin).
Captured live during a boot test. NO code changed during capture.

Triage order suggestion: **loc-load cluster (#2–#7) first** — likely one root cause (BOM/parse-halt regression) covers most of them.

---

## Findings

### #1 — Economy: starvation amid State food surplus  (functional + cosmetic)
Many pops starving in provinces whose owning **State has nonzero (sometimes a lot of) food**.
- Sub-item (cosmetic, EXPECTED): food is localized as **"Amenities"** (mod renames base-game food trade-good category; `imp19c_tradegoods_l_english.yml` TRADE_GOODS_CATEGORY_1 = "@food_icon! Amenities"). Underlying resource is still food.
- Real bug: likely the known **famine-amid-surplus / physical-deficit-svalue** class (see memory imp19c-1763-economy-log-floods). Territory-level physical deficit triggers starvation while province/State amenities storage stays positive → stored food not reaching starving territory's pops. Check partial-ownership effectiveness cut (ONLY_OWN_N_TERRITORIES) + granary seeding (#22/#23) actually feeding these territories.

### #2 — Grand Council panel: many broken localizations (raw keys), previously working  (broken text, REGRESSION)
### #3 — Southern Study: `QING_SS_OPEN_BTN` raw key on button, was working  (broken text, REGRESSION)
### #4 — Court Intrigue: `QING_PRINCES_OPEN_BTN` raw key on button, was working  (broken text, REGRESSION)
### #6 — Ministries: loc broken on **Personnel / Revenue / Rites** buttons ONLY; other ministries fine  (broken text, REGRESSION)
### #7 — Broken loc extends INSIDE the windows those buttons open, not just the labels  (broken text)
**CLUSTER #2/#3/#4/#6/#7:** button labels AND full window bodies show raw keys, across Grand Council / Southern Study / Court Intrigue / Personnel-Revenue-Rites — but OTHER ministries render fine. Strongly suggests specific .yml file(s) or contiguous key blocks failing to load — likely a **BOM/parse-halt regression** from a recent commit (candidates: #34 keju, #4 table reformat). One root cause probably covers most. HIGHEST-VALUE first investigation.

### #5 — Court Intrigue button misplaced  (layout)
Currently sits **below** the Southern Study button; should be **to the RIGHT** of it. (gui/government_view.gui ~2610–2643; put the two buttons in a horizontal flowcontainer.)

### #8 — "Propose a Marriage" still broken — REOPEN Task #2  (functional + layout)
Opens a **black box** (no content) and still has a **giant gray box spilling off the right side**. Should show content and not spill over.

### #9 — Harem: "Favour a Consort" / "Promote a Consort" don't let player pick  (functional)
Effect applies to a seemingly RANDOM consort. Both should open a click-to-select picker window (same proven template as "Take a Court Woman as Consort" / #29).

### #10 — Harem: "Take a Court Woman as Consort" header + placement + wording  (layout + wording)
- Remove the **redundant header** directly above the button.
- Move the button to sit **under the "Promote a Consort" button**.
- Reword button text to just **"Take a New Consort"**.

### #11 — Harem: consort picker filter should include imprisoned women  (filter)
Filter "living, unmarried, adult women" should ALSO include those who are **imprisoned** (don't gate out is_imprisoned). Apply across all consort pickers (also #9 once Favour/Promote use the same template).

### #12 — Ministry panels: performance progress bar broken  (broken UI)
On ALL ministry panels the performance **progress bar** is a **tiny green bar regardless** of value. Likely value-scale mismatch (0–100 vs 0.0–1.0; missing Multiply_CFixedPoint( …, '(CFixedPoint)0.01' )) or wrong/unset var. Possibly a #4 side-effect. Compare to a working panel's progressbar.

### #13 — "Accuse an Official" needs a cost  (balance)
Should **cost political influence** + carry a **small tyranny penalty**. Also gate is_valid on affording the influence.

### #14 — "Accuse an Official" should strip position instead of exempting  (design)
Protected officials currently exempt (vanilla Bring-to-Trial restriction). Instead:
- **Ministers** → remove from office, then accuse
- **Commanders** → remove from command, then accuse
- **Governors** → remove governorship, then accuse
- **Imperial House** → CANNOT strip (position of birth). If a vanilla restriction blocks accusing Imperial House members, it's FINE to leave them unaccusable — no workaround. Just confirm whether such a restriction actually exists.

### #15 — Religion window ("Faith & Sedition") broken  (functional)
Empty header, no content below, and **clicking on it does nothing** (non-interactive). Panel body not rendering + dead interaction. May relate to loc cluster #2–#7.

---

## Clusters for triage
- **Loc-load failures:** #2, #3, #4, #6, #7 (probably one root cause — check .yml BOM + first-error line per broken feature file).
- **Harem:** #9, #10, #11 (all #29 panel).
- **Accuse an Official:** #13, #14 (Task #6 follow-ups).
- **Reopen Task #2:** #8.
- **#4 side-effects candidates:** #12 (progress bars), maybe loc cluster.

---
## #38 LEAD (marriage_play_window.gui:118 & 167 — 'down' parse failure)
error.log: `Failed parsing data statement 'And( ...GetVariable('marriage_play_our_pick').IsSet, EqualTo_int32( Character.GetId, ...GetCharacter.GetId ) )' for property 'down'`.
- The list_button at :117/:166 OVERRIDES datacontext to `[GetScriptedGui('marriage_play_pick_own'/'_their')]`. `Character.GetId` in the `down=` can't bind against a ScriptedGui root → parse fail.
- WORKING analogue diplomatic_view.gui:2391 uses the identical And/EqualTo_int32 idiom but for `Country` and on a widget where the Country datacontext is intact (no scriptedgui override on the same node).
- `.GetVariable('x').GetCharacter` itself IS valid (characterwindow.gui:636 parses).
- LIKELY FIX: move the scriptedgui datacontext off the node carrying `down=`, or reference the char via the parent widget's `Scope.GetCharacter` context explicitly, so both `Character` (row char) and the picked-char comparison resolve. Verify against the #29 harem picker's selected-highlight idiom.
