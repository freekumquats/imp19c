# DESIGN — Concretize `qing_han_provincial_power`: derive from Han governors' loyal cohorts (漢族督撫坐大)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI.
**Part of** the meter-concretization program ([[imp19c-concrete-over-abstract-rule]]).

## 0. The problem — a meter-of-meters that ignores a fully-built concrete system

`qing_han_provincial_power` (0–100, seed 0) models the historical shift of provincial military power into
Han hands (曾國藩/李鴻章 and the regional armies). Verified drivers:
- **Target = `(qing_banner_decay + qing_greenstandard_decay)/2 − qing_modernarmy_share`** + a law bias
  (`se_QING_DECLINE.txt:424-433`). So it's a **pure meter-of-meters** — reads three OTHER abstract meters
  and NOTHING concrete. It uses central-army decay as a *proxy* for "the throne leans on Han magnates."
- Drift ±2/quarter toward that target; a few event nudges (the sanction lever `+15`, `se_QING_MECHANICS.txt:152`).

This is the sharpest anti-pattern in the audit: the mod ALREADY has the concrete system this meter names —
**task #90/#105's `QING_sanction_regional_army`** binds a personally-loyal army to a REAL Han
governor-general (`QING_regional_army_bind_commander`, `set_personal_loyalty = scope:qing_regional_magnate_
commander`, `se_QING_MECHANICS.txt:145-239`). A sanctioned 勇營 is a real character with real loyal cohorts.
Yet the meter that tracks exactly this reads decay proxies, not the magnate. The user's point: Han governors
are real characters with real culture AND real loyal-cohort power bases — read those.

## 1. Thesis — BLEND a magnate-governor COUNT into the existing target (revised after review)

⚠️ **First draft was wrong: `num_loyal_cohorts` cannot be SUMMED (review F1).** Being a per-character
*trigger* (`num_loyal_cohorts >= 10`) is NOT being a readable *value* — `add = scope:gov.num_loyal_cohorts`
is unproven (0 value-reads in either oracle repo; all ~36 uses are trigger comparisons) and won't compute.
My §3 "VERIFIED" was a conflation. So the raw-cohort-sum tally is unbuildable. Two buildable primitives
exist; use the COUNT one:

**Tally = COUNT of magnate-governors, using `num_loyal_cohorts` strictly as a TRIGGER:**
```
set qing_han_magnate_tally = 0
every_character = {
    limit = {
        employer = ROOT  is_governor = yes  is_alive = yes  has_culture = han   # NOT culture=han literal (F6)
        OR = { has_character_modifier = qing_regional_magnate         # the #105 sanctioned magnate (exists, F5)
               num_loyal_cohorts >= @han_magnate_cohort_threshold }   # trigger, not a value-read (F1)
    }
    ROOT = { change_variable = { name = qing_han_magnate_tally  add = 1 } }
}
```
This is (a) BUILDABLE — count + trigger + the already-existing `qing_regional_magnate` modifier (F5,
`se_QING_MECHANICS.txt:197`), all proven; and (b) opens at **0** in 1763 (no sanctioned magnates, no Han
governors with private armies at the High-Qing zenith) — matching the seed.
(NOT the `power_base`-sum alternative: `power_base` IS a readable value but the code warns holdings keep it
non-zero forever `se_QING_MECHANICS.txt:190` → it would open HIGH at 1763 and need a mandatory baseline-freeze.)

**But do NOT fully replace the decay target — BLEND (review #3).** The current target
`(banner_decay+greenstandard_decay)/2 − modernarmy_share` (`se_QING_DECLINE.txt:407-419`) is INTENTIONAL and
load-bearing: it models the *structural pressure* — when both central armies rot, the throne is FORCED to
lean on Han magnates even before any are sanctioned; a modern national army SUPPRESSES the vector. A pure
magnate-count would make provincial power rise ONLY when a magnate is actually sanctioned — so a passive/AI
Qing whose central armies rot to 100 but who never sanctions sits at 0 forever, and building 新軍 would no
longer suppress it. That's a behavioral regression, not a simplification. **Correct design: target = the
existing decay-pressure formula plus the concrete magnate-count as a WEIGHTED SUM** (re-review V2: NOT
`max()` — max would let the magnate term override 新軍 suppression, defeating the channel we're keeping).
`target = (banner+gs)/2 − modernarmy + qing_provmil_bias + 12×magnate_count`, added BEFORE the 0..100
clamp (`se_QING_DECLINE.txt:434`), alongside the existing `qing_provmil_bias` term (`:433`). So the meter
reflects BOTH latent pressure (decay) AND realized devolution (real magnates). Concretization ADDS a
concrete term; it does not delete the structural one. **Pin `@han_magnate_cohort_threshold >= 10`** (the one
proven value, `character_events.txt:175`); build-check that no 1763 Han governor starts at/above it (the
`qing_regional_magnate` arm is runtime-only, safe).

## 2. Consumers (unchanged — read the level)
Gates at `se_QING_DECLINE.txt:272/277/282` (bands: warlord ≥80 / 55 / 30), `se_QING_MECHANICS.txt:253/297`
+ `QING_mechanics_actions.txt:168` (reassert/sanction levers, `>=20`), and — load-bearing —
**`se_SEPARATISM.txt` the warlord separatist spawn: ARMS at ≥80** (`@separatism_qing_warlord_floor = 80`,
:472/500/532, 50% secession chance), **escalates to 75% at ≥90** (:523). ⚠️ Secession begins at **80, not
90** (my earlier "≥90" was wrong 3×, review F4). The scaling calibration target is therefore "a genuinely
magnate-dominated realm reaches 80" (fractures), and the tally→0-100 SCALING CONSTANT (unspecified in the
draft — now PINNED) decides whether/when 80 is hit. **CONSTANT (user 2026-08-06): 6 magnates = the
"heavily-devolved" reference; scaling = 12/magnate.** So 6 magnates → 12×6 = 72 from the count, + the
decay-pressure term (~8+ once central armies rot) → crosses the ~80 separatism-arm floor. A mildly-devolved
realm (1–2 magnates → 12–24) stays well below. Comment PLACEHOLDER-playtest.

## 3. Feasibility (corrected — the draft's "VERIFIED" was wrong)
- ⚠️ **`num_loyal_cohorts` is a TRIGGER, not a readable VALUE (review F1).** All ~36 oracle uses + this
  mod's `character_events.txt:175` are `num_loyal_cohorts >= X` trigger comparisons — ZERO `add=/value=`
  reads. So it CANNOT be summed; use it only as a threshold trigger in the count's `limit` (§1).
- **`power_base` IS a readable value** (`order_by = power_base`, `se_QING_MECHANICS.txt:335`) — the fallback
  primitive — BUT `:190` warns a real governor's holdings keep `power_base` non-zero forever, so a
  power_base sum opens HIGH at 1763 and needs a mandatory baseline-freeze. The COUNT approach (§1) avoids
  this — prefer it.
- **The `qing_regional_magnate` character modifier ALREADY EXISTS and is iterable (review F5 — clean).**
  `QING_magnate_track_grant` stamps it (`se_QING_MECHANICS.txt:197`); `QING_reassert_strip_magnate` iterates
  it via `any_character` + `ordered_character max=1` (`:329-335`) — so the modifier is proven iterable (no
  new marker needed), but that is an `any_character`/`ordered_character` precedent, NOT `every_character`
  (re-review 7B — corrected citation). For the COUNT, verify `every_character` over office-holders against a
  real `every_character` precedent, not the `any_character` trigger at `se_QING_DECLINE.txt:1571` (7C: that's
  a trigger, not the effect-iterator the count needs).
- **Use `has_culture = han`, NOT `culture = han` (review F6).** The proven sibling selection (qing_office.42
  `:1001`) uses `has_culture = han`; a bare `culture = <literal>` on a character scope is risky (a logfix at
  `se_QING_DECLINE.txt:1370` notes `culture=` literal was invalid on char scope). OPEN: `has_culture = han`
  excludes yue/hui/hoa Sinitic governors — decide `culture_group = chinese_group` vs `has_culture = han`
  (qing_office.42 uses the latter; match it for consistency).
- **Iteration + cadence:** `every_character { employer=ROOT is_governor=yes is_alive=yes }` is proven
  (`se_QING_DECLINE.txt:1571`); annual cadence, drift quarterly. Cheap.
- **RHS-comparison rule:** the drift compare needs `_cmpsvalue` (as the existing one does, `:437`).

## 4. Interaction — a BLEND, not a decouple (review #3 corrected the draft)
The draft called removing the banner/greenstandard/modernarmy dependency a "win." It is NOT — that coupling
is intentional structural pressure (central-army rot FORCES devolution; 新軍 suppresses it). Deleting it
means a passive/AI Qing that never sanctions sits at 0 forever and 新軍 stops suppressing provincial power.
So the target must BLEND the decay-pressure formula with the concrete magnate-count (§1), keeping both the
latent-pressure and realized-devolution channels. NOTE: the sanction event ALSO cuts banner/greenstandard
decay −8/−8 (`se_QING_MECHANICS.txt:148`) — a self-limiting feedback that must be preserved in the blend,
else repeated sanctioning drives to the 80 warlord band too fast (review #7 — re-tune the `+15` nudge and
the scaling together).

## 5. Build checklist
1. `QING_DECLINE_recompute_han_prov` (annual): `every_character { employer=ROOT is_governor=yes is_alive=yes
   has_culture=han  OR = { has_character_modifier=qing_regional_magnate  num_loyal_cohorts>=@threshold } }`
   → COUNT (add 1 each; NOT a cohort sum — F1). `qing_regional_magnate` modifier already exists (F5).
2. `qing_han_prov_target` = the EXISTING decay-pressure formula (`(banner+gs)/2 − modernarmy`, KEEP it) BLENDED
   with `12 × magnate-count` (§1/§4 — do NOT replace/decouple, review #3; scaling=12/magnate, 6 magnates≈72
   +decay → ~80, user-decided §2). KEEP the law-bias term (`:433`) and the ±2 drift.
3. ⚠️ **DROP/reduce the sanction `+15` nudge** (`se_QING_MECHANICS.txt:152`) — re-review V6: the sanctioned
   magnate now enters the COUNT durably (raising the target while he holds `qing_regional_magnate`), so the
   `+15` live nudge double-counts the same devolution. Let the count carry realized devolution; KEEP the
   −8/−8 decay cut (`:148`) as the central-relief feedback. Without this the meter ratchets to 80 too fast.
4. Verify consumers (bands ≥30/55/80, reassert lever `>=20`, **separatism warlord ARMS ≥80 / escalates ≥90**
   — F4, NOT 90-only) unchanged; verify 1763 opens LOW (0 sanctioned magnates + decay-pressure ~12.5 → the
   blend still opens near today's resting value, not a spike).
5. Review gates: magnate COUNT not cohort-sum (F1); `has_culture=han` not `culture=` literal (F6);
   BLEND not decouple — decay pressure + 新軍 suppression preserved (#3); separatism ARMS at 80 not 90 (F4);
   scaling constant pinned; sanction +15/−8−8 re-tuned (#7); RHS-cmpsvalue; 1763 opens near today's value;
   brace/quote/BOM; boot-crash review.
