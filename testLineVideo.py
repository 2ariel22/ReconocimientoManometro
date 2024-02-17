import cv2
import numpy as np

cap = cv2.VideoCapture(1)
frame2=None
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Imagen sin procesar', frame)
    try:
                
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gris = cv2.GaussianBlur(gris, (5, 5), 0)

        bordes = cv2.Canny(gris, 50, 150, apertureSize=3)

        #cv2.imshow('Lineas ', bordes)

        lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=3)

        if lineas is not None:
                for linea in lineas:
                    x1, y1, x2, y2 = linea[0]
                    print(f"x1:{x1}\ny1:{y1}\nx2:{x2}\ny2:{y2}")
                    frame2 = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
               
                    
    except:
        print("Shale")

    cv2.imshow('Manometro con Angulo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
