# DESIGN — Concretize `qing_corruption_level`: derive it from real character corruption (吏治貪腐)

**Branch:** merge-overnight. **Status:** ✅ SHIPPED 2026-08-06 (commit 748ab8e2a, one-sweep fold into QING_council_recompute). **Scope:** CHI only.
**Companion to:** `DESIGN_BUREAU_CAPACITY_CONCRETIZE.md` (same concrete-over-abstract program).

## 0. The problem & the user's test

`qing_corruption_level` is a stored 0–100 country meter. The user's acceptance test:

> "defensible **iff** it is derived from character corruption, an actual vanilla value."

Audit verdict (2026-08-06): **it FAILS.** It is a free-floating accumulator — seeded 12/0
(`se_QING_DECLINE.txt:76,78`) and moved ONLY by scattered flat `QING_DECLINE_nudge` calls. It is NOT
derived from the vanilla per-character `corruption` value, even though the mod already reads real
character `corruption` / `has_trait = corrupt` in dozens of event gates (`se_QING_DECLINE.txt:1581/1635/
1676`, `se_QING_ROSTER.txt`, etc.). The concrete referent exists (corrupt officials) but does not drive
the number. Same anti-pattern as `qing_bureau_capacity`, and the fix follows the same template:
`qing_council_effectiveness` (derived live from the seated councillors' skills, `se_QING_COUNCIL.txt:450`)
is the model of a meter *done right*.

## 1. Scale of the change — read this before committing to it

This is a MUCH larger surface than the yamen task. Grepped:
- **112 writer sites** (`QING_DECLINE_nudge = { var = qing_corruption_level  amount = ± N }` + a few
  `set_variable`) across **~25 files** — events (works/keju/censorate/office/revenue/household/decline/
  reform/personnel/roster/harem/opium/rebellion/dynasty/…) and scripted_effects.
- **~95 reader sites** — corrected below in §1's "Corrected surface" (event gates + `has_variable` guards + 2 GUI reads).
- **A 3-tier band** (`QING_DECLINE_apply_corruption_band`, `se_QING_DECLINE.txt:163`) applying real
  country modifiers `qing_corrupt_rampant` (≥60) / `qing_corrupt_endemic` (≥30) / `qing_corrupt_clean_
  government` (≤10).

**Corrected surface (adversarial review 2026-08-06 — the earlier counts were low):**
- **~115 writer sites** (`QING_DECLINE_nudge = { var = qing_corruption_level }` + 4 direct set/change).
- **~95 reader sites** (64 `var:` reads + 31 `has_variable` guards + **2 GUI `GetVariable` reads** — the
  GUI reads are outside the scripted-effect world and are also preservation targets).
- **~50 code files** touch the token (34 event files + 14 scripted_effects + 2 GUI), not "~25."
So the real surface is **~210 sites across ~50 files**, not 170. This matters below.

## 2. Thesis — MIRROR `qing_council_effectiveness` EXACTLY: single store, character target, drift, nudges kept

> ⚠️ **REWRITTEN 2026-08-06 after implementation-plan review.** The prior draft mandated a TWO-STORE model
> (new residual var + redirect ~112 writers + save-migration split) on a **false premise** — it claimed
> `qing_council_effectiveness` "works only because it has zero event writers." **That is factually wrong:**
> effectiveness has ~40 event `QING_DECLINE_nudge` writers (`se_QING_DYNASTY.txt` ×13, `qing_office_events.txt`
> ×15, faction/reform/roster) PLUS its own drift nudge (`se_QING_COUNCIL.txt:573/577`) — all on the live var.
> So the blessed pattern the user asked to mirror IS single-store. My "single-store is incoherent" argument
> was a strawman against the very design being copied. Two-store is defensible but over-engineered; build the
> single-store mirror.

**THE BUILD — single-store mirror (matches `qing_council_effectiveness` 1:1):**
1. **`QING_officialdom_corruption_target`** — a recompute (effect, §6) that sums the seated office-holders'
   vanilla `corruption` value (proven writable — `add_corruption`, ~21 uses e.g. `se_QING_AFFINITY.txt:395`)
   into a country-scope target, mirroring `qing_council_eff_target` (`se_QING_COUNCIL.txt:450-456`).
   Emperor/regent read separately (NOT in `qing_council_members` — `se_QING_COUNCIL.txt:368`).
   **Baseline-K correction (load-bearing, review #3):** autofill officials carry NO corruption
   (`create_character` at `:195-205` adds skills+degree trait only), so a raw aggregate opens ~0 and trips
   the `clean_government` band (≤10). Add a baseline constant so the target opens near the **12** seed at
   1763 — do NOT let the raw aggregate set the opening.
2. **Drift the live `qing_corruption_level` ±N/pulse toward the target** (via
   `qing_officialdom_corruption_target_cmpsvalue`, the proven RHS-compare idiom), exactly as effectiveness
   drifts ±3 toward `qing_council_eff_target_cmpsvalue` (`:571-578`).
3. **LEAVE the ~108 event nudges in place** on the live var. They are impulses that decay away as the drift
   re-converges toward the character target — the *damped* behavior effectiveness already ships (a `+25`
   scandal spikes then eases back toward the ~12 character baseline: desired, not a bug). NO residual var,
   NO writer redirection, NO save-migration split.

The **Tier-1 writer conversion** (§4) is now an OPTIONAL refinement, not a phase-1 requirement: the strongest
scandal/purge beats MAY additionally do `add_corruption`/`add_trait = corrupt` on the culprit office-holder
(so the character target itself moves, not just the live var), progressively making corruption more
character-anchored. But the single-store mirror already passes the user's `iff` test to **precisely the same
degree** `qing_council_effectiveness` does — which is the bar the user set.

### Why keep `qing_corruption_level` as the read interface (not delete it like bureau_capacity)?
Because bureau_capacity had ONE clean concrete referent (yamen count) and ~15 consumers. Corruption has
~200 touch sites, ~90 of them reads (incl. 2 GUI). Keeping the 0–100 var as the drifting live meter (exactly
as effectiveness keeps its var) preserves all readers and the band while anchoring its steady-state pull to
real corrupt characters. This is the SAME interface-preservation effectiveness uses — not a compromise.

### Two-store: optional Phase-3 refinement only
An explicit decaying `qing_corruption_event_residual` (separating institutional graft from character graft)
is defensible if playtest shows the single-store damping is too coarse — but it is NOT required, NOT phase-1,
and its prior "single-store is incoherent" justification was false. Park it as a future option.

## 3. The derived base — `QING_officialdom_corruption`

Mirror `qing_council_effectiveness`'s aggregate-over-office-holders idiom
(`se_QING_COUNCIL.txt:268-335, 450-456`), but average **corruption** instead of skill:

```
QING_officialdom_corruption = {   # 0..100, Scope: country (CHI). Read-only svalue.
    # aggregate corruption of the real seated office-holders — the concrete truth behind the meter.
    # sum each filled qing_office_<key>_holder's vanilla `corruption` (0..100), + a weight for
    # has_trait = corrupt, divided by the count of filled offices. Emperor/regent weighted like
    # the effectiveness aggregate so the throne's own graft-tolerance moves it.
    # (built as a scripted_effect that sums into scratch vars, exactly like QING_council_recompute,
    #  because a bare svalue cannot iterate ordered offices as cleanly — see §6 feasibility.)
}
```

Implementation reality (§6): the council aggregate is NOT a pure svalue — it's a scripted_effect
(`QING_council_recompute`) that walks the office-holder set into `qing_council_skill_total` /
`_filled_count` then computes a target. **Corruption must follow the same shape**: a
`QING_GOV_recompute_officialdom_corruption` effect in the governance pulse that sums holder `corruption`
into a scratch total and divides by the filled count, producing `qing_officialdom_corruption_target`.

## 4. Writer conversion (the ~115 sites) — tiered, NOT all-at-once

Under the two-store model, ALL ~115 writers first move off the live level onto
`qing_corruption_event_residual` (Phase 1, mechanical). Then Phase 2 tiers which ones convert to CHARACTER
effects (leaving the ambient ones on the residual). Tier them:

- **Tier 1 — office/personnel/censorate/keju events (the ~60 sites whose fiction IS a specific official
  being corrupt or cleaned):** convert to character effects. `+N corruption` → the culprit office-holder
  gets `add_trait = corrupt` (or `add_corruption` if the vanilla effect exists — verify) ; `−N` (a purge,
  an honest censor) → `remove_trait = corrupt` / lower a character's corruption, or DISMISS the corrupt
  holder (`QING_office_vacate_dispatch`). These are the sites where the concrete conversion is *most*
  meaningful and legible.
- **Tier 2 — systemic/ambient nudges (works/canton/household/revenue pulses, the small ±1..3 drifts):**
  these represent diffuse institutional graft, not one named official. Keep them as a nudge, BUT nudge the
  *target* anchor, or leave them as a residual drift on top of the character base. Lowest priority.
- **Tier 3 — the big set-pieces (`se_QING_MECHANICS.txt:83 +12`, `:510 −25`; `se_QING_SELFSTR.txt` resets;
  `qing_decline_events.txt:419 +25`):** these are era/reset beats (Heshen's fall, Self-Strengthening
  cleanup). Convert to character mass-effects where they name people (Heshen = a real character → seize
  his estate + remove him), else keep as an anchor shift.

Under the two-store model (§2): Tier-1/3 events that name a culprit act on the CHARACTER (`add_corruption`
on the office-holder). Tier-2 ambient nudges write `qing_corruption_event_residual`. The pulse recomputes
`qing_corruption_level = clamp(QING_officialdom_corruption + qing_corruption_event_residual)`. As Tier-1/3
convert, the residual's share shrinks and character corruption dominates.

## 5. What changes vs. stays
- The **~95 reader gates** (`var:qing_corruption_level >= 40`, `has_variable` guards, **and the 2 GUI
  `GetVariable` reads**) — the var still exists as the readout, so these are untouched. VERIFY the 2 GUI
  reads explicitly.
- The **band** (`QING_DECLINE_apply_corruption_band`) and its 3 modifiers — untouched CODE, but see the
  ripple caveat below.
- **Writers CHANGE:** the ~115 event nudges are redirected — Tier-1/3 to `add_corruption` on characters,
  Tier-2 to `qing_corruption_event_residual`. This IS a rewrite; the earlier "keep writers untouched"
  claim was wrong (§2).
- **Ripple caveat (was falsely called "untouched"):** `qing_bureau_integrity = 100 − corruption` and
  `qing_gov_corruption_drag = corruption/2` feed the capacity/exam targets. The derivation CODE is stable,
  but if the re-root moves the corruption *value*, their *outputs* shift. Must re-validate that the new
  1763 opening corruption lands where integrity/capacity expect (below).
- **Seed MUST stay a constant (do NOT compute the aggregate at seed) — two reasons (review #3/#4):**
  1. At `on_game_initialized` (where `QING_DECLINE_init` seeds) the office-holder set is **empty** — the
     day-32 deferred autofill (`qing_force_setup.12`, `se_QING_COUNCIL.txt:58-62`) hasn't run yet, so an
     aggregate would read ~0 off no holders.
  2. Even after autofill, the generated officials carry **no corruption** (autofill `create_character`
     adds finesse/charisma/martial/zeal + a degree trait only — `se_QING_COUNCIL.txt:195-205`), so the
     aggregate opens ~0, NOT the intended High-Qing 12, which would immediately trip the `clean_government`
     band (≤10 → +tax/+loyalty from turn one), a gameplay swing the 12-seed deliberately avoids.
  → Keep the constant seed (12/0). To make the *opening* character-anchored, either seed the 1763 roster's
    corruption (`add_corruption` on the starting officials to a High-Qing baseline) or add a baseline
    constant `K` to the aggregate so `base` opens near 12. The pulse then takes over from the seed.

## 6. Feasibility / gotchas (verified in review, 2026-08-06)
- **`add_corruption` EXISTS and is proven** — a numeric character write (±), already used ~21× in the mod
  (`se_QING_AFFINITY.txt:395` parametric `add_corruption = $amount$`, `se_QING_HOUSEHOLD.txt:223/243`,
  `qing_subject_integration.txt:316`). The char `corruption` value is read as a 0–100 gate throughout
  (`se_QING_DECLINE.txt:1581/1635`). So the aggregate and Tier-1 conversion are feasible; **drop the
  earlier "may be trait-only" hedge** — no oracle trip needed, it's answered in-repo.
- **Aggregate is an EFFECT, not a pure svalue** — piggyback `QING_council_recompute`'s existing
  office-holder walk (`se_QING_COUNCIL.txt:714-735`); add one line summing `prev.corruption` into a scratch
  total. **No second sweep.** Emperor/regent are NOT in `qing_council_members` (`:368`) — read them
  separately via the figurehead path, matching effectiveness.
- **RHS-comparison rule:** the drift-toward-target compare needs the `_cmpsvalue` wrapper idiom (every
  sibling uses it, e.g. `qing_council_eff_target_cmpsvalue:572`); a bare `var:x < var:y` violates the
  standing RHS rule and won't compile. Author `qing_officialdom_corruption_target_cmpsvalue`.
- **Div/0:** floor the filled-office count at 1.
- **Save migration:** existing saves have a hand-accumulated `qing_corruption_level`; on the patch, split
  it — leave the value in place, let the first pulse recompute it as `base + residual` (seed the residual
  from the old value minus the fresh base so the transition is continuous, then let it decay).

## 7. Recommendation on scope — HONEST phasing (Phase 1 alone does NOT pass the test)
Real surface ~210 sites / ~50 files. The user's test ("derived from character corruption") is met ONLY
once the dominant writers act on characters — a ±2–3 pulse anchor cannot overcome a stream of +10/+25
hand-nudges, so leaving them on the number keeps it event-dominated. Phasing:
- **Phase 1 (scaffolding, NOT test-passing):** add `QING_officialdom_corruption` aggregate +
  `qing_corruption_event_residual` var; redefine `qing_corruption_level = base + residual`; redirect the
  ~115 writers to the residual (mechanical); keep the constant seed. Now the *structure* is right but
  corruption is still event-dominated — an honest hybrid, explicitly NOT yet passing the test.
- **Phase 2 (this is what passes the test):** convert Tier-1/3 writers (office/personnel/censorate/keju +
  the named set-pieces like Heshen) from residual-nudge to `add_corruption`/trait/dismiss on the culprit
  characters. As these convert, character corruption becomes the dominant term.
- **Phase 3:** Tier-2 ambient cleanup; optional far-future deletion of the var (repoint ~95 readers).

## 8. Build checklist
**Phase 1 (structure):**
1. Add `qing_corruption_event_residual` (stored, decays toward 0) + `QING_officialdom_corruption` recompute
   (piggyback the council walk; figurehead read; div/0 floor) + `qing_officialdom_corruption_target_cmpsvalue`.
2. Redefine `qing_corruption_level` recompute = `clamp(base + residual)` in the pulse; KEEP the constant
   seed (§5) + baseline-K so the 1763 opening ≈ 12.
3. Redirect the ~115 writers from `var = qing_corruption_level` to `var = qing_corruption_event_residual`
   (mechanical find/replace within the nudge calls; verify each).
4. Verify the ~95 readers (incl. 2 GUI) + band still read the level unchanged; re-validate the 1763 opening
   lands in the intended band (NOT clean_government) and that integrity/capacity/exam outputs are sane.
**Phase 2 (concrete — the test-passing work):**
5. Convert Tier-1/3 named-culprit events to `add_corruption`/trait/dismiss on the office-holder.
**Review gates:** two-store model (base + residual), not a `max()`; seed stays constant; RHS-cmpsvalue idiom;
no reader/band/GUI regressions; 1763 opening re-validated; div/0 floor; brace/quote/BOM; boot-crash review.
