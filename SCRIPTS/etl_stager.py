from util import *

#tables = {'cruce_PrePle'}

for table, fcn in etl2.items():
    tdf = fcn()
    tdf.to_sql(table, conn2, index=False, if_exists='replace')
    print('WROTE:', len(tdf), 'records to table', table)
