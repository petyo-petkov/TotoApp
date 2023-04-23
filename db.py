from pymongo import MongoClient

cliente = MongoClient(
    "mongodb+srv://loto:loto@loto.tolwpbn.mongodb.net/?retryWrites=true&w=majority"
)

db = cliente.pruebas
toto = db.pruebas
gastos = db.gastado

