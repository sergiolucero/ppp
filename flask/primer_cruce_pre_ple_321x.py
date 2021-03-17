from machine import *

NIVEL = 'region,comuna,local'
cpre = sql(f'SELECT {NIVEL}, SUM(votos_g) AS Guillier, SUM(votos_p) AS Pinera FROM presi_v2 GROUP BY {NIVEL}')
cple = sql(f'SELECT {NIVEL}, SUM(apruebo) AS Apruebo, SUM(rechazo) AS Rechazo FROM plebi GROUP BY {NIVEL}')

cc = cpre.merge(cple)
print(len(cc))
pv1=sql('SELECT region, comuna, SUM(GOIC) AS votos_GOIC, SUM(KAST) AS votos_KAST, SUM(ENRIQUEZ) AS votos_ENRIQUEZ FROM presi_v1 GROUP BY region,comuna')
cc=cc.merge(pv1)

cc.to_sql('cruce_pre_ple_321x', sqlite3.connect('../cruce.db'), index=False)

# only 321 comunas match, how big are the ones that don't
