# DESIGN — #95 broad LAWS sweep: non-Qing law audit (loc + tech-prereq spot-check)

> STATUS 2026-08-12: REVIEW ROUND 2 — CONFIRMED ACCURATE. Round 1 found the original draft's
> placeholder-desc count (27) undercounted the real figure (68) by more than 2x, and the group/
> option totals were wrong (claimed 90/362 total, 44/228 non-Qing). Round 2 independently
> re-derived every number from scratch (two separate tokenizer implementations plus direct grep) and
> confirmed: 90 groups / 301 options total (not the round-1 doc's own hedged "~297-301" — 301 is the
> unambiguously correct figure, the 297 came from a less careful indentation-based parse that
> mis-tokenizes on mixed tabs/spaces in `00_constitutional_laws.txt`); 46/134 Qing; 6/24 MO#11/12;
> 38/143 non-Qing remainder; 68 placeholder desc keys, all non-Qing, exact per-file breakdown
> confirmed. The 12-file list is exhaustive (15 total files = 1 Qing + 2 MO#11/12 + 12 remainder).
> Ready to implement.

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:45`: "broad LAWS sweep — localizations + tech
prerequisites + wire laws into mechanics."

## Scope clarification: #95 covers BOTH Qing and vanilla law groups

#95's task text ("broad LAWS sweep") is not Qing-only or vanilla-only — it covers the entire
`common/laws/` surface. This doc's finding is that the QING HALF is already verifiably complete
(evidence below), so the actual remaining work is the vanilla half. This is a closure claim about
one half, not a scope narrowing of the task — #95 is not done until BOTH halves are confirmed, and
this doc's evidence for the Qing half is what allows it to close without further action there.

## Corrected counts (re-derived directly from `common/laws/*.txt`, brace-depth parse)

| Scope | Groups | Options |
|---|---|---|
| **TOTAL** (all 15 files) | **90** | **301** (independently confirmed by two separate brace-depth tokenizer implementations, zero variance between them — NOT the original draft's 362) |
| `00_qing_statutes_laws.txt` (Qing) | 46 | 134 (original draft's figure was correct here) |
| MO#11/#12 (`00_employment_laws.txt` + `00_industrialization_laws.txt`) | 6 (3+3) | 24 (12+12) |
| **Remaining non-Qing, non-MO11/12** | **38** | **143** |

The original draft's "90/362 total, 44/228 remainder" was wrong: the group total (90) was
coincidentally right, but every option count was inflated, and the remainder group count (44 vs.
actual 38) implied 6 extra non-existent groups. **Qing half: CLOSED, no further action** — the
46/134 figure and the "all built, no inert stubs" spot-check finding both hold.

## Corrected file list (12 files, not ~8/10)

The remaining non-Qing, non-MO11/12 surface is exactly these 12 files:
`00_administrative_laws.txt`, `00_army_laws.txt`, `00_civil_laws.txt`, `00_constitutional_laws.txt`,
`00_economic_laws.txt`, `00_governmental_laws.txt`, `00_monetary_policy_setting.txt`,
`00_monetary_standard.txt`, `00_social_laws.txt`, `00_standing_army_laws.txt`,
`00_succession_laws.txt`, `00_upper_house_laws.txt`. (The original draft's task list named ~10
files and omitted `00_administrative_laws.txt` outright, and was ambiguous about "monetary"
covering both monetary files — it covers both.) `00_civil_laws.txt` is included in this list for
completeness (it holds the group count) even though its one group, `citizens_rights`, is ALREADY
fully described (the #94 fix) — no further loc work needed there, but it's still in scope for the
tech-gating/wiring spot-check in principle.

## Per-item findings (corrected)

**Localizations — corrected to 68 placeholder/empty `_desc` keys** (not 27), independently
verified directly against `localization/english/laws_l_english.yml`: 19 keys with an empty string
value (`_desc:0 ""`) and 49 keys with literal filler text (`"<Name> desc"`, e.g. `executive_desc:0
"Executive desc"`). ALL 68 are in non-Qing groups (confirmed: zero placeholder descs in any
`qing_*_desc` key). The original draft's named list (`oligarchy_type`; the 3 `election_terms_`
groups; `executive`/`legislative`/`plebiscite`/`supermajority`; `immigration_`/`emigration_`) was a
partial SUBSET — it missed placeholder descs entirely in `00_constitutional_laws.txt` (constitutional
monarchy types, election term lengths, legislative body types, several legislative/constitutional
process options), `00_economic_laws.txt` (currency law, labour organisation law, business
regulation law — 13 keys), `00_governmental_laws.txt` (appointment laws, 2 keys),
`00_social_laws.txt` (religious law, financial assistance law, plus 2 more immigration/emigration
keys the original list missed), `00_standing_army_laws.txt` (3 keys), and `00_army_laws.txt`
(`self_supplied_army`, 1 key). #94 (the `citizens_rights` fix, committed, `00_civil_laws.txt`)
remains confirmed distinct from and non-overlapping with all 68 — no double-counting risk.

**Dead-code check — CLEAN, all 68 keys' groups are real and reachable.** Every group holding a
placeholder key gates on a genuine, defined trigger (e.g. `oligarchy_type`/`election_terms_
stratocracy`/`_megacorporation`/`_viceroyalty` gate on `government = oligarchy/stratocracy/
megacorporation/viceroyalty`, all four confirmed real government types in
`common/governments/00_albert.txt`), and every group is hand-wired into `gui/government_view.gui`'s
laws widget area. None are orphaned leftover definitions — safe to write real descriptions for all
68, not just the original 27.

**Tech prerequisites**: NOT actually a gap, confirmed on the corrected 12-file set. Only
`00_economic_laws.txt` has tech gating (`civic_tech >= 6` × 7, as originally found); the other 11
files gate on structural triggers instead (`government=`, `is_republic=`, `has_law=`), not tech —
spot-checked across the corrected file list and found no case of one sibling option in a group
gating on tech while another arbitrarily doesn't. This line item remains satisfied by prior work +
this audit's confirmation, rescoped to the corrected 12-file/68-key set.

**Wiring into mechanics**: same pattern — no inert stubs found in spot-checks across both Qing and
the corrected non-Qing set. The full sweep (task list below) should confirm this holds for every
group holding one of the 68 placeholder keys, not just the samples already checked.

## Why no larger design doc — unchanged, still a bounded audit, not a system decision

Unlike #88/#101/#115, there is no architectural decision to make here — no new mechanic, no new
GUI, no new pipeline. The remaining work is mechanical: (1) write real descriptions for all 68
placeholder keys, grounded in each law's actual modifier values, (2) spot-check for inert-stub
wiring gaps, (3) confirm tech-gating consistency. This is squarely a TASK LIST, not a design
document — per the standing "prepare-to-take-notes" and "bug vs missing-feature" project rules.

## The task list (the actual "design" for #95, corrected)

1. Audit exactly the 12 files listed above (not ~8-10) — every non-Qing, non-MO11/12 law file.
2. For all 68 placeholder desc keys: read the owning law group's actual modifier values, write a
   real description in the same escalating-tier tone #94's fix used for `citizens_rights` (grounded
   in concrete modifier numbers, not generic filler). Full key list by file:
   - `00_constitutional_laws.txt`: `1/4/6/8_year_terms`, `oligarchy_bourgeouis_dictatorship`/
     `_multiple_monarchy`/`_consortium`, `stratocracy_standard_ruler_retirement`/`_rule_for_life`/
     `_extended_ruler_career`/`_regular_elections`, `megacorporation_regular_board_elections`/
     `_double_terms`/`_election_on_retirement`/`_life_appointment`, `viceroyalty_15_year_terms`/
     `_10_year_terms`/`_20_year_terms`/`_life_appointment`, `no_monarchy`/`symbolic_monarchy`/
     `advisory_monarchy`/`administrative_monarchy`, `executive`/`legislative`, `unicameral_
     legislature`/`bicameral_legislature`/`legislative_assembly`/`executive_legislature`,
     `debate_floor`/`plebiscite`/`technocratic_oversight`/`technocratic_mandate`/`parliamentary_
     sovereignty`/`ratification_by_states`/`compulsory_review`/`supermajority`.
   - `00_economic_laws.txt`: `precious_metal_content_coinage`/`silver_standard_currency`/
     `promissory_notes`/`fiat_currency`, `labour_law_guilds`/`_trade_unions`/`_corporate_self_
     regulation`/`_state_monopoly`, and the business-regulation law's 5 members (self-regulation
     through full state planning — exact key names to confirm during execution against the file).
   - `00_governmental_laws.txt`: the 2 appointment-law members.
   - `00_social_laws.txt`: the remaining immigration/emigration closed-borders keys beyond what was
     originally found, plus the religious-law 4 members and the financial-assistance-law 2 members.
   - `00_standing_army_laws.txt`: `no_standing_army`/`limited_army`/`standing_army`.
   - `00_army_laws.txt`: `self_supplied_army`.
   (Exact key spellings to be pinned against the live file content during execution, not invented
   from this list alone — this enumeration is a coverage checklist, not a verbatim key dump.)
3. For all 12 files, spot-check every option for an empty/missing `modifier`/wiring block where a
   sibling option in the same group has a real one — fix any found (a correctness check against the
   group's own internal consistency, not a new mechanic).
4. Do NOT touch `00_qing_statutes_laws.txt`, `00_employment_laws.txt`, or
   `00_industrialization_laws.txt` — all three already fully covered by shipped prior work.
5. Do NOT add tech-prerequisite gating to any group in scope unless step 3's audit finds a SPECIFIC,
   concrete sibling-option inconsistency (not a blanket policy change) — none found in spot-checks
   so far, full sweep should confirm.

## Open questions for review
- Confirm the exact final key list for step 2 against live file content during execution (the
  checklist above is a coverage guide from this audit pass, not a guaranteed-exhaustive verbatim
  list — re-grep at execution time to catch anything drifted since this doc was written).
- Reconcile the two independent option-count parses (this review found ~297, the adversarial review
  found ~301, both agree the non-Qing remainder is in the 139-143 range) — the small discrepancy is
  immaterial to the task list (it doesn't change which keys need fixing), but should not be presented
  as a single precise figure without noting the parse-boundary ambiguity.
