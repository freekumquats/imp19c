# Global Province Ownership Audit — 1763

**Mandate (operator):** go over every one of the 13,281 province IDs, identify its proper historical
owner in 1763 (if any), and **create / update / remove tags** so the game setup matches 1763 history.
Deliverable: `PROVINCE_OWNERSHIP_1763.csv` — one row per province: `province_name, province_id,
owner_name_1763, owner_tag_1763, historical_justification_1763_with_source, current_owner_tag, status,
confidence`. `owner_*_1763` = the historically-correct owner; where it differs from `current_owner_tag`
the game is corrected.

Branch: `merge-overnight`. Every setup change gated on `setup/main/check_setup_invariants.py`
(0 new ownerless capitals, 0 new double-owned). Static-verified only — **no boot access this session**;
all changes are boot-pending. All commits authored freekumquats.

This file is the running DECISION LOG for the audit. Every tag created/updated/removed and every
non-obvious ownership call is recorded here with its reason + source.

---

## Method

1. **Foundation (done).** `build_ownership_audit.py` extracts name + current owner for all provinces →
   CSV skeleton. Baseline: OWNED 8775, UNOWNED(named) 2589, UNNAMED-placeholder 1917 (PROV#### =
   wasteland/sea/unused — excluded from tag work).
2. **Regional research.** Dispatch historical-research agents per world region to establish 1763 ground
   truth (polity → territory), citing academic sources (English + native-language scholarship where
   apt). Each returns: which polities existed, their extent, and whether they should be a full tag,
   a reduced-authority tag, or culture/population-only (no tag — stateless peoples).
3. **Reconciliation.** Fill the CSV's `owner_*_1763` + justification columns from the research; flag
   every province where current ≠ correct. Classify each fix: create tag / update tag cores / remove
   or empty tag / reassign province / leave (stateless → culture-only).
4. **Apply in invariant-gated batches** (5–8 tags per commit, checker must pass), each recorded here.

## Hard constraints
- Ownerless-capital crash class: every tag's capital ∈ its own non-empty cores. Enforced by the checker.
- Do not steal provinces from a LIVE tag without a historical reason recorded here.
- Stateless peoples (Aboriginal, San, Papuan interior, etc.) get culture/population, NOT a tag.
- Province geography source: `localization/english/provincenames_l_english.yml` (all 13,281 named).
- Tribal/rulerless tags follow the DIN/DNE pattern (no set_as_ruler, no create_character → no char-id
  concern). A centralized polity needing a named ruler adds the char at global max id+1.

---

## Decisions log

### 2026-07-20 — Foundation + first correction

**DNE (Dene) created — I-0.** DIN/Navajo (Diné) was a na-dene CATCH-ALL holding both the Four Corners
Navajo (7 cores, capital Tohatchi 2657) AND 18 northern BC/Pacific-NW provinces (Prince George,
Kamloops, Jasper, Fort St. John, Mackenzie, Yuquot, Nelson BC, Spokane, Colville…). Those northern
lands are **Northern Athabaskan (Dene)**, not Navajo (Southern Athabaskan) — sharing the na-dene
language family is why they were lumped, but a Tohatchi-capitaled Navajo tag should not own British
Columbia.
- **CREATE** DNE: rulerless federated_tribe, `primary_culture = chipewyan` (canonical Northern
  Athabaskan/Dene, culture exists), capital Mackenzie 4257, holding the 18 northern provinces.
- **UPDATE** DIN: trimmed to the 7 Four Corners Navajo cores.
- Justification: Athabaskan linguistic geography — the Navajo/Apache (Southern Athabaskan) migrated to
  the SW ~15th c.; the northern Dene (Chipewyan, Kaska, Sekani, Dakelh, Tahltan, etc.) remained across
  the western Subarctic/Cordillera. In 1763 these were distinct peoples, not one polity. (General
  ethnographic consensus; to be sourced precisely in the N. America research pass.)
- Invariant gate: 629 blocks, capital∈cores for both, 0 new ownerless/double-owned. Commit 931146f7b.

**Correction to prior overnight claim:** I earlier wrote "DIN correctly in the Four Corners, skip I-0."
That was wrong — it conflated the checker's self-consistency result (capital∈cores → won't crash) with
correct geographic placement (never verified). The province geography WAS available (provincenames loc);
my "no geography" deferral premise was false. Both errors corrected; the audit proceeds properly.

### Regional research — dispatched (in progress)
Agents fired per region to establish 1763 ground truth with sources. Results appended below as they
return, then reconciled into the CSV.
