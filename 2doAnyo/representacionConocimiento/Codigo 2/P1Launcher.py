'''
 ' Código principal de la aplicación para la práctica 1 de RyRDC
 ' No puede ser modificado por los alumnos
 ' 
 ' Creado por Diego Viejo
 ' el 16/09/2024
'''

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference



import pygame
from robot import *
from segmento import *
from expertSystem import *
AppTitle = "RRDC P1 2024"

RADIUS = 8 # Radio de dibujo para los puntos objetivo


# pygame setup
pygame.init()
sizeY = 720 #Necesario para adaptar las coordenadas del entorno a las de la pantalla de pygame
screen = pygame.display.set_mode((1280, sizeY))
clock = pygame.time.Clock()
running = True

miRobot = Robot()
robotIimage = pygame.image.load('robot1.png').convert_alpha();

def drawRobot(pose):
    #from Aleksandar haber
    # over here we rotate an image and create a copy of the rotated image 
    image1 = pygame.transform.rotate(robotIimage, pose[2])
    # then we return a rectangle corresponding to the rotated copy
    # the rectangle center is specified as an argument
    image1_rect = image1.get_rect(center=(10.0*pose[0], sizeY - 10.0*pose[1]))
    # then we plot the rotated image copy with boundaries specified by 
    # the rectangle
    screen.blit(image1, image1_rect)


path1 = segmento()

def drawSegment(Inic, Fin, activo=True):
    pInicio = (Inic[0]*10.0, sizeY-Inic[1]*10.0)
    pFin = (Fin[0]*10.0, sizeY-Fin[1]*10.0)
    if activo is True:
        colorInicio = "green"
        colorFin = "red"
        colorLinea = "darkgray"
    else:
        colorInicio = "lightgray"
        colorFin = "darkgray"
        colorLinea = "gray"
    pygame.draw.line(screen, colorLinea, pInicio, pFin, 5)
    pygame.draw.circle(screen, colorInicio, pInicio, RADIUS)
    pygame.draw.circle(screen, colorFin, pFin, RADIUS)



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
    drawSegment(path1.getInicio(), path1.getFin(), True)
    drawRobot(miRobot.getPose())
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
