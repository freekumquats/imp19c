# DESIGN — #63 give the Opium Commissioner a real revenue stream and a squeeze meter

> STATUS 2026-08-14: FINAL v7 — round-6 adversarial review complete, VERDICT: READY FOR
> IMPLEMENTATION. Round 6 independently re-verified round 5's fix (ease call moved into
> `QING_opium_appoint_commissioner`) against live source: confirmed both real callers of that
> wrapper are genuine one-shot event paths never reachable from `_reconcile`'s backfill, confirmed
> `QING_opium_commissioner_appoint` has exactly the 2 callers the doc claims (backfill + the
> wrapper) with no third path, and re-traced all four seating paths end-to-end finding no further
> same-call-overwrite hazard, no scope bug, and no double-fire risk (the `qing_lin_zexu_appointed`
> guard is permanently one-shot — confirmed `remove_variable` on it appears nowhere in the repo).
> Fixed 2 trivial LOW citation drifts (`QING_opium_treaty_legalize` :421-428→:421-427,
> `QING_opium_crackdown_destroy` :397-404→:398-407) found in the same pass. No further review
> rounds needed — 6 rounds, each surfacing a genuine bug in the prior round's fix, now converged
> to a clean, independently-confirmed design.
>
> STATUS (superseded, kept for provenance): round 5 re-verified both
> round-4 fixes hold correctly IN ISOLATION, then found a NEW interaction bug between them (exactly
> what round 4 asked round 5 to check for): the ease call, placed at `QING_opium_commissioner_
> appoint`'s top level per round 4's fix, fires on EVERY call to that shared function — including
> `QING_opium_commissioner_reconcile`'s own backfill step, which (per round 4's OTHER fix) is
> immediately followed by the mirror step in the SAME call, flatly overwriting whatever the ease
> call just computed. Not a correctness bug, but it silently defeats the ease mechanic's purpose
> (a one-quarter "new broom" bridge) for the backfill/relief paths — the most common real
> invocations of auto-pick. Fixed by moving the ease call OUT of the shared
> `QING_opium_commissioner_appoint` and INTO `QING_opium_appoint_commissioner` (the one-shot guard,
> confirmed NEVER called from inside `_reconcile`), restoring the exact separation Salt/Caravan/
> Canton already use (their ease calls live only in player-only `_rotate` wrappers, never in the
> shared `_appoint`/backfill path).
>
> STATUS (superseded, kept for provenance): round 4 traced all four
> seating entry paths end-to-end against the corrected sketch and found round 3's fixes were
> directionally right but incomplete in two more load-bearing ways, both fixed below: (1) the
> mirror block was sequenced BEFORE backfill in every prior draft, unlike Salt/Canton/Caravan's
> real (a)relief→(b)backfill→(c)mirror ordering — this left the squeeze meter stale for a full
> quarter on ANY backfill event (not just relief+backfill), since the mirror's own `is_alive=yes`
> gate fails before backfill has run. Fixed by moving the mirror to run AFTER backfill, matching
> the real precedent exactly. (2) The auto-pick ease-call placement instruction ("after the `_seat`
> call returns, still in country scope") was scope-ambiguous — read literally it places the call
> INSIDE the `ordered_character` block that seats the commissioner, where `this` is the candidate
> character, not CHI (the SAME scope-confusion class this file's own cr97 fix already warns about
> for this office) — which would silently no-op, identical in kind to the bug round 3 just fixed
> for the old inside-`_seat` placement. Fixed with an explicit, unambiguous code snippet placing
> the call after the `ordered_character` block's closing brace, at the function's own top level.
>
> STATUS (superseded, kept for provenance): round 3 found round 2's H-2
> fix was INCOMPLETE in two load-bearing ways, both fixed below: (1) the double-book relief block
> calls `remove_variable = qing_opium_commissioner_holder`, but Opium's EXISTING backfill step
> (`:312-322`, untouched by round 2's fix) only fires when the holder var EXISTS and is dead —
> unlike Salt's own backfill, which also fires when the var is ABSENT. Without also editing that
> existing limit to add the missing `OR = { NOT = { has_variable = ... } ... } }` clause (Salt's
> exact form), a double-book relief would strand the post PERMANENTLY vacant with no player lever
> to recover it — not "one extra quarter" as v3 claimed. Fixed below by adding this as a required
> edit to EXISTING code, not just new code. (2) the "ease on appointment" instruction told the
> implementer to add the ease call inside `QING_opium_commissioner_seat`, citing "the other 3 and
> #62's Customs" as precedent — round 3 found BOTH citations false (Customs never uses this
> helper at all; Salt/Caravan/Canton call it from COUNTRY-scope sites AFTER seating, never from
> inside their own character-scope `_seat` helpers) and the placement itself risky (character-scope
> unwrapped call, the same class of bug this file's own cr97 fix already warned about). Fixed
> below by moving the ease call to `se_QING_FRONTIER_PICKER.txt`'s existing opium branch (player
> path) and to `QING_opium_commissioner_appoint` itself (auto-pick path, confirmed country-scope).
>
> STATUS (superseded, kept for provenance): round 2 found two concrete
> fixes needed: (H-1) the posture=1 revenue block's alternate placement option ("a new small
> quarterly step") was a LIVE BUG TRAP, not a valid alternative — `qing_opium_outflow_tmp` is a
> pure scratch var, `remove_variable`'d at the end of `QING_opium_assess_trade_balance` every
> pulse, so any separate function reading it would see zero forever, silently killing the whole
> feature. Fixed below by pinning the ONLY correct insertion point (inside that same function,
> before its own `remove_variable` line) and deleting the alternative. (H-2) `QING_opium_
> commissioner_reconcile`'s own header comment explicitly justifies skipping the double-book
> guard Salt/Canton/Caravan/Customs all carry, on the stated grounds that "this office carries no
> squeeze/graft meter" — a premise this very design falsifies. Resolved below: add the same
> double-book guard, not silently inherit stale reasoning. Round 2 also RESOLVED open question #5
> (mirroring #62's vacancy-decay) with a finding, not an import: Opium's vacancy shape is
> DIFFERENT from Customs' — `QING_opium_commissioner_reconcile` runs a synchronous, same-pulse
> death-backfill every quarter (confirmed via the pulse call chain), unlike Customs' single,
> possibly-never-firing appointment path with no succession mechanism at all. The only real
> vacancy window for Opium is PRE-first-appointment, during which the whole attenuation branch is
> unreached anyway (gated on `qing_lin_zexu_appointed`) — so NO decay mechanism is needed here;
> importing #62's fix would be solving a problem this office doesn't actually have.
>
> STATUS (superseded, kept for provenance): round 1 confirmed the central
> claim (interdiction ≠ revenue-farming) and Option A's core direction, but found: (H1, HIGH)
> Option A's proposed hard threshold ("squeeze >= 60, attenuate toward 0") repeats a mistake this
> codebase already made and fixed TWICE elsewhere — `se_QING_CANTON.txt:137` (#111a) explicitly
> retired a squeeze>=60 cliff for the same reason, and `DESIGN_59` independently rediscovered and
> rejected the same shape. Fixed below: continuous attenuation, not a cliff. (H2, HIGH) Option A's
> framing ("the Commissioner is bribed") directly conflicts with flavor text this mod ALREADY
> shipped elsewhere describing this exact office as defined by incorruptibility (Lin Zexu spawns
> specifically as "the incorruptible... a man who cannot be bought"). Fixed below: mechanic and
> loc are about whoever the PLAYER APPOINTS (a game-mechanical slot with a corruption stat, same
> as the other 3 offices), never about Lin Zexu personally — round 1 also found the shared
> frontier-picker UI already shows a corruption stat for this exact office today, unused, which
> supports keeping the mechanic on the appointee rather than inventing a different actor. (M1,
> MEDIUM, pulled into scope) Round 1 found a real, ALREADY-CODED precedent this draft missed:
> `qing_opium.1`'s tolerate option (`events/imp19c_mod_events/qing_opium_events.txt`) already
> grants a one-shot `add_treasury = 20` on adopting posture=1 (弛禁徵稅, "wink at the trade and tax
> it instead"). This is real, sourced, and already partially built — round 1's recommendation
> (adopted below) is to make this a RECURRING quarterly credit under posture=1, generalizing an
> existing mechanism rather than inventing one, and giving the task's original "revenue" framing
> a genuinely sourced home instead of leaving it entirely on the Commissioner's shoulders.

## Task text

Follow-up from #51/#59. User: "the revenue/squeeze from the newly added opium commissioner"
should also reflect on the Revenue Minister's performance, matching Salt/Canton/Caravan/(Customs,
#62). #59's own research found Opium has NEITHER a real recurring revenue stream NOR a squeeze
meter, and explicitly scoped it out as a bigger, separately-designed lift. This is that design.

## Ground truth (traced this session — the central finding that reshapes this whole design)

**The Opium Commissioner is NOT a revenue-farming office. He is an INTERDICTION office.**
Confirmed by direct read of `se_QING_OPIUM.txt`'s own header (`:13-18`) and mechanics:

- `qing_lin_zexu_appointed` — "an Imperial Commissioner is enforcing interdiction." The post's
  entire modeled function, per the ramp-climb logic (`:109-113`): appointing a Commissioner under
  a prohibition posture (`qing_opium_posture = 0`) makes the opium-import-intensity ramp SHRINK
  (`qing_opium_climb_tmp = -4`, vs. the default `+3`). He actively fights the trade; he does not
  farm it. Contrast directly with Salt/Canton/Caravan, whose whole modeled function is COLLECTING
  revenue from a trade the state administers, which their squeeze meters then represent graft
  skimmed FROM that collection.
- Money does flow from opium in this file, but it is tied to POLICY (`qing_opium_posture`), not
  to the Commissioner: `QING_opium_treaty_legalize` (`:421-427`) is a ONE-SHOT, treaty-triggered
  effect (`add_treasury = 40`, "the opium tariff... at scale") that fires on legalization
  regardless of who holds — or whether anyone holds — the Commissioner post. This is the ONLY
  `add_treasury` call anywhere in the file (confirmed by #59's own research), and it's explicitly
  a ONE-TIME historical-moment payment (the Tianjin treaty tariff), not a recurring quarterly
  stream comparable to `qing_salt_income_last`/`qing_canton_last_state`/`qing_caravan_income_
  last`/`qing_customs_income_last`.
- The file's own header (`:13-18`) states PLAINLY: "THE GRAND-COUNCIL FOLD IS ALREADY WIRED...
  opium drain reaches the office-holder TRANSITIVELY: opium net-drain -> qing_currency_stress ->
  qing_min_perf_revenue (d) -> qing_council_eff_target. #366 adds NO new fold." This is a
  DELIBERATE prior design decision, not an oversight — the file's author explicitly considered
  and rejected adding a direct fold, judging the transitive currency-stress path sufficient.

## What this means for the task as originally framed

The user's framing ("the revenue/squeeze from the newly added opium commissioner," matching the
other 3 offices) assumed Opium is parallel in kind to Salt/Canton/Caravan/Customs. It is not — it
is the one office in this cluster whose entire point is fighting a trade, not farming it. Two
honest paths forward, NEITHER of which is "build a revenue stream + squeeze meter exactly like
the other 3," because that would misrepresent what a Qing Opium Commissioner actually was:

### Option A (recommended, revised) — a CORRUPTION meter on the APPOINTED OFFICER (not on any
### named historical figure) representing the opposite failure mode: under-enforcement, not
### collection-skimming
Since the post's entire function is suppression, its failure mode isn't "he takes a cut of a
legitimate revenue stream" (there is no such stream to cut) — it's "the man in the seat
under-enforces, letting the climb run closer to its un-suppressed rate instead of the full `-4`
interdiction rate." This maps cleanly onto state the file already has, AND onto UI the game
already shows: `QING_frontier_office_refresh_candidates`'s shared candidate list already renders
a corruption stat + tooltip for every candidate offered for this exact office today, unused by any
mechanic — round 1 confirmed this. The mechanic below just makes that already-displayed number
matter.

**Framing correction (round-1 H2 fix): this is about WHOEVER THE PLAYER APPOINTS, never about Lin
Zexu specifically.** The mod's own shipped flavor (`qing_roster_events.txt`/loc) introduces Lin
Zexu as "the incorruptible... a man who cannot be bought" — a real, deliberate characterization
this design must not contradict. The squeeze meter models the GAME-MECHANICAL office slot (any
courtier the player or an event seats there), exactly the same way Salt/Canton/Caravan's meters
model whoever sits in THEIR seats, not a claim about a specific named historical person. All loc
text for this mechanic must be written about "the appointed Commissioner" in the abstract, never
naming or implying Lin Zexu's own conduct.

- **New meter**: `qing_opium_commissioner_squeeze` (0..100), mirrored from the seated appointee's
  own `corruption` stat, same proven pattern as the other 3 (using the `save_scope_as` idiom,
  matching #62's own round-1 correction — not a bare attribute read).
- **Mechanical effect — CONTINUOUS, not a cliff (round-1 H1 fix).** A hard threshold on this
  variable was tried and explicitly retired once already in this codebase (`se_QING_CANTON.txt:
  137`, #111a) and independently rejected again by `DESIGN_59`'s own round 1. This design does not
  repeat that mistake a third time. Continuous attenuation of the interdiction bonus:
  ```
  # base interdiction bonus is -4 (posture=0, Commissioner appointed). Attenuate it toward 0
  # continuously as squeeze rises, rather than an all-or-nothing threshold.
  set_variable = { name = qing_opium_climb_tmp  value = -4 }
  change_variable = { name = qing_opium_climb_tmp  multiply = { value = 100  subtract = var:qing_opium_commissioner_squeeze } }
  change_variable = { name = qing_opium_climb_tmp  divide = 100 }
  ```
  At squeeze=0 (clean appointee): full -4 suppression. At squeeze=100 (maximally corrupt): 0
  suppression (the trade climbs at its natural, un-suppressed rate). At squeeze=50: -2, a smooth
  midpoint — no cliff anywhere in the curve.
- **Revenue-Minister fold**: NOT built in this task — matching #59's/#62's own precedent of
  shipping the mechanism separately from wiring it into term (h). Log as the natural next step.

### Posture=1 (tolerate-for-revenue) — pulled INTO this task's scope (round-1 M1)
Round 1 found the task's original "revenue" framing has a real, already-partially-built home:
`qing_opium.1`'s tolerate option already grants a ONE-SHOT `add_treasury = 20` on adopting
posture=1 — a real, sourced mechanism (Qing coastal customs winking at the trade for revenue,
弛禁徵稅) that this draft's v1 missed entirely. Generalizing this into a RECURRING quarterly
credit is a smaller, better-grounded lift than inventing anything: the customs-take already has a
real one-shot precedent; making it recurring under the SAME posture condition (`qing_opium_
posture = 1`) is not fabricating a new mechanism, it's extending an existing one to run every
quarter instead of once.

**Insertion point PINNED (round-2 H-1 fix — the "or a new small quarterly step" alternative in
v2 was a live bug trap and is deleted, not just deprioritized).** `qing_opium_outflow_tmp` is a
pure scratch var, `remove_variable`'d at the very end of `QING_opium_assess_trade_balance`
EVERY pulse (`se_QING_OPIUM.txt:221`, round-3 corrected — v2/v3 miscited this as :220, which
actually removes `qing_opium_inflow_tmp`) — it does not persist outside that one function. Any
separate function attempting to read it would see zero, silently killing this entire feature.
The block below MUST be inlined inside `QING_opium_assess_trade_balance` itself, placed AFTER
the addiction-amplifier add (`:200`) and BEFORE that function's own `remove_variable =
qing_opium_outflow_tmp` (`:221`) — there is no other valid placement:

```
# [inside QING_opium_assess_trade_balance, after the addiction-amplifier add at :200, BEFORE
# the function's own "remove_variable = qing_opium_outflow_tmp" at :221 — qing_opium_outflow_tmp
# does not exist outside this function, so this block cannot live anywhere else]
if = {
	limit = { var:qing_opium_posture = 1 }
	set_variable = { name = qing_opium_tolerate_revenue_tmp  value = var:qing_opium_outflow_tmp }
	change_variable = { name = qing_opium_tolerate_revenue_tmp  divide = 5 }   # [ASSUMPTION] scale factor, boot-tune
	set_variable = { name = qing_opium_income_last  value = var:qing_opium_tolerate_revenue_tmp }
	add_treasury = var:qing_opium_tolerate_revenue_tmp
	remove_variable = qing_opium_tolerate_revenue_tmp
}
else = {
	set_variable = { name = qing_opium_income_last  value = 0 }   # [precedent: qing_caravan_income_last's own "published even at 0" idiom]
}
```
Publishing `qing_opium_income_last` (unconditionally, even at 0) matches the exact idiom Salt/
Canton/Caravan/Customs already use for #59's term (g) — this is the piece that, once built, would
let a FUTURE small addition to term (g) finally include Opium the same way it includes the other
4 streams, closing the loop the user's original request was actually asking for. NOT wired into
term (g) in this task (same precedent as Option A's squeeze — ship the mechanism, wire it later).

### Option B (rejected) — invent a revenue stream anyway
Could construct SOME kind of recurring "confiscation revenue" or "licensed-trade-under-the-table
revenue" stream for the Commissioner to make him parallel to the other 3. REJECTED: this would be
fabricating a fiscal mechanism with no historical basis (the actual Lin Zexu-style commissioner
did not administer a revenue stream — HE DESTROYED CONTRABAND, at Humen he burned it, per
`QING_opium_crackdown_destroy`, `:398-407`, already in this file) purely to satisfy a structural
parallelism the real history doesn't support. This is exactly the kind of invented-to-fit-the-
pattern move the project's own research-first discipline (already applied hard in #58) exists to
prevent.

## Proposed mechanism — full call graph (round-1 L2, resolved, not left approximate)

Round 1 traced the complete init/seat/appoint sequence directly (correcting v1's approximate
citations):

- `QING_opium_init` (`:68-86`) seeds `import_index`/`addicted_share`/`posture` but does NOT
  auto-seat a Commissioner — unlike Salt's "always-filled post" precedent, this office starts
  VACANT. Add the squeeze seed here: `if = { limit = { NOT = { has_variable = qing_opium_
  commissioner_squeeze } } set_variable = { name = qing_opium_commissioner_squeeze value = 30 } }`.
- Seating path: `QING_opium_commissioner_seat` (`:329-357`, character scope, sets holder + flag +
  one-time legitimacy) — called by `QING_opium_commissioner_appoint` (`:362-381`, country-scope
  auto-pick), itself called by `QING_opium_commissioner_reconcile` (`:312-322`, death-backfill)
  and by `QING_opium_appoint_commissioner` (`:387-393`, one-shot guard from `qing_opium.1`'s
  prohibit option and `QING_opium_crackdown_destroy`) — OR directly via the player-picker path,
  `QING_frontier_office_seat_picked` (`se_QING_FRONTIER_PICKER.txt:110-122`).
- **Mirror**: add inside `QING_opium_commissioner_reconcile` (already exists, already handles
  dead-Commissioner cleanup) — guarded on the holder being alive, using the proven `save_scope_as`
  idiom (matching #62's own correction, not a bare attribute read). **[round-4 fix, HIGH — the
  mirror's POSITION relative to backfill was wrong in every prior draft.]** Round 4 traced the
  real Salt/Canton/Caravan reconciles and found ALL THREE order their steps (a) double-book relief
  → (b) backfill → (c)/(d)/(e) mirror — mirror runs STRICTLY AFTER backfill, so a freshly-seated
  holder's corruption gets mirrored the SAME pulse he's seated. Every prior draft of this design
  placed the mirror BEFORE backfill instead — which meant on EITHER a double-book relief OR a
  natural death, the mirror's own `is_alive = yes` gate fails (the holder is dead or just removed)
  before backfill has run, so it never fires that pulse — leaving `qing_opium_commissioner_squeeze`
  stale (holding the prior/dead/relieved holder's last value) for a full quarter on ANY backfill
  event, self-correcting only on the NEXT reconcile call. Not permanent, but a real, avoidable
  divergence from the exact precedent this design claims to mirror. **Fixed: the mirror block now
  runs AFTER the (also-corrected, see below) backfill step, matching Salt/Canton/Caravan's real
  ordering exactly — see the full corrected sequence below.**
  ```
  if = {
  	limit = { has_variable = qing_opium_commissioner_holder  var:qing_opium_commissioner_holder = { is_alive = yes } }
  	var:qing_opium_commissioner_holder = { save_scope_as = qing_opium_commissioner_seated }
  	set_variable = { name = qing_opium_commissioner_squeeze  value = scope:qing_opium_commissioner_seated.corruption }
  }
  ```
  **[RESOLVED, round 2 — was open question #5]** this office does NOT need #62's vacancy-decay
  fix mirrored. `QING_opium_commissioner_reconcile` runs a SYNCHRONOUS, same-pulse death-backfill
  every quarter (confirmed via the pulse call chain: `QING_opium_pulse` calls it, and
  `QING_opium_pulse` is itself called every `QING_DECLINE_pulse`) — genuinely unlike Customs'
  single, possibly-never-firing appointment path with no succession mechanism at all. The only
  real vacancy window here is PRE-first-appointment, before `qing_opium.1` ever fires and the
  player picks "prohibit" — during which the entire attenuation branch above is unreached anyway
  (gated on `has_variable = qing_lin_zexu_appointed`), so the seeded baseline (30) sits inert but
  harmlessly so. Importing #62's decay mechanism here would be solving a problem this office
  doesn't have — do not build it.
- **Double-book guard — RESOLVED, round 2 (was H-2, a live gap this design makes consequential).**
  `QING_opium_commissioner_reconcile`'s own header comment (`:305-311`) explicitly justifies
  skipping the double-book/engine-role check that Salt/Canton/Caravan/Customs all carry, on the
  stated grounds that "this office carries no squeeze/graft meter, so there's nothing else to
  reconcile." This design falsifies that premise the moment the squeeze meter above ships — the
  stale reasoning cannot be silently inherited. Decision: ADD the same guard the other three
  offices carry (checking the office-holder isn't ALSO serving as a general/governor/other
  courtier post before mirroring squeeze onto them), inside the same `if` block as the mirror
  above, immediately before the `save_scope_as` line:
  ```
  # [round-2 H-2 fix] mirrors se_QING_SALT.txt:181-206's (a) double-book relief, byte-for-byte
  # adapted to Opium's own holder/marker var names — real guard var names confirmed by direct
  # grep of se_QING_OPIUM.txt (qing_opium_commissioner_holder/_marker already exist, :46-47/:354)
  # and the shared OR-set Salt/Canton/Caravan all check (is_general/is_admiral/is_governor/
  # qing_officer_marker/qing_customs_ig_marker/qing_court_artist, se_QING_SALT.txt:192-201).
  if = {
  	limit = {
  		has_variable = qing_opium_commissioner_holder
  		var:qing_opium_commissioner_holder = { is_alive = yes }
  		var:qing_opium_commissioner_holder = {
  			OR = {
  				is_general = yes
  				is_admiral = yes
  				is_governor = yes
  				has_variable = qing_officer_marker
  				has_variable = qing_customs_ig_marker
  				has_variable = qing_court_artist
  			}
  		}
  	}
  	var:qing_opium_commissioner_holder = { if = { limit = { has_variable = qing_opium_commissioner_marker }  remove_variable = qing_opium_commissioner_marker } }
  	remove_variable = qing_opium_commissioner_holder
  	LOG_line = { sys = QING  msg = "opium: relieved a double-booked commissioner (also a serving commander/officer/other courtier post) for" }
  }
  ```
  **[round-4 fix — full corrected sequence, replacing the "mirror before backfill" ordering every
  prior draft used]** Placed inside `QING_opium_commissioner_reconcile`, matching Salt/Canton/
  Caravan's real (a)→(b)→(mirror) ordering exactly:
  1. **(a) Double-book relief** (block above) — FIRST.
  2. **(b) Backfill** — Opium's EXISTING dead-Commissioner backfill step (`:312-322`), WITH the
     round-3-required `OR = { NOT = { has_variable = ... } ... } }` edit applied (see below) so it
     also re-fires immediately after relief just cleared the holder, not just on natural death.
  3. **(c) Mirror + squeeze** — MOVED to run AFTER (b), not before it:
     ```
     if = {
     	limit = { has_variable = qing_opium_commissioner_holder  var:qing_opium_commissioner_holder = { is_alive = yes } }
     	var:qing_opium_commissioner_holder = { save_scope_as = qing_opium_commissioner_seated }
     	set_variable = { name = qing_opium_commissioner_squeeze  value = scope:qing_opium_commissioner_seated.corruption }
     }
     ```
     Running the mirror AFTER backfill (rather than before, as every prior draft had it) means a
     freshly-seated holder — whether from relief-then-backfill or a plain natural-death backfill —
     gets his corruption mirrored the SAME pulse he's seated, matching the proven precedent exactly
     instead of leaving the meter stale for one quarter.

  `QING_opium_commissioner_reconcile`'s own header comment (`:305-311`) must also be corrected — it
  currently states this office "carries no squeeze/graft meter, so there's nothing else to
  reconcile," which this design makes false; strike that sentence when implementing.

  **[round-3 fix, HIGH — the "same-pulse backfill" claim above was FALSE as sketched.]** Round 3
  traced Opium's EXISTING backfill limit (`:312-322`) directly:
  ```
  limit = { has_variable = qing_opium_commissioner_holder  var:qing_opium_commissioner_holder = { is_alive = no } }
  ```
  This only fires when the holder var EXISTS and is dead — unlike Salt's own backfill
  (`se_QING_SALT.txt:208-213`), which uses `OR = { NOT = { has_variable = ... } var:... = { is_alive
  = no } } }`. After the double-book relief above runs `remove_variable =
  qing_opium_commissioner_holder`, the holder var no longer EXISTS, so Opium's existing backfill's
  `has_variable` clause fails and the office goes vacant with no re-check anywhere else — not "one
  extra quarter" as the removed claim said, but PERMANENTLY, since neither player lever can recover
  it: the appoint button is gated `NOT has_variable = qing_lin_zexu_appointed` (set once, never
  removed anywhere in the file — confirmed by grep), and the rotate button is gated `has_variable =
  qing_opium_commissioner_holder` (now false). **Fix required at implementation time: Opium's
  EXISTING backfill limit (`:312-322`) must ALSO be edited to add the missing `OR = { NOT = {
  has_variable = qing_opium_commissioner_holder } ... } }` clause, matching Salt's form exactly —
  not left as a pre-existing, out-of-scope function this design only reads from.** This is a
  required edit to EXISTING code, not just new code, and must be logged as part of this task, not
  treated as untouched.
- **Ease on appointment — CORRECTED, round 3 (was H-2's placement, independently re-checked and
  found wrong).** v2/v3 said to add `QING_frontier_office_ease_squeeze` inside
  `QING_opium_commissioner_seat`, citing "the other 3 (and #62's Customs)" as precedent. Round 3
  found BOTH halves of that citation false: (a) grepped `se_QING_CUSTOMS.txt` directly — ZERO
  matches for `QING_frontier_office_ease_squeeze` anywhere; Customs does not use this helper at
  all (#62's own design doesn't add it there either). (b) Salt/Caravan/Canton do NOT call it from
  inside their own analogous `_seat` helpers — `QING_salt_commissioner_seat`, `QING_caravan_
  super_seat`, `QING_canton_seat_hoppo` never call it; it's called from COUNTRY-scope sites AFTER
  seating instead: the rotate actions (`se_QING_SALT.txt:261`, `se_QING_CARAVAN.txt:933`) and the
  frontier-picker's own per-office branches (`se_QING_FRONTIER_PICKER.txt:76/90/104`). Calling it
  from INSIDE `QING_opium_commissioner_seat`, which runs in CHARACTER scope (`this` = the picked
  character), risks exactly the unwrapped-scope bug this same file's own cr97 fix comment warns
  about (`se_QING_OPIUM.txt:334-339`). **Fix: add the ease call to `se_QING_FRONTIER_PICKER.txt`'s
  existing opium branch (`:107-122`) instead**, country-scoped, mirroring the Hoppo branch's own
  placement (`:104`) exactly:
  ```
  # [round-3 fix] se_QING_FRONTIER_PICKER.txt:107-122's opium branch currently has NO squeeze to
  # ease (its own header comment, :107-109, correctly said so as of v0 -- this design makes that
  # comment stale the moment the squeeze meter above ships; strike it and add the ease call,
  # mirroring the Hoppo branch immediately above at :104):
  		scope:qing_frontier_pick = { QING_opium_commissioner_seat = yes }
  		QING_frontier_office_ease_squeeze = { squeeze = qing_opium_commissioner_squeeze  holder = qing_opium_commissioner_holder }
  		LOG_line = { sys = QING  msg = "frontier picker: player seated a new Imperial Commissioner (欽差大臣) for" }
  ```
  This covers the PLAYER-picker seating path.

  **[round-4 fix, HIGH — the auto-pick placement instruction was scope-ambiguous and, read
  literally, wrong.]** v3 said to add the ease call "after the `_seat` call returns, still in
  country scope" inside `QING_opium_commissioner_appoint`. Round 4 found this is ambiguous in
  exactly the way that matters: `QING_opium_commissioner_seat = yes` is written INSIDE an
  `ordered_character` block, and `this` inside that block's body is the CANDIDATE CHARACTER, not
  CHI (confirmed via `QING_frontier_office_refresh_candidates`, `se_QING_FRONTIER_PICKER.txt:
  30-54`, which has to explicitly re-wrap in `ROOT = {...}` to write country-scope state from
  inside the identical `ordered_character` body) — the SAME scope-confusion class the file's own
  cr97 fix comment already warns about for this exact office. Adding the ease call as "the next
  line after the `_seat` call" would place it INSIDE `ordered_character`, evaluating
  `QING_frontier_office_ease_squeeze`'s unwrapped `has_variable = $holder$`/`var:$holder$` reads
  against the candidate character (who has no such variable) — a silent no-op, functionally
  identical to the bug round 3 just fixed for the OLD (inside-`_seat`) placement.

  **[round-5 fix, HIGH — round 4's own placement (top level of `QING_opium_commissioner_appoint`)
  was scope-correct but call-site wrong: that function is SHARED by two different code paths,
  and easing there fires the wrong path.]** `QING_opium_commissioner_appoint` is called from TWO
  places: (1) `QING_opium_appoint_commissioner` (`:387-393`, the ONE-SHOT fresh-appointment guard,
  the only caller round 3/4 actually intended), AND (2) `QING_opium_commissioner_reconcile`'s own
  backfill step (`:319`, confirmed by direct re-read) — which fires on EVERY natural-death backfill
  AND every relief-then-backfill sequence, i.e. exactly the two paths this whole design's mirror
  reorder (fix 1, above) was built to handle correctly. Placing the ease call at
  `QING_opium_commissioner_appoint`'s own top level means it ALSO fires on backfill, immediately
  followed — in the SAME `_reconcile` call — by the (correctly reordered) mirror step, which flatly
  overwrites whatever the ease call just computed. Not a correctness bug (the mirror's value is
  still the design's intended long-term value) but it silently defeats the ease mechanic's whole
  point (a one-quarter "new broom" bridge) for the backfill/relief paths — arguably the MOST common
  real invocations of auto-pick, since the one-shot fresh appointment fires at most once per game.
  Compare the real precedent again: Salt/Caravan/Canton's bare `_appoint`/`_seat` helpers NEVER
  contain the ease call — it lives ONLY in the separate, player-only `_rotate` wrapper
  (`se_QING_SALT.txt:247-264`, `se_QING_CARAVAN.txt:920-937`, `se_QING_CANTON.txt:513-529`), which
  `_reconcile`'s own backfill step never calls. **Fix: move the ease call OUT of
  `QING_opium_commissioner_appoint` (shared, called by backfill) and INTO
  `QING_opium_appoint_commissioner` instead (`:387-393` — the one-shot guard, NEVER called from
  inside `_reconcile`)** — restoring the real precedent's separation exactly:
  ```
  QING_opium_commissioner_appoint = {
  	ordered_character = {
  		limit = { ... }
  		order_by = finesse
  		max = 1
  		QING_opium_commissioner_seat = yes
  	}
  	# [round-5 fix] ease call REMOVED from here — this function is shared by
  	# QING_opium_commissioner_reconcile's own backfill step, which the mirror (fix 1, above)
  	# ALSO runs on, same call; easing here would fire on every backfill and get immediately
  	# overwritten by that mirror, silently defeating the ease mechanic for those paths.
  }

  QING_opium_appoint_commissioner = {
  	QING_opium_init = yes
  	if = {
  		limit = { NOT = { has_variable = qing_lin_zexu_appointed } }
  		QING_opium_commissioner_appoint = yes
  		# [round-5 fix] ease call lives HERE instead -- this wrapper is the one-shot fresh-
  		# appointment guard, called ONLY from qing_opium.1's prohibit option and
  		# QING_opium_crackdown_destroy, NEVER from _reconcile's backfill step -- so there is no
  		# same-call mirror to collide with, matching how Salt/Caravan/Canton confine the ease
  		# call to their own player-only, non-reconcile-routed lever paths.
  		QING_frontier_office_ease_squeeze = { squeeze = qing_opium_commissioner_squeeze  holder = qing_opium_commissioner_holder }
  	}
  }
  ```
- **Revenue-Minister fold**: NOT built in this task, for EITHER the squeeze meter or the new
  `qing_opium_income_last` — matching #59's/#62's own precedent of shipping mechanisms separately
  from wiring them into term (h)/(g). Log as the natural next step once both pieces exist.

## Open questions for round 6

1. **[RESOLVED, round 1]** Full call graph — traced above, no longer approximate.
2. **[RESOLVED, round 1]** Option A's premise holds (appointee-based, not Lin-Zexu-specific), per
   the H2 fix above — confirmed against the mod's own shipped Lin Zexu flavor text and the
   already-existing frontier-picker UI precedent (M2).
3. **[RESOLVED, round 1]** Continuous attenuation formula adopted above, not a cliff.
4. **[RESOLVED, round 3]** Posture=1 recurring revenue's insertion point — pinned since round 2;
   round 3 corrected a citation-drift (`:220`→`:221`) and confirmed `qing_opium_outflow_tmp` (gross
   opium-driven silver drain) is the more defensible revenue base than net flow. The `/5`
   scale-factor remains a plain [ASSUMPTION], boot-tune.
5. **[RESOLVED, round 2]** #62's vacancy-decay fix does NOT apply here — Opium's synchronous
   same-pulse death-backfill differs genuinely from Customs' single-shot appointment path.
6. Confirm no naming collision between `qing_opium_income_last` and any existing var (grep before
   implementation). Still open, carried forward unchanged.
7. **[RESOLVED, round 3]** The double-book guard's OR-set is correct as-is (Opium has no
   office-specific marker to add). The guard's ORDERING relative to backfill required an explicit
   edit to Opium's EXISTING backfill limit (adding Salt's `OR = { NOT = { has_variable = ... } ...
   } }` clause) — fixed, and per round 4 (below) the mirror's own position in the sequence also
   needed correcting.
8. **[RESOLVED, round 4]** Mirror-vs-backfill ordering — round 4 traced the real Salt/Canton/
   Caravan reconciles and found ALL THREE run mirror strictly AFTER backfill, not before (every
   prior draft of this design had it backwards, leaving the squeeze meter stale for a full quarter
   on any backfill event). Fixed: the full corrected sequence above is now (a) relief → (b)
   backfill → (c) mirror, matching the real precedent exactly.
9. **[RESOLVED, round 4]** Auto-pick ease-call scope ambiguity — the "after the `_seat` call
   returns, still in country scope" instruction, read literally, placed the call INSIDE
   `ordered_character`'s body (character scope, `this` = candidate, not CHI) — a silent no-op
   identical in kind to the bug round 3 fixed for the OLD placement. Fixed with an explicit code
   snippet placing the call after `ordered_character`'s closing brace, at the function's own
   (genuinely country-scope) top level.
10. **[RESOLVED, round 5]** Round 5 confirmed the mirror-after-backfill reorder and the
    ease-call-at-top-level placement are each individually correct, but found a NEW interaction:
    the ease call at `QING_opium_commissioner_appoint`'s top level ALSO fires on every backfill
    call (that function is shared by both the one-shot fresh-appoint wrapper AND `_reconcile`'s
    own backfill step), where the immediately-following mirror step overwrites it — silently
    defeating the ease mechanic for the backfill/relief paths. Fixed by moving the ease call OUT
    of the shared function and INTO `QING_opium_appoint_commissioner` (the one-shot wrapper,
    confirmed never called from inside `_reconcile`), restoring Salt/Caravan/Canton's own
    separation (ease calls live only in player-only, non-reconcile-routed paths).
11. **New, round 6**: confirm `QING_opium_appoint_commissioner` is genuinely the right, and ONLY,
    home for the ease call now — re-verify both its callers (`qing_opium.1`'s prohibit option via
    `QING_opium_crackdown_destroy`, and any other direct caller) are one-shot/non-reconcile paths,
    and re-confirm no OTHER function shares `QING_opium_commissioner_appoint` as a callee in a way
    that could reintroduce the same same-call-overwrite hazard this round just fixed.