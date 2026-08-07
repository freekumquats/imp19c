# DESIGN — Retire `qing_bureau_capacity` AND `qing_exam_ladder`; make the yamen + shuyuan networks the source of truth (衙門治理 / 書院文教)

**Branch:** merge-overnight. **Status:** ✅ SHIPPED 2026-08-06 (commit 23771cdf3; se_LOG follow-up 30e27023e). **Scope:** CHI only.

> **Two parallel conversions, same pattern (USER 2026-08-06: "do both").** #91 shipped items I (yamen ↔
> `qing_bureau_capacity`) and J (shuyuan ↔ `qing_exam_ladder`) as the *identical* hybrid anti-pattern:
> a stored 0–100 meter that SPAWNS a building on a band-cross, causation backwards. They share the same
> pulse (`QING_GOV_pulse`), the same `band_cur`/`band_prev` bookkeeping idiom, and the same fix. This doc
> covers BOTH. Everything below is written for the yamen/bureau_capacity case; §9 gives the shuyuan/
> exam_ladder parallel (the deltas — it is not a copy, the seed and buildability differ).

## 0. The problem (why this exists)

`qing_bureau_capacity` is a stored 0–100 country meter that violates the
[[imp19c-concrete-over-abstract-rule]] the whole #91 program was meant to enforce. Two user-stated
faults, both real:

- **Counterintuitive.** "Bureaucratic Capacity: 60" exposes no levers. Its inputs
  (`qing_council_effectiveness + qing_bureau_integrity` ÷2 − `qing_gov_corruption_drag`) are invisible;
  its outputs (mission gates, self-strengthening backing, three country modifiers) are scattered and
  never tell the player "you are blocked because this hidden number is < 55."
- **Poorly surfaced.** One panel line, no breakdown, no trend, no causal explanation.

Worse, the yamen was supposed to **replace** this meter (#91's concrete-over-abstract mandate), but #91
shipped it as a **HYBRID** — the meter still runs the show and the yamen hangs off it as a decorative
"face." Causation is backwards:

```
today:    council/integrity/corruption meters → qing_bureau_capacity (meter) → spawns a yamen (face)
intended: governance + real buildings → yamen network ON THE MAP → capacity DERIVED from the yamens
```

`#32` admin capacity already does it right — `ADMIN_provided_state` reads `num_of_qing_yamen_building`
directly (`ADMIN_svalues.txt:94-96`). This doc migrates the rest off the stored meter so the **yamen
count is the single source of truth** and the meter disappears.

## 1. Thesis — derive, don't store

Delete `qing_bureau_capacity` as a `set_variable`'d meter. Replace it with a **read-only derived
svalue**, `QING_bureau_reach`, computed on the fly from the concrete yamen network:

```
QING_bureau_reach = {   # 0..100, Scope: country (CHI). Pure read-only svalue (no cache needed — §3).
    # administrative reach = what FRACTION of the empire's county seats have a yamen.
    # concrete: COVERED provinces / coverable provinces. Counts provinces-with-a-yamen, NOT levels.
    value = {
        every_owned_province = { limit = { has_building = qing_yamen_building }  add = 1 }   # COVERED seats
    }
    divide = { value = QING_city_province_count  min = 1 }   # coverable seats; floor 1 (div/0)
    multiply = 100
    min = 0  max = 100
}
```
**CRITICAL — count covered PROVINCES, not building LEVELS (review finding #1).** The obvious idiom
`every_owned_province { add = num_of_qing_yamen_building }` sums *levels*, so stacking many yamens in one
city would inflate reach without covering a new seat, letting reach exceed 100 and making the "N/M seats"
loc a lie. Use `limit = { has_building } add = 1` (the proven `FUNC_num_ports_in_country` shape,
`FUNC_svalues.txt:71-79`) so reach is a true coverage fraction. **This REQUIRES `max_level = 1` on the
yamen def (see §1a)** — one magistrate's seat per county — which also closes the exploit in §1a.

Every current consumer of the meter reads this svalue (or the raw yamen count) instead. The meter, its
target-computation, its ±2 drift, its band-cur/prev bookkeeping, and the yamen **spawn** band-track all
go away — because the buildings are no longer spawned *from* the meter; the buildings are the input.

### What now drives yamen COUNT (the inversion) — USER DECISION 2026-08-06
**Yamens are seeded at 1763 AND freely player-buildable.** The player owns the network:
- **1763 seed** stays as-is (`se_QING_BUILDINGS.txt:180-197` blankets city provinces) — the baseline.
- **Player builds them** from the province buildings menu like any normal building. This requires
  UNLOCKING the def: today the yamen is only *conventionally* un-buildable (a comment; `add_building_level`
  bypasses `allow`). It already exposes a satisfiable `allow` (`tech_central_administration` + job slots)
  and a `cost`/`time`, so it is ALREADY effectively player-buildable — this task makes that intentional
  and keeps it (do NOT add `potential = { always = no }`). The cost/time IS the balance gate.
- **No script spawn/demolish loop.** The old `QING_GOV_yamen_band_track` (meter → build/remove) is DELETED
  outright. The count moves only via the seed + player construction + normal province loss. Events that
  used to nudge the meter (see §2 sites 9-13) simply **drop their nudge** — they no longer need to touch
  capacity at all, because capacity is now a pure read of the count the player controls.
- This is the cleanest form of the concrete-over-abstract rule: the player builds real offices; reach is
  just a readout of how many they've built vs how many seats exist. No hidden accumulator, no auto-spawn.

### §1a — MANDATORY: cap the yamen at `max_amount = 1` (fixes the admin-capacity exploit) — CORRECTED (review)
> ⚠️ **CORRECTION 2026-08-06 (review CRITICAL, FIXED in shipped code).** Earlier drafts said `max_level = 1`
> — **there is NO `max_level` engine key** (0 real uses in mod/Invictus/TI; the parser ignores it → no-op).
> The interim on-disk fix used `potential = { NOT = { has_building = <self> } }` — **also wrong**: a
> self-referential potential is UNATTESTED and flips FALSE the instant the building is placed, risking
> self-destruction (the imp19c-add-building-level-respects-potential memory warns of exactly this; no building
> in mod/Invictus/TI does it). **The PROVEN key is `max_amount = 1`** (Invictus/TI `00_default.txt`, 30+ uses,
> e.g. `fortress_ramparts_building` = `max_amount = 1` + a STABLE `potential = { has_city_status = yes }`).
> **DONE in code:** both `qing_yamen_building` and `qing_shuyuan_building` now use `max_amount = 1` + a
> STABLE `potential = { owner = { country_culture_group = jurchen/chinese_group } }` (`qing_governance_
> buildings.txt`). ⚠️ **[USER 2026-08-06] NO `has_city_status` gate** — yamens (rural county seats) and
> shuyuan did NOT require chartered cities historically. `max_amount = 1` does the capping; the owner-culture
> potential is required only so the def is well-formed and stays out of non-Qing menus (a building with no
> potential breaks). The rest of §1a stands. NOTE: dropping the city gate means the reach DENOMINATOR
> (`QING_city_province_count`, §3) may need revisiting — if yamens can now cover non-city provinces the
> numerator can exceed a city-only denominator; use owned-province count or `has_city_status` consistently on
> both sides (build-check the reach ≤100 clamp holds).
Review finding #2 (verified): the yamen def has **no `max_level`**, and building slots are effectively
unlimited (`global_settlement_building_slot = 9999`, `00_hardcoded.txt:741`); each level feeds **+8**
admin capacity (`ADMIN_svalues.txt:94-96`). So "freely player-buildable" as first drafted is a genuine
exploit: in a high-population province the only brake is `sufficient_job_slots` (1 pop/level), letting a
player stack dozens of yamens for near-unbounded admin capacity at 60 gold each. `cost`/`time` is a small
toll, NOT a cap — my earlier "it's the intended loop, cost is the balance lever" was wrong.

**Fix: add `max_amount = 1` to `qing_yamen_building`** (NOT `max_level` — §1a correction). One magistrate's
seat per county — matches the fiction, matches the 1763 seed's own `NOT has_building` idempotency guard
(`se_QING_BUILDINGS.txt:184`), and is the SAME change that makes `QING_bureau_reach` a true coverage fraction
(§1/§3, finding #1). With `max_amount = 1`, the player extends reach by covering *new* provinces (bounded by province count), not by
stacking — which is exactly the "administrative reach" fiction and cannot be gamed. #32 admin capacity
then also scales sanely (one +8 per province, bounded by owned provinces). This single def change resolves
BOTH criticals.
- Verify `add_building_level` respects `max_level` — if a pulse/event ever tries to add a 2nd level it
  should no-op, not stack. (Standard engine behavior; confirm no code relies on multi-level yamens — none
  found: all readers use `num_of_qing_yamen_building` which with max_level 1 = 0/1 per province.)

## 2. Migration table — every consumer of `qing_bureau_capacity` → what it reads instead

Audited via `rg qing_bureau_capacity` (13 sites). `R` = read/gate, `W` = writer/nudge.

| # | Site | Now | Becomes |
|---|---|---|---|
| 1 | `se_QING_GOVERNANCE.txt:34` | seed meter = 60 | **DELETE** (no stored meter) |
| 2 | `:80-98` | compute target + ±2 drift | **DELETE** (derived svalue, no drift) |
| 3 | `:108-127` `QING_GOV_apply_capacity_band` | add `qing_bureau_capable/strained/paralysed` country modifier at ≥70 / <50 / <30 | **KEEP the modifiers**, band on `QING_bureau_reach >= 70 / < 50 / < 30`. ⚠️ **NOT a mechanical no-op (review #6):** the decline SEMANTICS change. Today capacity drifts down under corruption/weak council → the empire can rot to `paralysed` (−18% tax, −10% PP, +1 global unrest) from *governance quality*. Under reach, the 1763 seed covers all city provinces → reach starts at exactly **100** and only falls when you lose covered provinces OR conquer uncovered ones. So `paralysed` (<30 reach = 70% of seats uncovered) becomes near-unreachable via rot, and instead means "you expanded faster than you administered." **This is a deliberate reframe (governance-rot → territorial-coverage), not a no-op — see §4.5.** If a corruption-driven decline path must survive, it now lives on the corruption band (`DESIGN_CORRUPTION_CONCRETIZE.md`), not here. |
| 4 | `:220-266` `QING_GOV_yamen_band_track` (spawn/remove yamen on meter band cross) | meter → yamen | **DELETE.** The yamen count is now the input, not an output of the meter. Count moves via §1 events instead. |
| 5 | `qing_reform_missions.txt:110,161` (R, ≥40/≥55) | gate on meter | **gate on `ADMIN_available_country` (§4.2, USER 2026-08-06) — NOT reach** |
| 6 | `qing_selfstrengthening_missions.txt` (R ×7, 40–60) | gate on meter | **gate on `ADMIN_available_country` (§4.2)** |
| 7 | `se_QING_SELFSTR.txt:55` (R, ≥50) | gate | **gate on `ADMIN_available_country` (§4.2)** |
| 8 | `se_QING_SELFSTR.txt:694-697` `qing_selfstr_backing` | **NOT a copy** — it's the FIRST term of a 3-way average: `value = capacity` → `add council_effectiveness` → `add integrity` → `divide 3` (the Elman refraction/hollow-test backing) | Change ONLY the `:694` term: `value = QING_bureau_reach`. **KEEP `:695-697` (the +council_eff +integrity +÷3) intact.** Do NOT collapse to a one-liner — that would silently drop two terms and corrupt the refraction test (review #5). |
| 9 | `se_QING_SELFSTR.txt:624` (W, +6) | nudge meter | **DROP the nudge** (capacity is now derived; the player builds yamens). Optionally the SelfStr success could `add_building_level` a yamen as a *reward*, but not required — see §4.3. |
| 10 | `se_QING_STUDENTS.txt:131` (W, +4) | nudge meter | **DROP the nudge** |
| 11 | `se_QING_MECHANICS.txt:680` (W, +2) | nudge meter | **DROP the nudge** |
| 12 | `qing_reform_events.txt:423` (W, +8) | nudge meter | **DROP the nudge** |
| 13 | `qing_integration_capstone_events.txt:78,103,126,166,244,298,357` (W, −5..−15) | nudge meter down | **DROP the nudges — MANDATORY, not per-event** (a surviving nudge resurrects the dead var, §5 invariant). If a collapse must cost reach, use `remove_building_level = qing_yamen_building` (guarded `has_building`) — NEVER a nudge on the dead var. |
| 14 | `qing_governance_l_english.yml:386` panel line | show meter value via `...MakeScope.Var('qing_bureau_capacity').GetValue` | show `QING_bureau_reach` **and** the raw count: "Administrative Reach: 78% (214 衙門 / 240 seats)". ⚠️ **NOT a drop-in `.Var()` edit (review MEDIUM):** `QING_bureau_reach` is a pure script_value, not a stored var — `.Var()` cannot read it. Use `...MakeScope.ScriptValue('QING_bureau_reach')` (proven in-mod at `gui/overview_view.gui:240` + `qing_province_reports_l_english.yml:60`, which display `ADMIN_available_country` exactly this way). |
| 15 | `00_event_values.txt:1859` `_target_cmpsvalue` | meter target wrapper | **DELETE** (no target) |

## 3. The derived svalue — implementation notes

- **Numerator** (covered provinces): `every_owned_province { limit = { has_building = qing_yamen_building }
  add = 1 }`. PROVEN country-scope precedent = `FUNC_num_ports_in_country` (`FUNC_svalues.txt:71-79`),
  which is the SAME `# Scope: Country` + `every_owned_province` + `limit = { has_building }` shape. (The
  earlier draft cited `ADMIN_provided_state:94` — that is a STATE-scope `every_state_province`, the wrong
  context; corrected per review #4.) With `max_level = 1` on the yamen (§1a) this count = provinces covered.
- **Denominator** (`QING_city_province_count`): `every_owned_province { limit = { has_city_status = yes }
  add = 1 }` (`has_city_status` in an svalue `limit` is proven: `EDU_svalues.txt:588-603`). Mirrors the
  1763 seed's own gate (`se_QING_BUILDINGS.txt:182`).
- **Guard** div/0: `divide = { value = QING_city_province_count  min = 1 }` (proven: `ADMIN_svalues.txt:193-196`).
- **Fully computable as a PURE svalue — no cache required** (review #4): country-scope svalues support
  `every_owned_province` sums, `divide` by another svalue, and `min`/`max` clamp (EDU/DEMAND/ADMIN
  precedents). This resolves the earlier §3 cache worry — the panel and gates read the svalue live. (If
  profiling ever shows the two sweeps are hot on GUI reads, a once-per-pulse `qing_bureau_reach_cache`
  read-var is an option, but it is NOT needed for correctness and adds a var — prefer the pure svalue.)

## 4. Design decisions / open questions for review

1. **Reach 0–100 is still a number on the panel — is that itself the anti-pattern?** No: the objection was
   a *hidden stored meter with invisible levers*. `QING_bureau_reach` is (a) derived live from a thing the
   player can see and change (build/lose yamens), (b) surfaced WITH its concrete basis ("78% — 214/240
   seats"). It's a readout of concrete state, not a hidden accumulator. If even the % is unwanted, the
   panel can show only "214 衙門 across 240 county seats" and gate missions on the raw count.
2. **Mission-gate target — USER DECISION 2026-08-06: gate on `ADMIN_available_country`, NOT `QING_bureau_reach`.**
   The 9 gates that today read `var:qing_bureau_capacity >= N` are **repointed to the real
   administrative-capacity number** — the concrete mechanic that already exists and that the user named
   directly: `ADMIN_available_country` (`ADMIN_svalues.txt:181` = `ADMIN_supplied_country −
   ADMIN_required_country`). Properties that make it the right target (better than reach):
   - **Concrete & already-trusted.** It reads the yamen network directly (`+8`/yamen, `ADMIN_svalues.txt:95`)
     and is already used as a live gate elsewhere (`DIPLOMACY_svalues.txt:14` `ADMIN_available_country < 0`).
   - **Signed — deficit vs surplus.** Unlike reach (which starts pinned at 100 and can only erode, so it
     *cannot* express "build up to unlock X" — the fatal flaw of the reach-gate approach), `ADMIN_available_
     country` swings **negative in deficit / positive in surplus**. An over-expanded realm goes into deficit;
     a well-administered one runs a surplus. This restores BOTH directions the reach ceiling lost.
   - **The 9 gates map by meaning, not by a copied number:**
     - *Reform unlocks that need a capable, non-overstretched bureaucracy* (constitutional draft `:161`,
       the higher self-str gates ≥55/≥60) → require a **positive cushion**, e.g. `ADMIN_available_country >= 0`
       (must be at least in balance) or a modest surplus.
     - *Early / foundational self-str tasks* (the ≥40/≥45 tier) → require merely **not in deep deficit**,
       e.g. `ADMIN_available_country >= NEG_FLOOR` (a small negative tolerance).
   - **The exact per-gate thresholds** need to be picked against the real 1763 `ADMIN_available_country`
     value for CHI (build-check: emit `LOG_line` of `ADMIN_supplied_country`/`ADMIN_required_country`/
     `ADMIN_available_country` at 1763 — the mod's own admin report already computes these per-state, so the
     realm total is derivable). Pick so the early tasks are open at 1763 and the deep-reform tasks require
     the player to first relieve the admin drain (build yamens / cut overstretch). This SUPERSEDES the old
     "classify coverage-floor vs build-up" analysis — the signed number expresses both natively.
   - **`QING_bureau_reach` is still built** (panel readout + the capable/strained/paralysed band, §2 row 3);
     it is just NOT what the mission gates read. Gates read the admin balance; the band/panel read reach.
   - **CAPABILITY PROVEN 2026-08-06 (bare script_value on a trigger-comparison LHS is legal in a mission
     gate).** `ADMIN_*` capacity is imp19c's OWN system (not upstream — no oracle hit expected), so the
     thing to prove is the grammar, not the name. Proven in-mod: `DIPLOMACY_power_from_economy >= 80` /
     `DIPLOMACY_power_from_military >= 30` (`imp19c_diplomacy_triggers.txt:59,61`) — both are script_values
     (`DIPLOMACY_svalues.txt:61`, `JOBS_svalues.txt:449` for the sibling `JOBS_available_slots > 0`) used
     BARE on a comparison LHS inside a `scripted_trigger`, which shares the mission `allow`/`trigger`
     grammar. And `ADMIN_available_country < 0` is itself already used this way in a `limit` block
     (`DIPLOMACY_svalues.txt:14`). So `ADMIN_available_country >= N` in a mission gate is proven-legal.
3. **The `+2` student/mechanics nudge (site 11)** is below the granularity of "build one yamen" (a yamen is
   ~0.4% reach). Options: accumulate small nudges into a build-when-enough counter (reintroduces a small
   accumulator — avoid), or simply DROP the sub-yamen nudges (a single returnee doesn't build a county
   office). Recommend DROP.
4. **The meters UNDER this one are OUT OF SCOPE here — but they are NOT equivalent, and only some are
   even candidates for future removal:**
   - `qing_council_effectiveness` — **KEEP, defensible (USER 2026-08-06).** It is already concrete-derived:
     computed (`se_QING_COUNCIL.txt:450+`) from the *average skill of the real seated Grand Council
     characters* + officer-corps martial + the ministry-performance fold (each filled ministry's
     `qing_min_perf_<office>`). It is a **readout of concrete character/office state**, not a free-floating
     accumulator — the same legitimate pattern `QING_bureau_reach` uses for buildings. This is the
     concrete-over-abstract rule working correctly; do not touch it.
   - `qing_bureau_integrity` (`:54`, `= 100 − qing_corruption_level`, −20 under a condition) and
     `qing_gov_corruption_drag` (`:86`, `= qing_corruption_level / 2`) — both are **derived restatements of
     `qing_corruption_level`**. `qing_gov_corruption_drag` is barely a meter at all (a one-line inline
     transform used only to drag the old capacity target).
   - `qing_corruption_level` itself — **CONFIRMED anti-pattern (audit 2026-08-06), a future concretization
     target.** It is a free-floating stored accumulator: seeded 12/0 (`se_QING_DECLINE.txt:76,78`) and moved
     ONLY by ~15 scattered `QING_DECLINE_nudge` calls (+12 scandal, −25 purge, ±2..6 censorate, etc.). It is
     NOT derived from the vanilla character `corruption` value — even though the mod already reads real
     per-character `corruption`/`has_trait=corrupt` all over `se_QING_DECLINE.txt` (e.g. :1581/:1635/:1676)
     to GATE events. Per the user's test ("defensible iff derived from character corruption, an actual
     vanilla value") it FAILS. The concrete fix — mirror council-effectiveness: derive it from the aggregate
     corruption of the seated GC + ministry office-holders, and convert the ±nudges into character-trait
     changes. This is a SEPARATE, larger task (~15 touch sites) — its own design doc, NOT this one.
   This doc kills exactly ONE meter — `qing_bureau_capacity` — the one whose concrete referent (the yamen)
   already exists on the map.
5. **`qing_bureau_integrity`'s own band** (`QING_GOV_apply_integrity_band`, meritocratic/venal) is a
   SEPARATE meter and stays — do not touch it in this task.
6. **Council-effectiveness is a HYBRID, kept for scope — not "pure concrete" (review #3 correction).**
   `QING_council_recompute` folds genuinely concrete terms (seated-member governing skill
   `se_QING_COUNCIL.txt:450`, officer-corps martial :525, and the ministry-perf meters which ARE concrete
   — holder martial/roster/garrison counts, `se_QING_MINISTRY.txt:189-254`) BUT also folds
   `qing_dynastic_harmony` (`:492`), which is itself a stored event-nudged accumulator (`se_QING_DYNASTY.txt`)
   — the very anti-pattern this program targets. So council_effectiveness is a hybrid; it is kept OUT OF
   SCOPE here for bounded-change reasons, not because it is fully concrete. (`qing_dynastic_harmony` is a
   candidate for a future concretization pass alongside corruption.)

### 4.5 — Decline semantics shift (from review #6)
Banding the capable/strained/paralysed modifiers on `QING_bureau_reach` (which starts at 100 and only
erodes) rather than the old rot-prone capacity meter **intentionally reframes the decline arc**: the
empire reaches `paralysed` not by *governance rotting under corruption/weak council*, but by *expanding
faster than it administers* (annexing uncovered provinces / losing covered ones). This is a deliberate
design choice, not a no-op. The governance-rot decline path it removes is **relocated, not lost** — it now
lives on the corruption band (`DESIGN_CORRUPTION_CONCRETIZE.md`), which once character-anchored will drive
the tax/PP/unrest penalties that a rotting bureaucracy should. Confirm this division is intended before
building; if a bureau-quality decline must remain HERE, keep a corruption term in the reach band.

## 5. Backward-compat / save games
- On the first pulse after this ships, `QING_GOV_init` should `remove_variable` the now-dead vars so stale
  saved meters don't linger: **`qing_bureau_capacity`, `qing_bureau_capacity_target`, `qing_yamen_band_cur`,
  `qing_yamen_band_prev`** (exact names — there is NO `qing_bureau_capacity_band_*`), and
  `qing_gov_corruption_drag` (the inline drag term, `se_QING_GOVERNANCE.txt:86`) if nothing else reads it.
  The derived svalue needs no migration — it reads live buildings already in the save.
- ⚠️ **HARD INVARIANT (review MEDIUM): ZERO surviving `QING_DECLINE_nudge` calls on `qing_bureau_capacity`
  or `qing_exam_ladder` may remain.** `QING_DECLINE_nudge` AUTO-CREATES its target var if absent (`if = {
  limit = { NOT = { has_variable } } set_variable = { value = 0 } }`), so ANY leftover nudge on a deleted
  var silently RESURRECTS it at 0 next pulse — defeating the `remove_variable` cleanup. So sites 9-13 + the
  keju writers (§9) are MANDATORY drops, not "recommend/optional/decide-per-event." If a capstone must cost
  administrative reach, it MUST use `remove_building_level = qing_yamen_building` (guarded `has_building`),
  NEVER a nudge on the dead var. Grep-gate the build: `rg 'QING_DECLINE_nudge.*qing_(bureau_capacity|exam_ladder)'`
  must return nothing.

## 6. Build checklist
1. ✅ **DONE: `max_amount = 1` (NOT `max_level`) on `qing_yamen_building` + `qing_shuyuan_building`** (§1a),
   stable owner-culture potential, NO city gate (USER). Fixes the admin exploit AND the coverage numerator.
2. Author `QING_bureau_reach` as a PURE svalue (covered-provinces ÷ city-provinces × 100, §3) — no cache.
3. `se_QING_GOVERNANCE.txt`: delete the seed (`:34`), target-compute + ±2 drift (`:80-98`), and
   `QING_GOV_yamen_band_track` (`:220-266`); repoint `QING_GOV_apply_capacity_band` to band on the reach.
4. Repoint the 9 mission/SelfStr gates (§2 sites 5-7) — **re-picked thresholds; classify coverage-floor
   vs build-up→count (§4.2).**
5. `se_QING_SELFSTR.txt`: change ONLY the `:694` term to `value = QING_bureau_reach`; KEEP `:695-697`
   (the +council_eff +integrity +÷3) — do not collapse the 3-way average (§2 row 8 / review #5).
6. DROP the 5 writer nudges (sites 9-13; per-event decision on demolish for the −15 capstones only).
7. Panel loc (site 14): "Administrative Reach: X% (N 衙門 / M seats)".
8. Delete orphaned passthrough svalues: `qing_bureau_capacity_target_cmpsvalue` (`00_event_values.txt:1859`,
   site 15) AND `qing_yamen_band_prev_cmpsvalue` (`00_event_values.txt:1913`, orphaned by deleting the
   band-track — review #8).
9. Stale-var cleanup in `QING_GOV_init` (§5 exact names).
10. §9: do the shuyuan/exam_ladder conversion in the SAME `se_QING_GOVERNANCE.txt` edit.
11. Review gates: no stored drift meter remains; yamen `max_level = 1`; reach counts covered PROVINCES not
    levels; every consumer reads concrete state; mission thresholds re-calibrated (not copied); SelfStr
    3-term average preserved; div/0 floor; decline-semantics reframe (§4.5) confirmed intended;
    brace/quote/BOM; boot-crash independent review.

---

## 9. PARALLEL CONVERSION — shuyuan (書院) ↔ `qing_exam_ladder` (item J)

Same disease, same cure, smaller surface. Deltas from the yamen/bureau_capacity case above:

### The current hybrid (to dismantle)
- Meter `qing_exam_ladder` (0–100, seed 60, `se_QING_GOVERNANCE.txt:40`) drifts ±2 toward
  `(bureau_integrity + council_effectiveness)/2 − exam_corruption_drag` (`:160-177`).
- `QING_GOV_shuyuan_band_track` (`:277-317`) buckets it into 3 bands (0=≤30, 1=>30, 2=≥70) and, on a
  band RISE, `add_building_level = qing_shuyuan_building` in the most-populous province; on a FALL,
  `remove_building_level`. Identical `band_cur`/`band_prev` idiom to the yamen. **DELETE this tracker.**
- 1763 seed: only TWO named academies — 嶽麓書院 (prov 2793) + 白鹿洞書院 (prov 2386),
  `se_QING_BUILDINGS.txt:215-217`. (Contrast the yamen, which blankets all city provinces.)

### The inversion
> **§9 was rewritten after adversarial review (2026-08-06).** The first draft copied the yamen's
> *conclusions* but DROPPED its two hardest fixes (`max_level=1`/count-provinces, and the mandatory
> recalibration). Because the shuyuan uses a count×K denominator that amplifies each building into a whole
> band, those fixes matter MORE here, not less. Corrected below.

- **Shuyuan: 1763-seeded (the 2 academies) + player-buildable, WITH `max_level = 1` (§9a).** The def
  (`qing_governance_buildings.txt:31-56`) exposes a satisfiable `allow` (`tech_education` + job slots) and
  cost 50 / time 180; keep it buildable, do NOT add a `potential` lock — BUT add `max_level = 1` (§9a).
- **`QING_exam_reach` = COVERED-PROVINCES × K, clamped 100 — NOT a level count (§9a, review #1).** The
  yamen's numerator lesson applies identically: count provinces-with-a-shuyuan, not building levels, or a
  player stacks N levels in one city to max reach. `value = { every_owned_province { limit = { has_building
  = qing_shuyuan_building } add = 1 } }  multiply = K  min 0 max 100`. **K is the calibration knob (§9c).**

### §9a — MANDATORY: `max_level = 1` on the shuyuan + covered-province numerator (review #1, CRITICAL)
Exactly mirrors §1a. `qing_shuyuan_building` has **no `max_level`** today — same exploit surface as the
yamen, and WORSE under count×K (each stacked level is amplified by K, hitting the ceiling even faster).
Add `max_level = 1`; count covered provinces. This is build-checklist step 1 for the shuyuan (there was no
§9 equivalent before). NOTE: unlike the yamen, the shuyuan does NOT feed #32 admin capacity, so the
exploit here is "trivially max exam_reach / vigorous band," not an admin-capacity exploit — but the fix is
the same and equally mandatory.

### Migration table (exam_ladder consumers — full census: 4 event writers + drift, ~5 readers)
| Site | Now | Becomes |
|---|---|---|
| `se_QING_GOVERNANCE.txt:40` seed=60 | seed meter | DELETE (derived) |
| `:157-189` target+drift | compute+±2 | DELETE |
| `:191-207` `QING_GOV_apply_exam_ladder_band` (vigorous ≥70 / clogged ≤30) | band on meter | KEEP the 2 modifiers; band on `QING_exam_reach` — **but see §9b: this is NOT a no-op, it severs the corruption→clogged signal** |
| `:277-317` `QING_GOV_shuyuan_band_track` (spawn/remove) | meter→building | DELETE (building is the input now) |
| `qing_keju_events.txt:82,105,382,563` (W: +8/−10/+4/−8) | nudge meter | **DROP the nudges** (review #2). Do NOT convert to add/remove_building_level: under count×K one academy ≈ a full band, so ±1 building is a sledgehammer vs the old ±8 drift, AND removing from the most-populous province would destroy a PLAYER-built academy (the yamen §2-row-13 concern). If a scandal must bite, apply a temporary `qing_exam_ladder_clogged`-style modifier, not a building removal. |
| `se_QING_EXAM.txt:78-79` `qing_exam_pass_rate` | **BASE term of a multi-term calc** (−corruption/2, −20 purchased-ranks, +civic, +curriculum, clamp — `:79-121`) | Change ONLY the `:79` value to `QING_exam_reach`; KEEP the subsequent terms (they're separate sequential statements, safe — review #7). Also DROP the `:78` `has_variable = qing_exam_ladder` guard (can't `has_variable` an svalue — review #3). Semantic note: pass_rate's base shifts from "ladder-health" to "academy-coverage". |
| `se_QING_CENSORATE.txt:116,165` gate `employer = { has_variable = qing_exam_ladder  var:qing_exam_ladder < 40 }` inside `ordered_character` | per-character gate | gate on the CACHED `qing_exam_reach_cache < 40` (review #3): the gate is inside an `ordered_character` limit (`se_QING_CENSORATE.txt:100,150`), evaluated per candidate — a live `every_owned_province`-sweep svalue would be O(court×provinces) per pulse. **This consumer REQUIRES a once-per-pulse cached read-var** (the one §3 exception). DROP the `has_variable` guard. RE-CALIBRATE the 40 threshold (§9c). |
| `se_QING_DECLINE.txt:1503` `has_country_modifier = qing_exam_ladder_clogged` (doubles keju.4 weight) | reads the band modifier | modifier KEPT, but its TRIGGER meaning changes (§9b) — the keju.4 doubling now fires on coverage, not corruption |
| `qing_governance_l_english.yml:177-181` band loc | — | UNCHANGED (band kept) |

### §9b — Decline-semantics reframe (review #4, mirrors §4.5)
Today `qing_exam_ladder` drifts DOWN under corruption (`qing_exam_corruption_drag`, `:165`) + weak
council/integrity (`:161`), so `qing_exam_ladder_clogged` is a **corruption/governance-rot** signal that
(a) doubles the keju.4 "brilliant scholar passed over" event (`se_QING_DECLINE.txt:1503`) and (b) widens
the censorate corruption net (the `<40` gates). Banding it on academy COUNT **severs that corruption→ladder
linkage**: "clogged" now means "few academies," not "the ladder rotted." Like §4.5, decide: either
re-inject a corruption term into `QING_exam_reach`'s band evaluation, or relocate the corruption-driven
keju/censorate coupling to the corruption band (`DESIGN_CORRUPTION_CONCRETIZE.md`). Do NOT ship this as a
silent "modifier UNCHANGED" — the trigger semantics change wholesale.

### §9c — MANDATORY calibration: the K squeeze (review #5, mirrors §4.2) — RESEEDED per research
**Historical research (2026-08-06, digest in the run log).** The mod seeds only **2** academies; history had
"thousands," with a hard structural anchor: the **1733 Yongzheng edict mandated a provincial academy in
every province → ~18–19 elite provincial-capital academies**, on top of the two most-famous (Yuelu, White
Deer Grotto). So the 2-academy seed under-represents the elite network by ~10×. Two build consequences:

1. **The two most-famous academies are now DISTINCT NAMED buildings (USER 2026-08-06), BUILT 2026-08-06:**
   `qing_yuelu_academy_building` (嶽麓, prov 2793) + `qing_bailudong_academy_building` (白鹿洞, prov 2386),
   defined in `qing_governance_buildings.txt`, seeded in `se_QING_BUILDINGS.txt` via a per-province site flag
   (`qing_is_yuelu_site` / `qing_is_bailudong_site` — `has_variable` `potential` gate, tighter than the
   Hanlin/Guozijian Zhili-region gate), loc + tooltips + placeholder icons done. Each `allow = always = no`
   (unique, seed-only), stronger than a generic shuyuan, below the capital Hanlin. **`QING_exam_reach` must
   count all three** (`has_building = qing_shuyuan_building` OR `qing_yuelu_academy_building` OR
   `qing_bailudong_academy_building`) so the named pair still contribute coverage.
2. **RESEED the generic provincial network** to the ~18-19 provincial-capital academies the 1733 edict
   implies (seed a generic `qing_shuyuan_building` at each of the ~18 province-capital provinces), so the
   1763 start reflects the real elite network, not a 2-point stub. Then **calibrate K against the reseeded
   count (~20 covered provinces incl. the 2 named)**, so the 1763 start reads **mid-band** (neither `≤30`
   clogged nor `≥70` vigorous — matches today's 60-seed intent):
   - With ~20 academies and the coverage denominator being city-provinces, pick K (or use the same
     coverage-fraction form as `QING_bureau_reach`) so ~20/denominator lands ~50–60.
   - The player then grows the network (more academies → vigorous) or lets it decay via loss (→ clogged).
**Still mandatory:** document the squeeze; verify the reseed lands (idempotent `NOT has_building` guard) and
that the named pair are counted. The reseed is a NEW build step (was not in the original §9).

### §9d — Backward-compat / orphan cleanup (review #6, mirrors §5 + checklist #8)
- `QING_GOV_init` (or the decline init): `remove_variable` the dead vars: `qing_exam_ladder`,
  `qing_exam_ladder_target`, `qing_exam_corruption_drag`, `qing_shuyuan_band_cur`, `qing_shuyuan_band_prev`.
- Delete orphaned passthrough svalues: `qing_exam_ladder_target_cmpsvalue` (`00_event_values.txt:1866`)
  and `qing_shuyuan_band_prev_cmpsvalue` (`00_event_values.txt:1908`).

### Build-order note
Do the yamen and shuyuan conversions in ONE `se_QING_GOVERNANCE.txt` edit — they share the file, the
`QING_GOV_pulse` dispatcher, and the band idiom; a half-done split leaves an inconsistent tracker.
