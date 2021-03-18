from lenin import *

for level in ['R','C','L','M']:
    k=Klass(f'{level}:Presi')
    print('    LEVEL:', level, 'N=', len(k.data))
    k.train()
