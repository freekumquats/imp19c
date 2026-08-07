# DESIGN — Concretize `qing_banner_decay` / `qing_greenstandard_decay` from garrison-commander corruption + low martial (八旗/綠營廢弛)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI. #91 item G — **redesigned** after the
building-count approach was REJECTED.

## 0. Why the FIRST design was rejected, why the SECOND stalled, and why THIS one works
The original "decay = inverse of garrison-building count" was rejected: garrison buildings are never removed
(monotonic count), so an inverse-of-count meter can't climb — it'd flatline near 0 and kill the decline arc.

The second draft (a corruption+martial *drift target*) drew a CRITICAL review finding: with equal weighting
×1 and BASELINE_MARTIAL 7, the target computed to ~6 — **far below the 30/60 bands the decline arc needs**,
and, fighting the still-live `+1` passive creep, it *dragged decay back down* → the SAME flatline that killed
the building-count version, through a different door.

**User ruling (2026-08-06): garrison-commander rot IS the decay — rework the METER'S MATH around it, don't
bolt it on.** So (a) the passive `+1` creep is DELETED — commander rot is the sole driver, not an accelerant
on a separate creep; and (b) the target is RESCALED so the commander stats span the full 0–100 band. This is
just arithmetic: pick the scaler + martial line so a healthy High-Qing corps reproduces the 10/15 seeds and a
rotten late-Qing corps crosses 60. 廢弛 = rot-IN-PLACE: intact garrisons, hollow leadership (corrupt AND
incompetent commanders). The referent is the **legion commander's `corruption` and `martial`**, both of which
genuinely VARY. The garrison commander IS the legion commander (garrison legions are explicitly named, e.g.
"Xi'an Banner Garrison 西安駐防"); no character on the garrison BUILDING (finding #3).

## 1. Thesis — the meter's target IS the (rescaled) commander-rot function, per force
Add a second dedicated `every_unit` walk in the DECLINE pulse (NOT a fold into the council walk — §2 caveat 4)
that averages commander `corruption` ↑ and `martial` ↓, SPLIT banner vs green-standard, and maps them onto
the 0–100 decay band:

```
decay_target(force) = base_force + K × ( avg_commander_corruption(force) + ( M0 − avg_commander_martial(force) ) )
# clamped 0..100. Drift the live meter ±2/pulse toward this (the existing meter idiom). NO passive creep.
```

**CALIBRATION (the arithmetic the review demanded — reaches the band by construction).** Preserves the user's
EQUAL weighting (corruption ×1, martial-gap ×1) and ±2 drift; the fix was the missing SCALER K and a corrected
martial line M0. Constants (PLACEHOLDER-playtest, but chosen to satisfy both anchors):
- **K = 2** (scaler), **M0 = 10** (the "competent officer" martial line — a garrison commander at martial 10
  contributes zero rot; below it adds, above it subtracts. NOTE: NOT the council walk's 7, which is a
  different deviation baseline for a different meter — do not conflate).
- **base_banner = 0, base_gs = 5** (per-force offset — reproduces the historical banner<GS early softness via
  the seed gap, so a similar officer corps still opens 10 vs 15).
- **Healthy 1763 corps** (avg_corr ≈ 4, avg_mart ≈ 9): banner `0 + 2×(4 + (10−9)) = 10` ✓; GS `5 + 2×5 = 15` ✓
  — reproduces the seeds.
- **Rotten late-Qing corps** (avg_corr ≈ 25, avg_mart ≈ 3): banner `0 + 2×(25 + 7) = 64` ✓ (crosses the 60
  severe band); GS `5 + 64 = 69` ✓.
So the arc's 30 (mild) and 60 (severe) bands are REACHABLE (not guaranteed — USER ruling (b), §6): the scaler
maps a genuinely-rotten corps (avg corruption ~25-28) past 60, but reaching that corruption depends on real
events/traits corrupting officers, NOT an assumed climb. A clean corps stays low — intended. Show this
arithmetic in the build commit; tune K/M0/base only if playtest stats diverge from the ~4/9 healthy and
~25/3 rotten assumptions. NOTE (§6): the setup seeds 0 commander corruption, so at a High-Qing start the
derive is gated off (`qing_high_qing_era`) and the meter holds the 10/15 seeds until ~1775 anyway.

## 2. ⚠️ VERIFIED PRIMITIVES + the 3 caveats (do NOT deviate — findings)
1. **SPLIT idiom — `sub_unit_type` is sub_unit-scope ONLY (finding #1).** `every_unit { limit = {
   sub_unit_type = X } }` is WRONG. Correct:
   ```
   every_unit = {
       limit = { has_commander = yes  commander = { is_alive = yes  employer = ROOT }
                 any_sub_unit = { sub_unit_type = qing_eight_banners } }   # GS: qing_green_standard
       commander = { ROOT = { change_variable = { name = qing_banner_officer_corr  add = prev.corruption }
                              change_variable = { name = qing_banner_officer_mart  add = prev.martial }
                              change_variable = { name = qing_banner_officer_n     add = 1 } } }
   }
   ```
   Then average (`divide = ..._n`, guarded `..._n > 0` against /0, mirroring `se_QING_COUNCIL.txt:528`).
   **MIXED-LEGION caveat:** `any_sub_unit` means "unit CONTAINS a banner sub_unit" — a mixed legion counts
   in BOTH banner and GS buckets. Acceptable (a mixed garrison's commander rots both), but DOCUMENT it; do
   not present it as a clean partition.
   **n = 0 IS CORRECT BEHAVIOR (USER 2026-08-06 — not a defect).** If there are no standing banner/GS
   garrison legions, `..._n = 0` and the /0 guard SKIPS the target recompute — the meter simply holds its
   last value that pulse. This is right: no garrisons means no garrison-commanders to rot, so there is
   nothing to measure — there is no "silent freeze" to fix. (An earlier review flagged this as a hole; it
   is not. The setup's standing banner/GS OOB is already proven — no re-proof needed.)
2. **Commander corruption read — PROVEN via `scope:X.corruption`, NOT `prev.corruption` (oracle-checked
   2026-08-06).** `prev.corruption` has 0 hits in either oracle — do NOT use that form. But corruption AS A
   NUMERIC VALUE is attested both ways in both oracles: bare `corruption` inside the char scope
   (Invictus `00_mission_turdetania.txt:135` `add = corruption`; TI/Invictus `impose_fine.txt:66`
   `subtract = corruption`) and scope-prefixed `scope:X.corruption` (`impose_fine.txt:45` `value =
   scope:target.corruption`; `governor_policies/00_default.txt` `value = governor_or_ruler.corruption`).
   **BOTH stats: use `scope:cmd.<stat>`, NOT `prev.<stat>` (oracle-checked 2026-08-06 — see below).**
   ```
   commander = {
       save_scope_as = cmd
       ROOT = { change_variable = { name = qing_banner_officer_corr  add = scope:cmd.corruption }
                change_variable = { name = qing_banner_officer_mart  add = scope:cmd.martial }
                change_variable = { name = qing_banner_officer_n     add = 1 } }
   }
   ```
   ⚠️ **`prev.martial` is NOT oracle-proven either — it is the MOD'S OWN untested convention (~8 in-mod
   uses, ZERO oracle hits), same as `prev.corruption`.** Per the proven-code rule ("proven" = upstream
   only, never mine), do NOT lean on `prev.martial`. Both `scope:X.martial` (Invictus
   `tribal_politics.txt:1331` `add = scope:clan_chief_duel_victim.martial`) and `scope:X.corruption`
   (`impose_fine.txt:45`) ARE upstream-attested, as is bare `martial`/`corruption` inside the char scope
   (TI `00_mission_cyrene.txt:21` `add = martial`). So save-scope + `scope:cmd.<stat>` is the fully-proven
   form for BOTH reads. No isolation build-test needed. Fallback: `has_trait = corrupt` as a +N flag.
3. **Pulse-only `every_unit` (finding #5).** NEVER `every_legion_unit` (crash-class inlined into GUI,
   `se_QING_GUARD.txt:113`), never in a scripted_gui.
   **FOLD INTO THE COUNCIL WALK — this IS fine (USER 2026-08-06).** Add the banner/GS corruption+martial
   accumulation as in-body `if`-buckets inside the EXISTING officer-corps `every_unit` pass
   (`se_QING_COUNCIL.txt:518-548`), so one walk computes council martial AND both decay terms. Two concerns
   an earlier review raised are explicitly NON-ISSUES:
   - **One-quarter-stale is fine.** The council walk runs in `QING_GOV_pulse` (after `QING_DECLINE_pulse`),
     so decay consumers read the previous quarter's average. A quarter of lag on a slow-moving rot meter is
     acceptable — no separate decline-pulse walk needed.
   - **Averaging council martial over ALL commanders (incl. navies) is fine** — the council walk keeps its
     existing all-unit martial average UNCHANGED; the banner/GS buckets are ADDITIONAL in-body `if`
     accumulators (`if = { limit = { any_sub_unit = { sub_unit_type = qing_eight_banners } } ... }`), they
     do NOT narrow the council `limit`. So the council-martial average is untouched; only new buckets are
     added alongside it.

## 3. Consumers (FULL census — line cites CORRECTED per review Finding F)
`QING_mechanics_actions.txt:137/138` (≥40), `se_QING_WAR.txt:78-82` (≥60, commander loyalty collapse),
`se_QING_DECLINE.txt:237/242` (bands ≥60/≥30), `:1032` (sect crosswire, banner ≥70), `:1990` (Nian gate
banner ≥30), `:2141` (decline-incident weight ≥40), `:924` (GS-accel self-gate ≥40),
`QING_army_apply_decay_debuffs` (`se_QING_MECHANICS.txt:424/425`, ≥60 — NOT :413, a comment),
the han_provincial_power blend (`se_QING_DECLINE.txt:424-425`, task #6 — in se_QING_DECLINE, not
se_QING_MECHANICS), reform_pressure sum (`se_QING_DECLINE.txt:353`), the **banner-vs-GS compare
`se_QING_MECHANICS.txt:439`** (`var:qing_banner_decay >= qing_greenstandard_decay_cmpsvalue` — the ONLY
reader of the GS cmpsvalue wrapper; was omitted), the **upkeep-bias `has_variable` reads `:942/943`** (§4b),
GUI (`qing_governance_l_english.yml:384/385` — NOT :378-379). All read the level — keep target+drift so the
level drifts smoothly; the derived value is the TARGET.

## 4. Interaction / gotchas
- **Twin asymmetry:** only `qing_greenstandard_decay` has a `_cmpsvalue` wrapper (`00_event_values.txt:1878`);
  add `qing_banner_decay_cmpsvalue` if the new code needs a banner RHS-compare. Only banner feeds
  reform_pressure + the sect crosswire — the two are NOT symmetric; handle separately though built together.
- **DELETE the passive `+1` creep (`se_QING_DECLINE.txt:914`).** Commander rot is the SOLE driver now — a
  parallel creep would fight the rescaled target (the second-draft flatline). The `NOT qing_fully_modernized`
  AND `NOT qing_high_qing_era` gate that wrapped the creep (`:909-914`) moves onto the DERIVE instead — else
  the self-strengthening capstone's hard-set-to-5 gets overwritten and the zenith wouldn't open calm.
- **CONVERT the levers to move COMMANDER STATS, not the abstract counter (USER 2026-08-06 — concrete &
  correct).** Today drill (−20), sanction (−8), Napoleon (−20) nudge the abstract `qing_banner_decay`
  counter. Under this design that is backwards: the meter is now DERIVED from commander corruption/martial,
  so a lever that touches only the counter would be immediately overwritten by the next rot recompute (the
  "transient blip" the review flagged). **Fix: the levers act on the real garrison commanders** — a drilling
  reform lowers their `corruption` and/or raises `martial`; a purge removes `corrupt`-trait officers. The
  meter then FALLS on its own next pulse because the underlying corps genuinely improved. This is the
  concrete-over-abstract rule applied to the levers themselves, not just the meter:
  ```
  # drill example — reach the banner/GS garrison commanders and improve them:
  every_unit = {
      limit = { has_commander = yes  any_sub_unit = { sub_unit_type = qing_eight_banners } }
      commander = { add_corruption = -0.1  add_martial = 1 }   # verify add_corruption/add_martial proven
  }
  ```
  **`add_corruption` / `add_martial` are PROVEN upstream (oracle-checked 2026-08-06)** — attested as
  character-scope effects across Invictus: `create_mercenary.txt:92` (`add_martial = -5`),
  `00_martial_inventions.txt:587` (`add_martial = 8`), `02_parthia_missions.txt` (multiple), and
  `00_event_effects_inv_1_0.txt:530` (`add_corruption = corruption_medium`). Also used in-mod
  (`00_ambitions.txt`). So the lever rework rests on proven code; no new capability to confirm. Trait ops
  (`remove_trait = corrupt`) remain a coherent alternative for a purge-type lever.
  ⚠️ **Magnitude accounts for the ×K rescale:** the derive multiplies the corruption+martial-gap by K=2
  (§1), so a lever that lowers avg corruption by 5 pulls the target down ~10. Tune the per-commander
  stat deltas so the through-the-derive drop approximates the old −20/−8 counter step (e.g. a drill lowering
  avg corruption ~10 / raising avg martial ~2 → target −24, ≈ the old −20). Confirm the delta lands after
  the ×K, not before.
- **1763 opening:** a healthy High-Qing officer corps (low corruption, decent martial) → target near the
  seeds 10/15. Banner historically softer than GS early — reproduce via the baseline/weight (verify the
  derived split opens banner-vs-GS in the right order, since it now depends on real commander stats, not the
  seed constants).
- Both meters need the sanction path checked: `QING_sanction_regional_army` raises a `qing_yongying` legion
  (not banner/GS) and cuts decay −8/−8 — under the derive, yongying commanders are NOT in the banner/GS
  buckets, so the −8/−8 stays a pure nudge (fine).

## 5. Build checklist (ONE commit — banner+GS together, they share the walk)
1. Add banner/GS buckets as in-body `if`-accumulators inside the EXISTING officer-corps `every_unit` walk
   (`se_QING_COUNCIL.txt:518-548`) — fold, do NOT add a second walk (caveat #3, USER: one-quarter-stale +
   all-commander council avg are both fine). Bucket via `any_sub_unit = { sub_unit_type = qing_eight_banners
   / qing_green_standard }` (caveat #1); read via `commander = { save_scope_as = cmd ... add =
   scope:cmd.corruption / scope:cmd.martial }` (caveat #2 — NOT `prev.` forms, mod-only/unproven); average
   with /0 guards. **n=0 → skip recompute, meter holds (caveat #1 — correct, not a freeze).**
2. `qing_banner_decay_target` / `_greenstandard_decay_target` = `base_force + K × (avg_corr + (M0 −
   avg_mart))`; **pin K=2, M0=10, base_banner=0, base_gs=5** — reproduces seeds 10/15 at a healthy corps AND
   crosses 60 at a rotten one (§1 arithmetic; PLACEHOLDER-playtest comment).
3. **DELETE the passive `+1` creep (`se_QING_DECLINE.txt:914`)** — rot is the sole driver. Drift the live
   counters ±2/pulse toward the targets; move the `NOT fully_modernized AND NOT high_qing_era` gate onto the
   derive (§4).
4. **CONVERT the drill/sanction/Napoleon levers to move COMMANDER STATS** (`add_corruption`/`add_martial` on
   the banner/GS garrison commanders — §4, ruling 4), NOT to nudge the counter. ⚠️ A counter nudge would be
   washed out by the ±2 drift toward the rot target (the "transient blip" §4 rejects) — do NOT "keep the
   nudge levers." (This corrects the earlier contradictory wording.) add `qing_banner_decay_cmpsvalue` if
   a banner RHS-compare is needed.
4b. ⚠️ **RE-ROUTE the per-pulse law-upkeep-bias writer (`se_QING_DECLINE.txt:940-943`) onto the TARGET, not
   the counter (review Finding C).** `QING_DECLINE_nudge amount = var:qing_banner_upkeep_bias` (+ the GS twin)
   runs EVERY pulse; under target+drift a per-pulse counter nudge washes out — re-creating the exact
   "dead-law" flaw (#32) this writer was hoisted to fix. It must ADD its bias to `qing_banner_decay_target`
   (a standing law effect biases the steady state), not step the counter. Same for any other STANDING
   per-pulse writer; one-shot event shocks (rebellion/office/canal/war/migration +8 bumps) may stay as
   transient counter nudges — but STATE that they're transient, don't claim they "step and hold."
5. Verify FULL consumer census unchanged; 1763 opens ~10/15 with correct banner<GS ordering; rotten corps
   crosses 60 (show arithmetic — SUBJECT TO Finding A, §6); mixed-legion double-bucket documented; creep deleted.
6. Review gates: split via any_sub_unit (NOT bare sub_unit_type); corruption/martial via scope:cmd.<stat>
   (NOT prev.); folded into council walk (one-quarter-stale OK per USER); K/M0/base reach the band (§1);
   creep `:914` deleted; fully_modernized/high_qing_era gate on derive; twin asymmetry; consumers unchanged
   (corrected cites §3); upkeep-bias re-routed to target (§4b); RHS-cmpsvalue; 1763 ordering; brace/quote/BOM;
   boot-crash review.

## 6. ⚠️ OPEN DESIGN QUESTION — Finding A: what makes commander corruption CLIMB? (needs a ruling)
The re-review confirmed the 4 rulings are correctly implemented and the arithmetic is internally sound —
BUT flagged the load-bearing empirical gap: **with the `+1` creep deleted, nothing in the current code makes
garrison-commander corruption rise over time.** Verified: setup seeds **0 corruption** for all Qing
characters; corruption climbs ONLY via `corrupt`/`crafty` traits or specific event/ambition modifiers; and
there is **no passive martial-decay** mechanic at all (martial only moves via the levers, which raise it).
So the martial-gap term `(M0 − avg_mart)` sits near-constant ~2 (median effective martial ~8), contributing
little; reaching the ≥60 severe band needs avg corruption ~28, and the sect crosswire (≥70) needs ~33.
**If the officer corps never organically accrues that corruption, the target holds low and the decline arc's
≥30/≥60 consumers never fire — the flatline, through a new door.**

This was a DESIGN call, not a plan fix. **USER RULING 2026-08-06: option (b) — accept a quieter meter. NO
artificial driver.** Decay climbs ONLY when events/traits genuinely make specific officers corrupt (or drop
their martial); a Qing that keeps a clean officer corps stays militarily sound and its banner/GS decay stays
low. This is the PUREST concrete-over-abstract form: the meter reflects real character state and nothing
else — no synthetic creep, no forced accrual. Consequences to build to:
- **The ≥30/≥60 bands are reachable but NOT guaranteed.** They fire only if enough banner/GS commanders
  actually become corrupt (via the existing scandal/ambition/trait events, or a passive AI that lets its
  officer corps rot). A well-managed or lucky Qing may never hit `severe` — that is intended. The §1
  "crosses 60 by construction" framing is REPLACED: 60 is reachable when avg commander corruption ~28, which
  now depends on real events corrupting officers, not an assumed climb.
- **This is a deliberate softening of the decline arc vs today's guaranteed +1 creep.** Downstream consumers
  that assumed decay always trends up (the Nian gate, decline-incident weights, the han_provincial blend)
  will fire LESS often for a well-run Qing. Acceptable per the ruling — decline is now *earned*, not
  automatic. Flag this in the build commit so it isn't mistaken for a broken meter.
- **No new code for a driver in THIS build** — do NOT add the per-pulse `add_corruption` drip or
  trait-stamping. This build ships the PLUMBING only: the derive (§1), the lever conversion (§4), the creep
  deletion (§5.3), the upkeep-bias re-route (§4b). The rot's engine is the pre-existing event/trait
  ecosystem for now.
- ⚠️ **FOLLOW-UP (USER 2026-08-06): a dedicated decay mechanic comes LATER, as its own task.** The user will
  add a specific mechanic that drives banner/GS commander rot (the concrete engine that makes the derived
  target climb). Until then the meter is intentionally quiet for a well-run Qing. When that mechanic lands it
  feeds THIS derive (corrupts real commanders → target rises) — no rework of this plumbing needed, just the
  new driver plugged into the same character stats.
