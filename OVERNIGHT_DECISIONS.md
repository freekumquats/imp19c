# Overnight Autonomous Build — Major Decisions Log

Started 2026-07-07. Author of all commits: **freekumquats** (repo-local identity, per standing rule).
This file records the major decisions taken while implementing the pending task queue
autonomously ("implement everything without stopping"). One line per non-obvious call,
with the *why*. Companion to SESSION_REPORT.md (which gets the per-feature detail).

## Scope & review base
- **Review base = `origin/fix-usa-roster-create-character` @ `5a79ddcd`** — the latest version
  confirmed to work (per user). Everything in `5a79ddcd..HEAD` is in-scope for the final
  adversarial review. This is exactly "back from the Grand Council rework" (b12e1219 is the
  first commit after 5a79ddcd).
- Already committed on top of the base this session: `b12e1219` (Grand Council rework:
  council-is-offices + accountability), `919eddfd` (amban→grand_secretary rename + Dynastic
  Health panel #110).

## Cross-cutting architectural decisions
1. **The coupling-family pattern.** Each of the great offices OWNS its natural charges, turning
   a static office modifier into a live character relationship. Uniform spine for #108/#113/#117/
   #118/#121/#122/#123/#124/#125/#126: (a) the office-holder's skill/loyalty gates outcomes+costs
   of the domain's events; (b) the domain's charges (residents/governors/commanders/etc.) join the
   character-affinity chart against the holder via `QING_char_affinity`/`QING_pair_friction`
   (se_QING_AFFINITY.txt) — agree→effective+loyal, clash→dysfunction/recall events; (c) a VACANT
   office = that domain drifts. Each coupling stays CONSISTENT with the accountability metric that
   already judges its office (se_QING_ACCOUNTABILITY.txt) and must NOT double-count.
   - Personnel 吏部 ↔ governors (#117) | War 兵部 ↔ army/navy commanders (#118) |
     Works 工部 ↔ dikes/canal/wall + buildings (#121) | Rites 禮部 ↔ ceremonies/tribute (#122) |
     Lifan Yuan 理藩院 ↔ ambans/residents (#113) | Zongli 總理衙門 ↔ embassies/Great Game (#108) |
     Censorate 都察院 ↔ impeachment/remonstrance (#123) | Revenue 戶部 ↔ salt/granaries/silver (#124) |
     Justice 刑部 ↔ autumn assizes/penal code (#125) | Grand Secretary 內務府 ↔ privy purse/eunuchs (#126).
2. **Permanent vs appointable seats.** Emperor 皇帝 + Crown Prince 皇太子 (#115) and Grand Regent /
   Empress Dowager (#116) are a DISTINCT seat class — non-appointable, non-vacatable, excluded from
   the 11-office accountability loop, the appoint targets, the challenger search, and the vacate verb.
   They coexist with the existing Emperor Emeritus 太上皇 seat (Napoleon arc).
3. **Secret succession (秘密立儲) is the RESOLUTION mechanic, not flavour (#119).** Sealing the
   tablet damps prince-jockeying friction and yields a smooth transition; refusing/leaking reignites
   it — re-enacting Yongzheng's historical fix for the 九子奪嫡.
4. **Empress Dowager leads the regency (#116).** The living `current_ruler.mother` is styled 皇太后
   and is the FIRST-priority regent candidate (the 垂簾聽政 default), above prince/grand-councillor
   archetypes; carries the sharpest cling-to-power (Cixi) risk. Matches Invictus's own mother-first
   regency pick (oracle-verified).
5. **Concrete over abstract** ([[imp19c-concrete-over-abstract-rule]]) throughout: operate on real
   characters, real posts, real provinces, real buildings + `add_building_level`, and reuse existing
   counters (qing_corruption_level, qing_currency_stress, unrest, legitimacy, GP-tension) rather than
   inventing new abstract meters.

## Engine-capability decisions (oracle-verified; per standing oracle rule)
- **var-holds-character-reference is SAFE** (#113): verified in Invictus/Terra-Indomita AND our own
  se_QING_NAPOLEON.txt:124 / se_QING_CUSTOMS.txt:159. Post a resident with create_character at CHI →
  `move_country` to subject → mark with a `duration=-1` role modifier GRANTED OUTSIDE the
  create_character block (the #90 boot-crash gotcha). Store the link on the OVERLORD keyed by subject
  tag. Teardown = `death`/`move_country` + `remove_variable` (NO `remove_character`/`banish` in
  Imperator). Guard every deref with `has_variable` + `is_alive`.
- **Regency/seat idioms (#115/#116):** child = `current_ruler = { is_adult = no }` (adulthood = AGE
  16). Incapacity = `has_trait = incapable` (only first-class marker; PARTIAL — pair with `age >= 70`
  proxy). Succession hook = `on_ruler_change` (+ monarchy variant). No on_coming_of_age/on_trait_removed
  → auto-clear via a HIDDEN MTTH triggered event (Invictus ip_monarchy.52 pattern). Heir =
  `primary_heir` scope + `has_primary_heir` gate (monarchy-only). Mother = `current_ruler.mother`
  scope (guard exists+is_alive; `is_female` confirms) — Invictus regency literally saves it as regent.
- **Map modes (#109/#120):** Imperator map modes are engine-enumerated via SelectMapModesView, NOT
  freely CK3-style script-registered. FEASIBILITY must be confirmed at build; if a true custom map
  mode is unsupported, fall back to a province map-icon/highlight overlay or leverage the existing
  trade-good map mode, and LOG the limitation (no silent scope-cut). #109 and #120 SHARE this
  scaffolding decision — resolve once.

## Existing-state reuse decisions
- New World crops (#120) already modelled as trade goods (maize/sweet_potato/potato) with province
  vars `produces_*` (se_GOODS.txt) + spread effect `QING_COLON_spread_newworld_crops` (se_QING_COLON.txt).
  #120 is JUST a map mode reading that state — NO new diffusion mechanic.
- Revenue (#124) reuses common/buildings/qing_granary_buildings.txt (extend, don't duplicate) and the
  qing_currency_stress counter shown on the #110 Dynastic Health panel.
- Works (#121) defines NEW buildings in common/buildings/qing_works_buildings.txt matching the
  qing_governance_buildings.txt schema (河堤 / 漕運倉 / 長城).

## Byte & process conventions (enforced on every file)
- se_*.txt + events .txt: no-BOM, LF, final newline. loc .yml: BOM, LF, final newline. .gui: TAB indent.
- Every net-new effect wired to se_LOG (LOG_enter/exit/line, sys=QING) per standing rule.
- Every fix/feature: task-tagged in-code comment + se_LOG marker + SESSION_REPORT entry.
- Brace-balance + byte-convention check after each edit. Mandatory post-implementation review
  (the final adversarial workflow covers 5a79ddcd..HEAD).

## Per-feature decisions
<!-- appended as features are built -->
