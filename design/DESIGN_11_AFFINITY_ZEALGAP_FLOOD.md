# DIAGNOSIS + FIX — #11 QING_char_affinity Script-system-error flood

## Status of the FIRST diagnosis: REFUTED (kept below for the trail)

The first pass blamed the zeal-gap cross-scope ARITHMETIC (`subtract = root.current_ruler.zeal`
"poisoning" `qing_aff_zeal_gap`) and proposed gating it on `root.current_ruler = { zeal >= 0 }`.
An adversarial review (task a91e393fac723ad5d) refuted that, and the refutation is sound:

1. **No "set-but-dead" tri-state.** Jomini variables are two-state (set / unset). If
   `set_variable ... value = zeal` (line 79) succeeds, the var holds a valid number; a later
   failed `change_variable` logs an error but leaves the PRIOR valid value — it cannot create a
   var that is `has_variable`-true yet dead. So the proposed cascade (82/87 throwing *because* 80
   corrupted the var) is not a real engine state.
2. **The proposed gate is a TAUTOLOGY → the fix was a no-op.** `root.current_ruler = { zeal >= 0 }`
   would sit INSIDE the existing `exists = root.current_ruler` guard (line 64). A live ruler's
   `zeal` is always a number ≥ 0, so the new trigger is always true when reached and skips nothing.
3. **The log is STALE (pre-#8-split).** It names `qing_canton.2.a → QING_censorate_impeach_uphold`.
   On disk `qing_canton.2` has NO option `.a` — the #8 split (commit 043acc1dd, 2026-08-18) retired
   the impeach option from canton.2 and moved it to `qing_censorate.11`. So the flood's exact
   reproduction path no longer exists in HEAD, and error-count disappearance cannot be validated
   against that log.
4. **Equal counts = systematic per-invocation failure.** The three message types are 4,566 EACH
   (perfectly equal) — the signature of every invocation on the path throwing all three, NOT a rare
   "on some ticks" transient (which would give sporadic, unequal counts).
5. **"Failed to fetch qing_char_affinity" can only come from a `var:qing_char_affinity` FETCH.**
   That var is SET at line 47 and READ at the clamp (lines 199-200), and **the clamp is OUTSIDE the
   `exists = root.current_ruler` guard** (the guard closes at line 196). Gating the zeal arithmetic
   therefore cannot suppress that message.

## Corrected root cause — an invalid CURRENT scope (`this`), not `root.current_ruler`

`QING_char_affinity` scores the CURRENT character scope (`this`) and writes `this`-scoped vars.
The prior fix guarded only `root.current_ruler`'s existence (line 64) — but the statements that
throw operate on `this`:

```
47   set_variable = { name = qing_char_affinity  value = 50 }        # OUTSIDE the guard
63   if = { limit = { exists = root.current_ruler }  ... ruler block ... }   # 64..196
199  if = { limit = { var:qing_char_affinity > 100 } set_variable = ... }    # OUTSIDE the guard
200  if = { limit = { var:qing_char_affinity < 0 }   set_variable = ... }    # OUTSIDE the guard
```

If `this` is an **invalid or dead-but-existing** character scope:
- line 47 cannot set the var,
- the clamp reads at 199/200 then throw "Failed to fetch variable for 'qing_char_affinity'",
- and the ruler-block reads throw "unset scope" / "invalid left side".

That is three error types PER invocation — exactly the equal-count signature. The prior
`exists = root.current_ruler` guard does nothing here because the bad scope is `this`, not the ruler.

### Why the impeach path can hand it a dead `this`
`QING_censorate_impeach_uphold` (se_QING_CENSORATE.txt:311) guards `exists = scope:qing_censorate_target`
(line 314) before `scope:qing_censorate_target = { QING_char_cleanse = yes ... }` (→ QING_char_affinity).
But `exists` proves the scope **resolves**, NOT that the character is **alive**. A target that died
between being saved and the effect running (or any other dead-but-existing saved/derived scope)
passes `exists`, so the affinity body runs on a dead `this` and floods. The 30+ other callers pass
saved/derived scopes too (`scope:qing_amban_current`, `current_ruler.spouse`, `ordered_character`
picks, `var:qing_office_*_holder`, …), any of which can be dead-but-existing on a given tick.

## Fix (se_QING_AFFINITY.txt) — guard the WHOLE scoring body on a live current scope

Wrap the set at 47, the ruler block, and the clamp in a single `is_alive = yes` guard on `this`:

```
QING_char_affinity = {
    LOG_enter = { sys = QING  fn = "QING_char_affinity" }
    if = {
        limit = { is_alive = yes }        # [fix #11] the whole score reads/writes `this`; a dead-but-
                                          # existing scope threw all 3 message types per call (equal
                                          # 4,566 counts). is_alive is a TRIGGER: on a dead/none scope
                                          # it returns false and the body is skipped — no set, no reads,
                                          # no errors. The old exists=root.current_ruler guard covered
                                          # the wrong scope (it stays, nested, for the ruler block).
        set_variable = { name = qing_char_affinity  value = 50 }
        if = { limit = { exists = root.current_ruler }  ... unchanged ruler block ... }
        # clamp 0..100 (now inside the is_alive guard)
        if = { limit = { var:qing_char_affinity > 100 } set_variable = { name = qing_char_affinity value = 100 } }
        if = { limit = { var:qing_char_affinity < 0 }   set_variable = { name = qing_char_affinity value = 0 } }
    }
    LOG_line = { sys = QING  msg = "char affinity: w/ throne = (zeal gap)" }   # static string, no var read — safe outside
    LOG_exit = { sys = QING  fn = "QING_char_affinity"  result = OK }
}
```

- `is_alive = yes` is a proven character-scope trigger (used across the household/panel code). On a
  dead or none `this` it degrades to false — it does NOT error — so the body is skipped cleanly.
- The zeal-gap arithmetic and its `has_variable` sub-guards are left EXACTLY as they are (the first
  diagnosis's edits are NOT applied); only the outer `is_alive` wrapper is added and the clamp moves
  inside it.
- LOG_enter/LOG_line/LOG_exit stay outside the guard: they are static strings with no var reads.

### Caller-read safety when the body is skipped
If `this` is dead, the body skips and `qing_char_affinity` stays unset. The main reader,
`QING_char_bind` (se_QING_AFFINITY.txt:213), guards `has_variable = qing_char_affinity` before it
reads (216-218). A bare read elsewhere on a genuinely-dead scope is at most ONE error on that broken
scope — not a per-tick flood. Net: the flood class is removed; no new flood is introduced.

## Honest limits of this fix (no over-claiming)
- The stale log's exact caller (`canton.2.a`) is ALREADY retired by #8 (043acc1dd), so the specific
  reproduction in that log is gone regardless of this change. This fix HARDENS the shared scoring
  effect so no caller — present or future — can flood it via a dead/invalid `this`.
- Confirmation is the ABSENCE of the three `QING_char_affinity` error messages on the next boot; no
  new probe is added (the error count is the signal). Because the log is pre-#8, I cannot pre-verify;
  this is a source-reasoned robustness fix, logged as such.

## Adjacent defect found by the review (NOT part of #11 — logged as a new item)
The review noted `QING_censorate_impeach_uphold` is also called from `qing_censorate.7`, a CHARACTER
event where `ROOT` = the accused, not CHI. On that path `root.current_ruler` is invalid, so the
`exists` guard skips the ruler-relative scoring and affinity stays a flat 50 (a silent SCORING
inaccuracy, not an error). This is a separate, non-erroring concern; it is NOT the flood and is not
fixed in this commit. Recorded for the backlog so it is not lost.

## FINAL RESOLUTION (applied 2026-08-18) — after the second adversarial review

The second review (task a29b39c237b994b62) returned SOUND-WITH-CHANGES. Its decisive finding:
my earlier plan to wrap the WHOLE body (incl. the set at 47) in `is_alive` would only RELOCATE
the "Failed to fetch qing_char_affinity" message to ~13 unguarded caller reads (se_QING_AMBAN,
se_QING_PERSONNEL, se_QING_WAR, se_QING_ACCOUNTABILITY, qing_regency, qing_greatgame). Its
Required #1 (the endorsed core fix): keep the neutral default and the clamp UNCONDITIONAL, wrap
ONLY the `this`-stat-reading ruler block in `is_alive`.

**What shipped (Required #1 exactly):** the guard at se_QING_AFFINITY.txt line 64 changed from
`limit = { exists = root.current_ruler }` to `limit = { is_alive = yes  exists = root.current_ruler }`.
- `set_variable = { name = qing_char_affinity value = 50 }` (line 47) STAYS unconditional and
  outside the guard — a guaranteed neutral default.
- The clamp (199-200) STAYS outside — it reads only `var:qing_char_affinity` (a var, never a
  stat), so it is safe on any scope once the default is set.
- Only the stat reads (charisma/zeal/culture/religion/age/health/power_base) now sit behind
  `is_alive`, so a dead-but-existing `this` skips them cleanly.

**Why Required #2 (guard the ~13 caller reads) is NOT needed here:** it was gated on "if and only
if line 47's `set_variable` itself throws on the bad scope." Variables are writable/readable on
dead-but-existing characters — the repo's own staleness idiom evaluates `var:X = { is_alive = no }`
on such scopes (se_QING_SALT.txt:239, se_QING_CANTON.txt:293, qing_dynasty_triggers.txt:40). So
line 47 sets the var even on a dead `this`; every caller that reads `var:qing_char_affinity` after
calling the macro then reads the neutral 50, never an unset. The fetch-unset class is closed at the
source by the preserved default, not relocated. (If a future boot shows the class survives at a
caller, that boot-only fact — line 47 throwing — is the trigger to add the #2 caller guards; it is
NOT deferred work, it is the documented next-round tuning per the overnight loop.)

**Honest status:** root cause is NOT definitively proven (two theories were refuted; a boot to
reproduce is unavailable — the newest log is pre-#8). The dominant caller in the stale log
(canton.2.a) is already RETIRED by #8 (043acc1dd); the new qing_censorate.11 / .7 paths still route
impeach → cleanse → affinity, so the hazard remains reachable. This fix is a can't-hurt hardening
of exactly the statements that can throw on a bad current scope, with a preserved neutral default.
Confirmation = absence of the three QING_char_affinity messages on the next boot.

## Review targets for the re-review of THIS (corrected) diagnosis
- Does `is_alive = yes` on the current scope actually degrade to false (not error) for a
  dead-but-existing character, and for a none scope? (It should — standard trigger semantics.)
- Does moving the clamp inside the guard change any legitimate output when `this` IS alive? (No —
  identical statements, same order.)
- Any caller that reads `var:qing_char_affinity` WITHOUT a `has_variable` guard immediately after
  calling the macro, which a skipped body would turn into a read-unset? (Audit the ~30 callers.)
```
