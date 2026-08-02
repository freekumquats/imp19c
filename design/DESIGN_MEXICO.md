# Design Plan — "La República Inestable": Mexico 1815–1867, Independence → Reforma → the Second Empire

**Status:** proposed (design; implementation to follow this doc)
**Feature id:** #96 (Mexico domestic arc) + #69-refactor (hook the Qing "Mexican Adventure" colonization tree into this)
**Author scope:** net-new Mexico subsystem that OWNS the Mexican political-instability arc, its state, and its
climax (the French Intervention → the Second Mexican Empire under Maximilian). The existing Qing #69 Mexico
colonization tasks (`qing_col_veracruz` / `qing_col_maximilian` / `qing_col_mexican_empire`) are refactored to
HOOK INTO this, not the other way around.

---

## 0. Guiding principle — coupling direction (per user directive)

> "Qing intervention in Mexico will then hook into Mexican content." + "follow the same implementation policy
> where the AI will control Mexico."

**The Mexico subsystem is the source of truth.** It owns:
- the political-instability state (on `c:MEX`),
- the Conservative↔Liberal polarization and the coup/pronunciamiento cycle,
- the foreign-debt meter that TRIGGERS the European intervention,
- the concrete climax: the French Intervention war and the released/installed Second Mexican Empire,
- the canonical signals "the Cession has been lost", "Mexico has defaulted", "an Emperor sits in Mexico City".

**The Qing #69 arc becomes a consumer / participant.** After this build, the Qing "Mexican Adventure"
(`qing_col_maximilian`) reacts to a Second Empire this arc has already put in motion (or joins the anti-French
Juarista coalition), rather than conjuring the Habsburg throne unilaterally. This is a CHANGE to shipped code
(#69) and gets heightened behavioural-equivalence scrutiny (fix-traceability rule).

**AI-autonomous by construction.** The player is almost always the Qing, so the Mexico arc must advance and
resolve with Mexico under AI control — the identical policy applied to #93 (USA) and #94 (Japan). Everything
decisive is pulse-driven (`MEX_instability_pulse`) or in event `immediate` blocks; player options only
*modulate*. No beat depends on a human choosing.

**US coupling (the other new subsystem).** The US arc (#93) already references "the Cession territory arrives
from the Mexico arc (#96)" at `usa_section.4`. This arc OWNS the 1848 Cession as a concrete territorial
transfer MEX→USA, and the French Intervention is gated on the US Civil War (the Monroe Doctrine cannot be
enforced against France until the Union wins in 1865 — so an early Union collapse *helps* Maximilian, and a
Union victory dooms him). This is the concrete US↔Mexico linkage the user asked for.

---

## 1. Historical spine (sourced digest)

Historiography: Meyer, Sherman & Deeds, *The Course of Mexican History*; Krauze, *Mexico: Biography of Power*
(1997); Bazant, *A Concise History of Mexico*; Hamnett, *Juárez* (1994); on the intervention, Cunningham,
*Mexico and the Foreign Policy of Napoleon III*; on the US linkage, Schoonover, *Dollars over Dominion*
(French/US/Mexican triangle). (Digest cross-checked against the researcher's return; see §9.)

| Date | Beat | Why it matters to the meter |
|------|------|------------------------------|
| 1821 | Treaty of Córdoba; Iturbide's Plan de Iguala ends the War of Independence | Independence born already split: monarchist vs republican |
| 1822–23 | First Mexican Empire (Iturbide crowned, then falls) | The monarchy option is *native* to Mexico, not a French import |
| 1824 | Federalist Constitution; first republic | Federalist (Liberal) vs Centralist (Conservative) — the master fault line |
| 1833–55 | Santa Anna's serial presidencies (≈11 turns in/out of power) | The praetorian-caudillo cycle; central authority never consolidates |
| 1835–36 | *Siete Leyes* — the Centralist constitution | Triggers regional revolts (Texas, Yucatán, Zacatecas) |
| 1836 | Texas secedes (Alamo, San Jacinto) | First great territorial amputation; prelude to US threat |
| 1838 | The Pastry War (France blockades Veracruz over debts) | Rehearsal for 1862: French guns at Veracruz over *debt* |
| 1846–48 | Mexican–American War; Treaty of Guadalupe Hidalgo | **The Cession**: CA/NV/UT/AZ/NM + parts of CO/WY lost; national trauma |
| 1848–1901 | Caste War of Yucatán (Maya rising) | Indigenous unrest as a permanent structural drain |
| 1853 | Gadsden Purchase (La Mesilla sold to the US) | Santa Anna sells more land; the last straw |
| 1854 | Ayutla Revolution (Álvarez, Comonfort) overthrows Santa Anna | Liberals seize the initiative; La Reforma begins |
| 1855–57 | *Ley Juárez*, *Ley Lerdo* (disentail Church lands), *Ley Iglesias*; 1857 Constitution | Church privilege attacked head-on → Conservative backlash |
| 1857–60 | War of the Reform (two rival governments: Juárez vs Miramón) | The polarization boils over into open civil war |
| 1861 | Juárez wins; suspends foreign-debt payments (July) | **The intervention trigger**: Britain/Spain/France land at Veracruz |
| 1862 | Cinco de Mayo — Zaragoza beats the French at Puebla | Britain/Spain withdraw; France stays and escalates |
| 1863 | French take Mexico City; Juárez flees north | The Republic reduced to a government-in-exile |
| 1864 | Maximilian von Habsburg crowned Emperor (Second Mexican Empire) | The concrete climax: a European throne in the Americas |
| 1865 | US Civil War ends → US pressure + arms to Juárez; France told to leave | **The US coupling fires**: Monroe Doctrine re-armed |
| 1867 | French withdraw; Maximilian executed at Querétaro; Republic restored | Resolution: the Empire falls, or (alt-history) survives with a foreign patron |

**Design thesis:** Mexican instability 1815–67 is *structural*, not accidental — a weak centre, a praetorian
army, an entrenched Church, chronic bankruptcy, and a predatory northern neighbour. That makes an
AI-autonomous, meter-driven, branching arc historically honest: the same forces reliably push toward
default → intervention → a monarchy, but the *timing* and *survival* of that monarchy are genuinely contingent
(on the US Civil War, on a foreign patron like the Qing #69 arc).

---

## 2. State model (on `c:MEX`) — the AI/summary layer

Five 0..100 counters (the `USA_section` idiom: counters are the AI/summary layer; every threshold hangs a real
on-map object). Seeded by `MEX_instability_init`, idempotent, self-healing on first pulse.

| Variable | Meaning | Start | Concrete object hung off it |
|----------|---------|-------|------------------------------|
| `mex_instability` | master road-to-collapse meter (coup/pronunciamiento pressure) | 30 | band modifier + a spawned *pronunciado* general on the high band |
| `mex_conservative` | Conservative/Centralist/Church-party strength | 45 | spawns a named Conservative (Alamán → Miramón) |
| `mex_liberal` | Liberal/Federalist/anticlerical strength | 40 | spawns a named Liberal (Juárez, Ocampo, Zaragoza) |
| `mex_church_privilege` | wealth & political power of the Church (disentailment lowers it) | 70 | band modifier (fiscal drag vs Liberal tax base) |
| `mex_foreign_debt` | accumulated foreign debt (drifts up; ≥ threshold → default → intervention) | 40 | **the intervention trigger**: European fleet + French war |

Plus legible markers (not clamped meters), mirroring `usa_slave_states`:
- `mex_territory_lost` (count: Texas, Cession, Gadsden) — legible amputation tally.
- `mex_pronunciado_count` (flooding cap 4 on spawned generals).
- once-only milestone/beat guards (`mex_beat_*`, `mex_milestone_*`, `mex_defaulted`, `mex_empire_installed`).

Bands on `mex_instability` (remove-all-then-add-one, `QING_DECLINE` idiom):
- `< 40` **estable** (calm) — small tax/stability bonus.
- `40–69` **inquieta** (restive) — unrest + maintenance drag.
- `≥ 70` **anarquía** (praetorian chaos) — heavy unrest, coup pressure, invites intervention.

---

## 3. Concrete objects (the CONCRETE-OVER-ABSTRACT rule)

Every meter threshold and every dated beat hangs a **real on-map object**:

1. **Named historical characters** (the `se_USA_ROSTER` / `se_QING_ROSTER` idiom — `create_character`, no name
   arg, identity via `add_nickname` + event text, once-guarded, explicit culture/religion/age). Roster:
   - **Conservatives:** Agustín de Iturbide (the native-monarchy precedent), Lucas Alamán (ideologue),
     Antonio López de Santa Anna (the opportunist caudillo — spans both), Miguel Miramón (Reform-War general).
   - **Liberals:** Benito Juárez (culture *zapotec* — the historically correct indigenous origin), Melchor
     Ocampo (ideologue), Ignacio Zaragoza (the Puebla victor), Porfirio Díaz (young general), Sebastián Lerdo
     de Tejada, Juan Álvarez (Ayutla caudillo).
   - **The Empire:** Maximilian I von Habsburg (culture *austrian*/German, spawned at the climax).
2. **Territory as real provinces** — the Cession is an actual MEX→USA province transfer (Northern_Mexico + the
   Cession-region provinces), not a counter tick. Texas secession is a real release. Veracruz (p:2069) is a
   real intervention beach-head.
3. **A released/installed country at the climax** — the Second Mexican Empire is a concrete government change
   (or a released client state), fought over in a real French Intervention war, carried cross-arc via a GLOBAL
   variable `mex_empire_country` (the oracle-confirmed cross-event handle, exactly as `usa_csa_country`).
4. **Provinces in open unrest** — the Caste War of Yucatán flips a real Eastern_Mexico (Yucatan/Quintana_Roo)
   province into a `mex_caste_war` province modifier (the `USA_flip_border_state` idiom).

---

## 4. The autonomous driver — `MEX_instability_pulse`

Monthly for `c:MEX`, self-gated on `tag = MEX` (NEVER `is_ai` — the whole point), throttled ~quarterly via a
cooldown var. Mirrors `USA_section_pulse` exactly:

1. **Era pressure** — a gentle date-keyed drift so an AI Mexico reliably reaches its climaxes even if some
   dated beats edge-cased out:
   - after 1830: `mex_instability` and `mex_foreign_debt` trend up (the caudillo era).
   - after 1855: `mex_conservative` vs `mex_liberal` polarize (La Reforma).
   - after 1858: `mex_foreign_debt` climbs steeply toward the default threshold.
2. **Bands** — re-apply the `mex_instability` economic band.
3. **Milestones** — hang concrete objects: high `mex_conservative` → spawn a Conservative; high `mex_liberal` →
   spawn a Liberal; high `mex_instability` → spawn a *pronunciado* general (coup risk); Caste-War flip.
4. **Climax checks** (once each):
   - `MEX_default_check` — `mex_foreign_debt ≥ 80` **OR** `current_date >= 1861.7.1` → suspend payments,
     fire the intervention.
   - `MEX_intervention_check` — post-default, the French escalate; gated on the **US Civil War state**
     (checks `usa_seceded` / whether the Union is intact) for the Monroe-Doctrine coupling.
   - `MEX_empire_check` — French ascendant → install/release the Second Mexican Empire (spawn Maximilian).
   - `MEX_empire_fall_check` — US Civil War over (Union won) **OR** date ≥ 1867 → US pressure + the Republic's
     resurgence topple the Empire, UNLESS a foreign patron (the Qing #69 arc) is propping it up.

---

## 5. Dated beats (`mex_instability.1 … .N`) — the flavour + big nudges

Seeded from `mex_instability_on_actions.txt` `on_game_initialized` for `tag = MEX`, NO `is_ai` guard (the
`usa_section` idiom: day offsets from the 1815.7.1 START_DATE, each event re-checks its own not-done guard).

| Event | Date | Beat | Concrete effect |
|-------|------|------|-----------------|
| `.1` | 1822 | Iturbide's First Empire | spawn Iturbide; a monarchy precedent set (small `mex_conservative`) |
| `.2` | 1824 | The Federalist Constitution | spawn Alamán (Conservative) vs a Liberal; polarization seeded |
| `.3` | 1833 | Santa Anna's era begins | spawn Santa Anna; `mex_instability` up |
| `.4` | 1836 | Texas secedes | **real release** of the Texas province(s) as an independent/USA-bound state; `mex_territory_lost++`, big instability spike |
| `.5` | 1838 | The Pastry War | French debt-blockade of Veracruz; `mex_foreign_debt` up (the rehearsal) |
| `.6` | 1846–48 | The Mexican–American War & the Cession | **real MEX→USA province transfer** (fires `usa_section.4` receipt); `mex_territory_lost++`, trauma spike |
| `.7` | 1853 | The Gadsden Purchase | more land sold; Santa Anna discredited → sets up Ayutla |
| `.8` | 1854 | The Ayutla Revolution | Santa Anna overthrown; `mex_liberal` surges; spawn Juárez/Álvarez |
| `.9` | 1855–57 | La Reforma & the 1857 Constitution | disentailment: `mex_church_privilege` drops hard; Conservative backlash (`mex_conservative` up) |
| `.10` | 1857–60 | The War of the Reform | the polarization → civil war (a `start_civil_war` or heavy unrest); spawn Miramón |
| `.11` | 1861 | Default & the intervention | fires `MEX_default_check` deterministically |
| `.12` | 1862–64 | Cinco de Mayo → Maximilian | the French climax; fires `MEX_empire_check`; **notifies the Qing #69 arc** (the inversion hook) |

`.10`/`.11`/`.12` are also reachable via the pulse's checks, so the climax is guaranteed for an AI Mexico even
if a beat is skipped (the `usa_section.12` belt-and-braces convention).

---

## 6. The climax — the French Intervention & the Second Mexican Empire (concrete)

`MEX_install_empire` (the `USA_release_confederacy` twin, relocating the #69 throne logic into Mexico
ownership):
- gather Mexico's core provinces (Pacific_Mexico incl. Mexico City p:8516, Eastern_Mexico, Northern_Mexico).
- **Path A — government change in place:** `change_government = imperial_monarchy` on `c:MEX`, spawn Maximilian
  as ruler, rename to the Second Mexican Empire (cosmetic `change_country_name`/`_adjective`). Cleanest: keeps
  one Mexican country on the map, flips its regime — the historical reality (Maximilian ruled the *same* state).
- **Path B — released client (if the Republic survives in the north):** release the French-held core as the
  Empire, leaving Juárez's Republic as a rump — models the 1863–67 split (two governments). Carried via
  `set_global_variable = { name = mex_empire_country … }`.
- either way: declare/represent the French Intervention war; France is the patron.
- **The US coupling:** the Empire's survival is checked against the US Civil War state each pulse
  (`MEX_empire_fall_check`) — Union victory ⇒ US pressure topples it (1867 Querétaro); Union collapse or a
  foreign patron ⇒ it survives (alt-history).

---

## 7. Coupling refactor — the Qing #69 "Mexican Adventure" becomes a consumer (CHANGE to shipped code)

Current #69 (`common/missions/qing_colonization_missions.txt`):
- `qing_col_veracruz` — provokes France at Veracruz p:2069, `QING_gp_frontier_play` vs FRA.
- `qing_col_maximilian` — the fork: with Napoleon-at-court → Franco-Qing condominium props Maximilian;
  without → solo Qing grab; either way betrays the Daoguang entente (USA affronted).
- `qing_col_mexican_empire` — releases the four Mexican regions as a Qing client Empire.

**Refactor (behavioural-equivalence-scrutinized):**
- These tasks now *reference the Mexico arc's state* rather than acting in a vacuum. `qing_col_maximilian`
  checks `global_var:mex_empire_country` / `MEX has mex_empire_installed`: if the Second Empire already exists,
  the Qing task JOINS/props it (patron → `MEX_empire_fall_check` reads a `mex_foreign_patron` flag that keeps it
  alive past 1867 — the alt-history divergence the #69 arc is *for*); if not yet, the Qing task can *accelerate*
  the arc (nudge `mex_foreign_debt` / trigger `mex_instability.12`).
- The Qing #69 release of a client Empire (`qing_col_mexican_empire`) is preserved but reconciled so it does not
  double-release against the Mexico arc's own Empire (guard on `mex_empire_installed` / the global var).
- The Mexico arc's `.12` beat NOTIFIES a human Qing (if `c:CHI` human + the #69 arc is in play) so the Qing
  court reacts to a Maximilian this arc set in motion — the exact `usa_section.12 → qing_uscw.1` inversion
  pattern.
- **No new Qing state is invented**; the #69 tasks only *read* the Mexico arc and set at most one patron flag.

---

## 8. File plan (mirrors #93/#94 exactly)

New files:
- `common/scripted_effects/se_MEXICO.txt` (no-BOM/LF) — init, nudge, bands, spawn-general, Caste-War flip,
  milestone/default/intervention/empire/empire-fall checks, `MEX_install_empire`, the pulse.
- `common/scripted_effects/se_MEXICO_ROSTER.txt` (no-BOM/LF) — the ~11 named figures (Iturbide, Alamán, Santa
  Anna, Juárez, Ocampo, Zaragoza, Díaz, Lerdo, Álvarez, Miramón, Maximilian), `MEX_roster_finalize` shared tail.
- `events/imp19c_mod_events/mex_instability_events.txt` (BOM/LF) — beats `.1–.12`.
- `common/modifiers/mex_instability_modifiers.txt` (no-BOM/LF) — the three bands + Church + Caste-War +
  intervention modifiers.
- `common/on_action/mex_instability_on_actions.txt` (BOM/LF) — `on_game_initialized` seed + dated beats +
  `mex_instability_pulse_on_action`.
- `localization/english/mex_instability_l_english.yml` (BOM/LF) — beats, bands, nicknames, Empire name/adj.

Edits (CHANGE to shipped code — heightened scrutiny + traceability):
- `common/on_action/00_monthly_country.txt` — register `mex_instability_pulse_on_action`.
- `common/missions/qing_colonization_missions.txt` — the §7 consumer refactor of the three Mexico tasks.
- `events/imp19c_mod_events/usa_section_events.txt` (`usa_section.4`) — wire the Cession as an actual transfer
  originating here (the US beat already documents the dependency; make it concrete).
- `localization/english/qing_colonization_l_english.yml` — reconcile any wording touched by the refactor.

Every new scripted_effect wired to `se_LOG` (LOG_enter/exit/line + LOG_fail on guard-miss, `sys = MEX`), per
the standing error-logging rule. Fix-traceability comments (`#96`) on every change to shipped code.

---

## 9. Engine feasibility (verified in-repo / oracle-backed)

- **AI-autonomous pulse** — `monthly_country_pulse` runs its effect for AI countries (self-gate on tag, never
  `is_ai`); proven by the shipped CHI blocks and now the #93 USA / #94 Japan pulses. ✔
- **`change_government` / `change_country_name` / `change_country_adjective`** — used in-repo (Japan #94 Meiji
  formation, Qing government changes). ✔
- **`LAND_release_from_list` + `reconquest_wargoal` + `FUNC_declare_war_with_wargoal_province`** — AI-prosecuted,
  proven by SEPARATISM and reused in #93. ✔
- **Cross-event/cross-country handoff via `set_global_variable`** — the `usa_csa_country` idiom. ✔
- **Named-character spawn** — `se_USA_ROSTER` / `se_QING_ROSTER` idiom (nickname-pinned, once-guarded, explicit
  culture/religion/age). Juárez culture = `zapotec` (present in MEX poptype_rights); Maximilian = an
  Austrian/German culture (verify exact key at build). ✔ (culture key to confirm)
- **MEX facts:** tag MEX = `revolutionary_republic`, primary_culture `mexican`, catholic, capital p:1809;
  key provinces Veracruz p:2069, Mexico City p:8516, Acapulco p:1800; regions Northern_Mexico / Eastern_Mexico /
  Central_America / Pacific_Mexico; neighbours FRA/GBR/SPA/AUS/USA all present (Austria = AUS; no separate HAB).
  Protectorate loc keys `qing_protectorate_mexico_name/adj` already defined by #69. ✔

**Open items to confirm at build:** (a) Maximilian's culture key; (b) whether a real Texas release target
already exists or should be a dynamic release; (c) the exact Cession province set (which Northern_Mexico +
adjacent provinces map to CA/NV/UT/AZ/NM) — read from the map at build; (d) the `start_civil_war` vs unrest
choice for the War of the Reform.

---

## 10. Research confirmation (digest returned — corrections folded in)

The Mexican-history research agent's digest CONFIRMS the §1 spine (dates, figures, the US-Civil-War hinge) and
adds three build-relevant refinements:

- **Plausibility root of the Qing coupling (the digest's key finding).** The *real* documented Qing–Mexico ties
  are exactly two, and both are already the theme of the #69 arc: (1) the **Manila Galleon (Acapulco↔Manila)
  ran for 250 years and its LAST voyage was 1815 — the game's start year**, a living-memory link just ending;
  (2) **Mexican silver pesos were the de-facto currency of the China trade**, circulating heavily in the Qing
  economy. Large Chinese migration to NW Mexico is post-1870 (out of window), so a 1860s Qing intervention is
  honest alt-history whose plausibility rests on *silver + the galleon memory*, not a real presence. The #69
  refactor (§7) should lean on this framing, not invent a fictitious diaspora.
- **The Qing Pacific beach-head = Guaymas / Mazatlán / Manzanillo / San Blas** (NW Pacific ports, French-
  blockaded during the intervention; Guaymas was a filibuster target). These are the concrete ports a Pacific
  Qing would land at — matching the user's "Guaymas port" note. Acapulco (p:1800, the galleon terminus) is
  already the #69 anchor.
- **Roster confirmations/additions.** Juárez = culture `zapotec` (Oaxacan, confirmed). Worthwhile extra named
  figures the digest surfaces: **Guadalupe Victoria** (first republican president), **Ignacio Comonfort**
  (the constitution-betrayer whose Plan de Tacubaya *ignites* the Reform War — a strong beat character),
  **Leonardo Márquez** / **Tomás Mejía** (Conservative generals executed with Maximilian at Querétaro),
  **Empress Carlota**. Foreign principals for event text (not spawned): Napoleon III, Bazaine, Polk.

**Branching points (digest §5) mapped to our beats:** the digest's 8 turning points map cleanly onto the §5
dated beats — independence's monarchist nature (.1), federalism-vs-centralism causing Texas secession (.4),
San Jacinto (.4), the 1846 war terms (.6), the Gadsden sale (.7), Comonfort's betrayal igniting the Reform War
(.10), the 1861 default (.11), and French escalation + the crown (.12) — with the Qing intervention window
(1861–65, during US paralysis) as the natural insertion point at .12. No change to the beat plan required.
