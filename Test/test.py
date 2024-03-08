import cv2
import numpy as np

def hallarLinea(imagen):

    centro_x, centro_y = imagen.shape[1] // 2, imagen.shape[0] // 2
    
   
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    bordes = cv2.Canny(gris, 50, 150, apertureSize=3)


    lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

    linea_final = None
    longitud_maxima = 0


    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]

    
            dist1 = np.sqrt((x1 - centro_x)**2 + (y1 - centro_y)**2)
            dist2 = np.sqrt((x2 - centro_x)**2 + (y2 - centro_y)**2)

     
            if dist1 > dist2:
                longitud = dist1
                punto_inicial = (x1, y1)
                punto_final = (x2, y2)
            else:
                longitud = dist2
                punto_inicial = (x2, y2)
                punto_final = (x1, y1)

       
            if longitud > longitud_maxima:
                longitud_maxima = longitud
                linea_final = (punto_inicial[0], punto_inicial[1], punto_final[0], punto_final[1])

    return linea_final

image = cv2.imread("color0.jpg")


x1, y1, x2, y2 = hallarLinea(image)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_contour = None
max_area = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        max_contour = contour

if max_contour is not None:
    ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
    center = (int(x), int(y + 10))
    radius = int(radius)
    cv2.circle(image, center, radius, (0, 255, 0), 2)

  
    delta_x = x1 - x2
    delta_y = y1 - y2
    angle_rad = np.arctan2(delta_y, delta_x)
    angle_deg = np.degrees(angle_rad)


    if angle_deg < 0:
        angle_deg += 360


    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, f'Angulo: {angle_deg:.2f} grados', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

cv2.imshow("Manometro con Angulo", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
