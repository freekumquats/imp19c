# 1763_bookmark.md — master decision & change log for the 1763 post-war → full-world bookmark

**Branch:** `1763_bookmark` (off `develop`; renamed from `early_bookmark`). All commits authored **and**
committed by `freekumquats`.
**Engine:** Imperator: Rome (Clausewitz-Jomini), Paradox script. Total-conversion mod "Imperatrix: Victoria".

This is the SINGLE master log for the whole bookmark program. It supersedes the earlier
`early_bookmark_decisions.md` (Qing-only) and cross-references `BOOKMARK_PROCESS.md` (reusable
methodology). Everything material — research findings, scope decisions, per-file changes, review
findings, and open items — is recorded here.

> **DATE PIVOT (2026-07-08):** the target moved **1759.9.1 → 1763.2.16**. Rationale from the user:
> pick the day **after the Treaty of Hubertusburg (signed 15 Feb 1763)**, which is also five days
> after the **Treaty of Paris (10 Feb 1763)** — i.e. the exact moment the Seven Years' War has JUST
> ended, so the world map starts **at peace with zero active great-power conflict**. The interim
> 1759.9.1 apogee framing (offset +20391) is SUPERSEDED; wherever "1759"/"apogee" survives in older
> notes below it is retained only as history of the decision.

---

## 0. PROGRAM SCOPE (as directed by the user, cumulative)

1. **Re-target the game to 1763** (day after Hubertusburg; end of the Seven Years' War). ✅ DONE for
   the date mechanic + Qing; see Part A.
2. **Update the rest of the world to 1763**, with the SAME depth of native-language academic research.
   User-chosen scope: **RULERS + FULL POLITICAL MAP** — re-authoring the map itself (undo Latin
   American independence → restore Spanish/Portuguese colonial empires per the 1763 Peace of Paris
   settlement; restore pre-Napoleonic Europe incl. Poland-Lithuania & the HRE states & pre-unification
   Italy incl. Venice & Genoa; Zand not Qajar Persia; divided Vietnam; Ayutthaya Siam; collapsed-Mughal
   India; pre-Sokoto Africa; etc.). Largest, highest-risk option.
3. **Validate the Qing 1763 economy** (buildings / trade goods / production) against deep historical
   research — confirm what's valid, flag anachronisms, fix. ✅ Reviewed (see Part C).
4. **Research + update the rest-of-world economy** (buildings / trade goods / production) for 1763.
5. Document all major decisions & changes here (this file).

**Method (all workstreams):** native-language academic sources (EN + FR/DE/RU/ES/PT/ZH/AR/TR/FA/… as
region demands); consult the Terra-Indomita + Invictus oracles before building on any UNPROVEN engine
capability (STANDING RULE); prefer concrete on-map objects over abstract counters; deep adversarial
review workflow before commit; task-tagged comments + se_LOG markers + SESSION_REPORT entries.

**Reality check on "full political map":** Imperator province *geometry* is fixed (the mod ships a
1815 province map). "Full political map" therefore means reassigning existing provinces'
owner/controller/core + tag, adjusting subjects/de-jure, and creating country tags IF the setup
supports it — it does NOT mean re-drawing province shapes. The feasibility scout (#198, DONE) determined
per-region what is representable. Regions that cannot be faithfully represented are documented as
explicit limitations, not silently approximated.

---

## WHY 1763 ≈ 1759 FOR THE QING (the date-pivot check the user asked for)

The user's hypothesis was: "the only major Qing change 1759→1763 is the Canton System being formalized,
which is a plus if anything." Confirmed, and it's net-positive:
- **Canton System (一口通商):** the single-port edict was **1757**; the tightening 防範外夷規條
  ("Regulations for Preventing Barbarians") followed the **1759 Flint Affair**. So by 1763 the system is
  **fully formalized** — an *addition* to Qing flavour, not a loss. ✅
- **Ili General office (伊犁將軍):** established **1762**. At the interim 1759 target this was logged as a
  ~3-year anachronism (accepted); **at 1763 it is now historically CORRECT.** ✅ (fixes an old caveat)
- **Borders / subjects / population:** essentially identical (first territorial losses are the 1850s–60s
  Amur/Ili treaties; Qianlong reigns until 1796). No regression.
- **Regnal year:** 1763 = **乾隆二十八年** (Qianlong acceded 1735, era from 1736) → `regnal_year_var = 28`
  (was 24 at the 1759 framing, 19 at 1815). Cosmetic loc only.
- **Treasury:** 1763 still sits in Qianlong's flush surplus era; the -24 seed (≈6yr war-chest, 2× the
  1815 baseline) remains valid. Unchanged.

Net: the pivot **improves** Qing period-accuracy and removes the one standing anachronism.

---

## PART A — DATE MECHANIC + QING (DONE)

Older Qing detail lives in `early_bookmark_decisions.md` and `research/QING_APOGEE_RESEARCH.md` +
`research/QIANLONG_ROSTER_RESEARCH.md`. Condensed record of the current (1763) state:

### A1. Year & anchor
- **1763.2.16**, START_DATE `"1763.2.16"` — day after the Treaty of Hubertusburg. Seven Years' War over.
- **Δdays(1815.7.1 → 1763.2.16) = 19127** (real-Gregorian day count; matches the convention the prior
  +20391 used). Every start-anchored dated arc offset re-based **+19127** (i.e. **−1264** from the old
  1759 values of +20391).

### A2. Changes applied (files) — all task-tagged `[bookmark-1763]`
- `common/defines/00_defines.txt:3` — START_DATE → 1763.2.16. END_DATE 1936.2.17 kept.
- Dated `on_game_initialized` arc offsets re-based to **+19127** across japan_bakumatsu (7 beats),
  mex_instability (10), usa_section (11), the Amherst one-shot (`qing_embassy.2` → {19537 19557}), and
  the pre-Perry backstop `qing_japan_preperry.10` (→ {32947 33067}) — so Perry (~1853), the US Civil
  War, Mexican independence, the Amherst embassy (1816), etc. still land on their TRUE dates.
  Effect-relative offsets ({1 3}/{1 5}/{3 12}/{120 300}) correctly left unshifted.
- `00_specific_from_code.txt` — mobilization game-start guard → `current_date > 1763.2.17`.
- `oa_economy_setup.txt` — `regnal_year_var 24 → 28` (乾隆二十八年; cosmetic loc).
- `se_QING_MECHANICS.txt` — treasury seed multiplier stays **-24** (≈6yr war-chest); comment re-anchored
  to 1763.
- Comment banners in all touched on_action files re-worded from the 1759/+20391 framing to 1763/+19127.
- `setup/characters/00_Qing.txt` — reigning emperor is **Qianlong (char:214, b.1711 d.1799)** (Jiaqing
  char:224 b.1760 still commented out — he is unborn at 1763 too). Qianlong court bench chars 720–729
  all born < 1763 (unchanged from the 1759 work; all valid at 1763). *(Carried over from Part A of the
  earlier build; unaffected by the 4-year pivot.)*

### A3. Deliberately UNCHANGED (research-justified)
- **Borders & subjects** — 1763 ≈ 1815 Qing land empire (first cessions are 1850s–60s treaties).
- **Ili governorship** — now CORRECT at 1763 (est. 1762); the old ~3yr-anachronism caveat is retired.
- **Buildings / OOB / laws** — building data is a flat province-ID list, NOT date-gated → the date
  shift strips nothing. Economy validity handled separately in Part C.

### A4. Key engine finding (oracle-verified) — future-born characters
- Setup chars with `birth_date` > START_DATE are **silently non-existent until born (no load crash)**.
- Only `set_as_ruler` on an unborn char auto-generates a fallback monarch; `set_as_governor` silently
  no-ops. Family links to unborn chars are safe.
- **Load-bearing fact for the whole world re-target** — the map/ruler work will not crash the load;
  worst case is fallback rulers where we don't supply a 1763 character. NOTE: moving 1815→1763 makes
  MORE setup characters unborn, so the 1763 rulers we author (Part B) directly reduce fallback count.

### A5. Adversarial review (earlier, task #196) — SHIP, no crash blockers; 4 findings fixed
Treasury cadence (-30→-24), regnal year, unborn-ruler count correction, doc fixes. All folded in.
A fresh adversarial review is OWED for the 1763 date-pivot edits + all world edits (see Open Items).

**OWED to user:** in-game load test on `1763_bookmark` — the definitive future-born-character proof.

---

## PART B — REST OF WORLD: 1763 RULERS + FULL POLITICAL MAP (RESEARCH IN, EDITS PENDING)

### B0. Feasibility scout (#198, DONE) — headline findings
Overall feasibility **MEDIUM-HIGH**. Engine supports arbitrary province owner/control/core reassignment
via `own_control_core` blocks in `setup/main/00_default.txt`; subjects via `dependency` lines; de-jure is
culture-driven (survives political changes). **647 tags ship.** Regression surface is **minimal** —
hard-coded tag refs cluster in 9 Qing mission files (CHI/RUS/GBR/FRA); Latin-American & Italian tags have
**zero** mission/event dependencies.
- **MISSING tags (the real gaps):** Lithuania/PLC (POL exists but is the 1815 rump Congress Poland),
  **Venice (VEN)**, **Genoa (GEN)**, Milan (part of 1815 Lombardy-Venetia). Ecclesiastical electorates
  (Mainz/Trier — TRI collides with Tripoli) may need coverage.
- **Tag creation:** `create_country` (province-anchored runtime spawn) is PROVEN in-repo
  (flavour_middle_east.txt spawns 5 Arabian tags); `change_country_tag` exists but is commented-out
  everywhere → **do not rely on it**. Mass `create_country` at scale is UNPROVEN → **oracle consult
  required** (Terra-Indomita/Invictus) before building the PLC/Venice/Genoa spawns.
- **Rulers:** ~100 `set_as_ruler` calls; most vanilla. Full 1763 ruler replacement needed for
  Europe/Americas. Character roster rebuild is mandatory (DNA/portrait strings needed).
- **Recommended path:** Phase 1 proof-of-concept (Poland-Lithuania + Venice + New Spain) → validate boot
  → then full map surgery. HIGH-RISK regions: Poland-Lithuania, Italy (Venice/Genoa).

### B1. Research delivered (native-language, by region) — files in `research/`
Rulers + political-map-delta-vs-1815 (several also carry economy, merging the #200/#201 fan-out):
- `1763_WORLD_WEurope.md` — France/GB/Spain/Portugal/Dutch/Austrian Netherlands (running/landed).
- `1763_WORLD_CEurope_HRE.md` — HRE structure (the single biggest European delta: hundreds of states
  incl. ecclesiastical electorates, all gone by the 1815 German Confederation), Austria/Prussia/Saxony/…
- `1763_WORLD_Americas.md` — **the 1763 Peace of Paris partition** (France→GB Canada+east-Mississippi;
  France→Spain Louisiana; Spain→GB Florida) + Spanish viceroyalties + Portuguese Brazil (capital→Rio
  1763) + the **1815-independent-tag → 1763-overlord mapping table** (critical for the edit).
- `1763_WORLD_Italy.md` — state-by-state incl. the two MISSING tags **Venice** (indep., →Austria 1797)
  and **Genoa** (indep., →Sardinia 1815); 1763→1815 transformation table.
- `1763_WORLD_Ottoman_MENA.md` — Ottoman (Mustafa III), **Zand Persia** (Karim Khan, not 1815 Qajar),
  Morocco, Oman, **First Saudi State/Diriyah** (exists 1763, destroyed 1818), Egypt/Iraq Mamluks.
- `1763_WORLD_SouthAsia.md` — collapsed Mughal (Shah Alam II) + Maratha confederacy post-Panipat +
  Durrani + Bengal-EIC + Mysore/Hyderabad; multipolar patchwork vs 1815 EIC raj.
- `1763_WORLD_EAsia_SEAsia.md` — Edo Japan (Ieharu), Joseon (Yeongjo), **divided Vietnam** (Trịnh/Nguyễn,
  not unified 1815 Nguyễn), **Ayutthaya Siam** (not Bangkok), Konbaung Burma, VOC insular SE Asia.
- `1763_WORLD_Africa.md` — Asante/Oyo/Dahomey, **pre-Sokoto Hausa states** (no 1804 Caliphate),
  Ethiopia, **Dutch (not British) Cape**, Omani Swahili coast.
- Teammate deep-dives: `1763_rulers_sweden.md`, `1763_rulers_poland_lithuania.md`,
  `1763_rulers_crimea_ottoman_vassals.md`.

### B2. Phase-1 proof-of-concept — PLC / Venice / (Latin America) map surgery + REVIEW FIXES
Phase-1 built LIT (Grand Duchy, 8 prov ex-RUS) + POL→LIT `royal_union`, VEN (13 prov), and the
GEN/MIL tag registrations. A post-build adversarial review (2026-07-08) confirmed the province
surgery is clean and load-safe (exact 8+13 moves, no double-ownership, capitals valid, keys
resolve, BOMs correct, braces balance) and surfaced ONE real finding, now resolved:

- **PLC started as a Russian *royal_union* (wrong mechanic + wrong ruler).** The 1815 baseline
  line `dependency = { first = RUS second = POL subject_type = royal_union }` ("Congress Poland")
  was left in place, so at 1763 (a) POL booted as a Russian subject AND (b) `royal_union`'s
  `has_overlords_ruler = yes` put the *Russian Tsar* on the Polish throne.
  - **User decision:** keep PLC as a Russian **protectorate** at game start — slightly
    anachronistic at Feb 1763 (the formal client relationship follows: Poniatowski's
    Russia-backed election 1764, the Repnin guarantee 1768) but broadly true of the
    Commonwealth's real dependence (Russian interference since the 1717 Silent Sejm; Seven
    Years' War transit rights). Changed the type `royal_union → protectorate`
    (`00_default.txt:718`): `has_overlords_ruler = no`, so **POL keeps its own king**.
  - The resulting nested chain **RUS → POL(protectorate) → LIT(royal_union)** is fine — the 1815
    baseline ships ~14 nested chains, including CHI's own (`CHI → ILI → XNG`, `CHI → TIB →
    feudatories`) and royal_union-under-royal_union (`AUS → HUN → CRO`). The reviewer's
    "unproven nesting" caveat is retired; recorded in memory (imp19c-nested-subjects-viable) so
    it is not re-litigated. Subject-type `allow` blocks gate runtime diplomacy only, NOT
    setup-placed dependencies.
- **POL cleanups folded in (same pass):**
  - `government` `viceroyalty → aristocratic_monarchy` (`00_default.txt:41291`): viceroyalty is
    the 1815 Congress-Poland *vassal* government; a sovereign szlachta elective monarchy is
    `aristocratic_monarchy` (matches LIT).
  - **1763 ruler authored:** new **char:730 = Augustus III (Wettin)**, King of Poland & Grand
    Duke of Lithuania from 1733, also Elector of Saxony (`00_Poland.txt`). Alive at the 16 Feb
    1763 start; d.5 Oct 1763 (~8 months in — historically triggered the 1764 election). POL's
    `set_as_ruler` pointer moved off char:14 (Józef Zajączek, b.1752 — an 11-yr-old child in
    1763, a Napoleonic-era figure; retained as a defined char but no longer the game-start ruler).

**Post-Phase-1 boot-test fixes (2026-07-08, task #218 + Latin-American leg):**
- **#218 — LIT detached-provinces bug.** The user's boot test as LIT showed Lithuania as a
  scatter of isolated provinces embedded in Russia. Root cause: LIT's initial `own_control_core`
  held only 8 provinces cherry-picked from 6 different areas, leaving the rest RUS. FIXED by
  giving LIT the FIVE COMPLETE core Grand Duchy of Lithuania areas — **Vilno, Grodno, Minsk,
  Mogilev, Vitebsk (95 provinces)** — and removing those 88 from RUS. The stray Kiev-area
  province (2669) was NOT given to LIT and instead consolidated into RUS: by 1763 Kiev city +
  left-bank Ukraine were Russian (Andrusovo 1667 / Eternal Peace 1686) and Right-bank Ukraine
  was the Polish Crown, never the Grand Duchy. Historical extent per
  `research/1763_rulers_poland_lithuania.md`. Verified: braces balanced, all 95 now LIT, 2669 now
  RUS, zero double-listed provinces. (Supersedes the original "8 prov ex-RUS" figure above.)
- **Latin-American reversion leg (Mexico).** The chosen minimal PoC leg reuses the `dependency`
  mechanic (no province surgery): 1815-independent **MEX** is bound to **SPA** as a
  `client_colony` (`00_default.txt:771`), matching the existing Spanish colonial pattern
  (SPA → NSP/QTO/PR1 client_colonies already in the 1815 baseline). MEX's `government` changed
  `revolutionary_republic → viceroyalty` (the 1821-independence republic is wrong for 1763; a
  Bourbon viceroyalty matches NSP/QTO/PR1). Provinces/culture untouched — reversible, low-risk.
  This validates the Spanish-America reversion approach that the full map surgery will apply to
  the remaining ~10 independent Latin-American tags per the B-section mapping tables.

Still OWED before Phase-1 is "done": in-game boot test on `1763_bookmark` (the definitive
future-born-character + nested-subject proof). Nothing promoted off `1763_bookmark`.

*(Per-region implementation decisions B3, … appended as the full map-surgery phase begins.)*

---

## PART C — ECONOMY VALIDITY

### C1. Qing 1763 economy review (#199, DONE) — findings
Five seeded specialty industries are **100% historically valid** for 1763 (Qianlong era): 江南三織造
imperial silk (Suzhou/Jiangning/Hangzhou), 景德鎮 imperial kilns (porcelain zenith), Wuyi/Huangshan tea,
松江/Wuxi cotton belt, Lianghuai/Changlu/Sichuan salt monopoly. **No anachronisms.** But:
- **BLOCKING BUG (not date-related):** `QING_seed_building` guards require matching province `trade_goods`,
  yet `map_data/province_setup.csv` assigns all 11 target provinces `trade_goods = cloth` → the buildings
  **won't spawn**. FIX: reassign p:2588/6659/8120→silk, 7397→porcelain, 3317/4441→tea,
  366/455→textile_fibres, 3208/3783/3008→salt. *(Pre-existing; surfaces regardless of start year.)*
- **MISSING (high priority):** Yunnan copper (銅礦) — backbone of Qing cash-coin minting; reassign Yunnan
  provinces → `trade_goods = copper` (good already defined).
- **Optional:** seed 漕運 canal depots (Yangzhou/Tianjin) + 河工 Yellow-River dikes (buildings exist).

### C2. Rest-of-world economy (#201) — research landing
1763 economic geography per region (goods/cash-crops/manufactures/extraction + locations) mapped onto the
mod's goods/building vocabulary. Teammate econ files landed: `1763_econ_russia_baltic.md`,
`1763_econ_russia_furs_urals.md`, `1763_econ_sweden_mining.md`, `1763_econ_denmark_norway.md`,
`1763_econ_poland_lithuania.md` (+ the economy sections inside the `1763_WORLD_*.md` regional files).
These are date-invariant 1759↔1763 (grain, furs, Falun copper, Baltic naval stores don't move in 4yr).
*(Concrete province trade_goods / building edits C3+ appended as the edit phase begins.)*

---

## OPEN ITEMS / RISKS
- **Fresh adversarial review OWED** for the 1763 date-pivot edits (offset re-base arithmetic especially)
  AND for all forthcoming world map/ruler/economy edits, before any commit.
- **Oracle consult OWED** (Terra-Indomita + Invictus) before building mass `create_country` spawns for
  the missing PLC / Venice / Genoa tags — STANDING RULE, capability unproven at scale.
- Full-map surgery regression surface (subjects, de-jure, missions, events, wargoals keyed to 1815 tags)
  is minimal per #198 but must be re-checked per region.
- Some 1763 states may not be representable on the 1815 province map / tag list → documented limitation.
- Everything stays on `1763_bookmark`; promotion to develop/master only on the user's in-game
  verification + explicit request (branch policy).

## AGENT / TASK STATE (as of 2026-07-08)
- DONE: #198 feasibility scout, #199 Qing economy review, #203 date-flip+arc-rebase, #206 re-dispatch,
  branch rename, doc rename.
- RUNNING/IN: #200 world rulers research + #201 world economy research (regional agents + teammates);
  #207 Ottoman/MENA economy synthesis.
- PENDING: #202 update BOOKMARK_PROCESS.md; #204 finish rename tidy-ups; #205 Qing delta doc (done above);
  then map-surgery edit phase → adversarial review → commit as freekumquats.
