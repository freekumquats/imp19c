# DESIGN — Concretize `qing_xinjiang_control` from the real ILI subject + Xinjiang provinces (控馭新疆)

**Branch:** merge-overnight. **Status:** ✅ SHIPPED 2026-08-06 (#10B commit 64de2b6ed). **Scope:** CHI. #91 item D.

## 0. Problem (verified)
`qing_xinjiang_control` (0–100, seed 40) is event-set/nudged (`se_QING_ILI.txt:98/125/153/232` set to
0/80/10/90 at story beats; a `−25` nudge :210). No derive block. But the concrete referents exist: the
real **ILI autonomous_governorship subject** (`c:ILI is_subject_of ROOT`, `se_QING_ILI.txt:458`) and the
Xinjiang provinces themselves.

## 1. Thesis — derive control from the real ILI subject fate + Xinjiang province state
`qing_xinjiang_control` target ← a blend of concrete facts:
- **ILI subject status:** `exists = c:ILI  c:ILI = { is_subject_of = ROOT }` → high control; ILI broken away
  / independent → control collapses. (This is the sharpest signal — the meter literally tracks "grip on the
  New Dominion," and ILI is that dominion's on-map embodiment.)
- **Xinjiang province ownership + unrest:** how many Xinjiang-region provinces ROOT controls, and their
  `province_unrest` — a revolt-wracked Xinjiang = low control.
The story-beat SETs (0/80/90 at reconquest/loss events) can stay as one-shot overrides OR become nudges the
live counter drifts back from; the derived target is the steady-state truth.

## 2. Consumers (unchanged): `se_QING_ILI.txt:281/286/319` (≥70/≤20), `se_QING_XINJIANG.txt:439` (≤30).
## 3. ⚠️ DOWNSTREAM: `qing_caravan_prosperity` reads `qing_xinjiang_control` (meter-of-meter, task #11) —
improves transitively; no action needed here but note it.
## 4. Feasibility / gotchas
- **`is_subject_of` proven** (memory: not recursive — use `owner={overlord={is_subject_of=X}}` for nested,
  but ILI is a direct subject so `c:ILI = { is_subject_of = ROOT }` is fine). VERIFY the Xinjiang-region
  province set (is_in_region key).
- **The story SETs are load-bearing:** the ILI arc SETS control to 0/80/90 at scripted moments (reconquest,
  loss). A derived target could FIGHT those (set to 90, then derive-drifts back down next pulse). DECISION:
  the story beats should move the underlying CONCRETE state (ILI subject status), not just the meter — e.g.
  a reconquest event re-subjugates ILI, and the derived control then reads high. If the arc can't be fully
  concretized, keep the SETs as overrides + a cooldown before the derived target resumes. This is the main
  design risk — verify the arc's SETs correspond to real subject-status changes.
- **1763 opening:** ILI is a subject at 1763 → control derives HIGH; seed is 40 (mid) — the derived value
  may open HIGHER than seed. Reconcile: is 1763 Xinjiang firmly held (high) or contested (40)? Match history
  (1759 conquest complete, so ~firmly held early) — the derive may be MORE correct than the seed; verify intent.
## 5. Checklist: derive control from ILI subject status + Xinjiang province ownership/unrest; reconcile the
story-beat SETs (move real subject status, not just the meter); consumers unchanged; verify 1763 opening;
caravan_prosperity noted; review.
