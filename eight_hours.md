
### 16:40:44 PDT — pos12-14 live BOOTS => combination involves pos15-17
Suspects narrowed: pos15 #11 sub-position titles (characterwindow.gui), pos16 #9 Impeach picker (censorate), pos17 B2 54-prov reassign (00_default).
Split: keep pos15+16 live (revert pos17 B2). BOOTS => partner is pos17 (B2 setup). CRASHES => partner in pos15/16.

### 16:45:43 PDT — pos12-16 live (pos17 B2 reverted) CRASHES => B2 NOT a partner
Partner is in pos15-16: #11 sub-position titles (635ec38ad) or #9 Impeach picker (2b7570463).
Split: revert pos16 (#9 impeach), keep pos12-15 live. BOOTS => #9 is a partner. CRASHES => #11 is a partner.

### 16:51:38 PDT — pos15(#11) live + pos16(#9) reverted BOOTS => #9 Impeach picker is a required partner
Combination = #9 (2b7570463) + a partner already live in base (pos12-14 or idx18). #11 titles NOT involved.
NEXT: keep ONLY #9 live (revert pos12-14 + all else). BOOTS => #9 needs a partner from pos12-14 (isolate which). CRASHES => #9 interacts with the idx18 base itself (isolate the #9 sub-change).
#9 files: se_QING_CENSORATE.txt, QING_censorate_panel.txt (scripted_gui), gui/imp19c_windows.gui (new picker window), qing_censorate.gui, events/qing_censorate_events.txt, loc.
