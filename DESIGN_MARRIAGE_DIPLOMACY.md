# DESIGN — Marriage Diplomacy & Dynastic Union (follow-up scope)

**Status:** SCOPED, not built. Feasibility-gated: several hooks are UNPROVEN and MUST pass an
oracle consult (Terra-Indomita + Invictus) before any build, per the standing oracle rule.
**Origin:** spun out of the Grand Council Empress-seat work (2026-07-09). The Empress seat itself
(current_ruler.spouse) ships in the GC batch; THIS is the larger inter-country layer, deliberately
deferred so it doesn't bloat that batch.
**Branch when built:** develop, own commit(s). Author freekumquats.

---

## 1. Intent
Give royal marriage a DIPLOMATIC dimension beyond the character-level `marry_character` that
currently exists only in the vanilla spouse-seeking scheme. A marriage between two ruling houses
should be able to:
- bind two realms (alliance / non-aggression / reduced tension), and
- open a path to DYNASTIC UNION and eventual INHERITANCE of one realm by the other —
  modelled to fit the existing `royal_union` subject type and the mod's concrete-over-abstract rule.

Historical fit for the 1815 Qing-centric setting is thin (Qing did not marry into European
houses), so this is primarily a mechanic for the European/dynastic AI powers and any player
running such a country — NOT a Qing-specific feature. Confirm target scope with user before build.

## 2. What ALREADY EXISTS (proven — verified 2026-07-09)
- `royal_union` subject type (common/subject_types): has_overlords_ruler=yes (shared ruler /
  personal union), joins_overlord_in_war, can_be_integrated, subject_can_cancel=no,
  overlord bears next_ruler_legitimacy -0.05. ~14 subjects incl. royal_union chains ship at 1815.
- `make_subject` (48 uses) / `release_subject` (24) — PROVEN subject create/teardown verbs.
- `marry_character` / `divorce_character` — PROVEN (00_ambitions.txt spouse scheme), character scope.
- `spouse` scope link — PROVEN (00_ambitions.txt:1230 exists=spouse); basis of the Empress seat.
- Ruler-change / death on_actions: qing_mechanics_on_actions.txt + 00_specific_from_code.txt —
  PROVEN hook points for "on ruler death, evaluate union/inheritance".
- primary_heir_attraction / next_ruler_legitimacy — PROVEN succession-weight country modifiers.

## 3. What DOES NOT exist / is UNPROVEN (MUST oracle-check BEFORE building)
- **[UNPROVEN-1] Automatic country inheritance on a shared-ruler's death.** Does the engine, when
  a royal_union overlord dies and the union shares his ruler, transfer/merge the subject's realm?
  personal_union_ruler + inheritance_svalue/inheritance_right exist as engine concepts but NO mod
  content uses them. ASSUME NOT until oracle-confirmed. Fallback: model inheritance OURSELVES via a
  scripted on_ruler_death handler that fires make_subject / annex logic (concrete, proven verbs).
- **[UNPROVEN-2] Forming royal_union FROM a marriage.** Can script, on a marriage between two ruling
  houses, create a royal_union bond (make_subject=royal_union) conditioned on there being no male
  heir in the junior house? Verb is proven; the DESIGN LOGIC (who becomes junior partner, when it
  triggers) is ours. Low risk — make_subject is proven — but confirm the diplomatic legality gates.
- **[UNPROVEN-3] Marriage between characters of DIFFERENT countries.** marry_character is proven
  same-court; can it marry a character in ANOTHER country's court (a foreign princess)? Needs oracle
  or a scripted create_character-in-our-court-then-marry fallback (as the spouse scheme already does).
- **[UNPROVEN-4] AI willingness / a diplomatic ACTION.** A player-facing "propose royal marriage"
  diplomatic action (scripted_gui or diplomatic interaction) with AI accept/reject scoring — does the
  interaction framework support a marriage payload? Fallback: an EVENT-driven offer (trigger_event to
  target country) rather than a formal diplomatic_action.

## 4. Proposed model (build ONLY after oracle clears §3)
Layered, each layer independently shippable:
- **L1 — Marriage pact (lowest risk):** a proposal (event or diplo action) that, on accept, marries a
  character of each court (create-in-court fallback if cross-court marry is unproven) and applies a
  RELATION bond: alliance OR a "royal marriage" country modifier reducing tension / raising trust.
  Uses only proven verbs. Ship this first.
- **L2 — Dynastic union:** if the two houses share a ruler (heir of one is the other's ruler) OR a
  junior house is left without a male heir, form royal_union via make_subject. Gated on §3 UNPROVEN-2.
- **L3 — Inheritance on death:** scripted on_ruler_death handler (qing_mechanics_on_actions.txt) — if a
  royal_union's shared ruler dies and inheritance conditions hold, transfer the junior realm (annex or
  re-parent). Gated on §3 UNPROVEN-1; model ourselves, do NOT rely on engine auto-inheritance.
- **L4 — GUI + loc:** a marriage-diplomacy panel or diplo-action button; se_LOG (sys = MARRIAGE or reuse
  QING where CHI-relevant); SESSION_REPORT + fix-traceability per standing rules.

## 5. Interactions / risks
- Ties to the Empress seat: a foreign-princess Empress could be the L1 payload for CHI (flavour only;
  no union for the Qing — they integrate, they aren't inherited).
- royal_union overlord penalty (next_ruler_legitimacy -0.05) already balances holding unions.
- Nested-union chains already ship (imp19c-nested-subjects-viable) — L2/L3 must not break those.
- Concrete-over-abstract: prefer real subject bonds + real on-map annexation over abstract "union points".

## 6. Build gate
DO NOT START until: (a) oracle consult resolves §3 UNPROVEN-1..4, (b) user confirms target scope
(AI-only dynastic powers vs. player feature; whether CHI participates at all), (c) it is sequenced
AFTER the current GC batch (#272/#273) and #165.
