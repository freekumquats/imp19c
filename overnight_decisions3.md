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
