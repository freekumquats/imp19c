# 1763 starting-tech seeding — historical audit + rework plan

## Handoff plan (read this first — this is the answer to "what are the steps")

This session is ending (model switch, to restore web access for real source-checking).
Phases below, in order. Everything after this section is supporting research already
done — read it before starting Phase 1, don't re-derive it.

**Phase 1 — finish the research (blocked items only, don't redo what's done):**
1. Re-run/confirm the GBR/FRA-individual audit (was mid-flight when interrupted; expect
   confirmation that all of GBR's and the FRA/NED/USA/german block's individually-listed
   techs are anachronistic, per the "Individual GBR/FRA grants" table below, but verify —
   don't assume).
2. Run the CHI-only deep second pass the user explicitly asked for (separate from every
   other bloc, no bundling). Use real web/academic sources now that they're available —
   the first-pass CHI findings below were trained-knowledge only. Specific angles to dig
   into: exact dates of Qing-Jesuit artillery technology transfer and its Qianlong-era
   stagnation (get real years, not "17th century"); whether Qing fiscal administration
   (地丁銀 land-poll tax, 常平倉 state granary administration) justifies a civic/oratory
   tech beyond what's already recommended; cross-check against this mod's other
   already-built Qing systems (Grand Council, Ministry of Revenue, Industrialisation
   seeding) so CHI's tech list is consistent with them, not decided in isolation.
3. Resolve the "Bloc E" open question below (currently-zero-grant Sub-Saharan
   African/Native American culture groups) — this is a scope ADDITION, not just a cap
   change, so it needs an explicit decision, ideally source-checked (firearms-by-trade
   reach into the Sahel/Horn of Africa and eastern-woodland North America by 1763).

**Phase 2 — design.** A fork produced an unplanned but genuinely sharper synthesis than my
own first-pass audit while this session ran (see "Superseding insight" below) — it caught
a granularity problem my per-bloc audits missed: `military_level_3` and `religious_level_3`
each mix pre-1763-real content with Napoleonic/19th-century content, so capping the WHOLE
tier either denies Europe its period-correct muskets/bayonets or grants it anachronistic
rifle corps. Use that synthesis's proposed fix (two new 1763-only subset macros,
`TECH_unlock_military_1763_syw` and `TECH_unlock_religious_1763_enlightenment`) as the
starting point for Phase 2, not my cruder uniform-tier-cap approach. Fold in the Phase-1
CHI/GBR-FRA results. Produce one concrete edit spec: per-bloc tier ceiling, named
exceptions (e.g. the oratory-4 banking trio for GBR/NED/Sweden/FRA/German only), and the
exact new macro contents — ready to paste into `se_TEST.txt`'s `else` branch.

**Phase 3 — adversarial review.** Dispatch a skeptical pass against the Phase 2 design
specifically (not the individual per-bloc audits again) — check internal consistency
across blocs (e.g.: does CHI end up out-bureaucracying Europe but lagging it in
mechanization, as intended? does the Western-Europe leader/laggard split — if adopted —
actually match which countries use which OR-list in the file?), and re-verify a sample of
the historical claims against real sources now that web access exists.

**Phase 4 — implement.** Edit `se_TEST.txt`'s 1763 `else` branch (currently the uniform
heuristic cap) to the reviewed design. Verify brace balance
(`python3 -c "print(open(f).read().count('{'), open(f).read().count('}'))"`-style check,
already the pattern used this session). Ideally boot-test.

Files already touched this session for this feature: `common/scripted_effects/se_TEST.txt`
(will be edited again in Phase 4). Design docs on disk: this file, plus
`design/DESIGN_1763_STARTING_TECH.md` (the fork's unplanned synthesis — untracked,
uncommitted, not reviewed by the user yet, but its analysis is the Phase 2 starting point
per above — read it in full, don't just skim the excerpt below).

## Context

`common/scripted_effects/se_TEST.txt`'s `TECH_unlock_all_starting_techs` grants free
starting inventions per culture-group bloc. It was tuned for the mod's original 1815
bookmark and fired unconditionally regardless of bookmark date. At the 1763 bookmark this
handed Western-European countries a decades-premature tech bundle (GBR: steam
locomotives, railways, torpedoes, steam warships — all real-world 1780s-1860s) while Qing
(CHI) got a much smaller, more period-appropriate list — the root cause of a reported
GBR=75/FRA=67/CHI=12 starting-Industrialisation-value gap.

**Already implemented** (this session, in `se_TEST.txt`):
1. Date gate: `if = { limit = { current_date >= 1815.1.1 } ... } else = { ... }`. The
   1815+ branch is byte-for-byte the original tuning, untouched.
2. A first-pass 1763 `else` branch: same culture-group OR-lists (no bloc removed), but a
   **uniform heuristic cap** per bloc (roughly: military 0-1, oratory 1-2, civic 1-2,
   religious 1-2), with every individually-listed late invention (GBR's steam/rail/
   torpedo grants, the FRA/NED/USA/german block's steam-engine grants, TUR's
   limber/howitzer/skirmisher_corps/rifles) dropped entirely.
3. Two pre-existing typo fixes unrelated to the date issue: `tech_warhsips` →
   `tech_warships`, `tech_neoclassicisim` → `tech_neoclassicism` (in the shared
   `TECH_unlock_military_level_1`/`TECH_unlock_religious_level_3` blocks, so both eras
   benefit).

**User's follow-up ask:** the uniform heuristic cap in step 2 is a shortcut, not a real
audit. Do the audit properly: per-bloc historical research → a design for what each
group's 1763 tech should actually look like → adversarial review of that design → then
implement. Qing specifically gets its own dedicated, deeper second pass (it must be
accurate to Qing itself, not folded into a broader-group heuristic). Consult academic
sources as needed — **note: this session has no web search tool**, only `WebFetch` against
a URL if one is supplied. The user is switching models specifically to restore web access
before continuing; context (this file) is the handoff.

## Tier reference (unchanged, from `se_TEST.txt`)

- Military L0: weapon_manufacturing, firearms, shipyards
- Military L1: permanent_army, field_ambulances, shipyards, warships, cannons
- Military L2: bombard_cannons, warships
- Military L3: sword_bayonet, replaceable_weapon_parts, rifles, mortar, wheeled_cannons,
  limber, howitzer, naval_explosives, carronade, multiple_deck_warships,
  round_bow_megavessels, copper_plating, commissioned_staff, regimental_structure,
  specialised_corps, mass_mobilisation, skirmisher_corps, mass_artillery, cartography
- Oratory L1: central_archiving, monetary_theory, central_administration
- Oratory L2: urban_planning, standardised_writing_system, chancery_and_diplomatics
- Oratory L3: clearing_houses
- Oratory L4: central_banking, insurance_agencies, public_debt_administration
- Civic L1: metalworking, construction
- Civic L2: artificial_canals, gear_systems, templating, mining_rails
- Civic L3: spinning_frame, threshing_machine
- Civic L4: mechanical_tools, sewer_systems, manufactories, bloomery,
  organometallic_compounds
- Civic L5: blast_furnace, electricity, reciprocating_engine
- Civic L6: experimental_telegraph, voltaic_pile
- Religious L1: education, art_history, astronomy
- Religious L2: national_epic, theatre
- Religious L3: scientific_method, astrophysics, absorption_spectroscopy,
  secular_sciences, neoclassicism

## Research findings so far (trained-knowledge audits, no live sources — re-verify once
## web access is back, especially anything marked ⚠)

### Western Europe (french/british/spanish/portuguese/south_latino/north_latino/german/
### scandinavian/italian/mediterranean_romance/hungarian/north_ugric/baltic/dutch/
### north_american)

| Category | Cap | Why |
|---|---|---|
| Military | L2 | L0-2 are mid-18th-c. or older (standing armies, ships of the line, howitzers/mortars). L3 is dominated by Revolutionary/Napoleonic content (mass_mobilisation = levée en masse 1793; skirmisher_corps/specialised_corps/commissioned_staff/mass_artillery = 1790s-1800s; carronade 1770s Carron Co.; round_bow_megavessels 1817; naval_explosives 19th c.) — 30-60+ yrs premature. |
| Oratory | L2 | L3 clearing_houses (~1770s London) is ~7 yrs premature. |
| Civic | L2 | L3 spinning_frame is Arkwright **1769** (not 1764 as I'd assumed — ⚠ recheck), threshing_machine ~1784. L4-6 (manufactories/blast furnace/reciprocating engine/telegraph/voltaic pile) are unambiguously 1770s-1840s. |
| Religious | L2, +exception | L3 is mixed: **keep** scientific_method/secular_sciences/neoclassicism (Enlightenment-era, genuinely contemporary — Encyclopédie 1751-72, neoclassicism emerging via Winckelmann/Adam/post-Herculaneum excavations by the early 1760s); **exclude** astrophysics/absorption_spectroscopy (19th-c., Fraunhofer/Kirchhoff). |

Exception candidates flagged, not yet decided:
- `central_banking`/`insurance_agencies`/`public_debt_administration` (oratory L4): genuinely
  mature by 1763 for GBR/NED/Sweden/France/Prussia specifically (Bank of England 1694, Bank
  of Amsterdam 1609, Sweden's Riksbank 1668 — oldest central bank in the world, Lloyd's-style
  marine insurance since 1680s, Britain's funded national debt decades old). **Not** for
  Spain (Banco de España 1782) or Portugal.
- `copper_plating` (military L3): borderline — HMS Alarm copper-sheathed 1761, but wider
  Royal Navy adoption not until the 1770s. Lean exclude.
- Bloc is NOT uniform: leaders (GBR/FRA/German states/NED, +Sweden for banking) vs.
  laggards (Spain/Portugal — Bourbon fiscal reforms only just starting under Charles III)
  vs. colonies (North American colonies plausibly lower than their metropole, but the
  existing check is culture-group not colonial-status — unresolved by tier alone).
- **Open design question:** does splitting this bloc into a "core" vs "periphery" OR-list
  (to express the leader/laggard exception) justify the added complexity, or is a single
  uniform L2 cap (dropping the banking exception bloc-wide) good enough? Not decided.

### GBR-specific and FRA/NED/USA/german-specific individual grants

**This audit fork (`a432409195b268c0a`) was still running when the session was
interrupted — re-run or resume it before finalizing.** Expectation based on the other
findings: essentially every individually-listed tech in both blocks
(rotative_beam_engine, cotton_gin, double_acting_cylinders, experimental_railway,
steam_locomotive, rack_railway, torpedoes, steam_powered_ships, scientific_revolution,
rocket_artillery) is 1770s-1860s and should be dropped from the 1763 branch entirely —
confirm before implementing, don't assume.

### Slavic (south/west/east_slavic — Russia, Poland-Lithuania, Balkan Slavs)

| Category | Cap | Why |
|---|---|---|
| Military | L2, + Russia-specific mass_artillery + commissioned_staff | Russia fielded a large, competent army with real artillery by 1763 (beat Prussia at Kunersdorf 1759, took Berlin 1760; Shuvalov's unicorn-gun artillery reforms). But L3 as a **bloc** grant is wrong — hands rifles/skirmisher_corps to Poland-Lithuania (militarily moribund, army capped near 12,000 by law) and the Balkans too. Bloc gets L0-2; add the two Russia-specific L3 items individually if a c:RUS block is added. |
| Oratory | L2 | No central bank in 1763 (State Assignation Bank FOUNDED 1768 by Catherine II's decree, operational/branches-open 1769 — corrected 2026-08-26, was misdated "1769 founded"; State Loan Bank 1786), no developed public-debt market (first foreign loan 1769). All postdate 1763, so the no-central-banking cap holds. |
| Civic | L2 | Even L3 spinning_frame (1769 English) is wrong for Russia. Level 1-2 justified: Urals ironworks (Demidov), Vyshny Volochyok canal system operational. |
| Religious | L2, Russia-specific L3 optional | St. Petersburg Academy of Sciences (1724), Moscow University (1755) give Russia a thin L3 claim, but wrong as a bloc grant for Poland/Balkans. Optionally add L3 for c:RUS specifically. |

### Ottoman/Islamicate (west_turkic/levantine_arabic/african_arabic/albanian/greek/
### armenian/romanian/central_iranian/eastern_arabic/dagestani/central_aryan/east_iranian/
### west_iranian) + TUR individual grants

| Category | Cap | Why |
|---|---|---|
| Military | L0-2 + mortar, wheeled_cannons (**drop** naval_explosives, carronade) | Ottoman gun-founding tradition (1453 great bombards → 18th-c. field guns) supports mortars/wheeled cannon and bombard_cannons (L2). Carronade is 1778 Scottish (Carron Co.) — ~15 yrs premature and specifically Western; Ottoman navy of the 1760s was conventional round-shot, not proto-explosive-shell ordnance. |
| Oratory | L1-2 (unchanged) | Ottoman scribal/chancery bureaucracy (divan, defterdar fiscal records, timar registers) genuinely supports this. No L3-4 (Ottoman Bank/public debt apparatus is 1850s-60s). |
| Civic | L1-2 (also: **fix the pre-existing duplicate `TECH_unlock_civic_level_3 = yes` line** — a bug independent of the era question) | L3 spinning_frame/threshing_machine is Western Industrial-Revolution machinery, absent from the 1763 Ottoman/Persian world. L1-2 (qanat/irrigation works, public works) defensible. |
| Religious | L1-2 (unchanged) | Islamic madrasa + astronomical tradition supports L1; Firdawsi's Shahnama tradition/Ottoman court literature supports L2 (national_epic/theatre). L3 is the specifically post-Enlightenment Western package — exclude. |

**TUR's 4 individual grants — drop all four:**
- `tech_limber` — Gribeauval-system mobile field artillery, 1765+ French. Drop.
- `tech_howitzer` — the one closest to defensible (howitzers existed generally by mid-18th c.), but Ottomans were artillery laggards by the 1760s; misrepresents pre-1768-war reality. Lean drop.
- `tech_skirmisher_corps` — Napoleonic-era (1790s+) doctrine. Drop.
- `tech_rifles` — 19th-c. corps-level capability. Drop.
All four are Nizam-i Cedid-era (Selim III's reforms began 1793) or later — no 1763-era
precedent. The bloc's mortar+wheeled_cannons already give period-correct Ottoman artillery.

### South/Southeast/East Asia (southern/western/eastern_aryan, dravidian, burmic, tai,
### vietic, malaysian, gurkani, indo-himalayan, bodish, koreanic, japanese_group)

**Recommendation: collapse to a single low uniform cap, no sub-group exceptions.**

| Category | Cap | Why |
|---|---|---|
| Military | L0 only | Firearms/gunpowder/shipbuilding were universal baseline knowledge (matchlocks in Japan/Korea/SE Asia since 16th c., Mughal-successor artillery corps, Siamese/Burmese/Vietnamese court arsenals) but L1's "permanent_army"/cannons and L2's bombard_cannons aren't universal across this very diverse bloc. |
| Oratory | L1 only | Central bureaucracies existed everywhere (Tokugawa bakufu, Joseon Six Ministries, Mughal-successor diwani, SE Asian court administrations) but L2 (urban_planning/standardised_writing/chancery) isn't universal for smaller Himalayan/mainland-SE-Asian polities. |
| Civic | L1 only | Universal pre-industrial baseline; L2 implies industrial-adjacent infrastructure not general across the bloc. |
| Religious | L1 | Confucian/Buddhist/Islamicate/Hindu scholarly+astronomical traditions were mature everywhere. |
| `tech_rocket_artillery` | **Drop from the uniform grant** | Best-fit case (Mysore under Hyder Ali/Tipu Sultan) is 1770s-90s — premature even for its strongest example; every other bloc member has no comparable tradition at 1763. |

Sub-group exceptions considered and **rejected** (not worth the added culture-group-list
complexity): dravidian-only rocket_artillery (still premature by 10-20 yrs even narrowed to
Mysore), japanese_group literacy/administration bonus (no matching tech exists in the
current tree to grant), koreanic (already covered by the L1 floor).

### Qing (c:CHI) — first pass, needs the dedicated deeper second pass the user asked for

First-pass verdict (audit fork bundled with the tradezone catch-all — **user wants CHI
fully separated from this and re-run on its own with more scrutiny**):

| Category | Verdict | Why |
|---|---|---|
| Military L0-1 (weapon_manufacturing, firearms, shipyards, permanent_army, field_ambulances, warships, cannons) | Keep | Eight Banners (八旗) + Green Standard (綠營) — arguably the largest standing army on earth in 1763. Jesuit-cast bronze artillery (17th-c. Verbiest guns) genuinely existed. |
| Military L2 (bombard_cannons) | Keep excluded — RATIONALE CORRECTED | Excluded, but NOT on "already stagnated by 1763" grounds — an academic dive (Andrade, *The Gunpowder Age*, Princeton UP 2016) shows that framing is chronologically backwards: stagnation is a process whose ONSET Andrade dates to the "Great Qing Peace" of 1760-1839, so 1763 is its leading edge, not its result. The earlier "reproducing 17th-c. Verbiest designs, nothing since" implication is also CONTRADICTED — Jesuit cannon work continued to the eve of 1763 (Félix da Rocha, court cannon-maker, Jinchuan 1747-49 and Zunghar campaigns 1755-59; Needham *SCC* Vol.5 Pt.7, Cambridge UP; Entenmann, *Hmong Studies Journal*). Correct basis for withholding the heavy-siege tier: Qing used LIGHTER cannon by deliberate doctrine (earthen-core walls absorb shot better than European stone; heavy siege trains are useless against steppe cavalry) — a rational adaptation, not neglect. Conclusion (no bombard_cannons) stands; the rationale is now doctrine, not stagnation. |
| `tech_rocket_artillery` | Keep (mild) | Chinese/Ming-Qing gunpowder rocket arrows (火箭) have deep pedigree; Ten Great Campaigns used rocket volleys. Slightly gamey but defensible; low priority to remove. |
| Oratory L1-2 | Keep — "strongest fit in the whole grant" | Qing bureaucracy, Grand Council (軍機處), standardized Hanzi, Board of Revenue monetary management, archival tradition (檔案). Audit suggests CHI should arguably be a **leader** here, on par with or ahead of Europe. |
| `tech_census`, `tech_postal_administration` | Keep | 保甲 registration + 1741+ population counts; 驛站 courier-relay network. Ancient, well-justified. |
| Civic L1 | Keep | Baseline. |
| Civic L2 block | **Do NOT grant the whole block** — cherry-pick `tech_artificial_canals` only | Grand Canal (大運河) + Qing hydraulic engineering (河工) justify canal tech specifically, but gear_systems/templating/mining_rails imply proto-industrial mechanization Qing did not have — granting the whole L2 block is a false-equivalence trap. |
| Religious L2 (national_epic, theatre) | **Add** | China's classical canon (紅樓夢/Dream of the Red Chamber completed ~1763!), mature theatrical tradition (kunqu 崑曲). Well-earned. |
| Religious L3 | Keep excluded | Correctly excluded — that's the European Scientific Revolution package. |

Cross-bloc note from the audit: if the other blocs get capped as recommended above, sanity-
check that CHI ends up **out-bureaucracying Europe but lagging it in mechanization/heavy
artillery** — that relative positioning is the point, not just an absolute tier number.

**What the user wants for the second pass, specifically:**
- Treat CHI entirely on its own terms — no shared audit task, no bundling with the
  tradezone catch-all or any other bloc.
- Apply deeper scrutiny than the first pass. Candidate angles the second pass should dig
  into once web access is back: verify the exact 1763 status of Qing artillery technology
  transfer (Jesuit missionaries at court, e.g. the reign of Kangxi/Yongzheng vs. Qianlong-
  era stagnation — get real dates, not "17th century" hand-waving); verify whether a
  civic/administrative tech beyond canals is defensible (Qing fiscal administration —
  地丁銀 land-poll tax, 常平倉 ever-normal granary system as *state economic
  administration* rather than just the building already modeled); check whether the
  existing CHI-only grants in `se_TEST.txt` interact correctly with the rest of the mod's
  Qing-specific systems already built this session (Grand Council, Ministry of Revenue,
  Industrialisation/civilization_value seeding) rather than being decided in isolation.
- Consult real academic sources once web access is available (e.g. sourced military/
  economic histories of the Qianlong era, not just trained-knowledge recall) before
  finalizing CHI's tier list.

## Remaining steps (in order)

1. **Resume/re-run the interrupted GBR/FRA-individual audit** (`a432409195b268c0a`) —
   confirm before assuming every individually-listed tech should be dropped.
2. **Run the dedicated, deeper, CHI-only second pass** — separate from every other bloc,
   with web-sourced verification once available.
3. **Synthesize all audits into a concrete edit plan** for `se_TEST.txt`'s 1763 `else`
   branch: per-bloc tier caps, explicit within-tier exceptions (e.g. Western Europe's
   banking trio for GBR/NED/Sweden/FRA/German only), explicit drops (all TUR individuals,
   all GBR/FRA/NED/USA/german individuals pending step 1, Ottoman naval_explosives/
   carronade), and the CHI-specific cherry-picks (artificial_canals only from civic L2,
   add religious L2). Decide the open design question on whether Western Europe needs a
   leader/laggard OR-list split or a single uniform cap.
4. **Adversarial review** of that synthesized design (the user's explicit next step) —
   dispatch a skeptical review pass against the concrete tier/exception list, not just
   the individual bloc audits in isolation, checking for internal consistency (e.g. does
   CHI actually end up more bureaucratically advanced than Europe but less industrially
   advanced, as intended cross-bloc?).
5. **Implement** the reviewed design into `se_TEST.txt`'s 1763 branch, replacing the
   current uniform-heuristic cap.
6. **Verify**: brace-balance check (`python3 -c "...count('{')/count('}')..."`, the
   pattern already used this session), and ideally a boot test to confirm no invention-ID
   typos or scope errors were introduced.

## Files touched so far this session (for context after model switch)

- `common/scripted_effects/se_TEST.txt` — date gate + first-pass uniform-cap 1763 branch +
  2 typo fixes. **This will be edited again** once the real per-bloc design (step 3-5
  above) replaces the uniform cap.
