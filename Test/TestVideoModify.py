import cv2
import Definitivo.Manometro as Manometro

video_path = r'C:\Users\ariel\OneDrive\Documentos\proyecto personales\Reconocimiento Manometro\Media\Pruebas.mp4'
cap = cv2.VideoCapture(video_path) 
#cap = cv2.VideoCapture(0)

manometro = Manometro.Manometro()

while cap.isOpened(): 
    ret, frame = cap.read()
    if not ret:
        break

    frame= manometro.HallarManometro(frame)

    cv2.imshow('Manometro con Angulo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
