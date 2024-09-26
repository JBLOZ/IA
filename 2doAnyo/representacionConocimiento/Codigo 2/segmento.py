'''
 ' Clase segmento
 ' Representa un segmento, con un comienzo y un final, en el plano XY
 ' Puede pintarse en un objeto screen de pygame.  Esto puede cambiar en versiones posteriores
 ' No puede ser modificado por los alumnos
'''

import pygame

RADIUS = 8

class segmento:
    def __init__(self, sizeY):
        self.pInicio = (0, 0)
        self.pFin = (0, 0)
        self.sizeY = sizeY

    def setInicio(self, inicio):
        self.pInicio = inicio
    
    def setFin(self, fin):
        self.pFin = fin

    def drawSegment(self, screen):
        pInicio = (self.pInicio[0]*10.0, self.sizeY-self.pInicio[1]*10.0)
        pFin = (self.pFin[0]*10.0, self.sizeY-self.pFin[1]*10.0)
        pygame.draw.line(screen, "darkgray", pInicio, pFin, 5)
        pygame.draw.circle(screen, "green", pInicio, RADIUS)
        pygame.draw.circle(screen, "red", pFin, RADIUS)

    # Obtiene el punto de inicio del segmento
    def getInicio(self):
        return self.pInicio
    
    # Obtiene el punto final del segmento
    def getFin(self):
        return self.getFin
