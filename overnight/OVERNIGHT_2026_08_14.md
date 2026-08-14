# Overnight run — 2026-08-14

## ASSUMPTIONS & GUESSES (best-guess values made without boot data — scan this section first)

- **`se_QING_SALT.txt` salt-income cap = 150.** Set just above the adversarial review's own
  calculated realistic ceiling (~46-138, from CHI's 8 salt provinces vs Canton's 42 tea+silk+
  porcelain provinces at the same per-province rate). No boot data confirms the exact right
  number — `LOG_line = "salt: national production base exceeded the 150 cap, clamped for"`
  fires if the cap is ever actually hit, which the next boot's debug.log will show.
- **`se_QING_DECLINE.txt` granary build cooldown = 1095 days (~3 years).** User asked for "once
  every few years"; 3 years is a plain reading of that, not derived from any in-game rate. No
  diagnostic log added specifically for this (the existing `LOG_line` on a successful build
  already shows the cadence on the next boot's timestamps).
- **Outliner building-icon fix is an unverified BOOT SPIKE, not a confirmed fix** — see task #73
  below. `OutlinerItem.GetBuilding` has no proven precedent anywhere (this repo, vanilla, or the
  Terra-Indomita oracle). It cannot regress below the current (already-broken) baseline if wrong.

## Task #67 — Fix amban/garrison subject-type check drift (integrating_governorship gap)
**What:** `QING_amban_warrants_resident_trigger` and `QING_fgar_scan` each kept their own
subject_type OR-set for amban/garrison eligibility; both were missing `integrating_governorship`
(the transient type a subject is rebound to during `SUBJ_QING_authorize_integration`), which is
why Urga silently lost its Replace-amban button and "Under imperial garrison" line mid-integration
despite remaining a direct CHI subject throughout.
**Decision:** consolidated both into one shared `QING_amban_garrison_eligible_type_trigger`
(`qing_dynasty_triggers.txt`) so the two systems can't drift apart again. Deliberately left the
two SEPARATE "integration-ladder-progression" gates (a narrower, intentionally different check)
unchanged — confirmed via review these are a different semantic, not a missed inconsistency.
**Review:** code-review CLEAN, no findings.
**Commit:** `0195b16b5`. **Status: DONE.**

## Task #69/#80/#81 — Inflation diagnosis: reserve-ratio-rail theory REFUTED, real cause open
**What:** first diagnosis (reserve-ratio multiplier railing at its cap as reserves accumulate) was
adversarially reviewed and REFUTED against the boot's own exact-tick data — the divisor
(`wvuscaled`) barely moves at the pivot quarter where `ess`/`ratio`/`infl` all jump. Real driver:
an unexplained ~51% collapse in the essentials-price SUM itself, in one quarterly tick. Only 2 of
its 12 inputs (grain, fish) had ever been probe-covered.
**Decision:** corrected `audits/AUDIT_CURRENCY_23.md` (added Finding 7, explicitly retracting the
refuted theory) rather than leaving a wrong diagnosis on record. Extended
`tools/gen_econ_tzprobe.py`'s GOODS list with the 9 remaining trackable essentials goods
(livestock, vegetables, temperate_fruit, processed_foods, clothing, furniture, pharmaceuticals,
luxury_clothing, luxury_furniture — `alcohol` excluded, confirmed dead/unloaded trade-good) and
regenerated `se_ECON_LOG_TZPROBE.txt`. Read-only diagnostic, zero gameplay effect.
**Review:** code-review CLEAN (one LOW doc count nit, fixed).
**Commit:** `754ffddf7`. **Status: root cause still OPEN (task #81) — genuinely BLOCKED-ON-DATA,
needs the next boot's new BAND rows to name the culprit good. Not a deferral: the probe that will
answer it is already shipped.**

## Task #79 — Treasury income enormously understates real treasury growth (hidden Qing revenue)
**What:** two-level bug, per the user's own framing: (1) magnitude — treasury jumps ~9000/quarter
some quarters vs a displayed few hundred to low thousands; (2) visibility — salt gabelle, Canton
customs, and caravan trade all pay `add_treasury` directly every quarter, entirely absent from the
topbar Change arrow and the nation-treasury tooltip (confirmed by reading both UI sources).
**Investigated as the magnitude suspect: salt's uncapped production base** (`se_QING_SALT.txt`
had no cap unlike its Canton/Caravan siblings, both of which explicitly cap their real-goods base
to prevent a "runaway export boom"). Adversarial review with real province-count arithmetic
REFUTED this as the ~9000 source (CHI has only 8 salt provinces vs Canton's 42 tea+silk+porcelain
provinces; salt's realistic ceiling lands at ~46-138, same order as Canton's own capped maximum
~106 — nowhere near 9000). Fixed the cap anyway as defensive hygiene/consistency with its
siblings (NOT sold as the spike fix — logged honestly as such).
**Fixed the visibility half in full:** added `INCOME_national_total_from_qing_revenue` (sums the
three streams' cached `_last` vars) and a NEW, separate `INCOME_national_total_quarterly_display`
(payment total + Qing revenue) read ONLY by the topbar's Plus/Minus/Change bindings and the
Ministry of Revenue's Total line — **first draft folded the Qing revenue directly into
`INCOME_national_total_quarterly`, which is also what `add_treasury` reads, and was caught by
adversarial review as a CRITICAL double-credit bug before commit.** Corrected to the
separate-display-value shape; re-reviewed CLEAN.
**Reviews:** salt-cap review CLEAN; income-wiring review CRITICAL (double-credit) → corrected →
re-review CLEAN (2 LOW comment nits, fixed).
**Commits:** `fda378e02` (salt cap), `f68d9e289` (income visibility).
**Status: visibility half DONE. Magnitude half (the actual ~9000 source) still OPEN — salt/Canton/
caravan all ruled out by arithmetic; remaining candidates not yet checked: tribute payments, the
silver-reserve-drift's own +250-350/quarter additions, the thin-stockpile wealth_owed trade
mechanism from AUDIT_CURRENCY_23 Finding 5/6. Genuinely BLOCKED-ON-DATA for the exact mechanism,
not a deferral — the UI half (which was fully fixable now) is shipped.**

## Task #71 — Fix Canton Silver Inflow unit display (lbs -> thousand-taels)
**What:** user reported this line might be showing lbs instead of thousand-taels.
**Diagnosis:** verified via source (`se_QING_CANTON.txt:223-237`, explicit ×10 萬兩→千兩
conversion, dated 2026-08-06, predates this session) and loc (`QING_REVENUE_MINISTRY_CANTON_
SILVER_LABEL`/`_TT` both explicitly say "千兩 (thousand taels)") — already correct, no lb/pounds
reference anywhere in this panel. **No code change made.**
**Status: DONE — verified already-correct, closed rather than left open on a stale report.**

## Task #74 — Slow Ever-Normal Granary auto-build cadence (every quarter -> every few years)
**What:** the good-year build branch of `QING_DECLINE_granary_concrete` matched and built a new
granary on every ~90-day governance pulse until the Yellow River basin backlog was exhausted,
reported as granaries auto-building too fast.
**Decision:** added a `qing_granary_build_cd` cooldown (1095 days, best-guess) gating ONLY the
build sub-block. **First draft accidentally put the cooldown in the shared outer `limit`, which
also silently gated the good-year RESTOCK block below it — caught by review as a MEDIUM bug** (a
famine-drained granary would stay wrongly flagged empty for up to 3 years after reserves actually
recovered). Corrected: restock is now its own sibling `if`, keyed purely on the stock band, no
cooldown/treasury/backlog dependency.
**Review:** first pass MEDIUM (restock over-gated) → corrected → not re-reviewed by a fresh agent
(mechanical restructure, verified the fix directly against the review's own suggested shape).
**Commit:** `6925d32dd`. **Status: DONE.**

## Task #73 — Fix Outliner icon fix regression (still showing placeholders)
**What:** a prior fix (`c1f84da9a`/`3afdea7bf`, #34) added `visible = yes` to reveal the
Construction categories' `action_icon` override, but a fresh boot screenshot (20260814014339_1.jpg)
confirms every queued item (9× Yamen, 2× Administration District) still shows the IDENTICAL
generic icon — the #34 fix did not actually resolve the symptom.
**Diagnosis:** the `action_icon` texture expression (`OutlinerItem.GetIcon`) is proven to resolve
for CHARACTER outliner items (the pattern it was copied from) but has NO proven precedent for
resolving a BUILDING's icon on a construction-queue item. Every confirmed-working building-icon
call site in this engine (`mapiconlayer.gui:1038`, `province_window.gui:4520`, and the
Terra-Indomita oracle's own `province_window.gui:324`/`gui_base.gui:6564`) instead uses
`GetBuildingIcon(<item>.GetBuilding)` — a different two-step accessor. No repo, vanilla, or oracle
precedent exists either way for `OutlinerItem` exposing `.GetBuilding`.
**Decision (Rule 1 hard-block #1 — unverifiable-without-a-boot render):** shipped as a labeled
BOOT SPIKE — changed both Construction categories' `action_icon` texture to
`GetBuildingIcon( OutlinerItem.GetBuilding )`. Cannot regress below the current (already-broken)
baseline: if the promote chain doesn't exist, it fails the same way the current code already
fails (icon blank, `_default.dds` still shows underneath).
**Status: SPIKE SHIPPED, NOT confirmed. Left in_progress. Needs a boot + fresh outliner
screenshot to confirm/refute.**

## Task #82 — Add COMPREHENSIVE LOGS across the entire economic system (log everything)
**What:** standing gap named directly by the user — every diagnostic probe this project has ever
built was scoped narrowly and reactively to one question at a time, not built as durable
exhaustive infrastructure, and "that wasn't logged" kept surfacing mid-investigation. User directive
(repeated, explicit): log everything, log volume is not a constraint.
**Status: IN PROGRESS, not yet complete.** First slice shipped as part of the inflation probe
extension (task #81/Finding 7, commit `754ffddf7`). Full scope (country_unit_price for every good,
not just zone-level prices; wealth_owed per category; exact-tick amounts for every hidden revenue
stream) still open — continuing this run.

## Task #79 continued — treasury ~9000/quarter spike hunt, sweeping the 24h commit surface
**Correction from the user mid-investigation:** this is NOT the same bug as #30/#112/#115
("treasury income orders of magnitude too high" — the DISPLAYED figure was wrong). The current bug
is "treasury income displayed is fine, but treasury VALUE increases by orders of magnitude more
than what income displays" — a hidden-payment bug, not a wrong-display bug. Per the user, the error
surface is code committed within 24h of the boot (Aug 13 02:00 - Aug 14 02:10).
**Swept and REFUTED, in order:**
- `ba8b38672` (fix #30) — user-confirmed different bug class, not this one.
- Maritime Customs (`QING_customs_pulse`/`CURRENCY_grant_country_wealth`, surfaced via `0c04c6620`)
  — arithmetic looked like an exact match (~1000x display-vs-real gap, up to ~11,400/quarter) but
  the mechanic is gated to the 1854+ Shanghai Customs founding and never fires in this 1763-1766
  boot — confirmed empirically, zero LOG-line occurrences. **Process lesson: checked the magnitude
  arithmetic before checking whether the mechanic was even ACTIVE — should always gate-check first.**
- Cottage Industry buildings / vegetables price (`b7b223729`) — user confirmed zero such buildings
  were actually constructed in the boot; considered for the separate inflation question, not this one.
- `qing_revenue.5` "Fullest Coffers" milestone event (`61a156e19`/`27e3ccdfb`) — double-refuted: no
  treasury effect in its own code, AND never fired in this boot (reserve well below its peak trigger).
**Still open, not yet ruled in or out:** tribute (`QING_subject_collect_tribute`,
`se_SUBJECT_QING.txt:1173-1224` — has an uncapped branch charging a subject its entire treasury,
paid directly to CHI) and the thin-stockpile `wealth_owed` income-side channel (AUDIT_CURRENCY_23
Finding 6). **Status: BLOCKED, genuinely unresolved at this point in the run — not a deferral, the
candidate list is real and traceable, just not yet finished.**
**Process note logged per user correction:** ruled-out hypotheses belong in
`audits/SCRATCH_CURRENCY_23.md`, never in `AUDIT_CURRENCY_23.md` (verified conclusions only) —
corrected mid-run (commit `5a9e96b88`) after initially polluting the audit doc.

## Related files
- `audits/AUDIT_CURRENCY_23.md` — Finding 6 (treasury-spike hypotheses ruled out/advanced),
  Finding 7 (inflation reserve-ratio theory refuted, corrected direction).
- `audits/SCRATCH_CURRENCY_23.md` — working notes, not committed (local reference only).
