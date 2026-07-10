# Reverse-Merge Ledger (1763_bookmark → develop)

Tracks work done ON `1763_bookmark` that should later be merged BACK into `develop`.
`develop` was already merged INTO `1763_bookmark`, so new mechanics are being built here;
this ledger is the manifest for the eventual reverse merge.

## HOW TO READ THIS DOC — the merge-safety classification

Every change below is tagged so the reverse merge is mechanical:

- **[MECH]** — a MECHANICAL change: branch-agnostic engine/logic/GUI/content that is correct
  at ANY start date. **Merge to develop as-is.** (New helpers, bug fixes, new buildings, new
  reusable systems, GUI wiring, schema.)
- **[DATE]** — a DATE-SPECIFIC change: tuning that only makes sense at the 1763 start, almost
  always guarded by `current_date < X` / a start-era flag. **Do NOT blind-merge** — either it
  is inert at the 1815 develop start (guard already makes it a no-op → safe to merge) or it
  must be reviewed/adapted. Each [DATE] entry states which.
- **[MIXED]** — a file touched by BOTH; the merge must take the [MECH] hunks and evaluate the
  [DATE] hunks. Listed hunk-by-hunk.

Design rule the code follows (so [DATE] merges are safe by construction): every 1763-specific
branch is gated on `current_date < 1772/1793/1850/...` or a start-era flag, so at the 1815
develop start the guard is simply false and the pre-existing behavior runs unchanged. A [DATE]
change that is *purely additive behind such a guard* is therefore merge-safe even to develop —
it just never fires there. Entries note any exception.

---

## POST-MERGE AUDIT (all commits after the develop→1763 merge f73a6d16)

Post-merge commits: `71d66742` (doc), `096cd286` (doc), `bd5098dd` (territorial/ruler batch),
`1921f3b0` (#291), `6d121dc9` (#303), + uncommitted #304. #291/#303/#304 are detailed below;
this section covers the two doc commits + the bd5098dd batch.

- `71d66742` + `096cd286` — **1763_bookmark.md only** (doc reconciliation / obsolete-block
  delete). **[DATE/doc]** — 1763-branch documentation; does NOT merge to develop.

### bd5098dd — Territorial/ruler accuracy batch (mostly [DATE], with 3 [MECH] hunks)

- **[DATE]** `setup/main/00_default.txt`, `setup/countries/countries.txt`,
  `setup/countries/india/bengal.txt`, `setup/countries/n_america/louisiana.txt`,
  `setup/characters/00_Ottoman Empire.txt` (Qırım Giray), `00_Persian Empire.txt` (Karim Khan
  Zand), `00_West_Africa.txt` (Iyoas), `localization/english/countries_l_english.yml`
  (LSA/BNG/CRM/TRH/SFB names) — these ARE the 1763 map/roster: USA-as-GBR-colony, Spanish
  Louisiana, New Granada, Crimean Khanate, Zand Persia, Bengal, 1763 rulers. The DIRECT OPPOSITE
  of the 1815 develop state. **Must NOT merge to develop.** Pure bookmark setup.
- **[DATE]** `1763_bookmark.md` — doc, does not merge.
- **[MECH]** `events/imp19c_mod_events/gbr_empire_events.txt` — the gbr_empire.3 "Loss of America"
  release_subject=c:USA block (#289). Self-guarded on `exists c:USA` + `c:USA is_subject_of=ROOT`,
  so at the develop start (where USA is NOT a GBR subject) it is a clean no-op. Branch-agnostic +
  inert-at-1815 → merge-safe. (The rest of gbr_empire is unchanged.)
- **[MECH-safe]** `common/on_action/economy/oa_economy_setup.txt` + `imp19c_setup_events.txt`
  (imp19c_setup.1) — the #302 Spanish-American-war TIMING fix: `if current_date >= 1810 → fire
  now (as before); else → defer to 1810 via imp19c_setup.1`. At the develop start (current_date
  >= 1810) the `if` branch fires immediately = **byte-for-byte the original behavior**; the
  `else` deferral only ever runs at a pre-1810 (1763) start. So merging this to develop changes
  nothing there — it's a strictly-additive earlier-start guard. Merge-safe.
- **[MECH/doc-comment]** `fra_revolution_on_actions.txt` + `aus_habsburg/pru_ascendancy/
  rus_expansion/spa_bourbon_events.txt` — COMMENT-ONLY edits (the "no scripted GP wars" design
  note deleted/replaced with the #303 pointer, per the user directive). No code change. Merge-safe
  (harmless comment sync).

**Audit verdict:** the only genuinely [DATE] / do-not-merge material in the whole post-merge
history is the 1763 SETUP (map/roster/countries + the branch doc). Every CODE/LOGIC change
(gbr_empire.3 release, the #302 timing guard, the arc-comment sync, and all of #291/#303/#304
below) is either [MECH] or [DATE-guarded-inert-at-1815] — i.e. merge-safe. No post-merge change
would silently alter the develop 1815 start.

---

## #291 — ROW specialty production buildings + Qing works seed + Yunnan copper (COMMITTED 1921f3b0)

- **[MECH]** `common/buildings/row_production_buildings.txt` (NEW) — generic row_manufactory /
  row_plantation buildings (gated on trade-good family + NOT chinese_group). Branch-agnostic.
- **[MECH]** `localization/english/row_buildings_l_english.yml` (NEW) — their loc.
- **[MECH]** GUI wiring: `gui/shared/gui_templates.gui`, `gui/shared/custom_tooltip.gui`,
  `gui/province_window.gui`, `gui/macro_builder_view.gui` — build-menu + macro-builder widgets
  + tooltips for the two ROW buildings. Branch-agnostic (the build menu is a fixed widget list;
  a non-seeded building needs these to appear).
- **[MECH]** `common/scripted_effects/se_ROW_BUILDINGS.txt` (NEW) — SE_row_starting_buildings
  seeds the two ROW buildings across substantial non-Chinese economies at game start. Data-driven,
  branch-agnostic (runs identically at any start).
- **[MECH]** `common/scripted_effects/se_QING_BUILDINGS.txt` — QING_seed_works_building helper +
  Board-of-Works infrastructure seed (canal depots, Yellow-River dikes). Branch-agnostic.
- **[MECH]** `setup/provinces/00_Yunnan.txt` — province 502 (Panzhihua) grain → copper. This is a
  map/setup fact true at every start (the Jinsha copper belt), so MECH not DATE.
- **[MECH]** `common/on_action/economy/oa_economy_setup.txt` — call SE_row_starting_buildings after
  the Qing seed, in on_game_initialized. Branch-agnostic.

## #303 — American Rev / French Rev / Napoleonic wars as dated events (COMMITTED 6d121dc9)

- **[MECH]** `events/imp19c_mod_events/imp19c_setup_events.txt` — the war-declaration events
  imp19c_setup.2 (ARW), .3 (French Rev), .4/.5 (Napoleonic 1803/1805). The EVENTS themselves are
  branch-agnostic (self-guarded on tag existence + NOT war_with). Merge-safe.
- **[DATE / inert-at-1815]** `common/on_action/economy/oa_economy_setup.txt` — the dated SCHEDULERS
  (`current_date < 1775.4.19` etc.). At the 1815 develop start every one of these guards is false
  (the wars are in the past), so they never fire — safe to merge, inert there. This is exactly the
  behavior develop wants (it must not re-fight the ARW in 1815).

---

## #304 — Re-base develop Qing mechanics to the 1763 High Qing zenith (REVIEWED, uncommitted)

This task is the one that most needs the MECH/DATE split, because it deliberately branches
develop's 1815-tuned mechanics on the start date. The MECH parts are new reusable systems (the
Emperor Emeritus office, the era-gate pattern); the DATE parts are the 1763-zenith tuning, all
guarded so they are inert at the 1815 develop start.

### Deep adversarial review (14-agent workflow) — 2 confirmed defects, both FIXED; 6 refuted

- **[MECH-fix]** `events/imp19c_mod_events/qing_embassy_events.txt` — Macartney (.1) and Amherst
  (.2) both re-entered on the SHARED `qing_embassy_britain` flag, which either embassy's
  resolution sets. At the 1763 start both are dated-scheduled, so Macartney (1793) resolving
  poisoned Amherst's (1816) trigger → Amherst no-op'd → the sole path into `qing_napoleon.5`
  (the #65 Emeritus/Napoleon chain) went dead. FIX: each embassy now re-guards on its OWN
  occurrence flag (`qing_embassy_macartney_done` / `qing_embassy_amherst_done`, set in
  `immediate`). The resolution wrappers STILL set `qing_embassy_britain`, so the 1815
  flavour-roll suppression (se_QING_DECLINE.txt:1026) is byte-for-byte unchanged. Merge-safe.
- **[MECH-fix]** `events/imp19c_mod_events/qing_emeritus_events.txt` — in qing_emeritus.2 option
  .2.a the `add_legitimacy = 15` ran BEFORE `QING_emeritus_abdicate`'s `set_as_ruler`, so the
  new reign's legitimacy (reinit'd from `next_ruler_legitimacy`) wiped it — the tooltip's promised
  +15 never stuck. FIX: moved `add_legitimacy = 15` to AFTER the abdication call (mirrors the
  prestige-ordering care already taken + the qing_succession.2 post-change pattern). Merge-safe.
- Refuted (no change): High-Qing corruption seed 12 "band gap", plus 5 others — all traced to
  correct behaviour by the verify pass.

### SECOND deep adversarial review (whole uncommitted batch, 11-agent workflow) — 4 confirmed, 3 FIXED
- **[MECH-fix]** `common/scripted_effects/se_QING_MISSIONARY_STATIONS.txt` (#309) — pre-treaty station
  SPREAD (`QING_mission_spread_one_pretreaty`) had NO reach ceiling while SEEDING stopped at reach<6.
  Each station rolled a 5% daughter-chance every yearly pulse → exponential growth (~14yr doubling),
  which over the ~97yr 1763 pre-treaty window blankets the interior into the hundreds, defeating the
  documented "handful of communities, never a blanket" cap and pegging social friction at its 45 cap,
  which fed qing_sect_pressure and silently inflated White Lotus / Red Turban rebellion pressure. FIX:
  wrapped the spread in `limit = { scope:mission_owner = { var:qing_missionary_reach < 6 } }`, matching
  the seed cap (the in-pulse running reach count caps cumulative founding per pass, consistent w/ seed).
- **[MECH-fix]** `common/scripted_effects/se_QING_FACTION.txt` (#308) — `qing_lobby_kind` (persistent)
  was never reset in `QING_faction_form_bloc` and the derivation is gated on `NOT has_variable`, so the
  FIRST call froze the kind forever; if the council later flipped (stale kind = conservative but con
  wing now empty) the bloc gathered zero members, `scope:lobby_leader` was never saved, and
  qing_faction.4 (every option gates on `exists = scope:lobby_leader`) fired option-less → softlock.
  FIX: `remove_variable = qing_lobby_kind` at the top of the effect, forcing a fresh recompute.
- **[MECH-fix]** `common/scripted_effects/se_QING_FACTION.txt` (#308) — the conservative-leader
  `ordered_in_list` filtered on `has_variable = qing_lobby_neg_stance` (a scratch var that is set but
  never cleared), not current stance, so a member who drifted OUT of the conservative wing but kept a
  stale neg_stance could be picked as the bloc's leader. FIX: added `has_variable = qing_char_stance
  var:qing_char_stance <= -20` to the leader limit, matching the bloc/setter gate.
- **[RESOLVED — user chose KEEP absolute date gates]** `common/missions/qing_selfstrengthening_missions.txt`
  + the taiping/students/techtransfer date gates: the reviewer flagged that these `current_date>=` gates
  are NOT strictly inert at the 1815 start — they withhold content the 1815 player previously had
  immediately (self-str >=1860, taiping >=1850, students >=1872, techtransfer >=1860). USER DECISION
  (2026-07-10): KEEP the absolute date gates on BOTH starts — historical timing is the intended
  behaviour; the 1815 start no longer surfacing self-strengthening/taiping decades early is a desired
  improvement, not a regression. This is a deliberate, accepted behaviour change to the 1815 develop
  start; NOT a defect. No code change. (The "1815 behaviourally unchanged" invariant is waived here.)

### Macartney EMBRACE track — the early-industrialization divergence (洋務先聲), user-requested

- **[MECH]** `common/scripted_effects/se_QING_EARLYINDUS.txt` (NEW) — an alt-history early-
  industrialization arc launched from the Macartney embassy's new EMBRACE option (~67 years before
  the historical Self-Strengthening Movement). It deliberately REUSES the SS engine
  (se_QING_SELFSTR.txt): the SAME `qing_selfstr_progress` counter (so the SS bands / golden-age /
  wonder / refraction hollow-test all apply for free), `QING_selfstr_advance` (whose built-in
  bureau/council damping models the "far too early" friction verbatim), and `QING_selfstr_build`
  (real on-map buildings). Founds four era-appropriate 1790s institutions (火器局 foundry, 譯館
  translation bureau, 機器船廠 steam yard, 機器製造局 machine-works) with a heavy conservative
  backlash + a consolidate step. Branch-agnostic engine; self-guards on the
  `qing_early_industrialization` flag. **Merge-safe** and INERT at 1815 (the flag can only be set
  via the Macartney EMBRACE option, and Macartney only fires from the 1763 dated scheduler — at
  1815 the roll offers only Amherst, which has no embrace option — so the arc is unreachable there).
- **[MECH]** `common/modifiers/qing_embassy_modifiers.txt` — the 6 divergence modifiers (harbinger,
  4 institutions, conservative-reaction). Dormant defs on develop; only applied by the arc above.
- **[MECH]** `events/imp19c_mod_events/qing_embassy_events.txt` — the new `qing_embassy.1.embrace`
  option + the `qing_embassy.10` program hub. The embrace option self-guards on the divergence flag
  being unset; qing_embassy.10 self-guards on it being SET. Merge-safe (unreachable at 1815 as above).
- **[MECH]** `localization/english/qing_embassy_l_english.yml` — embrace option + hub + modifier loc.
- **Adversarial review (11-agent workflow): 2 confirmed defects, both FIXED.** (1) the hub's
  "later" option had no body, so picking it closed the program forever (the found-* options each
  re-queued the hub, "later" did not) — FIXED: "later" now re-queues qing_embassy.10 unless already
  consolidated. (2) the four foundings total exactly 40 progress at full rate but
  QING_selfstr_advance halves each gain under weak 1790s machinery, and consolidate gated at ≥40
  (zero headroom) → one halved step stranded the player with the malus stuck — FIXED: both
  consolidate gates lowered 40→20 (reachable even fully-halved 4+5+5+6=20; the four-modifier
  requirement still proves the program was built). 1815 invariant untouched by both fixes.

### [MECH] — merge to develop as-is (new reusable systems / era gates that are correct anywhere)

- `common/defines/00_defines.txt` — **`MINIMUM_COLONISATION_POP` RE-ENABLED 99999 → 8** [user].
  Was a disable-sentinel from when the mod replaced fiat colonisation with the se_MIGRATION.txt
  bottom-up pull system; user wants the state to drive BOTH the migration-pull layer
  (migr_gov_pull, se_QING_COLON.txt) AND native engine colonisation. 8 = the TI-proven default; at
  this mod's ~4,500-people/pop scale an 8-pop source (~36k people) is a plausible colonist wave.
  GLOBAL engine define, NOT date-gated — applies to develop too (both starts get native
  colonisation back alongside the migration engine). Merge as-is.
- `common/scripted_effects/se_QING_EMERITUS.txt` (NEW) — the historical Emperor Emeritus (太上皇)
  abdication mechanic. GENERIC + reusable (any 60-year-reign emperor); not 1763-specific. The
  char:214-Qianlong preference inside qing_emeritus.2 is a data detail, not a date gate.
- `events/imp19c_mod_events/qing_emeritus_events.txt` (NEW) — qing_emeritus.1 checker + .2 offer.
  Generic (fires whenever an emperor reaches age 84 with an adult heir).
- `localization/english/qing_emeritus_l_english.yml` (NEW) — Emeritus loc.
- `common/on_action/00_specific_from_code.txt` — the Emeritus death hook in on_character_death.
  Branch-agnostic (self-guards on the emeritus office flag + qing_emeritus_active).
- `common/modifiers/qing_mechanics_modifiers.txt` — the qing_high_qing_prosperity modifier
  DEFINITION. Harmless to merge (only applied by the date-gated seed below); a dormant modifier
  def on develop is inert.
- **Era-gate sweep (all [MECH]-safe because current_date-guarded → inert or historically-correct
  at 1815):** the date-gates added to
  - `common/missions/qing_taiping_missions.txt` (potential += current_date>=1850) — at 1815
    develop this correctly blocks the tree until 1850, matching history. Merge-safe.
  - `common/missions/qing_selfstrengthening_missions.txt` (potential += current_date>=1860) — ditto.
  - `common/scripted_guis/QING_mechanics_actions.txt` (techtransfer button >=1860, students
    button >=1872) — ditto; blocks the 1815-1860/1872 window, historically correct on develop too.
  - `common/scripted_effects/se_QING_DECLINE.txt` Golden Urn roll-weight += current_date>=1793 —
    always-true at 1815 (>=1793), so a pure no-op there. Merge-safe.
  NOTE: these era-gates arguably IMPROVE develop too (they stop the 1815 game from surfacing
  self-strengthening/taiping/etc. a decade+ before their historical dates). Recommend merging.

### [DATE] — 1763-zenith tuning; guarded so INERT at the 1815 develop start (merge-safe but never fires there)

- `common/scripted_effects/se_QING_DECLINE.txt` — the High Qing era branch in QING_DECLINE_init
  (`current_date < 1772.1.1` → set qing_high_qing_era + grant prosperity + seed low corruption 12);
  the pulse creep + reaction-roll suppression gated on `NOT has qing_high_qing_era`. At 1815
  (current_date >= 1772) the era flag is never set → develop behavior byte-for-byte unchanged.
- `common/scripted_effects/se_QING_DYNASTY.txt` — date-aware harmony seed (82 if <1772 else 50).
  At 1815 → the original 50. Unchanged on develop.
- `events/imp19c_mod_events/qing_decline_events.txt` — qing_decline.40 (Heshen checker) + .41
  (inflection) + their loc in `qing_mechanics_l_english.yml`. Only armed by the <1772 scheduler;
  at 1815 never armed. The .41 event def is harmless (its trigger requires qing_high_qing_era,
  never set at 1815).
- `common/scripted_effects/imp19c_effects_legion_setup.txt` — the `current_date < 1772` High Qing
  OOB branch in SE_qing_armies (larger, commander-less). At 1815 → the else branch = the original
  1815 OOB, unchanged.
- `common/scripted_effects/se_QING_GREATGAME.txt` — the `current_date < 1793` tension-drift
  suppression. At 1815 (>=1793) → the else_if/else chain = original behavior, unchanged.
- `setup/characters/00_Qing.txt` — char:214 first_name → "Qianlong Emperor". **[DATE, review on
  merge]:** this is a display string on the 1763 reigning emperor. On develop (1815) Qianlong is
  long dead / not the ruler, so it's cosmetically harmless, but confirm no develop content keys
  off his name. Low risk.
- `common/on_action/economy/oa_economy_setup.txt` — the schedulers for qing_decline.40 (@1772),
  qing_emeritus.1 (@1794), qing_embassy.1/.2 dated British embassies (@1793/1816, sets
  qing_embassy_dated_schedule). All `current_date < X` guarded → inert at 1815. **[MIXED]** file:
  also holds the [MECH] SE_row_starting_buildings call (#291) and the [DATE] #303 war schedulers.

- `common/scripted_effects/se_QING_DECLINE.txt` embassy-roll tweak: the British-embassy roll-weight
  now also gated `NOT has qing_embassy_dated_schedule`. **[MECH-safe]:** at 1815 that flag is never
  set (only the <1793 scheduler sets it), so the roll offers Amherst exactly as before. Merge-safe.

### research (informational, not merged as code)

- `research/1763_HIGH_QING_mechanic_adaptation.md`, `research/1763_MISSIONARIES_pre_treaty.md` —
  research digests. Keep on both branches or wherever useful; no runtime effect.

---

## #309 — Missionary rework: active-but-low pre-treaty (IMPLEMENTED, uncommitted) — **[MECH]**

Start-agnostic and CORRECTS develop too: the old code gated ALL mission activity on
`qing_treaty_system_imposed`, so missions were fully dormant until 1858/60 — wrong at both starts
(Christianity was physically present ~280 years pre-treaty). The rework splits the single meter
and un-gates the station layer into two modes. No 1763-only date hunk — the whole feature keys off
the treaty flag, not the date, so at the 1815 develop start the 1815→1860 window now correctly
shows a small tolerated presence instead of nothing. Merge as-is.

- **[MECH]** `common/scripted_effects/se_QING_MISSIONARY.txt` — new `qing_mission_social_friction`
  meter (民教相爭, the ever-present SOCIAL irritant, capped low), driven at EVERY era; the political
  `qing_antichristian_sentiment` meter now drifts toward its target ONLY post-treaty (else bleeds to
  0), so it stays ~0 pre-treaty (no consuls = no political stake). Agitator + Boxer boil-over stay
  gated on the political meter (treaty-era only). New social band + pre-treaty local-crackdown
  handlers (`QING_missionary_tolerate_local` / `_suppress_local`, domestic-only, no GP touch).
- **[MECH]** `common/scripted_effects/se_QING_MISSIONARY_STATIONS.txt` — `QING_mission_stations_pulse`
  un-gated from the treaty flag; two modes. Pre-treaty: `QING_mission_seed_pretreaty` (slow, capped
  at ~6 stations at top-population interior provinces), `QING_mission_convert_pops_pretreaty` (thin
  trickle, local friction only), `QING_mission_spread_one_pretreaty` (5% creep). Post-treaty: the
  existing aggressive treaty-port mode, unchanged.
- **[MECH]** `common/modifiers/qing_missionary_modifiers.txt` — `qing_mission_social_unease` band
  (no diplomatic_reputation component — the tell that it is social, not political).
- **[MECH]** `events/imp19c_mod_events/qing_missionary_events.txt` — new `qing_missionary.2`
  pre-treaty local heterodoxy scare (tolerate/suppress, zero foreign stake).
- **[MECH]** `common/scripted_effects/se_QING_DECLINE.txt` — flavour-roll: `qing_missionary.1`
  (political 教案) now also gated `has qing_treaty_system_imposed`; new pre-treaty branch fires
  `qing_missionary.2` when social friction ≥25 and NOT treaty-imposed.
- **[MECH]** `gui/qing_religion.gui` + `localization/english/qing_religion_panel_l_english.yml` +
  `qing_missionary_l_english.yml` — surface the social meter in the panel; relabel the political
  meter "Anti-Foreign"; corrected the reach/anti-Christian tooltips for the new two-meter model.

---

## Queued (not yet built) — will be logged here as done

- **#307** — #165 sphere PULL rebuild — **[MECH]**, IMPLEMENTED (uncommitted, pending review).
  `common/scripted_effects/se_QING_SPHERE.txt`: added a PULL neighbour-diffusion layer on top of
  the existing PUSH sources — a two-pass pulse (pass 1 snapshots every ring state's four scores
  into *_influence_snap; pass 2 bleeds each state 1/4 toward the strongest adjacent contested
  march's snapshot, then runs the original push/decay/clamp/cap/recompute tick). Uses only proven
  idioms: cross-state `scope:X.var:Y` numeric read (now PROVEN per the probe), persistent-var
  arithmetic (subtract/divide), macro-in-varname `var:$power$_influence_snap` (4 fixed literals).
  Preserves the #277/#280 fixes (variable= iteration, frontier cap, nested-subject ring, is_home
  chain). Header design note updated (PUSH-only → PUSH sources + PULL diffusion; the PROVEN verdict
  cited). Removed the throwaway probe files (`se_SPHERE_probe.txt`, `on_action/SPHERE_probe_debug
  .txt`). Start-agnostic → merge to develop as-is.

---

## #308 — Grand Council 5-part deepening (IMPLEMENTED, uncommitted) — all **[MECH]**

Start-agnostic reusable social layer over the existing council/faction/affinity engines. All five
parts merge to develop as-is (they enrich the shared Qing machinery; nothing is date- or
start-gated).

- **[MECH] A — affinity/faction cross-wiring.** `se_QING_FACTION.txt`: new `QING_faction_ripple`
  = { favoured slighted } — a council decision now ripples through the WHOLE roster along the
  engine's own is_friend/is_rival relations + shared qing_char_stance (a favoured man's friends +
  fellow-partisans are gratified, his rivals + opponents affronted). Wired into all three
  `qing_faction_events.txt` decisions (reform memorial back/hold, Dowager defer/defy, deadlock
  purge) — the user's "Empress lobbying for one annoys his rivals, satisfies his friends" made
  general. O(offices), pure relation reads.
- **[MECH] B — tenure accrual surfaced in the statesmanship bar.** `qing_governance_modifiers.txt`:
  the `qing_officeholder` character modifier (already on every seat) gains
  `monthly_character_experience = 0.10`. Time in office accrues the engine's own character
  experience, which the statesmanship bar (`government_view.gui` `[Character.GetExperience]`)
  already renders — so a seasoned minister visibly outgrows a fresh appointee. Zero new GUI.
- **[MECH] C — Empress / Grand Regent / Emperor Emeritus as faction anchors.** `se_QING_FACTION.txt`
  `QING_faction_recompute`: added the three missing figurehead anchors (Empress weight 2, Regent
  weight 3, Emeritus weight 3) alongside the existing Emperor/Dowager/Crown-Prince — mirrors the
  effectiveness figureheads in `se_QING_COUNCIL.txt`, so faction + effectiveness see the same court.
  Each guarded on presence exactly as its effectiveness counterpart.
- **[MECH] D — Han / Manchu / OTHER ethnic balance.** `se_QING_COUNCIL.txt`: new
  `QING_council_classify_ethnicity` helper (replaces the duplicated Manchu/else-Han logic in both
  score fns) — three buckets: Manchu (dynasty culture) / Han (chinese_group) / Other (Mongol/
  Tibetan/Turkic, esp. Lifan Yuan). New `qing_council_other_count`; the balance bonus now gives the
  +15 滿漢並用 dyarchy plus a further +5 for a broad court that also seats an Other grandee (因俗而治).
  `government_view.gui` + `qing_governance_l_english.yml`: the balance readout is now 滿/漢/其他.
- **[MECH] E — sinicization drift on the council.** `se_QING_COUNCIL.txt`: new
  `QING_council_sinicize_drift_one` + a ~yearly-throttled pass in `QING_council_recompute` — every
  seated member + the throne row edges toward the Han pole (漢化) via
  `QING_char_shift_identity` (se_QING_MECHANICS.txt), EXCEPT conservatives (traditionalist trait /
  zeal≥12 / staunch identity≥80) who hold the line or harden; reformers drift faster. Generational,
  not quarterly (self-throttled 365 days).

### #308 follow-ups (user, mid-build) — all **[MECH]**

- **A2 — affinity-aware TARGET SELECTION.** `se_QING_FACTION.txt`: new `QING_faction_pick_ally` /
  `QING_faction_pick_foe` (+ `QING_faction_score_court_favour`) rank the roster by affinity +
  faction-alignment-with-the-ruler + friendship/rivalry of the emperor, saving scope:qing_picked_ally
  / _foe. Wired so POSITIVE beats fall on allies (qing_office.8 councillor memorial) and NEGATIVE
  beats on foes (qing_office.10 clique ringleader), each with a fallback to the prior pick. (Fixed
  saved-scope names — $MACRO$-into-save_scope_as is unattested in this codebase, so avoided.)
- **religious tension → outright rebellions (White Lotus / Red Turban).** `se_QING_MISSIONARY.txt`
  pulse now nudges `qing_sect_pressure +1` while religious tension runs high (social friction ≥30 OR
  political sentiment ≥40) — Christianity was lumped with the 邪教 sects. `se_QING_DECLINE.txt`
  `QING_rebellion_roll`: the White Lotus (qing_rebellion.1) and Red Turban (qing_rebellion.7) gates
  gain an OR religious-tension ignition path (sect pressure + high mission friction / anti-foreign
  fury), so a religiously-inflamed realm can tip into the historical risings even with modest graft.
- **collective lobbying (聯名上奏).** `se_QING_FACTION.txt` `QING_faction_form_bloc` assembles a
  lobbying bloc (usually factional — reformist/conservative caucus — but ~25% a cross-aisle issue
  coalition), picks its spokesman + kind. New `qing_faction.4` event (concede / face-down / co-opt
  the spokesman) + flavour-roll branch. The whole bloc reacts collectively.
- **occasional ALIGNMENT SHIFTS + faction squares in the GC UI.** Officials now drift
  reformist/conservative over time: `QING_char_stance` folds in a persistent `qing_stance_drift`
  moved by new `QING_char_stance_shift`; `QING_faction_drift_alignments` (yearly, from the recompute)
  gives each non-committed member a 20% chance to shift, usually bandwagoning to the ascendant wing.
  UI (`gui/shared/gui_base.gui` `qing_faction_square` + `qing_favor_square_max`, wired onto all 17
  GC title rows in `government_view.gui`): a SECOND title-row chip beside the Imperial Favor square
  shows each holder's alignment — BLUE reformist / YELLOW conservative / GREY neutral, live off
  `qing_char_stance`; the Emperor's Favor square is forced max-green (throne favours itself). Hover
  tooltip `QING_GC_FACTION_COLOR_TT` explains the colours. (Text-tint approach was prototyped then
  dropped for the cleaner second-square per user; the two custom colour formats in textformatting.gui
  are reused by the tooltip.)
- **A2 target selection also gained** the affinity-aware ally/foe pickers noted above.

---

## #311 — Dynastic-marriage FULL BUILD (IN PROGRESS, uncommitted) — **[MECH]**

Grounded in native-language 18th-c. dynastic research (`research/1763_ROYAL_MARRIAGE_diplomacy.md`,
15 design hooks). Extends the existing #276 skeleton (alliance-on-marriage / heirless→union→
inheritance) with the missing dimensions the history demanded, ADDS the player-facing L4 GUI, and
ENABLES the Qing. Start-agnostic (a dynastic layer, not date-gated) → merge to develop as-is. The
1815 develop start already ran the skeleton; the new gates/dowry/betrothal enrich it at both starts.

Isolated from the big Qing batch (marriage files don't overlap it) — will get its own review.

### Done so far
- **[MECH] `common/scripted_triggers/00_marriage_triggers.txt`** (rewritten) — the ELIGIBILITY
  GATES (hooks #1/#7): `MARRIAGE_eligible_realm_trigger` (dynastic monarchy, no longer excludes CHI),
  `MARRIAGE_western_house_trigger` (the Western Christian free-marriage bloc), `MARRIAGE_same_faith_
  trigger` (cross-scope religion compare), `MARRIAGE_pair_compatible_trigger` (same-bloc OR same-faith
  OR a forged bridge), `MARRIAGE_needs_bridge_trigger` (the cross-confessional case that needs a
  dispensation/conversion — the Catherine-née-Sophie pattern). CHI enters the system but a CHI↔Western
  match is hard-gated behind the bridge, matching the real absence of any Sino-European marriage tradition.

### DONE (this build) — all [MECH], isolated from the Qing batch, own review pending
- **`se_MARRIAGE.txt`** — 7 new verbs: `MARRIAGE_grant_dowry_claim` (#3 dowry = +30k wealth + a
  border claim for a deep bond), `MARRIAGE_forge_bridge` (#7 dispensation/conversion, the ONLY road
  across the confessional/cultural line — mutual `marriage_bridge_partners` list), `MARRIAGE_betroth`
  (#15) + `MARRIAGE_repudiate` (#5 = -60 jilted opinion + break_alliance + -30 prestige),
  `MARRIAGE_check_decay` (#2 aged alliances lapse via a 30-yr self-expiring timer; bond remains),
  `MARRIAGE_apply_dysfunction` (#10 loveless zeal-gap match → court-discord modifier),
  `MARRIAGE_press_succession_claim` (#8). Pulse re-gated: the AI only makes COMPATIBLE matches
  (save home as scope:target, MARRIAGE_pair_compatible_trigger); form_pact now pays a dowry, stamps
  the decay timer, checks loveless dysfunction; L3 inheritance now branches to a CONTESTED war-claim
  when a near-equal rival also holds a marriage bond (guarded by union_contested; clean transfer
  skipped). MARRIAGE_check_decay added to the pulse.
- **`common/scripted_triggers/00_marriage_triggers.txt`** — eligibility gates (#1/#7): CHI no longer
  excluded; `MARRIAGE_western_house_trigger`, `MARRIAGE_same_faith_trigger`, `MARRIAGE_pair_
  compatible_trigger`, `MARRIAGE_needs_bridge_trigger`, all reading the other house as scope:target
  (bound by the GUI's saved_scopes + the pulse's saved home — legal in both trigger + effect ctx).
- **`MARRIAGE_power_parity_trigger`** REWORKED [user]: the equal-standing gate no longer uses the
  formal RANK enum ("what you described is more like rank") — it now compares the mod's OWN
  economic+military great-power SCORE `DIPLOMACY_power` (economy+military+tech+recursive subjects+
  admin+stability). A pair is comparable when neither house's power exceeds 3× the other's. The 3×
  band is hoisted into **`common/script_values/MARRIAGE_svalues.txt`** (NEW, `MARRIAGE_power_x3_own`)
  and read cross-scope via the PROVEN `scope:target.<svalue>` idiom (a value-block trigger RHS is
  unattested; the direct `DIPLOMACY_power <= scope:X.DIPLOMACY_power` compare is proven in
  imp19c_additional_triggers.txt). NOT the cached var (`DIPLOMACY_power_base_cached` is set+removed
  within one loop, never persists — must eval the svalue live).
- **`common/scripted_guis/MARRIAGE_actions.txt`** (NEW) — the L4 player interface as country-target
  scripted GUIs (sell_provinces idiom): propose / seek-bridge / betroth / repudiate, CHI-enabled.
  PLUS `marriage_open_candidates` (country scope) — builds the candidate datamodel: every foreign
  eligible dynastic monarchy in diplomatic range fielding a marriageable child → `marriage_candidates`
  variable-list, caching each realm's + ROOT's `DIPLOMACY_power` into `marriage_display_power` for the
  side-by-side power read the parity gate is judged on.
- **`gui/marriage_window.gui`** (NEW) — the actual L4 candidate-LIST window (the piece that was
  genuinely missing; the scripted-GUI actions alone were only target-verbs with no browser). Proven
  idioms: `base_sub_window` + `dynamicgridbox datamodel=GetList('marriage_candidates')` (qing_province_
  reports.gui), country rows via `datacontext=[Scope.GetCountry]` + `new_country_flag` (diplomatic_view.gui
  player_subjects list). Each row shows flag + name + power score, and three per-row buttons (Propose /
  Seek-Dispensation / Betroth) that invoke the marriage_action_* GUIs against that row's country via
  `AddScope('target', Country.MakeScope)` — each self-gating on IsShown/IsValid so the row reveals whether
  the house is free-marriageable, needs a bridge, or is out of reach. Empty-list + hint footer.
- **`gui/government_view.gui`** — entry button "Royal Marriages (聯姻)" added to the CHI action strip
  (after the migration report button): `datacontext=GetScriptedGui('marriage_open_candidates')` builds
  the list, `createwidget gui/marriage_window.gui marriage_window` opens it. CHI-gated entry; the
  underlying scripted GUIs stay generic (any MARRIAGE_eligible_realm_trigger realm).
- **`common/modifiers/marriage_modifiers.txt`** (NEW) `royal_marriage_dysfunction`;
  **`common/opinions/imp19c_opinions.txt`** `royal_betrothal_opmod` + `royal_jilted_opmod`;
  **`localization/english/marriage_l_english.yml`** (NEW) gate tooltips + modifier/opinion names +
  the L4-window loc (MARRIAGE_OPEN_BTN/_TT, MARRIAGE_WINDOW_*, MARRIAGE_BTN_PROPOSE/_SEEK_BRIDGE/_BETROTH).
- Deferred (logged, not built): bloc mapmode (#13; superseded by the numeric qing_marriage_bloc_weight
  indicator), female-line inheritance laws (#14, → task #312); ministerial marriage-agency (#9, tie into
  the Grand Council) still PENDING — NOT served by the L4 GUI (that is player-driven; #9 is AI/court-driven).
- **CHI is enabled** (#311 core ask): a Qing↔Western match is possible but HARD-gated behind the
  bridge — the historical reality (no routine Sino-European marriage market).

### #311 review passes — engine review (3-dim) + GUI review (3-dim)
- **Engine review:** 4 raw findings, 1 CONFIRMED-major FIXED, 2 refuted (intended design), 1 duplicate.
  - **[MECH-fix] `se_MARRIAGE.txt` — decay broke UNRELATED alliances.** `MARRIAGE_check_decay` inferred
    "dynastic alliance expired" from the mere ABSENCE of `marriage_alliance_timer`, but that timer is set
    ONLY in the alliance branch of `MARRIAGE_form_pact` (skipped when the couple wed while ALREADY allied
    or at war). So a bond formed without that branch left no timer yet `bond_count>0` → every pulse, decay's
    `NOT has_variable marriage_alliance_timer` limit was true and `break_alliance` destroyed the couple's
    PRE-EXISTING independent alliance. FIX: track marriage-CREATED alliances in a dedicated list
    `marriage_alliance_partners` (added both ways where `add_alliance` actually fires); decay now gates on
    `has_variable_list = marriage_alliance_partners` (not bond_count) and iterates THAT list, so an alliance
    we did not create is never touched. List pruned consistently at all teardown sites (death-inherit +
    repudiate) and cleared after the decay loop (shared-timer realm-aggregate model, per the 2 refuted
    findings). `has_variable_list` proven (sell_provinces / ambitions).
  - Refuted: single shared `marriage_alliance_timer` = per-realm aging is intended (not per-partner);
    betrothal + marriage as independent bonds coexisting is intended (repudiate never touches marriage_partners).
- **GUI review:** 0 findings — all 3 dimensions (load-crash, loc-refs, runtime/scope) returned clean before
  verification. The window, candidate-list builder, entry button, and loc are proven-idiom and internally
  consistent (braces balanced, var names match builder↔window, all 3 row-button GUIs have saved_scopes={target}).

### #311 betrothal REWORK (user, post-commit — new work on 1763_bookmark) — all **[MECH]**
The betrothal was a bare country-level goodwill pledge that never matured. Reworked into a real child
betrothal per the user's spec: "promise two children will marry upon reaching adulthood, serious penalty
for breaking, but not if one child dies"; "betrothal must not create an alliance itself, only improve
relations in anticipation"; "great powers can't ally in vanilla — marriages must work around it"; "include
betrothals + eligible children in the UI".
- **`se_MARRIAGE.txt`**: `MARRIAGE_betroth` now binds two SPECIFIC children (minors allowed — the point),
  each getting a character var `betrothed_to_char` (→ partner child) + `betrothed_partner_country` (the
  proven TI `set_variable value=scope:X days=N` idiom, propose_marriage.txt); it applies ONLY the
  betrothal goodwill opinion — NO alliance (relations warm in anticipation). New `MARRIAGE_check_betrothals`
  (in the pulse) matures a pledge → marriage once BOTH children are adult+unwed, or dissolves it with NO
  penalty if a betrothed child died. New helpers: `MARRIAGE_mature_betrothal`, `MARRIAGE_dissolve_betrothal`,
  `MARRIAGE_clear_country_betrothal`, and `MARRIAGE_apply_marriage_bond` (the shared country-level payload,
  extracted from form_pact so maturation reuses it). `MARRIAGE_repudiate` now only penalises a WILFUL break
  (both children alive) and cleans the child-level vars.
- **GP-alliance workaround** [user]: `MARRIAGE_apply_marriage_bond` branches — a real `add_alliance` ONLY
  when neither house is `rank = great_power`; when a GP is involved it lays down a NEW `royal_marriage_entente`
  country modifier on both courts (diplomatic_relations +1, global_defensive +0.05, diplomatic_reputation +1)
  — the bond that works around the engine's hardcoded GP no-alliance rule. `MARRIAGE_check_decay` now strips
  the entente OR breaks the alliance (whichever applies) when the shared 30-yr timer lapses.
- **Death hook**: `on_character_death` (00_specific_from_code.txt) dissolves a dead betrothed child's pledge
  with no penalty, releasing the partner child.
- **UI** [user]: `marriage_open_candidates` now lists houses with any BETROTHABLE child (not only marriageable
  adults) and caches per-candidate `marriage_display_adult_children` / `_child_count` / `_wed` / `_betrothed`;
  `marriage_window.gui` gained a per-row line showing the children counts + a Wed/Betrothed status tag;
  `marriage_action_betroth` gained a betrothable-child gate. New modifier + loc keys (royal_marriage_entente,
  MARRIAGE_WINDOW_CHILDREN_*, MARRIAGE_WINDOW_STATUS_*, marriage_action_needs_betrothable_child_tt).
- Owes its OWN adversarial review before commit (not yet run).
