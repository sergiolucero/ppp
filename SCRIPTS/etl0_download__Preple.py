import wget

files = {
        'Presidencial_2017_v1.xlsx': 'https://www.servel.cl/wp-content/uploads/2018/03/Resultados_Mesa_PRESIDENCIAL_Tricel_1v.xlsx',
        'Presidencial_2017_v2.xlsx': 'https://www.servel.cl/wp-content/uploads/2018/03/Resultados_Mesa_PRESIDENCIAL_Tricel_2v.xlsx',
        #'Constitución_2020_AR.xlsx': 'https://tribunalcalificador.cl/wp-content/uploads/2020/12/RESULTADOS-OFICIALES-PLEBSICITO-CONSTITUCION-2020-SITIO-WEB.xlsx',
        'Constitución_2020_CM.xlsx': 'https://tribunalcalificador.cl/wp-content/uploads/2020/12/RESULTADOS-OFICIALES-PLEBISCITO-TIPO-DE-ORGANO-2020-SITIO-WEB.xlsx'
        }  # note el TRICEL también tiene Presi2017,... hasta Plebiscito1988

for local, remote in files.items():
    print('DOWN:', local)
    wget.download(remote, local)

# PROBLEMS: Const_AR
