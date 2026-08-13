# Research: Yunnan/Burma frontier (Kokang area) — 1815 borders inherited uncritically into the 1763 start

Task #47 (overnight backlog). Diagnosis only — no code changed. Digest per imp19c-research-digest-location-rule.

## Summary

No province, country tag, or loc string in the repo ever names "Kokang" — the term doesn't appear anywhere in `setup/`, `common/`, or `localization/`. The user's pointer to "the current map/borders near Kokang" is best read as: the Yunnan–Burma frontier (the Kokang region sits exactly on it, in the hills northeast of Kengtung/Lashio) inherited its `own_control_core` from the mod's 1815 base and was never checked for 1763 accuracy — unlike neighbouring Yunnan/Xinjiang/Tibet frontier work, which got a dedicated 1763 pass (`RESEARCH_QING_FRONTIER_GARRISONS_1763.md`, `RESEARCH_QING_XINJIANG_GARRISONS_1763.md`).

**Verified finding: BUR's core includes the entire Arakan (Rakhine) coast, historically wrong for 1763.**

`setup/main/00_default.txt:44368` — BUR's `own_control_core` includes province `30` (Akyab, `setup/provinces/00_Bay_of_Bengal.txt:1`, the historic seat of Arakan/Mrauk-U) plus the rest of the Bay-of-Bengal coastal cluster (`40 Shwegyin, 651 Kyonkpyoo, 1696 Thandwe, 3452 Satthwa, 5667 Buthidaung, 6627 Toungup, 8377 Bassein` — all Arakan/Rakhine-coast settlements) — 68 provinces total.

Historically, **Arakan (the Mrauk-U kingdom) was still independent in 1763** and was not conquered by Konbaung Burma until **1785**, under Bodawpaya — more than 20 years after this mod's start date, and outside even the Sino-Burmese War window (1765-69) the mod's own research already correctly dates. The existing project research doc itself contains the contradiction: `1763_WORLD_EAsia_SEAsia.md:243` lists "Arakan" as 1763 Burmese "Territory," but the SAME document's own "Delta vs 1815" note four lines below (`:271`) says Konbaung's "peak territorial extent (Arakan, Assam, Manipur, Tenasserim)" belongs to **Bodawpaya (r. 1782-1819)** — i.e. the doc's own delta analysis already flags Arakan as a later acquisition, but its "1763 Territory" line was never corrected to match. The setup file inherited the uncorrected line.

`1763_DELTA_Asia.md:355` (the pre-existing 1763-conversion checklist) explicitly flagged this exact risk and was never acted on:
> "**Provinces** (line 43677-43682): Verify 1763 Konbaung extent (just unified Burma 1757, expanding; 1815 = peak extent, **may need to trim Arakan/Assam/Manipur if added by 1815**)."

That checklist item is still open. No trim was ever applied — `own_control_core` for BUR is unchanged from the 1815 base map.

**Manipur/Assam**: not actually a problem — checked and BUR's core does NOT extend to Manipur or Assam-proper (no Meitei/Assamese-culture provinces appear in BUR's 68-province core; the "assamese" culture hits are all in `00_Bengal_region.txt`/`00_Eastern_Himalayas.txt`, outside BUR). Manipur was a Burmese vassal claim by 1815 but the mod never modeled a Manipur entity or gave BUR any Manipur-area cores, so there's nothing to trim there. The Delta checklist's caution about Manipur was pre-emptive and turned out not to apply to this map.

## Kokang / Shan-states cluster itself: correctly modeled, not the bug

Checked the actual Kokang-adjacent Shan sub-states (`setup/main/00_default.txt:44380-44632`): `HSI` (Hsipaw), `LSU` (Lisu), `MMT` (Mongmit), `MPN` (Mongpan), `MKN` (Mongkung), `KTG` (Kengtung), `CHH`, `MLM` (Mong Lem), `TNI` (Theinni) — each a tiny 1-6 province `absolute_kingdom`/`absolute_duchy`, all correctly dependency'd as `BUR` client_states (`:917-920`, plus `KTG` at `:915`). This matches the actual history reasonably well: the Shan states were under loose Burmese/Ava suzerainty from the Toungoo era onward, well before 1763, so their subordinate status is not anachronistic. **No overlap or gap was found between CHI's Yunnan core (614 provinces) and BUR/Shan-state cores** — verified programmatically (brace-depth province-set extraction, zero intersection).

BUR's ruler is unauthored (no character file references BUR; matches the "no ruler authored (engine-generated)" pattern the Delta doc flags for other tags it never got to). `1763_DELTA_Asia.md:347` names the correct 1763 ruler — **Hsinbyushin** (r. 1763-1776, acceded Jan 1763, son of Alaungpaya) — but this was never authored either. A second open item from the same checklist.

## Recommendation (not actioned this task — scope decision)

Two genuinely open 1763-accuracy gaps on Burma, both flagged years ago in `1763_DELTA_Asia.md` and never closed:
1. **Territorial**: strip the Arakan/Rakhine coastal cluster (province 30 + ~7-10 sibling provinces) out of BUR's `own_control_core` and either (a) leave them unowned frontier (matches the mod's existing "revert to unowned frontier" idiom for other anachronistic 1815-only holdings, e.g. NSW/QNG per the `own_control_core` emptying precedent at `:34455`), or (b) stand up a minimal Arakan/`ARK` tag as an independent `absolute_kingdom` (Mrauk-U was still a real, if declining, polity in 1763 — an authored tag is more historically legible than unowned frontier for a kingdom that existed).
2. **Character**: author Hsinbyushin as BUR's ruler (birth 1736, acceded Jan 1763, aggressive-expansionist military traits per the existing Delta doc's own character-creation notes).

Both are real fixes, but they are a **territorial remap + new-entity decision**, not a bugfix-in-place — option (a) vs (b) above is a genuine design call outside what "investigate the border" asked for. Logged as follow-up task #56 rather than actioned inline, per the no-scope-expansion discipline (same pattern as #54's INCOME_sell_reserves finding during #23).
