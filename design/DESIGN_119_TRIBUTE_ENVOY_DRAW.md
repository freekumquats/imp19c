# DESIGN — #119 tribute envoy draws an existing sender office-holder

> STATUS 2026-08-11: SECOND REVISION, NOT YET REVIEWED. The FIRST revision (draw an office-holder,
> mint-primary/draw-as-enhancement — see "## REVISED PROPOSAL (post-review)" below) was itself flawed:
> it kept `create_character` as the permanent, dominant path forever (subject countries never seed a
> foreign-minister office-holder, so the draw would never fire) — quietly abandoning the actual point of
> #119 (stop minting) while only fixing the transfer-risk bug. See "## SECOND REVISION — use the ruler's
> PORTRAIT, mint nothing" at the very bottom for the current proposal. That section supersedes
> everything above it in this document. Must pass adversarial design review before implementation.

## Task text
`overnight/SESSION_HANDOFF_2026_08_11.md:63`: "#119 tribute envoy draws an existing tributary
office-holder, not create_character."

## Does this violate the standing character-creation rule as written?
No, not literally. `QING_tribute_mint_envoy` (`se_QING_TRIBUTE.txt:140-160`) mints a plain minor
character for the SENDER (tributary) country and adds no exam-degree trait — the standing rule is about
degree-holding CHI court characters. #119 is grouped with #111/#113/#114/#116/#117 in the design docs
(`DESIGN_ONE_POST_VAR_118.md:41,121,199,402`) by task-title analogy, but it is a different, looser ask:
verisimilitude — the envoy a tributary sends should be an existing notable of THAT country (its
foreign-minister-equivalent, or its ruler), not an anonymous nobody conjured fresh every single mission.

## What draw-target actually exists on subject countries today
The mod maintains NO Qing-authored roster of subject-country courtiers. What exists is the native
engine office system: KOR/VIE/RYU/NEP are monarchies (`office_foreign_minister`, `00_monarchy.txt`);
TNN is tribal (`office_arbitrator`, `00_tribal.txt`). The proven draw idiom already in this codebase is
`se_DIPLOMACY.txt:434-459` (`DIPLOMACY_trigger_play_event`): try `any_character = { has_office = ... }`,
`random_character` if found, `else = { ruler = { save_scope_as = foreign_minister } } }`. Setup files
seed subject countries with only the ruling family (`setup/characters/00_Korea.txt`, 3 characters) — no
ministers — so the office is VACANT at boot and the ruler-fallback is the common case, not an edge case.

## THE BLOCKING RISK a naive fix would introduce (found this diagnosis pass, not in the task text)
`QING_tribute_mint_envoy` mints a FRESH character it OWNS (`set_home_country = ROOT`, i.e. CHI-employed),
which is why `QING_tribute_dismiss_envoy` can safely `set_home_country = var:qing_tribute_envoy_home` at
the end — sending its own creation "home."

If the fix instead DRAWS the sender's real ruler or foreign minister via the `se_DIPLOMACY.txt` idiom,
that drawn character is NOT owned by CHI — he is the actual sitting ruler/minister of a live subject
country. Calling `set_home_country` on him (either at arrival, to bring him to the Qing court, or having
inherited the mint's own dismiss-home logic) would forcibly TRANSFER that country's real ruler or
foreign minister into CHI employ — leaving the sender country's own government short a ruler/minister,
a far worse bug than the one being fixed. The existing `qing_tribute.1` event and the `QING_tribute_receive`
prestige logic have no assumption today that the envoy scope is CHI-employed mid-mission, but
`QING_tribute_dismiss_envoy`'s `set_home_country` call is written assuming exactly that (a character it
just created), so it must NOT be reused unmodified against a drawn ruler/minister.

## What a correct fix needs
- Draw via the office-else-ruler idiom, but treat the result as a REFERENCE only — no `set_home_country`
  call anywhere in the mission if the character was drawn (only the fallback create_character path, if
  one is kept for some edge case, would still own+dismiss the character it made).
- The arrival event's portraits/scopes (`qing_trib1_envoy` var persistence, `qing_tribute.1`'s
  `right_portrait`) must still resolve correctly to a character who was never moved to CHI — confirm the
  event's `left_portrait`/`right_portrait` and any `employer`-based logic don't assume the envoy scope is
  CHI-employed.
- Decide whether a genuinely officeless AND ruler-absent case is even reachable (a subject always has a
  ruler in this engine, so likely not) — if reachable, needs an honest skip, not a crash.
- Confirm `QING_tribute_dismiss_envoy` is either skipped entirely for a drawn envoy (nothing to send
  home — he was never moved) or split into two paths (drawn: no-op; minted fallback if kept: existing
  behavior).

## Recommendation (ORIGINAL — superseded by the revised proposal below)
Do not implement #119 by reusing `QING_tribute_dismiss_envoy`'s set_home_country unmodified against a
drawn character. Design the two-path (drawn: reference-only / minted-fallback: existing mint+dismiss)
shape first, run it through an adversarial design review, then implement — same gate sequence as #116.

## REVISED PROPOSAL (post-review, 2026-08-11)

Adversarial review of the original recommendation found it NOT CLEAN on three points, all now corrected
below.

### Finding 1 — the office-else-RULER fallback backfires on #119's own goal
Setup files seed subject countries with ONLY the ruling family (`setup/characters/00_Korea.txt`, 3
characters, no ministers). Reusing `se_DIPLOMACY.txt`'s office-else-ruler idiom verbatim means the ruler
branch fires almost EVERY mission — so the fix would put the actual reigning King of Korea personally in
Peking every ~3 years. That idiom was written for `DIPLOMACY_trigger_play_event`, a sovereign-equals
diplomatic PLAY, where ruler-level representation is correct; a tribute embassy is the opposite — a
routine, subordinate ceremony historically staffed by officials, never the monarch in person (the
Korean 燕行使 was a delegation of officials). Drawing the ruler is a WORSE verisimilitude outcome than
the anonymous mint being replaced.

### Finding 2 — the correct shape is mint-primary / draw-as-rare-enhancement, not draw-primary / mint-fallback
Since no ministers are seeded, an office-only draw (NO ruler fallback) will almost always find nobody —
which is fine: it means the EXISTING create_character mint stays the common path (fresh, distinct,
correct-culture envoys, exactly as it works today), and drawing a real minister becomes a rare
enhancement that only fires when other content has actually created one for that subject. This also
resolves the repetitiveness cost (Finding 4 below) for free, since the mint remains dominant.

**Revised shape:**
1. Try `any_character = { has_office = office_foreign_minister / office_arbitrator }` on the sender
   country ONLY — no ruler fallback.
2. If found: use him as a REFERENCE for this mission. Do NOT call `QING_tribute_mint_envoy`. Do NOT set
   `qing_is_tribute_envoy` / `qing_tribute_envoy_home` / `set_as_minor_character` on him — those are the
   mint's own ownership markers and must not be stamped onto another country's real official.
2. If not found (the common case): call the EXISTING `QING_tribute_mint_envoy` unchanged — no behavior
   change from today for the typical mission.

### Finding 3 — the dismiss logic was NOT actually the transfer hazard; correcting the diagnosis
The original doc named `QING_tribute_dismiss_envoy`'s `set_home_country` call as the risk. Re-examined:
that call sets `set_home_country = var:qing_tribute_envoy_home` — the SENDER country, not CHI — and it
is itself guarded on `has_variable = qing_tribute_envoy_home`, a var ONLY the mint ever sets. A drawn
office-holder (per Finding 2's shape) never goes through the mint, so he never carries that var, and
`QING_tribute_dismiss_envoy` is ALREADY an automatic no-op for him — no dismiss-path split is needed.
The ONLY actual transfer-into-CHI vector was ever the MINT's own `set_home_country = ROOT` — which the
revised shape simply never calls for a drawn reference. No dismiss changes required at all.

### Finding 4 — persistent-reference repetitiveness, resolved by Finding 2's mint-primary shape
A drawn reference persists (same character, same portrait) across every mission from that tributary for
the reign. Under the revised mint-primary shape this is a non-issue in practice, since a draw only
succeeds when a real minister happens to exist — an enhancement, not the default experience.

### Finding 5 — the death/free/overthrow gap across the arrival-event delay is already handled
`qing_tribute.1` already re-validates its persisted envoy/sender vars before firing (`exists =
var:qing_trib1_envoy`, `var:qing_trib1_sender = { is_subject_of = ROOT }`) — if a drawn office-holder
dies or the subject is freed in the scheduler-to-arrival delay window, the event cancels cleanly with no
crash and (since he was never minted/marked) leaks no stray character/marker. No additional guard
needed beyond confirming this existing re-validation is unchanged.

### What still needs implementer attention (unresolved, carried from the original diagnosis)
- Confirm the office check (`has_office = office_foreign_minister / office_arbitrator`) is evaluated on
  the correct country scope (the sender, `scope:trib_sender`), matching how `QING_tribute_schedule_missions`
  currently establishes that scope before calling the mint.
- Confirm `qing_tribute.1`'s portrait/scope logic degrades gracefully for a referenced (non-CHI-employed)
  envoy — no code path should assume `employer = ROOT` for the envoy scope.

## Recommendation (revised)
Implement the mint-primary / draw-as-rare-enhancement shape (Finding 2), with NO ruler fallback and NO
dismiss-path changes (Finding 3 shows none are needed). This revised proposal must pass its own
adversarial design review before implementation — do not implement directly from this document.

**SUPERSEDED — see the section below.** This revision still kept `create_character` as the permanent
dominant path (since subject countries never seed a foreign-minister office-holder, the draw would never
fire, ever) — it fixed the transfer-risk bug from the ORIGINAL proposal but abandoned #119's actual
point (stop minting a character for this at all).

## SECOND REVISION — use the ruler's PORTRAIT, mint nothing (user-directed, 2026-08-11)

The user's correction: the envoy is pure EVENT FLAVOR. Confirmed by reading the actual rendering code
(`events/imp19c_mod_events/qing_tribute_events.txt:34-98`) — `scope:trib_envoy` / `qing_trib1_envoy` are
used for exactly ONE thing, `right_portrait` on `qing_tribute.1` (line 45). Nothing moves the envoy,
employs him anywhere, or reads him for any mechanical effect — `QING_tribute_receive` (the treasury/
prestige payload) operates on `scope:trib_sender` (the COUNTRY), never on the envoy character.
`QING_tribute_dismiss_envoy`'s only job is undoing the mint's own `set_home_country`/`set_as_minor_
character`/marker-stamp — machinery that exists ONLY because a character was created and needs undoing.

**There is no reason to have a character at all.** The sender country already has a real ruler
(`scope:trib_sender.current_ruler`), always exists (a subject always has a ruler in this engine), and
needs no draw, no eligibility gate, no fallback, no ownership, no dismissal — he never leaves his own
country's employ because nothing about rendering a portrait touches `employer`/`set_home_country` at all.

### Proposed shape (supersedes all prior revisions in this document)
1. Delete `QING_tribute_mint_envoy` and `QING_tribute_dismiss_envoy` entirely — both exist solely to
   create/undo a character that no longer needs to exist.
2. `QING_tribute_schedule_missions` (`se_QING_TRIBUTE.txt:87-114`): remove the
   `QING_tribute_mint_envoy = { sender = scope:trib_sender }` call and the `qing_trib1_envoy` var-persist
   (`set_variable = { name = qing_trib1_envoy  value = scope:trib_envoy }`) — nothing downstream needs a
   persisted envoy reference once the portrait reads the sender's ruler directly at fire time.
3. `qing_tribute.1` (`qing_tribute_events.txt:34-98`): change `right_portrait = var:qing_trib1_envoy` to
   `right_portrait = var:qing_trib1_sender.current_ruler` (the sender country var is already persisted
   and re-validated — `has_variable = qing_trib1_sender`, `var:qing_trib1_sender = { is_subject_of = ROOT
   }` — so no new persistence/guard machinery is needed). Both options' `QING_tribute_dismiss_envoy = yes`
   calls are removed (nothing to dismiss).
4. Trace forward for any OTHER reader of `qing_is_tribute_envoy`/`qing_tribute_envoy_home` (grep the
   repo) before deleting the mint — if nothing else reads those markers, the deletion is total; if
   something does, that reader needs its own resolution first.

### Why this is strictly better than every prior revision in this document
- Zero `create_character` calls — fully satisfies the actual point of #119, not a corner of it.
- Zero transfer risk (Finding 1/2 of the prior revisions) — nothing is ever moved, employed, or owned.
- Zero dead-draw-path concern (the prior revision's Finding 1 open question) — there is no draw to be
  dead; the ruler always exists, so the portrait always resolves.
- Zero repetitiveness cost in the way a MINTED envoy has (a fresh face every mission) is traded for a
  DIFFERENT, arguably MORE correct repetitiveness (the same ruler represents his country every mission,
  which is how a subordinate country's ruler-as-figurehead-of-record actually reads over a reign) — but
  since nothing personally travels or is "cast" as an envoy anymore, this is not really a repetitiveness
  cost at all; it's simply "the country is represented by its head of state in a portrait," the same
  idiom `left_portrait = root.current_ruler` already uses for CHI's own side of the same event.

This proposal must still pass adversarial design review before implementation — do not implement
directly from this document.
