import numpy as np
import cv2
from time import gmtime, strftime

# HairCascade
faceCascade = cv2.CascadeClassifier(
    'cascade/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('cascade/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('cascade/haarcascade_smile.xml')

video = input("Nome do Video: ")

str0 = "video/"
str1 = video
str2 = ".mp4"

if video: 
    vid = str0 + str1 + str2
else:
    vid = 0

cap = cv2.VideoCapture(vid) 

cap.set(3, 1920)  # set Width
cap.set(4, 1080)  # set Heightt

# Loop para Dar Continuidade a Imagem
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta Face
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Mostra Face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detecta Olhos
        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(5, 5),
        )

        # Mostra Olhos
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 2)

        # Detecta Boca
        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.5,
            minNeighbors=15,
            minSize=(25, 25),
        )

        # Mostra Boca
        for (xx, yy, ww, hh) in smile:
            cv2.rectangle(roi_color, (xx, yy),
                          (xx + ww, yy + hh), (0, 255, 0), 2)

        # Mostra Video
        cv2.imshow("Recognize With OpenCV", frame)

    # Verifica Qual Tecla Foi Pressionada Caso Seja Esc(27) Ele Cai Fora
    k = cv2.waitKey(30) & 0xff
    if k == ord('s'):
        cv2.imwrite('img/image-' + strftime("%Y-%m-%d %H.%M.%S") + '.jpg', frame)
    elif k == 27:
        break

cap.release()
cv2.destroyAllWindows()
