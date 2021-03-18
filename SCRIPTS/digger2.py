from util import sql

q='''SELECT comuna, SUM(votos_p), SUM(votos_p), SUM(apruebo), SUM(rechazo), AVG(CAST(apruebo AS float)/(apruebo+rechazo)) AS porc_apr,                AVG(CAST(votos_p AS float)/(votos_p+votos_g)) AS porc_pin FROM cruce_locales WHERE region=8                GROUP BY comuna ORDER BY porc_apr-porc_pin DESC LIMIT 5'''
df8=sql(q)

mid = ','.join(['SUM(%s) AS total_%s' %(x,x) for x in ['votos_p','votos_g','apruebo','rechazo']])
q8p=f"SELECT local, {mid}, SUM(CAST(apruebo AS float))/(SUM(apruebo)+sum(rechazo)) AS porc_apr, SUM(CAST(votos_p AS FLOAT))/(SUM(votos_p)+SUM(votos_g)) AS porc_pin FROM cruce_locales WHERE comuna='PENCO' GROUP BY local"
mdf=sql(q8p)

local=mdf.iloc[0]['local']
lq=f"SELECT mesa, {mid}, SUM(CAST(apruebo AS float))/(SUM(apruebo)+sum(rechazo)) AS porc_apr, SUM(CAST(votos_p AS FLOAT))/(SUM(votos_p)+SUM(votos_g)) AS porc_pin FROM cruce_locales WHERE comuna='PENCO' AND local='{local}' GROUP BY mesa"
ldf=sql(lq)

#cdf=sql('SELECT * FROM (SELECT * FROM plebi2) AS ple, (SELECT * FROM presi) AS pre \
#	WHERE ple.region=pre.region AND ple.comuna=pre.comuna AND ple.local=pre.local AND pre.mesa=ple.mesa')

#cdfs.to_sql('cruce_simple', sqlite3.connect('cruce.db'),index=False)

cdfs = sql('SELECT * FROM cruce_simple')

lq=f"SELECT mesa, {mid}, SUM(CAST(apruebo AS float))/(SUM(apruebo)+sum(rechazo)) AS porc_apr, SUM(CAST(votos_p AS FLOAT))/(SUM(votos_p)+SUM(votos_g)) AS porc_pin FROM cruce_simple WHERE comuna='PENCO' AND local='{local}' GROUP BY mesa"
ldf=sql(lq)
ldf['delta']=ldf.porc_pin-ldf.porc_apr
