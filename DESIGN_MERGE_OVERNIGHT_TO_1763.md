# Merge: `1763_bookmark` → `merge-overnight`  (execution record + promotion path)

**Status: the merge is DONE** (commit `7175b83f4`, on `merge-overnight`, not yet pushed).
This document records what was merged, how the conflicts were resolved, and the remaining
steps before the union can be promoted.

> **Direction note.** The user chose to merge **1763_bookmark → merge-overnight** (fold the
> recent 1763 playtest/GUI fixes *up* into the big feature branch). `merge-overnight` remains
> the integration branch; `1763_bookmark` is untouched by this operation.

---

## 1. Why

`merge-overnight` carries the large net-new Qing subsystems (the ministry panels, tributary
system, Canton system, 文治 patronage, silver reserve, amban seed, the border rebase, and the
23-finding deep-review fix batch `49a04c3d7`). `1763_bookmark` carries 9 more recent commits —
playtest bug fixes BT-47…BT-64 — that never reached the feature branch. Merging brings the two
lines of work into one branch that can be boot-tested together before any promotion to
`develop`/`master`.

## 2. Topology at merge time

- merge-base: `66421aa70` (BT-39 per-province sinicization marker + BT-44)
- `1763_bookmark`: **9 ahead**, 80 behind → the 9 commits folded in:

  | commit | fix |
  |---|---|
  | `6f35dbcc7` | BT-53 religion-panel sentinel textbox (diagnostic) |
  | `eec8490fc` | BT-49 heir titled 皇太子 (Taizi), culture-scoped |
  | `c2eac97de` | BT-48 + BT-58b throne-card loyalty/statesmanship swap + subject tribute-to-bottom |
  | `58f4768e5` | BT-57 minister-vs-governor clash under the court event throttle |
  | `b529a3b13` | BT-47 shrink throne-card skill cells |
  | `64a110cad` | BT-58/59 restore subject loyalty bar + loyalty-breakdown overlap |
  | `e0e07000e` | BT-56 sinicization report per-province trend marker |
  | `39ddaf7c4` | BT-51/54/55 Dynastic Health colours, PI-cost tooltips, migration report order |
  | `02ce33b78` | BT-63 add_loyalty raw-int ladder + BT-64 sphere illegal-operator |

- 154 files changed only on the overnight side (clean), 4 only on 1763, **18 touched on both**
  (of which 14 auto-merged cleanly; 4 conflicted).

## 3. Conflicts and how they were resolved

| # | File | Nature | Resolution |
|---|---|---|---|
| 1 | `common/loyalty/00_imp19c_loyalty.txt` | **add/add** — both branches added this file with the *same* `add_loyalty` named-modifier ladder (1763 via BT-63, overnight via #371). Byte-identical modulo BOM/CRLF. | Kept **ours** (merge-overnight's CRLF copy). No modifier lost. |
| 2 | `common/scripted_effects/se_QING_DYNASTY.txt` | Both sides made the *same* `add_prestige → add_popularity` change (BT-5/6). HEAD had the fuller comment. | Kept **HEAD** (same code, fuller comment). |
| 3 | `events/imp19c_mod_events/qing_dynasty_events.txt` | Same as #2, two hunks (`qing_dynasty.8` options a/b, dowager popularity). | Kept **HEAD** (both hunks). |
| 4 | `common/scripted_effects/se_QING_PERSONNEL.txt` | **Real divergence.** HEAD had an un-throttled per-governor `random{ chance=10 → qing_personnel.2 }`; 1763 had **BT-57**, wrapping that roll in the shared court-event-slot guard (`qing_gc_event_slot_used`, the BT-28 pattern) so the per-governor loop can't spam clash events in one pulse. | Took **1763 (BT-57)** — strictly the newer, safer version. |

**Key non-issue clarified:** the loyalty-file "conflict" was NOT a content divergence — the two
files differ only in line endings (overnight = CRLF, 1763 = LF; both carry a BOM). The two
branches independently authored the identical 231-line ladder to fix the same bug (`add_loyalty`
given a raw integer is a silent no-op — the engine wants a named loyalty modifier). Likewise
**BT-64 (sphere illegal operator) now exists identically on both sides** — 1763 via `02ce33b78`,
merge-overnight via the deep-review batch `49a04c3d7`. That duplication is why the earlier
grep-gate recommendation mattered; both copies are equivalent.

## 4. Post-merge verification already done

- No conflict markers anywhere in `common/ events/ gui/ setup/ localization/`.
- Brace balance = 0 on all 4 resolved files **and** every file the merge changed.
- All 9 folded commits confirmed ancestors of HEAD.
- Spot-checks survived the auto-merge: the 3 corps-picker bridges + 26 office-picker bridges in
  `government_view.gui`, the sphere fix (`qing_sphere_top_val`), the BT-57 throttle
  (`qing_gc_event_slot_used`) in personnel, and the deep-review batch intact.
- Backup ref `backup/merge-overnight-pre1763` = `49a04c3d7` (pre-merge tip; revert target if needed).
- Independent code-review agent run over the 4 conflict seams (STRICT PRE-COMMIT REVIEW rule).

## 5. Remaining path to promotion (NOT yet done)

1. **Boot-test the union** — this exact combination has never run. Launch the 1763 start, then
   read `~/Downloads/debug.log` + `~/Downloads/error.log` (per the standing log-location rule;
   error.log is a multi-run baseline — check line timestamps against this merge, don't treat old
   lines as live). Watch specifically for: the ministry corps appoint path, the four-power sphere
   (BT-64), tributary gold transfer (T1-C), and the personnel clash throttle (BT-57) interacting
   with the overnight ministry perf recomputes.
2. **Resolve the two still-open 1763 task threads** (they came in with the merge):
   - `#391` — BT-25→BT-46 boot-test findings (pending).
   - `#378` — BT-22/23/24 three empty province reports (in_progress).
   These are now on `merge-overnight`; decide whether to clear them before or after the boot-test.
3. **Push** `merge-overnight` once the boot-test is clean.
4. **Promote** only when the user has verified in-game (branch policy: `develop` = pushed testing
   candidate; `master` = user-verified). Do not fast-forward `develop`/`master` unprompted.

## 6. Rollback

```
git reset --hard backup/merge-overnight-pre1763   # undo the merge on merge-overnight
```
The backup ref is local-only; it is the merge-overnight tip as it stood immediately after the
deep-review fix batch and before this merge.
