# -*- coding: utf-8 -*-

import argparse
import os
import sys
from collections import deque
import cv2
import imutils
import numpy as np
import random
import time
from pygame import mixer


cam = cv2.VideoCapture(0)
#print 'horizontal =', cam.get(3), 'vertical =', cam.get(4)

# Estructura para mantener una lista de ubicaciones
# nos permitirá dibujar el "contrail" de la pelota como su seguimiento
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])

centroPantalla = (215, 80)

#Funcion para invertir la imagen
def invertirImagen(img):
    return cv2.flip(img, 1)

#Funcion para convertir imagen a HSV
def convertirHSV(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
def img(img1,img2,xpos,ypos):
    rows2,cols2,channels2 = img2.shape
    rows1,cols1,channels1 = img1.shape
    print (str(rows2)+'x'+str(rows1))
    aux = np.zeros((rows2, cols2, 3), dtype = "uint8")
    for i in range(rows1):
        for j in range(cols1):
            aux[xpos+i,ypos+j]=img1[i,j]
    return aux
#Funciones de erode y dilate para eliminar el ruido
def transformacionesMorfologicas(mascara):
    kernel = np.ones((5, 5), "uint8")
    mascaraR = cv2.erode(mascara, kernel, iterations=2)
    mascaraR1 = cv2.dilate(mascaraR, kernel, iterations=2)
    return mascaraR1

#funcion que dibuja los rectangulos en las esquinas de la pantalla
def dibujarRectangulos(img):
    # Verde
    cv2.rectangle(img, (190, 100), (300, 200), (196, 230, 0), 3)
    # Azul
    cv2.rectangle(img, (380, 100), (487, 200), (196, 230, 0), 3)
    # Rojo
    cv2.rectangle(img, (380, 380), (487, 280), (196, 230, 0), 3)
    # Amarillo
    cv2.rectangle(img, (320, 380), (200, 280), (196, 230, 0), 3)

#Funcion para encontrar el rango hsv del color azul
def buscarAzul(hsv):
    #azulMin = np.array([49, 50, 50], np.uint8)
    #azulMax = np.array([100, 255, 210], np.uint8)
    azulMin = np.array([105, 100, 100], np.uint8)
    azulMax = np.array([130, 255, 255], np.uint8)
    azul = cv2.inRange(hsv, azulMin, azulMax)
    return azul


#Funcion para seguir el color azul
def seleccionarRespuesta_a(img, azulM):
    (contours, hierarchy) = cv2.findContours(azulM, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    numero=0
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(img, (int(x), int(y)), int(radius), (0, 0, 0), 2)
            cv2.circle(img, center, 5, (255, 255, 255), -1)
            cv2.putText(img, "AZUL", (int(x - radius), int(y - (radius + 10))), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)
            if x < 300 and y < 200:

                numero = 1
            if x > 387 and y < 200:

                numero = 2
            if x > 185 and x < 295 and y > 280 and y < 400:

                numero = 3
            if x > 387 and x < 480 and y > 280 and y < 380 :

                numero = 4

    return numero
def dibujarEmpezar(img):
    # Verde
    cv2.rectangle(img, (200, 130), (470, 300), (196, 230, 0), 3)

def seleccionarempezar(img, azulM):
    (contours, hierarchy) = cv2.findContours(azulM, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    emp = 0
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(img, (int(x), int(y)), int(radius), (0, 0, 0), 2)
            cv2.circle(img, center, 5, (255, 255, 255), -1)
            cv2.putText(img, "AZUL", (int(x - radius), int(y - (radius + 10))), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)
            if x < 470 and y < 300:
                emp = 8

    return emp

r = random.randint(1, 5)
r2 = random.randint(1, 5)
starting_point = time.time()
numero_s = 0
rsm = random.randint(1, 5)
rsm2 = random.randint(1, 5)
rsm3 = random.randint(1, 5)
rsm4 = random.randint(1, 5)
rsm5 = random.randint(1, 5)
rsm6 = random.randint(1, 5)
num_m1 = r * r2
num_m2 = rsm*rsm2
num_m3 = rsm3*rsm4
num_m4 = rsm5*rsm6
lista = [num_m1,num_m2,num_m3,num_m4]
random.shuffle(lista)

pres_n1 = lista[0]
pres_n2 = lista[1]
pres_n3 = lista[2]
pres_n4 = lista[3]
ress= 0
cap=0
mtap=0
mixer.init()
mixer.music.load('/home/edison/Escritorio/Tracking_objects_3-master/Code/cetus.mp3')
mixer.music.play()
start_time = time.time()
valorpuntuacion = 0
contador_multiplicaciones = 0
archivof = cv2.imread("imagen/bien.jpg")
tristef = cv2.imread("imagen/triste.png")
puntajef = cv2.imread("imagen/puntuacion.jpg")
valorstart =0
conttemp = 0
tiempo_men_int =0
numt = 1
while (1):
    _, img1 = cam.read()
    img = invertirImagen(img1)
    hsv = convertirHSV(img)
    azulB = buscarAzul(hsv)
    azulM = transformacionesMorfologicas(azulB)
    numeroemp= seleccionarempezar(img,azulM)
    tiempo_lapso_int = 0
    if numeroemp == 8:
        tiempo_lapso = time.time () - start_time
        tiempo_lapso_int = int(tiempo_lapso)
    else:
        start_time = time.time()

    if numeroemp == 8 and tiempo_lapso_int >= 3:
        valorstart = 1
    if valorstart == 0:
        dibujarEmpezar(img)
        cv2.putText(img, "Iniciar", (250,230), cv2.FONT_HERSHEY_SIMPLEX, 2, (3, 255,138), 6)
        print(numeroemp)
    if valorstart == 1:
        if valorpuntuacion > 0 and contador_multiplicaciones > 5:
            cv2.putText(puntajef,"Puntaje: "+str(valorpuntuacion), (45, 370), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.imshow("Mensaje", puntajef)
            if numt == 1:
                starttimemen = time.time()
            else:
                tiempo_men = time.time () - starttimemen
                tiempo_men_int = int(tiempo_men)
            numt = 0
            if tiempo_men_int >=10:
                cv2.destroyAllWindows()
                valorstart = 0
                contador_multiplicaciones=0
                valorpuntuacion=0

        if contador_multiplicaciones <=5:
            numeroseleccion = seleccionarRespuesta_a(img,azulM)
            if numeroseleccion > 0:
                if conttemp == 0:
                    selecstart = time.time()
                    conttemp = 1
                print(numeroseleccion)
                tiempo_e = time.time()
                lapso_tiempo = time.time() - selecstart
                lapso_tiempo_int = int(lapso_tiempo)
                if lapso_tiempo_int == 3:
                    tiempo_e = time.time()
                    if numeroseleccion == 1:
                        numero_s = 1
                    if numeroseleccion == 2:
                        numero_s = 2
                    if numeroseleccion == 3:
                        numero_s = 3
                    if numeroseleccion == 4:
                        numero_s = 4
                numeroseleccion = 0
            else:
                conttemp = 0

            if numero_s == 1:
                cv2.circle(img, (240, 150), 83, (0, 255, 0), 3)
            if numero_s == 2:
                cv2.circle(img, (430, 150), 83, (0, 255, 0), 3)
            if numero_s == 3:
                cv2.circle(img, (260, 330), 83, (0, 255, 0), 3)
            if numero_s == 4:
                cv2.circle(img, (440, 340), 83, (0, 255, 0), 3)

            elapsed_time = time.time () - starting_point
            elapsed_time_int = int(elapsed_time)
            cv2.putText(img, "Cuanto es:"+ str(r)+" * "+str(r2) , (40,80), cv2.FONT_HERSHEY_DUPLEX, 2, (3, 255,138), 2)

            cv2.putText(img, str(pres_n1), (200,170), cv2.FONT_HERSHEY_DUPLEX, 2, (3, 255,138), 3)
            cv2.putText(img, str(pres_n2), (400,170), cv2.FONT_HERSHEY_DUPLEX, 2, (3, 255,138), 3)
            cv2.putText(img, str(pres_n3), (210,340), cv2.FONT_HERSHEY_DUPLEX, 2, (3, 255,138), 3)
            cv2.putText(img, str(pres_n4), (400,340), cv2.FONT_HERSHEY_DUPLEX, 2, (3, 255,138), 3)

            if elapsed_time_int > 12:
                contador_multiplicaciones = contador_multiplicaciones + 1
                resultado_multip = r * r2
                #print(resultado_multip)
                if numero_s == 1:
                    if (pres_n1 == resultado_multip):
                        ress = 1
                        valorpuntuacion = valorpuntuacion + 10
                    else:
                        ress = 3
                if numero_s == 2:
                    if (pres_n2 == resultado_multip):
                        ress = 1
                        valorpuntuacion = valorpuntuacion + 10
                    else:
                        ress = 3
                if numero_s == 3:
                    if (pres_n3 == resultado_multip):
                        ress = 1
                        valorpuntuacion = valorpuntuacion + 10
                    else:
                        ress = 3
                if numero_s == 4:
                    if (pres_n4 == resultado_multip):
                        ress = 1
                        valorpuntuacion = valorpuntuacion + 10
                    else:
                        ress = 3

                r = random.randint(1, 5)
                r2 = random.randint(1, 5)
                starting_point = time.time()
                rsm = random.randint(1, 5)
                rsm2 = random.randint(1, 5)
                rsm3 = random.randint(1, 5)
                rsm4 = random.randint(1, 5)
                rsm5 = random.randint(1, 5)
                rsm6 = random.randint(1, 5)
                num_m1 = r * r2
                num_m2 = rsm*rsm2
                num_m3 = rsm3*rsm4
                num_m4 = rsm5*rsm6
                lista = [num_m1,num_m2,num_m3,num_m4]
                random.shuffle(lista)
                pres_n1 = lista[0]
                pres_n2 = lista[1]
                pres_n3 = lista[2]
                pres_n4 = lista[3]
                numero_s = 0
                cap = 0
                mtap = 0
                print("Se acabo el tiempo")

            if ress == 1:
                print("entra")
                if cap == 0:
                    tiempo_e1 = time.time()
                    cap = cap + 1
                lapso_tiempo1 = time.time () - tiempo_e1
                lapso_tiempo_int1 = int(lapso_tiempo1)
                if lapso_tiempo_int1 < 5:
                    cv2.putText(archivof, "Muy Bien, Sigue Asi", (45, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
                    cv2.imshow("Mensaje", archivof)
                if lapso_tiempo_int1 == 5:
                    cv2.destroyAllWindows()
                    ress = 0

            if ress == 3:
                if mtap == 0:
                    tiempo_e2 = time.time()
                    mtap = mtap + 1
                lapso_tiempo2 = time.time () - tiempo_e2
                lapso_tiempo_int2 = int(lapso_tiempo2)
                if lapso_tiempo_int2 < 5:
                    cv2.putText(tristef, "Tu Puedes, sigue intentando...!", (45, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
                    cv2.imshow("Mensaje", tristef)

                if lapso_tiempo_int2 == 5:
                    cv2.destroyAllWindows()
                    ress = 0

            dibujarRectangulos(img)


    cv2.imshow("Play and learn multiplication tables", img)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cam.release()
        cv2.destroyAllWindows()
        break
