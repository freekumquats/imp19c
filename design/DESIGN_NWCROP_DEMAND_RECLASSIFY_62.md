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
