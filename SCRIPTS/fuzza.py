from util import *
from operator import itemgetter
from fuzzywuzzy import fuzz
import pickle

dreg = {v:k for k,v in pickle.load(open('regiones.pk','rb')).items()}

equiv = []

for region in range(1,17):
    nreg = dreg[region]
    one_pre=[x[0] for x in sql(f'SELECT DISTINCT(local) FROM presi WHERE region={region}').values]

    if region==6:   # Dudu
        one_ple=[x[0] for x in sql(f"SELECT DISTINCT(local) FROM plebi WHERE region LIKE '{nreg[:10]}%'").values]
    else:
        one_ple=[x[0] for x in sql(f"SELECT DISTINCT(local) FROM plebi WHERE region='{nreg}'").values]
    print(region, nreg)

    for prelo in one_pre:
        scores=sorted([(plelo, fuzz.ratio(prelo,plelo)) for plelo in one_ple], key=itemgetter(1))
        #print(prelo, scores[-1])
        equiv.append([prelo, scores[-1][0],scores[-1][1]])

edf=pd.DataFrame(equiv, columns=['pre','ple','fw'])
print(edf.describe())
