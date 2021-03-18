from util import *

cdf=sql('SELECT * FROM cruce1')
xdf=cdf.groupby(['region','comuna','local']).sum()
regcomloc=xdf.index[0]

pre= lambda rcl: sql(f"SELECT mesa, votos_g, votos_p FROM presi WHERE region={rcl[0]} AND comuna='{rcl[1]}' AND local='{rcl[2]}'")
ple= lambda rcl: sql(f"SELECT mesa, apruebo, rechazo FROM plebi WHERE region={rcl[0]} AND comuna='{rcl[1]}' AND local='{rcl[2]}'")
