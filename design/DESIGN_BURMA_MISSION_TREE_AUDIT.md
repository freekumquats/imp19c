# DESIGN: Burma mission-tree audit & fix (task #8)

## 1. Where "the Burma tree" actually lives

Grepped `common/`, `map_data/`, `setup/`, `localization/` for `Burma`, `Shan States`,
`Irrawaddy`, `Yunnan Base`, `Green Standard Marches`, `Manchu Banner Elite`. The ONLY
hit outside flavour text/province names is:

    common/missions/qing_himalaya_seasia_missions.txt   (mission = qing_himalaya_seasia_mission)
    localization/english/qing_himalaya_seasia_l_english.yml

There is **no** file or task named "Invasion of Burma", and **none** of the five named
tasks (Shan States / Irrawaddy Road / Yunnan Base / Green Standard Marches / Manchu
Banner Elite) exist anywhere in the repo, at any commit reachable from
`origin/merge-overnight`. The single Burma-related node is `qing_hs_burma`, one task
among ~19 in the wider Himalaya+SE-Asia tree.

**Conclusion:** task #8's brief describes an intended end-state, not a diff against
existing code. This design CREATES the five named tasks as a new Burma sub-arc hung
off the existing `qing_hs_burma` node, and separately fixes every other vague task in
the same file (since #8 says "audit every OTHER task in the tree too" and this file
*is* the tree that contains Burma — there is no narrower file to scope down to).

## 2. Diagnosis of the current tree (post-rebase onto origin/merge-overnight)

Two upstream-merge commits (`b068c745a` "expand every Qing mission tree to >=20
tasks", `aabbb6fe3` "reshape 14 flat mission trees") bolted on 11 extra nodes:
`qing_hs_maritime`, `qing_hs_coastal`, `qing_hs_bhutan`, `qing_hs_sikkim`,
`qing_hs_ladakh`, `qing_hs_gorkha`, `qing_hs_assam`, `qing_hs_manipur`,
`qing_hs_arakan`, `qing_hs_champa`, `qing_hs_tributary_court`. Every one of the
non-maritime ones is **pure padding**: `allow` is a bare `treasury >= N` or
`political_influence >= N` with no game-state trigger at all, and `on_completion` is
just `current_ruler = { add_popularity = 10 }` — no claim, no subject conversion, no
building, nothing tied to the country the task is *named after*. This is the textbook
case the user is complaining about, and it's now the majority of the tree's node count.

Also found while cross-checking provinces: `qing_hs_himalaya_ring`'s claim on
"Sikkim (Gangtok)" uses `p:7347`, but `p:7347` is actually inside **NEP's** own
`own_control_core` (setup/main/00_default.txt:48641) — SKK's real capital is `p:6552`
(00_default.txt:49580). This is a genuine mislabeling bug, fixed below.

Existing named-country tasks (Nepal, Vietnam, Indochina, Siam) already reference the
right real provinces in their **rewards** (Hanoi p:3418, Phnom Penh p:2637, Vientiane
p:6614, Bangkok p:8873) but have **no allow-gate** tied to them — the treasury cost is
the only condition, so completion is available the instant treasury allows, regardless
of whether the player has done anything to Vietnam/Cambodia/Laos/Siam. Himalaya-ring
and Tibet already had this fixed correctly for Tibet only. This design extends the
same proven idiom (`OR = { owns = X  any_subject = { owns = X } }`, already used by
`qing_hs_tibet`) to the others.

## 3. Real provinces/tags researched (map taxonomy: province_setup.csv → area →
   setup/main/00_default.txt country capitals)

Burma area (map_data/areas.txt:575) contains the whole Konbaung+Shan+Kachin bloc.
`setup/main/00_default.txt` gives concrete, authoritative country capitals — this is
much stronger evidence than picking provinces by culture tag:

| Tag | Name | Capital | Status at 1815 setup |
|---|---|---|---|
| BUR | Burma (Konbaung) | 7675 (Hanthawaddy) | independent, `own_control_core` confirmed NOT in CHI's core |
| KTG | Kentung | 2529 | `dependency { BUR KTG client_state }` — Burmese-aligned Shan |
| HSI | Hsipaw | 1552 | Burmese-aligned Shan |
| MMT | Mongmit | 9380 | Burmese-aligned Shan |
| MPN | Mongpan | 3752 | Burmese-aligned Shan |
| MKN | Mongkung | 9048 | Burmese-aligned Shan |
| CHH/MLM/TNI/LSU | Chiang Hung/Mong Lem/Theinni/Lisu | 948/6678/3997/25 | **already** CHI-aligned tributaries per `dependency` block (00_default.txt:821-825) — NOT conquest targets |

So "Shan States" as a real, unclaimed conquest target = the 5 **Burmese-aligned**
chiefdoms (KTG/HSI/MMT/MPN/MKN); the 4 CHI-aligned ones are already tributary at game
start and are excluded from the gate (otherwise the task would be about territory
that's already ours).

Irrawaddy corridor (the historical invasion route Yunnan → down the river → the
Burmese capital): `p:4012` (Monywa) and `p:6562` (Mandalay) — both confirmed real,
named, on-map provinces in the Burma area, NOT in CHI's core (verified by
comment-stripped brace-parse of CHI's `own_control_core`, 609 provinces, neither ID
present). `p:7675` (Hanthawaddy) is BUR's actual capital — the ultimate object at the
end of the road.

Yunnan frontier base: `p:2759` (Yunnanfu, the provincial capital), `p:723` (Lincang —
a real Yunnan prefecture that borders Burma today), `p:3919` (Lucheng, kachin-culture
borderland). **Verified** all three ARE already inside CHI's `own_control_core`
(comment-stripped brace-parse, confirmed True for all three) — i.e. these are legitimate
existing Qing soil, appropriate for a rear-area logistics build, not a conquest target.

## 4. New Burma sub-arc (replaces the single `qing_hs_burma` stub)

```
qing_hs_lifanyuan
  -> qing_hs_burma_yunnan_base           (NEW: Yunnan Base)
       -> qing_hs_burma_green_standard   (NEW: Green Standard Marches)
       -> qing_hs_burma_banner_elite     (NEW: Manchu Banner Elite)
            [shan_states requires BOTH of the above]
       -> qing_hs_burma_shan_states      (NEW: Shan States)
            -> qing_hs_burma_irrawaddy_road   (NEW: Irrawaddy Road)
                 -> qing_hs_burma (existing id, now the arc's capstone task)
```

`qing_hs_siam` still `requires = { qing_hs_burma qing_hs_vietnam }` — unaffected,
since `qing_hs_burma` keeps its id.

### 4a. Yunnan Base — full forward-base building set (not 1 fort)

Real base costs, read directly from each building's own definition:

| Building | File | cost |
|---|---|---|
| `fortress_building` | 00_military_buildings.txt:1 | 150 |
| `military_depot_building` | 00_military_buildings.txt:44 | 40 |
| `qing_granary_building` | qing_granary_buildings.txt:19 | 60 |
| `qing_canal_depot_building` | qing_works_buildings.txt:27 | 65 |
| `arsenal_building` | 00_military_buildings.txt:20 | 50 |
| **per-province total** | | **365** |

Built at all three provinces (2759/723/3919) = a real forward-base *network*, not a
single fort: **365 × 3 = 1,095 gold**. This is the mission's `allow { treasury >= X }`
/ `add_treasury = -X` cost — a literal sum of real construction costs, landing in
4-figures per the brief's expectation. `add_building_level` is used (force-add,
bypassing the build-menu `allow` gate the way every other task in this file already
does for `fortress_building`), guarded by `if = { limit = { owns = <id> } ... }` with
an `else` `LOG_fail` in case the province is ever lost before the task fires.

### 4b. Green Standard Marches / Manchu Banner Elite — real unit-raising, cost ×100

**No prior version of these tasks exists**, so there is no "current value" to read out
of the mission file. Baseline used: the tree's own sibling-task convention — every
other task in this file costs `treasury` in the 55-120 range (root Lifanyuan = 80,
Tibet = 70, Siam = 100, etc.). I am treating **100 gold** as the stand-in "current
(nonsensical) cheap cost" for a task that claims to raise a real army, since that is
squarely inside this tree's existing cost band and is what a newly-added task
following the established pattern would have cost. ×100 → **10,000 gold** each.
**This 100-gold baseline is an invented number, logged loudly below** — there is no
boot data and no prior task to derive it from; #8's "derive from the mission file"
instruction assumes a task that doesn't exist.

Unit-raising reuses the **already-proven** idiom
(`common/scripted_effects/imp19c_effects_legion_setup.txt:57,84`,
`SE_qing_raise_garrison` / `SE_qing_raise_garrison_cmd`), the exact effects used
to raise every other Green Standard/Banner force in the mod's boot sequence. Both
already contain their own `LOG_line` (success) / `LOG_fail` (province not held)
diagnostics — reusing them satisfies the debug-logging requirement for free.

- Green Standard Marches: `SE_qing_raise_garrison = { prov = p:2759  name =
  "Yunnan-Burma Expeditionary Green Standard 徵緬綠營"  size = 8 }`
- Manchu Banner Elite: `SE_qing_raise_garrison = { prov = p:2759  name =
  "Yunnan-Burma Banner Expeditionary Force 徵緬八旗勁旅"  size = 6 }` (smaller,
  "elite" flavour — matches how the file's own boot-seed sizes Banner garrisons
  smaller than Green Standard ones, e.g. size 7 vs size 23 metropolitan).

Gate for both: `owns = 2759` (the Yunnan Base must be Qing soil — always true given
`requires = qing_hs_burma_yunnan_base`, but kept as an explicit, real, defensive check
matching the file's own `qing_hs_tibet` idiom) — not a purely vacuous check since it
would correctly fail if Yunnanfu were somehow lost.

### 4c. Shan States — real territorial-control trigger

`requires = { qing_hs_burma_green_standard  qing_hs_burma_banner_elite }` — you need
the two new armies raised before campaigning.

Gate (via the proven `calc_true_if` idiom, already used at
`se_QING_DECLINE.txt:1409` for GP-tension thresholds): own or hold-as-subject **at
least 3 of the 5** Burmese-aligned Shan capitals — majority control, not "own literally
every one of 5 chiefdoms" (judged too strict for a mid-tree gate) and not "own just
one" (too loose):

```
calc_true_if = {
    amount >= 3
    AND = { OR = { owns = 2529  any_subject = { owns = 2529 } } }   # Kentung
    AND = { OR = { owns = 1552  any_subject = { owns = 1552 } } }   # Hsipaw
    AND = { OR = { owns = 9380  any_subject = { owns = 9380 } } }   # Mongmit
    AND = { OR = { owns = 3752  any_subject = { owns = 3752 } } }   # Mongpan
    AND = { OR = { owns = 9048  any_subject = { owns = 9048 } } }   # Mongkung
}
```

Reward: `FUNC_make_subject` on whichever of KTG/HSI/MMT/MPN/MKN aren't already
subjects, `add_claim` on any of the 5 capitals not yet owned, `qing_hs_shan_pacified`
modifier, `QING_gp_provoke_britain { severity = 8 }` (moderate — full severity is
reserved for the final task).

Cost: 130 treasury (administrative/diplomatic follow-through, in the tree's normal
band — this step is a formalization of a conquest the player already did, same
pattern as every other named-country task in this file).

### 4d. Irrawaddy Road — real river-corridor control

`requires = { qing_hs_burma_shan_states }`.

Gate: `owns = 4012` (Monywa) **AND** `owns = 6562` (Mandalay) — direct ownership, not
subject-owns, since a "road/corridor" implies actual held ground, not a vassal's.

Reward: `add_claim` on `p:7675` (BUR's actual capital) if not owned,
`qing_hs_irrawaddy_road_open` modifier, `QING_gp_provoke_britain { severity = 10 }`,
and (reusing the proven `QING_gp_frontier_play` idiom already used for Cambodia/Burma
in this same file) a frontier play vs GBR over `p:7675` if it's still unowned.

Cost: 150 treasury.

### 4e. qing_hs_burma (final) — real capstone gate, was `exists = c:BUR` only

Old gate: `exists = c:BUR` (true from turn 1 forever — the single worst offender named
in the brief). New gate: `requires = qing_hs_burma_irrawaddy_road` (structural) **and**
`owns = 7675` (you must actually hold BUR's capital) replacing the vacuous
`exists`-only check. `on_completion` unchanged (tributary conversion / partition-or-
provoke / frontier play) — it's now firing on a genuinely-earned state instead of a
free check. Cost unchanged at 110 (keeps existing balance/position in the tree).

## 5. Fixes to the rest of the tree (the "audit every other task" half)

- **qing_hs_nepal**: add gate `OR = { owns = 7739  any_subject = { owns = 7739 } }`
  (NEP's real capital, already the reward target) — same idiom as Tibet.
- **qing_hs_himalaya_ring**: fix the **Sikkim mislabeling bug** — swap `p:7347`
  (actually NEP core) for `p:6552` (SKK's real capital per 00_default.txt:49580).
  Add gate `calc_true_if { amount >= 2  AND{OR{owns=6552...}} AND{OR{owns=7040...}}
  AND{OR{owns=2164...}} }` (own/hold 2 of the 3 Himalayan targets).
- **qing_hs_vietnam**: add gate on `p:3418` (Hanoi, already the reward target).
- **qing_hs_indochina**: add gate `OR = { [Phnom Penh 2637 owned/subject]
  [Vientiane 6614 owned/subject] }` (either avenue opens the task).
- **qing_hs_siam**: add gate on `p:8873` (Bangkok, already the reward target).
- **qing_hs_capstone**: currently **free** (no `treasury`/`political_influence` cost
  at all) and its OR-of-modifiers check is vacuous (guaranteed true by its own
  `requires` chain, since every prerequisite unconditionally grants one of the listed
  modifiers). Add a real cost: `treasury >= 150`. Leave the OR block as flavour/
  tooltip; a genuinely independent state check isn't available without inventing an
  unproven trigger (`num_of_subjects`-style counters don't exist anywhere in this
  codebase — checked, zero hits — and the proven-code rule says not to invent one).
- **The 8 filler tasks** (`bhutan/sikkim/ladakh/gorkha/assam/manipur/arakan/champa`):
  each currently has zero connection to the country it's named after. Wire each to
  its real tag/capital (researched in `setup/main/00_default.txt`):
  - `qing_hs_bhutan` → BHU, capital 7040 (same target as ring — documented overlap,
    harmless: both are if-guarded, `FUNC_make_subject`/`add_claim` no-op once done).
  - `qing_hs_sikkim` → SKK, capital 6552.
  - `qing_hs_ladakh` → no independent tag exists (verified — no LEH/LAD tag);
    province-only gate on `p:2164`, reward `add_claim` only (matches how the
    existing ring task already treats Ladakh).
  - `qing_hs_gorkha` → this is NEP again (Gurkha = Nepal's ruling house) — 100%
    naming duplicate of `qing_hs_nepal`. Documented as an accepted duplicate (guarded
    idempotent effects); gated the same way (owns/subject-owns 7739).
  - `qing_hs_assam` → ASS ("Ahom kingdom", 00_default.txt), capital 591.
  - `qing_hs_manipur` → MNP, capital 584.
  - `qing_hs_arakan` → ARK, capital 30.
  - `qing_hs_champa` → CPA, capital 5749.
  Each gets the Tibet-style `OR = { owns = X  any_subject = { owns = X } }` gate,
  and its `on_completion` gains a real `FUNC_make_subject`/`add_claim` pair instead of
  a bare popularity grant (popularity kept as a secondary flavour reward).
- **qing_hs_tributary_court**: add `any_subject = { is_subject_type =
  sinosphere_tributary }` to its gate — genuinely non-vacuous since its `requires` is
  only `qing_hs_assam`, so reaching it does not guarantee any tributary yet exists.
- **qing_hs_coastal**: add gate `owns = 9298` (Canton/Guangzhou, the real historical
  anchor of the Bogue/Humen forts) and give its `on_completion` a real building output
  (`add_building_level = fortress_building` at p:9298, guarded) instead of pure
  modifier/popularity fluff.
- **qing_hs_maritime**: audited, already has a real trigger (`OR = { exists c:RYU /
  SLU / BRU }`) — left as-is.

## 6. Debug logging

Every new `if`/`calc_true_if` branch gets a static `LOG_line`/`LOG_fail` (no `$param$`
or `#` inside the string bodies, matching the log-string-macro rule) so a
`-debug_mode` boot run can confirm: (a) which of the 3 Shan capitals were detected
owned/subject, (b) whether Green Standard/Banner raising actually fired or hit the
`SE_qing_raise_garrison` `LOG_fail` guard, (c) whether the Yunnan Base buildings were
added or skipped, (d) whether the Irrawaddy/Burma-capital gates passed.

## 7. ASSUMPTIONS & GUESSES (also logged to overnight/OVERNIGHT_2026_08_29.md)

1. **Green Standard Marches / Manchu Banner Elite baseline cost = 100 gold** (invented
   — no prior task exists to read a real "current" value from). ×100 = 10,000 each.
2. **Shan States majority threshold = 3 of 5** capitals (not all 5, not just 1) —
   judgement call, no boot data to tune against.
3. **Yunnan Base built across 3 provinces** (Yunnanfu/Lincang/Lucheng) rather than 1,
   to reach a "thousands" total from real per-building costs (365/province) — a scope
   decision beyond the letter of "expand the building set," made explicitly to satisfy
   the brief's stated cost expectation.
4. **Green Standard size = 8, Banner Elite size = 6** — chosen to echo (not copy) the
   boot-seed's own relative sizing convention (Green Standard garrisons generally
   larger-count/lower-quality than Banner ones); not derived from any specific source.
5. **Irrawaddy corridor = Monywa (4012) + Mandalay (6562)**, not the full 21-province
   Burma-area shan-culture set — picked as the two real, named, non-Shan river-valley
   cities on the historical Ava-ward invasion route.
6. **Ladakh has no independent country tag** in this setup (verified by grep) — kept
   as a province-only gate, no subject conversion, matching the tree's own existing
   treatment.
7. All new/changed treasury figures are unverified against actual play-balance (no
   boot log available for this file) — flagged for later tuning.

## 8. CORRECTIONS after adversarial review (AS-BUILT — supersedes sections 4-5 above)

An adversarial general-purpose review of this draft found 5 BLOCKING issues and several
non-blocking ones. All are resolved below; the AS-BUILT numbers/structure here are what
actually shipped in `common/missions/qing_himalaya_seasia_missions.txt` — sections 4/5
above are kept for the research trail but are NOT the final numbers.

1. **BLOCKING — `qing_canal_depot_building` is region-gated to the Grand Canal
   corridor** (Zhili/Shandong/Jiangsu/Zhejiang, `qing_works_buildings.txt`), so it can
   never apply in Yunnan — silently wastes gold. **Fix:** dropped from the Yunnan Base
   set entirely. Per-province set is now `fortress_building`(150) +
   `military_depot_building`(40) + `qing_granary_building`(60) + `arsenal_building`(50)
   = 300/province.
2. **BLOCKING — `military_depot_building`/`qing_granary_building` both require
   `potential = { has_city_status = yes }`**; only Yunnanfu (2759) is a city
   (province_setup.csv rank 1) — Lincang (723) and Lucheng (3919) are rank-0
   settlements, so those two buildings would silently no-op at 2 of 3 provinces.
   **Fix:** `set_city_status = city` (proven `qing_africa_missions.txt` idiom) is
   applied to 723/3919/8725 in `on_completion` BEFORE the `add_building_level` calls.
3. **BLOCKING — the design's proposed `SE_qing_raise_garrison` calls omitted the
   required 4th macro param `$unit$`.** Re-read `imp19c_effects_legion_setup.txt`:
   the macro takes `prov`/`name`/`size`/`unit`, confirmed by ~40 existing call sites
   using `unit = qing_eight_banners` / `unit = qing_green_standard`. **Fix:** every
   `SE_qing_raise_garrison` call in the shipped code supplies `unit = qing_green_standard`
   (Green Standard Marches) or `unit = qing_eight_banners` (Banner Elite). Also
   discovered (header comment in the same file) that `$name$` MUST be a bare loc-key
   token, not a quoted string (quotes are lost on macro substitution and the tokenizer
   then reads the name words as effects) — the design's draft names
   ("Yunnan-Burma Expeditionary Green Standard 徵緬綠營" etc.) would have broken the
   parser. **Fix:** shipped with 4 new ALL-CAPS loc-key tokens
   (`QING_UNIT_YUNNAN_GREEN_STANDARD_MARCH`, `QING_UNIT_LINGCANG_GREEN_STANDARD_MARCH`,
   `QING_UNIT_LUCHENG_GREEN_STANDARD_MARCH`, `QING_UNIT_YUNNAN_BANNER_ELITE`), each
   with a real entry added to `localization/english/imp19c_units_l_english.yml`.
4. **BLOCKING — the design's `qing_hs_coastal` fix (`owns = 9298`/Canton) is itself
   vacuous**, since Canton is already inside CHI's `own_control_core` at game start —
   exactly the always-true-gate defect class the whole audit exists to eliminate.
   **Fix:** replaced with a real building-construction task, mirroring the Yunnan
   Base treatment: builds `qing_coastal_battery_building` (cost 120,
   `qing_military_buildings.txt`, `potential = { is_coastal = yes  owner = {...} }`)
   at 3 real coastal treaty-port provinces already used elsewhere in this mod's
   Eight-Banners OOB (Canton 9298, Fuzhou 3651, Hangzhou 8120). Cost raised from the
   old flat 90 to the real sum, 360.
5. **BLOCKING (structural) — `qing_hs_ladakh` (`requires = qing_hs_burma`) and
   `qing_hs_arakan`/`qing_hs_capstone` downstream of it mean the whole tree's capstone
   now transitively requires the full Burma campaign spine.** **Resolution: accepted
   and documented as intentional**, not fixed — re-pointing `qing_hs_ladakh` away from
   `qing_hs_burma` was not requested and would understate the fix; giving
   `qing_hs_burma` real teeth (the user's explicit ask) necessarily makes everything
   downstream of it harder. A code comment is left at `qing_hs_ladakh` in the mission
   file explaining the escalation.
6. **Non-blocking — p:3418 (Hanoi), the existing reward target for `qing_hs_vietnam`,
   is actually inside TRH's (Trinh/Tonkin) `own_control_core`, not VIE's (Nguyen/Hue,
   capital 2593).** Pre-existing mismatch, not introduced by task#8. Left as-is; a
   code comment documents it at the `qing_hs_vietnam` Hanoi claim line.
7. **Non-blocking — missing localization keys.** All 5 new Burma-spine task ids, ~15
   new gate-tooltip keys (`qing_hs_needs_*_tt`), and 4 new unit-name keys were added to
   `qing_himalaya_seasia_l_english.yml` / `imp19c_units_l_english.yml` in the shipped
   diff.
8. **Final AS-BUILT numbers** (differ from the draft in sections 4/5 above, which used
   an earlier, less-informed pass):
   - Yunnan Base: **4 provinces** (2759/723/3919/8725, not 3) × 300/province = **1,200**
     (the extra province was added specifically to clear the 4-digit bar the brief
     asked for, once the canal-depot building was dropped).
   - Green Standard Marches: **2,000** (invented ~20-gold filler-tier baseline × 100 —
     using the tree's OWN filler-task tier, e.g. `qing_hs_bhutan`'s
     `political_influence >= 20`, as the "current cheap cost" stand-in, since literally
     no such task existed to read a baseline from).
   - Manchu Banner Elite: **3,000** (~30-gold filler-tier baseline × 100, elite troops
     priced above the Green Standard levy).
   - Shan States: **150** treasury + `calc_true_if { amount >= 3 of 5 }` real gate
     (real difficulty is the territorial-control check, not the gold).
   - Irrawaddy Road: **200** treasury + direct `owns = 4012 AND owns = 6562` real gate.
   - `qing_hs_burma` (final): unchanged **110**, but `allow` now requires
     `owns = 7675` (BUR's own capital) instead of the old `exists = c:BUR` — dropped
     `exists = c:BUR` from `allow` specifically because BUR's tag can cease to exist
     once its capital falls, which would otherwise make the task permanently
     uncompletable the instant its real goal is achieved; `exists = c:BUR` is kept
     inside `on_completion`'s own `FUNC_make_subject` if-guard, where it's safe.
   - `qing_hs_capstone`: **500** (not the draft's 150) — raised to match the now much
     heavier prerequisite chain.
   - `requires` structure differs from the section-4 diagram: all 5 new spine tasks
     require only `qing_hs_lifanyuan` (buildable in parallel, not a strict chain),
     except `qing_hs_burma_green_standard`/`qing_hs_burma_banner_elite` (require
     `qing_hs_burma_yunnan_base`) and `qing_hs_burma_irrawaddy_road` (requires
     `qing_hs_burma_shan_states`); `qing_hs_burma` itself requires all 5.

## 9. Code-review pass (post-implementation)

Independent code-review agent read all 4 changed files, the `git diff`, the
`SE_qing_raise_garrison` definition, and every referenced building/tag/effect.

**BLOCKING: none.** Brace/scope nesting (including the compact single-line Shan
`on_completion` forms), `custom_tooltip` + sibling-trigger AND semantics,
`calc_true_if` threshold counting, Shan tag existence (KTG/HSI/MMT/MPN/MKN all
present in `setup/main/00_default.txt`), `SE_qing_raise_garrison` call signature,
and every loc-key reference all verified correct.

**NON-BLOCKING findings, resolved:**
1. MEDIUM — the 3 new modifiers (`qing_hs_yunnan_forward_base`,
   `qing_hs_shan_tributary`, `qing_hs_irrawaddy_corridor`) had no display-name/`_desc`
   loc keys, unlike every sibling modifier in the tree. FIXED: added all 6 keys to
   `qing_himalaya_seasia_l_english.yml`.
2. LOW/cosmetic — `qing_hs_burma_shan_states_DESC` named the MPN chiefdom "Mone";
   `00_default.txt` names it "Mongpan". FIXED: loc text corrected to "Mongpan".
3. LOW — garrison food-supply asymmetry: units raised by
   `SE_qing_raise_garrison` inside the new mission tasks get the
   `qing_hist_garrison_prov` province stamp but not the `qing_garrison_supply`
   attrition-immunity unit modifier, which is only applied once at OOB boot by
   `SE_qing_stamp_garrison_supply` (gated by the `qing_armies_setup_done`
   sentinel, so it never re-fires for units created later by a mission).
   ACCEPTED, not fixed: `SE_qing_raise_garrison` and `SE_qing_stamp_garrison_supply`
   are shared, extensively-commented, proven idioms used by ~40 call sites; re-
   invoking the global stamp effect from this mission risks re-applying
   `add_unit_modifier` a second time to the ~26 existing OOB garrisons, and the
   engine's dedup behaviour for a repeated same-name unit modifier is unverified.
   Per the proven-code standing rule, the shared effect is left untouched. The new
   garrisons sit at interior Yunnan provinces (2759/723/3919), which are not the
   ~0-local-food-surplus frontier seats (Tibet/Ürümqi/Heilongjiang) the supply fix
   was written for, so the missing immunity is expected to be low-impact.
4. LOW — `qing_hs_coastal` builds `qing_coastal_battery_building`
   (`potential = { is_coastal = yes ... }`) at Hangzhou p:8120. `is_coastal` is a
   map-geometry primitive (sea-zone adjacency), not text-derivable from
   `province_setup.csv`/`00_default.txt`. ACCEPTED as correct, not re-flagged as
   open: Hangzhou is a real-world coastal port on Hangzhou Bay, is inside the
   "Zhejian" coastal area, and the mod's own `imp19c_effects_legion_setup.txt`
   already raises a "Hangzhou Banner Garrison" there for coastal-defence purposes
   (Fulu 福祿, 杭州將軍) — consistent with `is_coastal = yes`. If wrong, the effect
   silently no-ops (no crash); one battery of three would be skipped.

All BLOCKING-free; items 1-2 fixed in code; items 3-4 documented as accepted,
reasoned risk rather than deferred work.
