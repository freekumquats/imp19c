# Overnight run — 2026-08-04

Autonomous fix run on branch merge-overnight. Directive: fix Talleyrand, investigate the
debug.log `IMP19C FAIL` classes, fix all pending tasks, adversarial-review every change
before commit, log all decisions here, then implement DESIGN_MG_BUILDING_PRODUCTION_HOOKS.md.

Boot under analysis: **logs.zip Aug-4 01:32** (build hash f669472e, boot started 00:57:53).
CRITICAL: this boot PREDATES every commit made 2026-08-04 (Talleyrand fc4b53970 @01:09 and its
revert 30cac0e71 came AFTER the 00:57 boot). So this log is the PRE-FIX baseline; bugs reported
during the test (Talleyrand first) are in the tested build by definition.

---

## Correcting the record: the Talleyrand commits fc4b53970 + 30cac0e71 were BOTH wrong

- fc4b53970 wrapped keju.4's IMMEDIATE create_character in hidden_effect, claiming the option
  tooltip previewed a not-yet-created char. WRONG: immediate runs before the window renders, so
  that wrap is a no-op for the preview.
- 30cac0e71 reverted it, claiming hidden_effect CAUSED a 51k flood. Also WRONG: the tested build
  (00:57) ran neither commit — it ran the ORIGINAL bare-immediate keju.4 and STILL floods 76,455
  lines. So hidden_effect neither caused nor fixed the flood.
- The flood IS the Talleyrand bug (one root cause, two symptoms): scope:failed_scholar is not
  bound during the OPTION-EFFECT tooltip preview, so option 4.a's `scope:failed_scholar = { ...
  QING_char_bind }` -> QING_char_affinity runs its ~20 var ops (set_variable qing_char_affinity=50
  then read it) against an unbound scope. In tooltip-EVAL the set_variable is skipped but the reads
  are evaluated -> 76,455 "unset scope / Invalid comparison / Failed to fetch qing_char_affinity".
  keju.4 fired ONCE; all 76k is pure preview volume. keju.4's create_character does NOT fail
  (verified: only unrelated qing_guard_events:185 create fails in the whole log).

### Evidence pinning the mechanism
- All 76,455 errors chain: qing_keju_events.txt:357 (option 4.a) -> QING_char_bind:5 -> QING_char_affinity:9/80/81.
- keju.4's OTHER options 4.b/4.c reference scope:failed_scholar (add_trait/add_loyalty) and throw ZERO
  errors — because they don't call the var-heavy QING_char_bind. So the scope resolves for simple ops;
  only QING_char_affinity's var set-then-read pattern breaks under tooltip-eval.
- keju.2.a has the IDENTICAL structure (custom_tooltip + scope:laureate = { QING_char_bind }) and fired
  this boot (01:05) with ZERO flood — because keju.2's laureate is normally an EXISTING courtier whose
  affinity var may already exist / whose scope is bound differently; keju.4's scholar is freshly minted
  and never had QING_char_affinity run, so the preview-eval read of the unset var fails.

### The fix (PROVEN idiom, this time on the right target)
Wrap the OPTION-EFFECT (`scope:failed_scholar = { ... QING_char_bind }`) in `hidden_effect`, keeping
the option's existing `custom_tooltip` for player-facing text. hidden_effect suppresses the tooltip
EVAL (not just display) — proven by: INV 971 / TI 621 options pairing custom_tooltip+hidden_effect, and
the mod's own qing_new_world_missions.txt:155 ("wrapped in hidden_effect: the reward-preview tooltip-eval
... resolves to none in preview context; hidden_effect suppresses it"). Runtime unchanged (hidden_effect
hides tooltip, not effect). This is the OPTION effect, NOT the immediate mint fc4b53970 wrongly targeted.

---

## Changes (chronological)

### [1] Talleyrand fix (keju.4.a + latent keju.2.a) — events/imp19c_mod_events/qing_keju_events.txt
Wrapped both options' `scope:<char> = { ... QING_char_bind }` bodies in hidden_effect (keeping
custom_tooltip). Kills the 76,455-line flood + the Talleyrand-in-preview sighting. 4.a manifested
this boot; 2.a is the same latent bug on its fallback-mint path (guarded proactively per "no
deferring"). NOT the immediate-mint wrap that fc4b53970 wrongly did. Braces balanced.

### [2] IMP19C FAIL investigation (debug.log, 1310) — VERDICT: all benign, nothing to fix
Every FAIL is a LOG_fail SKIP-trace (guard reporting an intended no-op), not an error:
- DEJURE 623 = "de jure baseline already frozen; skipping re-freeze" (idempotency guard, WAI).
- DEJURE 7 = on_ownership_change on an ownerless/empty/unfrozen province (correct skip).
- QING 613 = QING_seed_starting_treasury "not CHI or already seeded" (per-country guard for the
  ~660 non-CHI nations iterated at setup — WAI).
- QING ~8-each = QING_napoleon/DECLINE_spawn_*/army_* pulse guards correctly not firing (below
  threshold / on cooldown / no eligible target). SEPAR 16 + MARRIAGE 1 likewise (gate not met /
  no marriageable pair). No action.

### [3] Estranged Servant loyalty overhaul (task #4) — 00_imp19c_loyalty.txt, se_QING_AFFINITY.txt, se_QING_WAR.txt, se_QING_NAPOLEON.txt, qing_loyalty_l_english.yml
Root: Songchun/Fulu/Guanting pinned at the -35 Estranged floor. Two causes: (a) magnitude too harsh,
(b) re-stamped every pulse with no idempotency guard (QING_char_bind + QING_war_review_commanders +
QING_napoleon_loyalty_pulse). Fix:
- Recalibrated loyalty_qing_estranged -16/min-35 -> value -5/min -10 (vanilla trait-shift band; severe
  tier loyalty_qing_disgraced -40/-60 stays for real hostility). loyalty_qing_congenial 14 -> 10, +max 10.
- Added shared apply-once helpers QING_apply_estranged_once / _congenial_once (has_loyalty guard + shed
  opposite band; proven verbs). QING_char_bind + the 4 se_QING_WAR sites + the 2 se_QING_NAPOLEON monthly
  sites now call them instead of bare add_loyalty.
- Review finding (band-cross): the "both central armies rotting" term (se_QING_WAR MO-ENH #3) is meant to
  be ADDITIVE on top of affinity scoring, but the shed-opposite-band helper would let the well-managed
  branch cancel it in the same pass. Fixed by giving it a DISTINCT modifier loyalty_qing_army_collapse
  (value -5/min -10, own helper QING_apply_army_collapse_once + QING_remove_army_collapse on recovery), so
  it coexists with congenial/estranged. Loc added. All braces balanced.
- Deferred-as-safe: se_QING_FACTION 487-525 (one-shot event options, not a recurring pulse — no re-stamp).

### [4] Non-Neo-Confucian −10 max-loyalty penalty (task #5) — qing_mechanics_modifiers.txt, imp19c_setup_events.txt, modifiers_l_english.yml
Vanilla WRONG_RELIGION_MAX_LOYALTY = -10 (defines:617) caps loyalty for every char whose religion !=
state religion. Qing state religion = confucianism, but the court is ~163/275 Tibetan-Buddhist
(vajrayana/mahayana) Manchu/Mongol elites whose faith was compatible with the Confucian state — the
flat -10 is historically wrong. Fix (user's "+10 Qing modifier" option, chosen over editing the global
define or exempting religions the flat define can't express): new CHI country modifier
qing_confucian_syncretism { max_loyalty = 10 }, applied once at CHI game-start (imp19c_setup.11,
guarded NOT-has-modifier), + loc. max_loyalty as a country modifier is proven (is_tribe 00_hardcoded;
TI 00_from_events_country). Net for same-religion Confucian chars: a mild +10 cap bonus (fine). braces OK.

### [5] Bayara create_character invalid culture/religion (task #9) — se_QING_GUARD.txt
QING_guard_raise_bayara's create_character used culture = ROOT.primary_culture (INVALID field —
boot error.log: 'scope type none, expected culture', PostValidate false, char NOT minted) + religion
= ROOT.religion (same invalid-field class as #61). Fixed to literals culture = manchu / religion =
vajrayana (Bayara 巴牙喇 = Manchu Tibetan-Buddhist banner palace-guard) — identical to the existing
se_QING_AMBAN.txt:122-123 fix. Swept the repo: no other create_character has this bug (remaining
ROOT.religion hits are valid pop_religion= / this.religion= comparisons). braces OK.

### [6] Anhua "Conservative Bloc" on a stratocracy card (task #6) — gui/characterwindow.gui
Root: stratocracy (common/governments/00_albert.txt:132) is `type = republic`, so the engine assigns
its characters republican parties (conservative/liberal/radical) and the card's party row (gated only
on IsRepublic) shows them — on a Manchu banner MILITARY GOVERNORATE (14 subjects: Jilin/Mukden/HLJ/
Ili/Uliastay/etc.) with no electoral politics. Considered but REJECTED the "root" fix (change
stratocracy type republic->monarchy): 14 subjects, swaps elections for heir-succession — too broad an
autonomous gameplay change, and the mod already treats stratocracy as non-republican via
generic_republic_trigger (excludes it). switch_to_random_party has no mod caller (engine-assigned), so
can't gate assignment. Kept it a VISUAL fix (the scope it was reported under): gated the party grid +
the senate-seat row on IsRepublic AND NOT stratocracy, comparing GetGovernment.GetName (localized) to
Localize('stratocracy') — the proven GUI string-compare idiom. NOTE: parties are still assigned in the
data (harmless); only the misleading card display is suppressed. braces OK.

### [7] minor_chi missing loc (task #3) — core_l_english.yml
minor_chi = engine auto family key for the ~147 CHI chars with family_name but no family= link (great
Manchu banner clans Fuca/Guwalgiya/Niohuru/etc. — historical individuals, not registered houses).
GetFamily.GetName rendered the raw key on their cards. Added loc `minor_chi:0 "Minor House"`. Chose the
loc fix (as reported) over minting 40 real family blocks for 147 period figures (not dynastic houses).

### [8] GC offices credited to Scorned Family mechanic (task #2) — qing_governance_modifiers.txt, se_QING_COUNCIL.txt, se_QING_GOVERNANCE.txt, modifiers_l_english.yml
FEATURE (not a bug fix — Sobisonator never wired this; additive, bug-vs-feature rule permits). The
vanilla Scorned Family mechanic (00_hardcoded.txt scorned_family + engine-internal loyalty hit) counts
ONLY engine job/office slots when deciding a family is under-employed and scorning every member's
loyalty. The mod's ~9 Qing court positions — Grand Council great offices (qing_office_held) + the
sub-positions (Zongli diplomat / Inspecting Censor / Imperial Guardsman / Southern & Upper Study scholar
/ Amban / palace eunuch / harem consort, the exact set already enumerated by QING_validate_one_position)
— are custom vars the engine's counter can't see, so a Guwalgiya/Niohuru grandee ON the Grand Council
still read as idle and got scorned. Fix: new QING_scorned_office_credit sweep (called from QING_GOV_pulse
next to the validation sweep) grants an offsetting character_loyalty credit ONLY while BOTH his family
is_scorned AND he holds a position, stripped the instant either lapses. Two tiers: great office
qing_office_family_credit (+8), sub-position qing_subpos_family_credit (+4); at most one carried (great-
office branch sheds any stale sub-position credit, and vice-versa; the else branch strips both on
recovery). is_minor_character=no guards the no-real-family case. All idioms proven: family={is_scorned=yes}
(on_ambitions:2894), add_character_modifier duration=-1 (se_QING_MECHANICS:197), has_character_modifier.
Loc added for both modifiers. Braces balanced (896/896).

### [9] Subject-integration actors overhaul (tasks #7 + #8) — se_SUBJECT_QING.txt, qing_subject_integration.txt, qing_integration_capstone_events.txt, 2 loc files, design/DESIGN_SUBJECT_INTEGRATION_ACTORS.md
FEATURE (additive — makes the resident amban + garrison, already tracked, actually GATE the choices;
bug-vs-feature rule permits). Design note written first (design→review→implement rule), decisions
logged there. #7 is two fixes inside the chain #8 overhauls, so done as one piece.
- **New shared resolver SUBJ_QING_resolve_integ_actors** (+ _clear_integ_actors): reads the resident
  amban (qing_amban_here, se_QING_AMBAN) → integ_amban_present / scope:integ_amban / integ_amban_band
  (0/1/2 on his loyalty), and the CHI garrison on the subject's soil (the QING_fgar_scan every_army +
  unit_location.owner walk) → integ_garrison_size vs the subject's own army sum integ_subject_size →
  integ_garrison_edge band (0 subject-outweighs / 1 parity / 2 garrison-dominant). No new persistent
  state; scratch vars cleared at each option tail. LITERAL-RHS bands (delta-var trick), proven
  `<iter> = { ROOT = { add = prev.unit_size } }` accumulation (COUNCIL:591), band var init'd
  unconditionally so no missing-var read.
- **#7a — crush = REAL war** (SUBJ_QING_crush_revolt_war, wired into .41.b): reparent sub-subjects →
  release_subject → FUNC_declare_war_with_wargoal_province conquer war on the freed rebel. Proven
  (JAPAN_PREPERRY release+war, setup_events declare func, reparent helper). Guarded to a live landed
  subject.
- **#7b — marry = REAL marriage** (SUBJ_QING_marry_into_chieftain, wired into .41.c): weds eldest
  eligible imperial prince to chieftain's eldest eligible daughter via marry_character (Invictus
  me_bithynia idiom). Guarded both sides; wedding-skip degrades to gold/prestige co-opt.
- **Actor-gated options**: .41.d staunch-amban-negotiates, .10.d steady-amban-calms-unrest, .12.d
  steady-amban-mediates (all hidden unless a present amban of the needed band sits). Garrison edge
  cheapens the force paths (.41.b/.10.a/.12.a/.30.c) and, when dominant, marches the garrison out vs
  holds its fortress (.41.b); a wavering/absent amban flees his post (.41.b). Loc added for all new
  options + refreshed .41.b/.41.c tooltips (war + wedding now literal).
- **Lighter touch** on .11/.20/.21 (not force-vs-persuasion dilemmas — resolver not run there).
- Braces balanced on all four code files (SUBJECT_QING 410/410, capstone 107/107, integration 149/149).

### Adversarial review (code-review agent, before commit)
Reviewed the full uncommitted diff, deep on tasks #2/#7/#8. VERDICT: no critical/high bugs — all six
high-risk axes verified correct (prev.unit_size binds to the iterated army as intended; scope:target
+ scope:integ_wargoal_prov stay valid after release_subject; every band var set unconditionally before
any option reads it; marry_character form matches se_MARRIAGE precedent; is_scorned family idiom + the
sweep's idempotent add/strip; zero RHS-comparison violations). Two LOW findings, both fixed:
- LOW#1 (latent): crush-war path left a stale SUBJ_integration_* meter on the freed rebel → if
  re-subjugated later it could fire the .30 capstone immediately. FIXED: clear integration state on
  scope:target before release_subject (mirrors SUBJ_QING_absorb_subject). 
- LOW#2 (flavour): code comments said "eldest" but order_by=age/max=1 picks youngest (same as the
  se_MARRIAGE precedent). FIXED: comments reworded to "an eligible child, deterministic" — no behaviour
  change (the precedent has the identical wording quirk).
