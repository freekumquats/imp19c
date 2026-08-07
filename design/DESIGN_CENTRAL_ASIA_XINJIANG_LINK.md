# DESIGN — Link Central Asia, Caravan, and Xinjiang subsystems (經略西域一體化)

**Branch:** merge-overnight. **Status:** DESIGN (needs adversarial review before build). **Scope:** CHI.  
**Subsystems:** #370 caravan, #422 Xinjiang consolidation, #448 Central Asia expansion.

## 0. Problem

Three Qing subsystems currently run parallel but disconnected:
1. **Caravan trade runtime** (#370, se_QING_CARAVAN.txt) — Kokand ultimatum → player grants aqsaqal OR refuses/temporises; route-cut crisis → military escort OR grant/invoke concession OR lapse. Flags: `qing_caravan_aqsaqal_granted`, `qing_xj_khoja_pending`, `qing_caravan_prosperity`.
2. **Xinjiang consolidation tree** (#422, qing_xinjiang_missions.txt) — tasks gate on begs, tuntian, governor capability, `qing_xj_consolidation ≥ 75/85`). Runtime: `QING_xj_derive_control` (se_QING_XINJIANG.txt :230-270) computes `qing_xinjiang_control` from ILI subject + begs + tuntian + xiexiang + secured/contested oases. Khoja-scare (~:500) backs pretenders when control ≤ 30 + empty/venal beg corps.
3. **Central Asia conquest tree** (#448, qing_central_asia_missions.txt) — subjugate Kazakh hordes GKH/ORT/KSH + khanates KOK/BUK/KHV via `FUNC_make_subject` (se_QING_CENTRAL_ASIA.txt), hold Fergana provinces. Currently NO feedback into Xinjiang.

**Gaps:**
- Player has no conquer-Kokand alternative to the aqsaqal humiliation (caravan.1 grants OR refuses-then-arms-khoja OR temporises; conquer unrecognised).
- Subjugating/annexing KOK does not suppress the khoja-scare that KOK backs (scare logic :503-518 gates only on control + beg corps, never checks KOK subject status).
- Central-Asia dominion (conquering/subjugating the khanates) provides no Xinjiang-consolidation benefit (no term in `QING_xj_derive_control`).
- Mission-tree tie-in absent: #448 KOK subjugation task (qing_ca_khanates :127-156) and caravan ultimatum both involve KOK but don't interlock.

## 1. Design — two pillars

### A. Conquer-Kokand alternative (caravan)

**New event chain:** when player refuses/revokes aqsaqal OR conquers/subjugates KOK, trigger a NEW event `qing_caravan.3` "The Khanate Yields" (浩罕屈服) offering:
- **Dictate terms** (天朝定制) — reopen caravan trade on CHI-dictated terms: NO aqsaqal, NO customs haircut, +12 prosperity, +8 control (secure one oasis), clear khoja-scare. Costs: treasury -100 (enforcement garrison), popularity +20.
- **Absorb the route** (併商道) — fold Kokand merchants into CHI state monopoly: set customs_rate=2 (heavy), +15 prosperity (monopoly volume), clear khoja-scare, +legitimacy. Costs: political_influence -40.

**Trigger:** `qing_caravan.3` fires from `QING_caravan_pulse` when:
```
OR = {
    AND = {  # refused/revoked the aqsaqal AND Kokand hostile
        NOT = { has_variable = qing_caravan_aqsaqal_granted }
        exists = c:KOK
        c:KOK = { opinion = { target = ROOT  value < -20 } }
        NOT = { c:KOK = { is_subject_of = ROOT } }
    }
    AND = {  # conquered/subjugated Kokand
        exists = c:KOK
        OR = {
            c:KOK = { is_subject_of = ROOT }
            any_owned_province = { count >= 3  is_in_region = Fergana  is_capital_of = c:KOK }
        }
    }
}
NOT = { has_variable = qing_caravan_kok_yielded }  # once-only
```

**New effects:** se_QING_CARAVAN.txt
- `QING_caravan_dictate_terms` — prosperity +12, control +8 via `QING_ili_apply_prov_band = { INTENT = secure_one }` + `QING_xj_derive_control`, clear `qing_xj_khoja_pending`, set `qing_caravan_kok_terms_dictated` flag. Permanently END khoja-scare/route-cut (gate them on NOT this flag).
- `QING_caravan_absorb_route` — customs_rate=2, prosperity +15, clear khoja-scare, +legitimacy 8. Set `qing_caravan_kok_absorbed` flag.

**Mission-tree tie-in:** qing_central_asia_missions.txt task `qing_ca_khanates` (:127-156) completion adds:
```
# Overawing Kokand unlocks the dictate-terms path if the aqsaqal was never granted.
if = {
    limit = { NOT = { has_variable = qing_caravan_aqsaqal_granted } }
    trigger_event = { id = qing_caravan.3  days = { 5 15 } }
}
```

Alternative: add a NEW mission task `qing_ca_kokand_subjugate` gated on `c:KOK = { is_subject_of = ROOT }` OR controlling Fergana capital, unlocking the caravan.3 event. Placed after qing_ca_khanates in tree (requires qing_ca_khanates).

**PROVEN idioms:**
- `is_subject_of = ROOT` (se_QING_CENTRAL_ASIA.txt :31/35/39/54/58/62).
- `QING_ili_apply_prov_band = { INTENT = secure_one }` (se_QING_XINJIANG.txt :106/173/201, qing_caravan.2 escort :481).
- `QING_xj_derive_control` (se_QING_XINJIANG.txt :230-270, called after every grip change).
- `opinion = { target = ROOT  value < X }` (se_QING_CARAVAN.txt :269).
- `is_capital_of = c:TAG` — **NEEDS VERIFICATION** (not found in corpus; alternative: `tag = KOK` in province owner scope).
- Mission `on_completion` adding event trigger (qing_xinjiang_missions.txt :74-79).

### B. Central-Asia dominion feeds Xinjiang consolidation

#### B.1 — Add Central-Asia term to control derivation

**Modify:** se_QING_XINJIANG.txt `QING_xj_derive_control` (:230-270). After line 255 (frontier_secured term), add:

```
# Central-Asia dominion: holding/subjugating the neighbouring khanates (KOK/BUK/KHV) + Kazakh hordes
# strengthens the grip on Xinjiang — the pacified hinterland secures the frontier. +5 per subjugated
# khanate/horde (cap +15 for all three khanates), mirroring qing_ili_frontier_secured +10.
set_variable = { name = qing_xj_ctl_term  value = 0 }
if = { limit = { exists = c:KOK  c:KOK = { is_subject_of = ROOT } }  change_variable = { name = qing_xj_ctl_term  add = 5 } }
if = { limit = { exists = c:BUK  c:BUK = { is_subject_of = ROOT } }  change_variable = { name = qing_xj_ctl_term  add = 5 } }
if = { limit = { exists = c:KHV  c:KHV = { is_subject_of = ROOT } }  change_variable = { name = qing_xj_ctl_term  add = 5 } }
# Kazakh hordes add a smaller +2 each (steppe buffer, not the key Fergana nexus).
if = { limit = { exists = c:GKH  c:GKH = { is_subject_of = ROOT } }  change_variable = { name = qing_xj_ctl_term  add = 2 } }
if = { limit = { exists = c:ORT  c:ORT = { is_subject_of = ROOT } }  change_variable = { name = qing_xj_ctl_term  add = 2 } }
if = { limit = { exists = c:KSH  c:KSH = { is_subject_of = ROOT } }  change_variable = { name = qing_xj_ctl_term  add = 2 } }
change_variable = { name = qing_xj_control_tmp  add = var:qing_xj_ctl_term }
LOG_line = { sys = QING  msg = "xinjiang: Central-Asia dominion control term for" }
```

**Effect:** subjugated KOK +5 control → `qing_xj_consolidation` rises (it reads `qing_xinjiang_control` as base :210) → eases Xinjiang mission-tree gates. Fully pacifying Central Asia (KOK+BUK+KHV) = +15 control, roughly matching one mission-task's secured-oasis contribution.

**PROVEN:** `is_subject_of = ROOT` (above). set_variable/change_variable/add on scratch var (lines :231-264 passim). LOG_line static msg.

#### B.2 — Subjugated/annexed Kokand ends the khoja-scare

**Modify:** se_QING_XINJIANG.txt `QING_xj_pulse` khoja-scare roll (:502-519). Change limit (:503-512) to:

```
limit = {
    has_variable = qing_xinjiang_control
    var:qing_xinjiang_control <= 30
    OR = {
        var:qing_xj_beg_count = 0
        var:qing_xj_beg_venal_count > 0
    }
    NOT = { has_variable = qing_xj_khoja_pending }
    # [LINK] khoja-scare is 'backed from Kokand' (separatism-backer rule). A subjugated OR annexed
    # Kokand CANNOT back pretenders → suppress the scare trigger entirely. Guard on KOK existing
    # as a free/hostile actor (not a CHI subject, not conquered).
    OR = {
        NOT = { exists = c:KOK }
        AND = {
            exists = c:KOK
            NOT = { c:KOK = { is_subject_of = ROOT } }
            # [NEEDS VERIFICATION] KOK not conquered — check CHI does NOT control KOK's capital.
            # Alternative if is_capital_of unavailable: set a flag qing_kok_conquered when CHI
            # takes Fergana capital provinces, gate on NOT that flag.
            NOT = { any_owned_province = { is_capital_of = c:KOK } }
        }
    }
}
```

**Effect:** once KOK is made a subject OR its capital provinces are annexed, `qing_xj_khoja_pending` can never be set → caravan.2 route-cut crisis stops firing (it triggers on khoja_pending :278). The player's Central-Asia conquest SOLVES the khoja threat permanently.

**Also modify:** qing_caravan_events.txt events .1/.2 add to their `trigger` blocks:
```
# [LINK] Kokand ultimatum/route-cut cannot fire if Kokand is a CHI subject or conquered (no backer).
OR = {
    NOT = { exists = c:KOK }
    AND = {
        exists = c:KOK
        NOT = { c:KOK = { is_subject_of = ROOT } }
        NOT = { any_owned_province = { is_capital_of = c:KOK } }
    }
}
```

**PROVEN:** `is_subject_of = ROOT` (above). `any_owned_province` iteration + limit (se_QING_XINJIANG.txt :458-465 contested-oasis check). `is_capital_of = c:TAG` — **NEEDS VERIFICATION**.

**Fallback if is_capital_of unproven:** add flag `qing_kok_conquered` set by a new effect `QING_ca_kok_conquered` called when CHI takes ≥ 3 Fergana provinces including p:110 (Kokand city). Gate khoja-scare on `NOT = { has_variable = qing_kok_conquered }`.

## 2. Mission-tree tie-ins

**Option A — minimal (event-driven):**
- qing_ca_khanates completion (se_QING_CENTRAL_ASIA.txt :51-66, qing_central_asia_missions.txt :127-156) triggers caravan.3 if aqsaqal not granted.
- NO new tasks; rely on player noticing control rising from subjugated khanates eases Xinjiang tree.

**Option B — explicit gate (new task):**
Add task `qing_ca_xinjiang_secured` to qing_central_asia_missions.txt:
```
qing_ca_xinjiang_secured = {
    icon = qing_ca_xinjiang_secured
    requires = { qing_ca_khanates }
    allow = {
        custom_tooltip = {
            text = qing_ca_xinjiang_secured_tt
            has_variable = qing_xinjiang_control
            var:qing_xinjiang_control >= 70
        }
    }
    on_completion = {
        custom_tooltip = qing_ca_xinjiang_secured_tt
        current_ruler = { add_popularity = 12 }
        # subjugating the khanates secures the New Dominion — stamp one more oasis secured.
        QING_ili_apply_prov_band = { INTENT = secure_one }
        QING_xj_derive_control = yes
        LOG_line = { sys = QING  msg = "MISSION task Central Asia secures Xinjiang for" }
    }
}
```
Placed after qing_ca_khanates, before qing_ca_ferghana. Gates on control ≥ 70 (risen FROM the khanate-subjugation terms), making Central-Asia conquest a VISIBLE path to Xinjiang consolidation.

**PROVEN:** mission task structure + custom_tooltip var-check (qing_xinjiang_missions.txt :92-123 qing_xj_fortify). `QING_ili_apply_prov_band = { INTENT = secure_one }` + `QING_xj_derive_control` (above).

**Recommendation:** Option A (event-driven) for build; Option B deferred to follow-up if playtest shows the link is too subtle.

## 3. Caravan model switch (conquer vs concede)

**Current:** aqsaqal granted → prosperity boosted but customs halved (:217-219); aqsaqal revoked → legitimacy +3, KOK angered, grip frays (:436-461).

**After conquest (caravan.3 "dictate terms"):** set flag `qing_caravan_kok_terms_dictated`. Modify `QING_caravan_pulse` (:164-286):
- Line 217-219 (aqsaqal customs haircut) add guard:
  ```
  if = {
      limit = {
          has_variable = qing_caravan_aqsaqal_granted
          NOT = { has_variable = qing_caravan_kok_terms_dictated }
      }
      change_variable = { name = qing_caravan_income_tmp  divide = 2 }
  }
  ```
  Effect: after dictating terms, CHI collects FULL customs even if aqsaqal was historically granted (conquest supersedes treaty).

- Lines 258-274 (Kokand ultimatum offer) add guard `NOT = { has_variable = qing_caravan_kok_terms_dictated }`.
- Lines 276-284 (route-cut offer) add guard `NOT = { has_variable = qing_caravan_kok_terms_dictated }`.

**Effect:** completing caravan.3 permanently ends both crisis chains (ultimatum + route-cut), and restores full customs. Conquest is a ONE-TIME alternative to managing the aqsaqal/khoja cycle.

**PROVEN:** flag set + guard (se_QING_CARAVAN.txt :70-84 init, :401 aqsaqal_granted guard). divide operation on var (line :203).

## 4. Files affected

**New:**
- `events/imp19c_mod_events/qing_caravan_events.txt` — add event `qing_caravan.3` (浩罕屈服) with 2 options (dictate/absorb).
- `localization/english/qing_caravan_l_english.yml` — loc keys for qing_caravan.3 title/desc/options + tooltips.

**Modified:**
- `common/scripted_effects/se_QING_XINJIANG.txt` —
  - `QING_xj_derive_control` (:230-270): add Central-Asia-dominion term (6 khanate/horde subject checks, +21 lines).
  - `QING_xj_pulse` (:428-522): khoja-scare limit add KOK-backer guard (+8 lines).
- `common/scripted_effects/se_QING_CARAVAN.txt` —
  - Add `QING_caravan_dictate_terms` (~15 lines).
  - Add `QING_caravan_absorb_route` (~12 lines).
  - `QING_caravan_pulse` (:164-286): add caravan.3 offer branch (~12 lines), guard ultimatum/route-cut/customs-haircut on NOT kok_terms_dictated (~6 lines).
- `common/scripted_effects/se_QING_CENTRAL_ASIA.txt` — (optional) add `QING_ca_embrace_khanates` hook to trigger caravan.3 (~3 lines in :51-66).
- `events/imp19c_mod_events/qing_caravan_events.txt` — modify .1/.2 triggers add KOK-backer guard (~5 lines each).
- `common/missions/qing_central_asia_missions.txt` — (Option B only) add task qing_ca_xinjiang_secured (~30 lines).

**Estimate:** ~150 lines new/modified code across 5-6 files.

## 5. Build checklist

1. **Write caravan.3 event** (qing_caravan_events.txt) — 2 options, trigger guard, immediate set flag, loc keys.
2. **Write new effects** (se_QING_CARAVAN.txt) — `QING_caravan_dictate_terms`, `QING_caravan_absorb_route`.
3. **Modify QING_xj_derive_control** (se_QING_XINJIANG.txt :230-270) — add Central-Asia term block (6 subject checks).
4. **Modify QING_xj_pulse khoja-scare** (se_QING_XINJIANG.txt :502-519) — add KOK-backer guard to limit.
5. **Modify QING_caravan_pulse** (se_QING_CARAVAN.txt :164-286) — add caravan.3 offer branch, guard ultimatum/route-cut/haircut.
6. **Modify caravan.1/.2 triggers** (qing_caravan_events.txt :54-65/:140-145) — add KOK-backer guard.
7. **(Optional)** add qing_ca_xinjiang_secured task (qing_central_asia_missions.txt).
8. **Loc** — qing_caravan.3 strings + tooltips (qing_caravan_l_english.yml).
9. **LOG all new branches** — static msgs, sys = QING.
10. **Boot-test** — CHI 1763, grant aqsaqal → revoke → conquer KOK → caravan.3 fires, dictate terms, verify khoja-scare stops, control rises, customs full.
11. **Playtest weights** — Central-Asia term +5/+2 placeholder; verify control ≥ 70 reachable via khanate path, doesn't trivialise Xinjiang tree.

## 6. Risks + mitigations

**RISK 1 — caravan↔control feedback loop reintroduced:**  
Meter-concretize #10B removed prosperity→control couple to break the loop. This design adds khanate-subjugation → +control AND khanate-subjugation → caravan.3 dictate-terms → +prosperity. But the loop is ONE-WAY NOW: conquest → control/prosperity both rise, but prosperity does NOT nudge control back (that couple is deleted :232-235 comment). Safe.

**RISK 2 — is_capital_of unproven:**  
`any_owned_province = { is_capital_of = c:KOK }` not found in corpus. **Mitigation:** test in console OR use fallback flag `qing_kok_conquered` set when CHI controls ≥ 3 Fergana provinces including p:110 (Kokand city). Verify capital-check or build fallback before merge.

**RISK 3 — conquering Kokand strands its sub-subjects:**  
If KOK holds other tags as its own subjects (not found in 1763 setup but possible in alt-history), absorbing KOK via `FUNC_make_subject` OR annexing its provinces could orphan them. **Mitigation:** se_SUBJECT_QING.txt `SUBJ_QING_reparent_sub_subjects` (:374-420) release-then-rebind pattern. When CHI makes KOK a subject, call reparent to lift KOK's subs to CHI. When annexing KOK, call `SUBJ_QING_absorb_subject` which already handles reparenting (:179-250). **Action:** verify qing_ca_khanates `FUNC_make_subject` call (:55) triggers reparent; if not, add explicit reparent loop after embrace in se_QING_CENTRAL_ASIA.txt.

**RISK 4 — Central-Asia term weights untuned:**  
+5/khanate, +2/horde → full pacification +21 control is ~2 mission-task beats. May trivialise Xinjiang tree OR be too weak. **Mitigation:** PLACEHOLDER-playtest weights. Boot-log the raw term at 1763 (0, no khanates subjugated) and after subjugating KOK/BUK/KHV (should land +15 → control rises ~15 → qing_xj_consolidation base lifts). Pin to historical: subjugating Kokand historically DID ease Xinjiang (1860s context), so +5 defensible. Tune in build-probe.

**RISK 5 — caravan.3 timing (fires too early/late):**  
Trigger fires when KOK subjugated OR refused aqsaqal + KOK hostile. May fire before player ready OR not fire when expected. **Mitigation:** throttle via once-only flag `qing_caravan_kok_yielded` + 5-15 day delay. If subjugate-KOK path fires .3 immediately, add cooldown var (e.g. quarters-since-subjugate ≥ 2). Playtest trigger.

**RISK 6 — mission-tree soft-lock (Option B):**  
Adding qing_ca_xinjiang_secured gated on control ≥ 70 creates circular dependency if control CAN'T reach 70 without completing other tasks. **Mitigation:** control derivation includes begs/tuntian/xiexiang (player-controlled) + ILI subject (setup) + Central-Asia (via this design). 1763 opens ~38 (ILI 30 + 2 begs ×4); +2 begs +1 tuntian +xiexiang = +18 → 56; +KOK+BUK+KHV = +15 → 71. Reachable WITHOUT Xinjiang tree. Safe. But Option A (event-driven, no gate) avoids risk entirely. **Recommend Option A.**

## 7. Design Q&A

**Q: Why not let aqsaqal-granted players re-negotiate after conquering KOK?**  
A: caravan.3 "dictate terms" IS the re-negotiation, offered when KOK subjugated (trigger line A.2). If aqsaqal already granted, dictate-terms overrides it (restores full customs, clears crisis chains). No separate re-negotiate option needed.

**Q: Does annexing KOK (full conquest, not subject) also trigger benefits?**  
A: Yes. Khoja-scare guard checks `NOT = { any_owned_province = { is_capital_of = c:KOK } }` (annexed capital = conquered). Control derivation checks `c:KOK = { is_subject_of = ROOT }` (false if annexed) — so annexed KOK does NOT give +5 control, but DOES suppress khoja-scare + unlock caravan.3. Trade-off: subject = +5 control ongoing; annex = one-time caravan.3 benefit. Historically CHI preferred suzerainty over annexation (cheaper, fits sinosphere model). Design mirrors that.

**Q: What if player conquers Fergana but KOK tag still exists elsewhere (driven out)?**  
A: Caravan.3 trigger OR-branch handles both: `c:KOK = { is_subject_of = ROOT }` (subjugated wherever) OR `any_owned_province = { count ≥ 3  is_in_region = Fergana  is_capital_of = c:KOK }` (held KOK capital). If KOK driven to steppe, no capital in Fergana → caravan.3 won't fire from conquest path, but subjugating the rump KOK still triggers it. Khoja-scare suppression similarly keys on subject OR capital-held. Covers both cases.

**Q: Does this obsolete the aqsaqal levers (grant/revoke)?**  
A: No. Aqsaqal path remains for players who don't conquer Central Asia OR grant concession before 1820 date-gate. Conquest is ALTERNATIVE, not replacement. Both paths coexist. A player who granted aqsaqal 1825, then conquers KOK 1830, fires caravan.3 and can dictate-terms (overriding prior grant). A player who never grants + never conquers faces recurring ultimatum/route-cut (historical 1832-1847 cycle).

## 8. Standing-rule compliance

- **concrete-over-abstract** — control derivation from real KOK subject status (not abstract "khanate pacified" counter). ✓
- **separatism-backer rule** — khoja-scare "backed from Kokand" (neighbouring Turkic power :20). Suppressed when backer subjugated/conquered. ✓
- **proven-code rule** — `is_subject_of`, `QING_ili_apply_prov_band`, `QING_xj_derive_control`, `FUNC_make_subject`, mission task structure all in-repo proven. ✓
- **log static msgs** — all new effects logged sys = QING, static strings. ✓
- **review-before-commit** — this is DESIGN; needs adversarial design review, then build, then code review. ✓
- **error-logging** — post-impl review adds se_LOG to new effects (checklist item 9). ✓

## 9. Verification TODOs (before build)

1. **CRITICAL:** verify `is_capital_of = c:TAG` trigger exists and works in province scope. Console-test `any_owned_province = { is_capital_of = c:KOK }` OR grep TI/Invictus oracle repos. If unavailable, build fallback flag `qing_kok_conquered`.
2. **Verify:** `FUNC_make_subject` for khanates (se_QING_CENTRAL_ASIA.txt :55) triggers sub-subject reparenting. If not, add explicit `SUBJ_QING_reparent_sub_subjects` call in se_QING_CENTRAL_ASIA.txt after embrace loop.
3. **Playtest weights:** Central-Asia control term +5/+2 — boot-log raw, verify control rises to ≥ 70 reachable, doesn't trivialise.
4. **Oracle consult:** search TI `missions/*.txt` for caravan-trade / khanate-conquest examples of mission-event tie-ins.

## 10. Alternatives considered

**ALT A — Abstract "Central Asia pacified" counter:**  
Rejected. Violates concrete-over-abstract rule. Real KOK subject status is on-map, more transparent.

**ALT B — Add Central-Asia term to consolidation score, not control:**  
Rejected. Consolidation (se_QING_XINJIANG.txt :171-219) is control + admin-bias ONLY after #10B meter-concretize. Adding khanate term there would reintroduce abstract meter layering. Control derivation is the right place (it's already a concrete-object sum).

**ALT C — Make caravan.3 a mission task instead of event:**  
Rejected. Mission tasks are build/hold goals; caravan.3 is a CRISIS RESOLUTION (player choice under pressure). Event is the right form (precedent: qing_caravan.1/.2 are events, not tasks).

**ALT D — Suppress khoja-scare entirely once any khanate subjugated:**  
Rejected. Khoja-scare is specifically "backed from Kokand" (history). BUK/KHV subjugation should ease grip (control term) but not suppress khoja unless KOK itself is neutralised. Design correctly keys scare-suppression only on KOK.

## 11. Phasing (if implementation split needed)

**Phase 1 (minimum viable link):**
- Modify `QING_xj_derive_control` add Central-Asia term.
- Modify `QING_xj_pulse` khoja-scare add KOK-backer guard.
- Boot-test: subjugate KOK → control rises, khoja stops.

**Phase 2 (caravan conquest path):**
- Write caravan.3 event + new effects.
- Modify `QING_caravan_pulse` add caravan.3 offer + guards.
- Playtest: conquer KOK → caravan.3 → dictate terms → full customs, no crises.

**Phase 3 (mission tie-in, optional):**
- Add qing_ca_xinjiang_secured task (Option B).

**Recommend:** build Phase 1+2 together (they interlock — Central-Asia term + khoja-suppression justify caravan.3 conquest payoff). Phase 3 deferred if time-constrained.

---

**Estimate:** 150 lines code, 6 files, ~2 days build + 1 day test. Needs design review + oracle verification (is_capital_of) before start.
