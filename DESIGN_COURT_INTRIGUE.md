# DESIGN — Court Intrigue + Succession Deep Sim (宮闈鬥爭 / 立儲之爭) — task #368

**Branch:** merge-overnight. **Status:** BUILT. No oracle probe needed — every primitive is proven
vanilla (see §3).

## 1. Thesis — a CONCRETE roster of contending princes over the EXISTING abstract succession

The mod already models the succession *contest* abstractly: `qing_succession.1` (九子奪嫡 princes intrigue)
raises a bool `qing_succession_jockeying` flag and a `qing_succession_faction_strife` country modifier;
`qing_succession.2` resolves it smooth-or-disputed at accession off the `qing_secret_succession_sealed`
flag. What it LACKS — the concrete-over-abstract gap (the standing house rule) — is the *princes
themselves*: there is no on-map roster of the emperor's adult sons contending for the throne, no
per-prince court backing, and no way to seal the tablet on a *specific* prince (the whole point of
Yongzheng's 秘密立儲 reform, which broke the open 九子奪嫡 bloodbath by naming a hidden, specific heir).

#368 supplies that: a live roster of the reigning emperor's adult imperial princes (皇子), each carrying
a court-backing score; player levers to groom, investigate, and — the teeth — *secretly designate a
specific prince* as the sealed heir; and a coupling of the contest's divisiveness into the EXISTING
`qing_dynastic_harmony` meter. It does NOT duplicate the succession events' flags — it drives the same
`qing_secret_succession_sealed` / `qing_succession_jockeying` flags the existing `qing_succession.2`
accession event already consumes, so the two layers interlock.

## 2. The Grand-Council fold is ALREADY WIRED (D3 satisfied transitively — no new fold)

Like the Harem (#360) and Upper Study (#337) — which are dynastic institutions, not Grand Council
offices — the succession contest folds into the council through `qing_dynastic_harmony`:
`QING_council_recompute` additively converts `qing_dynastic_harmony` into `qing_council_eff_target`
(se_QING_DYNASTY.txt header: "additive conversion of qing_council_eff_target in QING_council_recompute").
A house torn by a succession war (`qing_dynastic_harmony` dragged down by prince-backing divergence)
gums up the council; a house with a sealed, secure succession lets the great offices work. #368 adds NO
new fold — it nudges the shared harmony thermometer, which the council already reads. The succession
belongs to the *emperor*, not an office, so the harmony coupling (not a per-office perf term) is the
historically and structurally correct one.

## 3. Proven primitives (all verified in-repo — NO oracle needed)

- **Adult-prince iteration** — `current_ruler = { every_child / ordered_child = { limit = { is_male
  is_adult is_alive } } }` is the proven child iterator (se_MARRIAGE.txt:310, ordered_child with
  order_by=age; the standard vanilla iterator per its own comment). Princes are born through the
  engine's OWN birth mechanic (the harem's `make_pregnant`, #360) so they are real family-graph
  children — NO `create_character` is used, sidestepping the #90 boot-crash rule entirely.
- **Name a SPECIFIC prince heir (秘密立儲 teeth)** — `add_triggered_character_modifier = { name =
  nominated_heir_modifier  duration = -1 }` on the chosen prince + `recalc_succession = yes` on the
  country is the vanilla designate-heir mechanic (common/scripted_guis/anoint_heir_button.txt:121/227).
  `nominated_heir_modifier` carries `support_for_character_as_heir = 50` (00_hardcoded.txt:468), which
  makes that prince the `primary_heir`. Only ONE nominee at a time — the vanilla button strips any prior
  `nominated_heir_modifier` before adding the new one; #368 mirrors that.
- **Per-character backing** — `set_variable` / `change_variable` on a character scope (proven across the
  office roster suite). Clamped 0..100 via the shared nudge idiom.
- **Ranking** — `combined_stats_council_svalue` (QING_governance_svalues.txt:11, char scope) to pick the
  ablest prince; `order_by = age` for seniority.
- **Harmony coupling** — `QING_dynasty_harmony_nudge = { amount = N }` (se_QING_DYNASTY.txt, clamped).
- **The existing succession flags** — `qing_secret_succession_sealed` + `qing_succession_jockeying`
  (set/consumed by qing_succession.1/.2 in qing_regency_events.txt) + `qing_office_crownprince_holder`
  (se_QING_SEATS.txt, hidden while sealed).

## 4. The prince roster + backing model

`QING_princes_recompute_roster` (quarterly + on panel open) rebuilds `qing_princes` (variable_list on
CHI) = the reigning emperor's living adult sons, and `qing_prince_count`. Each prince self-inits a
`qing_prince_backing` (0..100, char var) the first time he enters the roster (seeded from his
`combined_stats_council_svalue` + a base, so an abler prince starts with more court support — the
historical pattern).

**Backing drift (`QING_princes_pulse`):** while the succession is UNSEALED and ≥2 adult princes exist
(the 九子奪嫡 condition), each prince's backing drifts up a little and — crucially — DIVERGES: the ablest
gains, the rest hold, so a contest with no clear heir grows more polarised over time. The *spread*
between the top and bottom backing is the factional-strife signal: a high spread drags
`qing_dynastic_harmony` down (a court split between princely cliques). Sealing the succession freezes
the drift and lifts harmony (the object of the jockeying is gone).

## 5. Player levers (L4 panel + events)

- **FAVOUR A PRINCE (培植)** — grant the chosen prince prestige + raise his backing. Advances a clear
  front-runner (good if you mean to seal on him) but, while unsealed, inflames the losers (a small
  harmony hit — open favour is what fed the 九子奪嫡).
- **SECRETLY DESIGNATE THE HEIR (秘密立儲)** — the teeth. Pick a specific adult prince; apply
  `nominated_heir_modifier` + `recalc_succession` so HE becomes the `primary_heir`, and set
  `qing_secret_succession_sealed` so the existing accession event (qing_succession.2) delivers a smooth
  transfer. Ends the jockeying, lifts harmony, +legitimacy. The Yongzheng reform, made concrete.
- **INVESTIGATE AN OVER-MIGHTY PRINCE (查辦)** — a prince whose backing has grown dangerously high (an
  over-mighty son building his own faction, the Yinreng/Yinsi pattern) can be investigated by the
  Censorate: strip his backing hard, at a cost in prestige and a harmony risk (moving against a son is
  ugly). Gated on a prince actually being over-mighty (mirrors the effect guard — no dead click).
- **UNSEAL / REOPEN (廢儲)** — a sealed succession can be reopened (the historical Kangxi deposition of
  Yinreng): clears the seal + nominee, reopens the jockeying, costs legitimacy + harmony. High-risk.

## 6. Events (namespace qing_princes)

- `.1` **THE PRINCES CONTEND (奪嫡之爭)** — offered when the backing spread first turns dangerous under
  an unsealed succession: SEAL NOW (seal on the front-runner) vs GROOM THE ABLEST (favour, keep it open)
  vs STAND ALOOF (let it simmer — harmony risk).
- `.2` **AN OVER-MIGHTY PRINCE (儲位太盛)** — a specific prince's backing has grown alarming: CURB HIM
  (investigate/strip) vs ELEVATE HIM (seal on him now — accept the front-runner) vs WATCH.

## 7. File list

- NEW `common/scripted_effects/se_QING_PRINCES.txt` — init, roster recompute, backing drift, the four
  levers, the pulse.
- NEW `events/imp19c_mod_events/qing_princes_events.txt` — .1 the contest, .2 the over-mighty prince.
- NEW `common/scripted_guis/QING_princes_panel.txt` + `gui/qing_princes.gui` — the L4 panel (prince
  roster with per-prince backing + designate/favour/investigate buttons).
- NEW `localization/english/qing_princes_l_english.yml`.
- EDIT `se_QING_GOVERNANCE.txt` (call QING_princes_pulse in QING_GOV_pulse after QING_upperstudy_pulse),
  `qing_mechanics_on_actions.txt` (QING_princes_init at game start), `government_view.gui` (open button).
