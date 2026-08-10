# OVERNIGHT 2026-08-10 — design + review phase (no builds until designed + reviewed)

Branch: merge-overnight. Author: freekumquats. Rule this session (user, explicit): **only build what has
passed diagnosis → adversarial review → design → adversarial review.** Several pending tasks were missing
designs; dispatch reviews + write those designs BEFORE building anything. Log every decision here (Rule 2).

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

## Reviews in flight (4)
rev-112bc (#112b/c), rev-63 (#63), rev-64 (#64), rev-65 (#65). Fold each verdict into its design as a corrections block BEFORE any code. NOTHING is being built until each design clears its gate (user directive this session).

## Ready-to-build once the review backlog clears (design+review complete)
- #44 salt monopoly (DESIGN_SALT_MONOPOLY_44 §77 corrections + revised minimal slice).
- #59 bimetallic (DESIGN_BIMETALLIC_59 locked Tier-A-first build order).
- #112b/c pending rev-112bc verdict; #63/#64/#65 pending their verdicts.

## Memory housekeeping
- MEMORY.md compacted 19.9KB → 18.2KB (capped hooks, fixed 5 links that pointed at repo docs not memory files; no entries dropped).
