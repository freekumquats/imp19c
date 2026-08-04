# DESIGN — Amban & Garrison as gating actors in the subject-integration event chain

Tasks #7 + #8 (2026-08-04). #7 is two concrete fixes inside the chain #8 overhauls, so they
are one piece of work.

## The user's ask (verbatim intent)
- "The Chieftain Resists" says the subject is in revolt but does not actually trigger a war —
  the "crush the revolt" option should start a REAL war, not abstractly crush it.
- The same event's "marry into the family" option should ACTUALLY marry characters.
- The local amban and garrison "should not only be mentioned but should directly influence the
  event choices" — "the local amban can negotiate or flee, the local garrison can march out or
  retreat into its fortress."
- Choices "dictated by the loyalty of the amban, and the strength of the garrison relative to
  the subject, and similar appropriate factors."
- ALL subject-integration events get the overhaul, not just The Chieftain Resists.

## The chain today (events/imp19c_mod_events/)
`qing_subject_integration.txt` — .10 unrest, .11 scandal, .12 ethnic strife, .20 harvest, .21 festival.
`qing_integration_capstone_events.txt` — .30 capstone/absorb, .40 incorporation decree, .41 resistance.
In every event `ROOT`/`this` = overlord (CHI player); `scope:target` = the subject governorship.

## The two actors, and how they are already tracked (no new bookkeeping)
- **Amban.** The subject carries `qing_amban_here` (se_QING_AMBAN.txt) — a var on the SUBJECT-country
  scope holding the resident amban's CHARACTER scope. He is a CHI-employed courtier, so his
  `loyalty` reads directly. Presence = `scope:target = { has_variable = qing_amban_here` AND the held
  char `is_alive = yes` `employer = ROOT` }`.
- **Garrison.** The subject carries `qing_frontier_garrisoned` (se_QING_FRONTIER.txt, set for ~200
  days whenever a CHI-controlled banner garrison stands on the subject's soil). Presence = that var.
  The garrison itself is a CHI army standing in a subject-owned province — its `unit_size` is the
  strength proxy, reachable by the SAME `every_army { unit_location.owner = scope:target }` walk
  QING_fgar_scan already uses. Subject strength proxy = the subject's own `any_army` unit_size sum
  (or, when it fields none, its `manpower`).

## New shared resolver — SUBJ_QING_resolve_integ_actors (se_SUBJECT_QING.txt or a new se file)
Called from each event's `immediate`, at COUNTRY (ROOT=CHI) scope, expects `scope:target`. Saves:
- `scope:integ_amban` (+ flag var `integ_amban_present`) — the live resident amban, if any.
- `integ_amban_loyal` (int 0/1/2 band on his loyalty: <40 wavering, 40-70 steady, >70 staunch).
- `integ_garrison_size` (summed CHI garrison unit_size on the subject's soil; 0 = none present).
- `integ_subject_size` (subject army unit_size sum; falls back to a manpower-derived proxy).
- `integ_garrison_edge` (int band: 2 = garrison clearly outweighs subject, 1 = rough parity,
  0 = subject outweighs / no garrison) — the "strength of the garrison relative to the subject".
All scratch country vars, removed by the event tail (or overwritten next resolve). Proven idioms
only: every_army + unit_location.owner (QING_fgar_scan), var-holding-a-char-scope (qing_amban_here),
LITERAL-RHS integer bands (RHS-comparison rule).

## How the actors gate the choices (per the user)
The resolver's outputs make actor-flavoured options APPEAR / disappear and shift outcomes:
- **Amban staunch + present** → an "the amban negotiates a settlement" option (cheap de-escalation:
  small integration step kept, loyalty of amban spent as the currency); amban wavering/absent →
  that option is hidden and instead the amban "flees his post" flavour fires (he loses the resident
  modifier; a small stability/legitimacy ding).
- **Garrison edge = 2 (outweighs)** → "the garrison marches out and crushes the rising in the field"
  is offered and is CHEAPER / lower-risk. Edge ≤1 → "the garrison retreats into its fortress" — it
  holds but cannot pacify; crushing then needs a real field army (the war path below), at full cost.
- These gate via `trigger = {}` on the option + `custom_tooltip`, the established pattern in the chain.

## #7a — "Crush" becomes a REAL war (qing_integ.41.b)
Faithful model: a subject in open revolt has thrown off the yoke — so the crush is a re-subjugation
WAR, not an abstract counter. Proven idiom (se_QING_JAPAN_PREPERRY.txt:199-214): `ROOT = {
release_subject = scope:target }` then `FUNC_declare_war_with_wargoal_province = { war_goal =
conquer_wargoal / reconquest_wargoal  province = <a subject province>  target = scope:target }`
(FUNC_declare_war_with_wargoal_province — imp19c_setup_events.txt:54). Gate the field-crush on a
garrison/army able to prosecute it; keep the treasury/tyranny/AE costs. If the garrison edge is
high, alternatively `start_civil_war` behind a loyal claimant is the lighter "crush in place" — but
the clean, user-legible path is release+declare, so that is the primary. LOG both branches.

## #7b — "Marry into the family" becomes a REAL marriage (qing_integ.41.c)
Proven idiom (se_MARRIAGE.txt:305-372, Invictus me_bithynia): pick an unmarried adult child of the
chieftain (`scope:target.current_ruler.ordered_child`, opposite sex, `is_married=no`), save as
`scope:integ_bride`; pick an unmarried adult of the imperial house (`ROOT.current_ruler.ordered_child`
or a from_ruler_family court adult), `marry_character = scope:integ_bride`. Guard the whole thing on
both existing (else the co-opt still works via gold/prestige, just without the wedding). This makes
the "marry into his family" text literally true.

## Scope of the overhaul across the chain (#8)
- **.41 resistance** — full treatment (both #7 fixes + amban/garrison actor options). This is the
  event the user named; it is the centre of gravity.
- **.10 unrest / .12 ethnic strife** — actor-gated: a present, loyal amban lets a "the amban
  restores order by persuasion" option replace pure force; a strong garrison makes the crush
  cheaper; neither present makes the situation worse (the flavour the user wants).
- **.30 capstone / .40 decree** — the resolver runs so the DESC can name the amban/garrison, and
  the coercive paths key off garrison presence (a coercive absorb with no garrison is dearer).
- **.11 scandal / .20 harvest / .21 festival** — lighter touch: resolver runs for DESC colour and
  the amban can be the pinned official / the honoured host, but no new hard gates (these are not
  force-vs-persuasion dilemmas). Keeps the overhaul consistent without inventing conflict where the
  event has none.

## Non-goals / guardrails
- No new persistent per-subject bookkeeping — reuse qing_amban_here + qing_frontier_garrisoned.
- No engine-unproven verbs. release_subject, FUNC_declare_war_with_wargoal_province, start_civil_war,
  marry_character, every_army/unit_location are all proven in-repo (cited above).
- Integer-band scratch vars only, LITERAL RHS on every comparison (RHS-comparison rule).
- se_LOG enter/exit + LOG_line on every new effect and every war/marriage branch (error-logging rule).
- Marriage & war both fully guarded so a missing child / freed-already subject degrades to a no-op,
  never a broken portrait or a dangling scope (mirrors the chain's existing self-abort triggers).

## Decisions log (implemented 2026-08-04)
- **Resolver lives in se_SUBJECT_QING.txt** (SUBJ_QING_resolve_integ_actors + _clear_integ_actors),
  beside the rest of the integration machinery. Outputs: integ_amban_present, scope:integ_amban,
  integ_amban_band (0/1/2), integ_garrison_size, integ_subject_size, integ_garrison_edge (0/1/2).
- **integ_amban_band initialized UNCONDITIONALLY to 0** at the top of resolve, so every option
  trigger/effect reads it without a missing-var fetch (the RHS-comparison / missing-var trap). Band 0
  = absent OR wavering; integ_amban_present distinguishes them where it matters (the "amban flees"
  flavour keys on NOT present OR band 0).
- **Garrison edge via a scratch delta** (garrison_size − subject_size), banded with LITERAL RHS
  (delta >= 4 → 2 dominant; >= -3 → 1 parity; else 0), because a var-ref on a comparison RHS is
  illegal (the RHS-comparison rule). Delta var removed at the end of resolve.
- **Army-size accumulation uses the proven `<iterated> = { ROOT = { change_variable = { add =
  prev.X } } }` idiom** (se_QING_COUNCIL.txt:591); prev inside the ROOT block resolves to the iterated
  army, and unit_size is a readable value (se_ARMY.txt:26). Garrison loop filters CHI armies whose
  unit_location.owner = scope:target; subject loop iterates scope:target's own armies.
- **#7a crush = REAL war**: SUBJ_QING_crush_revolt_war reparents sub-subjects (so they don't dangle),
  release_subject, then FUNC_declare_war_with_wargoal_province { conquer_wargoal, a rebel province,
  target = the freed rebel }. All proven (JAPAN_PREPERRY release+war; setup_events declare-war func;
  reparent helper). Fully guarded on a live landed subject.
- **#7b marry = REAL marriage**: SUBJ_QING_marry_into_chieftain weds the eldest eligible imperial
  prince (current_ruler.ordered_child, male, unmarried adult) to the chieftain's eldest eligible
  daughter (opposite sex), marry_character (Invictus me_bithynia idiom, se_MARRIAGE.txt:305-372).
  Guarded both sides — no eligible child ⇒ wedding skipped, co-opt gold/prestige still lands.
- **Actor-gated options added**: .41.d (staunch amban negotiates), .10.d (steady amban calms unrest),
  .12.d (steady amban mediates) — all hidden unless a present amban of the required band sits.
  Garrison edge cheapens the force paths (.41.b, .10.a, .12.a, .30.c) and, when dominant, has the
  garrison march out (.41.b) vs hold its fortress. A wavering/absent amban flees his post (.41.b).
- **Lighter touch on .11 scandal / .20 harvest / .21 festival**: NOT overhauled — these are not
  force-vs-persuasion dilemmas, so inventing amban/garrison gates there would be gratuitous. The
  resolver is not run for them (no wasted work). Consistent-where-it-fits, not uniform-for-its-own-sake.
- **Every new option calls SUBJ_QING_clear_integ_actors at its tail** so the scratch vars never
  outlive the event. se_LOG enter/exit + LOG_line on every new effect and war/marriage branch.
- Braces verified balanced on all four touched files.
