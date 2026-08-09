# Design — Frontier-customs superintendents: #111 Hoppo (Canton) · #112 Caravan superintendent + Kokandi aqsaqal

**Status:** DESIGN, not built. For adversarial review BEFORE any code. Consolidated 2026-08-09
(merges the earlier DESIGN_HOPPO_STATS_CANTON_111 draft + the #112 task scope).
**Theme:** concrete-over-abstract. A frontier-customs SUPERINTENDENT is a real character whose FULL
attribute set continuously drives the trade's revenue, skim, and events — at BOTH gates of the empire:
Canton (粵海關, the Hoppo — already a character, #69) and Kashgar (the caravan 參贊大臣 — not yet a
character). At Kashgar the Qing official contends with a real Kokandi counterparty, the aqsaqal.

---

## 1. Decisions locked (user, this session)

1. **#111 — the Hoppo's FULL attributes continuously drive Canton revenue + skim**, not just corruption→a
   single squeeze cliff, and his EVENTS are updated + EXPANDED.
2. **#112 — create the caravan superintendent (喀什噶爾參贊大臣) as a real character** whose attributes drive
   caravan customs revenue + skim, mirroring the Hoppo.
3. **#112 — the aqsaqal is a real character too: a FOREIGNER FROM KOKAND resident in Xinjiang** (allegiance
   to c:KOK), NOT a Qing office-holder — distinct from the Qing-employed Uighur begs.
4. **Every superintendent↔aqsaqal event/option outcome is a contest of their RELATIVE attributes** — the
   full stat set (finesse/charisma/zeal/martial/corruption), each mapped to a concrete role — shown as
   percentages (reusing the amban-negotiation svalue pattern).
5. **UI placement:** Hoppo → the Canton mechanism / its existing surface; caravan superintendent + aqsaqal →
   the **CARAVAN TRADE panel** (gui/qing_caravan.gui), NOT the Xinjiang window (the begs live there; the
   caravan officials belong on the caravan panel).
6. **Reuse proven scaffolding:** the beg corps (qing_xj_begs — real Uighur characters via create_character +
   set_as_minor_character + move_country, marked qing_is_xj_beg) and the Hoppo appoint/reconcile/siphon/impeach.

Design-first; each slice its own IMPLEMENTATION design + adversarial review + commit.

## 2. Current state (verified)

**Canton / Hoppo (se_QING_CANTON.txt).** Hoppo IS a real char (#69): `qing_hoppo_holder` + marker,
appointed `order_by finesse` (:349). ONLY corruption drives ongoing trade — `qing_hoppo_squeeze =
holder.corruption` (:299); `squeeze>=60 → yield ×0.7` (:133-135, a single CLIFF); `siphon = yield ×
corruption/200 → add_gold` to him, confiscated on impeach (#68/#70). Finesse used only at appoint/rotate
(:349/:417); charisma unused. ONE event: `qing_canton.1` "The Hong Merchants Cannot Pay" (Cohong crisis) —
already reads real corruption for impeach(`>10`)/caution(`<=10`).

**Caravan (se_QING_CARAVAN.txt).** NO superintendent character — abstract meters only
(qing_caravan_prosperity, qing_caravan_customs_rate 0/1/2, qing_caravan_bazaar_count, qing_xinjiang_control);
`add_treasury` at :227 (money, no silver — correct: Xinjiang is a silver SINK via xiexiang, already modelled).
The **aqsaqal exists only as a FLAG** (`qing_caravan_aqsaqal_granted`) via `qing_caravan.1` "The Kokand
Ultimatum" (+`.2`/`.3`). Caravan panel (gui/qing_caravan.gui) verified in #99.

**Beg corps (se_QING_XINJIANG.txt) — the character-corps template:** real Uighur chars, `qing_is_xj_beg`,
held in `qing_xj_begs`, listed on the Xinjiang panel roster. Employer = CHI (Qing-employed locals).

## 3. #111 — grade Canton yield/skim on the Hoppo's stats

Replace the `squeeze>=60 ×0.7` cliff (se_QING_CANTON.txt:133-135) with a CONTINUOUS Hoppo-effectiveness
factor inserted after the port multiplier, before the tariff bias. Read the seated char via the proven
`save_scope_as` → `scope:X.attr` idiom:
- **FINESSE lifts the take** (fiscal competence): deviation from a baseline (~7), small per-point step
  (mirrors the ministry-perf martial/finesse-deviation idiom, se_QING_MINISTRY.txt:199-204).
- **CORRUPTION shaves the take** (graded, replaces the cliff) AND sets the skim (keep siphon = yield×corr/200).
- Net multiplier = 1 + finesse_bonus − corruption_shave, CLAMPED to a sane band (e.g. [0.5,1.3]). Coefficients
  are boot-test knobs tuned to the ~30萬兩/qtr zenith baseline.
- **CHARISMA (optional):** a Cohong-management term easing the Cohong-crisis gate; include or defer (Q).
- Read corruption DIRECTLY off the char (more accurate than the lagged squeeze mirror); KEEP `qing_hoppo_squeeze`
  as the derived meter its OTHER consumers use (corruption-leak :282, Cohong gate :293). Cap-before-vs-after:
  keep the raw 45萬兩 goods-basis cap BEFORE the Hoppo factor (competence may modestly exceed it).

**Compose with the existing event (must-hold):** `qing_canton.1` manipulates corruption + squeeze; #111
READS the stats, must not double-write. It fires on a days delay so its corruption change lands a later
pulse (consistent with the existing 1-quarter lag). Removing the cliff orphans nothing (.1 reads
squeeze/corruption directly, not the cliff).

## 4. #111 — update + expand the Hoppo events

- **UPDATE qing_canton.1**: surface the graded yield in text; keep its corruption reads/squeeze nudges
  consistent with the graded model.
- **EXPAND** (each char-stat-driven, GC/court-slot throttled per #107, percentages-shown per #38/#41, loc +
  no macro-in-LOG; each justified by a concrete lever — do NOT overbuild):
  - a brilliant-Hoppo (high finesse) commendation beat (positive, cooldown-gated, mirrors #107 commend);
  - an early venal-Hoppo exposure (corruption) distinct from the Cohong collapse;
  - a 3-year Neiwufu rotation beat (who replaces him, drawn by finesse — the #389 rotate lever as an event);
  - a smuggling / Western-supercargo dispute where finesse+charisma set the outcome (ties to the frontier-sea file).

## 5. #112 — the caravan superintendent (參贊大臣)

- **Seat a real Qing char** as `qing_caravan_super_holder` + marker: employer=CHI, appointed from free
  courtiers `order_by` the relevant skill, subject to the 1:1 court-position rules (#76/#89 — add the marker
  to QING_char_holds_court_position). Reuse the Hoppo appoint/reconcile/siphon/impeach scaffolding wholesale.
- **His attributes drive caravan customs revenue + skim** — grade the abstract `qing_caravan_customs_rate`
  yield the way #111 grades Canton (finesse lifts, corruption shaves + skims real confiscable wealth).
- **Surface on the Caravan panel** as a summit office-card (Guard/Censor card idiom).
- **Verify:** new office vs reusing the ILI amban (the amban system posts residents to subjects; the 參贊大臣
  is a Qing court appointee superintending the trade — likely a NEW office; confirm against amban code).

## 6. #112 — the aqsaqal (a Kokandi foreigner resident at Kashgar)

- **Create as a real character**, NOT a flag: Kokandi/Central-Asian culture, allegiance/employer = c:KOK
  (a FOREIGN resident on Qing soil — NO Qing court marker), located at Kashgar. Reuse the beg-corps
  create_character idiom but with the foreign allegiance. His loyalty-to-Kokand / opinion is the concession
  friction lever (ties to the #13/#20 khoja chain + the KOK opinion).
- **Verify the create_character idiom** for a foreign-employed char resident in another country's territory
  (proven forms only — this is the one unproven-capability risk in #112; check TI/Invictus/vanilla first).
- **Surface on the Caravan panel** as a foreign-counterparty card, visibly distinct from the employed begs.

## 7. #112 — the relative-attribute contest (the heart of it)

The superintendent↔aqsaqal relationship and EVERY event/option outcome is a contest of their RELATIVE
attributes. Full stat set → concrete roles (for BOTH characters):
- **FINESSE** = fiscal / administrative / bargaining skill (the core customs-deal stat).
- **CHARISMA** = personal influence / diplomacy (winning the begs & merchants; the aqsaqal's sway).
- **ZEAL** = ideological/religious firmness (the aqsaqal's khoja/Islamic appeal vs the superintendent's
  Confucian rectitude; resistance to being suborned).
- **MARTIAL** = willingness/ability to coerce (threaten escort/force; the aqsaqal invoking Kokandi raiders).
- **CORRUPTION** = venality (lowers the superintendent's honest take + raises collusion risk; a venal
  aqsaqal is bribable).
Each event branch computes odds from the RELEVANT attributes of BOTH chars (e.g. a concession negotiation =
super.finesse+charisma vs aqsaqal.finesse+zeal; a coercion branch weights martial; a collusion branch weights
corruption), reusing the PROVEN amban-negotiation svalue pattern (#49/#61, `qing_amban_negotiate_chance_svalue`
— stash the odds on the char, render via `[X.MakeScope.GetVariable('…').GetValue]`), SHOWN as percentages
summing to 100 ("On Success (X%)", #38/#41). Which attributes weight which branch is the design's explicit
mapping job (§9 Q).

**Events:** update qing_caravan.1/.2/.3 to read the two real characters; add beats — concession negotiation,
collusion/extortion, competent-superintendent commendation, Kokand-pressure escalation (the foreigner
leveraging Khanate backing → ties to the khoja invasions). CHI player-gated, court-slot throttled,
percentages-shown, loc + no macro-in-LOG.

## 8. Build sequence (each its own IMPLEMENTATION design + adversarial review + commit)
1. #111a — grade Canton yield/skim on Hoppo finesse+corruption (replace the cliff).
2. #111b — update + expand Hoppo events.
3. #112a — caravan superintendent character + grade caravan customs on his stats + Caravan-panel card.
4. #112b — aqsaqal as a Kokandi-foreigner character + Caravan-panel counterparty card.
5. #112c — superintendent↔aqsaqal relative-attribute contest events.

## 9. Open questions for review
1. #111 coefficient spread ([0.5,1.3] band, finesse/corruption steps) vs the ~30萬兩 baseline — too swingy?
   Interaction with the currency system (#23): the Canton yield feeds treasury + silver reserve; confirm the
   max uplift is modest/bounded so it can't perturb the money model.
2. #111 charisma→Cohong term: now or defer?
3. #112 new office vs reusing the ILI amban — confirm.
4. #112 aqsaqal create_character as a c:KOK foreigner resident on CHI soil — is this a PROVEN capability?
   (The single highest-risk item; verify vs oracles before building. If unproven → boot-spike.)
5. Attribute→branch weighting map for the contest (§7) — is the proposed mapping sound/legible to the player?
6. Do two more court offices (Hoppo already exists; +caravan superintendent) strain the 1:1 court-position
   system or the GC event-slot budget? (#89/#107 throttle interplay.)

## 9b. ADVERSARIAL REVIEW FINDINGS (2026-08-09) — PROCEED with corrections

Verdict: source grounding strong; concrete thrust sound. Corrections (must fold into the per-slice impl designs):

**CORRECTIONS to this doc's wording (were inaccurate):**
1. §3 "stat-deviation svalue idiom" is MISLABELLED — se_QING_MINISTRY.txt:199-214 is inline
   set_variable/change_variable deviation MATHS (martial−7 ×4), NOT a script_value. The proven capability is
   `save_scope_as → scope:X.finesse` in effect context; cite **se_QING_CANAL.txt:109-121** as the cautionary
   precedent (its [review-fix] warns `value = var:X.finesse` reads 0 silently → use save_scope_as).
2. §6 "aqsaqal is a character, NOT a flag" is DANGEROUS as written — it must be a character *IN ADDITION TO*
   the retained `qing_caravan_aqsaqal_granted` flag. That flag gates qing_caravan.1/.2/.3 (trigger :64, option
   triggers :187/:208) + 7 reads; removing it breaks three events. Layer the character ON TOP; keep the flag.
3. §7 "reuse the PROVEN amban-negotiation svalue pattern" for a TWO-SIDED contest is INACCURATE. The amban
   svalue (QING_governance_svalues.txt:102-112, NOT se_QING_AMBAN.txt) is a ONE-SIDED solo roll
   (25 + 2×charisma + finesse, clamped 10..90; _fail = 100−chance). The only two-character helper,
   QING_pair_friction (se_QING_AFFINITY.txt:461-585), yields a symmetric friction score NEVER rendered as odds.
   A two-sided WIN-PROBABILITY contest shown as competing percentages is NET-NEW (composable from proven parts:
   two-scope stat reads + the 100−X complement) — #112c must BUILD + boot-verify it, not assume drop-in.

**#111 ORDERING HAZARD (MEDIUM — resolve in the #111a impl design):** the yield is computed + banked
(:155-176) BEFORE the Hoppo is reconciled (:217-233) / backfilled (:240-256). The current cliff reads LAST
quarter's squeeze meter at :133 DELIBERATELY (documented :129-132) to avoid reading a dead/double-booked/absent
holder mid-yield. So #111 must NOT `save_scope_as` on var:qing_hoppo_holder at the yield site to read live
finesse/corruption. FIX: mirror finesse into a LAGGED meter at :299 (alongside the squeeze=corruption mirror)
and have the graded factor read the two LAGGED meters — preserving the established ordering.

**CONFIRMED sound:** #111 cliff location + compose-with-qing_canton.1 (reads stats not the cliff, no double-write);
KEEP qing_hoppo_squeeze (3 consumers: corruption-leak :309-315, Cohong gate :320-330, event trigger); #112 new
office is the right call vs the ILI amban (posted amban's employer=subject, different role); 1:1 join = add a
qing_caravan_super_marker to QING_char_holds_court_position (qing_dynasty_triggers.txt:241-255, where the Hoppo
marker already sits :253); caravan panel exists but has NO card scaffolding — the Guard/Censorate cpt_button
`.GetCharacter` idiom (qing_guard.gui:103-131) is the proven clone, keyed to new holder vars.

**TWO BOOT-SPIKES required before #112b/#112c (net-new capabilities the doc wrongly treated as reuse):**
- SPIKE 1 (highest risk): `create_character` + `move_country = c:KOK` — KOK is an INDEPENDENT NON-SUBJECT
  foreign power (the begs employ to c:XNG, a CHI SUBJECT, and pin to NO province — NOT a precedent). The spike
  must test: (a) create + move_country to a non-subject foreign country; (b) does he render/persist on the
  Caravan panel via .GetCharacter; (c) LIFECYCLE — KOK conquered/annexed/at-war must not leave a dangling
  character (on-map-object-lifecycle-symmetry rule); DESIGN THE TEARDOWN PATH before building the card.
- SPIKE 2: a minimal two-sided contest svalue (super stats vs aqsaqal stats → win-prob) rendered as summed
  percentages — verify the render before scaling to all the contest events.

**OVERBUILD trims (#111b/#112c):** the "3-year Neiwufu rotation as an event" DUPLICATES the existing manual
QING_canton_rotate_hoppo lever (se_QING_CANTON.txt:397) — only keep it as a PASSIVE/random rotation with a
distinct outcome, else cut. The smuggling/supercargo beat is the only Hoppo beat with no existing lever — keep
only if it earns a distinct mechanical outcome. Budget the shared GC court slot: ~8 new throttled beats all
claim qing_gc_event_slot_used (#107) — the impl design must state cooldowns + confirm the slot isn't starved.

**BUILD ORDER (confirmed):** #111a (grade yield — do the lagged-meter fix) → #111b (events, trimmed) →
SPIKE 1 + SPIKE 2 → #112a (superintendent) → #112b (aqsaqal char, after spike 1) → #112c (contest, after spike 2).

## 10. Evidence files
- `se_QING_CANTON.txt` (Hoppo model + yield chain + qing_canton.1); `events/…/qing_canton_events.txt`.
- `se_QING_CARAVAN.txt` (caravan meters, :227 add_treasury); `events/…/qing_caravan_events.txt` (.1/.2/.3);
  `gui/qing_caravan.gui` (caravan panel).
- `se_QING_XINJIANG.txt` (beg-corps character template); `se_QING_AMBAN.txt` (appoint/negotiate pattern,
  qing_amban_negotiate_chance_svalue); `se_QING_MINISTRY.txt:199-204` (stat-deviation svalue idiom).
