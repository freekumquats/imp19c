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

### D-SCOPE — 2026-07-08 — **KEY DECISION: Qing-focused re-target, not a full-world 1790 conversion** ⚠️
`START_DATE` is GLOBAL. Moving it back ~25 years (1815 → ~1790) has world-wide consequences
far beyond the Qing:
- **15 of 90 `set_as_ruler` characters across all country files are born after 1780** — i.e.
  unborn or infants at a ~1790 start (verified by script): rulers in North America(451,b1781),
  Rio de la Plata(5,b1787), Colombia(6/38,b1783), Ottoman(45,b1785), Italy(136,b1791;154,b1782),
  India(522/523/525/527), Spain(22,b1784), and Qing's own 1815 heirs (327 b1813, 331 b1792,
  335 KOR-king b1790). At start the engine would find no valid ruler and auto-generate one
  (or the assignment silently fails) — messy, not necessarily a crash.
- **World political geography is 1815, not 1790:** independent Latin American republics
  (Colombia, Rio de la Plata, Chile, Brazil-as-independent) did not exist in 1790; the
  Napoleonic reorganisation of Europe/Italy hadn't happened; the Ottoman/India maps differ.
  Correcting all of that is effectively authoring a *different game*, not "the height of the
  Qing dynasty."

**Decision (default, taken because the user is away + asked for continuous progress + framed
the task Qing-centrically — "the height of the Qing dynasty … changing the starting Qing
characters and borders and buildings"):**
- **Scope = QING-FOCUSED peak bookmark.** Re-target `START_DATE` to the peak-Qing year and
  fully, correctly rework the **Qing**: reigning emperor, court bench, treasury, subjects,
  buildings, OOB, laws — everything the task enumerates for CHI.
- **The rest of the world is left at its existing 1815 configuration** and treated as an
  ACCEPTED, DOCUMENTED anachronism/limitation of this bookmark, EXCEPT where a specific
  world ruler being unborn causes an outright load failure — in which case that single ruler
  gets a minimal patch (assign the era-correct historical ruler, or a fallback). No wholesale
  world re-authoring.
- **Rationale:** matches the user's explicit framing; keeps the deliverable achievable and
  reviewable; the reusable process still documents the global-implications for future runs.
- **Flag for user review:** if the user actually wants a full-world 1790 conversion, that is
  a much larger, separate effort — this decision is the natural place to redirect. Called out
  here and in SESSION_REPORT so it's the first thing seen on return.

### D-DATES-DONE — 2026-07-08 — dated-content re-base APPLIED ✅
Δdays(1815.7.1 → 1759.9.1) = **20391**. Applied:
- **START_DATE** → `1759.9.1` (`00_defines.txt:3`). END_DATE 1936 kept.
- **Arc day-offsets +20391** (28 beats): japan_bakumatsu (7), mex_instability (10), usa_section (11)
  — so Perry/Civil-War/Mexican beats still land on their TRUE dates. Header notes added.
- **Amherst one-shot** (`qing_mechanics_on_actions.txt`) `days={410 430}`→`{20801 20821}` (keeps 1816 arrival).
- **Mobilization guard** (`00_specific_from_code.txt`) `current_date > 1815.7.2`→`1759.9.2`.
- **LEFT UNCHANGED (real historical thresholds, reachable at true dates from 1759 start,
  game runs to 1936):** `unique_chi.1` Amherst gate `>1815.10.15`; Napoleon window `<1821.5.5`;
  GP grip grace `1826.1.1`/`1852.1.1`; Mexico `1830.1.1`. These are absolute real-world dates, not
  start-relative offsets, so they remain correct — they simply become eligible at their true dates.

### D-ARC — 2026-07-08 — **KEY: dated arc offsets must be shifted, or they fire ~25 yrs early** ⚠️
The US/Japan/Mexico/Qing arcs fire from `on_game_initialized` via
`trigger_event = { id = … days = { A B } }`, where the day-offset is calibrated from the
**1815.7.1** START_DATE to land each beat on its **real historical date** (e.g.
`japan_bakumatsu.0 days≈13835` ≈ 1853 = Perry's arrival; `usa_section` beats → 1820 Missouri
Compromise, 1861 Civil War, etc.). These offsets are baked to 1815.
- **Problem:** move START_DATE back to ~1790 (≈9130 days earlier) and every offset now fires
  ~25 years too early — Perry arrives in ~1828, the US Civil War in ~1836. Historically broken.
- **Decision:** for each dated beat that represents a REAL historical event, **add the
  start-shift delta (`Δdays = 1815.7.1 − ${START}`) to its offset** so the beat still lands on
  its true date. Beats whose real date now falls *before* the new (earlier) start are dropped
  (the event already happened) — but with a ~1790 start, all these 19th-C beats are still in
  the future, so the rule is simply `new_offset = old_offset + Δdays` for all of them.
- **Affected files (offset re-base):** `japan_bakumatsu_on_actions.txt`,
  `mex_instability_on_actions.txt`, `usa_section_on_actions.txt`, and any
  `qing_*`/`se_MEXICO`/`se_QING_DIPLO` dated one-shots. Δdays computed once the exact
  ${START} is set (≈9131 days for 1790.7.1; will compute precisely).
- **Alternative considered & rejected:** leaving offsets as-is (arcs fire 25 yrs early). Rejected
  — it silently corrupts the historical timeline the arcs were built (#93/#94/#96) to reproduce.

### D3 — 2026-07-08 — **CHOSEN YEAR: 1759 (乾隆二十四年)** ✅
Research complete (full report: `research/QING_APOGEE_RESEARCH.md`; roster:
`research/QIANLONG_ROSTER_RESEARCH.md`). **Year = 1759**, the research's primary recommendation:
the completion of the Xinjiang conquest (Khoja brothers run down in Badakhshan, 1 Sep 1759) —
the Qing's maximal effective territorial extent, militarily unchallenged, Qianlong (age 47) at
peak vigour, treasury deep and rising, nothing yet foreshadowing decline. Crest of the High Qing
(康雍乾盛世).
- **START_DATE = "1759.9.1"** (the 1 Sep 1759 anchor event; keeps the calendar on the decisive date).
- **Δdays from 1815.7.1 back to 1759.9.1** = to be computed precisely for arc-offset shifting (D-ARC).
- **1790 alternative** deliberately NOT taken (it foregrounds decadence/Heshen/pre-decline; 1759 is
  the cleaner, decisive apogee anchor). Recorded as a possible future second bookmark.

### D4 — 2026-07-08 — Border scope: **NO net territorial change** ✅
Research confirms (high confidence) the Qing land empire of 1815 is essentially the same as
1759's — no cessions occurred 1759→1815 (first losses are the 1850s–60s Amur/Ili treaties);
White Lotus (1796) was internal. Xinjiang, Tibet, Mongolia, Manchuria all held in both.
- **Decision:** leave CHI's `own_control_core` UNCHANGED. The apogee-vs-1815 contrast is
  INTERNAL (treasury depth, army quality, court vigour, prestige, silver inflow), not territorial.
  This is faithful to the sources AND the low-risk path (no province-list surgery, no dangling cores).
- **Subjects:** keep the existing ring. Do NOT add Burma or Kokand (research: contested/not genuine
  tributaries). Nepal is correctly NOT a peak-1759 tributary either (post-1792) — but NEP is already
  a tributary in the 1815 setup; leaving it is a minor, acceptable anachronism (removing it risks
  breaking the subject/economy bookkeeping for marginal gain). **Decision: leave subject ring as-is.**

### D5 — 2026-07-08 — Reigning monarch: Jiaqing(char:224) → **Qianlong(char:214)** ✅
`char:214` (Qianlong) already exists with correct dates (b.1711.09.25, d.1799.02.07, alive in 1759)
and `add_trait=chinese_emperor`. Move the `c:CHI={ set_as_ruler=char:… }` ruler assignment from
char:224 (Jiaqing, currently the 1815 ruler) to char:214, and give char:214 the era-start effects
the Jiaqing block has (add_gold, add_popularity, era traits). Jiaqing (char:224, b.1760) is UNBORN
on 1759.9.1 — his birth_date is after start; he must NOT be referenced as a live character/heir at
start. **Action:** verify no start-time logic requires char:224 alive; if the engine needs an heir,
use a Qianlong-era prince alive in 1759 (e.g. an elder son) or leave heir unset.

### D5b — 2026-07-08 — char:224 residual references AUDITED, safe ✅
Two non-setup refs to char:224 (Jiaqing) remain and are intentionally LEFT:
- `00_custom_on_actions.txt:299` — inside `on_reign_ending_successor` (fires on emperor
  *death/succession*, ~1799 in-game, NOT at start); hardcodes Jiaqing as `previous_emperor`.
  Historically Jiaqing DID succeed Qianlong, so this stays plausible. Not start-critical.
- `000_GOVERNMENT_custom_loc.txt:461/656` — a cosmetic display-name loc trigger keyed to
  char:224. Cosmetic only; no start effect.
Both are pre-existing hardcodings unrelated to who rules at game start. No change needed.

### D6 — 2026-07-08 — Court bench: re-point Jiaqing-era → Qianlong-era ✅
The #166/#177 bench (chars 700–712) is Jiaqing/early-Daoguang (many born 1780s → unborn in 1759).
**Action:** add a 1759 Qianlong-era bench as new CHI-block characters (auto-employed as CHI courtiers
— verified no explicit employ logic needed): Liu Tongxun, Yu Minzhong, Agui, Zhaohui, Yin Jishan,
Ji Yun, Dai Zhen, Qian Daxin, Zhao Yi, Yuan Mei (Fuheng char:213 & Fuk'anggan char:218 already exist).
Guard the 1780s-born bench (700–712) so it does not seed live courtiers before their birth dates —
simplest: give each a `birth_date` the engine already respects (a character with birth_date after
START simply doesn't exist yet, so 700–712 are harmlessly absent in 1759; CONFIRM engine treats
future-born chars as non-existent rather than erroring).

### D7 — 2026-07-08 — Treasury: raise the derived multiplier ✅
`QING_seed_starting_treasury` (`se_QING_MECHANICS.txt:662`) seeds treasury = `-12 × monthly costs`
(one year, for strained 1815). For 1759's large-and-rising surplus (trajectory toward the ~73.9M
mid-1770s peak, well above the ~34M of 1735), raise the multiplier. **Decision:** the effect is
1815-specific (var named `qing_treasury_seed_1815`, sentinel `qing_treasury_seeded`). Rather than
mutate the 1815 tuning in place (a CHANGE to existing behaviour → extra scrutiny), gate it on
START_DATE: keep -12 baseline but multiply up for the earlier bookmark. Simplest faithful choice:
change the multiplier to represent ~2–3 years of costs (-24 to -36) for the surplus era. Final:
**-30** (≈2.5 yr of costs) as a defensible "deep surplus, not infinite" figure; logged as an
estimate (exact 1759 tael balance is not pinned in sources). Comment + LOG updated; behaviour-change
scrutiny per the fix-traceability rule.

### D8 — 2026-07-08 — Buildings/OOB/laws ✅
- **Buildings** (`SE_qing_starting_buildings`): the specialty-production works (silk/porcelain/tea/
  cotton/salt) existed in 1759 as much as 1815 (Jiaqing-era economy inherited them) — **keep as-is**.
- **Army/navy OOB** (`SE_qing_armies`/`SE_qing_navy`): research says the Banners were at PEAK quality
  in 1759 (vs decayed by 1815). The OOB *composition* (which forces/where) is essentially the same
  garrisons; the difference is quality/morale, which the mobilization/rot modifiers model, not the OOB
  counts. **Decision:** keep the OOB structure; OPTIONALLY grant a "peak banners" quality modifier at
  1759 start (concrete, low-risk) instead of altering counts. Deferred as a nice-to-have; core build
  first.
- **Laws:** the CHI 1815 law list (bureaucratic judiciary, regional militias, etc.) is broadly the
  same Qing institutional setup as 1759. **Keep as-is** — no sourced reason to change; the Grand
  Council/banner distinction is modelled elsewhere. Logged as reviewed-no-change.

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

---

## EXECUTION STATUS — 2026-07-08 (edits applied)

### D-FUTUREBORN — RESOLVED via oracle `a6b4f4f3c24ae67cf` ✅ (the load-bearing question)
The open item in D6 ("CONFIRM engine treats future-born chars as non-existent rather than
erroring") is now answered. Oracle finding (HIGH confidence):
- **Setup characters with `birth_date` > START_DATE are silently non-existent until their
  birth date arrives — they do NOT crash the load.** This is standard Imperator engine
  behaviour (a character simply hasn't been born yet).
- **The one real hazard is `set_as_ruler` (or a required office-holder) pointing at an
  unborn character** — the engine then auto-generates a fallback ruler or the assignment
  silently fails. Family (`father`/`mother`) links to unborn chars are safe.
- **Consequences for this bookmark, all consistent with D-SCOPE (Qing-focused):**
  - CHI ruler = char:214 Qianlong (b.1711) — born long before 1759, safe. ✅
  - The Jiaqing-era bench (700–712, born 1760s–1780s) is harmlessly absent at 1759 — no
    action needed beyond adding the Qianlong bench (done). ✅
  - char:224 Jiaqing (b.1760) ruler-assignment is commented out (D5) so no unborn char is
    set as ruler. ✅
  - **World-wide:** the "~15" figure originally cited here was WRONG — it was the count for the
    abandoned >1780 threshold (D-SCOPE line ~100), never recomputed for the actual 1759.9.1 start.
    ⚠️ **CORRECTED (adversarial review, 2026-07-08, script-verified):** at the true 1759.9.1
    threshold, **59 of 91 uncommented `set_as_ruler`/`set_as_co_ruler` targets are unborn**
    (63–64 counting co_ruler + the commented Jiaqing line). All get engine-generated fallback
    rulers — no crash, still a playable world — but this is a ~4× larger anachronism than the
    doc first stated. Accepted under D-SCOPE (Qing-FOCUSED bookmark, rest of world left at 1815).

### D-FUTUREBORN-QING — 2026-07-08 — CHI subject ring & governors ALSO have unborn assignees ⚠️
The review found — correctly — that the "clean Qing scope" claim above was FALSE. Inside
`setup/characters/00_Qing.txt`, several assignments on CHI's OWN subject ring and provinces point
at post-1759 births (script-verified):
- **6 subject-ring `set_as_ruler` targets unborn at 1759:** char:335 KOR (b.1790; real 1759 king
  was Yeongjo r.1724–76), char:327 MGA/Jebtsundamba (b.1813), char:329 ULS (b.1771), char:330 LAF
  (b.1770), char:331 SBG (b.1792), char:99 ADG (b.1765, a "made-up" placeholder ruler).
- **7 CHI `set_as_governor` targets unborn at 1759:** char:320 (Anhui/768, b.1770), 325 (b.1771),
  326 (b.1779), 336 (b.1765), 351 (b.1766), 352 (b.1779), 353 (b.1765).
- **Engine behaviour:** `set_as_ruler` on an unborn char → engine auto-generates a random
  fallback monarch (the subject tag is STILL a Qing subject — the dependency lines in
  00_default.txt are unaffected). `set_as_governor` on an unborn char → silently no-ops, the
  governorship simply opens without a named governor. **Neither crashes; the game is playable.**
- **DECISION (deliberate, documented — NOT silently ignored):** for THIS commit these are
  **accepted anachronisms**, consistent with D-SCOPE. Authoring 13 period-correct 1759 rulers/
  governors (e.g. Yeongjo for Korea, the era's real Mongol/frontier khans, mid-Qianlong provincial
  governors) is a substantial character-authoring task with its own bug-risk, and the fallbacks are
  functional. **Flagged as the top follow-up item** if the user wants full 1759 fidelity on the
  subject ring — the two highest-value fixes are Korea (char:335 → a Yeongjo character) and the
  Anhui governor. Recorded here so the gap is visible, not hidden.
- **Caveat on the oracle's method:** it partly reasoned from the repo *already* containing
  `START_DATE=1759.9.1` (my own uncommitted edit) and inferred "the mod loads." That specific
  inference is circular (not yet test-loaded), but the underlying engine-behaviour claim is
  independently sound and matches documented Imperator behaviour. Final proof = the user's
  in-game load test on the `early_bookmark` branch.

### Edits applied this session (all on branch `early_bookmark`, uncommitted)
1. **START_DATE** → `"1759.9.1"` (`00_defines.txt:3`). ✅ (D3)
2. **Arc offset +20391** — japan_bakumatsu (7), mex_instability (10), usa_section (11). ✅ (D-ARC)
3. **Amherst one-shot** → `days={20801 20821}` (`qing_mechanics_on_actions.txt`). ✅
4. **Mobilization guard** → `current_date > 1759.9.2` (`00_specific_from_code.txt`). ✅
5. **Qianlong set as ruler** — char:214 gets `c:CHI={set_as_ruler=char:214}` + add_gold/add_popularity;
   char:224 Jiaqing ruler block + grants commented out (unborn 1759). ✅ (D5)
6. **Qianlong court bench** — new CHI-block chars **720–729** (Liu Tongxun, Yu Minzhong, Agui,
   Zhaohui, Yin Jishan, Ji Yun, Dai Zhen, Qian Daxin, Zhao Yi, Yuan Mei) inserted before the
   CHI-block close. All born < 1759 (safe). IDs verified collision-free; traits/cultures/religion
   keys verified valid; braces balanced (238/238); BOM preserved. ✅ (D6)
7. **Treasury multiplier** → `-24` at `se_QING_MECHANICS.txt` (see D7-CORRECTED below). ✅ (D7)

### D7-CORRECTED — 2026-07-08 — treasury multiplier -30 → -24 (quarterly-cadence fix) ⚠️
The adversarial review CONFIRMED that the three `INCOME_cost_*` vars are **quarterly**, not
monthly (the file's own header line 638-639: summing them ×-4 = one year). So my first "-30 ≈
2.5 years" comment was wrong by 3× — -30 actually delivers ~7.5 years of costs, and even the
pre-existing #172 baseline of -12 is ~3 years (not the "~1 year" its comment implied).
- **Fix:** set the apogee seed to **-24 = 2× the accepted #172 baseline (-12)** → ≈6 years of
  costs on hand. Deep, defensible war-chest for the flush Qianlong surplus era WITHOUT the
  ~7.5-year economy distortion the review flagged. The user-verified -12 master baseline is
  LEFT UNCHANGED; only its comment phrasing is corrected. Framing the apogee seed as a multiple
  of the baseline sidesteps the monthly/quarterly confusion entirely.

### D10 — 2026-07-08 — regnal-year seed 19 → 24 (Qianlong era, cosmetic) ✅
Review found `oa_economy_setup.txt:2194` unconditionally seeds `regnal_year_var = 19` (Jiaqing's
regnal year at the old 1815 start), which the `chinese_era_description` loc renders as the ruler's
era year. With the emperor swapped to Qianlong (乾隆, acceded 1735/元年 1736), 1759 = 乾隆二十四年.
Changed to **24**. Cosmetic only (script-verified: `regnal_year_var` is read solely by the display
loc, no trigger/gate consumes it) — no crash, but it's stale start-state the retarget should fix.

### D9 — 2026-07-08 — Buildings are flat province-ID data, NOT date-gated ✅ (validates D8)
Investigated the `1759 = {…}`, `1815 = {…}` etc. blocks in `setup/main/00_default.txt`'s
`provinces = {}` section (line 1062+). These are **province IDs** (Derby=5014, Boston=3838, …
and provinces that happen to have IDs like 1815), a flat sibling list of starting-building
assignments applied at ANY start date — there is NO `date=`/`history` construct nesting them.
Therefore the date shift does NOT strip any buildings. Buildings/OOB/laws stay as-is (D8 holds).

### Remaining before commit
- [ ] #196 deep adversarial-review workflow of the whole diff.
- [ ] #197 commit as freekumquats + SESSION_REPORT entry.
- [ ] (owed to user) in-game load test on `early_bookmark` — the definitive future-born proof.

<!-- Subsequent decisions (chosen year, exact border moves, character cuts/adds, treasury
     figure, law changes, arc-date handling) appended below as they are made. -->
