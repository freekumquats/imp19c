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
13. Rename "Grand Inspector" → "Grand Inspector" (loc).
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

### #13 — Rename Grand Inspector → Grand Inspector (DONE)
Replaced all 10 "Grand Inspector" loc occurrences (qing_censorate_l_english.yml) with "Grand Inspector".

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

### #18 — colonise unowned land + Pacific islands (DONE — corrected scope)
CORRECTION after a user challenge: I initially claimed the mod had "disabled vanilla colonisation" and built a
button for the whole unowned frontier. That was WRONG. Native ENGINE colonisation IS enabled — define
`MINIMUM_COLONISATION_POP = 8` was re-enabled by #304 (it had been the 99999 disable-sentinel) — so the province
window's built-in ColonizeButton already colonises the CONTIGUOUS frontier for the Qing with no code needed.
What the mod deleted was the separate migrant `settle` ARMY ability (a different mechanic), and what the engine
genuinely CANNOT do is reach OVERSEAS/Pacific-island land out of colonisation range. So I NARROWED the scripted
button to fill only that real gap (it no longer duplicates the engine on adjacent land):
- common/scripted_guis/QING_colonise_frontier.txt — QING_colonise_frontier_button, a province-scope player
  button cloned from the proven found_city_button (saved_scopes={player}, is_shown/is_valid/effect). Shown to CHI
  on an UNOWNED, inhabitable (is_uninhabitable=no, not sea) province; is_valid gates on OVERSEAS-only reach:
  is_coastal = yes, NOT adjacent to any Qing province (so it never overlaps the engine ColonizeButton's contiguous
  range), AND the throne holds a Pacific foothold (fur-coast/silver-road/pacific-trade/golden-shore modifier or a
  California/Cascadia/Alaska/Pacific_Mexico province). This is the Pacific-island / out-of-range case the engine
  can't do. Price-gated via the proven found_city can_pay_price idiom.
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

---

## Follow-on session (post boot-test feedback)

### STANDING RULE ADDED — boot-crash review before "ready to test"
User directive: after ANY batch of changes, run an independent boot-crash review BEFORE saying it's ready to
boot-test (the user tests on a separate machine, so a missed crash costs a full round-trip). Saved to memory
imp19c-boot-crash-review-rule; on top of the existing fix-traceability rule, this makes the boot-crash review
unconditional for every batch.

### #18 CORRECTION — vanilla colonisation is ENABLED (I was wrong twice)
I twice claimed the mod "disabled vanilla colonisation." FALSE: `MINIMUM_COLONISATION_POP = 8` was re-enabled by
#304 (from the 99999 disable-sentinel), so the province window's built-in ColonizeButton already colonises the
CONTIGUOUS unowned frontier for the Qing with no code. What the mod deleted was the separate migrant `settle`
ARMY ability (a different mechanic). NARROWED my #18 button to the one thing the engine can't do — OVERSEAS /
Pacific-island land out of colonisation range (unowned coastal, NOT adjacent to Qing land, Pacific-foothold gated).
[STILL TO VERIFY — task: check whether a vanilla colonisation-range define can reach islands, and if so drop the
script entirely; see "consolidation" below.]

### MIGRATION PUSH — food capacity + over-capacity now real push factors (DONE)
User boot-test: the over-capacity push "does not appear to work." ROOT CAUSE: the prior term gated on
`has_province_modifier = overpopulation` — the engine's hardcoded auto-modifier, which is NOT queryable by name
from script, so the term was silently inert (the code comment had even hedged that it "may be inert"; the boot
test confirmed it IS). Also `has_province_modifier = starving_city` (same class). REPLACED both with DIRECT
readable arithmetic in MIGRATION_svalues.txt:
- `MIGRATION_pop_overcapacity_overflow` = total_population − modifier:local_population_capacity (min 0) — the
  proven readable pop-ceiling numeric (AI_svalues.txt:379 / MODIFIER_svalues.txt read modifier:local_* directly).
  Wired into the push × 1.5 (heavy, per "over-capacity should drive a lot of migration"). 人地矛盾.
- `MIGRATION_state_food_deficit` = shortfall of stored food below half the state's food capacity, normalised by
  capacity × 20 (empty granary ≈ +10). Reads has_state_food / has_state_food_capacity via the proven
  `state = { add = <primitive> }` scope-wrapper (JOBS_svalues idiom), NOT a dotted state.has_state_food accessor
  (unproven for engine primitives). Guarded on capacity > 0 so deserts/sea divide safely. This is the user's
  "lack of food (state food capacity low) … should be a migration push factor", distinct from the existing
  governorship per-good production-shortage term. Pure arithmetic — no trigger, no var-on-RHS comparison (safe
  per the RHS-operator rule). Brace-balanced 43/43.

### BOOT-CRASH REVIEW findings applied (independent review of the boot #7–#19 series)
Review verdict: series clean overall (0 double-owned provinces across 8,790 assignments; all re-territoried
capitals self-owned; IRO/arc/colonise/eunuch/deity mechanics all sound). Actioned findings:
- **MEDIUM (1763-crash class) FIXED:** common/deities/03_confucian_pantheon.txt carried CJK comments but NO BOM,
  while its populated sibling 00_generic.txt DOES have a BOM — my "no-BOM deities convention" claim was FACTUALLY
  WRONG (only 00_generic is populated, and it is BOM'd). Added the BOM + corrected the file's header comment.
- **MEDIUM (loc rule) FIXED:** localization/english/qing_americas_l_english.yml (heavy CJK) had no BOM → added.
- **LOW FIXED:** common/scripted_effects/se_QING_HOUSEHOLD.txt (CJK, pre-existing no-BOM) → added BOM for consistency.
- **NOTED (out of scope, pre-existing):** 5 ownerless capitals not touched by this session — MRI(7709) PSR(3856)
  MLK(883) SNR(883) KBO(4083) — a latent ownerless-capital crash risk IF those tags construct; flagged for a
  separate pass. Cosmetic: IRO placeholder Celtic ship names; 4 deities without holy sites (function fine).

### #72 — can vanilla colonisation reach Pacific islands? NO → keep #18 button (DONE, investigated)
Checked all colonisation defines: only `MINIMUM_COLONISATION_POP = 8` (the on/off gate) and
`MAX_COLONISATION_BARB_IN_TARGET = 2` exist — identical to the Terra-Indomita parent, and there is NO
colonisation-RANGE define. Vanilla I:R engine colonisation is hardcoded to ADJACENCY (a province is colonizable
only if it borders your territory or a sea zone you control), so it genuinely cannot reach an isolated Pacific
island from the Asian mainland. DECISION: keep the #18 QING_colonise_frontier button as the documented overseas
exception — it is not reinventing a vanilla capability, it fills a real engine gap. (Its adjacent-frontier case
was already removed in the earlier correction, so it no longer overlaps the engine ColonizeButton at all.)

### #73 — consolidate the 6 "settle the frontier" surfaces (DONE — cross-referenced, not merged)
Audited all six for what they actually target/do:
  1. Engine ColonizeButton (province window) — colonises EMPTY adjacent land (vanilla, enabled #304).
  2. #18 QING_colonise_frontier — colonises EMPTY overseas/Pacific-island land (fills the vanilla range gap; #72).
  3. Promote Frontier Settlement (Population panel, 移民實邊) — empire-wide MIGRATION POLICY; stamps migr_gov_pull
     on the held frontier so existing heartland pops drift there over decades. Settles no new ground.
  4. #451 Settle the Nomads (定牧墾邊) mission tree — DEVELOPS the held Mongol/Manchu ground (integrate the banner-
     governorships, lay the qing_frontier_reclamation texture).
  5. Xinjiang 屯田 (New Dominion panel) — DZUNGARIA-specific colony lever (grip + Yili integration).
  6. send_settlers diplomatic play — moves pops into a NEIGHBOUR's sparsely-held area.
FINDING (confirmed with the user): these are NOT mechanical duplicates — they act on different land (empty-
colonise vs owned-develop vs migration-policy vs diplomatic). An outright merge would erase real distinctions
(empire-wide vs Dzungaria-specific; policy vs one-shot). So the right consolidation is DISCOVERABILITY, not
deletion. Applied: added a cross-reference clause to each overlapping surface's tooltip so the player can tell
them apart —
  - #3 移民實邊 TT: "empire-wide migration policy, settles no new ground; to take empty land colonise directly / for
    Dzungaria use 屯田 / for the Mongol-Manchu ground run 定牧墾邊."
  - #5 屯田 TT: "Dzungaria-specific lever; for the empire-wide policy see 移民實邊 / for Mongol-Manchu see 定牧墾邊."
  - #4 定牧墾邊 DESCRIPTION: "DEVELOPS held ground; distinct from colonising empty land, the 移民實邊 policy, and 屯田."
  - #2 #18 TT already cross-refs "the ordinary colonisation of the neighbouring frontier" (the engine button).
LEAN-ON-VANILLA: settled by #72 — the only script that could have reinvented vanilla was #18, and vanilla can't
reach islands, so it stays as the documented exception; #1 (the vanilla ColonizeButton) is untouched and remains
the primary colonise route. No mechanic deleted; 3 loc tooltips edited, all BOM-verified.

### #74 — Faith & Sedition per-province drill-down reports (DONE)
The three Faith & Sedition read-outs in the religion view were abstract national aggregates. Made each a
CLICKABLE button that opens a province-list report of the concrete provinces driving that number — the data
already exists per-province (qing_prov_missionary_tension var; qing_mission_station + qing_mission_unrest
province modifiers). Followed the existing qing_province_reports template EXACTLY (per user "follow the existing
reports templates"):
- 3 report scripted_guis in qing_province_reports.txt (qing_report_open_antichristian / _missions / _friction)
  + their _empty indicators. Each walks every_owned_province (NOT every_governorships — reuses the boot #10
  lesson so the capital domain is covered), building the country list; degrades to empty gracefully.
    • Anti-Christian Sentiment → provinces with qing_prov_missionary_tension >= 30 (shows the value)
    • Mission Stations → provinces with the qing_mission_station modifier
    • Social Friction → provinces with the qing_mission_unrest (地方教案 disorder) modifier
- 3 report windows in qing_province_reports.gui, each cloned from qing_tension_report_window (base_sub_window /
  vbox / scrollarea / dynamicgridbox / per-row goto_button / empty-note / count).
- Wired the religion_view.gui Faith & Sedition block: each label is now a text_button_square_highlighted that
  Executes the report scripted_gui then createwidgets its window (the proven report-open idiom); the value
  textbox stays beside it. 13 loc keys added (BOM preserved). All brace-balanced (reports.txt 137/137,
  reports.gui 348/348, religion_view 377/377). No mechanic changed — pure read-only drill-down.

### PENDING (this follow-on)
- #75 eunuch danger → Household perf metric + Upper Study → Household perf + throttled eunuch GC events.
- #76 comprehensive audit: every ACTIVE feature under each Grand Council ministry should feed that ministry's
  effectiveness metric (not passive read-only reports).

---

## Follow-on batch (2026-07-16): #75 / #76 / #77 IMPLEMENTED

### Audit result (#76) — ministry ACTIVE features → effectiveness
Audited all 12 recompute functions in `se_QING_MINISTRY.txt`. 8 ministries already fold every
active lever. **4 gaps found & fixed:**
- **GAP1 Works (工部) — railway.** Added term (e) to `QING_ministry_recompute_perf_works`:
  `qing_rail_network_count` (from the panel's Extend-the-Railway action, se_QING_SELFSTR) now lifts the
  minister, +1/line, capped +12. Zero-rail (1763 norm) = no penalty (guarded on the var).
- **GAP2 Household (內務府) — Upper Study.** Added term (g) to `QING_ministry_recompute_perf_chamberlain`:
  `qing_upperstudy_schooling` deviation from ~50, /5. The 上書房 (crown-prince school) is the chamberlain's charge.
- **GAP3 Household — wenzhi patronage.** Added term (h): `qing_wenzhi_patronage` deviation from ~50, /5.
  The 文治 cultural patronage is managed from the Household panel; now folds into the chamberlain.
- **GAP4 Grand Secretariat (翰林院) — Southern Study.** Added term (f) to
  `QING_ministry_recompute_perf_grand_secretariat`: `qing_southernstudy_count` vs healthy ~3, x2. The
  "second a scholar to the Southern Study" lever drained the Hanlin bench (term b) with no credit back;
  now the 南書房 corps depth credits the Academy's leader (his brush-secretaries staff the inner chancery).
- **VERIFIED already-feeding** (no change): eunuch danger → chamberlain (−20, term c); canal condition →
  works (term d); Xinjiang consolidation → Lifan Yuan (term c); all Zongli/Revenue/Censorate/Justice/Guard/
  Personnel active levers. Passive read-only REPORTS deliberately excluded (per user).

### #75 — eunuch danger → Household perf (positive term) + throttled eunuch GC events
- **Perf:** added term (f) to `QING_ministry_recompute_perf_chamberlain` — a POSITIVE +6 when a palace-eunuch
  corps EXISTS and NONE leads a faction (distinguishes "eunuchs held in check" from "no eunuchs at all").
  The existing −20 danger penalty (term c) is the negative counterpart; the two are mutually exclusive by
  the negated faction-leader predicate. Also added Upper Study (g) per the user's follow-up.
- **Events:** two new throttled GC events in `qing_household_events.txt` — `qing_household.5` (POSITIVE: the
  敬事房 in good order; reward chamberlain / entrench 祖制 prohibitions / note-and-pass) and `qing_household.6`
  (EARLY WARNING: a eunuch oversteps before a full faction; nip early / chamberlain handles quietly / look away
  → raises .2 odds). Both wired into `QING_frontier_flavour_roll`'s random_list in `se_QING_DECLINE.txt`
  (weights 7 / 6), sharing the same `qing_gc_event_slot_used` court throttle as every other GC event, and each
  re-checks its own trigger in the fired event (stale-pick-safe).
- **Modifier:** new `qing_household_eunuchs_curbed` (10yr, `monthly_corruption = -0.05`) for .5.b, in
  `qing_household_modifiers.txt`.
- **Loc:** new keys in `qing_household_l_english.yml` (BOM preserved).

### #77 — auto-fill ALL ministry sub-posts (1:1 mapping; mint via exam when short)
Sub-post map (from the explorer): 13 top offices already autofill (`QING_council_autofill`). Ambans already
seed+sweep. The Studies (Southern/Upper) & Xinjiang begs already seed+auto-draw. The **three ministry corps
started EMPTY and filled only by manual player clicks** — those were the gap:
- **Zongli diplomats** (`qing_zongli_diplomat`, count `qing_zongli_diplomat_count`, cap 6)
- **Censorate inspectors** (`qing_is_censor_inspector`, `qing_censor_inspector_count`, cap 6)
- **Imperial Guard captains** (`qing_is_imperial_guardsman`, `qing_guard_corps_count`, cap 6)

New file **`se_QING_SUBPOSTS.txt`** (BOM, matching CJK sibling se_QING_HOUSEHOLD):
- `QING_subpost_fill_one` — fills one seat: prefers the ablest FREE eligible courtier
  (`combined_stats_council_svalue`); when none free, MINTS via `QING_exam_mint_scholar {degree=juren}` — the
  minted man is tagged `qing_is_above_exp_student` and counted in `qing_above_exp_student_count` (the "students
  who performed above expectations" the user asked for). Pool-drop on seating (shared exit path).
- `QING_subpost_staff_corps` — live-recounts from the marker (stale seats read vacant), then fills up to a
  target of 4 (unrolled 4 rungs; engine `while` counts only literals, and caps are small).
- `QING_subpost_seed_gamestart` — wired into `on_game_initialized` right after `QING_amban_seed_gamestart` and
  BEFORE the perf fold; self-calls `QING_exam_init` (idempotent) since the seed runs before the normal exam init.
- `QING_subpost_refill_sweep` — wired into `QING_GOV_pulse` beside `QING_amban_post_sweep`; per-corps gated on
  the relevant GC office being filled (a headless ministry conjures no staff, mirroring the amban sweep).
- **Player retains** the panel Recall/Discharge levers; the next sweep refills the gap.

**1:1 mapping enforcement:** new trigger `QING_subpost_eligible_candidate` (qing_dynasty_triggers.txt) =
`QING_office_eligible_candidate` (already excludes ruler/heir/governor/general/admiral/vanilla-office/GC-seat)
PLUS a hard NOT on every other sub-post marker (diplomat / inspector / guardsman / southernstudy / upperstudy /
amban / eunuch / foreign-advisor). So a character holds AT MOST one post and each post one character, with no
overlap with governors/commanders/GC offices.
- **NOTE on "researchers":** Imperator has NO `is_researcher` trigger / researcher role — the analogous
  conflicting roles (governor/general/admiral/office) are already excluded. Nothing to add.

### Rites window (new user ask)
Added a read-out row "Students Raised Above Expectation (拔貢)" in `gui/qing_rites_ministry.gui` (after the
military-degree row) bound to `qing_above_exp_student_count`, with loc `QING_RITES_MINISTRY_ABOVE_EXP_LABEL/_TT`
in `qing_rites_ministry_l_english.yml` (BOM preserved) — surfacing the exam-minted sub-post staff as
above-quota provincial students, framed as 拔貢 (selection of the outstanding beyond the triennial cohort).

### BOM decisions
- `se_QING_MINISTRY.txt` ships **noBOM** and boots fine with heavy CJK → my CJK-comment edits kept it noBOM
  (adding a BOM would diverge from its committed booting state).
- `se_QING_SUBPOSTS.txt` (NEW) written **with BOM** — matches `se_QING_HOUSEHOLD` (the CJK scripted_effect that
  carries one) and the standing BOM rule for CJK common/*.txt.
- All loc .yml edits preserved their BOM.

### Verification
- Brace balance confirmed on all 9 edited files + the new file.
- Pending: mandatory boot-crash review (standing rule) BEFORE ready-to-test.

### Boot-crash review (mandatory standing rule) — result
Ran independent code-review agent on the whole batch. **No boot crash found.** All crash classes traced clean
(no #90 modifier-in-create_character; new trigger correctly in scripted_triggers; var-RHS all literal; static LOG
strings; BOM bytes correct; on_init ordering sound; braces balanced; events is_triggered_only + share the court
throttle; corps fill bounded, cannot over-fill/loop).
- **FIX APPLIED (medium):** `QING_subpost_staff_corps` recount now excludes `qing_office_held`, matching the
  sibling perf recomputes (`_censor`/`_guard_commandant`) exactly — so a corps member promoted onto the Grand
  Council reads as a VACANCY and is refilled, and the sweep-stored count agrees with the meter's count
  (belt-and-suspenders; `QING_office_appoint` already strips corps markers at seating).
- **Not changed (non-issues):** (a) the mint-branch pool-drop uses `has_variable` existence checks (the
  documented same-tick gotcha was a NUMERIC change_variable read-back, not a boolean existence check; the branch
  is rare — no free courtier). (b) `qing_above_exp_student_count` is a deliberate lifetime tally (matches loc),
  not a live headcount. (c) `qing_household_events.txt` / `qing_household_modifiers.txt` are noBOM, but ALL their
  CJK-bearing event/modifier siblings are noBOM and boot fine (CJK is comment-only) — adding a BOM would diverge
  from the booting convention, so left as-is.

---

## Character-window court-position title row (new user ask)

**Ask:** show a row under a character's name naming their Grand Council position / sub-position, the way a
governor's window shows "Governor of X" or a ruler's shows "Huangdi".

**Feasibility:** fully feasible + clean. The character-window header (characterwindow.gui:35) already renders the
name via a character-scope custom_loc (`TITLES_character_name`), and the appoint picker already renders an
"Incumbent: <office>" line via a `QING_office_held_name` custom_loc gated on `[Character.MakeScope.Var('qing_office_held').IsSet]`.
Reused exactly those proven mechanisms.

**Implemented:**
- **New custom_loc `QING_court_position_name`** (common/customizable_localization/00_offices.txt, BOM) — character
  scope. Names, in priority order: the 13 Grand Council great offices (reusing the existing office-name keys via
  the `qing_office_held` flag map, identical idiom to the proven `QING_office_held_name` sibling), then the
  ministry sub-posts (`qing_zongli_diplomat` / `qing_is_censor_inspector` / `qing_is_imperial_guardsman`), the
  studies (`qing_is_southernstudy` / `qing_is_upperstudy`), the amban (`qing_amban_marker`), and the palace eunuch
  (`qing_is_palace_eunuch`). Fallthrough → `QING_OFFICE_NAME_GENERIC` ("a great office"), matching the sibling
  (so a stray office flag never renders a blank row).
- **New loc** (qing_governance_l_english.yml, BOM): `QING_SUBPOST_NAME_DIPLOMAT/_CENSOR/_GUARD/_SOUTHERNSTUDY/`
  `_UPPERSTUDY/_AMBAN/_EUNUCH`, `QING_COURT_POSITION_NONE` (""), `QING_COURT_POSITION_ROW_TT` (tooltip).
- **GUI row** (characterwindow.gui, noBOM) — a subtitle textbox inserted right after the header, before the main
  content block, rendering `[CharacterWindow.GetCharacter.Custom('QING_court_position_name')]`. Visible only when
  the char holds a post — a nested `Or()` of the 8 marker `.IsSet` checks (the proven `qing_office_held.IsSet`
  visibility idiom; `.IsSet` on an absent var returns false, so it's a clean no-op for every non-Qing character
  whose window is opened). `ignoreinvisible` collapses the gap when hidden. Comments kept pure-ASCII (no CJK / no
  em-dash) since the .gui is noBOM.

**1:1 alignment:** because `QING_office_appoint` strips sub-post markers on seating and
`QING_subpost_eligible_candidate` blocks double-booking (both from the earlier #77 batch), at most one branch
matches per character — the row names exactly one position.

**Boot-crash review:** ran independent review — CLEAN, no boot/gui-load/loc-load risk (custom_loc faithful to the
proven sibling; all 24 loc keys defined; Or() balanced 7/7; empty-string loc value legal; BOM states correct;
.gui confirmed pure ASCII). Applied the one low cosmetic suggestion (fallthrough → generic, not blank).
