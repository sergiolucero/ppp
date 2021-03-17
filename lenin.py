# lenin knows
from util import *
from machine import *

class Klass():

    def __init__(self, geo_elec):
        self.geo_elec = geo_elec
        self.geo = self.geo_elec.split(':')[0]       # nivel geográfico: región, comuna, local, mesa
        self.elec = self.geo_elec.split(':')[1]      # nivel eleccionario: presiv1, presiv2, plebi

        LEVELS = {
                    'R': 'region',                    'C': 'region, comuna',
                    'L': 'region, comuna, local',                    'M': 'region, comuna, local, mesa',
                    }
                    
        TABLES = {'Presi': ('presi_v1','presi_v2')}    
        COLUMNS = {'Presi': [('ENRIQUEZ', 'GOIC', 'GUILLIER', 'KAST', 'NAVARRO', 'PINERA', 'SANCHEZ', 'votos_g'), 'votos_p'],
        }
        #OUT: 'ARTES', 'Blancos','Nulos', 

        self.level = LEVELS[self.geo] 
        self.tables = TABLES[self.elec]
        self.columns = COLUMNS[self.elec]
        
        self.t1 = sql(f'SELECT * FROM {self.tables[0]}')
        self.t2 = sql(f'SELECT * FROM {self.tables[1]}')
        
        self.data = self.t1.merge(self.t2)

    def train(self):
        feat_cols, obj_col = self.columns
        self.xtrain = train_xgb(self.dat, feat_cols, obj_col)
        print('TRAINED!')
#klass = Klass('M:Presi')  # mesas PresiV1 vs PresiV2
