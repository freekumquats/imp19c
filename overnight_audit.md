# Overnight Audit — merge-overnight vs upstream (master)

**Scope:** ONE audit sweeping the entire `git diff master...merge-overnight`
(merge-base `8b2043a0f`; 1926 files, +247k/-28k) through THREE lenses, FIXING
everything found (nothing deferred). Working autonomously; all decisions logged here.

Standing rules in force: commits authored by freekumquats; PUSH after (user boot-tests
on a separate machine); extend canonical generators (tools/gen_table_icons.py,
gen_modifier_icons.py, gen_mission_headers.py) — never one-off scripts; "proven" = upstream
only. Cross-checked against the file-based engine-gotcha + open-boot-bug memories.

## Lenses
1. **Missing loc / placeholder icons** — referenced-but-undefined loc keys; blank /
   stopgap / all-identical icon families. Populate with suitable text + generator art.
2. **Bugs** — broken code, dangling references, wrongly-scoped modifiers, effects
   resolving to null, standing engine-gotcha crashes.
3. **Performance** — hot pulse/on_action work, unbounded iterators, uncapped ordered_*,
   per-tick recompute that can be cached/throttled. Trade a little accuracy for a lot
   of saved effort.

---

## Decision log

### Pre-audit — #116 finished first (was already in flight)
- `QING_GC_TITLES_UNASSIGNED_TT` enriched to name each of the 13 vacant Grand Council
  offices via per-office `SelectLocalization( qing_office_<key>_holder.IsSet, OK, VACANT )`.
  Added shared empty `QING_GC_SEAT_OK` + 13 `QING_GC_SEAT_VACANT_*` lines. Verified BOM,
  bracket/quote balance (13 SelectLocalization, 14 bracket pairs, 2 quotes). Committed
  `cd06a893a`. This is a Lens-1 (loc-enrichment) item; folded in.

### Findings (populated as the sweep runs)

Six discovery agents ran in parallel, partitioned by domain (logic / events+missions+guis /
defs / loc / gui / setup). Results consolidated below. NOTE: the logic agent's sweep was
shallow (3 tool calls over 187 files) and the gui agent ran while the safety classifier was
down — both cross-checked by hand before acting.

#### LENS 1 — MISSING LOC / PLACEHOLDER ICONS — FIXED

- **economic_enchancement_l_english.yml** (in-diff): 10 malformed loc headers FIXED —
  `KEY:0"…` (no space after version) on 7 debt-tooltip lines + `KEY: "…` (missing `:0`
  version) on 2 lines, plus one stray trailing `#!""` (double quote) on `issue_no_small_debt_allowed`.
  These are genuine parse hazards. Normalized to `KEY:0 "…`. BOM verified intact.
- **qing_household_l_english.yml** (in-diff): duplicate `QING_HAREM_FAVOUR_TT` (two DIFFERENT
  meanings — button vs favour-stat). The stat definition (line 196) was winning for BOTH via
  last-wins, so the "Favour a Consort" BUTTON showed the wrong tooltip. FIXED: renamed the
  button meaning to `QING_HAREM_FAVOUR_BTN_TT` and repointed gui/qing_harem.gui:208.
- **qing_treasure_fleet_l_english.yml** (in-diff): duplicate `qing_treasure_myriad_court`
  (line 97 dup of line 75). FIXED: deleted the dup pair; also lowercased the survivor's
  `_DESC`→`_desc` so the mission-task auto-derived description (lowercase) resolves.
- **technology_l_english.yml** (in-diff): duplicate `tech_electrochemistry`(+_desc). FIXED:
  removed the earlier EMPTY stub pair (line 407-408), kept the filled definition (line 733).
- **flavor_events_l_english.yml**: versionless `key: "value"` entries flagged by the agent are
  NOT in the branch diff (upstream "Merge flavour events from Zorgo") and the versionless form
  is a tolerated loc shape — LEFT AS-IS (out of scope, not a regression).
- Cross-file duplicate keys (subject-type labels, religion/culture names, etc.): these are
  intentional vanilla overrides or upstream overlap, NOT merge-overnight regressions — LEFT.
- **countries_l_english.yml: 28 bookmark-1763 tags shipped with NO name/adjective loc — FIXED.**
  26 of the 28 are active at game-start (would render as raw tag codes "MNZ", "VEN", …).
  Added `TAG:1 "Name"` + `TAG_ADJ:0 "Adjective"` for all 28: the HRE ecclesiastical/free
  cities (Mainz, Cologne, Trier, Salzburg, Würzburg, Bamberg, Münster, Paderborn, Osnabrück,
  Fulda, Passau, Konstanz, Eichstätt, Freising, Augsburg, Nuremberg, Ulm, Regensburg, Aachen,
  Rothenburg, Memmingen, Kempten, Palatinate), the Italian republics (Venice, Genoa), Milan,
  Lithuania, and (formable) Japan.

#### LENS 2 — BUGS

- **GC panel `.IsSet` on character-valued `qing_office_*_holder` (63 sites) — INVESTIGATED,
  NOT A CONFIRMED BUG, NOT CHANGED.** The gui agent (run without the safety classifier) claimed
  every office card's filled/vacant gating never renders because the holder vars are
  character-valued and `.IsSet` only works on flag/int vars ([[imp19c-gui-isset-character-var-quirk]]).
  Verified the vars ARE character-valued (`set_variable={name=qing_office_$office$_holder value=prev}`,
  se_QING_COUNCIL.txt:1370). BUT: (a) the quirk memory was proven on a CHARACTER scope
  (`Character.MakeScope.GetVariable`), whereas the GC panel reads off the COUNTRY scope
  (`GetPlayer.MakeScope.Var`); (b) this IS the shipped, screenshot-iterated flagship panel and
  every one of 13 cards uses the identical pattern — if broken, all cards would show
  permanently-vacant, which would be THE top boot-test bug, not the refinement-level vacancy
  the user reported. Mass-rewriting 63 working sites is the GUI repeat-failure trap the standing
  rule forbids. DECISION: leave as-is; flag for explicit boot-test confirmation. My #116
  tooltip deliberately uses this same proven-in-context pattern.
- **diplomatic_view.gui SUBJ_tab_selected `.IsSet` (country-valued)** — same reasoning; same
  country-scope pattern as the shipped subject tab. Not changed; flagged for boot-test.
- Logic / events / missions sweeps: no confirmed bugs. `pop_hapiness` is the canonical
  engine field spelling (vanilla), not a typo. Event-id / scripted-effect / ordered_*-max /
  event-throttle patterns all verified sound.
- **04_ideology_pantheons.txt "48 deities reference 15 missing svalues + 8 missing effects"
  (defs agent, CRITICAL) — FALSE POSITIVE, NOT CHANGED.** Verified `deity_*_svalue` and
  `*_apotheosis_*_effect` are BASE-GAME-provided definitions: they are referenced (never
  defined) identically across Invictus's shipping deity files, and the mod's own
  03_confucian_pantheon.txt (shipped, working) uses the exact same pattern. The new ideology
  pantheon follows the proven verbatim-clone structure. No missing definitions.

#### SETUP / WORLD DATA (setup agent)

- **"14 new setup/countries files carry a BOM → persistent reader rejects" (CRITICAL) — FALSE
  POSITIVE, NOT CHANGED.** Verified per [[imp19c-setup-reader-rejects-bom]]: the persistent
  reader rejects BOM ONLY on `setup/main/`, `setup/main/deities/`, `setup/post_character/`.
  `setup/countries/*.txt` are read by the COMMON lexer, which tolerates BOM — and EVERY shipped
  country file (new_south_wales, barbarians, angola, …) carries a BOM and boots fine. The 14
  new files match the existing convention. Touching them would be chasing a non-cause.
- **"MIL / JPN registered in countries.txt but absent from 00_default.txt" (CRITICAL) — NOT A
  BUG, NOT CHANGED.** This is the intended FORMABLE-ONLY tag pattern (JPN = "Meiji Japan, formed
  at Restoration #94"; MIL = "later refinement", territory currently held by LBV). The agent
  itself verified nothing references them as owner/subject at game-start, so no dangling-capital
  or null-owner crash. They activate only when formed.
- VERIFIED CLEAN by the agent (spot-confirmed): capital/ownership integrity (37 new tags, no
  ownerless capitals), setup character IDs contiguous 0..640, `setup/main/` + deity setup files
  BOM-free, province files' BOM intentional, no dangling owner refs.

#### LENS 3 — PERFORMANCE

- Quarterly `every_country { every_governorships }` economy pulse (oa_wealth_changes.txt) and
  the Qing quarterly mechanics pulse are the heaviest loads but are already throttled
  (quarterly + CHI-player-only) and the monthly variant was already disabled. Annual
  `every_owned_province` ethnic scan (se_QING_DECLINE) is annual + player-gated. No
  accuracy-for-speed change warranted; the throttling is the intended design. No action.

### Remaining
- #118 (tech icons) — SEPARATE from this audit; revert GUI to GetInventionIcon + fill icons.
- Commit + push all fixes (user boot-tests on a separate machine).
