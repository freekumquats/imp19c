# Boot-test master list — merge-overnight + manufactured_goods (2026-07-29)

Consolidated findings from BOTH branch boot tests. Legend:
DONE = fixed+pushed | OPEN = to fix | RESEARCH = under investigation |
DIVERGE = fix exists on the other branch, resolved by merging MG→MO | NOTABUG | NOISE = pre-existing baseline

Target of the fix pass (user directive): **merge manufactured_goods → merge-overnight, then fix all OPEN bugs on merge-overnight.**

## A. merge-overnight boot test — reported/visual
| task | id | status | note |
|---|---|---|---|
| baseline boot, no crash | #164 | DONE-verified | booted+ran ~14min |
| nobles desired-ratio icons render | #165 | OPEN(verify) | boot-visual |
| strata happiness modifier loc | #166 | OPEN(verify) | MO#3 fix present on MO |
| building tooltip WIP stub gone | #167 | OPEN(verify) | |
| 14 mission trees deep/narrow | #168 | OPEN(verify) | shape good per #159 |
| invention icons subject motifs | #169 | OPEN(verify) | |
| Titles Unassigned alert turn 1 | #170 | OPEN(verify) | #156 fix present |
| **Employment/Industrialization law sections NOT visible** | #178 | **OPEN BUG** | wrong GUI container (empty flowcontainer) |
| Local Indentured Output placeholder icon | #176 | OPEN | |
| deities missing Apotheosis Effects + loc | #180 | OPEN | genuine, audit false-negatived it |
| deity text literal `<i>` tags | #181 | OPEN | unsupported markup |
| cultural decisions loc (self_determination/language_recognition/language_standardization) | #182 | OPEN | +missing desc on first two |
| mission NODE graphics too large / overlapping | #183 | OPEN | size per TI/Invictus |

## B. merge-overnight boot log
| finding | id | status |
|---|---|---|
| gradient_black_flip flood gone | #174 | DONE-verified (0x, was 8565) |
| undefined-trigger spam (IND_/URB_/id) gone | #173 | DONE-verified (0x) |
| parse-token noise (is_triggered_only/secondary) | #175 | NOTABUG (baseline) |
| culture_additional_names_l_english.yml malformed (34 parse errors) | #184 | OPEN |
| octere naval subunit invalid (hinduism apotheosis) | #185 | OPEN (pre-existing) |

## C. manufactured_goods boot test — reported/visual
| finding | id | status |
|---|---|---|
| local_[class]_happyness modifiers missing loc | #186 | OPEN (DIVERGE: MO#3 loc only on MO) |
| regular_infantry_defensive/offensive (+MG-3 cluster) missing loc | #187 | OPEN |
| loyalty_qing_estranged missing loc | #189 | OPEN |
| **Qing frontier garrisons (Shengjing/Liangzhou/Heilongjiang/Urumqi/Tibet) losing food + attrition** | #190 | **RESEARCH** (garrisons shouldn't starve; subject-supply unclear) |
| Impeach the Venal doesn't remove vanilla Minister of Defence from office | #191 | OPEN |
| TRH tag "Trịnh Lords"→"Tonkin" | (n/a) | DONE-pushed e8f5d5dfa (MG) |

## D. manufactured_goods boot log — genuine new
| finding | id | status |
|---|---|---|
| INCOME_*__modifier double-underscore, remove_country_modifier can't find (28x each) | #192 | OPEN |
| is_ideology_religion at CHARACTER scope, character_events.txt:516 (192x) | #193 | OPEN |
| industrial-goods buttons missing *_add/remove_button_tt loc | #194 | OPEN |
| add_trait target null, setup/characters/00_North America.txt:664 | #195 | OPEN |
| pre-existing baseline noise (econ floods, stub-unit modifiers, vanilla-leftover db refs) | #196 | NOISE |

## E. Cross-cutting
| finding | id | status |
|---|---|---|
| Loc-coverage audit (script every referenced key vs loc) | #188 | OPEN (root-cause for #166/#176/#177/#180-loc/#182/#186/#187/#189/#194) |
| Branch divergence: MG trade-goods loc (#147) + modifiers (#148) not on MO | #177/#179 | resolved by MG→MO merge |

## Fix order on merge-overnight (after MG→MO merge lands the trade-goods/loc/galvanism/Tonkin work)
1. #178 laws GUI container (move areas into populated container) — CONFIRMED bug, high visibility
2. #193 is_ideology_religion scope (192x flood, one-line scope wrap)
3. #192 INCOME_*__modifier empty-param
4. #195 add_trait null at setup char
5. Loc sweep #188 (covers #166/#176-loc/#180-loc/#182/#186/#187/#189/#194) + #184 malformed yml
6. #180/#181 deities (apotheosis effects + `<i>` markup)
7. #183 mission node size (per TI/Invictus)
8. #185 octere subunit; #191 impeach vanilla-office removal
9. #190 garrison food — after research (#190 RESEARCH agent)
