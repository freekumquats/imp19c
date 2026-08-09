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

---

## #4 + #5 — exam-degree trait icons: gold border + white→parchment background — DONE

**What:** The 10 exam-degree trait icons (6 civil: 秀 shengyuan / 舉 juren / 貢 gongshi / 進 jinshi /
翰 hanlin / 譯 fanyi_jinshi; 4 military 武: wu_shengyuan / wu_juren / wu_jinshi / wu_zhuangyuan) are
54×54 uncompressed BGRA8 circular calligraphy discs. #4: add a gold border rim to ALL 10. #5: change
the CIVIL set's white background to parchment. Combined into one task — same 10 files, one regeneration.

**What I did:** wrote a COMMITTED, reusable, idempotent post-processor `tools/style_degree_icons.py`
(the original calligraphy render was an uncommitted one-off — no named generator existed; per the
icon-generator-canonical rule I made this a proper committed tool, not another one-off). It reads each
DDS via `dds_icon.read_dds_bgra8`, applies two numpy passes, writes back via `write_dds_bgra8`:
- **#4 gold rim:** a ~3px annulus at the disc's outer edge (radius from centre, gated on `alpha>8` so it
  follows the round antialiased boundary and never paints the transparent corners), with a radial
  gold→light-gold gradient. Applied to all 10.
- **#5 parchment:** recolor light + low-saturation (white) pixels to warm parchment RGB(228,208,165),
  scaled by source brightness to keep any vignette. Applied to the CIVIL set only.

**Key decision — parchment by FILE, not per-pixel; military green PRESERVED:**
- The military 武 set has a deliberate GREEN background (its martial distinguisher). #5 says
  "white→parchment"; the green is not white, so it stays. First cut used a per-pixel saturation gate
  to spare green — but the military's pale-green fill (227,238,235) is too near-white and got recolored
  too (a numeric check caught this: green fill → parchment, erasing the marker). Fixed by gating
  parchment by the CIVIL/MILITARY file lists (robust, unambiguous) rather than a fragile colour detector.
- *Rejected alt:* recolor military green→parchment-green for uniformity — dropped; the gold border
  already unifies the two sets (parchment+gold = civil, green+gold = martial), and erasing the green
  would lose the at-a-glance civil-vs-military read.

**Reviews:** code-review on the generator script (image-correctness + idempotency, not gameplay) —
verdict SOUND, no critical/medium. 2 LOW, both comment-accuracy: (1) the idempotency reason cited
brightness when SATURATION is the actual guard (parchment lum≈209 passes the lum>165 gate; it's spared
only by sat≈0.276 ≥ 0.14) → corrected the docstring + added a `_saturation(PARCHMENT) >= 0.14` self-check
assert so a future threshold change can't silently break idempotency; (2) a "blend eases over the ink
edge" comment overstated the algorithm (it's a hard assignment; dark glyph cores survive via the luma
gate) → reworded. Both fixed.

**Verification:** rendered before/after contact sheets and eyeballed (civil=parchment+gold, military=
green+gold, calligraphy + circle shape intact); dims 54×54 + BGRA8 format preserved on all 10; alpha
(circle shape) untouched; idempotent — re-run produces byte-identical DDS (md5-confirmed, twice); git
status shows exactly the 10 icons + the new script, no strays.

**Commit:** `8abfed049`, pushed to merge-overnight. Acceptance is boot-gated (icons render correctly on
the trait cards in-game).

---

## Task #7 (#94/#95) — Concrete grain economy: SLICE 2 (京倉 building + seeding + capacity anchor) — DONE

**What:** #94/#95 is a large, adversarially-reviewed design (design/DESIGN_GRAIN_FOOD_VALUE_94_95.md)
sequenced into 5 reviewed commits (§8b re-sequence). This is **slice 2 of 5** — the smallest reviewable
slice: put the concrete capital-granary building (京倉/通倉) on the map at 1763 start with a real
`local_food_capacity` anchor. NO delivery, NO consumption, NO famine-gate rewire (those are slices 3-6).

**What I did (per the §8c implementation spec I wrote + had reviewed):**
- New building `qing_capital_granary_building` (common/buildings/qing_granary_buildings.txt): +400
  local_food_capacity + 2 non-food flavour keys (state loyalty, happiness). `potential = is_in_region
  Zhili + jurchen/chinese culture`; `allow = sufficient_job_slots`.
- Seeded once at Beijing P8363 via `QING_seed_works_building` (se_QING_BUILDINGS.txt), adjacent to the
  canal-depot works block — the same ownership-guarded, idempotent macro the 5 hydraulic works use.
- Loc: name + `_desc` (qing_works_l_english.yml), results tooltip (imp19c_tooltips_l_english.yml).
- Icon: added the key to tools/gen_table_icons.py (canonical generator, no one-off) and generated
  gfx/interface/icons/buildings/qing_capital_granary_building.dds (200×200 BGRA8, byte-size identical
  to the sibling; sourced from a "Turpan Old Granary building" Wikimedia photo).

**Key decisions + why:**
- **`add_building_level` RESPECTS potential** (memory imp19c-add-building-level-respects-potential + the
  #190 in-repo correction). Verified P8363 = CHI-owned, city, region Zhili (areas.txt Beijing area ∈
  regions.txt Zhili:652), so `is_in_region = Zhili` + culture=jurchen passes → the seed lands, does not
  silently drop. Used the proven region+culture idiom (province_id in a building potential is unattested).
- **Capacity-only isolation (the whole point of slice 2):** deliberately NO `local_monthly_food_modifier`.
  The hardcoded `positive_state_food_growth` (00_hardcoded.txt:1193, +0.02 local_population_growth) fires
  on food SURPLUS, not capacity — so a capacity-only building with only non-food flavour keys CANNOT
  create surplus → cannot run Beijing's pop away. This is exactly why §8b isolated it as the safe first boot.
- **`allow = sufficient_job_slots` (NOT always=no):** reviewer suggested matching the seed-only
  institutions (hanlin/guozijian use always=no). REJECTED: a permanently-false `allow` HIDES the building
  type at boot (proven: qing_mission_cathedral note + the memory), which would void the +400 capacity. This
  building's whole point is a FUNCTIONING food-capacity modifier a later slice fills, so it follows the
  FOOD-building family (granary/dike/depot, all sufficient_job_slots). No phantom build option results — a
  build-menu entry requires a macro_builder config include, which this building has none of. Documented inline.
- **400 capacity = 2× the provincial 常平倉 (200)** — a vanilla-food-scale balance knob (design §1.3), NOT a
  historical shi figure; it's the calibration lever slice 3's delivery is tuned against (revisit there).

**Review verdict:** design-first — wrote the §8c per-slice implementation spec, then code-review
(subagent) grounded against real source. Verdict: **fundamentally sound, no critical/correctness/surplus
bug.** All 7 grounded checks CLEAN (potential satisfiable at P8363, capacity-only invariant holds, braces,
BOM/EOL, loc keys match siblings + no raw-key renders, seed guard idempotent, no RHS/macro/LOG hazards).
2 LOW: (1) missing building icon → FIXED (generated via canonical generator); (2) allow-vs-seed-only
inconsistency → RESOLVED by keeping sufficient_job_slots (memory-backed: false allow hides the type) +
documenting the decision inline. Both closed before commit.

**Verification:** braces balanced (20/20); git status = exactly the 6 changed files + 1 new DDS, no strays;
zero EOL churn (numstat == --ignore-cr-at-eol numstat); BOM preserved per file; DDS format matches sibling.
Acceptance is boot-gated (building appears at Beijing with the +400 capacity + a legible icon; slices 3-6
wire the delivery/consumption/retirement on top).

**Status:** SLICE 2 of 5 DONE. Slices 3-6 (canal→capital-state delivery + famine-gate rewire + retire
qing_grain_reserve; #95 depot display; qing_granary_stock retirement; canal-condition by corridor) follow
as their own reviewed commits per the design's re-sequence. NOTE: per NO-DEFERRALS this is NOT a punt — the
design ITSELF mandates separate reviewed commits ("Sequenced as separate reviewed commits… the per-step
IMPLEMENTATION design is written + re-reviewed before each commit"); the task is a multi-slice build and I
am building the slices in order, not carving off the hard part.

---

## Task #7 (#94/#95) — SLICE 3 of the concrete grain economy: canal→capital-state REAL FOOD + famine-gate rewire + payload re-point + retire `qing_grain_reserve`

**What it was:** §8b re-sequence step 3 — the substantive slice. Replace the abstract 0..100
`qing_grain_reserve` counter with REAL engine food on the Beijing/Zhili capital state (the 京倉 capacity
anchor from slice 2 is what that food fills): the Grand Canal delivers tribute grain via `add_state_food`,
the capital + banner garrisons + frontier armies draw it down, famine gates read the real fill %, the
famine-dilemma payloads act on real food, and `qing_grain_reserve` is retired.

**What I did:**
- **Design-first (§8d spec):** wrote the full per-slice implementation spec grounded in verified primitives
  (`capital_scope.state` effect scope proven se_DIPLOMACY.txt:1049; `add_state_food` block form + `multiply=-1`
  proven pool A :2431/:2451 + apotheosis :88; cross-scope `ROOT.var:` read into set_variable proven pool A
  :2413; `_cmpsvalue` for var-vs-var comparisons; GUI has no country→capital→state→food chain so the capital
  food/cap is mirrored into CHI vars like the #93 pool bar).
- **Adversarial review of the spec BEFORE coding (subagent):** returned 2 HIGH + 3 MED + 3 LOW. Both HIGH
  were CONFIRMED against source and forced a redesign (see Key decisions).
- **Implemented after the redesign:** rewrote `QING_canal_run_grain_balance` (delivery/draw now FRACTIONS of
  the measured `has_state_food_capacity`, applied to `capital_scope.state`, result mirrored to
  `qing_capital_food`/`_cap`/`_pct`); added shared helper `QING_canal_rederive_capital_pct`; deleted the
  `qing_grain_reserve` init seed; rewired both famine gates (`<40`/`<20` on `qing_capital_grain_pct` with
  `has_variable`+`cap>0` guards); re-pointed `QING_canal_relief_redirect` (−10% of cap, clamped to food) and
  `QING_canal_relief_hoard` (+5% of cap, clamped to headroom) to real food using the full precompute-operand
  idiom; re-pointed the GUI reserve bar + value; reworded `QING_WORKS_MINISTRY_GRAIN_TT`; re-pointed the
  canal.1 LOG; updated the module header comment + the crosswiring-assessment doc reference.

**Key decisions + why:**
- **HIGH-1 (CONFIRMED, redesign):** the spec's first draft anchored `FOOD_SCALE=4` on the 京倉's 400
  `local_food_capacity`, assuming the capital STATE's `has_state_food_capacity ≈ 400`. FALSE:
  `province_base_values` grants every province `local_food_capacity = 100` (00_hardcoded.txt:141) and the
  Beijing capital state is **7 provinces** (areas.txt:12969), so its capacity is ~700+400+farms ≈ **1100+**.
  A fixed ×4 band on ~1100 is <2%/qtr — the reserve would sit pinned near-full and the famine gates would
  never fire. **FIX:** make delivery + draw PERCENTAGES of the measured capacity (auto-scaling, no false
  anchor); the fill-ratio pct is already capacity-relative.
- **HIGH-2 (CONFIRMED, redesign):** a small fixed delivery clamped to near-zero headroom (a near-full state)
  is discarded every tick → canal condition has no grip on the reserve. **FIX:** make the DRAW a large,
  ALWAYS-APPLIED structural drain (0.06 of cap/qtr, −0.01 per 常平倉 to floor 0.04) — the 漕運 grain sink the
  north cannot self-supply. It re-opens headroom every tick, so the headroom-clamped delivery (0.08 × cond ×
  quota) is never permanently discarded; canal condition sets the equilibrium fill level (sound canal 8% >
  6% draw → fills; silted 2% < 6% → drains toward famine). Monotone grip = design intent.
- **Plan-1 preserved, Plan-2 NOT adopted:** the reviewer's fix (a) was "track the reserve as a private
  sub-quantity" — that is the REJECTED Plan 2 (§9). User LOCKED Plan 1 (real state food, gates read
  has_state_food). I took fix (b): keep the real-food observable, fix the calibration to be capacity-relative.
- **FOOD fractions (0.08 delivery / 0.06 draw) are boot-tuned, NOT deferred:** the mechanic is fully built +
  wired + self-scaling; the two literals are documented knobs a boot confirms (exactly the §3 "boot-test
  knob" / Q6 the design designates). Slice ships INSTRUMENTED — a `LOG_state` each tick dumps
  food/cap/pct/delivery/draw (LOG_line has no value field; `$`/`#` banned in msg) — so the first boot reveals
  whether Zhili's vanilla food regime is surplus or deficit and confirms/retunes in one literal. This is the
  design's own acceptance gate, not a punt.
- **MED-1 (illusory guard, corrected honestly):** `cap>0` does NOT detect a moved capital (a state always has
  cap=100×provinces>0). Relabelled as divide-by-zero + first-tick safety only; for CHI the capital is Beijing
  and never moves, so the fixed-Zhili 京倉 and the live delivery target never decouple. No per-tick
  has_building scan added (unwarranted for a case that can't arise for the only tag running this code).
- **MED-2:** added `has_variable = qing_capital_food_cap` to both famine gates for parity with the pct-derive.
- **MED-3:** the two payloads implement the FULL precompute-operand/`_cmpsvalue`/block-form idiom (not prose
  shorthand), and share the `QING_canal_rederive_capital_pct` helper so GUI+gate reflect the choice at once.
- **LOW-1:** retirement list corrected 13→14 sites (the :58 init guard, deleted with its block).
- **LOW-2:** DESIGN_QING_CROSSWIRING_ASSESSMENT.md:423 updated (banner-decay coupling now reads real pct).
- **LOW-3:** final food computed ARITHMETICALLY (initial+delivered−drawn) not by re-reading has_state_food
  after add_state_food (that re-read reflection is UNVERIFIED; pool A never re-reads).

**Review verdict:** applied-diff code-review returned 1 CRITICAL + 1 LOW, both fixed before commit:
- **CRITICAL-1 (FIXED):** two `_cmpsvalue` RHS operands used at se_QING_CANAL.txt:209/215/390/435
  (`qing_cap_room_tmp_cmpsvalue`, `qing_cap_food_tmp_cmpsvalue`) were never minted in
  `00_event_values.txt` — an undefined named svalue on a comparison RHS evaluates to 0, which INVERTS
  both clamps (delivery would always overwrite to full headroom → fill to cap every tick regardless of
  canal condition; draw would always overwrite to full food). This is the mod's #1 error class (the very
  rule the `_cmpsvalue` block enforces). Fix: minted both as same-scope passthroughs
  (`{ value = var:qing_cap_room_tmp }` / `{ value = var:qing_cap_food_tmp }`) at 00_event_values.txt:1861-1862,
  identical idiom to the adjacent `qing_gran_*` set. Both temps are set in-scope immediately before each compare.
- **LOW-1 (FIXED):** `LOG_state` emits a full ROOT scope-stack dump EVERY quarter forever = permanent heavy
  debug spam. Fix: gated behind a `qing_canal_log_ticks` counter (0→8) so the dump fires only for the first
  8 ticks (~2 game-years — enough to watch the reserve equilibrate and tune the two fractions), then goes
  silent for the campaign. Counter only increments (no drift), self-terminating.
- Reviewer CONFIRMED clean (once CRITICAL fixed): all other comparison RHS bare-literal or defined-svalue,
  no `ROOT.var:`/`scope:` on any RHS; add_state_food block form + `multiply=-1` for negatives (all 4 calls);
  scope integrity (save_scope_as precedes every read, ROOT write-back before remove_variable); value-field
  var reads legal; equilibrium sign logic correct (delivery + / draw −, dfrac 0.08 > drawfrac 0.06 → fills
  to ~0.94 cap, headroom-clamp binds, no forced surplus / runaway pop); divide-by-zero + first-tick guarded;
  retirement complete (zero live qing_grain_reserve refs); braces 215/215; no BOM on se_/gui/event.

**Verification (self, post-fix):** braces balanced (222/222 se_QING_CANAL after the log-gate `if` blocks; the
minted svalues added exactly 2 open + 2 close to 00_event_values.txt — its 611/610 count is a PRE-EXISTING
1-off at HEAD 609/608, a stray brace in a comment, not introduced here); repo-wide `qing_grain_reserve` grep = ZERO
live code refs (only 3 explanatory comments); tick order confirmed (init/update/balance :311-313 run BEFORE
the gates :329); zero EOL churn on all 6 files (numstat == --ignore-cr-at-eol numstat); BOM per file
(se_QING_CANAL/gui/event = none as before, loc yml = BOM). `multiply = ROOT.var:` / `value = ROOT.var:` are
value-field reads (legal; se_AI.txt:1317, pool A :2413), not comparison RHS.

**Status:** SLICE 3 DONE — built, reviewed (1 CRITICAL + 1 LOW both fixed), committed + pushed. Slices 4-6
(#95 depot 食-share display; qing_granary_stock retirement — the risky 12-consumer migration; canal-condition
by per-corridor coverage) follow as their own reviewed commits per the re-sequence.
