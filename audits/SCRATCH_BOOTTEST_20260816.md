# Scratch — 2026-08-16 boot-test fix pass

Working doc for the 10-item backlog from tonight's boot test + log/screenshot audit
(see `~/Downloads/scratch_logs_screenshots.md` for the raw log evidence). Mechanical
fixes go straight to implement. Anything with real design uncertainty gets a
diagnosis -> design -> implement -> review pass, logged below as it happens.

## Status board
1. Village Smithy icon (modern photo) — DONE
2. Sulphur cottage building unbuildable (no GUI wiring) — DONE
3. Construction-generic icon (illegible schematic) — DONE
4. Quarterly income tooltip (missing rows / topbar mismatch) — DONE (root cause: three prior fixes edited dead, unreferenced loc)
5. Imperial Household / Art Patronage duplicate buttons — DONE
6. Xinjiang/caravan double-fire (shared slot gap) — DONE
7. Cottage industry not moving Military Supplies (produced-vs-supplied gap) — DONE (reframed: magnitude bug, not a broken pipe)
8. Salt Gabelle revenue 10x cut — DONE
9. GC/subpost salaries not actually paying — DONE (not yet independently reviewed, see note below)
10. "A Dispute at Kashgar" over-firing (qing_caravan_events.txt:379) — DONE

## Item 8 — Salt Gabelle 10x cut (mechanical, DONE)
`se_QING_SALT.txt`, `QING_salt_income`: added `change_variable = { name = qing_salt_income_tmp
multiply = 0.1 }` right after the character-factor multiply and before the floor/pay block —
same pragmatic-cut approach as #102's tariffs cut. Every upstream factor (output cap,
market-soft, gabelle markup ×3.0, character factor) keeps its tuned shape; only the final paid
amount drops. Brace-balanced (163/163).

## Item 7 — re-diagnosis: the pipe is NOT broken, the magnitude is too small (DONE)
Traced the full chain: `COTTAGEIND_military_goods_building_bonus` adds directly to
`early_munitions_stockpile`/`clothing_stockpile`/`pharmaceuticals_stockpile`/
`construction_materials_stockpile` (right ordering -- runs before `CONSUME_all_stockpiles` in
`oa_wealth_changes.txt`) -> `CONSUME_from_stockpile`/`CONSUME_update_shortage` correctly
recompute `shortage_<good>` from the boosted stockpile (governorship-scoped, no clobbering) ->
`MILITARY_supplies_income_country` correctly sums `DEMAND_<good>_from_military x (1 -
shortage_<good>)` for exactly the 4 mapped goods. Every link is wired correctly. The
"Produced by good" vs "Supplied by good" tooltip gap for pharmaceuticals/construction materials
(150-700x) is ALSO not a bug -- "Supplied" is deliberately the MILITARY's own small demand slice
times fulfilment, not total national production, so a huge gap against total output is expected
whenever the military's own need for a good is a small fraction of total civilian+military
demand (true for pharma/construction, not true for clothing, which has a real, large shortage).
**Real root cause**: `GOODS_cottage_military_goods_output` (the per-building rate) was 0.2 --
confirmed via the reconstructed log data (3 quarters, `military_supplies_income`/`balance`
frozen bit-for-bit despite real production drift) to be too small to move the headline at all.
The rate's own derivation comment was self-contradictory: it says the bonus "bypasses
COTTAGEIND_scale_production's own discount chain" but then re-applied that exact chain's x0.1
discount anyway, undercutting its own stated purpose. **Fix**: removed the redundant x0.1,
using the plain undiscounted average of the 4 modern-industry per-building analogs (2), matching
what the bonus's own design always claimed to be. 10x increase, same file/mechanism, no new
code. This is the same class of fix as #8 (Salt Gabelle) and the standing "fixes must be
visible, not token" rule -- a technically-wired-but-imperceptible bonus is not a working fix.
Brace-balanced (1040/1040).

## Item 4 — real root cause found: three prior fixes edited DEAD loc (DONE)
The loc string all three prior #99 fix attempts edited (`imp19c_nation_treasury_tooltip`,
`localization/english/text_l_english.yml`) is **referenced by zero .gui files** -- confirmed by
a repo-wide grep. It is completely dead. The tooltip the player actually sees on hovering the
topbar income figure (`gui/ingame_topbar.gui:794`, `tooltipwidget = { nation_treasury_tt = {} }`)
is a totally separate, structured table widget (`gui/shared/custom_tooltip.gui:687`, `type
nation_treasury_tt`), built from individual `string_income_information` rows each bound to its
own script-value/variable accessor -- not a single big loc string at all. This explains
everything: why the screenshots showed "State monopolies & customs" and "One-off windfalls"
missing (they were never rows in the REAL widget, only in the dead string), why editing the dead
string 3 times never changed anything the player saw, and why the topbar number and its tooltip
never reconciled (the real widget was simply incomplete, not buggy-math).
**Fix**: added both missing rows directly to the REAL `nation_treasury_tt` template --
`topbar_tt_quarter_smc` (State monopolies & customs, `INCOME_national_total_from_qing_revenue`,
a script value) and `topbar_tt_quarter_oow` (One-off windfalls,
`INCOME_national_total_from_oneshot_grants`, a real stored variable per #99's own fix) -- new loc
keys added matching the existing `topbar_tt_quarter_*` naming convention, inserted in the same
order the dead string always had them. The Administrator wages / Military wages rows in this
SAME real widget automatically pick up item #9's new wage payments too, since they read the exact
`INCOME_cost_administrator_wages_country`/`INCOME_cost_military_wages_country` script values #9
fed. TODO row confirmed intentional (user), left untouched. Brace-balanced; loc quote-parity
checked. The dead loc string was left in place (not deleted) -- flagged here for a future
cleanup pass, out of scope for tonight's fix.

## Item 9 — GC/subpost salaries not actually paying (major feature, diagnosis+design below)

**Diagnosis.** `monthly_wage_for_character` is a vanilla Jomini-engine modifier field (used
throughout `common/offices/00_monarchy.txt` etc.), read natively by the engine to pay a
character a percentage of "nation's income" every month, and it's what #101/#5 attached to all
11 Qing-added wage-bearing character modifiers (GC base seat, Chancellor bonus, amban, salt/
caravan/hoppo/opium commissioners, customs IG, zongli diplomat, censor-inspector, imperial
guardsman). Screenshots confirm the engine DOES read the modifiers correctly (the wealth tooltip
correctly lists each modifier by name/value and computes a plausible combined percentage, e.g.
1.64% for the Chancellor) but the resulting absolute payment is exactly 0.00 in every observed
case, including a non-Qing vanilla-styled office (Minister of Culture, 0.99% of income) --
consistent across very different percentages, which only makes sense if the underlying "nation's
income" *this specific vanilla formula reads* is itself ~0 in this heavily-customized economy.
This mod runs its own parallel, fully custom income system (`INCOME_national_total_quarterly`
etc., paid via scripted `add_treasury`) alongside the vanilla engine's native economy -- the
standing `imp19c-two-trade-systems` pattern. It's a reasonable, well-evidenced read that whatever
native stat `monthly_wage_for_character` scales against was never populated by this mod's real
income flow, since real income never touches vanilla's own income-tracking path. Cannot verify
vanilla engine internals directly (closed source, no access), so this is the best-evidenced
diagnosis available, not a proven root cause -- flagged honestly.

**Design decision.** Given the uncertainty above, don't try to fix vanilla's internal accounting
(invasive, unverifiable). Instead replace `monthly_wage_for_character` on all 11 modifiers with a
new, mod-scripted, DIRECT payment effect using the same proven `add_gold` idiom already used for
the salt/Canton siphon and the Resident's Graft fix (cross-scope `value = 0  add = ROOT.var:X`).
Pay quarterly (alongside the other quarterly income cycles) as `rate x INCOME_national_total_quarterly`
-- the mod's own real income figure, the same one the tooltip and topbar read, so payment is
finally grounded in a number that's actually nonzero. Per user directive, split into two new
national cost-accumulator vars so item #4's tooltip can surface them:
- **Military wages** (`WAGE_gc_military_paid_last`): War seat, Guard Commandant seat, and the
  Guard Commandant's subordinates (the imperial guardsman corps).
- **Administrator wages** (`WAGE_gc_admin_paid_last`): every other seat/post (personnel, revenue,
  rites, justice, works, censor, lifanyuan, chamberlain, zongli, grand_secretariat GC seats;
  Chancellor's bonus; amban; salt/caravan/hoppo/opium commissioners; customs IG; zongli diplomat
  and censor-inspector subposts).
Scoped-down honestly: does NOT replicate vanilla's corruption/popularity discount multiplier the
broken mechanic was computing (visible in the old tooltip's "x0.82 due to corruption/popularity")
-- flat rate x real income only. Re-adding that discount is a reasonable future refinement, not
required to make the core bug (zero payment) real.

## Item 9 — implementation (2026-08-16)
New file `common/scripted_effects/se_QING_WAGES.txt`: `QING_pay_officeholder_wages` (quarterly
entry point) + 3 helper macros (`QING_pay_gc_seat_wage`, `QING_pay_single_post_wage`,
`QING_pay_marked_corps_wage`), all using the proven cross-scope `add_gold = { value = 0  add =
ROOT.var:X }` idiom (matches the Resident's Graft fix / salt-siphon precedent) and the proven
`ROOT = { ... }` re-entry idiom for country-scope writes from inside `every_character`
(matches `QING_subpost_staff_corps_minted`'s own `ROOT = { change_variable = ... }` line).
Pays: 12 GC seats (War + Guard Commandant -> military bucket; the other 10 -> admin), the
Chancellor's stacked bonus (admin), 5 single-holder commissioner/customs posts (admin), amban
via its character marker (admin), and the 3 subpost corps via their markers (zongli diplomat +
censor-inspector -> admin; imperial guardsman -> military, the Guard Commandant's own
subordinates per user directive). Publishes `WAGE_gc_admin_paid_last`/`WAGE_gc_military_paid_last`
each quarter. Wired into `oa_wealth_changes.txt`'s existing CHI-gated block, right after the
cottage/Military-Supplies probe.
Removed `monthly_wage_for_character` from all 11 modifiers it was on (qing_officeholder,
qing_officeholder_chancellor_bonus, the 4 commissioner offices, the 3 subpost offices, amban,
customs IG) -- confirmed non-functional, and leaving it would show a misleading "gaining X%"
tooltip line the player would never actually receive, on top of the real quarterly payment
landing separately. Single-field modifiers left as empty `{ }` markers (a proven, already-used
pattern in this codebase -- `absentee_father = {}`, the `fascination_with_*` modifiers), since
other code checks for their presence, not their contents.
Fed the two published accumulators into `INCOME_cost_administrator_wages_country`/
`INCOME_cost_military_wages_country` (`INCOME_svalues.txt`) as an additional `has_variable`-
guarded term each -- this is also #4's "hidden expense" fix, same root cause.
All touched files brace-balanced. **Not yet independently reviewed** -- this is the biggest,
most speculative fix in tonight's list (the vanilla-engine diagnosis can't be verified against
closed source); flagging for a dedicated review pass before calling it done.

## Item 6 — Xinjiang/caravan double-fire (diagnosis done pre-fix; DONE)
Root cause (from the log pass): `QING_xj_pulse` rolled a 15% chance, set `qing_xj_khoja_pending`,
and fired `qing_xinjiang.1` ("The Khoja Stirs") via `trigger_event` with NO shared-slot check at
all (`se_QING_XINJIANG.txt`). `QING_caravan_pulse` runs immediately after in the SAME quarter, by
design reads that same fresh flag, and fires `qing_caravan.2` ("The Road Is Cut") once IT claims
the shared `qing_gc_event_slot_used` slot -- which was still free, since xinjiang.1 never touched
it. One scare state, two events, same quarter, exactly matching the user's live report. The Qing
pacing overhaul (earlier tonight) never touched this pair.
**Fix**: added `NOT = { has_variable = qing_gc_event_slot_used }` to the khoja-scare roll's own
`limit=`, and `set_variable = { name = qing_gc_event_slot_used value = 1 }` inside the roll's
success branch -- the exact idiom already used at all 49 other claim sites (no `days=` param;
cleared by the existing `remove_variable` in `00_monthly_country.txt:80`, same as every other
site). Now only one of the pair can win the slot in a given quarter. Brace-balanced (357/357).

## Item 10 — "A Dispute at Kashgar" over-firing (DONE)
Root cause found via the full error.log ranked inventory: `qing_caravan_events.txt:379`
(`limit = { var:qing_caravan_contest_ok = 1 }` inside `qing_caravan.4`'s "negotiate" option) was
the single largest mod-specific error site in the entire log — ~5,166 hits for "unset scope" and
another ~5,166 for "invalid left side comparison" from that one line alone, plus ~5,203 more for
the underlying `qing_caravan_contest_ok` fetch failure across all 3 options (negotiate/coerce/
collude combined). The earlier #123 fix (`set_variable = { name = qing_caravan_contest_ok  value
= 0 }` placed BEFORE the `random` roll) was supposed to guarantee every read hit a valid 0/1.
Cross-checked against the real `LOG_line` messages each option's resolution emits
("caravan: the superintendent out-negotiates..." etc.): only **3** real option resolutions
happened in the entire boot, yet the error count was ~5,200 — proving the failures are not from
real play, but from the option's tooltip/effect-preview pass re-evaluating the WHOLE
`hidden_effect` block every time the event window renders, without committing ANY set_variable
inside it, including the pre-roll initializer #123 added (not just the one inside `random{}`, as
#123's own comment assumed). This is why the user saw the event "keep repeatedly firing" — the
window re-evaluating/re-rendering on every preview pass reads as repeated firing, even though the
underlying event only actually fired 3 times.
**Fix**: in all 3 options (negotiate, coerce, collude), dropped the pre-roll `set_variable = 0`
initializer and changed the read from `limit = { var:qing_caravan_contest_ok = 1 }` to `limit =
{ has_variable = qing_caravan_contest_ok  var:qing_caravan_contest_ok = 1 }`. `has_variable` is
only true after a REAL, committed `random` roll — a rolled-back preview pass now correctly reads
as "not set" and falls through to the existing `else` branch instead of erroring, with zero
gameplay change on a real click (the `else` branch's effects are unchanged). The 3 existing
`remove_variable = qing_caravan_contest_ok` calls at the end of each option are left unconditional
(a proven no-op-safe pattern in this codebase, e.g. `absentee_father = {}`-style empty-target
removals). Brace-balanced (185/185, whole file).
Shares its root file/chain with item 6 but is a DISTINCT bug (a preview-evaluation var-read
failure, not a missing shared-slot gate) — fixed independently, not as a side effect of item 6.

## Item 5 — Imperial Household / Art Patronage duplicate buttons (mechanical, DONE)
Both `gui/qing_household.gui` and `gui/qing_art_patronage.gui` independently defined all 4
buttons (Fund the Imperial Workshops, Commission the Painting Academy, Convene the Complete
Library, Make a Southern Inspection Tour) -- confirmed on screen. Per user directive: Imperial
Household keeps Convene the Complete Library + Make a Southern Inspection Tour; Art Patronage
keeps Fund the Imperial Workshops + Commission the Painting Academy. Removed the other pair from
each file (button widget + its comment, nothing else touched). Both files brace-balanced.

## Item 2 — Sulphur cottage building unbuildable (mechanical, DONE)
`qing_cottage_sulphur_pit_building` had a building def (`qing_cottage_buildings.txt:350`) and was
counted by `se_COTTAGEIND.txt:738`, but ZERO GUI wiring — confirmed missing: icon, build_item_
template, macro_build_item_ template, both tooltip templates, province_window.gui entry,
macro_builder_view.gui entry, macro-builder config allowlist entry, all loc keys. Mirrored the
`qing_cottage_sugarhouse_building` precedent exactly (same "pooled/specialized institution, not
generic craft" shape) at every site:
- Loc: name, desc, tooltip, macro-title (`qing_cottage_buildings_l_english.yml`).
- `gui/shared/gui_templates.gui`: `build_item_`/`macro_build_item_` types; also added a new
  `CottageIndustryItemsRow3` block, since Row2 was already at the proven 6-item/row max (same
  fix shape as #97/#98's IndustrialItemsRow3).
- `gui/shared/custom_tooltip.gui`: both tooltip templates.
- `gui/province_window.gui` + `gui/macro_builder_view.gui`: new Row3 blockoverride.
- `gfx/interface/macro_builder/config/00_default.txt`: added to the allowlist (else the new
  macro-builder entry renders empty, per the #97/#98 finding).
- Icon: no period Chinese sulphur-mining art exists on Commons; used the same-source Tiangong
  Kaiwu coal-mining plate (thematically closest mining scene, same source already used for this
  mod's other production buildings) via the existing fetch_wm.py/dds_icon.py pipeline.
All 5 touched files brace-balanced (counted, matched).

## Item 1 — Village Smithy icon (mechanical, DONE)
Old icon was a modern photo (car + modern building). Re-sourced via `fetch_wm.py` search
"Tiangong Kaiwu casting" -> File:Tiangong Kaiwu Tripod Casting.jpg (a genuine Ming-dynasty
woodblock illustration of men working furnaces/casting) -> converted via `dds_icon.py` to the
existing 200x200 donor format (`--like` qing_cottage_woodlot_building.dds). Visually verified.

## Log pass #2 (2026-08-16, /imp19c-logs re-run — logs.zip 17:30, screenshots 17:09-17:20)
Full details in `~/Downloads/scratch_logs_screenshots.md`. This boot predates the round-2
follow-up commits below (pushed ~17:55-17:58) -- confirms round 1 only.
- **Task 10 confirmed fixed**: `qing_caravan_contest_ok` errors are now 0 (was ~5,200/boot).
- **New bug found and fixed**: the single largest error class in the log (~78,000+ lines/boot
  across 3 error types combined, 5 call sites in 4 files) was `var:qing_current_post = flag:X`
  comparisons with no existence guard, introduced by an earlier #118 refactor that repointed
  these sites from a safe `has_variable=$marker$` check. Every character who never held any post
  (the vast majority of a country's character pool) threw this on every `every_character` pass.
  Pre-existing, not caused by this session's item 9 changes, though it touches the same subpost
  functions. Fixed all 5 sites (`se_QING_SUBPOSTS.txt` x2, `se_QING_MINISTRY.txt`,
  `se_QING_SOUTHERNSTUDY.txt`, `se_QING_UPPERSTUDY.txt`) with a `has_variable = qing_current_post`
  guard -- zero behavior change. Checked `se_QING_POST.txt`'s own unguarded dispatcher (a
  different, non-iterated call site) and found only 1 hit in the whole log -- not part of the
  flood, left untouched. All 4 files brace-balanced.
- Screenshots confirm items 2, 4, and 9's wage-counting are all working as designed on a real
  boot (State monopolies & One-off windfalls rows rendering; Administrator/Military wages rows
  much larger, reconciling close to the topbar's own quarterly-change figure; sulphur pit
  buildable in the macro builder).

## Follow-up round 2 (2026-08-16, live user feedback during re-test)

- **Khoja Stirs / Road Is Cut cadence.** The shared-slot fix (item 6) stopped the same-quarter
  double-fire, but user reported still seeing these too often, and stated directly: "once every
  few years is the correct cadence." Root cause: the khoja-scare roll's own base rate (15% per
  ~90-day pulse) averages under 2 years between rolls, with real variance -- never actually the
  problem item 6 targeted. Cut to 5% (`se_QING_XINJIANG.txt`), averaging ~5 years between rolls.
- **A Dispute at Kashgar cadence, real fix.** Re-checked after the same user complaint recurred:
  `qing_caravan.4`'s offer (`se_QING_CARAVAN.txt`) had **no chance roll at all** -- it fired
  unconditionally every pulse once both officials were seated, throttled only by a 270-day
  cooldown floor (~3 quarters between fires once both posts stay filled). Added a 5% chance roll
  around the existing slot-claim/cooldown/trigger_event, same idiom as the khoja fix -- the
  cooldown is now a floor under an already-rare roll, not the actual pacing.
- **Tooltip label style.** User: "State monopolies & customs" should shorten to "State
  Monopolies"; all row labels should be Title Case ("Tariffs and Shipping", "Subject Duties",
  "Administrator Wages", etc). Applied to every row in `nation_treasury_tt`'s loc keys
  (`imp19c_tooltips_l_english.yml`), including the header ("Quarterly Government Income").
- **Sulphur pit build-menu placement, corrected.** User caught a real placement error: I'd put
  the sulphur pit in a brand-new `CottageIndustryItemsRow3` (item 2) without checking whether an
  earlier row had room first. `CottageIndustryItems` (Row1) only held 4 of the proven 6-item
  budget -- moved sulphur pit there instead, and removed the now-empty Row3 block entirely
  (`gui_templates.gui`, `province_window.gui`, `macro_builder_view.gui`).
- **Military Supplies spending + supplies, doubled.** Direct user instruction: CHI should spend
  more on Military Supplies by default, and get more, both roughly doubled. Added a plain
  `multiply = 2` to `INCOME_cost_military_supplies_country` (the outgoing) and
  `MILITARY_supplies_income_country` (the "gains X/quarter" side) in `INCOME_svalues.txt` --
  `MILITARY_supplies_balance_country` reads from the income svalue, so it doubles automatically
  too, no separate edit needed. Same pragmatic-multiply-at-final-site style as the tariffs/salt
  cuts and the cottage-military rate fix.
- **Cottage-industry buildings seeded at 1763 start (new feature, not a bug).** Confirmed by a
  repo-wide grep: zero cottage buildings were seeded anywhere in `setup/` -- all 11 were
  100% player-built-only. User confirmed scope: seed every CHI-owned province that already
  qualifies under the building's own `allow=` gate (not a hand-picked subset), CHI only, not ROW.
  Found the exact proven idiom already in this codebase for this: `se_QING_BUILDINGS.txt`'s
  yamen/green-standard/community-granary block, explicitly documented there as the corrected
  model over hand-picked lists ("Capital-only lists were the wrong model"). Added:
  - A new `c:CHI = { every_owned_province = { ... } }` pass for the 8 trade-goods-gated cottage
    buildings (smithy/iron, leadworks/lead, weaving_hut/textile_fibres, silk_reeling_shed/silk,
    woodlot/wood, herbalist/vegetables, founders_workshop/copper-or-tin, quarry/stone), each
    mirroring its building's own `allow=` criteria exactly, guarded by `NOT has_building` for
    idempotency.
  - 25 calls to the existing `QING_seed_works_building` macro (already CHI-ownership-gated) for
    the 3 province-ID-gated buildings: sugarhouse (6 provinces), timber lineage (14 provinces),
    sulphur pit (5 provinces) -- exact same province-ID lists as each building's own `allow=`.
  Wired into `SE_qing_starting_buildings` (`se_QING_BUILDINGS.txt`), confirmed this function is
  actually invoked at boot for BOTH bookmarks (its sibling call right next to it is explicitly
  tagged `[bookmark-1763 #291]`, no gate between them) via `oa_economy_setup.txt`.
- **Wage tooltip still shows 0 income, even though wealth is visibly increasing (open, not fixed).**
  User confirmed the item 9 payment fix IS working (real wealth gain, confirmed). But the
  character wealth tooltip shows nothing for it, since `add_gold` is a quarterly LUMP grant, not
  a persistent per-month rate -- the same non-tooltip-visible behavior the salt/Canton siphon
  precedent already has (also silent). This is a real UX gap, not re-broken payment. Left open --
  building a "last wage paid" display would need new tooltip infrastructure, not attempted without
  an explicit ask.
- **Garrison commanders not earning salaries** -- reported, then retracted by user ("actually
  never mind I think they are earning, just very little"). No action taken.

## Follow-up icon audit (2026-08-16, user-requested after the boot-test list)
While fixing the Village Smithy icon, ran the repo's own `tools/qa_montage.py building` to
visually review every building icon at once. 13 looked like modern photos in the montage.
Checked each one individually (converted to PNG, viewed at full size) before touching anything:

**Confirmed bugs, re-sourced (7 DONE):**
- `qing_capital_granary` — was a modern building + parked cars. Now: a period Canton-waterfront
  painting (storage/warehouse theme).
- `qing_cottage_founders_workshop` — same bug class as the Smithy (modern car, modern building).
  Reused the Smithy's own Tiangong Kaiwu furnace-casting source (both are metalworking cottage
  buildings).
- `qing_dike` — was a modern satellite photo. Now: a detail from "The Qianlong Emperor's Southern
  Inspection Tour, Scroll Four: The Confluence of the Huai and Yellow Rivers" (Met Museum) — a
  genuine Qing court painting of the exact Yellow River hydraulic-works subject.
- `qing_grand_canal` — was a modern photo with a construction crane and skyscrapers. Now: a page
  from 廣輿圖 (Guang Yu Tu), a real Ming-dynasty atlas, showing the canal/waterway grid.
- `qing_likin_station` — was a modern Mediterranean mansion, wrong subject entirely. Now: "View
  of the Hongs, Canton" — a genuine period painting of the Canton trade/customs waterfront.
- `qing_tribute_depot` — was a modern concrete shed. Now: "Tribute Bearers" by Yan Liben and Yan
  Lide (Palace Museum, Beijing) — a genuine, famous Tang-dynasty painting literally titled for
  this building's theme.
- `qing_coal_mine` — was a modern European house with parked cars, wrong subject entirely. Reused
  the sulphur-pit icon's Tiangong Kaiwu coal-mining plate (the CORRECT subject for this building;
  it was only ever a closest-available substitute for sulphur).

**Confirmed bugs, left unresolved (2 OPEN — no viable art found, not forced):**
- `qing_oasis_bazaar` — the one real market-scene candidate (Along the River During the Qingming
  Festival) is an ultra-wide panoramic scroll; Commons only serves it as a 330x10px sliver,
  useless at icon scale. Nothing else on Commons matches "Central Asian/Xinjiang bazaar."
- `qing_yuelu_academy` — no painting or print of the academy exists on Commons; every hit is a
  modern photograph of the real, still-standing building (the same failure class as the original
  #96 bug -- "a photo of an old building" isn't period art).
Both still show their OLD (modern-photo) icon. Rejected two other candidates before landing on
the 7 above: a Tiangong Kaiwu grain-processing diagram (Figure-labeled technical illustration,
same "illegible schematic" problem the construction-icon fix already ran into) for the granary,
and a captioned tripod/bell-casting diagram (same problem) for the founders' workshop -- reused
the Smithy's clean, uncaptioned furnace scene instead.
Rejected as NOT bugs after individual review (period-appropriate as-is, left untouched):
`qing_foreign_concession` (genuine early-1900s photograph; the subject itself is a modern-era
institution), `qing_hanlin_academy` (genuine painted court scene), `qing_navy_yard` (genuine
1880s engraving of the Foochow Arsenal bombardment), `qing_telegraph` (genuine period engraving).
All 7 new icons visually verified at both source resolution and final 200x200 before committing.

## Item 3 — Construction-generic icon (mechanical, DONE — judgment call, flagged for review)
Old icon (#96's fix) was a Yingzao Fashi dougong bracket-joinery technical diagram — correct
period art by the title-vocabulary filter, but user reported it "looks like scratches on
paper," illegible as construction. Searched extensively for a Chinese-specific period
construction/scaffolding scene (Tiangong Kaiwu, Yingzao Fashi, Qing court paintings, Yuanmingyuan)
— none exist on Commons in a usable raster format. Used a 15th-c. German manuscript illumination,
"The Construction of the Tower of Babel" (Getty, via Google Art Project) — clearly, immediately
recognizable as a building under active construction (workers, scaffolding, materials being
hauled up). **Judgment call**: this has a simple rope-and-pulley hoist, which could be read as
brushing against #87's original "free of cranes" criterion. Read that criterion as targeting
anachronistic MODERN equipment (paired with "concrete" in the original commit message), not a
period rope hoist — but flagging explicitly since it's a real interpretation call, not a clean
mechanical swap. Easy to revert if the user disagrees — it's a single .dds file.
