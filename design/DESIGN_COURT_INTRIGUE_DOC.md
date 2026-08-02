# Court Intrigue Expansion — Harem (后妃) + Eunuch (內務府) Subsystems

Design for the two court subsystems that #37 and #38 grew into. Both build ON existing concrete code
(mapped with line citations), reuse proven primitives, and obey the construction-risk rules that the
harem/eunuch `create_character` paths already carry. **Nothing is built yet — this is for review.**

## ADVERSARIAL REVIEW PASS (2026-07-24) — applied fixes
Reviewers verified: NO create_character touched (blast radius confirmed untouched), NO #336 inline, named
branch is runtime-only. Fixes applied below:
- **1:1 validator (Risk 5/6):** the doc's "seat doesn't set qing_office_held" contradicted the regent
  precedent (which DOES set it → would trip `QING_validate_one_position`, se_QING_COUNCIL.txt:228-247, which
  counts both qing_office_held AND qing_is_palace_eunuch/qing_is_harem_consort). **RESOLUTION: separate
  seat-marker.** Chief-eunuch and dowager seats set `qing_seat_chief_eunuch` / `qing_seat_dowager` (NOT
  counted by the validator) + a display-only `qing_office_<key>_holder` country var (like the emperor/empress
  seats), and do NOT set `qing_office_held`. So a promoted eunuch keeps only `qing_is_palace_eunuch` (1
  marker → passes), a former-consort dowager keeps only `qing_is_harem_consort` (1 marker → passes).
- **A3/A5 scope:** all passive rolls + new events fire FROM `QING_harem_pulse` at ROOT=CHI using
  `ordered_in_list { variable = qing_harem_consorts }` and `trigger_event` to `type = country_event`s — NEVER
  from a character-root GUI context (BT-13/#373). Stated explicitly in A3/A5.
- **A1 favour drift (doom of the mechanic):** the earlier "drift toward rank×20" is a RESTORING drift that
  flattens every consort to her rank's value → kills the squabbling favour is meant to create. FIX: favour is
  a PURE ACCUMULATOR moved by the favour lever + events (+ a small decay toward 0 for un-favoured consorts,
  NOT toward rank). Favour becomes an axis INDEPENDENT of rank (low-rank favourite / high-rank cold political
  match) — that is the drama.
- **A3 fights-the-player:** passive promote/demote must SKIP any consort the player acted on within 730 days
  (`qing_consort_recently_acted` timer flag set by the player promote/demote levers; the roll gates
  `NOT has_variable`). The court drifts only consorts the player has left alone.
- **A5 dowager (harem.11) is ADVISORY, not forced:** she SUGGESTS a promotion/demotion (heed = +dowager
  favour/+harmony; defer = −dowager favour; refuse = −−favour + scandal risk). The player keeps the wheel.
- **B1 eunuch power formula (was underspecified):** define exactly —
  `qing_eunuch_power = min(100, qing_eunuch_count*8 + (faction_leader ? 30 : 0) + corruption_band_bonus)`,
  then `if chamberlain.charisma >= 8 { subtract 15 }` (a strong chamberlain checks the eunuchs). No
  boolean-in-arithmetic; the chamberlain term is a discrete guarded subtraction.
- **B2 doom-loop guard:** eunuch power feeds corruption/backlog/reform, but (a) the corruption nudge is
  gated `qing_corruption_level < 70` so it can't spiral past the crisis band; (b) the reform-balance penalty
  fires ONLY at high power (≥80), not the mid band; (c) add a PLAYER purge lever (a chamberlain decision,
  cost stability/harmony, −30 power, 1825-day cooldown) so counterplay isn't gated behind an event roll.
- **B2 reform-balance:** MUST use raw `change_variable` with the ±100 clamp (NEVER `QING_DECLINE_nudge`);
  verify existing qing_reform_faction_balance sites are all raw change_variable first.

## Hard constraints (from the code, non-negotiable)
1. **`create_character`:** no modifiers, no HEALTH-type traits inside it OR in a boot-reachable follow-up
   scope (the `castrated` trait was removed for exactly this — `se_QING_HOUSEHOLD.txt:96-103`,
   `se_QING_HAREM.txt:63-65`). culture/religion must be LITERALS (a country-scope value floods 1.4M log
   lines). New consorts/eunuchs spawn only at RUNTIME (pulse), never gamestate construction, and follow
   the proven mint idiom.
2. **Sorting iterators** (`ordered_character`, `ordered_in_list order_by=…`) must fire via a hidden
   `trigger_event` trampoline, NEVER inlined in a scripted_gui button (#336 AV crash class —
   `qing_harem_events.txt:176-217`).
3. **Picker rows run at CHARACTER root** — re-root to CHI via a hidden country_event before running
   ROOT-based machinery (BT-13/#373, `qing_harem_events.txt:154-163`).
4. **1:1 office validator** (`se_QING_COUNCIL.txt:228-247`): a character may hold only one position
   marker. A "chief eunuch" seat must be its OWN marker, NOT `qing_office_held` (else it trips the
   validator; `qing_is_palace_eunuch` is already a tracked position). Use the non-appointable-seat shape
   from `se_QING_SEATS.txt:15-18`.
5. **Event throttle:** any new court event shares `qing_gc_event_slot_used` (test-then-claim) — at most
   one court event per ~90-day pulse.
6. **Perf:** reads are O(1) counters + O(court) `any_character`; never sweep pops/provinces.

---

# SUBSYSTEM A — Harem Intrigue (后妃之爭)

## What exists (map summary)
4-rank ladder (`qing_consort_rank` 1-4, hard caps 1/2/4/uncapped enforced in 5 synced places); roster +
count + per-rank tallies; pickers draft·take / favour / promote; native heir via `make_pregnant`;
empress = `current_ruler.spouse`; quarterly `QING_harem_pulse` with a harmony↔fertility loop + ONE
12%-throttled intrigue event (schemer-vs-empress, 3 options). **Rank already feeds succession**:
`se_QING_PRINCES.txt:113-130` gives a prince +25 (嫡子, empress's son) / +12 (貴子, mother rank≥3) to
`qing_prince_backing`.

## Green field (what's missing)
No demote/disgrace (rank only rises); no promotion/demotion *chance* (deterministic); no per-consort
favour/affinity var (only engine popularity/prominence); no dowager; no elevate-to-empress; only one
intrigue event.

## Design

### A1. A real favour meter — `qing_consort_favour` (char var, 0..100)
The spine of squabbling. Seeded 30 on mint (follow-up scope, NOT in create_character). **[REVIEW FIX] Favour
is a PURE ACCUMULATOR, independent of rank** — do NOT drift it toward rank×20 (a restoring drift flattens
every consort to her rank and kills the squabbling). Nudged by:
- **Favour lever (臨幸):** the chosen/random favour effects add +12 favour (on top of the existing +15
  popularity + make_pregnant). The emperor's attention IS favour.
- **Quarterly decay in `QING_harem_pulse`:** un-favoured consorts decay toward 0 by −1..−2 (attention
  fades), NOT toward rank — so favour and rank can diverge (a beloved low-rank concubine; a prestigious but
  cold political match). Local nudge helper mirroring `QING_DECLINE_nudge` (clamp 0..100).
- **Intrigue outcomes** (below) move it in larger steps.
Read as the ORDER KEY for promotion/demotion picks (augmenting prominence) and the intrigue schemer pick.

### A2. Demotion + disgrace — the missing downward path
- **`QING_harem_demote_consort_target`** (mirror of promote, re-rooted): `qing_consort_rank -1` (floored
  at 1), -15 favour, -10 popularity, harmony -3. Cannot demote below rank 1 (she leaves the ladder only by
  death or disgrace). Player picker `qing_harem_demote_window` + trampoline `qing_harem.8`.
- **`QING_harem_disgrace_consort`** (冷宮 "cold palace"): the terminal fall. Strips
  `qing_is_harem_consort` (removes from roster like death, but she lives), sets a `qing_is_disgraced`
  marker, -all favour, big popularity hit, harmony -5. Gated on rank (can't disgrace the 皇貴妃 without a
  scandal event). This is the dismiss/expel the map found missing.

### A3. Promotion/demotion as a CHANCE, not a certainty
New pulse step: **`QING_harem_resolve_standings`** — fires FROM `QING_harem_pulse` at ROOT=CHI using
`ordered_in_list { variable = qing_harem_consorts }` (never a character-root GUI context — BT-13/#373). Each
quarter, for the most-favoured eligible consort below her cap, a `random chance = f(favour, harmony)`
promotes her; for the least-favoured high-rank, a chance demotes her. So standings SHIFT passively (the AI
court churns), not only on player click. **[REVIEW FIX] the passive roll SKIPS any consort the player acted
on within 730 days** (`limit = { NOT = { has_variable = qing_consort_recently_acted } }`; the flag is set with
`days = 730` by the player promote/demote levers) — so the court only drifts consorts you've left alone, and
never undoes a choice you just paid for. Throttled + cap-guarded against the same 5-place cap rule.

### A4. Rivalry & faction — `qing_consort_faction` (char var enum)
Consorts cluster into factions (e.g. empress's bloc / a rising-consort's bloc / neutral), assigned by a
pulse heuristic (highest-favour non-empress-aligned consort forms a rival bloc). Feeds:
- The intrigue event's schemer pick (the rival bloc's leader schemes).
- A new **harmony drain** when two blocs are both strong (court tension).
This reuses the existing `qing_dynastic_harmony` meter as the tension proxy — no new global meter.

### A5. New intrigue events (each shares the court slot, fires from `QING_harem_pulse`)
1. **qing_harem.9 — Pregnancy & the Question of an Heir (有喜):** on a consort conceiving (hook the
   make_pregnant), a beat: elevate her rank (favour + backing), or the empress's bloc moves against her
   (scandal risk). Couples directly to `qing_prince_backing` via her rank.
2. **qing_harem.10 — Miscarriage / Loss (小產):** low-harmony + rival-bloc-strong roll; a pregnancy is
   lost amid whispers of poison. Accuse (target a rival → disgrace chance) / mourn (harmony) / ignore.
   NO health-trait manipulation — pure favour/harmony/event state.
3. **qing_harem.11 — The Dowager Intervenes (太后懿旨):** if a dowager exists (see A6), she SUGGESTS a
   promotion or demotion. **[REVIEW FIX] ADVISORY, not forced** — heed her counsel (do it, +dowager
   favour/+harmony) / politely defer (no change, −dowager favour) / refuse outright (no change, −−dowager
   favour + scandal risk). Models 孝聖憲皇后-era matriarchal weight without the game seizing the player's wheel.
4. **qing_harem.12 — Scandal in the Inner Court (穢亂宮闈):** a high-rank consort implicated; disgrace
   (冷宮) or cover-up (corruption +, harmony -). The path to A2's disgrace lever.

### A6. Dowager concept — `qing_office_dowager_holder` (display-only seat)
Model the Empress Dowager (皇太后) as a non-appointable seat: the previous emperor's surviving empress/
high-consort, installed at succession. She gives a standing prestige modifier and is the trigger-owner of
qing_harem.11. **[REVIEW FIX — 1:1 validator] the install sets `qing_seat_dowager` (NOT counted by
`QING_validate_one_position`) + the display-only `qing_office_dowager_holder` country var, and does NOT set
`qing_office_held`** — so a former-consort dowager keeps only `qing_is_harem_consort` (1 marker, passes). Do
NOT "mirror the regent seat exactly" (regent DOES set qing_office_held). One install hook at accession.

## Harem risk assessment
- **A1/A2/A3/A4:** LOW — all var + effect + event work on the RUNTIME path (no create_character changes).
  The only care: keep the 5-place cap rule in sync when demotion crosses tiers.
- **A5 events:** LOW — pure event content, share the court slot.
- **A6 dowager:** LOW-MODERATE — touches the accession hook; mirror the regent-seat install exactly.
- **NONE of this touches `create_character`** — the boot-AV blast radius is untouched. The one place we
  read the mint path (A1 seeds favour) is in the EXISTING follow-up scope, not inside create_character.

---

# SUBSYSTEM B — Eunuch Influence (內務府 / 太監專權)

## What exists (map summary — MORE than expected)
The influence mechanic is already substantially wired via the **flag** `qing_eunuch_faction_leader`:
corruption-triggered spawn in `QING_household_pulse` (corruption≥50 + weak chamberlain → 20% promote
ablest eunuch: +ambitious, +loyal veterans, +gold, +corruption); 3 player levers (check / indulge /
instrument); 3 events (.2 faction ascends, .5 good order, .6 oversteps); GUI + loc. **What's dead: the
numeric `qing_eunuch_count` — written 4×, read nowhere.** All live logic keys off the flag.

## Design — give the count teeth + deepen the influence web

### B1. Make `qing_eunuch_count` a live signal — `qing_eunuch_power` (derived 0..100)
The header already DOCUMENTS a `qing_eunuch_power` "derived, not-stored" strength — build it for real.
Compute it each pulse in `QING_household_pulse`. **[REVIEW FIX — exact formula, no boolean-in-arithmetic]:**
`set_variable qing_eunuch_power = qing_eunuch_count`, `multiply = 8`; `if any_character{...faction_leader}
{ change +30 }`; `+ corruption_band_bonus` (e.g. +10 if corruption ≥50); `if chamberlain.charisma >= 8
{ change −15 }` (a strong chamberlain checks them); clamp 0..100. Gives the dead count a consumer (its whole
point) and a single number the new effects read.

### B2. Eunuch power CONSUMES into the court (the missing bite)
Each quarter, gated on `qing_eunuch_power` bands, the eunuch establishment exerts influence — reusing the
mapped hook primitives:
- **Corruption:** high power → standing `QING_DECLINE_nudge = { var = qing_corruption_level amount = +1/+2 }`
  (idiomatic; HOUSEHOLD already nudges corruption via check/indulge). **[REVIEW FIX — doom-loop cap]** gated
  `qing_corruption_level < 70` so eunuch graft can't spiral past the crisis band.
- **Secretariat backlog (票擬):** high power → `change_variable qing_secretariat_backlog +N` — eunuchs
  intercepting/slowing memorials, historically exact (敬事房 handled palace paperwork). Mirrors the +6
  fresh-rescript nudge.
- **Reform balance:** eunuchs are structurally reactionary → nudge `qing_reform_faction_balance`
  **negative** −1/−2 (raw change_variable, ±100 clamp — NOT the DECLINE_nudge macro). **[REVIEW FIX]** fires
  ONLY at very high power (≥80), not the mid band, so it's not a third simultaneous penalty at every level.
All guarded, all small, all at existing nudge sites — the P7 bias discipline. **[REVIEW FIX — counterplay]**
add a PLAYER purge lever (a chamberlain decision: cost stability/harmony, −30 eunuch power, 1825-day
cooldown) so the exit isn't gated behind an event roll + a strong-chamberlain RNG check.

### B3. Chief Eunuch seat — `qing_office_chief_eunuch_holder` (display-only)
When a faction leader entrenches (power ≥ high band for N quarters), he takes a named seat. **[REVIEW FIX —
1:1 validator] the install sets `qing_seat_chief_eunuch` (NOT counted by `QING_validate_one_position`) + the
display-only `qing_office_chief_eunuch_holder` country var; it does NOT set `qing_office_held`** — so the
holder keeps only his `qing_is_palace_eunuch` marker (1 marker, passes the validator). Do NOT mirror the
regent seat (regent DOES set qing_office_held → would trip the validator). The seat is the on-map face of
太監專權 (a 李蓮英-type; period-note: famous eunuchs are post-1763, so 1763 starts get an anonymous 掌印太監).
Gives a standing modifier and is the trigger-owner of new events.

### B4. Deepen the event web (share court slot)
- **qing_household.7 — The Directorate Overreaches (內務府擅權):** high power beat; purge (costly, resets
  power, needs a strong chamberlain) / tolerate (corruption+, backlog+) / harness (instrument path,
  co-opt for throne).
- **qing_household.8 — A Faction at Court (閹黨):** the eunuch bloc allies with a council faction — ties
  into `se_QING_FACTION.txt` (`QING_faction_pick_ally`), tilting reform balance.
- **qing_household.9 — Retrenchment (裁抑內宦):** a reformer emperor / strong chamberlain curbs the corps;
  grants `qing_household_eunuchs_curbed` (exists), drops power, backlog relief.

### B5. The law on top — `qing_eunuch_policy_law` (restrict / standard / empowered)
NOW it has bite. on_enact sets `qing_eunuch_policy` ∈ {restrict / standard / empowered}, read by B1/B2:
- **restrict (裁抑):** caps `qing_eunuch_power` lower, halves its corruption/backlog output, +chamberlain
  authority modifier. Historically the early-Qing 敬事房 discipline (Qing deliberately curbed eunuchs
  after Ming excess).
- **standard:** no-op (default, byte-identical).
- **empowered (寵信):** raises the power cap, +privy-purse efficiency but +corruption/+backlog output and
  −reform. The Ming-style road to 閹黨.
Modifiers express the palace-management trade. This is the policy overlay on the now-live subsystem.

## Eunuch risk assessment
- **B1/B2:** LOW — pure counter derivation + nudges at existing sites. Gives the dead count a consumer.
- **B3 seat:** LOW-MODERATE — non-appointable seat; mirror SEATS + DON'T trip the 1:1 validator.
- **B4 events:** LOW — event content, share court slot.
- **B5 law:** LOW — selector var read by B1/B2.
- **create_character:** the ONLY mint is the existing `QING_household_mint_eunuch` (runtime pulse, boot
  seed of 4). We add NO new boot-reachable spawn and NO health trait. Blast radius untouched.

---

# Build sequencing (fits the risk-ascending batch plan)
These two subsystems are bigger than a law — they slot in as their OWN batches AFTER the law batches, or
interleaved. Proposed:
- **Batch 6 — Eunuch subsystem** (B1-B5): lower risk (mostly deepening existing wired code + reviving a
  dead var). Do first of the two.
- **Batch 7 — Harem subsystem** (A1-A6): more new surface (favour meter, demotion, factions, 4 events,
  dowager seat). Do second.
Each: author state → effects → pulse wire → events → loc → GUI (new levers/pickers + trampolines) →
brace/quote check → code-review → BOOT-CRASH review (mandatory, create_character-adjacent) → commit as
freekumquats → push.

**USER DECISIONS (2026-07-24):**
1. **Add BOTH seats** — Dowager (皇太后, A6) + Chief Eunuch (掌印太監/掌印太監, B3), non-appointable SEATS
   shape, held out of pickers, NOT setting `qing_office_held` (1:1 validator).
2. **Allow the anachronistic named branch** — a late-game/high-power branch may spawn a NAMED historical
   eunuch (李蓮英-type) and named consorts via the `QING_roster_finalize { nick = NICKNAME_… }` pattern
   (`se_QING_ROSTER.txt:45`). 1763 starts still get anonymous 掌印太監 / 選秀 consorts by default; the named
   figure is a runtime-only (never boot-reachable) spawn, NO inline health trait. Author the NICKNAME_ loc
   keys.
3. **Build the FULL design** — A1-A6 + B1-B5, as Batches 7 (harem) and 6 (eunuch). Eunuch first (lower
   risk, revives dead code + deepens already-wired flag mechanic); harem second (more new surface).
