# DESIGN — #117 GC office eligibility checks suitable exam degrees

> STATUS 2026-08-11: THIRD REVIEW ROUND — NOT CLEAN, but confirmed the SUBSTANCE is sound. Round 2's
> three findings (jinshi-only predicate, false generic-picker premises, unacknowledged martial→civil
> door) were verified genuinely fixed. Round 3 found the in-place edits left internal contradictions —
> "edit all THREE copies" vs. the resolved "leave copy #1 unfiltered" decision; "gongshi-and-above"
> phrasing contradicting the actually-juren-inclusive predicate; the canonical-predicate mandate wrongly
> including the mint paths. All four now fixed below (numbered list corrected to 2 copies + an explicit
> "not edited" note for #1; "gongshi-and-above" replaced with the correct "juren-and-above"; the mandate
> scoped to check-paths only; the #6-principle deviation now explicitly acknowledged). Do not implement
> until a fresh adversarial review clears this revision.

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:62`: "#117 GC office eligibility checks suitable exam degrees
(degree->post mapping)."

## Current state (confirmed by diagnosis)
The 13 Grand Council offices split into 11 civil (require jinshi per `QING_council_autofill_office`'s
`$degree$` param) and 2 martial (war, guard_commandant — require wu_jinshi). Today:
- **Autofill** mints a fresh character with the correct degree baked in via `create_character` — always
  degree-correct by construction.
- **Manual appointment** (`QING_office_eligible_candidate`, `qing_dynasty_triggers.txt:168-225`, and
  `QING_council_refresh_candidates`/`QING_council_refresh_candidates_by`, `se_QING_COUNCIL.txt:1116-1318`)
  has NO degree check at all — a completely degreeless courtier can be appointed to any of the 13
  offices, civil or martial.
- **Retrofit-after-the-fact for the 2 martial seats only**: `qing_office.41`
  (`events/imp19c_mod_events/qing_office_events.txt:963-976`, fired by `QING_office_appoint` on every
  appointment) strips any civil degree and grants wu_jinshi to whoever ends up in war/guard_commandant,
  self-guarded on "already holds a wuju rank." No equivalent exists for the 11 civil offices — a
  degreeless Grand Chancellor stays degreeless forever.
- Skill ranking (`combined_stats_council_svalue`, `council_sort_martial|finesse|charisma|zeal`,
  `QING_governance_svalues.txt:185-232`) already folds in `qing_degree_prestige_svalue`/
  `qing_wu_degree_prestige_svalue` as a SOFT preference — a degree-holder outranks an equally-skilled
  degreeless man, but does not exclude the degreeless man from the ranking or from appointment.

## Bench-size finding (diagnosis)
Setup seed (`setup/characters/00_Qing.txt`, ~230 character blocks): 15 jinshi + 2 gongshi + 1 juren = 18
civil degree-holders at boot, **0** wu-degree holders. New wu-degree holders only accrue via
`QING_grant_martial_degree` calls onto existing generals/admirals (day-30/31 one-shot,
`qing_force_setup.1/.11`) and the triennial exam cohort's martial slot (#113, ~1/cycle, ~3-year clock).
Civil bench is thin-but-nonzero and refilled quarterly by #111's draw. A HARD filter (`has_trait =
$degree$` required, zero tolerance) would starve the manual picker of martial candidates for potentially
years of early game, even though autofill's mint-with-degree is unaffected (self-sufficient regardless).

## Proposed resolution (candidate — NOT reviewed, do not implement yet)

Two components, both applied to `QING_office_eligible_candidate` (the shared trigger feeding
`QING_council_refresh_candidates`/`_by` and the row-click handler's `is_valid` in
`QING_governance_actions.txt:645-681`):

1. **Soft preference is already present and sufficient for the 11 civil offices** — no change needed
   there beyond confirming the existing `qing_degree_prestige_svalue` weighting actually dominates
   enough that a jinshi-holder is realistically always preferred over a degreeless man when both are
   candidates (the diagnosis flagged this as "residual gap," not "urgent" — a high-finesse degreeless
   commoner can still theoretically outrank a low-stat jinshi-holder). Candidate change: NONE required
   here if the soft weighting is judged sufficient; OR add a modest additional soft bonus specifically
   for jinshi if the reviewer judges the existing 25-point weight (out of a 0-9 skill axis) is not
   dominant enough in practice.

2. **For the 2 martial offices specifically**, since `qing_office.41`'s retrofit already GUARANTEES any
   appointee ends up wu_jinshi-holding after the fact (strip-then-grant, self-guarded), the retrofit
   itself may already satisfy "enforce suitable degrees" for war/guard_commandant — the open question
   for review is whether "always grant the degree after appointment" is an acceptable interpretation of
   "checks suitable exam degrees" (task text says CHECKS, implying a pre-appointment gate, not a
   post-appointment grant), or whether #117 requires replacing/supplementing the retrofit with a real
   pre-appointment filter for the martial seats — and if so, whether a HARD filter is safe given the
   0-wu-degree-holder bench at boot (a hard filter would leave the martial picker's candidate list
   EMPTY for a potentially long early-game stretch, until the day-30 grant or the first exam cohort
   produces holders).

## Open questions a design review must resolve before implementation

- Does "enforce degree eligibility" mean a HARD exclusion (only degree-holders ever listed/appointable)
  or a STRENGTHENED soft preference (degree-holders dominate the ranking far more than today, but a
  degreeless man remains a last-resort fallback when no degree-holder exists — mirroring the
  "under-full is honest" pattern used everywhere else in this session's draw-conversion work)? The
  bench-size finding above argues strongly against a hard filter for the 2 martial offices specifically.
- If a hard filter is chosen for civil offices but a soft (or retrofit-preserving) approach for martial
  offices, is that asymmetry justified and clearly documented, or does it read as an arbitrary
  inconsistency a future maintainer would trip over?
- Does `qing_office.41`'s retrofit become redundant, partially redundant, or still load-bearing under
  whatever design is chosen — the retrofit covers appointment ROUTES a filter on
  `QING_office_eligible_candidate` cannot reach (e.g. `qing_force_setup.1/.11`'s day-30/31 reconciliation
  of generals/admirals promoted to councillor, and any future #116 draw-conversion of autofill that
  reuses `QING_office_appoint` without routing through the filtered picker) — should it be kept
  regardless of what #117 does to the picker, as defense-in-depth?
- Interaction with #116 (GC autofill create_character→draw, currently blocked pending its own design
  review): if #116's eventual draw also requires `has_trait = $degree$` (as its current proposed
  resolution does), does sequencing #117 before or after #116 change either design's risk profile?
  (#116's proposed resolution already independently arrived at requiring `has_trait = $degree$` on its
  draw — confirm whether #117 should generalize/share that requirement rather than defining it twice.)

## REVIEW FINDINGS (2026-08-11)

Adversarial design review returned **NOT CLEAN**. Two CRITICAL findings invalidate this doc's own
diagnosis; several MEDIUM findings show the doc hedged on the one decision it exists to make.

**Finding 1 (CRITICAL) — the "0 wu-degree holders at boot" premise is FALSE.** It counted only the
~230 STATIC setup character blocks (`setup/characters/00_Qing.txt`) and missed RUNTIME game-start
minting. After the deferred day-32 autofill and game-start sub-post staffing actually run, wu_jinshi-
holding, CHI-employed, non-commander courtiers exist from turn one: ~4 Imperial Guardsmen minted with
`degree = wu_jinshi` (`QING_subpost_staff_corps_minted`, `se_QING_SUBPOSTS.txt:214`/`:279`, refilled
quarterly, explicitly kept non-general/admiral/governor so they pass the picker's own exclusion gates
and are NOT excluded from the great-office candidate builders today); the 2 autofilled war/
guard_commandant holders themselves (`add_trait = wu_jinshi`, `se_QING_COUNCIL.txt:84`/`:92`); plus the
triennial exam martial slot's fallback mint. **The martial manual bench is not empty.** This dissolves
the doc's chief hedge against a hard martial filter — re-derive the bench-size argument against RUNTIME
state, not the static seed, before deciding hard vs. soft.

**Finding 2 (CRITICAL) — the proposed edit target is the wrong chokepoint; a change to
`QING_office_eligible_candidate` would be INERT for the manual picker.** The doc's "Proposed resolution"
says to apply changes to `QING_office_eligible_candidate`. Verified: neither candidate-list builder
(`QING_council_refresh_candidates`/`_by`, `se_QING_COUNCIL.txt:1116-1201`/`:1215-1318`) nor the row-click
handler's `is_valid` (`QING_governance_actions.txt:646-681`) actually CALLS that trigger — all three
independently HAND-INLINE their own copies of the same exclusion conditions (the row-click's own comment
even says "inlined because this is CHARACTER scope"). A degree check added only to
`QING_office_eligible_candidate` changes nothing observable on the manual-appointment path. **Fix:** the
design must name and edit all THREE enforcement copies (or mandate refactoring them to share one
predicate first, which would also serve #116's parallel need — see Finding 5).

**Finding 3 (MEDIUM) — the existing soft preference is already dominant; component 1's proposed
"maybe add a bonus" is unnecessary.** `council_sort_martial` already folds in
`qing_wu_degree_prestige_svalue` (the WU ladder, not the civil one) — the martial/civil ranking split
this doc worried about is ALREADY correctly implemented. Arithmetic: a 25-point degree bonus against a
0-9 raw skill axis means a degree-holder with skill 0 already beats a degreeless genius with skill 9 for
every single-skill office; only the summit chancellor/regent bench (a 0-36 sum) leaves room for a
max-stat degreeless man to edge out a low-stat degree-holder. **Fix:** drop the "maybe add a soft bonus"
musing; if soft-preference is the chosen answer, state plainly that the ranking half of #117 is ALREADY
satisfied by existing machinery and needs no code change.

**Finding 4 (MEDIUM) — the doc must make the hard-vs-soft decision, not leave it as an open question.**
The task text says eligibility "CHECKS" suitable degrees — today there is NO gate at all on the manual
picker (a fully degreeless courtier is listed and appointable to any of the 13 offices); ranking is not
a check. The doc's own component 1 conclusion ("no change needed" for civil) directly contradicts a
plain reading of the task for the 11 civil offices specifically, which have no retrofit at all (a
degreeless Grand Chancellor stays degreeless forever, unlike the 2 martial seats). **Fix:** decide
explicitly — either GATE (a real filter, matching this session's #111/#113/#114 "confer-else-create,
under-full is honest" pattern — and per Finding 1, safe for martial too now that the bench isn't empty)
or declare RANK-ONLY (state #117 is satisfied by existing machinery and close it as a ranking-only task).
This is the one decision #117 exists to make; it may not ship as an open question.

**Finding 5 (MEDIUM) — the doc never builds the "degree→post mapping" its own title names.** There is
no canonical office→degree table anywhere; the correspondence is scattered as inline literal
`degree = jinshi`/`degree = wu_jinshi` arguments across 13+ call sites in three effects
(`QING_council_autofill:80-92`, `QING_office_vacate_dispatch:1741-1753`, and implicitly `qing_office.41`
for the 2 martial seats). **Fix:** if #117 builds anything, define one canonical predicate/table (e.g.
`QING_office_required_degree = { office = $office$ }`) and require every path — the autofill args, the
vacate-dispatch backfill, AND any new picker filter — to consume it. #116's own draw (which independently
arrived at requiring `has_trait = $degree$`) should be REQUIRED to reuse this same predicate rather than
each task defining its own, resolving the open cross-task question at the bottom of this doc by
mandate rather than by musing.

**Finding 6 (MEDIUM) — `qing_office.41` is a post-hoc GRANT, not a CHECK, and pairing it with a filter
is incoherent.** `qing_office.41` doesn't verify eligibility — it forcibly re-credentials whoever lands
in war/guard_commandant (strips any civil degree, bolts on wu_jinshi). Keeping it as the ONLY martial
solution means #117 does literally nothing observable for the 2 martial offices. Running a hard filter
AND the auto-grant simultaneously is self-contradictory (why gate qualification if you also confer it by
fiat regardless?). **Fix:** decide explicitly. If #117 adds a real martial gate, `qing_office.41`'s
runtime auto-grant on the manual path should be removed or narrowed to boot/construction reconciliation
only (it remains legitimately load-bearing for `qing_force_setup.1/.11`'s day-30/31 commander
reconciliation and any death-backfill route a picker filter can't reach — keep it there as
defense-in-depth, documented as such). If #117 stays rank-only, state plainly that martial "eligibility"
is really "auto-confer on appointment" and #117 changes nothing for martial.

**Finding 7 (LOW, corrects an overstated risk) — the "great office sits permanently vacant" severity
fear is overstated.** `QING_office_vacate_dispatch` backfills every death/departure with a fresh
degree-correct MINT via `QING_council_autofill_office` regardless of what the manual picker's filter
does — only the manual-reshuffle twin (`_nobackfill`) leaves a seat empty, and that's a deliberate player
action. **Fix:** correct the severity framing; a hard filter's worst case is "the player's manual
replacement picker is briefly sparse," not "the ministry goes uncommanded for years" — and per Finding 1,
even that worst case doesn't hold for martial seats.

**Disposition:** the actual gap #117 needs to close is narrower than this doc framed it: the RANKING
preference (including the martial/civil ladder split) already exists and already works; what's missing
is (a) a real GATE on the three inlined enforcement copies (Finding 2) and (b) a canonical degree→post
map (Finding 5) that #116 should share. Rebuild the proposed resolution around Findings 1-6, then dispatch
a fresh design review before implementation.

## CORRECTED PROPOSAL (2026-08-11) — resolves Findings 1-6

**Decision (Finding 4, made explicitly, not left open):** GATE, not rank-only. Ranking is already
solved by existing machinery (Finding 3) and needs no change. The actual gap is that the manual picker
has NO exclusion at all — #117 adds one.

**Hard/soft split (Finding 1 + reconciled with #116's independent corrected proposal):** HARD filter
(`has_trait = $degree$` required) for the 11 civil offices. SOFT preference (existing
`qing_degree_prestige_svalue`/`qing_wu_degree_prestige_svalue` weighting, already sufficient per Finding
3) for the 2 martial offices (war, guard_commandant) — NOT a hard filter there. Finding 1 corrected the
bench-size premise (the martial bench isn't empty at boot), but #116's own corrected proposal
independently chose soft-preference for martial specifically to avoid making its OWN backfill draw a
near-permanent no-op; keeping #117's martial approach consistent with #116's avoids the exact
"asymmetric and undocumented" trap this doc's own original open-question worried about — the asymmetry
is now DELIBERATE and consistent across both tasks, not arbitrary.

**Canonical degree→post predicate (Finding 5) — WIDENED per review finding (see "## REVIEW FINDINGS
ROUND 2" below):** define, in a shared location (e.g. `common/scripted_triggers/qing_dynasty_triggers.txt`,
alongside `QING_office_eligible_candidate`):
```
QING_office_required_degree_civil = {
    OR = { has_trait = jinshi  has_trait = hanlin  has_trait = gongshi  has_trait = juren }
}
QING_office_required_degree_martial_soft = yes   # marker only — martial uses ranking, not a hard trigger
```
`jinshi`-only was found to reproduce the EXACT under-inclusiveness bug #111's own retroactive review
found in a parallel context: civil degree traits are mutually exclusive `status` traits
(`common/traits/00_imp19c.txt`) — `hanlin`/`gongshi`/`juren` are NOT jinshi variants, they are DISJOINT
degrees, so `has_trait = jinshi` alone would wrongly bar every Hanlin academician (the modeled top
historical civil officials — Li Hongzhang, Zeng Guofan, Zhang Zhidong, Guo Songtao — are all minted
with `hanlin`, never `jinshi`) plus every gongshi/juren graduate from ANY civil office, civil eligibility
checks are the specific place this matters (unlike #111's narrower "Hanlin pool," which deliberately
stayed jinshi-plus-hanlin-only and left gongshi/juren as an open scope question — a GC OFFICE eligibility
gate has no equivalent narrow-scope justification for excluding a real, qualified degree tier). This
widened set matches the codebase's own existing convention for "is this man exam-qualified": the amban
draws (`se_QING_AMBAN.txt:86/90/121/125/258/262`) already use
`OR = { has_trait = jinshi  has_trait = hanlin  has_trait = gongshi  has_trait = juren  has_trait =
shengyuan }`, and `qing_rites_events.txt:418-423` pools the same four-plus-shengyuan set. Deliberately
excludes `fanyi_jinshi` (the banner/translation track feeds amban posts, a separate population from
civil GC offices — autofill's own `$degree$` args never use it for civil offices either) and
`shengyuan`/`jiansheng` (the lowest two rungs — the amban bench's own inclusion of `shengyuan` reflects
that a frontier resident post has a much lower bar than a Grand Council seat). The gate stays at
JUREN-AND-ABOVE (matching the predicate exactly: jinshi, hanlin, gongshi, juren — juren IS included,
being the fourth member of the OR-set; there is no gongshi-and-above reading anywhere in this design).
The canonical predicate is consumed ONLY by the eligibility-CHECK paths listed under "Fix the
wrong-chokepoint bug" below — it is NOT consumed by the autofill/vacate-dispatch `$degree$` args, which
MINT a character with one concrete degree literal and cannot meaningfully "consume" an OR-of-four
predicate; those paths are unaffected by this design and continue passing their existing literal
`degree = jinshi` argument unchanged.

**Fix the wrong-chokepoint bug (Finding 2) — edit TWO of the three inlined copies (copy #1 stays
unfiltered by design — see the "generic picker" resolution below, which this numbered list must agree
with, not contradict):**
1. `QING_council_refresh_candidates_by` (`se_QING_COUNCIL.txt:1215-1318`): add
   `QING_office_required_degree_civil = yes` to the `ordered_character.limit`, conditionally on
   `$sortval$` — this is the PER-OFFICE cache (`$sortval$` already tells it which office's picker is
   opening), so THIS builder can correctly apply the hard filter unless `$sortval$ = council_sort_martial`
   (which maps to exactly, and only, the 2 martial offices — no civil office ever uses that sortval, so
   this discriminates perfectly with no new parameter needed).
2. The row-click handler's `is_valid` (`QING_governance_actions.txt:646-681`, the `trigger_else` "GREAT
   OFFICES" branch): add the hard civil filter here too, gated on
   `NOT = { OR = { scope:player.var:qing_gc_picker_office_var = flag:war
                    scope:player.var:qing_gc_picker_office_var = flag:guard_commandant } }`
   (i.e., apply the hard filter unless the target is one of the 2 martial offices).
3. `QING_council_refresh_candidates` (`se_QING_COUNCIL.txt:1116-1201`, enforcement copy #1) is
   DELIBERATELY NOT edited — see "generic picker" resolution below for why leaving it unfiltered is
   correct, not an oversight.

**The "generic picker" caveat — CORRECTED (a review found the original resolution rested on two false
premises — see "## REVIEW FINDINGS ROUND 2" below for the full finding):**
`QING_council_refresh_candidates` (the generic, non-office-aware builder, enforcement copy #1) has TWO
live callers, not one: the plain Grand-Council-tab-open button (`qing_gov_council_refresh_candidates`,
`QING_governance_actions.txt:354-362`), AND the hidden event `qing_office.40`
(`qing_office_events.txt:952`), fired by `QING_office_appoint`/`QING_office_vacate` after EVERY appoint/
vacate. Additionally, the three ministry CORPS token buttons (censor inspector, imperial guardsman,
zongli diplomat — NOT great offices, a separate capped roster) live in `gui/qing_censorate.gui`,
`gui/qing_guard.gui`, `gui/qing_zongli.gui` (not `government_view.gui`) and explicitly call the GENERIC
builder (copy #1), then open the SAME shared `qing_office_picker_window` — so copy #1's list genuinely
IS shown for corps enrolment, not never-shown as the original resolution claimed.

**Corrected decision (still option (c), but for the right reason):** leave enforcement copy #1
(`QING_council_refresh_candidates`) UNFILTERED — but not because it's "never shown." It's because the
row-click `is_valid` (enforcement copy #3) is the AUTHORITATIVE gate regardless of which list populated
the picker: it branches corps (`trigger_if`, `QING_governance_actions.txt:604-644`) vs. great-office
(`trigger_else`, `:646-681`) via `scope:player.var:qing_gc_picker_office_var`, and corps enrolment must
NOT carry a civil-degree filter (a censor inspector or imperial guardsman is not a GC office and has no
degree requirement). So even though copy #1's unfiltered list IS sometimes the one rendered (corps
buttons, and any stale state left by `qing_office.40` before a great-office picker re-refreshes via the
office-aware copy #2), a degreeless man can only ever be CLICKED INTO a corps slot from that list — the
great-office row-click branch (copy #3) independently re-verifies the hard filter and blocks him from
any civil GC seat regardless of what the displayed list contained. No degreeless-civil bypass exists;
copy #1 stays unfiltered by design (it correctly serves BOTH office and corps contexts, and only copy
#3's branch-aware gate needs to discriminate between them).

**Acknowledged deviation (not a defect, stated explicitly):** the `#6` fix (`se_QING_COUNCIL.txt:1142-1147`)
established a codebase principle of filtering the BUILDER, not just the click-handler, specifically
because a listed-but-unappointable candidate was a reported bug ("listed but un-appointable"). This
design's copy #1 deliberately does NOT follow that principle in the narrow `qing_office.40` stale-refresh
window (a degreeless man can transiently appear in what LOOKS like a civil-office picker with a
disabled/blocked Appoint action, until the office-aware copy #2 refresh runs). This is safe (copy #3
blocks the click) and narrow (requires an appoint/vacate to fire while a civil picker is already open),
but it is a deliberate, narrow exception to the `#6` principle, not an unnoticed gap.

**`qing_office.41` disposition (Finding 6, decided explicitly):** KEEP, unchanged, as defense-in-depth.
It remains load-bearing for `qing_force_setup.1/.11`'s day-30/31 commander reconciliation (a path that
never goes through the picker) and for any future appointment route that reaches `QING_office_appoint`
without passing through the now-filtered picker (e.g. #116's backfill draw, which mints/draws
independently of the manual picker's enforcement copies). It is NOT contradictory with the new hard
civil filter or the unchanged martial soft-preference, because it only ever fires for the 2 martial
offices — which never carry a hard filter under this design — so "gate qualification vs. confer it by
fiat" is not in tension for them; it stays a legitimate backstop.

**Acknowledged consequence (per review — a genuinely NEW behavioral change, accepted, not a bug to
fix):** `qing_office.41`'s `QING_grant_martial_degree` unconditionally STRIPS all seven civil-track
traits when a man is appointed to war/guard_commandant, with no inverse effect anywhere in the codebase
— the only way back to a civil degree is sitting the civil exam fresh. Before this design, a civil
minister appointed to a martial seat and later reshuffled back to a civil office could still serve (the
picker applied no degree check either way). AFTER this design's hard civil filter ships, that same man —
now `wu_jinshi`-holding with no civil degree — is PERMANENTLY BARRED from all 11 civil offices; the
civil→martial→civil career path that existed before this design is closed. This is a real, deliberate
behavioral change (arguably a correct one — a Grand Secretary drilled onto a military ladder as a token
of martial-office congruence is not obviously the right man to reshuffle back into a civil ministry —
but it is a CHANGE, not something to leave unstated). Recorded here as an accepted consequence of
shipping the hard civil filter, not a defect requiring a fix.

## REVIEW FINDINGS ROUND 2 (2026-08-11)

Adversarial review of the first corrected proposal returned **NOT CLEAN**. Three findings, all now
folded into the sections above:

**Finding 1 (CRITICAL, now fixed above) — `has_trait = jinshi` alone reproduces #111's exact
under-inclusiveness bug.** `hanlin`/`gongshi`/`juren` are mutually exclusive with `jinshi`, not subsets
of it; the modeled top historical civil officials (Li Hongzhang, Zeng Guofan, Zhang Zhidong, Guo
Songtao) are all minted `hanlin`-only. A jinshi-only civil filter would silently bar the most senior,
most qualified civil officials from GC office eligibility — the worst kind of failure since it wouldn't
crash, just quietly exclude the best candidates. Fixed by widening
`QING_office_required_degree_civil` to `OR = { jinshi  hanlin  gongshi  juren }`, matching the amban
draws' own proven precedent.

**Finding 2 (MEDIUM, now fixed above) — the original "generic picker" resolution rested on two false
premises.** (a) `QING_council_refresh_candidates` has a SECOND live caller, the hidden event
`qing_office.40` (fired by `QING_office_appoint`/`QING_office_vacate` on every appoint/vacate), not just
the tab-open button. (b) The three ministry-corps token buttons (censor/guard/zongli — separate GUI
files from `government_view.gui`) DO call the generic builder before opening the shared picker window,
so its unfiltered list genuinely is sometimes rendered. The underlying DECISION (leave copy #1
unfiltered) still holds, but for the correct reason: the row-click `is_valid` (copy #3) is authoritative
regardless of which list populated the window, and it already branches corps-vs-great-office before
applying any degree filter — so a degreeless man reachable via copy #1's unfiltered corps view can still
never be clicked into a civil GC seat. Rationale corrected above; decision unchanged.

**Finding 3 (MEDIUM, now fixed above) — the martial→civil one-way door was an unacknowledged new
regression.** `qing_office.41`'s unconditional civil-trait strip on martial appointment, combined with
this design's NEW hard civil filter, permanently bars a former civil minister who served in a martial
seat from ever returning to a civil office — a real behavioral change the original proposal never
stated. Now explicitly recorded as an accepted consequence, not silently shipped.

## Open questions a fresh design review must resolve
- Re-verify the widened `QING_office_required_degree_civil` predicate (Finding 1's fix) against the
  actual current trait definitions in `common/traits/00_imp19c.txt` — confirm the OR-set is complete and
  correctly excludes `fanyi_jinshi`/`shengyuan`/`jiansheng` as intended.
- Re-verify the corrected "generic picker" rationale (Finding 2's fix): confirm `qing_office.40`'s actual
  behavior (does it ever leave copy #1's list as the LAST-refreshed state right before a great-office
  row-click, and if so does copy #3's branch-aware gate genuinely still block a degreeless click, or is
  there a timing gap the correction missed), and confirm the three corps-panel GUI files
  (`qing_censorate.gui`/`qing_guard.gui`/`qing_zongli.gui`) really do call the generic builder as
  claimed.
- Confirm `QING_governance_actions.txt`'s row-click `is_valid` fix (enforcement copy #3) is gated on the
  CORRECT var (`scope:player.var:qing_gc_picker_office_var`, matching the existing pattern at
  `:1283-1287`/`:1299-1309` in the sibling candidate builder) and that the flag names (`flag:war`,
  `flag:guard_commandant`) match the office keys used elsewhere in this file.
- Whether `QING_office_required_degree_civil`'s now-widened OR-body is worth a named trigger (yes,
  clearly, now that it's non-trivial) — this question from round 1 is resolved by the widening itself.
