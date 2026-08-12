# DESIGN — #119 tribute envoy draws an existing sender office-holder

> STATUS 2026-08-11: DIAGNOSIS ONLY. Not implemented, not reviewed.

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

## Recommendation
Do not implement #119 by reusing `QING_tribute_dismiss_envoy`'s set_home_country unmodified against a
drawn character. Design the two-path (drawn: reference-only / minted-fallback: existing mint+dismiss)
shape first, run it through an adversarial design review, then implement — same gate sequence as #116.
