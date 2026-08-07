# DESIGN — Link the Xinjiang system to concrete garrisons (#19)

**Branch:** merge-overnight. **Status:** DESIGN (needs adversarial review before build). **Scope:** CHI.
**Coupled with:** #21 (seeds the garrison objects this reads), #20 (khoja-event garrison options gate on this).

## 0. Problem (the "major gap")
`QING_xj_derive_control` (se_QING_XINJIANG.txt:230-268) derives `qing_xinjiang_control` from concrete grip
objects — begs, tuntian colonies, secured/contested oasis modifiers, the xiexiang subsidy modifier — BUT the
only "garrison" term is the ABSTRACT `qing_xj_xiexiang` country-modifier (+10, commented "the paid garrison").
There is NO term for a REAL banner/Green-Standard garrison standing on Xinjiang soil. The integration capstone
ALREADY has the proven concrete pattern (count CHI army unit_size on the subject's soil) — Xinjiang should too.
This is the concrete-over-abstract program (#10B) applied to the frontier garrison.

## 1. The PROVEN pattern to mirror
`SUBJ_QING_resolve_integ_actors` (se_SUBJECT_QING.txt:828-910): `every_army { limit = { is_moving = no
exists = unit_location  unit_location = { owner = scope:target } }  ROOT = { change_variable = { name =
integ_garrison_size  add = prev.unit_size } } }` — sums CHI standing-army cohorts on the target's provinces
into a country var, then bands it. This is the concrete garrison-strength measure.

## 1b. [REVIEW-DECISIVE 2026-08-07] Count `qing_hist_garrison_prov`, NOT a building or army
The adversarial review found BOTH G1 (army count) and G2 (building count) count the WRONG object:
- G2 (buildings) misses the Tarim: `qing_banner_garrison_building` AND `qing_green_standard_post_building`
  both reject uighur XNG on their culture potential; #21 doesn't seed a building anyway (it's a create_unit).
- G1 (army count) as written is BROKEN: `unit_location = { area = area:X }` is NOT a valid trigger — the
  proven form is `is_in_area = Dzungaria` (no `area:` prefix, se_QING_ILI.txt:419). Plus armies move + need
  unit_size division.
- **THE RIGHT OBJECT ALREADY EXISTS:** the OOB garrison raise stamps a PERMANENT, OWNER-INDEPENDENT province
  variable **`qing_hist_garrison_prov`** (imp19c_effects_legion_setup.txt:130/156) on every garrison seat —
  and #21's guard-widen means Kashgar p:2700 now gets it too. So the term is a TUNTIAN-SHAPED count of
  `has_variable = qing_hist_garrison_prov` over `area:Dzungaria` + `area:Tarim` — owner-independent, covers
  Kashgar, no culture gate, no army fiddliness, works TODAY. This REPLACES G1 and G2.
```
set_variable = { name = qing_xj_ctl_term  value = 0 }
area:Dzungaria = { every_area_province = { limit = { has_variable = qing_hist_garrison_prov }  ROOT = { change_variable = { name = qing_xj_ctl_term  add = <N> } } } }
area:Tarim     = { every_area_province = { limit = { has_variable = qing_hist_garrison_prov }  ROOT = { change_variable = { name = qing_xj_ctl_term  add = <N> } } } }
# cap the term, then add to qing_xj_control_tmp BEFORE the :266 clamp.
change_variable = { name = qing_xj_control_tmp  add = var:qing_xj_ctl_term }
```
(NOTE: verify `qing_hist_garrison_prov` is a PROVINCE var readable via has_variable in every_area_province —
it's set on $prov$ at :148; confirm scope. Also #346 se_QING_FRONTIER.txt:51-72 has garrison-detection — check
it doesn't already provide a cleaner count.)

## 2. [SUPERSEDED by §1b] Original G1/G2 sketch — a concrete garrison term in the derive
Add to `QING_xj_derive_control`, using the `qing_xj_ctl_term` scratch pattern (set 0 → accumulate → add to
`qing_xj_control_tmp`), BEFORE the :266 clamp:

```
# concrete garrison: CHI (or subject) standing-army cohorts on Xinjiang soil (Dzungaria + Tarim areas),
# +N per some cohort threshold. Mirrors the capstone's every_army count.
set_variable = { name = qing_xj_ctl_term  value = 0 }
# count standing CHI armies located in the Dzungaria/Tarim areas (the New Dominion's soil)
every_army = {
    limit = {
        is_moving = no
        exists = unit_location
        unit_location = { OR = { area = area:Dzungaria  area = area:Tarim } }
        # owner: CHI itself, OR a Xinjiang subject (ILI/XNG) — the garrison holds the frontier regardless
        OR = { owner = ROOT  owner = { overlord = { is_subject_of = ROOT } }  owner = { is_subject_of = ROOT } }
    }
    ROOT = { change_variable = { name = qing_xj_ctl_term  add = prev.unit_size } }
}
# scale cohorts → control points (tune): e.g. divide to a sane term, cap the contribution.
# (thresholds/cap TBD in build — a few cohorts shouldn't swamp the 0..100 meter.)
change_variable = { name = qing_xj_control_tmp  add = var:qing_xj_ctl_term }
```

### DECISION — building-based vs army-based garrison count (resolve in review)
Two candidate "concrete garrison object":
- **(G1) ARMY units** on the soil (the capstone idiom above). Reflects actual military presence, moves with
  the war, and is what the player SEES in the Outliner ("Ili Banner Garrison 4,500"). But army location/owner
  in a subject's land is fiddly (nested XNG ownership; armies move).
- **(G2) the garrison BUILDINGS** `qing_banner_garrison_building` (+ the Tarim garrison from #21) — count
  `has_building` across the Xinjiang areas, like the tuntian term already does (:244-245 counts
  qing_xj_tuntian_colony province modifiers). Stable, on-map, doesn't move, and is EXACTLY what #21 seeds.
- **LEANING G2** — it's the same shape as the existing tuntian/secured terms (count a province object), pairs
  cleanly with #21 (which seeds the buildings), and avoids the army-location/ownership complexity. G1 could be
  ADDED later as a "field army present" bonus, but the durable grip term should be the buildings.

## 3. Coupling with #21 (CRITICAL — avoid double-count)
#21 seeds `qing_banner_garrison_building` (North) + a Tarim garrison (South) on Xinjiang provinces. If #19
counts those buildings (G2), the two are ONE system: #21 places the objects, #19 derives control from them.
They MUST be built together / in sequence so control isn't double-fed (e.g. don't also keep the abstract
xiexiang +10 AND a building term that represents the same garrison — decide whether xiexiang stays as the
"is the garrison PAID" modifier (a multiplier/gate) vs the buildings as the "does the garrison EXIST" count).
Proposed: buildings = existence (+N each), xiexiang = paid-and-effective (keep its +10 as the funding signal).

## 4. Coupling with #20 (khoja-event garrison options)
#20 wants the khoja-chain events to offer a "local garrison" option gated on a garrison being present. Once
#19 derives from concrete garrisons, #20's gate = `has_building = qing_banner_garrison_building` (or the Tarim
garrison) in the relevant area, OR the derived garrison term > 0 — a concrete, honest gate. #20 depends on #19+#21.

## 5. Files affected
- `common/scripted_effects/se_QING_XINJIANG.txt` — add the garrison term to QING_xj_derive_control (before :266 clamp).
- (No new vars beyond the reused qing_xj_ctl_term scratch; the term reads #21's seeded buildings.)

## 6. Build checklist
1. RESOLVE G1 vs G2 in review (lean G2 — count garrison buildings, pairs with #21).
2. Confirm the Xinjiang area keys (area:Dzungaria / area:Tarim — already used at :244-262) cover the garrison
   provinces (incl. the Tarim oases XNG owns).
3. Add the term via the qing_xj_ctl_term scratch, BEFORE the clamp; pick +N per garrison + a cap so it doesn't
   swamp the meter (the ILI garrison alone shouldn't max control).
4. Decide xiexiang's role (keep as funding signal; buildings as existence) — no double-count.
5. Boot-test: control rises when garrisons are seeded/built; falls if a garrison is lost; log via se_LOG.
6. Build AFTER/WITH #21 (needs the seeded objects to count).

## 6b. [REVIEW-DECISIVE] Two more fixes before build
- **XIEXIANG OVERLAP — reframe, don't stack.** The in-code comment (se_QING_XINJIANG.txt:442-443) says
  "xiexiang paid the GARRISON, not the begs" — so the existing +10 xiexiang term IS the garrison-funding
  proxy. Adding a garrison-EXISTENCE term while keeping xiexiang as an independent additive +10 double-scores
  one garrison (built + paid). FIX: make xiexiang a GATE/MULTIPLIER on the garrison term (a built-but-unpaid
  garrison contributes less), NOT a parallel flat additive. Decide this, don't stack.
- **HOT-FROM-TURN-1 CALIBRATION.** Unlike a buildable object, the Ili + Kashgar garrisons EXIST at 1763 game
  start, so this term is NON-ZERO at open. The shipped derive must keep: 1763 opens ~40 (ILI +30 + 2 begs),
  khoja trigger reachable at ≤30, capstone ≥85 reachable. A non-zero-at-open garrison term raises the opening
  AND the permanent floor — risking making the khoja ≤30 band UNREACHABLE (the exact landmine #11.2/CRITICAL-2
  of the control-concretize design fought). So: small +N/seat, capped ~10-12, AND re-derive the ≤30
  reachability + rebalance other weights if needed. Confirm the khoja scare can still fire on a neglected
  frontier after this term is added.

## 7. Risks
- **R1 double-count with #21/xiexiang** — §6b. Reframe xiexiang as a gate/multiplier, not a parallel additive.
- **R2 area coverage** — if the Tarim oases aren't in area:Tarim (or XNG's provinces are in a different area),
  the count misses them. Verify area membership of the seeded garrison provinces.
- **R3 magnitude/tuning** — +N per garrison must be calibrated so North (many garrisons) doesn't trivialise
  the 0..100 meter. Cap the term (like the begs/tuntian terms are bounded).
- **R4 sequence** — building #19 before #21 means it counts objects that don't exist yet (harmless — term = 0
  — but the feature does nothing until #21 lands). Build #21 first or together.
