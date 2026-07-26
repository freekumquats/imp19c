# Boot test 2026-07-25 (18:17 run, logs.zip + 3 screenshots) — running notes

Test build ≈ HEAD `fd2034c66` (18:08) — it PREDATES the loc + degree-title + tree-expansion commits
that followed at 18:29–18:33 and this session's work. So some "missing loc" reports below are already
resolved in the CURRENT tree and just need a re-boot to confirm. Log = `~/Downloads/logs.zip`
(extracted to `~/Downloads/logs_extracted/logs`). Screenshots: 182203 (Overview), 182337 (Religion),
183001 (Hanlin + Grand Council).

## Confirmed WORKING this test (fixes from the prior session landed)
- **BT — Religion panel** (screenshot 182337): the deity list scrolls inside the panel; the window is the
  right size (no runaway blank space). The 950→900 shrink + VerticalScrollAreaCutOff fix is good.
- **BT — Hanlin Academy population** (screenshot 183001): the Academy shows waiting laureates (e.g. Xie
  Ankai, 28, Neo-Confucian) with the roster/stat lines. The law-governed seed (QING_exam_seed_hanlin_pool,
  qing_hanlin_establishment_law cap) works — no more empty pool, and no autofill regression.
- **BT — Grand Council** (screenshot 183001): all seats populated (Yang Xiaoquan Censorate, Miao Enjue
  Lifan Yuan, Feng Anquan Guard, etc.) with skill/loyalty bars + Appoint buttons.

## Non-bugs (verified normal, no action)
- **Red "?" in the 4 National Idea slots** (screenshot 182203): these are vanilla `idea_slot_not_available`
  — empty, unpicked idea slots. Normal. (The idea system's 17 ideas all have complete name+desc loc.)
- **"country vs family" scope warnings** on `qing_americas_events.txt:255` (and aus_habsburg / fra_revolution
  events): load-time scope-inference warnings that also fire on vanilla-derived events. Not a runtime fault.
- **Culture "secondary"/tetrere/octere tokens + deity BOM tokens**: vanilla `common/cultures/*` and
  `setup/main/deities/*` baseline noise (documented). Not ours.
- **CURRENCY / TRADE / DEBT div-0 + "not set" floods**: the known upstream U4-class economy noise
  ([[imp19c-upstream-U4-flood-fix]]). Pre-existing, not this session.

## FIXED this session (committed + pushed)
- **BT — QING_pop_recompute_target none-value flood** (`d551409c6`): 3× at 18:23 "compare_value returned
  an unset scope" / "value of type none" at se_QING_POPULATION.txt QING_pop_recompute_target line 2. A
  transient early-pulse `total_population`→none left `qing_pop_pressure_target` unset, so the downstream
  `< 0` compares read an unset var. FIX: seed `qing_pop_pressure_target = 0` before the total_population
  read; the real value overwrites it on the next line. → VERIFY next boot: no pop-pulse errors at the
  first quarterly QING_GOV_pulse.
- **Reported missing loc `qing_office_chancellor_active` + `qing_hanlin_research_major`**: ALREADY present
  in HEAD (added `cf65cbfe1` @ 18:29, after the 18:17 test). No new work — just re-boot to confirm.
- **Admin/Academic tech trees too small** (`d551409c6`): oratory 32→60, religious 28→53 nodes; all with
  loc. → VERIFY next boot: both tech tabs render (NOT blank/4294967295 — the old date-gate failure mode),
  and the new nodes have names+tooltips.
- **Nation Overview modifier bar too small** (`d119d69cb`): the active-modifiers bar now horizontally
  scrolls (MarbleScrollBarHorizontal). → VERIFY next boot: with many country modifiers, the bar shows a
  horizontal scrollbar and all icons are reachable (no more hidden-past-the-edge).

## To VERIFY on the next boot (things touched but not yet seen working)
1. Admin + Academic tech trees render fully with all 57 new node names/tooltips (see above).
2. Nation Overview modifier bar scrolls horizontally (see above).
3. Pop-pulse no longer floods on the first quarterly tick (see above).
4. The 27 modifier locs + Hanlin scholar degree-title line (`[Character.Custom('qing_scholar_degree_name')]`,
   commit `f35474037`) — screenshot 183001 shows the roster but the degree-title line wasn't legible;
   confirm each waiting laureate shows a 功名 title (Hanlin/進士/舉人/…) under the name.
5. Building icons (24 stopgaps, `fd2034c66`) show in the macro builder + province window (foreign
   buildings no longer blank). Granary icon is lower-res (100×100 source) until real art.

## Still OPEN / carried forward (not this test)
- Bespoke `.dds` art for the ~130 placeholder icons (mission tasks test1/2/3, panel headers, distinctions,
  buildings) — pipeline documented in placeholder_icons.md; blocked on standing up a DDS encoder + the
  licensing decision.
- The Decision-candidate build-out (QING_DECISIONS_ANALYSIS.md): the genuinely-new best-fit picks are
  Resettle the Coast (遷界令 reversal), Open a Treaty Port by choice, Grand Amnesty (大赦天下) — NOT yet
  built, awaiting user go-ahead. (Move Capital + Lift the Sea Ban already have working surfaces.)
