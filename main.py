import pygame
import math
import requests
from widgets import *
import serial
import time

# Valor igual a 0, 90, 180, o 270 que determina la dirección a la cual está orientada el carro
direccionCarro = 0
# Coordenadas del carro
posCarroX = 0
posCarroY = 0
# Distancia a la que se mueve el carro cada vez que avanza
movimiento = 25
# Variables de apoyo para el comportamiento del carro durante la detección de obstáculos
giros = 0
anterior = False
# Distancia a la cual llega el escaneo
escaneo = 50
# Variables para controlar bucles de operacion
correr = True
scan = True

# Datos de ventana de opciones
pygame.init()

ancho = 350
alto = 125
tamano = (ancho, alto)
pantalla = pygame.display.set_mode(tamano)

pygame.display.set_caption("Opciones")

# Arreglo para almacenar coordenadas de obstáculos
obstaculos = []

# URL de módulo WiFi ESP8266
# !!! CAMBIAR SI EL MODULO WIFI DA UNA DIRECCIÓN IP DISTINTA AL INICIALIZARSE
url = "http://196.168.0.25/"

arduino = serial.Serial("COM3", baudrate=9600, timeout=.1)

# Prueba
def dibujarObstaculo(posX, posY):
    pygame.draw.circle(pantalla,(0,0,0),((ancho//2)+posX,(alto//2)+posY),1)

# Dibujar todos los obstáculos almacenados, tomando como (0,0) al centro de la ventana, y compensando por la posición actual del carro
def dibujarObstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.circle(pantalla,(0,0,0),((ancho//2)+(obstaculo[0]*2),(alto//2)+(obstaculo[1]*2)),1)
        # pygame.draw.circle(pantalla,(0,0,0),((ancho//2)+(obstaculo[0]//2),(alto//2)+(obstaculo[1]//2)),1)

# Enviar y recibir datos de monitor serial
def transmit(text):
    arduino.write(bytes(text, "utf-8"))
    time.sleep(0.05)
    data = arduino.readline()
    return data

# Enviar solicitud a Arduino para realizar el escaneo y recibir el dato de la ubicación del obstáculo
def escanear(obstaculos, direccionCarro, posCarroX, posCarroY):
    global escaneo
    transmit('f')
    for posicion in range(181):
        #server = int(requests.get(url + "escanear/").text)

        # Calcular la distancia hacia el obstáculo
        #distancia = int(server * 0.017)
        distancia = int(transmit('e').decode())

        # Calcular la distancia X y Y del obstáculo
        coord = []
        coord.append(int((distancia * math.cos(math.radians(posicion + direccionCarro))) + posCarroX))
        coord.append(int((distancia * math.sin(math.radians(posicion + direccionCarro))) + posCarroY))

        duplicado = False

        # Limitar la distancia de detección de obstáculos
        if distancia <= escaneo:
            # Revisar si la coordenada del obstáculo ya se encuentra registrada
            for obstaculo in obstaculos:
                if coord[0] == obstaculo[0] and coord[1] == obstaculo[1]:
                    duplicado = True

            # Si la coordenada no corresponde a un obstáculo registrado, agregarlo a la lista
            if duplicado == False:
                obstaculos.append(coord)
                dibujarObstaculos(obstaculos)
                pygame.display.flip()

# Funcion de ayuda para determinar que datos usar en el calculo de coordenadas
def determinarDatosDireccion(direccionDeteccion):
    global posCarroX
    global posCarroY
    global escaneo
    global direccionCarro

    datos = []

    if direccionDeteccion == "i":
        if direccionCarro == 0 or direccionCarro == 90:
            datos.append((-1 * escaneo) - 1)
            datos.append(-1)
            return datos
        else:
            datos.append(escaneo + 1)
            datos.append(1)
            return datos
    elif direccionDeteccion == "f":
        if direccionCarro == 0 or direccionCarro == 270:
            datos.append(escaneo + 1)
            datos.append(1)
            return datos
        else:
            datos.append((-1 * escaneo) - 1)
            datos.append(-1)
            return datos
    else:
        if direccionCarro == 0 or direccionCarro == 90:
            datos.append(escaneo + 1)
            datos.append(1)
            return datos
        else:
            datos.append((-1 * escaneo) - 1)
            datos.append(-1)
            return datos
    
# Funcion de ayuda para determinar las coordenadas X y Y
def determinarCoordenadas(angulo, pos, direccionDeteccion):
    global posCarroX
    global posCarroY
    global direccionCarro

    coordenadas = []
    # Dependiendo del ángulo, se usa tangente o cotangente más la posición X o Y del carro para encontrar las coordenadas
    if direccionDeteccion == "f":
        if direccionCarro == 0 or direccionCarro == 180:
            if angulo == 90 or angulo == 270:
                coordenadas.append(posCarroX)
            else:
                coordenadas.append(int((pos / math.tan(math.radians(angulo))) + posCarroX))
            coordenadas.append(pos + posCarroY)
        else:
            coordenadas.append(pos + posCarroX)
            coordenadas.append(int((pos * math.tan(math.radians(angulo))) + posCarroY))
    else:
        if direccionCarro == 0 or direccionCarro == 180:
            coordenadas.append(pos + posCarroX)
            coordenadas.append(int((pos * math.tan(math.radians(angulo))) + posCarroY))
        else:
            if angulo == 270 or angulo == 450:
                coordenadas.append(posCarroX)
            else:
                coordenadas.append(int((pos / math.tan(math.radians(angulo))) + posCarroX))
            coordenadas.append(pos + posCarroY)

# Detectar si hay un obstaculo a la izquierda
def detectarObstaculoIzquierda(obstaculos, direccionCarro, giros):
    global anterior
    
    # Detectar si se debe interrumpir el mapeo
    interrumpir()
    # Escanear para ver si hay obstáculos nuevos
    escanear(obstaculos, direccionCarro)
    
    # La variable y mide 45° a la izquierda del carro, sumando direccionCarro para compensar por el giro
    for angulo in range(180 + direccionCarro, 134 + direccionCarro, -1):
        # La variable pos mide hasta la distancia de mapeo, sumando la posicion x o y del carro segun corresponda para compensar por la posicion del carro
        # La combinación de posX y posY detecta obstáculos en un área equivalente a un triángulo rectángulo de 45° a una distancia definida hacia la izquierda
        datos = determinarDatosDireccion("i")
        for pos in range(0, datos[0], datos[1]):
            coordenadas = determinarCoordenadas(angulo, pos, "i")
            posX = coordenadas[0]
            posY = coordenadas[1]
            duplicado = False

            # Revisar si la coordenada ya se encuentra registrada como un obstáculo
            for obstaculo in obstaculos:
                if posX == obstaculo[0] and posY == obstaculo[1]:
                    duplicado = True
            
            # Significa que hay un obstaculo a la izquierda, continuar a verificar obstaculo al frente
            if duplicado == True:
                # Asignar que el último escaneo detectó un obstáculo a la izquierda
                anterior = True
                # Resetear los giros dados a la izquierda
                giros = 0

                return "f"
            else:
                # Si no hay un obstáculo al frente, y el último escaneo detectó un obstáculo a la izquierda, girar a la izquierda y avanzar
                if anterior == True:
                    # Resetear la detección de obstáculos a la izquierda
                    anterior = False

                    girarIzquierda()
                    avanzar()
                    return "i"

                # Resetear la detección de obstáculos a la izquierda
                anterior = False

                # Si se han hecho tres giros a la izquierda sin encontrar obstáculos, girar el carro a la derecha, apuntando hacia atrás, y avanzar hasta encontrar un obstáculo al frente
                if giros == 3:
                    girarDerecha(direccionCarro)
                    return "f"

                # Significa que no hay un obstaculo a la izquierda, girar a la izquierda y aumentar la cantidad de giros dados
                girarIzquierda(direccionCarro)
                giros += 1
                return "i"

# Detectar si hay un obstaculo al frente
def detectarObstaculoFrente(obstaculos, direccionCarro, giros):
    global escaneo

    # Detectar si se debe interrumpir el mapeo
    interrumpir()

    # La variable x mide 90° al frente del carro, sumando direccionCarro para compensar por el giro
    for angulo in range(135 + direccionCarro, 44 + direccionCarro, -1):
        # La variable posY mide hasta la distancia de mapeo, sumando posCarroY para compensar por la posicion del carro
        # La combinación de x y posY detecta obstáculos en un área equivalente a un triángulo rectángulo de 90° a una distancia definida hacia el frente
        datos = determinarDatosDireccion("f")
        for pos in range(0, datos[0], datos[1]):
            coordenadas = determinarCoordenadas(angulo, pos, "f")
            posX = coordenadas[0]
            posY = coordenadas[1]
            duplicado = False

            # Revisar si la coordenada ya se encuentra registrada como un obstáculo
            for obstaculo in obstaculos:
                if posX == obstaculo[0] and posY == obstaculo[1]:
                    duplicado = True

            # Significa que hay un obstaculo al frente, continuar a verificar obstaculo a la derecha
            if duplicado == True:
                return "d"
            else:
                # Si giros = 3, el carro está viendo hacia atrás, entonces se avanza al frente y se escanea hasta encontrar un obstáculo al frente
                if giros == 3:
                    avanzar()
                    escanear(obstaculos, direccionCarro)
                    return "f"

                # Significa que no hay un obstaculo al frente, avanzar al frente
                avanzar()
                return "i"
          
# Detectar si hay un obstaculo a la derecha
def detectarObstaculoDerecha(obstaculos, direccionCarro, giros):
    # Detectar si se debe interrumpir el mapeo
    interrumpir()

    # La variable y mide 45° a la izquierda del carro, sumando direccionCarro para compensar por el giro
    for angulo in range(45 + direccionCarro, -1 + direccionCarro, -1):
        # La variable posX mide hasta la distancia de mapeo, sumando posCarroX para compensar por la posicion del carro
        # La combinación de y y posX detecta obstáculos en un área equivalente a un triángulo rectángulo de 45° a una distancia definida hacia la derecha
        datos = determinarDatosDireccion("d")
        for pos in range(0, datos[0], datos[1]):
            coordenadas = determinarCoordenadas(angulo, pos, "d")
            posX = coordenadas[0]
            posY = coordenadas[1]
            duplicado = False

            # Revisar si la coordenada ya se encuentra registrada como un obstáculo
            for obstaculo in obstaculos:
                if posX == obstaculo[0] and posY == obstaculo[1]:
                    duplicado = True

            # Significa que hay un obstaculo a la derecha, continuar a moverse hacia atrás
            if duplicado == True:
                retroceder()
                return "d"
            else:
                # Significa que no hay un obstaculo a la derecha, girar a la derecha
                girarDerecha(direccionCarro)

                # Resetear los giros dados a la izquierda
                if giros == 3:
                    giros = 0

                avanzar()
                return "i"

# Código para mover el carro al frente
def avanzar():
    global movimiento
    # server = requests.post(url + "avanzar/").text
    # print(server)
    print("avanzar")
    time.sleep(2)

    # Cambiar las coordenadas del carro dependiendo de la dirección a la que está orientado
    if direccionCarro == 0:
       posCarroY += movimiento
    elif direccionCarro == 90:
       posCarroX -= movimiento
    elif direccionCarro == 180:
       posCarroY -= movimiento
    else:
       posCarroX += movimiento
    pass

# Código para mover el carro hacia atrás
def retroceder(obstaculos, direccionCarro, giros):
    # server = requests.post(url + "retroceder/").text
    # print(server)
    print("retroceder")
    time.sleep(2)

    # Cambiar las coordenadas del carro dependiendo de la dirección a la que está orientado
    if direccionCarro == 0:
       posCarroY -= movimiento
    elif direccionCarro == 90:
       posCarroX += movimiento
    elif direccionCarro == 180:
       posCarroY += movimiento
    else:
       posCarroX -= movimiento
    pass

# Código para girar el carro a la izquierda
def girarIzquierda(direccionCarro):
    # server = requests.post(url + "izquierda/").text
    # print(server)
    print("izquierda")
    time.sleep(2)

    # Agregar 90° al cambiar la dirección a la que está orientado el carro, y limitar el rango entre 0° y 360°
    direccionCarro += 90
    if direccionCarro == 360:
        direccionCarro = 0

# Código para girar el carro a la derecha
def girarDerecha(direccionCarro):
    # server = requests.post(url + "derecha/").text
    # print(server)
    print("derecha")
    time.sleep(2)

    # Agregar 270° al cambiar la dirección a la que está orientado el carro, y limitar el rango entre 0° y 360°
    direccionCarro += 270
    if direccionCarro >= 360:
        direccionCarro -= 360

# Funcion para interrumpir el mapeo al pulsar una tecla
def interrumpir():
    global correr
    global scan
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
            scan = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            scan = False

def ventanaPrincipal():
    global obstaculos
    global direccionCarro
    global giros
    global correr
    global scan
    while correr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:              
                correr = False
                pygame.quit()  

        scan = True
        res = "i"
        while scan == True:
            if res == "i":
                res = detectarObstaculoIzquierda(obstaculos, direccionCarro, giros)
            elif res == "f":
                res = detectarObstaculoFrente(obstaculos, direccionCarro, giros)
            else:
                res = detectarObstaculoDerecha(obstaculos, direccionCarro, giros)

        global pantalla
        pantalla.fill((255,255,255))

# Datos de elementos de ventana de opciones
# Lista de elementos a dibujar
elementosOpciones = []

# Elementos
etiquetaAncho = Etiqueta(elementosOpciones,"Ancho:",20,20)
cuadroAncho = CuadroTexto(elementosOpciones,20,45,150,25,(200,200,200))
etiquetaAlto = Etiqueta(elementosOpciones,"Alto:",180,20)
cuadroAlto = CuadroTexto(elementosOpciones,180,45,150,25,(200,200,200))
botonAplicarTamano = Boton(elementosOpciones,"Aplicar tamaño",20,80,310)


# Función para el botón
def botonClic(self):
    global ancho
    global alto
    global pantalla
    global obstaculos
    global direccionCarro
    global giros

    # Definir datos de la ventana principal
    ancho = int(cuadroAncho.texto)
    alto = int(cuadroAlto.texto)
    tamano = (ancho, alto)

    # Cerrar ventana de opciones
    pygame.quit()
    # Inicializar pygame para crear una nueva ventana
    pygame.init()

    # Asignar datos a la ventana
    pantalla = pygame.display.set_mode(tamano)
    pygame.display.set_caption("Mapeo")

    # Iniciar el mapeo
    detectarObstaculoIzquierda(obstaculos, direccionCarro, giros)

# Asignar la función al atributo .clic() del botón
botonAplicarTamano.clic = botonClic.__get__(botonAplicarTamano)

# Ventana de opciones, para elegir el tamaño de la ventana principal
def ventanaOpciones():
    # Bucle principal
    correr = True
    while correr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                correr = False
            # Revisar si se ha dado clic en un elemento
            if event.type == pygame.MOUSEBUTTONDOWN:
                for objeto in elementosOpciones:
                    # Si el elemento es un cuadro de texto, definirlo como activo, si no, desactivarlo
                    if type(objeto) == CuadroTexto:
                        if objeto.rect.collidepoint(event.pos):
                            objeto.activo = True
                        else:
                            objeto.activo = False
                    # Si el elemento es un botón, ejecutar la función asignada a su comportamiento clic()
                    if type(objeto) == Boton:
                        if objeto.rect.collidepoint(event.pos):
                            objeto.clic()
            # Revisar si se ha pulsado una tecla, y si un cuadro de texto está activo, escribir en él
            if event.type == pygame.KEYDOWN:
                for objeto in elementosOpciones:
                    if type(objeto) == CuadroTexto:
                        if objeto.activo == True:
                            objeto.texto += event.unicode
                            objeto.cambiarTexto(objeto.texto)

        # Dibujar elementos en la pantalla
        pantalla.fill((255,255,255))
        dibujarObjetos(pantalla, elementosOpciones)
        pygame.display.flip()

ventanaOpciones()