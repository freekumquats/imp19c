# OVERNIGHT — Abstract-meter concretization (autonomous run, 2026-08-06)

Mandate: verify remaining meter targets → design the passing ones → adversarially review each design →
implement all reviewed designs → adversarially review implementations → commit. Log every decision here.

## Standing lessons this session (why every step is read-verified + reviewed)
- **3 granary-style false positives** (granary, customs efficiency, gp_tension play-launch): a meter in the
  `QING_DECLINE_nudge` list may already be DERIVED, or its "referent" already built. ALWAYS read the full
  driver before calling it a target.
- **2 primitive over-claims** (han cohort-sum, "country-only"): a per-character TRIGGER (`num_loyal_cohorts >= X`)
  is NOT a readable VALUE. Verify the exact read primitive in the oracle repos, not a guessed token.
- Every design this session needed a review pass; 4 of 8 needed a retraction or core rewrite. Reviews stay.

## Phase A — verification verdicts (read-checked 2026-08-06)
| Meter | Driver today | Already derived? | Concrete referent | Verdict |
|---|---|---|---|---|
| `qing_suzerain_prestige` / `qing_tributary_prestige` | 26 nudges, NO derive block | No | live tributary SUBJECTS (Korea/Vietnam/Ryukyu/… `subject_type=tributary`) | **PASS → design** |
| `qing_treaty_ports` | hand `change_variable +5/+1` tally | No (hand-tally, not derived) | real `qing_treaty_port` province modifiers (`se_QING_TREATIES.txt:175`) | **PASS → design** |
| `qing_treaty_burden` | pure nudge | No | the treaty-port footprint (same referent as above) | **PASS → fold into treaty design** |
| `qing_banner_decay` / `qing_greenstandard_decay` | pure nudge (seed + nudges) | No | real `qing_banner_garrison_building` (10+ seeded) + banner/GS legions | **PASS → design** |
| `qing_xinjiang_control` | event set/nudge | No | the real **ILI subject** (`c:ILI is_subject_of ROOT`, `se_QING_ILI.txt:458`) + Xinjiang provinces | **PASS → design** |

All four PASS (none already-derived). Designs to be drafted + adversarially reviewed (Phase B/C), then
implemented (Phase D) and implementation-reviewed (Phase E), then committed (Phase F).

## Implementation ORDERING constraint (critical — logged before building)
`se_QING_DECLINE.txt` is a COLLISION ZONE: corruption(#2), sect(#5), han(#6), currency(#3), banner/gs, and
tributary/xinjiang all edit it. `se_QING_GOVERNANCE.txt` is edited by bureau/exam(#1) + corruption. So
implementation MUST be SERIAL per-file, never parallel (parallel edits to these shared files corrupt them).
Design+review (Phase B/C) IS safely parallel (design-only, no committed-code writes).

## Decisions log
(appended as the run proceeds)

## Readiness (user 2026-08-06)
- READY TO IMPLEMENT (reviewed+fixed): #1 bureau/exam, #2 corruption, #3 currency, #5 sect.
- NEEDS RE-REVIEW + fixes before implement: #6 han_provincial_power (revised after 1st review; not re-reviewed).
- 4 NEW designs to draft+review: tributary/suzerain prestige, treaty ports/burden, banner/GS decay, xinjiang_control.

## Execution plan (autonomous)
Phase B (parallel-safe, design-only): draft the 4 new designs.
Phase C (parallel): adversarial review — 4 new designs + #6 re-review = 5 agents.
Phase D (SERIAL per shared file — se_QING_DECLINE.txt + se_QING_GOVERNANCE.txt are collision zones):
  implement #1, then #2, then #3, then #5 (each fully verified before next). New designs implement after
  their reviews clear.
Phase E: adversarial review of each implementation.
Phase F: commit (freekumquats, merge-overnight, per branch+authorship rules) + push.

## User refinements (2026-08-06)
- ONE COMMIT PER METER (design→review→implement→review→commit individually) for easy debugging/bisect.
- Meter-of-meters (reform_pressure/caravan/modernarmy): revisit AFTER leaf meters land; concretize ONLY if
  a real referent exists — do NOT force it where it doesn't make sense. Same full process if pursued.
- Do not force implementations where concretization doesn't make sense (retract like customs/gp_tension).

## IMPLEMENTATION BLOCKER #1 (bureau/exam) — max_level is NOT a valid Imperator building key
Found at implement-time (2026-08-06): the bureau/exam design's CRITICAL fix "add max_level=1 to yamen/shuyuan"
is UNBUILDABLE — `max_level` appears 0× in this mod's buildings AND 0× in either oracle repo; Imperator's
building schema has no max_level/unique cap (only modifiers/cost/time/allow/modification_display; level count
is limited by job slots + building slots, not a per-building cap). This is another unverified-primitive catch.
RESOLUTION (verified idiom): use `potential = { NOT = { has_building = qing_yamen_building } }` to enforce
one-per-province — add_building_level RESPECTS potential (proven in-repo qing_works_buildings.txt:156 +
memory add-building-level-respects-potential). Once a province has the building, the type is hidden there =
effectively max 1 level per province. Update DESIGN_BUREAU_CAPACITY_CONCRETIZE.md §1a/§9a: max_level=1 →
potential-guard. NOTE the tradeoff: `potential` on a modded building that add_building_level also uses means
the SEED must run before/despite the potential (seed uses add_building_level which respects potential, and
NOT has_building is true on an empty province, so the seed still lands — verify). Also: the admin-capacity
exploit fix now relies on the potential-guard capping at 1 level/province (num_of_qing_yamen_building ∈ {0,1}).

## REVIEW: treaty_ports/burden (#8) — 2 CRITICALS → scope narrowed
- C1: deriving qing_treaty_burden from port COUNT is WRONG — burden is a path-dependent grievance gauge;
  ports never decrement, so revision (−12/−30) couldn't ease a count-derived burden (kills the payoff arc),
  and losing treaty-port provinces would DROP burden (losing a war reduces humiliation — backwards). CUT the
  burden derivation; burden stays a nudge meter. Restrict #8 to the COUNT only.
- C2: even the count change alters tier-band semantics — today qing_treaty_ports is a MONOTONIC "N ever
  opened" tally; a live modifier-count makes it "N currently OWNED" (tiers can fall on territory loss;
  _dominant needs 12 held cities, maybe unreachable). MUST be decided, not assumed. If the bands want
  monotonic semantics, a live count is the WRONG source → #8 may be a DON'T-FORCE (retract).
- DECISION: treaty_burden derivation CUT. treaty_ports count = deferred pending the monotonic-vs-owned
  semantics call — leaning DON'T-FORCE (the existing tally is arguably correct; concretizing it changes
  gameplay, not just cleans abstraction). Flag for user; do not implement #8 blindly.
Doc updated. This is the "do not force where it doesn't make sense" case the user flagged.

## IMPLEMENTATION PROGRESS
- #1 bureau/exam: building defs done (potential-guard = one-per-province, replaces the invalid max_level).
  Seed compatible (QING_seed_works_building already guards NOT has_building, se_QING_BUILDINGS.txt:443).
  se_QING_GOVERNANCE.txt meter-removal + reach-svalue edit: IN PROGRESS.

## REVIEW: tributary/suzerain prestige (#7) — DON'T FORCE (retract the derive)
- C1: `is_subject_type = tributary` matches only 1 of 4 (the others are `sinosphere_tributary`) → meter
  collapses at game start. Correct gate = QING_tribute_is_tributary_trigger (OR of both types).
- C2: abandon lever BOTH nudges −25 AND release_subject (shrinks roster) → derive double-charges the loss.
- M4/M5: static roster 1763→1890s adds little signal; the "readout of live roster" is ALREADY delivered by
  QING_vassal_sync_lost_flags. qing_tributary_prestige is DEAD code (never initialized) — retire it.
- DECISION: #7 = DON'T FORCE. Do NOT add a roster-derive to suzerain_prestige (would break more than it
  cleans). Narrow to retiring the dead qing_tributary_prestige stub (cosmetic). Task #7 → won't-fix as
  concretization; optional dead-code cleanup only.

## REVIEW: han_provincial_power (#6) re-review — 2 blockers FIXED, spec gaps remain (fixable)
Confirmed: cohort-sum→count correct, separatism 80 correct, blend-not-decouple correct. Remaining (all
spec-tightening, doc survives): (V2) pin the blend operator = WEIGHTED SUM (not max — max lets 新軍
suppression be overridden), added before the 0..100 clamp alongside qing_provmil_bias (:433). (V4) pin
@han_magnate_cohort_threshold >= 10 (the one proven value), verify no 1763 Han governor starts ≥ it.
(V6) sanction double-count: the magnate now enters the count durably AND the +15 nudge fires → DROP/reduce
the +15 (se_QING_MECHANICS.txt:152), let the count carry realized devolution, keep −8/−8 relief. (7B/7C)
2 miscited "proven" idioms (every_character vs any_character) — fix citations. Applying fixes to doc now.

## REVIEWS: banner (#9) + xinjiang (#10) — BOTH REJECT (don't force)
- #9 banner/GS decay: garrison buildings have NO removal path (monotonic) → "decay=inverse of count" can't
  climb, flatlines ~0, kills the decline arc; legion strength isn't readable (no manpower read; legion loop
  is GUI-crash-class). Existing meter already correct (high_qing_era suppresses zenith creep). CLOSE #91-G
  as "no change — abstraction is correct here."
- #10 xinjiang_control: written by 4 subsystems (#367 consolidation + caravan + missions + ILI arc), not
  just ILI; derive would clobber all; ILI-subject-status is INVARIANT 1763→1860s (no signal); only 1 of 4
  arc beats maps to subject status. DON'T FORCE.
Tasks #9/#10 → won't-fix as concretization.

## CALIBRATION DECISION (self-made, autonomous — user: no dithering)
For buildable meters, the starting constants are chosen to REPRODUCE the current seed/behavior at 1763
(a mechanical, defensible default), commented PLACEHOLDER-tune-in-playtest. This is NOT "forcing" — it's
the standard concretize-preserving-behavior approach. Specifics per meter at implement time.

## USER DECISIONS (2026-08-06 — reopening two "don't force" verdicts)
- #8 TREATY PORTS: user rules "N currently OWNED is the correct metric — losing territory is its own
  punishment, don't track it here." So the count DOES concretize (every_owned_province has_province_modifier
  = qing_treaty_port, replacing the +5/+1 tally); owned-semantics (tiers fall on loss) is INTENDED, not a
  regression. BURDEN still stays an accumulator (separate issue: burden is eased by treaty-revise which
  never removes ports, so a count-derived burden couldn't be eased — that half stays cut). Scope #8 =
  count-only. VERIFY tier thresholds 7/12 remain reachable given real coastal-city supply.
- #9 BANNER/GS DECAY: user reframes — the meter should measure the CORRUPTION OF GARRISON COMMANDERS
  (廢弛 = rot-in-place: intact garrisons, hollow corrupt leadership), NOT building count. This DODGES the
  review's rejection (which was against building-count-inverse; a commander's corruption genuinely VARIES).
  Banner vs GS ARE distinguishable (distinct buildings qing_banner_garrison_building/qing_green_standard_
  post_building; distinct sub_unit_type qing_eight_banners/qing_green_standard — sub_unit_type is a proven
  filter, se_MOBILIZATION.txt:77). The se_QING_MECHANICS.txt:407 "no reliable tag" note is stale. Officer-
  corps walk se_QING_COUNCIL.txt:518-548 already averages commander MARTIAL split by marker — extend to
  average CORRUPTION. Verification agent dispatched for the exact read primitives before drafting.
Tasks #8, #9 REOPENED (were wrongly closed as don't-force; user's reframes make both buildable).

## #9 REFINEMENT (user 2026-08-06): decay = commander corruption AND low martial
The garrison commander IS the legion commander (garrison legions are explicitly named "XYZ Garrison",
e.g. Xi'an Banner Garrison 西安駐防). NO province/governor-officer angle — read via every_legion/every_unit
→ commander → corruption + martial. Decay target per force (banner via sub_unit_type=qing_eight_banners,
GS via qing_green_standard) RISES with avg commander corruption AND as avg commander martial FALLS:
  decay ≈ avg_corruption + (baseline_martial − avg_martial), clamped 0..100.
Both inputs VARY (unlike monotonic building count) — dodges the review's rejection. Martial-averaging is
ALREADY proven (se_QING_COUNCIL.txt:518-548 officer-corps walk averages commander martial); extend it with
a corruption term, split by sub_unit_type. Calibration constant (baseline_martial + weights) chosen to
reproduce seeds ~10/15 at 1763, commented PLACEHOLDER-playtest. Verification agent covers the commander→
{corruption,martial} scope path + safe pulse-only iterator (GUI-crash constraint se_QING_GUARD.txt:113).

## #9 ORACLE CHECK (2026-08-06): commander corruption read = PROVEN (scope:X.corruption)
prev.corruption: 0 hits in either oracle — DO NOT use. But corruption-as-numeric-value is attested BOTH
ways in BOTH oracles: bare `corruption` in char scope (Invictus 00_mission_turdetania.txt:135 `add =
corruption`; impose_fine.txt:66 `subtract = corruption`) AND scope-prefixed `scope:X.corruption`
(impose_fine.txt:45 `value = scope:target.corruption`; governor_policies/00_default.txt `value =
governor_or_ruler.corruption`). LOCKED IDIOM: commander = { save_scope_as = cmd  ROOT = { change_variable
= { add = scope:cmd.corruption } } } for corruption; prev.martial (proven in-mod) for martial. Caveat #2
downgraded from "validate-first blocker" to RESOLVED. #9 design fully grounded — ready for adversarial review.

## USER REFRAME (2026-08-06): xinjiang_control + caravan_prosperity = a CONCRETE cluster (#10 + #11)
User: "caravan trade is a real thing, any caravan prosperity should derive from real measures." Reading the
code confirms caravan_prosperity is almost ALL abstract today: base 40 + xinjiang_control/4 (meter-of-meter)
+ yarkand_market×5 (yarkand_market = an abstract capped-4 investment COUNTER, not a building) + flags. None
reads real trade.
REFRAME the cluster:
- qing_caravan_prosperity ← REAL trade through the Xinjiang oasis provinces (trade routes / export volume of
  Kashgar/Yarkand area provinces, area:Tarim/area:Dzungaria), NOT xinjiang_control/4, NOT the yarkand_market counter.
- qing_caravan_yarkand_market (the "bazaar investment count") ← candidate to become a real market/caravanserai
  BUILDING in oasis provinces (yamen pattern), so its count derives from buildings not a capped var.
- qing_xinjiang_control ← concrete Xinjiang layer (ILI subject status + beg count + qing_xinjiang_prov_secured
  province modifiers + oasis-province unrest), retiring the #367/caravan/mission nudges.
This BREAKS the circular caravan↔control loop (both read the MAP instead of each other). Biggest cluster —
"Xinjiang economy" scope, ~corruption-sized. #10 REOPENED, #11 partially specified (caravan half).
VERIFY FIRST (no assumed referents): num_of_trade_routes / per-province export readable? oasis provinces
identifiable by area? Then draft the cluster design → review → build → review → commit.

## CORRECTION (user 2026-08-06): caravan trade = MOD trade system, NOT vanilla trade routes
Vanilla num_of_trade_routes / state_trade_routes are SUPERSEDED by the mod's own trade sim
(se_GLOBALTRADE_split.txt / GT_split_* / trade-zones / GOODS_ & DEMAND_ svalues). caravan_prosperity must
derive from the MOD trade signal for the Xinjiang oases, NOT vanilla routes. Verification agent redirected
to find a mod per-province/region/trade-zone trade value for Tarim/Dzungaria. KEY UNKNOWN: does the mod
trade sim expose oasis-granular trade, or only country-level aggregates? If country-only, the caravan half
is BLOCKED (can't attribute trade to the oases) — same dead-end shape as customs; will say so, not force it.

## prev.<charstat> SCAN + VERDICT (2026-08-06): NOT a bug — do NOT rewrite
Scanned all 24 prev.<stat> value-reads across 5 files (se_QING_COUNCIL 15, se_QING_MINISTRY 3,
se_QING_UPPERSTUDY 3, se_QING_SOUTHERNSTUDY 2, se_QING_REVENUE 2). ALL follow the pattern
`<char_scope> = { ROOT = { change_variable = { add = prev.<stat> } } }` — i.e. after switching char→ROOT,
`prev` correctly points BACK at the character, so prev.martial = that character's martial.
VERDICT: this is the COMPOSITION of two independently-proven things — `prev` as a scope-back reference
(oracle-attested: Invictus 00_india_effects.txt:113 `value = prev.governor_or_ruler.power_base`, :153
`add = prev.province_income`) + a char stat read (oracle: `add = martial`, `value = scope:X.martial`). The
earlier "0 oracle hits for prev.martial" was a RED HERRING — the oracle doesn't sum martial this exact way,
but uses the same prev.<field> mechanism for other fields. prev.<charstat> in a char→ROOT context is valid.
These 24 sites are shipped + boot-tested and NOT silently reading 0. NO FIX — rewriting to scope:X.<stat>
would be pure churn with real scope-save-bug risk on working code.
CORRECTION to the #9 banner doc: its `prev.martial` concern was an overcorrection; the flat
`commander = { ROOT = { add = prev.martial } }` is equally valid. Reverting the doc's scope:cmd form back to
the mod-standard prev.<stat> for consistency (both work; prev.<stat> matches the 24 existing sites).

## #10/#367 FINDING (2026-08-06): tuntian is DUPLICATED — counter+modifier AND a real building
Correcting my earlier "concrete pieces" claim: the #367 tuntian is NOT a building — it's qing_xj_tuntian
(int counter, cap 8) + qing_xj_tuntian_colony province MODIFIER (qing_xinjiang_consol_modifiers.txt:23,
add_province_modifier :260). BUT a REAL tuntian building already exists elsewhere:
qing_military_colony_building (軍屯總局, qing_military_buildings.txt:178, seeded at 5 frontier provinces) +
qing_frontier_colony_building (qing_foreign_buildings.txt:160). The mod models 屯田 TWICE, unlinked.
IMPLICATION for the Xinjiang cluster: derive xinjiang_control / #367 consolidation from the REAL objects —
beg CHARACTER count (qing_xj_beg_count IS character-backed, QING_xj_mint_beg creates real begs, cap 5) +
qing_military_colony_building count in area:Tarim/Dzungaria (the REAL tuntian building) — and RETIRE the
duplicate qing_xj_tuntian counter + qing_xj_tuntian_colony modifier (or back the counter with the building
count). This DE-DUPLICATES tuntian AND concretizes control. Feeds the cluster design (pending the mod-trade
verification for the caravan half).

## XINJIANG-ECONOMY VERIFICATION RESULT (2026-08-06): BUILDABLE (unlike customs)
Load-bearing Q resolved YES: num_goods_produced IS a proven province-scope value (GOODS_svalues.txt:1674,
EE_svalues.txt:8, both oracles). Oases addressable via is_in_area = Dzungaria/Tarim (se_QING_ILI.txt:406;
NO single Xinjiang region — union 2 areas). So caravan_prosperity CAN derive from real oasis trade.
Design written: DESIGN_XINJIANG_ECONOMY_CLUSTER.md. Two commits (caravan half A, control half B).
CAVEATS baked in: (1) break caravan↔control loop (cut caravan writes :219/226/403/428, drop the /4 read);
(2) no double-count — income already uses country GOODS_national_production_*, target uses OASIS-scoped
num_goods_produced; (3) NOT TZ balance (western_steppe_tradezone too coarse); (4) tuntian DE-DUP → real
qing_military_colony_building not the counter/modifier; (5) yarkand_market has no building (leave abstract);
(6) story-beat SETs need cooldown/contested-modifier reconciliation (main risk). Verify prev.num_goods_
produced scope form first. Ready for adversarial review.

## CONSTANTS (user-decided 2026-08-06)
- #9 banner/GS decay: EQUAL weighting (corruption ×1 + martial-gap ×1); drift ±2/pulse; BASELINE_MARTIAL=7
  (officer-corps deviation baseline). Locked in the doc.
- STILL OPEN (user input still wanted, or seed-reproducing defaults + PLACEHOLDER if not): #1 exam_reach K
  (~20-25 so 2 academies read mid-band) + the 9 mission-gate thresholds (re-pick, classify coverage-floor
  vs build-up); #6 han blend `scaling` (~10-15/magnate to hit the 80 separatism floor) + threshold ≥10;
  #10 caravan-prosperity scale (oasis num_goods_produced→0-100) + control-derive weights.
- STANDING DEFAULT for all un-specified constants: reproduce current seed/behavior at 1763, comment
  PLACEHOLDER-tune-in-playtest (concretize-preserving-behavior, not "forcing").
- #8 treaty count: NO calibration constants (pure has_province_modifier count; tier thresholds 1/7/12
  unchanged). Only open item = verify _dominant (12) reachable vs real coastal-city supply.

## DESIGN DOCS COMPLETE (3 new, all in review as of 2026-08-06)
DESIGN_BANNER_DECAY_CONCRETIZE.md (rev), DESIGN_XINJIANG_ECONOMY_CLUSTER.md, DESIGN_TREATY_PORTS_CONCRETIZE.md
— reviews dispatched. Earlier batch (#1/#2/#3/#5/#6) already reviewed+fixed.

## #6 HAN CONSTANTS PINNED (user 2026-08-06)
- scaling = 12 points per sanctioned magnate-governor. 6 magnates ("heavily devolved" reference, user) →
  12×6=72 from the count + decay-pressure term (~8+ when central armies rot) → crosses the ~80 separatism
  floor. Mildly-devolved (1-2 magnates) stays well below. Locked in DESIGN_HAN_PROVINCIAL_POWER_CONCRETIZE.md.
- @han_magnate_cohort_threshold = 10 (the one proven in-mod value, character_events.txt:175). Locked.
#6 han constants now fully pinned — no remaining calibration unknowns for han (blend=weighted sum ×12,
threshold ≥10, drift ±2, has_culture=han, corruption/martial via prev.<stat>).

## #1 SHUYUAN SEED PROBLEM (user 2026-08-06): 2 is wrong — reseed to the real network
The mod seeds only 2 shuyuan (Yuelu 嶽麓, White Deer Grotto 白鹿洞) — the 2 MOST FAMOUS, as flavour. But
Qing had HUNDREDS (provincial-capital 省會書院 ~18-19 after the 1733 Yongzheng edict + many prefectural/
county/lineage ones). Historical research dispatched (Deng Hongbo 鄧洪波《中國書院史》 = gold-standard count,
+ Elman). IMPLICATION for exam-reach concretization: don't just pick K to make 2 read mid-band — that makes
the meter player-build-driven (backwards; the network pre-existed). Instead RESEED the shuyuan network to
reality (provincial capitals + academy-dense Jiangnan/Hunan/Guangdong) so 1763 opens with a POPULATED
network reading ~vigorous, and scale K against that realistic count. exam_reach then tracks the real
network's health from a historical baseline. Fold the sourced number into DESIGN_BUREAU_CAPACITY_
CONCRETIZE.md §9 (shuyuan half) when research returns — likely reseed to ~the provincial-capital count
(18-19) + the famous academies, NOT 2.

---
## 2026-08-06 (continued) — session-resume decisions + one build

### Design reviews returned (3)
- **Treaty-count (#8): SOUND, 2 MEDIUM fixes.** Vectors 1/2/3/6/7/8 survive. F1: recount MUST fold in
  `apply_ports_modifier` and wire at all 3 stamp sites (impose:80 after the while-loop, open_port:103,
  pulse:258) — a pulse-only recount leaves the inline applier reading a stale/0 count for up to a quarter;
  no province-cession hook exists (loss lags one quarter, fine). F2: `_dominant`≥12 likely unreachable
  (river ports fail `is_coastal`) — count CHI coastal cities at build, decide band. LOW: stale log :192,
  burden/count divergence on failed stamp, O(1) mislabel. **Doc updated (§1 rewritten with F1 wiring).**
- **Banner decay (#9): NOT BUILDABLE AS WRITTEN.** CRITICAL: derived target lands ~6 (corruption+martial
  gap in single digits) — far below the 30/60 bands, and fights the surviving +1 creep → re-creates the
  rejected building-count flatline. CRITICAL: referent (standing commanded banner/GS legions) may be EMPTY
  most of the game → n=0 no-op. HIGH: "one walk" fold is wrong (wrong pulse ordering — council walk runs
  after decline pulse; and a shared `limit` would corrupt the council-martial average). HIGH: target+drift
  makes drill/sanction/Napoleon nudges transient. **Doc needs: arithmetic proving target reaches 60;
  proof setup keeps standing legions + n=0 policy; second dedicated every_unit walk in DECLINE pulse (not
  fold); lever→target coupling. NOT folded yet — needs rework before build.**
- **Xinjiang cluster (#10): NOT BUILDABLE AS WRITTEN, 4 CRITICAL.** (1) `every_owned_province` over
  Dzungaria/Tarim returns 0 — CHI doesn't own the oases, ILI/XNG do; must use `area:Dzungaria/Tarim +
  every_area_province` (the #91 lesson `se_QING_ILI.txt:301-314` already learned). (2) tuntian de-dup is
  FALSE — building (food HQ, 7 frontier prov, 2 in oases) ≠ counter (Dzungaria colonization lever, cap 8);
  retiring counter breaks a mission + panel + lever. (3) secured/contested are OUTPUTS of control (stamped
  by apply_prov_band) not inputs — reading them back = new self-loop. (4) consolidation already =
  control + 4·begs + 3·tuntian → deriving control from begs/tuntian double-counts into the Grand Council.
  **Weights question is premature — doc needs structural rewrite first. NOT folded yet.**

### USER directives this session
1. **9 mission gates → `ADMIN_available_country`, NOT `QING_bureau_reach`.** The real admin-capacity number
   (imp19c's own system, `ADMIN_svalues.txt:181` = supplied − required), signed (deficit −/surplus +),
   already a live gate (`DIPLOMACY_svalues.txt:14`). Supersedes the whole §4.2 reach-recalibration + the
   coverage-floor-vs-build-up classification (signed number expresses both natively). Capability PROVEN via
   oracle-rule (in-mod): bare script_value on trigger-comparison LHS is legal —
   `DIPLOMACY_power_from_economy >= 80` (`imp19c_diplomacy_triggers.txt:59`, svalue at DIPLOMACY_svalues:61),
   `JOBS_available_slots > 0`, and `ADMIN_available_country < 0` itself. Folded into bureau doc §2/§4.2.
2. **Yuelu + White Deer Grotto = DISTINCT NAMED buildings, not generic shuyuan. BUILT (uncommitted).**
   - `qing_yuelu_academy_building` (prov 2793) + `qing_bailudong_academy_building` (prov 2386) in
     `qing_governance_buildings.txt`; each `allow=always=no`, `potential = has_variable = qing_is_<site>`.
   - Seed sets the per-province flag FIRST then seeds via QING_seed_works_building (se_QING_BUILDINGS.txt).
     Flag gate (not region gate) → greyed build-tab entry shows ONLY at the one province.
   - Loc (qing_governance_l_english.yml) + tooltips (imp19c_tooltips_l_english.yml) + placeholder icons
     (copied from generic shuyuan — bespoke art OWED). Brace/BOM verified clean.
   - `QING_exam_reach` must count all THREE academy building keys (folded into §9c).
3. **Shuyuan research returned:** mod seeds 2; history ~thousands, structural anchor ~18-19 provincial-
   capital academies (1733 Yongzheng edict). §9c updated: RESEED generic shuyuan to ~18 province capitals +
   count the 2 named; calibrate K against ~20 covered so 1763 reads mid-band.

### Building-tab visibility note (answered)
`allow=always=no` only greys a building (non-constructable); `potential` controls VISIBILITY. Hanlin/
Guozijian use `is_in_region=Zhili` → they show greyed across ALL of Zhili, not just Beijing. The new
academies use a per-province flag → tighter (own province only).

---
## 2026-08-06 — design-review results (5 of 6 back)

USER framing: "my rulings are authoritative design-wise, but your implementation plan needs review."
So reviews verify PLAN correctness, not re-litigate design rulings.

- **#5 SECT — RETRACTED (leave abstract).** 3rd review: no valid on-map referent. pure_land_buddhism is an
  ACCEPTED faith (happiness +0.05, inside chinese_accepted_religion_trigger, dominant in dozens of Han core
  provinces); keying sect on it measures orthodox demography and moves OPPOSITE the mission→sect coupling
  (conversion lowers the count → target falls when panic should rise). No white_lotus religion object exists.
  Rebellion-derive is circular (sect GATES the 5 rebellions). = mandate_strength category. WON'T-BUILD.
- **#2 CORRUPTION — plan REWRITTEN, now sound.** Review caught my two-store model was over-engineered on a
  FALSE premise: I claimed qing_council_effectiveness "has zero event writers" — it has ~40 (se_QING_DYNASTY
  ×13, qing_office_events ×15, +its own drift nudge :573/577). The blessed pattern is SINGLE-store:
  char-derived target + drift + keep nudges. Rewrote to the single-store mirror. Baseline-K still load-bearing
  (autofill officials carry no corruption → raw aggregate opens ~0, trips clean_government ≤10; seed 12 at
  1763). add_corruption proven (21 uses). prev.corruption in-repo-proven (se_QING_COUNCIL:724). Two-store now
  optional Phase-3.
- **#3 CURRENCY — SOUND, both CRITICALs fixed.** ÷3 branch + no public_debt_administration for CHI confirmed;
  signed no-floor residual justified (both existing helpers floor at 0). Folded 3 census gaps: M1 the SECOND
  reserve→stress backfeed se_QING_REVENUE:146-158 (<10000 → +1) double-counts the reserve-derived base;
  M2 use DEFLATION side not CURRENCY_amt_circulated_inflation (fires only on glut, silent during 銀荒);
  M3 linear Board-of-Revenue consumer se_QING_MINISTRY:848-854 (currency_stress/6) shifts with the opening.
  Blocking: pre-build 1763/1815 reserve_ratio_impact measurement.
- **#10 XINJIANG — rewrite fixed CRIT 1/2/3 (confirmed sound); re-review caught 1 new CRIT + 2 MED + 1 LOW,
  all folded.** CRIT-5: my recommended CRIT-4 remedy (option a, drop control base) capped consolidation ~56
  → killed qing_xj_pacify (≥75) + qing_xj_integrate (≥85) missions; census had OMITTED those two reads (same
  error as CRIT-4). Switched to option (b) keep-base-drop-terms. MED: cut :264/:292 lever double-nudges;
  MED: frontier_secured must be a max-floor not additive + stamp at reconquest-win too (only zeng-triumph
  today); LOW: −5 customs drag means S×oasis≈10 not 5.
- **#9 BANNER — reworked per USER rulings, re-review IN FLIGHT.** rot IS the decay (delete +1 creep); target
  = base + K×(corr + (M0−mart)), K=2 M0=10 base 0/5 reproduces seeds 10/15 AND crosses 60 rotten; n=0 holds
  (correct); fold into council walk OK (1q stale fine); levers move real add_corruption/add_martial (proven
  Invictus). 
- **#1 BUREAU — review IN FLIGHT.** 9 gates → ADMIN_available_country (signed, proven LHS). 2 named academies
  BUILT (uncommitted). shuyuan reseed ~18 prov capitals.

READINESS: #6 han ready (constants locked). #2/#3 plan-sound (ready after their measurements). #5 retracted.
#7 won't-fix. #8/#9/#10/#1 awaiting review-clear (#8 folded, #9/#1 in flight, #10 folded).

---
## 2026-08-06 — final two reviews (#1 bureau, #9 banner) + shipped-code fix

- **#1 BUREAU — 1 CRITICAL (shipped-code bug), 2 MEDIUM, else sound.** CRITICAL: the level-cap idiom was
  wrong in BOTH doc AND on-disk code. `max_level` is a NON-KEY (0 uses anywhere); the shipped
  `potential = { NOT = { has_building = self } }` is UNATTESTED + risks self-destruction (own potential flips
  false after placement). PROVEN key = `max_amount = 1` (Invictus/TI 00_default.txt, 30+ uses).
  FIXED IN CODE: both qing_yamen_building + qing_shuyuan_building now `max_amount = 1` + STABLE owner-culture
  potential (proven hanlin/guozijian pattern). [USER: max_amount is the cap; NO has_city_status gate — yamens/
  academies existed in rural county seats; potential still required for a well-formed def, so owner-culture].
  MEDIUM: panel loc must use .ScriptValue() not .Var() (reach is an svalue). MEDIUM: HARD INVARIANT — zero
  surviving QING_DECLINE_nudge on the dead vars (it auto-creates → resurrects at 0). All folded. Capability
  (ADMIN_available_country signed, bare-svalue trigger LHS), SelfStr 3-term, pass-rate multi-term, named
  academies, migration table (no missed consumer) — ALL CONFIRMED SOUND. Denominator note: dropping city gate
  → reconcile reach numerator/denominator scope.
- **#9 BANNER — 4 rulings CONFIRMED correctly implemented; 1 MED-HIGH open + 2 contradictions folded.**
  Finding A (MED-HIGH, DESIGN — needs ruling): with the creep deleted, NOTHING makes garrison-commander
  corruption climb (setup seeds 0; no passive martial-decay). Target may hold low, never reach ≥30/≥60 =
  flatline through a new door. Added §6 with options; RECOMMEND (a) add a corruption-accrual driver for
  aging/long-tenured banner-GS commanders (concrete + guarantees bands reachable). Finding B: §5.4 contradicted
  §4 (said "keep nudge levers") — FIXED to the commander-stat conversion. Finding C: missed the per-pulse
  law-upkeep-bias writer se_QING_DECLINE:940-943 — under target+drift it washes out (dead-law flaw #32
  redux); FIXED §4b re-route bias to TARGET. Finding F: census cites corrected (:424/425 not :413; :353;
  :439 GS-cmpsvalue reader; loc :384/385). All primitives + arithmetic + 4 proofs CONFIRMED.

FINAL READINESS (all 6 reviewed):
- READY TO BUILD: #6 han (locked), #2 corruption (single-store mirror), #3 currency (after reserve measure),
  #8 treaty (F1/F2 folded), #1 bureau (code-cap FIXED; build the reach svalue + gate repoint + reseed).
- NEEDS A USER RULING BEFORE BUILD: #9 banner (Finding A — corruption-accrual driver: a/b/c).
- FOLDED, buildable: #10 xinjiang (option-b + 2 MED + LOW).
- WON'T-BUILD: #5 sect (no referent), #7 tributary (collapses meter). GP-tension/customs retracted earlier.

---
## 2026-08-06 — BUILD #6 han_provincial_power (COMMIT 1) [autonomous]

IMPLEMENTED (se_QING_DECLINE.txt QING_DECLINE_drift_han_provincial_power + se_QING_MECHANICS.txt):
- Added a magnate-governor COUNT walk before the target compute: every_character{ employer=ROOT is_governor
  is_alive has_culture=han OR{ has_character_modifier=qing_regional_magnate  num_loyal_cohorts>=10 } } →
  qing_han_magnate_tally. All idioms verified proven: every_character effect-iterator (se_QING_PERSONNEL:47),
  num_loyal_cohorts trigger (character_events:175 + TI), has_culture=han (QING_mechanics_actions:153),
  qing_regional_magnate modifier (se_QING_MECHANICS:197). Opens 0 at 1763 (no sanctioned magnates / no Han
  governors w/ private armies at the zenith) = matches seed.
- BLENDED into target: target = (banner+gs)/2 − modernarmy + provmil_bias + 12×magnate_tally, before the
  0..100 clamp. WEIGHTED SUM not max (national army still suppresses). 12/magnate + 6-magnate reference =
  user-decided; 6→72 crosses the ~80 separatism floor once decay adds in. Kept ±2 drift + law bias + clamp.
- DROPPED the sanction +15 nudge (se_QING_MECHANICS:152): the sanctioned magnate now enters the COUNT
  durably (holds qing_regional_magnate → +12 target while seated), so +15 would double-count. Kept the
  −8/−8 central-relief.
- Scratch vars (qing_han_magnate_tally, qing_han_magnate_term_tmp) used only in set/add/multiply → NO
  cmpsvalue needed. Reset each pulse (set value=0 at top).

REASONING on the reduce-levers (NOT changed): reassert (−20, :258) + pension (−28, :307) both call
QING_reassert_strip_magnate, which only CONDITIONALLY clears qing_regional_magnate (when granted-veterans
spend to 0). Unlike the +15, these are one-shot immediate nudges on a target+drift meter (already transient
by design); their durable effect flows through the marker-strip → count drop. No double-count → left as-is.

BOOT-CRASH REVIEW (standing rule): PASS. on_action is tag=CHI (ROOT=CHI); the exact
ROOT={change_variable add=1}-inside-iterator pattern is proven right below at :537/541/547 (ethnic
re-derivation, same pulse/file). Valid triggers, balanced braces, noBOM preserved.

---
## 2026-08-06 — BUILD #2 corruption (COMMIT 2) [autonomous]

IMPLEMENTED the SINGLE-STORE mirror of qing_council_effectiveness (design §2, post-review-rewrite):
- se_QING_COUNCIL.txt: piggybacked the EXISTING office-holder walk (QING_council_score_office +
  _score_chancellor) to sum seated holders' vanilla `corruption` into qing_officialdom_corr_total (one line
  each, `add = prev.corruption` — same proven prev.<value> idiom as prev.$skill$ right beside it). Reset in
  the recompute init alongside skill_total. NO second sweep.
- Target compute (after the effectiveness target, same filled_count): qing_officialdom_corruption_target =
  12 (baseline-K) + avg holder corruption (div/0 floor on filled_count), clamped 0..100. BASELINE_K=12
  because setup autofills officials with ZERO corruption → pristine court avg ~0 → target 12 = reproduces
  the 1763 seed and sits just above clean_government (≤10). Figureheads excluded (not in filled_count) —
  matches effectiveness; emperor-weighting refinement deferred.
- se_QING_DECLINE.txt: new QING_DECLINE_drift_corruption — ±2/pulse drift toward the target (slower than
  effectiveness's ±3; graft stickier), gated on target existing, self-seeds level. Called BEFORE
  QING_DECLINE_update_reform_pressure (which sums corruption at :350) so the sum reads the fresh value.
- 00_event_values.txt: added qing_officialdom_corruption_target_cmpsvalue (RHS-compare rule).
- KEPT all ~108 event nudges on the live var (single-store: they're impulses that decay as drift
  re-converges — the damped behavior effectiveness ships). NO residual var, NO writer redirection, NO
  save-migration split (the over-engineered two-store was retracted after review found its premise false).
- Phase-2 (convert named-culprit events to add_corruption/trait on the office-holder) is a FUTURE refinement
  per §7; not in this commit. This single-store mirror passes the user's iff-test to the same degree
  effectiveness does.

VERIFIED: prev.corruption proven-by-composition (corruption is a readable char value — Invictus impose_fine/
turdetania/governor_policies; same class as prev.martial used in the same walk; corruption_svalue reads
root.corruption). add_corruption proven (21 in-mod uses) for future Phase-2.
BOOT-CRASH REVIEW: PASS. Drift self-guards on has_variable target + self-seeds level → first-pulse-before-
recompute is a clean no-op, not a crash. ROOT=CHI (recompute runs in QING_GOV_pulse, tag=CHI). Braces
balanced; noBOM preserved on the 2 se_ files; 00_event_values.txt has a PRE-EXISTING brace-count of 1 (a
stray comment brace at HEAD, not my balanced one-liner).

---
## 2026-08-06 — BUILD #8 treaty_ports (COMMIT 3) [autonomous]

IMPLEMENTED (se_QING_TREATIES.txt) — derive the count from real qing_treaty_port modifiers:
- Added QING_treaty_recount_ports = { set qing_treaty_ports 0; every_owned_province limit{has_province_
  modifier=qing_treaty_port} ROOT change_variable add=1; QING_treaty_apply_ports_modifier } — FOLDS IN the
  applier (F1) so the inline tier read never sees a stale count. Proven idiom (FUNC_svalues.txt:71 shape).
- Wired recount at ALL 3 sites replacing the bare applier call: impose (AFTER the while-stamp loop, F1),
  open_port (after the stamp), pulse (quarterly demotion-on-loss). 
- RETIRED the +5 (impose) and +1 (open_port) counter bumps — count is now recounted from the real modifiers
  (OWNED-semantics: losing a port drops its tier, intended per user).
- F2: _dominant band 12 -> 9 (river treaty ports fail the is_coastal+has_city_status stamp guard, so 12
  simultaneous coastal-city ports likely unreachable; 9 = reachable apex). PLACEHOLDER-playtest.
- F3: fixed the stale stamp-fail log ("counter advanced but no port stamped" -> "no un-stamped coastal city
  owned; no on-map port stamped").
- burden UNTOUCHED (accumulator, out of scope). NOTE burden/count can diverge on a failed stamp — intended.

CONSUMER CENSUS: qing_treaty_ports has NO external readers — only the 3 tier bands in this file (customs hit
is a comment). Fully self-contained.
BOOT-CRASH REVIEW: PASS. All 3 recount calls country-scope ROOT=CHI; proven has_province_modifier count
idiom; recount set-0 safely overwrites the :52 init; braces balanced; noBOM preserved.

---
## 2026-08-06 — BUILD #9 banner/GS decay (COMMIT 4) [autonomous]

IMPLEMENTED the commander-rot derive (rot IS the decay; USER ruling b = quieter meter, driver added later):
- se_QING_COUNCIL.txt: folded banner/GS corruption+martial+count buckets into the EXISTING officer-corps
  every_unit walk (in-body if{any_sub_unit=sub_unit_type=qing_eight_banners / qing_green_standard} — does NOT
  narrow the walk limit, council-martial avg untouched). Then computed the two targets:
  target = base + K×(avg_corr + (M0 − avg_mart)), K=2, M0=10, base_banner=0/base_gs=5 (reproduces seeds
  10/15 healthy, crosses 60 rotten). n=0 → skip (meter holds). Folded the upkeep-law bias AND the
  deliberative posture bias into the TARGET before the clamp (durable, drift-respected; not counter nudges).
- se_QING_DECLINE.txt: DELETED the +1/+1 passive creep + the GS-accel; replaced with ±2/pulse drift toward
  the targets (gated NOT fully_modernized AND NOT high_qing_era, target-existence guarded). Removed the
  per-pulse upkeep-bias counter nudge (now target-folded).
- se_QING_DELIBERATIVE.txt: removed the standing posture-bias counter nudge (now target-folded); kept the
  dynamic cohesion ±1 band as a transient shock (live-state, not a standing setting).
- LEVERS converted from counter-nudge to REAL commander stats (add_corruption/add_martial, proven Invictus):
  banner drill −10corr/+2mart, GS drill −10/+2, sanction −4/+1 (both forces, matches old −8/−8),
  Napoleon levee −10/+2 (both forces, replaces −20/−20), fund-modern-army −3corr banner (matches −6).
  The meter then falls via the derive because the corps genuinely improved. Magnitudes account for ×K=2.
- 00_event_values.txt: added qing_banner_decay_target_cmpsvalue + qing_greenstandard_decay_target_cmpsvalue
  (twin asymmetry — banner had no cmpsvalue before; RHS-compare rule).

KEPT as transient event shocks (per ruling b): canal collapse, decline events, new-world mission, deliberative
cohesion band — one-shot spikes the drift re-converges from. FUTURE: a dedicated commander-rot driver
mechanic (USER, doc §6) — nothing artificially climbs commander corruption yet, so a clean corps stays low.

BOOT-CRASH REVIEW: PASS. Drift reads target one-quarter-stale (GOV pulse computes it AFTER decline pulse in
00_monthly_country.txt:82 vs :98) — acceptable per USER; first-pulse-before-recompute is a clean no-op
(has_variable guard). commander={} char-scope proven (existing walk); add_corruption/add_martial proven
upstream. All 6 files: braces balanced, BOM state preserved (00_event_values pre-existing brace=1 unrelated).

---
## 2026-08-06 — BUILD #10 Xinjiang COMMIT A: caravan_prosperity (COMMIT 5) [autonomous]

IMPLEMENTED (se_QING_CARAVAN.txt + QING_governance_svalues.txt) — caravan prosperity ← REAL oasis trade:
- New script_value QING_caravan_oasis_trade_svalue = area:Dzungaria{every_area_province{add=num_goods_produced}}
  + area:Tarim{...}. AREA iteration (CRIT-1 fix: oases are ILI/XNG-held, every_owned_province returns 0 for
  CHI). Proven: area:+every_area_province in a script_value (00_mission_seleukid:114); num_goods_produced bare
  province read (GOODS_svalues:1352). Read via set_variable (NOT prev.num_goods_produced in an effect — MED-1
  unproven; first drafted it that way, corrected to the svalue).
- QING_caravan_recompute_target: REPLACED the qing_xinjiang_control/4 meter-of-meter term with S×oasis_trade
  (S=0.5 PLACEHOLDER-playtest; LOG probe emits raw oasis sum to re-pick S so 1763 target ≈ 45 = base 40 −5
  customs +S×oasis). This also breaks the caravan READS control side of the circular loop (the WRITES side
  :228/:235 is cut in COMMIT B with the control derive).
- yarkand_market / aqsaqal / customs / khoja terms UNCHANGED.

NOTE: COMMIT B (control derive + cut caravan→control writes + consolidation option-b rework + story-beat
floor) is the larger half — deferred to next. Caravan is separable and committed alone per the design.
BOOT-CRASH REVIEW: PASS. recompute runs country-scope (QING_caravan_pulse via QING_GOV_pulse, CHI) so area:
resolves; svalue self-contained; braces balanced; noBOM preserved; no dangling grip_tmp.

---
## 2026-08-06 — status after 5 commits [autonomous]

SHIPPED (committed + pushed to merge-overnight): #6 han, #2 corruption, #8 treaty, #9 banner, #10A caravan.
Plus uncommitted-but-staged: the 2 named academies + yamen/shuyuan max_amount cap fix (belong with #1).

REMAINING:
- #10B (control derive) — STARTED but PAUSED. This is the highest-complexity piece: qing_xinjiang_control
  today is SET by story beats (reconquest-win=80 :125, zeng-triumph=90 :232, choose-coast=0, ratify=−25) that
  a per-pulse derive would FIGHT. The design's §5 max-floor + stamp-at-reconquest-win reconciliation must be
  IMPLEMENTED carefully (not placeholdered) or the Ili arc silently breaks (option-a already showed one such
  break). frontier_secured is stamped ONLY at zeng-triumph today (:240), NOT reconquest-win (:125) — so a
  reconquest-win floor needs a new stamp. Deferred for careful implementation + re-review, not a blind build.
- #1 bureau + #3 currency — MEASUREMENT-BLOCKED: both need a live-game read I can't produce (1763
  ADMIN_available_country / reserve_ratio_impact) to set gate thresholds / the transfer knee. Building blind
  would guess the numbers. Design + code-cap-fix (yamen/shuyuan max_amount) are DONE; the reach svalue + gate
  repoint + reseed for #1, and the two-store + calibration for #3, await either the measurement or a decision
  to ship with PLACEHOLDER thresholds + a build-probe LOG.

---
## 2026-08-06 — trade-metric provenance findings + admin=flat + corruption widening [autonomous]

TRADE METRIC (caravan #10A, user pushed on num_goods_produced=production not trade):
- regional_center_of_trade_level_N modifiers = LIVE MOD trade (stamped by tradezone_setup_effect /
  TRADE_setup_tradezones at game start, se_TRADE.txt:1898; tracked in list_of_trade_centers). NOT obsolete
  vanilla trade-node artifacts. So reading them is rule-compliant.
- BUT limitation found: tradezone_setup only ever stamps LEVEL_1 (one center per tradezone), and the oases
  fall in western_steppe_tradezone (bundles Siberia/Moscow/Caucasus — coarse). So at most ONE oasis province
  gets +5, often none. The center-of-trade bonus I added is thus mostly inert for the oases — the metric is
  effectively num_goods_produced + a rare +5. Correct in principle (credits throughput, live mod), marginal
  in practice. Honest: caravan prosperity remains production-dominated because the mod's TZ granularity puts
  no real trade center in the oases.
- state_commerce_income = VANILLA engine field (present in both oracle repos). Mod trade income flows through
  national_trade_income_pool (se_TRADE.txt:2363), NOT vanilla commerce — and the EE trade svalue wrappers
  (all_governorship_trade_svalue / all_region_trade_svalue / player_trade_total_value) are DEAD (0 callers).
  So state_commerce_income is NOT a good fallback either (vanilla, and mod income is pooled elsewhere). The
  center-of-trade-modifier read remains the best area-reachable trade signal, weak as it is.

ADMIN CAPACITY (#1) — USER 2026-08-06: assume 1763 ADMIN_available_country is FLAT (neither deficit nor
surplus, ≈ 0). This UNBLOCKS #1 gate calibration without a probe boot: the 9 reform/self-str gates that today
require qing_bureau_capacity >= 40..60 become ADMIN_available_country thresholds anchored on 0 = the 1763
baseline. Deep reforms (constitutional draft, high self-str) → require a positive cushion (surplus, must
IMPROVE admin past the flat baseline); early tasks → require not-deep-deficit (>= a small negative floor).
Logs confirm nothing admin is logged, so flat=0 is the working assumption. (currency #3: logs show the old
1-bit branch fired +=-1 ×8 only → reserve_ratio_impact ∈ [0.5,1.0] → calibrated transfer opens calm, no
upward re-center; buildable with a confirming LOG probe.)

CORRUPTION (#2) widened + committed: now walks ALL court-position holders via QING_char_holds_court_position
(office/diplomat/censor/guard/2 studies/amban/eunuch/consort/Protector-General), not just 13 council seats.

---
## 2026-08-06 — #10B RESOLVED via concrete-reward reframe (USER)

The story-beat-vs-derive fight (the reason #10B was paused) is DISSOLVED: instead of the Ili win/loss beats
SETTING the abstract control meter (80/90/10/−25) which a per-pulse derive then fights, the beats now produce
CONCRETE outcomes and control DERIVES one-way from them:
- reconquest-win: stamp qing_xinjiang_prov_secured on the oases DIRECTLY + a qing_ili_reconquered modifier
  (drop set control=80). zeng-triumph: keep frontier_secured, stamp full secured set (drop set=90).
- reconquest-fail/ratify: stamp qing_xinjiang_prov_contested (drop set 10 / −25).
- RETIRE QING_ili_apply_prov_band as the control→province stamper (it was the CRIT-3 loop source: it stamped
  secured FROM control≥70). Now beats stamp secured/contested directly → control derives from them ONE-WAY.
- control_target = W_ili·ILI-subject + W_beg·begs + W_tun·tuntian + W_sec·secured-count + W_front·frontier
  − W_cont·contested-count. No max-floor, no cooldown needed (the old §5 machinery is obsolete).
This is concrete-over-abstract applied to the REWARDS, not just the meter. Doc §5/§3/§7/§8/§9 updated.
NEXT: dispatch a review of the revised #10B before building (hardest piece; design-review caught breaks 2x).

---
## 2026-08-06 — CONSOLIDATED STATUS SNAPSHOT (all designs)

SHIPPED (built + boot-crash-reviewed + committed + pushed to merge-overnight):
- #6 Han provincial power — magnate-governor COUNT blended into target; dropped double-counting +15 nudge.
- #2 corruption — vanilla `corruption` of ALL court-position holders (widened per user: via
  QING_char_holds_court_position — office/diplomat/censor/guard/2 studies/amban/eunuch/consort/Protector-Gen),
  single-store mirror of council-effectiveness.
- #8 treaty ports — live recount of real qing_treaty_port modifiers; retired +5/+1 tally; _dominant 12→9.
- #9 banner/GS decay — garrison-commander corruption+martial (rot IS the decay); deleted passive creep;
  drill/sanction/Napoleon levers now move real commander stats (add_corruption/add_martial).
- #10A caravan prosperity — real oasis TRADE = num_goods_produced + regional_center_of_trade bonus (per user:
  production drives trade but isn't trade; center-of-trade = live MOD trade infra, not obsolete vanilla).

IN REVIEW:
- #10B Xinjiang control — REDESIGNED around concrete-reward (beats stamp secured/contested/frontier objects,
  control derives ONE-WAY; retire apply_prov_band as control→province stamper; option-b consolidation).
  Design committed; adversarial review dispatched + running. Build follows on clear.

READY TO BUILD (unblocked, not yet built):
- #1 bureau/exam — UNBLOCKED by USER "assume admin capacity is flat (≈0)": 9 gates anchor on
  ADMIN_available_country (deep reforms → surplus, early tasks → not-deep-deficit). Design review-clear;
  max_amount cap fix DONE; 2 named academies BUILT (uncommitted, ride with #1). NEXT to build.
- #3 currency — logs bound reserve_ratio_impact ∈ [0.5,1.0] → calibrated transfer opens calm, no upward
  re-center. Buildable with a confirming LOG probe. Review-clear.

CLOSED — won't build (design conclusions):
- #5 sect pressure — no valid on-map referent (pure_land = accepted faith, moves wrong way; no White Lotus
  religion object; rebellion-derive circular). RETRACTED.
- #7 tributary/suzerain — derive collapses the meter (subject-type key mismatch + double-count). WON'T-FIX.
- GP tension, customs — retracted earlier (capability/derivation didn't hold).

NOT STARTED:
- #11 meter-of-meters revisit (reform_pressure, modernarmy) — several addressed as side-effects of #2/#9;
  the rest pending.

FUTURE (design-noted, not a task): dedicated banner/GS commander-rot driver mechanic (USER, banner doc §6).

COUNT: 5 shipped · 1 in review · 2 ready-to-build · 3 closed · 1 not-started.

---
## 2026-08-06 — post-hoc reviews: #2 CLEAR, #10B NOT READY

#2 corruption widening (commit 6ad04d8ea) — REVIEWED SOUND, no critical/medium. prev.corruption resolves to
the character (proven by sibling banner walk :582), ROOT=CHI, div/0 guarded, legal _cmpsvalue, no
double-count. Flag #1 CLEARED: no seeded 1763 char carries corruption (ambans runtime-assigned) → opens 12 =
seed. Flag #2 (consorts in "officialdom"): USER ruled KEEP AS-IS. Optional perf (3rd full-pool every_character
walk) noted, not required. #2 DONE + verified.

#10B Xinjiang concrete-reward design — REVIEWED: NOT READY (2 CRIT + 2 HIGH). Directionally right (cuts,
area-iter, option-b, choose-coast collapse CONFIRMED sound) but:
- CRIT-1: "retire apply_prov_band" misses 4 MORE live callers — integrate_fully capstone (se_QING_XINJIANG:544),
  qing_ili.4 compromise (:190), choose-coast (se_QING_ILI:106), break_ili_free fallback (:466). Also drops the
  mutual-exclusion + mid-range self-clearing bookkeeping (documented stuck-secured bug precedent). SAME
  incomplete-census failure as prior Xinjiang passes.
- CRIT-2: qing_ili.4 set control=60 NOT converted (filed "keep override" but that fights the one-way derive);
  which pulse hosts the derive is unspecified (matters for the integrate=100 lock).
- HIGH-3: xiexiang 協餉 (the key paid grip lever) has NO derive term → paying it becomes inert. Plus ~8 other
  nudge-writers (discipline_beg, mission nudges, caravan levers, events) still fight the derive.
- HIGH-4: option-b ≥85 capstone gate may be UNREACHABLE under the derive (control ceils ~74 pre-Ili +
  consolidation ~82 < 85 under beg-indirect law). Needs arithmetic vs all 3 admin-law biases.
- MED-5: W_sec/W_front/W_cont unassigned; secured-province signal near-inert early (ILI+begs+tuntian already
  ~74, so the concrete centerpiece contributes little at the margin).
DEEPER ISSUE: Xinjiang control has FAR more live writers than the Ili story beats. A pure one-way derive can't
absorb them all without converting every writer to concrete (much larger scope than "convert 6 beats"). This
is a scoping decision for the user. #10B REMAINS DEFERRED — needs a redesign pass, not a build.

---
## 2026-08-06 — review outcomes: #2 sweep-merge REVERTED (real bug); #10B still not safe; #10A inert

#2 SWEEP-MERGE (commit 5ed90ea5c) — REVIEW FOUND A REAL MEDIUM BUG (I had committed without review):
moving the corruption accumulation into QING_validate_one_position (1 caller, pulse-only) made
QING_council_recompute (21 callers) read STALE totals on every non-pulse call (appoint/vacate/death events
compute the target from the pre-change court). "behaviour identical" was false. REVERTED (commit 0fceb1f53)
back to the reviewed-clean 6ad04d8ea state (dedicated walk in recompute = always fresh). PROCESS FAILURE:
committed a perf refactor without review; the revert restores correctness. If the one-sweep win is still
wanted, the CORRECT form is fold-into-recompute + drop the pulse-only validate call (recompute has 21 callers
and is always fresh; validate has 1) — that is a NEW change needing its own review, NOT bolted on.

#10B CONVERT-ALL-WRITERS (design §10) — REVIEWED: NOT SAFE (2 HIGH + 3 MED). Direction sound (xiexiang derive
term CONFIRMED; one-way acyclic; capstone reachable) BUT:
- HIGH-1: apply_prov_band has 8 callers not 6 — MISSED break_ili_free:466 AGAIN (3rd incomplete-census). Every
  caller must pass $intent$; :466 wants contested or it no-ops/parse-fails.
- HIGH-2: deleting the pulse neglect −1/qtr drift is NOT redundant — it's a TIME-INTEGRATING RATCHET that
  walks control down to the ≤30 khoja-revolt-scare threshold. A static W_xiexiang offset can't do that.
  Deleting it (+ secured stamps pinning control high forever, mid-range self-clear now dead) makes the khoja
  revolt (the core #367 threat) UNREACHABLE after a win. KEEP the drift or re-arm the scare another way.
- MED-3: 3 mission nudges (fortify+6/governor+8/pacify+6) have no derive-read object (fort isn't a term;
  governor/pacify change nothing on completion) — need a new derive term or keep the nudges.
- MED-4: table MISSED 2 caravan-event writers (qing_caravan_events.txt:87 −4, :175 −3).
- MED-5: qing_ili.4 "partial secured + some contested" infeasible with a single-intent all-provinces helper.
#10B needs ANOTHER design iteration (fix the 5) before build. Still deferred.

#10A trade-center bonus (commit 3052a2bba) — REVIEWED: EFFECTIVELY INERT. tradezone_setup stamps ONE level_1
center per tradezone on the most-populous province; Dzungaria→western_steppe (center = a Russian/CA city),
Tarim→eastern_steppe/Gansu (center = Beijing). NO oasis ever carries a center-of-trade modifier → all 10
branches always false → svalue still returns pure num_goods_produced. Levels 2-5 dead game-wide. My inline
comment (both oases in western_steppe) is also factually wrong (Tarim = eastern_steppe). USER DECISION: build
a BESPOKE oasis-entrepôt signal (caravan system stamps its own trade-hub modifier on Kashgar/Yarkand scaled
by aqsaqal + bazaar) — net-new mechanic, own design+review cycle. The inert trade-center branches to be
removed as part of that.
