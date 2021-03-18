from util import *

candis=sql('SELECT DISTINCT(Candidato) FROM p1').values
candis=[c[0] for c in candis]

cdf=lambda c: sql(f"SELECT * FROM p1 WHERE Candidato='{c}'")

df=cdf('GOIC')
df=df.rename(columns={'votos':'GOIC'})
df=df.drop('Candidato',axis=1)

for cand in candis[1:]:    # incluye nulos y blancos
    xdf = cdf(cand)
    xdf=xdf.rename(columns={'votos':cand})
    xdf=xdf.drop('Candidato',axis=1)
    df = df.merge(xdf)
    print(cand, len(df.columns))

for col in ['Región']+list(df.columns[-10:]):
    df[col]=df[col].apply(int)

# merge mesa
df['mesa'] = df['Mesa'].apply(int).apply(str) + df['Tipo mesa']
df = df.drop(['Mesa','Tipo mesa'], axis=1)
df = df.rename(columns={'Región':'region', 'Comuna':'comuna', 'Local':'local'})

df = df[list(df.columns[:3])+['mesa']+list(df.columns[5:-1])]
df.to_sql('presi_v1',sqlite3.connect('cruce.db'),index=False, if_exists='replace')
