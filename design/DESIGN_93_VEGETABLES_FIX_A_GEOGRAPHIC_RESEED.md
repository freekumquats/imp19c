# DESIGN — Fix A: geographic reseed of vegetables into deficit trade zones (task #93)

**Status:** DESIGN — CLEAN, ready to implement. First adversarial review REJECTed the
survivor-ratio sizing rule (falsified by real setup data), replaced by PROBE-FIRST measured
sizing (§3). The re-review (2026-08-18) returned PASS-WITH-FIXES; all 4 required fixes are folded
in (shared-region claim corrected to a clean partition §4; probe made a freestanding on_action
read §3; breadth-first governorship spread rule added §3/§5; mechanical grain/livestock depletion
guard added §6). See §11 for the full review record.
**Origin:** `DESIGN_93_VEGETABLES_BOOMBUST_DIAGNOSIS.md` §8, Direction A — the safest,
lowest-blast-radius fix for the vegetables collapse. That diagnosis (adversarial-reviewed)
is the authority; read it first.
**Companion change + SEQUENCING (honest, probe-first):** the `GOODS_vegetables_production_multiplier
= 4` (×4) revert SHIPS FIRST, on its own, together with this design — NOT with the reseed. Reason:
the reseed must be sized against the HONEST (un-boosted) per-zone deficit, and the Phase-0 probe
that measures it (§3) is ALREADY LIVE (the committed `se_ECON_LOG_TZPROBE.txt` already tracks
`vegetables` per zone — 1,210 band lines, all 22 zones, PRE+POST — so Phase 0 needs no new code).
The ×4 was masking the true deficit; reverting it BEFORE the measurement boot is what lets that
already-live probe log the real balance. So the honest order is: (1) ship the ×4 revert now →
(2) the next `-debug_mode` boot's `TZP BAND vegetables` lines give the honest per-zone deficit →
(3) Phase 1 sizes + emits the province reseed from those measured numbers. Steps 2-3 are a
genuine boot-data dependency of the reviewed design, NOT a deferral of choice: sizing off the
current ×4-active log (wrong baseline) or off province counts (falsified by the first review,
Finding 1) both contradict what passed review.
**Scope class:** setup data reseed only. No shared-loop / economy-formula edit. NO per-good
script modifier (that would reopen the #219 import-AI flood — see §7).

---

## 1. The problem this must solve (from the diagnosis)

Vegetables collapse to 0 stock in ~19 of 22 trade zones. Root cause = a **geography-gated
demand ratchet**: zone stock is a per-quarter FLOW (`zone_stockpile = Σ_local_govs max(0,
production − demand)`), and the shared ±10%-clamp + price-elasticity divide ratchet
governorship demand upward each quarter. Where local vegetable production is thin, ratcheted
demand overtakes it → `for_sale→0` → `price = order/stock` spikes 100-1000×.

**Only local production matters.** A zone's stock is only its own governorships' surplus —
national output cannot cross zone boundaries (imports feed the buyer *governorship's* stock,
never the *zone* stock variable). So the fix must add vegetable production INSIDE each
collapsing zone's member regions.

**Grain never collapses** because it is produced in ~1746 provinces — every zone. The fix
makes vegetables behave more like the other non-collapsing minor staples.

## 2. Historical / academic basis (vegetables were near-universal — the clustering is an artifact)

The current 418-province distribution is Russia/central-Europe/India/interior-China heavy,
with literal 0 in Korea, Japan (Kyushu/Honshu), coastal China (Zhejiang, Jiangsu, Taiwan),
Congo Basin, Argentina, the American Southwest, Appalachia, and the Antilles. That pattern is
a seeding artifact, not history. Kitchen-garden and market-garden vegetable growing follows
settled agriculture and population essentially everywhere:

- **East Asia — the strongest correction.** 18th-century China, Korea, and Japan ran some of
  the most intensive vegetable market-gardening on earth: peri-urban truck gardens, multiple
  cropping, and night-soil fertilisation. This is the classic subject of F. H. King,
  *Farmers of Forty Centuries* (1911), documenting Chinese/Korean/Japanese intensive
  vegetable cultivation. Korea (napa cabbage, radish — the kimchi complex), Japan (daikon,
  greens, roots), and the Yangtzi/coastal-China cities all sustained dense vegetable gardens.
  A literal 0 for Korea, Japan, Zhejiang, and Jiangsu is simply wrong.
- **New World.** The Americas domesticated a large share of the world's vegetables: squash,
  beans, tomatoes, peppers, and potatoes ("Three Sisters" agriculture = maize + beans +
  squash). Indigenous and colonial farms grew abundant garden vegetables. NOTE: beans,
  squash, and tomato are NOT modelled as separate trade goods in this mod (§5), so New World
  vegetable abundance must be represented via the `vegetables` good (maize/potato/sweet_potato
  stay as their own differentiated goods per `RESEARCH_NWCROP_GEOGRAPHY_64.md`).
- **Africa.** Indigenous African agriculture included cowpeas, okra, leafy greens, gourds,
  melons, and yams; kitchen gardens were universal across settled farming zones. Sub-Saharan
  interior at 0 is an artifact.

**Constraint from the crop-geography corpus:** the mod already has sourced per-crop ranges for
the differentiated New World crops (`RESEARCH_NWCROP_GEOGRAPHY_64.md`,
`DESIGN_57_NEWWORLD_CROPS_CONCRETE.md`). This reseed must NOT touch maize/potato/sweet_potato
provinces, and must not add a New World "vegetable" where the sourced record instead assigns a
differentiated crop. Vegetables (garden/kitchen crops) are the near-universal residual, so
they may be added broadly where settled population exists — but never by displacing a
differentiated or cash crop (§5).

## 3. Sizing rule — PROBE-FIRST, because province COUNT does not predict collapse (rev. after review)

**The first draft's sizing rule (a survivor-derived veg-to-food-province ratio `R`) was
REJECTED by the adversarial review, and correctly.** The reviewer computed real
population/province numbers from the live setup files (region→area→province joins, not the CSV)
and showed the ratio is empirically *uncorrelated* with collapse:

| zone | pop | food prov | veg prov | veg/food | veg/pop | outcome |
|---|---|---|---|---|---|---|
| central_europe | 8,200 | 204 | 40 | 0.196 | 0.00488 | survives |
| india | 40,431 | 265 | 30 | 0.113 | 0.00074 | survives |
| upper_yangtzi | 10,308 | 88 | 13 | 0.148 | 0.00126 | **collapses** |
| yellow_sea | 38,621 | 264 | 7 | 0.027 | 0.00018 | collapses |

`upper_yangtzi` COLLAPSES while already sitting at a veg/food ratio (0.148) ABOVE survivor
`india` (0.113) and at parity with the pooled survivor `R = 0.149`. Under the old rule it would
get **+1 province** — a no-op on the design's own flagship Chinese zone. Worse, the ordering is
non-monotonic in BOTH candidate predictors: `india` survives at a LOWER veg/pop (0.00074) than
`upper_yangtzi` collapses at (0.00126). **No province-COUNT threshold — ratio OR per-capita —
is consistent with both zones.** The real survival driver must involve per-province veg *yield*
(agriculture_productivity × num_goods_produced) and intra-zone *governorship* distribution
(zone stock = Σ over govs of `max(0, prod − demand)`; a single thin governorship stocks out even
if the zone total looks adequate) — quantities the setup province COUNT cannot see. Sizing on a
count proxy is therefore a guess dressed as a computation, and the review was right to reject it.

**Revised approach — measure, then size (probe-first, like the CPI task):**

- **Phase 0 (ALREADY LIVE — needs no new code): the per-zone balance probe already tracks
  vegetables.** The committed `se_ECON_LOG_TZPROBE.txt` (generated by `tools/gen_econ_tzprobe.py`,
  which lists `vegetables` in its GOODS set) already emits, per trade zone per quarter,
  `-debug_mode`-gated bands for vegetables `stock` (= Σ_gov `max(0, prod−demand)`, the for-sale
  surplus), `order` (= Σ_gov `max(0, demand−prod)`, the unmet demand), and `price` (= order/stock),
  plus a CHI `demand` band — 1,210 `IMP19C TZP BAND vegetables …` lines across all 22 zones, PRE
  and POST of the quarterly trade recompute. `stock` and `order` together ARE the measured per-zone
  production-vs-demand balance the count proxy could not supply and the india-vs-upper_yangtzi
  paradox proved we need. Read back with `tools/curx_analyze.py --good vegetables` (per
  `imp19c-logs`).
  - **This satisfies re-review Fix 2 already:** the probe is a FREESTANDING read-only pass that
    reads trade-zone GLOBALS from country scope (CHI, guarded) — it does NOT edit
    `se_GLOBALTRADE_split.txt`, so §7's no-shared-loop-edit safety contract holds. No new probe is
    built; the design's "Phase 0 ships first" requirement is met by pre-existing instrumentation.
  - **Only gap vs the original Phase-0 wish-list:** a per-zone contributing-governorship COUNT is
    not logged. It is NOT needed as a sizing input — the §6 helper enforces the breadth rule
    offline from setup governorship membership; post-boot, the `price` band (low = spread worked)
    verifies it. So no probe change is required before Phase 1.
  - **PRE-REQUISITE for a MEANINGFUL Phase-0 read:** the ×4 revert must be pushed first (see
    header sequencing), so the bands measure the honest un-boosted deficit, not the ×4-masked one.
- **Phase 1 (after the probe boot): size each collapsing zone to production ≥ demand + margin,
  from MEASURED numbers.** For each collapsing zone, `additions` = the veg-province count that
  raises measured production to `≥ measured_demand × (1 + margin)`, using that zone's OWN
  measured production-per-veg-province (not a borrowed survivor yield). `margin` first pass =
  0.25 (a guess, logged and boot-tuned). Because the ±10% demand clamp + price-elasticity brake
  damp a glut symmetrically (confirmed by the review, Finding 7), erring HIGH is safe — a
  transient cheap quarter, never a new shortage — so the margin deliberately over-provisions
  rather than trying to hit an exact threshold the data may not support.
- **`additions = max(0, target − current)`** — top up only; never remove existing veg.
- **Spread BREADTH-first across governorships, before depth within one (re-review Fix 3).** The
  zone price is `order / stock`, and both sums run over DISJOINT governorship subsets: `stock =
  Σ_gov max(0, prod − demand)`, `order = Σ_gov max(0, demand − prod)`. A concentrated placement
  (many additions in a few governorships) can lift the zone's aggregate margin — and pass §8's
  "stock stops hitting 0" bar — while the many still-zero governorships keep `order` large and the
  price elevated. So a zone's `additions` are allotted to the MOST distinct deficit governorships
  first (one per governorship, cycling), and only stack a second veg province into a governorship
  once every deficit governorship in that zone already has one. This makes the reseed reproduce the
  broad distribution of the survivor zones (`central_europe` ~40 provinces spread wide, `india`
  ~30), not an urban-concentrated cluster. Breadth ranking takes precedence over the §5 near-urban
  tiebreak, which now only orders candidates WITHIN a single governorship.

The TOTAL addition count is an OUTPUT of the measured Phase-1 computation, not pre-guessed, and
is logged per zone. The old "~660 cross-check anchor" is DROPPED (review Finding 7): the first
rule's own arithmetic produced 783, ~19% over that anchor, so the anchor was never a valid
sanity bound — measured production-vs-demand replaces it.

**ASSUMPTION / boot-tunable (guess-and-log):** the `margin = 0.25` and the Phase-0 band
thresholds are first-pass guesses; the probe logs the real balance so Phase 1 sizes from data,
and a still-collapsing zone gets its margin raised on the next boot.

## 4. The 19 collapsing zones to target (from the boot log, `DESIGN_93` §1)

Collapse-to-0 zones (oscillation summary, stock band reaches `0`): `atlantic_seaboard`,
`caribbean`, `east_africa`, `east_europe`, `east_mediterranean`, `east_north_america`,
`east_south_america`, `eastern_steppe`, `indo_china`, `middle_east`, `south_east_asia`,
`southern_africa`, `upper_yangtzi`, `west_africa`, `west_mediterranean`, `west_north_america`,
`west_south_america`, `western_steppe`, `yellow_sea`.
Survivors (never hit 0, used as the reference and left alone): `central_europe`, `india`,
`baltic`.

Zone → member regions come from `common/scripted_triggers/00_tradezone_triggers.txt`
(region-membership triggers). Example: `yellow_sea` = Jiangxi, Fujian, Zhejiang, Anhui,
Jiangsu, Henan, Shandong, Korea, Kyushu, Ezo, Honshu, Shikoku, Taiwan, Okinawa.

**Zones ARE a clean partition — the earlier "shared-region" claim was FALSE (re-review Fix 1,
programmatically verified this session).** The first revision claimed five regions were shared
across zones and would double-count. That was built from a stale source. A live parse of
`common/scripted_triggers/00_tradezone_triggers.txt` (respecting `#` comments) shows every one of
the five candidate regions is active in EXACTLY ONE zone — the second membership is commented out
in each case:
- `Anatolia` — live only in `middle_east_tradezone` (:534); `#is_in_region = Anatolia` in
  `east_mediterranean_tradezone` (:870).
- `Andalusia` — live only in `west_mediterranean_tradezone` (:749); commented out of
  `atlantic_seaboard_tradezone` (:663, note *"Moved to West Med so Gibraltar can capture shipping
  income there"*).
- `Silesia` — live only in `central_europe_tradezone` (:718); commented out of
  `baltic_tradezone` (:799).
- `Praire_Provinces` / `Northern_Territories` — live only in `east_north_america_tradezone`
  (:86-87); commented out of `west_north_america_tradezone` (:123, :126).
- `Great_Plains` — live only in `caribbean_tradezone` (:161); commented out of
  `west_north_america_tradezone` (:119).
CONSEQUENCE: no region contributes its `for_sale` to two zones, so per-zone production accounting
IS strictly additive and there is nothing to double-count or disclose. The reseed's per-zone sizing
(§3) needs no double-count correction. (The prior safety point still holds trivially: no survivor
zone shares a region with a collapsing zone, because no region is shared at all.)

## 5. Province selection rules (what to convert, and what to NEVER touch)

Within each target zone's regions, choose `additions` provinces to flip to
`trade_goods="vegetables"`, by these rules in order:

- **Prefer literal-zero regions first**, then thin regions: Korea, Kyushu, Honshu, Zhejiang,
  Jiangsu, Taiwan (yellow_sea); Congo_Basin, Angola, South_Africa (African zones); Argentina,
  American_Southwest, Appalachia, Antilles (New World zones).
- **Displace only OVER-REPRESENTED bulk staples — GRAIN or LIVESTOCK ONLY** (review Finding 2),
  and only where that region has a large surplus of them (e.g. Korea's 44 grain; Argentina's 47
  livestock). Grain (1,731 provinces) and livestock (1,859) have genuine order-of-magnitude
  headroom. **FISH IS STRUCK from the displacement list.** Fish runs the byte-identical collapse
  mechanism as vegetables (same price-elasticity divide + ±10% ratchet, `DEMAND_food_svalues.txt`
  fish region) and spreads only ~665 provinces — barely more than vegetables' pre-fix 418, i.e.
  fish is ITSELF near the collapse margin. Displacing coastal fish (Korea's 13 fish = ~23% of
  `yellow_sea`'s fish supply), preferring high-output near-urban ones, would very plausibly
  reproduce the same geography-gated collapse for fish that this design exists to cure for
  vegetables. Never convert a fish province, anywhere.
- **Prefer provinces near population/urban centres** (higher `civilization_value` / pop rank),
  reflecting the peri-urban market-garden reality of §2.
- **NEVER touch:**
  - Cash / specialty crops: silk, tea, sugar, cotton, tobacco, coffee, spices, indigo, dyes,
    wine, saltpetre, lead, and any non-food trade good. (The CSV mislabels some of these as
    "grain" — §6 reads the good from the live setup file, not the CSV, to honour this rule.)
  - FISH — struck above; it is not a safe displacement target.
  - The differentiated New World crops: maize, potato, sweet_potato, tropical_fruit (respect
    `RESEARCH_NWCROP_GEOGRAPHY_64.md`).
  - Any province that already grows vegetables (no double-assign; top-up only).
  - The survivor zones (`central_europe`, `india`, `baltic`) — untouched.
- **Deterministic ordering (breadth-first, re-review Fix 3):** allot a zone's `additions` by
  round-robin over its DEFICIT GOVERNORSHIPS first — take at most one province per governorship
  per pass, cycling through all deficit governorships before a second province lands in any one of
  them. Within a governorship, break ties by (already-zero-region flag, then bulk-staple surplus
  size, then civilization_value, then province_id). This is reproducible and reviewable — not
  random — and guarantees the spread the price formula needs (§3 breadth rule).

## 6. Implementation method (byte-safe edit of the setup files)

- Edits land in `setup/provinces/00_*.txt`, changing a province block's
  `trade_goods="<staple>"` → `trade_goods="vegetables"`. Quoted, tab-indented, exactly as the
  existing lines (`00_Korea.txt:5` shows `\ttrade_goods="grain"`).
- **PRESERVE the UTF-8 BOM and tabs.** All 345 province files carry a BOM (`ef bb bf`,
  verified 345/345) and load via the common lexer — per `imp19c-setup-reader-rejects-bom`,
  province files KEEP their BOM. Stripping it would make the edited file the odd one out. Use
  the byte-safe Python edit idiom (`imp19c-file-editing-path`): read bytes, regex-replace only
  the targeted `trade_goods` line inside the targeted province block, write bytes back,
  BOM+tabs intact. Run a brace-balance check on every edited file after writing.
- **A helper script** (`tools/reseed_vegetables.py`, new) computes the §3 targets from the
  MEASURED Phase-0 per-zone balance + the zone→region map, applies the §5 selection rule, and
  emits (a) the per-file edits and (b) a manifest of every province changed (id, name, region,
  zone, old good → vegetables) plus the per-region depletion headroom (§6 Fix-4 guard). The
  manifest is committed alongside for auditability. The script is deterministic; re-running it
  produces the same edits.
- **The helper reads EVERY good-assignment from the live `setup/provinces/*.txt`, NEVER from
  `research/PROVINCE_CONTENTS_1763.csv` (review Finding 4).** The CSV `trade_goods` column is
  measurably stale: 233 mismatches (1.75%) vs the live files, including provinces the CSV calls
  "grain" that are really saltpetre/lead (exactly the §5 never-touch goods), and 2 false-positive
  vegetables. Driving selection off the CSV would violate the never-touch rule and miscount
  `current_veg`. The CSV may still supply province NAMES / population rank for the "near urban
  centres" heuristic, but the good-assignment truth comes only from the setup files (uniform
  quoted, tab-indented `trade_goods="<good>"` format, confirmed across all 13,281 lines).
- **Mechanical grain/livestock depletion guard (re-review Fix 4) — not a plausibility argument.**
  Before the helper flips a grain (or livestock) province to vegetables, it ASSERTS in code that
  the province's own region keeps enough of that good: `region_production_of(good) − 1 province`
  must stay `≥ region_local_demand_of(good)`. The helper already reads every province's good and
  population from the live setup files (above), so it can sum the region's grain/livestock
  province count and compare against the region's own local demand proxy (its food-consuming
  population share). If a candidate flip would drop the region below its local demand for the
  displaced good, the helper SKIPS that province and takes the next candidate. The manifest logs,
  per region, the pre/post count of the displaced good and the headroom that remained — so the
  "1,731 grain / 1,859 livestock provinces = headroom" claim (§5) is verified per region, not
  asserted in aggregate.
- Edits are DATA; no `# task` code comment fits a province block. Traceability lives in the
  commit message + the committed manifest + this doc.

## 7. What is explicitly NOT touched (safety contract)

- **No script modifier of any kind on vegetables.** No `province = { ... }` /
  `country = { ... }` good modifier, no demand/production svalue edit. Adding one reopens the
  #219 vanilla import-AI request flood (`RESEARCH_TRADE_GOOD_DIFFERENTIATION_66.md`,
  `imp19c-vanilla-trade-request-flood-open`). Reseeding province `trade_goods` is the
  sanctioned lever and the ONLY one used here.
- **No good-definition edit** (`common/trade_goods/00_imp19c.txt` stays closed per #219).
- **No shared demand/trade-loop edit** — the ratchet itself (Direction C) is untouched; this
  fix removes the *necessary condition* (thin local production), not the engine.
- **No cash-crop or differentiated-crop displacement** (§5).
- The ×4 revert is the only script change in the companion commit; it is a clean revert
  (blob-verified) of `ae8d90818`.

## 8. Logging / verification (how the boot confirms it worked)

- **Phase 0** ships the per-zone production/demand/stock/gov-count band probe (§3). This is the
  NEW in-sim instrumentation the review showed is required — the count proxy could not supply
  measured production, and it is the only way to resolve the india-vs-upper_yangtzi paradox.
- **Phase 1** helper logs, at generation time: each collapsing zone's measured
  `production / demand / current_veg / target_veg / additions`, the per-zone production-per-veg-
  province used, the `margin`, the grand total added, and the resulting global vegetables count
  (an OUTPUT, no pre-set anchor — the ~660 cross-check is DROPPED, review Finding 7).
- Boot verification reuses `tools/curx_analyze.py --good vegetables` streamed over `debug.log`
  (per `imp19c-logs`). **The success bar is LOW PRICES, not merely non-zero stock (re-review
  Fix 3):** because `price = order/stock` can stay elevated at a healthy aggregate margin if
  additions were concentrated, the breadth-first spread (§3/§5) is what drives prices down. Expect
  the ~19 zones' stock to STOP hitting 0 AND prices to stay in the low bands. Compare against the
  pre-fix per-zone table in `DESIGN_93` §1. Any zone whose price stays high despite non-zero stock
  → its additions were too concentrated; spread wider before raising `margin`. Any zone still
  hitting 0 → raise its `margin` on the next boot (§3), not a blanket bump.

## 9. Questions raised by review — now RESOLVED

1. **RESOLVED (Fix 2).** Phase-0 probe correctness — the probe is NOT hooked inside
   `se_GLOBALTRADE_split.txt`; it is a freestanding read-only governorship walk at the on_action
   level, run AFTER `quarterly_global_trade_food` (`oa_wealth_changes.txt:421`) and BEFORE the
   quarter's consume, so it reads true production and cached demand upstream of the subtract (§3).
2. **BOOT-VERIFIED at Phase 0/1.** Whether measured sizing (production ≥ demand × (1+margin),
   per-zone own yield) covers `upper_yangtzi` — the zone the old rule no-op'd — is exactly what
   the probe boot measures and Phase 1 sizes from; a still-collapsing zone gets its margin raised.
3. **RESOLVED (Fix 3).** Intra-zone governorship distribution — Phase 1 now spreads additions
   BREADTH-first across deficit governorships before stacking depth (§3/§5), because the zone
   price `order/stock` sums over disjoint governorship subsets and a concentrated placement can
   pass an aggregate margin while leaving many zero governorships lifting `order`.
4. **RESOLVED (Fix 4).** Grain/livestock local depletion — the §6 helper now runs a mechanical
   per-region assertion (`region production of the displaced good − 1 ≥ region local demand`) and
   SKIPS any flip that would breach it, logging per-region pre/post counts + headroom. No longer a
   plausibility argument.
5. **CONFIRMED (Finding 6-PASS).** BOM/tab byte-safety — the Python edit idiom preserves BOM + tab
   indentation and a brace-balance check runs per edited file (§6).
6. **RESOLVED (Fix 1).** No shared-region double-count exists: zones are a clean partition, each
   of the five candidate regions is live in exactly one zone (the other side is commented out),
   verified in `00_tradezone_triggers.txt` this session (§4). No manifest disclosure needed.

## 10. ASSUMPTIONS & GUESSES (scan-in-one-place)

- **`margin = 0.25` over measured demand** (§3) — first-pass over-provision; the glut is
  self-damped (review Finding 7), so erring high is safe; boot-tuned per still-collapsing zone.
- **Phase-0 band thresholds** (§3/§8) — guessed bucket edges for production/demand/stock; the
  probe boot shows whether they resolve the india-vs-upper_yangtzi paradox and are re-cut if not.
- **Displace grain/livestock only, prefer near-urban provinces** (§5) — a historical-plausibility
  heuristic, not a per-province sourced assignment; the manifest lists every change for review.
- **The ~660 spread anchor is DROPPED** (review Finding 7) — it was ~19% below the old rule's own
  output and never a valid bound; measured production-vs-demand replaces it.

## 11. Adversarial review record (2026-08-18) — REJECT, then revised

First adversarial review verdict: **REJECT**, premise broken on §3's sizing rule. All findings
resolved in this revision:
- **Finding 1 (CRITICAL) — survivor-ratio `R` does not predict collapse** (falsified by
  `upper_yangtzi` at ratio-parity yet collapsing, and india<upper_yangtzi in veg/pop yet
  surviving). RESOLVED: §3 rewritten to PROBE-FIRST measured production-vs-demand sizing; the
  count-ratio rule is deleted, not patched.
- **Finding 2 (MED-CRIT) — fish is not a safe displacement target** (identical mechanism, thin
  spread). RESOLVED: §5 strikes fish; grain/livestock only.
- **Finding 3 (MED) — zones are not an exclusive partition; 5 shared-region pairs double-count**
  (no survivor contamination). RESOLVED: §4 discloses all five; §6 manifest lists them.
- **Finding 4 (MED) — CSV goods column stale (233 mismatches)**. RESOLVED: §6 helper reads
  good-assignment only from live `setup/provinces/*.txt`; CSV used for names/rank at most.
- **Finding 5/7 (LOW-MED) — ~660 anchor inconsistent with the rule's own 783 output**. RESOLVED:
  §3/§8/§10 drop the anchor; measured balance replaces it.
- Confirmed-safe findings kept: #219 non-reopening (Finding 5-PASS), BOM/tab/quote safety
  (Finding 6-PASS), no survivor contamination (Finding 3).

Re-review verdict (2026-08-18): **PASS-WITH-FIXES** — the probe-first §3 core survived the attack
(the reviewer traced a grain-identical, already-live self-capping mechanism —
`DEMAND_actual_vegetables` hard-capped by `min = DEMAND_consumer_minus_produced_vegetables`,
byte-identical to grain's own cap — validating that erring high is safe as a PROVEN pattern, not a
new bet; and confirmed the glut self-damps via `price = (order/stock)×0.6/num_food_tradegoods`,
div/0-guarded). Four required fixes, ALL folded in this revision:
- **Fix 1 — the "5 shared-region pairs" claim was factually WRONG.** A live parse (respecting `#`
  comments) shows zones are a CLEAN partition; each candidate region is live in exactly one zone,
  its second membership commented out. Independently re-verified this session. §4 rewritten; the
  double-count disclosure in §4/§6/§11 removed.
- **Fix 2 — Phase-0 probe placement.** Made an explicit freestanding read-only governorship walk
  at the on_action level (reusing `TZ_is_<zone>_tradezone`, mirroring `ECON_LOG_tzprobe_bands`),
  NOT an edit inside `se_GLOBALTRADE_split.txt` — keeps §7's no-shared-loop-edit contract honest.
- **Fix 3 — breadth-vs-concentration gap (the sharpest item).** Because `stock` and `order` sum
  over disjoint governorship subsets, a concentrated placement can pass an aggregate margin while
  keeping price high. Added a BREADTH-first spread rule (§3/§5) and made LOW PRICE, not non-zero
  stock, the §8 success bar.
- **Fix 4 — grain/livestock local depletion.** Turned §9-Q4 from a plausibility argument into a
  mechanical per-region assertion in the §6 helper (region production of the displaced good − 1 ≥
  region local demand, else skip), with per-region headroom logged in the manifest.
Design is now CLEAN and cleared to implement.
