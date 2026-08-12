# DESIGN — Amban appointment as a character-picker (#26)

**Branch:** merge-overnight. **Status:** DESIGN (needs adversarial review before build). **Scope:** CHI, player-only.

## 0. Problem / user directive

Amban appointment today is either (a) automatic (`QING_amban_post_sweep`, quarterly, auto-draws the ablest
banner graduate) or (b) a per-subject Diplomacy-tab button (`qing_amban_manage_post_button`) that also
auto-draws. There is **no player character-picker** and **no appoint control on the Lifan Yuan screen**.

User wants: appoint an amban by **picking a character from a list of eligible candidates**, exactly like the
Censorate's **"Commission an Inspector"**, reachable from BOTH:
1. a new "Post an Amban" button on the **Lifan Yuan screen** (`gui/qing_lifanyuan.gui`), and
2. the existing per-subject **Subjects/Diplomacy** "Post an Amban" button (rewired to open the same picker).

## 1. The PROVEN pattern to mirror (Censorate "Commission an Inspector")

End-to-end (verified in-repo):
- **Button** (`qing_censorate.gui:242-252`) fires 4 onclicks:
  1. `GetVariableSystem.Set('qing_gc_picker_office', 'censor_inspector')` — GUI-side picker tag.
  2. `qing_gc_set_picker_office_censor_inspector` scripted_gui → `set_variable qing_gc_picker_office_var = flag:censor_inspector` (SCRIPT-side picker tag the row handler dispatches off).
  3. `qing_gov_council_refresh_candidates` scripted_gui → `QING_council_refresh_candidates` builds the
     candidate list `qing_council_candidates` (a variable-list on CHI, se_QING_COUNCIL.txt:1116).
  4. `gui.createwidget gui/imp19c_windows.gui qing_office_picker_window` — opens the shared picker window.
- **Picker window** (`qing_office_picker_window`, imp19c_windows.gui) walks `MakeScope.GetList('qing_council_candidates')`
  and renders a row per candidate.
- **Row-click handler** (`qing_gov_office_appoint_selected`, character-scope, QING_governance_actions.txt:~580)
  reads `qing_gc_picker_office_var` and dispatches to the right `QING_office_appoint`. `this` = appointee,
  `scope:player` = CHI.

## 2. Design — reuse, don't reinvent

Add an amban path onto this SAME machinery, keyed by a new picker value `amban` (or per-subject variant).

### 2a. Candidate builder — `QING_amban_refresh_candidates`
New effect in se_QING_AMBAN.txt (mirrors `QING_council_refresh_candidates`): `clear_variable_list
qing_amban_candidates`, then iterate `any_character { employer=ROOT, is_adult, is_alive, NOT ruler/heir,
NOT general/admiral/governor, NOT QING_char_holds_court_position, AND the banner-exam-graduate filter
(fanyi_jinshi OR jurchen/mongolic degree-holder) }` — the SAME eligibility `QING_amban_post`'s draw uses
(se_QING_AMBAN.txt:52-140) — `add_to_variable_list qing_amban_candidates`. Order/limit for display sanity.

### 2b. Picker target = which SUBJECT gets the amban
The council picker appoints to a single office (no target). The amban picker MUST know WHICH subject.
Two entry points differ:
- **From the Subjects/Diplomacy button:** `scope:target` is already the shown subject. Save it as a var
  `qing_amban_picker_subject` (a country-ref var on CHI) so the row handler knows the destination.
- **From the Lifan Yuan screen:** there is no single subject in scope. Options:
  - (A) a SUB-PICKER first: list eligible vacant dependencies (Inner-Asian, mongolic/bodish ruler, no amban),
    player picks the subject → stores `qing_amban_picker_subject` → then the character picker opens.
  - (B) the Lifan Yuan button opens a subject list where each row's "Post an Amban" carries that subject.
  - **RECOMMEND (A)** — reuses the picker idiom twice (subject picker → character picker), least new GUI.

### 2c. Row-click handler — `qing_amban_appoint_selected` (character scope)
`this` = chosen candidate, `scope:player` = CHI, reads `qing_amban_picker_subject`. Effect: pay 25 PI,
set `qing_amban_manual` on the subject (freeze auto-sweep), then POST THIS SPECIFIC CHARACTER.

**[REVIEW-CORRECTION 2026-08-07] `QING_amban_wire` does NOT draw — it is ALREADY the pre-chosen-char entry
point.** The `ordered_character` sorting iterator lives in `QING_amban_post` (se_QING_AMBAN.txt:85-118), NOT
in `QING_amban_wire` (se_QING_AMBAN.txt:163-213). The wire expects `scope:qing_amban_new` to be ALREADY SET
and just does move_country / modifier / storage / marker / timer — exactly what we want. So:
- **No adaptation of QING_amban_wire needed.** New trampoline event `qing_amban.6`: preset
  `scope:qing_amban_new = <picked char>` (propagated via trigger_event saved scope, proven by qing_amban.5) +
  `scope:...subject`, then call `QING_amban_wire = { subject = X }` UNCHANGED. Do NOT reuse `.5` (it calls
  `QING_amban_post`, which draws).
- **R1 down-graded:** the wire has no sorting iterator, so the trampoline is belt-and-suspenders (consistency),
  not crash-avoidance — the recall button even calls move_country inline (SUB_QING_amban.txt:143) without crashing.
- **R4 already safe:** set_as_minor_character was moved OUT of the wire tail to the CREATE sites only (#34
  review-fix), so a picked major courtier keeps his standing. No new work.

**[REVIEW-CORRECTION] PI charge + qing_amban_manual MUST live in the ROW HANDLER, not the button.** Today the
Diplomacy button charges 25 PI + sets qing_amban_manual in its OWN on-click effect (SUB_QING_amban.txt:81-84).
If the button is rewired to merely OPEN the picker, that charge would fire even if the player closes the picker
without choosing — charging PI + freezing the auto-sweep for a post that never happens. MOVE the charge + flag-set
into qing_amban_appoint_selected; leave only the is_valid PI>=25 GATE on the button (so it won't open when unaffordable).

### 2d. Buttons
- **Lifan Yuan screen** (qing_lifanyuan.gui): add a "Post an Amban" button (mirrors the Censorate button's
  4-onclick shape) → set picker var `amban` → refresh candidates → open picker (subject sub-picker first per 2b-A).
- **Subjects/Diplomacy button** (SUB_QING_amban.txt `qing_amban_manage_post_button`): rewire its effect from
  the auto-draw trampoline to: save `qing_amban_picker_subject = scope:target` → refresh candidates → open the
  character picker. Keep its is_shown/is_valid gates (eligible subject, Lifan Yuan filled, PI≥25).

## 3. Coexistence with the auto-layer
Unchanged: setting `qing_amban_manual` on the subject freezes `QING_amban_post_sweep` for it (existing #163
behaviour). "Return to automatic" clears the flag. The picker is the manual override; the auto-sweep still
staffs un-flagged dependencies.

## 4. Files affected
- **New GUI window** (or reuse): a character picker + a subject sub-picker. Reuse `qing_office_picker_window`
  if its datamodel can be pointed at `qing_amban_candidates`; else a parallel `qing_amban_picker_window` in
  imp19c_windows.gui. (Investigate whether the shared window is generic enough — it currently reads
  `qing_council_candidates` hardcoded.)
- `common/scripted_effects/se_QING_AMBAN.txt` — `QING_amban_refresh_candidates`; adapt `QING_amban_wire`
  (or a new trampoline) to accept a PICKED char instead of drawing one.
- `common/scripted_guis/` — `qing_amban_set_picker`, `qing_amban_refresh_candidates_btn`,
  `qing_amban_appoint_selected` (row handler), and (2b-A) a subject sub-picker set/refresh/select.
- `gui/qing_lifanyuan.gui` — the new "Post an Amban" button.
- `common/scripted_guis/SUB_QING_amban.txt` — rewire `qing_amban_manage_post_button` to open the picker.
- loc for the new buttons/window.

## 5. Risks (updated post-review 2026-08-07)
- **R5 SUPERSEDED (2026-08-11, #114) — the create_character fallback this risk assumed no longer exists,
  and must NOT be reintroduced.** `#114` removed `QING_amban_post`'s create_character fallback entirely
  as an unsanctioned mint site (the character-creation standing rule permits create_character for a
  degree-holder ONLY at the boot seed and the exam cohort — a runtime "raise a new resident" fallback
  violates it). The auto-sweep now simply leaves a dependency unstaffed when the bench is empty (the
  same "under-full is honest" pattern used elsewhere this session). **Do NOT build the "raise a new
  resident" row this section originally recommended** — any future picker work on a narrow/empty bench
  must use the SAME honest-empty-state pattern (an empty-bench message, per the existing
  `IsDataModelEmpty` GUI idiom used by the other pickers in this file), never a create_character
  fallback. This section is kept for history; its RESOLUTION line is voided.
- **R2 shared picker window: parallel window is MANDATORY but ROUTINE (down-graded from "biggest unknown").**
  `qing_office_picker_window` (imp19c_windows.gui:36-169) HARDCODES `GetList('qing_council_candidates')` (:79),
  the row action (:92), and the close target (:93) — not parameterized. BUT there are already SIX hand-cloned
  copies (justice/censorate/4 harem) in the same file; `qing_amban_picker_window` is a mechanical clone, not a risk.
- **R3 subject-targeting / two-step picker: genuine SPIKE (up-graded from footnote).** 2b-A (subject sub-picker →
  char picker) is NET-NEW GUI: every existing picker is a CHARACTER picker (portrait/stat rows); a SUBJECT picker
  needs a country-list row template (flag/name) that doesn't exist. And there is NO existing two-step picker in the
  repo — sequential createwidget chaining is unproven here. So the doc's "2b-A is least new GUI" was WRONG. 2b-B
  (per-subject-row button on the Lifan Yuan roster, which already iterates a dynamicgridbox at qing_lifanyuan.gui:
  234-307) may be cheaper — but that roster lists subjects that HAVE an amban; posting needs the VACANT-eligible
  set (different datamodel either way). Treat Lifan-Yuan entry (Phase 2) as a spike; Phase 1 (Diplomacy button)
  does not need it.
- **R1 (#34 crash): LOW** (not HIGH) — the wire has no sorting iterator (see 2c correction); trampoline is
  belt-and-suspenders.
- **Replace-button inconsistency (NEW):** `qing_amban_manage_replace_button` (SUB_QING_amban.txt:151) auto-draws
  (recall + qing_amban.5 re-post). If Post becomes a picker but Replace keeps auto-drawing, the UX is split
  (hand-pick the first amban, engine picks the replacement). DECIDE: does Replace also become a picker, or is
  the split intentional? The design must address Replace, not just Post.

## 6. Build phasing
- **Phase 1:** candidate builder + rewire the Subjects/Diplomacy button to the char picker (single subject
  already in scope — simplest; proves the picker + trampoline-with-picked-char end to end).
- **Phase 2:** Lifan Yuan button + subject sub-picker (2b-A).
- Review after Phase 1 before Phase 2.

## 7. Open questions for review
- Is `qing_office_picker_window` reusable for a different candidate list + row handler, or must a parallel
  window be built? (R2 — the biggest structural unknown.)
- Should the Lifan Yuan entry use a subject sub-picker (2b-A) or a per-subject-row button (2b-B)?
- For the picked-char post: adapt `QING_amban_wire` to accept an appointee, or write a dedicated
  `QING_amban_post_picked` that sets `scope:qing_amban_new` then calls the wire tail?
