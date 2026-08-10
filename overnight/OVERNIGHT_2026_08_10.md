# OVERNIGHT 2026-08-10 — design + review phase (no builds until designed + reviewed)

Branch: merge-overnight. Author: freekumquats. Rule this session (user, explicit): **only build what has
passed diagnosis → adversarial review → design → adversarial review.** Several pending tasks were missing
designs; dispatch reviews + write those designs BEFORE building anything. Log every decision here (Rule 2).

## ⚠️ ASSUMPTIONS & GUESSES (scrutinize on the boot — every best-guess value/call lives here)
Per user directive: any magnitude, tuning constant, or best-guess design call made WITHOUT boot data is called out here explicitly so it can be checked/tuned on the verify boot. Each carries the log line that will confirm it.
- (#64) crop-seeding province PICKS + per-crop FLOORS (maize ≥12-15 etc.) — GUESS: chose specific American grain/livestock provinces + target counts by terrain/region judgement, not a sourced per-province list. Verify: crop distribution on the map + no economy destabilized (tzprobe).
- (#63) qing_monetary_bias VALUES — GUESS: standard_minting 0 / limited_minting −4 / currency_recall −8 / more_minting +4 / issue_bonds +8 (on a 0..100 stress meter where opium flow + reserve terms dominate). Verify: the "monetary-policy bias applied" LOG line + qing_currency_stress series shows a visible-but-not-swamping shift per stance.
- (#63) mint-CEILING magnitude — GUESS: sound-money ceiling = CURRENCY_minting_rate_cap × factor, factor = 1 + bias×0.0375 (limited −4 → ×0.85 / 15% tighter; recall −8 → ×0.70 / 30% tighter). PROPORTIONAL (a fraction of the cap, not a flat subtraction) so it scales with the cap + can NEVER zero minting regardless of the cap's magnitude (the #63-review MED). Verify: CURRENCY_minting_rate trimmed under a sound-money stance but nonzero.

- (#65) farmstead + reward magnitudes — GUESS: new_world_farmstead_building local_population_capacity_modifier 0.05 + local_lower_strata_output 0.1 + local_monthly_food 0.05; qing_newworld_agriculture modifier global_population_capacity_modifier 0.03 + global_population_growth 0.03; mission gate = ≥3 farmsteads. All best-guess (stack modestly on the automatic qing_nwcrop_abundance=8). Verify: pop logs show a boom, not a runaway.
- (#65) DESIGN DEVIATION (called out): the design said put the mission beat in qing_colonization_missions.txt, but that tree is FLEET/era-gated (the Pacific Enterprise) — wrong home for a 1763 domestic agrarian beat. Placed it instead in qing_settle_frontier_missions.txt (定牧墾邊, the domestic frontier-settlement tree, requires qing_settle_policy) — thematically correct + not fleet-gated. Flagged for the reviewer.

- (#44) salt revenue constants — GUESS: gabelle markup ×3.0; market-soft band [0.7,1.3] (raw salt price ×2 pivot); character factor band [0.5,1.3]; siphon = income×corruption/20; squeeze baseline 30 / finesse mirror 7. All best-guess to land salt near the ~12-15%-of-state-income target. Verify: the "salt: the 鹽課 pays its output-driven quarterly take" LOG vs total income (the ratio); commissioner factor moves it; siphon accrues to the man not the treasury/reserve.
- (#44) NOTE (pre-existing bug spotted, NOT fixed here to keep diff scoped): se_QING_REVENUE.txt:430 has a macro `$task$` inside a LOG_line string ("revenue fitness ($task$) = for") — a log-string-macro-rule violation that predates #44. Flag for a separate cleanup.

## Design/review inventory taken at session start (pending build tasks)
| Task | Design doc | Adv. review | Disposition |
|---|---|---|---|
| #29/#30 (#112b/c aqsaqal + contest) | §10 of DESIGN_FRONTIER_CUSTOMS_SUPERINTENDENTS_111_112.md | **dispatched** (rev-112bc) | impl-design written pre-compact; review was the MISSING gate |
| #44 salt monopoly | DESIGN_SALT_MONOPOLY_44 | ✓ done (§77 corrections) | design-complete, ready to build |
| #50 regional prices | DESIGN_REGIONAL_TRADE_PRICES_50 | ✓ done | complete; 1 open USER decision (cap) |
| #52 tier realism | DESIGN_TIER_REALISM_52 | ✓ done → "do-not-build; back to diagnosis" | blocked on full-tier probe data |
| #59 bimetallic | DESIGN_BIMETALLIC_59 | ✓ done (locked build order, Tier-A-first) | design-complete, ready to build |
| #62 NW double-count | DESIGN_NWCROP_DEMAND_RECLASSIFY_62 | ✓ done | blocked by #64 (crop geography) |
| #63 monetary-policy law | **was MISSING → written this session** | **not yet** | design written; review next |
| #64 NW crop American seeding | **MISSING** | — | research in flight (crop-geo agent) |
| #65 NW pop-boom flesh-out | **MISSING** | — | needs #64 + #66 first |
| #66 differentiation research | (research task, no design) | — | research in flight (good-diff agent) |

## Actions this session

### Dispatched — adversarial DESIGN review of #112b/#112c (§10 impl design)  [rev-112bc, running]
The §10 implementation design for the aqsaqal-promote (#112b) + the two-sided contest events (#112c) was
written pre-compaction but had NOT been through the second review gate. Building it would have skipped that
gate. Review dispatched (grounds against se_QING_AQSAQAL_SPIKE.txt, se_QING_CARAVAN.txt, qing_caravan_events,
gui/qing_caravan.gui, the #31 auto-arm hook, QING_governance_svalues) hunting: lifecycle-teardown wiring,
seat-timing / double-mint, flag↔character lockstep, the two-scope svalue read, whether "branch-parameterized
svalue" is actually implementable or needs N svalues, spike-retirement dangling refs, the #12 coupling claim,
and standing traps. Verdict will be folded into the doc as a §10-R CORRECTIONS block before any code.

### Dispatched — two research agents (prerequisites for #64/#65/#66)  [crop-geo, good-diff, running]
- **crop-geo**: real 1763 American geography of maize/sweet_potato/potato/peanut/chili (subsistence vs export,
  per-region), to correct the backwards seeding (#64) and unblock #62's per-crop demand choice.
- **good-diff (#66)**: how THIS mod (upstream = Sobisonator only) actually differentiates trade goods —
  demand svalues, building recipes, named script consumers — with a per-good table + verdict on where the NW
  crops sit. Feeds #65 (make the crops earn their keep) + #62.

### WROTE — DESIGN_MONETARY_POLICY_LAW_63.md (#63)  [design-complete, review next]
Verified the complaint: the Monetary Policy law options are read by NOTHING in live script (rg across common/
minus laws/loc → only design docs) — pure cosmetic vanilla modifiers, disconnected from the real currency
machinery. The PART D brace bug (DESIGN_LAW_EXPANSION) is ALREADY fixed and the cosmetic option fills ALREADY
shipped; #63 is the *mechanical wiring* PART D explicitly deferred.

**KEY DECISIONS logged in the design (with rejected alternatives):**
1. **Three additive+guarded wiring layers** (the P7 / #59-Tier-B idiom — a law writes a bias var; a pulse
   reads it behind `has_variable`, so default = byte-identical to today):
   - **Layer 1** `monetary_policy_setting` stance → a `qing_monetary_bias` var, read (a) into the existing
     qing_currency_stress recompute (se_QING_DECLINE.txt:201-211, one more additive term inside the clamp) and
     (b) into a CHI-only mint-rate clamp.
   - **Layer 2** `monetary_policy_law` (who controls the mint): **DECISION — do NOT add a second
     control→bias multiplier var** (over-build; the existing option modifiers already express competence/graft).
     Its only new role is unlocking Layer 3. Rejected alt: `qing_monetary_control_factor` — cut, logged loudly.
   - **Layer 3** — the deepest fix: `monetary_policy_setting.potential` is `has_law = legislative_monetary_policy`
     (republic-only), so a MONARCHY (the Qing) can NEVER pick a minting stance → the stance group is dead for the
     player. **DECISION — broaden the potential** to OR the three monetary_policy_law options (lean (a)); reject a
     parallel Qing-specific stance group (b) as duplication.
2. **Concrete lever = CHI-only guarded mint clamp**, NOT editing the shared `CURRENCY_minting_rate_cap` svalue
   (R2 currency-core caution: shared svalue feeds #23/#60 globally). Keep the change on the Qing side of the fence.
3. **R1 [HIGH] — NO stance flips `paper_money_allowed`** (would uncap minting → runaway M1 → #23/#60). issue_bonds
   stays a bias (+), not a paper-money unlock. Paper-money is a separate later gated mechanic, out of #63.
4. **Reconcile with DESIGN_LAW_EXPANSION item 23** ("Monetary Response" / qing_monetary_bias, not yet in script):
   #63 IS that wiring; item 23 (if later built) must reuse #63's qing_monetary_bias var, not a parallel one.

**OPEN capability check flagged (R5):** can a vanilla law OPTION carry an effect block, or must the bias-set be
an on_action on law change? If unproven after checking oracles/vanilla → small boot spike (overnight Rule 1
hard-block #1), not a hand-wave. **BLOCKER flagged:** confirm WHERE the Qing actually mints monthly (the CHI
call site of CURRENCY_mint_currency) so lever (a) has a real CHI-only insertion point — ground before impl.
Next: dispatch adversarial review of DESIGN_MONETARY_POLICY_LAW_63.md.

### Research returned (both agents) + digests recorded
- **#66 (good-diff) DONE** → research/RESEARCH_TRADE_GOOD_DIFFERENTIATION_66.md + memory imp19c-trade-good-differentiation-66. Verdict: 00_imp19c.txt is a CLOSED door (reverted by #219, afbf558b5); real differentiation = buildings + BOM recipes + a few bespoke demand svalues; maize/potato/sweet_potato earn their keep via the colonization-diffusion axis (unique), peanut/chili are flat dead-weight (need a BOM hookup or retirement). Task #66 marked completed.
- **#64 geography (crop-geo) DONE** → research/RESEARCH_NWCROP_GEOGRAPHY_64.md + memory imp19c-nwcrop-geography-64. Per-crop real 1763 ranges, region keys verified vs province_setup.csv. Key: maize/peanut/chili need Americas added (China → minority); potato must move OFF New Mexico onto Andean highlands; sweet_potato ~correct; the capacity lift is GLOBAL by design (American producers gaining it is intended).

### WROTE + dispatched review — DESIGN_NWCROP_AMERICAN_SEEDING_64.md (#64)  [rev-64 running]
Map-seeding design off the corrected geography. KEY: the source-of-truth blocker (CSV vs setup/provinces/*.txt — editing the wrong one is a silent no-op, the #281 trap) is flagged as the make-or-break to resolve at impl. CORRECTED a wrong premise mid-write: the qing_nwcrop_abundance capacity lift is GLOBAL BY DESIGN (se_QING_COLON.txt:283-285, CHI-gating explicitly rejected) — so American producers gaining it is intended, NOT a bug to owner-gate. Convert only generic grain/livestock provinces (don't destroy differentiated goods). Unblocks #62.

### WROTE + dispatched review — DESIGN_NWCROP_POPBOOM_65.md (#65)  [rev-65 running]
Flesh out the boom per the user's two rulings: buildings are GENERIC (Europe ate NW crops too), the Qing difference is a CHI reader keying off them (proven pattern). Three layers: (A) generic NW-crop farmstead + a peanut→oil / chili→processed-foods BOM hookup to make the two flat crops earn their keep (#66 gap); (B) CHI building-count boom reader extending the existing qing_migr_crop_boom; (C) events + a mission beat. Make-or-break flagged for the reviewer: is the peanut/chili BOM hookup buildable against an EXISTING manufactured good (no new trade good — #66 perf)? Depends on #64 + #62 landing first.

## Reviews returned + folded (3 of 4; rev-65 still running)
All three that returned = **PROCEED-WITH-CORRECTIONS**, folded into their designs as corrections blocks. Key catches:

- **#63 (rev-63):** (1) capability RESOLVED — law options DO carry `on_enact = { set_variable }` (proven 15× in 00_qing_statutes_laws.txt) → DROP the R5 boot-spike. (2) NO CHI-only mint site — CHI mints via the shared monthly_currency_pulse → lever (a) reframed as a CHI-only guarded rate-CEILING in the Qing pulse. (3) the mint lever can only TIGHTEN, not loosen (hard-clamp to the forbidden shared cap) — loose stances act only via stress-bias + cosmetic modifiers. (4) Layer 3 must scope to `OR={legislative  tag=CHI}` (broadening exposes every non-tribal monarchy AI). (5) read #1 = direct term into the stress LEVEL, never the decaying residual. (9) law files are BOM+**CRLF** (design missed CRLF). #59 collision NONE confirmed.

- **#64 (rev-64):** (C1) the source-of-truth blocker is ALREADY RESOLVED — edit `setup/provinces/*.txt`, NOT the CSV (CSV is not engine-read; decision at OVERNIGHT_DECISIONS2.md:207-218). (C2) current-state counts were STALE (from the CSV) and wrong — re-baselined from .txt: peanut=3 (not 5), chili=3 (not 6); qualitative defect (0 Americas) holds. (C-H1) commit to numeric per-crop American floors (maize ≥12-15, peanut ≥6, chili ≥6, potato Andean ≥4). R4 global-capacity + #62 ordering CONFIRMED sound (runaway worry over-stated; American provinces gain only the ceiling, not the ROOT=CHI growth push).

- **#112b/c (rev-112bc):** BLOCKERS — (C1) seat the aqsaqal in the shared `QING_caravan_grant_aqsaqal` effect (3 grant paths), NOT in qing_caravan.1. (C2) the REVOKE path dangles the character — seat+teardown must be PAIRED. (H1) teardown "reuse verbatim" was hand-waved — must rewire the death + KOK-lost hooks to a new shipping marker (spike retirement deletes the old ones). (H2) the contest svalue can't be "one branch-parameterized family" — needs 3 chance + 3 fail svalues. (H3) court-slot + `qing_dept_cd_caravan` throttle is MANDATORY (#41 flood class), not "if needed". (M1) the svalues ALREADY ship — don't "lift"/duplicate. Build gate: C1/C2 before #112b, H2/H3 before #112c code.

- **#65 (rev-65): PROCEED-WITH-CORRECTIONS — but the design was materially over-scoped on two WRONG premises, now corrected.** (C1) DROP the peanut/chili BOM hookup: it's buildable but the industrial-BOM demand path is DISABLED (se_DEMAND.txt:6-9, debug-gated, #133) → inert in the agrarian-boom era. (C2) #66's "peanut/chili luxury-only, no food path" was STALE — they already feed fulfilled_food_need (DEMAND_food_svalues.txt:101-102); the only gap is dynamic-basket membership (a #62 decision, not a building). (C3) Layer B's "fold a term into the boom driver" is IMPOSSIBLE — the boom is a flat event-applied modifier, no continuous driver; the honest lever is a small local modifier ON the building → Layers A+B COLLAPSE into one object, drop the CHI reader. (C7) MINIMAL SLICE: one generic "new world farmstead" (generic file, NO culture exclusion — C5) + one mission-task beat in the existing tree; the qing_migration.20-23 chain is already the boom narrative (don't rebuild). Fixed the wrong events path. Corrected the #66 research digest + memory to match (peanut/chili have a partial food role; BOM is a dead end).

## ALL FOUR REVIEWS RETURNED + FOLDED
Every pending design has now cleared the adversarial-review gate (all PROCEED-WITH-CORRECTIONS, corrections folded). NOTHING built (user directive). Design+review-complete + buildable (each with its build gate documented): #44, #59, #63, #64, #65 (minimal slice), #112b/c. #62 unblocks once #64 lands. Ready-to-build order when the user green-lights building: cheapest-certain first — #62 (after #64), #64, then #44/#59/#63/#65/#112b-c.

## Research digest corrections (post-review)
- RESEARCH_TRADE_GOOD_DIFFERENTIATION_66.md + memory imp19c-trade-good-differentiation-66: corrected the "peanut/chili luxury-only, no food path" claim (stale) → they have a partial food role; BOM-hookup is a dead end (dormant subsystem).

## ROUND-2 REVIEW CYCLE (user directive: "nothing gets built until a clean review passes", applies to ALL tasks)
The round-1 corrections were folded INTO each design body (not left as a contradictory appended block), committed (8e4c9180c), and re-dispatched for round-2 confirmation reviews:
- rev63b (#63), rev64b (#64), rev65b (#65), rev112b2 (#112b/c) — each confirms the integrated body is internally consistent + buildable (CLEAN) or returns remaining findings.
Autonomous plan (user directive: work per imp19c-overnight, full loop): round-2 CLEAN → task is build-ready; more corrections → fold + round-3 until clean. THEN implement in ID order, each task its own impl → adversarial review → fix → re-review until CLEAN → commit+push as freekumquats. #62 unblocks after #64 lands. #50 (cap decision) + #52 (probe data) remain the two genuine holds.

### Round-2 verdicts (as they land)
- **#65 (rev65b): CLEAN ✅** — the minimal-slice rewrite holds on every load-bearing point (BOM dropped/dormant confirmed; no continuous boom driver confirmed; generic-file + OMIT-culture-gate confirmed; farmstead capacity stacks on the automatic =8; mission idiom + tree file both exist; peanut/chili food-role confirmed; events path correct). No corrections. Design+review-COMPLETE. Build order: AFTER #64 + #62.
- **#63 (rev63b): PROCEED-WITH-CORRECTIONS (1 MED, 1 LOW) → folded, needs round-3.** MED: adding `tag=CHI` to the setting-group potential makes the Qing auto-default-hold the FIRST option (`currency_recall`), whose `modifier` applies at boot → silent −0.05 commerce/+0.03 stability, NOT byte-identical. FIX folded: prepend a neutral `standard_minting` first option (`modifier={}`, on_enact sets bias 0) — inert auto-default AND the "return to neutral" stance R6 wanted (two birds). LOW: read#2 lives in QING_DECLINE_pulse which is QUARTERLY/human-CHI, not monthly — reworded (correctness holds, ≤1 quarter slider slack). Core mechanism confirmed sound (on_enact proven, level-not-residual, mint asymmetry, Layer 3 scope, BOM+CRLF). Round-3 confirm dispatched.
- **#63 (rev63c round-3): effectively CLEAN ✅ — 3 LOWs folded.** Neutral-default fix CONFIRMED byte-identical (in-repo precedent: 00_qing_statutes_laws.txt:5-8 documents "first option = current-behavior default, held modifier applies"; empty modifier legal ~6 precedents; on_enact proven ~15×). LOW-1 (substantive): prepending standard_minting ALSO shifts the REPUBLIC default currency_recall→neutral — folded into R6 as intended/harmless ("republics unchanged" is true only of the potential change, not the prepend). LOW-2/3 (audit hygiene): tagged round-1 items #2 ("monthly"→quarterly superseded) + #6 (SUPERSEDED by round-2 R6) so an implementer skimming the trail can't follow stale guidance. Design+review-COMPLETE.
- **#64 (rev64b): PROCEED-WITH-CORRECTIONS (1 MED, rest CLEAN) → folded, no round-3 needed.** All 4 axes confirmed clean (CSV-demoted, counts exact [maize 6/peanut 3/chili 3/sweet_potato 6/potato 5 with file:line], floors achievable, R4/#62/revenue-coupling/#279 all sound). The ONE MED: my BOM directive was INVERTED — I wrote "keep setup/provinces BOM-free" but those history files DO carry a UTF-8 BOM (verified ef bb bf on Hunan/Peru/Southwest/Eastern_Mexico) and boot fine; the "setup-reader-rejects-bom" memory is a DIFFERENT reader (its own line 23 already scopes province files as BOM-keeping). FIX folded: "PRESERVE existing BOM+EOL, don't add/strip/convert." One-line polarity flip, fully consistent with verified memory → no round-3. Design+review-COMPLETE.
- **#112b/c (rev112b2): CLEAN ✅ + 2 LOW polish folded.** All five round-1 corrections confirmed correctly reflected (C1 seat-in-shared-effect, C2/H1 paired teardown into revoke/death/KOK-lost w/ new marker, H2/M1 3+3 svalues in place, H3 mandatory slot+dept throttle, M2 #12 write-back; M3 alive-guard + spike-retirement checklist also confirmed). LOW-1: ≥4 grant paths not 3 (the trade-concession law on_enact also routes through the choke-point effect — covered) → reworded. LOW-2: delete the loc key at its DEFINITION (qing_caravan_l_english.yml:21-22), not just the gui use-site → checklist precised. Design+review-COMPLETE (build #112b then #112c).

## IMPLEMENTATION PHASE (all four designs review-clean; building in ID order)
- **#64 — DONE ✅ (committed a3865a251).** Converted 38 American provinces' `trade_goods=` from generic grain/livestock (+ 2 misplaced New Mexico potato → maize) to the 5 NW crops across 13 setup/provinces/*.txt files. American totals: maize 18, peanut 6, chili 8, sweet_potato 3-new, potato 6 Andean — all floors met, China now minority for maize/peanut/chili, potato Andean-only. rev64impl = CLEAN (scope/floors/picks/integrity/downstream all verified). Full loop: design→review×2→impl→review→commit. Unblocks #62.
- **#62 — DONE ✅ (committed 8a35b6789).** Production-gated food-only rewrite of maize/potato/sweet_potato Totals + 6-line luxury call-list cleanup; peanut/chili untouched. Full loop: design→rev62(MED folded)→impl→rev62impl(HIGH: off-region phantom demand → gate fix)→re-review CLEAN→commit. On-region bounded food demand, off-region →0 (#279 invariant restored). Verify-on-boot via tzprobe demand bands.
- **#62 — (superseded log below) final resolution reviewed (rev62 = PROCEED-WITH-CORRECTIONS, 1 MED folded) → IMPLEMENTED, post-impl review running (rev62impl).** rev62 confirmed the core fix correct + potato food-only SAFE (no luxury floor — Andean producers consume locally, no industry consumer, near-zero 1763 China potato demand is historically right). MED folded: the 3 rewritten Totals mirror DEMAND_grain EXACTLY (`value = DEMAND_food_<crop>` + `min=0`) — dropped the luxury seed + else=base_total + wealth-elasticity block AND the final `multiply=DEMAND_elasticity_impact` (a wealth-downturn malus food goods must not carry); used the BOUNDED svalue not the raw var (rev62 LOW). IMPL: DEMAND_luxury_svalues.txt (3 Total rewrites, LF+BOM) + se_DEMAND.txt (−6 luxury call-list lines, CRLF+BOM preserved, numstat 0/6 no churn); peanut/chili untouched; #279 count block untouched; braces balanced. Pending rev62impl → commit.

## Ready-to-build once the review backlog clears (design+review complete)
- #44 salt monopoly (DESIGN_SALT_MONOPOLY_44 §77 corrections + revised minimal slice).
- #59 bimetallic (DESIGN_BIMETALLIC_59 locked Tier-A-first build order).
- #112b/c pending rev-112bc verdict; #63/#64/#65 pending their verdicts.

## Memory housekeeping
- MEMORY.md compacted 19.9KB → 18.2KB (capped hooks, fixed 5 links that pointed at repo docs not memory files; no entries dropped).
