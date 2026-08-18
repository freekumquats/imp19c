# Design: GC officeholder salary in the vanilla character WEALTH tooltip

## User request (verbatim, this session + carried spec)

Task #2: "The salary must appear in the vanilla CHARACTER WEALTH change tooltip
(`Wealth changes by [amount] each month due to: [source]`), NOT a separate GUI display.
Must apply to ALL GC offices AND their subordinates (diplomats, ambans, commanders, guard
captains)."

Hard constraint (verbatim, still in force): "GC positions were explicitly decided to NOT use
vanilla offices because that would add them to EVERY monarchy not just Qing. do not break that
rule / override the character wealth tooltip a different way."

Mid-task directive (verbatim): "just pay all of them a flat 1% rate if that makes it easier."

## Ground truth (diagnosed this session, all traced in source)

1. **The vanilla wealth tooltip is engine-generated.** Loc `MONTHLY_WEALTH:0 "#T Wealth#!\n
   Wealth changes by $CHANGE|+=2$@gold! each month due to:\n$WHY$"` (interface_l_english.yml:845),
   rendered by `[Character.GetWealthInformation]` (gui/shared/gui_base.gui:6119). It CANNOT be
   scripted directly. It aggregates the character's `monthly_character_wealth`-bearing modifiers:
   `$CHANGE$` = their sum, `$WHY$` = the itemized modifier list (each by its localized name).
   `monthly_character_wealth` is therefore the ONLY lever that puts a salary line there.
2. **`monthly_character_wealth` is proven in-mod** (01_schemes.txt x15, 00_from_events_character.txt
   x4, 00_military.txt x1). It is a flat, real gold-per-month character-wealth add. It is STATIC
   (a literal in the modifier definition) -- it cannot track a live "1% of income" figure.
3. **Every paid role ALREADY carries a persistent `duration = -1` character modifier**, added on
   appointment and removed on departure -- full lifecycle already wired, nothing to add:
   - 13 GC seats -> `qing_officeholder` (se_QING_COUNCIL.txt:1712, removed :1689/:1858)
   - chancellor -> `qing_officeholder_chancellor_bonus` (:1721)
   - salt/caravan/hoppo/opium commissioners -> `qing_{salt_commissioner,caravan_super,hoppo,
     opium_commissioner}_office`
   - zongli-diplomat / censor-inspector / imperial-guardsman subposts -> `qing_{zongli_diplomat,
     censor_inspector,imperial_guardsman}_office`
   - amban -> `qing_amban_resident` (se_QING_AMBAN.txt:188)
   All are currently EMPTY-or-flavour shells: task #9 stripped `monthly_wage_for_character` from
   them (that vanilla field reads the mod's zeroed vanilla nation income, so it paid 0.00).
4. **Real pay today is a quarterly `add_gold`** in `QING_pay_officeholder_wages` (se_QING_WAGES.txt):
   rate x `INCOME_national_total_quarterly` (1% most posts, 2% amban/zongli-diplomat, +1% chancellor
   stack), deficit-guarded (`> 0`). It is an instantaneous quarterly injection -- it does NOT and
   cannot appear in a "per MONTH" wealth tooltip.
5. **The income-tooltip linkage:** the quarterly snapshots `WAGE_gc_admin_paid_last` /
   `WAGE_gc_military_paid_last` feed `INCOME_cost_{administrator,military}_wages_country`
   (INCOME_svalues.txt:157-158/182-183), which feed the topbar income tooltip's wage rows. Any
   change to how wages are paid must keep feeding these two vars a QUARTERLY wage-cost figure or
   the income tooltip row goes stale/blank.
6. **The prior "panel display" (Task 5, b204b51d6) was REVERTED** (`9230a8dd0` + doc `b41c89d50`).
   It is NOT in the working tree. `QING_gc_office_wage_svalue` does not exist. Task #2 is a clean
   slate -- no panel to reconcile, and the revert confirms the user rejected the panel approach in
   favour of the vanilla tooltip.

## The core tension and how the user's directive resolves it

The tooltip requires a `monthly_character_wealth` modifier, which is STATIC. The current pay is
DYNAMIC (1% of live quarterly income). They cannot both be true: a static modifier cannot track
live income, and running BOTH the modifier and the add_gold would DOUBLE-PAY. Exactly one payment
channel must survive, and the tooltip requirement forces it to be the modifier.

The user's directive -- "just pay all of them a flat 1% rate if that makes it easier" -- resolves
this: convert the salary to a **uniform flat monthly wage** carried by the existing marker
modifiers. "Flat" authorises dropping the live income-scaling; "all of them ... 1% rate" authorises
a single uniform value (drop the 2%/chancellor-stack tiers). This is the simplest correct design.

## Design -- flat uniform `monthly_character_wealth` on the existing marker modifiers

### 1. Put a uniform `monthly_character_wealth = V` on each holder-borne marker modifier
- `qing_officeholder` (covers all 13 GC seats in one edit)
- `qing_salt_commissioner_office`, `qing_caravan_super_office`, `qing_hoppo_office`,
  `qing_opium_commissioner_office`
- `qing_zongli_diplomat_office`, `qing_censor_inspector_office`, `qing_imperial_guardsman_office`
- `qing_amban_resident`
- **`qing_officeholder_chancellor_bonus` is LEFT EMPTY.** The chancellor already carries
  `qing_officeholder`, so he receives V like everyone else. Adding V here too would pay him 2V --
  a tier the user's "flat ... 1% rate" directive explicitly removes.

Because these modifiers are already added/removed with each post, this needs ZERO new lifecycle
code. The salary appears in the wealth tooltip the instant a character is seated, and vanishes the
instant he leaves -- automatically. It is Qing-only (only Qing appointment paths grant these
markers), uses no vanilla offices, and does not touch/override the tooltip GUI -- fully inside the
hard constraint.

### 2. Remove the quarterly `add_gold` (else double-pay); convert `se_QING_WAGES.txt` to tally-only
The modifier now IS the payment. `QING_pay_officeholder_wages` keeps its holder-detection loops but,
per holder found, replaces the `add_gold` + income-read + deficit-guard block with a pure tally:
`change_variable WAGE_gc_$bucket$_paid_tmp += (V * 3)` (V = flat monthly wage; x3 = quarterly cost,
matching the quarterly figure `INCOME_cost_*_wages_country` expects). The two published snapshots
(`WAGE_gc_admin_paid_last` / `WAGE_gc_military_paid_last`) still get set, so the income tooltip row
stays correct. Bucket split unchanged (War + Guard Commandant seats + imperial guardsmen =
military; everything else = admin).

Simplifications this unlocks (all real, all traced):
- **No deficit guard needed.** Flat wages do not multiply by income, so the deficit-inversion bug
  (se_QING_WAGES.txt header bug #1: negative income -> negative pay) cannot occur. The guard is
  dropped because it is now provably dead, not to cut a corner.
- **No amban employer gymnastics for PAYMENT.** `monthly_character_wealth` pays the character
  regardless of employer, so the whole "amban is employed by the subject, not CHI, so the
  employer=ROOT filter missed him" problem (header bug #2) simply does not arise for payment. The
  amban is paid because he carries `qing_amban_resident`, full stop. (The tally still finds him via
  `has_variable = qing_amban_marker` and counts his V in CHI's admin bucket, preserving the prior
  income-tooltip accounting.)

### 3. Add loc names for the 7 markers that lack them
`qing_officeholder` ("Holder of High State Office (大員)") and `qing_amban_resident` ("Resident
Commissioner (駐紮大臣)") already have names. The other 7 (4 commissioners + 3 subposts) have none,
so the tooltip `$WHY$` line would show a raw key. Add a short titled loc entry for each so the wealth
tooltip reads e.g. "Salt Commissioner (鹽政)" etc.

## Chosen value V (GUESS -- Rule 1a, logged, boot-tunable)
`monthly_character_wealth = 5`, uniform. Rationale: sits squarely in the proven in-mod
`monthly_character_wealth` range (ambition mods run 2-24), a modest grandee stipend; quarterly cost
per holder = 15; with ~20-30 officeholders the total wage line is a few hundred gold/quarter, a
plausible small outlay. This is a FLAT stand-in for the old "1% of income" rate -- a static modifier
cannot track live income, and the user chose "flat" over scaling. If the next boot's wealth tooltip
(which now shows V directly) reads too high/low, V is the single tuning knob. No income figure was
available to calibrate against (newest log was 0 bytes).

## Rejected alternatives
- **Tiered income-scaled modifiers (quarterly remove-all-reapply, snap to a tier ladder).** Would
  preserve #9's income-scaling AND show in the tooltip, but needs a guessed tier ladder, a quarterly
  remove/re-add churn loop, and a chancellor double-tier -- a large, higher-risk rewrite of the
  just-fixed se_QING_WAGES.txt for a cosmetic-priority feature. The user's "flat ... if that makes
  it easier" directly rejects this in favour of flat.
- **Keep add_gold + a token display modifier.** Double-pays, and the tooltip value would not equal
  the real (income-scaled) pay -- dishonest. Rejected.
- **Vanilla offices / GUI tooltip override.** Forbidden by the hard constraint.

## LOUD REGRESSION NOTE (Rule 1)
This REVERSES task #9's income-scaling: officeholder pay is no longer 1% of live quarterly income;
it is a flat 5 gold/month per post. This is a deliberate, user-directed trade ("flat 1% rate if that
makes it easier") to satisfy the hard tooltip requirement, NOT a silent cut. Consequence: wages no
longer grow with the empire (arguably realistic -- fixed Qing stipends eroded under inflation), and
the deficit-inversion + amban-employer bug classes the #9 review fixed are now moot (flat pay can't
hit them). Logged here and in the overnight doc in the loudest terms.

## POST-REVIEW RESOLUTIONS (adversarial design review, 2026-08-17) — SUPERSEDES the claims above

The design review found 3 real gaps + 2 low notes. Each was re-verified in source THIS session
(not taken on the review's word) and resolved:

- **H1 (HIGH) — the Customs Inspector-General was MISSED.** The design's marker list had 9 markers;
  the 10th salaried post, the Customs IG (`qing_customs_ig_holder`, paid at se_QING_WAGES.txt),
  carries `qing_customs_inspector_general` (common/modifiers/qing_customs_modifiers.txt:57), NOT one
  of the 9. VERIFIED: char-scope, applied `duration = -1` at se_QING_CUSTOMS.txt:148, stripped
  :126/:175, and it ALREADY has a loc name ("Inspector-General of Customs (總稅務司)"). **Resolved:**
  added `monthly_character_wealth = 5` to it as the 10th marker; no new loc needed. Without this he'd
  lose pay while the treasury is still debited for him.
- **M1 (MEDIUM) — the Emperor Emeritus (太上皇).** VERIFIED: `QING_emeritus_take_office`
  (se_QING_EMERITUS.txt) calls `QING_office_appoint = { office = emeritus }`, which adds
  `qing_officeholder` (se_QING_COUNCIL.txt:1712), and the emeritus is employed by CHI. So putting
  wealth on `qing_officeholder` unavoidably pays him 5/mo. **Resolved:** rather than surgically
  exclude him (invasive — would fork the shared appoint path), FUND him: added
  `QING_pay_gc_seat_wage = { office = emeritus  bucket = admin }` so his treasury cost matches his
  pay. Thematically fine (a retired emperor drew imperial income). Rare abdication path; not a seat
  above, so no double-count. LOGGED as a deliberate scope consequence.
- **M2 (MEDIUM) — the regression note mis-framed the income vars as cosmetic.** VERIFIED: the wage
  tally is a REAL treasury outflow — WAGE_gc_*_paid_last -> INCOME_cost_*_wages_country
  (INCOME_svalues.txt) -> INCOME_national_total_quarterly -> `add_treasury` (se_INCOME.txt). The V*3
  = 15/quarter magnitude is CORRECT (matches 5/mo x 3). The header + regression note in
  se_QING_WAGES.txt now state this plainly (REAL outflow, not a display row).
- **L1 (LOW→corrected to load-bearing) — the chancellor block must be CONVERTED, not dropped.**
  VERIFIED against source, and it CONTRADICTS the file's own stale code comment: the chancellor is a
  DISTINCT 13th office (se_QING_COUNCIL.txt:669 "12 domain boards + chancellor"; autofill office=
  chancellor; `var:qing_office_held = flag:chancellor`), NOT a title stacked on a base seat. The 12
  `QING_pay_gc_seat_wage` calls do NOT include chancellor, so the chancellor block (:164-179) is his
  SOLE tally entry. **Resolved:** converted it to a flat V*3 admin tally (dropping it would leave the
  chancellor paid-but-not-debited). He still gets exactly V via `qing_officeholder`; the bonus
  modifier stays empty.
- **L2 (LOW) — accepted.** A stranded marker on a corpse is harmless: the engine does not tick a dead
  character's monthly_character_wealth, and the modifier leaves play with the character.
- **L3 (LOW) — accepted, verified.** The opium commissioner is NOT a `qing_current_post` family; its
  `qing_opium_commissioner_office` modifier is stripped on the only living-departure path (the
  per-pulse reconcile double-book relief, se_QING_OPIUM.txt:373-375) and death is engine-handled — so
  it cannot strand on a living non-holder to become a phantom salary. Same coverage as its siblings.

## Files touched (final, post-resolution)
- `common/modifiers/qing_governance_modifiers.txt` -- add `monthly_character_wealth = 5` to
  `qing_officeholder` + the 4 commissioner + 3 subpost `*_office` shells (8 blocks).
- `common/modifiers/qing_amban_modifiers.txt` -- add `monthly_character_wealth = 5` to
  `qing_amban_resident`.
- `common/modifiers/qing_customs_modifiers.txt` -- **[H1]** add `monthly_character_wealth = 5` to
  `qing_customs_inspector_general` (the 10th marker).
- `common/scripted_effects/se_QING_WAGES.txt` -- all 4 pay macros + chancellor block -> flat V*3
  tally; drop income-read/multiply/deficit-guard/add_gold and the now-unused `$rate$` param (+ its 8
  call-site args); **[M1]** add the emeritus fund line; **[L1]** convert (not drop) the chancellor
  block; **[M2]** rewrite the header/regression note (REAL treasury outflow).
- `localization/english/qing_governance_l_english.yml` -- 7 modifier-name loc entries (customs IG
  already named).
- overnight/OVERNIGHT_2026_08_17.md -- log + ASSUMPTIONS entry for V.
