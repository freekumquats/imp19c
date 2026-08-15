# DESIGN — #62 build a qing_customs_ig_squeeze meter for the Customs Inspector-General

> STATUS 2026-08-14: FINAL v7 — round-6 confirmation pass complete, VERDICT: READY FOR
> IMPLEMENTATION. Round 6 confirmed round 5's one-line fix (`change_variable` → `set_variable` on
> the count→scratch copy step) landed correctly and surgically in BOTH this doc and DESIGN_59,
> with nothing else disturbed, and did one fresh end-to-end read of both documents turning up no
> new issues after 6 total rounds. Build order: **#59 ships term (h)'s scaffold first** (the
> `qing_min_oversight_drag`/`_count`/`_scratch` machinery for Salt/Canton/Caravan), **then #62
> adds ONE `if` block for Customs** on top — no other cross-doc coordination needed.
>
> STATUS (superseded, kept for provenance): round 5 independently
> re-verified round 4's two fixes (scratch-var-then-divide replacement; the `qing_min_oversight_
> count` cleanup) and confirmed BOTH hold — found an EXTRA, tighter precedent for the divide shape
> (`se_QING_DECLINE.txt:2715-2730`) and an exhaustive zero-hit grep (repo + both oracle repos) for
> the OLD nested-divide form, confirming round 4's rejection was warranted. Round 5 also
> confirmed DESIGN_59's sketch is self-consistent as a standalone 3-office term (works correctly
> even if #62 never ships) and re-verified the Salt/Canton/Caravan "always-filled" wording fix
> against `qing_mechanics_on_actions.txt:257`. Found ONE new HIGH issue that slipped in via round
> 4's OWN replacement text: the count→scratch copy step (`change_variable = { name = ...scratch
> value = var:...count }`) used `change_variable` where every other scratch-reset line in the SAME
> block uses `set_variable` — an exhaustive grep (this repo + Invictus + Terra-Indomita) found
> ZERO precedent anywhere for `change_variable` paired with a bare `value =` key (only `add/
> subtract/multiply/divide/min/max`). Fixed below in both this doc and `DESIGN_59` — a one-line
> swap, not a redesign.
>
> STATUS (superseded, kept for provenance): round 4 hand-verified the
> running-average arithmetic (3-office case exactly unchanged at 3.0/10.0; 4-office max case
> overshoots the -10 rail by only ~2.8%, negligible) and confirmed the corrected line citations
> hold against current source with no drift. Found 2 concrete issues, both fixed below: (1) the
> nested `divide = { value = X  multiply = Y }` syntax in v4's sketch has NO exact byte-identical
> precedent anywhere in this codebase (round 4 grepped exhaustively — the two proven idioms it
> extrapolates from come from different call sites) — replaced with the doubly-proven scratch-
> var-then-divide pattern (`se_QING_MINISTRY.txt:374` precedent). (2) `DESIGN_59`'s own
> implementation sketch still showed the flat `/27` with a prose-only pointer to this doc — an
> implementer who copies #59's sketch verbatim, per round 4's finding, would ship the wrong
> divisor and rework it later. Fixed: #59's sketch itself now carries the `qing_min_oversight_
> count` scaffold directly, so #62's own implementation step is a pure one-`if`-block addition,
> touching neither the seed nor the divide. Also fixed 2 minor gaps: a missing `remove_variable =
> qing_min_oversight_count` (the third transient var was never cleaned up in either doc's sketch)
> and a wording correction ("Salt/Caravan always-filled posts" → all 3 of Salt/Canton/Caravan are
> unconditionally seeded, confirmed via `QING_canton_init`'s unconditional call site) plus a
> mis-attribution (v4 called 37 "round 2's target"; it was round 3's own rejected proposal).
>
> STATUS (superseded, kept for provenance): round 3 confirmed v3's core
> fix (folding the meter into term (h) as a real consumer) is sound in shape, but found: (1) the
> proposed divisor retune (27->37) silently WEAKENS the already-verified-sane 3-office baseline in
> the MORE COMMON case (Customs rarely/never appointed) — at seed baseline, `81/27=3.0` becomes
> `81/37=2.19`, a ~27% reduction that fires even when Customs contributes NOTHING to the sum, with
> no one having decided that tradeoff was acceptable. Fixed below by switching term (h) to a
> RUNNING AVERAGE (`sum / count_of_contributing_offices`) instead of a fixed divisor — this leaves
> the 3-office-only case completely untouched (still sum/3-equivalent-weighted, matching round 2's
> own verified magnitudes exactly) and only engages a 4th term when Customs genuinely contributes.
> (2) DESIGN_62's phrasing implied term (h) already exists as shipped code ("alongside the
> EXISTING... if blocks") when it is still only a sketch in `DESIGN_59`, itself marked
> "READY FOR IMPLEMENTATION" but not yet built (grep-confirmed: zero hits for `qing_min_oversight_
> drag` anywhere in `se_QING_MINISTRY.txt`) — fixed below with an explicit ordering statement:
> **#59 must implement term (h) FIRST** (for Salt/Canton/Caravan); #62 then ADDS the Customs `if`
> block + switches the divisor to the running-average form as part of #62's own implementation,
> not a second independent edit to a not-yet-real function. (3) Stale/self-contradicting line
> citations in step 4 (claimed `ROOT={}` closes at :129; actually closes at :131, matching this
> doc's OWN ground-truth section's citation of `:110-131` two paragraphs earlier) — corrected.

> STATUS (superseded, kept for provenance): v3's fixes — the `save_scope_as` idiom replacing a
> bare, unprecedented attribute read; the explicit vacancy-decay-to-baseline behavior, since "no
> IG seated" is Customs' default and likely-permanent state, not a rare transient; and documenting
> the total absence of any rotate/dismissal lever as an accepted limitation — all independently
> re-verified by round 3 and NOT reopened.

## Task text

Follow-up from #51/#59. Salt, Canton, and Caravan each have a real 0..100 corruption/squeeze
meter for their office-holder, mirrored from the seated officer's own `corruption` character
stat, eased on rotation via a shared helper. Customs has none — this gap was already flagged
once in `design/DESIGN_51_CUSTOMS_REVENUE_PERF_ROLLUP.md` under "Follow-up flagged, not built,"
and is what made #59 explicitly exclude Customs from the new Revenue-Minister oversight-drag
term. This task closes that gap.

## Ground truth (traced this session, not assumed)

`se_QING_CUSTOMS.txt` tracks TWO institutional counters for the office, confirmed by direct read:

- `qing_customs_efficiency` (0..100, seeded 40, `:46`) — "how well-run the service is."
- `qing_customs_foreign_control` (0..100, seeded 0, `:47`) — "degree of foreign management
  (Hart-style)."

Neither is a personal corruption meter. `QING_customs_pulse` (`:173-224`) drifts efficiency
toward a blend of `foreign_control × 2 + qing_bureau_integrity`, ÷3 — an INSTITUTIONAL formula
with no read of the IG's own character stats anywhere. The only place the IG's appointment
matters at all is a ONE-TIME nudge on appointment (`QING_customs_appoint_ig`, `:110-131`): +20
efficiency, +15 foreign control, `add_country_modifier = qing_customs_strong_ig` — flat bonuses
for "a strong IG showed up," never revisited each quarter the way Salt/Canton/Caravan's squeeze
meters are. Confirmed by grep: zero reads of `qing_customs_ig_holder.corruption` anywhere in the
file, and the file's own state-comment block (`:25-29`) lists only the two institutional counters
plus the holder var itself — no squeeze var exists under any name.

### The proven pattern being mirrored (Salt, verified exact)

```
# seed (QING_salt_init):
if = { limit = { NOT = { has_variable = qing_salt_squeeze } }  set_variable = { name = qing_salt_squeeze  value = 30 } }

# mirror (inside the quarterly reconcile, after any siphon/creep effects):
set_variable = { name = qing_salt_squeeze  value = scope:qing_salt_seated.corruption }

# ease on rotation (shared helper, se_QING_DECLINE.txt:2925-2939):
QING_frontier_office_ease_squeeze = { squeeze = qing_salt_squeeze  holder = qing_salt_commissioner_holder }
```

`QING_frontier_office_ease_squeeze` is a parametrized macro (`$squeeze$`/`$holder$`) already built
to take ANY squeeze var + holder var pair — it needs no changes to support Customs, just a call
with the new names.

## Proposed mechanism (revised, round-1 review)

1. **New var**: `qing_customs_ig_squeeze` (0..100).
2. **Seed** in `QING_customs_init` (`:46-47`), same guarded pattern as the other three, same
   baseline value 30 for consistency (round 1's L1 finding: the "not every appointee is honest"
   justification for 30 doesn't currently apply, since Hart is the ONLY appointable IG in this
   codebase today — kept at 30 anyway for consistency with Salt/Canton/Caravan's seed, and because
   it's immediately overwritten by the mirror once Hart is seated):
   ```
   if = { limit = { NOT = { has_variable = qing_customs_ig_squeeze } }  set_variable = { name = qing_customs_ig_squeeze  value = 30 } }
   ```
3. **Mirror** inside `QING_customs_pulse` (`:173-226`), using the PROVEN `save_scope_as` idiom
   (round-1 CRITICAL fix — the bare `holder.corruption` read in v1 had zero precedent anywhere in
   this codebase and risked silently resolving to 0):
   ```
   if = {
   	limit = { has_variable = qing_customs_ig_holder  var:qing_customs_ig_holder = { is_alive = yes } }
   	var:qing_customs_ig_holder = { save_scope_as = qing_customs_ig_seated }
   	set_variable = { name = qing_customs_ig_squeeze  value = scope:qing_customs_ig_seated.corruption }
   }
   else = {
   	# [round-1 H1 fix] "no IG seated" is the DEFAULT state (Hart's appointment is a rare,
   	# possibly-never-firing event gated to 1854+; there is no succession mechanism at all once
   	# he dies) — NOT a rare transient the other 3 offices ever face. Decay toward the
   	# institutional baseline (30) rather than freezing at whatever value the meter last held
   	# (Hart's own corruption, or the seed) for the remainder of the game. Small, slow drift —
   	# matches the "gradual, not instant" character of every other DECLINE-family counter.
   	if = {
   		limit = { var:qing_customs_ig_squeeze > 30 }
   		QING_DECLINE_nudge = { var = qing_customs_ig_squeeze  amount = -2 }
   	}
   	else_if = {
   		limit = { var:qing_customs_ig_squeeze < 30 }
   		QING_DECLINE_nudge = { var = qing_customs_ig_squeeze  amount = 2 }
   	}
   }
   ```
4. **Ease on appointment**, inside `QING_customs_appoint_ig`'s existing `ROOT = { ... }` block
   (`se_QING_CUSTOMS.txt:114-131` — corrected, round 3: v3 miscited the closing brace as line 129;
   it is actually line 131, matching this doc's OWN ground-truth section's `:110-131` citation),
   placed IMMEDIATELY BEFORE that closing brace — i.e., AFTER the existing `QING_customs_build_
   house = yes` line (line 130), still INSIDE `ROOT = {}`. The character-scope effects (`add_
   character_modifier`, `set_variable = qing_customs_ig_marker`) sit at lines 132-133, OUTSIDE
   this block — placing the ease call there instead would silently misresolve `holder =
   qing_customs_ig_holder`, which lives on CHI, not on the character (round 3 independently
   re-verified this scope-safety argument holds against current source):
   ```
   		QING_customs_build_house = yes
   		QING_frontier_office_ease_squeeze = { squeeze = qing_customs_ig_squeeze  holder = qing_customs_ig_holder }
   	}
   ```
   **[round-1 H2, documented limitation]** Unlike Salt/Canton/Caravan, Customs has NO rotate/
   dismissal action anywhere in the repo — this ease call fires exactly ONCE, at Hart's single
   appointment, never again for the rest of the game. Building a Customs IG rotate/dismissal
   action is explicitly OUT OF SCOPE for this task — logged as a natural follow-up. The
   vacancy-decay behavior in step 3 does most of the practical work for this meter across a
   typical playthrough.
5. **Consumer — PULLED INTO SCOPE (round-2 CRITICAL fix; divisor mechanism CORRECTED round 3).**
   Round 2 found the meter, as scoped in v2, had ZERO readers anywhere — a pure write-only
   variable, matching this project's own previously-rejected "inert lever" antipattern
   (2026-08-10, #67). Fixed by adding Customs to `#59`'s term (h) ("SUBORDINATE OVERSIGHT DRAG,"
   `se_QING_MINISTRY.txt`) — Customs needs NO Canton-style asymmetry weight (its foreign-control-
   driven `qing_corruption_level` REDUCTION, `se_QING_CUSTOMS.txt:217-221` — round 3 correction:
   this is a corruption CHECK, lowering the realm counter, not a "leak" raising it; the polarity
   is opposite what v3 said, though the conclusion is unaffected — it's still a DIFFERENT variable
   than the new squeeze meter, unlike Canton's own squeeze-drives-a-leak-directly case), so it
   slots in at the same 1.0x weight as Salt/Caravan.

   **Explicit ordering dependency (round-3 fix — this doc does NOT build term (h) from scratch):**
   `#59` owns building term (h)'s scaffold (the `qing_min_oversight_drag`/`_scratch` variables,
   the Salt/Canton/Caravan `if` blocks, the boot-log band ladder) for the ORIGINAL 3 offices —
   confirmed by grep this round that term (h) does NOT exist yet anywhere in `se_QING_MINISTRY.txt`
   (design/DESIGN_59_REVENUE_SQUEEZE_PENALTY.md is marked ready-for-implementation, not yet
   implemented). **#59 must ship first.** #62's OWN implementation step is then: add ONE more `if`
   block for Customs, AND switch the term's magnitude formula from a fixed divisor to a RUNNING
   AVERAGE (see below) — #62 does not re-implement or duplicate #59's scaffold.

   **Divisor mechanism corrected (round-3 fix, replaces the fixed-divisor plan):** a fixed
   divisor re-tuned for 4 offices (27→37, as v3 proposed) silently weakens the ALREADY-VERIFIED-
   SANE 3-office-only case (round 2's own arithmetic check: seed baseline 81/27=3.0) even when
   Customs contributes NOTHING — at 81/37=2.19, a ~27% reduction that fires in the COMMON case
   (Customs is rarely/never appointed, per this doc's own H1 finding), not just the rare maxed
   case. Fixed by switching to a running average — divide by the COUNT of offices actually
   contributing this pulse, not a fixed constant:
   ```
   set_variable = { name = qing_min_oversight_drag  value = 0 }
   set_variable = { name = qing_min_oversight_count  value = 0 }
   if = { limit = { has_variable = qing_salt_squeeze }
   	set_variable = { name = qing_min_oversight_scratch  value = var:qing_salt_squeeze }
   	change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
   	change_variable = { name = qing_min_oversight_count  add = 1 }
   }
   if = { limit = { has_variable = qing_hoppo_squeeze }
   	set_variable = { name = qing_min_oversight_scratch  value = var:qing_hoppo_squeeze }
   	change_variable = { name = qing_min_oversight_scratch  multiply = 0.7 }
   	change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
   	change_variable = { name = qing_min_oversight_count  add = 1 }
   }
   if = { limit = { has_variable = qing_caravan_super_squeeze }
   	set_variable = { name = qing_min_oversight_scratch  value = var:qing_caravan_super_squeeze }
   	change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
   	change_variable = { name = qing_min_oversight_count  add = 1 }
   }
   if = { limit = { has_variable = qing_customs_ig_squeeze }   # [#62] this task's addition
   	set_variable = { name = qing_min_oversight_scratch  value = var:qing_customs_ig_squeeze }
   	change_variable = { name = qing_min_oversight_drag  subtract = var:qing_min_oversight_scratch }
   	change_variable = { name = qing_min_oversight_count  add = 1 }
   }
   if = { limit = { var:qing_min_oversight_count > 0 }
   	# [round-4 fix] the nested "divide = { value = X  multiply = Y }" form has no exact
   	# byte-identical precedent anywhere in this codebase (round 4 grepped exhaustively — the
   	# divide-with-multiply-secondary-key idiom and the top-level-divide-taking-a-nested-block
   	# idiom are each independently proven, but never combined). Using the doubly-proven
   	# scratch-var-then-divide pattern instead (se_QING_MINISTRY.txt:374 precedent):
   	set_variable = { name = qing_min_oversight_scratch  value = var:qing_min_oversight_count }   # [round-5 fix] was change_variable; zero precedent anywhere for change_variable+value, every sibling reset line here uses set_variable
   	change_variable = { name = qing_min_oversight_scratch  multiply = 9 }
   	change_variable = { name = qing_min_oversight_drag  divide = var:qing_min_oversight_scratch }
   }
   remove_variable = qing_min_oversight_count   # [round-4 fix] third transient var, cleaned up
   						 # like its siblings qing_min_oversight_drag/_scratch
   ```
   With the original 3 offices always present (Salt/Canton/Caravan are ALL unconditionally-seeded,
   always-filled posts — round 4 confirmed `qing_hoppo_squeeze` is seeded unconditionally via
   `QING_canton_init`, `qing_mechanics_on_actions.txt:257`, same as Salt/Caravan; corrected wording,
   was previously mis-stated as "Salt/Caravan" only) and Customs absent (the common case),
   `count=3`, divisor=27 — IDENTICAL to the already-verified magnitude, completely untouched. When
   Customs is ALSO present, `count=4`, divisor=36 (round 4 hand-verified: 370/36=10.28, a ~2.8%
   overshoot of sibling (e)'s -10 rail at the rare all-4-maxed extreme — negligible against a
   100-point meter, not a fresh magnitude decision). **[round-4 correction]** the prior draft
   called 37 "round 2's target" — that number was actually round 3's OWN proposal (the fixed-
   divisor retune round 3 itself rejected in favor of this running average), never something round
   2 set; corrected here, no code impact. [ASSUMPTION] the `×9` scale factor reproduces the
   original `/27` at count=3 exactly (27/3=9) — boot-tune if the 4-office case still feels off
   after this fix.

## What this does NOT do (explicitly out of scope, per #59's own prior scoping)

- Does NOT add a yield-shave/siphon on `qing_customs_income_last` the way Salt/Canton/Caravan's
  squeeze meters shave their own revenue figures — #59's design intentionally treats the NEW
  oversight-drag term as reading squeeze directly without needing a yield-shave precedent first
  (unlike the other 3, which already had one before #59 existed). Adding a yield-shave here would
  be a SEPARATE feature, not required to close #62's stated gap (giving Customs a squeeze meter
  at all). Flag for the review: confirm this scoping boundary is correct, or whether a yield-shave
  should ship in the same pass for consistency with the other 3 offices.
- Does NOT change `qing_customs_efficiency`/`qing_customs_foreign_control`'s own institutional
  drift formula — those stay exactly as they are; the new squeeze meter is an ADDITIONAL,
  independent personal-corruption dimension, not a replacement for the institutional counters.
- **[SUPERSEDED, round 2]** v2 said this task would NOT fold the meter into #59's term (h). Round
  2 found that scoping decision produced an inert, consumer-less meter — fixed by pulling the
  small term (h) addition into THIS task's scope (see mechanism step 5 above). This is now the
  ONE deliberate exception to the "ship the mechanism, wire it separately" precedent #59/#63
  otherwise follow — justified because, unlike Opium (#63), this office has no OTHER plausible
  in-fiction consequence to attach the meter to (no revenue stream to shave, no enforcement-rate
  to attenuate) — term (h) is the only available consumer, so deferring it would ship nothing
  observable at all.

## Open questions for round 6

1. **[RESOLVED, round 1+2]** No-IG-seated behavior (decay to 30) — control flow verified clean,
   convergence arithmetic checked sane. Not re-open.
2. **[RESOLVED, round 1]** Scope-save idiom — byte-for-byte matches Salt/Canton/Caravan.
3. **[RESOLVED, round 1]** Baseline 30 — kept for consistency.
4. **[RESOLVED, round 1+2+3]** `QING_frontier_office_ease_squeeze` call placement — pinned
   explicitly, line citations corrected to match this doc's own ground-truth section; round 4
   re-verified against current source, no drift.
5. **[RESOLVED, round 1]** No-rotate-lever — documented limitation, not built.
6. **[RESOLVED, round 3+4]** Term (h) magnitude mechanism — switched from a fixed re-tuned divisor
   to a running average; round 4 hand-verified the arithmetic (3-office case unchanged, 4-office
   case overshoots the rail by only ~2.8%) and replaced the unverified nested-divide syntax with
   the doubly-proven scratch-var-then-divide idiom.
7. **[RESOLVED, round 3+4]** Ordering dependency — #59 must implement term (h)'s scaffold first;
   #62 adds the Customs `if` block only. Round 4 found the prose-only cross-reference wasn't
   enough (an implementer could still copy #59's own stale sketch) — fixed by updating #59's
   actual code sketch to carry the count scaffold directly, so #62's implementation step is now a
   genuine one-block addition, not a note the implementer has to remember to apply.
8. **[RESOLVED, round 4]** The `×9` scale factor — hand-verified exact at count=3 (27/3=9,
   reproducing the original divisor precisely) and checked at count=4 (36, ~2.8% over the -10
   rail at the rare all-4-maxed extreme, judged negligible). No other reader of a fixed `/27`
   constant exists yet since term (h) itself doesn't exist yet (confirmed by grep, round 3+4).
9. Verify no OTHER consumer of `qing_customs_ig_squeeze` is expected (e.g. GUI/panel exposure,
   matching Salt/Canton/Caravan's squeeze display) — confirm in/out of scope for #62. Still open,
   carried forward unchanged.
10. **[RESOLVED, round 5]** `remove_variable = qing_min_oversight_count` placement and the
    divide's operand — round 5 independently traced both sketches sequentially and confirmed the
    cleanup fires after the count's last read, and the divide correctly targets the scratch var
    (holding count×9), not count directly.
11. **[RESOLVED, round 5 fix]** The count→scratch copy step used `change_variable` where every
    sibling reset line in the same block uses `set_variable` — an exhaustive grep (this repo +
    both oracle repos) found zero precedent for `change_variable` paired with a bare `value =`
    key. Fixed in both this doc and DESIGN_59 (one-line swap to `set_variable`).