# Develop Merge Plan 2 — porting the overnight Qing bureaucracy to `develop-mech-port`

**Author:** freekumquats · **Date:** 2026-07-11 · **Branch under plan:** `merge-overnight`
**Target:** `develop-mech-port` (→ eventually `develop`)

**Goal (verbatim user intent):** *"draw up a plan to merge them to develop and add it to the
`develop-mech-port` branch following the existing philosophy of merging non-1763-specific features …
the plan should cover all changes on the 1763 branch as well as the merge-overnight branch."*

This is the **successor** to `DEVELOP_MERGE_PLAN.md`, which covered only **batch 1** (the #304/#308/
#309/#311 Qing-deepening + dynastic-marriage build). Batch 1 has already landed on `develop-mech-port`
as a single commit (`8226982f0` — "Port 1763 reusable mechanics to develop"). This doc covers
**everything built since**: the full overnight bureaucracy (the 13 ministry panels, the 8 candidate
deep-sims, the deferred exam/tributary/canal follow-ons) **plus** the intervening 1763-branch mechanic
work that batch 1 did not carry.

The classification philosophy is unchanged from plan 1 and `reverse_merge.md`:
**[MECH]** = branch-agnostic mechanic, merge as-is · **[DATE]** = 1763-only world/date surgery, never
merge · **[MIXED]** = hunk-by-hunk. The good news, established by the survey below, is that the
overnight batch is **almost entirely [MECH]** — so this is a large but *low-risk* port.

---

## 0. Branch topology (the three layers)

```
develop  ──6a31f077(base)──► 38854b19 (trade_goods #279/#281 already on develop)
                │
                └─ 8226982f0  develop-mech-port  = develop + BATCH 1 (#304/#308/#309/#311)   ◄─ TARGET
                                                     (1 commit ahead of develop)

1763_bookmark ──(interim 1763 mechanic layer, see §1)──► fbd1c073 (fork point)
                                                            │
merge-overnight ──(64 commits, THIS batch, see §2)────────► 8bf466ee (HEAD)
```

- **merge-base(merge-overnight, develop-mech-port) = `6a31f077`** — the common ancestor.
- **merge-overnight forked from `1763_bookmark` at `fbd1c073`**, NOT from develop. So the 64 overnight
  commits sit on top of the *whole 1763 world* — but (crucially) they **touch none of it**.
- **develop-mech-port is 127 commits "behind" merge-overnight**, but that count is inflated by the
  entire 1763 world-surgery series that we will NEVER merge. The real payload is two layers:
  1. **Layer A — the 1763-interim mechanic commits** (§1): mechanic features built on 1763_bookmark
     *after* batch 1's source commit (`ee44b72a9`) but that batch 1 didn't carry — #312/#313 succession
     & marriage-family, #321/#322/#323 the exam/tributary/canal BASE systems, #324 heiress-claim,
     #330 marry-into-subject, #331 commander roster, #332 log-fix, #348 land-transfer fix, plus the
     #314/#329/#352 boot-test bug-fixes. **The overnight batch DEPENDS on these** (e.g. every ministry
     panel that reads the exam ladder needs #321; the tributary dashboard needs #322; the canal
     follow-on needs #323). They must port FIRST.
  2. **Layer B — the overnight batch itself** (§2): the 64 commits `fbd1c073..merge-overnight`.

---

## 1. Layer A — the 1763-interim mechanic layer (port FIRST)

These are the commits in `6a31f077..fbd1c073` that batch 1's port (`8226982f0`) did not include. Each is
classified below by whether it is a pure mechanic (port), pure world-surgery (skip), or mixed.

### A-MECH — port these (branch-agnostic mechanics the overnight batch builds on)

| Commit | Feature | Files (mechanic) | Notes |
|---|---|---|---|
| `6e0765a11` | #312 Female-line succession laws | se_QING_DYNASTY, succession triggers, gov_view, loc | self-gates on law choice, not date |
| `9d056fbd4` | #313 Marriage non-ruling families + filters | se_MARRIAGE, 00_marriage_triggers, marriage_window.gui, loc | superset of batch-1 marriage; **diff-port onto batch-1's version** |
| `e985e5e3d` | #321 Imperial Examination hire-pool (科舉) | se_QING_EXAM, qing_keju_events, exam modifiers/gui/loc | **BASE for #333/#353/#358 in Layer B** |
| `9ef99561e` | #322 Tributary System (朝貢體系) | se_QING_TRIBUTE, qing_tribute_events, tribute gui/loc | **BASE for #334/#350/#353** |
| `87f36b1bd` | #323 Grand Canal grain-logistics (漕運) | se_QING_CANAL, QING_works_pulse, qing_canal_events, loc | **BASE for #335/#351** |
| `959e502d7`+`463abae86` | #324 Heiress-claim coupling (+guard) | se_QING_DYNASTY/MARRIAGE claim wiring | needs #312 |
| `b224f2e05`+`80e073e56` | #330 Marry-into-subject + foreign-spouse council lobby | se_MARRIAGE, se_QING_COUNCIL, diplo, loc | `loyalty_to_overlord` subject-side tie |
| `fee34fbeb` | Bug 7: office modifiers into hover tooltips | government_view.gui, office loc | pure GUI |
| `6bd7f126b` | #315 Qing colonization arc Australia/PNG | qing colonization mission/events/loc | mission-tree, self-gated |
| `d57c2da0c`+`c7cc248d4` | #331 1763 commander roster + War-Minister feed | **[MIXED]** — see A-MIXED | roster is DATE, the War-Minister-competence *wiring* is MECH |

### A-MIXED — hunk-by-hunk

- **`#331` commander roster (`d57c2da0c` ws=1, `c7cc248d4` ws=0):** the *roster* (create_character +
  setup OOB attach for the historical 1763 commanders) is **[DATE]** — those are 1763 people attached
  to the 1763 bookmark's garrisons; at 1815 they'd be wrong/dead. **Skip the roster.** But `c7cc248d4`'s
  *mechanic* — "garrison commanders interact with the War Minister + feed council competence" — is the
  same coupling #346/#349 rely on and is **[MECH]**; port that wiring (it will simply act on whatever
  commanders the 1815 start has). Diff `c7cc248d4` and take only the se_QING_WAR/COUNCIL hunks, not the
  setup/roster hunks.
- **`#332` (`cdc7aaa70` ws=3):** "move non-Chinese polities out of 00_Qing.txt into region files" is a
  **setup reorganisation of the 1763 world** — but the underlying *bug* it fixes (the
  `culture=primary_culture` char-scope error flood) is engine-wide. **On develop the fix is already
  moot** if develop's 00_Qing.txt never had those polities; verify with a diff. If develop shows the
  same error pattern, port only the scripted-effect/char-scope fix, not the 1763 country relocations.

### A-DATE / A-BOOTTEST — do NOT port to develop (1763-only or already-on-develop)

- **All world-surgery** (`6b3cf4d27`, `#229`–`#240`, `#278`, `#282a-g`, `#283`, `#284`, `#286`, `#287`,
  `bd5098dd`, the bookmark commits) — pure 1763 [DATE], never merge (same rule as plan 1 §2).
- **The `#314`/`#329`/`dadbf3283`/`a9f3b6aa0` boot-test fixes** — these fix bugs *in the 1763 setup*
  (wrong start rulers from setup `death_date`, out-of-range setup char IDs, unit-placement at the 1763
  bookmark, Supranational window). **Most are 1763-setup-specific and do NOT apply to develop's 1815
  setup.** BUT three carry engine-general GUI fixes that develop wants regardless:
  - `2c967c9ac` **`multi_line`→`multiline` (17 sites)** — a real GUI bug fix, **[MECH]**, port it (throne
    boxes render). Check whether batch 1 already carried it (it post-dates `ee44b72a9`, so likely not).
  - `0f59bd7cc` / `0bb8336c4` / `bd2f66024` throne/picker/skill-cell layout fixes — **[MECH]** GUI, port
    if the target files (`government_view.gui`, marriage/throne GUIs) exist on develop and show the bug.
  - `0b1bc66f3` #314 B14 "Supranational window opens without a federation" — **[MECH]** (guard fix), port.
- **`#348` land-transfer fix (`0bb41…` on diplo_play_fix, merged via `6c0d1397`):** the
  `LAND_transfer_provinces` "Unknown trigger type: list" parse error is **engine-general [MECH]** — it
  breaks ALL land transfers on any branch. **Port this.** (It came in via a `diplo_play_fix` merge into
  1763_bookmark; on develop, cherry-pick the single se_ file fix, `0bb1f9228`.)
- **`#352` boot-test findings (`0c795e2fe`):** F1–F16 load/runtime fixes — **[MIXED]**; most are fixes to
  the overnight/1763 mechanic files themselves (so they ride along when Layer B ports), a few may be
  1763-setup-specific. Since Layer B ports the *current* state of these files (which already include the
  F1–F16 fixes), **this commit needs no separate action** — it's subsumed.

---

## 2. Layer B — the overnight batch (`fbd1c073..merge-overnight`, 64 commits)

**Survey result (the headline): this batch is essentially ALL [MECH].**
- **146 files, +21,084 / −804.** **99 net-new files, 45 modified.**
- **ZERO files** under `setup/`, `bookmarks/`, `history/`, `map_data/`, `province_setup.csv`,
  `00_countries` — i.e. **no world-surgery whatsoever.**
- **One** `qing_high_qing_era` reference in the whole diff, and it is a `NOT = { has_variable = … }`
  **guard** — inert at 1815 (the flag is only set at the 1763 start), so merge-safe by the same logic
  plan 1 applied to se_QING_DECLINE's era-seed.
- Everything is CHI-gated, flag/eligibility-gated, or pulse-driven — none of it is date-gated to 1763.

### 2.1 What's in the batch (by feature group)

**Net-new subsystems (clean adds — 99 new files):**
- **13 ministry panels** (#349–#365): War, Lifan Yuan, Works, Rites, Zongli Yamen, Revenue, Hanlin,
  Imperial Household, Central Secretariat, Censorate, Board of Punishments, Imperial Guard, Board of
  Personnel — each = a `se_QING_<X>.txt` + `gui/qing_<x>.gui` + `common/scripted_guis/…` + events + loc.
  All fold their performance into the Grand Council (the D3 rule).
- **2 study institutions** (#336 Southern Study 南書房, #337 Upper Study 上書房).
- **1 harem mechanic** (#360 後宮).
- **8 candidate deep-sims** (#366 silver/opium monetary, #367 Xinjiang consolidation, #368 court
  intrigue, #369 population/famine, #370 Silk Road caravan) + their DESIGN_*.md docs.
- **Frontier-garrison overlay** (#346/#347) — standing-army province effects + War/Lifan turf war.
- **Marriage-proposal diplomatic play** (#356) — replaces the Dynastic Match stub.
- **Zongli Yamen global play-success factor** (#357).

**Modified existing files (45 — diff-port, watch for develop-side drift):**
- The **base mechanic files** the follow-ons extend: `se_QING_EXAM`, `se_QING_TRIBUTE`, `se_QING_CANAL`
  (these only exist on develop-mech-port AFTER Layer A ports them — so **Layer A is a hard prerequisite**).
- `se_QING_COUNCIL.txt` — the generic ministry-perf fold sweep (the hub every panel wires into).
- `se_QING_DECLINE.txt` — the banner-decay/prosperity coupling several deep-sims nudge (the one inert
  `qing_high_qing_era` NOT-guard lives here).
- `government_view.gui` — the Edicts button strip (now carries all 13 ministry-panel open buttons +
  study/harem/Great Game/Reports buttons). **⚠️ HIGHEST-DRIFT FILE** — see §3 REG1 warning.
- `common/on_action/00_monthly_country.txt`, `qing_mechanics_on_actions.txt`, `00_specific_from_code.txt`
  — the pulse + death-hook wiring for the new subsystems.
- `common/loyalty/00_imp19c_loyalty.txt` — the #371 graduated loyalty-delta ladder (18 rungs).
- `common/opinions/imp19c_opinions.txt` — amban/marriage/tribute opinion modifiers.
- 10 `common/modifiers/*.txt`, ~10 events files, ~27 loc files.

### 2.2 The one thing to check per modified file: develop-side drift

Since Layer A + batch 1 will have brought most of these files onto develop-mech-port already, the batch-B
port is mostly clean **checkout-port**, EXCEPT the handful of files touched by BOTH batch 1/Layer A AND
the overnight batch. Diff those against the port target FIRST (3-way reconcile, never blind-checkout):
- `government_view.gui` (batch 1 added marriage button; Layer A added succession/office-tooltip; batch B
  added 13 ministry buttons — **all three must coexist**; this is exactly the REG1 class, §3).
- `se_QING_COUNCIL.txt` (batch 1 #308 expansion + batch B ministry-fold sweep).
- `se_MARRIAGE.txt` / `00_marriage_triggers.txt` (batch 1 stub-superset + Layer A #313 filters + batch B
  #356 marriage-play).
- `se_QING_DECLINE.txt` (batch 1 #309 rebellion-ignition + batch B deep-sim nudges).
- `imp19c_opinions.txt` (batch 1 betrothal opmods + Layer A #330 + batch B amban/tribute).

---

## 3. Execution plan

**Precondition:** merge-overnight is fully committed (✅ — HEAD `8bf466ee`, working tree clean after the
#334/#335/#370-R commits) and both post-build adversarial reviews have cleared (in flight —
`wf_062c9da0` #334, `wf_18966771` #335; fold any confirmed fixes in before porting).

**Method — extend `develop-mech-port` in two ordered sub-ports (mirrors plan 1 §3):**

**Step 1 — Layer A onto develop-mech-port.**
1. `git checkout develop-mech-port` (it already = develop + batch 1).
2. For each **A-MECH net-new** feature (#312/#313/#321/#322/#323/#324/#330/#315): `git checkout
   1763_bookmark -- <mechanic files>` (they're self-gated, no 1763 coupling). For #313/#330 which touch
   files batch 1 already ported (se_MARRIAGE, marriage GUI, opinions), **diff-port** onto batch 1's
   version, don't clobber.
3. For **A-MIXED** (#331 War-Minister wiring, #332 char-scope fix): apply ONLY the mechanic hunks named
   in §1; skip the roster/setup hunks.
4. Port the **engine-general GUI/parse fixes**: `2c967c9ac` multiline, the throne/picker layout fixes,
   `0b1bc66f3` Supranational guard, and the `#348` `0bb1f9228` land-transfer parse fix.
5. Commit as **freekumquats**: `"Port 1763-interim mechanics to develop-mech-port (#312/#313/#321/#322/
   #323/#324/#330/#315/#331-wiring/#348 + GUI fixes)"`.

**Step 2 — Layer B (the overnight batch) onto develop-mech-port.**
6. For the **99 net-new files**: `git checkout merge-overnight -- <path>` in bulk (they carry no 1763
   coupling — verified §2). A scripted list is safest: derive it from
   `git diff --name-status 1763_bookmark...merge-overnight | grep '^A'`.
7. For the **45 modified files**: bulk-checkout the LOW-drift ones (loc, modifiers, new events, the
   base-mechanic files just introduced in Step 1); **3-way reconcile the 5 high-drift files in §2.2**
   (government_view.gui first — verify ALL button groups coexist, the REG1 lesson).
8. Strip the batch's own scaffolding docs from the port if desired (`overnight_*.md`, `DESIGN_*.md`,
   `RESEARCH_*.md` are process artifacts, not shipping content — optional to include; they're harmless).
9. Commit as **freekumquats**: `"Port overnight Qing bureaucracy to develop-mech-port (13 ministry
   panels + 8 deep-sims + study/harem + follow-ons; all [MECH], no world-surgery)"`.

**Step 3 — validate + review.**
10. **Boot-test on develop-mech-port at the 1815 start.** The whole safety argument is that everything
    self-gates: confirm NO load errors, the 13 ministry buttons render + open for CHI, no ministry
    misfire, no `qing_high_qing_era`-dependent path fires (it can't — the flag is unset at 1815). Read
    debug.log for any `se_LOG` anomalies.
11. **Adversarial review of the PORTED diff** (fresh workflow scoped to the develop-mech-port result) —
    the port itself can introduce reconcile bugs even though every source commit was already reviewed.
    Highest scrutiny on the 5 high-drift reconciled files.
12. PR `develop-mech-port → develop` once boot-tested and reviewed, per branch policy (develop = pushed
    testing candidate; promote to master only after user in-game verification). Commit/push as
    **freekumquats**.

---

## 4. Risk register + open decisions for the user

**Low-risk (established by survey):**
- No world-surgery in Layer B → no accidental 1763-territory bleed into develop.
- Everything CHI/flag/pulse-gated → nothing fires prematurely at 1815.

**The real risks (all in the reconcile, not the content):**
1. **`government_view.gui` button-strip regression (REG1 class).** This file was clobbered ONCE already
   during the overnight build (#356 dropped the whole strip; caught + restored). The port must land ALL
   button groups — batch 1's marriage button, Layer A's succession/office tooltips, and batch B's 13
   ministry + study/harem/Great Game/Reports buttons — coexisting. **Diff, don't checkout. Grep the final
   file for every expected `_open_panel_button` / edict button before committing.**
2. **Base-mechanic ordering.** Layer B's modified `se_QING_EXAM/TRIBUTE/CANAL` are the *follow-on* state
   of files Layer A introduces. If Step 2 checks these out from merge-overnight, it gets the final
   (follow-on-inclusive) version — which is correct and *supersedes* Layer A's base version. So **Step 2's
   checkout of these three files is authoritative; Step 1 need not port their base separately** (Step 1
   ports them only so the intervening #333/#334/#335 follow-on commits have a coherent base if you choose
   to split more granularly). Simplest: in Step 1 skip #321/#322/#323's se_ files and let Step 2's
   checkout bring the final version; Step 1 then only needs their *events/modifiers/gui/loc* that Layer B
   doesn't also touch. **Verify no base-file is left un-ported.**

**Open decisions for the user (before executing):**
1. **Squash vs. two commits vs. per-feature?** Recommendation: **two commits** (Layer A, Layer B) —
   matches plan 1's single-commit precedent, keeps the port reviewable, avoids re-litigating 64 messages.
   Per-feature is only worth it if you want to bisect later.
2. **Include the process docs** (`overnight_*.md`, `DESIGN_*.md`, `RESEARCH_*.md`) in the develop port?
   They're harmless flavour/rationale but clutter develop. Recommendation: **include the DESIGN/RESEARCH
   docs** (they document shipping mechanics) **but leave `overnight_decisions*.md` / `overnight_design*.md`
   on the build branches** (pure process log).
3. **`#303` dated wars (Am/Fr/Napoleonic)** — flagged in plan 1 §4.2 as past-dated at 1815, likely leave
   1763-only. Still open; unaffected by this batch. Recommendation: **leave 1763-only** unless develop
   wants them as historical flavour (they'd fire immediately/expired at 1815).
4. **`#332` non-Chinese-polity relocation** — port the char-scope error fix only, or is develop already
   clean? **Needs a develop-side diff to decide** (§1 A-MIXED).

---

## 5. One-glance table

| Layer | What | Kind | Action |
|---|---|---|---|
| A | #312 succession laws | [MECH] | ✅ checkout-port |
| A | #313 marriage families/filters | [MECH] enhance | ✅ diff-port onto batch-1 |
| A | #321/#322/#323 exam/tributary/canal BASE | [MECH] | ✅ (or defer to Layer B's final version — §4.2) |
| A | #324 heiress-claim, #330 marry-into-subject, #315 colonisation | [MECH] | ✅ checkout-port |
| A | #331 War-Minister competence wiring | [MECH] hunks | ✅ port wiring, skip roster |
| A | #331 commander roster, all world-surgery, #314/#329 setup boot-fixes | [DATE] | ❌ never |
| A | multiline fix / throne-picker layout / Supranational guard / #348 land-transfer parse | [MECH] | ✅ port |
| A | #332 polity relocation | [MIXED] | ⚠️ char-scope fix only, §4.4 |
| B | 13 ministry panels (#349–#365) | [MECH] NEW | ✅ checkout-port (99 new files) |
| B | 8 deep-sims (#366–#370), study×2, harem, follow-ons (#333/#334/#335) | [MECH] NEW/enhance | ✅ checkout-port |
| B | #346/#347 frontier garrison, #356 marriage-play, #357 Zongli factor | [MECH] | ✅ port |
| B | government_view.gui, se_QING_COUNCIL, se_MARRIAGE, se_QING_DECLINE, imp19c_opinions | [MECH] high-drift | ⚠️ 3-way reconcile, §2.2 + §4.1 |
| B | qing_high_qing_era NOT-guard (1 site, se_QING_DECLINE) | [DATE]-inert | ✅ harmless, keep |
| — | overnight_*.md / overnight_design*.md | process log | ⬜ leave on build branch (§4.2) |
