# Boot-test notes — 1763_bookmark (2026-07-11)

**Branch under test:** `1763_bookmark` @ HEAD `0c795e2fe` ("#352 Boot-test findings: fix F1–F16").
**Scope:** the 1763 build **WITHOUT** any overnight / merge-overnight bureaucracy work.
**Note-taker checked out on:** `merge-overnight` (findings diagnosed against the `1763_bookmark` file state via `git show`).
**Tag series:** BT-1, BT-2, … (continues past the earlier B1–B27 / F1–F16 batches).

Status legend: 🔴 open · 🟡 diagnosed, fix pending · 🟢 fixed (uncommitted) · ✅ committed.

---

## BT-1 🟡 — loc ERROR on event "The Frontier Cannot Wait for Peking" (qing_frontier.10)

**Observed (user):** the event desc renders `Word comes from ERROR:[scope:target.GetName] of a crisis
already resolved…` — the `scope:target` reference prints `ERROR:` instead of the subject's name.

**Files:**
- Event: `events/imp19c_mod_events/qing_frontier_sea_events.txt:26` (`qing_frontier.10`, `is_triggered_only`).
  Uses `scope:target` in `desc`, `right_portrait = scope:target.current_ruler`, and the immediate LOG.
- Loc: `localization/english/qing_mechanics_l_english.yml:174` (`qing_frontier.10.desc`).
- Trigger site: `common/scripted_effects/se_QING_DECLINE.txt:1121`, inside a random_list `12 = { … }`
  weight block that does `random_subject { limit=NOT primary_culture=ROOT … save_scope_as = target }`
  then `trigger_event = { id = qing_frontier.10  days = { 3 12 } }`.

**Diagnosis:** `scope:target` is saved, then the event fires 3–12 days later. `ERROR:` at render means
the saved subject scope is not resolving at display time — most likely the subject went invalid across
the delay window (annexed/released/integrated) or the scope did not survive to the delayed fire.

**Candidate fixes (confirm vs debug.log "invalid scope" lines before choosing):**
1. ROBUST: persist the subject as a country variable at trigger time and reference it in loc via a
   GetVariable data-function (matches the mod's concrete-object idiom). Needs oracle check that a
   country-var renders in a loc string.
2. SIMPLE: fire with `days = 0` so scope:target is guaranteed live (loses staggered-arrival flavour).
3. CHEAP: add `exists = scope:target` (+ `scope:target = { is_subject_of = ROOT }`) to the event
   `trigger` so it skips silently instead of printing ERROR (hides symptom, drops the event if gone).

**Recommendation:** pending debug.log — lean option 1 if the scope is genuinely lost across the delay;
option 3 as a belt-and-braces guard regardless.

---

## BT-2 🟡 — book titles show literal markdown asterisks (`*Monarchs and Ministers*`) instead of italics

**Observed (user):** on the same qing_frontier.10 event, the citations `*Monarchs and Ministers*` and
`*Beyond the Pass*` render with literal asterisks rather than as italicised titles.

**Diagnosis:** Paradox loc does NOT render markdown. Italic emphasis uses the engine formatting tag
**`#i …#!`** (proven in vanilla `alerts_l_english.yml:43`, `game_concepts_l_english.yml:199`,
`general_tooltips_l_english.yml:42`, `interface_l_english.yml:1425`). The desc strings were authored
with markdown `*asterisks*`, which display verbatim. NOTE: `#i` italic support depends on the font
having an italic face — VERIFY IN-GAME that `#i` actually slants; if the mod's body font has no italic
variant, fall back to a colour/emphasis tag (e.g. `#v …#!` value-highlight or `#T …#!` title) or just
drop the asterisks to plain text. Pick whichever reads best on screen.

**Full scope of this bug class — 7 lines, all in `localization/english/qing_mechanics_l_english.yml`:**
| Line | Key | Literal titles |
|---|---|---|
| 60  | `qing_decline.14.desc`  | `*The Manchu Way*`, `*Illustrated Treatise on the Maritime Kingdoms*` |
| 110 | `qing_reform.30.desc`   | (title cite) |
| 174 | `qing_frontier.10.desc` | `*Monarchs and Ministers*`, `*Beyond the Pass*` ← the reported one |
| 208 | `qing_frontier.30.desc` | `*Zheng He*`, `*The Manchu Way*` |
| 220 | `qing_char.10.desc`     | (title cite) |
| 236 | `qing_char.20.desc`     | `*Passage to Power*`, `*Forging the Golden Urn*` |
| 266 | `qing_urn.1.desc`       | (title cite) |

(No other `qing*_l_english.yml` file has the pattern — this file only.)

**Fix:** replace each `*Title*` with `#i Title#!` (subject to the in-game italic-face check above).
Sed-safe since these are ASCII book titles; do all 7 in one pass. Cosmetic, batch with BT-1's file.

---

## BT-3 🟡 — REGRESSION: qing_dynasty.2 "The Crown Prince Proves Himself" still shows `ERROR:[scope:crownprince.GetName]`

**Observed (user):** the previously-reported ERROR on this event is BACK / never fixed — desc + portrait
show `ERROR:[scope:crownprince.GetName]`. (Was supposedly addressed by #352 F16.)

**Files:** `events/imp19c_mod_events/qing_dynasty_events.txt` — affects **three** events that all use the
same F16 pattern: `qing_dynasty.2` (line 71/81), `qing_dynasty.3` (line 112/125), and the event at
line 200/210. Gate trigger: `common/scripted_triggers/qing_dynasty_triggers.txt:38`
`QING_dynasty_has_crownprince`.

**Root cause — the F16 fix aimed at the wrong character:**
- The gate `QING_dynasty_has_crownprince` checks `has_variable = qing_office_crownprince_holder` AND
  `var:qing_office_crownprince_holder = { is_alive = yes }` — i.e. the DESIGNATED crown-prince variable.
- But F16 changed the scope save to `primary_heir = { save_scope_as = crownprince }`. `primary_heir` is
  the ENGINE's automatic succession heir — a DIFFERENT character, and one that may not exist at the fire
  moment. When `primary_heir` is empty, `save_scope_as` saves nothing → `scope:crownprince` unset →
  `ERROR:` at render. The gate passing (var is set) does NOT guarantee `primary_heir` exists.
- The F16 comment ("var-held scope fails loc-resolve") is a MISDIAGNOSIS: referencing `var:X` *directly*
  in loc/portrait fails, but **saving the var-held character into a named scope first resolves fine** —
  that IS the proven idiom (`var:qing_amban_here = { save_scope_as = qing_lifan_amban_char }` in
  se_QING_MINISTRY, referenced in memory).

**Recommended fix (all 3 events):** replace
`primary_heir = { save_scope_as = crownprince }`
with
`var:qing_office_crownprince_holder = { save_scope_as = crownprince }`
so the scope resolves the SAME character the gate validated. Also verify `qing_dynasty.3`'s
`current_ruler.mother = { save_scope_as = dowager }` against its `QING_dynasty_has_dowager` gate the same
way (mother may be dead/absent while a dowager var is set) — if the dowager is also a var, resolve it
from the var, not `current_ruler.mother`.

**Belt-and-braces:** also add `exists = scope:crownprince` guards are NOT possible pre-immediate, but the
var-resolve fix removes the failure mode entirely. Blocker-ish (breaks a recurring dynasty event's text).

---

## BT-4 🟡 — UX request: appoint by clicking the candidate ROW; delete the per-row Appoint button

**Observed (user):** the Grand Council Appoint picker now works and lists candidates correctly (good —
the earlier empty-list bug is fixed). Minor UX ask: instead of each candidate row having its own
"Appoint" button on the right, make **clicking anywhere on the candidate row** perform the appointment,
and **remove the button**.

**File:** `gui/imp19c_windows.gui` — the `qing_office_picker_window`, candidate `datamodel` at line 79.
Each `item` is a `widget { size={588 92} datacontext=[Scope.GetCharacter] }` (line 81) holding the
portrait + stat row, then a `widget { size={160 74} }` (line ~128) containing **13 per-office
`text_button_square_highlighted` appoint buttons**, each:
- `datacontext = "[GetScriptedGui('qing_gov_office_appoint_<office>')]"`
- `visible` gated on `GetVariableSystem.HasValue('qing_gc_picker_office','<office>')` AND that gui's
  `IsShown(... Character + player ...)`
- onclick: `ScriptedGui.Execute(... Character + player ...)` then `GUI.ClearWidgets qing_office_picker_window`.

**Implementation approach (for the fix phase — NOT done, note-only):**
Move the click behaviour onto the row `widget` (line 81) itself. Two viable patterns:
1. **Make the row `widget` a button** (or wrap its content in a `button`/give the widget an `onclick`),
   and put ALL 13 office-conditional onclick lines on it — each guarded the same way the buttons are
   today. Since all onclicks on a widget fire, but only the matching office's `ScriptedGui.Execute` is
   valid (others no-op because IsValid is false for the wrong office var), this reproduces the current
   dispatch. Then one final `GUI.ClearWidgets`. Delete the 13-button `widget` block.
   ⚠️ RISK: 13 unconditional `onclick` lines all execute; must confirm the wrong-office Execute truly
   no-ops (enabled/IsValid gate is on the button, but a raw widget onclick has no per-onclick enable).
   Safer variant: keep a single **generic** appoint scripted_gui that reads `qing_gc_picker_office`
   internally and dispatches — one onclick, no 13-way fan. Check whether such a generic verb exists;
   if not, this may be the cleaner build (one new scripted_effect switch on the office var).
2. Keep the button logic but make it fill the whole row (invisible full-row button) — least code, but
   hacky.

**Recommendation:** pursue a single generic `qing_gov_office_appoint` scripted_gui keyed on the office
var, wired to the row's onclick — cleanest and avoids the 13-onclick no-op risk. Verify the office-var
→ office-holder-var mapping + eligibility gate is expressible generically first. This is a real
GUI+scripted_gui change, not a one-liner. Cosmetic/UX severity.

**⚠️ Branch note:** this picker is SHARED with the overnight ministry work (the 13-office fan matches the
ministry appoint buttons). A fix here on 1763_bookmark will need reconciling with merge-overnight — flag
for the REG1 high-drift set in DEVELOP_MERGE_PLAN_2.md.

---

## BT-5 🟡 — "prestige" rewards add FAMILY prestige (reads "currently 0", appears inert); + consolidate spurs reward

**Observed (user):** on qing_dynasty.2 "The Crown Prince Proves Himself", option A "Let him earn his
spurs in the offices" — the rewards line shows **"The Family gains [N] prestige (currently 0)"** and the
family prestige stays at 0 after choosing it, despite the flavour promising the prince gains prestige.
Also: the option applies **+20 then +10** as two separate adds — the user wants them **consolidated to a
single +30**.

## BT-6 🟡 — same root cause on qing_tribute.1 "A Tribute Embassy at Peking"

**Observed (user):** option A "Receive them in full ceremony" — reward line shows **"The Family gains 8
prestige (currently 0)"**; family prestige sat at 0 immediately after the Crown Prince event supposedly
granted 20+10. So the "+8 Ruler Prestige" the tooltip promises is not visibly landing either.

**SHARED ROOT CAUSE (BT-5 + BT-6):** `add_prestige` in Imperator is the **FAMILY-prestige** effect.
Proof: `localization/english/effects_l_english.yml:177` —
`ADD_PRESTIGE_EFFECT_POSITIVE: "The '[FAMILY.GetName]' Family gains $VALUE Prestige (Currently: $CURRENT_VALUE)"`,
and `interface_l_english.yml:568` `CHAR_PRESTIGE_TOOLTIP` = "#T Family Prestige#!". So every
`current_ruler = { add_prestige = X }` / `var:qing_office_crownprince_holder = { add_prestige = X }`
in se_QING_DYNASTY.txt (lines 219/235/245/268/271/327/338/357/456/467/476), se_QING_EMBASSY.txt:162,
se_QING_RITES.txt:111 adds to the character's FAMILY prestige — the engine auto-appends the "Family
gains…" tooltip line, which clashes with the hand-written "the Crown Prince gains prestige (+20)" /
"+8 Ruler Prestige" flavour that implies PERSONAL standing.

**Why it reads "currently 0" and seems not to accrue:** family prestige / power-base is fundamentally a
REPUBLIC mechanic; in a monarchy (Qing) the imperial family's prestige is near-inert, not a headline
stat, and is subject to monthly decay — so small +8/+20/+30 additions to a base of ~0 are invisible or
decay away. It is NOT a broken command; it is the WRONG stat for the intended "ruler/heir glory" reward.

**Design decision needed (options — pick per feature intent):**
1. **Repoint to a stat that shows + matters for a monarchy.** For ruler/heir glory the natural targets:
   - `current_ruler = { add_prestige }` → keep flavour honest by rewording to "Family prestige", OR
   - swap to **country legitimacy** (`add_legitimacy` — COUNTRY scope, the monarchy standing stat,
     proven per memory), and/or **`add_popularity`** on the character (ruler popularity IS a visible
     monarchy character stat), and/or **`add_character_experience`**.
   - The tribute +8 "Ruler Prestige" likely wants `add_legitimacy` (suzerain standing) — note it already
     nudges `qing_suzerain_prestige` +7, so the add_prestige +8 may be redundant flavour anyway.
2. **Keep add_prestige but fix the LOC** to say "the Imperial Family gains N prestige" so the tooltip and
   flavour agree — cheapest, but leaves the reward inert-feeling in a monarchy.

**Consolidation ask (BT-5, definite):** in `QING_dynasty_prince_shines` (se_QING_DYNASTY.txt:263), the
option adds `add_prestige = 20` unconditionally then `add_prestige = 10` gated on finesse≥10/martial≥10.
The user wants a single **+30**. Cleanest: collapse to one `add_prestige = 30` (drops the skill gate),
OR if the skill-scaled bonus is intended, keep the branch but present it in the tooltip as "up to +30".
Confirm with user whether the finesse/martial gate on the extra +10 should be KEPT or dropped.

### RESOLVED DESIGN (user directive, 2026-07-11):
> "why is family prestige even being awarded as a bonus for state events… it should be a state award
> not a character or family award. Legitimacy would make more sense for tributary mission awards,
> prestige can work for the crown prince himself and his family."

So the two split cleanly by WHOSE achievement it is:

- **BT-6 — qing_tribute.1 (STATE / tributary-order event):** the reward is the STATE's, not a person's.
  → **Repoint `current_ruler = { add_prestige = 8 }` → a state award.** Best fit = **`add_legitimacy`**
    (COUNTRY-scope monarchy standing; proven per memory as a country effect). The event already nudges
    `qing_suzerain_prestige +7` (the tributary-order meter) — so the personal +8 becomes `add_legitimacy`
    to represent the throne's affirmed mandate. Update the tooltip "+8 Ruler Prestige" → "+N Legitimacy".
  → AUDIT the sibling STATE events for the same misuse: any `current_ruler = { add_prestige }` in a
    state/diplomatic/tributary context (se_QING_EMBASSY.txt:162, se_QING_RITES.txt:111, and the
    qing_frontier/qing_tribute event options) should likely be legitimacy too. List them before editing.

- **BT-5 — qing_dynasty.2 (DYNASTIC / the prince's OWN achievement):** family/character prestige is
  CORRECT here per the directive — the Crown Prince distinguishing himself IS a family-standing gain.
  → KEEP `add_prestige` on the prince (and his family). Just (a) make the LOC say "the Imperial Family's
    prestige rises" so the auto-tooltip ("The Family gains N prestige") and flavour agree, and
    (b) CONSOLIDATE the +20 + gated +10 into a single **+30** (per the user's earlier ask — confirm
    whether to drop the finesse/martial skill-gate or keep it as "up to +30").
  → NOTE the "currently 0 / doesn't accrue" concern: family prestige in a monarchy is near-inert +
    monthly-decayed, so even a correct +30 may barely move the bar. Acceptable per directive (prestige
    "can work" for the prince), but flag that the number will look small — if the user wants it to feel
    impactful, layer a small `add_popularity`/`add_character_experience` on the prince too.

**Scope of the state-vs-dynastic audit (do in the fix phase):** grep every `add_prestige` in
se_QING_*.txt, classify each call as STATE-context (→ legitimacy) or PERSONAL/dynastic (→ keep prestige),
and fix + reword loc accordingly. Applies to BOTH branches (predate overnight; shared with merge-overnight).

---

## BT-7 🟡 — qing_tribute.1 "A Tribute Embassy at Peking": multiple broken loc scope refs
**Observed (user):** desc shows `ERROR:[scope:trib_sender.GetName]`, `ERROR:[scope:trib_envoy.GetName]`,
and `ERROR:[ROOT.Custom('get_country_formal_adjective')]`.
**File:** `events/imp19c_mod_events/qing_tribute_events.txt` (qing_tribute.1, line 30). Scopes saved in
`se_QING_TRIBUTE.txt` QING_tribute_schedule_missions: `random_subject { save_scope_as = trib_sender }`
then inside `ROOT = { QING_tribute_mint_envoy ...; trigger_event = { id = qing_tribute.1 days = { 5 20 } } }`.
**Diagnosis:** SAME systemic class as BT-1/BT-3 — scopes saved, then event fires 5–20 days LATER; the
saved `trib_sender`/`trib_envoy` scopes don't survive the delay to render time → ERROR. The
`get_country_formal_adjective` Custom is a third broken ref (either the Custom loc is undefined or it's
being called on a scope that's likewise unresolved). Event .1 HAS `exists = scope:trib_sender/trib_envoy`
in its trigger, so it should skip if truly gone — but ERROR at render means the scope is present-but-
unresolvable OR the trigger's exists passes while the loc-layer resolution fails (the var-held-scope
loc-resolution gotcha). NEEDS: confirm envoy is minted as a saved-scope char that persists; likely fix =
persist envoy+sender as country vars and re-save to named scopes in the event's OWN immediate before desc
renders (the proven `var:X = { save_scope_as = Y }` idiom), OR fire with days = 0.

## BT-8 🔴 — SYSTEMIC: event loc scopes broken across the board (delayed trigger_event scope loss)
**Observed (user):** "The War Minister's Report" shows `ERROR:[scope:officer_report_minister.GetName]`
and `ERROR:[scope:officer_report_commander.GetName]`. User notes "localizations are consistently broken
across the board for events."
**File:** qing_office.31 (`events/imp19c_mod_events/qing_office_events.txt:845+`). Scopes saved in
`se_QING_COUNCIL.txt` QING_council_officer_report_check (commander→officer_report_commander line 1308,
war/guard holder→officer_report_minister lines 1325/1330). NOTE: this one appears to fire IMMEDIATELY (no
days= delay visible at the check) — VERIFY whether qing_office.31 is trigger_event days={...} or same-tick.
If same-tick and STILL erroring, the root is NOT delay but something else (scope saved in a sub-scope not
propagated to the country event, or a var-held-scope loc-resolve failure).
**Diagnosis — the umbrella class (BT-1, BT-3, BT-7, BT-8):** every custom Qing event that renders
`scope:X` in desc/portrait is at risk. TWO distinct mechanisms to separate during the fix phase:
  (A) DELAYED-FIRE scope loss — scope saved, `trigger_event days = { N M }`, scope invalid/dropped by
      fire time (BT-1 frontier.10, BT-7 tribute.1). Fix = persist as country var + re-save to scope in
      immediate, or days=0.
  (B) VAR-HELD-SCOPE loc-resolution — referencing `var:X` (or a scope saved FROM a var) directly in loc
      fails to resolve even when the char is alive (BT-3 crownprince). Fix = `var:X = { save_scope_as = Y }`
      in immediate, reference `scope:Y` in loc.
  ⇒ FIX-PHASE ACTION: audit EVERY custom qing_*.txt event's desc/left_portrait/right_portrait for
    `scope:` refs; for each, confirm the scope is saved in the event's OWN immediate (not only at a
    delayed trigger site) and re-saved from any var. This is a single systematic sweep, not N ad-hoc fixes.

## BT-9 🔴 — Qing ruler displays as "Yongrong", not "Qianlong Emperor"
**Observed (user):** the emperor's name shows as Yongrong, not the Qianlong Emperor.
**File:** `setup/characters/00_Qing.txt` — char:214 (Qianlong) has `first_name="Qianlong Emperor"`,
`c:CHI = { set_as_ruler = char:214 }` (line 470-472), death_date already stripped (#329). Yongrong is a
SON of Qianlong (Prince Zhi 質莊親王, personal name 永瑢 Yongrong, b.1743). So the throne resolved to a
DIFFERENT character than char:214 — the set_as_ruler is not taking, and the engine auto-picked an heir
(Yongrong) instead. SAME CLASS as #329 (RUS Catherine set_as_ruler not taking).
**Candidate causes to check in fix phase:** (1) is char:214 actually alive at 1763.2 (birth 1711, no
death_date — should be); (2) does another later block re-`set_as_ruler` CHI to someone else, or a
succession law/regency auto-run overriding at boot; (3) is Yongrong (find his char ID) carrying a
`set_as_ruler` or a `father=char:214` + heir-designation that the engine prefers; (4) load-order: is the
1763 bookmark's set_as_ruler being clobbered by the 1815 baseline block. GREP for every set_as_ruler=CHI
and for Yongrong's char entry. 🔴 blocker — wrong emperor on the throne at start.

## BT-10 🟡 — event spam: same event re-fires within a year; want one Grand-Council event per quarter
**Observed (user):** "A Tribute Embassy at Peking" fired AGAIN very soon after the first; "The Crown
Prince Proves Himself" fired twice in short succession. RULE the user wants:
  - the SAME event should not fire more than once a YEAR (possibly longer);
  - to cut spam, only ONE Grand-Council-family event should fire per QUARTER (across the whole set).
**Diagnosis:** two throttles are missing/insufficient:
  (a) PER-EVENT cooldown — each recurring event needs a per-event "last fired" var/timer gate (e.g.
      set a var with days=365 on fire, gate the scheduler on NOT has_variable). qing_tribute.1 DOES stamp
      a per-SUBJECT cooldown (qing_tribute_cooldown days=1825) — but if MULTIPLE subjects are due, each
      fires its own embassy in quick succession (looks like "the same event twice"). Crown-Prince
      (qing_dynasty.2) likely has NO per-event cooldown at all → fires whenever its gate passes each pulse.
  (b) GLOBAL Grand-Council QUARTERLY budget — a single "a GC event fired this quarter" flag set by ANY
      of the council/dynasty/tribute/office events, checked by all of them, cleared once per quarter, so
      at most one fires per quarter. NEW cross-cutting throttle to design.
**FIX-PHASE ACTION:** (1) give qing_dynasty.2/.3 + the officer-report + tribute a per-event annual
cooldown var; (2) if multiple tributaries can be due same pulse, stagger or cap to one embassy per pulse;
(3) add a shared quarterly GC-event budget flag. Confirm the exact event set to include in the budget.

## BT-11 🟡 — vanilla "[tributary] cannot afford to send tribute" should tie into Lifan Yuan + add a punish/forgive follow-up
**Observed (user):** the vanilla event where a tributary cannot afford tribute should be tied to the
Lifan Yuan functionality, and there should be a FOLLOW-UP event letting the player decide how to punish
(or forgive) the defaulting tributary.
**FIX-PHASE ACTION (design + build, NOT a bugfix):**
  - Locate the vanilla "cannot afford tribute" event (grep vanilla events for tribute/afford). Hook it so
    that when it fires for a CHI tributary it routes through the Lifan Yuan (理藩院) system — e.g. degrade
    that subject's amban affinity / the tributary-order meter (qing_suzerain_prestige) / integration.
  - Author a NEW follow-up CHI country_event offering: PUNISH (loyalty/opinion hit, tighten grip, maybe
    demote subject type) vs FORGIVE (goodwill, legitimacy, tributary-order bump). Wire via trigger_event
    from the vanilla event (or an on_action hook if the vanilla event is not is_triggered_only).
  - Respects BT-10 throttle (counts as a GC/tribute event for the quarterly budget).

---

## BT-12 🟡 — Appoint-to-Office picker: mark candidates already on the Council; drop the current holder
**Observed (user):** in the Grand Council "Appoint to Office" window, candidates who ALREADY sit on the
Grand Council in another role should be clearly MARKED as such, and the CURRENT holder of the office being
filled should NOT appear as a candidate at all.
**Files:**
- List builder: `se_QING_COUNCIL.txt` — QING_council_refresh_candidates (line 799) and
  QING_council_refresh_candidates_by (line ~845). Per the #314 B7 fix, the list DELIBERATELY INCLUDES
  sitting office-holders (so the player can reshuffle one minister into another seat). Eligibility =
  employer=ROOT, is_adult, is_alive (the "_by" variant dropped the old `NOT = has_variable qing_office_held`).
- Per-office appoint verb: `common/scripted_guis/QING_governance_actions.txt` — e.g.
  qing_gov_office_appoint_chancellor (line 48): `is_valid` has `NOT = { var:qing_office_held = flag:chancellor }`,
  so the man who holds THIS office is un-appointable — but is_valid only DISABLES the button; the row still
  RENDERS. So the current holder shows as a greyed candidate, and other council members show unmarked.
- Picker window: `gui/imp19c_windows.gui:37` qing_office_picker_window, candidate row at line ~81.
**Two asks — fix-phase plan:**
  (1) MARK council-sitters: add a visible badge/text on the row when the candidate `has_variable = qing_office_held`
      (i.e. currently holds SOME office). Loc it (e.g. "(on the Council — [office])"). GUI-only: a text/icon
      widget on the row gated on `[Character.MakeScope...HasVariable('qing_office_held')]`, or expose the held
      office via a data-function for the label. Keep the reshuffle ABLE (don't remove them) — just flag them.
  (2) DROP the current holder of the office being filled: the man whose qing_office_held == the picker's
      qing_gc_picker_office should not be listed. Cleanest = exclude him IN THE LIST BUILDER
      QING_council_refresh_candidates_by, which already knows the target office (it's passed the sortval /
      office context) — add `NOT = { var:qing_office_held = flag:$office$ }` to the ordered_character limit so
      the sitting holder of THAT seat is filtered out up front, while holders of OTHER seats remain (marked
      per ask 1). Confirm the "_by" verb receives the office literal (it takes $sortval$; may need the office
      key threaded through, or read the GUI var qing_gc_picker_office inside the effect).
**Severity:** UX/clarity. Not a crash. Depends on BT-4 (row-click appoint) — do them together since both
touch the same picker row widget.

## BT-13 🔴🔴 BLOCKER — appointing a Grand Chancellor VACATES the entire Council; refilling then fails
**Observed (user):** clicked Appoint on the Grand Chancellor seat, picked a character → ALL Grand Council
offices were vacated. Trying to refill the now-empty offices also fails: the candidate list displays, but
clicking a candidate does NOT appoint them.
**Files (merge-overnight):**
- GUI onclick: `gui/imp19c_windows.gui:128-141` — chancellor row button runs
  `ScriptedGui.Execute( SetRoot(Character).AddScope('player', Player) )` then `GUI.ClearWidgets`.
- Verb: `QING_governance_actions.txt:48` qing_gov_office_appoint_chancellor → effect calls
  `QING_office_appoint = { office = chancellor }`.
- Appoint core: `se_QING_COUNCIL.txt:1043` QING_office_appoint. At line 1058-1064 it calls
  QING_office_vacate_dispatch IF the appointee already holds a DIFFERENT office.
- Dispatch: `se_QING_COUNCIL.txt:1186` QING_office_vacate_dispatch → per-office QING_office_vacate (1149+).
**Diagnosis — TWO candidate mechanisms (confirm against the FRESH debug.log the user will supply):**
  (1) MASS-VACATE on chancellor appoint. Hypotheses, in order of suspicion:
     a. The appointee picked for Chancellor was HIMSELF a sitting office-holder (BT-12: the list now
        includes council-sitters). QING_office_appoint fires QING_office_vacate_dispatch on him (correct,
        relieves his OLD seat) — but if `this`/`employer`/`prev` scope is mis-threaded through the
        chancellor path, the vacate could cascade. Chancellor is the ONLY office scored via a SEPARATE
        path (QING_council_score_chancellor, not QING_council_score_office) — a likely asymmetry source.
     b. `set_variable = { name = qing_office_$office$_holder value = prev }` (line 1086) relies on `prev`
        resolving to the appointee inside the `employer = { }` block; if `prev` mis-resolves for the
        chancellor call, the holder var is set wrong → the recompute/refresh sees every seat as vacant.
     c. A `qing_office_vacancy_strain` / autofill interaction: appoint removes vacancy strain (1085) then
        recompute runs — but autofill is NOT called from appoint, so a mass re-vacate must be explicit.
  (2) REFILL FAILS (click candidate = no appoint). After the cascade, clicking a candidate for another
     office does nothing. Likely the picker's qing_gc_picker_office GUI var is stale/wrong so NO office's
     button matches (visible= gate fails → the row's onclick Execute never fires), OR the is_valid PI gate
     now fails (chancellor appoint spent 20 PI; if PI < 20 every subsequent appoint is invalid and silently
     no-ops with only a tooltip). CHECK: does refill fail for ALL offices or only some? Is PI exhausted?
**FIX-PHASE PRIORITY: HIGHEST.** This breaks the core Grand Council loop. Needs the fresh debug.log to see
the QING_office_appoint/vacate LOG_line trace at the moment of the chancellor click. Do NOT fix blind —
the two mechanisms have different fixes. Likely related to BT-12 (list now includes sitting holders).

## BT-14 🔴 — Religion window STILL empty except the centred "Faith & Sedition" header
**Observed (user):** the Qing religion window shows only the "Faith & Sedition" header in the middle; the
body is empty. This is a RE-REGRESSION — was filed + "fixed" as #328 / R2-20 (task #345, Bug 6).
**File:** the religion panel GUI (grep "Faith & Sedition" / faith_sedition / qing_religion window). The
prior fix (#345) populated the body; it is empty AGAIN on this branch → either the fix didn't land on
merge-overnight, or a later edit reverted/renamed the datacontext the body binds to.
**✅ ROOT CAUSE FOUND + FIXED (2026-07-11, NOT layout — the real bug at last).** The panel is
gui/qing_religion.gui window `qing_religion_panel`; it opens fine (header renders) and error.log (Downloads)
has NO parse error on it. THREE prior "fixes" (#328/#345 greatgame-mirror, then TI-nested, then sibling-
margin) all rewrote the OUTER scaffold and all failed — because layout was never the cause. A byte-level
structural diff vs the proven-rendering twin gui/qing_greatgame.gui showed the scaffolds were byte-identical
through scrollarea>scrollwidget EXCEPT ONE line: religion put `layoutpolicy_horizontal = expanding` on the
flowcontainer that is the DIRECT child of `scrollwidget` (line 98). The working twin gives its equivalent top
flowcontainer NO layoutpolicy at all — it shrinks to content width and the scrollwidget sizes to it. A
scrollwidget's direct child sized by `expanding` tries to expand into a scrollwidget with no intrinsic width,
collapsing the whole body to zero → only the header shows (and floats mid-panel, the collapsed-body symptom).
Every prior rewrite carried this same offending line on the inner flowcontainer while shuffling the outer
scaffold, so the body kept collapsing. **FIX:** removed the `layoutpolicy_horizontal = expanding` from the
scrollwidget's direct-child flowcontainer (the `expanding` policy stays ONLY on the nested SECTION
flowcontainers, which have a defined-width ancestor — exactly as greatgame does). Left a loud
do-NOT-re-add comment at that line. Braces 97/97. Pending in-game verify.
NOTE on the F9 diagnostic: the `debug_log = "QING F9: religion panel open."` in QING_religion_panel.txt did
NOT fire in the boot log — because the button opens the window via `gui.createwidget` (a console command),
which BYPASSES the scripted_gui `effect` block entirely. A panel-open LOG can't be captured this way; that's
a dead diagnostic, not evidence the panel failed to open.

<!-- BT-15 REVIEW-FIX (2026-07-11, post adversarial review of the uncommitted diff):
  Finding 1 (HIGH) RESOLVED: my BT-15 edit had wrapped the land create_unit in `c:CHI = { }`.
  That is a REDUNDANT re-entry (SE_qing_armies already runs in c:CHI via qing_force_setup.1) AND
  it is the exact idiom the navy fix (SE_qing_navy_guangdong ~L408) recorded as re-resolving the
  absolute location to inland Beijing — the recurring #224 blocker. Changed all 3 land sites
  (SE_qing_raise_garrison + both _cmd branches) to a BARE create_unit in the ambient c:CHI scope:
  still CHI-controlled, no Beijing re-resolution, matches this file's header idiom #1 and the bare
  navy squadrons. Brace-balanced, LF preserved.
  Findings 2 & 3 = BOOT-TEST VERIFY items (not code defects): (2) confirm the 4 subject-owned
  frontier garrisons (Ili p:3534, Ürümqi p:2930, Kashgar p:2700, Heilongjiang p:43) actually spawn
  as CHI units on subject soil — bare-create-in-CHI-scope on another country's province is the
  untested case; if any vanish in debug.log, the owner-scope form was the working one for those.
  (3) Kashgar p:2700 owner XNG is a SUB-subject (overlord ILI, not CHI) — confirm is_subject_of=c:CHI
  is transitive; if not, that garrison's guard fails regardless (pre-existing #331 line, not a regression).
-->
## BT-15 🔴🔴 BLOCKER (RECURRING — user flags as MOST serious) — army & navy setup spawn — FIXED (uncommitted, pending in-game verify: navy is_port swap + garrison CHI-control flip; see the CONFIRMED ROOT CAUSE + LAND blocks below)
**User note:** "I don't see the army or navy bugs on the list, which are the most serious and recurring."
These are tracked in `BOOT_TEST_BUGS_2026-07-11.md` (REGRESSION-B21 / B22) + tasks #338/#331; logging here
so the boot-test list is COMPLETE.
- **B21 — garrisons:** THIS test (user, 2026-07-11) = PARTIAL WIN. Many garrisons now spawn in CORRECT
  locations across CHI (not all piled on Beijing); some have commanders, some don't. BUT: **no garrisons
  spawned in any CHI SUBJECTS** (frontier subject-owned provinces got none). The last fix (B21-v3,
  bare-country-scope + absolute location, no province→owner wrapper) fixed the CHI-core dispersal but the
  SUBJECT-owned garrisons (raised in the frontier subject's own country scope) are still absent.
- **B22 — navy:** THIS test = STILL BROKEN. Only ONE navy spawned — the Fujian coastal patrol again.
  Guangdong + Zhejiang squadrons still missing, despite the B22-v3 fix (all 3 in a bare c:CHI scope,
  Invictus me_tasm.13 idiom). So either the fix didn't land on the tested branch, or the bare-c:CHI
  three-in-one-tick spawn STILL culls to one on THIS engine/build.
- **COMMANDER assignment (user, 2026-07-11) — ROOT CAUSE FOUND + resolved by the BT-15 CHI-control flip:**
  There were TWO distinct reasons for the "some have commanders, some don't" mix:
  (1) Was DELIBERATE (9 of 27 pre-1772 garrisons used the bare no-cmd verb) → NOW FILLED per user
      direction "all garrisons should have commanders, use plausible minor officials if you can't find
      exact historical names." Added 9 new setup characters and converted all 9 bare raises to `_cmd`.
      [BT-20 CLEAN-REDO 2026-07-11] The FIRST attempt appended them at ids 592-600 AND renumbered the
      existing Qing 601-609 chars onto ids 354-358/425-426/459-460 believing those were free gaps — they
      were NOT (occupied by Japan's Tokugawa shogun 356 / Emperor Kōkaku 459 / Ayahito 460, plus India /
      Italy / North America / Persia chars), creating 9 cross-file DUPLICATE ids that re-created the exact
      silent-misbinding hazard BT-20 fixes. That renumber was fully REVERTED. The clean redo places the 9
      new commanders into the 9 REAL pre-existing gap ids in 00_Qing.txt (147-153, 164, 165) — NO existing
      character moves, so no char:N ref shifts. Global space is now contiguous 0..609, zero gaps, zero
      cross-file dupes. Mapping: Fuzhou→Cangbao 蒼保 (147), Ningxia→Deltai 德爾泰 (148), Liangzhou→Fusen 富森
      (149), Kaifeng→Bujantai 布占泰 (150), Taiyuan→Yehetu 葉赫圖 (151), Suiyuan→Chinggeltei 青格勒圖 (152,
      Mongol), Heilongjiang→Fusengge 傅森格 (153), Fujian Green Std→Wu Bida 吳必達 (164, Han/min), Taiwan
      Green Std→Lin Jun 林俊 (165, Han/min). Banner posts = Manchu/Mongol generals; Green Standard = Han.
      All marked "(plausible)"
      — representative period officers where the exact 1763 post-holder isn't firmly attested. All
      CHI-employed (default block), no death_date. So the pre-1772 OOB is now 27/27 commanded. NOTE: the
      1815-start branch (else) keeps its bare raises by design (user chose 1763-only; 1815 needs a separate
      roster).
  (2) A REAL DROP that BT-15 fixed — the 3 FRONTIER `_cmd` garrisons (Ili p:3534 / Urumqi p:2930 /
      Kashgar p:2700) sit on provinces owned by the **ILI subject** (00_default.txt:36018 ILI own_control_core),
      but their commanders (Mingrui char:582 / Šuhede 583 / Hailancha 584) are CHI-employed. The OLD code
      raised the unit in `scope:garrison_owner` (= ILI) and gated the commander on `employer = scope:garrison_owner`
      (= ILI) — so those 3 CHI officers FAILED the guard and the garrisons mustered commander-less. The BT-15
      flip (create in c:CHI, guard on `employer = c:CHI`) now PASSES for all 18 `_cmd` garrisons including the
      3 frontier ones, so they attach their historical commander AND are Qing-controlled. All 18 `_cmd`
      officers verified CHI-employed (no employer override → default 00_Qing.txt CHI block); all death_date
      stripped so none age out in the 31-day setup→raise gap. Net: after BT-15, exactly the 9 intended
      bare-raise garrisons are commander-less; every `_cmd` garrison has its commander. Pending in-game verify.
  - FUJIAN navy: has NO commander. The one navy that DOES spawn (B22) is commanderless. Per memory the
    Fujian navy commander should be Gan Guobao (甘國寶). Either the navy raise verb uses the no-commander
    form, or the assigned commander char failed to attach (death_date / invalid at setup). Note:
    commanderless units are ENGINE-VALID (Invictus 203:66) — so this is a roster-completeness issue,
    not a spawn blocker. Fold into the B21/B22 fix once the fresh debug.log shows the commander= traces.
- **File:** `common/scripted_effects/imp19c_effects_legion_setup.txt` — SE_qing_raise_garrison / _cmd (~94/135),
  SE_qing_navy_guangdong/_fujian/_zhejiang (~360), SE_qing_navy_disband (~334); wired qing_force_setup.1/.10/.11.
- **FIX-PHASE:** needs the FRESH debug.log — B22 especially hinges on whether the 3 navy scripts log
  "raised" (created-then-culled) or fail outright. For B21-subjects: confirm the subject-owned garrison
  branch resolves the subject's country scope (not CHI) and that the subject actually owns the location
  province at setup. HIGHEST priority tier alongside BT-13.

### BT-15 CONFIRMED ROOT CAUSE (from fresh debug.log + error.log 2026-07-11, tested @ 0c795e2fe)
**NAVY (B22) — SOLVED, root cause found.** error.log has exactly two rejections:
```
create_unit effect [ Trying to create naval unit where it does not belong: PROVINCE,7190 Zhuhai ]   (SE_qing_navy_guangdong, line 5)
create_unit effect [ Trying to create naval unit where it does not belong: PROVINCE,2968 Xiangshan ] (SE_qing_navy_zhejiang, line 5)
```
Only the Fujian squadron (Fuzhou p:3651) survived — that is why "only one navy spawns."
The bare-c:CHI three-in-one-tick idiom was NEVER the problem; the multi-navy fix (#314 B22) works.
The real fault: **`is_coastal = yes` is TRUE for river/lake-adjacent provinces and does NOT guarantee a
province borders a real SEA ZONE.** Zhuhai (7190, tested) / Xiangshan (2968) — and on merge-overnight
Canton (9298, a Pearl-River port) — pass `is_coastal` but the engine refuses to base a navy there.
The PROVEN port predicate is **`is_port = yes`** (province trigger, common/unit_abilities/naval_raiding.txt:67)
— the ONLY proven port predicate in the codebase; it is what distinguishes a sea-zone-bordering province
from a merely river-coastal one. Fuzhou p:3651 (which succeeded) is `is_port`; Zhuhai/Xiangshan/Canton are not.

**FIX (both branches; the branches use DIFFERENT hardcoded IDs so verify each):**
1. In SE_qing_navy_guangdong / _fujian / _zhejiang, change the PRIMARY-berth `limit` from
   `{ owner = c:CHI  is_coastal = yes }` to `{ owner = c:CHI  is_port = yes }`.
2. In the FALLBACK branches, change `is_coastal = yes` -> `is_port = yes` in BOTH the any_owned_province
   guard AND the ordered_owned_province limit. This makes the fallback self-correct: if the hardcoded
   primary ID is a river port (fails is_port), the fallback now auto-picks a genuine SEA port by population,
   excluding the other two home ports. No new hardcoded IDs required — is_port makes the existing fallback
   robust. (merge-overnight primary IDs = Canton 9298 / Fuzhou 3651 / Ningbo 2893; tested-branch = Zhuhai
   7190 / Fuzhou 3651 / Xiangshan 2968. Fuzhou is the only proven-good one; the other four need the
   is_port fallback to relocate them.)
3. Fujian navy commanderless: char:596 (Gan Guobao 甘國寶; PRE-EXISTING #331 navy commander, unchanged by the clean BT-20 fix) attach — check debug.log for the commander=
   drop (setup death_date breaks create_unit commander=, memory imp19c-1763-commander-roster). The
   two-step save_scope_as + set_as_commander form (proven) is more robust than inline commander=.

**LAND (B21) — CORRECTED (user 2026-07-11) → FIXED.** Earlier note said "no subject garrisons spawned; a
coverage gap." The USER corrected this: subject garrisons DID spawn — but under the SUBJECT's control, when
they should be QING-controlled (the Son of Heaven garrisons the marches). ROOT CAUSE: both raise helpers
(SE_qing_raise_garrison / _cmd) saved `$prov$.owner` as scope:garrison_owner and issued `create_unit` in
THAT scope, so a subject-owned frontier province (Ili/Xinjiang/Tibet) produced a subject-owned garrison.
FIX APPLIED (this session): issue `create_unit` in the **c:CHI** scope ALWAYS. The absolute `location = $prov$`
token resolves globally regardless of the creating scope (proven by TI galatian_invasion — the issuing
country places its OWN unit on a non-owned province — and se_QING_ILI raising at frontier provinces the
same way), so every garrison is now CHI-owned while still standing on its intended frontier province. The
`_cmd` commander guard changed from `employer = scope:garrison_owner` to `employer = c:CHI` (a CHI-owned
legion cannot be led by a subject's officer); a non-CHI-employed frontier commander now musters the CHI
garrison commanderless (engine-valid). scope:garrison_owner is fully removed. Braces 311/311. Pending
in-game verify that frontier garrisons now show under Qing control.

## BT-16 🟡 — "Type: Autonomous Governorship" label too small + misaligned vs the other subject types
**Observed (user):** in the Qing diplomatic view Subjects tab, "Type: Autonomous Governorship" renders
SMALLER and misaligned compared to "Type: Protectorate" / "Type: Feudatory" on subjects of those types.
**Root cause (found):** the label widget is `only_text { size = { 220 32 } }` at
`gui/diplomatic_view.gui:2802` (the subject-type SelectLocalization). The `only_text` template
(`gui/shared/gui_templates.gui:93-124`) has an inner textbox with `fontsize_min = 13`, `elide = right`,
`align = left|nobaseline`, `using = BaseFontM`. When the label string is too long to fit the 220px box at
full BaseFontM, the engine SHRINKS the font down toward fontsize_min to make it fit — and the shrink
shifts the vertical position. "Type: Autonomous Governorship" (~29 chars) overflows 220px, so it renders
at a reduced font; "Type: Feudatory" / "Type: Protectorate (羈縻)" are short enough to render at full
BaseFontM. All five loc strings share identical `#Y …#!` formatting (00_subject_rework_l_english.yml:73-77),
so it is NOT a loc-content difference — purely the fixed box width vs string length.
**NOTE:** there is a SECOND copy of the same subject-type label at `diplomatic_view.gui:1552` (size not
yet checked) — verify whether it has the same width and fix both if so.
**FIX (fix-phase, GUI-only, low-risk):** widen the `only_text` container at :2802 (and :1552 if same)
from `size = { 220 32 }` to enough to fit the longest label at full font — "Type: Autonomous Governorship"
needs ~300px. Set `size = { 300 32 }` (confirm it doesn't collide with the adjacent `widget { 60 35 }`
spacer / the interaction row; if space is tight, shorten the loc to "Type: Autonomous Gov." OR accept the
label wrapping). Simplest robust fix = widen the box; re-check in-game that all five types now render at
the same font size + baseline. Cosmetic severity.

## BT-17 🟡 — Subjects-tab: empty integration bar; move progress readout to single-subject view
**User directive (DO):** on the Subjects tab (iterated list, datacontext=Country) there is an empty
integration bar — REMOVE it (diplomatic_view.gui:2729-2787). But integration progress must still be
shown on the single-subject diplomatic view: as a numeric "progress/total" (X / 5) counter surfaced on
HOVER of the greyed-out Integrate button under Subject Actions. Refinement: the Integrate button should
be greyed while integration is IN PROGRESS (that is the only time progress needs showing); the counter
should ALSO be shown over the not-greyed Resume button when integration is PAUSED (suspended).
Single-subject bar already exists at diplomatic_view.gui:1555-1575 (DiplomaticView.GetTargetCountry).

## BT-18 🟡 — Subjects-tab: amban icon-strip cleanup (Recall/Replace)
**User directive (DO):** the Subjects tab shows Recall-the-Amban + a redundant lower Replace-the-Amban
icon (diplomatic_view.gui:2942-2981), while a HIGHER Replace icon sits to the right of the portrait
(:2625-2643). Move Recall UP to the LEFT of the higher Replace icon; REMOVE the lower redundant Replace.

## BT-19 🟡 — Amban recall/replace should cost tyranny (+ recall 10 PI)
**User directive (DO):** both Recall and Replace the Amban should cost a small amount of TYRANNY
(direct intervention in the bureaucracy). Recall should ALSO cost 10 political influence instead of 0.
Edit the scripted_gui effects: qing_amban_manage_recall_button / qing_amban_manage_replace_button.

## BT-20 🔴 — Emperor shown as Yongrong (prince, age 19) with a 2-yo "mother" Xiaoshurui — set_as_ruler not taking
**Observed (user):** in-game the current emperor displays as Yongrong (in-game id 275), aged 19, whose
"mother" Xiaoshurui (in-game id 214) is aged 2. Setup identities by age: char:214 = Qianlong (b.1711,
the intended `set_as_ruler=char:214` target, 00_Qing.txt:471); char:284 = Yongrong (b.1744.01.28 → 19 in
1763); char:223 = Xiaoshurui (b.1760.10.02 → ~2-3 in 1763). So `set_as_ruler=char:214` is NOT taking and
the engine auto-picked a prince as ruler (the #329 / BT-9 / F16 class). In-game ids (275/214) differ from
setup ids (284/223) — suspect the NEW-B27 renumber (commit dadbf3283) left a dangling reference OR the
death_date-strip on 214 didn't fully land in the tested build. NEEDS root-cause: confirm char:214 loads
as alive at 1763.2.16 and no competing assignment. HIGH — wrong monarch is the most visible possible bug.

### BT-20 ROOT CAUSE — GLOBAL char-id GAP compaction (CORRECTED 2026-07-11) → FIXED
The earlier "constant −9 renumber triggered by CHI's internal 123→183 gap" write-up was WRONG
(that gap pre-dated the bug, and a uniform per-country shift would be self-consistent and wouldn't
mis-bind). CONFIRMED mechanism: the engine COMPACTS the **GLOBAL** setup character-id space at load —
a character's runtime id = its written id − (count of missing ids anywhere below it across ALL
setup/characters/*.txt). The global space had 18 missing slots (gaps 147-153, 164-165, 354-358,
425-426, 459-460); **9 of them below 214**, so setup-214 Qianlong→runtime 205, setup-223
Xiaoshurui→runtime 214, setup-284 Yongrong→runtime 275 — reproducing the user's exact reported ids
(emperor 275, "mother" 214). `set_as_ruler=char:214` thus seated Xiaoshurui (2yo); the engine
promoted her adult kin Yongrong; his `father="char:214"`→runtime-214=Xiaoshurui = the "2-year-old
mother." This breaks EVERY character above a gap, not just Qianlong — a whole-space integrity bug.
Introduced by recent char add/remove/move churn (#332 move-out etc.) that left holes after NEW-B27
had made the space contiguous. **FIX APPLIED (this session):** closed all 18 gaps by moving the 18
highest ids (592-609) into the holes and updating every char:N reference (18 def-headers + 23 refs,
across 00_Qing/Poland/Italy/Persia/India + imp19c_effects_legion_setup.txt). Global id space is now
contiguous 0..591, so runtime id == written id and set_as_ruler=char:214 correctly seats Qianlong.
Added: a contiguity-invariant header in 00_Qing.txt and a boot self-check (QING_boot_ruler_integrity
in qing_mechanics_on_actions.txt) that logs `IMP19C FAIL QING : QING_boot_ruler_integrity` if the
seated CHI ruler is ever not an adult chinese_emperor again. A runtime set_as_ruler-by-trait
workaround was considered and REJECTED — it would mask the one visible victim while leaving every
other gap-displaced character (genealogy, OOB commanders) silently wrong. Fix the cause: keep ids
contiguous. Pending in-game verification.

## BT-21 🟡 — F1 statesmanship bar: correct on X, still BELOW the box on Y
**Observed (user):** the F1 fix placed the statesmanship bar correctly on the X axis but it sits BELOW
the box instead of inside it; move it UP by roughly its own bar-width so it renders inside the box.
File: government_view (the F1 edit site).

## BT-22 🔴 — Sinicization report opens an EMPTY window (Han-majority provinces not listed/calculated)
**Observed (user):** the Sinicization report (#318/#320 B26) opens empty — Han-majority-culture provinces
not displayed, possibly not calculated at all. NEEDS root-cause: the report's province list/datamodel.

## BT-23 🔴 — New World crops report opens an EMPTY window
**Observed (user):** same empty-window symptom as BT-22. Likely a shared root cause with the report
province-list datamodel. NEEDS root-cause.

## BT-24 🟡 — Ethnic Tension report opens an EMPTY window
**Observed (user):** empty window — UNSURE if genuinely no high-tension provinces exist at 1763 or a
list/calc error. NEEDS root-cause; if the calc is fine and there are simply no high-tension provinces,
add an empty-state line. Cluster with BT-22/BT-23 (three empty reports → suspect shared report-list bug).

## BT-22/23/24 ROOT-CAUSE DIAGNOSIS (empty reports) — recorded, fix pending fresh log
Iteration is FINE (migration report uses the identical every_governorships->state->province descent and
works). The three empty reports each fail at their FILTER:

- **BT-22 Sinicization** (qing_province_reports.txt:209, `dominant_province_culture_group = chinese_group`):
  China-proper provinces DO carry chinese_group cultures (setup: beihua 131, xiajiang 83, wu 55, yue 44,
  min 42, hakka 28, shangjiang 26, hui 16, xiang 15, gan 13, jin 1 — all members of chinese_group per
  common/cultures/00_chinese_group.txt:72-131). So the filter SHOULD match hundreds of provinces yet the
  list is empty ⇒ the keyword `dominant_province_culture_group` is NOT resolving as a province limit.
  SUSPECT: it is UNPROVEN — it appears ONLY in common/WIP/buildings/00_default.txt:457 (WIP = not loaded/
  unverified) and in my own qing files; NOWHERE in loaded vanilla/TI/Invictus. F6 "fixed" the dot-chain
  parse error by swapping to this keyword, which stopped the load error but the predicate matches nothing.
  → NEXT: oracle-verify the correct PROVEN province-culture-group idiom before editing. Candidates to test:
    (a) scope-block `dominant_province_culture = { culture_group = chinese_group }`;
    (b) save dominant_province_culture to a scope then test `scope:x.culture_group = chinese_group`;
    (c) iterate pops / dominant culture via a different accessor. Do NOT re-guess; consult oracle.

- **BT-23 New World crops** (qing_province_reports.txt:44-49, `trade_goods = maize/sweet_potato/potato`):
  ZERO provinces carry maize/sweet_potato/potato as trade_goods in setup (province trade_goods survey:
  none of the three appear), and NO gamestart seeding call for QING_COLON_apply_nwcrop_capacity /
  set_trade_goods=sweet_potato was found in on_actions. So at a FRESH 1763 start the crops report is
  GENUINELY empty until the colonisation/crop-spread mechanic runs and stamps qing_nwcrop_abundance /
  flips a province's trade_goods. → LIKELY not a bug per se, but: (1) confirm whether ANY 1763 province
  should already grow these (historically maize/sweet potato were widespread in SW China by 1763 — Yunnan/
  Guizhou/Sichuan — so setup may be missing them); (2) add an empty-state line so the window isn't blank;
  (3) consider seeding a few historically-attested New World crop provinces at 1763.

- **BT-24 Ethnic Tension** (qing_province_reports.txt:98-99, `qing_prov_ethnic_tension >= 30`):
  The pulse IS wired (qing_mechanics_on_actions.txt:157 QING_ethnic_tension_init). At a fresh start the var
  is seeded to 0 and only climbs over time, so >= 30 may genuinely match nothing early game. → confirm from
  the fresh log whether the pulse has run and what values exist; add an empty-state line regardless.

COMMON RECOMMENDATION for all three: add a "no provinces currently qualify" empty-state row so an empty
list reads as informative, not broken. Fixes HELD pending the fresh debug.log the user is producing.

### BT-22/23/24 RESOLUTION (implemented, uncommitted)
- **BT-22** already fixed+committed (fa1364e13): dominant_province_culture_group = culture_group:chinese_group.
  The empty-window log lines were all from the pre-fix 13:28-14:36 run (log predates the 17:20 fix).
- **BT-23 + BT-24 + BT-22 safety-net**: added a proven empty-state line to each report window. Three
  is_shown scripted_guis (qing_report_crops_empty / _tension_empty / _sinicization_empty) test
  `NOT = { has_variable_list = <list> }` — a list built by clear+conditional add_to_variable_list reads
  as ABSENT when nothing qualified (proven WAR_scripted_guis.txt:1220 gate). Each window shows an
  informative empty-state textbox (loc qing_*_report_empty) bound to that gate via the IsShown idiom
  (qing_religion.gui:265). Files: common/scripted_guis/qing_province_reports.txt (+3 guis),
  gui/qing_province_reports.gui (+3 textboxes), loc qing_province_reports + qing_governance.
- **BT-23 crop-seeding follow-up (DEFERRED, optional design)**: maize/sweet potato were historically
  widespread in SW China (Yunnan/Guizhou/Sichuan) by 1763. Seeding a handful of setup provinces with
  those trade_goods would make the report non-empty at start AND improve historical fidelity — but it
  changes province economics (a balance decision), so it is NOT part of this bug fix. Left as an
  optional enhancement, not a defect.

## FIXES ALREADY APPLIED THIS SESSION (fix-as-reported mode, on merge-overnight, UNCOMMITTED)
These are review-confirmed findings the user directed me to fix now (NOT the BT-N boot-test items, which
remain held for a batch):
- **#334 MAJOR + minor** (se_QING_MINISTRY.txt:145) — Lifan Yuan warrant/coverage/affinity loop filtered
  by `is_subject_type = autonomous_governorship` (phantom roster) → changed to the SAME predicate
  QING_amban_post_sweep uses (any_owned_province + current_ruler mongolic/bodish culture-group). One
  loop-filter fix resolves all four #334 sub-findings (coverage term b + dead-code affinity term e).
- **CARAVAN MAJOR** (se_QING_CARAVAN.txt:270, QING_caravan_invest_market) — advanced integration on
  c:XNG (a client_state SUB-subject of ILI) instead of c:ILI (the direct CHI autonomous_governorship);
  would drive integration toward the wrong overlord and, at threshold, LAND_transfer XNG's provinces to
  CHI rupturing the ILI→XNG chain. Repointed to c:ILI to match sibling #367 tuntian lever.
- **CANAL minor (behavioral)** (se_QING_CANAL.txt:109) — minister-competence term read finesse via the
  unproven `set_variable value = var:qing_office_works_holder.finesse` chain (attribute off a var-held
  scope in effect VALUE context, no precedent) → could silently read 0 and erase the capable-minister
  bonus. Converted to the proven save_scope_as → scope:X.finesse idiom.
- REVIEW FALSE-POSITIVE noted: MINISTRY:390 granary-in-Works-roster — NOT a bug; the inner roster-gate
  `if` (line 411-423) already excludes granary; only the count-tally admits it (by design, #335-R comment).
- REVIEW DEFERRED (design judgment, clamp-bounded): MINISTRY:391/410 dike/depot double-count into
  qing_min_perf_works via both coverage term (b) and canal-condition term (d). Balance skew, not a
  correctness defect; leave for a deliberate rebalance decision.
- ALREADY COMMITTED earlier (5499fe3ca): the 3 caravan flag-leak findings (qing_caravan_events.txt
  :68/133/147) — confirmed present in the committed file.
