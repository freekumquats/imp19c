# early_bookmark_decisions.md — big-decision log for the peak-Qing bookmark

Branch: `early_bookmark` (off `develop` @ 6a31f077). All commits authored+committed by
`freekumquats`. This doc records every *big decision* for the peak-Qing re-target, per the
user's instruction ("note all big decisions in a doc called early_bookmark_decisions").
The reusable methodology lives in `BOOKMARK_PROCESS.md`; this doc is the run-specific log.

---

## Task framing (user's verbatim intent)

> "fire off a research agent in english and chinese academic sources to find which date was
> the height of the Qing dynasty and then adjust the setup file to that year (including
> changing the starting Qing characters and borders and buildings and all other relevant
> data). the changes should be committed to a new branch called early_bookmark once
> completed and after a workflow deep adversarial review."

Accreted constraints:
- "you can and should adjust many more files than the setup file" → full game-start file
  set, not just `00_default.txt` (enumerated in `BOOKMARK_PROCESS.md`).
- "make sure you save the process" → `BOOKMARK_PROCESS.md` written (reusable for other years).
- "note all big decisions in a doc called early_bookmark_decisions" → this file.
- "work continuously until the task is completed" (user away ~5h).

---

## Decision log

### D0 — 2026-07-08 — Branch & process scaffolding
- Created/switched to `early_bookmark`. Confirmed current branch.
- Wrote `BOOKMARK_PROCESS.md`: the reusable year-swap checklist (9 sections + copy-checklist),
  since the user will re-run for other years.
- Completed the full game-start file inventory (see `BOOKMARK_PROCESS.md` §2 table).

### D1 — 2026-07-08 — Research in flight (year choice PENDING research completion)
- Three background research agents running: (a) `ae3547d185d329dd2` peak-Qing year +
  full data package (EN+ZH academic sources); (b) `abdd91cdc8ac2e9e8` treasury/population
  verification; (c) `afc194cbfe8d07473` Qianlong court-roster verification.
- **Strong early signal (NOT yet the final decision):** the verification agents are checking
  the ~70–80 M tael Qianlong-era treasury surplus and the Qianlong Grand Council roster
  (Heshen, Fuheng, Agui, Fuk'anggan) — i.e. the research is converging on the **Qianlong
  reign (乾隆, 1735–1796)** as the height, most plausibly the early-to-mid 1790s (after the
  Ten Great Campaigns / maximal territorial extent, before the 1796 White Lotus Rebellion
  and Heshen's fall began the decline). **Final year + justification to be recorded here on
  research-agent completion, before any historical-content edits.**
- **Rule for downstream work:** do NOT edit historical content (characters, borders,
  treasury figure, OOB) until the year is fixed from research. Non-historical scaffolding
  (process doc, inventory, decision log) proceeds now.

### D2 — 2026-07-08 — Reusable-asset discovery (huge head start)
While the research runs, I audited the existing content to see what a peak-Qing (likely
Qianlong-era) re-target can REUSE rather than invent:

- **Qianlong-era cast already exists in `setup/characters/00_Qing.txt`** as the ancestors of
  the 1815 characters, with correct dates and DNA already authored:
  - `char:214` = **the Qianlong Emperor** (Gaozong/Hongli), birth 1711.09.25, death
    **1799.02.07**, `add_trait = chinese_emperor` — alive for any 1790s start.
  - `char:213` = **Fuheng** (Grand Councillor/general, d.1770), `char:218` = **Fuk'anggan**
    (general, d.1796), `char:224` = Jiaqing (b.1760, the heir), plus consorts/princes 209–227.
  - **Implication:** for a ~1790s start the reigning-monarch swap is mostly a matter of
    changing `set_as_ruler=char:224` (Jiaqing) → `set_as_ruler=char:214` (Qianlong) and
    moving the `c:CHI={ set_as_ruler … }` / court-office seeds onto the era's live figures.
    Characters who died before the chosen year (Fuheng d.1770, Fuk'anggan d.1796) are only
    valid as office-holders if still alive at the start — must be checked per exact year.
  - **BUT:** the 1815 court-bench seed (#166/#177, ≈line 1830) is a *Jiaqing/early-Daoguang*
    bench (Muzhang'a b.1782 etc.). Those figures are children or unborn in the 1790s — the
    bench seed must be re-pointed at Qianlong-era office-holders (Heshen, Agui, Fuk'anggan,
    Wang Jie, Liu Yong, etc.), several of which the roster-verification agent is confirming.

- **Treasury seed is DERIVED, not a hardcoded tael figure:** `QING_seed_starting_treasury`
  (`se_QING_MECHANICS.txt:644`) sets treasury = 12 months of the country's own computed
  costs (multiply = -12). For a peak-Qing surplus year the decision is to *raise that
  multiplier* (e.g. -18 or -24) to represent the large Qianlong-era reserve, rather than
  invent an absolute number — keeps it consistent with the economy sim. Final multiplier
  pending the treasury agent's sourced figure (~70–80 M tael reserve).

- **Borders likely change LITTLE (to be confirmed by research):** Qianlong's conquests
  (Xinjiang/Zungharia 1755–59, Tibet protectorate, Mongolia) were all still held in 1815, so
  the 1815 map's `own_control_core` for CHI is already near the maximal *directly-controlled*
  extent. The peak-Qing distinctiveness was mostly in the **tributary/subject ring** (Burma
  1769, Nepal/Gurkha 1792, Annam 1789, Ryukyu, Korea, Siam, Sulu) and prestige, not in
  additional directly-owned provinces. So the border edit may be small or focused on subject
  relationships rather than large province transfers. **HOLD exact border moves for research.**

### D2b — 2026-07-08 — Subject/tributary ring is already near-peak in the 1815 setup
`setup/main/00_default.txt` already gives CHI a full subject ring via `dependency` lines
(817–870): Tibet (protectorate); Ili/Uliastai/Manchuria/Mukden/Heilongjiang
(autonomous_governorship); Vietnam(VIE)/Nepal(NEP)/Korea(KOR)/Ryukyu(RYU)/TNN (tributary);
plus feudatories (CKL, DER, CHH) and nominal vassals (LAF, FOS, MLM, TNI, LSU). This is the
maximal Qianlong-era directly-controlled + tributary configuration essentially intact.
- **Decision:** for a 1790s Qianlong start, keep this ring; the only *candidate* additions
  are tributaries that had lapsed by 1815 but were active at peak — chiefly **Burma (BUR)**
  (post-1769 war, missions from 1790) and possibly **Siam (SIA)** / **Sulu (SUL)** / **Annam**.
  These are HYBRID additions (add a `dependency` line) IF research confirms they belong and
  IF those tags exist on the map. **HOLD until research confirms tag existence + status.**

### D3 — PENDING — Chosen year + justification
_To be filled from the research agent on completion, before any historical-content edit._

---

## EXECUTION PLAN (edits keyed to research variables — run on year lock)

Notation: `${YEAR}` = chosen start year; `${START}` = `${YEAR}.M.D`; `${STARTP1}` = start+1 day.

1. **`common/defines/00_defines.txt:3`** — `START_DATE = "${START}"`.
2. **Dated-content re-base** (BOOKMARK_PROCESS.md §2 table): for each file, decide keep
   (real-event date still future) vs re-base (relative offset) vs cut (event now past).
   Minimum: `00_specific_from_code.txt` mobilization guard → `current_date > ${STARTP1}`;
   the arc start-gates (japan/mex/usa/qing on-actions at `1815.7.1`) → `${START}`.
3. **Reigning monarch** — in `setup/characters/00_Qing.txt`: move the `c:CHI={ set_as_ruler
   … }` from `char:224` (Jiaqing) to **`char:214` (Qianlong)** [if ${YEAR}<1799]. Add
   `add_trait` era traits + `add_gold`/`add_popularity` as the Jiaqing block currently has.
   Verify Qianlong birth 1711 < ${YEAR} < death 1799.
4. **Court bench re-point** — the #166/#177 bench (chars 700–712) is Jiaqing-era (many born
   1780s, unborn at peak). Replace/supplement with Qianlong-era office-holders confirmed by
   the roster agent (candidates: Heshen, Agui 阿桂, Fuk'anggan(char:218, d.1796), Wang Jie
   王杰, Liu Yong 劉墉, Jiqing, Sun Shiyi 孫士毅, Fukang'an). Each: char block with
   birth<${YEAR}<death, culture/religion, specialty `add_trait`. Characters inside the
   `"CHI"={…}` block are auto-CHI courtiers (no employ logic needed — verified).
5. **Treasury seed** — `se_QING_MECHANICS.txt:662` `multiply = -12` → raise to the sourced
   peak-reserve multiplier (candidate -18…-24; final from treasury agent's tael figure).
   Keep it derived (months-of-cost), not an absolute number, for economy-sim consistency.
6. **Borders** — likely minimal (D2). Apply only research-confirmed province moves in
   `own_control_core`, editing BOTH the gaining and losing country's list.
7. **Subjects** — apply only research-confirmed `dependency` additions (D2b: Burma etc.),
   after verifying each tag exists on the map (`grep 'TAG = {' setup/main/00_default.txt`).
8. **Buildings/OOB** — `SE_qing_starting_buildings` + `SE_qing_armies`/`SE_qing_navy`:
   adjust only if research shows the era's works/garrisons differ materially from 1815.
9. **Laws/government** — review the CHI law list vs the era (D7, pending research).
10. **Verify** (brace + BOM + residual-date grep) → **adversarial review** → **commit as
    freekumquats** + SESSION_REPORT + this doc's final decisions.

<!-- Subsequent decisions (chosen year, exact border moves, character cuts/adds, treasury
     figure, law changes, arc-date handling) appended below as they are made. -->
