import pandas as pd
df=pd.read_excel('DATA/Plebiscito_2020.xlsx')
df
df=pd.read_excel('DATA/Plebiscito_2020.xlsx',sheet_name=None)
df.keys()
df=df['resultados por mesa']
df
df.columns
df=df.drop(['llave', 'circunscripcion electoral'], axis=1)
import sqlite3
df.to_sql('plebis_propo', sqlite3.connect('cruce.db'),index=False)
df.columns=[c.replace(' ','_') for c in df.columns]
df.to_sql('plebis_propo', sqlite3.connect('cruce.db'),index=False,if_exists='replace')
df.columns
%hist -f plebi_proporciones.py
