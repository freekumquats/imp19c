# DESIGN — #118 structural 1:1 office/post via one `qing_current_post` var

> **STATUS 2026-08-11 v8: CLEAN — zero findings, READY TO IMPLEMENT.** Six independent adversarial review
> rounds (dr118 on v1→v2; dr118v3 on v3→v4; dr118v4 on v4→v5; a from-scratch review on v5→v6; a from-scratch
> review on v6→v7; a narrow confirm-only pass on v7→v8) progressively found and fixed 2 blocking + 3 medium +
> 6 low/descriptive issues. The final round returned CLEAN with zero findings. Per standing rule, this clears
> the gate — implementation may now begin, in the order given at the bottom of this doc (## Sequencing).
> - **(fixed) CHANGE 4's printed `on_move_country` guard was scope-type-mismatched**: `on_move_country`'s effect
>   runs in CHARACTER scope (`ROOT` = the moved character, confirmed at 00_specific_from_code.txt:792), so
>   comparing `scope:old_country = ROOT` / `NOT = { employer = ROOT }` compared a country to a character in both
>   clauses. Fixed: compare against the literal tag `c:CHI` instead of `ROOT` (every family this design covers
>   is a Qing-only institution, so hardcoding CHI here — unlike #75's deliberately global Monetary Standard —
>   is correct, not a scope narrowing).
> - **(fixed, minor)** CHANGE 5's "strips 11 ... at COUNCIL:1538-1583" phrasing was imprecise (gc_office is
>   handled at :1503/:1530, just above that range, not inside it) — reworded.
> - **(fixed, minor)** a stale effect name `QING_subpost_staff_corps` (only the `_minted` variant is live) —
>   corrected.
> v6's own 5 fixes (all reverified clean this round): the amban/march_gg/xj_beg exclusion is now fully
> consistent document-wide; the palace_eunuch row's list/holder-var citations check out and `remove_list_variable`
> is proven syntax in this codebase; the 10-site stamp inventory spot-checked correct across 8 of 10 rows; the
> CHANGE 3 backfill's 11-branch chain is complete and non-contradictory.
> - **(BLOCKING, fixed) CHANGE 4 was not implementable**: its cited precedent (00_specific_from_code.txt:295-332)
>   is actually inside the `on_character_death` block (opens :234) — those are DEATH handlers, not an
>   on-departure hook. No "on-employment-change/on-leave hook" exists in this codebase at all. v6 REPLACES
>   CHANGE 4 with a real target (`on_move_country`, :792, which provides `scope:old_country`), narrowly scoped
>   (see the new CHANGE 4 below) to avoid firing on normal appointment-into-employ.
> - **(MEDIUM, fixed) xj_beg is subject-employed exactly like march_gg** (`employer = c:XNG`,
>   se_QING_XINJIANG.txt:118/148/189) but wasn't given march_gg's exclusion treatment. v6 makes this consistent:
>   **amban, march_gg, AND xj_beg are ALL excluded from the qing_current_post machinery** (see below) — not
>   patched into it. This is also what makes the corrected CHANGE 4 safe (see above) and removes CHANGE 3's
>   dead branches (see below).
> - **(MEDIUM, fixed) CHANGE 3's boot backfill had dead else_if branches** for amban/march_gg/xj_beg (its
>   `employer = ROOT` outer limit can never reach any of them while posted). Resolved by the same exclusion.
> - **(LOW, fixed) the palace_eunuch CHANGE 2 row cited a nonexistent `qing_palace_eunuch_holder` var.** No such
>   var exists; the real state is the LIST `qing_household_eunuchs` + the display-only Chief-Eunuch seat var
>   `qing_office_chief_eunuch_holder` (SS_HOUSEHOLD:318/325). Row corrected below.
> - **(LOW, fixed) the design never enumerated the 13 non-gc_office stamp INSERTION sites** — only the gc_office
>   stamp (CHANGE 5) was ever named, for a design whose entire correctness claim is "every appoint path stamps."
>   v6 adds a concrete file:line inventory (new section below) for all remaining CHI-employed families.
> **The real driver (per user correction) is NOT #77/#79.** `create_character` is being retired as the way
> offices get filled (#111/#113/#114/#116/#117/#119: exam/GC/amban/tribute posts move to DRAWING existing
> characters instead of minting fresh ones). Once many subsystems all draw from overlapping pools of live
> characters, the risk of the SAME character double-seated across offices rises sharply — #118's job is to
> close that risk structurally, for ALL 14 office families, not just the Hanlin case #77/#79 patched.
>
> The #77/#79 framing in the original problem statement below was a misdiagnosis (that specific double-hat
> is already fixed by the per-appoint `QING_exam_pool_drop_member` idiom in SALT/CARAVAN/CANTON) — but that
> does NOT obsolete #118, because the general omission problem (7 sites each checking a different incomplete
> subset of the 14 markers) is real independent of #77/#79, and gets sharply worse once draw-conversion ships.
>
> **v2 had two real, source-confirmed defects (dr118v2), fixed below in v3 — NOT abandoned, corrected:**
> - **BLOCKING-1 (fixed by v3 CHANGE 1):** the "7 hand-rolled pickers" are actually RELIEF-SWEEP branches whose
>   outer `every_character` iteration is ALREADY gated on that family's own marker (verified in source:
>   SS:185, US:179, MINISTRY:528, SUBPOSTS:105/164, CARAVAN:284, SALT:173). Routing their inner disqualifier
>   through `QING_char_holds_court_position` (true for the very marker the outer loop requires) is a
>   tautology — every member matches its own relief condition → empties the roster. v3 does NOT do this.
> - **BLOCKING-3 (fixed by v3 CHANGE 5):** COUNCIL's existing 46-line strip block (COUNCIL:1538-1583) strips
>   ALL family markers unconditionally (self-guarded, handles a legacy 2-marker character fully); a single-
>   flag dispatch driven by `qing_current_post`'s one current value would only strip ONE, orphaning the other.
>   v3 does NOT delete that block — it stays as a defense-in-depth backstop; the stamp call is ADDED alongside it.
>
> **The actual draw-time eligibility gate is separate from those 7 sites**, and was already correctly designed:
> `QING_char_holds_court_position` (qing_dynasty_triggers.txt:241) IS the picker/candidate-eligibility filter
> used at real draw sites (e.g. the just-shipped `se_QING_FRONTIER_PICKER.txt:38`). It already lists 13 of 14
> families — missing only `qing_is_xj_beg`. That one-line addition ships independently of the rest of this design.

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

## ⟪v3 — CORRECTED per dr118v2 (2 BLOCKING) + user ruling on the real driver. Changes below supersede v1/v2.⟫

### v3 CHANGE 1 (was v2's HIGH #1, now corrected per dr118v2 BLOCKING-1) — two DIFFERENT mechanisms for two DIFFERENT kinds of site
v2 conflated "picker gates" (draw-time eligibility filters) with the 7 SS/US/MINISTRY/SUBPOSTS/SALT/CARAVAN
sites, which are actually relief-sweeps whose outer iteration is already gated on the family's own marker. One
fix cannot serve both; v3 splits them:

- **REAL picker/draw-time gates** (e.g. `se_QING_FRONTIER_PICKER.txt:38`, and any future #111/#113/#114/#116/
  #117/#119 draw-conversion) keep gating on **`QING_char_holds_court_position`** (qing_dynasty_triggers.txt:241)
  — this is the correct mechanism here, unchanged from v2's intent. Add the one missing term
  (`has_variable = qing_is_xj_beg`) to close its last omission. Ships independently, low-risk.
- **5 of the 7 sites are genuine marker-gated `every_character` relief-sweeps** (SS:171/185, US:165/179,
  MINISTRY:508/528, SUBPOSTS:102/105 and :157/164 — verified in source). These are NOT routed through
  `QING_char_holds_court_position` (that was the tautology). Instead: their outer `every_character` iteration
  limit changes from the family's own marker (`has_variable = qing_is_southernstudy` / `has_variable = $marker$`
  / etc.) to **`var:qing_current_post = flag:<this family>`**. Once every appoint path stamps `qing_current_post`
  atomically (vacating any old post first — CHANGE 2), a character can only ever appear in ONE family's
  post-holder set at a time, by construction — so the "cross-family" half of each site's fused disqualifier OR
  (the `qing_office_held` / `qing_is_harem_consort` terms) is DELETED as structurally unreachable, leaving a
  shorter but still-valid limit. The recompute/count/roster-list building logic in the `else` branch is
  UNCHANGED, just now gated on the corrected outer condition.
- **(dr118v4 fix, was a real bug in the above)** The engine-role half of that SAME fused disqualifier
  (`is_general`/`is_admiral`/`is_governor`/`qing_officer_marker`) is KEPT, per the earlier correction — but its
  STRIP ACTION must be EXTENDED: today it only does `remove_variable = qing_is_<family>` (+ chief marker). Once
  the outer iteration is keyed on `qing_current_post` instead of the family marker, that branch MUST ALSO call
  `QING_post_release` (clear `qing_current_post`) in the SAME `if`. Reason: the engine-role transition (a man
  becoming general/governor) fires no stamp/dispatch/hook of its own, so nothing else ever clears
  `qing_current_post` on that path. Without this addition, `qing_current_post` would still say `<family>` on a
  man long after his family marker was stripped — and when his command/governorship LATER ends, the
  `qing_current_post`-keyed outer iteration would re-catch him, the engine-role check would no longer match, and
  the `else` branch would silently RE-ADD him to the roster/count/chief-eligibility with no family marker at
  all — a phantom-member regression worse than what this design is fixing. Every repointed site's engine-role
  branch gets this one extra line; nothing else about it changes.
- **(dr118v4 note; name corrected dr118-final-v2 — `QING_subpost_staff_corps` without the `_minted` suffix is
  not a live effect, only the minted variant exists)** SUBPOSTS' two sweeps (`QING_subpost_staff_corps_minted`,
  `QING_subpost_strip_double_booked`)
  are shared PARAMETERIZED effects — one `$marker$` body serves the diplomat/censor/guard corps interchangeably.
  Repointing their outer iteration to `var:qing_current_post` therefore needs a THREADED `$post$` flag param
  (one per caller, matching whichever corps that call site serves), not a single hardcoded family flag — the
  param plumbing is mechanical but must not be skipped at implementation time.
- **SALT (:180-191) and CARAVAN (:280-289) are a DIFFERENT shape** (dr118v3 review, source-verified) — country-
  scope single-holder reconciles (`has_variable = qing_salt_commissioner_holder` / `qing_caravan_super_holder`,
  a COUNTRY var, not a per-character marker gate; no `every_character`). CHANGE 1 does NOT touch these two —
  they are NOT re-pointed to `var:qing_current_post`. Their NET-NEW dispatch-vacate branch (CHANGE 2) still
  applies (clearing the country holder var via `employer = {}` when `this` is that holder), but the EXISTING
  reconcile branch's own engine-role check (a) is LEFT IN PLACE, unchanged — it is the only thing enforcing 1:1
  for these two families today and nothing in v4 replaces it.
- **The ENGINE-role conflict case (is_general/is_admiral/is_governor/`qing_officer_marker`) is NOT centralized
  away** (dr118v3 review: the originally-proposed unified GOV_pulse sweep omitted `qing_officer_marker`, which
  exists specifically because a garrison field officer is not reliably caught by `is_general` — BT-7/Tsedan-612
  — and runs quarterly-only while these rosters also recompute on panel-open, so centralizing would reopen the
  #79 stale-roster symptom for up to a quarter). v4: KEEP each site's own engine-role+`qing_officer_marker`
  disqualifier exactly as it is today, for ALL 7 sites (including SALT/CARAVAN's). Only the CROSS-FAMILY
  disqualifier is removed from the 5 corps sites (per the bullet above) — the engine-role check is untouched
  everywhere. No unified GOV_pulse engine-role sweep is introduced by this design.

### v2 CHANGE 2 (was CRITICAL) — enumerate ALL 14 vacate targets: exist vs NET-NEW
v1 falsely assumed "call each family's existing char-scope vacate." dr118 verified only 1 of 14 exists. Actual map
(each dispatch branch reads `var:qing_current_post` in CHAR scope and must resolve the country + clear the holder
var ONLY IF `this` is that holder, then `remove_variable = qing_current_post`; NO backfill — see highest-risk note):

| post-family | existing vacate? | dispatch branch action |
|---|---|---|
| gc_office | ✓ `QING_office_vacate_dispatch_nobackfill` (COUNCIL:1705, char-scope, no-backfill) | call it directly |
| salt | ✗ inline in reconcile sweep (SALT:167-185), country-scope, next branch BACKFILLS | NET-NEW: clear qing_salt_commissioner_holder if=this; strip-only, NO backfill branch |
| caravan | ✗ inline (CARAVAN:282-294), same shape | NET-NEW strip-only |
| hoppo | ✗ inline (CANTON reconcile) | NET-NEW strip-only |
| southernstudy | ✗ bare remove_variable in strip branch (SS:186); doesn't decrement chief/count | NET-NEW: remove study marker + chief marker if held |
| upperstudy | ✗ bare remove_variable (US:180) | NET-NEW, as study |
| censor_inspector | ✗ inline in QING_office_appoint (COUNCIL:1538-1583) | NET-NEW: remove_variable qing_is_censor_inspector |
| zongli_diplomat | ✗ inline | NET-NEW: remove_variable qing_zongli_diplomat |
| imperial_guardsman | ✗ inline | NET-NEW: remove_variable qing_is_imperial_guardsman |
| palace_eunuch | ✗ inline / household recompute | NET-NEW (dr118-final corrected): `remove_variable = qing_is_palace_eunuch` + delist `this` from the LIST `qing_household_eunuchs` (SS_HOUSEHOLD, the actual roster — no per-eunuch holder var exists) + clear `qing_office_chief_eunuch_holder` ONLY `if=this` currently holds that seat (SS_HOUSEHOLD:318/325, the display-only Chief-Eunuch var — the ONLY holder-shaped var in this family; the prior table's "household holder var if=this" cited a nonexistent general holder var and is corrected here) |
| harem_consort | ✗ inline / harem recompute | NET-NEW: remove_variable qing_is_harem_consort |

**EXCLUDED from this table (dr118-final, made consistent — 3 families, not 1):** `amban`, `march_gg`, and
`xj_beg` are ALL employed by a SUBJECT country, not CHI (`se_QING_AMBAN.txt`:205 while posted;
`se_QING_MARCH.txt`; `se_QING_XINJIANG.txt`:118/148/189 — `employer = c:XNG`) — invisible to every
`employer = ROOT`-gated sweep this design uses (the picker gate, the boot backfill, any future GOV_pulse-style
sweep). The original table only conceded this for march_gg (and the concession was itself keyed to a phantom
holder-var, since corrected) while listing amban and xj_beg as ordinary NET-NEW targets — inconsistent, since
all three have the identical shape. v6: **all three are OUT of the `qing_current_post` machinery entirely** —
no CHANGE 2 vacate branch, no CHANGE 3 backfill branch, no CHANGE 4 release. 1:1 for these three continues to
rely solely on the EXISTING `QING_char_holds_court_position` marker gate (already listing `qing_amban_marker`
and `qing_march_gg`; `qing_is_xj_beg` is the one-line addition this design ships independently either way).
This is a genuine scope-narrowing, not a gap being hidden: the machinery's job is preventing double-booking
among CHI-EMPLOYED draw-conversion targets (#111/#113/#114/#116/#117/#119's exam/GC cluster), and a
subject-employed officer is not in that CHI-employed candidate pool to begin with (every real picker gate is
itself `employer = ROOT`-scoped) — so the marker-only gate these three already have is not a weaker fallback,
it is the actually-reachable enforcement for a family the new var structurally cannot see.

That leaves **11 of 14 dispatch branches** as NET-NEW char-scope strip effects (mostly one `remove_variable` +
an `if=this` holder-clear), all CHI-employed. They live in ONE new file (se_QING_POST.txt) as
`QING_post_vacate_<family>`, so the "centralised" claim becomes true: dispatch → 11 small strip effects
(+ the 1 existing gc_office call), none re-entering a fill. This is EXPLICITLY
the full scope — no "ship gc+amban, defer 12."

### v2 CHANGE 3 (was HIGH #2) — save-game backfill init sweep (REQUIRED)
qing_current_post is new; live saves have seated chars with family markers but no qing_current_post. One-time
guarded init (in QING_revenue_init-style boot path, per-var guarded so it's idempotent + backfills existing saves):
```
every_character = {
    limit = { employer = ROOT  NOT = { has_variable = qing_current_post }  QING_char_holds_court_position = yes }
    # derive the family flag from whichever marker the char carries, set qing_current_post accordingly.
    # ONLY the 11 CHI-employed families are enumerated here (dr118-final) — amban/march_gg/xj_beg are
    # deliberately ABSENT: they are excluded from the whole machinery (CHANGE 2 note above), and since
    # they're never employer=ROOT while posted, an else_if for them here would be dead code (the earlier
    # v5 draft included a qing_amban_marker branch that could never fire — removed, not just unreachable).
    if = { limit = { has_variable = qing_office_held }            set_variable = { name = qing_current_post value = flag:gc_office } }
    else_if = { limit = { has_variable = qing_salt_commissioner_marker }  set_variable = { name = qing_current_post value = flag:salt_commissioner } }
    else_if = { limit = { has_variable = qing_caravan_super_marker }      set_variable = { name = qing_current_post value = flag:caravan_super } }
    else_if = { limit = { has_variable = qing_hoppo_marker }              set_variable = { name = qing_current_post value = flag:hoppo } }
    else_if = { limit = { has_variable = qing_is_southernstudy }         set_variable = { name = qing_current_post value = flag:southernstudy } }
    else_if = { limit = { has_variable = qing_is_upperstudy }            set_variable = { name = qing_current_post value = flag:upperstudy } }
    else_if = { limit = { has_variable = qing_is_censor_inspector }      set_variable = { name = qing_current_post value = flag:censor_inspector } }
    else_if = { limit = { has_variable = qing_zongli_diplomat }          set_variable = { name = qing_current_post value = flag:zongli_diplomat } }
    else_if = { limit = { has_variable = qing_is_imperial_guardsman }    set_variable = { name = qing_current_post value = flag:imperial_guardsman } }
    else_if = { limit = { has_variable = qing_is_palace_eunuch }         set_variable = { name = qing_current_post value = flag:palace_eunuch } }
    else_if = { limit = { has_variable = qing_is_harem_consort }         set_variable = { name = qing_current_post value = flag:harem_consort } }
}
```
Because the PICKER gate is still QING_char_holds_court_position (change 1), an un-backfilled incumbent is STILL
un-drawable even before this sweep runs — so this is belt-and-suspenders, not the sole defense (defense in depth).

### v6 CHANGE 4 (was v2's MEDIUM; dr118-final found the ORIGINAL version unimplementable — corrected here)
Death is covered by the 5 on_character_death hooks (00_specific_from_code.txt:344-360, gain QING_post_release).
But "leaves CHI employ, no death" would orphan qing_current_post (all sweeps are employer=ROOT-gated so they
never touch a departed man → he returns un-drawable forever) — IF such a departure path existed for a
CHI-employed family member. It does, rarely (defection/exile/a subject absorption moving a man out of CHI).

**What was wrong (dr118-final):** the original text cited "the existing amban/pilgrim on-departure orphan
fixes at 00_specific_from_code.txt:295-332" as precedent to mirror, and told the implementer to add
`QING_post_release` to "the on-employment-change / on-leave hook." BOTH claims are false: lines 295-332 are
INSIDE the `on_character_death` block (which opens at :234) — they are the dying-amban and dying-pilgrim death
handlers, not an on-departure hook. And no "on-employment-change/on-leave" on_action exists anywhere in this
codebase. (This also mattered less than it looked: amban is now excluded from the machinery entirely — CHANGE
2 note above — so "mirror the amban fix" was never the right precedent to begin with.)

**The real hook, and the scoping it needs:** `on_move_country` (00_specific_from_code.txt:792) fires when a
character's employer country changes, and exposes `scope:old_country` (the origin). This is the only genuine
candidate. It must be scoped NARROWLY — `on_move_country` also fires on ordinary appointment-into-employ paths
for OTHER (excluded) families (e.g. a newly-minted Xinjiang beg or a newly-posted amban is `move_country`'d
INTO a subject, se_QING_XINJIANG.txt:118/148, se_QING_AMBAN.txt:183) — a naive unconditional
`QING_post_release` on this hook would strip a CHI-employed man's `qing_current_post` on any ordinary move, not
just a true departure. Since amban/march_gg/xj_beg no longer carry `qing_current_post` at all (CHANGE 2
exclusion), the ONLY characters this hook needs to act on are ones who HELD `qing_current_post` at the moment
their employer changed away from CHI:
```
on_move_country = {
    effect = {
        if = {
            limit = {
                scope:old_country = c:CHI
                has_variable = qing_current_post
                NOT = { employer = c:CHI }
            }
            QING_post_release = yes
        }
    }
}
```
(dr118-final-v2 fix: `on_move_country`'s effect block runs in CHARACTER scope — `ROOT` there IS the moved
character, verified at 00_specific_from_code.txt:792, so comparing `scope:old_country = ROOT` or `employer =
ROOT` — both country-vs-character — was a scope-type mismatch that would not express the intended condition.
Since every family this design tracks is a Qing-specific court post [gc_office, salt/caravan/hoppo,
southernstudy/upperstudy, censor/zongli/guardsman, eunuch, harem — all CHI-only institutions, unlike #75's
Monetary Standard which was deliberately global-uniform], the correct compare is against the literal tag
`c:CHI`, not `ROOT` — `has_variable`/`employer` with no scope prefix already implicitly read `this`/`ROOT`
the character in a character-scope effect, which is what the un-prefixed clauses correctly do here.)
This only ever fires for a man who WAS a CHI post-holder and is no longer employed by CHI — never on an
appointment INTO employ (a different transition), and never for the three excluded subject-employed families
(they never set `qing_current_post`, so the `has_variable` guard alone already excludes them).

### v6 NEW — the 10 remaining stamp INSERTION sites (dr118-final: this inventory was missing entirely)
CHANGE 5 named the ONE gc_office stamp site. The other 10 CHI-employed families' `QING_post_stamp` insertion
points were never enumerated — for a design whose entire correctness claim is "every appoint path stamps
atomically," an unlisted site is a silent gap the implementer could miss. Found by grepping every SET site of
each family's marker (source-verified, this session):

| family | stamp insertion site(s) — add `QING_post_stamp = { post = <family> }` immediately after each |
|---|---|
| salt_commissioner | se_QING_SALT.txt:79 (`QING_salt_commissioner_appoint`-style fill, sets `qing_salt_commissioner_marker`) |
| caravan_super | se_QING_CARAVAN.txt:892 |
| hoppo | se_QING_CANTON.txt:499 |
| southernstudy | se_QING_SOUTHERNSTUDY.txt:110, :140, :309 (3 sites — mint-fill + a second fill path + a promotion/chief-related path; stamp is idempotent so calling it at all 3 is safe even if one turns out to be a re-affirmation of an existing member, not a first assignment) |
| upperstudy | se_QING_UPPERSTUDY.txt:110, :138, :317 (same 3-site shape as southernstudy) |
| censor_inspector | common/scripted_guis/QING_governance_actions.txt:690, common/scripted_guis/QING_censorate_panel.txt:98 |
| zongli_diplomat | common/scripted_guis/QING_governance_actions.txt:702, common/scripted_guis/QING_zongli_panel.txt:106 |
| imperial_guardsman | common/scripted_guis/QING_governance_actions.txt:696, common/scripted_guis/QING_guard_panel.txt:99 |
| palace_eunuch | se_QING_HOUSEHOLD.txt:95 |
| harem_consort | se_QING_HAREM.txt:94, :136, :888 (3 sites) |

Implementation note: several families have 2-3 set sites (a scripted_gui appoint action + a panel-open handler,
or a mint-fill + a later recompute path) — this is EXISTING duplication in how these markers already get set,
not something this design introduces. Since `QING_post_stamp` is idempotent (setting the same flag value twice
is a no-op past the first call; only a DIFFERENT value triggers dispatch-vacate), stamping at every listed site
is safe and does not require first determining which site is the "real" first assignment.

### v3 CHANGE 5 (was v2's MEDIUM, corrected per dr118v2 BLOCKING-3) — do NOT delete the existing 46-line strip block
QING_office_appoint already handles **9 of the 11** CHI-employed families unconditionally (self-guarded
no-ops) — all except `salt_commissioner` and `caravan_super` (dr118-final-v3: the earlier "handles all 11"
phrasing directly contradicted this same paragraph's own "everything except salt/caravan/xj_beg" a few lines
down — corrected). 8 family markers are stripped via `remove_variable` at COUNCIL:1538-1583 (that range's 10
total strips also incidentally cover `qing_amban_marker`:1563 and `qing_march_gg`:1582, the two EXCLUDED
subject-employed families — not part of the CHI-employed 11 at all), plus `gc_office` itself is handled via
the vacate at :1503 and the overwrite at :1530 (dr118-final-v2: corrected from claiming gc_office is "at
1538-1583" — it's handled just above that range). This fully handles even a legacy character carrying TWO of
those 9 at once. A single-flag dispatch driven by `qing_current_post`'s one current value can only strip the
ONE family that value names — it would orphan a second, pre-existing stale marker on such a character.
RESOLUTION: the 46-line block STAYS, unchanged, as a defense-in-depth backstop against legacy multi-marked
state for those 9 families (salt/caravan/xj_beg were never covered by it and are not newly at risk — CHANGE 3's
boot backfill is what reconciles legacy salt/caravan multi-marking instead). `QING_post_stamp`
(for the `gc_office` flag) is called ADDITIONALLY, alongside it, not instead of it. Going forward, once every
appoint path is migrated to stamp through the one chokepoint, NEW multi-marking becomes structurally impossible
— the exhaustive block's job shrinks to "insurance for saves/characters that predate this fix," which is exactly
what CHANGE 3's boot backfill sweep is for (extend it to also strip any EXTRA stale markers beyond the one it
derives qing_current_post from, so legacy multi-marked characters get reconciled once, on boot, rather than
relying on 11 running blocks).

## The two chokepoints (new file se_QING_POST.txt)
```
# char scope. TAIL of every family fill, AFTER the family sets its own marker + holder var.
QING_post_stamp = {   # $post$ = one of the 11 CHI-employed flag ids (amban/march_gg/xj_beg excluded, see CHANGE 2)
    if = {   # already holding a DIFFERENT post -> vacate the old one first (no double-book by construction)
        limit = { has_variable = qing_current_post  NOT = { var:qing_current_post = flag:$post$ } }
        QING_post_dispatch_vacate = yes
    }
    set_variable = { name = qing_current_post  value = flag:$post$ }
    LOG_line = { sys = QING  msg = "post-stamp: char takes a court post for" }
}
# char scope. HEAD of every family vacate/recall/death/departure cleanup.
QING_post_release = { if = { limit = { has_variable = qing_current_post }  remove_variable = qing_current_post } }
# char scope. 11-branch if-chain on var:qing_current_post -> the right QING_post_vacate_<family> (each strip-only).
QING_post_dispatch_vacate = { ... 11 branches (table above) ... }   # gc_office branch calls the NO-BACKFILL dispatcher
```

## Engine roles (is_governor/general/admiral) — NO unified sweep (v3 CORRECTION, dr118v3)
v2 proposed ONE new centralized sweep in QING_GOV_pulse for the engine-role case. dr118v3 found this REGRESSES
two things: (1) it omitted `qing_officer_marker` (added to all 7 sites specifically because a garrison field
officer is not reliably caught by `is_general` — BT-7/Tsedan-612); (2) it would run quarterly-only while the
corps rosters also recompute on panel-open, reopening the #79 stale-roster-in-UI symptom for up to a quarter.
v3: **NO unified sweep is built.** Each of the 7 sites keeps its OWN existing engine-role+`qing_officer_marker`
disqualifier CONDITION exactly as today (the trigger/OR is untouched everywhere; SALT/CARAVAN's branch is
untouched period, per CHANGE 1). At the 5 repointed corps sites only, this branch's ACTION gains one line
(`QING_post_release`, per the dr118v4 fix above) — the condition that decides WHETHER it fires never changes,
only what it does once it fires, and only where the outer iteration was repointed. The picker-gate side
(`QING_char_holds_court_position`) still independently bars a character with BOTH an engine role and a script
post from being drawn, so double-draw protection is unaffected by dropping the unified-sweep idea.

## SINGLE HIGHEST-RISK POINT (dr118) — no-backfill everywhere in dispatch
The gc_office dispatch branch MUST call `QING_office_vacate_dispatch_nobackfill`, NEVER `QING_office_vacate_dispatch`
(the backfill variant → QING_council_autofill_office → QING_council_prune_seat → re-enters vacate = the documented
startup HANG "Too deeply nested scripted block", COUNCIL:120-130). Every NET-NEW salt/caravan/etc. vacate carved
from a reconcile sweep uses ONLY the strip half, EXCLUDING the backfill branch (e.g. SALT:180-185), or a stamp
(which fires dispatch-vacate) triggers a re-appoint chain. Re-entrancy is otherwise safe: release removes the old
var, then set writes the new — no clobber (dr118 vector 1, contingent on strip-only vacates).

## Why 1:1 now holds (post-fix scenarios; all dr118/dr118v3/dr118-final vectors resolved)
1. Draw A→seat1, A becomes governor: A's own site's UNCHANGED engine-role disqualifier relieves him (as it does
   today — this design does not touch that check, only extends its ACTION with `QING_post_release` at the 5
   repointed corps sites); picker bars him via the separate engine-role term until he leaves the governorship.
   No double-list. (No unified sweep needed for this — see the correction above.)
2. A routed into seat2 while holding seat1: stamp sees qing_current_post≠seat2 → dispatch-vacate seat1 first. 1:1 by construction.
3. A dies: on_death hook → family vacate → QING_post_release + holder clear. Gone from pool.
4. A CHI-employed post-holder leaves CHI's employ (no death — defection/exile/subject absorption): the
   corrected CHANGE 4 `on_move_country` hook (narrowly scoped to `scope:old_country = ROOT AND has_variable =
   qing_current_post AND NOT employer = ROOT`) fires `QING_post_release`. Not orphaned. (An amban/beg/march-GG
   posting or recall is a DIFFERENT transition — those 3 families never carry `qing_current_post` at all, so
   this hook is a no-op for them regardless of how often `on_move_country` fires for them.)
5. Study attendant becomes Salt Commissioner: salt fill's `QING_post_stamp` sees `qing_current_post` ≠
   southernstudy → dispatch-vacate strips the study marker (+ chief marker if held) BEFORE setting the new
   flag → NOT both (#77/#79 fixed, this time structurally). The Study recompute's outer iteration now reads
   `var:qing_current_post = flag:southernstudy`, which he no longer matches, so he silently drops off that
   roster next pulse too — redundant catch, no tautology (his OWN family's condition is what changed, not a
   blanket "holds any post" check).
6. Live save with unstamped incumbents (CHI-employed families only — see CHANGE 3): picker gate is still the
   marker-OR → un-drawable; the init sweep backfills qing_current_post so the dispatch driver works thereafter.
   amban/march_gg/xj_beg incumbents need no backfill — they were never in scope, and the marker-OR picker gate
   (unchanged, plus the one-line xj_beg addition) already covers them exactly as it does today.

## Fallback (per task, if impl proves intractable)
DISABLE autofill (seat unfilled, manual staffing) — NEVER mint. dr118 verdict: "NOT intractable — no need for the
disable-autofill fallback" once the 4 fixes are in.

## Validation / logging
Keep the existing >1-marker tripwire sweep (QING_council_recompute) as boot proof. Add LOG_line to
QING_post_dispatch_vacate (per relieve) + QING_post_stamp/_release. Static strings only (log-string-macro rule).

## Sequencing
Lands FIRST; gates #111/#113/#114/#116/#117/#119 (the create_character->draw-existing conversion cluster — the
real driver, per user ruling) and, as a side effect, structurally fixes #77/#79. Do NOT convert any autofill to
draw until the stamp/release/dispatch trio + the 10 net-new vacates (+ the 1 existing gc_office call) + the 10
stamp-insertion sites (v6 new section) + the init backfill + the corrected on_move_country release + the 5
relief-sweep site rewrites (v3/v6 CHANGE 1, corps sites only — SALT/CARAVAN excluded) are all in and this v6
design has passed a CLEAN independent review with ZERO findings (per standing rule — not "issues found and
fixed," an actual clean pass).
