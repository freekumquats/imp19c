# new_trade_goods.md — trade_goods branch decision log (#279)

Branch: **trade_goods** (off `develop`). LAST queued item; explicitly flagged RISKY by the user.
Author/committer identity: **freekumquats** (standing rule).

Scope as requested: *"try to add New World crops to the required basket of 6 essentials and add
rifles, porcelain, etc to the list of manufactured goods (both of which tie into many core systems
and are risky changes)."* Refer to `SESSION_REPORT.md` for prior decisions on why risky trade
changes were deferred (see esp. the **#64 crops** entry and the **P4 rifles DRAFT-ONLY** note under
the logistics build — the phantom-shortage failure mode documented there governs this branch).

---

## 0. What already exists (baseline audit before touching anything)

Before writing any code I mapped the whole trade-good + demand surface on `develop`. Two decisive facts:

### 0a. The "manufactured goods" half is ALREADY LIVE
`common/scripted_effects/se_DEMAND.txt` → `DEMAND_set_demand_from_luxury_all` (line ~550) already
lists, as luxury/manufactured demand goods:
`luxury_clothing, luxury_furniture, spices, tobacco, maize, porcelain, rifles, sweet_potato,
potato, peanut, chili, opium, sugar, gems, chocolate, salt, alcohol, coffee, glass, tea`.

So **porcelain and rifles already carry population luxury demand**, are defined trade goods
(`common/trade_goods/00_imp19c.txt`, category 4), are priced & traded (per-good `every_tradegood_complex`
price setup in `se_PRICE.txt`), have `global_mean_price_porcelain`/`_rifles` svalues
(`PRICE_svalues.txt:133/142`), and are produced via `GOODS_governorship_porcelain_produced` /
`_rifles_produced` (`GOODS_svalues.txt`). Work done under #180/#189 (see SESSION_REPORT lines
~2261-2296). **The "add manufactured goods" half of #279 needs verification + documentation, not
new implementation.** — DECISION D1 below.

### 0b. New World crops are ALREADY supply-side food + luxury demand — deliberately NOT staples
- `DEMAND_fulfilled_food_need_governorship` (`DEMAND_food_svalues.txt`) already adds
  `maize/sweet_potato/potato/peanut/chili` production as "quarter food" (÷2) on the SUPPLY side.
- They are in the luxury demand list (0a).
- They are **excluded from the fixed 6-good staple DEMAND basket** — and this exclusion is the
  #64-fix design intent (SESSION_REPORT ~line 155/173): the crops were cloned from the `tobacco`
  archetype as *category-2 cash crops that give `local_monthly_food` but are NOT added to the fixed
  6-good staple demand basket* precisely to avoid a worldwide phantom shortage.

### 0c. The fixed 6-good staple basket and its ~40 hardcode sites
The staple basket = **grain, fish, livestock, temperate_fruit, vegetables, processed_foods**.
Divisor `DEMAND_num_food_tradegoods = 6` (`DEMAND_food_svalues_new.txt:1`) and its sibling
`DEMAND_num_food_goods = 6` (`DEMAND_food_svalues.txt:12`). The six goods are literally enumerated
(and summed, then ÷ the divisor) in:
- `se_DEMAND.txt` — `DEMAND_set_demand_from_food_all` (6 per-good calls)
- `se_PRICE.txt` — local food avg price, MAD, normalised-price (conditional adds)
- `DEMAND_food_svalues.txt` — `DEMAND_food_avg_price`, `_price_MAD`, `_avg_price_normalised`
- `CURRENCY_svalues.txt`, `WEALTH_svalues.txt`, `AI_svalues.txt` — country-unit-price food aggregates
- `PRICE_svalues.txt` — `global_mean_price_X` per good (already present for crops too)
- `000_ECON_loc.txt` — price tracker custom loc

---

## D0. THE CORE RISK (why this was deferred, restated)
A naïve global **6 → 9** basket (adding maize/potato/sweet_potato as staples demanded *everywhere*)
does two damaging things:
1. **Dilutes existing staple demand ~33%** (pop×0.3 now ÷9 not ÷6) — every grain/fish/… order
   worldwide shrinks, distorting every price the economy has settled on.
2. **Creates permanent worldwide phantom shortages.** Only ~28 provinces on Earth grow these crops,
   but every governorship on the planet would now demand maize/potato/sweet_potato. Every
   non-producing governorship runs a permanent negative `*_stockpile` → `shortage_maize/potato/
   sweet_potato` → the shortage-malus cascade (`ECON_governorship_food_shortage`,
   `DEMAND_svalues.txt` shortage readers, `EE_scripted_guis.txt` shortage tooltips). This is exactly
   the failure the **P4 rifles DRAFT-ONLY** note warned about ("a half-registered good would inject a
   permanent phantom shortage that P1 would then punish").

So the naïve global expansion is REJECTED. See D2 for the chosen safe design.

---

## D1. Manufactured goods (porcelain / rifles) — VERIFIED COMPLETE, no new code
Full wiring confirmed on `develop` (all present before this branch):
- **Defined:** `common/trade_goods/00_imp19c.txt` porcelain (cat 4) / rifles (cat 4).
- **Localised:** `imp19c_tradegoods_l_english.yml:119 porcelain "Porcelain"` / `:121 rifles "Rifles"`;
  internal-trade-scope loc in `economic_enchancement_l_english.yml:1242-1247`.
- **Priced:** per-good `every_tradegood_complex` price setup (`se_PRICE.txt`); `global_mean_price_porcelain`
  (`PRICE_svalues.txt:133`), `global_mean_price_rifles` (`:142`).
- **Produced:** `GOODS_governorship_porcelain_produced` / `_rifles_produced` (`GOODS_svalues.txt`).
- **Demanded:** both in `DEMAND_set_demand_from_luxury_all` (`se_DEMAND.txt`).
- **Content-tied:** rifles ← arsenal_building (`QING_selfstr_found_jiangnan` retargets arsenal province
  to `set_trade_goods = rifles`); porcelain ← Jingdezhen imperial-kiln (御窯廠).

**DECISION D1:** the "add rifles/porcelain to the manufactured-goods list" half of #279 was already
delivered under #180/#189. This branch does **not** re-touch it; it only documents the verification
and (optionally) widens which regions grow porcelain. No risk, nothing to build. The rifles/porcelain
half of the user's request is **satisfied**.

---

## D2. New World crops → staple demand: CHOSEN SAFE DESIGN = "conditional (local) staple"

Rejected alternatives:
- **A. Naïve global 6→9 staple everywhere.** REJECTED — D0 (dilution + worldwide phantom shortage).
- **B. Fully category-iterated dynamic basket** (`every_trade_good` with an `is_food` flag driving
  ~40 sum-sites). REJECTED for this branch — a ~40-site rewrite of the settled price index is far
  higher blast-radius than the request warrants, and the price-index half gains nothing from it.

**CHOSEN — C. Conditional local staple, keyed to a concrete on-map fact (does this land grow the crop).**
Rationale is also historically correct: potato/maize/sweet_potato became *subsistence staples in the
regions that adopted them* (Irish potato, south-Chinese hillside sweet-potato, Andes/Mesoamerica
maize) — they were NOT universally-traded food staples in 1763-1836. So "staple where grown, nothing
where not" is both the safe model AND the accurate one. This is the concrete-over-abstract,
additive-conversion approach the project's standing design rules prefer.

Two divisors exist and are cleanly separated — this is what makes C safe:
- `DEMAND_num_food_tradegoods = 6` — the **global price-index** divisor (avg food price, MAD,
  normalised price; `DEMAND_food_svalues*.txt`, `se_PRICE.txt`, `se_DEMAND.txt`, `se_GLOBALTRADE_split.txt`).
  **LEFT AT 6, UNTOUCHED.** Crops have thin/absent markets in most regions; folding them into the
  global price average/MAD would inject noise and thin-market artifacts. Zero change here = zero risk
  to the settled price system.
- `DEMAND_num_food_goods = 6` — the **demand allocator** divisor (`DEMAND_food_svalues.txt:12`, used by
  `DEMAND_food_base`/`DEMAND_total_food_need_div_num_food_goods` and `ECON_governorship_food_shortage`).
  Made **per-governorship dynamic**: `6 + (# of {maize,potato,sweet_potato} this governorship grows)`.

Implementation (all additive, all gated on `GOODS_governorship_<crop>_produced > 0`, which already
exists and is already summed on the SUPPLY side of `DEMAND_fulfilled_food_need_governorship`):
1. `DEMAND_num_food_goods` → dynamic: base 6, `+1` per crop the governorship actually produces.
   Because the extra staple demand and the extra local food supply appear together, per-good demand is
   NOT diluted where the crop grows, and net food need tracks net food supply.
2. `DEMAND_set_demand_from_food_all` (`se_DEMAND.txt`) → add three GATED `DEMAND_set_demand_from_food`
   calls (maize/potato/sweet_potato), each wrapped in `if = { limit = { GOODS_governorship_<crop>_produced > 0 } }`.
   A governorship that does not grow the crop sets NO demand var for it → no order → no negative
   stockpile → **no phantom shortage** anywhere on the map. This is the single guard that neutralises D0.
3. Crops are ALREADY on the supply side of `DEMAND_fulfilled_food_need_governorship` — but currently at
   the "quarter food" (÷2 twice = ¼) weight. Since they are now genuine local staples, that supply
   weighting is left as-is for this pass (conservative: under-counting supply is safe, it can only make
   the model slightly hungrier, never inject a phantom surplus). Documented as a tuning knob, not changed.
4. Price index untouched (see above). `ECON_governorship_food_shortage` automatically benefits from the
   dynamic `DEMAND_num_food_goods` (its divisor), so its "16% if all satisfied except processed food"
   calibration self-adjusts where a crop is a local staple.

**Net effect:** in a governorship that grows sweet_potato, the population now demands sweet_potato as a
7th staple AND that governorship's own sweet_potato production feeds it; elsewhere nothing changes.
No global dilution, no phantom shortage, no price-index disturbance. This is the minimum-blast-radius
way to honour "add New World crops to the essentials basket" without the deferred catastrophe.

se_LOG marker + fix-traceability comments on every edit (standing rule). Boot-validity + adversarial
review workflow after build (standing rule).

### D2-oracle. Oracle consultation (standing rule — done BEFORE building)
Consulted Terra-Indomita + Invictus (feasibility-only). Findings:
- **Category-iterated basket is NOT engine-feasible.** Neither oracle uses `every_trade_good`/
  `any_trade_good` or runtime `category` filtering; goods are referenced by hardcoded name. Confirms
  **rejecting option B** — you cannot auto-size a demand basket from a category flag at the engine
  level. (Our own price loop uses `every_tradegood_complex`, but that is a zz_injectormaker-GENERATED
  hardcoded iterator, not an engine primitive — so it does not help auto-size the *demand* basket.)
- **Neither oracle models per-good food demand at all** — both use a single aggregate `has_state_food`
  scalar. So there is NO prior art for a per-good demand basket, and NO recorded phantom-shortage
  failure — because the failure mode simply cannot arise in a fungible-food model. Our mod is the only
  one with per-good food demand, so the D0 risk is real and ours alone to manage.
- **Shortage handling is soft** (loyalty/modifier penalty + famine events), never a crash. Confirms the
  D0 risk is economic-tuning, not a boot/stability failure.
- **No "regional/optional demand" precedent exists** — the oracles gate nothing by region. Our
  conditional-local-staple design (D2 option C) is therefore *pioneering*, but it is the safe pioneering
  choice: it is strictly additive and self-gating, so the worst case is "a crop staple that nobody
  ever demands" (a no-op), never a negative-stockpile cascade.
- The oracle's own suggestion (flat `= 9` global) is exactly rejected-option-A: the oracle cannot see
  our worldwide phantom-shortage risk because its economies have no per-good demand to break. We do not
  take that suggestion.

---

## D3. EXACT EDIT SET (conditional-local-staple, 5 coordinated edits)

Two divisors, cleanly separated so the price index is never touched:
- `DEMAND_num_food_tradegoods` — **price index only**, stays `= 6`. Used by `se_PRICE.txt`,
  `DEMAND_food_svalues*.txt` (avg/MAD/normalised), `se_GLOBALTRADE_split.txt:5823`. UNTOUCHED.
- `DEMAND_num_food_goods` — **demand allocator**, made per-governorship dynamic via a cached var.

Performance guard (per the #139-perf discipline): the crop-count is computed **once per governorship**
into `var:DEMAND_food_goods_count` inside the once-per-governorship demand pass, NOT recomputed inside
the per-good svalue (which is read 6-9×/gov/quarter). `GOODS_governorship_<crop>_produced` each scans
all provinces in the governorship, so caching avoids ~dozens of redundant province scans.

**Edit A — `se_DEMAND.txt` `DEMAND_set_demand_from_food_all`:**
- Compute `DEMAND_food_goods_count` = 6, `+1` for each of maize/potato/sweet_potato with
  `GOODS_governorship_<crop>_produced > 0` (governorship scope, cached once).
- Add 3 GATED `DEMAND_set_demand_from_food` calls (maize/potato/sweet_potato), each inside
  `if = { limit = { GOODS_governorship_<crop>_produced > 0 } }`. This gate is the single guard that
  prevents phantom shortages: a non-growing governorship sets no crop demand var → no order → no
  negative stockpile → no shortage. se_LOG marker on the block.

**Edit B — `se_DEMAND.txt` `DEMAND_set_demand_from_food` (the ÷ line, currently
`divide = DEMAND_num_food_tradegoods`):** repoint to `divide = DEMAND_num_food_goods`. This is the
demand ALLOCATOR splitting unfulfilled food need across the basket; it should use the allocator
divisor, not the price-index divisor. Both = 6 today, so this is **byte-identical at 6-good baseline**
and only diverges where a crop is a local staple (÷7 etc.), conserving total food need.

**Edit C — `DEMAND_food_svalues.txt:12` `DEMAND_num_food_goods`:** read `var:DEMAND_food_goods_count`
if present, else `6`. Governorship-scoped var (set in Edit A). Fallback 6 keeps every non-pass read
(GUI/AI) and pre-first-tick reads exactly at baseline.

**Edit D — `DEMAND_food_svalues_new.txt`:** add `DEMAND_food_maize`, `DEMAND_food_potato`,
`DEMAND_food_sweet_potato` svalues — direct clones of `DEMAND_food_grain` (read `var:DEMAND_food_<crop>`
else `DEMAND_food_base`, with the 110%/90% rubber-band bounds). Required because the food effect
references the `DEMAND_food_$tradegood$` svalue at lines 79/84/93.

**Edit E — `DEMAND_luxury_svalues.txt` `DEMAND_maize`/`_potato`/`_sweet_potato` (Totals):** add
`if = { limit = { has_variable = DEMAND_food_<crop> } add = var:DEMAND_food_<crop> }` before `min = 0`
— mirroring how `DEMAND_grain` (Total) adds `INDUSTRY_demand_alcohol_grain`. Where the crop is a local
staple the food-demand component is folded into the good's total demand; elsewhere the var is absent
and nothing is added (pure luxury demand, as today).

Conservative choices held for a later tuning pass (documented, NOT changed this pass):
- Crops keep their existing "quarter food" SUPPLY weight in `DEMAND_fulfilled_food_need_governorship`
  (under-counting supply is safe — can only make the model hungrier, never inject a phantom surplus).
- `ECON_governorship_food_shortage` (÷`DEMAND_num_food_goods`) auto-benefits from the dynamic divisor;
  it still sums only the 6 base shortages, so where a crop grows it slightly *under*-reports shortage —
  safe direction (crops WERE extra food security), and historically apt.

---

## D4. ADVERSARIAL-REVIEW FIXES (post-build, review run wf_b48dad8a-976)

The 3-dimension adversarial-review workflow (divisor-correctness / phantom-shortage-gate / syntax-scope-loc)
confirmed **2 major bugs** in the as-built Edit A block (both independently refutation-verified) + 1 nit.
Both fixed in `se_DEMAND.txt` `DEMAND_set_demand_from_food_all`; tagged `[#279][review-fix bugN]`.

**Bug 1 (interleaved divisor).** The original block reset `DEMAND_food_goods_count` to 6 AFTER the six base
`DEMAND_set_demand_from_food` calls, then incremented it interleaved with the crop calls. So the base staples
divided the unfulfilled food need by the *previous pass's leftover* count, and the crops divided by *partial*
counts (maize÷7, potato÷8, sweet_potato÷9) purely by call order — steady-state total ≈ 1.046×need (~4.6%
over-demand) plus a per-crop asymmetry (maize ≈ 1.29× sweet_potato). **FIX:** compute the full basket count
first (three `limit`-only `if` blocks incrementing the count), THEN issue all nine demand calls, so every good
divides by the same final divisor. Non-crop governorships keep count 6 → baseline byte-equivalence holds.

**Bug 2 (stale crop var → phantom shortage).** `DEMAND_food_<crop>` was written only inside the
`produced > 0` gate and never removed. A governorship that STOPPED producing the crop (e.g. ceded the crop
provinces in a war — `se_LAND.txt` recomputes demand on transfer) froze the stale var; `DEMAND_luxury_svalues.txt`
reads it on `has_variable` alone → inflated `DEMAND_<crop>` → `CONSUME_from_stockpile` drives `<crop>_stockpile`
negative → `shortage_<crop>` → the exact phantom-shortage cascade D0/D2 set out to prevent. **FIX:** each crop
gate now has a sibling `else = { remove_variable = DEMAND_food_<crop> }`, clearing the var when produced==0.

**Nit.** Dropped the literal `[#279]` bracket tag from the `LOG_line` msg text (engine can cosmetically mangle
square-bracket tags as data-function syntax in -debug output); the task tag stays in code comments instead.

Post-fix: braces 225=225, BOM+CRLF preserved on all 4 files; a second review pass re-run after these fixes.
