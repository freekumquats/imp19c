# DESIGN — Derive `qing_modernarmy_share` from the real modern-legion count (新軍)

**Branch:** merge-overnight. **Status:** ✅ SHIPPED 2026-08-06 (commit f0139a38f; rewritten to pure count×K after design review). **Scope:** CHI only.
**Sibling to:** the banner/GS decay (#9) and han-provincial (#6) docs — same [[imp19c-concrete-over-abstract-rule]],
same `every_unit` + `any_sub_unit = { sub_unit_type = … }` counting idiom, same count×K target-blend shape.
**User ruling 2026-08-06:** "Concretize it (recalibrated)" — derive from a real modern-legion count, accept the
behavioral change that losing modern armies drops the share (feeding warlordism via #6).

## 0. The problem (why this is a target)

`qing_modernarmy_share` (0–100, 新軍/levee) drifts toward an ABSTRACT ceiling (`qing_selfstr_progress`,
`se_QING_DECLINE.txt:484-511`), and the three founding events give a PERMANENT one-time boost
(+30 Ever-Victorious / +35 Beiyang / +25 Nanyang) via `QING_DECLINE_nudge`. Two faults:

- **The meter lies when the army dies.** The founding boost is permanent: if the Beiyang Army is annihilated
  (the Yalu 1894 collapse), the share still reads "modernized" forever — there is no concrete referent that
  falls. This is exactly the anti-pattern the #91 program targets.
- **Yet the concrete referent ALREADY EXISTS on the map.** The founding events raise REAL legions
  (`QING_selfstr_raise_modern_army`, `se_QING_SELFSTR.txt`) built from the `qing_ever_victorious` sub-unit
  (`common/units/army_qing_ever_victorious.txt`), and the unit is player-buildable (gated on the modernization
  doctrine law). So the share should be DERIVED from how many modern legions actually stand, not a stored drift.

`#9` (banner/GS decay) and `#6` (han-provincial) already do exactly this — count real sub-units by
`sub_unit_type` via `every_unit { any_sub_unit = { … } }`. This doc applies the identical idiom to the modern army.

## 1. Thesis — derive the share from a modern-legion count, PURE COUNT×K, NO FLOORS
> **REWRITTEN after adversarial design review (2026-08-06). The original §1 had a `doctrine_floor` term; the
> review CONFIRMED it (a) is almost always 0 (no `add_law`/`activate_law` exists anywhere in the repo → the
> doctrine law is only ever player-enacted, M1), and (b) where it IS held, a permanent floor reintroduces the
> exact "meter lies when the army dies" anti-pattern §0 exists to kill (C2/C3). So the floor is DROPPED. Pure
> count-derive is simpler, honours the user-approved "army dies → share falls" everywhere, and needs no law.**

Replace the abstract-ceiling drift with a target DERIVED purely from the concrete modern force:

```
target = clamp( modern_legion_count × K , 0, 100 )    # then ×0.5 if hollow; ± drill_posture_bias (see below)
share  drifts ±2 toward target   (KEEP the existing smooth drift — no instant snap)
```

- **`modern_legion_count`** = number of the country's legions carrying a modern sub-unit:
  `every_unit = { limit = { any_sub_unit = { sub_unit_type = qing_ever_victorious } } ROOT = { change_variable
  = { name = … add 1 } } }`. ⚠️ **NO commander guard, NO owner guard (review C1, CONFIRMED design-breaking).**
  `#9` counts with `has_commander = yes commander = { employer = ROOT }` ONLY because it reads commander
  stats — but `QING_selfstr_raise_modern_army` / the Beiyang / Nanyang / spawn_newarmy raises attach **no
  commander**, so copying #9's guard would filter out most founded legions → count reads 0 → share never
  leaves 0. `every_unit` in country scope iterates ONLY ROOT's own legions (proven, `se_QING_COUNCIL.txt:560`),
  so foreign/rebel EVA is already excluded and no owner guard is needed. Use the BARE `any_sub_unit` filter.
  Count LEGIONS (one per raised army), not sub-units — the unit of "a modern army fielded".
- **`K` — CALIBRATION.** Bands are 30 (emerging) / 60 (national). **K = 30** — chosen to REPRODUCE the current
  band-crossing arc via the count (not undershoot it, review M4):
  - 1 legion → 30 (**emerging** — matches today: `found_evarmy` alone lifts to the emerging band).
  - 2 legions → 60 (**national** — matches today: EVA + Beiyang reaches national).
  - 3 → 90; 4 → capped 100. (K=25 was rejected: 1→25 is BELOW emerging, a regression from current behavior
    where the first founding lands emerging.)
  - **spawn_newarmy interaction (review M3):** `QING_army_spawn_newarmy` (`se_QING_MECHANICS.txt:491`) raises a
    4th EVA legion ONCE when share ≥ 60 (guarded `qing_newarmy_legion_raised`). So a fully-founded realm
    settles at 4 legions → 100, not 3→90. Self-limiting (once-guarded), a real countable legion that falls if
    wiped — consistent with the thesis. Documented, no change needed.
  - **This is count×K, NOT a fraction** (`modern ÷ total_army`). No clean total-legion denominator exists, and
    a fraction would undershoot the bands among a large Green-Standard host. Same choice #6/#9 made. **K=30
    PLACEHOLDER-playtest.**
- **NO doctrine_floor.** The share is count-only. A realm whose modern armies are all wiped reads 0 (or the
  drift easing toward 0) — which is the POINT: losing your modern army drops the share and re-arms the warlord
  vector via #6 (§7). The institutional-doctrine-survives-the-battle nuance is NOT modelled (it was ~always 0
  anyway); if wanted later it belongs on a separate law-modifier, not this meter.
- **Hollow flag + drill-posture bias RELOCATE onto the count-target** (review L4 — they used to modify the
  ceiling; with no ceiling they'd be near-inert on a 0 floor). Applied to the count-derived target instead:
  `if hollow_flag: target ÷ 2` (a paper army of N legions reads as half — captures "looks modern, isn't");
  `if has qing_drill_posture_bias: target += bias` (intensive 新式操練 lifts, lax lowers). Both act on the
  count term (0..100+ span) so they stay meaningful. Guarded → default byte-identical.

The band application (`QING_DECLINE_apply_modernarmy_band`, 30/60) and EVERY reader are UNCHANGED — they read
`qing_modernarmy_share`. Only what SETS the target changes.

## 2. What now drives the share (the inversion) — writer census

Verified via `rg qing_modernarmy_share` (all sites):

| File:line | Now | Becomes |
|---|---|---|
| `se_QING_DECLINE.txt:484-511` `QING_DECLINE_drift_modernarmy_share` | target = selfstr_progress ceiling, ±2 drift | **target = legion_count×K + doctrine_floor**, KEEP the ±2 drift. This is the one derive rewrite. |
| `se_QING_SELFSTR.txt:388` (evarmy, +30) | permanent nudge | **DROP the nudge** — the event already raises the real EVA legion (`QING_selfstr_raise_modern_army`), which the derive now counts. The share climbs via the count next pulse. |
| `se_QING_SELFSTR.txt:471` (beiyang, +35) | permanent nudge | **DROP** — same (raises the real Beiyang legion). |
| `se_QING_SELFSTR.txt:506` (nanyang, +25) | permanent nudge | **DROP** — same (raises the real Nanyang legion). |
| `se_QING_MECHANICS.txt:404` (+12) | nudge | **DROP** — this lever should RAISE A LEGION if it is to move the share (see §4), or drop the share-nudge and keep its other effects. Decide per §4. |
| `events/qing_reform_events.txt:502,537` (+8, +5) | nudge | **DROP** — same class as the mechanics lever (§4). |
| `se_QING_NAPOLEON.txt:326` (+60, the levée) | permanent nudge | **DROP — see §5 (rewritten).** The levée DOES raise a real `qing_ever_victorious` legion (La Grande Armée), so it is already counted (1 legion → emerging on its own; national if combined with foundings). No floor. ⚠️ BEHAVIOR CHANGE: a pure-Napoleon path with no self-strengthening foundings now reaches only the EMERGING band, not national — accepted (the levée is one legion; national requires ≥2 modern legions). |
| `se_QING_SELFSTR.txt:789` capstone `set share = 100` | force-set the stored meter | **CHANGE — see §6.** A set on a now-derived meter is overwritten next pulse. |

⚠️ **HARD INVARIANT (mirrors the #1/#3 var-resurrection rule):** every dropped `QING_DECLINE_nudge` on
`qing_modernarmy_share` MUST be dropped, not left — but note `qing_modernarmy_share` is NOT being deleted (it
stays as the stored, drifted, band-read meter), so a stray nudge does not "resurrect a dead var" — it just
double-counts (the boost AND the legion the event raised). Still drop them so the count is the single channel.

## 3. The founding events already raise the real force — that's the whole point
`QING_selfstr_found_evarmy` / `_beiyang_army` / `_nanyang_army` each already call
`QING_selfstr_raise_modern_army` (`raise_legion` of 3× `qing_ever_victorious` + 2 artillery). So the concrete
referent is CREATED by the same events that today also nudge the meter — we just delete the redundant nudge and
let the derive read the legion the event raised. No new spawning needed; the map objects exist.

## 4. The non-founding share LEVERS (mechanics +12, reform-event +8/+5) — DECISION
These three are "invest in modernization" beats that today nudge the share without raising a legion. Options:
- **(a) DROP the share-nudge, keep their other effects** (treasury cost, banner-decay relief, selfstr advance).
  The share then only moves when a real legion is raised/lost. Cleanest concrete-over-abstract; RECOMMENDED.
- **(b) Convert them to raise a small modern legion** (a fourth+ raise site). More concrete but risks the count
  running away past the founded three, and these are recurring/roll beats (not one-shot foundings) → the player
  could spam legions. Reject.
- **DECISION: (a).** These levers keep their fiscal/selfstr/decay effects; they lose the direct share-nudge. A
  realm modernizes its ARMY SHARE by raising modern armies (the foundings + building EVA units), not by an
  abstract "invest" tick. Document the semantic shift.

## 5. The Napoleon levée (#65) — NO SPECIAL CASE NEEDED (review C2, CONFIRMED)
> **REWRITTEN — the original §5 was factually WRONG.** `QING_napoleon_reform_levee` (`se_QING_NAPOLEON.txt:379`)
> DOES raise a concrete `qing_ever_victorious` legion — "La Grande Armee de Chine 中華大軍", one legion of 15
> EVA battalions + 5 artillery. So the derive ALREADY COUNTS it (1 legion → +30 = emerging on its own; combined
> with any foundings it reaches national). There is NO missing referent.
- **DECISION: DROP the `+60` nudge (`se_QING_NAPOLEON.txt:326`), add NOTHING.** The levée's real legion is
  counted like any other. If the alt-history intent is that a mass conscript army should weigh MORE than a
  single professional corps, give its create_unit a distinguishing marker and count it ×2 — but the simplest
  correct behavior is: it's one modern legion, worth 30, and if the Grande Armée is annihilated the share
  falls, exactly as the user approved for every other modern army. No permanent floor (that was the C2 lie).

## 6. The Self-Strengthening CAPSTONE (`set share = 100`) — CHANGE (review C3, CONFIRMED)
> **REWRITTEN — the original §6 option (a) was factually WRONG.** `QING_selfstr_capstone_modernized`
> (`se_QING_SELFSTR.txt:760`) raises ZERO legions — it only `set_variable qing_modernarmy_share = 100` +
> force-adds `qing_modernarmy_national`. So "it already founds all three armies" is false; the capstone assumes
> the *missions* founded them earlier but does not guarantee it in-effect.
`se_QING_SELFSTR.txt:789` sets the stored meter to 100. On a derived meter that set is overwritten next pulse
(the #3 lesson). Fix — make the capstone RAISE A REAL LEGION so the count reflects it:
- **DECISION: replace `set share = 100` with a `QING_selfstr_raise_modern_army` call** (raise a capstone New
  Army legion at the capital, guarded not-already-raised), so the derive counts it and the share climbs
  concretely. Combined with the foundings + spawn_newarmy the count is already ≥3-4 legions at capstone →
  national by the derive. The force-added `qing_modernarmy_national` modifier STAYS as the immediate visual
  reward (the band is stamped instantly; the derive confirms it next pulse). NO permanent floor — a
  post-capstone realm that loses all its modern legions SHOULD see the share fall (consistent with §0/§7; the
  capstone is a one-time achievement, not permanent immunity to military catastrophe). If truly-permanent
  "modernized forever" is wanted, that is a separate explicit decision — flagged, not assumed.

## 7. Interaction / what stays
- **#6 han-provincial** subtracts `var:qing_modernarmy_share` (`se_QING_DECLINE.txt:559`) — UNCHANGED. Now it
  subtracts a share that FALLS when modern armies are lost → losing your modern army correctly RE-ARMS the
  warlord vector (the intended behavioral win, user-approved). This is the key coupling that makes the
  concretization matter.
- **Bands** (30/60 → emerging/national modifiers) + all readers (Napoleon `<60`, mechanics `>=60`, selfstr
  `<30/<40`) UNCHANGED — they read the level, and K=25 keeps the founded force reaching the bands.
- **Ordering:** the derive already runs in `QING_DECLINE_pulse` (`:1096`) BEFORE
  `QING_DECLINE_drift_han_provincial_power` (`:1097+` reads the fresh share) — KEEP that order (the count-derived
  share must be fresh before #6 subtracts it). Verify.

## 8. 1763 opening
No modern legions exist at 1763 (no founding fired), no modern doctrine law adopted → legion_count=0,
doctrine_floor=0 → target 0 → share opens 0. Matches the current seed (`:485` seeds 0). Correct: the High-Qing
fields only Banners/Green Standard.

## 9. Feasibility / gotchas
- **Perf:** `every_unit` over the country's legions is O(legions) — the same walk #9 already does every pulse
  for banner/GS decay. Cheap; no province/pop sweep. (If #9's walk and this can share ONE `every_unit` pass,
  fold them — but they're in different effects/files, so a second small walk is acceptable; note it.)
- **Sub-unit type name:** confirm `qing_ever_victorious` is the exact `sub_unit_type` key (the unit def is
  `common/units/army_qing_ever_victorious.txt`; the raise uses `sub_unit = qing_ever_victorious`). Verify the
  band/count reads the SUB-UNIT type, not the unit-file name, if they differ.
- **Legion vs sub-unit count:** `every_unit` iterates LEGIONS (armies); `any_sub_unit` tests membership. So
  `every_unit { limit = { any_sub_unit = { sub_unit_type = qing_ever_victorious } } }` counts LEGIONS that
  contain ≥1 modern sub-unit = "modern armies fielded". Correct granularity.
- **Mercenary/rebel EVA:** guard the count on `owner = ROOT` / employed legions so a rebel or foreign EVA
  legion isn't counted as the throne's modern army. Use the `has_commander`/`commander={employer=ROOT}` guard
  #9 uses, OR the legion-owner guard — verify which is right for `every_unit` (a raised legion is owned by CHI).
- **RHS-comparison rule:** the drift-toward compare already uses `qing_modernarmy_target_tmp_cmpsvalue` — keep it.
- **Hollow flag:** keep the halving but apply it to the doctrine_floor (not the legion count — a real legion is
  real whether or not the movement is hollow; the floor is the institutional claim that hollowness undercuts).

## 10. Build checklist (POST-REVIEW)
1. Rewrite `QING_DECLINE_drift_modernarmy_share`: target = `modern_legion_count × 30`, then `÷2 if hollow`,
   `+ drill_posture_bias` (both guarded), clamp 0..100, KEEP the ±2 drift. **NO doctrine_floor.**
2. Count via `every_unit = { limit = { any_sub_unit = { sub_unit_type = qing_ever_victorious } } ROOT = {
   change_variable = { name = qing_modernarmy_legion_ct  add = 1 } } }` — **BARE filter, NO commander/owner
   guard** (review C1). Seed `qing_modernarmy_legion_ct = 0` before the walk.
3. DROP the 3 founding-event share-nudges (`se_QING_SELFSTR.txt:388/471/506`) — the events keep raising the
   real legions, which the derive now counts.
4. DROP the mechanics `+12` (`se_QING_MECHANICS.txt:404`) and reform-event `+8/+5` (`qing_reform_events.txt:502/537`)
   share-nudges (§4a) — keep their other effects (treasury, decay relief, selfstr advance).
5. Napoleon (§5): DROP the `+60` nudge (`se_QING_NAPOLEON.txt:326`) — its Grande Armée legion is already counted.
6. Capstone (§6): replace `set share = 100` (`se_QING_SELFSTR.txt:789`) with a guarded
   `QING_selfstr_raise_modern_army` call (raise a capstone legion) so the count reflects it; keep the
   force-added `qing_modernarmy_national` modifier as the instant reward.
7. se_LOG: add a LOG_line to the derive reporting `legion_ct → target` (error-logging rule).
8. Verify ordering (derive `:1096` before #6 han-provincial `:1097+`), bands/readers unchanged, K=30 reaches
   the bands (1 legion→30 emerging, 2→60 national), 1763 opens 0 (no legions, no law).
9. Brace/quote/BOM; boot-crash independent review. K=30 flagged PLACEHOLDER-playtest.
10. Adversarial build review before commit.
