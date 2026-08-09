# DESIGN — #115: Yellow River Dike Breach — cost scales with dike count + add manpower cost

**Task (#3 in the 2026-08-09 overnight run):** `qing_works.1` ("The Yellow River Dike Breach")
charges a FLAT gold cost (335 expert / 380 standard, #1-rescaled) and levies NO manpower. Make
the treasury cost scale with the size of the dike network the throne already maintains, and add a
corvée manpower cost — mirroring the great-monument precedent (`QING_works_build_great_wall`
levies both `add_treasury` AND `add_manpower`).

This is the direct sibling of #114 (Examinations Convene): a concrete on-map building set already
exists (`qing_dike_building`, 4 seeded), so scale the cost off a single-source-of-truth count svalue,
exactly as #114 did with `QING_academy_count`.

---

## 1. Historical grounding (why cost RISES with dike count)

The Yellow River hydraulic-works budget (河工) is the textbook case of a state expense that
ballooned as the physical system grew: every new stretch of levee added a permanent maintenance
and flood-fighting liability, and by the late 18th–19th c. 河工 had become one of the largest and
most graft-ridden line-items in the Qing budget precisely *because* the dike network was so
extensive. So "the more dikes you maintain, the costlier the next repair" is not a gamey inversion —
it is the actual fiscal dynamic. Cost scaling UP with dike count is the correct direction.

(Contrast #114, where cost also rises with the academy network — a bigger exam is grander/costlier.
Same "bigger system = bigger bill" shape, independently justified.)

---

## 2. Current state (source of truth)

- **Verb** `QING_works_build_dike` (`common/scripted_effects/se_QING_WORKS.txt:149-208`), param `$cheap$`:
  - builds `qing_dike_building` at the most-populous minor-river province lacking one (`[#24 sweep]`
    guard already present — a valid province must exist before charging);
  - cost: `finesse >= 9` (expert) → `add_treasury = -335`; else (mediocre OR cheap) → `add_treasury = -380`
    (+corruption; cheap route +8, mediocre +4);
  - **NO manpower cost, NO internal treasury/manpower self-gate.**
- **Callers (3):**
  1. `qing_works.1` .a (cheap=no) and .b (cheap=yes) — `events/imp19c_mod_events/qing_works_events.txt:68-92`.
     Event-fire gate `treasury >= 400`; option .a gate = holder alive+employer only (NO treasury/manpower
     gate); option .c ("cannot afford") gate = `NOT holder OR treasury < 100`.
  2. `qing_works.5` .a (shoddy-dike follow-up, cheap=no) — `qing_works_events.txt:345`; option gate `treasury >= 400`.
  3. `qing_works_ministry_build_dike` (panel button, cheap=no) — `common/scripted_guis/QING_works_ministry_panel.txt:56-69`;
     `is_valid` = holder finesse≥7 + `treasury >= 380` + a dikeless province exists.
- **Precedent (treasury+manpower double levy):** `QING_works_build_great_wall` (`se_QING_WORKS.txt:430-472`)
  and `_grand_canal` (474-497): `add_treasury = -620/-595` AND `add_manpower = -10` (both `se_QING_WORKS.txt:449/490`),
  self-gated `treasury >= X  manpower >= 10  exists = capital_scope`. The dike is a smaller work than the
  great monuments, so it takes a smaller `-5` corvée levy (half the monument's 10), not the full 10.
- **Existing single-source-of-truth svalue pattern:** `QING_academy_count` (`QING_governance_svalues.txt:324`)
  — `value=0; every_owned_province{ limit={ has_building }; add=1 }`; #114 cost svalues consume it
  (`value = QING_academy_count  multiply = K  min/max`).

---

## 3. Design

### 3a. New svalues (`common/script_values/QING_governance_svalues.txt`)

Single source of truth for the dike network, then two cost tiers scaling off it. Placed adjacent to
the #114 block for discoverability. NO BOM (this file has none by design), LF.

```
QING_dike_count = {                # covered-province count of the dike building. ~4 at 1763 start
    value = 0
    every_owned_province = {
        limit = { has_building = qing_dike_building }
        add = 1
    }
}

# EXPERT tier (finesse >= 9): 4 dikes -> 335 (== the #1-rescale baseline it supersedes). +40/dike.
QING_dike_cost_expert_svalue = {
    value = QING_dike_count
    multiply = 40
    add = 175
    min = 175
    max = 700
}

# STANDARD tier (mediocre finesse<9 OR the cheap route): 4 dikes -> 380 (== old baseline). +40/dike.
QING_dike_cost_standard_svalue = {
    value = QING_dike_count
    multiply = 40
    add = 220
    min = 220
    max = 760
}
```

**Arithmetic / order of ops** (Jomini script_value applies operators top-to-bottom):
value=count → `multiply` → `add` → `min` (floor) → `max` (ceil). At count=4: expert 4·40+175=335,
standard 4·40+220=380 (start unchanged). At ~13 dikes: expert 695, standard ~740 (near cap). count=0
→ 175/220 (floors, no div/0 — there is no division anywhere).

**Why keep TWO tiers:** the finesse cost distinction (a capable minister builds cheaper) is an
existing, sensible mechanic — preserve it, scaling BOTH tiers with count (exactly as #114 preserved
the pass-rate quality axis while scaling the count axis). The task adds a count axis + manpower; it
does not ask to flatten the finesse axis.

### 3b. Verb `QING_works_build_dike` (`se_QING_WORKS.txt`)

1. **Add a manpower self-gate** to the build `if`'s `limit`: `manpower >= 5` (mirrors great_wall's
   `manpower >= 10` self-gate; manpower is not finesse-tiered so no branch ambiguity). Do NOT add a
   treasury self-gate — treasury is finesse-tiered and a self-gate on the wrong tier would silently
   drop the build; the three callers gate treasury (see 3c). This preserves current treasury behavior
   while making manpower atomic with the build.
2. **CHARGE BEFORE BUILD (applied-diff-review CRITICAL fix):** `add_building_level` applies
   immediately — the picked province reports `has_building` right after the call, and `QING_dike_count`
   / the cost svalues re-evaluate live on every reference. So the treasury charge MUST be read BEFORE
   the `ordered_owned_province { … add_building_level … }` block; charging after would read count=N+1 and
   overcharge by the +40/dike step (breaking both the 4→335/380 baseline and gate==charge). Order inside
   the build `if`: (a) finesse-tier treasury charge `if`, (b) flat `add_manpower = -5` (order-independent),
   (c) the `add_building_level` block LAST.
3. **Expert branch** (`finesse >= 9`): `add_treasury = -335` → `add_treasury = { value = QING_dike_cost_expert_svalue  multiply = -1 }`.
4. **Else branch** (mediocre/cheap): `add_treasury = -380` → `add_treasury = { value = QING_dike_cost_standard_svalue  multiply = -1 }`.
5. **LOG strings:** drop the now-stale literal "cost 335"/"cost 380"; replace with plain text
   ("cost = expert tier, scales with dike count; +5 corvée manpower" / "...standard tier..."). NO `#`
   or `$` in LOG strings (log-string-macro-rule).

### 3c. Callers — gate == charge (the #1 discipline)

All three gate treasury on the **STANDARD (higher) tier** + `manpower >= 5`. Gating on the higher tier
guarantees the player never dips into debt regardless of which finesse tier fires (an expert minister
between the two thresholds simply can't pick the option — the escape option covers that). RHS is a
named script_value → legal on `>=`/`<` (RHS-comparison rule; precedent `treasury >= army_size_merc_estimation_sg`).

- **`qing_works.1` .a** (`qing_works_events.txt`): add to its `trigger`:
  `treasury >= QING_dike_cost_standard_svalue` and `manpower >= 5` (keeps the existing holder-alive+employer conditions).
- **`qing_works.1` .b** (cheap): add a `trigger` with `treasury >= QING_dike_cost_standard_svalue` and `manpower >= 5`
  (it had none; the cheap route still builds a real dike with corvée labour, so it needs the same floor).
- **`qing_works.1` .c** (escape): widen its `trigger` OR-set so it shows whenever .a/.b are unaffordable —
  replace `treasury < 100` with `treasury < QING_dike_cost_standard_svalue`, and add `manpower < 5`.
  Guarantees no soft-lock (some option is always available). Preserves the "must act if you can afford it" flavor.
- **`qing_works.5` .a**: gate `treasury >= 400` → `treasury >= QING_dike_cost_standard_svalue` + `manpower >= 5`.
  Its `.b` (accept damage) is ungated → no soft-lock.
- **`qing_works_ministry_build_dike`** panel `is_valid`: `treasury >= 380` → `treasury >= QING_dike_cost_standard_svalue`,
  add `manpower >= 5`. (Touching this button is REQUIRED for gate==charge — it shares the verb; not scope creep,
  same rationale as #114 touching the ministry buttons that shared the keju verb.)

Event-fire trigger `treasury >= 400` stays: a flood crisis fires regardless of wealth; if the scaled
cost exceeds the treasury, .c ("we cannot afford it") is the intended outcome.

### 3d. Localization (`localization/english/qing_works_l_english.yml` + `qing_works_ministry_l_english.yml`)

Show the live cost + manpower. **Two forms, each on its proven ground (design-review M1 fix):**
- **Event tooltips** (`qing_works.1.a.tt`, `.1.b.tt`, `.5.a.tt`) use #114's proven var-read form
  `[Player.MakeScope.GetVariable('qing_dike_cost_display').GetValue|0]` — the var is populated in each
  event's `immediate` (all three events HAVE an `immediate`) via `set_variable`. This is the exact form
  #114 ships (`qing_office_events_l_english.yml:134,136` ← `se_QING_EXAM.txt:226-227`).
- **Panel button** (`QING_WORKS_MINISTRY_BUILD_DIKE_TT`) uses the live datafunction
  `[GuiScope.SetRoot(Player.MakeScope).ScriptValue('QING_dike_cost_standard_svalue')|0]` — the ONLY
  form that works for a scripted_gui, which has no `immediate` to stash a var. Proven on the
  scripted_gui/interface side: `sell_selected_provinces` (`sell_province_l_english.yml:4`),
  `tech_bonus_manufactories` (`core_l_english.yml:573`).

**Why the split:** the design-review flagged (M1) that the live `ScriptValue` form has NO in-repo
precedent in an *event-option* tooltip — only #114's `GetVariable` form does. Rather than bet an
unproven form on the event side for cosmetic uniformity, each site uses the form already proven for its
context. Both show the STANDARD-tier number (== the gate), with a note that a finesse-9 minister pays less.

The display var: a new `QING_DIKE_set_display_cost` helper (in `se_QING_WORKS.txt`) does
`set_variable = { name = qing_dike_cost_display  value = QING_dike_cost_standard_svalue }`; each of the
three events calls it in `immediate`. (Same-tick COUNTRY set-then-read is proven safe — #114
`se_QING_EXAM.txt:84-87`; the immediate runs before the window renders, so the tooltip reads it.)

- `qing_works.1.a.tt`: "...build a well-maintained river dike (河堤). Costs #Y [live] treasury and 5
  manpower (人力)#!, and rises with the size of the dike network (河工) you maintain — a truly expert
  Minister (finesse 9+) builds for less."
- `qing_works.1.b.tt`: add "#Y [live] treasury and 5 manpower#!" + keep the corruption/recurring-flood warning.
- `qing_works.5.a.tt`: mirror .1.a.tt's cost clause.
- `QING_WORKS_MINISTRY_BUILD_DIKE_TT`: replace "a treasury of 380" with the live-svalue clause + "and 5 manpower".

No `_desc` / mission keys touched. BOM + LF preserved (both loc files have BOM).

---

## 4. Files touched

| File | Change |
|---|---|
| `common/script_values/QING_governance_svalues.txt` | +3 svalues (count, expert, standard) |
| `common/scripted_effects/se_QING_WORKS.txt` | verb: manpower gate + `add_manpower=-5` + 2 treasury→svalue swaps + LOG text; new `QING_DIKE_set_display_cost` helper |
| `events/imp19c_mod_events/qing_works_events.txt` | `.1` .a/.b/.c gates, `.5` .a gate; `.1`+`.5` `immediate` calls display-cost helper |
| `common/scripted_guis/QING_works_ministry_panel.txt` | dike button `is_valid` treasury→svalue + manpower |
| `localization/english/qing_works_l_english.yml` | .1.a.tt/.1.b.tt/.5.a.tt live cost + manpower |
| `localization/english/qing_works_ministry_l_english.yml` | DIKE_TT live cost + manpower |

## 5. Invariants to verify (applied-diff review)

- Braces balanced in every touched file; BOM per convention (svalues none; se_ / events / loc BOM);
  no EOL churn (numstat == `--ignore-cr-at-eol` numstat).
- svalue arithmetic: count=4 → expert 335 / standard 380 (start unchanged); monotone up; capped.
- Every treasury gate == the tier actually charged, or higher (never lower → never surprise debt).
  Enumerate: .1.a, .1.b, .1.c-inverse, .5.a, panel — all reference `QING_dike_cost_standard_svalue`;
  verb charges expert(≤standard) or standard.
- `manpower >= 5` present at all 3 gate sites + the verb self-gate; `add_manpower = -5` levied exactly once per build.
- RHS-comparison: every `treasury >=/<` RHS is a literal or the named svalue (never `var:`).
- No `#`/`$` in any LOG string; loc datafunction spelled exactly as the proven precedent.
- No soft-lock: for any (holder, treasury, manpower) state, at least one option of qing_works.1 shows;
  qing_works.5 .b always shows.
```
