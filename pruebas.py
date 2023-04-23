import db


cursor = db.toto.find({}, {'Combinaciones': False,
                           '_id': False,
                           'Reintegro': False,
                           'Fecha millon': False,
                           'Numero millon': False})

for i in cursor:
    numero = i['Numero de serie']
    tipo = i['Tipo']
    fecha = i['Fecha']
    precio = i['Precio']

    result = f' {numero[-7:]} | {tipo} | {fecha} | {precio} \N{euro sign}'

    print(result)

