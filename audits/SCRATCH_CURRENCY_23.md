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

(none currently — the fresh-boot measurement with `natexp`/`wvuraw`/`poptick`/`wealthgen` all logged
simultaneously, per §I.12/§I.15, is the next required step before any new hypothesis can be tested without
these same confounds recurring. The `need_true = circ*0.004/ratio` back-solve, §I.16/§I.17, is a proven,
reusable technique to bring to that boot's analysis — it does not itself need to be re-derived or
re-reviewed again.)
