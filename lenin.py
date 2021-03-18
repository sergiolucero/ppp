# lenin knows
from util import *
from machine import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import eli5

class Klass():

    def __init__(self, geo_elec):
        self.geo_elec = geo_elec
        self.geo = self.geo_elec.split(':')[0]       # nivel geográfico: región, comuna, local, mesa
        self.elec = self.geo_elec.split(':')[1]      # nivel eleccionario: presiv1, presiv2, plebi

        LEVELS = {
                    'R': 'region',                    'C': 'region, comuna',
                    'L': 'region, comuna, local',                    'M': 'region, comuna, local, mesa',
                    }
                    
        TABLES = {
            'Presi': ('presi_v1','presi_v2'),    
            'PrePle': ('presi_v1','plebi'),   
            'PPP': ('presi_v1','presi_v2','plebi'),   
                }
        
        COLUMNS = {
            'Presi': [['ENRIQUEZ', 'GOIC', 'GUILLIER', 'KAST', 'NAVARRO', 'PINERA', 'SANCHEZ'], 'votos_p'],
            'PrePle': [['ENRIQUEZ', 'GOIC', 'GUILLIER', 'KAST', 'NAVARRO', 'PINERA', 'SANCHEZ'], 'apruebo'],
            'PPP': [['ENRIQUEZ', 'GOIC', 'GUILLIER', 'KAST', 'NAVARRO', 'PINERA', 'SANCHEZ'], ('votos_p','apruebo')],
        }
        #OUT: 'ARTES', 'Blancos','Nulos', 'votos_g'

        self.level = LEVELS[self.geo] 
        self.last_level = self.level.split(',')[-1]
        self.tables = TABLES[self.elec]
        self.columns = COLUMNS[self.elec]
        self.feats, self.label = self.columns
        cols1 = ', '.join([f'SUM({c}) AS {c}' for c in self.feats])
        cols2 = ', '.join([f'SUM({c}) AS {c}' for c in [self.label]])

        self.t1 = sql(f'SELECT {self.level}, {cols1} FROM {self.tables[0]} GROUP BY {self.level}')
        self.t2 = sql(f'SELECT {self.level}, {cols2} FROM {self.tables[1]} GROUP BY {self.level}')
        print('LENS:', len(self.t1),len(self.t2))
        self.data = self.t1.merge(self.t2)
        if len(self.tables)==3:
            self.t3 = sql(f'SELECT {self.level}, {cols2} FROM {self.tables[2]} GROUP BY {self.level}')
            self.data = self.data.merge(self.t3)
        
        if self.elec == 'Presi':
            self.data['delta_Pinera'] = self.data['votos_p'] - self.data['PINERA']   # nu
        self.data.to_sql(f'cruce_{self.geo}_{self.elec}', mconn, if_exists='replace')   # should be ignore: if not exists...
        ## should store to STAGE_TWO.db
        
    def train(self):
        feat_cols, obj_col = self.columns
        feat_cols = [c for c in feat_cols if c!='PINERA']  # nu
        if self.elec == 'Presi':
            self.obj_col = 'delta_Pinera'                           # nu
        else:
            self.obj_col = 'apruebo'
            
        self.xtrain = train_xgb(self.data, feat_cols, self.obj_col)
        
    def explain(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
        fig.suptitle(f'Resultados a nivel de {self.last_level}', size=18);
        
        data = self.xtrain
        xgb = data['xgb']
        
        ypred = xgb.predict(data['Xtest'])
        ytest=data['ytest']; ytrain=data['ytrain']
        Xtest=data['Xtest']; Xtrain = data['Xtrain']
        
        df = pd.DataFrame(dict(pred=ypred,real=ytest))
        pred_xtrain = xgb.predict(Xtrain)
        df2 = pd.DataFrame(dict(pred=pred_xtrain,real=ytrain))
        df = df.append(df2)   # full set for plotting
        
        #wdf = eli5.explain_weights_df(xgb, feature_names = list(Xtest.columns))
        wdf = eli5.explain_weights_xgboost(xgb, Xtrain)
        ow
        sns.scatterplot(data=df,x='real',y='pred',ax=ax1);
        xmin, xmax = df['real'].min(),df['real'].max()
        ax1.plot([xmin,xmax],[xmin,xmax],'k-')
        sns.histplot(data=wdf,x='weight',y='feature',ax=ax2, fill=False);

#klass = Klass('M:Presi')  # mesas PresiV1 vs PresiV2
