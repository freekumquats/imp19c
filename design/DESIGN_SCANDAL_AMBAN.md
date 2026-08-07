# DESIGN — Retarget 'A Scandal at Court' (qing_integ.11) to the integrated subject's amban (#22)

**Branch:** merge-overnight. **Status:** DESIGN (needs adversarial review before build). **Scope:** CHI.
**Decision (user, resolved):** the culprit is the AMBAN posted to the SUBJECT BEING INTEGRATED — specifically
scope:integ_amban for scope:target. NOT a random courtier, NOT any amban, NOT a senior GC minister (that is a
SEPARATE task #27). Related: #27 (senior-minister scandal chain — distinct rare event).

## 0. Current state (baseline a04a346c7)
qing_integ.11 (qing_subject_integration.txt:236) is an INTEGRATION-reaction event, dispatched from
SUBJ_QING_roll_reaction (se_SUBJECT_QING.txt:558-566) as a weight-15 (×3 if ruler corruption≥5) branch of the
reaction random_list — fires per-subject during that subject's integration. Currently it selects a fiscal/
governor courtier (is_governor / office flags) as scope:corrupt_official. The amban/garrison desc addendum was
already removed (nonsensical for a court scandal); the SUBJ_QING_resolve_integ_actors call was removed.

## 1. The reframe
The diverted funds are "silver appropriated to smooth the integration of [target]" — that is the resident
AMBAN's remit. So:
- **Culprit = scope:integ_amban** (the amban posted to scope:target), resolved by re-adding
  `SUBJ_QING_resolve_integ_actors = yes` to the immediate (it populates scope:integ_amban / integ_amban_present).
  Set `scope:corrupt_official = scope:integ_amban` so the existing desc/portrait ([corrupt_official.GetName],
  right_portrait) still work — now correctly showing the amban.
- **Gate on an amban being present:** the scandal branch should only fire (or the .11 event should only proceed)
  when `integ_amban_present` / `exists = scope:integ_amban`. If NO amban is posted to this subject, there is no
  one to skim the integration-silver → either don't fire the scandal (drop through in the dispatch), or the .11
  trigger self-aborts and picks a fallback. DECISION: gate the DISPATCH (add `has an amban` to the scandal
  branch's condition) so it simply doesn't roll a scandal for an amban-less subject — cleaner than a self-abort.

## 2. Consequences (amban-scale, via the proven per-amban helper)
Route the fallout through `SUBJ_QING_lifan_amban_outcome = { delta = -N }` (se_SUBJECT_QING.txt: sets
qing_lifan_recent_amban_outcome, folds into the Lifan Yuan performance) + a prominence hit on the amban
(add_prominence = -N) — mirroring the .10.d / .40.c amban-discredit pattern. The three existing options
(impeach/confiscate, hush up, yanglian stipends) still apply, now framed as dealing with the corrupt AMBAN:
- Impeach/confiscate: seize his estate (treasury +, tyranny +), the amban is disgraced (recall him? or
  add_prominence −−). Consider recalling the amban (QING_amban_recall) since he's disgraced.
- Hush up: pay him off, lose integration progress, Lifan Yuan marked down.
- Yanglian stipends: the systemic remedy — bind him, ruler popularity +.

## 3. Frequency
The reframe RESOLVES the "too common for a senior minister" complaint WITHOUT a weight change: an amban-level
embezzlement is plausibly a common integration event. Keep the weight-15 branch, but ADD the amban-present
gate (§1) so it only fires where an amban exists. If it still feels too frequent in playtest, lower the weight
— but the mis-targeting (senior minister) was the real problem, now fixed. NO senior-minister frequency concern
here (that's #27).

## 4. Desc addendum
The amban/garrison actor-status addendum (removed earlier as nonsensical for a random-courtier scandal) may now
be APPROPRIATE — the amban IS the subject of the event. RECONSIDER re-adding a triggered_desc naming the amban
on the ground (or simply rely on right_portrait = scope:corrupt_official = the amban + [corrupt_official.GetName]
in the desc). LEAN: no addendum needed — the desc already names the culprit; keep it simple.

## 5. Files affected
- `common/scripted_effects/se_SUBJECT_QING.txt` — the scandal dispatch branch (:558-566): add the amban-present
  gate so a scandal only rolls where an amban is posted.
- `events/imp19c_mod_events/qing_subject_integration.txt` — qing_integ.11: re-add SUBJ_QING_resolve_integ_actors
  to the immediate; set corrupt_official = scope:integ_amban (guarded; keep the ruler/courtier fallback ONLY if
  we allow the event to fire amban-less, else drop it); route option consequences through
  SUBJ_QING_lifan_amban_outcome + amban prominence; update loc to frame the culprit as the amban.
- `localization/english/qing_subject_integration_l_english.yml` — reword .11.desc/.a.tt to name the amban
  (currently references Heshen archetype + [corrupt_official.GetName] — keep the name, adjust framing).

## 5b. [REVIEW-DECISIVE 2026-08-07] Five fixes before build
1. **GATE ON THE RAW `qing_amban_here` PREDICATE, not integ_amban_present.** CRITICAL: SUBJ_QING_resolve_integ_actors
   runs only in each event's IMMEDIATE (post-dispatch), so integ_amban_present / scope:integ_amban do NOT exist
   at dispatch time (SUBJ_QING_roll_reaction) OR at the event's trigger-eval time. Both the dispatch branch gate
   AND the event self-abort guard MUST use the raw state resolve itself reads:
   `scope:target = { has_variable = qing_amban_here  var:qing_amban_here = { is_alive = yes  employer = scope:target } }`
   (se_SUBJECT_QING.txt:801-812). This is expressible in the random_list branch trigger (scope:target is set
   there, :531-536) and the event trigger.
2. **FULL LOC REWRITE of .11.t/.desc/.a.tt** — the current text is court-grandee/Heshen ("Seize the grandee's
   estate", dyke funds drowning prefectures, title "A Scandal at Court"). A frontier resident amban is not a
   Heshen-scale grandee. Rewrite to the frontier-amban register. NOTE: qing_household.4 ("Grand Secretary as
   Heshen", qing_household_events.txt:191) ALREADY is the court-grandee-Heshen scandal — so retargeting .11
   to the amban REDUCES overlap with it (good) and #27 becomes the senior-minister version.
3. **RESCALE the .11.a windfall.** It grants add_treasury = 150 ("Heshen-scale"). An amban's confiscated estate
   is not Heshen-scale — drop to a modest figure (e.g. +40-60).
4. **QING_amban_recall IS MANDATORY on the impeach path, not optional.** .11.a currently does
   `corrupt_official = { add_corruption 20  add_loyalty = inspired_disloyalty_other_l }`. If corrupt_official is
   the POSTED amban, that leaves a freshly-disloyaled amban IN PLACE, which QING_amban_evaluate then scores →
   subject drift / recall crises. So impeach MUST `QING_amban_recall = { subject = scope:target  reason = "impeached-for-graft" }`
   (se_QING_AMBAN.txt:220 — moves him back to CHI, char survives, clears qing_amban_here; safe mid-event, scope
   still valid for the portrait).
5. **REMOVE the dead a04a346c7 selection ladder** (qing_subject_integration.txt:267-327, the 5-tier
   is_governor/office_steward/courtier/ruler fallback). Setting corrupt_official = scope:integ_amban makes it
   all unreachable — this task substantially REVERTS a04a346c7. State that plainly in the commit. Keep ONE
   safety: if the amban died during the 3-10 day delay (scope:integ_amban unset at fire), self-abort via the
   trigger guard (#1) OR a minimal fallback — pick the trigger guard (cleaner; no scandal fires if the amban
   is gone, consistent with the dispatch gate).

## 6. Build checklist
1. Add amban-present gate to the scandal dispatch branch (se_SUBJECT_QING.txt:558-566).
2. qing_integ.11 immediate: SUBJ_QING_resolve_integ_actors = yes; if exists scope:integ_amban →
   save_scope_as corrupt_official (from the amban); decide fallback (drop it if gated at dispatch).
3. Options → SUBJ_QING_lifan_amban_outcome{delta} + amban prominence; consider QING_amban_recall on impeach.
4. Loc reframe (culprit = amban); keep the Heshen historical color.
5. Clear SUBJ_QING_clear_integ_actors at option tails (already present, idempotent).
6. Review + boot-test: scandal fires only with an amban posted; names/portraits the amban; Lifan perf moves.

## 7. Risks
- **R1 scope:integ_amban lifetime:** resolve_integ_actors populates it in the immediate; the options run in the
  same event so it's live (unlike the delayed-feedback events which needed the clear-order care). Confirm the
  clear_integ_actors at option tails doesn't wipe it before the option effect reads it (order: read amban →
  outcome → clear).
- **R2 fallback removal:** if we gate at dispatch (no amban → no scandal), the .11 event should NEVER fire
  amban-less, so the ruler-stand-in fallback becomes dead — remove it, OR keep a minimal guard in case the
  amban dies during the 3-10 day dispatch delay (defensive: if scope:integ_amban gone at fire time, self-abort
  like the .10 subject-vanished guard).
- **R3 overlap with #27:** ensure the amban scandal (#22, common, integration-context) and the senior-minister
  scandal (#27, rare, court-context) are clearly distinct events — no shared trigger, no double-fire.
