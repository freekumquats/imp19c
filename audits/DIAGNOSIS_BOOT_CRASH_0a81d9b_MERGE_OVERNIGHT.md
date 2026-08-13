# DIAGNOSIS — boot/load crash, range `0a81d9b79..merge-overnight`

## RESOLVED (2026-08-12, commit d91726097) — boot confirmed successful
**Root cause:** `common/laws/00_monetary_standard.txt` (commit 821b9b73e, "75: implement Monetary
Standard law group") gave `gold_standard_law` and `bimetallic_standard_law` each an
`ai_will_do = { base = N }` block. `ai_will_do` does NOT exist on a law-option's schema in this
engine — zero other law files in this repo use it, it never appears inside `common/laws/` in
either oracle repo (Invictus, Terra Indomita; it IS valid elsewhere, e.g. governor_policies, but
with a different sub-syntax, `modifier = { add/factor }`, never the decisions/missions-style bare
`base = N` form that was used here). Feeding that unrecognized field into a law-option's
field-dispatch desynced the engine's brace tracking, orphaning the file's own closing `}` so a
LATER, unrelated file's leftover brace got misread as the next lawgroup's NAME — producing the
literal `laws.cpp:184: Lawgroup '}' has no entries, this will cause crashes!` line seen ~20s
before the fatal `pdx_assert.cpp:612: Assertion failed: _nSize > 0`.

**Why the initial diagnosis (below) missed it:** the original 103-commit sweep scoped to
`0a81d9b79..merge-overnight`, which was ONE commit too late — the user later supplied a
more-precise last-good-boot log (`logs 2.18.32 AM.zip`, HEAD=`9677bdaa9`, confirmed clean via
`PostValidate` reached + hours of live gameplay in its log) that pinned the true error surface to
`9677bdaa9..merge-overnight`. The `#88`-focused sweep's best candidate
(`QING_wenzhi_suppress_jesuits`, trampolined in commit 6197eb70c) was a genuine, independently
code-reviewed fix for a real (if non-fatal-that-boot) scripted_gui compile-inline risk, but did
NOT resolve the actual crash — confirmed by a second crash on the identical signature after that
fix shipped. The real cause was found only after: (1) a byte-level good-vs-bad `error.log` diff
(not just reading each in isolation) surfaced `Lawgroup '}' has no entries` as the ONE genuinely
new error class between the two boots, and (2) a targeted 3-lens adversarial workflow specifically
hunting that error's mechanism, where one lens's `git diff 9677bdaa9 merge-overnight -- common/laws/`
found `00_monetary_standard.txt` was the only lawgroup file touched in-range and flagged the
schema-invalid `ai_will_do` field as the standout novel construct.

**Fix:** commit `d91726097` — removed both `ai_will_do` blocks. Code-review confirmed no
AI-selection regression (every other law in the mod, including this group's own default
`silver_standard_law`, already has zero author-supplied AI weighting — the engine's built-in
heuristic on standing modifiers is the only AI signal that exists anywhere in this mod's laws, per
`design/DESIGN_MO11_MO12_LAWS.md:15`).

## Original diagnosis (superseded — kept for record)

### Symptom (from the first boot test in this sequence)
- `Assertion failed: _nSize > 0` at `trait.cpp:158` (global trait-opposite-pair registration).
- Zero `PostValidate` lines in `error.log` — crash is before gamestate construction begins.
- `setup.log` dies at the same moment.
- Zero `IMP19C` debug breadcrumbs (consistent with a pre-script-execution parse/load failure).
- The `disgraced`/`completely_disgraced` trait pair (`2f2102125`) is RULED OUT — user confirmed
  a successful boot occurred with those traits present, so the true cause is a LATER commit.
- User has narrowed the error surface to the range `0a81d9b79..merge-overnight` (103 commits)
  and is certain the cause is in this range.

## Method
Full adversarial sweep, not a single hypothesis chase:
1. **Scan** — one subagent per commit (all 103), each given the full proven imp19c crash-pattern
   catalogue (create_character grant-to-just-made-char, scripted_gui compile-inline recursion,
   ownerless capital, setup char-id gaps, malformed comparison RHS, log-string `#`/macro
   corruption, gui.createwidget datamodel failures) and told to read `git show <hash>` in full
   and flag ANY plausible match, however weak.
2. **Verify** — 67 of 103 commits raised at least a weak flag. Each of those 67 went through an
   independent adversarial verification pass whose explicit job was to try to REFUTE the flag by
   finding a proven-safe precedent or showing the mechanism doesn't fit the pre-`PostValidate`
   phase. **All 67 were refuted** — every flagged construct had a byte-identical or
   structurally-identical proven-safe precedent already booting before this range, or the
   mechanism didn't match the parse-phase symptom.
3. **Round 2** — since nothing survived verification, three fresh-eyes lenses re-swept the
   *entire* range from scratch (not just the previously-flagged commits), per instruction to
   keep scanning until something plausible turns up:
   - **Traits/defines lens** — confirmed nothing. `common/traits/` has **zero commits** touching
     it anywhere in this range (the only trait-file changes are outside this range, already
     ruled out). `common/defines/00_defines.txt` only changes `MAXIMUM_GOLD`. Nothing here can
     reach `trait.cpp`'s global registration pass.
   - **Structural-corruption lens** — confirmed nothing. Quote-aware brace/quote-parity check
     across all 64 changed `.txt` files: zero imbalance introduced by this range. No new
     duplicate event/modifier/building IDs introduced by this range (2 pre-existing modifier-name
     dupes exist repo-wide but predate `0a81d9b79` untouched).
   - **GUI-chain lens** — traced every scripted_gui button added/changed in-range across all 8
     touched `common/scripted_guis/*.txt` files. No `raise_legion`/`create_unit`/call-cycle
     reachable from any changed button. **Surfaced one concrete candidate** (below) as the single
     structurally novel combination in the whole range.

## The one surviving candidate (unrefuted, but NOT boot-verified)

**`QING_wenzhi_suppress_jesuits`** — `common/scripted_effects/se_QING_WENZHI.txt:214-259`, wired
directly (no trampoline) from the Household panel button `qing_wenzhi_suppress_jesuits` at
`common/scripted_guis/QING_household_panel.txt:212-225` (`effect = { QING_wenzhi_suppress_jesuits
= yes }`). Introduced by commit `040d4897c` ("121/122: seed Castiglione as the Ruyiguan's Jesuit
court painter + Art Patronage panel").

**What it does, inlined directly into a scripted_gui button (compile-inlined at PARSE time, no
runtime guard):**
```
QING_wenzhi_suppress_jesuits = {
    every_character = { limit = { employer=ROOT is_alive=yes has_variable=qing_court_artist
                                   OR={culture=italian culture=portuguese} }
        remove_variable = qing_court_artist }
    set_variable = { name = qing_court_artist_count  value = 0 }
    every_character = { limit = { has_variable=qing_court_artist is_alive=yes employer=ROOT }
        ROOT = { change_variable = { name = qing_court_artist_count  add = 1 } } }
    if = { limit = { var:qing_court_artist_count < 5 }
        create_character = { age=30 culture=han religion=confucianism ... save_scope_as=... }
        scope:qing_new_court_artist_han = { set_home_country=ROOT set_variable=... }
    }
    ...
}
```

**Why it's the standout:** it is **two full-court `every_character` sweeps in sequence, plus a
conditional `create_character`, inlined directly into a button** (no `trigger_event` trampoline).
The nearest proven-booting sibling, `qing_wenzhi_commission_painting`, inlines only ONE
`every_character` + one `create_character`. This is a larger/denser inline chain than any prior
button in the codebase — a genuinely novel *combination*, not a single token that's individually
unprecedented. Per project memory's own hard-earned lesson (the two Study-panel crashes, the
personnel-panel crash), the actual discriminator for this crash CLASS has repeatedly turned out to
be **expanded inline size + iterator-nest pattern**, which static token-matching alone has failed
to predict before — it was only found by bisection each time.

**Why this is NOT a confirmed root cause, only a plausible one:**
- No `ordered_character`/sorting iterator here (the previously-catalogued depth-2 trigger) — both
  loops are non-sorting `every_character`, individually a proven-safe construct.
- The `create_character` here matches proven idioms elsewhere (culture=han literal,
  religion=confucianism literal, traits/stats set inside the block, only `set_home_country` +
  `set_variable` in the follow-up scope — all proven-safe per the #90 catalogue).
- It is *reachable only via a player button click*, not via `on_game_initialized` — so if this
  were the crash, it would need to be compile-inlined at PARSE time (which scripted_gui buttons
  are, regardless of runtime reachability) — mechanism fits, but no bisection has confirmed it
  actually blows the loader.
- Static analysis has been WRONG before about which specific construct in a "matches the family"
  bucket is the actual trigger (censorate's `ordered_character` was wrongly exonerated once,
  wrongly blamed another time) — this class of bug has never been reliably found by reading alone.

## Everything else checked and refuted
All 67 initially-flagged commits, refuted with specific proven-safe precedents. Categories that
were flagged and refuted (representative, not exhaustive — full list is in the workflow journal):
- Every `create_character` addition in-range (se_QING_COUNCIL, se_QING_EXAM, se_QING_MISSIONARY,
  se_QING_WENZHI ×2) — all set traits/stats inside the block, only safe ops (`set_home_country`,
  `set_variable`) in follow-up scope. Matches the proven #90-safe idiom exactly.
- The four new frontier-office picker buttons (salt/caravan/hoppo/opium rotate) inlining
  `QING_frontier_office_refresh_candidates`'s `ordered_character order_by=finesse` — byte-identical
  shape to `qing_canton_rotate_hoppo`, which is floor-proven booting since before this range.
- The `#`-in-LOG-string sweep commits (`70: log pass-4...`) — these commits REMOVED `#` characters
  from LOG strings, they didn't add any; net effect is corrective, not causal.
- `common/defines/00_defines.txt` MAXIMUM_GOLD change — pure numeric constant, no structural risk.
- All "112/111/116/117/119 design" commits — markdown-only, no code touched.
- `102: raise treasury cap` and its `EE_scripted_guis.txt` lockstep edits — pure numeric literal
  swaps (`99999` → `9999999`), no structural change.
- `93: fix construction-queue placeholder icons`, `87: real icon`, `96: widen panel widgets` —
  pure `.gui`/`.dds` asset references, no script logic.
- `106`/`107`/`108` unset-var-flood fixes and their revert/re-fix — all `set_variable`-seeding
  additions, no iterator/create_character/comparison-RHS risk.
- `115`/`112` regional pricing math changes — pure `script_values`/scripted_effects arithmetic,
  no parse-phase risk category matched.

## Recommendation
No commit in this range was confirmed as the cause by static/adversarial reading alone — this
matches the project's own standing lesson that this crash *class* (scripted_gui compile-inline)
has never been reliably pinpointed without bisection. The single unrefuted candidate
(`QING_wenzhi_suppress_jesuits`, above) is the best lead if a bisection or targeted disable/rename
test becomes available. No further static re-reading is likely to add signal beyond what three
independent fresh-eyes lenses already produced.
