# DESIGN — Generic officeholder-corruption censure (retire the Hoppo-specific censure event)

## User request
"There is a Censorate event scrutinizing the Hoppo, but instead of a specific
hoppo-targeted event there should be a generic event which targets any Qing
officeholder with high corruption for censure."

## Diagnosis (traced in source this session)

- **`qing_censorate.1`** (events/imp19c_mod_events/qing_censorate_events.txt:34) — the
  EXISTING generic impeach event. Trigger: `tag = CHI`, a seated censor
  (`qing_office_censor_holder` alive + employed), and `any_character` employed by ROOT
  with `corruption >= 30 OR has_trait=corrupt OR loyalty < 40`. Immediate calls
  `QING_censorate_find_corrupt`. Options: uphold / exonerate / suppress.
  - LIMITATION: it targets ANY corrupt courtier `employer = ROOT`, NOT officeholders
    specifically. A corrupt idle noble is as eligible as a corrupt minister.

- **`QING_censorate_find_corrupt`** (common/scripted_effects/se_QING_CENSORATE.txt:98) —
  `ordered_character order_by=corruption max=1`, limit = employed by ROOT, not ruler,
  adult, alive, not a rebel foil, and (corruption>=30 OR corrupt trait OR loyalty<40 OR
  thin-academy-widened corruption>=20). Saves `scope:qing_censorate_target`. NOT
  officeholder-restricted. The venal-picker roster `QING_censorate_refresh_venal`
  (:149) uses a BYTE-IDENTICAL limit and must stay in sync.

- **`qing_canton.2`** (events/imp19c_mod_events/qing_canton_events.txt) — the
  Hoppo-specific censure. Trigger: `tag = CHI`, `has_variable = qing_hoppo_holder`,
  holder alive. **NO corruption gate** — it fires on ANY living Hoppo, honest or venal.
  This is the "specific hoppo-targeted event" the user objects to. Options:
  - `.a` impeach (抄家): saves holder as `scope:qing_censorate_target`, strips
    `qing_hoppo_marker` + `qing_hoppo_office` modifier, calls
    `QING_censorate_impeach_uphold`, clears `qing_hoppo_holder`, cuts corruption,
    +legitimacy.
  - `.b` quiet transfer (調任): pockets 1/3 of his wealth, `QING_canton_rotate_hoppo`.
  - `.c` ignore (留中): squeeze +4, corruption +2.

- **No unified officeholder flag.** Each post has its own marker:
  - great offices → `qing_office_held` (var) + `qing_officeholder` (char modifier),
    set in `QING_office_appoint` (se_QING_COUNCIL.txt:1738-1739).
  - Hoppo → `qing_hoppo_marker` (var) + `qing_hoppo_office` (char modifier), tracked by
    country var `qing_hoppo_holder`.
  - amban → `qing_amban_marker` (var).

- **`QING_censorate_impeach_uphold`** (se_QING_CENSORATE.txt:225) clears the target's
  GREAT offices but does NOT strip the bespoke Hoppo marker — which is why `qing_canton.2.a`
  strips `qing_hoppo_marker`/`qing_hoppo_office`/`qing_hoppo_holder` by hand before calling
  uphold. If the generic path is to disgrace a corrupt Hoppo correctly, uphold must become
  Hoppo-aware.

## FINAL DESIGN (implemented 2026-08-18) — SUPERSEDES the "Design decision" section below

User CLARIFIED mid-task: "there should be a censor event against corrupt courtiers, and
another against corrupt officeholders" — i.e. TWO distinct events, NOT a restriction of the
existing one. And chose (AskUserQuestion) "Keep, re-gate as non-censure" for `qing_canton.2`.

What shipped:
1. **`qing_censorate.1` narrowed to CORRUPT COURTIERS.** Its `any_character` trigger gains
   `NOT = { QING_char_holds_court_position = yes }`; its immediate now calls the new
   `QING_censorate_find_corrupt_courtier`. Same three options (uphold/exonerate/suppress).
2. **New `qing_censorate.11` = CORRUPT OFFICEHOLDER.** Gated on `has_variable = qing_current_post`
   (a seated holder of one of the 11 CHI-employed court posts). Immediate calls the new
   `QING_censorate_find_corrupt_officeholder`. Uphold routes through
   `QING_censorate_impeach_uphold`, which vacates a `qing_current_post` holder via
   `QING_post_dispatch_vacate` — so an impeached Hoppo/minister/commissioner is cleanly
   stripped of his seat and his backfill draws a fresh man. NO change to `impeach_uphold`.
3. **Boundary = `qing_current_post`, NOT the wider `QING_char_holds_court_position`.** Chosen
   because `qing_current_post` is EXACTLY the set `impeach_uphold` fully vacates. The 3
   ROOT-employed honorary posts that carry no `qing_current_post` (court artist 如意館,
   customs IG 總稅務司, opium commissioner 欽差大臣) are deliberately kept out of BOTH
   auto-events: uphold does not strip their bespoke markers, so auto-firing would dangle the
   marker. They remain reachable only via the MANUAL Impeach-the-Venal picker (unchanged
   pre-existing behaviour + its pre-existing gap). Subject-employed posts (amban/march_gg/
   xj_beg) are excluded by `employer = ROOT` automatically.
4. **Two dispatch entries in `se_QING_DECLINE.txt`** (weight 10 each): `.1` gated on the
   courtier `NOT`, `.11` gated on `has_variable = qing_current_post`.
5. **`qing_canton.2` re-gated as NON-CENSURE.** Option `.a` (查辦抄家 impeach) removed —
   impeaching a corrupt Hoppo is now the Censorate's affair (`.11`, since the Hoppo carries
   `qing_current_post = flag:hoppo`). Options `.b` (調任 transfer-for-cut) and `.c` (留中
   bury) kept. Desc + orphaned `.a`/`.a.tt` loc removed. Dispatch gate (venal hoard
   `wealth >= 150`) unchanged.

NOT changed (verified this session, contradicting the older "Design decision" below):
- `QING_censorate_impeach_uphold` needs NO Hoppo-awareness edit — it ALREADY vacates the
  Hoppo via the `qing_current_post` dispatch (#118 + #101-follow-up postdate the old note).
- `QING_censorate_find_corrupt` + `QING_censorate_refresh_venal` (the manual picker pair) are
  UNCHANGED — the manual lever still covers all venal courtiers AND officeholders.
- No new `QING_char_is_officeholder` trigger — the canonical
  `QING_char_holds_court_position` (courtier NOT gate) + `qing_current_post` (officeholder
  gate) already exist.

---

## Design decision (SUPERSEDED — kept for the diagnosis trail)

Make the CENSURE path generic and officeholder-focused; retire the auto-firing
Hoppo-specific censure. Concretely:

1. **New scripted_trigger `QING_char_is_officeholder`** (character scope):
   `OR = { has_variable = qing_office_held  has_variable = qing_hoppo_marker  has_variable = qing_amban_marker }`
   — the three patronage/revenue posts where graft is the historical concern. (Guardsmen,
   study fellows, palace eunuchs are inner-court corps, not graft offices — excluded.)

2. **Restrict the censure pool to officeholders.** Add `QING_char_is_officeholder = yes`
   to the limit of BOTH `QING_censorate_find_corrupt` AND `QING_censorate_refresh_venal`
   (they must stay byte-identical), and to `qing_censorate.1`'s `any_character` trigger.
   This makes the generic event target "any Qing officeholder with high corruption" exactly
   as the user asked.

3. **Make `QING_censorate_impeach_uphold` Hoppo-aware.** Inside it, after resolving the
   target: `if = { limit = { scope:qing_censorate_target = { has_variable = qing_hoppo_marker } }`
   strip `qing_hoppo_marker` + `qing_hoppo_office`, and clear the country var
   `qing_hoppo_holder` (so the Canton pulse backfills a fresh honest man). This moves
   `qing_canton.2.a`'s manual Hoppo-cleanup into the generic uphold so a corrupt Hoppo
   impeached through the generic event is disgraced AND his seat freed.

4. **Retire `qing_canton.2` as the auto-firing censure.** A corrupt Hoppo is now an
   officeholder caught by `qing_censorate.1`. Options for the non-censure Canton flavor
   (調任 rotate-and-take-a-cut, 留中 squeeze-creep) — see OPEN QUESTION below.

## OPEN QUESTION (needs a call before implementing)
`qing_canton.2` also carries Canton-specific NON-censure flavor: the 調任 quiet-transfer
(throne pockets 1/3 of the Hoppo's hoard, rotates him) and 留中 do-nothing (squeeze
creeps). Two ways to honor "replace the specific with a generic":
- **(A) Delete `qing_canton.2` entirely.** Cleanest match to "instead of a specific
  event." Loses the 調任/留中 Canton-squeeze flavor.
- **(B) Keep `qing_canton.2` but re-gate it** so it is NO LONGER a censure: gate its
  trigger on a CORRUPT Hoppo only, and reframe it purely as the Canton squeeze/transfer
  decision, leaving impeachment to the generic censorate event.
Default if unresolved: (A) — the user said "instead of," and the generic uphold already
does 抄家-equivalent confiscation. `QING_canton_rotate_hoppo` (the rotate lever) survives
independently for other Canton events.

## Files touched
- common/scripted_triggers/ — new `QING_char_is_officeholder` (find the Qing trigger file).
- common/scripted_effects/se_QING_CENSORATE.txt — 2 limits + uphold Hoppo-cleanup.
- events/imp19c_mod_events/qing_censorate_events.txt — `.1` trigger `any_character` limit.
- events/imp19c_mod_events/qing_canton_events.txt — retire/re-gate `.2` per open question.

## Risks / review targets
- Byte-identical drift between find_corrupt and refresh_venal limits (must add the trigger
  to BOTH).
- `qing_censorate.1` trigger `any_character` must mirror the find limit or the event fires
  with no valid target (find returns none → event shows an empty right_portrait).
- Removing `qing_canton.2` must not orphan loc keys or a referenced event id (grep for
  `qing_canton.2` callers).
- `QING_char_is_officeholder` used inside `ordered_character` limit runs per-candidate —
  keep it cheap (three `has_variable` reads, O(1)).
