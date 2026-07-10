# 1763 Boot-Test Bugs — 2026-07-11 playtest

Branch under test: **1763_bookmark** (head `cf688030`, UNCHANGED since 2026-07-10 — none of the overnight `overnight-312-315-audits` work is included). Start: Qing (CHI), 1763.2.16.

Fixes for everything here land on **1763_bookmark**.

Legend: **REGRESSION-N** = a bug from the prior (2026-07-10) batch that was thought fixed but is NOT; **N** = newly observed this test.

---

## REGRESSION-B21 — Qing armies still all stacked on Beijing
- **Observed:** at start, the entire Qing order of battle (all ~27 banner + Green Standard garrisons) is piled on Beijing, NOT dispersed to Xi'an / Ili / Mukden / Chengdu / Canton / Fuzhou / Ningxia / Kashgar / etc.
- **History of the fix (this is now the 4th failed attempt):**
  1. original: `$prov$.state.governorship = { raise_legion = { ... location = pX } }` — raise_legion musters at the governorship SEAT, ignores location → all at Beijing.
  2. #241: `owner = { create_unit { location = $prov$ } }` (absolute p:X token) → still stacked.
  3. #314 B21 / current on 1763_bookmark: `$prov$ = { owner = { create_unit { location = prev.prev } } }` → **STILL STACKED (this test).**
- **File:** `common/scripted_effects/imp19c_effects_legion_setup.txt` — `SE_qing_raise_garrison` (line ~94) + `SE_qing_raise_garrison_cmd` (line ~135). Raised from `SE_qing_armies`, fired via `qing_force_setup.1`.
- **✅ ROOT CAUSE FOUND + FIXED (#314 B21-v2).** The bug was a **scope-overshoot in `prev.prev`**, not a land-vs-navy engine quirk. Inside `$prov$ = { owner = { create_unit } }` the create_unit runs in the **owner (country)** scope, where `prev` = `$prov$` (the province) but `prev.prev` = the scope the province was entered *from* = **ROOT (c:CHI)** → the engine resolves a country to its **capital = Beijing**. So every garrison mustered at Beijing. The Invictus `prev.prev` naval pattern (00_greek.txt:86) hides this because each tradition raises exactly **one** navy — nobody notices it sits at the capital port; the Qing raises ~27 and they all pile up. **FIX:** use the absolute province token — `location = $prov$` (galatian_invasion.txt:718 `create_unit { navy=no location=p:384 }`; nuragic_missions_2.txt:3366 `location=p:1453` — both LAND units at a named province). `$prov$` IS the `p:X` token, so each garrison now musters at its own province. Applied to all 3 create_unit sites in `SE_qing_raise_garrison`/`_cmd`. (The #241 note "absolute p:X token still stacked" appears to have been a mis-diagnosis — the absolute token is exactly what disperses.)
- **Severity:** MAJOR — RESOLVED (pending boot-test confirmation).

---

## REGRESSION-B22 — only the Fujian water-force spawns; Guangdong + Zhejiang still missing
- **Observed:** at start only **福建水師 (Fujian Coastal Patrol)** exists. The **廣東水師 (Guangdong, Canton p:9298)** and **浙江水師 (Zhejiang, Ningbo p:2893)** squadrons do NOT appear (same symptom as before the "fix").
- **History of the fix (also multiple failed attempts):** country-scope `create_unit { navy=yes location=p:X }` → spawned only one. Current on 1763_bookmark: three separate effects (`SE_qing_navy_guangdong` / `_fujian` / `_zhejiang`) each `p:X = { owner = { create_unit { navy=yes location = prev.prev } } }`, all fired ONE tick in `qing_force_setup.11` after a day-3 `SE_qing_navy_disband` (`every_navy = { destroy_unit }`). → **STILL only Fujian (this test).**
- **File:** `common/scripted_effects/imp19c_effects_legion_setup.txt` — `SE_qing_navy_guangdong` (~360), `_fujian`, `_zhejiang`, `SE_qing_navy_disband` (~334). Wired via `qing_force_setup.10` (disband) + `.11` (raise all three).
- **✅ ROOT CAUSE FOUND + FIXED (#314 B22-v2) — SAME BUG AS B21.** All three squadrons used `location = prev.prev`, which at the owner scope resolves to **ROOT's capital (Beijing)** for ALL three. The engine cannot berth three separate navies at one inland capital, so it kept only one (Fujian, the last raised) and silently dropped the other two — exactly the "only Fujian" symptom. **FIX:** each squadron now locates at its own **coastal home port via an absolute/saved-scope token** — main branches `location = p:9298` (Guangdong) / `p:3651` (Fujian) / `p:2893` (Zhejiang); fallback branches `location = scope:qing_gd_fallback_port` / `qing_navy_fallback_port` / `qing_zj_fallback_port`. Same absolute-token idiom as the B21 land fix. (The disband/same-tick theories were red herrings — the placement token was the real culprit.)
- **Severity:** MAJOR — RESOLVED (pending boot-test confirmation).

---

## REGRESSION-B7 — Grand Council "Appoint" button does nothing
- **Observed:** in the Grand Council / Government view, clicking **Appoint** on a great office does NOTHING — no candidate-picker window opens. Expected: a window listing eligible candidate courtiers (incl. sitting ministers, for reshuffle).
- **Prior status:** B7 was on the 2026-07-10 list as "wiring OK = runtime" (my audit memory said the dead-GUI audit cleared B7 as a runtime issue, not dead wiring). This test shows it is STILL broken at runtime on 1763_bookmark.
- **✅ ROOT CAUSE = THE SAME CORRUPTED BOM AS B14 — FIXED.** `error.log`: `Could not find widget 'qing_office_picker_window' in 'gui/imp19c_windows.gui'`. The picker window IS defined (imp19c_windows.gui:37) and the Appoint onclick (`gui.createwidget gui/imp19c_windows.gui qing_office_picker_window`, government_view.gui:2634 etc.) is correct — but the double-encoded BOM at the top of imp19c_windows.gui broke parsing at line 1, so `qing_office_picker_window` never registered → createwidget found nothing → click did nothing. The BOM repair (see B14 entry) restores it. **B7 + B14 share the one fix; nothing else needed.**
- **Severity:** MAJOR — RESOLVED by the BOM repair.

---

## 1 — Throne section: Statesmanship bars clipped by the Dynastic Health section
- **Observed:** in the Grand Council / Government view, the **"The Throne"** section and the **"Dynastic Health"** section are too close vertically — the **Statesmanship bars for the three Throne positions** (Emperor / Empress? / Crown Prince, or the three summit seats) are NOT visible; they are clipped/overlapped by the Dynastic Health block below.
- **Fix:** add vertical space between the two sections — increase the spacing/margin/offset (or the Throne container's min height) so the three Statesmanship bars render fully before Dynastic Health begins.
- **File(s):** `gui/government_view.gui` — the "The Throne" container and the "Dynastic Health" container; look for the flowcontainer spacing / a fixed size that's too short to fit the three bars, or a following block positioned with a hardcoded offset that overlaps.
- **Severity:** MINOR (layout/readability — data is there, just not shown).
- **NOTE:** this is a NEW section vs the 2026-07-10 layout — likely introduced by the B10 Edicts-strip reorg or the develop GC restructure (Empress seat / relocated Regent+Emeritus). Check what pushed the Throne block's height.

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

## REGRESSION-B12 — Royal Marriage / Dynastic Match window opens but the candidate list is EMPTY
- **Observed:** the **Dynastic Match** window now OPENS (so the B14-style window-culling is fixed), but the candidate list inside is **empty** — no foreign houses shown.
- **Prior theory (2026-07-10):** B12 "was expected to fix itself once real rulers with children load (B1/B2)." This test shows it is STILL empty → either B1/B2 is not fully fixed at the 1763 start, OR the emptiness has a different cause.
- **File:** `common/scripted_guis/MARRIAGE_actions.txt` — `marriage_open_candidates` (builds the `marriage_candidates` variable-list via `every_country`); window `gui/marriage_window.gui` reads `datamodel = "[Player.MakeScope.GetList('marriage_candidates')]"`.
- **The candidate `every_country` limit requires ALL of:** `exists = current_ruler`, `MARRIAGE_eligible_realm_trigger` (dynastic monarchy, not-subject, num_of_cities≥1), `ROOT = { in_diplomatic_range = prev }`, AND `current_ruler = { any_child = { is_alive=yes is_married=no prisoner=no } }`.
- **LEADS (rank by likelihood):**
  1. **Diplomatic range.** At a 1763 Qing start the empire is isolationist — `in_diplomatic_range` may exclude the European dynastic houses entirely, leaving only near neighbours (which may be tribes/republics/subjects that fail `MARRIAGE_eligible_realm_trigger`, or lack an eligible child). If so, the list is legitimately empty by the range gate. **Check debug.log for the "candidate-list window opened" LOG_line and whether any add_to_variable_list fired.** Consider whether CHI should see out-of-range houses in this window (the marriage window may need to relax `in_diplomatic_range`, since a dynastic match is a reason to open relations).
  2. **Childless rulers (B1/B2 residue).** If neighbouring monarchies' rulers still load without children at 1763, the `any_child` test fails for all of them. Cross-check with whether B1/B2 (ruler data) actually holds in THIS test — verify a few neighbours (Korea, Vietnam, Burma, the Central Asian khanates) have real rulers WITH children.
  3. **narrow_monarchy_trigger** may exclude the East/Central-Asian monarchies (khanates, the Tibetan/Nepalese states) if it's tuned to European monarchy government types — so even in-range neighbours fail eligibility. Inspect what `narrow_monarchy_trigger` accepts.
- **Severity:** MAJOR (the marriage feature is unusable for the Qing player — nothing to court).
- **NOTE:** distinct from the overnight #313 two-pass rewrite — 1763_bookmark still has the older #311 single-pass `every_country` build. Diagnose on THIS code.

---

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
- **FIX (NOT done this pass — larger structural change, needs care):** either (a) renumber these characters
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
