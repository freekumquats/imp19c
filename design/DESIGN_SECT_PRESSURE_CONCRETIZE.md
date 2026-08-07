# DESIGN — Concretize `qing_sect_pressure` — ⚠️ RETRACTED 2026-08-06: LEAVE ABSTRACT (no valid referent)

**Branch:** merge-overnight. **Status:** ⚠️ **RETRACTED / WON'T-BUILD.** **Scope:** CHI.
**Part of** the meter-concretization program ([[imp19c-concrete-over-abstract-rule]]).

## ⚠️ RETRACTION (2026-08-06, after 3rd adversarial review + standing "don't-force" rule)
`qing_sect_pressure` has **NO valid concrete on-map referent** — this is the audit's `mandate_strength`/
`wenzhi` category (genuinely abstract, leave alone), NOT a fixable predicate. Confirmed against files:
- **There is NO `white_lotus`/heterodox religion object** anywhere in `common/religions/`. The White Lotus
  has no on-map faith to count.
- The proposed proxy `pure_land_buddhism` is a **mainstream ACCEPTED faith** (`00_vthreereligions.txt:480`,
  `happiness_for_same_religion_modifier = +0.05`; inside `chinese_accepted_religion_trigger`,
  `00_religion_groups.txt:281`) and the dominant religion of ~dozens of core Han provinces at 1763. Keying
  the sect meter on it measures **stable orthodox demography**, and it moves the **WRONG WAY**: missionary
  conversion LOWERS the pure_land count → target FALLS, exactly when sect panic should RISE (opposite the
  intended mission→sect coupling `se_QING_MISSIONARY.txt:235`). Third miss on the religion key.
- The reviewer's alternative "derive from active-rebellion count" is **CIRCULAR** — sect_pressure GATES the
  five heterodox rebellions (White Lotus ≥25 `:1947`, Eight Trigrams ≥30, Nian ≥30, Red Turban ≥30, Taiping
  ≥45); deriving it from the rebellions it triggers is a feedback loop.
- Adding restoring drift toward an inert ~0 target would also SUPPRESS the very rebellion gates the meter
  exists to drive (a balance regression, MEDIUM finding).

**Decision:** leave `qing_sect_pressure` a free-floating event-nudged accumulator (as it is today). It is a
correctly-abstract meter — a valid target needs a concrete referent that VARIES the way the meter should,
and none exists. Per [[imp19c-concrete-over-abstract-rule]] + the standing don't-force rule, this is a
won't-build, not a deferred build. Everything below is the (rejected) prior design, kept for the record.

---

## 0. The problem

`qing_sect_pressure` (0–100, seed 0) is the heterodox-sect / secret-society (White Lotus 白蓮教, Triads)
unrest gauge. Verified: **seed 0 + 57 event nudges, NO derive block** (the only non-seed `set_variable` is
a self-strengthening reset). A pure free-floating accumulator — and it drives real decline (heterodox
rebellion gating, the corruption→famine→sect pathway `se_QING_DECLINE.txt:1024`, mandate erosion).

The user's point: this should be **the result of concrete metrics — Christian missions and pop religions**
— not a hand-nudged number. And the concrete referents already exist; one is computed right next door.

## 1. Thesis — TARGET+DRIFT with a baseline-freeze (mirror ethnic_tension EXACTLY)

⚠️ **Revised after adversarial review** — the first draft got the store model, the heterodox test, and the
mission-friction home wrong. Corrected:

**Use the mod's proven target+drift idiom, NOT base+residual (review M1/M2).** Every sibling meter in this
file (ethnic_tension, civic_identity, reform_pressure) computes a **target** annually, and a live counter
**drifts ±N/quarter toward it** (`QING_DECLINE_drift_ethnic_tension:810-817`, ±3). base+residual would make
the level LURCH once a year and would strand the player's suppression levers (a −25 suppress would only
drain a residual, leaving a high base). Instead: annual scan writes `qing_sect_pressure_target`; quarterly
`QING_DECLINE_drift_sect_pressure` steps the counter toward it. **No separate residual store** — the 57
nudges keep moving the live counter (as today), which then drifts back toward the demographic target.
Suppression levers work (they move the counter; the target governs long-run pull); the self-str hard reset
still works IF the target formula is gated to 0 under `has_variable = qing_fully_modernized` (else it
re-derives back up). ⚠️ NOT `qing_selfstr_progress` (re-review F3) — that's a 0..100 momentum meter that
rises mid-game, so gating on it would zero the target as soon as the player founds their first arsenal;
the actual capstone/reset marker is `qing_fully_modernized = 1` (se_QING_SELFSTR.txt:760, what zeroes the
counter at :764).

**The target is a baseline-FROZEN province tally (review L1) — mirror the STRUCTURE of
`se_QING_DECLINE.txt:563-578` (freeze the base on first scan, move target on DEVIATION), but with sect's
OWN seed constant, NOT ethnic's `+20`.** ⚠️ **`target = 0 + (current − frozen_base)/2`** — sect is seeded 0
(`:80`), whereas ethnic is seeded 20 (`:95`); copying the literal `+20` (re-review F2) would floor sect at
20, contradicting the calm seed-0 opening AND neutering suppression below 20. Use 0 (or a deliberately low
floor).

The sect tally sums (fold into the SAME annual `every_owned_province` loop — one pass, review L3; the
`dejure_culture` loop-limit covers all populated provinces, re-review REFUTED the under-count worry):
- **+ White-Lotus / sectarian provinces — key on the FAITH DIRECTLY, NOT the accepted-religion negation.**
  ⚠️ **My first-review C1 fix was ALSO wrong (re-review F1):** `pure_land_buddhism` — annotated in-code as
  "the Chinese phenomenon arising from the White Lotus Society" (`00_religion_groups.txt:281`) — is INSIDE
  `chinese_accepted_religion_trigger_province`. So negating "accepted" would EXCLUDE the White Lotus and
  instead flag only foreign/frontier faiths (catholic/orthodox/tengri/animism/shiite…) = the ETHNIC-tension
  geography, scoring ~0 during a real White Lotus surge and double-counting ethnic_tension (F4). CORRECT
  test: tally provinces whose `dominant_province_religion = pure_land_buddhism` (the actual White-Lotus key;
  optionally + a sectarian-unrest signal), NOT any negation. This keys the meter to the faith it names.
- **+ religious province-unrest** — high `province_unrest >= 4` in those sectarian provinces (double-weight).
- **− relief:** famine-relief / granary coverage (the `se_QING_DECLINE.txt:1042` pathway) already eases it.

**Mission friction — pick ONE home, don't double-count (review C2).** Mission friction ALREADY reaches
sect_pressure via live nudges: the missionary pulse `se_QING_MISSIONARY.txt:235` (+1/pulse), and the 教案
scare events `:116`/`:128`. And `qing_mission_social_friction` derives partly FROM sect (`:197`, `sect/4`)
then pushes back at `:235` — a two-way loop. So do NOT also fold the mission footprint into the target
(that would count it twice and tighten the loop). DECISION: leave mission friction as the existing nudges
(they move the live counter); the target is DEMOGRAPHIC only (heterodox pops + religious unrest). If the
mission footprint should instead live in the target, then remove the `:235` feedback and the `:197` `sect/4`
term — but the low-churn choice is: target = demographics, mission stays a nudge.

## 2. Writer/consumer census (corrected — review M3)
- **Writers:** 57 sites. UNCHANGED under target+drift — they keep nudging the live counter (§1). Note
  `se_QING_MISSIONARY.txt:235`/`:116`/`:128` are among them and live in scripted_effects, not events/ —
  an events-only grep misses them.
- **Consumers (unchanged — read the level):** the sect band + modifiers (`:187` ≥50), mandate erosion
  (`:1077` ≥50), the 5 rebellion gates (`:1947/1965/1975/1989/2016`), the sect-leader spawn (`:2420` ≥60),
  reaction weight (`:2131`), roster gates, GUI/loc.
- ⚠️ **`qing_reform_pressure` does NOT read sect_pressure** — the doc's earlier claim was wrong (review M3).
  `QING_DECLINE_update_reform_pressure:350-355` averages only corruption + currency_stress + ethnic_tension
  + banner_decay. So this change does NOT touch reform_pressure directly.

## 3. Feasibility / gotchas
- **PERFORMANCE — annual, folded into the existing sweep.** The ethnic sweep runs ANNUALLY by firm user
  decision (`se_QING_DECLINE.txt:465`). Fold the sect tally INTO that SAME `every_owned_province` loop (one
  annual pass computes both tallies). The quarterly `QING_DECLINE_drift_sect_pressure` then steps the live
  counter toward the annual target (±N), so there is NO annual lurch (this is exactly why ethnic uses drift).
- **Loop-limit coverage: FINE (re-review REFUTED the under-count worry).** `se_DEJURE.txt:41-49` sets
  `dejure_culture` on `every_province { is_sea=no  total_population>0 }` with NO culture/religion/owner
  filter — the identical limit the sect fold uses. So every populated sectarian province carries it; no
  under-count, no perf reopening. (Delete the earlier hedge.)
- **Religion key: `dominant_province_religion = pure_land_buddhism` (the White Lotus faith), NOT any
  negation** (re-review F1). The accepted/traditional-religion triggers INCLUDE pure_land_buddhism, so
  their negation excludes the White Lotus and measures foreign/frontier faiths (= ethnic geography). Key on
  the faith directly. Optionally add a sectarian-unrest signal; do NOT use the accepted-negation.
- **Migration:** target+drift means NO residual store — on patch the live counter keeps its value and just
  starts drifting toward the new demographic target. No seed-split needed.
- **Self-str reset:** `se_QING_SELFSTR.txt:764` `set qing_sect_pressure = 0` must ALSO zero the target's pull
  — gate the target formula to 0 under `has_variable = qing_fully_modernized` (NOT `qing_selfstr_progress`,
  which rises mid-game — re-review F3), else the annual scan re-derives it back up (review M2).
- **RHS-comparison rule / div0:** the drift-toward-target compare needs the `_cmpsvalue` wrapper; any scale
  divisor must be a literal (as the ethnic `/2` is), so no div0.
- **Mission double-count / loop (review C2):** mission friction already reaches sect via nudges
  (`se_QING_MISSIONARY.txt:235`/`:116`/`:128`) AND `qing_mission_social_friction` reads sect back (`:197`
  `sect/4`) then pushes at `:235` — a two-way loop. DO NOT also put the mission footprint in the target.
  Target = DEMOGRAPHICS only; mission stays a nudge. (Distinct from `qing_antichristian_sentiment`, which
  READS sect as an input at `:251` — not an overlap risk.)

## 4. Phasing
Single-phase, EASY/MEDIUM — fold the sect tally into the existing annual ethnic sweep (one pass computes
both `qing_ethnic_restive_weighted` and a new `qing_sect_restive_weighted`), then target+drift both.

## 5. Build checklist
1. Extend `QING_DECLINE_recompute`'s annual `every_owned_province` loop to ALSO tally
   `qing_sect_restive_weighted` = provinces with `dominant_province_religion = pure_land_buddhism` (the
   White Lotus faith — F1; NOT the accepted-religion negation) + religious `province_unrest>=4` (reuse the
   single pass; `dejure_culture` coverage is total — F3-REFUTED). DEMOGRAPHICS ONLY — no mission footprint (C2).
2. `qing_sect_pressure_target` from that tally with a BASELINE-FREEZE (structure of `:563-578`, but sect's
   OWN seed: `target = 0 + (current − frozen_base)/2` — NOT `+20`, F2), gated to 0 under
   `has_variable = qing_fully_modernized` (NOT `qing_selfstr_progress` — F3).
3. `QING_DECLINE_drift_sect_pressure`: quarterly ±N step of the live counter toward the target (mirror
   `QING_DECLINE_drift_ethnic_tension:810`). NO residual store.
4. Writers: 57 nudges UNCHANGED (they move the live counter; the target pulls it back — M1/M2).
5. Verify consumers (rebellion gates, mandate `>=50`, band — NOT reform_pressure, M3) unchanged; verify the
   1763 opening reads CALM (baseline-freeze → deviation ≈ 0, matching the seed-0 High-Qing start).
6. Review gates: target+drift (NOT base+residual); baseline-freeze with sect's OWN `+0` seed (NOT ethnic's
   `+20` — F2); sect faith = `pure_land_buddhism` DIRECT (NOT accepted-negation, which excludes the White
   Lotus & double-counts ethnic — F1/F4); self-str reset gated on `qing_fully_modernized` (NOT
   `qing_selfstr_progress` — F3); mission friction stays a nudge (no target double-count/loop — C2);
   reform_pressure NOT a consumer (M3); dejure coverage total (no under-count); RHS-cmpsvalue; 1763 opens
   calm at 0; brace/quote/BOM; boot-crash review.
