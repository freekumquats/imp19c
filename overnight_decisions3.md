# Overnight Decisions 3 — 2026-07-10/11

Branch: **overnight-312-315-audits** (off `1763_bookmark`). Autonomous run.

## Mandate (from user)
1. New branch (done: `overnight-312-315-audits`).
2. Implement tasks **#312, #313, #315** (#314 boot-test fixes are already code-complete on 1763_bookmark; only in-game verification remains — NOT re-done here).
3. Then implement **the overnight-build-candidate findings** = the Top-3 in `research/1763_OVERNIGHT_TOP3_DECOMP.md` (user confirmed "one of them was tributaries"):
   - **#1 Full Imperial Examination System (科舉)** — ~20h decomposition.
   - **#2 Full Tributary System (朝貢體系)** — ~18h decomposition.
   - **#3 Grand Canal Grain-Tribute Logistics (漕運)** — ~16h decomposition.
4. **Deep adversarial review (Workflow) after EACH task completes**; fix confirmed findings before moving on, THEN commit.
5. Log all major decisions here; **explicitly call out deferred pieces**.
6. Work continuously without stopping to ask, until all tasks complete.

## Corrected interpretation (2026-07-10)
- Initial reading mis-identified the "findings" as the AUDIT_* docs. User corrected: the target is the **~20h overnight build candidates** (Exam / Tributary / Grand Canal), decomposed in `research/1763_OVERNIGHT_TOP3_DECOMP.md` + `research/1763_OVERNIGHT_BUILD_CANDIDATES.md`.
- **DEFERRED (explicitly, not built this run):**
  - The AUDIT_* dashboard-suite (invisible-mechanics dashboards) and the B27 dead-code fix (`TRADE_update_all_TZ_local_prices`) — these are the OTHER audit stream, not the build candidates. Left for a later pass.
  - Build candidates 4-8 in `1763_OVERNIGHT_BUILD_CANDIDATES.md` (Silver/Opium monetary model, Xinjiang consolidation arc, Court-Intrigue sim, Population/Famine model, Silk-Road caravans) — only the Top-3 are in scope.
- **Execution reality note:** the Top-3 decompositions describe ~54h of parallel-agent work each with a research→design→engine→events→GUI→review pipeline. I am executing them SEQUENTIALLY (312/313/315 first, then Exam, then Tributary, then Grand Canal), scoping each to a correct, boot-safe, reviewed vertical slice rather than the full multi-agent fan-out. Where a decomposition sub-piece is dropped or reduced to fit, it is logged as DEFERRED in that task's entry below.

## Standing rules honoured
- Commit/push as **freekumquats** (repo-local identity already set).
- Byte conventions: script_values BOM/LF; scripted_effects no-BOM/LF; loc .yml BOM single-space-indent; modifiers no-BOM.
- Every feature wired to se_LOG; every fix gets a task-tagged comment.
- Consult Invictus + Terra-Indomita oracles for any UNPROVEN engine idiom before building on it.
- Concrete over abstract; additive conversion of existing counters.

## Interpretation decisions (made autonomously; flagged for review)
- **"overnight decision agent findings"** was ambiguous (candidate docs: `overnight_decisions2.md`, `research/1763_OVERNIGHT_BUILD_CANDIDATES.md`, `research/AUDIT_*.md`). CHOSE the **AUDIT_* findings** because (a) they are the most recent (2026-07-10) audit outputs, (b) they contain concrete, scoped, actionable items (the dashboard suite + the B27 dead-code defect) rather than open-ended new-feature candidates, and (c) the 1763_OVERNIGHT_BUILD_CANDIDATES are large NEW deep-sim features that read as a menu to pick from, not "findings to implement". If this is the wrong doc, the build candidates remain untouched and available.
  - **DEFERRED (not built this run):** all of `research/1763_OVERNIGHT_BUILD_CANDIDATES.md` (Examination System, Tributary System, Grand Canal logistics, Silver/Opium model, Xinjiang arc, Court Intrigue sim, Population/Famine model, Silk Road caravans). These are separate overnight-scale features, not "findings".

---

## Task log
(entries appended as each task + its review complete)

### #315 — Qing colonization arc: Australia + New Guinea (CODE-COMPLETE, review running)
- Added two tasks to the EXISTING `qing_colonization_mission` tree (common/missions/qing_colonization_missions.txt): `qing_col_new_holland` (requires pacific_isles; claims Sydney 633 / Melbourne 2107 / Adelaide 6001 / Perth 2441; GBR frontier-play on Sydney; frontier-pull; provoke_britain; grants qing_col_new_holland_settled) → `qing_col_new_guinea` (claims Wau 50 / Sarawaget 318 / Barapasi 1076 / Hobart 5734; grants qing_col_south_seas_dominion). Added new_guinea as 4th capstone prereq + south_seas_dominion to the capstone OR-gate.
- 2 new modifiers (qing_colonization_modifiers.txt), loc (qing_colonization_l_english.yml). All 8 province IDs confirmed in definition.csv. Reused the proven idiom exactly (add_claim guarded, QING_COLON_frontier_pull, QING_gp_provoke_britain, CURRENCY_grant_country_wealth). Gated on qing_selfstr OR qing_high_qing_era like the rest of the tree.
- **DECISION:** hung the branch off the maritime `pacific_isles` node (not a new root) so it inherits the fleet/era gate and feeds the existing Pacific-Dominion capstone — one coherent tree, not a parallel one.
- **DEFERRED:** no new units/colonists are spawned (concrete-over-abstract: add_claim + migration-pull only, matching sibling branches); a dedicated southern-fleet unit spawn was NOT added.
- **ADVERSARIAL REVIEW (15-agent workflow, 9 confirmed / 12 raised) — ALL FIXED:**
  - **CRITICAL:** `p:633` was Sydney, **Nova Scotia (Canada)** — NOT Sydney, Australia (`p:895`). The flagship claim + GBR frontier-play + migration-pull all targeted the wrong continent (and collided with the tree's own Canada branch). Fixed all uses 633→895 + header note.
  - **MAJOR:** the southern branch was UNREACHABLE at a 1763 start — its prerequisite `qing_col_pacific_isles` gated only on the 19th-c. fleet modifiers, no High-Qing escape. Added `has_variable = qing_high_qing_era` to pacific_isles' allow (matching the ROOT bureau gate), so the whole maritime chain is reachable at the bookmark start it was written for. Develop/1815 unchanged (era flag never set).
  - NITS fixed: header comment listed 2 provinces never claimed (Brisbane 4528 / Banabufi 1409); "Cook charted New Holland 1770" overstated (east coast only; Dutch mapped the rest); New Holland/新南威爾士 term mismatch → 新荷蘭; 南洋 → 大洋洲領地 for the modifier.
  - KEPT (nit, intentional): capstone lists both pacific_isles + new_guinea (redundant logically, but draws the UI prerequisite arrow). Refuted (not-a-bug): the 4th capstone prereq does not regress develop; GBR frontier-play resolves against GBR-subject-owned provinces via #58.

### #312 — Female-line succession laws (CODE-COMPLETE, review pending)
- **KEY ENGINE FINDING (oracle):** the ONLY runtime succession change is `change_law = <succession_law>`; there is NO set_succession / designate_heir effect. The engine has 3 hardcoded female-penalty tiers (agnatic / cognatic / egyptian) selected by the law's `succession = <type>` field. TRUE absolute-cognatic (zero female penalty) is NOT per-country scriptable — only a global defines change (COGNATIC_FEMALE_PENALTY) would do it, which affects all cognatic realms.
- **KEY MOD FINDING:** the mod's law rework REMOVED the vanilla `succession_law` group entirely — it did not exist. So I re-added it (common/laws/00_succession_laws.txt) with agnatic + cognatic tiers, potential is_monarchy=yes.
- Built: `SUCCESSION_set_agnatic / _agnatic_cognatic / _absolute_cognatic` effects (se_SUCCESSION.txt) wrapping change_law + legitimacy cost + the Pragmatic-Sanction contest (SUCCESSION_pragmatic_contest: rival great-power NEIGHBOURS with opinion<25 contest a female-permitting change → pragmatic_sanction_contested modifier + opinion_disputed_succession). 3 reform buttons + 3 read-only indicators (SUCCESSION_actions.txt), wired into the Grand Council Edicts strip. Modifiers (qing_succession_modifiers.txt), opinion (imp19c_opinions.txt), loc.
- **DECISION — Absolute-Cognatic is FAKED:** per the oracle limitation, "Absolute Cognatic" = the cognatic law PLUS the `absolute_cognatic_succession` modifier (small legitimacy/reputation nod) + tooltip presenting it as gender-equal. Mechanically it is still cognatic (males slightly preferred). This is explicitly a compromise, not true equal succession.
- **DEFERRED / FLAGGED FOR REVIEW:**
  - **Boot-safety risk:** re-adding the succession_law group makes `agnatic_succession_law` (first member) the DEFAULT for every monarchy at game start — a mod-wide behaviour change. Historically fine for 1763 (male-line was the norm) but must be confirmed not to regress/crash. The adversarial review must check this specifically.
  - Egyptian / agnatic-seniority / elective vanilla succession tiers were intentionally NOT reintroduced (out of scope — task is female-line laws only).
  - The reform buttons live on the QING GC surface only (the laws are monarchy-general, but the only player GUI is the Qing view). AI never uses these (ai_is_valid=no).
  - No mission-tree / marriage-claim interaction was wired (the task mentioned female-line laws changing which marriages create pressable claims — that heiress-claim coupling is DEFERRED; it needs the #313 marriage-claim layer).
