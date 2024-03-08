
import cv2
import numpy as np
import math


class Manometro():
    def __init__(self):
        self.valor = []
        self.valorProm=0
        self.angle_deg_prom=352
        self.count = 0
        self.center=[]
        self.radio=0

    def HallarManometro(self,frame):
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY)
            cv2.imshow('Imagen ', thresh)
            if(self.count<=20):
                self.DibujarCirculo(thresh)
                self.count+=1
            
            cv2.circle(frame, self.center, self.radio, (0, 255, 0), 2)

            try:
                    aux = self.extraerContornos(frame,self.center)
                    x1, y1, x2, y2 = aux
                    angle_deg = round(math.degrees(math.atan2(x1 - x2, y1 - y2)))
                    if angle_deg < 0:
                        angle_deg += 360
                    valor_minimo = 352
                    valor_maximo = 15

                    self.valor.append(angle_deg)
            except:
                    print("Shale")

                #cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            if(len(self.valor)==5):
                    self.angle_deg_prom = sum(self.valor)/len(self.valor)
                    valor_normalizado = (self.angle_deg_prom - valor_minimo) / (valor_maximo - valor_minimo)
                    self.valorProm = valor_normalizado * 300
                    if(self.valorProm<0):
                        self.valorProm=0
                    self.valor=[]

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f'Angulo: {self.angle_deg_prom:.2f} grados', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Valor: {round(self.valorProm)} ', (10, 60), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            return frame
            
    def extraerContornos(self,img,centro):
            gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gris = cv2.GaussianBlur(gris, (5, 5), 0)
            bordes = cv2.Canny(gris, 50, 150, apertureSize=3)
            lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
            centro_x, centro_y = centro
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
   
    def DibujarCirculo(self,thres):
            contours, _ = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_contour = None
            max_area = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = contour

            if max_contour is not None:
                ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
                self.center = (int(x), int(y))
                self.radio = int(radius)
                
                
