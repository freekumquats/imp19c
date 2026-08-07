# DESIGN — Senior GC Minister corruption scandal chain, with a trial (#27)

**Branch:** merge-overnight. **Status:** DESIGN (needs adversarial review before build). **Scope:** CHI.
**Distinct from #22** (the amban integration-scandal — common, integration-context). This is the rare,
court-context, Heshen-scale chain.

## ⚠ [REVIEW-DECISIVE 2026-08-07] REFRAME: EXTEND existing events, do NOT build a new parallel chain
The adversarial review found my overlap analysis was WRONG — I checked only qing_household.4 and missed
THREE existing events that already occupy this exact space:
- **qing_office.1 "The Overmighty Grandee (the Heshen pattern)"** (qing_office_events.txt:54-128) — IS the
  Heshen chain. Culprit = seated top GC office-holder; option .1.a = confiscation (add_treasury 150),
  QING_office_vacate_dispatch, QING_char_endow -400 (estate seizure), QING_char_taint, disgrace,
  power-base destruction, corruption -12. Everything I called "novel" already exists here — MINUS a trial + death.
- **qing_revenue.4 "Treasury Audit"** (qing_revenue_events.txt:276-344) — the seated Revenue 戶部 minister.
- **qing_works.4 "River-Works Embezzlement Scandal"** (qing_works_events.txt:247-292) — the seated Works 工部 minister.
So #27's culprit set (Revenue/Works) + confiscation/vacate/disgrace payload ALREADY EXIST. The ONLY genuinely
novel content is: (a) a multi-step CENSORATE TRIAL, and (b) minister DEATH/IMPRISONMENT.
**NEW SCOPE:** add a Censorate-trial + capital-punishment ESCALATION path to the existing qing_revenue.4 /
qing_works.4 (and/or qing_office.1) — a new OPTION on those events ("Impanel a tribunal") that leads to a
trial sub-event (convict → death/imprison + durable vacancy; acquit → corruption entrenches). Do NOT create a
new qing_gcscandal namespace/dispatcher (it would be redundant content competing for the same rare court slot
against the same seated minister). Reuse qing_office.1's proven confiscation/vacate/taint payload.

## ⚠ [REVIEW-DECISIVE] Vacate-vs-autofill CONTRADICTION + ordering
- My §2/§6 said BOTH "vacate → floor the meter" AND "autofill the office" — MUTUALLY EXCLUSIVE. Autofilling
  in the same immediate means the seat is never observed vacant, so the floor-to-25 never manifests (zero
  durable hit), and worse, a fresh clean jinshi RAISES the recomputed perf above the corrupt incumbent
  (removing the crook IMPROVES GC perf — inverts the intent). FIX: use BARE QING_office_vacate (or
  QING_office_vacate_dispatch_nobackfill, se_QING_COUNCIL.txt:1659) — NO autofill — so the seat sits empty
  (perf floored to 25 + qing_office_vacancy_strain 3650d) until the player re-appoints. The genuine durable hit.
  (qing_office.1 uses QING_office_vacate_dispatch which DOES autofill — #27's escalation must use the
  no-backfill form to get the durable vacancy.)
- **VACATE BEFORE KILL** (mandatory order): on_character_death auto-runs QING_office_vacate_dispatch (WITH
  backfill) if qing_office_held is still set. Kill-first → death hook spawns a replacement (undoes the
  vacancy). Vacate-first (bare vacate removes qing_office_held) → the death hook self-guards + no-ops → seat
  stays empty. So vacate → then kill.
- IMPRISON branch: reuse QING_justice_strip_for_trial (se_QING_JUSTICE.txt:315-325) — imprison rejects
  serving officials, so strip office/command/governorship first.
- TREASURY windfall: keep ≈150 (the codebase's Heshen-confiscation ceiling, qing_office.1.a / se_QING_EMERITUS),
  ideally scaled to qing_corruption_level — NOT "years of revenue" (out of scale).
- Throttle: qing_gc_event_slot_used is effectively QUARTERLY (reset gated by a 90d cooldown), hang off
  QING_GOV_pulse with a days=3650 cooldown. NOTE: task tag "#27" collides with the shipped frontier-march
  subsidy — use a fresh tag for traceability comments.

## 0. Intent (user)
A SEPARATE event chain from qing_integ.11: a scandal implicating a TOP-LEVEL Grand Council minister
(Grand Minister of Revenue 戶部 / Works 工部). Heshen (和珅) archetype — much more serious repercussions,
a TRIAL, and it fires MUCH LESS OFTEN.

## 1. Building blocks (all verified in-repo)
- **Culprit:** the seated GC minister — held as char-ref var `qing_office_revenue_holder` / `qing_office_works_holder`
  on CHI (also `qing_office_held = flag:revenue/works` on the character). Read `var:qing_office_revenue_holder = { ... }`.
- **Trial organ:** the Censorate (都察院). The impeach flow is proven: `qing_censorate_impeach_venal`
  (QING_censorate_panel.txt:125) → hidden trampoline event (qing_censorate.5) → `QING_censorate_find_corrupt`
  (se_QING_CENSORATE.txt:98, an ordered_character by corruption). Model the trial on this.
- **Removal + GC-perf hit (THE CLEAN MECHANISM):** `QING_office_vacate = { office = revenue }`
  (se_QING_COUNCIL.txt:1611) removes the holder; `QING_ministry_recompute_perf_revenue` (se_QING_MINISTRY.txt:805)
  FLOORS qing_min_perf_revenue LOW when the office is VACANT (:801). So removing the corrupt minister
  DURABLY drops the ministry meter until refilled — NO derived-meter nudge needed (avoids the meter-concretize
  trap: the perf meter is recomputed from scratch each pulse, so a one-shot change_variable would be erased;
  vacate-the-holder is the concrete, durable hit). Refill via `QING_council_autofill_office = { office = revenue degree = jinshi }`.
- **Rarity throttle:** `qing_gc_event_slot_used` (the shared quarterly court-event slot, reset monthly —
  se_QING_AMBAN.txt:361/367, se_QING_CANTON.txt:231) + a long cooldown var + gates (a minister seated, high
  corruption). Fire from a low-frequency pulse (a court/GC pulse), NOT the integration reaction roll.
- **Treasury windfall (Heshen confiscation):** add_treasury on the impeach-and-confiscate resolution
  (Heshen's confiscated fortune ~ years of revenue — a large one-time +). Proven add_treasury.

## 2. The chain (namespace qing_gcscandal, or reuse a court namespace)
- **.1 THE SCANDAL SURFACES.** Fired from a court/GC pulse when: a Revenue OR Works minister is seated,
  realm corruption high (qing_corruption_level) OR the minister's own corruption/honesty poor, the court-slot
  free, off cooldown. Picks the culprit = the seated minister (prefer the more-corrupt of Revenue/Works, or
  the one whose ministry meter is worst). Options:
  - **Impanel a tribunal (審理)** → trial (.2). The proper course.
  - **Suppress the memorial (壓摺)** → hush it: the minister stays, corruption festers (a lingering realm
    modifier / stability hit), legitimacy risk if it later resurfaces.
- **.2 THE TRIAL.** (Censorate-led.) A skill/evidence check — e.g. the Censorate holder's finesse/zeal vs the
  minister's finesse (a powerful minister can beat the rap), or a random_list weighted by evidence. Outcomes:
  - **CONVICTED (.3):** the Heshen fall. `QING_office_vacate` the minister (→ ministry meter floors),
    confiscate his fortune (large add_treasury), stability +/legitimacy + (justice served) but a shock to the
    council; optionally imprison/execute the character (death or imprisonment). Autofill the vacated office.
  - **ACQUITTED / WHITEWASHED (.4):** the minister survives (too powerful / bought the court); corruption
    entrenches (realm corruption up, a "faction protects him" modifier), legitimacy/stability hit, the player
    is marked as unable to discipline the great offices.
- (Optional .5 hidden trampoline if any option needs an ordered_character/sorting iterator — the #34
  no-inline-in-scripted_gui rule; but these are EVENTS not scripted_guis, so inline ordered_character is
  fine per se_QING_CENSORATE precedent — confirm.)

## 3. Repercussions (bigger than the amban scandal)
- Convict: large treasury windfall (confiscation), the ministry meter floors (vacancy) → GC effectiveness
  dips until refilled → a real governance disruption; stability/legitimacy +; the minister dies/imprisoned.
- Acquit: realm corruption entrenches (durable), legitimacy/stability −, a lingering "protected faction"
  modifier. Both outcomes are weightier than qing_integ.11's amban-scale prominence/Lifan nudge.

## 4. Frequency (RARE — the key contrast with #22)
- Fire from a LOW-frequency court pulse, gated: minister seated + high corruption + court-slot free + a long
  cooldown (e.g. set qing_gcscandal_cooldown days = 3650, so ~once a decade at most). Optionally once-per-reign.
- NOT the integration reaction roll (that's #22's common amban scandal). Distinct namespace, distinct trigger.

## 5. Files affected
- NEW `events/imp19c_mod_events/qing_gcscandal_events.txt` — the .1-.4 chain (+ .5 if needed).
- NEW loc `localization/english/qing_gcscandal_l_english.yml` (BOM).
- `common/scripted_effects/se_QING_*.txt` — a small dispatcher (find the corrupt minister, gate, fire .1),
  hung off an existing court/GC pulse (e.g. QING_GOV_pulse or the ministry pulse). Reuse QING_office_vacate /
  QING_council_autofill_office / the court-slot throttle.
- Possibly a character/country modifier for "protected faction" (acquit) + "disgraced" (convict) — check if
  suitable ones exist before minting.

## 6. Build checklist
1. Dispatcher: on the court pulse, if a Revenue/Works minister seated + corruption high + slot free + off
   cooldown → save the culprit minister as a scope → fire .1 (claim the slot + set cooldown).
2. Write .1 (surface: tribunal vs suppress), .2 (trial: check → convict/acquit), .3 (convict: vacate +
   confiscate + autofill + character fate), .4 (acquit: corruption entrenches).
3. GC-perf hit = QING_office_vacate (NOT a meter nudge) — the recompute floors the vacant ministry.
4. Loc (BOM, no #/$macro$ in LOG strings), LOG every branch sys = QING.
5. Review + boot-test: fires rarely; convict floors the ministry meter + windfall; acquit entrenches corruption.

## 7. Risks
- **R1 double-count / meter trap:** do NOT nudge qing_min_perf_revenue directly (recomputed each pulse →
  erased). Use vacate-the-holder (durable, concrete). ✓ designed this way.
- **R2 rarity:** must NOT become common (the whole point vs #22). Long cooldown + court-slot + high-corruption
  gate. Verify the pulse it hangs on isn't high-frequency.
- **R3 culprit exists:** gate on a Revenue/Works minister actually SEATED (var:qing_office_X_holder alive +
  employed). If both vacant, no scandal.
- **R4 char fate on a setup officer:** death/imprison on the minister — confirm safe (the create_character
  death gotcha is about boot-time HEALTH traits, not runtime death; runtime death is fine).
- **R5 overlap with #22 + the Censorate's own impeach lever:** #27 (senior minister, rare) vs #22 (amban,
  common) vs the existing qing_censorate_impeach_venal (player-initiated, any venal courtier). Ensure #27's
  auto-fired chain doesn't collide with the player's manual impeach (e.g. don't target a minister already
  mid-impeach; share the cooldown if needed).

## 8. GUESS FLAGS (autonomous — for user review)
- Whether the culprit is ALWAYS the worse of Revenue/Works, or could be any top GC office (chancellor/
  grand_secretariat). GUESS: Revenue + Works only (the fiscal offices that touch the silver/canal funds —
  the Heshen register); broaden later if wanted.
- The trial resolution mechanic (skill check vs random_list). GUESS: a skill check (Censorate finesse+zeal vs
  minister finesse) with a corruption/evidence modifier — more characterful than a flat roll.
- Convict = death or imprisonment or just dismissal+confiscation. GUESS: dismissal + confiscation always;
  death/imprisonment as a player CHOICE at the convict step (mercy vs the full Heshen forced-suicide).
- Cooldown length (~decade) + whether once-per-reign. GUESS: 10-year cooldown, not once-per-reign (a long
  reign could see two).
