# DESIGN — #101 follow-up: pay salaries to Qing sub-positions (v2, post-review corrections)

## Goal
Task #101 gave Grand Council seats a salary (`qing_officeholder`, 0.01, chancellor +0.01).
User wants the SAME treatment for every other Qing character-appointment post: ambans,
commissioners, and diplomats. This doc covers all of them.

## Roles in scope, and their state

| Role | Employer | Existing modifier | Wage today | Vanilla rate benchmark |
|---|---|---|---|---|
| Resident Amban | subject | `qing_amban_resident` | 0.02, DONE | `office_foreign_minister` 0.02 |
| Salt Commissioner | CHI | none (new `qing_salt_commissioner_office`) | grant done, strip incomplete | `office_steward` 0.01 |
| Caravan Superintendent | CHI | none (new `qing_caravan_super_office`) | not wired | `office_steward` 0.01 |
| Hoppo (Canton customs) | CHI | none (new `qing_hoppo_office`) | not wired | `office_steward` 0.01 |
| Opium Commissioner | CHI | none (new `qing_opium_commissioner_office`) | not wired | `office_steward` 0.01 |
| Customs Inspector-General | none today, needs `move_country` | `qing_customs_inspector_general` | none | `office_steward` 0.01 |
| Zongli diplomat | CHI | none ("#90 rule") | not wired | `office_foreign_minister` 0.02 |
| Censor-inspector | CHI | none | not wired | `office_high_priest_monarchy` 0.01 |
| Imperial guardsman | CHI | none | not wired | `office_marshal` 0.01 |

Excluded (employer is the subject country, not CHI — different design, not in scope unless asked):
March Governor-General, Xinjiang Beg.

## Rates
- 0.01 for ordinary posts (steward/marshal/high-priest tier).
- 0.02 for the amban and the zongli diplomat (diplomatic rank).
- No change to `qing_officeholder`/`qing_officeholder_chancellor_bonus` (#101, already shipped).

## KEY CORRECTION (round 1 review): strip coverage must cover EVERY live un-seat path, not just
rotate + `QING_post_vacate`. Each office has 3-5 distinct places a live holder can be un-seated:
quarterly rotation, the double-book reconcile relief (a holder who became general/governor/officer
gets bumped), the player frontier-picker (manual re-pick), and the shared `QING_post_vacate_*`
family dispatcher (holder takes another post). MISSING ANY ONE leaks the salary onto a man no
longer in the post. Full site list per role below.

## Per-role wiring plan

### 1. Amban — DONE, shipped this session
`qing_amban_resident` (`common/modifiers/qing_amban_modifiers.txt`) carries
`monthly_wage_for_character = 0.02`. Paid by the subject (his real employer). No further work.

### 2. Salt Commissioner — grant done, strip needs 4 sites (only 1 covered so far)
Modifier `qing_salt_commissioner_office` (0.01) granted at `QING_salt_commissioner_seat`
(`se_QING_SALT.txt:83`, done). **Strip must be added at ALL FOUR of:**
- `QING_salt_commissioner_rotate` (`se_QING_SALT.txt:273`, alongside the existing marker strip) —
  not yet added.
- Reconcile double-book relief (`se_QING_SALT.txt:223`) — a commissioner who became
  general/governor/officer is relieved here; strips marker+holder, must also strip the modifier.
- `QING_post_vacate_salt_commissioner` (`se_QING_POST.txt:75`) — salt IS in the #118 family
  (`QING_post_stamp = { post = salt_commissioner }`, `se_QING_SALT.txt:88`), so taking another
  post routes through this vacate.
- Frontier picker salt branch (`se_QING_FRONTIER_PICKER.txt:64-78`) — a player manual re-pick
  strips the old holder's marker+holder var here; must also strip the modifier.

### 3. Caravan Superintendent — grant + 4 strip sites, none done yet
Grant: `add_character_modifier = { name = qing_caravan_super_office  duration = -1 }` at
`QING_caravan_super_seat` (`se_QING_CARAVAN.txt:905`, after the marker-set at line 911 — same
insertion shape as salt, confirmed syntactically identical by review). Strip at:
- `QING_caravan_super_rotate` (`se_QING_CARAVAN.txt:929`)
- Reconcile double-book relief (`se_QING_CARAVAN.txt:303`)
- `QING_post_vacate_caravan_super` (`se_QING_POST.txt:84-93`, currently a marker+holder-var-only
  stub — adding the strip here is additive, non-conflicting)
- Frontier picker caravan branch (`se_QING_FRONTIER_PICKER.txt:79-92`)

### 4. Hoppo — grant + 6 strip sites (more than the others — GC promotion and impeachment also
un-seat him), none done yet
Grant: at `QING_canton_seat_hoppo` (`se_QING_CANTON.txt:495`, after the marker-set at line 506).
Strip at:
- `QING_canton_rotate_hoppo` (`se_QING_CANTON.txt:521`)
- Reconcile double-book relief (`se_QING_CANTON.txt:275`)
- `QING_post_vacate_hoppo` (`se_QING_POST.txt:95-104`, currently a stub, same as caravan)
- Frontier picker hoppo branch (`se_QING_FRONTIER_PICKER.txt:93-106`)
- Grand Council promotion strip (`se_QING_COUNCIL.txt:1729-1731`) — a hoppo promoted to a GC seat
  loses the customs post here.
- Censorate impeachment (`events/imp19c_mod_events/qing_canton_events.txt:89` and `:160`)

### 5. Opium Commissioner — CORRECTED approach (round 1 found the original plan unworkable)
Opium is NOT in the #118 one-post family — `QING_opium_commissioner_seat`
(`se_QING_OPIUM.txt:404-432`) never calls `QING_post_stamp`, so there is no
`QING_post_vacate_opium` path at all. The original plan ("strip inside the seat/appoint function
before granting to the new holder") is wrong: `_seat` runs in the INCOMING holder's scope, so a
strip there hits the wrong man; and on the picker path the outgoing holder's var is already
cleared by the picker before `_seat` even runs.
**Corrected fix — strip only at the two REAL live-unseat sites:**
- `QING_opium_commissioner_reconcile` double-book relief (`se_QING_OPIUM.txt:372`, alongside its
  existing marker strip)
- Frontier picker opium branch (`se_QING_FRONTIER_PICKER.txt:113-126`)
Grant stays at `QING_opium_commissioner_seat` (`se_QING_OPIUM.txt:404`, after its marker-set), NOT
at `QING_opium_commissioner_appoint` (`OPIUM.txt:437`, a shared pick also used by reconcile
backfill — an unconditional grant there would double-grant on backfill).

### 6. Customs Inspector-General — employer question RESOLVED, strip already complete
The "no `set_employer` idiom" claim in v1 was wrong — the proven idiom is **`move_country =
<country>`**, already used for this exact purpose: `move_country = $subject$` right before
`add_character_modifier = { name = qing_amban_resident ...}` in `QING_amban_seed_one`
(`se_QING_AMBAN.txt:187`), and `move_country = ROOT` at `se_QING_AMBAN.txt:301`. `set_home_country`
(what Hart already receives via `QING_roster_finalize`, `se_QING_ROSTER.txt:46`, shared by every
roster spawn) is a DIFFERENT link — it does NOT establish `employer` (confirmed by
`se_QING_CUSTOMS.txt:109-115`'s own explicit comment that Hart has no employer tie despite going
through the roster spawn path). **Fix:** add `move_country = ROOT` at `QING_customs_appoint_ig`
(`se_QING_CUSTOMS.txt:116+`), mirroring the amban's exact idiom, then add
`monthly_wage_for_character = 0.01` to `qing_customs_inspector_general`
(`common/modifiers/qing_customs_modifiers.txt:57-61`). **Strip is ALREADY fully wired** —
`QING_customs_appoint_ig` strips the modifier on re-appointment (`se_QING_CUSTOMS.txt:126-127`)
and `QING_customs_sinicize` strips it too (`:171`) — no new strip site needed, this is the
cleanest of the nine roles on that front.
**Note (design tension, not a blocker):** this reclassifies the IG as a CHI courtier for game
purposes, which is in tension with the module's original "foreign, not a CHI courtier" framing
(`se_QING_CUSTOMS.txt:19`) — proceeding per explicit user decision, but flagging so it's a known,
deliberate tradeoff, not an oversight.

### Param-threading plan — CORRECTED (round 3 found the plan couldn't reach every enumerated strip site)
Macro-token `$post$` cannot be branched on in a runtime `limit` (round 1: macro substitution is
text, not a scope value), so a new `$wage_modifier$` parameter must be threaded through EVERY
SHARED function these 3 roles pass through, not just the grant path. Round 3 found the original
plan only threaded the grant path (`QING_subpost_fill_one_minted` +
`QING_subpost_staff_corps_minted` + their 6 caller lines) and MISSED that
**`QING_subpost_strip_double_booked` (`se_QING_SUBPOSTS.txt:150-183`) and its 3 callers
(`:243/244/245`) also need `$wage_modifier$` threaded through them** — this function is one of the
enumerated strip sites (`:176-177`) below, and for censor-inspector/imperial-guardsman (whose
ministry-recompute functions do NOT self-heal double-booking, confirmed round 3) this is their
PRIMARY quarterly strip, not a backup. Without threading it, `:176` cannot reference the
per-role modifier name and the wage leaks on every double-book for those two roles, and even for
zongli in the headless-ministry case (no director seated to run the recompute pulse).
**Corrected plan (round 4 fix — the "9 caller lines" count was itself wrong): thread
`$wage_modifier$` through all THREE functions AND ALL 15 invocation lines:**
- `QING_subpost_fill_one_minted`'s OWN 6 internal calls (`se_QING_SUBPOSTS.txt:133-138`) — the
  wage grant lives inside this function's `scope:qing_subpost_new = {}` block, the only scope
  where the minted man exists, so `wage_modifier` must be forwarded here exactly like `degree`
  and `post` already are. Round 4 found round 3's plan omitted these 6 lines entirely — if an
  implementer follows "9 caller lines" literally, `$wage_modifier$` is left unsubstituted at mint
  time, producing an invalid modifier name (the same macro-arg-substitution failure class as
  commit `a9172944`/#108).
- `QING_subpost_staff_corps_minted`'s 6 callers (`se_QING_SUBPOSTS.txt:212,213,214,256,268,279`).
- `QING_subpost_strip_double_booked`'s 3 callers (`se_QING_SUBPOSTS.txt:243,244,245`).
No name collision with the function's existing `$marker$`/`$count$`/`$post$`/`$degree$` params
(confirmed round 4).

### Grant coverage — CORRECTED (round 3 found the grant only reaches minted characters)
The plan as written granted the wage only inside `QING_subpost_fill_one_minted` — the freshly-
created-character path. Round 3 found each role ALSO has live PLAYER-APPOINT paths that assign an
EXISTING courtier to the post, which never touch that function and so would be seated unpaid:
- Row-click picker (`common/scripted_guis/QING_governance_actions.txt:705-706` censor,
  `:714-715` guard, `:723-724` zongli — confirmed live corps-enrolment UI, comment at `:700-702`).
- Dedicated panel appoint verbs (`QING_zongli_panel.txt:106`, `QING_censorate_panel.txt:98`,
  `QING_guard_panel.txt:99`).
**Fix: add the role-specific `add_character_modifier` (hardcoded per-role name — these are
role-specific blocks, not shared, so no `$wage_modifier$` parameter needed here) at all 6 of these
sites**, so every path that seats a diplomat/censor/guardsman — minted or player-picked — pays him.

### 7. Zongli diplomat — new modifier `qing_zongli_diplomat_office` (0.02)
**Grant sites — 3** (round 3 correction): `QING_subpost_fill_one_minted` (minted path, param-
threaded) + `QING_governance_actions.txt:723-724` (picker) + `QING_zongli_panel.txt:106` (panel
appoint) — the latter two hardcode `qing_zongli_diplomat_office` directly.
**Strip sites — 5** (round 1 found 3, round 2 found 2 more, round 3 confirmed all 5 correct and
found the threading gap, now fixed above):
- `QING_post_vacate_zongli_diplomat` (`se_QING_POST.txt:132`, hardcoded)
- `QING_subpost_staff_corps_minted`'s own recount strip (`se_QING_SUBPOSTS.txt:112-113`, param-threaded)
- `QING_subpost_strip_double_booked` (`se_QING_SUBPOSTS.txt:176-177`, param-threaded — NOW correctly reachable)
- **Player-facing Recall lever**: `qing_zongli_recall_diplomat` (`QING_zongli_panel.txt:128`, hardcoded)
- **Roster-recompute double-book strip**: `QING_ministry_recompute_perf_zongli`
  (`se_QING_MINISTRY.txt:544`, hardcoded) — confirmed round 3: this runs on EVERY ministry pulse
  AND every panel open (`:522-524`), and reaches `qing_current_post` release BEFORE the quarterly
  sweep can — this is the EFFECTIVE PRIMARY strip site for zongli, not a backup.
- **Censorate impeachment (round 5 fix — see below)**: `QING_censorate_impeach_uphold`
  (`se_QING_CENSORATE.txt:256`).

### 8. Censor-inspector — new modifier `qing_censor_inspector_office` (0.01)
**Grant sites — 3:** `QING_subpost_fill_one_minted` (param-threaded) +
`QING_governance_actions.txt:705-706` (picker) + `QING_censorate_panel.txt:98` (panel appoint),
latter two hardcoded.
**Strip sites — 5:** `QING_post_vacate_censor_inspector` (`se_QING_POST.txt:128`, hardcoded) +
`SUBPOSTS.txt:112-113` (param-threaded) + `SUBPOSTS.txt:176-177` (param-threaded — confirmed
round 3 this is censor-inspector's PRIMARY quarterly strip, since
`QING_ministry_recompute_perf_censor` does NOT self-heal, exclude-only) PLUS:
- **Player-facing Recall lever**: `qing_censorate_recall_inspector`
  (`QING_censorate_panel.txt:120`, hardcoded).
- **Impeach-uphold disgrace strip**: `QING_censorate_impeach_uphold`
  (`se_QING_CENSORATE.txt:256`, on `scope:qing_censorate_target`, hardcoded).

### 9. Imperial guardsman — new modifier `qing_imperial_guardsman_office` (0.01)
**Grant sites — 3:** `QING_subpost_fill_one_minted` (param-threaded) +
`QING_governance_actions.txt:714-715` (picker) + `QING_guard_panel.txt:99` (panel appoint),
latter two hardcoded.
**Strip sites — 5** (round 5 found a 5th):** `QING_post_vacate_imperial_guardsman`
(`se_QING_POST.txt:136`, hardcoded) + `SUBPOSTS.txt:112-113` (param-threaded) +
`SUBPOSTS.txt:176-177` (param-threaded — confirmed round 3 this is imperial-guardsman's PRIMARY
quarterly strip, same reasoning as censor-inspector) PLUS:
- **Player-facing Discharge lever**: `qing_guard_discharge_guardsman`
  (`QING_guard_panel.txt:121`, hardcoded).
- **Censorate impeachment (round 5 fix — see below)**: `QING_censorate_impeach_uphold`
  (`se_QING_CENSORATE.txt:256`).

## ROUND 5 FIX — Censorate impeachment can un-seat a zongli diplomat or imperial guardsman with
no strip site to catch it (real gap, same class round 1 already fixed for Hoppo)
`QING_censorate_find_corrupt` (`se_QING_CENSORATE.txt:98-124`, the eligibility pool for the
Censorate's generic "impeach the venal" picker) has no exclusion for corps members — any
`employer = ROOT`, adult, living, non-rebel courtier is eligible, including a seated zongli
diplomat or imperial guardsman. `QING_censorate_impeach_uphold` (`:225-283`) already strips
`qing_is_censor_inspector` (`:256`, a prior #362 fix — role 8 is already covered) but has no
equivalent line for `qing_zongli_diplomat` or `qing_is_imperial_guardsman` — so an impeached
zongli/guardsman keeps his corps marker, his `qing_current_post`, and (once this task ships) his
wage forever. Contrast with Hoppo (role 4): its Censorate-impeachment exposure was already found
and fixed with a bespoke pre-strip in `qing_canton_events.txt:89`/`:160` — zongli/guardsman have
no equivalent anywhere.
**WIDENED FIX (per direct user direction — "should remove all titles, be it commissioner or
governor or commander or Captain of the Guard or whatever"), superseding the narrower two-line
patch first drafted here.** The hardcoded single-marker strip at `:256` was itself a symptom of a
BIGGER, pre-existing pattern: this codebase already has a GENERIC dispatcher for the entire subpost
family — `QING_post_dispatch_vacate` (`se_QING_POST.txt:51-64`), keyed on `var:qing_current_post`,
covering all 11 families in one call (gc_office, salt_commissioner, caravan_super, hoppo,
southernstudy, upperstudy, censor_inspector, zongli_diplomat, imperial_guardsman, palace_eunuch,
harem_consort) — plus two more proven, already-used-elsewhere strip verbs this effect never calls:
`remove_command` (military command, guarded `is_general`/`is_admiral`, precedent:
`events/annexation.txt:546`, `qing_war_events.txt:151`) and `remove_as_governor` (guarded
`is_governor`, precedent: `office_eligibility_events.txt:186`). `se_QING_JUSTICE.txt:322-339`
(`QING_justice_strip_for_trial`) already composes GC-office + command + governor as ITS OWN
"strip everything for trial" idiom — but has the COMPLEMENTARY gap: it never calls
`QING_post_dispatch_vacate` either, so a docketed subpost-holder keeps his post through the whole
trial. Neither of the codebase's two general-disgrace pathways is actually complete on its own.
**Fix — `se_QING_CENSORATE.txt:245-256`, widen `QING_censorate_impeach_uphold`'s existing strip
block (already has GC-office + vanilla-office) with the two missing proven verbs, and swap the
single hardcoded censor-inspector line for the full dispatcher (a strict superset, not a
narrowing — the dispatcher already handles censor-inspector as one of its ten branches):**
```
if = { limit = { has_variable = qing_office_held }  QING_office_vacate_dispatch = yes }   # unchanged, existing :245
if = { limit = { OR = { is_general = yes  is_admiral = yes } }  remove_command = yes }    # NEW
if = { limit = { is_governor = yes }  remove_as_governor = yes }                          # NEW
if = { limit = { has_any_office = yes }  remove_all_offices = yes }                       # unchanged, existing :252
if = { limit = { has_variable = qing_current_post }  QING_post_dispatch_vacate = yes }    # REPLACES the old
                                                                                            # qing_is_censor_inspector-
                                                                                            # only line at :256
```
**Second, additive-only fix — `se_QING_JUSTICE.txt:334` (`QING_justice_strip_for_trial`), close
the complementary gap so BOTH disgrace pathways reach full parity:**
```
if = { limit = { has_variable = qing_current_post }  QING_post_dispatch_vacate = yes }    # NEW line,
                                                                                            # added alongside the
                                                                                            # existing command/
                                                                                            # governor/GC-office
                                                                                            # lines, nothing removed
```
This second edit is a pure addition to fork-owned code (no existing line touched) — proposed here
because it is the SAME class of gap the user's principle names, in the sibling system, discovered
in the course of widening the Censorate fix. Tracked separately as its own task so the subpost-
salary design's own scope stays clear; not required to unblock task #101/#5, but left undone would
be knowingly leaving the identical bug live one file over.
No new mechanism invented anywhere in this fix — every verb used (`QING_post_dispatch_vacate`,
`remove_command`, `remove_as_governor`) is already defined and already used elsewhere in this
exact way; this only widens WHERE they're called from.

**[Round 7 findings, both confirmed non-blocking]**
1. **Amban / March Governor-General / Xinjiang Beg are formally unreachable by all 5 strip
   mechanisms** (`se_QING_POST.txt:15-20` deliberately excludes them from the 11 `qing_current_post`
   families; not `is_general`/`is_admiral`/`is_governor` either, since they're employed by a
   SUBJECT country, not CHI). Currently inert, not a live bug: both disgrace pickers
   (`QING_censorate_find_corrupt`/`_refresh_venal`, `QING_justice_refresh_accusable`) gate their
   pool on `employer = ROOT`, so these 3 roles can never enter either picker's target pool today.
   Noted for the record; no fix needed unless that employer-gate ever changes.
2. **Bonus fix, not a bug**: for a GC-office holder, the pre-existing `QING_office_vacate_dispatch`
   line clears `qing_office_held` but never `qing_current_post` — so a GC officer impeached or
   docketed for trial has ALWAYS kept a stale `qing_current_post = gc_office` afterward, until now.
   The new `QING_post_dispatch_vacate` line's trailing `QING_post_release` (`se_QING_POST.txt:63`)
   clears it too, at both edit sites (Censorate + Justice) — closing a second, previously-unnoticed
   staleness gap for free, not just the 3 subpost roles this task set out to fix.

**[Round 6 cross-check — resolved by this widening, not by the narrower patch round 6 reviewed]**
Round 6 reviewed the EARLIER, narrower two-line patch (bare `remove_variable` on the zongli/
guardsman markers) and found it did NOT clear `qing_current_post` — so the corps-establishment
scan in `QING_subpost_staff_corps_minted`/`_strip_double_booked` (keyed on `var:qing_current_post
= flag:zongli_diplomat`, per `#118`) would still count an impeached zongli diplomat as seated. That
finding is CORRECT against the patch it reviewed, but does not apply to this WIDENED fix: calling
`QING_post_dispatch_vacate` (rather than a bare `remove_variable`) reaches `QING_post_release`
(`se_QING_POST.txt:41-46`) at the end of its if-chain (`:63`), which unconditionally clears
`qing_current_post` whenever it is set — the exact clearing round 6 found missing. This resolves
round 6's HIGH and MEDIUM findings for all three roles uniformly (censor-inspector/zongli/
guardsman alike), not just the ministry-recompute half round 6 found already-safe. Round 7 is
reviewing this exact (already-widened) text; treat round 7's verdict as authoritative over round
6's for this specific point, since round 6 was reviewing superseded text.

**Not a missing site (round 2 checked, confirmed redundant-but-harmless):**
`se_QING_COUNCIL.txt:1695-1697` strips all three subpost markers on GC promotion — but this runs
AFTER `QING_post_stamp = { post = gc_office }` (`:1687`), which already routes through
`QING_post_dispatch_vacate` → the family vacate sites already listed above. No new strip needed
there; noted so a future pass doesn't "fix" a non-gap.

## Resolved questions (from round 1 review)
1. Salt gap confirmed real — now fully enumerated (4 sites, not 1).
2. Employer idiom found: `move_country = <country>`, proven precedent at `se_QING_AMBAN.txt:187`.
3. Param-threading confirmed the only workable shape (macro tokens aren't branchable at runtime).
4. Double-grant risk: LOW. The frontier picker already strips the old holder before seating the
   new one, and backfill/appoint paths only draw men who don't already hold a post
   (`NOT = { QING_char_holds_court_position = yes }`). The real risk is the OPPOSITE — a stale,
   never-stripped modifier from a missed site (which is why every site above is now enumerated).
5. Blast radius CONFIRMED SAFE — `common/ai_budget/00_default.txt` does not read
   `monthly_wage_for_character` or character wealth; no budget projection assumes these posts are
   unpaid. The wage key is already used by 40+ vanilla offices plus this mod's amban/GC seats,
   consumed uniformly by the engine's own wage channel.

## Remaining open item for round 2 review
Confirm the full corrected site list above is itself complete — round 1 found round 0 (the
original doc) missed 10+ sites across 5 roles; round 2 should specifically hunt for any FOURTH or
FIFTH un-seat path per role that this pass still missed (e.g. death-of-holder handling, succession/
usurpation edge cases, any other event file besides `qing_canton_events.txt` that touches these
posts).
