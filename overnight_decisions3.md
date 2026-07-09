# Overnight Decisions — Session 3 (develop branch)

Running log of major design/engineering decisions taken during the overnight autonomous
run on the **develop** branch. Major decisions taken on the **1763_bookmark** branch are
logged in that branch's own doc (see the 1763 section at the end for the pointer), NOT here.

Author/committer for all commits: **freekumquats**. develop = testing candidate; promote
to master only after in-game verification and only when asked.

Work queue for this run (in order — as directed by the user across several messages):
1. **#272 + #273** — Grand Council: Empress throne seat + 2 new appointable offices
   (Central Secretariat 內閣大學士 + Imperial Guard 領侍衛內大臣) + Chamberlain rename.
   → code review → commit + push develop.
2. **#165** — Four-power dynamic sphere-of-influence system.
3. **Religion rework** — traditional Chinese Confucian/Taoist/Buddhist/Shenist folk
   religion vs. arriving Christian missionaries → religious tension/conflict.
4. **Marriage diplomacy** (DESIGN_MARRIAGE_DIPLOMACY.md follow-up).
5. Deep adversarial review of #165 + religion + marriage → commit + push develop.
6. Switch to **1763_bookmark**, implement Phase 2/3/etc (major 1763 decisions logged in
   the 1763 branch's own doc, NOT here).
7. On 1763: populate ALL countries with 1763-appropriate buildings/trade-goods/industry/
   production (fire off deep native-language historical-research agents as needed).
8. When develop + 1763 are both exhausted: new branch **trade_goods** — add New World
   crops to the required basket of 6 essentials + add rifles/porcelain/etc to manufactured
   goods (RISKY: ties into many core systems). Document in a NEW `new_trade_goods` doc;
   refer to SESSION_REPORT for why risky trade changes were previously deferred.

**Cross-cutting standing instruction:** log every major decision as I go — develop decisions
here in overnight_decisions3.md; 1763 decisions in the 1763 doc; trade_goods decisions in
new_trade_goods.md.

---

## 1. Grand Council #272 + #273 (Empress seat + 2 offices + Chamberlain rename)

**Status:** script + appoint-verb + all localization complete; GUI + SESSION_REPORT +
code review pending before the single combined develop commit.

### #272 — Empress throne seat + figurehead
- **Scope link:** `current_ruler.spouse` (PROVEN — `exists = spouse` at 00_ambitions.txt:1230).
  Empress is display + figurehead only (`QING_council_score_figurehead` weight 1); she NEVER
  enters any appointable-office loop.
- **Seat storage:** `qing_office_empress_holder` country var, refreshed each quarter by
  `QING_seat_refresh_empress` (added to `QING_seat_refresh_all` after crownprince; mirrors
  `current_ruler.spouse` when alive, else clears the var).
- **Gate trigger:** `QING_dynasty_has_empress` added to `qing_dynasty_triggers.txt` (a
  scripted_TRIGGERS file, per the #157/#165 lesson that limit-position conditions must NOT
  live in scripted_effects or the guard collapses at load → boot crash).

### #272 — Empress dynastic events (qing_dynasty.6/.7/.8)
- **.6 Empress Intercedes** (POSITIVE): heed-her (harmony +6, prestige) vs keep-to-palace
  (emperor prestige +15, harmony -5).
- **.7 Consort Clan 外戚** (NEGATIVE): curb-clan (harmony +2, corruption eased, empress
  loyalty -8) vs indulge-clan (empress loyalty +12, corruption up, harmony -4).
- **.8 Two Suns in the Inner Palace** (empress-vs-dowager, NEGATIVE): side-with-dowager
  vs back-the-empress. Gated on BOTH `QING_dynasty_has_empress` AND `_has_dowager`.
- All three: `is_triggered_only`, tag=CHI + empress gate, saved scopes `scope:empress`
  (+`scope:dowager` for .8), fired from `QING_dynasty_flavour_roll` weighted random_list.
- **#253 rule honoured:** every new `LOG_line` msg is STATIC text only ("EVENT qing_dynasty.6
  (empress intercedes)") — no bracketed `[data-functions]`, which `debug_log` cannot resolve
  and which flood error.log. Bracketed `[scope:X.GetName]` is used ONLY in loc desc strings
  (valid there — the loc renderer resolves them; only debug_log does not).

### #273 — two new appointable offices (council 11 → 13)
- **Central Secretariat — 內閣大學士 Grand Secretary** (key=`grand_secretariat`, skill=charisma):
  drafts edicts/rescripts, generates political influence. Office modifier =
  `monthly_political_influence_modifier`.
- **Imperial Guard — 領侍衛內大臣 Grand Commandant** (key=`guard_commandant`, skill=martial):
  commands the palace guard, guards the emperor's PERSON. Buff = Guard vitality; power-base
  reconciled onto the emperor in `QING_council_recompute`.
- **Chamberlain rename:** Household Grand Secretary → **Grand Chamberlain of the Imperial
  Household** (內務府, key renamed `grand_secretary` → `chamberlain`). BEHAVIOURAL-CHANGE:
  existing office renamed, not new — flagged for behavioural-equivalence scrutiny in review.
- **Office events:** `qing_secretariat.1/.2/.3` (Edict Mill / Rescript Backlog / Drafting
  Scandal) + `qing_guard.1/.2/.3` (Guard Reviewed / Plot Against Throne / Overmighty
  Commandant — the praetorian/Oboi problem). Each gated on its office being filled by a
  living holder in ROOT's service; fired from `QING_frontier_flavour_roll` (se_QING_DECLINE).
- **Appoint verbs:** `qing_gov_office_appoint_grand_secretariat` + `_guard_commandant`
  (scope=character, CHI+employer shown, cost 15 political influence, calls `QING_office_appoint`).
- **Accountability:** grand_secretariat OWNS the influence metric (`QING_acc_metric_influence`:
  PI<20 fail / ≥80 thrive); guard_commandant OWNS the civil-war metric
  (`QING_acc_metric_civil_war`: civil war or disloyal-powerful char = fail).
- **Displaced/vacated-holder cleanup:** censorate-oversight (minor+major) buff strips added at
  BOTH appoint-displacement (~910) and vacate (~971) cleanup sites in se_QING_COUNCIL.txt, so a
  relieved officer leaves clean.

### Localization
- `qing_governance_l_english.yml`: chamberlain rename, 2 new office name/desc pairs, card
  titles, MOD one-liners, appoint-button + tooltip loc; Empress seat loc (QING_GC_EMPRESS +
  _VACANT); "eleven appointable" → "thirteen" in SEATS_TT + TITLES_UNASSIGNED_TT.
- `qing_dynasty_l_english.yml`: appended qing_dynasty.6/.7/.8 (title/desc/2×option+tt).
- NEW `qing_secretariat_l_english.yml` + `qing_guard_l_english.yml`: full loc for the 6 office
  events (BOM + `l_english:` header, matching house style).

### GUI (DONE)
- **`government_view.gui`:**
  - Chamberlain card: fixed stale loc keys (`QING_GC_OFFICE_GRAND_SECRETARY` →
    `_CHAMBERLAIN`, `QING_GC_MOD_GRAND_SECRETARY` → `_CHAMBERLAIN`) left over from the rename.
  - Office grid 10 → 12: added `grand_secretariat` (oratory icon, GetCharisma, refresh_charisma)
    and `guard_commandant` (military icon, GetMartial, refresh_martial) cards to OFFICES row 3,
    templated exactly from the zongli card so alignment/statesmanship-bar/appoint idiom match.
  - **Throne row** (was Emperor | Crown Prince | Regent): Regent box REPLACED by an **Empress**
    box (templated from the Crown Prince box incl. the #270 favour square; datacontext
    `qing_office_empress_holder`, loc QING_GC_EMPRESS/_VACANT). Throne row is now
    Emperor | Crown Prince | Empress.
  - **Regent + Emeritus relocated** into a right-hand vertical column beside the Grand
    Chancellor card (horizontal wrapper: Chancellor card | {Regent, Emeritus}). Regent box
    widened 312→470 to fill the column. Emeritus block moved up out of its old
    below-the-grid position (its IsSet visibility gate preserved, so it still only shows when
    a 太上皇 exists). This declutters the throne row and groups the "power behind the throne"
    seats with the Chancellor.
- **`imp19c_windows.gui`:** added the two per-office Appoint buttons (grand_secretariat,
  guard_commandant) to the shared picker window, keyed on `qing_gc_picker_office`, templated
  from the zongli button; tooltips QING_GOV_OFFICE_GRAND_SECRETARIAT_BTN_TT /
  _GUARD_COMMANDANT_BTN_TT (both confirmed present in loc).
- Both GUI files brace-balanced (delta 0) after edits.

### Still pending for #272/#273
- SESSION_REPORT.md entries (fix-traceability; behavioural-CHANGE note for the Chamberlain
  rename + reworked War/Censorate office modifiers).
- Post-implementation code review, then ONE combined develop commit as freekumquats.
