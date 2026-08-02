# Overnight Batch — autonomous work log (2026-07-22 → 23)

Running log of all changes made while the user is away. Each item: what, why, verify, review, commit hash. One push at the very end. Branch: merge-overnight.

## Work queue (in order)
1. **Divorce sweep** — stop engine gamestart auto-marriage of historically-single rulers (task #50 general case). Priority-1 MUST-STAY-UNMARRIED: char 616 Pope Clement XIII (PAP), 617 Carlo Emanuele III (SAR, widower), 622 Amat (PR1, bachelor), 572 Augustus III (POL, widower). char 144 Catherine already fixed (rus_expansion.10).
2. **Batch 1** (#37) — colonial reparents: HEL→DEN, BIG→NED, SLE→inert, BLZ→SPA.
3. **Batch 2** (#40) — ruler labels: SIA dynasty (Ban Phlu Luang), Persia Qajar→Zand.
4. **Batch 3** (#41) — ION → Venetian subject.
5. **Batch 4** (#42) — free ALL 14 EIC-subject India states + update Qing India events/missions.
6. **Batch 5** (#43) — fragment KHL Sikh Empire into 1763 misls.
7. **BT-3** (#48) — per-prince heir-backing + vanilla-style heir display.

Follow-ups logged, not force-fixed:
- **Data-gap monarchs** (Priority 2): 618 Jose I (BRZ), 620 Max III Joseph (BAV), 615 Adolf Frederick (SWE), 125 Francis I (AUS), 406 Louis XV (FRA) — historically MARRIED but lack marry_character, so the engine auto-marries them to a random stray. The DIVORCE fix is WRONG for them (they should be married, not single); correct fix = create/link their real spouse. Separate task, NOT done here.

---

## LOG

### 1. Divorce sweep — BUILT (pending review+commit)
Added imp19c_setup.10 (events/imp19c_mod_events/imp19c_setup_events.txt) divorcing chars 616/617/622/572; dispatched from oa_economy_setup.txt at days=2. Both files brace-balanced. Priority-1 targets verified (all rulers, no marry_character). Catherine 144 left on rus_expansion.10.
APPROACH NOTE: chose a single hidden sweep event over per-tag events (scales; one dispatch line). days=2 mirrors qing_force_setup deferral so it runs after the engine's post-on_game_initialized auto-marriage. Data-gap married monarchs (618/620/615/125/406) deliberately EXCLUDED — divorce would be wrong for them.

### 2. Batch 1 — colonial reparents — BUILT (pending review+commit)
setup/main/00_default.txt, all brace-balanced (10959/10959):
- HEL (landless, dependency-only): GBR->DEN (Heligoland Danish 1714-1807).
- BIG (British Guiana, 3 provs incl. "New Amsterdam"): GBR->NED + culture english->dutch, religion lutheran->reformed (Essequibo/Demerara/Berbice Dutch till 1796-1814).
- BLZ (Belize, 2 provs): GBR->SPA client_state (Spanish de jure 1763; Britain had only logging rights).
- SLE (Sierra Leone, 3 provs): dependency REMOVED -> independent. APPROACH NOTE: no European colony existed in 1763 (British 'Province of Freedom' 1787). Ideal = inert, but no native successor tag exists to absorb Freetown/Sherbro/Cape Coast; a landless-with-ruler tag crashes, so instead left SLE as a small INDEPENDENT owned tag (boot-safe). Recorded as a deliberate compromise.
All 4 tags have engine-gen rulers (no anachronistic char to reseat); DEN/NED/SPA all exist as landed overlords; no GBR-arc/mission/customs refs to BIG/SLE/BLZ/HEL.

### 3. Batch 2 — ruler/dynasty labels — BUILT (pending review+commit)
- SIA: dynasty-pool family 23 key "Chakri" -> "Ban Phlu Luang" (00_default.txt:171). Chakri began 1782; Ban Phlu Luang (King Ekkathat) ruled Ayutthaya in 1763. SIA has NO setup ruler char — draws engine-gen ruler from this pool family, so the pool-key rename is the correct fix.
- PERSIA: NO CHANGE. Research claimed PR2 family=13 Qajar; VERIFIED FALSE for the seated ruler — PR2 is already ruled by char 578 Karim Khan Zand (family c:ERI.fam:Zand, 00_Persian Empire.txt:197). The "Qajar" refs are the dynasty POOL (future-gen) + the ERI khanate ruler (char 548 Hossein Khan Sardar, correctly Qajar). Seated ruler already correct -> dropped.

### 4. Batch 3 — ION -> Venice — BUILT (pending review+commit)
- ION (Ionian Is., 4 greek/orthodox provinces Corfu etc.): dependency GBR protectorate -> VEN autonomous_governorship (00_default.txt:657). Venetian Stato da Mar till 1797; British protectorate is 1815. NOTE: Venice tag is VEN (not VNC as the task said); VEN is landed (north_italian, cap Venice 1135), sovereign in 1763. autonomous_governorship = the overseas-holding subject type (matches Spanish colonies). ION not double-parented; no GBR-arc refs.
Batches 1-3 all in 00_default.txt, braces 10959/10959.

### Boot-crash review (divorce sweep + Batches 1-3) — PASS after 1 fix
Independent review flagged ONE blocker (A5): the imp19c_setup.10 dispatch in
oa_economy_setup.txt was a BARE `trigger_event` in the on_game_initialized effect
block, which has no implicit country scope — every other trigger_event there is
wrapped in `c:XXX = {}`. A country_event must be dispatched from a country scope.
FIX: wrapped in `if = { limit = { exists = c:CHI } c:CHI = { trigger_event ... } }`
(event is self-scoping via absolute char:N, so carrier tag is arbitrary; CHI = the
always-present player). All other items PASS (divorce targets verified 4/4 rulers
no marry_character; overlords landed; SLE landed not landless-crash; SIA family key
with spaces valid per "Nguyễn"; ION single-parent; braces 10959/10959; BOM state ok).

### COMMITTED
- 0e3501f1 — #50 divorce sweep (imp19c_setup.10 + c:CHI dispatch).
- c1ff0dde — #37/#40/#41 Batches 1-3 (00_default.txt).

---

### 5. Batch 4 (#42) — free ALL 14 EIC-subject India states — DONE
Commented out 14 EIC dependency lines in 00_default.txt (MYS COO TRV HYD TJR DHN RMH
BNR BIH PAT AWA MUG BHU SKK). Research agent + boot-crash review agent BOTH confirmed:
all 14 LANDED (own provinces + capital owned + engine-gen ruler, no set_as_ruler) so
no landless-with-ruler crash; downstream Qing India missions/events UNAFFECTED (they
use FUNC_make_subject from any start-state; free-Mughal arc guarded NOT is_subject_of=ROOT;
asia_napoleonic.3 only touches c:EIC itself). No customs unions / nested sub-subjects /
orphan overlord refs. Trade agreements persist. Braces 10959/10959.
APPROACH NOTE: chose COMMENT-OUT over hard-delete (reversible, traceable; matches the SLE
precedent block right below). Single-file edit — the whole point of the research pass was
to prove no Qing India event/mission rewrite was needed, and it wasn't.
COMMITTED: 2d093f22.

### 6. Batch 5 (#43) — fragment KHL Sikh Empire into 1763 misls — IN PROGRESS

LOCKED PLAN (after research + collision checks):
KHL is an anachronistic UNIFIED Sikh Empire (Ranjit Singh, post-1799); its dynasty
pool is `Sukerchakia` (char 21 = Ranjit Singh's own misl). In 1763 the Punjab was the
Dal Khalsa — a confederacy of misls — with the west/north (Peshawar/Multan/Kashmir/
Derajat) held by the Durrani Afghans.

DESIGN: REPURPOSE KHL as the Sukerchakia Misl (keeps KHL a valid FEATURED/selectable
lobby tag — gui/shared/window_templates.gui uses ln.png + ln.dds + KHL_DESK, and the
DESK text already describes "the Sikh misls of the Dal Khalsa... the future Sikh Empire
would one day be forged", which fits a misl perfectly; Ranjit Singh char:156 keeps
spawning into KHL). Then mint 4 NEW tags (BHM Bhangi, AHL Ahluwalia, PHU Phulkian,
JMU Jammu) and hand the western/northern periphery to the existing AFG (Durrani).

Tag collisions checked: BHM/AHL/PHU/JMU all FREE. PAT=Patna and JAM=Jamaica were TAKEN
(so Jammu -> JMU). AFG exists + is landed (safe to receive 27 provinces).
New-tag template = the proven #300 BNG (Nawab of Bengal) 1763 tag: registry line in
countries.txt + def file setup/countries/india/<x>.txt + country block in 00_default.txt
(NO family=, NO set_as_ruler -> engine generates a period ruler, sidesteps char-ID
contiguity entirely) + se_COUNTRYNAME.txt custom-name line + countries_l loc (X:1 + X_ADJ:1)
+ COA. NO province-history ownership files touch these provinces (ownership lives only in
00_default own_control_core), so moving provinces is a pure 00_default edit.

Province split (46 total): KHL/Sukerchakia keeps Gujranwala core (5); BHM gets Lahore+Amritsar
core (4); AHL Doaba/Jalandhar (5); PHU cis-Sutlej Malwa (4); JMU Jammu (1); AFG gets the
27 Durrani periphery (Peshawar/Attock/Multan/Derajat/Kashmir/west Punjab).

DONE + COMMITTED cbdfcd84. Boot-crash review passed 8/8 (landless, double-ownership,
registration completeness vs BNG template, family/set_as_ruler, dangling KHL refs,
culture/religion/govt keys, loc/brace/BOM, tag collision). Partition is an exact bijection
(5+4+5+4+1+27=46). New def files carry BOM. Braces 10967/10967. Only KHL refs elsewhere are
se_CURRENCY (rupee adopter — still correct for a misl) + se_COUNTRYNAME custom-name + the
KHL_DESK lobby feature — all stay valid since KHL remains a landed featured tag.

### 7. BT-3 (#48) — per-prince heir-backing + colour-coded chip + legend — DONE
APPROACH: the user's asks #5/#6 (reuse vanilla heir-portrait card, script-recalc its scores)
are ENGINE-IMPOSSIBLE — vanilla heir-support is read-only C++ (memory imp19c-vanilla-heir-
support-readonly). The custom 皇子 panel already IS the Qing-scored heir display; so I built
asks #1-#4 and wired the panel's per-prince colours to the council chips. Chip now ALWAYS
present, grey=neutral, one of 4 birth-order colours = which prince backed; legend swatch on
each prince row. Built entirely on the PROVEN .IsSet overlay idiom (grey base + 4 colour
overlays each gated on a mirrored slot flag) — zero GUI value-comparison (the repeated blank
cause). Slot flags: qing_prince_slotN stamped eldest-first in the roster recompute; mirrored
to qing_hf_slotN on each backer in assign_core; swept on neutral/clear_all. Boot-crash review
passed 7/7 (incl. the critical increment-before-read ordering). COMMITTED fb6b61a2.

--- ALL 7 QUEUE ITEMS DONE. ---

### FINAL: cross-cutting review + PUSH
Ran a final CROSS-CUTTING boot-crash review over all 5 commits together (to catch
interactions the per-commit reviews couldn't — 3 of the 5 touched 00_default.txt).
PASSED 7/7: 00_default brace balance 10967/10967 + no clobbered/duplicate blocks; zero
province double-ownership (Punjab misls disjoint from the freed EIC India states); all 24
changed tags' capitals in-core (KHL 1917, BHM 2876, AHL 4427, PHU 5340, JMU 1311, AFG 9390
not moved); 4 new-tag registry+def files present; divorce chars (616/617/622/572) unrelated
to India; NO new char ids (contiguity intact); no broken c:TAG refs.

PUSHED to origin/merge-overnight (29fcc69b1..fb6b61a21) — 5 commits, ready for boot test:
  0e3501f1  #50 divorce sweep (4 single rulers)
  c1ff0dde  #37/#40/#41 Batches 1-3 colonial/independent reparents
  2d093f22  #42 free 14 EIC India subjects
  cbdfcd84  #43 KHL -> Dal Khalsa misls (4 new tags + AFG periphery)
  fb6b61a2  #48 BT-3 colour-coded succession chip + legend

BOOT-TEST WATCH ITEMS (things to eyeball in game):
- New misl tags (BHM/AHL/PHU/JMU) render with a fallback COA (no explicit COA authored —
  optional per BNG precedent, engine assigns one; author proper flags later if desired).
- BT-3 chip: confirm it shows on ALL minister cards (grey when neutral) and that the colour
  matches the prince's legend swatch on the 皇子 panel. This is the 6th+ attempt on this chip
  family — if blank again, the fault is NOT the .IsSet idiom (proven), look at instantiation.
- Divorce sweep: confirm the 4 rulers (Pope/Carlo Emanuele/Amat/Augustus III) show single at
  1763 start (day-2 event).
- Freed India: the 14 EIC states + the Punjab misls should appear independent on the map.
STILL OPEN (not in this batch): proper COAs/flags for the 4 new misl tags.

### POST-PUSH FOLLOW-UPS (user-requested, this session)

8. SLE fully inert (R2) — COMMITTED 2b3579c4. On the user's prompt ("cant you just empty the
provinces, leave them ownerless and move SLE's capital"), replaced the Batch-1 placeholder
(independent 3-prov SLE) with the proven inert-tag playbook: own_control_core emptied ->
Freetown/Sherbro/Cape Coast become unowned native frontier; capital 3357->3388 (GBR-owned);
no set_as_ruler + viceroyalty govt = boot-safe. Boot-crash review passed (matches ALC/NSW).

9. #50 data-gap MARRIED monarchs — DONE (pending review+commit). Added the 5 monarchs' real
wives as setup chars (627 Mariana Victoria->618 Jose I; 628 Maria Anna Sophia->620 Max III
Joseph; 629 Louisa Ulrika->615 Adolf Frederick; 630 Maria Theresa->125 Francis I; 631 Marie
Leszczynska->406 Louis XV), each female=yes + marry_character=char:<husband>, so the engine
pairs them correctly instead of auto-marrying a random stray. IDs contiguous 627-631 (max was
626); family_name string (no dynasty pointer, per the Charlotte/89 precedent); no death_date
(all alive 1763); BOM preserved. Boot-crash review passed 8/8. COMMITTED 7bdf9689.

--> #50 (auto-marriage) now FULLY CLOSED: 4 genuinely-single rulers divorced (imp19c_setup.10)
+ 5 historically-married monarchs given real spouses. Both halves complementary.

PUSHED (fb6b61a21..7bdf9689f): 2b3579c4 SLE inert R2 + 7bdf9689 data-gap spouses.
Ready for boot test alongside the earlier 5-commit batch.

### 10. Subject-integration rework: capstone hands off to VANILLA engine integration — DONE (pending review+commit)
USER DIRECTIVE: keep ALL custom logic (ladder, promote/demote, 5-step meter, reaction
events, .30 capstone + .40/.41 decree/resistance); change ONLY the capstone so instead of
instant-annexing it starts the vanilla integration process. Confirmed: the old capstone
instant-annexed (SUBJ_QING_absorb_subject -> LAND_transfer_provinces, same-tick).

ORACLE FINDING (TI + Invictus, both agree): vanilla subject-integration is a HARDCODED
engine mechanic — NO script verb starts it (start_integrating_subject/integrate_subject do
NOT exist; integration_progress is CULTURE integration, different system). The only
interface is (a) can_be_integrated = yes on the subject type -> engine's native Integrate
action appears, and (b) on_diplomatic_annex on_action fires on completion. This build DOES
have the native integrate relation (diplomatic_view.gui:1037 #integrate,
diplomatic_status_integrate_tooltip), so the handoff is feasible.

DESIGN (3 user decisions via AskUserQuestion): keep all custom logic; capstone flips the
flag + player finishes via engine; retire the custom instant-annex so the ONLY land
transfer is the engine (single path).

CHANGES:
- common/subject_types/00_default.txt: NEW transient type `integrating_governorship` =
  byte-clone of autonomous_governorship EXCEPT can_be_integrated = yes. autonomous_governorship
  STAYS can_be_integrated = no (native button hidden during the political phase).
- se_SUBJECT_QING.txt: NEW SUBJ_QING_authorize_integration — reparents sub-subjects NOW
  (while intermediary exists, correct ROOT=overlord scope), converts subject to
  integrating_governorship (lights up native Integrate), clears custom progress/active state.
  Capstone auto-fire path + fallback comments updated. (Removed a dead marker var-set.)
- events/.../qing_integration_capstone_events.txt: qing_integ.30 all 3 options now call
  SUBJ_QING_authorize_integration instead of SUBJ_QING_absorb_subject; costs/modifiers unchanged.
- SUB_QING_subject_interactions.txt: NEW qing_subject_type_is_integrating indicator. Promote/
  demote/integrate buttons still gate on autonomous_governorship so they hide once converted.
- gui/diplomatic_view.gui: type-label chain (both tabs) wrapped with the integrating case.
- loc: QING_SUBJECT_TYPE_INTEGRATING "Being Integrated (改土歸流)".

WHY reparent at authorize-time not on_diplomatic_annex: in on_diplomatic_annex ROOT = the
annexed subject (about to be deleted) and its sub-subject links vanish with it; reparenting
at authorize (ROOT=overlord, subject still exists) is the correct + only safe window. So
on_diplomatic_annex needs NO change (vanilla family cleanup already hooked there).

Flow: custom ladder -> autonomous_governorship -> 5-step meter fills (push button + frontier/
Xinjiang/caravan/reaction events) -> capstone .30 -> authorize -> integrating_governorship ->
player clicks native Integrate -> engine absorbs GRADUALLY. No reachable instant-annex on the
governorship path (line-258 direct absorb is an unreachable non-governorship safety net).
Braces all balanced. PENDING boot-crash + differential review, then commit.

---

## BOOT TEST — pre-overnight changes (below 0e3501f17). Findings:

### Section A — 1763 rulers seated (#31)
- A1 SPA Carlos III / AUS Francis I — PASS
- A2 PRU Frederick the Great / MUG Shah Alam II — PASS
- A3 SWE Adolf Frederick — PASS
- A4 PAP Clement XIII — PASS
- A5 SAR Carlo Emanuele III / POR+BRZ Jose I / TUR Mustafa III / BAV Max III Joseph — PASS
- A7 QTO Rubio de Arevalo / PR1 Amat / BWP Muhammad Bahawal Khan (Daudputra) / GUA Heredia / PHI Anda — PASS (BWP explicitly confirmed by user)
- **A6 MSS — FAIL.** Ruler displays as "Maria Teresa TUCCIMEI" (a random north_italian
  surname), not d'Este / Cybo-Malaspina. ROOT CAUSE: reseat commit 7d528867f made char 608
  the ruler, but 608 (and 607 Ercole III) have family="c:MSS.fam:dEste" with NO family_name
  literal; the dEste family is never DECLARED (MSS owns no family in 00_default), so the engine
  falls back to a random culture surname. Old ruler 134 displayed fine because it ALSO carries
  family_name="d'Este" (the literal fallback). FIX: add family_name to 608 (+607). Awaiting user
  choice of surname: "d'Este" (matches daughter/setup) vs "Cybo-Malaspina" (her own house).
  NOT YET FIXED.

### Section B — territory / tag reworks (#31)
- B1 MEX gone -> single Viceroyalty of New Spain (NSP) — PASS (user confirmed "MEX is correctly gone")
- B2 NSP ruler — PASS. Shows "Joaquin de Montserrat" = char 580, first_name="Joaquin"
  family_name="de Montserrat" = Joaquin de Montserrat, Marques de CRUILLAS, the real 1763
  Viceroy. "Cruillas" is his TITLE; "Joaquin de Montserrat" his personal name (correct display).
  BT-6 worked. (User flagged the name; verified it is the intended person, not a regression.)

### A6 MSS/Tuccimei — FIXED (pending commit)
Added family_name="d'Este" to chars 608 (ruler) + 607 (Ercole III consort) in 00_Italy.txt,
matching char:134's working literal. Was rendering random "Maria Teresa Tuccimei" because
c:MSS.fam:dEste is an undeclared family -> engine fell back to a random north_italian surname.
User chose surname = d'Este. Braces 42/42, BOM intact. NOT YET COMMITTED.

### Deferred task added
- #51 — rework Macau (prov 2481) POR->CHI territory + Portuguese foreign concession building
  (existing qing_foreign_buildings.txt section). Macau was Qing-sovereign in 1763 (Portugal
  gained sovereignty only 1887). Deferred until after this boot-test pass.

### Section C — marriage/succession GUI (#31/#30)
- C1 marriage screen 2 — PARTIAL/REGRESSION. Screen 2 now CLOSES (BT-1 goal met) BUT screen 3
  (marriage_play_their_window) NEVER APPEARS. User: "you broke it." INVESTIGATING.

### C1 marriage screen 3 — FIXED R2 (pending commit)
Root cause of the regression: the BT-1 R1 fix put ClearWidgets(own_window) BEFORE
createwidget(their_window). ClearWidgets destroys the button's host window mid-chain, so the
subsequent createwidget never ran -> screen 3 never appeared. The ORIGINAL screen-2-wont-close
bug was the margin-on-bare-widget flood (already fixed on screen-3 widgets), NOT the order.
FIX R2: Execute -> createwidget(screen 3) -> ClearWidgets(self) LAST (proven office-picker order).
Both rows (adults+children). Braces 103/103. NOT YET COMMITTED.

### D1 religion pantheon — PARTIAL. Deities list renders again (not blank) BUT it SPILLS over
the bottom edge of the panel (scroll/clamp failing). INVESTIGATING.

### D1 religion pantheon — STILL SPILLS (BT-2 not fully fixed)
Deities list renders (not blank) but SPILLS over the panel's bottom edge. Current structure
(religion_view.gui:435-455): parent flowcontainer(vertical) -> scrollarea name=pantheon_scroller
size={620 600} using=VerticalScrollAreaCutOff -> scrollwidget -> dynamicgridbox (no size).
The scrollarea IS fixed-size + cutoff, so the SPILL is likely (a) the scrollarea's on-screen
POSITION starting too low so 600px runs past the window bottom, or (b) VerticalScrollAreaCutOff
not actually clipping in this parent, or (c) the #45 ignoreinvisible on the shared parent not
applied. NEEDS DIFFERENTIAL DIAGNOSIS vs the working Holy-Sites scrollarea in THIS file — do
NOT re-guess (memory: failed 7x). NOT FIXED.

### D2 missions UI — STILL SCATTERED/BROKEN (BT-4 not fixed)
Graphic elements wildly misplaced. Same fragile family as pantheon. NEEDS DIFFERENTIAL
DIAGNOSIS vs a working mission-tree reference. NOT FIXED.

### D3 diplomat corps — STILL BREAKS 1:1 (BT-7 not holding)
User: "diplomats are still commanders and Ministers." The BT-7 fix (606ea8742) added a
qing_officer_marker exclusion at 4 chokepoints; either it's not applied at the diplomat-corps
builder, or the exclusion predicate is wrong (commanders + GC office-holders still leak in).
INVESTIGATING — verify the fix is present + gating the RIGHT roster.

### D3 diplomat corps — DIAGNOSIS (BT-7 gap found, but incomplete)
BT-7 added qing_officer_marker to 4 spots. Audit of the strip/gate sets now:
- QING_office_eligible_candidate (hire gate): HAS officer_marker + office_held  ✓
- QING_subpost_strip_double_booked (SUBPOSTS:112): HAS officer_marker  ✓
- render rebuild (MINISTRY:455): HAS officer_marker + office_held  ✓
- QING_subpost_staff_corps strip (SUBPOSTS:154): **MISSING qing_officer_marker**  ✗ <- real gap
BUT: ministers carry qing_office_held, which IS in ALL four sets — so a MINISTER leaking is
NOT explained by the 154 gap (that only leaks commanders). User sees BOTH commanders AND
ministers. => the render rebuild (455) that the panel shows DOES strip both; if a minister
still renders, either the panel reads a DIFFERENT list than qing_zongli_diplomats, or the
render recompute is not firing on open. NEEDS the differential-debug skill (2nd BT-7 attempt;
do NOT keep patching strip-sets blind). Confirmed fix-worthy: add officer_marker to SUBPOSTS:154.

### D4 title slots — PASS (user: "title slots are showing fine")

### D5 succession chip (BT-3 redesign) — STILL NOT SHOWING
The colour-coded per-prince chip (fb6b61a2) is not appearing. This is the 6th+ attempt on this
chip family. Needs differential diagnosis: is qing_prince_slotN being stamped (script), is
qing_hf_slotN mirrored onto officials, and is the chip instantiated on the card. NOT FIXED.

### D6 Talleyrand phantom (BT-7/B7) — PASS (user: "Talleyrand is confirmed fixed")

### C2 / BT-5 Catherine auto-marriage — STILL FAILING
User: Catherine married "Boris Ryzhkov" (was "Viktor Goncharov" last boot). The rus_expansion.10
divorce fix (cf10677df) is in this build but is NOT divorcing her. Same class as the overnight
imp19c_setup.10 sweep (which handled 616/617/622/572, NOT Catherine — she was left on
rus_expansion.10). If rus_expansion.10 fails, imp19c_setup.10 likely fails the same way ->
the WHOLE divorce approach may be broken. INVESTIGATING — top priority (affects overnight work too).

### C3 RUS heir — PASS (user: "RUS has no heir listed, which seems normal judging by other
diplomacy panels"). Not the old stale-Qing-char bug; a blank heir is normal display.

### B3 Ceylon + Kandy — PASS (user: "Ceylon and Kandy are fixed")

### C2 / BT-5 Catherine — DIAGNOSIS (timing hypothesis; affects overnight work)
char:144 IS Catherine (Yekaterina II). rus_expansion.10 IS dispatched (rus_expansion_on_actions.txt:29
trigger_event days=1) and its immediate divorces spouse. LEADING HYPOTHESIS: days=1 fires BEFORE
the engine's gamestart auto-marriage completes -> the trigger's `char:144={is_married=yes}` is FALSE
at day 1 (not yet married) so the event no-ops, THEN the engine marries her at day 1+. The event
does not re-fire, so she stays married.
IMPLICATION: the overnight divorce sweep (imp19c_setup.10) fires at days=2 — MIGHT be late enough,
MIGHT NOT. If day-2 is also too early, ALL 5 divorces (616/617/622/572 + this pattern) fail.
ROBUST FIX (regardless of exact auto-marriage tick): re-fire the divorce over a WINDOW (re-check
for the first ~month, divorce whenever is_married becomes true) instead of a single early shot.
NEEDS verification of the actual auto-marriage tick, or just switch to the windowed approach.
NOT FIXED — top priority (impacts committed overnight work).

### D5 succession chip — DIAGNOSED via logs+screenshots+git (NOT a new fix needed)
CRITICAL: the user booted build 827648b9a (PRE-overnight) — debug.log shows ZERO mirror_slot/
qing_hf_slot (my BT-3 redesign fb6b61a2 was NOT in the booted build). So the chip failure they
saw is the OLD chip, and my redesign is UNTESTED.
Root cause of the OLD failure, now understood: the booted chip gated on
visible="[...GetVariable('qing_favored_heir').IsSet]". debug.log PROVES qing_favored_heir WAS set
("heir-favour: the council backs the front-runner"). Yet the chip didn't show. WHY: qing_favored_heir
is a CHARACTER-valued var (value = scope:qing_hf_frontrunner). EVERY working chip in the mod gates
.IsSet on an INTEGER var (qing_char_affinity/qing_char_stance); there is NO working precedent for
.IsSet on a character-ref var. => .IsSet on a character-valued var does NOT report true in GUI the
way a flag/int var does. My redesign (fb6b61a2) replaced it with qing_hf_slotN INTEGER flags
(set_variable value=1) — the proven-working kind — so the redesign SHOULD fix D5. Screenshots also
confirm the data side is fine: Court Intrigue shows 5 princes with Court Backing (40/42/39/56/47);
the GC cards render the other two chips (favor/faction) fine, only the heir chip is absent.
ACTION: none needed beyond the already-committed redesign; re-test on next boot. Reverted a WRONG
mid-diagnosis (leader.dds "missing texture" — it loads fine from base game, 10 other refs, no error).

### C2 Catherine + divorce sweep — FIXED (robust timing)
Root: the booted build (827648b9a, 00:50) PREDATES the BT-5 Catherine fix (cf10677df, 02:28)
AND the overnight sweep — so Catherine married because no fix was present. But the single-shot
day-1/day-2 divorce is timing-fragile (engine auto-marriage tick is not fixed). FIX: made BOTH
rus_expansion.10 (Catherine) and imp19c_setup.10 (the 4-ruler sweep) SELF-RESCHEDULING — divorce
whoever is currently auto-married, re-fire every 30 days for ~6 months (pass-capped) until single.
CAUGHT A BUG mid-fix: rus_expansion.10's trigger gated on char:144.is_married=yes, which would
BLOCK the event (and the re-arm) if she wasn't married yet at day 1 — removed that gate (trigger now
tag/exists/alive only; divorce guarded is_married in the immediate). imp19c_setup.10 is
is_triggered_only w/ no trigger block, so no same bug. Braces 60/60 + 79/79. COMMITTED below.

### D3 diplomats — FIXED (closed the 4th BT-7 chokepoint)
Root: booted build (00:50) PREDATES BT-7 (606ea8742, 01:58), so the Tsedan-in-corps the user saw
was the pre-fix build. BUT a real gap remained in current HEAD: QING_subpost_staff_corps:154 strip
was the ONE BT-7 chokepoint (of 4) that 606ea8742 missed — a garrison field officer (qing_officer_marker,
not reliably is_general) could linger via this staffing sweep. Added qing_officer_marker to line 154
so all 4 chokepoints match. Verified via imp19c_effects_legion_setup.txt:182 that garrison officers
(Tsedan 612) DO carry the marker. Braces 79/79. COMMITTED below.

### FIXING SESSION (post-boot-test, logs+screenshots+git) — RESULTS
Key realization: the booted build was 827648b9a (00:50), which PREDATES most of the fixes —
so several "still broken" reports were stale-build artifacts. Fixes made/committed:
- 2f4c4fc3 — A6 MSS "Tuccimei" (family_name d'Este) + C1 marriage screen-3 (onclick reorder).
- fde3bcb7 — C2 divorce timing (self-reschedule) + D3 4th BT-7 diplomat chokepoint (staff_corps:154).
- 6730a0af — D1 pantheon spill (gridbox size, Holy Sites sibling) + D2 missions scatter
  (restored flowcontainer wrapper) + C2 review-fix (re-arm gated only on pass counter, was
  wrongly gated on is_married which defeated the window).
- D5 succession chip: NO new code — the OLD chip gated on a CHARACTER-valued var's .IsSet
  (doesn't render); my redesign fb6b61a2 already fixes it (int flags). Untested.
All fixes reviewed (code + boot-crash) before commit. Every one is fixed-but-UNTESTED (booted
build predated them); need a fresh boot. GUI fixes used the imp19c-debug differential skill +
git history to avoid the 11x-cycle. Recorded 2 memories: integrate_speed-is-subject,
GUI-.IsSet-character-var-quirk.

Still open: #51 Macau (deferred).

### D1 REOPENED — my gridbox-size fix was based on Holy Sites, a REJECTED reference
User (repeatedly): Holy Sites is NOT a valid reference — its list is too short to ever scroll,
so it never exercises the clip/scroll path and is not comparable to the long Pantheon list.
Reverted the size={600 160} I added to omens_grid. The ONLY valid proven large-scroll reference
is the OFFICE PICKER (qing_office_picker_window). Structural diff vs it:
- office picker: base_window{650x550} > vbox{MainWindowHeaderBoxCentered} > scrollarea{620x660}
  + plain scrollbar_vertical (NO VerticalScrollAreaCutOff) > scrollwidget > UNSIZED gridbox. WORKS.
- pantheon: flowcontainer{margin} > flowcontainer{vertical} > scrollarea{620x600} +
  VerticalScrollAreaCutOff > scrollwidget > UNSIZED gridbox. SPILLS.
Two candidate differences: (1) parent is flowcontainer, not a bounded vbox/base_window;
(2) uses VerticalScrollAreaCutOff instead of plain scrollarea+scrollbar. Memory
imp19c-pantheon-missions-scroll-rule already says the office-picker idiom "needs a bounded parent
imp19c lacks" — so the fix is likely to BOUND the pantheon scrollarea's parent (give it a sized
vbox), NOT to size the gridbox. Diagnosing against the office picker next (NOT Holy Sites).
D1 = NOT SOLVED.
