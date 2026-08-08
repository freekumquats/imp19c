# DESIGN — The Hoppo made concrete (#66 / #68 / #69 / #70)

**Date:** 2026-08-08. **Scope:** turn the 粵海關監督 (Hoppo) from an abstract squeeze meter
into a real character whose graft is visible and consequential. Four boot-reported gaps,
one coherent loop.

## The gaps (from the boot test)
- **#66** The Hoppo is referenced as a character (the `qing_canton.1` "Hong Merchants Cannot
  Pay" event, the "Rotate the Hoppo" button) but there is **no Hoppo character at game start**
  and **no UI to see him**. Root cause (code-verified): `QING_canton_init` (se_QING_CANTON.txt)
  seeds only the bookkeeping vars (`qing_canton_customs`, `qing_hoppo_squeeze`=30, …) — it
  never appoints a `qing_hoppo_holder`. The holder is created **only** when the player clicks
  Rotate. So on a fresh game the Canton window shows a squeeze number with no man behind it.
- **#69** The squeeze is an abstract 0..100 meter that drifts up on its own. The user wants the
  Hoppo's **character corruption** to drive his siphoning, and the siphon to be **real character
  wealth** (concrete-over-abstract standing rule).
- **#68** Reining in a corrupt Hoppo is purely abstract (`qing_canton.1.b` just nudges the
  squeeze meter down). A **significantly corrupt** Hoppo (corruption > 10) should be **actually
  impeached by the Censorate** — the real disgrace machinery.
- **#70** (done separately, upstream of this) Impeaching the venal now **confiscates the
  target's character wealth into the treasury** (抄家) — which is exactly the Hoppo's siphoned
  hoard once #69 makes it real.

## The loop (how the four close on each other)
Seed a Hoppo at game start (#66) → each quarter his **corruption creeps up** and he **siphons a
slice of the Canton yield into his own character wealth** (#69), shown on his portrait card in
the Canton window (#66) → when he is **corrupt > 10**, "Rein in the Hoppo (dispatch an
Inspector-General)" **impeaches him through the Censorate** (#68), which **confiscates his
siphoned hoard into the treasury** (#70). The squeeze meter becomes a **derived reflection of
his corruption**, not an independent drift.

## Implementation (proven idioms only)

### se_QING_CANTON.txt
1. **`QING_canton_appoint_hoppo` (new, extracted).** The ablest-finesse-courtier pick currently
   inside `QING_canton_rotate_hoppo` (the `ordered_character … order_by = finesse max = 1`)
   moves into its own scripted_effect. `QING_canton_rotate_hoppo` calls it (relieve-then-appoint,
   unchanged player path); `QING_canton_init` and the pulse backfill call it too. Same inline
   depth as today for the button path (no new #443 exposure — it is a scripted_effect call, and
   the existing #389 rotate already reaches this iterator from the button and boots).
2. **`QING_canton_init`** — after seeding vars, **appoint a Hoppo if none exists** so he is present
   from turn one. A fresh appointee has low/zero corruption → low squeeze (honest new broom).
3. **`QING_canton_pulse`** — replace the free-floating squeeze drift with the concrete model:
   - **Backfill**: if `qing_hoppo_holder` is unset or dead, appoint one (he must always exist so
     the window and impeachment have a subject).
   - **Graft creep**: the seated Hoppo's own vanilla `add_corruption` climbs (+1/qtr, capped
     < 90); the `qing_hoppo_regulation_bias` (board-audited −1 / tax-farmed +1) now adjusts the
     **corruption** creep (the source), not the meter.
   - **Siphon → real wealth**: he pockets a slice of this quarter's yield scaled by his
     corruption — `siphon = yield_tmp × corruption / 200` (corruption 30 seed ≈ 15% of the
     quarter's take; 100 ≈ 50%). `add_gold` to the Hoppo (his personal hoard). This is money
     that never reaches the throne, so the emperor/state split is computed on `yield − siphon`.
   - **Squeeze is derived**: `qing_hoppo_squeeze = the Hoppo's corruption` (clamped 0..100), set
     from a saved scope each pulse. All the existing squeeze consumers (Cohong-crisis gate,
     yield ×0.7 shave, corruption-level leak) keep working, now driven by the concrete stat.
   - **Vacant** (only transiently, before backfill): squeeze drifts +3 as today.

### gui/qing_province_reports.gui (`qing_canton_window`) — #66
Add a **Hoppo portrait card** at the top of the window (below the desc, above the customs
read-outs): `cpt_button` datacontext `Player.MakeScope.Var('qing_hoppo_holder').GetCharacter`,
his name, his **corruption** (icon_corruption + `GetCorruption`), and his **wealth** (the
siphoned hoard). Hidden when no Hoppo (guarded on the var). The party/bloc "C" chip is not an
issue (he is a CHI courtier, `icon_card`), so no PartyIcons suppression needed.

### events/qing_canton_events.txt (`qing_canton.1.b`) — #68
"Rein in the Hoppo — dispatch an Inspector-General (御史)". If a Hoppo is seated **and his
corruption > 10**, save him as `scope:qing_censorate_target` and run `QING_censorate_impeach_uphold`
(disgraces him, strips his post, and **confiscates his siphoned wealth** via #70), then clear
`qing_hoppo_holder` so the pulse backfills a clean replacement. If he is **not** corrupt enough
(≤ 10), keep the old abstract "restraint" outcome (squeeze/corruption-level nudge) — an
honest-ish Hoppo cannot be impeached, only cautioned. Tooltip states both branches.

## Balance guard (I have been wrong on the economy before)
- The siphon `× corruption / 200` is bounded: max 50% of a yield already capped at 45萬兩/qtr,
  so ≤ ~22萬兩/qtr into his purse — a plausible personal fortune over a 3-year term, not a
  treasury-wrecking figure. It reduces the throne's take by the same amount (money moved, not
  created). No new currency is minted; `add_gold` to a character does not touch `add_treasury`
  or the money supply.
- Confiscation on impeachment returns the hoard to the treasury (one-shot), so the loop is
  conservative over a full graft→impeach cycle.

## Verification / review
Proven idioms: `add_corruption` (se_QING_HOUSEHOLD.txt:223), `add_gold = { value = … }`
(HOUSEHOLD:534), `save_scope_as` on a var-held char + `scope:X.corruption/.wealth`
(HOUSEHOLD:373), `add_treasury = { value = scope:X.wealth }` (#70, MARCH:506 shape). Dispatch a
code-review on the full diff before commit (mandatory review-before-commit).
