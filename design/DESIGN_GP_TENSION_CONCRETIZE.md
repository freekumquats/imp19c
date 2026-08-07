# DESIGN — `qing_gp_tension_*` — RETRACTED (not a valid concretization target)

**Branch:** merge-overnight. **Status:** ❌ RETRACTED 2026-08-06 after adversarial review. DO NOT BUILD.

## Why this doc was wrong

The original draft proposed (A) deriving a tension "base" from real diplomacy and (B) wiring a
"high-tension → rival launches a real play" mechanic as an unbuilt #91 item H. Adversarial review + code
verification found the doc rested on **false premises**:

1. **#91 item H IS ALREADY BUILT.** `QING_gp_rival_launch_play` (`se_QING_DIPLO.txt:769-821`): a rival GP
   whose `qing_gp_tension_$power$ >= 75` opens a REAL `AI_begin_diplomatic_play` (`play_instigator = c:$tag$`,
   `play_target_country = ROOT`, `play_goal = get_territory`) against a bordering Qing frontier province —
   cooldown-throttled (3650d), border-gated, fanned over all 3 rivals, called each pulse from
   `QING_gp_scan_plays:743`. Header: `[#91 item H] concretize the counter`. My earlier "never wired"
   grep searched for `start_diplomatic_play`/`create_diplomatic_play` — tokens that **do not exist in this
   engine**. The real launcher is `AI_begin_diplomatic_play` (`se_AI.txt:420`). The doc's proposed vehicle
   `DIPLOMACY_complete_play` is a play RESOLVER/teardown (`se_DIPLOMACY.txt:205`, ends in
   `AI_remove_diplomatic_play`) — the OPPOSITE of a launcher.
2. **The base-derivation is infeasible.** 3 of the 5 proposed base signals read triggers ABSENT in this
   engine: `is_in_diplomatic_play`/`has_diplomatic_play` (0 matches — plays aren't iterable engine objects
   here), `at_war`/`is_at_war_with` (0 matches), country-scope `is_rival` (only a CHARACTER trigger). Only
   `opinion` + sphere are readable.
3. **The one readable base signal is circular.** Tension itself applies `qing_gp_rivalry_opinion` to the
   rival's opinion (`se_QING_DIPLO.txt:215`); a base reading opinion would read back what tension set.
4. **A live play already raises tension** as a per-pulse nudge (`QING_gp_scan_plays:720-735`, `+3` when a
   rival's play targets the Qing) — deriving it too would double-count.
5. **Retargeting the ~25→actually-175 tension sites to a residual would strand the player's cooling levers**
   (accommodate/court/dispatch/partition — the 以夷制夷 system): with a persistent opinion-derived base,
   diplomacy could zero the residual yet tension stays pinned. The census was also a large undercount
   (175 occurrences; consumers at thresholds 15/25/30/35/55 the doc never listed).

## Correct assessment

`qing_gp_tension_*` is **MORE concrete than first triaged** and is NOT a clean concretization target:
- Its OUTCOME is already concretized (item H — real diplomatic plays launch off it).
- A live play already feeds BACK into it (the scan-plays nudge).
- The player's diplomacy levers already move it and work.
It remains a drift/summary COUNTER by design — which #91 explicitly intended ("the counter stays the
drift/summary layer; this hangs a live confrontation off it"). That is the accepted hybrid, not the
anti-pattern. **Reclassify: LEAVE (accepted hybrid, outcome already concrete).**

## Optional follow-up (NOT concretization)
If anything is worth doing, it's a small AUDIT of the already-shipped `QING_gp_rival_launch_play`: cooldown
length (3650d ≈ 10y), whether the AI actually pursues an `AI_begin_diplomatic_play` it didn't choose, and
the border-gate. That's tuning, not a meter rework. Low priority.
