# Design: character stat distribution for minted officeholders/commanders

## User request (verbatim, across 5 messages)

"the characters created during the GC auto seeding and garrison commander spawning are too
skilled on average. high single digits and low double digits should be the norm for
martial/finesse/zeal/charisma, not mid double digits" / "it should be rare for a character
to have more than one double-digit attribute" / "it should be common for characters to have
one or two low-to-mid single digit attributes, and only one double digit attribute" / "the
average character should have one low single digit attribute, two mid single digit
attributes, and one double digit attribute" / "and it should not be rare for the double
digit attribute to be replaced by a high single digit attribute"

Target profile, synthesized: per character, across the 4 attributes (martial/finesse/
charisma/zeal) — ONE low single-digit (1-3), TWO mid single-digit (4-6), and ONE "peak" stat
that is usually double-digit (10-12) but often instead high-single-digit (7-9). Having MORE
than one elevated (7+) stat should be rare.

## Diagnosis — the two NAMED mechanisms are NOT the source (premise is false as stated)

Three rounds of source investigation this run, tracing every character-minting site tied to
"GC auto seeding" and "garrison commander spawning" literally:

1. **GC auto-seed / backfill mint** — common/scripted_effects/se_QING_COUNCIL.txt:317-327
   (`QING_council_autofill_office`'s fallback mint, run both at boot day-32 seed and at
   runtime backfill when a draw-from-pool fails). FIXED literals, IDENTICAL every time:
   finesse=6, charisma=5, martial=3, zeal=4. No variance, no double-digit, ever.
2. **Garrison/banner commander "spawning"** — common/scripted_effects/
   imp19c_effects_legion_setup.txt. Confirmed NO create_character exists here at all.
   Garrisons/fleets are commanded by pre-existing STATIC setup characters
   (`cmd = char:NNN`, e.g. char:581 Fuheng, char:586 Songchun) or left commanderless.
3. **The static 1763 roster itself** (setup/characters/00_Qing.txt) — sampled + regex'd the
   whole file for any double-digit add_martial/finesse/charisma/zeal. Exactly ONE hit in the
   entire file: char:584 Hailancha, martial=10. Every other sampled character (Fuheng 8/7/8/4,
   Songchun 6/5/5/4, Langfu 5/5/5/4, Šuhede 6/8/6/4, Mingrui 9/4/5/3) is single-digit, and the
   spread is fairly flat (no character has ONLY one elevated stat and three low ones — most
   have 2-3 stats clustered at 6-9 simultaneously, which itself somewhat conflicts with the
   "only one elevated stat" target, but none reach the "mid double digit, multiple 10+" pattern
   the user described).
4. **The GC draw-from-pool (backfill) branch** — se_QING_COUNCIL.txt's `ordered_character`
   selection, pool = `employer = scope:qing_autofill_country` (ALL of CHI's adult employed
   characters), filtered to exam-degree-holders, `order_by = combined_stats_council_svalue`.
   This does not GENERATE stats — it picks the max of whoever already exists in that pool.

**Conclusion: the premise as literally stated is false.** Neither GC auto-seeding nor
garrison-commander spawning, nor the static roster feeding them, produces "mid double digit"
characters. The user is very likely observing a REAL symptom (double-digit GC/garrison
characters in actual play) whose actual SOURCE is elsewhere. Two candidates found, one fixed
this pass, one logged as blocked-on-data:

## POST-REVIEW CORRECTION (adversarial design review, `review-char-stat-design`)

The original Candidate A/B split above was WRONG and has been superseded. The reviewer
independently re-verified every citation and found:

1. **char:584 Hailancha (martial=10, setup/characters/00_Qing.txt:2077-2089) IS a garrison
   commander** — assigned to the Kashgar Banner Garrison at
   `imp19c_effects_legion_setup.txt:311`. The original doc named him as the sole double-digit
   static character and then failed to notice his own garrison assignment, wrongly concluding
   no double-digit source exists under "garrison commander spawning." **Verdict: no fix
   needed here anyway** — he is a SINGLE, one-time, historically-justified outlier (one peak
   double-digit stat, three low/mid stats: 10/4/5/3 — this is *exactly* the target shape, not
   a violation of it) and does not move an "on average" complaint. Left untouched, reasoning
   logged so it isn't re-flagged as an open gap.
2. **The real "GC auto-seeding produces too-skilled officeholders" mechanism is the RUNTIME
   BACKFILL DRAW, not the mint.** `se_QING_COUNCIL.txt`'s backfill path (`ordered_character`,
   `order_by = combined_stats_council_svalue`, i.e. picks the MAX of the eligible pool) draws
   from every CHI-employed adult character — a pool the mod itself keeps re-salting with
   fresh high-stat mints from several event chains. Because the draw always takes the single
   best candidate, these event-minted characters get preferentially seated into GC offices
   far more often than their raw numbers would suggest — this is the actual "too skilled on
   average" lever, hiding behind the word "auto-seeding" rather than in its boot-time mint.
3. **Candidate A's original target (`qing_roster_events.txt`) is provably the WRONG file.**
   That file is on a stated 0-9 scale (no double-digit stat exists anywhere in it) — rebalancing
   it cannot remove any observed double-digit character, and the proposed `{8 11}` peak range
   would have RAISED roughly half of its 21 named figures from 9 into 10-11, adding double-digit
   stats to a file that currently has none. This would have been a token/counterproductive fix
   (violates the standing "fixes must be visible, not token" rule) — **dropped entirely.**
   `qing_roster_events.txt`, `japan_bakumatsu_events.txt`, and `fra_revolution_events.txt` are
   anachronistic named-historical-figure spawns (a different, deliberate flavor mechanism, not
   what the user pointed at) and are explicitly left untouched.

### Corrected fix target — the actual pool-feeders that get preferentially drawn into GC seats

Three event files mint anonymous/generic (not named-historical) CHI-employed courtiers that
ARE eligible for the backfill draw and DO commonly carry an elevated peak stat with no
compensating low stat (every attribute sits at 4+, none in the 1-3 "low" band — this, not
peak height, is the actual shape defect):

- `events/imp19c_mod_events/qing_war_events.txt` — `qing_war.5` (3 create_character blocks,
  lines 488-517: martial 8/9/10, finesse 5-7, charisma 4-6, zeal 5-6) and `qing_war.6` (1
  block, lines 533-540: martial 8, finesse 6, charisma 5, zeal 5). Minted in country scope
  with no `set_home_country` override, so they default to CHI employment — bare fresh
  examination-graduate courtiers, directly poolable.
- `events/imp19c_mod_events/qing_keju_events.txt` — the laureate guaranteed-mint fallback
  (lines 207-216: martial 5, finesse 8, charisma 7, zeal 6, explicitly `set_home_country =
  ROOT` at line 217) and the "failed scholar" mint (lines 375-384: martial 6, finesse 9,
  charisma 8, zeal 7 — three stats simultaneously elevated), which reaches CHI employment via
  option `.4.b`'s `set_home_country = ROOT` (line 416).
- `events/imp19c_mod_events/qing_advisor_events.txt` — `qing_advisor.2`'s four field branches
  (lines 115-150: naval/army/fiscal/technical, each `set_home_country = ROOT` at line 152),
  each with one clearly dominant stat (finesse or martial 8-9) but no low stat.

10 create_character blocks total across these 3 files — a small, well-bounded, mechanical
edit, not the originally-scoped 64-block sweep across 6 files.

## Fix — rebalance the 10 pool-feeder blocks to the target profile

For each block: keep the ALREADY-correct dominant attribute (martial for war.5/.6 and the
military-field advisors; finesse for the keju civil mints and the fiscal/technical advisors —
no per-block judgment call needed, unlike the named-figure family, since each block already
has one unambiguous highest stat), convert it to the proven ranged form
`add_martial = { 8 12 }` (widened from the original `{8 11}` per reviewer's LOW finding —
`se_QING_COUNCIL.txt`'s "major" officeholder-effectiveness buffs gate on `>= 12`
(:1494/1526/1558/1596); capping at 11 would make that band permanently unreachable for every
mod-minted officeholder, which is narrower than the user's own stated "10-12"). Set ONE of the
three remaining attributes to a genuinely low value (2-3 — vary which attribute per block for
flavor, not always the same one) and the other two to mid values (5-6), replacing the current
"no low stat, everything 4+" shape. This directly targets the real defect (no compensating low
stat) rather than the peak height, which was already reasonable.

This is a mechanical, per-block edit across 3 files (10 create_character blocks) — no
shared/upstream logic touched, no engine capability risk (ranged create_character stat rolls
already proven at se_QING_EXAM.txt:296-299 etc). One code-review pass covers the whole diff.

## Probe — corrected anchor point

The original probe anchor (`QING_revenue_pulse`) was WRONG per review: it only touches the
single revenue minister, not all 9 GC officeholders. Corrected anchor:
`QING_council_apply_officer_buffs` (`common/scripted_effects/se_QING_COUNCIL.txt`), which
already runs `every_in_list` over `qing_council_members` on the same quarterly pulse cadence —
add a debug_log-gated (`-debug_mode` only) snapshot of each member's 4 attributes there. This
still cannot distinguish "drawn from a mod-minted pool feeder" from "drawn from an ordinary
vanilla-generated courtier" with full certainty (no persistent per-character provenance flag
exists), so it remains logged as a supplementary data point, not a confirmed second fix.

## Implementation record

Implemented exactly as corrected above:
- `qing_war_events.txt`: war.5's 3 blocks + war.6's 1 block, peak martial `{8 12}`, one
  attribute per block dropped to 2-4 (varied per block, not always the same attribute).
- `qing_keju_events.txt`: laureate fallback + failed_scholar blocks, peak finesse `{8 12}`,
  martial dropped to 2 in both (civil scholars, correctly low-martial by flavor).
- `qing_advisor_events.txt`: all 4 field branches, peak finesse (naval/fiscal/technical) or
  martial (army) `{8 12}`, one low attribute per branch. [review-fix: the naval branch's
  ranged stat was initially misattributed to martial — its true original peak was finesse=8,
  not martial=6 (`review-char-stat-fix` caught this LOW-severity doc/code mismatch); corrected
  to finesse before commit.]
- `se_QING_COUNCIL.txt`: probe added to `QING_council_apply_officer_buffs` (corrected anchor,
  genuinely iterates all seated GC members via the existing `qing_council_members` list),
  `save_scope_as` + `[scope:X.GetName]`/`.GetMartial`/etc — matches the only proven LOG_line
  character-interpolation idiom in this codebase (saved-scope bracket form; no precedent
  exists for a bare/PREV form, so that draft was corrected before commit).

Reviewed by `review-char-stat-fix` before commit — see review verdict logged in
overnight/OVERNIGHT_2026_08_17.md Task 3 write-up.

## BOOT-SEED EXTENSION (2026-08-17) — the day-32 GC + garrison seed batch

The prior fix (above) rebalanced the RUNTIME event pool-feeders. The user then clarified the
actual complaint: the **initial day-32 seed batch** (`qing_force_setup.12` — the deferred GC +
garrison seed, delayed off game-start to avoid the create_character construction crash class)
mints "a large number of characters" whose stats are too skilled *on average*. This section
extends the SAME target profile to that boot batch. User restatement (this session, verbatim):
"one low single digit, two mid single digit, one high single digit or low double digit" and
"exceptions should exist in both directions."

### Target (unchanged in spirit, this is the authoritative restatement)
Per character, across the 4 attributes: ONE low single-digit (1-3), TWO mid single-digit (4-6),
ONE peak that is high-single-to-low-double (7-12). The PEAK sits in the character's own DOMAIN
skill (a general is martial, a mandarin finesse, an amban charisma). Ranged rolls give natural
exceptions in both directions (a peak rolling 7 = a modest official; the low rolling 1 = a real
dud stat) — no explicit outlier engineering needed.

### The four boot-batch mints (all reached ONLY from qing_force_setup.12 at day 32)
1. `QING_council_autofill_office` (se_QING_COUNCIL.txt) — 13 GC offices. Was a flat, deterministic
   6/5/3/4 clone for EVERY seat (no peak, no low). Also feeds the runtime backfill, so the same
   edit fixes both.
2. `QING_subpost_fill_one_minted` (se_QING_SUBPOSTS.txt) — the Zongli-diplomat / Censorate-inspector
   / Imperial-guard corps (up to 12). Was flat 7/5/1/4; the martial Guard corps wrongly got a
   finesse peak.
3. `QING_exam_mint_scholar` (se_QING_EXAM.txt) — the Hanlin waiting bench (3/6/9 by law). Was flat
   7/5/1/4.
4. `QING_exam_mint_banner_laureate` (se_QING_EXAM.txt) — the spare amban banner-laureate bench (6).
   Was already ranged (cha{5 8}/fin{4 7}/mar{1 3}/zeal{2 5}) — the least broken; standardised.

### Key mechanic — degree-trait bonuses STACK on add_X, so the peak add is REDUCED to compensate
Displayed stat = engine base + `add_X` + degree-trait bonus. The exam-degree traits grant a small
skill bonus that reinforces the domain skill: jinshi +3 finesse, juren +1 finesse, wu_jinshi +3
martial, fanyi_jinshi +3 finesse +2 charisma (common/traits/00_imp19c.txt:241-440). Unlike the
event-family mints (no degree trait), these boot mints ALL carry a degree trait — so the peak
`add_X` is set BELOW the 7-12 band by exactly the trait bonus, landing the DISPLAYED peak in-band
instead of overshooting the 12 ceiling. For the amban laureate, fanyi_jinshi's secondary +3 finesse
is held down (finesse add {1 3}) so finesse does not rise into a SECOND elevated stat (the profile
wants exactly one). ASSUMPTION (same as the shipped event-family fix): engine base ≈ 0. If the
next boot's officer-buff probe (QING_council_apply_officer_buffs already logs every seated GC
member's 4 attributes under -debug_mode) shows systematic overshoot, the trait bonuses are the
first tuning lever.

### Chosen add_X bands (peak / low / two mid)
- Council civil (jinshi, +3 fin):   fin {4 9}  mar {1 3}  cha {4 6}  zeal {4 6}
- Council martial (wu_jinshi, +3 mar): mar {4 9}  fin {1 3}  cha {4 6}  zeal {4 6}
- Subpost civil (juren, +1 fin):    fin {6 11} mar {1 3}  cha {4 6}  zeal {4 6}
- Subpost martial (wu_jinshi, +3 mar): mar {4 9}  fin {1 3}  cha {4 6}  zeal {4 6}
- Hanlin scholar (jinshi, +3 fin):  fin {4 9}  mar {1 3}  cha {4 6}  zeal {4 6}
- Banner laureate (fanyi, +2 cha,+3 fin): cha {5 10}  fin {1 3}  mar {1 3}  zeal {4 6}

### Implementation shape
For the two MIXING macros (council, subpost — each serves both civil and martial degrees) the
stat spread is applied AFTER create_character, on the saved scope, inside an `if (has_trait =
wu_jinshi) / else` branch. A stat add on a saved scope is NOT a trait/modifier, so it is off the
#90 create-time crash class, and the whole path is the deferred day-32 event regardless. The two
single-profile mints (scholar = always civil, laureate = always amban) keep their add_X inside
create_character, just ranged to the bands above. The named-historical mints (QING_amban_seed_one,
the static roster) are a DIFFERENT deliberate mechanism and are left untouched — they already sit
at modest, reproducible, historically-pinned stats (fin 3-4 / mar 2-6) that match the profile.

### POST-REVIEW REFINEMENT (code-review MEDIUM, 2026-08-17) — council peak follows the GOVERNING SKILL, not the degree
The first council implementation branched the peak on the DEGREE TRAIT (wu_jinshi -> martial peak,
jinshi -> finesse peak). The code-review caught that this is WRONG for 6 of the 13 council offices:
`QING_council_score_office` (se_QING_COUNCIL.txt:420-433) scores rites/justice on ZEAL and
lifanyuan/chamberlain/zongli/grand_secretariat on CHARISMA -- so a blanket finesse peak left those
offices' real domain skill stuck in the 4-6 mid band. Concrete defect: the Grand Secretary "major"
officeholder buff gates on `chamberlain charisma >= 12` (se_QING_COUNCIL.txt:1544), permanently
unreachable if an autofilled chamberlain's charisma maxes at 6. The user's own spec ("the PEAK sits
in the character's DOMAIN skill") is met only if the peak follows the office's governing skill.

**Fix -- a uniform base + a domain-keyed booster (no if/else needed).** Every seat gets the SAME
base spread `add_martial {1 3} / add_finesse {1 3} / add_charisma {4 6} / add_zeal {4 6}`, then a
single `add_$domain$ = { 3 6 }` booster raises the office's own governing skill into the peak band.
`$domain$` is a new macro param passed by every one of the 26 call sites (13 boot + 13 backfill),
mapped EXACTLY to the QING_council_score_office table: personnel/revenue/works/censor = finesse;
rites/justice = zeal; war/guard_commandant = martial; lifanyuan/chamberlain/zongli/grand_secretariat
= charisma; chancellor = finesse (a civil generalist, scored as the average of all four so any single
peak nets to a mid average). The booster STACKS additively on the matching base line. The arithmetic
lands 7-12 for every domain because the degree-trait bonus lines up:
- finesse  (jinshi   +3): base 1-3 + booster 3-6 + trait 3 = 7-12  (non-finesse jinshi offices keep
  finesse at 4-6 MID via the +3 trait on the 1-3 base -- a clean second mid stat)
- martial  (wu_jinshi +3): base 1-3 + booster 3-6 + trait 3 = 7-12  (wu_jinshi grants NO finesse, so
  martial offices keep finesse at 1-3 LOW -- the correct off-domain weakness)
- zeal / charisma (no degree bonus): base 4-6 + booster 3-6 = 7-12

Every case is one PEAK (7-12), two MID (4-6), one LOW (1-3), keyed to the true domain. This SUPERSEDES
the "Chosen add_X bands" table above for the COUNCIL mint only (the subpost + exam mints keep their
bands: they have NO per-skill scoring gate, so no unreachable-buff defect exists there, and the
user's spec "a mandarin finesse" matches the juren finesse peak; forcing charisma on a juren would
break the two-mid shape given juren's mere +1 finesse -- a traced, deliberate scope call, not a defer).
