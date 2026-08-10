# DESIGN — New World food-crop demand fix (#62): remove the spurious luxury double-count

**Status:** implementation design, 2026-08-10. Standalone correctness fix, split out of #52 (NOT luxury-pricing; NOT gated on the luxury probe/export research). Full pipeline: this design → adversarial review → implement → cross-country verify boot. Do NOT implement until reviewed.

## The defect (verified in source, NOT the category field)
The 5 New World crops (maize/sweet_potato/potato/peanut/chili) were fork-added by us (commit f45c9ce7b, 2026-07-05, "#64-fix") to unblock a parse crash, CLONED from the tobacco archetype → all got `category = 2` incidentally.

**My initial premise (reclassify category 2→1) was WRONG — verified:** the luxury-vs-staple demand split is NOT driven by the trade-good `category` field. Proof: category-1 holds grain/salt/fish (staples) AND spices/chocolate (luxuries); category-2 holds tea/coffee (luxuries) AND maize/potato. The demand system never reads `category`. The real driver is two EXPLICIT HARDCODED CALL-LISTS in se_DEMAND.txt:
- `DEMAND_set_demand_from_food_all` (~line 36) — the STAPLE/food basket (grain, livestock, temperate_fruit, vegetables, processed_foods, fish + conditionally-produced New World crops).
- `DEMAND_set_demand_from_luxury_all` (~line 605) — the 18-good LUXURY basket.

**THE ACTUAL DEFECT — a DOUBLE-COUNT (verified by cross-referencing both blocks):**
| crop | in FOOD block | in LUXURY block |
|---|---|---|
| maize | YES | YES |
| potato | YES | YES |
| sweet_potato | YES | YES |
| peanut | NO | YES |
| chili | NO | YES |

maize/potato/sweet_potato are demanded as BOTH food staples AND luxuries simultaneously — a spurious double-count inherited from the tobacco-clone. The food-side registration is already CORRECT + historically right (conditional on `GOODS_governorship_<crop>_produced > 0`, the `[#279]` guard). The luxury-side call is the leftover error.

## The fix (surgical — remove the luxury call, NOT a category edit)
1. **REMOVE maize / potato / sweet_potato / peanut from `DEMAND_set_demand_from_luxury_all`** (se_DEMAND.txt). This kills the spurious luxury demand. The EXACT precedent is the `[#281] rifles removed from the pop luxury basket` comment already in this block — rifles was pulled from the luxury basket the same way when its demand became military. Mirror that: remove the `DEMAND_set_demand_from_luxury = { tradegood = <crop> }` lines + a `[#62]` comment explaining why (subsistence food, not luxury; was a tobacco-clone artifact).
2. **ADD peanut to `DEMAND_set_demand_from_food_all`** — it's a subsistence food crop but is currently ONLY in the luxury block (not the food block). After removing it from luxury, it would have NO demand path unless added to food. Add it with the same `GOODS_governorship_peanut_produced > 0` conditional guard + bump the `DEMAND_food_goods_count` base/increment logic to count it (mirror the maize/potato/sweet_potato conditional increments at food_all:52-66). (maize/potato/sweet_potato are already in food, so removing them from luxury leaves them correctly food-only — no add needed.)
3. **chili: LEAVE as luxury-only.** It's a condiment/flavour good, not a bulk subsistence staple — genuinely closer to a luxury/spice than a calorie crop. It stays in the luxury basket, out of food. (If later wanted as food, that's a separate call.)
4. **`category` field: DO NOT TOUCH.** It doesn't drive demand (proven above). Leaving maize at category=2 is harmless for the demand fix. (A separate cosmetic-consistency question — is category=2 right for a food crop? — is OUT of scope for #62; the demand double-count is the actual bug.)

## Why this is better than the category-reclassify I first proposed
- Surgical: 4 line-removals + 1 food-add + count-bump, in ONE file (se_DEMAND.txt), vs editing the trade-good category scheme.
- Uses the PROVEN in-file precedent (`[#281]` rifles removal).
- Fixes the REAL defect (double-count → double demand → distorted orders for these crops), which a category edit would NOT have fixed (it would have done nothing to demand).
- The food-side path is already correct + historically guarded (#279), so we're removing an error, not adding new machinery.

## GATE / RISK (its own verify, NOT the luxury gates)
- **GLOBAL:** the demand baskets are read by EVERY country's governorships. Removing maize/potato/sweet_potato/peanut from luxury demand changes their demand for every country that grows them (the Americas, Europe, China). Verify cross-country.
- **Verify boot must confirm:** (a) maize/potato/sweet_potato/peanut now generate ONLY food demand (no luxury demand) — check the demand series; (b) their price/order behaviour is sane (no crash to zero-demand → dead good, no phantom shortage — the #279 conditional-on-production guard should hold); (c) they still feed the state food pool (local_monthly_food byproduct intact); (d) #384 crop-diffusion + #78 pop-boom (key off crop provinces) unaffected; (e) the food-shortage/famine path counts them correctly (they ARE food); (f) no country's economy destabilizes; (g) peanut, newly in the food basket, behaves like the other subsistence crops.
- **Extend the probe:** the #52 full-tier probe (or a small dedicated one) should log maize/potato/sweet_potato/peanut demand BOTH before + after so the double-count removal is measurable.

## Files
- common/scripted_effects/se_DEMAND.txt ONLY — remove 4 luxury-basket calls; add peanut to the food basket + its count-increment. NO trade_goods/ category edit. NO province_setup.csv. NO plumbing files.

## Traps / rules
- se_DEMAND.txt BOM/EOL convention — check before editing.
- The `[#279]` food-basket count logic (DEMAND_food_goods_count) must stay consistent — adding peanut means the count base/increments must include it, or the divisor is wrong (the #279 review-fix bug: interleaved count vs demand → over-demand). Count peanut in the SAME conditional-increment style.
- `[#219]` two-trade-systems flood caution: demand is a shared layer, but this is svalue-list editing (not province/country blocks), so flood-safe.
- Do NOT confuse raw `silk` etc. — this task is ONLY the 5 New World crops.
- Design-note-first → adversarial review → implement → cross-country verify boot. freekumquats/merge-overnight.

## Verify (cross-country boot)
- maize/potato/sweet_potato/peanut: luxury demand = 0 (removed), food demand present where produced; price/orders sane; no phantom shortage.
- State food pool + famine path still correct; #384/#78 unaffected.
- Sample the Americas / Europe / CHI — no economy destabilized.
- chili unchanged (still luxury-only).

---

## ADVERSARIAL DESIGN-REVIEW CORRECTIONS (2026-08-10) — "do NOT implement as written"; scope was wrong
Diagnosis (double-count) CONFIRMED correct, but the FIX under-delivers + is under-scoped. Corrections supersede the fix/files sections above:

**C1 [CRITICAL] — removing a crop from the call-list does NOT zero its luxury demand.** The Total svalues that drive orders/prices (DEMAND_maize/potato/sweet_potato/peanut in DEMAND_luxury_svalues.txt L325/480/534/588) are structured `if has_variable DEMAND_luxury_<crop> { value=var } else { value = DEMAND_luxury_base_total }`. DEMAND_set_demand_from_luxury is the ONLY writer of that var → remove the call → var never written → the Total takes the `else` = DEMAND_luxury_base_total (a NONZERO wealth-weighted base, L88-100), NOT zero. So my "luxury demand = 0" success criterion FAILS on boot; the call-list edit only removes the price/wealth MODULATION, could even RAISE demand in some governorships. This is the headline defect.

**C2 [CRITICAL] — the [#281] rifles precedent was NOT a call-list-only removal.** Rifles was removed from the call-list AND its Total svalue was rewritten to `value = DEMAND_rifles_base` with NO `else = DEMAND_luxury_base_total` fallback (L473-478). It works because the whole demand basis was replaced. The 4 crops have no such replacement → mirroring the precedent FAITHFULLY means editing the Total svalue too — which my "se_DEMAND.txt ONLY" scope forbade. The precedent contradicts my scope.

**H1 [HIGH] — the fix must edit DEMAND_luxury_svalues.txt (wrong file scoped).** For maize/potato/sweet_potato (which already fold in food demand, e.g. maize L368-371 `if has_variable DEMAND_food_maize add var`), rewrite each Total svalue FOOD-ONLY: drop the luxury var seed + the `else=base` so the value builds purely from var:DEMAND_food_<crop>. Then the call-list removal is consistent dead-writer cleanup. Call-list edit alone is INSUFFICIENT.

**H2 [HIGH] — peanut has NO food path at all; the food-add is multi-file.** No DEMAND_food_peanut svalue exists (per-good food svalues live in DEMAND_food_svalues_new.txt; only maize/potato/sweet_potato have them), and DEMAND_peanut Total (L588-632) has no `add var:DEMAND_food_peanut` fold-in. So giving peanut a food path requires: (a) author DEMAND_food_peanut in DEMAND_food_svalues_new.txt (clone maize); (b) add the food fold-in to DEMAND_peanut Total; (c) add peanut to the food_all calls + count-increment; (d) remove from luxury. Multi-file.

**H3 [HIGH, UNRESOLVED] — export/cash-crop dead-good risk NOT verified.** The crop-geography sub-agent never returned. Concrete risk: under a food-only rewrite (H1), the food path is production-GATED at the producer (M1), whereas luxury demand was UNIVERSAL — so a region that grows a crop as pure EXPORT (not local subsistence) could see collapsed internal demand + a producing exporter needs buyers. MUST verify which tags grow maize/sweet_potato/potato/peanut as export cash crops vs Chinese subsistence BEFORE choosing food-only (H1) vs keeping a luxury floor. Currently UNRESOLVED — verify directly.

**M1 [MED] — asymmetric gating (the key behavioral consequence).** Luxury call = EVERY governorship unconditionally; food call = ONLY where GOODS_governorship_<crop>_produced > 0. So a food-only rewrite makes NON-producing governorships get ZERO demand for these crops — arguably correct for a subsistence good, but it largely REMOVES worldwide baseline import demand for the 4 goods. Interacts with H3 (exporters need buyers). The single biggest econ-behavior change; must analyze + verify.

**M2 [MED] — famine-metric dilution.** DEMAND_num_food_goods (base 6 + produced NW crops) is the divisor for the famine metrics ECON_governorship_food_shortage/_physical (ECON_svalues.txt L418/442) whose numerators sum only the 6 base staples → each produced NW crop already DILUTES the famine metric (less famine) in producing regions; adding peanut to the count extends this. Undocumented side effect of the count-increment; flag for verify.

**M3 [MED] — count-increment wiring CONFIRMED needed:** DEMAND_food_goods_count (se_DEMAND.txt L52-66) → DEMAND_num_food_goods svalue; peanut MUST get a `+1` conditional (GOODS_governorship_peanut_produced > 0) in the count block or every food good in a peanut region over-demands (#279 bug class).

**LOW:** L1 chili stays luxury-only (consistent, unaffected). L2 category left as-is (correct; demand never reads it; low-risk). L3 there are TWO luxury call-lists — DEMAND_set_demand_from_luxury_all (L605) AND DEMAND_set_demand_from_luxury_all_first_time (L643) — BOTH list the 4 crops; remove from BOTH or first-tick vs steady-state diverge.

## CORRECTED SCOPE + MINIMAL FIX (supersedes "se_DEMAND.txt ONLY")
THREE files minimum: se_DEMAND.txt (call-lists x2 + count) + DEMAND_luxury_svalues.txt (Total svalue food-only rewrites) + DEMAND_food_svalues_new.txt (new DEMAND_food_peanut).
1. maize/potato/sweet_potato: rewrite Total svalue food-only (drop luxury seed + else=base), remove from BOTH luxury call-lists.
2. peanut: RESOLVE H3 geography FIRST. If subsistence → author DEMAND_food_peanut + food fold-in + food_all call + count-increment + remove from luxury. If primarily EXPORT → keeping it in the luxury basket may be MORE correct; decide after geography.
3. chili + category: leave.
VERIFY: boot-confirm Total DEMAND_<crop> actually DROPS for a non-producing governorship (proves C1 addressed); peanut DEMAND_food_peanut written AND read (H2); M2 dilution acceptable; H3 exporters still have buyers; cross-country, no destabilization.
BLOCKER: H3 crop geography is UNRESOLVED — resolve before implementing.

---

## H3 RESOLVED (2026-08-10, direct from common/province_setup.csv) — crop geography, per-crop
Queried the province trade-good seeding. Producing provinces (region), which decides food-only vs keep-luxury per crop:
- **maize** — 6 provinces, ALL China (Hunan/Jiangxi). Subsistence, China-only. → FOOD-ONLY safe.
- **peanut** — 5 provinces, ALL China (Guangdong/Fujian). Subsistence, China-only. → FOOD path safe (build the DEMAND_food_peanut path per H2).
- **chili** — 6 provinces, ALL China (Hunan). → LEAVE luxury-only (unchanged).
- **sweet_potato** — 6 provinces: 4 China (Fujian/Guangdong) + **2 in Costa de Peru**. Mostly China; the 2 Peru provinces grow it → they get local food demand under a food-only rewrite, so probably fine, but WATCH (Peru could have been a modeled exporter).
- **potato** — 5 provinces: **ALL in the Americas (New Mexico, Peru-Atacama, Potosí) — ZERO in China.** This is the H3 dead-good case: potato is a foreign/import good for the Qing economy. A FOOD-ONLY (production-gated) rewrite → every NON-producer (incl. ALL of China) gets ZERO potato demand → potato becomes a DEAD GOOD outside the Andes.

REFINED FIX (per-crop, resolves the H3 blocker):
- maize, peanut: food-only (maize) / build food path (peanut) — China-only, safe.
- chili: leave luxury-only.
- sweet_potato: food-only OK (both China + its 2 Peru producers grow it, so both get food demand); verify the Peru provinces on boot.
- **potato: do NOT go food-only.** Since it's grown ONLY in the Americas and consumed (in this model) as a cheap import elsewhere, removing its luxury/universal demand would strand it. OPTIONS for potato: (a) LEAVE potato in the luxury basket (accept it stays a minor universal-demand good — least-risk, potato is genuinely a minor import for Qing anyway); or (b) give it a food path AND keep a small universal/import demand floor so non-Andean consumers still buy it. LEAN (a): leave potato as-is — it is NOT double-counted the way maize/potato... wait: potato IS in BOTH baskets per the double-count table, but it has NO Chinese production, so its FOOD-block entry only fires in the Andean producers; its LUXURY-block entry is what gives the rest of the world (incl. China) any potato demand. So removing potato from luxury would zero Chinese potato demand. => KEEP potato in the luxury basket (do not remove it); only maize/peanut/sweet_potato get the food-only treatment. Revisit if a domestic-potato mechanic is ever wanted.

NET: the fix is NOT uniform across the 4 crops. maize + peanut + sweet_potato → food-side (China-grown subsistence). potato → LEAVE in luxury (Americas-only production; food-only would kill Qing demand). chili → leave. This is the H3-informed correction; the "remove all 4 from luxury" plan would have made potato a dead good in China.

---

## H3 RE-OPENED — the crop GEOGRAPHY itself is broken (user, 2026-08-10)
RETRACTION: my "H3 resolved, potato is Americas-only → leave in luxury" verdict was reasoning off BROKEN seed data. Checked BOTH province sources (common/province_setup.csv + setup/provinces/*.txt) — the counts are the same tiny numbers, and they are AHISTORICAL:
- maize: 6 provinces total worldwide, ALL in China (Hunan/Jiangxi) — ZERO in the Americas. (In 1763 maize was THE staple grain of the entire Western Hemisphere.)
- chili: 6, ALL Hunan. peanut: 5, ALL China (Guangdong/Fujian). sweet_potato: 4 China + 2 Peru. potato: 5, all Americas.
- American regions (American Southwest, Appalachia, Antilles, Argentina) grow livestock/grain/wood/tobacco/sugar — essentially NO maize/peanut/chili despite being the crops' homeland.
=> The mod seeds the New World crops almost entirely in CHINA (their novel 18thc diffusion frontier) and barely in the AMERICAS (their actual origin). This is BACKWARDS from the real 1763 distribution.

CONSEQUENCE — the demand fix (#62) must NOT be built on this broken geography:
- My per-crop food-only/leave-in-luxury verdicts were derived from where the crops are CURRENTLY (wrongly) grown. They are unreliable until the geography is fixed.
- Specifically the "potato is Americas-only, leave it in luxury" logic is an ARTIFACT of the broken seeding (potato happens to be the ONE crop seeded in the Americas), not a real design conclusion.

SPLIT INTO TWO TASKS:
1. #62 (this task) — the DEMAND double-count (maize/potato/sweet_potato in both food+luxury baskets). Still a real, separate bug in the demand svalues. But its per-crop food-only-vs-luxury decision should be REVISITED after the geography is fixed (or made robust to either geography). HOLD #62's final lever choice until the seeding task lands.
2. NEW TASK — seed the New World crops into their real 1763 AMERICAN ranges (maize across Mesoamerica/N.America/Andes fringe, peanut+chili across the Americas, potato Andean-core, etc.), correcting the backwards distribution. This is a map/setup content task (province_setup.csv + setup/provinces/*.txt), separate from the demand plumbing.
#62's demand fix depends on #new (get the geography right first, THEN decide each crop's food-vs-luxury demand on correct producer distribution).

---

## FINAL RESOLUTION (2026-08-10) — re-derived on the CORRECTED geography (#64 committed a3865a251)
#64 landed: the crops now grow in their real ranges. Re-deriving each crop's food-vs-luxury lever on the CORRECTED producer distribution, and grounded in the actual demand mechanic:
- **Mechanic (verified):** the LUXURY call-list (se_DEMAND.txt:618-627 steady + :655-664 first-time) applies UNIVERSAL demand (every governorship demands the good regardless of production); the FOOD call-list (:97/:102/:107) is PRODUCTION-GATED (fires only where `GOODS_governorship_<crop>_produced > 0`, and the count block :56-64/:96-106 bumps DEMAND_num_food_goods per produced crop). The double-count = maize/potato/sweet_potato appear in BOTH.
- **Corrected producer geography:** maize 18 Americas + 6 China; peanut 6 Americas + 3 China; chili 8 Americas + 3 China; sweet_potato 3 Americas + 4 China + 2 Peru; potato 6 Andean + 0 China.

**Per-crop lever (FINAL, on corrected geography):**
1. **maize** — food-only. Now grown across the Americas AND China (both are producers → both get the production-gated food demand). It is a bulk SUBSISTENCE grain everywhere, never a universal luxury. REMOVE from both luxury call-lists; rewrite DEMAND_maize Total food-only (drop the luxury seed + else=base). DEMAND_food_maize already exists (:36). Its food-count increment already exists (:56/:96).
2. **sweet_potato** — food-only. China (4) + Peru (2 pre-existing) + 3 new American producers → all get food demand. Same treatment as maize; DEMAND_food_sweet_potato exists (:92), count increment exists (:64/:106). Subsistence root everywhere.
3. **potato** — food-only NOW SAFE (the #64 geography flip changed this verdict). OLD reasoning kept potato in luxury because it was Americas-ONLY, so a production-gated food path would zero Chinese demand. But #64 did NOT add Chinese potato (correct — potato had near-zero 1763 China adoption), so potato remains Americas-only (6 Andean). HOWEVER: the double-count still makes it demanded as a universal LUXURY everywhere, which is wrong — 1763 potato was NOT a global luxury import into China (unlike, say, tobacco); it was an Andean/Irish subsistence staple. So the correct model is food-only (production-gated to the Andes), and ACCEPT that non-Andean potato demand drops to ~0 — that is HISTORICALLY RIGHT (China/Qing had no meaningful potato demand in 1763), not a "dead good" bug. DEMAND_food_potato already exists (:64), count increment exists (:60/:101). REMOVE from both luxury call-lists; rewrite DEMAND_potato Total food-only. (This SUPERSEDES the old "keep potato in luxury" verdict, which was an artifact of worrying about zeroing a Chinese demand that shouldn't exist.)
4. **peanut** — LEAVE luxury-only (REVISED from the old "build a food path"). Peanut is NOT in the food call-list or count block today, and has NO DEMAND_food_peanut svalue. Building a full food path (new svalue + fold-in + call + count-increment) is the biggest single piece of work in #62 — and on the corrected geography it is NOT warranted: peanut in 1763 was a minor oilseed/garden crop (research RESEARCH_NWCROP_GEOGRAPHY_64: "minor/garden crop everywhere… NOT a dominant staple"), i.e. genuinely closer to a discretionary good than a bulk calorie staple. It is NOT double-counted (luxury-only already). So: leave peanut exactly as-is. (Its deeper differentiation is the #65/#66 question, not #62.)
5. **chili** — LEAVE luxury-only (unchanged). Condiment/spice, never a bulk food; not double-counted. Correct as-is.

**NET #62 fix (final, minimal):** the double-count is maize/potato/sweet_potato (the 3 crops in BOTH baskets). Fix = for EACH of the three: (a) rewrite its DEMAND_<crop> Total svalue food-only (drop the luxury var seed + the `else = DEMAND_luxury_base_total` fallback, so the value builds purely from var:DEMAND_food_<crop> — the C1/C2 correction, the real fix, NOT just the call-list edit); (b) remove it from BOTH luxury call-lists (:618-627 + :655-664) as dead-writer cleanup. peanut + chili: LEAVE (luxury-only, not double-counted, no food path needed). NO new DEMAND_food_peanut (the old H2 work is DROPPED). Count block already correct (maize/potato/sweet_potato increments exist; no peanut increment needed since peanut stays out of food).
**Files (final):** se_DEMAND.txt (remove 3×2 = 6 luxury call-list lines) + DEMAND_luxury_svalues.txt (3 Total svalue food-only rewrites: maize/potato/sweet_potato). TWO files. NO DEMAND_food_svalues_new.txt change (all 3 food svalues + count increments already exist). NO peanut work.
**VERIFY (boot):** Total DEMAND_maize/potato/sweet_potato DROP to food-only (no universal luxury component) — a non-producing governorship shows ~0 demand for them; producing governorships (China maize/sweet_potato; Andes potato; the new American maize/etc.) show food demand. peanut/chili unchanged. No governorship destabilized; famine divisor (#279) intact (count block unchanged). Cross-country sample (China, Americas, Europe).
**BOM/EOL:** se_DEMAND.txt + DEMAND_luxury_svalues.txt — verify each file's convention before editing; no churn.
This FINAL RESOLUTION supersedes the earlier "H3 RESOLVED" + "REFINED FIX" sections (both computed on broken geography). Round-2 review of THIS resolution required before implementing (per the standing rule: nothing built until a clean review passes).
