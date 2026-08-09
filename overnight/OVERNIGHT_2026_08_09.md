# Overnight run — 2026-08-09

Autonomous backlog run under the `imp19c-overnight` skill. Branch `merge-overnight`, all
commits authored+committed by freekumquats. Design-first + adversarial review for larger
tasks; small mechanical edits go straight to code-review → commit → push. No deferrals.

---

## #23 — Currency / economy deep fix (silver-price oscillation) — DONE

Worked ahead of this doc under the strict diagnose→design→implement iterative protocol
(each stage adversarially reviewed). Full trail lives in `audits/AUDIT_CURRENCY_23.md`
(not here, per instruction). Summary:

- **Root cause:** the shared `sqrt` scripted effect (`se_ECON_functional.txt`, "Tobbzn's
  method") was mathematically broken — (1) loop recurrence computed `y = x/param` instead
  of the Babylonian invariant `y = param/x` (input>1 decayed x→~0); (2) signed epsilon
  guard skipped the loop entirely for input<1. Together a discontinuity at base=1.0 that
  rail-slammed gbip ~0.003⇄0.88 every quarter — the sawtooth. CHI peg is a verified
  passthrough of gbip.
- **Fix:** corrected recurrence `y=param/x` + bounded `while { count=12 }` loop (fixed-point
  safe; epsilon guard could 2-cycle forever under 3-decimal fixed point). Seed x=param, y=1.
  Sole caller = the gbip write at `se_GLOBALTRADE_split.txt:2701` (guarded `if base>0`), so
  blast radius = gbip only.
- **Status:** implemented, code-reviewed PASS, committed `14c9ed899`, pushed. ACCEPTANCE is
  boot-gated on the user's separate machine: re-run `tools/curx_analyze.py` on the new
  debug.log — gbip row must be flat, inflation~0, cost-of-living ~5 taels/adult/yr yardstick.

---

## #6 / #10 / #11 / #14 — small trait + localization edits — DONE

Four independent small tasks bundled into one focused commit `f5ef9daac`.

- **#6** — added missing `chinese_emperor` status-trait localization (title "Son of Heaven
  (天子)" + desc) to `imp19traits_l_english.yml`. The trait is granted to Qing rulers in
  `setup/characters/00_Qing.txt` (6 sites) but had no card string.
- **#10** — gave the six CIVIL exam-degree traits a modest `finesse` boost in
  `common/traits/00_imp19c.txt`: shengyuan=1, juren=1, gongshi=2, jinshi=3, hanlin=4,
  fanyi_jinshi=3. Monotonic-with-prestige, mirrors the existing military 武 martial 1..4
  ladder and the holding_income_modifier gradient.
- **#11** — added `value_civilization_cap` / `value_civilization_increase` interface labels
  to `interface_l_english.yml`. These are declared province-value modifier icons
  (`00_modifier_icons.txt:2716/2720`) that were rendering as raw keys.
- **#14** — added `monthly_character_popularity` to the two disgrace traits (disgraced=-0.1,
  completely_disgraced=-0.25), alongside the existing fam-prestige drag. Magnitudes match
  existing scheme/event ranges; hard disgrace ranks below the lesser taint.

**Key decision (EOL discipline):** `00_imp19c.txt` has MIXED line endings at HEAD (CRLF
civil-degree region, LF disgrace region). My first Edit-tool pass normalized everything to
CRLF, ballooning the diffstat to 346 lines of pure EOL churn. Reverted and re-applied via a
byte-precise script that preserves each region's native EOL — final diff is exactly 8
added lines, 0 deletions, no churn (verified `git diff --ignore-cr-at-eol --numstat` == plain).

**Review:** code-review agent — CLEAN, no findings. Confirmed `finesse` and
`monthly_character_popularity` are both legal inside status/health trait blocks (direct
precedent: freemason/banker finesse, 00_health.txt monthly_character_popularity), braces
70/70, loc keys match engine references, no EOL/BOM churn.

**Commit:** `f5ef9daac`, pushed to merge-overnight.

---

## #1 — Rescale Qing player treasury costs into the hundreds (cap ~1200) — DONE

**What:** Qing pay-for-benefit events/ministry-buttons charged gold in the **tens** (modal
30–80), noise against a treasury seeded at ~6 years' running costs. Lift them into the
hundreds so a spend choice is a real fiscal decision.

**What I did:** one closed-form monotonic map `new = round5(40 × sqrt(old))` applied to the
whole player-initiated Qing spend surface via `tools/treasury_rescale.py` (dry-run manifest →
eyeball → `--apply`). Sample: 10→125, 30→220, 60→310, 100→400, 240→620, 900→1200.
- **Mechanic (328 edits):** every `add_treasury = -X`, `treasury >= X` (literal RHS), and verb
  `cost = -X` param in `events/imp19c_mod_events/qing_*.txt` + `currency_crisis_events.txt`,
  `common/scripted_effects/se_QING_*.txt`, `common/scripted_guis/QING_*.txt`.
- **Loc (147 edits):** matching cost tooltips via a NUMBER-LEVEL classifier — a number scales
  iff treasury-associated (¥ / "treasury of" / nearest resource-noun) AND a cost not a gain
  (nearest cost-verb vs gain-verb / sign), with a same-line cost-restatement rule. Never
  `_DESC` keys, never a `custom_tooltip` wired from `common/missions/`.
- Stale `LOG_fail`/`LOG_line`/comment cost numbers in the touched verbs updated to match.

**Key decisions + why:**
- *Monotonic closed form, not a piecewise table* — a monotonic map preserves equality, so
  wherever `gate == cost` today it stays coupled after, with NO proximity heuristic (fixed the
  v1 event-level-gate miss). √-curve compresses the top so 250/500/900 ramp to the cap without
  colliding.
- *Ministry buttons IN by necessity* — they share the event verbs' cost bodies; excluding them
  would desync a button from its own cost. Not scope creep.
- *Missions OUT* — `common/missions/` (253 own costs) don't share event verbs, live in their
  own tree, and pace against mission rewards; a defensible subsystem boundary, not a deferral.
  Loc side hardened: mission `custom_tooltip` keys built into a runtime exclusion set (verified
  0 leaks incl. `qing_sp_*_DESC`).
- *Rewards / `var:` / non-Qing (usa/spa/flavor_eve) untouched* per the non-Qing principle.

**Reviews (design + applied diff, both adversarial):**
- Design v2 review — 3 findings, all fixed: (1) event-level gates → map ALL gates
  monotonically; (2) verb-delivered costs → include verb bodies + `cost=` params + sharing
  buttons; (3) FlavorEvents generic → OUT. Census confirmed no Qing `treasury >=` is a pure
  non-price wealth check and no event verb is called from a mission.
- Applied-diff code-review — 2 real findings, both fixed: **(HIGH)** `qing_integ.40.e.tt`
  quoted "100 gold" while its option charged the scaled 400 (verb-less cost restatement the
  classifier couldn't see) → allowlisted (key,100); **(HIGH invariant)** two combined-condition
  guards (`treasury >= 90/100` sharing a line with a `var:` condition) were skipped by the old
  line-level `'var:' not in line` guard, desyncing gate from charge → removed the redundant
  guard (RE_GATE already rejects `var:`/`negative_treasury` RHS structurally); both gates now
  scale to 380/400 == their charges. LOW stale-string finding also fixed.

**Verification:** map strictly monotonic, range [125,1200]; every gate==its charge (spot-checked
qing_war 490/490·535, WORKS wall/canal 620·595, CARAVAN escort 695, the 2 fixed verbs 380/400);
all LOG_fail thresholds match their gates; 90 files 487/487 digit-only swaps; brace balance
identical to HEAD; EOL 487/487 ignore-cr match (no churn); no BOM flips; no non-Qing leakage.

**Commit:** `4067120d9`, pushed to merge-overnight. Acceptance is boot-gated on the user's
machine (values render/charge correctly in-game); nothing here is boot-unverifiable.

---

## #2 — #114 "Examinations Convene": cost + test-takers + graduates scale with exam-hall count — DONE

**What:** `qing_keju.1` ("The Examinations Convene") charged a FLAT gold cost (380/220) and its
palace follow-up `qing_keju.2` minted a graduate cohort sized purely by pass-rate BAND. Neither
cost, nor any "test-taker" figure, nor graduate COUNT tracked the player's actual exam system — the
academy network (書院/shuyuan + the two named great academies) that already backs `QING_exam_reach`.
Make all three scale with that concrete hall count.

**What I did** (design → adversarial review → implement → review, both reviews grounded in source):
- **script_values (QING_governance_svalues.txt):** new `QING_academy_count` = the raw covered-province
  academy count, now the SINGLE source of truth for the building set. Rewrote `QING_exam_reach` to
  `value = QING_academy_count multiply=3 min=0 max=100` (behaviorally identical to the old inline loop
  — confirmed against `git show HEAD:`). New `QING_keju_cost_full_svalue` (×20, clamp 100–700) and
  `QING_keju_cost_modest_svalue` (×12, clamp 60–420), centred on the #1-rescale baseline (19 halls →
  380 / 228).
- **se_QING_EXAM.txt:** new `QING_keju_compute_convene` stores the convene-time DISPLAY vars
  (hall count, candidates = halls×500, both costs, expected graduates). Restructured
  `QING_exam_graduate_cohort` to split the two axes: degree QUALITY by pass-rate (jinshi lead if
  ≥30, else juren), graduate COUNT by hall thresholds (+1 juren at ≥16, +1 at ≥28). Bounded at 3.
- **qing_keju.1:** immediate calls `QING_keju_compute_convene`; options .a/.b gate+charge via the
  new svalues (`treasury >= SVALUE` / `add_treasury = { value = SVALUE multiply = -1 }`) instead of
  flat 380/220. Gate == charge by construction (same svalue).
- **loc (qing_office_events_l_english.yml):** .1.desc appends a live line (halls / candidates /
  "about N graduates expected"); .a.tt / .b.tt interpolate the live cost — all via the proven
  `[Player.MakeScope.GetVariable('X').GetValue|0]` datafunction.

**Key decisions + why:**
- *Halls = quantity, integrity = quality* — decoupling COUNT (hall network) from QUALITY (pass-rate)
  means corruption/捐納 now debases the DEGREES awarded, not the cohort SIZE. A deliberate model
  shift (a large academy network physically seats more candidates regardless of graft) and the point
  of the task; logged loudly in the design as a behavioral change from "corruption chokes intake."
- *Thresholds >=16/>=28, NOT >=8/>=16* — the design-review MEDIUM caught that the CURRENT baseline
  cohort is **2** graduates (not 3): at 19 halls `QING_exam_reach = 57` is the pass-rate ceiling
  before corruption drag, so the ≥60 healthy 3-cohort never fires at the 1763 start. Recalibrated so
  19 halls → 2 (unchanged), ≥28 → 3 (= today's healthy-band max, so the pool can't balloon), <16 → 1.
- *Costs superseded #1's flat 380/220 for these two options* — the task explicitly wants a dynamic
  cost; the svalue is centred on #1's baseline so the start is unchanged. Edited BY OPTION (the
  unrelated `qing_keju.4.b` also uses 220 and stays untouched).

**Reviews (design v1 + applied diff, both adversarial, grounded in real source):**
- Design v1 review — no blocking issues; 1 MEDIUM (baseline-cohort calibration was misread as 3,
  actually 2) + optionals, all fixed in design v2 (thresholds recalibrated, single-source-of-truth
  simplification adopted, corruption-decouple stated honestly, citations tightened).
- Applied-diff review — VERDICT CLEAN, no critical/medium. All 8 engine rules verified holding
  (RHS-comparison, exam_reach behavioral identity, gate==charge, same-tick country set-then-read,
  cohort self-computes hall count, datafunction form, brace/BOM/EOL, forecast==mint ladder). Fixed
  the one LOW (stale "the display cites" comment). One boot-watch flagged: named-svalue operand in
  `add_treasury = { value = SVALUE multiply = -1 }` is standard Jomini but eyeball the charge in-game.

**Verification:** braces balanced (111/111, 273/273, 124/124); BOM preserved (svalues none, others
BOM); no EOL churn (numstat == ignore-cr numstat); all 5 loc-read vars set by compute_convene; no
`#`/`$` in LOG strings; old QING_exam_reach pre-image confirmed identical; no dangling 380/220 in the
.1 flow; no identifier collisions.

**Commit:** `3c0455f18`, pushed to merge-overnight. Acceptance is boot-gated (values render/charge in-game).

---

## #3 — #115 "Yellow River Dike Breach": repair cost scales with dike count + corvée manpower — DONE

**What:** `qing_works.1` ("The Yellow River Dike Breach") charged a FLAT gold cost (335 expert / 380
standard, #1-rescaled) and levied NO manpower. Make the treasury cost RISE with the size of the dike
network the throne already maintains (the 河工 budget ballooned as the levee system grew — the actual
Qing fiscal dynamic), and add a corvée MANPOWER cost, mirroring `QING_works_build_great_wall` (which
levies both treasury AND manpower). Direct sibling of #114 — a concrete on-map building set already
exists (`qing_dike_building`, 4 seeded), so scale off a single-source-of-truth count svalue.

**What I did** (design → adversarial review → implement → applied-diff review → CRITICAL fix, both reviews grounded in source):
- **script_values (QING_governance_svalues.txt):** new `QING_dike_count` (covered-province count of
  the dike building, SSOT, mirrors `QING_academy_count`). Two cost tiers off it: `QING_dike_cost_expert_svalue`
  (`×40 +175`, clamp 175–700) and `QING_dike_cost_standard_svalue` (`×40 +220`, clamp 220–760). At the
  1763 start (4 dikes) → expert 335 / standard 380 (== the flat costs they superseded); +40/dike; expert
  sits 45 below standard at EVERY count, so gating on standard is always ≥ the charge.
- **se_QING_WORKS.txt (`QING_works_build_dike`):** added `manpower >= 5` self-gate + `add_manpower = -5`
  (mirrors great_wall's `manpower >= 10` self-gate/levy, scaled to the smaller work); swapped the two flat
  `add_treasury = -335/-380` to the count-scaled svalues via the proven `{ value = SVALUE multiply = -1 }`
  negate idiom. New `QING_DIKE_set_display_cost` helper stashes the standard-tier cost into a country var
  for the event tooltips.
- **qing_works.1 / qing_works.5:** immediates call the display-cost helper; .a/.b (and .5.a) gate
  `treasury >= QING_dike_cost_standard_svalue` + `manpower >= 5`; .c inverted (`treasury < STD` /
  `manpower < 5`) so it shows on unaffordability — no soft-lock (the guarantee rests on the holder-agnostic .b).
- **panel (QING_works_ministry_panel.txt):** dike button `is_valid` treasury→svalue + `manpower >= 5`
  (shares the verb — gate==charge requires touching it, same rationale as #114's ministry buttons).
- **loc:** event tooltips (.1.a.tt/.1.b.tt/.5.a.tt) show live cost via #114's PROVEN `GetVariable`
  datafunction; the panel TT uses the live `GuiScope.SetRoot(Player.MakeScope).ScriptValue(...)` form
  (the only one that works for a scripted_gui — no `immediate` to stash a var).

**Key decisions + why:**
- *Cost RISES with dike count* — historically correct: 河工 was the textbook Qing expense that ballooned
  as the levee network grew (more dikes = more permanent maintenance + flood-fighting liability + graft).
  Same "bigger system = bigger bill" shape as #114, independently justified.
- *Two finesse tiers preserved* — the "a capable minister builds cheaper" mechanic is existing and sensible;
  scale BOTH tiers with count (as #114 kept its pass-rate quality axis while scaling the count axis). The
  task adds a count axis + manpower; it doesn't ask to flatten the finesse axis.
- *Gate on the STANDARD (higher) tier at all 5 sites* — since expert ≤ standard at every count, this is
  always ≥ the actual charge (never surprise debt). An expert minister in the `[expert, standard)` band is
  routed to .c; acceptable (design-review L2, acknowledged).
- *Loc form split (design-review M1 fix)* — the live `ScriptValue` datafunction has NO in-repo precedent in
  an event-option tooltip (only scripted_gui/interface). Rather than bet an unproven form for cosmetic
  uniformity, each site uses the form already proven for its context: `GetVariable` (events) + `ScriptValue`
  (panel).

**Reviews (design v2 + applied diff, both adversarial, grounded in real source):**
- Design review — verdict "fundamentally sound"; 1 MEDIUM (M1, event-tooltip datafunction unproven → split
  the loc forms), 3 LOW (L2 acknowledged band tradeoff; L3 pre-existing free-reward gap NOT worsened,
  out of scope; L4 imprecise citation → fixed). Arithmetic, soft-lock De Morgan, gate==charge, RHS-comparison,
  expert≤standard all verified sound.
- Applied-diff review — 1 **CRITICAL** (off-by-one: `add_building_level` applies immediately, so the
  treasury charge — read AFTER the build in v1 — re-evaluated `QING_dike_count` at N+1, overcharging by the
  +40/dike step and breaking both the 335/380 baseline and gate==charge by up to 40 gold on the standard/
  cheap/mediocre path) + 1 LOG (inaccurate `max_amount=1` comment). **Both fixed:** reordered the verb to
  CHARGE BEFORE BUILD (treasury `if` → flat `add_manpower` → `add_building_level` LAST), so gate, display and
  charge all read the pre-build count N; corrected the svalue comment (`qing_dike_building` has no `max_amount`;
  the count works via `has_building` boolean + the NOT-has_building build guard). Everything else clean:
  RHS-comparison, negate/manpower idioms, display-var set-before-read (both events set in immediate),
  manpower levied once only on build, no soft-lock, no dangling flat costs, brace balance, no BOM/EOL churn.

**Post-fix verification:** at N=4 → expert charge 335, standard charge 380, standard gate 380 (== charge),
expert (335) ≤ gate (380) — baseline restored, gate==charge holds. Braces balanced (svalues 117/117,
se 248/248, events 139/139, panel 73/73); BOM preserved (svalues/se/events none, loc/panel BOM); no EOL
churn (numstat == ignore-cr numstat); no `#`/`$` in LOG strings; every var read has a matching set.

**Commit:** `bceccff37`, pushed to merge-overnight. Acceptance is boot-gated (cost/manpower render + charge in-game).
