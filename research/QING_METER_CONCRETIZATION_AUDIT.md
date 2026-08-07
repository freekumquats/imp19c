# Qing abstract-meter concretization audit (2026-08-06)

Systematic sweep of the Qing suite for abstract 0–100 "drift meters" (the `_target` + `_band_prev` +
`_cmpsvalue` signature) and nudge-accumulators, triaged by the [[imp19c-concrete-over-abstract-rule]]
test. Backs the ongoing conversion program (bureau_capacity/exam_ladder/corruption docs).

## Classification test
- **DERIVED** (leave — imitate): value computed live from concrete state (characters/buildings/provinces/pops).
- **ABSTRACT-OK** (leave): no single on-map referent — a genuinely systemic gauge.
- **TARGET-EASY**: concrete referent exists, low touch-count, clean convert.
- **TARGET-HARD**: concrete referent exists but many writer sites / rewrite needed.

## Meters found (21 with `_target`, plus pure accumulators)

### DERIVED — already concrete-driven (leave; these are the model)
| Meter | Derives from | Note |
|---|---|---|
| `qing_council_effectiveness` | seated GC characters' skill + ministry-perf | GOLD standard. (Minor: folds `qing_dynastic_harmony`, an accumulator — hybrid.) |
| `qing_ethnic_tension` | `qing_ethnic_restive_weighted` = `every_owned_province` unrest/culture-plurality sweep | concrete (pops+provinces). DERIVED. |
| `qing_pop_pressure` | `total_population` (pop object count) | DERIVED. |
| `qing_min_perf_*` (ministry panels) | holder martial / roster / garrison counts | DERIVED (feed council_eff). |
| `qing_reform_pressure` | SUM of corruption+currency_stress+ethnic_tension+banner_decay | derived, but from OTHER meters (transitively only as concrete as its inputs). |
| `qing_granary_stock` | **DERIVED = qing_granary_food / (granary_count × 200) × 100** (`se_QING_DECLINE.txt:2313`) | ⚠️ **CORRECTION 2026-08-06: this was WRONGLY listed as TARGET-EASY below on a signature-grep; it is ALREADY concretized (#91 K / #435).** The meter is a fill-ratio of the REAL `qing_granary_building` network (cap = count × 200 food) filled by an actual per-state surplus→shortage food sweep. Best-in-class concrete pattern (derives from buildings AND food flows). The `QING_DECLINE_nudge` hits are legacy consumers, not the driver. LEAVE — imitate. |

### ABSTRACT-OK — systemic gauges, no clean on-map referent (leave)
| Meter | Why abstract |
|---|---|
| `qing_mandate_strength` | Mandate-of-Heaven — VERIFIED pure accumulator (seed 80 + 4 nudges, decline gated on corruption≥65/sect≥50) but genuinely NO on-map referent exists. Correctly abstract; the purest leave-it in the suite. |
| `qing_wenzhi_patronage` | cultural-patronage standing (#390). Its PAYOFFS are concrete (dispatches real culture events + modifiers) but the meter itself has no single object. Weak/minor (~3 sites); leave. |
| `qing_hoppo_squeeze` | corruption of one post; could tie to the Hoppo character — minor, low priority. |

### ⚠️ RECLASSIFIED ABSTRACT-OK → TARGET on read-verification (2026-08-06)
My first-pass "abstract-OK" bucket was over-generous (same over-trust that mis-bucketed granary the other
way). Three flipped on reading the actual driver:
| Meter | Was | Now | Finding |
|---|---|---|---|
| `qing_currency_stress` | ABSTRACT-OK | **TARGET — DOC WRITTEN** | Already reads `CURRENCY_reserve_ratio_impact` but as a 1-BIT threshold (<0.5). Should derive continuously from reserve ratio + inflation; opium term (concrete #366) → residual. `DESIGN_CURRENCY_STRESS_CONCRETIZE.md`. |
| `qing_gp_tension_{britain,france,russia}` | ABSTRACT-OK | **❌ RETRACTED → LEAVE (accepted hybrid)** | My "reads nothing / #91 H unbuilt" claim was WRONG (adversarial review 2026-08-06). #91 H IS built: `QING_gp_rival_launch_play` (se_QING_DIPLO.txt:769) fires a REAL `AI_begin_diplomatic_play` off tension≥75; a live play already feeds BACK as a nudge (`QING_gp_scan_plays:720`). Base-derivation infeasible (is_in_diplomatic_play/at_war/country-is_rival don't exist in this engine) + circular (tension sets the opinion a base would read). Outcome already concrete; counter stays the drift layer BY #91 DESIGN. Not a target. My grep for `start_diplomatic_play` false-negatived (real launcher = `AI_begin_diplomatic_play`). See DESIGN_GP_TENSION_CONCRETIZE.md (retraction). |
| `qing_sect_pressure` | ABSTRACT-OK | **TARGET-EASY/MED — DOC WRITTEN (reviewed+revised)** | Seed 0 + 57 nudges, NO derive block. Fold a heterodox-province tally into the ANNUAL ethnic sweep (se_QING_DECLINE.txt:478-567), TARGET+DRIFT with baseline-freeze (NOT base+residual — review M1). Heterodox = NEGATION of `chinese_accepted_religion_trigger_province` (NOT `!=confucianism`, which flags ~600/610 provinces — review C1). DEMOGRAPHICS ONLY in target; mission friction stays a nudge (already feeds sect via se_QING_MISSIONARY.txt:235/:116/:128 — folding it in would double-count + tighten the :197 sect/4 loop — review C2). 57 nudges UNCHANGED. `DESIGN_SECT_PRESSURE_CONCRETIZE.md`. |

### TARGET — concrete referent exists but meter is a free accumulator
| Meter | Referent (should derive from) | Touch-count | Tier | Status |
|---|---|---|---|---|
| `qing_bureau_capacity` | **yamen building count** | ~13 | EASY | **DOC WRITTEN** (DESIGN_BUREAU_CAPACITY_CONCRETIZE.md) |
| `qing_exam_ladder` | **shuyuan building count** | ~11 | EASY | **DOC WRITTEN** (§9 same doc) |
| `qing_corruption_level` | **character `corruption` values** | ~210 | HARD | **DOC WRITTEN** (DESIGN_CORRUPTION_CONCRETIZE.md, 2-store) |
| `qing_xinjiang_control` | the real **ILI autonomous_governorship subject** + Xinjiang province modifiers | ~19 | MEDIUM | #91 item D — backlog says planned; verify if done. Referent is a live subject. |
| `qing_banner_decay` / `qing_greenstandard_decay` / `qing_modernarmy_share` | the real **banner/green-standard/新軍 legions** (unit objects) | ~24/7/9 | MEDIUM | #91 item G — decay bands→legion morale, modern share→raise_legion. Concrete referent = units. |
| ~~`qing_granary_stock`~~ | ~~granary buildings~~ | — | **NOT A TARGET** | ❌ **RETRACTED — already DERIVED (see DERIVED table above). #91 K / #435 already did this correctly.** My signature-grep false-positived it. |
| ~~`qing_customs_efficiency`~~ / ~~`qing_customs_foreign_control`~~ | — | — | **❌ RETRACTED → LEAVE** | Review 2026-08-06: efficiency is ALREADY DERIVED (`eff_target=(foreign_control×2+bureau_integrity)/3`, se_QING_CUSTOMS.txt:170 — 3rd granary-style false positive). foreign_control is a real accumulator but deriving from "IG foreign" is broken (no foreign flag; Manchu∈jurchen; can't reproduce the 0-100 gradient the sinicize verb needs). Custom-houses ARE seeded at 1763 (se_QING_BUILDINGS.txt:249). Both fine as shipped. Optional: fold guarded IG-finesse into efficiency's existing target. See DESIGN_CUSTOMS_CONCRETIZE.md (retraction). |
| `qing_suzerain_prestige` / `qing_tributary_prestige` | live **tributary subject count** | ~23/3 | MEDIUM | #91 item A — derive from `any_subject` count, not accumulate. |
| `qing_caravan_prosperity` | derives partly from `qing_xinjiang_control` (another meter) | ~5 | LOW | half-derived; only as concrete as xinjiang_control. |
| `qing_students_abroad`/`_returned`/`_alarm` | real **returnee characters** | ~3/7 | MEDIUM | #91 item C — spawn returnee chars at milestones. |
| `qing_dynastic_harmony` | the real **dynasty characters** (Emperor/Dowager/princes relations) | (folds into council_eff) | MEDIUM | pure accumulator; referent = imperial-family characters. Flagged by bureau review #3. |
| `qing_han_provincial_power` | real **Han magnate-governor characters** (#90/#105) | ~6 | MEDIUM — **DOC WRITTEN (reviewed+revised)** | Derive by BLENDING a COUNT of magnate-governors (`has_character_modifier=qing_regional_magnate` OR `num_loyal_cohorts>=X` as a TRIGGER — NOT a cohort sum, which is unbuildable; F1) into the EXISTING decay-pressure target (do NOT decouple — keeps the forced-devolution + 新軍-suppression channels; #3). Separatism ARMS at 80 not 90 (F4). `qing_regional_magnate` marker already exists (F5). DESIGN_HAN_PROVINCIAL_POWER_CONCRETIZE.md. |
| `qing_wenzhi_patronage` | ? (#390 — meter+initiatives) | ~3 | LOW | scholarship patronage; referent unclear, maybe abstract-OK. |
| `qing_antichristian_sentiment` | #91 item P — real agitator character at threshold | ~5 | LOW | ambient sentiment; concretize the OUTCOME (char), keep drift. |
| `qing_opium_import_index`/`_addicted_share` | the opium trade-balance model (#366) | ~3 | — | already a concrete trade-flow feed; ABSTRACT-OK outcome. |

## ⚠️ RELIABILITY CAVEAT (2026-08-06)
This table was built by SIGNATURE-GREP (the `_target`/`_band_prev`/nudge patterns), NOT a per-meter read
of each derivation. That produced at least one FALSE POSITIVE: `qing_granary_stock` was listed TARGET-EASY
but is in fact already DERIVED (#91 K/#435, retracted above). **Every "TARGET" below MUST be verified by
reading its actual driver before being trusted or turned into a design doc** — a meter appearing in the
`QING_DECLINE_nudge` list does NOT prove it's a free accumulator (the nudges may be legacy consumers atop a
derived value, as with granary). The three docs already written (bureau/exam/corruption) WERE read-verified;
the rest have not.

## VERIFIED status (all read-checked 2026-08-06)
**Docs written (3):** bureau_capacity+exam_ladder, corruption_level, currency_stress — all adversarially
reviewed except currency_stress (pending). Task cards created for each.

**Confirmed TARGETs still needing docs (read-verified as pure/near-pure accumulators):**
1. **sect_pressure** (EASY/MED — copy the adjacent ethnic_tension province-sweep; + mission system). 57 nudges→residual.
2. ~~gp_tension_×3~~ — RETRACTED, not a target (#91 H already built; see reclassified row above).
3. **suzerain/tributary_prestige** (MEDIUM — #91 A, derive from live `any_subject` count; TOP of #91 backlog).
4. **treaty_burden / treaty_ports** (MEDIUM — #91 B PARTIAL: stamps real `qing_treaty_port` modifiers but
   the count is a hand-`change_variable` tally, not `every_owned_province { has_province_modifier }`. Invert.).
5. **banner/greenstandard/modernarmy_share** (MEDIUM — #91 G, unit-derived; biggest thematic payoff).
6. **xinjiang_control** (MEDIUM — #91 D, ILI subject).
7. ~~customs_efficiency/foreign_control~~ — RETRACTED (efficiency already derived; foreign_control fine as accumulator). 3rd granary-style false positive.
8. **han_provincial_power** — DOC WRITTEN+REVISED (blend magnate-count into existing decay target).

**Meter-of-meter (fix transitively via their inputs, no own doc):** reform_pressure, caravan_prosperity,
modernarmy (reads selfstr_progress), han_provincial_power (reads banner_decay).

**Leave (genuinely abstract):** mandate_strength (no object), wenzhi_patronage (payoffs concrete, meter weak),
hoppo_squeeze (minor). ~~granary_stock~~ RETRACTED — already correctly derived.

**#91 status note:** #91 shipped its items as intended HYBRIDS ("add a concrete face/outcome, keep the
counter as the drift/summary layer"). Item H IS BUILT (`QING_gp_rival_launch_play`, se_QING_DIPLO.txt:769,
launches a real `AI_begin_diplomatic_play` off tension≥75). ⚠️ My earlier "H unbuilt" was a FALSE-NEGATIVE
GREP (searched `start_diplomatic_play`; this engine's launcher is `AI_begin_diplomatic_play`) — it
contaminated this audit + a memory file + a whole design doc before review caught it. LESSON: grep the
CAPABILITY (what effect launches X?), never a guessed token. The genuine remaining TARGETs are meters that
are pure accumulators IGNORING a concrete referent (bureau/exam/corruption/currency/sect + #91 A/D/E/G/K
items) — NOT ones whose outcome #91 already concretized (gp_tension is NOT a target).

## Note
Many TARGETs ARE #91 backlog items (A/C/D/E/G/K) — #91 was only PARTIALLY built (it concretized some as
"add a face, keep the meter" hybrids). This audit says: for the ones with a clean count referent (granary,
customs, tributary), finish the job by INVERTING (derive the meter FROM the object), not just adding a face.
