# Design: BT-I / BT-J / BT-K — full historical populate of empty map regions (1763)

Status: DESIGN / for review. No map edits by this document.
Approach: FULL BUILD (user decision 2026-07-20) — create the strong tags per continent, not
just culture-only fill. Supersedes the earlier "staged, DIN-first" plan.
Source research (already saved, drives every placement): RESEARCH_NATIVE_AMERICA_1763.md,
RESEARCH_AFRICA_1763.md, RESEARCH_OCEANIA_1763.md.

---

## 0. The hard constraint (governs the entire build)

Every new tag is an ownerless-capital HARD CRASH risk. The proven crash class
([[imp19c-ownerless-capital-crash-rule]]): a tag whose `capital` province is not inside its own
`own_control_core` crashes the game at gamestate construction. So the invariant for EVERY tag
added here is:

> **capital ∈ own_control_core, and every province is owned by exactly one tag (no double-owned,
> no ownerless-capital).**

Native tags in this mod are RULERLESS TRIBES (DIN/APA pattern: `government = federated_tribe`,
`primary_culture`, `religion`, `capital`, `own_control_core` — NO `set_as_ruler` /
`create_character`). This is the template to clone, and it means **no setup char-id contiguity
concern** (the [[imp19c-setup-char-id-rule]] only bites when a tag seeds characters). Keep the
new tags rulerless unless a specific polity needs a named ruler.

A new tag = THREE edits, in this order:
1. `setup/countries/countries.txt` — register `TAG = "setup/countries/<region>/<name>.txt"`.
2. `setup/countries/<region>/<name>.txt` — a country file (color/color2, ship_names optional).
   NOTE: these files carry a BOM in `common/`-adjacent trees, but `setup/countries/*` is read by
   the same reader as other setup — match the existing sibling files' BOM state exactly (verify
   per file; do NOT assume). See [[imp19c-setup-reader-rejects-bom]] for the setup/ BOM hazard.
3. `setup/main/00_default.txt` — the setup block (government/culture/religion/capital/cores).

Cultures: many needed cultures already exist (cree, comanche, cherokee, zulu, xhosa, maori,
aboriginal, papuan, sakalava, hausa — confirmed present). Several are MISSING and must be added
to `common/cultures/` first (blackfoot, lakota, dakota, ashanti, oyo, dahomey, buganda, lunda,
ethiopian, fijian, tongan, samoan — confirmed missing). A tag referencing a non-existent culture
is a load error, so **culture-add precedes tag-add**.

---

## 1. Build method — small verified batches, never one big pass

The #1 failure mode is a single ownerless capital among dozens crashing the boot with no clue
which tag. So:

- **Batch size: 5–8 tags per commit**, each batch its own boot test before the next.
- After each batch, run the mechanical invariant check (script below) BEFORE commit:
  0 ownerless capitals, 0 double-owned provinces, every new tag's capital ∈ its cores, every
  referenced culture/religion exists.
- Province IDs come from `map_data/areas.txt` / `definition.csv` — every province assigned to a
  new tag must currently be UNOWNED (or owned by an emptied inert tag we are reclaiming), never
  stolen from a live tag. Confirm current ownership before reassigning.
- Log what each batch consumed so coverage is auditable (which province ranges → which tag).

### Pre-commit invariant check (run every batch)
```
# ownerless capitals: every tag's capital must appear in its own own_control_core
# double-owned: no province id in two tags' own_control_core
# (implement as a python pass over the setup block after edits; brace-balance + BOM check too)
```
This is a gate, not a formality — a batch does not commit until it passes.

---

## 2. BT-I — North America (audit + fill the empty west)

Research verdict: **6/7 existing Native tags are correct**; only **DIN/Navajo is misplaced**
(currently W. Canada, belongs in SW Four Corners AZ/NM/UT/CO). Plus the west is empty.

### I-0 (do first, standalone): relocate DIN/Navajo
Move DIN's capital + cores from the W. Canada provinces to the Four Corners. This is an
existing-tag move (no new capital creation) — lowest risk, do as its own commit + boot before
any new tags. The W. Canada provinces DIN vacates become fill targets for I-1 (Dene/Cree/BC coast).

### I-1..I-n: new tags to fill the empty west (from research TIER 1 → TIER 3)
TIER 1 (strong, do first): Blackfoot Confederacy (S Alberta/N Montana), Cree (Prairies/boreal —
culture exists), Dene/Chipewyan (Subarctic/Mackenzie), Coast Salish (S BC/Puget Sound), Comanche
(Comanchería S Plains — culture exists), Lakota/Dakota Sioux (upper Missouri/Dakotas).
TIER 2: Tlingit, Haida, Mandan, Pawnee, Haudenosaunee/Iroquois Six Nations, Cherokee (culture exists).
TIER 3: Assiniboine, Tsimshian, Nez Perce, Shoshone bands, Crow, Ute, Osage, Kwakwakaʼwakw,
Dakelh, Hidatsa, Cheyenne, Arapaho, Shawnee.
Cultures to ADD before their tags: blackfoot, lakota, dakota (others exist or map to existing groups).
1763 context to honor: Royal Proclamation line, Pontiac's War actors (C3F/Shawnee/Miami) — keep
the eastern woodland tags consistent with the war already in the timeline.

## 3. BT-J — Africa (largest batch count; centralization tiers)

Research splits by authority level — this maps directly to tag strength / government type:
- **Centralized → strong tags** (do as full tags): Ashanti, Oyo, Dahomey, Buganda, Lunda, Luba,
  Ethiopia (Gondarine), Morocco (Alaouite), Rozvi, Bamana/Ségou, Darfur, Funj/Sennar, Kong,
  Benin, Kanem-Bornu.
- **Decentralized/confederal → reduced-authority tags**: Hausa city-states (Kano/Katsina/Zaria/
  Gobir — culture exists), Kongo, Loango, Futa Jallon, Imerina, Sakalava (culture exists), Burundi.
- **Stateless → CULTURE/POPULATION only, NO central tag**: Khoikhoi, San, pre-Mfecane Nguni
  (Xhosa/Zulu — cultures exist), pre-Mfecane Sotho-Tswana. These get province culture assignment,
  not a country — zero ownerless-capital risk, do them in a dedicated culture-only batch.
Cultures to ADD before tags: ashanti, oyo, dahomey, buganda, lunda, ethiopian (+ others per the
strong-tag list); reuse hausa, sakalava, nguni where present.
Existing footprint: North Africa (Morocco + Ottoman regencies Algiers/Tunis/Tripoli + Ottoman
Egypt) and the Swahili-coast-under-Oman may already have tags — AUDIT before adding, don't dup.
CAUTION: Africa is where the crash risk concentrates (most new tags) — keep batches to 5–8 and
boot each.

## 4. BT-K — Oceania (mostly culture-only; NZ is the tag work)

Research is explicit about which get tags vs. cultures:
- **Australia → CULTURES only, non-state** (Pama-Nyungan zones SE/interior/SW, non-PN north,
  Tasmanian Palawa). Province culture + population, NO tags. Zero crash risk. Cultures mostly
  exist (aboriginal present); add zone-specific ones only if the research demands granularity.
- **New Guinea → CULTURES only, non-state** (Highland/Sepik/S-Papuan/coastal/West-Papuan). papuan
  culture exists. Culture + population fill, no tags.
- **New Zealand → iwi TAGS** (one Māori culture, which EXISTS): North I. — Ngāpuhi, Ngāti Porou,
  Ngāti Kahungunu, Waikato/Tainui, Ngāti Tūwharetoa, Tūhoe, Ngāti Maniapoto, Te Atiawa;
  South I. — Ngāi Tahu (dominant), Kāti Māmoe/Waitaha (absorbed). This is the real tag batch for K.
- **Nearby islands → tags where hierarchical**: Fiji (Bau/Rewa — culture MISSING, add), Tonga
  (Tuʻi Kanokupolu — culture MISSING, add), Samoa (culture MISSING, add). Vanuatu/New Caledonia/
  Solomons → Melanesian cultures only, no tags.

---

## 5. Execution order (batches, each = commit + boot)

1. **I-0** DIN/Navajo relocation (existing-tag move) — commit + boot alone.
2. **Culture pre-adds** — one commit adding all MISSING cultures needed by upcoming tag batches
   (blackfoot/lakota/dakota; ashanti/oyo/dahomey/buganda/lunda/ethiopian; fijian/tongan/samoan).
   Cultures are low crash-risk (a bad culture is a load error, not a construction crash) but
   MUST precede any tag that references them. Boot to confirm clean load.
3. **BT-I TIER 1** (6 tags) → boot. **BT-I TIER 2** (6) → boot. **BT-I TIER 3** as wanted.
4. **BT-J centralized strong tags**, in 5–8-tag batches (West Africa → Central → East → NE/Sahel
   → North-Africa-audit-then-fill), each booted. Then **BT-J decentralized tags** batch(es).
   Then **BT-J stateless culture-only** batch (no crash risk).
5. **BT-K NZ iwi tags** (+ Fiji/Tonga/Samoa) as one-to-two batches → boot. Then **BT-K Australia +
   New Guinea culture-only** fill (no crash risk).
6. Final full-map invariant sweep (0 ownerless capitals, 0 double-owned) + a clean boot.

## 6. Non-goals / cautions

- Do NOT assign provinces currently owned by a LIVE tag to a new one (only unowned / emptied-inert).
- Do NOT give a stateless people a central tag (research is explicit: Khoikhoi/San/Aboriginal/
  Papuan = culture+pop, no country).
- Do NOT create rulers/characters for these tribal tags (rulerless, per DIN pattern) unless a
  specific centralized African polity warrants a named sovereign — and if so, add its char at
  global max id+1 ([[imp19c-setup-char-id-rule]]).
- Keep each new country file's BOM state matching its setup/countries siblings; verify per file.
- This is 1763-start data ([[imp19c-1763-border-audit-done]]) — placements must be plausible for
  1763, not 1815 or the classical base.
