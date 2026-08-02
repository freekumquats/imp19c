# Feasibility: vanilla Mercenaries mechanic for Yong Ying (勇營) regional armies

Task #105. Assessment of whether to represent the Yong Ying / Brave Battalions —
gentry-raised, personally-loyal regional armies (湘軍/淮軍/楚軍) — using Imperator's
vanilla **mercenary** mechanic, instead of (or alongside) the current implementation.

## TL;DR

**Not recommended as a replacement.** The vanilla mercenary mechanic is (a) largely
disabled in this mod, (b) architecturally the *opposite* of what Yong Ying are (hired
outsiders loyal to coin vs. gentry armies loyal to a named patron), and (c) would
require re-enabling a map-wide system that affects every country, not just the Qing.
The **existing** implementation (`QING_sanction_regional_army` + loyal-cohort binding to
a real Han governor-general) already models the historically-correct dynamic and is the
better spine. One **narrow, optional** borrow is worthwhile — the *buy-off / disband-
by-payment* idiom — as a lever to dissolve an overmighty Yong Ying. Details below.

---

## What the vanilla mercenary mechanic actually is (as shipped here)

Two distinct engine features share the word "mercenary":

### 1. Mercenary BANDS (the classic hire-an-army-on-the-map system)
Spawned armies led by an `is_mercenary = yes` general, hireable for a lump sum, that
serve while paid and can be bought off by the enemy. Controlled by defines:

    common/defines/00_defines.txt
      MIN_MERCENARIES_PER_REGION = 0
      MERCENARIES_CITY_THRESHOLD = 50
      MERCENARIES_PER_CITY       = 0
      MERCENARY_BASE_AMOUNT      = 0
      MERCENARY_PER_POP_SCALE    = 0
      MERCENARY_AMOUNT_DEVIATION = 0
      MERCENARY_MAINTENANCE      = 1.5
      MERCENARY_DEBT_THRESHOLD   = 1.0
      MERCENARY_REINFORCE_MULT   = 0.33

**The spawn parameters are all ZEROED** — this mod does not spawn mercenary bands at
all. Re-enabling them is a **global** change (mercenaries would appear for every country
worldwide, an 1815 Victorian setting where hireable classical merc bands are an
anachronism). The only live remnant is `bribe_mercenary_button.txt` (a scripted GUI to
buy off an enemy's merc general — dormant with no bands to buy off) and the engine
keywords `is_mercenary` / `employer` / the reserved `MER` tag.

### 2. Mercenary SUBJECT (a spawned client country)
`common/scripted_guis/mg_syr_merc_subject_button.txt` creates a `create_country { ... }`
and `make_subject = { type = subject_mercenary_city_state }`. **Caveat:** that subject
type is a vanilla **Magna Graecia DLC** type (the button is DLC-gated:
`has_dlc = "Magna Graecia"`), and it is **NOT** defined in the mod's own
`common/subject_types/00_default.txt` (which has 17 types: vassal_tribe, tributary,
sinosphere_tributary, client_state, satrapy, autonomous_governorship, ...). So relying on
it hard-couples a Qing core mechanic to an optional DLC.

---

## Why mercenaries are the wrong model for Yong Ying (historically + mechanically)

| Dimension | Vanilla mercenaries | Yong Ying (勇營) | Verdict |
|---|---|---|---|
| Loyalty | to whoever pays (buy-off-able by the enemy) | to their **gentry founder** (Zeng/Li/Zuo), not even the throne | **opposite** |
| Origin | rootless bands / foreign captains | **local** gentry militia (團練) raised in the founder's home province | **opposite** |
| Funding | lump-sum hire + upkeep | likin (釐金) transit tax, locally raised | different |
| Danger modelled | desertion when unpaid | **regional devolution → warlordism** (the 北洋 seed) | different |
| Scope | map-wide, all countries | Qing-specific | mismatch |

The mercenary system's core tension is *"pay them or they leave/turn."* The Yong Ying's
core tension is *"they fight superbly, but for their patron — and that patron becomes a
provincial warlord."* These are different failure modes; forcing Yong Ying into the merc
frame would misrepresent the history and require fighting the engine's buy-off logic.

---

## What already exists (and is the right spine)

`QING_sanction_regional_army` (se_QING_MECHANICS.txt) + `QING_regional_army_bind_commander`:
- eases both rotting central armies (`qing_banner_decay` / `qing_greenstandard_decay` −8),
- pushes `qing_han_provincial_power` **+15** (the devolution meter),
- **binds the army to a REAL sitting Han governor-general** via `add_loyal_veterans = 8`
  + `QING_magnate_track_grant` — concrete-over-abstract, correctly filtered on
  `has_culture = han` (NOT primary_culture, which is Manchu),
- the `qing_yongying` unit type (army_qing_yongying.txt) is the on-map force,
- the grandee's-private-army civil-war seed in se_QING_COUNCIL.txt uses `qing_yongying`.

This already delivers the personal-loyalty + warlord-seed dynamic the mercenary mechanic
cannot. (There is also a known, deliberately-removed else-branch that once tried to
`create_character` a founder at a crashing call site — see the #90-fix comment; the
feature intentionally no-ops the concrete grant when no Han governor stands.)

---

## The one worthwhile borrow: the buy-off / disband-by-payment idiom

`bribe_mercenary_button.txt` demonstrates a clean, proven pattern:
`pay_price` + a `set_variable = { ... days = 365 }` cooldown + a custom-tooltip gate. This
is directly reusable as a **"Disband / pension off a Yong Ying army"** lever — the throne
pays a lump sum to stand down an overmighty regional army, on a cooldown, reducing
`qing_han_provincial_power`. This borrows the *idiom*, not the mercenary *system*, so it
adds no global side-effects and no DLC dependency.

**Recommendation:** keep the current spine; optionally add a treasury-funded "stand down
the Yong Ying" action modelled on the bribe-button price/cooldown idiom, as the mirror to
the sanction action (raise ↔ disband). No re-enabling of merc bands; no merc subject type.

## If a stronger "regional-army-as-entity" model is ever wanted
Prefer the mod's **own** subject system (`client_state` / a new bespoke subject type in
`00_default.txt`) over the DLC `subject_mercenary_city_state`, so a sanctioned Yong Ying
could optionally become a semi-autonomous Han military subject (the 北洋 → warlord-clique
endgame) without a DLC dependency. This is a larger feature and out of scope for #105;
noted for the backlog.
