# DESIGN — Fix the dropped Altishahr/Tarim garrison for 1763 (#21) — v2 (post-review rewrite)

**Branch:** merge-overnight. **Status:** DESIGN v2 (v1 was BROKEN — solved the wrong problem). **Scope:** setup.
**Research:** research/RESEARCH_QING_XINJIANG_GARRISONS_1763.md.

## 0. What v1 got WRONG (why this is a rewrite)
v1 assumed the Outliner garrison is a `qing_banner_garrison_building` seed. **FALSE.** The adversarial review
proved:
- The garrison the player sees is a **`create_unit`** raised by `SE_qing_raise_garrison_cmd`
  (common/scripted_effects/imp19c_effects_legion_setup.txt:139). `qing_banner_garrison_building` is a
  PURE-MODIFIER building (local_defensive/loyalty) that spawns NO unit — seeding it puts nothing in the Outliner.
- **A Kashgar garrison army ALREADY EXISTS in the 1763 OOB** — `imp19c_effects_legion_setup.txt:267`
  (`prov = p:2700  QING_UNIT_KASHGAR_BANNER_GARRISON  size = 3  cmd = char:584` Hailancha 海蘭察), plus a
  fallback at :324. It is **silently DROPPED**, which is the actual bug.

## 1. ROOT CAUSE (verified)
Both garrison helpers guard ownership NON-recursively:
- `SE_qing_raise_garrison` (:83): `limit = { exists = $prov$  $prov$ = { OR = { owner = c:CHI  owner = { is_subject_of = c:CHI } } } }`
- `SE_qing_raise_garrison_cmd` (:144): same OR + `exists = $cmd$`.

**Kashgar p:2700 is owned by XNG** (in XNG's own_control_core), and **XNG is `client_state of ILI`**, ILI is
CHI's subject → nested CHI→ILI→XNG. `is_subject_of = c:CHI` is NON-RECURSIVE, so XNG is NOT a direct CHI
subject → the OR is false → `else` → `LOG_fail` → **Kashgar garrison not raised.** Ürümqi p:2930 is ILI-owned
(a DIRECT CHI subject) → passes → shows up. This exactly matches the boot symptom: Ili + Ürümqi + interior
garrisons visible, Kashgar/Tarim missing.

## 2. THE FIX (one branch, both helpers)
Widen the ownership guard on BOTH `SE_qing_raise_garrison` (:83) and `SE_qing_raise_garrison_cmd` (:144) to
admit a NESTED CHI subject, using the proven `exists = overlord` wrapper (the idiom already in the sibling
seed at imp19c_setup_events.txt:417 Khovd, and in qing_military_colony_building's potential):
```
$prov$ = { OR = {
    owner = c:CHI
    owner = { is_subject_of = c:CHI }
    owner = { AND = { exists = overlord  overlord = { is_subject_of = c:CHI } } }   # [#21] nested subject (CHI->ILI->XNG): Kashgar/Tarim
} }
```
This RESURRECTS the already-authored Kashgar garrison (both the _cmd version :267 with Hailancha and the
fallback :324) — no new garrison calls needed for Kashgar. It ALSO fixes any other nested-subject garrison
seat that was silently dropped (audit the call list for other XNG-owned provinces).

## 3. Do we need MORE Tarim garrisons than Kashgar?
The OOB currently authors garrisons at Kashgar (2700) + Ürümqi (2930) for the west. The research says the Tarim
had garrisons at Yarkand, Aksu, Ush, Khotan too (smaller). DECISION for review:
- **Minimum (fixes the bug):** just widen the guard → Kashgar garrison appears. This alone resolves the user's
  report ("none in Altishahr").
- **Fuller (historical):** ALSO add `SE_qing_raise_garrison` calls for Yarkand/Aksu/Ush/Khotan (small sizes,
  no commander → the plain helper), guarded by the now-widened helper. Sizes per research: Kashgar 3 (exists),
  Yarkand ~1-2, Aksu/Ush/Khotan ~1 each. N-heavy/S-light preserved (Ili 8, Ürümqi 4, Kashgar 3, others 1-2).
- **RECOMMEND:** ship the guard widen (bug fix) + add Yarkand + Aksu (the two next-largest Tarim seats) for
  historical texture; leave Ush/Khotan optional. Pin their province IDs first (00_Turkestan.txt).

## 4. Anachronism gate (research caveat)
Kashgar/Yarkand/Aksu/Ush/Khotan garrisons ARE 1763-extant (post-1759 conquest). Do NOT add Tarbagatai (1764),
and note the Ili garrison's Huiyuan seat finished 1766 / Sibe arrived 1764 — but those are the EXISTING Ili
seed's concern, not new. Any NEW Tarim call must use a real 1763 commander or the commanderless plain helper
(the research's commanders — Hailancha at Kashgar — are already wired).

## 5. Buildings? (v1's dead end — keep as SEPARATE, low-value)
`qing_banner_garrison_building` / `qing_green_standard_post_building` are pure-modifier infrastructure. If ever
wanted on Tarim soil as flavor, BOTH reject uighur XNG on their culture potential (banner=jurchen;
green-standard=jurchen|chinese_group) and would need the overlord-culture widening (the tuntian building's
potential shows the precedent). But this is ORTHOGONAL to the Outliner-garrison bug and has near-zero mechanical
payoff (the control derive counts MODIFIERS, not buildings — see #19). DEFER; not part of #21.

## 6. Coupling with #19
#19 (concrete garrison → control) counts province MODIFIERS (qing_xj_tuntian_colony, qing_xinjiang_prov_secured),
NOT armies or buildings — confirmed by the review. So resurrecting the Kashgar ARMY (this task) does NOT feed
#19's control derive. If we WANT the garrison to raise control, #19 must add a term that reads the army
(SE garrison unit_location) OR a garrison MODIFIER stamped alongside. Re-examine #19's G1-vs-G2 in light of this:
the "garrison" the player sees is an ARMY, so #19's G1 (army count) is the honest link, not G2 (buildings that
don't exist). → UPDATE #19 accordingly.

## 7. Files affected
- `common/scripted_effects/imp19c_effects_legion_setup.txt` — widen the guard on SE_qing_raise_garrison (:83)
  and SE_qing_raise_garrison_cmd (:144); (optional) add Yarkand/Aksu garrison calls (~:324 block).
- NO changes to imp19c_setup_events.txt or the buildings file (v1's targets — both wrong).

## 8. Build checklist
1. Widen the ownership guard (both helpers) with the nested-overlord branch (`exists = overlord` wrapped).
2. Boot-test: Kashgar Banner Garrison (海蘭察, size 3) now appears in the Outliner on p:2700.
3. (Optional) add Yarkand/Aksu (+Ush/Khotan) plain-helper calls; pin IDs from 00_Turkestan.txt; boot-verify.
4. Audit the full garrison call list for OTHER nested-subject provinces silently dropped by the old guard.
5. grep error/debug.log: confirm the "province not held by Qing; garrison not raised" LOG_fail for Kashgar is
   GONE and the create_unit succeeded.
6. Update #19's design (G1 army-count, not G2 buildings) per §6.

## 9. Risks
- **R1 guard widen too broad:** admitting `overlord = { is_subject_of = c:CHI }` could raise garrisons on OTHER
  nested subjects' land unintentionally. But garrisons are only raised where a `SE_qing_raise_garrison[_cmd]`
  CALL exists (a fixed authored list) — the guard only gates whether an AUTHORED call fires, it doesn't spawn
  anywhere new. So the widen only un-drops already-intended garrisons. Low risk; audit the call list (step 4).
- **R2 commander eligibility:** the _cmd Kashgar garrison attaches char:584 (Hailancha) — the _cmd helper's
  extra `exists = $cmd$` + the CHI-employed-commander logic (:162) must still pass for a nested-subject
  province. Verify Hailancha attaches (or the commanderless fallback :324 fires) after the widen.
- **R3 double depth:** the guard handles ONE overlord level (CHI→ILI→XNG: XNG.overlord=ILI, ILI is_subject_of
  CHI ✓). If any garrison seat is TWO levels nested, it'd need another overlord level — but Kashgar is exactly
  one level. Confirm no deeper nesting among garrison seats.
