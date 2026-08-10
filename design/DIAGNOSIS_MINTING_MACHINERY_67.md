# DIAGNOSIS (Stage 0) — #67 paper-money: the minting machinery it will touch

**Status:** Stage-0 diagnosis of the EXISTING minting code (the surface a paper-money regime modifies), 2026-08-10, source-traced. The NEW regime itself is research→design (gated on RESEARCH_QING_PAPER_MONEY_67.md, in flight). This diagnoses only the existing part.

TERMINOLOGY: "BOM" = byte-order-mark file header only.

## The mint chain (traced end-to-end)
1. **`CURRENCY_mint_currency`** (se_CURRENCY.txt:1381), monthly: clamps `var:CURRENCY_minting_rate` down to `CURRENCY_minting_rate_cap` if over, then mints that many thousands into `amt_circulated` (`CURRENCY_alter_amt_circulated`) + distributes to governorships. **The cap is the SOLE minting throttle** — nothing else bounds how much currency is created.
2. **`CURRENCY_minting_rate_cap`** (CURRENCY_svalues.txt:828): the branch that matters —
   - `var:official_currency.var:paper_money_allowed = flag:false` → `reserve_change_for_minting + 1%-of-circulation + trade_wealth + sister-countries` (a bounded, metal-reserve-anchored ceiling).
   - `else` (paper allowed) → **`value = 99999`** — effectively uncapped.
3. **`paper_money_allowed`** is a per-currency var, set once at currency creation (se_CURRENCY.txt:1841), CHI's = false. No runtime setter exists; it IS runtime-settable (hop into var:official_currency, set_variable). Read ONLY at CURRENCY_svalues.txt:837 (the cap branch above).

## The existing bounded-ceiling precedent to REUSE (#63)
`se_QING_DECLINE.txt` already implements a CHI-only PROPORTIONAL mint ceiling: `qing_mint_ceiling_tmp = CURRENCY_minting_rate_cap × qing_mint_factor_tmp` (factor = 1 + bias×0.0375, from the monetary-policy law bias), then an RHS-safe clamp of `CURRENCY_minting_rate` down to that ceiling. This is the exact shape a paper regime needs — only with a factor > 1 (a HIGHER ceiling) + an inflation penalty, instead of #63's tightening factor < 1.

## Verdict (confirms the task's design constraint)
- Flipping `paper_money_allowed = true` in a law option hits the **99999 branch = deletes the throttle → runaway M1 → re-breaks #23 (silver-price loop) + #60 (M1 rebalance).** Confirmed: the cap is the only throttle, and 99999 is not a "higher cap", it is "no cap". So the raw-flag approach is genuinely unsafe (matches the #63 R1 caution).
- The SAFE build: a paper-money regime sets a **higher-but-FINITE** CHI-side ceiling via the #63 `qing_mint_ceiling` mechanism (a paper `qing_mint_factor` > 1, magnitude from the research's over-issue/depreciation numbers) + an **inflation/backing-erosion penalty** that models the historical Baochao/Guanpiao depreciation. Reversible (abandon regime → factor back to specie). Does NOT touch `paper_money_allowed` (leaves it false so the 99999 branch never fires) — the regime works entirely through the bounded CHI ceiling, so #23/#60 stay intact.
- This is buildable on the existing #63 machinery; the research supplies the ceiling magnitude + the depreciation-penalty curve + the unlock gating (likely late/crisis, not 1763). Design stage gated on RESEARCH_QING_PAPER_MONEY_67.md.

## Note
No runtime setter for paper_money_allowed exists today; the regime deliberately does NOT add one (leaving the 99999 branch permanently unreached is the safety property). All minting stays on the bounded CHI ceiling path.
