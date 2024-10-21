import math
import numpy as np

class ExpertSystem:
    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.estado = 1


    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.estado = 1


    def tomarDecision(self, poseRobot):
            #Definicion de constantes
            #No importa si la velocidad lineal o angular es mayor ya que el programa tiene una capa que lo regula 
            VMAX = 3.0
            WMAX = 1.0
            #las constantes de aceleracion y frenado son importantes a la hora de calcular la velocidad lineal y angular para no derrapar ni pasarse del objetivo
            VACC = 1.0
            WACC = 0.5



            #Definicion de variables
            inicio = np.array(self.segmentoObjetivo.getInicio())
            fin = np.array(self.segmentoObjetivo.getFin())

            toleracionFinSegmento= 0.5
            toleranciaDistanciaInicio= 0.5

            x, y, theta = poseRobot[0], poseRobot[1], math.radians(poseRobot[2])

            #Calculo de la distancia al punto mas cercano
            distanciaAinicio = np.linalg.norm(inicio - poseRobot[0:2])

            # Calculo de la distancia al punto final del segmento
            distanciaPuntoFinal = np.linalg.norm(fin - poseRobot[0:2])
            
            if self.estado == 1:
                self.estado = 1
                # target punto mas cercano del segmento
                if distanciaAinicio <= toleranciaDistanciaInicio: 
                    self.estado = 2
            elif self.estado == 2:
                # target al final del segmento, siempre al ser posible sin que dist > toleracionFinSegmento
                if distanciaPuntoFinal <= toleracionFinSegmento:
                    self.estado = 3

            elif self.estado == 3:
                self.esObjetivoAlcanzado = True
                #cuando es objetivo alcanzado sea True otro segmento será generado y volvera al estado 1 para intentar llegar al final del segundo segmento, ten en cuenta que no habrá mas de dos segmentos

            
        

            return velocidad_lineal, velocidad_angular
    
    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False