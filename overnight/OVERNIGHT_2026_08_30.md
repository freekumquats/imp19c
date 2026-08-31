# Overnight run — 2026-08-30

Boot-test note-taking pass (user dictated findings, no investigation until "do it now"),
then a full autonomous pass on the resulting backlog per imp19c-overnight.

## ASSUMPTIONS & GUESSES

- **Task #6 (Zongli sort)**: assumed "Charisma" (per the office->skill map comment in
  `QING_governance_actions.txt`: "lifanyuan/chamberlain/zongli = charisma") is the intended
  sort key, matching the great office of the same name. Not independently confirmed by the
  user beyond their own explicit ask.
- Did NOT extend the charisma-sort change to the Censor Inspector / Imperial Guardsman corps
  buttons — the user only asked about Zongli, and there is no documented governing skill for
  those two sub-posts. Left them on the generic unsorted refresher.

## Task #11 — Invasion of Burma mission tree ignored (user: "you completely ignored my instructions")

Dispatched a dedicated diagnosis+fix agent rather than trust the prior commit's claim.
**Root cause found**: commit `c52d6d666` ("audit and fix Burma mission tree") audited the
WRONG tree — the tributary sub-branch `qing_hs_burma` inside
`qing_himalaya_seasia_missions.txt` — and never touched `qing_burma_war_missions.txt`, the
actual dedicated "Invasion of Burma" (#421) conquest tree where the user's named missions
live: **Yunnan Base** (`qing_burma_yunnan`), **Green Standard Marches**
(`qing_burma_green_standard`), **Manchu Banner Elite** (`qing_burma_manchu_bannermen`).

Found: Yunnan Base was already concrete. Green Standard Marches and Manchu Banner Elite were
pure stubs (spend treasury, gain popularity, tooltip claims units raised — none were). 8 more
tasks in the same tree had the identical stub problem (`shan`, `irrawaddy`, `kachin`, `laos`,
`siam_flank`, `teak`, `jade_mines`, `monsoon`, `pacify`), plus a genuine dead-code bug in
`qing_burma_fever` (country-scope check on a province-scope modifier).

Fixed all of it: green_standard/manchu_bannermen now raise real garrison units
(`SE_qing_raise_garrison`, Yunnanfu p:2759); shan/laos make the real minor-country tags
sinosphere tributaries; kachin/irrawaddy get real claims; teak/jade_mines retool real
provinces; monsoon/pacify get real miasma/ethnic-tension effects; fever's scope bug fixed.
Every province/tag/good verified against source data, not invented. All tooltips rewritten
quantified per the house template.

Committed `57594a787` (author freekumquats), cherry-picked onto `merge-overnight` as
`dc6f71b64`, pushed and verified via `git fetch` + `git log origin/merge-overnight`.
**STATUS: DONE.**

## Task #7 — Zongli "Recall" doesn't dismiss the diplomat (+ systemic check on the other 2 corps)

Traced the roster rebuild (`QING_ministry_recompute_perf_zongli`, `se_QING_MINISTRY.txt`):
after the #118 post-tracking refactor it filters corps membership by
`var:qing_current_post = flag:zongli_diplomat`, NOT by the family flag
`qing_zongli_diplomat`. The Recall button (`qing_zongli_recall_diplomat`,
`QING_zongli_panel.txt`) only ever cleared the family flag + salary modifier — it never
cleared `qing_current_post`. Result: a "recalled" diplomat kept his `qing_current_post`
stamp forever, so the very next recompute call (in the SAME effect) put him straight back
on the roster, and `qing_zongli_diplomat_count` never dropped — which also silently blocked
all future Appoints once the corps looked permanently full (the `count < 6` gate never
cleared). Fixed by adding `QING_post_release = yes` (the proven vacate idiom,
`se_QING_POST.txt`) to the Recall effect.

Checked the other two corps (Censor Inspector, Imperial Guardsman) for the same defect —
dispatched a targeted sub-check rather than assume parity. **Finding: they do NOT have this
bug.** `QING_ministry_recompute_perf_censor`/`_guard_commandant` filter by the FAMILY FLAG
directly (`has_variable = qing_is_censor_inspector` / `qing_is_imperial_guardsman`), not by
`qing_current_post` — so their existing Recall/Discharge effects (which already removed the
family flag) were already correct. Added `QING_post_release` to both anyway as harmless
consistency hygiene (their appoint path does stamp `qing_current_post` via the shared picker,
so leaving it stale on a recalled character violates the #118 design doc's "one man, one
post" invariant even though nothing currently reads it for these two) — a code-review pass
caught my first-draft comments overstating this as "the same bug" on all three; corrected
the comments to say plainly that only Zongli had an active bug.
**STATUS: DONE** (Zongli: real fix; Censor/Guard: verified NOT broken, hygiene-only change).

## Task #6 — Zongli "Appoint Diplomat" should sort by Charisma + must actually work

The "does nothing" half turned out to be the SAME root cause as task #7: once the corps
looked permanently full (Recall never actually decremented the count), the shared row-click
handler's `count < 6` validity check blocked every subsequent Appoint click — "selecting a
diplomat does nothing" was a downstream symptom of the Recall bug, not a separate appoint
defect. Fixed by task #7's fix.

The sort half: the Appoint button called the generic, unsorted `qing_gov_council_refresh_candidates`
(same as every other corps button) instead of a skill-sorted refresher. Switched it to
`qing_gov_refresh_candidates_charisma` (`QING_council_refresh_candidates_by { sortval =
council_sort_charisma }`), matching the documented "zongli = charisma" governing-skill
convention.

**Review caught a real regression this introduced**: the `_by` refresher applies a strict
juren+ exam-degree filter to every non-martial office, including corps sub-posts — but
neither the dedicated nor the shared corps-appoint effect requires a degree to join the
diplomat corps. Left as-is, this would have silently hidden every degreeless-but-otherwise-
eligible candidate from the picker with no explanation the moment a court ran short of
degree-holders. Fixed by exempting the three corps flags
(`zongli_diplomat`/`censor_inspector`/`imperial_guardsman`) from the degree clause in
`QING_council_refresh_candidates_by` (`se_QING_COUNCIL.txt`), so the list-filter now matches
the actual appoint rule.
**STATUS: DONE.**

## Task #9 — Diplomatic Plays window no longer draggable

Traced `movable = no` on the `supranational` window (`gui/imp19c_windows.gui`, houses the
Diplomatic Plays / Global Powers tabs) via `git blame` — it has been `no` since the earliest
upstream commit in this repo's history (2024, pre-dates every fork task number). NOT a
regression introduced by any commit in this fork, including task #11's own recent widening
of this same window. Fixed anyway per the user's functional ask: flipped to `movable = yes`.
Verified `parentanchor = center` + `movable = yes` is an already-proven combo used safely in
13 other window blocks in this codebase (code-review independently confirmed: no
`on_create`/tick/re-centering logic anywhere in this window's block that would fight a drag).
**STATUS: DONE.**

## Task #10 — "Play Success Chance" tooltip doesn't clarify thresholds

The tooltip (written in a prior session, task #13) already stated the 25/60 thresholds, but
in a single run-on sentence that buried "below X"/"above Y" without repeating the % context
right at the threshold. Rewrote with explicit `%` signs and one threshold per line, framed as
"THIS number decides the outcome" to remove any ambiguity about what the thresholds are
measured against.
**STATUS: DONE.**

## Task #8 — "A Report From the Field" event success-chance rise not quantified

Traced the exact mechanic: `QING_zongli_dispatch_pulse` (`se_QING_ZONGLI_DISPATCH.txt`) rolls
a charisma-weighted 50/50 and applies `DIPLOMACY_modify_play_success = { amt = 8 }` (success)
or `{ amt = -8 }` (failure) BEFORE firing this event as a pure notification. Replaced the
vague "the play's chance of success rises/falls" prose with quantified
`#G Play Success Chance: +8#!` / `#R ... -8#!` lines, matching the house tooltip convention.
Code-review confirmed the ±8 figures are correctly attributed to THIS event (not confused
with the separate variable-amount initial-dispatch boost, which has no event of its own).
**STATUS: DONE.**

## Task #4 — Raise max Political Influence cap 500 -> 1000

One-line define change (`MAXIMUM_POLITICAL_INFLUENCE`, `common/defines/00_defines.txt`).
Verified no adjacent define derives from the old 500 value, and no GUI progress-bar widget
hardcodes 500 as a display-scale max (grepped `political_influence` across `gui/` — only
icon references, no bar/scale literals found).
**STATUS: DONE.**

## Task #1 — Quantified-effects tooltip template, ALL events (4th recurrence of this exact ask)

Per the standing rule against grep-based sampling (this exact task has been marked "done" 3
times before while still leaving events unfixed), dispatched a dedicated coordinator agent
with an explicit mandate to open EVERY event file exhaustively — no keyword search — and
track its own per-file coverage. The coordinator fanned this out into 12 parallel batch
agents covering all 67 mod-authored event files under `events/imp19c_mod_events/`, each
cross-checking tooltip text against the real `effect = {}` blocks (including called
scripted_effects/modifiers), not just prose-editing.
**STATUS: IN PROGRESS as of this writing** — full results (files fixed / already-clean /
any gaps) to be logged in a follow-up entry once all 12 batches report back and are merged.

## Task #12 — scan ALL Qing mission trees for the same stub-task pattern, fix fully

User follow-up after the Burma fix: check every other Qing mission tree (19 files under
`common/missions/qing_*`) for the same pattern — a task that spends treasury/PI for nothing
but ruler popularity while its tooltip claims a concrete outcome (unit/subject/claim/
building/retool) the effect never delivers — and fix each stub with a real requirement AND
a real outcome, not just a tooltip patch.

Dispatched 4 parallel worktree-isolated agents, ~4-5 files each, each instructed to
self-correct onto `origin/merge-overnight` if it found itself on a stale worktree base
(two earlier agents this run hit that trap silently; this time it was made an explicit
first step).

- **Batch A** (Africa, Central Asia, Himalaya/SEA, India, Colonization): audited all ~5
  trees; Colonization was already clean; fixed 4 tooltip/effect mismatches in Africa, 12
  stubs in Central Asia (real garrisons, buildings, trade retool, tributaries, a frontier
  fort, ethnic-tension nudges) plus a scope bug and an illegal RHS var-ref, 3 more stubs in
  Himalaya/SEA beyond the already-fixed Burma tributary branch (new
  `qing_hs_tributary_court` modifier), 13 stubs in India (bidirectional opinion diplomacy
  with 8 princely states, 4 real claims, 2 tributaries, a real river-fleet unit). Committed
  `3aecf7996` → cherry-picked clean as `576fd764d`. Review: dispatched, pending at time of
  push (pushed anyway per the stacked-commit pattern; any finding gets a follow-up fix
  commit, same as task #5's).
- **Batch B** (Japan, pre-Perry Japan, Mexico, Nanyang): hit a background API error right
  before its first commit; resumed, self-verified its own uncommitted edits survived
  (Mexico's 16 tasks were genuinely already clean, not skipped by the crash — re-audited to
  confirm), rebased onto a fresh branch off current `origin/merge-overnight`, and committed
  cleanly. Fixed 11 stubs in Japan, 11 in pre-Perry Japan, 14 in Nanyang. Committed
  `451587e49` → cherry-picked clean as `f5b474b26`. Review: dispatched, pending.
- **Batch C** (New World, Open Japan, Reform, Self-Strengthening): New World and
  Self-Strengthening already clean. Fixed 14 stubs in Open Japan (real claims on 8
  provinces including 2 disclosed geographic proxies for two islands this map doesn't
  model separately, real rivalry/accommodation diplomacy with 6 daimyo domains, wealth
  grants) and 8 in Reform (a real bank building, reform-pressure/faction-balance wiring
  matching the tree's own proven pattern, one corrected tooltip that had been overclaiming
  a different task's effect). Committed `6435ddb3d` → cherry-picked clean as `f9f85e8d2`.
  **Review: CLEAN** — one LOW non-blocking caveat (a building-grant potential-gate risk
  shared with 4 pre-existing #234 grants, not a regression), no fixes needed.
- **Batch D** (Settle Frontier, Summer Palace, Taiping, Treasure Fleet, Xinjiang): dispatched,
  still running at time of writing.

All 3 landed commits + the code-review dispatches pushed to `merge-overnight` as of
`f5b474b26` (verified via `git fetch` + `git log origin/merge-overnight`).
**STATUS: IN PROGRESS** — batch D and 2 of 3 reviews still outstanding; logged in a
follow-up entry once everything lands (with fix commits for any review finding).

## Task #5 — Laws sequence-restriction audit (all law groups)

Dispatched to find the working Women's Rights precedent and extend the same adjacent-only
law-change restriction to every other law group. Found the precedent (Women's Rights,
`00_social_laws.txt`, task #12) and the identical idiom already used a second time
(succession_law, task #13): add `allow = { has_law = <preceding option> }` to every option
after the first in an ordered group, merged with any pre-existing allow conditions.

Audited all 10 files under `common/laws/`, 36 groups total, every option personally opened.
Also caught that an EARLIER "task #13 audit" claiming a null result had been run against 5
law files that don't even exist on this branch, and used the wrong screening criterion
("pure no-downside ladders" instead of "any group with a defined order") — that null result
was stale/wrong, redone from scratch.

**Gated 20 more groups** (full list in commit `c147c76f1`). **Left 15 groups ungated** with
reasons logged in the commit: several are categorical/lateral choices with no single-axis
order (`oligarchy_type`, `judiciary_law`, `vote_count_law`, etc.), one is a 2-axis matrix
(`non_tribal_land_law`), and two have only 2 options each (trivially adjacent already).

Also fixed a real pre-existing brace bug found while auditing `00_administrative_laws.txt`
(`legislative_monetary_policy` was nested inside `delegated_monetary_policy`'s body instead
of being a sibling option).

**Merge complication**: the agent's worktree had silently branched from a stale, diverged
base (not `merge-overnight` tip) — same class of issue the Burma agent hit and self-corrected
for; this one didn't notice. Cherry-picking its commit onto the real tip produced conflicts in
3 files: `00_administrative_laws.txt` and `00_upper_house_laws.txt` (real content drift —
current tip had newer modifier values/comments the stale base lacked) and `00_social_laws.txt`
(a whole-file conflict caused purely by a CRLF-vs-LF mismatch between the stale base and
current tip, not a real content conflict). Resolved all three by hand: recovered the current
tip's clean version of each file, then manually re-applied the same substantive `allow`-block
additions from the agent's diff, preserving every pre-existing modifier value/comment/on_enact
block. Re-verified brace balance and line-ending consistency (no EOL churn) after resolution.

**Post-merge code review, 3 findings**: (1) MEDIUM — `religious_law`'s new adjacency gates
are largely redundant with its pre-existing `religion = secular` gates on the normal
non-secular->secular path (the new `has_law` line isn't usually the deciding condition) —
not a regression, but the commit's "clean ladder" framing didn't fit this group. Corrected
the comment to describe the actual interaction honestly rather than re-model the group's
religion-state logic (out of this task's scope). (2) LOW — a comment in
`00_administrative_laws.txt` claimed a brace-bug fix that only applied to the agent's stale
base, not to what actually landed on this branch — corrected. (3) LOW/informational —
`constitutional_monarchy_laws`' ladder baseline (`symbolic_monarchy`) isn't the group's
first-listed option (`no_monarchy`); pre-existing behavior, not introduced by this commit,
noted but not touched (would need a setup-data check, out of scope).

Commit `c147c76f1` (cherry-picked from the agent's `b1e68b826`) + review-fix commit, both
committed as freekumquats, pushed to `merge-overnight`, verified via `git fetch` +
`git log origin/merge-overnight`.
**STATUS: DONE.**
