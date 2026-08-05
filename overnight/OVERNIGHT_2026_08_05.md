# OVERNIGHT 2026-08-05 — autonomous run

Branch: `merge-overnight`. Mandate: implement all open tasks autonomously, no deferring;
log every decision here; code-review adversarially BEFORE each commit.

Task board at start (pending): #32, #33, #34, #35, #36, #37, #39, plus new #40, #41.

---

## #40 — Verify all QING_seed_* province + trade-good mappings resolve on the 1763 map — DONE

**Why:** memory `imp19c-288-buildings-correction` flagged that `se_QING_BUILDINGS.txt`
seeds were authored against 1815-on-develop and their seed provinces + good-mappings
needed confirming on the 1763 map (post #284 pop/trade-good changes). A stale mapping =
a specialty building silently never seeds (all four seed macros fail silently+logged).

**Method:** wrote a Python cross-referencer. Extracted province→owner from every
`own_control_core` block in `setup/main/00_default.txt` and province→`trade_goods` from
all `setup/provinces/*.txt`, then checked each of the ~90 seed calls: province exists +
correct ownership (CHI-only for seed/works/port; CHI-or-subject for frontier) + (for
`QING_seed_building`) the required trade good G.

**Parser trap caught (verified against raw bytes, per AAA rule 7):** first pass reported
40 "problems" all clustering on tags MZH/SHG/YNG. Those are **commented-out** viceroyalty
blocks (`#MZH = { ... }`) whose *uncommented* province-ID lists fold directly into CHI's
`own_control_core`. My parser matched the dead `#TAG = {` headers. Re-ran with comment-
stripping → **3 real problems**, each then confirmed against raw setup:

1. **Foshan/Shiwan 石灣 kiln (P9301, `qing_porcelain_kiln_building`, G=porcelain)** — 1763
   models Foshan as `trade_goods="iron"` (its real Guangdong iron-casting industry; also a
   #63 holy site). G=porcelain guard silently failed → dead seed. No other Guangdong
   province is porcelain; the good is #234 pop-derived (not to be overridden). **Fix:**
   RETIRED the seed (Dehua 德化 Fujian + Jingdezhen 景德鎮 Jiangxi both resolve to porcelain
   correctly and remain the porcelain-kiln seeds).
2. **Turpan 吐魯番 karez (P9597, `qing_karez_building`)** — owned by ILI (the Xinjiang
   autonomous_governorship subject), not CHI directly → CHI-only `QING_seed_works_building`
   silently skipped. **Fix:** switched to the subject-tolerant `QING_seed_frontier_building`
   (building potential `is_in_region=Turkestan` already admits it).
3. **Kashgar 喀什 Id Kah Mosque (P2700, `qing_great_mosque_building`)** — owned by XNG,
   which is a subject of ILI, which is a subject of CHI (NESTED sub-subject). `is_subject_of`
   is NOT recursive (`imp19c-is-subject-of-not-recursive`), so even the frontier macro's
   `owner={is_subject_of=c:CHI}` branch failed. **Fix:** added a THIRD guard branch to
   `QING_seed_frontier_building` — `owner = { overlord = { is_subject_of = c:CHI } }` —
   admitting a province whose owner's DIRECT overlord is a CHI subject (XNG→ILI→CHI). This
   mirrors the single-level `overlord` branch the affected buildings already carry in their
   own `potential` (qing_great_mosque_building). One nesting level suffices for 1763.

**Post-fix:** re-ran the verifier with the corrected guard logic → **0 remaining problems**.
Braces balanced (212/212).

**Files:** `common/scripted_effects/se_QING_BUILDINGS.txt` only.

**Review:** code-review found ONE real defect (MEDIUM/HIGH): the new 3rd guard branch did an
`overlord = {}` scope-switch WITHOUT the `exists = overlord` guard — CHI itself hits this macro
(Liangzhou/Chahar/Xining) and has no overlord, which would re-trigger the 41,005-line overlord
flood that commit 7b88e9962 fixed mod-wide. FIXED: guarded with `exists = overlord` (matching
qing_great_mosque_building:257 and the 7-site convention). Re-verified 0 problems, braces 213/213.

**Status:** DONE — committed `6061c7f28`.

---

## #41 — Add ungranted modern-industry buildings as Self-Strengthening mission rewards — DONE

**Why:** three modern `qing_*` industrial buildings had NO `add_building_level` grant anywhere
(not seeded, not mission-granted) — reachable only via the invention-gated player build menu,
which may never open. User: add them as mission rewards; add new missions if necessary.

**Investigation (corrected the candidate list first, per the flag I raised):**
- Caught a false-grep: my initial "ungranted" scan matched only literal `add_building_level`,
  MISSING the `QING_selfstr_build = { building = X }` indirection. Re-ran catching all grant
  idioms. Results:
  - `qing_tongwen_guan_building` — **already granted** via `QING_selfstr_found_tongwen`
    (se_QING_SELFSTR.txt). EXCLUDED.
  - `qing_cotton_workshop_building` — a SEEDED specialty building (se_QING_BUILDINGS.txt:48).
    EXCLUDED (not modern-industry; user's original list conflated it).
  - `qing_n_poppy_farm_building` — buildable-from-start (poppy long cultivated), not gated.
    EXCLUDED.
- TRUE ungranted modern-industry set = **3**: `qing_steel_works_building` (漢陽鐵廠),
  `qing_coal_mine_building` (開平礦務局), `qing_textile_mill_building` (機器織布局).

**No new missions needed** — the Self-Strengthening tree ALREADY has three tasks named exactly
for these buildings (`qing_ss_hanyang`, `qing_ss_kaiping`, `qing_ss_cotton_mill`), but they only
granted `add_popularity` (+`add_stability` on cotton). They were stubs. Wired each to build its
eponymous building.

**Placement care:** steel/coal carry `base_resources = 2` (a MULTIPLIER on the province's
iron/coal output), so placing them on the most-populous province (what the existing
`QING_selfstr_build` helper does) would raise them where they yield nothing. None of the 3
buildings has a `potential` block, so `add_building_level` lands anywhere. Added a new helper
`QING_selfstr_build_on_good = { B = <building> GOOD = <good> }` (se_QING_SELFSTR.txt) that PREFERS
an owned province of the target good lacking the building (idempotent), and ONLY if none exists
falls back to the most-populous province — so the reward is never silently lost. Verified 1763
CHI owns iron provinces (5) and coal provinces (6). Each task also now calls
`QING_selfstr_advance = { amount = 8 }` (matching the other founding tasks, which all advance the
0..100 selfstr meter — the three stubs previously did not).

Wiring: hanyang→steel_works/iron, kaiping→coal_mine/coal, cotton_mill→textile_mill/textile_fibres.

**Files:** `common/scripted_effects/se_QING_SELFSTR.txt` (new helper),
`common/missions/qing_selfstrengthening_missions.txt` (3 task on_completions).

**Review:** code-review raised 3 findings.
- Finding #1 (MEDIUM, PLAUSIBLE): claimed the helper bets `add_building_level` bypasses the
  `allow` gate, contradicting memory `imp19c-add-building-level-respects-potential`, so the
  buildings would silently drop on rural resource provinces. **REFUTED after verification:** that
  memory VERIFIES `potential` is enforced, not `allow`; the review conflated the two — the exact
  error the memory itself flags a prior agent made. The 3 buildings have NO `potential` block. The
  decisive precedent: `qing_machine_works_building` has the IDENTICAL gate class (no potential;
  allow with has_city_status + civilization_value>=35 + sufficient_job_slots + industry-capacity +
  invention) and has shipped since #234 placed via add_building_level on capital_scope (reform
  mission) and most-populous (QING_selfstr_build) with ZERO gate replication. If `allow` were
  enforced on force-add, that flagship reward would silently fail — it doesn't. So the mechanism
  the comment describes is correct. No change.
- Finding #2 (LOW, design, ACCEPTED): good-targeting buys nothing for the textile mill (no
  base_resources, no trade-good gate) and could steer it to a smaller fibres settlement. FIXED:
  textile mill now uses plain `QING_selfstr_build` (most-populous, where the proletariat lives);
  good-targeting retained only for steel (iron) and coal (coal) where base_resources=2 bites.
- Finding #3 (LOW, convention, ACCEPTED): new LOG strings embedded `$B$`/`$GOOD$` macro params
  (log-string-macro rule). FIXED: both LOG_line strings made static.

Brace balance OK both files after fixes.

**Status:** DONE — committed (see git log).

---

## #39 — Protectors-General: Lifan Yuan roster section + event arc — IMPLEMENTED

Design doc `design/DESIGN_PROTECTORS_GENERAL_EVENTS.md` (READY, reviewed) implemented in the
build order it prescribed. The 都護府 marches = subject countries with qing_march=1; the GG is
the march's current_ruler (a Lifan appointee, set_as_ruler by QING_march_appoint_gg). Modelled
on the amban arc.

**PART A — roster (Lifan Yuan panel):**
- `se_QING_MINISTRY.txt` QING_ministry_recompute_perf_lifanyuan: rebuild
  `qing_lifanyuan_march_subjects` each Lifan pulse (every_subject over qing_march — non-recursive,
  same as the amban roster). Also added perf **term (h)**: fold `qing_lifan_recent_march_outcome`
  at HALF weight (divide by 2) — separate var from the amban term (g), no cross-contamination,
  no over-swing (review #4).
- `gui/qing_lifanyuan.gui`: new Protectors-General section between the amban roster and the
  tributary section. GG portrait via `Country.GetRuler` (proven datacontext — the GG IS the ruler,
  so no per-GG var, unlike the amban); PartyIcons chip suppressed (#86); empty-note.
- loc: `QING_LIFANYUAN_PG_TITLE` / `_EMPTY`.

**PART B — evaluate pulse + fold helper (se_QING_MARCH.txt):**
- `QING_march_evaluate`: called from QING_GOV_pulse right after QING_amban_evaluate. CHI player-only.
  Iterates marches, re-scores each GG's affinity (QING_char_affinity), rolls ~10% per quarter for
  AT MOST ONE mutually-exclusive event by priority (turnover .5 > overmighty .4 > unrest .2 >
  petition .1 > commend .3), sharing the court-event slot (qing_gc_event_slot_used).
  - SCOPE-LIFETIME care: the per-iteration scopes (qing_march_here/gg_here) would be overwritten
    by later iterations before a DEFERRED event (days 5-15) fires. Each fire branch re-saves
    DEDICATED event scopes (qing_march_evt_march/qing_march_evt_gg) at the moment of firing; only
    one branch fires per pulse (slot claim), and every event re-validates the scopes in its trigger.
  - Petition gate simplified to the subsidy-tier signal only (a var-vs-var cohort compare would
    break the RHS-operator rule; the invented svalue didn't exist).
- `QING_march_appoint_gg`: added a self-expiring tenure timer (qing_march_gg_tenure_pending, 2920d)
  mirroring the amban's, so the overmighty (.4) event can gate on "served long enough".
- `QING_march_recent_gg_outcome = { delta }`: clone of SUBJ_QING_lifan_amban_outcome; stamps the
  self-expiring 730d var (no ratchet).

**PART C — events (`events/imp19c_mod_events/qing_march_events.txt`, namespace qing_march) + loc:**
5 events (.1 petition, .2 unrest, .3 able, .4 overmighty, .5 turnover), each with a defensive
`trigger` re-validating the saved scopes (march still a subject + GG alive), CHI-only. Petition
grant has a light skill-gate (finesse>=6 → cheaper grant, a cost modifier not a roll); unrest .2.a
is a martial+zeal skill check (qing_garrison_clean_crush_chance_svalue from #27); .4/.5 reappoint via
QING_march_appoint_gg. Denials stamp a NEW stacking/decaying `qing_march_neglected_opinion`
(imp19c_opinions.txt) — the design's denial teeth (mod expresses subject disaffection via opinions,
not a raw liberty_desire poke, which is unused mod-wide). Every outcome folds via
QING_march_recent_gg_outcome. New loc file (UTF-8 BOM per loc convention).

**Self-check:** all touched files brace-balanced; pictures/verbs (add_gold/add_loyalty/
loyalty_qing_congenial/QING_char_promote_standing) all proven in the amban arc; Country.GetRuler
datacontext proven (the review's earlier "unproven" NO-GO was refuted in the design doc).

**Files:** se_QING_MINISTRY.txt, se_QING_MARCH.txt, se_QING_GOVERNANCE.txt, gui/qing_lifanyuan.gui,
localization/english/qing_lifanyuan_l_english.yml, common/opinions/imp19c_opinions.txt,
events/imp19c_mod_events/qing_march_events.txt (new), localization/english/qing_march_l_english.yml (new).

**Review:** code-review returned CLEAN — no crash/flood/correctness-critical defect. It confirmed
the scope-lifetime handling is sound (only one branch fires per pulse via the slot claim; scopes
survive the deferred event; cross-pulse clobber impossible), the slot serialisation is correct
(amban evaluate claims the same var first, so amban > march priority), the perf scratch var is
re-inited per term (no clobber), and all verbs/pictures/loc are legal. Four LOW findings, all fixed:
- #1 (LOW-MED): event triggers re-validated only scope existence, not the firing condition — a
  situation could drift in the 5-15d defer window (unrest subsided, affinity recovered). FIXED:
  .2/.3/.4 triggers now re-assert their scoring condition (parity with the amban arc).
- #2 (LOW): a displaced GG kept a stale qing_march_gg=1 (no tenure timer) after reappoint — could
  re-qualify for .4/.5 if succession re-elevated him. FIXED: QING_march_appoint_gg now clears the
  outgoing ruler's qing_march_gg + tenure var before set_as_ruler.
- #3 (LOW, balance): .1.b (troops) strictly dominated .1.a (silver) — same tier bump, cheaper, plus
  a host rebuild. FIXED: silver grant made cheaper (−20/−35) and troops pricier (−55), so silver is
  the lighter recurring commitment and troops the heavier all-in.
- #4 (LOW, doc): comment said the slot "resets monthly"; it clears each ~90d Qing pulse. FIXED wording.
The earlier design-round "Country.GetRuler unproven" NO-GO was re-confirmed refuted.

Brace balance OK all files after fixes.

**Status:** DONE — committed (see git log). Design doc committed alongside.
