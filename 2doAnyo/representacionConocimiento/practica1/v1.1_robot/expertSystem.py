import math
import numpy as np

class ExpertSystem:
    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.estado = 1
        self.previous_linear_velocity = 0.0
        self.previous_angular_velocity = 0.0
        self.primerSegmento = True

    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.estado = 1
        self.previous_linear_velocity = 0.0
        self.previous_angular_velocity = 0.0
    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        return np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)

    @staticmethod
    def get_point_on_segment(t, start_point, end_point):
        return (1 - t) * np.array(start_point) + t * np.array(end_point)

    def tomarDecision(self, poseRobot):
        #Definicion de constantes
        #No importa si la velocidad lineal o angular es mayor ya que el programa tiene una capa que lo regula 
        VMAX = 3.0
        WMAX = 1.0
        #las constantes de aceleracion y frenado son importantes a la hora de calcular la velocidad lineal y angular para no derrapar ni pasarse del objetivo
        VACC = 1.0
        WACC = 0.5
        
        FPS = 60



        #Definicion de variables
        inicio = np.array(self.segmentoObjetivo.getInicio())
        fin = np.array(self.segmentoObjetivo.getFin())

        toleracionFinSegmento= 0.5
        toleranciaDistanciaSegmento= 0.1

        #Calculo de la distancia al segmento
        dist = np.abs(self.straightToPointDistance(inicio, fin, np.array(poseRobot[0:2])))
        x, y, theta = poseRobot[0], poseRobot[1], math.radians(poseRobot[2])

        #Caluculo del punto mas cercano del segmento
        t = ((x - inicio[0]) * (fin[0] - inicio[0]) + (y - inicio[1]) * (fin[1] - inicio[1])) / ((fin[0] - inicio[0]) ** 2 + (fin[1] - inicio[1]) ** 2)
        puntoMasCercano = self.get_point_on_segment(t, inicio, fin)

        #Calculo de la distancia al punto mas cercano
        distanciaPuntoMasCercano = np.linalg.norm(puntoMasCercano - poseRobot[0:2])

        # Calculo de la distancia al punto final del segmento
        distanciaPuntoFinal = np.linalg.norm(fin - poseRobot[0:2])
        
        if self.estado == 1 or dist > toleracionFinSegmento:
            self.estado = 1
            # target punto mas cercano del segmento
            # cuando se este acercando ir cambiando la orientacion en base a una variable para reducir la frenada de aceleracion lineal y angular
            if dist <= toleranciaDistanciaSegmento: 
                self.estado = 2
        elif self.estado == 2:
            # target al final del segmento, siempre al ser posible sin que dist > toleracionFinSegmento
            if distanciaPuntoFinal <= toleracionFinSegmento:
                self.estado = 3

        elif self.estado == 3:
            self.primerSegmento = False
            self.esObjetivoAlcanzado = True
            #cuando es objetivo alcanzado sea True otro segmento será generado y volvera al estado 1 para intentar llegar al final del segundo segmento, ten en cuenta que no habrá mas de dos segmentos

        



        return velocidad_lineal, velocidad_angular

    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False