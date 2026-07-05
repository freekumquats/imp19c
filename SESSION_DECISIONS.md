# Session decisions log (2026-07-05, autonomous run: #78 → #77 → combined audit)

Running list of judgment calls made while the user is away. Newest section at the bottom.

## Already settled before the autonomous run
- **Traceability rule scope corrected:** the heightened "prove behavioural equivalence" tier applies ONLY to upstream/base-mod code I did NOT author. My own committed session features (Qing suite, economy fixes) are ordinary new-feature work when I fix them — trace, don't equivalence-gate. (User correction.)
- **Summer Palace #74-fix committed (98e5e033):** fixed 2 MEDIUM Branch-B bugs from SPreview2 review (double-modifier stack on standing Qingyi; Branch-B player could never trigger the 1860 sack), 1 LOG-fidelity follow-on, removed 1 dead loc key; left the Tongzhi modifier asymmetry as-is (historically correct) with a documenting comment.
- **#64-fix (crop trade-good definitions):** ScrutinyPass found a CRITICAL — the 5 New World crops (maize/sweet_potato/potato/peanut/chili) were assigned to 28 provinces + plumbed across ~20 economy files but never DEFINED under common/trade_goods/. Added 5 category=2 definitions cloned from the tobacco archetype (gold=0.2, local_monthly_food=0.07, distinct colors). This unblocks #78.
- **ScrutinyPass scope:** it audited ONLY the economy layer (commit 20db2dbd + the merge). Diplomacy-plays and migration/claims (commit c0eb5a39) were NOT audited.
- **Deferred audit decision (user):** do ONE combined correctness audit of ALL net-new Qing subsystems (diplomacy, migration, subjects, missions) as a dedicated pass AFTER #77/#78 — not interleaved. Recorded in memory imp19c-deferred-qing-subsystem-audit.
- **#78 mechanism (from oracle consultation):** local_population_capacity CANNOT live in a trade-good province={} block (unproven — no trade good in mod or either oracle does this). PROVEN path = a province modifier carrying local_population_capacity + local_population_growth, applied via add_province_modifier (precedent: 00_from_events_province.txt:77). So crops don't carry capacity; growing a crop TRIGGERS an applicator that stamps a pop-capacity modifier on the province.
