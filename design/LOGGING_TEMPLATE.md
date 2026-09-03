# LOGGING_TEMPLATE.md — how to get WORKING logs out of this mod

**Status:** authoritative. Read before you add or edit ANY `debug_log` / `LOG_*` line.
**Why this exists:** we repeatedly burned boot cycles shipping log code whose syntax was
wrong, so the boot produced garbage (e.g. the #23 currency probe: 2142 lines all reading
`=9`, and `$pos$` printed literally). Every failure was an **unverified assumption about
`debug_log` string syntax**. This doc records what the engine ACTUALLY does, proven at byte
level from real boot output, so it never has to be rediscovered.

---

## The one rule

**A `debug_log` string must be 100% LITERAL. No `$param$`. No `[Scope.Func]`. No `[...]`
brackets.** Dynamic values are emitted by choosing between literal strings (if/else_if band
ladders), never by substituting into a string.

If you catch yourself writing `debug_log = "... $x$ ..."` — STOP. It will mangle. Use a band
ladder (below).

---

## What the engine actually does (proven from boot Aug 7 2026, `od -c` on debug.log)

`debug_log` runs in scripted-effect / on_action / event context (NOT GUI context). Three cases:

| Form | Result | Proof |
|---|---|---|
| **Literal string** | ✅ renders **exactly** | `"IMP19C CURX ratio < 0.1 (deflation FLOOR)"` → clean |
| **`$param$` in string** | ❌ **mangled**: leading space eaten, value inserted, **trailing `$` left** | `"IMP19C $sys$: $msg$"` → `IMP19CQING$:...subject=$` (bytes: `...S U B J $ :`) |
| two adjacent `$a$ $b$` | ❌ collide | `"digit $tag$ $pos$"` → `digittrout$p8$` |
| **`[ROOT.MakeScope.GetVariable('x').GetValue]`** | ❌ "Could not find promote", renders **nothing** | see removal notes throughout `se_ECON_LOG.txt` |

The corruption is deterministic: `<space>$name$` → `<value>$`. There is **no** working
`$param$` variant — `EXIT $fn$ result=$result$` renders `EXITfoo$ resultOK$`. Every case tested.

> **Numeric values cannot be rendered at all.** There is no working "print this number"
> primitive in scripted-effect `debug_log`. Do not try. Emit a band (below).

> ⚠️ The old comment in `se_LOG.txt` claiming "`$arg$` substitution DOES work (proven:
> se_PURCHASE `$tradegood$`)" is **FALSE** — it was never checked against output. `se_PURCHASE`'s
> `$tradegood$` lines mangle exactly like everything else. Do not trust that comment.

---

## The PROVEN-CLEAN pattern: band ladders (copy this)

To log a value V, stage it into a temp var, sentinel-guard it, then pick a **literal** string
by threshold. This is the ONLY pattern proven to render clean. Every line is fully literal.

```txt
MY_LOG_ratio = {
    # Scope: country
    set_variable = { name = MY_tmp  value = SOME_script_value }        # set_variable NEVER errors; stores empty on Div0
    if =      { limit = { NOT = { has_variable = MY_tmp } }  debug_log = "IMP19C MYSYS ratio = UNSET" }
    else_if = {
        limit = { var:MY_tmp > -999999999 }                            # sentinel: empty/Div0 -> false -> EMPTY line below
        if =      { limit = { var:MY_tmp >= 1.5 }   debug_log = "IMP19C MYSYS ratio >= 1.50" }
        else_if = { limit = { var:MY_tmp >= 1.0 }   debug_log = "IMP19C MYSYS ratio 1.00-1.50" }
        else_if = { limit = { var:MY_tmp >= 0.5 }   debug_log = "IMP19C MYSYS ratio 0.50-1.00" }
        else =    { debug_log = "IMP19C MYSYS ratio < 0.50" }
    }
    else = { debug_log = "IMP19C MYSYS ratio = EMPTY (Div0/unset operand)" }   # the empty case is a FINDING, not noise
    remove_variable = MY_tmp
}
```

Rules baked into that template:
- **Every RHS is a LITERAL** (`>= 1.5`), never `>= var:x` or a script_value — see
  `imp19c-rhs-comparison-operator-rule` (var-on-RHS of a comparison is illegal).
- **Sentinel guard `> -999999999`** distinguishes a real value from a set-but-empty var (a
  Div0 or empty operand stores empty; `has_variable` is TRUE for it, so you MUST value-test).
  The `else` branch labels it `= EMPTY` — that is diagnostic signal, not noise.
- **Bands fine where decisions live, coarse in the tails.** Put tight bands around the
  boundary you care about (e.g. the inflation/deflation 1.0 line), wide ones elsewhere.
- **One metric = one effect with its OWN literal strings.** Do NOT factor the label into a
  `$param$` "generic emitter" — that reintroduces the bug. Repetition here is correct.
- **Temp vars prefixed + removed** each call (read-only tracing, no state leak).
- Reading back: `grep "IMP19C MYSYS ratio"` — each line states its own band in plain numbers.

For a **sign**, emit two literal lines: `if <0 -> "... = NEGATIVE"` / `else -> "... = POSITIVE"`.
For PRE/POST or any mode flag, write **two separate effects** with two literal marker strings —
never a `$phase$` param.

---

## Segmenting the trace

No in-game date appears on log lines; the wall-clock `[HH:MM:SS]` prefix is the only time key.
Emit a literal **marker** line at the top of each cycle so a reader can window the grep:

```txt
debug_log = "IMP19C CURX QUARTER-MARK POST (fresh recompute)"
```

Then per quarter: `grep -A400 "QUARTER-MARK POST" | grep "IMP19C CURX ratio"`.

---

## `debug_log` only fires under `-debug_mode`

All `debug_log` lines are silently dropped in a normal session — zero cost, zero gameplay
effect. A boot that was NOT launched with `-debug_mode` produces NO `IMP19C` lines at all
(see `imp19c-debug-mode-standing-rule`). If the trace is empty, check that first.

GUI-context caveat: `debug_log` fired from inside a `scripted_gui` invoked by a button's
`onclick` Execute did NOT reliably appear in past boots. To observe a GUI click, STAMP a
country variable in the GUI effect and READ+log it from an on_action pulse (see
`LOG_gui_probe_stamp` / `LOG_gui_probe_report` in `se_LOG.txt`).

---

## The core `se_LOG.txt` writers (`LOG_line` / `LOG_enter` / `LOG_exit` / `LOG_fail`)

These take a dynamic `$msg$` / `$fn$`, so by the rule above they mangle: the value is present
but a `$` trails it and the char before it is eaten. This is **structural and unavoidable** —
confirmed by proven code: the Invictus and Terra-Indomita oracles NEVER interpolate a param into
`debug_log`; every oracle `debug_log` is a fully-literal string. There is no clean-interpolation
primitive and no `log_effect`/`custom_log` alternative. So a dynamic log line CANNOT be made
fully clean. (This was determined from EXISTING boot bytes — the rule "each `$name$` eats the one
char before it and appends `$`" fully predicts a lone `"$msg$"` → `value$`. No boot-test needed;
do not add one.)

**What CAN be fixed — the grep KEY.** The one thing that mattered was that `"IMP19C $sys$: ..."`
fused the sys tag to the prefix (`IMP19CQING`), corrupting the string you grep on. Fix: put **two
spaces** before `$sys$` (`"IMP19C  $sys$: ..."`) — the engine eats one, one survives, so the key
renders `IMP19C QING` and `grep "IMP19C QING"` works. The trailing `$` after each param remains
(cosmetic, harmless to a tag grep). Applied to LOG_line/enter/exit/state/ok. `LOG_fail`'s key is
the literal `IMP19C FAIL` (param is mid-string), already clean. Phase markers `IMP19C ECON: ...`
are likewise clean-keyed (the sys tag is literal there; only `$stage$` fuses, mid-string).

**Bottom line:** dynamic lines are readable and grep-key-clean; they still carry a cosmetic `$`
per param. That is the ceiling. Do not try to eliminate the `$` — proven impossible.

**CORRECTION 2026-09-03 — a LEADING `$param$` is NOT merely cosmetic, it is CALL-VOIDING.**
Everything above holds when the `$param$` sits mid-string, after real literal text. It does
NOT hold when the substitution is the FIRST thing inside the quotes. `se_QING_COUNCIL.txt` had
four `LOG_line` calls shaped `msg = "$office$ seat filled by DRAW"` — `$office$` is the very
first token after the opening `"`. Real boot evidence: 286×/boot,
`Compiling source for LOG_line failed for unknown arguments: seat, by, (, )`. Mechanism: the
"eats the one char before the param" rule eats the OPENING QUOTE ITSELF when the param is
first — the string unquotes, and its own words (`seat`, `by`, `(`, `)`) leak out and get
parsed as stray bareword arguments to the `LOG_line` call, which is why the compiler names
them as "unknown arguments." Fix: **never let a `$param$` be the first character inside the
quotes** — prepend any literal word (`msg = "seat $office$ filled by DRAW"` compiles and
renders fine, cosmetic mangling only, per the rule above). This is now a MANDATORY checklist
item (below) — checked by making sure every dynamic `LOG_*` string's first non-quote
character is a letter/word, never `$`.

---

## Pre-commit checklist for any logging change (MANDATORY)

1. **No `$param$` in any NEW `debug_log` string** (for a dynamic value use a band ladder; the
   pre-existing core `LOG_*` writers are the documented exception — they can't be clean, see below).
   `grep -n 'debug_log = "[^"]*\$'` your file to see every param line.
2. **No `[` brackets in any `debug_log` string** (parsed as data-function syntax, mangles).
2b. **For the core `LOG_*` writers' `$param$` strings (the one documented exception to #1):
   the substitution must NEVER be the first character inside the quotes** — a leading
   `$param$` eats the opening quote and voids the whole call ("unknown arguments", see
   correction above), it is not just cosmetic. Prepend a literal word if needed.
3. **No numeric render attempt** (`.GetValue`, `Multiply_CFixedPoint`, digit math). Use bands.
4. **Every comparison RHS is a literal**, not `var:x` / a script_value.
5. **Sentinel-guard staged svalues** (`> -999999999`) and give the empty case its own line.
6. **Temp vars removed** at the end of the effect.
7. If you claim a form "works", **cite the byte-level proof** (a real log line), not another
   comment. Unverified "this should work" is banned — it is what burned the boots.

Reviewers: reject any logging diff that fails 1–4. This is the check the earlier reviews
skipped — they validated braces and logic but not macro-in-log-string, which is the entire
failure class.

---

## Related
`imp19c-log-string-macro-rule`, `imp19c-debug-mode-standing-rule`, `imp19c-logs` skill,
`imp19c-rhs-comparison-operator-rule`, `imp19c-econ-log-noise-not-bugs`,
`se_LOG.txt`, `se_ECON_LOG.txt` (`ECON_LOG_currency_snapshot` is the reference clean probe).
