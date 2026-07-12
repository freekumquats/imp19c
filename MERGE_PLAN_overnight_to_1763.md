# Merge plan — `overnight-312-315-audits` → `1763_bookmark`

**Status: PLAN ONLY — do not execute until approved.**
Drawn up 2026-07-11. Both branches diverge from **`cf688030`** (the boot-test checklist commit).

---

## 1. What each branch has (since divergence `cf688030`)

### Incoming from overnight (10 commits, would be merged IN):
- `69814e9e` Overnight run: branch + decisions doc
- `722b7bd9` Overnight: mandate → Top-3 build candidates
- `6bd7f126` **#315** Qing colonization arc: Australia + New Guinea
- `6e0765a1` **#312** Female-line succession laws + Pragmatic Sanction
- `9d056fbd` **#313** Marriage: non-ruling families + candidate-list filters/sorts
- `e985e5e3` **#321** Imperial Examination scholar hire-pool (科舉)
- `9ef99561` **#322** Tributary System embassy rhythm (朝貢體系)
- `87f36b1b` **#323** Grand Canal grain-tribute logistics (漕運)
- `959e502d` **#324** Heiress-claim coupling (female-line law × marriage)
- `463abae8` #324 post-fix review: `is_subject = no` guard

### Already on 1763 (5 commits, overnight is MISSING these):
- `c6d04a26` #314 B21/B22 unit placement + B7/B14 BOM + B6 religion + Bug1/2/3
- `a9f3b6aa` #329 wrong start rulers (death_date bug)
- `dadbf328` NEW-B27 setup id renumber
- `b224f2e0` **#330** marry-into-subject + foreign-spouse lobby + B12 allow-subjects
- `b591a513` #314 B15-v2 subject-button overlap

**Direction:** merge overnight **into** 1763 (1763 is the live testing branch per the branch policy; it must end up a superset).

---

## 2. Conflict map — 10 overlapping files

Churn shown as `[+added -removed]` since `cf688030`.

| File | overnight | 1763 | Risk | Nature |
|---|---|---|---|---|
| `common/scripted_guis/MARRIAGE_actions.txt` | +203 -8 | +12 -4 | **HIGH** | Both edit the SAME `marriage_open_candidates` block — overnight #313 is a **two-pass rewrite**; 1763 is my B12/#330 patch to the **old single-pass** version. True design conflict. |
| `common/scripted_effects/se_MARRIAGE.txt` | +164 -26 | +62 -0 | **HIGH** | overnight adds #313/#324 effects; 1763 adds the #330 subject-branch + origin-tag. Likely adjacent inserts + possible overlap in `MARRIAGE_apply_marriage_bond` / `MARRIAGE_form_pact`. |
| `common/scripted_triggers/00_marriage_triggers.txt` | +65 -0 | +23 -0 | MED | Both ADD new triggers (overnight: filters/sorts; 1763: `MARRIAGE_candidate_realm_trigger`). Additive → probably auto-mergeable, but same file region. |
| `gui/marriage_window.gui` | +32 -0 | +5 -1 | MED | overnight adds filter/sort UI; 1763 has the Bug 3 own-house header fix. Different regions likely. |
| `gui/government_view.gui` | +46 -0 | +13 -14 | MED | overnight #312/#324 succession UI; 1763 Bug 1/2 Throne+effectiveness. **NOTE: Bug 7 agent is ALSO editing this file right now (uncommitted)** — must be committed before merge. |
| `common/scripted_effects/se_QING_COUNCIL.txt` | +6 -0 | +61 -0 | LOW-MED | overnight small; 1763 adds the #330 foreign-spouse check (appended at EOF). Different regions. |
| `common/on_action/00_monthly_country.txt` | +8 -0 | +9 -0 | LOW | Both add pulse hooks; likely adjacent lines in the quarterly effect. |
| `localization/english/marriage_l_english.yml` | +16 -0 | +4 -1 | LOW | Both append keys; possible same-line-region but additive. |
| `localization/english/qing_governance_l_english.yml` | +16 -0 | +1 -1 | LOW | Additive loc. (Bug 7 agent also adding ~14 keys here — commit first.) |
| `localization/english/qing_office_events_l_english.yml` | +8 -0 | +10 -0 | LOW | Both append (overnight events; 1763 qing_office.30). Additive. |

**Non-overlapping = auto-clean:** all of overnight's NEW files (se_QING_EXAM/TRIBUTE/CANAL/WORKS, qing_keju/tribute/canal events + their loc, succession laws/modifiers, colonization) and all of 1763's setup/characters + legion_setup + gui/imp19c_windows + gui/qing_religion + gui/diplomatic_view. No interaction.

**Good news:** overnight does **NOT** touch `imp19c_effects_legion_setup.txt` — so the pending B21/B22 army/navy fix is fully independent of this merge.

---

## 3. The one genuine design conflict: the marriage candidate builder

`MARRIAGE_actions.txt` `marriage_open_candidates`:
- **overnight #313** rewrote it as a **two-pass** build (unordered cache pass → ordered list pass) to support the new candidate-list **filters + sorts**, and it also expanded eligibility to **non-ruling families**.
- **1763 (my B12/#330)** patched the **old single-pass** build to (a) drop `in_diplomatic_range` and (b) use `MARRIAGE_candidate_realm_trigger` (eligible realm OR ROOT's own subject).

overnight's version still has `MARRIAGE_eligible_realm_trigger` + `in_diplomatic_range` (does NOT include my B12/subject fixes). So a blind merge would either lose my B12/#330 fix or lose the two-pass rewrite.

**Resolution rule for this file:** take overnight's **two-pass structure as the base** (it is the richer, later design), then **re-apply the 1763 semantics on top**:
1. swap `MARRIAGE_eligible_realm_trigger` → `MARRIAGE_candidate_realm_trigger` in the builder's `every_country` limit(s) AND in the propose/betroth `scope:target` checks;
2. delete the `ROOT = { in_diplomatic_range = prev }` gate from the builder passes (keep it on the propose/betroth ACTIONS);
3. keep `MARRIAGE_candidate_realm_trigger` (from 1763's `00_marriage_triggers.txt`) — it merges in additively.
Same logic applies to `se_MARRIAGE.txt`: keep BOTH overnight's #313/#324 effects AND 1763's #330 subject-branch + origin-tag (they are separate effects / separate regions; verify the `MARRIAGE_apply_marriage_bond` alliance/entente/subject if-chain is preserved with the subject branch first).

---

## 4. Recommended execution sequence (when approved)

**Pre-merge (must-do first):**
1. **Land the two running background tasks:** commit the **Bug 7** office-tooltip edits (government_view.gui + qing_governance_l) — otherwise they collide with the merge and with overnight's government_view edits. (The commander-research agent output is data only, no repo changes.)
2. **Apply + commit the B21/B22 army-navy fix** (from the just-completed diagnosis) on 1763 first, so it's not entangled with the merge. Independent file (`imp19c_effects_legion_setup.txt`), overnight doesn't touch it.
3. Confirm working tree clean on 1763 (`git status`).

**Merge:**
4. `git checkout 1763_bookmark` (already here).
5. `git merge --no-commit --no-ff overnight-312-315-audits` — stop before committing to inspect conflicts.
6. **Resolve conflicts**, file by file, using §3 rules:
   - `MARRIAGE_actions.txt` — hand-merge: overnight two-pass base + re-apply B12/subject semantics.
   - `se_MARRIAGE.txt` — keep both sides' effects; verify the apply-bond if-chain.
   - The 4 loc files + `00_marriage_triggers.txt` + `00_monthly_country.txt` + `se_QING_COUNCIL.txt` + `government_view.gui` + `marriage_window.gui` — mostly additive; take both, dedupe.
7. **Per-file brace-balance check** on every conflicted `.txt`/`.gui` (the tab-depth gotcha).
8. `overnight_decisions3.md` — take overnight's copy (or drop; it's a scratch doc).

**Post-merge verification (before commit):**
9. Grep for the B12/#330 markers surviving in the merged builder (`MARRIAGE_candidate_realm_trigger`, no `in_diplomatic_range` in the builder, `royal_marriage_subject_tie`, `marriage_origin_country`, `QING_council_foreign_spouse_check`).
10. Grep for the #330 review-fix correctness (subject_loyalty on overlord, `qing_office.30` opinion directions).
11. **Adversarial Workflow review** of the merged marriage + council surface (the two HIGH-risk files especially) — same discipline as every other batch this session.
12. Fix any confirmed findings, re-check braces, then `git commit` the merge.
13. Update `BOOT_TEST_BUGS_2026-07-11.md` / task list; note the merge is **boot-test-owed** (per branch policy, merges to the testing branch need an in-game boot test before promotion to master).

**Do NOT push** until the user confirms (branch policy: push only when the user is ready to pull-and-test).

---

## 5. Risks / watch-items
- **Marriage builder is the crux** — if the two-pass merge is fumbled, either B12 regresses (empty list again) or the #313 filters break. This file deserves the most care + an explicit re-test.
- **Overnight is unpushed and boot-test-owed** — its 8 features (#312/#313/#315/#321/#322/#323/#324) have NOT themselves been in-game verified. Merging brings unverified content onto the testing branch; that's acceptable (that's what the branch is for) but the boot test after merge must exercise them.
- **Bug 7 + B21/B22 must be committed first** or they entangle with the merge.
- Double-check no overnight commit reintroduces a `death_date` on a `set_as_ruler` target or an out-of-range char id (the #329/NEW-B27 classes) — overnight predates those fixes; grep the merged setup/characters (none expected — overnight didn't touch setup/characters, but verify).
