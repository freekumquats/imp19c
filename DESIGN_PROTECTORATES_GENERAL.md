# DESIGN_PROTECTORATES_GENERAL.md — the Qing 都護府 as "Qing EICs"

**Branch:** `manufactured_goods`. **Status:** DESIGN (locked 2026-08-02). Task tag `#27` (colonization
rework). All commits authored + committed by `freekumquats`. Companion to `QING_FEATURES.md §13`
(colonization tree) and memory `imp19c-protectorate-general-rework`.

> **Scope:** replace the broken protectorate mechanic in the Qing overseas-colonization mission tree
> (`common/missions/qing_colonization_missions.txt`) — the seven 都護府 tasks anbei / andong / anxi /
> annan / anhai / anxin / anfei — and the effect behind them (`se_QING_PROTECTORATE.txt`
> `QING_establish_protectorate`). This doc does NOT cover the separate "claim-only → take+develop"
> reshaping of the maritime tasks (Alaska/Canada/California/Pacific/etc.), which is a related but
> distinct workstream under the same `#27` directive.

---

## 1. THE PROBLEM — the current mechanic is backwards

`QING_establish_protectorate` (as shipped) does the **inverse of history**:

1. runs `every_owned_province` over the region and adds the Qing's **own** provinces to a list;
2. calls `LAND_release_from_list` to **carve those Qing provinces off into a brand-new fabricated
   country**;
3. binds that fabricated country to CHI as a `sinosphere_tributary`.

So it **loses Qing core land**, **invents a polity from thin air**, and **garrisons nothing**. The
historical 都護府 (Protectorate-General, Tang "loose-rein" 羈縻 institution) and its 19th-century analogue
— the chartered company empire — were the opposite: a self-governing frontier instrument that **grew by
its own conquest** and **held the local polities as its own subordinates**, on the metropole's behalf.

## 2. THE MODEL — a "Qing EIC" (user's framing)

Mirror the mod's own **East India Company**: `GBR → EIC (government = megacorporation, a client_colony
of GBR) → princely states (Hyderabad, Mysore, Awadh, … as EIC's sub-subjects)`. The EIC was not land
carved out of Britain; it was a chartered frontier subject that conquered its own empire and ruled the
Indian states beneath itself, answering to London only at the top.

The Qing Protectorate-General is built the same way:

```
                 CHI  (the Son of Heaven)
                  │  frontier_protectorate  (mandate: expand & conquer)
                  ▼
          ┌───  MARCH  (都護府, government = megacorporation)  ───┐
          │  own governor-general · own army · own conquered land │
          ▼                                                        ▼
   local polity A                                           local polity B
   (the march's subject —                                   (the march's subject)
    a "princely state")
```

**Nested: `CHI → march → local polities`.** The local polities answer to the **march**, not to Beijing
(exactly as Hyderabad answered to the EIC, not to London).

### 2.1 What the march IS
- A **frontier subject of CHI** — not a directly-administered dependency, not Qing core territory.
- Its own **Governor-General** (govt `megacorporation`, `has_co_ruler = no` — the ruler slot IS the
  Governor-General), **appointed by the Lifan Yuan (理藩院)** — NOT an organically-generated local ruler
  (user ruling 2026-08-02). See §3.1 for the appointment mechanism. Its own **army**, its own
  **buildings/development**.
- A **DUAL mandate — expand by BOTH conquest AND colonization** (user ruling 2026-08-02), and it must
  **ACTIVELY expand, not merely be able to** (user ruling 2026-08-02) — the marches are AI-run and must
  actually go to war + settle, driven by a scripted expansion pulse (§3.4), not left to the vanilla AI's
  discretion:
  1. **Conquer OWNED land** — it wages its **own** offensive wars against neighbouring non-subject
     polities. Capability = `allowed_to_declare_war_against_others = yes` on the `frontier_protectorate`
     type (§3); the ACTION = `FUNC_declare_war_with_wargoal_province = { war_goal = conquer_wargoal
     province = <target> target = <owner> }` (se_FUNC.txt — the proven scripted war-declare-with-wargoal
     verb, as se_AI.txt uses it), fired from the march's expansion pulse.
  2. **Colonize UNOWNED land** — it plants colonies on empty/unclaimed frontier provinces. Base verb:
     `QING_colonise_this_province` (`se_QING_AMERICAS.txt:200-239`). **[REVIEW-CORRECTED M1]:** it has
     THREE hardcoded `scope:player` refs — `set_owned_by` (:203), the over-capacity source check (:208),
     and the settler-emigration picker (:215). Retargeting only `set_owned_by` would land the colony under
     the march but still emigrate settlers FROM CHI's crowded provinces. A correct march variant must
     parameterise/clone ALL THREE so the colony lands under the march AND draws its settlers from the
     MARCH's own over-capacity provinces (or a starter-pop fallback). Not a one-line retarget — a small
     clone.
- **Carved from conquered LOCAL-POLITY land — NEVER from CHI's own provinces.** It begins on the ground
  just taken from the locals (or first colonized) and grows from there by both roads.
- Holds the region's **existing local polities as its own subjects** (its princely states).

### 2.2 What the march is NOT — and why the amban/garrison questions don't apply
Earlier drafts tried to put **Qing** ambans (理藩院 residents) and **Qing** banner garrisons on the
protectorate. That created a contradiction ("if the ambans and garrisons are Qing, what is the march
*for*?"). The resolution: **the march is not directly administered by Beijing, so it correctly gets
neither.** Verified engine facts that force this:

- **The Lifan Yuan amban system reaches only CHI's DIRECT subjects.** Both the game-start seed and the
  quarterly sweep iterate `every_subject` / `random_subject` on ROOT = CHI, and the code comment is
  explicit: *"every_subject reaches direct subjects only"* (`se_QING_AMBAN.txt` ~L555). A sub-subject of
  the march is out of the Lifan Yuan's reach **by engine design** — so the march's princely states get
  no Qing amban, which is exactly right (they are the march's, not Beijing's).
- **A Qing garrison is a CHI-scope `create_unit`.** `SE_qing_raise_garrison` (the [BT-15] model) raises
  in `c:CHI` scope → a **CHI-controlled** unit. The march fields **its own** army instead — it is an
  autonomous conqueror, not a province Beijing garrisons.

So: **no Qing ambans, no Qing banner garrisons on the march or its princely states.** CHI deals only
with the march at the top of the chain. (The 1763-start Qing tributaries — TIB/KOR/VIE etc. — remain
the loose-rein direct subjects that *do* carry Qing ambans/garrisons; the protectorates-general are a
different, self-directed instrument and do not.)

## 3. THE SUBJECT TYPE — `frontier_protectorate` (DONE)

Off-the-shelf types don't fit: the two own-war-capable own-ruler types (`nominal_vassal`, `protectorate`)
**cannot build**, while the build-capable governorship/colony types **cannot self-declare war**. A
conquering march needs **both** (build/develop its conquests AND wage its own wars).

**Solution (built):** a NEW subject type `frontier_protectorate` in `common/subject_types/00_default.txt`,
cloned from **`client_colony`** (the EIC's own type — `can_build = yes`, `has_overlords_ruler = no`,
`joins_overlord_in_war = yes`, `protected_when_attacked = yes`, `can_be_integrated = no`,
`subject_can_cancel = no`, `has_limited_diplomacy = yes`) **plus the one field a colony lacks:**

```
allowed_to_declare_war_against_others = yes   # the expand-and-conquer mandate
```

- **Why a NEW type, not an edit to `client_colony`:** `client_colony` is shared by ~20 world colonies at
  game start (GBR's Gibraltar/Newfoundland/HBC/EIC, SPA's New Spain, POR's Brazil, NED's & DEN's colonies…).
  Granting own-war to `client_colony` would turn **every colonial dependency on the map** into a
  self-declaring conqueror — a massive unintended change. `frontier_protectorate` isolates the behaviour
  to the Qing marches.
- `allow = { always = no }` — the type is established ONLY by the colonization mission effect, never
  offered as a normal diplomatic action.
- Loc keys added (`frontier_protectorate` / `AM_` / `LEAD_`) in `mod_subject_types_l_english.yml`,
  mirroring `sinosphere_tributary`.

### 3.1 The Governor-General — appointed by the Lifan Yuan (理藩院)
The march's ruler is a **Governor-General appointed by the Qing Lifan Yuan** (user ruling 2026-08-02) —
not the ruler the engine would generate for a fresh `create_country`, and not an organic local. Mirror
the proven amban-appointment idiom (`QING_amban_post` / `QING_amban_wire`, `se_QING_AMBAN.txt`):

- Gate on a seated Lifan Yuan holder: `has_variable = qing_office_lifanyuan_holder` +
  `var:qing_office_lifanyuan_holder = { is_alive = yes  employer = ROOT }` (the same gate the amban sweep
  uses). The appointment is an act of that office.
- `create_character` in CHI scope for the Governor-General: `culture = manchu`, `religion = vajrayana`
  (or theatre-appropriate), moderate stats, `add_trait = fanyi_jinshi` (the translation-examination
  laureate, as ambans are) — the Manchu conquest-elite administrator, `save_scope_as`.
- Install him as the **march's ruler**: move him into the march + `set_ruler` (the Governor-General IS the
  megacorporation's ruler slot). **BOOT-CRASH GOTCHA** (memory `imp19c-create-character-crash-gotcha`
  / #90): never grant a role to a just-created character inside the same `create_character` block, and no
  HEALTH-trait on a boot char — set the ruler in a separate step, character created first.
- **[REVIEW-CORRECTED M5] Re-appoint on BOTH death AND term-end.** `megacorporation` is `type = republic`
  with `ruler_term = 3` (00_albert.txt:24-45) — so the march holds an ELECTION every ~3 years and would
  install its own LOCAL governor, defeating "Beijing picks the governor" if we only hooked death. The
  re-appointment must fire on term-end too: a periodic check (yearly pulse) that, whenever the sitting
  Governor-General is not a Lifan-Yuan appointee (no `qing_march_gg` marker) OR has died/termed-out,
  creates + installs a fresh CHI-appointed Manchu GG as the march's ruler. So the Lifan Yuan continually
  re-imposes its pick over the republic's election. **Cross-country ruler install is UNPROVEN** — verify
  `create_character` in CHI scope then `set_ruler`/`set_as_ruler` INTO the march (a different country)
  actually works (the #90 gotcha is separate — never grant a role inside the create_character block; here
  the extra risk is the cross-country ruler set itself). Fallback: create the GG in the march's own scope,
  or a `set_ruler` variant that takes a foreign character.

> This makes the march genuinely a Qing instrument at the top (Beijing picks its governor) while it
> remains self-governing below (own army, own conquests, own princely-state subjects) — the EIC pattern:
> a Court of Directors / Crown-appointed Governor-General over an autonomous company empire.

### 3.2 REVERSE TRIBUTE — the Qing SUBSIDIZES the march (money + manpower flow OUTWARD)
A tributary pays *in* to Beijing; a frontier march is the opposite — the throne **funds** its conquest
(the chartered-company / frontier-garrison subsidy: the EIC drew on Bengal revenue, but the Qing frontier
generalships — 伊犁/烏里雅蘇台 — were famously subsidised from the interior via the 協餉 xiéxiǎng system).
So the `frontier_protectorate` reuses the tribute mechanic **in reverse** (user ruling 2026-08-02).

**Mechanism — mirror `QING_subject_collect_tribute` (se_SUBJECT_QING.txt:715), flow reversed.** The
existing tribute effect runs on the Qing quarterly pulse over `every_subject` with a tribute tier and
does `subject -= amt; ROOT(CHI) += amt`. The march subsidy is a sibling effect
`QING_march_pay_subsidy` on the SAME quarterly pulse:
- `every_subject = { limit = { is_subject_type = frontier_protectorate } … }`.
- **Money:** `ROOT (CHI) -= amt; march += amt` — the reverse of the tribute transfer. Scale by a rate
  (a fraction of CHI's income, or a flat per-march stipend), and **clamp to CHI's own treasury** (Beijing
  cannot subsidise beyond what it holds — the historical xiéxiǎng dried up as the treasury did; a broke
  Qing stops funding, which naturally models 19th-c. frontier abandonment).
- **Manpower — [REVIEW-CORRECTED H3, 2026-08-02]:** manpower is docked from CHI **only when new cohorts
  are RAISED toward the tier target — NOT as a flat quarterly upkeep.** The original spec (dock the full
  5k/10k/15k EVERY quarter while ALSO maintaining a standing host) double-counts: a maintained army's
  manpower was already spent when raised, so re-docking it quarterly is an unbounded leak (one high march
  = 60k manpower/yr forever) that would bankrupt CHI's pool with no matching army growth. **Correct model:**
  the §3.3 maintenance pulse computes the shortfall (target size − current host); manpower is deducted from
  CHI == that shortfall only, at the moment those cohorts are raised (`add_manpower` deduct on CHI is fully
  proven — se_QING_WORKS.txt:449/:490). A steady-state march at its target costs ZERO manpower/quarter; the
  cost is the one-time levy to reach/rebuild the target after losses. (`add_manpower` deduct-on-CHI proven;
  crediting a subject's manpower pool directly is not needed — the CHI-scope raise IS the manpower delivery.)
- Gate/scale by the seated **Lifan Yuan / Board of Revenue** if we want it to depend on Qing fiscal
  health (optional — ties the subsidy to the same office that appoints the Governor-General).
- The 協餉 subsidy is the counterpart the tribute tooltip line promises in reverse; log `sys = SUBJ`.

> Net effect: the throne pours silver + men into its marches so they can conquer/colonize, exactly
> inverting the tributary who renders up to the throne. This is what makes a march an *investment*
> (Beijing funds expansion) rather than a revenue source.

**Player control — a low/med/high subsidy toggle, MIRRORING the tribute tier toggle (user ruling
2026-08-02).** The subsidy level is set from the SAME three-button (S/M/L) control in the Subject tab of
the Qing diplomatic view — the symmetric counterpart of the existing tribute-tier toggle:
- **GUI** (`gui/diplomatic_view.gui`, beside the tribute buttons ~L3004-3057): three
  `text_button_square_highlighted` buttons (S/M/L) bound to `qing_march_subsidy_{small,medium,large}_button`
  scripted GUIs, each with a green-tick `icon` gated on `qing_march_subsidy_is_{tier}`, and the whole group
  `visible` only when `scope:target` is a `frontier_protectorate` (so tribute buttons show for tributaries,
  subsidy buttons show for marches — same slot, mutually exclusive by subject type).
- **scripted GUIs** (`common/scripted_guis/SUB_QING_subject_interactions.txt`): clone the
  `qing_subject_tribute_{tier}_button` + `qing_subject_tribute_is_{tier}` set — `scope = country`,
  `saved_scopes = { target }`, `ai_is_valid = { always = no }`, `is_shown` = `scope:target` is a
  `frontier_protectorate`, `effect` = `QING_march_set_subsidy = { tier = <tier> }`.
- **effect** `QING_march_set_subsidy` = mirror `QING_subject_set_tribute` (se_SUBJECT_QING.txt:691): swap
  a `qing_subsidy_{small,medium,large}` country modifier on `scope:target` (the march) + a
  `qing_subsidy_tier` var that `QING_march_pay_subsidy` reads for the rate (e.g. small/med/high = a rising
  fraction of CHI income + rising manpower). No tier set → no subsidy (default off).

### 3.3 The march's ARMY scales with the subsidy (user ruling 2026-08-02)
The subsidy is not just gold + a manpower trickle — it directly sizes the march's standing host. A
frontier subsidy historically *was* the pay of the garrison (協餉 funded the 伊犁/烏里雅蘇台 banner armies),
so **the march's army size is directly proportional to its subsidy tier.** Concretely, on the quarterly
pulse (in `QING_march_pay_subsidy`, or a sibling `QING_march_size_army`):
- Compute the march's **target army size** from `qing_subsidy_tier` — **low = 5,000 men, medium = 10,000,
  high = 15,000** (user ruling 2026-08-02). No subsidy → target 0 (the march fields only what it can
  self-fund from its own conquests). NOTE these are soldier counts: convert to cohorts by the mod's
  men-per-cohort (verify the unit size at build — e.g. if a cohort ≈ 1,000, that is 5/10/15 cohorts;
  size the raised legion to hit the man-count, not a raw cohort literal).
- Reconcile the march's actual force to that target: raise cohorts up to the target when subsidy rises
  (proven `create_unit` / raise idiom, issued in the MARCH scope so the troops are the march's — contrast
  the CHI-scope garrison raise, §2.2), and stand down / let attrite toward the target when subsidy falls
  (concrete-over-abstract lifecycle symmetry — raising must have a matching curtail, memory
  `imp19c-onmap-object-lifecycle-symmetry`).
- So the low/med/high toggle is the player's lever on how large a conquering host Beijing funds for that
  march — turn the subsidy up to power an offensive, down to economise. **RESOLVED (review H3): the army is
  a MAINTAINED STANDING target, and CHI pays manpower only to RAISE toward it (§3.2), not as flat quarterly
  upkeep.** So raising a march from low→high (or rebuilding after battle losses) costs CHI the shortfall in
  manpower at that moment; a march sitting at its target costs nothing. Turning the tier UP is the manpower
  bill; a war of attrition that bleeds the march's host makes the maintenance pulse re-raise it, re-billing
  CHI — which IS the real, bounded cost of a hard-fought frontier war (not an unbounded per-quarter leak).

> Design tension to settle at build: whether the subsidy sizes a STANDING army the effect keeps topped
> up (a maintained garrison that shrinks if unfunded), or delivers a one-off reinforcement each quarter
> (cumulative). The "directly proportional" wording favours a **maintained target** (army size tracks the
> current tier), with lifecycle symmetry on the way down. Confirm at build.

**MARITIME marches also spawn NAVIES (user ruling 2026-08-02).** A march that must cross water needs a
fleet, not just an army — the subsidy sizes a **navy alongside the army** for the maritime marches. Which
marches are maritime:
- **Maritime (army + navy):** `Anhai` (Pacific), `Anxin` (New World), `Anfei` (Africa) — overseas — plus
  `Andong` (fragmented JAPAN — the daimyo/shogunate isles, per §4.1 retarget) and `Annan` (coastal SE-Asia).
- **Land-only (army only):** `Anxi` (the land-locked oasis khanates) and `Anbei` (the Kazakh steppe).
- **Mechanism:** each march tag carries a **`maritime` flag**. The subsidy effect (§3.2/§3.3) checks it:
  for a maritime march it ALSO raises a navy scaled to the subsidy tier, via `create_unit = { navy = yes
  location = <a port the march holds>  while = { count = <ships> add_subunit = <ship type> } }`.
  **[REVIEW-CORRECTED H2, 2026-08-02] — UNPROVEN, spike before relying on it:** every proven navy raise in
  the repo runs in the country's OWN scope at its OWN port (`owner = ROOT is_port = yes`); there is NO
  precedent for raising a navy in a SUBJECT/other-country scope, and imp19c_effects_legion_setup.txt:427-434
  documents that wrapping `create_unit` in a re-scope made `location` re-resolve wrong and fleets silently
  DROP — precisely the march-scope pattern here. So: (a) VERIFY a subject-scope navy raise at a march-owned
  is_port province actually berths (boot-test) before building on it; (b) if it fails, fall back to raising
  the navy in CHI scope and TRANSFERRING it to the march, or model the march's sea power abstractly.
- **CHICKEN-AND-EGG (review H2):** the three purely-overseas marches (Anhai/Anxin/Anfei) can't reach their
  theatre without a fleet, yet "skip the navy raise until the march holds a port" means an inland-founded
  maritime march no-ops its navy forever. RESOLVE at founding: a maritime march MUST be established already
  holding a coastal/port province (its founding conquest includes the port it was carved from), so it has a
  berth from turn one. If a march ever loses all ports, its navy raise pauses until it retakes one — but it
  is never founded portless. (Also why Anhai/Anxin/Anfei are founded from the naval colonization branches,
  which conquer coastal footholds first.)

### 3.4 The march ACTIVELY expands — a scripted expansion pulse (user ruling 2026-08-02)
The marches are AI-run, and `allowed_to_declare_war_against_others` only grants the *capability*; the
vanilla AI will not reliably drive a small frontier subject to conquer. So the marches expand under a
scripted driver — they go to war and colonize on their own. **CADENCE (user ruling 2026-08-02): a new
WAR OF CONQUEST is a LOW YEARLY CHANCE, gated on not-already-at-war** — NOT quarterly (quarterly would
have a march devour a continent in a few years; a real war takes years to fight + digest). The subsidy
PAYMENT/upkeep + army-maintenance (§3.2/§3.3) stay on the quarterly pulse; only the war-declaration is
rare.

`QING_march_expand_check` — fired **YEARLY** (on_yearly_pulse or a 365-day re-trigger), `every_country = {
limit = { is_subject_type = frontier_protectorate } }` — for each march:
- **War of conquest — LOW YEARLY CHANCE, gated on peace:** `if = { limit = { is_at_war = no  <not already
  fighting> } random = { chance = 15..20 ... } }` → pick a bordering province owned by a non-subject,
  non-Qing polity and `FUNC_declare_war_with_wargoal_province = { war_goal = conquer_wargoal  province =
  <it>  target = <its owner> }` (proven, se_FUNC.txt). So a march averages a new war every ~5–7 years,
  irregular, and never while a war is unfinished (the current war must be won + absorbed first).
- **Colonization of UNOWNED land — may be more frequent** (it is not a war): a bordering unowned province
  → `QING_colonise_this_province` retargeted to the march. Can run yearly without the chance-gate (or a
  higher chance), since peaceful settlement doesn't have the digest-time problem a conquest does.
- Pick the target by adjacency to the march (a `neighbor_country` / bordering-province scan), NOT its own
  overlord (CHI) or fellow Qing subjects.
- Scale ambition to the SUBSIDY tier (§3.3): a well-funded march (bigger army) may roll the war-chance
  higher / an unfunded one (target army 0) sits quiet. This ties the system together — Beijing's subsidy
  both sizes the host AND governs how boldly the march expands.
- **Guards:** never declare on CHI or a CHI subject/other march (check `is_subject_of = <overlord>` /
  `overlord = <the march's overlord>`); respect `protected_when_attacked` (FUNC already excludes those);
  skip if no valid target (no-op, logged). Keep it region-plausible (a march expands into its own theatre,
  not across the map) — gate targets by region/adjacency.

> This is the difference between a march that *could* expand and one that *does*. Combined with §3.3, the
> player's subsidy lever directly governs how aggressively each march eats its frontier.

### 3.5 The march gradually INTEGRATES its own subjects (user ruling 2026-08-02)
A princely state does not stay a subject forever — the march **digests it into direct rule over time**
(the EIC's own trajectory: subsidiary alliance → annexation; the Qing 改土歸流 "abolish the native chief,
appoint a magistrate"). Reuse the mod's proven gradual-integration mechanic
(`SUBJ_QING_advance_integration`, se_SUBJECT_QING.txt), but AUTONOMOUS (the march is AI-run) rather than
player-driven.

- **Mechanism — [REVIEW-CORRECTED H1, 2026-08-02]:** do NOT reuse `SUBJ_QING_advance_integration`'s
  threshold dispatcher. That dispatcher (se_SUBJECT_QING.txt:247-264) branches on the SUBJECT's TYPE, not
  on who the overlord is: if the subject `is_subject_type = autonomous_governorship` it fires the PLAYER
  event `qing_integ.30` (改土歸流, a human choice) — which an AI march can't answer and is CHI-flavored; the
  direct-absorb `else_if` only fires for a non-autonomous_governorship subject and is a legacy "unreachable"
  safety net. So a naïve reuse either fires a player event at an AI march OR requires binding the locals to
  `integrating_governorship` (an explicitly TRANSIENT `allow=always no` state — a misuse as a stable type).
  **Correct build:** write a MARCH-SPECIFIC integrate effect that accrues its own progress var and, at
  threshold, calls `SUBJ_QING_absorb_subject = yes` DIRECTLY (that effect is NOT CHI-gated — `grantee = ROOT`,
  se_SUBJECT_QING.txt:526-579 — so a march overlord can drive it), bypassing the advance-integration
  dispatcher entirely. No player event, no transient-type misuse.
- **CADENCE (user ruling): a slow YEARLY CHANCE per step** — each year, a low-chance roll advances one
  integration step on one of the march's eligible subjects (mirror the expansion pulse's yearly-chance
  idiom). So a subject takes, on average, several years to a decade of loose-rein before the march fully
  absorbs it — irregular/organic, not a fixed clock. 5 steps at a low yearly chance ≈ that pace.
- **Eligibility:** `SUBJ_QING_absorb_subject` (the verb we call at threshold) is not `can_be_integrated`-
  gated — it just transfers the subject's provinces to the overlord. So the march can absorb a bound local
  regardless of the local's subject type; the march-specific effect (below) owns its own progress var and
  threshold, so it does NOT depend on the local being `integrating_governorship` (which we avoid — it's a
  transient `allow=always no` state, not a stable princely-state type). Bind the locals at a normal
  subject type (§2/§5) and let the march-integrate effect absorb them directly at threshold.
- **Effect** `QING_march_integrate_pulse` (yearly), in each march's scope: pick one bound subject with a
  slow chance, advance a march-owned progress var (`qing_march_integ_progress` on the subject); at
  threshold call `SUBJ_QING_absorb_subject = yes` (scope:target = that subject). Absorbed provinces become
  the march's OWN direct territory (growing the march, not CHI). Own progress var + own threshold — do NOT
  route through `SUBJ_QING_advance_integration`'s player-event dispatcher (H1).

> So a march both EXPANDS its frontier (§3.4, conquest + colonization) AND CONSOLIDATES what it holds
> (§3.5, digesting its princely states) — the full company-empire lifecycle: subsidiary alliance, then
> annexation, on the march's own soil under Beijing's charter + subsidy.

### 3.6 Bogged-down march → a Qing RELIEF event (user ruling 2026-08-02)
When a march is **stuck in a long war** — losing/grinding — the Qing player gets an event to intervene.
This is the player-decision counterpart to the automatic standing subsidy (§3.2): a one-off war
emergency, chosen by the throne.

- **Trigger:** a `frontier_protectorate` subject that is `war = yes` with `has_war_exhaustion >=` a
  threshold (the proven stuck-war read, used in se_QING_ACCOUNTABILITY.txt:216 `has_war_exhaustion >= 10`);
  optionally also a days-at-war floor so brief wars don't fire it. Detected on the quarterly/yearly pulse;
  fire a country_event to CHI (ROOT), scope the stricken march as `scope:` target.
- **THROTTLE:** gate on the shared court-event slot `qing_gc_event_slot_used` (memory
  `imp19c-gc-event-throttle-rule`) — this is a Lifan Yuan / frontier-administration event, so it must not
  dogpile with other palace events. Check `NOT = { has_variable = qing_gc_event_slot_used }` in the
  offer's limit; claim it only on fire. Also a per-march cooldown so one march doesn't re-fire every pulse.
- **Options:**
  1. **Send extra money + manpower — SPAWN A RELIEF ARMY** (user ruling 2026-08-02): beyond the standing
     subsidy, this raises a fresh **~20,000-man army** for the march + `add_treasury` for the campaign;
     dock CHI the matching ~20,000 manpower + gold (the emergency 協餉 supplement). Raise via the proven
     `create_unit` idiom in the MARCH scope at a front/capital province.
     **[REVIEW-CORRECTED H4, 2026-08-02]:** there is NO per-unit "exempt from maintenance" primitive in
     this codebase (no unit-variables, no per-army maintenance-free flag). So "tag the relief army as
     exempt" is unbuildable. Instead express the relief as a **temporary raise of the march's maintained
     TARGET**: add a `qing_march_relief_bonus` var (+20,000) to the march that the §3.3 pulse ADDS to the
     tier target when computing the target size, so the pulse itself raises + then maintains the bigger
     host (no exemption needed — the relief IS part of the target while the bonus is live). Decay the bonus
     over time (e.g. −N/quarter or clear after M years / at war's end) so the swollen host is temporary and
     the march reverts to its tier baseline once the crisis passes. This uses only the proven target-
     reconcile machinery; no missing primitive.
  2. **The Qing joins the war** — Beijing enters the march's war directly: `add_to_war` run in the CHI
     scope (the joining country's scope — se_SEPARATISM.txt:285 gotcha), adding CHI to the march's war on
     the march's side. Brings the full imperial army to bear; the sharpest, costliest intervention (drags
     CHI into a frontier war it might otherwise avoid — GP-tension implications).
  3. **Decline / leave the march to its fate** — no cost; the march fights on alone (and may lose land,
     which is a natural check on overreach). Perhaps a small legitimacy/loyalty ding with the march.
- **Effect + event:** a new `qing_march_relief.N` event (namespace in a `qing_march_*` events file) fired
  by the detection pulse; LOG sys = SUBJ/QING. All money/manpower/join effects are the proven verbs above.

## 4. THE SEVEN MARCHES

Tang Protectorates-General, extended anachronistically. Each is minted as a **predefined dormant tag**
(§5) and established by its mission task (§6). Culture/religion = the theatre's dominant local one (the
march is a local conqueror-state under a Qing charter, not a Han colony).

### 4.1 The "already-Qing theatre" trap (why 3 of 7 are RETARGETED)
The model requires an **independent local polity to conquer the march out of**. But the Qing tributary
ring in 1763 is large (18 direct subjects: VIE/KOR/RYU/TIB/CKL/DER/ILI/ULS/MNC/MKD/HLJ/LAF/FOS/CHH/MLM/
TNI/LSU/TNN). Three of the original protectorate theatres are **already Qing / subject-held**, so there
is nothing independent there to conquer — they only ever "worked" via the broken carve-from-Qing-land
mechanic. Verified against `setup/main/00_default.txt`:
- **Mongolia** (old Anbei) — Inner Mongolia is CHI core; Outer Mongolia is ULS/MGA/KBD subjects; the
  Zunghars were destroyed 1759. No independent local to conquer.
- **Liaoning/Korea** (old Andong) — Liaoning is the Manchu CHI core; **Korea (KOR) is a CHI
  sinosphere_tributary** (line 912). Nothing independent. → Andong RETARGETS to **fragmented Japan**
  (dozens of daimyo tags under a loose Tokugawa — real conquerable polities), founded from
  `qing_open_japan_missions.txt`. (NOT the Russian Far East — Russia is unified/solid; Japan is the
  fragmented frontier that fits the march model, user ruling 2026-08-02.)
- **Vietnam** (old Annan) — **VIE is a CHI sinosphere_tributary** (line 910). Nothing independent.

So these three are **RETARGETED to real, still-independent frontiers** (user ruling 2026-08-02); the
other four fit as-is.

> **MAP REGION-NAME TRAP (verified 2026-08-02):** the map's Central-Asian region names are
> counterintuitive — do NOT gate tasks by the name you'd expect:
> - region **`Turkestan`** = the **Kazakh STEPPE** (areas Akmolinsk/Turgai; the nomad hordes) — NOT the
>   oasis states. The OLD `qing_col_anxi` task gated on `is_in_region = Turkestan`, i.e. it was pointed
>   at the steppe, not the oasis khanates it names — a pre-existing mis-target to fix.
> - the settled **oasis khanates** (Kokand/Bukhara/Khiva) are in **`Fergana` / `Bukhara` / `Khwarezm`**.
> - the **Tarim** basin (Kashgar/Aksu/Urumqi/Yarkand — the historical 安西 seat) is in region **`Gansu`**
>   (Tarim area) + `Turkestan` (Dzungaria) and is **already Qing** (ILI/XNG) — not conquerable.
> - **CENTRAL-ASIA SPLIT (user ruling):** Anxi = oasis khanates; Anbei = Kazakh steppe; the existing
>   `qing_col_central_asia` claim-task is **folded into these two marches** (its Kokand/Tashkent claims →
>   Anxi; its Alma-Ata/Bishkek steppe claims → Anbei), not left as a parallel claim-only task.

| Name (都護府) | Tag | Theatre / region (RETARGETED where noted) | Local polities it subordinates (princely states) |
|---|---|---|---|
| 安北 Ānběi — Pacified North | `ANB` **[land — army only]** | **RETARGET: the Kazakh STEPPE** — map region **`Turkestan`** (Akmolinsk/Turgai areas; nomad steppe, NOT the oasis states) | the independent Kazakh hordes — Great/Uly (GKH), Middle/Orta (ORT), Little/Kishi (KSH); none are CHI subjects. Absorbs the steppe claims of the old `qing_col_central_asia` (Alma-Ata/Bishkek) |
| 安東 Āndōng — Pacified East | `ADO` **[maritime — army + navy]** | **RETARGET: fragmented JAPAN** (the daimyo domains + shogunate isles), NOT already-Qing Liaoning/Korea and NOT unified Russia. Japan is heavily FRAGMENTED in 1763 (dozens of daimyo tags under a loose Tokugawa TKG) — real conquerable polities, like the khanates for Anxi; Russia is a solid wall (user ruling 2026-08-02) | the independent/loosely-held Japanese daimyo (Satsuma/Shimazu SHZ, Choshu CSU, Date DTE, Nambu NMB, Maeda MED, …), the Tokugawa TKG shogunate, + the Ainu (AIN) of Ezo |
| 安西 Ānxī — Pacified West | `AXI` **[land — army only]** | the settled **OASIS KHANATES** — map regions **`Fergana` / `Bukhara` / `Khwarezm`** (NOT "Turkestan", which is the steppe; NOT Tarim, which is already-Qing Xinjiang) | Kokand (KOK, cap 110/Fergana), Bukhara (BUK, cap 7614/Bukhara), Khiva (KHV, cap 713/Khwarezm) — all independent. Absorbs the oasis claims of the old `qing_col_central_asia` (Kokand/Tashkent) |
| 安南 Ānnán — Pacified South | `ANM` **[maritime — army + navy]** | **RETARGET: independent mainland SE-Asia** (NOT tributary Tonkin). **Founded from the BURMA WAR tree, not the colonization tree** (see §4.2) | Siam (SIA), the Nguyễn south (VIE, freed by the §4.3 fix), the Shan/Lao polities not already CHI subjects |
| 安海 Ānhǎi — Pacified Seas | `AHI` **[maritime — army + navy]** | the Pacific island territories (fits as-is) | the island polities the maritime tasks reach |
| 安新 Ānxīn — Pacified New World | `AXN` **[maritime — army + navy]** | the North-American Pacific coast (fits as-is) | the New-World coastal polities in reach |
| 安非 Ānfēi — Pacified Africa | `AFI` **[maritime — army + navy]** | the African holdings (Swahili/Cape/Congo/Red Sea) (fits as-is) | the African coastal polities in reach |

### 4.2 Each march is founded from the mission tree that CONQUERS its theatre (user ruling 2026-08-02)
**Not** from the abstract colonization Maritime Bureau. A march is established as the capstone/branch of
the tree where the player has actually just conquered the land it is carved from. The overseas theatres
(Pacific/New World/Africa/Amur) have **no standalone tree** — those arcs live as branches *inside*
`qing_colonization_missions.txt`, so those marches are founded from their respective colonization
branch. The land frontiers have dedicated conquering trees. Mapping:

| March | Founding tree | Conquest already in that tree |
|---|---|---|
| Anxi `AXI` (oasis khanates) | `qing_central_asia_missions.txt` | `qing_ca_khanates`/`_ferghana` conquer KOK/BUK/KHV |
| Anbei `ANB` (Kazakh steppe) | `qing_central_asia_missions.txt` | `qing_ca_kazakh` conquers GKH/ORT/KSH |
| Annan `ANM` (SE Asia) | `qing_burma_war_missions.txt` (#421) | Burma/Shan/Laos/Siam-flank tasks; `qing_burma_tribute` subjugates BUR |
| Andong `ADO` (fragmented Japan) | `qing_open_japan_missions.txt` (#447) — the naval opening/conquest of Sakoku Japan | already deals with TKG, the daimyo, and the Ainu (AIN) of Ezo; gated on the Treasure Fleet |
| Anhai `AHI` (Pacific) | `qing_colonization_missions.txt` — the **Pacific branch** (`qing_col_pacific_isles`/`_new_holland`) | overseas isles |
| Anxin `AXN` (New World) | `qing_colonization_missions.txt` — the **New-World branch** (`qing_col_alaska`/`_california`) | overseas coast |
| Anfei `AFI` (Africa) | `qing_colonization_missions.txt` — the **African branch** (`qing_col_zheng_he`→`_cape`→`_congo`) | overseas coast |

All call the same `QING_establish_protectorate` effect (§6) with the march tag + the theatre's local list.
The old standalone `qing_col_anbei`/`_andong`/`_anxi`/`_annan`/`_anhai`/`_anxin`/`_anfei` protectorate
tasks in the colonization tree are removed/relocated: Anxi+Anbei move to the Central Asia tree, Annan to
the Burma tree, and Andong/Anhai/Anxin/Anfei become the capstones of their existing colonization branches.

### 4.3 Standalone fidelity fix — Vietnam's tributary is TONKIN, not the Nguyễn south
The mod has Vietnam's tributary status **backwards**. Historically the Qing tributary "安南 Annam" was
the **Lê–Trịnh court in Tonkin / the NORTH** (capital Thăng Long/Hanoi) — that is where the tribute
missions to Peking came from; the mod's own `research/1763_TRUTH_CHINA.md:52` documents this and flags
the setup caveat. But `setup/main/00_default.txt:910` makes **VIE (Nguyễn SOUTH, Huế 2593)** the CHI
`sinosphere_tributary` while **TRH (Trịnh/Tonkin north, holds Hanoi 3418) has no dependency — independent**.
The Nguyễn were historically **independent** of the Lê and did **not** recognise the Lê emperor.

**Fix (user ruling 2026-08-02):** flip it — make **TRH the CHI sinosphere_tributary** (the real Annam)
and **free VIE (Nguyễn) to independent**. This is a standalone 1763-fidelity correction. It also feeds
the Annan retarget: the freed independent Nguyễn south (VIE) becomes one of the conquerable SE-Asian
targets. (Verify: TRH's capital is in its own_control_core; no ownerless-capital crash; TRH may need a
`dependency` line + the ritual-tributary comment mirroring the VIE line being removed.)

> Tag codes are 3 chars (registry is 100% 3-char); all seven verified free (`ADG`, `ANH` were TAKEN,
> hence `ADO`, `AHI`). Exact seat provinces + the concrete local-polity tag list per theatre are
> finalised at build time against `setup/main/00_default.txt` + `map_data` (the map-data trap:
> verify a province's AREA→REGION, never trust the culture column — memory
> `imp19c-colonization-mission-arcs`). The three retargeted tasks (`qing_col_anbei` / `_andong` /
> `_annan`) also need their `allow`/completion triggers re-pointed from the old already-Qing regions
> (Mongolia / Liaoning+Korea / Vietnam) to the new frontier regions + independent-polity targets.

## 5. MINTING THE TAGS (dormant, activated at runtime)

A predefined tag that is **landless with a ruler crashes at boot**. But a tag that is merely
**registered + defined with NO `00_default` block** lies dormant safely — **~46 shipped registered tags
already have no `00_default` block** (683 registered vs 637 blocks; review-corrected 2026-08-02 — the
earlier "152" figure was wrong, but the pattern holds and is boot-safe). They are released/spawned later.

> ⚠ **UNPROVEN combination (review 2026-08-02):** `create_country` and `change_country_tag` are each real,
> but the repo has NO precedent for `create_country` → then `change_country_tag` to a predefined code as a
> unit (the JPN precedent renames an ALREADY-EXISTING tag; every `create_country` stays an anonymous
> dynamic tag). Treat as unproven — spike it in isolation before relying on it, or fall back to a dynamic
> tag with a scripted custom name (loses only the fixed 3-letter code + predefined COA).

Per march (the proven recipe, memory `imp19c-new-country-tag-recipe`):
1. `setup/countries/countries.txt` — registry line `ANB = "setup/countries/<region>/<name>.txt"`.
2. `setup/countries/<region>/<name>.txt` — definition file **WITH BOM** (efbbbf): `color` / `color2` /
   `gender_equality = no` / `ship_names = { … }`. NO `family`/`set_as_ruler` (engine generates a period
   ruler → sidesteps the setup char-ID-contiguity rule).
3. **NO `00_default` block** → dormant, boot-safe.
4. `localization/english/countries_l_english.yml` — `ANB:0 "…"` + `ANB_ADJ:0 "…"`.

**Runtime activation** (in the mission effect, §6): `create_country` mints a fresh scope, then
`change_country_tag = ANB` renames it to the predefined code (VERIFIED real verb — `se_JAPAN_BOSHIN.txt:201`
`change_country_tag = JPN`; used across Terra-Indomita + Invictus; memory `imp19c-ai-autonomous-arc-verbs`).
Cosmetic `change_country_name`/`_adjective`/`_flag` wrapped in `hidden_effect`.

## 6. THE EFFECT — rewrite `QING_establish_protectorate`

Replace the `LAND_release_from_list`-from-Qing-soil body with:

```
QING_establish_protectorate = {   # args: $march_tag$, $name_key$, $adj_key$, $local_list$ (region's local polities)
  # 1. mint/activate the march from CONQUERED LOCAL-POLITY land — NOT from CHI provinces.
  #    (Build the province list from the just-conquered local territory, per §6.1.)
  # 2. change_country_tag = $march_tag$  (+ hidden_effect cosmetics); government = megacorporation.
  # 3. bind the march to CHI as frontier_protectorate  (FUNC_make_subject overlord=ROOT type=frontier_protectorate).
  # 4. GOVERNOR-GENERAL: gate on the seated Lifan Yuan holder; create a Manchu Governor-General char in
  #    CHI scope (§3.1) and install him as the MARCH's ruler (separate step — #90 boot gotcha). Register a
  #    re-appointment-on-death hook so the post stays a Lifan Yuan appointment.
  # 5. subordinate the region's existing local polities as the MARCH's subjects
  #    (FUNC_make_subject overlord = <the march scope>  target = <each local>  type = <protectorate/tributary>).
  # 6. DUAL MANDATE (§2.1): the march both CONQUERS (its own wars, via the subject type) and COLONIZES
  #    unowned frontier land — seed/enable the QING_colonise_this_province road retargeted to the march
  #    (set_owned_by = <march> on unowned provinces). The march's ARMY is sized by its subsidy tier (§3.3),
  #    maintained on the quarterly pulse (create_unit in the MARCH scope up to the tier target); seed an
  #    initial force here matching whatever subsidy tier the founding task sets.
  # 7. NO Qing amban post, NO SE_qing_raise_garrison — the march is self-governing (§2.2).
  # LOG every step sys = QING.
}
```

Plus a standing quarterly effect (§3.2), NOT part of the one-shot establish:
```
QING_march_pay_subsidy = {   # on the Qing quarterly pulse, ROOT = c:CHI — the 協餉 reverse-tribute
  every_subject = { limit = { is_subject_type = frontier_protectorate }
    # money: CHI -= amt ; march += amt  (reverse of QING_subject_collect_tribute), clamped to CHI treasury
    # manpower: CHI -> march reinforcement (verify transfer verb; else approximate)
    # ARMY (§3.3): reconcile the march's host to the tier's target size — raise cohorts (create_unit in
    #   the MARCH scope) up to target when funded, stand down toward target when unfunded (lifecycle symmetry)
  }
}
```

### 6.1 Where the march's land comes from
The march is **carved from the conquered local polity**, not from CHI. Concretely, at establishment the
task has just defeated/subjugated the local state(s); the march is created on **that** territory
(transferred from the local polity to the new march tag via the proven `LAND_transfer_provinces` with
the LOCAL polity's provinces as the list, grantee = the march) — CHI's `own_control_core` is never
touched. From that foothold the march expands by its own wars (`allowed_to_declare_war_against_others`).

**[REVIEW-CORRECTED M4] EXPLICIT RULE (resolves "carved from conquered land" vs "holds locals as
subjects" — you can't annex a polity's land AND keep it as a living subject):**
- At establishment the theatre has SEVERAL local polities (Anxi: Kokand/Bukhara/Khiva; Andong: multiple
  daimyo + Ainu; Anbei: three Kazakh hordes; Annan: Siam/Nguyễn/Shan/Lao; the overseas theatres: multiple
  coastal states). **One conquered polity (A) becomes the march** — `LAND_transfer_provinces` moves A's
  provinces to the new march tag (A is thereby consumed/destroyed as a separate country). **The OTHER
  local polities (B, C, …) are bound as the march's SUBJECTS** via `FUNC_make_subject` (overlord = the
  march) — they keep their rulers as princely states.
- **Multi-polity theatres only.** Every march theatre has ≥2 local polities, so this always has a "become
  the march" polity + "become subjects" polities. (If a theatre ever had a single local, the march would
  be that polity converted in-place — but none of the seven is single-polity; verify at build.)
- **`FUNC_declare_war_with_wargoal_province` side effect (review):** when a march's expansion pulse (§3.4)
  targets someone's TRIBUTARY, that verb permanently RELEASES the target from its overlord (the reinstate
  block is gated `always = no`, se_FUNC.txt:392-403). Acceptable (it frees the target to be conquered) but
  note it — a march attacking a tributary strips it from its overlord as a side effect.

## 7. FAILURE HISTORY (do not repeat)

Corrections made during design, each a rejected shape:
1. ❌ Release Qing provinces as a new fabricated tributary (`LAND_release_from_list` from Qing soil) — the
   ORIGINAL broken mechanic. **Never carve or release CHI's own land.**
2. ❌ March holds CHI-core land via `LAND_transfer_provinces` of Qing provinces — same sin, different verb.
   **The march holds conquered LOCAL land only.**
3. ❌ Local polities as **direct CHI** loose-rein subjects — rejected; they are the **march's** subjects.
4. ❌ Put **Qing** ambans + garrisons on the march / its subjects — impossible (Lifan Yuan reaches only
   CHI's direct subjects) AND pointless (would make the march an empty shell). The march is self-governing.
5. ❌ Reuse `client_colony` with the war field added — would arm ~20 world colonies. **New type instead.**
6. ❌ `change_country_tag` is fake — WRONG (I mis-flagged it); it is a real verb. BUT (review 2026-08-02)
   `create_country` → `change_country_tag`-to-a-predefined-code as a UNIT is unproven — spike it (§8.0).

## 8. BUILD ORDER

### 8.0 PHASING (review L1 — ship proven core first, defer/spike the unproven pieces)
This system is large and several primitives are UNPROVEN (flagged inline). Build in phases so a working,
boot-safe subset ships before the risky pieces, and SPIKE each unproven primitive in isolation (a throwaway
boot-test) before building on it:
- **UNPROVEN — spike before use:** (a) `create_country`→`change_country_tag` to a predefined code as a unit
  (§5); (b) cross-country `set_ruler` install of the Lifan-Yuan GG (§3.1/M5); (c) navy `create_unit navy=yes`
  in a SUBJECT scope (§3.3/H2); (d) march-driven `SUBJ_QING_absorb_subject` (§3.5/H1 — likely OK, `grantee=ROOT`,
  but confirm). If a spike fails, use the documented fallback.
- **PHASE 1 (proven, ship first):** the `frontier_protectorate` type (DONE) + the Vietnam fix + the split
  (all proven) + the founding effect with MONEY-ONLY reverse subsidy + army (no navy, no manpower-per-quarter
  bug, no self-integration, no relief). Marches exist, are subsidised in gold, hold their conquered core +
  princely-state subjects.
- **PHASE 2:** the manpower-on-raise model (§3.2 corrected), the army maintenance target (§3.3), the
  expansion pulse (§3.4 — proven verbs).
- **PHASE 3 (each behind its spike):** maritime navies (H2), self-integration (H1), the relief event
  incl. the 20k relief-army-as-target-bump (H4), the term-end GG re-appointment (M5).

### 8.1 STEPS
1. ✅ `frontier_protectorate` subject type + loc (DONE).
2. **Vietnam fidelity fix (§4.3):** in `setup/main/00_default.txt`, move the CHI `sinosphere_tributary`
   dependency from VIE to TRH; free VIE to independent. Verify TRH capital ∈ its own_control_core (no
   ownerless-capital crash). Standalone — can commit separately.
3. Mint the 7 dormant tags (registry + def files + loc). Verify: no tag-code collision, def files carry
   BOM, NO `00_default` block, boot-safe.
4. Rewrite `QING_establish_protectorate` to §6 (create_country → change_country_tag → carve from
   CONQUERED-LOCAL land → bind march as frontier_protectorate under CHI → subordinate the region's
   locals as the MARCH's subjects → seed the march's own army; NO Qing amban/garrison).
5. Found each march from **the tree that conquers its theatre** (§4.2), passing `$march_tag$` +
   `$local_list$`; drop the old `every_owned_province`-of-CHI list build:
   - **Anxi (AXI) + Anbei (ANB)** → capstone/branch tasks in `qing_central_asia_missions.txt` (Anxi off
     the khanate-conquest chain, Anbei off `qing_ca_kazakh`).
   - **Annan (ANM)** → capstone/branch in `qing_burma_war_missions.txt`.
   - **Andong (ADO) / Anhai (AHI) / Anxin (AXN) / Anfei (AFI)** → capstones of their existing colonization
     branches (Amur / Pacific / New-World / African).
   - Remove the seven old standalone `qing_col_an*` protectorate tasks from the colonization tree
     (the four overseas ones become their branch capstones; the three land ones relocate to CA/Burma).
6. Retire the dead parts of the old effect. Update loc + `QING_FEATURES.md §13`.
7. Verify boot-safety (BOM, ownerless-capital, brace balance, tag collision); adversarial review; commit + push.

## 9. VERIFIED ENGINE FACTS (load-bearing)
- `change_country_tag = TAG` — real; needs TAG pre-registered in `countries.txt`; cosmetics in `hidden_effect`.
- `create_country` — runtime tag-spawn (se_LAND, flavour_middle_east); mints a generated code.
- `LAND_transfer_provinces = { target_provinces=<varlist> grantee=<tag> }` — transfer to an EXISTING tag
  (se_LAND.txt:348), handles governorship wealth/stockpile split.
- `FUNC_make_subject = { overlord=<tag> target=<tag> type=<subject_type> }` — se_FUNC.txt:412; the overlord
  can be ANY tag (so a march can be an overlord of the locals).
- Dormant tag = registered + defined, NO `00_default` block (152 shipped examples boot fine).
- Lifan Yuan ambans reach CHI's **direct** subjects only (`every_subject` non-recursive).
- Subject type field `allowed_to_declare_war_against_others = yes` grants own offensive war.
- `government = megacorporation` (common/governments/00_albert.txt) — the EIC's govt, `type = republic`,
  `has_co_ruler = no`, `ruler_term = 3` — the ruler slot is the Governor-General.
- Stuck-war read = `war = yes` + `has_war_exhaustion >= N` (proven, se_QING_ACCOUNTABILITY.txt:216 uses
  `>= 10`); the relief event's trigger.
- `add_to_war = { … }` — join an existing war (se_SEPARATISM/se_DIPLOMACY/se_FUNC). GOTCHA
  (se_SEPARATISM.txt:285): it adds `this` to the war, so it MUST run in the JOINING country's scope — for
  "Qing joins the march's war", run it in the CHI scope, targeting the march's war on the march's side.
- Shared court-event throttle = `qing_gc_event_slot_used` (memory `imp19c-gc-event-throttle-rule`): every
  Lifan Yuan / frontier-administration event checks `NOT has_variable` in limit + claims on fire; reset
  monthly. The march-relief event uses it.
- Navy raise = `create_unit = { navy = yes  location = p:X (a port the raiser holds)  while = { count = N
  add_subunit = <ship> } }` — bare in country scope, NO `raise_legion` wrapper (memory
  `imp19c-create-unit-idiom`, in-game verified BT-52); multiple squadrons raise sequentially. For a
  maritime march, issue in the MARCH scope at a port the march holds; skip if it holds none yet.
- `QING_colonise_this_province` (se_QING_AMERICAS.txt) — the proven UNOWNED-land colonizer: `set_owned_by`
  an unowned province + move an over-capacity commoner pop (or starter-pop fallback). Retarget `set_owned_by`
  from `scope:player` to the march scope to colonize under the march. (Parameterise or clone a march variant.)
- Lifan Yuan appointment idiom = `QING_amban_post`/`QING_amban_wire` (se_QING_AMBAN.txt): gate on
  `qing_office_lifanyuan_holder`, `create_character` (Manchu, fanyi_jinshi) in CHI scope, install into the
  target. For the Governor-General, install as the march's RULER (separate step — #90 boot-crash gotcha:
  never grant a role inside the create_character block; no HEALTH trait on a boot char).
- Gradual integration = `SUBJ_QING_advance_integration = { steps = N }` (se_SUBJECT_QING.txt:209),
  overlord-scope, `scope:target` = the subject; accrues `SUBJ_integration_progress` 0..5, absorbs at
  threshold. CHI path fires the player capstone `qing_integ.30`; a MARCH (AI) must use the DIRECT-absorb
  branch (`SUBJ_QING_absorb_subject`) instead. Subject must be `can_be_integrated = yes`
  (`integrating_governorship`, or a convertible type). VERIFY the effect isn't hard-gated to CHI-overlord.
- `FUNC_declare_war_with_wargoal_province = { war_goal = conquer_wargoal  province = X  target = Y }` —
  proven scripted war-declaration-with-wargoal (se_FUNC.txt; used by se_AI.txt). Handles subject
  exclusions + brings in colonies/governorships. This is the ACTIVE-expansion verb for the march pulse.
- `common/ai_plan_goals/` is the engine AI-expansion config (an alternative/supplement to a scripted
  pulse — but a scripted yearly-chance pulse gives deterministic control over cadence, which the vanilla
  AI does not; the ruling favours the scripted driver).
- Reverse-tribute subsidy = mirror `QING_subject_collect_tribute` (se_SUBJECT_QING.txt:715) with the flow
  inverted (CHI -= amt; march += amt), on the Qing quarterly pulse, `every_subject { limit = {
  is_subject_type = frontier_protectorate } }`, clamped to CHI's treasury. `is_subject_type = X` is a
  proven trigger (used throughout se_AI/se_SUBJECT_QING). Manpower transfer: `add_manpower` validity on a
  subject scope + whether it can be moved CHI→subject is UNVERIFIED — confirm at build; fallback = grant
  the march a manpower/levy modifier instead of a direct transfer.
