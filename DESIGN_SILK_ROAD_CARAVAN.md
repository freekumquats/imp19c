# DESIGN — #370 Silk Road / Central Asian Caravan Trade-Node System (絲路商道 / 回疆貿易)

**Branch:** merge-overnight · **Status:** building · **Author:** freekumquats

## Thesis

After the Qianlong conquest of Altishahr (回疆, the Tarim Basin) 1755–59, a caravan trade
ran between Qing Xinjiang and the Central Asian khanates: tea, rhubarb, silk and silver went
west; horses, jade, cotton and dried fruit came east — funnelled through the oasis entrepôts
of **Kashgar (喀什噶爾), Yarkand (葉爾羌), Aksu, Khotan (和闐)** and, in the north, **Ili/Kulja
and Tarbagatai**. The Qing taxed it lightly (~5–10% ad valorem, levied chiefly at Yarkand),
ran the frontier at a fiscal **loss** covered by the 協餉 subsidy, and used commerce as a
**pacification instrument** — a prosperous oasis rebels less. The great historical crisis was
**commercial**: the Khanate of Kokand's escalating demands (the **aqsaqal 阿奇木伯克** consul,
the right to levy its own customs on third-party traders, extraterritoriality) culminated in
the **1832 settlement** — often called the first "unequal treaty" the Qing granted, a decade
before Nanking. Kokand weaponised the **White-Mountain khoja pretenders** (Jahangir 1826, the
Seven Khojas 1847) whenever its demands were rebuffed.

**#370 builds the caravan trade as a concrete economic layer that couples directly to the
existing Xinjiang consolidation arc (#367).** It is the frontier's *economic* twin: where #367
models the *grip* (garrisons, begs, tuntian, subsidy), #370 models the *commerce* (the trade
node, the customs rate, the Kokand concession) — and the two feed each other and the same
Lifan Yuan office-holder.

## Layer-don't-duplicate

- **Owns ONE new meter:** `qing_caravan_prosperity` (0..100, 商道繁榮) — the health/volume of
  the Kashgar–Yarkand trade. Joins the shared counter family (se_QING_DECLINE.txt), same
  clamped-nudge idiom (`QING_DECLINE_nudge`), same init, same band-swap.
- **Couples to #367, does not duplicate it:** prosperity reads and nudges the #367 grip meter
  `qing_xinjiang_control` (a prosperous oasis is easier to hold; a cut trade route frays the
  grip). The Kokand-concession lever couples to the SAME `qing_xj_kokand_emboldened` opinion
  and khoja-scare dynamics #367 already owns.
- **Grand-Council fold is the SAME office, a SECOND additive term:** caravan prosperity folds
  into the **Lifan Yuan (理藩院)** Director — the Court that historically governed Xinjiang
  trade relations — as term **(d)** inside `QING_ministry_recompute_perf_lifanyuan`, alongside
  the #367 consolidation term (c). Additive-inside (that recompute SETS the meter fresh each
  pulse), scaled small, so the two frontier terms are complementary, not double-counted.
- **Revenue:** the caravan customs pay a quarterly treasury trickle scaled by prosperity ×
  the customs rate — the historically-small-but-real fiscal contribution (net of the 協餉 the
  #367 arc already models as the cost side).

## State (CHI country scope)

| var | range | meaning |
|---|---|---|
| `qing_caravan_prosperity` | 0..100 | the trade-node health/volume (商道繁榮). Eases toward a recomputed target. |
| `qing_caravan_prosperity_target` | scratch | recomputed target the meter eases toward (hysteresis) |
| `qing_caravan_customs_rate` | 0/1/2 | 輕稅 light (5%) / 中稅 moderate / 重稅 heavy (15%+) |
| `qing_caravan_aqsaqal_granted` | flag | the Kokand aqsaqal concession is in force (1832-style) |
| `qing_caravan_yarkand_market` | int | count of market-infrastructure investments at the oases (cap 4) |
| `qing_caravan_initialized` | flag | init guard |

Reads/drives existing state: `qing_xinjiang_control` (#367 grip), `qing_xj_consolidation`
(#367 composite — the target reads it), `qing_xj_khoja_pending` (#367 scare), the `KOK`
opinion `qing_xj_kokand_emboldened`, the GP verbs (`QING_gp_react`/`QING_gp_grip_grace`).

## Engine (se_QING_CARAVAN.txt)

- `QING_caravan_init` — seed prosperity=45, customs_rate=1 (moderate), market=0; recompute.
- `QING_caravan_recompute_target` — target =
  base 40
  + `qing_xinjiang_control`/4 (a firmly-held frontier trades safely) — up to +25
  + `qing_caravan_yarkand_market` × 5 (bazaars/caravanserais) — up to +20
  + 8 if the aqsaqal concession is granted (Kokandi merchants flock in)
  − customs drag: light 0 / moderate −5 / heavy −15 (heavy tariffs depress volume + breed smuggling)
  − 15 if a khoja scare is pending (`qing_xj_khoja_pending`) — the route is cut
  clamped 0..100.
- `QING_caravan_pulse` (quarterly, from QING_GOV_pulse after QING_xj_pulse — reads its fresh
  grip/scare state): recompute; ease prosperity 1/4 toward target (hysteresis); pay the
  quarterly customs (prosperity × rate-factor /N → add_treasury); couple back into the grip
  (prosperity>=70 nudge `qing_xinjiang_control` +1; <30 nudge −1); offer the events.
- **Levers:**
  - `QING_caravan_set_customs` {rate} — set 輕/中/重. Heavy raises revenue-per-unit but drags
    prosperity + raises Kokand friction; light does the reverse.
  - `QING_caravan_invest_market` {} — spend treasury (−40), +1 market (cap 4), + prosperity,
    +1 step ILI integration (a thriving bazaar knits the oasis in). Mirrors the #367 tuntian lever.
  - `QING_caravan_grant_aqsaqal` — grant the Kokand concession (set flag): + prosperity + a big
    Kokand-relations lift (clear `qing_xj_kokand_emboldened`, add goodwill) + defuse the pending
    scare, BUT −prestige/−legitimacy (the "unequal treaty" humiliation) + a permanent customs
    revenue haircut (Kokand skims third-party duties). Set-once.
  - `QING_caravan_revoke_aqsaqal` — revoke it: restore sovereignty + revenue, BUT provoke Kokand
    (`QING_gp_react` russia-theatre? no — Kokand is not a GP; use the direct opinion + khoja-scare
    arming) + risk the khoja revolt (set `qing_xj_khoja_pending`-style pressure via a grip hit).

## Events (qing_caravan_events.txt)

- **.1 THE KOKAND ULTIMATUM (浩罕之求, ~1820s–30s):** offered when prosperity is high AND the
  aqsaqal is NOT granted AND Kokand is already emboldened (a festering khoja scare). Kokand
  demands the aqsaqal + customs rights. Options: GRANT (the 1832 settlement — QING_caravan_grant_aqsaqal),
  REFUSE & GARRISON (hold sovereignty, +grip cost, arm the khoja scare), TEMPORISE (buy time,
  small prestige cost, re-offers). Historically exact.
- **.2 THE ROUTE IS CUT (商道斷絕):** offered when a khoja scare is pending AND prosperity was
  high — the caravan trade collapses. Options: MILITARY ESCORT (spend treasury to reopen,
  +grip), NEGOTIATE VIA KOKAND (grant concession to reopen), LET IT LAPSE (prosperity crashes,
  revenue → 0 until the grip recovers).

Once-only offered flags set in each event's OWN immediate (the #366/#368 flag-leak fix).

## Panel (QING_caravan_panel.txt + gui/qing_caravan.gui)

Grand-Council-clone L4 window (clone of qing_xinjiang.gui): prosperity + grip read-outs, the
customs rate (3-way), the market count, the aqsaqal state banner, and the levers — set customs
(3 buttons, each is_valid mirrors "not already this rate"), invest market (treasury>=40 + cap),
grant aqsaqal (not granted), revoke aqsaqal (granted). Open button in government_view.gui after
the population (#369) button. menu_trade.dds icon.

## Proven-code notes

All primitives proven in-repo (no oracle): `QING_DECLINE_nudge` clamped counter (amount=var:),
`is_in_area`/`is_in_region` (se_QING_ILI), `add_treasury = var:` (se_QING_MECHANICS:675),
the #367 grip meter + Kokand opinion + khoja-scare vars, `SUBJ_QING_advance_integration`
(se_QING_XINJIANG tuntian lever), banded country modifiers, the ministry additive-inside fold
(#367 term c is the exact template for term d). No create_character (pure counter/lever model —
no #90 risk). Kokand is the NEIGHBOURING Turkic power (separatism-backer rule satisfied — this
reuses #367's KOK coupling, not a far-flung power).
