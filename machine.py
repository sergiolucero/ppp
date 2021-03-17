# we can now attempt to apply basic ML to predict PineraV2!
from util import *

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import eli5
from eli5 import show_weights, show_prediction, explain_weights_df
from eli5 import explain_prediction, explain_prediction_xgboost

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV
from tpot import TPOTRegressor
from xgboost import XGBRegressor

import seaborn as sns
import matplotlib.pyplot as plt
#############################
cols = ['votos_PINERA', 'votos_KAST', 'votos_GOIC', 'votos_ENRIQUEZ',
       'votos_GUILLIER', 'votos_NAVARRO', 'votos_SANCHEZ', 'votos_ARTES']
#############################
def linplot(pdf, bracket=None):
    fig, ax = plt.subplots(1, figsize=(20,8))
    p = sns.heatmap(pdf, annot=True, fmt='.2f', annot_kws={'size':18, 'weight': 'bold'}, cmap='RdYlGn');
    title = 'Influencia votos primera vuelta sobre voto Piñera 2da vuelta' 
    if bracket is not None:
        title += f'[{bracket}]'
    
    p.set_title(title, size=18);

def trainer(presi):
    if presi is None:
        presi = sql('SELECT * FROM cruce_presi')

    feats = presi[[c for c in presi.columns if 'votos_' in c]]
    labels = presi['PineraV2']
    train_features, test_features, train_labels, test_labels = train_test_split(feats, labels, test_size = 0.25)

    Regressor = RandomForestRegressor
    #Regressor = LinearRegression
    #Regressor = RidgeCV
    nRuns = 2
    for nRun in range(1,nRuns):
        if Regressor == RandomForestRegressor:
            rf = Regressor(n_estimators = 500)
        else:
            rf = Regressor()
        rf.fit(train_features, train_labels)
        print('RUN:',nRun,round(rf.score(test_features, test_labels),4), end=':')

    #print(rf.coef_)   # only linear, else appli eli5
    return rf

def train_xgb(data, train_cols, pred_col):
    
    X = data[train_cols];    y = data[pred_col]
    
    X_train, X_test, y_train, y_test = train_test_split(feats, labels, 
                                                        test_size = 0.2)

    xgb_clf = XGBRegressor(verbosity=verbosity, n_estimators = n_estimators)

    return {'xgb': xgb_clf, 'Xtest': X_test, 'ytest': y_test}
    
def xgtrain(presi, verbosity = 0, n_estimators=100):
    
    feats = presi[[c for c in presi.columns if 'votos_' in c][1:]]
    
    newly = False
    if newly:
        presi['DeltaPi'] = presi['PineraV2']-presi['votos_PINERA']
        labels = presi['DeltaPi']
        feats = feats.drop(['votos_PINERA'], axis=1)
        #print(feats.columns)
    else:
        labels = presi['PineraV2']
    # predicting PV2 from XV1, including Piñera!
    TEST_SIZE = 0.30 if len(feats)<10 else 0.25    
    X_train, X_test, y_train, y_test = train_test_split(feats, labels, 
                                                        test_size = TEST_SIZE)

    xgb_clf = XGBRegressor(verbosity=verbosity, n_estimators = n_estimators)
    xgb_clf.fit(X_train, y_train)

    #print('XGB:', round(xgb_clf.score(X_test, y_test),4))

    return xgb_clf, X_test, y_test, X_train, y_train

def regdata(region):
    #return rsql(region)    # ahora viene a nivel de COMUNA.. is that enough?
    NIVEL = 'comuna, local'
    candis = sql('SELECT * FROM presi_v1 LIMIT 1').columns[4:]
    csql = ', '.join(f'SUM({c}) AS votos_{c}' for c in candis)

    #print('CSQL:', csql)
    pre_RC1 = sql(f'SELECT {NIVEL}, {csql} FROM presi_v1 WHERE region={region} GROUP BY {NIVEL}')
    pre_RC2 = sql(f'SELECT {NIVEL}, SUM(votos_g) AS GuillierV2, SUM(votos_p) AS PineraV2 FROM presi  WHERE region={region} GROUP BY {NIVEL}')
    #print(len(pre_RC1), len(pre_RC2))
    # presi: RCLM+votos_g+votos_p, plebi: RCLM+apruebo+rechazo

    data = pre_RC1.merge(pre_RC2)
    data['G2m_G1pSanchez'] = data['GuillierV2']-(data['votos_SANCHEZ']+data['votos_GUILLIER'])
    data['G2m_G1p_MeoSanchez'] = data['GuillierV2']-(data['votos_SANCHEZ']+data['votos_GUILLIER']+data['votos_ENRIQUEZ'])
    data['P2m_P1pKast'] = data['PineraV2']-(data['votos_PINERA']+data['votos_KAST'])
    # data['region'] = region
    return data

def regtrain(region, show=True):

    data = regdata(region)
    data = data.drop(['votos_Blancos','votos_Nulos'], axis=1)   # no sirven!
    xgb, X_test, y_test, X_train, y_train = xgtrain(data)
    xscore = round(xgb.score(X_test, y_test),4)
    print('REGION:', region, 'score:', xscore, end=',')   # move print, include XGB.score!
    
    if show:
        #out = show_weights(xgb, feature_names = list(X_test.columns))
        out = eli5.explain_weights_df(xgb, feature_names = list(X_test.columns))
    else:
        #out = explain_weights_df(xgb, feature_names = list(X_test.columns)), xscore
        out = explain_prediction_xgboost(xgb, X_test.iloc[0])    
    xout = {r': (X_test, y_test), 
            'score': xscore, 'out': out, 'xgb': xgb}  # add y_test
    #return show_prediction(xgb_clf, X_test.iloc[0], show_feature_values=True)
    return xout

def reg_tpot():   # why the negative results?? 
    tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)
    tpot.fit(train_features, train_labels)
    print(tpot.score(test_features, test_labels))
    tpot.export('tpot_election_pipeline.py')


def regional_data():
    rexs = {}
    xscores = []
    for reg in range(1,16):  # no hay Ñuble, iñor!!
        rdata = regtrain(reg, False)  
        rexs[reg] = rdata[0]
        xscores.append(rdata[1])

    rdf = 100*rexs[1]            # add scores
    for reg in range(2,16):
        rdf = rdf.merge(100*rexs[reg], on='feature')

    rdf['feature'] = rdf.feature.apply(lambda f: f.split('_')[1].replace('votos',''))

    rdf.columns=['candidato']+[f'R{ix}' for ix in range(1,16)]

    return rdf

def tcut(x):
    thres = 0.01
    return x if x>=thres else 0

def iplotter():
    pdf = pd.DataFrame(columns=cols); xts = {}
    for region in range(1,16):
        xts[region] = regtrain(region, True)
        #dX0,dy0 = xts[region]['train_data'];    dtX0,dty0 = xts[region]['test_data']
        #dX0 = dX0.drop(['votos_NAVARRO','votos_ARTES','votos_PINERA'], axis=1); dtX0 = dtX0.drop(['votos_NAVARRO','votos_ARTES','votos_PINERA'], axis=1)
        #lr = RandomForestRegressor();     lr.fit(dX0,dy0)
        #print('REGION:', region, round(100*lr.score(dtX0,dty0),1), end=',')
        #print(str(dict(zip(dtX0.columns,[round(x,3) for x in lr.coef_]))))
        xo = xts[region]['out'];    vals = [100*tcut(xo[xo.feature==c]['weight'].values[0]) for c in cols]  # threshold cutoff
        pdf.loc[region-1] = vals
        #pdf = pdf.append(pd.DataFrame(dict(zip(dtX0.columns,[round(x,3) for x in lr.coef_])),index=[region]))
        #pdf = pdf.append(pd.DataFrame(dict(zip(dtX0.columns,[round(x,3) for x in lr.feature_importances_])),index=[region]))
    pdf.index = [idx+1 for idx in pdf.index]
    return pdf