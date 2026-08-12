# RETROACTIVE REVIEW — #114 amban post draws an existing banner laureate

**Status (2026-08-11): FIXES APPLIED, CLEAN.** #114 shipped this session (commit `06690b4b0`), already
passed its own implement→review→re-review cycle (2 rounds, final CLEAN). This doc records a SEPARATE,
LATER retroactive design-approach audit (requested alongside #111/#113's retroactive audits) and the two
follow-up fixes it produced.

## Verdict: shipped code is correct; findings are process + documentation hygiene, not bugs

The retroactive review confirmed:
- The final iteration-2 design (move `QING_amban_wire` inside the draw-success branch, no stale-scope
  guard) is not just correct but FORCED — no viable alternative exists. Restructuring
  `QING_amban_recall` to stop stripping `qing_amban_marker` (the naive alternative) would break FOUR
  other consumers (`QING_char_holds_court_position`, the deliberative-council picker, death-cleanup, the
  character-card title).
- The `qing_amban.4.a` treasury-charge gate (`qing_amban_here` discriminator) is correct for its context
  — event options execute atomically, no interleaving is possible.
- No correctness defect exists in the shipped code.

## Finding 1 (process, no code fix — recorded for future sessions)
The original iteration-1 bug (a stale-scope guard borrowed from #111/#113 by analogy, without
re-verifying its precondition — "nothing else strips this marker" — held at the new site) is a
repeatable failure mode: reusing a proven idiom without checking whether ITS PRECONDITION still holds
at the new site. A five-minute grep (`rg 'remove_variable = qing_amban_marker'`) would have caught it
before any code was written. #113 needed 3 review rounds for the same class of mistake (a duplicated
gate drifting from its own precondition). Recorded in [[imp19c-design-review-gate-mandatory]] territory
— no code action, a standing lesson for future idiom reuse.

## Finding 2 (FIXED) — `qing_amban.5` was genuinely dead code, left in the file with stale comments
Confirmed by whole-repo grep: zero `trigger_event = { id = qing_amban.5 }` callers anywhere — the
`#26`/`#62` picker migration rerouted all manual posting through `qing_amban.6`, orphaning `.5`.
**Fix applied**: deleted the `qing_amban.5` event block entirely from `qing_amban_events.txt`, replaced
its header comment with a note explaining the removal (so a future reader isn't confused by the sudden
absence), and corrected the one stale cross-reference in `se_QING_AMBAN.txt:326` (was
"qing_amban.5/.6 trampolines," now "qing_amban.6 trampoline"). Rationale for deleting rather than
leaving commented: a live `QING_amban_post` call inside dead code is a hazard — a future edit that
naively rewires a button onto `.5` would silently resurrect the un-picker'd auto-draw path.

## Finding 3 (FIXED) — `DESIGN_AMBAN_PICKER.md`'s R5 prescribed reintroducing the exact bug #114 removed
That doc's R5 ("BIGGEST LIVE RISK") recommended giving the amban picker a "raise a new resident" row
routed to the create_character fallback — the fallback #114 deleted as a standing-rule violation.
Anyone picking up that doc's Phase-2 work would have reintroduced the removed bug. **Fix applied**:
`DESIGN_AMBAN_PICKER.md`'s R5 section is marked SUPERSEDED, with an explicit instruction that any future
picker work on a narrow/empty bench must use the honest-empty-state pattern (matching every other picker
in the file), never a create_character fallback.

## Findings 4-7 (not fixed, informational — stale comments elsewhere in `se_QING_AMBAN.txt`, low severity)
Several pre-existing comments (predating #114, not introduced by it) now describe superseded machinery:
`QING_amban_wire`'s demotion-comment references "the fallback else below" (only one create site remains
now, `QING_amban_seed_one`); `QING_amban_post`'s header still says "Creates a character... stores the
link on CHI" (it draws now, and #113 moved storage to the subject); `QING_amban_recall`'s header
documents a `$reason$` param removed from all callers; `QING_amban_post_sweep`'s header says "at most
ONE posting per pulse" (superseded by #43's 1-3-per-pulse establishment loop). None affect correctness.
Left as a future hygiene pass, not urgent — flagging here so they aren't rediscovered as "new" bugs.

Also noted, unreachable today (outside #114's scope, no action): `se_QING_COUNCIL.txt:1564`'s
court-promotion strip clears `qing_amban_marker` but not the subject's `qing_amban_here` — currently
unreachable since GC pickers already exclude anyone holding a court position, but a latent gap worth a
comment if that exclusion ever changes.
