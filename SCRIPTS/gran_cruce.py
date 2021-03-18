from util import sql

cdf=sql('SELECT * FROM (SELECT * FROM plebi2) AS ple, (SELECT * FROM presi) AS pre \
	WHERE ple.region=pre.region AND ple.comuna=pre.comuna AND ple.local=pre.local AND pre.mesa=ple.mesa')
