# MG residual-correctness fixes — design (2026-07-29)

Two out-of-scope defects surfaced in the MG boot-test notes, now folded into the
`manufactured_goods` branch. Both are localized, upstream-verifiable one-token
corrections. Full pipeline still applies: design → adversarial review →
implement → adversarial review → commit/push.

Scope note: neither is strictly a *log flood* (a never-matching `flag:` compare
does not spam the log); the boot-test note grouped them under "residual". They
are real **correctness** bugs and are fixed as such.

---

## Bug 1 — bimetallic silver-reserve multiply typo

**File:** `common/scripted_effects/se_GLOBALTRADE_split.txt`
**Block:** the `else_if backing_type = flag:bimetallic_standard` branch of the
per-category state-reserve trade-share accumulation (≈ lines 5395-5450).

**Defect (line 5437-5440):**
```
change_local_variable = {
    name = trade_share_$category$_the_state_gold_reserves   # <-- WRONG: should be _silver_reserves
    multiply = DEMAND_silver_for_reserve_divided_by_base_demand
}
```
The silver half of the bimetallic branch does:
- `set   _silver_reserves = wealth_owed_for_silver`   (5426)
- `divide _silver_reserves by trade_expenses…(min 1)`  (5430)
- `multiply _GOLD_reserves by DEMAND_silver…`          (5437)  ← typo

Consequences:
1. `_silver_reserves` never receives its demand-ratio multiply (left at the
   raw divided value).
2. `_gold_reserves` is multiplied TWICE — once by `DEMAND_gold…` (5423, correct)
   and again by `DEMAND_silver…` (5439, spurious).
Then both reserves are added into `trade_share_$category$_the_state` (5442-5449),
so the state's bimetallic trade share is wrong for every bimetallic-standard
country.

**Proven-correct reference (same file, sibling branches):**
- gold-only branch (5374-5392): sets/divides/multiplies `_gold_reserves`, adds it.
- silver-only branch (5466-5484): sets/divides/multiplies `_silver_reserves`, adds it.
Both multiply the SAME reserve they set. The bimetallic branch must do likewise
for each metal.

**Fix:** line 5438 `_gold_reserves` → `_silver_reserves`. Single token. No other
line in the block changes.

---

## Bug 2 — cattle/livestock raw-goods classifier mismatch

**Real good:** `livestock` (`common/trade_goods/00_imp19c.txt:891`) is the only
loaded good. `cattle` is a defunct vanilla good name — NOT present in the goods
file — so `flag:$tradegood$` can never equal `flag:cattle`.

**The classifier** ("is this good raw resource-extraction vs manufacturing") is
copy-pasted in three places. Two list the correct `flag:livestock`; two list the
dead `flag:cattle`:

| location | lists | correct? |
|---|---|---|
| `se_GLOBALTRADE_split.txt:3491` (expenses side, `GT_split_scale_wealth_owed…`) | `flag:cattle` | **WRONG** |
| `se_GLOBALTRADE_split.txt:3600` (income side, `GT_split_get_governorship_income_due_tradegood`) | `flag:livestock` | correct |
| `common/scripted_triggers/00_trade_scripted_triggers.txt:74` (`is_raw_tradegood`, currently unused) | `flag:cattle` | **WRONG (latent)** |
| `se_GLOBALTRADE_split.txt:5881` (separate FOOD list, not the raw list) | `flag:livestock` | correct / unrelated |

**Consequence (live):** livestock **import expenses** fall through 3491's raw-goods
`if` into the `else` manufacturing bucket (`queued_trade_expenses_due_manufacturing`),
while livestock **income** (3600) is correctly booked to resource-extraction.
The two sides of the same good disagree — mis-splitting a country's
resource-extraction vs manufacturing expense accounting whenever it imports
livestock.

**Fix:** change `flag:cattle` → `flag:livestock` at BOTH wrong sites
(split:3491 and scripted_trigger:74). The scripted_trigger copy is currently
unused, but it is the "canonical" list and fixing it removes a latent trap for
whoever wires it up later.

**`cattle` residue left untouched (correct):**
- loc `cattle:0 "Livestock"` lives in the "Old Tradegoods" section — a legacy
  display string, not a live good; leave it.
- `is_raw_tradegood`'s only definition; no callers — see grep in review.

---

## Verification plan (post-impl)
1. Brace balance unchanged (no `{}` added/removed — pure token edits).
2. BOM/CR: `se_GLOBALTRADE_split.txt` and `00_trade_scripted_triggers.txt` — match
   each file's existing convention (do not add/strip BOM).
3. `rg "flag:cattle"` over `common/` returns ZERO after the fix.
4. `rg "_gold_reserves\s*\n\s*multiply = DEMAND_silver"` returns ZERO after the fix
   (the double-multiply is gone).
5. The three raw-goods lists (split:3491, split:3600, scripted_trigger:74) are now
   token-identical for the livestock entry.
