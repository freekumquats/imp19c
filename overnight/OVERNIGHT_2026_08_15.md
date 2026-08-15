# Overnight run — 2026-08-15

## ASSUMPTIONS & GUESSES
- None yet this session (this entry covers a diagnostic-instrumentation fix only, no new tuning
  constants introduced).

## Task #79/#102 continued — fixed the #79 diagnostic probe's own scope bug
Per direct user instruction ("investigate and fix 79 first, that is highest priority. follow the
standard diagnosis->review->design->review process"), re-opened the tariffs-magnitude diagnosis
after the prior gunpowder-thin-stock hypothesis was refuted (dollar contribution of all thin-stock
capped goods combined: ~$16.95 across the whole boot — trivial against the observed ~2000-2500/
quarter plateau) and the #102/#103 (cottage industry) connection was also refuted (military supplies
topbar formula never references gunpowder at all; #103 has its own pre-existing, correct diagnosis).

**Diagnosis (adversarially reviewed CLEAN):** the #79-era diagnostic probe itself,
`ECON_LOG_curx_tariffs_expenses` (`se_ECON_LOG.txt`, shipped in commit `3db638045`), has a scope bug
— it reads `this_expenses_from_resource_extraction/manufacturing_<strata>` at COUNTRY scope, but
these vars are GOVERNORSHIP-scoped (set only inside `every_governorships`,
`GT_split_calculate_actual_share_of_expenses_category`, `se_GLOBALTRADE_split.txt:4358-4365`,
`# Scope: governorship` at :4369). `has_variable` at country scope on a governorship var is
structurally always false, so this probe has emitted all-zero data since its own first boot —
confirmed against the real Aug-15 boot log: the sibling `expense_taxrate_tariffs` metric (a genuine
country var) read a real 0.075 in the same probe run while all 12 expense metrics read ZERO every
time. Also found the probe's stratum set was wrong: it covered upper/middle/lower/proletariat/
indentured/slaves (6), but `INCOME_governorship_tariffs_total_positive`
(`INCOME_svalues.txt:748-754`) sums exactly upper_strata/middle_strata/lower_strata/proletariat/
tribesmen (5) — missing tribesmen entirely, two wrong extras.

This means the ORIGINAL #79 diagnosis's claim of "concrete instrumentation, confirmed zero prior
logging, now instrumented" was never actually validated with real data — every prior boot's
tariffs-magnitude numbers from this probe were silently zero.

**Fix (adversarially reviewed CLEAN, no findings):** rewrote `ECON_LOG_curx_tariffs_expenses` to
wrap the reads in `every_governorships` (proven country-scope iterator), `save_scope_as` each
governorship's identity, and accumulate into 10 country-scope staging vars (5 strata x 2 categories)
via the proven `owner = { change_variable = { ... add = scope:<saved>.var:<field> } }` idiom
(cross-scope saved-var read confirmed against an exact codebase precedent, `se_LAND.txt:296-345`).
Corrected the stratum set to the real 5 (added tribesmen, dropped indentured/slaves). The taxrate
read (genuinely country-scope) is unchanged. Exact-tick-emits all 11 metrics (10 expense sums +
taxrate) same as before.

**Review verdict:** CLEAN across both the diagnosis (governorship-scope confirmed via setter +
caller trace, real log evidence re-extracted) and the fix (brace balance, cross-scope read
precedent, guard/add field-name match across all 10 blocks, accumulator name consistency
init->accumulate->readback->remove, tick_emit sentinel non-applicability, empty-iteration safety —
all individually verified, zero findings).

**Commit:** `27a70232b`, pushed to `merge-overnight`.

**Status: BLOCKED-ON-DATA (legitimate).** This is diagnostic instrumentation, not a gameplay fix —
it cannot itself reduce the tariffs plateau. The next boot's debug.log will, for the first time,
give REAL per-stratum national expense-base numbers, which are needed to confirm or refute the
surviving silver hypothesis (uncapped, high order-size, moderate local-price in well-stocked zones)
as the actual driver of the ~2000-2500/quarter "Tariffs and shipping" plateau. Continuing to the
rest of the backlog (#96, #97/#98, #99, #101, #103 reconfirm, #105, #106, #107) per the overnight
skill's "a hard block does not stop the run" rule while this awaits its boot.
