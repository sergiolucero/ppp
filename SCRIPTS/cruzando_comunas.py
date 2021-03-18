from util import *
rdf=pd.read_csv('resumen_comunal.csv')
sql('SELECT * FROM sqlite_master')
ple=sql('SELECT region, comuna, COUNT(*) AS nPlebi FROM plebi GROUP BY region, comuna')
ple.head()
ple.merge(rdf).head()
ple=sql('SELECT region, comuna, COUNT(*) AS nMesas, SUM(votos) AS nVotos FROM plebi GROUP BY region, comuna')
sql('SELECT * FROM plebi LIMIT 1')
ple=sql('SELECT region, comuna, COUNT(*) AS nMesas, SUM(apruebo+rechazo) AS nVotos FROM plebi GROUP BY region, comuna')
ple.merge(rdf).head()
ple=ple.merge(rdf)
ple['porc_plebi']=ple.nVotos/ple.N
ple.sort_values('porc_plebi').head()
ple.sort_values('porc_plebi').tail()
pre=sql('SELECT region, comuna, COUNT(*) AS nMesas, SUM(votos_g+votos_p) AS nVotos FROM presi GROUP BY region, comuna')
pre.head()
ple.merge(pre).head()
ple.head()
pre.head()
ple.to_sql('temple',sqlite3.connect('temp.db'),index=False)
pre.to_sql('tempre',sqlite3.connect('temp.db'),index=False)
plepre=pd.read_sql('SELECT * FROM temple AS ple, tempre AS pre WHERE ple.region=pre.region AND ple.comuna=pre.comuna')
plepre=pd.read_sql('SELECT * FROM temple AS ple, tempre AS pre WHERE ple.region=pre.region AND ple.comuna=pre.comuna',sqlite3.connect('temp.db'))
len(plepre)
plepre.head()
plepre.columns=list(plepre.columns([:-1]))+['votos_presi']
plepre.columns=list(plepre.columns[:-1])+['votos_presi']
plepre.head()
plepre['porc_presi']=plepre['votos_presi'].apply(int)
plepre['porc_presi']=plepre['votos_presi']/plepre.N
plepre['votos_presi']=plepre['votos_presi'].apply(int)
plepre.head()
plepre['premple']=plepre['porc_presi']-plepre['porc_plebi']
plepre.head()
plepre.sort_values('premple').head()
plepre.sort_values('premple').tail()
plepre.to_csv('plevspre.csv',index=False)
!nano plevspre.csv
%hist -f cruzando_comunas.py
