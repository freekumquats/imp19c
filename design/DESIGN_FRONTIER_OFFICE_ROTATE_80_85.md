# DESIGN — Frontier-office rotate rework (#80–#85): candidate LIST + corruption-tied easing + surfaced metric

Status: DRAFT for adversarial review. Author: overnight run 2026-08-11.
Scope: the three frontier fiscal offices that currently rotate by auto-pick — Salt Commissioner (兩淮鹽政,
se_QING_SALT.txt), Caravan Superintendent (喀什噶爾參贊大臣, se_QING_CARAVAN.txt), Hoppo (粵海關監督,
se_QING_CANTON.txt). All three share an identical rotate idiom, so the fix is one pattern applied thrice.

## Diagnosis (source-verified this session)
All three `QING_<office>_rotate` functions (SALT:219, CARAVAN:891, CANTON:493) do:
1. relieve prior holder (clear marker + holder var);
2. call `QING_<office>_appoint`, which runs `ordered_character { order_by = finesse  max = 1 }` — an
   AUTOMATIC single pick of the highest-finesse eligible courtier;
3. `QING_DECLINE_nudge = { var = <office>_squeeze  amount = -12 }` (flat), then a further `-6` if the new
   holder's `finesse >= 7`.

Problems (the six tasks):
- **#80 / #82 / #84** — the player has NO choice of appointee; the game auto-picks highest finesse. The GC
  offices, by contrast, open an eligible-character LIST the player clicks (qing_gc_set_picker_office_* +
  qing_gov_office_appoint_selected, QING_governance_actions.txt:455+; rendered in imp19c_windows.gui:30-33).
  The three frontier offices should use the SAME candidate-list UX.
- **#81** — the squeeze easing is flat (−12, −6-if-finesse). It should reflect the NEW commissioner's
  CORRUPTION: an honest man eases the squeeze more, a venal one barely at all. (The squeeze metric IS the
  holder's corruption — SALT:208 sets `qing_salt_squeeze = holder.corruption` on the quarterly pulse.)
- **#83 / #85** — the caravan superintendent's squeeze is NOT surfaced in the caravan panel (salt shows its
  squeeze; caravan doesn't). Also the caravan scratch var is named `n` (per the task) — rename descriptively.

## The GC candidate-list pattern (the target UX, source-verified)
GC offices work via: a per-office "set picker" scripted_gui writes `qing_gc_picker_office_var = flag:<office>`
(QING_governance_actions.txt:455-523); the shared candidate window (imp19c_windows.gui) renders an
`ordered_character` datamodel sorted by fitness whose rows are eligible courtiers; clicking a row runs
`qing_gov_office_appoint_selected` (QING_governance_actions.txt:584), which seats THAT character on the
office named by the picker var. The player picks the man; the eligibility filter is the office's own.

## ⟪v2 — REVISED per dr8085 (SOUND-WITH-CORRECTIONS, 5 findings). Changes below supersede the v1 DECISION/§81/§Fallback.⟫

### v2 CHANGE A (dr8085 F1) — #85 scratch-var `n` DOES NOT EXIST; #85 = #83
The `n` var was a GREP ARTIFACT: `rg -rn` treats `-r` as `--replace` (per the repo tooling rules), rewriting
every match to the literal `n`. There is NO `name = n` / `var:n` / single-letter var anywhere in
se_QING_SALT/CARAVAN/CANTON. The caravan's real scratch vars are already descriptive (qing_caravan_ease_tmp,
_super_sq_tmp, etc., CARAVAN:118-317). So #85 has no rename to do — it collapses entirely into #83 (surface
the caravan squeeze). No rename work.

### v2 CHANGE B (dr8085 F3) — model on the AMBAN picker, NOT the GC handler
The GC handler qing_gov_office_appoint_selected (QING_governance_actions.txt:584) is GC-specific: hardcoded PI
cost (−20/−15, :710), a 16-way council-seat/corps-cap dispatch, and a candidate list built by the GC filter
(QING_council_refresh_candidates_by, capped 12, different eligibility). Piggybacking it is wrong.
USE the AMBAN picker as the template — self-contained and lean: qing_amban_picker_window
(imp19c_windows.gui:176) + its own list var qing_amban_candidates + own refresh QING_amban_refresh_candidates
(se_QING_AMBAN.txt:231) + own handler qing_amban_appoint_selected (SUB_QING_amban.txt:114). The frontier
picker mirrors this shape (window + candidate-list var + refresh verb + handler + the 3 set-flag GUIs), with a
SEPARATE qing_frontier_picker_office_var (no collision with the GC var — different var/handler; windows
GUI.ClearWidgets on click). Surface area = window + handler + refresh + 3 set-flag GUIs (not just "one shared
picker" — the v1 undersold it).

### v2 CHANGE C (dr8085 F2) — DUAL PATH: keep auto-pick `_rotate` for event callers; picker only for the button
Caller sweep (dr8085, verified): salt/caravan `_rotate` are called ONLY by their player buttons
(QING_salt_panel.txt:31, QING_caravan_panel.txt:161). BUT `QING_canton_rotate_hoppo` is ALSO called by two
EVENT effects — qing_canton.2.b (qing_canton_events.txt:181) and qing_canton.3.b (:244) — which run inline in
option.effect and CANNOT open a GUI picker + await a click. So:
- KEEP the auto-pick `QING_<office>_rotate` effects intact (event/AI path, Canton needs it; keep all three for
  symmetry + any future event caller).
- The PLAYER buttons repoint to `qing_<office>_open_picker` (sets the flag + opens the window).
- The corruption-tied easing (#81) lives in a SHARED helper `QING_frontier_office_ease_squeeze = { office = X }`
  called by BOTH the picker-appoint handler AND the auto-`_rotate` — so qing_canton.2.b/.3.b get the new easing
  too, not the old flat −12/−6. (v1 missed this dual-path requirement.)

### v2 CHANGE D (dr8085 F4) — #81 reframed: the LIST is the durable lever; the nudge is a one-quarter bridge
Source-confirmed: the quarterly pulse OVERWRITES the squeeze var with the seated man's corruption every quarter
(qing_salt_squeeze = seated.corruption, SALT:208; likewise CANTON:337, CARAVAN:316). So ANY rotate-time nudge
(flat OR corruption-tied) is COSMETIC — it lasts one quarter until the next pulse re-mirrors. The DURABLE lever
is seating a low-corruption man. This is exactly what the LIST (#80/#82/#84) delivers: the candidate rows show
each man's CORRUPTION alongside finesse, so the player can pick a clean man → the pulse then mirrors his low
corruption into the squeeze durably. So #80 and #81 are the SAME fix: the list is the mechanism that ties the
squeeze to the chosen man's corruption.
- The rotate-time nudge is retained as a modest ONE-QUARTER bridge (so the effect isn't invisible until the next
  pulse), and made corruption-tied to satisfy #81's literal text: `easing = -(20 - corruption/5)` via a
  script_value on the seated man (0 corruption → −20, 100 → 0). Documented plainly as a one-quarter bridge, NOT
  a durable mover — the honest framing dr8085 asked for. (The "clamp ≤ 0" is dropped — dead code, the curve is
  never positive for corruption in [0,100].)

### v2 CHANGE E (dr8085 F5) — NO easy-half/hard-half fallback; the LIST ships for all three or it's not done
The v1 "Fallback / boot-spike salt first" pre-authorised shipping the easy #81/#83 while reducing the LIST (the
actual user-reported bug) to a one-office spike — the exact easy/hard split the anti-deferral contract forbids.
STRUCK. The list ships for all three offices, or #80/#82/#84 are honestly "not done" (per Sequencing line 76).
The AMBAN picker is a proven in-repo pattern (it renders + works), so this is not an unproven-capability spike —
it's a build. If a genuine hard block appears mid-build, it's logged loudly as a block, not dressed as a spike.

### v2 build order (all reviewed, nothing deferred)
1. Shared `QING_frontier_office_ease_squeeze` helper (script_value corruption curve) + wire into all three
   auto-`_rotate` effects (replaces the flat −12/−6). Small, testable. → code-review → commit.
2. #83 surface caravan squeeze row in gui/qing_caravan.gui (mirror the salt row). → review → commit.
3. The candidate LIST: frontier picker window + qing_frontier_candidates list + refresh verb + handler +
   3 set-flag GUIs, modelled on the amban picker; handler seats the clicked man (holder var + marker +
   QING_exam_pool_drop_member — MUST keep, or #77/#79 regress — + the ease helper), relieves prior holder.
   Repoint the 3 player buttons. → code-review → commit.
Each step commits only after its own CLEAN code-review.

---

## v1 DECISION (superseded by v2 CHANGE B/C above; kept for provenance) — reuse the GC candidate-window pattern, one shared frontier picker
Rather than build three bespoke list windows, add ONE shared frontier-office candidate picker mirroring the GC
one, parameterised by a `qing_frontier_picker_office_var` flag (salt | caravan | hoppo):
- Three "open picker" scripted_guis (`qing_<office>_open_picker`) each set the flag + open the shared window
  (the existing rotate BUTTON's onclick is repointed from `QING_<office>_rotate` to open the picker).
- The shared candidate window renders `ordered_character` (employer=CHI, the SAME eligibility limit each
  office's `_appoint` already uses — NOT QING_char_holds_court_position, is_general/admiral/governor=no,
  not hard-disgraced, not heir) sorted by finesse, showing each candidate's finesse + corruption so the
  player sees the trade-off.
- Clicking a row runs `qing_frontier_office_appoint_selected`, which branches on the picker flag to seat THAT
  character (set holder var + marker + QING_exam_pool_drop_member — the #77/#79 1:1 pool-drop MUST be kept),
  relieve the prior holder, and apply the corruption-tied easing (#81).

### #81 — corruption-tied easing (replaces flat −12/−6)
The seated man's corruption is 0..100 (lower = cleaner). Ease the squeeze by an amount that scales INVERSELY
with his corruption: `easing = -(20 - corruption/5)`, i.e.
- corruption 0 (a paragon) → −20 (strong easing);
- corruption 50 (average) → −10;
- corruption 100 (utterly venal) → 0 (no easing — a corrupt man does not clean up the racket).
Clamp the easing to ≤ 0 (never INCREASES the squeeze on a rotate — a rotate is at worst neutral). Implement as
a script_value read of `scope:<the seated char>.corruption`. This supersedes BOTH the flat −12 and the
finesse≥7 −6 (finesse still matters — it drives the yield GRADE on the quarterly pulse, unchanged).
[ASSUMPTION best-guess: the 20-max / /5 slope — logged; the rotate LOG_line will emit the computed easing +
the holder's corruption so the boot confirms the curve. Tunable in one script_value.]

### #83 / #85 — surface caravan squeeze + rename scratch var
- Add a caravan-squeeze read-out row to the caravan panel (gui/qing_caravan.gui), mirroring the salt panel's
  squeeze row (it reads `qing_caravan_super_squeeze`, already set on the pulse).
- Rename the caravan scratch var `n` (per the task) to `qing_caravan_super_pick` or similar descriptive name
  at its set + read sites. [VERIFY in impl: find the actual `n` var — the grep showed a `var:n` in
  se_QING_SALT/CARAVAN; confirm which office + rename only that one, not a shared helper param.]

## Fallback
If the shared parameterised picker proves too entangled to land safely this run, the SAFE minimal form is:
keep the auto-pick `_appoint` but (a) add the #81 corruption-tied easing (pure script_value, no UI) and
(b) surface the caravan metric (#83/#85, pure GUI). The LIST (#80/#82/#84) is the UI-heavy part; it can be a
labelled BOOT SPIKE (one office first — salt — to prove the shared-picker wiring renders, then extend to the
other two) rather than shipping all three unverified. Log clearly if the list is spiked-one-office vs all-three.

## Sequencing
- #81 (corruption easing) + #83/#85 (surface + rename) are low-risk and can land first (script_value + GUI).
- #80/#82/#84 (candidate list) is the design-first UI piece — mirror the GC picker; boot-spike salt first.
- Each piece: implement → code-review → commit. NOT closing #80/#82/#84 on an auto-pick that "still works".

## Adversarial-review asks
1. Is the shared parameterised picker actually simpler than 3 bespoke windows, or does the flag-branch
   dispatch add more risk than it saves? (GC does per-office set-pickers + one shared handler — is that the
   right model to copy, or should each office get its own small window?)
2. The GC `qing_gov_office_appoint_selected` handler branches on `qing_gc_picker_office_var` — can the
   frontier offices piggyback on a SEPARATE `qing_frontier_picker_office_var`, or is there a collision risk
   with the GC picker var if both windows can be open?
3. Does repointing the rotate button from `QING_<office>_rotate` to an open-picker break any caller that
   invokes `QING_<office>_rotate` directly (events, on_actions)? Must the auto-pick `_rotate` stay for
   AI / event callers while only the PLAYER button changes?
4. #81 curve: is `-(20 - corruption/5)` sane against the squeeze's own scale (0..100 = holder corruption)?
   Does a 0-easing at corruption 100 leave the squeeze stuck (the player rotated and got nothing)?
5. The 1:1 pool-drop (QING_exam_pool_drop_member) MUST run on the list-appoint path too — verify the new
   handler calls it (else #77/#79 regress).
