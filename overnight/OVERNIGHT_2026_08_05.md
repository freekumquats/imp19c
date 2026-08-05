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

**Status:** implemented; pending adversarial code-review before commit.
