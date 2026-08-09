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

---

## #1 — Rescale Qing player treasury costs into the hundreds (cap ~1200) — DONE

**What:** Qing pay-for-benefit events/ministry-buttons charged gold in the **tens** (modal
30–80), noise against a treasury seeded at ~6 years' running costs. Lift them into the
hundreds so a spend choice is a real fiscal decision.

**What I did:** one closed-form monotonic map `new = round5(40 × sqrt(old))` applied to the
whole player-initiated Qing spend surface via `tools/treasury_rescale.py` (dry-run manifest →
eyeball → `--apply`). Sample: 10→125, 30→220, 60→310, 100→400, 240→620, 900→1200.
- **Mechanic (328 edits):** every `add_treasury = -X`, `treasury >= X` (literal RHS), and verb
  `cost = -X` param in `events/imp19c_mod_events/qing_*.txt` + `currency_crisis_events.txt`,
  `common/scripted_effects/se_QING_*.txt`, `common/scripted_guis/QING_*.txt`.
- **Loc (147 edits):** matching cost tooltips via a NUMBER-LEVEL classifier — a number scales
  iff treasury-associated (¥ / "treasury of" / nearest resource-noun) AND a cost not a gain
  (nearest cost-verb vs gain-verb / sign), with a same-line cost-restatement rule. Never
  `_DESC` keys, never a `custom_tooltip` wired from `common/missions/`.
- Stale `LOG_fail`/`LOG_line`/comment cost numbers in the touched verbs updated to match.

**Key decisions + why:**
- *Monotonic closed form, not a piecewise table* — a monotonic map preserves equality, so
  wherever `gate == cost` today it stays coupled after, with NO proximity heuristic (fixed the
  v1 event-level-gate miss). √-curve compresses the top so 250/500/900 ramp to the cap without
  colliding.
- *Ministry buttons IN by necessity* — they share the event verbs' cost bodies; excluding them
  would desync a button from its own cost. Not scope creep.
- *Missions OUT* — `common/missions/` (253 own costs) don't share event verbs, live in their
  own tree, and pace against mission rewards; a defensible subsystem boundary, not a deferral.
  Loc side hardened: mission `custom_tooltip` keys built into a runtime exclusion set (verified
  0 leaks incl. `qing_sp_*_DESC`).
- *Rewards / `var:` / non-Qing (usa/spa/flavor_eve) untouched* per the non-Qing principle.

**Reviews (design + applied diff, both adversarial):**
- Design v2 review — 3 findings, all fixed: (1) event-level gates → map ALL gates
  monotonically; (2) verb-delivered costs → include verb bodies + `cost=` params + sharing
  buttons; (3) FlavorEvents generic → OUT. Census confirmed no Qing `treasury >=` is a pure
  non-price wealth check and no event verb is called from a mission.
- Applied-diff code-review — 2 real findings, both fixed: **(HIGH)** `qing_integ.40.e.tt`
  quoted "100 gold" while its option charged the scaled 400 (verb-less cost restatement the
  classifier couldn't see) → allowlisted (key,100); **(HIGH invariant)** two combined-condition
  guards (`treasury >= 90/100` sharing a line with a `var:` condition) were skipped by the old
  line-level `'var:' not in line` guard, desyncing gate from charge → removed the redundant
  guard (RE_GATE already rejects `var:`/`negative_treasury` RHS structurally); both gates now
  scale to 380/400 == their charges. LOW stale-string finding also fixed.

**Verification:** map strictly monotonic, range [125,1200]; every gate==its charge (spot-checked
qing_war 490/490·535, WORKS wall/canal 620·595, CARAVAN escort 695, the 2 fixed verbs 380/400);
all LOG_fail thresholds match their gates; 90 files 487/487 digit-only swaps; brace balance
identical to HEAD; EOL 487/487 ignore-cr match (no churn); no BOM flips; no non-Qing leakage.

**Commit:** `4067120d9`, pushed to merge-overnight. Acceptance is boot-gated on the user's
machine (values render/charge correctly in-game); nothing here is boot-unverifiable.
