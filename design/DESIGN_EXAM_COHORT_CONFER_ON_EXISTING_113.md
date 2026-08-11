# DESIGN #113 — the triennial exam cohort confers degrees on existing degreeless court adults (all 3 tracks), create_character ONLY as fallback

**Status:** DRAFT 2026-08-11. Needs one adversarial review before implementation. Distinct from #111 (Hanlin
POOL caller-split); this is the EXAM COHORT itself.

## The rule this serves (user-authoritative — see [[imp19c-character-creation-rule]])
`create_character` with an exam degree is permitted in EXACTLY two places: (a) the game-start boot seed, and
(b) the exam itself. This task keeps the exam as the sole ongoing factory but makes it **prefer conferring the
degree onto a real existing person**, creating a body only when no eligible candidate exists.

## Diagnosis (traced in source this session — se_QING_EXAM.txt)
Two exam mechanisms exist, and they embody graduates oppositely:
- **Per-person path — `QING_exam_sit_candidate` (:534), fired on_becoming_adult.** Tests an EXISTING court
  character and `add_trait`s the degree onto him. It ALREADY confers on real people, and already routes three
  tracks by profile (all inside the one effect):
  - **BANNER 翻譯科** (:566-589): gate `culture_group = jurchen OR mongolic` → `fanyi_jinshi` / `shengyuan`.
  - **MILITARY 武科** (:598-641): gate `martial > finesse` (see §ROUTING-FIX) → `wu_zhuangyuan/wu_jinshi/
    wu_juren/wu_shengyuan` by pass-rate band.
  - **CIVIL 文科** (:642-694): else → `hanlin/jinshi/gongshi/juren/shengyuan/jiansheng` by pass-rate band.
  This path never needs create_character — the sitter IS the existing character. UNTOUCHED by this task except
  the shared §ROUTING-FIX.
- **Cohort batch — `QING_exam_graduate_cohort` (:298), triennial.** Calls `QING_exam_mint_scholar` (:159) for
  every graduate slot, which UNCONDITIONALLY `create_character`s a fresh body (age 28 / han / confucianism /
  add_trait $degree$). **CIVIL ONLY today**, always spawns. THIS is what #113 reworks.

## Desired behavior (user, locked)
1. For each cohort graduate slot: FIRST try to confer the degree (`add_trait`) onto the **ablest** existing
   degreeless adult CHI-court character of the slot's track profile; `create_character` ONLY as fallback when
   none is eligible.
2. **Extend the cohort to all THREE tracks** (user: "extend the cohort to all 3 tracks"). Today only civil
   graduates come out of the batch; banner + martial graduates only trickle from the coming-of-age path. Give
   the cohort banner + martial slots too, so the amban bench (banner) and the Green Standard officer pool
   (martial) get a renewable triennial batch supply — the starvation #40 patched with a one-off banner mint;
   this absorbs that need.
3. The create_character **fallback applies to banner + martial too** (user: "add the create_character fallback
   to the banner and martial exam track"): when no eligible existing candidate of the track profile exists,
   create one with that track's profile.

## Design

### §ROUTING-FIX (shared, user directive)
Drop `martial > charisma` from the military-track routing gate; keep ONLY `martial > finesse`
(se_QING_EXAM.txt:600-601). Charisma is not a keju axis, so a martial+charismatic man still belongs on the
military ladder. Apply to BOTH the per-person path (:600) AND the new cohort track-selection so routing stays
consistent. This is the ONLY edit to the per-person `QING_exam_sit_candidate`.

### The cohort rework — a per-track "confer-else-create" helper
Replace each `QING_exam_mint_scholar = { degree = X }` call in `QING_exam_graduate_cohort` with a new
`QING_exam_seat_graduate = { track = <civil|banner|martial>  degree = X }` that does:

```
QING_exam_seat_graduate = {
    # Try to CONFER on the ablest eligible existing degreeless court adult of this track's profile.
    if = {
        limit = { any_character = { <track candidate gate> } }
        ordered_character = {
            limit = { <track candidate gate> }
            order_by = <track ability metric>     # civil: finesse; martial: martial; banner: charisma (amban stock)
            check_range_bounds = no
            max = 1
            save_scope_as = seated_graduate
        }
        scope:seated_graduate = {
            add_trait = $degree$
            set_variable = { name = qing_sat_keju  value = 1 }   # excludes him from the per-person path + next cohort slot
        }
    }
    # FALLBACK: no eligible existing candidate → create one with this track's profile (the sanctioned factory).
    else = {
        <track create_character>       # civil = existing QING_exam_mint_scholar body; banner/martial = new profiles below
    }
}
```

**Track candidate gate** = the per-person gate (QING_exam_sit_candidate:536-557) MINUS `NOT=has_variable
qing_sat_keju`? — NO: KEEP `qing_sat_keju` in the gate so a man who already sat (per-person) is not re-graded,
AND stamp `qing_sat_keju` on each conferred pick so the cohort's own multiple slots don't double-confer the
same man. Common gate: `exists=employer  employer={tag=CHI}  is_ruler=no  prisoner=no  is_adult=yes  NOT={has_
variable=qing_sat_keju}` + degreeless (NONE of jiansheng/shengyuan/juren/gongshi/jinshi/hanlin/fanyi_jinshi/
wu_shengyuan/wu_juren/wu_jinshi/wu_zhuangyuan). PLUS the per-track profile:
- **civil:** (no culture/martial constraint — the residual track). order_by = finesse.
- **banner:** `OR={ culture.culture_group=culture_group:jurchen  culture.culture_group=culture_group:mongolic }`.
  order_by = charisma (amban-broker profile, matches qing_amban_rank_svalue).
- **martial:** `martial > finesse`. order_by = martial.

NOTE the profiles are MUTUALLY the same routing as the per-person path, so a court adult is a candidate for
exactly one track — no cross-track poaching if the cohort is careful to run them in a fixed order and each
conferral stamps qing_sat_keju.

### Track fallbacks (create_character — the last resort)
- **civil:** the EXISTING `QING_exam_mint_scholar = { degree = $degree$ }` (age 28 / han / confucianism), UNCHANGED
  — already #90-safe, deferred-bind split intact. It also add_to_variable_list's the scholar pool + bind; for a
  cohort graduate that is fine (matches today's behavior).
  - OPEN Q for review: today EVERY civil graduate mint goes into qing_scholar_pool via mint_scholar. When we
    CONFER on an existing man instead, should he ALSO be added to the pool? Probably NOT automatically — pool
    membership is #111's draw-from-office-less-jinshi concern; a fresh jinshi graduate becomes pool-eligible
    naturally via #111's tick draw. Recommend: the conferred path adds the degree ONLY (no pool insert); the
    fallback-create path keeps today's pool insert (so behavior for created bodies is unchanged). Review to confirm.
- **banner:** new fallback mirroring `QING_exam_mint_banner_laureate` (:218): create manchu / vajrayana /
  charisma-lead body + add_trait fanyi_jinshi. (For lower banner outcome, shengyuan on a created body is odd —
  keep the fallback at the fanyi_jinshi tier the cohort slot represents.) #90-safe: no modifiers in
  create_character, runs from the deferred triennial path.
- **martial:** new fallback: create a martial-lead body (culture han — the wuju was the HAN path to the Green
  Standard, per :597) + add_trait $wu_degree$. Mirror QING_exam_mint_scholar's shape (age 28, add_martial lead,
  finesse/charisma spread) with the wu_* trait instead. #90-safe, deferred path.

### Cohort structure (all 3 tracks)
`QING_exam_graduate_cohort` currently: 1 civil lead (jinshi/juren by pass-rate) + hall-count civil extras +
1 banner-laureate mint (:326). Reshape to seat graduates across the three tracks:
- CIVIL lead + extras: KEEP the existing count/tier logic (jinshi if pass_rate>=30 else juren; +1 juren at >=16
  halls, +2 at >=28), routed through QING_exam_seat_graduate track=civil.
- BANNER: the existing 1 banner-laureate per cycle (:326, gated >=16 halls) → route through
  QING_exam_seat_graduate track=banner degree=fanyi_jinshi (confer on an eligible bannerman first, else create —
  this is a strict improvement over the current always-create QING_exam_mint_banner_laureate).
- MARTIAL: NEW — add martial graduate slot(s) scaled by hall count, tier by pass-rate band (wu_jinshi/wu_juren/
  wu_shengyuan mirroring the per-person martial ladder), routed through QING_exam_seat_graduate track=martial.
  MAGNITUDE (best-guess, log-and-tune per overnight Rule 1a): 1 martial graduate per cycle at >=16 halls, tier
  wu_jinshi if pass_rate>=30 else wu_juren. Logged so the boot confirms/tunes.

## #90 / crash safety
- Conferral is `add_trait` on an EXISTING adult (no create-then-grant) → #90-safe.
- All three fallback create_characters run only from the triennial cohort (a deferred/runtime path, never
  construction) with NO modifiers inside create_character — the proven idiom (QING_exam_mint_scholar,
  QING_exam_mint_banner_laureate). Deferred-bind split preserved for the civil pool insert.
- add_trait on the trait/opposite machinery must be RUNTIME only (QING_grant_martial_degree:735 note:
  access-violates at construction) — the cohort is triennial runtime, safe.

## Files
- common/scripted_effects/se_QING_EXAM.txt — §ROUTING-FIX at :600-601; new QING_exam_seat_graduate helper +
  banner/martial fallback creators; reshape QING_exam_graduate_cohort (:298) to seat across 3 tracks. Keep
  QING_exam_mint_scholar (civil fallback) + QING_exam_mint_banner_laureate (or fold into the banner fallback).
- No change to QING_exam_sit_candidate except §ROUTING-FIX. No change to #111's pool machinery.

## Review must test
1. §ROUTING-FIX applied to BOTH the per-person path and the cohort track-selection; no other per-person change.
2. Each cohort slot confers on the ablest eligible existing degreeless court adult of the RIGHT track profile;
   the profiles partition court adults into exactly one track (no cross-track double-eligibility given the
   culture/martial routing) — confirm a bannerman can't be pulled onto the civil slot and vice versa.
3. qing_sat_keju stamping prevents double-conferral across the cohort's multiple slots AND against the
   per-person path. Confirm a man who already sat (per-person) is excluded from the cohort.
4. Fallback create_character fires ONLY when no eligible candidate exists (the `else` of an `any_character`
   existence check) — not in addition. No double-graduation per slot.
5. Banner fallback = manchu/vajrayana/fanyi_jinshi; martial fallback = han/martial-lead/wu_*; civil = unchanged
   mint. All #90-safe (deferred path, no modifiers in create_character).
6. Degree-TIER logic preserved (civil jinshi>=30 else juren + hall extras; martial wu_jinshi>=30 else wu_juren;
   banner fanyi_jinshi). Magnitudes logged for boot tuning.
7. Pool interaction: conferred civil graduates should NOT be auto-inserted into qing_scholar_pool (that's #111's
   draw); confirm the fallback-create civil path's pool insert is preserved and the conferred path omits it — or
   justify a different choice. No regression to #111.
8. QING_exam_mint_banner_laureate: if the banner cohort slot now routes through the confer-else-create helper,
   is the standalone mint still called anywhere (QING_amban_seed_spare_laureates boot backfill)? Don't break #40.
