# 1763 Boot-Test Bugs — 2026-07-12 (post BT-25→BT-46 fixes)

Playtest of `1763_bookmark` @ `66421aa70` (after the BT-25→BT-46 batch). New findings
continue the BT numbering from BT-46. Branch: `1763_bookmark` (bugfix-only). Status
legend: 🔴 open · 🟡 investigating · 🟢 fixed (committed) · ⚪ needs in-game repro.

---

## BT-47 🔴 — Throne cards: skill numbers overrun into the next card
**Report:** In the Grand Council "The Throne" section, the Emperor, Crown Prince, and
Empress cards overlap slightly. The Emperor's **Finesse** and **Zeal** numbers are
obscured by the Crown Prince card; the Crown Prince's Finesse and Zeal are in turn
obscured by the Empress card.

**Suspected cause (to confirm):** `gui/government_view.gui` — the three throne cards are
laid out in a horizontal `flowcontainer` with `spacing = 0`, each card `size = { 312 168 }`.
Within each card the 2×2 skills grid (`icon_and_text` cells `88×24`, spacing 4 → a row is
~180px) sits to the right of the portrait (46) + Imperial-Favor square + faction square.
The skills column appears to overflow the 312px card width; because the cards abut
(spacing 0), the right-hand column cells — **Finesse** (top-right) and **Zeal**
(bottom-right) — bleed under the neighbouring card. Emperor block ~L2387-2400;
Crown Prince ~L2466-2484; Empress ~L2502+.

**Fix direction (user, not yet applied):** move the **loyalty + 2×2 skills block to the
LEFT** so it no longer overruns the card's right edge into the neighbouring card. The
name/loyalty/skills column currently sits after the portrait + Imperial-Favor square +
faction square, pushing the 2×2 grid past the 312px card width; shifting that block left
(tighten/remove the leading spacing or reduce the favor/faction gutter) pulls the
right-hand column (Finesse top-right, Zeal bottom-right) back inside the card. Apply to
all three cards (Emperor ~L2387-2400, Crown Prince ~L2466-2484, Empress ~L2502+); verify
the vacant-seat state and keep brace balance 0.

---

## BT-48 🔴 — Throne cards: swap the loyalty and statesmanship bar positions
**Report:** On the same three throne cards (Emperor / Crown Prince / Empress), the
**loyalty** read-out and the **statesmanship** progress bar should **swap places**.

**Context:** currently the statesmanship bar sits stacked UNDER the portrait (added in
BT-26, `government_view.gui` ~L2356-2364 for the Emperor), while the loyalty
`icon_and_text` sits in the name/skills column (~L2374-2379). The user wants these two
swapped — loyalty under the portrait, statesmanship bar in the column (or vice-versa;
confirm exact target when fixing). Applies to all three cards; do together with BT-47
(same block being repositioned). Keep brace balance 0; verify vacant-seat state.

---

## BT-49 🔴 — Qing "Primary Heir" position should be localized as "Taizi" (太子)
**Report:** For the Qing, the heir position currently shown as "Primary Heir" should read
**"Taizi"** (太子, the 皇太子 crown-prince title).

**Loc keys involved (`localization/english/interface_l_english.yml`):**
- `NEXT_RULER_TEXT_MONARCHY:0 "Primary Heir"` (L1463)
- `PRIMARY_HEIR_CHAR_MON_ONCE:0 "Primary Heir"` (L484)
- (possibly also PRIMARY_HEIR_CHAR_MON / _ADD L482-483 if the full sentence is shown)

**⚠️ Scope nuance (must NOT break other nations):** these are **vanilla, global**
monarchy-heir keys — editing the string directly renames the heir for EVERY monarchy
(France, Russia, etc.), which is wrong. The fix must be **Qing-only**. Options to weigh
when fixing:
  (a) if the label is rendered in a mod-owned GUI/scripted context, gate it with
      `SelectLocalization( <is CHI>, 'QING_TAIZI', 'NEXT_RULER_TEXT_MONARCHY' )` (the
      idiom already used for the subject-type labels in diplomatic_view.gui);
  (b) if it is emitted by the base-game engine with no mod hook, a custom_loc keyed on
      country tag or a government/position-name override may be needed — determine WHERE
      the string is actually surfaced (F-key screen? succession tooltip? heir card?)
      before choosing. The mod already models the 皇太子 seat as
      `qing_office_crownprince_holder` with its own "QING_GC_CROWNPRINCE" loc — reconcile
      so the two don't diverge. Confirm the exact on-screen location at fix time.

---

## BT-50 🔴 — Grand Council members need a real, exclusive OFFICIAL title (engine office, not a flag)
**Report (user):** Every Grand Council member should hold an OFFICIAL title of their own —
the same *kind* of title as Qianlong being officially Huangdi (皇帝) or the vanilla offices
being officially "Minister of XYZ". The point is the engine-enforced MUTUAL EXCLUSIVITY that
comes with a real position: one character cannot be both ruler and heir; one character cannot
hold two offices at once. GC members currently lack such an official title, so nothing stops
a GC office-holder from ALSO being ruler / heir / a vanilla office-holder / another GC office.

**Observed symptom (user, 2026-07-12):** the Grand Council is currently full of characters who
are SIMULTANEOUSLY army/navy COMMANDERS — which is wrong. A seated minister should not also be
leading a legion. Commander is exactly the kind of engine role a real, exclusive office would
prevent (the vanilla office system + `is_commander`/`employer` checks). So the exclusivity set the
fix must cover explicitly includes **commanders** (and the appoint candidate pool should exclude,
or on-appoint relieve, a character who currently holds a military command — and vice-versa, a GC
minister should not be pickable as a commander). Confirm desired direction: does taking a GC seat
DISCHARGE an existing command, or should commanders simply be ineligible for GC appointment?

**Root cause / current model:** the Qing Grand Council is a HOME-GROWN flag system, PARALLEL
to and invisible to the engine's native office system:
- membership is a country var per office (`qing_office_<office>_holder`) plus a character var
  `qing_office_held = flag:<office>` (se_QING_COUNCIL.txt; ~13 offices: chancellor, personnel,
  revenue, rites, war, justice, works, censor, lifanyuan, chamberlain, zongli,
  grand_secretariat, guard_commandant — plus the dynastic figurehead seats regent/emeritus).
- exclusivity is enforced ONLY within this custom layer: the appoint verb
  `QID_office_appoint`/`qing_gov_office_appoint_selected` checks `NOT has_variable qing_office_held`
  and relieves the prior seat (QING_governance_actions.txt:58+). The ENGINE has no idea these are
  offices, so it will happily let the same character be current_ruler / primary_heir / a vanilla
  `common/offices/00_monarchy.txt` office-holder (office_marshal, office_steward, etc.) / a
  provincial governor WHILE holding a GC seat. That is the gap the user is pointing at.

**Fix direction (DESIGN-LEVEL — scope before building, likely NOT a quick bugfix):** give each
GC office a genuine engine-recognized position so native exclusivity applies. Options to weigh:
  (a) map the GC offices onto the vanilla `common/offices/*` government-office system (real
      `office = ...` positions with proper title loc), so the engine enforces one-office-per-
      character AND ruler/heir/office mutual exclusion for free — but vanilla monarchy offers a
      FIXED, SMALL office set (~9 slots: foreign_minister, marshal, steward, high_priest, etc.),
      so 13 Qing ministries may not map 1:1; investigate whether the office list is moddable/
      extendable and whether the engine caps office count.
  (b) keep the custom layer but ADD the missing exclusivity guards the engine gives for free —
      i.e. exclude current_ruler + primary_heir + vanilla-office-holders + governors from the GC
      candidate pool and appoint verbs, and title the character via a nickname/custom_loc. This is
      cosmetic-title + guard, NOT a true engine office (a character could still be handed a vanilla
      office elsewhere after taking a GC seat).
  (c) hybrid: real engine offices for the seats vanilla supports, custom guards for the rest.

**⚠️ This needs an EXPLICIT design decision from the user + oracle check (native-office moddability
is UNPROVEN here) before implementation.** Almost certainly NOT a 1763_bookmark bugfix — it reworks
the core GC model that #349-#365 all build on; flag for merge-overnight / its own design task, and
confirm the intended exclusivity set (ruler? heir? governors? vanilla offices? each other?) first.
Relates to [[imp19c-grand-council-offices]] and [[imp19c-grand-council-office-redesign]].

---

## BT-51 🔴 — Dynastic Health read-outs: color the numbers (Harmony/Suzerain green, the meters blue)
**Report (user):** In the Grand Council "Dynastic Health" section:
- **Dynastic Harmony** and **Suzerain Prestige** should be shown in **green** text.
- the numbers for **Reform Pressure**, **Banner Decay**, and the rest of the meters should
  all be in **blue** text.

**Where (`gui/government_view.gui`, QING_GC_HEADER_HEALTH section):**
- Harmony line: `QING_GC_DYNASTIC_HARMONY_LINE` (textbox ~L2575); Suzerain:
  `QING_GC_SUZERAIN_PRESTIGE_LINE` (~L2582). → wrap value in green `#G …#!`.
- Health meters (~L2598-2661), each a `*_FMT` loc key: `QING_HEALTH_REFORM_FMT`,
  `QING_HEALTH_CORRUPTION_FMT`, `QING_HEALTH_CURRENCY_FMT`, `QING_HEALTH_SECT_FMT`,
  `QING_HEALTH_BANNER_FMT`, `QING_HEALTH_GREENSTANDARD_FMT`, `QING_HEALTH_BUREAU_FMT`,
  `QING_HEALTH_SELFSTR_FMT`. → wrap the numeric value in blue `#B …#!` (or the mod's blue
  color-tag; confirm a `#B` blue is defined in the color palette, else use the correct tag).

**Fix (loc-only, not yet applied):** edit the loc FORMAT strings in the qing loc yml(s) to
wrap the value token in the color tag (`#G [value]#!` / `#B [value]#!`) — do NOT change the
GUI `using = Default_FontColor` (the color rides in the loc string). Find the `*_FMT` /
`*_LINE` definitions (grep the qing_*_l_english.yml files), preserve the `[...|0]`/data-func
value tokens exactly, keep BOM, and verify `#B` renders as blue in-game (some Paradox palettes
use a different letter for blue). Purely cosmetic; no mechanic touched.

---

## BT-52 🟢 VERIFIED (not a bug) — Army + navy OOB spawns correctly at game start
**Confirmation (user, 2026-07-12):** both armies and navies now spawn correctly at the 1763
start. The current OOB approach is **VERIFIED WORKING and PROVEN** — treat it as the template
for any future unit-spawn work. Covers the BT-15 / BT-33/34/35 / #331 / #338 chain:
`SE_qing_raise_garrison[_cmd]` (capital_scope.governorship `raise_legion` + `location=$prov$`
+ commander via `add_to_legion PREV`/`set_as_commander`), bare `create_unit` in c:CHI control,
`is_port` navy berths, and the guarded fallback-berth commander attach. Recorded here so it is
not re-litigated; see [[imp19c-create-unit-idiom]] and [[imp19c-1763-commander-roster]].

---

## BT-53 🔴 — Religion (Faith & Sedition) panel STILL renders empty (4th recurrence)
**Report (user, 2026-07-12):** "Religion is still empty." The Faith & Sedition panel opens but
the body shows nothing (header only). This has now survived THREE prior fixes — B6/#314
(BOM), BT-14/#377/#352-F9 (layout + dims), BT-38 (scripted_gui BOM) — so DO NOT apply a 4th
blind layout tweak. Diagnose from evidence first.

**Fresh findings (HEAD `66421aa70`, verified 2026-07-12 — NOT assumed):**
- `gui/qing_religion.gui` is 357 lines of REAL content; brace balance 0; the meters block
  (QING_RELIGION_METERS_TITLE + 5 label/value rows, L133-244) is **UNGATED (always visible)**,
  reading `Player.MakeScope.GetVariable('qing_antichristian_sentiment' / _social_friction /
  _sect_pressure / _missionary_reach / _reform_pressure)`. So "empty" = a RENDER/LAYOUT failure,
  not missing data (if the window painted at all, these rows would show).
- **Lead 1 (layout):** the window uses `using = main_window_template` at L26 — a DIFFERENT
  container idiom than the L4 panels that DO render (province reports use a plain
  base_window + scrollarea). The #352-F9 note in QING_religion_panel.txt itself hypothesises a
  "body-as-sibling / no-layoutpolicy collapse" — i.e. the body is a sibling of the container
  rather than a child, so it collapses to zero height. Compare structurally against a KNOWN-GOOD
  twin (the greatgame/TI religion_view.gui, or a working mod L4 panel) and match the container
  nesting + layoutpolicy exactly.
- **Lead 2 (diagnostic blind spot):** the panel is opened by `gui.createwidget gui/qing_religion.gui
  qing_religion_panel` (religion_view.gui:230). createwidget **BYPASSES the scripted_gui effect**,
  so the F9 `debug_log = "QING F9: religion panel open."` in qing_religion_open_panel_button NEVER
  fires on this path — that's why prior "open vs data vs layout" triage got no signal. The BOM on
  gui/qing_religion.gui is ALSO absent (`no-BOM`, starts `###`) — .gui "should have" BOM (warning
  not hard error), but worth adding while here.

**Fix direction (diagnose, don't guess):** (a) get a decisive read — either add a visible debug
textbox to the raw body OR structurally diff against a rendering twin panel; (b) most likely fix
is correcting the window container nesting so the scrollarea/body is a CHILD with proper
layoutpolicy (not a collapsed sibling), matching a proven L4 panel; (c) add the .gui BOM. Confirm
in-game the meters actually paint before calling it fixed. Keep brace 0.

---

## BT-54 🔴 — Appoint + Tribute buttons should show PI cost in the vanilla "Price: [n] @icon" form
**Report (user):** The Appoint button should show its cost in political influence the same way
vanilla does — **`Price: [number] [Political Influence icon]`** — and the Light/Medium/Heavy
Tribute buttons should show the same **when hovered over**.

**Vanilla idiom to match:** the PI-icon token is `@political_influence_icon!` followed by the
number, e.g. `effects_l_english.yml:269` `... $VALUE|G$ @political_influence_icon! Political
Influence.` and the national-debt tooltips (`economic_enchancement_l_english.yml:1073`) render
`@political_influence_icon! [value]`. Use that icon token, not a plain "Political Influence" word.

**Current state (HEAD `66421aa70`):**
- **Appoint:** the cost IS in the per-office tooltips but as PLAIN RED TEXT — `qing_governance_l_english.yml:191+`
  `QING_GOV_OFFICE_*_BTN_TT` end with `Cost: #R 20 Political Influence#!` (chancellor 20, others
  15). No `@political_influence_icon!`. Also note BT-4 replaced the per-office buttons with a single
  ROW-CLICK, so the generic row tooltip is `QING_GC_APPOINT_ROW_TT` — confirm WHICH tooltip the
  user sees on the picker row and put the `Price: [n] @political_influence_icon!` line there
  (the row-click dispatches per office, so it may need the cost shown generically or per-office).
  The appoint verbs spend the PI in QING_governance_actions.txt (chancellor -20 L63, others -15).
  **What the user actually sees + wants DELETED:** the row tooltip `QING_GC_APPOINT_ROW_TT`
  (qing_governance_l_english.yml:290) currently reads *"...The appointment costs political
  influence and relieves any other minister he may already hold."* — the vague "costs political
  influence" clause must be DELETED and replaced with the concrete
  `Price: [n] @political_influence_icon!` form (keep the "relieves any other minister" clause).
- **Tribute tiers:** `qing_subject_tribute_small/medium/large_button` (SUB_QING_subject_interactions.txt)
  each `add_political_influence = -25`, but their tooltips `QING_TRIBUTE_SMALL/MEDIUM/LARGE_TT`
  (diplomatic_view.gui:2787/2808/2829) do NOT show the 25-PI cost at all — only the `is_valid`
  `qing_subject_needs_influence_25_tt` gate mentions influence. Add a `Price: 25 @political_influence_icon!`
  line to each of the three tribute tooltips.

**Fix (loc-only, not yet applied):** edit the tooltip loc strings — appoint `*_BTN_TT` (and/or
`QING_GC_APPOINT_ROW_TT`) to render `Price: [cost] @political_influence_icon!` in place of the
plain "Cost: #R n Political Influence#!"; add the same line to the three `QING_TRIBUTE_*_TT`.
Verify `@political_influence_icon!` is the correct token name in this mod (grep confirms it's used
live). Keep BOM; purely presentational (the actual PI spend already works).

---

## BT-55 🔴 — Migration report: order provinces by population (highest → lowest)
**Report (user):** The provinces listed in the Migration report should be ordered by population,
highest to lowest.

**Cause (HEAD `66421aa70`):** `qing_report_open_migration` (common/scripted_guis/qing_province_reports.txt:137-172)
builds `qing_migration_report_provinces` by walking `every_governorships → every_governorship_state
→ every_state_province` with a plain `if` and `add_to_variable_list` — so provinces are appended in
raw ITERATION order, not sorted. The GUI datamodel renders them in list order, hence unsorted.

**Fix direction (not yet applied):** the innermost `every_state_province` walk cannot itself sort;
replace the province-collection with an ORDERED pass so the list is built high-pop first. Options:
  (a) if the engine allows it, collect into the list then rebuild via an `ordered_in_list` /
      sort pass; simpler —
  (b) restructure to gather candidate provinces then `ordered_owned_province = { order_by =
      total_population  ... }`-style descent that emits into the list in descending pop order. Note
      the list must stay scoped to governorship provinces (the report's descent), so a plain
      `ordered_owned_province` over ALL owned provinces would change WHICH provinces show (capital-
      domain provinces aren't under a governorship) — keep the SAME membership, only change ORDER.
      Confirm the proven ordered-list idiom used elsewhere in this file / the sinicization report.
Read-only display change; keep brace 0, no membership change, just ordering.

---

## BT-56 🔴 — Sinicization report: no province-level change shown + a blank icon slot left of each name
**Report (user):** The Sinicization report shows no province-level change, and there is a BLANK
SPOT to the LEFT of each province name that looks like it expects an icon.

**CORRECTED diagnosis (user, 2026-07-12): the blank space is NOT the goto_button.** The goto_button
was always there, previously right next to the province name. The empty space is NEW since the BT-39
push and sits BETWEEN the goto_button and the name. Both symptoms trace to ONE cause — my BT-39 edit.

**Root cause (BT-39 diff `66421aa70`, verified):** BT-39 changed the sinicization row
(gui/qing_province_reports.gui:481-499) to (a) shrink the name textbox `260 → 200` and (b) INSERT a
new `56`-wide `▲New` marker textbox between the name and the culture columns. That marker is gated
`visible = [GetScriptedGui('qing_report_prov_newly_sinicized').IsShown(...)]` — but an INVISIBLE child
in an `hbox` STILL RESERVES ITS 56px of layout width (hbox reserves slot width regardless of child
visibility unless `ignoreinvisible = yes` is set on the container). So at a stable start where the
marker is never shown (see item 2), the row now has a permanent ~56px empty gap where the marker sits
— the "new empty space between goto button and name". (The name box also lost 60px, compounding it.)
NOTE the marker is placed AFTER the name in the hbox, yet the user sees the gap to the LEFT of the
name — confirm exact column order in-game; either way the invisible-but-space-reserving marker is the
new element. → the reserved-space fix: put `ignoreinvisible = yes` on the row hbox so a hidden marker
collapses its width, OR only allocate the marker column when something is shown.

**Item 2 — province-level change: INTENT CONFIRMED by user.** They want a per-province TREND
INDICATOR (▲ gaining Han share / ▼ receding / – steady), NOT the binary "newly-Han-this-year" ▲New
flag (which is near-always empty at a stable start and is what created the dead/space-reserving
column). So the fix REPLACES the BT-39 ▲New marker with a real per-province trend arrow:
  - extend se_QING_SINICIZATION.txt to store a per-province Han-share snapshot (e.g.
    `qing_prov_han_share_prev`) and compute a delta vs current each annual roll (same snapshot→delta
    idiom as the country-level #385 count and the ethnic-tension report);
  - the row shows ▲ (#G) if share rose, ▼ (#R) if it receded, – (grey) if steady — always SOMETHING,
    so the column is never dead and never reserves space for nothing;
  - retire `qing_prov_sinicized_new` / `qing_report_prov_newly_sinicized` (or repurpose) since the
    trend arrow supersedes the binary flag.

**Fix direction:** rework the BT-39 marker into a 3-state per-province trend arrow (above), and fix
the hbox width-reservation (`ignoreinvisible = yes` / restore name width) so no phantom gap remains.
Ties to BT-39 / #385. Keep brace 0, BOM; this REVISES my own BT-39 work — review before commit.

---

## BT-57 🔴 — "Clash between Ministers" fires several in a row — NOT covered by the BT-28 throttle
**Report (user):** Got several "Clash between Ministers" events in a row from the Grand Council.
Does the throttle cover them? → **NO, it does not.**

**Root cause (HEAD `66421aa70`, confirmed):** the clash event is `qing_personnel.2`
("Clash: [personnel_minister.GetName] vs. [clashing_governor.GetName]",
events/imp19c_mod_events/qing_personnel_events.txt:128). It is dispatched from
`QING_personnel_evaluate_governors` (se_QING_PERSONNEL.txt:31+), which iterates
**`every_character { is_governor = yes }`** — one pass PER GOVERNOR — and, for each governor in
high friction (>=40) + low affinity with the throne, rolls `random = { chance = 10 ... trigger_event
= { id = qing_personnel.2 } }` (se_QING_PERSONNEL.txt:134-143). There is **NO `qing_gc_event_slot_used`
gate and NO slot claim** anywhere in this loop. So every clashing governor rolls independently in the
SAME quarterly pulse, and several can queue a clash at once → the "several in a row" the user saw.
The BT-28 two-slot budget (court + external) covers dynasty/faction/works/tribute/frontier/foreign-
spouse/officer rolls, but this per-governor personnel loop was never wired into it.

**Same-class risk to check while here:** the sibling personnel/censorate/other per-character or
per-subject evaluate loops that `trigger_event` on a per-item `chance` — verify NONE of them bypass
the slot budget the same way (amban evaluate, censorate impeachment, personnel .1/.3/.4). The BT-28
gate was applied to the country-pulse flavour rolls but may not have reached these per-iterator loops.

**Fix direction (not yet applied):** bring qing_personnel.2 (and any sibling per-iterator event
dispatch) under the shared court-slot budget — gate the roll on `NOT has_variable
qing_gc_event_slot_used` and CLAIM the slot (`set_variable qing_gc_event_slot_used = 1`) inside the
`random` on the fire path, exactly like the BT-28 pattern in se_QING_WORKS / se_QING_DECLINE (claim
AFTER the chance succeeds, so a failed roll doesn't burn the slot). Because the loop is per-governor,
the gate must be checked EACH iteration so that once one governor claims the slot, no further governor
in the same pulse can fire — capping it at one clash per pulse. Confirm the slot is reset at pulse top
(it is, 00_monthly_country.txt) and that the personnel evaluate runs on that same pulse. Keep brace 0.

---

## BT-58 🔴 — Subject tab still a mess: RESTORE the loyalty bar + move tribute/[Decisions] to window bottom
**Report (user):** The Subjects tab in the Qing diplomatic view is still a mess. Two moves:
1. **RESTORE the loyalty progress bar** (this REVERSES BT-44, which removed it at the user's earlier
   request — the user now wants the bar back).
2. **Move the section with the tribute amount and the [Decisions] button to the BOTTOM of the window.**

**Where (`gui/diplomatic_view.gui`, the Subject panel ~L2840-2933):**
- The loyalty bar was removed by BT-44 at ~L2877 (the comment block now sits there); the removed
  widget was `widget = { size = { 180 25 } ... progressbar ... value = FixedPointToFloat(
  Multiply_CFixedPoint( Country.GetSubjectLoyalty, '(CFixedPoint)0.01' )) }`. **Restore it** between
  the `GetSubjectLoyaltyInfo` status text (L2870-2876) and the opinion read-out (L2880-2887) — its
  original position. (git show 66421aa70~1:gui/diplomatic_view.gui has the exact removed block, or
  the BT-44 entry / commit 66421aa70 diff.) NOTE BT-44's rationale was that the Qing ladder doesn't
  drive the engine SubjectLoyalty value so the bar looked empty — user accepts/wants it anyway;
  restore as-was. (If it genuinely reads empty, a follow-up may need to back it with a real value,
  but the ASK here is just to restore the bar.)
- The tribute/Decisions section = the treasury/manpower/PI `icon_and_text` row (L2893-2919) + the
  `Decisions` button widget (L2920-2933). Currently they sit mid-panel. **Move both to the BOTTOM**
  of the subject window (after everything else), so the panel reads: subject type → loyalty
  (status + restored bar) → opinion → [rest] → tribute figures + Decisions button last.

**Fix direction (not yet applied):** re-add the BT-44 loyalty-bar widget at its original slot;
reorder the flowcontainers so the tribute-figures row + Decisions button are the final children of
the subject panel container. Pure GUI layout; keep brace 0; verify all subject types + the vacant/
non-CHI paths still render. This is a GUI-cluster fix — review before commit (revises BT-44).

---

## BT-59 🔴 — Subject tab: "Loyalty to the Jurchen Major Power of Great Qing" section is jumbled text
**Report (user):** On the Subject tab, the section titled *"Loyalty to the Jurchen Major Power of
Great Qing"* is a jumbled mess of text.

**Diagnosis (user: THE LOC/TEXT IS PERFECTLY CORRECT — this is purely a SPACING problem). The text
is all OVERLAPPING ON ITSELF:** the loyalty-breakdown lines render on top of each other (no vertical
line spacing / zero line height), so the correct words pile up illegibly. Not a broken string, not a
data-function, not wrapping-off-the-edge — the lines have no room BETWEEN them and collide.

**Fix direction (GUI spacing, not loc):** on the Subject tab (`gui/diplomatic_view.gui` subject panel),
find the textbox showing this loyalty section and give it proper VERTICAL room — the box is almost
certainly too SHORT for its multi-line content (a fixed small height, or a container with no
`spacing`/insufficient height) so the lines stack over one another. Fix: enlarge the textbox height /
set the container to size to content / add line spacing / ensure `multiline = yes` with a tall-enough
box, matching a cleanly-rendering multiline section elsewhere. Ties to BT-58 (same Subject-tab loyalty
area — fix together). Confirm the exact widget + needed height in-game; keep brace 0. NOT a loc edit.

---

## BT-60 🔴 (SCOPE — base map, not Qing mechanics) — USA borders are 1815, wrong for 1763
**Report (user):** The US borders don't look right for 1763 — they look like the 1815 map.

**Cause (setup/main/00_default.txt):** the 1763 bookmark still ships the full 1815-era USA — tag USA
with its territorial subjects `dependency = { first = USA second = MIC/ILL/MSI/MSP/IND
subject_type = territory }` and Indian protectorates `CHT/CHC/CHE/MSG/MIA` (L515-525). This is a
gross anachronism: in **1763 the United States did not exist** — the Declaration of Independence is
1776 and the Treaty of Paris 1783. In 1763 that territory was **British** (the Thirteen Colonies +
the post-1763-Treaty-of-Paris cessions), **French** (pre-1763 New France, ceded to Britain/Spain at
the 1763 Peace of Paris), **Spanish** (Louisiana/Florida), and **Native American** nations. The map's
country ownership + the USA dependency block were never rebased from the develop/1815 start to 1763.

**⚠️ SCOPE NOTE:** this is a BASE-MAP / political-setup problem (country ownership, tags, dependency
graph across all of North America), NOT a Qing-mechanics bug — it is large, touches the shared world
setup every nation sees, and is well outside the boot-test's Qing-panel focus. It likely belongs to a
dedicated "1763 New World political rebase" task, not the 1763_bookmark Qing bugfix pass. Options to
weigh (design decision needed): (a) full rebase — remove USA, assign North America to GBR/FRA/ESP +
Native tags per the 1763 Peace of Paris map; big undertaking; (b) minimum viable — if the mod is
Qing-focused and the New World is cosmetic backdrop, decide whether it's worth the effort at all, or
whether to leave a known-anachronism note. Flag to user for a scope/priority call BEFORE any work.
Related: the develop→1763 rebase (#304) rebased the QING side; the New World was evidently not
rebased. See [[imp19c-1763↔develop-merge]] / the USA/Japan/Mexico arc work ([[imp19c-usa-japan-mexico-arc-design]]).

**⚠️ REGRESSION / DISCREPANCY (important):** a fix DID exist — commit `bd5098ddb` "#289 — USA reverted
to its 1763 state" made USA a **GBR client_colony** (Thirteen Colonies British, released by
gbr_empire.3 "Loss of America" 1783) and split **Spanish Louisiana** to a new SPA/LSA tag. BUT current
1763_bookmark HEAD (`66421aa70`) STILL shows the 1815 `dependency = { first = USA second =
MIC/ILL/MSI/MSP/IND ... }` block (00_default.txt:515-525). So #289 either never merged into this branch
or was CLOBBERED by a later merge (f73a6d16f / fbd1c0736 ports pulled the 1815 default back over it).
This is why the user "thought the borders were adjusted a while back" — they WERE (#289), the change is
just not present in what's booting. FIRST STEP: git-diff 00_default.txt HEAD vs bd5098ddb to see whether
the #289 USA/LSA hunks survive, and restore them if lost. This likely means OTHER #289/#296/#297/#298
territorial fixes were also lost in the same merge — check them all (New Granada SFB hierarchy, Crimea
Qırım Giray, Persia Zand). Ties to BT-61 (full border audit).

---

## BT-61 🔴 (SCOPE — base map) — Russia owns Alaska in 1763 (too early) + audit ALL countries' 1763 borders
**Report (user):** Russia appears in Alaska, which is obviously wrong for 1763; and the user thought
the borders had been adjusted to 1763 a while back — so a COMPREHENSIVE all-country border check is
wanted.

**Russia/Alaska:** Russian America was not territorial in 1763 — only promyshlenniki fur-trade
expeditions in the Aleutians; the first PERMANENT Russian settlement was Kodiak 1784, and the
Russian-American Company was chartered 1799. So RUS owning Alaskan provinces at a 1763 start is an
anachronism (~20+ years early). Find which tag/provinces show Russian Alaska in setup and revert to
uncolonized / native.

**The broader task (audit):** the #289/#296 batch (bd5098ddb) corrected a TARGETED set (USA/Louisiana,
New Granada, Crimea, Persia, Bengal) — it was never a comprehensive world pass, AND per the BT-60
regression note some of those corrections appear LOST on current HEAD. So the map at large may still be
1815-era in many places. NEEDED: a systematic country-by-country border/ownership audit against the
1763 historical map (post-Seven-Years'-War / 1763 Peace of Paris), covering at least: North America
(British colonies, New France ceded, Spanish Louisiana/Florida, Russian Alaska = none), the 1763
Peace-of-Paris cessions globally, India (post-Plassey Bengal / Mughal successor states / Maratha
extent), the partitions-of-Poland-era Europe (pre-1772, so Poland-Lithuania still whole — check),
Ottoman/Persia/Crimea, and colonial holdings worldwide.

**⚠️ SCOPE:** base-map political rebase across ALL nations — LARGE, shared world setup, outside the
Qing bugfix focus. This is a dedicated audit+rebase project, not a 1763_bookmark quick fix. Needs a
user priority/scope call (full historical rebase vs. fix-the-worst-anachronisms vs. accept-as-backdrop
for a Qing-focused mod). First concrete deliverable = an AUDIT (list every tag whose 1763 ownership is
wrong) before any rebase work. Tracked as its own task. See [[imp19c-1763-no-create-country-needed]]
(static-setup rebase is proven, no mass create_country needed).

---
# LOG-DRIVEN FINDINGS (fresh 1763 boot, HEAD 66421aa70 — logs confirmed brand-new by user 2026-07-12)

## BT-62 — (WITHDRAWN) develop.mod in the log is just noise, NOT an override cause
**User correction (2026-07-12):** `imp19c-develop.mod` appearing in the log is just noise — it is NOT
overriding 1763_bookmark's files and is NOT the cause of any error. So DISREGARD the dual-mod-override
theory; do not chase it and do not tell the user to disable develop. The logs reflect the real
1763_bookmark code. (Consequence: the `qing_trib_gift` line-12/15 mismatch is NOT explained by an
override — if that cluster is genuinely live it needs its own look, but per the user the develop entry
is not the issue. Leaving it un-chased unless it resurfaces as a real symptom.)

## BT-63 🔴 — add_loyalty with RAW INTEGERS in QING_personnel_evaluate_governors (engine rejects)
**Finding (live in HEAD code, confirmed):** error.log — *"Can not find loyalty '3'"*, *"loyalty '1'"*,
*"'-2'"*, *"'-1'"* + *"add_loyalty effect [ loyalty was null ]"*, traced to
`00_monthly_country.txt:97 QING_GOV_pulse → QING_personnel_evaluate_governors` lines 38/63/78/99.
**Cause:** `common/scripted_effects/se_QING_PERSONNEL.txt` calls `add_loyalty = <integer>` at SIX sites
(lines 79 `=3`, 113 `=1`, 132 `=-2`, 157 `=-1`, 214 `=5`, 246 `=-10`). On a CHARACTER, `add_loyalty`
takes a NAMED loyalty modifier (e.g. `loyalty_qing_delta_p3` / `_n2` — the family defined in
common/loyalty/00_imp19c_loyalty.txt, as used by the BT-5/6 dynasty fixes), NOT a bare number. So every
one of these silently no-ops AND spams the error each quarter per governor.
**Fix (not yet applied):** map each raw value to the matching named modifier: `3→loyalty_qing_delta_p3`,
`1→loyalty_qing_delta_p1`, `-2→loyalty_qing_delta_n2`, `-1→loyalty_qing_delta_n1`, `5→loyalty_qing_delta_p5`,
`-10→loyalty_qing_delta_n10` (confirm each exists in 00_imp19c_loyalty.txt; the p1/p3/p5/n1/n2/n10 all
appeared in the earlier grep, so they do). Grep the WHOLE repo for other `add_loyalty = <int>` on
character scope while here — this pattern may recur elsewhere. Cheap, unambiguous, HEAD-confirmed live.

## BT-64 🔴 — "Illegal use of operator >/<" in QING_sphere / faction / council recompute (var vs local_var)
**Finding (user confirms these are legitimate bugs, not noise):** error.log — repeated
*"Illegal use of operator >"* / *"<"* traced to `QING_sphere_recompute_dominant` (lines 5/10/15),
`QING_sphere_bleed_one_power`, `QING_sphere_tick_state`, and `QING_council_recompute →
QING_faction_recompute` (lines 77/82), plus `QING_council_recompute line 168/172`.
**Cause:** `se_QING_SPHERE.txt` QING_sphere_recompute_dominant compares a saved variable against a
LOCAL var on the right — `limit = { var:britain_influence > local_var:top_val }` (lines 281/286/291),
same for france/russia. The engine's trigger parser rejects `var:X > local_var:Y` (comparing a variable
against a local_var operand this way is the "illegal use of operator" — the RHS local_var isn't a valid
comparison operand in that position). Same class in QING_faction_recompute (lines ~77/82) and
QING_council_recompute (168/172). Result: the sphere DOMINANT-POWER pick (china/britain/france/russia)
misfires — the four-power sphere calc is silently broken, and the faction/council tallies too.
**Fix direction (not yet applied):** rework the compares into an engine-legal form — e.g. store the
running max in a NON-local `set_variable` and compare `var: > var:`, or use `ordered_*`/`is_target_in_*`
max-pick idioms (the [[imp19c-sphere-idioms-oracle]] note documents the proven ordered_in_list max-pick
for exactly this four-power scoring — the recompute_dominant hand-rolled a var-vs-local_var compare
instead). Oracle-verify the legal comparison form (TI/Invictus) before applying. Affects #165 sphere +
#158 faction + council effectiveness — verify each recompute after fixing. Keep brace 0.
