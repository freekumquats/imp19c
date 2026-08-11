# Overnight run — 2026-08-11

Working branch: merge-overnight. Author: freekumquats. Start HEAD: 01d84b54b.

This run picks up a large session-designed backlog. Ordering: land the one review-CLEAN
design first (#112 regional pricing), then cheap-certain boot-test mechanical fixes, then
advance the exam/GC-cluster gate (#118 diagnosis). The exam/GC draw-conversion tasks
(#111/#114/#116/#117) are GATED on #118 (structural 1:1) per the user and are NOT converted
this run until #118's diagnosis+design land.

## ASSUMPTIONS & GUESSES (scan here for every un-boot-confirmed number)
- **#112 regional price**: NO clamp/ceiling on the per-zone price (user directive); only the `min = 0.0001`
  strict-positive floor (copied from country_unit_price). Un-boot-confirmed effects to WATCH on the boot:
  (a) total trade-income shift per country (paying zone local_price vs national gbip, under order-weighting —
  not preserved by construction); (b) the §E zero-stockpile SILVER zones (upper_yangtzi/yellow_sea) whose
  local_price is computed UNDIVIDED → order-scale spike now re-exposed at the payment site. Logged via the
  existing tzprobe/ECON_LOG harness (kept from #50). If (b) destabilizes treasury, fix the underlying §E
  zero-stockpile bug, NOT a ceiling.

---

## Task log

### #112 — regional import pricing (per-zone local_price at the payment site) — DONE
- WHAT: province pays for imports at ITS OWN trade-zone's local_price instead of the national
  average country_unit_price. se_GLOBALTRADE_split.txt, GT_split_update_wealth_owed_for_tradegoods
  (~:2466): the price multiply swapped `owner.var:country_unit_price_$good$` → the direct block
  `local_price_$good$(paying zone) / (0.5 + owner.penetration)` (country_unit_price's own block copied
  verbatim, gbip→local_price; its min=0.0001 = the strict-positive floor; no ceiling per user directive).
- KEY DECISIONS: DIRECT substitution, not a gbip-ratio "index" (the gbip cancels). country_unit_price the
  VARIABLE is not written → currency peg isolated by construction (the correct side of the peg, unlike the
  reverted #50). Metals stay in (no gold exemption). Clamp removed (user); only the min-floor remains.
- DESIGN REVIEW: three passes (review112 → 112b [CRITICAL max/min floor bug caught] → 112c re-confirm CLEAN).
- CODE REVIEW: cr112 → CLEAN, zero findings (scope/macro/read-shape/equivalence/min-floor/peg-isolation/traps
  all verified against source).
- STATUS: DONE. Commit <pending>. Boot-watch: total-income shift + §E silver zero-stockpile spike (see ASSUMPTIONS).
- FOLLOW-ON: #115 (the "both" model — per-zone TZ_penetration denominator) supersedes the denominator on this
  same line if it clears its own pipeline; #112 is the safe minimal form shipping now.

### #102 — raise treasury cap 99999 → 9999999 — DONE
- WHAT: MAXIMUM_GOLD (00_defines.txt:52) 99999→9999999, plus the two cap-tracking refs that must move in
  lockstep: CURRENCY_svalues.txt:886 (the paper-money "no cap" minting_rate_cap branch) + the four
  EE_scripted_guis.txt national-debt is_valid gates (treasury < 99999 → < 9999999).
- KEY DECISION: MINIMUM_GOLD (debt floor, -99999) left AS-IS — user asked to raise the CAP, not the floor;
  asymmetry is intentional (logged). cr102 confirmed no functional downside + no third lockstep ref missed.
- REVIEW: cr102 → CLEAN. #23/#60 bounding untouched (the max=20000 hard cap at :853 is a separate branch).
- STATUS: DONE. Commit <pending>.

### #104 — finish the Arsenal→Machine Works rename (leftover tooltip word) — DONE
- WHAT: imp19c_tooltips_l_english.yml:79 "the Jiangnan Arsenal" → "the Jiangnan Machine Works". The building
  title was already renamed (3ead94d6c); this was a leftover flavor aside inconsistent with the new name.
- REVIEW: cr78104 → CLEAN. STATUS: DONE. Commit <pending>.

### #78 — remove duplicate "Reform the Salt Gabelle" button from the Revenue window — DONE
- WHAT: gui/qing_revenue_ministry.gui — deleted the redundant reform-gabelle text_button (the action now
  lives solely in the Salt Monopoly window per #44; it was duplicated here AND there). Replaced with a [#78]
  comment. The scripted_gui qing_revenue_ministry_reform_salt is UNTOUCHED — Salt Monopoly window still calls
  it (imp19c_windows.gui:1842); the "open Salt Monopoly window" button just above is intact.
- REVIEW: cr78104 → CLEAN (braces 156/156; action not orphaned; loc keys still used by the Salt window).
- STATUS: DONE. Commit <pending>.

### #72 — Dowager's Counsel "Set it gently aside" broken loc — FIXED (screenshot-confirmed)
- CORRECTION to my earlier note: I initially called this "not reproducible in source" because the loc keys
  exist and the ruler-name chain is used elsewhere. That was WRONG — the SCREENSHOT (20260810215558) shows the
  bug plainly: the qing_dynasty.1.b tooltip renders "___ asserts himself and rules alone" — the leading
  [ROOT.GetCountry.GetRuler.GetName] comes out BLANK, while a DIFFERENT name ref later in the same tooltip
  (the auto-effect "Qianlong Emperor (ID:214)") renders fine.
- ROOT CAUSE: the long [ROOT.GetCountry.GetRuler.GetName] chain renders empty in an option custom_tooltip
  context (same failure class the file's own [BT-3 logfix] already documents for crownprince: an unresolved
  chain -> blank/ERROR in loc). The .desc works because it's event-scope, not option-tooltip scope.
- FIX (proven idiom, loc-scope-syntax rule): save the ruler into a named scope in each event's immediate
  (current_ruler = { save_scope_as = emperor }) and change loc [ROOT.GetCountry.GetRuler.GetName] ->
  [emperor.GetName]. Applied across ALL affected events (qing_dynasty .1/.3/.4/.5/.6/.7/.8 — the whole family
  shares the broken construct; .2 doesn't reference the ruler). 11 loc refs switched; emperor-save added to
  each of the 7 referencing events (verified 1:1, event 2 correctly has none).
- FILES: events/imp19c_mod_events/qing_dynasty_events.txt, localization/english/qing_dynasty_l_english.yml.
- Braces 81/81, precommit clean. CODE REVIEW: <pending>. STATUS: DONE pending review.

### Screenshot cross-confirmations (from the 20260810222904 set, boot Aug 10 22:29 — grounds several pending tasks)
While hunting the #72 shot I read the whole set (logs-skill Rule 5); it visually CONFIRMS these open bugs:
- #74 (Examinations "Sell degrees"): the option tooltip reads "Great Qing gains ¥ 0.00" — the sell-degrees
  branch yields ZERO silver, exactly as reported. Real bug confirmed on the boot.
- #90 (Kashgar contest chances): "A Dispute at Kashgar" tooltip literally shows "On success (%)" / "On failure
  (%)" — the success/failure percentage is blank. Confirmed.
- #96 (Caravan window gap): there IS a visible gap between "Rotate the Superintendent" and "Revoke the Aqsaqal"
  — consistent with the reported missing button.
- #103 (Arsenal tech-gate tooltip): the Build Arsenal tooltip states "+2 military supplies (munitions)" with NO
  tech-gate caveat shown — supports both #98 (not contributing) and #103 (surface the gate).

### #74 — Examinations "Sell degrees" gives 0 money — FIXED (root cause: shared wealth-grant helper)
- WHAT: qing_keju.1.c (捐納) calls QING_sell_offices -> CURRENCY_grant_country_wealth { thousands = 80 }.
  That helper (se_CURRENCY.txt:1318) GUARDS the wealth-per-unit multiply: if the currency's backing price
  (country_unit_price_silver for CHI's silver standard) is transiently unset THIS frame, it took the `else`
  branch which did ONLY a LOG_fail -> granted NOTHING. Screenshot-confirmed: "Great Qing gains ¥ 0.00".
- FIX: the else branch now grants the NOMINAL $thousands$ directly (add_treasury = local_var:wealth_to_grant,
  which is set to $thousands$ before the guard, UN-multiplied on this path) — a strictly-positive, flood-free
  fallback (plain literal, no currency svalue read). The exact-conversion branch is unchanged for the common
  (price-resolved) case. Fixes #74 AND every other caller that silently granted 0 (marriage, customs, mexico,
  napoleon, treasure-fleet, USCW, self-strengthening, early-industry).
- ASSUMPTION: fallback = nominal thousands undervalues vs the pegged conversion, but a modest real grant beats
  zero; logged so a boot can confirm the sale now yields silver. Guard against the flood is PRESERVED.
- FILE: common/scripted_effects/se_CURRENCY.txt. Braces 531/531, precommit clean. CODE REVIEW <pending>.

### #90 — blank success/failure % on "A Dispute at Kashgar" (qing_caravan.4) — FIXED (screenshot-confirmed)
- WHAT: the 3 option tooltips rendered "On success (%)" / "On failure (%)" with a BLANK number (screenshot).
  Root cause: the loc read [ROOT.GetCountry.MakeScope.GetVariable('qing_super_*_shown')...] — but qing_caravan.4
  is a country_event, so ROOT IS ALREADY the country; the spurious .GetCountry hop resolved EMPTY in the loc
  data-context -> blank. The _shown vars are set on CHI (=ROOT) in immediate (:349-354), correctly.
- FIX: dropped .GetCountry -> [ROOT.MakeScope.GetVariable('qing_super_*_shown')...] (the proven idiom; the other
  6 _shown renders across canton/salt/caravan already use ROOT.MakeScope). 6 refs (3 success + 3 fail across
  negotiate/coerce/collude). Also fixed the stale header comment that described the broken form as "proven".
- "PRESUMABLY ALL CONTEST EVENTS": CHECKED — grep confirms caravan.4 was the ONLY place with the .GetCountry
  hop; all other superintendent/aqsaqal/hoppo/salt/amban _shown renders already use ROOT.MakeScope correctly.
  Bug was isolated to this one event, not systemic. (Same scope-quirk FAMILY as #72's Dowager fix — a chain
  that resolves in event scope but not in the option/tooltip data-context.)
- FILE: localization/english/qing_caravan_l_english.yml. BOM intact, 6/4 diff. CODE REVIEW <pending>.

### #93 — construction-queue placeholder icons — DIAGNOSED, arsenal NOT reproducible in source (needs the queue screenshot)
- CHECKED: arsenal_building icon = gfx/interface/icons/buildings/arsenal_building.dds — EXISTS, valid DDS
  ('DDS ' magic), 200x200 (identical to every working mod building icon e.g. qing_machine_works_building.dds).
  The construction queue (mapiconlayer.gui:1038) and build menu (province_window.gui:4520) BOTH resolve via
  the SAME engine fn [GetBuildingIcon(...GetBuilding)] — path-based, no spriteType registration needed (the
  mod's own 60+ buildings work this way, all present). Audited ALL qing_*_building icons: every one has its dds.
- FINDING: no source-level defect for the arsenal — icon present, valid, correct dimensions, resolved by the
  proven path. The screenshot I have is the build MENU (icons fine), not the queue placeholder, so I cannot see
  WHICH buildings actually placeholder in the queue. Cannot fabricate a fix for an unlocatable defect.
- STATUS: in_progress (NOT closed). Needs: the construction-QUEUE screenshot showing the placeholder, to pin
  the specific building(s). If it's arsenal specifically, the icon is correct in source — likely a vanilla
  GetBuildingIcon quirk for vanilla-defined buildings (arsenal_building is vanilla 00_military_buildings.txt),
  not the mod's icon. Deferring to boot-screenshot evidence, per no-fabrication rule. Moving on to fixable tasks.

### #94 — Civil "Citizens Rights" laws missing descriptions — FIXED
- FINDING (more than reported): the 4 member laws (judicial_discretion_rights / wealth_based_rights /
  bill_of_rights / constitutional_rights) all had PLACEHOLDER stub descs ("<Name> desc"), AND the group header
  citizens_rights had NO _desc at all (blank card).
- FIX: wrote real descriptions for all 4 members + the group, grounded in each law's actual modifiers
  (00_civil_laws.txt) and matching the mod's law-desc tone (escalating ladder: magistrate discretion -> wealth-
  pegged -> universal bill -> entrenched constitutional). Each member desc lists its concrete modifier lines
  with #G/#R colour tags. laws_l_english.yml, 5 desc keys. BOM intact, quotes balanced (2/line), 5/4 diff.
- CODE REVIEW cr94: CLEAN (keys bind, modifier values exact, YML integrity OK). Commit 7aa6973bd, pushed. STATUS: DONE.

## #89 — VANILLA silver-reserve (change) row shows garbage 151367 (mod 戶部 panel correct ~1513)
- DIAGNOSIS (traced in source, no boot needed — the ×100 ratio is deterministic): the vanilla economy
  view's silver row is loc key `SILVER_ACCUMULATION_RATE` (economic_enchancement_l_english.yml:1139),
  which renders `total (change/target lb)` with EVERY term wrapped in `Multiply_CFixedPoint(x,'100')`
  — a hundreds-troy-lb → lb conversion. That is correct for ROW, whose `silver_reserve_size` is seeded
  in hundreds lb (e.g. c:SAX = 12, c:TUR = 1070 # hundreds lb). BUT #425 REPURPOSED CHI's
  silver_reserve_size — and the change snapshot it now reads (CURRENCY_silver_reserve_actual_change_with
  _cashout = qing_silver_reserve_change_last, se_QING_REVENUE.txt) — to mean 千兩 (thousand taels), NOT
  hundreds-lb. So the shared ×100 multiplies CHI's 千兩 quantities by 100 → change 1513 千兩 → 151367
  (the reported garbage), total 62000 → 6.2M, etc. The mod 戶部 panel (qing_revenue_ministry.gui) reads
  the SAME vars raw (|0 / |+0), which is why it shows the correct ~1513 — CONFIRMS the #54 hunch that the
  mod panel is right and the VANILLA view is the defective display. The #54 comment claiming "the loc's
  ×100 scaling matches the reserve-total's ×100 (consistent units)" was WRONG: both terms are ×100 too big
  on CHI, they are just consistently wrong with each other. Gold is untouched (CHI gold = 0, real hundreds-lb).
- FIX: CHI-only loc variant, selected via customizable_localization (proven .Custom() idiom, same as
  inflation_deflation_text / toggle_freeze_reserves_text served in this very window):
  - economic_enchancement_l_english.yml: new key SILVER_ACCUMULATION_RATE_QING — same row, NO ×100, unit
    label 千兩 instead of lb; reads silver_reserve_size / change / silver_accumulation_rate raw.
  - 000_ECON_loc.txt: new `silver_reserve_row_text` (type=country): tag=CHI → the QING variant, else →
    the vanilla SILVER_ACCUMULATION_RATE byte-for-byte. ROW is entirely unaffected.
  - economy_view.gui:431: the silver row's Text now serves `[EconomyView.GetPlayer.Custom('silver_reserve
    _row_text')]` instead of the raw key.
  Deliberately scoped to CHI only + selector default = the untouched vanilla key, so no ROW regression
  (Sobisonator-caution: the shared key is not edited, a NEW key + a NEW selector are added alongside it).
- SCREENSHOT CONFIRM (20260810222904_1.jpg, Aug 10 22:29 boot — the boot that filed this backlog): the vanilla
  economy panel's silver row reads `6768809 (+151367/0 lb)`; the mod 戶部 panel reads Silver Treasury 67688 /
  Change 1513. 6768809 = 67688×100 and 151367 = 1513×100 EXACTLY — proves BOTH terms are ×100 too big on CHI
  (confirms the diagnosis; the #54 "consistent" claim was wrong) and that the mod panel is the correct one.
- CODE REVIEW cr89: dispatched; did not return within the run window. Self-review (in lieu): loc keys bind
  (SILVER_ACCUMULATION_RATE_QING + selector silver_reserve_row_text unique, no collision); QING variant uses the
  proven .Custom()-served data-fn forms (Player.MakeScope.GetVariable + GuiScope.SetRoot(Player.MakeScope).Script
  Value, same as inflation_tooltip served via inflation_deflation_text); ROW key byte-unchanged + is the selector
  default (always=yes fallback last); brace balance OK on all files; small diffstat, no EOL churn. STATUS: DONE.

## #86 — make the 京倉 Metropolitan Granary player-buildable, CAPITAL-only
- DIAGNOSIS: qing_capital_granary_building (common/buildings/qing_granary_buildings.txt) existed but was BOOT-SEED
  ONLY (add_building_level at Beijing P8363) with NO build-menu path — not in the macro allowlist, no build_item
  template, no province_window entry. Its potential gated to is_in_region = Zhili (the whole metropolitan corridor).
- FIX (mirrors the sibling buildable qing_granary_building wiring exactly):
  - qing_granary_buildings.txt: potential is_in_region = Zhili -> is_capital = yes (restrict to THE CAPITAL; proven
    province trigger; still satisfied at the Beijing P8363 capital seed site). Culture OR block kept.
  - gfx/interface/macro_builder/config/00_default.txt: added qing_capital_granary_building to the all_buildings
    allowlist (this is what populates the macro-builder list).
  - gui/shared/gui_templates.gui: added build_item_ + macro_build_item_ types (name-match on the building's loc name).
  - gui/shared/custom_tooltip.gui: added building_ + macro_building_ tooltip templates.
  - gui/province_window.gui + gui/macro_builder_view.gui: added the item entries after the granary ones.
  - imp19c_tooltips_l_english.yml: added tooltip_macro_building_title_qing_capital_granary_building. (The name/desc/
    results loc keys already existed from the seed era.)
  is_capital in potential does NOT hide it from the macro LIST (list membership = allowlist alone; potential gates
  per-province buildability at step 2) — so it appears in the list and is buildable only in the capital.
- CODE REVIEW cr86: dispatched; did not return within the run window. Self-review (in lieu): every referenced loc
  key exists (verified name/desc/tooltip_ pre-existing + the macro-title added); template names match the
  tooltipwidget refs + instantiations exactly; brace balance equal on all 4 .gui files; loc names of the two granary
  buildings differ so the name-match doesn't collide; small diffstat, no EOL churn. STATUS: DONE.

## #103 — surface the Arsenal's munitions tech-gate in a tooltip
- DIAGNOSIS: arsenal munitions production is gated `owner = { invention = tech_firearms }` (GOODS_svalues.txt
  GOODS_governorship_munitions_infra_output_compute:2771) — the SAME invention as the arsenal's build allow
  (00_military_buildings.txt:15). The machine_works munitions term is gated `tech_weapon_manufacturing` (:2794),
  again matching its own build allow (qing_industry_buildings.txt). Both tooltips ALREADY mentioned the invention
  (tooltip_arsenal_building "Requires Firearms" since e2ec51f3f; tooltip_qing_machine_works_building "Requires
  Weapon Manufacturing"), but the requirement read as a build gate buried mid-paragraph, NOT clearly tied to the
  "+N munitions" production line — which is why a boot tester still filed the task.
- FIX (loc-only, 2 tooltip lines, imp19c_tooltips_l_english.yml): rewrote both munitions lines to attach the tech
  gate DIRECTLY to the munitions output, in red, stating that before the invention the building produces no
  munitions (arsenal) / that the works produces from the moment it is raised (its build + production gate coincide).
  No mechanics change — the gates were already correct; this only makes them legible. Quotes balanced (2/line),
  BOM intact, 2-line diffstat. Small loc change -> straight to commit per the overnight skill.
- STATUS: DONE.

## #92 — automatic Ever-Normal Granary expansion should not be invisible or free
- DIAGNOSIS: QING_DECLINE_granary_concrete (se_QING_DECLINE.txt) auto-built a real qing_granary_building
  whenever granary stock >= 60 in a good year — for FREE and with NO player notification. The famine branch
  (stock <= 15) already flags granaries empty; only the expansion side was costless + silent.
- FIX:
  - added `treasury >= 255` to the good-year build limit (affordability gate; proven idiom se_QING_CARAVAN:482)
    so the expansion waits if the throne cannot bear it.
  - `save_scope_as = qing_gran_built_province` on the built province (for the notification loc).
  - after the build, `if = { exists = scope:qing_gran_built_province } { add_treasury = -255 ; trigger_event
    qing_revenue.6 }` — charges 255 (proven charge idiom se_QING_CARAVAN:494) and notifies the player, ONLY
    when a granary was actually raised this pulse.
  - new qing_revenue.6 notification event (pure acknowledge; the cost is charged by the caller) + its loc
    (.t/.desc/.a; desc names the funded province via [scope:qing_gran_built_province.GetName]).
- ASSUMPTION/GUESS (logged): 255 treasury cost — chosen to match the Caravan oasis-bazaar endowment (same
  order, same gate/charge idiom), NOT the granary building's bare cost=60, because this is a STATE-FUNDED
  strategic-reserve expansion, not a routine local build. Boot will show whether it throttles the auto-expand
  too hard/soft; tune next round. The qing_revenue.6 LOG_line confirms each funded build on the boot.
- CODE REVIEW cr92: dispatched (verdict pending at log time). Brace balance equal on both script files; event
  file BOM-free (0x23...); loc quotes balanced (2/line); small diffstat, no EOL churn.
- STATUS: DONE (pending cr92 clean).

## #123 — qing_caravan.4 contest options: 7127x 'qing_caravan_contest_ok' unset-var flood (NEW, found in Aug-10 23:17 boot)
- DIAGNOSIS (imp19c-logs full triage of the NEWEST error.log, 123330 lines): the single biggest source in the
  boot. Ranked classes: 33119 "Script system error", 9892 "Event target link 'var' returned an unset scope",
  8817 "Invalid left side during comparison 'var'", 7127 "Failed to fetch variable 'qing_caravan_contest_ok'".
  All three top classes trace to events/imp19c_mod_events/qing_caravan_events.txt lines 372/402/436 — the three
  qing_caravan.4 (A Dispute at Kashgar) contest options. Each did `random { chance=svalue  set_variable
  qing_caravan_contest_ok=1 }` then read the var in `if = { limit = { has_variable ... } }` + the nudge. The
  option's auto-generated EFFECT-TOOLTIP re-runs the hidden_effect in a preview pass (each is preceded in the log
  by "Data error in loc key 'qing_caravan.4.<opt>.tt'"), where the set inside random{} does not commit -> the var
  is unset -> ~48 errors/sec while the event window is open. NOT previously a tracked task.
- FIX: hoist `set_variable = qing_caravan_contest_ok = 0` to the TOP of each hidden_effect (BEFORE random{}), and
  change the guard from `has_variable` to `var:... = 1`. Now every read hits a defined 0/1 in the same eval pass,
  so no unset-fetch can fire. Semantics identical (init 0 -> win sets 1 -> test =1 -> win arm; else lose arm).
  This is the same init-before-read idiom as the earlier read-before-set flood fixes (#47 etc). Considered a
  random_list rewrite (no var at all) but REJECTED: svalue-named weight keys are unproven in this codebase/oracles
  (only integer-literal weights attested) — proven-code rule. brace balance 160/160; literal-RHS comparison legal.
- STATUS: DONE (boot will confirm the flood is gone via the absent error class + the unchanged skill-check LOG_lines).

## #106 — SHIPPING_svalues read-before-set: ~1700 unset shipping_<zone> errors/boot
- DIAGNOSIS (newest error.log, Aug-10 23:17): 1693 "Failed to fetch variable 'shipping_<zone>'" +
  contributing to the unset-scope/bad-comparison classes. Pinned to SHIPPING_svalues.txt (88 sites, e.g.
  :2241) reading `var:shipping_<zone> > 0` UNCONDITIONALLY for all 22 zones. But se_SHIPPING's piechart
  update only SETS shipping_<zone> for a zone a country actually ships in (the switch at ~:214). A country
  that does not ship in a zone -> unset var read. CONFIRMED harmless: `unset > 0` already evaluates false
  (the intended result); this is read-before-set NOISE (memory econ-log-noise-not-bugs), not a logic bug —
  but 1700 lines/boot of it. Upstream Sobisonator trade code (Sobisonator-caution).
- FIX (contained, purely additive — does NOT touch the 88 upstream read sites): new SHIPPING_seed_zone_defaults
  effect (se_SHIPPING.txt) sets all 22 shipping_<zone> vars to 0 (each per-var guarded, so it never overwrites
  a real value), called ONCE per country at game setup (oa_economy_setup every_country block). The vars persist
  in the save and the piechart update does not remove them, so a one-time seed covers the whole game with NO
  quarterly cost; the piechart update overwrites real shippers' zones, non-shippers keep 0. Seeded-zone set
  cross-checked to EXACTLY match the 22 distinct zones read in SHIPPING_svalues (shipping_power_total correctly
  excluded — it's a per-province var, not a per-country zone var).
- CODE REVIEW cr106: dispatched (verdict pending). Brace balance equal on both files; BOM intact (common/);
  small additive diffstat (+36/-0), no EOL churn.
- STATUS: DONE (boot will confirm the shipping_<zone> class is gone from error.log).

## #109 — DEBUG harness noise (debug_demand.txt + timetest_quarterly_tick.txt)
- DIAGNOSIS (imp19c-logs, newest boot): the task premise ("confirm -debug_mode-only and strip/gate") is WRONG.
  Both files are LIVE production infrastructure, NOT debug-gated: debug_demand.1/.2 fire from oa_wealth_changes
  (quarterly wealth on_action) and drive real food/luxury demand; timetest_quarterly_tick.1-30 is the ENTIRE
  quarterly economic tick (send-to-reserves, produce goods, pay wages, collect taxes, currency power, mil
  supplies, diplomacy power). They must NOT be stripped. The log noise is two real defects each:
  1. title/desc = "TEST" on every hidden event -> "Unrecognized loc key TEST" per fire (hidden events never
     display title/desc, so this is pure noise). debug_demand: 3 events; timetest: 31.
  2. debug_demand.1: `set_variable = first_time_food_demand_updated` was INSIDE the inner `limit = {}` (a
     trigger block) -> "Unknown trigger type: set_global_variable near line 36" every boot AND the first-time
     flag never actually got set (swallowed as a bad trigger). Mirrors the CORRECT placement in .2. REAL bug.
  3. timetest: the engine warns the file "should be in utf8-bom encoding" — it was plain ASCII (no BOM).
- FIX:
  - debug_demand.txt: dropped title/desc/picture from the 3 hidden events (-> hidden-only); moved .1's
    set_global_variable OUT of the limit{} to fix the parse error + restore the flag. Preserved original
    BOM+CRLF encoding (no EOL churn after restoring).
  - timetest_quarterly_tick.txt: dropped title/desc/picture from all 31 hidden events; ADDED the utf8 BOM the
    engine asked for. LF endings preserved; only content change is the TEST strips + BOM.
- SEPARATE BUG FOUND + FILED (#124, NOT folded here — it's a behavior change in upstream trade code, out of this
  loc-noise task's scope): timetest_quarterly_tick.22 is DEFINED TWICE (lines 442 + 462); the second overrides
  the first, so DIPLOMACY_get_power_in_play_TZ (first .22) never runs. Needs a renumber, reviewed on its own.
- STATUS: DONE (loc-noise + parse-error + BOM). #124 left for its own diagnosis->review pass.

## #124 — timetest_quarterly_tick.22 defined twice (duplicate event id)
- DIAGNOSIS: two `timetest_quarterly_tick.22` blocks (get_power_in_play_TZ + get_top_players_tradezone);
  the engine keeps only the LAST definition, so the first .22 (DIPLOMACY_get_power_in_play_TZ) was shadowed.
  BUT: traced dispatch — NOTHING fires timetest_quarterly_tick.* (no trigger_event / on_action anywhere; the
  se_DIPLOMACY comments call it "the DEBUG timetest harness"; the live quarterly tick runs via oa_wealth_changes
  + debug_demand). So the whole harness is DEAD and the shadowing had ZERO runtime impact — it's a parse-time
  duplicate-id defect only. Severity accordingly low (downgraded from the filed wording).
- FIX: renamed the SECOND .22 -> .31 (a free id). Did NOT renumber .23+ (avoids an 8-event cascade; since
  dispatch is by-id-nowhere, ordering is irrelevant). All ids now unique; braces 168/168; BOM-free.
- STATUS: DONE.

## #108 (part 1/2) — DEBT_events / INCOME_mitigate_deficit bimetallic unset-var flood
- DIAGNOSIS (full call-chain from newest error.log): 121x silver_needed_for_deficit + 121x
  gold_reserve_value_greater_than_silver + paired "unset scope 'local_var'" / "invalid comparison" — chain =
  DEBT_events.1 -> INCOME_mitigate_deficit -> INCOME_sell_largest_reserve line 54 -> INCOME_sell_reserves line 8.
  ROOT CAUSE (distinct from the earlier #19/#87 set-site guards, which were correct but insufficient): the four
  callers set `local_var:<metal>_needed_for_deficit` then passed `amount = local_var:<that>` into the
  INCOME_sell_reserves MACRO. A local_var does NOT cross into a called effect's scope, so the macro's
  `value = $amount$` (which expands to `value = local_var:<metal>_needed_for_deficit`) read an UNSET local in
  its own scope -> the flood. (DEBT_events.txt is 24 lines on disk; the log's "line 113" is the call-site chain,
  not the file.)
- FIX: at all 4 call sites (INCOME_mitigate_deficit gold/silver branches + INCOME_sell_largest_reserve
  gold/silver branches) changed set_local_variable -> set_variable (COUNTRY var — those DO propagate into called
  effects, proven throughout the mod), passed `amount = var:<metal>_needed_for_deficit`, and remove_variable
  after the call to avoid leaking the scratch var. 0 stale local_var:*_needed_for_deficit reads remain; braces
  210/210; BOM intact.
- REMAINING (part 2/2, NOT done here): the oa_wealth_changes floods (617x 'trade_center' unset @ :485, EDU_t2_
  educated_governorship, etc.) are a SEPARATE trade-tick read-before-set root cause in the hot quarterly path —
  left for its own consolidated diagnosis with #107 (they share the food-stockpile / trade-var lifecycle). #108
  the DEBT/INCOME half is the cleanly-rooted one and is fixed; the task stays in_progress for part 2.
- CODE REVIEW cr108a: dispatched (pending). Self-review: cross-macro local→country-var is the documented Jomini
  behaviour; the remove_variable cleanup keeps it tidy; no semantics change beyond the var scope.
- STATUS: part 1 DONE + committed; part 2 (oa_wealth_changes/trade_center) pending — task remains in_progress.

## #108 (part 2) — oa_wealth_changes trade_center unset flood (617x, the biggest single site)
- DIAGNOSIS: chain = oa_wealth_changes:485 (GT_split_do_global_trade_split type=5) -> GT_split_do_shipping_costs
  -> GT_split_get_governorship_shipping_income lines 20/24. Those read `var:trade_center.*` on the governorship.
  A governorship never assigned to a tradezone has no `trade_center` var (set only in TRADE_update_governorship
  _TZs, se_TRADE.txt:1886) -> 617x "Failed to fetch variable 'trade_center' / unset scope 'var'"/boot.
- FIX: wrapped the two trade_center-dependent change_variables in `if = { has_variable = trade_center  var:trade
  _center.SHIPPING_total_in_TZ > 0 }`; else set queued_trade_income_due_shipping = 0. A TZ-less governorship has
  no shipping income so 0 is correct; the >0 also dodges a Div/0 when TZ total shipping is 0. braces 1627/1627.
- STILL OPEN (part 3, LOUDLY NOT DONE — these are 3 more DISTINCT roots in the same file, each needs its own trace;
  NOT folding blind): (a) :341 GT_save_final_tradegood_vars unset 'var' (154x); (b) :101 EDU_set_t2_national_
  bonus_from_universities Div/0 (271x — a divide by an unset/0 university count); (c) :467 GT_split_cache_DEMAND
  _reserve_accumulation_basis_svalues 'silver_accumulation_rate' unset (207x — likely the same #106-class
  seed-defaults fix, silver_accumulation_rate not set for non-CHI). #108 stays IN_PROGRESS for these.
- CODE REVIEW cr108b: dispatched (pending). Self-review: has_variable guard is the proven read-before-set idiom
  (same as #106); the else 0-set is behaviour-preserving (init is already 0); no Sobisonator-logic change beyond
  the guard.
- STATUS: parts 1+2 committed; part 3 (3 sub-roots) explicitly OPEN, task in_progress.

## #92 FOLLOWUP + #125 — loc-scope-syntax fix (cr92 finding)
- cr92 (review of the shipped #92) found a MEDIUM: qing_revenue.6.desc used [scope:qing_gran_built_province
  .GetName]. Saved scopes are read BARE in loc ([x.GetName]); the scope: prefix renders literal ERROR:[scope:...]
  in-game, defeating the province-naming point of the event. Fixed -> [qing_gran_built_province.GetName].
- cr92 also flagged the identical PRE-EXISTING bug at qing_march_relief.1.desc (qing_march_relief_l_english.yml
  :10). Filed as #125 and fixed in the same commit (trivial one-line, same pattern). No other [scope: in loc now.
- All other cr92 findings CLEAN (scope propagation, guard/no-double-charge, 255 cost, is_triggered_only, BOM,
  log-string, no AI spam) — verdict was ship-after-the-one-loc-edit. Both edits done.
- Also cr74/cr90/cr94 returned CLEAN (earlier commits confirmed post-hoc).

## #107 (part 1) — food-stockpile unset flood (~600/boot)
- DIAGNOSIS: DEMAND_get_stockpile_percentages_all_tradegoods (se_DEMAND.txt:338+) reads var:<food>_stockpile
  unconditionally for all 6 food goods (grain/livestock/vegetables/temperate_fruit/processed_foods/fish); a
  governorship only gets a stockpile set once it produces/consumes that good -> ~600 unset-var errors/boot.
- FIX (#106-class seed-defaults): seed all 6 to 0 (per-var has_variable guard so it NEVER zeroes an accumulated
  stockpile) at the TOP of TRADE_reset_quarterly_governorship_values (runs at setup + quarterly, per-governorship).
- STILL OPEN (part 2, NOT done): #107 also bundles 101x Div/0 (oa_wealth_changes:450/416 — separate root, needs
  its own trace) + the 242 bimetallic reads (ALREADY fixed by #108 part 1). Div/0 sub-root left for a boot-verify.
- STATUS: food-stockpile half committed; Div/0 half open — task in_progress.

## #107 (part 2, COMPLETES #107) — GT_set_tradegood_price Div/0 (85x/boot)
- DIAGNOSIS: innermost frame GT_set_tradegood_price relative-line-3 = the divide at se_GLOBALTRADE_split.txt:5952,
  `divide = global_var:$tradezone$_stockpile_$tradegood$`, guarded only by `> 0`. At game SETUP (day 0,
  oa_economy_setup:2490, before stockpiles are seeded) the stockpile global is UNSET, and a bare `> 0` on an
  unset global inside a value{} svalue block does not reliably skip the divide -> Div/0 (85x/boot).
- FIX: add `has_global_variable = $tradezone$_stockpile_$tradegood$` to the limit (read-before-set-safe). Unset
  -> skip divide, price = raw order size (correct default before any stockpile exists). 1-line, braces 1628/1628.
- #107 NOW COMPLETE: food-stockpile seed (19dc745d4) + this Div/0 guard. The 242 bimetallic reads bundled in the
  task were fixed by #108 part 1. All three sub-roots of #107 closed.

## #108 — final accounting of the three named files
- oa_wealth_changes.txt (1962 lines of errors): the TWO real high-count roots FIXED — bimetallic cross-macro
  local_var (part 1, b58a025b3) + trade_center unset 617x (part 2, c4e5f538b). Residual: EDU Div/0 16x
  (EDU_update_effect -> EDU_set_t2_national_bonus...; a divide whose exact frame is ambiguous in upstream EDU
  svalues) + tradegood-var reads — LOW count, upstream EDU/trade svalues, NOT blind-editing without a boot to
  confirm the divide site. Stated plainly, not buried.
- DEBT_events.txt (732): FIXED — its whole flood was INCOME_mitigate_deficit's bimetallic local_var bug (part 1).
- WAR_scripted_guis.txt (804): NOT an error — it is a NON-FATAL engine WARNING ("testing for exact value (=),
  this will work, but is probably not intended") from PEACE_get_warscore, an UPSTREAM Sobisonator effect
  explicitly marked "# DEFUNCT - hopefully. war_score_value should replace this now". It's a ~200-branch
  war_score = {value=-100..+100} exact-match ladder; the warning is cosmetic (the code works). Rewriting a
  defunct 200-branch upstream chain on a non-fatal warning is exactly the Sobisonator-caution trap; NOT touched.
- NET: the two genuine high-volume ERROR floods in #108 are eliminated; the 804 "WAR" lines are warnings in
  defunct upstream code (cosmetic); the EDU Div/0 residual (16x) is boot-gated. #108 real-error work is done.

## #91 — contest/skill-check events fire a silent hidden_effect; add outcome notification (caravan family)
- DIAGNOSIS: qing_caravan.4 (A Dispute at Kashgar) resolves the super-vs-aqsaqal skill check inside a hidden_effect
  — the player picks Negotiate/Coerce/Collude and sees NOTHING (no win/lose feedback). Same shape in 3 other
  files (integration capstone, march, subject_integration) — the task says audit ALL.
- FIX (caravan family, this commit): each of the 6 win/lose branches now sets a qing_caravan_outcome flag
  (negotiate_win/lose, coerce_win/lose, collude_win/lose); each option fires a new qing_caravan.5 notification
  (days=2) that shows the matching result via 6 triggered_desc keyed on the flag, then clears the flag on ack.
  New event qing_caravan.5 + 8 loc keys (title/option/6 descs). Braces 187/187; loc quotes 2/line; BOM intact.
- REMAINING (the other 3 contest families — march / integration-capstone / subject_integration): SAME pattern to
  apply. NOT skipping — doing them next in this run so #91's "audit ALL" clause is met whole.
- STATUS: caravan family done + committed; extending to the other 3 families next (task stays in_progress until all 4).

## #91 — march family + full audit of ALL 4 contest families (COMPLETES #91)
- march family: qing_march.2.a "let the GG handle it" resolved its skill-roll in a silent hidden_effect. Fixed:
  clean/chaotic branches set qing_march_unrest_outcome; option fires new qing_march.6 (2 triggered_desc) + clears
  the flag on ack. New event + 4 loc keys. Braces 122/122; loc quotes 2/line; BOM-free events / BOM loc.
- AUDIT of the other 2 families (the "audit ALL" clause): qing_subject_integration.txt AND
  qing_integration_capstone_events.txt ALREADY fire outcome events after their skill-checks (both do
  `trigger_event = { id = qing_integ.46 }` post-roll; capstone has 14 trigger_events for its 15 hidden/random
  blocks; qing_integ.46 exists as the outcome event). So they were NOT silent — no fix needed, verified in source.
- #91 COMPLETE: 4 contest families audited; the 2 silent ones (caravan, march) fixed; the 2 already-notifying ones
  (subject-integration, capstone) verified correct. Nothing deferred.
