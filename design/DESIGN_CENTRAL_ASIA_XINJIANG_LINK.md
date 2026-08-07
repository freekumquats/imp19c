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
- **Dictate terms** (天朝定制) — reopen caravan trade on CHI-dictated terms: NO aqsaqal, NO customs
  haircut (set `qing_caravan_kok_terms_dictated`), clear khoja-scare, secure one oasis (`INTENT =
  secure_one` = **+3 control** in the derive, see LOW-7 below). Costs: treasury -100, popularity +20.
- **Absorb the route** (併商道) — fold Kokand merchants into CHI state monopoly: clear khoja-scare,
  +legitimacy 8. Costs: political_influence -40.

**[FIX 2026-08-07 — MEDIUM-5] prosperity payoffs removed as one-shot nudges.**
`qing_caravan_prosperity` is a HYSTERESIS-EASED DERIVE (eases ¼ toward a recomputed *target* each pulse,
se_QING_CARAVAN.txt:168-174), NOT a settable stock. A one-shot `+12`/`+15` `QING_DECLINE_nudge` bleeds
off within a few pulses — worse, "Absorb route" set `customs_rate = 2` (heavy), which *lowers* the
prosperity target by −15 (recompute_target :138-141), so the heavy-customs penalty would persist while
the +15 vanished (net negative — self-defeating, the same class as the #10B control error). Instead the
two paths change what the derive READS.

**[FIX 2026-08-07 — NEW-MEDIUM-1] correct the prosperity lever.** The re-review found the "restores full
customs → raises the prosperity target" chain is MECHANICALLY FALSE: the `:217` aqsaqal haircut operates
on `qing_caravan_income_tmp` (the quarterly TREASURY take, computed *downstream* of prosperity as
`income = goods × prosperity/100 × rate`, :201-218). `QING_caravan_recompute_target` (:93-156) never
reads the haircut or the `kok_terms_dictated` flag — so un-halving the haircut raises **treasury income**,
NOT the prosperity target (the #10B couples that fed income back into prosperity were deleted). The ONE
durable prosperity lever caravan.3 actually pulls is **clearing `qing_xj_khoja_pending`**, which removes
the −15 route-disruption term in `recompute_target` (:148-151). So:
- Dictate terms: durable prosperity gain comes from **clearing the khoja scare** (−15 term drops out →
  target rises). Separately, the `kok_terms_dictated` flag restores full **treasury customs** (the :217
  haircut guard) — a treasury gain, NOT a prosperity gain. Keep both effects but attribute each to the
  right meter; do NOT claim the haircut moves prosperity.
- Absorb route: `customs_rate = 2` LOWERS the prosperity target (−15, monopoly extraction over volume) —
  thematically fine, but then do NOT also promise a prosperity boost. Its durable prosperity gain, like
  dictate, is only the khoja-clear. Pick the customs model deliberately; do not pair heavy customs with a
  prosperity-boost claim.
- If a bigger *durable* prosperity target lift is wanted for either path, add a `kok_terms_dictated`/
  `kok_absorbed` term to `recompute_target` itself (the only place that moves the target) — the concrete,
  #10B-clean way. Flagged for build.

**[FIX — LOW-7] "+8 control" corrected to +3.** One `secure_one` stamp = one `qing_xinjiang_prov_secured`
modifier = **+3** in `QING_xj_derive_control` (:249-252). Post-#10B you cannot "add 8 control" — you
secure map objects and control DERIVES. If a bigger conquest payoff is wanted, secure more oases
(call `secure_one` N times) or add a `qing_ili_frontier_secured` modifier (+10); state the real number.

**Trigger:** `qing_caravan.3` fires from `QING_caravan_pulse` when:
```
QING_kok_conquered_trigger = yes                   # subjugated OR Kokand city held — CONQUEST ONLY
NOT = { has_variable = qing_caravan_kok_yielded }  # once-only (set in the event IMMEDIATE, mirrors .1/.2)
```

**[FIX 2026-08-07 — NEW-MEDIUM-3] caravan.3 is STRICTLY CONQUEST-GATED.** The prior draft had a first
OR-branch that fired on merely "refused the aqsaqal AND KOK hostile AND explicitly NOT conquered" — which
would hand the full "The Khanate Yields" (浩罕屈服) dictate/absorb rewards (secure an oasis, suppress the
khoja scare, restore full customs / state monopoly) to an unbeaten, independent, hostile Kokand. That is
incoherent with the event's premise and, unlike caravan.1 (gated `current_date >= 1820.1.1` +
`prosperity >= 55`), that branch had NO date and NO prosperity throttle, so it could pre-empt the entire
aqsaqal arc as early as 1763 the moment `c:KOK opinion < 0`. It also contradicted §7 Q1's own mental
model ("dictate-terms is offered when KOK subjugated"). **Fix: drop the un-conquered branch entirely.**
The refuse-the-aqsaqal path already has its own consequences (caravan.1 refuse → arms the khoja scare →
route-cut cycle); "The Khanate Yields" now fires ONLY when Kokand is actually beaten (subjugated or its
city held). This also makes the event title truthful.

**[FIX 2026-08-07 — CRITICAL-1/2] `is_capital_of` does NOT exist** (absent in-repo AND in both
oracle repos — confirmed). The prior draft's `count >= 3 … is_capital_of = c:KOK` was doubly broken
(non-existent trigger + a country has exactly ONE capital, so "own 3 provinces each = KOK's capital"
is impossible). Conquest-detection is re-expressed on PROVEN idioms:
- `c:KOK = { is_subject_of = ROOT }` — subjugated (se_QING_CENTRAL_ASIA.txt:54).
- `owns_or_subject_owns = p:110` — CHI (or a CHI subject) holds **Kokand city** (p:110, the khanate
  seat; proven country trigger in Invictus/TI decisions + 00_missions.txt). This is the concrete
  "held the heartland" test, and correctly covers the case where a CHI *subject* (e.g. the Anxi
  march carved off Fergana) holds it.
- `any_owned_province = { count >= 1  is_in_region = Fergana }` — CHI directly holds Fergana ground
  (proven, qing_central_asia_missions.txt:172). Use this OR the p:110 test per how tight we want it.

Factor the conquest test into ONE scripted_trigger `QING_kok_conquered_trigger` (single source of
truth, reused by the caravan.3 trigger, the khoja-scare guard §B.2, and the .1/.2 guards):
```
QING_kok_conquered_trigger = {   # scope: country (CHI). TRUE once Kokand is neutralised by force.
    OR = {
        AND = { exists = c:KOK  c:KOK = { is_subject_of = ROOT } }   # subjugated
        owns_or_subject_owns = 110                                    # hold Kokand city (p:110, annexed heartland)
    }
}
```
**[LOW]** In-repo live script uses the BARE province id (`owns_or_subject_owns = 110`); the `p:110` form
is attested only in the oracle repos. Both parse; use bare `110` for in-repo consistency. p:110 = Kokand
city confirmed (setup/main/00_default.txt:46848 `capital = 110`; setup/provinces/00_Fergana.txt `110 = {
#Kokand … province_rank="city"`), so TODO §9.3 is CLOSED.

**New effects:** se_QING_CARAVAN.txt
- `QING_caravan_dictate_terms` — set `qing_caravan_kok_terms_dictated` (restores full TREASURY customs
  via the :217 haircut guard — a treasury gain, NOT prosperity, per NEW-MEDIUM-1), clear
  `qing_xj_khoja_pending` (THIS is the durable prosperity-target lift: drops the −15 term),
  `QING_ili_apply_prov_band = { INTENT = secure_one }` guarded on `NOT qing_xj_fully_integrated` (LOW —
  match the sibling levers) + `QING_xj_derive_control` (+3 control on the map). End the crisis chains by
  gating .1/.2 on `NOT QING_kok_yielded_flag` (§3, MEDIUM-6). NO one-shot prosperity nudge (MEDIUM-5).
- `QING_caravan_absorb_route` — set `qing_caravan_kok_absorbed`, clear `qing_xj_khoja_pending`,
  +legitimacy 8. Customs framing is the design decision flagged in MEDIUM-5 above (monopoly-heavy vs
  full) — pick ONE, do not pair heavy customs with a prosperity boost.
- Both set the terminal flag in the EVENT immediate (mirrors .1/.2 flag hygiene, MEDIUM-6); the
  once-only `qing_caravan_kok_yielded` guard is also set in the immediate.

**Mission-tree tie-in (PREFERRED — pulse-driven, no mission hook):** the caravan.3 offer lives in
`QING_caravan_pulse` gated on `QING_kok_conquered_trigger` (+ once-only flag). The pulse is the proven
offer site for .1/.2, already runs quarterly, and reads fresh conquest state — so subjugating OR
annexing Kokand drives caravan.3 with no dependency on the unverified mission `on_completion →
trigger_event` idiom (MEDIUM-4). `QING_ca_embrace_khanates` (se_QING_CENTRAL_ASIA.txt:51) is where the
subjugation happens; nothing extra is needed there.

**Alternative (only if MEDIUM-4 verifies):** fire caravan.3 from `qing_ca_khanates` `on_completion`.
Do NOT adopt unless `trigger_event`-in-`on_completion` is first confirmed legal.

**PROVEN idioms:**
- `is_subject_of = ROOT` (se_QING_CENTRAL_ASIA.txt :54/58/62).
- `QING_ili_apply_prov_band = { INTENT = secure_one }` (se_QING_ILI.txt :371; se_QING_XINJIANG.txt callers).
- `QING_xj_derive_control` (se_QING_XINJIANG.txt :230-270, called after every grip change).
- `opinion = { target = ROOT  value < X }` (se_QING_CARAVAN.txt :269).
- `owns_or_subject_owns = p:110` (Kokand city) — PROVEN country trigger (Invictus/TI decisions,
  00_missions.txt). REPLACES the non-existent `is_capital_of`.
- `any_owned_province = { count >= 1  is_in_region = Fergana }` (qing_central_asia_missions.txt :172).
- **[FIX — MEDIUM-4]** Mission `on_completion → trigger_event` is **UNVERIFIED** — the prior citation
  (qing_xinjiang_missions.txt :74-79) was false; those lines call `QING_xj_init = yes`, NOT
  `trigger_event`. NO task in either mission tree fires an event from `on_completion`. Before build,
  either (a) verify `trigger_event` is legal in a Jomini mission `on_completion` (grep TI/Invictus
  mission trees; console-test), or (b) preferred — do NOT couple via the mission at all: let
  `QING_caravan_pulse` offer caravan.3 off `QING_kok_conquered_trigger` (the pulse already runs and
  is the proven event-offer site for .1/.2), so the conquest itself (subjugate/annex) drives it with
  no mission-completion hook needed. **Recommend (b).**

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

**PROVEN:** `is_subject_of = ROOT` (above). set_variable/change_variable/add on the `qing_xj_ctl_term`
scratch var, added to `qing_xj_control_tmp` BEFORE the clamp/publish at :266-268 (exactly the existing
term pattern — NOT a post-publish nudge, so it is not erased by re-derivation; the #10B lesson is
respected). LOG_line static msg.

**[NOTE — LOW-8] `is_subject_of` is non-recursive.** At 1763 KSH is a *feudatory of ORT*, not of CHI
(setup/main/00_default.txt:764), so `c:KSH = { is_subject_of = ROOT }` is FALSE in that state. That is
fine for the intended path: `QING_ca_embrace_kazakh` (se_QING_CENTRAL_ASIA.txt:40) makes KSH a *direct*
CHI subject (severing KSH→ORT), after which the +2 counts. But a player who subjugates ORT by other
means will silently not get KSH's +2 (KSH stays ORT's subject). Acceptable; documented so it is not
mistaken for a bug. If we want the +2 to follow ORT, add `OR = { c:KSH = { is_subject_of = ROOT }
c:KSH = { overlord = { is_subject_of = ROOT } } }` (the nested-overlord idiom).

#### B.2 — Subjugated/annexed Kokand ends the khoja-scare

**Modify:** se_QING_XINJIANG.txt `QING_xj_pulse` khoja-scare roll (:503-519). Add ONE guard to the
limit (:504-511):

```
limit = {
    has_variable = qing_xinjiang_control
    var:qing_xinjiang_control <= 30
    OR = {
        var:qing_xj_beg_count = 0
        var:qing_xj_beg_venal_count > 0
    }
    NOT = { has_variable = qing_xj_khoja_pending }
    # [LINK] khoja-scare is 'backed from Kokand' (separatism-backer rule). Suppress it when Kokand is
    # currently beaten (conquered_trigger) OR was permanently settled by caravan.3 (yielded_flag).
    # [FIX NEW-MEDIUM-2] BOTH guards, different lifetimes — see below.
    NOT = { OR = { QING_kok_conquered_trigger = yes  QING_kok_yielded_flag = yes } }
}
```

**[FIX 2026-08-07 — MEDIUM-3] the prior guard was LOGICALLY INVERTED.** It enabled the scare via
`OR = { NOT = { exists = c:KOK } ... }` — meaning a FULLY ANNEXED / destroyed KOK (tag gone) would
*re-enable* the scare, while conquering less (tag survives) suppressed it: conquering MORE turned the
threat back ON, the opposite of the goal. Replaced with `NOT = { QING_kok_conquered_trigger = yes }`,
which is monotonic: subjugated OR Kokand-city-held ⇒ conquered ⇒ scare suppressed; otherwise it can
fire. (If KOK is destroyed AND CHI does not hold p:110, the trigger is false and the scare CAN fire —
which is correct: a driven-off-but-not-held Kokand can still shelter pretenders in the hills.)

**[FIX 2026-08-07 — NEW-MEDIUM-2] the scare guard needs BOTH triggers (different lifetimes).**
`QING_kok_conquered_trigger` is a LIVE derive — it flips back false if KOK later breaks vassalage and CHI
does not hold p:110. `QING_kok_yielded_flag` (dictated/absorbed) is PERMANENT. If the scare were gated on
the live trigger alone, then "resolve via caravan.3 → later lose Kokand" would re-arm the khoja scare
(re-set `qing_xj_khoja_pending`, re-fire qing_xinjiang.1, re-apply the −15 prosperity drag) while the
paired caravan route-cut (gated on the permanent `yielded_flag`) stayed dead — a jarring half-resurrected
crisis, and it breaks §3's "permanently ends the khoja-scare" promise. Gating on
`NOT = { OR = { conquered_trigger  yielded_flag } }` fixes it: a caravan.3-RESOLVED Kokand stays settled
forever (yielded_flag), while a merely-driven-off-never-settled Kokand can still re-arm (§7 Q4's desired
raw case — neither flag set). The two consumers now express two different intents correctly.

**Effect:** once KOK is subjugated / Kokand city held / settled via caravan.3, `qing_xj_khoja_pending` can
never be set → caravan.2 route-cut crisis stops firing. A never-settled rump Kokand can still stir.

**Also modify:** qing_caravan_events.txt events .1/.2 add ONE line to their `trigger` blocks:
```
# [LINK] ultimatum/route-cut cannot fire once Kokand is beaten or settled via caravan.3.
NOT = { QING_kok_yielded_flag = yes }
NOT = { QING_kok_conquered_trigger = yes }
```
(This also fixes the MEDIUM-3 inversion for the events — the prior `NOT = { exists = c:KOK }` branch
would have let the "Kokand ultimatum" fire when Kokand does not exist.)

**PROVEN:** `is_subject_of = ROOT`, `owns_or_subject_owns = p:110` (above). Single scripted_trigger reused.

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

- Kokand ultimatum offer + route-cut offer add guard `NOT = { QING_kok_yielded_flag = yes }`.

**[FIX 2026-08-07 — MEDIUM-6] three distinct flags; use a scripted_trigger for the "yielded" test.**
There are THREE flags with different jobs — do not conflate them:
- `qing_caravan_kok_yielded` — the once-only OFFER guard (set in caravan.3's immediate so a re-check
  failure during the 5-15 day delay never strands it; mirrors .1/.2's own-immediate discipline).
- `qing_caravan_kok_terms_dictated` — end-state of the *dictate* option (restores full customs).
- `qing_caravan_kok_absorbed` — end-state of the *absorb* option (state monopoly).

Both END-STATE flags must suppress the crisis chains, so gate the pulse offers on a scripted_trigger,
NOT on `kok_terms_dictated` alone (else the absorb-route player would keep getting ultimatums):
```
QING_kok_yielded_flag = { OR = { has_variable = qing_caravan_kok_terms_dictated
                                 has_variable = qing_caravan_kok_absorbed } }
```
The customs-haircut guard (:217) keys specifically on `kok_terms_dictated` (only dictate restores full
customs; absorb sets its own customs model per MEDIUM-5).

**Effect:** completing caravan.3 (either option) permanently ends both caravan crisis chains (they gate
on the permanent `QING_kok_yielded_flag`), AND — because the khoja scare is now gated on `OR {
conquered_trigger  yielded_flag }` (NEW-MEDIUM-2) — the khoja scare stays suppressed even if Kokand
later breaks free. Dictate also restores full treasury customs. Conquest/settlement is a ONE-TIME
alternative to managing the aqsaqal/khoja cycle.

**PROVEN:** flag set + guard (se_QING_CARAVAN.txt :70-84 init, :401 aqsaqal_granted guard). divide operation on var (line :203).

## 4. Files affected

**New:**
- `common/scripted_triggers/qing_kok_triggers.txt` (or an existing Qing scripted_trigger file) —
  `QING_kok_conquered_trigger`, `QING_kok_yielded_flag` (~8 lines).
- `events/imp19c_mod_events/qing_caravan_events.txt` — add event `qing_caravan.3` (浩罕屈服) with 2 options (dictate/absorb).
- `localization/english/qing_caravan_l_english.yml` — loc keys for qing_caravan.3 title/desc/options + tooltips (BOM).

**Modified:**
- `common/scripted_effects/se_QING_XINJIANG.txt` —
  - `QING_xj_derive_control` (:230-268): add Central-Asia-dominion term via `qing_xj_ctl_term` scratch,
    BEFORE the :266 clamp (6 khanate/horde subject checks, ~+10 lines).
  - `QING_xj_pulse` khoja-scare limit (:503-511): add `NOT = { QING_kok_conquered_trigger = yes }` (+1 line).
- `common/scripted_effects/se_QING_CARAVAN.txt` —
  - Add `QING_caravan_dictate_terms` (~12 lines), `QING_caravan_absorb_route` (~10 lines).
  - `QING_caravan_pulse`: add caravan.3 offer branch, guard ultimatum/route-cut on `NOT QING_kok_yielded_flag`,
    customs haircut on `NOT kok_terms_dictated`.
- `events/imp19c_mod_events/qing_caravan_events.txt` — modify .1/.2 triggers: add `NOT = { QING_kok_conquered_trigger = yes }` (+1 line each).
- `common/missions/qing_central_asia_missions.txt` — (Option B only) add task qing_ca_xinjiang_secured (~30 lines).

**Estimate:** ~150 lines new/modified code across 5-6 files.

## 5. Build checklist

0. **Add scripted_triggers** (common/scripted_triggers/) — `QING_kok_conquered_trigger` (subjugated OR
   owns_or_subject_owns p:110) and `QING_kok_yielded_flag` (dictated OR absorbed). Single source of truth.
1. **Write caravan.3 event** (qing_caravan_events.txt) — 2 options, trigger on `QING_kok_conquered_trigger`
   + `NOT qing_caravan_kok_yielded`, IMMEDIATE sets `qing_caravan_kok_yielded` + the option's end-state
   flag, loc keys.
2. **Write new effects** (se_QING_CARAVAN.txt) — `QING_caravan_dictate_terms` (flag + secure_one +3 +
   derive + clear khoja), `QING_caravan_absorb_route` (flag + clear khoja + legitimacy). NO prosperity nudge.
3. **Modify QING_xj_derive_control** (se_QING_XINJIANG.txt :230-268) — add the Central-Asia term via the
   `qing_xj_ctl_term` scratch, added to `qing_xj_control_tmp` BEFORE the :266 clamp (6 subject checks).
4. **Modify QING_xj_pulse khoja-scare** (se_QING_XINJIANG.txt :503-519) — add `NOT = {
   QING_kok_conquered_trigger = yes }` to the limit.
5. **Modify QING_caravan_pulse** (se_QING_CARAVAN.txt) — add the caravan.3 offer as an INDEPENDENT `if`
   BEFORE the existing `if {ultimatum} else_if {route-cut}` chain (:258-284), so a conquered-but-still-
   hostile KOK gets "The Khanate Yields", not a shadowed ultimatum; the ultimatum/route-cut offers are in
   turn guarded on `NOT QING_kok_yielded_flag` + `NOT QING_kok_conquered_trigger` (so they don't compete).
   Guard the customs haircut on `NOT kok_terms_dictated`.
6. **Modify caravan.1/.2 triggers** (qing_caravan_events.txt) — add `NOT = { QING_kok_conquered_trigger = yes }`.
7. **(Optional)** add qing_ca_xinjiang_secured task (qing_central_asia_missions.txt).
8. **Loc** — qing_caravan.3 strings + tooltips (qing_caravan_l_english.yml, BOM).
9. **LOG all new branches** — static msgs, sys = QING (no data-functions/`#`/`$macro$` in LOG strings).
10. **Boot-test** — CHI 1763, grant aqsaqal → revoke → conquer KOK → caravan.3 fires, dictate terms, verify khoja-scare stops, control rises, customs full.
11. **Playtest weights** — Central-Asia term +5/+2 placeholder; verify control ≥ 70 reachable via khanate path, doesn't trivialise Xinjiang tree.

## 6. Risks + mitigations

**RISK 1 — caravan↔control feedback loop reintroduced:**  
Meter-concretize #10B removed prosperity→control couple to break the loop. This design adds khanate-subjugation → +control AND khanate-subjugation → caravan.3 dictate-terms → +prosperity. But the loop is ONE-WAY NOW: conquest → control/prosperity both rise, but prosperity does NOT nudge control back (that couple is deleted :232-235 comment). Safe.

**RISK 2 — RESOLVED: `is_capital_of` does not exist.**  
Confirmed absent in-repo AND in both oracle repos. Replaced entirely with `owns_or_subject_owns = p:110`
(proven country trigger, Invictus/TI) + `c:KOK = { is_subject_of = ROOT }`, factored into the
`QING_kok_conquered_trigger` scripted_trigger. No console test or fallback flag needed. (The old
"fallback flag `qing_kok_conquered`" is likewise unnecessary — the scripted_trigger IS the clean form.)

**RISK 3 — MOOT at 1763; low elsewhere.**  
At 1763 setup KOK holds NO sub-subjects, and `QING_ca_embrace_khanates` (se_QING_CENTRAL_ASIA.txt:51-63)
subjugates KOK/BUK/KHV via plain `FUNC_make_subject` (no reparent needed — nothing to reparent). In
alt-history where KOK gained sub-subjects, `SUBJ_QING_reparent_sub_subjects` and `SUBJ_QING_absorb_subject`
exist (se_SUBJECT_QING.txt) to handle it, but this design adds NO annexation path of its own (conquest is
the player's via normal war), so it introduces no new orphan risk. No action required for build.

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
A: Yes. `QING_kok_conquered_trigger` is TRUE on `owns_or_subject_owns = p:110` (Kokand city held), so
annexation suppresses the khoja-scare + unlocks caravan.3. The B.1 control term keys on
`c:KOK = { is_subject_of = ROOT }` (false if annexed) — so annexed KOK does NOT give the +5 control
term, but DOES suppress the scare + unlock caravan.3. Trade-off: subject = +5 control ongoing; annex =
scare-suppression + one-time caravan.3 benefit. Historically CHI preferred suzerainty (cheaper, fits the
sinosphere model). Design mirrors that.

**Q: What if player conquers Fergana but KOK tag still exists elsewhere (driven out)?**  
A: `QING_kok_conquered_trigger` handles both: `c:KOK = { is_subject_of = ROOT }` (subjugated wherever)
OR `owns_or_subject_owns = p:110` (Kokand city held). If KOK is driven to the steppe and CHI does NOT
hold p:110, the trigger is false → caravan.3 won't fire from the conquest path and the scare CAN still
fire (correct: a rump Kokand in the hills can still shelter pretenders); but subjugating the rump KOK
flips the trigger true. Both the caravan.3 offer and the scare-suppression key on the same trigger, so
they stay consistent.

**Q: Does this obsolete the aqsaqal levers (grant/revoke)?**  
A: No. Aqsaqal path remains for players who don't conquer Central Asia OR grant concession before 1820 date-gate. Conquest is ALTERNATIVE, not replacement. Both paths coexist. A player who granted aqsaqal 1825, then conquers KOK 1830, fires caravan.3 and can dictate-terms (overriding prior grant). A player who never grants + never conquers faces recurring ultimatum/route-cut (historical 1832-1847 cycle).

## 8. Standing-rule compliance

- **concrete-over-abstract** — control derivation from real KOK subject status (not abstract "khanate pacified" counter). ✓
- **separatism-backer rule** — khoja-scare "backed from Kokand" (neighbouring Turkic power :20). Suppressed when backer subjugated/conquered. ✓
- **proven-code rule** — `is_subject_of`, `QING_ili_apply_prov_band`, `QING_xj_derive_control`,
  `FUNC_make_subject`, `owns_or_subject_owns = p:NNN`, `opinion = { value < X }` all proven (in-repo or
  oracle). `is_capital_of` was NOT proven — REMOVED (it does not exist). Mission `on_completion →
  trigger_event` NOT proven — design routes around it (pulse-driven). ✓ (after 2026-08-07 review fixes)
- **log static msgs** — all new effects logged sys = QING, static strings. ✓
- **review-before-commit** — this is DESIGN; needs adversarial design review, then build, then code review. ✓
- **error-logging** — post-impl review adds se_LOG to new effects (checklist item 9). ✓

## 9. Verification TODOs (before build)

1. ~~**CRITICAL:** verify `is_capital_of`.~~ **RESOLVED** — it does not exist (in-repo or oracle);
   replaced with `owns_or_subject_owns = 110` + `is_subject_of` in `QING_kok_conquered_trigger`.
2. ~~**Verify** `FUNC_make_subject` reparenting.~~ **RESOLVED** — KOK holds no sub-subjects at 1763;
   embrace uses plain `FUNC_make_subject`; this design adds no annexation path. No action.
3. ~~**Verify `owns_or_subject_owns = 110`** = Kokand city.~~ **RESOLVED** — `capital = 110`
   (setup/main/00_default.txt:46848); province 110 is Kokand `province_rank="city"`
   (setup/provinces/00_Fergana.txt). Use the bare `110` form (in-repo convention).
4. **[STILL OPEN — MEDIUM-4] Verify `trigger_event` in a mission `on_completion`** IF the alternative
   mission-hook path is chosen. Preferred design avoids this entirely (pulse-driven), so this is only a
   blocker for the alternative. Grep TI/Invictus mission trees / console-test.
5. **Playtest weights:** Central-Asia control term +5/+2 — boot-log raw, verify control ≥ 70 reachable
   via the khanate path, doesn't trivialise the Xinjiang tree.
6. **Decide the once-only re-fire semantics:** `qing_caravan_kok_yielded` is set in caravan.3's immediate
   and never cleared → caravan.3 fires exactly ONCE per game even if Kokand is lost and re-taken. This is
   intended (it is a one-time settlement, and the end-state flags `kok_terms_dictated`/`kok_absorbed`
   keep the crisis chains suppressed regardless). Confirm at build; if a re-conquest should re-offer,
   clear `qing_caravan_kok_yielded` on loss of p:110 — but default is DO NOT (keeps it a one-shot).

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

**Estimate:** ~155 lines code, 6 files, ~2 days build + 1 day test. Adversarial design review DONE
(2026-08-07); CRITICAL/MEDIUM findings folded in. Remaining pre-build checks: TODO §9.3 (confirm p:110
is Kokand's seat) and, only if the mission-hook alternative is chosen, §9.4 (`trigger_event` in
`on_completion`).
