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
