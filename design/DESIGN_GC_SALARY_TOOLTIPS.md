# DESIGN: Grand Council officeholder salary tooltips

Scope: UI-only. Show what each Grand Council (GC) officeholder currently earns, in his own
character card, in the same GUI panel that already shows his name and governing-skill readout.
This does NOT change any payout amount, any accumulator, or any file in
`common/scripted_effects/se_QING_WAGES.txt`. It reads that file's own existing rate/formula and
displays it.

## 1. Where the salary amount is defined today

`common/scripted_effects/se_QING_WAGES.txt` pays every GC seat via `QING_pay_gc_seat_wage`
(lines 48-65):

```
set_variable = { name = WAGE_pay_tmp  value = INCOME_national_total_quarterly }
change_variable = { name = WAGE_pay_tmp  multiply = 0.01 }
if = { limit = { var:WAGE_pay_tmp > 0 }  ... add_gold ... }
```

The macro takes NO `$rate$` parameter — `0.01` is hardcoded. All 12 calls to it
(`se_QING_WAGES.txt:148-159`: personnel, revenue, rites, war, justice, works, censor, lifanyuan,
chamberlain, zongli, grand_secretariat, guard_commandant) use the same 0.01. The 13th office,
chancellor, is paid by a separate inline block (lines 164-179) that is **also** flat 0.01.

**Finding: all 13 Grand Council offices pay an identical flat rate — 1% of
`INCOME_national_total_quarterly` (the mod's own real-income figure, country-scope var) — floored
at 0 in a deficit quarter** (the `var:WAGE_pay_tmp > 0` guard; a deficit quarter pays nothing
rather than docking the officeholder, per the file's own review-fix history). It does not vary by
office, by holder skill, or by anything else. (Non-GC posts — the 5 single-holder commissioners,
the amban, and the 3 sub-post markers — use their own separate rates 0.01-0.02 via different
macros; they are explicitly out of scope, see §5.)

## 2. Chosen approach: live-compute via a shared script_value

**Recommendation: compute the figure live in a `script_value`, read by the GUI at render time.
Do NOT store a per-character "last paid" variable.**

Proven precedent in this codebase for a GUI reading a script_value inline (not a stored variable):
- `gui/ingame_topbar.gui:1170`: `text = "¥[GuiScope.SetRoot(Player.MakeScope).ScriptValue('WEALTH_total_private_moveable_wealth')|3]"`
- `gui/economy_view.gui:504,612,720,828...`: `GuiScope.SetRoot(Player.MakeScope).ScriptValue('INCOME_excise_duties_country')|3+=`
- `gui/mapiconlayer.gui:2774`: `GuiScope.SetRoot(Scope.GetProvince.MakeScope).ScriptValue('SHIPPING_province_power')`
- `gui/province_window.gui:1688`: `GreaterThan_CFixedPoint(GuiScope.SetRoot(...).ScriptValue('INDUSTRY_governorship_free_industry_slots'), '(CFixedPoint)0')`

And for the script_value math itself, `common/script_values/INCOME_svalues.txt` already contains
the exact shape needed: `value = var:X`, `multiply = <rate>`, `min = 0` (e.g.
`INCOME_governorship_property_tax_upper_strata` at line 548-551, `INCOME_subject_overlord_duty`
at line 257-259 uses `min = 0` directly).

So the new script_value is a two-line, zero-risk addition:

```
# common/script_values/QING_WAGES_svalues.txt (new file, or appended to an existing QING svalues file)
QING_gc_office_wage_svalue = {
	value = var:INCOME_national_total_quarterly
	multiply = 0.01
	min = 0
}
```

One shared script_value covers all 13 offices, because the rate is identical for all of them
(§1). No per-office variants are needed unless a future balance change makes rates diverge — if
that happens, split into `QING_wage_<office>_svalue` at that time; do not pre-build that
flexibility now (no code needed until it's needed).

**Rejected alternative: stored per-character last-paid variable** (e.g.
`set_variable` on the holder inside `QING_pay_gc_seat_wage`, then GUI reads
`Var('qing_office_X_holder').GetCharacter.MakeScope.GetVariable('qing_last_wage_paid').GetValue`).

Rejected because:
- It shows what was **actually paid last quarter**, not the current rate — less useful to a
  player deciding whether to appoint someone, and wrong/stale for the first ~3 months after a
  fresh appointment (the var does not exist until the first `QING_GOV_pulse` quarterly tick pays
  it, so a newly-appointed minister's tooltip would show nothing or a stale predecessor's figure
  until then).
- It requires editing `se_QING_WAGES.txt` — the exact file whose own header documents **two**
  real bugs already found and fixed by independent review this same day (the deficit-quarter sign
  inversion, and the amban never-paid employer-filter bug). Touching that payout logic again for
  a purely cosmetic display feature reopens a file the project has just finished hardening, for no
  functional gain — a clear violation of the "UI-only, no payout changes" scope in §5.
- Live-compute needs **zero new state**: no new variable, no new set_variable call anywhere, no
  interaction with the wage-payment macros at all. The GUI-only change is strictly lower risk.

## 3. GUI change (one pattern, applied to every panel)

Each per-office ministry/institution panel already renders a "Minister card" with this exact
shape (verified in `gui/qing_revenue_ministry.gui:106-134`, mirrored byte-for-byte across the
other 11 dedicated panels):

```
flowcontainer = {
	visible = "[GetScriptedGui('qing_<office>_ministry_filled').IsShown(...)]"
	spacing = 8
	cpt_button = { size = { 50 77 }  datacontext = "[Player.MakeScope.Var('qing_office_<office>_holder').GetCharacter]" }
	flowcontainer = {
		direction = vertical
		spacing = 4
		textbox = { text = "[Player.MakeScope.Var('qing_office_<office>_holder').GetCharacter.GetName]" ... }
		flowcontainer = {
			datacontext = "[Player.MakeScope.Var('qing_office_<office>_holder').GetCharacter]"
			icon_and_text = {
				size = { 70 24 }
				blockoverride "Icon" { using = icon_civic }
				blockoverride "Text" { text = "[Character.GetFinesse]" }
				tooltip = "[Character.GetFinesseToolTip]"
			}
		}
	}
}
```

Add ONE sibling `icon_and_text` next to the existing skill readout (same flowcontainer, no new
datacontext needed since the wage figure is country-scoped, not character-scoped):

```
icon_and_text = {
	size = { 70 24 }
	blockoverride "Icon" { using = icon_civic }   # placeholder — see note below
	blockoverride "Text" { text = "[GuiScope.SetRoot(Player.MakeScope).ScriptValue('QING_gc_office_wage_svalue')|2]" }
	tooltip = "QING_GC_WAGE_TT"
}
```

Note on the icon: this codebase has no dedicated "money/coin" icon key already in use inside an
`icon_and_text` block (checked `economy_view.gui`, `ingame_topbar.gui`). Whoever implements this
should do a one-time lookup of the actual currency/wealth GFX sprite key (or reuse `icon_civic` as
a neutral placeholder, matching the existing skill readout, until a better icon is confirmed) —
this is an implementation detail, not a design blocker.

### Files to touch (14 total)

Twelve dedicated per-office dashboards, each with exactly one "Minister card" for its own office
(add the block above once, in each):

| File | Office |
|---|---|
| `gui/qing_personnel.gui` | personnel |
| `gui/qing_revenue_ministry.gui` | revenue |
| `gui/qing_rites_ministry.gui` | rites |
| `gui/qing_war_ministry.gui` | war |
| `gui/qing_justice.gui` | justice |
| `gui/qing_works_ministry.gui` | works |
| `gui/qing_censorate.gui` | censor |
| `gui/qing_lifanyuan.gui` | lifanyuan |
| `gui/qing_household.gui` | chamberlain |
| `gui/qing_zongli.gui` | zongli |
| `gui/qing_guard.gui` | guard_commandant |
| `gui/qing_hanlin.gui` | grand_secretariat (Hanlin Academy clone-dashboard) |

Plus one office with TWO dedicated dashboards sharing the same office var (both need the block,
each independently — they are separate panel files, not includes):

| File | Office |
|---|---|
| `gui/qing_secretariat.gui` | grand_secretariat (Central Secretariat clone-dashboard — same office as qing_hanlin.gui, second panel) |

Plus the master hub, which shows ALL 13 offices (the 12 above + chancellor, who has no dedicated
ministry panel of his own) in one file — needs 13 additions, one per office card
(`gui/government_view.gui:3050` chancellor, `:3296` personnel, `:3406` revenue, `:3516` rites,
`:3626` war, `:3739` justice, `:3849` works, `:3959` censor, `:4069` lifanyuan, `:4182`
chamberlain, `:4292` zongli, `:4404` grand_secretariat, `:4515` guard_commandant):

| File | Offices |
|---|---|
| `gui/government_view.gui` | all 13 (chancellor + the 12 above) |

**Explicitly excluded**: `gui/qing_greatgame.gui` shows a secondary, incidental mini-card for the
zongli holder inside the Great-Power-rivalry panel (`:123-136`) — a different, non-council-hub
context. The task asks for the tooltip in "the relevant GUI panel" (singular, canonical); adding
the wage figure to every incidental appearance of an officeholder across the whole mod is
scope-creep beyond what was asked. If the user wants it there too, that is a one-line follow-up
using the identical pattern.

## 4. Localization key naming

One shared tooltip key, since the wage figure and its explanation are identical for all 13
offices (§1):

- `QING_GC_WAGE_TT` — the tooltip text, e.g. "Quarterly salary: 1% of the Qing state's net
  quarterly income. Paid at the start of each quarter; unpaid in a deficit quarter."

No per-office label key is needed — the icon_and_text's own tooltip is sufficient, matching the
finesse readout it sits beside (which also carries no separate label, just
`Character.GetFinesseToolTip`).

## 5. Scope

This is a UI-only addition: one new script_value (pure read, `min = 0` floor, no side effects)
and one repeated GUI block across 14 files. It does NOT:
- change any rate, multiplier, or floor in `se_QING_WAGES.txt`,
- add any new `set_variable`/`add_gold`/accumulator,
- touch the non-GC wage-bearing posts (salt commissioner, caravan superintendent, Hoppo, opium
  commissioner, customs inspector-general, amban, zongli diplomat sub-post, censor-inspector
  sub-post, imperial-guardsman sub-post) — those are not Grand Council offices per
  `se_QING_COUNCIL.txt`'s own definition of "the 13 appointable offices", and are not shown in any
  of the panels this doc's file list touches.

## Adversarial review

**Claim under test:** a Jomini GUI `icon_and_text.tooltip`/`.text` expression can read a
scripted-effect-derived number *inline*, without a stored variable, the same way the existing
finesse readout reads `Character.GetFinesseToolTip` inline.

**Check 1 — does `GuiScope.SetRoot(Player.MakeScope).ScriptValue('X')` actually work in THIS
codebase, live, uncommented, in a shipped panel (not a commented-out draft)?**
Yes — `gui/ingame_topbar.gui:1170,1183,1196`, `gui/economy_view.gui:504,612,720,828,1163,1271,1379`,
and `gui/mapiconlayer.gui:2720,2774` all use this exact call shape, live, in the topbar and the
economy view, both panels a player looks at every session. Not a dead/experimental pattern.
Resolved: proven.

**Check 2 — is a `script_value` allowed to read a country-scope stored variable
(`INCOME_national_total_quarterly`) with a multiply and a floor, the same shape needed here?**
Yes — `common/script_values/INCOME_svalues.txt:257-259`
(`INCOME_subject_overlord_duty = { value = INCOME_national_total_from_regions  min = 0 }`) and
`:548-551` (`multiply = WEALTH_...`) are the identical shape (`value = var:X`, `multiply`, `min`)
already live in this exact script_values family. `INCOME_national_total_quarterly` is itself a
script_value already read this way elsewhere (`common/script_values/AI_svalues.txt:2066`,
`DIPLOMACY_svalues.txt:548,552`). Resolved: proven, and reads the SAME variable
`se_QING_WAGES.txt` itself reads for the actual payout — no risk of the display drifting from a
different income figure than what's really paid.

**Check 3 — does the surrounding GUI block's `datacontext` (set to the officeholder CHARACTER)
break a `ScriptValue` call rooted at `Player.MakeScope` (COUNTRY), i.e. is there a scope mismatch?**
No — `GuiScope.SetRoot(Player.MakeScope)` explicitly re-roots the scope for that one call,
independent of the surrounding `datacontext`. `gui/qing_greatgame.gui` and every ministry panel
already mix a character-scoped `datacontext` with country-scoped reads elsewhere in the same
window (e.g. `gui/qing_justice.gui:161`: `Player.MakeScope.GetVariable('qing_min_perf_justice')`
sits inside a panel whose Minister card block above it uses a character `datacontext`). Resolved:
no conflict — the two scopes coexist in the same file today.

**Check 4 — is there a reason THIS specific wage figure would be flagged "None"/blank for a
freshly appointed holder, undermining the "shows the current rate even before first payout"
selling point of live-compute?**
No — `INCOME_national_total_quarterly` is a standing national aggregate that exists from game
start regardless of who holds what office; it is not per-holder state. A freshly appointed
minister's card shows the real current 1%-of-income figure on the very same tick he is appointed,
with no lag. This is exactly the advantage claimed in §2, and it holds up.

**Outcome: no changes required to the approach in §2-§3.** All four load-bearing assumptions
(proven `ScriptValue()` GUI call, proven script_value multiply/floor shape, no scope conflict, no
first-payout lag) check out against concrete, live (non-commented, non-draft) examples already
shipping in this codebase. No fixes needed; the design stands as originally proposed.
