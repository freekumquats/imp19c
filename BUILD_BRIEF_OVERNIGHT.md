# Overnight content-agent BUILD BRIEF — READ FIRST

You are building ONE self-contained Qing office-coupling content feature for the
"Imperatrix: Victoria" mod (Imperator: Rome total conversion). Repo root:
`/Users/alan.chiang/github.com/imp19c`. Follow this brief EXACTLY. Your work is
reviewed adversarially afterward; correctness and convention-adherence matter more
than volume.

## THE CORE IDEA — the coupling-family pattern
Each great office of the Grand Council OWNS its natural charges, turning a static
office modifier into a live character relationship. Your feature makes ONE office's
domain come alive: (a) the office-holder's skill/loyalty GATES the outcomes+costs of
that domain's events; (b) the domain's charges join the character-affinity chart
against the holder; (c) a VACANT office = that domain drifts. Stay CONSISTENT with
the accountability metric that already judges that office and do NOT double-count it.

## HARD RULES (non-negotiable — from the project's standing rules)
1. **Concrete over abstract.** Prefer real characters, real provinces, real on-map
   objects (add_building_level, create_character, raise_legion) and REUSE existing
   counters over inventing new abstract meters. Only add a new variable if no existing
   one fits.
2. **se_LOG on every effect.** Every scripted_effect you write wraps its body in
   `LOG_enter = { sys = QING  fn = "<EffectName>" }` … `LOG_exit = { sys = QING  fn = "<EffectName>"  result = OK }`,
   and logs key branches with `LOG_line = { sys = QING  msg = "…" }`. Every event's
   `immediate` opens with a `LOG_line` naming the event. This is mandatory.
3. **Do NOT build on unproven engine capability.** Use ONLY the idioms listed in
   "VERIFIED IDIOMS" below, or idioms you can PROVE by citing an existing occurrence
   in this repo (grep for it). If you need something not proven, STOP and report it in
   your return payload as an OPEN ORACLE QUESTION rather than guessing.
4. **Only write NEW files.** Do NOT edit any shared file (the flavour-roll dispatcher
   se_QING_DECLINE.txt, the main loc yml, on_actions, existing se_/event/modifier
   files). Instead RETURN the exact splice text for those to the orchestrator (see
   "RETURN PAYLOAD"). This avoids write-collisions with other agents running in
   parallel. Creating brand-new files in common/scripted_effects/, common/modifiers/,
   common/scripted_guis/, events/imp19c_mod_events/, and localization/english/ is fine
   and expected — the engine auto-loads every file in those dirs.
5. **Author identity / commits.** Do NOT commit. The orchestrator commits everything
   as freekumquats. Just create files + return payload.

## BYTE CONVENTIONS (verify before finishing — use Python)
- `common/**/*.txt` and `events/**/*.txt`: **no BOM**, LF line endings, final newline.
- `localization/english/*_l_english.yml`: **UTF-8 BOM (ef bb bf)**, LF, final newline,
  and the file MUST start with `l_english:` on line 1 (after the BOM).
- Loc line format is Paradox's: ` KEY:0 "value"` — ONE leading space, then key, `:0`,
  space, quoted value. (Generic YAML linters mis-flag this; ignore those warnings.)
- Verify with:
  ```python
  raw=open(F,'rb').read()
  # for .txt: assert raw[:3]!=b'\xef\xbb\xbf' and b'\r' not in raw and raw.endswith(b'\n')
  # for .yml: assert raw[:3]==b'\xef\xbb\xbf' and b'\r' not in raw and raw.endswith(b'\n')
  # brace balance: s=raw.decode('utf-8-sig'); assert s.count('{')==s.count('}')
  ```
- Editing `.txt` reliably: write the whole file with Python (heredoc or Write tool),
  then brace-check. Tabs for indentation in .txt/.gui.

## VERIFIED IDIOMS (safe to use)

### Office-holder state (se_QING_COUNCIL.txt / se_QING_SEATS.txt)
- Each office holder is a country var: `qing_office_<key>_holder` holding a character
  reference. Keys: `chancellor personnel revenue rites war justice works censor
  lifanyuan grand_secretary zongli`. Dynastic seats: `emperor crownprince regent`.
- Guard EVERY deref: `if = { limit = { has_variable = qing_office_<key>_holder
  var:qing_office_<key>_holder = { is_alive = yes  employer = ROOT } } … }`.
- A character holding an office has `has_variable = qing_office_held` and
  `var:qing_office_held = flag:<key>`.
- Read the holder in country scope, e.g.:
  `var:qing_office_war_holder = { save_scope_as = the_minister }`.

### Character-affinity spine (se_QING_AFFINITY.txt) — the agree/disagree machinery
Call these inside a COURTIER's character scope (this = courtier), ROOT = CHI:
- `QING_char_affinity = yes` → scores compatibility with the throne into
  `var:qing_char_affinity` (0..100, 50 neutral). Pure read.
- `QING_char_bind = yes` → turns the score into loyalty + friend/rival of the throne.
- Mutators (each re-scores after): `QING_char_assimilate`, `QING_char_convert`,
  `QING_char_cultivate = { stat = finesse|martial|charisma|zeal  amount = <signed> }`,
  `QING_char_endow = { amount = <signed gold> }`,
  `QING_char_promote_standing = { pop = <signed>  prom = <signed> }`,
  `QING_char_honour_family = { amount = <signed prestige> }`,
  `QING_char_taint`, `QING_char_cleanse`, `QING_char_corruption = { amount = <signed> }`.
- PAIR FRICTION (transient, country scope, two saved char scopes):
  `QING_pair_friction = { a = scope:x  b = scope:y }` → sets `var:qing_pair_friction`
  (0..100, HIGH = they clash). **This is your "office-holder vs his charge agree or
  disagree" tool**: score the charge against the office-holder; high friction →
  dysfunction/recall event, low → they cooperate. Read it immediately; it is not stored.

### The affinity-chart coupling recipe (use this for #113/#117/#118 etc.)
To make a charge (governor / commander / resident) "report to" an office-holder and
be able to AGREE or DISAGREE with him:
```
# country scope; office-holder saved as scope:minister, the charge as scope:charge
QING_pair_friction = { a = scope:minister  b = scope:charge }
if = { limit = { var:qing_pair_friction >= 50 }  <clash outcome: recall/dispute event, loyalty/effectiveness hit> }
else = { <cooperation outcome: buff, loyalty, standing> }
```
You may ALSO score the charge against the throne with `QING_char_affinity`/`QING_char_bind`
where it fits (e.g. a loyal-vs-disloyal governor).

### Counters you should REUSE (do not reinvent) — all CHI country vars
`qing_corruption_level qing_currency_stress qing_reform_pressure qing_sect_pressure
qing_banner_decay qing_greenstandard_decay qing_bureau_capacity qing_selfstr_progress
qing_council_effectiveness` and GP tension `qing_gp_tension_britain/france/russia`.
Nudge a 0..100 counter with `QING_DECLINE_nudge = { var = <name>  amount = <signed> }`
(clamps 0..100). Do NOT set these raw.

### Event skeleton (country_event; the house style)
```
namespace = qing_<yourns>

qing_<yourns>.1 = {
	type = country_event
	title = "qing_<yourns>.1.t"
	desc = "qing_<yourns>.1.desc"
	picture = chinese_throne_room          # or senate_debate, senate, etc. — pick an existing one
	left_portrait = root.current_ruler
	right_portrait = scope:<a saved char>   # optional
	is_triggered_only = yes
	trigger = { tag = CHI  <extra gates> }
	immediate = {
		LOG_line = { sys = QING  msg = "EVENT qing_<yourns>.1 (<what>) [ROOT.GetTag]" }
		<save scopes>
	}
	option = {
		name = "qing_<yourns>.1.a"
		custom_tooltip = "qing_<yourns>.1.a.tt"
		<effects>
	}
	# 2-4 options, each a real trade-off. Gate options with their own trigger={} where apt.
}
```
Pictures that exist in-mod (safe): `chinese_throne_room`, `senate_debate`, `senate`.
If unsure, use `chinese_throne_room`.

### Concrete on-map object idioms (VERIFIED in-repo — grep to confirm before use)
- Buildings: `add_building_level = <building_key>` in a province/state scope. New
  buildings are defined in `common/buildings/*.txt` (see qing_governance_buildings.txt
  for the schema: cost, time, modifier, potential/allow, etc.).
- Legions/navies: `raise_legion = { create_unit = { … sub_unit = regular_infantry … } }`
  (see se_QING_COUNCIL.txt:373 QING_council_raise_grandee_legion and se_QING_SELFSTR.txt).
- Characters: `create_character = { … }` BUT never grant a modifier / loyal-veterans /
  culture-religion ref INSIDE the create_character block (verified #90 boot-crash);
  create first, then in a SEPARATE following effect apply modifiers / move_country.
- Vars can hold character references safely (se_QING_NAPOLEON.txt, se_QING_SEATS.txt).
- There is NO remove_character / banish in Imperator; end a character with `death = …`
  or move them with `move_country`, then `remove_variable` the stored ref.

## RETURN PAYLOAD (what you hand back to the orchestrator — put this at the END of
your final message, clearly delimited)
1. **FILES CREATED**: list every new file path you wrote.
2. **DISPATCHER SPLICE**: the exact `random_list` weight-entries to add to
   `QING_frontier_flavour_roll` in `common/scripted_effects/se_QING_DECLINE.txt`
   (weight int + trigger gate + trigger_event line), ready to paste. Keep weights in
   the 5–12 range consistent with the existing entries. If your feature is driven some
   other way (on_action, mission, dated event), specify that instead and give the exact
   hook line + which file it goes in.
3. **INIT SPLICE** (if you added any new counter needing a game-start seed): the
   `QING_<x>_init = yes` line for the on_game_initialized block, plus the init effect.
4. **SESSION_REPORT ENTRY**: a 3-6 line markdown blurb describing the feature, its
   files, its trigger, and its couplings — for SESSION_REPORT.md.
5. **OPEN ORACLE QUESTIONS**: anything you wanted to do but couldn't prove safe.
6. **SELF-CHECK RESULTS**: paste your byte-convention + brace-balance check output.

Keep the prose in events historically grounded and concise. Traditional Chinese
characters for court terms, as the rest of the mod does.
