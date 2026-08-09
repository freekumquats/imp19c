# DESIGN v2 — Task #1: Rescale Qing event pay-for-benefit treasury costs into the hundreds (cap ~1200)

Status: DESIGN v2 (post adversarial-review-1). Branch merge-overnight. 2026-08-09.
v1 refuted on 3 points (event-level gate miss, verb-delivered costs skipped, FlavorEvents generic).
This v2 addresses all three.

## Problem

Qing player events/ministry-buttons charge gold via `add_treasury = -X`, gated on `treasury >= X`,
described to the player in loc as "Costs ¥X". Costs cluster in the **tens** (modal 30–80). But the
treasury is seeded at `-24 × quarterly costs` (`se_QING_MECHANICS.txt:834`) ≈ 6 years' running costs, so
a 40-gold choice is noise. User wants them lifted **into the hundreds**, capped **~1200**, so a
pay-for-benefit choice is a real fiscal decision.

## The single mapping rule (one closed form, applied to EVERY in-scope value)

    new = round-to-nearest-5( 40 × sqrt(old) )

Verified over the complete distinct Qing cost/gate set {10,15,…,180,200,220,240,250,300,500,900}:
**strictly monotonic, zero collisions, caps exactly at 1200 (900→1200), modal 30–80 → 220–360.**
A closed-form monotonic map is chosen deliberately over a piecewise table because **a monotonic function
preserves equality**: wherever `gate == cost` today, `map(gate) == map(cost)` after — so gate/cost coupling
holds automatically, with NO proximity heuristic (this is the fix to v1's event-level-gate miss). A √ curve
(vs linear ×5) compresses the top so the three campaign sinks 250/500/900 ramp gracefully to the cap instead
of colliding at a clamp.

Sample: 10→125, 20→180, 30→220, 40→255, 50→285, 60→310, 70→335, 80→360, 90→380, 100→400, 120→440,
130→455, 140→475, 150→490, 180→535, 200→565, 220→595, 240→620, 250→630, 300→695, 500→895, 900→1200.

## Scope — the coherent "player-initiated Qing spend" surface (events + the buttons that share their verbs)

**Fix to v1 finding 1 (event-level gates):** ALL `treasury >= X` in the in-scope files are mapped, not just
option-adjacent ones — the monotonic map keeps every gate consistent with the cost it guards regardless of
distance. qing_war.3:314 (>=150) and qing_war.4:419 (>=50) now scale with their option costs.

**Fix to v1 finding 4 (verb-delivered costs):** the verbs that events call to charge gold are IN, at the
verb body — `QING_household_replenish_purse`/`_workshop_commission` (`cost=$X$` params at call sites +
gates), `QING_anticorruption_audit`, `QING_suppress_sects`, the works verbs, caravan escort, summer-palace
`QING_sp_yiheyuan_from_treasury`. These verbs are ALSO called by ministry buttons; since verb and button
share one body, the button gates in `common/scripted_guis/QING_*.txt` move in lockstep (else button desyncs
from its own cost). Buttons are in by necessity, not scope creep — they cannot be separated from the events.

**IN (mechanic):**
- `events/imp19c_mod_events/qing_*.txt` + `currency_crisis_events.txt`: every `add_treasury = -Xint`,
  every `treasury >= X` (excl. `var:` / `negative_treasury`), every verb `cost = -X` param.
- `common/scripted_effects/se_QING_*.txt`: every hardcoded `add_treasury = -Xint` in a player-spend verb
  (incl. the Wall/Canal 240/220 — rescaling them too, to 620/595, keeps them the costliest actions so the
  ordering "a great work > a flavor event" is preserved; leaving them would let a 450 exam rival the Wall)
  **AND every effect-internal `treasury >= X` guard that protects such a charge** (excl. `var:` /
  `negative_treasury`). [review-1 fix] These self-guarding verbs — `se_QING_CARAVAN.txt:503` `limit = {
  treasury >= 300 … }` guarding the -300 escort, `se_QING_WORKS.txt:443/485` guarding the -240 wall / -220
  canal — MUST scale their guard in lockstep with the co-located charge, or the guard stops protecting it
  (fires with 300 in the bank, drives treasury to -395). The monotonic map keeps `guard == charge`
  automatically; the point is only that the guard is explicitly IN, not omitted. `manpower >=` on the same
  line is untouched (not a treasury axis).
- `common/scripted_guis/QING_*.txt`: every `treasury >= X` gate + any inline `add_treasury = -X`.

**IN (loc):** the free-text cost mentions that mirror these numbers, rescaled by a NUMBER-LEVEL classifier
(not a verb-prefix regex — that missed real costs). [review-1 fix] For every 2–3 digit number whose raw
value is in the in-scope cost set, in an EVENT/BUTTON key (`.tt`/`_tt`/`_TT`, never `_DESC`/`_DESCRIPTION`
and never a `custom_tooltip` wired from `common/missions/`), it is rescaled iff BOTH:
  (1) TREASURY-associated — a `¥` immediately precedes, OR "treasury of" precedes, OR the nearest resource
      noun after it (before the next number) is treasury/gold/silver (not political/legitimacy/manpower/
      influence/prestige/stability/…); AND
  (2) a COST not a gain — nearest signal before it: a leading `+` or gain-verb (raise/gain/reclaim/seize/
      saved/enrich/…) ⇒ gain (skip); a leading `-` or cost-verb (cost[:]/costs/spend/pay/requires/"treasury
      of") ⇒ cost. Plus a same-line cost-restatement rule (a value confirmed a cost anywhere on the line is
      that cost wherever it recurs, e.g. "spend ¥140 … and ¥140"; verified 0 cost/gain value collisions
      across the corpus). This catches the `Cost:`-colon, lowercase-verb, parenthetical `(-150 gold)`,
      bare `treasury of N`, and multi-resource `240 treasury AND 10 manpower` forms the old rule missed,
      while leaving every `+N Treasury` / "Raise ~¥80" gain untouched. Manifest-eyeballed clean.

**OUT (explicit, not deferred — a defensible subsystem boundary):**
- **The mission system** — `common/missions/*.txt` (253 own costs) + mission-only loc files + mission keys
  inside mixed loc files. Missions do NOT share event verbs (verified: no event verb is called from
  common/missions/), live in their own file tree, and are not "events." "Event pay-for-benefit costs" does
  not name the mission trees. (If the user later wants missions rescaled, that is its own task with its own
  calibration — mission costs interact with mission-reward pacing, not the event economy.)
- **Non-Qing events** — `usa_1812_events.txt`, `spa_america_events.txt`, and the generic `flavor_eve.*`
  set in `FlavorEvents.txt` (fires for any tag — v1 wrongly included it; rescaling would hit non-Qing
  players). OUT, per the non-Qing principle.
- **Positive `add_treasury`** (rewards/windfalls) and `add_treasury = var:` (formula-driven). Untouched.

## Implementation — dry-run manifest first, then apply

1. Python script defines `map(x)=round5(40√x)` and an in-scope file list (globs above).
2. **Mechanic pass:** rewrite `add_treasury = -X` → `-map(X)`, `treasury >= X` → `>= map(X)`, `cost = -X`
   → `-map(X)`. Integer + leading-minus anchored (no decimals exist — verified; positives/`var:` skipped).
3. **Loc pass:** build the mission-key exclusion set (keys in mission-only loc files + `*_mission_*`/known
   mission-tree keys in mixed files). For each event/button loc line, rescale a cost-context number per the
   (a)(b)(c) rule above.
4. **Dry run → manifest** (file:line, old→new, matched text) for BOTH passes. I review the manifest by eye
   for any mis-hit (a reward caught, a mission key caught, a non-cost number caught) BEFORE applying.
5. Apply; re-run inventory → assert: strictly-monotonic map, **0 gate≠cost mismatches** among option-local
   pairs, every new cost in [50,1200], brace/paren balance unchanged, EOL/BOM per file preserved.
6. Adversarial code-review on the applied diff (not just the design). Fix findings. Commit + push.

## Risk / blast radius

- Digits only — no logic/scope/structure change. AI unaffected (ai_chance untouched). Currency sim (#23)
  untouched (that is `gbip`/`add_treasury` is a different axis).
- Worst failure = a loc tooltip that disagrees with its mechanic (caught by the key-by-key rule + manifest
  eyeball), or a gate/cost desync (caught by the monotonic map + post-apply mismatch assertion).
- The manifest step is the safety net that makes a ~100-file numeric sweep reviewable rather than blind.
