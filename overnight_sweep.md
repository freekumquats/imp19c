# Overnight Sweep — 1763 Trade-Good & Building Seeding (#228–#231)

Autonomous implementation of research-driven 1763 seeding. China at full historical
fidelity; rest of world at good-enough abstraction. Reviewed increments; push before boot-test.
All commits authored freekumquats.

Research target lives in memory: imp19c-china-1763-seeding-program, imp19c-1763-row-seeding,
imp19c-1763-seeding-corrections, imp19c-china-granularity-rule.

## Baseline (audit, branch merge-overnight)
- 57 trade goods, all neutral (local_monthly_food=0.07, no country{} — #219 flood fix intact).
- Province trade_goods tally: porcelain=1 (Jingdezhen P7397), saltpetre=0 static (dynamic block only),
  coal=151 (~1 in China), rifles=16+1.
- NO static buildings= blocks in setup/provinces. Seeding via game-start add_building_level effects
  (se_QING_BUILDINGS.txt ~37 bldgs, se_ROW_BUILDINGS.txt data-driven, granaries×5, Macau×1).

---

## CHANGELOG

### #228 — Trade goods seeded statically + saltpetre geography corrected (DONE, commit pending)

Static province `trade_goods=` assignments (setup/provinces/*.txt). Only abundant/food-neutral
goods (grain/peanut, or anachronistic tea in Bihar) converted; never clobbered silk/tea/cotton
that feed the seeded Qing workshops. All three goods confirmed present in injector rosters
(zz_tradegood_injector.txt etc.) so they feed the trade/production sim (no silent-drop).

**PORCELAIN** (was 1 province → now 3):
- Jingdezhen (Jiangxi P7397) — unchanged, dominant.
- Anxi/Quanzhou pref (Fujian P3302): peanut → porcelain [Dehua blanc-de-chine region].
- Foshan (Guangdong P9301): grain → porcelain [Shiwan export kilns].

**SALTPETRE** (was 0 static / dynamic-only → now 11 static, India-dominant):
- India Bihar (00_Bahar.txt): Chhapra/Saran P1571 (tea→), Gaya P580, Sasaram P532, Bhagalpur P4014,
  Sahibganj P1593, Dumka P6577 — 6 provinces, the DOMINANT world source.
- China SW-karst belt: Guangxi Xuancun P246 / Chongzuo P878 / Rong'an P899; Guizhou Weng'an P2745 /
  Zunyi P3566 — 5 provinces. CORRECTS the old N.China-plain geography (Zigong Sichuan salt-well
  deliberately AVOIDED — that's NaCl, not niter).

**COAL** (China had ~1 → now Shanxi cluster): Dai P542, Wutai P2407 (grain→coal). +existing 3.

**REMOVED**: dynamic `saltpetre_seeded` block in common/on_action/economy/oa_economy_setup.txt
(L218-246) — wrong regions (Bengal_region/Zhili/Shandong/Shanxi), replaced by comment pointing to
static placement. No dynamic saltpetre seeding remains.

Files: 00_Bahar, 00_Fujian, 00_Guangdong, 00_Guangxi, 00_Guizhou, 00_Shanxi, oa_economy_setup.txt.
All brace-balanced; BOM/LF preserved.
COMMIT: 42bf98df0

### #229 — Qing buildings expanded to 1763 reality (DONE, commit pending)

Extended SE_qing_starting_buildings in common/scripted_effects/se_QING_BUILDINGS.txt using the
existing self-guarding macros (QING_seed_building / _works_building / _frontier_building — all
skip+log if not CHI/subject-owned or already present, so liberal seeding is safe). All 31 referenced
building keys confirmed defined; braces 178/178. Research target from memory + 6 teammate research
slices, all anachronism-flagged.

ADDED (net-new seeds beyond the original ~37):
- **Porcelain kilns**: Dehua/Anxi (P3302), Foshan/Shiwan (P9301) — beyond Jingdezhen.
- **Banner garrisons** (was 5 → 15): +Beijing, Jiangning, Chengdu, Ningxia, Liangzhou, Taiyuan,
  Kaifeng, Dezhou (interior) + Shengjing, Jilin, Heilongjiang/Qiqihar, Ili/Huiyuan (frontier seats;
  Ili flagged "est. 1763, under construction").
- **Green Standard posts** (new building): 18 provincial capitals.
- **Yamen** (new): 18 provincial capitals (Baoding=Zhili cap, NOT Beijing; frontier excluded).
- **Exam halls** (was 4 → 16): +12 provincial capitals. NO Anhui hall (Jiangnan/Nanjing served
  both) or Gansu/Lanzhou hall (1875 anachronism; Xi'an served Shaan-Gan).
- **Shuyuan** (new): Yuelu (Changsha P2793), White Deer Grotto (Nankang/Lushan P2386).
- **Confucian temple**: +Qufu (P9041, Jining) as the San Kong anchor.
- **Gelug monasteries** (new): Lhasa, Shigatse/Tashilhunpo, Xining/Kumbum, Labrang, Beijing/Yonghegong.
  Chengde 外八廟 — only Puning (1755) pre-1763; rest (1766-80) deliberately NOT seeded.
- **Great mosques** (new): Xi'an Great Mosque, Kashgar Id Kah.
- **Customs houses** (new): all four 1685 海關 (Canton/Xiamen/Ningbo/Shanghai); Canton = sole legal
  Western port post-1757 but others kept for domestic trade (not deleted).
- **Guild halls** (new): Beijing, Suzhou, Hankou, Canton.
- **Provincial mints** (new): 8 provincial 寶X局 (Yunnan copper-hub heavy) + existing Beijing central.
- **Tribute depots** (new): Huai'an (漕運總督 seat), Jining.
- **Grand Canal control works** (new): Huai'an/Qingjiangpu junction.
- **River conservancy**: +Jining (東河總督, officeholder attested Nov 1763).
- **Sea wall**: Haining 海塘 (P3504, Qianlong toured 1762) via dike building.
- **Great Wall passes** (new, legacy-only): Shanhaiguan, Juyongguan.
- **Horse pastures**: +Mulan Weichang (P9356 Rehe), +Chahar imperial herds (P9529 Xilin Gol).

FIXED (anachronism REMOVAL, not addition):
- **Draft bank**: removed the Taiyuan 票號 piaohao seed (Shanxi piaohao = ~1823, 60yr anachronism);
  reflavoured onto Jiangnan qianzhuang 錢莊 (Shanghai 1736 / Ningbo / Suzhou) — the period-correct
  native money-shop.

Anachronisms deliberately EXCLUDED at 1763 (left mechanic/event-gated): coastal batteries (19th-c.;
at most 1 Humen later), likin stations (1853), imperial bank/telegraph/steel/machine works, treaty
ports/concessions/embassies, Chengde temples 1766-80, Xuehaitang academy (1824), dense Turpan karez
(1842). Existing karez seed at Turpan left as-is (pre-existing #190 decision, minor).
COMMIT: 37298b1cc

### #230/#231 — ROW (non-Qing) buildings: naval dockyards + arsenals (DONE, commit pending)

common/scripted_effects/se_ROW_BUILDINGS.txt. The existing data-driven every_country sweep
(1 manufactory + 1 plantation per substantial non-Chinese realm) ALREADY covers #230 manufacturing
at the good-enough-abstraction level the granularity rule prescribes — left as-is. Added the
missing piece: the genuine large "works" of 1763 (naval dockyards + royal arsenals), which serves
#231 (non-manufacturing) and the arms-works angle of #230.

Added new macro ROW_seed_row_arsenal (owner-agnostic: exists + city-status + not-present; seeds
generic arsenal_building, whose allow-gate add_building_level bypasses). 10 HIGH-confidence sites:
- Britain: Portsmouth (P5294), Chatham/Medway (P9936), Woolwich/London (P3388)
- France: Brest (P5582), Toulon (P8110)
- Russia: Kronstadt/St Petersburg (P3174), Tula arms (P7891)
- Spain: Ferrol (P6142); Venice: Venetian Arsenal (P1135); Ottoman: Istanbul Tersane-i Amire (P7709)

EXCLUDED as anachronistic/unverified: Saint-Étienne (state manufactory 1764); low-confidence
Rochefort/Lorient/Cadiz/Cartagena/Arkhangelsk/Boston/Spandau (abstraction layer doesn't need them).
Braces 51/51; owner-agnostic guard is safe (skip+log if no city).
COMMIT: 93604cc19

### Follow-on fix — Wuyishan latent tea-works skip (found in self-review)

Self-review (good-guard vs current-good cross-check) surfaced a PRE-EXISTING latent bug: P3317
Wuyishan carried trade_goods="peanut", but the shipped qing_tea_workshop_building seed guards on
G=tea — so the Wuyi/Bohea tea works (the single most iconic Qing export-tea centre) has been
silently SKIPPING at every game start. Not caused by my edits (peanut confirmed at HEAD~4). Fixed
P3317 peanut->tea so the seed activates. setup/provinces/00_Fujian.txt, braces 146/146.

---

## SUMMARY
All four tasks (#228-#231) implemented, self-reviewed, committed. Review checks passed: no
duplicate (P,building) seeds; grain supply preserved per region; all 68 seeded province IDs exist;
all good-guarded seeds match current goods (after Wuyishan fix). Anachronisms held out per research.
Commits: 42bf98df0 (#228), 37298b1cc (#229), 93604cc19 (#230/#231), + Wuyishan follow-on.
