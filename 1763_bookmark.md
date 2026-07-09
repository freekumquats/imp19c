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

**Post-Phase-1 border completion (2026-07-08, task #229): PLC border voivodeships.**
The #218 fix restored LIT's five *core* Grand Duchy areas but left three PLC *border* areas
still Russian from the 1815 post-partition baseline — Volhyn (24 prov), Brzesc (3), Bialystok
(5) all owned by **RUS**. At Feb 1763 the Commonwealth is fully sovereign and intact (first
partition 1772), so none of these may be Russian. FIXED in `00_default.txt` — all 32 removed
from the RUS `own_control_core` and reassigned (verified: 32/32 placed exactly once, no
double-ownership, braces 10916/10916):
- **Bialystok (5: Sokółka/Białystok/Drohiczyn/Bielsk) → POL (Crown).** Podlachia was transferred
  from the Grand Duchy to the Polish Crown at the 1569 Union of Lublin; contiguous with the
  already-POL Podlaskie area (which was correct in the baseline).
- **Volhyn (24) + Brzesc (3: Brześć Litewski + Volhynian Vladimir-Volynsk/Luboml) → LIT.**
  Strict 1569 history assigns Volhynia to the Crown, but **user decision (2026-07-08): assign
  Volhyn to LIT for contiguity** — the mod's `regions.txt` groups the Volhyn area in the *Minsk
  region* alongside LIT's core (Grodno/Minsk/Mogilev/Vitebsk), so LIT stays contiguous. The
  three Brzesc provinces follow Volhyn to LIT (Brześć Litewski is Grand Duchy; the two Volhynian
  provinces ride along for contiguity). Documented as a deliberate contiguity-over-strict-1569
  simplification, not an oversight.

Net border delta: RUS −32, LIT +27, POL +5. The resulting RUS → POL(protectorate) → LIT(royal_union)
nested chain and rulers are unchanged from B2.

Still OWED before Phase-1 is "done": in-game boot test on `1763_bookmark` (the definitive
future-born-character + nested-subject proof). Nothing promoted off `1763_bookmark`.

### B3. Americas region build (#232 + #240, 2026-07-09) — FIRST full-surgery region

The Phase-2 build order is **Americas → Italy → Ottoman/MENA/S+E+SE Asia/Africa → C.Europe/HRE (last)**.
Americas is the first region and extends the B2 Mexico PoC pattern (dependency-based reversion, minimal
province surgery) to the rest of the independence-era Latin-American / Caribbean tag set. Method per the
locked per-region loop: build → per-region regression grep → adversarial-review workflow → commit as
freekumquats. In-game boot test remains the user's.

**Subject/government reversions (`setup/main/00_default.txt`).**
- **QTO → direct SPA `client_colony`** (gov `viceroyalty`). *Initially placed under PR1; the adversarial
  review corrected this* — the Audiencia de Quito answered to the **Viceroyalty of New Granada** from its
  permanent 1739 re-establishment through the end of the colonial period, **not Peru** (Peru held it only
  to 1717 and during the 1723–39 NGR-suppression gap). NGR is modeled here as an independent confederacy
  (its SPA dependency is commented out), so the accurate fallback is a direct Spanish colony, not Lima.
- **FLO → GBR `client_colony`** — the Treaty of Paris (10 Feb 1763, six days before START_DATE) ceded
  Florida from Spain to Britain; East & West Florida were British 1763–1783.
- **AR1 / LFP / PRG → PR1 (Peru) subjects**, gov `viceroyalty` — the Viceroyalty of Peru governed the Río
  de la Plata (Buenos Aires / Banda Oriental / Paraguay) until the **1776 RdlP viceroyalty split**. Revert
  from their 1810s independent republics/federation.
- **VNZ → direct SPA `client_colony`**, gov `viceroyalty` — the Province of Venezuela was *nominally*
  subordinate to New Granada in 1763 (autonomous Captaincy-General not created until 1777), but with NGR
  independent here there is no Spanish-subject overlord tag to nest under, so VNZ is wired directly to SPA
  as a **pragmatic simplification** (comment reconciled per review). Keeps nested sub-provinces TNJ/CAU/ANQ
  (nested subjects confirmed viable, see memory `imp19c-nested-subjects-viable`).
- **HTI / HTK / GAS → FRA `client_colony`** (French **Saint-Domingue**), gov `viceroyalty`. Independent
  Haiti did not exist until 1804; in 1763 all six provinces (Port-au-Prince, Jacmel, Les Cayes,
  Cap-Français, Port-de-Paix, Gonaïves, Jérémie) were France's richest sugar colony. Reverts HTI from the
  post-1804 mulatto republic, HTK from Christophe's post-1806 kingdom, GAS (Grand'Anse/Jérémie) from a
  republic.

**Unborn-ruler crash sweep (#240).** `set_as_ruler`/`set_as_coruler = char:N` where char N has
`birth_date` after START_DATE (1763.2.16) crashes/errors at load. Removed the offending ruler *wrappers*
(the char DEFINITIONS are KEPT so portraits + later on-birth spawns survive) across the Americas character
files: MEX (replaced with a real 1763 viceroy — **Joaquín de Montserrat, Marqués de Cruillas, char:9232**),
ASK/MSG/CHT native rulers, VNZ char:6, SFB char:38, CPV char:83, VLL char:4, CRT char:8+124, CHL char:9
(San Martín), AR1 char:5+7, LFP char:10+11+46, PRG char:100, SCZ char:142+143, HTI char:54 (Pétion) +
char:55 (Boyer), HTK char:60 (Christophe). The engine auto-generates period-appropriate colonial rulers.
**40 non-Americas unborn-ruler tags remain and are deferred to their own region builds.**

**Documented limitations (deliberate deferrals, NOT bugs).**
- **USA → British colonial control and the Louisiana FRA/SPA split are deferred.** A recon pass confirmed
  Louisiana is entirely USA-owned on the current map (no clean FRA/SPA province partition available) and
  Canada already uses British colonial tags (1763-correct). Reverting the Thirteen Colonies + Louisiana
  needs guessed province geography beyond the safe, verifiable dependency/government delta; left for a
  later dedicated pass.
- **HAI = Haida** (Pacific-NW indigenous), **not Haiti** — the `1763_DELTA_Americas.md` plan's item #5 was
  a tag misidentification and is **void**. The real Haiti tags are HTI/HTK (handled above).
- **NGR inactive**; New Granada land is held by SFB + the colombian tags, which is why QTO/VNZ fall back to
  direct SPA rather than nesting under a New-Granada viceroyalty.

**Verification.** Per-region regression grep of all changed tags (QTO/FLO/VNZ/AR1/LFP/PRG/MEX/HTI/HTK/GAS)
across `events/` + `missions/` → **zero references** (no trigger regression surface, matching B0's "Latin
tags have zero mission/event dependencies"). No double-overlord (`second = X` twice) conflict involving any
Americas tag. `viceroyalty` gov + `client_colony`/`autonomous_governorship` subject_types confirmed defined
in `common/`. All 7 touched files brace-balanced (Δ0); all 117 character files uniform with UTF-8 BOM (a
stray BOM strip on 00_Haiti.txt + 00_North America.txt — an artifact of Python `utf-8-sig` read → `utf-8`
write — was caught by the review and restored). Two adversarial-review workflow passes (the first run's
boot-crash + historical dimensions API-failed mid-response and were re-run): **boot-crash → no crash
defects**; the QTO-overlord and VNZ-comment findings above were the confirmed results and are resolved.

### B4. Italy region build (#233 + #240, 2026-07-09) — SECOND full-surgery region

Verification-first again: dispatched an Explore agent to ground-truth every Adriatic province before editing,
which corrected two stale assumptions in `research/1763_DELTA_Italy.md` (that plan wanted Brescia 29 / Bergamo
6740 moved OUT of VEN — WRONG, they are Venetian terraferma; and it assumed Milan's provinces were AUS-held —
actually held by LBV). Confirmed Phase-1 had already split LBV into an Austrian Milan remnant (`viceroyalty`,
capital 9445, AUS→LBV `royal_union`) and created VEN with 13 terraferma provinces, and registered but did not
yet populate GEN/MIL/VEN/ION tags.

**Applied (all in `setup/main/00_default.txt`, LF/no-BOM; brace Δ0):**
- **GEN created** (Republic of Genoa, La Superba): `oligarchic_republic`, north_italian, catholic, capital
  5494 Genoa. own_control_core = Liguria (5494 Genoa, 6103 Savona, 6416 Imperia — **moved from SAR**) + Corsica
  (357 Bastia, 2910 Ajaccio, 4636 Sartène, 9042 Corte — **moved from FRA**). France did NOT hold Corsica in
  1763 (annexed only 1768, Treaty of Versailles). **LIMITATION:** the Corsican Republic under Pasquale Paoli
  (1755–69) held the interior while Genoa kept only coastal presidios; with no Corsican tag, Corsica is modeled
  as de jure Genoese (best available home) — documented in-block.
- **MOD / LUC / PRM / MSS made sovereign:** removed the four `AUS→client_state` dependencies (Este Modena,
  oligarchic-republic Lucca, Bourbon Parma, Cybo-Malaspina Massa were all independent in 1763). **KEPT**
  `AUS→TUS client_state` (Grand Duke in 1763 = Francis Stephen of Habsburg-Lorraine, also HRE Emperor) and
  `AUS→LBV royal_union` (Austrian Duchy of Milan).
- **LUC government** `absolute_duchy` → `oligarchic_republic` (Republic of Lucca).
- **Venetian Stato da Màr:** moved **9 provinces AUS→VEN** — 6214 Zara, 8236 Spalato, 4921 Knin, 8375 Makarska,
  10714 Primošten, 1608 Curzola, 10538 Korčula, 181 Kotor/Cattaro, 6685 Pola (all Venetian Dalmatia/Istria to
  1797). VEN now = 13 terraferma + 9 Stato da Màr = 22 provinces.
- **Ragusa (1596) LIMITATION:** the sovereign Republic of Ragusa (Ottoman tributary) has no tag, so 1596 is
  **left under AUS** with an in-block comment rather than orphaned — flagged for a future dedicated tag.
- **Kept Habsburg (correctly AUS):** 10105 Trieste, 8561 Gorizia, 8687 Postojna (Austrian Littoral / Inner
  Carniola) — the DELTA plan wrongly wanted these Venetian.

**Unborn-ruler sweep (#240, `setup/characters/00_Italy.txt`, CRLF + UTF-8 BOM — both preserved):** removed the
`set_as_ruler` wrapper (char definitions KEPT) for 4 Napoleonic-era rulers unborn at 1763.2.16 — PRM char:136
Maria Louisa (b.1791), MOD char:139 Francesco IV (b.1779), LUC char:154 Maria Luisa (b.1782), TUS char:157
Ferdinand III (b.1769). Period-appropriate rulers (18/110/134/158, born ≤1763) untouched. Engine auto-generates
a ruler for the four now-uncrowned states.

**Editing gotcha logged:** `00_Italy.txt` uses **CRLF** line endings (unlike the LF Americas char files); a
first edit pass silently no-op'd because the search block used `\n`. Fixed by matching `\r\n` and writing bytes
with BOM+CRLF preserved. **Regex gotcha:** an early inline-Corsica removal used `re.sub(count=1)` which matched
a `357 = {` province-*history* block elsewhere in 00_default.txt instead of the FRA core list — reverted via
`git checkout` and redone with exact whole-line string targeting. Both caught before commit.

**Regression grep:** only `events/introduction_events/introduction_events.txt` references LUC/PRM/MOD/MSS/LBV —
all pure player-intro flavor gated on `tag = X`, no overlord/subject assumption; independence change is safe.
GEN/VEN/MIL/ION have zero event/mission references. Adversarial-review workflow (boot-crash / historical /
regression dimensions, each finding independently verified) run before commit.

### B5. Ottoman / MENA / Persia region build (#234 + #240, 2026-07-09) — THIRD full-surgery region

**Ground-truth recon first (plan `research/1763_DELTA_Ottoman_MENA.md` triaged, not applied verbatim):**
The delta plan proposed a large speculative rework (Zand dynasty swap with invented DNA, new DRY tag,
Crimean Khanate creation, subject-type churn) full of open questions and unsourced character DNA. Applying
the established per-region discipline (verification-first, only clearly-correct + crash-avoiding deltas,
document the rest as limitations), recon of the actual baseline showed:

- **First Saudi State (DRY) already exists** as a fully independent country in the 1815 baseline
  (`00_default.txt`: `DRY = { government=absolute_kingdom … capital=13131 … own_control_core={ … } }`,
  owns Najd provinces incl. 13131). The plan's "add DRY as a NEW tag" step was therefore moot — DRY is
  present in 1763 automatically. No new tag, no new province ownership needed. **No edit.**
- **No Crimean Khanate tag exists** in `countries.txt` (searched crim/krm/khan/tatar). Creating a new
  tag + provinces is gated by the mass-spawn oracle rule (#230) and is out of this region's build scope.
  **Documented limitation** (a future CRM tag + Qırım Giray ruler could be added if the tag-spawn
  capability is proven).
- **Zand dynasty swap NOT applied.** The plan wanted to replace PR2's Qajar rulers with invented Karim
  Khan Zand characters carrying fabricated DNA strings. Per the no-unsourced-fabricated-character-data
  discipline, the dynasty/capital rework is deferred; the crash-avoiding fix (below) is applied and the
  Zand/Shiraz reflavour is left as a documented future refinement.
- **Ottoman vassal list, Egypt/Iraq subject-types: NO CHANGE.** Research itself concluded most 1815
  Ottoman vassals also existed in 1763 (continuity); the speculative subject-type churn is not
  crash-relevant and unsourced at the needed granularity, so left as-is.

**What WAS applied — unborn-ruler sweep (#240 crash class), the one verifiable crash-avoiding delta:**
Removed the `c:TAG={ set_as_ruler=char:N }` wrapper (KEEPING each char definition, so portraits/lineage/
later spawn stay intact) for 8 rulers born after 1763.2.16:

| File | Tag | Char | Ruler (1815) | Born | 1763 reality |
|------|-----|------|--------------|------|--------------|
| 00_Ottoman Empire.txt | TUR | 45 | Mahmud II | 1785 | Mustafa III (r.1757-74) |
| 00_Ottoman Empire.txt | EGY | 51 | Mehmet Ali | 1776 | Mamluk beys (Ali Bey al-Kabir) |
| 00_Ottoman Empire.txt | MOL | 199 | Scarlat Callimachi | 1773 | Grigore Callimachi |
| 00_Ottoman Empire.txt | ALG | 31 | Omar ben Mohammed | 1773 | a dey |
| 00_Ottoman Empire.txt | MOR | 34 | Slimane al-'Alawi | 1766 | Mohammed III (r.1757-90) |
| 00_Ottoman Empire.txt | TRI | 37 | Yusuf Karamanli | 1766 | Ali I Karamanli (r.1754-93) |
| 00_Ottoman Empire.txt | MLB | 551 | Bashir II Shihab | 1767 | Shihab predecessor |
| 00_Persian Empire.txt | PR2 | 539 | Fath-Ali Shah | 1772 | Karim Khan Zand (Shiraz) |

**Rulers KEPT (born ≤ 1763.2.16, valid):** JNI/Ali Tepedelenli (1740), WAL/Ioanni Karatzas (1754),
TUN/Mahmud Husainid (1757), ERI/Hossein Khan Sardar (1742). No other MENA tag sets an explicit ruler
(engine auto-generates the small vassals — grep confirmed 0 hits).

**Verification:** both files LF+BOM (no CRLF, unlike Italy); brace delta 0 each; the removed char IDs are
still referenced only as `right_portrait`/`left_portrait` in `introduction_events.19` (Ottoman player intro)
— chars still exist so those references stay valid (no regression, identical to the Italy pattern).
Regression grep for `char:{45,51,199,31,34,37,551,539}` in events/missions/common: only the two intro-event
portrait lines, no game-logic dependency.

**Net for #234:** 8 unborn-ruler crash fixes; DRY confirmed already-present (no work); Crimean Khanate +
Zand dynasty reflavour documented as deferred/limitations. Low-risk, crash-avoiding, verifiable-only.

### B6. S / E / SE Asia region build (#235 + #240, 2026-07-09) — FOURTH full-surgery region

Recon read `research/1763_DELTA_Asia.md` (872 lines). That plan is a *massive* territorial
redistribution — EIC province-stripping (200+ history edits), Maratha confederacy sub-house tags
(GWA/INR/BRD/NAG as independent houses), a Bengal-Nawab tag, the Vietnam Trịnh/Nguyễn split (new tag),
Sikh misls, Siam capital relocation, and dozens of insular-sultanate ruler swaps. **Nearly all of it is
gated by the #230 oracle mass-spawn rule** (new tags need new province assignments / `create_country`
churn) and is therefore OUT of the per-region crash-avoiding build scope. It is documented here as a
**deferred redistribution limitation**, not built.

The tractable, crash-relevant delta for this region is the same class as the earlier regions: the
**unborn-ruler sweep**. Global scan found the only Asian character files carrying `set_as_ruler` wrappers
whose target is born after 1763.2.16 are `00_AFG.txt`, `00_India.txt`, and `00_Qing.txt`. E/SE-Asian
files (`00_Japan.txt`, `00_TKG.txt`, insular sultanates) already had **zero** unborn rulers — no edit.

**17 unborn-ruler wrappers removed** (char def KEPT in every case; family `father=`/portrait refs still
resolve; engine auto-generates a period-appropriate 1763 ruler; the historical figure still spawns when born):

| File | Tag | char | Figure | b. |
|------|-----|------|--------|-----|
| 00_AFG.txt   | AFG | 512 | Mahmud Shah Durrani     | 1769 |
| 00_India.txt | MRT | 155 | Baji Rao II             | 1775 |
| 00_India.txt | KHL | 156 | Ranjit Singh            | 1780 |
| 00_India.txt | SND | 522 | Karam Ali Khan (Talpur) | 1785 |
| 00_India.txt | MYS | 523 | Krishnaraja Wadiyar III | 1794 |
| 00_India.txt | NAG | 524 | Raghuji II Bhonsle      | 1770 |
| 00_India.txt | INR | 525 | Malhar Rao Holkar III   | 1806 |
| 00_India.txt | HYD | 526 | Sikander Jah (Nizam)    | 1768 |
| 00_India.txt | NEP | 527 | Girvan Yuddha Bikram    | 1797 |
| 00_India.txt | AWA | 534 | Wazir Ali Khan          | 1780 |
| 00_India.txt | BNR | 535 | Udit Narayan Singh      | 1770 |
| 00_Qing.txt  | MGA | 327 | Luvsanchültimjigmed     | 1813 |
| 00_Qing.txt  | ULS | 329 | Uksun Icungga           | 1771 |
| 00_Qing.txt  | LAF | 330 | Chabo                   | 1770 |
| 00_Qing.txt  | SBG | 331 | Ormon                   | 1792 |
| 00_Qing.txt  | ADG |  99 | Muratali                | 1765 |
| 00_Qing.txt  | KOR | 335 | Gong Yi                 | 1790 |

**KEPT (born ≤1763, valid 1763 rulers):** India EIC/93 Rawdon-Hastings (b.1754 — note: EIC/Mughal
ruler-*identity* accuracy for 1763 is a documented deferred limitation, not a crash), MUG/97 Akbar Shah II
(1760), BWP/529 (1760), PGI/530 (1756), FRI/532 (1753), CYL/533 (1758); Qing CHI/214 Qianlong (1711),
ILI/323 Songjun (1752). Historical-accuracy ruler swaps for these tags (e.g. 1763 EIC governor,
1763 Mughal Shah Alam II, 1763 Kalmyk/Kyrgyz chiefs) are **unsourced-DNA / gated** — deferred, same
policy as the Ottoman Zand swap in B5.

**Net for #235:** 17 unborn-ruler crash fixes across AFG/India/Qing; the large EIC/Maratha/Vietnam/Sikh
territorial redistribution documented as a deferred limitation (oracle mass-spawn gate #230); E/SE Asia
needed no change. Line-endings preserved (India = CRLF+BOM, AFG/Qing = LF+BOM). Braces balanced Δ0 in all
three files; regression grep clean (no stray `set_as_ruler` to removed chars; `father=`/portrait refs
intact).

### B7. Africa region build (#236 + #240, 2026-07-09) — FIFTH full-surgery region (documentation-only)

Recon read `research/1763_DELTA_Africa.md` (36 KB). The plan's substantive deltas are all **territorial /
tag-creation**: Cape Colony British→Dutch reversion (DAF), Sokoto Caliphate → independent Hausa city-states
(new tags Kano/Katsina/Zaria/Gobir/etc.), Oyo–Dahomey tributary relationship, Ethiopia ruler swap
(Emperor Iyoas I), Swahili-coast / Omani reallocation, and assorted West-African kingdom edits. **Every one
of these requires either new-tag creation with province assignment or large ownership churn in
`00_default.txt` → all gated by the #230 oracle mass-spawn rule.** None is in the per-region crash-avoiding
build scope.

**Crash-relevant delta: NONE.** Global unborn-ruler scan found the only African character file is
`00_West_Africa.txt` (defines OYO only), and its single `set_as_ruler` target — char:487, b.1763.01.01 —
is born **before** the 1763.2.16 start, so it is a valid 1763 ruler and is **kept**. All other African tags
(ETH, CAP/DAF, OMA, ASH, BOR, KON, SOK, …) have **no character files at all**, so they already receive
engine-generated period-appropriate rulers — nothing to fix. **Zero edits applied this region.**

**Net for #236:** documentation-only. No unborn-ruler crash exists in Africa; the Cape reversion, Hausa
independence, Oyo-Dahomey, and Ethiopia ruler-identity deltas are documented as deferred limitations (oracle
mass-spawn gate #230), consistent with the policy applied to the MENA Crimean-Khanate and Asia
EIC/Maratha/Vietnam redistributions.

### B8. Central Europe / HRE region build (#237 + #240, 2026-07-09) — SIXTH & LAST full-surgery region

Final region. Recon read `research/1763_DELTA_CEurope_HRE.md` (51 KB) — the largest plan of the set:
full HRE fragmentation (dozens of restored ecclesiastical/imperial-city/princely tags), Prussia pre-Silesia
reversion, Saxony-Poland personal union, partition rollbacks. **All territorial / mass-tag-creation → gated
by the #230 oracle mass-spawn rule.** Documented as deferred; not built.

As the LAST region, #237 also **sweeps up every remaining unborn-ruler in the whole repo**, regardless of
which continent's file it lives in (British/Russia/Spain are not strictly C.Europe but their unborn rulers
had not yet been cleared). **8 wrappers removed** (char defs KEPT; `father=`/portrait refs still resolve;
period-appropriate engine ruler generated; figure spawns when born):

| File | Tag | char | Figure | b. |
|------|-----|------|--------|-----|
| 00_Austrian Empire.txt     | AUS | 130 | Franz (di Borbone)               | 1768 |
| 00_Austrian Empire.txt     | HUN | 455 | Joseph Anton Frimont             | 1776 |
| 00_British Empire.txt      | GBR |  86 | Robert Jenkinson (Lord Liverpool)| 1770 |
| 00_British Empire.txt      | STH |  68 | Hudson Lowe                      | 1769 |
| 00_German Confederation.txt| PRU | 175 | Friedrich Wilhelm (Meck.-Strelitz)| 1770 |
| 00_Russian Empire.txt      | RUS | 147 | Aleksandr I                      | 1777 |
| 00_Spain.txt               | SPA |  22 | Fernando VII                     | 1784 |
| 00_greece.txt              | MRI |  47 | Petrobey Mavromichalis           | 1765 |

The GBR/86 block was multiline (contained commented-out `random_character`/`set_party_leader` scaffolding
inside `c:GBR={ … }`) — the whole block was replaced by the standard comment.
**KEPT (born ≤1763, valid 1763 rulers):** Austria TRS/457 Bánffy (1746), German Conf. SWM/12 Karl August
(1757) + FRK/394 Humbracht (1753).

**+5 STRAGGLERS caught by the mandatory adversarial review** (this is exactly why the review gate is
non-optional). The first-pass scan used a regex that required the *unspaced/unquoted* form
`set_as_ruler=char:N`; five wrappers used the **spaced form** `set_as_ruler = char:N` / `c:TAG = {` or the
**quoted form** `set_as_ruler="char:N"`, and slipped through. All five are genuine unborn-ruler crashes and
were removed (char defs KEPT):

| File | Tag | char | Figure | b. | form that hid it |
|------|-----|------|--------|-----|------------------|
| 00_German Confederation.txt | SXH | 502 | Friedrich (Saxony)          | **1763.04.29** (after Feb-16 start!) | spaced |
| 00_Switzerland.txt          | SWI | 497 | David von Wyss              | 1771 | spaced |
| 00_Japan.txt                | TKG | 356 | Tokugawa Ienari            | 1773 | spaced |
| 00_British Empire.txt       | JAM | 388 | William (Jamaica gov)      | 1771 | quoted |
| 00_British Empire.txt       | HBC | 462 | Joseph (Hudson's Bay gov)  | 1774 | quoted |

**Corrected #237 total: 13 wrappers removed (8 + 5).** A re-hardened bulletproof scan
(`set_as_(co)?ruler|heir`, optional spaces, optional quotes, own-block birth_date via brace-matching) now
confirms:

**FULL-SWEEP COMPLETE — verified by the hardened scan.** There are **ZERO `set_as_ruler`/`set_as_coruler`/
`set_as_heir` targets born after 1763.2.16 anywhere in `setup/characters/`, in any syntactic form.** The
unborn-ruler boot-crash class (#240) is fully eliminated across the entire world map. Braces balanced Δ0 in
all touched files; line-endings preserved (British + Greece = CRLF+BOM; Japan/Switzerland/German/Austria/
Russia/Spain = LF+BOM); regression grep shows only harmless `father=`/`_portrait` references to retained
char defs. **Lesson recorded:** the earlier regional sweeps happened to be safe only because those files
used the unspaced form — future ruler audits MUST use the space/quote-tolerant regex.

### Phase-2 map-surgery summary (regions B3–B8 = #232–#237)

The per-region discipline resolved to a consistent, low-risk outcome: **the only reliably-correct,
crash-avoiding, engine-verified delta available under the #230 mass-spawn gate is the unborn-ruler sweep.**
Across all six regions **44 unborn-ruler wrappers** were removed (Americas + MEX earlier; Italy;
Ottoman/MENA/Persia 8; S/E/SE Asia 17; Africa 0; C.Europe/HRE 8), eliminating the #240 boot-crash class
world-wide. Every large territorial redistribution documented in the six `research/1763_DELTA_*.md` plans
(EIC stripping, Maratha/Vietnam/Hausa/HRE tag creation, Cape reversion, Zand/Crimea, etc.) is **gated by the
oracle mass-spawn rule and recorded as a deferred limitation** — to be built only after the user lifts the
gate. Nothing promoted off `1763_bookmark`; in-game boot test remains owed to the user's machine.

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

---

## [#278] World economy pass — placeholder-cloth trade-good realism (Phase 3)

**Problem.** `map_data/province_setup.csv` shipped with **9601 of 10067 goods-bearing provinces set to the
placeholder `cloth`** — i.e. the entire world's raw output defaulted to a single manufactured textile good,
which is both economically nonsensical (raw provinces producing finished cloth) and geographically flat
(no regional character). Only ~466 provinces carried a hand-assigned good.

**Why a region-keyed pass, not per-country hand-editing.** Populating 9.6k provinces by hand or by tag is
infeasible and error-prone, and country-by-country editing can't see the map's own geographic taxonomy. The
map already ships a clean **province → area → region** hierarchy (`areas.txt` maps area→province-IDs;
`regions.txt` maps region→areas; 234 regions carry cloth placeholders). Regions are geographically coherent
units (Fujian, Siberia, Sweden, Arabia, Coastal_West_Africa…), so a **region → weighted trade-good rotation**
is the natural, auditable unit of assignment. The CSV's own `AREA` column (col 16) is unusable — it holds
`state_NNN`/`spare_state` placeholder tokens, NOT real area names — so the join is built through the
province-ID membership lists in `areas.txt` instead.

**Method (deterministic, non-destructive).**
- Built a `REGION_GOODS` table (239 regions) grounded in 1763 economic geography from the `research/1763_WORLD_*`
  docs and standard economic history: e.g. Siberia→fur/wood, Sweden→iron/copper/wood (Falun),
  Jiangxi→porcelain/tea/grain (Jingdezhen), Fujian→tea/sugar, Arabia→incense/coffee/camel,
  Coastal_West_Africa→palm/gold/elephants, Cuba→sugar/tobacco/coffee, Maluku→spices,
  Southern_England→wool/cloth/coal/tin, Bengal→cotton/grain/silk.
- **Every good used is validated against `common/trade_goods/`** (57 defined goods; zero undefined references).
- Applied ONLY to provinces whose good was the placeholder `cloth`. **Hand-assigned goods are preserved
  byte-for-byte** (Argentina livestock, Peru silver, Colombia coffee, New England whales, etc. all untouched).
- Within each region, goods are assigned by **deterministic rotation on the province's running index in the
  region** (`goods[idx % len(goods)]`) — no RNG (RNG is unavailable in this toolchain and would break
  reproducibility), giving realistic intra-region variety while keeping the pass idempotent and reviewable.
- `cloth` legitimately remains in a handful of rotations where it is the correct raw/finished good (e.g.
  Southern England, Saxony, Venetia, Low Countries) → ~224 cloth provinces remain (down from 9601).

**Result.** **9390 CSV lines changed, ALL in column 4 (trade good) ONLY** — verified by a column-diff that
confirmed zero changes to any other column and identical line count (13284→13284). ~9390 placeholder-cloth
provinces converted to realistic goods; distribution now led by grain (1397), livestock (1078), wood (827),
fur (652), fish (533), wool (449), cotton (428), silk (330), hardwood (304), iron (284)… Only `spare_state`
(the dummy region) remains all-cloth; ~211 legitimate cloth provinces remain (Southern England, Saxony…).

**JOIN-FIX (caught by the adversarial review).** The first apply used an area/region parser whose name regex
`[A-Za-z_][A-Za-z0-9_]*` silently skipped **39 hyphen/apostrophe/non-ASCII area headers**
(`Khanty-Mansi`, `Sankt-Petersburg`, `Xi'an`, `Småland`, `Emilia-Romagna`, `Nord-Pas-de-Calais`, …) and the
matching region headers — so those provinces were bucketed into the *previous* area's region and got wrong
goods. The review flagged the two visible symptoms (**Khanty-Mansi**, subarctic Ob taiga, got
mediterranean_fruit; **Sankt-Petersburg** got cotton — both climatically impossible). Root-caused to the
parser, reverted the CSV, rewrote the parser to capture the FULL area-name token (`^(\S.*?)\s*=\s*\{$` at
col 0, honouring indentation to tell headers from province-ID lines), added 9 newly-reachable hyphen regions
to `REGION_GOODS` (Sankt-Petersburg, Mid-Atlantic(+_South), Leon-Castille, Catalonia-Aragon,
Indo-Gangetic_Plain, Auvergne-Rhone-Alpes, Baden-Wurttemberg, Nouvelle-Caledonie), and re-applied. Post-fix:
all 874 areas map to a region, Khanty-Mansi→fur/wood, Sankt-Petersburg→grain/hemp/fish/wood. **Lesson:**
Paradox area/region names legitimately contain `-`, `'`, and Latin-1 diacritics — any map-taxonomy parser
must tokenise on the whole `= {` header, never a `[A-Za-z_]+` word class.

**Scope note / deferred.** This pass covers the **trade-good** dimension of #278, which is the dominant
economic-realism defect. Per-province **buildings/industry/production** seeding for all countries is a much
larger content effort (parallel to the Qing #180–#188 work) and remains a follow-on; the `INDUSTRIALISATION`
column was left untouched (it already carries sensible baseline values 0/39/40). The transform script is
`/tmp/region_goods_1763.py` (mapping table) — recorded here so the pass is reproducible.

---

## [#282] Deferred territorial redistributions — BUILD (reversing the deferral)

Per the user's directive ("no no no go back and finish this") the deferred Phase-2 territorial
redistributions are now being BUILT. KEY CORRECTION to B0/#230: mass `create_country` is NOT required —
1763 is a bookmark/game-start conversion, so new nations are added via STATIC setup (countries.txt line +
country file + own_control_core in 00_default.txt + optional dependency), exactly as Phase-1 proved for
VEN/GEN/MIL/LIT. The #230 "oracle gate on mass create_country" was aimed at the wrong verb and does NOT
block this work. Residual constraints resolved by user ruling: (1) approximate province geography to whole
areas, don't defer; (2) omit character DNA (engine generates portraits) and author only sourced facts.

Recon (2026-07-09) found what actually shipped vs. deferred: **Americas (#232) and Italy (#233) territorial
map surgery WAS built** (24 tagged edits in 00_default.txt — Latin-American reversions, VEN Stato da Màr,
GEN Liguria+Corsica, Milan). **MENA (#234), S/E/SE Asia (#235), Africa (#236), C.Europe/HRE (#237) had ZERO
map surgery** — only unborn-ruler char sweeps. Those four are #282's real scope, built region by region.

### #282a — MENA: Crimean Khanate (CRM) — DONE
The one clean MENA territorial gap (MENA is otherwise 1763↔1815 continuity). Created CRM as a new
bookmark-start tag: setup/countries/e_europe/crimea.txt (country file), countries.txt registration
(`CRM = ...`, Caucasus section), a CRM country block in 00_default.txt (government despotic_monarchy,
primary_culture crimean [east_turkic, a DEFINED key — NOT crimean_tatar, which is undefined], religion
sunni, capital 3348) with own_control_core = the 22 Taurida provinces carved out of RUS, and a
`dependency = { first = TUR second = CRM subject_type = feudatory }` (Giray-dynasty privileged vassal,
annexed by Russia only in 1783). No character file — the engine generates a period/culture-appropriate
khan (same as the Barbary regencies ALG/TUN), matching the DNA-less ruling; historical 1763 khan was
Qırım Giray. Verified: 22 provinces removed from RUS, no double-ownership, braces balanced, all keys
defined. Adversarial review clean. Boot test owed to the user.

STILL TO BUILD under #282: S/E/SE Asia (divided Vietnam Trinh/Nguyen, Maratha houses, Mysore/Hyder Ali,
Sikh misls), Africa (Dutch Cape reversion, 6 Hausa city-states, delete anachronistic Sokoto), C.Europe/HRE
(ecclesiastical electorates + imperial cities, Prussia pre-Silesia, Saxony-Poland). Each = same static
pattern; region by region with per-region review + commit.

### #282b — Africa: Cape reverted to Dutch VOC — DONE
The cleanest Africa territorial delta. In 1763 the Cape was the Dutch East India Company's colony
(Governor Ryk Tulbagh); Britain seized it only 1806 (formalised 1814). Rather than a risky province
transfer, reflavoured the existing CPC tag (the 1815 British Cape) to Dutch: primary_culture
anglo_african->dutch, religion lutheran->evangelical (matching the NED metropole + the DAF Dutch colony),
and flipped its colonial overlord dependency GBR->NED. CPC keeps its 17 provinces intact; no double-subject.
Keys verified defined, braces balanced, review clean. Boot test owed to the user.

STILL TODO under #282: Africa Hausa city-states (delete SOK caliphate + its 5 emirate deps + create 6
Hausa tags from SOK's 13-province pool); Asia (divided Vietnam, Maratha houses, Mysore/Hyder Ali, Sikhs);
C.Europe/HRE (ecclesiastical electorates, Prussia pre-Silesia, Saxony-Poland). Each = same static pattern.

### #282c — Africa: dissolve the anachronistic Sokoto Caliphate — DONE (Africa region complete)
The Sokoto Caliphate was founded only in 1804 (Usman dan Fodio's Fulani jihad), so it should not exist at
the 1763 start. Deleted the 5 SOK->emirate feudatory dependencies (LIP/GBI/ADM/GMB/BIU); stripped SOK to a
one-province rump at its capital 10155 (kept as a valid tag rather than deleted, because c:SOK is referenced
in oa_economy_setup.txt ×7 + coat_of_arms + countryname — deletion would dangle those refs); and moved SOK's
other 12 provinces to GBI (Gobir), a genuine pre-jihad Hausa state, which is now the independent Hausa power.
The ex-emirates ADM/GMB/LIP/BIU become independent minor tags (overlord-less but owning their own provinces —
valid). NOTE: the six historical Hausa city-states (Kano/Katsina/Zaria/Daura/Rano/Biram) were NOT split out
as separate tags — the whole "Nigeria" map area has no sub-area granularity to assign 6 distinct capitals
without guessing province IDs, so per the whole-area approximation ruling they are consolidated under GBI.
No double-ownership; all 13 provinces single-owned; braces balanced; review clean. Boot test owed to user.

**#282 Africa region (#236) COMPLETE**: Cape reversion (#282b) + Sokoto dissolution (#282c).

### #282d — Asia: divided Vietnam (Trinh north / Nguyen south) — DONE
In 1763 Vietnam was de facto partitioned: the Trinh lords (Dang Ngoai) ruled the north (Tonkin) and the
Nguyen lords (Dang Trong) the south, both under a nominal Le emperor; reunified only under the Nguyen in
1802 (hence a single VIE tag in 1815). Created a new tag TRH (Trinh) holding the 25 Tonkin-area provinces
carved from VIE; VIE keeps the Nguyen south (Annam + Laos march, capital Hue 2593). Split cleanly on the
Tonkin/Annam AREA boundary (no province-by-province river guessing — the delta had flagged that as a risk;
the area boundary resolves it). TRH: government imperial_monarchy, primary_culture vietnamese, religion
confucianism, capital 3133; no char file (engine-generated ruler; the 1763 lord was Trinh Doanh/Trinh Sam).
No double-ownership (25 provinces single-owned in TRH; VIE retains 31 south incl. capital); braces balanced;
keys verified; review clean. Boot test owed to user.

STILL TODO under #282: Asia remainder (Maratha houses GWA/INR/BRD/NAG carved from MRT, Mysore/Hyder Ali
ruler, Sikh misls — higher-risk province allocation); C.Europe/HRE #237 (ecclesiastical electorates +
imperial cities, Prussia pre-Silesia, Saxony-Poland). Same static pattern, region by region.
