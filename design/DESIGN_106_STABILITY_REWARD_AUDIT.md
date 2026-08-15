# DESIGN — #106: event-reward stability audit (too many/too large, convert some to PI)

## Request
Direct user report: too many event options grant stability, some grants are too large, and
some should be converted to political influence instead.

## Scope
Audited every `add_stability` grant that is a positive, event/effect-reward context (excluded:
negative penalties, and the passive `QING_dynasty_harmony_nudge`/harem/pulse-style drift
mechanics already covered by other tasks). Found 20 sites via `rg "add_stability"` across
`events/` and `common/scripted_effects/`.

## Findings and disposition, site by site

| Site | Was | Disposition | Reason |
|---|---|---|---|
| `se_QING_JUSTICE.txt:92` (`QING_justice_fair_assize`) | +10 | **-> +6** | outsized vs `STABILITY_TARGET=45`; live, called from `qing_justice_events.txt:73` |
| `qing_justice_events.txt:284` (`qing_justice.4.a`) | +10 | **-> +6** | same cut, sibling grant |
| `qing_integration_capstone_events.txt:75` (`qing_integ.30.a`) | +5 | **-> PI 15** (stability dropped) | already carries +20 legitimacy; a triumphal ceremony is a political-standing display, converted per user's PI-conversion ask |
| `agitator_sponsorship.txt:355` (`agitator_sponsorship.2.b`) | +5 | **-> PI 12** (stability dropped) | banishing a foreign-sponsored agitator is a diplomatic/political win, not a domestic-order lever |
| `se_QING_RITES.txt:172` (`QING_rites_dispute` orthodoxy) | +5 | **-> +3** | live, one-shot, thematically fits stability (settled order) |
| `FlavorEvents.txt:839` (`flavor_eve.13.c`) | +5 | **-> +3** | crackdown-restores-order theme fits stability |
| `agitator_sponsorship.txt:716` (`agitator_sponsorship.5.b`) | +5 | **-> +3** | NOT converted to PI — this option already spends `-3 PI` as its own cost; converting the reward too would wash out the intended treasury+PI-for-order trade-off |
| `se_IDEOLOGY_APOTHEOSIS.txt:42` (`ideology_apotheosis_conservatism_effect`) | +5 | **unchanged** | vanilla-derived per-ideology deification reward (monarchism->legitimacy+popularity, nationalism->manpower/mil-xp, socialism->food) — conservatism's reward IS stability by design; changing it breaks the pattern, and it's a rare capstone, not a frequent grant |
| `se_QING_JUSTICE.txt:47` (`QING_justice_pulse`, capable-holder branch) | +5 | **unchanged, flagged** | confirmed via `rg` that `QING_justice_pulse` has ZERO call sites anywhere in the codebase — dead code, never fires. Not a live contributor to the reported problem. Left as-is (removing dead code is out of scope for this task); worth a future cleanup pass. |
| `00_ambitions.txt:1006` (`ambition_become_dictator_finish`) | +10 | **out of scope, unchanged** | generic vanilla-adjacent Imperator ambition system (become-dictator), not a Qing-specific mod event the user was reporting on; touching shared/vanilla mechanics without a diagnosed bug is out of scope per the Sobisonator-caution standing rule |
| 8 remaining `+3` sites (`se_QING_EARLYINDUS.txt:220`, `se_QING_REFORM.txt:59`, `qing_character_events.txt:176`, `qing_integration_capstone_events.txt:578`, `FlavorEvents.txt:118/138/818/1061`) | +3 | **unchanged** | already modest, within the "not too large" band |

## Net effect
- 2 sites cut from +10 to +6 (outsized single grants trimmed).
- 2 sites converted from +5 stability to political influence entirely (15 and 12).
- 3 sites cut from +5 to +3 (modest trim, kept as stability where thematically core or where
  converting would cancel an existing PI cost in the same option).
- 3 sites explicitly left alone with a stated reason (per-ideology design, dead code, out-of-scope
  vanilla system).

## Loc updated
- `qing_integ_capstone_l_english.yml` (`qing_integ.30.a.tt`): "legitimacy and stability" ->
  "legitimacy and political influence".
- `mod_events_l_english.yml` (`agitator_sponsorship.2.b.tt`): hardcoded "@stability! +5" ->
  "@political_influence! +12".
- All other touched sites had no hardcoded stability number in their loc (generic wording or no
  dedicated tooltip), so no further loc changes were needed.

## Guess-and-log
The exact cut ratios (+10->+6, +5->+3, PI values 12/15) are best-guess tuning constants, not
derived from a formula — there is no in-repo "correct" stability-per-event baseline to calibrate
against beyond `STABILITY_TARGET=45` (defines). Logged per the standing "guess and log"
convention; the next several campaigns' observed stability trajectory is the real confirmation.
