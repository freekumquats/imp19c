# 1763 Boot-Test Bugs — 2026-07-11 playtest

Branch under test: **1763_bookmark** (head `cf688030`, UNCHANGED since 2026-07-10 — none of the overnight `overnight-312-315-audits` work is included). Start: Qing (CHI), 1763.2.16.

Fixes for everything here land on **1763_bookmark**.

Legend: **REGRESSION-N** = a bug from the prior (2026-07-10) batch that was thought fixed but is NOT; **N** = newly observed this test.

---

## REGRESSION-B21 — Qing armies still all stacked on Beijing
- **Observed:** at start, the entire Qing order of battle (all ~27 banner + Green Standard garrisons) is piled on Beijing, NOT dispersed to Xi'an / Ili / Mukden / Chengdu / Canton / Fuzhou / Ningxia / Kashgar / etc.
- **History of the fix (CORRECTED via `git log -S` — the oscillation was a single bad round-trip, NOT 4 failures):**
  1. original: `raise_legion` wrapper → musters at the governorship SEAT, ignores location → all at Beijing.
  2. `fdc207b3`→`ee44b72a` (FOUR consecutive commits): `$prov$ = { owner = { create_unit { location = $prov$ } } }` — the ABSOLUTE province token. **This form was stable and is the CORRECT one.**
  3. `d42deb74` (boot pt2, my prior commit): I changed the absolute token → `location = prev.prev` on a misread of the Invictus naval pattern. **THIS is the build the user boot-tested** (`d42deb74` is an ancestor of the tested head `cf688030`, confirmed via `git merge-base --is-ancestor`). `prev.prev` at the owner scope = ROOT's capital = Beijing → the stack. So the regression was introduced by `d42deb74`, not by any earlier attempt.
  4. `c6d04a26` (this fix): REVERTED to the absolute token that was stable for the four commits before `d42deb74`. A revert to a proven idiom, not a new blind variant.
- **File:** `common/scripted_effects/imp19c_effects_legion_setup.txt` — `SE_qing_raise_garrison` (line ~94) + `SE_qing_raise_garrison_cmd` (line ~135). Raised from `SE_qing_armies`, fired via `qing_force_setup.1`.
- **✅ ROOT CAUSE FOUND + FIXED (B21-v3 — supersedes v1/v2; the user confirmed it was ALWAYS broken, incl. the absolute-token builds).** So the location TOKEN was never the fix. Oracle diagnosis (2026-07-11, HIGH confidence, 3 parallel investigations vs Invictus/vanilla) found the load-bearing bug is the **`$prov$ = { owner = { create_unit } }` PROVINCE→OWNER wrapper itself**: entering the country scope THROUGH a province scope makes the new unit's placement re-resolve against the scope-entry context (collapsing to ROOT's capital = Beijing) instead of honouring the absolute `location` token. Every proven reference spawn issues create_unit **DIRECTLY in a bare country scope** with an absolute `location = p:X` token and NEVER via `p:X = { owner = { } }` — Invictus `invasions.2` (2 land units, 1 tick, bare country scope), `galatian_invasion.10` (`create_unit { navy=no location=p:384 }`), `me_tasm.13` (3 navies at 3 ports, 1 tick), vanilla `me_duuchuu.5` (12 navies, 1 tick). Commander is NOT required (commanderless creates outnumber commanded 203:66 in Invictus and persist). **FIX:** `SE_qing_raise_garrison`/`_cmd` now do `$prov$ = { owner = { save_scope_as = garrison_owner } }` then `scope:garrison_owner = { create_unit { navy=no location=$prov$ ... } }` — a BARE country scope (c:CHI, or the frontier SUBJECT that owns the province), absolute location token, no province→owner wrapper. Adversarially reviewed → 0 findings.
- **Severity:** MAJOR — RESOLVED (pending boot-test confirmation). ⚠️ This is the FIRST time the actual wrapper (not the token) was addressed; all prior "fixes" (incl. c6d04a26) only changed the token and left the wrapper, so they never worked.
- **❌ BOOT-TEST 2026-07-10 (build c7cc248d): STILL BROKEN.** User: "I see 22 armies stacked on Beijing, none of which have commanders." So the v3 wrapper-removal fix ALSO failed — IDENTICAL symptom to every prior build. TWO independent code theories (v1 location-token, v3 wrapper-removal) now produce the EXACT same result → both falsified. Plus a NEW datapoint: **no commanders attach either.** The `commander = $cmd$` inline field is also being ignored at `on_game_initialized`. Conclusion forming: at game-init time `create_unit` honours NEITHER `location=` NOR `commander=` for these land units — the problem is likely the FIRING CONTEXT (on_game_initialized), not the scope idiom. STOP blind-coding scope variants. Need the DECISIVE artifact (see below) before the next attempt.

---
- **🔑 NEW RUNTIME CLUE (boot-test 2026-07-10):** User: "I don't see any other [non-Qing] armies raised, though I did see some armies popping up in Qing vassals (this is probably the same garrison script) — however they are gone now, not sure if AI manually disbanded them or a bug." IMPLICATIONS: (a) garrisons raised in SUBJECT-owned frontier provinces (Ili p:3534 etc. via the scope:garrison_owner = <subject> branch) DID appear AT THE CORRECT PROVINCE — so `location = p:X` WAS honoured there, partially CONTRADICTING the "engine ignores location" theory; (b) they then DISAPPEARED — so the real mechanism may be post-creation CULLING/DISBAND, not misplacement. That reframes B21/B22: units are created (some at the right place), then merged/relocated/disbanded. Suspects to check in logs: the SE_qing_navy_disband `every_navy = { destroy_unit }` (does an analogous army-disband exist / does every_navy catch land units?); AI vassal auto-disband of a handed-down legion it can't afford; or the units being created UNDER the subject (owner=subject) then culled when the subject can't support them. The Qing's OWN units piling at Beijing may be a DIFFERENT facet (created in c:CHI scope, placement collapses to capital) than the vassal units (created under subject, placed right, then culled). DIAGNOSE FROM debug.log LOG_line markers — do NOT blind-fix.

## REGRESSION-B22 — only the Fujian water-force spawns; Guangdong + Zhejiang still missing
- **Observed:** at start only **福建水師 (Fujian Coastal Patrol)** exists. The **廣東水師 (Guangdong, Canton p:9298)** and **浙江水師 (Zhejiang, Ningbo p:2893)** squadrons do NOT appear (same symptom as before the "fix").
- **History of the fix (also multiple failed attempts):** country-scope `create_unit { navy=yes location=p:X }` → spawned only one. Current on 1763_bookmark: three separate effects (`SE_qing_navy_guangdong` / `_fujian` / `_zhejiang`) each `p:X = { owner = { create_unit { navy=yes location = prev.prev } } }`, all fired ONE tick in `qing_force_setup.11` after a day-3 `SE_qing_navy_disband` (`every_navy = { destroy_unit }`). → **STILL only Fujian (this test).**
- **File:** `common/scripted_effects/imp19c_effects_legion_setup.txt` — `SE_qing_navy_guangdong` (~360), `_fujian`, `_zhejiang`, `SE_qing_navy_disband` (~334). Wired via `qing_force_setup.10` (disband) + `.11` (raise all three).
- **✅ ROOT CAUSE FOUND + FIXED (B22-v3 — SAME wrapper bug as B21; supersedes v2).** debug.log proved all 3 navy scripts SUCCEED (each logs "raised" at a valid port) yet only Fujian survives — the units are created then merged/culled, not failed. The culprit is the **`p:X = { owner = { create_unit } }` province→owner wrapper** (see B21), which collapses all 3 hulls' placement so the engine keeps only the last. **FIX:** all 3 squadrons (main + fallback branches) now create in a **bare `c:CHI` scope** — `c:CHI = { create_unit { navy=yes location=p:9298/p:3651/p:2893 ... } }` (fallbacks use `location = scope:qing_*_fallback_port`), verbatim the Invictus `me_tasm.13` idiom (3 commanderless navies at 3 ports, one tick, bare country scope — all persist). No owner wrapper, no commander, no stagger needed. Adversarially reviewed → 0 findings. (The location-token and same-tick theories were both wrong; the wrapper was always the bug.)
- **Severity:** MAJOR — RESOLVED (pending boot-test confirmation).
- **❌ BOOT-TEST 2026-07-10 (build c7cc248d): STILL BROKEN.** User: "Fujian coastal patrol is the only navy, also no commander." Same symptom as every prior build + no commander. Same root class as B21 — the v3 bare-c:CHI-scope fix did NOT work. Firing context (on_game_initialized) is the prime suspect, not the scope idiom.

- **🔑 CLUE REFINED (same test):** User: "I believe they appeared in subject CAPITAL cities, though I'm not sure." If the vassal garrisons landed at the SUBJECT'S CAPITAL (not the target frontier province Ili p:3534 etc.), then `location = p:X` was NOT honoured in the subject branch either — placement collapsed to the scope-owner's capital, EXACTLY like the Qing units collapsing to Beijing. So it is ONE consistent bug after all: **create_unit places the unit at the SCOPE OWNER'S CAPITAL and ignores the `location` token** — for c:CHI that's Beijing, for scope:garrison_owner=<subject> that's the subject's capital. This RESURRECTS the location-ignored theory (now confirmed in BOTH scopes) and means the "wrapper removal" (v3) genuinely did not change engine behaviour. The vanishing afterward is a SECOND effect (AI subject disbanding a legion it didn't order / can't afford, OR the disband sweep). Two things to confirm in debug.log: (1) the LOG_line says "raised at p:3534" while the unit actually sits at the subject capital = location ignored; (2) whether a later tick logs a disband. STILL do not blind-fix — but the leading hypothesis is now: create_unit at game-init ignores location= entirely (a known-hard Imperator limitation), and the real fix is likely a DIFFERENT placement mechanism (raise_legion at a province-scoped governorship, or a dated/on_action deferred raise rather than on_game_initialized).

---

## REGRESSION-B7 — Grand Council "Appoint" button does nothing
- **Observed:** in the Grand Council / Government view, clicking **Appoint** on a great office does NOTHING — no candidate-picker window opens. Expected: a window listing eligible candidate courtiers (incl. sitting ministers, for reshuffle).
- **Prior status:** B7 was on the 2026-07-10 list as "wiring OK = runtime" (my audit memory said the dead-GUI audit cleared B7 as a runtime issue, not dead wiring). This test shows it is STILL broken at runtime on 1763_bookmark.
- **✅ ROOT CAUSE = THE SAME CORRUPTED BOM AS B14 — FIXED.** `error.log`: `Could not find widget 'qing_office_picker_window' in 'gui/imp19c_windows.gui'`. The picker window IS defined (imp19c_windows.gui:37) and the Appoint onclick (`gui.createwidget gui/imp19c_windows.gui qing_office_picker_window`, government_view.gui:2634 etc.) is correct — but the double-encoded BOM at the top of imp19c_windows.gui broke parsing at line 1, so `qing_office_picker_window` never registered → createwidget found nothing → click did nothing. The BOM repair (see B14 entry) restores it. **B7 + B14 share the one fix; nothing else needed.**
- **Severity:** MAJOR — RESOLVED by the BOM repair.
- **⚠️ BOOT-TEST 2026-07-10 (build c7cc248d): WINDOW OPENS (BOM fix WORKED), but NEW layout bug.** User: "the character list is displayed horizontally and cut off on the right side. It should instead be displayed vertically, and scrollable." CAUSE: gui/imp19c_windows.gui:71-73 the candidate list uses `dynamicgridbox { datamodel_wrap = 1 }` which flows items into a horizontal GRID row → clips on the right. FIX: render as a vertical scrollable list (vbox/flowcontainer direction=vertical + datamodel, or dynamicgridbox with proper vertical flow). Tracked as B7-layout.

---

## 1 — Throne section: Statesmanship bars clipped by the Dynastic Health section
- **Observed:** in the Grand Council / Government view, the **"The Throne"** section and the **"Dynastic Health"** section are too close vertically — the **Statesmanship bars for the three Throne positions** (Emperor / Empress? / Crown Prince, or the three summit seats) are NOT visible; they are clipped/overlapped by the Dynastic Health block below.
- **Fix:** add vertical space between the two sections — increase the spacing/margin/offset (or the Throne container's min height) so the three Statesmanship bars render fully before Dynastic Health begins.
- **File(s):** `gui/government_view.gui` — the "The Throne" container and the "Dynastic Health" container; look for the flowcontainer spacing / a fixed size that's too short to fit the three bars, or a following block positioned with a hardcoded offset that overlaps.
- **Severity:** MINOR (layout/readability — data is there, just not shown).
- **NOTE:** this is a NEW section vs the 2026-07-10 layout — likely introduced by the B10 Edicts-strip reorg or the develop GC restructure (Empress seat / relocated Regent+Emeritus). Check what pushed the Throne block's height.
- **⚠️ BOOT-TEST 2026-07-10 (build c7cc248d): SPACING FIXED, but NEW sub-bug.** User: "the Dynastic Health section was successfully moved down and I see the bottom of the three boxes (Emperor, Crown Prince, Empress) but curiously there is no statesmanship bar displayed for any of them." + "all three boxes should display a statesmanship bar the same way as shown by the Grand Chancellor box." FIX: give the Emperor/Crown-Prince/Empress boxes the SAME statesmanship-bar widget the Grand Chancellor box uses (copy that box's bar block). Tracked as Bug1-throne-bars. ALSO (same three boxes, same test): the Martial/Finesse/Charisma/Zeal ICONS render but with NO number beside each — the skill VALUE textbox is missing/empty. User: "they should display each character's values." Almost certainly the SAME root cause (the three boxes lack the content widgets the Grand Chancellor box has). Fix both together by mirroring the Grand Chancellor box's stat + bar widgets.

---

## 2 — Council effectiveness shown twice (bar + number); keep only the bar, number on hover
- **Observed:** in the Grand Council view, **council effectiveness** is displayed BOTH as a progress bar AND as a separate numeric readout. Redundant.
- **Wanted:** show it as the **bar ONLY**; the exact numeric value should appear in the bar's **tooltip (on hover)**, not as a standing number beside it.
- **Fix:** remove the standalone numeric text widget; move its value into the bar's `tooltip`. Keep the bar's `progresstexture`/value binding as-is.
- **TOOLTIP FORMAT (from user):** currently the hover reads *"Council effectiveness (0-100)....."*. It should read:
  **`Council Effectiveness: [current value]/100. [description text follows]`**
  i.e. lead with the label + the LIVE value out of 100 (bind `qing_council_effectiveness` via `GetVariable(...)|0`), then the descriptive text. Drop the "(0-100)" range annotation from the lead.
- **File(s):** `gui/government_view.gui` — the council-effectiveness bar + the adjacent number widget (search for `qing_council_effectiveness` bindings). Loc key for the tooltip: prepend `Council Effectiveness: [.../100].` then keep the existing description; put the value token in the loc string (Paradox `[Scope.MakeScope.GetVariable('qing_council_effectiveness').GetValue|0]`) or as a `$VAL$` data-substitution.
- **Severity:** MINOR (cosmetic/de-clutter + tooltip wording).

---
- **✅ BOOT-TEST 2026-07-10 (build c7cc248d): FIXED — CONFIRMED.** User: "Bug 2 is fixed."

## REGRESSION-B12 — Royal Marriage / Dynastic Match window opens but the candidate list is EMPTY
- **Observed:** the **Dynastic Match** window now OPENS (so the B14-style window-culling is fixed), but the candidate list inside is **empty** — no foreign houses shown.
- **Prior theory (2026-07-10):** B12 "was expected to fix itself once real rulers with children load (B1/B2)." This test shows it is STILL empty → either B1/B2 is not fully fixed at the 1763 start, OR the emptiness has a different cause.
- **File:** `common/scripted_guis/MARRIAGE_actions.txt` — `marriage_open_candidates` (builds the `marriage_candidates` variable-list via `every_country`); window `gui/marriage_window.gui` reads `datamodel = "[Player.MakeScope.GetList('marriage_candidates')]"`.
- **The candidate `every_country` limit requires ALL of:** `exists = current_ruler`, `MARRIAGE_eligible_realm_trigger` (dynastic monarchy, not-subject, num_of_cities≥1), `ROOT = { in_diplomatic_range = prev }`, AND `current_ruler = { any_child = { is_alive=yes is_married=no prisoner=no } }`.
- **LEADS (rank by likelihood):**
  1. **Diplomatic range.** At a 1763 Qing start the empire is isolationist — `in_diplomatic_range` may exclude the European dynastic houses entirely, leaving only near neighbours (which may be tribes/republics/subjects that fail `MARRIAGE_eligible_realm_trigger`, or lack an eligible child). If so, the list is legitimately empty by the range gate. **Check debug.log for the "candidate-list window opened" LOG_line and whether any add_to_variable_list fired.** Consider whether CHI should see out-of-range houses in this window (the marriage window may need to relax `in_diplomatic_range`, since a dynastic match is a reason to open relations).
  2. **Childless rulers (B1/B2 residue).** If neighbouring monarchies' rulers still load without children at 1763, the `any_child` test fails for all of them. Cross-check with whether B1/B2 (ruler data) actually holds in THIS test — verify a few neighbours (Korea, Vietnam, Burma, the Central Asian khanates) have real rulers WITH children.
  3. **narrow_monarchy_trigger** may exclude the East/Central-Asian monarchies (khanates, the Tibetan/Nepalese states) if it's tuned to European monarchy government types — so even in-range neighbours fail eligibility. Inspect what `narrow_monarchy_trigger` accepts.
- **✅ ROOT CAUSE CONFIRMED (via debug.log) + FIXED (#330).** debug.log shows the builder fired (5× "candidate-list window opened by") but added nobody → the `every_country` limit rejected all. Two structural causes for an isolationist 1763 Qing, both now addressed: (1) **`in_diplomatic_range`** excluded essentially every dynastic house (the isolationist Qing reaches almost no European/distant court) — **DROPPED** from the candidate builder (a marriage overture is itself a reason to open relations; the propose/betroth ACTIONS keep their own range check so an unreachable match is shown-but-gated). (2) **`is_subject = no`** (inside `MARRIAGE_eligible_realm_trigger`) excluded the Qing's own tributary monarchies (Korea/Vietnam/the khanates) — the builder + propose + betroth now use a new **`MARRIAGE_candidate_realm_trigger`** = an eligible realm OR **ROOT's own subject monarchy**, so tributaries appear (per the user's "also allow subjects" decision + the marry-into-subject tightens-ties feature #330). Also relies on the #329 death_date ruler fix so real rulers with real children now load. **File:** `common/scripted_triggers/00_marriage_triggers.txt` (new trigger), `common/scripted_guis/MARRIAGE_actions.txt` (builder + actions).
- **Severity:** MAJOR — RESOLVED (pending boot-test).

---
- **❌ BOOT-TEST 2026-07-10 (build c7cc248d): WORSE — 3 symptoms.** User: "B12 is broken and weirder than ever, no candidates are displayed and now Our House shows minor_chi instead of the previous (and correct) Aisin Gioro. Also the old number for Marriage Power has been replaced by the literal text 'Marriage Power' instead of the correct 'Marriage Power: [value]'."
  1. **No candidates** (still empty) — the core B12. Awaiting logs to see whether the builder loop iterates (per-candidate LOG lines) or the ruler-data cascade (B1/B2) still yields childless neighbours.
  2. **"Our House" = `minor_chi`** — `minor_chi` = the engine's auto-generated `minor_<tag>` family, shown when the read character has NO family_name. char:214 (Qianlong) IS correctly `set_as_ruler=char:214` with `family_name="Aisin Gioro"` (death_date stripped), so the marriage window's "Our House" is reading a DIFFERENT character than the seated ruler (a scope/data problem, NOT loc). DIAGNOSE FROM LOGS — do not blind-fix. Possible link to the missing-commanders / mis-seated-character class (B21/B22).
  3. **"Marriage Power" literal, no value** — this is the Bug 3 fix (MARRIAGE_WINDOW_POWER_LABEL="Marriage Power", value moved to hover tooltip MARRIAGE_WINDOW_POWER_TT). User wants the value INLINE: "Marriage Power: [value]". RECONCILE Bug 3 (remove stray raw number) with this (labelled inline value) — change the label cell to show `Marriage Power: [Country.MakeScope.Var('marriage_display_power').GetValue|0]` (marriage_window.gui:169 already reads that var; fold it into the label text). Standalone loc/gui fix, not log-gated.

## 3 — Marriage window own-house row shows a stray raw number (e.g. "21447") on the far right
- **Observed:** in the Dynastic Match window, the own-house row reads **"Our House: Aisin Gioro"** (correct) but a bare number (**21447**) is displayed at the far RIGHT of the same row. Should not be shown.
- **ROOT CAUSE (found in code):** `gui/marriage_window.gui`, the own-house header — a second `textbox` (size `{120 100%}`, align right) binds `text = "[Player.MakeScope.Var('marriage_display_power').GetValue|0]"`. That raw great-power score is the "21447". Worse: `marriage_display_power` is only `set_variable`'d on CANDIDATE countries inside the `marriage_open_candidates` `every_country` loop — it is **never cached on the player's OWN realm**, so this readout is a stale/garbage value, not even the player's real power.
- **Fix (per the same design principle as Bug 2 — value belongs in the tooltip, not as a bare number):** remove the bare right-aligned number from the own-house header row.
- **KEEP a live own-power figure ON HOVER (user):** yes, surface it in the tooltip, but it MUST be labelled with context — **"Marriage Power"**, and explicitly **of our House of Aisin Gioro** (the ruling-house name), otherwise the number is meaningless. So the tooltip should read something like:
  **`Marriage Power of the House of [Player.GetRuler.GetFamily.GetName]: [value]`** followed by the existing explanation of what marriage power means.
- **Implementation:** (1) cache the own value — add `set_variable = { name = marriage_display_power  value = DIPLOMACY_power }` on ROOT at the top of `marriage_open_candidates` (it's currently only set on candidates, never on ROOT — that's why the bare readout was garbage). (2) remove the right-aligned `{120 100%}` power `textbox` (or keep an icon/label only, NOT the bare number) and move the value into `MARRIAGE_WINDOW_POWER_TT`, rewording that loc key to lead with "Marriage Power of the House of [house name]: [value]".
- **File(s):** `gui/marriage_window.gui` (own-house header, ~line 66-72 + the `MARRIAGE_WINDOW_POWER_TT` tooltip binding); `common/scripted_guis/MARRIAGE_actions.txt` (`marriage_open_candidates` — cache own power on ROOT); `localization/english/marriage_l_english.yml` (`MARRIAGE_WINDOW_POWER_TT` reword with the House name + value token).
- **Severity:** MINOR (cosmetic + missing context; also currently displays a meaningless/stale value).

---

## REGRESSION-B14 — Supranational (diplomatic-play) window STILL does not open
- **Observed:** clicking the **Supranational** icon still opens NO window at the 1763 Qing start.
- **What the "fix" (`0b1bc66f`) did:** diagnosed the cause as the window-root `datacontext = Player...member_of_federation.GetProvince` resolving null when the player is not in a federation → engine culls the window. It RELOCATED that Province datacontext off the window root onto the federation-tab flowcontainer (confirmed: `Province.MakeScope` now appears only at line ~347, inside the federation subtree). → **STILL no window (this test).** So the null-datacontext-culling theory was WRONG or INCOMPLETE.
- **File:** `gui/imp19c_windows.gui` — `type supranational = base_window` (~line 410).
- **✅ ROOT CAUSE FOUND + FIXED (via error.log): CORRUPTED BOM broke the whole file.** `error.log` shows `gui/imp19c_windows.gui:4 - '=' is not a valid widget/property` and `'ï»¿' is not a valid widget/property`. The file's first bytes were `c3 af c2 bb c2 bf` — a **double-encoded UTF-8 BOM** (the real BOM `EF BB BF` got re-encoded to the mojibake `ï»¿`). The engine read `ï»¿#...` as content, broke parsing at line 1, and **every window `type` in the file failed to register** — including `supranational` (topbar: `ingame_topbar.gui:1630 - 'supranational' is not a valid widget/property`) AND `qing_office_picker_window` (B7). FIX: rewrote the leading 6 bytes to a proper single BOM `EF BB BF`; file now decodes clean (utf-8-sig), braces 379/379, all window types intact. **This one repair fixes B14 AND B7.** (The user's recollection that it "worked until the diplomatic-play-initiation change" is CONFIRMED: commit **d623041d** "Grand Council eligibility/exclusivity + subject-action & play-button GUI fixes" is the one that rewrote `imp19c_windows.gui` (+188 lines) AND touched `province_window.gui`'s play buttons in the SAME commit — so the play-init edit and the BOM mangling landed together, exactly as the user remembered.) Scan of all *.gui/*.txt/*.yml found NO other file with this mojibake BOM — isolated.
- **Prior re-diagnosis notes (now moot for the parse break, kept for reference):**
  1. **Isolate opener vs window.** In-game, open the console and run `window.open supranational` (or the mod's exact widget name). If the window APPEARS via console but not via the icon → the bug is in the OPENER (the Supranational button's onclick in `outliner.gui` / `ingame_topbar.gui`), not the window. If it does NOT appear even via console → the window itself is still culled/erroring.
  2. **Check the topbar/outliner opener** for the Supranational button: is its `onclick`/`visible` gated on something false for the 1763 Qing (federation membership, a GP count, `is_at_war`, etc.)? The prior fix said "opener path was identical to upstream so not implicated" — but if console-open works, the opener IS the culprit and that assumption was wrong.
  3. **Re-scan the window for ANY OTHER unresolved datacontext/scope** that culls it (not just the relocated federation one) — e.g. `on_start` `GetVariableSystem.Set('supranational_tabs', ...)`, a `[Scope.GetCharacter]` (line 78) or `host_tag.GetCountry` (line 347) resolving null on the default tab, or a global-power datamodel that's empty for an isolationist Qing.
  4. **Grep error.log / debug.log** for the widget name — a GUI parse/scope error on open would be logged.
- **Severity:** MAJOR (the whole diplomatic-play / GP-rivalry surface is inaccessible; #52/#108 content is gated behind it).
- **NOTE:** get **error.log** + **debug.log** for this session — several of these (B14, B22, B12) hinge on runtime markers/parse errors that script-reading alone cannot resolve. This is the single most valuable artifact for the fix pass.

*(A reported "Tribute S/M/L buttons inert" was investigated and withdrawn — the buttons were merely greyed by the 25-political-influence `is_valid` gate at a low-PI start. Working as designed, NOT a bug.)*

---
- **✅ BOOT-TEST 2026-07-10 (build c7cc248d): FIXED — CONFIRMED.** User: "the Supranational window is opening properly now." The BOM repair resolved it (shared fix with B7, which also now opens).

## REGRESSION-B1/B2 (RUS) — Russia STILL shows the wrong ruler (Bulganin placeholder + infant Aleksandr I)
- **Observed:** at the 1763 start Russia's ruler is still the engine placeholder **Grigoriy Bulganin** and an **infant Aleksandr I Romanov** appears — NOT **Catherine II**, which the #320 fix was supposed to seat.
- **CONTROL (works):** the SAME fix pattern DID take for the **USA** — Madison/Jefferson no longer appear (correctly de-seated). So the ruler-fix mechanism works in general; it is failing specifically for RUS.
- **Code state (1763_bookmark, looks CORRECT on paper):** `setup/characters/00_Russian Empire.txt` char:144 = "Yekaterina II 'the Great'", birth 1729 / death 1796 (alive at 1763.2.16), with a `c:RUS = { set_as_ruler = char:144 }` block inside her definition (added by #320 / commit `33d45d36`). char:147 = Aleksandr I, birth **1777** (unborn at 1763).
- **THE TELL:** an **infant Aleksandr I (b.1777) cannot exist at a 1763 start from data alone** — his appearing means either (a) the whole RUS character block is being read against a LATER date context / a different setup path is overriding it, or (b) `set_as_ruler` here is not taking and the engine is falling back to its own generated line (Bulganin) plus surfacing Aleksandr from somewhere. This is NOT explicable by the character data, which is correct.
- **✅ ROOT CAUSE FOUND + FIXED (via error.log). It was SYSTEMIC, not RUS-specific.** error.log:
  `set_as_ruler effect [ Target Character ... Yekaterina II ... ( ID: 144 ) is not alive ]`. The SAME
  error fires for **Louis XV (FRA 406), Qianlong (CHI 214), Abdul Hamid (TUR 42)** — every historical
  ruler I seated via in-block `set_as_ruler` who carries a `death_date`. **The engine's setup snapshot
  treats ANY character bearing a `death_date` as already-dead when it evaluates `set_as_ruler`** — even
  though the death_date (1774/1796/1799/1789) is AFTER the 1763.2.16 start. So the effect no-ops and the
  engine auto-generates a placeholder line (Bulganin) + surfaces the next historical Romanov (the b.1777
  Aleksandr) as the heir. Confirmed idiom: **0 of 94 Invictus setup rulers carry a death_date** — a setup
  ruler must NOT have one; natural death is handled by the age/history system after load. **FIX:** removed
  the `death_date` field from all four ruler blocks (RUS 144, FRA 406, CHI 214, TUR 42). Runtime was
  correctly 1763 (the High Qing garrison branch `current_date < 1772.1.1` fired), so this was purely the
  death_date-in-setup rule, NOT a stale 1815 clock.
- **NOTE (why USA worked):** USA needed a DE-seat (remove Madison/Jefferson), which needs no `set_as_ruler`
  — that's why it took while the four death_dated rulers silently failed.
- **Severity:** MAJOR — RESOLVED for RUS/FRA/CHI/TUR (pending boot-test). Also unblocks B12 (a real ruler now
  loads with real children for the marriage market). **A SEPARATE bug (ID-range, see below) still leaves
  Poland's ruler unseated.**

---
- **BOOT-TEST 2026-07-10 (build c7cc248d): RUS half-fixed** (Catherine II now ruler ✅), but heir/Pavel death_date residue → see the death_date + no-family systemic entries below.
- **✅ OTHER RULER SPOT-CHECKS PASS:** FRA = Louis XV ✅, CHI = "Qianlong Emperor" ✅ (throne correct — note CHI's marriage-window "Our House = minor_chi" is a SEPARATE marriage-window family-read bug, not the ruler seating). Japan = Ieharu ✅ (see #5). POL ruler = August Wettin ✅ but wrong HEIR (see N-POL-HEIR / N-RULER-NO-FAMILY).

## NEW-B27 (from logs) — setup character ID-range violations leave ~28 chars UNCREATED (incl. Poland's ruler)
- **Observed (error.log):** `Character 730 in country POL should have id 572 or use create_character` — and 27 more:
  **CHI 700–729** (the anachronistic-figure roster), **POL 730, MRT 731, HYD 732, MYS 733, AWA 734, MLB 735,
  ERI 736, GDR 737, MEX 9232**. For each, the engine then throws `Failed to scope to character via ID 'N'`
  → `set_as_ruler [ target was null ]` (Poland line 19).
- **ROOT CAUSE:** the setup character loader assigns IDs from a **running global counter per country**; a
  hand-written id that exceeds the country's next-expected slot is **rejected — the character is NEVER
  created**. So any `set_as_ruler = char:730` (POL) scopes to null and POL falls back to an engine-gen ruler.
  This is distinct from the death_date bug: 730 dies 1763.10.05 (8 months AFTER start, i.e. alive at start)
  yet still fails — because it was never instantiated, not because it's "dead".
- **Scope of impact:** POL loses its historical ruler (Augustus III). The CHI 700–729 block is the
  anachronistic-spawn roster (characters summoned later by event) — if those are meant to be created at
  runtime via `create_character`, they should NOT be in setup at all; if meant to exist at start, they need
  in-range ids. MRT/HYD/MYS/AWA/etc. (Indian states) + MEX 9232 similarly lose seated characters.
- **✅ FIXED + COMMITTED (dadbf328).** Renumbered all 28 to their engine-expected sequential ids (700→553 … 9232→580) and updated every `char:<id>` reference; the setup id space is now contiguous 0–580. Adversarially reviewed → 0 findings. (Original deferral note kept below for context.)
- **FIX (original plan):** either (a) renumber these characters
  into their country's allocated id block (fragile — must match the exact expected counter), or (b) move the
  ones that are meant to be spawned-later out of setup and into a `create_character` in the relevant event
  (the engine's own suggested remedy: "or use create_character"). Poland's ruler (730) should be renumbered
  to an in-range id so `set_as_ruler` resolves. **Deferred — flag for user: this is a separate work item from
  the death_date ruler fix, touches many files, and the CHI 700–729 roster needs a design decision (setup vs
  event-spawn).**
- **Severity:** MAJOR for POL (wrong ruler); MEDIUM overall (mostly anachronistic-roster chars that may be
  event-spawned anyway — needs confirmation).

---

## 5 — Japan (TKG) shows "Tokugawa Yoshinobu" as ruler at 1763
- **Observed:** Japan's ruler at start reads **Tokugawa Yoshinobu** (the real LAST shogun, b.1837, r.1866-68) — an obvious anachronism at 1763.
- **DIAGNOSIS (important — likely NOT the same bug as RUS, may be working-as-designed):** "Yoshinobu" appears in the code ONLY in the japanese **namelist** (`common/cultures/00_japanese.txt`) and the bakumatsu events — there is **NO `set_as_ruler` seating him for TKG**. The TKG character file (`setup/characters/00_Japan.txt`) DELIBERATELY does not seat a start ruler: char 356 Tokugawa Ienari (b.1773) is unborn at 1763 and its comment says *"removed as set ruler to avoid the unborn-ruler boot error; engine generates a period-appropriate 1763 ruler."* So **the engine is generating a RANDOM Japanese ruler and happened to draw the given-name "Yoshinobu" + family "Tokugawa"** — a name-pool coincidence, not a stale reference to the historical figure.
- **So this is a DESIGN CHOICE reading as a bug:** TKG was intentionally left to engine-gen (no real 1763 shogun was seated). The fix is a JUDGEMENT CALL:
  - **(a)** Accept engine-gen (as designed) — but then it will occasionally draw jarring real-historical names. Acceptable if TKG is minor/background.
  - **(b)** Seat the HISTORICAL 1763 shogun — **Tokugawa Ieharu** (10th shogun, r.1760-1786) — as a proper character with `set_as_ruler`, the same fix pattern as RUS/FRA. This is the correct historical answer (Japan is a real 1763 power and the Bakumatsu arc #94 cares about the shogunate). RECOMMENDED.
- **✅ FIXED — option (b).** Repurposed the existing in-range `char:356` block (was the unborn Ienari,
  b.1773) into the actual 1763 shogun **Tokugawa Ieharu** (家治, 10th shogun, r.1760–1786, b.1737) and
  added `c:TKG = { set_as_ruler = char:356 }`. Carries **NO death_date** (per the RUS/FRA rule — a setup
  ruler with a death_date reads as already-dead). Reused char:356 rather than adding a new id to avoid the
  setup ID-range rule (see the ID-range bug below); succession seats the historical successors after his
  natural death via the age system.
- **File(s):** `setup/characters/00_Japan.txt` char:356.
- **Severity:** MINOR — RESOLVED (pending boot-test).

---
- **✅ BOOT-TEST 2026-07-10 (build c7cc248d): FIXED — CONFIRMED.** User: "Japan shows Tokugawa Ieharu." Ieharu = 10th shogun (r.1760-1786), CORRECT for the 1763.2.16 start. The setup now seats char:356 Ieharu explicitly (was auto-picking the anachronistic last-shogun Yoshinobu). Resolved.

## REGRESSION-B15 — Integrate/Loosen buttons STILL overlap the subject header/type labels
- **Observed:** in the diplomatic view → Subject Actions (Qing subject open), the **Integrate / Loosen** action buttons still render **on top of** the header + subject-type text, despite the B15 fix.
- **What the fix did (`gui/diplomatic_view.gui` ~line 1527-1560):** the `subject_actions_open` `vbox` had a header whose `autoresize=yes` gave it 0 layout height, so buttons stacked on top. Fix replaced it with a fixed-size `textbox` (`size {300 28}`, multiline) for `QING_SUBJECT_INTERACTIONS_HEADER`. → **STILL overlapping (this test)** → the fix addressed the HEADER textbox but not everything above the buttons.
- **LEADS (rank by likelihood):**
  1. **The `only_text` subject-TYPE widget** immediately below the fixed header (the big SelectLocalization block, `size {300 28}`) — `only_text` (like the old `autoresize` textbox) may NOT reserve layout height inside the vbox, so IT collapses to 0 and the buttons stack over it. The B15 fix converted the HEADER textbox but left the subject-type line as `only_text`. **Try: give the `only_text` an explicit reserved height / wrap it in a fixed-size `widget`, or convert it to a plain fixed-size `textbox` like the header.**
  2. **The integration-progress `widget` (`size {300 40}`)** below it uses an ABSOLUTE `position = { 0 22 }` for its inner progressbar — absolute-positioned children don't participate in vbox flow, but the widget itself is fixed-size so it should reserve 40px; verify it's actually inside the vbox flow and not overlapping.
  3. **The buttons' own container** — check whether the Integrate/Loosen buttons are in the SAME vbox (flowing below) or in a sibling container with an absolute/`position` offset that puts them over the header regardless of the header's height. If they're absolutely positioned, no amount of header-height fixing helps.
- **DIAGNOSTIC:** the fix comment claims fixed-size lets the vbox "reserve real height so buttons flow below" — but they still overlap, so EITHER a widget between header and buttons still collapses (lead #1, the `only_text`), OR the buttons aren't actually in the flowed vbox (lead #3). Read the full vbox from line 1527 down to where the Integrate/Loosen buttons are defined and confirm they're flow-children after fixed-height siblings.
- **File(s):** `gui/diplomatic_view.gui` — the `subject_actions_open` vbox (~1527) and the Integrate/Loosen button block (~1666 / `qing_subject_integrate_button`).
- **Severity:** MINOR (readability/overlap; feature still usable).

---
- **❌ BOOT-TEST 2026-07-10 (build c7cc248d): STILL BROKEN.** User: "the Tighten and Loosen Control buttons still very much overlap (try moving the text down instead)." Both prior fixes (v1 header autoresize→fixed, v2 subject-type only_text→fixed textbox) did NOT resolve it. The vbox (diplomatic_view.gui:1526) holds header textbox → subject-type textbox → integration progress widget → the diplomacy_action_button rows. LEAD: the action buttons carry `parentanchor = hcenter` (e.g. line 1583) which can DETACH them from the vbox's vertical flow so they float up over the label rows regardless of the labels reserving height. USER'S SUGGESTED APPROACH: move the TEXT down (add top margin/offset to the header+type labels, or push the whole label block below where the buttons anchor) rather than trying again to make the labels reserve height. Consider: drop parentanchor=hcenter from the buttons so they stack in flow, OR add margin_top to the label block. Verify in-game. Tracked as B15-v3.

## 6 — Religion panel ("Faith & Sedition") opens EMPTY — only the header renders, no meters
- **Observed:** the Qing Religion window opens showing only the **"Faith & Sedition"** title/header; the whole body (the 5 meters — Anti-Foreign / Social Friction / Sectarian Pressure / Missionary Reach / Reform Pressure — the band text, and the Taiping section) is MISSING.
- **INVESTIGATED — earlier structural theory REFUTED, now HOLD FOR LOGS:**
  - Initial theory (base_window+main_window_template vs the marriage window's base_sub_window) is **WRONG**: `gui/qing_greatgame.gui` uses the IDENTICAL structure (`base_window` + `using = main_window_template` + a sibling `flowcontainer` with a `MainWindowHeaderBox` header + a `margin_widget` body) and ITS body renders fine (B10 moved content into it, B20 was about its body text overflow). So the template/structure is not the cause.
  - Ruled out: NOT per-row culling (no `visible` gate on the meters flowcontainer); NOT unset-var-abort (all five meter vars — qing_antichristian_sentiment, qing_mission_social_friction, qing_sect_pressure, qing_missionary_reach, qing_reform_pressure — ARE seeded at game start, and the binds use `GetValue|0` fallback anyway).
  - The window is structurally identical to a working one and its data is seeded, yet only the header renders. **Cause not resolvable from script — needs the render/error log.** Suspects to check WITH logs: (a) a GUI parse/expression error in a body widget that aborts the subtree on open (grep error.log for `qing_religion`); (b) the window opening at an off-screen position or a body/scrollarea computing 0 content height; (c) the createwidget instantiating a stale/duplicate `qing_religion_panel` name.
- **File(s):** `gui/qing_religion.gui`; ref working twin `gui/qing_greatgame.gui`; opener `gui/religion_view.gui:230`.
- **✅ ROOT CAUSE FOUND + FIXED (via logs, suspect (b) confirmed).** error.log for this run has **NO parse error** on `qing_religion.gui` (only a benign utf8-bom *warning* on the unrelated `common/scripted_guis/QING_religion_panel.txt` — a scripted_gui, not the window). So it was **suspect (b): the body computed 0 content height/width.** The one structural difference from the proven-rendering twin `qing_greatgame.gui` was that religion put its body flowcontainer DIRECTLY in the `margin_widget`, while greatgame wraps its (otherwise identical) body in a `scrollarea > scrollwidget`. The body's meters sub-section uses `layoutpolicy_horizontal = expanding`, which needs a defined-width ancestor to expand into; a bare shrink-to-fit flowcontainer gave it none, collapsing the whole body. **FIX:** wrapped the religion body in the same `scrollarea (460x540) > scrollwidget` the twin uses, and applied the twin's B20 description fix (drop `autoresize=yes`, taller fixed multiline box). Braces 94/94.
- **Severity:** MAJOR — RESOLVED (pending boot-test confirmation).

---
- **❌ BOOT-TEST 2026-07-10 (build c7cc248d): STILL BROKEN.** User: "Religion panel still shows empty panel with just the label 'Faith & Sedition'." The scrollarea>scrollwidget wrapper fix did NOT resolve it. Braces balanced (94/94); the structure now closely mirrors the proven-rendering twin qing_greatgame.gui (base_window + main_window_template + flowcontainer[header widget + margin_widget[scrollarea>scrollwidget>flowcontainer(vertical)]]). Yet the body still collapses to nothing. THIRD GUI/layout theory this session to pass review but fail in-game (with B21, B22). NOT blind-fixing a 4th variant. Get error.log/debug.log — need to see whether the window emits a parse/scope error at open, or the body's scripted-gui `visible=` conditions all evaluate false (which would blank every meter row). Candidate to compare byte-for-byte against qing_greatgame.gui in a focused diff. Tracked as Bug6-v2.

## 7 — Grand Council office cards: move the displayed modifier list into hover text on the office name
- **Request (design/UX, not a defect):** for EVERY Grand Council office card, the modifiers are currently displayed inline on the card. Move them into a **tooltip on the office NAME** instead. The tooltip should read as a short description of the office FOLLOWED by the granted modifiers, e.g.:
  > *"The Grand Chancellor is the leader of the Grand Council and wields outsized influence over its operations…. When filled, the office grants the following modifiers to Great Qing: [modifier list]."*
- **Scope:** all appointable great offices — chancellor, personnel, revenue, rites, war, justice, works, censor, lifanyuan, chamberlain, zongli, grand_secretariat, guard_commandant (13). Each needs: (a) a one-line role description, (b) the "when filled, grants … to Great Qing:" lead, (c) the office's modifier list rendered in the tooltip.
- **Implementation:**
  1. **Remove** the inline modifier display from each office card in `gui/government_view.gui`.
  2. **Add a `tooltip` to the office-name widget** on each card. The modifier list can be pulled in with the engine's modifier-tooltip token (the `GetModifier`/`AddModifierText`-style expression the game uses to render a modifier block), or written into a loc key per office if the modifier objects don't expose a clean tooltip token.
  3. **Loc:** one new key per office, e.g. `QING_OFFICE_CHANCELLOR_ROLE_TT`, structured as `<description>. When filled, the office grants the following modifiers to Great Qing:\n[modifier block]`. The office modifiers are the `qing_office_<office>_active` country modifiers (`common/modifiers/qing_governance_modifiers.txt`) — surface THAT modifier's own tooltip/effect list.
  4. **Best path (verify):** if `qing_office_<office>_active` is a real country modifier, the engine can auto-render its effect list in a tooltip via the modifier-reference token — so the loc need only supply the description + lead sentence, and the engine appends the modifier lines. Confirm the token that does this against an existing modifier tooltip in the mod.
- **File(s):** `gui/government_view.gui` (office cards — remove inline modifiers, add name tooltips); `localization/english/qing_governance_l_english.yml` (13 `_ROLE_TT` keys); ref `common/modifiers/qing_governance_modifiers.txt` (the `qing_office_*_active` modifiers).
- **Severity:** enhancement / UX polish (declutters the cards, adds flavor + discoverability). Not a bug.

---
- **⚠️ BOOT-TEST 2026-07-10 (build c7cc248d): MOSTLY FIXED, minor formatting.** User: "the modifier is awkwardly displayed on a newline after the description, fix that." The 13 QING_GC_OFFICE_<X>_TT keys (qing_governance_l_english.yml:245-257) format the modifier as `<desc>\n\nWhen filled, the office grants the following to Great Qing:\n<modifiers>` — the modifier values sit on their own line under the intro. FIX: tighten the modifier presentation (put the values on the SAME line as the intro, or drop the verbose intro line so the modifier reads cleanly right after the description). Confirm desired exact layout with user before editing. Tracked as Bug7-tooltip-format.

## N-ATTR-ICONS — Martial/Finesse/Charisma/Zeal icons wrong in many places
- **Observed:** the four attribute icons are wrong/swapped in many places (introduced by my recent GUI edits). Correct reference: https://imperator.paradoxwikis.com/Attributes — and vanilla/other-mod usage.
- **Canonical mapping (vanilla):** Martial → `icon_military` (font_icon_military.dds), Finesse → `icon_civic` (font_icon_civic.dds), Charisma → `icon_oratory` (font_icon_oratory.dds), Zeal → `icon_religious` (font_icon_religious.dds). Templates defined in `gui/shared/font_icons.gui` (texticon military_icon/civic_icon/oratory_icon/religious_icon). Reference files that map them correctly: `gui/selectcommanderwindow.gui`, `gui/select_office.gui`, `gui/shared/gui_base.gui`.
- **NOTE:** my picker block in `imp19c_windows.gui:93-113` ALREADY uses the correct vanilla mapping, so the breakage is elsewhere — either an overridden icon TEXTURE or a crossed `blockoverride "Icon"` in another file I edited. FIX PASS: `git diff` my GUI commits vs the vanilla reference files, find where the icon↔attribute mapping got crossed, restore to the canonical mapping above.
- **Severity:** MINOR (cosmetic, but widespread + confusing).

---

## N-GREATGAME — Great Game tab label all-caps + panel DESC still spills
- **Observed (boot-test 2026-07-10, build c7cc248d):** (1) the Qing diplomatic-view "GREAT GAME" tab is ALL-CAPS, should be "Great Game". (2) the Great Game panel intro ("The throne's dashboard for playing the great powers...") STILL spills off the right edge of the window despite the #314 B20 multiline+fixed-width fix.
- **Symptom 1 CAUSE + FIX:** `QING_GREAT_GAME_TAB_BUTTON:0 "GREAT GAME"` (qing_greatgame_l_english.yml:40) is literally uppercase in the loc → change to "Great Game". (The sibling QING_GREAT_GAME_TAB_TITLE is already "The Great Game".) Trivial loc fix.
- **Symptom 2:** GREAT_GAME_PANEL_DESC textbox (qing_greatgame.gui:88-94) ALREADY has multiline=yes + fixed size {460 64} (the B20 fix) yet STILL spills. So multiline+fixed-width alone isn't wrapping here — same failure the text-wrap standing rule warns about. Needs boot-verified diagnosis: check the parent width anchor / a missing max_width / whether 460 exceeds the usable width. Compare to a proven-wrapping textbox. Log-gated with the other GUI-render mysteries (Bug6).
- **STANDING RULE created:** GUI paragraph text must wrap (multiline=yes + fixed width, never autoresize=yes) — recurs in many places per user. See memory [[imp19c-text-wrap-rule]]. Fix pass should SWEEP all textboxes for autoresize=yes on paragraph text.
- **Severity:** MINOR (cosmetic), but the wrap issue is WIDESPREAD.

---

## N-POL-HEIR — Poland's heir (flag-right) is a foreign Russian (Aleksandr I Romanov)
- **Observed (boot-test 2026-07-10):** POL shows August Wettin (ruler, left of flag — CORRECT, the NEW-B27/#329 fix worked) but **Aleksandr I Romanov on the RIGHT (heir)**. The right side IS the heir/successor slot.
- **CAUSE:** August Wettin (char:572, the seated POL king) has NO child/heir defined in-realm. Poland's setup file (00_Poland.txt) also parks a RUSSIAN prince — char:153 "Konstantin", `family="c:RUS.fam:Romanov"`, father=char:146/mother=char:145 (the RUS Romanov line), culture=russian — as an unlanded character (staged for a later Congress-Poland / personal-union arc). With no in-realm successor for a childless elective-monarchy king, the engine's succession auto-picks the nearest eligible character it can reach through the defined family graph → it lands on the RUS Romanov line (Aleksandr I). Same *class* as the RUS Bulganin/Aleksandr auto-pick: a slot left unfilled → engine grabs a wrong character.
- **FIX OPTIONS (confirm with user):** (a) give August Wettin a defined child/heir (historically his son Frederick Christian of Saxony, or seat the historical 1764 successor Poniatowski as heir); (b) if Poland is an elective monarchy with no dynastic heir by design, that may be ENGINE-correct behaviour to leave — but it should not pull a foreign Romanov. Needs a real Polish/Saxon heir character. Also relates to the parked RUS char:153 in the POL file (should it carry a death_date/where does it belong?).
- **Severity:** MODERATE (wrong heir → wrong succession, foreign dynasty inherits Poland). Data fix.

---

## N-RULER-NO-FAMILY — many seated 1763 rulers have NO family graph (parents/spouse/siblings/children)
- **Observed (boot-test 2026-07-10):** User: "both August Wettin and Tokugawa Ieharu have no parents, spouses, siblings, or children which doesn't seem correct (this is probably a much bigger issue affecting many characters you created)." CORRECT — systemic.
- **SCOPE (grep of setup/characters/): 31 SET-AS-RULER characters have ZERO family-relation fields** (no father/mother/spouse/marry_character/children). Incl. POL char:572 August Wettin, and by the same pattern TKG char:356 Ieharu (has a bare `family=` clan tag but no actual kin). Others: AUS 457, Central_Asia 323 (Songjun), COL 41, GER 394, India 573/93/575/574/529/530/532/533/576, Italy 18/134, N.America 453/478/580/16/85/81/141, Ottoman 42/250/35/577, Persia 548/578, Peru 1, RUA 552. (Many predate my work; the 1763-bookmark ones I seated — 572, 356, the char:5xx roster — are squarely in scope.)
- **CONSEQUENCE:** this is the ROOT of N-POL-HEIR — a childless ruler with no dynasty forces the engine's succession to auto-pick the nearest reachable character (a foreign Romanov for POL). Also means: no heir shown on flag-right for many nations, broken/foreign succession, empty dynastic trees, and likely feeds B12 (marriage candidate rulers with no children fail the any_child gate — the ORIGINAL B12 empty-list theory). Possibly linked to the marriage `minor_chi` (a family-less character shows the engine's minor_<tag> auto-family).
- **FIX (large data task, confirm scope with user):** give each seated ruler a minimal historical family — at minimum a spouse + an heir (child), ideally parents for dynasty continuity. Prioritise: (1) the rulers I created for 1763 (POL 572, TKG 356, + the char:5xx bookmark roster) and (2) any nation whose flag-right shows a foreign/wrong heir. Use real historical kin where known. This likely also resolves N-POL-HEIR and materially helps B12.
- **Severity:** MAJOR (systemic — succession, heirs, marriage candidates, dynastic trees all depend on the family graph).


---

## N-DEATHDATE — ~109 setup characters carry a FUTURE death_date → shown as already-dead
- **Rule:** the setup snapshot treats ANY character with a `death_date` as already-dead (the #329 class), so anyone with death_date AFTER the 1763.2.16 start (alive-then, dies-later) is wrongly shown dead. Only past death_dates (e.g. Pyotr III 1762) are legitimate.
- **SCOPE (grep, comments excluded): ~109 future-dated death_dates across 16 country files.** Per-country: AFG 2, Austria 6, Brazil 1, Britain 10, France 8, German Conf 6, Haiti 2, India 1, Italy 4, Korea 1, N.America 9, Ottoman 2, Persia 3, Qing 51, Russia 1 (Pavel — the last un-stripped), W.Africa 2. (Poland's was already stripped; note Poland's had a trailing-period typo `1763.10.05.`.)
- **CONFIRMED in-game instances:** RUS Pavel I "died 1801"; **FRA heir Louis Ferdinand de Bourbon (char:407) "dead since 20 Dec 1765"** (Louis XV's son + heir, correctly alive at 1763). Both future → the bug.
- **FIX:** strip `death_date` from all ~109 future-dated setup characters (natural death is handled by the age system after load — see the RUS char:144 / POL char:572 / TKG char:356 precedent). Leave PAST death_dates intact. Also fix the Poland `1763.10.05.` trailing-period typo if that block still has it. Mechanical sweep + per-file brace check.
- **Severity:** MAJOR (systemic — heirs/rulers/dynasts across 16 nations shown dead; feeds wrong-heir + empty-marriage-candidate symptoms).

