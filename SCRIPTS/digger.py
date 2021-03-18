from util import sql
q='''SELECT comuna, local, votos_p, votos_p, apruebo, rechazo, AVG(CAST(apruebo AS float)/(apruebo+rechazo)) AS porc_apr,                AVG(CAST(votos_p AS float)/(votos_p+votos_g)) AS porc_pin FROM cruce_locales WHERE region=8                GROUP BY comuna, local ORDER BY porc_apr-porc_pin DESC LIMIT 5'''
q='''SELECT comuna, SUM(votos_p), SUM(votos_p), SUM(apruebo), SUM(rechazo), AVG(CAST(apruebo AS float)/(apruebo+rechazo)) AS porc_apr,                AVG(CAST(votos_p AS float)/(votos_p+votos_g)) AS porc_pin FROM cruce_locales WHERE region=8                GROUP BY comuna ORDER BY porc_apr-porc_pin DESC LIMIT 5'''
df8=sql(q)
df8
mid = ','.join(['SUM(%s) AS total_%s' %(x,x) for x in ['votos_p','votos_g','apruebo','rechazo']])
q8p=f"SELECT local, {mid}, SUM(CAST(apruebo AS float))/(SUM(apruebo)+sum(rechazo)) AS porc_apr, SUM(CAST(votos_p AS FLOAT))/(SUM(votos_p)+SUM(votos_g)) AS porc_pin FROM cruce_locales WHERE comuna='PENCO' GROUP BY local"
mdf=sql(q8p)
mdf
%hist -f digger.py
