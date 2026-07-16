# Boot-test fixes 2026-07-16 — decision log

Working through the user's reported boot-test issues on `1763_bookmark`. Decisions noted here as
taken. Standing rules in force: commits authored by freekumquats; push after each logical batch so
the user can boot-test on the other machine; proven idioms only (upstream vanilla Imperator /
Invictus / Terra Indomita — NEVER mod/Qing code as the reference); loc reads scopes BARE `[x.GetName]`
never `[scope:x]`, adjective is `[X.GetCountry.GetAdjective]` (see memory imp19c-loc-scope-syntax-rule).

## Ordered work list (as agreed with the user)
1. Deep scan: event localization vs proven oracles — align data-function idioms.
2. Mission Completion Criteria shows eligibility ("Play as Qing") not the completion goal.
3. Missing mission loc: qing_burma_war / qing_colonization / qing_central_asia / qing_himalaya_seasia.
4. Ministry of Rites table overlap — drop the parenthetical Chinese names on the 3 long labels.
5. Ministry of Works — Hydraulic Works: one row per building type under the header (not crammed/cut off).
6. Public Works buildings not shown in province view — add a "Public Works" building category.
7. Propose-a-Marriage window — rebuild as 3 sequential single-column pickers (country → own char → their char).
8. Religion — populate vanilla deities (Confucian/Buddhist/Taoist/folk) + Holy Sites.
9. Starving pops remain: Yulin, Taiyuan, Jinhua over capacity.
10. Migration Report filter shows only Nanchong.
11. (RESOLVED, no code) New Treasure Fleet = standalone tree #439, hub gating Pacific+Japan trees.
12. Eunuch characters — add real eunuch characters (on-map), not just the threat meter.
13. Rename "Censor-in-Chief" → "Grand Inspector" (loc).
14. USA coastal chain broken by #397 trim — restore seaboard SC/GA (Charleston 3082, Savannah 3400, …).
15. French Louisiana too small — give LSA its historical CONTROLLED extent (not merely-claimed interior).
16. Empty unowned US-area territory — historical check: more Native tags? match 1763 layout.
17. Spanish-America Napoleonic disruption arc + Qing intervention opportunity.
18. Colonise unowned land (incl. Pacific islands) via the vanilla colonization mechanic.
19. New Treasure Fleet tree not visible in the missions list — likely loc-key/registration mismatch.

---

## Decisions taken

### #2 — Mission Completion Criteria showed eligibility (DONE)
Oracle-verified: `_CRITERIA_DESCRIPTION` is the mission-level COMPLETION-GOAL summary (Invictus/TI:
"This mission will be considered complete when we…"), NOT the start/eligibility gate. The 15 Qing
trees wrongly put the eligibility text ("Play as the Qing (CHI), and X must exist") there. Rewrote all
15 to describe the completion objective ("This enterprise is complete when …"). Files: burma_war,
colonization, central_asia, india, himalaya_seasia, japan_preperry, japan, open_japan, reform,
settle_frontier, selfstrengthening, summer_palace, treasure_fleet, taiping, xinjiang.

### #3 — "Missing mission loc" (burma/colonization/central_asia/himalaya_seasia) — RESOLVED BY VERIFICATION
Checked all four: mission title key, _DESCRIPTION, _CRITERIA_DESCRIPTION, and every per-task key
(_tt/_desc/needs_*) are ALL present; BOM + `l_english:` header correct; fully populated (30/168/26/51
keys); no parse-breakers (no missing :N, no stray quotes). This was a STALE report — the keys were
added by the completed task #55 ("CRITERIA_DESCRIPTION showing raw"). No change needed.

### #4 — Ministry of Rites table label overlap (DONE)
Removed the parenthetical Chinese from the three long labels so they no longer overrun the value
column: "Candidates Awaiting Appointment (科舉候選)"→"Candidates Awaiting Appointment"; "Civil
Degree-Holders in Service (科舉出身)"→"Civil Degree-Holders in Service"; "Military Degree-Holders in
Service (武舉出身)"→"Military Degree-Holders in Service". (qing_rites_ministry_l_english.yml.)

### #13 — Rename Censor-in-Chief → Grand Inspector (DONE)
Replaced all 10 "Censor-in-Chief" loc occurrences (qing_censorate_l_english.yml) with "Grand Inspector".

### #5 — Ministry of Works Hydraulic Works layout (DONE)
Was a single crammed value "Dikes N · Depots N · Granaries N" that overran the right edge. Restructured
the GUI block (qing_works_ministry.gui) into a header + THREE indented per-type rows (Yellow River Dikes
/ Grand Canal Depots / Ever-Normal Granaries), each with its own count var. Added 3 label loc keys,
removed the obsolete `_HYDRAULIC_VALUE` key (no dangling refs).

### #6 — Public Works buildings not shown in province view (DONE)
Root cause: the province build view (province_window.gui:4044-4067) uses a CURATED per-type item list
(build_item_* types, name-matched via EqualTo_string in gui_templates.gui) — NOT an auto-enumeration —
so the 6 Board-of-Works buildings (real building defs in qing_works_buildings.txt + qing_granary_buildings.txt)
had no item type and never displayed, though they stood on the works roster. FIX: added 6 `build_item_qing_*`
types (dike/canal_depot/wall_section/granary/great_wall/grand_canal) cloned from the vanilla infrastructure
pattern (name-match on the building's loc key, verified all 6 name keys exist), and wired them into the
InfrastructureItems block. The buildings' own allow-gate keeps them appropriately placed. This IS the
"new Public Works category in the province view" the user asked for (grouped under Infrastructure).

### #1 — Event-loc data-function scan vs oracles (DONE)
Cataloged every `[X.Method]` head/method the mod's event loc calls; validated each against Invictus + Terra-Indomita loc (never against mod code). Findings + fixes:
- `[scope:X...]` → bare `[X...]` — already fixed prior commit (0 residual; scope: is script-only, absent from both oracles).
- `[ROOT.GetAdjective]` → `[ROOT.GetCountry.GetAdjective]` — already fixed prior commit (oracles always `.GetCountry.GetAdjective`).
- **NEW: `[trib_invest_vassal.current_ruler.GetName]` → `.GetRuler.GetName`** (qing_tribute.2.desc). `current_ruler` is script scope; the loc data function is `GetRuler` (oracles: 953 uses of `.GetRuler.GetName`, ZERO bare `current_ruler.` in loc). This was a live ERROR: in-game.
- `[qing_censorate_target.GetCorruption]` → added `|0` format specifier. GetCorruption IS a valid data fn (15 mod-GUI uses); bare is tolerated but numeric fixed-point should be `|0`. Low-risk consistency fix.
- Validated as CORRECT (no change): `.GetName` (206), `.GetCulture.GetName`, `.GetRuler.GetName` — all heavily used in both oracles.
Result: 0 residual loc antipatterns across all mod loc.

### PRIORITY INTERRUPT — new logs in ~/Downloads (user directive: fix log issues first)

Log is fresh (14:43) but the error.log is a MULTI-RUN ACCUMULATOR (312 distinct HH:MM:SS run-stamps;
per the stale-log rule the same file spans many boots incl. pre-fix ones). Triaged top signatures;
separated LIVE mod bugs from stale/pre-fix and inherited-framework noise:

**LIVE mod bug FIXED — `QING_DECLINE_granary_pool` operator flood** (se_QING_DECLINE.txt).
`Unsupported scope operator '<'` / `Unknown trigger type: value`. Root cause: the FILL/SHIP `limit`
comparisons used a TRIGGER (`has_state_food`, `has_state_food_capacity`) or a cross-scope `ROOT.var:`
INSIDE the comparison `{ value = ... }` RHS block, evaluated in `every_country_state` scope — the
parser can't resolve that and the whole effect aborted, so the ever-normal granary NEVER moved grain
(dead relief → likely why Yulin/Taiyuan/Jinhua still starve, item #9). This DISPROVES the old
se_QING_SPHERE:287 comment that claimed the `has_state_food < { value = ... }` form was silent.
FIX: precompute every operand into a plain STATE var first (set_variable can read the trigger /
ROOT.var: fine), then compare `var:stateX op { value = var:stateY }` — the SAME-SCOPE var-to-var form
that council/governance/canal/customs use with ZERO log hits (forensically confirmed silent). Added
6 per-state temps (cap/food/fill_thr/ship_thr/pool/poolcap), removed at loop end; also fixed the SHIP
clamp's `ROOT.var:` RHS. Brace-balanced.

**LIVE gui bug FIXED — `qing_personnel.gui:268` margin** — a plain `widget` root carried `margin`,
which it does not accept ("Property 'margin' not handled" → factory error at :266). Removed; the inner
flowcontainer already has margin. (Line 69 is a `margin_widget`, which DOES accept margin — left.)

**STALE, no change needed** (already fixed at HEAD e799a7c04, log entries predate it):
- `QING_tribute_receive` "Failed to fetch variable 'qing_trib_gift'" (384×) — HEAD already seeds the
  var to 0 before any read (init-before-read fix present + correct).
- `MARRIAGE_PLAY_seed_char_bonus` "Unknown trigger type: value" (315×) — HEAD line 184 already uses
  the silent `var:X >= { value = var:Y }` same-scope form (the e799a7c04 fix). Council/governance use
  the identical form with 0 log hits, confirming it's legal; these hits are pre-fix.

### #7 — Propose-a-Marriage rebuilt as 3 sequential single-column screens (DONE)
The 3-column layout (900×640) had repeatedly rendered as a blank black frame + grey overspill despite
several layout fixes. Per the religion-panel lesson (stop re-fixing a layout that keeps failing; clone a
PROVEN structure instead), rebuilt marriage_play_window.gui as THREE standalone `base_window`s cloned from
the proven `qing_office_picker_window` single-column picker (windowgfx / parentanchor=center / one fixed
scrollarea under a MainWindowHeaderBoxCentered header / dynamicgridbox datamodel / window-level button_close):
  1. `marriage_play_window`        — pick TARGET REALM (marriage_play_realms).
  2. `marriage_play_own_window`    — pick OUR character (marriage_play_own_candidates).
  3. `marriage_play_their_window`  — pick THEIR character (marriage_play_their_candidates) + Propose/Cancel bar.
Each row's onclick keeps the PROVEN idiom unchanged (datacontext = Scope.GetCountry/GetCharacter; inline
GetScriptedGui(...).Execute(GuiScope.SetRoot(...).AddScope(...).End) — the #8 boot-fix that stops a
ScriptedGui datacontext override from blanking the row), then chains forward: pick_realm closes screen 1 +
createwidget screen 2; pick_own closes screen 2 + createwidget screen 3; on screen 3 the Propose button runs
the already-validated marriage_play_launch (both picks set, opposite sex, unmarried) then closes. The data
layer (MARRIAGE_PLAY_actions.txt) already sequenced realm→own→their, so NO script change was needed — pick_realm
builds the their-list, pick_own re-filters it by sex, launch guards opposite-sex/unmarried. government_view.gui
button unchanged (still opens marriage_play_window = screen 1). Added 6 loc keys (3 per-screen INSTR_* + 3
NO_* empty-list lines); brace-balanced (100/100), .gui no-BOM, loc BOM present.

### #8 — Religion: populate the Qing pantheon deities + holy sites (DONE)
Vanilla ships `confucianism` (the Qing state religion, confirmed CHI religion=confucianism, capital
Beijing 8363) with ZERO deities, so the vanilla Pantheon & Holy Sites panel stood empty for the player.
Populated it with TWELVE deities across the four traditions of the realm — Confucian sages (Kongzi/Mengzi/
Zhu Xi), martial guardians (Guan Yu/Xuanwu/Nezha), Taoist & wealth (Laozi/Caishen/Mazu), Buddhas & Heaven
(Guanyin/Shangdi/Tudigong) — in common/deities/03_confucian_pantheon.txt. Slot balance mirrors the proven
base-game 00_generic.txt: 3 each of war/economy/culture/fertility.
DECISION — clone the mod's OWN proven-loading 00_generic.txt bodies, NOT the Invictus 01_chinese_religions.txt:
the Invictus file is the closest thematic reference but depends on Invictus-only infrastructure absent from
imp19c (common_deity_trigger, holy_site_deity_check_trigger, deity_china_* icons, its own religion
`chinese_religions`). 00_generic's tokens (icons deity_war/wealth/eloquence/love, deity_*_svalue passives,
omen_*_svalue omens, *_apotheosis_*_effect on_activate) are ALL base-game vanilla, inherited at runtime —
so cloning them verbatim and only swapping the key + religion (region1 -> confucianism) is guaranteed to load.
Verified all 8 referenced apotheosis `_tt_description` loc macros exist as base-game keys (present in Invictus's
apotheosis_tooltips loc).
HOLY SITES: the engine reads `holy_site=<deity key>` in PROVINCE HISTORY (proven Invictus/base-game
convention — holy_site is a province field, NEVER a deity field; verified 0 deity-field uses across both
oracles). My first draft wrongly put holy_site= inside the deity blocks; corrected to comments there and added
`holy_site=deity_X` to 8 province setup blocks (Tai'an 7197 Kongzi / Jining 9041 Mengzi / Fuzhou 3651 Zhu Xi /
Luoyang 8620 Guan Yu / Leshan 8145 Laozi / Putian 1159 Mazu / Wutai 2407 Guanyin / Beijing 8363=Temple of
Heaven Shangdi), inserted after each block's religion= line with BOM preserved. Loc file
qing_deities_l_english.yml follows the proven Invictus `deity_KEY:0 "$omen_KEY$"` / `omen_KEY:1 "Name"` /
`omen_KEY_desc` triple with the apotheosis-effect macro. Deity file no-BOM (deities/ convention), braces 72/72,
loc BOM present, all 6 province files brace-balanced + BOM-preserved.

### #9 — remaining starving pops (Yulin / Taiyuan / Jinhua) (DONE)
Confirmed the granary_pool operator fix does NOT address this — that fix buffers the *capital* grain
draw (漕運/糧儲), whereas the Pops-Starving alert here fires on *local* population > *local* capacity.
Diagnosed the four remaining outliers: Yulin (Shaanxi 5270 + Guangxi 9709 — the user's "Yulin" is
ambiguous so both are covered), Taiyuan (8501), Jinhua (9585). All four are hills/plains, low-civilisation
SETTLEMENTS: their seeded 1763 density sits just above even the #49 doubled base capacity, while their
FARMLAND peers at equal-or-higher pop (e.g. 6053 @319, 8311 @349) clear it — so terrain-driven low base
capacity, not headcount, is the discriminator, and the empire-wide +100% couldn't lift these last few.
FIX: a targeted permanent province modifier `qing_dense_prefecture` (local_population_capacity_modifier =
0.75 — a proven base-game province token, TI 00_from_missions_* / 00_aos_modfiers) applied to exactly these
four at game start via QING_boot_relieve_dense_prefectures (hooked right after qing_populous_realm in the
tag=CHI init). Each add is existence-checked (exists = p:$PROV$ — a trimmed map can't error) and
modifier-guarded (re-init can't stack), logged per-province. Proven idiom p:<id> add_permanent_province_modifier
(TI p:687 second_temple). Added modifier name/desc loc. Brace-balanced across all four files; se_QING_MECHANICS
kept its existing no-BOM, modifiers loc kept BOM.

### #10 — Migration Report listed only Nanchong (DONE)
ROOT CAUSE: the report's PASS-1 membership walk iterated `every_governorships > every_governorship_state
> every_state_province`, which visits ONLY governorship provinces and EXCLUDES the entire CAPITAL DOMAIN —
most of China proper, where nearly every crowded/over-capacity province actually sits. Only Nanchong showed
because it happens to lie under a governorship. PASS 2 already emits via `ordered_owned_province` (ALL owned
provinces), so the two passes disagreed on membership. FIX: mark in PASS 1 over `every_owned_province` (a
proven iterator, 00_tech_modifier_applicator_effects.txt) so it matches PASS 2's scan — now every crowded /
overpopulation-flagged / in-migration-boom province across the whole realm is listed, high-pop-first.
Brace-balanced (89/89). The qualifying criteria (boom modifiers / overpopulation / total_population>=20) are
unchanged.

### #12 — Eunuch characters (add real eunuchs, not just the threat meter) (DONE)
The user saw "The Eunuchs (太監)" as a Household field but only a threat-indicator + a faction-leader
flag (stamped on an ad-hoc created stranger) stood behind it — no visible corps. Added a CONCRETE
palace-eunuch establishment (concrete-over-abstract house rule), mirroring the proven harem consort
roster (se_QING_HAREM.txt):
- se_QING_HOUSEHOLD.txt: QING_household_seed_eunuchs (guarded, seeds an opening corps of 4 Han eunuchs
  at game start, called from QING_household_init which runs in the CHI init block), QING_household_mint_eunuch
  (create_character, #90-safe — markers in a follow-up scope: qing_is_palace_eunuch + set_home_country;
  finesse/charisma gifts), QING_household_recompute_eunuchs (self-healing roster rebuild → qing_household_eunuchs
  list + qing_eunuch_count, run on pulse + panel open). REWORKED the pulse's faction-arising branch: the
  danger now PROMOTES the most capable serving eunuch (ordered_character order_by=finesse max=1) to
  qing_eunuch_faction_leader instead of conjuring a fresh stranger (falls back to minting one only if the
  corps is empty).
- QING_household_panel.txt: panel-open now seeds+recomputes the roster; added qing_household_has_eunuchs indicator.
- qing_household.gui: added a "Palace Eunuchs (太監)" roster section (dynamicgridbox over qing_household_eunuchs,
  Character.GetName + finesse/charisma; a faction-leader eunuch tagged in red via
  Character.MakeScope.Var('qing_eunuch_faction_leader').IsSet — the proven imp19c_windows.gui idiom).
- Added 4 loc keys. All files brace-balanced (se 137/137, panel 81/81, gui 147/147); ordered_character
  order_by=finesse is a proven in-mod idiom (se_QING_CANTON.txt).

### #19 — New Treasure Fleet tree not visible in the missions list (DONE)
ROOT CAUSE: the tree's `potential` carried a PROVINCE-scope condition — `any_owned_province = { is_port = yes }`
— and it is the ONLY Qing tree that put a province walk in `potential`; every visible sibling
(japan_preperry / xinjiang / colonization / india) gates `potential` on tag / flag / tag-existence only.
A province-scope check in mission `potential` hides the whole tree from the mission browser, so the New
Treasure Fleet never listed. FIX: reduced `potential` to `tag = CHI  is_ai = no` (matching the siblings) and
moved the "empire must touch the sea" precondition into the opening task's `allow` as a custom_tooltip
(`any_owned_province = { is_port = yes }` + new loc qing_treasure_needs_coast_tt). The tree is now visible and
the first task simply can't be taken until the empire holds a port — the mechanic is unchanged, only the gate's
placement. Answers the user's "what is the starting criteria": CHI + coastal (a port province); the later
tasks then gate on a level-3 harbour and fleet size. Brace-balanced (42/42), missions no-BOM preserved.
(This also closes the #11/#19 New-Treasure-Fleet thread: standalone tree #439, now correctly listed.)

### #14 — USA Atlantic seaboard chain broken (Charleston / Savannah) (DONE)
The #397 trim listed Charleston 3082 (South Carolina) and Savannah 3400 (Georgia) among the
"trans-Appalachian/western frontier" provinces it dropped as unowned — but these are the principal
British SEABOARD PORT cities of the SC & GA colonies in 1763, and dropping them broke the coastal chain
between the kept ports Beaufort 144 / Georgetown 2672 / Brunswick 10054. RESTORED both to the USA (=GBR
client-colony at 1763) own_control_core, and removed them from the "removed" comment so the ledger stays
honest. Left the genuine trans-Appalachian interior removed (that's #16, pending research). Verified no
other tag's own_control_core claims 3082/3400 (they were unowned holes, no conflict). Per the user: "if
the coastal gap is historically accurate, then leave it" — it was NOT accurate; these two are unambiguous
Atlantic ports, so restored.

### #15 — French/Spanish Louisiana too small (confined to the modern state) (DONE)
Confirmed all 14 LSA provinces sat inside the modern US state of Louisiana. Per research
(.research/1763_north_america_map_groundtruth.md §1), Spanish Louisiana's CONTROLLED footprint in 1763
ran up the WEST bank of the Mississippi (Ste. Genevieve district near St. Louis, Cape Girardeau) and the
lower Arkansas River (Arkansas Post 1686, Little Rock) — a riverine post corridor, NOT the trans-plains
interior (that was paper-claim only). Added the 4 controlled west-bank posts (Saint Louis 4459, Cape
Girardeau 3587, Arkansas Post 3057, Little Rock 3643) — all confirmed currently UNOWNED (they were in MSI's
now-inert commented frontier list), so no ownership conflict; verified each now belongs only to LSA. Left the
Osage plains interior unowned for the Native-tag pass (#16). Per the user: give LSA "its historical territory,
which was much larger… do not give it the territory that was merely claimed and not controlled" — done. No-BOM
preserved.

### #16 / #17 / #18 — DEFERRED to a user steer (larger interpretive map + subsystem work)
These three are a different class from the discrete boot bugs and carry design latitude, so surfacing for a
steer before building:
- #16 (Native tags over the trans-Appalachian + plains interior): the mod ALREADY ships Native tags
  CHE/CHT/CHC/MSG/MIA/SHO/LAK/DAK/PWN with country files; missing ones I'd otherwise add = Creek/Iroquois/
  Comanche/Osage/Pawnee/Shawnee/Ottawa. Question: place ownership using only the existing tags, or mint the
  missing nations too? And how much interior to fill vs leave colonisable-unowned (feeds #18).
- #17 (Spanish-America Napoleonic disruption arc + Qing intervention): a new event chain (San Ildefonso 1800 /
  Louisiana Purchase 1803 / Bayonne 1808 / West Florida 1810 / Hidalgo 1810) — scope/size TBD.
- #18 (colonise unowned land incl. Pacific islands via vanilla colonization): depends on #16 leaving the right
  land colonisable; the vanilla mechanic is the army `settle` ability on colonizable provinces.

### #16a — mint the Haudenosaunee (Iroquois) tag (DONE)
Audited the Native roster: the mod ALREADY ships Creek (MSG/alabama), Comanche (CMC), Osage (OSG=niukonska/
"Wazhazhe"), Pawnee (PWN), Shawnee (SHW), plus Choctaw/Chickasaw/Cherokee/Miami/Council-of-Three-Fires/etc — so
of the "key missing nations" the user approved, only the **Haudenosaunee (Iroquois Six Nations)** was genuinely
absent. Minted tag IRO: country file setup/countries/n_america/haudenosaunee.txt (BOM, cloned from the shawnee
template), registered in countries.txt, setup block (government federated_tribe, primary_culture mohawk, religion
waashat, capital 8418 Ashtabula). Their upstate-NY homeland sits inside the USA (=GBR 13-colonies) claim, so IRO
takes its unowned western-Lake-Erie / upper-Ohio "Ohio Country" (the conquered hunting-grounds reserved to Natives
by the 1763 Proclamation Line): 8418 8696 9828 9164 9149 9881 — all confirmed UNOWNED (vacated by the #397 trim),
each now owned only by IRO. Added IRO / IRO_ADJ loc. Setup file brace-balanced (10967/10967).

### #16b — assign the vacated 1763 interior to the Native nations (DONE)
The #397 trim vacated ~200 trans-Appalachian / Ohio-Valley / plains provinces to unowned. Each unowned
interior province already carries its historical Native `culture=` in the province data, so I bucketed them
by culture to the culturally-matching Native tag (no guesswork): assigned 143 provinces across 13 tags —
CHE (Cherokee), CHT (Choctaw), CHC (Chickasaw), MSG (Muscogee/Creek — incl. creek/koasati cultures), CDD
(Caddo — incl. wichita), MIA (Miami/Illinois confederation — the `illinois` culture), SHW (Shawnee), C3F
(Council of Three Fires — ojibwe), OSG (Osage — incl. quapaw/iowa Dhegihan/Chiwere kin), CMC (Comanche —
incl. kiowa southern-plains), DAK (Dakota — yanktonai), DIN (Diné/Navajo), IRO (Haudenosaunee — the seneca
culture). LEFT 65 settler-culture provinces (dixie/yankee/creole, the coastal-adjacent margin) UNOWNED as the
colonisable frontier for #18 — consistent with the 1763 Proclamation-Line Indian Reserve. Verified: 0
double-owned provinces, 0 misassignments. Also repointed 6 tags' capitals (CHE/CHC/MIA/DAK/CHT/MSG) that the
#397 crash-fix had parked in USA/LAK land back onto their OWN reclaimed territory (avoids the ownerless/foreign-
capital construction crash class — memory imp19c-ownerless-capital-crash-rule). Setup file brace-balanced
(10967/10967).

### #17 — Spanish-America Napoleonic disruption arc + Qing hook (DONE)
Found the existing `spa_bourbon` arc scripts Spain's OWN 1763-1815 trajectory (Jesuits/San Ildefonso/Dos de
Mayo/Ferdinand) and `qing_americas.2` already gives a Qing "seize the Californian shore" beat — so the gap the
user asked for was the COLONIAL-side disruption in Spanish America. Built a new `spa_america` arc (namespace
spa_america) mirroring the proven spa_bourbon idiom (is_triggered_only country events, self-gated tag=SPA,
per-beat has_variable done-flags, ai_chance-weighted posture nudges, sys=SPA logging):
- .1 1800.10 Retrocession of Louisiana (San Ildefonso) — political_influence/prestige nudge
- .2 1803.12 Louisiana Purchase — the vigorous new US neighbour
- .3 1808.05 Bayonne abdications → the colonial juntas (stability/prestige/influence hit — the turmoil the
  MEX/mex_instability arc presumes)
- .4 1810.09 Grito de Dolores + Republic of West Florida (US annexation)
- .5 (CHI-only) 1808.06 "Spain prostrate — a Pacific opening": the Qing-intervention hook, gated on a Pacific
  presence (same trigger as qing_americas.2), firing the PROVEN QING_americas_press_pacific_coast effect. This
  is the user's "give Qing an opportunity to intervene as well."
Driver common/on_action/spa_america_on_actions.txt: on_actions LIST form (bare on_game_initialized doesn't
merge, develop #254); SPA beats under a tag=SPA if, the Qing beat under a separate tag=CHI if; day-offsets from
1763.2.16. Loc spa_america_l_english.yml (BOM). Events + on_action BOM'd (sibling convention + BOM rule), each
brace-balanced (events 49/49, on_action 19/19); verified QING_americas_press_pacific_coast + the col-modifier/
region gates exist. se_LOG-wired throughout.

### #18 — colonise unowned land + Pacific islands (DONE)
The mod REMOVED the vanilla migrant `settle` ability (it keeps `military_colonies`, which requires
`has_owner = yes` — it settles ALREADY-owned land), and the engine's built-in ColonizeButton
(ProvinceWindow.QuickColonize) rides on that disabled migrant system — so the Qing had no working way to take
the empty frontier / Pacific islands. The full vanilla `settle` import would graft the whole num_of_migrants
subsystem (heavy, risky for a settled empire). Instead built a scripted colonise action in the mod's own idiom:
- common/scripted_guis/QING_colonise_frontier.txt — QING_colonise_frontier_button, a province-scope player
  button cloned from the proven found_city_button (saved_scopes={player}, is_shown/is_valid/effect). Shown to CHI
  on an UNOWNED, inhabitable (is_uninhabitable=no, not sea) province; enabled when Qing-REACHABLE — either
  any_neighbor_province owned by the Qing (contiguous frontier — the #16b-vacated interior, Ili/Xinjiang marches)
  OR a coastal province while the Qing holds a Pacific colonial foothold (fur-coast/silver-road/pacific-trade/
  golden-shore modifier or a California/Cascadia/Alaska/Pacific_Mexico province) — so PACIFIC ISLANDS qualify.
  Price-gated via the proven found_city can_pay_price idiom.
- price_colonise_frontier (common/prices/00_from_script.txt): 30 political influence + 100 gold.
- QING_colonise_this_province (se_QING_AMERICAS.txt): transfers the clicked province with set_owned_by = scope:player
  (the proven in-mod province-transfer idiom, se_QING_BURMA:149) + seeds a create_state_pop tribesmen (the
  se_QING_COLON settler idiom); guarded on still-unowned so a stale/double click can't re-transfer owned land.
- Wired a button into gui/province_window.gui's UNOWNED-province row (beside the inert engine ColonizeButton),
  gated by the ScriptedGui.IsShown/IsValid over province+player scope.
- Loc: confirm_t/desc + button tooltip in qing_americas_l_english.yml.
All proven-in-mod triggers (is_coastal/any_neighbor_province/is_uninhabitable/is_sea/has_owner/create_state_pop/
set_owned_by); scripted_gui BOM'd; brace-balanced (gui 23/23, province_window 1954/1954, prices 70/70,
se_QING_AMERICAS 80/80).

**INHERITED / framework noise (not mod-authored, left):** PROVINCE_TOOLTIP loc (10790), missing
`gradient_black_flip.dds` texture (7378), the `oa_wealth_changes`/`GT_split_*`/`EE_scripted_guis`
economy-framework script errors + sqrt `Illegal use of operator` (the economy-framework's own
local_var-on-RHS, tracked separately in the economy-audit backlog), map-locator bounding-box warnings,
COHORT_NAME_jurchen ordinal. These are upstream/framework, out of scope for this pass.
