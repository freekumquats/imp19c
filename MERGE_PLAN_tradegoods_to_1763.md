# Plan: port trade_goods features → 1763_bookmark (feature-by-feature)

Approach (per user): do NOT bulk `git merge`. Port each discrete feature from trade_goods onto 1763
individually, so both branches' work is preserved and each feature is verified on the 1763 base before the
next. Merge base = `6a31f077` (2026-07-08); trade_goods +15 commits, 1763 +26 since.

Source of truth: **develop** now contains everything trade_goods has PLUS #280/#260/#268 (the clean
trade_goods→develop merge, 38854b19). So "trade_goods features" = develop features. Port from whichever is
convenient; content is identical for the shared set.

---

## The features on trade_goods/develop NOT yet on 1763, in recommended port order

### TIER A — CLEAN ports (1763 does not touch these files; drop-in, low risk)

**A1. #279 New World crops as conditional local staples**
- Files: `se_DEMAND.txt`, `DEMAND_food_svalues.txt`, `DEMAND_food_svalues_new.txt`, `DEMAND_luxury_svalues.txt`.
- 1763 side: **UNTOUCHED (0 lines)** on all of these → take trade_goods' version wholesale.
- CAVEAT: `DEMAND_luxury_svalues.txt` ALSO carries the #281 rifle-demand rewrite — porting it brings both #279
  and part of #281 at once. Fine, but sequence A1 and B1 together (same file).
- Verify: braces, BOM/CRLF; boot-test crop demand on an Americas governorship.

**A2. #281/#290 rifles — production province edits (13 of 14 files clean)**
- Files: `setup/provinces/00_{Austria,Saxony,Brandenburg,Sweden,Low_Countries,Moscow,Kazan,New_England,
  Appalachia,Wales_Mercia,Sankt-Petersburg,Atlantic_France,Auvergne-Rhone-Alpes}.txt` — 1763 UNTOUCHED → clean.
- **BUT** the good must match 1763's post-#278 map: on 1763 these provinces are wool/wood/grain/etc., NOT the
  cloth they were on trade_goods. Porting = set `trade_goods="rifles"` on the SAME 14 province IDs, replacing
  whatever 1763's #278 pass assigned. So re-apply the rifle assignment to 1763's current values (not a blind
  file copy — the surrounding rows differ). Small, mechanical, per-ID.

**A3. #281/#290 rifles — the new unit + gfx (all NEW files, no conflict)**
- Files: `common/units/army_riflemen.txt` (new), the 5 `gfx/models/units/*/*.asset` fallback-entity appends,
  `localization/english/text_l_english.yml` (one line `riflemen:0`).
- 1763 side: these unit/gfx files are untouched → the new file drops in; the .asset appends and the loc line
  apply clean (append-only). Low risk.

**A4. #281/#290 rifles — the demand/supply/logistics svalues**
- Files: `DEMAND_luxury_svalues.txt` (the military DEMAND_rifles — comes with A1), `DEMAND_svalues.txt`
  (DEMAND_army_ratio_rifles constant), `GOODS_svalues.txt` (arsenal rifle-supply term), `se_LOGISTICS.txt`
  (shortage_phys_rifles scan).
- 1763 side: check each — DEMAND_svalues/GOODS_svalues/se_LOGISTICS may have minor 1763 edits; if untouched,
  clean. (se_LOGISTICS scan block is append-in-list, low collision risk regardless.)

### TIER B — COLLIDING file, but NON-OVERLAPPING lines (clean 3-way, verify)

**B1. #281 rifles — Beijing province**
- File: `setup/provinces/00_Zhili.txt` — flagged "changed in both", BUT: 1763's #284 pop rescale changed OTHER
  Zhili provinces' `amount=` lines; trade_goods changed ONLY Beijing 8363's `trade_goods=` line. Verified: 1763's
  Zhili diff does NOT touch the 8363 block. → line-level non-overlapping → 3-way auto-merges, OR just set
  Beijing 8363 `trade_goods="rifles"` on 1763 by hand (it's currently silk there too). Trivial. Also decide:
  keep Beijing as a Qing rifle site (yes — that was the #281 decision).

### TIER C — GENUINE STRUCTURAL CONFLICTS (manual resolution required)

**C1. Event-seed on_actions restructure (#254) vs 1763 offset rebase (+19127)** — THE hard part.
- Files: `usa_section_on_actions.txt`, `japan_bakumatsu_on_actions.txt`, `mex_instability_on_actions.txt`,
  `qing_mechanics_on_actions.txt`, `oa_economy_setup.txt`, `00_specific_from_code.txt`.
- Conflict: trade_goods (develop #254) converted `on_game_initialized` from a bare inline-effect block to the
  NAMED `on_actions = { imp19c_*_on_game_initialized }` LIST form (so it merges across files). 1763 kept the bare
  form but ADDED +19127 days to every `trigger_event = { id=X days={A B} }` offset (rebasing 1815→1763 dates).
- Resolution: take trade_goods' #254 LIST STRUCTURE **and** 1763's +19127 OFFSET VALUES. I.e. wrap 1763's
  rebased seeds inside the named `imp19c_*_on_game_initialized` action block. Per file, by hand.
- RISK: this is where a wrong merge silently breaks event timing (events fire 52 yrs early, or don't fire at
  all). Each file needs careful reconciliation + the #254 rationale check (does 1763 even have the multi-file
  merge problem #254 fixed? If 1763 only ships one such block per file, the bare form may still work — but
  adopting #254 is safer and forward-consistent with develop).

**C2. Qing mechanics — trade_goods has MORE (additive, take fuller side + verify)**
- Files: `se_QING_WORKS.txt` (tg +150 incl. Grand Council #272/#273 + 6-bug batch; 1763 +114 mostly the shared
  #209 re-committed), `se_QING_DECLINE.txt` (tg +154 incl. #272/#273; 1763 +31), `se_QING_GOVERNANCE.txt`,
  `se_QING_MECHANICS.txt`, `qing_governance_l_english.yml`.
- Root cause: both branches independently re-committed #209 (QING_works_pulse) after the split (tg 0852e5c5,
  1763 604dbf5d) → git sees "changed in both". trade_goods then layered the Grand Council expansion (#272/#273)
  + develop bugfixes ON TOP. 1763 did not get those.
- Resolution: take trade_goods' version (it is a superset for these files), but DIFF against 1763 first to
  confirm 1763 made no 1763-specific edit here that would be lost. Mostly "accept theirs" with a review pass.
- NOTE: this is really "port the whole Grand Council expansion #272/#273 + develop diplo/UI bugfix cluster" —
  a develop-feature port, separable from the economy/rifle work. Could be its own tier/phase.

### TIER D — DATA/DOC (cosmetic or take-either)

**D1. `map_data/province_setup.csv`** — 1763 rewrote 18,782 lines (#278 world-econ); trade_goods changed 32
(rifle rows). The CSV is BUILD-TIME-INERT (engine loads setup/provinces/*.txt). → KEEP 1763's version entirely;
the rifle data lives in the province files (A2/B1). Do NOT port trade_goods' CSV rifle rows (they'd fight #278
and don't matter at runtime). Optionally re-sync the 15 rifle rows in 1763's CSV to rifles later for regen
consistency — cosmetic, low priority.

**D2. `setup/characters/00_Qing.txt`** — 1763 +179 (peak-Qing 1759 Qianlong court + unborn-ruler sweeps),
tg +8 (develop council/diplo fixes). KEEP 1763's version; hand-port the tg +8 lines only if they're a real
fix (check what they are — likely the ab925f1b date-poison / council fixes).

**D3. Docs** — `SESSION_REPORT.md`, `new_trade_goods.md`, `RIFLE_PRODUCTION_1815.md`, `DESIGN_LOGISTICS_RIFLES.md`
etc. Take either / concatenate; zero gameplay impact.

---

## Recommended execution phases (each = its own commit + review + boot-test-gate)

1. **Phase 1 — Economy+rifles (Tiers A + B + D1):** the self-contained, mostly-clean feature set.
   #279 crops + #281/#290 rifles (provinces, unit, gfx, demand/supply/logistics, Beijing). ~clean; highest value.
2. **Phase 2 — Event-seed reconciliation (Tier C1):** the 6 on_actions files. Careful manual merge of
   #254-structure × +19127-offsets. Isolate so a timing bug is easy to bisect.
3. **Phase 3 — Grand Council + develop fixes (Tier C2 + D2):** port #272/#273 + the develop diplo/UI/bug
   cluster (#210/#213/#215/#216/#217/#220/#221/#222/#254). Larger; separable; do last.

Also portable (now on develop, not on trade_goods-at-split): **#280 sphere, #260 statesmanship, #268 religion
panel** — if you want 1763 fully current with develop, add these as a Phase 4 (all were clean-merged to develop,
so they're clean ports too).

Each phase: verify braces + byte conventions, adversarial-review workflow, commit as freekumquats, boot-test-owed.
