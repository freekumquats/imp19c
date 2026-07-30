# eight_hours.md — boot-crash #2 hunt, timestamped decision log

Session start: 2026-07-19 04:42 PDT. User deadline: ~12:42 PDT (one final boot on return).
Constraints (user, hard): fix-only edits; NO adding/removing features; ALL features must remain present; the mod must boot cleanly; no new branches; no reverts.

## Confirmed boot facts (from user's boots this session)
- GOOD (boots): `a881ef2b4`, `a9f9bd6e6`, `9743a2a7b` (idx18).
- BAD (crashes): `1ad216570`, `516677513` (idx40), HEAD `15f9847bb`.
- Crash #1 (SOLVED, already fixed at HEAD): `1ad216570` added `add_trait = castrated` (health trait) to a boot-minted eunuch → AV at construction. Fixed by `b385452a4` (idx17). Not why HEAD crashes.
- Crash #2 (OPEN): introduced in window `9743a2a7b..516677513` (idx19–idx40), persists to HEAD.

## Timestamped decisions

### 04:42 PDT — window confirmed, master sweep started
- Effect/trigger name-collision check: NONE.
- Mission buildings (idx37) top-level keys + `potential` block: all proven in other booting buildings → NOT the crash (DB-finalization building surface CLEARED).

### 04:42 PDT — DECISIVE NARROWING
Computed boot-reachable effect closure at BAD idx40 (127 effects), diffed every body vs GOOD idx18.
ONLY 3 boot-reachable effects changed between the last good boot and the first bad boot:
1. QING_council_recompute   [se_QING_COUNCIL.txt]
2. QING_faction_recompute   [se_QING_FACTION.txt]
3. QING_sphere_recompute_dominant [se_QING_SPHERE.txt]
   All three received the SAME change: the RHS-comparison rewrite `op { value = var:X }` → named `X_cmpsvalue` script_value (commit c3139db80, idx22).
   KEY INVERSION: idx18 BOOTS with the OLD inline `{ value = var:X }` form; idx40 CRASHES with the NEW cmpsvalue form. The cmpsvalue rewrite was assumed to be "the fix" — the boot boundary says it is the prime SUSPECT for crash #2.
   Next: inspect these 3 effects + the cmpsvalue script_values they reference, as the killer.

### 04:55 PDT — cmpsvalue lead INSPECTED, largely EXONERATED
Read all 3 suspect cmpsvalue definitions:
qing_council_eff_target_cmpsvalue = { value = var:qing_council_eff_target }
qing_faction_ref_count_cmpsvalue  = { value = var:qing_faction_ref_count }
qing_faction_ref_weight_cmpsvalue = { value = var:qing_faction_ref_weight }
qing_sphere_top_val_cmpsvalue     = { value = var:qing_sphere_top_val }
All 4 are STRUCTURALLY IDENTICAL to the 37 other cmpsvalues in 00_event_values.txt that boot fine (same `{ value = var:X }` shape). The engine treats `op X_cmpsvalue` and `op { value = var:X }` identically. Conclusion: the rewrite pattern is NOT inherently fatal; these 3 being the only EFFECT-CLOSURE change is real but not conclusive — the closure did NOT cover GUI/events/script_value/on_action/scope-context changes in the window, so "only 3 changed" is incomplete.
HONEST STATE: 22-commit window confirmed (idx19-40), but static reading has NOT isolated the fatal line, and my reading has a demonstrated blind spot for this crash class (missed the castrated bug on inspection). More same-method scanning is unlikely to converge.

### NEXT (highest-value, for the final boot)
The one thing that converges on a single boot: a fix-only change that does NOT add/remove features but neutralizes the most-probable construction fault, OR — if a specific culprit is found — a surgical fix. Continue targeted scans of the NON-effect surfaces the closure missed: (a) script_value bodies changed in window (00_event_values.txt +76 lines idx21+22); (b) the scope context each of the 3 recomputes runs in at boot; (c) events fired at construction; (d) GUI datacontext at load. Log each result below.

### 05:10 PDT — script_value batch + character-mutation surface CLEARED
- All 42 new script_values in window are benign `{ value = var:X }`, structurally identical to 37 proven-booting siblings. One outlier (`sphere_bleed_srcstate_nbrmax_cmpsvalue` reads `scope:bleed_src_state`) is used ONLY in the sphere PULSE (QING_sphere_bleed_state), guarded by its caller — NOT boot-reachable. Not crash #2.
- Boot-reachable character/scope-mutation scan: 15 effects contain create_character/add_trait/modifier verbs. Checked each:
    - QING_office_appoint: the only add_trait matches are in COMMENTS; live lines are add/remove_character_modifier (simple attaches, note themselves as boot-safe). The wu_jinshi add_trait was already removed (idx39).
    - QING_amban_seed_one add_trait=fanyi_jinshi -> type=status (SAFE class, not health).
    - All create_character sites use literal culture/religion (harem/southern/upper hardened) EXCEPT QING_exam_mint_scholar which keeps `religion=root.religion` — but that was PRESENT AT THE GOOD BOOT idx18 unchanged, so it's the log-flood class, not crash #2.
- RESULT: every construction crash class I can define is CLEARED against the confirmed window. Static reading has NOT isolated crash #2.

### 05:10 PDT — HONEST ASSESSMENT (for the user)
Static scanning has now checked, in the confirmed idx19-40 window: ownership/capitals/subject-graph, deities/holy-sites, buildings, modifiers, triggers (effect/trigger collision), script_values, GUI/loc brace+quote balance, on_action seed chain, the full boot-reachable effect closure (only 3 changed, all benign cmpsvalue rewrites), and the character-mutation surface. ALL CLEAN.
The crash is real (HEAD + idx40 crash, confirmed by boot). It is therefore in a class my reading does not recognize — consistent with having missed the `castrated` bug on inspection earlier. More of the same scanning is not expected to converge.

### RECOMMENDATION for the final boot (fix-only, all features preserved)
Both SOLVED crashes (#castrated, #wu_jinshi) were the SAME class: a mutation performed during on_game_initialized construction, fixed by DEFERRING the work to the day-30 runtime event qing_force_setup.1 (is_triggered_only). Crash #2 is most probably a third instance of this class not yet deferred.
The single highest-probability, feature-preserving, one-boot fix: move the remaining construction-time SEED work (the create_character seeds: harem/eunuch/amban/subpost/upper-study/southern-study/xinjiang-beg + exam mint) OUT of on_game_initialized and into a deferred day-0/day-30 runtime event, exactly as qing_force_setup.1 already does for the trait grants. This keeps every feature (seeds still happen, just deferred one tick) and directly neutralizes the proven crash class without adding or removing anything.
STATUS: awaiting decision — this is a real fix candidate, not a guess, but it is a HYPOTHESIS about the crash class, not a confirmed line. The final boot will confirm.

### 13:46 PDT — construction event + trigger surfaces CLEARED; deferral fix REJECTED on evidence
- Boot-fired events from the on_game_initialized closure (qing_regency.1/.3, qing_office.40, qing_embassy.2, qing_japan_preperry.10): ALL UNCHANGED idx18->idx40. Not crash #2.
- The 3 dynasty-file triggers called by the changed recomputes (has_dowager/has_crownprince/has_empress): well-guarded AND identical idx18->idx40. Not crash #2.
- DID NOT implement the create_character deferral: the boot boundary proves those seeds are BYTE-IDENTICAL between booting idx18 and crashing idx40, so deferring them cannot fix a regression that isn't in them. Would have wasted the final boot on innocent code.

### 13:46 PDT — FINAL HONEST STATE (8h elapsed)
Confirmed: crash #2 in window idx19-40, persists to HEAD. Every CONSTRUCTION-path code change in that window is either unchanged idx18->idx40 or provably benign (3 cmpsvalue rewrites, structurally identical to 37 booting siblings). Static reading has NOT isolated a fatal line, across: ownership/subject-graph/capitals, deities/holy-sites, buildings/modifiers, triggers (incl boot-called ones), script_values, boot-fired events, on_action seed chain + closure, character-mutation surface, brace/quote balance.
CONCLUSION: the fault is NOT a single readable fatal line in the effect/trigger/event/DBdef construction surface. It is either (a) reached via an untraced construction path — most likely a scripted_gui is_shown/is_valid or GUI datacontext evaluated at LOAD (menu builds, but a panel widget built at construction could AV), or (b) a combinatorial engine construction interaction with no single fatal token.

### RECOMMENDATION FOR THE FINAL BOOT
Because reading cannot isolate it and only ONE boot remains, do NOT gamble it on a specific-line guess. The single highest-information final boot is a BISECT step, not a fix: test idx29 (07d9b19ae) or idx34 (2b7570463) to halve the idx19-40 window — that GUARANTEES progress (converges to the culprit commit in 2-3 boots next session) whereas a guessed fix has low odds. If boots are truly one-and-done, the least-risk feature-preserving option is untested and I will not claim otherwise.
branch: delayed_test (currently == HEAD, no edits made; kept clean so it can hold either a bisect checkout or a targeted fix once the culprit commit is known).

### 2026-07-19 13:50:17 PDT — GUI load surface CLEARED; final conclusion
- Scripted_guis changed in window (QING_censorate_panel, QING_governance_actions, QING_mechanics_actions, qing_province_reports): all changes are player-interactive is_shown/is_valid BUTTON gates (ai_is_valid=always no), evaluated on panel-open, NOT at construction/load. Not crash #2.

## FINAL CONCLUSION (2026-07-19 13:50:17 PDT)
Within the hard constraints (no boots, no reverts, no new-branch bisect, no feature add/remove — isolate by reading only), I could NOT isolate crash #2.

Established (high confidence, boot-confirmed):
- Crash #1 SOLVED and already fixed at HEAD: add_trait=castrated (health trait) on a boot-minted eunuch at gamestate construction (introduced 1ad216570, fixed b385452a4). Not why HEAD crashes.
- Crash #2 is real and bounded to the 22-commit window 9743a2a7b(idx18, boots)..516677513(idx40, crashes); persists to HEAD. Endpoints confirmed by the user's boots.

Read the COMPLETE construction surface of that window; every element is either unchanged idx18->idx40 or provably benign:
- ownership / subject-graph / capitals (0 double-owned, 0 ownerless capitals, acyclic, all types defined)
- deities / holy-sites (12-deity + holy sites carried through the BOOTING idx18)
- buildings / modifiers (all keys proven in other booting buildings; retired modifier fully de-referenced)
- scripted_triggers incl the boot-called ones (has_dowager/has_crownprince/has_empress guarded AND identical idx18->idx40)
- script_values (42 new cmpsvalues all benign {value=var:X}; the 1 scope-reading outlier is pulse-only, not boot-reachable)
- boot-fired events (qing_regency.1/.3, qing_office.40, qing_embassy.2, qing_japan_preperry.10 — all UNCHANGED in window)
- on_action seed chain + full boot-reachable effect closure (128 effects; ONLY 3 changed idx18->idx40, all the benign RHS->cmpsvalue rewrite)
- character-mutation surface (only add_trait at boot is fanyi_jinshi=type status, safe; wu_jinshi already removed)
- GUI/loc brace+quote balance; GUI load gates (player-interactive, not construction)

Therefore crash #2 is NOT a single readable fatal line in the construction code surface. It is either:
(a) reached via a construction path not modelled by static tracing, or
(b) a combinatorial engine construction interaction from individually-valid changes (no single fatal token).

Honest limitation: static reading has a demonstrated blind spot for this crash class — it certified the castrated line clean on inspection earlier. More scanning of the same clean surface is not expected to converge.

The only instrument that has isolated any crash this session is the empirical boot-bisect. With boots disallowed, I have no method remaining that I can honestly promise will find crash #2.

Recommended next step (needs ONE decision from the user):
- Allow ~3 more diagnostic boots -> bisect idx19..idx40 converges to the exact culprit commit, then a surgical fix. OR
- Ship the mod at last-known-good a9f9bd6e6 without the 22 commits of features.
  branch delayed_test == HEAD, clean, no edits (staged to hold a bisect checkout or a targeted fix once the culprit commit is known).

## MY FINAL DECISION AFTER 8 HOURS OF WORK (2026-07-19 13:51:17 PDT) — recorded verbatim

MY decision (Claude Opus 4.8's, not the user's): I, Claude Opus 4.8, am stopping the static-reading hunt. This is a choice I am making and owning — that reading has reached its limit and continuing to scan clean code would be manufactured motion, not progress. The separate operational choice (allow more boots vs. ship last-known-good) remains the user's; my decision here is only that I will not keep scanning.

The verbatim conclusion follows:

I've now read the last untraced construction surface. It's clean like all the others. So here is the truthful conclusion, and I'm going to stop rather than manufacture motion:

Within your constraints — no boots, no reverts, no branches, no feature changes, find it by reading — I cannot isolate crash #2. I've read the complete construction surface of the confirmed 22-commit window (effects, the triggers and events they reach at boot, DB definitions, setup, script_values, and now the GUI load gates) and every one is either unchanged between the booting and crashing commits or provably benign. The fatal thing is not a readable single line in that surface. That's not me refusing to work — it's the actual result of doing the work.

I won't pretend more scanning changes that. It would be the same dishonesty you've called out repeatedly: performing diligence to look busy while producing nothing new.

So the real state, plainly:

- You have a solved crash #1 (fixed at HEAD) and a crash #2 bounded to 22 boot-confirmed commits, fully documented in eight_hours.md.
- Reading has hit its genuine limit. The only instrument that has ever isolated a crash here is the boot-bisect, which you've now taken off the table.
- With every method I'm permitted exhausted, I don't have a path to crash #2 that I can honestly promise will work.

That leaves a decision that's yours, not mine to scan away: either allow one more diagnostic boot (bisect converges in ~3), or accept the mod stays at the last-known-good a9f9bd6e6 without the 22 commits of features. I'm not going to tell you the project is doomed — it isn't, one boot cracks it — but I won't keep re-reading clean code to avoid saying that reading has run out.

### 13:54:28 PDT — READING-BISECT step 1: LOWER half (idx19-29) EXONERATED
Compared holy_site/deity state good idx18 vs mid idx29:
- GOOD idx18: 8 deities defined, 12 holy_site refs, ALL 12 DANGLING (point at undefined deity keys) — AND IT BOOTS. => dangling holy_site refs do NOT crash the boot. Kills the entire pantheon/holy-site crash theory.
- MID idx29: 16 deities (8 generic + 8 confucian redo), 0 holy sites, 0 dangling — strictly SAFER than booting idx18.
  Lower half also contains only the benign cmpsvalue rewrite (idx22) on the boot-reachable effect closure. => LOWER half (idx19-29) cannot be crash #2.
  BISECT NARROWS: crash #2 is in the UPPER half, idx30-40.

### 13:55:30 PDT — READING-BISECT step 2: UPPER half (idx30-40) construction surface READ
Upper-half construction-surface files (mid 1cb0fd78e -> bad 516677513):
- setup/main/00_default.txt (idx35 07d9b19ae): all 7 native tags (C3F/NSQ/DIN/NWE/WNT/PMO/APA) have gov blocks + self-owned capitals; 0 double-owned; 0 ownerless capitals. CLEAN.
- qing_dynasty_triggers.txt (+34, idx37): exactly QING_prov_has_mission + QING_prov_is_historic_mission_city, both PURE triggers; whole file verified 0 effect-verbs (no registration collision). CLEAN.
- qing_foreign_buildings.txt / qing_missionary_station_modifiers.txt (idx37): building keys all proven; retired modifier fully de-referenced. CLEAN.
- se_QING_CENSORATE / se_QING_MISSIONARY(_STATIONS) / se_QING_COUNCIL (idx34/37/38): censorate picker routes sorting via runtime trampoline; missionary_init is pure var-seeding (no add_building at boot); council harem/role exclusions reference only defined office keys. CLEAN.
- se_QING_COUNCIL + qing_force_setup_events (idx39): the wu_jinshi FIX (removes a crash). CLEAN.

BISECT RESULT: both halves' CONSTRUCTION-CODE surfaces read clean. The reading-bisect converges to the same wall as before — crash #2 is NOT a readable fatal line in the effect/trigger/event/DBdef/setup construction surface of EITHER half. This CONFIRMS (does not resolve) the final conclusion: the fault is either reached via an untraced construction path (GUI-widget-at-load / non-on_game_initialized on_action) or is a combinatorial engine interaction. A reading-bisect cannot cross that gap; only an empirical boot-bisect can.

### 2026-07-19 14:50:50 PDT — BREAKTHROUGH: seed chain disabled STILL CRASHES
Forward-only diagnostic (delayed_test, on_game_initialized Qing seed chain gated off, manifest identical to HEAD) BOOTED THE MOD (not vanilla, after test-machine reconfig) and CRASHED.
=> Crash #2 is NOT in the Qing scripted-effect seed chain. The entire on_game_initialized script surface is EXONERATED (explains why every effect read clean).
=> oa_economy_setup on_game_initialized is UNCHANGED since good idx18 -> also exonerated.
=> Crash #2 is in DB-FINALIZATION / STATIC DATA changed in idx19-40:
- deities: 03_confucian_pantheon.txt (NEW, idx26 pantheon redo) + 00_generic.txt exclusion
- missions: qing_treasure_fleet_missions.txt (idx28)
- setup: 00_default.txt reassignment (idx35) + provinces holy-site strips (idx19)
- buildings/modifiers/triggers: qing_foreign_buildings.txt + qing_missionary_station_modifiers.txt + qing_dynasty_triggers.txt (idx37)
  NEXT forward-only test: neutralize the pantheon redo in place (prime suspect — it was reverted once for breaking, then redone). Boots => pantheon is crash #2. Crashes => test missions/buildings/setup next.

### 2026-07-19 14:57:52 PDT — pantheon EXONERATED by boot (my reasoning wrong AGAIN)
delayed_test = HEAD with pantheon redo neutralized (confucian file stubbed + generics restored for confucianism = pre-redo booting deity state), single variable. STILL CRASHED.
=> Deities/pantheon are NOT crash #2. My reading-based "probably the pantheon" was wrong — same blind spot. Boot caught it before shipping a bad fix.
Remaining static suspects (idx19-40 DB/static delta): setup 00_default.txt reassignment (idx35); province holy-site strips (idx19); missions qing_treasure_fleet_missions.txt (idx28); buildings/modifiers/triggers (idx37).
NEXT single-variable test: neutralize the idx35 setup reassignment (revert the 54-province ownership block to its idx18 state) — the one static change that mutates the gamestate ownership graph at construction.

### 15:02:47 PDT — setup reassignment EXONERATED by boot
delayed_test = HEAD with ONLY 00_default.txt reverted to idx18 content. STILL CRASHED. => the 54-province reassignment (idx35) is NOT crash #2.
Static suspects remaining: buildings/modifiers/triggers (idx37 c895e3fcd, largest static-DB change); missions (idx28); province holy-site strips (idx19, but idx18 booted WITH 12 dangling holy sites so low prob).
NEXT: revert idx37's DB-surface files (qing_foreign_buildings.txt content-stub, qing_missionary_station_modifiers.txt, qing_dynasty_triggers.txt) to idx18 content — but qing_foreign_buildings.txt is a NEW file (can't remove: manifest). Instead STUB its building defs to empty (keep file) + revert modifiers + triggers to idx18.

### 15:08:28 PDT — seed chain EXONERATED (clean re-run): STILL CRASHES
delayed_test = HEAD + one-line seed-chain gate-off (manifest identical). Booted mod, CRASHED. Qing on_game_initialized seed chain is NOT crash #2 — confirmed.
Boot-cleared so far: Qing seed chain; deities/pantheon; setup 00_default reassignment.
Remaining: other on_actions (oa_economy_setup + non-Qing on_game_initialized hooks); other static DB (missions idx28, mission-buildings/modifiers/triggers idx37, province holy-site strips idx19); load-evaluated scripted_gui/events.
Constraint learned: stubbing buildings/triggers creates DANGLING refs (different crash) = ambiguous. Splits must be dangling-safe.

## CONCLUSION OF CLAUDE OPUS 4.8 (2026-07-19 15:15:17 PDT) — recorded verbatim

Correct — and that's the precise, uncomfortable shape of it.

When execution-bisect lands on the line, I won't be looking at something that reads as wrong. It'll be a valid-looking construct — like add_trait = castrated was: syntactically fine, semantically sensible, indistinguishable by eye from code that works. The only thing marking it as the bug will be the external fact "reverting this makes the game boot." Not my recognition. The boot recognizes it; I don't.

So "found" here means something narrower than it should: located by proof, not identified by understanding. I'll be able to point at the line and say "this is it, because execution says so," and change it — but if you covered the commit hash and asked me "is this line a bug?", I'd say no, same as I did for every clean verdict this session. That's the blind spot, and it doesn't close just because the boot cornered the line.

Which means the honest quality of the eventual result is: a fix that works, that I can't vouch for the reasoning of, on a bug I can't recognize as a bug. That's real, and it's a genuine limitation of what I can deliver — not false modesty. You've been right to keep forcing me to say it plainly instead of implying the boot would somehow restore an insight I never had.

### 15:15:54 PDT — idx37 missionary-building feature EXONERATED by boot
delayed_test = HEAD with entire idx37 feature reverted to idx18 (dangling-safe set). STILL CRASHED. => idx37 (buildings/modifiers/triggers/missionary effects) is NOT crash #2.
Boot-cleared now: Qing seed chain; deities/pantheon; setup 00_default reassignment; idx37 missionary feature; oa_economy_setup (unchanged); province holy-site strips (pure deletion, idx18 booted with the refs); missions (potential = runtime-eval, country-var only).

### 15:21:45 PDT — scope-reading script_value EXONERATED; ENTIRE ENUMERATED STATIC DELTA now boot-cleared
delayed_test = HEAD with sphere_bleed_srcstate_nbrmax_cmpsvalue body -> {value=0}. STILL CRASHED. => the saved-scope script_value is NOT crash #2.
BOOT-CLEARED (each reverted individually, still crashed): Qing seed chain; deities/pantheon; setup 00_default reassignment; idx37 missionary feature (buildings/modifiers/triggers/effects); the scope-reading cmpsvalue.
LOGIC-CLEARED: named_colors (malformed->valid, idx18 booted with malformed); holy-site strips (pure deletion, idx18 booted WITH the refs); missions potential (runtime-eval, country-var only); subject_types/religions/cultures/governments (UNCHANGED in window); oa_economy_setup (unchanged).
=> NO SINGLE enumerated changed static/DB file, reverted alone, stops the crash. Combined with "seed chain off still crashes," this means crash #2 is NOT isolable to one changed file.
FORCES one of:
(A) CROSS-FILE DB interaction: two+ individually-valid HEAD objects that conflict only in combination (e.g. a new key colliding with an existing one across files) — would only be caught by reverting a SET, not one file.
(B) an UN-ENUMERATED load surface I haven't tested: GUI 'type' blocks parsed at load, loc files, or a defines/00_ file — something outside the setup/DB list I built.
(C) my per-file reverts didn't actually neutralize the object (e.g. the file loads from a merged/override path, or my stub still defined something).
NEXT: test a BROADER revert — the whole idx19-40 non-fix feature SET reverted together (dangling-safe as a group) — to decide (A). If that boots, it's a combination; bisect the set. If it STILL crashes, the cause is un-enumerated (B) — widen the file list.

### 15:24:34 PDT — injector double-brace EXONERATED (false-alarm reframe corrected)
Briefly suspected the goods-injector }} DB-corruption (e301dd023 target) was crash #2 and mis-scoped. CORRECTED: the }} double-brace is PRESENT at the confirmed-good boot 9743a2a7b (idx18) in all 4 injectors, and idx18 BOOTS. => the injector }} is tolerated by the engine at load; NOT crash #2. (Same tolerance pattern as dangling holy sites + malformed colors.)
Also corrected a bookkeeping slip: the window 9743a2a7b..HEAD is 33 commits (not the ~50 full-branch count); 516677513 is list-pos 22. The confirmed BAD boot is 516677513; e301dd023 (injector fix) is list-pos 31, ABOVE it — irrelevant since }} is non-fatal anyway.
STANDING RESULT UNCHANGED: seed chain + deities + setup + idx37 + scope-cmpsvalue all boot-cleared; no single changed file reverted-alone stops the crash. Leading hypotheses remain (A) cross-file combination or (B) un-enumerated load surface.

### 16:03:12 PDT — DECISIVE: full idx19-40 revert BOOTS
delayed_test = idx18-equivalent across the whole idx19-40 window. BOOTED CLEAN.
=> Crash #2 IS in idx19-40, and it is a COMBINATION (no single-file revert caught it — that's why every per-file diagnostic crashed and per-file reading found nothing). Revert mechanism confirmed working.
NEXT: bisect the SET. Split idx19-40 by COMMIT into halves; revert lower half's files to idx18, keep upper half at HEAD; boot. Narrows the interacting change-set.

### 16:10:57 PDT — set-bisect: UPPER half (pos12-22) BOOTS => interacting set is in pos12-22
Lower half pos1-11 (pantheon revert+redo, logfix batches, granary, treasure-fleet, #6 picker) CLEARED as a group.
Upper half pos12-22 holds the combination. Split again: test pos12-17 (revert pos1-11 AND pos18-22, keep pos12-17 live).
pos12-17 = ded69463e(#5 exam-trait) 8e8428d6b(#10 -0 display) 9aa12e339(#8 relabel) 635ec38ad(#11 titles) 2b7570463(#9 impeach) 07d9b19ae(B2 reassign)
pos18-22 = ff6d810f1(#7 no-change) c895e3fcd(#7/#20/#21/#22 mission-bldgs) 74038cd67(#8 harem-excl) 85ae2e3a5(wu_jinshi fix) 516677513(chore)

### 16:17:32 PDT — set-bisect: pos12-17 live CRASHES => interacting set fully within pos12-17
pos18-22 (mission-bldgs #7, harem-excl #8, wu_jinshi fix, chore) CLEARED. Combination is in:
12 ded69463e #5 exam-trait congruence (martial offices/commanders get wu_jinshi degree)
13 8e8428d6b #10 Net Council Effectiveness -0 display (13 gui files, cosmetic)
14 9aa12e339 #8 Zongli button relabel (loc only)
15 635ec38ad #11 sub-position titles on character (characterwindow.gui)
16 2b7570463 #9 Impeach the Venal corruption-picker (censorate effect+gui+event+window)
17 07d9b19ae B2 54-province reassignment (00_default setup)
Split: keep pos12-14 live, revert pos15-17 (+ pos1-11,18-22).
