# SCRATCH — #23/deflation working notes and disproven hypotheses

Per user instruction (2026-08-12): AUDIT_CURRENCY_23.md should preserve the CONFIRMED cause once found,
not every wrong guess along the way. This file is where in-progress hypotheses, ruled-out leads, and
retracted reconstructions get recorded WHILE digging — promote to the audit doc only what survives
adversarial review. Once a cause is confirmed, the audit doc gets cleaned to keep only the real chain of
reasoning that led there; this file keeps the full messy history for reference.

## Disproven / retracted so far (moved out of the live audit doc)

- **#50-revert hypothesis** (mine): `75f25152a` reverting penetration cap-lift. REFUTED — timeline (0.4545
  predates this symptom) + magnitude (pen only swings ~0.07-0.20, far too small).
- **`wvuraw` retroactive reconstruction "strengthens #112"** claim: REFUTED by adversarial review.
  `need` has 3 terms, 2 divide by wvuraw-derived quantities not 1; `need`'s 16.0 display cap censors the
  true swing, making any "residual too big for divisor" argument circular; `ess`/`wvuscaled` were already
  logged and unread, showing 4.35x/2.48x swings that were never checked before reaching for the unmeasured
  numerator.
- **MONSTD_reconcile / #75 backing-flip**: ruled out by log — `MONSTD_switch_backing`'s own log line has
  zero hits despite `MONSTD_reconcile` firing every month (61,400 times). Mechanism real, inert this boot.
- **#74 (sell-degrees fallback grant), #102 (treasury cap raise), #106 (shipping_<zone> seed) + its
  revert**: all ruled out by direct diff read — none touch `need`'s formula terms.

- **constant-ess, trout-band-correlated "need swing CONFIRMED" claim** (2026-08-12, was I.14 in the audit):
  REFUTED by adversarial review. The underlying observation (q5 POST ess=64/need=16.0-CAPPED/trout
  100-500k -> q6 PRE ess=64/need=1.76-exact/trout 0-10k) is real and not a parsing artifact — re-verified
  independently by the reviewer. But of the full 14 constant-ess pairs (not 13; a within-quarter idx26->27
  pair was missed in the first count), only 2 cleanly support "trout moves need": 5 are CAP-CAP (need
  capped both sides = zero evidence, wrongly counted as support) and 6 have trout's band completely FLAT
  while need still swings hard (which, by the same control logic, EXONERATES trout in those 6). Two
  confounds were also found: (a) `country_population` (the OTHER factor in `ess*population/4000`, never
  logged anywhere in this investigation) could explain a swing at constant `ess` just as well; (b)
  `CURRENCY_wealth_generated_country_as_currency_value` shares `trout`'s exact divisor
  (`CURRENCY_wealth_value_1_unit`), re-importing the exact shared-divisor confound that refuted the
  `wvuraw` reconstruction above. Genuinely useful output kept: `need`'s exact-tick scale was hitting its
  8000-tick cap on 17/29 quarters (rescaled 500->50); `poptick`/`wealthgen` exact logging added to close
  both confounds for the next boot (`se_ECON_LOG.txt`, `tools/curx_analyze.py`).

- **back-solved-need "trout is a confirmed contributor" claim** (2026-08-12, was I.16 in the audit):
  the ARITHMETIC (`need_true = circ*0.004/ratio`, recovering need past its display cap) was verified sound
  by adversarial review and KEPT — see AUDIT §I.17. The CAUSAL claim about trout was REFUTED, for two
  reasons: (a) `need` subtracts trout, and trout arrives already negative, so "trout band grows -> need
  grows" is close to a formula-sign tautology, not new evidence, given only 4 trout-band-change events to
  check it against; (b) EVERY constant-ess pair is a POST(N)->PRE(N+1) transition, and `ECON_LOG_curx_
  dump_post` fires BEFORE `TRADE_national_expenditure`'s own cache-refresh in the same on_action block
  (Finding B, §I.14) — so every pair straddles exactly one guaranteed cache-refresh landing BY
  CONSTRUCTION, not as 14 independent natural events. The "control" was measuring the mechanism Finding B
  already named, not testing an independent hypothesis against it.

## Live leads not yet promoted to the audit doc

- **`ratio`'s upstream inputs vs `wealth_owed`** (2026-08-14): the fresh boot shows `ratio`/`gbip`
  stepping up permanently around quarter-index 11 and never reverting (promoted to Finding 6 as a
  described-but-untraced observation). Whether this step is caused by Finding 5's thin-stock
  `wealth_owed` inflation (as opposed to a genuinely growing trade economy outpacing reserves) was
  NOT checked this pass — `ratio`'s formula (`wvuraw`/agsilver-derived, see `CURRENCY_svalues.txt`)
  needs to be read against the same quarters' `wealth_owed`/tariff income to settle this. Do not
  re-derive the stockpile-toggle evidence below when picking this up — it's already confirmed.

## Session 2026-08-14 (logs.zip Aug-14 02:10) — promoted to Finding 6, and what got ruled out

The fresh boot Finding 5 asked for finally landed (`natexp`/`wvuraw`/`poptick`/`wealthgen` all
logged). Used it for TWO separate investigations — Finding 5's stockpile question, and a NEW
user-reported symptom ("treasury jumps ~2-3x the displayed quarterly income every other quarter")
that is related (same income/treasury machinery) but is not the periodic #23 oscillation this
whole file otherwise tracks.

**Ruled out for the treasury-spike symptom** (full reasoning now in Finding 6, not repeated here):
double-firing of `INCOME_update_treasury_country` (wall-clock PRE/POST markers are evenly spaced,
no back-to-back pairs); `INCOME_mitigate_deficit` reserve-selling (zero occurrences in this boot,
CHI never went into deficit); "Tariffs and shipping" vs "Tariffs" being a double-count (it's a
legitimate national-sum-vs-one-governorship scope difference — though the "shipping" HALF of that
line is separately confirmed dead code, `this_income_from_shipping_the_state` is never set anywhere).

**Advanced, not closed:** Finding 5's thin/zero-stockpile mechanism. 16/22 zones toggle stock band
across the 29 quarters; 9+ hit exact stock=0. This is common, not rare — supports the mechanism
being LIVE. But `natexp` (TRADE_national_expenditure, confirmed genuinely set every quarter, not an
unread var) stayed near-zero/negative for all 29 quarters — an argument AGAINST this being the
dominant driver on the expenditure side specifically. Income-side channels (tariffs/income-tax,
which also read wealth_owed) were not separately measured this pass — that's the natural next step,
not natexp again (natexp is expenditure-only by construction, see se_ECON_LOG.txt:435-456).

**New, unresolved, low-priority:** `wealthgen`'s exact-tick probe has no matching coarse-band CURX
call anywhere (only natexp got one) and reads exact 0 for all 29 quarters. Could be a genuinely
near-zero wealth-generation figure, or an unwired probe. Not investigated further — flagged only.

## Session 2026-08-14 continued — treasury ~9000/quarter spike, hypotheses tried and refuted

User framing (authoritative, do not re-litigate): the bug is "treasury income is fine but treasury
VALUE is increasing by orders of magnitude more than what treasury income displays" — a DIFFERENT
bug from #30/#112/#115 ("treasury income is orders of magnitude too high", the displayed number
itself was wrong). The error surface per the user is code committed within 24h of the boot in
question (Aug 13 02:00 - Aug 14 02:10).

- **REFUTED — `ba8b38672` (fix #30, wealth_owed quantity-rationing).** User confirmed directly:
  related but not the same bug (#30 = displayed income wrong; current bug = displayed income right,
  treasury delta wrong). Do not re-chase this commit for the current bug.
- **REFUTED — Maritime Customs (`QING_customs_pulse` → `CURRENCY_grant_country_wealth`,
  surfaced via `0c04c6620`).** Arithmetic looked like an exact match (thousands-input 0-20 ×
  wvuscaled×1000 [0.32-0.57] = up to ~11,400/quarter, invisible to any display) — but
  `QING_customs_pulse` only fires once `qing_customs_established` is set
  (`se_QING_GOVERNANCE.txt:324-325`), gated to the 1854+ Shanghai Customs founding (Robert Hart,
  `d855ac9a1`). Confirmed empirically: zero occurrences of its own LOG lines anywhere in the actual
  boot's debug.log — never fired in this Dec-1763-to-Jun-1766 boot. Lesson: checked the arithmetic
  before checking whether the mechanic was even ACTIVE in the relevant period — should invert that
  order next time (activity-gate first, magnitude second).
- **REFUTED — Cottage Industry buildings / `vegetables` price (commit `b7b223729`, considered for
  the SEPARATE inflation/essentials-price question, not the treasury spike).** User confirmed
  directly: zero Cottage Industry buildings were constructed in the boot in question. No buildings
  built → no supply-side price effect from this source, regardless of the mechanism's plausibility
  on paper.
- **REFUTED — `qing_revenue.5` "Fullest Coffers" milestone event (`61a156e19`/`27e3ccdfb`).**
  Double-refuted: (1) its own effect body (`events/imp19c_mod_events/qing_revenue_events.txt:408+`)
  has no `add_treasury`/gold/wealth grant at all — flavor/milestone only; (2) it never fired in this
  boot anyway — zero occurrences of its LOG line, consistent with the boot's own reported silver
  reserve (~52863 per screenshot) sitting far below the 81820 peak threshold. The boot's internal
  timestamp (~01:28) postdates #61's 19:23-Aug-13 landing, so this is a real post-fix boot, not a
  stale pre-fix one — the event correctly hasn't fired because the reserve hasn't reached its peak,
  not because of a residual gating bug.

## Remaining un-eliminated candidates for the ~9000 spike (none yet confirmed)
Tribute (`se_SUBJECT_QING.txt:1173-1224`, `QING_subject_collect_tribute` — has an uncapped branch
that can charge a subject its ENTIRE treasury as tribute, paid directly to CHI's treasury; was mid-
trace when redirected, not yet ruled in or out) and the thin-stockpile `wealth_owed` mechanism
(AUDIT_CURRENCY_23 Finding 6, confirmed common but `natexp` stayed flat, arguing against it
dominating on the expenditure side — the INCOME side via tariffs/income-tax was never separately
measured). Both still open; neither confirmed.
