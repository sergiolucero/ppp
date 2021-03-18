import glob
import sqlite3
import pandas as pd

data = {fn: pd.read_excel(fn, sheet_name=None) for fn in glob.glob('*.xlsx')}

# cruzando Plebiscito: AR+CM
con_mesa_df=data['Constitución_2020_AR.xlsx']['MESA A MESA']
con_mesa_df2=data['Constitución_2020_CM.xlsx']['MESA A MESA']
con_mesa = con_mesa_df.merge(con_mesa_df2, on=['Región','Provincia','Comuna','Circunscripción','Local','Tipo','Mesa'])

print([len(x) for x in (con_mesa_df, con_mesa_df2, con_mesa)])

con_mesa.to_csv('Plebiscito_2020_ARCM.csv', index=False)

# cruzando Presidencial: V1+V2

pre1 = data['Presidencial_2017_v1.xlsx']['CHILE'].dropna()
pre2 = data['Presidencial_2017_v2.xlsx']['CHILE'].dropna()

conn=sqlite3.connect('etl.db')
pre1.to_sql('presi_v1', conn, index=False)
pre2.to_sql('presi_v2', conn, index=False)
sql = lambda q: pd.read_sql(q, conn)

pre1.columns = [col.replace(' ','_') for col in pre1.columns]
pre2.columns = [col.replace(' ','_') for col in pre2.columns]
pre1.to_sql('presi_v1', conn, index=False, if_exists='replace')
pre2.to_sql('presi_v2', conn, index=False, if_exists='replace')

# at this stage, we need to pivot

modpre = sql('SELECT Región AS region, 
