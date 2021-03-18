from util import *
pd.set_options
pd.set_option('max_colwidth',200)
sql('SELECT * FROM sqlite_master')
# rewrite pivot_presi
pdf=sql("SELECT * from presi WHERE Candidato='PIÑERA'")
gdf=sql("SELECT * from presi WHERE Candidato='GUILLER'")
pdf.head()
cdf=pdf.join(gdf,on=['region','comuna','local','mesa'])
pdf.merge
pdf.merge?
gdf=sql("SELECT * from (SELECT * FROM presi WHERE Candidato='GUILLER') AS g, (SELECT * FROM presi WHERE Candidato='PIÑERA') AS p\")
gdf=sql("SELECT * from (SELECT * FROM presi WHERE Candidato='GUILLER') AS g, (SELECT * FROM presi WHERE Candidato='PIÑERA') AS p WHERE p.region=g.region AND p.comuna=g.comuna AND p.local=g.local") # first cross
len(gdf)
sql("SELECT region, COUNT(*) FROM presi GROUP BY region")
sql("SELECT region, COUNT(*) FROM plebi GROUP BY region")
ls
dregs
dreg
dreg=pickle.load(open('regiones.pk','rb'))
dreg
import pickle
dreg=pickle.load(open('regiones.pk','rb'))
dreg
!nano util.py
plebi=sql('SELECT * FROM plebi')
len(plebi)
sql('SELECT COUNT(*) FROM presi')
plebi.head()
plebi['region']=plebi.region.apply(lambda r: dreg[r])
plebi.head()
sql('SELECT * FROM presi LIMIT 3')
plebi.to_sql('plebi', index=False,if_exists='replace')
plebi.to_sql('plebi', sqlite3.connect('cruce.db'), index=False,if_exists='replace')
%hist
gdf=sql("SELECT * from (SELECT * FROM presi WHERE Candidato='GUILLER') AS g, (SELECT * FROM presi WHERE Candidato='PIÑERA') AS p WHERE p.region=g.region AND p.comuna=g.comuna AND p.local=g.local AND p.mesa=g.mesa") # first cross
gdf
gdf=sql("SELECT * FROM presi WHERE Candidato='GUILLIER")
gdf=sql("SELECT * FROM presi WHERE Candidato='GUILLIER'")
len(gdf)
gdf=sql("SELECT * from (SELECT * FROM presi WHERE Candidato='GUILLIER') AS g, (SELECT * FROM presi WHERE Candidato='PIÑERA') AS p WHERE p.region=g.region AND p.comuna=g.comuna AND p.local=g.local AND p.mesa=g.mesa") # first cross
len(gdf)
sql('SELECT COUNT(*) FROM presi')
gdf.head()
gdf.columns=['region','comuna','local','mesa','CG','votos_g','rp','cp','lp','mp','CP','votos_p']
gdf.head()
gdf=gdf[['region','comuna','local','mesa','votos_g','votos_p']]
gdf.to_sql('presi',sqlite3.connect('cruce.db'),index=False,if_exists='replace')
!ls -l
sql('SELECT * FROM presi LIMIT 5')
sql('SELECT * FROM plebi LIMIT 5')
ls
sql('SELECT * FROM sqlite_master')
sql('SELECT * FROM equiv').to_dict()
edf=sql('SELECT * FROM equiv')
edf.head()
edf[edf.pre!=edf.ple]
ple2pre=dict(ple=edf.ple,pre=ed.pre)
ple2pre=dict(ple=edf.ple,pre=edf.pre)
ple2pre
ple2pre=dict(ple=edf.ple.values,pre=edf.pre.values)
pdf
whos
gdf
%hist
plebi
plebi['local']=plebi.local.apply(lambda loc:ple2pre[loc])
plebi['local']=plebi.local.apply(lambda loc:ple2pre.get(loc,loc))
plebi.to_sql('plebi2', sqlite3.connect('cruce.db'), index=False,if_exists='replace')
cdf=sql('SELECT * (SELECT * FROM plebi2) AS ple, (SELECT * FROM presi) AS pre WHERE ple.region=pre.region AND ple.comuna=pre.comuna AND ple.local=pre.local AND pre.mesa=ple.mesa')
cdf=sql('SELECT * FROM (SELECT * FROM plebi2) AS ple, (SELECT * FROM presi) AS pre WHERE ple.region=pre.region AND ple.comuna=pre.comuna AND ple.local=pre.local AND pre.mesa=ple.mesa')
len(cdf)
sql('SELECT COUNT(*) FROM presi')
cdf.head()
cdf.columns
cc=cdf.columns[:6]+['pr','pc','pl','pm','votos_g','votos_p']
cc
cc=cdf.columns[:6].append(['pr','pc','pl','pm','votos_g','votos_p'])
cc=list(cdf.columns[:6])+['pr','pc','pl','pm','votos_g','votos_p']
cc
cdf.columns=cc
cdf.head()
cdf=cdf[list(cc.columns[:6])+list(cc.columns[-2:])]
cdf=cdf[list(cdf.columns[:6])+list(cdf.columns[-2:])]
cdf.head()
cdf.to_sql('cruce1',sqlite3.connect('cruce.db'),index=False,if_exists='replace')
cdf['Pi_vs_Gu_menos_Rec_vs_Apr']=
cdf['Pi_vs_Gu']=cdf['votos_p']-cdf['votos_g']
cdf['Rec_vs_Apr']=cdf['rechazo']-cdf['apruebo']
cdf.head()
for x in ('votos_g','votos_p'):
    cdf[x]=cdf[x].apply(int)
cdf['Pi_vs_Gu']=cdf['votos_p']-cdf['votos_g']
cdf.head()
cdf.to_sql('cruce1',sqlite3.connect('cruce.db'),index=False,if_exists='replace')
xdf=cdf.groupby(['region','comuna','local']).sum()
xdf.head()
xdf.to_html('TotalMesas.html')
xdf.corr()
xdf.to_sql('cruce_locales',sqlite3.connect('cruce.db'),index=False)
%hist -f manipulando.py
