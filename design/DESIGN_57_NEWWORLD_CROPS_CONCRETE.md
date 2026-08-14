# DESIGN — #57 make the New World crops boom concrete (real goods, real pops, real migration)

> STATUS 2026-08-13: DRAFT v3 — round-2 adversarial review complete. Round 2 independently
> re-derived round 1's fixes (confirmed the farmstead-count/pops-per-tier conflation fix holds,
> confirmed the `migr_gov_push` push-not-pull citation and the `QING_COLON_nwcrop_diffuse`
> citation both check out exactly against source) and found two NEW issues: a HIGH interaction
> bug (the new pulse's `QING_COLON_heartland_push` would be silently wiped almost every quarter by
> an existing guard in `QING_pop_pulse`, se_QING_POPULATION.txt:184-190 — the SAME failure mode
> that guard's own comment says it was already patched once for a different caller) — fixed below
> by having the new pulse set the recognized `qing_migr_crop_boom` modifier so the existing guard
> treats it correctly; and a MEDIUM factual correction (round 1's "~11-province" 1763 baseline was
> WRONG — independently re-counted at exactly 16 provinces across Guangdong/Hunan/Jiangxi/Fujian,
> confirmed by direct grep of `setup/provinces/00_*.txt` — the tier-threshold tuning guidance is
> corrected below to use the real number, which gives a meaningfully tighter runway than round 1's
> undercount implied).
>
> STATUS 2026-08-13: DRAFT v4 — round-3 adversarial review complete. Round 3 independently
> re-verified both v3 fixes hold exactly as intended (the crop-boom-modifier grant does prevent
> the guard from wiping the push; the 16-province count is exact, re-derived from scratch, no
> missed province anywhere) and found one more concrete, scoped gap: granting `qing_migr_crop_
> boom` created a NEW risk — the modifier's only removal path is downstream of an event chain
> that fires at an expected rate of roughly once per 100 years, so in a game where that chain
> never rolls, the modifier becomes permanently stuck with no re-evaluation. Fixed below by
> having the new pulse own its own removal condition (clear the modifier when `farmstead_count`
> drops back below tier-1), rather than depending on a separate, rarely-firing system to clean up
> state it created.
>
> **STATUS 2026-08-14: FINAL v9 — round-7 adversarial review complete, VERDICT: READY FOR
> IMPLEMENTATION.** Round 7 did an exhaustive sweep for the exact recurring failure pattern that
> hit this doc across all 6 prior rounds (a claim fixed at its "headline" location while a stale
> duplicate survives elsewhere) — checked every location touching the compounding/logging/#65-
> precedent topic, every other named fix from all 6 rounds (tier SET-not-increment, "this decade"
> clarification, removal-check ordering, 16-province count, push-not-pull citation), and found
> zero remaining stale duplicates anywhere. Fixed one trivial LOW citation mis-attribution (the
> ~40,000-pop-object figure was attributed to "the ground-truth section," which never states it;
> corrected to its real source, `se_QING_POPULATION.txt:63-64`). No further rounds needed — 7
> rounds, each surfacing a genuine issue in the prior round's fix, now converged to a clean,
> independently-confirmed design.
>
> STATUS 2026-08-14 (superseded, kept for provenance): DRAFT v8 — round-6 adversarial review found a STALE DUPLICATE of round 4's
> already-superseded claim survived in the Open Questions section, contradicting round 5's fix
> sitting one page above it.** This doc's edit passes have repeatedly fixed a claim at its
> "headline" location (Design Goal #4, the inline Q3 block) while an OLDER copy of the same
> resolution kept living on, unedited, in the Open Questions section — this is now the SAME failure
> mode recurring for a second time (round 4→Goal #4 was the first instance). Round 6 found: (1,
> CRITICAL) Open Question 3 still said "the stack is real and likely compounds... matching #65's
> precedent" and "log both the pop count and total_population trend" — VERBATIM the round-4
> overclaim round 5 rejected, sitting unedited one section below the corrected text. Fixed: rewritten
> to explicitly state it MIRRORS Design Goal #4/the inline Q3 block rather than independently
> re-deriving an answer, specifically to stop this duplication pattern from recurring a third time.
> (2, MEDIUM) the population-band logging proposal's suggested default (reuse `QING_pop_
> recompute_target`'s pressure thresholds) was a unit mismatch — those thresholds classify a 0-100
> INDEX, not `total_population`'s five-figure headcount, so the "default" could never actually
> fire. Fixed: replaced with an instruction to build a new small ladder sized to this doc's own
> per-tier pop-injection math, not reuse an incompatible existing one.
>
> STATUS 2026-08-14 (superseded, kept for provenance): DRAFT v7 — round-5 adversarial review found round 4's OWN fix had a subtler
> third layer of overclaim, plus 2 new gaps, all fixed.** Round 5 found: (1, HIGH) round 4's Q3
> fix borrowed MORE certainty from `DESIGN_NWCROP_POPBOOM_65`'s precedent than that precedent
> actually supports — #65's stack is two additive terms of the SAME modifier key (engine-
> guaranteed to sum), while THIS design's claimed interaction (pop-count injection under a growth-
> rate modifier) is a genuinely different, unverified kind of interaction. Fixed: stated honestly
> that whether this interaction compounds is NOT known — only the PRACTICE (size small, verify on
> boot) is borrowed from #65, not its certainty. (2, HIGH) open question 2 (the tier-threshold/
> pop-count magnitude) was never updated to note it now has a SECOND job (bounding the Q3
> interaction, not just the absolute-count runaway it was originally about) — fixed with an
> explicit cross-reference. (3, MEDIUM) "log the pop count and total_population trend" was not
> actually implementable — this engine can't render raw numeric values in logs
> (`design/LOGGING_TEMPLATE.md:37-38`), and no proven trend-logging idiom exists anywhere in this
> codebase. Fixed by replacing it with a concrete, proven band-ladder shape (matching
> `QING_DECLINE_apply_pop_pressure_band`'s exact idiom) — log the tier crossed + the population
> band at that moment, not an invented delta mechanism. (4, MEDIUM) "bump `qing_newworld_pop_
> tier`" was ambiguous about multi-tier jumps in a single pulse (increment-by-1 vs. set-to-current-
> tier) — a bare increment would permanently under-credit skipped tiers given the ratchet's
> one-way design. Fixed: SET to the computed tier level directly, not increment.
>
> STATUS 2026-08-14 (superseded, kept for provenance): DRAFT v6 — round-4 adversarial review found v5's own Q3 "resolution" was
> WRONG and fixed it properly this time.** Round 4 found two real problems with v5's fix: (1,
> CRITICAL) Design Goal #4 (never updated) still said the likely fix was to REPLACE the modifier's
> growth term with the pulse's pop count, directly contradicting v5's "keep both, no interaction"
> resolution elsewhere in the same doc; (2, HIGH) v5's resolution asserted categorical certainty
> about an engine population-growth formula this repo doesn't document anywhere — `#88`'s own
> research already noted this formula "is not instrumented or verified anywhere in this mod" — and
> this project's OWN precedent for the same feature family (`DESIGN_NWCROP_POPBOOM_65`'s capacity-
> term stack) treats an equivalent interaction as REAL and accepted, bounded by sizing the new term
> small and boot-log-verifying it, not argued away by formula reasoning. **Corrected: Q3 (and Goal
> #4) now both say the same thing — the stack between the pulse's flat pop-count injection and the
> modifier's growth-rate term is real and probably compounds, is NOT eliminated, and is bounded by
> keeping `pops_per_tier` small/capped (open question 2) and boot-log-verifying the actual
> population trend, matching this project's own precedent rather than inventing a new "no
> interaction" claim with no engine-formula evidence behind it.** Also fixed a MEDIUM ambiguity
> round 4 found: the "hasn't already created a generation this decade" throttle language could be
> misread as a separate calendar-date check — clarified it IS the tier-count comparison itself
> (`floor(farmstead_count/threshold) > qing_newworld_pop_tier`), no date/timer variable needed.
>
> **STATUS 2026-08-14: DRAFT v5 (SUPERSEDED BY v6 ABOVE) — independent CONFIRMATION-PASS review found round 3's own "ready
> for implementation" self-assessment was WRONG, and fixed below.** Round 3's verdict claimed this
> was ready "not a full round 4," but the doc's own Open Questions section (unedited since round
> 1) explicitly says "do not implement past this point" and Q3 — the doc's OWN "single highest-risk
> unresolved call" — had never actually been resolved by any round. The confirmation pass found and
> fixed 3 concrete issues: **(1, CRITICAL, resolves Q3)** `qing_migr_crop_boom` grants a REAL engine
> `global_population_growth = 0.10` term (`common/modifiers/qing_migration_modifiers.txt:38-42`) —
> a continuous growth-RATE effect — while this design's new pulse ALSO does one-time
> `create_state_pop` injections. These are NOT the same quantity and do not need reconciling
> against each other the way Q3 feared (a rate term and a one-time injection don't "double-count"
> in the sense of reading the same number twice) — but round 3 never stated this explicitly, so the
> doc's own gate was never actually satisfied. Resolved below: state plainly that the modifier's
> growth-RATE term and the pulse's pop-COUNT term are complementary, not competing, and both are
> intentional (the modifier explains WHY growth accelerates in-fiction; the pulse makes the
> population NUMBER concrete) — no term needs capping or removing. **(2, HIGH)** round 3's removal
> fix was ambiguously nested — written as if it were a sub-bullet of the SAME upward tier-crossing
> gate that guards the grant, which by construction never fires on a downward move, reproducing the
> exact stuck-modifier bug round 3 claimed to close. Fixed below by stating the removal check as a
> SEPARATE, unconditional branch evaluated every pulse, independent of the tier-crossing gate — plus
> resolving the un-addressed `qing_newworld_pop_tier` reset question (does NOT reset on removal —
> the pop/tier ratchet is permanent by design, only the flavour modifier is reversible). **(3,
> MEDIUM)** open question 5 still cited the stale "~11-province" figure after round 2 corrected it
> to 16 everywhere else — fixed.

## Task text

User (this session, following #88's fix): "the point of the population boom mechanic was to
mirror history, i.e. New World crops -> increased food production -> pop boom -> pop pressure ->
migration or famine... these New World crops should drive that loop within the game on concrete
terms (real trade goods swapped, real pops created, migrated, etc)."

## Ground truth: what already exists (confirmed by source trace, not assumption)

The crop system is NOT starting from zero. Four real pieces already exist, but they don't chain
into a loop — each is an isolated island the others don't read:

1. **Real trade goods**: `maize`, `sweet_potato`, `potato`, `peanut`, `chili` are genuine trade
   goods (`common/trade_goods/00_imp19c.txt`), priced and traded like any other good.
2. **Real building**: `new_world_farmstead_building` (`common/buildings/00_infrastructure_
   buildings.txt:140-165`) — generic, NO culture gate (deliberately: "Europe, the Americas, and
   the Qing alike ate New World crops"). Effects: `local_population_capacity_modifier=0.05`,
   `local_lower_strata_output=0.1`, `local_monthly_food=0.05`. Player-buildable wherever one of
   the 5 crops is the province's trade good.
3. **Real province modifier**: `qing_nwcrop_abundance` (`common/modifiers/qing_migration_
   modifiers.txt:70-72`) — `local_population_capacity=8`. Auto-applied by
   `QING_COLON_apply_nwcrop_capacity` (`se_QING_COLON.txt:276-325`) to EVERY province worldwide
   growing one of the 5 crops (not gated to CHI — "the lift is a property of the CROP, not the
   polity"). This is a real, continuously-recomputed capacity lift, stacking on top of the
   farmstead building's own capacity term.
4. **Real one-shot pop creation + a real migration lever**: the flavour-roll event chain
   `qing_migration.20/21/22/23` (`events/imp19c_mod_events/qing_frontier_migration_events.txt`)
   fires once (weight-8 roll off `QING_frontier_flavour_roll`, gated on `NOT has_variable
   qing_newworld_crops`), then over its branches: creates 2-3 `freemen` pops directly
   (`create_state_pop = freemen`, on the top provinces by `total_population`, `.20`:180-187/
   203-210 and `.22`:281-287), sets `migr_gov_push` on those same provinces via
   `QING_COLON_heartland_push` (a real read by the generic migration engine's **PUSH**-score
   svalue, `MIGRATION_svalues.txt:135-153` — `MIGRATION_push_province`, NOT the pull svalue;
   `heartland_push`'s own name and its "encourage people to leave" comment already say push, so
   this is a citation correction only, not a mechanism change), and swaps a country modifier
   through 3 states (`qing_migr_crop_boom` -> `_golden` or `qing_migr_overpopulation`, each
   carrying real `global_population_growth`/`local_monthly_food_modifier`/etc. terms).
5. **A second, already-running crop-geography pulse**: `QING_COLON_nwcrop_diffuse` (#384,
   `se_QING_COLON.txt:399-489`), called quarterly from `00_monthly_country.txt:112`, spreads the
   crop GOOD itself (not pops) into new adjacent provinces, capped at a nationwide 3/year, then
   re-runs the capacity sweep. This doesn't create pops, so it doesn't close the gap below — but
   any new production-linked pulse this design adds must be checked against it so the mod doesn't
   end up with two independently-tuned "how fast do New World crops spread/compound" throttles
   that fight each other or double-count the same geographic growth.

## The actual gap (confirmed, not assumed)

None of the above is CONTINUOUS or PRODUCTION-LINKED. Specifically:

- The pop creation (`create_state_pop`) is a ONE-TIME flavour beat tied to the event firing, not
  a function of how much maize/potato/sweet-potato the realm is actually producing. A realm that
  builds 200 farmsteads gets the exact same 2-3 pops as a realm that builds 3 (the mission's own
  `allow` gate only checks `count >= 3`).
  This is the same disconnect the design memory `imp19c-234-pop-rederivation-method`
  established for #234: pop counts should derive from a concrete driver (there, terrain; here,
  food production), not a flat mult/one-shot event.
- `total_population` (the actual headcount the crowding term in `QING_pop_recompute_target`
  reads, `se_QING_POPULATION.txt:85-87`) is otherwise grown ENTIRELY by the engine's native,
  mod-uncontrolled population simulation. The mod's own capacity lifts (building + province
  modifier, both real) raise the CEILING the engine's native growth can climb toward, but nothing
  in mod script converts "this province produces more food" into "this province's pop count goes
  up" on a running basis — that link is left entirely to whatever the engine's native growth
  formula happens to do with a higher capacity number, which #88's own research confirmed is not
  instrumented or verified anywhere in this mod.
- #88 deleted the ONE piece that used to make the mission's OWN reward feed growth at all
  (`qing_newworld_agriculture`'s `global_population_growth`/`global_population_capacity_modifier`
  terms), replacing it with a flat pressure-target discount that has no production link either.
  This was the right call for THAT task (the old modifier was a silent island the pressure meter
  never read), but it leaves the mission with zero growth-side effect today — its only remaining
  lever is subtracting from the PRESSURE side of the loop, never adding to the BOOM side.

In short: the "boom" half of "crops -> boom -> pressure -> migration/famine" is missing a
concrete, scalable driver. The "pressure -> migration/famine" half is real and working (the
crowding term, the granary/frontier relief valves, the sect-pressure/famine-event escalation).
The one-shot event chain (`qing_migration.20-23`) is a flavour vignette sitting ALONGSIDE the
loop, not a mechanism that scales with it.

## Design goals

1. **Production-linked, not event-linked.** The boom's size should track how much New World crop
   the realm actually grows (farmstead building count / trade-good coverage), not a die roll that
   fires once regardless of scale.
2. **Concrete pop creation, not a modifier abstraction.** Where the design calls for "more
   people," prefer an actual `create_state_pop` (or an engine growth-rate term the crowding math
   already reads — `total_population`) over inventing a NEW abstract country-scale number nobody
   else reads. Per `imp19c-concrete-over-abstract-rule`.
3. **Reuse the existing loop, don't build a second one.** `QING_pop_recompute_target`'s crowding
   term already reads `total_population` directly (`/1200`). If real pops get created by crop
   production, the crowding term picks it up for free — no new coupling code needed on that side.
   The existing involution (+18) / golden-relief (-10) / frontier-resettlement (-12) / policy
   (-8/-16) terms in that function are the existing "pressure" vocabulary; a production-linked
   boom just needs to feed `total_population` (via real pop creation) and optionally keep a
   flavour-scale involution/relief term for the "did it resolve well or badly" narrative beat the
   event chain already tells.
4. **Don't double-count — [RESOLVED, round 4/v6, PRECISION-CORRECTED round 5/v7 — the precedent
   citation below claimed more certainty than it actually supports; corrected to state the real,
   weaker epistemic status honestly.]** Round 4 found the v5 draft's Q3 resolution overclaimed
   certainty about an engine growth formula this repo doesn't document anywhere (`#88`'s own
   research already noted the engine's native growth-vs-capacity link "is left entirely to
   whatever the engine's native growth formula happens to do... not instrumented or verified
   anywhere in this mod") — and directly contradicted THIS goal's own "likely replace" language,
   never updated to match. Round 5 found round 4's OWN fix then leaned too hard on
   `design/DESIGN_NWCROP_POPBOOM_65.md`'s precedent to cover this uncertainty: that doc's stack is
   two flat ADDITIVE `local_population_capacity` terms of the SAME modifier key — engine-native
   modifier stacking that is structurally guaranteed to sum, no formula speculation needed. THIS
   design's claimed interaction — a one-time flat pop-COUNT injection under a percentage growth-
   RATE modifier — is a different, genuinely uncertain kind of interaction (compounding depends on
   whether the engine's growth formula is proportional-to-headcount, which is NOT verified
   anywhere). **Stated honestly: it is NOT known whether this interaction compounds at all — only
   that IF it does, the mitigation (small `pops_per_tier`, boot-log observation) is the right
   shape, borrowing #65's PRACTICE (size it small, verify on logs) without borrowing #65's
   CERTAINTY (which came from additive-stacking being structurally guaranteed, not from anything
   this design shares).** The count injection must be sized small (per-tier, capped — see open
   question 2, NOW EXPLICITLY LINKED to this constraint, round-5 fix) and the new pulse's own
   diagnostic logging must confirm the actual observed behavior on a real boot, rather than either
   asserting no interaction (v5's error) or asserting a specific compounding mechanism with
   unwarranted confidence (round 4's own softer version of the same error).
5. **Keep the existing migration lever, extend its trigger.** `QING_COLON_heartland_push` already
   works and is read by the real migration engine (`MIGRATION_svalues.txt`) — a good target for
   "crop boom -> migration," just needs to fire from a production threshold instead of only the
   one-shot event.

## Proposed mechanism (draft — needs review)

Add a periodic (quarterly, piggybacking the existing `QING_GOV_pulse`/pop-pulse cadence, NOT a
new on_action) function, e.g. `QING_pop_newworld_growth_pulse`, scoped to CHI (or generic —
open question below). **Two DISTINCT quantities, deliberately named differently so an
implementer cannot conflate them** (round-1 review found the v1 draft's mechanism text reused a
single variable `N` for both, which would make a tier crossing spawn as many pops as the realm
has TOTAL farmsteads — dozens after decades of diffusion — instead of a small per-tier batch):

- `farmstead_count` — count of owned provinces with `has_building = new_world_farmstead_building`.
  This is the GATE input, read every pulse, never itself the number of pops created.
- `pops_per_tier` — a SEPARATE, small, fixed or capped constant (best-guess, e.g. 1-3; needs
  boot-log tuning per Rule 1a) — the number of pops actually created each time a tier is crossed.
  NEVER derived from `farmstead_count` directly.
- If `farmstead_count` crosses a tier threshold (e.g. every 10 farmsteads owned — see the sanity
  bound below) AND the realm hasn't already created a "New World generation" of pops for THIS
  tier — **[round-4 fix, MEDIUM — clarifying an ambiguity]** "hasn't already... this decade" was
  loose narrative phrasing that could be misread as a SEPARATE calendar-date check (a stored
  timestamp compared against current date + 10 years). It is NOT that. The throttle IS the tier-
  count comparison itself: `floor(farmstead_count / tier_threshold) > qing_newworld_pop_tier` —
  a pure integer comparison against the SAME counter this bullet already creates, no date/timer
  variable needed anywhere. "This decade" was illustrative flavour text for how often a tier is
  EXPECTED to be crossed in practice (per the sanity-bound math below), not a literal mechanism
  requirement — drop the phrase or read it as color commentary only, not a spec:
  - `create_state_pop = freemen`, exactly `pops_per_tier` times, on the `pops_per_tier`
    highest-`total_population` NEW-WORLD-CROP-GROWING provinces specifically (not just
    highest-population provinces generally — ties the pop placement to where the crop is
    actually grown, unlike the current event chain's generic `ordered_owned_province { order_by =
    total_population }`, which doesn't check the province grows a New World crop at all — this is
    itself a small defect in the CURRENT event chain worth fixing regardless of the rest of this
    design; see open question #5).
  - **[round-5 fix, MEDIUM — "bump the tier counter" was ambiguous about multi-tier jumps]** Set
    `qing_newworld_pop_tier = floor(farmstead_count / tier_threshold)` (SET to the current tier
    level, NOT increment-by-1). If `farmstead_count` crosses more than one tier threshold in a
    single pulse (plausible: several 180-day farmstead builds can complete the same quarter, or
    diffusion + construction line up), a bare "bump by 1" would under-credit the skipped tiers
    FOREVER — the pop/tier ratchet is one-way (see below), so lost credit never recovers on a later
    pulse. Setting directly to the computed tier level, rather than incrementing, means a multi-tier
    jump still only grants ONE `pops_per_tier` batch for that pulse (this remains a deliberate,
    accepted simplification — a realm that leaps 2 tiers in one quarter gets 1 tier's worth of pops,
    not 2 — but the TIER COUNTER itself is no longer permanently wrong afterward, which is the part
    that actually matters for the removal-check's `< tier-1` comparison later).
  - `QING_COLON_heartland_push` on those same provinces (reuses the existing, working migration
    push lever).
  - **[Round-2 review fix, HIGH]** Also `add_country_modifier = { name = qing_migr_crop_boom
    duration = -1 }` if not already present. WITHOUT this, the push set above is at real risk of
    being silently erased almost immediately: `QING_pop_pulse` (`se_QING_POPULATION.txt:184-190`,
    already wired into the SAME `QING_GOV_pulse` cadence this new function piggybacks on) contains
    an `else_if` that calls `QING_COLON_clear_heartland_push` — which strips `migr_gov_push` from
    EVERY owned province — whenever `qing_pop_pressure < 35 AND NOR = { has_country_modifier =
    qing_migr_crop_boom, has_country_modifier = qing_migr_overpopulation }`. That guard's own
    comment documents this EXACT failure mode already being hit once for the event chain's own
    push calls ("without this guard the quarterly clear wiped the boom's push within one
    quarter"). The new pulse's push is invisible to that guard unless it also sets one of the two
    recognized modifiers — so it must, or its migration lever will be silently inert whenever
    pressure happens to be under 35 (a common early/mid-game state). Granting the neutral
    `qing_migr_crop_boom` (not `_golden` or `_overpopulation` — this is a production-linked boom,
    not an event-chain resolution) is the correct choice: it's the SAME modifier the event chain's
    own neutral-boom branch grants, so this doesn't invent a fourth state, just lets the two boom
    sources share the one modifier that already protects the push lever.
- **[Round-3 fix, CORRECTED round-4/v5 — the removal check's PLACEMENT was ambiguous and, read
  literally, non-functional.]** Round 3 found `qing_migr_crop_boom`'s only removal path
  (`qing_migration.22`:263, `.23`:307) fires from an ~0.25%/quarter weighted roll — an expected
  ~100-YEAR wait — so if the new pulse is the only system that ever GRANTS the modifier, it
  becomes a PERMANENT fixture with no re-evaluation once the realm drops below tier-1 (buildings
  sacked, land lost). Round 3's own fix text nested the removal check as if it were a sub-bullet
  of the SAME upward tier-crossing gate that guards the grant — but that gate, by construction,
  only evaluates true on an UPWARD crossing; nesting removal inside it means removal can
  structurally never fire on a downward move, reproducing the exact stuck-modifier bug this fix
  claims to close. **Corrected: the removal check is a SEPARATE, unconditional branch, evaluated
  every pulse independent of the tier-crossing gate**, not a bullet under it:
  ```
  # (evaluated every pulse, unconditionally — NOT nested under the tier-crossing gate above)
  if = {
  	limit = { has_country_modifier = qing_migr_crop_boom  var:farmstead_count < TIER_1_THRESHOLD }
  	remove_country_modifier = qing_migr_crop_boom
  }
  ```
  The `has_country_modifier` guard matches this codebase's own idempotency convention for
  unconditional-removal sites (`se_INCOME.txt:396-409`, `se_QING_HOUSEHOLD.txt:342`) rather than a
  bare unguarded `remove_country_modifier` call, which — per `design/DESIGN_UPSTREAM_BUGS.md`
  finding U2 — produces harmless but avoidable "Cannot find X in Modifier database" log noise when
  the modifier is already absent. If the event chain's OWN `.22`/`.23` removal fires first for
  unrelated reasons, the guard here is already false and this check is a clean no-op — no
  double-removal hazard.

  **[New, v5 — the un-addressed `qing_newworld_pop_tier` reset question.]** Removing the modifier
  does NOT reset `qing_newworld_pop_tier`. The pop/tier ratchet is a PERMANENT, one-way counter by
  design (matching how the doc frames `pops_per_tier` creation as a one-time historical event, not
  a reversible resource) — only the flavour modifier (`qing_migr_crop_boom`, representing the
  CURRENT state of the boom) is reversible. This means a realm that reaches tier 2, loses land
  (drops below tier-1, modifier removed), then rebuilds only back to tier-1 will NOT re-earn a
  second tier-1 pop batch or re-grant the modifier at that exact threshold a second time — the
  tier-crossing gate's own "hasn't already created a generation this decade" check is about
  cadence within a climb, not about re-arming a fallen tier. This is an intentional, stated
  asymmetry (population creation is a one-shot historical event; the boom-modifier flavour is a
  live read of current conditions), not an oversight — but it was never stated anywhere before this
  fix, and an implementer needs to know it's deliberate, not a bug to "fix" by resetting the tier
  counter on removal.

  **[Q3, RESOLVED, round 4/v6 — CORRECTED, v5's "no interaction exists" claim was itself the
  bug.]** Does the new pulse's `create_state_pop` "double-count" against `qing_migr_crop_boom`'s
  `global_population_growth = 0.10` term (`common/modifiers/qing_migration_modifiers.txt:38-42`)?
  v5 answered "no, they're different kinds of quantity that never interact" — round 4 correctly
  rejected this: it asserted certainty about an engine growth formula this repo doesn't document
  anywhere (see Design Goal #4, corrected above, for the full reasoning) and directly contradicted
  Goal #4's own un-updated "likely replace" language.

  **[round-5 fix — round 4's OWN fix over-borrowed certainty from a precedent that doesn't
  actually cover this case; corrected honestly.]** `DESIGN_NWCROP_POPBOOM_65`'s stack is two flat
  ADDITIVE terms of the SAME modifier key (engine-native, structurally guaranteed to sum — no
  formula uncertainty). This design's claimed interaction (a one-time pop-COUNT injection under a
  percentage growth-RATE modifier) is NOT the same shape — whether it compounds depends on an
  engine growth formula that is genuinely unverified anywhere in this repo. **The honest position:
  it is not known whether this specific interaction compounds. What IS known and adopted from
  #65's precedent is the PRACTICE, not a borrowed certainty — size the new term small and verify
  on a real boot, rather than asserting a mechanism either way.** `pops_per_tier` must be sized
  small and capped (see open question 2, NOW explicitly tied to this constraint) specifically so
  that WHICHEVER way the formula actually behaves, the realm can't run away.

  **Diagnostic logging, made concrete (round-5 fix — "log the trend" was not implementable as
  stated).** This engine's `debug_log`/`LOG_line` cannot render raw numeric values
  (`design/LOGGING_TEMPLATE.md:37-38`) — only a sentinel-guarded BAND LADDER is proven to work
  (the exact idiom `QING_DECLINE_apply_pop_pressure_band`, `se_QING_DECLINE.txt:330-340`, already
  uses: `remove_country_modifier` both bands, then `if`/`else_if` against literal thresholds, one
  static `LOG_line` string per band). No existing precedent in this codebase logs a TREND (a
  delta across pulses) — every existing precedent logs a snapshot band of a live level. Rather
  than invent an unproven trend-logging idiom, the new pulse's own diagnostic should follow the
  SAME proven snapshot-band shape: log which tier was just crossed (a literal string per tier,
  e.g. "New World pop tier 1/2/3 reached for") at the moment of each grant, and separately log
  `total_population`'s CURRENT band. **[round-6 fix, MEDIUM — the "reuse `QING_pop_recompute_
  target`'s thresholds" default was a unit mismatch, not a real option.]** Those thresholds
  (45/75/etc.) classify `qing_pop_pressure`, a derived 0-100 INDEX — not `total_population`, a raw
  headcount `se_QING_POPULATION.txt:63-64`'s own comment states is ~40,000 pop objects at the
  1763 start (round-7 citation fix — previously mis-attributed to "the doc's own ground-truth
  section," which never states this figure).
  Literal 0-100-scale thresholds would never cross against a five-figure headcount; this was not a
  real fallback, it was a wrong default with a vague escape hatch. **Corrected: build a NEW small
  ladder specifically for `total_population`, sized to this doc's own already-established
  16-province/tier-threshold math** (e.g. bands at rough multiples of the per-tier pop injection
  size, so each band boundary means something concrete like "one tier's worth of pops past the
  last band" — exact thresholds are [ASSUMPTION], boot-tune per Rule 1a, same as `pops_per_tier`
  itself) — giving a real boot log two aligned snapshots per crossing (tier reached + population
  band at that moment) that a human reader can compare across quarters to see whether growth
  accelerated, without requiring this design to build a new persisted-delta mechanism with no
  proven precedent, and without silently shipping a threshold ladder that can never fire.
- Retire (or fold into this) the flat one-shot `create_state_pop` calls inside
  `qing_migration.20`/`.22` — the event chain becomes the NARRATIVE wrapper (the golden/Malthusian
  branch still decides whether the boom is a blessing or a crisis, still swaps the country
  modifier for its growth-RATE flavour), while the concrete pop count is now driven by the
  production-linked pulse instead of the event's own one-shot spawn.

**Tier-threshold sanity bound (round-2 review CORRECTION — round 1's ~11 figure was wrong, verified
by direct grep, not estimated):** at the 1763 CHI start, exactly **16** provinces already grow a
New World crop and are therefore eligible to build the farmstead — 4 in Guangdong (1 sweet_potato +
3 peanut), 7 in Hunan (4 maize + 3 chili), 2 in Jiangxi (maize), 3 in Fujian (sweet_potato), all
CHI-owned, confirmed via direct grep of `setup/provinces/00_Guangdong.txt`/`00_Hunan.txt`/
`00_Jiangxi.txt`/`00_Fujian.txt` (no other candidate region — Guangxi/Sichuan_Kham/Guizhou/Yunnan —
has any). This is a MEANINGFULLY TIGHTER margin than round 1's undercount implied: a "tier every
10 farmsteads" reaches its first crossing from starting geography ALONE (16 > 10), and the SECOND
tier (20) needs only 4 more crop-provinces — reachable via `QING_COLON_nwcrop_diffuse`'s own
throttle (max +3 crop-provinces/year) in under 2 years, not "a few decades" as round 1 implied.
Partially offsetting this: the farmstead itself still costs `60 treasury / 180 days` to build
(`common/buildings/00_infrastructure_buildings.txt:140-165`), which is a real, if soft, brake on
how fast `farmstead_count` can climb even once eligible provinces exist. Tune the threshold
against the real 16-province baseline and this construction-cost brake together, not the
originally-assumed ~11.

## Open questions for round 4

1. **Scope: CHI-only or generic?** The farmstead building is deliberately generic (any country).
   Should the production-linked growth pulse also be generic, or stay a CHI-only flavour system
   (matching the rest of `se_QING_POPULATION.txt`'s CHI-only pressure meter)? If generic, this
   becomes a much bigger task (touching non-Qing AI countries' pop growth) — likely OUT of this
   task's scope; recommend CHI-only for v1, log the generic case as a follow-up if wanted. Still
   open — not touched by the v5 confirmation-pass fixes.
2. **Tier threshold and pop count per tier** — pure best-guess, needs boot-log tuning per Rule 1a.
   Proposed starting point: 1 pop per 10 farmsteads, capped at some max tier count so a maxed-out
   realm doesn't create hundreds of pops in one go. NEEDS an explicit cap decision + log line.
   **[round-5 fix — this cap now has a SECOND, previously-unstated job.]** `pops_per_tier`'s
   magnitude is no longer sized against ONE failure mode (a maxed realm creating hundreds of pops
   in a single go) — per Design Goal #4/Q3's corrected resolution above, it must ALSO be small
   enough to keep the pop-count/growth-rate interaction bounded, whichever way the (unverified)
   engine growth formula actually behaves. Whoever picks the actual constant at implementation
   time must size it against BOTH constraints together, not just the absolute-count one this
   question originally named — and the boot-log tuning pass (per the diagnostic logging fix above)
   is how both get checked at once. Still open otherwise — not resolved to an actual number by
   this round.
3. **[RESOLVED, round 6/v8 — this entry was a STALE round-4-era duplicate that survived round 5's
   fix elsewhere and still contradicted it; now reconciled.]** Does this replace or stack with the
   event chain's `global_population_growth` modifier terms? v5 claimed "no interaction, case
   closed" (wrong, per round 4). Round 4 then claimed "the stack is real and likely compounds,
   matching #65's precedent" (ALSO wrong, per round 5 — #65's stack is two additive terms of the
   SAME modifier key, structurally guaranteed to sum; this design's claimed interaction is a
   different, genuinely unverified kind, and no engine growth formula anywhere in this repo
   confirms it compounds at all). **Honest answer, matching Design Goal #4 and the inline Q3 block
   above (this entry must never again drift from those two — it restates them, it does not
   independently re-derive them): it is NOT KNOWN whether this interaction compounds. Only the
   PRACTICE (size `pops_per_tier` small and capped, per open question 2; verify on a real boot) is
   borrowed from #65's precedent, not its certainty.** The diagnostic logging for this is the
   tier-crossed + population-band snapshot shape specified in the mechanism section above (NOT "log
   the pop count and total_population trend" — that phrasing is retired; this engine cannot render
   raw numeric values in logs, per `design/LOGGING_TEMPLATE.md:37-38`, and no trend-logging idiom
   exists anywhere in this codebase).
4. **Should famine (the OTHER branch of "migration or famine") also get a concrete counterpart?**
   Currently famine is `qing_pop_pressure >= 60` + thin granary -> event + `QING_DECLINE_nudge`
   on pressure/sect (no concrete pop LOSS). If "concrete terms" should extend to famine too, that
   needs a `kill_pop` / population-loss mechanism, which is a bigger and riskier addition (real
   pop death) than anything else in this draft — flag for explicit user/review sign-off before
   building, not a default-yes. Still open — not touched by the v5 confirmation-pass fixes.
5. Should the "grows a New World crop" province filter be added to the EXISTING event chain's
   `create_state_pop` picker regardless of whether the rest of this design ships? Cheap and
   directionally correct, but NOT fully independent as originally claimed (round-1 review
   correction): the current code has NO crop filter anywhere in this path, including the OUTER
   `any_owned_province` guard, not just the inner `ordered_owned_province` iterator. Adding the
   filter only to the inner iterator without also updating the outer guard would let a realm with
   zero currently-crop-growing provinces silently create 0 pops on `on_completion` — a quiet
   reward no-op rather than an error. **[Fixed, v5 — stale count corrected]** was citing round 1's
   superseded "~11-province" figure; corrected to the real, round-2-verified 16-province baseline
   (still low risk in practice, the number just needed to match the rest of the doc). The fix must
   touch BOTH the outer guard and the inner iterator, not just the iterator. Still open otherwise —
   not built.
6. **New, v5**: confirm the `qing_newworld_pop_tier` no-reset-on-removal policy (stated explicitly
   above for the first time) is the right call, or whether a realm that falls and rebuilds should
   be able to re-earn a tier's pop batch — this is a genuine design choice this draft is now making
   explicitly rather than leaving implicit.
