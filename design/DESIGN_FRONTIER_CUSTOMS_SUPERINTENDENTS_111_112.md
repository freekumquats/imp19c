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

## 9c. #111b IMPLEMENTATION DESIGN (2026-08-09) — update + expand the Hoppo events

Scope: `events/imp19c_mod_events/qing_canton_events.txt` + `localization/english/qing_mechanics_l_english.yml`
only (NO scripted-effect changes except the two new pulse-gated `trigger_event` blocks + one passive-rotation
hook in `se_QING_CANTON.txt`). Grounded reads done: qing_canton.1 (3 options), #111a graded-yield block
(se_QING_CANTON.txt:137-174), the reconcile mirror that sets `qing_hoppo_finesse`/`qing_hoppo_squeeze`
(:337/:345), the Cohong gate (:367-377), `QING_censorate_impeach_uphold` (confiscates wealth 抄家,
se_QING_CENSORATE.txt:269-274), `qing_amban_negotiate_chance_svalue` (one-sided roll, QING_governance_svalues
.txt:102-122), loyalty_qing_commended reward idiom (qing_censorate_events.txt:162).

### A. UPDATE qing_canton.1 (the Cohong crisis) — text + option-b consistency
- **Text only** for the graded-yield surfacing: the `.desc`/`.b.tt` loc already speaks of the Hoppo's
  "squeeze" as the source; add ONE clause to `.1.desc` that the customs the throne actually receives now
  rises and falls with the man's **competence AND his squeeze** (matches #111a's continuous factor), so the
  player reads why a capable honest Hoppo matters. NO mechanical change to options a/b/c — they already read
  `qing_hoppo_holder.corruption` / nudge `qing_hoppo_squeeze` directly (the graded model reads those same
  meters; #111a introduced NO new option-side writes). **Loc bug caught while grounding:** `.1.a.tt` says
  "Spends ~220萬兩" but the effect draws `qing_canton_customs −30` + ruler `add_gold −24` — the 220 is a stale
  copy-paste from the pop-relief tooltip. FIX the number to ~30萬兩 (matches the `>= 30` gate + `subtract = 30`).

### B. ADD qing_canton.2 — VENAL-HOPPO EXPOSURE (an early, distinct beat before the Cohong collapse)
Distinct from .1 (which fires on high **squeeze** = the merchants buckling): .2 fires when the seated Hoppo
has personally amassed a **large graft hoard** (his `wealth`, the #69 siphon) while squeeze is only *moderate*
— i.e. the corruption is caught EARLY, before it has cascaded into a Cohong debt crisis. A memorial from a
Canton censor names the hoard. Distinct mechanical outcome from .1.b: this is a *pre-emptive* impeachment
choice keyed on the concrete **wealth** lever, not the squeeze meter.
- **Gate (in QING_canton_pulse, a NEW throttled block alongside the Cohong gate :367-377):**
  ```
  if = {
      limit = {
          has_variable = qing_hoppo_holder
          var:qing_hoppo_holder = { is_alive = yes  wealth >= 150 }   # a fat siphon hoard
          var:qing_hoppo_squeeze < 65                                  # BELOW the Cohong-crisis band (mutually exclusive with .1)
          NOT = { has_variable = qing_canton_venal_cooldown }
          NOT = { has_variable = qing_gc_event_slot_used }
      }
      set_variable = { name = qing_canton_venal_cooldown  days = 1825 }   # ~5y throttle (rarer than the 3y Cohong)
      set_variable = { name = qing_gc_event_slot_used  value = 1 }
      trigger_event = { id = qing_canton.2  days = { 5 20 } }
      LOG_line = { sys = QING  msg = "canton: a censor's memorial exposes the Hoppo's hoard for" }
  }
  ```
  Ordering: **[R2 fix]** the three Canton gates run in order **commend (.3) → venal (.2) → Cohong (.1)** in
  the pulse (see §E; the earlier "sits AFTER the Cohong gate" wording was wrong — struck). .1 (squeeze≥65) and
  .2 (squeeze<65) ARE band-disjoint so they never collide. `wealth` is a proven char trigger
  (character_events.txt:374 `wealth >= 500`).
- **Event .2 options:**
  - **(a) Impeach through the Censorate now (抄家).** Re-uses the EXACT proven path from .1.b's
    corruption>10 branch: save the holder as `scope:qing_censorate_target`, strip his `qing_hoppo_marker`,
    `QING_censorate_impeach_uphold = yes` (this confiscates his hoard to the treasury, disgraces him, vacates
    the post), `remove_variable = qing_hoppo_holder` (pulse backfills a fresh man), corruption-level nudge −5,
    `add_legitimacy = 3`. Distinct from .1.b: fires on the wealth trigger BEFORE the debt crisis, so the
    confiscated hoard is the reward for vigilance.
  - **(b) Quietly transfer him (調任) — take the customary cut.** The corrupt but useful Neiwufu bondservant
    is rotated out without scandal; the throne pockets a share of his hoard as an informal "gift". Effect:
    **[R1 fix]** the holder is a VARIABLE, not a saved scope — reading `var:qing_hoppo_holder.wealth` in a
    value block reads 0 silently (the se_QING_CANAL.txt:118-120 trap). So FIRST
    `var:qing_hoppo_holder = { save_scope_as = qing_hoppo_seated }`, THEN
    `add_treasury = { value = scope:qing_hoppo_seated.wealth  divide = 3 }` (a third, the customary squeeze on
    the squeezer — the PROVEN saved-scope value-block form, se_QING_CENSORATE.txt:271). He KEEPS the other 2/3
    (no `add_gold = -wealth` strip — intentional, unlike the impeach path). Then rotate via the existing
    `QING_canton_rotate_hoppo` lever (fresh man, squeeze eases). No disgrace, no legitimacy. A cynical middle
    path — realistic Qing practice (Heshen-era).
  - **(c) Look away (留中不發).** The memorial is "kept in the palace" (unactioned). Squeeze nudge +4, a small
    `qing_corruption_level` +2 leak. No cost, festering graft.

### C. ADD qing_canton.3 — BRILLIANT-HOPPO COMMENDATION (positive, high-finesse)
Fires when the seated Hoppo is **highly competent AND honest** (high finesse, low squeeze) — the throne's
Canton spring runs rich and clean. A commendation beat mirroring #107. Distinct mechanical lever: rewards the
CHARACTER (loyalty + a modest wealth grant) and gives a one-off customs bonus, keyed on **finesse** (the stat
#111a made matter). No existing lever does this (rotate is neutral/negative-facing).
- **Gate (a third throttled block in the pulse):**
  ```
  if = {
      limit = {
          has_variable = qing_hoppo_holder
          # [R2 fix] add wealth < 150 — venal (.2) and commend (.3) are NOT band-disjoint by squeeze alone
          # (a competent honest-LOOKING Hoppo at squeeze 30 with a 150+ secret hoard qualifies for BOTH).
          # Exclude the hoarder here so a man sitting on a graft pile can never be commended; the venal beat
          # (.2) claims him instead. Now the two ARE disjoint (wealth<150 commend vs wealth>=150 venal),
          # not merely slot-guarded.
          var:qing_hoppo_holder = { is_alive = yes  finesse >= 9  wealth < 150 }
          var:qing_hoppo_squeeze < 35                                  # genuinely honest
          NOT = { has_variable = qing_canton_commend_cooldown }
          NOT = { has_variable = qing_gc_event_slot_used }
      }
      set_variable = { name = qing_canton_commend_cooldown  days = 2555 }   # ~7y (rare, positive)
      set_variable = { name = qing_gc_event_slot_used  value = 1 }
      trigger_event = { id = qing_canton.3  days = { 5 20 } }
  }
  ```
  Ordering: place this block FIRST of the three (positive beat is rarest + narrowest gate: finesse≥9 AND
  squeeze<35 AND wealth<150). All three share the slot guard so at most one fires per pulse. **[R5 note]**
  drop the redundant `is_ai = no` on all three new gates — the whole on_action is already CHI/`is_ai = no`
  (matches the existing Cohong gate, which omits it).
- **Event .3 options:**
  - **(a) Commend him (嘉獎) — a plaque and a bonus.** Holder `add_loyalty = loyalty_qing_commended` +
    a modest `add_gold` (an honest reward, NOT a siphon), `add_stability = 1`, and a one-off customs top-up
    `qing_canton_customs += 10` (his clean administration delivered a surplus). Percentages-N/A (no roll).
  - **(b) Promote him to a metropolitan post (內遷) — lose him at Canton.** He's too good to leave milking
    trade; recall him to the capital. Effect: `add_legitimacy = 2`, then `QING_canton_rotate_hoppo` (he
    leaves, a new — likely lesser — man takes over). The trade-off: reward the realm's meritocracy at the
    cost of Canton's best administrator. Distinct outcome from (a).

### D. §9b OVERBUILD TRIMS — honored
- **3-year Neiwufu rotation → CUT ENTIRELY.** §9b permitted a passive rotation ONLY "with a distinct
  outcome, else cut." **[R3 fix]** The adversarial review of THIS impl design confirmed the proposed passive
  `random = { chance = 8 ... QING_canton_rotate_hoppo }` has NO distinct outcome — it calls the manual
  button's effect verbatim; only the trigger differs (no player click), and "a distinct trigger is not a
  distinct outcome." It also carried a real hazard: an 8%/quarter roll could churn away the exact
  high-finesse honest Hoppo that #111a + the commend beat (.3) are built to reward, and the gate was
  self-contradictory ("served long" but "no tenure var"). **DECISION: CUT.** The manual `QING_canton_rotate_hoppo`
  button already gives the player rotation agency; a mechanically-identical passive copy is pure churn risk.
  Recorded loudly per the no-silent-cut rule — this is the §9b-licensed "else cut", NOT a deferral.
- **Smuggling / Western-supercargo beat → FOLDED, not a 4th event.** §9b: keep only if it earns a distinct
  mechanical outcome. It does NOT (a smuggling dispute resolves to the same squeeze/corruption/legitimacy
  levers the three beats already cover, and the two-sided finesse+charisma contest belongs to #112c's
  net-new svalue, NOT proven here). **DECISION: CUT** to conserve the shared GC slot (three throttled beats
  is already a real budget draw). Recorded loudly here per the no-silent-cut rule — this is a scope trim the
  §9b review explicitly licensed, NOT a deferral of required work.

### E. GC EVENT-SLOT BUDGET (per #107 — must state cooldowns + confirm no starvation)
**TWO new throttled beats** (venal .2, commend .3) + the existing Cohong crisis (.1) all claim
`qing_gc_event_slot_used`, cleared at the top of every quarterly pulse (verified: on_action/00_monthly_country
.txt:80, unconditional, before any roller). The passive rotation was CUT (§D) so it no longer figures.
Cooldowns: Cohong 3y (existing), venal-exposure **5y**, commendation **7y**. Mutual exclusivity is now by
BAND for every pair: Cohong squeeze≥65 / venal wealth≥150 & squeeze<65 / commend finesse≥9 & squeeze<35 &
**wealth<150** (the R2 fix makes venal vs commend disjoint too, not merely slot-guarded). The per-pulse slot
guard is the belt-and-suspenders backstop. Long cooldowns (5–7y) mean Canton's slot draw is far below the
shared budget's other claimants (dynasty/faction/war fire on their own bands). No starvation: Canton yields
the slot 3 of 4 quarters even in its rare firing years, and a pre-empted beat wastes no cooldown (cooldown +
slot are both set INSIDE the slot-guarded `if`, so it simply retries next pulse). **Ordering in the pulse:
commend gate → venal gate → Cohong gate** (rarest/narrowest first; defensive even though bands are disjoint).

### F. Consistency / traps checklist (self-review before dispatch)
- No macro `$param$` or `#`/`$` in any LOG string (all new LOG_line are plain prose). ✓ planned
- percentages-shown: N/A — none of the three beats is a two-sided ROLL (those are #112c). The one place a
  roll could appear (smuggling) was CUT. Options are deterministic; tooltips state exact effects. ✓
- RHS-comparison rule: all new triggers are var-vs-LITERAL (`wealth >= 150`, `finesse >= 9`,
  `qing_hoppo_squeeze < 65`) — bare-legal, no `_cmpsvalue` needed. ✓
- No double-write vs #111a: the events read/nudge `qing_hoppo_squeeze` + holder corruption/wealth exactly as
  .1 already does; #111a only READS the lagged mirrors at the yield site — no conflict. ✓
- Impeach path re-uses the PROVEN .1.b sequence verbatim — **[R4 fix]** correct order is **save scope →
  marker-strip → uphold → remove holder** (you cannot strip the marker off scope:qing_censorate_target before
  that scope is saved; qing_canton_events.txt:78-84). QING_censorate_impeach_uphold does NOT touch the bespoke
  qing_hoppo_marker, so the explicit strip IS required. ✓  The .2.b transfer cut reads `scope:X.wealth` after a
  `save_scope_as` (NOT `var:X.wealth`, which reads 0 — R1) then `divide = 3`. ✓
- BOM: qing_canton_events.txt is a se-adjacent event file (no-BOM/LF); loc yml keeps its BOM. Verify diffstat
  no EOL churn. ✓ planned
- New vars to seed? `qing_canton_venal_cooldown` / `_commend_cooldown` are set-on-fire cooldowns (has_variable
  guard, never read as a value) — NO init seed needed (mirrors the existing `qing_canton_cohong_cooldown`,
  which is also unseed­ed). ✓

### G. #111b CODE REVIEW (2026-08-09) — PASS, 2 LOW accepted
Full code review of the built diff returned **PASS — no critical/medium**; brace balance (se 216/216,
events 75/75 after the is_alive hardening), BOM (events no-BOM / loc BOM), RHS-rule, proven-idiom reuse all
confirmed. Two LOW observations:
- **LOW-1 (venal gate keys on total `wealth`, not just siphoned graft) — ACCEPTED as a design nuance.** A
  Hoppo personally rich AT APPOINTMENT (`wealth>=150`) trips the venal beat for a hoard he didn't squeeze.
  In practice the appoint picker draws ordinary courtiers (modest starting wealth) and the #69 siphon
  accrues over tenure, so it reads correctly almost always. There is NO separate "graft-only wealth" stat to
  key on (the siphon is add_gold into his single wealth pool), so keying on total wealth is the only concrete
  lever available — the concrete-over-abstract choice. Not worth a synthetic graft-ledger var. Left as-is.
- **LOW-2 (dead-holder-in-the-gap) — FIXED.** Added `var:qing_hoppo_holder = { is_alive = yes }` to the .2/.3
  event triggers (matches the .1.b option-limit form, events:83) so a Hoppo dying in the 5–20-day schedule
  delay can't render a dead portrait / silently no-op the options. (The base .1 shares the weaker
  has_variable-only trigger; out of #111b scope, not touched.)

## 10. Evidence files
- `se_QING_CANTON.txt` (Hoppo model + yield chain + qing_canton.1); `events/…/qing_canton_events.txt`.
- `se_QING_CARAVAN.txt` (caravan meters, :227 add_treasury); `events/…/qing_caravan_events.txt` (.1/.2/.3);
  `gui/qing_caravan.gui` (caravan panel).
- `se_QING_XINJIANG.txt` (beg-corps character template); `se_QING_AMBAN.txt` (appoint/negotiate pattern,
  qing_amban_negotiate_chance_svalue); `se_QING_MINISTRY.txt:199-204` (stat-deviation svalue idiom).

## 9d. #112a IMPLEMENTATION DESIGN (2026-08-09) — the caravan superintendent (喀什噶爾參贊大臣)

Scope: a NEW se_QING_CARAVAN_SUPER.txt (or a block appended to se_QING_CARAVAN.txt) + the caravan pulse hook
+ QING_char_holds_court_position marker + gui/qing_caravan.gui card + loc. Mirrors the Hoppo model
(#69/#111a) WHOLESALE — this is the caravan twin of the 粵海關監督. NO unproven capability (a Qing court char,
employer=CHI — the proven appoint/reconcile/siphon idiom; NOT the aqsaqal foreigner, which is #112b + SPIKE 1).

**Confirmed (review §9b): NEW office, not the ILI amban** — the amban posts a resident to a SUBJECT
(employer=subject); the 參贊大臣 is a CHI court appointee superintending the trade (employer=CHI). Different role.

**State (on CHI), mirroring the Hoppo:**
- `qing_caravan_super_holder` — the seated char (country link). `qing_caravan_super_marker` — on the man
  (per-char post marker; ADD to QING_char_holds_court_position, beside qing_hoppo_marker).
- `qing_caravan_super_finesse` — lagged finesse mirror (for the yield grade; set at reconcile).
- `qing_caravan_super_squeeze` — DERIVED from his corruption (the graft meter), like qing_hoppo_squeeze.

**A. APPOINT (QING_caravan_super_appoint):** clone QING_canton_appoint_hoppo — ordered_character employer=ROOT,
adult/alive/not-ruler/not-general/admiral/governor, NOT QING_char_holds_court_position, NOT hard_disgraced,
not heir; order_by finesse; max=1; save + set qing_caravan_super_holder + qing_caravan_super_marker.

**B. INIT + SEAT (in QING_caravan_init):** seed qing_caravan_super_squeeze baseline (30) + finesse mirror (7)
if unset; if NOT has qing_caravan_super_holder → appoint one (the post is always filled, like the Hoppo #66).

**C. GRADE THE CARAVAN YIELD (in QING_caravan_pulse, at the income calc ~:38-52):** apply the SAME continuous
factor #111a uses on Canton: factor = 1 + (super_finesse−7)×0.03 − super_squeeze×0.004, clamped [0.5,1.3],
multiplied into qing_caravan_income_tmp BEFORE it's banked/published. Reads the LAGGED mirrors (set later in
the pulse's reconcile block) — the same one-quarter-lag design as the Hoppo (avoids a live read at the yield
site before reconcile). Guarded on has_variable so pre-first-reconcile is a clean ×1.

**D. RECONCILE + GRAFT (new block at the pulse tail, mirroring se_QING_CANTON:273-347):** backfill a
dead/missing holder; graft creep (add_corruption +1/qtr capped <90); SIPHON = income × corruption / 200 as
REAL add_gold to him (confiscable on impeach — touches only his char wealth, NOT treasury/silver, so it
can't perturb #23 currency); set qing_caravan_super_squeeze = his corruption; set qing_caravan_super_finesse
= his finesse (lagged mirror for C).

**E. ROTATE lever (QING_caravan_super_rotate):** clone QING_canton_rotate_hoppo — relieve + re-appoint, ease
the squeeze; a high-finesse man eases more. (Panel button — the player's proactive lever.)

**F. PANEL CARD (gui/qing_caravan.gui):** a summit office-card, the proven
`datacontext="[Player.MakeScope.Var('qing_caravan_super_holder').GetCharacter]"` clone (qing_guard.gui:103),
visible via a scripted_gui qing_caravan_super_seated (has_variable holder). Shows his name + finesse (the
governing skill). Place near the top of the caravan panel, above the aqsaqal debug card.

**G. IMPEACH:** reuse the proven censorate path (as the Hoppo does in qing_canton.1.b) — a venal superintendent
event is #112c's territory; for #112a the graft is made concrete (siphon) and the ROTATE lever + a future
event handle it. Do NOT build a bespoke impeach here (the censorate uphold + marker-strip is the shared path).

**Traps checklist:** no macro/# in LOG strings; RHS var-vs-literal only; save_scope_as→scope:X.finesse for
char reads (NOT var:X.finesse — reads 0); lagged mirror at reconcile not live read at yield; factor clamp
[0.5,1.3] bounds the currency-perturbation risk (same as #111a); marker added to court-position for 1:1;
se_QING_* file no-BOM/LF, gui/loc keep their conventions. Each of A–G reviewed before commit.

### 9d-R. #112a DESIGN CORRECTIONS after adversarial review (2026-08-09) — re-grounded to current line numbers

Real se_QING_CARAVAN.txt layout: income built :201-224 (throughput × rate-factor :207-215 × Kokand /2
:216-224), banked add_treasury :227, published qing_caravan_income_last :234, **income_tmp REMOVED :235**,
pulse continues (KOK opinion :249-259, event offers) and ENDS :313. QING_caravan_init :70-85 uses a SINGLE
`NOT has_variable qing_caravan_initialized` guard wrapping all seeds.

- **C-1 (CRITICAL) — siphon must read qing_caravan_income_last, NOT income_tmp.** income_tmp is removed at
  :235; a Hoppo-style tail reconcile would read a dead var → siphon permanently 0. FIX: the new reconcile/
  graft/siphon block is inserted AFTER :235 (before the KOK-opinion block ~:249) and the siphon computes
  `siphon = qing_caravan_income_last × corruption / DIV`. income_last is the fully-processed (graded,
  post-Kokand) take — a coherent siphon base, and it persists (never removed).
- **M-1 — add the double-book relief block** (mirror se_QING_CANTON:255-271) at the top of the reconcile:
  if the seated holder is now is_general/is_admiral/is_governor/has qing_officer_marker → strip
  qing_caravan_super_marker + remove holder (next backfill re-seats). Same 1:1 hazard as the Hoppo.
- **M-2 — init seeds OUTSIDE the qing_caravan_initialized block.** Place the super-var seeds
  (qing_caravan_super_squeeze=30, _finesse=7) + the init appoint each behind their OWN
  `if NOT has_variable` guard, OUTSIDE the single-guard initialized block, so existing saves backfill them
  (matching QING_canton_init:58-79). Otherwise the seat is empty on existing saves until pulse 1.
- **M-3 — re-scale the siphon divisor to caravan magnitudes.** Caravan income ~2-4/qtr (vs Canton ~30), so
  /200 yields a cosmetic ~1-2 gold hoard. Use `/20` (corruption 30 on income 4 ≈ 0.6/qtr; corruption 90 on
  income 6 ≈ 2.7/qtr — a hoard that actually accrues). NOTE for #112c: any venal-superintendent wealth gate
  must be scaled to this (NOT the Hoppo's wealth>=150; use a caravan-appropriate threshold or a tenure gate).
- **L-1 — grade order:** insert the superintendent factor immediately after the rate-factor block (~:215),
  BEFORE the Kokand /2 haircut, so the two throne-side multipliers sit together and Kokand cuts the graded base.
- **L-2 — currency-safety rationale corrected:** caravan income is add_treasury ONLY (no silver, file
  header :42) — grading it CANNOT perturb the #23 currency model (unlike Canton, which feeds
  silver_reserve_size). The [0.5,1.3] clamp is treasury-swing sanity, not currency-coupling. Siphon (add_gold
  to char) is currency-safe (matches Hoppo).
- **FILE PLACEMENT:** APPEND to se_QING_CARAVAN.txt (the pulse grade + reconcile MUST live there; appoint/
  rotate/init keep the coupled logic in one file, as the Hoppo does). No separate se_QING_CARAVAN_SUPER.txt.
