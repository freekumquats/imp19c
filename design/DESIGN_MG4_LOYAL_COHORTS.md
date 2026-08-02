# MG-4 Design — Loyal-cohorts grant adds nothing

**Bug (user boot-test):** An event/lever that grants a regional governor loyal cohorts fires,
but no loyal cohorts materialise on the governor's legion.

## Root cause (research-confirmed, agent a9a0371a8326a0238)
`add_loyal_veterans = N` on a character has TWO different meanings depending on whether that
character commands an army:
- On a **commander with a legion**: (behaviourally) converts/adds loyal cohorts that visibly answer
  to him.
- On an **army-less governor/courtier**: only increments the abstract `num_loyal_veterans` pool +
  applies the passive `loyal_veterans` static modifier (popularity/prestige/heir-support). **No
  physical loyal cohorts appear** — there is no army for the pool to manifest in.

The culprit is **`QING_regional_army_bind_commander`** (`se_QING_MECHANICS.txt:172`), reached from
the **Sanction a Regional Army (勇營)** scripted_gui lever (`QING_mechanics_actions.txt:157` →
`QING_sanction_regional_army` → `QING_regional_army_bind_commander`). It does
`ordered_character = { … add_loyal_veterans = 8  QING_magnate_track_grant = yes }` on a sitting Han
governor **who commands no legion**. So the lever's own tooltip
(`QING_ACTION_SANCTION_REGIONAL_ARMY_TT`) promises "a real Han magnate gains a personal power base of
**loyal cohorts**" — but the player sees zero cohorts. Exactly the reported no-op.

(The former `else` branch that would `create_character` a founder was already removed as a
boot-crash; see the #90-fix comment at :199-212. So when no Han governor stands, only the +15
counter lands — also cohort-less, but that path is intentional.)

## Fix — complete the concrete link (the tooltip already promises it)
Mirror the PROVEN grandee-flip idiom `QING_council_raise_grandee_legion`
(`se_QING_COUNCIL.txt:929-964`) and the SELFSTR raises: raise a real 勇營 (`qing_yongying`) legion at
the capital, attach the Han magnate as its commander, and `set_personal_loyalty` its sub_units to
him — so the cohorts visibly answer to HIM (the civil-war seed the counter abstracts). This is the
concrete embodiment task #90's own comments (:153-157) already describe; only the physical raise was
missing.

### CRITICAL — scripted_gui compile-inline crash guard ([[imp19c-scripted-gui-compile-recursion-crash]])
`QING_sanction_regional_army` is called from a **scripted_gui button** (`effect = { … }`). A
scripted_gui compile-inlines its whole effect chain at PARSE time; a `raise_legion`/`create_unit`
body inside a `random`/`ordered_character` iterator inlined into a compiled button is the exact
`EXCEPTION_ACCESS_VIOLATION` class fixed for #443. Therefore the raise MUST go through a
**`trigger_event` trampoline** (a runtime ref, never compile-inlined).

**Proven precedent (CORRECTED — design review agent ad5dc10127c852f5c, Flag 1):** the trampoline
pattern for a raise-from-a-button is genuinely demonstrated at
`common/scripted_guis/QING_guard_panel.txt:143` — `trigger_event = { id = qing_guard.10 }`, whose
#443-crash-fix comments (`QING_guard_panel.txt:134-142`) state that inlining the
`create_character` + `raise_legion`/`create_unit` chain into the GUI parse unit caused an
`EXCEPTION_ACCESS_VIOLATION` at the loading bar, and that this is the ONLY loaded panel reaching
raise_legion/create_unit — every other panel trampolines through an event. `qing_guard.10` is defined
at `events/imp19c_mod_events/qing_guard_events.txt:183`.
(An earlier draft of this doc cited "5 sibling levers … `trigger_event = { id = qing_advisor.1 }` at
`se_QING_MECHANICS.txt:508-616`" — that citation was FABRICATED: that file has zero `trigger_event`
occurrences and :508-616 hold unrelated effects. The conclusion stands; only the evidence was wrong.)

### Implementation (two edits, no behaviour lost)
1. **New hidden trampoline event** `qing_office.42` (next free id after .41) in
   `qing_office_events.txt`, `country_event`, `hidden = yes`, `is_triggered_only = yes`. Its
   `immediate` does the Han-governor selection + concrete raise:
   ```
   qing_office.42 = {
       type = country_event
       hidden = yes
       is_triggered_only = yes
       immediate = {
           LOG_line = { sys = QING  msg = "EVENT qing_office.42 (勇營 regional-army raise trampoline) [ROOT.GetTag]" }
           # empower the weightiest sitting Han governor (Han culture, NOT primary_culture=manchu)
           if = {
               limit = { any_character = { employer = ROOT  is_ruler = no  is_adult = yes  is_alive = yes  is_governor = yes  has_culture = han } }
               ordered_character = {
                   limit = { employer = ROOT  is_ruler = no  is_adult = yes  is_alive = yes  is_governor = yes  has_culture = han }
                   order_by = power_base
                   check_range_bounds = no
                   max = 1
                   # [Flag-2 fire-once] capture whether this man was ALREADY a magnate BEFORE the
                   # grant, so the raise below fires only on his FIRST sanction (see balance note).
                   if = { limit = { has_character_modifier = qing_regional_magnate }  set_variable = { name = qing_had_yongying_already  value = 1 } }
                   # abstract power base (kept — passive modifier the man carries)
                   add_loyal_veterans = 8
                   QING_magnate_track_grant = yes
                   save_scope_as = qing_regional_magnate_commander
                   LOG_line = { sys = QING  msg = "勇營 raised under sitting Han governor (+8 loyal veterans + concrete legion) for" }
               }
               # concrete legion so the loyal cohorts actually exist — ONLY on the man's FIRST
               # sanction (guarded on capital_scope + the fire-once flag). Repeat sanctions of the
               # same man grow only his abstract tally (mirrors QING_magnate_track_grant's own
               # first-vs-subsequent split), so one magnate = one physical legion = no unbounded pile.
               if = {
                   limit = {
                       exists = ROOT.capital_scope  exists = scope:qing_regional_magnate_commander
                       NOT = { scope:qing_regional_magnate_commander = { has_variable = qing_had_yongying_already } }
                   }
                   ROOT.capital_scope = { state.governorship = { QING_regional_army_raise_yongying = yes } }
               }
               # clean up the transient fire-once flag regardless of branch
               if = { limit = { exists = scope:qing_regional_magnate_commander }  scope:qing_regional_magnate_commander = { remove_variable = qing_had_yongying_already } }
           }
           else = { LOG_fail = { … "no sitting Han governor …" } }
       }
   }
   ```
2. **New raise effect** `QING_regional_army_raise_yongying` in `se_QING_MECHANICS.txt` (clone of
   `QING_council_raise_grandee_legion`, scope:qing_regional_magnate_commander as commander):
   ```
   QING_regional_army_raise_yongying = {
       raise_legion = {
           create_unit = {
               name = "A Regional Army (勇營)"
               location = ROOT.capital_scope
               sub_unit = qing_yongying
               save_scope_as = qing_regional_yongying_legion
               add_subunit = qing_yongying
               add_subunit = qing_yongying
               add_subunit = qing_yongying
               add_subunit = qing_yongying
           }
           if = {
               limit = { exists = scope:qing_regional_magnate_commander }
               scope:qing_regional_magnate_commander = { add_to_legion = PREV }
               random_legion_unit = { set_as_commander = scope:qing_regional_magnate_commander }
           }
       }
       if = {
           limit = { exists = scope:qing_regional_yongying_legion  exists = scope:qing_regional_magnate_commander }
           scope:qing_regional_yongying_legion = {
               every_sub_unit = { set_personal_loyalty = scope:qing_regional_magnate_commander }
           }
       }
   }
   ```
3. **Rewire** `QING_regional_army_bind_commander` (the scripted-effect reached from the GUI button):
   REPLACE its inline `ordered_character { add_loyal_veterans … }` if-branch with a single
   `trigger_event = { id = qing_office.42 }` (runtime dispatch off the compiled path). The abstract
   grant + tracking now live inside the event. Keep the `else` LOG_fail semantics (event handles the
   "no Han governor" log itself).

### Why not reuse QING_council_raise_grandee_legion directly?
It saves `scope:grandee_rebel_commander` and names the army "A Grandee's Private Army" (a REBEL
seed). The sanction lever is the THRONE *authorising* a loyal provincial army — different scope var
+ display name. A parallel effect keyed on `scope:qing_regional_magnate_commander` avoids
cross-wiring the two mechanics' saved scopes.

## Disband symmetry — REQUIRED (user directive 2026-07-29, [[imp19c-onmap-object-lifecycle-symmetry]])
> "if you are raising new units on the map, the related events to curtail a governor's power needs to
> disband those units as well"

Because MG-4 now raises a **real on-map 勇營 legion** under the magnate, the paired curtail levers
(reassert / pension) must destroy that physical army — not merely strip the abstract `-8` veteran
pool as they do today. Otherwise the throne "breaks his power base" while his loyal army stays on the
map answering to him, and repeated sanction→reassert cycles leave an unbounded legion pile.

### Where — `QING_reassert_strip_magnate` (`se_QING_MECHANICS.txt:319`)
This one effect is the single teardown point: it is called by BOTH `QING_reassert_central_command`
AND `QING_pension_off_regional_army`, so fixing it here covers both curtail paths.

### How to reach the units — character scope, NOT governorship scope
The raised legion is a **free legion** (a personal army bound to the commander, like
`QING_council_raise_grandee_legion`'s civil-war seed), so it is NOT the capital governorship's
`legion` — Invictus's `capital_scope.governorship.legion` + `disband_legion = yes` handle does not
reach it. The durable handle is the **commander→his-units link**: the strip path already selects the
magnate via `ordered_character = { … has_character_modifier = qing_regional_magnate }`, and from that
character scope `every_character_unit = { destroy_unit = yes }` destroys the units he commands. Both
verbs are proven: `destroy_unit` (Invictus `000_country_switch_effect.txt:413` nukes the ruler's
raised capital levy via exactly `every_character_unit = { destroy_unit = yes }`; also
`ai_war_effects.txt:434`) and `every_character_unit`/`any_character_unit` (in-mod
`00_ambitions.txt:2323`, `bribe_mercenary_button.txt:29`; Invictus `merc_buyoff.txt`,
`recruit_general.txt`). No cross-event legion-scope save is needed — the char IS the handle, found
fresh each call. (This also means the `save_scope_as = qing_regional_yongying_legion` in the raise is
purely for the same-tick `set_personal_loyalty` bind; it need not persist.)

### Symmetry rule — disband on the FULL break only
The strip already draws `-8` granted veterans per call and clears the `qing_regional_magnate` marker
only when `qing_magnate_granted_veterans <= 0` ("his private army is spent, he is a governor again").
That marker-clear branch is the exact moment the private army ceases to exist — so the physical
disband belongs THERE, inside the existing `if = { limit = { var:qing_magnate_granted_veterans <= 0 } … }`:

```
if = {
    limit = { var:qing_magnate_granted_veterans <= 0 }
    # [disband-symmetry 2026-07-29] the throne-authorised army is spent — destroy the real
    # 勇營 cohorts this magnate commanded (mirror of the concrete raise on sanction), not just
    # the abstract pool. Proven idiom: Invictus 000_country_switch_effect.txt:413.
    every_character_unit = { destroy_unit = yes }
    remove_character_modifier = qing_regional_magnate
    remove_variable = qing_magnate_granted_veterans
    LOG_line = { sys = QING  msg = "reassert: broke the power base of regional magnate — private 勇營 disbanded, marker cleared for" }
}
```
A partial draw (`-8` but pool still `> 0`) leaves the army standing — he is still a marked magnate
with a diminished but real following, which is the intended graduated pressure. Full break =
army gone. This keeps create↔destroy symmetric: each fully-broken magnate loses exactly the army the
sanction raised for him.

### Reviewer flag — over-broad destroy?
`every_character_unit` destroys ALL units the magnate commands. In the normal flow his ONLY commanded
army is the 勇營 the sanction raised (the marker is applied nowhere else). Edge case: if the player
independently made this same character a general of another legion, that legion would also be
destroyed on the full break. Judged acceptable — the reassert is explicitly "break this man's
military power," and it mirrors the country-switch precedent that nukes all of the ruler's raised
units. Flagged for the adversarial reviewer to confirm no narrower filter (e.g. per-sub_unit-type or
a raised-army unit modifier) is warranted.

## Balance / dedup note — RESOLVED to fire-once-per-man (design review Flag 2, MEDIUM)
The Sanction lever is **repeatable and has no treasury cost or cooldown** — confirmed:
`qing_action_sanction_regional_army` (`QING_mechanics_actions.txt:131-158`) gates only on
`is_shown` (decay ≥ 40) + `is_valid` (a Han governor exists), and `QING_sanction_regional_army`
(`se_QING_MECHANICS.txt:145-161`) spends nothing. So a naive "raise every click" would let the
player spam an **unbounded legion pile** (save-bloat/perf/AI hole).

Prior draft leaned "repeatable raise (historical 湘/淮/楚 multi-army reality)". **Overruled by the
review and corrected above:** the concrete legion is now raised **only on a man's FIRST sanction**
(the `qing_had_yongying_already` fire-once guard), while repeat sanctions still grow his abstract
`qing_magnate_granted_veterans` tally — precisely mirroring the existing no-restack split in
`QING_magnate_track_grant` (`se_QING_MECHANICS.txt:221-232`). This keeps the create↔destroy ledger
exactly 1:1: **one magnate → one physical 勇營 → disbanded on his full break**. The multi-army reality
is still expressed — each *distinct* Han governor sanctioned gets his own legion; it is only
re-sanctioning the *same* man that no longer stacks legions. No unbounded pile.

(The pension lever's own 730-day cooldown, `se_QING_MECHANICS.txt:304`, is the throttle precedent;
the fire-once marker is the more precise fit here since the bound object is per-character.)

## Out of scope
- The abstract-only grants elsewhere (`qing_roster.4.b`, `qing_office.4.b`) are INTENTIONAL "power
  base bound by gratitude" flavour — their tooltips say "power base"/"following", NOT "cohorts", so
  they are not the bug. Untouched.

## Edit count (updated for disband symmetry)
FOUR edits, not two: (1) new `qing_office.42` trampoline; (2) new `QING_regional_army_raise_yongying`;
(3) rewire `QING_regional_army_bind_commander`'s if-branch to the trampoline; (4) **NEW** — add
`every_character_unit = { destroy_unit = yes }` to the marker-clear branch of
`QING_reassert_strip_magnate` (disband symmetry).

## Review gates: adversarial DESIGN review (this doc) → implement → adversarial POST-IMPL review.
NOTE: the running design review (agent ad5dc10127c852f5c) was dispatched BEFORE the disband-symmetry
amendment — its verdict does NOT cover the new edit (4). Re-review edit (4) before commit.
