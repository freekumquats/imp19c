# Task #33 — Which Qing choices fit the vanilla Decisions mechanic (ANALYSIS ONLY)

Date: 2026-07-25. Analysis only — no build. Answers "what player choices would fit under the vanilla
Decisions mechanic" given everything the mod already ships.

## The Decisions mechanic, and where it fits

`decisions/*.txt` → `country_decisions = { <name> = { potential / allow / effect / ai_will_do } }`.
The mod already uses it three times (imp19c_ideology / imp19c_economy / imp19c_south_american_revolutions
+ the vanilla culture_decisions). The idiom (see `imp19c_ideology_decisions.txt`): CHI-gated, a `potential`
visibility gate, an `allow` readiness gate (guarded var reads), an `effect` that usually fires a choice/
trampoline event (keeping heavy effects out of compile-inlining — the #443 class), and `ai_will_do = 0`
for player-only.

**A decision is the right tool ONLY when the choice is:**
- **One-shot / rare** — fires once and flips a durable state (re-adoption would need its own decision).
- **A strategic PIVOT, not recurring policy** — recurring "which stance" belongs in a **law** (we have 36).
- **Not a multi-step arc** — a staged campaign belongs in a **mission tree** (we have 16).
- **Not a continuous lever** — a per-pulse dial belongs in a **scripted-gui panel** (we have ~60 subsystems).
- **Naturally read as "the throne RESOLVES to X"** — a deliberate, gated, headline act.

## What is ALREADY covered (do NOT rebuild as decisions)

- **Recurring policy stances** → the 36 qing_*_law groups (opium, caravan customs, hoppo, succession method,
  tribute ritual, exam curriculum, modernization doctrine, customs regime, etc.). Laws already ARE the
  "set-and-forget posture" surface. A decision here would duplicate.
- **Multi-step territorial / reform campaigns** → mission trees (colonization, self-strengthening, reform,
  treasure fleet, Xinjiang, Burma, open-Japan, Taiping, summer palace, …).
- **Continuous governance dials** → panels (Grand Council, harem, censorate, canal, caravan, customs,
  amban, deliberative, household, …).
- **Ideology adoption** → already a decision (qing_embrace_political_creed).

## CANDIDATES THAT GENUINELY FIT (one-shot strategic pivots, currently only reachable via event/flag or not at all)

Ranked by fit + value. Each is a *pivot* that flips durable state, era-gated, player-only.

### Tier 1 — strong fit, clear gap
1. **移都 / Move the Capital (遷都)** — resolve to shift the capital (e.g. Beijing → a southern/coastal
   seat for a maritime-facing reign, or the reverse). One-shot, durable, headline. Gate: stability +
   treasury + own the target province. Effect: set_capital + a transition modifier. No current surface.
2. **廢除海禁 / Lift the Sea Ban** — the single deliberate reversal of the closed-coast posture, the natural
   PRECONDITION pivot for the Treasure Fleet tree + maritime trade. Gate: High-Qing era or reform pressure.
   Effect: a standing "open coast" country modifier (commerce + ship-build) + unlock flag. One-shot.
3. **改土歸流 / Abolish the Native Chieftaincies (bulk)** — the empire-wide resolve to convert the remaining
   tusi (土司) to regular administration in one strategic act (the arc's capstone as a *decision*, distinct
   from province-by-province events). Gate: reform track. Effect: state-loyalty + assimilation nudge.
4. **遷界令 reversal / Resettle the Coast** — undo the Kangxi-era coastal clearance; a one-shot repopulation
   pivot. Gate: coastal provinces owned. Effect: pop-growth/settlement modifier on coastal states.
5. **禁教 → 弛禁 / Toleration Edict for Christianity** — the one-shot reversal of the 1724 proscription (or
   its re-imposition), a headline reign-defining act distinct from the recurring missionary-policy law.
   Gate: reform pressure OR a Western-embassy flag. Effect: flips the missionary-tolerance state.

### Tier 2 — good fit, more niche
6. **開海設關 / Open a New Treaty Port by choice** — proactively designate a second licensed port (vs the
   forced treaty-port events), a deliberate liberalization pivot. Gate: coastal port owned + reform.
7. **改元 / Proclaim a New Reign Era-Name** — a legitimacy-reset flourish on accession/after a crisis.
   One-shot per reign. Gate: new ruler / low legitimacy. Effect: legitimacy + stability tick, a modifier.
8. **大赦天下 / Grand Amnesty** — a one-shot unrest-relief + legitimacy act (vs the recurring penal law).
   Gate: high unrest or on accession. Effect: unrest cut + tyranny cut, cooldown-gated so it stays "rare."
9. **編修四庫全書 / Commission the Complete Library (四庫全書)** — the Qianlong cultural-capital monument as a
   one-shot prestige project (with the literary-inquisition dark side as a choice). Gate: High-Qing era +
   treasury. Effect: research/legitimacy modifier (± a censorship cost).
10. **停止捐納 / Abolish the Sale of Offices** — a one-shot anti-corruption reform pivot (the office-selling
    LAW is the recurring stance; the DECISION is the irreversible abolition). Gate: reform track + PI.

### Tier 3 — fits but lowest priority / overlaps existing arcs
11. **鑄新幣 / Currency Reform (mint a new standard)** — one-shot monetary reset; overlaps the currency
    subsystem, so only if it does something the U-series currency model doesn't.
12. **修長城 / Restore the Great Wall** — one-shot defensive monument; overlaps the Public-Works buildings
    now in the macro builder (BT-L), so likely better as a building than a decision.

## RECOMMENDATION

If any of these are built, start with **Tier 1 #2 (Lift the Sea Ban)** — it's the cleanest fit (one-shot,
durable, currently missing) AND it thematically GATES the Treasure Fleet tree just expanded in BT-M, giving
that tree a proper deliberate entry pivot. **#1 (Move the Capital)** and **#5 (Christian Toleration Edict)**
are the next best — both are headline reign-defining pivots with no current one-shot surface.

Everything recurring, staged, or continuous is already better served by the existing law / mission / panel
surfaces — the Decisions mechanic should be reserved for the deliberate, rare, durable PIVOTS above.
