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
