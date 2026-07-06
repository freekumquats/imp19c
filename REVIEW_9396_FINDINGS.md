# #93-96 Deep Review — Developer Action List (extracted from workflow w7iipeldq)

*Source: the review workflow's own final synthesis (result.synthesis + result.ranked), extracted
from the run summary. 39 agents, 6 candidates → 5 ranked survivors + 2 new gaps from the
completeness critic. This is the authoritative finding set (supersedes the reconstructed summary).*

## MAJOR

### M1 — Boshin: Tosa (YCH) & Saga (SGA) can never be released
`se_JAPAN_BOSHIN.txt:103` (call sites :130-131). Their `domain_sonno` seeds at 15/12
(se_JAPAN_BAKUMATSU.txt:84-85) and is nudged by NO code path, so the `>= 45` release gate is
permanently false; `JPN_boshin_execute`'s release calls for YCH/SGA always hit LOG_fail. The two
tozama named in the design header (:114-118) never become independent Boshin objects.
**Fix:** add YCH/SGA to the `domain_sonno` nudge paths (mirror CSU/SHZ in pulse drift + beats), or
lower/relativize the release gate for the tozama tier.

### M2 — USA: meter-driven secession climax unreachable on historical path
`se_USA_SECTION.txt:254`. `usa_free_states` can never exceed `usa_slave_states`: both seed 11, and
the only nudges (Missouri +1/+1, Texas-annex slave+1 @91% odds, Comp-1850 free+1) yield 13/13 on
the dominant path, so the strict `var: > var:` gate is false forever. Secession fires ONLY via the
`current_date >= 1861.4.1` fallback — meters have zero effect on timing, defeating the structural
trigger.
**Fix:** re-balance so a fully-radicalized Union can trip free>slave before 1861 (add a free-state
admission nudge to a Northern beat, or gate the climax on the reachable tension/party meters),
keeping the date as a true fallback.

### M3 — Japan: `baku_grip_*` band frozen out of sync after Meiji retag
`se_JAPAN_BOSHIN.txt:149`. The pulse applies the authority band before the climax; `execute` then
overwrites `baku_legitimacy = 5` and retags TKG→JPN. The pulse on-action gates on `tag = TKG`, so
apply_bands never re-runs — the last band (`broken` on the meter path, `firm` on the date-fallback
path) is stranded on Meiji Japan forever, with no code path to clear it.
**Fix:** in `JPN_boshin_execute`, remove all three `baku_grip_*` bands after setting legitimacy /
around the retag; do not rely on the TKG pulse to reconcile.

### M4 (NEW — GAP A) — Mexico: "Union reconquered the CSA" empire-fall trigger is dead
`se_MEXICO.txt:457` (root cause se_USA_SECTION.txt:343). `global_var:usa_csa_country` is set once
and removed nowhere, so `MEX_empire_fall_check`'s reunification branch
(`NOT = { exists = global_var:usa_csa_country }`) can never be true — the Second Empire only ever
falls on the 1867 date. The stale global also leaves a dangling handle that later consumers
(se_QING_USCW.txt:91) may act on after the CSA is gone.
**Fix:** `remove_global_variable = usa_csa_country` when the reconquest war is won / the CSA is
annexed, so the reunification-fall branch and recognition consumers see an accurate map.

## MINOR

### m5 (survivor #5, EXPANDED by GAP B) — "Prop the Second Empire" pays out on THREE entry points
`qing_colonization_missions.txt:1102` (+ :1213-1219) and `qing_mexico_adventure_events.txt:47`. No
shared guard across (a) `qing_mexico_adventure.1` "Prop", (b) `qing_col_maximilian` on_completion,
(c) `qing_col_mexican_empire` on_completion. A human CHI collects ~150k wealth + up to +85 prestige,
provokes Britain twice, betrays the US entente twice. Name-unique crown modifiers don't stack, but
wealth/prestige/GP-tension are additive one-shots.
**Fix:** one shared idempotency flag (e.g. `qing_mexico_propped`) set by whichever path fires first
and checked (`NOT = has_variable`) by all three before granting the wealth/prestige/GP package.

### m6 (survivor #3) — Tosa (YCH) domain milestone gate is dead code
`se_JAPAN_BAKUMATSU.txt:187`. `c:YCH = { var:domain_sonno >= 55 }` can never be true (YCH frozen at
seed 15). Harmless in practice (Ryoma also spawns via japan_bakumatsu.5, and YCH's sonno_committed
is never read), but a permanently dead gate. Resolved as a side-effect of M1's YCH nudge fix.

## Untraced flows the critic flagged for a second pass (no confirmed defect)
1. Patron-withdrawal / CHI-collapse leaving `mex_empire_defended` with a dangling patron and no
   fall check.
2. Timing of se_QING_USCW recognition vs. CSA defeat (compounds M4).
3. `USA_section_init` re-entrancy (does re-seeding clobber accumulated nudges? — compounds M2).
4. Modifier-lifecycle across `change_country_tag`/`change_government` in the USA/Mexico subsystems
   (beyond the Japan M3 case).
