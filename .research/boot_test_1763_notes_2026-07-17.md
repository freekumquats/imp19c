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

---
# ============================================================
# BOOT TEST — 2026-07-17 session (Royal Marriage + western NA)
# Branch: 1763_bookmark @ b385452a4 (pushed). No code changed during capture.
# Eunuch health-trait boot-crashfix (b385452a4): NO crash reported on load ✓
# (implies the fix held — confirm clean load to game).
# ============================================================

## B1-a — Royal Marriage button placement  (GUI, cosmetic-ish)
The "Royal Marriage" button renders on its OWN line BELOW Trade Actions, not
inside the **Alliance Actions** category where it belongs.
- diplomatic_view.gui:1539 the [B1] margin_widget is a standalone sibling of the
  Trade-Actions block (1416) — a top-level row, not folded into any category_drop.
- "Alliance Actions" is a vanilla diplomatic-action CATEGORY (loc: INVITE/ASKJOIN/
  LEAVE/GUARANT/ALLIANCE/CALL _CATEGORY = "Alliance Actions"), rendered by the
  generated actions_grid (diplomatic_view.gui:1350 GetActions datamodel). Our custom
  button is NOT an engine diplomatic_action, so it can't natively land in that
  generated category — it's a scripted_gui button. FIX options to weigh:
    (a) relocate the margin_widget to render visually under the Alliance-Actions
        category header (position/reorder), or
    (b) wrap it as its own category_drop styled to match (like Trade/Subject Actions),
        or (c) leave standalone but relabel. Confirm user intent = "inside Alliance
        Actions grouping" vs "just move it up near alliances."

## B1-b — Royal Marriage picker DEAD-ENDS at screen 2→3  (functional, MAJOR)
Clicking Royal Marriage correctly opens screen 2 (our eligible Qing chars). Picking
a char DOES NOTHING and CLOSES the window — screen 3 (target realm's opposite-gender
chars) never opens.
- Flow: diplomatic entry marriage_play_diplo_open (MARRIAGE_PLAY_actions.txt:44) sets
  marriage_play_target + builds own & their lists. Screen-2 row onclick
  (marriage_play_window.gui:145-147): Execute marriage_play_pick_own, ClearWidgets
  own_window, createwidget marriage_play_their_window.
- Symptom = "closes, nothing opens" ⇒ ClearWidgets ran but the createwidget of
  marriage_play_their_window silently failed OR the window opened empty and was
  perceived as closed.
- Prior note #38 flagged a `down=` PARSE FAILURE in this window. VERIFIED TODAY: the
  current screen-3 down= (marriage_play_window.gui:221) now MATCHES the proven working
  SUBJ_tab_selected idiom (diplomatic_view.gui:2465) — row datacontext = Character,
  scriptedgui inlined in onclick only. So the old parse bug appears already fixed;
  this is likely a DIFFERENT cause.
- CANDIDATE CAUSES to check with a fresh error.log:
    1. marriage_play_pick_own is_valid GATE fails silently (line 95: is_alive/
       is_married=no/employer=scope:player) so no rebuild happens — but that wouldn't
       stop createwidget. Lower priority.
    2. screen-3 window still fails to parse/create for some OTHER reason (a later line
       in the their_window block). Needs error.log confirmation.
    3. marriage_play_their_candidates ends up EMPTY (build_their want_male filter) so
       screen 3 opens but shows only the "no candidates" textbox → user reads it as
       "did nothing." Check MARRIAGE_PLAY_build_their (se_MARRIAGE_PLAY.txt:443) in the
       pick_own path: it saves `this` as mplay_home_country (the country) — but in the
       pick_own GUI context ROOT=Character, this=country; the review-fix comment claims
       `this` is country in both paths. VERIFY at runtime.
- BLOCKER on root-causing: NO fresh error.log in ~/Downloads this session. Need the
  user to reproduce with -debug_mode and share error.log (look for: "Failed parsing"
  near marriage_play_window, or absence of "their-candidate list built" MARRIAGE line).

## B2 — Empty unowned land in WESTERN North America  (history/setup)
User: considerable empty unowned land in the west where NSP (New Spain) + HBC/NWC
were trimmed (commits ed57f3648, 27adb7ae7). Question: were Native American tags
historically present there → should the land be assigned to them?
- Trim commit ed57f3648 CLAIMED it reassigned stripped land to resident Native tags
  (APA/LIP/CDD/ICF/C3F/DAK) and left only Timmins 910 unowned. User sees more empty
  land than that ⇒ either more provinces were left unassigned than the commit claims,
  or a later commit re-emptied some, or the "west" gaps are from a different trim.
- NOTE the tag swap: HBC tag → north_west_company.txt; NWC tag → hudson_bay_company.txt
  (crossed in countries.txt:155/178).
- Large existing western Native roster already ships (SHO/UTE/YAK/BLF/CMC/APA/DIN/HAI/
  BCK/ARP/CHY/CRW/ICF/ASB + Pacific-NW Salish MCK/NSQ/PUY/LKU + NWE/WNT/NUU/PMO).
- → dispatched research agent to (1) list actually-ownerless western province IDs from
  setup/provinces/00_default.txt (ignoring # comments), (2) name historical Native
  occupant per cluster, (3) recommend existing-tag / new-tag / defensibly-empty.
  [PENDING agent result — fill in below.]

## B3 — Province Buildings tab: Military + Urban Districts cut off  (GUI, needs scrollbar)
The province window Buildings tab clips its lower sections — Military District and
Urban Districts fall below the window bottom and can't be selected.
- province_window.gui:4025 the buildings-tab margin_widget is a FIXED size = { 500 500 }
  holding a vertical flowcontainer (4029) of section rows via `building_box`
  (4050): Port / Education / Industrial / Infrastructure / PublicWorks / Military
  (4085) / UrbanDistricts (4089). NO scrollarea wraps the section stack, so once the
  [B2] PublicWorks row (6 Qing works buildings, 4077) + others exceed ~500px the last
  two sections (Military, Urban Districts) render past the bottom edge.
- Likely made worse on Qing specifically by the extra PublicWorksItems row we added.
- FIX: wrap the inner section flowcontainer (4029/4040) in a scrollarea+scrollwidget
  (clone the queued-buildings scrollarea idiom at 4098, or the pops-tab pattern), with
  a VerticalScrollBar, so all sections are reachable. Keep the sub_header outside the
  scroll region. Mind the fixed 500x500 — the scrollwidget content can exceed it.

## B4 — "The Fullest Coffers" (qing_revenue.5) fires too early (June 1763)  (balance/seed BUG)
Event = qing_revenue.5 "The Fullest Coffers the Dynasty Has Known" (#372 peak-treasury
milestone). Fired ~June 1763, should fire only when the 戶部 silver reserve first NEARS
its historic high near mid-reign, NOT at the 1763 start.
- Trigger: se_QING_REVENUE.txt:156-164 fires when `var:silver_reserve_size >= 80000`
  (~98% of the 81820 千兩 peak), one-shot (qing_silver_reserve_peaked) + GC slot-gated.
- 1763 seed: se_CURRENCY.txt:1033-1040 date-gates `current_date < 1772.1.1` → seeds
  silver_reserve_size = 62000 (千兩). Quarterly drift (se_QING_REVENUE.txt:110-114) is
  only +250 (+100 extra for high finesse) → 62000→80000 would take ~12-18 YEARS.
- ⇒ ROOT CAUSE is NOT drift/timing: the reserve must ALREADY be >= 80000 at game start.
  Something seeds/reads silver_reserve_size higher than 62000 at the 1763 start.
  CANDIDATES to verify with runtime value + log:
    1. Generic reserve seed CURRENCY_base_starting_reserve_silver (se_CURRENCY.txt:1137,
       "hundreds lb" units) runs for all tags — if it executes AFTER the CHI date-gated
       62000 override (on_action ordering), it overwrites CHI with a value that reads
       >= 80000 in the milestone's units. UNIT MISMATCH suspect (千兩 vs hundreds-lb).
    2. The CHI date-gated block (line 1033) not executing at seed → CHI falls through to
       a higher default.
    3. qing_high_qing_era or another init bumps silver_reserve_size at start.
- CONFIRM: log line "CHI silver reserve seeded 62000..." (se_CURRENCY.txt:1040) — if it
  DOES appear, the reserve was 62000 then something raised it; if it does NOT, the CHI
  seed never ran. Either way check the runtime silver_reserve_size at 1763.2 vs 80000.
- Quick guardrails once root-caused: (a) the milestone `if` could also gate on
  `NOT = { qing_high_qing_era via date }` isn't right; better (b) fix the seed so the
  reserve genuinely starts ~62000 < 80000; and/or (c) add a min-elapsed-time / date
  floor to the milestone so a warm start can't trip it turn 1.

## B5 — Canton Trade window too small; share buttons spill past bottom  (GUI, resize)
qing_province_reports.gui:713 qing_canton_window is size = { 380 360 }. When the
Canton system is OPEN, the vbox content overflows: margin_top 50 + desc(60) +
3 readout rows(20 each)+spacing + Rotate-Hoppo(30) + SHARE readout row(20) +
3 share buttons (share_0 "All to the Treasury", share_50 "Split Evenly", share_100
"All to the Privy Purse", 30 each) + 10px spacings + margin_bottom 15. That's
~ 50+60+ (3*28) + 38 + 28 + (3*40) + 15 ≈ 400+ px of content in a 360-tall window,
so the last two share buttons FLOAT over/past the bottom (user: not clipped, spilling).
- NOTE the buttons are mutually-visible with open/close/rotate depending on system
  state, but at the state the user hit (open + split levers shown) the stack is tallest.
- FIX: enlarge the window height (size = { 380 ~520 }) so the full open-state stack
  fits, OR wrap the vbox in a scrollarea. Simple resize is what the user asked for
  ("make the window bigger so it includes those buttons"). Pick a height that fits the
  TALLEST state (system open: readouts + rotate hoppo + share readout + 3 share btns).
  ~520-540 tall should clear it; verify against the open-state button set.

# ============================================================
# 2026-07-17 SESSION SUMMARY (6 findings; all captured, none fixed yet)
#   B1-a  Royal Marriage button placement (below Trade Actions, not in Alliance Actions)  [GUI]
#   B1-b  Royal Marriage picker dead-ends screen 2->3 (MAJOR; needs fresh error.log)      [FUNC]
#   B2    Empty unowned western N.America land — Native-tag reassignment  [history; agent running]
#   B3    Province Buildings tab: Military+Urban Districts cut off — add scrollbar         [GUI]
#   B4    "Fullest Coffers" qing_revenue.5 fires June 1763 — reserve seeded >=80000?       [BUG]
#   B5    Canton Trade window too small — share buttons spill; enlarge window              [GUI]
# NO fresh error.log in ~/Downloads this session — B1-b + B4 root-cause need one.
# ============================================================

## B2 — RESOLVED DIAGNOSIS: 54 ownerless western provinces (NWC + ALC emptied, never reassigned)
VERIFIED against setup/main/00_default.txt (the real ownership file; NOT setup/provinces/).
Root cause = an INCONSISTENCY in the 1763 trim campaign:
- HBC + NSP trims (commit ed57f3648) STRIPPED paper frontier AND REASSIGNED it to resident
  Native tags (APA/LIP/CDD/ICF/C3F/DAK), per user directive "assign to Native tags, not unowned."
- BUT the NWC trim (27adb7ae7) and ALC trim (daa78d570) EMPTIED the tag's own_control_core
  and left the stripped land UNOWNED — inconsistent with the HBC/NSP directive. Capitals were
  repointed to avoid the ownerless-capital crash (NWC cap->4918, ALC cap->3807), so it boots,
  but the map shows a big empty hole in the west. Spot-checked 483/521/2076/3067/5505/8161/9296
  = all OWNERLESS. This is the "empty unowned land" the user sees.

  NWC "was (23 -> unowned Native)": 3067 4532 8668 6667 9524 1333 2213 2861 6916 4257 2067
    6961 3747 6674 9190 7417 2349 7745 9614 1239 1005 8881 3810
    (BC interior, Vancouver Island, Cascadia/interior WA, NW-Ontario boreal)
  ALC "was" California (26): 483 521 525 774 980 992 1323 1482 1493 2681 2711 4182 6440 7760
    7774 7789 8161 8483 8496 8510 8730 8870 9166 9296 9846 9997
  ALC "was" Arizona (5): 2076 5185 5505 7784 7837
  (HBC 910 Timmins intentionally left unowned — 1 province, defensible.)

HISTORICAL CHECK (were Native nations present? YES — all densely populated in 1763):
  Reassignment recommendation per cluster (agent research, needs user sign-off on new tags):
  EXISTING TAGS (no new tag needed) — preferred, lowest risk:
    - NWC Cascadia/interior WA  -> YAK (Yakama) [Columbia Plateau]
    - NWC BC coast/N            -> HAI (Haida) [or consolidate coast under HAI]
    - NWC NW-Ontario boreal     -> C3F (Council of Three Fires / Ojibwe)
    - ALC CA Central Valley     -> WNT (Wintun) + PMO (Pomo) for the north coast
    - ALC Central Arizona       -> APA (Apache) [Tonto/Yavapai range is contiguous with APA]
  MAJOR NATIONS WITH NO EXISTING TAG (would need new inert Native tags, à la #16 IRO):
    - Ohlone (SF Bay), Chumash (Central Coast), Tongva/Kumeyaay (LA/San Diego),
      Yokuts (S. Central Valley); BC interior Salish (Secwepemc/Okanagan/Nlaka'pamux),
      Kwakwaka'wakw/Nuu-chah-nulth (mid/W Vancouver Is.)
  DEFENSIBLY UNOWNED: HBC 910 Timmins; any true high-Sierra/alpine or high-latitude
    boreal provinces (verify per-province before leaving empty).
  CRASH-SAFETY for any fix: every recipient tag must already own land + have a valid capital
    (ownerless-capital crash rule); NWC/ALC capitals were already repointed, so DON'T touch
    those. Reassigning provinces to EXISTING tags that already boot is the safe path;
    new tags need the full inert-tag playbook (capital in owned land, no set_as_ruler crash).

DECISION NEEDED FROM USER: (a) existing-tags-only quick fix (YAK/HAI/C3F/WNT/PMO/APA) —
  leaves CA coast nations unrepresented but is fast + crash-safe; OR (b) full build with
  ~6 new Native tags for the CA coast + BC interior (more historical, more work + boot risk).

# ============================================================
# #7 NANCHANG CHRISTIAN MISSION — RESOLVED: NO CHANGE (anachronistic + not present)
# ============================================================
# User asked: "Nanchang is listed as having a Christian mission in 1763 — historically accurate?
# If so, add it as a new building on its own row under a new 'Foreign' section of the Buildings tab."
#
# HISTORY (researched 2026-07-18): NO functioning Catholic mission existed at Nanchang in 1763.
#   Nanchang had an active Jesuit mission in the tolerant Kangxi era (late 1600s-early 1720s), but
#   the 1724 Yongzheng edict closed provincial missions across China; by 1763 (Qianlong) only the
#   Beijing court Jesuits were tolerated (until the 1770s). Provincial Christianity was underground,
#   no resident missionaries / official churches, until the post-1842/1860 unequal treaties reopened
#   provincial missions. Sources: Latourette, "A History of Christian Missions in China"; Qing
#   religious-policy scholarship on the Yongzheng/Qianlong edicts.  => an ACTIVE 1763 mission = ANACHRONISM.
#
# IN-GAME CHECK: province 4842 Nanchang (00_Jiangxi.txt) has religion=pure_land_buddhism, pops in
#   daoism/vajrayana — NO christian/catholic pop, NO mission building (building_list.txt:15524 =
#   URB/EDU/IND only), NO holy_site, NO modifier, and no missionary event targets it. There is NO
#   Christian mission at Nanchang anywhere in the data.
#
# RESOLUTION: NO CHANGE. Adding a "Foreign > Christian mission" building at Nanchang would introduce
#   a historical error, and there is nothing erroneous currently present to remove. The user likely
#   saw a base-game tooltip / a different province / a misread. If a Christian-mission MECHANIC is
#   wanted, the historically-correct home is a POST-treaty (1842/1860+) unlock, not the 1763 setup.
#   (The "Foreign" Buildings-tab section is therefore NOT added; B3's scrollbar already handles the
#   existing section overflow.)
# ============================================================
