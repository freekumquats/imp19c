# Law Expansion — Full Design (all remaining law groups)

> ## ADVERSARIAL REVIEW PASS (2026-07-24) — applied fixes
> Four adversarial reviewers (classification / boot-crash / GUI-loc-modkeys / gameplay-balance) audited this
> doc against live code. **Classification core verified CORRECT** (every backing-var class, line citation,
> no-op default, and the signed-clamp warning confirmed). **Zero boot-crash risks.** The fixes below address
> exploits, incoherence, and specification gaps they surfaced. Empirically confirmed: EVERY existing law's
> on_enact uses `set_variable`/modifier (idempotent) — none nudge — so a nudge-on-enact IS a toggle-farm.
>
> **SHIP-BLOCKER fixes (applied to the sections below):**
> - **Toggle-farm exploit (#13, #44, #47):** `on_enact` fires on EVERY enact, so any on_enact that NUDGES a
>   var is farmable by re-enacting. FIX: all three drop the on_enact nudge. #13/#47 become pure
>   modifier-swap; #44's "kickstart" nudge is once-guarded (`if NOT has_variable qing_X_adopted { nudge; set
>   adopted }`) so it fires at most once ever.
> - **Ratchet-defeating exposure (#19, #20, #44):** exposing drift-from-play decline meters as a standing
>   policy that CANCELS the pressure defeats the mechanic. FIX: #19/#20 biases are made SMALL and band-gated
>   (tilt, not cancel — a −1 audit bias against a meter nudged +N from many sources only slows accrual, and
>   is floored so it can't drive the meter to 0); #44 becomes a pure modifier-law (no ongoing var-write).
> - **#38 eunuch law shipped before its consumer:** REMOVED from the law batches — #37/#38 live ONLY in the
>   court-intrigue subsystem batches (6/7), law + backing mechanic in the same batch.
>
> **INCOHERENCE fixes (applied):**
> - **Monetary triple-overlap** (#23 + vanilla currency_law + #48/49): #23 is GATED distinct from the vanilla
>   `currency_law` debasement (Qing-specific `qing_currency_stress` bias only, no commerce/tax modifier that
>   would double vanilla's); PART D #48/49 stay ROW-scoped (see below). Documented as orthogonal, not additive.
> - **Military triple-stack** (P7 + #14 + #15): #14 (勇營 regional) and #15 (新軍 central) are made ORTHOGONAL —
>   #15's modernarmy bias must NOT subtract from #14's han-provincial target (the two levers were canceling).
>   Verify the `se_QING_DECLINE.txt` han-provincial target formula and keep them independent.
> - **#30 tariff fake-choice:** re-specified to WRITE a stance var `qing_tariff_stance` the trade pulse reads
>   as `min(treaty_autonomy, stance)`, so the law has bite under a treaty (was a pure modifier the treaty
>   overrode). If that read can't be added cheaply, DEFER #30 rather than ship a fake choice.
> - **1:1 validator on new seats (chief eunuch #B3, dowager #A6):** the doc's "doesn't set qing_office_held"
>   claim contradicted the regent precedent (which DOES). RESOLUTION CHOSEN: separate seat-marker
>   (`qing_seat_chief_eunuch` / `qing_seat_dowager`), NOT counted by `QING_validate_one_position`; the
>   `qing_office_<key>_holder` country var is display-only (like emperor/empress seats). See court doc.
>
> **BATCH-1 SCOPE additions (now explicit):** enumerate ~270 loc keys for the new groups; author the 7 domain
> header loc keys (`qing_statutes_governance`…`qing_statutes_foreign`, see PART A — the single 統治大典 header is
> RETIRED, laws split into 7 domain columns); verify 7-column horizontal fit in the 970px scrollarea (or
> wrap); author an explicit OLD→NEW re-filing map for the 13 existing entries (avoid duplicate/vanish);
> replace `omen_power` (#51, means MINING in this TC) with `monthly_legitimacy`/a religion modifier;
> isolation-test #31's on_enact→scripted_effect (else inline the 3-line lever body).
>
> **BALANCE tuning (deferred to testing, noted per element):** eunuch triple-penalty doom-loop (cap the
> corruption feedback, decouple one output, add a non-event purge lever); harem passive promote/demote must
> skip player-acted consorts (2-yr `qing_consort_recently_acted` flag) and the dowager event is ADVISORY not
> forced; harem favour drift must NOT restore to rank×20 (kills squabbling) — make favour a pure accumulator
> the player/events move. See court doc for these.

> ## 1763-LIVENESS + CONCRETENESS REVIEW (2026-07-24) — the hard gate
> Trigger: the tariff law was tied to a var (`qing_tariff_autonomy`) only set by post-1842 treaty events, so
> it was DEAD at a 1763 start. Two adversarial reviewers then audited EVERY pending law against: **(1) is the
> backing mechanic LIVE at a 1763 start (not frozen until a later date / post-1842 event / an office that
> doesn't exist yet)? (2) is it CONCRETE (moving it produces a visible in-game effect, not just an abstract
> counter)?** A third pass audits the 13 already-shipped laws (running). Verdicts:
>
> **DORMANT-AT-1763 — dead for decades; DEFER to a future "late-Qing laws" pass OR re-base on a 1763-live
> mechanic:**
> - **#15 Army Modernization 新軍** — `qing_modernarmy_share`=0, target=`qing_selfstr_progress`=0 → NO drift
>   until Self-Strengthening (post-1842). `se_QING_DECLINE.txt:94/380`.
> - **#27 Customs Regime 海關** — Maritime Customs Service doesn't EXIST until an establish event (~1854);
>   pulse gated on `qing_customs_established`. `se_QING_CUSTOMS.txt:47/60`.
> - **#44 Modernization Doctrine 自強** — same `qing_selfstr_progress`=0 frozen until post-1842.
> - **#18 Great-Power Alignment** — `qing_gp_tension_*` drift GATED `current_date >= 1793.1.1`
>   (`se_QING_GREATGAME.txt:51-54`) → frozen the first 30 years.
> - **#17 Overseas Education 留學** — `qing_students_abroad`=0 until the mission launches (historical 1872).
>   Anachronistic at 1763. `se_QING_STUDENTS.txt:46/56`.
> - **#42 National Integration** — `qing_civic_identity` target derives from `qing_selfstr_progress`=0
>   → frozen. `se_QING_DECLINE.txt:830`. (Also: nationalism/civic-nation is a 19c construct.)
> - **#33 Foreign-Office Doctrine 總理衙門** — the Zongli Yamen was FOUNDED 1861; the office doesn't exist at
>   1763. `se_QING_LEGATIONS.txt:9`. ANACHRONISTIC.
>
> **HALF-DORMANT — one component dead at 1763:**
> - **#28 Missionary Policy** — the SOCIAL friction target is live at 1763, but the POLITICAL (`qing_antichr_target`)
>   only drifts post-treaty (`se_QING_MISSIONARY.txt:242`, gated `has_variable = qing_treaty_system_imposed`).
>   FIX: the 1763 law biases ONLY the live social-friction target; the political side is a post-treaty add-on.
>
> **LIVE-BUT-ABSTRACT / WEAK — works but the player sees little:**
> - **#23 Currency Stress** — moves via events at 1763 but only feeds `reform_pressure` (abstract → abstract);
>   no treasury/commerce/pop effect. FIX: give it a concrete effect (a treasury or commerce modifier band) or
>   fold into vanilla currency_law rather than ship an invisible number.
> - **#14 Provincial Militarization 勇營** — `qing_han_provincial_power` starts 0, drifts toward target 15 →
>   ~2 years to cross the first band. FIX: seed a nonzero 1763 baseline OR accept the slow ramp (design intent).
>
> ### RE-BASE PLAN (2026-07-24, verified) — the 7 dormant laws onto 1763-live concrete hooks
> Research found a distinct, 1763-live, non-duplicative concrete anchor for 5; 2 have NO clean 1763 analogue.
> - **#15 Army Modernization → "Drill / Military-Reform Posture".** Re-based onto the LIVE banner/green-standard
>   decay via a SHARED drill bias (neglect +1 both / adequate 0 / reform-drills −2 both), distinct from P7 which
>   biases Banner vs Green-Standard SEPARATELY (funding split). Orthogonal: funding (P7) × drill-intensity
>   (this). `se_QING_DECLINE.txt:81-85/877-921`. **NB — pairs with the P7 fix:** both must apply during the
>   High-Qing era (currently the whole decay block is suppressed by `qing_high_qing_era` until ~1772), else both
>   are dead at 1763. Fix = let a small drill/upkeep bias act even in the golden-age era.
> - **#17 Overseas Education → "Inner-Court Scholarship (南書房/上書房)".** Re-themed onto the LIVE Southern Study
>   corps (`se_QING_SOUTHERNSTUDY.txt`): recruitment intensity / literary-depth (neglect / patronage / intensive
>   cultivation → wildcard-recruit rate + literary ceiling → legitimacy/prestige). Distinct from #12 exam cadence
>   (triennial cycle). Concrete: mints real attendant characters + `qing_southernstudy_luster` modifier.
> - **#18 Great-Power Alignment → "Canton Trade-Supervision Posture (粵海關監督)".** Re-based onto the LIVE
>   `qing_hoppo_squeeze` drift (`se_QING_CANTON.txt:58/146-163`): lax +3/qtr (revenue bleeds to graft → feeds
>   corruption) / moderate +1 / strict-audit −1 (Hoppo accountable → Canton yield rises). Distinct from #6
>   (open/closed) and #7 (purse split) — orthogonal supervision axis. Concrete: feeds treasury + corruption +
>   Cohong-debt events.
> - **#33 Foreign-Office Doctrine → "Frontier-Diplomacy Doctrine (理藩院)".** Re-themed onto the LIVE Lifan Yuan
>   Amban coverage target (`se_QING_MINISTRY.txt:257-386`): minimal / adequate / intensive Amban staffing →
>   `qing_min_perf_lifanyuan` + real Amban characters posted to frontier subjects. The 1763 institutional
>   ancestor of the 1861 Zongli Yamen. Distinct from #39 (tribute cadence) and #26 (Xinjiang control).
> - **#42 National Integration → KEEP STANDALONE + FOCUS ON THE NATIONALISM MECHANIC [USER 2026-07-24].**
>   (Research recommended merge into #8; user chose standalone.) The law should drive the PART IV NATIONALISM
>   layer (Design 4 / P1) — `qing_national_awakening` modifier, the culture→nationalism concept, citizenship
>   decisions, `qing_civic_identity` + settle-bonus — NOT just ethnic-stance. Verifier to map the actual
>   nationalism vars/hooks (see PART IV in overnight_designs.md, se_QING_SETTLE_FRONTIER, the nationalism concept
>   layer) and specify the concrete 1763-live backing the law biases. This differentiates it cleanly from #8
>   ethnic-governance (dyarchy/banner/han stance): #42 is the NATION-BUILDING / citizenship axis. `qing_civic_identity` is NOT frozen — it
>   rises at 1763 via the Design-4 `qing_civic_identity_settle_bonus` (+8/arc, `se_QING_DECLINE.txt:856`,
>   `se_QING_SETTLE_FRONTIER`). A law could bias the accrual rate (+5/+8/+12 per arc), but that's a second-order
>   multiplier on a meter that mostly waits for arcs. **RECOMMEND: merge into #8 ethnic-governance as a 4th
>   "unified imperial citizenry" stance** that lifts both dyarchy AND the settle-bonus, rather than a third
>   standalone knob. (Or drop — #8 + settlement missions already regulate this well.)
> - **#27 Customs Regime → BUILD 1763-RELEVANT, FOCUS ON THE UPSTREAM (BASE-GAME) TRADE SYSTEM
>   [USER 2026-07-24 — override of DROP].** The clean separation: #27 governs ORDINARY empire-wide trade — the
>   vanilla/upstream engine trade mechanic (trade routes, commerce, `global_commerce_modifier` /
>   `global_capital_trade_routes` / trade-route count / commerce income) — IN CONTRAST WITH the bespoke special
>   trade systems, which stay their own laws: Canton 粵海關 (#6/#7/#18) and the caravan 定稅則 (#4). So #27 is a
>   general TARIFF/COMMERCE-REGULATION law on the base trade system (e.g. free-trade / regulated / protectionist
>   stances, each a modifier on commerce + trade routes + tax), NOT a fourth Canton knob and NOT the 1854 Hart
>   inspectorate. Researcher to confirm the upstream trade modifiers/vars live for CHI at 1763 (the engine trade
>   system is on — see currency/trade svalues) and specify the concrete backing. Distinct from #30 tariff (which
>   the redesign put on Canton real-goods) — reconcile: #30 taxes the Canton export base specifically; #27 sets
>   the empire-wide commercial-trade regime. If they overlap too much, MERGE #27+#30 into one "Trade & Tariff
>   Regime" law spanning base trade + Canton. Verifier to make that call.
> - **#44 Modernization Doctrine → BUILD 1763-RELEVANT, FOCUS ON TECHNOLOGY + NEW UNITS + MODIFIERS
>   [USER 2026-07-24 — override of DROP].** NOT the High-Qing-era-timing angle. The law drives a MODERNIZATION
>   posture whose stances grant concrete, 1763-applicable effects: research/technology modifiers (military_tech
>   / civic_tech investment, research_points), access to NEW/upgraded UNIT types (e.g. drilled/firearm units,
>   artillery — via unlock or a recruitment modifier), and standing country MODIFIERS (discipline, morale,
>   research, cost). All of these are engine-level and LIVE at 1763 (tech + units + modifiers exist from game
>   start — no self-strengthening meter needed). Conservative / balanced / aggressive-modernization stances,
>   each a modifier-swap (+ optional unit unlock). The post-1842 `qing_selfstr_progress` bands remain a LATER
>   layer. Verifier/researcher to confirm the exact engine tech/unit/modifier keys available at 1763 (military_
>   experience, discipline, land_morale_modifier, research modifiers, unit unlock idioms). Distinct from #17
>   (court scholarship = legitimacy/prestige) — #44 is the MILITARY/technological modernization axis.
>
> ### RE-BASE VERIFICATION (2026-07-24) — 4 of 5 REFUTED. The re-bases mostly DON'T hold as proposed.
> An adversarial verifier read the actual code against each re-base claim. Result: **1 SOUND, 4 BROKEN.** The
> recurring reason: these bespoke systems expose NO settable law knob — the value is recomputed from a roster or
> the drift is a hardcoded literal, so a law can't bias it without ADDING new plumbing (a bias var + a read at
> the site = net-new-lite, real code, not a free re-base).
> - **#15 Drill Posture — BROKEN.** Still dead at 1763: the decay block (incl. the bias read) is inside the
>   `qing_high_qing_era` guard (`se_QING_DECLINE.txt:893-921`), suppressed until ~1772 — same flaw as P7. AND it
>   writes the SAME two vars as P7 (`qing_banner/greenstandard_upkeep_bias`) → last-writer-wins collision. Fix
>   requires: (a) let a small bias act during the High-Qing era, (b) give #15 its OWN drill var distinct from
>   P7's funding bias. Real plumbing.
> - **#17 Southern Study — BROKEN.** `qing_southernstudy_count`/`_literary` are RECOMPUTED from the character
>   roster (`QING_southernstudy_recompute_roster`); recruitment is player-invoked. No settable
>   intensity/depth-target var to bias. Would need a NEW recruit-rate input the pulse reads.
> - **#18 Canton Hoppo Supervision — BROKEN.** The `qing_hoppo_squeeze` drift amounts (+3 vacant / +1 held) are
>   HARDCODED literals (`se_QING_CANTON.txt:146-154`), not read from a bias var. Would need a NEW drift-bias
>   input at the nudge site.
> - **#33 Frontier Diplomacy (Lifan Yuan) — BROKEN.** No `qing_amban_estab_target` exists; the amban staffer
>   seeds/​refills but reads no law-settable ceiling. This also confused #33 (Zongli doctrine, post-1861) with
>   #43 (Amban Establishment, already flagged NET-NEW). Would need the NET-NEW amban-target plumbing (= #43).
> - **#42 National Integration — SOUND.** `qing_civic_identity_settle_bonus` is a real 1763-live input read into
>   the civic-identity drift TARGET (`se_QING_DECLINE.txt:853-858`, guarded); a law can bias the +8/arc accrual
>   via a one-line multiplier at `se_QING_SETTLE_FRONTIER.txt:125`. (User also wants this focused on the broader
>   nationalism layer — hook mapping pending.)
>
> ### CONCRETE HOOKS for #27 / #44 / #42 (2026-07-24 researcher, verified file:line)
> - **#27 Customs Regime → the researcher recommends MERGE with #30**, NOT a standalone. Reason: no distinct
>   1763 maritime-customs dimension exists — Canton owns open/closed (#6), purse (#7), Hoppo (#18-attempt), and
>   its yield already reads real goods. BUT the USER's later steer was DIFFERENT: #27 should govern the UPSTREAM
>   base-game trade system (commerce/trade-routes), explicitly IN CONTRAST with the bespoke Canton/caravan
>   systems. So #27 is NOT a Canton knob at all — it's a modifier law on the vanilla engine trade
>   (`global_commerce_modifier`, `global_capital_trade_routes`, trade-route count), free-trade/regulated/
>   protectionist. That is genuinely distinct from #30 (Canton export tax) and from Canton/caravan. KEEP
>   separate per user; the researcher's merge suggestion is noted but overridden by the user's contrast framing.
>   (Confirm the upstream trade modifiers are live for CHI at 1763 — they are engine-level, so yes.)
> - **#44 Modernization Doctrine → USER STEER = TECH + NEW UNITS + MODIFIERS**, not the researcher's High-Qing-
>   era-timing angle. So the backing is ENGINE-LEVEL and 1763-live by construction: research modifiers
>   (military/civic tech investment, `research_points_modifier`), unit access (drilled/firearm/artillery via
>   unlock or recruitment modifier), and standing modifiers (`discipline`, `land_morale_modifier`, cost).
>   Conservative/balanced/aggressive stances = modifier-swaps (+ optional unit unlock). No qing_selfstr meter, no
>   era-timing. Distinct from #17 (scholarship=legitimacy) — #44 is the military-tech axis. Confirm exact engine
>   keys at build.
> - **#42 National Integration → SOUND hook confirmed.** Backing = the `qing_civic_identity` drift TARGET at
>   `se_QING_DECLINE.txt:857` (where `qing_civic_identity_settle_bonus` is already read+added). Law sets
>   `qing_civic_law_bias` added at the same site (lifts the TARGET, persists — ratchet-safe). Bands at
>   DECLINE:318-338; feeds the citizenship-assimilation bridge (≥50) + ethnic-tension relief. NOTE: the var is
>   `qing_civic_identity` — there is NO `qing_national_awakening` VAR (it is a P1 capstone MODIFIER + descriptive
>   only). User wants the law focused on this nationalism/citizenship layer → this hook IS that layer. Distinct
>   from #8 (governance stance) — #42 is the nation-building doctrine. dynastic/shared-institutions/federalism.
>
> ### FINAL DISPOSITION [USER 2026-07-24]
> - **The 4 refuted re-bases → BUILD AS NET-NEW-LITE (Batch 4).** #15 Drill (own var distinct from P7 + fix the
>   High-Qing era guard so a small bias acts pre-1772), #17 Southern-Study (new recruit-rate input the pulse
>   reads), #18 Canton-supervision (new Hoppo drift-bias var at the nudge site), #33 Amban (= build the #43
>   net-new amban-target). Each = one bias/target var + one guarded read added at the recompute/drift site.
> - **#27 KEPT SEPARATE on the upstream base-game trade system** (commerce/trade-routes modifier law:
>   free-trade / regulated / protectionist), distinct from #30 Canton export tariff and from Canton/caravan.
>   NOT merged.
> - **P7 fix:** the existing military_upkeep law's bias must also act during the High-Qing era (currently dead
>   until ~1772). Bundled with #15 (same era-guard site, `se_QING_DECLINE.txt:893-921`).
>
> **HONEST REALITY:** "re-base" undersold the work. 4 of the 5 need NET-NEW plumbing (a bias var + a read at a
> recompute/drift site, plus #15's era-guard fix) — the same class of work as the net-new-lite laws, not a free
> retarget. They are all still BUILDABLE, but each is a small code task, not a design relabel. Pending: the
> second researcher's concrete hooks for #27 (upstream trade), #44 (tech/units/modifiers), #42 (nationalism).
>
> **NET after re-base:** 5 of 7 salvaged as distinct 1763-live laws (#15 drill, #17 scholarship, #18 Canton
> supervision, #33 Lifan Yuan); #42 merges into #8; #27 and #44 dropped from the 1763 pass (re-authorable later
> in a reform-era bucket driving their real post-1842 meters). Plus the P7 shipped-law High-Qing-era fix.

> **CARAVAN real-goods fix (#4 shipped law + affects any frontier-trade tariff):** the caravan customs income
> is `qing_caravan_prosperity × rate / 40` — an ABSTRACT prosperity meter, not real trade. Per user: this is an
> IMPLEMENTATION FAILURE — caravan revenue should read REAL Central-Asian goods traded (mirror Canton's
> `GOODS_national_production_*` sum, `se_QING_CANTON.txt:93-102`), using whatever the Xinjiang/frontier
> provinces actually produce at 1763 (tea/rhubarb/horses/jade/cotton — pending the shipped-law audit). Tracked
> as a caravan-income rework, separate from the caravan LAW (which just sets the rate).
>
> **CLEARED as LIVE+CONCRETE at 1763 (pending):** #5 salt, #6 canton regime, #7 canton purse, #13 industrial
> (modifier), #22 deliberative, #24 council composition, #25 canal quota, #26 xinjiang admin, #30 tariff
> (REDESIGNED onto Canton real-goods), #39 tributary ritual, #46 censorate, #47 works.
>
> ## SHIPPED-LAW AUDIT (2026-07-24) — the 13 already-live groups, same bar
> 11 of 13 PASS as LIVE+CONCRETE at 1763 (penal, ritual, opium, salt, canton regime, ethnic gov, office-selling,
> exam cadence, ministry estab, advisory estab, canton purse). Problems found:
> - **P7 `qing_military_upkeep_law` — DORMANT AT 1763 (the exemplar was dead).** The banner/green-standard
>   decay it biases is suppressed by the `qing_high_qing_era` flag until ~1772 (`se_QING_DECLINE.txt:896` guard
>   `NOT has_variable qing_high_qing_era`; flag set at :64 for `current_date < 1772`). The bias read at :919-920
>   sits INSIDE that failed guard → the law does nothing at a 1763 start until the High-Qing era ends. **FIX:
>   either apply a small upkeep bias even during the High-Qing era (a golden-age army still drills/neglects), or
>   re-theme the law to a 1763-live military-quality knob** (ties into the #15 re-base — see research). This is
>   the same 1763-dead failure as the tariff; it shipped in P7 because the era-gate wasn't checked.
> - **#4 caravan customs — LIVE-BUT-ABSTRACT base** (confirmed): income = `qing_caravan_prosperity × rate/40`,
>   and prosperity is computed from grip/investment/flags, NOT real goods (`se_QING_CARAVAN.txt:85-130`), unlike
>   Canton's real-goods sum. CARAVAN REWORK (approved). **Goods reality check:** only `tea` and `silk` have
>   `GOODS_national_production_*` aggregates; horses/jade/cotton/rhubarb/dried-fruit do NOT. So the rework reads
>   real frontier tea/silk production (the westbound Qing exports the loc documents) as the caravan base, ×rate
>   — mirroring Canton — rather than inventing new goods types. Abstract prosperity can stay as a secondary
>   multiplier (grip/route-security), but the BASE becomes real goods.
> - **Reform-gated options (INTENDED) — but the TOOLTIP must say so [USER 2026-07-24]:** the
>   `revised`/`pragmatic`/`reformed` options of penal (#1), ritual (#2), salt (#5) are locked behind
>   `qing_reform_track_unlocked` (reform pressure ≥50). The GROUPS are live; these are deliberate mid-game
>   unlocks. **ACTION — GENERAL BUILD RULE: any law option with an `allow`/`potential` gate or prerequisite MUST
>   have its hover text (the option `_desc` loc) explicitly CALL OUT the gate** — e.g. "#R Requires: the reform
>   track opened (reform pressure ≥ 50)#!". Applies to EVERY gated option across ALL laws (reform-track,
>   is_republic, has_law=X, era flags, tariff-autonomy caps, …) AND to the existing 13 (audit their gated-option
>   descs, add the callout where missing) so the player always knows WHY an option is greyed.
>
> **DISPOSITION (USER DECISION 2026-07-24): RE-BASE each of the 7 dormant/anachronistic laws
> (#15/#17/#18/#27/#33/#42/#44) onto a 1763-LIVE concrete mechanic** (not defer). Constraint: each re-base must
> drive a mechanic that (a) is operative at 1763 AND (b) does NOT merely duplicate an already-cleared law
> (ethnic governance #8, exam cadence #12, canton regime #6, canton purse #7, assimilation #41, tributary
> ritual #39, tariff/Canton #30). Candidate re-bases pending research (see below); any law with NO clean 1763
> analogue (the Zongli Yamen #33 is founded 1861) is flagged for an honest call — re-theme to its 1763
> institutional ancestor (理藩院 Lifan Yuan / 粵海關 / tributary-Board-of-Rites frame) or drop. The
> post-1842 SUPERSTRUCTURE of each (Self-Strengthening bands, treaty-era customs, Zongli Yamen) can still layer
> on later — but the LAW must bite at 1763. **CARAVAN real-goods rework: APPROVED** (see caravan task).

**Goal:** finish the law-group build-out. Design 2 shipped 13 Qing law groups (P7's
`qing_military_upkeep_law` was the last). This doc designs **every remaining candidate** from the
§A–H catalogue in `overnight_designs.md:219–316`, PLUS the four **upstream Victorian-TC stubs**
(Upper House ×2, Monetary Policy ×2) that ship with empty `modifier = {}` on every option.

Each law is designed against **verified backing-var ground truth** (three fan-out audits, line-cited
below). The single hard rule that governs correctness:

> **A law may only WRITE a var the pulse READS. It may NOT write a var the pulse itself
> COMPUTES/nudges** — doing so makes the law fight the recompute (the documented `qing_censorate_vigor`
> exclusion). The four safe patterns:
> - **SELECTOR (a):** law `set_variable`s a value/flag the pulse reads as-is. Trivial + safe.
> - **MODIFIER-SWAP:** option carries a `modifier = {}` block only (no var). Trivial + safe.
> - **BIAS-A (accumulator):** law sets a standing bias var; the pulse adds it at its existing
>   `QING_DECLINE_nudge`/`change_variable` site (one guarded line). This is the P7 pattern.
> - **BIAS-B (recomputed target):** law sets a bias var threaded INTO the pulse's `set_variable`
>   formula (one guarded `change_variable` term before the clamp). Slightly higher risk (touches a
>   recompute).
> - **MODIFIER-LAW (event/treaty state):** no var-write; the option is a pure standing
>   `modifier = {}`. Used where the backing var is set only by discrete events/treaties.

Every Qing group gets `potential = { tag = CHI }`, a no-op default option (byte-identical to today),
loc, and a `laws_widget` entry in `government_view.gui` (see §GUI). Every bias var is read **guarded**
(`has_variable`) at the pulse site so the default is a true no-op.

---

## PART A — GUI capacity (blocking constraint for the whole build)

`government_view.gui` does **not** auto-enumerate law groups — each is hand-listed as a `laws_widget`
inside a `laws_widget_area` column (lines 2258–2304 hold the current 13 in one column). Vanilla splits
its ~50 laws across ~9 area columns. **Adding ~30 more Qing laws to one column overflows the panel.**

**Design [USER 2026-07-24 — the single "Statutes 統治大典" header is RETIRED]:** ~40 laws under one header is
too many; split into **7 domain sub-headers**, each its OWN `laws_widget_area` column, mirroring vanilla's
Economic/Military/Social/Constitutional split. FINALIZED categories (each gets a header loc key; the historical
Chinese header is the display title). This list is CORRECTED to the post-review surviving set (dropped
laws removed; re-themed laws under their new names):

1. **`qing_statutes_governance` · 治道 Governance & Council** — ethnic_governance, office_selling,
   ministry_estab, advisory_estab, council_composition, deliberative_governance
2. **`qing_statutes_fiscal` · 財政 Fiscal & Trade** — salt_admin, canton_regime, canton_purse,
   caravan_customs, canal_quota, monetary_response, tariff_regime (關稅, Canton real-goods),
   customs_regime (upstream base-game trade), + upstream stubs monetary_policy / monetary_setting
3. **`qing_statutes_military` · 武備 Military** — military_upkeep (P7), drill_posture, modernization_doctrine
   (tech/units/modifiers)
4. **`qing_statutes_frontier` · 邊疆 Frontier & Subjects** — xinjiang_admin, tributary_ritual,
   frontier_settlement, assimilation_doctrine, national_integration (nationalism/citizenship), amban_estab,
   frontier_trade_sovereignty
5. **`qing_statutes_court` · 宮廷 Court & Succession** — succession_method, regency_rules,
   princely_establishment (+ harem_establishment / eunuch_policy from Batches 6/7 when built)
6. **`qing_statutes_culture` · 文教 Culture, Justice & Learning** — penal_code, ritual_orthodoxy,
   opium_policy, exam_cadence, exam_curriculum, cultural_patronage, inner_court_scholarship (南書房),
   censorate_empowerment, missionary_policy, works_priority
7. **`qing_statutes_foreign` · 通商洋務 Foreign Affairs & Enterprise** — overseas_expansion,
   frontier_diplomacy (理藩院 Lifan Yuan), industrial_encouragement

Each column carries ~4–8 laws; no header holds the whole set. (The 4 upstream Upper-House / Monetary stubs
keep their EXISTING vanilla area registration — they are not Qing-statute laws — except the two monetary ones
which fit naturally beside 財政; leave them where the vanilla GUI already lists them unless re-filing is
trivial.)

**Task (Batch-1 FIRST, prerequisite for ANY new law being visible):** author the 7 `laws_widget_area` blocks
(replace the single current Qing area at government_view.gui:2258-2304), re-file the 13 existing entries into
their new home column per an EXPLICIT old→new map, add the new entries, author 7 header loc keys
(`qing_statutes_governance` … `qing_statutes_foreign`). Verify the 7 columns fit/wrap in the 970px scrollarea.

---

## PART B — Qing law groups by classification

Legend for each entry: **[CLASS]** · backing var · **PATTERN** · risk. Options are `default (no-op) /
stance / stance`. "Pulse site" = the exact line where BIAS is applied.

### B1. SELECTOR / MODIFIER-SWAP — trivial, safe (build first)

**1. Penal Code Regime 大清律例** — *already shipped* (`qing_penal_code_law`). Modifier-swap.
**2. Ritual Orthodoxy 禮部** — *already shipped* (`qing_ritual_orthodoxy_law`). Modifier-swap.
**3. Opium / 4. Caravan / 5. Salt / 6. Canton regime / 7. Canton purse / 8. Ethnic gov / 9. Office-selling
/ 10. Ministry estab / 11. Advisory estab / 12. Exam cadence** — *already shipped.*

**13. Industrial Encouragement 官辦 / 官督商辦 / 商辦** — [MODIFIER-SWAP + NET-NEW-lite selector]
- Backing: modifier targets EXIST (`qing_earlyindus_*`, `qing_selfstr_guandu_tension`
  `se_QING_SELFSTR.txt:421`), but no numeric tri-state selector var.
- **Design:** pure **modifier-swap** law — 3 options each carrying a `modifier = {}` expressing the
  school's trade-off (官辦 state-run: +research, +cost, −commerce; 官督商辦 merchant-supervised: balanced,
  small guandu-tension; 商辦 merchant-run: +commerce, +middle-strata output, −state control). NO var.
  Do NOT invent a selector var (nothing reads it). **[REVIEW FIX] NO on_enact nudge** — the earlier "optionally
  nudge qing_selfstr_progress" is a TOGGLE-FARM (on_enact fires every enact → re-enact to farm the nudge).
  Pure modifier-swap only; the state-run school's modernization edge is expressed as a research modifier, not a
  var nudge. Risk: low.

### B2. BIAS-A — accumulators (P7 pattern: one guarded nudge line)

**14. Provincial Militarization 勇營** — [ACCUMULATOR] `qing_han_provincial_power` (nudged ±2,
`se_QING_DECLINE.txt:426`). Law sets `qing_provmil_bias` ∈ {centralized −1 / sanctioned 0 / delegated +1};
pulse adds it guarded at the :426 nudge. Modifiers: delegated = +manpower/−central control; centralized =
inverse. **CAVEAT:** design note says these are "arguably better AI/event-driven" — still viable; a law is
the player's explicit lever over the 湘軍/淮軍 delegation. Risk: low.

**15. Army Modernization Mandate 新軍** — [ACCUMULATOR] `qing_modernarmy_share` (nudged ±2,
`se_QING_DECLINE.txt:390`). Law sets `qing_modernarmy_bias` ∈ {traditional −1 / mixed 0 / new-army +1}; pulse
adds guarded. Modifiers express drill/discipline vs. banner-conservatism prestige cost. Risk: low.

**16. Cultural Patronage 文治** — [ACCUMULATOR] `qing_wenzhi_patronage` (init 40, −1/qtr drift
`se_QING_WENZHI.txt:75`). Law sets `qing_wenzhi_bias` ∈ {austere +? / standard 0 / lavish −?} added at :75
so lavish offsets the decay (net 0 or positive) and austere quickens it. **Ratchet-rule caution:** lavish
must be a *bias at the drift site*, NOT a positive free nudge — the band-gate + the existing −1 base keeps
it bounded. Modifiers: lavish = +prestige/−treasury; austere = inverse. Risk: low.

**17. Overseas Education 留學** — [ACCUMULATOR + flag] `qing_students_abroad` (nudged, `se_QING_STUDENTS.txt:92`).
Law sets `qing_students_bias` ∈ {none / limited / large}; adds to the recurring +20 abroad nudge (large
accelerates, none zeroes the recurring gain via a negative bias floored at 0). Also modifier: large =
+research/−conservative-happiness. **Interaction:** the students mission-active flag is event-owned; the law
biases the *rate*, not the flag. Risk: low.

**18. Great-Power Alignment** — [ACCUMULATOR ×3] `qing_gp_tension_britain/france/russia`
(`se_QING_GREATGAME.txt:79-110`). Law sets `qing_gp_alignment_bias` ∈ {isolation / balance / align};
applied as a standing per-power tension nudge (isolation = +tension all; align = −tension toward the aligned
power, event-picked). **CAVEAT:** "align-with-one" needs a target — model as balance (symmetric −) vs.
isolation (symmetric +); a specific alignment stays event-driven. Risk: low-moderate (3 nudge sites).

**19. Anti-Corruption Stance** — [ACCUMULATOR] `qing_corruption_level` (init 12, nudged many).
**[REVIEW FIX — ratchet-defeat guard]** Build as opt-in, but the bias must TILT not CANCEL: corruption is
nudged +N from 15+ sources, so a standing −1 (audits) / −2 (draconian) only SLOWS accrual — and the applied
bias must be FLOORED so the law alone can never drive the meter toward 0 (e.g. apply the negative bias only
while `qing_corruption_level > 20`, so it thins graft but never legislates a spotless court). Modifier cost
(−admin-efficiency / +stability / −upper-strata happiness). tolerant 0 / audits −1 / draconian −2. Risk: low.

**20. Heterodox Sect Policy 白蓮教** — [ACCUMULATOR] `qing_sect_pressure` (`se_QING_DECLINE.txt:1005`).
**[REVIEW FIX — ratchet-defeat guard]** Sect pressure is the OUTPUT of 8+ systems (opium, canal neglect,
missionary friction, granary failure) and is meant to build toward rebellion. A standing suppress bias that
cancels it would legislate away the White-Lotus/Taiping. FIX: bias is SMALL and band-gated — suppress −1
applied only while `qing_sect_pressure > 25` (thins low-level unrest, cannot prevent a genuine crisis), with
a −minority-happiness cost that itself feeds unrest (so heavy suppression is self-limiting). tolerate 0 /
monitor 0 +watch modifier / suppress −1. Risk: low.

**21. Reform Posture** — [ACCUMULATOR, SIGNED ±100] `qing_reform_faction_balance`
(`se_QING_FACTION.txt:424`, raw `change_variable`, clamp ±100). **CRITICAL:** must use `change_variable`,
NOT `QING_DECLINE_nudge` (the macro clamps at 0 and would corrupt the signed meter — verify ALL existing
nudge sites use raw change_variable before adding the law bias). **[REVIEW: build with small tilt]** faction
balance is meant to emerge from events, so the law bias is a SMALL signed nudge (conservative −1 / gradualist
0 / reformist +1) that tilts the drift without swamping the ±5..±10 event/mission nudges. Modifier expresses
the court's reform posture. Risk: moderate (signed-clamp footgun — the #1 implementation caution).

**22. Deliberative / Banner Nobility Governance 議政王大臣** — [ACCUMULATOR] `qing_delib_cohesion`
(init 50, `se_QING_DELIBERATIVE.txt:367`). Law sets `qing_delib_bias` ∈ {empower +/ balance 0 / curb −}
added at the cohesion nudge; cohesion feeds `qing_banner_decay` bands. Modifiers express Manchu-grandee
prestige vs. autocratic centralization. Risk: low.

**23. Currency Stress / Monetary Response** — [ACCUMULATOR] `qing_currency_stress`
(`se_CURRENCY_STRESS.txt` engine drift + discrete nudges). **Pairs with vanilla `currency_law`.** Law sets
`qing_monetary_bias` ∈ {hard-specie −/ stabilization 0 / debasement +} added as a standing stress nudge.
Modifiers: hard-specie = +stability/−commerce; debasement = +tax/−stability. Risk: low. *(This is the Qing
analogue; see PART D for the vanilla monetary stubs.)*

### B3. BIAS-B — recomputed targets (one guarded term in the formula, before the clamp)

**24. Council Composition** — [RECOMPUTED-TARGET] `qing_council_eff_target` (rebuilt to 0 each pulse,
`se_QING_COUNCIL.txt:441`; clamp :554). Law sets `qing_council_comp_bias` threaded as `change_variable`
before :554. **BUT** the catalogue's real intent (Manchu-weighted / balanced / meritocratic) maps better to
the **`qing_council_dyarchic_balance` MODIFIER + seat composition** than to eff_target. **Design:** a
MODIFIER-SWAP law (each option a `modifier`) + optional bias into eff_target for the "meritocratic" tilt.
Do NOT set `qing_council_dyarchic_balance` (it's a banded modifier, not a var). Risk: moderate.

**25. Canal Grain Tribute Quota 漕運** — [RECOMPUTED-TARGET] `qing_canal_jiangnan_quota` (rebuilt to 0.5
each pulse, `se_QING_CANAL.txt:209`; clamp :228). Law sets `qing_canal_quota_bias` added before the :228
clamp. Options: relaxed −0.1 / standard 0 / maximal +0.15. Modifier: maximal = +grain/−Jiangnan happiness.
Risk: moderate.

**26. Xinjiang Administration 屯田/伯克** — [RECOMPUTED-TARGET] `qing_xj_consolidation` is rebuilt from
`qing_xinjiang_control` + terms (`se_QING_XINJIANG.txt:229`). **Law must feed an INPUT, not the output.**
Two clean choices: (a) bias `qing_xinjiang_control` (the ACCUMULATOR input, BIAS-A at a nudge) — but that's
the event-owned grip meter; risky. (b) add `qing_xj_admin_bias` as a term in the consolidation scratch
formula (BIAS-B before :227 clamp). **Design: BIAS-B** — options military-farm 屯田 (+consolidation) /
beg-indirect 伯克 (0) / provincialize 行省 (+more, +cost). Risk: moderate.

**27. Customs Service Regime 海關** — [RECOMPUTED-TARGET via input] `qing_customs_eff_target` rebuilt from
`qing_customs_foreign_control`×2 + bureau_integrity (`se_QING_CUSTOMS.txt:173-176`). The catalogue's
native/foreign-supervised axis maps to `qing_customs_foreign_control` (ACCUMULATOR, `:144` `$amount$`
helper). **Design: BIAS-A on `qing_customs_foreign_control`** via a standing nudge — native = −, Hart-style
foreign-supervised = + (efficiency up, autonomy/prestige down). Modifier expresses the sovereignty cost.
Risk: moderate. **Overlaps `qing_tariff_autonomy`** (treaty-state, see B4) — keep distinct: this is the
*administration*, tariff is the *rate*.

**28. Missionary Policy** — [RECOMPUTED-TARGET] `qing_antichr_target` / `qing_social_friction_target`
rebuilt from formula (`se_QING_MISSIONARY.txt:243-252/194-203`). Law sets `qing_missionary_tol_bias` as a
term in the target formula (prohibit − toleration → but that raises friction? model carefully: prohibit =
+sentiment via suppression backlash OR −reach; open = +reach/+friction). **Design: BIAS-B** on the target
formula + gate cathedral promotion (Design-1 coupling). Options prohibit / tolerate / open. Risk:
moderate-high (two coupled meters + Design-1). *Recommend building AFTER the simpler ones validate.*

**29. Sphere / (folded into #18 Great-Power Alignment)** — `qing_sphere_dominant` is RECOMPUTED from the
sphere formula and is better left read-only; the alignment law (#18) biases tension, not the sphere result.
No separate law. 

### B4. MODIFIER-LAW — event/treaty state (pure `modifier`, no var-write)

**30. Tariff Regime 關稅** — [TRADE × RATE, 1763-LIVE + CONCRETE] **[REDESIGNED 2026-07-24 — the treaty-var
version was DEAD at 1763].** The original design hooked `qing_tariff_autonomy` (`se_QING_TREATIES.txt`), a var
set ONLY by post-1842 unequal-treaty events — so at a 1763 start it is a flat 0 and the law was inert. The
speculative treaty-pulse edit was REVERTED. Correct frame: **tariffs are collected on ACTUAL TRADE, live from
game start.**
- **The real site (mapped + verified):** the **Canton pulse** `se_QING_CANTON.txt:93-102` computes customs
  yield from REAL engine trade-good production — `qing_canton_yield_tmp = (GOODS_national_production_tea +
  silk + porcelain) / 8`, then ×port-development ×Hoppo, split emperor/state by `qing_canton_purse_share`,
  paid to the treasury via `add_treasury` at `:140`. The Canton System (一口通商) is OPEN from game start
  (`qing_canton_regime = flag:open` seeded at boot, `qing_mechanics_on_actions.txt:188-190`; 1757 decree).
  This is the ONLY treasury customs revenue derived from actual on-map commerce. (Maritime Customs 海關 is
  `efficiency/5` with NO trade term and dormant until Hart ~1860s; caravan customs is real rate×base but
  taxes an abstract prosperity meter — both wrong for a 1763 trade tariff.)
- **Design:** the law sets `qing_canton_tariff_rate` ∈ {low / moderate / high}; the Canton pulse multiplies
  `qing_canton_yield_tmp` by the rate factor right after the goods sum (`:96`, mirroring the proven caravan
  `customs_rate` idiom, `se_QING_CARAVAN.txt:157-174`). Higher tariff = more customs revenue but a
  commerce/smuggling or foreign-friction cost modifier; low = less revenue, freer trade. NET-NEW-lite: one
  rate var + one guarded `multiply` (guarded `has_variable` → default byte-identical: unset = today's
  implicit moderate). Options 輕稅 low / 中稅 moderate (no-op default) / 重稅 high.
- **Late-game coupling (optional, deferred):** once the treaty era arrives (post-1842), `qing_tariff_autonomy`
  could CAP the reachable rate (the treaty-fixed 5% ceiling blocks "high") — an ADD-ON to the 1763-live trade
  law, not its foundation. Not built this pass.
- Risk: low-moderate (one multiply into a live real-trade formula; verify the rate factor + treasury-split
  interaction). **Concrete + 1763-live: PASSES the review criteria.**

**31. Frontier Trade Sovereignty 阿奇木** — [STATE-FLAG] `qing_caravan_aqsaqal_granted` toggled by
`QING_caravan_grant_aqsaqal`/`_revoke_aqsaqal` levers. Design: a law whose on_enact CALLS the existing
grant/revoke lever (grant-concession → `QING_caravan_grant_aqsaqal = yes`; assert → `_revoke_aqsaqal`).
This is a SELECTOR-via-lever (the levers are guarded + idempotent). Risk: low. *Novel pattern — on_enact
calling a scripted_effect; verify on_enact accepts effect calls (it does — see estab laws' set_variable).* 

**32. Overseas Expansion** — [MODIFIER/EVENT-STATE] colonies + treasure fleet are boolean country
modifiers granted by missions/events (`se_QING_TREASURE_FLEET.txt:144-153`). Design: pure MODIFIER-LAW —
isolationist / trade-fleet / colonial, each a `modifier = {}` (naval/colonial cost vs. prestige). on_enact
may nudge `qing_tributary_prestige`. Does NOT grant colonies (those stay mission-earned). Risk: low.

**33. Foreign-Office Doctrine 總理衙門** — [EVENT-STATE] legation/embassy counts are event-established;
`qing_zongli_diplomat_count` is RECOMPUTED from marked characters. Design: MODIFIER-LAW — tributary-only /
resident-legations / full-diplomacy, each a `modifier` (diplomatic-reputation/reform-pressure trade).
on_enact nudges `qing_reform_pressure` (adopting full diplomacy breaks the tribute worldview, matching the
P3 legation event). `allow` gates "full diplomacy" on `qing_legation_count >= 1`. Risk: low.

### B5. Court / Succession — mixed, several construction-risky or one-way (design with care)

**34. Succession Method 秘密立儲** — [ONE-WAY-FLAG] `qing_secret_succession_sealed` is a discrete seal set
=1 then event-REMOVED at accession (`se_QING_PRINCES.txt:342/400`). It is NOT a persistent policy toggle.
**A reversible law is new capability.** Design: MODIFIER-LAW selector `qing_succession_method_law` ∈ {open
公開 / secret 秘密立儲 / deliberative 議政} where the option sets a NEW standing var `qing_succession_mode`
(this is a genuine policy stance, distinct from the per-reign seal flag) that the princes/accession code
reads to choose the pick algorithm. **This is NET-NEW-lite** (new var + a read at the accession pick,
`se_QING_PRINCES.txt:336` `order_by`). Risk: moderate (touches succession). *Recommend: design now, build
in its own careful chunk.*

**35. Regency Rules** — [EVENT-STATE] `qing_office_regent_holder` (char handle) + `qing_regent_pick_kind`
(flag, log-only) installed/cleared by regency machinery. No persistent policy var. Design: MODIFIER-LAW +
NET-NEW selector `qing_regency_pref` ∈ {dowager / prince / councillor} that `QING_seat_regent_install`
(`se_QING_SEATS.txt:270-324`) reads to order its pick. NET-NEW-lite (one read added). Risk: moderate.

**36. Princely Establishment** — [ACCUMULATOR, per-character] `qing_prince_backing` (char var, nudged +
`order_by` selector). Country-scope law can't set a per-char var directly. Design: MODIFIER-LAW (favour /
investigate / restrict) each a `modifier` affecting prince loyalty/threat, + optionally a country var
`qing_prince_policy` read by `QING_prince_backing_nudge` to scale the nudge. Risk: low-moderate.

**37. Harem Establishment 后妃** — [RECOMPUTED + CONSTRUCTION-RISKY] `qing_harem_rankN_count` rebuilt from
the consort roster (`se_QING_HAREM.txt:122-142`); touches consort create/promote paths. **DEFER** — the
audit flags the harem create path as #90/#336-sensitive; a size/rank-distribution law would need to gate
the promotion cap, and the value is a recomputed tally (can't be set). If built: a cap var
`qing_harem_size_cap` read at the promotion gate (`:246`). **Recommend: DEFER** (construction risk >
value). Risk: high.

**38. Eunuch Policy 內務府** — [RECOMPUTED + CONSTRUCTION-RISKY] `qing_eunuch_count` sits on the
`create_character` eunuch-mint path (`se_QING_HOUSEHOLD.txt:82-106`); no live consumer outside its own file.
**DEFER** — restrict/standard/empowered would gate the mint count (construction-risky) and nothing reads the
count today, so the policy has no mechanical bite yet. **Recommend: DEFER.** Risk: high.

### B6. Frontier / Integration

**39. Tributary Ritual Frequency 朝貢** — [PER-SUBJECT TIMER] `qing_tribute_cooldown` is a per-subject
`days=` timer gate (`se_QING_TRIBUTE.txt:257-266`). A CHI country law can't set a per-subject var. Design:
MODIFIER-LAW + a country var `qing_tribute_cadence_law` that `QING_tribute_*` reads to CHOOSE the cooldown
length (1095/1825/2190 already the three branch values — the law selects which branch). NET-NEW-lite (one
read). Options frequent / standard / rare. Risk: low-moderate.

**40. Frontier Settlement Policy 移民實邊** — [ONE-WAY-FLAG] `qing_frontier_resettlement` set once =1, never
cleared (`se_QING_POPULATION.txt:242`). **A closed↔encouraged↔forced law needs a clear-path (new
capability).** Design: replace the one-way flag read at `se_QING_POPULATION.txt:95` with a tri-state var
`qing_frontier_settle_policy` ∈ {closed 0 / encouraged 1 / forced 2} the law sets; migrate the existing
flag semantics (flag-set ⇒ value≥1). NET-NEW-lite + a migration guard. Options closed / encouraged / forced
(forced = +migration/−minority happiness). Risk: moderate (migration-relief-valve interaction).

**41. Cultural Assimilation Doctrine 漢化** — [per-char selector + RECOMPUTED count] `qing_manchu_identity`
(per-char, banded modifier-swap) + `qing_sinic_count` (recomputed province tally). Country law can't set
per-char identity. Design: MODIFIER-LAW (preserve-Manchu / balanced / sinicize) each a `modifier` + a
country var `qing_assimilation_doctrine` read by `QING_char_shift_identity`/sinicization pulse to bias the
drift direction. NET-NEW-lite. Risk: moderate.

**42. National Integration** — [ACCUMULATOR via target-lift] `qing_civic_identity` — the SAFE knob is the
Design-4 `qing_civic_identity_settle_bonus` target-lift (`se_QING_DECLINE.txt:856`). Law sets
`qing_integration_doctrine_bias` folded into `qing_civic_target_tmp` alongside the settle bonus (BIAS-B into
the target). Options dynastic (0) / multi-ethnic (+) / civic-nation (++). Modifier: civic-nation =
+assimilation/−traditional-legitimacy. **Couples to Design 4.** Risk: low-moderate.

**43. Amban Establishment 理藩院** — [NET-NEW] `QING_AMBAN_MIN` does not exist (not even a constant — only
a nickname substring). Design: author a new var `qing_amban_estab_target` (mirror `qing_ministry_estab_law`
exactly — that's the proven precedent) read by the amban staffer. **NET-NEW plumbing** (var + one read).
Options lean / standard / expanded. Risk: moderate (mirrors proven estab work).

### B7. Modernization capstones

**44. Modernization Doctrine 自強** — [ACCUMULATOR] `qing_selfstr_progress` (band → 3-modifier swap,
`se_QING_SELFSTR.txt:672`). Self-strengthening progress is meant to be EARNED (missions/events), not
legislated. Design: a pure MODIFIER-LAW (conservative / ti-yong 中體西用 / wholesale-western) each a `modifier`
expressing the reform posture. **[REVIEW FIX — no farmable nudge]** the earlier "one-time on_enact nudge" is
a toggle-farm (on_enact fires every enact). If a "wholesale-adoption kickstart" is wanted, it MUST be
once-guarded: `on_enact = { if = { limit = { NOT = { has_variable = qing_selfstr_wholesale_adopted } }
QING_selfstr_advance = { amount = X }  set_variable = qing_selfstr_wholesale_adopted } }` — fires at most once
ever. Default: no kickstart, pure modifier. Risk: low-moderate. *The three band-modifiers stay
progress-driven; the law is the posture overlay.*

**45. Exam Curriculum (practical-subjects / abolition)** — [NET-NEW] beyond cadence, no backing mechanic
exists. Design: new var `qing_exam_curriculum` ∈ {classical 0 / practical 策論 1 / abolition 2}; classical
= no-op, practical = bias `qing_exam_pass_rate` recompute + a research modifier, abolition = disables the
exam cycle (gate `QING_exam_*` on curriculum≠2) + a big stability/legitimacy shock. **NET-NEW plumbing**
(var + reads in the exam pulse). Options classical / practical / abolition. Risk: moderate-high (abolition
disables a whole subsystem — needs careful gating). *Recommend: build classical/practical first; abolition
as a follow-up.*

**46. Censorate Empowerment 都察院** — [RECOMPUTED-TARGET] `qing_censorate_vigor` rebuilt from officeholder
traits/finance each cycle (`se_QING_CENSORATE.txt:58-64`, clamp 0..50). This was the ORIGINAL exclusion.
Design: BIAS-B — add `qing_censorate_bias` as a term in the recompute before the :66 clamp (weak −/ active 0
/ weaponized +). Modifier: weaponized = +corruption-detection/−official happiness (factional purges). Risk:
moderate (this is the meter the whole "fights-the-pulse" rule was named after — bias-B is the correct, safe
way now that the pattern is proven).

**47. Public/Palace Works Priority 三山五園** — [EVENT/MODIFIER-STATE] no numeric priority meter; the
Summer Palace (`qing_sp_*`) + Works (`qing_works_*`) subsystems are event/flag-driven. Design: pure
MODIFIER-LAW (frugal / balanced / grand) each a `modifier` (construction/prestige vs. treasury/corruption).
**[REVIEW FIX — no farmable nudge]** does NOT nudge `qing_corruption_level` on_enact (toggle-farm). The
"grand works breed graft" flavour is expressed as a standing `monthly_corruption` MODIFIER on the "grand"
option, not a one-off var nudge. Does NOT build the palace (that stays the Summer Palace tree). Risk: low.

---

## PART C — Summary: build order & disposition

**BUILD — trivial (SELECTOR / MODIFIER-SWAP / MODIFIER-LAW), no pulse edits (~9):**
Industrial Encouragement (13), Tariff Regime (30), Frontier Trade Sov (31), Overseas Expansion (32),
Foreign-Office Doctrine (33), Princely Establishment (36), Public Works Priority (47), + the two vanilla
Upper House stubs & monetary stubs (PART D).

**BUILD — BIAS-A, one guarded nudge line each (~7):** Provincial Militarization (14), Army Modernization
(15), Cultural Patronage (16), Overseas Education (17), Great-Power Alignment (18), Deliberative Governance
(22), Monetary Response (23). Plus opt-in Anti-Corruption (19).

**BUILD — BIAS-B, one guarded formula term each (~6):** Council Composition (24), Canal Quota (25),
Xinjiang Admin (26), Customs Regime (27), Missionary Policy (28), National Integration (42), Censorate
Empowerment (46).

**BUILD — NET-NEW-lite, new var + one read (~6):** Succession Method (34), Regency Rules (35), Tributary
Ritual (39), Frontier Settlement (40), Assimilation Doctrine (41), Amban Establishment (43), Modernization
Doctrine (44), Exam Curriculum practical (45, classical/practical only).

**USER DECISION (2026-07-24):** build all deferrals EXCEPT the exam-abolition tier. Sequence **by risk
ascending, commit + push each batch** so boot-testing is incremental.
- Harem Establishment (37) — **BUILD** (extra care on the consort create/promote path; law gates the
  promotion cap `qing_harem_size_cap`, does NOT touch create_character itself).
- Eunuch Policy (38) — **BUILD** (law sets a mint-cap var read at the mint gate; does NOT add modifiers
  inside create_character — #90 rule).
- Heterodox Sect (20) — **BUILD** (Bias-A on `qing_sect_pressure`; tolerate/monitor/suppress).
- Reform Posture (21) — **BUILD** (Bias-A on `qing_reform_faction_balance` — MUST use raw `change_variable`
  with the ±100 clamp, NOT `QING_DECLINE_nudge`).
- Exam Abolition tier (45b) — **STILL DEFERRED** (disables a subsystem; follow-up only). Exam Curriculum
  (45) ships classical/practical only.

**Net new law groups this pass: ~32 built + 4 vanilla stubs filled = ~36**, taking the Qing total from 13 →
~45.

### Batch plan (risk ascending; each boots + commits on its own)
- **Batch 1 — GUI + trivial + upstream stubs:** PART A (6 new `laws_widget_area` columns + re-file 13
  existing), the ~9 selector/modifier-swap/modifier-law groups (13/30/31/32/33/36/47), the 4 vanilla stub
  fills (48/49/50/51) + the `00_administrative_laws.txt` brace fix. GUI is a prerequisite so it leads.
- **Batch 2 — Bias-A** (one guarded nudge line each): 14/15/16/17/18/19/20/21/22/23/44.
- **Batch 3 — Bias-B** (one guarded formula term each): 24/25/26/27/28/42/46.
- **Batch 4 — Net-new-lite** (new var + one read): 34/35/39/40/41/43/45(classical+practical).
- **Batch 5 — [REVIEW FIX] REMOVED.** #37 (harem) and #38 (eunuch) are NOT standalone laws — a law shipped
  before its backing mechanic is a no-op. They live ONLY in the court-intrigue subsystem batches (6 eunuch /
  7 harem), where the law is built in the SAME batch as the mechanic it gates. The old Batch 5 is dissolved.
Each batch: author data → loc → GUI entry → pulse wire (if any) → brace/quote check → code-review →
boot-crash review → commit as freekumquats → push merge-overnight.

---

## PART D — Upstream Victorian-TC stubs (Upper House ×2, Monetary ×2)

These ship in the repo with **empty `modifier = {}` on every option** and are absent from vanilla Imperator
AND both oracle repos (Invictus, TI never added a bicameral legislature or monetary-setting layer). Nothing
to copy — fill plausibly with **proven modifier keys** (drawn from `00_economic_laws.txt` currency_law etc.).

**FIRST, fix the brace bug:** `00_administrative_laws.txt` is 9-open / 8-close — `delegated_monetary_policy`
(line 10) never closes, so `legislative_monetary_policy` is nested inside it (the group has only 2 valid
options). Add the missing `}` after `delegated_monetary_policy`'s `modifier`.

**48. `monetary_policy_law`** (executive / delegated / legislative) — WHO controls minting. Fills:
- executive: `stability_monthly_change = 0.02`, `monthly_corruption = 0.02` (crown control, mild graft)
- delegated: `global_commerce_modifier = 0.03`, `global_tax_modifier = 0.02` (competent ministry)
- legislative (`allow = is_republic`): `global_commerce_modifier = 0.05`, `research_points_modifier = 0.02`,
  `stability_monthly_change = -0.02` (accountable but slow). This gates `monetary_policy_setting`.

**49. `monetary_policy_setting`** (recall / limited minting / more minting / issue bonds) — the stance,
gated on `legislative_monetary_policy`:
- currency_recall: `global_commerce_modifier = -0.05`, `stability_monthly_change = 0.03` (deflationary sound-money)
- limited_minting: `monthly_corruption = -0.03`, `global_upper_strata_happyness = 0.03`
- more_minting: `global_tax_modifier = 0.05`, `global_commerce_modifier = 0.05`, `stability_monthly_change = -0.02`
- issue_bonds: `global_commerce_modifier = 0.1`, `global_capital_trade_routes = 1`, `monthly_corruption = 0.03`
  (mirrors currency_law's `promissory_notes`).

**50. `upper_house_powers_law`** (veto / review / delay) — gated `has_law = bicameral_legislature`:
- power_of_veto: `stability_monthly_change = 0.03`, `global_middle_strata_happyness = 0.05`,
  `monthly_political_influence = -0.05` (strong chamber, slower governance)
- power_of_review: `global_upper_strata_happyness = 0.03`, `stability_monthly_change = 0.01`
- power_of_delay: `monthly_political_influence = 0.03`, `global_middle_strata_happyness = -0.02` (weak chamber)

**51. `upper_house_composition_law`** (appointed-spiritual / appointed / elected / state-reps) — gated
`has_law = bicameral_legislature`:
- appointed_hereditary_spiritual: `global_upper_strata_happyness = 0.05`, `monthly_legitimacy = 0.05`
  (`omen_power` was WRONG — it means MINING output in this TC, per imp19c_modifier_equivalencies.txt;
  monthly_legitimacy fits a hereditary/spiritual chamber), `global_middle_strata_happyness = -0.02`
- appointed: `monthly_political_influence = 0.05`, `global_upper_strata_happyness = 0.02`
- elected: `global_middle_strata_happyness = 0.05`, `global_lower_strata_happyness = 0.03`,
  `stability_monthly_change = -0.02`
- state_representatives: `global_pop_assimilation_speed_modifier = 0.05`, `diplomatic_reputation = 0.5`
  (federal chamber).

**LOC:** replace placeholder descs (`"Power of Veto desc"`, `""`) with real 1-line flavour for all option
`_desc` keys (laws_l_english.yml:367-637). **VERIFY every modifier key** against the schema before commit
(all keys above are drawn from existing law/modifier files, but confirm `omen_power`/`monthly_governor_wage`
etc. resolve — a bad key is a boot error).

**GUI:** the four vanilla stubs are ALREADY registered in `government_view.gui` (lines 2040-2144); no new
area needed for them — only the `modifier`/loc fills + the brace fix.

---

## PART E — Cross-cutting build rules (apply to every group)

1. **Guarded reads:** every bias var read at a pulse site MUST be `if = { limit = { has_variable = X } … }`
   so the default (var unset) is byte-identical to today. (P7 proven, `se_QING_DECLINE.txt:919-920`.)
2. **No-op default:** every group's first option sets the bias to 0 / the current value — enacting nothing
   changes nothing. Verify against each var's INIT.
3. **Signed meters:** `qing_reform_faction_balance` is ±100 via raw `change_variable` — NEVER drive with
   `QING_DECLINE_nudge` (clamps at 0). (If (21) is ever built.)
4. **Recomputed targets:** never `set_variable` the target directly — thread the bias into the formula
   BEFORE the clamp (BIAS-B). Applies to 24/25/26/27/28/42/46.
5. **on_enact calling effects:** (31) calls `QING_caravan_grant_aqsaqal` — confirm on_enact accepts effect
   calls (estab laws prove set_variable works; a scripted_effect call is the same effect context — verify at
   build).
6. **GUI registration is mandatory:** an unregistered law group is invisible. Every new group needs a
   `laws_widget` line in its domain `laws_widget_area` (PART A).
7. **BOM:** `00_qing_statutes_laws.txt` — check whether it carries a BOM before Python-editing (setup/ reader
   rejects BOM; common/ lexer tolerates it — but preserve whatever's there).
8. **Boot-crash review + se_LOG** per standing rules; commit as freekumquats; push to merge-overnight.

---

## MASTER EFFECTS TABLE (all laws — implemented + pending, 2026-07-24)

### IMPLEMENTED (13, common/laws/00_qing_statutes_laws.txt)
| Law | Options | Effect |
|---|---|---|
| Penal Code 大清律例 | balanced / merciful / harsh / revised¹ | merciful −0.5 unrest +0.02 legit −0.02 tyranny; harsh −1 unrest +0.01 stab −0.02 legit; revised¹ −0.5 unrest +0.02 legit +0.02 state-loyalty |
| Ritual Orthodoxy 禮部 | conventional / orthodox / pragmatic¹ | orthodox +0.03 legit +0.01 stab −0.03 commerce; pragmatic¹ +0.05 commerce −0.01 legit |
| Opium Policy 鴉片 | prohibit / tolerate / legalize² | qing_opium_posture 0/1/2 → opium climb + trade-drain → currency stress |
| Caravan Customs 定稅則 | light / moderate / heavy | qing_caravan_customs_rate 0/1/2 → income base ×{0.25/0.5/1.0} → treasury (base→real goods, pending) |
| Salt Admin 鹽政 | farmed-out / reformed¹ | qing_salt_gabelle_reformed → +15 salt revenue, ministry eff, −venal pool |
| Canton Regime 廣州體制 | open / closed | qing_canton_regime flag → open runs Canton real-goods customs; closed seclusion |
| Ethnic Governance 滿漢 | dyarchy / banner / han | QING_set_ethnic_stance → stance modifiers + ethnic-tension drift |
| Office-Selling 捐納 | exam-only / mixed / open-sale | qing_office_purchased_ranks modifier (+corruption −tax −promotion) + −bureau integrity |
| Exam Cadence 科舉 | triennial / biennial / sexennial | qing_law_exam_cadence → cooldown 730/1095/2190 → jinshi spawn rate |
| Ministry Estab 員額 | lean3 / standard4 / expanded6 | qing_law_ministry_estab_target → diplomat/censor/guard head-count |
| Advisory Estab 顧問 | cautious2 / measured3 / open5 | qing_advisor_slot_cap → advisor retention cap |
| Canton Purse 內帑 | treasury0 / shared50 / purse100 | qing_canton_purse_share → Canton revenue state/emperor split |
| Military Upkeep 武備 (P7) | statutory / reformist / frugal | banner/gs upkeep bias 0/−1/+1 at decay nudge ⚠️DORMANT<1772 (High-Qing fix pending) |
¹reform-track gated (pressure≥50) · ²treaty-era gated

### PENDING — SURVIVING SET (post 1763-liveness review)
**Trivial/modifier-swap:** Industrial Encouragement (state/supervised/merchant — research/commerce trade-offs); Princely Establishment (favour/investigate/restrict); Public Works Priority 三山五園 (frugal/balanced/grand); Frontier Trade Sovereignty 阿奇木 (grant/assert — aqsaqal lever); Overseas Expansion (isolationist/trade-fleet/colonial).
**Bias-A:** Provincial Militarization 勇營 (±1 qing_han_provincial_power); Cultural Patronage 文治 (qing_wenzhi_patronage drift); Deliberative Governance 議政王大臣 (qing_delib_cohesion); Monetary Response (qing_currency_stress); Anti-Corruption 肅貪 (−1/−2 corruption, floored>20); Heterodox Sect 白蓮教 (−1 sect, gated>25); Reform Posture (±1 signed reform_faction_balance).
**Bias-B:** Council Composition (qing_council_eff_target); Canal Quota 漕運 (qing_canal_jiangnan_quota); Xinjiang Admin 屯田/伯克 (qing_xj_consolidation); Missionary Policy (qing_social_friction_target + cathedral gate); Censorate Empowerment 都察院 (qing_censorate_vigor).
**Net-new-lite:** Tariff Regime 關稅 (rate × Canton real-goods yield → treasury); Succession Method 秘密立儲; Regency Rules; Tributary Ritual 朝貢; Frontier Settlement 移民實邊; Assimilation Doctrine 漢化; Amban Establishment 理藩院; Exam Curriculum (classical/practical, abolition deferred).
**Re-based (1763-live, verifying):** Drill Posture (was Army Modernization — banner/gs drill bias, needs High-Qing fix); Inner-Court Scholarship 南書房 (was Overseas Education); Canton Supervision 粵海關監督 (was Great-Power Alignment — Hoppo squeeze); Frontier Diplomacy 理藩院 (was Foreign-Office — Lifan Yuan Amban coverage); National Integration (→NATIONALISM mechanic: qing_national_awakening/civic-identity/citizenship); Modernization Doctrine 自強 (→TECH + new units + modifiers); Customs Regime (→UPSTREAM base-game trade system, vs Canton/caravan; may merge w/ Tariff).
**Upstream stubs:** Monetary Policy (executive/delegated/legislative³); Monetary Setting (recall/limited/more/bonds); Upper House Powers (veto/review/delay); Upper House Composition (spiritual/appointed/elected/state-reps).
³is_republic gated
