# Overnight run — 2026-08-09

Autonomous backlog run under the `imp19c-overnight` skill. Branch `merge-overnight`, all
commits authored+committed by freekumquats. Design-first + adversarial review for larger
tasks; small mechanical edits go straight to code-review → commit → push. No deferrals.

---

## #23 — Currency / economy deep fix (silver-price oscillation) — DONE

Worked ahead of this doc under the strict diagnose→design→implement iterative protocol
(each stage adversarially reviewed). Full trail lives in `audits/AUDIT_CURRENCY_23.md`
(not here, per instruction). Summary:

- **Root cause:** the shared `sqrt` scripted effect (`se_ECON_functional.txt`, "Tobbzn's
  method") was mathematically broken — (1) loop recurrence computed `y = x/param` instead
  of the Babylonian invariant `y = param/x` (input>1 decayed x→~0); (2) signed epsilon
  guard skipped the loop entirely for input<1. Together a discontinuity at base=1.0 that
  rail-slammed gbip ~0.003⇄0.88 every quarter — the sawtooth. CHI peg is a verified
  passthrough of gbip.
- **Fix:** corrected recurrence `y=param/x` + bounded `while { count=12 }` loop (fixed-point
  safe; epsilon guard could 2-cycle forever under 3-decimal fixed point). Seed x=param, y=1.
  Sole caller = the gbip write at `se_GLOBALTRADE_split.txt:2701` (guarded `if base>0`), so
  blast radius = gbip only.
- **Status:** implemented, code-reviewed PASS, committed `14c9ed899`, pushed. ACCEPTANCE is
  boot-gated on the user's separate machine: re-run `tools/curx_analyze.py` on the new
  debug.log — gbip row must be flat, inflation~0, cost-of-living ~5 taels/adult/yr yardstick.

---

## #6 / #10 / #11 / #14 — small trait + localization edits — DONE

Four independent small tasks bundled into one focused commit `f5ef9daac`.

- **#6** — added missing `chinese_emperor` status-trait localization (title "Son of Heaven
  (天子)" + desc) to `imp19traits_l_english.yml`. The trait is granted to Qing rulers in
  `setup/characters/00_Qing.txt` (6 sites) but had no card string.
- **#10** — gave the six CIVIL exam-degree traits a modest `finesse` boost in
  `common/traits/00_imp19c.txt`: shengyuan=1, juren=1, gongshi=2, jinshi=3, hanlin=4,
  fanyi_jinshi=3. Monotonic-with-prestige, mirrors the existing military 武 martial 1..4
  ladder and the holding_income_modifier gradient.
- **#11** — added `value_civilization_cap` / `value_civilization_increase` interface labels
  to `interface_l_english.yml`. These are declared province-value modifier icons
  (`00_modifier_icons.txt:2716/2720`) that were rendering as raw keys.
- **#14** — added `monthly_character_popularity` to the two disgrace traits (disgraced=-0.1,
  completely_disgraced=-0.25), alongside the existing fam-prestige drag. Magnitudes match
  existing scheme/event ranges; hard disgrace ranks below the lesser taint.

**Key decision (EOL discipline):** `00_imp19c.txt` has MIXED line endings at HEAD (CRLF
civil-degree region, LF disgrace region). My first Edit-tool pass normalized everything to
CRLF, ballooning the diffstat to 346 lines of pure EOL churn. Reverted and re-applied via a
byte-precise script that preserves each region's native EOL — final diff is exactly 8
added lines, 0 deletions, no churn (verified `git diff --ignore-cr-at-eol --numstat` == plain).

**Review:** code-review agent — CLEAN, no findings. Confirmed `finesse` and
`monthly_character_popularity` are both legal inside status/health trait blocks (direct
precedent: freemason/banker finesse, 00_health.txt monthly_character_popularity), braces
70/70, loc keys match engine references, no EOL/BOM churn.

**Commit:** `f5ef9daac`, pushed to merge-overnight.
