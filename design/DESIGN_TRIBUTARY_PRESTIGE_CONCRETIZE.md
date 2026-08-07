# DESIGN — Concretize `qing_suzerain_prestige` / `qing_tributary_prestige` from live tributary subjects (朝貢威望)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI. #91 item A (top of backlog).

## 0. Problem (verified)
Both are 0–100 accumulators — 26 `QING_DECLINE_nudge` sites, **no derive block**. Yet the concrete referent
is the mod's real tributary SUBJECTS (Korea/Vietnam/Ryukyu/Burma/Nepal, `subject_type = tributary` in
`00_default.txt`). Prestige should be a readout of the live tributary roster, not a hand-nudged number.

## 1. Thesis — TARGET+DRIFT from the live tributary-subject roster
`qing_suzerain_prestige` target ← derived each pulse from the real subjects:
```
set qing_suzerain_tally = 0
every_subject = { limit = { is_subject_type = tributary } ROOT = { change_variable = { name = qing_suzerain_tally  add = 1 } } }
# + weight for a high-value tributary (Korea), − for a lost/rebellious one
# scale to 0..100 → qing_suzerain_prestige_target; drift ±N/quarter (mirror ethnic_tension).
```
The 26 nudges keep moving the live counter (a diplomatic snub/tribute mission is a transient bump); the
target pulls it toward "how many tributaries actually still answer the throne." Losing Vietnam to France =
the roster shrinks = prestige falls, concretely.

`qing_tributary_prestige` (if distinct from suzerain — VERIFY they're not the same concept under two names)
folds into the same tally or is retired as a duplicate.

## 2. Consumers (unchanged): `se_QING_VASSAL.txt:204/209` (≥70/≤30), `se_QING_TRIBUTE.txt:343` (<35).
## 3. Feasibility
- **`every_subject` / `is_subject_type = tributary`** — VERIFY the exact idiom (memory `is_subject_of not
  recursive`; `any_subject`/`every_subject` proven). The subject-type test key must be confirmed.
- **1763 opening:** CHI starts with a full tributary roster → tally high → prestige opens HIGH (matches the
  High-Qing zenith; the seed is presumably high too — verify it doesn't spike vs the seed).
- Baseline-freeze may be needed if a static roster should read at a fixed prestige rather than max.
- Target+drift, `_cmpsvalue`, no residual store.
## 4. Checklist: derive suzerain target from `every_subject` tributary count; keep 26 nudges on the live
counter; verify tributary_prestige isn't a duplicate; consumers unchanged; 1763 opens at seed; review.
