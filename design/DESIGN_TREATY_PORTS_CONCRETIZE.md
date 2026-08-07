# DESIGN — Concretize `qing_treaty_ports` count from real treaty-port modifiers (通商口岸)

**Branch:** merge-overnight. **Status:** DESIGN (not built). **Scope:** CHI. #91 item B (count half only).

## 0. Scope — COUNT only; burden stays an accumulator
`qing_treaty_ports` is a hand-maintained `change_variable` tally (`+5` on system imposition
`se_QING_TREATIES.txt:71`, `+1` per additional port `:99`). It ALREADY stamps real `qing_treaty_port`
province modifiers alongside (`:175`, via `QING_treaty_stamp_port`). So the concrete object exists; the
count just isn't read from it. This doc derives the COUNT from the real modifiers.

**`qing_treaty_burden` is OUT OF SCOPE — it stays an accumulator** (separate, verified reason): burden is
eased by *treaty revision* (tariff autonomy −12, extrality abolition −30, `QING_treaty_revise:8/18`), which
never removes ports. A count-derived burden could never be lowered by reform (killing the sovereignty-clawback
payoff arc), and would perversely DROP when treaty-port provinces are lost. Burden is a path-dependent
grievance, not a footprint fact. Leave it.

## 1. Thesis — derive the count from `has_province_modifier = qing_treaty_port`
Replace the `+5/+1` hand-tally with a live count of the real modifiers. ⚠️ **The recount MUST fold in the
tier-applier and be wired at all three stamp sites (review F1) — the count feeds `apply_ports_modifier`
INLINE, so a recount that runs only on the pulse leaves the applier reading a stale/zeroed count for up to a
quarter.** Bundle recount+apply into one effect:
```
QING_treaty_recount_ports = {
    set_variable = { name = qing_treaty_ports  value = 0 }
    every_owned_province = {
        limit = { has_province_modifier = qing_treaty_port }
        ROOT = { change_variable = { name = qing_treaty_ports  add = 1 } }
    }
    QING_treaty_apply_ports_modifier = yes   # recount THEN apply — never read a stale count (F1)
}
```
(proven country-scope idiom — `FUNC_num_ports_in_country` skeleton `FUNC_svalues.txt:71`, body =
`limit = { has_province_modifier } add = 1`; `qing_treaty_port` modifier proven at `qing_treaties_modifiers.txt`.
The `ROOT = { change_variable add = 1 }` effect form — NOT a bare `add=` — is the correct translation of the
svalue skeleton, since all treaty effects run in country scope ROOT=CHI; matches the dike/depot/granary
recount idiom `se_QING_MINISTRY.txt`.)

**Wiring (F1 — AND, not OR; pin the order):** replace the three existing `QING_treaty_apply_ports_modifier = yes`
calls with `QING_treaty_recount_ports = yes`:
- `QING_treaty_impose` `:80` — must sit AFTER the `while`-stamp loop `:74` (else it reads 0 ports right after
  imposing 5, drops the commerce tier for a quarter — the exact beat that should light `_minor`).
- `QING_treaty_open_port` `:103` — right after the stamp `:102`.
- `QING_treaty_pulse` `:258` — the quarterly demotion-on-loss pass.

Remove the `+5`/`+1` counter bumps at `:71/:99` (the `QING_treaty_stamp_port` calls that STAMP the modifiers
stay — they place the concrete object; only the parallel counter bump is retired).

⚠️ **There is NO province-cession hook (F1).** The doc's earlier "call after loss" implied a trigger that
does not exist — demotion-on-loss lags up to one quarter, riding the `QING_treaty_pulse` cadence (matching
`QING_fbuild_upkeep_sweep`, `se_QING_FOREIGNBUILD.txt:214`). That lag is fine; state it, don't imply an
instantaneous loss hook.

## 2. USER DECISION — "N currently OWNED" is the correct metric (2026-08-06)
This flips the count from MONOTONIC ("N ports ever opened") to OWNED ("N held right now"):
- A treaty port lost to conquest/cession drops out of the count → its tier can fall. **This is INTENDED** —
  losing a treaty port is its own punishment; it doesn't need separate tracking, and the humiliation
  correctly eases as the foreign foothold is expelled.
- This also self-corrects the existing **counter↔modifier divergence** the `+5` loop can cause: the `while =
  { count = 5  QING_treaty_stamp_port }` (`:74`) stamps FEWER than 5 modifiers if China lacks un-stamped
  coastal cities (`QING_treaty_stamp_port` guards `is_coastal + has_city_status + NOT has_modifier`, `:159`;
  else-branch logs "counter advanced but no port stamped" `:192`). Under "N owned," the count = real ports,
  so this divergence vanishes (you only get credit for ports actually opened). ✓ correct by design.

## 3. ⚠️ Tier-reachability check (the review's open question)
The count feeds ONLY the 3 tier bands (`se_QING_TREATIES.txt:204-215`): `_minor ≥1`, `_major ≥7`,
`_dominant ≥12`. Under owned-semantics, reaching `_dominant` needs **12 simultaneously-held coastal-city
treaty ports**. VERIFY at build: does CHI realistically own ≥12 coastal cities that can be stamped? If the
coastal-city supply caps below 12, `_dominant` becomes unreachable (a behavior change from the monotonic
tally, which could hit 12 by counting ever-opened ports even if some were later lost). Options if
unreachable: lower the `_dominant` threshold, or accept `_dominant` as a rare late-game apex. DECIDE against
the real coastal-city count — do not assume 12 is reachable.

## 4. Concession exclusion (the customs-review lesson)
Count ONLY the `qing_treaty_port` modifier (foreign-forced). Do NOT count `qing_foreign_concession_building`
(Macau — the Qing-DOMINANT, sovereign concession, `qing_foreign_buildings.txt:83`). Different thing:
concession = Qing holds the quarter; treaty port = foreign-forced. The modifier is already the right
foreign-forced signal (the missionary-station system reads the same modifier, `se_QING_MISSIONARY_STATIONS.txt:170`
— consistent, no conflict).

## 5. 1763 opening + feasibility
- **1763 = 0 treaty ports** (pre-Opium-War; the system isn't imposed) → count 0, `_minor` band absent. Matches
  the seed (`:52` seeds 0). No div0 (pure addition, no division).
- Pure count svalue/effect; country-scope `every_owned_province` is cheap. No drift/target needed — it's an
  integer FACT, recomputed on change, not a gauge.

## 6. Build checklist (ONE commit — count only)
1. `QING_treaty_recount_ports` (every_owned_province has_province_modifier count); call after stamp/loss or per pulse.
2. Remove the `+5` (`:71`) and `+1` (`:99`) counter bumps; KEEP the `QING_treaty_stamp_port` modifier stamps.
3. Verify tier bands 1/7/12 still read the recomputed count; check `_dominant` (12) reachability vs real
   coastal-city supply (§3).
4. Burden UNTOUCHED (accumulator).
5. Review gates: count from qing_treaty_port modifier only (not concession); owned-semantics intended (tiers
   fall on loss); _dominant reachability checked; 1763 opens 0; stamps retained/counter retired; brace/quote/BOM;
   boot-crash review.
