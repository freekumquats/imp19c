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
