# DESIGN — Protectors-General: Lifan Yuan roster section + event arc

Task #39. Two parts, one subsystem (the 都護府 frontier marches, `se_QING_MARCH.txt`; see
`[[imp19c-protectorate-general-rework]]`). Modelled deliberately on the **amban arc** —
the roster in the Lifan Yuan panel and the `qing_amban.*` events — so the Protectors-General
(the marches' Governors-General) get the same central-roster visibility and the same kind of
lifecycle/interaction events, per the user: *"asking for additional money or manpower, dealing
with unrest in their protectorates, and so on."*

## Verified data model (code, not assumption)
- A **march / Protectorate-General** = a subject country carrying `qing_march = 1`
  (`se_QING_MARCH.txt:104/217`, set by `QING_found_march`; `qing_march_maritime = 1` for the
  maritime ones). It holds its own local princely states as ITS sub-subjects.
- Its **Governor-General (GG)** = the march country's **`current_ruler`**. `QING_march_appoint_gg`
  (`se_QING_MARCH.txt:255`) creates a Manchu Lifan-Yuan appointee (culture manchu + fanyi_jinshi,
  marked `qing_march_gg = 1`) and `set_as_ruler`s him on the march (:279).
- Existing per-march quarterly pulse: **`QING_march_pay_subsidy`** (`se_QING_MARCH.txt:453`, called
  from `00_monthly_country.txt:167`) already does `every_subject { limit = { has_variable =
  qing_march } ... }` — the iteration a GG-event scoring pass needs.
- Existing march-management effects the event options will call:
  `QING_march_set_subsidy = { tier = small|medium|high }` (sets `qing_subsidy_tier` + the
  `qing_subsidy_*` modifier); `QING_march_size_army` (rebuilds the subsidy army to
  `qing_march_target_cohorts`, which is 10/20/30 by subsidy tier); `QING_march_appoint_gg` /
  reappoint (installs a new GG).
- Lifan-Yuan perf coupling precedent: `qing_lifan_recent_amban_outcome` (a self-expiring signed
  var folded into `qing_min_perf_lifanyuan`, `se_QING_MINISTRY.txt:413`, added by #27). A march
  analog can fold GG-event outcomes the same way (the GG is a Lifan appointee, like the amban).

## PART A — Roster section (Lifan Yuan panel)
Clone the amban roster the panel already renders.
1. **Roster build** — in `se_QING_MINISTRY.txt`, alongside the existing
   `qing_lifanyuan_amban_subjects` build inside `QING_ministry_recompute_perf_lifanyuan`:
   `clear_variable_list qing_lifanyuan_march_subjects`; `every_subject { limit = { has_variable =
   qing_march }  ROOT = { add_to_variable_list = { name = qing_lifanyuan_march_subjects  target =
   prev } } }`. (Refreshes each Lifan pulse, so it tracks marches founded/lost.)
2. **Panel section** — `gui/qing_lifanyuan.gui`, a new block UNDER the amban `dynamicgridbox`
   (~:259–290 over `qing_lifanyuan_amban_subjects`). New `dynamicgridbox` datamodel =
   `Player.MakeScope.GetList('qing_lifanyuan_march_subjects')`; each row: GG portrait
   (datacontext = `Country.GetRuler`) + `[Country.GetRuler.GetName]` + the march's name/flag; an
   empty-note (`IsDataModelEmpty`) like the amban section's :251; suppress the party "C" chip
   (`blockoverride "PartyIcons" {}`, per #86).
   - **DATACONTEXT NOTE (review-checked):** the adversarial review claimed `Country.GetRuler` is
     "unproven" and that the GG must be stored in a var like the amban's `qing_amban_here`. That is
     WRONG and the claim was verified against the repo: `Country.GetRuler` / `<view>.GetRuler` is a
     proven portrait datacontext used throughout the GUI (diplomatic_view.gui:174/2734,
     government_view.gui:169/390/477/563/647). The amban uses a VAR only because the amban is NOT the
     ruler; the GG IS the march's ruler (`set_as_ruler`, se_QING_MARCH.txt:279), so `GetRuler` is the
     correct AND proven read. NO GG-data-model rewrite is needed (this removes the review's NO-GO).
3. **Loc** — header `QING_LIFANYUAN_PROTECTORS_GENERAL:0 "Protectors-General (都護府)"` + empty note.
- **Invariant:** list the march COUNTRY only (gated `qing_march`), never its sub-subject princely
  states.

## PART B — The Protectors-General event arc (`qing_march.*`)
New file `events/imp19c_mod_events/qing_march_events.txt`, namespace `qing_march`, CHI player-only,
mirroring `qing_amban_events.txt` shape (defensive `trigger` re-validating saved scopes;
`random_subject` re-pick where relevant; hidden follow-ups for any var-heavy work per the keju #38
tooltip-eval lesson — keep var math out of option previews). The GG to act on = a march's
`current_ruler`; scopes saved by the firing pulse (below).

### The event set (the user's concrete asks + amban parallels) — 5 events (right-sized to the amban arc's 4)
| id | event | trigger condition | options (cost/benefit to CHI) |
|---|---|---|---|
| `qing_march.1` | **Petition for support** (協餉) — the GG asks the throne for more silver AND/OR troops. ONE event, options branch by the march's actual need (subsidy vs establishment). [review #5: collapsed the former separate silver/troops events into one, matching the amban arc's size] | subsidy tier < high OR march army under `qing_march_target_cohorts`; a frontier threat/expansion flag | GRANT SILVER → `QING_march_set_subsidy` up one tier (recurring treasury cost); GRANT TROOPS → bump tier + `QING_march_size_army` (one-off manpower/treasury); DENY → soft-but-real: GG standing down + `liberty_desire` +5–10 + a stacking `qing_march_neglected` opinion (−20, ~2y) so repeated denials compound [review #7]. LIGHT SKILL GATE [review #6]: a high-skill GG's grant costs LESS (throne trusts his judgment), a low-skill GG's more — cost modifier, not a success/fail roll. |
| `qing_march.2` | **Unrest in the protectorate** — a rising among the march's own princely-state subjects; the GG puts it down | the march has a sub-subject with high unrest / low loyalty | LET THE GG HANDLE IT → skill check on GG martial+zeal (reuse the `qing_garrison_clean_crush_chance_svalue` idiom from #27): clean = cheap, chaotic = stab/legit toll + march loyalty hit; SEND IMPERIAL AID → treasury cost, reliable, GG standing down (undermined) |
| `qing_march.3` | **An able Governor-General** — a capable GG pacifies/expands the march (reward) | GG affinity ≥ 70 and march prospering | COMMEND (gold + standing, small treasury) / NOTE IT (small standing) — direct clone of `qing_amban.3` |
| `qing_march.4` | **A Governor-General goes overmighty / native** — long-tenured + estranged GG builds a personal power base | GG tenure elapsed + affinity < 40 | RECALL & REAPPOINT (`QING_march_appoint_gg`, turnover cost) / LEAVE HIM (march drifts, liberty_desire up) — clone of `qing_amban.2` |
| `qing_march.5` | **Turnover** — the GG dies / must be replaced | GG old/unhealthy or dead | REPLACE (`QING_march_appoint_gg`, appointment cost) / LEAVE VACANT (march drifts) — clone of `qing_amban.4` |

Every outcome folds a signed magnitude into a self-expiring `qing_lifan_recent_march_outcome`
var that `QING_ministry_recompute_perf_lifanyuan` reads (a new term beside the amban one) — the GG
is a Lifan charge, so good/bad GG management moves the Court of Colonial Affairs' Grand Council
standing, exactly as amban outcomes do (#27 req-7 pattern; self-expiring `days = 730`, NOT a bare
meter poke — the no-restoring-drift rule). [review #4 double-swing] SCALE the march term down (fold
it at HALF weight, or divide the recompute read by 2) and/or use a lower per-quarter fire chance
(~10% vs the amban ~15%), so amban + march outcomes firing in the same pulse don't over-swing the
meter. Keep the march var SEPARATE from the amban var (no cross-contamination).

### Firing pulse
Add **`QING_march_evaluate`** (se_QING_MARCH.txt), modelled on `QING_amban_evaluate`: iterate
`every_subject { limit = { has_variable = qing_march } }` (proven non-recursive — the amban roster
uses the identical pattern over CHI's DIRECT subjects; add a comment noting it does NOT descend into
the marches' princely-state sub-subjects [review #3]), save the march + its GG as scopes, and roll a
low per-quarter `random { chance = N }` for each event, **mutually exclusive by priority**
(turnover > overmighty > unrest > petition > commend — at most one per march per quarter), each gated
on the event's own condition. **CALL SITE [review #2, corrected]:** NOT from `QING_march_pay_subsidy`
(that is a pure 協餉 treasury/army transfer, not an event dispatcher). Call it from **`QING_GOV_pulse`
(se_QING_GOVERNANCE.txt), right after `QING_amban_evaluate` (~:620)** — so march and amban lifecycle
evaluations run together in the same governance pulse, matching the amban split (amban EVALUATE is in
the GOV pulse; the amban PAY/subsidy analog is separate). Throttle modal events through the shared
GC/court-event slot (`qing_gc_event_slot_used`, `[[imp19c-gc-event-throttle-rule]]`) so they don't
collide with GC/ministry events. (The double per-quarter `every_subject` over marches — this evaluate
+ the existing pay_subsidy — is intentional and matches the amban pattern; march count is small, ~7.)

### Loc + data
`qing_march.N.t/.desc/.a/.b(.tt)` per event; any new opinion/loyalty modifiers cloned from the
amban set (`qing_amban_cooperation_opinion` etc.); money strings use `¥` (task #30 done).

## Build order (design → review → implement in small reviewed steps)
1. This doc → review (adversarial) → user OK on the event set + the skill-check/perf-coupling choices.
2. PART A (roster) first — small, self-contained, verifiable in the panel.
3. `QING_march_evaluate` scoring pass + the perf-fold var + its recompute term.
4. `qing_march_events.txt` events one cluster at a time (petitions → unrest → lifecycle), each with loc.
5. Adversarial review of each batch BEFORE commit; brace-check; stage named files only.

## Open questions — RESOLVED (adversarial review 2026-08-05 + user)
- OQ-1: **Separate `QING_march_evaluate`**, called from `QING_GOV_pulse` after `QING_amban_evaluate`
  (NOT folded into `QING_march_pay_subsidy`). [review #2]
- OQ-2: **Light skill gate on the petition** — a cost MODIFIER (skilled GG's grant costs less), not a
  success/fail roll; the .2 unrest OUTCOME and the .3 "able" TRIGGER remain the full skill checks. [review #6]
- OQ-3: **Soft but real denial** — GG standing down + `liberty_desire` +5–10 + stacking
  `qing_march_neglected` opinion (~2y); repeated denials compound. No immediate breakaway. [review #7]
- OQ-4: **CHI player-only**, same as the amban arc (guard `tag = CHI` + not-AI via the pulse). [review OQ-4]
- OQ-5: **NEW `qing_lifan_recent_march_outcome` var**, folded at reduced weight (half) so it doesn't
  cross-contaminate or over-swing vs the amban outcome term. [review #4/#5]

## ADVERSARIAL REVIEW (2026-08-05) — VERDICT: GO after the minor edits above (NOT the rewrite the review demanded)
The review returned NO-GO on ONE "critical" item — that the roster's `Country.GetRuler` datacontext is
"unproven" and the GG must be moved into a var like the amban. **That blocker was checked against the
repo and is WRONG:** `Country.GetRuler` is a proven portrait datacontext (diplomatic_view.gui:174/2734,
government_view.gui:169/390/477/563/647); the amban uses a var only because it is not the ruler, whereas
the GG IS the march's ruler. No GG-data-model rewrite. The review's VALID findings are all folded in
above: #2 pulse location (→ QING_GOV_pulse), #4 perf double-swing (→ scaled/lower-chance), #5 collapse
the two petitions (→ one `qing_march.1`, 5-event arc), #6 light petition skill-gate, #7 denial teeth,
#3 non-recursive-every_subject comment. Two review points were STALE/wrong: #10 (it said the keju
"hidden follow-up" tooltip-eval-safety pattern doesn't exist — it DOES, committed this session as
qing_keju.20/.21, #38) and #1 (the datacontext blocker above).

## STATUS: DESIGN READY — reviewed, blocker refuted, valid fixes folded in. Awaiting user greenlight to
## implement (build order above: roster first, then evaluate pulse + perf term, then events by cluster).
