import pandas as pd
from sqlalchemy import create_engine

user='dbmasteruser'
passwd='RyMp0*DGtVWDc}Ew^*)I#T!Gm4Z%#9|9'
#endpoint='ls-daef2eb550393f2c3554c8dc0e02aa8033648082.cxuluyjslj42.us-east-1.rds.amazonaws.com'
endpoint='ls-95140a2bfdab01efb730add5d0c2cd92342f55eb.cxuluyjslj42.us-east-1.rds.amazonaws.com'

eng_url = f'postgresql+psycopg2://{user}:{passwd}@{endpoint}:5432/postgres'
engine = create_engine(eng_url)
conn = engine.raw_connection()

psql = lambda q: pd.read_sql(q, con=engine)

def pstore(data,tablename):
    print('INSERTING %d records' %len(data)) 
    chunksize = max(len(data)/10,10000)
    nchunks = int(len(data)/chunksize)
    for ix in range(nchunks+1):
        chunk = data.iloc[ix*chunksize:(ix+1)*chunksize]
        print(ix,len(chunk))
        chunk.to_sql(tablename, con=engine, index=False, 
                    if_exists='replace' if ix==0 else 'append')


# add DROP TABLE
# SHOW_TABLES
