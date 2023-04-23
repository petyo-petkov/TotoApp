import cv2
from pyzbar.pyzbar import decode


class Captura:
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
