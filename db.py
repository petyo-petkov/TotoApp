from pymongo import MongoClient

cliente = MongoClient(
    "mongodb://localhost:27017"
)

db = cliente.pruebas
toto = db.pruebas
gastos = db.gastado

