# DESIGN (draft, pre-review) — Salt Gabelle reform as a multi-year struggle + Decision

## Requirements (direct user instructions, this session)

1. "Reform the Salt Gabelle" becomes a **series of events playing out over many years**, not
   one dilemma — proposed reform, pushback, rewards and penalties, bickering between the
   Minister of Revenue and the Salt Commissioner.
2. The series focuses on **the Minister's struggle to assert authority over the Commissioner**,
   who **defends entrenched interests**.
3. A new prerequisite event, **"Statecraft Reform,"** must fire and be accepted by the player
   before the chain can start. Its text must make clear that **choosing to reform unlocks
   future events**.
4. The actual reform becomes a **Decision** (not an event option), requiring: (a) the event
   chain has played out, and (b) **the Minister of Revenue is more charismatic than the Salt
   Commissioner**.
5. The decision **costs political influence**, **costs revenue short-term**, and produces a
   **long-term payoff of higher salt production and revenue**.

## What exists today (audited directly, not assumed)

- `events/imp19c_mod_events/qing_revenue_events.txt`, `qing_revenue.1` — the CURRENT one-shot
  "Reform the Salt Gabelle" dilemma. Triggered from `QING_revenue_pulse`
  (`se_QING_REVENUE.txt:284-317`, a weighted `random_list` entry, chance 20/40, throttled by
  `qing_revenue_event_cooldown` (270 days) and the shared `qing_gc_event_slot_used` court-slot
  gate), requiring a living seated Salt Commissioner + `NOT qing_salt_gabelle_reformed`.
  Three options: **A** reform (fitness-gated `>=50`: +8% tax via `qing_salt_gabelle_reformed_mod`,
  +0.02 legitimacy, commissioner's corruption -20, his own popularity/loyalty hit); **B** milk it
  (instant +80 treasury, `qing_salt_gabelle_graft` modifier [+4% tax, -0.03 legitimacy] for 10
  years, a corrupt commissioner personally skims +25 gold/+10 corruption); **C** defer
  (fitness-gated `<50`: status quo, +2 corruption drift).
- `QING_salt_assess_fitness` (`se_QING_SALT.txt:300-361`) scores the SEATED COMMISSIONER
  (`qing_salt_commissioner_holder`) 0-100 from his finesse, honest/corrupt traits, numeric
  corruption stat, and loyalty — into `qing_salt_fitness`. This currently just gates which
  options are visible; nothing else reads it.
- The standing quarterly salt income (`QING_salt_income`, `se_QING_SALT.txt:96-196`, called
  every quarter from `QING_revenue_salt_income`) is `GOODS_national_production_salt ×
  market-soft[0.7,1.3] × gabelle-markup(×3.0) × character-factor`, where character-factor =
  `1 + (finesse-7)×0.03 − squeeze×0.004`, clamped [0.5,1.3]. **Audited directly: this formula
  never reads `qing_salt_gabelle_reformed` or `qing_salt_gabelle_graft`** — despite
  `QING_revenue_pulse`'s own comment claiming income is "scaled by... whether the gabelle is
  REFORMED... vs GRAFT-ridden." The old event's real revenue effect is entirely INDIRECT: it
  moves the commissioner's own `corruption` stat, which `QING_salt_reconcile` mirrors into
  `qing_salt_squeeze` every quarter, which is what the character-factor term actually reads.
  The `+8% global_tax_modifier` from `qing_salt_gabelle_reformed_mod` is real and separate (a
  general tax-efficiency country modifier, not salt-specific).
- `qing_office_revenue_holder` (Minister of Revenue, `se_QING_REVENUE.txt`/`se_QING_COUNCIL.txt`)
  and `qing_salt_commissioner_holder` (Salt Commissioner, `se_QING_SALT.txt`) are both real,
  always-checkable country-scope character links, each with `is_alive`/`employer` guards already
  proven throughout this codebase.
- Decision file format, confirmed from `decisions/imp19c_mod_decisions/imp19c_economy_decisions.txt`:
  `country_decisions = { key = { potential = {} allow = {} effect = {} } }`. `add_political_influence`
  is a proven effect (`-10` used in that same file).
- Multi-year day-delay chain idiom, confirmed from `qing_reform.30` (`events/imp19c_mod_events/
  qing_reform_events.txt:191-256`): `trigger_event = { id = X  days = { 180 900 } }` between
  stages, `change_variable` meters carried on country-scope vars across stages.
- Char-vs-char stat comparison: engine RHS-comparison rule (project-standing) forbids a bare
  `var:A > var:B` trigger (RHS must be literal/svalue). Proven idiom elsewhere is to STAGE the
  difference into ONE var via a periodic mirror (same shape as `qing_salt_finesse`/
  `qing_salt_squeeze`'s own quarterly mirror), then compare that var to the literal `0`.

## Design

### 1. Retarget `qing_revenue.1` into "Statecraft Reform" (the entry gate)

Keep its existing trigger conditions, cooldown, and court-slot throttle unchanged (proven,
already-working plumbing) — only the options change:

- **Option A — "Press for reform of the salt administration."** Sets
  `qing_saltreform_stage = 1`, `qing_saltreform_authority = 20` (Minister's starting foothold —
  not zero, since he's already moved), claims no extra cost yet. Text explicitly states that
  taking this path opens a longer struggle (satisfies requirement 3 — "make clear that choosing
  to reform unlocks future events"). `trigger_event = { id = qing_revenue.7  days = { 180 540 } }`
  (6-18 months to the first pushback, matching the `qing_reform.30` idiom's own scale).
- **Option B — "Leave the Commissioner to his own methods."** Unchanged from the current
  Option B (instant +80 treasury, `qing_salt_gabelle_graft` modifier, corrupt commissioner
  self-enriches). Sets `qing_salt_gabelle_declined = 1` with the SAME re-offer cooldown idiom
  the file already uses elsewhere (a `qing_revenue_event_cooldown`-style timed var), so the
  player can revisit Statecraft Reform again in a future reign rather than being locked out
  forever.
- Old Option C (defer, fitness<50) is DROPPED — fitness now drives the chain's difficulty (see
  below) instead of gating entry. Every seated commissioner gets a real fight, not a filtered-out
  non-choice.

### 2. The struggle chain — `qing_revenue.7`, `.8`, `.9` (new; `.2`-`.6` are taken by unrelated
events)

Central mechanic: **`qing_saltreform_authority`** (0-100, country-scope), the Minister's
asserted control, tugging against the Commissioner's OWN existing `qing_salt_fitness` (his
competence at defending the status quo) and `qing_salt_squeeze` (how much he personally profits
from leaving it alone — the concrete "entrenched interests" stake, already a real meter, not a
new abstraction).

- **`.7` — "The Minister Presses His Case."** Both office-holders on screen
  (`left_portrait = var:qing_office_revenue_holder`, `right_portrait =
  var:qing_salt_commissioner_holder`), text framed as the Minister formally requesting an audit
  of the 兩淮鹽政's books; the Commissioner citing decades of precedent and the merchants' own
  stake in stability. Two options:
  - **"Press the audit."** `change_variable = { qing_saltreform_authority  add = 20 }`. Real
    cost now: `add_treasury = -40` (audit expenses) — the FIRST short-term cost (requirement 5).
    Commissioner's loyalty takes a hit: a bare `add_loyalty = loyalty_qing_estranged`, matching
    the CURRENT `qing_revenue.1` Option A's own precedent (a one-shot option click, not a
    repeating pulse) — [review-fix] `QING_apply_estranged_once` is the wrong citation, that
    helper exists specifically for idempotency across REPEATING quarterly/monthly pulses
    (`se_QING_WAR.txt`/`se_QING_NAPOLEON.txt`), not a single option-click effect.
  - **"Give him time to comply voluntarily."** No cost, `authority += 5` only (the Commissioner
    stalls). Lower risk, weaker progress — a real choice, not a trap option.
  `trigger_event = { id = qing_revenue.8  days = { 360 720 } }`.
- **`.8` — "The Commissioner Digs In."** The pushback event (requirement 2, "defending entrenched
  interests" made concrete): the Commissioner tries to co-opt the Minister (an offer, tied to
  `qing_salt_squeeze` — a richer graft pool bribes harder) OR, if that's rejected/unavailable,
  quietly leans on his merchant patrons to slow-walk compliance (a modest, temporary quarterly
  income dip via a short-duration country modifier, the "penalty" side of requirement 1). Options:
  - **"Refuse the bribe and press on."** `authority += 15`. Real risk: `if =
    {limit={var:qing_salt_squeeze >= 50} ... }` a chance of a short income-dip modifier (the
    Commissioner's networks retaliate) — rewards AND penalties in the same branch, not
    guaranteed.
  - **"Let it pass for now."** `authority += 0`, but ALSO no risk — a genuine stall option, not
    a punishment for caution.
  `trigger_event = { id = qing_revenue.9  days = { 360 720 } }`.
- **`.9` — "The Reckoning."** Final showdown; resolves the chain. Trigger includes
  `has_variable = qing_saltreform_authority` (always true by this point). Immediate block
  computes the outcome from the SAME two existing meters used throughout this design (no new
  parallel state):
  ```
  set_variable = { name = qing_saltreform_margin  value = var:qing_saltreform_authority }
  change_variable = { name = qing_saltreform_margin  subtract = var:qing_salt_fitness }
  ```
  - **If `qing_saltreform_margin > 0`** (Minister's pressure outweighs the Commissioner's own
    competence at resisting): the chain SUCCEEDS. Sets `qing_salt_reform_chain_complete = 1`
    (Decision requirement (a), satisfied). Text: the Commissioner formally submits to oversight.
    Small immediate reward: Minister +popularity, matching this codebase's existing
    `QING_char_promote_standing` idiom.
  - **Else**: the chain FAILS. Sets `qing_salt_gabelle_reform_failed = 1` with a multi-year
    cooldown (a timed var, `days = 3650`, matching `qing_taint_expiry`'s proven auto-lapsing
    idiom) before Statecraft Reform can be re-offered. No decision unlock. This is the genuine
    "penalty" branch requirement 1 asks for — reform is not guaranteed just for trying.
  Single option acknowledging the outcome (text branches via `triggered_desc`, matching
  `qing_wenzhi_painter.2`'s own proven fallback-desc convention), no further mechanical choice.

### 3. Charisma-gap mirror (Decision requirement (b))

New scratch effect, called every quarter from the ALREADY-EXISTING `QING_revenue_pulse`
(`se_QING_REVENUE.txt:240`) — no new on_action hook needed:
```
QING_revenue_saltreform_charisma_gap = {
	set_variable = { name = qing_saltreform_charisma_gap  value = 0 }
	if = {
		limit = { has_variable = qing_office_revenue_holder  var:qing_office_revenue_holder = { is_alive = yes } }
		change_variable = { name = qing_saltreform_charisma_gap  add = var:qing_office_revenue_holder.charisma }
	}
	if = {
		limit = { has_variable = qing_salt_commissioner_holder  var:qing_salt_commissioner_holder = { is_alive = yes } }
		change_variable = { name = qing_saltreform_charisma_gap  subtract = var:qing_salt_commissioner_holder.charisma }
	}
}
```
The Decision's `allow=` then reads `var:qing_saltreform_charisma_gap > 0` — a literal RHS,
satisfying the project's own RHS-comparison rule.

### 4. The Decision — `decisions/imp19c_mod_decisions/qing_salt_decisions.txt` (new file)

```
country_decisions = {
	qing_reform_salt_gabelle = {
		potential = {
			tag = CHI
			has_variable = qing_salt_reform_chain_complete
			# [review-fix] qing_salt_admin_law (common/laws/00_qing_statutes_laws.txt:163-178)
			# touches this SAME var on enact -- even re-selecting the default qing_salt_farmed
			# option calls set_variable value=0, which CREATES the var. A bare NOT=has_variable
			# would then read false forever after any law touch, exactly the gap se_QING_REVENUE.
			# txt:299-306 already documents fixing for qing_revenue.1's own trigger. Same OR-guard.
			OR = {
				NOT = { has_variable = qing_salt_gabelle_reformed }
				var:qing_salt_gabelle_reformed = 0
			}
		}
		allow = {
			has_variable = qing_saltreform_charisma_gap
			var:qing_saltreform_charisma_gap > 0
			political_influence >= 10
		}
		effect = {
			set_variable = { name = qing_salt_gabelle_reformed  value = 1 }
			add_political_influence = -10
			# short-term cost (requirement 5)
			add_treasury = -120
			TREASURY_LOG_it = { amount = -120 }
			# long-term payoff: the SAME permanent tax-efficiency modifier the old one-shot
			# event already granted (proven, unchanged) ...
			add_country_modifier = { name = qing_salt_gabelle_reformed_mod  duration = -1 }
			# ... PLUS a genuine, durable salt-PRODUCTION cleanup, not just a generic tax
			# bump: reforming directly cleans out the commissioner's own graft rather than
			# waiting on the slow quarterly reconcile drift.
			if = {
				limit = { var:qing_salt_squeeze > 10 }
				set_variable = { name = qing_salt_squeeze  value = 10 }
			}
			LOG_line = { sys = QING  msg = "revenue: salt gabelle formally reformed via decision (chain complete, minister's authority prevailed)" }
		}
	}
}
```

**Why `qing_salt_squeeze -> 10` is the production/revenue lever, not a new multiplier constant**:
per the audited formula above, `qing_salt_squeeze` is the ONLY term in the standing quarterly
salt income that represents "how much of the monopoly's real yield actually reaches the
treasury" — directly setting it low is the mechanically correct way to deliver "increased salt
production and revenue" without inventing a parallel, redundant multiplier (the vegetables
precedent added a NEW multiplier because vegetables had no equivalent squeeze/corruption
concept; salt already does). `qing_salt_squeeze`'s normal path back down is the slow quarterly
`QING_salt_reconcile` mirror off the commissioner's own corruption stat — this decision instead
delivers an immediate, durable floor-cleanup, consistent with "formally reforming the
administration" being a decisive act, not a gradual drift.

### 5. Closing the law bypass (review-driven addition)

`qing_salt_admin_law`'s `qing_salt_reformed` option (`common/laws/00_qing_statutes_laws.txt:
174-177`) sets the exact same `qing_salt_gabelle_reformed=1` flag directly, for one law-enactment
cost, once `qing_reform_track_unlocked` — completely bypassing Statecraft Reform, the struggle
chain, the charisma-gap requirement, and the treasury/political-influence cost. This is REAL and
pre-existing (the old one-shot event had the same exposure), but this redesign's entire point is
a gated, earned reform — leaving an unconditional side door defeats it. Add the same
chain-complete gate to the law option:
```
qing_salt_reformed = {
	allow = {
		has_variable = qing_reform_track_unlocked
		has_variable = qing_salt_reform_chain_complete
	}
	on_enact = { set_variable = { name = qing_salt_gabelle_reformed  value = 1 } }
}
```
This makes the law option a second, equally-earned ROUTE to the same end-state (useful for a
player who already ran the chain and decision but also wants to enshrine it in statute) rather
than a shortcut around the chain. Not touching `qing_salt_farmed`'s own `on_enact` — the reset-
to-0 path stays available (matches the OR-guard fix above; resetting to 0 must remain legal so a
player can genuinely un-reform / re-enter graft, mirroring the old event's own reversibility).

### What this does NOT touch

- `QING_salt_assess_fitness` / `qing_salt_fitness` — unchanged, now read by `.9` instead of
  gating `.1`'s options.
- The standing quarterly `QING_salt_income` formula itself — unchanged; the decision acts on one
  of its existing inputs (`qing_salt_squeeze`), not the formula.
- `qing_salt_gabelle_graft` / Option B's flavor — unchanged, still reachable by declining at
  Statecraft Reform.

## Open questions for review

- Is the `.9` success condition (`authority - fitness > 0`) well-calibrated? Authority can reach
  at most 20+20+5+15+0 = 60 across the offered paths (assuming max-effort play); fitness is
  0-100. A highly fit/loyal commissioner (a real, not rare, state) could make the chain
  effectively unwinnable even with every "press" choice taken. Worth widening authority's ceiling
  or softening the comparison (e.g. `authority - fitness/2`)?
- Is retargeting `qing_revenue.1` in place (rather than adding a brand-new event id) the right
  call, or does reusing an id already referenced by other code/comments (`se_QING_SALT.txt:302-
  304`'s own comment naming "qing_revenue.1") risk confusion? The comment would need updating
  regardless.
- Should the `.8` bribe-retaliation risk be gated on `is_ai = no` player-only like the parent
  events, or should AI China face the same struggle (currently the whole file's events are
  `is_ai = no` gated — matches existing convention, not flagged as a question, just confirming
  no change intended there).
- `add_treasury = -120` and `-40` (the two short-term costs) are guesses, matching this project's
  own "boot-tune, flagged as a guess" convention — no existing figure to anchor them to since
  the old event had NO cost at all on this path.

## Review outcome (adversarial review, 2026-08-17)

Reviewed independently. Two real findings, both addressed above (§5 for the law-bypass/self-lock
issue — the more severe one, since it would have silently defeated the whole redesign's point;
the `QING_apply_estranged_once` mis-citation, cosmetic, fixed in §2 above). Everything else in
the design's factual claims about existing code checked out: event-id numbering, decision file
format, the salt income formula never reading the reformed/graft flags, the fitness helper, the
`QING_revenue_pulse` quarterly hook, and every cited idiom precedent.

**One review finding was itself checked against a live boot log and found FALSE, not adopted**:
the review claimed the design's "`var:A > var:B` is illegal, must stage a difference into one
var" premise is contradicted by a working counter-example at `se_USA_SECTION.txt:255`
(`var:usa_free_states > var:usa_slave_states`, cited via a `#97-fix` code comment claiming it
was corrected). Checked directly against the current boot's `error.log`: this EXACT site
(`USA_secession_check line: 9`, confirmed by re-reading the function body — it's the same
comparison) throws `"Illegal use of operator >"` in the live log. The code comment's claim was
wrong (it fixed a DIFFERENT bug — a missing `var:` prefix on one side, not the illegality of
var-vs-var comparison itself) — the standing memory rule and this design's original staged-
comparison approach are both correct as written. No change made on this point; recorded here
so the discrepancy doesn't get re-litigated from the same stale comment in a future session.

**Status: ready for implementation** with §5 (law-bypass closure) included as part of the
first-pass build, not deferred.
