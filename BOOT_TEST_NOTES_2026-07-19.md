# Boot-test notes — 2026-07-19

Branch: 1763_bookmark. Test target: PERF-AUDIT merge (46353a75f / cb8e3aa6d).
Upstream ports (c87e8156b, 6e0c11604) NOT in scope for this test per user.

## CONFIRMED-CLEAN BASE (user boot tests)
- PERF-AUDIT merge (46353a75f) BOOTS clean.
- Upstream ports (c87e8156b + 6e0c11604) BOOT clean (user confirmed).
=> The next boot test is STRICTLY against this session's bugfixes (BT-A/B/D + any further).
   A crash on the next test is attributable to a bugfix, not to the merge/ports.

## HEADLINE RESULT
- **PERF-AUDIT merge BOOTS — no crash.** Crash question: PASS.
- Boot surfaced pre-existing FUNCTIONAL regressions (below). None are in files the
  perf merge touched; these are separate bugs the boot revealed.

## FIX PROGRESS (2026-07-19 pass 1)
- BT-B FIXED (commit 52900ff8c): Suppress Missions button wrapped in expanding margin_widget
  (was parentanchor=hcenter in a layout → "Widget cannot have a position in a layout").
- BT-D FIXED (commit 52900ff8c): Works Dikes/Depots/Granaries labels widened 200→284 so the
  counts align at x~308 with the Canal/Grain column; removed invalid `margin` on roster widget.
- BT-C INVESTIGATED, fix NOT applied — a cold agent proposed adding `employer=scope:player` to
  the cultivate/discipline is_shown, but that only HIDES buttons; it does NOT remove non-governor
  ROWS (the actual complaint). List builder already filters employer=CHI + is_governor + NOT
  qing_office_held. Real cause still unproven: list members that render with no title AND no
  buttons are failing is_governor at GUI-eval despite being in the stored list — likely stale
  membership or is_governor semantics differing in char-datacontext. NEEDS more proof before fix.
- BT-M INVESTIGATED, fix NOT applied — `order_by = age` is proven (13 uses, DESCENDING = eldest
  first). Youngest-first needs ASCENDING; no ascending flag exists, and negating via a script_value
  reading `age` is UNPROVEN syntax (age is never used as a value-body read anywhere in the repo).
  Need to verify age-in-svalue works, or find another ascending idiom, before applying.

## Functional bugs found (NOT yet investigated — list only)

### BT-A: Religion panel completely broken
- Symptom: religion panel shows NO vanilla gods, NO holy sites — nothing at all,
  just some "none" text floating.
- User note: the religion-touching fixes made PRIOR to the perf audit (pantheon
  redo 2998dc826 / revert 06cf2a5ad) evidently FAILED. The clean boot at 35c70c521
  only confirmed no-crash; the panel itself was never verified then.
- Status: OPEN, uninvestigated.

### BT-B: Suppress Missions button misaligned (#22)
- Symptom: the new "Suppress Missions" button is misaligned and off-center in the
  Mission Stations window.
- File (likely): gui/qing_province_reports.gui.
- Status: FIXED + USER-VERIFIED (commit 52900ff8c). Button wrapped in an expanding
  margin_widget. Confirmed correct on boot.

### BT-C: Governor Corps list includes non-governors (Ministry of Personnel)
- Symptom: the Governor Corps list under the Ministry of Personnel includes
  characters who are NOT governors — they lack the "Governor of XYZ" title and are
  missing the Cultivate / Discipline buttons.
- Status: OPEN, uninvestigated.

### BT-D: Ministry of Works — stat numbers left-aligned instead of right (misaligned column)
- Symptom: the Ministry of Works panel displays Yellow River Dikes, Grand Canal
  Depots, and Ever-Normal Granaries, but their NUMBERS sit too far to the LEFT;
  they should be on the RIGHT, aligned with all the other numbers.
- Status: FIXED + USER-VERIFIED (commit 52900ff8c). Dikes/Depots/Granaries labels
  widened 200->284 so counts align at x~308 with the other columns. Confirmed on boot.

### BT-E: Royal Marriage button misaligned on country diplomatic view (#12, REGRESSION)
- Symptom: the Royal Marriage button is badly misaligned on the country diplomatic
  view — floating freely between Relation Actions and Trade Actions instead of
  sitting under Alliance Actions where it belongs.
- Note: PREVIOUSLY attempted (#12, commit ~9743a2a7b) and FAILED — still wrong.
- Status: OPEN, uninvestigated.

### BT-F: Royal Marriage picker list unsorted (should be age-sorted, child/adult sections)
- Symptom: clicking the Royal Marriage button shows a single randomly-sorted list.
  It should display a list sorted by AGE, split into TWO sections: children and adults.
- Related to BT-E (same feature, #13 picker).
- Status: OPEN, uninvestigated.

### BT-G: Royal Marriage row-click dead-ends (#13, REGRESSION — fix failed again)
- Symptom: selecting a Royal Marriage by clicking a row does NOTHING — the window
  just disappears instead of showing a list of marriage candidates from the TARGET
  country.
- Note: SAME behavior reported before; the prior fix (#13) FAILED. Still broken.
- Related to BT-E / BT-F (same feature).
- Status: OPEN, uninvestigated.

### BT-H: Navajo present in western Canada (possible historical/geographic error)
- Symptom: a lot of Navajo in western Canada — user unsure if historically accurate
  (Navajo/Diné are a US Southwest people; western Canada would be geographically wrong).
- Likely related to the B2 54-province Native reassignment (#17, 07d9b19ae) — check
  which tag/culture (DIN = Diné/Navajo?) got assigned to western Canadian provinces.
- Status: OPEN, uninvestigated (needs historical verification, not just a code check).

### BT-I: Review ALL Native American tags for historical accuracy
- Task: audit every Native American tag for historical + geographic accuracy (correct
  people in correct region, plausible for the 1763 start).
- Known Native tags (setup/countries/n_america/, per countries.txt):
    APA = apacheria.txt        (Apache)
    DIN = dinetah.txt          (Diné / Navajo — see BT-H, appearing in W. Canada)
    NSQ = nisqually.txt        (Nisqually — Puget Sound)
    C3F = council_of_three_fires.txt (Council of Three Fires — Great Lakes)
    PMO = pomo.txt             (Pomo — N. California)
    NWE = newe.txt             (Newe / Western Shoshone — Great Basin)
    WNT = wintun.txt           (Wintun — N. California)
  Plus other resident Native tags from the B2 reassignment (#17) / #397.
- Scope: tag placement/capitals in setup/main/00_default.txt + culture assignments;
  cross-check against real 1763 tribal geography.
- Status: OPEN, uninvestigated (broad historical review — supersedes BT-H).

### BT-J: Substantial unowned/empty land in Africa — historical sweep + populate
- Symptom: large tracts of unowned/empty land in Africa at the 1763 start.
- Task: historical sweep of 1763 African polities; populate the empty provinces with
  the correct tags/cultures as needed (parallels the BT-I Native-tag sweep, and the
  earlier N. America ownerless-province work #17/#397).
- CAUTION: ownership edits touch setup/main/00_default.txt — the ownerless-capital
  crash class. Any new tag needs a self-owned capital; verify 0 ownerless capitals
  and 0 double-owned after.
- Status: OPEN, uninvestigated (broad historical review + populate; parallels BT-I).

### BT-K: New Guinea / Australia / New Zealand nearly deserted — populate with natives
- Symptom: New Guinea, Australia, and New Zealand are almost empty; expect Aboriginal
  Australian / Papuan / Māori populations + tags at the 1763 start.
- Task: historical sweep of 1763 Oceania/Sahul peoples; populate provinces with
  appropriate tags/cultures (parallels BT-I N. America + BT-J Africa sweeps).
- CAUTION: same ownerless-capital crash-class caution as BT-J — any new tag needs a
  self-owned capital; verify 0 ownerless capitals + 0 double-owned after.
- Status: OPEN, uninvestigated (broad historical review + populate).

### BT-L: Appoint Diplomat picker still shows harem members (#8, REGRESSION)
- Symptom: the Appoint Diplomat button still causes harem members to appear in the
  updated Diplomat Corps list.
- Note: PREVIOUSLY fixed (#8 — the harem-council leak, memory imp19c-8-harem-council-leak,
  fix = NOT has_variable qing_is_harem_consort in both builders). Regressed OR the fix
  did not cover the "updated Diplomat Corps list" path. Check both the appoint picker
  builder AND the corps-list builder for the harem-consort exclusion.
- Status: FIXED + USER-VERIFIED (commits 2e57cd07e + 62e451ba3). User clarified the sequence: appoint a
  VALID candidate, then the Diplomat Corps roster back-fills with HAREM WOMEN "replacing" diplomats.
  ROOT CAUSE: the corps AUTO-FILL. QING_subpost_staff_corps (se_QING_SUBPOSTS.txt:149) tops the
  diplomat corps up to target=4 via QING_subpost_fill_one, whose ordered_character picks by
  QING_subpost_eligible_candidate -> QING_office_eligible_candidate, which had NO harem-consort
  exclusion. So the auto-fill stamped qing_zongli_diplomat on the ablest "eligible" courtier — a
  consort qualified — and she showed in the corps. The #8 candidate-builder exclusions
  (se_QING_COUNCIL.txt:928/1011) never covered this auto-fill path.
  FIX (2 edits): (1) add NOT={has_variable=qing_is_harem_consort} to QING_office_eligible_candidate
  (qing_dynasty_triggers.txt) — the shared base gate, closing appoint picker + council autofill +
  corps auto-fill at once; (2) add consort to the QING_subpost_staff_corps release-sweep strip so a
  consort already holding a marker (pre-fix save) is stripped + the seat refilled (self-healing).

### BT-M: "Take a Court Woman as Consort" picker should be age-sorted (youngest first)
- Symptom: the candidate list in the Take-a-Consort picker is unsorted; it should be
  sorted by AGE, youngest first.
- File (likely): the harem take-consort picker builder (QING_harem_* refresh effect
  feeding qing_harem_candidates) + gui/imp19c_windows.gui qing_harem_take_window.
- Status: ABANDONED (user decision 2026-07-19). True youngest-first needs either an
  ordered_character order_by=age sorting iterator (the #443/#9 compile-inline boot-crash
  class in the scripted_gui Execute path — QING_harem_refresh already trampolines its
  ordered_character through qing_harem.3 for exactly this reason) or age-band multi-pass
  plumbing (as BT-F did). Not worth the churn for a cosmetic sort on this picker. WON'T FIX.

### BT-N: Minister of War & Commandant of the Guard have civil Presented Scholar trait (#5, NOT fixed)
- Symptom: the Minister of War and Commandant of the Guard STILL carry the civil
  "Presented Scholar" (進士/wu_jinshi civil) trait instead of a MILITARY exam trait
  (武舉/wu_ju military degree).
- Note: #5 (exam-trait congruence, ded69463e) + #48 (wuju military exam) were supposed
  to give martial offices the military degree. Still wrong for War + Guard offices.
- CAUTION: this touches the exam-trait grant path near QING_office_appoint — the same
  area as the wu_jinshi/health-trait-at-construction CRASH class (#5<->pos21). Any fix
  must keep the trait grant OFF the boot construction path (deferred to runtime).
- Status: OPEN, uninvestigated.

### BT-O: Military Presented Scholar trait icon broken (placeholder circle-triangle-square)
- Symptom: garrison commanders CORRECTLY have the Military Presented Scholar (武舉/wu_ju)
  trait — but its ICON is broken, showing the colored circle-triangle-square placeholder.
- Positive signal: confirms the military exam trait EXISTS and IS granted correctly to
  garrison commanders (so BT-N is specifically the War/Guard office-appoint path, not a
  missing trait). This is purely a missing/mis-referenced trait icon (.dds / gfx entry).
- Status: OPEN, uninvestigated.

### BT-P: Naval commanders lack the Military Presented Scholar trait
- Symptom: naval commanders do NOT have the Military Presented Scholar (武舉/wu_ju) trait,
  though garrison commanders do (BT-O). The grant path evidently covers land/garrison
  commanders but misses naval commanders.
- ROOT-CAUSED + FIXED (pending review/boot): TIMING. The martial grant lives in
  qing_force_setup.1 (day 30); the navies raise in qing_force_setup.11 (day 31). At day 30
  no admiral exists, so is_admiral matched nobody. FIX: added the guarded admiral grant to
  qing_force_setup.11 (after SE_qing_navy_* raise the fleets), same remove-civil-first idiom.

### EXAM-TRAIT CLUSTER FIXES (BT-N/O/P) — pending review/boot
- BT-O (military trait icon = placeholder): trait icons resolve by file convention
  gfx/interface/icons/traits/<key>.dds. Civil shengyuan/juren/gongshi/jinshi have .dds;
  hanlin/fanyi_jinshi + all four wu_* (added #48) had NONE -> placeholder. FIX: created the
  6 missing .dds from the rank-appropriate existing degree art (stopgap real art, not the
  engine placeholder; bespoke martial icons can replace later). wu_shengyuan<-shengyuan,
  wu_juren<-juren, wu_jinshi/wu_zhuangyuan/hanlin/fanyi_jinshi<-jinshi.
- BT-N (War/Guard show civil Presented Scholar): the day-30 grant did bare add_trait=wu_jinshi
  on a man already holding civil jinshi; relying on opposite-resolution to strip the civil
  trait was unreliable. FIX: remove_trait the held civil degree FIRST, then add_trait wu_jinshi
  (proven Invictus idiom for swapping mutually-exclusive status traits).
- All: brace-balanced, UTF-8 valid, 6 new .dds are real 56x56 DXT3.

### BT-Q: Vanilla succession/heir-favoring mechanics not cross-referenced with Qing succession
- Symptom/design gap: vanilla has succession mechanics where characters (governors,
  commanders, etc.) favor one heir or another. These operate independently of the
  Qing-specific succession mechanics that were added (e.g. the Princes / seal-succession
  system, qing_princes_*). The two should cross-reference each other so a character's
  vanilla heir-favoring aligns with / feeds the Qing succession system.
- Scope: integration/design work, not a bug — wire vanilla heir-preference into the
  Qing succession mechanics (and vice versa) rather than running two disconnected systems.
- Status: OPEN, uninvestigated (design integration task).

### BT-R: Investigate Military Supplies (upstream mechanic) — production/consumption chain
- Task: understand how the upstream Military Supplies mechanic works — how supplies are
  PRODUCED and CONSUMED. Hypothesis: produced in Arsenals (seems logical), but the
  Arsenal building tooltip says NOTHING about it — so either the tooltip is incomplete,
  or production happens elsewhere.
- Deliverable: trace the mechanic (which building/effect produces it, what consumes it,
  where the numbers live), then determine whether the Arsenal tooltip needs the info
  added or whether production is defined elsewhere.
- Status: OPEN, uninvestigated (investigation/understanding task).
