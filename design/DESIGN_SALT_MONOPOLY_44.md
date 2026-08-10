# DESIGN — Salt Monopoly window + 兩淮鹽政 Salt Commissioner (#44)

**Status:** design note, 2026-08-10. Grounded in RESEARCH_QING_SALT_ADMINISTRATION.md (#45). Design-note-first → adversarial review → implement → adversarial review. Mirrors the proven Canton/Hoppo pattern (se_QING_CANTON.txt) end-to-end.

## What the user asked for (boot-test session)
1. "Should the salt monopoly sit under the Ministry of Revenue or Works" → **Revenue** (戶部 books the 鹽課; the Hoppo sits under the Imperial Household, so salt ≠ Hoppo's home).
2. "Create a new Salt Monopoly window and open it via button from the Ministry of Revenue panel."
3. "The Reform the Salt Gabelle button should live in the new Salt Monopoly window (and the effects should be updated)."
4. "Examine how the salt monopoly revenue is calculated, because it's pretty low right now (way below 12-15% of state income)."
5. "Salt revenue should be a function of the actual salt buildings / is salt a trade good? if so that should also be factored in." → **salt IS a trade good** (qing_salt_yard_building `trade_goods = salt`).
6. "Salt revenue should come from output + market price, but the concern was that market price is not a fair representation of historical value." → so **output-driven with a gabelle markup**, market price as a bounded/soft factor, NOT the raw sim price (the #52 finding: sim prices luxuries wrong; salt sits 0.1-1, a staple band — using raw price would understate the historically dear gabelle).
7. "Consider whether salt should only touch money or also touch silver reserves." → the 鹽課 was booked through the 戶部 as ordinary fiscal income (treasury/money); the Imperial-Household 鹽政 skim is the reserve-adjacent flavour. Decision below.
8. Research followup (#45, DONE): 兩淮鹽政 (Lianghuai Salt Censor / Chief Salt Commissioner) is the right single office — regional (Lianghuai dominant), IHD-linked, graded on finesse + corruption, historically abolished 1831/32.

## The current state (what exists, to build on)
- `QING_revenue_salt_income` (se_QING_REVENUE.txt): flat base-6 + reform±/graft± + a finesse≥8 minister +3 + realm-scale (num_of_cities/15, capped 14). Paid to treasury quarterly, published as `qing_salt_income_last`. **No salt-yard-output link, no market price, no dedicated salt character.** This is the "too low, not building-driven" the user flagged.
- `qing_revenue.1` ("Reform the Salt Gabelle"): 3-option event (reform / milk / defer), fired from QING_revenue_pulse, sets `qing_salt_gabelle_reformed` + the `qing_salt_gabelle_reformed_mod` / `qing_salt_gabelle_graft` country modifiers.
- `qing_salt_yard_building`: base_resources 2, trade_goods salt, seeded at Lianghuai/Changlu/Sichuan. **The concrete object salt revenue should scale on.**
- Canton/Hoppo precedent (se_QING_CANTON.txt): `qing_hoppo_holder` character, graded yield on finesse + `qing_hoppo_squeeze` (corruption), seated at game start, events + a panel card. THE template.
- Window-open idiom (PROVEN): `onclick = "[ExecuteConsoleCommand('n gui/imp19c_windows.gui <window>')]"` (qing_lifanyuan.gui amban picker, qing_guard.gui office picker).

## THE DESIGN

### A. The 兩淮鹽政 Salt Commissioner character (mirror the Hoppo exactly)
- **State var** `qing_salt_commissioner_holder` on CHI (parallel to `qing_hoppo_holder`).
- **Seat at game start**: mint an IHD-linked 兩淮鹽政 at boot the same way the Hoppo is seated (#66 pattern) — from the DEFERRED day-32 `qing_force_setup.12` (the #90-safe create_character placement, NOT construction). culture = manchu (IHD bondservant), religion = as Hoppo. NO modifiers inside create_character; deferred bind if any (mirror the Hoppo seat exactly — reuse its proven shape). Add a `qing_salt_commissioner` marker var so the office is identifiable + the panel renders him via `.GetCharacter`.
- **Grade on finesse + corruption** (the two-axis Hoppo pattern): a `qing_salt_yield_factor` svalue (parallel to `qing_canton_hoppo_factor`) = a multiplier from his finesse (competence → merchant-quota compliance, revenue reaching the 戶部) MINUS his corruption/`qing_salt_squeeze` (skim/patronage). Vacant office or high squeeze → less to the treasury.
- **Squeeze var** `qing_salt_squeeze` (parallel to `qing_hoppo_squeeze`): drifts up under a corrupt/venal commissioner, down under an honest one; feeds the yield factor + the skim.

### B. Revenue calc — output × market × gabelle-markup, character-graded (fixes "too low")
Replace the flat base-6 in `QING_revenue_salt_income` with a build-driven figure:
- **OUTPUT base**: count/​sum the salt-yard concreteness. Since salt is a trade good, scale on the salt-yard PROVINCES the empire owns — `every_owned_province { limit = { has_building = qing_salt_yard_building } }` summed, OR (simpler + proven) a scaled count via an ordered/every loop into a scratch var. Each salt-yard province contributes an output term (its `base_resources`-equivalent). This is the "function of the actual salt buildings" the user wants.
- **MARKET price factor**: salt IS a trade good, so factor the salt price — but BOUNDED, because (user) "market price is not a fair representation of historical value" and (#52 finding) the sim prices salt in the low staple band (0.1-1) while the historical gabelle was dear (7-14× markup over raw salt, per RESEARCH_TRADE_GOOD_PRICES_1763.md). So: use the salt price as a SOFT multiplier around a neutral 1.0 (e.g. clamp its contribution to ±30%), NOT the raw price — the price nudges revenue but a mispriced sim can't tank or balloon it.
- **GABELLE MARKUP**: the核心 — the monopoly's value is the tax wedge, not the salt's commodity price. Apply a fixed gabelle-markup multiplier (research: 7-14×; use a conservative in-engine constant tuned so total salt revenue lands at the historical **~12-15% of state income**, the user's target — currently "way below"). This markup is what makes salt a major revenue line rather than a minor commodity sale.
- **CHARACTER factor**: multiply by `qing_salt_yield_factor` (the commissioner's finesse − squeeze), so a capable honest commissioner delivers the full take and a corrupt/vacant one leaks it.
- **Result** = OUTPUT × market-soft × gabelle-markup × character-factor, floored ≥1, paid to treasury, published `qing_salt_income_last`. Tune the constants against the ~12-15%-of-income yardstick (needs the #51 econ logs to verify on the next boot — the salt price series is already logged).

### C. Silver reserve touch (user Q7)
The 鹽課 proper → **treasury/money** (as now; it's ordinary 戶部 fiscal income). The commissioner's **skim** (the IHD-conduit flavour, the Southern-Tours-financing angle from research) → a SMALL feed to the **silver reserve** (戶部銀庫 / silver_reserve_size) under a high-squeeze commissioner, mirroring how Canton's Hoppo skim feeds the privy purse/reserve. So: honest commissioner = more to treasury; corrupt = a slice diverts to the reserve (the emperor's accessible silver) instead of the state treasury — a concrete, historically-flavoured trade-off, and it ties the salt office into the existing reserve model (#42/#54) rather than money-only. Keep the reserve feed MODEST (the reserve model is CHI-tuned; don't destabilize #23/#42).

### D. Salt Monopoly window (new L4 window off the Revenue panel)
- **New window** `qing_salt_monopoly_window` in gui/imp19c_windows.gui (where the amban picker window lives), styled like the Revenue/Lifan panels (fixed scrollarea + cutoff + text-wrap per the standing GUI rules).
- **Opened by a button on the Revenue ministry panel** (gui/qing_revenue_ministry.gui) via the proven `onclick = "[ExecuteConsoleCommand('n gui/imp19c_windows.gui qing_salt_monopoly_window')]"` idiom.
- **Contents**: the 兩淮鹽政 commissioner's portrait + name + finesse/corruption (the Hoppo-card layout), the current quarterly 鹽課 read-out (`qing_salt_income_last`), the salt-yard province count, the squeeze level, the reform state (reformed / graft / untouched), and **the "Reform the Salt Gabelle" button MOVED here** (it currently only surfaces via the qing_revenue.1 event) — the button fires the reform effect (extracted from qing_revenue.1's options into a scripted_gui/effect the button can call), so the player reforms from the window, not only when the event happens to roll.

### E. Reform lever (move + update)
- Extract qing_revenue.1's reform/milk logic into a reusable effect (or scripted_gui) the window button invokes, so "Reform the Salt Gabelle" is a player-driven L4 action (like the Canton/Hoppo levers), not only an event roll. Keep qing_revenue.1 as the ambient/flavour path OR retire its reform option in favour of the button (decide in impl — leaning: keep the event as a prompt but have both routes call the same shared effect, no double-apply, guarded on `qing_salt_gabelle_reformed`).
- **Updated effects** (user "the effects should be updated"): the reform should now visibly move the NEW output-driven revenue (a reformed gabelle raises the character-factor / lowers squeeze), not just the old flat modifier — so the reform's payoff shows in the 鹽課 read-out.
- **Abolition endpoint** (research + on-map-object-lifecycle-symmetry rule): preserve room for a Tao-Zhu-style "abolish the salt censorate → ticket sales (票鹽法)" decision (1815+ / dynamic) that RETIRES the commissioner character (disband, not a dangling var) — scope a hook now, full build can be a follow-up if it balloons.

## Files
- se_QING_REVENUE.txt — rewrite QING_revenue_salt_income (output×market×markup×character); add the salt-commissioner seat + squeeze drift (or a new se_QING_SALT.txt if it grows — lean: new se_QING_SALT.txt mirroring se_QING_CANTON.txt, keep REVENUE lean).
- common/script_values/ — qing_salt_yield_factor svalue (finesse − squeeze), the output/markup svalues.
- events/imp19c_mod_events/qing_revenue_events.txt — update qing_revenue.1; extract the shared reform effect.
- common/scripted_guis/ — the window's scripted_gui backing (button visibility/effects) + the reform-button effect.
- gui/imp19c_windows.gui — new qing_salt_monopoly_window.
- gui/qing_revenue_ministry.gui — the open-window button.
- localization/english/ — window loc, commissioner title 兩淮鹽政, reform-button loc, read-out labels.
- qing_force_setup.12 (qing_force_setup_events.txt) — seat the commissioner at day-32 (mirror the Hoppo/#66 seat).

## Traps / rules
- create_character + add_trait ONLY from the deferred day-32 event (#90 boot-crash class), never construction — mirror the Hoppo/amban/#40 seat exactly.
- No modifiers inside create_character; deferred bind, no same-tick affinity read (#61 flood lesson).
- Reserve feed MODEST + CHI-only + band-gated so it can't destabilize the #23/#42 currency/reserve model (no-restoring-drift ratchet rule: band-gate the drift).
- Revenue tuning: verify the ~12-15%-of-income target on the #51 econ logs (salt price series already logged) — measure, don't guess; the gabelle-markup constant is the tuning knob.
- GUI: fixed scrollarea + cutoff + UNSIZED per the pantheon/missions scroll rule; paragraph text multiline=yes + fixed width (text-wrap rule); .IsSet renders only FLAG/INT not char-valued (GUI .IsSet quirk) — render the commissioner via .GetCharacter/.MakeScope, not .IsSet.
- Window-open: the proven `n gui/imp19c_windows.gui <window>` console idiom (NOT an unproven gui.createwidget form).
- se_/events no-BOM/LF; gui/loc BOM. Brace balance. Code-review before commit. freekumquats@users.noreply.github.com, merge-overnight.

## Verify (next boot)
- Ministry of Revenue panel shows a "Salt Monopoly" button; clicking opens the window.
- Window shows the 兩淮鹽政 commissioner (portrait/name/finesse/corruption), the quarterly 鹽課, salt-yard count, squeeze, reform state; the "Reform the Salt Gabelle" button is there and works.
- debug.log / econ logs: salt revenue is now output-driven and lands near ~12-15% of state income (up from "way below"); the character factor + squeeze move it; the modest reserve feed appears under a corrupt commissioner without destabilizing the currency chain.
