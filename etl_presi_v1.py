from util import *

pv1=pd.read_excel('DATA/Presidencial_2017_1v.xlsx',sheet_name=None)
edf=pv1['EXTRANJERO']	# we ignore these, sorry brous
cdf=pv1['CHILE']
cdf['candidato']=cdf.Candidato.apply(lambda c: c.split()[1])
cdf.candidato=cdf.candidato.apply(lambda c:c.replace('ANTONIO','KAST'))

cdf['mesa']=['%d%s' %(row['Mesa'],row['Tipo mesa']) for _,row in cdf.iterrows()]
cdf=cdf.rename(columns={'Votos TRICEL':'votos'})
cdf=cdf.rename(columns={'Región':'region'})
cdf=cdf.rename(columns={'Comuna':'comuna','Local':'local'})
cdf=cdf[['region','comuna','local','mesa','candidato','votos']]
cdf.to_sql('etl_presi_1v',sqlite3.connect('cruce.db'))

plebi=cdf.groupby(['region','comuna','local','mesa','candidato']).sum()['votos'].reset_index()
plebi['region']=plebi.region.apply(int)
plebi['votos']=plebi.region.apply(int)

plebi=cdf.groupby(['region','comuna','local','mesa']).sum()['votos'].reset_index()
plebi=plebi.rename(columns={'votos':'total'})

for c, ccdf in cdf.groupby('candidato'):
    print(c,len(ccdf))
    plebi[c]=ccdf.groupby(['region','comuna','local','mesa']).agg({'votos':'sum'}).reset_index()['votos'].apply(int)

plebi=plebi.rename(columns={'PIÑERA':'PINERA','ENRIQUEZ-OMINAMI':'ENRIQUEZ'})
plebi['region']=plebi.region.apply(int)
plebi['total']=plebi.total.apply(int)
plebi.to_sql('presi_v1',sqlite3.connect('cruce.db'),index=False, if_exists='replace')
