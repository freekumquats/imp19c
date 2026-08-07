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

## §10 — CONVERT EVERY CONTROL-WRITER TO CONCRETE (USER 2026-08-06; supersedes "keep as override")
The review round-3 found ~24 control-writers; the earlier plan converted only the 6 Ili beats and left ~8
nudge-writers fighting the one-way derive (HIGH-3), incl. xiexiang (the key grip lever) with NO derive term.
**USER decision: convert ALL of them to concrete.** control becomes a PURE one-way derive; every writer
either (a) already changes a real object beside its nudge → drop the nudge, derive reads the object, or
(b) has no object → give it a concrete stamp, or delete if redundant. Full writer→concrete map:

**New derive term needed:** `+ W_xiexiang × [ has_country_modifier = qing_xj_xiexiang ]` (the 協餉 subsidy is
a real, paid, standing country modifier — the single most important grip lever; it MUST be a derive term or
paying it is inert). So the full target:
`control_target = W_ili·ILI-subject + W_beg·beg_count + W_tun·tuntian + W_sec·secured-count
                  + W_front·frontier_secured + W_xiexiang·xiexiang − W_cont·contested-count`.

| Writer (site) | Real object it already changes | Conversion |
|---|---|---|
| xiexiang_on `+6` / _off `−6` (`se_QING_XINJIANG.txt:359/373`) | `qing_xj_xiexiang` country modifier (add/remove) | DROP nudge → add `W_xiexiang·xiexiang` derive term |
| appoint_beg `+4` (`:292`) | `qing_xj_beg_count +1` | DROP nudge (derive reads beg_count) |
| plant_tuntian `+5` (`:264`) | `qing_xj_tuntian +1` | DROP nudge (derive reads tuntian) |
| discipline_beg `+3` (`:339`) | removes `qing_is_xj_beg`/`qing_xj_beg_venal` (↓venal, changes beg quality) | DROP nudge (derive reads beg_count; add a `−W_venal·venal_count` term if venal grip-drag must survive) |
| pulse maint `+1` / neglect `−1` (`:409/414`) | none (pure drift on xiexiang+beg state) | DELETE — the derive already reflects xiexiang + beg_count, so this is redundant double-count |
| reconquest-win `set 80` (`se_QING_ILI.txt:125`) | (today) apply_prov_band | stamp secured provs DIRECTLY + `qing_ili_reconquered` modifier; DROP set |
| zeng-triumph `set 90` (`:232`) | `qing_ili_frontier_secured` (kept) | stamp full secured set; DROP set |
| reconquest-fail `set 10` (`:153`) / ratify `−25` (`:210`) | (today) apply_prov_band | stamp contested provs DIRECTLY; DROP set/nudge |
| choose-coast `set 0` (`:98`) | `release_subject c:ILI` (already) | DROP set (ILI-subject term collapses); KEEP apply_prov_band's contested stamp here (CRIT-1 caller) |
| qing_ili.4 compromise `set 60` (`qing_ili_events.txt:185`) | apply_prov_band | stamp PARTIAL secured + some contested; DROP set (CRIT-2) |
| integrate_fully `set 100` (`se_QING_XINJIANG.txt:542`) | apply_prov_band (`:544`, stamps whole oasis secured) | KEEP the secured stamp; DROP set; fully_integrated lock already freezes the pulse |
| mission nudges `+6/+8/+6` (`qing_xinjiang_missions.txt:104/168/193`) | mission-specific (verify each: beg appt / tuntian / xiexiang?) | route to the concrete object the mission task represents; DROP nudge |
| caravan levers `−6/+4` (`se_QING_CARAVAN.txt:412/437`) | revoke-aqsaqal / military-escort | escort → stamp secured or +beg; revoke → +contested; DROP nudge |
| caravan auto `+1/−1` (`:228/235`) | none (prosperity↔control loop) | DELETE (loop-break, already planned) |
| xinjiang_events `+12/−10` (`qing_xinjiang_events.txt:57/69`) | khoja-scare resolve/worsen | stamp secured/contested; DROP nudge |

**CRIT-1 (apply_prov_band's 4 extra callers) is now RESOLVED cleanly:** do NOT retire apply_prov_band as an
effect — instead RE-PURPOSE it as the shared "stamp secured/contested provinces" helper the beats call
DIRECTLY (it already does the mutual-exclusion clear + area iteration). Only its CONTROL-BAND TRIGGER changes:
today it stamps based on `control ≥70/≤20`; instead the BEATS pass it an explicit secured|contested intent.
This keeps all 6 callers (win/fail/ratify/zeng/choose-coast/integrate-fully) working, preserves the
mutual-exclusion + mid-range self-clear bookkeeping (the stuck-secured bug guard), and breaks the loop
(it no longer reads control). One-way flow: beats → apply_prov_band(intent) → secured/contested provs →
control derives. This is BETTER than "retire it" — reuses the proven bookkeeping instead of re-implementing it.

**HIGH-4 reachability (the ≥85 capstone):** with xiexiang now a derive term (`+W_xiexiang`), recompute the
control ceiling: `W_ili + 5·W_beg + 8·W_tun + secured-count·W_sec + W_front + W_xiexiang`. With the win-beat
secured stamps + frontier + xiexiang all live, control reaches ~100, so consolidation (control base + xiexiang
+ admin_bias − venal) clears 85 under ALL admin-law biases. MUST show the arithmetic per bias in build.

**Weights to pin (build):** W_ili, W_beg, W_tun, W_sec, W_front, W_xiexiang, W_cont, W_venal — sized so
1763 opens ~40 (ILI-subject + 2 begs, no xiexiang/secured yet) AND a fully-won+subsidised frontier ~90-100.
Build-probe LOG the derive components. This is the largest single commit in the cluster; re-review before build.

## §11 — FINAL DESIGN (USER 2026-08-06): concrete derive + CHANGE the downstream mechanics to read concrete state
Grounded in the full deep-read census (all 26 writers, 8 apply_prov_band callers, 9 landmines — see
overnight log). The guiding correction: **do NOT contort the derive to reproduce the old accumulator's
behavior (the ≤30 ratchet, the 70/20 bands). If the abstract meter's downstream mechanics no longer fit a
concrete derive, CHANGE THOSE MECHANICS to read the concrete state directly.** control becomes a pure
one-way derive; everything that used to read the accumulator's artifacts is re-pointed at real objects.

### 11.1 The derive (pure one-way, no drift)
`qing_xinjiang_control` recomputed each pulse (in QING_xj_pulse, before consolidation) as:
```
control = clamp(
    W_ili   · [ c:ILI exists AND is_subject_of ROOT ]      # the spine
  + W_beg   · qing_xj_beg_count                             # rebuilt-each-recompute, clean (D)
  + W_tun   · (COUNT qing_xj_tuntian_colony prov modifiers over Dzungaria+Tarim)   # real modifiers, NOT the
                                                            #   possibly-stale qing_xj_tuntian int (fixes D1)
  + W_xiexiang · [ has_country_modifier = qing_xj_xiexiang ]                       # the paid grip lever (HIGH-3)
  + W_sec   · (COUNT qing_xinjiang_prov_secured over the areas)                    # beat-stamped (§5)
  + W_front · [ has_country_modifier = qing_ili_frontier_secured ]                 # gives D2's orphan a reader
  − W_venal · qing_xj_beg_venal_count
  − W_cont  · (COUNT qing_xinjiang_prov_contested over the areas)
, 0, 100)
```
NO target+drift, NO QING_DECLINE_nudge accumulation — a straight `set_variable` from the concrete state each
pulse. (The other meters use target+drift because their referents are noisy character stats; Xinjiang's
referents are discrete on/off objects, so a direct derive is stabler and truer here.)

### 11.2 KEEP the khoja trigger `control ≤ 30` — and make NEGLECT DEGRADE THE CONCRETE (Option A, USER 2026-08-06)
⚠️ **The khoja revolt happens because control is LOW — KEEP `control ≤ 30` as the trigger.** But the re-review
found the naive claim "a neglected frontier just derives ≤30" is FALSE for a BUILT frontier (CRITICAL-2): the
concrete positives are PERMANENT — `qing_xinjiang_prov_secured` + `qing_xj_tuntian_colony` are `duration=-1`,
ILI stays a subject during neglect (`W_ili` floor), and nothing removes them. So `W_ili + W_tun·colonies +
W_sec·secured` is a permanent floor control can't fall below, AND passive neglect stamps NO contested (only
the late Ili-crisis beats + caravan do), so the `−W_cont` term is 0 exactly when neglect matters. Deleting the
−1/pulse ratchet removed the only walk-down. Net: khoja was UNREACHABLE for any frontier that ever built.

**The principle-correct fix (USER: Option A — "change the concrete, abstract follows"): sustained neglect
must DEGRADE THE REAL OBJECTS, so control derives low because the MAP actually rotted.** New pulse mechanic in
`QING_xj_pulse` (replaces the deleted −1/pulse abstract ratchet). ⚠️ **ROT GATE = `NOT xiexiang` ALONE (USER
2026-08-06, round-5 fix): cutting the subsidy ALWAYS rots the garrison; begs modulate the RATE, not whether.**
The earlier `(beg_count=0 OR venal>0)` gate was historically backwards + a consequence-free hole (a loyal-beg
frontier could cut xiexiang forever with no rot). xiexiang paid the Manchu/Green-Standard GARRISON, not the
begs (1826 Jahangir: loyal begs, hollow unpaid garrison). So the garrison rots whenever unpaid; a loyal beg
corps only BUFFERS the bleed (delays each rot-tick), it can't stop it.
```
# NEGLECT ROT — an unpaid frontier garrison hollows out and mutinies. Gated on NO xiexiang alone.
if = {
    limit = { NOT = { has_country_modifier = qing_xj_xiexiang }        # garrison unpaid
              NOT = { has_variable = qing_xj_fully_integrated } }
    change_variable = { name = qing_xj_neglect_quarters  add = 1 }
    # begs modulate the RATE via the rot threshold (loyal corps = slower bleed; bare/venal = fast collapse):
    #   rot_threshold = 8 if beg_count>=3 AND venal=0   (loyal buffer, ~2yr/tick → ≤30 in ~10-14yr)
    #                 = 4 if 1-2 begs or a mix
    #                 = 2 if beg_count=0 OR venal>0      (no buffer, fast → ≤30 in ~2-3yr; the pre-1826 case)
    # (compute rot_threshold into a scratch var from the beg state, then compare — PLACEHOLDER-playtest values)
    if = {
        limit = { var:qing_xj_neglect_quarters >= <rot_threshold> }
        # flip ONE secured oasis prov → contested (random_area_province over Dzungaria+Tarim, limit
        # has_province_modifier=qing_xinjiang_prov_secured; remove secured + add contested — the proven
        # mutual-exclusion stamp). AND decay ONE tuntian_colony: remove_province_modifier qing_xj_tuntian_colony
        # from a random Dzungaria province that has it, AND ⚠️ change_variable qing_xj_tuntian subtract=1
        # (round-5 HIGH fix: the int MUST track the modifier removal or the plant guard var:qing_xj_tuntian<8
        # soft-locks re-planting — int=8 while only 7 colonies exist). random_area_province (NOT
        # ordered_area_province — the proven in-file iterator, se_QING_XINJIANG.txt:250-260).
        <flip 1 secured→contested; remove 1 qing_xj_tuntian_colony AND decrement qing_xj_tuntian>
        set_variable = { name = qing_xj_neglect_quarters  value = 0 }   # reset after each tick (slow bleed)
    }
}
else = { set_variable = { name = qing_xj_neglect_quarters  value = 0 } }   # xiexiang resumed → clock resets
```
As secured provinces flip and colonies decay, control DERIVES down (both `+W_sec`/`+W_tun` shrink AND
`−W_cont` grows — a double swing per flip), crossing 30 after enough neglected quarters — for a BUILT frontier,
not just a bare one. Then:
- **KEEP** the khoja arm `control ≤ 30 AND (beg_count = 0 OR venal > 0)` + the event `≤30` re-check — they now
  read a meter that genuinely reaches ≤30 via real map rot.
- **DELETE** the −1/pulse abstract ratchet (writers #13/#14) — the concrete rot replaces it.
- **Reversibility (round-5 HIGH fix):** resuming xiexiang resets the neglect clock + STOPS rot, and because
  the int now tracks the modifier, the player CAN re-plant decayed colonies (int<8 again) and re-secure
  flipped provinces (via the mission secured-stamp, §11.6) — at treasury+time cost. Lasting but recoverable.
- E1 defensive-clear preserved: arrest neglect during the event delay → control re-derives >30 → scare cancels.
This is the principle end-to-end: neglect rots the MAP (concrete), control MODELS the rotted map (abstract
follows), the `≤30` reader fires because grip is genuinely low. rot_threshold values = PLACEHOLDER-playtest.

### 11.3 CHANGE the province bands — beats stamp them, control no longer sets them (fixes C/G loop + unbanded)
Re-purpose `QING_ili_apply_prov_band` per §10 (beats pass explicit secured|contested intent; it keeps its
mutual-exclusion + self-clear bookkeeping). ALL 8 callers (incl. `:466 break_ili_free` and `:190 compromise`
— the two I kept missing) get an intent (see §11.6 table). The `control ≥70/≤20` band TRIGGER is deleted —
provinces are banded by the story beats' concrete intent, so the "mid-range leaves the map unbanded" problem
(compromise=60, ratify) vanishes: compromise stamps a MIX (see §11.6), not a blank.

### 11.4 CHANGE the integration lock — extend it to the caravan writers (fixes H1)
`qing_xj_fully_integrated` currently freezes only QING_xj_pulse; caravan revoke/couple/refuse still move
control + re-arm khoja post-integration. Gate the caravan control-affecting paths (revoke_aqsaqal, the ±1
couple, qing_caravan.1 refuse's khoja-set) on `NOT has_variable = qing_xj_fully_integrated` too, so the
"henceforth a normal province" end-state actually holds.

### 11.5 Consolidation — option-b CORRECTED: drop ALL terms now in the control base (fixes CRITICAL-1)
⚠️ **CRITICAL-1 (re-review): option-b as first written re-created the CRIT-4 double-count.** §10 widened
`control` to include `+W_xiexiang·xiexiang` and `−W_venal·venal`. Consolidation today =
`control + 4·begs + min(3·tuntian,18) + 8·xiexiang − 6·venal + admin_bias` (`se_QING_XINJIANG.txt:206-225`).
Dropping only the begs/tuntian terms (as §3a said) LEAVES `+8·xiexiang` (`:218-221`) and `−6·venal`
(`:223-225`) — but `control` NOW ALREADY CONTAINS xiexiang + venal → both double-counted into the Lifan Yuan
fold (`se_QING_MINISTRY.txt:365-371`, term c) → the Grand Council. **Fix: consolidation must DROP every term
that now enters through the control base — begs, tuntian, xiexiang, AND venal** — leaving simply:
`qing_xj_consolidation = control + admin_bias` (clamped). Every concrete input enters exactly once, via
control. Re-derive the ≥85 capstone / ≥75 pacify reachability against THIS (§11.7) — the earlier check was
inflated by the double-count, so it must be recomputed honestly.

### 11.6 All 26 writers → concrete (supersedes §10 table; every caller enumerated)
- **xiexiang on/off, appoint_beg, plant_tuntian, discipline_beg:** DROP the control nudge; the object they
  already change (xiexiang modifier / beg_count / tuntian_colony modifier / venal flag) is a derive term.
- **pulse maint/neglect ±1 (#13/#14):** DELETE (the ratchet's only job was walking the accumulator down to
  ≤30; now the concrete derive of a neglected frontier LANDS ≤30 directly, so the khoja trigger `control ≤ 30`
  is kept and correct without the walk — §11.2).
- **8 apply_prov_band callers → explicit intent:** win/zeng/integrate = SECURED; fail/ratify/choose-coast/
  break_ili_free = CONTESTED; **compromise (`:190`) = MIXED** — a new `QING_ili_apply_prov_band_mixed` (stamp
  ~half the oases secured, rest contested) so control derives to ~mid (≈60 equivalent) without a `set 60`.
- **mission nudges — ⚠️ do NOT use a fort-count derive term (MED-3, re-review): geometry + writer both fail.**
  fortify plants `qing_frontier_fort_building` over `is_in_region = Turkestan` — which is Dzungaria + KAZAKH
  STEPPE areas and does NOT contain Tarim (Tarim is in the Gansu region). So a fort-count "over Dzungaria+Tarim"
  misses Tarim forts AND the beat can land its fort on a steppe province outside the counted set. WORSE,
  `qing_frontier_fort_building` is stamped by SIX effects (settle-frontier, central-asia/burma/new-world
  missions) — a count would pick up non-Xinjiang forts (a new uncounted-writer problem). **Instead: the three
  mission tasks stamp a Xinjiang-specific concrete object the derive already reads** — fortify → stamp a
  `qing_xinjiang_prov_secured` on an oasis; governor → mark `qing_xj_governed` while a capable Lifan Director
  sits (fold into the beg term — governor ≈ +1 effective beg — rather than a brand-new unimplemented derive
  term); pacify → stamp secured on a contested oasis. DROP all three control nudges; NO fort-count term.
  ⚠️ **The secured-stamp MUST use `area:Dzungaria`/`area:Tarim` + `random_area_province` (round-5 MED fix)** —
  NOT the missions' current `any_owned_province { is_in_region = Turkestan }` idiom, which (a) EXCLUDES Tarim
  (Tarim is in the Gansu region, not Turkestan) and (b) returns nothing for subject-held oases (the CRIT-1
  every_owned_province→0 blocker). Reuse the re-purposed `QING_ili_apply_prov_band(secured)` helper (§11.3),
  which already area-iterates correctly, rather than a fresh mission-local stamp that would re-inherit CRIT-1.
- **caravan revoke/escort/couple + caravan.1 refuse:** escort → +beg or secured stamp; revoke → contested
  stamp; DROP the ±1 couple (loop); all gated on NOT fully_integrated (§11.4).
- **⚠️ caravan.2 LAPSE `−3` (`qing_caravan_events.txt:175`) — MISSED in the prior table (MED-4).** The route-cut
  crisis's lapse option nudges control −3; under the pure derive it's a stray writer clobbered next pulse.
  Convert: lapse → stamp a contested oasis (the road's insecurity is real) OR fold into the prosperity drop it
  already applies; DROP the control nudge.
- **xinjiang.1 suppress/fester:** suppress → clear a contested / +order; fester → already turns a beg venal
  (concrete) → DROP nudge.
- **LOW-5:** `QING_xj_integrate_fully` must ALSO `remove_variable = qing_xj_khoja_pending` — a scare pending at
  the moment of integration currently survives (and `qing_caravan.2`'s trigger isn't integration-gated), so a
  route-cut can fire post-integration off a stale flag. Clear it in the capstone.
- **LOW-6:** under the intent model no caller passes a "neutral/clear" intent, so `apply_prov_band`'s mid-range
  self-clear else-branch (`se_QING_ILI.txt:356-382`) becomes dead code. Either DELETE it, or give the MIXED
  helper a defined clear step. Don't claim it's "preserved" — it isn't exercised.

### 11.0 THE PRINCIPLE (USER 2026-08-06) — the whole program in one rule
**Abstract is a useful PROXY for concrete. Abstract FOLLOWS concrete; abstract MODELS concrete. WITHOUT a
concrete referent, an abstract meter is USELESS and should be DELETED.** Three cases:
- **Concrete referent exists → CONCRETIZE:** make the abstract a faithful function of the real objects
  (this is control — §11.1). It becomes an honest proxy; every downstream reader keying on it is correct
  for free; nothing drives the concrete FROM the abstract.
- **No concrete referent → DELETE** (not "leave abstract"), as a FORWARD rule for new work: a free-floating
  accumulator that models nothing real is not worth adding/keeping. ⚠️ This does NOT mean ripping out
  already-shipped meters (#5 sect, #7 tributary are closed + stable) — deleting live meters and migrating
  their consumers now would inject regressions into working committed state for a philosophy cleanup, which
  we do NOT do. The rule guides FUTURE concretization decisions; closed work stays as-is unless the user
  explicitly asks to revisit it.

control specifically: an abstract readout that MODELS the concrete grip and FOLLOWS it — it never drives the concrete.
The real state is the objects: ILI subjecthood, begs, tuntian colonies, the xiexiang subsidy, secured/
contested provinces, frontier_secured. control = a faithful function of those (§11.1). Because it models them
faithfully, every downstream reader that keys on the abstract ("grip firm ≥70", "grip low ≤30", consolidation
base) is correct FOR FREE — no reader changes its threshold; the meter under it just became honest. Anything
that used to DRIVE the concrete FROM the abstract (province bands stamped from control≥70/≤20) is inverted:
the concrete is set by real events, control follows. This is the single rule the whole §11 rewrite serves.

### 11.7 Weights + 1763 opening + ceiling (build-probe; recomputed against CORRECTED consolidation)
Constraints the weights must jointly satisfy (build-probe LOG the components, pin against real 1763 values):
- **1763 open ≈ 40:** ILI-subject + 2 seeded begs, no xiexiang/secured/tuntian → `W_ili + 2·W_beg ≈ 40`.
- **Neglect reaches ≤30 — now via §11.2 concrete ROT, not weights alone:** the neglect-rot mechanic flips
  secured→contested and decays tuntian over sustained-neglect quarters, so even a built frontier's positives
  ERODE (the permanent-floor problem is fixed by removing the objects, not by shrinking W_ili). So W_ili need
  NOT be ≤30 — the rot walks control down regardless. (This is what makes the ≤30 claim actually hold; §11.2.)
- **Full build ceiling ~100:** secured set + frontier_secured + xiexiang + tuntian + loyal begs → clamps 100.
- **⚠️ ceiling recomputed against the CORRECTED consolidation `= control + admin_bias` (§11.5, no double-count):**
  ≥85 capstone (`qing_xinjiang_missions.txt:212`) needs `control + admin_bias ≥ 85` → at full build control ~100,
  clears under all 3 biases (provincialize +10 / military-farm +5 / beg-indirect 0). ≥75 pacify (`:188`) likewise.
  Since the inflated `+8 xiexiang −6 venal` terms are GONE, control itself must reach ~85+ at capstone-time — verify
  the weight sum (W_ili+5·W_beg+8·W_tun+W_xiexiang+W_front+secured·W_sec) clamps high enough. SHOW this arithmetic
  in the build commit; it was previously masked by the double-count.

### 11.8 Landmine disposition (all 9 from the deep read)
1 accumulator→derive: FIXED (§11.1). 2 ≤30 reachability: FIXED by the CONCRETE NEGLECT-ROT mechanic (§11.2,
Option A) — sustained neglect flips secured→contested + decays tuntian so a built frontier's positives ERODE
and control genuinely reaches ≤30; the `≤30` trigger is KEPT. (The earlier "weights alone reach ≤30" was
WRONG — CRITICAL-2 — because the concrete positives were permanent.) 3 loop: FIXED (§11.3). 4 mid-range
unbanded: FIXED (§11.3/§11.6 mixed stamp + LOW-6 clear). 5 partial integration lock: FIXED (§11.4 + LOW-5
clears khoja_pending). 6 orphaned frontier_secured: FIXED (modelled term, §11.1). 7 tuntian drift: FIXED
(reads real modifiers, §11.1). 8 khoja_pending leak: FIXED (§11.2 defensive clear + §11.6 LOW-5 capstone
clear). 9 stale-read lag: unchanged/intended.

### 11.9 Re-review round-4 findings folded (2 CRITICAL + 2 MED + 2 LOW)
- CRIT-1 (xiexiang/venal double-count into consolidation→Grand Council): FIXED §11.5 — consolidation drops
  ALL base-included terms → `control + admin_bias`.
- CRIT-2 (khoja unreachable on a built frontier — permanent positives): FIXED §11.2 — concrete neglect-rot.
- MED-3 (fort-count term unsound — Turkestan≠Tarim geometry + 6-writer shared building): DROPPED §11.6 —
  missions stamp Xinjiang-specific secured provinces instead.
- MED-4 (caravan.2 lapse −3 writer missed): FIXED §11.6 — converted to a contested stamp.
- LOW-5 (integrate doesn't clear khoja_pending): FIXED §11.6.
- LOW-6 (dead self-clear branch): FIXED §11.6 — delete or give MIXED a clear step.
- Also LOW-7: consolidation vs panel/mission read tuntian differently (real modifiers vs int) — noted,
  acceptable (both plant-only), reconcile only if province-loss edge matters.

**This is the largest commit in the program. Re-review §11 in full before ANY build. This round-4 rewrite has
NOT been re-reviewed — it needs one more adversarial pass before implementation.**
