# Reference — freekumquats fork vs Sobisonator upstream (divergence + pull assessment)

**Last surveyed:** 2026-08-06. **Purpose:** a standing reference so upstream-sync research isn't redone from
scratch each time. Records the remotes, the git gotcha that makes counts lie, how to compare correctly, and
the per-commit verdict on the commits our master was behind.

## Remotes (in this working copy)
| Remote | URL | Role |
|---|---|---|
| `origin` | github.com/freekumquats/imp19c | OUR fork (master = user-verified; merge-overnight = pushed candidate) |
| `sobiso` **and** `upstream` | github.com/sobisonator/imp19c | UPSTREAM (both remotes point at the same Sobisonator repo) |

Note: `sobiso` and `upstream` are duplicate remotes for the same URL. Use either.

## ⚠️ GIT GOTCHA #1 — this clone was SHALLOW; commit counts LIE until unshallowed
The clone had a `.git/shallow` graft. Symptom: `git log <upstream-branch>` shows only the tip commit with NO
parents, `git merge-base origin/master sobiso/master` returns EMPTY, and `origin/master..sobiso/master`
reports **1** commit when GitHub's compare view shows **16**. The tip is grafted with no ancestry, so git
can't walk history. **FIX (already applied 2026-08-06):** `git fetch --unshallow origin` (+ `git fetch sobiso
--deepen=200`). Verify with `git rev-parse --is-shallow-repository` → must be `false`. ALWAYS check this
before trusting any ahead/behind count.

## ⚠️ GIT GOTCHA #2 — commits are spread across MANY upstream branches, not just master
Only `sobiso/master` had 1 commit past the fork; the real work sat on other branches. Sweep ALL of them:
```
git fetch sobiso --prune
for b in master public-alpha unstable-shipping-and-trade Dr4GonFire; do
  echo "== $b: $(git rev-list --count <fork-point>..sobiso/$b) =="; git log --oneline <fork-point>..sobiso/$b; done
```
Live upstream branches seen 2026-08-06: `master`, `public-alpha`, `unstable-shipping-and-trade` (34 commits —
a big WiP shipping/trade-engine rework), `Dr4GonFire` (Artillery tree + Argentina, welded to a ~1M-line
map-data churn), plus stale ones (`luk-branch` 2022, `Robska-Branch` 2020, `cumlorduwu-master` 2021,
`pre_ranked_trade/experimental` 2024).

## ⚠️ GIT GOTCHA #3 — histories are RELATED but heavily diverged → cherry-pick, don't merge
`origin/master` and `sobiso/master` DO share a merge-base (`8b2043a0f`, 2026-07), but our tree has diverged
so much that most file-level diffs conflict wholesale (a whole-file `<<<<<<<`). A full `git merge` would drag
in unrelated content. Port fixes by `git cherry-pick -x <sha>` and resolve per-file; when the conflict is
just divergent surrounding content, isolate the commit's REAL change with
`git show <sha> -- <file> | rg '^[+-]' | rg -v '^[+-]{3}'` and hand-apply only that.

## Snapshot 2026-08-06
- Fork point (merge-base): `8b2043a0f`.
- `origin/master` head: `fe6c274a`.  `sobiso/master` head: `b78ccc1f6`.
- Our active work branch: `merge-overnight` (@ `438408552`), which is AHEAD of `origin/master` with the whole
  Qing meter-concretization program + much else (freekumquats has independently ported many upstream fixes
  into this line already — several of the "16 behind" were found ALREADY PRESENT).

## The 16 commits `origin/master` was behind `sobiso/master` — per-commit verdict
`x` = don't pull. Grouped by category.

### Already in our tree (freekumquats already ported them) — SKIP
| SHA | What | Evidence it's present |
|---|---|---|
| `d1b2bbe38` | Fix `LAND_transfer_provinces` bad `is_in_list` block-form trigger | our `se_LAND.txt:371-379` cites "Sobisonator d1b2bbe verbatim"; [[imp19c-macro-list-trigger-rule]] |
| `5fd01155a` | Add missing `input =` arg to `sqrt` call (GT_split import price) | our `se_GLOBALTRADE_split.txt:2702` already has `input =` |
| `45e15a2ea` | Guard `shortage.1` against impossible (empty) province | our `shortage_events.txt` already has `total_population > 1` guards |
| `86dec6cf5` | `DIPLOMATIC_RANGE 800 → 3000` (whole-world diplo) | our `00_defines.txt:465` already = 3000 (cherry-pick came up EMPTY) |
| `da0b54723` (partial) | Remove defunct setup-time `TRADE_reset_internal_trade_stockpiles` | our `oa_economy_setup.txt:2404/2425` already comment it out |

### Moot — a feature we DON'T have (custom peace window) — SKIP
`2076e4040` WiP custom peace button · `7452c7b3c` WiP replacement peace window · `f1e9ea04c` open/close peace
window · `803161819` final-offer button · `0a42ccea4` warscore GUI fix. Our `gui/imp19c_windows.gui` has
ZERO `peace_window_active_war`/warscore code, so these attach to nothing. `da0b54723`'s remaining bit (an
`any_war_participant = { this = scope:target }` fix) also lives inside the orphaned `imp19c_diplo_peace_button`
scripted_gui → not importable in isolation.

### ❌ UPSTREAM BUG — do NOT pull
| SHA | Claimed | Reality |
|---|---|---|
| `b78ccc1f6` | "Condense multiplication calls for `wealth_owed_for_$` from 2 to 1" | **NOT behavior-preserving.** Old: `wealth = order_size × unit_price × order_size_modifier`. New: `wealth = order_size × (unit_price + order_size_modifier)`. `order_size_modifier` is a **[0,1] market-access fulfilment fraction** (`GT_split_get_order_size_modifier_tradegood`, clamped to 1) that must SCALE wealth down — turning `× fraction` into `+ fraction` is arithmetically wrong and corrupts every trade-wealth calc. Rejected; our correct 2-multiply form kept. |

### Large content / feature bundles — NOT a safe cherry-pick (own decision if wanted)
| SHA | What | Note |
|---|---|---|
| `d6d9c3e31` | "WiP (#714)" | huge — COA/achievements/manufacturing/hundreds of files. A content wave, not a fix. |
| `11fd3438d` + `79cd96014` | Dr4GonFire merge: Artillery tech tree + Argentina flavour | renames `conscripts.txt`→`army_conscripts.txt`, adds inventions/heritages/modifiers we don't have. Feature bundle. |
| `80049ca31` | "Restore BOM to tooltips" (+ edits `00_Sudan.txt`) | cosmetic; we follow our own BOM convention ([[imp19c-bom-convention-rule]]). |
| `9629ea1f2` | "Restore vanilla unit type file overrides" | creates EMPTY `army_archers.txt` etc. to shadow vanilla units out — a design choice, and `11fd3438d` partly reverts it. |

## Bottom line (2026-08-06)
Of the 16, **zero were worth pulling**: 5 already present, 5 moot (peace-window), 1 an upstream bug, 4 large
feature/content bundles needing their own decision. The genuinely-valuable upstream work is on
`unstable-shipping-and-trade` (34-commit trade-engine rework, still WiP) — evaluate that branch specifically
if a trade-engine refresh is wanted; it is out of scope for a "safe fixes" sweep.

## How to re-run this survey
1. `git rev-parse --is-shallow-repository` → if `true`, `git fetch --unshallow origin` first (GOTCHA #1).
2. `git fetch origin --prune && git fetch sobiso --prune`.
3. `git log --oneline origin/master..sobiso/master` (and sweep other branches per GOTCHA #2).
4. For each candidate: `git show <sha> -- <file> | rg '^[+-]' | rg -v '^[+-]{3}'` to see the REAL change;
   check it isn't already in our tree (`git show HEAD:<file> | grep ...`) and isn't a disguised behavior change.
5. Cherry-pick with `-x`; resolve per-file taking OUR side where the change is already present.
