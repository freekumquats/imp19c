# MO#8 — Mission-tree reshape (wide+shallow -> tall+deep) — design/plan (2026-07-29)

Branch: merge-overnight (worktree imp19c-mo). Boot-test finding #8: expanded trees (#127/#129) laid
out as one root with a dozen+ direct children (flat fan-out); desired = deep chains (2-4 children/node,
successive layers, converging capstone).

## Root cause (verified)
- Layout is 100% engine-computed from the `requires` DAG. NO `position` field exists anywhere in
  common/missions/*.txt or common/military_traditions/*.txt. gui/mission_view.gui (254-300) reads
  engine coords ([MissionLineItem.GetPosition]/[MissionTaskItem.GetPosition]). Depth = requires-chain
  length; width = siblings sharing a parent. Nothing to hand-position — fixing `requires` re-lays out.
- Mechanical cause: tools/gen_mission_tasks.py:58 hard-codes every generated task's
  `requires = { <tree parent-root> }`, so all breadth tasks became direct children of the root.

## Scope
- AFFECTED (14 files, common/missions/qing_*.txt): burma_war, central_asia, himalaya_seasia, india,
  japan, japan_preperry, nanyang, open_japan, reform, settle_frontier, summer_palace (worst: 17 flat,
  no real capstone), taiping, treasure_fleet, xinjiang.
- NOT AFFECTED (already deep/narrow, no change): qing_colonization_missions.txt,
  qing_selfstrengthening_missions.txt, and all 7 common/military_traditions/*.txt (manchu_shiquan /
  napoleon_grande_armee are the proof-of-shape exemplars).

## Target shape — DERIVED FROM UPSTREAM (Invictus + Terra-Indomita), per user directive
Measured the requires-DAG topology of every upstream mission tree >=15 nodes (Invictus 58 trees;
Terra-Indomita 52 trees), comment/brace-aware, intra-file requires only:

  metric              INV median(mean)   TI median(mean)
  root fan-out        4 (4.6)            4 (4.4)
  max depth           5 (5.7)            5 (5.4)
  multi-parent nodes  3 (3.6)            3 (3.1)

=> CANONICAL TARGET per tree: root fan-out ~4 (cap ~7), max depth >=5, >=3 reconvergence (multi-parent)
nodes. Our 14 broken trees sit at rootfan 12-18 / depth 2-4 — clear outliers. Healthy mod trees
(colonization rootfan7/depth5; military_traditions) already sit in the upstream band.

Exemplar idiom (TI 01_diadochi_empire.txt: nodes=31 rootfan=7 depth=6 multiparent=4): a few branch
heads (empty requires), each a depth-3-6 chain (fan-out 1-2), periodic multi-parent reconvergence —
e.g. `diadochi_school_of_x requires={ ...art ...gods }`,
`diadochi_imperial_capital requires={ ...crown_egypt ...two_rivers ...invictus_1 }`. Multi-key
`requires` AND-semantics is the upstream reconvergence mechanism (mod already uses it: qing_con_draft
requires 2). Invictus 01_Albion_missions.txt (69n, rootfan9 depth11 multiparent12) is a larger example.

## Actual current state (extracted, NOT the stale hand-table)
The earlier per-tree hand table has >=1 stale claim (himalaya qing_hs_capstone is NOT orphaned — it
already has requires={ himalaya_ring indochina siam ... }). So the rewire MUST be built off each
tree's TRUE current requires graph (extracted), validated as a DAG, targeting the upstream numbers
above — not applied verbatim from the hand table.

  burma_war       26n root=qing_burma_mobilise         flat=12
  central_asia    26n root=qing_ca_beyond_pass         flat=14
  himalaya_seasia 26n root=qing_hs_lifanyuan           flat=13  (hs_capstone already multi-parent)
  india           26n root=qing_india_descent          flat=16
  japan           26n root=qing_jp_open_relations      flat=13
  japan_preperry  26n root=qing_jppre_nagasaki_channel flat=12
  nanyang         26n root=qing_nanyang_champion       flat=16
  open_japan      26n root=qing_openjapan_arrive       flat=16
  reform          26n root=qing_con_bureau             flat=13
  settle_frontier 26n root=qing_settle_policy          flat=13
  summer_palace   26n roots=qing_sp_yuanmingyuan+qing_sp_qingyi flat=18 (worst; no true capstone)
  taiping         26n root=qing_hk_channel             flat=13
  treasure_fleet  34n root=qing_treasure_revive_yards  flat=15
  xinjiang        26n root=qing_xj_governorship        flat=16

## Fix = requires-only edits (ZERO new mission keys, ZERO new content)
Per-tree edit tables (full list from the investigation) — each re-parents the flat leaves into 3-4
sequential chains and folds each chain's tail into an existing capstone's requires. All named head/
chain/capstone keys VERIFIED to already exist (spot-checked burma: all present).
[See investigation report / task #159 for the complete per-tree requires table — 14 trees.]

Key structural fixes beyond simple chaining:
- himalaya_seasia: qing_hs_capstone currently `requires={}` (ORPHAN) -> wire to 4 branch tails.
- summer_palace: no true capstone -> designate existing leaf qing_sp_grand_garden as convergent
  capstone (requires 4 chain tails + existing yiheyuan mini-branch). No new node.

## Implementation approach
- Generated tasks (owned by gen_mission_tasks.py): the CANONICAL fix is to add a per-task chain-parent
  field to tools/mission_task_content.py's T rows and change gen_mission_tasks.py:58 to emit that
  instead of the fixed root, then REGENERATE — idempotent, matches the canonical-generator rule.
- Hand-authored capstone/mid-tree nodes (NOT generator-owned): their `requires` lists are edited in
  place to fold in the new chain tails.
- Verify after: no cycles, every requires target exists, every node reachable from root, exactly one
  capstone per tree, root fan-out <=4, max depth >=5 on the 14 trees.

## Risks
1. Cycle introduction (A requires B requires A) -> tree fails to load / mission unreachable. Mitigate:
   post-edit DAG validation (topological sort must succeed).
2. Orphan (node not reachable from root) -> invisible mission. Mitigate: reachability check from root.
3. Capstone left with a dangling requires target (typo'd key) -> load error. Mitigate: every requires
   token must match a declared key in the same tree file.
4. Generator drift: if I hand-edit generated tasks but DON'T update the content table, a future
   regen reverts the fix. Mitigate: encode chain-parent in the table (canonical path).
