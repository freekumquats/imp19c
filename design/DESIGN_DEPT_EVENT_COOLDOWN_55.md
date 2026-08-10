# DESIGN — per-department court-event stand-down (#55)

**Status:** design note, 2026-08-10. System-wide throttle correction. Design-note-first per the overnight rule → adversarial review → implement → adversarial review.

## The bug (user, boot-tested)
#34's per-governor fix stopped the Personnel "Clash" (qing_personnel.2) from repeating the SAME target, but the user still received SEVERAL Clash events in a row, and OTHER court events did not fire. The court felt like one department on repeat, not a variety.

## Root cause (confirmed in source)
The shared court slot `qing_gc_event_slot_used` (reset at the top of every quarterly pulse, 00_monthly_country.txt:80) already serializes the court to **at most one event per quarter** — every dispatcher gates on `NOT = has_variable qing_gc_event_slot_used` and claims it on its fire path. That part works.

The problem is **WHO wins the slot each quarter**. Dispatchers run in a FIXED order inside QING_GOV_pulse (se_QING_GOVERNANCE.txt), and the FIRST one that rolls a fire grabs the slot for the whole quarter:

```
425  QING_personnel_evaluate_governors   ← evaluated FIRST, ~10%/governor/quarter, MANY governors
429  QING_war_review_commanders
433  QING_censorate_pulse
436  QING_revenue_pulse                   ← HAS qing_revenue_event_cooldown (270d)
443  QING_works_pulse                     ← HAS qing_works_event_cooldown
446  QING_household_pulse
470  QING_wenzhi_pulse
476  QING_canton_pulse                    ← HAS qing_canton_*_cooldown (per-event)
519  QING_amban_evaluate                  ← HAS qing_amban_clash_cd (per-subject)
...  (frontier turf-war HAS qing_frontier_turfwar_cd 365d)
```

Personnel is evaluated FIRST **and has no department-level cooldown** — only the #34 per-GOVERNOR marker (qing_personnel_clashed_recently) + a 10% roll. With ~dozens of governors scanned per pulse, the probability that *some* governor rolls a clash each quarter is high, so Personnel re-wins the slot most quarters and starves every department below it. A different governor each time (so #34 holds), but always the same DEPARTMENT — the reported "several Clashes in a row, nothing else fires."

Revenue and Works already solved exactly this for themselves with a **department cooldown** (`qing_revenue_event_cooldown` = 270d ≈ 3 quarters at se_QING_REVENUE.txt:310-313; `qing_works_event_cooldown`). After either fires ANY of its events, the whole department stands down ~3 quarters, yielding the slot to others. Personnel/War (and others) never got one.

## The fix — generalize the department-cooldown pattern to every court-event department
Give each court-event DEPARTMENT one department-level cooldown var that ALL that department's dispatch rolls check AND claim, mirroring the proven Revenue/Works pattern. When any event of a department fires, that department stands down for ~3 quarters, so the shared slot rotates ACROSS departments (Personnel → War → Canton → Revenue → …), giving the player variety.

### Department cooldown convention
Each department dispatch gate becomes:
```
limit = {
    NOT = { has_variable = qing_gc_event_slot_used }        # the shared 1-per-quarter slot (unchanged)
    NOT = { has_variable = qing_dept_cd_<dept> }            # NEW: this department stood down recently
    ...existing department-specific triggers...
}
# on the fire path (after the roll succeeds), claim BOTH:
set_variable = { name = qing_gc_event_slot_used  value = 1 }
set_variable = { name = qing_dept_cd_<dept>  days = 270 }   # ~3 quarters (matches Revenue's 270)
```

### Departments + their cooldown vars (audit of the slot-claimers)
| Department | Dispatcher(s) | Existing dept cooldown? | Action |
|---|---|---|---|
| Personnel 吏部 | QING_personnel_evaluate_governors (se_QING_PERSONNEL.txt:153) | **NO** (only per-governor) | **ADD** `qing_dept_cd_personnel` |
| War 兵部 | se_QING_WAR.txt:152,170 (qing_war.1/.4) | **NO** | **ADD** `qing_dept_cd_war` |
| Revenue 戶部 | se_QING_REVENUE.txt (qing_revenue.1-5) | YES `qing_revenue_event_cooldown` 270d | keep (already correct) |
| Works 工部 | se_QING_WORKS.txt:58,85 | YES `qing_works_event_cooldown` | keep |
| Canton 粵海關 | se_QING_CANTON.txt:383,398,412 | per-EVENT (commend/venal/cohong) cooldowns, NOT a dept one | **ADD** `qing_dept_cd_canton` (an umbrella so the 3 Canton events don't all fire in consecutive quarters) |
| Household 內務府 | se_QING_HOUSEHOLD (eunuch), se_QING_HAREM | per-event (qing_eunuch_event_cd) | LEAVE — low chance, self-throttled; not a reported offender |
| Wenzhi 文治 | se_QING_WENZHI.txt:92 | one-shot flag (zenith) | LEAVE — one-shot, cannot spam |
| Frontier | se_QING_FRONTIER.txt:182 (turf war) | YES `qing_frontier_turfwar_cd` 365d | keep |
| Amban/Lifan | se_QING_AMBAN.txt:446 | per-subject `qing_amban_clash_cd` | LEAVE — per-subject already rotates; and #40 recall cd added |
| March 都護府 | se_QING_MARCH.txt (per-march) | per-march | LEAVE — already 1/march/quarter |
| Dynasty/Faction/Princes | se_QING_DYNASTY/FACTION/PRINCES | 20-25% chance, slot-gated | LEAVE — low chance; the family/faction beats are meant to be occasional and already lose most races to earlier departments |

### Scope of the actual change (minimal, targeted)
The acute offender is **Personnel** (first in order, no dept cd, many governors). The clear secondary gaps are **War** (multiple rolls, no dept cd) and **Canton** (3 events, only per-event cds). So the implementation ADDS a department cooldown to exactly those three: `qing_dept_cd_personnel`, `qing_dept_cd_war`, `qing_dept_cd_canton`. Revenue/Works/frontier/amban/march already self-throttle at the department or finer grain and are left untouched. The low-chance flavour rolls (dynasty/faction/princes/household/wenzhi) are occasional by design and are not reported offenders — left as-is to avoid over-suppressing the court into silence.

Cooldown length: **270 days (~3 quarters)**, matching the existing Revenue cooldown, so the convention is uniform. This means a department that fires stands down 3 quarters — with ~4-5 active departments that gives a rotation where the player sees a different department most quarters and each recurs roughly annually.

### Why not a single shared "last department" rotation table?
Simpler and lower-risk to reuse the proven per-department-cooldown idiom (Revenue/Works already ship it, boot-verified) than to invent a new rotation-scheduler primitive. Each department owns its own timed var; no central registry to desync. This is the [[gc-event-throttle-rule]] pattern extended, not replaced.

## Files
- se_QING_PERSONNEL.txt — add `NOT = has_variable qing_dept_cd_personnel` to the clash dispatch limit (:153-157) + `set_variable qing_dept_cd_personnel days=270` on the fire path (:166-173).
- se_QING_WAR.txt — add the gate + claim to BOTH rolls (:152, :170) using `qing_dept_cd_war` (shared across the two so an officer-review firing also holds the mil-exam roll for the department window).
- se_QING_CANTON.txt — add `qing_dept_cd_canton` gate + claim to the 3 event dispatches (:383/:398/:412), umbrella-ing the existing per-event cooldowns.
- No new files; no loc. All se_ files are no-BOM/LF.

## Traps / rules
- Claim the department cd ONLY on the fire path (after the roll/chance succeeds), never in the limit-eval — mirror the BT-28/#107 "claim only when it actually fires" pattern, so a no-op roll does not suppress the department.
- The shared slot claim stays exactly as-is; the dept cd is ADDITIVE (both must be free to fire; both are set on fire).
- Personnel is a per-GOVERNOR loop: the dept cd must be a ROOT (country) var checked/set on ROOT, NOT on the governor scope (the per-governor marker qing_personnel_clashed_recently stays on the governor; the NEW dept cd is on ROOT). Do not conflate the two.
- Timed vars (`days=270`) self-expire — no cleanup tick needed (proven idiom).
- se_ no-BOM/LF; brace balance; code-review before commit; freekumquats@users.noreply.github.com; merge-overnight.

## Verify (next boot)
- Over several years the court shows a MIX of departments (Personnel, War, Canton, Revenue, Works…), not Personnel on repeat.
- debug.log: after a Personnel clash fires, `qing_dept_cd_personnel` is set and no further Personnel clash fires for ~3 quarters; the slot goes to another department those quarters.
