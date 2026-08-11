# DESIGN — #118 structural 1:1 office/post via one `qing_current_post` var

> **STATUS 2026-08-11: NOT-READY — PREMISE INVALIDATED by dr118v2 (adversarial re-review), source-confirmed.**
> Do NOT implement. The design's core justification — that #118 is needed to structurally fix the #77/#79
> "also a Hanlin Scholar" double-hat — is a **misdiagnosis**, verified wrong in source THIS session:
> - "Also a Hanlin Scholar" is the `qing_is_pool_scholar` title (00_offices.txt:191/253), NOT the Study marker.
> - #77 and #79 are **already fixed**: `QING_exam_pool_drop_member = yes` runs in the salt appoint
>   (se_QING_SALT.txt:69, tagged `[#77 1:1]`) and the caravan appoint (se_QING_CARAVAN.txt:882, `[#79 1:1]`),
>   forfeiting the Academy posting on appointment. The same per-appoint pool-drop idiom is applied in
>   COUNCIL/AMBAN/CANTON. `qing_is_pool_scholar` is not in this design's 14-flag domain, so the proposed
>   machinery would never even touch the marker that produced #77/#79.
> - dr118v2 BLOCKING-1: the doc's "7 hand-rolled pickers" are actually RELIEF-SWEEP branches (outer iter
>   already gated on the family marker); routing them through QING_char_holds_court_position would fire the
>   relief `if` for EVERY sitting member → EMPTY the Study/salt/caravan rosters. Roster-destroying.
> - dr118v2 BLOCKING-3: CHANGE 3+5 lose the existing multi-marker cleanup (COUNCIL:1538-1583 strips ALL
>   markers a char carries; the single-flag dispatch strips only one → a two-marker legacy char orphans one).
>
> **CONSEQUENCE: #118 as scoped is chasing a bug that is already closed.** The real 1:1 enforcement is the
> per-appoint `QING_exam_pool_drop_member` pattern, which already ships and works. A full structural refactor
> (new var + one chokepoint + 14 vacate paths + save-game backfill) is NOT required by any active bug. This is
> now a USER SCOPE DECISION (see overnight log): close #118 as obsoleted, or keep it as defensive hardening
> despite no active bug. NOT implementing either way until the user rules — the v1/v2 mechanism below is
> UNSAFE (roster-emptying) and must not be built as written.

---
Status: DRAFT — SUPERSEDED, see the NOT-READY banner above. Author: overnight run 2026-08-11. Diagnosis by diag118 (premise since REFUTED).

## Problem (from the task + diag118, source-verified)
"1:1 character↔post" repeatedly fails because there is **no single source of truth** for "what post does this
character hold." 14 independent per-family character markers (`qing_office_held`, `qing_zongli_diplomat`,
`qing_is_censor_inspector`, `qing_is_imperial_guardsman`, `qing_is_southernstudy`, `qing_is_upperstudy`,
`qing_amban_marker`, `qing_is_palace_eunuch`, `qing_is_harem_consort`, `qing_march_gg`, `qing_hoppo_marker`,
`qing_caravan_super_marker`, `qing_salt_commissioner_marker`, `qing_is_xj_beg`) are set (~31 paths) and cleared
(~33 paths) independently, and **7 hand-rolled eligibility checks each omit a DIFFERENT subset** of the markers:

- se_QING_CARAVAN.txt:284 — 4 terms (is_general/admiral/governor + qing_officer_marker); omits ALL script court markers
- se_QING_SALT.txt:173 — 4 terms; same omission
- se_QING_MINISTRY.txt:528 — 6 terms; omits zongli/censor/guard/study/amban/march/hoppo/caravan/salt/xj
- se_QING_SUBPOSTS.txt:105, :164 — 6 terms; same
- se_QING_SOUTHERNSTUDY.txt:185 — 5 terms; omits salt/caravan/hoppo/amban/... → **#79 root cause**
- se_QING_UPPERSTUDY.txt:179 — 5 terms → **#77 root cause**

The canonical trigger `QING_char_holds_court_position` (qing_dynasty_triggers.txt:241) DOES list all script court
markers, but these 7 sites never call it. Every omission is a latent #77/#79-shaped double-booking bug.

## #77 / #79 root cause (CONFIRMED in source)
Not a missing strip in the GC-appoint path. The Study **reconcile-sweeps** (SS:185 / US:179) relieve an attendant
who has taken another post by stripping his study marker — but their 5-term OR omits `qing_salt_commissioner_marker`
and `qing_caravan_super_marker`, so an attendant who becomes Salt Commissioner / Kashgar Superintendent is never
relieved → he holds both ("also a Hanlin Scholar" is the Study's flavor titling). Fixed structurally below.

## Decision: PARALLEL new var, NOT widening `qing_office_held` (correction to diag118)
diag118 proposed widening `qing_office_held`'s flag domain from 15 → 25 values (keeping the name to dodge a
203-ref / 37-file rename — that no-rename instinct is CORRECT and confirmed). BUT widening its DOMAIN silently
changes the meaning of every **bare** `has_variable = qing_office_held` read from "is a GC minister" to "holds any
court post" — a hidden regression across the ~15 GC-specific folds (COUNCIL figurehead/faction/corruption/decay,
JUSTICE, DECLINE, ACCOUNTABILITY, DELIBERATIVE, FACTION). The `var:qing_office_held = flag:chancellor`-style
VALUE comparisons would keep working, but the bare existence checks would not.

→ Instead: introduce a NEW var **`qing_current_post`** (flag value = the post-family id) that is the single
"is this character occupying ANY script-owned post?" source of truth. `qing_office_held` and all 13 other
per-family markers STAY exactly as they are (they carry family-specific meaning that GUIs/events read). This is
purely additive: no rename, no domain-widening, no change to any existing read. The dual-write is centralised in
the two chokepoints so it cannot drift.

`qing_current_post` flag domain (14, one per family; a char in a corps of N still holds ONE post):
`gc_office` (any of the 15 GC offices — family granularity, not per-office, since qing_office_held already carries
the specific office), `zongli_diplomat, censor_inspector, imperial_guardsman, southernstudy, upperstudy, amban,
palace_eunuch, harem_consort, march_gg, hoppo, caravan_super, salt_commissioner, xj_beg`.

## ⟪v2 — REVISED per dr118 adversarial review (1 CRITICAL + 2 HIGH + 2 MEDIUM). Changes below supersede v1.⟫

### v2 CHANGE 1 (was HIGH #1) — `qing_current_post` is the DISPATCH driver, NOT the picker gate
v1 replaced the pickers' 14-marker OR (`QING_char_holds_court_position`) with a lone
`NOT = { has_variable = qing_current_post }`. dr118: that DROPS the safety net — one forgotten stamp = a marker
present with no qing_current_post = silently drawable = double-book, with no marker-OR left to catch it. So:

- **PICKER GATE stays `QING_char_holds_court_position`** (the existing OR over all family markers). We ONLY
  EXTEND that trigger to include the markers it currently lists (it already has hoppo/caravan/salt/amban — verified
  qing_dynasty_triggers.txt:241). The 7 hand-rolled pickers (SS:185, US:179, SALT:173, CARAVAN:284, MINISTRY:528,
  SUBPOSTS:105/164) are changed to **CALL `QING_char_holds_court_position`** instead of their omit-prone inline OR —
  keeping engine-role terms (`is_general/is_admiral/is_governor`) and `qing_officer_marker` as SEPARATE terms (those
  are outside the trigger's script-marker domain). This closes #77/#79 (the Study sweeps gain the salt/caravan markers)
  AND every other omission at once, WITHOUT removing the redundant net.
- `qing_current_post` is used SOLELY to drive the vacate-old dispatch inside QING_post_stamp (change 2). It is a
  second source of truth kept as a CROSS-CHECK, never the sole gate. Two sources are safer than one only because the
  redundant one (the marker-OR) is retained.

### v2 CHANGE 2 (was CRITICAL) — enumerate ALL 14 vacate targets: exist vs NET-NEW
v1 falsely assumed "call each family's existing char-scope vacate." dr118 verified only 1 of 14 exists. Actual map
(each dispatch branch reads `var:qing_current_post` in CHAR scope and must resolve the country + clear the holder
var ONLY IF `this` is that holder, then `remove_variable = qing_current_post`; NO backfill — see highest-risk note):

| post-family | existing vacate? | dispatch branch action |
|---|---|---|
| gc_office | ✓ `QING_office_vacate_dispatch_nobackfill` (COUNCIL:1705, char-scope, no-backfill) | call it directly |
| amban | partial: `QING_amban_recall` (AMBAN:276) is SUBJECT/country-scope, $subject$-param, NOT `this`-callable | NET-NEW char-scope wrapper: resolve `this`'s amban subject, clear qing_amban_here there, then recall |
| salt | ✗ inline in reconcile sweep (SALT:167-185), country-scope, next branch BACKFILLS | NET-NEW: clear qing_salt_commissioner_holder if=this; strip-only, NO backfill branch |
| caravan | ✗ inline (CARAVAN:282-294), same shape | NET-NEW strip-only |
| hoppo | ✗ inline (CANTON reconcile) | NET-NEW strip-only |
| southernstudy | ✗ bare remove_variable in strip branch (SS:186); doesn't decrement chief/count | NET-NEW: remove study marker + chief marker if held |
| upperstudy | ✗ bare remove_variable (US:180) | NET-NEW, as study |
| xj_beg | ✗ bare remove_variable (XINJIANG:403) | NET-NEW |
| censor_inspector | ✗ inline in QING_office_appoint (COUNCIL:1538-1583) | NET-NEW: remove_variable qing_is_censor_inspector |
| zongli_diplomat | ✗ inline | NET-NEW: remove_variable qing_zongli_diplomat |
| imperial_guardsman | ✗ inline | NET-NEW: remove_variable qing_is_imperial_guardsman |
| palace_eunuch | ✗ inline / household recompute | NET-NEW: remove_variable qing_is_palace_eunuch (+ household holder var if=this) |
| harem_consort | ✗ inline / harem recompute | NET-NEW: remove_variable qing_is_harem_consort |
| march_gg | ✗ inline / march recompute | NET-NEW: clear march holder if=this |

So 13 of 14 dispatch branches are NET-NEW char-scope strip effects (mostly one `remove_variable` + an
`if=this` holder-clear). They live in ONE new file (se_QING_POST.txt) as `QING_post_vacate_<family>`, so the
"centralised" claim becomes true: dispatch → 14 small strip effects, none re-entering a fill. This is EXPLICITLY
the full scope — no "ship gc+amban, defer 12."

### v2 CHANGE 3 (was HIGH #2) — save-game backfill init sweep (REQUIRED)
qing_current_post is new; live saves have seated chars with family markers but no qing_current_post. One-time
guarded init (in QING_revenue_init-style boot path, per-var guarded so it's idempotent + backfills existing saves):
```
every_character = {
    limit = { employer = ROOT  NOT = { has_variable = qing_current_post }  QING_char_holds_court_position = yes }
    # derive the family flag from whichever marker the char carries, set qing_current_post accordingly
    if = { limit = { has_variable = qing_office_held }            set_variable = { name = qing_current_post value = flag:gc_office } }
    else_if = { limit = { has_variable = qing_amban_marker }      set_variable = { name = qing_current_post value = flag:amban } }
    ... (one else_if per family marker, same order as the trigger) ...
}
```
Because the PICKER gate is still QING_char_holds_court_position (change 1), an un-backfilled incumbent is STILL
un-drawable even before this sweep runs — so this is belt-and-suspenders, not the sole defense (defense in depth).

### v2 CHANGE 4 (was MEDIUM) — on-departure release (leaves-employ-without-dying)
Death is covered by the 5 on_character_death hooks (00_specific_from_code.txt:344-360, gain QING_post_release).
But "leaves CHI employ, no death" orphans qing_current_post (all sweeps are employer=ROOT-gated so they never touch
a departed man → he returns un-drawable forever). Add QING_post_release to the on-employment-change / on-leave hook
(mirror the existing amban/pilgrim on-departure orphan fixes at 00_specific_from_code.txt:295-332).

### v2 CHANGE 5 (was MEDIUM) — reconcile the EXISTING 46-line strip block in QING_office_appoint
QING_office_appoint (COUNCIL:1538-1583) already has its own 1:1 strip block. The stamp-tail must NOT create a
third parallel strip. RESOLUTION: QING_office_appoint's inline strip is REPLACED by the stamp call (QING_post_stamp
runs the dispatch-vacate-old); the 46-line block is deleted in favor of the one chokepoint. Verified this block's
targets are a subset of the 14 dispatch branches, so no behaviour is lost.

## The two chokepoints (new file se_QING_POST.txt)
```
# char scope. TAIL of every family fill, AFTER the family sets its own marker + holder var.
QING_post_stamp = {   # $post$ = one of the 14 flag ids
    if = {   # already holding a DIFFERENT post -> vacate the old one first (no double-book by construction)
        limit = { has_variable = qing_current_post  NOT = { var:qing_current_post = flag:$post$ } }
        QING_post_dispatch_vacate = yes
    }
    set_variable = { name = qing_current_post  value = flag:$post$ }
    LOG_line = { sys = QING  msg = "post-stamp: char takes a court post for" }
}
# char scope. HEAD of every family vacate/recall/death/departure cleanup.
QING_post_release = { if = { limit = { has_variable = qing_current_post }  remove_variable = qing_current_post } }
# char scope. 14-branch if-chain on var:qing_current_post -> the right QING_post_vacate_<family> (each strip-only).
QING_post_dispatch_vacate = { ... 14 branches (table above) ... }   # gc_office branch calls the NO-BACKFILL dispatcher
```

## Engine roles (is_governor/general/admiral) — unified sweep (CLEAN per dr118)
ONE new sweep in QING_GOV_pulse; a char with both qing_current_post and an engine role is barred TWICE at the
picker (the two term-groups are separate), so no double-draw during the ≤1qtr window. The swept vacate uses
no-backfill (matches QING_council_prune_seat, COUNCIL:140) — seat sits empty as today.
```
every_character = { limit = { employer = ROOT  has_variable = qing_current_post
                              OR = { is_general=yes is_admiral=yes is_governor=yes } }
    QING_post_dispatch_vacate = yes }
```

## SINGLE HIGHEST-RISK POINT (dr118) — no-backfill everywhere in dispatch
The gc_office dispatch branch MUST call `QING_office_vacate_dispatch_nobackfill`, NEVER `QING_office_vacate_dispatch`
(the backfill variant → QING_council_autofill_office → QING_council_prune_seat → re-enters vacate = the documented
startup HANG "Too deeply nested scripted block", COUNCIL:120-130). Every NET-NEW salt/caravan/etc. vacate carved
from a reconcile sweep uses ONLY the strip half, EXCLUDING the backfill branch (e.g. SALT:180-185), or a stamp
(which fires dispatch-vacate) triggers a re-appoint chain. Re-entrancy is otherwise safe: release removes the old
var, then set writes the new — no clobber (dr118 vector 1, contingent on strip-only vacates).

## Why 1:1 now holds (post-fix scenarios; all dr118 vectors resolved)
1. Draw A→seat1, A becomes governor: GOV_pulse sweep dispatch-vacates the script post (no-backfill); picker bars A
   via the separate engine-role term until he leaves the governorship. No double-list.
2. A routed into seat2 while holding seat1: stamp sees qing_current_post≠seat2 → dispatch-vacate seat1 first. 1:1 by construction.
3. A dies: on_death hook → family vacate → QING_post_release + holder clear. Gone from pool.
4. A leaves employ (no death): on-departure hook (change 4) → QING_post_release. Not orphaned.
5. Study attendant becomes Salt Commissioner: salt fill stamps salt_commissioner ≠ southernstudy → dispatch-vacate
   strips the study marker → NOT both (#77/#79 fixed). AND the Study picker now calls QING_char_holds_court_position
   which lists the salt marker → the reconcile sweep also relieves him (redundant catch).
6. Live save with unstamped incumbents: picker gate is still the marker-OR → un-drawable; the init sweep (change 3)
   backfills qing_current_post so the dispatch driver works thereafter.

## Fallback (per task, if impl proves intractable)
DISABLE autofill (seat unfilled, manual staffing) — NEVER mint. dr118 verdict: "NOT intractable — no need for the
disable-autofill fallback" once the 4 fixes are in.

## Validation / logging
Keep the existing >1-marker tripwire sweep (QING_council_recompute) as boot proof. Add LOG_line to
QING_post_dispatch_vacate (per relieve) + QING_post_stamp/_release. Static strings only (log-string-macro rule).

## Sequencing
Lands FIRST; gates #111/#114/#116/#117 and structurally fixes #77/#79. Do NOT convert any autofill to draw until
the stamp/release/dispatch trio + the 13 net-new vacates + the init backfill + the on-departure release are all in
and this v2 design has passed a CLEAN code-review.
