# Design Plan — Bakumatsu → Boshin → Meiji: Japan 1815–1868

**Status:** proposed (design only; no code written)
**Feature id:** #94 (Japan domestic arc) + #81-refactor (invert Qing pre-Perry coupling)
**Author scope:** net-new Japan subsystem that OWNS the bakumatsu→Boshin arc, its state, and its
climactic civil war; the existing Qing #81 pre-Perry content is refactored to HOOK INTO this.

---

## 0. Guiding principle — coupling direction (per user directive)

> "Qing content should hook into existing US and Japan content, not the other way around."

**The Japan subsystem is the source of truth.** It owns:
- the domestic legitimacy state (on the Tokugawa tag `TKG` and the daimyo tags),
- the per-domain sabaku↔sonnō alignment,
- the Perry shock and every downstream beat, run AI-autonomously,
- the Satchō Alliance bond and the Boshin War (fought on the map),
- the canonical "Perry has come / the Restoration has happened" signals.

**The Qing #81 arc becomes a consumer.** After this build, the Qing's pre-Perry meddling is an
*optional overlay input* that biases Japan's meters; and the Qing's post-Perry Japan mission tree
listens for Japan-side signals. #81's own CHI-side content (Nagasaki intel, the Opium-War
cautionary tale) stays as-is; what changes is that Japan's fate no longer lives on CHI variables.

**AI-autonomous by construction.** The player is almost always the Qing, so the whole arc must
reach Meiji ≈1868 with Japan under AI control. Everything decisive is pulse-driven or in event
`immediate` blocks; player options only modulate.

---

## 1. Historical spine (sourced digest)

Historiography: Jansen, *The Making of Modern Japan* (2000); Totman, *The Collapse of the
Tokugawa Bakufu* (1980); Beasley, *The Meiji Restoration* (1972); Craig, *Chōshū in the Meiji
Restoration* (1961); Wilson, *Patriots and Redeemers in Japan* (1992); Wakabayashi, *Anti-
Foreignism and Western Learning* (1986).

**Structural strain (1815–1853).** The *bakuhan* system froze the 1600 Sekigahara settlement:
the Tokugawa *bakufu* (~4M koku + the great cities, mines, foreign-relations monopoly) over ~260
*han* sorted into *shinpan* (collateral houses), *fudai* (hereditary vassals, office-eligible),
and *tozama* (outside lords held at the periphery — Satsuma, Chōshū, Tosa, Hizen). The tozama had
the grievance, the distance, and the coastal exposure. *Sakoku* seclusion coexisted with *rangaku*
(the Nagasaki Dutch pipe). The **Tenpō crisis (1833–37)** — famine, the **Ōshio rising (1837)** —
and failed **Tenpō Reforms (1841–43)** exposed fiscal decay; **Opium War (1839–42)** news via the
Nagasaki *fūsetsugaki* softened the 1825 expel-vessels edict to the 1842 provide-water edict.

| Date | Beat | Meter effect |
|---|---|---|
| Jul 1853 / 1854 | **Perry** (Uraga → Convention of Kanagawa) | legitimacy − ; foreign pressure spikes |
| 1858 | **Harris Treaty** signed by tairō **Ii Naosuke** *without* imperial sanction; **Kōmei refuses** | legitimacy −− ; imperial prestige + (Kyoto becomes a rival power) |
| 1858–60 | **Ansei Purge** (Ii executes Yoshida Shōin et al.) → **Sakuradamon** (Ii assassinated, Mar 1860) | legitimacy −− ; sonnō + across domains |
| 1862–63 | **Namamugi Incident** → **Anglo-Satsuma War / Kagoshima bombardment** | Satsuma sonnō + ; Satsuma converts to Western arms |
| 1863–64 | **Shimonoseki bombardments**; Chōshū's failed Kinmon coup; **First Chōshū Expedition** | Chōshū sonnō + |
| 1866 | **Second Chōshū Expedition collapses**; **Satchō Alliance** (brokered by Sakamoto Ryōma) | legitimacy −−− (bakufu can't beat one domain); Satchō bond forms |
| Nov 1867 | **Taisei hōkan** (Yoshinobu returns rule to the throne) | imperial prestige +++ |
| 3 Jan 1868 | **Ōsei fukko** coup (shogunate abolished) | legitimacy floor |
| Jan 1868–Jun 1869 | **Boshin War**: Toba-Fushimi → Edo surrender (Katsu ↔ Saigō) → Ōuetsu Reppan Dōmei / Aizu → Hakodate/Ezo | the climax |

**Structural drivers to model:** shogunate legitimacy vs imperial/court prestige (a zero-sum
transfer that Kanagawa/Harris/Kōmei's refusal set in motion); per-domain sabaku↔sonnō alignment
(the great tozama flip to sonnō, Aizu/fudai hold sabaku); foreign pressure/treaty humiliation;
modernization vs seclusion (the jōi radicals become the modernizers after Kagoshima/Shimonoseki).

**Characters** (attach to their domain tags; add to `setup/characters/00_Japan.txt` as dated
historicals, promote at the beat): **Tokugawa Yoshinobu** (TKG, last shogun), **Ii Naosuke** (TKG,
tairō, dies 1860), **Emperor Kōmei** / **Emperor Meiji** (the Court — see §7.5), **Saigō
Takamori** & **Ōkubo Toshimichi** (SHZ), **Kido Takayoshi** & **Yoshida Shōin** (CSU), **Sakamoto
Ryōma** (YCH/Tosa), **Shimazu Hisamitsu** (SHZ, kōbu-gattai moderate), **Katsu Kaishū** (TKG navy).

---

## 2. Existing mod assets & the critical AI gap

### 2.1 Japan tags at 1815 (verified)
**No unified JPN tag exists at start.** Japan is **TKG (Tokugawa Shogunate)** + ~37 daimyo subject
countries wired at `setup/main/00_default.txt:557–593` as
`dependency = { first = TKG  second = <TAG>  subject_type = ... }`. Relevant playable domains:
**CSU** = Chōshū, **SHZ** = Shimazu/Satsuma (both `nominal_vassal`); **YCH** = Tosa (Yamauchi);
**SGA** = Saga/Hizen; **AZU** = Aizu (`semi_autonomous_governorship` — the tighter shinpan tie,
historically correct for the pro-bakufu holdouts); **DTE** = Date/Sendai.

`release_subject` (se_QING_VASSAL.txt:110) and `start_civil_war = scope:<char>`
(se_QING_JAPAN_PREPERRY.txt:214) are proven verbs. The post-Perry `qing_japan_missions.txt` has
dormant `exists = c:JPN` fallbacks — a hint that forming JPN at Meiji is the intended terminus.

### 2.2 The #81 pre-Perry chain (what to invert)
- Files: `se_QING_JAPAN_PREPERRY.txt` (`QING_jppre_*`), `qing_japan_preperry_missions.txt`,
  `qing_japan_preperry_events.txt`, `qing_japan_preperry_modifiers.txt`, loc.
- Counters (**on CHI**): `qing_jppre_intel`, `qing_jppre_reform_faction`, `qing_jppre_shogun_grip`
  (starts 70). Hand-off var `qing_jppre_perry_done` (set by `QING_jppre_perry_handoff`).
- `qing_jppre_backed_tag` = `flag:CSU`/`flag:SHZ`; `QING_jppre_resolve_daimyo{ tag }` →
  `scope:qing_jppre_daimyo`; `QING_jppre_spawn_reform_leader`; `QING_jppre_restoration_break`
  (release_subject + start_civil_war — the Boshin analog already sketched).
- Perry scheduled at `qing_mechanics_on_actions.txt:76–79` (`qing_japan_preperry.10`,
  days ≈13820–13940 ≈1853) — but **only `if = { limit = { is_ai = no } }`**.

### 2.3 ⚠️ CRITICAL AI GAP (drives the whole design)
**The entire #81 chain is CHI-human-only and runs no state on the Japanese tags.**
The pre-Perry missions gate `potential = { tag = CHI  is_ai = no }`; the Japan pulse is
`tag = CHI  is_ai = no`; the Perry hand-off is `is_ai = no`; and **all counters live on CHI, not
on TKG/daimyo**. So when the player is the Qing (or nobody plays Japan), *none* of it fires and
Japan has no domestic state at all. **The new subsystem therefore cannot "continue #81's state" —
it must OWN its own state on the Japanese tags** and read #81's CHI variables only as an optional
overlay. This is exactly why the coupling must be inverted.

### 2.4 House idioms to mirror
Counter+band+pulse (`se_QING_DECLINE.txt`, `QING_DECLINE_nudge`); milestone→spawn
(`QING_DECLINE_spawn_sect_leader`); `se_LOG`; `ai_chance = { modifier = { factor = N  <trigger> } }`
on options; and the **all-country autonomous hook**: `yearly_country_pulse`
(`00_yearly_country.txt`) runs its `effect` for *every* country with internal `if/limit` gating —
this is the AI-safe hook (unlike `monthly_country_pulse`'s CHI-self-gated Qing sub-pulse).

---

## 3. File plan

| File | Contents |
|---|---|
| `common/scripted_effects/se_JAPAN_BAKUMATSU.txt` | `JPN_baku_*`; `sys = BAKU`. Meters, bands, autonomous pulse, domain realignment, Perry ingest + overlay read of #81. |
| `common/scripted_effects/se_JAPAN_BOSHIN.txt` | `JPN_boshin_*`; `sys = BOSHIN`. Satchō bond, `JPN_boshin_execute` (release_subject + start_civil_war), war resolution, Meiji end-state. |
| `events/imp19c_mod_events/japan_bakumatsu_events.txt` | namespace `japan_bakumatsu` — dated beats, each `immediate` + `ai_chance` options. |
| `events/imp19c_mod_events/japan_boshin_events.txt` | namespace `japan_boshin` — Toba-Fushimi, Edo surrender, northern war. |
| `common/missions/japan_bakumatsu_missions.txt` | **player-overlay** tree (`potential` gated on `is_ai = no` + `OR{ tag=TKG tag=CSU tag=SHZ … }`); not required for AI progression. |
| `common/modifiers/japan_bakumatsu_modifiers.txt` | band modifiers + reward/opinion modifiers. |
| `common/on_action/japan_bakumatsu_on_actions.txt` | schedules dated beats (all-country, tag-gated, **no is_ai guard**); registers the autonomous pulse on `yearly_country_pulse`. |
| `localization/english/japan_bakumatsu_l_english.yml` | loc. |

---

## 4. Mechanics

### 4.1 Meters (concrete-over-abstract; counters are the summary layer)

**National, stored on TKG** (so they exist for AI Japan — the fix for the #81 gap):
- `baku_legitimacy` (0..100, start **70**) — Tokugawa central authority. Drift: Perry −, Ansei −−,
  Sakuradamon −−, failed Chōshū expeditions −−.
- `imperial_prestige` (0..100, start **20**) — the Kyoto/sonnō pole; rises as legitimacy falls.

**Per-domain `domain_sonno`** (0..100) stored **on each roster daimyo tag** (CSU, SHZ, YCH, SGA,
DTE, AZU) — the sabaku↔sonnō alignment; the genuinely concrete political variable.

**Concrete objects on the bands:**
- `baku_legitimacy` < 40 → crisis events unlock; the shogun's-grip modifier flips to a penalty;
  < 25 arms the Boshin trigger.
- `domain_sonno` ≥ 60 on CSU/SHZ → spawn the domain's real firebrand (**Yoshida Shōin** in CSU,
  **Saigō** in SHZ) via a once-guarded `create_character`; stamp `sonno_committed`; estrange the
  ruler's loyalty toward TKG.
- `domain_sonno` ≥ 55 on **both** CSU and SHZ → the **Satchō Alliance as a concrete diplo bond**.
- `imperial_prestige` ≥ 60 → spawn young **Meiji**; enable the taisei hōkan event.

### 4.2 AI-autonomous driver (the hard requirement)
`japan_bakumatsu_pulse` attached to `yearly_country_pulse`'s effect (all-country), self-gated
`if = { limit = { tag = TKG } }`, **no `is_ai` guard**. It (a) drifts meters toward date-anchored
targets, (b) applies bands, (c) fires the once-guarded concrete spawns, (d) checks the Boshin
arming condition. Because state lives on TKG and the gate is tag-only, the arc advances identically
for AI and human Japan.

**Belt-and-suspenders per beat:** dated scheduled beats (Perry, Ansei, Sakuradamon, bombardments,
Satchō, taisei hōkan, Toba-Fushimi) are seeded from `on_game_initialized` for `tag = TKG` with
**no is_ai guard** and a self-re-checking date+state trigger; each crisis event's decisive
state-change is in `immediate` (fires regardless of option), options only modulate and carry
`ai_chance`.

### 4.3 Boshin climax — in-engine resolution (proven verbs only)
`JPN_boshin_execute` (`sys = BOSHIN`), called from the pulse when armed
(`baku_legitimacy < 30` AND `taisei_hokan_done`, or a **hard date fallback ≥ 1868.1.1**):
1. **Domain realignment:** each roster daimyo picks its side by `domain_sonno` band — sonnō
   (CSU/SHZ/YCH/SGA) go imperial, sabaku (AZU + fudai) hold with TKG.
2. **Release the imperial-side tozama:** `c:TKG = { release_subject = c:CSU }`, `= c:SHZ`, …
   (proven idiom; the on-map break mirroring `QING_jppre_restoration_break`).
3. **Raise the restoration civil war** behind a real commander:
   `c:SHZ = { start_civil_war = scope:saigo }` (fall back to `current_ruler` if Saigō dead, as
   #81 already does) — Saigō being the Toba-Fushimi/Edo commander is historically the right
   instigator.
4. **Northern holdout:** keep AZU (Aizu) + DTE (Sendai) sabaku so the war has a concrete northern
   bloc (Ōuetsu Reppan Dōmei) — no new mechanic, just don't realign them.
5. **Edo surrender flavour:** `japan_boshin.2` spawns Katsu Kaishū (TKG) ↔ Saigō; on the
   historical branch transfers TKG's core relatively peacefully (reduces exhaustion) rather than a
   grinding siege.
6. **Meiji end-state:** on imperial victory (or a timed resolution if the AI war stalls) set
   `meiji_restoration_done`; **form/rename to JPN** (lighting up the dormant `exists = c:JPN`
   fallbacks in `qing_japan_missions.txt`) — see §6/§8.

**AI-advance for the climax:** arming is pulse-checked on TKG regardless of is_ai; steps 2–3 are
scripted-effect (no option gate); the ≥1868 hard fallback forces arming even if drift lagged, so
an AI Japan always reaches the Restoration.

---

## 5. Beat list (date-anchored)

| # | Beat / date | Trigger | Player options (overlay) | Concrete effect | AI advance |
|---|---|---|---|---|---|
| B0 | **Perry, 1853–54** | scheduled ~1853 for TKG (no is_ai) | sign / resist (magnitude) | `baku_legitimacy −8`; set `baku_perry_done` on TKG; **overlay:** if a human Qing ran #81, `JPN_baku_ingest_preperry` reads CHI's `qing_jppre_*` to bias the seed, else historical default | immediate fires; `ai_chance` favours sign |
| B1 | **Ansei/Harris + Kōmei refusal, 1858** | date≥1858, `baku_perry_done` | seek sanction (fails) / sign unilaterally | `baku_legitimacy −12`, `imperial_prestige +10`; spawn **Ii Naosuke** (tairō) | immediate; sign 10 |
| B2 | **Ansei Purge → Sakuradamon, 1858–60** | Ii alive + date≥1860 | purge harder / restraint | kill Ii; `baku_legitimacy −10`; CSU/SHZ `domain_sonno +12` | immediate handles assassination + backlash |
| B3 | **Namamugi → Kagoshima, 1862–63** | date≥1862, `exists c:SHZ` | (reaction) | SHZ `domain_sonno +15` + modernization modifier; spawn Saigō/Ōkubo if band hit | pulse/immediate |
| B4 | **Shimonoseki + Chōshū expeditions, 1863–66** | date≥1863, `exists c:CSU` | (reaction) | CSU `domain_sonno +15`; spawn Yoshida Shōin/Kido; **2nd expedition fails →** `baku_legitimacy −15` | pulse/immediate |
| B5 | **Satchō Alliance, 1866** | both CSU/SHZ `domain_sonno≥55` OR date≥1866 fallback | (reaction) | broker via Sakamoto Ryōma (spawn YCH); form the **concrete alliance bond** + `satcho_pact` marker on both; `imperial_prestige +15`, `baku_legitimacy −10` | meter-gate + date fallback both fire immediate |
| B6 | **Taisei hōkan, Nov 1867** | `imperial_prestige≥55` ∧ `baku_legitimacy<40` OR date≥1867 | resign gracefully / cling | spawn/promote **Meiji**; set `taisei_hokan_done` | `ai_chance` favours resign; flag set regardless |
| B7 | **Boshin War, 1868–69** | `baku_legitimacy<30` ∧ `taisei_hokan_done` OR date≥1868 fallback | — | **§4.3 execute** | pulse fires it; no click |

---

## 6. Refactor of the Qing #81 arc (invert the coupling)

**Today:** all of Japan's fate is simulated on CHI variables and only when a human Qing plays.

**After this build:**
1. **Japan owns its state.** The new `baku_legitimacy`/`imperial_prestige`/`domain_sonno` on the
   Japanese tags are authoritative. #81's CHI-side `qing_jppre_*` counters remain, but only as an
   *input signal*: at B0, `JPN_baku_ingest_preperry` reads them if present to bias the seed (a Qing
   who backed CSU nudges CSU `domain_sonno` up; a Qing who shored the bakufu seeds higher
   `baku_legitimacy`). Absent a human Qing, the seed is historical default.
2. **Perry is scheduled by the Japan arc**, not the CHI-only hook. Move the Perry one-shot into
   `japan_bakumatsu_on_actions.txt` on `tag = TKG` with **no is_ai guard**. The old
   `qing_mechanics_on_actions.txt:76` CHI-only Perry schedule is either removed or repurposed to
   *notify a human Qing* that Perry has come (fire the Qing's pre-Perry hand-off `qing_japan
   _preperry.10` off the Japan-side B0 signal), so #81's CHI narrative still triggers — but now as
   a consumer of Japan's event, not the driver of Japan's fate.
3. **The post-Perry Qing mission tree listens for Japan signals.** `qing_japan_missions.txt` gates
   on `has_variable = qing_jppre_perry_done` today; add readiness to also key off the Japan-side
   `baku_perry_done`/`meiji_restoration_done` (via a small bridge that sets the CHI flag when the
   Japan-side signal fires, for a human Qing). When the Restoration forms JPN, the tree's dormant
   `exists = c:JPN` fallbacks activate naturally.
4. **Keep #81's genuinely Qing content** (Nagasaki intel, fūsetsugaki, Opium-War cautionary tale,
   the Qing's ability to *back* a daimyo) untouched — the Qing backing becomes one of the overlay
   inputs to Japan's `domain_sonno`, satisfying the separatism-backer rule natively (the Qing is a
   plausible neighbouring power; GBR post-Kagoshima is the only other permitted external nudge).

**Scrutiny (CHANGE to shipped #81):** document that Japan's arc now runs AI-side where before it
did nothing; that #81's CHI counters/missions still exist and still respond to a human Qing; and
that the only inversion is *who owns the simulation* (Japan, not CHI).

---

## 7. Unproven engine capabilities — oracle-check before build

1. `yearly_country_pulse` genuinely executes its `effect` for **AI** countries (so a `tag = TKG`
   gate with no is_ai guard runs AI-side). Load-bearing — verify.
2. `start_civil_war` fires correctly for an **AI** country from its own pulse and yields a working
   rebel side (proven syntactically in #81, but only ever with a human Qing acting *on* an AI
   daimyo).
3. `release_subject` from an **AI** overlord (`c:TKG = { release_subject … }` when TKG is AI).
4. Per-pulse variable read/write on non-player AI tags at acceptable cost (only TKG + ~6 domains
   carry state — likely fine; confirm no per-tick scan blows up).
5. **Emperor/Court scope:** Japan has no imperial-court tag at 1815. Recommend the emperor be a
   character *inside TKG* with an `imperial_court` marker (proven, low-risk) rather than a released
   court tag; verify `create_character` + later leadership if JPN is formed.
6. `ai_chance` on standalone `country_event` options reliably steers the AI to the weighted default
   (proven for play events; confirm for these).
7. Alliance/defensive-pact effect scripted between two **AI** tozama (CSU↔SHZ) for the Satchō
   bond; if unsupported, fall back to a shared marker var + coordinated realignment (no hard
   engine dependency).
8. Forming/renaming to **JPN** at Meiji and whether the dormant `qing_japan_missions.txt`
   `exists = c:JPN` guards then behave.

---

## 8. Open questions / scope decisions

1. **Intended player:** build the **autonomous AI arc as baseline** (this plan); the human-overlay
   mission tree covers which domains? (all four Satchō leaders, or just TKG + CSU + SHZ?)
2. **Emperor scope:** character-inside-TKG (recommended) vs dedicated court tag.
3. **Meiji terminus tag:** form **JPN** (recommended — activates the existing Qing post-Perry tree)
   / keep TKG relabelled / leave tozama independent.
4. **Coupling strength:** overlay-only (recommended — Japan self-sufficient, Qing meddling biases
   it) vs. letting a human Qing *prevent* the Restoration (a bigger commitment).
5. **Boshin failure branch:** may a sustained high-`baku_legitimacy` bakufu-modernization path let
   the shogunate *survive* into a Tokugawa-led modern Japan (ahistorical player-agency payoff), or
   is Meiji the guaranteed terminus? Affects whether the ≥1868 hard fallback is unconditional.
6. **Roster size:** confirm the 6 domain tags carrying `domain_sonno` (CSU, SHZ, YCH, SGA, DTE,
   AZU); more are cheap but each needs a historical alignment default.

---

## 9. Build order

1. Oracle-check §7 items 1–3, 5 (the AI-autonomy load-bearers) FIRST.
2. Add the dated historical characters to `setup/characters/00_Japan.txt`.
3. `se_JAPAN_BAKUMATSU.txt` (meters on TKG/domains, `yearly_country_pulse` hook, bands,
   firebrand concreteness, `JPN_baku_ingest_preperry` overlay read) + on_action + modifiers + loc.
4. `se_JAPAN_BOSHIN.txt` (Satchō bond, `JPN_boshin_execute`, war resolution, Meiji/JPN formation).
5. Beats B0–B7 events.
6. **Then** refactor #81 (§6) — move Perry scheduling to the Japan arc, repurpose the CHI-only hook
   to notify a human Qing, wire the post-Perry tree to Japan-side signals.
7. se_LOG audit of every new effect; SESSION_REPORT entries (#94 + #81-refactor).
