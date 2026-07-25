# 1763 Ownership-Layer Audit — Findings & Implementation Design

Draft for user review. Covers the two ownership-layer audits run 2026-07-22:
- **#34** colonial dependency audit (subject/colony relationships)
- **#38** independent-country audit (all 318 sovereign tags)

Both audits were **verified against the actual setup** before this doc (several of
their raw claims were wrong — corrections noted inline). All line numbers are
`setup/main/00_default.txt` unless stated. **Decisions are LOCKED (2026-07-22, §F);
the authoritative implementation plan is §G.** Nothing here is applied yet.

> **Reading order:** §A (dropped false positives) → §F (decisions) → §G (batch plan =
> what to implement). §B/§C/§D are the original findings/analysis, kept for rationale;
> where they said "your call", §F is the answer.

Already fixed this session (for context): **CYL** Ceylon → Dutch VOC + Kandy Sinhalese
(#33); **USA** name → "Thirteen Colonies" (#35); **MEX/NSP** merge (#32). Those are done
and pushed; not repeated below.

---

## A. Audit claims that turned out WRONG (verified — no action)

| Flag | Audit said | Reality (verified) | Verdict |
|------|-----------|--------------------|---------|
| **MOD** Modena | landless (0 provinces) | Owns province **7325 Modena** (capital there); a valid 1-province Este duchy | **NO FIX** — drop |
| **KHL** Sikh | landless (0 provinces) | Owns a ~40-province Punjab block (Lahore 2876 capital, Multan, Amritsar…) | Territory fine; unified-"Empire" framing anachronistic → §D2 / §F.2 (fragment, Batch 5) |
| **RUA** Russian-American Co. | anachronistic company existing 1763 | Already an **inert phantom tag** — #397 emptied its own_control_core + repointed capital; owns 0 provinces, dormant | **NO FIX** (optional: confirm it can't activate pre-1799) |

---

## B. HIGH-confidence colonial ownership fixes (APPROVED — §F)

Each is a straightforward reparent/inert on the dependency line + (where relevant) a
culture/religion + ruler correction, exactly like the CYL fix. Low risk, clear history.

### B1. HEL (Heligoland) — GBR → DEN
- Line 655: `dependency = { first = GBR second = HEL subject_type = client_colony }`.
- **History:** Heligoland was **Danish** 1714–1807; Britain seized it only in 1807. In 1763 it is Danish.
- **Fix:** change `first = GBR` → `first = DEN`. Check HEL culture (should be Frisian/German, not English) + any GBR arc referencing HEL.

### B2. BIG (British Guiana) — GBR → NED
- Line 675: `dependency = { first = GBR second = BIG ... }`.
- **History:** Essequibo/Demerara/Berbice were **Dutch (VOC)** colonies until Britain took them 1796–1814.
- **Fix:** reparent `first = GBR` → `first = NED`; set BIG culture/religion to Dutch (mirror CYL); check the tag name/loc ("British Guiana" is anachronistic — consider a "Dutch Guiana"/Essequibo cosmetic name). Verify vs the existing **DUG** (Dutch Guiana/Suriname) tag — BIG + DUG should not overlap provinces.

### B3. ION (Ionian Islands) — GBR → **Venetian subject** (§F.3, Batch 3)
- Line 657: `dependency = { first = GBR second = ION subject_type = protectorate }`.
- **History:** Venetian until 1797; British "United States of the Ionian Islands" only 1815. In 1763 they were **Venetian**.
- **DECIDED (§F.3):** fold ION under **VNC** (Venice) as a subject (VNC exists). See Batch 3 (§G). (Note: pulled out of Batch 1 into its own Batch 3.)

### B4. SLE (Sierra Leone) — GBR → uncolonized/inert
- Line 701: `dependency = { first = GBR second = SLE subject_type = client_colony }`.
- **History:** No European colonial government in 1763; British "Province of Freedom" settlement began **1787**. Coastal trade posts only; interior was Temne/Mende.
- **Fix:** apply the **inert-tag playbook** (empty own_control_core → repoint capital to an extant province → drop the GBR→SLE dependency → remove any set_as_ruler), OR reassign its provinces to a resident African tag if one exists. Same pattern as ALC/#397.

---

## C. Independent-country fixes (APPROVED — §F, low risk)

### C1. SIA (Siam) — wrong dynasty on the ruler
- Capital Ayutthaya is **correct**; only `family = 23` (Chakri, ruled from 1782) is wrong.
- 1763 king = **Ekkathat**, of the **Ban Phlu Luang** dynasty (r.1758–1767, until the 1767 Burmese sack).
- **Fix:** point `family` at the correct dynasty (create the family if absent) and/or set a correct 1763 ruler character. Cosmetic-ish; no territory change. (Same *class* as the Persia `family=13 Qajar` cosmetic label the audit noted — consider fixing both.)

### C2. Persia PR2 — cosmetic family label (LOW)
- PR2 correctly = Karim Khan Zand, capital Shiraz. Only `family = 13` ("Qajar") is a wrong label; Qajars ruled from 1789. Cosmetic; fix if trivial.

---

## D. DESIGN-JUDGMENT items — DECIDED (see §F for the ruling; analysis kept for rationale)

These weren't simple bugs; they were scenario-scope choices. All now decided — each
subsection notes the ruling; the analysis below it is retained as rationale.

### D1. The EIC-in-India cluster (14 dependencies, lines 685–698) → **DECIDED: FREE ALL 14** (§F.1, Batch 4)
The setup subordinates a large slice of India to **EIC** at the 1763 start:
- **protectorate:** MYS (Mysore), HYD (Hyderabad)
- **subsidiary_ally:** COO (Coorg), TRV (Travancore)
- **client_state:** TJR, DHN, RMH, BNR, BIH, PAT, AWA (Awadh), MUG (Mughal)
- **tributary:** BHU (Bhutan), SKK (Sikkim)

**History:** In Feb 1763 the EIC was **pre-Buxar** (Buxar = Oct 1764). Post-Plassey (1757)
it dominated **Bengal** but almost nothing else. Specifically wrong for 1763:
- **MYS** (Hyder Ali) — *hostile independent power*; fought the EIC in four wars 1767–99. Should be **independent**.
- **HYD** (Nizam) — independent; subsidiary alliance only **1798**. Should be **independent**.
- **TRV / COO** — independent; British ties **1795 / post-1834**. Should be **independent**.
- **AWA** (Awadh) — independent Nawab until Buxar/Allahabad **1764–65**. ~1–2 yrs early.
- **MUG** (Mughal) — nominally sovereign in Feb 1763; de-facto EIC control from Buxar. ~1.5 yrs early.
- **BNR/BIH/PAT/DHN/RMH/TJR** — Bengal/Bihar successor fragments; the *Bengal* ones (BNR Bengal, BIH Bihar, PAT Patna) are the **defensible** post-Plassey EIC sphere; the southern ones are not.

The full free-all-14 list: MYS HYD TRV COO TJR DHN RMH BNR BIH PAT AWA MUG BHU SKK.
(Original analysis leaned toward a partial free — freeing only MYS/HYD/TRV/COO + maybe
MUG, keeping the Bengal cluster BNR/BIH/PAT. **Overridden by §F.1: free ALL 14.**)
The interaction with EIC missions/arcs is the reason Batch 4 (§G) includes mandatory
downstream event updates. *Implementation:* delete each `dependency` line; verify each
freed tag is landed/viable; check culture/religion/ruler; update every EIC-subject
reference (see §G Batch 4).

### D2. KHL — "Sikh Empire" tag is anachronistic (framing, not territory) → **DECIDED: FRAGMENT into misls** (§F.2, Batch 5)
KHL owns the Punjab correctly, but as a unified **`imperial_monarchy` "Sikh Empire"**.
The Sikh Empire is **Ranjit Singh, 1799**. In 1763 the Punjab was the **misl confederacy**
(independent Sikh misls), not one empire. (Original recommendation was the cheap cosmetic
re-government; **overridden by §F.2: fragment into misl tags** — see Batch 5 for scope.)

### D3. BLZ (Belize) — GBR client_state → SPA de jure → **DECIDED: FIX** (§F.4, Batch 1)
Line 676. Britain had only **logging rights** (1763 Treaty of Paris), not sovereignty;
Belize remained **Spanish de jure** until 1786+. Reparent GBR→SPA (or inert). Folded into
Batch 1.

---

## E. (superseded) — the authoritative plan is §G

The original 4-batch order here was replaced by the locked 5-batch plan in **§G**
(after the decisions in §F). See §G. Tracker tasks: #37 (Batch 1), #40 (Batch 2),
#41 (Batch 3), #42 (Batch 4 EIC), #43 (Batch 5 KHL).

---

## F. DECISIONS (locked by user 2026-07-22)
1. **EIC-India (D1):** **FREE ALL 14** from EIC — the Company keeps only its factory ports; every subordinated Indian state becomes independent. (MYS HYD TRV COO TJR DHN RMH BNR BIH PAT AWA MUG BHU SKK — lines 685–698.) Must verify each freed tag is landed + viable, and that EIC itself + any EIC mission/arc survives losing all subjects.
2. **KHL (D2):** **FRAGMENT into misls** — split the unified "Sikh Empire" into independent misl tags. Largest effort (new tags, COAs, province reassignment across the Punjab bloc). Research the historical misls + their rough territory first.
3. **ION (B3):** **Venetian subject** — fold ION under VNC (Venice).
4. **BLZ (D3):** **FIX** — Belize was Spanish de jure in 1763; reparent GBR→SPA (or inert). 
5. Also DO: **HEL→DEN, BIG→NED, SLE→inert** (B1/B2/B4); **SIA dynasty + Persia label** (C1/C2).
6. Design doc: **NOT committed** — kept as a local working file.

## G. Implementation batches (in order; each reviewed + boot-crash-reviewed before commit)
- **Batch 1 (low-risk reparents):** HEL→DEN, BIG→NED (+Dutch culture), SLE→inert, BLZ→SPA. One commit per tag or grouped.
- **Batch 2 (ruler labels):** SIA dynasty (Ekkathat/Ban Phlu Luang), Persia Qajar→Zand label. One commit.
- **Batch 3 (ION→Venice):** fold ION under VNC as a subject.
- **Batch 4 (EIC free-all-14):** remove all 14 EIC dependency lines; verify each freed tag landed/viable; check EIC + missions survive. Its own review + boot test.
  - **⚠️ DOWNSTREAM EVENT/MISSION UPDATES (user-flagged) — MUST do as part of this batch:**
    - `common/missions/qing_india_missions.txt` — frames the campaign "vs the EIC for the paramountcy of Hindustan"; gate `exists = c:EIC` still fine, but any mission task that assumes EIC *subjects* (e.g. targeting/weakening subordinated states) must be re-scoped. The Qing-intervenes-in-India arc is the headline one to update.
    - `common/scripted_effects/se_QING_INDIA.txt:51` — stamps a modifier on ports where `controller = { OR = { tag = EIC  is_subject_of = c:EIC } }`. After free-all-14, `is_subject_of = c:EIC` matches nothing → the descent bears only on EIC's OWN Bengal/Bihar factory ports. That is arguably MORE correct (post-Plassey the Company held Bengal directly), but VERIFY the mission still has meaningful targets. May want to broaden to the now-independent Bengal states (BNR/BIH/PAT) or GBR-India.
    - `common/missions/qing_himalaya_seasia_missions.txt` — references BHU/SKK (freed tributaries) as `FUNC_make_subject` targets for the Qing; freeing them from EIC is fine (they become independent, still valid subject targets), but confirm.
    - `events/imp19c_mod_events/asia_napoleonic_events.txt:129` — `exists = c:EIC` + `c:EIC = { ... }`; check it doesn't iterate EIC subjects.
    - `common/scripted_effects/se_QING_GREATGAME.txt` — comments only (post-Plassey EIC), likely no code change.
    - `events/introduction_events/introduction_events.txt:531` (tag = EIC) + `se_CURRENCY.txt` (EIC currency adopter) — verify unaffected (EIC still exists, just subject-less).
  - EIC ITSELF stays (megacorporation with its Bengal factory ports); only its 14 subjects are freed.
- **Batch 5 (KHL→misls):** biggest — research the historical Sikh misls (Sukerchakia, Bhangi, Ahluwalia, Kanhaiya, Ramgarhia, Nakai, Dallewalia, Faizullapuria/Singhpuria, Karorsinghia, Nishanwalia, Shaheedan, Phulkian/Patiala…) + their rough 1763 territory; create tags (+ COAs, loc, culture=punjabi/religion=sikhism); reassign KHL's ~40 Punjab provinces across them. Check any ref to KHL (2 files) — re-point or drop. Its own full cycle + boot test.

## H. Superseded open questions (answered above; kept for history)
1. EIC-India scope → FREE ALL 14. 2. KHL → FRAGMENT. 3. ION → Venetian subject. 4. BLZ → fix. 5. HEL/BIG/SLE + SIA/Persia → do.
