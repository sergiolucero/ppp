import time
from util import *

com8 = sql('SELECT DISTINCT(comuna) FROM cruce_simple').values
com8 = [c[0] for c in com8]

t0=time.time()
for com in com8:
    comjson(com)
    print(com, round(time.time()-t0,2))
