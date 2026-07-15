# Overnight autonomous run — 2026-07-15

User directive (2026-07-15, user away, work without stopping):
1. Drop #7 from pending tasks. **[DONE]**
2. Finish #4 (reformat ALL ministry panel read-outs into neat tables) → review → commit → push.
3. Switch to `merge-overnight`, pull all `1763_bookmark` branch changes into it.
4. Implement #28 (convert Grand Council offices + Amban into engine positions), oracle-gated.
5. Implement ALL mission trees in `pending_mission_trees.md` (#447/#448/#449/#451 + dropped ideas as feasible).
6. Document every decision here; review + commit + push throughout.

Standing rules in force: commits authored by freekumquats; independent code-review agent before every commit;
preserve each file's existing per-file BOM state (.gui = no-BOM upstream, but PRESERVE actual state); BOM is
NOT a crash cause; scripted_gui compile-recursion crash class (route sorting iterators / create_character /
imprison through hidden trigger_event trampolines); user boot-tests on a SEPARATE machine so MUST push;
oracle-gate any unproven engine capability (consult TI + Invictus).

---

## Task #4 — Reformat ALL ministry panel read-outs into neat tables

**Problem (playtest):** ministry L4 panels' label:value read-out rows don't align — the first ("performance")
row uses a 180px label, later rows use 240px or 300px, and value cells vary 40/60/80/120px, so numbers never
form a column.

**Design decision (user-approved via AskUserQuestion 2026-07-15):**
- Uniform label column = **300px**, value cell = **60px**, both `size = { W 20 }`, row `spacing = 8`.
- Performance row: keep label:value on the aligned row, **move the progress bar to its own full-width line
  below** (option "Bar on its own line"). Bar `size = { 300 12 }`.
- Rows with a conditional two-textbox value (reformed/unreformed, raised/unraised, danger/checked) keep BOTH
  value textboxes but normalize them to the value-column width so whichever is visible lands in the column.
- Roster/dynamicgridbox rows and section-title textboxes (`size = { 460 28 }`) are NOT touched — only the
  label:value read-out `flowcontainer` rows inside the standing/summary sections.

**Panels touched (24, extended beyond the initial 14 for visual consistency — "ALL"):** revenue_ministry,
household, zongli, secretariat, censorate, rites_ministry, war_ministry, works_ministry, lifanyuan, hanlin,
guard, personnel, harem, justice, southern_study, upper_study, caravan, greatgame, opium, population, princes,
province_reports, religion, xinjiang.

**Method:** wrote a brace-aware Python transformer (deleted after use) that recognized a read-out row as a
`flowcontainer` whose direct children are all `textbox`/`progressbar` AND whose first textbox `text` ends in
`_LABEL`; regenerated each in canonical form. Everything else (section titles size {460 28}, character-card
flowcontainers, dynamicgridbox rosters) untouched. All 24 files: braces balanced, no-BOM preserved.

**Code review (code-review agent) — 1 real regression + 4 cosmetic, ALL FIXED:**
- REGRESSION: `qing_province_reports.gui` Canton revenue-split row had a *container-level* `visible` guard
  (#426: shown only while the hoppo-rotation system is open). The transformer dropped container-level
  attributes (it only migrated child-textbox `visible`s). Restored the guard on the flowcontainer.
- CLIPPING (value cells narrowed to 60px but hold descriptive strings, not numbers): widened back —
  harem rank line (皇貴妃…/貴妃…/妃…) → 210; revenue salt reformed/unreformed → 200 each; household eunuch
  danger/checked → 200 each; works hydraulic VALUE → 180. Numeric value cells stay at 60 (they align).
- The two ratio rows (lifanyuan amban/warrant, personnel gov_clean/gov_count) manually kept at 120.

**Progress:** DONE — pending commit + push.
