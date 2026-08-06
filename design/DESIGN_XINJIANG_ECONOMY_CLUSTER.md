# DESIGN — Xinjiang economy cluster: concretize `qing_caravan_prosperity` + `qing_xinjiang_control` (西域經略)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI. #91 D + #10/#11.
**REWRITTEN 2026-08-06 after adversarial review returned 4 CRITICALs** (all now addressed below; §8 tracks
each). Supersedes the rejected single-meter DESIGN_XINJIANG_CONTROL_CONCRETIZE.md (flat ILI-only signal).

## 0. The knot today (all abstract / circular)
- `qing_caravan_prosperity` target (`se_QING_CARAVAN.txt:89-136`) = base 40 + `qing_xinjiang_control/4`
  (meter-of-meter) + `qing_caravan_yarkand_market×5` (abstract capped-4 investment counter) + flags.
  **Reads no real trade.**
- `qing_xinjiang_control` = a pure nudge/set meter written by ~4 subsystems (ILI arc, #367 consolidation,
  caravan, missions). Owned by none cleanly. Seed 40 (`se_QING_ILI.txt:63`).
- **Circular:** caravan target READS control (`:97`) AND caravan WRITES control (`:219/226`).
The user's point: caravan trade and Xinjiang grip are REAL things on the map — derive both from the map,
break the loop. But the oases are held by SUBJECTS, not CHI directly — this drove three of the four
CRITICALs and reshapes the whole approach.

## 1. ⚠️ THE LOAD-BEARING CORRECTION — the oases are SUBJECT-held; iterate by AREA not by owner (CRITICAL 1)
`every_owned_province { limit = { is_in_area = Dzungaria/Tarim } }` returns **NOTHING** for CHI: the oasis
provinces are `own_control_core` of **ILI** (Dzungaria block + Urumqi 2930 + Turpan 9597) and **XNG** (Tarim
basin), NOT CHI (`setup/main/00_default.txt:35994-36038`; deps `CHI→ILI autonomous_governorship`,
`ILI→XNG client_state`). This is **verbatim the #91 blocker `se_QING_ILI.txt:301-314` documents and fixed**.
The PROVEN owner-independent idiom is already in-file:
```
area:Dzungaria = { every_area_province = { ... } }
area:Tarim     = { every_area_province = { ... } }
```
(`se_QING_ILI.txt:320-333,406`; both areas exist, `areas.txt:2401/2427`; NO single Xinjiang region — union
the two. Note Urumqi 2930 files under `Tarim`, covered by the union.) **EVERY per-province sweep in both
theses below uses `area:` + `every_area_province`, never `every_owned_province`.**

Because these are subject-held, an oasis-province term counts land the Qing controls THROUGH ILI/XNG — which
is exactly the fiction ("grip on the Western Regions via the subject frontier"), not a bug.

## 2. Thesis A — `qing_caravan_prosperity` ← real oasis trade (as a script_value, not inline add)
⚠️ **The read form is a SCRIPT_VALUE accumulator, not `prev.num_goods_produced` (CRITICAL/MEDIUM 1).** Grep
finds ZERO scope-prefixed `num_goods_produced` reads — it is ALWAYS read bare in the province/state scope
(`add = num_goods_produced`, `GOODS_svalues.txt:1674`; `value = num_goods_produced`, `:3460`). The proven
"sum across a province set into a country total" idiom is a script_value (how GOODS_svalues does it), read
via `set_variable`:
```
QING_caravan_oasis_trade_svalue = {   # Scope: country (CHI). Bare num_goods_produced in area-province scope.
    value = 0
    area:Dzungaria = { every_area_province = { add = num_goods_produced } }
    area:Tarim     = { every_area_province = { add = num_goods_produced } }
}
# then: set_variable = { name = qing_caravan_oasis_trade  value = QING_caravan_oasis_trade_svalue }
# scale to a 0..100 prosperity contribution; drift the meter toward the target (hysteresis, as today).
```
- ⚠️ **Do NOT double-count** the #32 income rework: it reads country-level `GOODS_national_production_*`
  (`se_QING_CARAVAN.txt:167`) — a distinct, wider quantity. The prosperity TARGET reads the oasis-SCOPED
  `num_goods_produced` subset (narrower). Overlapping goods, different aggregation — not a double-count
  (review confirmed vector 2 safe).
- ⚠️ **NOT the `western_steppe_tradezone` balance** (bundles Siberia/Moscow/Caucasus — wrong granularity).
- **REMOVE the `qing_xinjiang_control/4` term** (`:97`) — breaks the meter-of-meter AND the circular loop (§4).
- `qing_caravan_yarkand_market×5`: leave as-is (abstract investment counter; making it a real bazaar
  building is optional net-new work, not this cluster's core).

### §2a — scale + 1763 opening (MEDIUM 4 — must be shown, not deferred)
prosperity seeds **45** (`se_QING_CARAVAN.txt:73`); consumers gate at ultimatum ≥55 (`:252`) / crisis ≥40
(`:267`). ⚠️ **The full 1763 target today = `40 + control/4 (10) + market×5 (0) − moderate-customs (5) = 45`**
— the `qing_caravan_customs_rate = 1` default (`:74`) subtracts **−5** at `:124` (LOW finding — the earlier
sketch forgot this). So removing `control/4` and landing back at 45 requires the oasis term to overcome BOTH
the lost +10 AND the −5 customs drag: `40 − 5 + S×oasis_trade ≈ 45 → S×oasis_trade ≈ 10` (NOT ≈5). Build-check:
`LOG_line` the raw `QING_caravan_oasis_trade_svalue` at 1763, then pick S so the full target
(`40 + S×oasis + yarkand − customs_drag`) lands ~45. Show the arithmetic against the ≥55/≥40 thresholds in
the build commit. Do NOT ship an unscaled term.

## 3. Thesis B — `qing_xinjiang_control` ← the concrete Xinjiang layer (ONE-WAY derive; concrete rewards §5)
Target derives from real objects the ILI/#367 systems + the mission beats place. ⚠️ **CRIT-2 still holds; CRIT-3
is RESOLVED by the concrete-reward reframe (§5), which flips secured/contested from OUTPUT to a beat-stamped
INPUT:**
- ✅ **secured/contested province modifiers are now one-way INPUTS (revised §5).** They were OUTPUTS of
  control only because `QING_ili_apply_prov_band` stamped them FROM control≥70/≤20. Under the concrete-reward
  reframe, the STORY BEATS stamp them DIRECTLY and `apply_prov_band` is retired as a control→province stamper
  — so the loop is broken and control can derive FROM them one-way. Count `qing_xinjiang_prov_secured` (+) and
  `qing_xinjiang_prov_contested` (−) over the oasis areas.
- ❌ **do NOT count `qing_military_colony_building` as "tuntian" — the de-dup was FALSE** (CRITICAL 2). The
  building (食-capacity garrison-feed HQ, seeded at 7 frontier provinces, only 2 in the oases) and the
  `qing_xj_tuntian` counter (Dzungaria-only colonization lever, cap 8, `se_QING_XINJIANG.txt:243-275`) are
  DIFFERENT mechanics. The counter has live readers (mission `qing_xinjiang_missions.txt:133`, panel
  `QING_xinjiang_panel.txt:43`, consolidation `se_QING_XINJIANG.txt:213`). **KEEP the counter; read
  `var:qing_xj_tuntian` (O(1)) as the colony term. Do NOT retire it, do NOT substitute a building count.**

Concrete inputs (all proven, ONE-WAY — nothing derives these FROM control; §5 stamps them):
```
control_target =
      W_ili   × [ exists = c:ILI AND c:ILI = { is_subject_of = ROOT } ]   # 1/0, the big signal (:458 proven)
    + W_beg   × var:qing_xj_beg_count                                     # 0..5, proven var (:74/124/153)
    + W_tun   × var:qing_xj_tuntian                                       # 0..8, proven counter (KEEP, CRIT 2)
    + W_sec   × (count qing_xinjiang_prov_secured over oasis areas)       # beat-stamped, §5 (was CRIT-3 output)
    + W_front × [ has_country_modifier = qing_ili_frontier_secured ]      # zeng/reconquest win referent
    − W_cont  × (count qing_xinjiang_prov_contested over oasis areas)     # beat-stamped degrade
    (clamped 0..100; drift the live meter toward it, as today)
```

### §3a — MANDATORY: rework `qing_xj_consolidation` in the SAME commit (CRITICAL 4) — USE OPTION (b)
`QING_xj_recompute_consolidation` (`se_QING_XINJIANG.txt:205-232`) today = `control(base :206) + 4·begs +
3·tuntian + 8·xiexiang − 6·venal`. If control becomes `f(begs, tuntian)`, then consolidation counts begs &
tuntian **twice**, and it folds into the Lifan Yuan council office (`se_QING_MINISTRY.txt:367`) → the
double-count reaches the Grand Council.

⚠️ **USE OPTION (b) — the re-review proved option (a) breaks two missions (NEW CRITICAL, 2026-08-06).**
- ❌ **Option (a) — DROP the control base at `:206`** — DO NOT. Consolidation would then = begs+tuntian+
  xiexiang−venal, **max ≈ 56** (begs 20 + tuntian 18 + xiexiang 8 + law bias 10). But two mission gates read
  consolidation at high thresholds: `qing_xj_pacify >= 75` (`qing_xinjiang_missions.txt:188`) and the
  capstone `qing_xj_integrate >= 85` (`:212`). With the base gone, the score can't exceed ~56 → **both gates
  become permanently unreachable**, and `qing_xj_fully_integrated` (`QING_xj_pulse:397`) never gets set.
  These two reads were OMITTED from the §6 census — the same incomplete-census error CRIT 4 itself was.
- ✅ **Option (b) — KEEP the control base at `:206`, DROP the `+4·begs` (`:208-210`) + `+3·tuntian`
  (`:213-216`) terms.** This removes the double-count (begs/tuntian now enter consolidation ONLY through the
  control base) while preserving the ~0-100 scale the 75/85 gates were calibrated against. Control stays the
  headline grip meter; consolidation = control + xiexiang − venal + admin_bias.
Add BOTH mission reads (`:188`, `:212`) PLUS `:206` + the Ministry fold to the §6 census.

### §3b — 1763 opening (MEDIUM 4)
control seeds **40** (`se_QING_ILI.txt:63`); consumers gate ≥70 (grip firm, `:281`), ≤30 (khoja-scare,
`se_QING_XINJIANG.txt:439`), ≤20 (`:286`). At 1763: ILI is a live subject (big +), 2 seeded begs
(`:86-87`), 0 tuntian, low unrest. **Pick weights so the target lands ~40, NOT ≥70** (else `grip_firm`
trips at game start and the khoja-scare ≤30 path is unreachable). Show the arithmetic. E.g. with
`W_ili≈30, W_beg≈4, W_tun≈3`: 30 + 4×2 + 0 = 38 ≈ seed. Tune against the bands; document.

## 4. Break the circular loop — writers to cut vs KEEP (CORRECTED, MEDIUM 2)
⚠️ **Only the AUTOMATIC per-pulse coupling is cut; player levers are PRESERVED as overrides** (the first
draft over-cut).
- **CUT** (the loop): caravan `:219 (+1 @ prosperity≥70)` / `:226 (−1 @ <30)` — automatic feedback. And
  caravan READS control `:97` — REMOVE (Thesis A drops it).
- **KEEP as event/lever overrides** (discrete player-action consequences, NOT the loop): `:403 (−6,
  QING_caravan_revoke_aqsaqal)` and `:428 (+4, QING_caravan_military_escort)`. These are levers with a
  price/payoff — same override treatment as the §5 story beats. Deleting them silently strips two levers.
- **Full control-writer census a re-derive must reconcile (the first draft's list was INCOMPLETE):** ILI arc
  `se_QING_ILI.txt:63/98/125/153/210/232` (STORY BEATS — §5), #367 `se_QING_XINJIANG.txt:264/292/339/359/
  373/409/414/542`, missions `qing_xinjiang_missions.txt:104/168/193`, **PLUS** `qing_caravan_events.txt:87
  (−4)/:175 (−3)`, `qing_ili_events.txt:185 (set 60)`, `qing_xinjiang_events.txt:57 (+12)/:69 (−10)` — all
  write control; keep as lever/story overrides, they are not the automatic loop.
- ⚠️ **CUT the #367 levers' DIRECT control nudges — they double-apply into the derive (NEW MEDIUM, 2026-08-06).**
  `QING_xj_plant_tuntian` does `tuntian +1` (`:255`) **AND** `control +5` (`:264`); `QING_xj_appoint_beg` does
  `beg_count +1` **AND** `control +4` (`:292`). Under Thesis B, `control_target = W_beg·beg_count +
  W_tun·tuntian + …`, so each lever pushes control up TWICE — once as the instant nudge, once by raising the
  derive target the meter drifts toward (the exact CRIT-4 double-count class). **DROP the `:264`/`:292` direct
  control nudges** — the begs/tuntian increment already moves control through the derive. (The 30-treasury
  cost + the tuntian/beg increment stay; only the redundant control nudge goes.)

## 5. The story beats — RESOLVED: mission rewards produce CONCRETE outcomes, control DERIVES (USER 2026-08-06)
> **This dissolves the entire floor/cooldown problem.** The earlier drafts fought a losing battle: the beats
> SET the abstract meter (control=80/90) and a per-pulse derive dragged it back. The clean fix (user):
> **the win/loss beats stamp REAL objects; control is a one-way derive from those objects.** No SET to fight,
> no `max`-floor, no cooldown — control rises because the MAP changed, and falls when the map is lost. This
> is the concrete-over-abstract rule applied to the mission REWARDS, not just the meter.

Per-beat concrete rewrite (each beat DROPS its `set control = N` / nudge and instead places the object the
derive reads):
- **reconquest-win** (`:125`, was `set control = 80`) — **stamp `qing_xinjiang_prov_secured` on the oasis
  provinces DIRECTLY** (not via the control→band path — see the loop-break note below), close the Dungan
  rising (already does). Control then derives UP from the newly-secured provinces. Also stamp a durable
  `qing_ili_reconquered` country modifier as the "won the field" referent.
- **zeng-triumph** (`:232`, was `set control = 90`) — already stamps `qing_ili_frontier_secured` (`:240`);
  KEEP that, DROP the `set control = 90`, and stamp the full secured-province set. Control derives to its
  apex from frontier_secured + all-oases-secured + ILI-subject + begs + tuntian.
- **reconquest-fail** (set 10) / **ratify-livadia** (−25) — stamp `qing_xinjiang_prov_contested` on oasis
  provinces (the concrete "grip slipping" object); control derives DOWN from the contested stamp.
- **choose-coast** (set 0 → `release_subject c:ILI`, `:459`) — already concrete: releasing ILI drops the
  `c:ILI = { is_subject_of = ROOT }` term, control collapses naturally. No change.
- **integrate-fully** (100) — already safe (`QING_xj_pulse` early-returns on `qing_xj_fully_integrated`).

⚠️ **The one-way discipline (resolves CRIT-3 + the old loop):** today `QING_ili_apply_prov_band` stamps
secured/contested FROM control (`control≥70 → secured`, `se_QING_ILI.txt:315-383`). If control also derives
FROM secured, that's a loop. **Fix: the STORY BEATS stamp secured/contested directly; `apply_prov_band` is
retired as a control→province stamper** (or reduced to non-control cosmetic). Then the flow is strictly
one-way: beats + levers → concrete objects (secured provs, begs, tuntian, ILI-subject, frontier modifiers)
→ control derives. The derive READS these; nothing derives the objects FROM control.
- Control-derive terms (all concrete, one-way): `W_ili·(c:ILI is_subject_of ROOT)` + `W_beg·beg_count` +
  `W_tun·tuntian` + `W_sec·(count of qing_xinjiang_prov_secured over the oasis areas)` +
  `W_front·(has qing_ili_frontier_secured)` − `W_cont·(count of qing_xinjiang_prov_contested)`.
- 1763 opens ~40 (§3b): ILI-subject + 2 begs, no secured/contested/frontier stamps yet → weights tuned so
  the base lands ~40, matching the seed. A win beat stamping the secured set pushes it to ~80-90 concretely.

## 6. Consumers (FULL census — CORRECTED to include the double-count sites)
- control: `se_QING_ILI.txt:281/286/319` (≥70/≤20 bands + prov modifiers), `se_QING_XINJIANG.txt:439` (≤30),
  **`se_QING_XINJIANG.txt:206` `QING_xj_recompute_consolidation` (the base term — §3a)**, **the Lifan Yuan
  council fold `se_QING_MINISTRY.txt:367` (via consolidation)**.
- **`qing_xj_consolidation` gates (were OMITTED — the option-a break): `qing_xinjiang_missions.txt:188`
  (`qing_xj_pacify >= 75`) + `:212` (`qing_xj_integrate >= 85`).** Option (b) keeps these reachable (§3a);
  re-verify both open reachable after the rework.
- caravan_prosperity: ultimatum ≥55 (`se_QING_CARAVAN.txt:252`) / crisis ≥40 (`:267`) bands + the #32
  customs-income reads.
Verify all after re-derive.

## 7. Build checklist (TWO commits — caravan and control are separable)
COMMIT A — caravan_prosperity ← oasis trade (Thesis A): author `QING_caravan_oasis_trade_svalue` (area:
+ every_area_province + bare num_goods_produced, §1/§2); set the var; remove the `control/4` term (`:97`);
scale S so 1763 target ≈ 45 (§2a, show arithmetic); verify no #32 double-count.
COMMIT B — xinjiang_control ← concrete ONE-WAY derive (Thesis B + concrete-reward §5): target =
W_ili·(ILI-subject) + W_beg·beg_count + W_tun·tuntian + W_sec·(secured-prov count) + W_front·(frontier_secured)
− W_cont·(contested-prov count); weights so 1763 ≈ 40 (§3b). **CONCRETE-REWARD REWRITE (§5):** the win/loss
beats DROP their `set control = 80/90/10/−25` and instead stamp the real objects (secured/contested provs,
frontier_secured, reconquered modifier); RETIRE `QING_ili_apply_prov_band` as a control→province stamper so
the derive can read secured/contested one-way (breaks the old loop AND CRIT-3). CUT caravan `:228/:235`
control writes + the #367 lever direct control nudges `:264/:292`; KEEP the treasury cost + beg/tuntian
increments. **Rework `QING_xj_recompute_consolidation` (§3a option-b: keep control base, drop begs/tuntian
terms) in THIS commit.**

Review gates (both): **area: iteration NOT every_owned_province (CRIT 1)**; num_goods_produced via
script_value bare-scope read NOT prev. (MED 1); **tuntian counter KEPT, no false building de-dup (CRIT 2)**;
**secured/contested NOT read as control inputs (CRIT 3)**; **consolidation reworked same commit, no
Grand-Council double-count (CRIT 4)**; loop broken (no caravan↔control) but levers `:403/:428` preserved
(MED 2); story-beat WIN-referent resolved via frontier_secured floor (MED 3); 1763 openings shown against
bands (MED 4); no TZ-balance; consumers incl. `:206`/Ministry verified; RHS-cmpsvalue; brace/quote/BOM;
boot-crash review.

## 8. Review-finding tracker (round 1: 4 CRITICALs; round 2: 1 new CRITICAL + 2 MEDIUM + 1 LOW)
Round-1 fixes (all CONFIRMED SOUND by the re-review):
- **CRIT 1 (every_owned_province→0):** FIXED §1 — all sweeps `area:Dzungaria/Tarim + every_area_province`.
- **CRIT 2 (false tuntian de-dup):** FIXED §3 — counter KEPT, read `var:qing_xj_tuntian`; no building count.
- **CRIT 3 (secured/contested self-loop):** RESOLVED via concrete-reward (§5, USER 2026-08-06) — beats stamp
  secured/contested DIRECTLY, apply_prov_band retired as a control→province stamper, so control derives from
  them ONE-WAY (no loop). Cleaner than the round-1 "cut as inputs" — they're now a genuine concrete signal.
- **CRIT 4 (consolidation double-count):** diagnosis right; option-b remedy (round-2 CRIT-5).

## §9 — CONCRETE-REWARD RESOLUTION (USER 2026-08-06) supersedes the §5 floor/cooldown machinery
The whole "story-beat SET fights the derive → need a max-floor + cooldown" problem is DISSOLVED by making the
mission rewards produce CONCRETE outcomes instead of setting the abstract meter. Win beats stamp real objects
(secured provinces, frontier_secured, reconquered modifier); loss beats stamp contested provinces; control
DERIVES one-way from the map. No SET to fight, no floor, no cooldown. The earlier §5 (max-floor at both win
beats) is OBSOLETE — kept below struck-through for history. This also makes the derive genuinely
concrete-over-abstract at the REWARD layer, matching the program's intent.

Round-2 findings (the re-review of the rewrite):
- **NEW CRIT-5 (option-a killed 2 missions):** FIXED §3a — my recommended remedy (drop the control base)
  capped consolidation at ~56, making `qing_xj_pacify >= 75` + `qing_xj_integrate >= 85` unreachable
  (census had OMITTED `qing_xinjiang_missions.txt:188/212`). **Switched to option (b)** (keep base, drop the
  begs/tuntian terms) + added both mission reads to §6.
- **NEW MED (lever double-apply):** FIXED §4 — DROP the `:264`/`:292` direct control nudges on
  plant_tuntian/appoint_beg (the begs/tuntian increment already moves control via the derive).
- **NEW MED (floor not a floor + one beat only):** FIXED §5 — `max`-clamp floor (not additive), and stamp a
  durable modifier at reconquest-win too (not just zeng-triumph), driving the floor off it.
- **LOW (customs drag in arithmetic):** FIXED §2a — the −5 `customs_rate=1` drag means S×oasis ≈ 10, not ~5.
- MED 1 (read form): FIXED §2 (script_value, CONFIRMED sound). MED 4 (1763 openings): FIXED §2a/§3b.
