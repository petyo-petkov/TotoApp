from pymongo import MongoClient

cliente = MongoClient(
    "http://localhost/127.0.0.1"
)

db = cliente.pruebas
toto = db.pruebas
gastos = db.gastado

