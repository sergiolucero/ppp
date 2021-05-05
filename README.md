## Proyecto PPP: Presidenciales 2017 + Plebiscito 2021.

Este repositorio contiene código en Python, archivos de datos en Excel y mapas generados en HTML para intentar responder la pregunta: 
¿dónde está el voto recuperable de Piñera que se fue al Apruebo? Se obtuvieron los resultados nacionales a nivel de mesa para la elección
presidencial de 2017 (1ra y 2da vuelta) y del referendo apruebo/rechazo 2021. Es importante destacar que los cruces no pueden hacerse de 
forma evidente entre mesas pues en el período transcurrido entre ambas instancias, muchas mesas fueron fusionadas o eliminadas, e incluso
se crearon locales nuevos de votación. Aun así, el código que aquí presentamos permite detectar aquellas comunas donde más se observó la diferencia

###Presidencial: (Piñera,Guillier, Otros)
###Plebiscito: (Apruebo/Rechazo)(Mixta/Constituyente)

Entre otros resultados, utilizando algoritmos de regresión con machine learning, 
detectamos que en muchas instancias, el peso del voto en primera presidencial por candidatos como Goic y MEO, que no necesariamente se traspasaron a Guillier en 2da.

# Cómo montar el Servicio
Los resultados obtenidos, así como los mapas generados, se visualizan utilizando un servidor Flask, que gracias a Python puede correr tanto en un Mac/PC que contenga
todo el código, como en una máquina asignada en un servicio cloud como Amazon Webservices. Los puntos de acceso principales son:

/comuna/<region_comuna>:    permite visualizar los locales de votación (con diferencia relevante) de una comuna (ej: /comuna/13_VITACURA)
/sql:                       permite consultar la base de datos utilizando lenguaje SQL
/regdata:                   resumen regional de resultados
