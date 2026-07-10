# Develop Merge Plan — porting the new 1763 mechanics back to `develop`

**Goal:** bring the NEW, branch-agnostic mechanics built on `1763_bookmark` into `develop`,
WITHOUT dragging in any 1763-specific content (the bookmark date, territorial/ruler surgery,
unborn-ruler sweeps, High-Qing era tuning). The classification already lives per-change in
`reverse_merge.md` (**[MECH]** = merge as-is, **[DATE]** = 1763-only, **[MIXED]** = hunk-by-hunk).
This doc is the *execution* plan on top of that ledger.

---

## 0. The branch topology (why this is a diff-port, not a cherry-pick)

- **merge-base:** `6a31f077` — the branches diverged here.
- **`develop` moved on AFTER the base** with the *predecessor* features this batch enhances:
  `#165` sphere, `#276` marriage-diplomacy STUB, `#268/#275` religion/missionary, `#272/#273`
  Grand Council expansion, `#279/#281` trade_goods+rifles (merged to develop as `38854b19`).
- **`1763_bookmark` moved on** with ~35 commits: a MIX of 1763-only world-surgery **and** the
  new reusable mechanics (the uncommitted working-tree batch + `#291`, `#303`).

**Consequence:** most new mechanics are ENHANCEMENTS to files that already exist on develop
(se_QING_FACTION, se_QING_MISSIONARY*, se_QING_COUNCIL, se_MARRIAGE, 00_marriage_triggers,
qing_faction_events, …), a few are NET-NEW files (se_QING_EARLYINDUS, se_QING_EMERITUS,
MARRIAGE_actions, MARRIAGE_svalues, marriage_window.gui). So we CANNOT `git merge 1763_bookmark`
(that would drag the whole bookmark). We port **content**, file-by-file, guided by the ledger.

---

## 1. What is IN scope (the [MECH] payload to port)

All currently **uncommitted** and tagged [MECH] in `reverse_merge.md`, grouped by feature:

### A. #304 core reusable systems (NET-NEW files — clean adds)
- `se_QING_EMERITUS.txt` + `qing_emeritus_events.txt` + `qing_emeritus_l_english.yml`
  + the Emeritus death-hook in `00_specific_from_code.txt` + the `qing_high_qing_prosperity`
  modifier DEF in `qing_mechanics_modifiers.txt` (a dormant def is inert on develop).
- `se_QING_EARLYINDUS.txt` (the Macartney EMBRACE early-industrialization track) + its
  `qing_embassy_events.txt` embrace-option hunks + loc.

### B. #308 Grand Council deepening (ENHANCE existing files)
- `se_QING_COUNCIL.txt`, `se_QING_FACTION.txt`, `qing_faction_events.txt`, `qing_office_events.txt`,
  `qing_governance_modifiers.txt` (tenure accrual), `government_view.gui` (17 faction squares +
  3-way ethnic readout), `gui_base.gui` (qing_faction_square + qing_favor_square_max),
  `textformatting.gui` (qing_conservative/qing_reformist codes), faction/governance loc.

### C. #309 missionary rework (ENHANCE existing files)
- `se_QING_MISSIONARY.txt`, `se_QING_MISSIONARY_STATIONS.txt`, `se_QING_DECLINE.txt`
  (the religious-tension→rebellion ignition; MIXED — see §2), `qing_missionary_events.txt`,
  `qing_missionary_modifiers.txt`, `qing_religion.gui`, missionary/religion loc.

### D. #311 dynastic-marriage FULL BUILD (MIX of new + enhance) — all [MECH]
- NEW: `MARRIAGE_actions.txt`, `MARRIAGE_svalues.txt`, `marriage_window.gui`,
  `marriage_modifiers.txt`, `marriage_l_english.yml`.
- ENHANCE: `se_MARRIAGE.txt`, `00_marriage_triggers.txt` (both already exist on develop as the
  `#276` stub — this is the full build ON TOP), `imp19c_opinions.txt` (betrothal/jilted opmods),
  `government_view.gui` (the "Royal Marriages" entry button).
- **Predecessor note:** develop's `#276` marriage stub is the base; the port must land the FULL
  build as a superset (CHI enabled, power-parity via DIPLOMACY_power, dowry/bridge/betroth/decay,
  L4 GUI). Diff-merge, not overwrite, if develop's stub has drifted.

### E. the one global define — colonization re-enable ([MECH], global)
- `common/defines/00_defines.txt`: `MINIMUM_COLONISATION_POP 99999 → 8`. Applies to develop too
  (both starts regain native colonisation alongside the migration engine). One-line change.

### F. already-COMMITTED 1763 commits carrying [MECH] hunks (port their MECH content only)
- `#291` (`1921f3b0`) ROW specialty production buildings + Yunnan copper — [MECH] per ledger.
- `#303` (`6d121dc9`) Am.Rev/Fr.Rev/Napoleonic as DATED events — **evaluate:** these are dated
  1776/1789/etc.; at the 1815 develop start those dates are in the PAST, so the events would be
  mid/expired. Likely **[DATE]-adjacent** → review before porting (may already be develop's job
  via a different mechanism). Flag for the user, don't blind-port.
- `bd5098dd` territorial batch — mostly [DATE]; ledger lists 3 [MECH] hunks — port ONLY those 3.

---

## 2. What is OUT of scope (do NOT merge)

- **The bookmark itself:** `START_DATE`, the 1759 peak-Qing bookmark, `-24` treasury, regnal 28,
  the 1763.2.17 legion guard, the `+19127` event-seed offsets — all in the committed 1763 commits
  (`8b33e4d7`, `6b3cf4d2`, `e5fc2af9`, `f73a6d16`). NEVER merge.
- **World surgery:** every `#232`–`#287`, `#278`, `#229`–`#240` commit (territorial reversions,
  HRE fragmentation, Vietnam split, Crimean Khanate, unborn-ruler sweeps, population rescale,
  industrialisation gradient). Pure 1763 [DATE].
- **[DATE] hunks inside [MIXED] files** — per `reverse_merge.md`, notably:
  - `se_QING_DECLINE.txt` — the **High-Qing era branch** in `QING_DECLINE_init` (`current_date <
    1772` → set `qing_high_qing_era`, prosperity, low-corruption seed) is [DATE]. It is *guarded*
    so INERT at 1815, hence technically merge-safe — BUT to keep develop clean we port only the
    [MECH] hunks of this file (the rebellion-ignition wiring) and LEAVE the era-seed branch, OR
    accept the inert guard. **Decision needed** (see §4).
  - `qing_embassy_events.txt` — the per-embassy occurrence-flag FIX is [MECH]; any 1763-dated
    scheduling is [DATE].
- **The absolute mission date-gates** (self-str ≥1860, taiping ≥1850, students ≥1872, techtransfer
  ≥1860): user chose to KEEP these on both starts (a deliberate, accepted behaviour change to the
  1815 start). So these DO port — but flag them explicitly in the merge commit as a known 1815
  behaviour change, not a silent one.

---

## 3. Execution mechanics (how to actually do it)

**Precondition:** the whole uncommitted batch is committed on `1763_bookmark` first (per the
current plan: one combined commit after both marriage reviews clear). Merging is easier from
named commits than a dirty tree.

**Recommended method — per-feature checkout-port on a develop-based branch:**
1. `git checkout develop && git pull` → branch `git checkout -b develop-mech-port`.
2. For **NET-NEW files** (§1.A, §1.D-new, §1.E is a 1-liner): `git checkout 1763_bookmark -- <path>`
   for each. These carry no 1763 coupling (verified: they self-gate on flags/eligibility, not date).
3. For **ENHANCED files** (§1.B, §1.C, §1.D-enhance): do NOT blind-checkout (that would clobber any
   develop-side drift). Instead `git diff 6a31f077 1763_bookmark -- <path>` to see the batch's
   changes, and apply them onto develop's current version — clean where develop hasn't touched the
   file since base, 3-way reconcile where it has. The files most likely to have develop-side drift:
   `se_MARRIAGE.txt` + `00_marriage_triggers.txt` (#276 stub), `government_view.gui`,
   `se_QING_COUNCIL.txt` (#272/#273 expansion). Diff those against develop FIRST.
4. For **[MIXED] files** (§2: se_QING_DECLINE, qing_embassy_events): apply ONLY the [MECH] hunks the
   ledger names; skip the [DATE] hunks (or keep them if the guard makes them inert — §4 decision).
5. **Boot-test on develop** (1815 start) — the whole point of the guards is that nothing new fires
   prematurely; confirm no load errors, the marriage button appears for CHI, the faction squares
   render, no missionary/rebellion misfire at 1815.
6. Adversarial review of the PORTED diff (a fresh workflow scoped to the develop-side result — the
   port itself can introduce reconcile bugs even though the source was reviewed).
7. PR `develop-mech-port → develop`, commit/push as **freekumquats** (standing rule).

**Alternative (heavier):** interactive rebase/cherry-pick of the eventual feature-commits — only
viable if the combined commit is SPLIT into per-feature commits first. Not recommended given the
batch is landing as one commit.

---

## 4. Open decisions for the user (before executing)

1. **se_QING_DECLINE High-Qing era-seed branch** — it is [DATE] but guarded-inert at 1815. Port it
   (harmless dormant code, keeps the two branches closer) or strip it from the develop port (cleaner
   develop, but the files then diverge and future merges get harder)?
2. **#303 dated wars** (Am/Fr/Napoleonic) — port to develop or leave 1763-only? (They're past-dated
   at 1815; likely leave.)
3. **Timing** — port immediately after the batch commits, or let the batch soak (boot-tested on the
   1763 branch) first, then port?

---

## 5. One-glance table

| Feature | Files | Kind | Merge? |
|---|---|---|---|
| Emeritus (#304) | se_QING_EMERITUS + events + loc + on_action hook | NEW | ✅ as-is |
| Early-Industry EMBRACE (#304) | se_QING_EARLYINDUS + embassy hunks + loc | NEW+enhance | ✅ as-is |
| Grand Council (#308) | se_QING_COUNCIL/FACTION + events + gui + loc | ENHANCE | ✅ diff-port |
| Missionary (#309) | se_QING_MISSIONARY* + decline(MECH hunks) + gui + loc | ENHANCE/MIXED | ✅ MECH hunks |
| Marriage (#311) | MARRIAGE_* (new) + se_MARRIAGE/triggers (enhance) + gui + loc | NEW+enhance | ✅ diff-port |
| Colonisation define | 00_defines.txt (1 line) | GLOBAL | ✅ as-is |
| ROW buildings (#291) | committed 1921f3b0 | [MECH] | ✅ port MECH |
| Bookmark + world surgery | ~30 commits | [DATE] | ❌ never |
| High-Qing era seed | se_QING_DECLINE branch | [DATE]-inert | ⚠️ §4 decision |
| Absolute mission date-gates | missions/*.txt | [MECH] (user-kept) | ✅ + flag 1815 change |
