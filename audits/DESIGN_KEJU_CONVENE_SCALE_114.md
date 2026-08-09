# DESIGN — Task #2 (#114): "Examinations Convene" — cost + test-takers + graduates scale with exam-hall count

Status: DESIGN v2 (post adversarial-review). Branch merge-overnight. 2026-08-09.
v1 corrected on the baseline-cohort calibration (review MEDIUM-1: current baseline is 2 graduates,
not 3 — pass-rate ceiling at 19 halls = 57 < 60, so the healthy 3-cohort never fires at start) plus
the single-source-of-truth simplification and honest citations. All engine rules verified holding.

## Problem

`qing_keju.1` ("The Examinations Convene", the triennial host prompt) charges a FLAT gold cost
(option .a = 380, .b = 220 after the #1 rescale) and its palace-exam follow-up `qing_keju.2`
mints a graduate cohort whose SIZE (1–3) is chosen purely by the pass-rate BAND. Neither the cost,
nor any "test-taker" figure, nor the graduate COUNT scales with how large the player's actual
examination system is — i.e. the academy network (書院/shuyuan + the two named great academies),
the concrete on-map object that already backs `QING_exam_reach`. The task: make all three scale
with that hall count, so a wide academy network is a bigger, costlier, more productive exam.

## What already exists (grounding)

- **The concrete hall network.** `QING_exam_reach` (QING_governance_svalues.txt:323) counts
  covered provinces holding ANY academy (`qing_shuyuan_building` OR `qing_yuelu_academy_building`
  OR `qing_bailudong_academy_building`), ×3, clamped 0..100. The 1763 seed = ~19 covered provinces
  → reach ~57. This is the "exam-hall count" the task names.
- **Graduates already scale INDIRECTLY.** `QING_exam_graduate_cohort` (se_QING_EXAM.txt:211) calls
  `QING_exam_compute_pass_rate` (whose base IS `QING_exam_reach`), then mints 1 jinshi + 2 juren
  (pass≥60) / 1 jinshi + 1 juren (30–59) / 1 juren (<30). So COUNT is a pass-rate-BAND artefact,
  not a direct hall-count function, and is hard-capped at 3 "so the pool cannot balloon".
- **Cost is flat.** `qing_keju.1` .a `add_treasury = -380` / `trigger = { treasury >= 380 }`;
  .b `-220` / `>= 220`. No hall coupling.
- **No test-taker figure exists** anywhere in the convene flow.

## Design — one hall-count spine feeds all three axes

The academy count is the single input. Compute it live from buildings (no drift meter), store the
derived figures as country vars at CONVENE time (in `qing_keju.1`'s `immediate`, which runs BEFORE
the window renders — so the vars exist for both option-preview and loc), and read them back for the
gate, the charge, and the display.

### New script_values (QING_governance_svalues.txt, beside QING_exam_reach — NO BOM, LF, matches file)

    QING_academy_count          = raw covered-province academy count — the SINGLE SOURCE OF TRUTH
                                  for the academy building-set (review OPT-5). ~19 at 1763 start.
    QING_keju_cost_full_svalue  = { value = QING_academy_count  multiply = 20  min = 100  max = 700 }
    QING_keju_cost_modest_svalue= { value = QING_academy_count  multiply = 12  min = 60   max = 420 }

And REWRITE QING_exam_reach to consume it (one iteration body, no behavior change):

    QING_exam_reach = { value = QING_academy_count  multiply = 3  min = 0  max = 100 }

Calibration (centre on the #1-rescaled baseline so #1's tuning is preserved at the start):
19 halls → full 380 / modest 228 (≈ the current 380 / 220). 30 halls → 600 / 360. 10 → 200 / 120.
`min` floors so a war-shrunk network still costs something; `max` caps well under the #1 ~1200 ceiling.
`min`/`max` clamp semantics are the proven QING_bureau_reach idiom (min=lower bound, max=upper bound).

### New helper (se_QING_EXAM.txt): QING_keju_compute_convene — Scope COUNTRY (CHI)

Stores the CONVENE-time display vars (the gate/charge read the svalues live, see below; these vars
are for LOC + the expected-graduate count):

    QING_exam_init = yes
    set_variable qing_keju_hall_count   = QING_academy_count
    set_variable qing_keju_candidates   = QING_academy_count ; change_variable multiply = 500   # narrative "test-takers"
    set_variable qing_keju_cost_full    = QING_keju_cost_full_svalue
    set_variable qing_keju_cost_modest  = QING_keju_cost_modest_svalue
    QING_exam_compute_pass_rate = yes                         # refresh the rate the display cites
    # expected graduates (= 1 lead + hall-band extras, mirrors the cohort mint below) for the tooltip.
    # THRESHOLDS (>=16, >=28) are the coupled pair kept in lockstep with the cohort mint (review LOW-2).
    set_variable qing_keju_expected_grads = 1
    if hall_count >= 16 : change_variable qing_keju_expected_grads add = 1
    if hall_count >= 28 : change_variable qing_keju_expected_grads add = 1

Same-tick country-var set-then-read is proven safe (se_QING_EXAM.txt:84–87 does it for the pass-drag).
"test-takers" = candidates = hall_count × 500 is a NARRATIVE figure (the licentiates/graduates
gathering across the network), the readable face of the same hall count that drives cost + graduates.
×500 → ~9,500 at baseline (a defensible "thousands" feel, not a literal historical count).

### qing_keju.1 changes

- `immediate`: add `QING_keju_compute_convene = yes` (after the LOG_line).
- option .a: `trigger = { treasury >= QING_keju_cost_full_svalue }`,
  `add_treasury = { value = QING_keju_cost_full_svalue  multiply = -1 }`.
- option .b: `trigger = { treasury >= QING_keju_cost_modest_svalue }`,
  `add_treasury = { value = QING_keju_cost_modest_svalue  multiply = -1 }`.

Both the gate and the charge read the SAME named svalue live — mutually consistent by construction,
and a named-svalue RHS on `treasury >=` is the proven idiom (bribe_mercenary_button.txt:36,
`treasury >= army_size_merc_estimation_sg`). The `add_treasury = { value = … multiply = -1 }` drain
form is proven with a var operand (se_SUBJECT_QING.txt:1195 `value = var:qing_trib_amt`,
se_QING_MARCH.txt:506); a NAMED-svalue operand in the same slot is standard Jomini (the svalue's
internal min/max resolve first, then `-1` negates). This SUPERSEDES #1's flat 380/220 for these two
options (edit BY OPTION, not by value find-replace — `220` also appears in the unrelated qing_keju.4.b
at :375-376 which stays untouched; review LOW-4): the task
explicitly wants the cost dynamic, and the svalue is centred on #1's baseline so the start is unchanged.

### QING_exam_graduate_cohort restructure (se_QING_EXAM.txt)

Separate the two axes cleanly — **degree QUALITY from pass-rate, graduate COUNT from hall count**:

    QING_exam_init = yes
    QING_exam_compute_pass_rate = yes
    set_variable qing_keju_hall_count = QING_academy_count      # self-contained; any caller is safe
    # LEAD graduate — quality by the pass-rate band (preserves the current top-degree intent)
    if pass_rate >= 30 : QING_exam_mint_scholar = { degree = jinshi }
    else               : QING_exam_mint_scholar = { degree = juren }
    # EXTRA graduates — COUNT scales directly with the academy network (literal-RHS thresholds)
    if hall_count >= 16 : QING_exam_mint_scholar = { degree = juren }
    if hall_count >= 28 : QING_exam_mint_scholar = { degree = juren }

**Calibration (review MEDIUM-1, corrected).** The CURRENT baseline cohort is **2** graduates, not 3:
at 19 halls QING_exam_reach = 57, which is the pass-rate CEILING before the corruption/捐納 drag, so
the `pass_rate >= 60` healthy 3-cohort NEVER fires at the 1763 start — baseline sits in the `>= 30`
middling band = 1 jinshi + 1 juren = **2**. The thresholds above are therefore set to `>=16 / >=28`
(NOT `>=8 / >=16`) so:
- baseline **19 halls → lead + 1 extra = 2** (matches the current baseline exactly), 
- a WIDE network **≥28 halls → 3** (= the current healthy-band max, so the pool cannot balloon past
  today's ceiling; the age-55 retirement tick + office draws still hold the band), 
- a THIN/war-shrunk network **<16 halls → 1**.

**Behavioral shift, stated honestly (review MEDIUM-1):** decoupling COUNT from pass-rate means
corruption/捐納 no longer throttles the NUMBER of graduates, only their QUALITY (a corrupt realm
still fields a full-sized cohort, but juren-led rather than jinshi-led). This is the deliberate model
— **halls = quantity of the exam system, integrity = quality of its product** — and it is defensible:
a large academy network physically seats more candidates regardless of graft, while graft debases the
degrees awarded. It is a change from today's "corruption chokes intake size," accepted as the point
of the task (COUNT must track the concrete hall network). No `while`/division (fixed-point floor trap
avoided); all comparisons are literal-RHS (RHS-comparison rule).

### Loc (qing_office_events_l_english.yml — BOM, LF, matches file)

- `qing_keju.1.desc`: append a line citing the live network — hall count, gathered candidates,
  and "about N graduates expected" (forecast language — the real cohort recomputes at .2-time 60-150
  days later, review LOW-2) — via `[Player.MakeScope.GetVariable('qing_keju_hall_count').GetValue|0]`
  etc. (proven datafunction, cf. qing_greatgame QING_SPHERE_INLINE_TALLY, qing_integ.20.a.tt).
- `qing_keju.1.a.tt` / `.b.tt`: replace the literal "Costs 380/220 Treasury" with
  `[Player.MakeScope.GetVariable('qing_keju_cost_full').GetValue|0]` / `..._cost_modest`.

## Scope / out

- Only the CONVENE flow (.1 → .2 cohort). Grace exam (.5) doesn't mint a cohort today; unchanged.
- `qing_keju.2.b`'s political-influence gate (15 PI) is not a treasury cost — untouched.
- No new buildings, no AI hooks, digits/vars/loc only. CHI-only, player-only (the convene path is
  CHI + is_ai=no gated upstream).

## Risk / blast radius

- Worst case = a loc figure disagreeing with the mechanic (both read the same var/svalue, so aligned)
  or a var read before set (all sets are in .1's immediate, which runs before the window + before .2).
- The cohort self-computes hall_count, so a caller that skips convene still mints correctly.
- No `while`, no var-on-RHS, no fixed-point division — the three traps for this engine are all avoided.
