# DIAGNOSIS — vegetables' global boom-bust-to-zero (task #93, 3rd pass)

**Status:** DIAGNOSIS, adversarial-reviewed 2026-08-18. Mechanism CORRECTED after review
(the first draft's "seeded reservoir + infrastructure export cap" model was refuted — see
§4). No code change proposed yet; fix directions in §8 are candidates only.
**Author:** freekumquats, 2026-08-18.
**Supersedes the conclusions of:** `DESIGN_93_VEGETABLES_SHORTAGE.md`,
`DESIGN_93_FOLLOWUP_VEGETABLES_STILL_COLLAPSING.md`,
`DESIGN_93_VEGETABLES_PROVINCE_COUNT_AUDIT.md`, `DESIGN_93_VEGETABLES_WORLDWIDE_AUDIT.md`
(all treat 419 provinces as Chinese; 418 active provinces are worldwide, Russia/India/
central-Europe/upper-Yangtzi dominant — see §6).

Built from a live boot (`logs.zip` Aug 17 22:14), verified against source, then attacked by an
adversarial reviewer who refuted the original §4 mechanism. This version reflects the corrected
model. Two earlier diagnoses were already overturned this session — do not treat any single line
as settled without the file:line evidence attached.

---

## 1. The symptom (measured)

`tools/curx_analyze.py --good vegetables` over the whole `debug.log` (6.68M lines), per-zone
**price | stock | order**, POST snapshots, quarters 0-9:

- **~20 of 22 trade zones stock out** (stock band → `0`) by q4-q7, price spikes into the
  **`10-100` band** from a `0-0.01`/`0.1-1` baseline — a **100-1000× rise**.
- Includes **China's own zones**: `yellow_sea` (stock 1000-10000 → 0 at q6) and `upper_yangtzi`
  (stock 100-1000 → 0 at q7), price 0.1-1 → 10-100 in both.
- **Only 2 zones stay healthy**: `central_europe` (~40 local veg provinces) and `india` (~30).
  Both hold heavy LOCAL vegetable production.
- Trajectory: cheap+high-stock early (q0-q3), crash to 0 mid (q4-q6), pinned at 0/high-price after.

Real, near-global shortage. Prices rise fast — confirmed. NOT a probe artifact.

## 2. The paradox the diagnosis must explain

Vegetables is the MOST-cushioned food good, yet the only one that collapses:
- **Lowest industrial demand-pressure of any food** (base_demand ÷ provinces): vegetables
  6/418 = 0.0143 vs temperate_fruit 10/661 = 0.0151, grain 20/1746 = 0.0114, livestock 0.0111,
  fish 0.0060. (Constants trimmed 5/6/6 → 2/2/2 by `4ee1f5412`, `INDUSTRY_svalues.txt:1389/2493/3111`.)
  CAVEAT: this metric ignores factory COUNT (actual demand = base × factories) — a weak proxy,
  though the arithmetic is right.
- **Uniquely gets a ×4 production multiplier** (`GOODS_svalues.txt:1977-1993`; grain lacks it,
  `:1995-2006`), and it **reaches the real stockpile** (`se_GOODS.txt:239-244`:
  `vegetables_stockpile = GOODS_governorship_vegetables_produced`, ×4-inclusive).

A pure magnitude story cannot explain a good with the lowest demand AND 4× production collapsing
alone. The answer is the INTERACTION of geography and a demand ratchet.

## 3. The shared demand ratchet — the collapse ENGINE (corrected: not a bystander)

Every food good runs the same two-part demand shape (verified identical across all six):
- a **price-elasticity divide**: `DEMAND_actual_$good$` divides by `..._price_diff_to_food_avg`
  (`DEMAND_food_svalues.txt` grain `:334`, fish `:557`, livestock `:604`, vegetables `:651`,
  temperate_fruit `:692`, processed_foods `:739`). When a good is CHEAP (price below the food
  average), the divide **inflates** its demand — pops pile into the cheap food.
- a **±10%/tick clamp**: demand is bounded to `previous_tick × [0.9, 1.1]` (grain `:343`, fish
  `:572`, livestock `:619`, vegetables `:660`, temperate_fruit `:707`, processed_foods `:748`).

Together these RATCHET demand upward each quarter and prevent it unwinding faster than 10%/tick.
Grain even divides twice (`:357-358`) — MORE elasticity-amplified — yet never collapses. So the
ratchet is NOT unique to vegetables. But it is the ENGINE of the collapse trajectory, not a minor
term (the first draft wrongly downgraded it to "may worsen").

## 4. How the collapse actually works (CORRECTED — flow model, not reservoir)

**The first draft was wrong that zones hold a "seeded initial stock" that is "burned through"
and that an infrastructure export cap throttles refills. Refuted by code:**

- `$tradezone$_stockpile_$tradegood$` is **NOT a reservoir**. It is **reset to 0 for all 22 zones
  at the start of every quarterly pass** (`se_GLOBALTRADE_split.txt:204-207`, in
  `GT_split_reset_global_TZ_variables_tradegood`, called first) and **rebuilt by `add` only**
  (`:1032-1035`, `add = var:for_sale_$tradegood$` summed over the zone's governorships). There is
  **no `subtract`** against it anywhere. Nothing carries between quarters.
- Price is an **instantaneous ratio**: `price = (zone_order_size / zone_stockpile) × 0.6 ÷
  num_food_tradegoods` (`:6243-6268`).
- The infrastructure cap on `for_sale` (`:761-813`) is **single-digit-to-tens** in magnitude
  (`TRADE_svalues.txt:88-97`) — far too small to produce the observed 1000-10000 zone stock, and
  being constant it cannot create a high→zero *trajectory*. **It does not bind here.** Deficit-zone
  refill is instead throttled by `global_supply_as_percentage_of_order` (`:3159-3176`).

**So each quarter, per zone:**
```
zone_stockpile = Σ over local govs of  max(0, production×4 − governorship_demand)     (thin where few veg provinces)
zone_order     = Σ over local govs of  max(0, governorship_demand − production×4)
price          = zone_order / zone_stockpile × 0.6 / num_food_tradegoods
```
Production is stable/rising (CHI 12,980→13,560). The ONLY quantity that moves across quarters is
**governorship demand**, ratcheting up (§3). Where production is thin, ratcheted demand overtakes
it → `for_sale → 0` → `zone_stockpile → 0` → `order` grows → `price = order/stock` **explodes**
→ the ±10% clamp pins demand high → permanent 0-stock / high-price. **A geography-gated demand
ratchet.**

Grain is immune only because its production is abundant in **every** zone (1746 provinces), so
ratcheted demand can never overtake local supply.

**Why China's own zones crash (the weak link, now precise):** a zone's stock is ONLY the local
for_sale of its own governorships. `yellow_sea` (Shandong/Jiangsu/Fujian/Korea/Japan — huge
demand, only ~7 veg provinces) and `upper_yangtzi` (~13) are thin; CHI's healthy 13,560 is
produced in *other* governorships and **cannot cross** — imports feed the buyer *governorship's*
stock, never the *zone* stock variable. National production is irrelevant to a zone's price.

## 5. Why each lever tried so far missed — and why ×4 is now REOPENED

- **Demand trim 17→6 (`4ee1f5412`):** lowered the ratchet's ceiling slightly but added no local
  production in deficit zones. Wrong axis. (The followup's "did not move the outcome" fits.)
- **×4 production (`ae8d90818`) — sign now AMBIGUOUS, "keep it" is UNSUPPORTED:** ×4 raises q0
  zone stock, which via `price = order/stock` makes the **early price CHEAPER**, which makes the
  elasticity divide (§3) inflate demand **harder** — a HOTTER ratchet ignition. So ×4 buys
  production headroom AND accelerates the demand ratchet; the net sign is untested. Removing or
  right-sizing ×4 is a **live candidate**, not the closed question the first draft claimed. Its
  stated rationale is also mis-derived (province-count ratio is not causal; 418 worldwide, not
  "419 CHI").
- **Demand-side shortage throttle (proposed then REJECTED in `4ee1f5412` review):** CRITICAL
  same-tick circular dependency (`shortage_vegetables` is computed by dividing by the very demand
  it would gate). Dead path — do not revisit.

## 6. What the prior docs got wrong

All four `DESIGN_93_VEGETABLES_*` docs treat the 419 provinces as **Chinese** and justify keeping
the assignment on **China-scoped** research. **418 active provinces (one "419th" is in
`setup/provinces/00_0_setup.txt_old`, a backup the game does not load) are worldwide** — heavy in
central Europe (~40 feeding central_europe zone), India (~30), upper Yangtzi (~13), Russia, with
only ~7 in the coastal-China `yellow_sea` bucket. Their "no change / keep" verdict was never
tested against the non-China majority (~88%). Unsupported for that majority.

## 7. Adversarial review outcome (2026-08-18)

Reviewer verdict: **geography differentiator CONFIRMED; low-stakes CONFIRMED; §4 mechanism
REFUTED and rewritten above.** Corrected true root cause = **a geography-gated demand ratchet**:
- Necessary condition (geography): thin, concentrated veg production; ~0 in the New World, most of
  Africa, coastal China/Korea/Japan.
- Active mechanism (the ratchet, §3): shared elasticity-divide + ±10% clamp drive governorship
  demand up each quarter; where production is thin it is overtaken; per-quarter `price=order/stock`
  then spikes. Both must combine.
Reviewer's three required corrections, all applied above: (i) drop the seeded-stock/infra-cap
narrative; (ii) treat the ±10% ratchet as the engine, not a bystander; (iii) reopen the ×4 (it
may ACCELERATE the ratchet by cheapening the early price).

## 8. Candidate fix directions (NOT decided — design phase, after a fix is chosen)

- **A. Geographic reseed (addresses the necessary condition; safest, lowest blast radius):** add
  vegetables to under-served deficit-region provinces (the New World historically grew abundant
  vegetables — beans, squash, maize, tomatoes, potatoes, peppers) so ratcheted demand cannot
  overtake local production. Must respect sourced crop geography (`imp19c-nwcrop-geography-64`).
- **B. Right-size or remove the ×4 (now a real option, not off-limits):** test whether removing it
  COOLS the ratchet (higher early price → less demand inflation) more than it hurts headroom. Sign
  is untested — needs a boot with logging. Pairs naturally with A.
- **C. Dampen the ratchet ignition** (e.g. a gentler early-price / elasticity response for foods
  with thin production). Touches the SHARED food-demand loop that grain/fish/etc. also use — high
  risk, needs a probe; do not blind-edit (Sobisonator-caution).
- **D. Accept as low-stakes:** CHI cost-of-living stayed 16-26 (never near the 32000 cap), pops
  substitute and do not starve; the only real cost is the 3 vegetable-input factories'
  (alcohol/pharmaceuticals/processed_foods) output malus + absurd displayed prices. Fix only the
  mislabeled ×4 rationale and document ROW vegetables as a known abstraction gap.
- **REJECTED:** any demand-side shortage throttle (circular, §5).

No code until a direction is chosen and (for B/C, which touch shared loops) probe-verified.
