from util import *

cdf=sql('SELECT presi.region,presi.comuna, presi.local, presi.mesa, apruebo, rechazo, votos_g, votos_p \
	FROM plebi, presi,equiv WHERE plebi.local=equiv.ple AND presi.local=equiv.pre AND presi.mesa=plebi.mesa')
gdf=cdf.groupby('comuna').agg({k: 'sum' for k in cdf.columns[-4:]})
gdf['porcP']=100*gdf['votos_p']/(gdf['votos_p']+gdf['votos_g'])
gdf['porcR']=100*gdf['rechazo']/(gdf['rechazo']+gdf['apruebo'])
gdf['p_vs_r']=(gdf['porcP']-gdf['porcR']);gdf.to_csv('porcentajes.csv')

for region, rdf in cdf.groupby('region'):
    cr1=rdf.comuna.values
    gdf1=gdf[gdf.index.isin(cr1)]
    gdf1.to_csv(f'cruce_R{region}.csv')
