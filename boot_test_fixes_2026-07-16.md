# Boot-test fixes 2026-07-16 — decision log

Working through the user's reported boot-test issues on `1763_bookmark`. Decisions noted here as
taken. Standing rules in force: commits authored by freekumquats; push after each logical batch so
the user can boot-test on the other machine; proven idioms only (upstream vanilla Imperator /
Invictus / Terra Indomita — NEVER mod/Qing code as the reference); loc reads scopes BARE `[x.GetName]`
never `[scope:x]`, adjective is `[X.GetCountry.GetAdjective]` (see memory imp19c-loc-scope-syntax-rule).

## Ordered work list (as agreed with the user)
1. Deep scan: event localization vs proven oracles — align data-function idioms.
2. Mission Completion Criteria shows eligibility ("Play as Qing") not the completion goal.
3. Missing mission loc: qing_burma_war / qing_colonization / qing_central_asia / qing_himalaya_seasia.
4. Ministry of Rites table overlap — drop the parenthetical Chinese names on the 3 long labels.
5. Ministry of Works — Hydraulic Works: one row per building type under the header (not crammed/cut off).
6. Public Works buildings not shown in province view — add a "Public Works" building category.
7. Propose-a-Marriage window — rebuild as 3 sequential single-column pickers (country → own char → their char).
8. Religion — populate vanilla deities (Confucian/Buddhist/Taoist/folk) + Holy Sites.
9. Starving pops remain: Yulin, Taiyuan, Jinhua over capacity.
10. Migration Report filter shows only Nanchong.
11. (RESOLVED, no code) New Treasure Fleet = standalone tree #439, hub gating Pacific+Japan trees.
12. Eunuch characters — add real eunuch characters (on-map), not just the threat meter.
13. Rename "Censor-in-Chief" → "Grand Inspector" (loc).
14. USA coastal chain broken by #397 trim — restore seaboard SC/GA (Charleston 3082, Savannah 3400, …).
15. French Louisiana too small — give LSA its historical CONTROLLED extent (not merely-claimed interior).
16. Empty unowned US-area territory — historical check: more Native tags? match 1763 layout.
17. Spanish-America Napoleonic disruption arc + Qing intervention opportunity.
18. Colonise unowned land (incl. Pacific islands) via the vanilla colonization mechanic.
19. New Treasure Fleet tree not visible in the missions list — likely loc-key/registration mismatch.

---

## Decisions taken

### #2 — Mission Completion Criteria showed eligibility (DONE)
Oracle-verified: `_CRITERIA_DESCRIPTION` is the mission-level COMPLETION-GOAL summary (Invictus/TI:
"This mission will be considered complete when we…"), NOT the start/eligibility gate. The 15 Qing
trees wrongly put the eligibility text ("Play as the Qing (CHI), and X must exist") there. Rewrote all
15 to describe the completion objective ("This enterprise is complete when …"). Files: burma_war,
colonization, central_asia, india, himalaya_seasia, japan_preperry, japan, open_japan, reform,
settle_frontier, selfstrengthening, summer_palace, treasure_fleet, taiping, xinjiang.

### #3 — "Missing mission loc" (burma/colonization/central_asia/himalaya_seasia) — RESOLVED BY VERIFICATION
Checked all four: mission title key, _DESCRIPTION, _CRITERIA_DESCRIPTION, and every per-task key
(_tt/_desc/needs_*) are ALL present; BOM + `l_english:` header correct; fully populated (30/168/26/51
keys); no parse-breakers (no missing :N, no stray quotes). This was a STALE report — the keys were
added by the completed task #55 ("CRITERIA_DESCRIPTION showing raw"). No change needed.

### #4 — Ministry of Rites table label overlap (DONE)
Removed the parenthetical Chinese from the three long labels so they no longer overrun the value
column: "Candidates Awaiting Appointment (科舉候選)"→"Candidates Awaiting Appointment"; "Civil
Degree-Holders in Service (科舉出身)"→"Civil Degree-Holders in Service"; "Military Degree-Holders in
Service (武舉出身)"→"Military Degree-Holders in Service". (qing_rites_ministry_l_english.yml.)

### #13 — Rename Censor-in-Chief → Grand Inspector (DONE)
Replaced all 10 "Censor-in-Chief" loc occurrences (qing_censorate_l_english.yml) with "Grand Inspector".

### #5 — Ministry of Works Hydraulic Works layout (DONE)
Was a single crammed value "Dikes N · Depots N · Granaries N" that overran the right edge. Restructured
the GUI block (qing_works_ministry.gui) into a header + THREE indented per-type rows (Yellow River Dikes
/ Grand Canal Depots / Ever-Normal Granaries), each with its own count var. Added 3 label loc keys,
removed the obsolete `_HYDRAULIC_VALUE` key (no dangling refs).

### #6 — Public Works buildings not shown in province view (DONE)
Root cause: the province build view (province_window.gui:4044-4067) uses a CURATED per-type item list
(build_item_* types, name-matched via EqualTo_string in gui_templates.gui) — NOT an auto-enumeration —
so the 6 Board-of-Works buildings (real building defs in qing_works_buildings.txt + qing_granary_buildings.txt)
had no item type and never displayed, though they stood on the works roster. FIX: added 6 `build_item_qing_*`
types (dike/canal_depot/wall_section/granary/great_wall/grand_canal) cloned from the vanilla infrastructure
pattern (name-match on the building's loc key, verified all 6 name keys exist), and wired them into the
InfrastructureItems block. The buildings' own allow-gate keeps them appropriately placed. This IS the
"new Public Works category in the province view" the user asked for (grouped under Infrastructure).

### #1 — Event-loc data-function scan vs oracles (DONE)
Cataloged every `[X.Method]` head/method the mod's event loc calls; validated each against Invictus + Terra-Indomita loc (never against mod code). Findings + fixes:
- `[scope:X...]` → bare `[X...]` — already fixed prior commit (0 residual; scope: is script-only, absent from both oracles).
- `[ROOT.GetAdjective]` → `[ROOT.GetCountry.GetAdjective]` — already fixed prior commit (oracles always `.GetCountry.GetAdjective`).
- **NEW: `[trib_invest_vassal.current_ruler.GetName]` → `.GetRuler.GetName`** (qing_tribute.2.desc). `current_ruler` is script scope; the loc data function is `GetRuler` (oracles: 953 uses of `.GetRuler.GetName`, ZERO bare `current_ruler.` in loc). This was a live ERROR: in-game.
- `[qing_censorate_target.GetCorruption]` → added `|0` format specifier. GetCorruption IS a valid data fn (15 mod-GUI uses); bare is tolerated but numeric fixed-point should be `|0`. Low-risk consistency fix.
- Validated as CORRECT (no change): `.GetName` (206), `.GetCulture.GetName`, `.GetRuler.GetName` — all heavily used in both oracles.
Result: 0 residual loc antipatterns across all mod loc.

### PRIORITY INTERRUPT — new logs in ~/Downloads (user directive: fix log issues first)

Log is fresh (14:43) but the error.log is a MULTI-RUN ACCUMULATOR (312 distinct HH:MM:SS run-stamps;
per the stale-log rule the same file spans many boots incl. pre-fix ones). Triaged top signatures;
separated LIVE mod bugs from stale/pre-fix and inherited-framework noise:

**LIVE mod bug FIXED — `QING_DECLINE_granary_pool` operator flood** (se_QING_DECLINE.txt).
`Unsupported scope operator '<'` / `Unknown trigger type: value`. Root cause: the FILL/SHIP `limit`
comparisons used a TRIGGER (`has_state_food`, `has_state_food_capacity`) or a cross-scope `ROOT.var:`
INSIDE the comparison `{ value = ... }` RHS block, evaluated in `every_country_state` scope — the
parser can't resolve that and the whole effect aborted, so the ever-normal granary NEVER moved grain
(dead relief → likely why Yulin/Taiyuan/Jinhua still starve, item #9). This DISPROVES the old
se_QING_SPHERE:287 comment that claimed the `has_state_food < { value = ... }` form was silent.
FIX: precompute every operand into a plain STATE var first (set_variable can read the trigger /
ROOT.var: fine), then compare `var:stateX op { value = var:stateY }` — the SAME-SCOPE var-to-var form
that council/governance/canal/customs use with ZERO log hits (forensically confirmed silent). Added
6 per-state temps (cap/food/fill_thr/ship_thr/pool/poolcap), removed at loop end; also fixed the SHIP
clamp's `ROOT.var:` RHS. Brace-balanced.

**LIVE gui bug FIXED — `qing_personnel.gui:268` margin** — a plain `widget` root carried `margin`,
which it does not accept ("Property 'margin' not handled" → factory error at :266). Removed; the inner
flowcontainer already has margin. (Line 69 is a `margin_widget`, which DOES accept margin — left.)

**STALE, no change needed** (already fixed at HEAD e799a7c04, log entries predate it):
- `QING_tribute_receive` "Failed to fetch variable 'qing_trib_gift'" (384×) — HEAD already seeds the
  var to 0 before any read (init-before-read fix present + correct).
- `MARRIAGE_PLAY_seed_char_bonus` "Unknown trigger type: value" (315×) — HEAD line 184 already uses
  the silent `var:X >= { value = var:Y }` same-scope form (the e799a7c04 fix). Council/governance use
  the identical form with 0 log hits, confirming it's legal; these hits are pre-fix.

**INHERITED / framework noise (not mod-authored, left):** PROVINCE_TOOLTIP loc (10790), missing
`gradient_black_flip.dds` texture (7378), the `oa_wealth_changes`/`GT_split_*`/`EE_scripted_guis`
economy-framework script errors + sqrt `Illegal use of operator` (the economy-framework's own
local_var-on-RHS, tracked separately in the economy-audit backlog), map-locator bounding-box warnings,
COHORT_NAME_jurchen ordinal. These are upstream/framework, out of scope for this pass.
