# DESIGN — Inner Mongolia as spun-off Qing subject states (option b)

> STATUS 2026-08-20: DRAFT v2 — design only, NOT implemented (large feature, deferred by user).
> v1 was architecturally WRONG and is corrected here. Per user design call on task #19: the
> shipped fix keeps a simplified vanilla governor slot at p:3309 Ulanqab (option a — char:674
> 蘊著 Yunzhu, the real 1763 綏遠城將軍, as a gameplay-uniformity stand-in on Qing-OWNED land).
> This document specifies the historically-faithful alternative (option b) for a later cycle.
>
> **v1 CORRECTION (why v2 exists).** v1 proposed "tie the owned Inner-Mongolia provinces to the
> Lifan Yuan minister" + "jasagh princes holding their banners as fiefs." That is incoherent:
> `set_as_governor` is VANILLA functionality that only applies to provinces a country DIRECTLY
> OWNS, and a jasagh holding a banner "as a fief" IS a subject relationship, not something that
> can be layered onto owned land. You cannot have fief-holding jasaghs on Qing-owned provinces.
> The real, faithful representation is therefore NOT a governance-tie on owned land — it is
> **spinning Inner Mongolia OFF as Qing subject states**, exactly the machinery the mod already
> uses for its other autonomous frontier subjects. That ownership→subject conversion is the whole
> feature; everything else hangs off it.

## The core historical fact

In 1763 Inner Mongolia had NO civil governor (巡撫/總督). It was administered as:
- **The banner-league (盟旗) system** — 6 leagues (盟: Jerim 哲里木, Josotu 卓索圖, Juu Uda 昭烏達,
  Xilingol 錫林郭勒, Ulanqab 烏蘭察布, Ikh Juu 伊克昭), each a confederation of hereditary banners
  (旗) ruled by a **jasagh (札薩克)** — a Mongol prince holding his banner as a hereditary fief
  under Qing investiture. A **league captain-general (盟長)** led each league (musters/arbitration,
  not a governorship).
- **The Lifan Yuan (理藩院)** — the central ministry that confirmed jasagh succession, set banner
  boundaries, ran the frontier legal code, and channelled tribute. It supervised the SUBJECT
  relationship from Peking; it did not "own and govern" the land as a province.
- **Chahar (察哈爾)** — the ONE exception: the eight Chahar banners were directly-ruled Eight-Banner
  territory under a 察哈爾都統, NOT a hereditary jasagh fief.

## Why option (a) is coherent and option (b) is a large feature

- **(a) keeps the land Qing-OWNED**, so vanilla `set_as_governor` is the only in-engine way to
  "administer" it, and a real 1763 official (綏遠城將軍 蘊著) in the slot is a correct-enough
  placeholder. Nothing is broken.
- **(b) requires converting Inner Mongolia from Qing-owned provinces into Qing SUBJECT STATES.**
  Once they are subjects, the jasaghs are the RULERS of those subject tags (not "governors" of
  owned land), and the Lifan Yuan supervises the subject relationship. This is the faithful model,
  but it is a multi-part territorial change, not a modifier bolt-on.

## Proposed representation (option b)

### B1 — Spin the banner-leagues off as new subject country tags (the core work)
For each jasagh league to be represented (start with the ones whose provinces currently sit in
Qing-owned Inner Mongolia — Ulanqab p:3309 and neighbours), mint a new country tag via the proven
new-tag recipe (memory `new-country-tag-recipe`: registry + country definition/BOM + 00_default +
localization):
- Transfer the league's provinces OUT of Qing ownership into the new tag (ownership + control +
  own_control_core), so the land is the subject's, not Qing's.
- De jure / core cleanup: the spun-off land must stop being a Qing core, or Qing keeps a reconquest
  claim and the AI churns (cf. the inert-tag / ownerless-capital crash playbooks — every new tag
  needs a valid owned capital or it hard-crashes at construction).
- No `set_as_governor` anywhere on this land any more — it is a subject, administered by its own
  ruler.

### B2 — Jasagh princes as the subject rulers
Seed the historically-attested 1763 jasagh / league-captain for each new tag as its ruler
(`set_as_ruler`), Mongol culture / vajrayana. Needs a dedicated 1763 jasagh research pass (same
zh.wikipedia office-list sourcing the governor sweep used). Because they are now RULERS of subject
tags, they are automatically outside the Qing court-position pool — no `qing_mongol_jasagh` marker
or 1:1-trigger change is needed (v1's B2 was designed for the wrong — owned-land — model).

### B3 — Subject type + Lifan Yuan supervision
- Bind each league to Qing with `dependency = { first = CHI second = <league> subject_type = X }`.
  Candidate subject_type: `feudatory` or `autonomous_governorship` (real administrative
  subordination, on the annexation ladder), OR a dedicated Mongol-banner subject type if the
  existing ones do not fit the "hereditary fief under investiture, cannot secede, joins overlord's
  wars" profile. Nested chains are proven viable (memory `nested-subjects-viable`), so a
  league→banner sub-subject layer is possible if desired later.
- The existing `qing_office_lifanyuan_holder` / `qing_min_perf_lifanyuan` meter then supervises
  these SUBJECTS (loyalty band, integration speed, succession confirmation) — mirroring the amban
  loyalty-band pattern (design/DESIGN_SUBJECT_INTEGRATION_ACTORS) — rather than governing owned land.

### B4 — Chahar stays Qing-owned (the real exception)
Chahar was directly-ruled Eight-Banner territory, so it stays Qing-OWNED and keeps a garrison
character (a 察哈爾都統, like the existing 綏遠城將軍/盛京將軍 banner generals in
imp19c_effects_legion_setup.txt) — NOT spun off as a subject. Only the jasagh-fief leagues convert.

## Why this is deferred, not done now (user call)
- B1 alone is a multi-tag territorial conversion (new tags + ownership transfer + core/de-jure
  cleanup + capital validity) — the highest-risk class of change in this codebase (boot crashes).
- B2 needs a dedicated 1763 jasagh/league-captain research pass.
- Option (a)'s real-official placeholder (char:674 蘊著) is correct-enough meanwhile, so nothing is
  blocked while (b) waits.

## Open questions for review
1. Which leagues to spin off, and at what granularity (per-league tags, or one "Inner Mongolia"
   tag, or nested league→banner sub-subjects)?
2. Which subject_type fits the jasagh-fief profile (existing feudatory/autonomous_governorship, or
   a new Mongol-banner type)?
3. Exact 1763 jasagh/league-captain rulers (needs the sourcing pass).
4. De jure / core handling so spun-off land is not a Qing reconquest target every campaign.
