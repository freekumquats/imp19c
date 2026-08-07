# DESIGN — customs meters — LARGELY RETRACTED (efficiency already derived; foreign_control not cleanly concretizable)

**Branch:** merge-overnight. **Status:** ❌ MOSTLY RETRACTED 2026-08-06 after adversarial review. DO NOT BUILD as first drafted.

## Why this doc was wrong (two false premises, verified)

The original draft claimed both customs meters are pure accumulators with concrete referents to derive
from (custom-house buildings + the IG character). Adversarial review + code verification found:

1. **`qing_customs_efficiency` is ALREADY DERIVED — the granary false-positive AGAIN.** It is a
   drift-toward-target quantity (`se_QING_CUSTOMS.txt:170-186`): `eff_target = (foreign_control×2 +
   qing_bureau_integrity)/3`, and efficiency nudges ±3/pulse toward it. NOT an accumulator. My "no derive
   block" claim was false. (This is the THIRD granary-style false positive this session — granary,
   gp_tension, customs. Standing lesson reinforced: read the full driver before calling a meter an
   accumulator.)
2. **Four custom-houses ARE seeded at 1763** — `se_QING_BUILDINGS.txt:249-252` seeds 粵海關 Canton, 閩海關
   Xiamen, 浙海關 Ningbo, 江海關 Shanghai (the historic 1685 native 海關), plus Macau's concession. My "at
   1763 there are NO custom-houses" premise was flatly wrong. Worse, these pre-modern native customs share
   the `qing_customs_house_building` TYPE with the 1854 foreign Maritime Customs — so a building-count
   cannot distinguish native from foreign service, making it unusable as the foreign-service signal.
3. **`foreign_control`-from-IG is broken:** Hart is minted `culture = scottish` with NO foreign flag
   (`qing_roster_events.txt:498`); "not chinese_group" mis-flags the Manchu ruling house (Manchu ∈ jurchen
   group, not chinese_group); a binary "IG foreign?" can't reproduce the 0–100 gradient the consumers band
   on (≤20/≥50/≥66) or the continuous **sinicize verb** (`:144`) that walks foreign_control down and trips
   the ≤20 relinquish — a derived value would snap, not glide, and fight that verb.
4. **Internal contradiction:** the doc said "keep the existing drift (:180)" AND feed it a building-derived
   target — but that drift's target IS the foreign_control+bureau_integrity formula; you can't keep it and
   replace it.

## Correct assessment
- **`qing_customs_efficiency`:** already a coherent derived meter (foreign_control + host bureau_integrity).
  LEAVE. Not a concretization target.
- **`qing_customs_foreign_control`:** genuinely a pure accumulator (establish +60, appoint +15, sinicize
  `$amount$`) — BUT deriving it from "IG is foreign" is worse than the status quo (§3 above). Its
  continuity is load-bearing for the sinicize verb. LEAVE as an accumulator; it works.
- Both are **#91 E hybrids that are fine as shipped** — the custom-house building is the concrete face, the
  meters are the summary layer, and efficiency already reads real host-competence (bureau_integrity).

## The one narrow, optional salvage (NOT concretization)
Fold a **guarded live IG `finesse` bonus** into efficiency's EXISTING target (`:173-176`): a capable
Inspector-General (Hart, finesse 9) collects better. `read var:qing_customs_ig_holder.finesse` guarded on
`has_variable` + `is_alive` (the var is removed on sinicization, `:155`). That's a small re-tune of a
working formula — a character-competence term, in the council-effectiveness spirit — NOT a rework. Low
priority, optional.

## Bearing on the audit
Reclassify customs from TARGET → **LEAVE** (efficiency already derived; foreign_control works and its
continuity is needed). Remove it from the doc-less-targets list.
