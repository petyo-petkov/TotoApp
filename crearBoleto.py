from captura import Captura

datos = Captura.myData


class CrearBoletoJson:
    @staticmethod
    def crear_json():
        precio: float
        numero_millon: str
        fecha_millon: str

        tipo: str = datos[1]
        num_serie: int = datos[0][2:]
        fecha: str = datos[2][5:12]
        combinaciones: str = datos[4].split('.')
        del combinaciones[0]
        reintegro: str = datos[6][2:]

        match tipo:
            case 'P=1':
                tipo = "Primitiva"
                precio = int((1 * len(combinaciones) * int(datos[2][-1])))
                numero_millon = None
                fecha_millon = None
            case 'P=2':
                tipo = "Bonoloto"
                precio = float((0.5 * len(combinaciones) * int(datos[2][-1])))
                numero_millon = None
                fecha_millon = None
            case 'P=7':
                tipo = "Euromillones"
                precio = float((2.5 * len(combinaciones) * int(datos[2][-1])))
                reintegro = None
                numero_millon = datos[6][21:]
                fecha_millon = datos[6][11:18]
            case 'P=6':
                tipo = "Loteria"
                fecha = datos[0][:2]
                precio = 3
                combinaciones = datos[0][9:14]
                reintegro = None
                numero_millon = None
                fecha_millon = None
            case 'P=10':
                tipo = "Loteria"
                fecha = datos[0][:2]
                combinaciones = datos[0][9:14]
                reintegro = None
                numero_millon = None
                fecha_millon = None
                precio = 3
            case 'P=5':
                tipo = "Loteria"
                fecha = datos[0][:2]
                precio = 6
                combinaciones = datos[0][9:14]
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
        # boleto = json.dumps(boleto, indent=4, ensure_ascii=False)  # crea el boleto en formato string

        return boleto

