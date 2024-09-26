'''
 ' Código principal de la aplicación para la práctica 1 de RyRDC
 ' No puede ser modificado por los alumnos
 '
 ' Creado por Diego Viejo
 ' el 16/09/2024
'''


import pygame
from robot import *
from segmento import *
from expertSystem import *
AppTitle = "RRDC P1 2024"



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

miRobot = Robot(720)
path1 = segmento(720)

experto = ExpertSystem()
experto.setObjetivo(path1)

miRobot.setPose((10,10,10))

path1.setInicio((22, 34))
path1.setFin((95,62))

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    # RENDER YOUR GAME HERE
    path1.drawSegment(screen)
    miRobot.drawRobot(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    timeLapse = clock.tick(60)
    miRobot.updateDynamics(timeLapse)
    if experto.esObjetivoAlcanzado():
        miRobot.setVel((0,0))
        #TODO: comunicar puntuación de la trayectoria
    else:
        velocidades = experto.tomarDecision(miRobot.getPose())
        miRobot.setVel(velocidades)


# this is important, run this if the pygame window does not want to close
pygame.quit()
