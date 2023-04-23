import cv2
from pyzbar.pyzbar import decode
import db
from datetime import datetime


class AddBoleto:
    @staticmethod
    def captura_qr():
        cap = cv2.VideoCapture(0)
        success = True
        while success:
            # leyendo y decodificando la img.
            success, img = cap.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                myData = myData.split(';')
                # preparando myData para los decimos de la loteria
                if len(myData) == 1:
                    myData = f'{myData[0][2:]} P={myData[0][0]} {0} {0} {0} {0} {0} {0} {0}'
                    myData = myData.split(' ')

                print(myData)
                success = False

            # mostrando los resultados
            cv2.namedWindow("Scann", cv2.WINDOW_NORMAL)  # para mostrar ventana mas pequieña.
            cv2.imshow('Scann', img)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

        precio: float
        numero_millon: str
        fecha_millon: str

        tipo: str = myData[1]
        num_serie: str = myData[0][2:]
        fecha: str = myData[2][5:12]
        combinaciones: str = myData[4].split('.')
        del combinaciones[0]
        reintegro: str = myData[6][2:]

        match tipo:
            case 'P=1':
                tipo = "Primitiva"
                precio = int((1 * len(combinaciones) * int(myData[2][-1])))
                numero_millon = None
                fecha_millon = None
            case 'P=2':
                tipo = "Bonoloto"
                precio = float((0.5 * len(combinaciones) * int(myData[2][-1])))
                numero_millon = None
                fecha_millon = None
            case 'P=7':
                tipo = "Euromillones"
                precio = float((2.5 * len(combinaciones) * int(myData[2][-1])))
                reintegro = None
                numero_millon = myData[6][21:]
                fecha_millon = myData[6][11:18]
            case 'P=6':
                tipo = "Loteria"
                fecha = myData[0][:2]
                precio = 3
                combinaciones = myData[0][9:14]
                reintegro = None
                numero_millon = None
                fecha_millon = None
            case 'P=10':
                tipo = "Loteria"
                fecha = myData[0][:2]
                combinaciones = myData[0][9:14]
                reintegro = None
                numero_millon = None
                fecha_millon = None
                precio = 3
            case 'P=5':
                tipo = "Loteria"
                fecha = myData[0][:2]
                precio = 6
                combinaciones = myData[0][9:14]
                reintegro = None
                numero_millon = None
                fecha_millon = None

        boleto = {
            "Numero de serie": num_serie,
            "Tipo": tipo,
            "Fecha": fecha,
            "Precio": precio,
            "Combinaciones": combinaciones,
            "Reintegro": reintegro,
            "Numero millon": numero_millon,
            "Fecha millon": fecha_millon

        }

        # comprobando si el boletos existe en la DB y lo añadimos en caso que no.
        if boleto['Numero de serie'] not in db.toto.distinct('Numero de serie'):
            db.toto.insert_one(boleto)
            print("Boleto añadido correctamente")
        else:
            print("Ya existe este boleto")

    @staticmethod
    def sum_precios() -> None:
        # sumando los precios de los boletos
        cursor = db.toto.find({})
        suma = 0
        for i in cursor:
            precios = float(i["Precio"])
            suma = suma + precios

        gastado = {"gastado": suma,
                   "date": datetime.utcnow()}

        # actualizando la suma de los boletos
        try:
            old = db.gastos.find_one()
            new = {"$set": gastado}
            db.gastos.update_one(old, new)

        except:
            db.gastos.insert_one(gastado)


