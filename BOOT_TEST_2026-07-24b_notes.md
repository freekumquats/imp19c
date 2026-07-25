# Boot test 2026-07-24 (post law Batches 1-3) — running notes

## BT-A — "The Question of Korea" (qing_vassal.1) fired in 1763 (~100y too early)
- ROOT CAUSE FOUND: fired by `QING_frontier_flavour_roll` random_list (se_QING_DECLINE.txt:1180-1186),
  branch gated ONLY on `NOT lost_korea` + `exists JPN|TKG`. Tokugawa (TKG) exists at 1763 → fires immediately.
  NO date/era floor. The event is a late-Qing imperialism crisis (Sino-Japanese, 1894).
- SAME BUG CLASS (no era gate): qing_vassal.2 Vietnam (Sino-French 1884, :1187), .3 Ryukyu (1879, :1194),
  .4 Burma (1885, :1201). All four fire ~century early.
- FIX (pending): add an era/date floor to each of the 4 branches. current_date idiom is proven
  (se_QING_OPIUM.txt uses `limit = { current_date >= 1800.1.1 }`). Candidate floor ~1840+ (post-first-contact/
  treaty era) OR gate on qing_treaty_system_imposed / a Western-pressure flag. NOT a Batch 1-3 regression —
  pre-existing content bug surfaced by the test.

## BT-B — Religion panel: too much empty space at the BOTTOM
- Want: extend the window so there's a SMALL margin at the bottom, not a big gap.
- Site: gui/religion_view.gui `@window_height = 852` (+ the vertical-expanding scrollarea). NOT touched in
  Batches 1-3 (this is from the earlier session's religion-panel work).
- FIX (pending): trim/adjust @window_height so the clip line sits just under the last row.

## BT-C — Faith & Sedition panel now SQUASHED with a blank space at the very top
- "you messed up the F&S panel" — regression from the earlier-session F&S inline-list / layout edits.
- Interacts with BT-B (both are religion_view.gui vertical layout). Need to look at the F&S vbox/spacer.
- FIX (pending): investigate the F&S section layout (the earlier margin_widget spacer / expanding vbox).

## BT-D — Newly added laws all land in the RIGHT column; want them balanced (some on the left)
- The 7 Qing domain `laws_widget_area` blocks were all inserted into ONE (the right) vertical flowcontainer.
  Vanilla balances laws across TWO side-by-side flowcontainers (left col + right col).
- FIX (pending): distribute the 7 domain areas across the left + right flowcontainers (e.g. governance/
  fiscal/military/frontier left; court/culture/foreign right) so both columns are populated.
- This IS a Batch-1 GUI consequence (I stacked all 7 in the existing single Qing flowcontainer).

## BT-E — "Grand Secretary of the Secretariat" → "Grand Secretary of the Central Secretariat" — FIXED
- qing_governance_l_english.yml:242 (title) + :257 (tooltip). Both updated to "…Central Secretariat (內閣)".
- Pre-existing loc, not a Batch 1-3 change. Trivial text fix, applied immediately.

## BT-F — Qianlong (char:214) has no living wife at the 1763 start
- CAUSE: his marry_character="char:212" is COMMENTED OUT (00_Qing.txt:463) because char:212 (Empress
  Xiaoxianchun 孝賢純, Fuca) died 1748; the only other consort in setup, char:204 (Consort Chun 純惠),
  died 1760. Both dead by 1763.2.16 → no spouse.
- HISTORICAL FIX: his 1763 wife was the STEP-EMPRESS, Ula Nara clan (繼皇后 / 那拉皇后): b.1718, made
  Step-Empress 1750, fell from favour 1765, d.1766. She is ABSENT from setup entirely.
- BUILD (pending, setup addition — NOT a trivial edit): mint a new setup character (Step-Empress, Ula Nara
  clan, manchu, b.1718, female, NO death_date per the setup-snapshot rule) + marry_character to char:214.
  MUST respect the setup char-ID contiguity rule (gap compacts runtime ids → char:N mismatches). Use the next
  contiguous id. Marriage idiom: either marry_character on her block pointing to 214, or on 214 (the
  now-commented line) pointing to the new id. Verify female + culture + no_traits + family(Ula Nara) so she
  reads as a valid empress. Pre-existing setup gap, not a Batch 1-3 regression.

## BT-G — Harem portraits taller than every other panel — FIXED
- gui/qing_harem.gui:277 cpt_button was size = { 46 84 } (stretched to fill a 3-line row); every other Qing
  panel uses the standard { 46 68 }. Changed to 46 68. Row height (468x100) unchanged — portrait just no
  longer stretches. Trivial GUI consistency fix, applied immediately. Braces balanced.

## BT-H — Harem should be populated historically for 1763
- Currently the harem is seeded with generic minted consorts (QING_harem_init mints an opening 3). At 1763,
  Qianlong's actual harem should be represented by real historical consorts.
- Ties into BT-F (his empress, Step-Empress Ula Nara). 1763 harem candidates (living, from history):
  Step-Empress Ula Nara (繼皇后, b.1718 d.1766 — she IS the empress, BT-F); Consort Ling 令妃 (魏佳氏,
  b.1727, later Xiaoyichun, mother of Jiaqing, alive 1763, d.1775 — a KEY one); Consort Shu 舒妃 (葉赫那拉,
  b.1728 d.1777); Consort Yu 愉妃 (珂里葉特, b.1714 d.1792); Consort Rong 容妃 (the "Fragrant Concubine"
  香妃/和卓氏, b.1734 d.1788, entered court ~1760). BUILD (pending, setup addition): mint these as setup
  characters with qing_is_harem_consort + qing_consort_rank + marry/home to CHI ruler, respecting char-ID
  contiguity. Pairs with BT-F and with Batch 7 (harem subsystem). NOT a Batch 1-3 regression.

## LOG + SCREENSHOT ANALYSIS (2026-07-24 test, logs.zip + drive-download shots)

### KEY RESULT: my law work (Batches 1-3) produced ZERO script errors.
Grepped error.log for all 4 law files, the 7 domain areas, government_view.gui, and every bias var
(qing_*_bias, comp/quota/admin/tol/civic/censorate/provmil): 0 hits. The GUI split, 16 new laws, 4 stub
fills, and all bias-var wiring are clean. Screenshot 224326 confirms the Laws tab renders ALL headers +
laws with proper loc (no raw keys): Fiscal/Military/Frontier/Court/Culture headers + Canton/Caravan/Canal/
Upkeep/Provincial/FrontierTrade/Xinjiang/NationalIntegration/Princely/Penal/Ritual/Opium all show names +
option values correctly.

### error.log is a 996k-line FLOOD, but it is PRE-EXISTING, not from laws:
1. **~256k+ lines: CURRENCY_svalues.txt read-before-set = the UPSTREAM U4 bug.** (Script system error /
   Value of wrong type 'none' / Failed to fetch CURRENCY_amt_circulated/national_debt/gold_reserve_size.)
   The guarded-var FIX exists on the `upstream_bugs` branch but was NEVER merged to merge-overnight. This is
   the dominant flood. NOT mine. → decide whether to port the U4 fix to merge-overnight.
2. **~23k lines: qing_vassal_events.txt (BT-A runtime).** QING_vassal_defend -> QING_vassal_pressure_
   encroacher reads var:qing_encroach_pw "unset scope" / "Invalid left side during comparison 'var'" /
   "Failed to fetch qing_encroach_pw". So BT-A is TWO bugs: (a) fires ~century early (no era gate), (b) the
   Defend option errors because qing_encroach_pw isn't set when pressure_encroacher reads it. se_QING_VASSAL
   .txt:165 sets it as flag:$encroacher$ — the read at :166-168 or the pressure effect may run before the
   set, or $encroacher$ passes empty. Investigate the call order in QING_vassal_defend.
3. ~8k lines: gradient_black_flip.dds missing texture (cosmetic, pre-existing vanilla/mod asset gap).

### NEW screenshot-only findings:
- **BT-I — "debug_log_scopes has no localization"** shows in the Question-of-Korea "Defend Korea" option
  tooltip (shot 224110). A stray debug_log_scopes call left in an event/effect option. Find + remove.
- **BT-C refined** — the Faith & Sedition TAB content (header 民教相爭 + columns 仇教/民教/傳教 + "No province
  yet bears a mission station" + Suppress Missions button) is VERTICALLY CENTERED in an over-tall container:
  big blank gap ABOVE the content, button floating low. Fix = top-align the F&S vbox (drop an expanding/
  centering layoutpolicy) — the earlier-session fix over-corrected. gui/religion_view.gui.
- **BT-D confirmed** — Laws tab: ALL Qing law areas stacked in the RIGHT column, entire LEFT half empty.
  The 7 laws_widget_area blocks must be split across the two side-by-side flowcontainers.
- BT-B (religion bottom gap) — the Pantheon/Holy-Sites tabs (shots 224140) look OK-ish; the gap issue is
  mainly the F&S tab (BT-C). Re-verify window height after fixing BT-C.

### PUNCH-LIST STATUS
FIXED: BT-E (Central Secretariat), BT-G (harem portrait 46x68).
PENDING GUI: BT-C (F&S top-align), BT-D (laws two-column balance), BT-B (religion window height, re-check).
PENDING CONTENT/CODE: BT-A (vassal era-gate + qing_encroach_pw unset), BT-I (debug_log_scopes stray).
PENDING SETUP: BT-F (Qianlong wife / Ula Nara), BT-H (historical 1763 harem).
PENDING UPSTREAM: U4 currency flood — port the upstream_bugs fix to merge-overnight? (dominant log flood.)

## FIXES APPLIED (2026-07-24, post-analysis)
- **U4 currency flood — FIXED** (cherry-pick 2a395702b → merge-overnight commit 96bbea5cc). CURRENCY_svalues.txt
  reads now guarded on has_variable. Only file in the commit; probe/record-doc excluded. ~256k-line flood gone.
- **BT-A (vassal crises century-early) — FIXED.** Added `current_date >= 1870.1.1` floor to all 4 branches in
  QING_frontier_flavour_roll (se_QING_DECLINE.txt) AND to the 4 events' own triggers (qing_vassal_events.txt,
  defense-in-depth). 1870 = the scramble-for-tributaries era (Ryukyu 1872-79 / Vietnam 1874-85 / Korea
  1876-94 / Burma 1885). No longer fires at 1763.
- **BT-A (qing_encroach_pw ~23k flood) + BT-I (debug_log_scopes tooltip) — FIXED (same root cause).**
  QING_vassal_pressure_encroacher reads were unguarded; in the event-option TOOLTIP PREVIEW the engine
  evaluates the if/limit triggers WITHOUT running the preceding set_variable, so var:qing_encroach_pw read
  unset (23k errors) and fell through to else->LOG_fail->debug_log_scopes ("has no localization" in the Defend
  tooltip). Guarded all reads on has_variable + guarded the else's LOG_fail on has_variable → preview
  short-circuits cleanly; runtime behaviour unchanged. se_QING_VASSAL.txt.

- **BT-D (new laws all in right column) — FIXED.** The 7 Qing laws_widget_area blocks were all in the RIGHT
  flowcontainer (government_view.gui:2149). Moved the first 4 (governance/fiscal/military/frontier) into the
  LEFT flowcontainer (after upper_house_laws, before constitutional_laws); court/culture/foreign stay right.
  Now both columns populate. Braces 2025/2025; all 7 areas present.
- **BT-C (Faith & Sedition squashed + blank top) — FIXED.** Root cause: as the lone visible child of the
  expanding top-level body-vbox, the F&S body-vbox (whose expanding was dropped by the earlier BT#3 fix)
  got vertically distributed. Fix (omens/sites sibling idiom): RESTORE vertical-expanding on the F&S body
  vbox + DROP the contradictory fixed-170+expanding on the inner scrollarea (now clean fixed 170) + ADD a
  trailing expanding-filler widget so content TOP-PACKS under the tab row and slack goes to the BOTTOM.
- **BT-B (religion bottom margin) — deferred to next-boot visual check.** With the F&S filler now absorbing
  that tab's slack at the bottom, the F&S tab's margin is handled. The omens-tab @window_height (852) is a
  known chase; NOT blind-tweaking it — re-verify visually next boot and trim only if it still spills.
