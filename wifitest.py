import pygame
import serial
import time

pygame.init()

ancho = 350
alto = 125
tamano = (ancho, alto)
pantalla = pygame.display.set_mode(tamano)

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

pygame.display.set_caption("Opciones")

def transmit(text):
    arduino.write(bytes(text, "utf-8"))
    #time.sleep(0.02)
    data = arduino.readline()
    return data


run = True
while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            rec = transmit('a')
            for i in range(181):
                rec = transmit('e').decode()
                #time.sleep(0.005)
                print(str(i) + ": " + rec)