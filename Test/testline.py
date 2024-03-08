import cv2
import numpy as np


imagen = cv2.imread('color1.jpg')

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

gris = cv2.GaussianBlur(gris, (5, 5), 0)

bordes = cv2.Canny(gris, 50, 150, apertureSize=3)

cv2.imshow('Lineas ', bordes)

lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=3)


if lineas is not None:
    for linea in lineas:
        x1, y1, x2, y2 = linea[0]
        print(f"x1:{x1}\ny1:{y1}\nx2:{x2}\ny2:{y2}")
        cv2.line(imagen, (x1, y1), (x2, y2), (0, 255, 0), 3)

cv2.imshow('Lineas detectadas', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
