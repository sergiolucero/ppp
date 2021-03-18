ls DATA
ls DATA/plebiscito/
import pandas as pd
df=pd.read_csv('DATA/plebiscito/PLEB_2020_CPE_UDLA.csv')
df
df.iloc[0]
ls
ls DATA
pledf=pd.read_excel('DATA/Plebiscito_2020.xlsx', sheet_name=None)
pledf
len(pledf)
pledf.keys()
ple=pledf['resultados por mesa']
ple
ple.columns
ls
ls SCRIPTS/
!cat SCRIPTS/etl1_cruce_datos.py
ls
ls SCRIPTS
!cp SCRIPTS/Plebiscito_2020_ARCM.csv DATA
ple=pd.read_csv('DATA/Plebiscito_2020_ARCM.csv')
ple
ple
ple.iloc[0]
ple.groupby('Región').sum()
_.sum()
ple.corr()
ple.columns
ple.columns=[c.lower().replace('ó','o') for c in ple.columns]
ple.to_sql('plebi_full', sqlite3.connect('cruce.db'), index=False)
import sqlite3
ple.to_sql('plebi_full', sqlite3.connect('cruce.db'), index=False)
ple.head()
lcdf = ple[ple.comuna=='LAS CONDES']
lcdf
lcdf.corr()
ple=ple[[c for c in ple.columns if ('nulos' not in c) and ('blancos' not in c)]]
ple.columns
ple.to_sql('plebi_full', sqlite3.connect('cruce.db'), index=False, if_exists='replace')
sql = lambda q: pd.read_sql(q, sqlite3.connect('cruce.db'))
sql('SELECT * FROM plebi_full LIMIT 10')
ple=ple[[c for c in ple.columns if ('total' not in c) and ('blancos' not in c)]]
ple.to_sql('plebi_full', sqlite3.connect('cruce.db'), index=False, if_exists='replace')
sql('SELECT * FROM plebi_full LIMIT 10')
lcdf = ple[ple.comuna=='LAS CONDES']
lcdf
lcdf.sum()
%hist -f cruce_correcto_plebiscitos.py
