'''
 ' Clase Robot
 ' Implementa la dinámica de un robot diferencial
 ' Lo controlamos con comandos de velocidad lineal y velocidad angular
 ' Mantiene una representación de su Pose
 ' Puede pintarse en un objeto screen de pygame de acuerdo a su Pose. Esto puede cambiar en versiones posteriores
 ' No puede ser modificado por los alumnos
 ' 
 ' Creado por Diego Viejo
 ' el 19/09/2024
'''



import pygame
import numpy as np
import math

RADIOROBOT = 0.15
BGCOLOR = "black"
VMAX = 3 #m/s
WMAX = 1 #rad/s
VACC = 1 #m/s2
WACC = 0.5 #rad/s2


class Robot:
    def __init__(self, sizeY):
        self.sizeY = sizeY #Necesario para adaptar las coordenadas del entorno a las de la pantalla de pygame

        self.coordX = 0.0
        self.coordY = 0.0
        self.heading = 0.0 #vector (1,0) in degrees

        self.linearVel = 0
        self.angularVel = 0 
        self.actualLinearVel = 0
        self.actualAngularVel = 0

        self.image = pygame.image.load('robot1.png').convert_alpha();
    
    def setPose(self, pose):
        self.coordX = pose[0]
        self.coordY = pose[1]
        self.heading = pose[2]
    
    def getPose(self):
        return (self.coordX, self.coordY, self.heading)

    def setVel(self, velocidades):

        self.linearVel = velocidades[0]
        if self.linearVel > VMAX:
            self.linearVel = VMAX
        if self.linearVel < -VMAX:
            self.linearVel = -VMAX

        self.angularVel = velocidades[1]
        if self.angularVel > WMAX:
            self.angularVel = WMAX
        if self.angularVel < -WMAX:
            self.angularVel = -WMAX
    
    def drawRobot(self, screen):
        #from Aleksandar haber
        # over here we rotate an image and create a copy of the rotated image 
        image1 = pygame.transform.rotate(self.image,self.heading)
        # then we return a rectangle corresponding to the rotated copy
        # the rectangle center is specified as an argument
        image1_rect = image1.get_rect(center=(10.0*self.coordX, self.sizeY - 10.0*self.coordY))
        # then we plot the rotated image copy with boundaries specified by 
        # the rectangle
        screen.blit(image1, image1_rect)


    #
    def updateDynamics(self, timelapse):
        a = 1
        # Partimos de V y W
        # Actualizamos las velocidades si todavía no se ha llegado a la velocidad deseada!!!!!!
        timeSeconds = timelapse / 1000.0


        #Actualizamos velocidades
        changeV = VACC * timeSeconds
        changeW = WACC * timeSeconds
        if self.actualLinearVel < self.linearVel:
            self.actualLinearVel = self.actualLinearVel + changeV
            if self.actualLinearVel > VMAX:
                self.actualLinearVel = VMAX
        if self.actualLinearVel > self.linearVel:
            self.actualLinearVel = self.actualLinearVel - changeV
            if self.actualLinearVel < -VMAX:
                self.actualLinearVel = -VMAX
        if self.linearVel == 0 and abs(self.actualLinearVel)<changeV:
            self.actualLinearVel = 0

        if self.actualAngularVel < self.angularVel:
            self.actualAngularVel = self.actualAngularVel + changeW
            if self.actualAngularVel > WMAX:
                self.actualAngularVel = WMAX
        if self.actualAngularVel > self.angularVel:
            self.actualAngularVel = self.actualAngularVel - changeW
            if self.actualAngularVel < -WMAX:
                self.actualAngularVel = -WMAX
        if self.angularVel == 0 and abs(self.actualAngularVel)<changeW:
            self.actualAngularVel = 0

        # calculamos cuántos grados hay que girar por el tiempo que ha pasado (si W>0)
        #   obtenemos el ICC y aplicamos la rotación
        #   o calculamos la traslación en linea recta también ponderada por el tiempo que ha pasado
        if self.actualAngularVel != 0:
            if self.actualLinearVel != 0:
                ICCRad = self.actualLinearVel/self.actualAngularVel
                
                headingRad = (90-self.heading) * math.pi / 180
                ICCgx = self.coordX - ICCRad * math.cos(headingRad)
                ICCgy = self.coordY + ICCRad * math.sin(headingRad)

                ICCtgx = self.coordX - ICCgx
                ICCtgy = self.coordY - ICCgy

                rotatedICCx = ICCtgx * math.cos(self.actualAngularVel*timeSeconds) - ICCtgy * math.sin(self.actualAngularVel*timeSeconds)
                rotatedICCy = ICCtgx * math.sin(self.actualAngularVel*timeSeconds) + ICCtgy * math.cos(self.actualAngularVel*timeSeconds)


                self.coordX = rotatedICCx + ICCgx
                self.coordY = rotatedICCy + ICCgy
            #else: #rotation around robot center
            acAngVelDeg = self.actualAngularVel*180/math.pi
            self.heading = self.heading + acAngVelDeg * timeSeconds 
        else:
            #linea recta
            dist = self.actualLinearVel * timeSeconds
            angleRad = self.heading * math.pi / 180
            self.coordX = self.coordX + dist*math.cos(angleRad)
            self.coordY = self.coordY + dist*math.sin(angleRad)

