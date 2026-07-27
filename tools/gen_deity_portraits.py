import sys, os, re; sys.path.insert(0,'tools')
from fetch_wm import fetch, resolve_search
from dds_icon import convert
OUT='gfx/interface/icons/deities'; os.makedirs(OUT,exist_ok=True)
SRC='art_src/deity'; os.makedirs(SRC,exist_ok=True)
# deity_key -> person query (portrait). CJK stripped; add "portrait" for a face.
P={
 'deity_montesquieu':'Montesquieu portrait','deity_adam_smith':'Adam Smith portrait',
 'deity_voltaire':'Voltaire portrait','deity_tocqueville':'Alexis de Tocqueville portrait',
 'deity_john_stuart_mill':'John Stuart Mill portrait','deity_ricardo':'David Ricardo economist portrait',
 'deity_kant':'Immanuel Kant portrait','deity_yan_fu':'Yan Fu scholar portrait',
 'deity_burke':'Edmund Burke portrait','deity_friedrich_list':'Friedrich List economist portrait',
 'deity_de_maistre':'Joseph de Maistre portrait','deity_bonald':'Louis de Bonald portrait',
 'deity_hume':'David Hume portrait','deity_malthus':'Thomas Robert Malthus portrait',
 'deity_coleridge':'Samuel Taylor Coleridge portrait','deity_feng_guifen':'Feng Guifen portrait',
 'deity_hegel':'Georg Wilhelm Friedrich Hegel portrait','deity_colbert':'Jean-Baptiste Colbert portrait',
 'deity_bossuet':'Jacques-Benigne Bossuet portrait','deity_metternich':'Klemens von Metternich portrait',
 'deity_de_maistre_legit':'Joseph de Maistre portrait','deity_necker':'Jacques Necker portrait',
 'deity_carlyle':'Thomas Carlyle portrait','deity_zeng_guofan':'Zeng Guofan portrait',
 'deity_fichte':'Johann Gottlieb Fichte portrait','deity_list_nat':'Friedrich List economist portrait',
 'deity_herder':'Johann Gottfried Herder portrait','deity_mazzini':'Giuseppe Mazzini portrait',
 'deity_michelet':'Jules Michelet portrait','deity_hamilton':'Alexander Hamilton portrait',
 'deity_mickiewicz':'Adam Mickiewicz portrait','deity_liang_qichao':'Liang Qichao portrait',
 'deity_blanqui':'Auguste Blanqui portrait','deity_saint_simon':'Henri de Saint-Simon portrait',
 'deity_fourier':'Charles Fourier socialist portrait','deity_robert_owen':'Robert Owen portrait',
 'deity_louis_blanc':'Louis Blanc portrait','deity_sismondi':'Jean de Sismondi portrait',
 'deity_proudhon':'Pierre-Joseph Proudhon portrait','deity_kang_youwei':'Kang Youwei portrait',
 'deity_karl_marx':'Karl Marx portrait','deity_engels':'Friedrich Engels portrait',
 'deity_bakunin':'Mikhail Bakunin portrait','deity_babeuf':'Gracchus Babeuf portrait',
 'deity_kautsky':'Karl Kautsky portrait','deity_lassalle':'Ferdinand Lassalle portrait',
 'deity_luxemburg':'Rosa Luxemburg portrait','deity_li_dazhao':'Li Dazhao portrait',
}
DON=None  # no local donor; use --size 100 BGRA8 (matches Invictus deity_cr_car_melqart 100x100)
log=open('tools/deity_portrait_log.tsv','w',encoding='utf-8'); log.write("key\tquery\tsource\tstatus\n")
for k,q in P.items():
    out=f'{OUT}/{k}.dds'; src=f'{SRC}/{k}.jpg'; ok=False
    for qq in [q, q.replace(' portrait','')]:
        try:
            u,t=resolve_search(qq,width=300)
        except Exception: continue
        if not t or t.lower().endswith(('.pdf','.djvu')): continue
        try:
            if os.path.exists(src): os.remove(src)
            fetch(('search',qq),src,width=300); convert(src,out,size=100)
            log.write(f"{k}\t{qq}\t{t}\tOK\n"); print(f"OK {k} <- {t[:40]}",flush=True); ok=True; break
        except Exception as e: print("try-fail",k,e,flush=True)
    if not ok: log.write(f"{k}\t{q}\tERR\n"); print("ERR",k,flush=True)
log.close(); print("DONE",flush=True)
