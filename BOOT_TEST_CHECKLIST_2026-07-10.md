# 1763 Boot-Test Checklist — bugs fixed 2026-07-10

Branch: **1763_bookmark** (pull latest — all fixes pushed to `origin/1763_bookmark`).
Commits in this batch: `360fe45d`, `d42deb74`, `33d45d36`, `0b1bc66f`.

How to use: boot the mod as the **Qing (CHI)** at the 1763.2.16 start unless a row says otherwise, then walk the list. Each row says **where to look** and **what "fixed" should look like**. Tick the box if it holds; note anything that doesn't.

---

## A. Needs in-game verification (fixes applied but UNPROVEN — check these first)

These four are the ones I could not prove from script alone; they are the real reason to test.

- [ ] **B21 — armies no longer stack on Beijing.** Open the military/army view (or the map) right after start. The ~27 Qing garrisons should be **spread across their provinces** (Xi'an, Ili, Mukden, Chengdu, Canton, Fuzhou, Ningxia, Kashgar, etc.), NOT all piled in Beijing. *(4th attempt at this — the fix switched to the `location = prev.prev` province→owner idiom. If they still stack, that idiom is also wrong and we escalate.)*

- [ ] **B22 — all three coastal navies appear.** Check the navy list / coasts. There should be **three** water-forces: 廣東水師 (Guangdong, Canton p:9298), 福建水師 (Fujian, Fuzhou p:3651), 浙江水師 (Zhejiang, Ningbo p:2893). Before the fix only Fujian appeared.

- [ ] **B12 — Dynastic Match table is populated.** Open the marriage/dynastic-match window (Grand Council tab → **Reports**? no — it's the marriage button in the Edicts strip, or wherever the L4 marriage GUI opens). The candidate list should show **foreign houses with eligible children**, not be empty. This was expected to fix itself once real rulers (with children) load — see B1/B2 below.

- [ ] **B14 — Supranational window opens.** Click the **Supranational** icon (left topbar / outliner). A window should open showing the **Diplomatic Plays** tab. Before the fix, clicking it did nothing (the window was culled because the Qing isn't in a federation).

---

## B. Ruler data (B1/B2) — check the major powers' rulers at start

Root cause: an earlier cleanup left several powers with **no ruler set**, so the engine generated random childless placeholders (the "Grigoriy Bulganin" you saw for Russia) — which also emptied the marriage table (B12).

- [ ] **Russia** ruler is **Catherine II (Yekaterina II "the Great")**, not a random name.
- [ ] **France** ruler is **Louis XV**, not a 9-year-old Talleyrand.
- [ ] **Great Britain** ruler is **George III**, and he is **sane/capable** — NOT flagged lunatic/incapable/stressed (those were his 1815 Regency-crisis traits; at 1763 he was 25 and fine). He should have `confident` + `just`.
- [ ] **Ottomans (TUR)** have an **adult sultan (Abdul Hamid I)**, not a toddler or a random placeholder.
- [ ] **USA** — Madison is **not** the ruler (he was a 12-year-old; USA is a pre-independence anachronism in 1763). Engine placeholder is fine here.
- [ ] Not-a-bug spot checks (should be historically CORRECT child rulers, leave them): Naples (Ferdinand IV), Sardinia (Vittorio Emanuele I). SWE/PRU/BAV/SXH have engine-generated rulers (no in-file candidate) — acceptable.

---

## C. Grand Council / Government view (Qing)

- [ ] **B4 — office count reads "/ 13"** in the Grand Council roster header (was "13 / 11").
- [ ] **B7 — the Appoint button works.** In the Grand Offices grid, click **Appoint** on any office; the picker window should open with a **non-empty list of candidates** (including sitting ministers you can reshuffle). Before, it opened an empty picker / did nothing.
- [ ] **B8 — the offices window is titled "Grand Offices of State"** (was "Great Offices of State").
- [ ] **B5 — Throne cards are not clipped.** The Emperor / Crown Prince / Regent cards should show their full **4-skill statesmanship row** at the bottom — not cut off by the Dynastic Health panel below.
- [ ] **B9 — office-card Appoint buttons are fully visible.** In the 3 rows of office cards, the Appoint/Replace button at the bottom of each card should not be clipped.
- [ ] **B6 — the "Emperor rules in his own person…" Grand Regent text wraps** onto multiple lines and isn't cut off on the right.
- [ ] **B24 — Emperor Emeritus card shows when present.** The Chancellor + Regent + (if a Taishang Huang exists) Emeritus column should all be visible. *(Note: the width-reduction ask — boxes filling only 2/3 of the row — was deliberately NOT done; the Chancellor card's 4-skill row needs its width. Tell me if the full-width boxes still bother you.)*

## C2. Grand Council Edicts strip (B10 reorg)

- [ ] **B10a — one "Canton Trade" button** (not separate Open/Close). Clicking it opens a **Canton Trade window** with the open/close action(s) inside.
- [ ] **B10b — the Court Britain/France/Russia + Japan accord/rivalry buttons are GONE from the Edicts strip** and now live inside the **Great Game panel** (open it via the Great Game button → scroll to "Courting the Powers").
- [ ] **B10c — one "Reports" button** (not three). Clicking it opens a **Reports window** with launchers for: New World Crops, Ethnic Tension, Migration, and **Sinicization**.

## C3. New Qing mechanics

- [ ] **B25 — Emperor "Retreat into Seclusion".** In the Edicts strip there's a **Retreat into Seclusion (退居休養)** button (shown for a capable adult emperor). Clicking it should cost legitimacy and open a **Grand Regency** (regent-selection event fires). A **Resume Personal Rule (親政)** button should appear while secluded, and dissolve the regency when clicked.
- [ ] **B26 — Sinicization report** (via the Reports window, see B10c) lists provinces whose dominant culture is **Han (chinese_group)**.

---

## D. Diplomatic view — Subject tab (Qing subjects)

- [ ] **B15 — Integrate/Loosen buttons no longer overlap the labels.** Open a subject (e.g. a governorship) in the diplomatic view → Subject Actions. The action buttons should sit **below** the subject-type/interaction header text, not on top of it.
- [ ] **B16 — the "Overseer" portrait shows the resident Amban** (not the subject's own ruler). For a subject with no Amban posted, the portrait is hidden and a **Post-Amban button appears next to it**.
- [ ] **B17 — the three "Overseer" toggles now do something.** They should be a **tribute-size selector (S / M / L)** — Small/Medium/Large. Setting one costs 25 influence, marks the active tier (checkmark), and changes the subject's loyalty toward you; a quarterly gold tribute is then collected (2% / 5% / 9% of the subject's income). Only one tier active at a time.
- [ ] **B23 — Tibet "Incorporate Protectorate" costs Legitimacy, not Prestige** (check the button tooltip / cost).

---

## E. Other GUI overflow fixes

- [ ] **B11 — the Dynastic Match window footer text** ("No eligible house…" / hints) no longer spills off the left/right edges.
- [ ] **B13 — the marriage window header shows "Our House: Aisin Gioro"** (the family NAME), not a raw id like "20088".
- [ ] **B20 — the Great Game tab description text** ("The throne's dashboard…") no longer spills off the right edge.

---

## Notes / known-deferred
- **B3** (George III listed) was historically correct for 1763 — addressed via the B1/B2 trait fix, not a separate bug.
- **B24 width** (Chancellor/Regent boxes → 2/3 of row) intentionally left; revisit if the full-width layout still reads badly in-game.
- game.log may show many `provNNNNN has no area assigned to it` — that's a separate map-data integrity note, out of scope here.

If B21/B22 still fail after this build, that's the signal the `prev.prev` placement idiom is also not honoured for these units and we go back to the oracle for a different approach (e.g. post-creation relocation).
