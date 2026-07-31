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
