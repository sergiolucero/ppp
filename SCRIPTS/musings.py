from util import *
df=dd.read_excel('DATA/Presidencial_2017_1v.xlsx',sheet_name='CHILE')
p1=pd.read_excel('DATA/Presidencial_2017_1v.xlsx',sheet_name='CHILE')
p1.iloc[0]
p1['Candidato']=p1.Candidato.apply(lambda c: c.split()[1])
p1=p1.dropna()
p1['Candidato']=p1.Candidato.apply(lambda c: c.split()[1])
p1=p1.drop([c for c in p1.columns if 'Circ' in c],axis=1)
p1.iloc[0]
p1=p1.drop(['Provincia','Distrito','Electores','Nro.voto'],axis=1)
p1=p1.rename(columns={'Votos TRICEL':'votos'})
p1.to_sql('p1',sqlite3.connect('presi.db'),index=False)
!ls -l
p1.to_sql('p1',sqlite3.connect('cruce.db'),index=False)
!ls -l *db
!rm presi.db
sql('SELECT Candidato, COUNT(*) AS N FROM p1v GROUP BY Candidato')
sql('SELECT * FROM sqlite_master')
sql('SELECT Candidato, COUNT(*) AS N FROM p1 GROUP BY Candidato')
cand=_.Candidato.values
cand
xq=','.join([f"(SELECT votos AS votos_{c} FROM p1 WHERE Candidato='{c}')" for c in cand])
xq
odf=pd.DataFrame()
p1.iloc[0]
for cand,cdf in p1.groupby('Candidato'):
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    odf=odf.append(cdf)
len(odf)
odf=pd.DataFrame()
ix=0
for cand,cdf in p1.groupby('Candidato'):
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    if ix==0:
        odf=cdf.rename(columns={'votos':f'votos_{cand}'})
        ix=1
    else:
        odf[f'votos_{cand}']=cdf[f'votos_{cand}']
len(odf)
odf.iloc[1]
for cand,cdf in p1.groupby('Candidato'):
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    if ix==0:
        odf=cdf[[cdf.columns[:6]]]
        ix=1
    odf[f'votos_{cand}']=cdf[f'votos_{cand}']
len(odf)
odf.iloc[1]
ix
ix=0
for cand,cdf in p1.groupby('Candidato'):
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    if ix==0:
        odf=cdf[[cdf.columns[:6]]]
        ix=1
    odf[f'votos_{cand}']=cdf[f'votos_{cand}']
ix
for cand,cdf in p1.groupby('Candidato'):
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    if ix==0:
        odf=cdf[[list(cdf.columns[:6])]]
        ix=1
    odf[f'votos_{cand}']=cdf[f'votos_{cand}']
cdf.columns[:6]
list(cdf.columns[:6])
cdf.columns
c6=cdf[cdf.columns[:6]]
c6.head()
for cand,cdf in p1.groupby('Candidato'):
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    if ix==0:
        odf=cdf[list(cdf.columns[:6])]
        ix=1
    odf[f'votos_{cand}']=cdf[f'votos_{cand}']
odf.head()
%hist
cdf.head()
for cand,cdf in p1.groupby('Candidato'):
    print(f'votos_{cand}')
    cdf[f'votos_{cand}']=cdf['votos'].apply(int)
    if ix==0:
        odf=cdf[list(cdf.columns[:6])]
        ix=1
    odf[f'votos_{cand}']=cdf[f'votos_{cand}']
odf.iloc[0]
%hist -f musings.py
