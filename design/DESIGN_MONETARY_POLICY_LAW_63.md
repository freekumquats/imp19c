# DESIGN — Wire the Monetary Policy laws to the real currency system (#63)

**Status:** implementation design, 2026-08-10. Design-note-first → adversarial review → implement → verify boot. Do NOT implement until reviewed. freekumquats / merge-overnight.

## The complaint (task #63)
The Monetary Policy law group is "outdated and doesn't connect properly with minting/conversion/etc features." Verified: the two law groups' options carry ONLY flat vanilla `modifier = {}` blocks (commerce/tax/stability/corruption nudges) and are **read by nothing in live script** — `rg` for every option key (`currency_recall|limited_minting|more_minting|issue_bonds|executive_monetary_policy|delegated_monetary_policy|legislative_monetary_policy`) across `common/` (excluding laws/loc) returns ONLY design docs. The laws are cosmetic; the real currency machinery (mint rate, mint-rate cap, backing value, the Qing `qing_currency_stress` meter, the #23 sqrt/gbip chain, #59 Tier B) runs entirely independently of the player's stated monetary stance. Choosing "sound money / recall" vs "loose minting" changes a commerce modifier but does NOT change how much the country actually mints or how its currency is backed.

## Current state (verified in source)

### The laws (common/laws/00_administrative_laws.txt + 00_monetary_policy_setting.txt)
- **`monetary_policy_law`** (`potential = { is_tribal = no }`): WHO controls the mint —
  - `executive_monetary_policy` — `stability_monthly_change 0.02`, `monthly_corruption 0.02` (crown/treasury; firm but graft-prone).
  - `delegated_monetary_policy` — `global_commerce_modifier 0.03`, `global_tax_modifier 0.02` (competent board).
  - `legislative_monetary_policy` (`allow = is_republic`) — `global_commerce_modifier 0.05`, `research_points_modifier 0.02`, `stability_monthly_change -0.02`. **Gates** `monetary_policy_setting` (its `potential = { has_law = legislative_monetary_policy }`).
  - NOTE: the PART D brace bug (DESIGN_LAW_EXPANSION §PART D) is **already fixed** — 3 balanced options, 3 open / 3 close. The cosmetic `modifier` fills PART D specified are **already shipped**. #63 is the wiring PART D explicitly deferred ("Nothing to copy — fill plausibly with proven modifier keys"; PART D did the fill, NOT the mechanical wiring).
- **`monetary_policy_setting`** (`potential = { has_law = legislative_monetary_policy }`): the STANCE — `currency_recall` (deflationary), `limited_minting`, `more_minting`, `issue_bonds`. **Only reachable by republics** today (the potential gate), so for the Qing (a monarchy) this whole group is UNREACHABLE — a monarchy can never pick a minting stance. That is the deepest disconnect: the stance group that SHOULD drive minting is locked behind a republic-only gate.

### The real currency machinery (what the laws should touch)
- **`CURRENCY_minting_rate`** (var, per-country) — how much the country mints each month. SET by the player via `common/scripted_guis/EE_scripted_guis.txt:452-537` (the Economy view mint slider), clamped to `CURRENCY_minting_rate_cap`. READ by `CURRENCY_mint_currency` (se_CURRENCY.txt:1381) → `CURRENCY_alter_amt_circulated`. **This is the concrete "minting" lever the laws claim to govern.**
- **`CURRENCY_minting_rate_cap`** (svalue, CURRENCY_svalues.txt:828) — the ceiling: if paper money NOT legal → `reserve_change_for_minting + 1% of circulation + trade_wealth_income + sister-country recycling`; if paper legal → `99999` (uncapped). **This is the concrete "backing/discipline" lever** — sound money = a tight cap, loose money = a loose cap.
- **`qing_currency_stress`** (0..100, se_QING_DECLINE.txt) — the Qing monetary-health meter, RECOMPUTED each pulse as `clamp(base + opium_flow + residual, 0, 100)` (se_QING_DECLINE.txt:201-211). Already an ADDITIVE-term recompute (opium flow + a decaying residual thread in as `change_variable ... add`), band-classified via the shared `CURR_STRESS_classify` → `qing_curr_monetary_crisis`/strain modifiers. **This is the natural, proven insertion point for a law-driven bias** (mirrors #59 Tier B's "additive term into an existing recompute" and DESIGN_LAW_EXPANSION item 23's proposed `qing_monetary_bias`, which does NOT yet exist in script).
- **`paper_money_allowed`** (flag on the currency object) — gates the mint cap (uncapped when true). The `issue_bonds` / deficit-finance stance is the natural law that would touch this, but flipping it is HIGH-risk (uncaps minting → runaway M1 → the #23/#60 money-supply model) — see RISK.
- The #23 sqrt/gbip chain and #59 Tier B are DOWNSTREAM of mint volume + reserves; #63 must NOT touch them directly (only influence mint volume/cap + the stress bias, which they already consume).

## THE DESIGN — three wiring layers, additive + guarded (the P7 / #59-Tier-B idiom)

The principle (matches every prior meter-concretize + the DESIGN_LAW_EXPANSION PART E rules): a law writes a **bias variable**; a pulse site reads that var behind `if = { limit = { has_variable = X } }` so the default (law never enacted / var unset) is **byte-identical to today**. No law directly `set_variable`s a currency number; each threads ONE guarded term into an EXISTING recompute or the mint gate. No new modifier NAMES are parameterized (not a proven construct). All on_action wiring reuses proven law-change hooks.

### Layer 1 — `monetary_policy_setting` stance → a minting-discipline bias (`qing_monetary_bias`)
The stance group is the "how much / how disciplined" lever. Wire each option to set a Qing country var `qing_monetary_bias` ∈ {hard-specie −N / neutral 0 / debasement +N}:
- `currency_recall` → bias **−** (sound money: pull debased coin, tighten issuance).
- `limited_minting` → bias **−/2** (disciplined).
- `more_minting` → bias **+** (loose).
- `issue_bonds` → bias **+/2** (deficit finance, looser — but does NOT flip `paper_money_allowed`; see RISK R1).

**Two concrete reads of `qing_monetary_bias` (both guarded, both additive):**
1. **Into the Qing stress recompute** (se_QING_DECLINE.txt:201-211): add `qing_monetary_bias` as one more `change_variable = { name = qing_currency_stress add = var:qing_monetary_bias }` term, INSIDE the existing clamp, alongside the opium_flow + residual terms it already sums. A debasement stance raises monetary stress (historically faithful — over-minting debases); sound money lowers it. This is the exact additive-into-existing-recompute pattern already proven in that block.
2. **Into the mint-rate cap** (the discipline lever): a sound-money stance should TIGHTEN what the player can mint, a loose stance LOOSEN it. Do NOT edit the vanilla `CURRENCY_minting_rate_cap` svalue (it's shared by every country + feeds #23/#60). Instead, apply the bias where the Qing mint is exercised: a small guarded adjustment to `CURRENCY_minting_rate` clamp behaviour for CHI only, OR a Qing-scoped modifier. **LEANING: option (a) below** — see "concrete lever choice."

### Layer 2 — `monetary_policy_law` (who controls the mint) → the bias's MAGNITUDE / integrity
The control group is the "how competent / how corrupt is minting" lever. Rather than a second independent bias var, make it a MULTIPLIER on how faithfully the stance is executed + a graft term:
- `executive_monetary_policy` — crown control: full bias magnitude, but the existing `monthly_corruption 0.02` modifier already models the patronage-trough graft (keep it; it feeds the Hoppo/salt-style corruption meters). No extra var needed — the modifier IS the wiring for the corruption half.
- `delegated_monetary_policy` — competent board: the stance executes cleanly (bias applies at full strength, no graft add) — its `global_commerce/tax` modifiers already reward competence.
- `legislative_monetary_policy` — accountable but slow: stance changes lag (model as-is via the `stability_monthly_change -0.02`; no new mechanic).

**DECISION (logged, overnight Rule 1):** do NOT build a second `qing_monetary_control_factor` var multiplying the bias. It adds a var + a read for a second-order effect the existing option modifiers already express. Layer 2 stays as its shipped cosmetic modifiers; its ONLY new mechanical role is UNLOCKING the stance group (Layer 3). Rejected alternative: a control→bias multiplier — cut as over-build (a var paying its cost for a subtle interaction the modifiers already cover). Recorded loudly, not deferred.

### Layer 3 — UNLOCK the stance group for the Qing (the deepest fix)
Today `monetary_policy_setting.potential = { has_law = legislative_monetary_policy }` → a monarchy can NEVER pick a minting stance, so for the Qing the entire stance group (the actual minting lever) is dead. Options:
- **(a) Broaden the potential** to `OR = { has_law = legislative_monetary_policy  has_law = executive_monetary_policy  has_law = delegated_monetary_policy }` — i.e. any monetary_policy_law lets you set a stance. Simplest; makes the stance group reachable for the Qing under its default (executive) monetary law. **LEANING (a).**
- (b) A Qing-specific parallel stance law group (兌換條例 / mint-regulation) — more work, duplicates the vanilla group. Reject unless (a) has a gate problem.

**Verify:** which monetary_policy_law the Qing holds at 1763 start (setup) — if none is set, Layer 3 must also ensure the Qing has a default `monetary_policy_law` (executive) so the broadened potential is satisfied. Ground this in the setup before implementing.

## Concrete lever choice — how the bias actually moves minting (the load-bearing decision)
Two candidate concrete hooks for the mint-discipline half of Layer 1's read #2:
- **(a) Qing-scoped guarded term in the mint pulse:** where CHI mints (find CHI's `CURRENCY_mint_currency` / minting call in the Qing monthly currency pulse), clamp `CURRENCY_minting_rate` DOWN by the sound-money bias (a sound stance caps the player's mint slider lower) / allow UP by the loose bias, CHI-only, guarded on `has_variable = qing_monetary_bias`. Does NOT touch the shared svalue. **LEANING (a)** — narrowest blast radius, CHI-only, additive, reversible (clear the var = today's behaviour).
- (b) Edit `CURRENCY_minting_rate_cap` svalue with a CHI-only guarded branch — rejected: the svalue is monthly, shared, and feeds #23/#60; a mistake there is global. (a) keeps the change on the Qing side of the fence (the [[currency sqrt]]/#60 caution: don't touch shared currency-core svalues).

**BLOCKER to resolve before impl:** confirm WHERE the Qing actually mints each month (the CHI call site of `CURRENCY_mint_currency` or `CURRENCY_alter_amt_circulated`) so lever (a) has a real, CHI-only insertion point. If the Qing minting is done by the same shared monthly pulse as everyone else (no CHI-only site), then read #2 must instead be a CHI-only guarded pre-step in that pulse. Ground this in se_CURRENCY.txt / the monthly currency on_action before writing.

## Files (anticipated — confirm at impl)
- `common/laws/00_administrative_laws.txt` — Layer 3 potential broaden (+ confirm Qing default monetary_policy_law).
- `common/laws/00_monetary_policy_setting.txt` — Layer 1: each stance option ADDS an `effect = { … set_variable qing_monetary_bias … }` (laws CAN carry an `on_enact`/effect? — VERIFY: vanilla law options take `modifier`; do they take an effect block, or must the bias be set via an `on_change`/on_action hook? This is a capability check — see traps). If law options cannot carry effects, the bias is set from an **on_action** that fires on law change (find the proven monetary/law-change on_action; DESIGN_LAW_EXPANSION PART E references guarded law-bias reads — confirm HOW those laws set their bias var: on_action vs option effect).
- `common/scripted_effects/se_QING_DECLINE.txt` — Layer 1 read #1: one guarded additive term into the qing_currency_stress recompute (:201-211).
- the CHI mint site (se_CURRENCY.txt or a Qing currency pulse se_) — Layer 1 read #2 lever (a), CHI-only guarded.
- `localization/english/laws_l_english.yml` — update option descs to state the REAL effect (mint discipline / stress), not just the cosmetic modifier.
- NO trade_goods, NO province/country blocks (no #219 flood risk — this is law + svalue + guarded var work).

## RISK
- **R1 [HIGH] — do NOT let any stance flip `paper_money_allowed`.** That uncaps `CURRENCY_minting_rate_cap` (→ 99999) → runaway M1 → directly destabilizes #23/#60. `issue_bonds` is the tempting candidate; keep it a bias (+) only, NOT a paper-money unlock. The paper-money transition is a separate, later, deliberately-gated mechanic — out of #63.
- **R2 [HIGH] — currency-core caution ([[currency sqrt root cause]], #60).** #63 must NOT edit shared currency svalues (`CURRENCY_minting_rate_cap`, backing_value, the gbip/sqrt chain). Only: set a Qing bias var, add ONE guarded additive term to the Qing stress recompute, and clamp the Qing mint rate CHI-only. Everything downstream (#23/#59) consumes those existing channels unchanged.
- **R3 [MED] — no-restoring-drift ratchet ([[no-restoring-drift ratchet rule]]).** The stress bias is a STANDING additive term (not a one-shot nudge), band-gated by the existing clamp — so it does not ratchet. Confirm the bias is re-read each pulse (a standing term), not accumulated.
- **R4 [MED] — magnitude.** The bias must be tuned so a debasement stance visibly raises monetary stress / loosens the mint WITHOUT swamping the opium_flow + reserve-ratio terms that dominate qing_currency_stress today. Small integer bias (e.g. ±5..±10 on a 0..100 meter). Verify on the #23/#51 econ logs (stress series is logged) — measure, don't guess.
- **R5 [MED] — capability: can a law option carry an effect?** If not, the bias-set must be an on_action on law change. This is the single unproven construct in #63; if unproven after checking the oracles/vanilla, it becomes a small BOOT SPIKE (per overnight Rule 1 hard-block #1), NOT a hand-wave.

## Verify (boot)
- The Qing (a monarchy) can now REACH the `monetary_policy_setting` stance group (Layer 3).
- Enacting `currency_recall`/`limited_minting` sets `qing_monetary_bias` negative → qing_currency_stress trends DOWN + the Qing mint rate cap tightens (mint slider ceiling lower); `more_minting`/`issue_bonds` → bias positive → stress up + looser mint. Confirm on the econ logs (stress series + minting_rate already logged in se_ECON_LOG).
- Default (no stance enacted / var unset): byte-identical to today (guarded reads).
- `paper_money_allowed` UNCHANGED by every stance (R1). M1 (#60) not destabilized. #23 sqrt/gbip stable.
- Loc: each option desc states its real mint/stress effect.

## Traps / rules
- Guarded reads (P7): every `qing_monetary_bias` read behind `has_variable`. No-op default byte-identical.
- No shared currency-core svalue edits (R2). CHI-only for the mint clamp.
- No macro `$param$`/`#` in LOG strings. RHS var-vs-literal only (bias reads are `add = var:qing_monetary_bias` — effect context, legal; any TRIGGER on the bias must be var-vs-literal).
- BOM/EOL: common/laws + loc = BOM; se_QING_DECLINE.txt — check its convention before editing (se_ files are usually no-BOM/LF, but VERIFY this specific file). No EOL churn.
- Reconcile with DESIGN_LAW_EXPANSION item 23 ("Monetary Response" / qing_monetary_bias) — #63 IS that wiring; if item 23 is later built, it must reuse #63's qing_monetary_bias var, not a parallel one. Cross-ref locked here.
- Capability check (R5) before writing the bias-set path.
- Design-note-first → adversarial review → implement → verify boot.

---

## ADVERSARIAL DESIGN-REVIEW CORRECTIONS (rev-63, 2026-08-10) — PROCEED-WITH-CORRECTIONS
Core mechanism (law-set bias var read at guarded pulse sites) is SOUND + proven in-repo. Three load-bearing claims were wrong/hand-waved; the boot-spike is unnecessary. These supersede the conflicting text above.

**#1 [MED] — CAPABILITY RESOLVED YES; DROP the R5 boot-spike.** Law options DO carry `on_enact = { … }`, used ~15× in `common/laws/00_qing_statutes_laws.txt` with `set_variable` for exactly this kind of bias var (qing_opium_posture :130/:134/:140; qing_caravan_customs_rate :151/:155/:159; qing_canton_regime :238/:243). `on_enact` fires ONLY on active enactment, NOT on default-hold at game start (:117-120) — which is what preserves byte-identity. => bias-set is `on_enact = { set_variable = { name = qing_monetary_bias value = N } }`; NO law-change on_action needed. DELETE R5's spike + the §Files "do law options take an effect block?" hedge (it's settled).

**#2 [HIGH] — NO CHI-only mint site exists (the design's lever (a) premise is wrong).** CHI mints via the SHARED `monthly_currency_pulse` (`on_action/economy/oa_wealth_changes.txt:111-133` → `CURRENCY_mint_currency` se_CURRENCY.txt:1381), tag-agnostic, one path for every country with official_currency. => reframe lever (a): a CHI-only, `has_variable = qing_monetary_bias`-guarded CLAMP of `var:CURRENCY_minting_rate` placed in the QING monthly pulse (the same one calling QING_DECLINE_recompute_currency_stress). CURRENCY_minting_rate is a standing player var, so clamping it CHI-side persists regardless of on_action ordering vs the shared mint pulse. Do NOT describe (a) as "where CHI mints."

**#3 [HIGH] — the mint-discipline lever is ONE-DIRECTIONAL (can only TIGHTEN).** CURRENCY_mint_currency hard-clamps CURRENCY_minting_rate DOWN to CURRENCY_minting_rate_cap every mint (se_CURRENCY.txt:1384-1392); the cap is the shared svalue R2 forbids editing. So a sound-money stance CAN tighten (clamp below cap), but `more_minting`/`issue_bonds` CANNOT push mint volume above the cap without editing the forbidden svalue — the "allow UP by the loose bias" in Layer 1 read #2 / §Concrete lever (a) is INERT. => state the asymmetry: loose stances act ONLY via read #1 (stress bias +) + the cosmetic modifiers; they do NOT raise mint volume. Drop the "loosen minting" claim.

**#4 [HIGH] — Layer 3 leaning (a) is a WORLD change, not a Qing fix.** Broadening to `OR={legislative/executive/delegated}` exposes the stance group + its commerce/tax/stability modifiers to EVERY non-tribal monarchy AI (executive is the default first option, is_tribal=no) — scope creep vs China-fine/ROW-abstraction + AI-eval churn. => scope Layer 3 to the target: `potential = { OR = { has_law = legislative_monetary_policy  tag = CHI } }`. Republics unchanged, Qing gains it, nobody else moves. VERIFIED NOT inert: Qing holds no explicit monetary law in setup/ → default-holds executive_monetary_policy → the CHI branch is satisfied; both groups already GUI-registered (government_view.gui:2048 law / :2124 setting) so the monarchy stance group will render.

**#5 [MED] — read #1 must hit the LEVEL, not the decaying residual.** Add qing_monetary_bias as a DIRECT additive term into the qing_currency_stress level (se_QING_DECLINE.txt:201-211, rebuilt from qing_curr_base_tmp each pulse → no ratchet). Do NOT route it through QING_DECLINE_nudge_signed / qing_currency_stress_residual (se_QING_OPIUM.txt:330/342), which DECAYS at 0.85 (:216-217) — a law bias must not decay. R3 (no-ratchet) holds ONLY on the direct-level path. (LAW_EXPANSION item 23 calls it a "nudge" — in THIS codebase that word means the decaying residual; ignore the wording, use the direct term.)

**#6 [MED/LOW] — no neutral first stance; byte-identity rests on the guard.** The setting group's first option is currency_recall (bias −); there is NO neutral (0) stance. Byte-identity still holds: on_enact doesn't fire on default-hold (var stays unset) + all reads has_variable-guarded. State two consequences: (a) once any stance is enacted the var is set and never cleared (on_enact only sets — no path back to bias 0); (b) with the CHI-scoping (#4) a dangling non-CHI bias is moot — otherwise `tag=CHI`-guard the on_enact.

**#9 [LOW] — BOM/EOL: the design missed CRLF on the law files.** `00_monetary_policy_setting.txt` + `00_administrative_laws.txt` = **BOM + CRLF** (editing tools must NOT convert to LF). se_QING_DECLINE.txt = no-BOM/LF (confirmed); se_CURRENCY.txt = BOM/LF; 00_qing_statutes_laws.txt = BOM/LF. If lever (a) edits oa_wealth_changes.txt, check its convention too.

**#10 [LOW] — mint clamp fights the player slider.** Implement as a CEILING (`if rate > bias_cap → set rate = bias_cap`), NOT an unconditional set, else it overwrites the player's slider (EE_scripted_guis.txt:440-541) each month. Consider reflecting the lowered ceiling in the slider max to avoid a tug-of-war.

**CONFIRMED SOUND:** #7 R1 paper_money safe (no stance flips it; issue_bonds bias-only OK); #8 NO #59 collision (bimetallic touches world gold:silver bullion market/reserve valuation, not qing_currency_stress/minting/M1 — different vars, cross-ref to LAW_EXPANSION item 23 correct, reuse the same qing_monetary_bias); PART D brace bug already fixed (3 balanced options).
