# Design: Refactor Qing systems to build ON TOP of vanilla, not beside it

Status: DESIGN / for review. No code changed by this document.
Author basis: four read-only coupling-maps (2026-07-19) of marriage/succession/regency,
justice/censorate/Grand-Council/offices, stability/politics/subjects, plus a full
classification of the zeroed vanilla event files. Every verdict below cites what the maps
actually found; where a claim is unverified it says so.

---

## 0. The governing question (read this first)

The user's ask: "Qing systems should build ON TOP of the existing [vanilla] ones instead of
being separate standalone."

The maps show the answer is **conditional on whether the vanilla mechanic is actually LIVE
in this total-conversion**. A Qing parallel is only "gratuitous" (a refactor target) if the
vanilla mechanic it shadows is present and usable. Where the TC has **removed, disabled, or
reserved-for-others** the vanilla mechanic, the Qing layer is a **necessary replacement**,
not a parallel to collapse.

So the doc's spine is a triage, per subsystem:

- **LAYERED-WELL** — already reads/writes the live vanilla value; keep, just document the seam.
- **NECESSARY-PARALLEL** — vanilla mechanic is absent/disabled/reserved; the bespoke system
  is justified. Do NOT collapse it; optionally strengthen the vanilla read-points it *can* use.
- **REFACTOR-TARGET** — vanilla is live and the Qing layer needlessly shadows it, OR the Qing
  layer runs independently of a live vanilla mechanic and they double up (correctness risk).

The single most important finding: **most Qing subsystems are already LAYERED-WELL or
NECESSARY-PARALLEL.** The genuine refactor work is narrow — a few doubling-up hazards and a
few underused vanilla read-points — not a wholesale rebuild.

---

## 1. Per-subsystem triage (grounded in the maps)

### 1a. Stability & Tyranny — LAYERED-WELL (no refactor needed)
Vanilla `stability` / `tyranny` / `aggressive_expansion` are **fully available** (defined in
`common/defines/00_defines.txt`; governments carry `monthly_tyranny`). Every Qing mechanic
already writes to the vanilla values directly — `add_stability` / `add_tyranny` /
`add_aggressive_expansion` appear across se_QING_JUSTICE, se_QING_WORKS, se_QING_WAR,
se_SUBJECT_QING, politics_events, etc. The `tyranny_and_stability_events/` folder is
**stubs only** — no bespoke meter was ever built. This is the model the rest should imitate.
**Action: none, beyond a one-line "layered on vanilla stability/tyranny" comment.**

### 1b. Marriage — LAYERED-WELL (minor, oracle-gated polish)
The core wedding is vanilla `marry_character`; unions are vanilla `royal_union` via
`FUNC_make_subject`; death/inheritance hangs off the `on_character_death` on_action. Custom
vars (`marriage_partners`, `betrothed_to_char`, `marriage_bridge_partners`,
`royal_marriage_entente`) **augment** vanilla rather than shadow it, each for a reason vanilla
can't cover (multi-realm bonds; betrothal is oracle-unproven in I:R; cross-faith dispensation;
the great-power-can't-ally engine restriction).
**Actions (both oracle-gated, low priority):**
- If vanilla `royal_union` auto-inherits land on junior extinction, drop the manual
  `LAND_transfer_provinces` (se_MARRIAGE.txt) to avoid a double land-transfer. VERIFY first.
- There is no `on_marriage` on_action in I:R (unverified but consistent with the code never
  referencing one), so the death-time hook is correct; do not "move flavor to on_marriage."

### 1c. Succession (秘密立儲 seal) — NECESSARY-PARALLEL + one real doubling-up (BT-Q)
Layered part: the seal is enforced by vanilla `nominated_heir_modifier` + `recalc_succession`
— correct. Parallel part: the **prince-backing contest** (`qing_prince_backing` meter, faction
jockeying, 九子奪嫡) has no vanilla equivalent (vanilla has an heir *pointer*, not an heir
*contest*), so it's justified.
**The doubling-up (this is BT-Q, and it's a correctness bug, not cosmetics):** vanilla
`recalc_succession` fires on its own triggers (birth, trait change, marriage) and can run
*after* the Qing seal, potentially overwriting the sealed heir. Current mitigation is
"call recalc immediately after sealing" — best-effort, not airtight.
**Actions:**
- **Primary:** guard against post-seal vanilla recalc. If an `on_recalc_succession`-style hook
  exists, suppress/re-assert the sealed heir there; if not, re-assert the seal on the
  birth/death on_actions that can trigger a recalc. (Oracle-gate the hook's existence.)
- **Secondary (event-driven roster):** move `QING_princes_recompute_roster` off the quarterly
  poll onto `on_birth` / `on_character_death` (ruling family, CHI), keeping the pulse only for
  backing *drift*. Closer to vanilla's reactive model; fewer stale rosters.

### 1d. Regency — NECESSARY-PARALLEL (vanilla `regent` unproven in base I:R)
Reads vanilla minority/incapacity gates (`is_adult`, `has_trait = incapable`, `age`) — good.
But the regent *scope*/`set_regent` is Invictus-only per prior notes, **unproven in base
I:R**, so the custom `qing_office_regent_holder` storage + picker + hand-back drama is
justified, not gratuitous.
**Actions:**
- Oracle-gate: does base I:R (not just Invictus) expose a `regent` scope + `set_regent`? If
  yes, store the regent there (vanilla UI/tooltips light up for free) and keep Qing flavor on
  top. If no, keep custom.
- Fire regency evaluation on `on_ruler_change` for instant onset at a child-emperor accession,
  keeping a lighter pulse for the mid-reign recovery check.

### 1e. Justice / Censorate — NECESSARY-PARALLEL (docket + surveillance have no vanilla form)
Already uses vanilla `imprison` for convictions, plus `add_loyalty` / `add_tyranny` /
`corruption` / `add_popularity` throughout — genuinely layered. The bespoke parts —
a **persistent docket** (`qing_justice_accused`, an accusable roster, strip-office-on-charge)
and a **surveillance/impeachment body** (都察院) — have no vanilla equivalent (vanilla
`hold_trial` is instant, fire-and-forget; there is no proactive-impeachment office).
**Action:** keep bespoke; document the vanilla seam. Optional: surface vanilla `prisoner = yes`
state (already set via `imprison`) as a GUI indicator on a jailed official's card.

### 1f. Grand Council / Offices — NECESSARY-PARALLEL (vanilla offices reserved-for-others)
Vanilla monarchy offices EXIST (8 generic European slots: marshal/steward/…) but the Qing
system **deliberately excludes** vanilla office-holders from candidacy
(se_QING_COUNCIL.txt:201-208) — reserving vanilla offices for European/American AI while Qing
models its own 13 semantically-specific boards (六部/理藩院/總理衙門/軍機處). The
effectiveness meter (skill-per-office, 滿漢 balance, harmony/faction/officer-corps couplings)
is a derived governance system far beyond vanilla's flat office bonuses. Already reads/writes
vanilla `power_base` / `add_loyal_veterans` / `prominence` and respects vanilla
`has_office`/`is_general`/`is_admiral`/`is_governor` exclusions.
**Action (the one genuinely new build-on-top idea worth considering):**
- **Shadow the Qing office into a vanilla office slot** (e.g. War minister → also
  `give_office = office_marshal`), stripped symmetrically on vacate, with the Qing vars
  remaining source-of-truth. Benefit: external AI/diplomacy/character-UI see "CHI's minister."
  **Risk:** vanilla office side-effects/events may fire — must boot-test in isolation before
  committing. Treat as an experiment, not a given.

### 1g. Factions (conservative/reformist) — NECESSARY-PARALLEL (vanilla monarchy parties disabled)
Vanilla parties are **republic-only**; the two monarchy factions
(`traditionalist_faction`/`reformist_faction`) are **disabled stubs** (`allow = { always = no }`).
The Qing per-character stance layer (`qing_char_stance`, `qing_council_reform_lean`,
polarization → gridlock penalty) fills that void and needs per-character granularity vanilla
never offered. **Action: keep; add a comment stating it is NOT the vanilla party system.**

### 1h. Subjects / Tributaries — LAYERED-WELL foundation + underused vanilla read-points
Built ON vanilla subject types (`is_subject_type`, `make_subject` via `FUNC_make_subject`,
the ladder is just a convenience var). The bespoke part — a stateful 0..5
`SUBJ_integration_progress` arc with historical reaction events (改土歸流, White Lotus, Three
Feudatories) — is justified because vanilla `can_be_integrated` is a silent UI-only flag with
no process/events.
**Actions (genuine build-on-top, low risk, high fit):**
- Read vanilla `loyalty_to_overlord` (already defined on some subject types) to weight
  integration reaction-event selection (loyal → positive; disloyal → unrest).
- Factor the vanilla `integrate_speed` modifier into the `SUBJ_integration_progress` step rate.
- Use `can_be_integrated = yes` as the entry gate instead of hardcoding
  `is_subject_type = autonomous_governorship`, so new subject types auto-slot in.

### 1i. Pop political support — ORPHANED (decide, then wire or remove)
`se_POLITICS.txt` computes `country_reactionary/conservative/liberal_support` from pop tallies,
reads vanilla `stability` — but the output is consumed only by one `POLITICS_test_election`
stub. It's currently dead-end scaffolding (same failure class as the marriage sort/filter
cluster just removed).
**Action (needs a design decision):** either (a) wire it to the Qing faction layer (pop
leanings pressure Grand Council stances), (b) reserve it for a future constitutional-monarchy
reform path and wire to vanilla `add_party_conviction` when that government is adopted, or
(c) remove it as dead scaffolding. Do not leave it computed-but-unconsumed.

---

## 2. The zeroed-event question (why "reuse the appropriate ones" mostly resolves to "already done")

The ~130 zeroed vanilla event files were emptied by the upstream author (Sobisonator,
commit 8f97c3218) purely to reduce error-log noise — never a per-file gameplay decision.
Classifying the non-flagrantly-Roman set:

- **13 ALREADY-QING-LAYERED** (succession/monarchy/offices/integration/commander-loyalty/
  stability/civil-war/rename/influence): reviving the vanilla file would COLLIDE with the
  bespoke system. These are the subsystems triaged in §1 — the work is refactor-in-place
  (§1c BT-Q, §1h read-points), not revive-the-vanilla-file.
- **34 BUILD-ON-TOP-CANDIDATES** — generic mechanics with NO current Qing layer, i.e. genuine
  net-new content, not refactors. Biggest clusters:
  - **Disasters / omens** (fire, food/famine, storms, comet, natural_disasters) — TI/Invictus
    keep intact sources; strong thematic fit for a Mandate-of-Heaven layer.
  - **Character intrigue** (befriend, assassinate, lovers, friend_rival, prominent_actor) —
    Invictus has befriend/friend_rival intact; rest zeroed everywhere.
  - **Honors** (distinctions) — Invictus 1044-line source; maps to Victorian orders / bannerman ranks.
  - **Local flavor** (province_events, city_events, state_improvement).
- **0 SKIP-BORDERLINE** among the non-excluded set.

So: the marriage/trial/succession ones the user intuited as reusable are exactly the
ALREADY-LAYERED collision set — reuse is moot there. The real reuse opportunities are the
disaster/intrigue/honors gaps below.

---

## 2b. ADDITIONS — net-new content (the 34 build-on-top candidates)

These are mechanics with NO current Qing layer, so there is nothing to collapse — the work
is *adding* a system. But the same layering discipline applies: each addition should ride a
live vanilla hook/value and hang Qing thematic framing on top, NOT invent a parallel meter.
Sources below are the intact TI/Invictus files found (revive-and-adapt, not write-from-scratch);
"strip" = classical dependencies to remove (Roman offices, Hellenic religion, `is_tribal`).

### CLUSTER A — Disasters & Omens → a MANDATE-OF-HEAVEN layer (highest thematic fit)
The single best-fitting addition. In Qing political theology, natural calamity reads as Heaven's
displeasure (天譴) — so disasters shouldn't just be economic hits, they should feed legitimacy /
stability, which is the vanilla value the mod already uses everywhere (§1a). That makes this a
genuine build-on-top: **disaster event → vanilla `add_stability` / legitimacy nudge + local
economic effect, framed as a Mandate omen.**

| File | Source (revive) | Strip | Vanilla hook it rides | Qing framing |
|---|---|---|---|---|
| fire_events | Invictus fire_events (235 ln) — REUSE-READY, 0 classical deps | — | province/city scope; `add_stability` local | city conflagration; relief → legitimacy |
| food_events | Invictus food_events (4309 ln) | modern-logistics flavor | harvest/famine, pop unrest, `add_stability` | 荒政 famine-relief; failure = Mandate doubt |
| storms | TI storms (2101 ln) | ~5 priest/pic refs | naval damage, supply, coastal province | 漕運/typhoon; disrupts canal grain fleet (ties to §Works `qing_canal_condition`) |
| comet | Invictus comet (689 ln) | 3 priest-office checks | ruler reaction, stability | 彗星 omen → direct Mandate read; ruler-response branch |
| natural_disasters | TI disasters_inv (1753 ln) | classical flavor | earthquake/flood province effects | 地震/水災; the general 天譴 chain |

**Design spine:** one shared `qing_mandate_omen` scripted_effect that any disaster calls with a
severity arg; it applies the vanilla stability/legitimacy delta + a ruler-facing event whose
options trade treasury (relief) vs. legitimacy (neglect). This unifies the five files behind one
Qing-thematic hook instead of five disconnected vanilla chains. Priority: **HIGH** (fills the
"no disasters at all" gap + reinforces the legitimacy loop the mod already runs).

### CLUSTER B — Character intrigue (deepens the character layer the GC/justice systems rely on)
The mod is character-driven (Grand Council, censorate, princes) but has NO interpersonal
intrigue — characters have no friendships, rivalries, or plots. These ride vanilla character
scopes + `add_loyalty`/opinion, and should feed the systems that already exist (a rivalry
between two councillors → faction polarization §1g; a plot → a censorate impeachment §1e).

| File | Source (revive) | Vanilla hook | Qing framing / feed-in |
|---|---|---|---|
| befriend | Invictus befriend (1021 ln) — has office-demand chain | `add_loyalty`, opinion | patronage ties (門生/幕友); feeds GC bloc cohesion |
| friend_rival | TI friend_rival (1203 ln) | opinion, character relations | councillor rivalries → feed `qing_char_stance` polarization |
| assassinate | zeroed both mods (write fresh, small) | `imprison`/`death`, `add_tyranny` | palace plots; caught → censorate docket (§1e) |
| lovers | zeroed both (write fresh, small) | character relations | consort/harem intrigue → ties to harem-rank + succession backing |
| prominent_actor | zeroed both | character flavor | low priority; opera/literati patronage flavor |

**Design note:** befriend + friend_rival are the two worth doing (intact sources, and they feed
live Qing systems). Wire rivalry/friendship outputs INTO `qing_char_stance` and the harem/prince
backing so intrigue isn't a cosmetic side-pool. Priority: **MEDIUM** (befriend/friend_rival),
**LOW** (assassinate/lovers/prominent_actor).

### CLUSTER C — Honors & Distinctions → imperial favour / bannerman ranks
No honors system today. Invictus distinctions (1044 ln) is a character-honors chain (Roman
triumphs) that remaps cleanly to Qing merit classes (一等/二等/三等), Yellow Jacket (黃馬褂),
peacock feather (花翎), posthumous names. Rides vanilla trait/character-modifier grants; feeds
GC effectiveness (an honored minister carries more weight) and loyalty.
Priority: **MEDIUM** — strong for a character-driven mod, medium adaptation (remap the honor set).

### CLUSTER D — Local flavour (province/city/state) → tie to the economy + works systems
`province_events`, `city_events`, `state_improvement` are generic local-development events. The
mod has economy (trade/production) + a Works ministry but no local narrative layer. These ride
province/state scope and should nudge existing values (development, `qing_canal_condition`, local
stability) rather than a new meter. TI state_improvement (766 ln) is a source.
Priority: **LOW–MEDIUM** — nice depth, but broad and lower-stakes than A/B/C.

### CLUSTER E — Skip / defer among the candidates (stated so it's not silently dropped)
- `slave_revolts` — 1815 Qing has no chattel-slavery pop; would need full rework as
  lower-strata/serf unrest, and the mod already has `qing_rebellion_events` + ethnic tension.
  DEFER (overlaps existing rebellion layer).
- `deficit` — the mod has a debt/economy subsystem; `deficit` triggers may already be covered.
  AUDIT economy coverage before adding.
- `country_diplomacy`, `dip_friends_rivals` — the mod has diplomatic-play + Great-Game systems;
  generic diplo flavor risks overlap. DEFER pending a diplo-coverage check.
- `gambling`, `treatment`, `architect`, `random_nicknames` — pure minor flavor, no source in
  TI/Invictus (zeroed there too), lowest ROI. SKIP unless a flavor pass is explicitly wanted.
- `war_council`, `assembly_events`, `governor_policies`, `rise_of_the_family`,
  `power_base_character_events` — either republic-flavored or covered by GC/faction/rebellion
  systems. DEFER/SKIP.

### Additions — ranked shortlist
1. **Mandate-of-Heaven disaster layer (Cluster A)** — highest fit, fills a real gap, reinforces
   the legitimacy/stability loop. Start with fire_events (reuse-ready) as the pilot, then the
   shared `qing_mandate_omen` effect, then food/storms/comet/natural_disasters onto it.
2. **befriend + friend_rival (Cluster B)** — intact sources, feed live faction/harem systems.
3. **distinctions / imperial honours (Cluster C)** — feeds GC effectiveness + loyalty.
4. **local flavour (Cluster D)** — broad, lower stakes.

Additions are net-new content and separately scoped from the §1 refactors; if approved they
should each get their own boot-tested batch (events touch on_actions + can flood logs), and
each must respect the standing throttle/GC-slot conventions.

---

## 3. Recommended order of work (if approved)

Ranked by (correctness value × safety), most worth doing first:

1. **§1c BT-Q — succession seal vs. vanilla recalc doubling-up.** This is a live correctness
   bug (sealed heir can be silently overwritten), already on the backlog. Oracle-gate the hook,
   then re-assert the seal on the recalc-triggering on_actions. HIGH value, contained.
2. **§1h — subject integration reads `loyalty_to_overlord` + `integrate_speed` + `can_be_integrated`
   gate.** Three small, low-risk edits that make a bespoke system consume live vanilla values
   it currently ignores. Clear "build on top" wins.
3. **§1i — resolve the orphaned pop-support scaffolding** (wire or remove). Decision first.
4. **§1f — shadow Qing offices into vanilla slots.** Genuinely new capability (external
   visibility) but carries side-effect risk; do as an isolated experiment with a boot test.
5. **Documentation seams** (§1a/1e/1g comments) — cheap, prevents the next reader from
   re-litigating "why is this parallel."

Everything else (marriage land-transfer, regent scope, event-driven rosters) is oracle-gated
polish — do only after verifying the vanilla capability exists.

## 4. What NOT to do (explicit non-goals)

- Do not collapse the 13-office Grand Council into vanilla's 8 European slots (semantic
  mismatch; loses 六部 flavor; vanilla offices reserved for other tags).
- Do not convert Qing factions to vanilla parties (parties are republic/election mechanics;
  monarchy parties are disabled stubs).
- Do not replace the justice docket or subject-integration arc with vanilla's silent one-shot
  mechanics (the stateful narrative is the design).
- Do not revive the ALREADY-LAYERED vanilla event files (collision).
- Do not treat "build on top" as "rip out the parallel" — for NECESSARY-PARALLEL subsystems the
  vanilla mechanic is absent/disabled/reserved, so the parallel IS the correct architecture.
