import sys, os, glob; sys.path.insert(0,'tools')
from fetch_wm import fetch, resolve_search
from dds_icon import convert
D=sorted(glob.glob('gfx/interface/icons/military_traditions/arabic_*.dds'))[0]
TD='gfx/interface/icons/military_traditions'; SRC='art_src/tradfix2'; os.makedirs(SRC,exist_ok=True)
jobs={
 'qing_frontier_rotation':['Pingding battle engraving Qing','Ayusi lance rebels','Battle at Elei Zhalatu'],
 'napoleon_baton':['Nicolas Charles Oudinot Robert Lefevre','Marshal Ney portrait','Napoleonic marshal portrait'],
 'shiquan_burma':['Konbaung Burmese army painting','Burmese war elephant','Konbaung soldiers'],
 'qing_green_start':['Qing soldiers battle Attiret','Battle at Elei Zhalatu','Ayusi lance rebels'],
 'qing_green_patrol':['Qing dynasty guards painting','Battle at Elei Zhalatu','Ayusi lance'],
 'napoleon_dieu_de_la_guerre':['Vernet Battle of Hanau','Napoleonic artillery painting'],
 'qing_mongol_capstone':['Battle at Elei Zhalatu','Zhao Mengfu horse rider','Mongol cavalry painting'],
 'qing_mongol_khalkha':['Zhao Mengfu Mongol rider','Mongol horseman painting'],
 'qing_mongol_camels':['Kazakhs Presenting Horses Castiglione','Qianlong Mulan hunt','imperial hunt China'],
 'qing_green_rattan':['Victory at Heluo Heshi Attiret','Battle at Elei Zhalatu'],
 'napoleon_grande_batterie':['Vernet Battle of Hanau','Napoleonic battery painting'],
 'qing_green_marines':['Destroying Chinese war junks Duncan','Qing war junk painting'],
}
for k,qlist in jobs.items():
    out=f'{TD}/{k}.dds'; src=f'{SRC}/{k}.jpg'; ok=False
    for q in qlist:
        try:
            u,t=resolve_search(q,width=400)
        except Exception: continue
        if not t or t.lower().endswith(('.pdf','.djvu')): continue
        try:
            if os.path.exists(src): os.remove(src)
            fetch(('search',q),src,width=400); convert(src,out,like=D); print(f"OK {k} <- {t[:42]}",flush=True); ok=True; break
        except Exception as e: print(f"try-fail {k}: {e}",flush=True)
    if not ok: print(f"ERR {k}",flush=True)
print("DONE",flush=True)
